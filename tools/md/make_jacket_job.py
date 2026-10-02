"""The jacket specification (tools/md/jaeger_spec.py's JSON) as a job for Marvelous Designer (run by the bridge,
tools/md/md_bridge.py): the pieces made from their outlines, their seams sewn, the roll lines drawn, the fused pieces
stiffened, the layers set.

    python tools/md/make_jacket_job.py SPEC.json JOB.py [--tol 0.8] [--corner 0 --curve 1]

WHY, 1 October (Jafar's Marvelous proof, CLOTHES.md item 0). In Marvelous a piece's outline is a chain of lines
between corner points, with curve points inside a line, and a seam joins whole lines (AddSeamlinePairGroup). So every
end of a seam stretch on a piece becomes a corner point, and the outline between them curve points; then each seam
stretch is one line, numbered in the outline's order. The outlines (sampled every 2 mm by FreeSewing) are thinned to
points no more than --tol mm off the curve. The job prints, for each piece, its pattern index and the line number of
each corner-to-corner stretch, so later jobs (arrangement, sewing, simulation) can refer to them.
"""
import json
import math
import sys

argv = sys.argv[1:]
SPEC, JOB = argv[0], argv[1]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


TOL = opt("--tol", 0.8)
CORNER, CURVE = opt("--corner", 0, int), opt("--curve", 1, int)
spec = json.load(open(SPEC, encoding="utf-8"))


def simplify(pts, keep, tol):
    """Douglas-Peucker on a closed outline, never dropping the indices in keep."""
    n = len(pts)
    must = sorted(set(keep) | {0})
    out = set(must)

    def rec(i, j):
        # points strictly between i and j (indices mod n)
        idx = [(i + k) % n for k in range(1, (j - i) % n)]
        if not idx:
            return
        a, b = pts[i % n], pts[j % n]
        ab = (b[0] - a[0], b[1] - a[1])
        L = math.hypot(*ab) or 1e-9
        best, bd = None, -1.0
        for k in idx:
            p = pts[k]
            d = abs((p[0] - a[0]) * ab[1] - (p[1] - a[1]) * ab[0]) / L
            if d > bd:
                bd, best = d, k
        if bd > tol:
            out.add(best)
            rec(i, best)
            rec(best, j if j > best else j + n)

    for a, b in zip(must, must[1:] + [must[0] + n]):
        rec(a, b)
    return sorted(out)


# the corners of each piece: every seam stretch's two ends, and the outline's sharp turns (over 35 degrees)
corners = {p["key"]: set() for p in spec["pieces"]}
for a_runs, b_runs in spec["seams"]:
    for r in a_runs + b_runs:
        corners[r["piece"]].update((r["from"], r["to"]))
pieces_out = []
for p in spec["pieces"]:
    pts = p["points"]
    n = len(pts)
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (b[0] - a[0], b[1] - a[1])
        v2 = (c[0] - b[0], c[1] - b[1])
        n1, n2 = math.hypot(*v1), math.hypot(*v2)
        if n1 > 1e-6 and n2 > 1e-6:
            cosang = (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)
            if cosang < math.cos(math.radians(35)):
                corners[p["key"]].add(i)
    keep = sorted(corners[p["key"]])
    idx = simplify(pts, keep, TOL)
    # the left pieces are mirrored, so their outline runs the other way round: Marvelous wants one winding; the
    # job reverses them and the line numbers are counted on the reversed outline
    reverse = p["side"] == "L"
    order = list(reversed(idx)) if reverse else idx
    corner_set = set(keep)
    out_pts = [[pts[i][0], pts[i][1], CORNER if i in corner_set else CURVE] for i in order]
    corner_order = [i for i in order if i in corner_set]
    pieces_out.append({"key": p["key"], "points": out_pts, "corners": corner_order, "reverse": reverse,
                       "fabric": p["fabric"], "fused": p["fused"], "layer": p["layer"], "outlineLen": n})


def line_of(piece, i_from, i_to):
    """The line number (0-based, in the job's outline order) of the stretch from corner i_from to corner i_to, and
    whether the seam runs against the outline's direction."""
    po = next(q for q in pieces_out if q["key"] == piece)
    cs = po["corners"]
    k = len(cs)
    for j in range(k):
        a, b = cs[j], cs[(j + 1) % k]
        if {a, b} == {i_from, i_to}:
            return j, (a != i_from)
    # a stretch spanning several corner-to-corner lines: list them
    return None, None


def lines_of(piece, i_from, i_to):
    """The job's line numbers covering the stretch from outline index i_from to i_to, and whether the seam runs
    against the job's outline direction. Every stretch in this pattern lies between its two ends without passing the
    outline's start (index 0), so the stretch is the corners between the two indices (the shorter way round would
    take the facing's inside edge for its front edge)."""
    po = next(q for q in pieces_out if q["key"] == piece)
    cs = po["corners"]
    lo, hi = min(i_from, i_to), max(i_from, i_to)
    if i_from not in cs or i_to not in cs:
        raise SystemExit("%s: %d or %d is not a corner" % (piece, i_from, i_to))
    lines = [j for j in range(len(cs) - 1) if lo <= cs[j] <= hi and lo <= cs[j + 1] <= hi]
    increasing = not po["reverse"]
    rev = (i_from > i_to) if increasing else (i_from < i_to)
    if rev:
        lines = list(reversed(lines))
    if not lines:
        raise SystemExit("%s: no lines between %d and %d" % (piece, i_from, i_to))
    return lines, rev


seams_out = []
for a_runs, b_runs in spec["seams"]:
    sa, sb = [], []
    for r in a_runs:
        ls, rev = lines_of(r["piece"], r["from"], r["to"])
        sa.append({"piece": r["piece"], "lines": ls, "reversed": rev, "names": r["names"]})
    for r in b_runs:
        ls, rev = lines_of(r["piece"], r["from"], r["to"])
        sb.append({"piece": r["piece"], "lines": ls, "reversed": rev, "names": r["names"]})
    seams_out.append([sa, sb])

plan = {"pieces": pieces_out, "seams": seams_out, "folds": spec["folds"], "pockets": spec["pockets"]}
job = '''# Generated by tools/md/make_jacket_job.py from %(spec)s: make the jacket's pieces in Marvelous Designer.
import json
PLAN = json.loads(%(plan)r)
made = {}
for p in PLAN["pieces"]:
    pts = [(float(x), float(y), int(t)) for x, y, t in p["points"]]
    idx = pattern_api.CreatePatternWithPoints(pts)
    made[p["key"]] = idx
    try:
        pattern_api.SetPatternPieceName(idx, p["key"])
    except Exception as e:
        print("name", p["key"], e)
print("MADE", json.dumps(made))
JACKET = {"made": made, "plan": PLAN}
''' % {"spec": SPEC, "plan": json.dumps(plan)}
open(JOB, "w", encoding="utf-8").write(job)
print("job: %d pieces (%s points), %d seams -> %s" % (len(pieces_out), sum(len(p["points"]) for p in pieces_out), len(seams_out), JOB))
for p in pieces_out:
    print("  %-14s %3d points, %2d corners" % (p["key"], len(p["points"]), len(p["corners"])))
