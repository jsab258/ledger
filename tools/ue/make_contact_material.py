"""Make /Game/Ledger/M_LedgerContact, the floor's shine taken away under a sole, as a projected decal, from a script.
    Called from tools/ue/make_base_material.py main(), after the stain, as the wet and the stain are; or on its own:
    UnrealEditor-Cmd ue-probe/LedgerProbe.uproject -run=pythonscript -script=tools/ue/make_contact_material.py
    python tools/ue/make_contact_material.py --selftest    # runs without Unreal

WHY, 30 October 2026 (his order C9, Tom's boots; a fresh reviewer: a pale band under both soles on the wet paving):
the reflection a wet floor shows under a sole is the sole's own underside, which the camera never sees, and the
street's software Lumen does not trace skinned meshes, so it shows the sky there instead
(tools/meshgen/blender/sole_footprints.py has the reading). Where a sole stands, the floor beneath it is shut off from
the sky: so the game lays this decal under each half of each sole (ue-probe LedgerGarments.h, "contact"), and it
writes Specular 0 there (the engine's DBuffer carries Specular with Roughness: DBufferDecalShared.ush), soft at its rim.

WHAT IT WRITES, through the decal's opacity (a rounded oblong in the decal's own square, full in the middle and
falling to nothing at its edge over the outer RIM of it, times ContactStrength): Specular ContactSpecular (default 0)
and Roughness ContactRoughness (the DBuffer writes the two together; 0.6, so what shine is left is dull). No colour,
no normal: the floor's own colour and grain stay under it.
"""
import os
import sys

PACKAGE = "/Game/Ledger"
ASSET = "M_LedgerContact"
ASSET_PATH = PACKAGE + "/" + ASSET
STRENGTH_PARAM, STRENGTH_DEFAULT = "ContactStrength", 1.0
SPEC_PARAM, SPEC_DEFAULT = "ContactSpecular", 0.0
ROUGH_PARAM, ROUGH_DEFAULT = "ContactRoughness", 0.6
CORNER = 0.5     # the oblong's corner radius, as a share of each half-side: a sole's rounded outline
RIM = 0.35       # the share of each half-side over which the opacity falls to nothing
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


def contact_line(status, wired, asked, flags, saved):
    return ("contactMaterialStatus=%s contactMaterialPath=%s contactMaterialWired=%d/%d contactMaterialSaved=%s contactMaterialFlags=%s"
            % (status, ASSET_PATH, wired, asked, "yes" if saved else "no", "+".join(flags) or "none"))


