"""The scale test's layout: where the street's copies stand on the Hook's road lines, and the walk along them (n16-3 step 2).

    python tools/scale_test_layout.py [--n 15] [--allow-outside] [--walk-slots K]   # writes production/specs/scale-test.json
    python tools/scale_test_layout.py --selftest

WHY, 16 November (production/research/street-scale-test/STEP2-DESIGN-2026-11-16.md,
"Layout: a new offline tool"; METHOD-NOTE-2026-11-16.md sections 1, 4 and 7):
the switch -ScaleTest=N measures what a district costs by standing N-1 copies of
the built 48 m street along the Hook's own road lines, and the day walk must run
along those copies (the review's first fix), not along the one street. Where the
copies stand is geometry, decided once offline and checked here, so the game only
reads a list of transforms and a polyline; nothing is placed by hand. A
measuring switch only: never shipped, never on his page.

WHAT IT READS: production/art/atlas-01/data/atlas.json: the Hook's polygon
(districts[id=hook]), the routes of kind main or minor (foot paths are not
road lines), and street_anchor's transform, east = 400 + z_m, north = 350 + x_m.

WHAT IT DOES, all in the street frame (x along the street, z across, yaw from
+x toward +z as vignette-scene.json's cameras):
  - each route segment (between two of its points) is cut where it crosses the
    Hook's edge, giving straight pieces inside and outside the Hook;
  - along each piece, from its end nearest the built street, straight slots of
    48 m (one street-length) with 2 m gaps; a slot never runs past its piece's
    ends, so it never crosses a corner; its footprint is 48 x 26.3 m (frontage
    to back of the built street) centred on the road line; a slot whose
    footprint touches an exclusion slides on along the piece in 0.5 m steps;
  - exclusions: the built street (x -2 to 50, |z| <= 14) and the approach
    (x 48 to 108.8, z -14 to 60);
  - slots are taken greedily by distance from the built street (inside the
    Hook first, then outside, only with --allow-outside): of every piece's next
    free slot the nearest is taken; a piece whose next slot would overlap an
    earlier slot (oriented-rectangle test) slides on along itself, so a corner
    shared by two roads costs one arm some metres, not its whole slot;
  - the first N-1 are written (N counts street-lengths: N-1 copies);
  - the walk: a polyline along the road centrelines that runs the whole length
    of every written slot and ends at cam_hook's spot (x -3.0, z -1.6), built
    backwards from cam_hook, nearest slot next, by shortest paths on the road
    graph; --walk-slots K walks only the K nearest slots (default: every
    written slot), since the Hook's slots fan out along four roads and a walk
    through all of them is long.

WHAT IT WRITES: production/specs/scale-test.json:
  {"about", "street_lengths", "copies", "capacity_in_hook", "slots": [{k, route,
  segment, x_m, z_m, yaw_deg, atlas: [e, n], in_hook, unit_shift}], "walk":
  [[x_m, z_m], ...], "walk_m"}. unit_shift k: copy k shows shop (u + k) mod 7's
  pictures (the design's -ScaleTest pictures rule).
"""
import heapq
import json
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(REPO, "production", "art", "atlas-01", "data", "atlas.json")
OUT = os.path.join(REPO, "production", "specs", "scale-test.json")

SLOT_L = 48.0               # one street-length (atlas street_anchor.length_m)
SLOT_W = 26.3               # frontage to back, centred on the road line (the design)
GAP = 2.0                   # between slots along one piece
SLIDE = 0.5                 # a blocked slot moves on this far
EPS = 1e-6
ROAD_KINDS = ("main", "minor")
CAM_HOOK = (-3.0, -1.6)     # vignette-scene.json cameras[cam_hook] x_m, z_m
# (x0, x1, z0, z1) in the street frame
EXCLUSIONS = (("built_street", -2.0, 50.0, -14.0, 14.0),
              ("approach", 48.0, 108.8, -14.0, 60.0))
BUILT = EXCLUSIONS[0]


# ---- frames -------------------------------------------------------------
def atlas_to_street(p, origin=(400.0, 350.0)):
    """[east, north] -> (x_m, z_m): east = 400 + z_m, north = 350 + x_m."""
    return (p[1] - origin[1], p[0] - origin[0])


