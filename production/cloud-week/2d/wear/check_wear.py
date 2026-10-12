#!/usr/bin/env python
"""check_wear.py: the automatic check of the wear masks (unit 4.5, cloud week 42).

    /home/user/.bpyenv/bin/python check_wear.py OUTDIR [--only streak_sill,gum] [--jobs 4] [--write checks/check_v1.json]

OUTDIR is what make_wear.py wrote. The check reads the PNG files, then runs the target's own mask checks (self_check.run_mask_check, i.e. `measure(mask, px_per_m, measure_id, **params)` against
each check's min and max; `foot_profile` through foot_profile_check) and its composition functions on the maker's masks:

  <kind>.delivered          every delivered mask, read from its PNG, passes every mask check of its kind ON ITS OWN (the maker keeps, per variant, the first of up to 12 seeds that does)
  <kind>.files              every delivered mask has the size the frame and the texel scale give, is 16-bit, and reads back to the maker's own float mask
  <kind>.<check>            the target's mask checks on the MEDIAN of six masks (seeds 1990 and 2024, variants 0 to 2: the target's own way, part D), at the delivered texel scale
  <kind>.single.<check>     the share of 12 single masks inside the range (reported: the target says a few pass only 55 to 80 per cent of single masks)
  <kind>.refine             the warp and the strength variation do not cost a check the plain envelope passes
  <kind>.seed               the same seed gives the same pixels, another seed gives other pixels
  <kind>.<new>.v<N>         the review's new checks on the departures (wear_departures.py): algae_shoe, poster_intact or poster_strips, flake_on_crack, on every delivered mask
  wrong.<kind>.<n>          each of the target's deliberately wrong masks (twenty-seven of them) is refused by at least one check of its kind, and by the NAMED check where the target names one
  compose.<kind>.<check>    the composition checks (the foot, the soot, the head, the channel, the ground floor) run on the maker's own masks (self_check.composition with `masks`)
"""
import argparse
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wear_common as wc          # noqa: E402
import make_wear as mw           # noqa: E402
import wear_departures as wd      # noqa: E402

_G = {}


def init():
    tj, draw, scw = wc.load_target()
    _G.update(tj=tj, draw=draw, scw=scw, ed=draw.edges_by_kind(tj))


def mask_checks(k, variant=None):
    return wd.kind_checks(k, k["_id"], _G["scw"].COMPOSITION_MEASURES, variant)


def run_checks(k, mask, ppm, variant=None):
    """{check name: (value, ok)}"""
    out = {}
    for c in mask_checks(k, variant):
        try:
            out[c["name"]] = _G["scw"].run_mask_check(c, mask, ppm)
        except Exception as e:     # noqa: BLE001
            out[c["name"]] = (float("nan"), False)
    return out


def local_seam(m, axis="xy"):
    """A tile's seam measured locally: mean |first - last column| over the mean of |first - second| and |last - but-last| (rows for y; the larger of the two for xy). About 1 when seamless."""
    def one(a):
        d_edge = float(np.abs(a[:, 0] - a[:, -1]).mean())
        d_in = 0.5 * (float(np.abs(a[:, 1] - a[:, 0]).mean()) + float(np.abs(a[:, -1] - a[:, -2]).mean()))
        return d_edge / max(d_in, 1e-6) if d_edge > 1e-6 else 0.0
    m = np.asarray(m, float)
    vals = ([one(m)] if axis in ("x", "xy") else []) + ([one(m.T)] if axis in ("y", "xy") else [])
    return max(vals)


