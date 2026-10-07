"""Put a labelled pixel grid over a photograph, so outline points can be read off it.

    python photo_grid.py in.jpg out.png [step_px] [crop x0 y0 x1 y1]

Used to trace a jacket's outline in a period photograph as numbered points in
the photograph's own pixels; the points, not the eye's verdict, are then compared.
"""
import sys

from PIL import Image, ImageDraw


def grid(src, dst, step=50, crop=None, max_side=1400):
    im = Image.open(src).convert("RGB")
    if crop:
        im = im.crop(crop)
    ox, oy = (crop[0], crop[1]) if crop else (0, 0)
    s = min(1.0, max_side / max(im.size))
    im = im.resize((int(im.width * s), int(im.height * s)))
    dr = ImageDraw.Draw(im)
    W, H = im.size
    k = step * s
    i = 0
    while i * k < W:
        x = i * k
        dr.line([(x, 0), (x, H)], fill=(255, 0, 0) if i % 2 == 0 else (255, 160, 0), width=1)
        dr.text((x + 2, 2), str(int(ox + i * step)), fill=(255, 0, 0))
        i += 1
    j = 0
    while j * k < H:
        y = j * k
        dr.line([(0, y), (W, y)], fill=(0, 0, 255) if j % 2 == 0 else (0, 170, 255), width=1)
        dr.text((2, y + 2), str(int(oy + j * step)), fill=(0, 0, 255))
        j += 1
    im.save(dst)
    return dst


if __name__ == "__main__":
    a = sys.argv
    step = int(a[3]) if len(a) > 3 else 50
    crop = tuple(int(v) for v in a[4:8]) if len(a) >= 8 else None
    print(grid(a[1], a[2], step, crop))
