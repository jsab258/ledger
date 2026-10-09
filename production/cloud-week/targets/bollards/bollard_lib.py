"""Shared helpers of the bollards family: a lathe profile as r(z), its silhouette, and the edge fit of a drawing on a photograph.
Pure numpy (PIL only to read pictures)."""
import math
import numpy as np


def scale_profile(pts, k):
    return [(round(r * k, 2), round(z * k, 2)) for r, z in pts]


def r_of_z(profile, zs):
    """radius at heights zs for a profile that rises in z (ties are allowed: the larger r wins). Outside the profile: nan."""
    P = np.array(profile, float)
    z = P[:, 1] + np.arange(len(P)) * 1e-6          # break ties
    r = P[:, 0]
    out = np.interp(zs, z, r, left=np.nan, right=np.nan)
    return out


def silhouette(profile, a0=0.0, lean_deg=0.0):
    """(left, right) outline point lists (t, z) in mm of a profile with its axis at t = a0 + z tan(lean) -- the elevation polygon"""
    P = np.array(profile, float)
    s = math.tan(math.radians(lean_deg))
    left = [(a0 + s * z - r, z) for r, z in P]
    right = [(a0 + s * z + r, z) for r, z in P]
    return left, right


def elevation_polygon(profile, a0=0.0, lean_deg=0.0):
    left, right = silhouette(profile, a0, lean_deg)
    return left + right[::-1]


def gradient_x(gray, sigma=1.5):
    from scipy.ndimage import gaussian_filter
    g = gaussian_filter(gray.astype(float), sigma)
    gx = np.zeros_like(g)
    gx[:, 1:-1] = (g[:, 2:] - g[:, :-2]) / 2.0
    return gx


def fit_axis(gray, mm, t_left, z_top, profile, z_lo=15.0, z_hi=None, step=4.0):
    """grid search of the axis offset a0 (mm) and lean (deg) of a profile on a picture (1 px = mm, column 0 at t_left, row 0 at z_top);
    maximises the sum of |horizontal gradient| at the two predicted edges. returns a0, lean_deg, score"""
    gx = np.abs(gradient_x(gray))
    P = np.array(profile, float)
    H = P[:, 1].max()
    z_hi = H - 20 if z_hi is None else z_hi
    zs = np.arange(z_lo, z_hi, step)
    rs = r_of_z(profile, zs)
    ok = ~np.isnan(rs)
    zs, rs = zs[ok], rs[ok]
    rows = np.clip(((z_top - zs) / mm).astype(int), 0, gx.shape[0] - 1)
    best = (-1, 0, 0)
    for lean in np.arange(-2.0, 2.01, 0.1):
        s = math.tan(math.radians(lean))
        for a0 in np.arange(-30, 30.1, 1.0):
            cl = ((a0 + s * zs - rs) - t_left) / mm
            cr = ((a0 + s * zs + rs) - t_left) / mm
            m = (cl >= 1) & (cr < gx.shape[1] - 2)
            if m.sum() < len(zs) * 0.8:
                continue
            sc = gx[rows[m], np.round(cl[m]).astype(int)].sum() + gx[rows[m], np.round(cr[m]).astype(int)].sum()
            if sc > best[0]:
                best = (sc, a0, lean)
    return best[1], best[2], best[0]


def edge_residuals(gray, mm, t_left, z_top, profile, a0, lean_deg, win=12.0, step=5.0, z_lo=15.0, z_hi=None, min_contrast=2.0):
    """for rows along the profile: the offset (mm) from the predicted edge to the strongest edge within +-win mm, left and right;
    returns arrays of offsets (px==mm) and the fraction of rows with enough contrast"""
    gx = gradient_x(gray)
    P = np.array(profile, float)
    H = P[:, 1].max()
    z_hi = H - 15 if z_hi is None else z_hi
    s = math.tan(math.radians(lean_deg))
    offs, rows_used, total = [], 0, 0
    for z in np.arange(z_lo, z_hi, step):
        r = r_of_z(profile, np.array([z]))[0]
        if np.isnan(r):
            continue
        row = int(round((z_top - z) / mm))
        if not 0 <= row < gx.shape[0]:
            continue
        for sign in (-1, 1):
            total += 1
            t_pred = a0 + s * z + sign * r
            c = (t_pred - t_left) / mm
            lo, hi = int(round(c - win / mm)), int(round(c + win / mm))
            if lo < 1 or hi >= gx.shape[1] - 1:
                continue
            seg = np.abs(gx[row, lo:hi + 1])
            k = int(np.argmax(seg))
            if seg[k] < min_contrast:
                continue
            rows_used += 1
            offs.append((lo + k - c) * mm)
    return np.array(offs), rows_used / max(total, 1)
