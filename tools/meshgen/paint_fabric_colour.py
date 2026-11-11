#!/usr/bin/env python3
"""A GARMENT'S OWN COLOUR MAP, PAINTED WITH ITS FABRIC'S STRUCTURE (11 November 2026, Tom's surfaces, the researched
different method after two failed tries with shared tiles).

    python tools/meshgen/paint_fabric_colour.py SPEC.json

WHY. His look at Tom (11 Nov): "the jacket has no cloth texture, the jeans no denim". The garment material draws
Tint x ColourMap, and the colour maps were neutral greys, so every pixel of a garment had one hue: lighter or darker,
never denim's two-yarn colour. Shared tiles (try 1 and 2) failed: a weave is invisible past arm's length and cloth
sheen chalked the jeans. Denim reads by colour structure: an indigo warp over a pale weft, the weft showing where the
cloth is rubbed (thighs, knees, seat, seams' ridges, hems), vertical slub streaks along the grain, stonewash mottle;
seams and hollows keep the deep dye. Cotton reads by a fine heather and faint wear at edges. So the colour is painted
into the garment's own map, in true millimetres along each pattern piece's grain, and the row's tint goes to white.

THE SPEC (JSON): {"grey": the garment's baked colour map (neutral grey with its wear, seams and occlusion: the chain's
own map), "out": the painted PNG, "kind": "denim" or "cotton", "target_linear": [r,g,b] the average cloth colour the
garment showed before (its old tint times the grey's median, so the look he judged keeps its colour), and either
"raster": an .npz with per-pixel pattern coordinates in mm ("px_pat", "py_pat", "piece"; the bake chain's raster_flat)
with "grain_x_pieces" (pieces whose grain runs along x, e.g. waistbands), or "mm_per_px" (no raster: the map's own
axes stand in, grain along "grain_axis" "u" or "v"); optional "seed", "amounts" overriding the defaults below,
"preview": a smaller JPEG beside it}.
The npz's rows run bottom-up (UV v), so they are flipped to the image's rows; the script checks the flip against the
grey map's empty pixels and stops if neither orientation matches.

Every amount is a weft-visibility fraction (denim) or a lightness fraction (cotton); the defaults were chosen to read
at 3 to 8 m and are judged by eye at the gate (FADE-REFERENCE.md beside Tom's jeans names the wear's sources).
"""
import json
import os
import sys

import numpy as np
from PIL import Image

DENIM = {
    "weft_linear": [0.50, 0.49, 0.45],   # ecru weft, dulled
    "v0": 0.08,          # baseline weft showing on unworn stonewash
    "fade_gain": 1.0,    # weft visibility per unit the grey map rises above its median (its wear: thighs, knees, seat)
    "dark_gain": 1.0,    # colour multiplied by the grey's ratio below its median (seams, hollows, occlusion)
    "heather": [0.8, 0.8, 0.05],      # cell mm across, mm along, amplitude: yarn-level speckle
    "slub": [1.2, 26.0, 0.06],        # warp slubs: thin streaks along the grain
    "rope": [3.5, 120.0, 0.035],      # roping: long soft streaks
    "mottle": [28.0, 28.0, 0.04],     # stonewash mottle
    "mottle2": [70.0, 70.0, 0.03],
    "vmax": 0.55,
}
COTTON = {
    "heather": [0.7, 0.7, 0.045],     # lightness fraction
    "slub": [1.0, 18.0, 0.03],
    "mottle": [35.0, 35.0, 0.025],
    "edge_gain": 0.6,    # lightening per unit the grey map rises (worn edges), desaturating as it goes
    "dark_gain": 1.0,
}


def srgb_to_lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055) * 255.0


def value_noise(x, y, sx, sy, seed):
    """Smooth value noise on a lattice of sx by sy mm, sampled at mm coordinates x, y (arrays)."""
    rng = np.random.default_rng(seed)
    gx, gy = x / sx, y / sy
    ix, iy = np.floor(gx).astype(np.int64), np.floor(gy).astype(np.int64)
    fx, fy = gx - ix, gy - iy
    fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    ox, oy = ix.min(), iy.min()
    w, h = ix.max() - ox + 2, iy.max() - oy + 2
    lat = rng.uniform(-1, 1, size=(h, w)).astype(np.float32)
    a, b = ix - ox, iy - oy
    v00, v10, v01, v11 = lat[b, a], lat[b, a + 1], lat[b + 1, a], lat[b + 1, a + 1]
    return (v00 * (1 - fx) + v10 * fx) * (1 - fy) + (v01 * (1 - fx) + v11 * fx) * fy


def layered(along, across, spec_amounts, keys, seed):
    out = np.zeros_like(along)
    for i, k in enumerate(keys):
        if k not in spec_amounts:
            continue
        sa, sl, amp = spec_amounts[k]
        out += amp * value_noise(across, along, sa, sl, seed + 101 * (i + 1))
    return out


def ridges(normal_png, cloth):
    """0 to 1 where the baked normal map bulges outward (seam ridges, fold crests, edges): cotton fades there first.
    The map is DirectX (green down); convexity = d(nx)/dcol + d(ny_down)/drow, softened over about 1.5 px, scaled by its
    99th percentile on the cloth."""
    nm = np.asarray(Image.open(normal_png).convert("RGB")).astype(np.float32) / 127.5 - 1
    nx, ny_down = nm[..., 0], nm[..., 1]   # DirectX: green points down the image, the way rows run
    conv = np.gradient(nx, axis=1) + np.gradient(ny_down, axis=0)
    k = np.array([1, 4, 6, 4, 1], dtype=np.float32) / 16
    for ax in (0, 1):
        conv = np.apply_along_axis(lambda v: np.convolve(v, k, mode="same"), ax, conv)
    pos = np.maximum(conv, 0)
    s = np.percentile(pos[cloth], 99) if cloth.any() else 1
    return np.clip(pos / max(s, 1e-6), 0, 1)


