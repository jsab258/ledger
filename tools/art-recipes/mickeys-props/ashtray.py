"""A heavy round pressed-glass ashtray with four rests, smoked glass, with a
little ash and two stubbed-out cigarette ends in it (tobacco is allowed; the
ends carry no brand).

    blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/ashtray.py [-- --no-render] [-- --empty]

SIZE (read 6 October 2026):
- 6 in (152 mm) across: "Vintage Ravenhead Glass Co 4-Slot Ashtray Heavy Glass
  England 6\" Diameter", https://poshmark.com/listing/Vintage-Ravenhead-Glass-Co-4Slot-Ashtray-Heavy-Glass-England-6-Diameter-2-pcs-6834f1f9e48e860b88cbd467
  (no height given).
- 40 mm high at 150 mm across: V&A 44111 ashtray, Old Hall, made 1963-1981,
  https://collections.vam.ac.uk/item/O381809/44111-ashtray-robert-welch/
So 152 mm x 40 mm. The form is a plain generic one, no maker's pattern.
Origin: centre of the foot, z = 0.
"""
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _desk_common as C  # noqa: E402

D, H = 0.152, 0.040
R = D / 2


def build(empty=False):
    C.reset()
    glass = C.material("ashtray_smoked_glass", (0.60, 0.56, 0.50), 0.04, transmission=1.0, ior=1.52)
    prof = [
        (0.0, 0.0018), (0.050, 0.0018), (0.0545, 0.0010), (0.0565, 0.0), (0.0650, 0.0),
        (0.0690, 0.0012), (0.0712, 0.0040), (0.0730, 0.0120), (0.0748, 0.0260),
        (R - 0.0004, 0.0350), (R, 0.0375), (R - 0.0004, 0.0393), (R - 0.0018, H),
        (0.0625, H), (0.0608, 0.0394), (0.0598, 0.0370), (0.0570, 0.0300),
        (0.0525, 0.0215), (0.0480, 0.0168), (0.0420, 0.0150), (0.0200, 0.0144), (0.0, 0.0143),
    ]
    body = C.lathe("glass", prof, segs=72, mat=glass)
    # four rests across the rim, set at 45 degrees so two face the front
    cutters = []
    for k in range(4):
        a = math.radians(45 + 90 * k)
        c = Vector((0.068 * math.cos(a), 0.068 * math.sin(a), H + 0.0012))
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.0058, radius2=0.0058, depth=0.03)
        bmesh.ops.transform(bm, matrix=C.mat4(c, (0, math.pi / 2, a)), verts=bm.verts)
        me = bpy.data.meshes.new("rest")
        bm.to_mesh(me)
        bm.free()
        me.materials.append(glass)
        ob = bpy.data.objects.new("rest", me)
        bpy.context.scene.collection.objects.link(ob)
        cutters.append(ob)
    for ob in cutters:
        md = body.modifiers.new("rest", "BOOLEAN")
        md.operation = "DIFFERENCE"
        md.solver = "EXACT"
        md.object = ob
        md.material_mode = "TRANSFER"
    bpy.context.view_layer.objects.active = body
    for md in list(body.modifiers):
        bpy.ops.object.modifier_apply(modifier=md.name)
    for ob in cutters:
        bpy.data.objects.remove(ob)
    C.bevel_part(body, 0.0009, segs=2, angle=40)
    body["sharp_angle"] = 40.0

    if not empty:
        ash = C.material("ashtray_ash", (0.32, 0.31, 0.30), 0.95)
        filt = C.material("cigarette_filter_cork", (0.78, 0.58, 0.36), 0.75)
        rnd = random.Random(11)
        # a low heap of ash, off-centre
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
        for v in bm.verts:
            # smooth lumps (no per-vertex noise, which folds the UVs)
            x, y, z = v.co
            v.co *= 1.0 + 0.10 * math.sin(3.1 * x + 1.3) * math.cos(2.7 * y - 0.4) + 0.06 * math.sin(5.0 * y + 2.0 * z)
        bmesh.ops.transform(bm, matrix=C.mat4((0.008, 0.006, 0.0150), (0, 0, 0.4), (0.030, 0.024, 0.0035)),
                            verts=bm.verts)
        heap = C._link("ash", bm, ash)
        heap["no_wn"] = True
        heap["sharp_angle"] = 80.0

        def end(name, start, heading, droop, paper_len):
            # a crushed filter end: 21 mm cork filter, then a short bent
            # stub of burnt paper buckled where it was pressed out
            d = Vector((math.cos(heading), math.sin(heading), 0))
            side = Vector((-d.y, d.x, 0))
            p0 = Vector(start)
            ctrl = [p0, p0 + d * 0.010, p0 + d * 0.021]
            fp = C.resample(C.catmull(ctrl, 6), 0.0015)[0]
            t = C.tube(name + "_filter", fp, 0.0039, sides=12, mat=filt)
            t["sharp_angle"] = 50.0
            q = fp[-1]
            ctrl2 = [q, q + d * 0.004 + side * 0.002 + Vector((0, 0, -droop * 0.5)),
                     q + d * paper_len + side * 0.004 + Vector((0, 0, -droop))]
            pp = C.resample(C.catmull(ctrl2, 6), 0.0012)[0]
            n = len(pp)
            radii = [0.0039 * (1.0 - 0.45 * i / (n - 1)) * (0.8 if i % 2 else 1.0) for i in range(n)]
            radii[0] = 0.0039
            s = C.tube(name + "_paper", pp, 0.0039, sides=12, mat=ash, radii=radii)
            s["sharp_angle"] = 30.0
        end("end_a", (-0.030, -0.012, 0.0192), math.radians(25), 0.002, 0.009)
        end("end_b", (0.016, 0.022, 0.0188), math.radians(200), 0.0025, 0.007)

    o = C.cli()
    stem = "ashtray-empty" if empty else "ashtray"
    ob, info = C.finish_prop(stem, stem.replace("-", "_"), ao_distance=0.02, edge_span=0.10,
                             ref={"x": D, "y": D, "z": H}, render=o["render"],
                             preview_kw={"azimuth": -35, "elevation": 32})
    return info


if __name__ == "__main__":
    build(empty="--empty" in C.cli()["argv"])
