"""FreeSewing's Jaeger jacket (tools/meshgen/freesewing_draft.mjs's JSON) as a sewing specification for Marvelous
Designer: the pieces (each outline in millimetres, y up, left and right copies), their seams (which stretch of one
piece's edge is sewn to which stretch of another's, by Jaeger's own named points), the lapel's roll line as a fold,
which pieces are fused, and the pockets' places.

    python tools/md/jaeger_spec.py PATTERN.json SPEC.json [--longer 50] [--front-balance 130] [--stance-drop 70]

WHY, 1 October (Jafar's Marvelous proof, DECISIONS.md and CLOTHES.md item 0): the jacket is made the tailor's way
in Marvelous Designer, from our own pattern, FreeSewing's Jaeger (MIT). A tailored jacket's pieces: two fronts (the
lapel cut in one with each), two side bodies, two backs (a centre-back seam opening into the vent), two two-piece
sleeves, an undercollar and a top collar, two front facings (the lapel's visible face), two hip-pocket flaps and a
chest welt. The seams follow the pattern's names, so they move with any size the pattern is drafted at: the sleeve
head is set round the armhole from the back pitch, the undersleeve under the arm.
The front's lining and the pocket bags are left out: nothing outside shows them.
"""
import json
import math
import sys

argv = sys.argv[1:]
SRC, OUT = argv[0], argv[1]
pat = json.load(open(SRC, encoding="utf-8"))
P = pat["parts"]


# THE SKIRT LENGTHENED, 2 October: Jaeger at its longest (lengthBonus 25%) ends Ron's jacket at the crotch in his
# reference pose; a 1990 suit jacket covered the seat. So the body pieces are stretched below the hip line by
# --longer mm (default 50), the pockets, buttons and vent top (all above the hip line) where Jaeger puts them.
LONGER = float(argv[argv.index("--longer") + 1]) if "--longer" in argv else 50.0
BODY = ("jaeger.front", "jaeger.side", "jaeger.back")


def longer(base, v):
    if base not in BODY or LONGER == 0:
        return v
    hips = P["jaeger.front"]["points"]["hips"][1]
    hem = P["jaeger.front"]["points"]["hem"][1]
    if v[1] <= hips:
        return v
    return [v[0], v[1] + LONGER * (v[1] - hips) / (hem - hips)]


# THE FRONT BALANCE, 2 October: on Ron the front's hem rode 9 to 11 cm above the back's and the top button sat on
# his lower chest (1.38 m; his waist is 1.14 m): Jaeger drafts the front for an average figure, and a big chest and
# belly take up front length (production/art/clothing/md-jacket, the drape measured). The tailor's adjustment:
# length added to the front across the chest, from --front-balance mm at centre front tapering to nothing at the
# side seam (so the side seam keeps its length), spread over a band below the armhole (250 to 350 mm down from the
# neck point, so the armhole keeps its shape). Everything below moves down with it: the break point and so the
# roll line (a lower button stance), the buttons, the pockets, the hem.
BALANCE = float(argv[argv.index("--front-balance") + 1]) if "--front-balance" in argv else 0.0
# --stance-drop mm: the break point (the top button) and the buttons below it moved down centre front, a lower
# button stance and a longer lapel (a 1990 two-button jacket's top button sat at or just below the waist; on Ron the
# balanced jacket's was still 15 cm above his)
STANCE = float(argv[argv.index("--stance-drop") + 1]) if "--stance-drop" in argv else 0.0
BAL_Y = (250.0, 350.0)


def balance(base, v):
    if base != "jaeger.front" or BALANCE == 0:
        return v
    xs = max(q[0] for q in P["jaeger.front"]["paths"]["seam"]["points"] if q[0] is not None)
    f = max(0.0, min(1.0, (xs - v[0]) / xs))
    t = max(0.0, min(1.0, (v[1] - BAL_Y[0]) / (BAL_Y[1] - BAL_Y[0])))
    return [v[0], v[1] + BALANCE * f * t * t * (3 - 2 * t)]


