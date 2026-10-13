"""Shared by make_target.py, target_drawing.py and self_check.py (cloud week 42, unit 8): the game's projection rule for a house window's
room, the cards, the review cameras and the stand-off budgets for the smaller window rooms.

Derived from files the game already has (tools/ue/make_interior_material.py `trace`; production/specs/vignette-scene.json;
tools/art-recipes/terrace-front.py), never typed twice. Units: metres unless a name ends in _mm.

Frames
  street   x along the street (0 at the quay end, +x north), y across (east side +y, west side -y), z up from the road crown
  picture  X to the PICTURE's right from the card's picture-left edge, Y back from the card plane INTO the room (negative in front of
           it), Z up from the card bottom (the room's floor). An east card's picture runs right-to-left along street x; a west card's
           left-to-right (make_interior_material.py: Unreal is left-handed). The card's centre is the picture's centre.
  The glass plane is in front of the card by CARD_Y_BACK_OF_FRONTAGE - glass depth; the box is the room behind the card.
"""
import importlib.util
import json
import math
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MIM = _load(os.path.join(ROOT, "tools", "ue", "make_interior_material.py"), "make_interior_material_hw")
trace = MIM.trace           # the game's rule in Python: picture (u, v down) for a card point p seen from c (card frame, east card)
project = MIM.project       # the render's rule: room point to picture (u, v up)

# ---- the street's fixed numbers -----------------------------------------------------------------------------------------------
FRONTAGE_Y = 5.125                # terrace-front.py STREET_FRONTAGE_M
FOOTWAY_ABOVE_CROWN = 0.10        # THRESHOLD_ABOVE_CROWN_M
EYE_ABOVE_FOOTWAY = 1.60
EYE_Z = EYE_ABOVE_FOOTWAY + FOOTWAY_ABOVE_CROWN        # 1.70 above the crown
PAVEMENT_FAR_Y = 3.505            # the far pavement's kerb edge (unit 7)
WALL_T = 0.215                    # one brick
CARD_Y_BACK = 0.270               # the card plane stands this far behind the frontage line (9 cm... see TARGET section 7)
GLASS_UPPER_DEPTH = 0.142         # the checked sash: upper glass 142 mm behind the brick face (1a)
GLASS_LOWER_DEPTH = 0.190         # lower glass 190 mm
GLASS_MID_DEPTH = 0.166           # used for the sight-through computation
WIN_W = 0.85                      # the opening
WIN_H_PERIOD = 1.6764             # 5 ft 6 in (ruling 8 October)

ROOMS = {
    "UP": {"w": 2.8, "h": 2.55, "d": 4.2, "camd": 2.8, "floor_z": 3.75, "pic_w": 1536},
    "GF": {"w": 3.4, "h": 2.60, "d": 4.2, "camd": 3.4, "floor_z": 0.45, "pic_w": 3072},
}


def aspect(room):
    return room["h"] / room["w"]


def back_wall_rect_uv(room):
    """The back wall's rectangle in the picture by the render rule: u, v (v up) from-to."""
    f = room["camd"] / (room["camd"] + room["d"])
    return (0.5 - 0.5 * f, 0.5 + 0.5 * f)


def back_wall_px(room, width_px):
    lo, hi = back_wall_rect_uv(room)
    hpx = width_px * aspect(room)
    return (round(lo * width_px, 1), round(lo * hpx, 1), round(hi * width_px, 1), round(hi * hpx, 1))


# ---- eyes ---------------------------------------------------------------------------------------------------------------------
def eye_street(cam, side, xc):
    """The review camera's eye in the street frame for a window at street x = xc on `side` (+1 east, -1 west).
    cam = (kind, a, b): 'across' (distance to the glass plane is derived, off-axis degrees a); 'along' (perpendicular distance from the wall b,
    angle from the wall a); 'under' (perpendicular distance b, directly below)."""
    kind, a, b = cam
    if kind == "across":
        y = -side * PAVEMENT_FAR_Y
        dist = abs(side * FRONTAGE_Y - y) + GLASS_MID_DEPTH
        lat = dist * math.tan(math.radians(a))
        return np.array([xc - lat, y, EYE_Z])
    if kind == "along":
        y = side * (FRONTAGE_Y - b)
        along = b / math.tan(math.radians(a))
        return np.array([xc - along, y, EYE_Z])
    if kind == "under":
        y = side * (FRONTAGE_Y - b)
        return np.array([xc, y, EYE_Z])
    raise ValueError(kind)


