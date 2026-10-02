# The jacket arranged on the stock man (whose arrangement points our MetaHuman bodies cannot get by script), then
# the stock man replaced by our own body before any simulation, the arranged pieces left where they are; exported
# to see that one avatar remains and the pieces stayed. Settings from F:\LedgerTools\tmp\clothes\md\drape.json, the
# body from its "body" entry.
import json, os, time
C = json.load(open(r"F:\LedgerTools\tmp\clothes\md\drape.json"))
LUKA = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Avatar\Male\MV2.1_Luka.avt"
FAB = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Fabric"
utility_api.NewProject()
# the stock man enlarged (C["lukaScale"]) so the shells his arrangement points place the pieces on clear our body
# (a bigger man than he is): Marvelous ignores the offset that would set a piece's distance from the body
# (SetArrangementPosition moved nothing; research MD-LAPEL-FOLD-TURNED-2026-10-02.md)
lo = ApiTypes.ImportExportOption()
lo.scale = float(C.get("lukaScale", 1.0))
import_api.ImportAvatar(LUKA, lo)
pattern_api.ImportPatternJSON(C["sewn"])
arr = {a["ArrangementName"]: int(a["ArrangementIndex"]) for a in pattern_api.GetArrangementList()}
names = {pattern_api.GetPatternPieceName(i): i for i in range(pattern_api.GetPatternCount())}
for key, pt in C["place"].items():
    pattern_api.SetArrangement(names[key], arr[pt])
for key, o in C.get("orient", {}).items():
    pattern_api.SetArrangementOrientation(names[key], int(o))
for key, z in C.get("z", {}).items():
    a = pattern_api.GetArrangementOfPattern(names[key])
    pattern_api.SetArrangementPosition(names[key], int(a["ArrangementOffsetX"]), int(a["ArrangementOffsetY"]), int(z))
# the offsets take effect only when the pieces are placed again (setting them alone moved nothing before the swap)
for key, pt in C["place"].items():
    pattern_api.SetArrangement(names[key], arr[pt])
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = True
if C.get("lookBefore"):
    export_api.ExportOBJ(C["out"].replace(".obj", "-onluka.obj"), eo)
opt = ApiTypes.ImportExportOption()
opt.bAdd = False
opt.bMoveGarment = False
opt.bAutoTranslate = False
opt.bAddArrangementPoints = False
opt.bAutoCreateFittingSuit = False
opt.bSizeAndPoseFromAvatar = False
opt.scale = float(C.get("bodyScale", 10.0))   # the body FBX is in centimetres; replacing the stock man, Marvelous read it as millimetres
print("SWAP", import_api.ImportFBX(C["body"], opt))
print("SHOWN", [utility_api.IsShowAvatar(i) for i in range(2)])
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = True
print("EXPORT", export_api.ExportOBJ(C["out"].replace(".obj", "-swapped.obj"), eo))
