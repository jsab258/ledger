# Controlled test of which way an internal line's fold angle turns a piece (2 October): a 300 x 500 mm panel with a
# vertical line 100 mm in from one edge, folded to 30 and to 330 (180 is flat), in empty space without gravity, so
# only the fold moves it; exported before and after, to see whether the strip turns towards the panel's front face
# (the side that faces out from the body when arranged) or away from it.
import json, os
OUT = r"C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-clothes\a7b8ce43-be87-4946-b632-3ba22bdea8f7\scratchpad\md\fold"
RECT = [(0.0, 0.0, 0), (300.0, 0.0, 0), (300.0, 500.0, 0), (0.0, 500.0, 0)]
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = False
eo.bExportGarment = True
for ang in (30, 330):
    utility_api.NewProject()
    try:
        print("AVATARS?", utility_api.IsShowAvatar())
        utility_api.DeleteAvatar(0)
    except Exception as e:
        print("delete avatar", e)
    p = pattern_api.CreatePatternWithPoints(RECT)
    pattern_api.CreateInternalShapeWithPoints(p, [(100.0, 0.0, 0), (100.0, 500.0, 0)], False)
    path = os.path.join(OUT, "a%d.json" % ang)
    pattern_api.ExportPatternJSON(path)
    d = json.load(open(path))
    for il in d["PatternList"][0]["InternalLineList"]:
        if not il.get("IsClosed"):
            il["FoldData"] = {"iAngle": ang, "iStrength": 15, "bRenderFolded": True}
    json.dump(d, open(path, "w"))
    utility_api.NewProject()
    try:
        utility_api.DeleteAvatar(0)
    except Exception as e:
        pass
    pattern_api.ImportPatternJSON(path)
    try:
        utility_api.SetSimulationGravity(0.0)
    except Exception as e:
        print("gravity", e)
    pattern_api.SetParticleDistanceOfPatterns(15.0)
    export_api.ExportOBJ(os.path.join(OUT, "f%d-before.obj" % ang), eo)
    utility_api.Simulate(300)
    export_api.ExportOBJ(os.path.join(OUT, "f%d-after.obj" % ang), eo)
    print("A", ang, "done")
