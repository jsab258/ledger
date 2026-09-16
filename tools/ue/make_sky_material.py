"""Make the one material that lets the approved photograph BE the sky.

    UnrealEditor-Cmd.exe LedgerProbe.uproject -run=pythonscript \
        -script="tools/ue/make_sky_material.py" -unattended -nopause -nosplash
    python3 tools/ue/make_sky_material.py --selftest   # runs without Unreal

WHY A SECOND MATERIAL AND NOT A BRANCH IN THE FIRST. M_LedgerSurface is lit,
opaque and single-sided, and every one of those three is wrong for a sky:
a sky dome is seen from INSIDE (so the material must be two-sided), it is not
lit by the scene (so it is unlit and its colour arrives through Emissive), and
a sky light capturing in real time is documented to capture sky-flagged
materials (so it carries the sky flag). Putting a static switch through the
proven material to get those three would put every one of 563 pieces behind a
new permutation for a dome that is one actor. This file is small on purpose.

WHY A MATERIAL ASSET AT ALL. Unreal cannot build a material at runtime: the
shader compiler is editor-only and a packaged game can only make INSTANCES of
materials that already exist as assets. Same reason, same route and the same
build step as tools/ue/make_base_material.py, whose docstring carries the
argument in full.

WHAT IT MAKES. One material, /Game/Ledger/M_LedgerSky:

    SkyMap        TextureSampleParameter2D   the long-lat photograph
    SkyLuminance  ScalarParameter            multiplied into the sample
                  -> Emissive Color

THE PARAMETER NAMES ARE A CONTRACT WITH C++ THAT NOTHING AT RUNTIME CHECKS: a
dynamic instance asked for a parameter the material does not have sets
nothing, returns nothing and logs nothing, and the dome comes back grey with
every count green. --selftest reads the names back out of the C++ that sets
them and refuses to agree with itself. That check runs in the container that
writes this file, so it is run before every dispatch.

SKYLUMINANCE IS THE FIRST VALUE OF A SERIES THAT HAS NEVER BEEN PRINTED and
rule 2 forbids calling it anything better. The dome is unlit, so its emissive
is an absolute value going into an auto-exposed filmic tonemap whose key this
container cannot compute; 1.0 is the identity and it is deliberately NOT
guessed upward. The frame prints what the sky band read, and the second value
comes off that reading.

THREE FLAGS DECIDE WHETHER THIS WORKS AND ALL THREE ARE READ BACK. unlit,
two-sided and is-sky are set through set_editor_property, which raises on a
name this engine version does not have; each is tried, read back, and printed
as taken/refused/not-exposed. A refusal does not stop the material being made:
an unlit two-sided material that is not sky-flagged still DRAWS the
photograph, it only stops feeding the sky light's real-time capture, and the
difference belongs in the verdict rather than in a silence.
"""

import os
import sys

PACKAGE = "/Game/Ledger"
ASSET = "M_LedgerSky"
ASSET_PATH = PACKAGE + "/" + ASSET

# THE CONTRACT. Spelled here and asserted against VignetteShot.cpp, which is
# where C++ sets them. Not in SurfaceBind.h, which this change may not touch.
TEXTURE_PARAM = "SkyMap"
SCALAR_PARAM = "SkyLuminance"
SCALAR_DEFAULT = 1.0

# THE DEFAULT TEXTURE THE SAMPLER MUST CARRY TO COMPILE AT ALL. Run 23 landed
# a perfect-looking verdict over a material that never compiled because one
# sampler held no texture and another held a texture of the wrong type. This
# list and its order are make_base_material.py's COLOUR_DEFAULTS, unchanged,
# because that list is the one this project has measured: the sky sample is an
# sRGB colour sample exactly as base colour is.
COLOUR_DEFAULTS = [
    "/Engine/EngineResources/DefaultTexture",
    "/Engine/EngineResources/WhiteSquareTexture",
    "/Engine/EngineMaterials/DefaultDiffuse",
]

