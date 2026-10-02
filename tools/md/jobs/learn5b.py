# Import the two hand-made variants of the flap seam and see which one Marvelous keeps (and whether the fold angle
# survives), by exporting again.
import json, os
OUT = r"F:\LedgerTools\tmp\clothes\md\learn5"
for n in (1, 2):
    utility_api.NewProject()
    ok = pattern_api.ImportPatternJSON(os.path.join(OUT, "v%d.json" % n))
    c = pattern_api.GetSeamlinePairGroupCount()
    pattern_api.ExportPatternJSON(os.path.join(OUT, "v%d-back.json" % n))
    d = json.load(open(os.path.join(OUT, "v%d-back.json" % n)))
    print("V", n, ok, "patterns", pattern_api.GetPatternCount(), "seams", c, json.dumps(d.get("SeamLinePairGroupList"))[:600])
    print("   folds", [il.get("FoldData") for il in d["PatternList"][0]["InternalLineList"]])
