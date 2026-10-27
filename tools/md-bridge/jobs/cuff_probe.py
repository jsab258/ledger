# THE CUFFS' THIRD TRY, STEP 0 (27 October 2026; production/research/game-clothing-pipeline/RIB-CUFFS-2026-10-27.md,
# section 3): before anything is draped, read from Marvelous itself what the calls the recipe leans on take and say
# (their __doc__), and the avatar's own skin offset, so the pass marks are set from it and not guessed.
NAMES = ["CutPatternAlongInternalShapes", "AddSeamlinePairGroupPartial", "AttachPatternToAvatarMeasure",
         "SetPatternEdgeToAvatarMeasure", "ReDrape3DArrangement", "ActivateAllPatterns", "GetAvatarMeasurements",
         "GetClothPositions", "GetArrangementOfPattern", "GetArrangementList", "SetArrangement", "SetArrangementPosition",
         "SetArrangementOrientation", "SetArrangementShapeStyle", "GetAvatarProperties", "SetAvatarProperties",
         "GetAddlThicknessCollisionValue", "SetAddlThicknessCollision", "SetWidthShrinkagePercentage",
         "GetShrinkagePercentage", "GetFabricInfo", "SetPatternFreeze", "SetParticleDistanceOfPattern",
         "SetPatternPieceElastic", "SetPatternPieceElasticStrengthRatio", "ResetClothArrangement",
         "GetPatternIndexFrom3DView", "OffsetAsInternalLine", "GetIntersectionPoints"]
docs = {}
for name in NAMES:
    found = []
    for mod in ("utility_api", "pattern_api", "fabric_api", "import_api", "export_api"):
        f = getattr(globals().get(mod), name, None)
        if f is not None:
            found.append("%s: %s" % (mod, (getattr(f, "__doc__", None) or "(no doc)").strip()[:1200]))
    docs[name] = found or ["absent"]
result["docs"] = docs
log("cuff probe: docs read")
