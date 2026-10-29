#!/usr/bin/env python3
"""A jacket's rib cuffs built round the wrist's own shape, in place of the cloth simulator's (his order C9: the bake
route he picked on his page of 28 October, after Marvelous's elastic rib failed twice on 29 October).

    python tools/md/build_cuffs.py DRAPE_UNPOSED.obj OUT.obj [--clear 4.5] [--height 60] [--blend 0.3]
        [--edge-at-hand [--edge-past 0] [--reach 60] [--joints J.json]]
    python tools/md/build_cuffs.py --selftest

WHY. Marvelous's cuffs met every mark but the gap: a single-layer rib band with two free edges bulged or rolled on
the wrist (13.1, 12.4 and 12.5 mm off it against 10.5; one rolled to 83% cover: DECISIONS.md, 29 October 11:57).
The method (production/research/game-clothing-pipeline/SLEEVE-END-2026-10-28.md, option 1): the sleeve kept where it
is round, a rib band made round the wrist's own shape and joined to that round end, skinned to hand and forearm.

HOW. The drape bent back to his pose (tools/md/unpose_garment.py) holds each cuff as Marvelous made it: a grid whose
UVs are its pattern (u round the wrist, v its height) and whose sewn top edge lies on the sleeve's end. Only the
cuff's vertices move, so its faces, UVs, seam and every later step of the bake chain stay as they are:
- the seam edge (the cuff edge lying on the sleeve, found by distance) is kept exactly where the drape put it;
- each vertex keeps its column's angle round the forearm's axis (the seam vertex at the same u) and goes down the arm
  from the seam by its share of the band's height (--height mm, the pattern's own 60);
- its distance from the axis is the skin's there (tools/md-bridge/cuff_measure.py's skin_radius, the farthest skin
  in a 30 degree wedge, so the band bridges the hollows between tendons as a tape does) plus --clear mm (the skin
  offset 3 and half the rib's thickness), eased from the seam's own radius over the first --blend of the height;
- the two side edges, sewn together, take the same place, so the seam stays shut.
The result is checked with the same tools as every drape (cuff_measure.py, sleeve_wrap.py, cuff_faults.py).
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "md-bridge"))
import cuff_measure as cm  # noqa: E402

JOINTS = "F:/LedgerTools/bodies/MH_TomL1/joints-md-mm.json"


def read_obj(path):
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    V, T, groups, cur = [], [], {}, None
    for line in lines:
        if line.startswith("v "):
            V.append([float(x) for x in line.split()[1:4]])
        elif line.startswith("vt "):
            T.append([float(x) for x in line.split()[1:3]])
        elif line.startswith("g "):
            cur = line[2:].strip()
            groups.setdefault(cur, set())
        elif line.startswith("f ") and cur:
            for t in line.split()[1:]:
                a = t.split("/")
                groups[cur].add((int(a[0]) - 1, int(a[1]) - 1 if len(a) > 1 and a[1] else -1))
    return lines, np.array(V), np.array(T) if T else np.zeros((0, 2)), groups


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def cut_sleeve(V, groups, piece, f, seam_xyz, s_top, reach):
    """THE SLEEVE CUT WHERE IT IS ROUND (the method's first step): the sleeve's last `reach` mm drawn up so its end, the
    cuff's seam, lies square to the forearm at s_top; each sleeve point keeps its angle and distance from the axis and
    only its place along the arm is scaled, so the sleeve blouses a little over the cuff as a gathered end does.
    Returns {vertex index: xyz} for the sleeve and the seam's new points."""
    rel = seam_xyz - f["centre"]
    s_seam = rel @ f["axis"]
    a_seam = np.arctan2(rel @ f["w"], rel @ f["u"])
    o = np.argsort(a_seam)
    a_sorted, s_sorted = a_seam[o], s_seam[o]
    a_ext = np.r_[a_sorted[-1] - 2 * math.pi, a_sorted, a_sorted[0] + 2 * math.pi]
    s_ext = np.r_[s_sorted[-1], s_sorted, s_sorted[0]]
    out = {}
    for idx in sorted({v for v, _ in groups["sleeve" + piece[-1]]}):
        r = V[idx] - f["centre"]
        s = float(r @ f["axis"])
        end = float(np.interp(math.atan2(float(r @ f["w"]), float(r @ f["u"])), a_ext, s_ext))
        start = end - reach
        if s <= start:
            continue
        s2 = start + (s - start) * (s_top - start) / (end - start)
        out[int(idx)] = V[idx] + f["axis"] * (s2 - s)
    return out


def build(V, T, groups, piece, side, clear, height, blend, top=None, reach=60.0):
    """New positions for one cuff's vertices (and, with top, the sleeve's end): {vertex index: xyz}."""
    body = V[sorted({v for v, _ in groups[next(k for k in groups if k.endswith("LOD0"))]})]
    f = cm.forearm(body, side)
    sleeve = V[sorted({v for v, _ in groups["sleeve" + piece[-1]]})]
    pairs = sorted(groups[piece])
    vi = np.array([p[0] for p in pairs])
    uv = T[np.array([p[1] for p in pairs])]
    P = V[vi]
    w0, w1 = uv[:, 1].min(), uv[:, 1].max()
    span_v = w1 - w0
    u0, u1 = uv[:, 0].min(), uv[:, 0].max()
    edge = {w: np.abs(uv[:, 1] - w) < span_v * 0.01 for w in (w0, w1)}
    # the seam edge: the one lying on the sleeve's end
    def off_sleeve(m):
        d = np.sqrt(((P[m][:, None, :] - sleeve[None, :, :]) ** 2).sum(axis=2)).min(axis=1)
        return float(np.median(d))
    w_seam = min(edge, key=lambda w: off_sleeve(edge[w]))
    seam = edge[w_seam]
    seam_off = off_sleeve(seam)
    moved = {}
    if top is not None:
        s_top = top(f)
        moved.update(cut_sleeve(V, groups, piece, f, P[seam], s_top, reach))
        for k in np.where(seam)[0]:
            P[k] = P[k] + f["axis"] * (s_top - float((P[k] - f["centre"]) @ f["axis"]))
            moved[int(vi[k])] = P[k].copy()
    rel = lambda p: p - f["centre"]  # noqa: E731
    def polar(p):
        r = rel(p)
        return float(r @ f["axis"]), math.atan2(float(r @ f["w"]), float(r @ f["u"])), math.hypot(float(r @ f["u"]), float(r @ f["w"]))
    # the seam edge as a function of u: along, angle (unwrapped), radius
    su = uv[seam, 0]
    o = np.argsort(su)
    sp = [polar(p) for p in P[seam][o]]
    s_s = np.array([q[0] for q in sp])
    a_s = np.unwrap(np.array([q[1] for q in sp]))
    r_s = np.array([q[2] for q in sp])
    su = su[o]
    toward_hand = 1.0                        # the axis points toward the hand (cuff_measure.forearm)
    out = {}
    for k, idx in enumerate(vi):
        if seam[k]:
            continue
        u, w = uv[k]
        t = abs(w - w_seam) / span_v          # 0 at the seam, 1 at the free edge
        s0 = float(np.interp(u, su, s_s))
        ang = float(np.interp(u, su, a_s))
        r0 = float(np.interp(u, su, r_s))
        s = s0 + toward_hand * t * height
        skin = cm.skin_radius(f["arm"], f, s, math.atan2(math.sin(ang), math.cos(ang)))
        if math.isnan(skin):
            skin = r0 - clear
        r = r0 + (skin + clear - r0) * float(smoothstep(t / blend))
        out[int(idx)] = (f["centre"] + f["axis"] * s + (f["u"] * math.cos(ang) + f["w"] * math.sin(ang)) * r)
    # the side seam: the two side edges (u at either end) are sewn, so each pair takes one place
    left = np.abs(uv[:, 0] - u0) < (u1 - u0) * 0.004
    right = np.abs(uv[:, 0] - u1) < (u1 - u0) * 0.004
    for k in np.where(left)[0]:
        j = np.where(right)[0][np.argmin(np.abs(uv[right, 1] - uv[k, 1]))]
        a, b = int(vi[k]), int(vi[j])
        pa, pb = out.get(a, V[a]), out.get(b, V[b])
        m = (np.asarray(pa) + np.asarray(pb)) / 2.0
        if a in out or b in out:
            out[a] = out[b] = m
    moved.update(out)
    info = {"wristGirthMm": round(f["girth"], 1), "seamEdgeOffSleeveMm": round(seam_off, 2), "moved": len(moved)}
    if top is not None:
        info["seamAtMmPastWrist"] = round(s_top, 1)
    return moved, info


def write(lines, V, moved, path):
    vi = -1
    with open(path, "w", encoding="utf-8") as fo:
        for line in lines:
            if line.startswith("v "):
                vi += 1
                if vi in moved:
                    p = moved[vi]
                    line = "v %.4f %.4f %.4f" % (p[0], p[1], p[2])
            fo.write(line + "\n")


def selftest():
    ok = [abs(float(smoothstep(0.5)) - 0.5) < 1e-9, float(smoothstep(2.0)) == 1.0, float(smoothstep(-1.0)) == 0.0]
    print("build_cuffs selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


def main(a):
    if "--selftest" in a:
        return selftest()
    opt = lambda n, d: float(a[a.index(n) + 1]) if n in a else d  # noqa: E731
    src, dst = a[0], a[1]
    lines, V, T, groups = read_obj(src)
    height = opt("--height", 60.0)
    # --edge-at-hand (the cuff's place, reference first): Mafia's tailored sleeve ends in a lip 1.5 to 1.7 cm past the
    # hand joint (production/research/game-clothing-pipeline/MAFIA-JACKET-2026-10-28.md, section 2); a rib cuff grips
    # rather than hangs, so its lower edge goes at the hand joint itself (ours), plus --edge-past mm, and its top, the
    # sleeve's cut end, the band's height above that, square to the forearm
    joints = json.load(open(a[a.index("--joints") + 1] if "--joints" in a else JOINTS, encoding="utf-8"))
    past = opt("--edge-past", 0.0)
    moved = {}
    for piece, side in (("cuffL", 1.0), ("cuffR", -1.0)):
        hand = np.array(joints["hand_" + ("l" if side > 0 else "r")])
        top = (lambda f, hand=hand: float((hand - f["centre"]) @ f["axis"]) + past - height) if "--edge-at-hand" in a else None
        m, info = build(V, T, groups, piece, side, opt("--clear", 4.5), height, opt("--blend", 0.3), top, opt("--reach", 60.0))
        moved.update(m)
        print("built", piece, info)
    write(lines, V, moved, dst)
    print("wrote", dst, "moved", len(moved), "vertices")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
