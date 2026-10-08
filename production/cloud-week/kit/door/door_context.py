"""The context wall for the door's review renders: never part of the door's .glb.

    import door_context; parts = door_context.build(T, "T1")        # list of dicts: name, V (mm), F, kind

The wall is built from target.json (brick.* for T1) and from the target review's plinth-return numbers (the fault the
review left standing: TARGET-REVIEW.md, re-review try 2): the brick plinth wraps both reveal corners, a return 70 mm
wide into the doorway (inner faces at x 70 and 812), standing from the tread's top to z 12 with the splayed course
mitred round the corner, so the threshold and riser show only between the returns and its horns run on behind them.
DECISIONS.md 8 Oct: that is the wall's, not the door piece's; it is built here only so the renders look like photograph 1.

T1 (terrace): red brick wall 342.9 thick with the reveal 114.3 deep and the check behind it for the frame; buff quoins in
ten blocks of three courses (long and short alternating, both sides in step, the reveal's return faces buff); a 13-brick
segmental arch with radial joints and a curved extrados resting on the top quoin block; a red-brick plinth 60 proud with
a 45 degree splayed top course. F1 (flat over a shop): painted-render pilaster returns and a fascia above the head.
Each part carries a `kind` (red, quoin, arch, mortar, plinth, render, dark) that render_door.py turns into a shader.
Millimetres, the target's axes (x from the left reveal, y into the wall, z up from the threshold's top).
"""
import math
import os
import sys

import numpy as np
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_door as bd  # noqa: E402

LONG_SPAN = 40000.0        # the wall runs far off both ways, so no end shows from the low view


def polys_of(g):
    if g.is_empty:
        return []
    geoms = [g] if g.geom_type == "Polygon" else [h for h in g.geoms if h.geom_type == "Polygon"]
    return [h for h in geoms if h.area > 1.0]


def extrude_region(name, region, y0, y1, kind, parts):
    """Extrude a shapely region (x, z) along y; polygons with holes are split by a vertical slit so each part is a simple prism."""
    for k, p in enumerate(polys_of(region)):
        if list(p.interiors):
            raise RuntimeError("region %s has a hole" % name)
        pts = list(p.exterior.coords)[:-1]
        V, F = bd.prism(pts, ("x", "z"), "y", y0, y1)
        parts.append({"name": name + ("" if k == 0 else str(k)), "V": V, "F": F, "kind": kind})


def obj_to_vf(o):
    """Take a (boolean-cut) bpy object's mesh back as (V, F) and remove the object."""
    me = o.data
    V = np.array([v.co[:] for v in me.vertices], float)
    F = [tuple(p.vertices) for p in me.polygons]
    bd._drop(o)
    return V, F


def soffit_circle(P):
    O = P["opening"]
    half = O["width_mm"] / 2
    rise = O["camber_rise_mm"]
    if rise <= 0:
        return None
    R = (half ** 2 + rise ** 2) / (2 * rise)
    return R, half, O["crown_height_mm"] - R


def soffit_z(P, x):
    c = soffit_circle(P)
    if c is None:
        return P["opening"]["crown_height_mm"]
    R, cx, cz = c
    return cz + math.sqrt(R ** 2 - (x - cx) ** 2)


