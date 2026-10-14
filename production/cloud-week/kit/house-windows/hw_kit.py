"""The four house-window kit pieces (S22, S11, RC, RC2) and the cottages' room card, built by script in Blender 5.2 (bpy) to target.json sections 4 to 8.

Kit frame (target section 8): metres in the glb, z up in Blender (the glb is glTF y-up as every kit glb: kit (x, y, z) = (x_glb, -z_glb, y_glb)); x across the window (0 at its middle, + to the viewer's
right), y INTO the wall from the brick face (0 at the face), z UP from the opening's bottom edge; the pivot is the opening's bottom-edge centre on the brick face; the street is at -y.

S22 and S11 are the lab's checked sash (production/assets/sash-window/sash_window.glb and _1over1.glb, 41 and 35 nodes), imported and not redrawn: their glass sheets become one node a pane (the 2/2's
split at the bar), each pane tilted by a seeded angle (target 5.2), every joinery vertex gets its colour (the box shade, 5.4), and the nets, drapes, blinds, pendant and room card are added. RC and RC2 are
built from the target's parts tables (4.3), bevelled 1.5 mm, with the gasket line and the welded-corner grooves as strips.

The lessons of the shops' reviews, applied from the start (14 October): nothing is left open; the glass is a part (a pane node each, never a stand-in); a net or curtain has varied folds with soft normals
and a see-through weave (hw_cloth.py); curtains have a pole with finials and brackets and the nets a rod with brackets (so a head is gathered on something); the models carry real UVs and real RGB
normal maps; no part floats (every net, curtain and blind hangs from its rod or headrail, every rod from its brackets, every bracket from a lining or the wall).
"""
import json
import math
import os
import sys
import zlib

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402
import bmesh  # noqa: E402
from mathutils import Vector, Matrix, Euler  # noqa: E402
import hw_t as T  # noqa: E402
import hw_cloth as CL  # noqa: E402

MM = 0.001
EPS = 0.3                      # mm: two faces closer than this touch
BAND = 8.0                     # mm: an inside corner's reach (box shade)
Y_GLASS = {"S22": {"upper": 142.0, "lower": 190.0}, "S11": {"upper": 142.0, "lower": 190.0}, "RC": {"all": 112.5}, "RC2": {"all": 112.5}}
DEFAULT_PAINT = {"S22": "white_fresh", "S11": "white_fresh", "RC": "white_upvc", "RC2": "white_upvc"}
GLB_NAMES = {"S22": "hw_S22.glb", "S11": "hw_S11.glb", "RC": "hw_RC.glb", "RC2": "hw_RC2.glb", "GF": "hw_room_card_gf.glb"}


# ---------------------------------------------------------------------------------------------------------------------------- scene helpers
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for m in list(bpy.data.materials):
        bpy.data.materials.remove(m)


def srgb8_to_lin(c):
    return T.srgb_to_lin(c)


def principled(m):
    return m.node_tree.nodes["Principled BSDF"]


