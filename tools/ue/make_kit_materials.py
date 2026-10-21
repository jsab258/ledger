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
PARAMS = ("BaseColor", "Roughness", "Metallic", "Specular", "EmissiveColor", "Opacity")


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


def _make_master(unreal, name, translucent):
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    path = PACKAGE + "/" + name
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        unreal.EditorAssetLibrary.delete_asset(path)
    mat = tools.create_asset(name, PACKAGE, unreal.Material, unreal.MaterialFactoryNew())
    if mat is None:
        return None, 0, 0
    if translucent:
        mat.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
        mat.set_editor_property("translucency_lighting_mode", unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
    asked = []
    y = 0

    def param_vec(pname, default):
        nonlocal y
        e = mel.create_material_expression(mat, unreal.MaterialExpressionVectorParameter, -500, y)
        e.set_editor_property("parameter_name", pname)
        e.set_editor_property("default_value", unreal.LinearColor(default[0], default[1], default[2], 1.0))
        y += 160
        return e

    def param_scalar(pname, default):
        nonlocal y
        e = mel.create_material_expression(mat, unreal.MaterialExpressionScalarParameter, -500, y)
        e.set_editor_property("parameter_name", pname)
        e.set_editor_property("default_value", default)
        y += 120
        return e

    asked.append((param_vec("BaseColor", (0.5, 0.5, 0.5)), unreal.MaterialProperty.MP_BASE_COLOR))
    asked.append((param_scalar("Roughness", 0.6), unreal.MaterialProperty.MP_ROUGHNESS))
    asked.append((param_scalar("Metallic", 0.0), unreal.MaterialProperty.MP_METALLIC))
    asked.append((param_scalar("Specular", 0.5), unreal.MaterialProperty.MP_SPECULAR))
    asked.append((param_vec("EmissiveColor", (0.0, 0.0, 0.0)), unreal.MaterialProperty.MP_EMISSIVE_COLOR))
    if translucent:
        asked.append((param_scalar("Opacity", 0.35), unreal.MaterialProperty.MP_OPACITY))
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
    unreal.EditorAssetLibrary.save_asset(path)
    return mat, wired, len(asked)


def _make_instance(unreal, name, parent, values):
    tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    path = PACKAGE + "/" + name
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        unreal.EditorAssetLibrary.delete_asset(path)
    mi = tools.create_asset(name, PACKAGE, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    if mi is None:
        return False
    mel.set_material_instance_parent(mi, parent)
    for k, v in (values or {}).items():
        if k in ("BaseColor", "EmissiveColor"):
            mel.set_material_instance_vector_parameter_value(mi, k, unreal.LinearColor(v[0], v[1], v[2], 1.0))
        elif k in PARAMS:
            mel.set_material_instance_scalar_parameter_value(mi, k, float(v))
    return bool(unreal.EditorAssetLibrary.save_asset(path))


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
    kinds_made = 0
    kind_assets = {}
    for kind, row in spec["kinds"].items():
        parent = masters.get(row["master"])
        if parent is None:
            continue
        vals = {"Opacity": row["opacity"]} if "opacity" in row else {}
        if _make_instance(unreal, "MI_KitKind_" + kind, parent, vals):
            kinds_made += 1
            kind_assets[kind] = unreal.EditorAssetLibrary.load_asset(PACKAGE + "/MI_KitKind_" + kind)
    slots_made = 0
    for slot, row in slots.items():
        parent = kind_assets.get(row["kind"])
        if parent is not None and _make_instance(unreal, "MI_Kit_" + slot, parent, row["values"]):
            slots_made += 1
    ok = wired_all == asked_all and kinds_made == len(spec["kinds"]) and slots_made == len(slots) and not missing
    _write("kitMaterials=%s masters=%d wired=%d/%d kinds=%d/%d slots=%d/%d missingSlots=%s"
           % ("MADE" if ok else "INCOMPLETE", len([m for m in masters.values() if m]), wired_all, asked_all,
              kinds_made, len(spec["kinds"]), slots_made, len(spec["slots"]), ",".join(missing) or "none"))
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
            print(k, v["kind"], v["from"], {a: (tuple(round(x, 3) for x in b) if isinstance(b, tuple) else round(b, 3)) for a, b in v["values"].items()})
        print("missing:", miss)
        sys.exit(0)
    main()
