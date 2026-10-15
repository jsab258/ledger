"""Draw the front door's target from target.json alone.

    python target_drawing.py OUT_DIR [--variant flat_door_over_shop] [--overlay PHOTO.jpg OVERLAY.jpg]

Writes OUT_DIR/target_drawings.json (filled polygons in millimetres; the builder's automatic check reads
it) and pictures (PNG) into OUT_DIR. Nothing else is read: the numbers are target.json's.

Drawings (every one in the frame of target.json: x across from the left brick reveal, y into the wall with the
outside at -y, z up from the top of the threshold):
  elevation            the outside view: x across, z up (layers: brick, buff, stone, frame, glass, leaf,
                       panel, moulding, iron; the check compares frame, glass, leaf, panel, moulding)
  section_h            plan cut through the lower panels
  section_h_lock       plan cut through the lock-rail band, the cylinder lock and the keep
  section_h_plate      plan cut through the letter plate (upper panels)
  section_h_transom    plan cut through the transom's face (shows how it overlaps the jambs)
  section_v            elevation-side cut on the centre line of the left-hand panels
  section_v_muntin     cut on the muntin's centre line (the letter plate, the numerals, the knob on F1)
  section_v_plinth     cut through the left plinth at x -60 (T1): the projecting base, its 45 degree splay, the wall above
  plan                 the step, the plinth, the threshold and the wall seen from above (the tread's outline steps back beside the plinth)
  profiles             every profile as a closed polygon in its own frame (bolection, band, weatherboard,
                       transom front, jamb, glazing bead, threshold and step, plate, knob)
  furniture            the ironmongery in front view in its own frame
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "target.json"


# ---------------------------------------------------------------- loading
def load(path=None):
    return json.loads(Path(path or TARGET).read_text(encoding="utf-8"))


def parts(T, variant=None):
    """The blocks of one variant: the top level is the default (terrace_four_panel)."""
    if variant in (None, T.get("default_variant")):
        return T
    return T["variants"][variant]["parts"]


class C:
    """Derived constants of one variant (all from the blocks)."""
    pass


def consts(P):
    c = C()
    L, F, O, S, B = P["leaf"], P["frame"], P["opening"], P["step"], P["brick"]
    c.W, c.H, c.TH = L["width_mm"], L["height_mm"], L["thickness_mm"]
    c.X0, c.Z0, c.LY0 = L["x0_mm"], L["z0_mm"], L["outside_face_y_mm"]
    c.LY1 = c.LY0 + c.TH
    c.OW, c.CROWN, c.SPRING = O["width_mm"], O["crown_height_mm"], O["springing_height_mm"]
    c.REV, c.WALL = O["reveal_depth_mm"], O["wall_thickness_mm"]
    c.SHOW = F["jamb_showing_past_brick_mm"]
    c.JF, c.JD = F["jamb_face_mm"], F["jamb_depth_mm"]
    c.REB_W = F["rebate_width_mm"]
    c.FY0, c.FY1 = F["frame_outside_face_y_mm"], F["frame_inside_face_y_mm"]
    c.STOP_Y = c.FY0 + F["stop_depth_mm"]
    tr, gl, hd = F["transom"], F["glazing"], F["head_section_mm"]
    c.Z_STOP, c.Z_TR_TOP, c.Z_REB = tr["z_stop_underside"], tr["z_top"], tr["rebate_underside_z"]
    c.TR_X0, c.TR_X1 = tr["x_mm"]
    c.GZ0, c.GZ1 = gl["opening_z_mm"]
    c.GX0, c.GX1 = gl["opening_x_mm"]
    c.CGX0, c.CGX1 = gl["clear_glass_x_mm"]
    c.CGZ0, c.CGZ1 = gl["clear_glass_z_mm"]
    c.GLASS_Y, c.GLASS_T, c.GLASS_RB = gl["glass_y_mm"], gl["glass_thickness_mm"], gl["glass_rebate_mm"]
    c.HEAD_Z0 = hd["z0"]
    c.PT, c.GR, c.PLAY = P["panels"]["thickness_mm"], P["panels"]["groove_depth_mm"], P["panels"]["side_play_mm"]
    c.PY0 = c.LY0 + (c.TH - c.PT) / 2
    c.PY1 = c.PY0 + c.PT
    c.JL = F["jamb_x_mm"]["left"]
    c.JR = F["jamb_x_mm"]["right"]
    c.LAP = P["mouldings"]["outside_bolection"]["lap_over_framing_mm"]
    c.BW = P["mouldings"]["outside_bolection"]["width_on_face_mm"]
    c.SW = P["mouldings"]["inside_single"]["width_on_face_mm"]
    c.OPEN = P["panels"]["openings_leaf_uv_mm"]
    c.band = P["mouldings"]["lock_rail_band"]
    c.weather = P["mouldings"]["weatherboard"]
    c.step = S
    c.brick = B
    c.iron = P["ironmongery"]
    c.thr = S["threshold"]
    c.ground = S.get("ground_z_mm", -70.0)
    c.BR = 300.0
    c.plinth = B.get("plinth") if isinstance(B.get("plinth"), dict) else None
    c.splay = tr.get("end_splay", {})
    c.glazing = gl
    # the head's soffit: a circle through the crown and the springings (flat when there is no camber)
    half = c.OW / 2
    rise = O["camber_rise_mm"]
    if rise > 0:
        c.R = (half ** 2 + rise ** 2) / (2 * rise)
        c.CZ = c.CROWN - c.R
    else:
        c.R = None
        c.CZ = None
    return c


def soffit_z(c, x):
    """The brick head's underside (and the frame head's top edge) at x: a circle through the crown and the springings."""
    if not c.R:
        return c.CROWN
    return c.CZ + math.sqrt(c.R ** 2 - (x - c.OW / 2) ** 2)


def extrados_z(c, x):
    a = c.brick["arch"]
    return c.CZ + math.sqrt((c.R + a["depth_mm"]) ** 2 - (x - c.OW / 2) ** 2)


# ---------------------------------------------------------------- drawing helpers
def rect(x0, z0, x1, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


def circle(cx, cz, r, n=32):
    return [[cx + r * math.cos(2 * math.pi * i / n), cz + r * math.sin(2 * math.pi * i / n)] for i in range(n)]


def arc(cx, cy, r, a0, a1, n=10):
    return [[cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))] for i in range(n + 1)]


def poly(name, layer, pts, holes=None, shade=None, optional=False):
    d = {"name": name, "layer": layer, "pts": [[round(a, 2), round(b, 2)] for a, b in pts]}
    if holes:
        d["holes"] = [[[round(a, 2), round(b, 2)] for a, b in h] for h in holes]
    if shade is not None:
        d["shade"] = shade
    if optional:
        d["optional"] = True
    return d


def interp_profile(prof, zrel):
    """p of a (z, p) outline at z (points 1..n-2 are the front face; the ends are the closing points)."""
    pts = prof[1:-1]
    if zrel <= pts[0][0]:
        return pts[0][1]
    for (z0, p0), (z1, p1) in zip(pts, pts[1:]):
        if z0 <= zrel <= z1:
            return p0 if z1 == z0 else p0 + (p1 - p0) * (zrel - z0) / (z1 - z0)
    return pts[-1][1]


def front_y(prof, zrel):
    """Frontmost (most negative) y of the transom's front profile at z (relative to the stop underside)."""
    best = None
    for (y0, z0), (y1, z1) in zip(prof, prof[1:]):
        lo, hi = min(z0, z1), max(z0, z1)
        if lo <= zrel <= hi:
            y = y0 if z1 == z0 else y0 + (y1 - y0) * (zrel - z0) / (z1 - z0)
            best = y if best is None else min(best, y)
    return best


def centre_x(c):
    return c.OW / 2


