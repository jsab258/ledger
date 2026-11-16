#!/usr/bin/env python3
"""Ron's donkey jacket as one job for Kiln (run_job_script.py) or Marvelous (md_job.py): FreeSewing's Brian block at
his size cut into a donkey jacket's pieces, Simon's collar stand and fall on its neckline, placed on the body's
arrangement points by name, sewn, draped and exported.

    python tools/md-bridge/donkey_jacket.py BRIAN.json JOB.py [--simon SIMON.json] [--out DIR] [--avatar BODY]
        [--steps 400] [--lap 40] [--sleeve-shorten MM]
    python F:/LedgerTools/tool-dev/kiln/python/run_job_script.py JOB.py RESULT.json     # Kiln
    python tools/md-bridge/md_job.py JOB.py                                              # Marvelous (an .avt needed)
    python tools/md-bridge/donkey_jacket.py --selftest

WHY, 16 November 2026 (advisor 172; production/art/clothing/RON-KILN-OUTFIT-PLAN-2026-11-16.md, section 2, step 4):
Kiln's M6 outfit is Ron's navy donkey jacket refit to his own body (MH_RoccoP2). The draft is the corrected one of
29 September (production/art/clothing/donkey-jacket-sewn/brian-ron.json: chest 1175, biceps 442, shoulder to shoulder
520, slope 5, the back 20 mm tucked above its armhole); its girths stand against the full-body re-measure of 16 Nov
(F:/LedgerTools/garments/ron/kiln-outfit-2026-11-16/STEP1-DELTA.md). The collar is Simon's (FreeSewing, MIT;
production/art/clothing/donkey-jacket-pattern/simon-ron.json, drafted with the earlier armpit, its neck the same 442).
The zip jacket's helpers (tools/md-bridge/zip_jacket.py: named edges, mirroring, winding, the back and the sleeves)
are imported, not copied, as tools/md-bridge/jeans.py imports them.

THE PIECES, a 1990 melton donkey jacket: a whole back, two fronts, two one-piece sleeves, Simon's collar stand along
the whole neckline and his fall sewn to the stand's top edge, in a stiffer cloth (the stand and fall of a work
jacket are interlined). No rib, cuffs or zip tapes: the sleeves end open, the hem is plain. The shoulder yoke (black
PVC in 1990) and the two patch pockets are not pieces: they are drawn in the normal map and the ID map (decided by
the session, 16 Nov; the zip jacket put its welts in the map the same way), and their places are written into the
plan in each piece's own pattern coordinates ("map"), which the drape's UV islands carry. The buttons are the bake's.

THE LAP (LAP mm; tools/meshgen/blender/finish_donkey.py: "the left front laps over the right by 4 cm (a man's
jacket)"). A drape can only sew outline to outline, and a front's centre line under a lap is no outline. So the
closure is sewn where it shows: the wearer's left front carries the lap (its centre edge moved LAP past the centre
front, the neck and hem drawn straight out to it), the right front is cut LAP short of its centre front, and the two
lap edges are sewn edge to edge. The girth is the draft's, the closing line is where the lap's edge is seen, and the
lap's double layer, its thickness and the buttons come later from the bake (as finish_donkey's FrontLap did). The
neckline is then a closed ring, so the stand is sewn round it and its two ends to each other at the lap's edge: the
jacket worn buttoned to the top.

THE COLLAR fitted to this neckline: Simon's stand cut at its own centre-front points (his button extension dropped),
stretched along its length so its foot matches Brian's neckline from centre front to centre front (the factor is in
the plan, "collar.scale"), then its left end drawn out LAP and its right end cut LAP short, as the fronts are. Its fall
is stretched by the same factor and sewn to the stand's top edge symmetric about the centre back; where its right end
would pass the stand's cut end it stops there (the fall's tip lies under the lap on a real jacket).

EVERY EDGE IS NAMED BY ITS TWO ENDS (Brian's own points, or the lap's and collar's here), and a seam pairs two edges by
those names, so its directions follow from which ends meet (zip_jacket.py). Every outline is wound counter-clockwise
with y up, starting on a corner. Nothing in this file is a measure of one body: every length comes from the drafts.

THE CLOTH (only its physics; nothing of a library fabric's look goes into the game): on Marvelous its own boiled
melton and, for the collar, canvas; on Kiln, which cannot read those files, our own fabric descriptions written beside
the job (<name>.drape-fabric.json, read by Kiln's fabric_for_file; F:/LedgerTools/tool-dev/kiln/python/kiln_front/
compat.py). Their numbers are estimates (MELTON, COLLAR below), to be measured against the drape.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zip_jacket import ARRANGE as ZIP_ARRANGE  # noqa: E402
from zip_jacket import CORNER, CURVE, area, build as zip_build, ccw, edges_from, idx_of, length, load, mirror_edges  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SIMON = os.path.join(REPO, "production", "art", "clothing", "donkey-jacket-pattern", "simon-ron.json")
BRIAN = os.path.join(REPO, "production", "art", "clothing", "donkey-jacket-sewn", "brian-ron.json")
OUT_DIR = r"F:\LedgerTools\garments\ron\kiln-outfit-2026-11-16"
BODY = r"F:\LedgerTools\bodies\MH_RoccoP2\MH_RoccoP2_FullBody.fbx"

LAP = 40.0              # mm, the left front over the right (finish_donkey.py)
FALL_END_MIN = 5.0      # mm: a fall corner nearer a stand end than this is put on the end itself
# the map's places (finish_donkey.py, 29 September, after the V&A's T.561-1993): two flapless patch pockets PW x PH,
# their feet PFOOT above the hem, their inner edges PX from the centre front (the right one clear of the lap); the yoke
# down to FRONT_YOKE under the shoulder seam on the fronts, from YOKE_CF off the centre front, and to BACK_YOKE under
# the collar seam on the back
PW, PH, PFOOT, PX = 190.0, 200.0, 80.0, 70.0
FRONT_YOKE, YOKE_CF, BACK_YOKE = 100.0, 60.0, 290.0
# the piece's points by name (zip_jacket.py's, the collar on the neck's back point)
ARRANGE = {k: ZIP_ARRANGE[k] for k in ("frontR", "frontL", "back", "sleeveR", "sleeveL")}
ARRANGE.update({"stand": ZIP_ARRANGE["collar"], "fall": ZIP_ARRANGE["collar"]})

# THE FABRICS. "md" is Marvelous's stock file (its physics only); "kiln" our own description, in Kiln's units
# (doc.rs, struct Fabric: stretch, shear, bending 0..100, density g/m2, thickness mm). ESTIMATES, none measured:
# melton about 0.7 kg/m2 (the plan; donkey-jacket-sewn/README.md: "melton's 0.7 kg/m2"), 3 mm thick (finish_donkey's
# wool), a dense felted wool so firmer than Kiln's Cotton Twill (80/82/60/35) in stretch, shear and bending; the
# collar the same wool doubled over an interlining, so heavier, thicker and nearer Kiln's Stiff Interlining (96/90/95).
# The file names avoid "wool": if a description failed to load, Kiln picks a preset by name, and "wool" is its
# low-gauge sweater knit.
MELTON = {"name": "ron_melton", "color": [32, 36, 52], "stretch_weft": 90.0, "stretch_warp": 92.0, "shear": 80.0,
          "bending_weft": 65.0, "bending_warp": 65.0, "density": 700.0, "friction": 45.0, "thickness": 3.0,
          "damping": 15.0}
COLLAR = {"name": "ron_melton_collar", "color": [32, 36, 52], "stretch_weft": 95.0, "stretch_warp": 95.0, "shear": 88.0,
          "bending_weft": 85.0, "bending_warp": 85.0, "density": 900.0, "friction": 45.0, "thickness": 4.0,
          "damping": 15.0}
ESTIMATE_NOTE = ("ESTIMATES (16 Nov 2026, tools/md-bridge/%s): not measured; melton about 0.7 kg/m2 per the plan and "
                 "donkey-jacket-sewn/README.md; stiffness set by judgement against Kiln's presets (doc.rs). Check them "
                 "against the drape before trusting them.")
FABRICS = {"melton": {"md": "V2_Woven_Melton_Boiled_1.zfab", "kiln": MELTON},
           "collar": {"md": "V2_Woven_Canvas_1.zfab", "kiln": COLLAR}}


def load_parts(path, parts):
    """Only the named parts of a FreeSewing draft, as zip_jacket.load reads them (y up). zip_jacket.load reads every
    part and stops on Simon's, whose button plackets have no seam path."""
    d = json.load(open(path, encoding="utf-8"))
    out = {}
    for part in parts:
        p = d["parts"][part]
        pts = [[x, -y] for x, y in p["paths"]["seam"]["points"]]
        if pts[0] == pts[-1]:
            pts = pts[:-1]
        out[part] = (pts, {n: [x, -y] for n, (x, y) in p["points"].items()})
    return out