def coords(spec, alpha):
    """mm coordinates along and across the grain for every pixel, and the cloth mask."""
    h, w = alpha.shape
    if "raster" in spec:
        z = np.load(spec["raster"])
        piece, x, y = z["piece"], z["px_pat"], z["py_pat"]
        # every raster piece pixel must land on painted (alpha > 0) map; the bake's padding may reach further
        filled = alpha > 0
        ok_flip = np.mean(filled[np.flipud(piece) >= 0])
        ok_same = np.mean(filled[piece >= 0])
        if max(ok_flip, ok_same) < 0.98:
            sys.exit("the raster's pieces match the grey map's empty pixels in neither orientation (%.3f, %.3f)" % (ok_same, ok_flip))
        if ok_flip > ok_same:
            piece, x, y = np.flipud(piece), np.flipud(x), np.flipud(y)
        along, across = y.copy(), x.copy()
        for p in spec.get("grain_x_pieces", []):
            m = piece == p
            along[m], across[m] = x[m], y[m]
        # each piece its own noise: offset by piece so mirrored halves never repeat each other
        off = (piece.astype(np.float32) + 1) * 5000.0
        return along + off, across + off * 0.37, piece >= 0
    mm = spec["mm_per_px"]
    rr, cc = np.mgrid[0:h, 0:w].astype(np.float32)
    if spec.get("grain_axis", "v") == "v":
        return rr * mm, cc * mm, alpha > 0
    return cc * mm, rr * mm, alpha > 0


def main(path):
    spec = json.load(open(path, encoding="utf-8"))
    im = Image.open(spec["grey"]).convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    alpha = a[..., 3]
    grey = srgb_to_lin(a[..., :3]).mean(axis=2)
    along, across, cloth = coords(spec, alpha)
    cloth &= alpha > 0
    g0 = float(np.median(grey[cloth]))
    r = grey / max(g0, 1e-4)
    target = np.array(spec["target_linear"], dtype=np.float32)
    seed = int(spec.get("seed", 1990))
    kind = spec["kind"]
    if kind == "denim":
        am = dict(DENIM, **spec.get("amounts", {}))
        weft = np.array(am["weft_linear"], dtype=np.float32)
        v0 = am["v0"]
        warp = (target - v0 * weft) / (1 - v0)   # so unworn cloth averages to the colour he judged
        if (warp <= 0).any():
            sys.exit("the target is too pale for this weft and v0: warp would be %s" % warp)
        n = layered(along, across, am, ["heather", "slub", "rope", "mottle", "mottle2"], seed)
        # a soft ceiling on the wear (a hard clip left the thighs one flat grey), the streaks kept on top of it,
        # and the warp itself paler where rubbed (ring-dyed indigo wears to a lighter blue, not to grey)
        fade = am["fade_gain"] * np.maximum(r - 1, 0)
        base = am["vmax"] * np.tanh((v0 + fade) / am["vmax"])
        v = np.clip(base + n, 0, 0.6)
        warp_l = warp[None, None, :] * (1 + am.get("warp_fade", 1.5) * fade[..., None])
        col = warp_l * (1 - v[..., None]) + weft[None, None, :] * v[..., None]
        shade = np.where(r < 1, r ** am["dark_gain"], 1.0)
        col = col * shade[..., None]
    elif kind == "cotton":
        am = dict(COTTON, **spec.get("amounts", {}))
        n = layered(along, across, am, ["heather", "slub", "mottle"], seed)
        lift = am["edge_gain"] * np.maximum(r - 1, 0)
        if spec.get("ridge_normal"):
            lift = lift + am.get("ridge_gain", 0.35) * ridges(spec["ridge_normal"], cloth)
        lum = 1 + n + lift
        grey_t = np.full(3, float(target.mean()), dtype=np.float32)
        desat = np.clip(lift * 1.5, 0, 0.5)[..., None]   # worn edges go greyer as well as lighter
        base = target[None, None, :] * (1 - desat) + grey_t[None, None, :] * desat
        shade = np.where(r < 1, r ** am["dark_gain"], 1.0)
        col = base * (lum * shade)[..., None]
    else:
        sys.exit("kind must be denim or cotton")
    out = lin_to_srgb(col)
    bg = lin_to_srgb(np.broadcast_to(target, out.shape))
    out = np.where(cloth[..., None], out, bg)   # padding and empty space take the average, so mips never bleed grey
    rgba = np.dstack([out, alpha]).round().clip(0, 255).astype(np.uint8)
    os.makedirs(os.path.dirname(spec["out"]), exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(spec["out"])
    mean_lin = col[cloth].mean(axis=0)
    rec = {"spec": path, "out": spec["out"], "grey_median_linear": g0, "target_linear": target.tolist(),
           "painted_mean_linear": [round(float(c), 4) for c in mean_lin],
           "painted_mean_srgb": [round(float(c)) for c in lin_to_srgb(mean_lin)]}
    if spec.get("preview"):
        Image.fromarray(rgba[..., :3]).resize((1024, 1024), Image.LANCZOS).save(spec["preview"], quality=88)
    json.dump(rec, open(os.path.splitext(spec["out"])[0] + ".record.json", "w"), indent=1)
    print("painted %s: mean linear %s (target %s), sRGB %s" % (spec["out"], rec["painted_mean_linear"], rec["target_linear"], rec["painted_mean_srgb"]))


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].endswith(".json"):
        sys.exit("usage: paint_fabric_colour.py SPEC.json")
    main(sys.argv[1])
