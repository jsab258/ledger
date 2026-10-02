"""The jacket specification (tools/md/jaeger_spec.py's JSON) as a job for Marvelous Designer (run by the bridge,
tools/md/md_bridge.py): the pieces made from their outlines, their seams sewn, the roll lines drawn, the fused pieces
stiffened, the layers set.

    python tools/md/make_jacket_job.py SPEC.json JOB.py [--out DIR] [--tol 0.8] [--corner 0 --curve 2]

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
CORNER, CURVE = opt("--corner", 0, int), opt("--curve", 2, int)   # 2: a spline through the point (1 was ignored: a straight line)
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
for a_runs, b_runs in spec["seams"] + spec.get("inseams", []):
    for r in a_runs + b_runs:
        if "internal" not in r:
            n_ = len(next(q for q in spec["pieces"] if q["key"] == r["piece"])["points"])
            corners[r["piece"]].update((r["from"] % n_, r["to"] % n_))
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
    # the line numbers are counted on the job's outline, reversed when the piece winds clockwise
    # one winding for every piece, counter-clockwise (y up), or Marvelous refuses it (1 October: the right sleeve's
    # pieces and the left facing came back -1, wound the other way)
    area = sum(pts[idx[k]][0] * pts[idx[(k + 1) % len(idx)]][1] - pts[idx[(k + 1) % len(idx)]][0] * pts[idx[k]][1]
               for k in range(len(idx))) / 2.0
    reverse = area < 0
    order = list(reversed(idx)) if reverse else idx
    corner_set = set(keep)
    # the outline starts on a corner (a reversed outline started on a curve point, and Marvelous refused the piece)
    first = next(k for k, i in enumerate(order) if i in corner_set)
    order = order[first:] + order[:first]
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
    n = po["outlineLen"]
    lo, hi = min(i_from, i_to), max(i_from, i_to)
    if i_from % n not in cs or i_to % n not in cs:
        raise SystemExit("%s: %d or %d is not a corner" % (piece, i_from, i_to))
    # a stretch written to end at n (the outline's first point, reached the short way round) counts that point as n
    val = lambda c: n if (c == 0 and hi == n) else c  # noqa: E731
    k = len(cs)
    increasing = not po["reverse"]
    # a line between two corners inside the stretch, running the outline's own way (not the line that closes the
    # outline round its start: with only two corners, as on a pocket flap, both lines join the same pair)
    lines = [j for j in range(k) if lo <= val(cs[j]) <= hi and lo <= val(cs[(j + 1) % k]) <= hi
             and ((val(cs[j]) < val(cs[(j + 1) % k])) if increasing else (val(cs[j]) > val(cs[(j + 1) % k])))]
    rev = (i_from > i_to) if increasing else (i_from < i_to)
    if rev:
        lines = list(reversed(lines))
    if not lines:
        raise SystemExit("%s: no lines between %d and %d" % (piece, i_from, i_to))
    return lines, rev


def side(runs):
    out = []
    for r in runs:
        if "internal" in r:
            out.append({"piece": r["piece"], "internal": r["internal"]})
            continue
        ls, rev = lines_of(r["piece"], r["from"], r["to"])
        out.append({"piece": r["piece"], "lines": ls, "reversed": rev, "names": r["names"]})
    return out


seams_out = [[side(a), side(b)] for a, b in spec["seams"]]
inseams_out = [[side(a), side(b)] for a, b in spec.get("inseams", [])]
plan = {"pieces": pieces_out, "seams": seams_out, "inseams": inseams_out, "internals": spec.get("internals", []),
        "folds": spec["folds"], "pockets": spec["pockets"]}
OUTDIR = opt("--out", "", str)
job = '''# Generated by tools/md/make_jacket_job.py from %(spec)s: make the jacket's pieces in Marvelous Designer, draw the
# lines on them (roll lines, pocket mouths, the welt's edges, button tacks), and write out the pattern file and each
# piece's measured lines (to %(out)s) for tools/md/write_pattern.py to sew.
import json, os
PLAN = json.loads(%(plan)r)
OUT = %(out)r
utility_api.NewProject()
made = {}
for p in PLAN["pieces"]:
    pts = [(float(x), float(y), int(t)) for x, y, t in p["points"]]
    idx = pattern_api.CreatePatternWithPoints(pts)
    made[p["key"]] = idx
    try:
        pattern_api.SetPatternPieceName(idx, p["key"])
    except Exception as e:
        print("name", p["key"], e)
drawn = []
for il in PLAN["internals"]:
    pts = il["points"]
    q = [(float(x), float(y), 0 if k in (0, len(pts) - 1) else 2) for k, (x, y) in enumerate(pts)]
    drawn.append(pattern_api.CreateInternalShapeWithPoints(made[il["piece"]], q, False))
print("MADE", json.dumps(made))
print("DRAWN", drawn)
if OUT:
    os.makedirs(OUT, exist_ok=True)
    info = {key: json.loads(pattern_api.GetPatternLineInfo(idx)) for key, idx in made.items() if idx >= 0}
    json.dump({"made": made, "lineinfo": info}, open(os.path.join(OUT, "made.json"), "w"))
    pattern_api.ExportPatternJSON(os.path.join(OUT, "pieces.json"))
    print("WROTE", OUT)
''' % {"spec": SPEC, "plan": json.dumps(plan), "out": OUTDIR}
open(JOB, "w", encoding="utf-8").write(job)
json.dump(plan, open(JOB[:-3] + ".plan.json", "w", encoding="utf-8"))
print("job: %d pieces (%s points), %d seams, %d onto drawn lines -> %s" % (
    len(pieces_out), sum(len(p["points"]) for p in pieces_out), len(seams_out), len(inseams_out), JOB))
for p in pieces_out:
    print("  %-14s %3d points, %2d corners" % (p["key"], len(p["points"]), len(p["corners"])))
