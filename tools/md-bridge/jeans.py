#!/usr/bin/env python3
"""Tom's jeans as one Marvelous Designer job: FreeSewing's Titan block at his size with a jeans' ease, two fronts and
two backs, the leg tapered from the knee to a 1990 straight leg's hem, a waistband in two halves, placed on his avatar's
own points, sewn, draped, exported.

    python tools/md-bridge/jeans.py TITAN.json JOB.py [--out DIR] [--steps 400] [--avatar AVT] [--shorten MM] [--settle] [--front-position X,Y,OFFSET]
    python tools/md-bridge/md_job.py JOB.py          # runs it through the bridge
    python tools/md-bridge/jeans.py --selftest

WHY, 30 October 2026 (his order C9: after the cuffs, the jumper, jeans and shoes by the game-garment skill; the plan,
production/art/clothing/tom-outfit/JEANS-PLAN-2026-10-30.md). Charlie, the plan's first pick, puts its waistband at the
hip line (its waistHeight runs only to 40% of the waist-to-hips drop), a low-rise chino; Titan, the block it is built
on, reaches the natural waist, so Titan is drafted (F:/LedgerTools/garments/tom/jeans/pattern/titan-jeans.json:
seatEase 9%, kneeEase 20% with fitKnee, waistHeight 90%): seat 1,136 mm round (+9%), knee 478 (+20%), the band's top
about 2 to 5 cm under his natural waist. Its pieces are plain: no fly, pockets, yoke or loops to sew; those are drawn
in the normal map, the loops modelled after the drape if the bake reads flat (the plan). The jumper's helpers
(tools/md-bridge/zip_jacket.py: named edges, mirroring, winding) are imported, not copied.

THE CUT: Titan's leg runs straight down from the knee (hem = knee, 478 mm, 18.8 in), wider than the 501's 16 in
(JEANS-2026-09-30, D [12]); the outseam and inseam are drawn in from the knee to HEM_ROUND, the front and back alike so
their seams still match. The waistband WAISTBAND_H deep, cut to WAISTBAND_OF_WAIST of the trousers' waist so it draws
them in a little, in two halves closed at the centre front and the centre back.

The particle distance as the skill orders it: 20 mm while it settles, then 10 mm on the legs, 6 mm on the waistband,
Fitting last.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zip_jacket import CORNER, CURVE, ccw, edges_from, idx_of, length, load, mirror_edges  # noqa: E402

HEM_ROUND = 419.0           # mm round the hem, 16.5 in (the 501's 16 in, a little eased)
WAISTBAND_H = 38.0          # mm, 1.5 in
WAISTBAND_OF_WAIST = 0.97   # the band against the trousers' waist edge
ARRANGE = {"frontR": "Leg_Front_R", "frontL": "Leg_Front_L", "backR": "Leg_Back_R", "backL": "Leg_Back_L",
           "waistbandR": "Body_Waist_R", "waistbandL": "Body_Waist_L"}
FABRIC = "V2_Woven_Denim_1.zfab"      # its physics only: a denim twill


def shorten(pts, names, s):
    """The leg below the knee drawn up by s mm (the hem raised, the knee where it was), every point there moved in
    proportion to its drop below the knee, so the front and back still match. y up, the floor lowest."""
    if s <= 0:
        return pts, names
    knee_y, floor_y = names["kneeOut"][1], names["floorOut"][1]
    k = (knee_y - floor_y - s) / (knee_y - floor_y)

    def f(p):
        return list(p) if p[1] >= knee_y else [p[0], knee_y - (knee_y - p[1]) * k]
    return [f(p) for p in pts], {n: f(p) for n, p in names.items()}


def taper(pts, names, hem_round_half):
    """Every point below the knee drawn toward the leg's middle in proportion to its drop below the knee, so the hem
    is hem_round_half wide (this piece's share of the round) and the knee untouched. y up, the floor lowest."""
    knee_y, floor_y = names["kneeOut"][1], names["floorOut"][1]
    x_out, x_in = names["floorOut"][0], names["floorIn"][0]
    mid = (x_out + x_in) / 2.0
    cut = (abs(x_in - x_out) - hem_round_half) / 2.0
    if cut <= 0:
        return pts, names

    def f(p):
        if p[1] >= knee_y:
            return list(p)
        k = (knee_y - p[1]) / (knee_y - floor_y)
        toward = 1.0 if p[0] < mid else -1.0
        return [p[0] + toward * cut * k, p[1]]
    return [f(p) for p in pts], {n: f(p) for n, p in names.items()}


def build(titan, shorten_mm=0.0):
    fpts, fn = shorten(*titan["titan.front"], shorten_mm)
    bpts, bn = shorten(*titan["titan.back"], shorten_mm)
    front_w = abs(fn["floorIn"][0] - fn["floorOut"][0])
    back_w = abs(bn["floorIn"][0] - bn["floorOut"][0])
    # the hem's round shared as the drafted hem is, front to back
    fpts, fn = taper(fpts, fn, HEM_ROUND * front_w / (front_w + back_w))
    bpts, bn = taper(bpts, bn, HEM_ROUND * back_w / (front_w + back_w))
    corner = lambda pts, nm, order: [(idx_of(pts, nm[n]), tag) for n, tag in order]  # noqa: E731
    # THE DRAFT AS DRAWN IS HIS RIGHT LEG: the front seen from the front has its centre front (+x) to the side seam's
    # right, the back seen from behind its centre back (-x) to the side seam's left; the left leg is their mirror
    front = edges_from(fpts, sorted(corner(fpts, fn, [("styleWaistOut", "fWaistOut"), ("floorOut", "fFloorOut"), ("floorIn", "fFloorIn"),
                                                      ("fork", "fFork"), ("styleWaistIn", "fWaistIn")])))
    back = edges_from(bpts, sorted(corner(bpts, bn, [("fork", "bFork"), ("floorIn", "bFloorIn"), ("floorOut", "bFloorOut"),
                                                     ("styleWaistOut", "bWaistOut"), ("styleWaistIn", "bWaistIn")])))
    tag = lambda edges, s: [(seg, a + s, b + s) for seg, a, b in edges]  # noqa: E731
    pieces = {"frontR": ccw(tag(front, "R")), "frontL": ccw(tag(mirror_edges(front), "L")),
              "backR": ccw(tag(back, "R")), "backL": ccw(tag(mirror_edges(back), "L"))}
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    # THE WAISTBAND IN TWO HALVES, each round one side from the centre front to the centre back: its foot in two lines,
    # the front's waist then the back's, so each is sewn to its own edge
    for s in ("R", "L"):
        wf = length(E("front" + s, "fWaistIn" + s, "fWaistOut" + s)) * WAISTBAND_OF_WAIST
        wb = length(E("back" + s, "bWaistOut" + s, "bWaistIn" + s)) * WAISTBAND_OF_WAIST
        half = [([[0, 0], [wf, 0]], "wbCF" + s, "wbSide" + s), ([[wf, 0], [wf + wb, 0]], "wbSide" + s, "wbCB" + s),
                ([[wf + wb, 0], [wf + wb, WAISTBAND_H]], "wbCB" + s, "wbTopCB" + s),
                ([[wf + wb, WAISTBAND_H], [0, WAISTBAND_H]], "wbTopCB" + s, "wbTopCF" + s),
                ([[0, WAISTBAND_H], [0, 0]], "wbTopCF" + s, "wbCF" + s)]
        pieces["waistband" + s] = ccw(half) if s == "L" else ccw(mirror_edges(half))
    return pieces


def seams():
    out = []
    for s in ("R", "L"):
        out += [(("front" + s, "fWaistOut" + s, "fFloorOut" + s), ("back" + s, "bWaistOut" + s, "bFloorOut" + s)),   # outseam
                (("front" + s, "fFloorIn" + s, "fFork" + s), ("back" + s, "bFloorIn" + s, "bFork" + s)),              # inseam
                (("waistband" + s, "wbCF" + s, "wbSide" + s), ("front" + s, "fWaistIn" + s, "fWaistOut" + s)),
                (("waistband" + s, "wbSide" + s, "wbCB" + s), ("back" + s, "bWaistOut" + s, "bWaistIn" + s))]
    out += [(("frontR", "fForkR", "fWaistInR"), ("frontL", "fForkL", "fWaistInL")),       # the front rise, the fly shut
            (("backR", "bForkR", "bWaistInR"), ("backL", "bForkL", "bWaistInL")),         # the back rise
            (("waistbandR", "wbCFR", "wbTopCFR"), ("waistbandL", "wbCFL", "wbTopCFL")),   # the band shut at the front
            (("waistbandR", "wbCBR", "wbTopCBR"), ("waistbandL", "wbCBL", "wbTopCBL"))]   # and at the back
    return out


def patch():
    """Each piece's four grid corners for the bake chain (tools/meshgen/blender/retopo_pieces.py): the hem the bottom,
    the waist the top; the outseam one side, the inseam and rise the other; the band's foot its bottom."""
    out = {}
    for s in ("R", "L"):
        out["front" + s] = {"bottom": ["fFloorOut" + s, "fFloorIn" + s], "top": ["fWaistIn" + s, "fWaistOut" + s]}
        out["back" + s] = {"bottom": ["bFloorIn" + s, "bFloorOut" + s], "top": ["bWaistOut" + s, "bWaistIn" + s]}
        out["waistband" + s] = {"bottom": ["wbCF" + s, "wbCB" + s], "top": ["wbTopCB" + s, "wbTopCF" + s]}
    return out


def plan(titan, shorten_mm=0.0):
    pieces = build(titan, shorten_mm)
    out_pieces, lines = [], {}
    for key, edges in pieces.items():
        pts = []
        for k, (seg, a, b) in enumerate(edges):
            lines[(key, a, b)] = (k, True)
            lines[(key, b, a)] = (k, False)
            pts.append([round(seg[0][0], 2), round(seg[0][1], 2), CORNER])
            pts += [[round(x, 2), round(y, 2), CURVE] for x, y in seg[1:-1]]
        out_pieces.append({"key": key, "points": pts, "arrange": ARRANGE[key], "fabric": "denim"})
    out_seams = []
    for (pa, a0, a1), (pb, b0, b1) in seams():
        la, fa = lines[(pa, a0, a1)]
        lb, fb = lines[(pb, b0, b1)]
        out_seams.append({"a": [pa, la, fa], "b": [pb, lb, fb], "names": [a0, a1, b0, b1]})
    corners = {key: [[a, round(seg[0][0], 2), round(seg[0][1], 2)] for seg, a, _b in edges] for key, edges in pieces.items()}
    return {"pieces": out_pieces, "seams": out_seams, "corners": corners, "patch": patch(),
            "cut": {"hem_round_mm": HEM_ROUND, "waistband_mm": WAISTBAND_H, "waistband_of_waist": WAISTBAND_OF_WAIST,
                    "shorten_mm": shorten_mm}}


JOB = '''# Generated by tools/md-bridge/jeans.py from %(src)s: Tom's jeans made, placed on his avatar's points, sewn, draped
# (%(steps)d steps at 20 mm, 200 at 10 mm, 100 at Fitting) and exported to %(out)s.
import json, os
PLAN = json.loads(%(plan)r)
AVT = %(avt)r
OUT = %(out)r
if not os.path.isfile(AVT):
    raise FileNotFoundError(AVT)
os.makedirs(OUT, exist_ok=True)
utility_api.NewProject()
result["avatar"] = bool(import_api.ImportAvatar(AVT, ApiTypes.ImportExportOption()))
points = {p["ArrangementName"]: int(p["ArrangementIndex"]) for p in pattern_api.GetArrangementList()}
made = {}
for p in PLAN["pieces"]:
    idx = pattern_api.CreatePatternWithPoints([(float(x), float(y), int(t)) for x, y, t in p["points"]])
    made[p["key"]] = idx
    pattern_api.SetPatternPieceName(idx, p["key"])
    if p["arrange"] in points and idx >= 0:
        pattern_api.SetArrangement(idx, points[p["arrange"]])%(front)s
        pattern_api.SetArrangementShapeStyle(idx, "Curved")
result["made"] = made
result["arranged"] = {p["key"]: p["arrange"] in points for p in PLAN["pieces"]}
result["sewn"] = [bool(pattern_api.AddSeamlinePairGroup(made[s["a"][0]], s["a"][1], made[s["b"][0]], s["b"][1], s["a"][2], s["b"][2]))
                  for s in PLAN["seams"]]
FAB = r"C:\\Users\\Public\\Documents\\MarvelousDesigner\\New Assets\\Fabric"
fabrics = {}
path = os.path.join(FAB, %(fabric)r)
if os.path.isfile(path):
    fabrics["denim"] = fabric_api.AddFabric(path)
for p in PLAN["pieces"]:
    if p.get("fabric") in fabrics:
        fabric_api.AssignFabricToPattern(fabrics[p["fabric"]], made[p["key"]], 1)
result["fabrics"] = fabrics
%(simulate)s
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = True
eo.bSingleObject = False
eo.scale = 1.0
result["exported"] = export_api.ExportOBJ(os.path.join(OUT, "jeans.obj"), eo)
result["zprj"] = export_api.ExportZPrj(os.path.join(OUT, "jeans.zprj"))
log("jeans made, sewn and draped")
'''

# THE SIMULATION AS JOB N1 RAN IT: one call per stage
SIM_PLAIN = '''pattern_api.SetParticleDistanceOfPatterns(20.0)
result["settled20"] = bool(utility_api.Simulate(%(steps)d))
pattern_api.SetParticleDistanceOfPatterns(10.0)
# the waistband finer, 6 mm, as the skill orders for bands
for p in PLAN["pieces"]:
    if p["key"].startswith("waistband"):
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], 6.0)
result["settled10"] = bool(utility_api.Simulate(200))
try:
    utility_api.SetSimulationQuality(2, 0)
    result["fitting"] = "set: 2 Fitting, CPU"
except Exception as e:
    result["fitting"] = "refused: %%s" %% e
result["simulated"] = bool(utility_api.Simulate(100))'''

# --settle (30 October 2026, drape n1 fell to his hips): the same stages in short calls, the cloth exported after each
# (OUT/stages, garment only). Probed on his avatar (F:/LedgerTools/garments/tom/jeans/n2/probe): the first step at 20 mm
# throws the band 34 mm down (the hems start below the floor, the band 24 mm above the trousers' top); run as one
# 400-step call the jeans slid on to his hips (band top 1.03 m, then 1.00 after Fitting, the band stretched 13%), run
# as 1, 29, 70 and 300 steps with an export between they held with the band's top 22 to 24 mm under his natural waist
# from step 30 to 400. Each call starts from rest, so the first steps' throw is not carried on.
SIM_SETTLE = '''STAGES = os.path.join(OUT, "stages")
os.makedirs(STAGES, exist_ok=True)
def snap(tag):
    so = ApiTypes.ImportExportOption()
    so.bExportGarment = True
    so.bExportAvatar = False
    so.bSingleObject = False
    so.scale = 1.0
    export_api.ExportOBJ(os.path.join(STAGES, "%%s.obj" %% tag), so)
def settle(calls, tag):
    ok, done = True, 0
    for n in calls:
        ok = bool(utility_api.Simulate(n)) and ok
        done += n
        snap("%%s_%%03d" %% (tag, done))
    return ok
pattern_api.SetParticleDistanceOfPatterns(20.0)
snap("p20_000")
result["settled20"] = settle([1, 29, 70, %(rest20)d], "p20")
pattern_api.SetParticleDistanceOfPatterns(10.0)
# the waistband finer, 6 mm, as the skill orders for bands
for p in PLAN["pieces"]:
    if p["key"].startswith("waistband"):
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], 6.0)
result["settled10"] = settle([1, 19, 180], "p10")
try:
    utility_api.SetSimulationQuality(2, 0)
    result["fitting"] = "set: 2 Fitting, CPU"
except Exception as e:
    result["fitting"] = "refused: %%s" %% e
result["simulated"] = settle([1, 19, 80], "fit")'''


def main(argv):
    src, job = argv[0], argv[1]
    opt = lambda n, d: float(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
    out = argv[argv.index("--out") + 1] if "--out" in argv else r"F:\LedgerTools\garments\tom\jeans\drape"
    # --shorten MM: the leg drawn up below the knee (the hem raised); --settle: the stages in short calls (SIM_SETTLE)
    p = plan(load(src), opt("--shorten", 0.0))
    steps = int(opt("--steps", 400))
    sim = SIM_SETTLE % {"rest20": max(1, steps - 100)} if "--settle" in argv else SIM_PLAIN % {"steps": steps}
    # --front-position X,Y,OFFSET (30 October 2026, drape n3: the fronts start through his feet, which stand out in front
    # of the shins, 42 points over 3 mm in at the start of n2 and n3 alike; n2 shook them out, n3 kept 68). Along the leg's
    # arrangement volume Y 55 is the point's own; 65 lifts the fronts 91 mm, clear of the feet at the start
    # (F:/LedgerTools/garments/tom/jeans/n4/probe). The shape style is set after the position, or it does not move
    # (RIB-CUFFS-2026-10-27.md).
    front = ""
    if "--front-position" in argv:
        fp = [int(t) for t in argv[argv.index("--front-position") + 1].split(",")]
        front = ('\n        if p["key"].startswith("front"):\n'
                 '            pattern_api.SetArrangementPosition(idx, %d, %d, %d)' % tuple(fp))
    open(job, "w", encoding="utf-8").write(JOB % {
        "src": src, "plan": json.dumps(p), "out": out, "steps": steps, "fabric": FABRIC, "simulate": sim, "front": front,
        # the straight-elbowed drape body, as the jacket's and the jumper's (the skill, step 2)
        "avt": argv[argv.index("--avatar") + 1] if "--avatar" in argv else r"F:\LedgerTools\garments\tom\MH_TomL1_straight.avt"})
    json.dump(p, open(job[:-3] + ".plan.json", "w", encoding="utf-8"), indent=1)
    print("jeans: %d pieces, %d seams -> %s" % (len(p["pieces"]), len(p["seams"]), job))
    for q in p["pieces"]:
        print("  %-10s %3d points  on %s" % (q["key"], len(q["points"]), q["arrange"]))


def selftest():
    import math
    ok = []
    src = r"F:\LedgerTools\garments\tom\jeans\pattern\titan-jeans.json"
    if not os.path.isfile(src):
        print("jeans selftest: passed=0/0 failed=0 (no pattern on this machine)")
        return 0
    p = plan(load(src))
    keys = [q["key"] for q in p["pieces"]]
    ok.append(keys == ["frontR", "frontL", "backR", "backL", "waistbandR", "waistbandL"] and len(p["seams"]) == 12)
    pieces = build(load(src))
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    L = lambda seg: sum(math.dist(seg[k], seg[k + 1]) for k in range(len(seg) - 1))  # noqa: E731
    # every trouser seam's two edges within 3% of each other's length; the band against the waist by its cut
    ratios = []
    for (pa, a0, a1), (pb, b0, b1) in seams():
        r = L(E(pa, a0, a1)) / L(E(pb, b0, b1))
        ratios.append(r)
        band = pa.startswith("waistband") and not pb.startswith("waistband")
        ok.append(abs(r - WAISTBAND_OF_WAIST) < 0.005 if band else 0.97 <= r <= 1.03)
    # the hem's round at its target: each leg's front and back hem edges together
    hem = L(E("frontR", "fFloorOutR", "fFloorInR")) + L(E("backR", "bFloorInR", "bFloorOutR"))
    ok.append(abs(hem - HEM_ROUND) < 2.0)
    # the left leg the right's mirror: the same seam lengths
    ok.append(abs(L(E("frontL", "fWaistOutL", "fFloorOutL")) - L(E("frontR", "fWaistOutR", "fFloorOutR"))) < 0.5)
    print("jeans selftest: hem %.0f mm round (target %.0f)" % (hem, HEM_ROUND))
    print("jeans selftest: passed=%d/%d failed=%d (seam ratios %s)" % (
        sum(ok), len(ok), len(ok) - sum(ok), ", ".join("%.3f" % r for r in ratios)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(selftest() if "--selftest" in a else main(a))
