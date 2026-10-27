# THE CUFFS, RESEARCH AFTER THE THIRD TRY (27 October 2026; its fresh review): cuff_arrange2.py's position runs were
# confounded. The two that moved the cuff (offset, X) set the shape style AFTER the position, and no Y run did; three Y
# runs read back 50. Here every run sets the point, then the position, then the shape style, and Y is read back.
import os
AVT = r"F:\LedgerTools\garments\tom\MH_TomL1.avt"
OUT = r"F:\LedgerTools\garments\tom\cuff_try3\arrange3"
os.makedirs(OUT, exist_ok=True)
W, H = 197.1, 60.0
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = False
eo.bSingleObject = False
eo.scale = 1.0
ways = {}
for point in ("Wrist_Outside_L", "Arm_Outside_3_L"):
    for y in (0, 50, 100):
        utility_api.NewProject()
        import_api.ImportAvatar(AVT, ApiTypes.ImportExportOption())
        points = {p["ArrangementName"]: int(p["ArrangementIndex"]) for p in pattern_api.GetArrangementList()}
        c = pattern_api.CreatePatternWithPoints([(0.0, 0.0, 0), (W, 0.0, 0), (W, H, 0), (0.0, H, 0)])
        pattern_api.SetPatternPieceName(c, "cuffL")
        pattern_api.SetArrangement(c, points[point])
        pattern_api.SetArrangementPosition(c, 50, y, 50)
        pattern_api.SetArrangementShapeStyle(c, "Curved")
        name = "%s_y%d" % (point.split("_")[0].lower(), y)
        back = dict(pattern_api.GetArrangementOfPattern(c))
        export_api.ExportOBJ(os.path.join(OUT, name + ".obj"), eo)
        ways[name] = {"readBackY": back.get("ArrangementOffsetY"), "readBackX": back.get("ArrangementOffsetX")}
result["ways"] = ways
log("arranged %d ways, shape style after position" % len(ways))
