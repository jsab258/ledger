"""A built MetaHuman exported whole for Blender: Epic's export for other programs.

    set LEDGER_MH_SCRIPT=export_dcc
    set LEDGER_DCC=/Game/Ledger/MetaHumans/MH_RoccoP2/MH_RoccoP2   (the character asset; comma-separated for more)
    set LEDGER_DCC_OUT=F:/LedgerTools/tmp/dcc
    set LEDGER_DCC_MODE=geometry       (the body as FBX meshes instead of the rig format)
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 28 September (Jafar's list, item 5: "sew the garment around the actual
MetaHuman body in Blender, with a separate simulation mesh"). The body the
game's build makes has no torso: 0 vertices within 15 cm of the middle from
the waist up (F:/LedgerTools/tmp/bodies/SKM_MH_RoccoBare_BodyMesh.fbx, read
in Blender, 28 September), because a build drops the skin under the preset's
clothes. MetaHumanCharacterExportBlueprintLibrary.export_dcc (Epic's
example_export_tools.py) exports a character for other programs; this writes
it unzipped to LEDGER_DCC_OUT/<name>/ and what it made to export-dcc.txt there.
Reads the character only; saves nothing in the project.
"""
import os
import time


def geometry(unreal, ch, name, out_dir):
    """LEDGER_DCC_MODE=geometry (28 September; production/research/character-pipeline/
    metahuman-body-to-blender-2026-09-28.md): export_dcc writes only the rig format (.dna)
    and textures, which Blender cannot open. export_geometry copies the editor's own
    preview body, which keeps the skin a build cuts from under clothes, into the
    project as skeletal meshes (the full body with its measurements too); each is
    then written to FBX in out_dir, as tools/ue/export_body_fbx.py does."""
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    opened = not sub.is_object_added_for_editing(ch) and sub.try_add_object_to_edit(ch)
    dest = "/Game/Ledger/Export/" + name
    try:
        gp = unreal.MetaHumanGeometryExportParams()
        gp.project_path = dest
        gp.head_skeletal_mesh = False
        gp.body_skeletal_mesh = True
        gp.full_body_skeletal_mesh = True
        gp.overwrite_existing_assets = True
        unreal.MetaHumanCharacterExportBlueprintLibrary.export_geometry(ch, gp)
    finally:
        if opened:
            sub.remove_object_to_edit(ch)
    # KEPT IN THE PROJECT too (28 September): the cloth template copies skin
    # weights from this body (tools/ue/make_cloth_jacket.py), and unsaved the
    # assets were gone when the editor closed.
    unreal.EditorAssetLibrary.save_directory(dest, only_if_is_dirty=False, recursive=True)
    os.makedirs(out_dir, exist_ok=True)
    made = []
    for path in unreal.EditorAssetLibrary.list_assets(dest, recursive=True):
        a = unreal.load_asset(path)
        if not isinstance(a, unreal.SkeletalMesh):
            continue
        dst = os.path.join(out_dir, path.split("/")[-1].split(".")[0] + ".fbx")
        task = unreal.AssetExportTask()
        task.set_editor_property("object", a)
        task.set_editor_property("filename", dst)
        task.set_editor_property("exporter", unreal.SkeletalMeshExporterFBX())
        task.set_editor_property("automated", True)
        task.set_editor_property("prompt", False)
        task.set_editor_property("replace_identical", True)
        task.set_editor_property("options", unreal.FbxExportOption())
        ok = unreal.Exporter.run_asset_export_task(task)
        made.append("%s ok=%s %d bytes (asset %s)" % (dst, ok, os.path.getsize(dst) if os.path.exists(dst) else 0, path))
    return "%s geometry: %s" % (name, "; ".join(made) or "no skeletal meshes made under " + dest)


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    root = os.environ.get("LEDGER_DCC_OUT", "F:/LedgerTools/tmp/dcc")
    os.makedirs(root, exist_ok=True)
    report = os.path.join(root, "export-dcc.txt")

    def run():
        lines = []
        for path in [p for p in os.environ.get("LEDGER_DCC", "").split(",") if p]:
            name = path.split("/")[-1].split(".")[0]
            ch = unreal.load_asset(path)
            if ch is None:
                lines.append("%s NOT FOUND" % path)
                continue
            if os.environ.get("LEDGER_DCC_MODE") == "geometry":
                lines.append(geometry(unreal, ch, name, os.path.join(root, name)))
                with open(report, "w", encoding="utf-8") as fh:
                    fh.write("\n".join(lines) + "\n")
                continue
            p = unreal.MetaHumanDCCExportParams()
            p.external_path = os.path.join(root, name).replace("\\", "/")
            p.bake_make_up = True
            p.compress_in_zip_file = False
            p.archive_name = name
            t0 = time.time()
            # OPEN FOR EDITING FIRST: without it the export dies inside the
            # MetaHuman editor on a map lookup (Assertion failed: Pair !=
            # nullptr, 28 September), as other calls on a character need it.
            sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
            opened = not sub.is_object_added_for_editing(ch) and sub.try_add_object_to_edit(ch)
            try:
                unreal.MetaHumanCharacterExportBlueprintLibrary.export_dcc(ch, p)
                made = []
                for dp, _d, fs in os.walk(p.external_path):
                    made += [os.path.relpath(os.path.join(dp, f), p.external_path) for f in fs]
                lines.append("%s exported in %.0f s: %d files: %s" % (name, time.time() - t0, len(made), ", ".join(sorted(made)[:40])))
            except Exception as e:
                lines.append("%s REFUSED %r" % (name, e))
            finally:
                if opened:
                    sub.remove_object_to_edit(ch)
            with open(report, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines) + "\n")

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            with open(report, "a", encoding="utf-8") as fh:
                fh.write("raised %r\n" % (e,))
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
