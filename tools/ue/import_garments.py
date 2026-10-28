"""The clothing session's garments onto the cast, in the MetaHuman project.

    set LEDGER_MH_SCRIPT=import_garments
    UnrealEditor.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -unattended
    python tools/ue/import_garments.py --selftest        # the list, without Unreal

WHY, 30 September. The clothing session (CLAUDE.md, three sessions) makes
each garment in Blender on the body the builder exported, skinned to that
body's own bones, and hands it over (NOW.md, Handovers); the builder fits
it in Unreal. production/specs/garments.json lists them. Each skinned FBX
becomes a skeletal mesh on its wearer's body skeleton, keeping the weights
it came with (the boots' README: re-transferring them would send the toe
box to the toe bones), at /Game/Ledger/MetaHumans/Garments/<Name>/SKM_<Name>.
That folder sits with the cast's MetaHumans, outside the public repository,
and the build machine mirrors it with them (ledger-probe-unreal.yml). The
game wears each by following the body's pose (LedgerGarments.h).

Writes import-garments.txt beside the project: each asset, its skeleton,
its size and its material slots.

LEDGER_GARMENTS=RonJacket,... imports only those. A garment's "materials"
maps its FBX slot names to material instances already in the project (the
bound jacket takes the donkey jacket's wool, yoke and buttons), set on the
mesh after the import.
"""
import json
import os
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(REPO, "production", "specs", "garments.json")
DEST = "/Game/Ledger/MetaHumans/Garments"
# Each wearer's approved MetaHuman, whose body the garments were made on
# (the face take changes the face, never the body: F:/LedgerTools/bodies/README.md).
BODY = {"Rocco": "MH_RoccoP2", "Lena": "MH_LenaS4", "Sam": "MH_SamC5",
        # Tom (28 October 2026, his page: his zip jacket worn in the game with drape 19's cuffs): his MetaHuman L1,
        # worn over Epic's sample character (SliceCharacter.cpp), the body the jacket was draped and skinned on
        "Tom": "MH_TomL1"}


# A GARMENT BAKED TO THREE MAPS (28 October 2026, Tom's zip jacket; BAKE-PLAN-2026-10-27.md, "Next: into the game"):
# "maps" names a colour map (neutral greys with occlusion in alpha), a normal map (DirectX) and a packed map (roughness
# R, the part's ID in G, metal B); one material over every slot, the cloth and rib tinted, the tape and the teeth
# their own colours by the ID (cloth 0, rib 0.25, tape 0.5, teeth 0.75, welt 1)
PACKED_BASE = DEST + "/M_LedgerGarmentPacked"


