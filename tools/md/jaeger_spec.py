"""FreeSewing's Jaeger jacket (tools/meshgen/freesewing_draft.mjs's JSON) as a sewing specification for Marvelous
Designer: the pieces (each outline in millimetres, y up, left and right copies), their seams (which stretch of one
piece's edge is sewn to which stretch of another's, by Jaeger's own named points), the lapel's roll line as a fold,
which pieces are fused, and the pockets' places.

    python tools/md/jaeger_spec.py PATTERN.json SPEC.json [--picture SPEC.png]

WHY, 1 October (Jafar's Marvelous proof, DECISIONS.md and CLOTHES.md item 0): the jacket is made the tailor's way
in Marvelous Designer, from our own pattern, FreeSewing's Jaeger (MIT). A tailored jacket's pieces: two fronts (the
lapel cut in one with each), two side bodies, two backs (a centre-back seam opening into the vent), two two-piece
sleeves, an undercollar and a top collar, two front facings (the lapel's visible face), two hip-pocket flaps and a
chest welt. The seams follow the pattern's names, so they move with any size the pattern is drafted at: the sleeve
head is set at its pitch points (the top sleeve's front and back pitch to the front's and back's, its crown to the
shoulder), the undersleeve into the underarm.
The front's lining and the pocket bags are left out: nothing outside shows them.
"""
import json
import math
import sys

argv = sys.argv[1:]
SRC, OUT = argv[0], argv[1]
pat = json.load(open(SRC, encoding="utf-8"))
P = pat["parts"]


def outline(name):
    pts = [p for p in P[name]["paths"]["seam"]["points"] if p[0] is not None]
    if len(pts) > 1 and math.dist(pts[0], pts[-1]) < 0.05:
        pts = pts[:-1]
    return pts


def at(name, point):
    """The index on the piece's outline nearest one of its named points."""
    pts = outline(name)
    v = P[name]["points"][point]
    i = min(range(len(pts)), key=lambda k: (pts[k][0] - v[0]) ** 2 + (pts[k][1] - v[1]) ** 2)
    d = math.dist(pts[i], v)
    if d > 1.0:
        raise SystemExit("%s.%s is %.1f mm off the outline" % (name, point, d))
    return i


def mirror(pts):
    return [[-x, y] for x, y in pts]


def piece(key, src, side, fabric="wool", fused=False, layer=0):
    pts = outline(src)
    # FreeSewing draws y down: flip to y up; the right side is the pattern as drafted (the wearer's right front),
    # the left its mirror
    pts = [[x, -y] for x, y in pts]
    if side == "L":
        pts = mirror(pts)
    return {"key": key, "source": src, "side": side, "points": [[round(x, 2), round(y, 2)] for x, y in pts],
            "fabric": fabric, "fused": fused, "layer": layer}


pieces = []
for s in ("R", "L"):
    pieces += [piece("front" + s, "jaeger.front", s, fused=True),
               piece("side" + s, "jaeger.side", s),
               piece("back" + s, "jaeger.back", s),
               piece("topsleeve" + s, "jaeger.topsleeve", s),
               piece("undersleeve" + s, "jaeger.undersleeve", s),
               piece("facing" + s, "jaeger.frontFacing", s, fused=True, layer=1),
               piece("flap" + s, "jaeger.pocket", s, layer=1)]
pieces += [piece("undercollar", "jaeger.underCollar", "R", fused=True),
           piece("topcollar", "jaeger.underCollar", "R", fused=True, layer=1),
           piece("chestwelt", "jaeger.chestPocketWelt", "L", fused=True, layer=1)]
keys = {p["key"]: p for p in pieces}


def run(key, a, b):
    """A stretch of a piece's outline, from named point a to named point b (along the outline's own order; the
    seam's direction is a to b)."""
    src = keys[key]["source"]
    return {"piece": key, "from": at(src, a), "to": at(src, b), "names": [a, b]}


