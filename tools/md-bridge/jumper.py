#!/usr/bin/env python3
"""Tom's plain jumper as one Marvelous Designer job: FreeSewing's Brian block at his size with a jumper's ease, cut
into a whole front, a whole back and two sleeves, placed on his avatar's arrangement points, sewn, draped, exported.

    python tools/md-bridge/jumper.py BRIAN.json JOB.py [--out DIR] [--steps 400] [--sleeve-shorten 70]
        [--neck-depth 80] [--body-length 535] [--avatar AVT] [--sleeve-position X,Y,OFFSET] [--cuff-position X,Y,OFFSET]
    python tools/md-bridge/md_job.py JOB.py          # runs it through the bridge

WHY, 29 October 2026 (his order C9: after the cuffs, the jumper, jeans and shoes by the game-garment skill; the plan,
production/art/clothing/tom-outfit/JUMPER-PLAN-2026-10-29.md). The block is Brian drafted at chest ease 10%
(F:/LedgerTools/garments/tom/jumper/pattern/brian-jumper.json); the jacket's helpers (tools/md-bridge/zip_jacket.py:
the outline's named edges, mirroring, winding) are imported, not copied.

THE RIB EDGES ARE BUILT, NOT DRAPED TO FIT. Marvelous's elastic rib was set aside after two tries on the jacket's cuffs
(29 October) and the cuffs built to the wrist's shape passed every mark, so the welt, cuffs and crew neckband are
draped loosely with the shell, sewn plainly, and then built to the body's shape on this drape (tools/md/build_cuffs.py
moves only a band's points, keeping its faces, UVs and seam).

THE CUT (the plan's numbers, each with its source there): the front's neckline lowered from Brian's 61 mm to NECK_DEPTH
(a crew neck 3 to 4 in deep); the body from the shoulder's high point to the welt BODY_LENGTH, its points under the
armhole drawn up in proportion so the armhole is untouched; the sleeve shortened by --sleeve-shorten under its biceps
line, as the jacket's was (its drapes 2 and 3: 40 mm off Brian's sleeve and a 60 mm cuff ended at the wrist; the
jumper's 75 mm cuff and 70 off end it about 15 mm short of the jacket's, so the jumper never shows below it).

The particle distance as the skill orders it: 20 mm while it settles, then 10 mm on the whole garment, Fitting last.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zip_jacket import CORNER, CURVE, WRIST_MM, ccw, edges_from, idx_of, length, load, mirror_edges, rect  # noqa: E402

NECK_DEPTH = 80.0           # mm below the shoulder's high point at the centre front
BODY_LENGTH = 535.0         # mm, the shoulder's high point to the welt's top edge
WELT_H, CUFF_H, NECKBAND_H = 75.0, 75.0, 28.0   # the built edges, for the record and the bake chain
SLEEVE_SHORTEN = 70.0
# THE RIB PIECES DRAPED LOOSELY WITH THE SHELL (29 October): the built route moves the points of a band Marvelous has
# already sewn on (tools/md/build_cuffs.py keeps the drape's faces, UVs and seam and moves only the band's vertices),
# so the welt, cuffs and neckband are in the drape, cut as the jacket's were and sewn plainly, no elastic: the welt
# at 0.90 of the hem (drawn in 8 to 10%, JUMPER-2026-09-30), the cuffs at the wrist's own girth (the jacket's third
# try), the neckband at 0.92 of the neckline, one ring closed at the left shoulder
RIB_WELT, RIB_NECK = 0.90, 0.92
ARRANGE = {"front": "Body_Front_Center_3", "back": "Body_Back_Center_3", "sleeveR": "Arm_Outside_2_R", "sleeveL": "Arm_Outside_2_L",
           "weltFront": "Body_Front_Center_5", "weltBack": "Body_Back_Center_5", "cuffR": "Arm_Outside_3_R", "cuffL": "Arm_Outside_3_L",
           "neckband": "Neck_Back"}
RIB = ("welt", "cuff", "neckband")
FABRIC = "V2_Cut_Sew_Knit_LowGaugeKnit_1.zfab"      # its physics only: a jumper's knit, heavier than jersey


def shorten_body(pts, names, armhole_y, hem_y, length):
    """Every point below the armhole drawn up in proportion so the hem lands at -length (y up, the shoulder's high
    point at 0); the armhole and everything above it untouched."""
    k = (length + armhole_y) / (-hem_y + armhole_y) if hem_y < armhole_y else 1.0
    f = lambda p: [p[0], armhole_y + (p[1] - armhole_y) * k if p[1] < armhole_y else p[1]]  # noqa: E731
    return [f(p) for p in pts], {n: f(p) for n, p in names.items()}


def lower_neck(pts, names, depth):
    """The front's neck curve (hps to cfNeck) deepened to `depth` below the high point, its points scaled down in y."""
    hps, cf = names["hps"], names["cfNeck"]
    k = depth / max(hps[1] - cf[1], 1e-6)
    # the neck edge runs forward along the outline from the high point to the centre front, wrapping past its end
    # as edges_from walks it (cfNeck is the outline's first corner)
    i, j = idx_of(pts, hps), idx_of(pts, cf)
    seg = set(range(i, j + 1)) if j > i else set(range(i, len(pts))) | set(range(0, j + 1))
    out = [[x, hps[1] - (hps[1] - y) * k] if n in seg else [x, y] for n, (x, y) in enumerate(pts)]
    names = dict(names, cfNeck=[cf[0], hps[1] - depth])
    return out, names


