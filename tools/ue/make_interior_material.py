"""Make /Game/Ledger/M_LedgerInterior, a shop's room seen through its window, from a script.

    Called from tools/ue/make_base_material.py main(), as make_glass_material.py is,
    or on its own:  UnrealEditor-Cmd.exe <project> -run=pythonscript -script=tools/ue/make_interior_material.py -EnablePlugins=PythonScriptPlugin
    python tools/ue/make_interior_material.py --selftest    # without Unreal

WHY, 1 October (item 2a). Jafar: "the shop windows are black voids in every
view ... fake interiors in the shop windows by interior mapping, as games do
it". The method (production/research/shop-window-interiors/NOTE.md): each
shop's room is one perspective picture rendered from in front of its window
(tools/art-recipes/shop-room.py), and this material, on the card behind the
glass, finds for every pixel where the eye's line meets the room's box behind
the card and looks that point up in the picture by the render's own rule
(production/specs/shop-interiors.json, "camera"), so the room shows depth as
the player walks past.

UNREAL IS LEFT-HANDED (x forward, y right, z up): standing on the pavement
and looking into an east-side room (+y), the viewer's right is -x, so the
picture's left edge is at the card's HIGH x. The first trial had it the other
way and showed the pawnbroker's room mirror-imaged, its counter notice
reading backwards (1 October); the self-test now checks the notice's side.

THE POSITIONS ARE MADE RELATIVE OUTSIDE THE CODE: the pixel's and the
camera's world positions minus the card's corner, by ordinary material nodes,
so the large-world double precision of UE 5 stays out of the HLSL.

Parameters (set per shop by the game, LedgerInteriors in VignetteShot.cpp):
CardOrigin (the card's front corner in world centimetres: low x, front y, bottom
z), RoomSize (W, H, D in cm), CamD (the render's distance in cm), Side (+1
when the room goes back along +Y, -1 along -Y), DayTex, LitTex, DarkTex (the
three pictures), Night (0 by day, 1 at night), LitOn (1 when the shop is lit
at night) and Brightness (the emissive scale).

IT CANNOT TAKE THE MATERIAL RUN DOWN: it appends one line to ue-material.txt
and its caller catches anything it raises.
"""
import os
import sys

PACKAGE = "/Game/Ledger"
ASSET = "M_LedgerInterior"
ASSET_PATH = PACKAGE + "/" + ASSET

HLSL = r"""
float3 dir = normalize(P - C);
float W = Size.x, H = Size.y, D = Size.z;
float3 o = float3(Side > 0 ? W - P.x : P.x, P.z, P.y * Side);
float3 v = float3(-dir.x * Side, dir.z, dir.y * Side);
float tx = v.x > 0 ? (W - o.x) / v.x : (0 - o.x) / min(v.x, -1e-5);
float ty = v.y > 0 ? (H - o.y) / v.y : (0 - o.y) / min(v.y, -1e-5);
float tz = (D - o.z) / max(v.z, 1e-5);
float t = max(0, min(min(tx, ty), tz));
float3 h = o + v * t;
float s = CamD / (CamD + max(h.z, 0));
float u = 0.5 + (h.x / W - 0.5) * s;
float w = 0.5 + (h.y / H - 0.5) * s;
return float2(u, 1 - w);
"""


def project(x, y, z, w, h, d):
    """The render's rule, as tools/art-recipes/shop-room.py: room point to picture (u, v up)."""
    return 0.5 + (x / w) * d / (d + y), 0.5 + ((z - h / 2.0) / h) * d / (d + y)


