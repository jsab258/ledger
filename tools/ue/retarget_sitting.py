"""Sitting down, the seated loop and standing up, carried onto the cast's MetaHuman skeleton.

    UnrealEditor-Cmd.exe LedgerProbe.uproject -run=pythonscript -script="tools/ue/retarget_sitting.py"
        (or called from tools/ue/make_base_material.py, the build's import step)
    python tools/ue/retarget_sitting.py --selftest     # runs without Unreal

WHY, 7 October (phase 1, item 1.2: Tom and a speaker "walking, sitting and turning";
production/research/sit-and-turn/METHOD-2026-10-06.md, section 1, steps 2 and 5: retarget offline,
once, with Epic's IK Retargeter; sitting is a sit-down clip, a seated loop and a stand-up). The
clips are Mixamo's, chosen by what they do (tools/meshgen/blender/sitting_clips.py made each into
an FBX Unreal can read, on F: as a game input). Each is imported with its own Mixamo skeleton, an
IK rig is made for it by the engine's own auto-generation, a retargeter maps it to the MetaHuman
plugin's IK rig by chain name, and one batch retarget puts it onto the cast's shared body skeleton
as A_<clip>_MH under OUT_DIR, which the build cooks. Root motion is not made: the game places the
body so the clip's last pose lands on the seat (the method's simpler alignment); the seat's own
warp can come later.

ONE LINE, appended to ue-material.txt: asked, made, and each clip's length.
"""
import os
import sys
import time

CLIPS = ("sit_down", "sit_talk", "stand_up")
INPUTS = os.environ.get("LEDGER_GAME_INPUTS", r"F:\LedgerTools\game-inputs")
SOURCE_REL = os.path.join("production", "assets", "anim", "sit")
TARGET_MESH = "/Game/Ledger/MetaHumans/MH_LenaS4/Body/SKM_MH_LenaS4_BodyMesh"   # the cast's shared skeleton
TARGET_RIG = "/MetaHumanCharacter/Animation/Retargeting/IK_MH_IKRig"
WORK_DIR = "/Game/Retarget/Sit"
OUT_DIR = "/Game/Ledger/Anim/Sit"
SUFFIX = "_MH"


def source_fbx(clip, inputs=None):
    return os.path.join(INPUTS if inputs is None else inputs, SOURCE_REL, clip + ".fbx")


def out_path(clip):
    return "%s/A_%s%s" % (OUT_DIR, clip, SUFFIX)


def status_line(status, asked, made, seconds, note):
    return ("sittingClips=%s sittingAsked=%d sittingMade=%d sittingSeconds=%.0f sittingNote=%s"
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
        print("retarget_sitting: " + line)

    target_mesh = unreal.load_asset(TARGET_MESH)
    target_rig = unreal.load_asset(TARGET_RIG)
    if target_mesh is None or target_rig is None:
        write("NO-TARGET", 0, "mesh %s rig %s" % (target_mesh is not None, target_rig is not None))
        return
    missing = [c for c in CLIPS if not os.path.isfile(source_fbx(c))]
    if missing:
        write("NO-SOURCE", 0, "missing " + ",".join(missing))
        return
    if lib.does_directory_exist(WORK_DIR):
        lib.delete_directory(WORK_DIR)
    made, notes = 0, []
    for clip in CLIPS:
        dest = "%s/%s" % (WORK_DIR, clip)
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_as_skeletal", True)
        ui.set_editor_property("import_animations", True)
        ui.set_editor_property("import_materials", False)
        ui.set_editor_property("import_textures", False)
        ui.set_editor_property("create_physics_asset", False)
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", source_fbx(clip))
        task.set_editor_property("destination_path", dest)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        task.set_editor_property("options", ui)
        tools.import_asset_tasks([task])
        src_mesh = anim = None
        for p in lib.list_assets(dest, recursive=True, include_folder=False):
            a = lib.load_asset(p)
            if isinstance(a, unreal.SkeletalMesh) and src_mesh is None:
                src_mesh = a
            elif isinstance(a, unreal.AnimSequence):
                if anim is None or a.get_play_length() > anim.get_play_length():
                    anim = a
        if src_mesh is None or anim is None:
            notes.append("%s:no-mesh-or-anim" % clip)
            continue
        src_rig = tools.create_asset("IK_" + clip, dest, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
        rc = unreal.IKRigController.get_controller(src_rig)
        rc.set_skeletal_mesh(src_mesh)
        auto_ok = rc.apply_auto_generated_retarget_definition()
        rtg = tools.create_asset("RTG_" + clip + "_to_MH", dest, unreal.IKRetargeter, unreal.IKRetargetFactory())
        ctrl = unreal.IKRetargeterController.get_controller(rtg)
        ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, src_rig)
        ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_rig)
        try:
            ctrl.add_default_ops()
            ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.SOURCE, src_rig)
            ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.TARGET, target_rig)
        except Exception:
            pass
        ctrl.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)
        inputs = unreal.IKRetargetBatchOperationInputs()
        inputs.set_editor_property("assets_to_retarget", [unreal.AssetRegistryHelpers.create_asset_data(anim)])
        inputs.set_editor_property("source_mesh", src_mesh)
        inputs.set_editor_property("target_mesh", target_mesh)
        inputs.set_editor_property("ik_retarget_asset", rtg)
        inputs.set_editor_property("suffix", SUFFIX)
        inputs.set_editor_property("target_path", OUT_DIR)
        inputs.set_editor_property("include_referenced_assets", False)
        inputs.set_editor_property("overwrite_existing_files", True)
        result = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
        names = [str(a.package_name) for a in result] if result else []
        anims = [n for n in names if n.startswith(OUT_DIR)]
        # A FIXED NAME FOR THE GAME, whatever the batch called it.
        if anims and anims[0] != out_path(clip):
            if lib.does_asset_exist(out_path(clip)):
                lib.delete_asset(out_path(clip))
            lib.rename_asset(anims[0], out_path(clip))
        if lib.does_asset_exist(out_path(clip)):
            made += 1
            seq = unreal.load_asset(out_path(clip))
            notes.append("%s:%.1fs/auto-rig-%s" % (clip, seq.get_play_length() if seq else -1.0, "yes" if auto_ok else "NO"))
        else:
            notes.append("%s:not-made" % clip)
    lib.save_directory(WORK_DIR, only_if_is_dirty=False, recursive=True)
    if lib.does_directory_exist(OUT_DIR):
        lib.save_directory(OUT_DIR, only_if_is_dirty=False, recursive=True)
    write("MADE" if made == len(CLIPS) else ("PARTIAL" if made else "NOT-MADE"), made, ",".join(notes))


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("retarget_sitting selftest FAIL " + name)
    check("the clips the Blender step makes", CLIPS == ("sit_down", "sit_talk", "stand_up"))
    check("a fixed name the game loads", out_path("sit_down") == "/Game/Ledger/Anim/Sit/A_sit_down_MH")
    check("it lands where the build cooks", out_path("stand_up").startswith("/Game/Ledger/"))
    check("the work stays out of the cook", not WORK_DIR.startswith("/Game/Ledger/"))
    check("the source is a game input on F:", source_fbx("sit_down", r"F:\X").endswith(os.path.join("anim", "sit", "sit_down.fbx")))
    check("the line names its status", "sittingClips=MADE" in status_line("MADE", 3, 3, 1.0, "x"))
    print("retarget_sitting selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
