#!/usr/bin/env python3
"""Writes the reviewers' previews of the photographs this target measured, cropped to the windows, with every mask drawn flat grey.
usage: make_previews.py [--photos DIR] [--out DIR]   (default out: production/previews/cloud-week/refs/house-windows)
Photographs are fetched from Geograph when missing from DIR (the page names the file). Run with /home/user/.bpyenv/bin/python."""
import os
import sys
import argparse

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hw_photos as P
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUTDIR = os.path.join(ROOT, "production", "previews", "cloud-week", "refs", "house-windows")


def preview_name(pid):
    ph = P.PHOTOS[pid]
    yr = ph["taken"].split()[-1]
    what = {"P1": "oblique-sashes-nets", "P2": "painted-frames-nets", "P3": "stone-terrace-nets", "P4": "bw-oblique-nets", "P5": "bw-bays-nets",
            "P6": "replacement-window-bay", "P7": "bw-double-glazing-nets", "P8": "rear-sashes-from-below", "P9": "tall-sashes-oblique",
            "P10": "georgian-6over6-boarded", "P11": "council-casements", "P12": "sashes-olive-white", "P13": "under-10-degrees-slit", "P14": "boarded-houses"}[pid]
    return "%s-%s-%s-%s.jpg" % (pid.lower(), ph["place"], yr, what)


def write(pid, photo_dir, out_dir, max_side=1200, max_bytes=300 * 1024):
    ph = P.PHOTOS[pid]
    src = P.fetch(photo_dir, pid)
    im = Image.open(src).convert("RGB")
    dr = ImageDraw.Draw(im)
    for m in ph["masks"]:
        b = m["box"]
        dr.rectangle([b[0], b[1], b[2] - 1, b[3] - 1], fill=P.GREY)
    c = ph["crop"]
    im = im.crop(c)
    s = ph["scale"]
    w, h = int(im.width * s), int(im.height * s)
    k = min(1.0, float(max_side) / max(w, h))
    im = im.resize((int(w * k), int(h * k)), Image.LANCZOS)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, preview_name(pid))
    for q in (88, 82, 76, 70, 64, 58, 50):
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) <= max_bytes:
            break
    return path, im.size, os.path.getsize(path)


def measured_sheet(photo_dir, out_dir):
    """the 18 measured windows, outline red and pane boxes green, one tile each (nearest-neighbour, so the pixels are the photographs' own)."""
    import hw_measure as M
    tiles = []
    for k, (pid, state, ol, panes, at, note) in M.WINDOWS.items():
        im = Image.open(P.fetch(photo_dir, pid)).convert("RGB")
        pad = 6
        c = im.crop((ol[0] - pad, ol[1] - pad, ol[2] + pad, ol[3] + pad))
        sc = max(1, int(230 / max(c.width, c.height))) if max(c.width, c.height) < 230 else 1
        c = c.resize((c.width * sc, c.height * sc), Image.NEAREST)
        dr = ImageDraw.Draw(c)
        dr.rectangle([pad * sc, pad * sc, (pad + ol[2] - ol[0]) * sc, (pad + ol[3] - ol[1]) * sc], outline=(255, 0, 0))
        for b in panes:
            dr.rectangle([(b[0] - ol[0] + pad) * sc, (b[1] - ol[1] + pad) * sc, (b[2] - ol[0] + pad) * sc, (b[3] - ol[1] + pad) * sc], outline=(0, 255, 0))
        dr.text((2, 2), k, fill=(255, 255, 0))
        tiles.append(c)
    rows = [tiles[i:i + 6] for i in range(0, len(tiles), 6)]
    Wd = max(sum(t.width + 4 for t in r) for r in rows)
    Hh = sum(max(t.height for t in r) + 4 for r in rows)
    sheet = Image.new("RGB", (Wd, Hh), (40, 40, 40))
    y = 0
    for r in rows:
        x = 0
        for t in r:
            sheet.paste(t, (x, y))
            x += t.width + 4
        y += max(t.height for t in r) + 4
    k = min(1.0, 1200.0 / max(sheet.size))
    sheet = sheet.resize((int(sheet.width * k), int(sheet.height * k)), Image.LANCZOS)
    path = os.path.join(out_dir, "measured-windows-sheet.jpg")
    for q in (88, 80, 70, 60):
        sheet.save(path, quality=q, optimize=True)
        if os.path.getsize(path) <= 300 * 1024:
            break
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photos", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), "hw_photos"))
    ap.add_argument("--out", default=OUTDIR)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    ids = [x for x in a.only.split(",") if x] or list(P.PHOTOS)
    for pid in ids:
        path, size, nbytes = write(pid, a.photos, a.out)
        print(pid, os.path.basename(path), size, nbytes)
    if not a.only:
        print("sheet", measured_sheet(a.photos, a.out))
        import json
        import target_drawing as TD
        t = json.load(open(os.path.join(HERE, "target.json")))
        ov = os.path.join(a.out, "p8-oxford-sunningwell-road-rear-1987-target-on-photo.jpg")
        TD.overlay(t, P.fetch(a.photos, "P8"), ov)
        from PIL import Image as _I
        im = _I.open(ov)
        k = min(1.0, 1200.0 / max(im.size))
        if k < 1.0:
            im = im.resize((int(im.width * k), int(im.height * k)), _I.LANCZOS)
        for q in (88, 80, 70, 60):
            im.save(ov, quality=q, optimize=True)
            if os.path.getsize(ov) <= 300 * 1024:
                break
        print("overlay", ov, os.path.getsize(ov))


if __name__ == "__main__":
    main()
