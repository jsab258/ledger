"""The door furniture of the front-doors-all kit: the target's 28 variants as separate parts (plus the stacked form of NM1), each its own .glb.

Every variant is built in millimetres in its own frame and written in metres: the origin is the fitting's mounting point on the leaf's face (the bell push: on the
jamb's stop face; the scraper: on the ground against the wall), x across as seen from the street, z up, y into the wall (the street toward -y, so a fitting
stands at negative y), scale 1. A fitting stands 0.4 mm INTO the face it sits on and carries what it needs (a plate its own dark liner), so no leaf is cut for
it and no two faces are coplanar. Which house gets which variant, and where (the mount point in the kind's own frame), is data: doors_street.py, houses.json.
A lever is built pointing +x (toward the middle of a left-locking door); houses.json says mirror_x for the others.

Reserve variants (LP3, KN1, KN2, BL2, NM2, NM4, NM5) are built and placed nowhere; KN3 (lion's head) is not offered by the target and is not built.
Digits are a small stroke font of the kit's own (no real typeface); the digit strings are placeholders the town assigns (see houses.json "numbers").
"""
import json
import math
import os
import sys

import numpy as np
from shapely.geometry import LineString, Point, Polygon
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doors_lib as L  # noqa: E402
from doors_lib import bd  # noqa: E402

import bpy  # noqa: E402
from mathutils import Matrix  # noqa: E402

# placeholder numbers (the town's to assign; none is canon): the forms are the target's, the digits are not
NUMBERS = {"NM1:T1": "34", "NM1:F2": "246", "NM6:T2": "21", "NM3:F3": "15"}


def srgb(c):
    return [int(round(v)) for v in c]


def make_mats(N):
    F = N["furniture"]
    return {
        "brass": bd.make_material("brass", F["letter_plate"]["LP1"]["srgb"], 0.4, 1.0),
        "chrome_nickel": bd.make_material("chrome_nickel", [170, 170, 168], 0.35, 1.0),
        "steel_dark": bd.make_material("steel_dark", [40, 40, 42], 0.6, 1.0),
        "cast_iron": bd.make_material("cast_iron", [30, 30, 32], 0.65, 1.0),
        "aluminium_pale": bd.make_material("aluminium_pale", [190, 190, 185], 0.45, 1.0),
        "plastic_white": bd.make_material("plastic_white", [226, 224, 214], 0.4, 0.0),
        "paint_numeral_white": bd.make_material("paint_numeral_white", [226, 224, 214], 0.35, 0.0),
        "paint_black": bd.make_material("paint_black", [35, 36, 40], 0.35, 0.0),
        "slot_interior": bd.make_material("slot_interior", [12, 12, 12], 0.95, 0.0),
        "plastic_dark_grey": bd.make_material("plastic_dark_grey", [60, 60, 62], 0.6, 0.0),
        "plastic_dark": bd.make_material("plastic_dark", [42, 40, 38], 0.5, 0.0),
        "plastic_pale": bd.make_material("plastic_pale", [200, 196, 184], 0.5, 0.0),
    }


class PartSet:
    """The parts of one variant: created now (so booleans can follow), finished (bevel, metres, UVs, shading, materials) at the end."""

    def __init__(self, name, mats):
        self.name, self.mats, self.objs = name, mats, []

    def add(self, name, V, F, mat, bev=None):
        ob = bd.new_obj(name, V, F)
        self.objs.append({"ob": ob, "mat": mat, "bev": bev})
        return ob

    def finish(self):
        M = Matrix.Scale(0.001, 4)
        out = []
        for d in self.objs:
            ob = d["ob"]
            if d["bev"]:
                w, pred, seg = d["bev"]
                bd.bevel(ob, w, pred, 30.0, seg)
            me = ob.data
            me.transform(M)
            me.update()
            bd.box_uv(me)
            me.shade_smooth()
            me.set_sharp_from_angle(angle=math.radians(35.0))
            me.materials.clear()
            me.materials.append(self.mats[d["mat"]])
            out.append(ob)
        return out


# ------------------------------------------------------------------ shared shapes
def rrect(cx, cz, w, h, r=1.0, n=3):
    pts = []
    for (ax, az, a0) in ((cx + w / 2 - r, cz + h / 2 - r, 0), (cx - w / 2 + r, cz + h / 2 - r, 90), (cx - w / 2 + r, cz - h / 2 + r, 180), (cx + w / 2 - r, cz - h / 2 + r, 270)):
        pts += L.arc_pts(ax, az, r, a0, a0 + 90, n)
    return L.dedupe(pts)


