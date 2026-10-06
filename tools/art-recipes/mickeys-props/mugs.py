"""Two office mugs for Mickey's front office: a plain off-white one with a tea
line inside, and a brown-glazed one with a chip out of the rim.

    blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/mugs.py [-- --no-render]

Outputs mug.glb and mug-chipped.glb (game-inputs/production/assets/mickeys-props),
their .blend files and previews (F:/LedgerTools/mickeys-props).

SIZE. Science Museum Group object Y1980.1.39, a porcelain mug made in
Stoke-on-Trent in 1978: overall 92 mm x 114 mm x 81 mm (height, width over the
handle, body diameter); read 6 October 2026,
https://collection.sciencemuseumgroup.org.uk/objects/co8405537/flying-scotsman-commemotive-mug
The shape is a plain straight-sided can mug with a foot ring, no maker's.
Origin: centre of the body's foot, z = 0; handle toward +X, so from the front
(-Y) the handle is on the right.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _desk_common as C  # noqa: E402

H, R, W_HANDLE = 0.092, 0.0405, 0.114
WALL = 0.0040


def profile():
    """(r, z) from the underside centre, out over the foot, up the outside,
    over the rim, down the inside to the inner floor centre. Returns points and
    a per-segment tag."""
    ri = R - WALL
    pts = [
        (0.0, 0.0030, "foot"), (0.026, 0.0030, "foot"), (0.0300, 0.0022, "foot"),
        (0.0312, 0.0004, "foot"), (0.0322, 0.0, "foot"), (0.0352, 0.0, "foot"),
        (0.0368, 0.0006, "foot"), (0.0384, 0.0030, "out"), (0.0398, 0.0075, "out"),
        (0.0404, 0.0140, "out"), (R, 0.030, "out"), (R, 0.060, "out"), (R, 0.0840, "out"),
        (R - 0.0001, 0.0895, "out"), (R - 0.0006, 0.0912, "out"), (R - 0.0018, H, "out"),
        (ri + 0.0012, H - 0.0001, "in"), (ri + 0.0002, H - 0.0012, "in"),
        (ri, H - 0.0040, "in"), (ri, 0.075, "in"), (ri, 0.0715, "tea"), (ri, 0.0690, "in"),
        (ri, 0.050, "in"), (ri, 0.030, "in"), (ri - 0.0003, 0.0170, "in"),
        (ri - 0.0020, 0.0115, "in"), (ri - 0.0060, 0.0090, "in"), (0.022, 0.0082, "in"),
        (0.0, 0.0080, "in"),
    ]
    return pts


def build(stem, glaze, biscuit, tea=None, chip=False):
    C.reset()
    mats = {"glaze": glaze(), "biscuit": biscuit()}
    if tea:
        mats["tea"] = tea()
    order = list(mats)
    pts = profile()
    prof = [(r, z) for r, z, _ in pts]

    def slot(i):
        tag = pts[i][2]
        if tag == "foot":
            # the foot ring's flat bottom is unglazed biscuit, the recess glazed
            r0, r1 = pts[i][0], pts[i + 1][0]
            return order.index("biscuit") if r0 >= 0.0300 and r1 <= 0.0370 else 0
        if tag == "tea" and "tea" in mats:
            return order.index("tea")
        return 0
    body = C.lathe("body", prof, segs=64, mat=None, mat_of=slot)
    for k in order:
        body.data.materials.append(mats[k])
    body["no_wn"] = True
    body["sharp_angle"] = 70.0

    # handle: an oval section swept round a C in the XZ plane at +X
    xo = W_HANDLE - R                       # outer reach of the handle from the axis
    t = 0.0085                              # section thickness in the C's plane
    # a squared-off D (superellipse) from the top joint round to the bottom one
    xc, zc, b, ex = 0.0415, 0.048, 0.0265, 2.0 / 2.6
    a_ = xo - t / 2 - xc
    # the joints sit at x = 37.8 mm, inside the 4 mm wall (36.5 to 40.5 mm)
    a_end = math.pi - math.acos(((xc - 0.0378) / a_) ** (1 / ex))
    path = []
    for k in range(61):
        ang = a_end - (2 * a_end) * k / 60
        c_, s_ = math.cos(ang), math.sin(ang)
        x = xc + a_ * math.copysign(abs(c_) ** ex, c_)
        z = zc + b * math.copysign(abs(s_) ** ex, s_)
        path.append(Vector((x, 0, z)))
    path, _ = C.resample(path, 0.0020)
    sec = C.ellipse(0.0125, t, n=14)
    # taper the section a little toward the joints
    n = len(path)
    sc = [0.92 + 0.08 * math.sin(math.pi * i / (n - 1)) for i in range(n)]
    h = C.profile_sweep("handle", path, sec, mat=mats["glaze"], scale=sc)
    h["no_wn"] = True
    h["sharp_angle"] = 80.0

    if chip:
        # a chip out of the rim at the front left, cut by an irregular stone
        import bmesh
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.0085)
        import random
        rnd = random.Random(7)
        for v in bm.verts:
            v.co *= 1.0 + rnd.uniform(-0.18, 0.18)
            v.co.z *= 0.75
        a = math.radians(-112)
        c = Vector((R * math.cos(a), R * math.sin(a), H + 0.0012))
        bmesh.ops.transform(bm, matrix=C.mat4(c, (0.35, -0.2, a)), verts=bm.verts)
        me = bpy.data.meshes.new("chip_cutter")
        bm.to_mesh(me)
        bm.free()
        cutter = bpy.data.objects.new("chip_cutter", me)
        bpy.context.scene.collection.objects.link(cutter)
        me.materials.append(mats["biscuit"])
        md = body.modifiers.new("chip", "BOOLEAN")
        md.operation = "DIFFERENCE"
        md.solver = "EXACT"
        md.object = cutter
        md.material_mode = "TRANSFER"
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.select_all(action="DESELECT")
        body.select_set(True)
        bpy.ops.object.modifier_apply(modifier="chip")
        bpy.data.objects.remove(cutter)
        body["sharp_angle"] = 45.0

    o = C.cli()
    ref = {"z": H, "x": W_HANDLE, "y": 2 * R}
    ob, info = C.finish_prop(stem, stem.replace("-", "_"), ao_distance=0.03, edge_span=0.12,
                             ref=ref, render=o["render"],
                             preview_kw={"azimuth": -40, "elevation": 24})
    return info


def glaze_white():
    return C.material("mug_glaze_offwhite", (0.86, 0.84, 0.79), 0.07, coat=0.0)


def glaze_brown():
    return C.material("mug_glaze_brown", (0.21, 0.115, 0.06), 0.10)


def biscuit():
    return C.material("mug_biscuit", (0.80, 0.74, 0.64), 0.85)


def tea():
    return C.material("mug_tea_line", (0.60, 0.45, 0.28), 0.12)


if __name__ == "__main__":
    build("mug", glaze_white, biscuit, tea=tea, chip=False)
    build("mug-chipped", glaze_brown, biscuit, tea=None, chip=True)
