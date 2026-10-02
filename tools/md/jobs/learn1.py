# Learning job 1: options and conventions before the jacket.
import inspect, json, os
OUT = r"F:\LedgerTools\tmp\clothes\md\learn1"
os.makedirs(OUT, exist_ok=True)
def attrs(o):
    return {a: repr(getattr(o, a))[:80] for a in dir(o) if not a.startswith("_") and not callable(getattr(o, a))}
for cls in ("ImportExportOption", "ImportZPRJOption", "ExportUSDOption", "MaterialPropertyOptions", "ObjectBrowserContextOptions", "CloApiInternalShape"):
    try:
        o = getattr(ApiTypes, cls)()
        print("OPTION", cls, json.dumps(attrs(o)))
    except Exception as e:
        print("OPTION", cls, "ERR", e)
print("SEAMDOC", pattern_api.AddSeamlinePairGroup.__doc__)
print("ARRDOC", pattern_api.SetArrangementPosition.__doc__, pattern_api.SetPatternPiecePos.__doc__, pattern_api.SetPatternPieceMove.__doc__)
print("VERSION", utility_api.GetMajorVersion(), utility_api.GetMinorVersion(), utility_api.GetPatchVersion())
utility_api.NewProject()
opt = ApiTypes.ImportExportOption()
for a, v in (("bAddArrangementPoints", True), ("bAutoCreateFittingSuit", True)):
    if hasattr(opt, a):
        setattr(opt, a, v)
ok = import_api.ImportFBX(r"F:\LedgerTools\tmp\clothes\md\bodies\MH_RoccoP2_padded.fbx", opt)
print("IMPORT", ok, "avatars", export_api.GetAvatarNameList() if hasattr(export_api, "GetAvatarNameList") else "?")
arr = pattern_api.GetArrangementList()
print("ARRANGEMENTS", len(arr), json.dumps(arr[:60])[:3000])
# one test piece, 300 x 500 mm, with an internal line across it
idx = pattern_api.CreatePatternWithPoints([(0.0, 0.0, 0), (300.0, 0.0, 0), (300.0, 500.0, 0), (0.0, 500.0, 0)])
print("PIECE", idx, pattern_api.GetPatternCount(), pattern_api.GetPatternOutlinePoints(idx) if hasattr(pattern_api, "GetPatternOutlinePoints") else "")
li = pattern_api.CreateInternalShapeWithPoints(idx, [(50.0, 100.0, 0), (250.0, 400.0, 0)], False)
print("INTERNAL", li)
print("BBOX", pattern_api.GetBoundingBoxOfPattern(idx))
print("INFO", str(pattern_api.GetPatternInformation(idx))[:600])
print("LINEINFO", str(pattern_api.GetPatternLineInfo(idx))[:1500])
pattern_api.ExportPatternJSON(os.path.join(OUT, "test.json"))
print("JSONSIZE", os.path.getsize(os.path.join(OUT, "test.json")) if os.path.exists(os.path.join(OUT, "test.json")) else None)
print("MAT", str(utility_api.GetMaterialPropertiesAsJson(0, 0, ApiTypes.ObjectBrowserContextOptions(), ApiTypes.MaterialPropertyOptions()))[:2500])
