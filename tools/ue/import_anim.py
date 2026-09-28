"""An animation made in Blender, imported onto the MetaHuman body skeleton.

    set LEDGER_MH_SCRIPT=import_anim
    set LEDGER_ANIM_FBX=F:/LedgerTools/tmp/drape/ron_sit.fbx
    set LEDGER_ANIM_DEST=/Game/Ledger/Cloth/anims
    set LEDGER_ANIM_NAME=AS_Ledger_Sit
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 28 September (Jafar's list, item 5: the jacket tested sitting). The sit
is made by tools/meshgen/blender/sit_anim.py on Ron's own exported skeleton;
this brings it in on the skeleton Epic's MetaHuman walk plays on, which is the
cast's body skeleton, and writes what it made to import-anim.txt beside the project.

The root and the pelvis at the start are written out too: the first sit came
in with the root at a scale of 100, the body a hundred times too big and out of
every frame (sit_anim.py had dropped the skeleton's parent, which scales it to
metres; 28 September). The root's scale should read 1 and the pelvis about a
metre up.
"""
import os
import time

WALK = "/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/AS_MH_Neutral_Walk_Loop_F.AS_MH_Neutral_Walk_Loop_F"


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "import-anim.txt")

    def run():
        lines = []
        skel = unreal.load_asset(WALK).get_editor_property("skeleton")
        lines.append("skeleton %s" % skel.get_path_name())
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", os.environ.get("LEDGER_ANIM_FBX"))
        task.set_editor_property("destination_path", os.environ.get("LEDGER_ANIM_DEST", "/Game/Ledger/Cloth/anims"))
        task.set_editor_property("destination_name", os.environ.get("LEDGER_ANIM_NAME", "AS_Ledger_Sit"))
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", False)
        ui.set_editor_property("import_animations", True)
        ui.set_editor_property("import_as_skeletal", True)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
        ui.set_editor_property("skeleton", skel)
        ui.anim_sequence_import_data.set_editor_property("convert_scene", True)
        ui.anim_sequence_import_data.set_editor_property("import_bone_tracks", True)
        task.set_editor_property("options", ui)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        paths = list(task.get_editor_property("imported_object_paths") or [])
        lines.append("imported %s" % paths)
        for p in paths:
            a = unreal.load_asset(p)
            if isinstance(a, unreal.AnimSequence):
                lines.append("%s: %.2f s" % (p, a.get_play_length()))
                for bone in ("root", "pelvis"):
                    t = unreal.AnimationLibrary.get_bone_pose_for_time(a, bone, 0.0, False)
                    lines.append("%s at 0: at %s, scale %s" % (bone, [round(v, 2) for v in (t.translation.x, t.translation.y, t.translation.z)],
                                                           [round(v, 3) for v in (t.scale3d.x, t.scale3d.y, t.scale3d.z)]))
                unreal.EditorAssetLibrary.save_loaded_asset(a)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(out, "a", encoding="utf-8") as fh:
                fh.write("raised %r\n" % (e,))
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
