"""Make /Game/Ledger/M_LedgerStain, the look method's one decal material for stains and grime, from a script.
    Called from tools/ue/make_base_material.py main(), after the grime and the wet, as they are;
    or on its own in the editor (the script's FULL path, or the commandlet fails quietly):
    UnrealEditor-Cmd ue-probe/LedgerProbe.uproject -run=pythonscript -script=C:/Users/Jafar/ledger-local/tools/ue/make_stain_material.py
    python tools/ue/make_stain_material.py --selftest    # runs without Unreal

WHY, 29 October 2026 (his order D11, the look; production/research/street-wear/MAFIA-WEAR-2026-10-28.md, "The
layer recipe, shared by both", step 1): Mafia lays its wear with one decal material that writes colour, roughness
and coverage, so a stain differs from its wall in sheen as well as in colour. The street's own grime decal
(M_LedgerGrime) writes colour only, and changing it would change every stain already on the street before any gate,
so this is its own material, used by the new office and shop-front decals until they pass. Built on the grime's
colour rule and the wet decal's roughness wiring (reuse first: make_grime_material.py, make_wet_material.py).

TWO WAYS, ONE MATERIAL (the method's (a) and (b)):
  (a) a drawn stain picture (StainTex: colour, coverage in alpha) for leaks, streaks and rust;
  (b) the same picture as a mask over a tiling pattern (TileTex, its red channel, tiled TileScale times across
      the decal; UseTile 1) for grunge and damp.
Colour as the grime's: the stain darkened by StainTint (or the tint itself, TintOnly 1, for wear that lightens);
coverage (1 - the picture's brightness) x its alpha x StainStrength, times the tile where it is used; roughness
StainRoughness under the same coverage. No normal is written: the wall's own detail stays (the method's step 4,
no detail normals unless a gate asks).

THE CHECK (the method's step 1): a stain differs from its wall by at least 0.1 in the roughness view and darkens
the base colour by at most 40%. The selftest holds the defaults to it on a mid wall (roughness 0.6, colour 0.35).
"""
import os
import sys

PACKAGE = "/Game/Ledger"
ASSET = "M_LedgerStain"
ASSET_PATH = PACKAGE + "/" + ASSET
TEX_PARAM = "StainTex"
TILE_PARAM, TILE_SCALE_PARAM, TILE_SCALE_DEFAULT, USE_TILE_PARAM = "TileTex", "TileScale", 1.5, "UseTile"
STRENGTH_PARAM, STRENGTH_DEFAULT = "StainStrength", 0.6
TINT_PARAM, TINT_DEFAULT = "StainTint", (0.35, 0.33, 0.3)
TINT_ONLY_PARAM, TINT_ONLY_DEFAULT = "TintOnly", 0.0
ROUGH_PARAM, ROUGH_DEFAULT = "StainRoughness", 0.85
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


def stain_line(status, wired, asked, flags, saved):
    return ("stainMaterialStatus=%s stainMaterialPath=%s stainMaterialWired=%d/%d stainMaterialFlags=%s stainMaterialSaved=%s"
            % (status, ASSET_PATH, wired, asked, "/".join(flags) or "none", "yes" if saved else "NO"))


def darkening(wall, tint, strength, picture=0.0, alpha=1.0):
    """How much a full-coverage stain darkens a wall of brightness `wall`: the decal blends its colour (the picture
    times the tint) over the wall by its coverage ((1 - picture) x alpha x strength)."""
    cover = (1.0 - picture) * alpha * strength
    colour = picture * tint
    out = wall * (1.0 - cover) + colour * cover
    return 1.0 - out / wall


def roughness_shift(wall_rough, stain_rough, strength, picture=0.0, alpha=1.0):
    cover = (1.0 - picture) * alpha * strength
    return abs((wall_rough * (1.0 - cover) + stain_rough * cover) - wall_rough)


