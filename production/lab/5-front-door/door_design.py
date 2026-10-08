"""The attempt: the street's four-panel front door and its frame as 3D joinery.

Reads target/target.json's numbers only (never target_drawing.py or its drawings), assembles
the door the way a joiner makes it, and writes a parts list for tools/blender_parts.py:
- the solid frame: two jambs rebated out of the solid with an ovolo on the outer arris, a
  head, a transom rebated for the leaf's top, a fixed fanlight pane in a groove;
- the leaf: stiles full height, the three rails and the muntin between them, all grooved
  for the panels; four flat panels in the grooves with side play;
- outside: a bolection moulding round each panel (ogee and fillet, lapping the framing), the
  projecting band across the lock rail, the weatherboard; inside: a single planted moulding;
- for context: the stone sill and the brick wall with its reveal.

Axes as the target: x across (0 at the left brick reveal), y into the wall (outside -y, 0 at
the brick face), z up (0 at the top of the stone sill). Millimetres in, metres out.

    python door_design.py [version]   -> F:/LedgerTools/lab/door/build/parts_<version>.json
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import joinery  # noqa: E402

MM = 0.001
OUT = "F:/LedgerTools/lab/door/build"


def arc(cx, cy, r, a0, a1, n=8):
    return [(cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def m(P):
    return [[a * MM, b * MM] for a, b in P]


def prism(name, layer, profile, axis, plane, start, end):
    return {"name": "%s_%s" % (layer, name), "material": layer, "profile": m(profile), "axis": axis,
            "plane": plane, "start": start * MM, "end": end * MM}


def mesh(name, layer, V, F):
    return {"name": "%s_%s" % (layer, name), "material": layer,
            "mesh": {"V": [[float(c) for c in v] for v in V], "F": [[int(i) for i in f] for f in F]}}


def ogee_profile(width, lap, proud, face_y, panel_y, fillet_frac=0.36, n=10):
    """The bolection, across its run: d from its outer edge inward, y depth. It stands `proud`
    in front of the framing face over a fillet, falls in an ogee (convex then concave) to the
    panel face at its inner edge, and its back is rebated `lap` over the framing edge."""
    top = face_y - proud
    f = fillet_frac * width
    P = [(0.0, face_y), (0.0, top), (f, top)]
    for i in range(1, n + 1):
        t = i / n
        # ogee: y goes from the top to the panel face along a smooth S (cosine ease)
        d = f + (width - f) * t
        y = top + (panel_y - top) * (0.5 - 0.5 * math.cos(math.pi * t))
        P.append((d, y))
    P += [(lap, panel_y), (lap, face_y)]
    return P


def single_profile(width, back_y, panel_back_y, n=8):
    """The inside planted moulding in the angle of framing and panel: d from the framing edge
    inward, y depth; its face an ovolo from the framing's back face down to the panel's."""
    P = [(0.0, back_y)]
    for i in range(1, n + 1):
        t = i / n
        d = width * t
        y = back_y - (back_y - panel_back_y) * math.sin(math.pi / 2 * t)
        P.append((d, y))
    P += [(0.0, panel_back_y)]
    return P


def design(T):
    o, lf, pn, mo, fr = T["opening"], T["leaf"], T["panels"], T["mouldings"], T["frame"]
    parts = []
    W, H = o["brick_width_mm"], o["brick_height_mm"]
    reveal, wall = o["reveal_depth_mm"], o["wall_thickness_mm"]
    # ---- the frame
    jf, jd = fr["jamb_face_mm"], fr["jamb_depth_mm"]
    rw, rd = fr["rebate_width_mm"], fr["rebate_depth_mm"]
    fy0 = fr["frame_outside_face_y_mm"]
    fy1 = fy0 + jd
    stop_back = fy1 - rd                         # the face the leaf closes against
    r = mo["frame_ovolo_radius_mm"]
    head_top = fr["head_section_mm"]["z0"] + fr["head_section_mm"]["height"]
    for side, (x0, x1) in (("L", fr["jamb_x_mm"]["left"]), ("R", fr["jamb_x_mm"]["right"])):
        sgn = 1 if side == "L" else -1
        edge = x1 if side == "L" else x0         # the arris facing the opening
        stop_edge = edge - sgn * rw
        back = x0 if side == "L" else x1
        prof = [(back, fy0), (edge - sgn * r, fy0)]
        c = (edge - sgn * r, fy0 + r)
        prof += arc(c[0], c[1], r, -math.pi / 2, (-math.pi / 2 + sgn * math.pi / 2), 8)[1:]
        prof += [(edge, stop_back), (stop_edge, stop_back), (stop_edge, fy1), (back, fy1)]
        if side == "R":
            prof = prof[::-1]
        parts.append(prism("jamb_" + side, "frame", prof, "z", ["x", "y"], 0.0, head_top))
    xj0, xj1 = fr["jamb_x_mm"]["left"][1], fr["jamb_x_mm"]["right"][0]      # between the jambs' faces
    fl = fr["fanlight"]
    gy, gt, grb = fl["glass_y_mm"], fl["glass_thickness_mm"], fl["glass_rebate_mm"]
    hz0 = fr["head_section_mm"]["z0"]
    # head: plain, grooved underneath for the fanlight's pane
    parts.append(prism("head", "frame", [(fy0, hz0), (gy - gt / 2, hz0), (gy - gt / 2, hz0 + grb), (gy + gt / 2, hz0 + grb),
                                         (gy + gt / 2, hz0), (fy1, hz0), (fy1, head_top), (fy0, head_top)],
                       "x", ["y", "z"], xj0 - 20.0, xj1 + 20.0))
    tr = fr["transom"]
    t0, t1, trb = tr["z_stop_underside"], tr["z_top"], tr["rebate_underside_z"]
    parts.append(prism("transom", "frame", [(fy0, t0), (stop_back, t0), (stop_back, trb), (fy1, trb), (fy1, t1),
                                            (gy + gt / 2, t1), (gy + gt / 2, t1 - grb), (gy - gt / 2, t1 - grb),
                                            (gy - gt / 2, t1), (fy0, t1)], "x", ["y", "z"], xj0 - 20.0, xj1 + 20.0))
    parts.append(prism("fanlight", "glass", [(gy - gt / 2, t1 - grb), (gy + gt / 2, t1 - grb), (gy + gt / 2, hz0 + grb),
                                             (gy - gt / 2, hz0 + grb)], "x", ["y", "z"], xj0 - 6.0, xj1 + 6.0))
    # ---- the leaf
    lx0, lz0, lw, lh, lt = lf["x0_mm"], lf["z0_mm"], lf["width_mm"], lf["height_mm"], lf["thickness_mm"]
    ly0 = lf["outside_face_y_mm"]
    ly1 = ly0 + lt
    pt, gd, play = pn["thickness_mm"], pn["groove_depth_mm"], pn["side_play_mm"]
    py0 = ly0 + (lt - pt) / 2
    py1 = py0 + pt
    st, mu = lf["stile_mm"], lf["muntin_mm"]
    tr_h, lr_h, br_h = lf["top_rail_mm"], lf["lock_rail_mm"], lf["bottom_rail_mm"]
    lrc = lf["lock_rail_centre_above_leaf_bottom_mm"]
    lr0, lr1 = lrc - lr_h / 2, lrc + lr_h / 2

    def grooved(u0, u1, groove_lo, groove_hi):
        """A member's section across its width (u) and thickness (y), grooved on either edge."""
        P = [(u0, ly0), (u1, ly0)]
        if groove_hi:
            P += [(u1, py0), (u1 - gd, py0), (u1 - gd, py1), (u1, py1)]
        P += [(u1, ly1), (u0, ly1)]
        if groove_lo:
            P += [(u0, py1), (u0 + gd, py1), (u0 + gd, py0), (u0, py0)]
        return P
    X = lambda u: lx0 + u
    Z = lambda v: lz0 + v
    parts.append(prism("stile_L", "leaf", grooved(X(0), X(st), False, True), "z", ["x", "y"], Z(0), Z(lh)))
    parts.append(prism("stile_R", "leaf", grooved(X(lw - st), X(lw), True, False), "z", ["x", "y"], Z(0), Z(lh)))
    for nm, v0, v1, lo, hi in (("bottom_rail", 0.0, br_h, False, True), ("lock_rail", lr0, lr1, True, True),
                               ("top_rail", lh - tr_h, lh, True, False)):
        sec = [(y, z) for z, y in grooved(Z(v0), Z(v1), lo, hi)]
        parts.append(prism(nm, "leaf", sec, "x", ["y", "z"], X(st), X(lw - st)))
    for nm, v0, v1 in (("muntin_low", br_h, lr0), ("muntin_high", lr1, lh - tr_h)):
        parts.append(prism(nm, "leaf", grooved(X((lw - mu) / 2), X((lw + mu) / 2), True, True), "z", ["x", "y"], Z(v0), Z(v1)))
    # panels in the grooves: side play split both sides; close lengthways (Ellis p.92)
    bol = mo["outside_bolection"]
    sgl = mo["inside_single"]
    for key, op in pn["openings_leaf_uv_mm"].items():
        u0, u1, v0, v1 = op["u0"], op["u1"], op["v0"], op["v1"]
        px0, px1 = X(u0) - gd + play / 2, X(u1) + gd - play / 2
        pz0, pz1 = Z(v0) - gd, Z(v1) + gd
        parts.append(prism("panel_" + key, "panel", [(px0, py0), (px1, py0), (px1, py1), (px0, py1)], "z", ["x", "y"], pz0, pz1))
        # the bolection, outside: its outer edge lapping the framing
        lap = bol["lap_over_framing_mm"]
        prof = ogee_profile(bol["width_on_face_mm"], lap, bol["projection_above_framing_mm"], ly0, py0)
        V, F = joinery.sweep_frame([(d * MM, (y - ly0) * MM) for d, y in prof],
                                   (X(u0) - lap) * MM, (Z(v0) - lap) * MM, (X(u1) + lap) * MM, (Z(v1) + lap) * MM, ly0 * MM)
        parts.append(mesh("bolection_" + key, "moulding", V, F))
        # the single moulding, inside: in the angle of framing and panel
        prof = single_profile(sgl["width_on_face_mm"], ly1, py1)
        V, F = joinery.sweep_frame([(d * MM, (y - ly0) * MM) for d, y in prof],
                                   X(u0) * MM, Z(v0) * MM, X(u1) * MM, Z(v1) * MM, ly0 * MM)
        parts.append(mesh("single_" + key, "moulding", V, F))
    # the band across the lock rail and the weatherboard: across the leaf, short of the stops
    # as the target draws them, from stop to stop (a real band wants a hair of clearance there)
    bx0, bx1 = xj0, xj1
    b0, b1 = mo["lock_rail_band"]["z_above_leaf_bottom_mm"]
    bp = mo["lock_rail_band"]["projection_mm"]
    parts.append(prism("lock_band", "moulding", [(ly0 - bp, Z(b0)), (ly0, Z(b0)), (ly0, Z(b1)), (ly0 - bp, Z(b1))],
                       "x", ["y", "z"], bx0, bx1))
    w0, w1 = mo["weatherboard"]["z_above_leaf_bottom_mm"]
    wp = mo["weatherboard"]["projection_mm"]
    parts.append(prism("weatherboard", "moulding", [(ly0 - wp, Z(w0)), (ly0, Z(w0)), (ly0, Z(w1)), (ly0 - wp, Z(w0) + 12.0)],
                       "x", ["y", "z"], bx0, bx1))
    # ---- context: the stone sill, rounded at its nose, and the brick round the opening
    s = fr["sill"]
    nr = 19.0
    sp = [(s["front_y_mm"], -s["thickness_mm"]), (s["front_y_mm"], -nr)] + \
        arc(s["front_y_mm"] + nr, -nr, nr, math.pi, math.pi / 2, 8)[1:] + \
        [(s["back_y_mm"], 0.0), (s["back_y_mm"], -s["thickness_mm"])]
    parts.append(prism("sill", "stone", sp, "x", ["y", "z"], 0.0, W))
    return parts


if __name__ == "__main__":
    ver = sys.argv[1] if len(sys.argv) > 1 else "v1"
    T = json.load(open(os.path.join(HERE, "target", "target.json"), encoding="utf-8"))
    parts = design(T)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "parts_%s.json" % ver)
    json.dump({"parts": parts}, open(path, "w"))
    print("wrote", path, len(parts), "parts")
