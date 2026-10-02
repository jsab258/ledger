# The sewn jacket (tools/md/write_pattern.py) on Marvelous's stock man, each piece on one of his arrangement points,
# exported before any simulation so the placing can be looked at (tools/md/look_md.py).
import json, os
D = r"F:\LedgerTools\tmp\clothes\md\ron1"
OUT = r"C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-clothes\a7b8ce43-be87-4946-b632-3ba22bdea8f7\scratchpad\md"
LUKA = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Avatar\Male\MV2.1_Luka.avt"
utility_api.NewProject()
opt = ApiTypes.ImportExportOption()
print("AVATAR", import_api.ImportAvatar(LUKA, opt))
print("PATTERN", pattern_api.ImportPatternJSON(os.path.join(D, "sewn.json")), "seams", pattern_api.GetSeamlinePairGroupCount())
arr = {a["ArrangementName"]: int(a["ArrangementIndex"]) for a in pattern_api.GetArrangementList()}
names = {pattern_api.GetPatternPieceName(i): i for i in range(pattern_api.GetPatternCount())}
print("NAMES", names)
PLACE = {"frontL": "Body_Front_3_L", "frontR": "Body_Front_3_R", "facingL": "Body_Front_3_L", "facingR": "Body_Front_3_R",
         "sideL": "Body_Side_L", "sideR": "Body_Side_R", "backL": "Body_Back_3_L", "backR": "Body_Back_3_R",
         "topsleeveL": "Arm_Outside_2_L", "topsleeveR": "Arm_Outside_2_R", "undersleeveL": "Arm_Inside_2_L",
         "undersleeveR": "Arm_Inside_2_R", "undercollar": "Neck_Collar", "topcollar": "Neck_Collar",
         "flapL": "Body_Front_4_L", "flapR": "Body_Front_4_R", "chestwelt": "Body_Front_2_L"}
for key, pt in PLACE.items():
    i = names[key]
    pattern_api.SetArrangement(i, arr[pt])
print("ARRANGED", {k: pattern_api.GetArrangementOfPattern(names[k]) for k in ("frontL", "backL", "topsleeveL", "undercollar")})
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = True
eo.bSingleObject = False
print("EXPORT", export_api.ExportOBJ(os.path.join(OUT, "arranged.obj"), eo))