def _lerp(p, q, x):
    t = (x - p[0]) / (q[0] - p[0])
    return [x, p[1] + (q[1] - p[1]) * t]


def clip_x(pts, c, keep_below):
    """A closed outline cut by the upright line x = c, keeping the side x <= c (keep_below) or x >= c."""
    inside = (lambda p: p[0] <= c + 1e-9) if keep_below else (lambda p: p[0] >= c - 1e-9)
    out = []
    for k, p in enumerate(pts):
        q = pts[(k + 1) % len(pts)]
        if inside(p):
            out.append(list(p))
            if not inside(q):
                out.append(_lerp(p, q, c))
        elif inside(q):
            out.append(_lerp(p, q, c))
    return out


def split_at(seg, d):
    """A polyline split at distance d along it: (before, after), the split point ending one and starting the other."""
    run = 0.0
    for k in range(len(seg) - 1):
        s = math.dist(seg[k], seg[k + 1])
        if run + s >= d:
            t = (d - run) / s if s else 0.0
            p = [seg[k][0] + (seg[k + 1][0] - seg[k][0]) * t, seg[k][1] + (seg[k + 1][1] - seg[k][1]) * t]
            return seg[:k + 1] + [p], [p] + seg[k + 1:]
        run += s
    return list(seg), [seg[-1]]


