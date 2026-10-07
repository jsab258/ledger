"""Sitting down, sitting, standing up and turning: Mixamo clips, each made ready for Unreal to retarget.

    blender -b --python tools/meshgen/blender/sitting_clips.py -- [SOURCE_DIR] [OUT_DIR]
    python tools/meshgen/blender/sitting_clips.py --selftest      # runs without Blender

WHY, 7 October (phase 1, item 1.2: "one complete Tom and one speaker walking, sitting and
turning"; production/research/sit-and-turn/METHOD-2026-10-06.md, section 1.5: a sit-down clip
with its travel, the seated loop, the stand-up, retargeted offline onto the body). Jafar named the
clips on 7 October; last month's harvest had them under other names (%USERPROFILE%/ledger-mixamo).
Mixamo's downloads without skin carry a skeleton and no mesh, which Unreal will not take as a
skeletal mesh, and no valid bind pose, so Unreal took each clip's FIRST FRAME as its skeleton's
rest (production/research/sit-and-turn/RETARGET-FAULT-2026-10-07.md): the seated clips' rest was
seated, the retargeter copied changes from it, and the MetaHuman came out standing and twisted.
Each file's skeleton at its true rest is Mixamo's T-pose (measured), so each character leaves once as
that T-pose with a small stand-in mesh bound to its hips (a valid bind), and each clip leaves as its
skeleton's motion only, which Unreal imports onto that character's skeleton. Travel stays in the hips.

The output is a build input, not art: F:/LedgerTools/game-inputs/production/assets/anim/sit/
<clip>.fbx (git takes no file over 1 MB). tools/ue/retarget_sitting.py carries them on.
"""
import os
import sys

# CHOSEN BY WHAT THEY DO, NOT BY THEIR NAMES (7 October, evening): the harvest's file names do not
# match their motions (its "Stand To Sit" travels 1.9 m and never sits; its "Sitting Idle" stands;
# a "Stand Up" lies on the floor), so every sitting-named clip was profiled by its hips: a sit-down
# falls from standing (about 1.0 m) to a seat (about 0.6 m) with little travel, a stand-up the
# reverse, a seated loop holds near 0.6 m. X Bot is 2dee24f8, Y Bot 4f5d21e1 (characters_available.txt).
X_BOT, Y_BOT = "2dee24f8-3b49-48af-b735-c6377509eaac", "4f5d21e1-4ccc-41f1-b35b-fb2547bd8493"
MIRROR = "mirror"
REVERSE = "reverse"
# THE SIT-DOWN IS THE STAND-UP PLAYED BACKWARDS (8 October, the sit proof): the only clip that sits
# down from standing ("Seated Idle", 1.03 to 0.65 m) lowers the body bent nearly double, its head at
# 80 cm over hips at 75 (torso 0.05 of its rest length above the hips; F:/LedgerTools/scratch/
# sitprofile2.txt); "Sit To Stand" keeps the head well up (0.48), and backwards it sits down.
CLIPS = (("Sit To Stand_" + X_BOT, "sit_down", X_BOT, "reverse"),   # 1.03 to 0.57 m, 0.47 m back
         ("Sitting Talking_" + Y_BOT, "sit_talk", Y_BOT),   # 0.56 m held 44 s, hands 0.2 to 0.3 m
         ("Sit To Stand_" + X_BOT, "stand_up", X_BOT),      # 0.57 to 1.03 m, 0.47 m forward
         # TURNING TO A SPEAKER (7 October, late): every 90-degree turn profiled by the up-legs' side
         # line, the head's lowest against its rest height, the hands against the hips and the lean
         # (F:/LedgerTools/scratch/turnprofile2.txt). "Standing Turn Right 90" held the right hand at
         # the chest throughout and both "Standing" turns crouched to 0.88 and leant: Sheila hunched
         # in the game. X Bot's "Left Turn 90" is the plainest (head 0.98, hands down, lean 3 cm,
         # travel 2 cm, +90.0 degrees in 29 frames); no right turn came near it, so the right turn
         # is its mirror image (MIRROR, mirrored()).
         ("Left Turn 90_" + X_BOT, "turn_left", X_BOT),
         ("Left Turn 90_" + X_BOT, "turn_right", X_BOT, MIRROR))
