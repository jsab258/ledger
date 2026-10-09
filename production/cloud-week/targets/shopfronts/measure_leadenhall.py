#!/usr/bin/env python
"""Measure the Leadenhall Market photograph (P1) for the shopfront target, and write the previews.

P1 is Poly Haven's "Leadenhall Market" 360 degree HDRI (Andreas Mischok, CC0, taken 19 May 2019;
https://polyhaven.com/a/leadenhall_market, files by https://api.polyhaven.com/files/leadenhall_market).
It is re-projected here to a rectilinear, level view of the arcade's right-hand wall (yaw 90 degrees
from the panorama's centre, pitch 0, focal length 2400 px), so that every plane parallel to that
wall is drawn at one scale (a true elevation). Coordinates below are pixels of that virtual image,
x to the right and y DOWN from its principal point, which is the camera's eye level.

What this writes (all next to this file, or in the previews folder):
  photo_measurements.json   every measured number, its crop, method and snapped strength
  previews: crops of the JOINERY ONLY (lettering masked), JPEG, at most 1200 px, under 300 KB.

Nothing from the photograph is placed in the game, traced into a texture or fed to an image model:
the measurements are numbers, and the previews are for reviewers. The unmasked views carry real
businesses' names and trade notices; they live only in the scratch folder and are never saved
into the repository.

Run:  /home/user/.bpyenv/bin/python measure_leadenhall.py --work SCRATCH_DIR [--previews DIR]
The work folder holds (or receives) the 16k HDR, converted once to a tone-mapped 8-bit array.
"""
import argparse
import json
import os
import sys
import time
import urllib.request

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
HDR_URL = "https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/16k%2B/leadenhall_market_16k.hdr"
F = 2400.0           # focal length of the virtual view, pixels
YAW = 90.0
EYE_UNKNOWN = True

# ---- the crops (virtual-image coordinates: x0, y0, width, height) --------------------------
CROPS = {
    "plinth":   (-1360, -80, 350, 700),
    "capital":  (-1360, -1760, 350, 340),
    "fascia":   (-1400, -2340, 520, 660),
    "sill":     (-1100, 90, 850, 530),
    "transom":  (-1100, -700, 850, 180),
    "cornice":  (-1030, -2340, 200, 380),
}
# lettering to mask in the previews (virtual-image boxes: x0, y0, x1, y1): the house numerals and a logo fragment
MASKS = {"fascia": [(-1395, -1865, -1300, -1755), (-1012, -1865, -866, -1750)],
         "plinth": [(-1360, -80, -1316, 95)]}   # the numerals; a fragment of a shop-window logo behind the plinth


def ensure_pano(work):
    npy = os.path.join(work, "pano16k_u8.npy")
    if os.path.exists(npy):
        return np.load(npy, mmap_mode="r")
    os.makedirs(work, exist_ok=True)
    hdr = os.path.join(work, "leadenhall_16k.hdr")
    if not os.path.exists(hdr):
        print("downloading", HDR_URL)
        urllib.request.urlretrieve(HDR_URL, hdr)
    import bpy  # Blender's python module reads Radiance HDR quickly
    img = bpy.data.images.load(hdr)
    w, h = img.size
    a = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(a)
    a = a.reshape(h, w, 4)[::-1, :, :3]
    ex = 0.20 / np.percentile(a.mean(axis=2)[::8, ::8], 50)
    out = np.lib.format.open_memmap(npy, mode="w+", dtype=np.uint8, shape=(h, w, 3))
    for y0 in range(0, h, 512):
        c = a[y0:y0 + 512] * ex
        c = c / (1 + c * 0.25) * 1.25
        c = np.clip(c, 0, 1)
        c = np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)
        out[y0:y0 + 512] = (c * 255 + 0.5).astype(np.uint8)
    out.flush()
    return np.load(npy, mmap_mode="r")