def make_mats(kind, cloth):
    """The kit's materials, named as the target says (7: paint_<name>, glass_house, net_voile, curtain, blind, pendant_shade, room_card)."""
    P = T.paints()
    pn = DEFAULT_PAINT.get(kind, "white_fresh")
    mats = {}
    m = bpy.data.materials.new("paint_" + pn)
    m.use_nodes = True
    p = principled(m)
    p.inputs["Base Color"].default_value = (*P[pn]["lin"], 1.0)
    p.inputs["Roughness"].default_value = P[pn]["rough"]
    p.inputs["Metallic"].default_value = 0.0
    mats["paint"] = m
    # the pane (GLASS.pane): base colour 0.03, specular 1.0 (F0 0.08: Cycles' Specular IOR Level 1.0), roughness 0.03, metallic 0, no transmission, no emission by day
    g = bpy.data.materials.new("glass_house")
    g.use_nodes = True
    p = principled(g)
    p.inputs["Base Color"].default_value = (0.03, 0.03, 0.03, 1.0)
    p.inputs["Roughness"].default_value = 0.03
    p.inputs["Metallic"].default_value = 0.0
    p.inputs["Specular IOR Level"].default_value = 1.0
    p.inputs["Transmission Weight"].default_value = 0.0
    mats["glass"] = g

    def tex_mat(name, base_png, normal_jpg, colour_lin, rough, blend=True):
        mm = bpy.data.materials.new(name)
        mm.use_nodes = True
        nt = mm.node_tree
        p = nt.nodes["Principled BSDF"]
        ti = nt.nodes.new("ShaderNodeTexImage")
        ti.image = bpy.data.images.load(base_png, check_existing=True)
        ti.image.colorspace_settings.name = "sRGB"
        ti.image.alpha_mode = "STRAIGHT"
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        mix.inputs[7].default_value = (*colour_lin, 1.0)
        nt.links.new(ti.outputs["Color"], mix.inputs[6])
        nt.links.new(mix.outputs[2], p.inputs["Base Color"])
        nt.links.new(ti.outputs["Alpha"], p.inputs["Alpha"])
        if normal_jpg:
            tn = nt.nodes.new("ShaderNodeTexImage")
            tn.image = bpy.data.images.load(normal_jpg, check_existing=True)
            tn.image.colorspace_settings.name = "Non-Color"
            nm = nt.nodes.new("ShaderNodeNormalMap")
            nt.links.new(tn.outputs["Color"], nm.inputs["Color"])
            nt.links.new(nm.outputs["Normal"], p.inputs["Normal"])
        p.inputs["Roughness"].default_value = rough
        p.inputs["Metallic"].default_value = 0.0
        if blend:
            mm.surface_render_method = "BLENDED"
        mm.use_backface_culling = False
        return mm
    d = cloth["dir"]
    mats["net"] = tex_mat("net_voile", os.path.join(d, "net_voile_basecolour.png"), os.path.join(d, "net_voile_normal.jpg"), srgb8_to_lin((238, 238, 232)), 0.9)
    mats["curtain"] = tex_mat("curtain", os.path.join(d, "curtain_basecolour.png"), os.path.join(d, "curtain_normal.jpg"), srgb8_to_lin((214, 198, 166)), 0.85)
    mats["blind"] = tex_mat("blind", os.path.join(d, "blind_basecolour.png"), None, srgb8_to_lin((226, 224, 214)), 0.5)
    ps = bpy.data.materials.new("pendant_shade")
    ps.use_nodes = True
    p = principled(ps)
    p.inputs["Base Color"].default_value = (*srgb8_to_lin((236, 226, 196)), 1.0)
    p.inputs["Roughness"].default_value = 0.9
    ps.use_backface_culling = False
    mats["shade"] = ps
    rc = bpy.data.materials.new("room_card")
    rc.use_nodes = True
    principled(rc).inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)
    principled(rc).inputs["Roughness"].default_value = 1.0
    mats["card"] = rc
    return mats


def mesh_from(name, verts_mm, faces, mat, uvs=None, parent=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x * MM, y * MM, z * MM) for x, y, z in verts_mm], [], faces)
    me.update()
    if uvs is not None:
        uv = me.uv_layers.new(name="UVMap")
        for poly in me.polygons:
            for li, vi in zip(poly.loop_indices, poly.vertices):
                uv.data[li].uv = uvs[vi]
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    if mat is not None:
        me.materials.append(mat)
    return ob


def card(name, x0, x1, z0, z1, y, mat, rect, flip=False, skew=0.0):
    """A flat two-triangle card facing the street (-y) at plane y (mm), its UVs the atlas rect (u0, v0, u1, v1) with v up. `skew`: the bottom-left corner raised (a torn net's hem out of true)."""
    u0, v0, u1, v1 = rect
    verts = [(x0, y, z0 + skew), (x1, y, z0), (x1, y, z1), (x0, y, z1)]
    uvs = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    faces = [(0, 1, 2, 3)]
    ob = mesh_from(name, verts, faces, mat, uvs)
    return ob


def box_mm(name, x0, x1, y0, y1, z0, z1, mat, bevel=0.0):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    ob = mesh_from(name, v, f, mat)
    ob["hw_box"] = True
    if bevel > 0:
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bevel * MM, offset_type="OFFSET", segments=1, affect="EDGES", profile=0.5)
        bm.normal_update()
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bm.to_mesh(ob.data)
        bm.free()
    return ob


def cyl_x(name, xa, xb, y, z, r, mat, n=8):
    """A cylinder along x (mm): a rod."""
    verts, faces = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        verts.append((xa, y + r * math.cos(a), z + r * math.sin(a)))
        verts.append((xb, y + r * math.cos(a), z + r * math.sin(a)))
    for i in range(n):
        j = (i + 1) % n
        faces.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    faces.append(tuple(2 * i for i in reversed(range(n))))
    faces.append(tuple(2 * i + 1 for i in range(n)))
    return mesh_from(name, verts, faces, mat)


def smooth(obj, deg=32.0):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(deg))
    except Exception:
        for p in obj.data.polygons:
            p.use_smooth = True


def apply_all(objs):
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def bbox_mm(o):
    pts = [o.matrix_world @ v.co for v in o.data.vertices]
    lo = [min(p[i] for p in pts) / MM for i in range(3)]
    hi = [max(p[i] for p in pts) / MM for i in range(3)]
    return lo, hi


def tris(o):
    o.data.calc_loop_triangles()
    return len(o.data.loop_triangles)