def stance(base, v):
    """The lower button stance: between the break point and the hem, near centre front (fully to 20 mm in from it,
    nothing from 100 mm), the front squeezed down towards the hem, the break point moving --stance-drop mm, the hem
    not at all (Jaeger's own lapelStart is at its limit; moving the buttons alone put the lower one in the curve of
    the front edge)."""
    if base != "jaeger.front" or STANCE == 0:
        return v
    pn = P["jaeger.front"]["points"]
    yb = balance(base, longer(base, pn["lapelBreakPoint"]))[1]
    yh = balance(base, longer(base, pn["hemEdge"]))[1]
    if not yb - 1e-6 <= v[1] <= yh:
        return v
    f = max(0.0, min(1.0, (100.0 - v[0]) / 80.0))
    return [v[0], v[1] + STANCE * f * (yh - v[1]) / (yh - yb)]


def fitted(base, v):
    """A point of Jaeger's drawing where this jacket has it: the skirt lengthened, the front balanced, the stance
    lowered."""
    return stance(base, balance(base, longer(base, v)))


def raw(name):
    pts = [p for p in P[name]["paths"]["seam"]["points"] if p[0] is not None]
    if len(pts) > 1 and math.dist(pts[0], pts[-1]) < 0.05:
        pts = pts[:-1]
    return [fitted(name, q) for q in pts]


def near(pts, v):
    return min(range(len(pts)), key=lambda k: (pts[k][0] - v[0]) ** 2 + (pts[k][1] - v[1]) ** 2)


def cross(a, b, c, d):
    """Where the line through a and b meets the line through c and d."""
    r = (b[0] - a[0], b[1] - a[1])
    q = (d[0] - c[0], d[1] - c[1])
    t = ((c[0] - a[0]) * q[1] - (c[1] - a[1]) * q[0]) / (r[0] * q[1] - r[1] * q[0])
    return [a[0] + t * r[0], a[1] + t * r[1]]


# THE OUTLINES AS SEWN, where Jaeger's differ (2 October):
# - the sleeves end at the finished cuff: Jaeger's sleeve outline carries a 30 mm hem turn-up below the wrist line
#   and, on both sleeve pieces, a 50 mm vent extension beyond the hindarm seam, which hang loose when nothing folds
#   them. So each sleeve piece is cut along the hindarm seam (elbow to the top of the vent, carried on down) and
#   along the wrist line; the vent becomes a closed seam, as on most ready-made suits of 1990 (its buttons sewn on).
# - the left back is cut along centre back below the vent's top: the vent's overlap. The right back keeps its
#   extension, the underlap lying beneath it, as a tailor makes a centre vent (left over right).
EXTRA = {}


def insert_on(pts, v):
    """The outline with point v put on its nearest edge (or the index of the sample already there)."""
    best = None
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]
        ab = (b[0] - a[0], b[1] - a[1])
        L2 = ab[0] ** 2 + ab[1] ** 2 or 1e-12
        t = max(0.0, min(1.0, ((v[0] - a[0]) * ab[0] + (v[1] - a[1]) * ab[1]) / L2))
        d = math.dist((a[0] + t * ab[0], a[1] + t * ab[1]), v)
        if best is None or d < best[0]:
            best = (d, i, t)
    d, i, t = best
    if d > 1.0:
        raise SystemExit("%s is %.1f mm off the outline" % (v, d))
    if math.dist(pts[i], v) < 0.3:
        return pts, i
    if math.dist(pts[(i + 1) % len(pts)], v) < 0.3:
        return pts, (i + 1) % len(pts)
    return pts[:i + 1] + [list(v)] + pts[i + 1:], i + 1


def reflect(q, a, b):
    """q reflected across the line through a and b."""
    d = (b[0] - a[0], b[1] - a[1])
    L2 = d[0] ** 2 + d[1] ** 2
    t = ((q[0] - a[0]) * d[0] + (q[1] - a[1]) * d[1]) / L2
    f = (a[0] + t * d[0], a[1] + t * d[1])
    return [2 * f[0] - q[0], 2 * f[1] - q[1]]


