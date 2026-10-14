"""The Poly Haven helpers of the house windows: the fetcher's import, the glTF and map lookups, the blanking of a mark on a map, an HDRI loaded as an array and viewed through a pinhole.

Copied on 14 October 2026 (03:13 UTC) from production/cloud-week/kit/shop-windows/sw_assets.py (md5 3d64a1c39efff85d63e37ba641cb2bef at the copy) and TRIMMED to what the house windows use:
_fetcher, gltf_path, base_maps, map_path, _ring, _grain, _edge_share, _clean_patch, blank_map, _load_hdri, _rect_view are the shop kit's functions as they were; the shops' own blanking tables, their
print library and their texture lists are not copied (they hold other shops' models). The house windows' marks and prints are in hw_models.py.
"""
import hashlib
import importlib.util
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
POLY = os.environ.get("LEDGER_HW_SCRATCH", "/home/user/ledger-scratch/house-windows") + "/polyhaven"
RES = "1k"


def _fetcher():
    path = os.path.join(REPO, "tools", "art-recipes", "fetch_polyhaven.py")
    spec = importlib.util.spec_from_file_location("fetch_polyhaven", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gltf_path(asset, clean=True):
    folder = os.path.join(POLY, asset, RES)
    if clean:
        c = os.path.join(folder, asset + "_clean.gltf")
        if os.path.exists(c):
            return c
    return next((os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.endswith(".gltf") and not f.endswith("_clean.gltf")), None)


def base_maps(asset):
    """The base-colour image files a model's glTF names (paths relative to its folder, once each)."""
    g = json.load(open(gltf_path(asset, clean=False), encoding="utf-8"))
    out = []
    for m in g.get("materials", []):
        t = m.get("pbrMetallicRoughness", {}).get("baseColorTexture")
        if t is not None:
            img = g["textures"][t["index"]]["source"]
            if g["images"][img]["uri"] not in out:
                out.append(g["images"][img]["uri"])
    return out


def map_path(asset, name):
    """The relative path (as the glTF writes it) of the image whose file name is `name`."""
    g = json.load(open(gltf_path(asset, clean=False), encoding="utf-8"))
    for im in g["images"]:
        if os.path.basename(im["uri"]) == name:
            return im["uri"]
    raise KeyError("%s has no image %s" % (asset, name))


def _ring(arr, box, w=6):
    h, wd = arr.shape[:2]
    x0, y0, x1, y1 = box
    X0, Y0, X1, Y1 = max(0, x0 - w), max(0, y0 - w), min(wd, x1 + w), min(h, y1 + w)
    m = np.ones((Y1 - Y0, X1 - X0), bool)
    m[(y0 - Y0):(y1 - Y0), (x0 - X0):(x1 - X0)] = False
    patch = arr[Y0:Y1, X0:X1][m]
    return np.median(patch, axis=0)


def _grain(p):
    """A patch's grain: the patch minus its own broad level (a 4 px blur)."""
    pim = Image.fromarray(np.clip(p, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
    return p - np.asarray(pim).astype(np.float32)


def _edge_share(p):
    gy, gx = np.gradient(p.mean(axis=2))
    return float((np.hypot(gx, gy) > 14).mean())


def _clean_patch(arr, box, boxes, rng):
    """A same-size patch of the map's own grain from the nearest area that is clear of every listed box, close in colour to the ring, and
    itself free of print and edges (a patch that carries numerals or a scale would only move the lettering). None when the map has no such
    area near: the caller then draws grain of the ring's own strength."""
    h, wd = arr.shape[:2]
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    ring = _ring(arr, box)

    def clear(a, b, c, d):
        if a < 0 or b < 0 or c > wd or d > h:
            return False
        for (u0, v0, u1, v1) in boxes:
            if not (c <= u0 - 4 or a >= u1 + 4 or d <= v0 - 4 or b >= v1 + 4):
                return False
        return True
    for r in range(1, 60):
        for dx, dy in ((0, -r), (0, r), (-r, 0), (r, 0), (-r, -r), (r, -r), (-r, r), (r, r)):
            a, b = x0 + dx * (bw + 6) // 2, y0 + dy * (bh + 6) // 2
            if not clear(a, b, a + bw, b + bh):
                continue
            p = arr[b:b + bh, a:a + bw]
            dist = float(np.abs(np.median(p.reshape(-1, p.shape[-1]), axis=0) - ring).max())
            if dist < 30 and _edge_share(p) < 0.0015:
                return a, b
    return None


def blank_map(src, dst, boxes, whole_map_print=None, seed=1, fills=None, grain_scale=1.0):
    """Paint the boxes of one map to their ring colour plus the map's own grain. Returns the report rows."""
    img = Image.open(src).convert("RGB")
    arr = np.asarray(img).astype(np.float32)
    out = arr.copy()
    rows = []
    rng = np.random.default_rng(seed)
    for box in boxes:
        x0, y0, x1, y1 = box
        ring = _ring(arr, box)
        if fills and tuple(box) in fills:
            ring = np.array(fills[tuple(box)], np.float32)
        pos = _clean_patch(arr, box, boxes, rng)
        fill = np.empty((y1 - y0, x1 - x0, 3), np.float32)
        fill[:] = ring
        if pos is not None:
            a, b = pos
            grain = _grain(arr[b:b + (y1 - y0), a:a + (x1 - x0)])
            how = "the map's own grain from the patch at %s" % (pos,)
        else:
            # no clean area near: grain of the ring's own strength (the ring is the print-free pixels just outside the box)
            h, wd = arr.shape[:2]
            X0, Y0, X1, Y1 = max(0, x0 - 8), max(0, y0 - 8), min(wd, x1 + 8), min(h, y1 + 8)
            rp = _grain(arr[Y0:Y1, X0:X1])
            m = np.ones(rp.shape[:2], bool)
            m[(y0 - Y0):(y1 - Y0), (x0 - X0):(x1 - X0)] = False
            sd = np.clip(np.median(np.abs(rp[m]), axis=0) * 1.4826, 1.0, 9.0)
            grain = rng.normal(0.0, 1.0, (y1 - y0, x1 - x0, 3)).astype(np.float32) * sd
            grain = np.asarray(Image.fromarray(np.clip(grain + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) - 128
            how = "grain drawn at the ring's strength (%s)" % ", ".join("%.1f" % v for v in sd)
        fill = fill + np.clip(grain * grain_scale, -13, 13)
        out[y0:y1, x0:x1] = fill
        rows.append({"box": box, "ring": [round(float(c), 1) for c in ring], "patch_from": pos, "grain": how})
    Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst, quality=98, subsampling=0)
    return rows


def _load_hdri(path):
    import bpy
    im = bpy.data.images.load(path, check_existing=True)
    w, h = im.size
    px = np.empty(w * h * 4, np.float32)
    im.pixels.foreach_get(px)
    return px.reshape(h, w, 4)[::-1, :, :3].copy()             # row 0 at the top


def _rect_view(env, yaw_deg, pitch_deg, hfov_deg, out_w, out_h):
    """A rectilinear (pinhole) view of an equirectangular image: yaw, pitch and horizontal field in degrees; bilinear."""
    h, w = env.shape[:2]
    f = (out_w / 2.0) / np.tan(np.radians(hfov_deg) / 2.0)
    xs = (np.arange(out_w) + 0.5 - out_w / 2.0)
    ys = (np.arange(out_h) + 0.5 - out_h / 2.0)
    X, Y = np.meshgrid(xs, ys)
    d = np.stack([X / f, -Y / f, np.ones_like(X)], axis=-1)                # camera: +z forward, +y up
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    p, yv = np.radians(pitch_deg), np.radians(yaw_deg)
    Rp = np.array([[1, 0, 0], [0, np.cos(p), -np.sin(p)], [0, np.sin(p), np.cos(p)]])
    Ry = np.array([[np.cos(yv), 0, np.sin(yv)], [0, 1, 0], [-np.sin(yv), 0, np.cos(yv)]])
    d = d @ Rp.T @ Ry.T
    lon = np.arctan2(d[..., 0], d[..., 2])
    lat = np.arcsin(np.clip(d[..., 1], -1, 1))
    u = (lon / (2 * np.pi) + 0.5) * w - 0.5
    v = (0.5 - lat / np.pi) * h - 0.5
    out = np.stack([ndimage.map_coordinates(env[..., c], [v, u], order=1, mode="wrap") for c in range(3)], axis=-1)
    return out