def lathe_y(profile, nseg=40, ox=0.0, oz=0.0):
    """A solid of revolution whose axis is along -y (proud toward the street): profile (r, s) with s proud of the face (negative = into the leaf)."""
    V, F = bd.lathe(profile, nseg)
    return bd.place_axis_y(V, ox, 0.0, oz), F


def concat(parts):
    Vs, Fs, off = [], [], 0
    for V, F in parts:
        Vs.append(np.asarray(V, float))
        Fs += [tuple(i + off for i in f) for f in F]
        off += len(V)
    return np.vstack(Vs), Fs


def torus_y(R, r, nu=48, nv=10, cx=0.0, cz=0.0, y=0.0):
    """A ring in the x-z plane (a knocker's ring), major radius R, tube radius r, centre (cx, y, cz)."""
    V = []
    for i in range(nu):
        a = 2 * math.pi * i / nu
        for j in range(nv):
            b = 2 * math.pi * j / nv
            rr = R + r * math.cos(b)
            V.append((cx + rr * math.cos(a), y + r * math.sin(b), cz + rr * math.sin(a)))
    F = []
    for i in range(nu):
        i1 = (i + 1) % nu
        for j in range(nv):
            j1 = (j + 1) % nv
            F.append((i * nv + j, i1 * nv + j, i1 * nv + j1, i * nv + j1))
    return np.array(V, float), F


# ------------------------------------------------------------------ letter plates
def plate_rim(ps, d, mat, aperture_top_margin, bosses=None):
    """A framed plate with a raised, 45 degree chamfered rim round a sprung flap (3.1 as built): outer w x h, aperture aw x ah, backplate bt, rim proud rp."""
    w, h = d["outer"]
    aw, ah = d["aperture"]
    bt, rp = d["backplate_t"], d["rim_proud"]
    ch = rp - bt
    yb = 0.4
    ztop, zbot = h / 2, -h / 2
    ztop_ap = ztop - aperture_top_margin
    zbot_ap = ztop_ap - ah
    rings = [bd.rect_ring(-w / 2, zbot, w / 2, ztop, yb), bd.rect_ring(-w / 2, zbot, w / 2, ztop, -bt),
             bd.rect_ring(-w / 2 + ch, zbot + ch, w / 2 - ch, ztop - ch, -bt - ch), bd.rect_ring(-aw / 2, zbot_ap, aw / 2, ztop_ap, -rp),
             bd.rect_ring(-aw / 2, zbot_ap, aw / 2, ztop_ap, yb)]
    V, F = bd.loft_rings(rings)
    ps.add("iron_letter_plate", V, F, mat)
    # the dark liner behind the flap: 0.3 in front of the leaf's face, so the gaps round the flap and under its lip read as a slot, never as paint
    V, F = bd.box(-aw / 2 + 0.3, -0.5, zbot_ap + 0.3, aw / 2 - 0.3, -0.3, ztop_ap - 0.3)
    ps.add("iron_letter_liner", V, F, "slot_interior")
    fw = aw / 2 - 1.0
    xs_ = [-fw + 2 * fw * i / 12 for i in range(13)]
    front = [(x, -3.5 + 3.0 * (1 - (x / fw) ** 2)) for x in xs_]
    back = [(x, y + 2.6) for x, y in front[::-1]]
    V, F = bd.prism(front + back, ("x", "y"), "z", zbot_ap + 1.0, ztop_ap - 2.0)
    ps.add("iron_letter_flap", V, F, mat)
    sel = [i for i, (x, y) in enumerate(front) if abs(x) <= fw - 0.3]
    front2 = [(front[i][0], front[i][1] - 1.8) for i in sel]
    back2 = [(back[len(back) - 1 - i][0], back[len(back) - 1 - i][1] + 0.3) for i in sel[::-1]]
    V, F = bd.prism(front2 + back2, ("x", "y"), "z", zbot_ap + 0.6, zbot_ap + 5.0)
    ps.add("iron_letter_lip", V, F, mat)
    if bosses:
        r_b, up = 4.0, 2.5
        for sx, tag in ((-1, "l"), (1, "r")):
            cx_, cz_ = sx * (aw / 2 - 6.0), ztop_ap - 4.5
            Vh, Fh = lathe_y([(0.0, -1.0), (r_b, -1.0), (r_b, rp + up - 1.6), (r_b - 1.0, rp + up - 0.6), (r_b - 2.2, rp + up - 0.1), (0.0, rp + up)], 24, cx_, cz_)
            ps.add("iron_plate_pivot_" + tag, Vh, Fh, mat)