# ---------------------------------------------------------------------------------------------------------------------------- the lab sash
def import_lab(kind):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=T.LAB_GLB[kind])
    new = [o for o in bpy.data.objects if o not in before]
    meshes = []
    for o in new:
        if o.type == "MESH":
            mw = o.matrix_world.copy()
            o.parent = None
            o.matrix_world = mw
            meshes.append(o)
    for o in new:
        if o.type != "MESH":
            bpy.data.objects.remove(o, do_unlink=True)
    apply_all(meshes)
    for o in meshes:
        # the importer's split normals go: the shading is set again by angle below (the lab's ovolo profiles are 11 degree facets)
        if o.data.has_custom_normals:
            bpy.context.view_layer.objects.active = o
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
    return {o.name: o for o in meshes}


def is_box(o):
    """A mesh that is an axis-aligned box (its vertices are all corners of its bounding box): the nodes whose contacts the inside-corner band is built on."""
    if o.get("hw_box"):
        return True
    lo, hi = bbox_mm(o)
    for v in o.data.vertices:
        p = o.matrix_world @ v.co
        for i in range(3):
            c = p[i] / MM
            if abs(c - lo[i]) > 0.05 and abs(c - hi[i]) > 0.05:
                return False
    return True


# ---------------------------------------------------------------------------------------------------------------------------- the box shade (5.4)
def bisect(o, axis, value_mm):
    """Cut a mesh with the plane axis = value (mm): every face that crosses it is split (the inside-corner bands and the track need their edges)."""
    bm = bmesh.new()
    bm.from_mesh(o.data)
    no = [0, 0, 0]
    no[axis] = 1.0
    co = [0, 0, 0]
    co[axis] = value_mm * MM
    geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
    bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no, clear_inner=False, clear_outer=False)
    bm.to_mesh(o.data)
    bm.free()
    o.data.update()


def find_corners(boxes):
    """Inside (concave) corners of the union of axis-aligned boxes that touch: for every contact rectangle of A against B, an edge of it where A's side face rises from B's face and B's face runs on
    beyond (exactly one of the two ends there). Returns bands: {'A', 'B', 'a', 'sA', 'plane', 'o', 'c', 'e', 'third'} (mm)."""
    out = []
    bb = {o.name: bbox_mm(o) for o in boxes}
    for A in boxes:
        for B in boxes:
            if A is B:
                continue
            la, ha = bb[A.name]
            lb, hb = bb[B.name]
            for a in range(3):
                for sA in (1, -1):
                    pa = ha[a] if sA == 1 else la[a]
                    pb = lb[a] if sA == 1 else hb[a]
                    if abs(pa - pb) > EPS:
                        continue
                    others = [i for i in range(3) if i != a]
                    ov = {}
                    ok = True
                    for o_ in others:
                        lo_ = max(la[o_], lb[o_])
                        hi_ = min(ha[o_], hb[o_])
                        if hi_ - lo_ < 0.5:
                            ok = False
                        ov[o_] = (lo_, hi_)
                    if not ok:
                        continue
                    for oi, o_ in enumerate(others):
                        third = others[1 - oi]
                        for e, c in ((0, ov[o_][0]), (1, ov[o_][1])):
                            a_ends = abs((la[o_] if e == 0 else ha[o_]) - c) < EPS
                            b_ends = abs((lb[o_] if e == 0 else hb[o_]) - c) < EPS
                            if a_ends and not b_ends:
                                out.append({"A": A, "B": B, "a": a, "sA": sA, "plane": pa, "o": o_, "c": c, "e": e, "third": ov[third], "third_axis": third})
    return out


def apply_cuts(corners, track_cuts):
    """Bisect the meshes at 8 mm from each inside corner (on the side face of A and on the exposed face of B), and at the track's edges."""
    done = set()
    for k in corners:
        A, B = k["A"], k["B"]
        # A: the cut at a = plane - sA * 8 (the side face's band rises from the contact plane)
        key = (A.name, k["a"], round(k["plane"] - k["sA"] * BAND, 2))
        if key not in done:
            bisect(A, k["a"], k["plane"] - k["sA"] * BAND)
            done.add(key)
        # B: the cut at o = c -+ 8 (the exposed face beyond A's side)
        cb = k["c"] - BAND if k["e"] == 0 else k["c"] + BAND
        key = (B.name, k["o"], round(cb, 2))
        if key not in done:
            bisect(B, k["o"], cb)
            done.add(key)
    for o, axis, vals in track_cuts:
        for v in vals:
            bisect(o, axis, v)


def poly_normal_mm(o, poly):
    n = (o.matrix_world.to_3x3() @ poly.normal).normalized()
    return n


