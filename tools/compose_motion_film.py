#!/usr/bin/env python3
"""Put a solved motion's front and side views beside its source clip, frame by frame (n09-8).

    python tools/compose_motion_film.py FILM_DIR

FILM_DIR is tools/blender-live/film_motion_fbx.py's output (source/f-0001.png, front/f-00001.png, side/...).
Writes FILM_DIR/frames/f-00001.jpg ... (source | front | side, 720 high, frame numbers stamped), ready for
tools/film_webp.py FILM_DIR/frames 1 N out.webp --ms 42 (24 frames a second).
"""
import glob
import os
import sys

from PIL import Image, ImageDraw

d = sys.argv[1]
src = sorted(glob.glob(os.path.join(d, "source", "f-*.png")))
front = sorted(glob.glob(os.path.join(d, "front", "f-*.png")))
side = sorted(glob.glob(os.path.join(d, "side", "f-*.png")))
n = min(len(src), len(front), len(side))
os.makedirs(os.path.join(d, "frames"), exist_ok=True)
H = 720
for i in range(n):
    s = Image.open(src[i]).convert("RGB")
    s = s.resize((round(s.width * H / s.height), H), Image.LANCZOS)
    f = Image.open(front[i]).convert("RGB")
    g = Image.open(side[i]).convert("RGB")
    out = Image.new("RGB", (s.width + f.width + g.width, H), (20, 20, 20))
    out.paste(s, (0, 0)); out.paste(f, (s.width, 0)); out.paste(g, (s.width + f.width, 0))
    dr = ImageDraw.Draw(out)
    dr.text((8, 8), "source %d" % (i + 1), fill=(255, 255, 0))
    dr.text((s.width + 8, 8), "solve, front", fill=(255, 255, 0))
    dr.text((s.width + f.width + 8, 8), "solve, side", fill=(255, 255, 0))
    out.save(os.path.join(d, "frames", "f-%05d.jpg" % (i + 1)), quality=88)
print("composed %d frames (source %d, solve %d)" % (n, len(src), len(front)))
