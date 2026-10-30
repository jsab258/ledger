"""A cloud shopfront's painted joinery into Unreal in the kit's paint-over-wood material (his order D11, the chandler's
S2; production/research/street-wear/MAFIA-WEAR-2026-10-28.md, section 5).

    UnrealEditor-Cmd ue-probe/LedgerProbe.uproject -run=pythonscript -script=C:/Users/Jafar/ledger-local/tools/ue/import_front_joinery.py
    python tools/ue/import_front_joinery.py --selftest    # runs without Unreal

WHY, 30 October 2026. tools/art-recipes/front_joinery.py writes the front with its trim UV set and its edge pictures
(production/specs/shop-fronts/<name>-joinery.json, its numbers in <out>-made.json); tools/art-recipes/wood_trim.py the
wood. This imports them and puts the paint over wood on the paints the spec names, nothing else:
  * the trim sheet's three maps and each paint's edge picture as textures under /Game/Ledger/Kit/Joinery (each with the
    compression its sampler reads: colour sRGB, masks as masks, normals as normals, the edges linear);
  * M_LedgerKitPaintWood (tools/ue/make_kit_materials.py make_paint_wood_master), rebuilt in place;
  * the front's glb as /Game/Ledger/ShopFronts/<out>/SM_<out> by the shop fronts' own step (tools/ue/import_vehicles.py
    import_glb), unless the chain's import_shop_displays.py has just done it (main(import_mesh=False));
  * one instance a paint, MI_Joinery_<out>_<slot> under /Game/Ledger/Kit/Joinery, holding the slot's own glTF paint
    pictures and factors (read from the material the import gave the slot) and the layer's numbers from the made file,
    set on the mesh's slot and saved with it. A mesh slot the spec does not name keeps the import's material.
ONE LINE, appended to ue-material.txt: frontJoinery=MADE or INCOMPLETE, with what was asked and made, the mesh's UV sets,
and the material's pixel-shader instruction count (0 means it did not compile).
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC_DIR = os.path.join(REPO, "production", "specs", "shop-fronts")
GAME_INPUTS = os.environ.get("LEDGER_GAME_INPUTS", r"F:\LedgerTools\game-inputs")
FRONTS_REL = "production/assets/shop-fronts"
TRIM_REL = "production/assets/wood-trim"
FRONTS_ROOT = "/Game/Ledger/ShopFronts"
JOINERY = "/Game/Ledger/Kit/Joinery"
SPECS = ("chandler-front-joinery.json",)
#: the trim sheet's maps: (file, asset, sRGB, compression)
TRIM = (("wood_trim_colour.png", "T_WoodTrim_Colour", True, "TC_DEFAULT"),
        ("wood_trim_masks.png", "T_WoodTrim_Masks", False, "TC_MASKS"),
        ("wood_trim_normal.png", "T_WoodTrim_Normal", False, "TC_NORMALMAP"),
        ("wood_trim_flatnormal.png", "T_WoodTrim_FlatNormal", False, "TC_NORMALMAP"))
#: the glTF import's parameter names (Interchange's glTF material instances) and ours
GLTF_TEXTURES = (("BaseColorTexture", "PaintMap"), ("MetallicRoughnessTexture", "PaintORM"), ("NormalTexture", "PaintNormal"))
#: and the glTF master's specular: its SpecularFactor drives Unreal's Specular one for one (measured 30 October in the lit
#: view at the chandler, the navy's luminance: the glTF paint 0.0411; ours at Specular 1.0 0.0408, at 0.5 0.021, at 0 0.009;
#: base colour and roughness equal throughout), so a dark paint's sheen, most of its light by day, is kept
GLTF_SCALARS = (("RoughnessFactor", "RoughnessFactor"), ("MetallicFactor", "MetallicFactor"), ("SpecularFactor", "Specular"))
LAYER_SCALARS = ("ChipAmount", "WornWidth", "ChipSharpness", "WoodMaskEdge", "PaintCracksTiling", "PaintFadeIntensity",
                 "WeatheringOpacity", "WeatheringRoughnessAdd", "DirtMaskIntensity", "DirtRoughness", "DirtOpacity",
                 "DirtDarken")


def pick(*paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None


def instance_name(out, slot):
    return "MI_Joinery_%s_%s" % (out.replace("-", "_"), slot.replace(".", "_"))


def instance_values(spec, made, slot):
    """The scalars and vectors one slot's instance takes: the layer's (ChipAmount from the made file) and, for a box
    paint, its box and weight."""
    layer = dict(spec["layer"])
    layer["ChipAmount"] = made["layer"]["ChipAmount"]
    s = {k: float(layer[k]) for k in LAYER_SCALARS}
    v = {}
    s["EdgeCm"] = float(spec["edge_m"]) * 100.0
    s["EdgeLawGain"] = 1.0 if spec.get("edge_law", "gain") == "gain" else 0.0
    s["ClusterFrom"], s["ClusterGain"] = float(spec["cluster"]["from"]), float(spec["cluster"]["gain"])
    row = made["paints"][slot]
    if spec["paints"][slot]["edges"] == "box":
        s["EdgeFromBox"] = 1.0
        s["BoxWeight"] = float(row["box_weight"])
        v["BoxMin"], v["BoxMax"] = tuple(row["box_cm"]["min"]), tuple(row["box_cm"]["max"])
    else:
        s["EdgeFromBox"] = 0.0
    return s, v


def _import_png(unreal, png, dest_dir, name, srgb, compression):
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", png)
    task.set_editor_property("destination_path", dest_dir)
    task.set_editor_property("destination_name", name)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", False)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    path = dest_dir + "/" + name
    tex = unreal.EditorAssetLibrary.load_asset(path)
    if tex is None:
        return None
    set_kind(unreal, tex, srgb, compression)
    unreal.EditorAssetLibrary.save_asset(path)
    return tex


def set_kind(unreal, tex, srgb, compression):
    try:
        tex.set_editor_property("srgb", srgb)
        tex.set_editor_property("compression_settings", getattr(unreal.TextureCompressionSettings, compression))
    except Exception:
        pass


def main(import_mesh=True):
    import unreal
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import make_kit_materials as mkm
    lib = unreal.EditorAssetLibrary
    mel = unreal.MaterialEditingLibrary
    notes, asked, made_n = [], 0, 0
    lines = []
    trim = {}
    for fname, asset, srgb, comp in TRIM:
        asked += 1
        png = pick(os.path.join(REPO, TRIM_REL, fname), os.path.join(GAME_INPUTS, TRIM_REL, fname))
        t = _import_png(unreal, png, mkm.JOINERY_PACKAGE, asset, srgb, comp) if png else None
        trim[asset] = t
        made_n += t is not None
        if t is None:
            notes.append("no-" + asset)
    for spec_name in SPECS:
        spec = json.load(open(os.path.join(SPEC_DIR, spec_name), encoding="utf-8"))
        made = json.load(open(os.path.join(SPEC_DIR, spec["out"] + "-made.json"), encoding="utf-8"))
        out = spec["out"]
        edges = {}
        for slot, row in made["paints"].items():
            if "edges_png" not in row:
                continue
            asked += 1
            png = pick(os.path.join(GAME_INPUTS, FRONTS_REL, row["edges_png"]))
            t = _import_png(unreal, png, mkm.JOINERY_PACKAGE, "T_JoineryEdges_%s_%s" % (out.replace("-", "_"), slot),
                            False, "TC_DEFAULT") if png else None
            edges[slot] = t
            made_n += t is not None
        # THE MASTER, its own-kind defaults from the joinery's textures
        any_edge = next((t for t in edges.values() if t is not None), None)
        master, w, a, mnotes = mkm.make_paint_wood_master(unreal, {
            "PaintORM": any_edge, "EdgeMask": any_edge, "PaintNormal": trim.get("T_WoodTrim_FlatNormal"),
            "WoodColour": trim.get("T_WoodTrim_Colour"), "WoodMasks": trim.get("T_WoodTrim_Masks"),
            "WoodNormal": trim.get("T_WoodTrim_Normal")})
        notes += mnotes[:6]
        asked += 1
        made_n += master is not None and w == a
        instr = 0
        try:
            st = mel.get_statistics(master)
            instr = int(st.get_editor_property("num_pixel_shader_instructions"))
        except Exception as err:
            notes.append("stats=%s" % str(err).split("\n")[0][:40])
        # THE MESH
        mesh_path = "%s/%s/SM_%s" % (FRONTS_ROOT, out, out)
        if import_mesh:
            import import_vehicles
            glb = os.path.join(GAME_INPUTS, FRONTS_REL, out + ".glb")
            m_ok, off, note = import_vehicles.import_glb(unreal, glb, "%s/%s" % (FRONTS_ROOT, out), mesh_path)
            if note:
                notes.append(note)
        mesh = lib.load_asset(mesh_path)
        if mesh is None:
            notes.append("no-mesh-" + out)
            lines.append("%s mesh=MISSING" % out)
            continue
        uvs, lm = 0, "?"

        def uv_sets():
            # the subsystem where there is one; in a commandlet only the old library answers, and it may answer 0
            sub = unreal.get_editor_subsystem(unreal.StaticMeshEditorSubsystem)
            if sub is not None:
                return int(sub.get_num_uv_channels(mesh, 0))
            return int(unreal.EditorStaticMeshLibrary.get_num_uv_channels(mesh, 0))
        try:
            uvs = uv_sets()
        except Exception as err:
            notes.append("uvs=%s" % str(err).split("\n")[0][:30])
        # THE GENERATED LIGHTMAP KEPT OFF THE TRIM'S UV SET: the front is movable (no baked light); its lightmap goes
        # where the import put it (30 October: UV 1, and this setting did not stick in a commandlet), which
        # front_joinery.py leaves to it as a copy of UV 0, the trim on UV 2
        try:
            bs = unreal.EditorStaticMeshLibrary.get_lod_build_settings(mesh, 0)
            on = bs.get_editor_property("generate_lightmap_u_vs")
            dst = int(bs.get_editor_property("dst_lightmap_index"))
            lm = "%s@%d" % ("on" if on else "off", dst)
            if on and dst == 2:
                notes.append("lightmap-over-the-trim-uv-%s" % out)
        except Exception as err:
            notes.append("lightmap=%s" % str(err).split("\n")[0][:30])
        mats = list(mesh.get_editor_property("static_materials"))
        done = []
        for i, sm in enumerate(mats):
            slot = str(sm.get_editor_property("material_slot_name"))
            if slot not in spec["paints"]:
                continue
            asked += 1
            base = sm.get_editor_property("material_interface")
            name = instance_name(out, slot)
            mpath = mkm.JOINERY_PACKAGE + "/" + name
            mi = lib.load_asset(mpath) if lib.does_asset_exist(mpath) else None
            if mi is not None:
                mel.clear_all_material_instance_parameters(mi)
            else:
                mi = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
                    name, mkm.JOINERY_PACKAGE, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
            if mi is None:
                notes.append("no-instance-" + slot)
                continue
            mel.set_material_instance_parent(mi, master)
            got = []
            for gname, ours in GLTF_TEXTURES:
                t = None
                try:
                    t = mel.get_material_instance_texture_parameter_value(base, gname)
                except Exception:
                    t = None
                if t is not None:
                    # the paint's own pictures read as our samplers read them (the import's own copies, this mesh's)
                    if ours == "PaintORM":
                        set_kind(unreal, t, False, "TC_DEFAULT")
                        lib.save_loaded_asset(t)
                    mel.set_material_instance_texture_parameter_value(mi, ours, t)
                    got.append(ours)
            for gname, ours in GLTF_SCALARS:
                try:
                    v = mel.get_material_instance_scalar_parameter_value(base, gname)
                    mel.set_material_instance_scalar_parameter_value(mi, ours, float(v))
                except Exception:
                    pass
            try:
                c = mel.get_material_instance_vector_parameter_value(base, "BaseColorFactor")
                mel.set_material_instance_vector_parameter_value(mi, "BaseColorFactor", c)
            except Exception:
                pass
            s, v = instance_values(spec, made, slot)
            for k, val in s.items():
                mel.set_material_instance_scalar_parameter_value(mi, k, val)
            for k, val in v.items():
                mel.set_material_instance_vector_parameter_value(mi, k, unreal.LinearColor(val[0], val[1], val[2], 1.0))
            for k, t in (("WoodColour", trim.get("T_WoodTrim_Colour")), ("WoodMasks", trim.get("T_WoodTrim_Masks")),
                         ("WoodNormal", trim.get("T_WoodTrim_Normal")), ("EdgeMask", edges.get(slot))):
                if t is not None:
                    mel.set_material_instance_texture_parameter_value(mi, k, t)
            lib.save_asset(mpath)
            mesh.set_material(i, mi)
            done.append("%s(%s)" % (slot, "+".join(got) or "no-paint-pictures"))
            made_n += "PaintMap" in got
            if "PaintMap" not in got:
                notes.append("no-paint-map-%s" % slot)
        lib.save_loaded_asset(mesh, only_if_is_dirty=False)
        lines.append("%s uvSets=%d lightmap=%s slots=%s" % (out, uvs, lm, ",".join(done)))
        # 0 is "not answered" (the commandlet's library, 30 October; the build's own log line read "UVs 2"), 1 a fault
        if uvs == 1:
            notes.append("one-uv-set-%s" % out)
    ok = made_n == asked and not any(x.startswith(("no-", "one-uv")) for x in notes)
    line = ("frontJoinery=%s asked=%d made=%d masterInstructions=%d %s notes=%s" % (
        "MADE" if ok else "INCOMPLETE", asked, made_n, instr, " ".join(lines), ("/".join(notes) or "none").replace(" ", "~")[:400]))
    try:
        with open(os.path.join(unreal.Paths.project_dir(), "ue-material.txt"), "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass
    print("import_front_joinery: " + line)
    return 0 if ok else 2


def selftest():
    ok = []
    spec = json.load(open(os.path.join(SPEC_DIR, SPECS[0]), encoding="utf-8"))
    made_p = os.path.join(SPEC_DIR, spec["out"] + "-made.json")
    ok.append(instance_name("chandler-front-joinery", "brass.001") == "MI_Joinery_chandler_front_joinery_brass_001")
    if os.path.exists(made_p):
        made = json.load(open(made_p, encoding="utf-8"))
        s, v = instance_values(spec, made, "fascia_chandler")
        ok.append(s["EdgeFromBox"] == 1.0 and len(v["BoxMin"]) == 3 and s["EdgeCm"] == 5.0)
        s2, v2 = instance_values(spec, made, "paint_navy")
        ok.append(s2["EdgeFromBox"] == 0.0 and not v2 and 0.0 < s2["ChipAmount"] <= 1.0)
        ok.append(all(k in s2 for k in LAYER_SCALARS))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import make_kit_materials as mkm
    names = {n for n, _ in mkm.PAINT_WOOD_SCALARS}
    ok.append(set(LAYER_SCALARS) <= names and {"EdgeFromBox", "EdgeCm", "BoxWeight", "ClusterFrom", "ClusterGain"} <= names)
    ok.append({ours for _, ours in GLTF_TEXTURES} <= {n for n, _, _, _ in mkm.PAINT_WOOD_TEXTURES})
    print("import_front_joinery selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


def _inside_unreal():
    try:
        import unreal  # noqa: F401
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if "--selftest" in sys.argv or not _inside_unreal():
        sys.exit(selftest())
    main()
