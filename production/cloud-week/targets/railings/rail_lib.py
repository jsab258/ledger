"""Shared helpers of the railings family: re-projecting an equirectangular panorama onto a vertical plane (an elevation), pixel <-> ray, and edge probes.
Pure numpy and scipy (PIL only to read pictures).  Frame of a panorama: the camera at the origin, x to the east of the panorama's own lon = +90 deg,
y forward (lon = 0 is the middle column), z up; the ground is the plane z = -h (h the camera height above the ground the object stands on)."""
import math
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates
Image.MAX_IMAGE_PIXELS = None

_cache = {}


def load_gray(path):
    k = ('g', path)
    if k not in _cache:
        _cache[k] = np.asarray(Image.open(path).convert('L'), float)
    return _cache[k]


def load_rgb(path):
    k = ('c', path)
    if k not in _cache:
        _cache[k] = np.asarray(Image.open(path).convert('RGB'), float)
    return _cache[k]


def pix_to_dir(col, row, W, H):
    lon = (col / W - 0.5) * 2 * math.pi
    lat = (0.5 - row / H) * math.pi
    return np.array([math.cos(lat) * math.sin(lon), math.cos(lat) * math.cos(lon), math.sin(lat)])


def dir_to_pix(d, W, H):
    d = np.asarray(d, float)
    lon = np.arctan2(d[..., 0], d[..., 1])
    lat = np.arctan2(d[..., 2], np.hypot(d[..., 0], d[..., 1]))
    return (lon / (2 * math.pi) + 0.5) * W, (0.5 - lat / math.pi) * H


def ground_point(col, row, W, H, h):
    """(x, y) on the ground plane z = -h seen at pixel (col, row); row must be below the horizon"""
    d = pix_to_dir(col, row, W, H)
    if d[2] >= 0:
        raise ValueError('above the horizon')
    t = h / -d[2]
    return np.array([d[0] * t, d[1] * t])


class Plane:
    """a vertical plane through two ground points A and B (metres); s runs from A toward B (mm), z up from the ground (mm); off (mm) moves the plane
    away from the camera along its normal (0 = the line AB itself)"""

    def __init__(self, A, B, h, off_mm=0.0):
        self.A = np.asarray(A, float)
        self.B = np.asarray(B, float)
        self.h = float(h)
        e = self.B - self.A
        self.length = float(np.hypot(*e))
        self.e = e / self.length
        n = np.array([-self.e[1], self.e[0]])
        if np.dot(n, self.A) < 0:       # the normal points away from the camera
            n = -n
        self.n = n
        self.off = off_mm / 1000.0

    def point(self, s_mm, z_mm):
        s = np.asarray(s_mm, float) / 1000.0
        z = np.asarray(z_mm, float) / 1000.0
        P = self.A[None, None, :] if np.ndim(s) == 2 else self.A
        xy = np.stack([self.A[0] + s * self.e[0] + self.off * self.n[0], self.A[1] + s * self.e[1] + self.off * self.n[1]], -1)
        return np.concatenate([xy, (z - self.h)[..., None]], -1)

    def to_pix(self, s_mm, z_mm, W, H):
        return dir_to_pix(self.point(s_mm, z_mm), W, H)

    def distance(self, s_mm):
        """horizontal distance (m) from the camera to the plane point at s"""
        s = np.asarray(s_mm, float) / 1000.0
        return np.hypot(self.A[0] + s * self.e[0] + self.off * self.n[0], self.A[1] + s * self.e[1] + self.off * self.n[1])


def elevation(path, plane, s0, s1, z0, z1, mm, rgb=False, order=1):
    """the plane's elevation as an array, 1 px = mm, row 0 = z1 (top), column 0 = s0; gray unless rgb"""
    img = load_rgb(path) if rgb else load_gray(path)
    H, W = img.shape[:2]
    ss = s0 + (np.arange(int(round((s1 - s0) / mm))) + 0.5) * mm
    zz = z1 - (np.arange(int(round((z1 - z0) / mm))) + 0.5) * mm
    S, Z = np.meshgrid(ss, zz)
    u, v = plane.to_pix(S, Z, W, H)
    u = u % W
    if rgb:
        out = np.stack([map_coordinates(img[..., c], [v - 0.5, u - 0.5], order=order, mode='nearest') for c in range(3)], -1)
    else:
        out = map_coordinates(img, [v - 0.5, u - 0.5], order=order, mode='nearest')
    return out


def local_scale(path, plane, s_mm, z_mm=500.0):
    """mm per pixel across and up on the panorama at plane point s (a check on the resolution)"""
    im = Image.open(path)
    W, H = im.size
    u0, v0 = plane.to_pix(np.array([[s_mm]]), np.array([[z_mm]]), W, H)
    u1, _ = plane.to_pix(np.array([[s_mm + 100.0]]), np.array([[z_mm]]), W, H)
    _, v1 = plane.to_pix(np.array([[s_mm]]), np.array([[z_mm + 100.0]]), W, H)
    return 100.0 / abs(float(u1 - u0)), 100.0 / abs(float(v0 - v1))


def smooth(a, sigma):
    from scipy.ndimage import gaussian_filter
    return gaussian_filter(a, sigma)