def whole(half, names_order):
    """A whole piece from a half drafted with its centre on x 0: the half's edges, then its mirror, joined along the
    centre (the centre edge vanishes); the hem and neck become single edges across it. `half` is [(seg, a, b)] with
    the centre edge first (centre neck to centre hem); names_order names the half's corners after the centre hem."""
    hb = {(a, b): seg for seg, a, b in half}
    c_hem, hem, arm, sh, hps, c_neck = names_order
    hem_r = hb[(c_hem, hem)]
    neck_r = list(reversed(hb[(hps, c_neck)]))
    return [([[-x, y] for x, y in reversed(hem_r)][:-1] + hem_r, "hemL", "hemR"),
            (hb[(hem, arm)], "hemR", "armholeR"),
            (hb[(arm, sh)], "armholeR", "shoulderR"),
            (hb[(sh, hps)], "shoulderR", "hpsR"),
            (list(reversed(neck_r)) + [[-x, y] for x, y in neck_r][1:], "hpsR", "hpsL"),
            ([[-x, y] for x, y in reversed(hb[(sh, hps)])], "hpsL", "shoulderL"),
            ([[-x, y] for x, y in reversed(hb[(arm, sh)])], "shoulderL", "armholeL"),
            ([[-x, y] for x, y in reversed(hb[(hem, arm)])], "armholeL", "hemL")]