CAMERAS = {
    "H_ACROSS_0": {"what": "from the far pavement's kerb edge, square on to the window", "spec": ("across", 0.0, None), "vfov_deg": 39.0},
    "H_ACROSS_30": {"what": "from the far pavement's kerb edge, 30 degrees off the window's normal toward the quay end", "spec": ("across", 30.0, None), "vfov_deg": 39.0},
    "H_ALONG_15_NEAR": {"what": "on the house's own footway 1.5 m from the wall, the window seen 15 degrees from the wall (5.6 m along)", "spec": ("along", 15.0, 1.5), "vfov_deg": 46.0},
    "H_ALONG_30_NEAR": {"what": "on the house's own footway 1.5 m from the wall, the window seen 30 degrees from the wall (2.6 m along)", "spec": ("along", 30.0, 1.5), "vfov_deg": 46.0},
    "H_ALONG_15_ROAD": {"what": "in the road, 1 m out from the kerb (2.6 m from the wall: the footway is 5.125 - 3.505 = 1.62 m wide), the window seen 15 degrees from the wall (9.7 m along)", "spec": ("along", 15.0, 2.6), "vfov_deg": 39.0},
    "H_UNDER": {"what": "0.8 m from the wall, directly below the window (looking up)", "spec": ("under", None, 0.8), "vfov_deg": 60.0},
}
STAND_OFF_CAMERAS = ["H_ACROSS_0", "H_ACROSS_30", "H_ALONG_15_NEAR", "H_ALONG_30_NEAR", "H_ALONG_15_ROAD", "H_UNDER"]


def eye_in_picture(eye, side, card_cx, room):
    """The eye in the PICTURE frame. xr: east card -> toward low street x is the picture's right; west card -> toward high x."""
    xr = (card_cx - eye[0]) if side > 0 else (eye[0] - card_cx)
    # distance from the card plane: the card is CARD_Y_BACK behind the frontage line; the eye's distance from the frontage line along -side
    d_front = side * FRONTAGE_Y - side * eye[1]       # positive: eye in front of the wall, toward the street
    y = -(d_front + CARD_Y_BACK)
    return np.array([room["w"] / 2.0 + xr, y, eye[2] - room["floor_z"]])


def window_in_picture(room, win_off_x, sill_above_floor, head_above_floor):
    """The glass rectangle in the picture frame: x0, x1 (to the picture's right), z0, z1 above the floor; win_off_x = the window centre's offset from the
    card centre toward the PICTURE's right."""
    cx = room["w"] / 2.0 + win_off_x
    return (cx - WIN_W / 2.0, cx + WIN_W / 2.0, sill_above_floor, head_above_floor)


# ---- the box and the rays -----------------------------------------------------------------------------------------------------
def hit_box(origin, dirs, room):
    """First surface a ray from `origin` (n,3 dirs) meets inside the box x 0..W, y 0..D, z 0..H (picture frame). Returns point, surface id
    (0 back, 1 left, 2 right, 3 floor, 4 ceiling) and the parameter t."""
    W, D, H = room["w"], room["d"], room["h"]
    d = np.asarray(dirs, float)
    o = np.broadcast_to(np.asarray(origin, float), d.shape)
    big = 1e12
    with np.errstate(divide="ignore", invalid="ignore"):
        tb = np.where(d[:, 1] > 1e-12, (D - o[:, 1]) / d[:, 1], big)
        tl = np.where(d[:, 0] < -1e-12, (0 - o[:, 0]) / d[:, 0], big)
        tr = np.where(d[:, 0] > 1e-12, (W - o[:, 0]) / d[:, 0], big)
        tf = np.where(d[:, 2] < -1e-12, (0 - o[:, 2]) / d[:, 2], big)
        tc = np.where(d[:, 2] > 1e-12, (H - o[:, 2]) / d[:, 2], big)
    ts = np.stack([tb, tl, tr, tf, tc], axis=1)
    sid = ts.argmin(axis=1)
    t = ts.min(axis=1)
    return o + d * t[:, None], sid, t


NORMALS = np.array([[0, -1, 0], [1, 0, 0], [-1, 0, 0], [0, 0, 1], [0, 0, -1]], float)   # pointing INTO the room from each surface


def slide_deg_vec(eye, obj, hitpts, sid, room):
    """The angle (degrees, at the eye) between the eye's ray to an object `obj` (n,3) standing in front of the surface and to the place
    where the render camera painted it (the point R0 on the surface plane along the render camera's ray through the object)."""
    C0 = np.array([room["w"] / 2.0, -room["camd"], room["h"] / 2.0])
    planes = [(1, room["d"]), (0, 0.0), (0, room["w"]), (2, 0.0), (2, room["h"])]
    out = np.zeros(len(obj))
    for k, (ax, val) in enumerate(planes):
        m = sid == k
        if not m.any():
            continue
        O = obj[m]
        t = (val - C0[ax]) / (O[:, ax] - C0[ax])
        R0 = C0 + (O - C0) * t[:, None]
        a = O - eye
        b = R0 - eye
        cos = (a * b).sum(1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1))
        out[m] = np.degrees(np.arccos(np.clip(cos, -1, 1)))
    return out


