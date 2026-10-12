#!/usr/bin/env python
"""make_wear.py: the 33 kinds of wear mask of Quay Street, by script, from the wear target (unit 4.5, cloud week 42).

    /home/user/.bpyenv/bin/python make_wear.py OUTDIR [--only streak_sill,gum] [--seed-base 1990] [--jobs 4] [--no-refine]
    python make_wear.py OUTDIR --verify

Reads  production/cloud-week/targets/wear/target.json and its drawing module target_drawing.py (the shape envelope of each kind in millimetres: its rule of place, size and shape).
Writes into OUTDIR (never into git):
       <kind>/<kind>_v<N>.png     one 16-bit greyscale mask per variant (the kind's own `variants.count`: 3 to 10), 65535 = the kind's full effect (mask 1.0), row 0 the TOP of the
                                  decal frame, column 0 its left, at the kind's recommended texel scale (`texel.px_per_m_recommended`), over the frame `mask.frame_extent_m`
       manifest.json              each file: the kind, variant, seed, size in pixels and metres, px/m, wrap behaviour (seamless tile, tile along x, stamp), the origin text, the tone rows, the wet
                                  and dry multipliers, the variants' differences, and the SHA-256 of the pixels
What this adds to the target's own envelope drawing (and what it keeps): the envelope is rasterised exactly as the target's checks read it (levels, then the stated 10-90 per cent edge), then
(1) the edges are warped by a few tenths of a millimetre of noise (so that no edge is a ruled polygon's), and (2) a soft kind's strength varies a little inside its marks (up to 12 per cent, in
patches 4 to 8 times its smallest feature, wrapping where the kind tiles). Hard-edged kinds (cracks, flakes, discs, lines) and the kinds whose checks read where a level crosses a threshold (the foot and head bands, the salt, the gutter, the sign ghost) get the warp only. check_wear.py shows that both leave every one of the
target's mask checks where the plain envelope has them.
Deterministic: every random draw comes from (seed base, kind, variant); the same seed gives the same pixels.
"""
import argparse
import json
import platform
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wear_common as wc          # noqa: E402

SCHEMA = "ledger.cloud-week-42.wear-masks-manifest/1"
HARD = {"paint_flake", "render_crack", "road_crack", "flag_patch_crack", "line_wear", "grate_wear", "cig_end", "gum", "rust_bleed", "render_patch", "poster_remnant", "bird_dropping", "tyre_scuff"}
# kinds whose checks read WHERE a level crosses a threshold (the band's top edge on a brick course, its column profile, the peak): a strength variation would slide that line, so they take the warp only
EDGE_KINDS = {"wall_foot_splash", "wall_foot_damp", "wall_head_band", "salt_bloom", "gutter_grime", "sign_ghost"}
TRIES = 12                # seeds tried per variant until its mask passes every check of its kind on its own
MOD_DEPTH = 0.12          # a soft kind's strength varies inside its marks by up to this much
_G = {}


def init():
    tj, draw, scw = wc.load_target()
    _G.update(tj=tj, draw=draw, scw=scw, ed=draw.edges_by_kind(tj))


def seed_for(base, variant):
    return base + 1000 * variant          # the first seed tried; a variant may take up to TRIES - 1 more (the manifest records the one kept)


def refine(m, kid, k, ppm, ed_mm, wrap, rng):
    """Warp the edges by noise (a few tenths of a millimetre) and, for a soft kind, vary the strength a little inside its marks."""
    h, w = m.shape
    warp_px = float(np.clip(0.18 * max(ed_mm, 3.0) * ppm / 1000.0, 0.35, 1.6))
    sc_px = max(2.0, k["texel"]["smallest_feature_mm"] * ppm / 1000.0 * 1.5)
    dx = wc.noise_field((h, w), sc_px, rng, wrap, 1) * warp_px * 0.5
    dy = wc.noise_field((h, w), sc_px, rng, wrap, 1) * warp_px * 0.5
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    mode = "grid-wrap" if wrap in (True, "xy") else "reflect"
    if wrap == "x":
        # periodic along x only: warp rows with wrapped x, reflected y
        out = ndi.map_coordinates(m, [np.clip(yy + dy, 0, h - 1), (xx + dx) % w], order=1, mode="nearest")
    else:
        out = ndi.map_coordinates(m, [yy + dy, xx + dx], order=1, mode=mode)
    if kid not in HARD and kid not in EDGE_KINDS:
        n = wc.noise_field((h, w), k["texel"]["smallest_feature_mm"] * ppm / 1000.0 * 5.0, rng, wrap, 2)
        out = out * np.clip(1.0 - MOD_DEPTH * (0.5 + 0.5 * np.tanh(n)), 0.0, 1.0)
    return np.clip(out, 0.0, 1.0).astype(np.float32)


def make_mask(tj, draw, ed, kid, seed, variant, ppm=None, do_refine=True):
    k = tj["kinds"][kid]
    ext = k["mask"]["frame_extent_m"]
    ext_mm = tuple(v * 1000.0 for v in ext)
    ppm = ppm or k["texel"]["px_per_m_recommended"]
    wrap = wc.wrap_mode(k)
    polys = draw.kind_envelope(tj, kid, seed, variant)
    m = draw.rasterize(polys, ext_mm, ppm, ed.get(kid, 0.0), wrap=wrap)
    if do_refine:
        m = refine(m, kid, k, ppm, ed.get(kid, 0.0), wrap, wc.rng_for(seed, kid, variant, "refine"))
    return m, polys, ppm


