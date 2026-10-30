"""Give a built MetaHuman a body hidden face map by script, rebuild it, and record what the build changed.

    set LEDGER_MH_SCRIPT=hidden_faces
    set LEDGER_HF_STEP=probe            (or build)
    UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject -unattended
        (the project's Content/Python/init_unreal.py calls main_after_idle())
    python tools/ue/hidden_faces.py --selftest     # runs without Unreal

WHY, 30 October 2026. Tom's skin came through his own garments (the jacket's sleeves at the elbows with
his arms hanging, the jeans' crotch, the boots), which the game puts on over his built MetaHuman as
skeletal meshes following the body (ue-probe LedgerGarments.h). MetaHuman's own way to stop that is a
body hidden face map on a wardrobe item: the Optimized build cuts the body's faces under it on every
LOD (production/research/character-pipeline/HIDDEN-FACES-2026-10-30.md, the engine source and lines).

HOW. The engine's plain garment (WI_DefaultGarment, a T-shirt and shorts) already carries a map
(DG_BodyShapeA_BodyMask) and Tom wears two copies of it in the Outfits slot (the base preset's and the
cast maker's). A wardrobe item's map cannot be set on Tom's character alone, and the engine's own item
is not ours to edit, so:
  probe  records Tom's slot selections, the default garment's map and settings, exports that map as
         PNG, and exports the game's current build (body and face as FBX with every LOD, a few baked
         textures, every material instance's parameters, the folder's asset list) to OUT/before/.
  build  imports OUT/map/tom_body_hidden_faces.png as a linear texture, duplicates WI_DefaultGarment
         into /Game/Ledger/Wardrobe with that texture as its body hidden face map, swaps the second of
         Tom's two default-garment selections for it (so he still wears two, the first unchanged), builds
         him Optimized/High exactly as make_cast_metahumans.py's build step does (its hair recolour after),
         into LEDGER_HF_BUILD_ROOT (a side folder by default, below), then exports the same records to
         OUT/after/. A side build puts Tom's selections back and saves; put the character's file back
         from OUT/before/files afterwards all the same (the editor closed), and check its hash.
The build combines every pinned item's map (the lowest value wins), so Tom's body loses the union of
the default garment's cut and ours.

THE OUTFIT'S EDITOR PIPELINE IS NOT EXPOSED TO PYTHON (30 October, probe try 1): it is wrapped as its parent,
MetaHumanItemEditorPipeline, so its own properties answer only to their C++ names (BodyHiddenFaceMapTexture),
not the snake-case Python ones.

PUTTING IT BACK: the game's copy is untouched by a side build; delete /Game/Ledger/HiddenFaces and
/Game/Ledger/Wardrobe in the editor if they are not wanted. A build over the game's copy is undone by copying
OUT/before/files/MetaHumans/MH_TomL1 and OUT/before/files/Cast/MH_TomL1.uasset back with no editor open.

ONE JSON PER STEP in OUT (probe.json, build.json), and one line in the project's ue-material.txt.
"""
import json
import os
import sys
import time

