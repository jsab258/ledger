"""Previews of the photograph measured for K2 (S12) and the target laid on it: reduced JPEGs into production/previews/cloud-week/refs/litter-bins/.

    /home/user/.bpyenv/bin/python -I make_previews.py PHOTO_974902.jpg

PHOTO_974902.jpg is the 427 x 640 reduced copy of Geograph 974902 (Jim Champion, 2008-09-21, CC BY-SA 2.0), fetched from the Geograph feed's thumbnail address without its
size suffix. The crop keeps the bin only (the pillar box beside it is cut away) and the council's crest sticker on the bin is painted out; the overlay lays K2's outer
profile on the crop with one dimension fitted (the crown to the base centre = 900 mm), the target's own scale, never the photograph's.
"""
import json
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'previews', 'cloud-week', 'refs', 'litter-bins')
BOX = (40, 235, 250, 575)         # the bin only, in the 427 x 640 photograph's pixels
STICKER = (183, 362, 206, 428)    # the crest sticker, painted out
CROWN_ROW, BASE_ROW, AXIS_X = 257.0, 548.0, 138.0
UP = 3


def main(photo):
    os.makedirs(OUT, exist_ok=True)
    T = json.load(open(os.path.join(HERE, 'target.json')))
    im = Image.open(photo).convert('RGB')
    assert im.size == (427, 640), im.size
    # paint the sticker out with the bin's own grey (the median of a ring of pixels round it)
    x0, y0, x1, y1 = STICKER
    ring = [im.getpixel((x, y)) for x in range(x0 - 6, x0 - 2) for y in range(y0, y1)]
    grey = tuple(sorted(c[i] for c in ring)[len(ring) // 2] for i in range(3))
    ImageDraw.Draw(im).rectangle(STICKER, fill=grey)
    crop = im.crop(BOX).resize(((BOX[2] - BOX[0]) * UP, (BOX[3] - BOX[1]) * UP), Image.LANCZOS)
    p1 = os.path.join(OUT, 'geo974902-southampton-hooded-bin-2008.jpg')
    crop.save(p1, quality=84)
    # the overlay: K2's profile, both sides, at 900 / (BASE_ROW - CROWN_ROW) mm a pixel
    mm_px = T['kinds']['K2']['height'] / (BASE_ROW - CROWN_ROW)
    prof = T['kinds']['K2']['outer_profile_rz']
    ov = crop.copy()
    d = ImageDraw.Draw(ov)
    def px(r, z):
        return ((AXIS_X + r / mm_px - BOX[0]) * UP, (BASE_ROW - z / mm_px - BOX[1]) * UP)
    right = [px(r, z) for r, z in prof]
    left = [px(-r, z) for r, z in prof]
    d.line(right, fill=(0, 255, 255), width=2)
    d.line(left, fill=(0, 255, 255), width=2)
    ap = T['kinds']['K2']['aperture']
    d.line([px(-200, ap['sill_z']), px(200, ap['sill_z'])], fill=(255, 255, 0), width=1)
    d.line([px(-200, ap['top_z']), px(200, ap['top_z'])], fill=(255, 255, 0), width=1)
    p2 = os.path.join(OUT, 'geo974902-southampton-hooded-bin-2008-target-on-photo.jpg')
    ov.save(p2, quality=84)
    for p in (p1, p2):
        print(p, os.path.getsize(p))


if __name__ == '__main__':
    main(sys.argv[1])
