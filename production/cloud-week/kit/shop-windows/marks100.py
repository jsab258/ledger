#!/usr/bin/env python3
"""Every placed model's 1k base-colour map at 100 per cent, for the eye (batch B, 14 October 2026; from the ironmonger's close review, fault 3: a tyre pump's roundel and a trowel handle's stamped word
were not painted out because nobody looked at the finished maps region by region).

    python3 marks100.py bananas lemon wall_clock ...      # writes marks_<model>.png (one picture per model, 1024 px per map, the clean base colour)
    python3 marks100.py --regions wall_clock               # the same, cut in 512 px regions (marks_<model>_r<row><col>.png), for a map whose detail is fine

The maps shown are the `_diff_1k_clean.jpg` the glTF points at (the original where there is none). Pictures go to the scratchpad's view folder (LEDGER_SW_VIEW); nothing is a deliverable.
Run with the Python that has Pillow (the bpy one will do). The looking is done by a person or an agent, and written in NOTES.md ("Marks: looked at at 100 per cent, region by region").
"""
import argparse
import os
import sys

from PIL import Image

POLY = os.environ.get("LEDGER_POLY", "/home/user/ledger-scratch/polyhaven")
VIEW = os.environ.get("LEDGER_SW_VIEW", "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/view")


def maps_of(model):
    d = os.path.join(POLY, model, "1k", "textures")
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d)):
        if "_diff_" in f and f.endswith(".jpg") and "_clean" in f:
            out.append(os.path.join(d, f))
    if not out:
        out = [os.path.join(d, f) for f in sorted(os.listdir(d)) if "_diff_" in f and f.endswith(".jpg")]
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("models", nargs="+")
    ap.add_argument("--regions", action="store_true")
    ap.add_argument("--pairs", action="store_true", help="two models' first clean maps side by side in one 2048 x 1024 picture (marks_pair_<n>.png), for a quick look at many models")
    a = ap.parse_args(argv)
    os.makedirs(VIEW, exist_ok=True)
    if a.pairs:
        ims = []
        for m in a.models:
            ms = maps_of(m)
            if ms:
                ims.append((m, Image.open(ms[0]).convert("RGB")))
        for k in range(0, len(ims), 2):
            grp = ims[k:k + 2]
            sheet = Image.new("RGB", (sum(im.width for _, im in grp), max(im.height for _, im in grp)), (255, 0, 255))
            x = 0
            for _, im in grp:
                sheet.paste(im, (x, 0))
                x += im.width
            out = os.path.join(VIEW, "marks_pair_%d.png" % (k // 2))
            sheet.save(out)
            print(out, [m for m, _ in grp])
        return
    for m in a.models:
        ms = maps_of(m)
        if not ms:
            print(m, "no base-colour map found")
            continue
        ims = [Image.open(p).convert("RGB") for p in ms]
        if a.regions:
            for i, im in enumerate(ims):
                for r in range(0, im.height, 512):
                    for c in range(0, im.width, 512):
                        out = os.path.join(VIEW, "marks_%s_%d_r%dc%d.png" % (m, i, r // 512, c // 512))
                        im.crop((c, r, min(c + 512, im.width), min(r + 512, im.height))).save(out)
            print(m, len(ims), "maps in regions")
            continue
        # a model's maps side by side, 1024 px each, at most two to a picture
        for k in range(0, len(ims), 2):
            grp = ims[k:k + 2]
            W = sum(im.width for im in grp)
            H = max(im.height for im in grp)
            sheet = Image.new("RGB", (W, H), (255, 0, 255))
            x = 0
            for im in grp:
                sheet.paste(im, (x, 0))
                x += im.width
            out = os.path.join(VIEW, "marks_%s_%d.png" % (m, k // 2))
            sheet.save(out)
            print(out, [os.path.basename(p) for p in ms[k:k + 2]], [im.size for im in grp])


if __name__ == "__main__":
    main(sys.argv[1:])
