#!/usr/bin/env python
"""make_paper.py: the paper, cards, plates and boards of Quay Street, by script, from target.json alone (units 4.2, 4.3 and 4.4, cloud week 42).

    /home/user/.bpyenv/bin/python make_paper.py OUTDIR [--only P01,K05,S01n] [--classes wear|A,B,C,D|all] [--seed-base 1] [--jobs 4] [--no-clean]
    python make_paper.py OUTDIR --verify         # rebuild into OUTDIR_verify and compare every SHA-256 of the raw pixels with OUTDIR/manifest.json

Reads  production/cloud-week/targets/posters-boards-plates/target.json (and its reader, self_check.py and glyphlib.py, for the glyph layout and the fonts it names),
       the OFL fonts in production/fonts/ (copied flat into OUTDIR/_fonts: the reader looks fonts up by file name).
Writes into OUTDIR (never into git):
       <ID>/<ID>_<class>_basecolour.png   sRGB 8-bit, RGBA where the item has an outline (a star, a hole, tears, loss, a sleeve's clear band), else RGB; row 0 the TOP, column 0 the
                                          viewer's LEFT, ONE PIXEL SCALE per item (items[].px_per_mm); square-on: no skew, no rotation
       <ID>/<ID>_<class>_height.png       16-bit grey, 32768 = the face; units per mm in the manifest (25600, or 8192 on the plates with 3 mm of relief)
       <ID>/<ID>_<class>_orm.png          linear 8-bit: R 255 (no occlusion drawn), G roughness, B metal
       <ID>/<ID>.glyphs.json              the glyph manifest the reader needs (one entry per character of every block, the registration offset and the hand jitter included)
       _check/<ID>_A_clean.png            the class-A render before wear (what ITEM.clean reads); a diagnostic, not for the game
       manifest.json                      every file, its size in pixels and millimetres, the item's words, fonts, inks, stock, process, class, seed, wear and SHA-256 of the pixels
Classes: `wear` (default) makes the classes the target lists in items[].wear.classes; `all` makes A to D.
Deterministic: every random draw comes from a numpy Generator seeded from (seed base, item, what it is for); the same seed gives the same pixels.
"""
import argparse
import hashlib
import json
import os
import platform
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import paper_common as pc          # noqa: E402

SCHEMA = "ledger.cloud-week-42.paper-manifest/1"
_G = {}
EXTRA_SEEDS = {"K03a": 2, "K03b": 2}      # the OPEN / CLOSED sign hangs on eight doors: three seeds of its scratches and grime (the review of 12 October)


def init(out):
    sc, gl = pc.load_reader(out)
    _G["sc"], _G["gl"] = sc, gl
    _G["P"] = pc.Palette(sc.T)
    import paper_ink, paper_render      # noqa: E402,F401
    _G["pi"], _G["pr"] = paper_ink, paper_render


def pix_hash(arr):
    a = np.ascontiguousarray(arr)
    return hashlib.sha256(str(a.shape).encode() + str(a.dtype).encode() + a.tobytes()).hexdigest()


def file_hash(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save_png(arr, path, mode=None):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr, mode=mode).save(path, format="PNG", compress_level=6)


def classes_for(item, spec):
    if spec == "wear":
        return list(item["wear"].get("classes") or ["B"])
    if spec == "all":
        return list(pc.CLASSES)
    return [c for c in spec.split(",") if c in pc.CLASSES]