# THE FLAGS, AS (python property name, wanted value, what it buys). Spelled as
# data so the readback loop cannot drift from the write loop.
FLAGS = [
    ("shading_model", "MSM_UNLIT", "the-photograph-is-not-lit-by-the-street"),
    ("two_sided", True, "a-dome-is-seen-from-inside"),
    ("is_sky", True, "the-skylight-realtime-capture-reads-sky-materials"),
]


def _write(line):
    """The evidence channel is a file, not a log tail, and this one is written
    beside the project exactly as ue-material.txt is so the workflow step can
    fold it into the build verdict."""
    try:
        import unreal
        root = unreal.Paths.project_dir()
    except Exception:
        root = "."
    # APPENDED TO ue-material.txt, NOT A FILE OF ITS OWN. The workflow step
    # reads that file whole and folds it into the build verdict; a second
    # file would need a second read, and the step has no room for one.
    # make_base_material.py has already written its single line in "w" mode
    # by the time this runs, so appending cannot lose it.
    path = os.path.join(root, "ue-material.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def _first_that_loads(unreal, paths):
    """The first candidate that is in the asset registry AND loads. The
    registry check is not an optimisation: load_asset on a missing path logs
    an editor Error, and editor Errors are what turn a working script into a
    non-zero exit."""
    for p in paths:
        try:
            if not unreal.EditorAssetLibrary.does_asset_exist(p):
                continue
            a = unreal.EditorAssetLibrary.load_asset(p)
            if a is not None:
                return a, p
        except Exception:
            continue
    return None, "NOT-FOUND/tried=" + ";".join(paths)


def _set_flag(unreal, mat, name, wanted):
    """Set one flag and READ IT BACK. Returns one of taken / refused /
    not-exposed / readback-differs, which are four different facts and have
    never been the same fact."""
    value = wanted
    if isinstance(wanted, str):
        # An enum spelled by name, because the enum type differs by version
        # and a missing attribute must read as not-exposed rather than raise.
        enum = getattr(unreal, "MaterialShadingModel", None)
        value = getattr(enum, wanted, None) if enum is not None else None
        if value is None:
            return "not-exposed"
    try:
        mat.set_editor_property(name, value)
    except Exception:
        return "refused"
    try:
        got = mat.get_editor_property(name)
    except Exception:
        return "not-exposed"
    return "taken" if got == value else "readback-differs"


def main():
    import unreal

    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary

    if unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH):
        # ALWAYS REGENERATED, for make_base_material.py's reason: an asset
        # kept from a previous run cannot be shown to match the script that
        # claims to have made it.
        unreal.EditorAssetLibrary.delete_asset(ASSET_PATH)

    mat = tools.create_asset(ASSET, PACKAGE, unreal.Material,
                             unreal.MaterialFactoryNew())
    if mat is None:
        _write("skyMaterialStatus=CREATE-FAILED skyMaterialPath=%s "
               "skyMaterialNote=asset-tools-returned-nothing" % ASSET_PATH)
        return 2

    flags = []
    for name, wanted, why in FLAGS:
        flags.append("%s=%s" % (name, _set_flag(unreal, mat, name, wanted)))

    tex_expr = mel.create_material_expression(
        mat, unreal.MaterialExpressionTextureSampleParameter2D, -700, 0)
    tex_expr.set_editor_property("parameter_name", TEXTURE_PARAM)
    default_tex, default_from = _first_that_loads(unreal, COLOUR_DEFAULTS)
    if default_tex is not None:
        tex_expr.set_editor_property("texture", default_tex)
    lum = mel.create_material_expression(
        mat, unreal.MaterialExpressionScalarParameter, -700, 220)
    lum.set_editor_property("parameter_name", SCALAR_PARAM)
    lum.set_editor_property("default_value", SCALAR_DEFAULT)
    mul = mel.create_material_expression(
        mat, unreal.MaterialExpressionMultiply, -420, 60)

    # EVERY CONNECTION IS COUNTED AND THE DENOMINATOR IS THE NUMBER ASKED FOR,
    # so a material with two of three wires can never print as made. The pin
    # spellings are the ones make_base_material.py's sweep settled on: an
    # empty output name is the expression's default output, and A/B are the
    # multiply's two inputs.
    asked = [
        (tex_expr, "", mul, "A"),
        (lum, "", mul, "B"),
    ]
    wired = 0
    refused = []
    for src, out, dst, inp in asked:
        ok = False
        try:
            ok = bool(mel.connect_material_expressions(src, out, dst, inp))
        except Exception:
            ok = False
        if ok:
            wired += 1
        else:
            refused.append("%s-to-%s" % (src.get_name(), inp))
    try:
        to_emissive = bool(mel.connect_material_property(
            mul, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR))
    except Exception:
        to_emissive = False
    if to_emissive:
        wired += 1
    else:
        refused.append("multiply-to-emissive")

    try:
        mel.recompile_material(mat)
    except Exception:
        pass
    saved = False
    try:
        saved = bool(unreal.EditorAssetLibrary.save_asset(ASSET_PATH))
    except Exception:
        saved = False

    # THE STATUS NEEDS EVERY WIRE AND THE SAVE. Nothing less is MADE, for the
    # reason the 3 September ruling gave: a status word that can be printed
    # over a half-wired material is not a reading.
    ok = (wired == len(asked) + 1) and saved and default_tex is not None
    _write("skyMaterialStatus=%s skyMaterialPath=%s "
           "skyMaterialWired=%d/%d skyMaterialRefused=%s "
           "skyMaterialDefaultTex=%s skyMaterialSaved=%s "
           "skyMaterialParams=%s,%s skyMaterialLuminanceDefault=%.3f "
           "skyMaterialFlags=%s skyMaterialReturn=%d"
           % ("MADE" if ok else "INCOMPLETE", ASSET_PATH,
              wired, len(asked) + 1,
              ";".join(refused) if refused else "none/0-of-3-refused",
              default_from.replace(" ", "~"), "yes" if saved else "NO",
              TEXTURE_PARAM, SCALAR_PARAM, SCALAR_DEFAULT,
              "/".join(flags), 0 if ok else 2))
    return 0 if ok else 2


