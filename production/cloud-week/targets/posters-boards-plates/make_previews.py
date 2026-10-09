"""Rebuilds the previews of this family (cloud week 42): the one photograph measured (interiors masked), the drawing laid on it, and the layout sheets.

    /home/user/.bpyenv/bin/python make_previews.py [--pano PATH] [--draw DIR]

Needs (outside git): the Poly Haven tonemapped panorama urban_street_01.jpg (CC0, A. Mischok, 18 Aug 2019) and a folder written by
target_drawing.py. Everything is cropped to the OBJECT (a glazed notice case); the glazed windows, which held real posters, are painted flat grey
before the crop is saved, so no word, face or crest is kept. Previews are JPEG, at most 1200 px on the long side, under 300 KB.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SCRATCH = Path("/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/posters")
PANO = SCRATCH / "ph" / "urban_street_01.jpg"
DRAW = SCRATCH / "draw"
if "--pano" in sys.argv:
    PANO = Path(sys.argv[sys.argv.index("--pano") + 1])
if "--draw" in sys.argv:
    DRAW = Path(sys.argv[sys.argv.index("--draw") + 1])
OUT = ROOT / "production" / "previews" / "cloud-week" / "refs" / "posters-boards-plates"
T = json.loads((HERE / "target.json").read_text(encoding="utf-8"))
Image.MAX_IMAGE_PIXELS = None


def render(pano, yaw_deg, pitch_deg, fov_deg, out_w=1200, out_h=900):
    H, W = pano.shape[:2]
    f = (out_w / 2) / np.tan(np.radians(fov_deg) / 2)
    xs = (np.arange(out_w) - out_w / 2 + 0.5) / f
    ys = (np.arange(out_h) - out_h / 2 + 0.5) / f
    X, Y = np.meshgrid(xs, ys)
    d = np.stack([X, Y, np.ones_like(X)], -1)
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    p = np.radians(pitch_deg)
    cp, sp = np.cos(p), np.sin(p)
    wx, wy, wz = d[..., 0], -d[..., 1], d[..., 2]
    wy2 = wy * cp + wz * sp
    wz2 = -wy * sp + wz * cp
    yw = np.radians(yaw_deg)
    cy, sy = np.cos(yw), np.sin(yw)
    lon = np.arctan2(wx * cy + wz2 * sy, -wx * sy + wz2 * cy)
    lat = np.arcsin(np.clip(wy2, -1, 1))
    u = (lon / (2 * np.pi) + 0.5) * W
    v = (0.5 - lat / np.pi) * H
    u0 = np.floor(u).astype(int) % W
    v0 = np.clip(np.floor(v).astype(int), 0, H - 1)
    u1 = (u0 + 1) % W
    v1 = np.clip(v0 + 1, 0, H - 1)
    fu = (u - np.floor(u))[..., None]
    fv = (v - np.floor(v))[..., None]
    img = (pano[v0, u0] * (1 - fu) * (1 - fv) + pano[v0, u1] * fu * (1 - fv) + pano[v1, u0] * (1 - fu) * fv + pano[v1, u1] * fu * fv)
    return Image.fromarray(img.astype(np.uint8))


def save_jpeg(im, path, maxside=1200, limit=300_000):
    im = im.copy()
    im.thumbnail((maxside, maxside))
    q = 88
    while True:
        im.save(path, quality=q, optimize=True)
        if path.stat().st_size < limit or q < 40:
            break
        q -= 6
    return path.stat().st_size


def photo_previews():
    P = T["photo"]["P1"]
    if not PANO.exists():
        print("panorama not found:", PANO, "(skipping the photograph previews)")
        return
    pano = np.asarray(Image.open(PANO)).astype(np.float32)
    view = render(pano, 84.6, 2, 18, 1200, 900)
    cx, cy = P["crop_origin"]
    sc = P["crop_scale"]
    w, h = P["crop_size"]
    crop = view.crop((cx, cy, cx + w, cy + h)).resize((int(w * sc), int(h * sc)), Image.LANCZOS)
    d = ImageDraw.Draw(crop)
    # mask every glazed window (the posters inside are real): flat grey, for the cases in the crop (case 2 fully; case 1 and 3 edges)
    for key in ("c1", "c2", "c3", "c4"):
        x0, y0, x1, y1 = P["px"][key]["window"]
        X0, Y0, X1, Y1 = [(x0 - cx) * sc, (y0 - cy) * sc, (x1 - cx) * sc, (y1 - cy) * sc]
        d.rectangle([X0, Y0, X1, Y1], fill=(176, 176, 176))
    n1 = save_jpeg(crop, OUT / "P1-urban-street-01-notice-case.jpg")
    # the overlay: scale fitted on ONE dimension, the outer height of case 2; the other edges are the test
    r = T["photo"]["ratios"]
    img = crop.copy()
    d = ImageDraw.Draw(img)
    ox0, oy0, ox1, oy1 = P["px"]["c2"]["outer"]
    wx0, wy0, wx1, wy1 = P["px"]["c2"]["window"]
    Y0, Y1 = (oy0 - cy) * sc, (oy1 - cy) * sc
    X0, X1 = (ox0 - cx) * sc, (ox1 - cx) * sc
    H = Y1 - Y0
    pred = [Y0, Y0 + r["top_band_over_h"] * H, Y0 + (r["top_band_over_h"] + r["window_over_h"]) * H, Y1]
    meas = [Y0, (wy0 - cy) * sc, (wy1 - cy) * sc, Y1]
    errs = []
    for yp, ym in zip(pred, meas):
        d.line([(X0 - 30, yp), (X1 + 30, yp)], fill=(255, 40, 40), width=2)
        errs.append(abs(yp - ym) / sc)
    W = X1 - X0
    sb = r["side_bands_sum_over_w"] * W / 2.0
    for xp in (X0, X0 + sb, X1 - sb, X1):
        d.line([(xp, Y0 - 20), (xp, Y1 + 20)], fill=(40, 200, 255), width=1)
    n2 = save_jpeg(img, OUT / "P1-urban-street-01-notice-case-target-on-photo.jpg")
    res = dict(predicted_y_crop_px=[round(v, 1) for v in pred], measured_y_crop_px=[round(v, 1) for v in meas], abs_error_view_px=[round(e, 2) for e in errs], saved=[n1, n2])
    print("photo previews", res)
    return res


def sheet_previews():
    names = [("sheet_bills.png", "L1-quay-street-bills-layout-sheet.jpg"), ("sheet_notices.png", "L2-quay-street-notices-layout-sheet.jpg"),
             ("sheet_cards.png", "L3-quay-street-cards-layout-sheet.jpg"), ("sheet_boards_plates.png", "L4-quay-street-boards-and-plates-layout-sheet.jpg")]
    for src, dst in names:
        p = DRAW / src
        if p.exists():
            print(dst, save_jpeg(Image.open(p).convert("RGB"), OUT / dst))
    a = DRAW / "elevation_SF1.png"
    b = DRAW / "elevation_SF2.png"
    if a.exists() and b.exists():
        ia, ib = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
        ib = ib.resize((ia.size[0], int(ib.size[1] * ia.size[0] / ib.size[0])))
        sheet = Image.new("RGB", (ia.size[0], ia.size[1] + ib.size[1] + 8), (255, 255, 255))
        sheet.paste(ia, (0, 0))
        sheet.paste(ib, (0, ia.size[1] + 8))
        print("L5", save_jpeg(sheet, OUT / "L5-quay-street-gable-and-glass-paste-plan.jpg"))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    photo_previews()
    sheet_previews()