def fronts(brian, lap=LAP):
    """The wearer's left front (as drafted, its side on +x) with the lap drawn out past the centre front, and his
    right front (the drafted one cut lap short of its centre front, then mirrored)."""
    fpts, fn = brian["brian.front"]
    corner = [(idx_of(fpts, fn[n]), n) for n in ["cfNeck", "cfHem", "hem", "armhole", "shoulder", "hps"]]
    e = {(a, b): seg for seg, a, b in edges_from(fpts, corner)}
    cf_n, cf_h = fn["cfNeck"], fn["cfHem"]
    # the lap: the centre edge moved lap towards -x (past the centre front, over the right front)
    left = [([[cf_n[0] - lap, cf_n[1]], [cf_h[0] - lap, cf_h[1]]], "lapNeck", "lapHem"),
            ([[cf_h[0] - lap, cf_h[1]]] + e[("cfHem", "hem")], "lapHem", "hem"),
            (e[("hem", "armhole")], "hem", "armhole"), (e[("armhole", "shoulder")], "armhole", "shoulder"),
            (e[("shoulder", "hps")], "shoulder", "hps"),
            (e[("hps", "cfNeck")] + [[cf_n[0] - lap, cf_n[1]]], "hps", "lapNeck")]
    # the right front cut at x = centre front + lap: the neck and the hem must cross that line once
    cut = cf_n[0] + lap
    neck, hem = e[("hps", "cfNeck")], e[("cfHem", "hem")]
    if any(neck[k][0] < neck[k + 1][0] for k in range(len(neck) - 1)) or any(hem[k][0] > hem[k + 1][0] for k in range(len(hem) - 1)):
        raise ValueError("the front's neck or hem doubles back across the lap's line")
    k = next(i for i in range(len(neck) - 1) if neck[i + 1][0] <= cut)
    neck_r = neck[:k + 1] + [_lerp(neck[k], neck[k + 1], cut)]
    j = next(i for i in range(len(hem) - 1) if hem[i + 1][0] > cut)
    hem_r = [_lerp(hem[j], hem[j + 1], cut)] + hem[j + 1:]
    right = [([neck_r[-1], hem_r[0]], "lapNeck", "lapHem"), (hem_r, "lapHem", "hem"),
             (e[("hem", "armhole")], "hem", "armhole"), (e[("armhole", "shoulder")], "armhole", "shoulder"),
             (e[("shoulder", "hps")], "shoulder", "hps"), (neck_r, "hps", "lapNeck")]
    tag = lambda edges, s: [(seg, a + s, b + s) for seg, a, b in edges]  # noqa: E731
    return ccw(tag(left, "L")), ccw(tag(mirror_edges(right), "R"))


