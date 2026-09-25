"""Import the flat cap sewn in Blender (tools/meshgen/blender/sew_cap.py) as a static mesh.

    set LEDGER_MH_SCRIPT=import_cap
    set LEDGER_CAP_FBX=F:/LedgerTools/freesewing/cap/sew/cap.fbx
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 25 September: the first garment on the free route, from FreeSewing's
pattern to worn in the street. A cap does not bend with the body, so it is a
static mesh riding the head bone (the portrait tool's -PortraitHat); the
outfit tools that fit one garment to many bodies are for the jacket.

It goes beside the jacket under /Game/Ledger/MetaHumans/Clothing, which the
game project on this PC shares with the scratch project, so the portrait
tool finds both by the same path. Writes import-cap.txt beside the project:
the asset, its size and its material.
"""
import os
import time

DEST = "/Game/Ledger/MetaHumans/Clothing/FlatCap"
NAME = "SM_FlatCap_Florent"
MATERIAL = "M_FlatCap_Wool"
WOOL = (0.045, 0.038, 0.030)      # linear: a dark grey-brown tweed


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "import-cap.txt")
    fbx = os.environ.get("LEDGER_CAP_FBX", "F:/LedgerTools/freesewing/cap/sew/cap.fbx")

    def run():
        lines = []
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_as_skeletal", False)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
        ui.set_editor_property("import_materials", True)
        ui.set_editor_property("import_textures", False)
        ui.set_editor_property("import_animations", False)
        sm = ui.get_editor_property("static_mesh_import_data")
        sm.set_editor_property("combine_meshes", True)
        sm.set_editor_property("convert_scene", True)
        sm.set_editor_property("generate_lightmap_u_vs", False)
        sm.set_editor_property("auto_generate_collision", False)
        sm.set_editor_property("normal_import_method", unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", fbx)
        task.set_editor_property("destination_path", DEST)
        task.set_editor_property("destination_name", NAME)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        task.set_editor_property("options", ui)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        lines.append("imported %s: %s" % (fbx, ", ".join(task.get_editor_property("imported_object_paths"))))
        mesh = unreal.load_asset(DEST + "/" + NAME)
        if mesh is None:
            lines.append("MISSING %s/%s" % (DEST, NAME))
        else:
            # ITS OWN CLOTH: the importer reused an old material of the same
            # name, and a renamed one came in as the grey placeholder, so the
            # cap's material is made here: a dark grey-brown wool, matte.
            mat = unreal.load_asset(DEST + "/" + MATERIAL)
            if mat is None:
                mat = unreal.AssetToolsHelpers.get_asset_tools().create_asset(MATERIAL, DEST, unreal.Material, unreal.MaterialFactoryNew())
            mel = unreal.MaterialEditingLibrary
            mel.delete_all_material_expressions(mat)
            colour = mel.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -300, 0)
            colour.set_editor_property("constant", unreal.LinearColor(*WOOL, 1.0))
            rough = mel.create_material_expression(mat, unreal.MaterialExpressionConstant, -300, 200)
            rough.set_editor_property("r", 0.92)
            mel.connect_material_property(colour, "", unreal.MaterialProperty.MP_BASE_COLOR)
            mel.connect_material_property(rough, "", unreal.MaterialProperty.MP_ROUGHNESS)
            mel.recompile_material(mat)
            unreal.EditorAssetLibrary.save_loaded_asset(mat)
            mesh.set_material(0, mat)
            unreal.EditorAssetLibrary.save_loaded_asset(mesh)
            b = mesh.get_bounds()
            lines.append("bounds extent cm: %s" % [round(x, 1) for x in (b.box_extent.x, b.box_extent.y, b.box_extent.z)])
            lines.append("bounds origin cm: %s" % [round(x, 1) for x in (b.origin.x, b.origin.y, b.origin.z)])
            lines.append("materials: %s" % [(str(m.get_editor_property("material_slot_name")), m.get_editor_property("material_interface").get_name() if m.get_editor_property("material_interface") else None) for m in mesh.get_editor_property("static_materials")])
        unreal.EditorAssetLibrary.save_directory(DEST)
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
