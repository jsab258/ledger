# The jacket draped on our own body, run by the bridge (tools/md/md_bridge.py) as the settings file
# F:\LedgerTools\tmp\clothes\md\drape.json says. 2 October, the jacket proof:
#  1. the sewn pattern (tools/md/write_pattern.py) placed on Marvelous's stock man, the only avatar with arrangement
#     points a script can use (research MD-AVATAR-ARRANGEMENT-2026-10-02.md);
#  2. the stock man replaced, before any simulation, by a thinned copy of our body (tools/md/shrink_body.py) that
#     fits inside the placed pieces (the distance a piece sits off the body cannot be set by script);
#  3. draped, then fuller copies swapped in a few millimetres at a time, the cloth settling at each, up to the body
#     itself; the result exported.
import json, os, time
C = json.load(open(r"F:\LedgerTools\tmp\clothes\md\drape.json"))
LUKA = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Avatar\Male\MV2.1_Luka.avt"
FAB = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Fabric"
utility_api.NewProject()
import_api.ImportAvatar(LUKA, ApiTypes.ImportExportOption())
pattern_api.ImportPatternJSON(C["sewn"])
arr = {a["ArrangementName"]: int(a["ArrangementIndex"]) for a in pattern_api.GetArrangementList()}
names = {pattern_api.GetPatternPieceName(i): i for i in range(pattern_api.GetPatternCount())}
for key, pt in C["place"].items():
    pattern_api.SetArrangement(names[key], arr[pt])
for key, o in C.get("orient", {}).items():
    pattern_api.SetArrangementOrientation(names[key], int(o))
shell = fabric_api.AddFabric(os.path.join(FAB, C.get("shell", "V2_Woven_Twill_1.zfab")))
fused = fabric_api.AddFabric(os.path.join(FAB, C.get("fused", "V2_Woven_Canvas_1.zfab")))
for k, i in names.items():
    pattern_api.SetPatternPieceFabricIndex(i, fused if k in C["fusedPieces"] else shell)
    pattern_api.SetPatternLayer(i, int(C.get("layer", {}).get(k, 0)))
pattern_api.SetParticleDistanceOfPatterns(float(C.get("particle", 20)))
# the canvassed pieces held firm (Strengthen; Bond, Marvelous's fused interlining, has no script call)
for k in C.get("strengthen", []):
    pattern_api.SetPatternStrengthen(names[k], True)
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = True


def swap(path):
    opt = ApiTypes.ImportExportOption()
    opt.bAdd = False
    opt.bMoveGarment = False
    opt.bAutoTranslate = False
    opt.bAddArrangementPoints = False
    opt.bAutoCreateFittingSuit = False
    opt.bSizeAndPoseFromAvatar = False      # True (the default) read the incoming body ten times too small
    opt.scale = float(C.get("bodyScale", 10.0))   # the bodies are in centimetres, read as millimetres otherwise
    return import_api.ImportFBX(path, opt)


t0 = time.time()
for n, (body, steps) in enumerate(C["grow"]):
    ok = swap(body)
    # the cloth let slide while the body fills out under it (the avatar's static friction, 0.8 by default, held the
    # fronts in the folds they took on the thinned body)
    if "growFriction" in C:
        utility_api.SetAvatarProperties(0, {"StaticFriction": "%f" % C["growFriction"], "KineticFriction": "%f" % C["growFriction"]})
    if n == 0 and C.get("lookStart"):
        export_api.ExportOBJ(C["out"].replace(".obj", "-start.obj"), eo)
    if "particleAt" in C and n == C["particleAt"][0]:
        pattern_api.SetParticleDistanceOfPatterns(float(C["particleAt"][1]))
    sim = utility_api.Simulate(int(steps))
    print("GROW", n, os.path.basename(body), ok, steps, sim, round(time.time() - t0, 1))
if "settleFriction" in C:
    utility_api.SetAvatarProperties(0, {"StaticFriction": "%f" % C["settleFriction"][0], "KineticFriction": "%f" % C["settleFriction"][1]})
print("AVATAR", utility_api.GetAvatarProperties(0))
# the settle on the full body, each stage [steps, particle distance in mm (0: unchanged)]
for steps, pd in C.get("settle", []):
    if pd:
        pattern_api.SetParticleDistanceOfPatterns(float(pd))
    for k, v in C.get("fine", {}).items():           # finer still where the eye goes (lapels, collar)
        if pd:
            pattern_api.SetParticleDistanceOfPattern(names[k], min(float(pd), float(v)))
    print("SETTLE", steps, pd, utility_api.Simulate(int(steps)), round(time.time() - t0, 1))
print("EXPORT", export_api.ExportOBJ(C["out"], eo))