def shade_object(o, kind, corners_by_obj, node_role):
    """COLOR_0 on every loop of a joinery mesh by the box-shade rules of target 5.4 (grey, R = G = B)."""
    me = o.data
    if "Color" in me.color_attributes:
        me.color_attributes.remove(me.color_attributes["Color"])
    attr = me.color_attributes.new("Color", "FLOAT_COLOR", "CORNER")
    me.attributes.active_color = attr
    name = o.name
    yg_tab = Y_GLASS[kind]
    yg = yg_tab.get("all") or (yg_tab["upper"] if "upper" in name else yg_tab["lower"])
    bands = corners_by_obj.get(o.name, [])
    for poly in me.polygons:
        n = poly_normal_mm(o, poly)
        for li, vi in zip(poly.loop_indices, poly.vertices):
            p = o.matrix_world @ me.vertices[vi].co
            x, y, z = p[0] / MM, p[1] / MM, p[2] / MM
            street = n.y < -0.5
            if "putty" in name:
                val = 0.35
            elif name.startswith(("gasket", "paint_joinery__gasket")):
                val = 0.30
            elif "weld" in name:
                val = 0.35
            else:
                grad = 1.0 - 0.4 * min(max(y / yg, 0.0), 1.0)
                val = 1.0 if street else grad
                if "upper_bottom_rail" in name and n.z < -0.5:
                    val = 0.40
                if "parting_bead" in name and abs(n.x) > 0.5:
                    val = 0.10
                if "pulley_stile" in name and abs(n.x) > 0.5 and 184.1 - 0.05 <= y <= 222.2 + 0.05:
                    # the track: the face between the parting bead and the staff bead (its two end vertices are on the cuts)
                    ymid = sum((o.matrix_world @ me.vertices[v].co).y / MM for v in poly.vertices) / len(poly.vertices)
                    if 184.1 < ymid < 222.2:
                        val = 0.50
                if not street:
                    for bnd in bands:
                        if bnd["axis_n"] is not None and abs(n[bnd["axis_n"]] - bnd["sign_n"]) < 0.2:
                            inside = all(bnd["lo"][i] - 0.06 <= (o.matrix_world @ me.vertices[v].co)[i] / MM <= bnd["hi"][i] + 0.06 for v in poly.vertices for i in range(3))
                            if inside:
                                val = min(val, 0.30)
            attr.data[li].color = (val, val, val, 1.0)


def band_specs(corners):
    """The faces each inside corner darkens, by object: the normal's axis and sign and the box (mm) the face's vertices must lie in."""
    by = {}
    for k in corners:
        A, B = k["A"], k["B"]
        a, o_, third = k["a"], k["o"], k["third_axis"]
        # A's side face at o = c: normal along o, pointing away from A's body (-o at the low end, +o at the high end); the band: a within 8 mm of the plane on A's side
        lo, hi = [-1e9] * 3, [1e9] * 3
        lo[o_] = hi[o_] = k["c"]
        lo[third], hi[third] = k["third"]
        lo[a], hi[a] = (k["plane"] - k["sA"] * BAND, k["plane"]) if k["sA"] == 1 else (k["plane"], k["plane"] + BAND)
        by.setdefault(A.name, []).append({"axis_n": o_, "sign_n": -1.0 if k["e"] == 0 else 1.0, "lo": lo, "hi": hi})
        # B's exposed face at a = plane: normal along a pointing toward A (-sA); the band: o within 8 mm of c, beyond A's edge
        lo, hi = [-1e9] * 3, [1e9] * 3
        lo[a] = hi[a] = k["plane"]
        lo[third], hi[third] = k["third"]
        lo[o_], hi[o_] = (k["c"] - BAND, k["c"]) if k["e"] == 0 else (k["c"], k["c"] + BAND)
        by.setdefault(B.name, []).append({"axis_n": a, "sign_n": float(-k["sA"]), "lo": lo, "hi": hi})
    return by


def uv_box(o):
    """UVs at real scale (1 UV unit = 1 m), box projection per face: the face's dominant axis picks the plane."""
    me = o.data
    if "UVMap" in me.uv_layers:
        me.uv_layers.remove(me.uv_layers["UVMap"])
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        n = poly.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        for li, vi in zip(poly.loop_indices, poly.vertices):
            p = o.matrix_world @ me.vertices[vi].co
            if ax == 0:
                u, v = p.y, p.z
            elif ax == 1:
                u, v = p.x, p.z
            else:
                u, v = p.x, p.y
            uv.data[li].uv = (u, v)