def _closed(pts):
    """A closed outline counter-clockwise."""
    a = sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1] for k in range(len(pts)))
    return pts if a > 0 else list(reversed(pts))


def _ends(pts):
    """The four end corners of a collar piece lying along x: (bottom left, bottom right, top right, top left)."""
    xs = [p[0] for p in pts]
    lo, hi = min(xs), max(xs)
    left = [k for k, p in enumerate(pts) if p[0] <= lo + 0.5]
    right = [k for k, p in enumerate(pts) if p[0] >= hi - 0.5]
    return (min(left, key=lambda k: pts[k][1]), min(right, key=lambda k: pts[k][1]),
            max(right, key=lambda k: pts[k][1]), max(left, key=lambda k: pts[k][1]))


def _walk(pts, i, j):
    return pts[i:j + 1] if j >= i else pts[i:] + pts[:j + 1]


def collar(simon, n_left, n_back, n_right, n_cf_to_cf, lap=LAP):
    """Simon's stand and fall fitted to a neckline whose three edges (left front, back, right front) are n_left,
    n_back and n_right long, n_cf_to_cf the neckline as drafted from centre front to centre front. Placed at the back
    of the neck and seen from behind, the wearer's left is on -x. Returns (stand edges, fall edges, scale)."""
    spts, sn = simon["simon.collarStand"]
    cpts, cn = simon["simon.collar"]
    # the stand cut at its own centre-front points (Simon's button extension beyond them dropped)
    st = clip_x(clip_x(_closed(spts), sn["rightBottomCf"][0], True), sn["leftBottomCf"][0], False)
    bl, br, _tr, _tl = _ends(st)
    k = n_cf_to_cf / length(_walk(st, bl, br))
    st = [[x * k, y] for x, y in st]
    # its left end drawn out lap (its two end corners moved), its right end cut lap short
    bl, br, tr, tl = _ends(st)
    for i in (bl, tl):
        st[i] = [st[i][0] - lap, st[i][1]]
    st = _closed(clip_x(st, st[br][0] - lap, True))
    bl, br, tr, tl = _ends(st)
    foot, top = _walk(st, bl, br), _walk(st, tr, tl)
    f1, rest = split_at(foot, n_left)
    f2, f3 = split_at(rest, n_back)
    # the fall stretched as the stand, its neck edge on the stand's top symmetric about the centre back (x = 0)
    fall_pts = _closed([[x * k, y] for x, y in cpts])
    fi = {n: idx_of(fall_pts, [cn[n][0] * k, cn[n][1]]) for n in ("leftBottomEdge", "rightBottomEdge", "rightTopEdge", "leftTopEdge")}
    neck = _walk(fall_pts, fi["rightTopEdge"], fi["leftTopEdge"])
    # the top runs from the right end to the left; where it crosses the centre back
    run, mid = 0.0, None
    for i in range(len(top) - 1):
        if (top[i][0] >= 0.0) != (top[i + 1][0] >= 0.0):
            t = top[i][0] / (top[i][0] - top[i + 1][0])
            mid = run + math.dist(top[i], top[i + 1]) * t
            break
        run += math.dist(top[i], top[i + 1])
    half = length(neck) / 2.0
    a, b = mid - half, mid + half
    segs = []
    rest = top
    if a > FALL_END_MIN:
        s0, rest = split_at(rest, a)
        segs.append((s0, "stTopR", "stFallR"))
        cur, done = "stFallR", a
    else:
        cur, done = "stTopR", 0.0
    s1, s2 = split_at(rest, b - done)
    segs.append((s1, cur, "stFallL"))
    segs.append((s2, "stFallL", "stTopL"))
    stand = [(f1, "stCfL", "stHpsL"), (f2, "stHpsL", "stHpsR"), (f3, "stHpsR", "stCfR"),
             (_walk(st, br, tr), "stCfR", "stTopR")] + segs + [(_walk(st, tl, bl), "stTopL", "stCfL")]
    fall_start = cur
    fall = [(_walk(fall_pts, fi["leftBottomEdge"], fi["rightBottomEdge"]), "fallOutL", "fallOutR"),
            (_walk(fall_pts, fi["rightBottomEdge"], fi["rightTopEdge"]), "fallOutR", "fallNeckR"),
            (neck, "fallNeckR", "fallNeckL"),
            (_walk(fall_pts, fi["leftTopEdge"], fi["leftBottomEdge"]), "fallNeckL", "fallOutL")]
    return ccw(stand), ccw(fall), {"scale": k, "fallRightOnStand": fall_start, "fallHalfMm": half, "midOnTopMm": mid}


