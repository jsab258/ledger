#!/usr/bin/env python3
"""Tom's zip jacket as one Marvelous Designer job: FreeSewing's Brian block at his size cut into a zip-front jacket's
pieces, placed on his avatar's arrangement points, sewn, draped and exported.

    python tools/md-bridge/zip_jacket.py BRIAN.json JOB.py [--steps 400] [--particle 20] [--out DIR] [--sleeve-shorten MM]
        [--cuff-of-wrist 1.0] [--cuff-particle 6] [--grip 85] [--cuff-seam-late STEPS]
        [--flip-cuff-seam R|L|RL] [--no-cuffs]
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

THE ZIP'S TAPES AND THE POCKETS' PLACES (26 October night; production/research/game-clothing-pipeline/
ZIP-POCKETS-2026-10-26.md, the route, step 1): no Marvelous zipper (no API call makes one, and its trims would
escape the game mesh's retopology). Instead two zip tapes, TAPE_W wide, each running the whole closure (the hem
band's front end, the front's centre edge, the collar's front end), sewn to those three edges on one side and to
each other on the other: the zip drawn closed, with the tapes' own width and a firmer cloth's stiffness. The teeth,
the welts' lips and the stops are built later in Blender on the drape and baked (step 3). The two hip welts' places
are written into the plan in each front's own pattern coordinates (WELT_*), which the drape's UV islands carry.

EVERY EDGE IS NAMED BY ITS TWO ENDS (Brian's own points), and a seam pairs two edges by those names, so its
directions follow from which ends meet, not from how each outline happens to wind. Every outline is wound
counter-clockwise with y up, starting on a corner, as Marvelous wants (tools/md/make_jacket_job.py's lessons).
"""
import json
import math
import sys

CORNER, CURVE = 0, 2
# the band 0.85 (27 October, the baked jacket's fresh review: at 0.90 the hem band stood off the hips instead of gripping)
RIB_BAND, RIB_CUFF = 0.85, 0.85
BAND_H, CUFF_H, COLLAR_H = 55.0, 60.0, 70.0
# THE CUFF CUT TO THE WRIST, NOT THE SLEEVE (27 October, drape 6's fresh review: cut at 0.85 of the sleeve's 231 mm
# wrist edge, about 196 mm round, each cuff was as wide as his 197 mm wrist and hung off it as a bell or a flap): cut at
# 0.85 of his wrist's girth (F:/LedgerTools/bodies/MH_TomL1/measurements.json, "wrist"), it grips the wrist and the
# sleeve's end gathers into it, as a blouson's rib cuff does
# THE CUFFS' THIRD TRY (27 October, his yes; production/research/game-clothing-pipeline/RIB-CUFFS-2026-10-27.md): cut
# at 1.0 of the wrist to settle loose first, then drawn in to grip by the piece's weft shrinkage (--grip), not by a
# cut narrower than the hand it must pass
WRIST_MM, CUFF_OF_WRIST = 197.1, 1.0
TAPE_W = 12.0
# a hip welt: its slit's length and its lips' height, its centre this far up from the front's hem and this share of
# the way from the centre front to the side seam, leaning this many degrees from upright with its top towards the
# side seam (a hand-warmer welt; slanted, not upright: DECISIONS, 26 October night)
# (0.40 across, 27 October: at 0.55 the welts sat where the front turns back round the body and their lips bent across
# that crease in the drape, the bake plan's "welt across a fold")
WELT_L, WELT_H, WELT_UP, WELT_ACROSS, WELT_LEAN = 150.0, 15.0, 120.0, 0.40, 20.0


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


