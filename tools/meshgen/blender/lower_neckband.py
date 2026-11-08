"""A skinned jumper's crew neckband brought down to a crew neck's height, each column shortened toward its own seam.

    blender -b SKINNED.blend -P tools/meshgen/blender/lower_neckband.py -- PACKED.png OUT_DIR NAME
            [--height 0.022] [--above 1.45] [--selftest]

WHY, 8 November 2026 (n02-9-knit-and-neckband; his note on the dressed men, "Darren's neckband stands up stiffly with
small peaks"). Measured on darren_jumper_skinned.blend: the band's columns stand 25 to 47 mm tall and its top rises
about 35 mm higher at the sides than at front and back, so it reads as a short polo collar with points at the
shoulders. A crew neckband is about 20 to 25 mm deep (the plan's band, JUMPER-PLAN-2026-10-29.md; build_rib_band.py's
neckband is drawn to the band's cut height). Its seam ring (where the band meets the body) is the neckline's shape and
stays; only the band above it is shortened.

HOW: the band's points are the rib part (the packed map's green 0.25, read at each corner's UV) above --above metres;
its seam ring is those of them joined by an edge to a point outside the rib. Each band point keeps its direction from
the seam point nearest it round the neck (by angle about the band's centre) and its distance from it is scaled by
--height over that column's own height, so every column ends --height above its seam. Weights, UVs and faces are left
as they are (the band's points stay over the same skin, lower); the armature and mesh are exported as skin_garment.py
exports them. OUT_DIR gets NAME_skinned.fbx, NAME_skinned.blend and band.json (each 20-degree sector's height before
and after).
"""
import json
import math
import os
import sys

import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


def sectors(P, cx, cy, z0):
    """Per 20-degree sector: points, the band's height above its seam (max), as [angle, n, mm]."""
    a = np.degrees(np.arctan2(P[:, 1] - cy, P[:, 0] - cx))
    out = []
    for s in range(-180, 180, 20):
        m = (a >= s) & (a < s + 20)
        if m.any():
            out.append([s, int(m.sum()), round(float((P[m, 2] - z0[m]).max() * 1000), 1)])
    return out


def scale_columns(P, seam, height):
    """Each point moved toward the seam point nearest it by angle, to height over its column's height; returns new P,
    the seam index used per point and each column's height before."""
    cx, cy = seam[:, 0].mean(), seam[:, 1].mean()
    sa = np.arctan2(seam[:, 1] - cy, seam[:, 0] - cx)
    pa = np.arctan2(P[:, 1] - cy, P[:, 0] - cx)
    d = np.abs(np.angle(np.exp(1j * (pa[:, None] - sa[None, :]))))
    near = d.argmin(axis=1)
    off = P - seam[near]
    length = np.linalg.norm(off, axis=1)
    tall = np.zeros(len(seam))
    for i in range(len(seam)):
        m = near == i
        if m.any():
            tall[i] = (P[m, 2] - seam[i, 2]).max()
    col = np.maximum(tall[near], 1e-4)
    k = np.minimum(1.0, height / col)
    return seam[near] + off * k[:, None], near, tall, length


def selftest():
    # a straight band 40 mm tall on a level seam ring of radius 6 cm, and one column 50 mm tall
    ring = np.array([[0.06 * math.cos(t), 0.06 * math.sin(t), 1.6] for t in np.linspace(0, 2 * math.pi, 24, endpoint=False)])
    P = np.vstack([ring + [0, 0, h] for h in (0.0, 0.02, 0.04)] + [ring[:1] + [0, 0, 0.05]])
    Q, near, tall, _ = scale_columns(P, ring, 0.022)
    checks = [("every column ends at the height", abs((Q[:, 2] - ring[near][:, 2]).max() - 0.022) < 1e-9, ""),
              ("the seam stays where it is", np.allclose(Q[:24], ring), ""),
              ("the taller column is shortened by its own height", abs(Q[-1, 2] - 1.622) < 1e-9, str(Q[-1])),
              ("a column already short is left alone", np.allclose(scale_columns(ring + [0, 0, 0.01], ring, 0.022)[0], ring + [0, 0, 0.01]), "")]
    bad = [c for c in checks if not c[1]]
    for c in bad:
        print("lower_neckband selftest FAIL %s %s" % (c[0], c[2]))
    print("lower_neckband selftest: passed=%d/%d failed=%d" % (len(checks) - len(bad), len(checks), len(bad)))
    return 1 if bad else 0


def main():
    packed_png, out_dir, name = argv[0], argv[1], argv[2]
    src = bpy.data.filepath
    height, above = opt("--height", 0.022), opt("--above", 1.45)
    img = bpy.data.images.load(packed_png)
    W, H = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(H, W, 4)
    ob = [o for o in bpy.data.objects if o.type == "MESH" and o.find_armature() is not None][0]
    me = ob.data
    uv = me.uv_layers.active.data
    rib = set()
    for poly in me.polygons:
        for li in poly.loop_indices:
            u, v = uv[li].uv
            x = min(W - 1, max(0, int(u % 1.0 * W)))
            y = min(H - 1, max(0, int(v % 1.0 * H)))
            if abs(px[y, x, 1] - 0.25) < 0.08:
                rib.add(me.loops[li].vertex_index)
    M = ob.matrix_world
    Mi = M.inverted()
    co = np.array([tuple(M @ v.co) for v in me.vertices])
    band = sorted(i for i in rib if co[i, 2] > above)
    bset = set(band)
    seam_ids = sorted({a for e in me.edges for a, b in (e.vertices, e.vertices[::-1]) if a in bset and b not in rib})
    if len(band) < 20 or len(seam_ids) < 8:
        print("BAND FAIL band=%d seam=%d" % (len(band), len(seam_ids)))
        sys.exit(1)
    P, seam = co[band], co[seam_ids]
    cx, cy = seam[:, 0].mean(), seam[:, 1].mean()
    near0 = scale_columns(P, seam, 1e9)[1]
    before = sectors(P, cx, cy, seam[near0][:, 2])
    Q, near, tall, _ = scale_columns(P, seam, height)
    after = sectors(Q, cx, cy, seam[near][:, 2])
    from mathutils import Vector
    for i, q in zip(band, Q):
        me.vertices[i].co = Mi @ Vector(tuple(q))
    me.update()
    os.makedirs(out_dir, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    ob.select_set(True)
    arm = ob.find_armature()
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.export_scene.fbx(filepath=os.path.join(out_dir, name + "_skinned.fbx"), use_selection=True,
                             object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, mesh_smooth_type="OFF",
                             use_tspace=True, colors_type="LINEAR", bake_anim=False)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out_dir, name + "_skinned.blend"))
    moved = np.linalg.norm(Q - P, axis=1)
    log = {"in": src, "height": height, "band": len(band), "seam": len(seam_ids), "moved": int((moved > 5e-4).sum()),
           "mostMovedMm": round(float(moved.max() * 1000), 1), "columnMm": [round(float(tall.min() * 1000), 1), round(float(tall.max() * 1000), 1)],
           "before": before, "after": after}
    json.dump(log, open(os.path.join(out_dir, "band.json"), "w"), indent=1)
    print("BAND " + json.dumps({k: v for k, v in log.items() if k not in ("before", "after")}))


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in argv else main())
