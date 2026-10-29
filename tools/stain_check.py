"""THE LAYER RECIPE'S CHECK, MEASURED IN THE GAME (his order D11, the look; production/research/street-wear/
MAFIA-WEAR-2026-10-28.md, "The layer recipe", step 1: "a stain differs from its wall by at least 0.1 in the roughness
view and darkens the base colour by at most 40%").

    python tools/stain_check.py WITH_DIR WITHOUT_DIR      # each holding roughness.png and basecolor.png
    python tools/stain_check.py --selftest

Two pictures of the same view through the game's camera, one with the marks and one without (-NoOfficeWear), in
Unreal's roughness and base-colour buffer views. Where the two differ is where a mark lies: each mark found (a
connected patch of changed pixels, at least MIN_PIXELS) is measured at its strongest tenth, so a mark's soft edge
does not hide its middle. The roughness view's pixels are read as the base colour's are, sRGB-encoded (Unreal shows
its buffers through the same output; unverified for roughness, so the raw difference is printed beside it).

Passes when every mark found changes roughness by at least 0.1 and darkens its base colour by at most 40%
(a mark that lightens, the pale oblongs, is reported and not failed on darkening).
"""
import json
import os
import sys

import numpy as np

MIN_PIXELS = 150          # smaller patches are noise or a mark seen edge on
CHANGED = 0.02            # a linear roughness change below this is not a mark
ROUGH_MIN, DARKEN_MAX = 0.1, 0.40


def srgb_to_linear(v):
    v = np.asarray(v, dtype=float)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def load(path):
    from PIL import Image
    return np.asarray(Image.open(path).convert("RGB"), dtype=float) / 255.0


def measure(rough_with, rough_without, base_with, base_without):
    """Per mark: its pixels, roughness change (linear and raw display) and base-colour change, at its strongest tenth."""
    from scipy import ndimage
    rw, ro = srgb_to_linear(rough_with[..., 0]), srgb_to_linear(rough_without[..., 0])
    d = rw - ro
    labels, n = ndimage.label(np.abs(d) > CHANGED)
    bw = srgb_to_linear(base_with).mean(axis=2)
    bo = srgb_to_linear(base_without).mean(axis=2)
    marks = []
    for k in range(1, n + 1):
        m = labels == k
        if m.sum() < MIN_PIXELS:
            continue
        strength = np.abs(d[m])
        top = strength >= np.quantile(strength, 0.9)
        dr = float(np.median(d[m][top]))
        raw = float(np.median((rough_with[..., 0] - rough_without[..., 0])[m][top]))
        ratio = bw[m][top] / np.maximum(bo[m][top], 1e-4)
        darken = float(1.0 - np.median(ratio))
        ys, xs = np.nonzero(m)
        marks.append({"pixels": int(m.sum()), "centre": [int(xs.mean()), int(ys.mean())], "rough_change": round(dr, 3),
                      "rough_change_raw": round(raw, 3), "darkens": round(darken, 3),
                      "ok": abs(dr) >= ROUGH_MIN and darken <= DARKEN_MAX})
    return marks


def run(with_dir, without_dir):
    marks = measure(load(os.path.join(with_dir, "roughness.png")), load(os.path.join(without_dir, "roughness.png")),
                    load(os.path.join(with_dir, "basecolor.png")), load(os.path.join(without_dir, "basecolor.png")))
    for m in marks:
        print("stainMark at %s: %d px, roughness %+.3f (raw %+.3f), base colour %s %.0f%% %s" % (
            m["centre"], m["pixels"], m["rough_change"], m["rough_change_raw"], "darker" if m["darkens"] >= 0 else "lighter",
            abs(m["darkens"]) * 100, "PASS" if m["ok"] else "FAIL"))
    ok = sum(m["ok"] for m in marks)
    print("stainCheck marks=%d passed=%d failed=%d" % (len(marks), ok, len(marks) - ok))
    with open(os.path.join(with_dir, "stain-check.json"), "w", encoding="utf-8") as fh:
        json.dump(marks, fh, indent=1)
    return 0 if marks and ok == len(marks) else 1


def selftest():
    passed = failed = 0

    def check(name, cond):
        nonlocal passed, failed
        passed, failed = (passed + 1, failed) if cond else (passed, failed + 1)
        if not cond:
            print("stain_check selftest FAIL " + name)

    def enc(v):
        v = np.asarray(v, dtype=float)
        return np.where(v <= 0.0031308, v * 12.92, 1.055 * v ** (1 / 2.4) - 0.055)
    h = w = 64
    wall_r, wall_b = np.full((h, w, 3), 0.85), np.full((h, w, 3), 0.30)
    r1, b1 = wall_r.copy(), wall_b.copy()
    r1[10:30, 10:30] = 0.70            # a stain 0.15 smoother, darkening 20%
    b1[10:30, 10:30] = 0.24
    r1[40:60, 40:60] = 0.80            # a faint one: 0.05 smoother, darkening 50%
    b1[40:60, 40:60] = 0.15
    m = measure(enc(r1), enc(wall_r), enc(b1), enc(wall_b))
    check("two marks found", len(m) == 2)
    a = min(m, key=lambda x: x["centre"][1])
    b = max(m, key=lambda x: x["centre"][1])
    check("the first passes: 0.15 smoother, 20% darker", a["ok"] and abs(a["rough_change"] + 0.15) < 0.01 and abs(a["darkens"] - 0.20) < 0.01)
    check("the second fails on both counts", not b["ok"] and abs(b["rough_change"]) < 0.1 and b["darkens"] > 0.4)
    check("an unchanged pair finds nothing", measure(enc(wall_r), enc(wall_r), enc(wall_b), enc(wall_b)) == [])
    print("stain_check selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(run(sys.argv[1], sys.argv[2]))
