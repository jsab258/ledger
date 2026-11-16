#!/usr/bin/env python3
"""Ron's dark wool work trousers as one job for Kiln (run_job_script.py) or Marvelous (md_job.py): jeans.py's route
(FreeSewing's Titan, two fronts, two backs, a waistband in two halves, placed on the body's leg and waist points by
name, sewn, draped, exported) with a work trouser's draft, a wool twill's physics and a plain straight hem.

    python tools/md-bridge/work_trousers.py TITAN.json JOB.py [--out DIR] [--avatar BODY] [--steps 400] [--settle]
        [--front-position X,Y,OFFSET] [--hem-round MM] [--break MM]
    python F:/LedgerTools/tool-dev/kiln/python/run_job_script.py JOB.py RESULT.json     # Kiln
    python tools/md-bridge/md_job.py JOB.py                                              # Marvelous (an .avt needed)
    python tools/md-bridge/work_trousers.py --selftest

WHY, 16 November 2026 (advisor 172; production/art/clothing/RON-KILN-OUTFIT-PLAN-2026-11-16.md, section 2, step 5):
Kiln's M6 outfit is Ron's donkey jacket and dark wool work trousers from the breadth set, refit to MH_RoccoP2; the
trousers are not a recoloured variant of the jeans (DECISIONS 16 Nov 07:09). The draft is Titan at Ron's measures
(F:/LedgerTools/garments/ron/kiln-outfit-2026-11-16/titan-ron-trousers.json: seat ease 11%, knee ease 10%, the
waist at the natural waist, a straight leg, cuffless). jeans.py's build, seams, patch corners and simulation stages are
imported, not copied; the crease and the fly are drawn in the normal map, as the jeans' fly and pockets are.

THE HEM: Titan's leg runs straight down from the knee, so the hem's round is the knee's (the plan asks a hem wider
than the jeans' 419 mm, about 460 to 480). It is kept as drafted unless --hem-round asks a narrower one (jeans.py's
taper only draws a leg in). The leg is shortened only if the draft runs past the body's waist-to-floor less a break
of BREAK mm over the boot: Titan adds its own length bonus, so the draft's waist-to-floor is longer than the body's,
and the overshoot comes off below the knee (jeans.shorten), measured from the draft's own waist line (waistX).

THE CLOTH (its physics only): on Marvelous its stock flannel (a woven wool-type cloth; whether its physics is wool's
is unverified), on Kiln, which cannot read that file, our own description beside the job (<name>.drape-fabric.json,
read by Kiln's fabric_for_file; F:/LedgerTools/tool-dev/kiln/python/kiln_front/compat.py). Its numbers are estimates
(WOOL_TWILL below). Nothing here is a measure of one body: every length and girth comes from the draft and its own
"measurements".
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jeans  # noqa: E402
from jeans import SIM_PLAIN, SIM_SETTLE, WAISTBAND_OF_WAIST  # noqa: E402
from zip_jacket import length, load  # noqa: E402

TITAN = r"F:\LedgerTools\garments\ron\kiln-outfit-2026-11-16\titan-ron-trousers.json"
OUT_DIR = r"F:\LedgerTools\garments\ron\kiln-outfit-2026-11-16"
BODY = r"F:\LedgerTools\bodies\MH_RoccoP2\MH_RoccoP2_FullBody.fbx"
BREAK = 25.0          # mm the hem stops short of the floor: a plain trouser's break over a boot
# the draft's own options as drafted on 16 Nov (FreeSewing Titan; the draft file keeps its measures, not its options)
SEAT_EASE, KNEE_EASE = 0.11, 0.10
PLAN_HEM = (460.0, 480.0)   # the plan's hem round, step 2 (a guess there: no dated photograph found)
# THE FABRIC: "md" Marvelous's stock file (its physics only), "kiln" our own in Kiln's units (doc.rs, struct Fabric:
# stretch, shear, bending 0..100, density g/m2, thickness mm). ESTIMATES, none measured: a work trouser's wool twill
# about 10 oz/yd2 (about 340 g/m2), under a millimetre thick, stiffer than Kiln's Cotton Twill (80/82/60/35) and softer
# in bending than its Denim (92/94/75/70). The name avoids "wool": if the description failed to load, Kiln picks a
# preset by name, and "wool" is its low-gauge sweater knit.
WOOL_TWILL = {"name": "ron_trouser_twill", "color": [44, 46, 52], "stretch_weft": 88.0, "stretch_warp": 90.0,
              "shear": 70.0, "bending_weft": 45.0, "bending_warp": 48.0, "density": 340.0, "friction": 40.0,
              "thickness": 0.9, "damping": 12.0}
FABRIC_MD = "V2_Woven_Flannel_1.zfab"
ESTIMATE_NOTE = ("ESTIMATES (16 Nov 2026, tools/md-bridge/work_trousers.py): not measured; a wool trouser twill about "
                 "340 g/m2; stiffness set by judgement against Kiln's presets (doc.rs). Check them against the drape "
                 "before trusting them.")


def measures(path):
    return json.load(open(path, encoding="utf-8"))["measurements"]


def shorten_for(titan, meas, brk=BREAK):
    """How much the leg comes up: the draft's waist line to its floor against the body's waist-to-floor less brk."""
    fn = titan["titan.front"][1]
    drafted = fn["waistX"][1] - fn["floorOut"][1]
    return max(0.0, drafted - (meas["waistToFloor"] - brk)), drafted


def drafted_hem(titan):
    """The draft's hem round, front and back hem widths together (Titan: the knee's, straight down)."""
    fn, bn = titan["titan.front"][1], titan["titan.back"][1]
    return abs(fn["floorIn"][0] - fn["floorOut"][0]) + abs(bn["floorIn"][0] - bn["floorOut"][0])


def plan(titan, meas, hem_round=None, brk=BREAK):
    """jeans.plan with the hem kept as drafted (or hem_round), the leg shortened only past the break; jeans.build
    reads its hem from the module, so it is set for the one call and put back."""
    s, drafted = shorten_for(titan, meas, brk)
    keep = jeans.HEM_ROUND
    jeans.HEM_ROUND = hem_round if hem_round else drafted_hem(titan)
    try:
        p = jeans.plan(titan, s)
    finally:
        jeans.HEM_ROUND = keep
    for q in p["pieces"]:
        q["fabric"] = "wool"
    p["cut"].update({"break_mm": brk, "draft_waist_to_floor_mm": round(drafted, 1),
                     "body_waist_to_floor_mm": meas["waistToFloor"], "hem_as_drafted": not hem_round})
    return p, s


def build(titan, meas, hem_round=None, brk=BREAK):
    s, _ = shorten_for(titan, meas, brk)
    keep = jeans.HEM_ROUND
    jeans.HEM_ROUND = hem_round if hem_round else drafted_hem(titan)
    try:
        return jeans.build(titan, s)
    finally:
        jeans.HEM_ROUND = keep


def girths(titan, meas, pieces):
    """The draft's seat, knee and hem rounds against the body's plus the draft's ease (mm)."""
    fn, bn = titan["titan.front"][1], titan["titan.back"][1]
    seat = 2 * (math.dist(fn["seatOut"], fn["cfSeat"]) + math.dist(bn["seatOut"], bn["cbSeat"]))
    knee = math.dist(fn["kneeOut"], fn["kneeIn"]) + math.dist(bn["kneeOut"], bn["kneeIn"])
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    hem = length(E("frontR", "fFloorOutR", "fFloorInR")) + length(E("backR", "bFloorInR", "bFloorOutR"))
    wf = length(E("frontR", "fWaistInR", "fWaistOutR"))
    wb = length(E("backR", "bWaistOutR", "bWaistInR"))
    band = length(E("waistbandR", "wbCFR", "wbSideR")) + length(E("waistbandR", "wbSideR", "wbCBR"))
    return {"seat": (seat, meas["seat"], meas["seat"] * (1 + SEAT_EASE)),
            "knee": (knee, meas["knee"], meas["knee"] * (1 + KNEE_EASE)),
            "hem": (hem, None, None), "trouserWaist": (2 * (wf + wb), meas["waist"], None),
            "band": (2 * band, meas["waist"], None)}