def plate_flush(ps, d, mat):
    """An oblong plate (LP4 to LP7): a frame of frame_w standing `proud`, a chamfered outer edge, a letter flap 0.8 in front of a dark liner."""
    w, h = d["outer"]
    fw, pr = d.get("frame_w", 5.0), d["proud"]
    yb = 0.4
    ow, oh = w - 2 * fw, h - 2 * fw
    rings = [bd.rect_ring(-w / 2, -h / 2, w / 2, h / 2, yb), bd.rect_ring(-w / 2, -h / 2, w / 2, h / 2, -(pr - 0.8)),
             bd.rect_ring(-w / 2 + 0.8, -h / 2 + 0.8, w / 2 - 0.8, h / 2 - 0.8, -pr), bd.rect_ring(-ow / 2, -oh / 2, ow / 2, oh / 2, -pr),
             bd.rect_ring(-ow / 2, -oh / 2, ow / 2, oh / 2, yb)]
    V, F = bd.loft_rings(rings)
    ps.add("iron_letter_plate", V, F, mat)
    V, F = bd.box(-ow / 2 + 0.3, -0.5, -oh / 2 + 0.3, ow / 2 - 0.3, -0.3, oh / 2 - 0.3)
    ps.add("iron_letter_liner", V, F, "slot_interior")
    V, F = bd.box(-ow / 2 + 1.2, -(pr - 0.8) + 0.0 - 0.0 + 0.0, -oh / 2 + 1.2, ow / 2 - 1.2, -(pr - 0.8) + 0.8 + 0.0, oh / 2 - 1.2)
    ps.add("iron_letter_flap", V, F, mat)


# ------------------------------------------------------------------ handles
def knob(ps, d):
    rz = [tuple(q) for q in d["profile_rz"]]
    z0 = 1.4                                                                       # the rose's flat centre
    bulb = bd.smooth_open([rz[1]] + [q for q in rz[2:] if q[1] < 58.0] + [(8.0, 58.0), (0.0, 58.0)], l_max=20.0, turn_max=70.0, step=1.6)
    prof0 = [(0.0, -0.4 + z0 - 1.0), (rz[1][0], -0.4 + z0 - 1.0)] + [(r, z + z0) for r, z in bulb]

    def r_at(zq):
        for (ra, za), (rb, zb) in zip(prof0, prof0[1:]):
            if za < zb and za <= zq <= zb:
                return ra + (rb - ra) * (zq - za) / (zb - za)
        return prof0[-1][0]
    rings, hw, depth = (10.0, 19.0, 28.0, 37.0, 46.0), 1.3, 1.5                  # five turned rings, V-cut 1.5 deep
    prof, pending = [], [z + z0 for z in rings]
    for r, z in prof0:
        while pending and z >= pending[0] - hw and z > 5.0 + z0:
            zg = pending.pop(0)
            prof += [(r_at(zg - hw), zg - hw), (r_at(zg) - depth, zg), (r_at(zg + hw), zg + hw)]
        if any(abs(z - (zg + z0)) < hw for zg in rings):
            continue
        prof.append((r, z))
    V, F = lathe_y(prof, 44)
    ps.add("iron_knob", V, F, "paint_black")
    V, F = lathe_y([(0.0, 57.9 + z0), (8.1, 57.9 + z0), (7.2, 59.4 + z0), (4.2, 61.2 + z0), (0.0, 62.0 + z0)], 40)
    ps.add("iron_knob_cap", V, F, "brass")
    V, F = lathe_y([(0.0, -0.4), (38.0, -0.4), (38.0, 1.4), (36.6, 2.0), (32.0, 1.4), (0.0, 1.4)], 48)
    ps.add("iron_knob_rose", V, F, "paint_black")


