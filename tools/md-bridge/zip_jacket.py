#!/usr/bin/env python3
"""Tom's zip jacket as one Marvelous Designer job: FreeSewing's Brian block at his size cut into a zip-front jacket's
pieces, placed on his avatar's arrangement points, sewn, draped and exported.

    python tools/md-bridge/zip_jacket.py BRIAN.json JOB.py [--steps 400] [--particle 20] [--out DIR]
    python tools/md-bridge/md_job.py JOB.py          # runs it through the bridge (Jafar's one click a session)

WHY, 26 October 2026 (his order of 25 October, item 3: Tom's outfit in Marvelous Designer to Study 6's numbers; his
casting sheet: "a zip-front cotton or nylon jacket for the rain, a plain jumper, jeans, leather shoes"). The pattern
is FreeSewing's Brian (MIT), drafted at Tom's measurements by October's drafter (tools/meshgen/freesewing_draft.mjs;
F:/LedgerTools/garments/tom/pattern/brian.json): a front and a half back of a hip-length body block with jacket ease
(chest 1.23 m on his 1.07 m) and a one-piece sleeve. October's chain (tools/md: jaeger_spec, make_jacket_job,
write_pattern) sews through Marvelous's pattern file because a tailored jacket needs turned seams and folds; a zip
jacket's seams are all plain, so here they are sewn by the API's own AddSeamlinePairGroup, and the pieces are placed
on Tom's own arrangement points (his avatar file, F:/LedgerTools/garments/tom/MH_TomL1.avt, 109 points), where
October had to drape on Marvelous's stock man and swap the body in.

THE PIECES, a 1990 cotton zip jacket of the blouson cut: two fronts (Brian's front, the right as drafted, the left
mirrored), a whole back (Brian's half back mirrored about the centre back), two one-piece sleeves, a rib band at the
hem in three parts (each front's and the back's, sewn at the side seams), a rib cuff at each wrist, and a stand
collar along the whole neckline. The zip is drawn closed: the fronts' centre edges, the bands' and the collar's
front ends are sewn edge to edge (no API call makes a zip; the zip itself is a detail for the game mesh). Rib is cut
shorter than the edge it is sewn to (the band 0.9, the cuff 0.85) so it draws the cloth in, as rib does.

EVERY EDGE IS NAMED BY ITS TWO ENDS (Brian's own points), and a seam pairs two edges by those names, so its
directions follow from which ends meet, not from how each outline happens to wind. Every outline is wound
counter-clockwise with y up, starting on a corner, as Marvelous wants (tools/md/make_jacket_job.py's lessons).
"""
import json
import math
import sys

CORNER, CURVE = 0, 2
RIB_BAND, RIB_CUFF = 0.90, 0.85
BAND_H, CUFF_H, COLLAR_H = 55.0, 60.0, 70.0


def load(path):
    d = json.load(open(path, encoding="utf-8"))
    out = {}
    for part, p in d["parts"].items():
        pts = [[x, -y] for x, y in p["paths"]["seam"]["points"]]     # FreeSewing draws y down
        if pts[0] == pts[-1]:
            pts = pts[:-1]
        names = {n: [x, -y] for n, (x, y) in p["points"].items()}
        out[part] = (pts, names)
    return out


def idx_of(pts, q):
    return min(range(len(pts)), key=lambda k: (pts[k][0] - q[0]) ** 2 + (pts[k][1] - q[1]) ** 2)


def edges_from(pts, corners):
    """corners: [(index, name)] in outline order; returns [(edge points, start name, end name)] closing the loop."""
    out = []
    for k, (i, a) in enumerate(corners):
        j, b = corners[(k + 1) % len(corners)]
        seg = pts[i:j + 1] if j > i else pts[i:] + pts[:j + 1]
        out.append((seg, a, b))
    return out


def mirror_edges(edges):
    """The same edges with x mirrored: the winding flips, so the order and each edge's direction reverse."""
    return [([[-x, y] for x, y in reversed(seg)], b, a) for seg, a, b in reversed(edges)]


def area(edges):
    pts = [p for seg, _, _ in edges for p in seg[:-1]]
    return sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1] for k in range(len(pts))) / 2


def ccw(edges):
    return edges if area(edges) > 0 else [(list(reversed(seg)), b, a) for seg, a, b in reversed(edges)]