JOB = '''# Generated by tools/md-bridge/work_trousers.py from %(src)s: Ron's work trousers made, placed on the body's points
# by name, sewn, draped (%(steps)d steps at 20 mm, 200 at 10 mm, 100 at Fitting) and exported to %(out)s. Runs on
# Kiln (run_job_script.py) or Marvelous (md_job.py).
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
# THE CLOTH: Marvelous's stock file where it is and this is Marvelous; on Kiln (its modules are stand-ins that cannot
# read a locked fabric) our own description, <name>.drape-fabric.json beside the job
ON_KILN = type(fabric_api).__name__ == "_Module"
FAB = r"C:\\Users\\Public\\Documents\\MarvelousDesigner\\New Assets\\Fabric"
lib = os.path.join(FAB, %(fabric_md)r)
path = lib if (not ON_KILN and os.path.isfile(lib)) else %(fabric_own)r
fabrics = {}
if ON_KILN or os.path.isfile(path):
    fabrics["wool"] = fabric_api.AddFabric(path)
for p in PLAN["pieces"]:
    if p.get("fabric") in fabrics:
        fabric_api.AssignFabricToPattern(fabrics[p["fabric"]], made[p["key"]], 1)
result["fabrics"] = {k: path for k in fabrics}
%(simulate)s
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = True
eo.bSingleObject = False
eo.scale = 1.0
result["exported"] = export_api.ExportOBJ(os.path.join(OUT, "work_trousers.obj"), eo)
result["zprj"] = export_api.ExportZPrj(os.path.join(OUT, "work_trousers.zprj"))
log("work trousers made, sewn and draped")
'''


