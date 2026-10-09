#!/usr/bin/env python
"""Re-makes the reduced reference crops and overlays of TARGET.md (lamp-posts family).

    /home/user/.bpyenv/bin/python make_previews.py PANO_DIR [OUT_DIR]

PANO_DIR holds Poly Haven's tone-mapped JPGs (CC0, Andreas Mischok, 8192 x 4096): tm_bethnal_green_entrance.jpg and tm_urban_street_01.jpg.
OUT_DIR defaults to production/previews/cloud-week/refs/lamp-posts/. Every crop is of the object only: signs that carry text, a telephone number or a drawing are masked
flat grey, a parked car is cropped out, nothing else is in frame (no people, no shop names, no children, no drink, no betting). JPEG, at most 1200 px, under 300 KB.
The overlay (-target-on-photo) draws target.json's lower column over the BGE strips at a scale fitted on ONE dimension only (the sleeve's width on the photograph)."""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lamp_lib as L  # noqa: E402
import target_drawing as TD  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PANO = sys.argv[1]
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "production", "previews", "cloud-week", "refs", "lamp-posts")
os.makedirs(OUT, exist_ok=True)
T = TD.load()
PF = T["photo_frames"]
GREY = np.array([128, 128, 128], np.float32)


def mask_rect(strip, x0, mm, z1, xa, xb, za, zb):
    """paint the rectangle x in [xa, xb], z in [za, zb] of a strip flat grey; the strip's column 0 is x0, its row 0 is z1"""
    z0 = z1 - strip.shape[0] * mm
    if zb < z0 or za > z1:
        return
    c0 = max(0, int((xa - x0) / mm))
    c1 = min(strip.shape[1], int((xb - x0) / mm) + 1)
    r0 = max(0, int((z1 - min(zb, z1)) / mm))
    r1 = min(strip.shape[0], int((z1 - max(za, z0)) / mm) + 1)
    strip[r0:r1, c0:c1] = GREY


def bge_strips():
    img = L.load(PANO, "bethnal_green_entrance")
    f = PF["BGE_STRIPS"]
    mm, x0, x1 = f["mm_per_px"], f["x0_mm"], f["x1_mm"]
    out = []
    for s in f["strips"]:
        st = L.elevation(img, f["yaw_deg"], f["d_m"], f["camera_height_m"], x0, x1, s["z0"], s["z1"], mm)
        # masks: the blue sign and the drawn board (z 2205 to 2850) and the notice board (z 2990 to 3725), full strip width
        mask_rect(st, x0, mm, s["z1"], x0, x1, 2205, 2850)
        mask_rect(st, x0, mm, s["z1"], x0, x1, 2990, 3725)
        out.append(st)
    gap = np.full((out[0].shape[0], f["gap_px"], 3), 244, np.float32)
    row = []
    for i, st in enumerate(out):
        row.append(st)
        if i < len(out) - 1:
            row.append(gap)
    return np.concatenate(row, axis=1)


def measure_sleeve_centre_scale(strip0):
    """left and right edge of the sleeve in strip 0 (z 100 to 800) by the gradient fit: returns (centre_x_mm, width_mm)"""
    f = PF["BGE_STRIPS"]
    mm, x0 = f["mm_per_px"], f["x0_mm"]
    ws, cs = [], []
    for z in range(100, 900, 100):
        r = int((1200 - z) / mm)
        prof = L.luminance(strip0[r - 4:r + 5]).mean(0)
        g = np.gradient(np.convolve(prof, np.ones(3) / 3, mode="same"))
        xs = x0 + (np.arange(len(g)) + 0.5) * mm
        lw = (xs > -56 - 14) & (xs < -56 + 14)
        rw = (xs > 67 - 14) & (xs < 67 + 14)
        li = int(np.argmin(np.where(lw, g, 1e9)))
        ri = int(np.argmax(np.where(rw, g, -1e9)))
        ws.append(xs[ri] - xs[li])
        cs.append((xs[ri] + xs[li]) / 2)
    return float(np.mean(cs)), float(np.mean(ws))


