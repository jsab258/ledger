"""Shared by make_target.py, target_drawing.py and self_check.py: the game's projection rule, the cards, the review cameras and the
stand-off numbers that say what a projected room can honestly hold.

Everything here is derived from files the game already has (tools/ue/make_interior_material.py `trace`, production/specs/
vignette-scene.json, tools/art-recipes/terrace-front.py's card), never typed twice. Units: metres unless a name ends in _mm.

Frames
  street     x along the street (0 at the south/quay end, +x north), y across (east side +y, west side -y), z up from the road crown
  card       the game's CardOrigin frame (what `trace` takes): x from the card's low-x edge, y back from the card INTO the room
             for an east card (and the same world direction y for a west card, where the room is toward -y), z up from the card bottom
  room       the shop-room.py frame: x across with 0 at the card's centre, +x the PICTURE's right, y back from the card, z up from the box floor
"""
import importlib.util
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MIM = _load(os.path.join(ROOT, "tools", "ue", "make_interior_material.py"), "make_interior_material")
trace = MIM.trace            # the game's rule in Python: picture (u, v down) for a card point p seen from c (card frame)
project = MIM.project        # the render's rule: room point to picture (u, v up)

# ---- the street's fixed numbers (SCENE-SLOTS.md, terrace-front.py 2385-2417, vignette-scene.json) -----------------------------
FRONTAGE_Y = 5.125           # terrace-front.py STREET_FRONTAGE_M
CARD_BACK_OF_FRONTAGE = 0.75  # the card's front face stands 0.75 m behind the frontage line (y0 = frontage + 0.75, thickness 0.04)
CARD_Y = FRONTAGE_Y + CARD_BACK_OF_FRONTAGE            # 5.875
GLASS_Y_FRONT, GLASS_Y_BACK = 5.245, 5.265            # the street model's bay glass (shop-interiors.json: "panes at 5.245 to 5.265 m back")
GLASS_Y_MID = 5.255
FOOTWAY_ABOVE_CROWN = 0.10   # THRESHOLD_ABOVE_CROWN_M
CARD_BOTTOM, CARD_TOP = 0.65, 3.05                      # above the crown: threshold + 0.55 and + 2.95
BED_Z = 0.70                 # the stallriser's top (0.60 above the footway) = the display bed
CARD_INSET = 0.35            # the card runs from bay start + 0.35 to bay end - 0.35
BAY_W = 6.0
W, H = BAY_W - 2 * CARD_INSET, CARD_TOP - CARD_BOTTOM   # 5.3 x 2.4
CAMERA_D = W                 # the render camera stands one room-width in front of the card (spec: camera_d 5.3)
EYE_ABOVE_FOOTWAY = 1.60
EYE_Z = EYE_ABOVE_FOOTWAY + FOOTWAY_ABOVE_CROWN         # 1.70 above the crown
PAVEMENT_FAR_Y = 3.505       # the far pavement's kerb edge (3.0 carriageway + 0.255 channel + 0.125 kerb + 0.125 inside it)
GLASS_TO_CARD = CARD_Y - GLASS_Y_BACK                    # 0.61 (display: front 5.27, 0.55 deep, ends 5.82)
DISPLAY_DEPTH = 0.55
DISPLAY_FRONT_FROM_GLASS = 5.27 - GLASS_Y_BACK           # 0.005


def load_scene():
    return json.load(open(os.path.join(ROOT, "production", "specs", "vignette-scene.json")))


def block(scene, bid):
    return next(b for b in scene["blocks"] if b["id"] == bid)


def bay_x0(scene, bid, bay):
    """The bay's low-x end, as terrace-front.py places it (a west block's bays run from its HIGH x end)."""
    b = block(scene, bid)
    run = b["bays"] * b["bay_width_m"]
    if b["side"] == "east":
        return b["start_x_m"] + bay * b["bay_width_m"]
    return b["start_x_m"] + run - (bay + 1) * b["bay_width_m"]


def card_of(scene, bid, bay):
    """The interior card for a bay, as terrace-front.py 2405-2417 makes it."""
    b = block(scene, bid)
    bx = bay_x0(scene, bid, bay)
    side = 1 if b["side"] == "east" else -1
    return {"x0": round(bx + CARD_INSET, 3), "x1": round(bx + b["bay_width_m"] - CARD_INSET, 3), "bottom": CARD_BOTTOM, "top": CARD_TOP,
            "z": side * CARD_Y, "side": side, "bay_x0": bx}