def build(brian, simon, lap=LAP, sleeve_shorten=0.0):
    zp = zip_build(brian, sleeve_shorten)
    pieces = {}
    pieces["frontL"], pieces["frontR"] = fronts(brian, lap)
    for key in ("back", "sleeveR", "sleeveL"):
        pieces[key] = zp[key]
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    nL = length(E("frontL", "hpsL", "lapNeckL"))
    nB = length(E("back", "hpsR", "hpsL"))
    nR = length(E("frontR", "hpsR", "lapNeckR"))
    nf = _front_neck(brian)
    pieces["stand"], pieces["fall"], info = collar(simon, nL, nB, nR, 2 * nf + nB, lap)
    order = ["frontR", "frontL", "back", "sleeveR", "sleeveL", "stand", "fall"]
    return {k: pieces[k] for k in order}, info


def _front_neck(brian):
    """The front neck as drafted, from the high shoulder point to the centre front."""
    fpts, fn = brian["brian.front"]
    corner = [(idx_of(fpts, fn[n]), n) for n in ["cfNeck", "cfHem", "hem", "armhole", "shoulder", "hps"]]
    return length(next(seg for seg, a, b in edges_from(fpts, corner) if (a, b) == ("hps", "cfNeck")))


# THE SEAMS: (piece, end, end) against (piece, end, end), the ends that meet listed in the same order
def seams(fall_right="stFallR"):
    out = []
    for s in ("R", "L"):
        out += [(("front" + s, "hps" + s, "shoulder" + s), ("back", "hps" + s, "shoulder" + s)),
                (("front" + s, "armhole" + s, "hem" + s), ("back", "armhole" + s, "hem" + s)),
                (("sleeve" + s, "bicepsRight" + s, "sleeveTop" + s), ("front" + s, "armhole" + s, "shoulder" + s)),
                (("sleeve" + s, "sleeveTop" + s, "bicepsLeft" + s), ("back", "shoulder" + s, "armhole" + s)),
                (("sleeve" + s, "bicepsLeft" + s, "wristLeft" + s), ("sleeve" + s, "bicepsRight" + s, "wristRight" + s))]
    out += [(("frontL", "lapNeckL", "lapHemL"), ("frontR", "lapNeckR", "lapHemR")),        # the closure, at the lap
            (("stand", "stCfL", "stHpsL"), ("frontL", "lapNeckL", "hpsL")),               # the stand round the neck
            (("stand", "stHpsL", "stHpsR"), ("back", "hpsL", "hpsR")),
            (("stand", "stHpsR", "stCfR"), ("frontR", "hpsR", "lapNeckR")),
            (("stand", "stCfL", "stTopL"), ("stand", "stCfR", "stTopR")),                 # its ends shut at the lap
            (("fall", "fallNeckR", "fallNeckL"), ("stand", fall_right, "stFallL"))]       # the fall on the stand
    return out