SOURCE_DIR = os.path.join(os.path.expanduser("~"), "ledger-mixamo", "MixamoHarvester", "animations")
OUT_DIR = os.path.join("F:" + os.sep, "LedgerTools", "game-inputs", "production", "assets", "anim", "sit")


def clip_file(src_dir, name):
    return os.path.join(src_dir, "%s.fbx" % name)


def tpose_file(src_dir, bot):
    return os.path.join(src_dir, "T-Pose_%s.fbx" % bot)


def tpose_out(out_dir, bot):
    """A character's T-pose skeleton with its stand-in mesh: the skeleton its clips are imported onto."""
    return os.path.join(out_dir, "tpose_%s.fbx" % bot[:8])


def out_file(out_dir, take):
    """One file a clip: the two characters' skeletons differ, so each keeps its own."""
    return os.path.join(out_dir, "%s.fbx" % take)


def flipped_name(name):
    """A bone's other side: Mixamo names its sides Left and Right inside the name."""
    if "Left" in name:
        return name.replace("Left", "Right")
    if "Right" in name:
        return name.replace("Right", "Left")
    return name


def mirrored(path, index):
    """Where a key goes in the mirror image and its sign, as Blender's own flipped paste does across
    the armature's X (Mixamo's rest pose is symmetric across it): the bone to its other side, its
    location's x and its rotation's y and z turned over."""
    head, _, rest = path.partition('pose.bones["')
    bone, _, prop = rest.partition('"]')
    if not rest:
        return path, 1.0
    sign = 1.0
    if prop == ".location" and index == 0:
        sign = -1.0
    elif prop == ".rotation_quaternion" and index in (2, 3):
        sign = -1.0
    elif prop == ".rotation_euler" and index in (1, 2):
        sign = -1.0
    return head + 'pose.bones["' + flipped_name(bone) + '"]' + prop, sign


def is_tpose(hips_z, hand_z, shoulder_z, hand_out, shoulder_out):
    """A T-pose by its own numbers: standing hips, hands level with the shoulders and out past them."""
    return 0.85 <= hips_z <= 1.15 and abs(hand_z - shoulder_z) <= 0.06 and hand_out > shoulder_out + 0.35