def length(seg):
    return sum(math.dist(seg[k], seg[k + 1]) for k in range(len(seg) - 1))


def rect(w, h, names):
    """A rectangle's four edges, counter-clockwise from its bottom left: bottom, right, top, left; names its corners."""
    bl, br, tr, tl = names
    return [([[0, 0], [w, 0]], bl, br), ([[w, 0], [w, h]], br, tr), ([[w, h], [0, h]], tr, tl), ([[0, h], [0, 0]], tl, bl)]


def build(brian, sleeve_shorten=0.0):
    fpts, fn = brian["brian.front"]
    bpts, bn = brian["brian.back"]
    spts, sn = brian["library.sleeve"]
    # THE SLEEVE SHORTENED BELOW THE BICEPS LINE (the second drape: with its cuff the sleeve reached onto the hand):
    # every point under the biceps line drawn up in proportion, so the cap is untouched
    if sleeve_shorten:
        k = 1.0 - sleeve_shorten / -min(y for _, y in spts)
        spts = [[x, y * k if y < 0 else y] for x, y in spts]
        sn = {n: [x, y * k if y < 0 else y] for n, (x, y) in sn.items()}
    corner = lambda pts, nm, names: [(idx_of(pts, nm[n]), n) for n in names]  # noqa: E731
    front = edges_from(fpts, corner(fpts, fn, ["cfNeck", "cfHem", "hem", "armhole", "shoulder", "hps"]))
    half_back = edges_from(bpts, corner(bpts, bn, ["cbNeck", "cbHem", "hem", "armhole", "shoulder", "hps"]))
    sleeve = edges_from(spts, corner(spts, sn, ["bicepsLeft", "wristLeft", "wristRight", "bicepsRight", "sleeveTop"]))
    pieces = {}
    # the fronts, seen from the front as Marvelous places them: the drafted front (its side seam on +x) is the
    # wearer's LEFT front, the mirrored one his right; the back, seen from behind, has his right on +x (as drafted)
    tag = lambda edges, s: [(seg, a + s, b + s) for seg, a, b in edges]  # noqa: E731
    pieces["frontL"] = ccw(tag(front, "L"))
    pieces["frontR"] = ccw(tag(mirror_edges(front), "R"))
    # the whole back: the half back's right side, then its mirror, joined along the centre back (cbNeck to cbHem
    # vanishes); the hem and the neck become single edges across it
    hb = {(a, b): seg for seg, a, b in half_back}
    hem_r = hb[("cbHem", "hem")]
    neck_r = list(reversed(hb[("hps", "cbNeck")]))                     # cbNeck -> hps on the right
    back = [([[-x, y] for x, y in reversed(hem_r)][:-1] + hem_r, "hemL", "hemR"),
            (hb[("hem", "armhole")], "hemR", "armholeR"),
            (hb[("armhole", "shoulder")], "armholeR", "shoulderR"),
            (hb[("shoulder", "hps")], "shoulderR", "hpsR"),
            (list(reversed(neck_r)) + [[-x, y] for x, y in neck_r][1:], "hpsR", "hpsL"),
            ([[-x, y] for x, y in reversed(hb[("shoulder", "hps")])], "hpsL", "shoulderL"),
            ([[-x, y] for x, y in reversed(hb[("armhole", "shoulder")])], "shoulderL", "armholeL"),
            ([[-x, y] for x, y in reversed(hb[("hem", "armhole")])], "armholeL", "hemL")]
    pieces["back"] = ccw(back)
    # the sleeves: the front pitch is on the drafted sleeve's +x side; the right sleeve as drafted, the left mirrored.
    # Its cap meets the front armhole from the underarm (bicepsRight) to the top, the back from the top to bicepsLeft.
    pieces["sleeveR"] = ccw(tag(sleeve, "R"))
    pieces["sleeveL"] = ccw(tag(mirror_edges(sleeve), "L"))
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    # the rib: each band and cuff a rectangle cut shorter than the edge it is sewn to
    for s in ("R", "L"):
        w = length(E("front" + s, "cfHem" + s, "hem" + s)) * RIB_BAND
        band = rect(w, BAND_H, ["bandCfLow" + s, "bandSideLow" + s, "bandSide" + s, "bandCf" + s])
        # each band's centre-front end on the same side as its front's (the right front's is on +x)
        pieces["bandFront" + s] = ccw(mirror_edges(band)) if s == "R" else band
        w = length(E("sleeve" + s, "wristLeft" + s, "wristRight" + s)) * RIB_CUFF
        pieces["cuff" + s] = rect(w, CUFF_H, ["cuffAlow" + s, "cuffBlow" + s, "cuffB" + s, "cuffA" + s])
    w = length(E("back", "hemL", "hemR")) * RIB_BAND
    pieces["bandBack"] = rect(w, BAND_H, ["bandBackLowL", "bandBackLowR", "bandBackR", "bandBackL"])
    # the stand collar along the whole neckline, its neck edge in three lines (right front, back, left front) so each
    # meets one neck edge; worn standing, its neck edge at the bottom
    nR = length(E("frontR", "hpsR", "cfNeckR"))
    nB = length(E("back", "hpsR", "hpsL"))
    nL = length(E("frontL", "hpsL", "cfNeckL"))
    W = nR + nB + nL
    # placed at the back of the neck and seen from behind, his left is on the collar's -x end
    pieces["collar"] = [([[0, 0], [nL, 0]], "colCfL", "colHpsL"), ([[nL, 0], [nL + nB, 0]], "colHpsL", "colHpsR"),
                        ([[nL + nB, 0], [W, 0]], "colHpsR", "colCfR"), ([[W, 0], [W, COLLAR_H]], "colCfR", "colTopCfR"),
                        ([[W, COLLAR_H], [0, COLLAR_H]], "colTopCfR", "colTopCfL"), ([[0, COLLAR_H], [0, 0]], "colTopCfL", "colCfL")]
    return pieces