# ---------------------------------------------------------------- elevation
def quoin_width_at(c, z):
    q = c.brick["quoins"]
    b = int((z - q["z_start_mm"]) // q["block_height_mm"])
    b = max(0, min(q["blocks"] - 1, b))
    long_ = (b % 2 == 0) == (q["bottom_block"] == "long")
    return q["stretcher_width_mm"] if long_ else q["header_width_mm"]


def quoin_polys(c):
    """Blocks of three courses, long and short alternating, both sides in step."""
    out = []
    q = c.brick["quoins"]
    if not q.get("present"):
        return out
    for i in range(q["courses"]):
        z0 = q["z_start_mm"] + i * q["course_gauge_mm"]
        z1 = z0 + q["course_gauge_mm"] - q["joint_mm"]
        w = quoin_width_at(c, z0 + 1.0)
        out.append(poly(f"quoin_l{i}", "buff", rect(-w, z0, 0, z1)))
        out.append(poly(f"quoin_r{i}", "buff", rect(c.OW, z0, c.OW + w, z1)))
    return out


def arch_polys(c):
    """A segmental ring of bricks on end: radial joints about the soffit's centre, the extrados parallel to the soffit."""
    out = []
    a = c.brick["arch"]
    if not a.get("present"):
        return out, None
    sc = a["soffit_circle"]
    R, cx, cz, depth = sc["radius_mm"], sc["centre_x_mm"], sc["centre_z_mm"], a["depth_mm"]
    th = math.asin((a["soffit_ends_x_mm"][1] - cx) / R)
    n, j = a["bricks"], a["joint_mm"]
    d = (j / 2) / R
    for i in range(n):
        p0 = -th + 2 * th * i / n + (d if i else 0.0)
        p1 = -th + 2 * th * (i + 1) / n - (d if i < n - 1 else 0.0)
        ph = [p0 + (p1 - p0) * k / 6 for k in range(7)]
        low = [[cx + R * math.sin(p), cz + R * math.cos(p)] for p in ph]
        high = [[cx + (R + depth) * math.sin(p), cz + (R + depth) * math.cos(p)] for p in ph[::-1]]
        out.append(poly(f"arch_brick{i}", "buff", low + high))
    return out, a["extrados_z_at_crown_mm"]


def plinth_polys(c):
    out = []
    pl = c.plinth
    if not pl or not pl.get("present"):
        return out
    sp = pl["splay"]
    x_each = pl["x_each_side_mm"]
    ground = pl["ground_z_mm"]
    z_face_top = sp["z_from_mm"]
    lines = [z_face_top, -65.0, -142.0, -219.0, -296.0, ground]
    for side, (xa, xb) in (("l", (-x_each, 0.0)), ("r", (c.OW, c.OW + x_each))):
        for i, (zt, zb) in enumerate(zip(lines, lines[1:])):
            out.append(poly(f"plinth_face_{side}{i}", "brick", rect(xa, zb, xb, zt - (0 if i == 0 else 10.0)), shade="plinth"))
        n = int(x_each // sp["pitch_mm"])
        for k in range(n):
            if side == "l":
                x1 = -sp["pitch_mm"] * k
                x0 = x1 - sp["brick_face_mm"]
            else:
                x0 = c.OW + sp["pitch_mm"] * k
                x1 = x0 + sp["brick_face_mm"]
            out.append(poly(f"plinth_splay_{side}{k}", "brick", rect(x0, sp["z_from_mm"], x1, sp["z_to_mm"]), shade="splay"))
    return out


def tread_geometry(c):
    """The step's nose: a full round of radius R along the front, its underside turning in to the base face."""
    td = c.step["tread"]
    nr = td["nosing_radius_mm"]
    ztop_f = td["top_z_mm"] - td["fall_to_front_mm"]
    yf = td["front_y_mm"]
    zc = ztop_f - nr
    cos_t = (td["undercut_mm"] - nr) / nr
    th_end = 360.0 - math.degrees(math.acos(cos_t))     # on the lower half: 236.3 degrees for r 45, undercut 20
    z_end = zc + nr * math.sin(math.radians(th_end))
    return td, nr, ztop_f, yf, zc, th_end, z_end


def nose_poly(c, za, zb, name):
    """A transom nose zone between z (above the stop underside) za and zb: its ends splayed at 45 degrees."""
    sp = c.splay
    ov = c.SHOW - c.TR_X0
    zf, zt = sp.get("from_stop_edge_z_mm", 0.0), sp.get("to_z_mm", 1.0)

    def xl(z):
        t = 0.0 if z <= zf else (1.0 if z >= zt else (z - zf) / (zt - zf))
        return c.SHOW - ov * t

    def xr(z):
        t = 0.0 if z <= zf else (1.0 if z >= zt else (z - zf) / (zt - zf))
        return c.OW - c.SHOW + ov * t
    zs = sorted({za, zb} | {z for z in (zf, zt) if za < z < zb})
    left = [[xl(z), c.Z_STOP + z] for z in zs]
    right = [[xr(z), c.Z_STOP + z] for z in zs[::-1]]
    return left + right


def elevation(P):
    c = consts(P)
    out = []
    S = c.step
    zb_hole = S["riser"]["z_mm"][0] if S["riser"].get("present", True) else c.thr["top_z"] - c.thr["thickness_mm"]
    cam = [[x, soffit_z(c, x)] for x in [c.OW * k / 12 for k in range(13)]]
    hole = [[0, zb_hole], [c.OW, zb_hole]] + cam[::-1]
    arch, arch_top = arch_polys(c)
    wall_top = (arch_top or c.CROWN) + c.BR
    wall_bot = min(c.ground, zb_hole) - 20.0
    out.append(poly("brick_wall", "brick", rect(-c.BR, wall_bot, c.OW + c.BR, wall_top), holes=[hole]))
    out += plinth_polys(c)
    out += quoin_polys(c)
    out += arch
    # stone: threshold, riser, step
    t = c.thr
    out.append(poly("threshold", "stone", rect(0, t["top_z"] - t["thickness_mm"], c.OW, t["top_z"])))
    if S["riser"].get("present", True):
        out.append(poly("riser", "stone", rect(0, S["riser"]["z_mm"][0], c.OW, S["riser"]["z_mm"][1])))
    if S["tread"].get("present", True):
        td, nr, ztop_f, yf, zc, th_end, z_end = tread_geometry(c)
        x0, x1 = td["x_mm"]
        out.append(poly("tread_base", "stone", rect(x0, td["ground_z_mm"], x1, z_end), shade="base"))
        out.append(poly("tread_undercut_shadow", "stone", rect(x0, z_end - 24.0, x1, z_end), shade="shadow"))
        out.append(poly("tread", "stone", rect(x0, z_end, x1, ztop_f)))
    # frame
    out.append(poly("jamb_left", "frame", rect(0, 0, c.SHOW, c.GZ1)))
    out.append(poly("jamb_right", "frame", rect(c.OW - c.SHOW, 0, c.OW, c.GZ1)))
    head = [[0, c.GZ1], [c.OW, c.GZ1]] + [[x, soffit_z(c, x)] for x in [c.OW * (12 - k) / 12 for k in range(13)]]
    out.append(poly("head", "frame", head))
    # transom: the face and slope are full-width strips; the nose zones have splayed ends
    for zn, (za, zb) in P["frame"]["transom"]["zones_z_mm"].items():
        if zn in ("lip", "cove", "nose", "quirk"):
            out.append(poly(f"transom_{zn}", "frame", nose_poly(c, za, zb, zn), shade=zn))
        else:
            out.append(poly(f"transom_{zn}", "frame", rect(c.TR_X0, c.Z_STOP + za, c.TR_X1, c.Z_STOP + zb), shade=zn))
    # glazing: bead (or putty) ring over the glass opening, clear glass inside
    out.append(poly("glass_clear", "glass", rect(c.CGX0, c.CGZ0, c.CGX1, c.CGZ1)))
    out.append(poly("glazing_bead", "frame", rect(c.GX0, c.GZ0, c.GX1, c.GZ1), holes=[rect(c.CGX0, c.CGZ0, c.CGX1, c.CGZ1)]))
    # leaf, between the stops
    out.append(poly("leaf_visible", "leaf", rect(c.SHOW, c.Z0, c.OW - c.SHOW, c.Z_STOP)))
    for k, o in c.OPEN.items():
        x0, z0 = c.X0 + o["u0"], c.Z0 + o["v0"]
        x1, z1 = c.X0 + o["u1"], c.Z0 + o["v1"]
        outer = rect(x0 - c.LAP, z0 - c.LAP, x1 + c.LAP, z1 + c.LAP)
        inner = rect(x0 - c.LAP + c.BW, z0 - c.LAP + c.BW, x1 + c.LAP - c.BW, z1 + c.LAP - c.BW)
        out.append(poly(f"bolection_{k}", "moulding", outer, holes=[inner]))
        out.append(poly(f"panel_field_{k}", "panel", inner))
    if c.band.get("present"):
        zb0, zb1 = c.band["z_above_leaf_bottom_mm"]
        bx0, bx1 = c.band["x_mm"]
        out.append(poly("lock_rail_band", "moulding", rect(bx0, c.Z0 + zb0, bx1, c.Z0 + zb1)))
    if c.weather.get("present"):
        zw0, zw1 = c.weather["z_above_leaf_bottom_mm"]
        wx0, wx1 = c.weather["x_mm"]
        out.append(poly("weatherboard", "moulding", rect(wx0, c.Z0 + zw0, wx1, c.Z0 + zw1)))
    out += iron_front(c)
    return out


def parts_transom_profile(c, P):
    return P["frame"]["transom"]["front_profile_yz_mm"]


# ---------------------------------------------------------------- ironmongery, front view
def plate_geometry(c):
    lp = c.iron["letter_plate"]
    xc = c.X0 + lp["centre_u_mm"]
    zc = c.Z0 + lp["centre_above_leaf_bottom_mm"]
    return lp, xc, zc


def iron_front(c, local=False):
    out = []
    ir = c.iron
    lp, xc, zc = plate_geometry(c)
    if lp.get("present"):
        w, h = lp["outer_w_mm"], lp["outer_h_mm"]
        aw, ah = lp["aperture_w_mm"], lp["aperture_h_mm"]
        x0, x1, z0, z1 = xc - w / 2, xc + w / 2, zc - h / 2, zc + h / 2
        ztop_ap = z1 - lp["aperture_top_margin_mm"]
        out.append(poly("letter_plate", "iron", rect(x0, z0, x1, z1), holes=[rect(xc - aw / 2, ztop_ap - ah, xc + aw / 2, ztop_ap)]))
        out.append(poly("letter_plate_flap", "iron", rect(xc - aw / 2 + 1.0, ztop_ap - ah + 1.0, xc + aw / 2 - 1.0, ztop_ap - 2.0)))
    hn = ir.get("house_number", {})
    if hn.get("present") and "v_ranges_mm" in hn:
        for i, (v0, v1) in enumerate(hn["v_ranges_mm"]):
            dx = hn["digit_w_mm"] / 2
            out.append(poly(f"house_number_{i}", "iron", rect(c.X0 + hn["centre_u_mm"] - dx, c.Z0 + v0, c.X0 + hn["centre_u_mm"] + dx, c.Z0 + v1), optional=True))
    cl = ir.get("cylinder_lock", {})
    if cl.get("present"):
        cx, cz = c.X0 + cl["centre_u_mm"], c.Z0 + cl["centre_above_leaf_bottom_mm"]
        out.append(poly("cylinder_collar", "iron", circle(cx, cz, cl["outer_diameter_mm"] / 2), holes=[circle(cx, cz, cl["plug_diameter_mm"] / 2)]))
        out.append(poly("cylinder_plug", "iron", circle(cx, cz, cl["plug_diameter_mm"] / 2)))
    kh = ir.get("old_keyhole", {})
    if kh.get("present"):
        kx, kz = c.X0 + kh["centre_u_mm"], c.Z0 + kh["centre_above_leaf_bottom_mm"]
        out.append(poly("old_keyhole", "iron", rect(kx - kh["w_mm"] / 2, kz - kh["h_mm"] / 2, kx + kh["w_mm"] / 2, kz + kh["h_mm"] / 2)))
    kn = ir.get("knob", {})
    if kn.get("present"):
        nx, nz = c.X0 + kn["centre_u_mm"], c.Z0 + kn["centre_above_leaf_bottom_mm"]
        out.append(poly("knob_rose", "iron", circle(nx, nz, kn["rose_diameter_mm"] / 2), holes=[circle(nx, nz, kn["diameter_mm"] / 2)]))
        out.append(poly("knob", "iron", circle(nx, nz, kn["diameter_mm"] / 2)))
    kp = ir.get("keep", {})
    if kp.get("present"):
        z0, z1 = kp["z_range_mm"]
        out.append(poly("keep", "iron", rect(kp["centre_x_mm"] - kp["w_mm"] / 2, z0, kp["centre_x_mm"] + kp["w_mm"] / 2, z1)))
    return out


# ---------------------------------------------------------------- horizontal sections
def bolection_plan(P, c, xe, s):
    prof = P["mouldings"]["outside_bolection"]["profile_dh_mm"]
    below = P["mouldings"]["outside_bolection"]["panel_face_below_framing_mm"]
    pts = [[xe - s * c.LAP + s * d, c.LY0 - h] for d, h in prof]
    pts += [[xe, c.LY0 + below], [xe, c.LY0]]
    return pts


def single_plan(c, xe, s):
    return [[xe, c.LY1], [xe + s * 4.0, c.LY1], [xe + s * 10.0, c.LY1 - 6.0], [xe + s * 16.0, c.PY1 + 4.0], [xe + s * c.SW, c.PY1], [xe, c.PY1]]


def jamb_plan(P, c, left):
    if left:
        xs, xr, xb = c.SHOW, c.SHOW - c.REB_W, c.SHOW - c.JF
    else:
        xs, xr, xb = c.OW - c.SHOW, c.OW - c.SHOW + c.REB_W, c.OW - c.SHOW + c.JF
    return [[xb, c.FY0], [xs, c.FY0], [xs, c.STOP_Y], [xr, c.STOP_Y], [xr, c.FY1], [xb, c.FY1]]


def stop_bead_plan(P, c, left):
    sb = P["frame"].get("stop_inner_bead")
    if not sb:
        return None
    xs = c.SHOW if left else c.OW - c.SHOW
    s = -1 if left else 1       # the bead sits on the stop's inner edge, on the door side of xs
    w, pr = 5.0, 2.5
    return [[xs, c.FY0], [xs + s * w, c.FY0], [xs + s * w, c.FY0 - 0.6], [xs + s * 0.82 * w, c.FY0 - 1.7], [xs + s * 0.45 * w, c.FY0 - 2.4], [xs, c.FY0 - pr]]


def brick_plan(c):
    JL0, JR1 = c.JL[0], c.JR[1]
    left = [[-c.BR, 0], [0, 0], [0, c.REV], [JL0, c.REV], [JL0, c.WALL], [-c.BR, c.WALL]]
    right = [[c.OW, 0], [c.OW + c.BR, 0], [c.OW + c.BR, c.WALL], [JR1, c.WALL], [JR1, c.REV], [c.OW, c.REV]]
    return [poly("brick_left", "brick", left), poly("brick_right", "brick", right)]


def v_zone(c, z_cut):
    v = z_cut - c.Z0
    o = c.OPEN
    bl, tl = o["bottom_left"], o["top_left"]
    if bl["v0"] <= v <= bl["v1"]:
        return "bottom_panels"
    if tl["v0"] <= v <= tl["v1"]:
        return "top_panels"
    return "rail"


def section_h(P, z_cut):
    c = consts(P)
    out = brick_plan(c)
    q = c.brick.get("quoins", {})
    if q.get("present"):
        w = quoin_width_at(c, z_cut)
        out.append(poly("reveal_return_left", "buff", rect(-w, 0.0, 0.0, c.REV)))
        out.append(poly("reveal_return_right", "buff", rect(c.OW, 0.0, c.OW + w, c.REV)))
    out.append(poly("jamb_left", "frame", jamb_plan(P, c, True)))
    out.append(poly("jamb_right", "frame", jamb_plan(P, c, False)))
    for left in (True, False):
        b = stop_bead_plan(P, c, left)
        if b:
            out.append(poly("stop_bead_" + ("l" if left else "r"), "frame", b))
    zone = v_zone(c, z_cut)
    v = z_cut - c.Z0
    gy0, gy1 = c.PY0, c.PY1
    lp, xc, zc = plate_geometry(c)
    plate_here = lp.get("present") and abs(z_cut - zc) <= lp["outer_h_mm"] / 2
    ap_here = plate_here and (zc + lp["outer_h_mm"] / 2 - lp["aperture_top_margin_mm"] - lp["aperture_h_mm"] <= z_cut <= zc + lp["outer_h_mm"] / 2 - lp["aperture_top_margin_mm"])
    cl = c.iron.get("cylinder_lock", {})
    cx = c.X0 + cl.get("centre_u_mm", 0)
    lock_here = cl.get("present") and abs(z_cut - (c.Z0 + cl["centre_above_leaf_bottom_mm"])) <= cl["outer_diameter_mm"] / 2
    if zone == "rail":
        stile_pts = rect(c.X0, c.LY0, c.X0 + c.W, c.LY1)
        holes = []
        if ap_here:
            holes.append(rect(xc - lp["aperture_w_mm"] / 2, c.LY0, xc + lp["aperture_w_mm"] / 2, c.LY1))
        if lock_here:
            hw = math.sqrt(max((cl["outer_diameter_mm"] / 2) ** 2 - (z_cut - (c.Z0 + cl["centre_above_leaf_bottom_mm"])) ** 2, 0.0))
            holes.append(rect(cx - hw, c.LY0, cx + hw, c.LY0 + 30.0))
        out.append(poly("rail", "leaf", stile_pts, holes=holes or None))
    else:
        oo = c.OPEN["bottom_left"] if zone == "bottom_panels" else c.OPEN["top_left"]
        o_l = c.OPEN["bottom_left" if zone == "bottom_panels" else "top_left"]
        o_r = c.OPEN["bottom_right" if zone == "bottom_panels" else "top_right"]
        xs = [c.X0, c.X0 + o_l["u0"], c.X0 + o_l["u1"], c.X0 + o_r["u0"], c.X0 + o_r["u1"], c.X0 + c.W]
        GR, PLAY = c.GR, c.PLAY
        sl_holes = []
        if ap_here:
            sl_holes.append(rect(xc - lp["aperture_w_mm"] / 2, c.LY0, xc + lp["aperture_w_mm"] / 2, c.LY1))
        out.append(poly("stile_left", "leaf", [[xs[0], c.LY0], [xs[1], c.LY0], [xs[1], gy0], [xs[1] - GR, gy0], [xs[1] - GR, gy1], [xs[1], gy1], [xs[1], c.LY1], [xs[0], c.LY1]]))
        mh = sl_holes or None
        if lock_here:
            hw = math.sqrt(max((cl["outer_diameter_mm"] / 2) ** 2 - (z_cut - (c.Z0 + cl["centre_above_leaf_bottom_mm"])) ** 2, 0.0))
            right_holes = [rect(cx - hw, c.LY0, cx + hw, c.LY0 + 30.0)]
        else:
            right_holes = None
        out.append(poly("muntin", "leaf", [[xs[2], c.LY0], [xs[3], c.LY0], [xs[3], gy0], [xs[3] - GR, gy0], [xs[3] - GR, gy1], [xs[3], gy1], [xs[3], c.LY1],
                                           [xs[2], c.LY1], [xs[2], gy1], [xs[2] + GR, gy1], [xs[2] + GR, gy0], [xs[2], gy0]], holes=mh))
        out.append(poly("stile_right", "leaf", [[xs[4], c.LY0], [xs[5], c.LY0], [xs[5], c.LY1], [xs[4], c.LY1], [xs[4], gy1], [xs[4] + GR, gy1], [xs[4] + GR, gy0], [xs[4], gy0]], holes=right_holes))
        for nm, a, b in (("panel_left", xs[1], xs[2]), ("panel_right", xs[3], xs[4])):
            out.append(poly(nm, "panel", rect(a - GR + PLAY / 2, gy0, b + GR - PLAY / 2, gy1)))
            out.append(poly(nm + "_bolection_l", "moulding", bolection_plan(P, c, a, +1)))
            out.append(poly(nm + "_bolection_r", "moulding", bolection_plan(P, c, b, -1)))
            out.append(poly(nm + "_single_l", "moulding", single_plan(c, a, +1)))
            out.append(poly(nm + "_single_r", "moulding", single_plan(c, b, -1)))
    # band and weatherboard (they span stop to stop)
    for key, blk, prof_key in (("lock_rail_band", c.band, "profile_zp_mm"), ("weatherboard", c.weather, "profile_zp_mm")):
        if not blk.get("present"):
            continue
        za, zb = blk["z_above_leaf_bottom_mm"]
        if za <= v <= zb:
            p = interp_profile(blk[prof_key], v - za)
            x0, x1 = blk["x_mm"]
            out.append(poly(key, "moulding", rect(x0, c.LY0 - p, x1, c.LY0)))
    # letter plate in section
    if plate_here:
        w = lp["outer_w_mm"]
        bt, rw, rp = lp["backplate_thickness_mm"], lp["rim_width_mm"], lp["rim_proud_mm"]
        aw = lp["aperture_w_mm"]
        if ap_here:
            for sgn in (-1, 1):
                xa = xc + sgn * aw / 2
                xo = xc + sgn * w / 2
                pts = [[xa, c.LY0], [xo, c.LY0], [xo, c.LY0 - bt], [xo - sgn * 2.0, c.LY0 - bt - 1.0], [xa, c.LY0 - rp]]
                out.append(poly("letter_plate_" + ("l" if sgn < 0 else "r"), "iron", pts))
            out.append(poly("letter_plate_flap", "iron", rect(xc - aw / 2 + 0.05, c.LY0 - 2.0, xc + aw / 2 - 0.05, c.LY0 + 0.6)))
        else:
            out.append(poly("letter_plate", "iron", [[xc - w / 2, c.LY0], [xc + w / 2, c.LY0], [xc + w / 2, c.LY0 - bt], [xc + w / 2 - 2.0, c.LY0 - bt - 1.0], [xc + w / 2 - rw, c.LY0 - rp],
                                                    [xc - w / 2 + rw, c.LY0 - rp], [xc - w / 2 + 2.0, c.LY0 - bt - 1.0], [xc - w / 2, c.LY0 - bt]]))
    if lock_here:
        out.append(poly("cylinder_collar", "iron", rect(cx - cl["outer_diameter_mm"] / 2, c.LY0 - cl["collar_proud_mm"], cx + cl["outer_diameter_mm"] / 2, c.LY0 + 4.0),
                        holes=[rect(cx - cl["plug_diameter_mm"] / 2, c.LY0 - cl["collar_proud_mm"], cx + cl["plug_diameter_mm"] / 2, c.LY0 + 4.0)]))
        out.append(poly("cylinder_plug", "iron", rect(cx - cl["plug_diameter_mm"] / 2, c.LY0 - cl["collar_proud_mm"] + 0.5, cx + cl["plug_diameter_mm"] / 2, c.LY0 + 28.0)))
    kp = c.iron.get("keep", {})
    if kp.get("present") and kp["z_range_mm"][0] <= z_cut <= kp["z_range_mm"][1]:
        out.append(poly("keep", "iron", rect(kp["centre_x_mm"] - kp["w_mm"] / 2, c.FY0 - kp["proud_mm"], kp["centre_x_mm"] + kp["w_mm"] / 2, c.FY0)))
    kn = c.iron.get("knob", {})
    if kn.get("present") and abs(z_cut - (c.Z0 + kn["centre_above_leaf_bottom_mm"])) <= 0.5:
        nx = c.X0 + kn["centre_u_mm"]
        rz = kn["profile_rz_mm"]
        pts = [[nx + r_, c.LY0 - z_] for r_, z_ in rz] + [[nx - r_, c.LY0 - z_] for r_, z_ in rz[::-1]]
        out.append(poly("knob", "iron", pts))
    return out


def section_h_transom(P):
    c = consts(P)
    out = brick_plan(c)
    out.append(poly("jamb_left", "frame", jamb_plan(P, c, True)))
    out.append(poly("jamb_right", "frame", jamb_plan(P, c, False)))
    zrel = P["frame"]["transom"]["zones_z_mm"]["face"][0] + 4.0
    fy = front_y(P["frame"]["transom"]["front_profile_yz_mm"], zrel)
    y_front = c.FY0 + fy
    x0, x1 = c.TR_X0, c.TR_X1
    sl, sr_ = c.SHOW, c.OW - c.SHOW
    out.append(poly("transom", "frame", [[x0, y_front], [x1, y_front], [x1, c.FY0], [sr_, c.FY0], [sr_, c.STOP_Y], [sr_ + c.REB_W, c.STOP_Y], [sr_ + c.REB_W, c.FY1],
                                          [sl - c.REB_W, c.FY1], [sl - c.REB_W, c.STOP_Y], [sl, c.STOP_Y], [sl, c.FY0], [x0, c.FY0]]))
    return out, c.Z_STOP + zrel


# ---------------------------------------------------------------- vertical sections
def bolection_vert(P, c, ze, s):
    prof = P["mouldings"]["outside_bolection"]["profile_dh_mm"]
    below = P["mouldings"]["outside_bolection"]["panel_face_below_framing_mm"]
    pts = [[c.LY0 - h, ze - s * c.LAP + s * d] for d, h in prof]
    pts += [[c.LY0 + below, ze], [c.LY0, ze]]
    return pts


def single_vert(c, ze, s):
    return [[y, z] for z, y in [(ze, c.LY1), (ze + s * 4.0, c.LY1), (ze + s * 10.0, c.LY1 - 6.0), (ze + s * 16.0, c.PY1 + 4.0), (ze + s * c.SW, c.PY1), (ze, c.PY1)]]


def transom_poly_vert(P, c):
    pr = P["frame"]["transom"]["front_profile_yz_mm"]
    pts = [[c.STOP_Y, c.Z_STOP]]
    for y, z in pr[1:]:
        pts.append([c.FY0 + y, c.Z_STOP + z])
    ga, gb = c.GLASS_Y - 2.0, c.GLASS_Y + 2.0
    pts += [[ga, c.Z_TR_TOP], [ga, c.Z_TR_TOP - c.GLASS_RB], [gb, c.Z_TR_TOP - c.GLASS_RB], [gb, c.Z_TR_TOP],
            [c.FY1, c.Z_TR_TOP], [c.FY1, c.Z_REB], [c.STOP_Y, c.Z_REB]]
    return pts


def bead_vert_section(P, c, bottom):
    """Quarter-round bead on the glass's front, a (along the face, z) and p (proud, y)."""
    gl = P["frame"]["glazing"]
    prof = gl["bead_profile_ap_mm"]
    gf = c.GLASS_Y - c.GLASS_T / 2
    if bottom:
        return [[gf - p, c.Z_TR_TOP + a] for a, p in prof]
    return [[gf - p, c.GZ1 - a] for a, p in prof]


def section_v(P, x_cut):
    c = consts(P)
    out = []
    u = x_cut - c.X0
    o_l, o_r = c.OPEN["bottom_left"], c.OPEN["bottom_right"]
    in_col = (o_l["u0"] <= u <= o_l["u1"]) or (o_r["u0"] <= u <= o_r["u1"])
    gy0, gy1 = c.PY0, c.PY1
    GR = c.GR
    o_b = c.OPEN["bottom_left"]
    o_t = c.OPEN["top_left"]
    zs = [c.Z0, c.Z0 + o_b["v0"], c.Z0 + o_b["v1"], c.Z0 + o_t["v0"], c.Z0 + o_t["v1"], c.Z0 + c.H]
    # stone: threshold, riser, tread, ground
    S = c.step
    t = c.thr
    zt0, zt1 = t["top_z"] - t["thickness_mm"], t["top_z"]
    r = t["nose_radius_mm"]
    thr = [[t["front_y_mm"], zt0]]
    thr += [[t["front_y_mm"], zt1 - r]] if r > 0 else []
    thr += arc(t["front_y_mm"] + r, zt1 - r, r, 180, 90, 8)[1:] if r > 0 else [[t["front_y_mm"], zt1]]
    thr += [[t["back_y_mm"], zt1], [t["back_y_mm"], zt0]]
    out.append(poly("threshold", "stone", thr))
    out.append(poly("ground", "ground", rect(-600.0, c.ground - 100.0, t["back_y_mm"] if S["tread"].get("present", True) else t["front_y_mm"], c.ground)))
    if S["riser"].get("present", True):
        z0r, z1r = S["riser"]["z_mm"]
        out.append(poly("riser", "stone", [[S["riser"]["face_y_mm"], z0r], [t["back_y_mm"], z0r], [t["back_y_mm"], z1r], [S["riser"]["face_y_mm"], z1r]]))
    if S["tread"].get("present", True):
        td, nr, ztop_f, yf, zc, th_end, z_end = tread_geometry(c)
        pts = [[t["back_y_mm"], td["top_z_mm"]], [S["riser"]["face_y_mm"], td["top_z_mm"]], [yf + nr, ztop_f]]
        pts += arc(yf + nr, zc, nr, 90, th_end, 12)[1:]
        pts += [[yf + td["undercut_mm"], td["ground_z_mm"]], [t["back_y_mm"], td["ground_z_mm"]]]
        out.append(poly("tread", "stone", pts))
    # leaf
    if not in_col:
        out.append(poly("leaf_solid", "leaf", rect(c.LY0, zs[0], c.LY1, zs[5])))
    else:
        out.append(poly("bottom_rail", "leaf", [[c.LY0, zs[0]], [c.LY1, zs[0]], [c.LY1, zs[1]], [gy1, zs[1]], [gy1, zs[1] - GR], [gy0, zs[1] - GR], [gy0, zs[1]], [c.LY0, zs[1]]]))
        out.append(poly("lock_rail", "leaf", [[c.LY0, zs[2]], [gy0, zs[2]], [gy0, zs[2] + GR], [gy1, zs[2] + GR], [gy1, zs[2]], [c.LY1, zs[2]], [c.LY1, zs[3]],
                                              [gy1, zs[3]], [gy1, zs[3] - GR], [gy0, zs[3] - GR], [gy0, zs[3]], [c.LY0, zs[3]]]))
        out.append(poly("top_rail", "leaf", [[c.LY0, zs[4]], [gy0, zs[4]], [gy0, zs[4] + GR], [gy1, zs[4] + GR], [gy1, zs[4]], [c.LY1, zs[4]], [c.LY1, zs[5]], [c.LY0, zs[5]]]))
        out.append(poly("panel_bottom", "panel", rect(gy0, zs[1] - GR, gy1, zs[2] + GR)))
        out.append(poly("panel_top", "panel", rect(gy0, zs[3] - GR, gy1, zs[4] + GR)))
        for nm, ze, s in (("b_lower", zs[1], +1), ("b_upper", zs[2], -1), ("t_lower", zs[3], +1), ("t_upper", zs[4], -1)):
            out.append(poly("bolection_" + nm, "moulding", bolection_vert(P, c, ze, s)))
            out.append(poly("single_" + nm, "moulding", single_vert(c, ze, s)))
    # band and weatherboard
    for key, blk in (("lock_rail_band", c.band), ("weatherboard", c.weather)):
        if blk.get("present"):
            za, zb = blk["z_above_leaf_bottom_mm"]
            pr = blk["profile_zp_mm"]
            out.append(poly(key, "moulding", [[c.LY0 - p, c.Z0 + za + z] for z, p in pr]))
    # frame: transom, beads, glass, head
    out.append(poly("transom", "frame", transom_poly_vert(P, c)))
    out.append(poly("bead_bottom", "frame", bead_vert_section(P, c, True)))
    out.append(poly("bead_top", "frame", bead_vert_section(P, c, False)))
    ga, gb = c.GLASS_Y - c.GLASS_T / 2, c.GLASS_Y + c.GLASS_T / 2
    out.append(poly("glass", "glass", rect(ga, c.Z_TR_TOP - c.GLASS_RB, gb, c.GZ1 + c.GLASS_RB)))
    hz1 = c.GZ1 + c.JF
    out.append(poly("head", "frame", [[c.FY0, c.GZ1], [c.GLASS_Y - 2.0, c.GZ1], [c.GLASS_Y - 2.0, c.GZ1 + c.GLASS_RB], [c.GLASS_Y + 2.0, c.GZ1 + c.GLASS_RB],
                                       [c.GLASS_Y + 2.0, c.GZ1], [c.FY1, c.GZ1], [c.FY1, hz1], [c.FY0, hz1]]))
    # brick head
    a = c.brick["arch"]
    sz = soffit_z(c, x_cut)
    if a.get("present"):
        top = extrados_z(c, x_cut)
        out.append(poly("arch_ring", "buff", [[0, sz], [c.FY0, sz], [c.FY0, max(hz1, sz)], [c.WALL, max(hz1, sz)], [c.WALL, top], [0, top]]))
    else:
        out.append(poly("brick_over_head", "brick", [[0, sz], [c.FY0, sz], [c.FY0, hz1], [c.WALL, hz1], [c.WALL, hz1 + 200.0], [0, hz1 + 200.0]]))
    return out


def section_v_muntin(P):
    c = consts(P)
    xm = c.X0 + c.W / 2
    sv = section_v(P, xm)
    lp, xc, zc = plate_geometry(c)
    out = [d for d in sv if d["layer"] != "leaf" or True]
    # letter plate section on the muntin (y, z): backplate, rim, flap, slot through the leaf
    if lp.get("present"):
        h, bt, rp, rw = lp["outer_h_mm"], lp["backplate_thickness_mm"], lp["rim_proud_mm"], lp["rim_width_mm"]
        z1 = zc + h / 2
        z0 = zc - h / 2
        ztop_ap = z1 - lp["aperture_top_margin_mm"]
        zbot_ap = ztop_ap - lp["aperture_h_mm"]
        # slot through the leaf
        for d in out:
            if d["name"] == "leaf_solid":
                d["pts"] = [[c.LY0, c.Z0], [c.LY1, c.Z0], [c.LY1, zbot_ap], [c.LY0, zbot_ap], [c.LY0, c.Z0]]  # lower leaf part
                d["name"] = "leaf_below_slot"
        out.append(poly("leaf_above_slot", "leaf", rect(c.LY0, ztop_ap, c.LY1, c.Z0 + c.H)))
        out.append(poly("letter_plate_top", "iron", [[c.LY0, ztop_ap], [c.LY0 - rp, ztop_ap], [c.LY0 - bt - 1.0, z1 - 2.0], [c.LY0 - bt, z1], [c.LY0, z1]]))
        out.append(poly("letter_plate_bottom", "iron", [[c.LY0, zbot_ap], [c.LY0 - rp, zbot_ap], [c.LY0 - bt - 1.0, z0 + 2.0], [c.LY0 - bt, z0], [c.LY0, z0]]))
        out.append(poly("letter_plate_flap", "iron", [[c.LY0 - 2.0, ztop_ap], [c.LY0 + 0.6, ztop_ap], [c.LY0 + 0.6, zbot_ap + 4.0], [c.LY0 - 2.0, zbot_ap + 4.0]]))
    hn = c.iron.get("house_number", {})
    if hn.get("present") and "v_ranges_mm" in hn:
        for i, (v0, v1) in enumerate(hn["v_ranges_mm"]):
            out.append(poly(f"house_number_{i}", "iron", rect(c.LY0 - hn["relief_mm"], c.Z0 + v0, c.LY0, c.Z0 + v1), optional=True))
    return out, xm


def step_plan(P):
    c = consts(P)
    S, t = c.step, c.thr
    out = []
    out.append(poly("wall_left", "brick", [[-c.BR, 0], [0, 0], [0, c.REV], [c.JL[0], c.REV], [c.JL[0], c.WALL], [-c.BR, c.WALL]]))
    out.append(poly("wall_right", "brick", [[c.OW, 0], [c.OW + c.BR, 0], [c.OW + c.BR, c.WALL], [c.JR[1], c.WALL], [c.JR[1], c.REV], [c.OW, c.REV]]))
    pl = c.plinth
    if pl and pl.get("present"):
        yp = -pl["front_proud_of_wall_face_mm"]
        out.append(poly("plinth_left", "brick", rect(-pl["x_each_side_mm"], yp, 0, 0), shade="plinth"))
        out.append(poly("plinth_right", "brick", rect(c.OW, yp, c.OW + pl["x_each_side_mm"], 0), shade="plinth"))
    b = t.get("bearing_into_wall_each_side_mm", 0.0)
    out.append(poly("threshold", "stone", rect(-b, t["front_y_mm"], c.OW + b, t["back_y_mm"])))
    out.append(poly("jamb_left_foot", "frame", rect(c.JL[0], c.FY0, c.SHOW, c.FY1)))
    out.append(poly("jamb_right_foot", "frame", rect(c.OW - c.SHOW, c.FY0, c.JR[1], c.FY1)))
    if S["tread"].get("present", True):
        td = S["tread"]
        x0, x1 = td["x_mm"]
        r_ = td["plan_corner_radius_mm"]
        yb, yf = S["riser"]["face_y_mm"], td["front_y_mm"]
        yp = -pl["front_proud_of_wall_face_mm"] if pl and pl.get("present") else yb
        pts = [[x0, yp], [0.0, yp], [0.0, yb], [c.OW, yb], [c.OW, yp], [x1, yp], [x1, yf + r_]]
        pts += arc(x1 - r_, yf + r_, r_, 0, -90, 8)[1:] + arc(x0 + r_, yf + r_, r_, -90, -180, 8)[0:-1] + [[x0, yf + r_]]
        out.append(poly("tread", "stone", pts))
    return out


def section_v_plinth(P):
    """A cut through the left plinth (x = -60): the projecting base, its 45 degree splay and the wall above."""
    c = consts(P)
    pl = c.plinth
    if not pl or not pl.get("present"):
        return None, None
    sp = pl["splay"]
    yp = -pl["front_proud_of_wall_face_mm"]
    g = pl["ground_z_mm"]
    out = [poly("plinth", "brick", [[yp, g], [yp, sp["z_from_mm"]], [0, sp["z_to_mm"]], [c.WALL, sp["z_to_mm"]], [c.WALL, g]], shade="plinth"),
           poly("wall_above", "brick", rect(0, sp["z_to_mm"], c.WALL, sp["z_to_mm"] + 400.0)),
           poly("ground", "ground", rect(-600.0, g - 100.0, c.WALL, g))]
    return out, -60.0


# ---------------------------------------------------------------- profiles and furniture (own frames)
def profiles(P):
    c = consts(P)
    out = {}
    bol = P["mouldings"]["outside_bolection"]
    below = bol["panel_face_below_framing_mm"]
    pts = [[d, h] for d, h in bol["profile_dh_mm"]] + [[c.LAP, -below], [c.LAP, 0.0]]
    out["bolection (d across the face, h proud of the framing)"] = pts
    if c.band.get("present"):
        out["lock-rail band (p proud, z up from its underside)"] = [[p, z] for z, p in c.band["profile_zp_mm"]]
    if c.weather.get("present"):
        out["weatherboard (p proud, z up from its underside)"] = [[p, z] for z, p in c.weather["profile_zp_mm"]]
    tr = P["frame"]["transom"]
    fp = tr["front_profile_yz_mm"]
    tp = [[y, z] for y, z in fp] + [[19.0, tr["face_height_mm"]], [127.0, tr["face_height_mm"]], [127.0, 0.0]]
    out["transom front (y from the jamb face, outwards negative; z up from the stop underside)"] = tp
    jb = [[-c.JF, 0], [0, 0], [0, c.STOP_Y - c.FY0], [-c.REB_W, c.STOP_Y - c.FY0], [-c.REB_W, c.JD], [-c.JF, c.JD]]
    out["jamb section, square (x into the opening, y into the wall), left jamb"] = jb
    out["glazing bead (a along the face, p proud)"] = [[a, p] for a, p in P["frame"]["glazing"]["bead_profile_ap_mm"]]
    t = c.thr
    thr = [[t["front_y_mm"], t["top_z"] - t["thickness_mm"]]]
    r = t["nose_radius_mm"]
    thr += [[t["front_y_mm"], t["top_z"] - r]] + arc(t["front_y_mm"] + r, t["top_z"] - r, r, 180, 90, 8)[1:] + [[t["back_y_mm"], t["top_z"]], [t["back_y_mm"], t["top_z"] - t["thickness_mm"]]]
    out["threshold (y into the wall, z)"] = thr
    if P["step"]["tread"].get("present", True):
        td, nr, ztop_f, yf, zc, th_end, z_end = tread_geometry(c)
        pp = [[P["step"]["riser"]["face_y_mm"], td["top_z_mm"]], [yf + nr, ztop_f]] + arc(yf + nr, zc, nr, 90, th_end, 12)[1:] + [[yf + td["undercut_mm"], td["ground_z_mm"]], [P["step"]["riser"]["face_y_mm"], td["ground_z_mm"]]]
        out["step tread, full round nose over an undercut (y, z)"] = pp
    if c.plinth and c.plinth.get("present"):
        sp = c.plinth["splay"]
        out["plinth splay (y, z)"] = [[-c.plinth["front_proud_of_wall_face_mm"], c.plinth["ground_z_mm"]], [-c.plinth["front_proud_of_wall_face_mm"], sp["z_from_mm"]], [0, sp["z_to_mm"]], [60.0, sp["z_to_mm"]], [60.0, c.plinth["ground_z_mm"]]]
    kn = c.iron.get("knob", {})
    if kn.get("present"):
        rz = kn["profile_rz_mm"]
        out["turned centre knob (r, z proud)"] = [[r_, z_] for r_, z_ in rz] + [[-r_, z_] for r_, z_ in rz[::-1]]
    return out


def furniture(P):
    c = consts(P)
    out = []
    ir = c.iron
    lp = ir["letter_plate"]
    if lp.get("present"):
        w, h = lp["outer_w_mm"], lp["outer_h_mm"]
        aw, ah = lp["aperture_w_mm"], lp["aperture_h_mm"]
        top = h / 2 - lp["aperture_top_margin_mm"]
        out.append(poly("letter_plate", "iron", rect(-w / 2, -h / 2, w / 2, h / 2), holes=[rect(-aw / 2, top - ah, aw / 2, top)]))
        out.append(poly("letter_plate_flap", "iron", rect(-aw / 2 + 1, top - ah + 1, aw / 2 - 1, top - 2)))
    cl = ir.get("cylinder_lock", {})
    if cl.get("present"):
        out.append(poly("cylinder_collar", "iron", [[x + 120, z] for x, z in circle(0, 0, cl["outer_diameter_mm"] / 2)], holes=[[[x + 120, z] for x, z in circle(0, 0, cl["plug_diameter_mm"] / 2)]]))
        out.append(poly("cylinder_plug", "iron", [[x + 120, z] for x, z in circle(0, 0, cl["plug_diameter_mm"] / 2)]))
    kp = ir.get("keep", {})
    if kp.get("present"):
        out.append(poly("keep", "iron", rect(200 - kp["w_mm"] / 2, -kp["h_mm"] / 2, 200 + kp["w_mm"] / 2, kp["h_mm"] / 2)))
    kn = ir.get("knob", {})
    if kn.get("present"):
        out.append(poly("knob_rose", "iron", [[x + 300, z] for x, z in circle(0, 0, kn["rose_diameter_mm"] / 2)], holes=[[[x + 300, z] for x, z in circle(0, 0, kn["diameter_mm"] / 2)]]))
        out.append(poly("knob", "iron", [[x + 300, z] for x, z in circle(0, 0, kn["diameter_mm"] / 2)]))
    return out


# ---------------------------------------------------------------- the whole set
def all_drawings(T, variant=None):
    P = parts(T, variant)
    c = consts(P)
    lock_z = c.Z0 + c.iron["cylinder_lock"]["centre_above_leaf_bottom_mm"]
    bz = c.Z0 + sum(c.band["z_above_leaf_bottom_mm"]) / 2 if c.band.get("present") else c.Z0 + 787.0
    o_b = c.OPEN["bottom_left"]
    z_low = c.Z0 + (o_b["v0"] + o_b["v1"]) / 2
    lp, xc, zc = plate_geometry(c)
    doc = {"source": "target.json " + (variant or T.get("default_variant", "")), "units": "mm", "variant": variant or T.get("default_variant")}
    doc["elevation"] = {"axes": "x across, z up; origin left brick reveal, top of the threshold", "polygons": elevation(P)}
    doc["section_h"] = {"axes": "x across, y into the wall (outside -y)", "cut_z_mm": round(z_low, 1), "polygons": section_h(P, z_low)}
    doc["section_h_lock"] = {"axes": "x across, y into the wall (outside -y)", "cut_z_mm": round(lock_z, 1), "polygons": section_h(P, lock_z)}
    if c.band.get("present"):
        doc["section_h_band"] = {"axes": "x across, y into the wall (outside -y)", "cut_z_mm": round(bz, 1), "polygons": section_h(P, bz)}
    doc["section_h_plate"] = {"axes": "x across, y into the wall (outside -y)", "cut_z_mm": round(zc, 1), "polygons": section_h(P, zc)}
    sh_t, z_t = section_h_transom(P)
    doc["section_h_transom"] = {"axes": "x across, y into the wall (outside -y)", "cut_z_mm": round(z_t, 1), "polygons": sh_t}
    u_mid = (o_b["u0"] + o_b["u1"]) / 2
    doc["section_v"] = {"axes": "y into the wall (outside -y), z up", "cut_x_mm": round(c.X0 + u_mid, 1), "polygons": section_v(P, c.X0 + u_mid)}
    sm, xm = section_v_muntin(P)
    doc["section_v_muntin"] = {"axes": "y into the wall (outside -y), z up", "cut_x_mm": round(xm, 1), "polygons": sm}
    doc["plan"] = {"axes": "x across, y into the wall (outside -y), seen from above", "polygons": step_plan(P)}
    spl, xpl = section_v_plinth(P)
    if spl:
        doc["section_v_plinth"] = {"axes": "y into the wall (outside -y), z up", "cut_x_mm": xpl, "polygons": spl}
    doc["profiles"] = {k: [[round(a, 2), round(b, 2)] for a, b in v] for k, v in profiles(P).items()}
    doc["furniture"] = {"axes": "each item in its own frame: mm from its centre (the cylinder shifted +120, the keep +200, the knob +300)", "polygons": furniture(P)}
    return doc


# ---------------------------------------------------------------- pictures
LAYER_RGB = {"brick": (176, 96, 72), "buff": (214, 200, 160), "stone": (178, 176, 168), "frame": (238, 238, 232), "glass": (150, 190, 205),
             "leaf": (170, 30, 30), "panel": (205, 60, 55), "moulding": (120, 15, 15), "iron": (200, 165, 70), "ground": (120, 120, 120)}
SHADE = {"slope": 0.0, "face": -22, "cove": -48, "lip": -8, "lip_and_cove": -30, "nose": -30, "quirk": -70, "splay": 18, "plinth": -10, "base": -35, "shadow": -95}


def render(polys, path, scale=1.0, flip=True, margin=20, bounds_layers=None, title=None):
    from PIL import Image, ImageDraw
    sel = [d for d in polys if (bounds_layers is None or d["layer"] in bounds_layers)]
    xs = [p[0] for d in sel for p in d["pts"]]
    ys = [p[1] for d in sel for p in d["pts"]]
    x0, x1, y0, y1 = min(xs) - margin, max(xs) + margin, min(ys) - margin, max(ys) + margin
    w, h = int(math.ceil((x1 - x0) * scale)), int(math.ceil((y1 - y0) * scale))
    top = 18 if title else 0
    im = Image.new("RGB", (w, h + top), (255, 255, 255))
    dr = ImageDraw.Draw(im)

    def tp(p):
        return ((p[0] - x0) * scale, top + ((y1 - p[1]) if flip else (p[1] - y0)) * scale)
    for d in polys:
        col = LAYER_RGB.get(d["layer"], (128, 128, 128))
        if d.get("shade") in SHADE:
            col = tuple(int(max(0, min(255, v + SHADE[d["shade"]]))) for v in col)
        if d.get("holes"):
            mask = Image.new("L", im.size, 0)
            md = ImageDraw.Draw(mask)
            md.polygon([tp(p) for p in d["pts"]], fill=255)
            for hole in d["holes"]:
                md.polygon([tp(p) for p in hole], fill=0)
            im.paste(Image.new("RGB", im.size, col), (0, 0), mask)
            dr.line([tp(p) for p in d["pts"]] + [tp(d["pts"][0])], fill=(0, 0, 0), width=1)
            for hole in d["holes"]:
                dr.line([tp(p) for p in hole] + [tp(hole[0])], fill=(0, 0, 0), width=1)
        else:
            dr.polygon([tp(p) for p in d["pts"]], fill=col, outline=(0, 0, 0))
    if title:
        dr.text((4, 3), title, fill=(0, 0, 0))
    im.save(path)
    return w, h + top


def render_profiles(prof, path, scale=6.0):
    from PIL import Image, ImageDraw
    items = list(prof.items())
    cells = []
    for name, pts in items:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        w, h = (max(xs) - min(xs)), (max(ys) - min(ys))
        s = min(scale, 260.0 / max(w, 1e-6), 260.0 / max(h, 1e-6))
        cells.append((name, pts, min(xs), min(ys), max(ys), s, int(w * s) + 24, int(h * s) + 36))
    W = max(c[6] for c in cells) * 2 + 40
    rows = (len(cells) + 1) // 2
    H = sum(max(cells[i][7], cells[i + 1][7] if i + 1 < len(cells) else 0) for i in range(0, len(cells), 2)) + 20 * rows
    im = Image.new("RGB", (W, H), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    y = 10
    for i in range(0, len(cells), 2):
        rh = 0
        for j in (0, 1):
            if i + j >= len(cells):
                continue
            name, pts, mx, my0, my1, s, cw, ch = cells[i + j]
            ox = 12 + j * (W // 2)
            dr.text((ox, y), name[:70], fill=(0, 0, 0))
            dr.polygon([((p[0] - mx) * s + ox, (my1 - p[1]) * s + y + 16) for p in pts], fill=(214, 200, 190), outline=(0, 0, 0))
            rh = max(rh, ch)
        y += rh + 20
    im.save(path)


def overlay_on_photo(T, photo_path, out_path, long_side=1200):
    """The drawing's edges laid on photograph P1 at the scale fitted on its visible width only."""
    from PIL import Image, ImageDraw
    P = T
    c = consts(P)
    ph = T["photo"]["P1"]["scale"]
    s = ph["mm_per_px"]
    ax, ox = ph["x_anchor_px_at_opening_centre_x_mm"]
    zr, z0 = ph["z_anchor_row_at_z_mm"]
    im = Image.open(photo_path).convert("RGB")
    k = long_side / max(im.size)
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    dr = ImageDraw.Draw(im)

    def tp(p):
        return ((ax + (p[0] - ox) / s) * k, (zr - (p[1] - z0) / s) * k)
    colours = {"moulding": (255, 220, 0), "frame": (0, 220, 255), "glass": (80, 160, 255), "leaf": (255, 255, 255), "iron": (255, 0, 255), "buff": (0, 255, 120), "stone": (255, 140, 0), "panel": (255, 120, 120)}
    for d in elevation(P):
        if d["layer"] in ("brick",) and not d["name"].startswith("plinth"):
            continue
        col = colours.get(d["layer"], (255, 255, 255))
        if d["name"].startswith("quoin"):
            col = (0, 200, 90)
        pts = [tp(p) for p in d["pts"]]
        dr.line(pts + [pts[0]], fill=col, width=1)
        for hole in d.get("holes", []):
            hp = [tp(p) for p in hole]
            dr.line(hp + [hp[0]], fill=col, width=1)
    # a plain key
    y = 6
    for nm, col in (("mouldings, band, weatherboard", colours["moulding"]), ("frame, transom, beads", colours["frame"]), ("ironmongery", colours["iron"]),
                    ("arch, quoins and plinth", colours["buff"]), ("step (door-plane scale: the stone, nearer, reads wider)", colours["stone"])):
        dr.rectangle([6, y, 16, y + 8], fill=col)
        dr.text((22, y - 1), nm, fill=(255, 255, 255))
        y += 13
    for q in (85, 75, 65, 55):
        im.save(out_path, quality=q, optimize=True)
        if Path(out_path).stat().st_size < 300 * 1024:
            break
    return im.size


# ---------------------------------------------------------------- command line
def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    out = Path(argv[1])
    out.mkdir(parents=True, exist_ok=True)
    variant = None
    overlay = None
    i = 2
    while i < len(argv):
        if argv[i] == "--variant":
            variant = argv[i + 1]
            i += 2
        elif argv[i] == "--overlay":
            overlay = (argv[i + 1], argv[i + 2])
            i += 3
        else:
            i += 1
    T = load()
    names = [None] + [v for v in T["variants"] if "parts" in T["variants"][v]]
    docs = {}
    for v in ([variant] if variant else names):
        doc = all_drawings(T, v)
        docs[v or T["default_variant"]] = doc
        tag = (v or T["default_variant"])
        (out / f"target_drawings_{tag}.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
        P = parts(T, v)
        c = consts(P)
        info = {}
        info["elevation"] = render(doc["elevation"]["polygons"], out / f"elevation_{tag}.png", 0.8, True, bounds_layers=("frame", "glass", "leaf", "panel", "moulding", "stone", "buff", "iron"), title=f"{tag}: elevation (0.8 px/mm)")
        for key in ("section_h", "section_h_lock", "section_h_band", "section_h_plate", "section_h_transom"):
            if key in doc:
                info[key] = render(doc[key]["polygons"], out / f"{key}_{tag}.png", 2.0, False, title=f"{tag}: {key} at z={doc[key]['cut_z_mm']}")
        info["section_v"] = render(doc["section_v"]["polygons"], out / f"section_v_{tag}.png", 0.8, True, title=f"{tag}: section_v at x={doc['section_v']['cut_x_mm']}")
        info["section_v_muntin"] = render(doc["section_v_muntin"]["polygons"], out / f"section_v_muntin_{tag}.png", 0.8, True, title=f"{tag}: section_v_muntin at x={doc['section_v_muntin']['cut_x_mm']}")
        info["plan"] = render(doc["plan"]["polygons"], out / f"plan_{tag}.png", 0.8, False, title=f"{tag}: plan")
        if "section_v_plinth" in doc:
            info["section_v_plinth"] = render(doc["section_v_plinth"]["polygons"], out / f"section_v_plinth_{tag}.png", 1.0, True, title=f"{tag}: section_v_plinth at x={doc['section_v_plinth']['cut_x_mm']}")
        render_profiles(doc["profiles"], out / f"profiles_{tag}.png")
        info["furniture"] = render(doc["furniture"]["polygons"], out / f"furniture_{tag}.png", 3.0, True, title=f"{tag}: furniture")
        print(tag, {k: v_ for k, v_ in info.items()})
    # the builder's check reads target_drawings.json: the default variant's set
    (out / "target_drawings.json").write_text(json.dumps(docs[T["default_variant"]] if T["default_variant"] in docs else list(docs.values())[0], indent=1), encoding="utf-8")
    if overlay:
        print("overlay", overlay_on_photo(T, overlay[0], overlay[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
