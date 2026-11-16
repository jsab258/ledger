#!/usr/bin/env python3
"""Darren's purple and teal nylon jacket as one job for Kiln (run_job_script.py) or Marvelous (md_job.py): Tom's zip
jacket re-cut (FreeSewing's Brian at Sam's measures with a looser blouson ease; two fronts, a whole back, two
one-piece sleeves, a rib band at the hem in three parts, rib cuffs, a stand collar, the zip drawn closed between two
tapes), placed on the body's arrangement points by name, sewn, draped and exported.

    python tools/md-bridge/nylon_jacket.py --draft BRIAN.json [--meas MEAS.json] [--chest-ease 0.22]
    python tools/md-bridge/nylon_jacket.py BRIAN.json JOB.py [--out DIR] [--avatar BODY] [--steps 400]
    python F:/LedgerTools/tool-dev/kiln/python/run_job_script.py JOB.py RESULT.json     # Kiln
    python tools/md-bridge/md_job.py JOB.py                                              # Marvelous (an .avt needed)
    python tools/md-bridge/nylon_jacket.py --selftest

WHY, 16 November 2026 (his decision: the practice garments' patterns from our own pattern tools straight into
Kiln's job format, Marvelous not needed; production/art/clothing/BREADTH-PATTERNS-2026-11-16.md, section 4; casting:
"shiny purple and teal nylon shell-suit jacket", production/casting/darren-milner/SHEET.md). The draft is Brian
(FreeSewing, MIT) drafted by the project's drafter (tools/meshgen/freesewing_draft.mjs, F:/LedgerTools/freesewing)
at Sam's measures with chest ease CHEST_EASE (the note's 20 to 25%, a guess; Tom's jacket had Brian's default 15%),
every other option Brian's default as Tom's was. --draft writes it with its "measurements" block, and the job reads
the measures from the draft as work_trousers.py does. zip_jacket.py's build, seams and arrangement are imported, not
copied.

THE MEASURES AND THE BODY: the only measured set for Sam is MH_SamC5's (F:/LedgerTools/bodies/MH_SamC5/
measurements.json: chest 1025.2, biceps 327.7, wrist 191.6 ...); MH_SamS6, the game's body, has no measurement file
(its folder holds the body and its build record: moved from C5 by 37 mm on average, 56 at most). Measuring S6 needs
Blender, which this task did not run. So the draft is at C5's measures and the job drapes on S6's body
(BODY; --avatar takes another); the girth difference this leaves is not known until S6 is measured.

THE CHANGES FROM TOM'S JACKET: the looser chest; the cuffs cut to Sam's wrist (zip_jacket.py hard-codes Tom's
197.1 mm, so the cut is given as Sam's wrist over Tom's); the rib band and cuffs stand for the elastic hem and cuffs
(the rib's own weft shrinkage draws them in, Kiln's Rib Knit numbers); a thin crisp nylon's physics. No hip welts:
none is asked for, and the zip jacket's welts were a map detail. THE TWO COLOURS are not separate pieces: they are
an ID-mask map over the drape's UV islands (the Hook list's "two-colour maps"), and the plan's "colours" names a
first split (teal above each front's and the back's armhole foot and on each sleeve's cap above the biceps line,
purple elsewhere) only as a starting place: where the colours fall is a look, decided at the gate, not here.

WHAT THIS JOB LEAVES OUT: the carry from C5's measures to S6 (the note's caution; here the drape is made on S6
directly from a C5 draft); Marvelous's elastic, freeze and grip stages of the zip jacket's cuff tries (their
lessons are recorded there; Kiln's rib shrinkage stands in); any pose but standing. Carried-over risks the note
names: Tom's stand collar showed his throat (set aside after four tries) and the rib cuffs needed three.

THE CLOTH (its physics only): on Marvelous its stock taffeta (a crisp woven; whether it is nylon's is unverified),
rib knit and canvas (the tapes); on Kiln our own descriptions beside the job (<name>.drape-fabric.json). ESTIMATES.
"""
import json
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zip_jacket  # noqa: E402
from zip_jacket import ARRANGE, CORNER, CURVE, RIB_BAND, area, build as zip_build, length, load, seams, welts  # noqa: E402,F401