def map_places(brian, lap=LAP):
    """The pockets' and the yoke's places for the normal and ID maps, in each piece's pattern coordinates (the left
    front as drafted, the right mirrored; the back whole, its centre at x = 0)."""
    fn, bn = brian["brian.front"][1], brian["brian.back"][1]
    hem_y, cf_x = fn["cfHem"][1], fn["cfNeck"][0]
    side = 1.0 if fn["hem"][0] > cf_x else -1.0
    out = {"pockets": [], "yoke": []}
    for s, sx, clear in (("L", 1.0, 0.0), ("R", -1.0, lap)):
        x0 = cf_x + side * (PX + clear)
        x1 = x0 + side * PW
        out["pockets"].append({"piece": "front" + s, "x": sorted([round(x0 * sx, 1), round(x1 * sx, 1)]),
                               "y": [round(hem_y + PFOOT, 1), round(hem_y + PFOOT + PH, 1)], "patch": True})
        low = min(fn["shoulder"][1], fn["hps"][1]) - FRONT_YOKE
        out["yoke"].append({"piece": "front" + s, "above_y": round(low, 1),
                            "from_x": round((cf_x + side * YOKE_CF) * sx, 1), "towards": "armhole"})
    out["yoke"].append({"piece": "back", "above_y": round(bn["cbNeck"][1] - BACK_YOKE, 1), "whole_width": True})
    return out


def plan(brian, simon, lap=LAP, sleeve_shorten=0.0):
    pieces, info = build(brian, simon, lap, sleeve_shorten)
    out_pieces, lines = [], {}
    for key, edges in pieces.items():
        pts = []
        for k, (seg, a, b) in enumerate(edges):
            lines[(key, a, b)] = (k, True)
            lines[(key, b, a)] = (k, False)
            pts.append([round(seg[0][0], 2), round(seg[0][1], 2), CORNER])
            pts += [[round(x, 2), round(y, 2), CURVE] for x, y in seg[1:-1]]
        out_pieces.append({"key": key, "points": pts, "arrange": ARRANGE[key],
                           "fabric": "collar" if key in ("stand", "fall") else "melton"})
    out_seams = []
    for (pa, a0, a1), (pb, b0, b1) in seams(info["fallRightOnStand"]):
        la, fa = lines[(pa, a0, a1)]
        lb, fb = lines[(pb, b0, b1)]
        out_seams.append({"a": [pa, la, fa], "b": [pb, lb, fb], "names": [a0, a1, b0, b1]})
    corners = {key: [[a, round(seg[0][0], 2), round(seg[0][1], 2)] for seg, a, _b in edges] for key, edges in pieces.items()}
    patch = {}
    for s in ("R", "L"):
        patch["front" + s] = {"bottom": ["lapHem" + s, "hem" + s], "top": ["shoulder" + s, "lapNeck" + s]}
        patch["sleeve" + s] = {"bottom": ["wristLeft" + s, "wristRight" + s], "top": ["bicepsRight" + s, "bicepsLeft" + s]}
    patch["back"] = {"bottom": ["hemL", "hemR"], "top": ["shoulderR", "shoulderL"]}
    patch["stand"] = {"bottom": ["stCfL", "stCfR"], "top": ["stTopR", "stTopL"]}
    patch["fall"] = {"bottom": ["fallOutL", "fallOutR"], "top": ["fallNeckR", "fallNeckL"]}
    return {"pieces": out_pieces, "seams": out_seams, "corners": corners, "patch": patch, "map": map_places(brian, lap),
            "collar": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in info.items()},
            "cut": {"lap_mm": lap, "sleeve_shorten_mm": sleeve_shorten}}


