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


def members(T):
    """The window as the manual draws it: a list of (name, kind, polygon) in
    the three drawings. kind: 'elev' (x, z), 'vsec' (y, z) at the drawing's
    section x, 'hsec' (x, y) at the drawing's section z.
    """
    o, f, s = T["opening"], T["frame"], T["sash"]
    W, H = o["width_mm"] * MM, o["height_mm"] * MM
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
    y_il1 = y_sb1 + f.get("inner_lining_past_staff_bead_mm", 0) * MM
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
    for nm, z0, z1, top_rail, bot_rail, y0, y1 in (("upper", z_up0, z_up1, tr, mr, y_up0, y_up1),
                                                   ("lower", z_lo0, z_lo1, mr, br, y_lo0, y_lo1)):
        rect("vsec", nm + "_top_rail", y0, z1 - top_rail, y1, z1)
        rect("vsec", nm + "_bottom_rail", y0, z0, y1, z0 + bot_rail)
    rect("vsec", "head_outer_lining", y_ol0, z_top_clear, y_ol1, H)
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
        r("inner_lining_" + ("L" if side < 0 else "R"), x_ps, y_il1, x_ps + il_w, y_il1 + il_t)
        r("lower_stile_" + ("L" if side < 0 else "R"), x_ps - st, y_lo0, x_ps, y_lo1)
    if s.get("panes_per_sash", 1) == 2:
        rect("hsec", "lower_bar", -bar / 2, y_lo0, bar / 2, y_lo1)
    geo = dict(x_ol=x_ol, x_ps=x_ps, y_up=(y_up0, y_up1), y_lo=(y_lo0, y_lo1), z_lo=(z_lo0, z_lo1),
               z_up=(z_up0, z_up1), z_sill=z_sill, z_top_clear=z_top_clear, W=W, H=H)
    return E, geo


FRAMES = {
    "elev": lambda T: Frame(-0.60, -0.05, 1.20, (T["opening"]["height_mm"] + 150) * MM, 1.0),
    "vsec": lambda T: Frame(-0.10, -0.05, 0.40, (T["opening"]["height_mm"] + 150) * MM, 1.0),
    "hsec": lambda T: Frame(-0.60, -0.10, 1.20, 0.40, 1.0),
}


def masks(T):
    E, geo = members(T)
    out = {}
    for kind in ("elev", "vsec", "hsec"):
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
