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


def main():
    import unreal
    t0 = time.time()
    lib = unreal.EditorAssetLibrary
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")

    def write(status, made, note):
        line = status_line(status, len(CLIPS), made, time.time() - t0, note)
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        print("make_root_motion_clips: " + line)

    rig = unreal.load_asset(MH_RIG)
    mesh = unreal.load_asset(BODY_MESH)
    clips = [unreal.load_asset(SOURCE_DIR + c + "." + c) for c in CLIPS]
    if rig is None or mesh is None or any(c is None for c in clips):
        write("NO-SOURCE", 0, "rig=%s mesh=%s clips=%d/%d" % (rig is not None, mesh is not None,
                                                              sum(c is not None for c in clips), len(CLIPS)))
        return
    if lib.does_asset_exist(WORK_DIR + "/RTG_MH_RootMotion"):
        lib.delete_asset(WORK_DIR + "/RTG_MH_RootMotion")
    rtg = tools.create_asset("RTG_MH_RootMotion", WORK_DIR, unreal.IKRetargeter, unreal.IKRetargetFactory())
    ctrl = unreal.IKRetargeterController.get_controller(rtg)
    ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, rig)
    ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, rig)
    ctrl.add_default_ops()
    ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.SOURCE, rig)
    ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.TARGET, rig)
    ctrl.auto_map_chains(unreal.AutoMapChainType.EXACT, True)
    # THE ROOT MOTION OP, set to make the root's travel from the target's pelvis.
    found = False
    for i in range(ctrl.get_num_retarget_ops()):
        oc = ctrl.get_op_controller(i)
        if isinstance(oc, unreal.IKRetargetRootMotionController):
            s = oc.get_settings()
            s.set_editor_property("root_motion_source", unreal.RootMotionSource.GENERATE_FROM_TARGET_PELVIS)
            oc.set_settings(s)
            found = True
    if not found:
        write("NO-ROOT-MOTION-OP", 0, "the default op stack has no Root Motion op")
        return
    inputs = unreal.IKRetargetBatchOperationInputs()
    inputs.set_editor_property("assets_to_retarget", [unreal.AssetRegistryHelpers.create_asset_data(c) for c in clips])
    inputs.set_editor_property("source_mesh", mesh)
    inputs.set_editor_property("target_mesh", mesh)
    inputs.set_editor_property("ik_retarget_asset", rtg)
    inputs.set_editor_property("suffix", SUFFIX)
    inputs.set_editor_property("target_path", OUT_DIR)
    inputs.set_editor_property("include_referenced_assets", False)
    inputs.set_editor_property("overwrite_existing_files", True)
    unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
    made, travel = 0, []
    for c in CLIPS:
        a = unreal.load_asset(out_path(c))
        if not isinstance(a, unreal.AnimSequence):
            travel.append("%s=missing" % c[len("AS_MH_Neutral_"):])
            continue
        a.set_editor_property("enable_root_motion", True)
        lib.save_loaded_asset(a, only_if_is_dirty=False)
        made += 1
        try:
            t = unreal.AnimationLibrary.extract_root_motion_from_track_range(a, 0.0, a.get_play_length(), True) \
                if hasattr(unreal.AnimationLibrary, "extract_root_motion_from_track_range") else None
            cm = t.translation.length() if t is not None else -1.0
        except Exception:
            cm = -1.0
        travel.append("%s=%.0fcm" % (c[len("AS_MH_Neutral_"):], cm))
    lib.save_directory(OUT_DIR, only_if_is_dirty=False, recursive=True)
    write("MADE" if made == len(CLIPS) else "PART", made, ",".join(travel))


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
    print("make_root_motion_clips selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