JOB = '''# Generated by tools/md-bridge/donkey_jacket.py from %(src)s: Ron's donkey jacket made, placed on the body's
# arrangement points by name, sewn, draped (%(steps)d steps at 20 mm, 200 at 10 mm with the collar at 6, 100 at
# Fitting) and exported to %(out)s. Runs on Kiln (run_job_script.py) or Marvelous (md_job.py).
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
result["made"] = made
result["arranged"] = {p["key"]: p["arrange"] in points for p in PLAN["pieces"]}
result["sewn"] = [bool(pattern_api.AddSeamlinePairGroup(made[s["a"][0]], s["a"][1], made[s["b"][0]], s["b"][1], s["a"][2], s["b"][2]))
                  for s in PLAN["seams"]]
# THE CLOTH: Marvelous's stock files where they are and this is Marvelous; on Kiln (its modules are stand-ins that
# cannot read a locked fabric) our own descriptions, <name>.drape-fabric.json beside the job
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
# the collar finer, 6 mm, as the skill orders for collars and bands
for p in PLAN["pieces"]:
    if p["key"] in ("stand", "fall"):
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], 6.0)
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
result["exported"] = export_api.ExportOBJ(os.path.join(OUT, "donkey_jacket.obj"), eo)
result["zprj"] = export_api.ExportZPrj(os.path.join(OUT, "donkey_jacket.zprj"))
log("donkey jacket made, sewn and draped")
'''


def write_fabrics(folder):
    """Each fabric's Kiln description beside the job; returns {name: {"md", "own"}} for the job."""
    out = {}
    for name, f in FABRICS.items():
        d = dict(f["kiln"])
        d["_estimates"] = ESTIMATE_NOTE % os.path.basename(__file__)
        own = os.path.join(folder, d["name"] + ".zfab")       # never a file: Kiln reads the description beside it
        json.dump(d, open(os.path.join(folder, d["name"] + ".drape-fabric.json"), "w", encoding="utf-8"), indent=1)
        out[name] = {"md": f["md"], "own": own}
    return out


def main(argv):
    src, job = argv[0], argv[1]
    opt = lambda n, d: float(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
    sarg = lambda n, d: argv[argv.index(n) + 1] if n in argv else d  # noqa: E731
    simon_path = sarg("--simon", SIMON)
    out = sarg("--out", os.path.join(OUT_DIR, "donkey_jacket"))
    steps = int(opt("--steps", 400))
    p = plan(load(src), load_parts(simon_path, ["simon.collarStand", "simon.collar"]), opt("--lap", LAP),
             opt("--sleeve-shorten", 0.0))
    folder = os.path.dirname(os.path.abspath(job))
    fab = write_fabrics(folder)
    open(job, "w", encoding="utf-8").write(JOB % {"src": src + " and " + simon_path, "plan": json.dumps(p), "out": out,
                                                  "steps": steps, "fabrics": fab,
                                                  # --avatar: the body draped on (Kiln reads an FBX; Marvelous needs an .avt)
                                                  "avt": sarg("--avatar", BODY)})
    json.dump(p, open(job[:-3] + ".plan.json", "w", encoding="utf-8"), indent=1)
    print("donkey jacket: %d pieces, %d seams -> %s (collar scale %.4f)" % (len(p["pieces"]), len(p["seams"]), job,
                                                                         p["collar"]["scale"]))
    for q in p["pieces"]:
        print("  %-8s %3d points  on %s  (%s)" % (q["key"], len(q["points"]), q["arrange"], q["fabric"]))


def _check(brian, simon, label):
    """The selftest's measures on one draft: (list of passes, lines to print)."""
    ok, msg = [], []
    pieces, info = build(brian, simon)
    p = plan(brian, simon)
    keys = [q["key"] for q in p["pieces"]]
    ok.append(keys == ["frontR", "frontL", "back", "sleeveR", "sleeveL", "stand", "fall"])
    ok.append(not any(k.startswith(("band", "cuff", "tape", "collar")) for k in keys))
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    # every seam found by its named ends on both pieces, and the two edges' lengths: within 3% of each other, except a
    # sleeve's cap against its armhole (a set-in sleeve's cap is cut longer, eased in: up to 12%; Tom's back cap
    # drafts 0.1% short, within the 3% every seam is allowed)
    ratios = []
    for (pa, a0, a1), (pb, b0, b1) in seams(info["fallRightOnStand"]):
        r = length(E(pa, a0, a1)) / length(E(pb, b0, b1))
        cap = pa.startswith("sleeve") and pb != pa
        ratios.append("%s %s-%s %.3f" % (pa, a0, a1, r))
        ok.append(0.97 <= r <= 1.12 if cap else 0.97 <= r <= 1.03)
    ok.append(len(p["seams"]) == len(seams()))
    # every seam's two edges named by ends that meet: each name pair is one edge of its piece
    for s in p["seams"]:
        ok.append(s["a"][1] < len(pieces[s["a"][0]]) and s["b"][1] < len(pieces[s["b"][0]]))
    # the areas against the drafts within 1%
    fpts, fn = brian["brian.front"]
    bpts, bn = brian["brian.back"]
    spts, sn = brian["library.sleeve"]
    poly = lambda pts: abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1] for k in range(len(pts))) / 2)  # noqa: E731
    front, half_back, sleeve = poly(fpts), poly(bpts), poly(spts)
    cf = abs(fn["cfNeck"][1] - fn["cfHem"][1])
    st_pts = simon["simon.collarStand"][0]
    st_draft = poly(clip_x(clip_x(_closed(st_pts), simon["simon.collarStand"][1]["rightBottomCf"][0], True),
                           simon["simon.collarStand"][1]["leftBottomCf"][0], False))
    fall_draft = poly(simon["simon.collar"][0])
    k = info["scale"]
    checks = [("back", area(pieces["back"]), 2 * half_back), ("sleeveR", area(pieces["sleeveR"]), sleeve),
              ("sleeveL", area(pieces["sleeveL"]), sleeve), ("frontL", area(pieces["frontL"]), front + LAP * cf),
              ("fronts", area(pieces["frontL"]) + area(pieces["frontR"]), 2 * front),
              ("stand", area(pieces["stand"]), st_draft * k), ("fall", area(pieces["fall"]), fall_draft * k)]
    for name, got, want in checks:
        ok.append(abs(got / want - 1.0) <= 0.01)
        msg.append("  %s %-7s area %9.0f mm2, draft %9.0f (%+.2f%%)" % (label, name, got, want, 100 * (got / want - 1)))
    msg.append("  %s collar scale %.4f; fall's right end on %s; seams: %s" % (label, k, info["fallRightOnStand"], "; ".join(ratios)))
    return ok, msg


