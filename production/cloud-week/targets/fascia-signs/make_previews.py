"""Rebuilds the reference previews of the photographs measured for this target (cloud week 42).

    /home/user/.bpyenv/bin/python make_previews.py [--cache DIR]

Downloads (Poly Haven, CC0; the only photograph source the cloud network reached) the tone-mapped
Leadenhall Market panorama and two painted-plank textures into DIR (default: the scratch folder it was
written in), renders the level square-on elevation of the panorama (yaw 90, pitch 0, 110 degrees wide,
3600 x 2400), and writes reduced JPEGs (at most 1200 px on the long side, under 300 KB) into
production/previews/cloud-week/refs/fascia-signs/. The photographs are for measuring only: never placed in
the game, never traced into a texture, never fed to an image model.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.ndimage import map_coordinates

Image.MAX_IMAGE_PIXELS = None
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT / "production" / "previews" / "cloud-week" / "refs" / "fascia-signs"
CACHE = Path(sys.argv[sys.argv.index("--cache") + 1]) if "--cache" in sys.argv else Path("/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/fascia/dl")
URLS = {
    "leadenhall_market_tm.jpg": "https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/leadenhall_market.jpg",
    "blue_painted_planks_diff_2k.jpg": "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/blue_painted_planks/blue_painted_planks_diff_2k.jpg",
    "black_painted_planks_diff_2k.jpg": "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/black_painted_planks/black_painted_planks_diff_2k.jpg",
}
# the crop of the 3600 x 2400 elevation that is the board preview, and its reduction
P1_CROP = (1150, 120, 2450, 400)
P1_SCALE = 1200.0 / 1300.0


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    for f, u in URLS.items():
        p = CACHE / f
        if not p.exists():
            urllib.request.urlretrieve(u, p)


def render(src, yaw, pitch, fov, w, h):
    im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    H, W, _ = im.shape
    f = (w / 2) / np.tan(np.radians(fov) / 2)
    xs = np.arange(w) - w / 2 + 0.5
    ys = np.arange(h) - h / 2 + 0.5
    X, Y = np.meshgrid(xs, -ys)
    d = np.stack([X, Y, np.full_like(X, f)], -1)
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    p = -np.radians(pitch)
    yw = np.radians(yaw)
    Rx = np.array([[1, 0, 0], [0, np.cos(p), -np.sin(p)], [0, np.sin(p), np.cos(p)]])
    Ry = np.array([[np.cos(yw), 0, np.sin(yw)], [0, 1, 0], [-np.sin(yw), 0, np.cos(yw)]])
    d = d @ Rx.T @ Ry.T
    lon = np.arctan2(d[..., 0], d[..., 2])
    lat = np.arcsin(np.clip(d[..., 1], -1, 1))
    u = (lon / (2 * np.pi) + 0.5) * W - 0.5
    v = (0.5 - lat / np.pi) * H - 0.5
    ch = [map_coordinates(im[..., c], [v, u], order=1, mode="wrap") for c in range(3)]
    return Image.fromarray(np.stack(ch, -1).clip(0, 255).astype(np.uint8))


def save(im, name, q=88, limit=300_000):
    p = OUT / name
    for qq in (q, 84, 80, 74, 68):
        im.save(p, quality=qq, optimize=True)
        if p.stat().st_size < limit:
            break
    print(name, im.size, p.stat().st_size, "bytes")


def main():
    fetch()
    OUT.mkdir(parents=True, exist_ok=True)
    e90 = render(CACHE / "leadenhall_market_tm.jpg", 90, 0, 110, 3600, 2400)
    # P1 board
    c = e90.crop(P1_CROP)
    save(c.resize((1200, int(round(c.size[1] * P1_SCALE))), Image.LANCZOS), "P1-leadenhall-chamberlain-board-elevation.jpg")
    # P1 front with the door leaf for scale (annotated)
    fr = e90.crop((1150, 100, 2450, 1560))
    k = 1200.0 / fr.size[1]
    fr = fr.resize((int(fr.size[0] * k), 1200), Image.LANCZOS)
    dr = ImageDraw.Draw(fr)
    def Y(y):
        return (y - 100) * k
    for y, lab, colr in ((1200, "horizon (image centre row 1200)", (0, 255, 255)), (790, "door leaf top 790", (255, 255, 0)), (1482, "door leaf bottom 1482", (255, 255, 0)),
                         (179, "field top 179", (255, 0, 255)), (326, "field bottom 326", (255, 0, 255)), (1505, "footway at the front 1505", (0, 255, 0))):
        dr.line([(0, Y(y)), (fr.size[0], Y(y))], fill=colr, width=1)
        dr.text((6, Y(y) - 11), lab, fill=colr)
    save(fr, "P1-leadenhall-chamberlain-front-scale.jpg")
    # P2 / P3
    b = Image.open(CACHE / "blue_painted_planks_diff_2k.jpg").convert("RGB")
    a = np.asarray(b).astype(float)
    r, g, bl = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * bl
    exposed = (g >= bl - 4) & (lum < 95)
    rowl = lum.mean(axis=1)
    gap = ndi.binary_dilation(rowl < np.percentile(rowl, 50) * 0.6, iterations=4)
    exposed &= ~gap[:, None]
    mask = Image.fromarray((exposed * 255).astype(np.uint8)).convert("RGB")
    s = Image.new("RGB", (1200, 600))
    s.paste(b.resize((600, 600), Image.LANCZOS), (0, 0))
    s.paste(mask.resize((600, 600), Image.NEAREST), (600, 0))
    ImageDraw.Draw(s).text((8, 8), "P2 blue painted planks, 1.0 m square: photograph | paint loss (white) 28.6 per cent, patches median 8.9 mm, aspect 3.6", fill=(255, 255, 0))
    save(s, "P2-bluepaintedplanks-weathering-measure.jpg")
    k3 = Image.open(CACHE / "black_painted_planks_diff_2k.jpg").convert("RGB")
    a3 = np.asarray(k3).astype(float)
    L3 = 0.2126 * a3[..., 0] + 0.7152 * a3[..., 1] + 0.0722 * a3[..., 2]
    sc = (L3 > np.percentile(L3, 50) + 14)
    s = Image.new("RGB", (1200, 600))
    s.paste(k3.resize((600, 600), Image.LANCZOS), (0, 0))
    s.paste(Image.fromarray((sc * 255).astype(np.uint8)).convert("RGB").resize((600, 600), Image.NEAREST), (600, 0))
    ImageDraw.Draw(s).text((8, 8), "P3 black painted planks, 1.6 m square: photograph | scuffs and abrasion (white = 14 levels brighter than the median luminance)", fill=(255, 255, 0))
    save(s, "P3-blackpaintedplanks-scuff-measure.jpg")
    # H1 sheet
    hs = Image.open(ROOT / "production" / "reference" / "hook-sheet.png").convert("RGB")
    c = hs.crop((290, 480, 840, 575))
    c = c.resize((1100, 190), Image.LANCZOS)
    d = ImageDraw.Draw(c)
    def HX(x):
        return (x - 290) * 2
    def HY(y):
        return (y - 480) * 2
    for y, lab in ((500, "board top 500"), (548, "board bottom 548"), (513, "cap top 513"), (546, "baseline 546")):
        d.line([(0, HY(y)), (1100, HY(y))], fill=(0, 255, 255), width=1)
        d.text((4, HY(y) - 11), lab, fill=(0, 255, 255))
    for x, lab in ((630, "x 630"), (746, "x 746")):
        d.line([(HX(x), 0), (HX(x), 190)], fill=(255, 255, 0), width=1)
    save(c, "H1-hook-sheet-mickeys-board-measure.jpg")


if __name__ == "__main__":
    main()
