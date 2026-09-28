"""The donkey jacket as an Unreal cloth asset, from Epic's static-mesh cloth template, by script.

    set LEDGER_MH_SCRIPT=make_cloth_jacket
    set LEDGER_JACKET_DIR=F:/LedgerTools/tmp/drape      (NAME_render_static.fbx and NAME_sim_static.fbx, tools/meshgen/blender/drape_jacket.py)
    set LEDGER_JACKET_NAME=ron_donkey
    set LEDGER_JACKET_BODY=/Game/Ledger/Export/MH_RoccoP2/MH_RoccoP2_Body     (the body the jacket was hung on; tools/ue/export_dcc.py, geometry mode)
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY, 28 September (Jafar's list, item 5; production/research/character-
pipeline/cloth-graph-python-2026-09-28.md). Epic's cloth template
DF_StaticMeshClothTemplate reads a render and a simulation static mesh
(its nodes StaticMesh_Render and StaticMesh_SIM), copies skin weights from a
skeletal mesh (TransferSkinWeights), sets the simulation's settings and writes
a cloth asset (its terminal). Its node names were read from the template file
itself, since Python cannot list a graph. This imports the two meshes, copies
Epic's cloth asset template and graph under /Game/Ledger/Cloth/<NAME>, lists
the graph's variables, sets the meshes and the body (as variables where the
template has them, otherwise as node properties), regenerates the cloth asset
and writes what happened to cloth-jacket.txt beside the project.
"""
import os
import time

