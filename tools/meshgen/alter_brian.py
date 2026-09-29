"""Alterations to a drafted Brian pattern that FreeSewing's options do not make, written as a new pattern file.

    python tools/meshgen/alter_brian.py IN.json OUT.json [--back-tuck MM]

WHY, 29 September (the clothing session; the first blind review of Ron's
donkey jacket: 'a horizontal roll of sagging wool sits just below the yoke').
Brian cuts the back and the front the same length. On a big-bellied man the
belly takes up length at the front, so the back has length to spare, which
folds across under the shoulder blades. A tailor shortens the back above the
armhole for such a figure: --back-tuck takes MM out of the back between the
neck and the armhole line, most at the neck and shoulder, none at the
armhole, so the side seams still match. Every point and path of the back is
moved; nothing else changes.
"""
import json
import sys

args = sys.argv[1:]
SRC, OUT = args[0], args[1]
TUCK = float(args[args.index("--back-tuck") + 1]) if "--back-tuck" in args else 30.0

p = json.load(open(SRC, encoding="utf-8"))
back = p["parts"]["brian.back"]
y_arm = back["points"]["armhole"][1]


def move(xy):
    x, y = xy
    if y < y_arm:
        y = y + TUCK * (1.0 - max(0.0, y) / y_arm)
    return [round(x, 2), round(y, 2)]


for name, pt in back["points"].items():
    back["points"][name] = move(pt)
for name, path in back["paths"].items():
    path["points"] = [move(q) for q in path["points"]]
p.setdefault("alterations", []).append({"backTuckMm": TUCK, "above": round(y_arm, 1)})
json.dump(p, open(OUT, "w", encoding="utf-8"), indent=1)
print("altered: back shortened %.0f mm above its armhole line (y %.0f)" % (TUCK, y_arm))
