"""A skinned garment whose loose part is cloth, by script (item 7, 1 October).

    set LEDGER_MH_SCRIPT=make_cloth_garment
    set LEDGER_GARMENT_DIR=F:/LedgerTools/garments/suit_jacket_test/ron    (NAME_static.fbx and NAME_skinned.fbx)
    set LEDGER_GARMENT_NAME=ron_suit_jacket
    set LEDGER_GARMENT_BODY=/Game/Ledger/Export/MH_RoccoP2/MH_RoccoP2_Body (the body it was made on)
    set LEDGER_GARMENT_FREE=97.2,86.9,4   (skinned above the first height, cm; free by up to the
                                           last value, cm, at the second; garment.json's simMaxDistance)
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended

WHY. Jafar, 30 September: a garment is a skeletal mesh skinned to the
MetaHuman skeleton, and only loose parts, a coat's hem or a skirt, are
cloth. The clothing session hands over the garment skinned panel by panel
and, unskinned, the same mesh for the cloth route (its README). This makes
one Chaos cloth asset from Epic's static-mesh cloth template
(DF_StaticMeshClothTemplate, as tools/ue/make_cloth_jacket.py does) with:

- the skin weights copied from the clothing session's own skinned garment
  (TransferSkinWeights, closest point on the surface of the same shape, so
  its panel binding is kept), not from the body;
- how far each point may leave the skinned shape written onto the cloth's
  simulation mesh as a weight layer by height (production/research/
  character-pipeline/cloth-weight-maps-2026-09-29.md, route B: Geometry
  Script's weight maps, carried by the template's static-mesh import), 0
  above the hip line, rising to 1 at the hem, and the max-distance setting
  pointed at that layer by name (LedgerMaxDistance), so nothing depends on
  the template's own painted map or on splicing its graph;
- a material instance per slot, MI_Slot_<slot> and MI_Slot_<number>, from the garment's own
  colour and normal textures, which the game sets on the cloth component
  (LedgerJacket.h, WearCloth).

Writes cloth-garment.txt beside the project: what was imported, the layer's
heights and counts, each property set and the regeneration's result.
"""
import os
import time

ROOT = "/Game/Ledger/Cloth/"
LAYER = "LedgerMaxDistance"
# In the graph the values go into the template's own map, after its paint node:
# the max-distance setting's weight-map name is also an input pin, wired from
# that node's "MaxDistance", which overrode any other name set on it (1 October:
# LedgerMaxDistance, even at a constant 1, freed nothing).
GRAPH_MAP = "MaxDistance"
# Plain colours by slot name, as the clothing session made it (charcoal cloth,
# the shirt front, the tie, the buttons); anything else takes the cloth's.
COLOURS = {"shirt": (0.62, 0.62, 0.6), "tie": (0.09, 0.03, 0.03), "button": (0.015, 0.014, 0.013), "cloth": (0.03, 0.03, 0.032)}
ROUGHNESS = {"shirt": 0.8, "tie": 0.6, "button": 0.4, "cloth": 0.9}


