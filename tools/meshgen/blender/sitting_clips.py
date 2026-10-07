"""Sitting down, sitting and standing up: three Mixamo clips, each made ready for Unreal to retarget.

    blender -b --python tools/meshgen/blender/sitting_clips.py -- [SOURCE_DIR] [OUT_DIR]
    python tools/meshgen/blender/sitting_clips.py --selftest      # runs without Blender

WHY, 7 October (phase 1, item 1.2: "one complete Tom and one speaker walking, sitting and
turning"; production/research/sit-and-turn/METHOD-2026-10-06.md, section 1.5: a sit-down clip
with its travel, the seated loop, the stand-up, retargeted offline onto the body). Jafar named the
clips on 7 October; last month's harvest had them under other names (%USERPROFILE%/ledger-mixamo).
Mixamo's downloads without skin carry a skeleton and no mesh, which Unreal will not take as a
skeletal mesh; so each clip gets a small stand-in mesh bound to its hips and leaves as its own FBX,
which Unreal imports as a skeletal mesh and one animation sequence. Their travel stays in the hips
(In Place off); the retargeter makes the root follow it.

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
CLIPS = (("Seated Idle_2dee24f8-3b49-48af-b735-c6377509eaac", "sit_down"),       # 1.03 to 0.65 m, 0.28 m back
         ("Sitting Talking_4f5d21e1-4ccc-41f1-b35b-fb2547bd8493", "sit_talk"),   # 0.56 m held 44 s, hands 0.2 to 0.3 m
         ("Sit To Stand_2dee24f8-3b49-48af-b735-c6377509eaac", "stand_up"))      # 0.57 to 1.03 m, 0.47 m forward
SOURCE_DIR = os.path.join(os.path.expanduser("~"), "ledger-mixamo", "MixamoHarvester", "animations")
OUT_DIR = os.path.join("F:" + os.sep, "LedgerTools", "game-inputs", "production", "assets", "anim", "sit")


def clip_file(src_dir, name):
    return os.path.join(src_dir, "%s.fbx" % name)


def out_file(out_dir, take):
    """One file a clip: the two characters' skeletons differ, so each keeps its own."""
    return os.path.join(out_dir, "%s.fbx" % take)


def main(src_dir, out_dir):
    import bpy
    made = []
    for name, take in CLIPS:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        path = clip_file(src_dir, name)
        if not os.path.isfile(path):
            print("sittingClips=NO-SOURCE missing=%s" % name.replace(" ", "~"))
            return 2
        bpy.ops.import_scene.fbx(filepath=path, automatic_bone_orientation=False)
        arm = next((o for o in bpy.data.objects if o.type == "ARMATURE"), None)
        if arm is None or arm.animation_data is None or arm.animation_data.action is None:
            print("sittingClips=NO-ACTION clip=%s" % name.replace(" ", "~"))
            return 2
        arm.name = "SitRig"
        act = arm.animation_data.action
        act.name = take
        # THE STAND-IN MESH: a small box at the hips, wholly bound to them, so the FBX is a skinned mesh.
        hips = next((b.name for b in arm.data.bones if b.name.lower().endswith("hips")), arm.data.bones[0].name)
        bpy.ops.mesh.primitive_cube_add(size=0.05, location=arm.matrix_world @ arm.data.bones[hips].head_local)
        box = bpy.context.active_object
        box.name = "SitStandIn"
        vg = box.vertex_groups.new(name=hips)
        vg.add(list(range(len(box.data.vertices))), 1.0, "REPLACE")
        box.parent = arm
        mod = box.modifiers.new("Armature", "ARMATURE")
        mod.object = arm
        for o in bpy.data.objects:
            o.select_set(o in (arm, box))
        bpy.context.view_layer.objects.active = arm
        # THE CLIP'S OWN LENGTH: the export bakes the scene's range, by default 250 frames, which made
        # every clip 8.3 s in Unreal (the first run, 7 October, 21:11).
        sc = bpy.context.scene
        sc.frame_start, sc.frame_end = (int(x) for x in act.frame_range)
        out = out_file(out_dir, take)
        os.makedirs(out_dir, exist_ok=True)
        bpy.ops.export_scene.fbx(filepath=out, use_selection=True, object_types={"ARMATURE", "MESH"},
                                 add_leaf_bones=False, bake_anim=True, bake_anim_use_all_actions=False,
                                 bake_anim_use_nla_strips=False, bake_anim_force_startend_keying=True,
                                 apply_unit_scale=True, armature_nodetype="NULL")
        f = tuple(int(x) for x in act.frame_range)
        made.append("%s:%d-%d/%dKB" % (take, f[0], f[1], os.path.getsize(out) // 1024))
    print("sittingClips=MADE dir=%s clips=%s" % (out_dir.replace(" ", "~"), ",".join(made)))
    return 0


def selftest():
    ok = bad = 0

    def check(what, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("sitting_clips selftest FAIL " + what)
    check("three clips: down, the seated loop, up, in that order", [t for _, t in CLIPS] == ["sit_down", "sit_talk", "stand_up"])
    check("each clip is its own file", out_file(OUT_DIR, "sit_down").endswith("sit_down.fbx"))
    check("the output is a game input on F:, never in git",
          OUT_DIR.lower().replace("/", os.sep).startswith(os.path.join("f:" + os.sep, "ledgertools", "game-inputs")))
    print("sitting_clips selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    sys.exit(main(args[0] if len(args) > 0 else SOURCE_DIR, args[1] if len(args) > 1 else OUT_DIR))