def crop(P, x0, y0, w, h, yaw=YAW, f=F):
    """Rectilinear crop [x0, x0+w) x [y0, y0+h) of the virtual image (principal point (0, 0))."""
    H, W, _ = P.shape
    X, Y = np.meshgrid(np.arange(x0, x0 + w) + 0.5, np.arange(y0, y0 + h) + 0.5)
    d = np.stack([X, Y, np.full_like(X, f)], -1)
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    cy, sy = np.cos(np.radians(yaw)), np.sin(np.radians(yaw))
    xw = d[..., 0] * cy + d[..., 2] * sy
    zw = -d[..., 0] * sy + d[..., 2] * cy
    lon = np.arctan2(xw, zw)
    lat = np.arctan2(-d[..., 1], np.hypot(xw, zw))
    u = (lon / (2 * np.pi) + 0.5) * W - 0.5
    v = (0.5 - lat / np.pi) * H - 0.5
    u0 = np.floor(u).astype(np.int64)
    v0 = np.floor(v).astype(np.int64)
    fu = (u - u0)[..., None]
    fv = (v - v0)[..., None]
    u0m, u1m = u0 % W, (u0 + 1) % W
    v0c, v1c = np.clip(v0, 0, H - 1), np.clip(v0 + 1, 0, H - 1)
    out = np.empty((h, w, 3), np.float32)
    for r0 in range(0, h, 128):
        s = slice(r0, min(h, r0 + 128))
        a = P[v0c[s], u0m[s]].astype(np.float32)
        b = P[v0c[s], u1m[s]].astype(np.float32)
        c = P[v1c[s], u0m[s]].astype(np.float32)
        e = P[v1c[s], u1m[s]].astype(np.float32)
        out[s] = (a * (1 - fu[s]) + b * fu[s]) * (1 - fv[s]) + (c * (1 - fu[s]) + e * fu[s]) * fv[s]
    return np.clip(out + 0.5, 0, 255).astype(np.uint8)


def lum(a):
    a = a.astype(np.float32)
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def snap(img, kind, expect, pa, pb, win, sig=1.2, sign=0):
    """Strongest luminance gradient near `expect` (crop pixels), averaged over pa..pb on the other
    axis. kind 'R' finds a row, 'C' a column. sign +1 takes only edges that get brighter going down or
    right, -1 only darker, 0 either. Returns (position, strength) with a parabola fit."""
    L = lum(img)
    v = L[:, pa:pb].mean(axis=1) if kind == "R" else L[pa:pb, :].mean(axis=0)
    g = np.gradient(gaussian_filter1d(v, sig))
    lo, hi = max(1, int(round(expect - win))), min(len(g) - 2, int(round(expect + win)))
    seg = np.abs(g[lo:hi + 1]) if sign == 0 else np.maximum(0.0, sign * g[lo:hi + 1])
    k = int(np.argmax(seg))
    i = lo + k
    a, b, c = abs(g[i - 1]), abs(g[i]), abs(g[i + 1])
    den = a - 2 * b + c
    d = 0.5 * (a - c) / den if abs(den) > 1e-9 else 0.0
    return float(i + max(-1.0, min(1.0, d))), float(seg[k])


