# Load Marvelous's stock man (MV2.1_Luka.avt, with his own arrangement points) by script, and list his points and
# measurements: the route round our MetaHuman bodies having none (research MD-AVATAR-ARRANGEMENT-2026-10-02.md, C).
import json
utility_api.NewProject()
opt = ApiTypes.ImportExportOption()
ok = import_api.ImportAvatar(r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Avatar\Male\MV2.1_Luka.avt", opt)
print("IMPORTED", ok)
arr = pattern_api.GetArrangementList()
print("POINTS", len(arr))
print("FIRST", json.dumps(arr[:80]))
for i in range(0, 40):
    try:
        m = utility_api.GetAvatarMeasurements(i)
        if m: print("MEAS", i, m)
    except Exception as e:
        print("MEASERR", i, e); break
