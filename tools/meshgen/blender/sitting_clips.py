"""Sitting down, sitting and standing up: three Mixamo clips, each made ready for Unreal to retarget.

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
CLIPS = (("Seated Idle_" + X_BOT, "sit_down", X_BOT),       # 1.03 to 0.65 m, 0.28 m back
         ("Sitting Talking_" + Y_BOT, "sit_talk", Y_BOT),   # 0.56 m held 44 s, hands 0.2 to 0.3 m
         ("Sit To Stand_" + X_BOT, "stand_up", X_BOT))      # 0.57 to 1.03 m, 0.47 m forward
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
    for name, take, bot in CLIPS:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        rig = load(clip_file(src_dir, name))
        if rig is None or rig.animation_data is None or rig.animation_data.action is None:
            print("sittingClips=NO-ACTION clip=%s" % name.replace(" ", "~"))
            return 2
        rig.name = "SitRig"
        act = rig.animation_data.action
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
    check("three clips: down, the seated loop, up, in that order", [c[1] for c in CLIPS] == ["sit_down", "sit_talk", "stand_up"])
    check("each clip is its own file", out_file(OUT_DIR, "sit_down").endswith("sit_down.fbx"))
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