def trace(p, c, size, camd, side=1):
    """The HLSL above in Python, for the self-test: picture (u, v down) for a card point p seen from c."""
    import math
    dx, dy, dz = p[0] - c[0], p[1] - c[1], p[2] - c[2]
    n = math.sqrt(dx * dx + dy * dy + dz * dz)
    dx, dy, dz = dx / n, dy / n, dz / n
    W, H, D = size
    o = ((W - p[0] if side > 0 else p[0]), p[2], p[1] * side)
    v = (-dx * side, dz, dy * side)
    tx = (W - o[0]) / v[0] if v[0] > 0 else (0 - o[0]) / min(v[0], -1e-5)
    ty = (H - o[1]) / v[1] if v[1] > 0 else (0 - o[1]) / min(v[1], -1e-5)
    tz = (D - o[2]) / max(v[2], 1e-5)
    t = max(0.0, min(tx, ty, tz))
    hx, hy, hz = o[0] + v[0] * t, o[1] + v[1] * t, o[2] + v[2] * t
    s = camd / (camd + max(hz, 0.0))
    return 0.5 + (hx / W - 0.5) * s, 1 - (0.5 + (hy / H - 0.5) * s)


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_interior_material selftest FAIL " + name)
    W, H, D, d = 530.0, 240.0, 450.0, 530.0
    # From the render's own camera (centre line, d in front), a card point shows
    # exactly the picture's pixel behind it: the projection is the identity there.
    # On an east card the viewer's left is the card's high x (Unreal is left-handed).
    cam = (W / 2, -d, H / 2)
    for (px, pz) in ((50.0, 30.0), (265.0, 120.0), (480.0, 200.0)):
        u, v = trace((px, 0.0, pz), cam, (W, H, D), d)
        check("from the render's camera, card point %s,%s shows itself" % (px, pz), abs(u - (1 - px / W)) < 1e-6 and abs(v - (1 - pz / H)) < 1e-6)
    # The picture's left (u near 0) is at the viewer's left: high x on an east card, low x on a west one.
    u_hi, _ = trace((W - 20.0, 0.0, 100.0), cam, (W, H, D), d)
    u_lo_w, _ = trace((20.0, 0.0, 100.0), (W / 2, d, H / 2), (W, H, D), d, side=-1)
    check("the picture's left at the viewer's left on both sides", u_hi < 0.1 and u_lo_w < 0.1)
    # Looking square on through the card's centre lands on the back wall's centre.
    u, v = trace((W / 2, 0.0, H / 2), (W / 2, -150.0, H / 2), (W, H, D), d)
    check("square through the centre, the back wall's centre", abs(u - 0.5) < 1e-6 and abs(v - 0.5) < 1e-6)
    # The same room point projects the same by the Python and by the render rule.
    pu, pv = project(-W / 2, D, H, W, H, d)
    check("the render rule's back-wall corner", abs(pu - (0.5 - 0.5 * d / (d + D))) < 1e-9)
    # A west-side card (side -1) is seen from the other side of the road, so the
    # room's left is at the card's low x: 10 cm from the viewer's left is the
    # same picture point on either side of the street.
    u_e, v_e = trace((W - 10.0, 0.0, 100.0), (W / 2, -d, H / 2), (W, H, D), d, side=1)
    u_w, v_w = trace((10.0, 0.0, 100.0), (W / 2, d, H / 2), (W, H, D), d, side=-1)
    check("a west card measured from the viewer's left matches the east", abs(u_e - u_w) < 1e-6 and abs(v_e - v_w) < 1e-6)
    print("make_interior_material selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main():
    import unreal
    root = unreal.Paths.project_dir()
    note = []
    try:
        tools = unreal.AssetToolsHelpers.get_asset_tools()
        mel = unreal.MaterialEditingLibrary
        if unreal.EditorAssetLibrary.does_asset_exist(ASSET_PATH):
            unreal.EditorAssetLibrary.delete_asset(ASSET_PATH)
        m = tools.create_asset(ASSET, PACKAGE, unreal.Material, unreal.MaterialFactoryNew())
        m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)

        def node(cls, x, y):
            return mel.create_material_expression(m, cls, x, y)

        wpos = node(unreal.MaterialExpressionWorldPosition, -1400, 0)
        cpos = node(unreal.MaterialExpressionCameraPositionWS, -1400, 120)
        origin = node(unreal.MaterialExpressionVectorParameter, -1400, 240)
        origin.set_editor_property("parameter_name", "CardOrigin")
        p_rel = node(unreal.MaterialExpressionSubtract, -1150, 0)
        c_rel = node(unreal.MaterialExpressionSubtract, -1150, 120)
        mel.connect_material_expressions(wpos, "", p_rel, "A")
        mel.connect_material_expressions(origin, "", p_rel, "B")
        mel.connect_material_expressions(cpos, "", c_rel, "A")
        mel.connect_material_expressions(origin, "", c_rel, "B")
        size = node(unreal.MaterialExpressionVectorParameter, -1150, 260)
        size.set_editor_property("parameter_name", "RoomSize")
        size.set_editor_property("default_value", unreal.LinearColor(530.0, 240.0, 450.0, 0.0))
        camd = node(unreal.MaterialExpressionScalarParameter, -1150, 380)
        camd.set_editor_property("parameter_name", "CamD")
        camd.set_editor_property("default_value", 530.0)
        side = node(unreal.MaterialExpressionScalarParameter, -1150, 460)
        side.set_editor_property("parameter_name", "Side")
        side.set_editor_property("default_value", 1.0)
        # float3 views of the relative positions and the size (masks drop LWC and alpha)
        def rgb(src, x, y):
            mk = node(unreal.MaterialExpressionComponentMask, x, y)
            for ch in ("r", "g", "b"):
                mk.set_editor_property(ch, True)
            mk.set_editor_property("a", False)
            mel.connect_material_expressions(src, "", mk, "")
            return mk
        p3, c3, s3 = rgb(p_rel, -950, 0), rgb(c_rel, -950, 120), rgb(size, -950, 260)
        custom = node(unreal.MaterialExpressionCustom, -700, 100)
        custom.set_editor_property("code", HLSL)
        custom.set_editor_property("output_type", unreal.CustomMaterialOutputType.CMOT_FLOAT2)
        custom.set_editor_property("description", "Interior")
        ins = []
        for name in ("P", "C", "Size", "CamD", "Side"):
            ci = unreal.CustomInput()
            ci.set_editor_property("input_name", name)
            ins.append(ci)
        custom.set_editor_property("inputs", ins)
        mel.connect_material_expressions(p3, "", custom, "P")
        mel.connect_material_expressions(c3, "", custom, "C")
        mel.connect_material_expressions(s3, "", custom, "Size")
        mel.connect_material_expressions(camd, "", custom, "CamD")
        mel.connect_material_expressions(side, "", custom, "Side")
        samples = {}
        for k, name in enumerate(("DayTex", "LitTex", "DarkTex")):
            t = node(unreal.MaterialExpressionTextureSampleParameter2D, -400, -150 + 220 * k)
            t.set_editor_property("parameter_name", name)
            mel.connect_material_expressions(custom, "", t, "UVs")
            samples[name] = t
        lit_on = node(unreal.MaterialExpressionScalarParameter, -150, 300)
        lit_on.set_editor_property("parameter_name", "LitOn")
        night = node(unreal.MaterialExpressionScalarParameter, 50, 300)
        night.set_editor_property("parameter_name", "Night")
        bright = node(unreal.MaterialExpressionScalarParameter, 250, 300)
        bright.set_editor_property("parameter_name", "Brightness")
        bright.set_editor_property("default_value", 1.0)
        night_mix = node(unreal.MaterialExpressionLinearInterpolate, -150, 150)
        mel.connect_material_expressions(samples["DarkTex"], "RGB", night_mix, "A")
        mel.connect_material_expressions(samples["LitTex"], "RGB", night_mix, "B")
        mel.connect_material_expressions(lit_on, "", night_mix, "Alpha")
        day_night = node(unreal.MaterialExpressionLinearInterpolate, 50, 0)
        mel.connect_material_expressions(samples["DayTex"], "RGB", day_night, "A")
        mel.connect_material_expressions(night_mix, "", day_night, "B")
        mel.connect_material_expressions(night, "", day_night, "Alpha")
        scaled = node(unreal.MaterialExpressionMultiply, 250, 0)
        mel.connect_material_expressions(day_night, "", scaled, "A")
        mel.connect_material_expressions(bright, "", scaled, "B")
        mel.connect_material_property(scaled, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
        mel.recompile_material(m)
        unreal.EditorAssetLibrary.save_loaded_asset(m, only_if_is_dirty=False)
        note.append("interiorMaterialStatus=MADE interiorMaterial=%s" % ASSET_PATH)
    except Exception as e:
        note.append("interiorMaterialStatus=RAISED interiorMaterialNote=%s" % str(e).replace(" ", "~")[:200])
    with open(os.path.join(root, "ue-material.txt"), "a", encoding="utf-8") as f:
        f.write(" ".join(note) + "\n")
    print("make_interior_material: " + " ".join(note))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
