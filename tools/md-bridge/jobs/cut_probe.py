# THE CUFFS' THIRD TRY, EPIC'S METHOD, ITS CALLS FIRST (27 October 2026): what CutPatternAlongInternalShapes does with
# its third argument, whether the two halves come back sewn, and where an internal line drawn with
# CreateInternalShapeWithPoints lands in the piece's own coordinates. A 200 x 300 mm piece, no avatar, no drape.
utility_api.NewProject()
out = {}
for sew in (True, False):
    utility_api.NewProject()
    p = pattern_api.CreatePatternWithPoints([(0.0, 0.0, 0), (200.0, 0.0, 0), (200.0, 300.0, 0), (0.0, 300.0, 0)])
    pattern_api.SetPatternPieceName(p, "sleeve")
    before = {"patterns": pattern_api.GetPatternCount(), "seams": pattern_api.GetSeamlinePairGroupCount(),
              "outline": [list(map(float, q))[:3] for q in pattern_api.GetPatternOutlinePoints(p)][:8]}
    s = pattern_api.CreateInternalShapeWithPoints(p, [(0.0, 60.0, 0), (200.0, 60.0, 0)], False)
    shape = pattern_api.GetPatternInternalShapePoints(p, s) if s is not None and s >= 0 else None
    try:
        ok = pattern_api.CutPatternAlongInternalShapes(p, s, sew)
        err = None
    except Exception as e:
        ok, err = None, str(e)[:300]
    after = {"patterns": pattern_api.GetPatternCount(), "seams": pattern_api.GetSeamlinePairGroupCount()}
    after["outlines"] = {}
    for i in range(after["patterns"]):
        after["outlines"][i] = {"name": pattern_api.GetPatternPieceName(i) if hasattr(pattern_api, "GetPatternPieceName") else "",
                                "outline": [list(map(float, q))[:3] for q in pattern_api.GetPatternOutlinePoints(i)][:8]}
    out["sew" if sew else "nosew"] = {"before": before, "shapeIndex": s, "shape": str(shape)[:300], "cut": ok, "error": err,
                                     "after": after}
result["cut"] = out
log("cut probe done")
