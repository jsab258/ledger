"""The MetaHuman plugin's own walk clips, given the travel their root bone lacks.

    UnrealEditor-Cmd.exe LedgerProbe.uproject -run=pythonscript -script="tools/ue/make_root_motion_clips.py"
        (or called from tools/ue/make_base_material.py, the build's import step)
    python tools/ue/make_root_motion_clips.py --selftest     # runs without Unreal

WHY, 6 October (phase 1, item 1.2; production/research/sit-and-turn/METHOD-2026-10-06.md, "Step 2,
measured"). The people's move slot played Epic's AS_MH_Neutral_Walk_Start_F_Rfoot whole and found
its root bone travels 0.0 cm: the plugin's locomotion clips are authored in place, the travel in the
pelvis. The professional route, and the method's, is to make root motion at retargeting: Epic's IK
Retargeter, the MetaHuman's own IK rig as both source and target, its Root Motion op set to
"Generate From Target Pelvis", so the root follows the pelvis over the ground and the pelvis is
carried on it. Each clip comes out as <name>_RM in OUT_DIR, its root-motion flag on, a build product
made by this script in the import step (no file over 1 MB may be pushed, and these are made, not
authored).

THAT ROUTE FAILED (Step 3, measured): the clips carry no travel in the pelvis either, so the
retargeter had nothing to copy. main() now bakes it from the planted foot (planted_travel; the
research's route 1, production/research/sit-and-turn/LOCOMOTION-2026-10-06.md). MH_RIG, BODY_MESH
and WORK_DIR are the first route's, kept for its record.

ONE LINE, appended to ue-material.txt: asked, made, and the travel each now carries.
"""
import os
import sys
import time

SOURCE_DIR = "/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/"
CLIPS = ("AS_MH_Neutral_Walk_Start_F_Rfoot", "AS_MH_Neutral_Walk_Loop_F", "AS_MH_Neutral_Walk_Stop_F_Lfoot",
         "AS_MH_Neutral_Walk_Stop_RL_Rfoot", "AS_MH_Neutral_Walk_Start_RL_Rfoot")
MH_RIG = "/MetaHumanCharacter/Animation/Retargeting/IK_MH_IKRig"
# Any built MetaHuman's body on the cast's skeleton serves as both meshes: Sheila's, the speaker's.
BODY_MESH = "/Game/Ledger/MetaHumans/MH_LenaS4/Body/SKM_MH_LenaS4_BodyMesh"
WORK_DIR = "/Game/Retarget/RootMotion"
OUT_DIR = "/Game/Ledger/Anim/RootMotion"
SUFFIX = "_RM"


def out_path(clip):
    return "%s/%s%s" % (OUT_DIR, clip, SUFFIX)


def status_line(status, asked, made, seconds, note):
    return ("rootMotionClips=%s rootMotionAsked=%d rootMotionMade=%d rootMotionSeconds=%.1f rootMotionNote=%s"
            % (status, asked, made, seconds, (note or "none").replace(" ", "~")[:220]))


def planted_travel(left, right, hysteresis=1.0):
    """[(x, y)] of the body's travel per frame from the two balls' component-space positions
    [(x, y, z)], cm: the planted foot is the lower one (within the hysteresis both are down and
    their mean is taken), and the body moves by minus that foot's horizontal step."""
    out = [(0.0, 0.0)]
    for f in range(1, min(len(left), len(right))):
        zl, zr = left[f - 1][2], right[f - 1][2]
        if abs(zl - zr) <= hysteresis:
            feet = (left, right)
        else:
            feet = (left,) if zl < zr else (right,)
        dx = sum(ft[f][0] - ft[f - 1][0] for ft in feet) / len(feet)
        dy = sum(ft[f][1] - ft[f - 1][1] for ft in feet) / len(feet)
        px, py = out[-1]
        out.append((px - dx, py - dy))
    return out


