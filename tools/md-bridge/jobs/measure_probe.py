# THE SLEEVE'S END, STEP 0 (28 October 2026): the calls that might tie a sleeve's end to Tom's wrist or change his pose
# for the drape, probed before any drape: their own descriptions, the avatar's measures, and his pose written out.
import os
AVT = r"F:\LedgerTools\garments\tom\MH_TomL1.avt"
OUT = r"F:\LedgerTools\garments\tom\sleeve_try4\probe"
os.makedirs(OUT, exist_ok=True)
utility_api.NewProject()
import_api.ImportAvatar(AVT, ApiTypes.ImportExportOption())
docs = {}
for mod in (pattern_api, utility_api, import_api, export_api):
    for n in ("AttachPatternToAvatarMeasure", "SetPatternEdgeToAvatarMeasure", "GetPatternEdgeToAvatarMeasureAttachment",
              "GetAllPatternToAvatarMeasures", "GetAvatarMeasurements", "ImportPose", "ImportPoseW", "ExportPose",
              "GetClothPositions", "ReDrape3DArrangement", "ResetClothArrangement", "MoveAnimationFrame",
              "SetPatternPieceMove", "GetAvatarProperties", "AlignAvatarsAndGarmentToCenter", "UnfoldPatternPiece"):
        f = getattr(mod, n, None)
        if f is not None:
            docs["%s.%s" % (mod.__name__, n)] = (getattr(f, "__doc__", None) or "")[:600]
result["docs"] = docs
for mod in (utility_api, pattern_api, import_api):
    f = getattr(mod, "GetAvatarMeasurements", None)
    if f:
        try:
            m = f()
            result["measurements"] = str(m)[:4000]
        except Exception as e:
            result["measurementsError"] = repr(e)
        break
for mod in (export_api, utility_api):
    f = getattr(mod, "ExportPose", None)
    if f:
        try:
            result["poseExported"] = str(f(os.path.join(OUT, "tom_pose.pos")))
        except Exception as e:
            result["poseError"] = repr(e)
        break
log("probed")
