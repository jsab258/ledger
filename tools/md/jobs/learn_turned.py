# Controlled test of what a turned seam does (2 October): two equal 300 x 500 mm panels side by side in empty space
# without gravity, A's left edge sewn to B's left edge, turned and not turned, fold strength 0 and 10; exported after
# 400 steps to see where B ends: stacked on A (in front of or behind its face) or opened flat beside it.
import json, os
OUT = r"C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-clothes\a7b8ce43-be87-4946-b632-3ba22bdea8f7\scratchpad\md\fold"
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = False
eo.bExportGarment = True
for turned in (True, False):
    for k in (0, 10):
        utility_api.NewProject()
        a = pattern_api.CreatePatternWithPoints([(0.0, 0.0, 0), (300.0, 0.0, 0), (300.0, 500.0, 0), (0.0, 500.0, 0)])
        b = pattern_api.CreatePatternWithPoints([(400.0, 0.0, 0), (700.0, 0.0, 0), (700.0, 500.0, 0), (400.0, 500.0, 0)])
        pattern_api.SetPatternPieceName(a, "A")
        pattern_api.SetPatternPieceName(b, "B")
        path = os.path.join(OUT, "t.json")
        pattern_api.ExportPatternJSON(path)
        d = json.load(open(path))
        PA, PB = d["PatternList"]
        la, lb = PA["ShapeInfo"]["LineList"][3]["ID"], PB["ShapeInfo"]["LineList"][3]["ID"]
        d["SeamLinePairGroupList"] = [{"Name": "edge", "bIsTurned": turned, "FoldData": {"iAngle": 180, "iStrength": k},
            "PairList": [{"First": {"ShapeID": PA["ID"], "LengthParam": {"fStart": 0.6875, "fEnd": 1.0}, "Direction": True, "LineID": la},
                          "Second": {"ShapeID": PB["ID"], "LengthParam": {"fStart": 0.6875, "fEnd": 1.0}, "Direction": True, "LineID": lb}}]}]
        json.dump(d, open(path, "w"))
        utility_api.NewProject()
        pattern_api.ImportPatternJSON(path)
        utility_api.SetSimulationGravity(0.0)
        pattern_api.SetParticleDistanceOfPatterns(15.0)
        utility_api.Simulate(400)
        export_api.ExportOBJ(os.path.join(OUT, "turned%s-k%d.obj" % (int(turned), k)), eo)
        print("T", turned, k, "seams", pattern_api.GetSeamlinePairGroupCount())