def to16(m):
    return np.clip(np.round(m * 65535.0), 0, 65535).astype(np.uint16)


def build_kind(task):
    out, kid, seed_base, do_refine = task
    if not _G:
        init()
    tj, draw, ed = _G["tj"], _G["draw"], _G["ed"]
    k = tj["kinds"][kid]
    t0 = time.time()
    rows = []
    n = int(k["variants"]["count"])
    checks = [c for c in k["checks"] if c.get("applies_to") == "mask" and c["measure"] not in _G["scw"].COMPOSITION_MEASURES]
    for v in range(n):
        # the target tests its ranges on the median of a batch, and says a few kinds pass only 55 to 80 per cent of single masks; a delivered mask is used alone, so each variant takes
        # the first of up to TRIES seeds whose mask passes every one of its kind's checks on its own (or, failing that, the seed with the fewest failing checks)
        best = None
        for t in range(TRIES):
            seed = seed_for(seed_base, v) + t
            m, polys, ppm = make_mask(tj, draw, ed, kid, seed, v, do_refine=do_refine)
            fails = []
            for c in checks:
                try:
                    val, ok = _G["scw"].run_mask_check(c, m, ppm)
                except Exception:     # noqa: BLE001
                    ok = False
                if not ok:
                    fails.append(c["name"])
            if best is None or len(fails) < len(best[3]):
                best = (m, seed, ppm, fails, t + 1)
            if not fails:
                break
        m, seed, ppm, fails, tries = best
        a = to16(m)
        rel = "%s/%s_v%d.png" % (kid, kid, v)
        p = Path(out) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(a).save(p, compress_level=6)
        rows.append(dict(file=rel, variant=v, seed=seed, seeds_tried=tries, failing_checks=fails, size_px=[int(a.shape[1]), int(a.shape[0])], px_per_m=ppm, coverage_half=float((m >= 0.5).mean()),
                         mean=float(m.mean()), max=float(m.max()), sha256_pixels=wc.pix_hash(a)))
    ext = k["mask"]["frame_extent_m"]
    return dict(kind=kid, label=k["label"], layer=k["layer"], frame_extent_m=ext, decal_frame_m=k["mask"]["decal_frame_m"], origin=k["mask"]["origin"], wrap=wc.wrap_mode(k) or "none (a stamp)",
                encoding="16-bit greyscale, 65535 = mask 1.0 (the kind's full effect), row 0 the top of the frame", px_per_m=k["texel"]["px_per_m_recommended"], smallest_feature_mm=k["texel"]["smallest_feature_mm"],
                edge_10_90_mm=ed.get(kid, 0.0), tone=k["tone"], wet_dry=k["wet_dry"], variants_note=k["variants"]["differ_by"], files=rows, seconds=round(time.time() - t0, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--only", default="")
    ap.add_argument("--seed-base", type=int, default=1990)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--no-refine", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    if a.verify:
        ref = json.loads((out / "manifest.json").read_text())
        out2 = Path(str(out) + "_verify")
        sys.argv = [sys.argv[0], str(out2), "--seed-base", str(ref["seed_base"]), "--jobs", str(a.jobs)] + (["--no-refine"] if not ref["refined"] else [])
        main()
        new = json.loads((out2 / "manifest.json").read_text())
        bad = 0
        for r0, r1 in zip(ref["kinds"], new["kinds"]):
            for f0, f1 in zip(r0["files"], r1["files"]):
                if f0["sha256_pixels"] != f1["sha256_pixels"]:
                    bad += 1
                    print("DIFFERS", f0["file"])
        print("verify: %d differing masks of %d" % (bad, sum(len(r["files"]) for r in ref["kinds"])))
        return 0 if not bad else 1
    out.mkdir(parents=True, exist_ok=True)
    init()
    tj = _G["tj"]
    ids = list(tj["kinds_order"])
    if a.only:
        ids = [i for i in ids if i in [s.strip() for s in a.only.split(",")]]
    t0 = time.time()
    tasks = [(str(out), i, a.seed_base, not a.no_refine) for i in ids]
    rows = []
    with Pool(a.jobs, initializer=init) as p:
        for r in p.imap_unordered(build_kind, tasks):
            rows.append(r)
            print("%-18s %2d masks %5.1f s" % (r["kind"], len(r["files"]), r["seconds"]), flush=True)
    rows.sort(key=lambda r: ids.index(r["kind"]))
    import PIL
    man = dict(schema=SCHEMA, made=time.strftime("%Y-%m-%d %H:%M:%S"), seconds=round(time.time() - t0, 1), seed_base=a.seed_base, refined=not a.no_refine,
               versions=dict(python=platform.python_version(), numpy=np.__version__, pillow=PIL.__version__), target=str(wc.TDIR / "target.json"), kinds=rows,
               note="pixels are hashed raw (sha256_pixels); a PNG file's own hash differs between library versions")
    (out / "manifest.json").write_text(json.dumps(man, indent=1), encoding="utf-8")
    print("wrote %d kinds, %d masks in %.0f s" % (len(rows), sum(len(r["files"]) for r in rows), time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
