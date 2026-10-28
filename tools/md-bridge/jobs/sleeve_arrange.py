# THE SLEEVE'S END, STEP 0 OF THE FOURTH ROUND (28 October 2026; his pick of 27 October night: the sleeve's end first,
# then the cuffs; production/research/game-clothing-pipeline/RIB-CUFFS-2026-10-27.md, "Another direction" 1). Every
# drape's sleeve end lay as a flat flap the hand came through. Before any drape: where does each way of arranging the
# sleeve put its cloth round the arm? Sleeves only, nothing sewn, nothing simulated; each way exported for
# tools/md-bridge/sleeve_wrap.py to measure how far round the forearm the cloth goes.
import json, os
AVT = globals().get("AVT", r"F:\LedgerTools\garments\tom\MH_TomL1.avt")
PLAN = r"F:\LedgerTools\garments\tom\zip_jacket\job_v13.plan.json"
# a sweep sets SUBDIR and WAYS_OVERRIDE above this text (a copy of this job with two lines put first)
OUT = os.path.join(r"F:\LedgerTools\garments\tom\sleeve_try4", globals().get("SUBDIR", "arrange"))
os.makedirs(OUT, exist_ok=True)
pieces = {p["key"]: p for p in json.load(open(PLAN, encoding="utf-8"))["pieces"]}
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = False
eo.bSingleObject = False
eo.scale = 1.0
WAYS = globals().get("WAYS_OVERRIDE") or [("as_jacket", "Arm_Outside_2", None, None), ("curved", "Arm_Outside_2", None, "Curved"),
        ("off0_curved", "Arm_Outside_2", (50, 50, 0), "Curved"), ("front2_curved", "Arm_Front_2", None, "Curved"),
        ("inside2_curved", "Arm_Inside_2", None, "Curved"), ("outside1_curved", "Arm_Outside_1", None, "Curved"),
        ("flat", "Arm_Outside_2", None, "Flat")]
ways = {}
for name, point, pos, style in WAYS:
    utility_api.NewProject()
    import_api.ImportAvatar(AVT, ApiTypes.ImportExportOption())
    if name == "as_jacket" or globals().get("WAYS_OVERRIDE") and name == WAYS[0][0]:
        ea = ApiTypes.ImportExportOption()
        ea.bExportGarment = False
        ea.bExportAvatar = True
        ea.bSingleObject = False
        ea.scale = 1.0
    points = {p["ArrangementName"]: int(p["ArrangementIndex"]) for p in pattern_api.GetArrangementList()}
    got = {}
    for s in ("R", "L"):
        p = pieces["sleeve" + s]
        i = pattern_api.CreatePatternWithPoints([(float(x), float(y), int(t)) for x, y, t in p["points"]])
        pattern_api.SetPatternPieceName(i, "sleeve" + s)
        pattern_api.SetArrangement(i, points["%s_%s" % (point, s)])
        if pos:
            pattern_api.SetArrangementPosition(i, *pos)
        if style:
            pattern_api.SetArrangementShapeStyle(i, style)
        got[s] = dict(pattern_api.GetArrangementOfPattern(i))
    export_api.ExportOBJ(os.path.join(OUT, name + ".obj"), eo)
    if name == "as_jacket" or globals().get("WAYS_OVERRIDE") and name == WAYS[0][0]:
        export_api.ExportOBJ(os.path.join(OUT, "avatar.obj"), ea)
    ways[name] = got
result["ways"] = ways
log("sleeves arranged %d ways, nothing sewn or simulated" % len(ways))