ROOT = "/Game/Ledger/Cloth/"


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "cloth-jacket.txt")
    lines = []

    def log(l):
        lines.append(l)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def import_static(fbx, dest, name):
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", fbx)
        task.set_editor_property("destination_path", dest)
        task.set_editor_property("destination_name", name)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_as_skeletal", False)
        ui.set_editor_property("import_mesh", True)
        # THE JACKET'S OWN COLOURS: navy wool, the black yoke, the buttons, as
        # Blender made them (without them it wore the engine's grey, 28 September).
        ui.set_editor_property("import_materials", True)
        ui.set_editor_property("import_textures", False)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
        ui.static_mesh_import_data.set_editor_property("combine_meshes", True)
        ui.static_mesh_import_data.set_editor_property("convert_scene", True)
        task.set_editor_property("options", ui)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        paths = list(task.get_editor_property("imported_object_paths") or [])
        log("imported %s -> %s" % (os.path.basename(fbx), paths))
        return unreal.load_asset(paths[0]) if paths else None

    # THE JACKET'S COLOURS on the render mesh's slots, by the slot names Blender
    # gave them (a re-import over the existing mesh brought no materials, 28
    # September): instances of the engine's basic shape material, whose one
    # parameter is its colour.
    COLOURS = {"wool": (0.035, 0.043, 0.075), "yoke": (0.012, 0.012, 0.013), "button": (0.02, 0.018, 0.016)}

    def colour_render_mesh(mesh, dest):
        # A BASE MATERIAL OF OUR OWN, flagged for skinned meshes and cloth: the
        # engine's basic shape material is not, and on the game's cloth
        # component it fell back to the engine's grey (28 September).
        base_path = dest + "/M_DonkeyJacket_Base"
        base = unreal.load_asset(base_path) if unreal.EditorAssetLibrary.does_asset_exist(base_path) else             unreal.EditorAssetLibrary.duplicate_asset("/Engine/BasicShapes/BasicShapeMaterial", base_path)
        for flag in ("used_with_skeletal_mesh", "used_with_clothing"):
            try:
                base.set_editor_property(flag, True)
            except Exception as e:
                log("  %s: %s" % (flag, e))
        unreal.MaterialEditingLibrary.recompile_material(base)
        unreal.EditorAssetLibrary.save_loaded_asset(base, only_if_is_dirty=False)
        log("base material %s: skeletal %s, clothing %s" % (base_path, base.get_editor_property("used_with_skeletal_mesh"),
                                                            base.get_editor_property("used_with_clothing")))
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        mats = mesh.get_editor_property("static_materials")
        for i, sm in enumerate(mats):
            slot = str(sm.get_editor_property("material_slot_name")).lower()
            key = next((k for k in COLOURS if k in slot), "wool")
            name = "MI_DonkeyJacket_" + key.capitalize()
            path = dest + "/" + name
            mi = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else tools.create_asset(
                name, dest, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
            unreal.MaterialEditingLibrary.set_material_instance_parent(mi, base)
            r, g, b = COLOURS[key]
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, "Color", unreal.LinearColor(r, g, b, 1.0))
            unreal.EditorAssetLibrary.save_loaded_asset(mi, only_if_is_dirty=False)
            mesh.set_material(i, mi)
            log("slot %d %s -> %s" % (i, slot, name))
        unreal.EditorAssetLibrary.save_loaded_asset(mesh, only_if_is_dirty=False)

    def run():
        src = os.environ.get("LEDGER_JACKET_DIR", "F:/LedgerTools/tmp/drape")
        name = os.environ.get("LEDGER_JACKET_NAME", "ron_donkey")
        body_path = os.environ.get("LEDGER_JACKET_BODY", "/Game/Ledger/Export/MH_RoccoP2/MH_RoccoP2_Body")
        dest = ROOT + name
        render = import_static(os.path.join(src, name + "_render_static.fbx"), dest, "SM_" + name + "_Render")
        sim = import_static(os.path.join(src, name + "_sim_static.fbx"), dest, "SM_" + name + "_Sim")
        if render is not None:
            colour_render_mesh(render, dest)
        body = unreal.load_asset(body_path)
        log("body %s: %s" % (body_path, type(body).__name__ if body else "NOT FOUND"))
        lib = unreal.EditorAssetLibrary
        # A FRESH PAIR EACH TIME, under the time it was made: the template's
        # import nodes keep their own copy of the meshes from the first import
        # and refresh only when their Reimport button is pressed, so a kept
        # graph never saw the new ease or colours (28 September); and deleting
        # a pair and copying again under the same name failed.
        stamp = time.strftime("%m%d%H%M")
        df_path, ca_path = dest + "/DF_" + name + "_" + stamp, dest + "/CA_" + name + "_" + stamp
        df = lib.duplicate_asset("/ChaosClothAsset/DF_StaticMeshClothTemplate", df_path)
        ca = lib.duplicate_asset("/ChaosClothAsset/CA_Template", ca_path)
        log("cloth asset path %s.%s" % (ca_path, ca_path.split("/")[-1]))
        log("graph %s, cloth asset %s" % (type(df).__name__ if df else None, type(ca).__name__ if ca else None))
        if not (df and ca and render and sim):
            return
        # the cloth asset's own graph: point it at our copy
        for prop in ("dataflow_instance", "dataflow"):
            try:
                inst = ca.get_editor_property(prop)
                log("cloth asset %s = %r" % (prop, inst))
                if prop == "dataflow_instance":
                    inst.set_editor_property("dataflow_asset", df)
                    ca.set_editor_property(prop, inst)
                else:
                    ca.set_editor_property(prop, df)
                log("  set %s to our graph" % prop)
                break
            except Exception as e:
                log("  %s: %s %s" % (prop, type(e).__name__, e))
        dbl = unreal.DataflowBlueprintLibrary
        # NODE PROPERTIES, not variables: listing the graph's variables on the
        # copied cloth asset crashed the engine (a null read in DataflowEngine,
        # 28 September).
        del_ = unreal.DataflowEditorBlueprintLibrary
        for node, prop, obj in (("StaticMesh_Render", "StaticMesh", render), ("StaticMesh_SIM", "StaticMesh", sim),
                                ("TransferSkinWeights", "SkeletalMesh", body)):
            if obj is None:
                continue
            try:
                done = del_.set_dataflow_node_property(df, node, prop, obj.get_path_name())
            except Exception as e:
                done = "%s %s" % (type(e).__name__, e)
            log("set %s.%s = %s: %s" % (node, prop, obj.get_path_name(), done))
        try:
            ok = dbl.regenerate_asset_from_dataflow(ca, False)
            log("regenerate: %s" % ok)
        except Exception as e:
            log("regenerate: %s %s" % (type(e).__name__, e))
        for a in (df, ca):
            lib.save_loaded_asset(a, only_if_is_dirty=False)
        log("done")

    def tick(delta):
        if st["done"] or time.time() - st["t0"] < seconds:
            return
        st["done"] = True
        unreal.unregister_slate_post_tick_callback(st["h"])
        try:
            run()
        except Exception as e:
            log("raised %r" % (e,))
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)
