# TOM'S DNA AVATAR, EXPORTED (2 November, the clothing deep-dive's trial 2,
# production/research/clothing-pipeline/DEEP-DIVE-2026-11-01.md): after his head and body DNA (Epic's export,
# F:\LedgerTools\bodies\MH_TomL1\dna) were brought into an empty scene by Marvelous's own File > Import (Add) >
# DNA (a window step: no API call reads DNA), the avatar alone goes out as OBJ beside an .avt, with its
# arrangement points and measurements, to be compared with MH_TomL1.avt's own export (avatar-check.obj).
OUT = globals().get("OUT", r"F:\LedgerTools\bodies\MH_TomL1\dna-md\dna-avatar.obj")
AVT_OUT = globals().get("AVT_OUT", r"F:\LedgerTools\bodies\MH_TomL1\dna-md\MH_TomL1_dna.avt")
try:
    result["arrangementPoints"] = len(pattern_api.GetArrangementList())
except Exception as e:
    result["arrangementPoints"] = "error: %s" % e
try:
    result["measurements"] = utility_api.GetAvatarMeasurements(0)
except Exception as e:
    result["measurements"] = "error: %s" % e
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = False
eo.bSingleObject = True
eo.scale = 1.0
result["exported"] = export_api.ExportOBJ(OUT, eo)
result["avatarSaved"] = export_api.ExportAVT(AVT_OUT)