def opacity_at(x, y):
    """The mask the graph draws, in Python, at a point of the decal's square (0..1 each way): for the selftest."""
    qx, qy = abs(x - 0.5) * 2.0, abs(y - 0.5) * 2.0
    dx, dy = max(qx - (1.0 - CORNER), 0.0), max(qy - (1.0 - CORNER), 0.0)
    d = (dx * dx + dy * dy) ** 0.5 / CORNER                     # 1 on the corner's arc
    edge = max(d, max(qx, qy))                                  # and on the straight sides
    return min(max((1.0 - edge) / RIM, 0.0), 1.0) * STRENGTH_DEFAULT


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
    X = unreal
    if unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH):
        unreal.EditorAssetLibrary.delete_asset(ASSET_PATH)
    mat = tools.create_asset(ASSET, PACKAGE, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        _write(contact_line("CREATE-FAILED", 0, 1, [], False))
        return 2
    flags = ["%s=%s" % (p, _set_enum(unreal, mat, p, e, v)) for p, e, v in FLAGS]

    def node(cls, x, y, **props):
        n = mel.create_material_expression(mat, cls, x, y)
        for k, v in props.items():
            n.set_editor_property(k, v)
        return n
    uv = node(X.MaterialExpressionTextureCoordinate, -1500, 0)
    centred = node(X.MaterialExpressionSubtract, -1350, 0, const_b=0.5)          # uv - 0.5
    absd = node(X.MaterialExpressionAbs, -1220, 0)
    q = node(X.MaterialExpressionMultiply, -1100, 0, const_b=2.0)                # 0 middle, 1 edge, each way
    inner = node(X.MaterialExpressionSubtract, -980, 0, const_b=1.0 - CORNER)
    clampd = node(X.MaterialExpressionMax, -860, 0, const_b=0.0)
    length = node(X.MaterialExpressionLength, -740, 0)
    d = node(X.MaterialExpressionDivide, -620, 0, const_b=CORNER)              # 1 on the rounded edge
    # in the oblong's straight middles the corner's distance is nil, so the edge is also the larger of q's two parts
    qx = node(X.MaterialExpressionComponentMask, -980, 200, r=True, g=False, b=False, a=False)
    qy = node(X.MaterialExpressionComponentMask, -980, 320, r=False, g=True, b=False, a=False)
    qmax = node(X.MaterialExpressionMax, -860, 260)
    edge = node(X.MaterialExpressionMax, -500, 100)
    one_minus = node(X.MaterialExpressionOneMinus, -380, 100)
    ramp = node(X.MaterialExpressionDivide, -260, 100, const_b=RIM)
    sat = node(X.MaterialExpressionSaturate, -140, 100)
    strength = node(X.MaterialExpressionScalarParameter, -260, 300, parameter_name=STRENGTH_PARAM, default_value=STRENGTH_DEFAULT)
    opacity = node(X.MaterialExpressionMultiply, -20, 150)
    spec = node(X.MaterialExpressionScalarParameter, -260, 450, parameter_name=SPEC_PARAM, default_value=SPEC_DEFAULT)
    rough = node(X.MaterialExpressionScalarParameter, -260, 600, parameter_name=ROUGH_PARAM, default_value=ROUGH_DEFAULT)
    links = [(uv, "", centred, "A"), (centred, "", absd, ""), (absd, "", q, "A"), (q, "", inner, "A"),
             (inner, "", clampd, "A"), (clampd, "", length, ""), (length, "", d, "A"),
             (q, "", qx, ""), (q, "", qy, ""), (qx, "", qmax, "A"), (qy, "", qmax, "B"),
             (d, "", edge, "A"), (qmax, "", edge, "B"), (edge, "", one_minus, ""), (one_minus, "", ramp, "A"),
             (ramp, "", sat, ""), (sat, "", opacity, "A"), (strength, "", opacity, "B")]
    wired = 0
    for a, out_name, b, in_name in links:
        try:
            if mel.connect_material_expressions(a, out_name, b, in_name):
                wired += 1
        except Exception:
            pass
    for src, prop in ((spec, unreal.MaterialProperty.MP_SPECULAR),
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
    _write(contact_line("MADE" if ok else "INCOMPLETE", wired, asked, flags, saved))
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
    line = contact_line("MADE", 21, 21, ["material_domain=taken"], True)
    check("the line carries its wired denominator", "contactMaterialWired=21/21" in line, line)
    check("and names the asset the game loads", "contactMaterialPath=/Game/Ledger/M_LedgerContact" in line)
    check("full under the sole's middle", abs(opacity_at(0.5, 0.5) - 1.0) < 1e-9)
    check("nothing at the decal's edge, so no line on the floor", opacity_at(0.0, 0.5) == 0.0 and opacity_at(0.5, 1.0) == 0.0)
    check("nothing in a corner (the oblong is rounded, as a sole is)", opacity_at(0.02, 0.02) == 0.0)
    check("still full a little inside the rim", abs(opacity_at(0.5, 0.5 + 0.5 * (1.0 - RIM) - 0.01) - 1.0) < 1e-9)
    check("the floor's shine is shut off, not dulled only (Specular 0: F0 0, no grazing reflection)", SPEC_DEFAULT == 0.0)
    print("make_contact_material selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    try:
        import unreal  # noqa: F401
        main()
    except ImportError:
        print(__doc__)
