"""The fish market's painted plywood A-board (variant AB1), by script, at real size, from its target.

    python -I tools/meshgen/blender/clutter/a_board_paint.py --out F:/LedgerTools/tmp/clutter/a-board/a_board_paint.png
    blender --background --factory-startup --python tools/meshgen/blender/clutter/a_board.py -- --out F:/LedgerTools/tmp/clutter/a-board/script-1.glb

    --paint <png>   the painted face (default: a_board_paint.png beside --out; made by the first line if missing)
    --turn <deg>    turn the whole board about the vertical before export (180 photographs the back leaf's face
                    with the same sheet maker; the piece itself is always exported with 0)

Every number comes from the target, production/cloud-week/targets/street-dressing/
a-board/target.json (millimetres, z up, the front leaf's painted face looking -y,
the pivot at the middle of the feet's line on the paving): variant AB1's 23 parts
with their centres, sizes, polygons, cylinders, the chain's catenary points and
each leaf's transform (a roll of -12 or +12 degrees about the ridge pivot and a
lift that sets the inner foot edge on the paving); the materials' sRGB, roughness
and metal. Each part is built in its own leaf's frame and hung by its xf exactly as
the target's own geometry library does (sd_lib.rot: Rz(yaw) Ry(pitch) Rx(roll)),
then written in metres as one .glb, a named mesh per part under one root.

What the target leaves to the builder, and what was chosen:
- the leaf (f_main and its two feet) is one material, ply_paint, whose colour is the
  painted texture of a_board_paint.py: the outer face carries the fish list,
  unmirrored and the right way up on both leaves (on each face the image's right is
  the viewer's right); the inner face, top edge, cut edges, foot soles and the
  arch's cuts sample strips of bare, laminated and dirty ply below the face on the
  same image, so the back of each leaf is bare as the target says;
- each screw eye is a shank and a ring within the target's cylinder (r 5, its tip
  at the cylinder's end, where the chain's points begin), not a solid peg;
- the chain is a six-sided tube along the target's 17 catenary points (its
  builder note: the links are a texture's business, not geometry's);
- the feet's tops, hidden against the panel's underside, are left out; the 2 mm
  eased arrises and the 2 mm swelling at the foot's corners are not modelled
  (below what any view of a 1 m board resolves).
Every surface gets a UV (box-projected in metres where it carries no texture) so a
lightmap can be generated from it.
"""
import json
import math
import os
import subprocess
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(name, default=None):
    return argv[argv.index(name) + 1] if name in argv else default


try:
    HERE = os.path.dirname(os.path.abspath(__file__))
except NameError:
    HERE = os.path.dirname(os.path.abspath(sys.argv[sys.argv.index("--python") + 1]))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = arg("--out", "a_board.glb")
TARGET = arg("--target", os.path.join(REPO, "production", "cloud-week", "targets", "street-dressing", "a-board", "target.json"))
PAINT = arg("--paint", os.path.join(os.path.dirname(os.path.abspath(OUT)), "a_board_paint.png"))
TURN = float(arg("--turn", "0"))
VARIANT = "AB1"

if not os.path.exists(PAINT):
    subprocess.run(["python", "-I", os.path.join(HERE, "a_board_paint.py"), "--out", PAINT, "--target", TARGET], check=True)
LAYOUT = json.load(open(os.path.splitext(PAINT)[0] + ".json", encoding="utf-8"))
T = json.load(open(TARGET, encoding="utf-8"))
V = T["variants"][VARIANT]
PARTS = V["parts"]
BYID = {p["id"]: p for p in PARTS}

bpy.ops.wm.read_factory_settings(use_empty=True)


# ------------------------------------------------------------------ materials (the target's, by its ids)
def linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


MATS = {}
for mid in sorted({p["material"] for p in PARTS}):
    t = T["materials"][mid]
    m = bpy.data.materials.new(mid)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = tuple(linear(c) for c in t["srgb"]) + (1.0,)
    b.inputs["Roughness"].default_value = t["rough"]
    b.inputs["Metallic"].default_value = 1.0 if t["metal"] else 0.0
    if mid == "ply_paint":
        tex = m.node_tree.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(PAINT)
        tex.image.colorspace_settings.name = "sRGB"
        m.node_tree.links.new(tex.outputs["Color"], b.inputs["Base Color"])
    MATS[mid] = m