def build(brian, sleeve_shorten=0.0, cuff_of_wrist=CUFF_OF_WRIST):
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
        w = WRIST_MM * cuff_of_wrist
        cuff = rect(w, CUFF_H, ["cuffAlow" + s, "cuffBlow" + s, "cuffB" + s, "cuffA" + s])
        # the right cuff mirrored, as the right band is (27 October: cut as drafted beside the drafted right sleeve, it
        # had to turn inside out through itself to be sewn; it draped as a crumpled flap and baked 83% wrong)
        pieces["cuff" + s] = ccw(mirror_edges(cuff)) if s == "R" else cuff
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
    # THE ZIP'S TAPES: each the closure's whole length, its outer side in three lines that meet the band's front end,
    # the front's centre edge and the collar's front end, its inner side one line meeting the other tape's
    for s in ("R", "L"):
        lb = length(E("bandFront" + s, "bandCfLow" + s, "bandCf" + s))
        lf = length(E("front" + s, "cfHem" + s, "cfNeck" + s))
        lc = COLLAR_H
        t = "tape" + s
        tape = [([[0, 0], [TAPE_W, 0]], t + "LowO", t + "LowI"),
                ([[TAPE_W, 0], [TAPE_W, lb + lf + lc]], t + "LowI", t + "TopI"),
                ([[TAPE_W, lb + lf + lc], [0, lb + lf + lc]], t + "TopI", t + "TopO"),
                ([[0, lb + lf + lc], [0, lb + lf]], t + "TopO", t + "NeckO"),
                ([[0, lb + lf], [0, lb]], t + "NeckO", t + "BandO"),
                ([[0, lb], [0, 0]], t + "BandO", t + "LowO")]
        pieces[t] = ccw(tape if s == "L" else mirror_edges(tape))
    return pieces


def welts(brian):
    """The two hip welts' places in each front's pattern coordinates (the left front as drafted, the right mirrored)."""
    fpts, fn = brian["brian.front"]
    cf, side = fn["cfHem"], fn["hem"]
    cx = cf[0] + (side[0] - cf[0]) * WELT_ACROSS
    cy = cf[1] + (side[1] - cf[1]) * WELT_ACROSS + WELT_UP
    lean = WELT_LEAN if side[0] > cf[0] else -WELT_LEAN
    out = []
    for s, sx in (("L", 1), ("R", -1)):
        out.append({"piece": "front" + s, "centre": [round(cx * sx, 1), round(cy, 1)], "length": WELT_L, "lips": WELT_H,
                    "leanDegreesFromUpright": round(lean * sx, 1), "leansTowards": "side seam"})
    return out


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
            # the zip, closed: each tape's outer side to the band's, the front's and the collar's front ends, and the
            # two tapes' inner sides to each other
            (("tapeR", "tapeRLowI", "tapeRTopI"), ("tapeL", "tapeLLowI", "tapeLTopI"))]
    for s in ("R", "L"):
        t = "tape" + s
        out += [((t, t + "LowO", t + "BandO"), ("bandFront" + s, "bandCfLow" + s, "bandCf" + s)),
                ((t, t + "BandO", t + "NeckO"), ("front" + s, "cfHem" + s, "cfNeck" + s)),
                ((t, t + "NeckO", t + "TopO"), ("collar", "colCf" + s, "colTopCf" + s))]
    return out


# a piece is centred on its point: the first try, on the chest's and the upper arm's points, put the body pieces'
# tops above the head and the sleeves' caps above the shoulders, and the sleeves bunched at the elbow (26 October)
# THE CUFFS ON THE ARM'S OWN LOWEST POINT (the third try, step 1, 27 October: tools/md-bridge/jobs/cuff_arrange.py and
# cuff_measure.py): on Wrist_Outside a cuff's centre lands 177 mm past the wrist, over the hand, and the two drapes'
# cuffs ended 66 to 70 mm onto it; on Arm_Outside_3 it lands at the wrist (1 mm), beside the arm until sewn
ARRANGE = {"frontR": "Body_Front_3_R", "frontL": "Body_Front_3_L", "back": "Body_Back_Center_3",
           "sleeveR": "Arm_Outside_2_R", "sleeveL": "Arm_Outside_2_L", "cuffR": "Arm_Outside_3_R", "cuffL": "Arm_Outside_3_L",
           "bandFrontR": "Body_Front_5_R", "bandFrontL": "Body_Front_5_L", "bandBack": "Body_Back_Center_5", "collar": "Neck_Back",
           "tapeR": "Body_Front_Center_3", "tapeL": "Body_Front_Center_3"}


