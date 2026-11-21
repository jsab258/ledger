# EXPORT BEFORE THE MARVELOUS MONTH ENDS (21 November 2026; handover step 4, deadline Thu 26 Nov): one saved project
# opened in a fresh scene, its pattern written as JSON and its garment as FBX beside the .zprj, so the work outlives
# the subscription. The open itself is the check that the file reopens. A copy sets SRC above this text
# (tools/md-bridge/export_all.py writes one job per .zprj).
import os
SRC = globals().get("SRC", "")
if not os.path.isfile(SRC):
    raise FileNotFoundError(SRC)
base = os.path.splitext(SRC)[0]
utility_api.NewProject()
try:
    opened = import_api.ImportZprj(SRC, ApiTypes.ImportZPRJOption())
except TypeError:
    opened = import_api.ImportZprj(SRC)
result["src"] = SRC
result["opened"] = str(opened)
result["pattern"] = bool(pattern_api.ExportPatternJSON(base + ".pattern.json"))
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = False
eo.bSingleObject = False
eo.scale = 1.0
result["fbx"] = str(export_api.ExportFBX(base + ".garment.fbx", eo))
result["files"] = {p: (os.path.getsize(p) if os.path.isfile(p) else None)
                   for p in (base + ".pattern.json", base + ".garment.fbx")}
