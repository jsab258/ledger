"""CMU motion (cgspeed BVH) made ready for Unreal's retargeter: steps 1 to 3 of
production/research/ai-video-motion/CMU-RETARGET-METHOD-2026-11-12.md (review 17 Nov, fixes 1, 2 and 8).

    blender -b --python C:/Users/Jafar/ledger-local/tools/meshgen/blender/cmu_clips.py -- [SRC_DIR] [OUT_DIR]

Per clip: the BVH is imported at SCALE metres a unit (not inches), armature object scale 1; the
frame-0 T-pose (cgspeed's added first frame) becomes the REST pose (pose.armature_apply) and is dropped
from the clip with the first TRIM samples after it (a turn over 90 degrees in one step there); the rest samples are taken every fourth (120 to 30 fps); the motion is re-keyed against
the new rest. Output as sitting_clips.py writes Mixamo clips: one skeleton FBX (T-pose rest with a
stand-in cube bound to the hips) and one motion-only FBX per clip. Then flip checks (any bone turning
over 90 degrees between two 30 fps frames) on the BVH and on each exported FBX re-imported, and the
pelvis heights. The output is a build input on F:, never in git.
"""
import math
import os
import sys

SCALE = 0.0564
STEP = 4   # 120 fps to 30 fps
TRIM = 2   # 30 fps samples dropped after the T-pose: the first step turns the hips and left arm over 90 degrees (17 Nov)
CLIPS = (("143_18", "sit_get_up_143_18"), ("113_15", "sit_get_up_113_15"), ("131_01", "start_walk_stop_131_01"))
SRC_DIR = "F:/LedgerTools/game-inputs/cmu-2026-11-17/src"
OUT_DIR = "F:/LedgerTools/game-inputs/cmu-2026-11-17"
LIMB_END = ("UpLeg", "Leg", "Foot", "ToeBase", "Arm", "ForeArm", "Hand", "Shoulder")


def is_limb(name):
    return name.startswith(("Left", "Right")) and name.endswith(LIMB_END) and "Finger" not in name