# THE SEAMS: (piece, end, end) against (piece, end, end), the ends that meet listed in the same order
def seams():
    out = []
    for s in ("R", "L"):
        out += [(("front" + s, "hps" + s, "shoulder" + s), ("back", "hps" + s, "shoulder" + s)),
                (("front" + s, "armhole" + s, "hem" + s), ("back", "armhole" + s, "hem" + s)),
                (("sleeve" + s, "bicepsRight" + s, "sleeveTop" + s), ("front" + s, "armhole" + s, "shoulder" + s)),
                (("sleeve" + s, "sleeveTop" + s, "bicepsLeft" + s), ("back", "shoulder" + s, "armhole" + s)),
                (("sleeve" + s, "bicepsLeft" + s, "wristLeft" + s), ("sleeve" + s, "bicepsRight" + s, "wristRight" + s)),
                (("bandFront" + s, "bandCf" + s, "bandSide" + s), ("front" + s, "cfHem" + s, "hem" + s)),
                (("bandFront" + s, "bandSide" + s, "bandSideLow" + s), ("bandBack", "bandBack" + s, "bandBackLow" + s)),
                (("cuff" + s, "cuffA" + s, "cuffB" + s), ("sleeve" + s, "wristLeft" + s, "wristRight" + s)),
                (("cuff" + s, "cuffA" + s, "cuffAlow" + s), ("cuff" + s, "cuffB" + s, "cuffBlow" + s))]
    out += [(("bandBack", "bandBackL", "bandBackR"), ("back", "hemL", "hemR")),
            (("collar", "colCfR", "colHpsR"), ("frontR", "cfNeckR", "hpsR")),
            (("collar", "colHpsR", "colHpsL"), ("back", "hpsR", "hpsL")),
            (("collar", "colHpsL", "colCfL"), ("frontL", "hpsL", "cfNeckL")),
            # the zip, closed: the fronts', the bands' and the collar's front edges
            (("frontR", "cfNeckR", "cfHemR"), ("frontL", "cfNeckL", "cfHemL")),
            (("bandFrontR", "bandCfR", "bandCfLowR"), ("bandFrontL", "bandCfL", "bandCfLowL")),
            (("collar", "colCfR", "colTopCfR"), ("collar", "colCfL", "colTopCfL"))]
    return out


# a piece is centred on its point: the first try, on the chest's and the upper arm's points, put the body pieces'
# tops above the head and the sleeves' caps above the shoulders, and the sleeves bunched at the elbow (26 October)
ARRANGE = {"frontR": "Body_Front_3_R", "frontL": "Body_Front_3_L", "back": "Body_Back_Center_3",
           "sleeveR": "Arm_Outside_2_R", "sleeveL": "Arm_Outside_2_L", "cuffR": "Wrist_Outside_R", "cuffL": "Wrist_Outside_L",
           "bandFrontR": "Body_Front_5_R", "bandFrontL": "Body_Front_5_L", "bandBack": "Body_Back_Center_5", "collar": "Neck_Back"}


