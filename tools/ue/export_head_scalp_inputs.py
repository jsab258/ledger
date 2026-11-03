"""Tom's head skin material's parameters read, and the two pictures his scalp paint starts from exported (nothing changed).

    UnrealEditor-Cmd <full path>/ue-probe/LedgerProbe.uproject -run=pythonscript -script=<full path>/tools/ue/export_head_scalp_inputs.py -EnablePlugins=PythonScriptPlugin -unattended -nopause -nosplash -stdout

3 November (his ruling of that day, hair, 3: paint the scalp under Tom's hair in his hair's colour): his near head material takes its
base colour from "Basecolor Baked" (T_Head_LOD1_BC, the MetaHuman Character plugin's bake), and the plugin's own skin accent
regions mark the scalp (T_SkinAccentRegions_002, its fourth channel). Both are written to F:/LedgerTools/tmp/scalp as TGA;
tools/meshgen/tom_scalp_paint.py reads copies kept in F:/LedgerTools/bodies/MH_TomL1/scalp-inputs."""
import os
import unreal

OUT = "F:/LedgerTools/tmp/scalp"
os.makedirs(OUT, exist_ok=True)
lines = []
mel = unreal.MaterialEditingLibrary
for mi_path in ("/Game/Ledger/MetaHumans/MH_TomL1/Face/Materials/MI_Face_Skin_Baked_LOD1",
                "/Game/Ledger/MetaHumans/MH_TomL1/Face/Materials/MI_Face_Skin_Baked_LOD5to7"):
    mi = unreal.load_asset(mi_path)
    if mi is None:
        lines.append("MISSING " + mi_path)
        continue
    lines.append("== " + mi_path + " parent=" + str(mi.get_editor_property("parent").get_path_name() if mi.get_editor_property("parent") else None))
    for n in mel.get_texture_parameter_names(mi):
        v = mel.get_material_instance_texture_parameter_value(mi, n)
        lines.append("  tex %s = %s" % (n, v.get_path_name() if v else None))
    for n in mel.get_scalar_parameter_names(mi):
        lines.append("  scalar %s = %s" % (n, mel.get_material_instance_scalar_parameter_value(mi, n)))
    for n in mel.get_vector_parameter_names(mi):
        lines.append("  vector %s = %s" % (n, mel.get_material_instance_vector_parameter_value(mi, n)))
for tex in ("/Game/Ledger/MetaHumans/MH_TomL1/Face/Baked/T_Head_LOD1_BC",
            "/MetaHumanCharacter/Lookdev_UHM/Skin/Textures/T_SkinAccentRegions_001",
            "/MetaHumanCharacter/Lookdev_UHM/Skin/Textures/T_SkinAccentRegions_002",
            "/MetaHumanCharacter/Lookdev_UHM/Skin/Textures/T_BakedGroomDefault"):
    a = unreal.load_asset(tex)
    if a is None:
        lines.append("MISSING " + tex)
        continue
    t = unreal.AssetExportTask()
    t.object = a
    t.filename = OUT + "/" + tex.rsplit("/", 1)[1] + ".tga"
    t.automated = True
    t.prompt = False
    t.replace_identical = True
    ok = unreal.Exporter.run_asset_export_task(t)
    lines.append("export %s ok=%s size=%sx%s" % (tex, ok, a.blueprint_get_size_x(), a.blueprint_get_size_y()))
open(OUT + "/inspect.txt", "w").write("\n".join(lines) + "\n")
print("scalpInspect done lines=%d" % len(lines))