# ---------------------------------------------------------------------------------------------------------------------------- glass panes
def pane(name, x0, x1, y_front, thick, z0, z1, mat, grid=True, seed_key=""):
    """A glass pane node (mm): origin at its front-face centre, the front face gridded so that the dirt band (6 mm round the edge, the lowest 25 mm) can be painted in COLOR_0 (1.0 clean, 0.8 band)."""
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    xs = [x0, x0 + 6.0, x1 - 6.0, x1] if grid else [x0, x1]
    zs = [z0, z0 + 25.0, z1 - 6.0, z1] if grid else [z0, z1]
    bm = bmesh.new()
    gv = [[bm.verts.new(((x - cx) * MM, 0.0, (z - cz) * MM)) for x in xs] for z in zs]
    faces = []
    for j in range(len(zs) - 1):
        for i in range(len(xs) - 1):
            f = bm.faces.new((gv[j][i], gv[j + 1][i], gv[j + 1][i + 1], gv[j][i + 1]))      # facing -y (toward the street)
            faces.append(f)
    res = bmesh.ops.extrude_face_region(bm, geom=faces)
    verts = [e for e in res["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0.0, thick * MM, 0.0), verts=verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = (cx * MM, y_front * MM, cz * MM)
    # the dirt mask on the front faces (COLOR_0 R = G = B: 1.0 clean, 0.8 band), 1.0 elsewhere; the cells of the grid are the band's own faces
    attr = me.color_attributes.new("Color", "FLOAT_COLOR", "CORNER")
    me.attributes.active_color = attr
    for poly in me.polygons:
        val = 1.0
        if poly.normal.y < -0.5:
            c = poly.center
            px, pz = c.x / MM + cx, c.z / MM + cz
            if grid and (px < x0 + 6.0 or px > x1 - 6.0 or pz < z0 + 25.0 or pz > z1 - 6.0):
                val = 0.8
        for li in poly.loop_indices:
            attr.data[li].color = (val, val, val, 1.0)
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li, vi in zip(poly.loop_indices, poly.vertices):
            p = me.vertices[vi].co
            uv.data[li].uv = (p.x + 0.5, p.z + 0.5)
    return ob


def tilts(names, kind):
    """Seeded tilts for a window's panes: yaw about the vertical axis within +-0.5 degrees, pitch about the horizontal one within +-0.3, none exactly zero, a spread of at least 0.3 degrees in each
    among the panes of one window (or the one pane's own tilt not zero). Returns {name: (pitch_deg, yaw_deg)}."""
    for seed in range(1, 200):
        rng = np.random.default_rng(zlib.crc32(("%s-%d" % (kind, seed)).encode()))
        out = {n: (float(rng.uniform(-0.3, 0.3)), float(rng.uniform(-0.5, 0.5))) for n in names}
        py = [v[0] for v in out.values()]
        yw = [v[1] for v in out.values()]
        if min(abs(v) for v in py + yw) < 0.04:
            continue
        if len(names) > 1 and (max(py) - min(py) < 0.3 + 0.02 or max(yw) - min(yw) < 0.3 + 0.02):
            continue
        return out
    raise RuntimeError("no tilt set")


# ---------------------------------------------------------------------------------------------------------------------------- the common nodes: nets, curtains, blinds, pendant, room card
def add_dressing(kind, mats, cloth, family="UP"):
    """Nets (a card each, hung from its own rod with brackets), curtains (cards on a pole with finials and brackets), blinds (cards from a headrail), the pendant shade and the room card."""
    Pl = 235.0 if kind in ("RC", "RC2") else 254.0
    nets = T.target()["nets"]
    objs = []
    R = cloth["net"]["rects"]
    for key, nm, torn in (("N1", "net__N1", False), ("N2", "net__N2", False), ("N3", "net__N3", False)):
        c = nets[key]["card"]
        o = card(nm, c["x"][0], c["x"][1], c["z"][0], c["z"][1], Pl, mats["net"], R[key])
        objs.append(o)
        # the rod it hangs from: a 5 mm rod along the net's head, 2 brackets (a 12 x 12 x 7 mm block each) on the lining's back (S22/S11) or the wall's inner face (RC: 215)
        zt = c["z"][1] - 6.0
        xr = c["x"][1] + 6.0
        objs.append(cyl_x("net_rod__" + key, -xr, xr, Pl, zt, 2.5, mats["paint"], 8))
        back = 250.8 if kind in ("S22", "S11") else 215.0
        for s, side in ((-1, "L"), (1, "R")):
            x = s * (xr + 1.0)
            objs.append(box_mm("net_bracket__%s_%s" % (key, side), x - 6.0, x + 6.0, back, Pl + 7.0 if kind in ("S22", "S11") else Pl + 4.0, zt - 6.0, zt + 6.0, mats["paint"]))
    if kind == "S22":
        # the torn net of the unlet flat (bay 3): one lower corner off its wire, the hem 80 mm out of true
        c = nets["N1"]["card"]
        objs.append(card("net__N1_torn", c["x"][0], c["x"][1], c["z"][0], c["z"][1], Pl, mats["net"], R["N1_torn"], skew=80.0))
    # curtains: C1 drawn (a card), C2 open (two cards, each 170 wide, taken from the left and right ends of the same fold map)
    cur = T.target()["curtains"]
    CR = cloth["curtain"]["rects"]["C1"]
    u0, v0, u1, v1 = CR
    objs.append(card("curtain__C1_drawn", -480, 480, 0, 1780, 262.0, mats["curtain"], CR))
    fw = 170.0 / 960.0 * (u1 - u0)
    objs.append(card("curtain__C2_open_L", -480, -310, 0, 1780, 262.0, mats["curtain"], (u0, v0, u0 + fw, v1)))
    objs.append(card("curtain__C2_open_R", 310, 480, 0, 1780, 262.0, mats["curtain"], (u1 - fw, v0, u1, v1)))
    # the pole (a 16 mm rod across the head, finials and two brackets to the wall's inner face: the cloth's head is gathered on it)
    objs.append(cyl_x("curtain_pole", -510, 510, 262.0, 1784.0, 8.0, mats["paint"], 10))
    for s, side in ((-1, "L"), (1, "R")):
        xe = s * 510.0
        objs.append(cyl_x("curtain_finial__" + side, min(xe, xe + s * 22.0), max(xe, xe + s * 22.0), 262.0, 1784.0, 12.0, mats["paint"], 10))
        xb = s * 480.0
        objs.append(box_mm("curtain_bracket__" + side, xb - 7.0, xb + 7.0, 215.0, 268.0, 1778.0, 1792.0, mats["paint"]))
    # blinds
    BR = cloth["blind"]["rects"]
    bl = T.target()["blinds"]
    for key, nm in (("B1", "blind__B1"), ("B2", "blind__B2"), ("B3", "blind__B3")):
        c = bl[key]["card"]
        o = card(nm, c["x"][0], c["x"][1], c["z"][0], c["z"][1], 240.0, mats["blind"], BR[key])
        objs.append(o)
    # headrails and the roller: the blinds hang from them (material `blind`, UVs on a plain place of the blind's own map)
    def solid_uv(o, key):
        u0_, v0_, u1_, v1_ = BR[key]
        if key == "B1":
            uvp = (u0_ + (u1_ - u0_) * 0.5, v1_ - (v1_ - v0_) * 0.0036)
        elif key == "B3":
            uvp = (u0_ + (u1_ - u0_) * 0.04, (v0_ + v1_) / 2)
        else:
            uvp = (u0_ + (u1_ - u0_) * 0.5, (v0_ + v1_) / 2)
        uv = o.data.uv_layers.active or o.data.uv_layers.new(name="UVMap")
        for li in range(len(o.data.loops)):
            uv.data[li].uv = uvp
    h1 = box_mm("blind_headrail__B1", -400, 400, 232, 252, 1650, 1676, mats["blind"])
    h3 = box_mm("blind_headrail__B3", -420, 420, 232, 252, 1640, 1668, mats["blind"])
    rl = cyl_x("blind_roller__B2", -396, 396, 244.0, 1662.0, 18.0, mats["blind"], 12)
    for o, k in ((h1, "B1"), (h3, "B3"), (rl, "B2")):
        solid_uv(o, k)
        objs.append(o)
    # the pendant: a paper drum shade 340 across and 240 high, its centre 550 mm behind the card (y 820), top 300 below the ceiling (the one real object in the room)
    objs.append(pendant(mats["shade"], 0.0, 820.0, 1536.0, 1776.0))
    # the room card
    if family == "UP":
        o = mesh_from("room__card", [(-1400, 270.0, -473.6), (1400, 270.0, -473.6), (1400, 270.0, 2076.4), (-1400, 270.0, 2076.4)], [(0, 1, 2, 3)], mats["card"], [(0, 0), (1, 0), (1, 1), (0, 1)])
        objs.append(o)
    return objs


def pendant(mat, xc, yc, z0, z1, rb=170.0, rt=105.0, n=24):
    verts, faces = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        verts.append((xc + rb * math.cos(a), yc + rb * math.sin(a), z0))
        verts.append((xc + rt * math.cos(a), yc + rt * math.sin(a), z1))
    for i in range(n):
        j = (i + 1) % n
        faces.append((2 * i, 2 * j, 2 * j + 1, 2 * i + 1))
    faces.append(tuple(2 * i + 1 for i in reversed(range(n))))          # the top (the cord's cap)
    ob = mesh_from("pendant__shade", verts, faces, mat)
    smooth(ob, 40.0)
    return ob


# ---------------------------------------------------------------------------------------------------------------------------- the kinds
def build_sash(kind, mats, cloth):
    lab = import_lab(kind)
    paint = mats["paint"]
    joinery = []
    glass_src = {}
    for nm, o in list(lab.items()):
        if nm.startswith("glass__"):
            glass_src[nm] = o
            continue
        o.data.materials.clear()
        o.data.materials.append(paint)
        joinery.append(o)
    # the panes: the lab's sheets, split at the bar for the 2/2
    panes = []
    ll, lu = glass_src["glass__lower_glass"], glass_src["glass__upper_glass"]
    (lx0, lx1), (ux0, ux1) = (bbox_mm(ll)[0][0], bbox_mm(ll)[1][0]), (bbox_mm(lu)[0][0], bbox_mm(lu)[1][0])
    ly, lz0, lz1 = bbox_mm(ll)[0][1], bbox_mm(ll)[0][2], bbox_mm(ll)[1][2]
    uy, uz0, uz1 = bbox_mm(lu)[0][1], bbox_mm(lu)[0][2], bbox_mm(lu)[1][2]
    for o in glass_src.values():
        bpy.data.objects.remove(o, do_unlink=True)
    if kind == "S22":
        spec = [("glass__lower_L", lx0, -4.7, ly, lz0, lz1), ("glass__lower_R", 4.7, lx1, ly, lz0, lz1), ("glass__upper_L", ux0, -4.7, uy, uz0, uz1), ("glass__upper_R", 4.7, ux1, uy, uz0, uz1)]
    else:
        spec = [("glass__lower", lx0, lx1, ly, lz0, lz1), ("glass__upper", ux0, ux1, uy, uz0, uz1)]
    tl = tilts([s[0] for s in spec], kind)
    for nm, x0, x1, y, z0, z1 in spec:
        o = pane(nm, x0, x1, y, 2.5, z0, z1, mats["glass"])
        pitch, yaw = tl[nm]
        o.rotation_euler = Euler((math.radians(pitch), 0.0, math.radians(yaw)), "XYZ")
        o["tilt_pitch_deg"] = round(pitch, 4)
        o["tilt_yaw_deg"] = round(yaw, 4)
        panes.append(o)
    return joinery, panes


def rc_parts(kind, mats):
    """The RC / RC2 frame, sashes, gasket strips and weld grooves from the target's parts tables (mm); bevel 1.5 mm; glass 4 mm. Returns (joinery objects, pane objects)."""
    K = T.target()["kinds"][kind]
    paint = mats["paint"]
    joinery, panes = [], []
    gl = []
    for p in K["parts_mm"]:
        nm = p["name"]
        x0, x1 = p["x"]
        y0, y1 = p["y_into_wall"]
        z0, z1 = p["z_up"]
        if nm.startswith("glass"):
            gl.append((nm.replace("glass_", "glass__"), x0, x1, y0, y1 - y0, z0, z1))
            continue
        o = box_mm("paint_joinery__" + nm, x0, x1, y0, y1, z0, z1, paint, bevel=1.5)
        joinery.append(o)
    tl = tilts([g[0] for g in gl], kind)
    for nm, x0, x1, y0, th, z0, z1 in gl:
        o = pane(nm, x0, x1, y0, th, z0, z1, mats["glass"])
        pitch, yaw = tl[nm]
        o.rotation_euler = Euler((math.radians(pitch), 0.0, math.radians(yaw)), "XYZ")
        o["tilt_pitch_deg"] = round(pitch, 4)
        o["tilt_yaw_deg"] = round(yaw, 4)
        panes.append(o)
    # the gasket line: a 6 mm strip (3 mm of seal, shaded over 6) just inside each glazed opening, on the glass's front plane (y 109.5 to 112.5)
    openings = []
    if kind == "RC":
        openings = [("lower", -365, 365, 60, 1172), ("top", -316, 316, 1291, 1567.4)]
    else:
        openings = [("casement", -316, -84, 109, 1022.4), ("fixed", 39, 365, 60, 1071.4), ("top", -365, 365, 1141.4, 1616.4)]
    for nm, x0, x1, z0, z1 in openings:
        yf, yb = 109.5, 112.5
        for tag, a in (("b", (x0 + 6, x1 - 6, z0, z0 + 6)), ("t", (x0 + 6, x1 - 6, z1 - 6, z1)), ("l", (x0, x0 + 6, z0, z1)), ("r", (x1 - 6, x1, z0, z1))):
            joinery.append(box_mm("paint_joinery__gasket_%s_%s" % (nm, tag), a[0], a[1], yf, yb, a[2], a[3], paint))
    # the welded-corner grooves: at each corner of the opening sash, a 6 mm shade line along the mitre (a strip 0.5 mm proud of the sash's face)
    sash_boxes = {"RC": (-361, 361, 1246, 1612.4, 45.0, 80.5), "RC2": (-361, -39, 64, 1067.4, 45.0, 80.5)}[kind]
    sx0, sx1, sz0, sz1, fw, sy = sash_boxes
    for tag, (cx, cz, sx, sz) in {"bl": (sx0, sz0, 1, 1), "br": (sx1, sz0, -1, 1), "tl": (sx0, sz1, 1, -1), "tr": (sx1, sz1, -1, -1)}.items():
        # a diagonal strip from the outer corner toward the inner corner: 6 wide, fw * sqrt2 long, built as a rotated thin box (the mitre of a welded sash corner)
        ln = fw * math.sqrt(2.0) * 0.98
        ang = math.atan2(sz, sx)
        verts = []
        for (u, v) in ((0, -3), (ln, -3), (ln, 3), (0, 3)):
            # u along the diagonal (from the corner inward), v across it
            dx, dz = math.cos(ang), math.sin(ang)
            px = cx + dx * u - dz * v
            pz = cz + dz * u + dx * v
            verts.append((px, pz))
        v3 = [(px, sy - 0.5, pz) for px, pz in verts]
        v3b = [(px, sy, pz) for px, pz in verts]
        faces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        joinery.append(mesh_from("paint_joinery__weld_%s" % tag, v3 + v3b, faces, paint))
    return joinery, panes


def finish_joinery(kind, joinery, extra_track=True):
    """Cuts for the track and the inside corners, the vertex colours, the UVs and the smooth shading."""
    boxes = [o for o in joinery if is_box(o) and "putty" not in o.name and "weld" not in o.name and "gasket" not in o.name]
    corners = find_corners(boxes)
    track = []
    if kind in ("S22", "S11") and extra_track:
        for o in joinery:
            if "pulley_stile" in o.name:
                track.append((o, 1, [184.1, 222.2]))
    apply_cuts(corners, track)
    by = band_specs(corners)
    for o in joinery:
        shade_object(o, kind, by, None)
        uv_box(o)
        smooth(o, 32.0)
    return corners


def build_kind(kind, out_path, log=print):
    reset()
    cloth = CL.build_all(os.path.join(T.KITWORK, "cloth"))
    mats = make_mats(kind, cloth)
    if kind in ("S22", "S11"):
        joinery, panes = build_sash(kind, mats, cloth)
    else:
        joinery, panes = rc_parts(kind, mats)
    corners = finish_joinery(kind, joinery)
    dress = add_dressing(kind, mats, cloth, "UP")
    log("%s: %d joinery nodes, %d panes, %d dressing nodes, %d inside corners" % (kind, len(joinery), len(panes), len(dress), len(corners)))
    export(out_path, [o for o in bpy.data.objects if o.type == "MESH"])
    total = sum(tris(o) for o in bpy.data.objects if o.type == "MESH")
    return {"kind": kind, "triangles": total, "nodes": len([o for o in bpy.data.objects if o.type == "MESH"]), "corners": len(corners), "path": out_path}


def build_gf_card(out_path, log=print):
    """The cottages' shared room card: 3.4 x 2.6 m on the card plane, centred between the house's two windows (x 0), floor 373.6 below the opening's bottom, ceiling 2226.4 above it, and the pendant at
    the room's centre (the window kits' own pendant nodes are switched off on a cottage)."""
    reset()
    cloth = CL.build_all(os.path.join(T.KITWORK, "cloth"))
    mats = make_mats("S22", cloth)
    o = mesh_from("room__card_gf", [(-1700, 270.0, -373.6), (1700, 270.0, -373.6), (1700, 270.0, 2226.4), (-1700, 270.0, 2226.4)], [(0, 1, 2, 3)], mats["card"], [(0, 0), (1, 0), (1, 1), (0, 1)])
    p = pendant(mats["shade"], 0.0, 820.0, 1686.0, 1926.0)
    p.name = "pendant__shade_gf"
    export(out_path, [o, p])
    return {"kind": "GF", "triangles": sum(tris(x) for x in (o, p)), "nodes": 2, "path": out_path}


def export(path, objs):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True, export_yup=True, export_cameras=False, export_lights=False, export_animations=False,
                              export_vertex_color="ACTIVE", export_all_vertex_colors=False, export_image_format="AUTO", export_extras=True, export_normals=True, export_texcoords=True,
                              export_materials="EXPORT")


if __name__ == "__main__":
    kinds = sys.argv[1:] or ["S22", "S11", "RC", "RC2", "GF"]
    for k in kinds:
        p = os.path.join(T.KITWORK, "out", GLB_NAMES[k])
        r = build_gf_card(p) if k == "GF" else build_kind(k, p)
        print(r, os.path.getsize(p))
