"""The jacket's seams and folds written into Marvelous Designer's own pattern file, ready to import.

    python tools/md/write_pattern.py DIR PLAN.json OUT.json [--roll 330 --roll-strength 8]

DIR holds what the pieces job wrote (tools/md/make_jacket_job.py --out): pieces.json, Marvelous's export of the
pieces and their drawn lines (pattern_api.ExportPatternJSON), and made.json, each piece's index and its lines as
Marvelous measures them (GetPatternLineInfo). PLAN.json is the job's plan (written beside the job): each seam as
stretches of outline lines in seam order, or a whole drawn line; the drawn lines and their folds.

WHY, 2 October (the jacket proof): Marvelous's script calls cannot set fold angles, turned seams, or a seam that
runs one line against two; its pattern file can. Learnt by exporting test pieces (tools/md/jobs/learn2.py, learn5.py):
each drawn line carries FoldData {iAngle, iStrength} (kept on import), each seam group bIsTurned and FoldData, each
pair of stretches a ShapeID, LineID and LengthParam {fStart, fEnd} (fractions of the piece's whole outline; when
Direction is false the stretch runs from fStart back to fEnd). A stretch of outline names the piece's ID; a drawn
line names the drawn shape's own ID (naming the piece with a drawn line's LineID, Marvelous moved the seam onto the
outline). So every seam is measured on both sides, cut wherever either side changes line, and its bits paired. The
front edge (front to facing, round the lapel) and the collar's outer edge (top collar to undercollar) are turned
seams, sewn face to face as a tailor does, with no fold strength: they puffed otherwise
(production/research/clothing-pipeline/MD-TAILORED-JACKET-2026-10-01.md). Each roll line gets its fold angle (180 is
flat; --roll sets the lapel's and collar's turn).
"""
import json
import math
import os
import sys

argv = sys.argv[1:]
DIR, PLAN, OUT = argv[0], argv[1], argv[2]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


ROLL, ROLL_K = opt("--roll", 330, int), opt("--roll-strength", 8, int)
pat = json.load(open(os.path.join(DIR, "pieces.json"), encoding="utf-8"))
mj = json.load(open(os.path.join(DIR, "made.json"), encoding="utf-8"))
plan = json.load(open(PLAN, encoding="utf-8"))
made, lineinfo = mj["made"], mj["lineinfo"]
P = pat["PatternList"]
pid = {key: P[idx]["ID"] for key, idx in made.items() if idx >= 0}
line_ids = {key: [l["ID"] for l in P[idx]["ShapeInfo"]["LineList"]] for key, idx in made.items() if idx >= 0}
lengths = {key: [float(l["length"]) for l in lineinfo[key]["lines"]] for key in pid}
for key in pid:
    if len(lengths[key]) != len(line_ids[key]):
        raise SystemExit("%s: %d measured lines, %d in the file" % (key, len(lengths[key]), len(line_ids[key])))


def pts_of(shape):
    out = []
    for l in shape["LineList"]:
        for q in l["PointList"]:
            v = (q["Position"]["x"], q["Position"]["y"])
            if not out or math.dist(out[-1], v) > 1e-6:
                out.append(v)
    return out


# each drawn line in the plan found in the file by its two ends (Marvelous adds its own closed base line too)
drawn = {}
for il in plan["internals"]:
    shapes = [s for s in P[made[il["piece"]]].get("InternalLineList", []) if not s.get("IsClosed")]
    a, b = il["points"][0], il["points"][-1]
    best = min(shapes, key=lambda s: math.dist(pts_of(s)[0], a) + math.dist(pts_of(s)[-1], b))
    q = pts_of(best)
    if math.dist(q[0], a) + math.dist(q[-1], b) > 1.0:
        raise SystemExit("%s %s: no drawn line ends at %s, %s" % (il["piece"], il["name"], a, b))
    if len(best["LineList"]) != 1:
        raise SystemExit("%s %s: drawn as %d lines" % (il["piece"], il["name"], len(best["LineList"])))
    drawn[(il["piece"], il["name"])] = best
    if il.get("fold") is not None:
        best["FoldData"] = {"iAngle": ROLL, "iStrength": ROLL_K, "bRenderFolded": True}


def bits(runs):
    """A seam side as [piece or (piece, drawn line), line, from, to (fractions of the line), length, forward] bits."""
    out = []
    for r in runs:
        if "internal" in r:
            s = drawn[(r["piece"], r["internal"])]
            q = pts_of(s)
            L = sum(math.dist(q[k], q[k + 1]) for k in range(len(q) - 1))
            out.append([(r["piece"], r["internal"]), 0, 0.0, 1.0, L, True])
            continue
        for j in r["lines"]:
            out.append([r["piece"], j, 0.0, 1.0, lengths[r["piece"]][j], not r["reversed"]])
    return out