sys.path.insert(0, "F:/LedgerTools/tool-dev")
from outpath import checked  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRAFTER = os.path.join(REPO, "tools", "meshgen", "freesewing_draft.mjs")
MODULES = r"F:\LedgerTools\freesewing\node_modules"
MEAS = r"F:\LedgerTools\bodies\MH_SamC5\measurements.json"
OUT_DIR = r"F:\LedgerTools\garments\darren\kiln-breadth-2026-11-16"
DRAFT = os.path.join(OUT_DIR, "brian-darren.json")
BODY = r"F:\LedgerTools\bodies\MH_SamS6\MH_SamS6_Body.fbx"
CHEST_EASE = 0.22             # a guess inside the note's 20 to 25% (Tom's 15%)
BRIAN_BICEPS_EASE = 0.15      # Brian's default, as drafted
ORDER = ["frontR", "frontL", "back", "sleeveR", "sleeveL", "bandFrontR", "cuffR", "bandFrontL", "cuffL", "bandBack",
         "collar", "tapeR", "tapeL"]
# THE FABRICS, Kiln's units (doc.rs, struct Fabric). ESTIMATES, none measured: a thin, crisp, shiny nylon about
# 90 g/m2 and 0.15 mm (Kiln's MIT nylon ripstop is 58.5 g/m2, 0.076 mm), little stretch, crisper in bending than
# Kiln's Silk Charmeuse (5); the rib Kiln's own Rib Knit (doc.rs); the tapes as Kiln's Stiff Interlining.
NYLON = {"name": "darren_nylon", "color": [96, 40, 120], "stretch_weft": 90.0, "stretch_warp": 92.0, "shear": 70.0,
         "bending_weft": 12.0, "bending_warp": 12.0, "density": 90.0, "friction": 20.0, "thickness": 0.15,
         "damping": 10.0}
RIB = {"name": "darren_rib", "color": [96, 40, 120], "stretch_weft": 50.0, "stretch_warp": 60.0, "shear": 30.0,
       "bending_weft": 20.0, "bending_warp": 25.0, "density": 300.0, "friction": 60.0, "thickness": 1.2,
       "shrink_weft": 10.0, "damping": 10.0}
TAPE = {"name": "darren_zip_tape", "color": [30, 30, 34], "stretch_weft": 96.0, "stretch_warp": 96.0, "shear": 90.0,
        "bending_weft": 95.0, "bending_warp": 95.0, "density": 250.0, "friction": 30.0, "thickness": 1.0,
        "damping": 10.0}
FABRICS = {"nylon": {"md": "V2_Woven_Taffeta_1.zfab", "kiln": NYLON},
           "rib": {"md": "V2_Cut_Sew_Knit_Rib_1.zfab", "kiln": RIB},
           "tape": {"md": "V2_Woven_Canvas_1.zfab", "kiln": TAPE}}
ESTIMATE_NOTE = ("ESTIMATES (16 Nov 2026, tools/md-bridge/nylon_jacket.py): not measured; a thin crisp nylon about "
                 "90 g/m2; the rib Kiln's Rib Knit; stiffness set by judgement against Kiln's presets (doc.rs). Check "
                 "them against the drape before trusting them.")


def measures(path):
    return json.load(open(path, encoding="utf-8"))["measurements"]