def write_fabric(folder):
    d = dict(WOOL_TWILL)
    d["_estimates"] = ESTIMATE_NOTE
    json.dump(d, open(os.path.join(folder, d["name"] + ".drape-fabric.json"), "w", encoding="utf-8"), indent=1)
    return os.path.join(folder, d["name"] + ".zfab")       # never a file: Kiln reads the description beside it


def report(g):
    out = []
    for k in ("seat", "knee"):
        got, body, want = g[k]
        out.append("%s %.1f mm round, body %.1f + ease = %.1f (%+.2f%%)" % (k, got, body, want, 100 * (got / want - 1)))
    out.append("hem %.1f mm round (the plan's %d-%d; the jeans' 419)" % (g["hem"][0], PLAN_HEM[0], PLAN_HEM[1]))
    out.append("trousers' waist edge %.1f, band %.1f (%.3f of it; %.3f of the body's waist %.1f)" % (
        g["trouserWaist"][0], g["band"][0], g["band"][0] / g["trouserWaist"][0], g["band"][0] / g["band"][1], g["band"][1]))
    return out


def main(argv):
    src, job = argv[0], argv[1]
    opt = lambda n, d: float(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
    sarg = lambda n, d: argv[argv.index(n) + 1] if n in argv else d  # noqa: E731
    out = sarg("--out", os.path.join(OUT_DIR, "work_trousers"))
    titan, meas = load(src), measures(src)
    hem = opt("--hem-round", 0.0) or None
    brk = opt("--break", BREAK)
    p, s = plan(titan, meas, hem, brk)
    steps = int(opt("--steps", 400))
    sim = SIM_SETTLE % {"rest20": max(1, steps - 100)} if "--settle" in argv else SIM_PLAIN % {"steps": steps}
    # --front-position X,Y,OFFSET as jeans.py (the fronts lifted clear of the feet at the start)
    front = ""
    if "--front-position" in argv:
        fp = [int(t) for t in sarg("--front-position", "").split(",")]
        front = ('\n        if p["key"].startswith("front"):\n'
                 '            pattern_api.SetArrangementPosition(idx, %d, %d, %d)' % tuple(fp))
    own = write_fabric(os.path.dirname(os.path.abspath(job)))
    open(job, "w", encoding="utf-8").write(JOB % {
        "src": src, "plan": json.dumps(p), "out": out, "steps": steps, "fabric_md": FABRIC_MD, "fabric_own": own,
        "simulate": sim, "front": front, "avt": sarg("--avatar", BODY)})
    json.dump(p, open(job[:-3] + ".plan.json", "w", encoding="utf-8"), indent=1)
    print("work trousers: %d pieces, %d seams -> %s (leg shortened %.1f mm)" % (len(p["pieces"]), len(p["seams"]), job, s))
    for line in report(girths(titan, meas, build(titan, meas, hem, brk))):
        print("  " + line)
    for q in p["pieces"]:
        print("  %-10s %3d points  on %s" % (q["key"], len(q["points"]), q["arrange"]))


def _structure(titan, meas, label):
    """Seams paired by named ends, the band's cut, the length: on any Titan draft."""
    ok, msg = [], []
    p, s = plan(titan, meas)
    pieces = build(titan, meas)
    keys = [q["key"] for q in p["pieces"]]
    ok.append(keys == ["frontR", "frontL", "backR", "backL", "waistbandR", "waistbandL"] and len(p["seams"]) == 12)
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    ratios = []
    for (pa, a0, a1), (pb, b0, b1) in jeans.seams():
        r = length(E(pa, a0, a1)) / length(E(pb, b0, b1))
        ratios.append(r)
        band = pa.startswith("waistband") and not pb.startswith("waistband")
        ok.append(abs(r - WAISTBAND_OF_WAIST) < 0.005 if band else 0.97 <= r <= 1.03)
    # the hem: from the draft's waist line it ends the break short of the body's waist-to-floor, or where drafted
    fn = titan["titan.front"][1]
    hem_y = min(y for seg, a, b in pieces["frontR"] for x, y in seg)
    drop = fn["waistX"][1] - hem_y
    _, drafted = shorten_for(titan, meas)
    ok.append(abs(drop - min(drafted, meas["waistToFloor"] - BREAK)) < 1.0)
    # the left leg the right's mirror
    ok.append(abs(length(E("frontL", "fWaistOutL", "fFloorOutL")) - length(E("frontR", "fWaistOutR", "fFloorOutR"))) < 0.5)
    msg.append("  %s: leg shortened %.1f mm (draft waist to floor %.1f, body %.1f less %.0f); hem %.1f mm under the "
               "waist line; seam ratios %s" % (label, s, drafted, meas["waistToFloor"], BREAK, drop,
                                               ", ".join("%.3f" % r for r in ratios)))
    return ok, msg, pieces


def selftest():
    ok, msg = [], []
    if not os.path.isfile(TITAN):
        print("work trousers selftest: passed=0/0 failed=0 (no draft on this machine)")
        return 0
    titan, meas = load(TITAN), measures(TITAN)
    o, m, pieces = _structure(titan, meas, "Ron")
    ok += o
    msg += m
    g = girths(titan, meas, pieces)
    # the girths: the draft's seat and knee within 0.5% of the body's plus the draft's ease; the hem as drafted (the
    # knee's, straight down) and inside the plan's range; the band 0.97 of the trousers' waist and not under his waist
    for k in ("seat", "knee"):
        ok.append(abs(g[k][0] / g[k][2] - 1) <= 0.005)
    ok.append(abs(g["hem"][0] - drafted_hem(titan)) < 0.5 and PLAN_HEM[0] <= g["hem"][0] <= PLAN_HEM[1])
    ok.append(abs(g["band"][0] / g["trouserWaist"][0] - WAISTBAND_OF_WAIST) < 0.002)
    ok.append(g["band"][0] >= g["band"][1])
    msg += ["  Ron: " + line for line in report(g)]
    # NO SPECIAL-CASE NUMBERS FOR ONE BODY: the same structure on Tom's jeans draft (30 October, jeans' ease)
    tom = r"F:\LedgerTools\garments\tom\jeans\pattern\titan-jeans.json"
    if os.path.isfile(tom) and "measurements" in json.load(open(tom, encoding="utf-8")):
        o, m, _ = _structure(load(tom), measures(tom), "Tom")
        ok += o
        msg += m
    # jeans.py's module left as it was found (its hem is set only for one call)
    ok.append(jeans.HEM_ROUND == 419.0)
    fields = {"name", "color", "stretch_weft", "stretch_warp", "shear", "bending_weft", "bending_warp", "density",
              "friction", "thickness", "shrink_weft", "shrink_warp", "damping", "texture", "texture_scale", "texture_angle"}
    ok.append(set(WOOL_TWILL) <= fields and "wool" not in WOOL_TWILL["name"])
    print("\n".join(msg))
    print("work trousers selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(selftest() if "--selftest" in a else main(a))
