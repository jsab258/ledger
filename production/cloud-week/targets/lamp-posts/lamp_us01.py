"""US01's bracket and lantern read in 3D (shared by measure_photos.py, make_previews.py and self_check.py).

Why 3D. The picture of US01 is an "elevation": the vertical plane through the column's axis, square to the line of sight, drawn flat (lamp_lib.elevation). An arm that points
out of that plane, toward the camera, shows extra rise in it: the camera looks UP at the bracket from 8.8 m away (about 45 degrees), so everything that points toward the camera
climbs in the picture. The street's own direction gives the arm's plan direction: the kerbs and parked cars vanish at bearing -57.8 degrees (photo_measurements.json
us01_street_vp), the column stands on the street's right-hand footway and its arm reaches over the carriageway, square to the kerb, so the arm points at bearing
-57.8 - 90 = -147.8 degrees: 42.1 degrees out of the picture's plane (the plane's own normal is the line of sight, bearing -15.7; the plane's left direction is -105.7).

plane(P) projects a 3D point (east, north, up above the footway; metres) from the camera (origin, at CAM above the footway) onto that plane: the same centre projection that made
the picture, so a 3D curve can be laid on the picture and compared with the photographed bracket."""
import math

import numpy as np
from scipy.optimize import least_squares
from shapely.geometry import LineString, Point

YAW, D, CAM = -15.7, 8.8, 1.16          # bearing of the column's axis (degrees), horizontal distance (m), camera height above the footway (m)
FWD = np.array([math.sin(math.radians(YAW)), math.cos(math.radians(YAW))])
RGT = np.array([math.cos(math.radians(YAW)), -math.sin(math.radians(YAW))])
AXIS = D * FWD                           # the column's axis in plan, metres east, north from the camera


def plane(P):
    """(east, north, up above the footway) metres -> (x, z) in the picture's plane, millimetres (x to the right, z above the footway)"""
    h = np.array(P[:2], float)
    u = P[2] - CAM
    s = D / float(h @ FWD)
    return float((h * s) @ RGT) * 1000.0, float(u * s + CAM) * 1000.0


def apparent_points(lum, x0, z1, mm, sky=None):
    """the apparent centreline of US01's stem and bend (rows, z 9830 to 10290) and arm (columns, x -1180 to -300) in an elevation picture's luminance array
    (columns x from x0 at mm a pixel, row 0 at z1); returns (stem_and_bend, arm) lists of (x, z) in millimetres"""
    if sky is None:
        sky = float(np.median(lum[:30, -60:]))
    thr = sky - 45
    stem = []
    for z in range(9830, 10300, 10):
        r = int((z1 - z) / mm)
        idx = np.where(lum[r] < thr)[0]
        if len(idx) == 0:
            continue
        runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
        ref = stem[-1][0] if stem else -33.0
        best = min(runs, key=lambda a: abs((x0 + (a[0] + a[-1]) / 2 * mm) - ref))
        stem.append((x0 + (best[0] + best[-1]) / 2 * mm, float(z)))
    arm = []
    for x in range(-1180, -300, 20):
        c = int((x - x0) / mm)
        idx = np.where(lum[:, c] < thr)[0]
        for a in np.split(idx, np.where(np.diff(idx) > 1)[0] + 1):
            if len(a) == 0:
                continue
            zc = z1 - (a[0] + a[-1]) / 2 * mm
            if 10100 <= zc <= 11300 and 30 <= len(a) * mm <= 140:
                arm.append((float(x), zc))
    return stem, arm


def observed(lum, x0, z1, mm):
    stem, arm = apparent_points(lum, x0, z1, mm)
    return np.array([p for p in stem if p[1] < 10300] + arm)


def target_curve(cl_yz, k, zs, beta_deg, z_socket_top):
    """the target's bracket centreline (y, z) of target.json, scaled by k about its own socket top and stood on US01's column at height zs (mm above the footway),
    its plan direction beta (bearing, degrees), as the apparent (x, z) polyline in the picture's plane. Only the part above the socket top is used."""
    a = np.array([math.sin(math.radians(beta_deg)), math.cos(math.radians(beta_deg))])
    out = []
    for y, z in cl_yz:
        if z < z_socket_top:
            continue
        hr = k * y / 1000.0
        up = (zs + k * (z - z_socket_top)) / 1000.0
        out.append(plane((AXIS[0] + a[0] * hr, AXIS[1] + a[1] * hr, up)))
    return np.array(out)


def residuals(poly, obs):
    ls = LineString([tuple(p) for p in poly])
    return np.array([ls.distance(Point(o)) for o in obs])


def fit_scaled(cl_yz, obs, beta_deg, z_socket_top):
    """fit the target's bracket (one uniform scale k and the height zs of its socket top on US01's shaft; nothing else): returns (k, zs, residuals)"""
    best = None
    for k0 in (1.5, 2.0, 2.5):
        for zs0 in (9700.0, 9800.0, 9900.0):
            r = least_squares(lambda p: residuals(target_curve(cl_yz, p[0], p[1], beta_deg, z_socket_top), obs), [k0, zs0], bounds=([0.5, 9400.0], [5.0, 10200.0]))
            if best is None or r.cost < best.cost:
                best = r
    res = residuals(target_curve(cl_yz, best.x[0], best.x[1], beta_deg, z_socket_top), obs)
    return float(best.x[0]), float(best.x[1]), res