def lever(ps, d):
    """A lever handle on a round rose, pointing +x: a rose (rose_dia, rose_proud, rounded edge), a neck, and a bar of the lever's length (from the rose's centre)
    and width, 14 deep, standing lever_proud from the face."""
    rr, rpr = d["rose_dia"] / 2.0, d["rose_proud"]
    ln, wd = d["lever"]
    lp = d["lever_proud"]
    V, F = lathe_y([(0.0, -0.4), (rr, -0.4), (rr, rpr - 1.5), (rr - 1.5, rpr), (0.0, rpr)], 40)
    ps.add("iron_rose", V, F, "chrome_nickel")
    V, F = lathe_y([(0.0, rpr - 0.4), (7.0, rpr - 0.4), (7.0, lp - 6.0), (0.0, lp - 6.0)], 24)
    ps.add("iron_neck", V, F, "chrome_nickel")
    cap = LineString([(0.0, 0.0), (ln - wd / 2.0, 0.0)]).buffer(wd / 2.0, resolution=6)
    pts = list(cap.exterior.coords)[:-1]
    V, F = bd.prism(L.ccw(pts), ("x", "z"), "y", -lp, -(lp - 14.0))
    ps.add("iron_lever", V, F, "chrome_nickel", (1.5, None, 1))


def bar_pull(ps, d):
    """HD3: a vertical bar pull on two standoffs (dark steel): 25 x 270, 35 proud."""
    w, h = d["size"]
    pr = d["proud"]
    V, F = bd.prism(rrect(0.0, 0.0, w, h, 8.0, 5), ("x", "z"), "y", -pr, -(pr - 12.0))
    ps.add("iron_pull_bar", V, F, "steel_dark", (1.0, None, 1))
    for z, tag in ((h / 2 - 28.0, "u"), (-h / 2 + 28.0, "l")):
        V, F = lathe_y([(0.0, -0.4), (6.0, -0.4), (6.0, pr - 11.6), (0.0, pr - 11.6)], 20, 0.0, z)
        ps.add("iron_pull_post_" + tag, V, F, "steel_dark")


def thumb_latch(ps, d):
    """HD4: the iron thumb latch of a ledged door: a back plate, a grip bar on two posts, a pressed thumb piece at its head."""
    pw, ph = d["plate"]
    bt = d["plate_t"]
    V, F = bd.prism(rrect(0.0, 0.0, pw, ph, 6.0, 4), ("x", "z"), "y", -bt, 0.4)
    ps.add("iron_latch_plate", V, F, "steel_dark", (0.8, None, 1))
    bw, bh = d["bar"]
    V, F = bd.prism(rrect(0.0, -10.0, bw, bh, 8.0, 4), ("x", "z"), "y", -(bt + 12.0), -(bt + 3.0))
    ps.add("iron_latch_bar", V, F, "steel_dark", (0.8, None, 1))
    for z, tag in ((-10.0 + bh / 2 - 22.0, "u"), (-10.0 - bh / 2 + 22.0, "l")):
        V, F = lathe_y([(0.0, 0.0), (4.0, 0.0), (4.0, bt + 3.5), (0.0, bt + 3.5)], 16, 0.0, z)
        ps.add("iron_latch_post_" + tag, V, F, "steel_dark")
    tw, th = 25.0, 35.0
    V, F = bd.prism(rrect(0.0, ph / 2 - 6.0 - th / 2 + 0.0, tw, th, 8.0, 4), ("x", "z"), "y", -(bt + 9.0), -(bt - 0.4))
    ps.add("iron_latch_thumb", V, F, "steel_dark", (1.0, None, 1))


# ------------------------------------------------------------------ latches (the rim night latch)
def cylinder_plain(ps, d):
    """LK1: a plain collar (the escutcheon), one solid of revolution: collar 43.5, plug 28, standing 5 proud with a 3 mm round, a dark gap ring, a vertical keyway 3 x 9."""
    ro, rpl, proud = d["collar"] / 2, d["plug"] / 2, d["collar_proud"]
    depth = 4.6
    rr = 3.0
    outer = [(ro - rr + rr * math.cos(math.radians(a)), proud - rr + rr * math.sin(math.radians(a))) for a in (90, 75, 60, 45, 30, 15, 0)]
    prof = [(0.0, proud - 0.6), (rpl - 0.4, proud - 0.6), (rpl, proud - 1.0), (rpl, -2.5), (rpl + 0.3, -2.5), (rpl + 0.3, proud - 1.0),
            (rpl + 0.7, proud - 0.3), (rpl + 1.3, proud)] + outer + [(ro, -4.0), (rpl, -4.0), (rpl, -depth), (0.0, -depth)]
    V, F = lathe_y(prof, 56)
    o = ps.add("iron_lock", V, F, "chrome_nickel")
    kw, kh = 3.0, 9.0
    bd.cut(o, *bd.box(-kw / 2, -proud - 1.0, -kh / 2, kw / 2, 2.0, kh / 2))