def main():
    import unreal
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    if unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH):
        unreal.EditorAssetLibrary.delete_asset(ASSET_PATH)
    mat = tools.create_asset(ASSET, PACKAGE, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        _write(stain_line("CREATE-FAILED", 0, 1, [], False))
        return 2
    flags = ["%s=%s" % (p, _set_enum(unreal, mat, p, e, v)) for p, e, v in FLAGS]
    X = unreal
    white = unreal.load_asset(WHITE)

    def node(cls, x, y, **props):
        n = mel.create_material_expression(mat, cls, x, y)
        for k, v in props.items():
            n.set_editor_property(k, v)
        return n
    tex = node(X.MaterialExpressionTextureSampleParameter2D, -1100, 0, parameter_name=TEX_PARAM)
    tile = node(X.MaterialExpressionTextureSampleParameter2D, -1100, 900, parameter_name=TILE_PARAM)
    if white is not None:
        tex.set_editor_property("texture", white)
        tile.set_editor_property("texture", white)
    uv = node(X.MaterialExpressionTextureCoordinate, -1500, 900)
    tile_scale = node(X.MaterialExpressionScalarParameter, -1500, 1050, parameter_name=TILE_SCALE_PARAM, default_value=TILE_SCALE_DEFAULT)
    tiled_uv = node(X.MaterialExpressionMultiply, -1300, 900)
    use_tile = node(X.MaterialExpressionScalarParameter, -1100, 1100, parameter_name=USE_TILE_PARAM, default_value=0.0)
    one = node(X.MaterialExpressionConstant, -1100, 1250, r=1.0)
    tile_or_one = node(X.MaterialExpressionLinearInterpolate, -800, 950)
    tint = node(X.MaterialExpressionVectorParameter, -1100, 300, parameter_name=TINT_PARAM, default_value=unreal.LinearColor(*TINT_DEFAULT, 1.0))
    strength = node(X.MaterialExpressionScalarParameter, -1100, 450, parameter_name=STRENGTH_PARAM, default_value=STRENGTH_DEFAULT)
    third = node(X.MaterialExpressionConstant3Vector, -1100, 600, constant=unreal.LinearColor(1.0 / 3, 1.0 / 3, 1.0 / 3, 1.0))
    tint_only = node(X.MaterialExpressionScalarParameter, -1100, 750, parameter_name=TINT_ONLY_PARAM, default_value=TINT_ONLY_DEFAULT)
    rough = node(X.MaterialExpressionScalarParameter, -400, 650, parameter_name=ROUGH_PARAM, default_value=ROUGH_DEFAULT)
    colour = node(X.MaterialExpressionMultiply, -700, 0)
    pick = node(X.MaterialExpressionLinearInterpolate, -500, 0)
    bright = node(X.MaterialExpressionDotProduct, -800, 500)
    dark = node(X.MaterialExpressionOneMinus, -650, 500)
    masked = node(X.MaterialExpressionMultiply, -500, 450)
    tiled = node(X.MaterialExpressionMultiply, -350, 600)
    opacity = node(X.MaterialExpressionMultiply, -200, 450)
    links = [(uv, "", tiled_uv, "A"), (tile_scale, "", tiled_uv, "B"), (tiled_uv, "", tile, "UVs"),
             (one, "", tile_or_one, "A"), (tile, "R", tile_or_one, "B"), (use_tile, "", tile_or_one, "Alpha"),
             (tex, "RGB", colour, "A"), (tint, "", colour, "B"),
             (colour, "", pick, "A"), (tint, "", pick, "B"), (tint_only, "", pick, "Alpha"),
             (tex, "RGB", bright, "A"), (third, "", bright, "B"), (bright, "", dark, ""),
             (dark, "", masked, "A"), (tex, "A", masked, "B"),
             (masked, "", tiled, "A"), (tile_or_one, "", tiled, "B"),
             (tiled, "", opacity, "A"), (strength, "", opacity, "B")]
    wired = 0
    for a, out_name, b, in_name in links:
        try:
            if mel.connect_material_expressions(a, out_name, b, in_name):
                wired += 1
        except Exception:
            pass
    for src, prop in ((pick, unreal.MaterialProperty.MP_BASE_COLOR),
                      (rough, unreal.MaterialProperty.MP_ROUGHNESS),
                      (opacity, unreal.MaterialProperty.MP_OPACITY)):
        try:
            if mel.connect_material_property(src, "", prop):
                wired += 1
        except Exception:
            pass
    asked = len(links) + 3
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
    _write(stain_line("MADE" if ok else "INCOMPLETE", wired, asked, flags, saved))
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
    line = stain_line("MADE", 23, 23, ["material_domain=taken"], True)
    check("the line carries its wired denominator", "stainMaterialWired=23/23" in line, line)
    check("and names the asset the game loads", "stainMaterialPath=/Game/Ledger/M_LedgerStain" in line)
    # the method's step 1 check, on a mid wall (colour 0.35, roughness 0.6), a full-coverage dark stain (picture 0.3)
    d = darkening(0.35, max(TINT_DEFAULT), STRENGTH_DEFAULT, picture=0.3)
    check("a stain darkens its wall by at most 40%", 0.0 < d <= 0.40, "%.2f" % d)
    r = roughness_shift(0.6, ROUGH_DEFAULT, STRENGTH_DEFAULT, picture=0.3)
    check("and differs from it by at least 0.1 in roughness", r >= 0.1, "%.3f" % r)
    check("the tile is tiled 1 to 2 times across the decal (the method's (b))", 1.0 <= TILE_SCALE_DEFAULT <= 2.0)
    check("no normal is written (the method's step 4)", "MP_NORMAL" not in open(__file__, encoding="utf-8").read().split("def main")[1].split("def selftest")[0])
    print("make_stain_material selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    try:
        import unreal  # noqa: F401
        main()
    except ImportError:
        print(__doc__)
