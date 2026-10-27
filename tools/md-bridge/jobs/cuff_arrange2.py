# THE CUFFS' THIRD TRY, STEP 1 AGAIN (27 October 2026): cuff_arrange.py found SetArrangementPosition read back but did
# not move the placed cuff. Does it take in another order (position before the point; the point set again after; the
# arrangement redrawn)? One cuff alone on his avatar, exported where it stands (no Simulate) after each.
import os
AVT = r"F:\LedgerTools\garments\tom\MH_TomL1.avt"
OUT = r"F:\LedgerTools\garments\tom\cuff_try3\arrange2"
os.makedirs(OUT, exist_ok=True)
utility_api.NewProject()
result["avatar"] = bool(import_api.ImportAvatar(AVT, ApiTypes.ImportExportOption()))
points = {p["ArrangementName"]: int(p["ArrangementIndex"]) for p in pattern_api.GetArrangementList()}
W, H = 197.1, 60.0
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = False
eo.bSingleObject = False
eo.scale = 1.0


def fresh():
    utility_api.NewProject()
    import_api.ImportAvatar(AVT, ApiTypes.ImportExportOption())
    c = pattern_api.CreatePatternWithPoints([(0.0, 0.0, 0), (W, 0.0, 0), (W, H, 0), (0.0, H, 0)])
    pattern_api.SetPatternPieceName(c, "cuffL")
    return c


ways = {}
for name in ("pos_first_y0", "pos_first_y100", "again_y0", "redrape_y0", "offset0", "x25_y50"):
    c = fresh()
    try:
        if name.startswith("pos_first"):
            pattern_api.SetArrangementPosition(c, 50, 0 if name.endswith("y0") else 100, 50)
            pattern_api.SetArrangement(c, points["Wrist_Outside_L"])
        elif name == "again_y0":
            pattern_api.SetArrangement(c, points["Wrist_Outside_L"])
            pattern_api.SetArrangementPosition(c, 50, 0, 50)
            pattern_api.SetArrangement(c, points["Wrist_Outside_L"])
        elif name == "redrape_y0":
            pattern_api.SetArrangement(c, points["Wrist_Outside_L"])
            pattern_api.SetArrangementPosition(c, 50, 0, 50)
            utility_api.ReDrape3DArrangement(ApiTypes.ImportExportOption())
        elif name == "offset0":
            pattern_api.SetArrangement(c, points["Wrist_Outside_L"])
            pattern_api.SetArrangementPosition(c, 50, 50, 0)
            pattern_api.SetArrangementShapeStyle(c, "Curved")
        elif name == "x25_y50":
            pattern_api.SetArrangement(c, points["Wrist_Outside_L"])
            pattern_api.SetArrangementPosition(c, 25, 50, 50)
            pattern_api.SetArrangementShapeStyle(c, "Flat")
            pattern_api.SetArrangementShapeStyle(c, "Curved")
        back = dict(pattern_api.GetArrangementOfPattern(c))
        ok = export_api.ExportOBJ(os.path.join(OUT, name + ".obj"), eo)
        ways[name] = {"readBack": back, "exported": str(ok)[:120]}
    except Exception as e:
        ways[name] = {"error": str(e)[:300]}
result["ways"] = ways
log("cuff arranged again, %d ways" % len(ways))