def build_T1(T):
    P = T
    O, F, S, B = P["opening"], P["frame"], P["step"], P["brick"]
    OW, REV, WALL = O["width_mm"], O["reveal_depth_mm"], O["wall_thickness_mm"]
    ground = S["ground_z_mm"]
    parts = []
    q, a, pl = B["quoins"], B["arch"], B["plinth"]
    top = 4800.0
    # ---- quoins: ten blocks of three courses, long and short alternating, both sides in step
    quoin_rects = []
    for b, (z0, z1) in enumerate(q["block_z_mm"]):
        long_ = (b % 2 == 0) == (q["bottom_block"] == "long")
        w = q["stretcher_width_mm"] if long_ else q["header_width_mm"]
        quoin_rects += [sbox(-w, z0, 0.0, z1), sbox(OW, z0, OW + w, z1)]
        for side, (x0, x1) in (("L", (-w, 0.0)), ("R", (OW, OW + w))):
            V, Fc = bd.box(x0, 0.0, z0, x1, REV, z1)
            parts.append({"name": "ctx_quoin_%s%02d" % (side, b), "V": V, "F": Fc, "kind": "quoin", "block": b, "side": side, "z": (z0, z1), "x": (x0, x1)})
    # ---- the arch: 13 bricks on end, joints radial to the soffit's centre, extrados parallel to the soffit
    sc = a["soffit_circle"]
    R, cx, cz, depth = sc["radius_mm"], sc["centre_x_mm"], sc["centre_z_mm"], a["depth_mm"]
    th = math.asin((a["soffit_ends_x_mm"][1] - cx) / R)
    n, j = a["bricks"], a["joint_mm"]
    d = (j / 2) / R
    ring_pts_lo = [(cx + R * math.sin(-th + 2 * th * k / 60), cz + R * math.cos(-th + 2 * th * k / 60)) for k in range(61)]
    ring_pts_hi = [(cx + (R + depth) * math.sin(-th + 2 * th * k / 60), cz + (R + depth) * math.cos(-th + 2 * th * k / 60)) for k in range(61)]
    ring_region = Polygon(ring_pts_lo + ring_pts_hi[::-1])
    for i in range(n):
        p0 = -th + 2 * th * i / n + (d if i else 0.0)
        p1 = -th + 2 * th * (i + 1) / n - (d if i < n - 1 else 0.0)
        ph = [p0 + (p1 - p0) * k / 8 for k in range(9)]
        low = [(cx + R * math.sin(p), cz + R * math.cos(p)) for p in ph]
        high = [(cx + (R + depth) * math.sin(p), cz + (R + depth) * math.cos(p)) for p in ph[::-1]]
        V, Fc = bd.prism(low + high, ("x", "z"), "y", 0.0, REV)
        parts.append({"name": "ctx_arch_brick%02d" % i, "V": V, "F": Fc, "kind": "arch", "index": i})
    # the dark joints: a backing ring 4 mm back, 1 mm shy of the faces so no surface is shared
    thb = th - 1.5 / R                                      # 1.5 mm shy of the ring's end faces too
    lo2 = [(cx + (R + 1.0) * math.sin(-thb + 2 * thb * k / 60), cz + (R + 1.0) * math.cos(-thb + 2 * thb * k / 60)) for k in range(61)]
    hi2 = [(cx + (R + depth - 1.0) * math.sin(-thb + 2 * thb * k / 60), cz + (R + depth - 1.0) * math.cos(-thb + 2 * thb * k / 60)) for k in range(61)]
    V, Fc = bd.prism(lo2 + hi2[::-1], ("x", "z"), "y", 4.0, REV - 0.5)
    parts.append({"name": "ctx_arch_joints", "V": V, "F": Fc, "kind": "mortar"})
    # ---- the red wall: the front part (the reveal's depth) and the rear part (the check for the frame, the wall behind)
    opening = Polygon([(0.0, ground - 1000.0), (OW, ground - 1000.0)] + [(x, soffit_z(P, x)) for x in [OW * (24 - k) / 24 for k in range(25)]])
    horns = [sbox(-S["threshold"]["bearing_into_wall_each_side_mm"] - 1, S["threshold"]["top_z"] - S["threshold"]["thickness_mm"] - 0.5, 0.0, S["threshold"]["top_z"] + 0.0),
             sbox(OW, S["threshold"]["top_z"] - S["threshold"]["thickness_mm"] - 0.5, OW + S["threshold"]["bearing_into_wall_each_side_mm"] + 1, S["threshold"]["top_z"] + 0.0)]
    rect = sbox(-LONG_SPAN, ground, OW + LONG_SPAN, top)
    front = rect.difference(unary_union([opening, ring_region] + quoin_rects + horns))
    extrude_region("ctx_wall_front", front, 0.0, REV, "red", parts)
    jl, jr = F["jamb_x_mm"]["left"][0], F["jamb_x_mm"]["right"][1]
    open_rear = Polygon([(jl, ground - 1000.0), (jr, ground - 1000.0)] + [(x, soffit_z(P, x)) for x in [jl + (jr - jl) * (24 - k) / 24 for k in range(25)]])
    rear = rect.difference(unary_union([open_rear] + horns))
    extrude_region("ctx_wall_rear", rear, REV, WALL, "red", parts)
    # the dark inside, closing the doorway behind the frame (the fanlight shows it, never the sky)
    V, Fc = bd.box(jl - 20.0, WALL, ground + 100.0, jr + 20.0, WALL + 30.0, 2700.0)
    parts.append({"name": "ctx_interior", "V": V, "F": Fc, "kind": "dark"})
    # ---- the plinth: 60 proud, a 45 degree splayed top course to the wall face at z 12; returns in the doorway
    sp = pl["splay"]
    yp = -pl["front_proud_of_wall_face_mm"]
    z_from, z_to = sp["z_from_mm"], sp["z_to_mm"]
    side = [(yp, ground), (yp, z_from), (0.0, z_to), (0.0, ground)]
    tread_top = S["tread"]["top_z_mm"]
    V, Fc = bd.prism(side, ("y", "z"), "x", -LONG_SPAN, 0.0)
    parts.append({"name": "ctx_plinth_L", "V": V, "F": Fc, "kind": "plinth"})
    V, Fc = bd.prism(side, ("y", "z"), "x", OW, OW + LONG_SPAN)
    parts.append({"name": "ctx_plinth_R", "V": V, "F": Fc, "kind": "plinth"})
    ret_w = 70.0
    run = z_to - z_from                              # the splay's rise (60): it turns the corner
    for sd, sgn in (("L", 1), ("R", -1)):
        xe = 0.0 if sd == "L" else OW                # the reveal line
        xi = xe + sgn * ret_w                        # the return's inner face
        plan = [(xe, yp), (xi, yp), (xi, 0.0), (xe, 0.0)]
        V, Fc = bd.prism(plan, ("x", "y"), "z", tread_top - 4.0, z_to)
        o = bd.new_obj("_ret", V, Fc)
        # the splay on the front (z <= y + 12) and, mitred round the corner, on the inner face (z <= z_to - (|x - xi| ... toward the reveal)
        bd.cut(o, *bd.prism([(-80.0, z_from - 20.0 - 0.0 + 0.0), (0.0, z_to), (0.0, z_to + 100.0), (-80.0, z_to + 100.0)], ("y", "z"), "x", min(xe, xi) - 5, max(xe, xi) + 5))
        far = xe + sgn * (ret_w + 20.0)
        near = xe + sgn * (ret_w - run)
        bd.cut(o, *bd.prism([(far, z_from - 20.0), (near, z_to), (near, z_to + 100.0), (far, z_to + 100.0)], ("x", "z"), "y", yp - 5, 5.0))
        V, Fc = obj_to_vf(o)
        parts.append({"name": "ctx_plinth_return_" + sd, "V": V, "F": Fc, "kind": "plinth"})
        # level through the reveal to the frame's front face: 12 mm of brick on the threshold, beside the jamb's foot
        xs0, xs1 = (xe, xe + sgn * F["jamb_showing_past_brick_mm"])
        V, Fc = bd.box(min(xs0, xs1), 0.0, S["threshold"]["top_z"] - 0.3, max(xs0, xs1), REV, z_to)
        parts.append({"name": "ctx_plinth_reveal_" + sd, "V": V, "F": Fc, "kind": "plinth"})
    return parts


