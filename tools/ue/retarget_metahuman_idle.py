"""Give the corner's MetaHuman a standing idle: a street person's own idle, retargeted to its body.

    UnrealEditor.exe <scratch project>   with Content/Python/init_unreal.py calling main_after_idle()
    python tools/ue/retarget_metahuman_idle.py --selftest     # runs without Unreal

WHY, 24 September. MH_Test stood in Mickey's corner with its arms out in the
default pose, because an assembled MetaHuman carries no animation. The street's
people each loop an idle on their own skeletons (tools/ue/import_people.py);
Unreal's IK retargeter carries a clip from one skeleton to another. So: one
person's GLB imported beside the MetaHuman, an IK rig made for its skeleton
by the engine's own auto-generation, the MetaHuman plugin's IK rig for the
other side, a retargeter mapping the two by chain name, and one batch
retarget of the idle onto MH_Test's body into /Game/Ledger/MetaHumans, so the
build copies it with the rest.

IN THE FULL EDITOR, like the assembly, and for the same reason: the retarget
runs on the editor's loop. Everything else it makes goes under /Game/Retarget,
which the build does not copy. One line to ue-material.txt either way.
"""
import os
import sys
import time

SOURCE_STEM = "elizabeth-idle"
SOURCE_DIR = "/Game/Retarget/Source"
WORK_DIR = "/Game/Retarget"
TARGET_MESH = "/Game/Ledger/MetaHumans/MH_Test/Body/SKM_MH_Test_BodyMesh"
TARGET_RIG = "/MetaHumanCharacter/Animation/Retargeting/IK_MH_IKRig"
OUT_DIR = "/Game/Ledger/MetaHumans/MH_Test/Anim"
SUFFIX = "_MH"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def out_anim_path():
    return "%s/A_%s%s" % (OUT_DIR, SOURCE_STEM, SUFFIX)


def status_line(status, made, seconds, note):
    return ("metahumanIdle=%s metahumanIdleMade=%s metahumanIdleFrom=%s metahumanIdleSeconds=%.0f metahumanIdleNote=%s"
            % (status, made, SOURCE_STEM, seconds, (note or "none").replace(" ", "~")[:200]))


def main():
    import unreal
    t0 = time.time()
    lib = unreal.EditorAssetLibrary
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")

    def write(status, made, note):
        l = status_line(status, made, time.time() - t0, note)
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(l + "\n")
        print("retarget_metahuman_idle: " + l)

    target_mesh = unreal.load_asset(TARGET_MESH)
    target_rig = unreal.load_asset(TARGET_RIG)
    if target_mesh is None or target_rig is None:
        write("NO-TARGET", "no", "mesh %s rig %s" % (target_mesh is not None, target_rig is not None))
        return
    dest = "%s/%s" % (SOURCE_DIR, SOURCE_STEM)
    if lib.does_directory_exist(WORK_DIR):
        lib.delete_directory(WORK_DIR)
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", os.path.join(repo_root(), "production", "assets", "people", SOURCE_STEM + ".glb"))
    task.set_editor_property("destination_path", dest)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", True)
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
        write("NO-SOURCE", "no", "the person's GLB gave mesh %s anim %s" % (src_mesh is not None, anim is not None))
        return
    src_rig = tools.create_asset("IK_" + SOURCE_STEM.replace("-", "_"), WORK_DIR, unreal.IKRigDefinition,
                                 unreal.IKRigDefinitionFactory())
    rc = unreal.IKRigController.get_controller(src_rig)
    rc.set_skeletal_mesh(src_mesh)
    auto_ok = rc.apply_auto_generated_retarget_definition()
    rtg = tools.create_asset("RTG_" + SOURCE_STEM.replace("-", "_") + "_to_MH", WORK_DIR, unreal.IKRetargeter,
                             unreal.IKRetargetFactory())
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
    made = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
    lib.save_directory(WORK_DIR, only_if_is_dirty=False, recursive=True)
    lib.save_directory(OUT_DIR, only_if_is_dirty=False, recursive=True)
    names = [str(a.package_name) for a in made] if made else []
    anims = [n for n in names if n.startswith(OUT_DIR)]
    # THE ONE THE CORNER LOADS HAS A FIXED NAME, whatever the batch called it.
    if anims and anims[0] != out_anim_path() and not lib.does_asset_exist(out_anim_path()):
        lib.rename_asset(anims[0], out_anim_path())
    ok = lib.does_asset_exist(out_anim_path())
    write("MADE" if ok else "NOT-MADE", "%d-assets" % len(names),
          "auto-rig-%s/%s" % ("yes" if auto_ok else "NO", ",".join(n.split("/")[-1] for n in names)[:120]))


def main_after_idle(seconds=20.0):
    """Waits for the editor to settle, runs once from a tick, closes the editor."""
    import unreal
    state = {"t0": time.time(), "h": None}

    def tick(delta):
        if time.time() - state["t0"] < seconds:
            return
        unreal.unregister_slate_post_tick_callback(state["h"])
        try:
            main()
        except Exception as e:
            with open(os.path.join(unreal.Paths.project_dir(), "ue-material.txt"), "a", encoding="utf-8") as fh:
                fh.write(status_line("RAISED", "no", 0.0, repr(e)) + "\n")
        finally:
            unreal.SystemLibrary.quit_editor()

    state["h"] = unreal.register_slate_post_tick_callback(tick)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("retarget_metahuman_idle selftest FAIL " + name)
    check("the corner loads a fixed name", out_anim_path() == "/Game/Ledger/MetaHumans/MH_Test/Anim/A_elizabeth-idle_MH")
    check("it lands where the build copies from", out_anim_path().startswith("/Game/Ledger/MetaHumans/"))
    check("the work stays out of the copy", not WORK_DIR.startswith("/Game/Ledger/"))
    check("the line names its status", "metahumanIdle=MADE" in status_line("MADE", "3-assets", 1.0, "x"))
    print("retarget_metahuman_idle selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