def build(brian, sleeve_shorten=SLEEVE_SHORTEN, neck_depth=NECK_DEPTH, body_length=BODY_LENGTH):
    fpts, fn = brian["brian.front"]
    bpts, bn = brian["brian.back"]
    spts, sn = brian["library.sleeve"]
    fpts, fn = lower_neck(fpts, fn, neck_depth)
    fpts, fn = shorten_body(fpts, fn, fn["armhole"][1], fn["cfHem"][1], body_length)
    bpts, bn = shorten_body(bpts, bn, bn["armhole"][1], bn["cbHem"][1], body_length)
    if sleeve_shorten:
        k = 1.0 - sleeve_shorten / -min(y for _, y in spts)
        spts = [[x, y * k if y < 0 else y] for x, y in spts]
        sn = {n: [x, y * k if y < 0 else y] for n, (x, y) in sn.items()}
    corner = lambda pts, nm, names: [(idx_of(pts, nm[n]), n) for n in names]  # noqa: E731
    front = edges_from(fpts, corner(fpts, fn, ["cfNeck", "cfHem", "hem", "armhole", "shoulder", "hps"]))
    back = edges_from(bpts, corner(bpts, bn, ["cbNeck", "cbHem", "hem", "armhole", "shoulder", "hps"]))
    sleeve = edges_from(spts, corner(spts, sn, ["bicepsLeft", "wristLeft", "wristRight", "bicepsRight", "sleeveTop"]))
    tag = lambda edges, s: [(seg, a + s, b + s) for seg, a, b in edges]  # noqa: E731
    # the front seen from the front: the drafted half (its side on +x) is the wearer's left, so its +x corners are L
    # and the mirror's R; the back seen from behind has his right on +x, as drafted
    pieces = {}
    f = ccw(whole(front, ["cfHem", "hem", "armhole", "shoulder", "hps", "cfNeck"]))
    swap = lambda n: n[:-1] + ("L" if n.endswith("R") else "R")  # noqa: E731
    pieces["front"] = ccw([(seg, swap(a), swap(b)) for seg, a, b in f])
    pieces["back"] = ccw(whole(back, ["cbHem", "hem", "armhole", "shoulder", "hps", "cbNeck"]))
    pieces["sleeveR"] = ccw(tag(sleeve, "R"))
    pieces["sleeveL"] = ccw(tag(mirror_edges(sleeve), "L"))
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    for k, src in (("weltFront", "front"), ("weltBack", "back")):
        w = length(E(src, "hemL", "hemR")) * RIB_WELT
        pieces[k] = rect(w, WELT_H, [k + "LowL", k + "LowR", k + "R", k + "L"])
    for s in ("R", "L"):
        cuff = rect(WRIST_MM, CUFF_H, ["cuffAlow" + s, "cuffBlow" + s, "cuffB" + s, "cuffA" + s])
        pieces["cuff" + s] = ccw(mirror_edges(cuff)) if s == "R" else cuff
    nf, nb = length(E("front", "hpsR", "hpsL")) * RIB_NECK, length(E("back", "hpsR", "hpsL")) * RIB_NECK
    # the band's foot in two lines, the front's neck then the back's, from the left shoulder round by the right;
    # its two short ends meet at the left shoulder
    pieces["neckband"] = [([[0, 0], [nf, 0]], "nbFrontL", "nbFrontR"), ([[nf, 0], [nf + nb, 0]], "nbFrontR", "nbBackL"),
                          ([[nf + nb, 0], [nf + nb, NECKBAND_H]], "nbBackL", "nbTopEnd"),
                          ([[nf + nb, NECKBAND_H], [0, NECKBAND_H]], "nbTopEnd", "nbTopStart"),
                          ([[0, NECKBAND_H], [0, 0]], "nbTopStart", "nbFrontL")]
    return pieces


