# THE CUFFS' THIRD TRY, STEP 1 (27 October 2026; production/research/game-clothing-pipeline/RIB-CUFFS-2026-10-27.md,
# section 3): where an arranged cuff lands before any drape. One rib cuff cut at 1.0 x his wrist (197.1 mm by 60 mm),
# alone on his avatar, placed several ways; after each the arrangement is read back and the cuff exported where it
# stands (no Simulate), so tools/md-bridge/cuff_measure.py can say which way puts the ring round the forearm at the wrist.
import json, os
AVT = r"F:\LedgerTools\garments\tom\MH_TomL1.avt"
OUT = r"F:\LedgerTools\garments\tom\cuff_try3\arrange"
os.makedirs(OUT, exist_ok=True)
utility_api.NewProject()
result["avatar"] = bool(import_api.ImportAvatar(AVT, ApiTypes.ImportExportOption()))
result["avatarProps"] = dict(utility_api.GetAvatarProperties(0))
try:
    result["measures"] = [str(m) for m in utility_api.GetAvatarMeasurements(0)][:60]
except Exception as e:
    result["measures"] = "error: %s" % e
points = {p["ArrangementName"]: p for p in pattern_api.GetArrangementList()}
result["wristArmPoints"] = {k: v for k, v in points.items() if k.endswith("_L") and (k.startswith("Wrist") or k.startswith("Arm_Outside"))}
W, H = 197.1, 60.0
cuff = pattern_api.CreatePatternWithPoints([(0.0, 0.0, 0), (W, 0.0, 0), (W, H, 0), (0.0, H, 0)])
pattern_api.SetPatternPieceName(cuff, "cuffL")
FAB = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Fabric"
rib = fabric_api.AddFabric(os.path.join(FAB, "V2_Cut_Sew_Knit_Rib_1.zfab"))
fabric_api.AssignFabricToPattern(rib, cuff, 1)
result["ribInfo"] = fabric_api.GetFabricInfo(rib)[:3000]
result["collisionThickness"] = pattern_api.GetAddlThicknessCollisionValue(cuff)
result["shrinkage"] = dict(pattern_api.GetShrinkagePercentage(cuff))

# (name, arrangement point, position (x, y, offset) or None)
WAYS = [("wrist", "Wrist_Outside_L", None),
        ("wrist_y0", "Wrist_Outside_L", (50, 0, 50)),
        ("wrist_y100", "Wrist_Outside_L", (50, 100, 50)),
        ("arm3", "Arm_Outside_3_L", None),
        ("arm3_y5", "Arm_Outside_3_L", (50, 5, 50)),
        ("arm3_y0", "Arm_Outside_3_L", (50, 0, 50))]
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bSingleObject = False
eo.scale = 1.0
ways = {}
first = True
for name, point, pos in WAYS:
    pattern_api.SetArrangement(cuff, int(points[point]["ArrangementIndex"]))
    pattern_api.SetArrangementShapeStyle(cuff, "Curved")
    if pos is not None:
        pattern_api.SetArrangementPosition(cuff, pos[0], pos[1], pos[2])
    back = dict(pattern_api.GetArrangementOfPattern(cuff))
    eo.bExportAvatar = first
    first = False
    ok = export_api.ExportOBJ(os.path.join(OUT, name + ".obj"), eo)
    ways[name] = {"point": point, "pos": pos, "readBack": back, "exported": bool(ok) if not isinstance(ok, (list, str)) else str(ok)[:200]}
result["ways"] = ways
log("cuff arranged %d ways, no drape" % len(WAYS))