def selftest():
    ok, msg = [], []
    if not os.path.isfile(BRIAN) or not os.path.isfile(SIMON):
        print("donkey jacket selftest: passed=0/0 failed=0 (no drafts on this machine)")
        return 0
    simon = load_parts(SIMON, ["simon.collarStand", "simon.collar"])
    o, m = _check(load(BRIAN), simon, "Ron")
    ok += o
    msg += m
    # NO SPECIAL-CASE NUMBERS FOR ONE BODY: the same checks on another man's Brian (Tom's, 26 October), the collar
    # stretched to his neckline by the same rule
    tom = r"F:\LedgerTools\garments\tom\pattern\brian.json"
    if os.path.isfile(tom):
        o, m = _check(load(tom), simon, "Tom")
        ok += o
        msg += m
    # the lap: the left front's lap edge LAP past its centre front, the right's LAP short of it, on the same side
    pieces, _ = build(load(BRIAN), simon)
    lx = [x for x, y in next(seg for seg, a, b in pieces["frontL"] if {a, b} == {"lapNeckL", "lapHemL"})]
    rx = [x for x, y in next(seg for seg, a, b in pieces["frontR"] if {a, b} == {"lapNeckR", "lapHemR"})]
    ok.append(all(abs(x + LAP) < 0.01 for x in lx) and all(abs(x + LAP) < 0.01 for x in rx))
    # the fabric descriptions load as Kiln's struct Fabric would: only its fields, numbers where numbers are
    fields = {"name", "color", "stretch_weft", "stretch_warp", "shear", "bending_weft", "bending_warp", "density",
              "friction", "thickness", "shrink_weft", "shrink_warp", "damping", "texture", "texture_scale", "texture_angle"}
    for f in FABRICS.values():
        ok.append(set(f["kiln"]) <= fields and "wool" not in f["kiln"]["name"])
    ok.append(abs(MELTON["density"] - 700.0) < 1e-6)
    print("\n".join(msg))
    print("donkey jacket selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(selftest() if "--selftest" in a else main(a))
