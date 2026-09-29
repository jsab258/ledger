"""The pieces of a jacket drafted from FreeSewing's Brian block, as flat meshes with their seam lines, for Blender.

Used by sew_donkey.py (the drape, at about 12 mm) and finish_donkey.py (the
game's simulation mesh, at about 25 mm, mapped onto the drape through the
flat pattern). Both cut the pieces the same way, so a seam's points lie at
the same fractions of its length on both sides, and the coarse mesh's seams
fall on the fine mesh's.

The pieces (mm, y down, as FreeSewing draws): the back (half, on the fold at
centre back), the front (half, sewn to its mirror at centre front for now),
the one-piece sleeve, its cap split between the back and front armholes in
proportion to their lengths. The flat layout (UVs, m) puts the back at u 0
(its right half mirrored to u < 0), the fronts at u +1 and -1, the sleeves at
u +2 and -2, v = -y.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tailor  # noqa: E402

LAYOUT = {("back", 1): (0.0, 0.0), ("back", -1): (0.0, 0.0), ("front", 1): (1.0, 0.0), ("front", -1): (-1.0, 0.0),
          ("sleeve", 1): (2.0, 0.0), ("sleeve", -1): (-2.0, 0.0)}


def pieces(path, edge):
    """Everything about the pattern the sewing needs: segments B, F, S (polylines, mm), the pieces' flat meshes,
    each piece's segment indices, the seam point counts, and the pattern's named points."""
    pattern = json.load(open(path, encoding="utf-8"))
    back, front, sleeve = (pattern["parts"][k] for k in ("brian.back", "brian.front", "library.sleeve"))
    bp, fp, sp = back["points"], front["points"], sleeve["points"]
    back_out = tailor.closed(back["paths"]["seam"]["points"])
    front_out = tailor.closed(front["paths"]["seam"]["points"])
    sleeve_out = tailor.closed(sleeve["paths"]["seam"]["points"])
    seg, L = tailor.seg, tailor.length
    B = {n: seg(back_out, bp[a], bp[b]) for n, (a, b) in {
        "fold": ("cbNeck", "cbHem"), "hem": ("cbHem", "hem"), "side": ("hem", "armhole"),
        "armhole": ("armhole", "shoulder"), "shoulder": ("shoulder", "neck"), "neckline": ("neck", "cbNeck")}.items()}
    F = {n: seg(front_out, fp[a], fp[b]) for n, (a, b) in {
        "cf": ("cfNeck", "cfHem"), "hem": ("cfHem", "hem"), "side": ("hem", "armhole"),
        "armhole": ("armhole", "shoulder"), "shoulder": ("shoulder", "neck"), "neckline": ("neck", "cfNeck")}.items()}
    cap = seg(sleeve_out, sp["bicepsLeft"], sp["bicepsRight"])
    if min(y for _, y in cap) > -10:                       # took the wrist way round
        cap = list(reversed(seg(sleeve_out, sp["bicepsRight"], sp["bicepsLeft"])))
    cap_back, cap_front = tailor.split_at(cap, L(B["armhole"]) / (L(B["armhole"]) + L(F["armhole"])) * L(cap))
    S = {"capBack": cap_back, "capFront": cap_front,
         "right": seg(sleeve_out, sp["bicepsRight"], sp["wristRight"]), "cuff": seg(sleeve_out, sp["wristRight"], sp["wristLeft"]),
         "left": seg(sleeve_out, sp["wristLeft"], sp["bicepsLeft"])}

    def steps(*polys):
        return max(2, round(sum(L(p) for p in polys) / len(polys) / edge))

    N = {"side": steps(B["side"], F["side"]), "shoulder": steps(B["shoulder"], F["shoulder"]),
         "armB": steps(B["armhole"], S["capBack"]), "armF": steps(F["armhole"], S["capFront"]),
         "under": steps(S["right"], S["left"]), "cf": steps(F["cf"]), "bfold": steps(B["fold"]), "bhem": steps(B["hem"]),
         "bneck": steps(B["neckline"]), "fhem": steps(F["hem"]), "fneck": steps(F["neckline"]), "cuff": steps(S["cuff"])}
    bb, b_idx = tailor.loop([("fold", B["fold"], N["bfold"]), ("hem", B["hem"], N["bhem"]), ("side", B["side"], N["side"]),
                             ("armhole", B["armhole"], N["armB"]), ("shoulder", B["shoulder"], N["shoulder"]),
                             ("neckline", B["neckline"], N["bneck"])])
    fb, f_idx = tailor.loop([("cf", F["cf"], N["cf"]), ("hem", F["hem"], N["fhem"]), ("side", F["side"], N["side"]),
                             ("armhole", F["armhole"], N["armF"]), ("shoulder", F["shoulder"], N["shoulder"]),
                             ("neckline", F["neckline"], N["fneck"])])
    sb, s_idx = tailor.loop([("capBack", S["capBack"], N["armB"]), ("capFront", S["capFront"], N["armF"]),
                             ("right", S["right"], N["under"]), ("cuff", S["cuff"], N["cuff"]), ("left", S["left"], N["under"])])
    return {
        "pattern": pattern, "B": B, "F": F, "S": S, "cap": cap, "N": N, "points": {"back": bp, "front": fp, "sleeve": sp},
        "pieces": {"back": tailor.panel(bb, edge), "front": tailor.panel(fb, edge), "sleeve": tailor.panel(sb, edge)},
        "idx": {"back": b_idx, "front": f_idx, "sleeve": s_idx},
        "lengths": {"backArmhole": round(L(B["armhole"])), "frontArmhole": round(L(F["armhole"])), "cap": round(L(cap)),
                    "capEaseMm": round(L(cap) - L(B["armhole"]) - L(F["armhole"])), "side": round(L(B["side"]))},
    }