def street_to_atlas(q, origin=(400.0, 350.0)):
    return [round(origin[0] + q[1], 3), round(origin[1] + q[0], 3)]


def yaw_of(d):
    """Street-frame yaw of direction (dx, dz): 0 faces +x, 90 faces +z."""
    y = math.degrees(math.atan2(d[1], d[0]))
    return y + 360.0 if y <= -180.0 else y


# ---- geometry -----------------------------------------------------------
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def rect_corners(c, yaw_deg, length, width):
    """Corners of a rectangle centred at c, long axis along yaw."""
    a = math.radians(yaw_deg)
    u = (math.cos(a), math.sin(a))
    v = (-u[1], u[0])
    hl, hw = length / 2.0, width / 2.0
    return [(c[0] + su * hl * u[0] + sv * hw * v[0], c[1] + su * hl * u[1] + sv * hw * v[1])
            for su, sv in ((1, 1), (1, -1), (-1, -1), (-1, 1))]


def box_corners(box):
    _, x0, x1, z0, z1 = box
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def rects_overlap(p, q):
    """Separating-axis test on two convex quads; touching counts as overlap
    (the slots must never touch an exclusion)."""
    for poly in (p, q):
        for i in range(4):
            e = sub(poly[(i + 1) % 4], poly[i])
            ax = (-e[1], e[0])
            n = math.hypot(*ax)
            if n < EPS:
                continue
            ax = (ax[0] / n, ax[1] / n)
            pp = [dot(ax, c) for c in p]
            qq = [dot(ax, c) for c in q]
            if max(pp) < min(qq) - EPS or max(qq) < min(pp) - EPS:
                return False
    return True


def point_in_poly(pt, poly):
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xc = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if xc > x:
                inside = not inside
    return inside


def seg_intersect_t(a, b, c, d):
    """Parameter t on a-b where it crosses c-d (proper or touching), or None."""
    r = sub(b, a)
    s = sub(d, c)
    den = r[0] * s[1] - r[1] * s[0]
    if abs(den) < EPS:
        return None
    w = sub(c, a)
    t = (w[0] * s[1] - w[1] * s[0]) / den
    u = (w[0] * r[1] - w[1] * r[0]) / den
    if -EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS:
        return min(1.0, max(0.0, t))
    return None


def split_by_poly(a, b, poly):
    """Pieces of a-b as (p, q, inside)."""
    ts = {0.0, 1.0}
    for i in range(len(poly)):
        t = seg_intersect_t(a, b, poly[i], poly[(i + 1) % len(poly)])
        if t is not None:
            ts.add(t)
    ts = sorted(ts)
    out = []
    for t0, t1 in zip(ts, ts[1:]):
        if (t1 - t0) * dist(a, b) < 1e-3:
            continue
        p, q = lerp(a, b, t0), lerp(a, b, t1)
        out.append((p, q, point_in_poly(lerp(a, b, (t0 + t1) / 2.0), poly)))
    # merge neighbours of equal state (a touch of the edge splits nothing)
    merged = []
    for piece in out:
        if merged and merged[-1][2] == piece[2] and dist(merged[-1][1], piece[0]) < 1e-6:
            merged[-1] = (merged[-1][0], piece[1], piece[2])
        else:
            merged.append(piece)
    return merged


def point_box_dist(p, box):
    _, x0, x1, z0, z1 = box
    dx = max(x0 - p[0], 0.0, p[0] - x1)
    dz = max(z0 - p[1], 0.0, p[1] - z1)
    return math.hypot(dx, dz)


def point_seg_dist(p, a, b):
    ab = sub(b, a)
    L2 = dot(ab, ab)
    t = 0.0 if L2 < EPS else max(0.0, min(1.0, dot(sub(p, a), ab) / L2))
    return dist(p, lerp(a, b, t))


# ---- the layout ---------------------------------------------------------
def pieces_of(routes, poly, allow_outside):
    """routes: [(id, [(x, z), ...])] -> [(route, segment index, p, q, inside)]."""
    out = []
    for rid, pts in routes:
        for i in range(len(pts) - 1):
            for p, q, inside in split_by_poly(pts[i], pts[i + 1], poly):
                if inside or allow_outside:
                    out.append((rid, i, p, q, inside))
    return out