def build_item(task):
    """One item: lay it out, render its classes, write its files. Returns the manifest row."""
    out, iid, spec, seed_base, write_clean = task
    if not _G:
        init(out)
    sc, gl, P, pi, pr = _G["sc"], _G["gl"], _G["P"], _G["pi"], _G["pr"]
    it = sc.ITEMS[iid]
    t0 = time.time()
    geo = pi.build(sc, gl, P, it, seed_base)
    classes = classes_for(it, spec)
    row = dict(item=iid, title=it["title"], kind=it["kind"], format_mm=[it["format"]["w_mm"], it["format"]["h_mm"]], px_per_mm=it["px_per_mm"], size_px=[geo.shape[1], geo.shape[0]],
               stock=it["stock"], process=it["process"], wear_table=it["wear"].get("table"), held=bool(it.get("held")), seed=seed_base,
               registration_offset_mm=list(geo.second_off), art_slots=[a["id"] for a in geo.art], classes={})
    man = dict(item=iid, px_per_mm=it["px_per_mm"], size_px=[geo.shape[1], geo.shape[0]], blocks={bid: [dict(g) for g in gs] for bid, gs in geo.man.items()})
    gpath = Path(out) / iid / (iid + ".glyphs.json")
    gpath.parent.mkdir(parents=True, exist_ok=True)
    gpath.write_text(json.dumps(man), encoding="utf-8")
    row["glyphs_json"] = dict(file="%s/%s.glyphs.json" % (iid, iid), sha256=file_hash(gpath))
    row["words"] = {b["id"]: b["text"] for b in it["blocks"] if not b.get("ghost")}
    row["fonts"] = sorted({b["font"] for b in it["blocks"] if not b.get("ghost")})
    row["inks"] = sorted({b["ink"] for b in it["blocks"] if not b.get("ghost")})
    if write_clean:
        r = pr.render(P, geo, "A", seed_base, wear=False)
        rgb, a = pr.to_rgba8(r)
        save_png(np.dstack([rgb, a]), Path(out) / "_check" / (iid + "_A_clean.png"), "RGBA")
        row["clean_png"] = dict(file="_check/%s_A_clean.png" % iid, sha256_pixels=pix_hash(np.dstack([rgb, a])))
    for cls in classes:
        extra = []
        for v in range(1 + EXTRA_SEEDS.get(iid, 0)):
            r = pr.render(P, geo, cls, seed_base + 7919 * v, wear=True)
            rgb, a = pr.to_rgba8(r)
            has_alpha = bool((a < 255).any())
            base = np.dstack([rgb, a]) if has_alpha else rgb
            h16 = pr.height16(r)
            orm = pr.orm8(r)
            f0 = "%s/%s_%s%s" % (iid, iid, cls, "" if v == 0 else "-s%d" % (v + 1))
            save_png(base, Path(out) / (f0 + "_basecolour.png"), "RGBA" if has_alpha else "RGB")
            save_png(h16, Path(out) / (f0 + "_height.png"))
            save_png(orm, Path(out) / (f0 + "_orm.png"), "RGB")
            entry = dict(
                basecolour=dict(file=f0 + "_basecolour.png", mode="RGBA" if has_alpha else "RGB", sha256_pixels=pix_hash(base)),
                height=dict(file=f0 + "_height.png", units_per_mm=r["units"], zero=32768, sha256_pixels=pix_hash(h16)),
                orm=dict(file=f0 + "_orm.png", sha256_pixels=pix_hash(orm)),
                wear=r["log"], paper_lost_share=float(1 - r["alpha"].mean()))
            if v == 0:
                row["classes"][cls] = entry
            else:
                extra.append(entry)
        if extra:
            row["classes"][cls]["seed_variants"] = extra
    row["seconds"] = round(time.time() - t0, 1)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--only", default="")
    ap.add_argument("--classes", default="wear")
    ap.add_argument("--seed-base", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--no-clean", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    out = Path(a.out)
    if a.verify:
        out2 = Path(str(out) + "_verify")
        ref = json.loads((out / "manifest.json").read_text())
        only = ",".join(r["item"] for r in ref["items"])
        main_args = [sys.argv[0], str(out2), "--only", only, "--classes", ref["classes_arg"], "--seed-base", str(ref["seed_base"]), "--jobs", str(a.jobs)]
        sys.argv = main_args
        main()
        new = json.loads((out2 / "manifest.json").read_text())
        bad = 0
        for r0, r1 in zip(ref["items"], new["items"]):
            for c in r0["classes"]:
                for k in ("basecolour", "height", "orm"):
                    if r0["classes"][c][k]["sha256_pixels"] != r1["classes"][c][k]["sha256_pixels"]:
                        bad += 1
                        print("DIFFERS", r0["item"], c, k)
        print("verify: %d differing maps" % bad)
        return 0 if not bad else 1
    out.mkdir(parents=True, exist_ok=True)
    init(out)
    sc = _G["sc"]
    ids = [i["id"] for i in sc.T["items"]]
    if a.only:
        want = [s.strip() for s in a.only.split(",") if s.strip()]
        missing = [w for w in want if w not in ids]
        if missing:
            print("unknown items:", missing)
            return 2
        ids = [i for i in ids if i in want]
    # the biggest first, so that the long ones start early
    ids.sort(key=lambda i: -sc.ITEMS[i]["megapixels"] if "megapixels" in sc.ITEMS[i] else 0)
    tasks = [(str(out), i, a.classes, a.seed_base, not a.no_clean) for i in ids]
    t0 = time.time()
    rows = []
    if a.jobs > 1:
        with Pool(a.jobs, initializer=init, initargs=(str(out),)) as p:
            for r in p.imap_unordered(build_item, tasks):
                rows.append(r)
                print("%-10s %6.1f s  %s" % (r["item"], r["seconds"], " ".join(r["classes"])), flush=True)
    else:
        for t in tasks:
            r = build_item(t)
            rows.append(r)
            print("%-10s %6.1f s  %s" % (r["item"], r["seconds"], " ".join(r["classes"])), flush=True)
    rows.sort(key=lambda r: ids.index(r["item"]))
    import PIL
    man = dict(schema=SCHEMA, made=time.strftime("%Y-%m-%d %H:%M:%S"), seconds=round(time.time() - t0, 1), seed_base=a.seed_base, classes_arg=a.classes,
               versions=dict(python=platform.python_version(), numpy=np.__version__, pillow=PIL.__version__), target=str(pc.TARGET_DIR / "target.json"),
               items=rows, note="pixels are hashed raw (sha256_pixels); a PNG file's own hash differs between library versions")
    (out / "manifest.json").write_text(json.dumps(man, indent=1), encoding="utf-8")
    print("wrote %d items in %.0f s" % (len(rows), time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