def build_F1(T):
    P = bd.variant_parts(T, "F1")
    O, F, S = P["opening"], P["frame"], P["step"]
    OW, REV, WALL = O["width_mm"], O["reveal_depth_mm"], O["wall_thickness_mm"]
    ground = S["ground_z_mm"]
    head_top = O["crown_height_mm"]
    parts = []
    jl, jr = F["jamb_x_mm"]["left"][0], F["jamb_x_mm"]["right"][1]
    top = 3300.0
    rect = sbox(-LONG_SPAN, ground, OW + LONG_SPAN, top)
    opening = sbox(0.0, ground - 1000.0, OW, head_top)
    sill_ends = [sbox(jl - 1, -S["threshold"]["thickness_mm"] - 0.5, 0.0, 0.0), sbox(OW, -S["threshold"]["thickness_mm"] - 0.5, jr + 1, 0.0)]
    front = rect.difference(unary_union([opening] + sill_ends))
    extrude_region("ctx_pilaster_front", front, 0.0, REV, "render", parts)
    open_rear = sbox(jl, ground - 1000.0, jr, head_top)
    rear = rect.difference(unary_union([open_rear] + sill_ends))
    extrude_region("ctx_pilaster_rear", rear, REV, WALL, "render", parts)
    V, Fc = bd.box(jl - 20.0, WALL, ground + 100.0, jr + 20.0, WALL + 30.0, 2700.0)
    parts.append({"name": "ctx_interior", "V": V, "F": Fc, "kind": "dark"})
    return parts


def build(T, variant):
    parts = build_T1(T) if variant == "T1" else build_F1(T)
    return parts


def make_objects(parts, variant, pivot):
    """Create the bpy objects (metres, at the door's pivot, UVs by cube projection); each carries its kind as a custom property."""
    import bpy
    from mathutils import Matrix
    px, py, pz = pivot
    M = Matrix.Scale(0.001, 4) @ Matrix.Translation((-px, -py, -pz))
    obs = []
    for p in parts:
        ob = bd.new_obj(p["name"], p["V"], p["F"])
        ob.data.transform(M)
        ob.data.update()
        bd.box_uv(ob.data)
        ob["kind"] = p["kind"]
        obs.append(ob)
    return obs