def seams():
    out = []
    for s in ("R", "L"):
        out += [(("front", "hps" + s, "shoulder" + s), ("back", "hps" + s, "shoulder" + s)),
                (("front", "armhole" + s, "hem" + s), ("back", "armhole" + s, "hem" + s)),
                (("sleeve" + s, "bicepsRight" + s, "sleeveTop" + s), ("front", "armhole" + s, "shoulder" + s)),
                (("sleeve" + s, "sleeveTop" + s, "bicepsLeft" + s), ("back", "shoulder" + s, "armhole" + s)),
                (("sleeve" + s, "bicepsLeft" + s, "wristLeft" + s), ("sleeve" + s, "bicepsRight" + s, "wristRight" + s)),
                (("cuff" + s, "cuffA" + s, "cuffB" + s), ("sleeve" + s, "wristLeft" + s, "wristRight" + s)),
                (("cuff" + s, "cuffA" + s, "cuffAlow" + s), ("cuff" + s, "cuffB" + s, "cuffBlow" + s))]
    # the welt: the front's along the front's hem (seen from the front, his right on -x), the back's along the back's;
    # its two parts sewn at the side seams
    out += [(("weltFront", "weltFrontR", "weltFrontL"), ("front", "hemR", "hemL")),
            (("weltBack", "weltBackL", "weltBackR"), ("back", "hemL", "hemR")),
            (("weltFront", "weltFrontR", "weltFrontLowR"), ("weltBack", "weltBackR", "weltBackLowR")),
            (("weltFront", "weltFrontL", "weltFrontLowL"), ("weltBack", "weltBackL", "weltBackLowL")),
            # the neckband round the neckline from the left shoulder, closed there
            (("neckband", "nbFrontL", "nbFrontR"), ("front", "hpsL", "hpsR")),
            (("neckband", "nbFrontR", "nbBackL"), ("back", "hpsR", "hpsL")),
            (("neckband", "nbTopStart", "nbFrontL"), ("neckband", "nbTopEnd", "nbBackL"))]
    return out


def plan(brian, sleeve_shorten=SLEEVE_SHORTEN, neck_depth=NECK_DEPTH, body_length=BODY_LENGTH):
    pieces = build(brian, sleeve_shorten, neck_depth, body_length)
    out_pieces, lines = [], {}
    for key, edges in pieces.items():
        pts = []
        for k, (seg, a, b) in enumerate(edges):
            lines[(key, a, b)] = (k, True)
            lines[(key, b, a)] = (k, False)
            pts.append([round(seg[0][0], 2), round(seg[0][1], 2), CORNER])
            pts += [[round(x, 2), round(y, 2), CURVE] for x, y in seg[1:-1]]
        out_pieces.append({"key": key, "points": pts, "arrange": ARRANGE[key], "fabric": "rib" if key.startswith(RIB) else "knit"})
    out_seams = []
    for (pa, a0, a1), (pb, b0, b1) in seams():
        la, fa = lines[(pa, a0, a1)]
        lb, fb = lines[(pb, b0, b1)]
        out_seams.append({"a": [pa, la, fa], "b": [pb, lb, fb], "names": [a0, a1, b0, b1]})
    corners = {key: [[a, round(seg[0][0], 2), round(seg[0][1], 2)] for seg, a, _b in edges] for key, edges in pieces.items()}
    patch = {"front": {"bottom": ["hemR", "hemL"], "top": ["shoulderL", "shoulderR"]},
             "back": {"bottom": ["hemL", "hemR"], "top": ["shoulderR", "shoulderL"]}}
    for s in ("R", "L"):
        patch["sleeve" + s] = {"bottom": ["wristLeft" + s, "wristRight" + s], "top": ["bicepsRight" + s, "bicepsLeft" + s]}
        patch["cuff" + s] = {"bottom": ["cuffAlow" + s, "cuffBlow" + s], "top": ["cuffB" + s, "cuffA" + s]}
    for k in ("weltFront", "weltBack"):
        patch[k] = {"bottom": [k + "LowL", k + "LowR"], "top": [k + "R", k + "L"]}
    patch["neckband"] = {"bottom": ["nbFrontL", "nbBackL"], "top": ["nbTopEnd", "nbTopStart"]}
    built = {"welt_mm": WELT_H, "cuff_mm": CUFF_H, "neckband_mm": NECKBAND_H, "neck_depth_mm": neck_depth, "body_length_mm": body_length,
             "sleeve_shorten_mm": sleeve_shorten}
    return {"pieces": out_pieces, "seams": out_seams, "corners": corners, "patch": patch, "built_edges": built}