CHARACTER = "/Game/Cast/MH_TomL1"
WHO, TAKE = "tom", "L1"
GAME_ROOT = "/Game/Ledger/MetaHumans"
# A SIDE BUILD BY DEFAULT (30 October): the game reads /Game/Ledger/MetaHumans/MH_TomL1 (a junction from
# ue-probe), and there Tom wears only his jacket until the jeans, jumper and boots are passed (garments.json
# "hold"; LedgerGarments.h 89-102), so a body cut under the jeans and boots would leave him legless in the
# game. LEDGER_HF_BUILD_ROOT=/Game/Ledger/MetaHumans builds over the game's own copy, once the outfit is passed.
# LEDGER_HF_CONTROL=1: the same build with no map and nothing changed on the character, beside the other, so
# what a rebuild alone changes (the baked textures, 30 October) is told from what the map changes.
CONTROL = os.environ.get("LEDGER_HF_CONTROL", "") == "1"
BUILD_ROOT = os.environ.get("LEDGER_HF_BUILD_ROOT", "/Game/Ledger/HiddenFacesControl" if CONTROL else "/Game/Ledger/HiddenFaces")
BUILT = BUILD_ROOT + "/MH_TomL1"
BUILT_GAME = GAME_ROOT + "/MH_TomL1"
# The character is saved with the item worn only when building the game's own copy; a side build leaves
# the character asset as it was (its file is checked against the copy in OUT/before afterwards).
KEEP_CHARACTER = BUILD_ROOT == GAME_ROOT
GARMENT = "/MetaHumanCharacter/Optional/Clothing/WI_DefaultGarment"
WARDROBE = "/Game/Ledger/Wardrobe"
WI_NAME = "WI_TomL1_HiddenFaces"
TEX_NAME = "T_TomL1_BodyHiddenFaces"
OUT = os.environ.get("LEDGER_HF_OUT", "F:/LedgerTools/bodies/MH_TomL1/hidden-faces")
MAP_PNG = os.environ.get("LEDGER_HF_MAP", OUT + "/map/tom_body_hidden_faces.png")
# The engine's defaults (MetaHumanGeometryRemovalTypes.h 26, 33, 50): black (<= 0.1) cut, white (>= 0.9) kept,
# no shrinking; the build's combined map keeps these too (MetaHumanGeometryRemoval.cpp 30-32).
SETTINGS = {"max_cull_value": 0.1, "min_keep_value": 0.9, "max_shrink_distance": 0.0}
MESHES = ["Body/SKM_MH_TomL1_BodyMesh", "Face/SKM_MH_TomL1_FaceMesh"]   # the *_DNA assets are DNA, not meshes
TEXTURES = ["Face/Baked/T_Head_LOD1_BC", "Body/Baked/T_Body_BC", "Body/Baked/T_Body_N"]
NEED_FREE_GB = 10.0