# THE LAPEL, 2 October. Marvelous turns a lapel over its roll line only with Fold Arrangement, a mouse tool with no
# script call (the research, MD-TAILORED-JACKET-2026-10-01.md; a fold angle alone moved a test panel 3 mm, and two
# drapes left the lapel standing and the facings outside the fronts). So the front is cut along the roll line, from
# the break point at the top button to the gorge, and the lapel is made its own piece, already turned: its outline
# reflected across the roll line, as it lies on the chest, sewn back to the front along the roll line as a hinge. It
# stands for both layers of a real lapel (the front's and the facing's, fused), so the facings go: below the break
# nothing outside shows them. Jaeger's lapel is 72 mm wide at the gorge, a 2010s width; a 1990 suit's was about
# 3 1/2 in (BELLY widens it to about 90 mm, the edge swinging out from the break point to the lapel's point).
BELLY = 20.0
CACHE = {}


def front_split():
    if "split" in CACHE:
        return CACHE["split"]
    pn = P["jaeger.front"]["points"]
    pts = [list(q) for q in raw("jaeger.front")]
    B, R = fitted("jaeger.front", pn["lapelBreakPoint"]), fitted("jaeger.front", pn["shoulderRoll"])
    lp = fitted("jaeger.front", pn["neckEdge"])
    pts, iB = insert_on(pts, B)
    n = len(pts)
    pts = pts[iB:] + pts[:iB]                    # B first
    iL = near(pts, lp)
    if iL > n / 2:                               # the lapel's edge upwards from B is to come first: wind it so
        pts = [pts[0]] + list(reversed(pts[1:]))
        iL = near(pts, lp)
    # the front edge from the break point to the lapel's point, resampled every 4 mm and swung out
    seq = pts[:iL + 1]
    dense = [list(seq[0])]
    for a, b in zip(seq, seq[1:]):
        m = max(1, int(math.dist(a, b) / 4.0))
        dense += [[a[0] + (b[0] - a[0]) * k / m, a[1] + (b[1] - a[1]) * k / m] for k in range(1, m + 1)]
    y0, y1 = B[1], lp[1]
    for q in dense[1:]:
        t = max(0.0, min(1.0, (y0 - q[1]) / (y0 - y1)))
        q[0] -= BELLY * t + 4.0 * math.sin(math.pi * t)
    pts = dense + [list(q) for q in pts[iL + 1:]]   # B, the lapel's edge up, the notch, ... round to before B
    pts, iR = insert_on(pts, R)
    lapel = pts[:iR + 1]                          # B .. lapel point .. notch .. R, closed by the roll line
    body = pts[iR:] + [pts[0]]                    # R .. collar corner .. neck .. hem .. B, closed by the roll line
    lap = [reflect(q, B, R) for q in lapel]
    lp2 = reflect(dense[-1], B, R)
    CACHE["split"] = (body, lap)
    EXTRA["jaeger.front~body"] = {"rollBottom": B, "rollTop": R}
    EXTRA["jaeger.front~lapel"] = {"rollBottom": B, "rollTop": R, "notch": reflect(pn["notch"], B, R), "lapelPoint": lp2}
    # the lapel held where it lies: its outer edge, from a third of the way up to just below its point, tacked to a
    # line drawn on the front beneath it (a hinge alone let the lapels slide under the fronts in a long settle, and
    # back in the next run); the roll near the break and at the top stays free
    i0, i1 = int(len(dense) * 0.35), int(len(dense) * 0.75)
    EXTRA["jaeger.front~lapel"].update({"tackStart": reflect(dense[i0], B, R), "tackEnd": reflect(dense[i1], B, R)})
    CACHE["lapelTack"] = [reflect(q, B, R) for q in dense[i0:i1 + 1]]
    CACHE["lapelWidth"] = abs((dense[-1][0] - B[0]) * (R[1] - B[1]) - (dense[-1][1] - B[1]) * (R[0] - B[0])) / math.dist(B, R)
    return CACHE["split"]