JOB = '''# Generated by tools/md-bridge/jumper.py from %(src)s: Tom's jumper's shell made, placed on his avatar's points,
# sewn, draped (%(steps)d steps at 20 mm, 200 at 10 mm, 100 at Fitting) and exported to %(out)s.
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
SLEEVE_POS = %(sleeve_pos)r
CUFF_POS = %(cuff_pos)r
made = {}
for p in PLAN["pieces"]:
    idx = pattern_api.CreatePatternWithPoints([(float(x), float(y), int(t)) for x, y, t in p["points"]])
    made[p["key"]] = idx
    pattern_api.SetPatternPieceName(idx, p["key"])
    if p["arrange"] in points and idx >= 0:
        pattern_api.SetArrangement(idx, points[p["arrange"]])
        if p["key"].startswith("sleeve") and SLEEVE_POS:
            pattern_api.SetArrangementPosition(idx, *SLEEVE_POS)
            pattern_api.SetArrangementShapeStyle(idx, "Curved")
        # the cuffs as the jacket's best drape placed them (drape 19: Y 0, offset 30 on the straight-elbowed body),
        # curved round the wrist before sewing
        if p["key"].startswith("cuff"):
            if CUFF_POS:
                pattern_api.SetArrangementPosition(idx, *CUFF_POS)
            pattern_api.SetArrangementShapeStyle(idx, "Curved")
result["made"] = made
result["arranged"] = {p["key"]: p["arrange"] in points for p in PLAN["pieces"]}
result["sewn"] = [bool(pattern_api.AddSeamlinePairGroup(made[s["a"][0]], s["a"][1], made[s["b"][0]], s["b"][1], s["a"][2], s["b"][2]))
                  for s in PLAN["seams"]]
FAB = r"C:\\Users\\Public\\Documents\\MarvelousDesigner\\New Assets\\Fabric"
# THE CLOTH, its physics only: a jumper's low-gauge knit for the shell, rib knit for the welt, cuffs and neckband
fabrics = {}
for name, f in (("knit", %(fabric)r), ("rib", "V2_Cut_Sew_Knit_Rib_1.zfab")):
    path = os.path.join(FAB, f)
    if os.path.isfile(path):
        fabrics[name] = fabric_api.AddFabric(path)
for p in PLAN["pieces"]:
    if p.get("fabric") in fabrics:
        fabric_api.AssignFabricToPattern(fabrics[p["fabric"]], made[p["key"]], 1)
result["fabrics"] = fabrics
pattern_api.SetParticleDistanceOfPatterns(20.0)
result["settled20"] = bool(utility_api.Simulate(%(steps)d))
pattern_api.SetParticleDistanceOfPatterns(10.0)
# the bands finer, 6 mm, as the skill orders for bands, cuffs and collars
for p in PLAN["pieces"]:
    if p.get("fabric") == "rib":
        pattern_api.SetParticleDistanceOfPattern(made[p["key"]], 6.0)
result["settled10"] = bool(utility_api.Simulate(200))
# Fitting last (utility_api.SetSimulationQuality(quality, mode): 2 Fitting, 0 CPU; drape 23 gave one argument and
# was refused)
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
result["exported"] = export_api.ExportOBJ(os.path.join(OUT, "jumper.obj"), eo)
result["zprj"] = export_api.ExportZPrj(os.path.join(OUT, "jumper.zprj"))
log("jumper shell made, sewn and draped")
'''


