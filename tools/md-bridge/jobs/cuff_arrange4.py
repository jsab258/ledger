# THE CUFFS, FOURTH ROUND (28 October 2026): on the straight-elbowed drape body the sleeve's end now goes round the
# forearm (drape 16), but a cuff placed on Arm_Outside_3 with its own offset still closed into a band beside the wrist
# (drape 18). Here each cuff is placed the way the sleeve now is (position set, then the shape style curved), over a
# sweep of positions along the arm and offsets, nothing sewn or simulated, each way exported for
# tools/md-bridge/sleeve_wrap.py (--piece cuffL --joints) to read how far round the forearm it goes and where.
import json, os
AVT = globals().get("AVT", r"F:\LedgerTools\garments\tom\MH_TomL1_straight.avt")
PLAN = globals().get("PLAN", r"F:\LedgerTools\garments\tom\zip_jacket\job_v18.plan.json")
OUT = os.path.join(r"F:\LedgerTools\garments\tom\sleeve_try4", globals().get("SUBDIR", "cuff_arrange4"))
os.makedirs(OUT, exist_ok=True)
pieces = {p["key"]: p for p in json.load(open(PLAN, encoding="utf-8"))["pieces"]}
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = False
eo.bSingleObject = False
eo.scale = 1.0
WAYS = globals().get("WAYS") or [("%s_y%d_z%d" % (pt.split("_")[1].lower() + pt[-1], y, z), pt, (50, y, z))
                                 for pt in ("Arm_Outside_3", "Arm_Outside_2") for y in (0, 15, 30) for z in (30, 40)]
ways = {}
for name, point, pos in WAYS:
    utility_api.NewProject()
    import_api.ImportAvatar(AVT, ApiTypes.ImportExportOption())
    points = {p["ArrangementName"]: int(p["ArrangementIndex"]) for p in pattern_api.GetArrangementList()}
    got = {}
    for s in ("R", "L"):
        p = pieces["cuff" + s]
        i = pattern_api.CreatePatternWithPoints([(float(x), float(y), int(t)) for x, y, t in p["points"]])
        pattern_api.SetPatternPieceName(i, "cuff" + s)
        pattern_api.SetArrangement(i, points["%s_%s" % (point, s)])
        pattern_api.SetArrangementPosition(i, *pos)
        pattern_api.SetArrangementShapeStyle(i, "Curved")
        got[s] = dict(pattern_api.GetArrangementOfPattern(i))
    export_api.ExportOBJ(os.path.join(OUT, name + ".obj"), eo)
    ways[name] = got
result["ways"] = ways
log("cuffs arranged %d ways, nothing sewn or simulated" % len(ways))
