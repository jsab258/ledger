"""Make /Game/Ledger/M_LedgerGlass, the see-through glass, from a script, in CI.

    Called from tools/ue/make_base_material.py main(), in the editor run the
    probe step already starts, as make_sky_material.py and import_street.py are.
    python tools/ue/make_glass_material.py --selftest    # runs without Unreal

WHY, 23 September. The look moved into Unreal, and the one base material the
street wears is opaque: a shop window drawn with it was a solid pane in
front of the lit room the recipe puts behind it, so the display glass was
left out altogether (production/specs/unreal-look.json glass_see_through).
The sheet's shop windows show the room THROUGH reflections, which is what
this material is for: translucent, lit in the forward pass so the sky and
the street's light land on it as a sheen, tinted, nearly smooth.

THREE PARAMETERS, each with its default here, all set per street mesh by the
probe from the look file: GlassTint (the colour the glass lays over what is
behind it), GlassOpacity (how much of it is glass and how much is room) and
GlassRoughness.

IT CANNOT TAKE THE MATERIAL RUN DOWN: it appends one line to
ue-material.txt and its caller catches anything it raises. A run where this
fails leaves the glass out, exactly as before it existed.
"""
import os
import sys

PACKAGE = "/Game/Ledger"
ASSET = "M_LedgerGlass"
ASSET_PATH = PACKAGE + "/" + ASSET
TINT_PARAM, TINT_DEFAULT = "GlassTint", (0.05, 0.06, 0.07)
OPACITY_PARAM, OPACITY_DEFAULT = "GlassOpacity", 0.25
ROUGH_PARAM, ROUGH_DEFAULT = "GlassRoughness", 0.05
#: what the clean pane lets through (the research's recipe: a faint green of float glass)
TRANSMIT_PARAM, TRANSMIT_DEFAULT = "GlassTransmit", (0.88, 0.92, 0.90)

#: (property, enum type name, enum value name) - read back after the write.
FLAGS = [
    ("blend_mode", "BlendMode", "BLEND_TRANSLUCENT"),
    ("translucency_lighting_mode", "TranslucencyLightingMode", "TLM_SURFACE_PER_PIXEL_LIGHTING"),
    ("shading_model", "MaterialShadingModel", "MSM_THIN_TRANSLUCENT"),
]


