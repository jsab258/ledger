#!/usr/bin/env python3
"""Sheila's brown pleated skirt, knee length, as one job for Kiln (run_job_script.py) or Marvelous (md_job.py): a
hip yoke front and back cut from GarmentCode's fitted skirt at her measures, a waistband in two halves, and below the
yoke two straight panels laid in knife pleats, placed on the body's waist and skirt points by name, sewn, draped and
exported.

    python tools/md-bridge/pleated_skirt.py --draft DRAFT.json [--meas MEAS.json]     # the yoke, from GarmentCode
    python tools/md-bridge/pleated_skirt.py DRAFT.json JOB.py [--out DIR] [--avatar BODY] [--steps 400]
        [--pleats 8] [--length MM] [--pleat-particle 6]
    python F:/LedgerTools/tool-dev/kiln/python/run_job_script.py JOB.py RESULT.json     # Kiln
    python tools/md-bridge/md_job.py JOB.py                                              # Marvelous (an .avt needed)
    python tools/md-bridge/pleated_skirt.py --selftest

WHY, 16 November 2026 (his decision: the practice garments' patterns from our own pattern tools, FreeSewing and
GarmentCode, straight into Kiln's job format; production/art/clothing/BREADTH-PATTERNS-2026-11-16.md, section 3).
The note's pick for the yoke, FreeSewing's Penelope, is not installed here (F:/LedgerTools/freesewing has bent,
brian, charlie, florent, jaeger, simon, titan) and nothing was downloaded; so the yoke comes from the other
allowlisted tool on this machine, GarmentCode 2.0.2 (MIT, F:/LedgerTools/garmentcode-lab, the n09-6 lab): its
PencilSkirt's fitted front and back (FittedSkirtPanel: the waist-to-hip difference shared between the side curve and
waist darts, two in front, four behind, the back's hip depth 1.05 of the front's) drafted at her measures and cut at
the hip line. --draft runs that under the lab's own Python and writes the draft in the FreeSewing drafter's shape
(parts, each a seam outline and named points, mm, y down) with her "measurements" block, so the job reads it exactly
as work_trousers.py reads its Titan draft (zip_jacket.load, measures()).

THE MEASURES: S4's own set, F:/LedgerTools/garments/sheila/step0-2026-11-11/meas_S4.json (waist 813.9, seat 920.4,
waist to seat 150, waist to knee 544); bodies/MH_LenaS4/measurements.json holds Lena C1's numbers and is not used
(the note, "Measurement files disagree"). GarmentCode drafts without ease, so the ease is put into the girths it is
given (WAIST_EASE, SEAT_EASE: guesses, Penelope's own defaults unread). Its back widths are S4's waistBack and
seatBack with the same ease; its dart places (bum_points, bust_points) and hip inclination are its mean woman's,
not measured on S4.

THE PIECES (six): yokeFront, yokeBack (each whole, darts sewn shut, side seams sewn; the zip drawn closed, so the
skirt is a closed ring), bandFront, bandBack (BAND_H deep, cut to the yoke's waist edge, closed at the sides),
pleatsFront, pleatsBack (straight panels, PLEATS knife pleats each, all turned the same way round the body, sewn to
the yoke's hip edge and to each other at the sides). The hem is level with the knee plus KNEE_BELOW at the centre
front (--length). Each panel's visible face matches its yoke's hip edge; the pleats take PLEAT_TAKE more cloth (the
note's "hem about 1.5 times the seat", a guess), so each pleat is s visible and 2d folded under, d = s * PLEAT_TAKE / 2.

THE PLEATS, AS THE JOB FORMAT ALLOWS THEM. Each knife pleat is three points on the panel's top edge: its outer fold F,
its inner fold B a depth d further on, and its placement line P a depth d beyond B (P lies under F once folded). The
top edge is cut into lines at every F, B and P, so (1) each visible stretch P to F is sewn to its own stretch of the
yoke's hip edge, and (2) each pleat is tacked shut at the top by sewing B-F to B-P (F meets P, the fold held where
the yoke catches it, as a real pleat is caught in the yoke seam). Down the panel, each F and B is an internal line
(CreateInternalShapeWithPoints) given a fold (SetInternalLineFold: FOLD_ANGLE, FOLD_STRENGTH, +F and -B).

WHAT KILN CANNOT YET DO FOR THIS SKIRT (production/research/tool-tests-2026-11/KILN-PARITY-LIST-2026-11-16.md):
  * No pleat pressing and no pleat tacking down the length: nothing holds a pleat closed below the yoke seam. The
    fold lines only give the cloth a rest angle along them (sim.rs, "Fold lines"), with the fold's own stiffness; a
    pressed pleat's set crease and an edge-stitched pleat are not there, so the pleats will open towards the hem
    more than pressed wool would.
  * The fold's sign is not used: Kiln's rest length across a fold uses cos(angle), so +F and -B fold alike; which
    way each pleat turns comes only from the tack at the top. Marvelous's angle convention for this call is
    unverified (its help pages answered 403 to the note).
  * A fold line acts only where the mesh's edges lie along it (within 0.45 of the particle distance): with d about
    14 mm the panels are meshed at --pleat-particle (6 mm) in the fine stage; whether the mesh follows the lines is
    unverified until a run.
  * No drape in a sitting pose (the parity list: poses tested on refits only; no seated pose file found, the note):
    the job drapes standing only. The sitting test that set the Blender skirt aside is not part of this job.
  * Its long loose part (the pleated hem) handed to Unreal's cloth: not built (M6).
On Marvelous the pleats would normally be made with its Pleats Fold / Pleats Sewing tools, which the bridge's API was
not found to reach (the note); the same internal-line route is written for both.

EVERY EDGE IS NAMED BY ITS TWO ENDS and a seam pairs two edges by those names (zip_jacket.py's rule). Sides are named
by the wearer: the front and its band and panel are placed from the front (their +x the wearer's left), the back
pieces from behind (+x the wearer's right), as zip_jacket.py places them. Nothing in this file is a measure of one
body: every length and girth comes from the draft and its own "measurements".

THE CLOTH (its physics only): on Marvelous its stock flannel (as work_trousers.py; a woven wool-type cloth, whether
its physics is wool's is unverified), the band its canvas; on Kiln our own descriptions beside the job
(<name>.drape-fabric.json, read by Kiln's fabric_for_file). ESTIMATES (SKIRT_CLOTH, BAND_CLOTH below).
"""
import json
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zip_jacket import CORNER, CURVE, area, ccw, edges_from, idx_of, length, load  # noqa: E402

