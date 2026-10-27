# THE CUT CALL, TESTED PROPERLY (27 October 2026; the third try's fresh review): cut_probe.py gave the cut the index
# CreateInternalShapeWithPoints returned (2, likely the pattern's index space, not the line's) and read nothing back, so it
# showed nothing either way. Here the piece's own information is read before and after (GetPatternInformation), the line
# is drawn past the piece's edges as well as edge to edge, and OffsetAsInternalLine (documented; Epic's own step) is tried.
import json
out = {}


def info(p):
    try:
        return json.loads(pattern_api.GetPatternInformation(p))
    except Exception as e:
        return "error: %s" % e


def piece():
    utility_api.NewProject()
    p = pattern_api.CreatePatternWithPoints([(0.0, 0.0, 0), (200.0, 0.0, 0), (200.0, 300.0, 0), (0.0, 300.0, 0)])
    pattern_api.SetPatternPieceName(p, "sleeve")
    return p


p = piece()
out["infoPlain"] = str(info(p))[:1500]
for label, pts in (("edge_to_edge", [(0.0, 60.0, 0), (200.0, 60.0, 0)]), ("past_edges", [(-20.0, 60.0, 0), (220.0, 60.0, 0)])):
    for idx_try in (0, 1, "returned"):
        for sew in (True, False):
            p = piece()
            r = pattern_api.CreateInternalShapeWithPoints(p, pts, False)
            idx = r if idx_try == "returned" else idx_try
            before = pattern_api.GetPatternCount()
            try:
                ok = pattern_api.CutPatternAlongInternalShapes(p, idx, sew)
                err = None
            except Exception as e:
                ok, err = None, str(e)[:200]
            key = "%s_idx%s_sew%s" % (label, idx_try, sew)
            out[key] = {"returned": r, "cut": ok, "error": err, "patterns": [before, pattern_api.GetPatternCount()],
                        "seams": pattern_api.GetSeamlinePairGroupCount()}
            if label == "edge_to_edge" and idx_try == 0 and sew:
                out["infoWithLine"] = str(info(p))[:1500]
# OffsetAsInternalLine(pattern, line, ?, distance, ?, ?): the bottom edge (line 0) offset 60 mm inward, then cut
for args in ((0, 1, 60.0, True, False), (0, 1, 60.0, False, False), (0, 0, 60.0, True, True)):
    p = piece()
    try:
        pattern_api.OffsetAsInternalLine(p, *args)
        made = str(info(p))[:800]
        cuts = []
        for idx in (0, 1):
            cuts.append(pattern_api.CutPatternAlongInternalShapes(p, idx, True))
            if pattern_api.GetPatternCount() > 1:
                break
        out["offset_%s" % "_".join(map(str, args))] = {"info": made, "cuts": cuts, "patterns": pattern_api.GetPatternCount(),
                                                     "seams": pattern_api.GetSeamlinePairGroupCount()}
    except Exception as e:
        out["offset_%s" % "_".join(map(str, args))] = {"error": str(e)[:300]}
result["cut"] = out
log("cut probe 2 done")
