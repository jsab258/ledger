#!/usr/bin/env python3
"""THE STREET'S SURFACES AGAINST REAL VALUES, MEASURED IN THE GAME'S OWN BUFFERS (his note of 29 October, D11: "check
how bright the pavement, road and brick are ... against real values and real photographs of a wet overcast street").

    python tools/surface_values.py DIR BOXES.json      # DIR holds basecolor.png and lit.png of one view
    python tools/surface_values.py --selftest

WHY. production/research/street-wear/WET-OVERCAST-VALUES-2026-10-29.md (revised after its review) derived the road,
flags and brick at 2 to 8 times darker than real from the code's numbers alone; its first step for the work is to
measure them where the player sees them, in Unreal's base-colour view (the look method's check C6), and beside it the
lit picture against the photographs' bands. Every target here is that file's, and it stays their home.

HOW. Each named box (x0, y0, x1, y1 pixels, chosen on the picture and kept in BOXES.json beside the pictures, so the
reading can be repeated) is read in both pictures: the base colour as linear RGB and luminance (Rec. 709 weights; the
buffer view is sRGB-encoded, as tools/stain_check.py reads it), its middle half of values so an edge or a mark does
not pull it; the lit picture as sRGB levels. A box's kind (road, flags, kerb, brick) gives its bands.
"""
import json
import os
import sys

import numpy as np

# THE BANDS (WET-OVERCAST-VALUES-2026-10-29.md, "Target values" and its review's fix 3: wet base colour excludes the
# water's own reflection, which the game's film specular supplies). Base colour as linear luminance; lit as sRGB.
BANDS = {
    "road": {"base": (0.05, 0.06), "lit": (100, 186), "note": "aged asphalt, wet; lit 160 to 186 along the street, 100 to 110 looking down"},
    "flags": {"base": (0.11, 0.20), "lit": (100, 150), "note": "concrete flags, wet"},
    "kerb": {"base": (0.11, 0.20), "lit": (100, 150), "note": "as the flags (inferred in the research)"},
    "brick": {"base": (0.10, 0.20), "lit": (55, 130), "note": "red brick, dry walls; colour about (0.26, 0.10, 0.06)"},
}


def srgb_to_linear(v):
    v = np.asarray(v, dtype=float)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def middle(a):
    """The middle half of a box's values (per channel), so its edges and any mark do not pull the reading."""
    lo, hi = np.percentile(a, 25, axis=0), np.percentile(a, 75, axis=0)
    keep = np.all((a >= lo) & (a <= hi), axis=1)
    return a[keep] if keep.any() else a


def read(base, lit, box):
    x0, y0, x1, y1 = box
    b = middle(srgb_to_linear(base[y0:y1, x0:x1].reshape(-1, 3)))
    rgb = b.mean(axis=0)
    lum = float(rgb @ np.array([0.2126, 0.7152, 0.0722]))
    l = np.median(lit[y0:y1, x0:x1].reshape(-1, 3), axis=0) * 255.0
    return {"base_linear": [round(float(c), 4) for c in rgb], "base_luminance": round(lum, 4),
            "lit_srgb": [int(round(float(c))) for c in l]}


def judge(kind, r):
    band = BANDS[kind]
    lo, hi = band["base"]
    lit = float(np.mean(r["lit_srgb"]))
    return {"base_in_band": lo <= r["base_luminance"] <= hi, "base_factor_to_band": round(lo / r["base_luminance"], 2) if r["base_luminance"] > 0 else None,
            "lit_in_band": band["lit"][0] <= lit <= band["lit"][1]}


def load(path):
    from PIL import Image
    return np.asarray(Image.open(path).convert("RGB"), dtype=float) / 255.0


def run(d, boxes_path):
    boxes = json.load(open(boxes_path, encoding="utf-8"))
    base, lit = load(os.path.join(d, "basecolor.png")), load(os.path.join(d, "lit.png"))
    out = {}
    for name, b in boxes.items():
        kind = b["kind"]
        r = read(base, lit, b["box"])
        r.update(judge(kind, r))
        r["kind"] = kind
        out[name] = r
        print("surface %-14s %-5s base %.4f (band %.2f-%.2f, x%s to reach it) lit %s (band %d-%d)" % (
            name, kind, r["base_luminance"], BANDS[kind]["base"][0], BANDS[kind]["base"][1], r["base_factor_to_band"],
            r["lit_srgb"], BANDS[kind]["lit"][0], BANDS[kind]["lit"][1]))
    json.dump(out, open(os.path.join(d, "surface-values.json"), "w", encoding="utf-8"), indent=1)
    return 0


def selftest():
    ok = []
    v = srgb_to_linear(np.array([0.5]))[0]
    ok.append(abs(v - 0.214) < 0.001)
    base = np.full((10, 10, 3), 0.5)
    base[0, 0] = 1.0                                              # one bright pixel the middle half drops
    lit = np.full((10, 10, 3), 120 / 255.0)
    r = read(base, lit, (0, 0, 10, 10))
    ok.append(abs(r["base_luminance"] - 0.214) < 0.002 and r["lit_srgb"] == [120, 120, 120])
    j = judge("road", {"base_luminance": 0.012, "lit_srgb": [90, 90, 90]})
    ok.append(not j["base_in_band"] and abs(j["base_factor_to_band"] - 4.17) < 0.01 and not j["lit_in_band"])
    print("surface_values selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(selftest() if "--selftest" in a else run(a[0], a[1]))