def draft(out, meas_path=MEAS, chest_ease=CHEST_EASE):
    """Brian at the measures in meas_path, by the project's FreeSewing drafter (node)."""
    out = checked(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    meas = measures(meas_path)
    args = ["node", DRAFTER, MODULES, "brian"] + ["%s=%s" % kv for kv in meas.items()] + [
        "opt.chestEase=%g" % chest_ease, out]
    return subprocess.call(args)


def build(brian, meas):
    """zip_jacket's thirteen pieces, the cuffs cut to this body's wrist (its module's WRIST_MM is Tom's)."""
    return zip_build(brian, 0.0, meas["wrist"] / zip_jacket.WRIST_MM * zip_jacket.CUFF_OF_WRIST)


def colours(brian):
    """A first split for the ID-mask map, in each piece's pattern coordinates (left front as drafted, right
    mirrored; the back whole, its centre at x = 0; the sleeves as drafted): a starting place for the look gate."""
    fn, bn, sn = brian["brian.front"][1], brian["brian.back"][1], brian["library.sleeve"][1]
    out = {"default": "purple", "regions": []}
    for s in ("R", "L"):
        out["regions"].append({"piece": "front" + s, "colour": "teal", "above_y": round(fn["armhole"][1], 1)})
        out["regions"].append({"piece": "sleeve" + s, "colour": "teal",
                               "above_y": round(max(sn["bicepsLeft"][1], sn["bicepsRight"][1]), 1)})
    out["regions"].append({"piece": "back", "colour": "teal", "above_y": round(bn["armhole"][1], 1)})
    out["note"] = "a first split only (a guess); where the colours fall is decided at the look gate"
    return out


def plan(brian, meas):
    pieces = build(brian, meas)
    out_pieces, lines = [], {}
    for key in ORDER:
        edges = pieces[key]
        pts = []
        for k, (seg, a, b) in enumerate(edges):
            lines[(key, a, b)] = (k, True)
            lines[(key, b, a)] = (k, False)
            pts.append([round(seg[0][0], 2), round(seg[0][1], 2), CORNER])
            pts += [[round(x, 2), round(y, 2), CURVE] for x, y in seg[1:-1]]
        out_pieces.append({"key": key, "points": pts, "arrange": ARRANGE[key],
                           "fabric": "rib" if key.startswith(("band", "cuff")) else "tape" if key.startswith("tape") else "nylon"})
    out_seams = []
    for (pa, a0, a1), (pb, b0, b1) in seams():
        la, fa = lines[(pa, a0, a1)]
        lb, fb = lines[(pb, b0, b1)]
        out_seams.append({"a": [pa, la, fa], "b": [pb, lb, fb], "names": [a0, a1, b0, b1]})
    corners = {key: [[a, round(seg[0][0], 2), round(seg[0][1], 2)] for seg, a, _b in pieces[key]] for key in ORDER}
    patch = {}
    for s in ("R", "L"):
        patch["front" + s] = {"bottom": ["cfHem" + s, "hem" + s], "top": ["shoulder" + s, "cfNeck" + s]}
        patch["sleeve" + s] = {"bottom": ["wristLeft" + s, "wristRight" + s], "top": ["bicepsRight" + s, "bicepsLeft" + s]}
        patch["bandFront" + s] = {"bottom": ["bandCfLow" + s, "bandSideLow" + s], "top": ["bandSide" + s, "bandCf" + s]}
        patch["cuff" + s] = {"bottom": ["cuffAlow" + s, "cuffBlow" + s], "top": ["cuffB" + s, "cuffA" + s]}
        patch["tape" + s] = {"bottom": ["tape%sLowO" % s, "tape%sLowI" % s], "top": ["tape%sTopI" % s, "tape%sTopO" % s]}
    patch["back"] = {"bottom": ["hemL", "hemR"], "top": ["shoulderR", "shoulderL"]}
    patch["bandBack"] = {"bottom": ["bandBackLowL", "bandBackLowR"], "top": ["bandBackR", "bandBackL"]}
    patch["collar"] = {"bottom": ["colCfL", "colCfR"], "top": ["colTopCfR", "colTopCfL"]}
    return {"pieces": out_pieces, "seams": out_seams, "corners": corners, "patch": patch, "colours": colours(brian),
            "cut": {"chest_ease_drafted": CHEST_EASE, "cuff_mm": round(meas["wrist"] * zip_jacket.CUFF_OF_WRIST, 1),
                    "rib_band_of_edge": RIB_BAND, "measures_from": "MH_SamC5 (S6 not measured)"}}


JOB = '''# Generated by tools/md-bridge/nylon_jacket.py from %(src)s: Darren's nylon jacket made, placed on the body's
# arrangement points by name, sewn, draped (%(steps)d steps at 20 mm, 200 at 10 mm with the rib and collar at 6 and the
# zip tapes at 4, 100 at Fitting) and exported to %(out)s. Runs on Kiln (run_job_script.py) or Marvelous (md_job.py).
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
        pattern_api.SetArrangement(idx, points[p["arrange"]])
        if p["key"].startswith(("cuff", "sleeve")):
            pattern_api.SetArrangementShapeStyle(idx, "Curved")
result["made"] = made
result["arranged"] = {p["key"]: p["arrange"] in points for p in PLAN["pieces"]}
result["sewn"] = [bool(pattern_api.AddSeamlinePairGroup(made[s["a"][0]], s["a"][1], made[s["b"][0]], s["b"][1], s["a"][2], s["b"][2]))
                  for s in PLAN["seams"]]
# THE CLOTH: Marvelous's stock files where they are and this is Marvelous; on Kiln our own descriptions beside the job
ON_KILN = type(fabric_api).__name__ == "_Module"
FAB = r"C:\\Users\\Public\\Documents\\MarvelousDesigner\\New Assets\\Fabric"
FABRICS = %(fabrics)r
fabrics, used = {}, {}
for name, f in FABRICS.items():
    lib = os.path.join(FAB, f["md"])
    path = lib if (not ON_KILN and os.path.isfile(lib)) else f["own"]
    if ON_KILN or os.path.isfile(path):
        fabrics[name] = fabric_api.AddFabric(path)
        used[name] = path
for p in PLAN["pieces"]:
    if p.get("fabric") in fabrics:
        fabric_api.AssignFabricToPattern(fabrics[p["fabric"]], made[p["key"]], 1)
result["fabrics"] = used
pattern_api.SetParticleDistanceOfPatterns(20.0)
result["settled20"] = bool(utility_api.Simulate(%(steps)d))
pattern_api.SetParticleDistanceOfPatterns(10.0)
for p in PLAN["pieces"]:
    if p["key"].startswith(("band", "cuff", "collar")):
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], 6.0)
    if p["key"].startswith("tape"):
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], 4.0)
result["settled10"] = bool(utility_api.Simulate(200))
try:
    utility_api.SetSimulationQuality(2, 0)
    result["fitting"] = "set: 2 Fitting, CPU"
except Exception as e:
    result["fitting"] = "refused: %%s" %% e
result["simulated"] = bool(utility_api.Simulate(100))
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = True
eo.bSingleObject = False
eo.scale = 1.0
result["exported"] = export_api.ExportOBJ(os.path.join(OUT, "nylon_jacket.obj"), eo)
result["zprj"] = export_api.ExportZPrj(os.path.join(OUT, "nylon_jacket.zprj"))
log("nylon jacket made, sewn and draped")
'''


def write_fabrics(folder):
    out = {}
    for name, f in FABRICS.items():
        d = dict(f["kiln"])
        d["_estimates"] = ESTIMATE_NOTE
        json.dump(d, open(checked(os.path.join(folder, d["name"] + ".drape-fabric.json")), "w", encoding="utf-8"), indent=1)
        out[name] = {"md": f["md"], "own": os.path.join(folder, d["name"] + ".zfab")}   # never a file: Kiln reads beside it
    return out


def girths(brian, meas, pieces):
    """The draft's chest (at the armhole line) against the body's plus ease, the sleeve's biceps against the floor
    of the body's plus Brian's biceps ease; the hem and
    collar rounds; the back's length (mm)."""
    fn, bn, sn = brian["brian.front"][1], brian["brian.back"][1], brian["library.sleeve"][1]
    chest = 2 * abs(fn["armhole"][0] - fn["cfNeck"][0]) + 2 * abs(bn["armhole"][0] - bn["cbNeck"][0])
    biceps = math.dist(sn["bicepsLeft"], sn["bicepsRight"])
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    hem = length(E("frontR", "cfHemR", "hemR")) + length(E("frontL", "cfHemL", "hemL")) + length(E("back", "hemL", "hemR"))
    band = sum(length(E(k, a, b)) for k, a, b in (("bandFrontR", "bandCfR", "bandSideR"), ("bandFrontL", "bandCfL", "bandSideL"),
                                                    ("bandBack", "bandBackL", "bandBackR")))
    neck = length(E("frontR", "hpsR", "cfNeckR")) + length(E("back", "hpsR", "hpsL")) + length(E("frontL", "hpsL", "cfNeckL"))
    cuff = length(E("cuffR", "cuffAR", "cuffBR"))
    back = abs(bn["cbNeck"][1] - bn["cbHem"][1])
    return {"chest": (chest, meas["chest"] * (1 + CHEST_EASE)), "biceps": (biceps, meas["biceps"] * (1 + BRIAN_BICEPS_EASE)),
            "hem": (hem, None), "band": (band, hem * RIB_BAND), "neck": (neck, None), "cuff": (cuff, meas["wrist"]),
            "back": (back, None)}


def main(argv):
    src, job = argv[0], checked(argv[1])
    opt = lambda k, d: float(argv[argv.index(k) + 1]) if k in argv else d  # noqa: E731
    sarg = lambda k, d: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
    out = checked(sarg("--out", os.path.join(OUT_DIR, "nylon_jacket")))
    brian, meas = load(src), measures(src)
    p = plan(brian, meas)
    steps = int(opt("--steps", 400))
    fab = write_fabrics(os.path.dirname(os.path.abspath(job)))
    open(job, "w", encoding="utf-8").write(JOB % {"src": src, "plan": json.dumps(p), "out": out, "steps": steps,
                                                  "fabrics": fab, "avt": sarg("--avatar", BODY)})
    json.dump(p, open(checked(job[:-3] + ".plan.json"), "w", encoding="utf-8"), indent=1)
    print("nylon jacket: %d pieces, %d seams -> %s" % (len(p["pieces"]), len(p["seams"]), job))
    for k, (got, want) in girths(brian, meas, build(brian, meas)).items():
        print("  %-6s %.1f mm%s" % (k, got, "" if want is None else " (against %.1f, %+.2f%%)" % (want, 100 * (got / want - 1))))
    for q in p["pieces"]:
        print("  %-11s %3d points  on %s  (%s)" % (q["key"], len(q["points"]), q["arrange"], q["fabric"]))


def _check(brian, meas, label, ease=True):
    """The structure on any Brian draft; the ease checks only on a draft made at CHEST_EASE."""
    ok, msg = [], []
    pieces = build(brian, meas)
    p = plan(brian, meas)
    keys = [q["key"] for q in p["pieces"]]
    ok.append(sorted(keys) == sorted(ORDER) and len(set(keys)) == len(keys) == 13)
    for key, edges in pieces.items():
        names = [a for _s, a, _b in edges]
        ok.append(len(names) == len(set(names)))
    ok.append(len(p["seams"]) == len(seams()) == 29)
    # every seam by its named ends: plain seams 1:1 within 3%, a sleeve cap up to 12% long (eased in), rib bands
    # RIB_BAND of their edge, the cuffs against the sleeve end free (cut to the wrist, gathered by the rib)
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    ratios = []
    for (pa, a0, a1), (pb, b0, b1) in seams():
        r = length(E(pa, a0, a1)) / length(E(pb, b0, b1))
        ratios.append(r)
        if pa.startswith("band") and not pb.startswith("band"):
            ok.append(abs(r - RIB_BAND) < 0.005)
        elif pa.startswith("cuff") and pb.startswith("sleeve"):
            ok.append(r < 1.0)
        elif pa.startswith("sleeve") and pb != pa:
            ok.append(0.97 <= r <= 1.12)
        else:
            ok.append(0.97 <= r <= 1.03)
    g = girths(brian, meas, pieces)
    if ease:
        ok.append(abs(g["chest"][0] / g["chest"][1] - 1) <= 0.01)
    # the sleeve at its biceps line no narrower than the biceps plus Brian's biceps ease (Brian widens the sleeve
    # beyond it so its cap fits the armhole; the cap against the armhole is checked with the seams)
    ok.append(g["biceps"][0] >= g["biceps"][1])
    ok.append(abs(g["cuff"][0] - meas["wrist"] * zip_jacket.CUFF_OF_WRIST) < 0.5)
    ok.append(abs(g["band"][0] / g["band"][1] - 1) < 0.002)
    # the back's length: Brian's centre back from the neck to hip level (hps to waist back plus waist to hips, less
    # the neck's drop, about 15 to 30 mm): within 40 mm
    want_back = meas["hpsToWaistBack"] + meas["waistToHips"]
    ok.append(abs(g["back"][0] - want_back) <= 40.0)
    # the areas against the draft within 1%
    poly = lambda pts: abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1] for k in range(len(pts))) / 2)  # noqa: E731
    for key, want in (("back", 2 * poly(brian["brian.back"][0])), ("frontR", poly(brian["brian.front"][0])),
                      ("frontL", poly(brian["brian.front"][0])), ("sleeveR", poly(brian["library.sleeve"][0]))):
        ok.append(abs(area(pieces[key]) / want - 1) <= 0.01)
    msg.append("  %s: chest %.1f (body %.1f + ease = %.1f), biceps %.1f (at least %.1f), hem %.1f, band %.1f, neck %.1f, cuff %.1f, "
               "back %.1f (hps-waist-hips %.1f); seam ratios %.3f to %.3f" % (
                   label, g["chest"][0], meas["chest"], g["chest"][1], g["biceps"][0], g["biceps"][1], g["hem"][0],
                   g["band"][0], g["neck"][0], g["cuff"][0], g["back"][0], want_back, min(ratios), max(ratios)))
    return ok, msg