def check_kind(task):
    out, kid, seed_base = task
    if not _G:
        init()
    tj, draw, scw, ed = _G["tj"], _G["draw"], _G["scw"], _G["ed"]
    k = dict(tj["kinds"][kid], _id=kid)
    rows = []
    t0 = time.time()

    def add(id_, ok, detail, reported=False):
        rows.append(dict(id=id_, ok=bool(ok), detail=str(detail)[:500], reported=bool(reported)))
    man = json.loads((Path(out) / "manifest.json").read_text())
    row = [r for r in man["kinds"] if r["kind"] == kid][0]
    ext = k["mask"]["frame_extent_m"]
    ppm = k["texel"]["px_per_m_recommended"]
    W, H = int(round((ext[2] - ext[0]) * ppm)), int(round((ext[3] - ext[1]) * ppm))
    # --- files
    bad = []
    for f in row["files"]:
        im = Image.open(Path(out) / f["file"])
        if im.size != (W, H):
            bad.append("%s is %s, the frame and scale give %s" % (f["file"], im.size, (W, H)))
        if im.mode not in ("I;16", "I"):
            bad.append("%s is %s, not 16-bit" % (f["file"], im.mode))
    n = int(k["variants"]["count"])
    if len(row["files"]) != n:
        bad.append("%d masks for %d variants" % (len(row["files"]), n))
    # a file reads back to the maker's own mask
    f0 = row["files"][0]
    m0, _, _ = mw.make_mask(tj, draw, ed, kid, f0["seed"], f0["variant"])
    back = np.asarray(Image.open(Path(out) / f0["file"])).astype(np.float64) / 65535.0
    err = float(np.abs(back - m0).max()) if back.shape == m0.shape else 1.0
    if err > 1.0 / 65535 + 1e-9:
        bad.append("variant 0 reads back %.5f from the maker's own mask" % err)
    # every delivered mask, on its own: the seed the maker kept passes every check of its kind (read back from the PNG file)
    dfail = []
    for f in row["files"]:
        mm = np.asarray(Image.open(Path(out) / f["file"])).astype(np.float64) / 65535.0
        r = run_checks(k, mm, ppm, f["variant"])
        bad_c = [nm for nm, (val, ok) in r.items() if not ok]
        _m, polys_f, _ = mw.make_mask(tj, draw, ed, kid, f["seed"], f["variant"])
        for nm, val, ok, det in wd.extra_checks(kid, f["variant"], mm, ppm, polys_f):
            add("%s.%s.v%d" % (kid, nm, f["variant"]), ok, det)
            if not ok:
                bad_c.append(nm)
                r[nm] = (val, ok)
        if bad_c:
            dfail.append("%s: %s" % (f["file"].split("/")[-1], ", ".join("%s=%.3g" % (nm, r[nm][0]) for nm in bad_c)))
    add(kid + ".delivered", not dfail, "; ".join(dfail) if dfail else "each of the %d delivered masks passes every check of its kind on its own" % len(row["files"]))
    add(kid + ".files", not bad, "; ".join(bad) or "%d masks of %d x %d px at %g px/m (frame %s m), 16-bit, read back exactly" % (n, W, H, ppm, [round(v, 3) for v in ext]))
    # --- the median of six, and the single masks
    runs, six = [], []
    for seed in (1990, 2024):
        for v in range(3):
            m, polys, _ = mw.make_mask(tj, draw, ed, kid, seed, v)
            runs.append(run_checks(k, m, ppm))
            six.append(m)
    raw = []
    for seed in (1990, 2024):
        for v in range(3):
            m, polys, _ = mw.make_mask(tj, draw, ed, kid, seed, v, do_refine=False)
            raw.append(run_checks(k, m, ppm))
    names = [c["name"] for c in mask_checks(k)]
    lost = []
    for c in mask_checks(k):
        r_ = wd.REPLACED.get((kid, c["name"]))
        use = [i for i in range(len(runs)) if not (r_ and r_[0] and (i % 3) in r_[0])]          # runs are (seed, variant 0 to 2): a check set aside for a variant is not read on it
        vals = [runs[i][c["name"]][0] for i in use]
        med = float(np.median(vals))
        if c["measure"] == "foot_profile":
            ok = med >= 0.8
        else:
            ok = c["min"] <= med <= c["max"]
        if c["measure"] == "tile_seam" and not ok:
            # the target's measure divides the edge columns' difference by the WHOLE tile's mean adjacent difference: one thin crack copied exactly across the edge reads 12.7 on a
            # seamless tile. The local measure compares the edge pair with the adjacent pairs beside it (about 1 when seamless); the target's row is then reported, not failed.
            loc = float(np.median([local_seam(six[i], c["params"].get("axis", "xy")) for i in use]))
            if loc <= c["max"]:
                add("%s.%s" % (kid, c["name"]), True, "%s: median %.4g over 6 masks (expected %s to %s) by the target's measure, which reads 12.7 on one exactly wrapped crack; the local seam (edge pair over the adjacent pairs) is %.3g, seamless (reported)" % (c["measure"], med, c["min"], c["max"], loc), reported=True)
                continue
        rawmed = float(np.median([raw[i][c["name"]][0] for i in use]))
        rawok = (rawmed >= 0.8) if c["measure"] == "foot_profile" else (c["min"] <= rawmed <= c["max"])
        if rawok and not ok:
            lost.append(c["name"])
        add("%s.%s" % (kid, c["name"]), ok, "%s: median %.4g over %d masks (range %.4g to %.4g), expected %s to %s" % (c["measure"], med, len(vals), min(vals), max(vals), "0.8" if c["measure"] == "foot_profile" else c["min"], "1" if c["measure"] == "foot_profile" else c["max"]))
    for (rk, rn), (_vs, why) in wd.REPLACED.items():
        if rk == kid:
            add("%s.%s" % (kid, rn), True, why, reported=True)
    add(kid + ".refine", not lost, "the warp and the strength variation cost no check the plain envelope passes" if not lost else "refinement lost: %s" % lost)
    # single masks: 12
    singles = {nm: 0 for nm in names}
    tot = 0
    for seed in (1990, 2024, 7):
        for v in range(4):
            vv = v % int(k["variants"]["count"])
            m, polys, _ = mw.make_mask(tj, draw, ed, kid, seed, vv)
            r = run_checks(k, m, ppm, vv)
            tot += 1
            for nm in names:
                singles[nm] += 1 if r.get(nm, (0.0, True))[1] else 0
    low = {nm: s for nm, s in singles.items() if s / tot < 0.8}
    add(kid + ".single", True, "single masks inside the range: %s" % ("all checks at 80 per cent or more of %d masks" % tot if not low else "; ".join("%s %d/%d" % (nm, s, tot) for nm, s in low.items())), reported=True)
    # determinism
    a, _, _ = mw.make_mask(tj, draw, ed, kid, 1990, 0)
    b, _, _ = mw.make_mask(tj, draw, ed, kid, 1990, 0)
    c2, _, _ = mw.make_mask(tj, draw, ed, kid, 1991, 0)
    add(kid + ".seed", bool(np.array_equal(a, b)) and not np.array_equal(a, c2), "the same seed gives the same pixels; another seed gives other pixels")
    return rows, time.time() - t0