sys.path.insert(0, "F:/LedgerTools/tool-dev")
from outpath import checked  # noqa: E402

MEAS = r"F:\LedgerTools\garments\sheila\step0-2026-11-11\meas_S4.json"
OUT_DIR = r"F:\LedgerTools\garments\sheila\kiln-breadth-2026-11-16"
DRAFT = os.path.join(OUT_DIR, "gc-yoke-sheila.json")
BODY = r"F:\LedgerTools\bodies\MH_LenaS4\MH_LenaS4_FullBody.fbx"
GC_LAB = r"F:\LedgerTools\garmentcode-lab\lab"
GC_PY = r"F:\LedgerTools\garmentcode-lab\venv\Scripts\python.exe"

WAIST_EASE, SEAT_EASE = 0.015, 0.05   # guesses: about 12 mm at her waist, 46 mm at her seat
BACK_HIP_EXT = 1.05                   # GarmentCode's back hip depth against the front's (FittedSkirtPanel, hipline_ext)
KNEE_BELOW = 40.0                     # mm the hem falls below the knee's line at the centre front (a guess)
PLEATS = 8                            # knife pleats per panel: 16 round, the Blender skirt's count (sheila/README.md)
PLEAT_TAKE = 0.5                      # cloth folded under against the visible width (the note's 1.5 x, a guess)
BAND_H = 30.0                         # mm
BAND_OF_WAIST = 1.0                   # a skirt band sewn flat to the yoke's eased waist
FOLD_ANGLE, FOLD_STRENGTH = 160.0, 80.0   # degrees from flat (Kiln: 0 flat, 180 folded double), 0..100
PLEAT_PARTICLE = 6.0                  # mm on the pleated panels in the fine stage
ARRANGE = {"yokeFront": "Body_Front_Waist", "yokeBack": "Body_Back_Waist", "bandFront": "Body_Front_Waist",
           "bandBack": "Body_Back_Waist", "pleatsFront": "Leg_Skirt_Front", "pleatsBack": "Leg_Skirt_Back"}
ORDER = ["yokeFront", "yokeBack", "bandFront", "bandBack", "pleatsFront", "pleatsBack"]
# THE FABRICS, Kiln's units (doc.rs, struct Fabric). ESTIMATES, none measured: a skirt-weight wool flannel about
# 280 g/m2, softer than the trousers' twill (88/90/70/45/48, 340); the band the same cloth over an interlining, nearer
# Kiln's Stiff Interlining. The names avoid "wool" (Kiln's fallback preset by that name is a sweater knit).
SKIRT_CLOTH = {"name": "sheila_skirt_flannel", "color": [92, 64, 44], "stretch_weft": 85.0, "stretch_warp": 88.0,
               "shear": 65.0, "bending_weft": 35.0, "bending_warp": 38.0, "density": 280.0, "friction": 40.0,
               "thickness": 0.7, "damping": 12.0}
BAND_CLOTH = {"name": "sheila_skirt_band", "color": [92, 64, 44], "stretch_weft": 95.0, "stretch_warp": 95.0,
              "shear": 88.0, "bending_weft": 80.0, "bending_warp": 80.0, "density": 400.0, "friction": 40.0,
              "thickness": 1.2, "damping": 12.0}
FABRICS = {"skirt": {"md": "V2_Woven_Flannel_1.zfab", "kiln": SKIRT_CLOTH},
           "band": {"md": "V2_Woven_Canvas_1.zfab", "kiln": BAND_CLOTH}}
