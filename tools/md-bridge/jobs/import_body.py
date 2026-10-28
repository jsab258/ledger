# TOM'S BODY AS THE AVATAR (26 October, item 3; production/art/clothing/tom-outfit/SPEC.md): a clean
# project, his MetaHuman body (FBX, Unreal's centimetres, reference A-pose) imported as the avatar with
# arrangement points, then exported back alone as OBJ, so its size can be measured outside Marvelous
# before any pattern is drawn (CLO's docs never define the import scale: MD-SCRIPTING-2026-10-26.md).
# a copy run for another body sets BODY, OUT and AVT_OUT above this text (28 October: the straight-elbowed drape body)
BODY = globals().get("BODY", r"F:\LedgerTools\bodies\MH_TomL1\MH_TomL1_FullBody.fbx")
OUT = globals().get("OUT", r"F:\LedgerTools\garments\tom\avatar-check.obj")
import os
# A WRONG PATH OPENS A BOX IN MARVELOUS THAT ONLY JAFAR CAN CLOSE (26 October: "Failed to initialize FBX
# Importer", the first try named a file that is not there): every file is checked here first.
if not os.path.isfile(BODY):
    raise FileNotFoundError(BODY)
utility_api.NewProject()
opt = ApiTypes.ImportExportOption()
opt.ImportObjectType = 0                  # an avatar, not a trim
opt.bAddArrangementPoints = True          # his A-pose takes them
opt.bAutoCreateFittingSuit = True
# THE OCTOBER LESSON (tools/md/jobs/grow_drape.py, 2 October): these bodies are in centimetres, and Marvelous
# reads them as millimetres at scale 1 (ten times too small, too small for its pose test); so scale 10, and
# its own size-and-pose guess off (MD-AVATAR-2026-10-26.md)
opt.bSizeAndPoseFromAvatar = False
opt.scale = float(globals().get("SCALE", 10.0))
result["imported"] = bool(import_api.ImportFBX(BODY, opt))
try:
    result["measurements"] = utility_api.GetAvatarMeasurements(0)
except Exception as e:
    result["measurements"] = "error: %s" % e
try:
    result["arrangementPoints"] = len(pattern_api.GetArrangementList())
except Exception as e:
    result["arrangementPoints"] = "error: %s" % e
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = False
eo.bSingleObject = True
eo.scale = 1.0
result["exported"] = export_api.ExportOBJ(OUT, eo)
# THE AVATAR KEPT WITH ITS POINTS, so later jobs load it (ImportAvatar) with no import box to answer
if isinstance(result.get("arrangementPoints"), int) and result["arrangementPoints"] > 0:
    result["avatarSaved"] = export_api.ExportAVT(globals().get("AVT_OUT", r"F:\LedgerTools\garments\tom\MH_TomL1.avt"))
log("body imported and exported for measuring")