def selftest():
    """ACCEPTING CASE FIRST, and the accepting fixture is the live codebase:
    the names this script writes must be the names the C++ sets, and the C++
    is the file that cannot be compiled here. The rejecting fixture is
    synthetic, a parameter name that exists nowhere, so that doing the work
    this tool prompts can never break the tool."""
    here = os.path.dirname(os.path.abspath(__file__))
    cpp = os.path.normpath(os.path.join(here, "..", "..", "ue-probe", "Source",
                                        "LedgerProbe", "Private",
                                        "VignetteShot.cpp"))
    fails = []
    checks = 0
    try:
        with open(cpp, "r", encoding="utf-8") as f:
            src = f.read()
    except OSError as e:
        print("make_sky_material --selftest: FAIL checks=0 failed=1 :: "
              "cannot read %s (%s)" % (cpp, e))
        return 2
    # The C++ loads the OBJECT path (package.asset), which is the same asset
    # spelled the way LoadObject needs it. Asserting the package path alone
    # would pass over a C++ file that named a different asset in that package.
    for name in (TEXTURE_PARAM, SCALAR_PARAM, ASSET_PATH + "." + ASSET):
        checks += 1
        if ('"%s"' % name) not in src and ('TEXT("%s")' % name) not in src:
            fails.append("%s is not spelled in VignetteShot.cpp" % name)
    checks += 1
    if 'TEXT("NoSuchSkyParameter")' in src:
        fails.append("the rejecting fixture leaked into the C++")
    checks += 1
    if len(FLAGS) != 3:
        fails.append("FLAGS is %d entries, the verdict prints three"
                     % len(FLAGS))
    print("make_sky_material --selftest: %s checks=%d failed=%d%s"
          % ("PASS" if not fails else "FAIL", checks, len(fails),
             "" if not fails else " :: " + "; ".join(fails)))
    return 0 if not fails else 2


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    # sys.exit is not called on the editor path, for make_base_material.py's
    # reason: raising SystemExit through an embedded interpreter is a
    # plausible way to turn a successful script into a non-zero process.
    main()