ESTIMATE_NOTE = ("ESTIMATES (16 Nov 2026, tools/md-bridge/pleated_skirt.py): not measured; a skirt-weight wool flannel "
                 "about 280 g/m2; stiffness set by judgement against Kiln's presets (doc.rs). Check them against the "
                 "drape before trusting them.")


# ---- THE DRAFT: GarmentCode's fitted skirt at her measures, cut at the hip line (run under the lab's Python) ----

def gc_body(meas, we=WAIST_EASE, se=SEAT_EASE):
    """GarmentCode's body values (cm) that come from her measures; the rest stay its mean woman's."""
    return {"waist": round(meas["waist"] * (1 + we) / 10, 3), "hips": round(meas["seat"] * (1 + se) / 10, 3),
            "hips_line": round(meas["waistToSeat"] / 10, 3),
            "waist_back_width": round(meas["waistBack"] * (1 + we) / 10, 3),
            "hip_back_width": round(meas["seatBack"] * (1 + se) / 10, 3)}


def _gc_draft(out, meas_path):
    """Runs inside GarmentCode's venv: the PencilSkirt's two panels, their bottoms cut away at the hip line."""
    import copy  # noqa: F401
    import yaml
    sys.path.insert(0, GC_LAB)
    import gcpath  # noqa: F401
    from assets.bodies.body_params import BodyParameters
    from assets.garment_programs.skirt_paneled import PencilSkirt
    meas = json.load(open(meas_path, encoding="utf-8"))["measurements"]
    bd = yaml.safe_load(open(os.path.join(gcpath.SRC, "assets", "bodies", "mean_female.yaml")))
    over = gc_body(meas)
    bd["body"].update(over)
    body_file = checked(os.path.join(os.path.dirname(out), "gc-body-sheila.yaml"))
    yaml.safe_dump(bd, open(body_file, "w"))
    body = BodyParameters(body_file)
    design = yaml.safe_load(open(os.path.join(gcpath.SRC, "assets", "design_params", "default.yaml")))["design"]
    skirt = PencilSkirt(body, design, slit=False)

    def pts_of(edge):
        if type(edge).__name__ == "CurveEdge":
            n = max(4, int(edge.length() * 5))          # about every 2 mm
            return [list(e.start) for e in edge.linearize(n)]
        return [list(edge.start)]

    parts = {}
    # GarmentCode draws both panels as seen from the front (+x the wearer's left, its body frame): the front is kept
    # so, the back mirrored (sx -1) so that, placed from behind, its +x is the wearer's right (zip_jacket.py's rule).
    # The sides are found by their shape, not GarmentCode's interface names: the two curved edges are the side
    # curves from the hip line up to the waist, and the edges between them along the outline are the waist and darts.
    for key, pan, sx in (("gc.yokeFront", skirt.front, 1.0), ("gc.yokeBack", skirt.back, -1.0)):
        edges = list(pan.edges)
        c1, c2 = [k for k, e in enumerate(edges) if type(e).__name__ == "CurveEdge"][:2]
        e1, e2 = edges[c1], edges[c2]
        top = edges[c1 + 1:c2]
        mid = (e1.start[0] + e2.end[0]) / 2.0
        s1 = "L" if e1.start[0] > mid else "R"
        s2 = "R" if s1 == "L" else "L"
        names = {"hip" + s1: list(e1.start), "waist" + s1: list(e1.end),
                 "waist" + s2: list(e2.start), "hip" + s2: list(e2.end)}
        verts = [list(e.start) for e in top] + [list(top[-1].end)]
        top_y = max(v[1] for v in verts)
        k = 0
        for j in range(1, len(verts) - 1):
            if verts[j][1] < top_y - 1.0:
                names["d%da" % k], names["d%dtip" % k], names["d%db" % k] = verts[j - 1], verts[j], verts[j + 1]
                k += 1
        outline = pts_of(e1)
        for e in top:
            outline += pts_of(e)
        outline += pts_of(e2) + [list(e2.end)]
        mm = lambda p: [round(sx * p[0] * 10, 2), round(-p[1] * 10, 2)]  # noqa: E731  cm y up -> mm y down
        parts[key] = {"paths": {"seam": {"points": [mm(p) for p in outline]}},
                      "points": {n: mm(p) for n, p in names.items()},
                      "first_side": s1, "mirrored": sx < 0, "hipLineMm": round(-e1.start[1] * 10, 2)}
    d = {"design": "garmentcode.PencilSkirt, cut at the hip line (GarmentCode 2.0.2, MIT)",
         "made_by": "tools/md-bridge/pleated_skirt.py --draft", "measurements": meas, "measurements_file": meas_path,
         "ease": {"waist": WAIST_EASE, "seat": SEAT_EASE}, "garmentcode_body_cm": over,
         "not_measured": ["bum_points", "bust_points", "hip_inclination (GarmentCode's mean woman)"], "parts": parts}
    json.dump(d, open(checked(out), "w", encoding="utf-8"), indent=1)
    print("pleated skirt draft: %s (%s)" % (out, ", ".join("%s %d darts" % (k, sum(1 for n in v["points"] if n.endswith("tip")))
                                                           for k, v in parts.items())))


