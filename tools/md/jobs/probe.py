# The first job through the bridge: what Marvelous Designer's script interface holds in this version, and the
# signatures and help of the calls the jacket needs. Output saved by the session to
# production/research/clothing-pipeline/md-api-2026.txt.
import inspect
print("MODULES", BRIDGE_MODULES)
want = ("ImportFBX", "ImportOBJ", "ImportAvatar", "ImportZprj", "CreatePatternWithPoints", "CreateInternalShapeWithPoints",
        "CreateInternalLine", "AddSeamlinePairGroup", "ExportPatternJSON", "ImportPatternJSON", "ExportUSD", "ExportFBX",
        "ExportOBJ", "Simulate", "SetSimulationQuality", "AddFabric", "AssignFabricToPattern", "SetParticleDistanceOfPattern",
        "SetPatternLayer", "SetPatternPieceSeamtaping", "SetPatternPieceElastic", "SetArrangement", "SetArrangementPosition",
        "SetPatternPieceTranslation", "GetPatternCount", "ExportZprj", "SaveProject", "NewProject", "ClearAll")
for name in BRIDGE_MODULES:
    mod = globals().get(name)
    if mod is None or name in ("BRIDGE_MODULES",):
        continue
    calls = [c for c in dir(mod) if not c.startswith("_")]
    print("\n== %s (%d)" % (name, len(calls)))
    print(" ".join(calls))
print("\n== WANTED")
for name in BRIDGE_MODULES:
    mod = globals().get(name)
    if mod is None:
        continue
    for c in dir(mod):
        if any(w.lower() in c.lower() for w in want) or any(k in c.lower() for k in ("fold", "bond", "strength", "fusible", "pad", "button", "tape", "internal", "seam", "arrange", "json")):
            f = getattr(mod, c)
            doc = (getattr(f, "__doc__", "") or "").strip().replace("\n", " ")[:300]
            try:
                sig = str(inspect.signature(f))
            except Exception:
                sig = "(?)"
            print("%s.%s%s  %s" % (name, c, sig, doc))