def cylinder_scalloped(ps, d):
    """LK2: a knurled collar of 8 rounded scallops round a plug 18 across whose face stands 1 behind it; keyway 3 x 9."""
    ro, rpl, proud = d["collar"] / 2, d["plug"] / 2, d["collar_proud"]
    n = int(d.get("scallops", 8))
    lobe_r, lobe_c = 7.0, ro - 7.0
    per = 14
    outer = []
    for i in range(n):
        for k in range(per):
            a = 2 * math.pi * (i + k / per) / n - math.pi / n
            best = 0.0
            for j in (i - 1, i, i + 1):
                aj = 2 * math.pi * j / n
                dl = a - aj
                v = lobe_c * math.cos(dl) + math.sqrt(max(lobe_r ** 2 - (lobe_c * math.sin(dl)) ** 2, 0.0))
                best = max(best, v)
            outer.append((best * math.cos(a), best * math.sin(a)))
    Nn = len(outer)
    inner = [((rpl - 0.3) * math.cos(2 * math.pi * k / Nn), (rpl - 0.3) * math.sin(2 * math.pi * k / Nn)) for k in range(Nn)]
    V, F = bd.Door.ring_prism(outer, inner, -proud, 4.0)
    ps.add("iron_lock_collar", V, F, "chrome_nickel", (1.2, lambda a, b: abs(a.y + proud) < 1e-3 and abs(b.y + proud) < 1e-3, 2))
    V, F = lathe_y([(0.0, -4.6), (rpl, -4.6), (rpl, proud - 1.0 - 0.4), (rpl - 0.4, proud - 1.0), (0.0, proud - 1.0)], 48)
    o = ps.add("iron_lock_plug", V, F, "chrome_nickel")
    kw, kh = 3.0, 9.0
    bd.cut(o, *bd.box(-kw / 2, -proud - 1.0, -kh / 2, kw / 2, 2.0, kh / 2))


def cylinder_bare(ps, d):
    """LK3: a bare dark cylinder face 18 across under the lever, no collar, standing 2 proud, a keyway 2 x 6."""
    r, proud = d["plug"] / 2, d["collar_proud"]
    V, F = lathe_y([(0.0, -2.0), (r, -2.0), (r, proud - 0.6), (r - 0.6, proud), (0.0, proud)], 32)
    o = ps.add("iron_lock", V, F, "steel_dark")
    bd.cut(o, *bd.box(-1.0, -proud - 1.0, -3.0, 1.0, 1.0, 3.0))


# ------------------------------------------------------------------ keyhole, knockers, bells
def keyhole(ps, d):
    """KH1: a plugged mortice keyhole: a round head over a parallel slot, a dark plate 0.8 proud (the target: a recess 2 mm sunk; the leaf is not cut here), a pale blank
    filling the slot, 0.8 higher."""
    from shapely.geometry import Polygon as SPoly
    hd, sw = d["head_dia"], d["slot_w"]
    hh = d["size"][1]
    out = SPoly(bd.Door.keyhole_outline(0.0, 0.0, hd, sw, hh))
    V, F = bd.prism(L.ccw(list(out.buffer(-0.0).exterior.coords)[:-1]), ("x", "z"), "y", -0.8, 0.4)
    ps.add("iron_keyhole_plate", V, F, "steel_dark")
    top = hh / 2 - hd / 2
    foot = -hh / 2 + sw / 2
    blank = LineString([(0.0, top - hd / 2 + 1.5), (0.0, foot)]).buffer((sw - 1.8) / 2, 10, cap_style=1)
    V, F = bd.prism(L.ccw(list(blank.exterior.coords)[:-1]), ("x", "z"), "y", -1.6, -0.5)
    ps.add("iron_keyhole_blank", V, F, "chrome_nickel")


def knocker_ring(ps, d):
    """KN1 (reserve): a ring knocker on a back plate 70 x 110 x 5, a lug, a ring of 95 outside and a 12 tube, a striker button below."""
    pw, ph = d["plate"]
    pt = d["plate_t"]
    V, F = bd.prism(rrect(0.0, 0.0, pw, ph, 22.0, 6), ("x", "z"), "y", -pt, 0.4)
    ps.add("iron_knocker_plate", V, F, "brass", (1.0, None, 1))
    Rr = 95.0 / 2 - 6.0
    V, F = bd.prism(rrect(0.0, ph / 2 - 24.0, 16.0, 22.0, 6.0, 4), ("x", "z"), "y", -(pt + 10.0), -(pt - 0.4))
    ps.add("iron_knocker_lug", V, F, "brass")
    V, F = torus_y(Rr, 6.0, 48, 10, 0.0, ph / 2 - 24.0 - Rr + 4.0, -(pt + 6.0))
    ps.add("iron_knocker_ring", V, F, "brass")
    V, F = lathe_y([(0.0, 0.0), (11.0, 0.0), (11.0, pt + 3.0), (7.0, pt + 9.0), (0.0, pt + 11.0)], 24, 0.0, -ph / 2 + 14.0)
    ps.add("iron_knocker_striker", V, F, "brass")


