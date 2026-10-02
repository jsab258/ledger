# Learn whether Marvelous's pattern file can sew an outline edge to an internal line (a pocket flap to its line on
# the front, a button tack between the fronts), and how internal lines are numbered. Safe: no avatar, no dialogs.
import json, os
OUT = r"F:\LedgerTools\tmp\clothes\md\learn5"
utility_api.NewProject()
a = pattern_api.CreatePatternWithPoints([(0.0, 0.0, 0), (300.0, 0.0, 0), (300.0, 500.0, 0), (0.0, 500.0, 0)])
b = pattern_api.CreatePatternWithPoints([(400.0, 0.0, 0), (560.0, 0.0, 0), (560.0, 55.0, 0), (400.0, 55.0, 0)])
k1 = pattern_api.CreateInternalShapeWithPoints(a, [(70.0, 300.0, 0), (230.0, 300.0, 0)], False)
k2 = pattern_api.CreateInternalShapeWithPoints(a, [(50.0, 100.0, 0), (150.0, 120.0, 2), (250.0, 100.0, 0)], False)
print("PIECES", a, b, "INTERNAL", k1, k2)
print("LINEINFO", pattern_api.GetPatternLineInfo(a))
try:
    print("ISHAPES", [(s.name if hasattr(s, "name") else str(s)) for s in utility_api.GetInternalShapeInformation(a)])
except Exception as e:
    print("ISHAPES err", e)
try:
    print("IPOINTS", pattern_api.GetPatternInternalShapePoints(a, 0), pattern_api.GetPatternInternalShapePoints(a, 1))
except Exception as e:
    print("IPOINTS err", e)
pattern_api.ExportPatternJSON(os.path.join(OUT, "before.json"))
