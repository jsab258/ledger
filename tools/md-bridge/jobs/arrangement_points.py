# TOM'S ARRANGEMENT POINTS (26 October, item 3): the names and places of the points Marvelous fitted to his avatar,
# loaded from the saved avatar (no import box), so the zip jacket's pieces can be placed by name.
import os
AVT = r"F:\LedgerTools\garments\tom\MH_TomL1.avt"
if not os.path.isfile(AVT):
    raise FileNotFoundError(AVT)
utility_api.NewProject()
opt = ApiTypes.ImportExportOption()
result["loaded"] = bool(import_api.ImportAvatar(AVT, opt))
lst = pattern_api.GetArrangementList()
result["count"] = len(lst)
result["points"] = [dict(p) for p in lst]