# ------------------------------------------------------------------ the shapes, in a part's own frame (mm)
def bm_from(verts, faces, smooth):
    bm = bmesh.new()
    bv = [bm.verts.new(v) for v in verts]
    for f, s in zip(faces, smooth):
        face = bm.faces.new([bv[i] for i in f])
        face.smooth = s
    bm.normal_update()
    return bm


def box(c, s):
    c, h = Vector(c), Vector(s) / 2.0
    vs = [c + Vector((sx * h.x, sy * h.y, sz * h.z)) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    fs = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    bm = bm_from(vs, fs, [False] * 6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def prism(poly, w, drop_top_z=None):
    n = len(poly)
    vs = [Vector((x, w[0], z)) for x, z in poly] + [Vector((x, w[1], z)) for x, z in poly]
    fs = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
    fs += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    bm = bm_from(vs, fs, [False] * len(fs))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if drop_top_z is not None:                 # the side lying against the panel's underside: never seen
        hidden = [f for f in bm.faces if all(abs(v.co.z - drop_top_z) < 1e-6 for v in f.verts)]
        bmesh.ops.delete(bm, geom=hidden, context="FACES_ONLY")
    return bm


def frame(e):
    e = e.normalized()
    t = Vector((1, 0, 0)) if abs(e.x) < 0.9 else Vector((0, 1, 0))
    u = e.cross(t).normalized()
    return e, u, e.cross(u)


def cyl(p0, p1, r, n=10, caps=True, bm=None):
    p0, p1 = Vector(p0), Vector(p1)
    e, u, v = frame(p1 - p0)
    ring = [u * math.cos(2 * math.pi * i / n) + v * math.sin(2 * math.pi * i / n) for i in range(n)]
    bm = bm or bmesh.new()
    bv = [bm.verts.new(p0 + d * r) for d in ring] + [bm.verts.new(p1 + d * r) for d in ring]
    new = [bm.faces.new((bv[i], bv[(i + 1) % n], bv[n + (i + 1) % n], bv[n + i])) for i in range(n)]
    for f in new:
        f.smooth = True
    if caps:
        new += [bm.faces.new(bv[:n]), bm.faces.new(bv[n:][::-1])]
    bmesh.ops.recalc_face_normals(bm, faces=new)
    return bm


def screw_eye(p0, p1, r_out, plane_normal):
    """a shank from p0 and a ring whose outer tip is p1, the ring's outer radius r_out, its plane holding the axis"""
    p0, p1 = Vector(p0), Vector(p1)
    e = (p1 - p0).normalized()
    nrm = Vector(plane_normal).normalized()
    side = nrm.cross(e).normalized()
    rw = 1.3                                     # the ring's wire radius
    R = r_out - rw
    c = p1 - e * r_out
    bm = bmesh.new()
    nm, nn = 10, 4
    rows = []
    for i in range(nm):
        a = 2 * math.pi * i / nm
        radial = e * math.cos(a) + side * math.sin(a)
        rows.append([bm.verts.new(c + radial * (R + rw * math.cos(2 * math.pi * j / nn)) + nrm * rw * math.sin(2 * math.pi * j / nn))
                     for j in range(nn)])
    for i in range(nm):
        for j in range(nn):
            f = bm.faces.new((rows[i][j], rows[(i + 1) % nm][j], rows[(i + 1) % nm][(j + 1) % nn], rows[i][(j + 1) % nn]))
            f.smooth = True
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    cyl(p0, c - e * (R - 0.5 * rw), 1.6, n=6, caps=False, bm=bm)        # the shank, its ends buried
    bm.normal_update()
    return bm


def tube(pts, r, n=6):
    pts = [Vector(p) for p in pts]
    bm = bmesh.new()
    rings = []
    for k, p in enumerate(pts):
        tng = (pts[min(k + 1, len(pts) - 1)] - pts[max(k - 1, 0)]).normalized()
        u = Vector((1, 0, 0)) - tng * tng.x
        u.normalize()
        v = tng.cross(u)
        rings.append([bm.verts.new(p + (u * math.cos(2 * math.pi * i / n) + v * math.sin(2 * math.pi * i / n)) * r)
                      for i in range(n)])
    for k in range(len(rings) - 1):
        for i in range(n):
            f = bm.faces.new((rings[k][i], rings[k][(i + 1) % n], rings[k + 1][(i + 1) % n], rings[k + 1][i]))
            f.smooth = True
    for rg in (rings[0], rings[-1]):
        bm.faces.new(rg).smooth = False
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def shape(p):
    k = p["type"]
    if k == "box":
        return box(p["c"], p["s"])
    if k == "prism":
        top = max(z for _, z in p["poly"])
        main = BYID[p["id"][:2] + "main"]
        under = main["c"][2] - main["s"][2] / 2.0
        return prism(p["poly"], p["w"], drop_top_z=top if abs(top - under) < 1.5 else None)
    if k == "cyl" and "eye" in p["id"]:
        return screw_eye(p["p0"], p["p1"], p["r0"], (0, 1, 0))
    if k == "cyl":
        return cyl(p["p0"], p["p1"], p["r0"], n=10)
    if k == "wire":
        return tube(p["pts"], p["r"], n=6)
    raise ValueError(k)


# ------------------------------------------------------------------ UVs
CW, CH = LAYOUT["canvas_mm"]
ZB = LAYOUT["canvas_z_bottom_mm"]
SU0, SU1 = LAYOUT["strip_u"]


def leaf_of(pid):
    main = BYID[pid[:2] + "main"]
    sgn = 1.0 if main["c"][1] > 0 else -1.0          # the outer face's side: -y front leaf, +y back leaf
    outer_y = main["c"][1] + sgn * main["s"][1] / 2.0
    top = main["c"][2] + main["s"][2] / 2.0
    return sgn, outer_y, main["s"][1], top, main["s"][0]


def strip_uv(name, s, t):
    lo, hi = LAYOUT["strips"][name]["use"]
    return Vector((SU0 + (SU1 - SU0) * min(max(s, 0.0), 1.0),
                   (hi - (hi - lo) * min(max(t, 0.0), 1.0) - ZB) / CH))


def uv_leaf(bm, pid):
    sgn, outer_y, thick, top, width = leaf_of(pid)
    right = -sgn                                    # the viewer's right on that face: +x in front, -x behind
    uvl = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        n = f.normal
        cen = f.calc_center_median()
        if n.y * sgn > 0.9:
            kind = "face"
        elif n.y * sgn < -0.9:
            kind = "inner"
        elif abs(cen.x) > width / 2.0 - 0.5 and abs(n.x) > 0.9:
            kind = "edge"
        elif cen.z > top - 0.5:
            kind = "top"
        else:
            kind = "dirty"
        for lp in f.loops:
            x, y, z = lp.vert.co
            dpt = abs(y - outer_y) / thick
            if kind == "face":
                lp[uvl].uv = ((x * right + width / 2.0) / width, (z - ZB) / CH)
            elif kind == "inner":
                lp[uvl].uv = strip_uv("inner", (x + width / 2.0) / width, z / top)
            elif kind == "top":
                lp[uvl].uv = strip_uv("inner", (x + width / 2.0) / width, 0.5 + 0.05 * dpt)
            elif kind == "edge":
                lp[uvl].uv = strip_uv("edge", z / top, dpt)
            else:
                lp[uvl].uv = strip_uv("dirty", (x + width / 2.0) / width, dpt)


def uv_box(bm):
    uvl = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        a, b = [(1, 2), (0, 2), (0, 1)][ax]
        for lp in f.loops:
            lp[uvl].uv = (lp.vert.co[a] * 0.001, lp.vert.co[b] * 0.001)


# ------------------------------------------------------------------ the transform (sd_lib.rot and PartSet)
def rot(yaw=0.0, pitch=0.0, roll=0.0):
    return (Matrix.Rotation(math.radians(yaw), 4, "Z") @ Matrix.Rotation(math.radians(pitch), 4, "Y")
            @ Matrix.Rotation(math.radians(roll), 4, "X"))


def xf_matrix(p):
    xf = p.get("xf")
    if not xf:
        return Matrix.Identity(4)
    o = Vector(xf.get("pivot", [0, 0, 0]))
    return Matrix.Translation(o + Vector(xf.get("t", [0, 0, 0]))) @ rot(*xf.get("rot", [0, 0, 0])) @ Matrix.Translation(-o)


TO_M = Matrix.Rotation(math.radians(TURN), 4, "Z") @ Matrix.Scale(0.001, 4)
root = bpy.data.objects.new("a_board_" + VARIANT, None)
bpy.context.scene.collection.objects.link(root)
world_mm = {}
local_mm = {}
for p in PARTS:
    bm = shape(p)
    local_mm[p["id"]] = [v.co.copy() for v in bm.verts]
    if p["material"] == "ply_paint":
        uv_leaf(bm, p["id"])
    else:
        uv_box(bm)
    M = xf_matrix(p)
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    world_mm[p["id"]] = [v.co.copy() for v in bm.verts]
    bmesh.ops.transform(bm, matrix=TO_M, verts=bm.verts)
    me = bpy.data.meshes.new(p["id"])
    bm.to_mesh(me)
    bm.free()
    me.materials.append(MATS[p["material"]])
    ob = bpy.data.objects.new(p["id"], me)
    bpy.context.scene.collection.objects.link(ob)
    ob.parent = root

# ------------------------------------------------------------------ measured back off what was built
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
tris = {o.name: sum(len(f.vertices) - 2 for f in o.data.polygons) for o in meshes}


def bbox(ids):
    pts = [v for i in ids for v in world_mm[i]]
    lo = [min(v[k] for v in pts) for k in range(3)]
    hi = [max(v[k] for v in pts) for k in range(3)]
    return lo, hi


excl = set(V.get("overall_exclude", []))
lo_x, hi_x = bbox([i for i in world_mm if i not in excl])
lo_a, hi_a = bbox(list(world_mm))
ov, tol = V["overall"], V["overall_tol"]
size_x = [hi_x[k] - lo_x[k] for k in range(3)]
overall = {"w": [round(size_x[0], 2), ov["w"]], "d": [round(size_x[1], 2), ov["d"]], "h": [round(size_x[2], 2), ov["h"]],
           "tol": tol, "base_z": round(lo_x[2], 2),
           "pass": all(abs(a - b) <= tol for a, b in zip(size_x, (ov["w"], ov["d"], ov["h"])))}
lm = local_mm["f_main"]
foot = [v for v in local_mm["f_foot_l"] if -1.0 <= v.z <= 1.0]
eye_lo, eye_hi = bbox(["f_eye"])
ch = world_mm["chain"]
pts = [Vector(q) for q in BYID["chain"]["pts"]]
clen = sum((pts[i + 1] - pts[i]).length for i in range(len(pts) - 1))
lean = math.degrees((xf_matrix(BYID["f_main"]).to_3x3() @ Vector((0, 0, 1))).angle(Vector((0, 0, 1))))
pins = [bbox([i]) for i in ("hinge_pin_l", "hinge_pin_r")]
numbers = {
    "N1 leaf width": [max(v.x for v in lm) - min(v.x for v in lm), 600.0, 15.0],
    "N2 leaf length": [max(v.z for v in lm), 990.0, 25.0],
    "N3 ply thickness": [max(v.y for v in lm) - min(v.y for v in lm), 12.0, 3.0],
    "N4 arch height": [min(v.z for v in lm), 58.0, 6.0],
    "N5 foot width at ground": [max(v.x for v in foot) - min(v.x for v in foot), 118.0, 8.0],
    "N6 arch flat top half width": [min(v.x for v in local_mm["f_foot_r"]), 138.0, 15.0],
    "N7 lean deg": [lean, 12.0, 3.0],
    "N8 height to ridge": [size_x[2], 972.4, 30.0],
    "N9 depth foot to foot": [size_x[1], 435.1, 40.0],
    "N10 chain low to eye top": [eye_hi[2] - min(v.z for v in ch), 249.5, 40.0],
    "N11 eye height": [(eye_lo[2] + eye_hi[2]) / 2.0, 590.0, 30.0],
    "N12 hinge spacing": [((pins[1][0][0] + pins[1][1][0]) - (pins[0][0][0] + pins[0][1][0])) / 2.0, 410.0, 30.0],
}
numbers = {k: {"built": round(a, 2), "target": b, "tol": c, "pass": abs(a - b) <= c} for k, (a, b, c) in numbers.items()}
chain = {"length_over_span": round(clen / (pts[-1] - pts[0]).length, 3), "lowest_mm": round(min(v.z for v in ch), 1),
         "pass": clen / (pts[-1] - pts[0]).length >= 1.15 and min(v.z for v in ch) > 150.0}

# the painted face's orientation on each leaf, from the built mesh: +u to the viewer's right, +v up, not mirrored
orient = {}
for o in meshes:
    if o.name not in ("f_main", "r_main"):
        continue
    me = o.data
    uvd = me.uv_layers["UVMap"].data
    sgn = leaf_of(o.name)[0]
    face = None
    for f in me.polygons:
        n = (TO_M.inverted().to_3x3() @ f.normal).normalized()
        if f.area > 0 and (xf_matrix(BYID[o.name]).inverted().to_3x3() @ n).y * sgn > 0.9:
            face = f
    li = list(face.loop_indices)
    P = [TO_M.inverted() @ me.vertices[me.loops[i].vertex_index].co for i in li]
    U = [uvd[i].uv for i in li]
    du, dv = U[1] - U[0], U[2] - U[0]
    dp1, dp2 = P[1] - P[0], P[2] - P[0]
    det = du.x * dv.y - du.y * dv.x
    a = (dp1 * dv.y - dp2 * du.y) / det             # dP/du
    b = (dp2 * du.x - dp1 * dv.x) / det             # dP/dv
    nrm = (TO_M.inverted().to_3x3() @ face.normal).normalized()
    viewer_right = Vector((0, 0, 1)).cross(nrm).normalized()
    orient[o.name] = {"outward": [round(c, 3) for c in nrm], "u_to_viewer_right": round(a.normalized().dot(viewer_right), 3),
                      "v_up": round(b.normalized().dot(Vector((0, 0, 1))), 3), "unmirrored": a.cross(b).dot(nrm) > 0,
                      "pass": a.normalized().dot(viewer_right) > 0.99 and b.normalized().z > 0.95 and a.cross(b).dot(nrm) > 0}

report = {
    "variant": VARIANT, "out": OUT, "turn_deg": TURN, "parts": len(meshes), "parts_target": len(PARTS),
    "triangles": sum(tris.values()), "triangles_by_part": tris,
    "overall_without_eyes_and_chain_mm": overall,
    "bbox_all_mm": {"lo": [round(c, 2) for c in lo_a], "hi": [round(c, 2) for c in hi_a]},
    "numbers": numbers, "chain": chain, "face_orientation": orient,
    "materials": {mid: {"srgb_target": T["materials"][mid]["srgb"], "rough": T["materials"][mid]["rough"],
                        "metal": T["materials"][mid]["metal"], "textured": mid == "ply_paint"} for mid in MATS},
    "paint": {"file": PAINT, "image": LAYOUT["image"], "px_per_mm": LAYOUT["px_per_mm"],
              "ground_srgb_measured": LAYOUT["ground_srgb_measured"]},
}
if TURN == 0:
    json.dump(report, open(os.path.splitext(OUT)[0] + ".checks.json", "w"), indent=1)
print("a_board triangles:", report["triangles"], "parts:", len(meshes))
print("a_board overall (no eyes, chain):", json.dumps(overall))
for k, v in numbers.items():
    print("  %-28s %8.2f  target %6.1f +-%4.1f  %s" % (k, v["built"], v["target"], v["tol"], "ok" if v["pass"] else "FAIL"))
print("a_board chain:", json.dumps(chain))
print("a_board faces:", json.dumps(orient))

bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_image_format="AUTO", export_yup=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.splitext(OUT)[0] + ".blend")
print("a_board written:", OUT)