def _write(line):
    try:
        import unreal
        root = unreal.Paths.project_dir()
    except Exception:
        root = "."
    with open(os.path.join(root, "ue-material.txt"), "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _set_enum(unreal, mat, prop, enum_name, value_name):
    enum = getattr(unreal, enum_name, None)
    value = getattr(enum, value_name, None) if enum is not None else None
    if value is None:
        return "not-exposed"
    try:
        mat.set_editor_property(prop, value)
    except Exception:
        return "refused"
    try:
        return "taken" if mat.get_editor_property(prop) == value else "readback-differs"
    except Exception:
        return "not-exposed"


def glass_line(status, wired, asked, flags, saved):
    return ("glassMaterialStatus=%s glassMaterialPath=%s glassMaterialWired=%d/%d "
            "glassMaterialFlags=%s glassMaterialSaved=%s glassMaterialParams=%s,%s,%s"
            % (status, ASSET_PATH, wired, asked, "/".join(flags) or "none",
               "yes" if saved else "NO", TINT_PARAM, OPACITY_PARAM, ROUGH_PARAM))


def main():
    import unreal
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    if unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH):
        unreal.EditorAssetLibrary.delete_asset(ASSET_PATH)
    mat = tools.create_asset(ASSET, PACKAGE, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        _write(glass_line("CREATE-FAILED", 0, 4, [], False))
        return 2
    flags = ["%s=%s" % (p, _set_enum(unreal, mat, p, e, v)) for p, e, v in FLAGS]
    # ON SKINNED MESHES TOO, 30 September: Sheila's spectacle lenses wear it
    # (LedgerGarments.h), and a material not marked for skeletal meshes draws
    # as the engine's grey stand-in in a game: the lenses came out opaque grey.
    try:
        mat.set_editor_property("used_with_skeletal_mesh", True)
        flags.append("used_with_skeletal_mesh=%s" % ("taken" if mat.get_editor_property("used_with_skeletal_mesh") else "REFUSED"))
    except Exception as e:
        flags.append("used_with_skeletal_mesh=RAISED-%s" % type(e).__name__)

    tint = mel.create_material_expression(mat, unreal.MaterialExpressionVectorParameter, -500, 0)
    tint.set_editor_property("parameter_name", TINT_PARAM)
    tint.set_editor_property("default_value", unreal.LinearColor(*TINT_DEFAULT, 1.0))
    opac = mel.create_material_expression(mat, unreal.MaterialExpressionScalarParameter, -500, 200)
    opac.set_editor_property("parameter_name", OPACITY_PARAM)
    opac.set_editor_property("default_value", OPACITY_DEFAULT)
    rough = mel.create_material_expression(mat, unreal.MaterialExpressionScalarParameter, -500, 320)
    rough.set_editor_property("parameter_name", ROUGH_PARAM)
    rough.set_editor_property("default_value", ROUGH_DEFAULT)

    # THIN TRANSLUCENT GLASS, 1 October (Jafar: "The shop windows have interiors
    # and reflections"; a fresh reviewer that evening: "no reflection and no dirt,
    # so it looks like an open hole"). Two tries failed because Unreal's
    # Translucent blend multiplies everything the glass draws by its Opacity, the
    # reflection included: 4% of the street at 0.25 opacity is 1%, and a Fresnel
    # opacity only lifted it at grazing angles. The Thin Translucent shading model
    # keeps the reflection whole (Lumen's front-layer reflection still reaches it,
    # DefaultEngine.ini) and lets the room through by its Transmittance Color; so
    # Opacity is now only the dirt on the pane, GlassTint the dirt's colour
    # (production/research/shop-glass-reflections/NOTE.md, its recipe).
    spec = mel.create_material_expression(mat, unreal.MaterialExpressionConstant, -500, 600)
    spec.set_editor_property("r", 1.0)
    trans = mel.create_material_expression(mat, unreal.MaterialExpressionVectorParameter, -500, 700)
    trans.set_editor_property("parameter_name", TRANSMIT_PARAM)
    trans.set_editor_property("default_value", unreal.LinearColor(*TRANSMIT_DEFAULT, 1.0))
    thin = mel.create_material_expression(mat, unreal.MaterialExpressionThinTranslucentMaterialOutput, -150, 700)
    thin_wired = False
    for pin in ("Transmittance Color", "TransmittanceColor", ""):
        try:
            if mel.connect_material_expressions(trans, "", thin, pin):
                thin_wired = True
                break
        except Exception:
            pass
    flags.append("thin_translucent_output=%s" % ("taken" if thin_wired else "NOT-WIRED"))
    asked = [(tint, unreal.MaterialProperty.MP_BASE_COLOR),
             (opac, unreal.MaterialProperty.MP_OPACITY),
             (rough, unreal.MaterialProperty.MP_ROUGHNESS),
             (spec, unreal.MaterialProperty.MP_SPECULAR)]
    wired = 0
    for src, prop in asked:
        try:
            if mel.connect_material_property(src, "", prop):
                wired += 1
        except Exception:
            pass
    try:
        mel.recompile_material(mat)
    except Exception:
        pass
    saved = False
    try:
        saved = bool(unreal.EditorAssetLibrary.save_asset(ASSET_PATH))
    except Exception:
        saved = False
    ok = wired == len(asked) and saved and all(f.endswith("=taken") for f in flags)
    _write(glass_line("MADE" if ok else "INCOMPLETE", wired, len(asked), flags, saved))
    return 0 if ok else 2


def selftest():
    passed = failed = 0

    def check(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("FAILED - %s : %s" % (name, detail))

    line = glass_line("MADE", 4, 4, ["blend_mode=taken"], True)
    check("the line carries its wired denominator", "glassMaterialWired=4/4" in line, line)
    check("and names the asset the probe loads", "glassMaterialPath=/Game/Ledger/M_LedgerGlass" in line)
    check("a failed save says NO", "glassMaterialSaved=NO" in glass_line("INCOMPLETE", 3, 3, [], False))
    check("the defaults are glass: nearly smooth, mostly see-through",
          ROUGH_DEFAULT < 0.2 and 0.0 < OPACITY_DEFAULT < 0.5)
    check("thin translucent: the reflection is not scaled by opacity", ("shading_model", "MaterialShadingModel", "MSM_THIN_TRANSLUCENT") in FLAGS)
    check("and lets most light through", all(0.8 < c < 1.0 for c in TRANSMIT_DEFAULT))
    print("make_glass_material selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