def plan(brian, sleeve_shorten=0.0, cuff_of_wrist=CUFF_OF_WRIST, cuffs=True):
    pieces = build(brian, sleeve_shorten, cuff_of_wrist)
    # --no-cuffs (the third try's fresh review, 27 October): the sleeves alone, to see whether a sleeve's own end goes
    # round the arm before any cuff is sewn to it
    if not cuffs:
        pieces = {k: v for k, v in pieces.items() if not k.startswith("cuff")}
    out_pieces, lines = [], {}
    for key, edges in pieces.items():
        pts = []
        for k, (seg, a, b) in enumerate(edges):
            lines[(key, a, b)] = (k, True)
            lines[(key, b, a)] = (k, False)
            pts.append([round(seg[0][0], 2), round(seg[0][1], 2), CORNER])
            pts += [[round(x, 2), round(y, 2), CURVE] for x, y in seg[1:-1]]
        out_pieces.append({"key": key, "points": pts, "arrange": ARRANGE.get(key),
                           "fabric": "rib" if key.startswith(("band", "cuff")) else "tape" if key.startswith("tape") else "shell"})
    out_seams = []
    for (pa, a0, a1), (pb, b0, b1) in seams():
        if pa not in pieces or pb not in pieces:
            continue
        la, fa = lines[(pa, a0, a1)]
        lb, fb = lines[(pb, b0, b1)]
        # the cuff's own side seam (it closes the cuff into a tube) is sewn LATE when asked (--cuff-seam-late)
        late = pa == pb and pa.startswith("cuff")
        out_seams.append({"a": [pa, la, fa], "b": [pb, lb, fb], "names": [a0, a1, b0, b1], "late": late})
    # EACH PIECE'S NAMED CORNERS (pattern millimetres) and ITS FOUR PATCH CORNERS for the game mesh's grid (the bake
    # chain, tools/meshgen/blender/retopo_pieces.py; production/art/clothing/tom-outfit/BAKE-PLAN-2026-10-27.md,
    # step 2): the bottom side runs from the first to the second; the grid's rows run bottom to top
    corners = {key: [[a, round(seg[0][0], 2), round(seg[0][1], 2)] for seg, a, _b in edges] for key, edges in pieces.items()}
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
    return {"pieces": out_pieces, "seams": out_seams, "welts": welts(brian), "corners": corners, "patch": patch}


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
        # THE CUFFS WRAPPED ROUND THE WRIST (27 October, drape 7: placed flat beside the wrist, each cuff closed into a
        # tube outside the arm and hung below the hand): curved round the wrist's arrangement volume before sewing
        if p["key"].startswith("cuff"):
            pattern_api.SetArrangementShapeStyle(idx, "Curved")
result["made"] = made
sewn = []
# THE CUFF'S SIDE SEAM SEWN LATE (the cuffs' third try, 27 October: sewn at once, each cuff closed into a flat tube beside
# the arm where it was placed, and the arm never passed through it): first each cuff hangs open from the sleeve's end
# and is carried round the arm as the sleeve's own seam closes; its side seam is sewn after LATE_STEPS
LATE_STEPS = %(late)d
# --flip-cuff-seam R|L|RL: that side's cuff sewn to its sleeve's end the other way round (a seam sewn against the
# wrap twists the piece through itself, the manual's twisted seam; the right cuff met it once on 27 October)
FLIP = %(flip)r
for s in PLAN["seams"]:
    if LATE_STEPS and s.get("late"):
        continue
    pa, la, fa = s["a"]
    pb, lb, fb = s["b"]
    if pa.startswith("cuff") and pb.startswith("sleeve") and pa[-1] in FLIP:
        fb = not fb
    sewn.append(bool(pattern_api.AddSeamlinePairGroup(made[pa], la, made[pb], lb, fa, fb)))
result["sewn"] = sewn
# THE CLOTH (only its physics: nothing of a library fabric's look goes into the game): cotton twill for the
# shell, rib knit for the bands and cuffs, from Marvelous's stock library as October's drapes used
FAB = r"C:\\Users\\Public\\Documents\\MarvelousDesigner\\New Assets\\Fabric"
fabrics = {}
for name, f in (("shell", "V2_Woven_Twill_1.zfab"), ("rib", "V2_Cut_Sew_Knit_Rib_1.zfab"), ("tape", "V2_Woven_Canvas_1.zfab")):
    path = os.path.join(FAB, f)
    if os.path.isfile(path):
        fabrics[name] = fabric_api.AddFabric(path)
for p in PLAN["pieces"]:
    if p.get("fabric") in fabrics:
        fabric_api.AssignFabricToPattern(fabrics[p["fabric"]], made[p["key"]], 1)