def draft(out, meas_path=MEAS):
    """The draft written by GarmentCode's own Python (its venv; numpy, scipy, svgpathtools live there)."""
    out = checked(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    try:
        import pygarment  # noqa: F401
        _gc_draft(out, meas_path)
        return 0
    except ImportError:
        return subprocess.call([GC_PY, os.path.abspath(__file__), "--gc-draft", out, meas_path])


# ---- THE PIECES ----

def measures(path):
    return json.load(open(path, encoding="utf-8"))["measurements"]


def _yoke(pts, nm, n_pleats, tag):
    """A yoke's outline as named edges: its hip edge a straight line cut into n_pleats equal stretches, named C0
    (the wearer's right side) to Cn (his left); its top cut at every dart point."""
    darts = sorted({n[:-3] for n in nm if n.endswith("tip")}, key=lambda n: int(n[1:]))
    # the corners round the outline as the draft writes it: from the hip of its first side (the outline's first
    # point) up to its waist, across the top (dart points in order, d0 nearest the first side), down the other side
    s1 = first_side(pts, nm)
    s2 = "R" if s1 == "L" else "L"
    corner_names = ["hip" + s1, "waist" + s1]
    for d in darts:
        corner_names += [d + "a", d + "tip", d + "b"]
    corner_names += ["waist" + s2, "hip" + s2]
    corner = [(idx_of(pts, nm[n]), n) for n in corner_names]
    edges = edges_from(pts, corner)
    # the closing edge (the cut at the hip line) replaced by its n stretches, from the last side's hip to the first's
    seg, a, b = edges[-1]
    p, q = seg[0], seg[-1]
    cn = ["C%d" % k for k in range(n_pleats + 1)]           # C0 on the wearer's right
    names = list(reversed(cn)) if a == "hipL" else cn
    out = edges[:-1]
    for k in range(n_pleats):
        t0, t1 = k / n_pleats, (k + 1) / n_pleats
        out.append(([[p[0] + (q[0] - p[0]) * t0, p[1] + (q[1] - p[1]) * t0],
                     [p[0] + (q[0] - p[0]) * t1, p[1] + (q[1] - p[1]) * t1]], names[k], names[k + 1]))
    ren = {"hipR": "C0", "hipL": "C%d" % n_pleats}
    out = [(s, ren.get(x, x), ren.get(y, y)) for s, x, y in out]
    return ccw([(s, x + tag, y + tag) for s, x, y in out]), darts, s1


def first_side(pts, nm):
    """Which of the wearer's sides the draft's outline starts on (its first point is that side's hip)."""
    return "L" if idx_of(pts, nm["hipL"]) == 0 else "R"


def _top_stretches(edges, darts, s1, tag):
    """The yoke's waist edge as its stretches between darts, from the wearer's right side to his left:
    [(right end's name, left end's name, length)]."""
    s2 = "R" if s1 == "L" else "L"
    stops = ["waist" + s1]                   # the darts run from the first side (d0) to the other
    for d in darts:
        stops += [d + "a", d + "b"]
    stops.append("waist" + s2)
    E = {frozenset((a, b)): seg for seg, a, b in edges}
    out = []
    for k in range(0, len(stops), 2):
        a, b = stops[k] + tag, stops[k + 1] + tag
        out.append((a, b, length(E[frozenset((a, b))])))
    if s1 == "L":                            # listed from his left: turned round, each from its right end
        out = [(b, a, L) for a, b, L in reversed(out)]
    return out


def _band(stretches, tag, h=BAND_H):
    """A band whose foot is cut into the yoke's waist stretches (in order, from x = 0 upward), closed by its ends."""
    x, foot = 0.0, []
    for k, (_a, _b, L) in enumerate(stretches):
        w = L * BAND_OF_WAIST
        foot.append(([[x, 0.0], [x + w, 0.0]], "bf%d" % k + tag, "bf%d" % (k + 1) + tag))
        x += w
    n = len(stretches)
    return ccw(foot + [([[x, 0.0], [x, h]], "bf%d" % n + tag, "btE" + tag), ([[x, h], [0.0, h]], "btE" + tag, "btS" + tag),
                       ([[0.0, h], [0.0, 0.0]], "btS" + tag, "bf0" + tag)])


def pleat_layout(visible, n, take=PLEAT_TAKE):
    """A panel's top-edge points along x: [(name, x)] with each pleat's visible stretch s, outer fold F, inner fold B
    a depth d further, placement P a depth d beyond (the next stretch starts at P). Returns (points, s, d, width)."""
    s = visible / n
    d = s * take / 2.0
    pts, x = [("top0", 0.0)], 0.0
    for k in range(n):
        x += s
        pts.append(("f%d" % k, x))
        pts.append(("b%d" % k, x + d))
        pts.append(("p%d" % k, x + 2 * d))
        x += 2 * d
    return pts, s, d, x


def _panel(visible, n, h, tag, take=PLEAT_TAKE):
    tops, s, d, w = pleat_layout(visible, n, take)
    edges = [([[0.0, 0.0], [w, 0.0]], "hem0" + tag, "hemW" + tag),
             ([[w, 0.0], [w, h]], "hemW" + tag, tops[-1][0] + tag)]
    for k in range(len(tops) - 1, 0, -1):
        edges.append(([[tops[k][1], h], [tops[k - 1][1], h]], tops[k][0] + tag, tops[k - 1][0] + tag))
    edges.append(([[0.0, h], [0.0, 0.0]], "top0" + tag, "hem0" + tag))
    folds = []
    for name, x in tops:
        if name[0] in "fb":
            folds.append({"name": name + tag, "points": [[round(x, 2), 0.0], [round(x, 2), round(h, 2)]],
                          "angle": FOLD_ANGLE if name[0] == "f" else -FOLD_ANGLE, "strength": FOLD_STRENGTH})
    return ccw(edges), folds, {"visible_mm": round(s, 2), "depth_mm": round(d, 2), "width_mm": round(w, 2)}


def build(gc, meas, n=PLEATS, skirt_len=None, take=PLEAT_TAKE):
    """The six pieces as named edges, the fold lines, and the cut's numbers."""
    L = skirt_len or meas["waistToKnee"] + KNEE_BELOW
    pieces, info, folds = {}, {}, {}
    fpts, fn = gc["gc.yokeFront"]
    bpts, bn = gc["gc.yokeBack"]
    pieces["yokeFront"], dF, sF = _yoke(fpts, fn, n, "F")
    pieces["yokeBack"], dB, sB = _yoke(bpts, bn, n, "B")
    stF, stB = _top_stretches(pieces["yokeFront"], dF, sF, "F"), _top_stretches(pieces["yokeBack"], dB, sB, "B")
    # each band's x runs as its yoke's: the front's from his right (placed from the front), the back's from his left
    # (placed from behind), so the back band's foot takes the stretches in the other order
    pieces["bandFront"], pieces["bandBack"] = _band(stF, "F"), _band(list(reversed(stB)), "B")
    # the hem's line: the front yoke's depth at its centre plus the panel make L
    yd = abs(max(p[1] for p in fpts) - fn["hipR"][1])
    h = L - yd
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    for t, key in (("F", "yokeFront"), ("B", "yokeBack")):
        hip = sum(length(E(key, "C%d" % k + t, "C%d" % (k + 1) + t)) for k in range(n))
        pieces["pleats" + ("Front" if t == "F" else "Back")], folds[t], info["pleats" + t] = _panel(hip, n, h, t, take)
    info.update({"skirt_length_mm": round(L, 1), "front_yoke_depth_mm": round(yd, 1), "panel_height_mm": round(h, 1),
                 "pleats_per_panel": n, "pleat_take": take, "darts": {"front": len(dF), "back": len(dB)},
                 "top_stretches": {"F": [s[:2] for s in stF], "B": [s[:2] for s in stB]}})
    return {k: pieces[k] for k in ORDER}, folds, info


def seams(info, n):
    """(piece, end, end) against (piece, end, end), the ends that meet listed in the same order."""
    out = []
    # the darts shut (each leg from the waist to the tip)
    for t, key in (("F", "yokeFront"), ("B", "yokeBack")):
        for k in range(info["darts"]["front" if t == "F" else "back"]):
            out.append(((key, "d%da" % k + t, "d%dtip" % k + t), (key, "d%db" % k + t, "d%dtip" % k + t)))
    # the yoke's side seams, hip to waist: the wearer's left of the front to the left of the back, and the right
    out += [(("yokeFront", "C%dF" % n, "waistLF"), ("yokeBack", "C%dB" % n, "waistLB")),
            (("yokeFront", "C0F", "waistRF"), ("yokeBack", "C0B", "waistRB"))]
    # the band's foot to the yoke's waist stretches, in order from the wearer's right (front) and left (back)
    for t, key, band in (("F", "yokeFront", "bandFront"), ("B", "yokeBack", "bandBack")):
        st = info["top_stretches"][t]
        if t == "B":
            st = list(reversed([(b, a) for a, b in st]))      # the back's x runs from his left to his right
        for k, (a, b) in enumerate(st):
            out.append(((band, "bf%d" % k + t, "bf%d" % (k + 1) + t), (key, a, b)))
    # the band shut at the sides: the front's end (his left) to the back's start (his left), and the right
    nf, nb = len(info["top_stretches"]["F"]), len(info["top_stretches"]["B"])
    out += [(("bandFront", "bf%dF" % nf, "btEF"), ("bandBack", "bf0B", "btSB")),
            (("bandFront", "bf0F", "btSF"), ("bandBack", "bf%dB" % nb, "btEB"))]
    # each pleated panel's visible stretches to its yoke's hip stretches, and each pleat tacked shut at the top
    for t, key, pan in (("F", "yokeFront", "pleatsFront"), ("B", "yokeBack", "pleatsBack")):
        yk = (lambda k: "C%d" % k + t) if t == "F" else (lambda k: "C%d" % (n - k) + t)
        for k in range(n):
            start = "top0" if k == 0 else "p%d" % (k - 1)
            out.append(((pan, start + t, "f%d" % k + t), (key, yk(k), yk(k + 1))))
            out.append(((pan, "b%d" % k + t, "f%d" % k + t), (pan, "b%d" % k + t, "p%d" % k + t)))
    # the panels' sides, hem to top: the front's last pleat over the back's start (his left), the back's end to the
    # front's start (his right): the ring of pleats runs one way round the body
    out += [(("pleatsFront", "hemWF", "p%dF" % (n - 1)), ("pleatsBack", "hem0B", "top0B")),
            (("pleatsBack", "hemWB", "p%dB" % (n - 1)), ("pleatsFront", "hem0F", "top0F"))]
    return out


def plan(gc, meas, n=PLEATS, skirt_len=None, take=PLEAT_TAKE):
    pieces, folds, info = build(gc, meas, n, skirt_len, take)
    out_pieces, lines = [], {}
    for key, edges in pieces.items():
        pts = []
        for k, (seg, a, b) in enumerate(edges):
            lines[(key, a, b)] = (k, True)
            lines[(key, b, a)] = (k, False)
            pts.append([round(seg[0][0], 2), round(seg[0][1], 2), CORNER])
            pts += [[round(x, 2), round(y, 2), CURVE] for x, y in seg[1:-1]]
        q = {"key": key, "points": pts, "arrange": ARRANGE[key], "fabric": "band" if key.startswith("band") else "skirt"}
        if key.startswith("pleats"):
            q["folds"] = folds[key[6]]
        out_pieces.append(q)
    out_seams = []
    for (pa, a0, a1), (pb, b0, b1) in seams(info, n):
        la, fa = lines[(pa, a0, a1)]
        lb, fb = lines[(pb, b0, b1)]
        out_seams.append({"a": [pa, la, fa], "b": [pb, lb, fb], "names": [a0, a1, b0, b1]})
    corners = {key: [[a, round(seg[0][0], 2), round(seg[0][1], 2)] for seg, a, _b in edges] for key, edges in pieces.items()}
    patch = {"yokeFront": {"bottom": ["C0F", "C%dF" % n], "top": ["waistLF", "waistRF"]},
             "yokeBack": {"bottom": ["C%dB" % n, "C0B"], "top": ["waistRB", "waistLB"]},
             "pleatsFront": {"bottom": ["hem0F", "hemWF"], "top": ["p%dF" % (n - 1), "top0F"]},
             "pleatsBack": {"bottom": ["hem0B", "hemWB"], "top": ["p%dB" % (n - 1), "top0B"]}}
    for t, key in (("F", "bandFront"), ("B", "bandBack")):
        patch[key] = {"bottom": ["bf0" + t, "bf%d" % len(info["top_stretches"][t]) + t], "top": ["btE" + t, "btS" + t]}
    return {"pieces": out_pieces, "seams": out_seams, "corners": corners, "patch": patch, "cut": info,
            "kiln_cannot": ["pleat pressing or tacking below the yoke seam", "fold direction (sign unused)",
                            "a drape in a sitting pose", "the hem handed to Unreal's cloth (M6)"]}


JOB = '''# Generated by tools/md-bridge/pleated_skirt.py from %(src)s: Sheila's pleated skirt made, its pleats' fold lines
# drawn, placed on the body's points by name, sewn, draped (%(steps)d steps at 20 mm, 200 at 10 mm with the band at 6
# and the pleated panels at %(pp)g, 100 at Fitting) and exported to %(out)s. Runs on Kiln (run_job_script.py) or
# Marvelous (md_job.py). Kiln has no pleat pressing: see the writer's docstring.
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
        pattern_api.SetArrangementShapeStyle(idx, "Curved")
result["made"] = made
result["arranged"] = {p["key"]: p["arrange"] in points for p in PLAN["pieces"]}
# THE PLEATS' FOLD LINES (each kept as its answer, so a refused call shows)
folds = {}
for p in PLAN["pieces"]:
    for f in p.get("folds", []):
        try:
            k = pattern_api.CreateInternalShapeWithPoints(made[p["key"]], [(float(x), float(y)) for x, y in f["points"]], False)
            folds[f["name"]] = [k, bool(pattern_api.SetInternalLineFold(made[p["key"]], k, f["angle"], f["strength"]))]
        except Exception as e:
            folds[f["name"]] = "refused: %%s" %% e
result["folds"] = folds
result["sewn"] = [bool(pattern_api.AddSeamlinePairGroup(made[s["a"][0]], s["a"][1], made[s["b"][0]], s["b"][1], s["a"][2], s["b"][2]))
                  for s in PLAN["seams"]]
# THE CLOTH: Marvelous's stock files where they are and this is Marvelous; on Kiln our own descriptions beside the job
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
for p in PLAN["pieces"]:
    if p["key"].startswith("band"):
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], 6.0)
    if p["key"].startswith("pleats"):
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], %(pp)g)
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
result["exported"] = export_api.ExportOBJ(os.path.join(OUT, "pleated_skirt.obj"), eo)
result["zprj"] = export_api.ExportZPrj(os.path.join(OUT, "pleated_skirt.zprj"))
log("pleated skirt made, sewn and draped")
'''


def write_fabrics(folder):
    out = {}
    for name, f in FABRICS.items():
        d = dict(f["kiln"])
        d["_estimates"] = ESTIMATE_NOTE
        json.dump(d, open(checked(os.path.join(folder, d["name"] + ".drape-fabric.json")), "w", encoding="utf-8"), indent=1)
        out[name] = {"md": f["md"], "own": os.path.join(folder, d["name"] + ".zfab")}   # never a file: Kiln reads beside it
    return out


def girths(gc, meas, pieces, info, n):
    """The yoke's waist (darts shut) and hip rounds against the body's plus ease, and the panels' widths (mm)."""
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    waist = sum(L for t in "FB" for _a, _b, L in [(a, b, length(E("yoke" + ("Front" if t == "F" else "Back"), a, b)))
                                                   for a, b in info["top_stretches"][t]])
    hip = sum(length(E(k, "C%d" % j + k[4], "C%d" % (j + 1) + k[4])) for k in ("yokeFront", "yokeBack") for j in range(n))
    band = sum(length(E(b, "bf%d" % j + b[4], "bf%d" % (j + 1) + b[4]))
               for b in ("bandFront", "bandBack") for j in range(len(info["top_stretches"][b[4]])))
    hem = sum(info["pleats" + t]["width_mm"] for t in "FB")
    return {"waist": (waist, meas["waist"] * (1 + WAIST_EASE)), "hip": (hip, meas["seat"] * (1 + SEAT_EASE)),
            "band": (band, waist), "hem_flat": (hem, hip * (1 + info["pleat_take"]))}


def main(argv):
    src, job = argv[0], checked(argv[1])
    opt = lambda k, d: float(argv[argv.index(k) + 1]) if k in argv else d  # noqa: E731
    sarg = lambda k, d: argv[argv.index(k) + 1] if k in argv else d  # noqa: E731
    out = checked(sarg("--out", os.path.join(OUT_DIR, "pleated_skirt")))
    n = int(opt("--pleats", PLEATS))
    gc, meas = load(src), measures(src)
    sl = opt("--length", 0.0) or None
    p = plan(gc, meas, n, sl)
    steps = int(opt("--steps", 400))
    folder = os.path.dirname(os.path.abspath(job))
    fab = write_fabrics(folder)
    open(job, "w", encoding="utf-8").write(JOB % {"src": src, "plan": json.dumps(p), "out": out, "steps": steps,
                                                  "fabrics": fab, "pp": opt("--pleat-particle", PLEAT_PARTICLE),
                                                  "avt": sarg("--avatar", BODY)})
    json.dump(p, open(checked(job[:-3] + ".plan.json"), "w", encoding="utf-8"), indent=1)
    c = p["cut"]
    print("pleated skirt: %d pieces, %d seams, %d fold lines -> %s" % (
        len(p["pieces"]), len(p["seams"]), sum(len(q.get("folds", [])) for q in p["pieces"]), job))
    print("  length %.1f mm (yoke %.1f + panel %.1f); pleats %d a panel, front s %.1f d %.1f, back s %.1f d %.1f" % (
        c["skirt_length_mm"], c["front_yoke_depth_mm"], c["panel_height_mm"], n, c["pleatsF"]["visible_mm"],
        c["pleatsF"]["depth_mm"], c["pleatsB"]["visible_mm"], c["pleatsB"]["depth_mm"]))
    pieces, _f, info = build(gc, meas, n, sl)
    for k, (got, want) in girths(gc, meas, pieces, info, n).items():
        print("  %-8s %.1f mm (against %.1f, %+.2f%%)" % (k, got, want, 100 * (got / want - 1)))
    for q in p["pieces"]:
        print("  %-11s %3d points  on %s  (%s)" % (q["key"], len(q["points"]), q["arrange"], q["fabric"]))


def _check(gc, meas, n, label):
    ok, msg = [], []
    pieces, folds, info = build(gc, meas, n)
    p = plan(gc, meas, n)
    keys = [q["key"] for q in p["pieces"]]
    ok.append(keys == ORDER and len(set(keys)) == len(keys))
    # every piece's corner names unique within it
    for key, edges in pieces.items():
        names = [a for _s, a, _b in edges]
        ok.append(len(names) == len(set(names)))
    # the seam count: darts, 2 yoke sides, band stretches, 2 band sides, n stretches and n tacks a panel, 2 panel sides
    nd = info["darts"]["front"] + info["darts"]["back"]
    nst = len(info["top_stretches"]["F"]) + len(info["top_stretches"]["B"])
    want_seams = nd + 2 + nst + 2 + 4 * n + 2
    ok.append(len(p["seams"]) == want_seams)
    # every seam's two edges, found by their ends, of matching length: darts, bands, stretches, tacks and panel sides
    # 1:1 within 1%; the yoke's side seams the back's hip extension (front / back = 1 / 1.05) within 1%
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    bad = []
    for (pa, a0, a1), (pb, b0, b1) in seams(info, n):
        r = length(E(pa, a0, a1)) / length(E(pb, b0, b1))
        side = pa == "yokeFront" and pb == "yokeBack"
        good = abs(r * BACK_HIP_EXT - 1) <= 0.01 if side else abs(r - 1) <= 0.01
        ok.append(good)
        if not good:
            bad.append("%s %s-%s %.3f" % (pa, a0, a1, r))
    # each pleat's tack: both halves d long; the fold lines two a pleat
    for t in "FB":
        ok.append(len(folds[t]) == 2 * n)
    g = girths(gc, meas, pieces, info, n)
    for k in ("waist", "hip"):
        ok.append(abs(g[k][0] / g[k][1] - 1) <= 0.005)
    ok.append(abs(g["band"][0] / g["band"][1] - BAND_OF_WAIST) <= 0.002)
    ok.append(abs(g["hem_flat"][0] / g["hem_flat"][1] - 1) <= 0.002)
    # the length: the front yoke's depth (its hip line under its waist) plus the panel make the skirt, and the yoke's
    # depth is the draft's waist-to-seat
    ok.append(abs(info["front_yoke_depth_mm"] + info["panel_height_mm"] - info["skirt_length_mm"]) < 0.5)
    ok.append(abs(info["front_yoke_depth_mm"] - meas["waistToSeat"]) <= 2.0)
    ok.append(abs(info["skirt_length_mm"] - (meas["waistToKnee"] + KNEE_BELOW)) < 0.5)
    # the areas: the yokes' as drafted, less nothing (the cut at the hip line is their own bottom), within 1%
    poly = lambda pts: abs(sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1] for k in range(len(pts))) / 2)  # noqa: E731
    for key, part in (("yokeFront", "gc.yokeFront"), ("yokeBack", "gc.yokeBack")):
        got, want = area(pieces[key]), poly(gc[part][0])
        ok.append(abs(got / want - 1) <= 0.01)
    msg.append("  %s: %d pleats a panel; waist %.1f against %.1f; hip %.1f against %.1f; band %.3f of the waist; flat hem "
               "%.1f; length %.1f = yoke %.1f + panel %.1f; darts %d front %d back; %d seams%s" % (
                   label, n, g["waist"][0], g["waist"][1], g["hip"][0], g["hip"][1], g["band"][0] / g["band"][1],
                   g["hem_flat"][0], info["skirt_length_mm"], info["front_yoke_depth_mm"], info["panel_height_mm"],
                   info["darts"]["front"], info["darts"]["back"], len(p["seams"]),
                   ("; off: " + ", ".join(bad)) if bad else ""))
    return ok, msg