def main(src_dir, out_dir):
    import bpy

    def load(path):
        before = set(bpy.data.objects)
        bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=False)
        return next((o for o in bpy.data.objects if o not in before and o.type == "ARMATURE"), None)

    def world(arm, end):
        bpy.context.view_layer.update()
        return arm.matrix_world @ next(b for b in arm.pose.bones if b.name.lower().endswith(end)).head

    def export(out, objs, anim):
        for o in bpy.data.objects:
            o.select_set(o in objs)
        bpy.context.view_layer.objects.active = objs[0]
        os.makedirs(os.path.dirname(out), exist_ok=True)
        bpy.ops.export_scene.fbx(filepath=out, use_selection=True,
                                 object_types={"ARMATURE", "MESH"} if len(objs) > 1 else {"ARMATURE"},
                                 add_leaf_bones=False, bake_anim=anim, bake_anim_use_all_actions=False,
                                 bake_anim_use_nla_strips=False, bake_anim_force_startend_keying=True,
                                 apply_unit_scale=True, armature_nodetype="NULL")

    made = []
    # ONE T-POSE MESH A CHARACTER: the skeleton at its own rest (Mixamo's T-pose, measured: hips about
    # 1.0 m, hands level with the shoulders), exported with the rest as its pose, so its bind is valid.
    for bot in sorted({c[2] for c in CLIPS}):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        rig = load(clip_file(src_dir, next(c[0] for c in CLIPS if c[2] == bot)))
        if rig is None:
            print("sittingClips=NO-RIG bot=%s" % bot)
            return 2
        rig.animation_data_clear()
        rig.data.pose_position = "REST"
        rig.name = "SitRig"
        h, a, sh = world(rig, "hips"), world(rig, "lefthand"), world(rig, "leftarm")
        if not is_tpose(h.z, a.z, sh.z, abs(a.x - h.x), abs(sh.x - h.x)):
            print("sittingClips=NOT-A-TPOSE bot=%s hips=%.2f hand=%.2f shoulder=%.2f" % (bot, h.z, a.z, sh.z))
            return 2
        hips = next(b.name for b in rig.data.bones if b.name.lower().endswith("hips"))
        bpy.ops.mesh.primitive_cube_add(size=0.05, location=rig.matrix_world @ rig.data.bones[hips].head_local)
        box = bpy.context.active_object
        box.name = "SitStandIn"
        box.vertex_groups.new(name=hips).add(list(range(len(box.data.vertices))), 1.0, "REPLACE")
        box.parent = rig
        box.modifiers.new("Armature", "ARMATURE").object = rig
        export(tpose_out(out_dir, bot), [rig, box], False)
        made.append("tpose_%s/hips-%.2f" % (bot[:8], h.z))
    # EACH CLIP AS ITS SKELETON'S MOTION ONLY, imported in Unreal onto its character's T-pose skeleton.
    for clip in CLIPS:
        name, take, bot = clip[:3]
        bpy.ops.wm.read_factory_settings(use_empty=True)
        rig = load(clip_file(src_dir, name))
        if rig is None or rig.animation_data is None or rig.animation_data.action is None:
            print("sittingClips=NO-ACTION clip=%s" % name.replace(" ", "~"))
            return 2
        rig.name = "SitRig"
        act = rig.animation_data.action
        if MIRROR in clip[3:]:
            # THE MIRROR IMAGE: every key copied to its bone's other side, signs turned over; then
            # checked: each hand and foot must land where its other side's was, reflected in x.
            def sample(a):
                rig.animation_data.action = a
                out = []
                for f in range(int(a.frame_range[0]), int(a.frame_range[1]) + 1, 3):
                    bpy.context.scene.frame_set(f)
                    bpy.context.view_layer.update()
                    out.append({b.name: b.head.copy() for b in rig.pose.bones})   # in the armature's own space
                return out
            was = sample(act)
            new = bpy.data.actions.new(take)
            rig.animation_data.action = new
            # Blender 5 keeps an action's curves in its layers' strips, one channel bag a slot.
            curves = [fc for layer in act.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
            copied = 0
            for fc in curves:
                path, sign = mirrored(fc.data_path, fc.array_index)
                nc = new.fcurve_ensure_for_datablock(rig, path, index=fc.array_index,
                                                     group_name=flipped_name(fc.group.name) if fc.group else "")
                nc.keyframe_points.add(len(fc.keyframe_points))
                for k, nk in zip(fc.keyframe_points, nc.keyframe_points):
                    nk.co = (k.co[0], k.co[1] * sign)
                    nk.interpolation = k.interpolation
                nc.update()
                copied += 1
            if copied == 0:
                print("sittingClips=NO-MIRROR clip=%s fcurves-unreadable" % take)
                return 2
            got = sample(new)
            worst = 0.0
            for a, b in zip(was, got):
                for bone in a:
                    if not any(k in bone for k in ("Hand", "Foot", "Head")):
                        continue
                    o, m = a[flipped_name(bone)], b[bone]
                    worst = max(worst, ((o.x + m.x) ** 2 + (o.y - m.y) ** 2 + (o.z - m.z) ** 2) ** 0.5)
            print("sittingClips: %s mirrored from %s, worst hand/foot/head off its reflection %.4f (armature units)" % (take, name, worst))
            if worst > 0.02 * max(1.0, max(v.length for v in was[0].values())):
                print("sittingClips=MIRROR-OFF clip=%s worst=%.4f" % (take, worst))
                return 2
            act = new
        if REVERSE in clip[3:]:
            # BACKWARDS: every key at the clip's other end; checked by its first and last poses swapping.
            f0, f1 = (int(x) for x in act.frame_range)
            new = bpy.data.actions.new(take)
            rig.animation_data.action = new
            curves = [fc for layer in act.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
            for fc in curves:
                nc = new.fcurve_ensure_for_datablock(rig, fc.data_path, index=fc.array_index,
                                                     group_name=fc.group.name if fc.group else "")
                keys = sorted(((f0 + f1 - k.co[0], k.co[1]) for k in fc.keyframe_points))
                nc.keyframe_points.add(len(keys))
                for (t, v), nk in zip(keys, nc.keyframe_points):
                    nk.co = (t, v)
                    nk.interpolation = "LINEAR"
                nc.update()
            hips = next(b for b in rig.pose.bones if b.name.lower().endswith("hips"))
            def hz(a, f):
                rig.animation_data.action = a
                bpy.context.scene.frame_set(f)
                bpy.context.view_layer.update()
                return hips.head.copy()
            off = max((hz(act, f0) - hz(new, f1)).length, (hz(act, f1) - hz(new, f0)).length)
            print("sittingClips: %s reversed from %s, ends swapped within %.3f (armature units)" % (take, name, off))
            if off > 1.0:
                print("sittingClips=REVERSE-OFF clip=%s off=%.3f" % (take, off))
                return 2
            rig.animation_data.action = new
            act = new
        act.name = take
        sc = bpy.context.scene
        sc.frame_start, sc.frame_end = (int(x) for x in act.frame_range)   # the clip's own length
        export(out_file(out_dir, take), [rig], True)
        made.append("%s:%d-%d" % (take, sc.frame_start, sc.frame_end))
    print("sittingClips=MADE dir=%s made=%s" % (out_dir.replace(" ", "~"), ",".join(made)))
    return 0


def selftest():
    ok = bad = 0

    def check(what, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("sitting_clips selftest FAIL " + what)
    check("down, the seated loop, up, then the two turns", [c[1] for c in CLIPS] == ["sit_down", "sit_talk", "stand_up", "turn_left", "turn_right"])
    check("the right turn is the left one's mirror", CLIPS[4][0] == CLIPS[3][0] and MIRROR in CLIPS[4][3:])
    check("a mirrored key goes to the other side, turned over",
          mirrored('pose.bones["mixamorig:LeftHand"].rotation_quaternion', 2) == ('pose.bones["mixamorig:RightHand"].rotation_quaternion', -1.0)
          and mirrored('pose.bones["mixamorig:Hips"].location', 0) == ('pose.bones["mixamorig:Hips"].location', -1.0)
          and mirrored('pose.bones["mixamorig:Hips"].location', 1)[1] == 1.0
          and mirrored('pose.bones["mixamorig:Spine"].rotation_quaternion', 0)[1] == 1.0)
    check("each clip is its own file", out_file(OUT_DIR, "sit_down").endswith("sit_down.fbx"))
    check("the sit-down is the stand-up backwards", CLIPS[0][0] == CLIPS[2][0] and REVERSE in CLIPS[0][3:])
    check("each clip goes onto its own character's T-pose skeleton", all(c[0].endswith(c[2]) for c in CLIPS)
          and tpose_out("O", X_BOT).endswith("tpose_2dee24f8.fbx"))
    check("a T-pose is told by its numbers", is_tpose(1.0, 1.42, 1.43, 0.75, 0.2) and not is_tpose(0.56, 0.9, 1.1, 0.3, 0.2))
    check("the output is a game input on F:, never in git",
          OUT_DIR.lower().replace("/", os.sep).startswith(os.path.join("f:" + os.sep, "ledgertools", "game-inputs")))
    print("sitting_clips selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(args[0] if len(args) > 0 else SOURCE_DIR, args[1] if len(args) > 1 else OUT_DIR))
