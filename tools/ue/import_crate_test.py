"""Import the texturing test's crate twice, as it comes and repainted, for one-run films (12 Nov 2026).

    UnrealEditor-Cmd.exe C:/Users/Jafar/ledger-local/ue-probe/LedgerProbe.uproject -run=pythonscript
        -script="C:/Users/Jafar/ledger-local/tools/ue/import_crate_test.py"
        -EnablePlugins=PythonScriptPlugin -unattended -nopause -nosplash -stdout
    python tools/ue/import_crate_test.py --selftest      # without Unreal: the source files are there

WHY: the texturing test (production/research/texture-pipeline/VERDICT-2026-11-11.md, "The crate's offline
chain") ends with the crate in the game beside the scan as it comes. One mesh, the Megascans Industrial Junkyard
Crate Metal from his Fab download (Epic's own content, allowed in the game: RULINGS 13 Oct), two materials:
  CrateScan    the scan's own maps cut to 1024 px (base colour, normal, roughness, AO)
  CrateRepaint TextureCraft's dull green paint over the scan, Unreal packed (base colour, normal, ORM)
Each lands at /Game/Ledger/Test/<Name>/SM_<Name>, which the game's -PropTest=<Name>@x,z,yaw stands on the
pavement for one run (VignetteShot.cpp). Nothing in the street file names them; they leave with the test.

Scale 1, Nanite off, one box of collision (a medium prop's floor). The scan's normal map is taken as DirectX
(Unreal's own convention, as Fab's Unreal exports come): UNVERIFIED; a reviewer seeing light from below on the
ribs means flip it (FLIP_SCAN_GREEN). Writes ONE LINE to ue-material.txt beside the project:
    crateTest=OK|FAIL scan=<path> repaint=<path> tris=<n> size_cm=<x,y,z> nanite=off ...
"""
import os
import sys

SRC = "F:/LedgerTools/texture-tools/crate"
FBX = SRC + "/in/crate.fbx"
FLIP_SCAN_GREEN = False
VARIANTS = {
    "CrateScan": {
        "BaseColor": SRC + "/as-it-comes/BaseColor.png",
        "Normal": SRC + "/as-it-comes/Normal.png",
        "Roughness": SRC + "/as-it-comes/Roughness.png",
        "AO": SRC + "/as-it-comes/AO.png",
    },
    "CrateRepaint": {
        "BaseColor": SRC + "/out1024/T_CrateRepaint_BaseColor.png",
        "Normal": SRC + "/out1024/T_CrateRepaint_Normal.png",
        "ORM": SRC + "/out1024/T_CrateRepaint_OcclusionRoughnessMetallic.png",
    },
}


def selftest():
    missing = [p for p in [FBX] + [f for v in VARIANTS.values() for f in v.values()] if not os.path.isfile(p)]
    print("crateTestSelftest=%s missing=%s" % ("PASS" if not missing else "FAIL", missing or "none"))
    return 0 if not missing else 1


def import_texture(unreal, path, dest, name, role):
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", path)
    task.set_editor_property("destination_path", dest)
    task.set_editor_property("destination_name", name)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", False)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    tex = unreal.load_asset(dest + "/" + name)
    if role == "normal":
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
        tex.set_editor_property("srgb", False)
        if FLIP_SCAN_GREEN and "as-it-comes" in path:
            tex.set_editor_property("flip_green_channel", True)
    elif role == "mask":
        tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
        tex.set_editor_property("srgb", False)
    else:
        tex.set_editor_property("srgb", True)
    unreal.EditorAssetLibrary.save_loaded_asset(tex)
    return tex