def card_origin(card):
    """CardOrigin (the card's front corner: low x, front y, bottom z) in world metres."""
    return np.array([card["x0"], card["z"], card["bottom"]])


def to_card(p_world, card):
    return np.asarray(p_world, float) - card_origin(card)


# ---- the rule, vectorised ----------------------------------------------------------------------------------------------------
def trace_vec(P, C, size, camd, side=1):
    """`trace` for arrays: P (n, 3) card points, C (3,) the eye, both in the card frame; returns picture u, v (v down) and the hit."""
    Wm, Hm, Dm = size
    P = np.asarray(P, float)
    dirv = P - np.asarray(C, float)
    dirv = dirv / np.linalg.norm(dirv, axis=1)[:, None]
    ox = (Wm - P[:, 0]) if side > 0 else P[:, 0]
    o = np.stack([ox, P[:, 2], P[:, 1] * side], axis=1)
    v = np.stack([-dirv[:, 0] * side, dirv[:, 2], dirv[:, 1] * side], axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        tx = np.where(v[:, 0] > 0, (Wm - o[:, 0]) / v[:, 0], (0 - o[:, 0]) / np.minimum(v[:, 0], -1e-5))
        ty = np.where(v[:, 1] > 0, (Hm - o[:, 1]) / v[:, 1], (0 - o[:, 1]) / np.minimum(v[:, 1], -1e-5))
        tz = (Dm - o[:, 2]) / np.maximum(v[:, 2], 1e-5)
    t = np.maximum(0, np.minimum(np.minimum(tx, ty), tz))
    h = o + v * t[:, None]
    s = camd / (camd + np.maximum(h[:, 2], 0))
    u = 0.5 + (h[:, 0] / Wm - 0.5) * s
    w = 0.5 + (h[:, 1] / Hm - 0.5) * s
    return u, 1 - w, h


# ---- room frame <-> card frame (east card, side +1: the picture's right is the card's LOW x) -------------------------------------
def room_to_card(x, y, z, w=W):
    """A room point (x across, 0 at the centre, +x the picture's right; y back; z up from the box floor) to the card frame of an EAST card."""
    return np.array([w / 2.0 - x, y, z])


def card_to_room(p, w=W):
    return np.array([w / 2.0 - p[0], p[1], p[2]])


# ---- the review cameras (street frame), named exactly -----------------------------------------------------------------------
CAMERAS = {
    "STREET_SQUARE": {"what": "from the far pavement, square on to the window's centre", "distance_to_glass_m": round(PAVEMENT_FAR_Y + GLASS_Y_MID, 3),
                      "off_axis_deg": 0.0, "vfov_deg": 39.0, "aim_z_above_crown": 1.60, "resolution": [2560, 1440]},
    "STREET_30": {"what": "from the far pavement, 30 degrees off the window's normal, toward the quay end (low street x)",
                  "distance_to_glass_m": round(PAVEMENT_FAR_Y + GLASS_Y_MID, 3), "off_axis_deg": 30.0, "vfov_deg": 39.0, "aim_z_above_crown": 1.60,
                  "resolution": [2560, 1440]},
    "CLOSE_35": {"what": "from the near pavement, 1.5 m from the glass, 35 degrees off its normal toward the quay end; aimed at the display's middle",
                 "distance_to_glass_m": 1.5, "off_axis_deg": 35.0, "vfov_deg": 60.0, "aim_z_above_crown": 1.45, "resolution": [2560, 1440]},
    "CLOSE_35_B": {"what": "CLOSE_35 moved 2.0 m along the street toward the high end: the second eye of the parallax test (same aim point)",
                   "distance_to_glass_m": 1.5, "off_axis_deg": 35.0, "vfov_deg": 60.0, "aim_z_above_crown": 1.45, "resolution": [2560, 1440],
                   "shift_along_street_m": 2.0},
}


def camera_pose(cam_name, card, window_centre_x):
    """(eye, aim) in the street frame for a camera and a shop: the eye is on the OPPOSITE side of the road for the street views and on
    the shop's own pavement for the close views; its lateral offset is toward low street x."""
    c = CAMERAS[cam_name]
    side = card["side"]
    dist = c["distance_to_glass_m"]
    lateral = dist * math.tan(math.radians(c["off_axis_deg"]))
    if cam_name.startswith("STREET"):
        eye_y = -side * PAVEMENT_FAR_Y
    else:
        eye_y = side * (GLASS_Y_MID - dist)
    eye = np.array([window_centre_x - lateral + c.get("shift_along_street_m", 0.0), eye_y, EYE_Z])
    aim_y = side * (GLASS_Y_MID if cam_name.startswith("STREET") else (GLASS_Y_BACK + 0.25))
    aim = np.array([window_centre_x, aim_y, c["aim_z_above_crown"]])
    return eye, aim


def eye_in_picture(eye_street, card):
    """The eye in the PICTURE frame (X to the picture's right from the card's left edge, Y back from the card plane (negative in front of it),
    Z up from the card bottom). An east card's picture runs right-to-left along street x (the viewer faces +y: his right is -x); a west card's
    runs left-to-right. The card's centre is the picture's centre."""
    side = card["side"]
    cx = (card["x0"] + card["x1"]) / 2.0
    xr = (cx - eye_street[0]) if side > 0 else (eye_street[0] - cx)
    y = -(CARD_Y - side * eye_street[1])
    return np.array([W / 2.0 + xr, y, eye_street[2] - CARD_BOTTOM])


# ---- how far a thing may stand off the surface it is painted on ---------------------------------------------------------------
def slide_deg(eye_card, obj_room, plane, D, w=W, h=H, camd=CAMERA_D):
    """How far (degrees, as the EYE sees it) an object drawn into the picture appears to slide off its true place.

    The picture is taken from the render camera C0 = (W/2, -camd, H/2) in the card frame of an east card. An object at O stands s in front of
    the surface plane; the picture paints it on the surface at the point R0 where C0's ray through O meets the plane; the eye at C1 sees it
    there instead of at O. plane = ('back', D) | ('left', 0) | ('right', W) | ('floor', 0), in the card frame."""
    C0 = np.array([w / 2.0, -camd, h / 2.0])
    O = np.asarray(obj_room, float)
    ax, val = {"back": (1, D), "left": (0, 0.0), "right": (0, w), "floor": (2, 0.0)}[plane[0]] if isinstance(plane, tuple) else (None, None)
    if plane[0] == "back":
        ax, val = 1, D
    t = (val - C0[ax]) / (O[ax] - C0[ax])
    R0 = C0 + (O - C0) * t
    C1 = np.asarray(eye_card, float)
    a = O - C1
    b = R0 - C1
    cosang = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    return math.degrees(math.acos(max(-1.0, min(1.0, cosang))))


def stand_off_budget(D, tol_deg, family=None, nx=60, nz=30):
    """The largest stand-off (m) at which an object painted on a surface appears to slide by at most tol_deg, for the pavement positions of
    `family` (distance from the glass, lateral offset from the card's centre): the 25th percentile over what a player sees there.
    Returns {surface: metres} for back wall, side walls (near, middle, far third of the depth), floor and ceiling."""
    if family is None:
        family = [(g, lat) for g in (1.0, 1.5, 1.9) for lat in (-3.0, -1.5, 0.0, 1.5, 3.0)]
    xs = np.linspace(0.05, W - 0.05, nx)
    zs = np.linspace(0.08, H - 0.05, nz)
    X, Z = np.meshgrid(xs, zs)
    P = np.stack([X.ravel(), np.zeros(X.size), Z.ravel()], axis=1)
    C0 = np.array([W / 2.0, -CAMERA_D, H / 2.0])
    bucket = {"back": [], "side_near": [], "side_mid": [], "side_far": [], "floor": [], "ceiling": []}

    def hit(Pm, C):
        dirv = Pm - C
        dirv = dirv / np.linalg.norm(dirv, axis=1)[:, None]
        big = 1e9
        with np.errstate(divide="ignore", invalid="ignore"):
            tx = np.where(dirv[:, 0] > 1e-9, (W - Pm[:, 0]) / dirv[:, 0], np.where(dirv[:, 0] < -1e-9, (0 - Pm[:, 0]) / dirv[:, 0], big))
            tz = np.where(dirv[:, 2] > 1e-9, (H - Pm[:, 2]) / dirv[:, 2], np.where(dirv[:, 2] < -1e-9, (0 - Pm[:, 2]) / dirv[:, 2], big))
            ty = (D - Pm[:, 1]) / np.maximum(dirv[:, 1], 1e-9)
        t = np.minimum(np.minimum(tx, tz), ty)
        surf = np.where(ty <= np.minimum(tx, tz) + 1e-9, 0, np.where(tx <= tz, 1, 2))
        return Pm + dirv * t[:, None], dirv, t + np.linalg.norm(Pm - C, axis=1), surf

    def tans(dirv, surf):
        out = np.zeros((len(dirv), 2))
        eps = 1e-9
        m = surf == 0
        out[m] = np.stack([dirv[m, 0] / dirv[m, 1], dirv[m, 2] / dirv[m, 1]], axis=1)
        m = surf == 1
        dx = np.where(np.abs(dirv[m, 0]) < eps, eps, dirv[m, 0])
        out[m] = np.stack([dirv[m, 1] / dx, dirv[m, 2] / dx], axis=1)
        m = surf == 2
        dz = np.where(np.abs(dirv[m, 2]) < eps, eps, dirv[m, 2])
        out[m] = np.stack([dirv[m, 0] / dz, dirv[m, 1] / dz], axis=1)
        return out

    for g, lat in family:
        C1 = np.array([W / 2.0 + lat, -(g + GLASS_TO_CARD), EYE_Z - CARD_BOTTOM])
        h1, d1, L1, s1 = hit(P, C1)
        h0, d0, L0, s0 = hit(P, C0)
        t1 = tans(d1, s1)
        # the render ray's tangent on the SAME surface plane the eye's ray lands on
        d0b = h1 - C0
        d0b = d0b / np.linalg.norm(d0b, axis=1)[:, None]
        t0 = tans(d0b, s1)
        disp = np.linalg.norm(t1 - t0, axis=1)
        k = L1 / np.maximum(disp, 1e-6)
        m = s1 == 0
        bucket["back"].append(k[m])
        m = s1 == 1
        y = h1[m, 1]
        for name, lo, hi in (("side_near", 0, D / 3), ("side_mid", D / 3, 2 * D / 3), ("side_far", 2 * D / 3, D + 1)):
            mm = (y >= lo) & (y < hi)
            bucket[name].append(k[m][mm])
        m = s1 == 2
        zhit = h1[m, 2]
        bucket["floor"].append(k[m][zhit < H / 2])
        bucket["ceiling"].append(k[m][zhit >= H / 2])
    tol = math.radians(tol_deg)
    return {k: round(float(np.percentile(np.concatenate(v), 25)) * tol, 4) if v and sum(len(x) for x in v) > 20 else None for k, v in bucket.items()}


def slide_px(eye_pic, obj_pic, plane, D, vfov_deg, res_h=1440):
    """slide_deg in pixels of a res_h-high frame with the given vertical field of view."""
    return slide_deg(eye_pic, obj_pic, plane, D) / (vfov_deg / float(res_h))


def max_standoff(eye_pic, region, D, px_limit, vfov_deg):
    """The greatest stand-off (m) of an object painted on `region` that slides no more than px_limit pixels from this eye.
    region: ('back', x) | ('left', y) | ('right', y) | ('floor', x, y)  (a sample place on that surface)."""
    kind = region[0]
    lo, hi = 0.0, 3.0
    for _ in range(40):
        mid = (lo + hi) / 2.0
        if kind == "back":
            obj, plane = (region[1], D - mid, 1.2), ("back", D)
        elif kind == "left":
            obj, plane = (mid, region[1], 1.2), ("left", 0.0)
        elif kind == "right":
            obj, plane = (W - mid, region[1], 1.2), ("right", W)
        else:
            obj, plane = (region[1], region[2], mid), ("floor", 0.0)
        if slide_px(eye_pic, obj, plane, D, vfov_deg) <= px_limit:
            lo = mid
        else:
            hi = mid
    return lo


def standoff_table(D, px_limit, scene=None, bid="east_parade", bay=2):
    """What a picture honestly holds: for each review camera the greatest stand-off at which a painted object slides at most px_limit pixels
    (2560 x 1440), at a spread of places; the budget is the smallest over the three cameras (STREET_SQUARE, STREET_30, CLOSE_35)."""
    scene = scene or load_scene()
    card = card_of(scene, bid, bay)
    cx = (card["x0"] + card["x1"]) / 2.0
    places = {"back wall, left third": ("back", 1.0), "back wall, middle": ("back", W / 2), "back wall, right third": ("back", W - 1.0),
              "left wall, near third": ("left", D / 6), "left wall, middle third": ("left", D / 2), "left wall, far third": ("left", 5 * D / 6),
              "right wall, near third": ("right", D / 6), "right wall, middle third": ("right", D / 2), "right wall, far third": ("right", 5 * D / 6),
              "floor, near": ("floor", W / 2, 1.0), "floor, middle": ("floor", W / 2, D / 2), "floor, far": ("floor", W / 2, D - 0.8)}
    out = {}
    for name, region in places.items():
        per = {}
        for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35"):
            for sgn in (+1, -1):
                # both mirror images of the pavement position (the picture's right or left of the card)
                eye, _ = camera_pose(cam, card, cx)
                ep = eye_in_picture(eye, card)
                ep = np.array([W - ep[0] if sgn < 0 else ep[0], ep[1], ep[2]])
                per["%s%s" % (cam, "" if sgn > 0 else "_mirrored")] = round(max_standoff(ep, region, D, px_limit, CAMERAS[cam]["vfov_deg"]), 4)
        out[name] = {"by_camera": per, "budget_m": round(min(per.values()), 3)}
    return out


def texel_stats(distance_to_glass, angle_deg, pic_w_px, D, vfov_deg=60.0, res=(1600, 900), game_h=1440):
    """Screen pixels per picture texel over the glass area (>1 is magnification: soft), for a pavement eye at `distance_to_glass` from the
    glass and `angle_deg` off the window's normal. Measured on a res-sized frame and scaled to a game_h-high frame (the angle per pixel scales).
    Returns the median and 95th percentile and the fraction of the glass area softer than 2 pixels a texel."""
    lat = distance_to_glass * math.tan(math.radians(angle_deg))
    eye = np.array([W / 2.0 + lat, -(distance_to_glass + GLASS_TO_CARD), EYE_Z - CARD_BOTTOM])
    aim = np.array([W / 2.0, 0.0, 1.30 - 0.65 + 0.2])
    f = aim - eye
    f /= np.linalg.norm(f)
    right = np.cross(f, np.array([0, 0, 1.0]))
    right /= np.linalg.norm(right)
    up = np.cross(right, f)
    w, h = res
    tv = math.tan(math.radians(vfov_deg / 2))
    th = tv * w / h
    xs = (np.arange(w) + 0.5) / w * 2 - 1
    ys = 1 - (np.arange(h) + 0.5) / h * 2
    X, Y = np.meshgrid(xs, ys)
    dirs = (f[None, None, :] + X[..., None] * th * right[None, None, :] + Y[..., None] * tv * up[None, None, :]).reshape(-1, 3)
    t = -eye[1] / dirs[:, 1]
    P = eye + dirs * t[:, None]
    ok = (dirs[:, 1] > 0) & (P[:, 0] > 0) & (P[:, 0] < W) & (P[:, 2] > 0.05) & (P[:, 2] < H)
    idx = np.where(ok)[0]
    if idx.size < 200:
        return None
    # the picture here is in the PICTURE frame; trace_vec wants the card frame of an east card, whose x runs the other way
    def uv(ix):
        tj = -eye[1] / dirs[ix, 1]
        Pj = eye + dirs[ix] * tj[:, None]
        Pc = Pj.copy()
        Pc[:, 0] = W - Pc[:, 0]
        ec = eye.copy()
        ec[0] = W - ec[0]
        u, v, _ = trace_vec(Pc, ec, (W, H, D), CAMERA_D)
        return u, v
    u0, v0 = uv(idx)
    ux, vx = uv(np.clip(idx + 1, 0, dirs.shape[0] - 1))
    uy, vy = uv(np.clip(idx + w, 0, dirs.shape[0] - 1))
    aspect = H / W
    tpp = np.maximum(np.hypot((ux - u0) * pic_w_px, (vx - v0) * pic_w_px * aspect), np.hypot((uy - u0) * pic_w_px, (vy - v0) * pic_w_px * aspect))
    ppt = 1.0 / np.maximum(tpp, 1e-6) * (game_h / float(res[1]))
    return {"median": round(float(np.median(ppt)), 2), "p95": round(float(np.percentile(ppt, 95)), 2), "soft_fraction_over_2": round(float((ppt > 2).mean()), 3),
            "glass_fraction_of_frame": round(idx.size / float(dirs.shape[0]), 3)}
