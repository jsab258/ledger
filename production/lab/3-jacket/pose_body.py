"""Ron's body with the arms let down from MetaHuman's A-pose to hang about 12 degrees off vertical,
so the jacket drapes as in a standing photograph. Writes ron_down.npz (LOD0 and LOD1, world metres)."""
import bpy, numpy as np, math, mathutils
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=r"F:/LedgerTools/bodies/MH_RoccoP2/MH_RoccoP2_Body.fbx")
arm = bpy.data.objects["root"]
W = arm.matrix_world
def head(n): return W @ arm.pose.bones[n].head
bpy.context.view_layer.update()
for side, sgn in (("l", 1), ("r", -1)):
    sh, el = head("upperarm_" + side), head("lowerarm_" + side)
    d = el - sh
    ang = math.atan2(abs(d.x), -d.z)            # off vertical, in the x-z plane
    want = math.radians(12)
    rot = sgn * (ang - want)                    # about +y: positive turns +x toward -z ... tested below
    for trial in (rot, -rot):
        pb = arm.pose.bones["upperarm_" + side]
        R = mathutils.Matrix.Translation(sh) @ mathutils.Matrix.Rotation(trial, 4, 'Y') @ mathutils.Matrix.Translation(-sh)
        before = pb.matrix.copy()
        pb.matrix = W.inverted() @ R @ W @ pb.matrix
        bpy.context.view_layer.update()
        e2 = head("lowerarm_" + side)
        if abs(e2.x) < abs(el.x):
            print("ARM", side, "from", round(math.degrees(ang), 1), "deg; elbow now", tuple(round(v, 3) for v in e2))
            break
        pb.matrix = before
        bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
out = {}
for o in bpy.context.scene.objects:
    if o.type != 'MESH' or not any(k in o.name for k in ("LOD0", "LOD1")): continue
    e = o.evaluated_get(dg); m = e.to_mesh(); m.calc_loop_triangles()
    V = np.array([(o.matrix_world @ v.co)[:] for v in m.vertices]); F = np.array([t.vertices[:] for t in m.loop_triangles])
    key = "LOD0" if "LOD0" in o.name else "LOD1"
    out[key + "_V"], out[key + "_F"] = V, F
    print("MESH", key, V.shape, "x", V[:, 0].min().round(3), V[:, 0].max().round(3))
    e.to_mesh_clear()
np.savez_compressed(r"F:/LedgerTools/lab/jacket/ron_down.npz", **out)
bpy.ops.wm.save_as_mainfile(filepath=r"F:/LedgerTools/lab/jacket/ron_down.blend")
