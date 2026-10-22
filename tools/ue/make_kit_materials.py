"""The kit's shared master materials and one instance per kind and per slot, from a script.

    UnrealEditor-Cmd ue-probe/LedgerProbe.uproject -run=pythonscript -script=tools/ue/make_kit_materials.py
    python tools/ue/make_kit_materials.py --selftest     # runs without Unreal
    python tools/ue/make_kit_materials.py --list         # the slots and their starting values

WHY, 21 October 2026 (his order, item 5): "shared Unreal master materials made once from the
material slot names (paint, cast iron, glass, brick, concrete, granite, enamel, galvanised steel),
with the base values in the targets as starting points only; the look is made in Unreal against
the Hook sheet." The cloud's kit pieces (production/assets/cloud-week) name every material slot by
what it is; the held-props route used to give a prop one street surface in slot 0 and leave the
rest to the glTF importer. Kit pieces keep their slots instead, each wearing the instance named
for it here.

WHAT IT MAKES, under /Game/Ledger/Kit:
  M_LedgerKit       opaque: BaseColor, Roughness, Metallic, Specular, EmissiveColor
  M_LedgerKitGlass  translucent, lit per pixel on its surface: the same and Opacity
  MI_KitKind_<kind> one per kind in production/specs/kit-materials.json, parented to its master
  MI_Kit_<slot>     one per slot named there, parented to its kind, starting at the values the
                    first kit model with that slot carries (glTF baseColorFactor, roughness,
                    metallic); the slot's "overrides" there, if any, win.
EmissiveColor is black in every instance: the game drives the lamp slots' glow (VignetteShot.cpp).

The kit models it reads: the file's "pieces", each ledger/Assets/Props/base-mesh/<piece>.glb
(joined copies of the cloud's, as the street places them, by tools/art-recipes/kit_for_game.py). One line appended to ue-material.txt.
"""
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(REPO, "production", "specs", "kit-materials.json")
KIT_DIR = os.path.join(REPO, "ledger", "Assets", "Props", "base-mesh")
PACKAGE = "/Game/Ledger/Kit"
MASTERS = {"opaque": "M_LedgerKit", "translucent": "M_LedgerKitGlass"}
PARAMS = ("BaseColor", "Roughness", "Metallic", "Specular", "EmissiveColor", "Opacity", "DetailSize",
          "DetailIntensity", "RoughDetail", "DirtHeight", "DirtStrength", "DirtColour", "StreakSize", "StreakLength",
          "StreakStrength", "StreakColour", "TopStrength", "TopColour", "StreakFall", "StainStrength")


def load_spec(path=SPEC):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def glb_materials(path):
    """{slot name: (r, g, b linear, roughness, metallic)} from a glb's own material table."""
    with open(path, "rb") as f:
        b = f.read()
    if b[:4] != b"glTF":
        return {}
    n = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + n].decode("utf-8"))
    out = {}
    for m in j.get("materials", []):
        pbr = m.get("pbrMetallicRoughness", {})
        c = pbr.get("baseColorFactor", [0.5, 0.5, 0.5, 1.0])
        out[m.get("name", "")] = (float(c[0]), float(c[1]), float(c[2]),
                                  float(pbr.get("roughnessFactor", 1.0)), float(pbr.get("metallicFactor", 0.0)))
    return out


def slot_values(spec, kit_dir=KIT_DIR):
    """Each named slot's starting values, from the first kit piece carrying it (the file's
    "pieces", sorted by name), then the slot's overrides. Slots no piece carries are reported,
    not invented."""
    found = {}
    for p in sorted(os.path.join(kit_dir, name + ".glb") for name in spec.get("pieces", [])):
        if not os.path.exists(p):
            continue
        for name, v in glb_materials(p).items():
            found.setdefault(name, (v, os.path.basename(p)))
    out, missing = {}, []
    for slot, row in spec["slots"].items():
        if slot not in found:
            missing.append(slot)
            continue
        (r, g, b_, rough, metal), src = found[slot]
        kind = spec["kinds"][row["kind"]]
        v = {"BaseColor": (r, g, b_), "Roughness": rough, "Metallic": metal, "Specular": 0.5,
             "Opacity": kind.get("opacity", 1.0)}
        v.update(row.get("overrides", {}))
        out[slot] = {"kind": row["kind"], "master": kind["master"], "from": src, "values": v}
    return out, missing