result["fabrics"] = fabrics
pattern_api.SetParticleDistanceOfPatterns(%(particle)g)
# THE TAPES FINER (the research's fresh review, 26 October night: a 12 mm tape at the jacket's 10 to 20 mm is one
# row of cloth): each tape at a third of its width
for p in PLAN["pieces"]:
    if p["key"].startswith("tape"):
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], 4.0)
    # THE CUFFS FINER (the cuffs' third try, step 2: at 10 mm a cuff is about 8 particles round and 3 deep, too coarse to
    # fold round a wrist; a little below the avatar's quad size, only where needed)
    if p["key"].startswith("cuff") and %(cuff_particle)g > 0:
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], %(cuff_particle)g)
if LATE_STEPS:
    result["openSimulated"] = bool(utility_api.Simulate(LATE_STEPS))
    late = []
    for s in PLAN["seams"]:
        if s.get("late"):
            pa, la, fa = s["a"]
            pb, lb, fb = s["b"]
            late.append(bool(pattern_api.AddSeamlinePairGroup(made[pa], la, made[pb], lb, fa, fb)))
    result["lateSewn"] = late
result["simulated"] = bool(utility_api.Simulate(%(steps)d))
eo = ApiTypes.ImportExportOption()
eo.bExportGarment = True
eo.bExportAvatar = True
eo.bSingleObject = False
eo.scale = 1.0
result["exported"] = export_api.ExportOBJ(os.path.join(OUT, "zip_jacket.obj"), eo)
result["zprj"] = export_api.ExportZPrj(os.path.join(OUT, "zip_jacket.zprj"))
# THE GRIP (the cuffs' third try, step 3): everything but the sleeves and cuffs frozen, still colliding, while each
# cuff's weft shrinks to GRIP per cent and draws the sleeve's end in; then all free to settle together
GRIP = %(grip)g
if GRIP > 0:
    for p in PLAN["pieces"]:
        if not p["key"].startswith(("sleeve", "cuff")):
            pattern_api.SetPatternFreeze(made[p["key"]], True)
    for s in ("cuffR", "cuffL"):
        pattern_api.SetWidthShrinkagePercentage(made[s], float(GRIP))
    result["gripShrinkage"] = {s: dict(pattern_api.GetShrinkagePercentage(made[s])) for s in ("cuffR", "cuffL")}
    result["gripSimulated"] = bool(utility_api.Simulate(200))
    for p in PLAN["pieces"]:
        pattern_api.SetPatternFreeze(made[p["key"]], False)
    result["settled"] = bool(utility_api.Simulate(100))
    grip_out = os.path.join(OUT, "grip")
    os.makedirs(grip_out, exist_ok=True)
    result["gripExported"] = export_api.ExportOBJ(os.path.join(grip_out, "zip_jacket.obj"), eo)
    result["gripZprj"] = export_api.ExportZPrj(os.path.join(grip_out, "zip_jacket.zprj"))
log("zip jacket made, sewn and draped")
'''


def main(argv):
    src, job = argv[0], argv[1]
    opt = lambda n, d: float(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
    out = argv[argv.index("--out") + 1] if "--out" in argv else r"F:\LedgerTools\garments\tom\zip_jacket"
    p = plan(load(src), opt("--sleeve-shorten", 0.0), opt("--cuff-of-wrist", CUFF_OF_WRIST), "--no-cuffs" not in argv)
    open(job, "w", encoding="utf-8").write(JOB % {"src": src, "plan": json.dumps(p), "out": out,
                                                  "steps": int(opt("--steps", 400)), "particle": opt("--particle", 20.0),
                                                  "cuff_particle": opt("--cuff-particle", 6.0), "grip": opt("--grip", 0.0),
                                                  "late": int(opt("--cuff-seam-late", 0)),
                                                  "flip": argv[argv.index("--flip-cuff-seam") + 1] if "--flip-cuff-seam" in argv else ""})
    json.dump(p, open(job[:-3] + ".plan.json", "w", encoding="utf-8"), indent=1)
    print("zip jacket: %d pieces, %d seams -> %s" % (len(p["pieces"]), len(p["seams"]), job))
    for q in p["pieces"]:
        print("  %-11s %3d points  on %s" % (q["key"], len(q["points"]), q["arrange"]))


if __name__ == "__main__":
    main(sys.argv[1:])