def free_curve(zs, R, L, rake_deg, beta_deg, n=60):
    """a bracket of the same kind (vertical stem to zs, one bend of radius R, a straight arm to horizontal run L at rake above horizontal), all free in size: apparent polyline"""
    a = np.array([math.sin(math.radians(beta_deg)), math.cos(math.radians(beta_deg))])
    pts3 = [(AXIS[0], AXIS[1], z / 1000.0) for z in np.linspace(9700, zs, 10)]
    turn = math.radians(90 - rake_deg)
    for t in np.linspace(0, turn, n):
        hr = R * (1 - math.cos(t)) / 1000.0
        pts3.append((AXIS[0] + a[0] * hr, AXIS[1] + a[1] * hr, zs / 1000.0 + R * math.sin(t) / 1000.0))
    hr0 = R * (1 - math.cos(turn)) / 1000.0
    vz0 = zs / 1000.0 + R * math.sin(turn) / 1000.0
    for s in np.linspace(0, 1, 40):
        hh = hr0 + (L / 1000.0 - hr0) * s
        pts3.append((AXIS[0] + a[0] * hh, AXIS[1] + a[1] * hh, vz0 + (hh - hr0) * math.tan(math.radians(rake_deg))))
    return np.array([plane(p) for p in pts3])


def fit_free(obs, beta_deg, rake_deg=None):
    """stem height, bend radius and arm length free; the rake fixed (rake_deg) or free (None). Returns (params, residuals)"""
    best = None
    for zs0 in (9900.0, 9950.0):
        for R0 in (200.0, 435.0):
            for L0 in (1200.0, 1500.0, 2000.0):
                if rake_deg is None:
                    for rk0 in (0.0, 20.0, 40.0):
                        r = least_squares(lambda p: residuals(free_curve(p[0], p[1], p[2], p[3], beta_deg), obs), [zs0, R0, L0, rk0],
                                          bounds=([9800.0, 50.0, 500.0, -30.0], [10100.0, 1500.0, 4000.0, 70.0]))
                        if best is None or r.cost < best.cost:
                            best = r
                else:
                    r = least_squares(lambda p: residuals(free_curve(p[0], p[1], p[2], rake_deg, beta_deg), obs), [zs0, R0, L0], bounds=([9800.0, 50.0, 500.0], [10100.0, 1500.0, 4000.0]))
                    if best is None or r.cost < best.cost:
                        best = r
    rk = rake_deg if rake_deg is not None else float(best.x[3])
    res = residuals(free_curve(best.x[0], best.x[1], best.x[2], rk, beta_deg), obs)
    return best.x, res


def lantern_midline(lum, rgb, x0, z1, mm, arm_pts, boss_xz=(-1170.0, 11080.0)):
    """The lantern's silhouette against the sky, in the elevation picture, and how it lies about the arm's apparent line.
    The arm's line is fitted on `arm_pts` (x, z). Returns dict: angle of the arm line, angle of the silhouette's principal axis, the midline's offsets from the arm line
    (min, max, mm) over the silhouette's length along the line, the drift of the midline (degrees), the length along the line (mm)."""
    sky = float(np.median(lum[:30, -60:]))
    H, W = lum.shape
    xs = x0 + (np.arange(W) + 0.5) * mm
    zs = z1 - (np.arange(H) + 0.5) * mm
    X, Z = np.meshgrid(xs, zs)
    sat = rgb.max(-1) - rgb.min(-1)
    mask = (lum < sky - 45) | ((sat > 90) & (rgb[..., 0] > 150))
    mask &= (X < boss_xz[0] + 30) & (Z > boss_xz[1] - 150) & (X > x0 + 60)
    a = np.array(arm_pts)
    m, b = np.polyfit(a[:, 0], a[:, 1], 1)
    ang = math.degrees(math.atan2(-m, -1.0)) if False else math.degrees(math.atan(abs(m)))
    # unit vector along the arm line, pointing up and to the left (out toward the lantern), and its normal
    u = np.array([-1.0, -m]) / math.hypot(1.0, m)
    n = np.array([-u[1], u[0]])
    P = np.stack([X[mask], Z[mask]], 1)
    if len(P) < 500:
        return None
    ref = np.array([boss_xz[0], m * boss_xz[0] + b])
    s = (P - ref) @ u
    t = (P - ref) @ n
    c = np.cov(np.stack([P[:, 0], P[:, 1]]))
    w, v = np.linalg.eigh(c)
    pa = v[:, np.argmax(w)]
    if pa[0] > 0:
        pa = -pa
    pang = math.degrees(math.atan2(pa[1], -pa[0]))
    mids = []
    for s0 in np.arange(80, s.max() - 80, 40):
        sel = (s > s0 - 20) & (s < s0 + 20)
        if sel.sum() > 30:
            lo, hi = np.percentile(t[sel], [3, 97])
            mids.append((s0, (lo + hi) / 2.0, hi - lo))
    mids = np.array(mids)
    drift = math.degrees(math.atan(np.polyfit(mids[:, 0], mids[:, 1], 1)[0])) if len(mids) > 3 else None
    return {"arm_line_deg": round(ang, 1), "silhouette_principal_axis_deg": round(pang, 1), "midline_offset_mm": [round(float(mids[:, 1].min()), 1), round(float(mids[:, 1].max()), 1)],
            "drift_deg": round(float(drift), 2) if drift is not None else None, "silhouette_length_along_arm_line_mm": round(float(s.max()), 0), "width_mm": [round(float(mids[:, 2].min())), round(float(mids[:, 2].max()))],
            "pixels": int(mask.sum())}
