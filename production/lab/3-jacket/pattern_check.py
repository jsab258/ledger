"""The flat pattern's automatic checks, beyond the worked values and Plate 16:
every pair of edges that is sewn together, measured, with the ease the book or
the trade expects. Writes checks/pattern_<tag>.json.

    python pattern_check.py ron
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def length(P):
    P = np.asarray(P, float)
    return float(np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1)))


def stretch(pc, name):
    O = np.array(pc["outline_in"])
    a, b = pc["stretches"][name]
    return O[a:b + 1]


def main(tag):
    d = json.load(open(os.path.join(HERE, "pattern_%s.json" % tag)))
    pcs = d["pieces"]
    L = {}
    for piece, pc in pcs.items():
        for name in pc["stretches"]:
            L[name] = length(stretch(pc, name))
    # the forepart's scye joins its two parts across the fish's mouth; the armhole is back scye + front scye
    fore_scye = L["scye_low"] + L["scye_high"]
    armhole = L["back_scye"] + fore_scye
    collar_line = L["back_neck"] + L["neck"] + float(np.linalg.norm(np.array(d["collar_points"]["notch"]) - np.array(d["points"]["NN"])))
    checks = [
        # name, sewn edge a, edge b, expected (b - a) range in inches, source
        ("side seam", L["back_side"], L["fore_side"], (-0.75, 0.75), "the two side seams meet; the plate draws them within about 1/2 in"),
        ("shoulder", L["front_shoulder"], L["back_shoulder"], (0.0, 0.5), "back shoulder 1/4 in longer than the front's X (p. 54), eased in"),
        ("fish", L["fish_a"], L["fish_b"], (-0.25, 0.25), "a dart's two legs are equal"),
        ("forearm seam", L["forearm_t"], L["forearm_u"], (-0.25, 0.25), "top and under sleeve share the forearm line (Plate 46)"),
        ("hind-arm seam", L["hind_u"], L["hind_t"], (-0.5, 1.0), "the top sleeve's hind arm is eased onto the under sleeve's at the elbow"),
        ("sleeve head", armhole, L["head"] + L["under_top"], (0.5, 3.5), "sleeve head eased into the scye; Thornton's own example carries about 3 in (head 12 in on a 9 in upper scye)"),
        ("collar to neck", collar_line, L["collar_neck"], (-0.5, 0.25), "'the collar should measure the same as the neck of the coat' (p. 14)"),
    ]
    out = {"tag": tag, "lengths_in": {k: round(v, 3) for k, v in L.items()}, "armhole_in": round(armhole, 3),
           "checks": []}
    ok_all = True
    for name, a, b, (lo, hi), why in checks:
        diff = b - a
        ok = lo <= diff <= hi
        ok_all &= ok
        out["checks"].append({"seam": name, "a_in": round(a, 3), "b_in": round(b, 3), "b_minus_a": round(diff, 3),
                              "allowed": [lo, hi], "ok": bool(ok), "why": why})
    out["pass"] = bool(ok_all)
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "checks", "pattern_%s.json" % tag), "w"), indent=1)
    for c in out["checks"]:
        print("%-15s %7.2f vs %7.2f  diff %+6.2f  allowed %s  %s" % (c["seam"], c["a_in"], c["b_in"], c["b_minus_a"], c["allowed"], "ok" if c["ok"] else "FAIL"))
    print("PASS" if ok_all else "FAIL")
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ron")