def selftest():
    import contextlib
    import io
    ok, msg = [], []
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            checked("jacket/x.json")
        ok.append(False)
    except SystemExit:
        ok.append(True)
    fields = {"name", "color", "stretch_weft", "stretch_warp", "shear", "bending_weft", "bending_warp", "density",
              "friction", "thickness", "shrink_weft", "shrink_warp", "damping", "texture", "texture_scale", "texture_angle"}
    for f in FABRICS.values():
        ok.append(set(f["kiln"]) <= fields and "wool" not in f["kiln"]["name"])
    ok.append(set(ORDER) <= set(ARRANGE))
    if os.path.isfile(DRAFT):
        brian, meas = load(DRAFT), measures(DRAFT)
        # the draft's measures are Sam's measured set (C5's file)
        ok.append(meas == measures(MEAS))
        o, m = _check(brian, meas, "Darren")
        ok += o
        msg += m
        # the colour split's lines lie inside their pieces
        for r in colours(brian)["regions"]:
            ys = [y for seg, _a, _b in build(brian, meas)[r["piece"]] for _x, y in seg]
            ok.append(min(ys) < r["above_y"] < max(ys))
    else:
        msg.append("  (no Darren draft on this machine: his pattern checks skipped)")
    # NO SPECIAL-CASE NUMBERS FOR ONE BODY: the same structure on Tom's jacket draft (26 October, Brian's 15%)
    tom = r"F:\LedgerTools\garments\tom\pattern\brian.json"
    if os.path.isfile(tom):
        o, m = _check(load(tom), measures(tom), "Tom", ease=False)
        ok += o
        msg += m
    # zip_jacket's module left as found (its wrist is Tom's; this file never changes it)
    ok.append(zip_jacket.WRIST_MM == 197.1)
    print("\n".join(msg))
    print("nylon jacket selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--draft" in a:
        sys.exit(draft(a[a.index("--draft") + 1], a[a.index("--meas") + 1] if "--meas" in a else MEAS,
                       float(a[a.index("--chest-ease") + 1]) if "--chest-ease" in a else CHEST_EASE))
    sys.exit(main(a))
