"""The attempt: the sash window as 3D joinery, made as solids for Blender.

Reads target.json's numbers only (never target_drawing.py), assembles the
window member by member the way a joiner makes it (box frame, two sashes with
moulded and rebated stiles and rails, horns, glazing bars, an oak sill), and
writes parts.json for tools/blender_parts.py. The checker then cuts the built
model and compares it with the target drawing.

Axes as target_drawing.py: x across (0 at the centre), y into the house (0 at
the brick face), z up (0 at the top of the stone sill), metres.

    python window_design.py [version]   -> parts_<version>.json
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MM = 0.001


def arc(cx, cy, r, a0, a1, n=8):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def member_profile(width, thick, rebate_w, rebate_d, ovolo_r, glass_side=+1):
    """Section of a sash stile or rail, across its length: `width` across the
    face (u), `thick` through the sash (v, 0 = outside face). The glass side is
    at u = width when glass_side=+1. Outside: a rebate for glass and putty;
    inside: an ovolo stuck on the arris by the glass. Returns a closed polygon
    in (u, v), counter-clockwise."""
    W, T = width, thick
    P = [(0.0, 0.0), (W - rebate_w, 0.0), (W - rebate_w, rebate_d), (W, rebate_d)]
    # inner arris by the glass, from (W, T - r) round to (W - r, T): an ovolo (quarter round, convex)
    if ovolo_r > 0:
        P += [(W, T - ovolo_r)] + arc(W - ovolo_r, T - ovolo_r, ovolo_r, 0.0, math.pi / 2)[1:]
    else:
        P += [(W, T)]
    P += [(0.0, T)]
    if glass_side < 0:
        P = [(W - u, v) for u, v in P][::-1]
    return P


def bar_profile(width, thick, rebate_w, rebate_d, ovolo_r):
    """A glazing bar: glass both sides, rebated outside, ovolo both arrises inside."""
    W, T, h = width, thick, width / 2
    P = [(-h + rebate_w, 0.0), (h - rebate_w, 0.0), (h - rebate_w, rebate_d), (h, rebate_d),
         (h, T - ovolo_r)] + arc(h - ovolo_r, T - ovolo_r, ovolo_r, 0.0, math.pi / 2)[1:]
    P += arc(-h + ovolo_r, T - ovolo_r, ovolo_r, math.pi / 2, math.pi)[1:]
    P += [(-h, rebate_d), (-h + rebate_w, rebate_d)]
    return P


def design(T):
    o, f, s, sill = T["opening"], T["frame"], T["sash"], T["sill"]
    W, H = o["width_mm"] * MM, o["height_mm"] * MM
    R = f["reveal_mm"] * MM
    parts = []

    def prism(name, mat, profile, axis, plane, start, end):
        parts.append({"name": name, "material": mat, "profile": [list(map(float, p)) for p in profile],
                      "axis": axis, "plane": plane, "start": float(start), "end": float(end)})

    def box(name, mat, x0, y0, z0, x1, y1, z1):
        prism(name, mat, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "z", ["x", "y"], z0, z1)

    # ---- the box frame ----------------------------------------------------
    m = f["outer_lining_margin_mm"] * MM
    olw, olt = f["outer_lining_width_mm"] * MM, f["outer_lining_thickness_mm"] * MM
    stop = f["outer_lining_projection_mm"] * MM
    pst = f["pulley_stile_thickness_mm"] * MM
    ilw, ilt = f["inner_lining_width_mm"] * MM, f["inner_lining_thickness_mm"] * MM
    pbw, pbe = f["parting_bead_width_mm"] * MM, f["parting_bead_projection_mm"] * MM
    sbw, sbe = f["staff_bead_width_mm"] * MM, f["staff_bead_projection_mm"] * MM
    head_vis = f["head_visible_mm"] * MM
    ts, clr = s["thickness_mm"] * MM, s.get("clearance_mm", 2) * MM

    x_edge = W / 2 - m                 # outer lining's inner edge, seen in the brick opening
    x_face = x_edge + stop             # pulley stile's face: the sashes' edges run against it
    y0 = R                             # outer lining's outside face
    y_up = (y0 + olt + clr, y0 + olt + clr + ts)
    y_pb = (y_up[1] + clr, y_up[1] + clr + pbw)
    y_lo = (y_pb[1] + clr, y_pb[1] + clr + ts)
    y_sb = (y_lo[1] + clr, y_lo[1] + clr + sbw)
    y_back = y_sb[1] + f.get("inner_lining_past_staff_bead_mm", 0) * MM   # pulley stile's back edge
    z_sill = sill["height_at_front_mm"] * MM
    z_clear = H - head_vis             # underside of the head lining's visible margin
    z_head_face = z_clear + stop       # head's face (the upper sash's top runs to it)

    for side, tag in ((-1, "L"), (1, "R")):
        sx = lambda a, b: (min(side * a, side * b), max(side * a, side * b))
        xa, xb = sx(x_edge, x_edge + olw)
        box("outer_lining_" + tag, "paint", xa, y0, z_sill, xb, y0 + olt, H)
        xa, xb = sx(x_face, x_face + pst)
        box("pulley_stile_" + tag, "paint", xa, y0 + olt, z_sill, xb, y_back, z_head_face)
        xa, xb = sx(x_face - pbe, x_face)
        box("parting_bead_" + tag, "paint", xa, y_pb[0], z_sill, xb, y_pb[1], z_head_face)
        xa, xb = sx(x_face - sbe, x_face)
        box("staff_bead_" + tag, "paint", xa, y_sb[0], z_sill, xb, y_sb[1], z_head_face)
        xa, xb = sx(x_face, x_face + ilw)
        box("inner_lining_" + tag, "paint", xa, y_back, z_sill, xb, y_back + ilt, H)
    # head: outer lining across the top, head (pulley) lining, beads
    box("head_outer_lining", "paint", -(x_edge + olw), y0, z_clear, x_edge + olw, y0 + olt, H)
    box("head_lining", "paint", -(x_face + pst), y0 + olt, z_head_face, x_face + pst, y_back, z_head_face + pst)
    box("head_parting_bead", "paint", -x_face, y_pb[0], z_head_face - pbe, x_face, y_pb[1], z_head_face)
    box("head_staff_bead", "paint", -x_face, y_sb[0], z_head_face - sbe, x_face, y_sb[1], z_head_face)

    # ---- the oak sill, weathered ------------------------------------------
    nose = sill["projection_mm"] * MM
    fall = sill["fall_mm"] * MM
    up = sill["upstand_mm"] * MM
    sill_prof = [(y0 - nose, 0.0), (y_back + ilt, 0.0), (y_back + ilt, z_sill + up), (y_lo[0], z_sill + up),
                 (y_lo[0], z_sill), (y0 - nose, z_sill - fall)]
    prism("oak_sill", "paint", sill_prof, "x", ["y", "z"], -(x_face + pst + sill.get("horns_mm", 0) * MM),
          x_face + pst + sill.get("horns_mm", 0) * MM)

    # ---- the two sashes, closed -------------------------------------------
    st, tr, br, mr = (s[k] * MM for k in ("stile_width_mm", "top_rail_mm", "bottom_rail_mm", "meeting_rail_depth_mm"))
    rw, rd, ov = s["rebate_width_mm"] * MM, s["rebate_depth_mm"] * MM, s["ovolo_radius_mm"] * MM
    barw = s["glazing_bar_width_mm"] * MM
    horn = s["horn_length_mm"] * MM
    sash_w = 2 * x_face
    sash_h = (z_head_face - z_sill + mr) / 2
    z_lo = (z_sill, z_sill + sash_h)
    z_up = (z_head_face - sash_h, z_head_face)

    def sash(nm, yy, zz, top, bottom, horns):
        # stiles: section in (x, y), run along z; glass side toward the centre
        for side, tag in ((-1, "L"), (1, "R")):
            prof = member_profile(st, ts, rw, rd, ov, glass_side=+1)
            P = [((-x_face + u) if side < 0 else (x_face - u), yy[0] + v) for u, v in prof]
            prism("%s_stile_%s" % (nm, tag), "paint", P, "z", ["x", "y"], zz[0] - (horn if horns else 0), zz[1])
        # rails: section in (z, y), run along x between the stiles (tenons hidden)
        for rail, depth, at_top in (("top_rail", top, True), ("bottom_rail", bottom, False)):
            prof = member_profile(depth, ts, rw, rd, ov, glass_side=+1)
            P = [((zz[1] - u) if at_top else (zz[0] + u), yy[0] + v) for u, v in prof]
            prism("%s_%s" % (nm, rail), "paint", P, "x", ["z", "y"], -x_face + st, x_face - st)
        if s.get("panes_per_sash", 1) == 2:
            P = [(u, yy[0] + v) for u, v in bar_profile(barw, ts, rw, rd, ov)]
            prism(nm + "_bar", "paint", P, "z", ["x", "y"], zz[0] + bottom - rd, zz[1] - top + rd)
        # the pane(s): 4 mm glass in the rebate
        g = s.get("glass_mm", 3) * MM
        gy = yy[0] + rd - g
        box(nm + "_glass", "glass", -x_face + st - rw + 0.001, gy, zz[0] + bottom - rw + 0.001,
            x_face - st + rw - 0.001, gy + g, zz[1] - top + rw - 0.001)

    sash("upper", y_up, z_up, tr, mr, True)
    sash("lower", y_lo, z_lo, mr, br, False)
    return parts


if __name__ == "__main__":
    ver = sys.argv[1] if len(sys.argv) > 1 else "v1"
    T = json.load(open(os.path.join(HERE, "target.json")))
    parts = design(T)
    out = os.path.join(r"F:/LedgerTools/lab/sash/build", "parts_%s.json" % ver)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"parts": parts}, open(out, "w"), indent=0)
    print("wrote", out, len(parts), "parts")