def _write(line):
    try:
        import unreal
        root = unreal.Paths.project_dir()
    except Exception:
        root = REPO
    try:
        with open(os.path.join(root, "ue-material.txt"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line)


WORLD_ALIGNED = "/Engine/Functions/Engine_MaterialFunctions01/Texturing/WorldAlignedTexture.WorldAlignedTexture"
DETAIL_DIR = os.environ.get("LEDGER_KIT_DETAIL", "F:/LedgerTools/game-inputs/production/assets/kit-detail")
NEUTRAL_TEX = "/Engine/EngineResources/WhiteSquareTexture.WhiteSquareTexture"
# THE DETAIL AND THE DIRT (21 October 2026, production/research/aaa-street/KIT-MATERIALS-2026-10-21.md):
# a world-aligned detail map (R: luminance high-passed to 0.5, G: roughness likewise, B: broad grunge)
# multiplies the authored colour by lerp(1, 2 x R, DetailIntensity), so the slot's colour stays in
# charge; a dirt band darkens the piece's foot, DirtHeight cm up from its own lowest point, its edge
# broken by the grunge. Every scalar defaults to off, so a kind without them is the flat colour.
SCALARS = (("Roughness", 0.6), ("Metallic", 0.0), ("Specular", 0.5), ("DetailSize", 60.0),
           ("StreakSize", 30.0), ("StreakLength", 200.0), ("StreakStrength", 0.0), ("TopStrength", 0.0),
           ("StreakFall", 250.0), ("StainStrength", 0.0),
           ("DetailIntensity", 0.0), ("RoughDetail", 0.0), ("DirtHeight", 50.0), ("DirtStrength", 0.0))
VECTORS = (("BaseColor", (0.5, 0.5, 0.5)), ("EmissiveColor", (0.0, 0.0, 0.0)), ("DirtColour", (0.45, 0.42, 0.38)),
           ("StreakColour", (0.6, 0.58, 0.55)), ("TopColour", (0.6, 0.68, 0.5)))
# THE WEATHER (21 October 2026, his ruling: the lamp columns "weathered and a shade darker"): rain
# streaks, a drawn map of vertical runs stretched StreakLength cm tall on vertical faces only,
# multiply the colour toward StreakColour; growth on faces turned to the sky (the vertex normal's
# up part, broken by the detail's grunge) toward TopColour. Both off at 0.


def _make_master(unreal, name, translucent):
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    path = PACKAGE + "/" + name
    # REBUILT IN PLACE, never deleted (21 October, measured): once the instances and the lamp's
    # mesh refer to a master, delete_asset refuses it and create_asset then fails unattended.
    mat = unreal.EditorAssetLibrary.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else None
    if mat is not None:
        mel.delete_all_material_expressions(mat)
    else:
        mat = tools.create_asset(name, PACKAGE, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        return None, 0, 0
    if translucent:
        mat.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
        mat.set_editor_property("translucency_lighting_mode", unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
    n = {"made": 0, "asked": 0, "notes": []}

    def ex(cls, x, y, **props):
        e = mel.create_material_expression(mat, cls, x, y)
        for k, v in props.items():
            try:
                e.set_editor_property(k, v)
            except Exception as err:
                n["notes"].append("%s.%s=%s" % (cls.__name__, k, str(err).split("\n")[0][:40]))
        return e

    def link(a, ao, b, bi):
        n["asked"] += 1
        try:
            if mel.connect_material_expressions(a, ao, b, bi):
                n["made"] += 1
                return
        except Exception:
            pass
        n["notes"].append("link-%s-%s" % (ao or "out", bi or "in"))

    def prop(a, ao, mp):
        n["asked"] += 1
        try:
            if mel.connect_material_property(a, ao, mp):
                n["made"] += 1
                return
        except Exception:
            pass
        n["notes"].append("prop-%s" % mp)

    P = {}
    y = 0
    for pname, default in SCALARS:
        P[pname] = ex(unreal.MaterialExpressionScalarParameter, -2200, y, parameter_name=pname, default_value=default)
        y += 110
    for pname, default in VECTORS:
        P[pname] = ex(unreal.MaterialExpressionVectorParameter, -2200, y,
                      parameter_name=pname, default_value=unreal.LinearColor(default[0], default[1], default[2], 1.0))
        y += 160
    MP = unreal.MaterialProperty
    if translucent:
        op = ex(unreal.MaterialExpressionScalarParameter, -400, 900, parameter_name="Opacity", default_value=0.35)
        prop(op, "", MP.MP_OPACITY)
        prop(P["BaseColor"], "", MP.MP_BASE_COLOR)
        prop(P["Roughness"], "", MP.MP_ROUGHNESS)
    else:
        neutral = unreal.load_asset(NEUTRAL_TEX)
        tex = ex(unreal.MaterialExpressionTextureObjectParameter, -2000, -400, parameter_name="DetailMap")
        if neutral is not None:
            tex.set_editor_property("texture", neutral)
        wa = ex(unreal.MaterialExpressionMaterialFunctionCall, -1750, -400)
        fn = unreal.load_asset(WORLD_ALIGNED)
        try:
            wa.set_editor_property("material_function", fn)
        except Exception as err:
            n["notes"].append("worldaligned=%s" % str(err).split("\n")[0][:40])
        link(tex, "", wa, "TextureObject")
        link(P["DetailSize"], "", wa, "TextureSize")
        mr = ex(unreal.MaterialExpressionComponentMask, -1500, -460, r=True, g=False, b=False, a=False)
        mg = ex(unreal.MaterialExpressionComponentMask, -1500, -360, r=False, g=True, b=False, a=False)
        mb = ex(unreal.MaterialExpressionComponentMask, -1500, -260, r=False, g=False, b=True, a=False)
        for m in (mr, mg, mb):
            link(wa, "XYZ Texture", m, "")
        # the colour: BaseColor x lerp(1, 2R, DetailIntensity) x lerp(1, DirtColour, dirt)
        r2 = ex(unreal.MaterialExpressionMultiply, -1300, -460, const_b=2.0)
        link(mr, "", r2, "A")
        alb = ex(unreal.MaterialExpressionLinearInterpolate, -1100, -460, const_a=1.0)
        link(r2, "", alb, "B")
        link(P["DetailIntensity"], "", alb, "Alpha")
        # the dirt: saturate(1 - h / DirtHeight - (B - 0.5) x 0.6) x DirtStrength, h from the piece's lowest point
        try:
            lp = ex(unreal.MaterialExpressionLocalPosition, -1750, 200)
            lb = ex(unreal.MaterialExpressionObjectLocalBounds, -1750, 320)
            from_lp, from_lb = (lp, ""), (lb, "Min")
        except Exception as err:
            n["notes"].append("localbounds=%s" % str(err).split("\n")[0][:40])
            wp = ex(unreal.MaterialExpressionWorldPosition, -1750, 200)
            opw = ex(unreal.MaterialExpressionObjectPositionWS, -1750, 320)
            from_lp, from_lb = (wp, ""), (opw, "")
        lz = ex(unreal.MaterialExpressionComponentMask, -1550, 200, r=False, g=False, b=True, a=False)
        bz = ex(unreal.MaterialExpressionComponentMask, -1550, 320, r=False, g=False, b=True, a=False)
        link(from_lp[0], from_lp[1], lz, "")
        link(from_lb[0], from_lb[1], bz, "")
        h = ex(unreal.MaterialExpressionSubtract, -1400, 250)
        link(lz, "", h, "A")
        link(bz, "", h, "B")
        hd = ex(unreal.MaterialExpressionDivide, -1250, 250)
        link(h, "", hd, "A")
        link(P["DirtHeight"], "", hd, "B")
        gb = ex(unreal.MaterialExpressionSubtract, -1300, 360, const_b=0.5)
        link(mb, "", gb, "A")
        gb6 = ex(unreal.MaterialExpressionMultiply, -1150, 360, const_b=0.6)
        link(gb, "", gb6, "A")
        hs = ex(unreal.MaterialExpressionAdd, -1050, 280)
        link(hd, "", hs, "A")
        link(gb6, "", hs, "B")
        om = ex(unreal.MaterialExpressionOneMinus, -900, 280)
        link(hs, "", om, "")
        sat = ex(unreal.MaterialExpressionSaturate, -800, 280)
        link(om, "", sat, "")
        dirt = ex(unreal.MaterialExpressionMultiply, -700, 280)
        link(sat, "", dirt, "A")
        link(P["DirtStrength"], "", dirt, "B")
        dcol = ex(unreal.MaterialExpressionLinearInterpolate, -550, 100, const_a=1.0)
        link(P["DirtColour"], "", dcol, "B")
        link(dirt, "", dcol, "Alpha")
        c1 = ex(unreal.MaterialExpressionMultiply, -800, -460)
        link(P["BaseColor"], "", c1, "A")
        link(alb, "", c1, "B")
        c2 = ex(unreal.MaterialExpressionMultiply, -400, -300)
        link(c1, "", c2, "A")
        link(dcol, "", c2, "B")
        stex = ex(unreal.MaterialExpressionTextureObjectParameter, -2000, 700, parameter_name="StreakMap")
        if neutral is not None:
            stex.set_editor_property("texture", neutral)
        wa2 = ex(unreal.MaterialExpressionMaterialFunctionCall, -1750, 700)
        try:
            wa2.set_editor_property("material_function", fn)
        except Exception as err:
            n["notes"].append("worldaligned2=%s" % str(err).split("\n")[0][:40])
        ss2 = ex(unreal.MaterialExpressionAppendVector, -1900, 820)
        link(P["StreakSize"], "", ss2, "A")
        link(P["StreakSize"], "", ss2, "B")
        ss3 = ex(unreal.MaterialExpressionAppendVector, -1850, 880)
        link(ss2, "", ss3, "A")
        link(P["StreakLength"], "", ss3, "B")
        link(stex, "", wa2, "TextureObject")
        link(ss3, "", wa2, "TextureSize")
        sr = ex(unreal.MaterialExpressionComponentMask, -1500, 700, r=True, g=False, b=False, a=False)
        link(wa2, "XYZ Texture", sr, "")
        vn = ex(unreal.MaterialExpressionVertexNormalWS, -1750, 950)
        vz = ex(unreal.MaterialExpressionComponentMask, -1550, 950, r=False, g=False, b=True, a=False)
        link(vn, "", vz, "")
        vabs = ex(unreal.MaterialExpressionAbs, -1400, 950)
        link(vz, "", vabs, "")
        vert = ex(unreal.MaterialExpressionOneMinus, -1300, 950)
        link(vabs, "", vert, "")
        # TRY 2 (21 October, the close view's review: an even grain, no source): the streaks hang
        # from the top of the piece, where the water comes off, strongest there and fading down
        # StreakFall cm, a third of them left lower down.
        mz = ex(unreal.MaterialExpressionComponentMask, -1550, 1150, r=False, g=False, b=True, a=False)
        link(from_lb[0], "Max" if from_lb[1] == "Min" else from_lb[1], mz, "")
        dtop = ex(unreal.MaterialExpressionSubtract, -1400, 1150)
        link(mz, "", dtop, "A")
        link(lz, "", dtop, "B")
        dfall = ex(unreal.MaterialExpressionDivide, -1250, 1150)
        link(dtop, "", dfall, "A")
        link(P["StreakFall"], "", dfall, "B")
        fall1 = ex(unreal.MaterialExpressionOneMinus, -1150, 1150)
        link(dfall, "", fall1, "")
        fall2 = ex(unreal.MaterialExpressionSaturate, -1050, 1150)
        link(fall1, "", fall2, "")
        fall3 = ex(unreal.MaterialExpressionLinearInterpolate, -950, 1150, const_a=0.33, const_b=1.0)
        link(fall2, "", fall3, "Alpha")
        st0 = ex(unreal.MaterialExpressionMultiply, -1250, 760)
        link(sr, "", st0, "A")
        link(fall3, "", st0, "B")
        st1 = ex(unreal.MaterialExpressionMultiply, -1150, 760)
        link(st0, "", st1, "A")
        link(vert, "", st1, "B")
        st2 = ex(unreal.MaterialExpressionMultiply, -1000, 760)
        link(st1, "", st2, "A")
        link(P["StreakStrength"], "", st2, "B")
        scol = ex(unreal.MaterialExpressionLinearInterpolate, -850, 700, const_a=1.0)
        link(P["StreakColour"], "", scol, "B")
        link(st2, "", scol, "Alpha")
        up = ex(unreal.MaterialExpressionSaturate, -1300, 1050)
        link(vz, "", up, "")
        tp1 = ex(unreal.MaterialExpressionMultiply, -1150, 1050)
        link(up, "", tp1, "A")
        link(mb, "", tp1, "B")
        tp2 = ex(unreal.MaterialExpressionMultiply, -1000, 1050)
        link(tp1, "", tp2, "A")
        link(P["TopStrength"], "", tp2, "B")
        tcol = ex(unreal.MaterialExpressionLinearInterpolate, -850, 1000, const_a=1.0)
        link(P["TopColour"], "", tcol, "B")
        link(tp2, "", tcol, "Alpha")
        c3 = ex(unreal.MaterialExpressionMultiply, -300, -200)
        link(c2, "", c3, "A")
        link(scol, "", c3, "B")
        c4 = ex(unreal.MaterialExpressionMultiply, -200, -100)
        link(c3, "", c4, "A")
        link(tcol, "", c4, "B")
        # A PIECE'S OWN STAINS (22 October 2026, the lamp's staining after two tries of world-aligned
        # runs read as grain; production/research/street-wear/LAMP-STAINING-BAKE-2026-10-22.md): a
        # picture on the piece's first UV, its colour laid over by its alpha times StainStrength
        # (tools/art-recipes/kit_stain.py draws it). StainStrength defaults to 0, so every slot
        # without a stain draws exactly as before.
        stain = ex(unreal.MaterialExpressionTextureSampleParameter2D, -500, 120, parameter_name="StainMap")
        if neutral is not None:
            stain.set_editor_property("texture", neutral)
        sa = ex(unreal.MaterialExpressionMultiply, -300, 160)
        link(stain, "A", sa, "A")
        link(P["StainStrength"], "", sa, "B")
        c5 = ex(unreal.MaterialExpressionLinearInterpolate, -100, -60)
        link(c4, "", c5, "A")
        link(stain, "RGB", c5, "B")
        link(sa, "", c5, "Alpha")
        prop(c5, "", MP.MP_BASE_COLOR)
        # the roughness: saturate(Roughness + (G - 0.5) x 2 x RoughDetail + dirt x 0.08)
        gr = ex(unreal.MaterialExpressionSubtract, -1300, -120, const_b=0.5)
        link(mg, "", gr, "A")
        gr2 = ex(unreal.MaterialExpressionMultiply, -1150, -120, const_b=2.0)
        link(gr, "", gr2, "A")
        grd = ex(unreal.MaterialExpressionMultiply, -1000, -120)
        link(gr2, "", grd, "A")
        link(P["RoughDetail"], "", grd, "B")
        r1 = ex(unreal.MaterialExpressionAdd, -850, -120)
        link(P["Roughness"], "", r1, "A")
        link(grd, "", r1, "B")
        dr = ex(unreal.MaterialExpressionMultiply, -850, 0, const_b=0.08)
        link(dirt, "", dr, "A")
        r2b = ex(unreal.MaterialExpressionAdd, -700, -60)
        link(r1, "", r2b, "A")
        link(dr, "", r2b, "B")
        rs = ex(unreal.MaterialExpressionSaturate, -550, -60)
        link(r2b, "", rs, "")
        prop(rs, "", MP.MP_ROUGHNESS)
    prop(P["Metallic"], "", MP.MP_METALLIC)
    prop(P["Specular"], "", MP.MP_SPECULAR)
    prop(P["EmissiveColor"], "", MP.MP_EMISSIVE_COLOR)
    try:
        mel.layout_material_expressions(mat)
    except Exception:
        pass
    try:
        mel.recompile_material(mat)
    except Exception:
        pass
    unreal.EditorAssetLibrary.save_asset(path)
    if n["notes"]:
        print("make_kit_materials %s notes: %s" % (name, " ".join(n["notes"][:8])))
    return mat, n["made"], n["asked"]


def _import_detail(unreal, name, png):
    """One detail map imported as /Game/Ledger/Kit/T_KitDetail_<name>, sRGB off (the multiply
    expects 0.5 to mean 'no change'), compressed as masks."""
    if not os.path.exists(png):
        return None
    dest = "T_KitDetail_" + name
    path = PACKAGE + "/" + dest
    task = unreal.AssetImportTask()   # replace_existing re-imports over the old one in place
    task.set_editor_property("filename", png)
    task.set_editor_property("destination_path", PACKAGE)
    task.set_editor_property("destination_name", dest)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", False)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    tex = unreal.EditorAssetLibrary.load_asset(path)
    if tex is None:
        return None
    try:
        tex.set_editor_property("srgb", False)
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
    except Exception:
        pass
    unreal.EditorAssetLibrary.save_asset(path)
    return tex


def _import_stain(unreal, slot, png):
    """One slot's stain picture (tools/art-recipes/kit_stain.py) imported as
    /Game/Ledger/Kit/T_KitStain_<slot>: its colour sRGB, its amount in alpha."""
    if not os.path.exists(png):
        return None
    dest = "T_KitStain_" + slot
    path = PACKAGE + "/" + dest
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", png)
    task.set_editor_property("destination_path", PACKAGE)
    task.set_editor_property("destination_name", dest)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", False)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    tex = unreal.EditorAssetLibrary.load_asset(path)
    if tex is None:
        return None
    try:
        tex.set_editor_property("srgb", True)
    except Exception:
        pass
    unreal.EditorAssetLibrary.save_asset(path)
    return tex


def _make_instance(unreal, name, parent, values, textures=None):
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    path = PACKAGE + "/" + name
    mi = unreal.EditorAssetLibrary.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else None
    if mi is not None:
        mel.clear_all_material_instance_parameters(mi)
    else:
        mi = tools.create_asset(name, PACKAGE, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    if mi is None:
        return False
    mel.set_material_instance_parent(mi, parent)
    vec_names = {v[0] for v in VECTORS}
    for k, v in (values or {}).items():
        if k in vec_names:
            mel.set_material_instance_vector_parameter_value(mi, k, unreal.LinearColor(v[0], v[1], v[2], 1.0))
        elif k in PARAMS:
            mel.set_material_instance_scalar_parameter_value(mi, k, float(v))
    for k, t in (textures or {}).items():
        if t is not None:
            mel.set_material_instance_texture_parameter_value(mi, k, t)
    return bool(unreal.EditorAssetLibrary.save_asset(path))


def kind_values(row):
    """A kind's own parameters from its detail and dirt rows (the file's names to the master's)."""
    v = {}
    if "opacity" in row:
        v["Opacity"] = row["opacity"]
    d = row.get("detail") or {}
    if d:
        v.update({"DetailSize": d.get("size_cm", 60.0), "DetailIntensity": d.get("intensity", 1.0),
                  "RoughDetail": d.get("rough", 0.0)})
    w = row.get("streaks") or {}
    if w:
        v.update({"StreakSize": w.get("size_cm", 30.0), "StreakLength": w.get("length_cm", 200.0),
                  "StreakStrength": w.get("strength", 0.5), "StreakFall": w.get("fall_cm", 250.0)})
        if "colour" in w:
            v["StreakColour"] = tuple(w["colour"])
    tp = row.get("top") or {}
    if tp:
        v["TopStrength"] = tp.get("strength", 0.5)
        if "colour" in tp:
            v["TopColour"] = tuple(tp["colour"])
    t = row.get("dirt") or {}
    if t:
        v.update({"DirtHeight": t.get("height_cm", 50.0), "DirtStrength": t.get("strength", 0.5)})
        if "colour" in t:
            v["DirtColour"] = tuple(t["colour"])
    return v


def main():
    import unreal
    spec = load_spec()
    slots, missing = slot_values(spec)
    masters, wired_all, asked_all = {}, 0, 0
    for key, name in MASTERS.items():
        m, w, a = _make_master(unreal, name, key == "translucent")
        masters[key] = m
        wired_all += w
        asked_all += a
    details = {}
    for kind, row in spec["kinds"].items():
        name = (row.get("detail") or {}).get("map")
        if name and name not in details:
            details[name] = _import_detail(unreal, name, os.path.join(DETAIL_DIR, name + "_detail.png"))
    kinds_made = 0
    kind_assets = {}
    for kind, row in spec["kinds"].items():
        parent = masters.get(row["master"])
        if parent is None:
            continue
        vals = kind_values(row)
        name = (row.get("detail") or {}).get("map")
        texs = {"DetailMap": details.get(name)} if name else {}
        if row.get("streaks"):
            if "streaks" not in details:
                details["streaks"] = _import_detail(unreal, "streaks", os.path.join(DETAIL_DIR, "streaks_detail.png"))
            texs["StreakMap"] = details.get("streaks")
        if _make_instance(unreal, "MI_KitKind_" + kind, parent, vals, texs):
            kinds_made += 1
            kind_assets[kind] = unreal.EditorAssetLibrary.load_asset(PACKAGE + "/MI_KitKind_" + kind)
    slots_made = 0
    stains = {}
    for slot, row in slots.items():
        parent = kind_assets.get(row["kind"])
        png = spec["slots"][slot].get("stain_map")
        texs = None
        if png:
            stains[slot] = _import_stain(unreal, slot, png)
            texs = {"StainMap": stains[slot]}
        if parent is not None and _make_instance(unreal, "MI_Kit_" + slot, parent, row["values"], texs):
            slots_made += 1
    det_ok = all(t is not None for t in list(details.values()) + list(stains.values()))
    ok = (wired_all == asked_all and kinds_made == len(spec["kinds"]) and slots_made == len(slots)
          and not missing and det_ok)
    _write("kitMaterials=%s masters=%d wired=%d/%d kinds=%d/%d slots=%d/%d missingSlots=%s details=%s"
           % ("MADE" if ok else "INCOMPLETE", len([m for m in masters.values() if m]), wired_all, asked_all,
              kinds_made, len(spec["kinds"]), slots_made, len(spec["slots"]), ",".join(missing) or "none",
              ",".join("%s:%s" % (k, "ok" if v is not None else "MISSING") for k, v in details.items()) or "none"))
    return 0 if ok else 2


def selftest():
    passed = failed = 0

    def check(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("make_kit_materials selftest FAIL %s: %s" % (name, detail))

    spec = load_spec()
    check("every slot names a kind the file defines", all(r["kind"] in spec["kinds"] for r in spec["slots"].values()))
    check("every kind names a master this script makes", all(r["master"] in MASTERS for r in spec["kinds"].values()))
    check("his eight kinds are there (paint, cast iron, glass, brick, concrete, granite, enamel, galvanised)",
          all(k in spec["kinds"] for k in ("paint", "cast_iron", "glass", "brick", "concrete", "granite", "enamel", "galvanised")))
    check("a glowing slot casts no shadow (the lamp's glass, its tube, its bowl)",
          all(r.get("shadow", True) is False for r in spec["slots"].values() if r.get("glow")))
    check("the glow is relative to the arc tube, which is 1", spec["slots"].get("arc_tube", {}).get("glow") == 1.0)
    slots, missing = slot_values(spec)
    if os.path.isdir(KIT_DIR):
        check("every slot named is carried by a kit piece in ledger/Assets/Props/base-mesh", not missing, ",".join(missing))
        check("every kit piece named has its joined copy there",
              all(os.path.exists(os.path.join(KIT_DIR, n + ".glb")) for n in spec.get("pieces", [])))
        check("starting values come from the model, not invented",
              all(0.0 <= s["values"]["Roughness"] <= 1.0 and len(s["values"]["BaseColor"]) == 3 for s in slots.values()))
    print("make_kit_materials selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--list" in sys.argv:
        s, miss = slot_values(load_spec())
        for k, v in s.items():
            print(k, v["kind"], v["from"], {a: (tuple(round(x, 3) for x in b) if isinstance(b, (tuple, list)) else round(b, 3)) for a, b in v["values"].items()})
        print("missing:", miss)
        sys.exit(0)
    main()