def make_material(unreal, dest, name, tex):
    mel = unreal.MaterialEditingLibrary
    path = dest + "/M_" + name
    mat = unreal.load_asset(path)
    if mat is None:
        mat = unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_" + name, dest, unreal.Material, unreal.MaterialFactoryNew())
    mel.delete_all_material_expressions(mat)

    def sample(t, y, kind):
        s = mel.create_material_expression(mat, unreal.MaterialExpressionTextureSample, -500, y)
        s.set_editor_property("texture", t)
        s.set_editor_property("sampler_type", kind)
        return s

    S = unreal.MaterialSamplerType
    bc = sample(tex["BaseColor"], -300, S.SAMPLERTYPE_COLOR)
    nm = sample(tex["Normal"], 0, S.SAMPLERTYPE_NORMAL)
    mel.connect_material_property(nm, "RGB", unreal.MaterialProperty.MP_NORMAL)
    if "ORM" in tex:
        orm = sample(tex["ORM"], 300, S.SAMPLERTYPE_MASKS)
        mel.connect_material_property(bc, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)
        mel.connect_material_property(orm, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
        mel.connect_material_property(orm, "G", unreal.MaterialProperty.MP_ROUGHNESS)
        mel.connect_material_property(orm, "B", unreal.MaterialProperty.MP_METALLIC)
    else:
        ro = sample(tex["Roughness"], 300, S.SAMPLERTYPE_LINEAR_COLOR)
        ao = sample(tex["AO"], 600, S.SAMPLERTYPE_LINEAR_COLOR)
        mel.connect_material_property(bc, "RGB", unreal.MaterialProperty.MP_BASE_COLOR)
        mel.connect_material_property(ro, "R", unreal.MaterialProperty.MP_ROUGHNESS)
        mel.connect_material_property(ao, "R", unreal.MaterialProperty.MP_AMBIENT_OCCLUSION)
    mel.recompile_material(mat)
    unreal.EditorAssetLibrary.save_loaded_asset(mat)
    return mat


def import_mesh(unreal, dest, name):
    ui = unreal.FbxImportUI()
    ui.set_editor_property("import_mesh", True)
    ui.set_editor_property("import_as_skeletal", False)
    ui.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
    ui.set_editor_property("import_materials", False)
    ui.set_editor_property("import_textures", False)
    ui.set_editor_property("import_animations", False)
    sm = ui.get_editor_property("static_mesh_import_data")
    sm.set_editor_property("combine_meshes", True)
    sm.set_editor_property("convert_scene", True)
    sm.set_editor_property("generate_lightmap_u_vs", False)
    sm.set_editor_property("auto_generate_collision", False)
    sm.set_editor_property("normal_import_method", unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS)
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", FBX)
    task.set_editor_property("destination_path", dest)
    task.set_editor_property("destination_name", "SM_" + name)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("save", False)
    task.set_editor_property("options", ui)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    return unreal.load_asset(dest + "/SM_" + name)


def main():
    import unreal
    out = os.path.join(unreal.Paths.project_dir(), "ue-material.txt")
    if not os.path.isfile(FBX):
        with open(out, "a", encoding="utf-8") as fh:
            fh.write("crateTest=SKIPPED no-source-on-F\n")
        return
    parts, ok = [], True
    for name, maps in VARIANTS.items():
        dest = "/Game/Ledger/Test/" + name
        try:
            tex = {}
            for role, path in maps.items():
                kind = "normal" if role == "Normal" else ("color" if role == "BaseColor" else "mask")
                tex[role] = import_texture(unreal, path, dest, "T_%s_%s" % (name, role), kind)
            mat = make_material(unreal, dest, name, tex)
            mesh = import_mesh(unreal, dest, name)
            if mesh is None:
                ok = False
                parts.append("%s=MISSING" % name)
                continue
            nan = mesh.get_editor_property("nanite_settings")
            nan.set_editor_property("enabled", False)
            mesh.set_editor_property("nanite_settings", nan)
            for i in range(len(mesh.get_editor_property("static_materials"))):
                mesh.set_material(i, mat)
            b = mesh.get_bounding_box()
            size = [round(b.max.x - b.min.x, 1), round(b.max.y - b.min.y, 1), round(b.max.z - b.min.z, 1)]
            body = mesh.get_editor_property("body_setup")
            if body is not None:
                box = unreal.KBoxElem()
                box.set_editor_property("center", (b.min + b.max) * 0.5)
                box.set_editor_property("x", size[0])
                box.set_editor_property("y", size[1])
                box.set_editor_property("z", size[2])
                agg = body.get_editor_property("agg_geom")
                agg.set_editor_property("box_elems", [box])
                body.set_editor_property("agg_geom", agg)
            unreal.EditorAssetLibrary.save_loaded_asset(mesh)
            unreal.EditorAssetLibrary.save_directory(dest)
            tris = mesh.get_num_triangles(0) if hasattr(mesh, "get_num_triangles") else -1
            parts.append("%s=%s/SM_%s tris=%s size_cm=%s,%s,%s nanite=%s" % (
                name, dest, name, tris, size[0], size[1], size[2],
                "on" if mesh.get_editor_property("nanite_settings").get_editor_property("enabled") else "off"))
        except Exception as e:  # one line, never a silent half
            ok = False
            parts.append("%s=RAISED:%r" % (name, e))
    line = "crateTest=%s %s" % ("OK" if ok else "FAIL", " ".join(parts))
    print(line)
    with open(out, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    main()