def overlay_on_strips(sheet):
    f = PF["BGE_STRIPS"]
    mm, x0 = f["mm_per_px"], f["x0_mm"]
    strip_w = int((f["x1_mm"] - x0) / mm)
    xc, wmeas = measure_sleeve_centre_scale(sheet[:, :strip_w])
    s = wmeas / T["geometry"]["A"]["lower"]["outer_rz"][2][0] / 2.0
    im = Image.fromarray(np.clip(sheet, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for i, st in enumerate(f["strips"]):
        ox = i * (strip_w + f["gap_px"])
        left, right = [], []
        z = st["z0"]
        while z <= min(st["z1"], 4280):   # above z 4300 the photograph's column carries a post-top pod (variant P), not variant A's collar and bracket
            e = TD.lower_edges(T, z / s)
            if e:
                row = (st["z1"] - z) / mm
                left.append((ox + (xc + e[0] * s - x0) / mm, row))
                right.append((ox + (xc + e[1] * s - x0) / mm, row))
            z += 2
        if left:
            d.line(left, fill=(255, 40, 40), width=1)
            d.line(right, fill=(255, 40, 40), width=1)
    return im, s, xc


def bge_pod():
    img = L.load(PANO, "bethnal_green_entrance")
    f = PF["BGE_POD"]
    return L.elevation(img, 138.5, 2.73, 1.02, f["x0_mm"], f["x1_mm"], 4000, 4900, f["mm_per_px"])[: int((4900 - 4000) / f["mm_per_px"])]


def us01():
    img = L.load(PANO, "urban_street_01")
    f = PF["US01_ARM"]
    arm = L.elevation(img, f["yaw_deg"], f["d_m"], f["camera_height_m"], f["x0_mm"], f["x1_mm"], f["z0_mm"], f["z1_mm"], f["mm_per_px"])
    lit = L.view(img, -23.5, 49, 5, 800, 800)
    g = PF["US01_SLEEVE"]
    sl = L.elevation(img, f["yaw_deg"], f["d_m"], f["camera_height_m"], g["x0_mm"], g["x1_mm"], g["z0_mm"], g["z1_mm"], g["mm_per_px"])
    return arm, lit, sl


def hook_overlay():
    """lays variant A, at its scene slot x 8 east, on the Hook sheet's reduced copy with the sheet's own lens (production/reference/hook-sheet-lens.md; the scene's cam_hook):
    camera x -3.0, z -1.6, eye 2.2 above the crown, yaw 20.4 toward +z (the east, on the LEFT of the sheet), pitch -3.4, 46 degrees vertical on 1600 x 850. A placement test, not a measurement."""
    sheet = Image.open(os.path.join(ROOT, "production", "previews", "hook-sheet-2026-10-05.jpg")).convert("RGB")
    W, H = sheet.size
    fpx = (H / 2) / math.tan(math.radians(23.0))
    psi, th = math.radians(20.4), math.radians(-3.4)
    cam = np.array([-3.0, 2.2, -1.6])
    fwd0 = np.array([math.cos(psi), 0.0, math.sin(psi)])
    left = np.array([-math.sin(psi), 0.0, math.cos(psi)])
    up0 = np.array([0.0, 1.0, 0.0])
    fwd = math.cos(th) * fwd0 + math.sin(th) * up0
    up = -math.sin(th) * fwd0 + math.cos(th) * up0

    def proj(p):
        v = np.array(p) - cam
        depth = v @ fwd
        return (W / 2 - fpx * (v @ left) / depth, H / 2 - fpx * (v @ up) / depth)
    views = TD.build_views(T)
    gy = 0.065
    ox = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ox)
    for p in views["A_side_elevation"]["polys"]:
        for g in TD.polys_of(p["geom"]):
            pts = [proj((8.0, gy + v / 1000.0, 3.725 - u / 1000.0)) for u, v in g.exterior.coords]
            d.polygon(pts, fill=(255, 40, 40, 150), outline=(255, 255, 0, 255))
    # the kerb's back edge and the footway's front line, for scale: z 3.125 at the column's x and 10 m either side
    for zz in (3.0, 3.125):
        d.line([proj((x, 0.05, zz)) for x in (2.0, 14.0)], fill=(0, 255, 255, 255), width=1)
    out = Image.alpha_composite(sheet.convert("RGBA"), ox).convert("RGB")
    out = out.crop((420, 120, 1020, 720)).resize((960, 960), Image.LANCZOS)
    return out, proj((8.0, gy, 3.725)), proj((8.0, gy + 5.0, 3.725))


def save(arr_or_im, name):
    path = os.path.join(OUT, name)
    arr = np.asarray(arr_or_im) if not isinstance(arr_or_im, np.ndarray) else arr_or_im
    size, px = L.save_jpeg(arr, path)
    print(f"{name}: {px[0]} x {px[1]} px, {size / 1000:.0f} KB")
    return path


def main():
    sheet = bge_strips()
    save(sheet, PF["BGE_STRIPS"]["file"])
    im, s, xc = overlay_on_strips(sheet)
    save(np.asarray(im), PF["BGE_STRIPS"]["file"].replace("strips", "target-on-photo"))
    print("overlay scale fitted on the sleeve:", round(s, 4), "centre x", round(xc, 1))
    save(bge_pod(), PF["BGE_POD"]["file"])
    arm, lit, sl = us01()
    save(arm, PF["US01_ARM"]["file"])
    save(lit, PF["US01_LIT"]["file"])
    save(sl, PF["US01_SLEEVE"]["file"])
    hk, base, top = hook_overlay()
    save(np.asarray(hk), "hook-sheet-slot-x8-east-target-on-sheet.jpg")
    print("slot on the 1600 x 850 sheet: foot", [round(v) for v in base], "lantern-level", [round(v) for v in top])


if __name__ == "__main__":
    main()
