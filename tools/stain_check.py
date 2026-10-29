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


def project(cam, p, w=1920, h=1080):
    """Unreal's camera: cam = (x, y, z cm, pitch, yaw, horizontal fov degrees); p in Unreal cm. Pixel (u, v), or None behind."""
    import math
    cx, cy, cz, pitch, yaw, fov = cam
    th, ps = math.radians(pitch), math.radians(yaw)
    f = (math.cos(th) * math.cos(ps), math.cos(th) * math.sin(ps), math.sin(th))
    r = (-math.sin(ps), math.cos(ps), 0.0)
    u = (-math.sin(th) * math.cos(ps), -math.sin(th) * math.sin(ps), math.cos(th))
    d = (p[0] - cx, p[1] - cy, p[2] - cz)
    depth = sum(a * b for a, b in zip(d, f))
    if depth <= 1.0:
        return None
    k = (w / 2.0) / math.tan(math.radians(fov) / 2.0)
    return (w / 2.0 + k * sum(a * b for a, b in zip(d, r)) / depth, h / 2.0 - k * sum(a * b for a, b in zip(d, u)) / depth)


def footprint(d, inner=0.6):
    """The middle `inner` of a mark's rectangle, its four corners in Unreal cm (VignetteShot.cpp SpawnWear's axes:
    a wall mark's width runs along the wall, its height up; a ground mark's width along its yaw)."""
    import math
    a = math.radians(d["yaw_deg"])
    c = (d["x_m"] * 100.0, d["z_m"] * 100.0, d["y_m"] * 100.0)
    hw, hh = d["w_m"] * 50.0 * inner, d["h_m"] * 50.0 * inner
    if d["pitch_deg"] > 45.0:
        along, across = (math.cos(a), math.sin(a), 0.0), (-math.sin(a), math.cos(a), 0.0)
    else:
        along, across = (math.cos(a), math.sin(a), 0.0), (0.0, 0.0, 1.0)
    return [tuple(c[i] + sa * hw * along[i] + sb * hh * across[i] for i in range(3)) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def measure_marks(rough_with, rough_without, base_with, base_without, cam, marks, min_pixels=40):
    """Per mark of the wear file: the pixels inside its projected middle, measured at their strongest tenth."""
    from PIL import Image, ImageDraw
    h, w = rough_with.shape[:2]
    d_r = srgb_to_linear(rough_with[..., 0]) - srgb_to_linear(rough_without[..., 0])
    bw, bo = srgb_to_linear(base_with).mean(axis=2), srgb_to_linear(base_without).mean(axis=2)
    out = []
    for k, m in enumerate(marks):
        pts = [project(cam, p, w, h) for p in footprint(m)]
        row = {"mark": k, "kind": m["kind"], "picture": m["picture"].split("/")[-1], "at": [m["x_m"], m["y_m"], m["z_m"]]}
        if any(p is None for p in pts):
            out.append(dict(row, seen=False, why="behind the camera"))
            continue
        img = Image.new("L", (w, h), 0)
        ImageDraw.Draw(img).polygon(pts, fill=1)
        inside = np.asarray(img, dtype=bool)
        if inside.sum() < min_pixels:
            out.append(dict(row, seen=False, why="%d px on screen" % inside.sum()))
            continue
        strength = np.abs(d_r[inside])
        top = strength >= np.quantile(strength, 0.9)
        dr = float(np.median(d_r[inside][top]))
        darken = float(1.0 - np.median(bw[inside][top] / np.maximum(bo[inside][top], 1e-4)))
        out.append(dict(row, seen=True, pixels=int(inside.sum()), rough_change=round(dr, 3), darkens=round(darken, 3),
                        ok=abs(dr) >= ROUGH_MIN and darken <= DARKEN_MAX))
    return out


def run_marks(with_dir, without_dir, cam, wear_file, on="mickeys_room"):
    marks = [d for d in json.load(open(wear_file, encoding="utf-8"))["decals"] if d["on"] == on]
    rows = measure_marks(load(os.path.join(with_dir, "roughness.png")), load(os.path.join(without_dir, "roughness.png")),
                         load(os.path.join(with_dir, "basecolor.png")), load(os.path.join(without_dir, "basecolor.png")), cam, marks)
    for r in rows:
        if not r["seen"]:
            continue
        print("stainMark %2d %-6s %-16s %d px: roughness %+.3f, base colour %s %.0f%% %s" % (
            r["mark"], r["kind"], r["picture"], r["pixels"], r["rough_change"], "darker" if r["darkens"] >= 0 else "lighter",
            abs(r["darkens"]) * 100, "PASS" if r["ok"] else "FAIL"))
    seen = [r for r in rows if r["seen"]]
    ok = sum(r["ok"] for r in seen)
    print("stainCheck marks=%d seen=%d passed=%d failed=%d" % (len(rows), len(seen), ok, len(seen) - ok))
    with open(os.path.join(with_dir, "stain-marks.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=1)
    return 0 if seen and ok == len(seen) else 1


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
    cam = (0.0, 0.0, 0.0, 0.0, 0.0, 90.0)
    c = project(cam, (500.0, 0.0, 0.0))
    check("a point dead ahead lands mid-screen", abs(c[0] - 960) < 1e-6 and abs(c[1] - 540) < 1e-6)
    r = project(cam, (500.0, 500.0, 100.0))
    check("to the right (+y) is right, up (+z) is up, 45 degrees at the screen's edge", abs(r[0] - 1920) < 1e-6 and r[1] < 540)
    check("behind the camera is not drawn", project(cam, (-100.0, 0.0, 0.0)) is None)
    fp = footprint({"x_m": 8.65, "y_m": 1.2, "z_m": 6.0, "w_m": 0.5, "h_m": 0.4, "yaw_deg": 270.0, "pitch_deg": 0.0}, inner=1.0)
    check("a mark on the notice wall stays on it, its width along the wall and its height up",
          all(abs(p[0] - 865.0) < 1e-6 for p in fp) and abs(max(p[1] for p in fp) - min(p[1] for p in fp) - 50.0) < 1e-6
          and abs(max(p[2] for p in fp) - min(p[2] for p in fp) - 40.0) < 1e-6)
    print("stain_check selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    if "--camera" in sys.argv:
        cam = tuple(float(x) for x in sys.argv[sys.argv.index("--camera") + 1].split(","))
        wear = sys.argv[sys.argv.index("--wear") + 1] if "--wear" in sys.argv else os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "production", "specs", "street-wear.json")
        sys.exit(run_marks(sys.argv[1], sys.argv[2], cam, wear))
    sys.exit(run(sys.argv[1], sys.argv[2]))