def weight_at(z, top, hem):
    """0 at and above the hip line (top), 1 at and below the hem, straight between."""
    if top <= hem:
        return 0.0
    return min(1.0, max(0.0, (top - z) / (top - hem)))


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "cloth-garment.txt")
    lines = []

    def log(l):
        lines.append(l)
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")

    def import_fbx(fbx, dest, name, skeleton=None):
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", fbx)
        task.set_editor_property("destination_path", dest)
        task.set_editor_property("destination_name", name)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_materials", True)
        ui.set_editor_property("import_textures", False)
        if skeleton is None:
            ui.set_editor_property("import_as_skeletal", False)
            ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
            ui.static_mesh_import_data.set_editor_property("combine_meshes", True)
            ui.static_mesh_import_data.set_editor_property("convert_scene", True)
        else:
            ui.set_editor_property("import_as_skeletal", True)
            ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
            ui.set_editor_property("skeleton", skeleton)
            ui.set_editor_property("import_animations", False)
            ui.skeletal_mesh_import_data.set_editor_property("convert_scene", True)
        task.set_editor_property("options", ui)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        paths = list(task.get_editor_property("imported_object_paths") or [])
        want = unreal.StaticMesh if skeleton is None else unreal.SkeletalMesh
        meshes = [a for a in (unreal.load_asset(p) for p in paths) if isinstance(a, want)]
        log("imported %s -> %s" % (os.path.basename(fbx), [p for p in paths]))
        return meshes[0] if meshes else None

    def import_texture(png, dest, name, normal=False):
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", png)
        task.set_editor_property("destination_path", dest)
        task.set_editor_property("destination_name", name)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", False)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        paths = list(task.get_editor_property("imported_object_paths") or [])
        tex = unreal.load_asset(paths[0]) if paths else None
        if tex is not None and normal:
            # The maker's normal map is OpenGL's way up: Unreal wants green flipped.
            tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
            tex.set_editor_property("srgb", False)
            tex.set_editor_property("flip_green_channel", True)
        if tex is not None:
            unreal.EditorAssetLibrary.save_loaded_asset(tex, only_if_is_dirty=False)
        log("texture %s -> %s" % (os.path.basename(png), tex.get_path_name() if tex else "NOT IMPORTED"))
        return tex

    def slot_materials(mesh, dest, src, name):
        """MI_Slot_<slot> per material slot, under a matt base flagged for skinned meshes and
        cloth: the garment's own colour and normal textures where it has them
        (NAME_basecolor.png, NAME_normal.png), else a plain colour by the slot's name."""
        mel = unreal.MaterialEditingLibrary
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        colour_png, normal_png = (os.path.join(src, name + s) for s in ("_basecolor.png", "_normal.png"))
        colour_tex = import_texture(colour_png, dest, "T_" + name + "_BaseColor") if os.path.exists(colour_png) else None
        normal_tex = import_texture(normal_png, dest, "T_" + name + "_Normal", normal=True) if os.path.exists(normal_png) else None
        base_path = dest + "/M_Garment_Matt"
        if unreal.EditorAssetLibrary.does_asset_exist(base_path):
            base = unreal.load_asset(base_path)
        else:
            base = tools.create_asset("M_Garment_Matt", dest, unreal.Material, unreal.MaterialFactoryNew())
            col = mel.create_material_expression(base, unreal.MaterialExpressionVectorParameter, -700, 0)
            col.set_editor_property("parameter_name", "Color")
            col.set_editor_property("default_value", unreal.LinearColor(1.0, 1.0, 1.0, 1.0))
            tex = mel.create_material_expression(base, unreal.MaterialExpressionTextureSampleParameter2D, -700, 200)
            tex.set_editor_property("parameter_name", "BaseColorMap")
            if colour_tex is not None:
                tex.set_editor_property("texture", colour_tex)
            mul = mel.create_material_expression(base, unreal.MaterialExpressionMultiply, -350, 100)
            mel.connect_material_expressions(col, "", mul, "A")
            mel.connect_material_expressions(tex, "RGB", mul, "B")
            mel.connect_material_property(mul, "", unreal.MaterialProperty.MP_BASE_COLOR)
            if normal_tex is not None:
                nrm = mel.create_material_expression(base, unreal.MaterialExpressionTextureSampleParameter2D, -700, 450)
                nrm.set_editor_property("parameter_name", "NormalMap")
                nrm.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
                nrm.set_editor_property("texture", normal_tex)
                mel.connect_material_property(nrm, "RGB", unreal.MaterialProperty.MP_NORMAL)
            rough = mel.create_material_expression(base, unreal.MaterialExpressionScalarParameter, -700, 650)
            rough.set_editor_property("parameter_name", "Roughness")
            rough.set_editor_property("default_value", 0.9)
            mel.connect_material_property(rough, "", unreal.MaterialProperty.MP_ROUGHNESS)
        for flag in ("used_with_skeletal_mesh", "used_with_clothing"):
            base.set_editor_property(flag, True)
        mel.recompile_material(base)
        unreal.EditorAssetLibrary.save_loaded_asset(base, only_if_is_dirty=False)
        for i, sm in enumerate(mesh.get_editor_property("static_materials")):
            slot = str(sm.get_editor_property("material_slot_name"))
            key = next((k for k in COLOURS if k in slot.lower()), "cloth")
            # By the slot's name and by its number: the cloth asset the template
            # makes can carry the slot unnamed (1 October), and the game then
            # looks the instance up by number (LedgerJacket.h, WearCloth).
            for mi_name in ("MI_Slot_" + slot, "MI_Slot_%d" % i):
                path = dest + "/" + mi_name
                mi = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else tools.create_asset(
                    mi_name, dest, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
                mel.set_material_instance_parent(mi, base)
                if colour_tex is not None:
                    mel.set_material_instance_texture_parameter_value(mi, "BaseColorMap", colour_tex)
                    mel.set_material_instance_vector_parameter_value(mi, "Color", unreal.LinearColor(1.0, 1.0, 1.0, 1.0))
                else:
                    r, g, b = COLOURS[key]
                    mel.set_material_instance_vector_parameter_value(mi, "Color", unreal.LinearColor(r, g, b, 1.0))
                mel.set_material_instance_scalar_parameter_value(mi, "Roughness", ROUGHNESS[key])
                unreal.EditorAssetLibrary.save_loaded_asset(mi, only_if_is_dirty=False)
                log("slot %d %s -> %s (%s)" % (i, slot, mi_name, "its texture" if colour_tex else key))

    def write_layer(sm, top, hem):
        """The LedgerMaxDistance weight layer on the static mesh, by each point's height."""
        gs = unreal

        def lib_with(method):
            # Geometry Script's function libraries go by different Python names
            # across versions (GeometryScript_ListUtils is not one here): find
            # the class by the method it offers.
            names = [n for n in dir(unreal) if "GeometryScript" in n and hasattr(getattr(unreal, n), method)]
            # the function libraries (GeometryScript_..., GeometryScriptLibrary_...) before the
            # list structs, whose same-named methods want the list itself
            names.sort(key=lambda n: (not ("_" in n), n))
            log("  %s offered by %s" % (method, names))
            if names:
                return getattr(unreal, names[0])
            raise AttributeError("no Geometry Script library offers " + method)

        dm = gs.DynamicMesh()
        opts = gs.GeometryScriptCopyMeshFromAssetOptions()
        opts.set_editor_property("apply_build_settings", False)
        lod = gs.GeometryScriptMeshReadLOD()
        res = gs.GeometryScript_AssetUtils.copy_mesh_from_static_mesh(sm, dm, opts, lod)
        dm = res[0] if isinstance(res, tuple) else dm
        pos = lib_with("get_all_vertex_positions").get_all_vertex_positions(dm, False)
        plist = next((x for x in (pos if isinstance(pos, tuple) else (pos,)) if type(x).__name__ == "GeometryScriptVectorList"), None)
        pts = lib_with("convert_vector_list_to_array").convert_vector_list_to_array(plist)
        zs = [p.z for p in pts]
        values = [weight_at(z, top, hem) for z in zs]
        log("layer: %d points, z %.1f to %.1f cm; free %d, partly %d, skinned %d"
            % (len(zs), min(zs), max(zs), sum(1 for v in values if v >= 1.0),
               sum(1 for v in values if 0.0 < v < 1.0), sum(1 for v in values if v <= 0.0)))
        found = lib_with("find_or_add_mesh_weight_map").find_or_add_mesh_weight_map(dm, LAYER)
        handle = next((x for x in (found if isinstance(found, tuple) else (found,)) if type(x).__name__ == "GeometryScriptWeightMapHandle"), None)
        log("  weight map handle: %s" % (handle,))
        wm = lib_with("set_mesh_weight_map_values")
        log("  weight map library %s: %s" % (wm.__name__, [m for m in dir(wm) if "weight" in m.lower()]))
        conv = lib_with("convert_array_to_scalar_list")
        scalars = conv.convert_array_to_scalar_list(values)
        log("  scalar list: %s" % type(scalars).__name__)
        if isinstance(scalars, tuple):
            scalars = next((x for x in scalars if type(x).__name__ == "GeometryScriptScalarList"), scalars)
        log("  %s" % (wm.set_mesh_weight_map_values.__doc__ or "").splitlines()[:1])
        wm.set_mesh_weight_map_values(dm, scalars, handle, False)
        wopts = gs.GeometryScriptCopyMeshToAssetOptions()
        for prop, v in (("enable_recompute_normals", False), ("enable_recompute_tangents", False),
                        ("replace_materials", False), ("emit_transaction", False)):
            try:
                wopts.set_editor_property(prop, v)
            except Exception as e:
                log("  copy-to-asset option %s: %s" % (prop, e))
        wlod = gs.GeometryScriptMeshWriteLOD()
        gs.GeometryScript_AssetUtils.copy_mesh_to_static_mesh(dm, sm, wopts, wlod)
        unreal.EditorAssetLibrary.save_loaded_asset(sm, only_if_is_dirty=False)
        log("layer %s written onto %s" % (LAYER, sm.get_path_name()))

    def run():
        src = os.environ.get("LEDGER_GARMENT_DIR", "F:/LedgerTools/garments/suit_jacket_test/ron")
        name = os.environ.get("LEDGER_GARMENT_NAME", "ron_suit_jacket")
        body_path = os.environ.get("LEDGER_GARMENT_BODY", "/Game/Ledger/Export/MH_RoccoP2/MH_RoccoP2_Body")
        # Git Bash turns "/Game/..." in the environment into "C:/Program Files/Git/Game/...": keep the asset path.
        body_path = body_path[body_path.find("/Game/"):] if "/Game/" in body_path else body_path
        top, hem, most = (float(v) for v in os.environ.get("LEDGER_GARMENT_FREE", "97.2,86.9,4").split(","))
        dest = ROOT + name
        body = unreal.load_asset(body_path)
        skel = body.get_editor_property("skeleton") if body else None
        log("body %s: %s, skeleton %s" % (body_path, type(body).__name__ if body else "NOT FOUND",
                                          skel.get_path_name() if skel else "none"))
        sim = import_fbx(os.path.join(src, name + "_static.fbx"), dest, "SM_" + name)
        skinned = import_fbx(os.path.join(src, name + "_skinned.fbx"), dest, "SKM_" + name, skeleton=skel) if skel else None
        log("skinned garment: %s" % (skinned.get_path_name() if skinned else "NOT IMPORTED"))
        if sim is None or skinned is None:
            return
        slot_materials(sim, dest, src, name)
        write_layer(sim, top, hem)
        lib = unreal.EditorAssetLibrary
        stamp = time.strftime("%m%d%H%M")
        df_path, ca_path = dest + "/DF_" + name + "_" + stamp, dest + "/CA_" + name + "_" + stamp
        df = lib.duplicate_asset("/ChaosClothAsset/DF_StaticMeshClothTemplate", df_path)
        ca = lib.duplicate_asset("/ChaosClothAsset/CA_Template", ca_path)
        log("cloth asset path %s.%s" % (ca_path, ca_path.split("/")[-1]))
        if not (df and ca):
            return
        inst = ca.get_editor_property("dataflow_instance")
        inst.set_editor_property("dataflow_asset", df)
        ca.set_editor_property("dataflow_instance", inst)
        del_ = unreal.DataflowEditorBlueprintLibrary
        settings = (("StaticMesh_Render", "StaticMesh", sim.get_path_name()),
                    ("StaticMesh_SIM", "StaticMesh", sim.get_path_name()),
                    ("TransferSkinWeights", "SkeletalMesh", skinned.get_path_name()),
                    ("TransferSkinWeights", "TransferMethod", "ClosestPointOnSurface"),
                    ("SimulationMaxDistanceConfig", "MaxDistance",
                     '(bIsAnimatable=True,Low=0.000000,High=%f,WeightMap="%s")' % (most, GRAPH_MAP if os.environ.get("LEDGER_GARMENT_ROUTE", "graph") == "graph" else LAYER)
                     if not os.environ.get("LEDGER_GARMENT_UNIFORM") else
                     # a diagnostic: the whole garment free by this much, the layer ignored
                     '(bIsAnimatable=True,Low=%s,High=%s)' % (os.environ["LEDGER_GARMENT_UNIFORM"], os.environ["LEDGER_GARMENT_UNIFORM"])))
        for node, prop, value in settings:
            try:
                done = del_.set_dataflow_node_property(df, node, prop, value)
            except Exception as e:
                done = "%s %s" % (type(e).__name__, e)
            log("set %s.%s = %s: %s" % (node, prop, value, done))
        # ROUTE A (the research's first choice; the layer on the mesh, route B,
        # did not reach the cloth, 1 October: at 30 cm its skirt never moved):
        # a height gradient inside the graph, written as the LedgerMaxDistance
        # attribute of the simulation vertices just before the max-distance
        # setting reads it.
        if os.environ.get("LEDGER_GARMENT_ROUTE", "graph") == "graph":
            v2 = unreal.Vector2D
            for typ, base, at in (("FDataflowLinearGradientFloatSamplerNode", "LedgerGradient", v2(-400.0, 600.0)),
                                  ("FDataflowFloatSamplerToAttributeNode", "LedgerToMaxDistance", v2(-100.0, 600.0))):
                try:
                    got = del_.add_dataflow_node(df, typ, base, at)
                except Exception as e:
                    got = "%s %s" % (type(e).__name__, e)
                log("add %s as %s: %s" % (typ, base, got))
            graph_sets = (("LedgerGradient", "Gradient",
                           "(StartPoint=(X=0.000000,Y=0.000000,Z=%f),StartValue=%s,EndPoint=(X=0.000000,Y=0.000000,Z=%f),EndValue=1.000000,bClamp=True)" % (top, os.environ.get("LEDGER_GARMENT_STARTVALUE", "0.000000"), hem)),
                          ("LedgerToMaxDistance", "AttributeName", GRAPH_MAP),
                          ("LedgerToMaxDistance", "VertexGroup", '(Name="SimVertices3D")'))
            for node, prop, value in graph_sets:
                try:
                    done = del_.set_dataflow_node_property(df, node, prop, value)
                except Exception as e:
                    done = "%s %s" % (type(e).__name__, e)
                log("set %s.%s = %s: %s" % (node, prop, value, done))
            for frm, out_pin, to, in_pin in (("LedgerGradient", "Sampler", "LedgerToMaxDistance", "Sampler"),
                                             ("WeightMap_MaxDistance", "Collection", "LedgerToMaxDistance", "Collection"),
                                             ("LedgerToMaxDistance", "Collection", "SimulationMaxDistanceConfig", "Collection")):
                try:
                    done = del_.connect_dataflow_nodes(df, frm, out_pin, to, in_pin)
                except Exception as e:
                    done = "%s %s" % (type(e).__name__, e)
                log("connect %s.%s -> %s.%s: %s" % (frm, out_pin, to, in_pin, done))
        try:
            log("regenerate: %s" % unreal.DataflowBlueprintLibrary.regenerate_asset_from_dataflow(ca, False))
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
            import traceback
            log("raised %r" % (e,))
            log(traceback.format_exc())
        finally:
            unreal.SystemLibrary.quit_editor()

    st["h"] = unreal.register_slate_post_tick_callback(tick)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_cloth_garment selftest FAIL " + name)
    check("skinned above the hip line", weight_at(100.0, 97.2, 86.9) == 0.0 and weight_at(97.2, 97.2, 86.9) == 0.0)
    check("free at and below the hem", weight_at(86.9, 97.2, 86.9) == 1.0 and weight_at(80.0, 97.2, 86.9) == 1.0)
    check("straight between", abs(weight_at(92.05, 97.2, 86.9) - 0.5) < 1e-9)
    check("no layer when the heights are the wrong way round", weight_at(90.0, 86.9, 97.2) == 0.0)
    print("make_cloth_garment selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    import sys
    sys.exit(selftest() if "--selftest" in sys.argv else 0)