def candidates_on(piece, exclusions):
    """A straight piece made ready for slots: its cursor at the end nearest
    the built street; None when it is shorter than one street-length."""
    rid, seg, p, q, inside = piece
    if point_box_dist(q, BUILT) < point_box_dist(p, BUILT):
        p, q = q, p
    L = dist(p, q)
    if L < SLOT_L - EPS:
        return None
    u = ((q[0] - p[0]) / L, (q[1] - p[1]) / L)
    yaw = yaw_of(u)
    ex = [box_corners(b) for b in exclusions]
    return {"route": rid, "segment": seg, "p": p, "q": q, "u": u, "L": L, "yaw": yaw,
            "in_hook": inside, "ex": ex, "s": 0.0}


def next_slot(st, blockers, s0=None):
    """The first slot on piece st at or past s0 (default its cursor) whose
    footprint is clear of the exclusions and of every blocker; None if the
    piece has no room left."""
    p, u, yaw = st["p"], st["u"], st["yaw"]
    s = st["s"] if s0 is None else s0
    while s + SLOT_L <= st["L"] + EPS:
        c = (p[0] + u[0] * (s + SLOT_L / 2.0), p[1] + u[1] * (s + SLOT_L / 2.0))
        fp = rect_corners(c, yaw, SLOT_L, SLOT_W)
        if any(rects_overlap(fp, e) for e in st["ex"]) or any(rects_overlap(fp, b) for b in blockers):
            s += SLIDE
            continue
        a = (p[0] + u[0] * s, p[1] + u[1] * s)
        b = (p[0] + u[0] * (s + SLOT_L), p[1] + u[1] * (s + SLOT_L))
        return {"route": st["route"], "segment": st["segment"], "c": c, "yaw": yaw, "a": a, "b": b,
                "fp": fp, "in_hook": st["in_hook"], "piece": (st["p"], st["q"]), "s": s,
                "d": point_box_dist(c, BUILT), "d0": dist(c, ((BUILT[1] + BUILT[2]) / 2.0, 0.0))}
    return None


def slot_key(s):
    return (not s["in_hook"], round(s["d"], 6), round(s["d0"], 6), s["route"], s["segment"], round(s["s"], 3))


def layout(routes, poly, exclusions=EXCLUSIONS, allow_outside=False):
    """Greedy by distance: of every piece's next free slot, take the one
    nearest the built street (inside the Hook first), move that piece's
    cursor 48 + 2 m on, and slide any piece whose next slot the new one
    overlaps. -> (slots in order, how many times a slot was slid past an
    earlier one)."""
    states = [s for s in (candidates_on(pc, exclusions) for pc in pieces_of(routes, poly, allow_outside)) if s]
    fps = []
    nxt = [next_slot(st, fps) for st in states]
    taken, slid = [], 0
    while True:
        live = [(slot_key(c), i) for i, c in enumerate(nxt) if c is not None]
        if not live:
            break
        _, i = min(live)
        c = nxt[i]
        taken.append(c)
        fps.append(c["fp"])
        states[i]["s"] = c["s"] + SLOT_L + GAP
        nxt[i] = next_slot(states[i], fps)
        for j, o in enumerate(nxt):
            if j != i and o is not None and rects_overlap(o["fp"], c["fp"]):
                slid += 1
                nxt[j] = next_slot(states[j], fps, o["s"])
    return taken, slid


# ---- the road graph and the walk ---------------------------------------
class Graph:
    def __init__(self):
        self.key = {}
        self.pts = []
        self.adj = []

    def node(self, p):
        k = (round(p[0], 3), round(p[1], 3))
        if k not in self.key:
            self.key[k] = len(self.pts)
            self.pts.append((k[0], k[1]))
            self.adj.append({})
        return self.key[k]

    def edge(self, i, j):
        if i == j:
            return
        w = dist(self.pts[i], self.pts[j])
        self.adj[i][j] = min(w, self.adj[i].get(j, w))
        self.adj[j][i] = self.adj[i][j]

    def path(self, i, j):
        best = {i: 0.0}
        prev = {}
        h = [(0.0, i)]
        while h:
            d, n = heapq.heappop(h)
            if n == j:
                break
            if d > best.get(n, 1e18):
                continue
            for m, w in self.adj[n].items():
                nd = d + w
                if nd < best.get(m, 1e18):
                    best[m] = nd
                    prev[m] = n
                    heapq.heappush(h, (nd, m))
        if j not in best:
            return None, None
        out = [j]
        while out[-1] != i:
            out.append(prev[out[-1]])
        return best[j], out[::-1]