# features: (id, crop, kind, expected virtual coordinate, span lo, span hi (virtual), window, what)
FEATURES = [
    # the pilaster (P-a), from the foot up
    ("pil_foot", "plinth", "R", 604, -1290, -1150, 14, "foot of the plinth, on the footway"),
    ("plinth_block1_top", "plinth", "R", 195, -1290, -1150, 10, "top of the plinth's lowest block"),
    ("plinth_block2_top", "plinth", "R", 91, -1290, -1150, 10, "top of its second block"),
    ("plinth_block3_top", "plinth", "R", 53, -1290, -1150, 8, "top of its third block"),
    ("plinth_cap_top", "plinth", "R", -46, -1290, -1150, 12, "top of the weathered cap slab, where the shaft starts"),
    ("plinth_block1_left", "plinth", "C", -1330, 300, 560, 12, "left edge of the lowest block"),
    ("plinth_block2_left", "plinth", "C", -1320, 110, 180, 10, "left edge of the second block"),
    ("plinth_block3_left", "plinth", "C", -1311, 56, 84, 10, "left edge of the third block"),
    ("plinth_cap_left", "plinth", "C", -1305, -30, 40, 10, "left edge of the weathered cap slab"),
    ("neck_ledge_left", "capital", "C", -1285, -1556, -1553, 6, "left end of the necking's ledge"),
    ("shaft_top", "capital", "R", -1529, -1215, -1200, 8, "top of the shaft (cream) under the necking"),
    ("neck_ledge", "capital", "R", -1552, -1215, -1200, 6, "the necking's ledge"),
    ("abacus_bottom", "capital", "R", -1675, -1215, -1200, 6, "underside of the capital's top band"),
    ("abacus_top", "capital", "R", -1704, -1215, -1200, 8, "top of the capital's top band (the fascia field's foot)"),
    ("shaft_left", "capital", "C", -1270, -1500, -1440, 8, "shaft, left edge"),
    ("shaft_right", "capital", "C", -1102, -1500, -1440, 8, "shaft, right edge of the front face"),
    ("shaft_return_outer", "capital", "C", -1072, -1500, -1440, 8, "the shaft's right return, outer edge (where it meets the wall)"),
    # the fascia end (the cornice's lowest and highest edges)
    ("fascia_field_top", "fascia", "R", -1989, -960, -940, 10, "gilt line at the field's top"),
    ("fascia_field_bottom", "fascia", "R", -1705, -960, -940, 8, "gilt line at the field's foot (or the board's foot)"),
    ("crown_top", "fascia", "R", -2298, -1250, -1150, 10, "top edge of the upper pier cap / crown"),
    # the continuous crown (cornice and frieze) running off to the right of the pier
    ("cornice_base", "cornice", "R", -1990, -1000, -950, 8, "the field's top: the crown's lowest fillet"),
    ("cornice_cove_top", "cornice", "R", -2020, -1000, -950, 8, "top of the first cove"),
    ("cornice_soffit_top", "cornice", "R", -2047, -1000, -950, 8, "top of the dark soffit band"),
    ("cornice_lit_top", "cornice", "R", -2110, -1000, -950, 8, "top of the broad lit member"),
    ("cornice_frieze_foot", "cornice", "R", -2143, -1000, -950, 8, "foot of the tall plain face"),
    ("cornice_top", "cornice", "R", -2240, -1000, -950, 12, "top of the crown (under the cap quirk), the first-floor wall above"),
    # the window frame, sill and stallriser
    ("stile_left", "sill", "C", -1034, 300, 500, 10, "left stile, left edge (frame beside the pilaster)"),
    ("stile_right", "sill", "C", -953, 300, 500, 10, "left stile, right edge"),
    ("sill_top", "sill", "R", 107, -900, -700, 12, "top of the sill group (the glazing rebate's foot)"),
    ("sill_r2", "sill", "R", 127, -900, -700, 10, "sill: lower edge of the bead"),
    ("sill_nose", "sill", "R", 145, -900, -700, 10, "sill: the nose / weathering's lower edge"),
    ("grille_top", "sill", "R", 200, -900, -700, 12, "top of the stallriser's panel (the cast grille in its frame)"),
    ("grille_bottom", "sill", "R", 527, -900, -700, 12, "bottom of the stallriser's panel"),
    ("bottom_rail_foot", "sill", "R", 559, -900, -700, 12, "foot of the stallriser's frame"),
    ("transom_top", "transom", "R", -619, -800, -600, 10, "transom bar, top (the mid-height bar of the window)"),
    ("transom_bottom", "transom", "R", -596, -800, -600, 10, "transom bar, bottom"),
    ("mullion_left", "transom", "C", -380, -700, -540, 12, "central mullion, left edge"),
    ("mullion_right", "transom", "C", -285, -700, -540, 12, "central mullion, right edge"),
]


