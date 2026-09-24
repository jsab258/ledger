"""Import the donkey jacket, in its sizes, into the MetaHuman scratch project.

    set LEDGER_MH_SCRIPT=import_jacket
    set LEDGER_JACKET_FBX=F:/LedgerTools/tmp/jacket/donkey_jacket.fbx,F:/LedgerTools/tmp/jacket/donkey_jacket_l.fbx
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended

WHY, 25 September. The jacket made by tools/meshgen/blender/donkey_jacket.py
is cut from MetaHuman's template body and keeps its skin weights, so it is a
MetaHuman-derived file: it lives under /Game/Ledger/MetaHumans (never in the
public repository), which the build machine mirrors into the game project
with the cast (ledger-probe-unreal.yml). In the game it is a skeletal mesh
that follows a cast member's body by leader pose (LedgerJacket.h), in the
size that wearer takes: donkey_jacket.fbx becomes SKM_DonkeyJacket,
donkey_jacket_l.fbx SKM_DonkeyJacket_L.

Writes import-jacket.txt beside the project: each asset's path, skeleton,
size and material slots.
"""
import os
import time

DEST = "/Game/Ledger/MetaHumans/Clothing/DonkeyJacket"


def asset_name(fbx):
    """donkey_jacket.fbx -> SKM_DonkeyJacket; donkey_jacket_l.fbx -> SKM_DonkeyJacket_L."""
    stem = os.path.splitext(os.path.basename(fbx))[0]
    size = stem.partition("_jacket")[2].strip("_")
    return "SKM_DonkeyJacket" + ("_" + size.upper() if size else "")


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "import-jacket.txt")
    fbxs = [f for f in os.environ.get("LEDGER_JACKET_FBX", "F:/LedgerTools/tmp/jacket/donkey_jacket.fbx").split(",") if f]

    def one(fbx, lines):
        name = asset_name(fbx)
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_as_skeletal", True)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
        ui.set_editor_property("import_materials", True)
        ui.set_editor_property("import_textures", False)
        ui.set_editor_property("import_animations", False)
        ui.set_editor_property("create_physics_asset", False)
        sk = ui.get_editor_property("skeletal_mesh_import_data")
        sk.set_editor_property("import_morph_targets", False)
        sk.set_editor_property("convert_scene", True)
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", fbx)
        task.set_editor_property("destination_path", DEST)
        task.set_editor_property("destination_name", name)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        task.set_editor_property("options", ui)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        lines.append("imported %s: %s" % (fbx, ", ".join(task.get_editor_property("imported_object_paths"))))
        mesh = unreal.load_asset(DEST + "/" + name)
        if mesh is None:
            lines.append("MISSING %s/%s" % (DEST, name))
            return
        b = mesh.get_bounds()
        lines.append("  bounds extent cm: %s" % [round(x, 1) for x in (b.box_extent.x, b.box_extent.y, b.box_extent.z)])
        lines.append("  bounds origin cm: %s" % [round(x, 1) for x in (b.origin.x, b.origin.y, b.origin.z)])
        skel = mesh.get_editor_property("skeleton")
        lines.append("  skeleton: %s" % (skel.get_path_name() if skel else "none"))
        lines.append("  materials: %s" % [str(m.get_editor_property("material_slot_name")) for m in mesh.get_editor_property("materials")])
        unreal.EditorAssetLibrary.save_directory(DEST)

    def run():
        lines = []
        for fbx in fbxs:
            one(fbx, lines)
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
                fh.write("RAISED %r\n" % e)
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