def knocker_bar(ps, d):
    """KN2 (reserve): a plain bar knocker 150 x 30 on two lugs, a striker plate below."""
    bw, bh = d["size"]
    V, F = bd.prism(rrect(0.0, 0.0, bw, bh, 8.0, 4), ("x", "z"), "y", -34.0, -20.0)
    ps.add("iron_knocker_bar", V, F, "brass", (1.0, None, 1))
    for sx, tag in ((-1, "l"), (1, "r")):
        V, F = lathe_y([(0.0, -0.4), (9.0, -0.4), (9.0, 21.0), (0.0, 21.0)], 20, sx * (bw / 2 - 18.0), 0.0)
        ps.add("iron_knocker_lug_" + tag, V, F, "brass")
    V, F = bd.prism(rrect(0.0, -42.0, 60.0, 34.0, 6.0, 3), ("x", "z"), "y", -6.0, 0.4)
    ps.add("iron_knocker_strike", V, F, "brass", (0.8, None, 1))


def bell_push(ps, d):
    """BL1: ONE plain dark oblong, 22 x 72.6, square-cornered (r 1), 3 proud of the stop's face, with a groove 14 x 2 x 1 a little (8 mm) below its middle. Mounted on the
    jamb's stop face (the origin is its centre on that face). The first build's bezel and button are gone (the handover's fix)."""
    w, h = d["size"]
    g = d["groove"]
    r = d["corner_r"]
    pts = []
    for (cx_, cz_, a0) in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        pts += L.arc_pts(cx_, cz_, r, a0, a0 + 90, 3)
    V, F = bd.prism(pts, ("x", "z"), "y", -d["proud"], 0.4)
    ob = ps.add("iron_bellpush", V, F, "plastic_dark_grey")
    zg = -g["below_centre"]
    bd.cut(ob, *bd.box(-g["w"] / 2, -d["proud"] - 1.0, zg - g["h"] / 2, g["w"] / 2, -d["proud"] + g["depth"], zg + g["h"] / 2))


def bell_pull(ps, d):
    """BL2 (reserve): an old brass bell pull, ONE part: a small round plate, a rod 12 across and 90 long standing out from it, a turned knob 40 across at its end."""
    kn = d["knob"][0]
    rod_d, rod_l = d["rod"]
    pieces = []
    pieces.append(lathe_y([(0.0, -0.4), (30.0, -0.4), (30.0, 3.0), (27.0, 4.0), (0.0, 4.0)], 40))
    pieces.append(lathe_y([(0.0, 3.0), (rod_d / 2, 3.0), (rod_d / 2, rod_l - 8.0), (0.0, rod_l - 8.0)], 20))
    prof = [(0.0, rod_l - 12.0), (kn / 2 - 6.0, rod_l - 12.0), (kn / 2, rod_l - 4.0)] + [(kn / 2 * math.cos(math.radians(a)), rod_l - 4.0 + kn / 2 * math.sin(math.radians(a))) for a in (15, 30, 45, 60, 75, 90)]
    pieces.append(lathe_y(prof, 32))
    objs = [bd.new_obj("_p", V, F) for V, F in pieces]
    ob = bd.unite_objs("iron_bellpull", objs)
    ps.objs.append({"ob": ob, "mat": "brass", "bev": None})


# ------------------------------------------------------------------ numbers and the plaque
def number_part(ps, d, text, w, h, stroke, gap, relief, mat, stacked_z=None, name="iron_numerals", on_glass=False):
    """A row (or a stack) of digits as one solid: each digit's strokes are capsule prisms united by boolean; `relief` proud, 0.4 into the face."""
    r = stroke / 2.0
    if stacked_z is not None:
        centres = [(0.0, z) for z in stacked_z]
    else:
        n = len(text)
        total = n * w + (n - 1) * gap
        x = -total / 2.0 + w / 2.0
        centres = []
        for _ in text:
            centres.append((x, 0.0))
            x += w + gap
    objs = []
    for ch, (cx, cz) in zip(text, centres):
        for line in L._G[ch]:
            pts = [(cx - w / 2.0 + r + px * (w - 2 * r), cz - h / 2.0 + r + py * (h - 2 * r)) for px, py in line]
            for p0, p1 in zip(pts[:-1], pts[1:]):
                cap = LineString([p0, p1]).buffer(r, resolution=3, cap_style=1)
                V, F = bd.prism(L.ccw(list(cap.exterior.coords)[:-1]), ("x", "z"), "y", -relief, 0.4)
                objs.append(bd.new_obj("_stroke", V, F))
    ob = bd.unite_objs(name, objs)
    ps.objs.append({"ob": ob, "mat": mat, "bev": None})


