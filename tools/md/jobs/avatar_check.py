# Load a body as the avatar WITHOUT arrangement points (no dialog), read its measurements, and export it as Marvelous
# holds it, to see its size and which way it faces.
import json, os
OUT = r"F:\LedgerTools\tmp\clothes\md\learn3"
os.makedirs(OUT, exist_ok=True)
utility_api.NewProject()
opt = ApiTypes.ImportExportOption()
ok = import_api.ImportFBX(AVATAR, opt)
print("IMPORT", ok)
try:
    ms = utility_api.GetAvatarMeasurements(0)
    print("MEASURES", len(ms), [str(m)[:120] for m in ms[:6]])
except Exception as e:
    print("MEASURES ERR", e)
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = False
eo.bSingleObject = True
res = export_api.ExportOBJ(os.path.join(OUT, "avatar.obj"), eo)
print("EXPORT", res)