def fcurves_of(act):
    """Every F-curve of an action (Blender 5: layered actions, as sitting_clips.py reads them)."""
    if hasattr(act, "layers"):
        return [fc for layer in act.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
    return list(act.fcurves)


def main(src_dir, out_dir):
    import bpy

    log = []

    def say(s):
        print("cmuClips: " + s)
        log.append(s)

    def fresh():
        bpy.ops.wm.read_factory_settings(use_empty=True)

    def hips_z(rig):
        return (rig.matrix_world @ rig.pose.bones["Hips"].head).z

    def flips(rig, frames):
        """Every bone's turn (degrees) between consecutive sampled frames, by its local rotation."""
        found, prev = [], None
        for f in frames:
            bpy.context.scene.frame_set(f)
            bpy.context.view_layer.update()
            cur = {b.name: b.matrix_basis.copy() for b in rig.pose.bones}
            if prev:
                for n, m in cur.items():
                    a = math.degrees((prev[n].inverted() @ m).to_quaternion().angle)
                    if a > 180:
                        a = 360 - a
                    if a > 90:
                        found.append((n, f, round(a, 1), is_limb(n)))
            prev = cur
        return found

    def segs(hs):
        """Sit and rise in 30 fps clip frames (1-based) from the pelvis heights."""
        n = len(hs)
        lo, hi = min(hs), max(hs)
        i_lo = hs.index(lo)
        stand0 = max(hs[:max(1, i_lo)])
        top = 0.97 * stand0
        a = max([i for i in range(i_lo) if hs[i] >= top] or [0])       # last standing frame before the sit
        b = next((i for i in range(i_lo + 1) if hs[i] <= lo + 0.03), i_lo)   # first frame at the bottom
        c = max(i for i in range(n) if hs[i] <= lo + 0.03)              # last frame at the bottom
        stand1 = max(hs[c:])
        d = next((i for i in range(c, n) if hs[i] >= 0.97 * stand1), n - 1)
        return dict(lowest=i_lo + 1, highest=hs.index(max(hs)) + 1, sit=(a + 1, b + 1), seat_hold=(b + 1, c + 1), rise=(c + 1, d + 1))

    results = {}
    for num, take in CLIPS:
        fresh()
        bvh = os.path.join(src_dir, num + ".bvh")
        bpy.ops.import_anim.bvh(filepath=bvh, global_scale=SCALE, rotate_mode="NATIVE", update_scene_fps=False,
                                use_fps_scale=False, frame_start=0)
        rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
        rig.name = "CmuRig"
        sc = bpy.context.scene
        total = int(rig.animation_data.action.frame_range[1]) + 1
        say("%s: BVH imported, %d samples at 120 fps, object scale %s, %d bones" % (num, total, tuple(rig.scale), len(rig.pose.bones)))
        samples = list(range(1 + TRIM * STEP, total, STEP))   # sample 0 is the T-pose, dropped, and the first TRIM steps
        # --- the BVH itself: flips and heights at 30 fps
        sc.frame_set(0)
        bpy.context.view_layer.update()
        rest_hips_import = hips_z(rig)
        bvh_flips = flips(rig, samples)
        # --- stored poses (armature space), old rest
        stored = []
        for f in samples:
            sc.frame_set(f)
            bpy.context.view_layer.update()
            stored.append({b.name: b.matrix.copy() for b in rig.pose.bones})
        # --- the T-pose frame becomes the rest pose
        sc.frame_set(0)
        bpy.context.view_layer.update()
        tpose_hips = hips_z(rig)
        bpy.context.view_layer.objects.active = rig
        for o in bpy.data.objects:
            o.select_set(o == rig)
        bpy.ops.object.mode_set(mode="POSE")
        bpy.ops.pose.select_all(action="SELECT")
        bpy.ops.pose.armature_apply(selected=False)
        bpy.ops.object.mode_set(mode="OBJECT")
        rig.animation_data_clear()
        for b in rig.pose.bones:
            b.location = (0, 0, 0)
            b.rotation_mode = "QUATERNION"
            b.rotation_quaternion = (1, 0, 0, 0)
        bpy.context.view_layer.update()
        rest_hips = hips_z(rig)
        say("%s: rest Hips height after scaling %.3f m (T-pose frame; import rest was %.3f)" % (num, rest_hips, rest_hips_import))
        # stand-in cube bound to the hips, then the skeleton file
        bpy.ops.mesh.primitive_cube_add(size=0.05, location=rig.matrix_world @ rig.pose.bones["Hips"].head)
        box = bpy.context.active_object
        box.name = "CmuStandIn"
        box.vertex_groups.new(name="Hips").add(list(range(len(box.data.vertices))), 1.0, "REPLACE")
        box.parent = rig
        box.modifiers.new("Armature", "ARMATURE").object = rig

        def cm_scale(objs, k):
            """Bones in centimetres, the rig node unscaled (17 Nov: with Blender's default 'All Local' the exporter
            puts the metres-to-cm x100 on the root node only (export_fbx_bin.py 3542-3545, 5.2.2), Unreal keeps it as
            a scaled root bone CmuRig, and its retargeter threw the targets' pelvis about 96 m off). The rest and the
            location keys are scaled by k and applied; the scene's unit scale makes the exporter's factor 1."""
            for o in bpy.data.objects:
                o.select_set(o in objs)
            bpy.context.view_layer.objects.active = rig
            rig.scale = (k, k, k)
            bpy.context.view_layer.update()
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            act = rig.animation_data.action if rig.animation_data else None
            if act:
                for fc in fcurves_of(act):
                    if fc.data_path.endswith(".location"):
                        for kp in fc.keyframe_points:
                            kp.co[1] *= k
                            kp.handle_left[1] *= k
                            kp.handle_right[1] *= k
                        fc.update()
            bpy.context.view_layer.update()

        def export(path, objs, anim):
            sc.unit_settings.scale_length = 0.01
            cm_scale(objs, 100.0)
            for o in bpy.data.objects:
                o.select_set(o in objs)
            bpy.context.view_layer.objects.active = objs[0]
            bpy.ops.export_scene.fbx(filepath=path, use_selection=True,
                                     object_types={"ARMATURE", "MESH"} if len(objs) > 1 else {"ARMATURE"},
                                     add_leaf_bones=False, bake_anim=anim, bake_anim_use_all_actions=False,
                                     bake_anim_use_nla_strips=False, bake_anim_force_startend_keying=True,
                                     apply_unit_scale=True, armature_nodetype="NULL")
            cm_scale(objs, 0.01)
            sc.unit_settings.scale_length = 1.0
        skel = os.path.join(out_dir, "tpose_%s.fbx" % num)
        export(skel, [rig, box], False)
        bpy.data.objects.remove(box)
        # --- re-key the motion against the new rest
        sc.render.fps = 30
        sc.render.fps_base = 1.0
        order = [b.name for b in rig.pose.bones]
        worst = 0.0
        for k, st in enumerate(stored):
            for n in order:
                pb = rig.pose.bones[n]
                pb.matrix = st[n]
                bpy.context.view_layer.update()
            for n in order:
                pb = rig.pose.bones[n]
                if n == "Hips":
                    pb.keyframe_insert("location", frame=k + 1)
                pb.keyframe_insert("rotation_quaternion", frame=k + 1)
        sc.frame_start, sc.frame_end = 1, len(stored)
        hs = []
        for k, st in enumerate(stored):
            sc.frame_set(k + 1)
            bpy.context.view_layer.update()
            for n in order:
                d = (rig.pose.bones[n].matrix.translation - st[n].translation).length
                worst = max(worst, d)
            hs.append(hips_z(rig))
        say("%s: re-keyed %d frames at 30 fps; worst bone head off its stored place %.4f m" % (num, len(stored), worst))
        motion = os.path.join(out_dir, "%s.fbx" % take)
        rig.animation_data.action.name = take
        export(motion, [rig], True)
        results[num] = dict(take=take, frames=len(stored), seconds=len(stored) / 30.0, hs=hs, bvh_flips=bvh_flips,
                            rest=rest_hips, skel=skel, motion=motion, segs=segs(hs), worst=worst, tpose_hips=tpose_hips)

    # --- the exported FBX files, re-imported and checked
    for num, take in CLIPS:
        r = results[num]
        fresh()
        bpy.ops.import_scene.fbx(filepath=r["motion"])
        rig = next(o for o in bpy.data.objects if o.type == "ARMATURE")
        act = rig.animation_data.action
        f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
        r["fbx_frames"] = f1 - f0 + 1
        r["fbx_flips"] = flips(rig, list(range(f0, f1 + 1)))
        hz = []
        for f in range(f0, f1 + 1):
            bpy.context.scene.frame_set(f)
            bpy.context.view_layer.update()
            hz.append((rig.matrix_world @ rig.pose.bones["Hips"].head).z)
        r["fbx_hs"] = hz
        r["fbx_root"] = [o.name for o in bpy.data.objects]
    for num, r in results.items():
        hs, fh = r["hs"], r["fbx_hs"]
        say("RESULT %s %s frames=%d seconds=%.2f restHips=%.3f pelvis=%.3f..%.3f fbxFrames=%d fbxPelvis=%.3f..%.3f" % (
            num, r["take"], r["frames"], r["seconds"], r["rest"], min(hs), max(hs), r["fbx_frames"], min(fh), max(fh)))
        say("RESULT %s segments %s" % (num, r["segs"]))
        say("RESULT %s bvhFlips=%d %s" % (num, len(r["bvh_flips"]), r["bvh_flips"][:20]))
        say("RESULT %s fbxFlips=%d %s (objects %s)" % (num, len(r["fbx_flips"]), r["fbx_flips"][:20], r["fbx_root"]))
    with open(os.path.join(out_dir, "cmu_clips_result.txt"), "w") as fh:
        fh.write("\n".join(log))
    bad = sum(len(r["bvh_flips"]) + len(r["fbx_flips"]) for r in results.values())
    print("cmuClips=MADE flipsFound=%d dir=%s" % (bad, out_dir.replace(" ", "~")))
    return 0


if __name__ == "__main__":
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(args[0] if len(args) > 0 else SRC_DIR, args[1] if len(args) > 1 else OUT_DIR))
