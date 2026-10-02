# Load one posed body as the avatar with arrangement points; report what Marvelous finds.
import json
utility_api.NewProject()
opt = ApiTypes.ImportExportOption()
opt.bAddArrangementPoints = True
ok = import_api.ImportFBX(AVATAR, opt)
arr = pattern_api.GetArrangementList()
print("IMPORT", ok, "ARRANGEMENT POINTS", len(arr))
print("FIRST", json.dumps(arr[:4])[:800])
try:
    ms = utility_api.GetAvatarMeasurements(0)
    print("MEASURES", len(ms))
except Exception as e:
    print("MEASURES ERR", e)
