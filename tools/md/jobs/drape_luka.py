# The sewn jacket (tools/md/write_pattern.py) arranged on Marvelous's stock man and draped, as the settings file
# F:\LedgerTools\tmp\clothes\md\drape.json says (pattern, export path, steps, particle distance, which pieces are
# fused and strengthened for the first settle, layers, distances off the body). A new project each time.
import json, os, time
C = json.load(open(r"F:\LedgerTools\tmp\clothes\md\drape.json"))
LUKA = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Avatar\Male\MV2.1_Luka.avt"
FAB = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Fabric"
utility_api.NewProject()
import_api.ImportAvatar(C.get("avatar", LUKA), ApiTypes.ImportExportOption())
pattern_api.ImportPatternJSON(C["sewn"])
print("PATTERN", pattern_api.GetPatternCount(), "seams", pattern_api.GetSeamlinePairGroupCount())
arr = {a["ArrangementName"]: int(a["ArrangementIndex"]) for a in pattern_api.GetArrangementList()}
names = {pattern_api.GetPatternPieceName(i): i for i in range(pattern_api.GetPatternCount())}
for key, pt in C["place"].items():
    pattern_api.SetArrangement(names[key], arr[pt])
for key, o in C.get("orient", {}).items():
    pattern_api.SetArrangementOrientation(names[key], int(o))
for key, z in C.get("z", {}).items():
    a = pattern_api.GetArrangementOfPattern(names[key])
    pattern_api.SetArrangementPosition(names[key], int(a["ArrangementOffsetX"]), int(a["ArrangementOffsetY"]), int(z))
shell = fabric_api.AddFabric(os.path.join(FAB, C.get("shell", "V2_Woven_Twill_1.zfab")))
fused = fabric_api.AddFabric(os.path.join(FAB, C.get("fused", "V2_Woven_Canvas_1.zfab")))
for k, i in names.items():
    pattern_api.SetPatternPieceFabricIndex(i, fused if k in C["fusedPieces"] else shell)
    pattern_api.SetPatternLayer(i, int(C.get("layer", {}).get(k, 0)))
for k in C.get("strengthen", []):
    pattern_api.SetPatternStrengthen(names[k], True)
pattern_api.SetParticleDistanceOfPatterns(float(C.get("particle", 20)))
t0 = time.time()
for n, steps in enumerate(C["steps"]):
    if n == C.get("unstrengthenAfter", -1):
        for k in C.get("strengthen", []):
            pattern_api.SetPatternStrengthen(names[k], False)
    if "particleAfter" in C and n == C["particleAfter"][0]:
        pattern_api.SetParticleDistanceOfPatterns(float(C["particleAfter"][1]))
    ok = utility_api.Simulate(int(steps))
    print("SIM", n, steps, ok, round(time.time() - t0, 1))
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = True
print("EXPORT", export_api.ExportOBJ(C["out"], eo))