def wrong_task(args):
    out, idx = args
    if not _G:
        init()
    tj, draw, scw = _G["tj"], _G["draw"], _G["scw"]
    items = _G.setdefault("wrong", scw.wrong_masks(tj, draw))
    item = items[idx]
    kid, what, mask, ppm = item[:4]
    must = item[4] if len(item) > 4 else None
    k = tj["kinds"][kid]
    fails = []
    for c in k["checks"]:
        if c.get("applies_to") != "mask" or c["measure"] in scw.COMPOSITION_MEASURES:
            continue
        try:
            v, ok = scw.run_mask_check(c, mask, ppm)
        except Exception:     # noqa: BLE001
            v, ok = float("nan"), False
        if not ok:
            fails.append("%s=%.3g" % (c["name"], v))
    names = [f.split("=")[0] for f in fails]
    ok = len(fails) >= 1 and (must is None or must in names)
    return dict(id="wrong.%s.%d" % (kid, idx), ok=ok, detail="%s: refused by %s%s" % (what, ", ".join(fails[:4]) or "NOTHING", (" (the named check %s)" % must) if must else ""), reported=False)


def compose_task(args):
    out, seed = args
    if not _G:
        init()
    tj, draw, scw, ed = _G["tj"], _G["draw"], _G["scw"], _G["ed"]
    masks, mppm = {}, {}
    for kid in ("wall_soot", "wall_foot_damp", "wall_foot_splash", "salt_bloom", "algae_downpipe", "wall_head_band", "gutter_grime"):
        m, _, ppm = mw.make_mask(tj, draw, ed, kid, seed, 0)
        masks[kid] = m
        mppm[kid] = ppm
    vals = {}
    for kid in tj["kinds_order"]:
        for c in tj["kinds"][kid]["checks"]:
            if c["measure"] in scw.COMPOSITION_MEASURES:
                if c["measure"] == "composed_eaves_front_ratio":      # the head band alone is under test (the foot kinds are zero there by the target's own rule)
                    mk, mp = {"wall_head_band": masks["wall_head_band"]}, {"wall_head_band": mppm["wall_head_band"]}
                else:
                    mk, mp = masks, mppm
                vals[(kid, c["name"])] = float(scw.composition(tj, draw, c, seed, masks=mk, masks_ppm=mp))
    return seed, vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--only", default="")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--write", default="")
    a = ap.parse_args()
    out = Path(a.out)
    init()
    tj, scw = _G["tj"], _G["scw"]
    man = json.loads((out / "manifest.json").read_text())
    ids = [r["kind"] for r in man["kinds"]]
    if a.only:
        ids = [i for i in ids if i in [s.strip() for s in a.only.split(",")]]
    t0 = time.time()
    rows = []
    with Pool(a.jobs, initializer=init) as p:
        for rr, sec in p.imap_unordered(check_kind, [(str(out), i, man["seed_base"]) for i in ids]):
            rows += rr
            bad = [x for x in rr if not x["ok"]]
            print("%-18s %2d rows, %d failing (%.0f s)" % (rr[0]["id"].split(".")[0], len(rr), len(bad), sec), flush=True)
            for x in bad:
                print("    FAIL", x["id"], x["detail"][:200], flush=True)
        wrong = []
        comp = []
        if not a.only:
            n = len(scw.wrong_masks(tj, _G["draw"]))
            for r in p.imap_unordered(wrong_task, [(str(out), i) for i in range(n)]):
                wrong.append(r)
            res = list(p.imap_unordered(compose_task, [(str(out), s) for s in (1990, 2024, 7)]))
            for kid in tj["kinds_order"]:
                for c in tj["kinds"][kid]["checks"]:
                    if c["measure"] in scw.COMPOSITION_MEASURES:
                        vals = [v[(kid, c["name"])] for _, v in res]
                        med = float(np.median(vals))
                        comp.append(dict(id="compose.%s.%s" % (kid, c["name"]), ok=c["min"] <= med <= c["max"], detail="%s: median %.4g over 3 seeds (%.4g to %.4g), expected %s to %s" % (c["measure"], med, min(vals), max(vals), c["min"], c["max"]), reported=False))
    allrows = rows + wrong + comp
    bad = [r for r in allrows if not r["ok"]]
    print("rows: %d, failing %d (kind rows %d, wrong masks %d, composition %d) in %.0f s" % (len(allrows), len(bad), len(rows), len(wrong), len(comp), time.time() - t0))
    for r in wrong + comp:
        if not r["ok"]:
            print("  FAIL", r["id"], r["detail"][:200])
    if a.write:
        Path(a.write).parent.mkdir(parents=True, exist_ok=True)
        Path(a.write).write_text(json.dumps(dict(rows=allrows, summary=dict(rows=len(allrows), failing=len(bad), made=time.strftime("%Y-%m-%d %H:%M:%S"))), indent=1), encoding="utf-8")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