def build_graph(routes, extra_points):
    """Road segments split at every route vertex, every crossing between
    segments and every extra point lying on a segment."""
    segs = []
    for rid, pts in routes:
        for i in range(len(pts) - 1):
            segs.append((pts[i], pts[i + 1]))
    g = Graph()
    for a, b in segs:
        ts = {0.0, 1.0}
        for c, d in segs:
            t = seg_intersect_t(a, b, c, d)
            if t is not None:
                ts.add(t)
        L = dist(a, b)
        for p in extra_points:
            if L > EPS and point_seg_dist(p, a, b) < 1e-3:
                ts.add(max(0.0, min(1.0, dot(sub(p, a), sub(b, a)) / (L * L))))
        ts = sorted(ts)
        nodes = [g.node(lerp(a, b, t)) for t in ts]
        for i, j in zip(nodes, nodes[1:]):
            g.edge(i, j)
    return g


def nearest_on_roads(p, routes):
    best = (1e18, None)
    for rid, pts in routes:
        for a, b in zip(pts, pts[1:]):
            ab = sub(b, a)
            L2 = dot(ab, ab)
            t = 0.0 if L2 < EPS else max(0.0, min(1.0, dot(sub(p, a), ab) / L2))
            q = lerp(a, b, t)
            if dist(p, q) < best[0]:
                best = (dist(p, q), q)
    return best[1]


def simplify(pl):
    out = []
    for p in pl:
        p = (round(p[0], 3), round(p[1], 3))
        if out and dist(out[-1], p) < 1e-3:
            continue
        out.append(p)
    i = 1
    while i < len(out) - 1:
        a, b, c = out[i - 1], out[i], out[i + 1]
        cr = (b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])
        if abs(cr) < 1e-6 and dot(sub(b, a), sub(c, b)) > 0:
            out.pop(i)
        else:
            i += 1
    return out


def make_walk(routes, slots, end=CAM_HOOK):
    """Backwards from cam_hook: nearest unvisited slot by road distance, its
    whole length, and so on; then reversed so the walk ends at cam_hook."""
    foot = nearest_on_roads(end, routes)
    extra = [foot] + [s["a"] for s in slots] + [s["b"] for s in slots]
    g = build_graph(routes, extra)
    cur = g.node(foot)
    rev = [end, g.pts[cur]]
    todo = list(range(len(slots)))
    while todo:
        best = None
        for si in todo:
            for near, far in ((slots[si]["a"], slots[si]["b"]), (slots[si]["b"], slots[si]["a"])):
                d, p = g.path(cur, g.node(near))
                if d is not None and (best is None or d < best[0]):
                    best = (d, p, si, far)
        if best is None:
            raise ValueError("a slot is not reachable on the road graph")
        d, p, si, far = best
        rev += [g.pts[n] for n in p]
        d2, p2 = g.path(p[-1], g.node(far))
        rev += [g.pts[n] for n in p2]
        cur = g.node(far)
        todo.remove(si)
    walk = simplify(rev[::-1])
    length = sum(dist(a, b) for a, b in zip(walk, walk[1:]))
    return walk, length


# ---- reading the atlas --------------------------------------------------
def read_atlas(path=ATLAS):
    a = json.load(open(path, encoding="utf-8"))
    anchor = a["street_anchor"]
    origin = tuple(anchor["origin_atlas"])
    if anchor.get("source_to_atlas", "").replace(" ", "").find("east=400+z_m;north=350+x_m") < 0 or origin != (400, 350):
        raise ValueError("street_anchor's transform is not east=400+z_m, north=350+x_m: " + anchor.get("source_to_atlas", ""))
    hook = [d for d in a["districts"] if d["id"] == "hook"][0]
    poly = [atlas_to_street(p) for p in hook["polygon"]]
    routes = [(r["id"], [atlas_to_street(p) for p in r["points"]]) for r in a["routes"] if r["kind"] in ROAD_KINDS]
    return routes, poly