def plaque_oval(ps, d):
    """NM5 (reserve): an oval plaque 230 x 154, dark moulded plastic with a pale rim and a plain relief ornament (no digits)."""
    a, b = d["size"][0] / 2, d["size"][1] / 2
    n = 48
    oval = [(a * math.cos(2 * math.pi * k / n), b * math.sin(2 * math.pi * k / n)) for k in range(n)]
    V, F = bd.prism(oval, ("x", "z"), "y", -8.0, 0.4)
    ps.add("plaque_body", V, F, "plastic_dark", (1.0, None, 1))
    rim_o = L.offset_poly(oval, 0.0)
    rim_i = L.offset_poly(oval, 9.0)
    V, F = bd.Door.ring_prism(rim_o, rim_i, -10.0, -7.6)
    ps.add("plaque_rim", V, F, "plastic_pale")
    orn = [(0.55 * a * math.cos(2 * math.pi * k / 32), 0.45 * b * math.sin(2 * math.pi * k / 32)) for k in range(32)]
    V, F = bd.prism(orn, ("x", "z"), "y", -10.4, -7.6)
    ps.add("plaque_ornament", V, F, "plastic_pale", (0.8, None, 1))


# ------------------------------------------------------------------ the boot scraper
def scraper(ps, d):
    """BS1: a cast-iron boot scraper (Judgement from D10): a straight blade 300 x 25 x 12 with a notched underside between two end standards 200 high
    (the target's point list standard_profile_xz, mirrored for the other end), each on a foot running back to the wall. Origin: its centre on the ground at the wall; y runs
    toward the street (negative). The standards stand 140 either side of the centre so the whole is 330 long."""
    prof = [tuple(q) for q in d["standard_profile_xz"]]
    th = d["blade_thickness"]
    depth = d["size"][1]
    xo = 140.0
    zb0, zb1 = 110.0, 135.0                                         # the blade's height: 25 on edge
    for sx, tag in ((-1, "l"), (1, "r")):
        pts = [(sx * (xo + x), z) for x, z in prof]
        pts = L.ccw(pts)
        V, F = bd.prism(pts, ("x", "z"), "y", -(depth / 2 + th / 2), -(depth / 2 - th / 2))
        ps.add("iron_scraper_standard_" + tag, V, F, "cast_iron", (0.8, None, 1))
        V, F = bd.box(sx * (xo + 12.5) - 11.7, -depth, 0.4, sx * (xo + 12.5) + 11.7, 0.4, th + 0.4)       # the foot, 23.4 wide (no face shared with the standard), running back to the wall
        ps.add("iron_scraper_foot_" + tag, V, F, "cast_iron")
    bl = d["blade"][0]
    nt = d["blade_underside_notch"]
    pts = [(-bl / 2, zb0), (-nt["length_at_underside"] / 2, zb0), (-nt["length_at_top"] / 2, zb0 + nt["depth"]), (nt["length_at_top"] / 2, zb0 + nt["depth"]),
           (nt["length_at_underside"] / 2, zb0), (bl / 2, zb0), (bl / 2, zb1), (-bl / 2, zb1)]
    V, F = bd.prism(L.ccw(pts), ("x", "z"), "y", -(depth / 2 + th / 2 - 0.6), -(depth / 2 - th / 2 + 0.6))       # 0.6 thinner each side than the standards: no face shared with them
    ps.add("iron_scraper_blade", V, F, "cast_iron", (0.8, None, 1))


