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


if __name__ == "__main__":
    main()