def pixel_angle_deg(vfov_deg, res_h=1440):
    """The angle one pixel subtends at the centre of the frame for a pinhole camera of vertical field vfov_deg over res_h lines: atan(tan(vfov / 2) / (res_h / 2)).
    (The first version of this file used vfov / res_h, which is 4 per cent small at 39 degrees and 10 per cent small at 60: the review's 'exact pixel angles'.)"""
    return math.degrees(math.atan(math.tan(math.radians(vfov_deg / 2.0)) / (res_h / 2.0)))


def max_standoff(eye, hitpts, sid, room, px_limit, vfov_deg, res_h=1440):
    """For each hit point the greatest stand-off (m) at which an object painted on its surface slides at most px_limit pixels."""
    lim = px_limit * pixel_angle_deg(vfov_deg, res_h)
    lo = np.zeros(len(hitpts))
    hi = np.full(len(hitpts), 3.0)
    nrm = NORMALS[sid]
    for _ in range(36):
        mid = (lo + hi) / 2.0
        obj = hitpts + nrm * mid[:, None]
        s = slide_deg_vec(eye, obj, hitpts, sid, room)
        ok = s <= lim
        lo = np.where(ok, mid, lo)
        hi = np.where(ok, hi, mid)
    return lo


def sample_glass(rect, depth_from_card, n=(9, 16)):
    """Sample points on the glass rectangle (picture frame) at its plane: y = -depth_from_card."""
    x0, x1, z0, z1 = rect
    xs = np.linspace(x0 + 0.05, x1 - 0.05, n[0])
    zs = np.linspace(z0 + 0.05, z1 - 0.05, n[1])
    X, Z = np.meshgrid(xs, zs)
    return np.stack([X.ravel(), np.full(X.size, -depth_from_card), Z.ravel()], axis=1)


def see_through(eye, rect, room, depth_from_card=None):
    """Rays from `eye` through the glass rectangle into the room: returns hit points, surface ids, the glass points. Rays that miss the glass
    (the eye behind it) or that leave the box through the card plane are dropped."""
    depth = (CARD_Y_BACK - GLASS_MID_DEPTH) if depth_from_card is None else depth_from_card
    G = sample_glass(rect, depth)
    d = G - eye
    d = d / np.linalg.norm(d, axis=1)[:, None]
    # the ray enters the box at the card plane (y = 0)
    t0 = (0.0 - eye[1]) / d[:, 1]
    P = eye + d * t0[:, None]
    ok = (d[:, 1] > 1e-6) & (P[:, 0] > 0) & (P[:, 0] < room["w"]) & (P[:, 2] > 0) & (P[:, 2] < room["h"])
    G, d, P = G[ok], d[ok], P[ok]
    hp, sid, t = hit_box(P, d, room)
    return hp, sid, G, P


def budgets_for(room_key, sill_above_floor, head_above_floor, win_off_x, sides=(+1,), card_cx=0.0, px=(20, 40)):
    """The stand-off table for one room and window, over the review cameras and both mirror images of the pavement position: for each surface
    class the 15th percentile, over the points the window shows, of the greatest stand-off, then the smallest over the cameras.
    The EYE STANDS BY THE WINDOW, as the camera table says (TARGET-REVIEW narrow point 1): the cameras are placed relative to the window's own street x
    (xc = card_cx - win_off_x for an east card), not the card's centre; the mirror image is taken about the window, not about the room's middle. For a cottage
    (window 0.9 m off the card's centre) the first version put every eye 0.9 m from its window and so over-stated the back wall's budget (0.41 against 0.38)."""
    room = ROOMS[room_key]
    rect = window_in_picture(room, win_off_x, sill_above_floor, head_above_floor)
    classes = {"back": [0], "side": [1, 2], "floor": [3], "ceiling": [4]}
    acc = {c: {p: [] for p in px} for c in classes}
    per_cam = {}
    for cam in STAND_OFF_CAMERAS:
        spec = CAMERAS[cam]["spec"]
        for mirror in (+1, -1):
            xc = card_cx - win_off_x                       # the window's street x (east card: the picture's right is toward low x)
            e_st = eye_street(spec, 1, xc)
            e_pic = eye_in_picture(e_st, 1, card_cx, room)
            if mirror < 0:
                cxw = room["w"] / 2.0 + win_off_x           # the window's centre in the picture: the mirror is about the window
                e_pic = np.array([2.0 * cxw - e_pic[0], e_pic[1], e_pic[2]])
            hp, sid, G, P = see_through(e_pic, rect, room)
            if len(hp) < 8:
                continue
            for p in px:
                m = max_standoff(e_pic, hp, sid, room, p, CAMERAS[cam]["vfov_deg"])
                for c, ids in classes.items():
                    sel = np.isin(sid, ids)
                    if sel.sum() >= 4:
                        v = float(np.percentile(m[sel], 15))
                        acc[c][p].append(v)
                        per_cam.setdefault(cam, {}).setdefault(c, {}).setdefault(str(p), []).append(round(v, 3))
    out = {}
    for c in classes:
        out[c] = {("true_%dpx" % p): (round(min(acc[c][p]), 3) if acc[c][p] else None) for p in px}
    return out, per_cam
