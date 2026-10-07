"""Sitting down, the seated loop and standing up, carried onto the cast's MetaHuman skeleton.

    UnrealEditor-Cmd.exe LedgerProbe.uproject -run=pythonscript -script="tools/ue/retarget_sitting.py"
        (or called from tools/ue/make_base_material.py, the build's import step)
    python tools/ue/retarget_sitting.py --selftest     # runs without Unreal

WHY, 7 October (phase 1, item 1.2: Tom and a speaker "walking, sitting and turning";
production/research/sit-and-turn/METHOD-2026-10-06.md, section 1, steps 2 and 5: retarget offline,
once, with Epic's IK Retargeter; sitting is a sit-down clip, a seated loop and a stand-up). The
clips are Mixamo's, chosen by what they do (tools/meshgen/blender/sitting_clips.py: each character's
T-pose skeleton with a stand-in mesh, and each clip as its skeleton's motion only, on F: as game
inputs). Each character's T-pose is imported as a skeletal mesh and its clips onto its skeleton; an
IK rig is made for it by the engine's own auto-generation, a retargeter maps it to the MetaHuman
plugin's IK rig by chain name and lines the T-pose up with the MetaHuman's A-pose, and one batch
retarget puts the clips onto the cast's shared body skeleton as A_<clip>_MH under OUT_DIR, which the
build cooks. Root motion is not made: the game places the body on its seat. (7 October: the first
way, each clip imported with its own skeleton, took the clip's first frame as that skeleton's rest,
and the seated clips came out standing and twisted: production/research/sit-and-turn/
RETARGET-FAULT-2026-10-07.md.)

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


# Which Mixamo character's skeleton each clip moves (tools/meshgen/blender/sitting_clips.py CLIPS).
CLIP_BOT = {"sit_down": "2dee24f8", "sit_talk": "4f5d21e1", "stand_up": "2dee24f8"}
BOTS = ("2dee24f8", "4f5d21e1")


def tpose_fbx(bot, inputs=None):
    return os.path.join(INPUTS if inputs is None else inputs, SOURCE_REL, "tpose_%s.fbx" % bot)


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

    def fbx(path, dest, name, skeleton):
        """The FBX as a skeletal mesh (skeleton None) or as an animation on skeleton (as
        tools/ue/import_figure.py does); every asset now under dest."""
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", skeleton is None)
        ui.set_editor_property("import_as_skeletal", True)
        ui.set_editor_property("import_animations", skeleton is not None)
        ui.set_editor_property("import_materials", False)
        ui.set_editor_property("import_textures", False)
        ui.set_editor_property("create_physics_asset", False)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH
                               if skeleton is None else unreal.FBXImportType.FBXIT_ANIMATION)
        if skeleton is not None:
            ui.set_editor_property("skeleton", skeleton)
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", path)
        task.set_editor_property("destination_path", dest)
        task.set_editor_property("destination_name", name)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        task.set_editor_property("options", ui)
        tools.import_asset_tasks([task])
        return [lib.load_asset(q) for q in lib.list_assets(dest, recursive=True, include_folder=False)]

    target_mesh = unreal.load_asset(TARGET_MESH)
    target_rig = unreal.load_asset(TARGET_RIG)
    if target_mesh is None or target_rig is None:
        write("NO-TARGET", 0, "mesh %s rig %s" % (target_mesh is not None, target_rig is not None))
        return
    missing = [c for c in CLIPS if not os.path.isfile(source_fbx(c))] + \
              [b for b in BOTS if not os.path.isfile(tpose_fbx(b))]
    if missing:
        write("NO-SOURCE", 0, "missing " + ",".join(missing))
        return
    if lib.does_directory_exist(WORK_DIR):
        lib.delete_directory(WORK_DIR)
    made, notes = 0, []
    for bot in BOTS:
        # THE CHARACTER'S T-POSE SKELETON, a valid bind (tools/meshgen/blender/sitting_clips.py).
        dest = "%s/%s" % (WORK_DIR, bot)
        got = fbx(tpose_fbx(bot), dest, "tpose", None)
        src_mesh = next((a for a in got if isinstance(a, unreal.SkeletalMesh)), None)
        if src_mesh is None:
            notes.append("%s:no-tpose-mesh" % bot)
            continue
        skel = src_mesh.get_editor_property("skeleton")
        anims = []
        for clip in [c for c in CLIPS if CLIP_BOT[c] == bot]:
            before = set(str(a.get_path_name()) for a in got if a is not None)
            got = fbx(source_fbx(clip), dest, clip, skel)
            seqs = [a for a in got if isinstance(a, unreal.AnimSequence) and str(a.get_path_name()) not in before]
            if not seqs:
                notes.append("%s:no-anim" % clip)
                continue
            anims.append((clip, max(seqs, key=lambda a: a.get_play_length())))
        if not anims:
            continue
        src_rig = tools.create_asset("IK_" + bot, dest, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
        rc = unreal.IKRigController.get_controller(src_rig)
        rc.set_skeletal_mesh(src_mesh)
        auto_ok = rc.apply_auto_generated_retarget_definition()
        rtg = tools.create_asset("RTG_" + bot + "_to_MH", dest, unreal.IKRetargeter, unreal.IKRetargetFactory())
        ctrl = unreal.IKRetargeterController.get_controller(rtg)
        ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, src_rig)
        ctrl.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, target_rig)
        for side, mesh in ((unreal.RetargetSourceOrTarget.SOURCE, src_mesh), (unreal.RetargetSourceOrTarget.TARGET, target_mesh)):
            try:
                ctrl.set_preview_mesh(side, mesh)
            except Exception:
                notes.append("%s:preview-mesh-refused" % bot)
        try:
            ctrl.add_default_ops()
            ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.SOURCE, src_rig)
            ctrl.assign_ik_rig_to_all_ops(unreal.RetargetSourceOrTarget.TARGET, target_rig)
        except Exception:
            notes.append("%s:ops-refused" % bot)
        ctrl.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)
        # THE T-POSE LINED UP WITH THE METAHUMAN'S A-POSE (RETARGET-FAULT-2026-10-07.md, step 4).
        try:
            ctrl.auto_align_all_bones(unreal.RetargetSourceOrTarget.SOURCE)
        except Exception as e:
            notes.append("%s:auto-align-refused-%s" % (bot, str(e)[:40].replace(" ", "~")))
        inputs = unreal.IKRetargetBatchOperationInputs()
        inputs.set_editor_property("assets_to_retarget", [unreal.AssetRegistryHelpers.create_asset_data(a) for _, a in anims])
        inputs.set_editor_property("source_mesh", src_mesh)
        inputs.set_editor_property("target_mesh", target_mesh)
        inputs.set_editor_property("ik_retarget_asset", rtg)
        inputs.set_editor_property("suffix", SUFFIX)
        inputs.set_editor_property("target_path", OUT_DIR)
        inputs.set_editor_property("include_referenced_assets", False)
        inputs.set_editor_property("overwrite_existing_files", True)
        result = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
        names = [str(a.package_name) for a in result] if result else []
        for clip, seq in anims:
            want = out_path(clip)
            # A FIXED NAME FOR THE GAME, whatever the batch called it.
            hit = next((n for n in names if n.startswith(OUT_DIR) and n.split("/")[-1].startswith(str(seq.get_name()))), None)
            if hit and hit != want:
                if lib.does_asset_exist(want):
                    lib.delete_asset(want)
                lib.rename_asset(hit, want)
            if lib.does_asset_exist(want):
                made += 1
                done = unreal.load_asset(want)
                notes.append("%s:%.1fs/auto-rig-%s" % (clip, done.get_play_length() if done else -1.0, "yes" if auto_ok else "NO"))
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
    check("each clip goes onto its own character's T-pose skeleton", set(CLIP_BOT) == set(CLIPS)
          and set(CLIP_BOT.values()) == set(BOTS) and tpose_fbx("2dee24f8", "X").endswith("tpose_2dee24f8.fbx"))
    print("retarget_sitting selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
