"""Make /Game/Ledger/M_LedgerWet, standing water as a projected decal, from a script.
    Called from tools/ue/make_base_material.py main(), after the grime, as the
    glass and the grime are; or on its own in the editor:
    UnrealEditor-Cmd ue-probe/LedgerProbe.uproject -run=pythonscript -script=tools/ue/make_wet_material.py
    python tools/ue/make_wet_material.py --selftest    # runs without Unreal

WHY, 1 October (the proof frame, stage 1, item 3, the wet street; the street
research, production/research/aaa-street, section 3: Lagarde's wet surfaces,
puddles in the dips): the street's base material makes a surface wetter by
lowering its roughness and darkening its colour, but water that STANDS is
another thing: inside a puddle the surface under it is near black and a near
mirror, and the bumps of the ground are drowned flat. A deferred decal does
exactly that over whatever is beneath it, placed by rule (tools/street_wear.py,
"puddle"), so the base material, whose every wire is counted, is not touched.

WHAT IT WRITES, through the decal's opacity (WetMask's alpha x WetStrength):
BaseColor WetTint (default 0.025, the colour of water over asphalt), Roughness
WetRoughness (default 0.04), and Normal flat up. On the PC the engine draws a
deferred decal through its DBuffer, which takes colour, normal and roughness
from the pins connected.
"""
import os
import sys

PACKAGE = "/Game/Ledger"
ASSET = "M_LedgerWet"
ASSET_PATH = PACKAGE + "/" + ASSET
MASK_PARAM = "WetMask"
STRENGTH_PARAM, STRENGTH_DEFAULT = "WetStrength", 0.9
TINT_PARAM, TINT_DEFAULT = "WetTint", (0.06, 0.062, 0.066)   # 2 October: 0.025 read as holes in the first stage-1 frame
ROUGH_PARAM, ROUGH_DEFAULT = "WetRoughness", 0.05   # 2 October, evening: 0.04 "read as holes" while every decal was turned wrong; with the turn fixed, near-mirror puddles to reflect the shopfronts (his "wet street and its reflections")
WHITE = "/Engine/EngineResources/WhiteSquareTexture.WhiteSquareTexture"
FLAGS = [
    ("material_domain", "MaterialDomain", "MD_DEFERRED_DECAL"),
    ("blend_mode", "BlendMode", "BLEND_TRANSLUCENT"),
]


def _write(line):
    try:
        import unreal
        root = unreal.Paths.project_dir()
    except Exception:
        root = "."
    try:
        with open(os.path.join(root, "ue-material.txt"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass
    print(line)


def wet_line(status, wired, asked, flags, saved):
    return ("wetMaterialStatus=%s wetMaterialPath=%s wetMaterialWired=%d/%d wetMaterialSaved=%s wetMaterialFlags=%s"
            % (status, ASSET_PATH, wired, asked, "yes" if saved else "no", "+".join(flags) or "none"))


def _set_enum(unreal, mat, prop, enum_name, value):
    try:
        mat.set_editor_property(prop, getattr(getattr(unreal, enum_name), value))
        return "taken"
    except Exception:
        return "REFUSED"


def main():
    import unreal
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    if unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH):
        unreal.EditorAssetLibrary.delete_asset(ASSET_PATH)
    mat = tools.create_asset(ASSET, PACKAGE, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        _write(wet_line("CREATE-FAILED", 0, 8, [], False))
        return 2
    flags = ["%s=%s" % (p, _set_enum(unreal, mat, p, e, v)) for p, e, v in FLAGS]
    X = unreal
    mask = mel.create_material_expression(mat, X.MaterialExpressionTextureSampleParameter2D, -900, 0)
    mask.set_editor_property("parameter_name", MASK_PARAM)
    white = unreal.load_asset(WHITE)
    if white is not None:
        mask.set_editor_property("texture", white)
    tint = mel.create_material_expression(mat, X.MaterialExpressionVectorParameter, -900, 300)
    tint.set_editor_property("parameter_name", TINT_PARAM)
    tint.set_editor_property("default_value", unreal.LinearColor(*TINT_DEFAULT, 1.0))
    rough = mel.create_material_expression(mat, X.MaterialExpressionScalarParameter, -900, 450)
    rough.set_editor_property("parameter_name", ROUGH_PARAM)
    rough.set_editor_property("default_value", ROUGH_DEFAULT)
    strength = mel.create_material_expression(mat, X.MaterialExpressionScalarParameter, -900, 600)
    strength.set_editor_property("parameter_name", STRENGTH_PARAM)
    strength.set_editor_property("default_value", STRENGTH_DEFAULT)
    flat = mel.create_material_expression(mat, X.MaterialExpressionConstant3Vector, -900, 750)
    flat.set_editor_property("constant", unreal.LinearColor(0.0, 0.0, 1.0, 1.0))
    opacity = mel.create_material_expression(mat, X.MaterialExpressionMultiply, -300, 450)
    links = [(mask, "A", opacity, "A"), (strength, "", opacity, "B")]
    wired = 0
    for a, out_name, b, in_name in links:
        try:
            if mel.connect_material_expressions(a, out_name, b, in_name):
                wired += 1
        except Exception:
            pass
    for src, prop in ((tint, unreal.MaterialProperty.MP_BASE_COLOR),
                      (rough, unreal.MaterialProperty.MP_ROUGHNESS),
                      (flat, unreal.MaterialProperty.MP_NORMAL),
                      (opacity, unreal.MaterialProperty.MP_OPACITY)):
        try:
            if mel.connect_material_property(src, "", prop):
                wired += 1
        except Exception:
            pass
    asked = len(links) + 4
    try:
        mel.recompile_material(mat)
    except Exception:
        pass
    saved = False
    try:
        saved = bool(unreal.EditorAssetLibrary.save_asset(ASSET_PATH))
    except Exception:
        saved = False
    ok = wired == asked and saved and all(f.endswith("=taken") for f in flags)
    _write(wet_line("MADE" if ok else "INCOMPLETE", wired, asked, flags, saved))
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
    line = wet_line("MADE", 6, 6, ["material_domain=taken"], True)
    check("the line carries its wired denominator", "wetMaterialWired=6/6" in line, line)
    check("and names the asset the game loads", "wetMaterialPath=/Game/Ledger/M_LedgerWet" in line)
    check("standing water is darker than wet asphalt (about 0.05) and a near mirror",
          max(TINT_DEFAULT) < 0.05 and ROUGH_DEFAULT < 0.1)
    print("make_wet_material selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    try:
        import unreal  # noqa: F401
        main()
    except ImportError:
        print(__doc__)
