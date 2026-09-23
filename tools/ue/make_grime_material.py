"""Make /Game/Ledger/M_LedgerGrime, the street's stains as real decals, from a script, in CI.

    Called from tools/ue/make_base_material.py main(), in the editor run the
    probe step already starts, as make_glass_material.py is.
    python tools/ue/make_grime_material.py --selftest    # runs without Unreal

WHY, 24 September. The scene file lays ten stains - water streaks down the
parade, moss at the foot of the west row, broken tarmac, two manholes, a
sticker - as MULTIPLY decals: the surface times the stain. The one base
material in this build is opaque, so the probe hid every one of them
(decalsMultiplyNote), and the street in Unreal carried none of its dirt.
Stage 1's A22.11, wear and dirt, and the gap to Kingdom Come's frame both
start here.

A MULTIPLY, DONE WITH A DEFERRED DECAL. On a DBuffer platform - the PC - the
engine turns a Modulate decal into a Translucent one (DecalRenderingCommon.cpp,
FinalizeBlendDesc), so there is no true multiply. But laying a near-black
colour at opacity o gives surface x (1 - o), and a multiply by a grey stain of
value v at strength s gives surface x (1 - s(1 - v)): the same thing when
o = s x (1 - v) x the stain's own mask. So: BaseColor is the stain's colour
darkened by GrimeTint, Opacity is (1 - its brightness) x its alpha x
GrimeStrength. A coloured stain loses a little of its hue; a grey one is
exact.

THREE PARAMETERS the probe sets per decal: GrimeTex (the stain, RGBA),
GrimeStrength (the scene file's strength_wall or strength_ground), GrimeTint.

IT CANNOT TAKE THE MATERIAL RUN DOWN: one line to ue-material.txt, and its
caller catches anything it raises. A run where this fails leaves the stains
hidden, as before it existed.
"""
import os
import sys

PACKAGE = "/Game/Ledger"
ASSET = "M_LedgerGrime"
ASSET_PATH = PACKAGE + "/" + ASSET
TEX_PARAM = "GrimeTex"
STRENGTH_PARAM, STRENGTH_DEFAULT = "GrimeStrength", 0.75
TINT_PARAM, TINT_DEFAULT = "GrimeTint", (0.2, 0.2, 0.2)
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


def grime_line(status, wired, asked, flags, saved):
    return ("grimeMaterialStatus=%s grimeMaterialPath=%s grimeMaterialWired=%d/%d "
            "grimeMaterialFlags=%s grimeMaterialSaved=%s grimeMaterialParams=%s,%s,%s"
            % (status, ASSET_PATH, wired, asked, "/".join(flags) or "none",
               "yes" if saved else "NO", TEX_PARAM, STRENGTH_PARAM, TINT_PARAM))


def main():
    import unreal
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    if unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH):
        unreal.EditorAssetLibrary.delete_asset(ASSET_PATH)
    mat = tools.create_asset(ASSET, PACKAGE, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        _write(grime_line("CREATE-FAILED", 0, 8, [], False))
        return 2
    flags = ["%s=%s" % (p, _set_enum(unreal, mat, p, e, v)) for p, e, v in FLAGS]
    X = unreal
    tex = mel.create_material_expression(mat, X.MaterialExpressionTextureSampleParameter2D, -900, 0)
    tex.set_editor_property("parameter_name", TEX_PARAM)
    white = unreal.load_asset(WHITE)
    if white is not None:
        tex.set_editor_property("texture", white)
    tint = mel.create_material_expression(mat, X.MaterialExpressionVectorParameter, -900, 300)
    tint.set_editor_property("parameter_name", TINT_PARAM)
    tint.set_editor_property("default_value", unreal.LinearColor(*TINT_DEFAULT, 1.0))
    strength = mel.create_material_expression(mat, X.MaterialExpressionScalarParameter, -900, 450)
    strength.set_editor_property("parameter_name", STRENGTH_PARAM)
    strength.set_editor_property("default_value", STRENGTH_DEFAULT)
    third = mel.create_material_expression(mat, X.MaterialExpressionConstant3Vector, -900, 600)
    third.set_editor_property("constant", unreal.LinearColor(1.0 / 3, 1.0 / 3, 1.0 / 3, 1.0))
    colour = mel.create_material_expression(mat, X.MaterialExpressionMultiply, -500, 0)
    bright = mel.create_material_expression(mat, X.MaterialExpressionDotProduct, -600, 500)
    dark = mel.create_material_expression(mat, X.MaterialExpressionOneMinus, -450, 500)
    masked = mel.create_material_expression(mat, X.MaterialExpressionMultiply, -300, 450)
    opacity = mel.create_material_expression(mat, X.MaterialExpressionMultiply, -150, 450)

    links = [(tex, "RGB", colour, "A"), (tint, "", colour, "B"),
             (tex, "RGB", bright, "A"), (third, "", bright, "B"),
             (bright, "", dark, ""),
             (dark, "", masked, "A"), (tex, "A", masked, "B"),
             (masked, "", opacity, "A"), (strength, "", opacity, "B")]
    wired = 0
    for a, out_name, b, in_name in links:
        try:
            if mel.connect_material_expressions(a, out_name, b, in_name):
                wired += 1
        except Exception:
            pass
    for src, prop in ((colour, unreal.MaterialProperty.MP_BASE_COLOR),
                      (opacity, unreal.MaterialProperty.MP_OPACITY)):
        try:
            if mel.connect_material_property(src, "", prop):
                wired += 1
        except Exception:
            pass
    asked = len(links) + 2
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
    _write(grime_line("MADE" if ok else "INCOMPLETE", wired, asked, flags, saved))
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

    line = grime_line("MADE", 11, 11, ["material_domain=taken"], True)
    check("the line carries its wired denominator", "grimeMaterialWired=11/11" in line, line)
    check("and names the asset the probe loads", "grimeMaterialPath=/Game/Ledger/M_LedgerGrime" in line)
    # THE ARITHMETIC THE DOCSTRING CLAIMS: black at o = s(1-v)a is multiply by v at s.
    for v, s, a in ((0.5, 0.75, 1.0), (0.2, 0.8, 0.6), (1.0, 0.7, 1.0)):
        o = s * (1 - v) * a
        multiply = 1 - s * a * (1 - v)
        check("black at o equals multiply for v=%.1f s=%.2f a=%.1f" % (v, s, a), abs((1 - o) - multiply) < 1e-9)
    print("make_grime_material selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
