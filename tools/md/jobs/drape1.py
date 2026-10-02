# A first coarse drape of the arranged jacket (tools/md/jobs/arrange_luka.py, the project still open): wool twill for
# the shell, a stiffer cloth standing in for the fused pieces (Bond has no script call), the fused pieces strengthened
# for the first settle, the left back over the right at the vent, the flaps and welt over the fronts, 20 mm
# particles; then a few hundred simulation steps, timed, and the result exported for a look.
import json, os, time
OUT = r"C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-clothes\a7b8ce43-be87-4946-b632-3ba22bdea8f7\scratchpad\md"
FAB = r"C:\Users\Public\Documents\MarvelousDesigner\New Assets\Fabric"
names = {pattern_api.GetPatternPieceName(i): i for i in range(pattern_api.GetPatternCount())}
shell = fabric_api.AddFabric(os.path.join(FAB, "V2_Woven_Twill_1.zfab"))
fused = fabric_api.AddFabric(os.path.join(FAB, "V2_Woven_Canvas_1.zfab"))
print("FABRICS", shell, fused, fabric_api.GetFabricCount())
FUSED = {"frontL", "frontR", "facingL", "facingR", "undercollar", "topcollar", "flapL", "flapR", "chestwelt"}
for k, i in names.items():
    pattern_api.SetPatternPieceFabricIndex(i, fused if k in FUSED else shell)
print("ASSIGNED", {k: pattern_api.GetPatternPieceFabricIndex(i) for k, i in list(names.items())[:3]})
LAYER = {"backL": 1, "flapL": 1, "flapR": 1, "chestwelt": 1}
for k, i in names.items():
    pattern_api.SetPatternLayer(i, LAYER.get(k, 0))
# the left front over the right where they cross at centre front, each facing behind its front
Z = {"frontL": 60, "frontR": 45, "facingL": 40, "facingR": 28, "flapL": 75, "flapR": 60, "chestwelt": 75, "topcollar": 85}
for k, z in Z.items():
    a = pattern_api.GetArrangementOfPattern(names[k])
    pattern_api.SetArrangementPosition(names[k], int(a["ArrangementOffsetX"]), int(a["ArrangementOffsetY"]), z)
print("ZNOW", {k: pattern_api.GetArrangementOfPattern(names[k])["ArrangementOffsetZ"] for k in ("frontL", "facingR")})
for k in FUSED:
    pattern_api.SetPatternStrengthen(names[k], True)
pattern_api.SetParticleDistanceOfPatterns(20.0)
t0 = time.time()
done = 0
for chunk in range(6):
    ok = utility_api.Simulate(50)
    done += 50
    print("SIM", done, ok, round(time.time() - t0, 1))
eo = ApiTypes.ImportExportOption()
eo.bExportAvatar = True
eo.bExportGarment = True
print("EXPORT", export_api.ExportOBJ(os.path.join(OUT, "drape1.obj"), eo))
