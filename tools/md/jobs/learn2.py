# Learning job 2: how Marvelous sees the avatar; how a seam is written in the pattern file. No dialogs.
import json, os
OUT = r"F:\LedgerTools\tmp\clothes\md\learn2"
os.makedirs(OUT, exist_ok=True)
for name in ("GetAvatarMeasurements", "GetAvatarProperties"):
    f = getattr(utility_api, name)
    try:
        print(name, str(f())[:1500])
    except TypeError as e:
        try:
            print(name, str(f(0))[:1500])
        except Exception as e2:
            print(name, "ERR", e2, "| doc:", (f.__doc__ or "")[:300])
print("ONBODY", str(pattern_api.GetPatternOnBodyDetails.__doc__)[:300])
# two test pieces beside the first, sewn edge to edge by each overload in turn
a = pattern_api.CreatePatternWithPoints([(400.0, 0.0, 0), (700.0, 0.0, 0), (700.0, 500.0, 0), (400.0, 500.0, 0)])
b = pattern_api.CreatePatternWithPoints([(800.0, 0.0, 0), (1100.0, 0.0, 0), (1100.0, 500.0, 0), (800.0, 500.0, 0)])
print("PIECES", a, b, pattern_api.GetPatternCount())
r1 = pattern_api.AddSeamlinePairGroup(a, 1, b, 3, True, False)
print("SEAM6", r1, pattern_api.GetSeamlinePairGroupCount())
pattern_api.ExportPatternJSON(os.path.join(OUT, "seam.json"))
d = json.load(open(os.path.join(OUT, "seam.json"), encoding="utf-8"))
print("SEAMJSON", json.dumps(d.get("SeamLinePairGroupList"))[:3000])
print("ARRMAP", json.dumps([p.get("ArrangementPointDataMap") for p in d["PatternList"]])[:800])