seams = []
for s in ("R", "L"):
    F, S, B, T, U, FA = "front" + s, "side" + s, "back" + s, "topsleeve" + s, "undersleeve" + s, "facing" + s
    seams += [
        # the body: the front to the side body, the side body to the back, the shoulders
        [run(F, "hem", "fsArmhole"), run(S, "sideHem", "fsArmhole")],
        [run(S, "bsHem", "bsArmholeHollow"), run(B, "hem", "armholeHollow")],
        [run(F, "shoulder", "neck"), run(B, "shoulder", "neck")],
        # the sleeve's two seams
        [run(T, "elbowRight", "tsRightEdge"), run(U, "elbowRight", "usRightEdge")],
        [run(T, "tsLeftEdge", "tsWristLeft"), run(U, "usLeftEdge", "usWristLeft")],
        # the sleeve head: the top sleeve's crown to the shoulder at its pitch points, the undersleeve to the underarm
        [run(T, "top", "frontPitchPoint"), run(F, "shoulder", "armholePitch")],
        [run(T, "frontPitchPoint", "tsLeftEdge"), run(F, "armholePitch", "armholeHollow")],
        [run(T, "backPitchPoint", "top"), run(B, "backArmholePitch", "shoulder")],
        [run(T, "tsRightEdge", "backPitchPoint"), run(B, "armholeHollow", "backArmholePitch")],
        [run(U, "usLeftEdge", "usTip"), run(F, "armholeHollow", "fsArmhole")],
        [run(U, "usTip", "usRightEdge"), run(S, "fsArmhole", "bsArmholeHollow")],
        # the facing to the front, from the gorge round the lapel and down the front edge to the hem
        [run(F, "collarCorner", "facingBottom"), run(FA, "collarCorner", "facingBottom")],
    ]
# the backs to each other down the centre, to the top of the vent
seams.append([run("backR", "cbNeck", "ventSlopeStart"), run("backL", "cbNeck", "ventSlopeStart")])
# the undercollar's neck edge to the neckline, each half one stretch against two: the front's gorge, then the back's neck
seams += [
    [[run("undercollar", "collarCorner", "collarstandCbBottom")], [run("frontR", "collarCorner", "neck"), run("backR", "neck", "cbNeck")]],
    [[run("undercollar", "collarstandCbBottom", "leftCollarCorner")], [run("backL", "cbNeck", "neck"), run("frontL", "neck", "collarCorner")]],
]
# the top collar to the undercollar round its outer edge (the fall)
seams.append([run("topcollar", "notchLeft", "notch"), run("undercollar", "notchLeft", "notch")])
# every seam as two lists of stretches (most are one against one)
seams = [[a if isinstance(a, list) else [a], b if isinstance(b, list) else [b]] for a, b in seams]

# THE LAPEL'S ROLL LINE: on each front, from the break point (the top button, on the front edge) to the collar line at
# the shoulder; a fold, the lapel turning out over it
fr = P["jaeger.front"]["points"]
roll = [[fr["lapelBreakPoint"][0], -fr["lapelBreakPoint"][1]], [fr["shoulderRoll"][0], -fr["shoulderRoll"][1]]]
folds = [{"piece": "frontR", "line": roll, "angle": 180},
         {"piece": "frontL", "line": mirror(roll), "angle": 180},
         {"piece": "facingR", "line": roll, "angle": 180},
         {"piece": "facingL", "line": mirror(roll), "angle": 180}]
# the collar's roll line (the fold between stand and fall)
uc = P["jaeger.underCollar"]["points"]
croll = [[uc["notchTipRollLeft"][0], -uc["notchTipRollLeft"][1]], [uc["collarCbTopRoll"][0], -uc["collarCbTopRoll"][1]],
         [uc["notchTipRoll"][0], -uc["notchTipRoll"][1]]]
folds += [{"piece": "undercollar", "line": croll, "angle": 160}, {"piece": "topcollar", "line": croll, "angle": 160}]

# POCKETS: the flap's top edge at the front's pocket line; the welt on the left chest
def line_of(part, path):
    pts = [p for p in P[part]["paths"][path]["points"] if p[0] is not None]
    return [[x, -y] for x, y in pts]


pockets = {"flapLine": line_of("jaeger.front", "frontPocket"), "chestLine": line_of("jaeger.front", "chestPocket"),
           "buttons": [[fr["button1"][0], -fr["button1"][1]], [fr["button2"][0], -fr["button2"][1]]]}
spec = {"pattern": SRC, "measurements": pat.get("measurements"), "pieces": pieces, "seams": seams, "folds": folds,
        "pockets": pockets}
json.dump(spec, open(OUT, "w", encoding="utf-8"), indent=1)
print("spec: %d pieces, %d seam pairs, %d folds -> %s" % (len(pieces), len(seams), len(folds), OUT))
for a, b in seams:
    print("  %s  <->  %s" % (" + ".join("%s %s-%s" % (r["piece"], *r["names"]) for r in a),
                             " + ".join("%s %s-%s" % (r["piece"], *r["names"]) for r in b)))