SIGN = {"fascia_field_top": 1, "fascia_field_bottom": 1}   # the gilt line is 8 px thick: take its rising edge only


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--previews", default=os.path.join(HERE, "..", "..", "..", "previews", "cloud-week", "refs", "shopfronts"))
    ap.add_argument("--out", default=os.path.join(HERE, "photo_measurements.json"))
    a = ap.parse_args()
    t0 = time.time()
    P = ensure_pano(a.work)
    arr = {k: crop(P, *v) for k, v in CROPS.items()}
    meas = {}
    for fid, cname, kind, exp, pa, pb, win, what in FEATURES:
        x0, y0, w, h = CROPS[cname]
        im = arr[cname]
        if kind == "R":
            pos, st = snap(im, "R", exp - y0, pa - x0, pb - x0, win, sign=SIGN.get(fid, 0))
            meas[fid] = {"crop": cname, "kind": "row", "y": round(pos + y0, 2), "strength": round(st, 1),
                         "expected": exp, "span_x": [pa, pb], "what": what, "sign": SIGN.get(fid, 0)}
        else:
            pos, st = snap(im, "C", exp - x0, pa - y0, pb - y0, win)
            meas[fid] = {"crop": cname, "kind": "col", "x": round(pos + x0, 2), "strength": round(st, 1),
                         "expected": exp, "span_y": [pa, pb], "what": what}
    # the shop door (the unmasked view; the glass carries lettering, so these are NOT re-measurable on a preview)
    dc = crop(P, 380, -900, 200, 1520)
    for fid, kind, exp, pa, pb, win, what in [
            ("door_foot", "R", 551, 440, 540, 6, "foot of the door's brass strip (the leaf's bottom)"),
            ("door_foot_strip_top", "R", 532, 440, 540, 10, "top of the brass foot strip"),
            ("door_glass_bottom", "R", 96, 430, 540, 15, "bottom edge of the glazing (the lock rail's top)"),
            ("door_glass_top", "R", -761, 430, 540, 20, "top edge of the glazing"),
            ("door_leaf_top", "R", -828, 430, 540, 25, "top of the leaf under the head")]:
        pos, st = snap(dc, "R", exp + 900, pa - 380, pb - 380, win)
        meas[fid] = {"crop": "door (unmasked, not saved)", "kind": "row", "y": round(float(pos) - 900, 2), "strength": round(st, 1),
                     "expected": exp, "span_x": [pa, pb], "what": what, "remeasurable": False}
    # the scale object: an A5 notice 148 x 210 mm on the door glass (unmasked view; not re-measurable
    # on a saved preview), and the door's foot and glass line, read on the unmasked view
    sc = crop(P, 860, 0, 140, 160)
    sl, _ = snap(sc, "C", 891 - 860, 40, 100, 8)
    sr, _ = snap(sc, "C", 970 - 860, 40, 100, 8)
    st_, _ = snap(sc, "R", 21, 900 - 860, 950 - 860, 8)
    sb, _ = snap(sc, "R", 131, 900 - 860, 950 - 860, 8)
    meas["_sign"] = {"x0": round(float(sl) + 860, 2), "x1": round(float(sr) + 860, 2), "y0": round(float(st_), 2), "y1": round(float(sb), 2),
                     "note": "an A5 notice (148 x 210 mm) taped to the shop door's glass; read on the unmasked view"}
    out = {"photo": "P1 Leadenhall Market, Andreas Mischok, CC0, taken 2019-05-19",
           "view": {"yaw_deg": YAW, "pitch_deg": 0, "focal_px": F, "origin": "principal point = eye level; y down"},
           "crops": {k: list(v) for k, v in CROPS.items()}, "masks": MASKS, "features": meas,
           "seconds": round(time.time() - t0, 1)}
    json.dump(out, open(a.out, "w"), indent=1)
    # previews: joinery only, lettering masked, JPEG, <= 1200 px, < 300 KB
    os.makedirs(a.previews, exist_ok=True)
    names = {"plinth": "P1-leadenhall-pilaster-plinth", "capital": "P1-leadenhall-pilaster-capital",
             "fascia": "P1-leadenhall-pier-fascia-cornice", "sill": "P1-leadenhall-sill-stallriser-stile",
             "transom": "P1-leadenhall-transom-mullion", "cornice": "P1-leadenhall-cornice-run"}
    for k, im in arr.items():
        x0, y0, w, h = CROPS[k]
        img = Image.fromarray(im.copy())
        for (bx0, by0, bx1, by1) in MASKS.get(k, []):
            box = (max(0, bx0 - x0), max(0, by0 - y0), min(w, bx1 - x0), min(h, by1 - y0))
            if box[2] <= box[0] or box[3] <= box[1]:
                continue
            ring = np.asarray(img.crop((max(0, box[0] - 12), max(0, box[1] - 12), min(w, box[2] + 12), min(h, box[3] + 12))))
            col = tuple(int(v) for v in np.median(ring.reshape(-1, 3), axis=0))
            patch = Image.new("RGB", (box[2] - box[0], box[3] - box[1]), col)
            img.paste(patch, box[:2])
        path = os.path.join(a.previews, names[k] + ".jpg")
        for q in (88, 84, 80, 74, 68):
            img.save(path, quality=q, optimize=True)
            if os.path.getsize(path) < 295_000:
                break
        print(path, img.size, os.path.getsize(path))
    print("measured", len(meas), "features in", out["seconds"], "s ->", a.out)


if __name__ == "__main__":
    main()