def outline(name):
    base = name.split("~")[0]
    if name == "jaeger.front~body":
        return front_split()[0]
    if name == "jaeger.front~lapel":
        return front_split()[1]
    pts = raw(base)
    pn = P[base]["points"]
    if base in ("jaeger.topsleeve", "jaeger.undersleeve"):
        wrist = "tsWristLeft" if base == "jaeger.topsleeve" else "usWristLeft"
        h = cross(pn["elbowRight"], pn["ventSlopeStart"], pn[wrist], pn["ventFoldRight"])
        i0, i1 = near(pts, pn["ventSlopeStart"]), near(pts, pn[wrist])
        EXTRA.setdefault(name, {})["cuffSeam"] = h
        return [h] + pts[i0:i1 + 1]
    if name == "jaeger.back~cut":
        out, gap = [], None
        for q in pts:
            if q[0] < pn["cbHem"][0] - 1.0 and q[1] > pn["ventSlopeStart"][1]:   # the extension, below the vent's top
                gap = len(out) if gap is None else gap
                continue
            out.append(q)
        out.insert(gap, list(pn["cbHem"]))
        return out
    return pts


def at(name, point):
    """The index on the piece's outline nearest one of its named points."""
    pts = outline(name)
    v = EXTRA.get(name, {}).get(point) or fitted(name.split("~")[0], P[name.split("~")[0]]["points"][point])
    i = min(range(len(pts)), key=lambda k: (pts[k][0] - v[0]) ** 2 + (pts[k][1] - v[1]) ** 2)
    d = math.dist(pts[i], v)
    if d > 1.0:
        raise SystemExit("%s.%s is %.1f mm off the outline" % (name, point, d))
    return i


def mirror(pts):
    return [[-x, y] for x, y in pts]


# WHICH COPY IS WHICH SIDE (2 October): Marvelous shows and arranges every piece from its outside, so a piece fits
# the side of the body on which its drawing, seen from outside, falls. Jaeger's front as drafted (centre front on the
# left, the side seam on the right) seen from outside is the wearer's LEFT front, and so are its side body, top sleeve
# and facing (the facing a copy of the front's edge); its back as drafted (centre back on the left) seen from behind
# is the wearer's RIGHT back, and its undersleeve (drawn as seen through the arm, its forearm edge on the left like
# the top sleeve's) the RIGHT arm's. "L" and "R" below are the wearer's left and right; each side's seams join
# pieces of that side only.
LEFT_IS_DRAFTED = {"jaeger.front", "jaeger.side", "jaeger.topsleeve", "jaeger.frontFacing"}


def mirrored(src, side):
    return (side == "R") if src.split("~")[0] in LEFT_IS_DRAFTED else (side == "L")


def piece(key, src, side, fabric="wool", fused=False, layer=0):
    pts = outline(src)
    pts = [[x, -y] for x, y in pts]                          # FreeSewing draws y down: flip to y up
    if mirrored(src, side):
        pts = mirror(pts)
    return {"key": key, "source": src, "side": side, "points": [[round(x, 2), round(y, 2)] for x, y in pts],
            "fabric": fabric, "fused": fused, "layer": layer}


pieces = []
for s in ("R", "L"):
    pieces += [piece("front" + s, "jaeger.front~body", s, fused=True),
               piece("side" + s, "jaeger.side", s),
               # the left back laps over the right at the vent: cut along centre back there, its layer above
               piece("back" + s, "jaeger.back" + ("~cut" if s == "L" else ""), s, layer=1 if s == "L" else 0),
               piece("topsleeve" + s, "jaeger.topsleeve", s),
               piece("undersleeve" + s, "jaeger.undersleeve", s),
               piece("lapel" + s, "jaeger.front~lapel", s, fused=True, layer=1)]
# THE COLLAR, 2 October: Jaeger's split collar, the stand (sewn to the neckline, up to the roll line) and the fall
# (from the roll line down to the collar's edge), made two pieces for the reason the lapel is: the fall is cut
# lying already turned down over the stand. Jaeger draws the collar with its neck edge at the top; worn, the stand's
# neck edge is at the bottom, so the stand is placed turned over (arranged upside down), and its +x end comes to the
# wearer's left; the fall, drawn with its roll edge at the top, is placed as drawn, its +x end on the wearer's
# right. (The first drapes placed a one-piece undercollar neck edge up, and it stayed behind the neck.)
pieces += [piece("stand", "jaeger.collarStand", "R", fused=True),
           piece("fall", "jaeger.collar", "R", fused=True, layer=1)]
keys = {p["key"]: p for p in pieces}

