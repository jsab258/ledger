# Import the sewn jacket pattern file into a new project and export it again, to see that Marvelous keeps every seam,
# pair and fold (tools/md/write_pattern.py writes it).
import json, os
D = r"F:\LedgerTools\tmp\clothes\md\ron1"
utility_api.NewProject()
ok = pattern_api.ImportPatternJSON(os.path.join(D, "sewn.json"))
pattern_api.ExportPatternJSON(os.path.join(D, "sewn-back.json"))
d = json.load(open(os.path.join(D, "sewn-back.json")))
src = json.load(open(os.path.join(D, "sewn.json")))
print("IMPORT", ok, "patterns", pattern_api.GetPatternCount(), "seam groups", pattern_api.GetSeamlinePairGroupCount())
print("PAIRS", sum(len(g["PairList"]) for g in src["SeamLinePairGroupList"]), "->", sum(len(g["PairList"]) for g in d["SeamLinePairGroupList"]))
print("TURNED", [g["Name"] for g in d["SeamLinePairGroupList"] if g["bIsTurned"]])
print("FOLDS", [(p["Name"], [il["FoldData"]["iAngle"] for il in p["InternalLineList"] if il.get("FoldData") and il["FoldData"]["iAngle"] != 180]) for p in d["PatternList"] if any(il.get("FoldData") and il["FoldData"]["iAngle"] != 180 for il in p["InternalLineList"])])