def packed_material(unreal, g, folder, lines):
    mel = unreal.MaterialEditingLibrary
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    maps = g["maps"]

    def texture(png, name, kind):
        task = unreal.AssetImportTask()
        for k, v in (("filename", png), ("destination_path", folder), ("destination_name", name),
                     ("automated", True), ("replace_existing", True), ("save", True)):
            task.set_editor_property(k, v)
        tools.import_asset_tasks([task])
        t = unreal.load_asset(folder + "/" + name)
        if t is None:
            lines.append("  MISSING texture %s from %s" % (name, png))
            return None
        if kind == "normal":
            t.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
            t.set_editor_property("srgb", False)
        elif kind == "packed":
            t.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
            t.set_editor_property("srgb", False)
        unreal.EditorAssetLibrary.save_loaded_asset(t, only_if_is_dirty=False)
        return t

    colour = texture(maps["colour"], "T_%s_ColourAO" % g["name"], "colour")
    normal = texture(maps["normal"], "T_%s_Normal" % g["name"], "normal")
    packed = texture(maps["packed"], "T_%s_Packed" % g["name"], "packed")
    if not (colour and normal and packed):
        return None
    # THE GRAPH BUILT AFRESH EVERY RUN (28 October: a broken first graph stayed, since a found material was kept as it was)
    if unreal.EditorAssetLibrary.does_asset_exist(PACKED_BASE):
        base = unreal.load_asset(PACKED_BASE)
        mel.delete_all_material_expressions(base)
    else:
        base = tools.create_asset("M_LedgerGarmentPacked", DEST, unreal.Material, unreal.MaterialFactoryNew())

    def node(cls, x, y, **props):
        e = mel.create_material_expression(base, cls, x, y)
        for k, v in props.items():
            e.set_editor_property(k, v)
        return e

    c = node(unreal.MaterialExpressionTextureSampleParameter2D, -1400, -300, parameter_name="ColourMap", texture=colour)
    p = node(unreal.MaterialExpressionTextureSampleParameter2D, -1400, 100, parameter_name="PackedMap", texture=packed,
             sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_MASKS)
    n = node(unreal.MaterialExpressionTextureSampleParameter2D, -1400, 500, parameter_name="NormalMap", texture=normal,
             sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL)
    tint = node(unreal.MaterialExpressionVectorParameter, -1000, -500, parameter_name="Tint")
    tape = node(unreal.MaterialExpressionVectorParameter, -1000, -350, parameter_name="TapeColour")
    teeth = node(unreal.MaterialExpressionVectorParameter, -600, -500, parameter_name="TeethColour")
    cloth = node(unreal.MaterialExpressionMultiply, -800, -450)
    mel.connect_material_expressions(tint, "", cloth, "A")
    mel.connect_material_expressions(c, "RGB", cloth, "B")
    tapec = node(unreal.MaterialExpressionMultiply, -800, -300)
    mel.connect_material_expressions(tape, "", tapec, "A")
    mel.connect_material_expressions(c, "RGB", tapec, "B")

    def is_part(value, y):
        # 1 where the ID is this part's value, 0 an eighth away: saturate(1 - |G - value| * 8)
        s = node(unreal.MaterialExpressionSubtract, -1000, y, const_b=value)
        mel.connect_material_expressions(p, "G", s, "A")
        a = node(unreal.MaterialExpressionAbs, -900, y)
        mel.connect_material_expressions(s, "", a, "")
        m = node(unreal.MaterialExpressionMultiply, -800, y, const_b=8.0)
        mel.connect_material_expressions(a, "", m, "A")
        o = node(unreal.MaterialExpressionOneMinus, -700, y)
        mel.connect_material_expressions(m, "", o, "")
        sat = node(unreal.MaterialExpressionSaturate, -600, y)
        # one-input nodes (Abs, OneMinus, Saturate) join by an unnamed pin (28 October: connected as "Input", nothing joined, and the cook failed
        # the material: "Missing Saturate input")
        mel.connect_material_expressions(o, "", sat, "")
        return sat

    on_tape, on_teeth = is_part(0.5, -100), is_part(0.75, 0)
    l1 = node(unreal.MaterialExpressionLinearInterpolate, -400, -350)
    mel.connect_material_expressions(cloth, "", l1, "A")
    mel.connect_material_expressions(tapec, "", l1, "B")
    mel.connect_material_expressions(on_tape, "", l1, "Alpha")
    l2 = node(unreal.MaterialExpressionLinearInterpolate, -250, -350)
    mel.connect_material_expressions(l1, "", l2, "A")
    mel.connect_material_expressions(teeth, "", l2, "B")
    mel.connect_material_expressions(on_teeth, "", l2, "Alpha")
    mel.connect_material_property(l2, "", unreal.MaterialProperty.MP_BASE_COLOR)
    mel.connect_material_property(p, "R", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.connect_material_property(p, "B", unreal.MaterialProperty.MP_METALLIC)
    mel.connect_material_property(c, "A", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
    mel.connect_material_property(n, "RGB", unreal.MaterialProperty.MP_NORMAL)
    base.set_editor_property("used_with_skeletal_mesh", True)
    mel.recompile_material(base)
    unreal.EditorAssetLibrary.save_loaded_asset(base, only_if_is_dirty=False)
    mi_name = "MI_" + g["name"]
    path = folder + "/" + mi_name
    mi = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else tools.create_asset(
        mi_name, folder, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi, base)
    mel.set_material_instance_texture_parameter_value(mi, "ColourMap", colour)
    mel.set_material_instance_texture_parameter_value(mi, "PackedMap", packed)
    mel.set_material_instance_texture_parameter_value(mi, "NormalMap", normal)
    for k in ("Tint", "TapeColour", "TeethColour"):
        r, gr, b = maps[k.lower()]
        mel.set_material_instance_vector_parameter_value(mi, k, unreal.LinearColor(r, gr, b, 1.0))
    unreal.EditorAssetLibrary.save_loaded_asset(mi, only_if_is_dirty=False)
    lines.append("  material %s on %s: tint %s, tape %s, teeth %s" % (mi_name, PACKED_BASE, maps["tint"], maps["tapecolour"], maps["teethcolour"]))
    return mi


def garments(path=SPEC):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)["garments"]


def selftest():
    failed = 0
    g = garments()
    checks = [
        ("the list names garments", len(g) >= 1, str(len(g))),
        ("every wearer has an approved body", all(x["who"] in BODY for x in g), str([x["who"] for x in g])),
        ("every name is one word", all(x["name"].isalnum() for x in g), ""),
        ("every garment's file is where it says", all(os.path.isfile(x["fbx"]) for x in g) or not os.path.isdir("F:/LedgerTools"),
         str([x["fbx"] for x in g if not os.path.isfile(x["fbx"])])),
        # 3 October: Ron's shirt front and tie, made for the jacket's test films, said "held" in
        # its own words but carried no hold, so the game wore it and his chest was a hole.
        ("a garment its own words call held carries a hold",
         all("hold" in x for x in g if "held" in x.get("made", "") or "worn only" in x.get("made", "")),
         str([x["name"] for x in g if ("held" in x.get("made", "") or "worn only" in x.get("made", "")) and "hold" not in x])),
        ("nothing the game wears lives in a scratch folder (tmp is cleared after seven days)",
         all("hold" in x for x in g if "/tmp/" in x["fbx"].replace("\\", "/").lower()),
         str([x["name"] for x in g if "/tmp/" in x["fbx"].replace("\\", "/").lower() and "hold" not in x])),
    ]
    for name, ok, detail in checks:
        if not ok:
            failed += 1
            print("import_garments selftest FAIL %s: %s" % (name, detail))
    print("import_garments selftest: passed=%d/%d failed=%d" % (len(checks) - failed, len(checks), failed))
    return 1 if failed else 0


def main_after_idle(seconds=20.0):
    import unreal
    st = {"t0": time.time(), "h": None, "done": False}
    out = os.path.join(unreal.Paths.project_dir(), "import-garments.txt")

    def body_skeleton(who):
        mh = BODY[who]
        mesh = unreal.load_asset("/Game/Ledger/MetaHumans/%s/Body/SKM_%s_BodyMesh" % (mh, mh))
        return mesh.get_editor_property("skeleton") if mesh else None

    def one(g, lines):
        name = "SKM_" + g["name"]
        folder = DEST + "/" + g["name"]
        skel = body_skeleton(g["who"])
        ui = unreal.FbxImportUI()
        ui.set_editor_property("import_mesh", True)
        ui.set_editor_property("import_as_skeletal", True)
        ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_SKELETAL_MESH)
        ui.set_editor_property("import_materials", True)
        ui.set_editor_property("import_textures", False)
        ui.set_editor_property("import_animations", False)
        ui.set_editor_property("create_physics_asset", False)
        if skel is not None:
            ui.set_editor_property("skeleton", skel)
        sk = ui.get_editor_property("skeletal_mesh_import_data")
        sk.set_editor_property("import_morph_targets", False)
        sk.set_editor_property("convert_scene", True)
        task = unreal.AssetImportTask()
        task.set_editor_property("filename", g["fbx"])
        task.set_editor_property("destination_path", folder)
        task.set_editor_property("destination_name", name)
        task.set_editor_property("automated", True)
        task.set_editor_property("replace_existing", True)
        task.set_editor_property("save", True)
        task.set_editor_property("options", ui)
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
        mesh = unreal.load_asset(folder + "/" + name)
        if mesh is None:
            lines.append("MISSING %s/%s (from %s)" % (folder, name, g["fbx"]))
            return
        b = mesh.get_bounds()
        lines.append("%s: %s/%s" % (g["who"], folder, name))
        lines.append("  on the skeleton %s (the body's: %s)" % (
            mesh.get_editor_property("skeleton").get_path_name() if mesh.get_editor_property("skeleton") else "none",
            skel.get_path_name() if skel else "none"))
        lines.append("  size cm %s, centre %s" % ([round(2 * x, 1) for x in (b.box_extent.x, b.box_extent.y, b.box_extent.z)],
                                                 [round(x, 1) for x in (b.origin.x, b.origin.y, b.origin.z)]))
        lines.append("  material slots: %s" % [str(m.get_editor_property("material_slot_name")) for m in mesh.get_editor_property("materials")])
        if "maps" in g:
            mi = packed_material(unreal, g, folder, lines)
            if mi is not None:
                slots = list(mesh.get_editor_property("materials"))
                for i, s in enumerate(slots):
                    s.set_editor_property("material_interface", mi)
                    slots[i] = s
                mesh.set_editor_property("materials", slots)
                lines.append("  every slot set to %s" % mi.get_name())
        mats = g.get("materials", {})
        if mats:
            slots = list(mesh.get_editor_property("materials"))
            for i, s in enumerate(slots):
                want = mats.get(str(s.get_editor_property("material_slot_name")))
                mi = unreal.load_asset(want) if want else None
                if mi is not None:
                    s.set_editor_property("material_interface", mi)
                    slots[i] = s
            mesh.set_editor_property("materials", slots)
            lines.append("  materials set: %s" % [str(s.get_editor_property("material_interface").get_name()) if s.get_editor_property("material_interface") else "none" for s in slots])
        unreal.EditorAssetLibrary.save_directory(folder)

    def run():
        lines = []
        only = [x for x in os.environ.get("LEDGER_GARMENTS", "").split(",") if x]
        for g in garments():
            if only and g["name"] not in only:
                continue
            try:
                one(g, lines)
            except Exception as e:
                lines.append("%s RAISED %r" % (g["name"], e))
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


if __name__ == "__main__" and "--selftest" in sys.argv:
    sys.exit(selftest())