# THE POCKETS, drawn here: Jaeger drafts patch pockets, and Jafar's jacket has flap pockets and a welted breast
# pocket. The flap: as wide as the pocket mouth Jaeger marks on the front (to the side seam), 55 mm deep (2 1/4 in,
# the period's flap), its lower corners rounded 12 mm, sewn by its top edge to the mouth (a line drawn on the front)
# and lying over the front. The welt: the breast pocket's finished strip exactly as Jaeger marks it on the left
# front, sewn top and bottom to the two lines bounding it (research: "a welt cut into the front and Bonded, not a
# layered piece"; a strip sewn flat on both long edges is the nearest the pattern file allows).
fr = P["jaeger.front"]["points"]
FLAP_W = fr["frontPocketTopEnd"][0] - fr["frontPocketTopLeft"][0] - 1.0
FLAP_D, FLAP_R = 55.0, 12.0


def flap_outline():
    pts = [[0.0, 0.0], [FLAP_W, 0.0]]
    for k in range(0, 7):                                   # the lower right corner, rounded
        a = math.radians(-90 * k / 6)
        pts.append([FLAP_W - FLAP_R + FLAP_R * math.cos(a), -FLAP_D + FLAP_R + FLAP_R * math.sin(a)])
    for k in range(0, 7):                                   # the lower left corner
        a = math.radians(-90 - 90 * k / 6)
        pts.append([FLAP_R + FLAP_R * math.cos(a), -FLAP_D + FLAP_R + FLAP_R * math.sin(a)])
    out = []
    for q in pts:
        if not out or math.dist(out[-1], q) > 0.05:
            out.append([round(q[0], 2), round(q[1], 2)])
    return out


for s in ("R", "L"):
    pts = flap_outline()
    pieces.append({"key": "flap" + s, "source": None, "side": s, "points": mirror(pts) if s == "R" else pts,
                   "fabric": "wool", "fused": True, "layer": 1,
                   "named": {"topLeft": 0, "topRight": 1, "botRight": 8, "botLeft": 9}})
assert flap_outline()[8] == [round(FLAP_W - FLAP_R, 2), -FLAP_D] and flap_outline()[9] == [FLAP_R, -FLAP_D]
W = [[fr[n][0], -fr[n][1]] for n in ("chestPocketTopLeft", "chestPocketTopRight", "chestPocketBottomRight", "chestPocketBottomLeft")]
pieces.append({"key": "chestwelt", "source": None, "side": "L", "points": W, "fabric": "wool", "fused": True,
               "layer": 1, "named": {"topLeft": 0, "topRight": 1, "bottomRight": 2, "bottomLeft": 3}})
keys = {p["key"]: p for p in pieces}


def run(key, a, b):
    """A stretch of a piece's outline, from named point a to named point b (along the outline's own order; the
    seam's direction is a to b)."""
    if keys[key]["source"] is None:                          # a piece drawn here: its corners by name
        nm = keys[key]["named"]
        return {"piece": key, "from": nm[a], "to": nm[b], "names": [a, b]}
    src = keys[key]["source"]
    i, j, n = at(src, a), at(src, b), len(outline(src))
    # a stretch from the outline's first point to a point past its middle runs the short way round, to its end:
    # written as ending at n, so it is not read as the whole outline the other way (make_jacket_job.py)
    if i == 0 and j > n / 2:
        i = n
    if j == 0 and i > n / 2:
        j = n
    return {"piece": key, "from": i, "to": j, "names": [a, b]}