def selftest():
    ok, msg = [], []
    # the pleat layout alone (no draft needed): widths and depths add up for any count
    for vis, n in ((455.0, 8), (511.0, 8), (966.0, 16), (480.0, 5)):
        pts, s, d, w = pleat_layout(vis, n)
        xs = [x for _n, x in pts]
        ok.append(abs(w - vis * (1 + PLEAT_TAKE)) < 1e-6 and abs(s * n - vis) < 1e-6 and abs(2 * d * n - vis * PLEAT_TAKE) < 1e-6)
        ok.append(all(xs[k] < xs[k + 1] for k in range(len(xs) - 1)) and len({nm for nm, _ in pts}) == len(pts))
    # outpath: a relative path is refused before anything is written
    import contextlib
    import io
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            checked("pleats/x.json")
        ok.append(False)
    except SystemExit:
        ok.append(True)
    fields = {"name", "color", "stretch_weft", "stretch_warp", "shear", "bending_weft", "bending_warp", "density",
              "friction", "thickness", "shrink_weft", "shrink_warp", "damping", "texture", "texture_scale", "texture_angle"}
    for f in FABRICS.values():
        ok.append(set(f["kiln"]) <= fields and "wool" not in f["kiln"]["name"])
    if os.path.isfile(DRAFT):
        gc, meas = load(DRAFT), measures(DRAFT)
        # the draft's measures are S4's own file's, not the bodies/ file's (Lena C1's)
        ok.append(meas == json.load(open(MEAS, encoding="utf-8"))["measurements"])
        # NO SPECIAL-CASE NUMBERS: the same checks at other pleat counts on the same draft
        for n in (PLEATS, 6, 12):
            o, m = _check(gc, meas, n, "Sheila")
            ok += o
            msg += m
    else:
        msg.append("  (no draft on this machine: the pattern checks skipped)")
    print("\n".join(msg))
    print("pleated skirt selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--gc-draft" in a:
        i = a.index("--gc-draft")
        _gc_draft(checked(a[i + 1]), a[i + 2])
        sys.exit(0)
    if "--draft" in a:
        sys.exit(draft(a[a.index("--draft") + 1], a[a.index("--meas") + 1] if "--meas" in a else MEAS))
    sys.exit(main(a))