# ------------------------------------------------------------------ the catalogue
def variant_builders(N):
    """{id: callable(ps)} for every variant the kit builds, from the target's own rows."""
    F = N["furniture"]
    B = {}
    lp = F["letter_plate"]
    B["LP1"] = lambda ps: plate_rim(ps, lp["LP1"], "brass", 22.0)
    B["LP2"] = lambda ps: plate_rim(ps, lp["LP2"], "brass", 15.0, bosses=True)
    B["LP3"] = lambda ps: plate_rim(ps, lp["LP3"], "cast_iron", 15.0)
    B["LP4"] = lambda ps: plate_flush(ps, lp["LP4"], "chrome_nickel")
    B["LP5"] = lambda ps: plate_flush(ps, lp["LP5"], "aluminium_pale")
    B["LP6"] = lambda ps: plate_flush(ps, lp["LP6"], "plastic_white")
    B["LP7"] = lambda ps: plate_flush(ps, lp["LP7"], "aluminium_pale")
    hd = F["handle"]
    B["HD1"] = lambda ps: knob(ps, hd["HD1"])
    for k in ("HD2a", "HD2b", "HD2c"):
        B[k] = (lambda kk: (lambda ps: lever(ps, hd[kk])))(k)
    B["HD3"] = lambda ps: bar_pull(ps, hd["HD3"])
    B["HD4"] = lambda ps: thumb_latch(ps, hd["HD4"])
    lk = F["latch"]
    B["LK1"] = lambda ps: cylinder_plain(ps, lk["LK1"])
    B["LK2"] = lambda ps: cylinder_scalloped(ps, lk["LK2"])
    B["LK3"] = lambda ps: cylinder_bare(ps, lk["LK3"])
    B["KH1"] = lambda ps: keyhole(ps, F["keyhole"]["KH1"])
    B["KN1"] = lambda ps: knocker_ring(ps, F["knocker"]["KN1"])
    B["KN2"] = lambda ps: knocker_bar(ps, F["knocker"]["KN2"])
    B["BL1"] = lambda ps: bell_push(ps, F["bell"]["BL1"])
    B["BL2"] = lambda ps: bell_pull(ps, F["bell"]["BL2"])
    nm = F["number"]

    def nm_row(vid, text, mat):
        d = nm[vid]
        w, h = d["digit"]
        return lambda ps: number_part(ps, d, text, w, h, d["stroke"], d.get("gap", 12.0), d.get("relief", 3.0), mat)
    B["NM1"] = nm_row("NM1", NUMBERS["NM1:F2"], "brass")
    d = nm["NM1"]
    # T1's form (3.1: P1 stacks two digits 39 x 72 on the muntin, v 1207 to 1277.6 and 1300 to 1373): the first digit above the second, the pair's middle at v 1290
    zlo, zhi = 0.5 * (1207.0 + 1277.6), 0.5 * (1300.0 + 1373.0)
    zmid = 0.5 * (1207.0 + 1373.0)
    B["NM1_stacked"] = lambda ps: number_part(ps, d, NUMBERS["NM1:T1"], 39.0, 72.0, 7.0, 22.0, 3.0, "brass", stacked_z=[zhi - zmid, zlo - zmid])
    B["NM2"] = nm_row("NM2", "46", "cast_iron")
    dd = nm["NM3"]
    B["NM3"] = lambda ps: number_part(ps, dd, NUMBERS["NM3:F3"], 38.0, dd["digit_h"], dd["stroke"], 14.0, 0.3, "paint_numeral_white")
    d4 = nm["NM4"]
    B["NM4"] = lambda ps: number_part(ps, d4, "12", 56.0, d4["digit_h"], d4["stroke"], 18.0, 0.3, "paint_numeral_white")
    B["NM5"] = lambda ps: plaque_oval(ps, nm["NM5"])
    d6 = nm["NM6"]
    B["NM6"] = lambda ps: number_part(ps, d6, NUMBERS["NM6:T2"], d6["digit"][0], d6["digit"][1], d6["stroke"], d6["gap"], d6["relief"], "steel_dark")
    B["BS1"] = lambda ps: scraper(ps, F["scraper"]["BS1"])
    return B


def build_variant(N, vid, out_dir, npz_dir):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats = make_mats(N)
    ps = PartSet(vid, mats)
    variant_builders(N)[vid](ps)
    obs = ps.finish()
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(npz_dir, exist_ok=True)
    glb = os.path.join(out_dir, vid + ".glb")
    npz = os.path.join(npz_dir, "furniture_%s.npz" % vid)
    bd.blender_parts.export(obs, npz)
    bd.export_glb(glb)
    return {"id": vid, "glb": glb, "glb_bytes": os.path.getsize(glb), "triangles": bd.tri_count(obs), "parts": sorted(o.name for o in obs),
            "materials": sorted({o.data.materials[0].name for o in obs})}