def plan(brian, sleeve_shorten=0.0):
    pieces = build(brian, sleeve_shorten)
    out_pieces, lines = [], {}
    for key, edges in pieces.items():
        pts = []
        for k, (seg, a, b) in enumerate(edges):
            lines[(key, a, b)] = (k, True)
            lines[(key, b, a)] = (k, False)
            pts.append([round(seg[0][0], 2), round(seg[0][1], 2), CORNER])
            pts += [[round(x, 2), round(y, 2), CURVE] for x, y in seg[1:-1]]
        out_pieces.append({"key": key, "points": pts, "arrange": ARRANGE.get(key),
                           "fabric": "rib" if key.startswith(("band", "cuff")) else "shell"})
    out_seams = []
    for (pa, a0, a1), (pb, b0, b1) in seams():
        la, fa = lines[(pa, a0, a1)]
        lb, fb = lines[(pb, b0, b1)]
        out_seams.append({"a": [pa, la, fa], "b": [pb, lb, fb], "names": [a0, a1, b0, b1]})
    return {"pieces": out_pieces, "seams": out_seams}


JOB = '''# Generated by tools/md-bridge/zip_jacket.py from %(src)s: Tom's zip jacket made, placed on his own avatar's
# arrangement points, sewn, draped %(steps)d steps at %(particle)g mm and exported to %(out)s.
import json, os
PLAN = json.loads(%(plan)r)
AVT = r"F:\\LedgerTools\\garments\\tom\\MH_TomL1.avt"
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
result["made"] = made
sewn = []
for s in PLAN["seams"]:
    pa, la, fa = s["a"]
    pb, lb, fb = s["b"]
    sewn.append(bool(pattern_api.AddSeamlinePairGroup(made[pa], la, made[pb], lb, fa, fb)))
result["sewn"] = sewn
# THE CLOTH (only its physics: nothing of a library fabric's look goes into the game): cotton twill for the
# shell, rib knit for the bands and cuffs, from Marvelous's stock library as October's drapes used
FAB = r"C:\\Users\\Public\\Documents\\MarvelousDesigner\\New Assets\\Fabric"
fabrics = {}
for name, f in (("shell", "V2_Woven_Twill_1.zfab"), ("rib", "V2_Cut_Sew_Knit_Rib_1.zfab")):
    path = os.path.join(FAB, f)
    if os.path.isfile(path):
        fabrics[name] = fabric_api.AddFabric(path)
for p in PLAN["pieces"]:
    if p.get("fabric") in fabrics:
        fabric_api.AssignFabricToPattern(fabrics[p["fabric"]], made[p["key"]], 1)
result["fabrics"] = fabrics
pattern_api.SetParticleDistanceOfPatterns(%(particle)g)
result["simulated"] = bool(utility_api.Simulate(%(steps)d))
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = True
eo.bSingleObject = False
eo.scale = 1.0
result["exported"] = export_api.ExportOBJ(os.path.join(OUT, "zip_jacket.obj"), eo)
result["zprj"] = export_api.ExportZPrj(os.path.join(OUT, "zip_jacket.zprj"))
log("zip jacket made, sewn and draped")
'''


def main(argv):
    src, job = argv[0], argv[1]
    opt = lambda n, d: float(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
    out = argv[argv.index("--out") + 1] if "--out" in argv else r"F:\LedgerTools\garments\tom\zip_jacket"
    p = plan(load(src), opt("--sleeve-shorten", 0.0))
    open(job, "w", encoding="utf-8").write(JOB % {"src": src, "plan": json.dumps(p), "out": out,
                                                  "steps": int(opt("--steps", 400)), "particle": opt("--particle", 20.0)})
    json.dump(p, open(job[:-3] + ".plan.json", "w", encoding="utf-8"), indent=1)
    print("zip jacket: %d pieces, %d seams -> %s" % (len(p["pieces"]), len(p["seams"]), job))
    for q in p["pieces"]:
        print("  %-11s %3d points  on %s" % (q["key"], len(q["points"]), q["arrange"]))


if __name__ == "__main__":
    main(sys.argv[1:])