def slot_record(k, s):
    return {"k": k, "route": s["route"], "segment": s["segment"],
            "x_m": round(s["c"][0], 3), "z_m": round(s["c"][1], 3),
            "yaw_deg": round(s["yaw"], 3), "atlas": street_to_atlas(s["c"]),
            "in_hook": s["in_hook"], "unit_shift": k}


def run(n, allow_outside, write=True, walk_slots=None):
    routes, poly = read_atlas()
    inside, dropped_in = layout(routes, poly, allow_outside=False)
    slots, dropped = (layout(routes, poly, allow_outside=True) if allow_outside else (inside, dropped_in))
    need = max(0, n - 1)
    used = slots[:need]
    walked = used if walk_slots is None else used[:walk_slots]
    walk, walk_m = make_walk(routes, walked)
    off = 0.0
    for a, b in zip(walk, walk[1:]):
        if not point_in_poly(lerp(a, b, 0.5), poly):
            off += dist(a, b)
    doc = {
        "about": ("The scale test's layout (n16-3 step 2), written by tools/scale_test_layout.py from "
                  "production/art/atlas-01/data/atlas.json; do not edit by hand. A measuring switch only "
                  "(-ScaleTest=N), never shipped. Street frame: x along the street, z across, yaw_deg from +x "
                  "toward +z (vignette-scene.json's cameras); atlas = [400 + z_m, 350 + x_m]. Each slot is one "
                  "copy of the built street, 48 x 26.3 m centred on a main or minor road line, straight, never "
                  "over the built street (x -2 to 50, |z| <= 14) or the approach (x 48 to 108.8, z -14 to 60), "
                  "ordered by distance from the built street, inside the Hook first; in_hook false only with "
                  "--allow-outside. unit_shift k: copy k shows shop (u + k) mod 7's pictures. walk: road "
                  "centrelines through every slot's whole length, ending at cam_hook's spot; walk_m its length."),
        "street_lengths": n,
        "copies": len(used),
        "copies_wanted": need,
        "capacity_in_hook": len(inside),
        "allow_outside": allow_outside,
        "slid_past_slots": dropped,
        "slots": [slot_record(k, s) for k, s in enumerate(used, 1)],
        "walk": [[round(p[0], 3), round(p[1], 3)] for p in walk],
        "walk_m": round(walk_m, 2),
        "walk_slots": len(walked),
        "walk_m_outside_hook": round(off, 2),
    }
    if write:
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(doc, f, indent=1)
            f.write("\n")
    return doc, inside, slots