def main():
    """THE FOOT BAKE, 6 October evening (production/research/sit-and-turn/LOCOMOTION-2026-10-06.md,
    route 1, the third try in a new direction): the plugin's clips carry no curves and no travel in
    root or pelvis, so retargeting had nothing to copy. An in-place clip keeps its travel in the
    planted foot, which slides backward at walking speed; that speed, read from the balls in
    component space and integrated, is written into the root bone's keys (the pelvis untouched),
    so each clip carries its walk."""
    import unreal
    t0 = time.time()
    lib = unreal.EditorAssetLibrary
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")

    def write(status, made, note):
        line = status_line(status, len(CLIPS), made, time.time() - t0, note)
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        print("make_root_motion_clips: " + line)

    made, notes = 0, []
    for c in CLIPS:
        short = c[len("AS_MH_Neutral_"):]
        src = SOURCE_DIR + c
        dst = out_path(c)
        # loaded, not looked up: a commandlet's asset registry may not have scanned the plugin yet
        src_obj = unreal.load_asset(src + "." + c)
        if src_obj is None:
            notes.append("%s=no-source" % short)
            continue
        if lib.does_asset_exist(dst):
            lib.delete_asset(dst)
        a = lib.duplicate_loaded_asset(src_obj, dst)
        if not isinstance(a, unreal.AnimSequence):
            notes.append("%s=no-copy" % short)
            continue
        try:
            n = unreal.AnimationLibrary.get_num_frames(a)
            opts = unreal.AnimPoseEvaluationOptions()
            left, right = [], []
            for f in range(n + 1):
                pose = unreal.AnimPoseExtensions.get_anim_pose_at_frame(a, f, opts)
                for bone, into in (("ball_l", left), ("ball_r", right)):
                    t = unreal.AnimPoseExtensions.get_bone_pose(pose, bone, unreal.AnimPoseSpaces.WORLD)
                    v = t.translation
                    into.append((v.x, v.y, v.z))
            travel = planted_travel(left, right)
            ctrl = a.controller
            pos = [unreal.Vector(x, y, 0.0) for (x, y) in travel]
            rot = [unreal.Quat(0.0, 0.0, 0.0, 1.0)] * len(pos)
            scl = [unreal.Vector(1.0, 1.0, 1.0)] * len(pos)
            try:
                ctrl.set_bone_track_keys("root", pos, rot, scl)
            except Exception:
                try:
                    ctrl.add_bone_curve("root")
                except Exception:
                    ctrl.add_bone_track("root")
                ctrl.set_bone_track_keys("root", pos, rot, scl)
            a.set_editor_property("enable_root_motion", True)
            lib.save_loaded_asset(a, only_if_is_dirty=False)
            made += 1
            cm = (travel[-1][0] ** 2 + travel[-1][1] ** 2) ** 0.5
            secs = a.get_play_length()
            notes.append("%s=%.0fcm/%.2fs/%.2fm_s" % (short, cm, secs, (cm / 100.0) / secs if secs > 0 else 0.0))
        except Exception as e:
            notes.append("%s=RAISED:%s" % (short, str(e)[:60]))
    lib.save_directory(OUT_DIR, only_if_is_dirty=False, recursive=True)
    write("MADE" if made == len(CLIPS) else ("PART" if made else "FAILED"), made, ",".join(notes))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("make_root_motion_clips selftest FAIL " + name)
    check("every clip is the plugin's own walk", all(c.startswith("AS_MH_Neutral_Walk_") for c in CLIPS))
    check("the made clips land in the game's own content, with their suffix",
          out_path(CLIPS[0]) == "/Game/Ledger/Anim/RootMotion/AS_MH_Neutral_Walk_Start_F_Rfoot_RM")
    check("the line carries what was asked", "rootMotionAsked=5" in status_line("MADE", 5, 5, 1.0, "x"))
    check("a note keeps no spaces", " " not in status_line("MADE", 1, 1, 1.0, "a b").split("Note=")[1])
    # a foot planted on the left while the right swings: the body goes forward by the foot's slide
    lf = [(0.0, -10.0 * f, 0.0) for f in range(5)]
    rf = [(20.0, 5.0 * f, 8.0) for f in range(5)]
    tr = planted_travel(lf, rf)
    check("the planted foot's backward slide is the body's forward travel", abs(tr[-1][1] - 40.0) < 1e-6 and tr[-1][0] == 0.0)
    both = planted_travel([(0.0, -4.0 * f, 0.0) for f in range(3)], [(0.0, -2.0 * f, 0.5) for f in range(3)])
    check("both feet down: their mean step", abs(both[-1][1] - 6.0) < 1e-6)
    print("make_root_motion_clips selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