seams = []
for s in ("R", "L"):
    F, S, B, T, U = "front" + s, "side" + s, "back" + s, "topsleeve" + s, "undersleeve" + s
    seams += [
        # the body: the front to the side body, the side body to the back, the shoulders
        [run(F, "hem", "fsArmhole"), run(S, "sideHem", "fsArmhole")],
        [run(S, "bsHem", "bsArmholeHollow"), run(B, "hem", "armholeHollow")],
        [run(F, "shoulder", "neck"), run(B, "shoulder", "neck")],
        # the sleeve's two seams: the hindarm from the cuff to the back pitch (the undersleeve's tip reaches it), the
        # forearm from the cuff to the head
        [run(T, "cuffSeam", "backPitchPoint"), run(U, "cuffSeam", "usTip")],
        [run(T, "tsLeftEdge", "tsWristLeft"), run(U, "usLeftEdge", "usWristLeft")],
        # the sleeve head, set round the armhole from the back pitch and back to it, its ease (5 mm on Ron's draft,
        # 551 against 546) spread evenly, so the crown falls about 2 cm forward of the shoulder seam. Pinned at the
        # crown as well, the back of the head carried 19 mm of ease and the rest 15 mm too little; the pitch points
        # Jaeger marks on the top sleeve fall elsewhere on the front (156 against 99 mm to the front pitch).
        [[run(T, "backPitchPoint", "tsLeftEdge"), run(U, "usLeftEdge", "usTip")],
         [run(B, "backArmholePitch", "shoulder"), run(F, "shoulder", "fsArmhole"), run(S, "fsArmhole", "bsArmholeHollow"),
          run(B, "armholeHollow", "backArmholePitch")]],
        # the lapel to the front along the roll line (the hinge)
        [run(F, "rollBottom", "rollTop"), run("lapel" + s, "rollBottom", "rollTop")],
    ]
# the backs to each other down the centre, to the top of the vent
seams.append([run("backR", "cbNeck", "ventSlopeStart"), run("backL", "cbNeck", "ventSlopeStart")])
# the stand's neck edge to the neckline, each half one stretch against two (the front's neck, the back's), its +x
# half to the wearer's left (the stand is placed upside down)
seams += [
    [[run("stand", "collarCorner", "collarstandCbBottom")], [run("frontL", "collarCorner", "neck"), run("backL", "neck", "cbNeck")]],
    [[run("stand", "collarstandCbBottom", "leftCollarCorner")], [run("backR", "cbNeck", "neck"), run("frontR", "neck", "collarCorner")]],
]
# the fall to the stand along the roll line (the hinge): the stand's left end meets the fall's -x end
seams += [
    [[run("stand", "collarstandTip", "collarstandCbTop")], [run("fall", "collarstandTipLeft", "collarstandCbTop")]],
    [[run("stand", "collarstandCbTop", "leftCollarstandTip")], [run("fall", "collarstandCbTop", "collarstandTip")]],
]
# THE GORGE: the collar's end (the stand's, then the fall's to the notch) to the front's gorge (the front's, then the
# lapel's to the notch). The first drapes left this unsewn, and the collar slid back round the neck.
seams += [
    [[run("stand", "collarCorner", "collarstandTip"), run("fall", "collarstandTipLeft", "notchLeft")],
     [run("frontL", "collarCorner", "rollTop"), run("lapelL", "rollTop", "notch")]],
    [[run("stand", "leftCollarCorner", "leftCollarstandTip"), run("fall", "collarstandTip", "notch")],
     [run("frontR", "collarCorner", "rollTop"), run("lapelR", "rollTop", "notch")]],
]
# every seam as two lists of stretches (most are one against one)
seams = [[a if isinstance(a, list) else [a], b if isinstance(b, list) else [b]] for a, b in seams]

folds = []                                   # the lapel and the collar's fall are cut already turned (above)
fr = P["jaeger.front"]["points"]


# POCKETS: the flap's top edge at the front's pocket line; the welt on the left chest
def line_of(part, path):
    pts = [p for p in P[part]["paths"][path]["points"] if p[0] is not None]
    return [[x, -y] for x, y in pts]


FP = lambda n: fitted("jaeger.front", fr[n])  # noqa: E731
pockets = {"flapLine": line_of("jaeger.front", "frontPocket"), "chestLine": line_of("jaeger.front", "chestPocket"),
           "buttons": [[FP("button1")[0], -FP("button1")[1]], [FP("button2")[0], -FP("button2")[1]]]}
# LINES DRAWN ON THE PIECES (Marvelous's internal lines): the roll lines (folds), each flap's pocket mouth, the welt's
# two edges, and the button tacks. A tack is a 10 mm line at a button's place on centre front, the same on both
# fronts, sewn to its twin: the jacket buttoned (the research: buttons are fastened only by hand in Marvelous, so the
# fronts are held where the buttons would hold them). Each internal line: piece, name, points (mm, y up), fold.
internals = []
for f in folds:
    internals.append({"piece": f["piece"], "name": "roll", "points": f["line"], "fold": f["angle"]})
