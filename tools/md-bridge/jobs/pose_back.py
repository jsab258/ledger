# THE SLEEVE'S END, FOURTH ROUND (28 October 2026): a jacket draped on the straight-elbowed body (its sleeves now round
# the forearms to their ends) taken back to Tom's reference pose inside Marvelous, as its manual changes pose: the drape's
# project opened, the reference body's pose (exported from his own avatar) loaded, then simulated, so the cloth follows
# the arms as they bend. The avatar is written before and after the pose, to see whether the pose took.
# A copy sets SRC (the drape's .zprj), POSE (the .pos) and OUT above this text.
import os
SRC = globals().get("SRC", r"F:\LedgerTools\garments\tom\zip_jacket\v16\zip_jacket.zprj")
POSE = globals().get("POSE", r"F:\LedgerTools\garments\tom\sleeve_try4\probe\tom_pose.pos")
OUT = globals().get("OUT", r"F:\LedgerTools\garments\tom\zip_jacket\v16\pose_ref")
STEPS = int(globals().get("STEPS", 300))
for p in (SRC, POSE):
    if not os.path.isfile(p):
        raise FileNotFoundError(p)
os.makedirs(OUT, exist_ok=True)
utility_api.NewProject()
try:
    result["opened"] = str(import_api.ImportZprj(SRC, ApiTypes.ImportZPRJOption()))
except TypeError:
    result["opened"] = str(import_api.ImportZprj(SRC))
ea = ApiTypes.ImportExportOption()
ea.bExportGarment = False
ea.bExportAvatar = True
ea.bSingleObject = True
ea.scale = 1.0
eg = ApiTypes.ImportExportOption()
eg.bExportGarment = True
eg.bExportAvatar = False
eg.bSingleObject = False
eg.scale = 1.0
result["avatarBefore"] = export_api.ExportOBJ(os.path.join(OUT, "avatar_before.obj"), ea)
result["posed"] = bool(import_api.ImportPose(POSE, bool(globals().get("POSE_TRANSLATION", True)), False))
result["avatarAfterPose"] = export_api.ExportOBJ(os.path.join(OUT, "avatar_after_pose.obj"), ea)
result["garmentAfterPose"] = export_api.ExportOBJ(os.path.join(OUT, "garment_after_pose.obj"), eg)
result["simulated"] = bool(utility_api.Simulate(STEPS))
result["avatarAfterSim"] = export_api.ExportOBJ(os.path.join(OUT, "avatar.obj"), ea)
result["garment"] = export_api.ExportOBJ(os.path.join(OUT, "zip_jacket.obj"), eg)
log("posed back and simulated %d steps" % STEPS)
