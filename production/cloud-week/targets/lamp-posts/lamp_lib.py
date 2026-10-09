"""Shared helpers for the lamp-post target's photograph work (author tools; the self-check and the drawing do not need them).

Panoramas are Poly Haven's tone-mapped JPGs (CC0, Andreas Mischok, 8192 x 4096, equirectangular, level), saved as <PANO_DIR>/tm_<id>.jpg.
elevation() re-projects a vertical plane that passes through an object's axis, square to the line of sight, to a flat picture at a stated
millimetres a pixel; the plane's distance d (horizontal, metres) and the camera's height above the object's ground (metres) are the two
numbers that give the picture its scale (the same method as the bollards' and kerbs' targets; calibrate.py there)."""
import os
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

Image.MAX_IMAGE_PIXELS = None
_cache = {}


def load(pano_dir, name):
    key = (pano_dir, name)
    if key not in _cache:
        _cache[key] = np.asarray(Image.open(os.path.join(pano_dir, f"tm_{name}.jpg")).convert("RGB"))
    return _cache[key]


def rot(yaw, pitch):
    cy, sy = np.cos(np.radians(yaw)), np.sin(np.radians(yaw))
    cp, sp = np.cos(np.radians(pitch)), np.sin(np.radians(pitch))
    return np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]) @ np.array([[1, 0, 0], [0, cp, sp], [0, -sp, cp]])


def to_uv(d, W, H):
    lon = np.arctan2(d[..., 0], d[..., 2])
    lat = np.arcsin(np.clip(d[..., 1] / np.linalg.norm(d, axis=-1), -1, 1))
    return (lon / (2 * np.pi) + 0.5) * W, (0.5 - lat / np.pi) * H


def sample(img, u, v):
    out = np.empty(u.shape + (3,), np.float32)
    for c in range(3):
        out[..., c] = map_coordinates(img[..., c].astype(np.float32), [v, u], order=1, mode="wrap")
    return out


def view(img, yaw, pitch, fov, w, h):
    """rectilinear view, fov = horizontal degrees; yaw 0 is the panorama's centre column"""
    H, W, _ = img.shape
    f = (w / 2) / np.tan(np.radians(fov) / 2)
    X, Y = np.meshgrid((np.arange(w) - w / 2 + .5) / f, -(np.arange(h) - h / 2 + .5) / f)
    d = np.stack([X, Y, np.ones_like(X)], -1) @ rot(yaw, pitch).T
    return sample(img, *to_uv(d, W, H))


def elevation(img, yaw_c, d, cam_h, x0, x1, z0, z1, mm):
    """Flat square-on picture of the vertical plane at horizontal distance d (m) on bearing yaw_c (deg), camera cam_h (m) above the plane's
    ground (z = 0). Columns are x (mm, to the right), rows are z (mm, up); row 0 is z1. Returns float32 (rows, cols, 3)."""
    H, W, _ = img.shape
    X, Z = np.meshgrid(np.arange(x0, x1, mm) / 1000.0 + mm / 2000.0, np.arange(z1, z0, -mm) / 1000.0 - mm / 2000.0)
    cy, sy = np.cos(np.radians(yaw_c)), np.sin(np.radians(yaw_c))
    fwd = np.array([sy, 0, cy])
    rgt = np.array([cy, 0, -sy])
    d3 = d * fwd[None, None, :] + X[..., None] * rgt[None, None, :] + np.array([0, 1, 0])[None, None, :] * (Z[..., None] - cam_h)
    return sample(img, *to_uv(d3, W, H))


def luminance(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def save_jpeg(arr, path, max_side=1200, size_cap=300_000, quality=90):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    if max(im.size) > max_side:
        s = max_side / max(im.size)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
    q = quality
    while True:
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) < size_cap or q <= 45:
            break
        q -= 5
    return os.path.getsize(path), im.size