def main(argv):
    src, job = argv[0], argv[1]
    opt = lambda n, d: float(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
    out = argv[argv.index("--out") + 1] if "--out" in argv else r"F:\LedgerTools\garments\tom\jumper\drape"
    # --neck-depth and --body-length (30 October, drape j2): the cut's two lengths from the shoulder's high point as
    # flags, for a block drafted with that point measured on the full body (the first block's measures took it from
    # MH_TomL1_Body.fbx, which has no neck, about 61 mm low: its shoulder slope came out negative, FreeSewing drew the
    # shoulder flat, and drape j1's front rose to the neck and its armholes sat high)
    p = plan(load(src), opt("--sleeve-shorten", SLEEVE_SHORTEN), opt("--neck-depth", NECK_DEPTH), opt("--body-length", BODY_LENGTH))
    open(job, "w", encoding="utf-8").write(JOB % {
        "src": src, "plan": json.dumps(p), "out": out, "steps": int(opt("--steps", 400)), "fabric": FABRIC,
        # the straight-elbowed drape body, as the jacket's later drapes (the skill, step 2)
        "avt": argv[argv.index("--avatar") + 1] if "--avatar" in argv else r"F:\LedgerTools\garments\tom\MH_TomL1_straight.avt",
        "sleeve_pos": [int(v) for v in argv[argv.index("--sleeve-position") + 1].split(",")] if "--sleeve-position" in argv else None,
        "cuff_pos": [int(v) for v in argv[argv.index("--cuff-position") + 1].split(",")] if "--cuff-position" in argv else None})
    json.dump(p, open(job[:-3] + ".plan.json", "w", encoding="utf-8"), indent=1)
    print("jumper: %d pieces, %d seams -> %s" % (len(p["pieces"]), len(p["seams"]), job))
    for q in p["pieces"]:
        print("  %-8s %3d points  on %s" % (q["key"], len(q["points"]), q["arrange"]))


def selftest():
    import math
    ok = []
    src = r"F:\LedgerTools\garments\tom\jumper\pattern\brian-jumper.json"
    if not os.path.isfile(src):
        print("jumper selftest: passed=0/0 failed=0 (no pattern on this machine)")
        return 0
    p = plan(load(src))
    keys = [q["key"] for q in p["pieces"]]
    ok.append(keys == ["front", "back", "sleeveR", "sleeveL", "weltFront", "weltBack", "cuffR", "cuffL", "neckband"] and len(p["seams"]) == 21)
    pieces = build(load(src))
    E = lambda key, a, b: next(seg for seg, x, y in pieces[key] if {x, y} == {a, b})  # noqa: E731
    L = lambda seg: sum(math.dist(seg[k], seg[k + 1]) for k in range(len(seg) - 1))  # noqa: E731
    # every shell seam's two edges within 3% of each other's length (the cap eases into the armhole, a little longer);
    # a rib piece sewn to the shell draws it in by its cut (welt 0.90, neckband 0.92, cuff the wrist against the
    # sleeve's end, about 0.83); a piece's own closing seam matches itself
    ratios = []
    for (pa, a0, a1), (pb, b0, b1) in seams():
        r = L(E(pa, a0, a1)) / L(E(pb, b0, b1))
        ratios.append(r)
        rib_to_shell = pa.startswith(RIB) and not pb.startswith(RIB)
        ok.append(0.80 <= r <= 0.95 if rib_to_shell else 0.97 <= r <= 1.10)
    # the front's neck at its depth, the hem at the body's length (y up, the high point at 0)
    front = pieces["front"]
    ys = [y for seg, _, _ in front for _, y in seg]
    ok.append(abs(-min(ys) - BODY_LENGTH) < 1.0)
    cf_neck = min((y for seg, a, b in front if {a, b} == {"hpsR", "hpsL"} for x, y in seg if abs(x) < 1.0), default=None)
    ok.append(cf_neck is not None and abs(-cf_neck - NECK_DEPTH) < 1.5)
    # the neckband passes his head: at rest at least 14.5 in round, so at the knit's 50% stretch his 22 in head goes
    # through (JUMPER-2026-09-30, the crew neck [K2])
    band = sum(L(seg) for seg, a, b in pieces["neckband"] if b in ("nbFrontR", "nbBackL"))
    ok.append(band >= 14.5 * 25.4)
    print("jumper selftest: neckband %.0f mm round at rest (at least %.0f)" % (band, 14.5 * 25.4))
    print("jumper selftest: passed=%d/%d failed=%d (seam ratios %s)" % (
        sum(ok), len(ok), len(ok) - sum(ok), ", ".join("%.3f" % r for r in ratios)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(selftest() if "--selftest" in a else main(a))
