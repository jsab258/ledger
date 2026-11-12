"""Independent leg measures of an animation FBX on the MetaHuman skeleton, in Blender (no window):
    blender -b --factory-startup --python tools/tool-tests/measure_fbx_legs.py -- out.json a.fbx [b.fbx ...]
Per file: frames; knee bend (deg from straight) median and worst, over frames where both feet are planted;
floor (lowest foot/ball point, cm); planted-ball drift (cm): horizontal travel of a ball while it stays
within 2 cm of the floor and moves under 2 cm a frame. Written for the Motionsmith test, 12 Nov 2026."""
import bpy, json, sys, math
from mathutils import Vector
args = sys.argv[sys.argv.index("--") + 1:]
out, files = args[0], args[1:]
res = {}
for f in files:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=f, automatic_bone_orientation=False)
    arm = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
    act = arm.animation_data.action if arm.animation_data else None
    f0, f1 = (int(act.frame_range[0]), int(act.frame_range[1])) if act else (0, 0)
    sc = bpy.context.scene
    unit = 100.0 * arm.matrix_world.to_scale()[0]  # metres in scene -> cm
    P = lambda n: arm.matrix_world @ arm.pose.bones[n].head
    rows = []
    for fr in range(f0, f1 + 1):
        sc.frame_set(fr)
        r = {}
        for s in "lr":
            th, ca, fo, ba = P("thigh_" + s), P("calf_" + s), P("foot_" + s), P("ball_" + s)
            a, b = (ca - th).normalized(), (fo - ca).normalized()
            r["knee_" + s] = math.degrees(a.angle(b))
            r["foot_" + s] = [fo.x * 100, fo.y * 100, fo.z * 100]
            r["ball_" + s] = [ba.x * 100, ba.y * 100, ba.z * 100]
        rows.append(r)
    floor = min(min(r["ball_l"][2], r["ball_r"][2], r["foot_l"][2], r["foot_r"][2]) for r in rows)
    stats = {"frames": len(rows), "floor_cm": round(floor, 2)}
    for s in "lr":
        zs = [r["ball_" + s][2] for r in rows]
        zmin = min(zs)
        drift, start = 0.0, None
        for i, r in enumerate(rows):
            p = Vector(r["ball_" + s][:2])
            planted = r["ball_" + s][2] < zmin + 2.0 and (i == 0 or (p - Vector(rows[i - 1]["ball_" + s][:2])).length < 2.0)
            if planted:
                start = p if start is None else start
                drift = max(drift, (p - start).length)
            else:
                start = None
        stats["ball_drift_" + s] = round(drift, 2)
        stats["ball_height_" + s] = [round(zmin, 2), round(max(zs), 2)]
    both = [r for r in rows if r["ball_l"][2] < floor + 3 and r["ball_r"][2] < floor + 3]
    for s in "lr":
        k = sorted(r["knee_" + s] for r in (both or rows))
        stats["knee_" + s + "_median"] = round(k[len(k) // 2], 1)
        stats["knee_" + s + "_worst"] = round(k[-1], 1)
        stats["knee_" + s + "_least"] = round(k[0], 1)
    stats["both_planted_frames"] = len(both)
    res[f] = stats
json.dump(res, open(out, "w"), indent=1)
