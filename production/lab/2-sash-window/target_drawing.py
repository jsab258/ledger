"""The sash window's target, drawn in 2D straight from target.json's numbers,
the way a joinery manual draws it: an elevation from outside, a vertical section
and a horizontal section. This is the reference the Blender model is checked
against; it never reads the model or the model's code.

Axes (metres): x across the window, 0 at its centre, + to the right seen from
outside; y into the house, 0 at the brick face; z up, 0 at the top of the stone
sill (the bottom of the brick opening).

    python target_drawing.py            # writes target_*.png and target.npz to BUILD on F:
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = r"F:/LedgerTools/lab/sash/build"   # pictures and arrays stay off git (tools/git-size-guard.py)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from outline import Frame  # noqa: E402

MM = 0.001


def load_target(path=os.path.join(HERE, "target.json")):
    return json.load(open(path))


def member_section(u_outer, u_glass, v_out, v_in, rebate_w, rebate_d, ovolo_r, n=6):
    """A sash member cut across (Ellis p.127): from its outer edge u_outer to its glass edge u_glass
    (u is across the member, either direction), v from the outside face v_out to the inside face
    v_in. A glass rebate rebate_w by rebate_d on the outside face at the glass edge; an ovolo of
    radius ovolo_r on the inside arris at the glass edge. Returns the polygon (u, v)."""
    sgn = 1.0 if u_glass > u_outer else -1.0
    ug = u_glass
    P = [(u_outer, v_out), (ug - sgn * rebate_w, v_out), (ug - sgn * rebate_w, v_out + rebate_d), (ug, v_out + rebate_d),
         (ug, v_in - ovolo_r)]
    for k in range(1, n + 1):                       # quarter round from the glass face to the inside face
        a = (math.pi / 2) * k / n
        P.append((ug - sgn * ovolo_r * (1 - math.cos(a)), v_in - ovolo_r * (1 - math.sin(a))))
    P += [(u_outer, v_in)]
    return P


def bar_section(u_mid, half_w, v_out, v_in, rebate_w, rebate_d, ovolo_r, n=6):
    """A glazing bar: rebated for glass on both sides outside, ovolo both arrises inside."""
    a = member_section(u_mid, u_mid + half_w, v_out, v_in, rebate_w, rebate_d, ovolo_r, n)
    b = member_section(u_mid, u_mid - half_w, v_out, v_in, rebate_w, rebate_d, ovolo_r, n)
    return a[1:-1] + b[1:-1][::-1]


def members(T):
    """The window as the manual draws it: a list of (name, kind, polygon) in
    the three drawings. kind: 'elev' (x, z), 'vsec' (y, z) at the drawing's
    section x, 'hsec' (x, y) at the drawing's section z.
    """
    o, f, s = T["opening"], T["frame"], T["sash"]
    W, H = o["width_mm"] * MM, o["height_mm"] * MM
    H_ = H
    R = f["reveal_mm"] * MM                       # brick face to outer lining face
    m = f["outer_lining_margin_mm"] * MM          # outer lining showing inside the brick reveal
    ol_t = f["outer_lining_thickness_mm"] * MM
    stop = f["outer_lining_projection_mm"] * MM   # outer lining past the pulley stile face (outer stop)
    ps_t = f["pulley_stile_thickness_mm"] * MM
    pb_w = f["parting_bead_width_mm"] * MM
    pb_e = f["parting_bead_projection_mm"] * MM
    sb_w = f["staff_bead_width_mm"] * MM          # across the frame face (y)
    sb_e = f["staff_bead_projection_mm"] * MM     # standing out from the inner lining (x)
    il_t = f["inner_lining_thickness_mm"] * MM
    il_w = f["inner_lining_width_mm"] * MM
    ts = s["thickness_mm"] * MM
    clr = s.get("clearance_mm", 2) * MM
    st = s["stile_width_mm"] * MM
    tr = s["top_rail_mm"] * MM
    br = s["bottom_rail_mm"] * MM
    mr = s["meeting_rail_depth_mm"] * MM
    horn = s["horn_length_mm"] * MM
    bar = s["glazing_bar_width_mm"] * MM
    sill = T["sill"]
    sill_h = sill["height_at_front_mm"] * MM      # oak sill's visible height above the stone, at its front
    sill_d = sill["projection_mm"] * MM           # oak sill's nose in front of the outer lining
    head_h = f["head_visible_mm"] * MM            # head lining showing below the brick head, from outside

    # x: the visible clear width between outer linings, and the pulley stile faces
    x_ol = W / 2 - m                    # outer lining's inner edge
    x_ps = x_ol + stop                  # pulley stile face (sash edges run here)
    # y: the tracks
    y_ol0, y_ol1 = R, R + ol_t
    y_up0 = y_ol1 + clr                 # upper (outer) sash
    y_up1 = y_up0 + ts
    y_pb0 = y_up1 + clr
    y_pb1 = y_pb0 + pb_w
    y_lo0 = y_pb1 + clr                 # lower (inner) sash
    y_lo1 = y_lo0 + ts
    y_sb0 = y_lo1 + clr
    y_sb1 = y_sb0 + sb_w
    y_il1 = y_sb1 - il_t      # the inside lining under the staff bead, its room face flush with the bead's (Ellis Fig. 400)
    # z: the sashes closed
    z_sill = sill_h                     # where the lower sash's bottom rail sits (front edge of the oak sill)
    z_head = H - head_h + head_h        # frame head's underside = brick head (head lining hidden)
    z_top_clear = H - head_h            # clear light top, seen from outside
    sash_h = (z_top_clear + stop - z_sill + mr) / 2   # equal sashes overlapping by one meeting rail
    z_lo0, z_lo1 = z_sill, z_sill + sash_h
    z_up1 = z_top_clear + stop
    z_up0 = z_up1 - sash_h

    E = []

    def rect(kind, name, a0, b0, a1, b1):
        E.append((name, kind, [(a0, b0), (a1, b0), (a1, b1), (a0, b1)]))

    # ---- elevation, joinery seen from outside (x, z) -----------------------
    rect("elev", "outer_lining_L", -W / 2, z_sill, -x_ol, H)
    rect("elev", "outer_lining_R", x_ol, z_sill, W / 2, H)
    rect("elev", "head", -W / 2, z_top_clear, W / 2, H)
    rect("elev", "oak_sill", -W / 2, 0.0, W / 2, z_sill)
    for nm, z0, z1, top_rail, bot_rail in (("upper", z_up0, z_up1, tr, mr), ("lower", z_lo0, z_lo1, mr, br)):
        rect("elev", nm + "_stile_L", -x_ps, z0, -x_ps + st, z1)
        rect("elev", nm + "_stile_R", x_ps - st, z0, x_ps, z1)
        rect("elev", nm + "_top_rail", -x_ps, z1 - top_rail, x_ps, z1)
        rect("elev", nm + "_bottom_rail", -x_ps, z0, x_ps, z0 + bot_rail)
        if s.get("panes_per_sash", 1) == 2:
            rect("elev", nm + "_bar", -bar / 2, z0, bar / 2, z1)
    rect("elev", "horn_L", -x_ps, z_up0 - horn, -x_ps + st, z_up0)
    rect("elev", "horn_R", x_ps - st, z_up0 - horn, x_ps, z_up0)

    # ---- vertical section at x = a quarter of the width (y, z) ------------
    # sashes' rails cut across their thickness; the stone below and the brick are not joinery.
    ex = s.get("meeting_rail_extra_thickness_mm", 0) * MM
    for nm, z0, z1, top_rail, bot_rail, y0, y1 in (("upper", z_up0, z_up1, tr, mr, y_up0, y_up1),
                                                   ("lower", z_lo0, z_lo1, mr, br, y_lo0, y_lo1)):
        # the meeting rails are 3/8 in thicker than the stiles, into the parting bead's gap
        ty0, ty1 = (y0, y1) if nm == "upper" else (y0 - ex, y1)
        by0, by1 = (y0, y1 + ex) if nm == "upper" else (y0, y1)
        rw_, rd_, ov_ = s["rebate_width_mm"] * MM, s["rebate_depth_mm"] * MM, s["ovolo_radius_mm"] * MM
        top = member_section(z1, z1 - top_rail, y0, y1, rw_, rd_, ov_)          # glass below a top rail
        bot = member_section(z0, z0 + bot_rail, y0, y1, rw_, rd_, ov_)          # glass above a bottom rail
        E.append((nm + "_top_rail", "vsec", [(v if abs(v - y0) > 1e-9 else ty0, u) for u, v in top]))
        E.append((nm + "_bottom_rail", "vsec", [(v if abs(v - y1) > 1e-9 else by1, u) for u, v in bot]))
    rect("vsec", "head_outer_lining", y_ol0, z_top_clear, y_ol1, H)
    head_t = f.get("head_thickness_mm", 31.8) * MM                       # 'H', 1 1/4 in, Fig. 399
    rect("vsec", "head", y_ol1, z_up1, y_il1, z_up1 + head_t)
    rect("vsec", "head_parting_bead", y_pb0, z_up1 - pb_e, y_pb1, z_up1)
    rect("vsec", "head_staff_bead", y_sb0, z_up1 - sb_e, y_sb1, z_up1)
    # oak sill: weathered top falling outward from under the lower sash to its nose
    y_nose = R - sill_d
    y_back = y_sb1
    E.append(("oak_sill", "vsec", [(y_nose, 0.0), (y_back, 0.0), (y_back, z_sill + sill["upstand_mm"] * MM),
                                   (y_lo0, z_sill + sill["upstand_mm"] * MM), (y_lo0, z_sill), (y_nose, z_sill - sill["fall_mm"] * MM)]))

    # ---- horizontal section through the lower sash's middle (x, y) ---------
    for side in (-1, 1):
        def r(name, xa, ya, xb, yb):
            rect("hsec", name, min(side * xa, side * xb), ya, max(side * xa, side * xb), yb)
        r("outer_lining_" + ("L" if side < 0 else "R"), x_ol, y_ol0, x_ol + f["outer_lining_width_mm"] * MM, y_ol1)
        r("pulley_stile_" + ("L" if side < 0 else "R"), x_ps, y_ol1, x_ps + ps_t, y_il1)
        r("parting_bead_" + ("L" if side < 0 else "R"), x_ps - pb_e, y_pb0, x_ps, y_pb1)
        r("staff_bead_" + ("L" if side < 0 else "R"), x_ps - sb_e, y_sb0, x_ps, y_sb1)
        r("inner_lining_" + ("L" if side < 0 else "R"), x_ps, y_il1, x_ps + il_w, y_sb1)
        rw_, rd_, ov_ = s["rebate_width_mm"] * MM, s["rebate_depth_mm"] * MM, s["ovolo_radius_mm"] * MM
        E.append(("lower_stile_" + ("L" if side < 0 else "R"), "hsec",
                  member_section(side * x_ps, side * (x_ps - st), y_lo0, y_lo1, rw_, rd_, ov_)))
    if s.get("panes_per_sash", 1) == 2:
        E.append(("lower_bar", "hsec", bar_section(0.0, bar / 2, y_lo0, y_lo1, rw_, rd_, ov_)))

    # ---- vertical section through the stiles (y, z): the horn below the upper sash ------
    rect("vsec_stile", "upper_stile", y_up0, z_up0, y_up1, z_up1)
    rect("vsec_stile", "lower_stile", y_lo0, z_lo0, y_lo1, z_lo1)
    # the horn (Ellis Fig. 416, 'bracket', 3 in): full thickness under the rail, a 1/8 in step at
    # 1/4 in down, an ogee taking the inner face back to half the thickness by 2 1/4 in, then
    # straight to its foot (the step and ogee scaled off the figure, not printed)
    Hh = horn
    step_z, step_in = 0.25 * 25.4 * MM, 0.125 * 25.4 * MM
    og_end = 2.25 * 25.4 * MM
    half = y_up0 + ts / 2
    prof = [(y_up0, z_up0), (y_up1, z_up0), (y_up1, z_up0 - step_z), (y_up1 - step_in, z_up0 - step_z)]
    for k in range(1, 13):
        f = k / 12.0
        g = 0.5 - 0.5 * math.cos(math.pi * f)                   # an S-curve from the step to half thickness
        prof.append(((y_up1 - step_in) + (half - (y_up1 - step_in)) * g, z_up0 - step_z - (og_end - step_z) * f))
    prof += [(half, z_up0 - Hh), (y_up0, z_up0 - Hh)]
    E.append(("horn", "vsec_stile", prof))
    rect("vsec_stile", "head_outer_lining", y_ol0, z_top_clear, y_ol1, H_)
    rect("vsec_stile", "head", y_ol1, z_up1, y_il1, z_up1 + head_t)
    rect("vsec_stile", "head_parting_bead", y_pb0, z_up1 - pb_e, y_pb1, z_up1)
    rect("vsec_stile", "head_staff_bead", y_sb0, z_up1 - sb_e, y_sb1, z_up1)
    E.append(("oak_sill", "vsec_stile", [(y_nose, 0.0), (y_back, 0.0), (y_back, z_sill + sill["upstand_mm"] * MM),
                                         (y_lo0, z_sill + sill["upstand_mm"] * MM), (y_lo0, z_sill), (y_nose, z_sill - sill["fall_mm"] * MM)]))
    geo = dict(x_ol=x_ol, x_ps=x_ps, y_up=(y_up0, y_up1), y_lo=(y_lo0, y_lo1), z_lo=(z_lo0, z_lo1),
               z_up=(z_up0, z_up1), z_sill=z_sill, z_top_clear=z_top_clear, W=W, H=H)
    return E, geo


FRAMES = {
    "elev": lambda T: Frame(-0.60, -0.05, 1.20, (T["opening"]["height_mm"] + 150) * MM, 1.0),
    "vsec": lambda T: Frame(-0.10, -0.05, 0.40, (T["opening"]["height_mm"] + 150) * MM, 0.5),
    "hsec": lambda T: Frame(-0.60, -0.10, 1.20, 0.40, 0.5),
    "vsec_stile": lambda T: Frame(-0.10, -0.05, 0.40, (T["opening"]["height_mm"] + 150) * MM, 0.5),
}


def masks(T):
    E, geo = members(T)
    out = {}
    for kind in ("elev", "vsec", "hsec", "vsec_stile"):
        fr = FRAMES[kind](T)
        h, w = fr.shape
        img = Image.new("1", (w, h), 0)
        dr = ImageDraw.Draw(img)
        for name, k, poly in E:
            if k != kind:
                continue
            P = [fr.to_px(a, b) for a, b in poly]
            dr.polygon(P, fill=1, outline=1)
        out[kind] = np.array(img, dtype=bool)
    return out, geo


if __name__ == "__main__":
    T = load_target()
    M, geo = masks(T)
    np.savez_compressed(os.path.join(BUILD, "target.npz"), **M)
    for k, a in M.items():
        Image.fromarray((~a * 255).astype(np.uint8)).save(os.path.join(BUILD, "target_%s.png" % k))
    print({k: int(v.sum()) for k, v in M.items()}, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in geo.items()})