def pick_swap(outfit_keys):
    """Of the Outfits selections (in order), the one kept and the ones replaced by the hidden-face item."""
    if not outfit_keys:
        return None, []
    return outfit_keys[0], list(outfit_keys[1:])


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("hidden_faces selftest FAIL " + name)
    check("the first of two default garments is kept, the second replaced", pick_swap(["a", "b"]) == ("a", ["b"]))
    check("one default garment: kept, ours added beside it", pick_swap(["a"]) == ("a", []))
    check("none: nothing kept", pick_swap([]) == (None, []))
    check("the engine's own thresholds", SETTINGS["max_cull_value"] == 0.1 and SETTINGS["min_keep_value"] == 0.9)
    check("Tom's built folder", BUILT.endswith("/MH_TomL1") and CHARACTER.endswith("MH_TomL1"))
    check("a side build by default, the character left as it was",
          os.environ.get("LEDGER_HF_BUILD_ROOT") or (BUILD_ROOT != GAME_ROOT and not KEEP_CHARACTER))
    print("hidden_faces selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main_after_idle(seconds=20.0, settle=15.0):
    import unreal
    step_name = os.environ.get("LEDGER_HF_STEP", "probe")
    st = {"t0": time.time(), "h": None, "phase": "wait", "busy": False, "rep": {"step": step_name, "notes": []}}
    rep = st["rep"]
    sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
    os.makedirs(OUT, exist_ok=True)
    log = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")

    def save_report():
        with open(os.path.join(OUT, step_name + ("-control" if CONTROL else "") + ".json"), "w", encoding="utf-8") as fh:
            json.dump(rep, fh, indent=1, default=str)

    def note(s):
        rep["notes"].append(s)
        print("hidden_faces: " + s)
        save_report()

    def key_info(k):
        d = {"str": str(k)}
        for prop in ("variation", "principal_asset_or_external_wardrobe_item"):
            try:
                d[prop] = str(k.get_editor_property(prop))
            except Exception as e:
                d[prop] = "unreadable-" + type(e).__name__
        return d

    def selections(ch):
        out = []
        for d in ch.internal_collection.default_instance.get_slot_selection_data():
            sel = d.get_editor_property("selection")
            out.append((str(sel.get_editor_property("slot_name")), sel.get_editor_property("selected_item")))
        return out

    def prop(obj, *names):
        """An editor property by its Python name or, for a class Python does not expose (the outfit's editor
        pipeline is wrapped as its exposed parent, so its own properties have no Python names), its C++ name."""
        err = None
        for n in names:
            try:
                return obj.get_editor_property(n), n
            except Exception as e:
                err = e
        raise err

    def map_of(wi):
        pl = wi.get_editor_property("pipeline")
        ep = pl.get_editor_property("editor_pipeline")
        hf, st["hf_name"] = prop(ep, "body_hidden_face_map_texture", "BodyHiddenFaceMapTexture")
        s = hf.get_editor_property("settings")
        tex = hf.get_editor_property("texture")
        return {"pipeline": pl.get_class().get_name(), "editor_pipeline": ep.get_class().get_name(), "property_name": st["hf_name"],
                "struct": type(hf).__name__, "texture": tex.get_path_name() if tex else None,
                "size": [tex.blueprint_get_size_x(), tex.blueprint_get_size_y()] if tex else None,
                "srgb": bool(tex.get_editor_property("srgb")) if tex else None,
                "settings": {k: s.get_editor_property(k) for k in SETTINGS}}

    def export_png(tex, dst):
        task = unreal.AssetExportTask()
        task.set_editor_property("object", tex)
        task.set_editor_property("filename", dst)
        task.set_editor_property("exporter", unreal.TextureExporterPNG())
        task.set_editor_property("automated", True)
        task.set_editor_property("prompt", False)
        task.set_editor_property("replace_identical", True)
        ok = unreal.Exporter.run_asset_export_task(task)
        return bool(ok) and os.path.exists(dst)

    def export_fbx(mesh, dst):
        task = unreal.AssetExportTask()
        task.set_editor_property("object", mesh)
        task.set_editor_property("filename", dst)
        task.set_editor_property("exporter", unreal.SkeletalMeshExporterFBX())
        task.set_editor_property("automated", True)
        task.set_editor_property("prompt", False)
        task.set_editor_property("replace_identical", True)
        o = unreal.FbxExportOption()
        o.set_editor_property("level_of_detail", True)
        o.set_editor_property("export_morph_targets", False)
        o.set_editor_property("collision", False)
        task.set_editor_property("options", o)
        ok = unreal.Exporter.run_asset_export_task(task)
        return bool(ok) and os.path.exists(dst)

    def mesh_stats(mesh):
        d = {"path": mesh.get_path_name()}
        sms = unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem)
        try:
            n = sms.get_lod_count(mesh)
            d["lods"] = n
            d["verts"] = [sms.get_num_verts(mesh, i) for i in range(n)]
        except Exception as e:
            d["lod_error"] = repr(e)
        try:
            d["morphs"] = len(mesh.get_all_morph_target_names())
        except Exception as e:
            d["morph_error"] = type(e).__name__
        try:
            d["skeleton"] = mesh.get_editor_property("skeleton").get_path_name()
            d["materials"] = [str(m.get_editor_property("material_slot_name")) + "=" +
                              (m.get_editor_property("material_interface").get_path_name() if m.get_editor_property("material_interface") else "none")
                              for m in mesh.get_editor_property("materials")]
        except Exception as e:
            d["mat_error"] = repr(e)
        return d

    def mi_params(mi):
        d = {}
        for prop, kind in (("scalar_parameter_values", "s"), ("vector_parameter_values", "v"), ("texture_parameter_values", "t")):
            try:
                for pv in mi.get_editor_property(prop):
                    name = str(pv.get_editor_property("parameter_info").get_editor_property("name"))
                    val = pv.get_editor_property("parameter_value")
                    if kind == "v":
                        val = [round(val.r, 5), round(val.g, 5), round(val.b, 5), round(val.a, 5)]
                    elif kind == "t":
                        val = val.get_path_name() if val else None
                    else:
                        val = round(val, 5)
                    d[kind + ":" + name] = val
            except Exception as e:
                d[kind + ":error"] = type(e).__name__
        try:
            parent = mi.get_editor_property("parent")
            d["parent"] = parent.get_path_name() if parent else None
        except Exception:
            pass
        return d

    def record(where, built):
        """A build's state (built: its folder), exported to OUT/<where>/: meshes as FBX, textures as PNG,
        materials and assets as JSON."""
        d = os.path.join(OUT, where)
        os.makedirs(d, exist_ok=True)
        r = {"assets": {}, "meshes": {}, "textures": {}, "materials": {}}
        for p in sorted(unreal.EditorAssetLibrary.list_assets(built, recursive=True, include_folder=False)):
            ad = unreal.EditorAssetLibrary.find_asset_data(p)
            r["assets"][p.split(".")[0]] = str(ad.asset_class_path.asset_name) if ad else "?"
        for m in MESHES:
            mesh = unreal.load_asset(built + "/" + m)
            if mesh is None:
                r["meshes"][m] = "missing"
                continue
            s = mesh_stats(mesh)
            dst = os.path.join(d, m.split("/")[-1] + ".fbx")
            s["fbx"] = dst if export_fbx(mesh, dst) else "export-failed"
            r["meshes"][m] = s
            save_report()
        for t in TEXTURES:
            tex = unreal.load_asset(built + "/" + t)
            if tex is None:
                r["textures"][t] = "missing"
                continue
            dst = os.path.join(d, t.split("/")[-1] + ".png")
            r["textures"][t] = {"size": [tex.blueprint_get_size_x(), tex.blueprint_get_size_y()],
                                "png": dst if export_png(tex, dst) else "export-failed"}
        for p, cls in r["assets"].items():
            if cls == "MaterialInstanceConstant":
                mi = unreal.load_asset(p)
                if mi is not None:
                    r["materials"][p] = mi_params(mi)
        with open(os.path.join(d, "record.json"), "w", encoding="utf-8") as fh:
            json.dump(r, fh, indent=1, default=str)
        return {"assets": len(r["assets"]), "meshes": {k: (v if isinstance(v, str) else {kk: v[kk] for kk in v if kk in ("lods", "verts", "morphs")})
                                                    for k, v in r["meshes"].items()}}

    def probe():
        ch = unreal.load_asset(CHARACTER)
        if ch is None:
            note("NO-CHARACTER " + CHARACTER)
            return
        rep["selections"] = [{"slot": s, "item": key_info(k)} for s, k in selections(ch)]
        rep["python_names"] = {n: hasattr(unreal, n) for n in ("HiddenFaceMapTexture", "HiddenFaceMapSettings",
                                                               "MetaHumanOutfitEditorPipeline", "MetaHumanSkeletalMeshEditorPipeline",
                                                               "MetaHumanSkeletalMeshPipeline", "MetaHumanWardrobeItemFactory",
                                                               "TextureExporterPNG")}
        wi = unreal.load_asset(GARMENT)
        rep["default_garment_map"] = map_of(wi)
        save_report()
        tex = unreal.load_asset(rep["default_garment_map"]["texture"])
        os.makedirs(os.path.join(OUT, "map"), exist_ok=True)
        rep["default_garment_map_png"] = export_png(tex, os.path.join(OUT, "map", "DG_BodyShapeA_BodyMask.png"))
        save_report()
        rep["before"] = record("before", BUILT_GAME)
        note("PROBED")

    def make_item():
        """The map as a linear texture, and the default garment's copy that carries it."""
        if not os.path.exists(MAP_PNG):
            note("NO-MAP " + MAP_PNG)
            return None
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", MAP_PNG)
        t.set_editor_property("destination_path", WARDROBE)
        t.set_editor_property("destination_name", TEX_NAME)
        t.set_editor_property("automated", True)
        t.set_editor_property("replace_existing", True)
        t.set_editor_property("save", False)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
        tex = unreal.load_asset(WARDROBE + "/" + TEX_NAME)
        if tex is None:
            note("NO-TEXTURE-IMPORTED")
            return None
        # Linear, as the engine's own maps are (MetaHumanGeometryRemoval.cpp 217-218); no mips: the build
        # reads the source's top level only (184-207).
        tex.set_editor_property("srgb", False)
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_GRAYSCALE)
        tex.set_editor_property("mip_gen_settings", unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
        unreal.EditorAssetLibrary.save_loaded_asset(tex, only_if_is_dirty=False)
        wi_path = WARDROBE + "/" + WI_NAME
        if not unreal.EditorAssetLibrary.does_asset_exist(wi_path):
            made = unreal.EditorAssetLibrary.duplicate_asset(GARMENT, wi_path)
            if made is None:
                note("NO-DUPLICATE " + GARMENT)
                return None
        wi = unreal.load_asset(wi_path)
        pl = wi.get_editor_property("pipeline")
        ep = pl.get_editor_property("editor_pipeline")
        hf, name = prop(ep, "body_hidden_face_map_texture", "BodyHiddenFaceMapTexture")
        hf.set_editor_property("texture", tex)
        s = hf.get_editor_property("settings")
        for k, v in SETTINGS.items():
            s.set_editor_property(k, v)
        hf.set_editor_property("settings", s)
        ep.set_editor_property(name, hf)
        unreal.EditorAssetLibrary.save_loaded_asset(wi, only_if_is_dirty=False)
        rep["item"] = {"path": wi_path, "map": map_of(wi), "outer_of_editor_pipeline": ep.get_outer().get_path_name()}
        save_report()
        return wi

    def open_character():
        f = None
        try:
            import make_cast_metahumans as mc
            f = mc.free_gb()
        except Exception:
            pass
        if f is not None and f < NEED_FREE_GB:
            note("REFUSED free %.1f GB under %.0f" % (f, NEED_FREE_GB))
            return False
        ch = unreal.load_asset(CHARACTER)
        if ch is None or not sub.try_add_object_to_edit(ch):
            note("NOT-EDITABLE")
            return False
        st["ch"] = ch
        st["opened"] = time.time()
        return True

    def wear(ch, wi):
        col = ch.internal_collection
        inst = col.default_instance
        before = selections(ch)
        rep["selections_before"] = [{"slot": s, "item": key_info(k)} for s, k in before]
        outfits = [k for s, k in before if s == "Outfits"]
        ours = [k for k in outfits if WI_NAME in str(k)]
        if ours:
            note("already-worn")
            return True
        keep, replaced = pick_swap(outfits)
        st["replaced"] = replaced
        got = col.try_add_item_from_wardrobe_item("Outfits", wi)
        new_key = got[-1] if isinstance(got, tuple) else got
        if keep is not None:
            inst.set_single_slot_selection("Outfits", keep)
            added = inst.try_add_slot_selection(unreal.MetaHumanPipelineSlotSelection(slot_name="Outfits", selected_item=new_key))
        else:
            inst.set_single_slot_selection("Outfits", new_key)
            added = True
        rep["swap"] = {"kept": key_info(keep) if keep is not None else None, "replaced": [key_info(k) for k in replaced],
                       "added": key_info(new_key), "added_ok": bool(added)}
        rep["selections_after"] = [{"slot": s, "item": key_info(k)} for s, k in selections(ch)]
        save_report()
        return bool(added)

    def build():
        import make_cast_metahumans as mc
        ch = st["ch"]
        if not sub.can_build_meta_human(ch, True):
            note("CANNOT-BUILD")
            return
        p = unreal.MetaHumanCharacterEditorBuildParameters()
        p.set_editor_property("pipeline_type", unreal.MetaHumanDefaultPipelineType.OPTIMIZED)
        p.set_editor_property("pipeline_quality", unreal.MetaHumanQualityLevel.HIGH)
        p.set_editor_property("absolute_build_path", BUILD_ROOT)
        tb = time.time()
        sub.build_meta_human(ch, p)
        made = unreal.EditorAssetLibrary.list_assets(BUILT, recursive=True, include_folder=False)
        mc.use_take(TAKE)
        recoloured = mc.recolour_hair(WHO, made)
        unreal.EditorAssetLibrary.save_directory(BUILT, only_if_is_dirty=False, recursive=True)
        rep["build"] = {"seconds": round(time.time() - tb, 1), "assets": len(made), "hair_recoloured": recoloured, "root": BUILD_ROOT}
        save_report()

    def finish():
        unreal.unregister_slate_post_tick_callback(st["h"])
        ch = st.get("ch")
        if ch is not None and sub.is_object_added_for_editing(ch):
            sub.remove_object_to_edit(ch)
        if ch is not None and step_name == "build" and not KEEP_CHARACTER and rep.get("swap"):
            # A SIDE BUILD PUTS THE SELECTIONS BACK (the added palette item stays, unselected) and saves, so the
            # editor never stops at a save prompt; the file itself is then put back from OUT/before (see header).
            try:
                inst = ch.internal_collection.default_instance
                kept = [k for s_, k in selections(ch) if s_ == "Outfits" and WI_NAME not in str(k)]
                if kept:
                    inst.set_single_slot_selection("Outfits", kept[0])
                    for k in st.get("replaced", []):
                        inst.try_add_slot_selection(unreal.MetaHumanPipelineSlotSelection(slot_name="Outfits", selected_item=k))
                rep["selections_reverted"] = [{"slot": s_, "item": key_info(k)} for s_, k in selections(ch)]
            except Exception as e:
                rep["revert_error"] = repr(e)
        if ch is not None and step_name == "build":
            # saved even unchanged (control), so the editor never stops at a save prompt; put back from OUT/before
            unreal.EditorAssetLibrary.save_loaded_asset(ch, only_if_is_dirty=False)
        rep["character_saved"] = bool(ch is not None and step_name == "build")
        rep["character_keeps_item"] = bool(KEEP_CHARACTER)
        rep["seconds"] = round(time.time() - st["t0"], 1)
        save_report()
        with open(log, "a", encoding="utf-8") as fh:
            fh.write("hiddenFaces step=%s seconds=%.0f notes=%s\n" % (step_name, rep["seconds"], "|".join(rep["notes"])[:300].replace(" ", "~")))
        unreal.SystemLibrary.quit_editor()

    def step():
        now = time.time()
        if st["phase"] == "wait":
            if now - st["t0"] < seconds:
                return
            if step_name == "probe":
                probe()
                st["phase"] = "quit"
            else:
                wi = None if CONTROL else make_item()
                if wi is None and not CONTROL:
                    st["phase"] = "quit"
                else:
                    st["wi"] = wi
                    st["phase"] = "settle" if open_character() else "quit"
        elif st["phase"] == "settle":
            if now - st["opened"] < settle:
                return
            if CONTROL:
                build()
                rep["control"] = record("control", BUILT)
                note("BUILT-CONTROL")
            elif wear(st["ch"], st["wi"]):
                build()
                rep["after"] = record("after", BUILT)
                rep["selections_final"] = [{"slot": s, "item": key_info(k)} for s, k in selections(st["ch"])]
                note("BUILT")
            else:
                note("NOT-WORN")
            st["phase"] = "quit"
        if st["phase"] == "quit":
            finish()

    def tick(delta):
        if st["busy"]:
            return
        st["busy"] = True
        try:
            step()
        except Exception as e:
            import traceback
            note("RAISED " + repr(e) + " " + traceback.format_exc()[-600:])
            try:
                finish()
            except Exception:
                unreal.SystemLibrary.quit_editor()
        finally:
            st["busy"] = False

    st["h"] = unreal.register_slate_post_tick_callback(tick)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    print("hidden_faces runs inside the editor; see the header")
