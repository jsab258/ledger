"""Read-only numbers for item n09-6's resizing verdict: what Epic's resizing already puts on each built MetaHuman.

    UnrealEditor-Cmd.exe C:/LedgerTools/mh-assemble/MHAssemble.uproject -run=pythonscript
        -script=C:/Users/Jafar/ledger-local/tools/ue/resize_probe.py -unattended -nosplash

WHY, 11 November. Every built cast member carries <name>_Outfits: Epic's default garment (the white base
layer), fitted to that body by the outfit pipeline at build time (MetaHumanOutfitEditorPipeline.cpp). Its
cost and make-up are the resizing route's real numbers on our bodies, beside our own skinned garments.
Writes resize-probe.json beside the project; saves nothing.
"""
import json
import os

MESHES = [
    "/Game/Ledger/MetaHumans/MH_TomL1/Clothing/MH_TomL1_Outfits",
    "/Game/Ledger/MetaHumans/MH_TomL1/Clothing/MH_TomL1_Outfits_2",
    "/Game/Ledger/MetaHumans/MH_Test/Clothing/MH_Test_Outfits",
    "/Game/Ledger/MetaHumans/MH_LenaS4/Clothing/MH_LenaS4_Outfits",
    "/Game/Ledger/MetaHumans/MH_RoccoP2/Clothing/MH_RoccoP2_Outfits",
    "/Game/Ledger/MetaHumans/Garments/TomJeans/SKM_TomJeans",
    "/Game/Ledger/MetaHumans/Garments/TomBoots/SKM_TomBoots",
    "/Game/Ledger/MetaHumans/Garments/TomJumper/SKM_TomJumper",
    "/Game/Ledger/MetaHumans/Garments/TomZipJacket/SKM_TomZipJacket",
]


def describe(unreal, path):
    a = unreal.load_asset(path)
    if a is None:
        return {"path": path, "loaded": False}
    d = {"path": path, "loaded": True, "class": a.get_class().get_name()}
    try:
        d["diskBytes"] = os.path.getsize(unreal.SystemLibrary.convert_to_absolute_path(
            unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir()
                                                        + path.replace("/Game/", "") + ".uasset")))
    except Exception as e:
        d["diskBytes"] = "error: %s" % e
    if isinstance(a, unreal.SkeletalMesh):
        lods = []
        try:
            sms = unreal.get_editor_subsystem(unreal.SkeletalMeshEditorSubsystem)
        except Exception:
            sms = None
        try:
            n = len(a.get_editor_property("lod_info"))
        except Exception:
            n = None
        d["lods"] = n
        for i in range(n or 0):
            row = {"lod": i}
            try:
                row["verts"] = sms.get_num_verts(a, i) if sms else "no-subsystem"
            except Exception as e:
                row["verts"] = "n/a: %s" % e
            try:
                row["sections"] = sms.get_num_sections(a, i) if sms else "no-subsystem"
            except Exception as e:
                row["sections"] = "n/a"
            lods.append(row)
        d["lodRows"] = lods
        try:
            d["materials"] = [str(m.get_editor_property("material_slot_name")) for m in a.get_editor_property("materials")]
        except Exception as e:
            d["materials"] = "error: %s" % e
        try:
            d["clothingAssets"] = len(a.get_editor_property("mesh_clothing_assets") or [])
        except Exception as e:
            d["clothingAssets"] = "error: %s" % e
        try:
            d["morphTargets"] = len(a.get_all_morph_target_names())
        except Exception:
            d["morphTargets"] = "n/a"
        try:
            b = a.get_bounds()
            d["boundsCm"] = [round(b.box_extent.x * 2, 1), round(b.box_extent.y * 2, 1), round(b.box_extent.z * 2, 1)]
        except Exception:
            pass
        try:
            d["resourceKB"] = round(a.get_resource_size_bytes(unreal.ResourceSizeMode.EXCLUSIVE) / 1024)
        except Exception:
            pass
    try:
        refs = unreal.EditorAssetLibrary.find_package_referencers_for_asset(path, False)
        d["referencers"] = list(refs)[:8]
    except Exception:
        pass
    return d


def main():
    import unreal
    out = os.path.join(unreal.Paths.project_dir(), "resize-probe.json")
    rows = [describe(unreal, p) for p in MESHES]
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
    print("resizeProbe written=%s meshes=%d loaded=%d" % (out, len(rows), sum(1 for r in rows if r.get("loaded"))))


main()