# ---- selftest -----------------------------------------------------------
def selftest():
    ok = bad = 0

    def check(cond, what):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("scale_test_layout selftest FAIL " + what)

    # 1. the overlap test on known rectangles
    A = rect_corners((0, 0), 0, 10, 4)
    check(rects_overlap(A, rect_corners((9, 0), 0, 10, 4)), "overlapping boxes read apart")
    check(not rects_overlap(A, rect_corners((10.5, 0), 0, 10, 4)), "separate boxes read overlapping")
    check(rects_overlap(A, rect_corners((10, 0), 0, 10, 4)), "touching boxes must count as touching")
    # rotated: bounding boxes overlap, the rectangles do not
    B = rect_corners((0, 0), 45, 10, 1)
    C = rect_corners((3.2, -3.2), 45, 10, 1)
    check(not rects_overlap(B, C), "parallel diagonal strips 4.5 m apart read overlapping")
    check(rects_overlap(B, rect_corners((0, 0), -45, 10, 1)), "a crossing X reads apart")
    check(rects_overlap(rect_corners((0, 0), 0, 2, 2), rect_corners((0, 0), 30, 20, 20)), "contained box reads apart")
    check(rects_overlap(rect_corners((0, 0), 0, 10, 10), rect_corners((7.0, 0), 45, 4, 4)), "rotated square into a box reads apart")
    check(not rects_overlap(rect_corners((0, 0), 0, 10, 10), rect_corners((7.9, 0), 45, 4, 4)), "rotated square clear of a box reads overlapping")

    # 2. a synthetic map: an L road with a corner, a diagonal, an exclusion
    big = [(-1000, -1000), (1000, -1000), (1000, 1000), (-1000, 1000)]
    routes = [("L", [(-300.0, 0.0), (-60.0, 0.0), (-60.0, 200.0)]),
              ("diag", [(100.0, 100.0), (250.0, 250.0)]),
              ("short", [(0.0, -100.0), (40.0, -100.0)])]
    ex = (("built_street", -2.0, 50.0, -14.0, 14.0), ("blk", -200.0, -150.0, -20.0, 20.0))
    slots, dropped = layout(routes, big, exclusions=ex)
    check(len(slots) > 4, "synthetic layout found %d slots" % len(slots))
    check(not any(s["route"] == "short" for s in slots), "a 40 m road took a 48 m slot")
    for s in slots:
        for e in ex:
            check(not rects_overlap(s["fp"], box_corners(e)), "slot %s touches %s" % (s["c"], e[0]))
        dmin = min(point_seg_dist(s["c"], a, b) for _, pts in routes for a, b in zip(pts, pts[1:]))
        check(dmin <= 0.5, "slot centre %.2f m off the road" % dmin)
        p, q = s["piece"]
        check(point_seg_dist(s["a"], p, q) < 1e-6 and point_seg_dist(s["b"], p, q) < 1e-6,
              "slot ends leave their straight piece (corner crossed)")
        check(abs(dist(s["a"], s["b"]) - SLOT_L) < 1e-6, "slot not 48 m")
    # the corner at (-60, 0): no slot centreline passes through it
    for s in slots:
        if s["route"] == "L":
            check(point_seg_dist((-60.0, 0.0), s["a"], s["b"]) > 1e-6 or
                  dist(s["a"], (-60.0, 0.0)) < 1e-6 or dist(s["b"], (-60.0, 0.0)) < 1e-6,
                  "a slot crosses the L's corner")
    for i, s in enumerate(slots):
        for t in slots[:i]:
            check(not rects_overlap(s["fp"], t["fp"]), "two slots overlap")
    check(dropped >= 1, "the corner's two arms should slide at least one slot past the other (slid %d)" % dropped)
    ds = [s["d"] for s in slots]
    check(ds == sorted(ds), "slots not ordered by distance from the built street")
    # clipping: a polygon covering half the L's long arm
    half = [(-200.0, -50.0), (0.0, -50.0), (0.0, 50.0), (-200.0, 50.0)]
    pcs = split_by_poly((-300.0, 0.0), (-60.0, 0.0), half)
    check([round(p[0][0], 3) for p in pcs] == [-300.0, -200.0] and [x[2] for x in pcs] == [False, True],
          "clipping a segment to a polygon: %s" % pcs)
    sin, _ = layout(routes, half, exclusions=ex)
    check(all(-200.0 - EPS <= min(s["a"][0], s["b"][0]) and max(s["a"][0], s["b"][0]) <= 0.0 + EPS for s in sin),
          "a slot left the clipping polygon")
    sout, _ = layout(routes, half, exclusions=ex, allow_outside=True)
    check(any(not s["in_hook"] for s in sout) and not any(not s["in_hook"] for s in sin),
          "outside slots only with allow_outside")
    flags = [s["in_hook"] for s in sout]
    check(flags == sorted(flags, reverse=True), "inside slots must come before outside ones")
    # the synthetic walk
    lslots = [s for s in slots if s["route"] == "L"]   # the only road joined to the end's
    walk, wl = make_walk(routes, lslots, end=(-60.0, -1.6))
    check(len(lslots) >= 2 and wl >= SLOT_L * len(lslots) - EPS, "synthetic walk %.1f m shorter than its slots" % wl)
    check(dist(walk[-1], (-60.0, -1.6)) < 1e-6, "synthetic walk does not end at its end spot")
    for s in lslots:
        check(all(min(point_seg_dist(lerp(s["a"], s["b"], t / 8.0), a, b) for a, b in zip(walk, walk[1:])) < 0.01
                  for t in range(9)), "synthetic walk misses a slot")

    # 3. the real atlas
    routes, poly = read_atlas()
    inside, dropped_in = layout(routes, poly)
    allslots, _ = layout(routes, poly, allow_outside=True)
    cap_out = len(allslots)
    parts = []
    for n in (2, 4, 10, 15):
        need = n - 1
        if need <= len(inside):
            parts.append("N=%d needs %d: ok in the Hook" % (n, need))
        elif need <= cap_out:
            parts.append("N=%d needs %d: short by %d in the Hook, ok with --allow-outside" % (n, need, need - len(inside)))
        else:
            parts.append("N=%d needs %d: short by %d even outside" % (n, need, need - cap_out))
    print("capacity: %d slots inside the Hook (%d slides past an earlier slot), %d with --allow-outside; %s"
          % (len(inside), dropped_in, cap_out, "; ".join(parts)))
    check(len(inside) >= 1, "no slot inside the Hook")
    for s in allslots:
        for e in EXCLUSIONS:
            check(not rects_overlap(s["fp"], box_corners(e)), "real slot %s touches %s" % (s["c"], e[0]))
        dmin = min(point_seg_dist(s["c"], a, b) for _, pts in routes for a, b in zip(pts, pts[1:]))
        check(dmin <= 0.5, "real slot centre %.2f m off the road" % dmin)
    for s in inside:
        check(all(point_in_poly(lerp(s["a"], s["b"], t / 10.0), poly) or
                  min(point_seg_dist(lerp(s["a"], s["b"], t / 10.0), poly[i], poly[(i + 1) % len(poly)])
                      for i in range(len(poly))) < 1e-3 for t in range(11)),
              "an in-Hook slot's centreline leaves the Hook")
    for n, outside in ((10, False), (15, True)):
        use = (allslots if outside else inside)[:n - 1]
        walk, wl = make_walk(routes, use)
        segs_ok = True
        for i, (a, b) in enumerate(zip(walk, walk[1:])):
            if i == len(walk) - 2:
                continue   # the last step leaves the centreline for cam_hook's spot
            for t in (0.0, 0.25, 0.5, 0.75, 1.0):
                pnt = lerp(a, b, t)
                if min(point_seg_dist(pnt, c, d) for _, pts in routes for c, d in zip(pts, pts[1:])) > 0.01:
                    segs_ok = False
        check(segs_ok, "N=%d walk leaves the road lines" % n)
        check(dist(walk[-1], CAM_HOOK) < 1e-6, "N=%d walk does not end at cam_hook" % n)
        check(dist(walk[-2], walk[-1]) < 2.0, "N=%d walk's last step off the road is %.2f m" % (n, dist(walk[-2], walk[-1])))
        for s in use:
            covered = all(min(point_seg_dist(lerp(s["a"], s["b"], t / 8.0), a, b) for a, b in zip(walk, walk[1:])) < 0.01
                          for t in range(9))
            check(covered, "N=%d walk misses part of slot at %s" % (n, s["c"]))
        print("walk N=%d%s: %d points, %.1f m, continuous on the road lines: %s"
              % (n, " (with outside)" if outside else "", len(walk), wl, "yes" if segs_ok else "NO"))
    print("scale_test_layout selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    n = 15
    if "--n" in argv:
        n = int(argv[argv.index("--n") + 1])
    allow = "--allow-outside" in argv
    ws = int(argv[argv.index("--walk-slots") + 1]) if "--walk-slots" in argv else None
    doc, inside, slots = run(n, allow, walk_slots=ws)
    print("scale-test.json: N=%d street-lengths, %d copies wanted, %d written (%d in the Hook), "
          "capacity in the Hook %d%s; walk through %d slots, %d points, %.1f m (%.1f m outside the Hook)"
          % (n, doc["copies_wanted"], doc["copies"], sum(1 for s in doc["slots"] if s["in_hook"]),
             doc["capacity_in_hook"], ", outside allowed" if allow else "", doc["walk_slots"], len(doc["walk"]),
             doc["walk_m"], doc["walk_m_outside_hook"]))
    if doc["copies"] < doc["copies_wanted"]:
        print("SHORT: %d copies have no slot%s" % (doc["copies_wanted"] - doc["copies"],
                                                    "" if allow else " (try --allow-outside)"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
