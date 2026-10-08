"""The street's brick and maroon fascias in the hook frame, against target.json.

    python measure_brick.py                 the two frames named in target.json
    python measure_brick.py FRAME.png ...   any 2560 x 1440 hook frame
    python measure_brick.py --sheet         also the Hook sheet's own regions
    python measure_brick.py --photos        also the photographs' walls (F: drive)

For each region: the pooled sRGB mean, HSV saturation of that mean (judged),
the mean of per-pixel saturation, the hue of the mean (judged), V, the pale
joint share, and PASS or FAIL against the region's bands. Exit code 0 only if
every frame passes. Definitions: target.json "metric". Needs Pillow and numpy.
"""
import colorsys
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageCms

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = json.load(open(os.path.join(HERE, "target.json"), encoding="utf-8"))
FRAME_SIZE = (2560, 1440)


def load(path):
    """RGB array in sRGB; an embedded ICC profile (e.g. Display P3) is converted."""
    im = Image.open(path)
    icc = im.info.get("icc_profile")
    if icc:
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        if "srgb" not in ImageCms.getProfileDescription(src).lower().replace(" ", ""):
            im = ImageCms.profileToProfile(im.convert("RGB"), src, ImageCms.createProfile("sRGB"), outputMode="RGB")
    return np.asarray(im.convert("RGB")).astype(np.float64)


def measure(a, boxes):
    px = np.concatenate([a[y0:y1, x0:x1].reshape(-1, 3) for x0, y0, x1, y1 in boxes])
    mx, mn = px.max(1), px.min(1)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0.0)
    m = px.mean(0)
    h, sm, v = colorsys.rgb_to_hsv(*(m / 255.0))
    pale = s < 0.6 * np.median(s)
    b = px[~pale].mean(0)
    return {"n": len(px), "mean": m, "S": sm, "meanS": s.mean(), "hue": h * 360.0, "V": v,
            "pale": pale.mean(), "faceS": (b.max() - b.min()) / max(b.max(), 1e-9)}


def in_band(x, band, wrap=False):
    lo, hi = band
    return (lo <= x <= hi) if (lo <= hi or not wrap) else (x >= lo or x <= hi)


def line(name, r, target=None):
    m = r["mean"]
    out = (f"  {name:20s} {m[0]:5.1f}/{m[1]:5.1f}/{m[2]:5.1f}  S {r['S']:.3f}  meanS {r['meanS']:.3f}  "
           f"hue {r['hue']:5.1f}  V {r['V']:.3f}  joints {100 * r['pale']:4.1f}%  faceS {r['faceS']:.3f}  n {r['n']}")
    if target is None:
        return out, True
    okS = in_band(r["S"], target["S_of_mean"])
    okH = in_band(r["hue"], target["hue_deg"], wrap=True)
    h, s, v = target["hue_deg"], target["S_of_mean"], r["V"]
    hc = ((h[0] + h[1]) / 2.0) if h[0] <= h[1] else ((h[0] + h[1] + 360) / 2.0) % 360
    want = np.array(colorsys.hsv_to_rgb(hc / 360.0, (s[0] + s[1]) / 2.0, v)) * 255
    out += (f"\n  {'':20s} target S {s[0]:.2f}-{s[1]:.2f} {'ok' if okS else 'OUT'}, hue {h[0]:g}-{h[1]:g} "
            f"{'ok' if okH else 'OUT'}; at this V the target reads {want[0]:.0f}/{want[1]:.0f}/{want[2]:.0f}"
            f"  -> {'PASS' if okS and okH else 'FAIL'}")
    return out, okS and okH


def frame(path):
    a = load(path)
    h, w, _ = a.shape
    sx, sy = w / FRAME_SIZE[0], h / FRAME_SIZE[1]
    print(f"\n{path}  ({w} x {h})")
    if (w, h) != FRAME_SIZE:
        print(f"  NOTE: not {FRAME_SIZE[0]} x {FRAME_SIZE[1]}; boxes scaled by {sx:.3f} x {sy:.3f}")
    allok = True
    for name, reg in TARGET["regions"].items():
        boxes = [(round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy)) for x0, y0, x1, y1 in reg["boxes"]]
        text, ok = line(name, measure(a, boxes), reg["target"])
        print(text)
        allok &= ok
    print(f"  FRAME {'PASSES' if allok else 'FAILS'}")
    return allok


def sheet():
    src = TARGET["sources"]["sheet"]
    a = load(src["file"])
    print(f"\nTHE HOOK SHEET  {src['file']}")
    for k in ("near", "parade", "far", "right_cottage"):
        print(line(k, measure(a, src[k]))[0])
    for k, boxes in src["maroon_front"].items():
        print(line("maroon " + k, measure(a, boxes))[0])


def photos():
    src = TARGET["sources"]["photographs"]
    folder = src["folder"].split(" ")[0]
    print("\nTHE PHOTOGRAPHS")
    for group in ("walls", "dressings"):
        for f, parts in src[group].items():
            p = os.path.join(folder, f)
            if not os.path.exists(p):
                print(f"  missing {p}")
                continue
            a = load(p)
            print(f" {f}  ({parts['light']})")
            for k, boxes in parts.items():
                if k != "light":
                    print(line(k, measure(a, boxes))[0])


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    frames = args or list(TARGET["frames"].values())
    if "--sheet" in sys.argv:
        sheet()
    if "--photos" in sys.argv:
        photos()
    ok = all([frame(p) for p in frames])
    sys.exit(0 if ok else 1)