fl = pockets["flapLine"]
mtl = FP("frontPocketTopLeft")
mtr = fitted("jaeger.front", [fr["frontPocketTopLeft"][0] + FLAP_W, fr["frontPocketTopLeft"][1]])
_m = math.dist(mtl, mtr)
mouth = [[mtl[0], -mtl[1]], [mtl[0] + (mtr[0] - mtl[0]) * FLAP_W / _m, -(mtl[1] + (mtr[1] - mtl[1]) * FLAP_W / _m)]]
internals += [{"piece": "frontR", "name": "flapMouth", "points": mirror(mouth), "fold": None},
              {"piece": "frontL", "name": "flapMouth", "points": mouth, "fold": None},
              {"piece": "frontL", "name": "weltTop", "points": W[0:2], "fold": None},
              {"piece": "frontL", "name": "weltBottom", "points": [W[3], W[2]], "fold": None}]
for k, (bx, by) in enumerate(pockets["buttons"]):
    for s in ("R", "L"):
        internals.append({"piece": "front" + s, "name": "tack%d" % k, "points": [[bx - 5.0, by], [bx + 5.0, by]], "fold": None})
# each flap held flat by its bottom edge too (it hangs that way when he stands; one wandered up the chest unheld),
# and each lapel by its outer edge (front_split above)
# the flap's foot along the mouth's slope (the balance tilts the mouth a little towards centre front)
_dx, _dy = mouth[1][0] - mouth[0][0], mouth[1][1] - mouth[0][1]
_L = math.hypot(_dx, _dy)
_ux, _uy = _dx / _L, _dy / _L
bottom = [[mouth[0][0] + _ux * FLAP_R + _uy * FLAP_D, mouth[0][1] + _uy * FLAP_R - _ux * FLAP_D],
          [mouth[0][0] + _ux * (_L - FLAP_R) + _uy * FLAP_D, mouth[0][1] + _uy * (_L - FLAP_R) - _ux * FLAP_D]]
lt = [[x, -y] for x, y in CACHE["lapelTack"]]
internals += [{"piece": "frontR", "name": "flapBottom", "points": mirror(bottom), "fold": None},
              {"piece": "frontL", "name": "flapBottom", "points": bottom, "fold": None},
              {"piece": "frontR", "name": "lapelTack", "points": mirror(lt), "fold": None},
              {"piece": "frontL", "name": "lapelTack", "points": lt, "fold": None}]
# seams onto internal lines: a stretch of a piece's outline against a whole internal line, or line against line
inner = lambda piece, name: {"piece": piece, "internal": name}  # noqa: E731
inseams = [[[run("flapR", "topLeft", "topRight")], [inner("frontR", "flapMouth")]],
           [[run("flapL", "topLeft", "topRight")], [inner("frontL", "flapMouth")]],
           [[run("chestwelt", "topLeft", "topRight")], [inner("frontL", "weltTop")]],
           [[run("chestwelt", "bottomLeft", "bottomRight")], [inner("frontL", "weltBottom")]]]
for k in range(len(pockets["buttons"])):
    inseams.append([[inner("frontR", "tack%d" % k)], [inner("frontL", "tack%d" % k)]])
for s in ("R", "L"):
    inseams += [[[run("flap" + s, "botLeft", "botRight")], [inner("front" + s, "flapBottom")]],
                [[run("lapel" + s, "tackStart", "tackEnd")], [inner("front" + s, "lapelTack")]]]
spec = {"pattern": SRC, "measurements": pat.get("measurements"), "pieces": pieces, "seams": seams, "folds": folds,
        "pockets": pockets, "internals": internals, "inseams": inseams}
json.dump(spec, open(OUT, "w", encoding="utf-8"), indent=1)
print("spec: %d pieces, %d seam pairs, %d lines drawn, %d seams onto them, lapel %.0f mm wide -> %s" % (
    len(pieces), len(seams), len(internals), len(inseams), CACHE.get("lapelWidth", 0), OUT))
for a, b in seams:
    print("  %s  <->  %s" % (" + ".join("%s %s-%s" % (r["piece"], *r["names"]) for r in a),
                             " + ".join("%s %s-%s" % (r["piece"], *r["names"]) for r in b)))