def cut(side, marks):
    """Cut a side's bits at the seam fractions in marks (0..1 of the side's whole length)."""
    total = sum(b[4] for b in side)
    pos, out = 0.0, []
    for b in side:
        s0, s1 = pos / total, (pos + b[4]) / total
        at = [s0] + [m for m in marks if s0 + 1e-6 < m < s1 - 1e-6] + [s1]
        for u0, u1 in zip(at, at[1:]):
            f0, f1 = (u0 - s0) / (s1 - s0), (u1 - s0) / (s1 - s0)
            out.append([b[0], b[1], f0, f1, b[4] * (f1 - f0), b[5]])
        pos += b[4]
    return out


def end(b):
    """One side of a pair: the shape, its line and the stretch as fractions of the shape's whole outline."""
    piece, line, f0, f1, _, fwd = b
    if isinstance(piece, tuple):                            # a drawn line: one line, the shape's whole length
        s = drawn[piece]
        return {"ShapeID": s["ID"], "LengthParam": {"fStart": round(f0, 6), "fEnd": round(f1, 6)}, "Direction": True,
                "LineID": s["LineList"][0]["ID"]}
    L = lengths[piece]
    total, start = sum(L), sum(L[:line])
    if fwd:
        a, b2 = start + f0 * L[line], start + f1 * L[line]
    else:                                                   # against the outline: from the line's far end back
        a, b2 = start + (1 - f0) * L[line], start + (1 - f1) * L[line]
    return {"ShapeID": pid[piece], "LengthParam": {"fStart": round(a / total, 6), "fEnd": round(b2 / total, 6)},
            "Direction": bool(fwd), "LineID": line_ids[piece][line]}


# HINGES, 2 October: the lapel and the collar's fall are cut lying already turned over the front and the stand
# (tools/md/jaeger_spec.py), and sewn back along the roll line; that seam must not straighten them out, so it carries
# no fold strength, and --hinge-turned says whether Marvelous is told the two lie folded onto each other (1) or not.
HINGES = [{"front", "lapel"}, {"stand", "fall"}]
HINGE_TURNED = bool(opt("--hinge-turned", 1, int))


def kind(p):
    p = p[0] if isinstance(p, tuple) else p
    return p.rstrip("RL")


groups, mismatch = [], []
for n, (a_runs, b_runs) in enumerate(plan["seams"] + plan.get("inseams", [])):
    A, B = bits(a_runs), bits(b_runs)
    ta, tb = sum(x[4] for x in A), sum(x[4] for x in B)
    mismatch.append((abs(ta - tb) / max(ta, tb), n, round(ta, 1), round(tb, 1)))
    # each side cut where either changes line; breaks within 3 mm of each other are one break, each side cut at its
    # own (a sliver of 0.04 mm, where the front's lapel line and the facing's differ by that much, made Marvelous
    # throw away every seam in the file)
    brk = sorted([(sum(x[4] for x in A[:k]) / ta, "A") for k in range(1, len(A))] +
                 [(sum(x[4] for x in B[:k]) / tb, "B") for k in range(1, len(B))])
    tol, clusters = 3.0 / min(ta, tb), []
    for f, who in brk:
        if clusters and f - clusters[-1][-1][0] < tol:
            clusters[-1].append((f, who))
        else:
            clusters.append([(f, who)])
    ma, mb = [], []
    for c in clusters:
        mean = sum(f for f, _ in c) / len(c)
        ma.append(next((f for f, w in c if w == "A"), mean))
        mb.append(next((f for f, w in c if w == "B"), mean))
    ca, cb = cut(A, ma), cut(B, mb)
    if len(ca) != len(cb):
        raise SystemExit("seam %d: %d bits against %d" % (n, len(ca), len(cb)))
    pieces_in = sorted({r["piece"] for r in a_runs + b_runs})
    hinge = {kind(p) for p in pieces_in} in HINGES
    groups.append({"Name": "S%02d_%s" % (n, "_".join(pieces_in)), "bIsTurned": hinge and HINGE_TURNED,
                   "FoldData": {"iAngle": 180, "iStrength": 0 if hinge else 5},
                   "PairList": [{"First": end(x), "Second": end(y)} for x, y in zip(ca, cb)]})
pat["SeamLinePairGroupList"] = groups
json.dump(pat, open(OUT, "w", encoding="utf-8"), indent=1)
print("pattern: %d seam groups (%d turned), %d pairs, %d lines folded to %d -> %s" % (
    len(groups), sum(g["bIsTurned"] for g in groups), sum(len(g["PairList"]) for g in groups),
    sum(1 for il in plan["internals"] if il.get("fold") is not None), ROLL, OUT))
for m, n, ta, tb in sorted(mismatch, reverse=True)[:6]:
    print("  seam %2d: %.1f against %.1f mm (%.1f%% apart)  %s" % (n, ta, tb, 100 * m, groups[n]["Name"]))
