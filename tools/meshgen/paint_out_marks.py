#!/usr/bin/env python3
"""A brand mark painted out of a scanned asset's texture set: each masked area filled from its own edge, its grain taken
from a clean patch of the same surface, every map of the set (colour, normal, occlusion, roughness, specular) alike.

    python tools/meshgen/paint_out_marks.py MARKS.json OUT_DIR      # MARKS.json: maps + marks, as below
    python tools/meshgen/paint_out_marks.py --selftest

WHY, 30 October 2026 (his ruling of that morning: CC BY 4.0 for clothes and their accessories, any visible brand mark
painted out). Tom's shoes come from a CC BY 4.0 photo scan of an old oxford whose insole carries the maker's woven
label and a printed code, and whose outsole carries the brand moulded in, a size badge and an ink stamp. No inpainting
library is installed here and none is needed for flat leather and rubber: the fill is the mask's edge diffused inward
(the low frequencies), plus the high frequencies of a clean patch of the same surface tiled by mirroring (the grain),
blended in through a feathered edge. The scanner's own copyright line in an unused corner of the texture is left: the
licence asks for its notice to be kept, and the credits carry it too.

MARKS.json: {"maps": {"albedo": PATH, "normal": PATH, ...}, "marks": [{"name": ..., "poly": [[x, y], ...] or
"rect": [x0, y0, x1, y1] or "circle": [cx, cy, r], "patch": [x0, y0, x1, y1], "feather": px}]} in the maps' pixels;
each mark is placed on the map that shows it best (moulded letters show most in the normal map: 30 October, the
outsole's colour hid two lines of moulded print and the scanner's own name that its normal map showed). Normal maps
(named "normal") are renormalised after the fill. OUT_DIR gets each map under its own file name and marks.report.json.
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw


def mask_of(mark, w, h):
    m = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(m)
    if "poly" in mark:
        d.polygon([tuple(p) for p in mark["poly"]], fill=255)
    elif "rect" in mark:
        d.rectangle(mark["rect"], fill=255)
    else:
        cx, cy, r = mark["circle"]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    return np.asarray(m) > 0


def blur(a, s):
    """A separable box blur three times over (close to a Gaussian of about s), per channel."""
    r = max(1, int(s))
    out = a.astype(np.float64)
    for _ in range(3):
        for ax in (0, 1):
            c = np.cumsum(np.pad(out, [(r + 1, r) if i == ax else (0, 0) for i in range(out.ndim)], mode="edge"), axis=ax)
            n = out.shape[ax]
            hi = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=ax)
            lo = np.take(c, np.arange(0, n), axis=ax)
            out = (hi - lo) / (2 * r + 1)
    return out


def diffuse(img, hole, iters=400):
    """The hole filled by repeated averaging of its four neighbours, its edge held (a Laplace fill), on a 4x smaller
    copy for speed and then refined at full size."""
    def solve(a, m, n):
        a = a.copy()
        ys, xs = np.nonzero(m)
        if len(ys) == 0:
            return a
        known = a[~m].mean(axis=0)
        a[m] = known
        for _ in range(n):
            p = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode="edge")
            avg = (p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) * 0.25
            a[m] = avg[m]
        return a
    h, w = hole.shape
    small = np.asarray(Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).resize((max(1, w // 4), max(1, h // 4)), Image.BILINEAR)).astype(np.float64)
    if small.ndim == 2:
        small = small[..., None]
    hs = np.asarray(Image.fromarray(hole.astype(np.uint8) * 255).resize((max(1, w // 4), max(1, h // 4)), Image.NEAREST)) > 0
    small = solve(small, hs, iters)
    up = np.stack([np.asarray(Image.fromarray(np.clip(small[..., c], 0, 255).astype(np.uint8)).resize((w, h), Image.BILINEAR))
                   for c in range(small.shape[2])], axis=-1).astype(np.float64)
    a = img.copy()
    a[hole] = up[hole]
    return solve(a, hole, 60)


def grain(patch, shape, s=6):
    """The patch's high frequencies (itself less its blur), tiled by mirroring to the shape, mean nil."""
    hf = patch - blur(patch, s)
    ph, pw = hf.shape[:2]
    tile = np.concatenate([np.concatenate([hf, hf[:, ::-1]], axis=1), np.concatenate([hf[::-1], hf[::-1, ::-1]], axis=1)], axis=0)
    reps = (shape[0] // (2 * ph) + 1, shape[1] // (2 * pw) + 1, 1)
    out = np.tile(tile, reps)[:shape[0], :shape[1]]
    return out - out.mean(axis=(0, 1))


def paint(img, mark, feather=6.0):
    h, w = img.shape[:2]
    hole = mask_of(mark, w, h)
    ys, xs = np.nonzero(hole)
    m = int(feather * 4) + 8
    y0, y1, x0, x1 = max(0, ys.min() - m), min(h, ys.max() + m), max(0, xs.min() - m), min(w, xs.max() + m)
    sub, sh = img[y0:y1, x0:x1].astype(np.float64), hole[y0:y1, x0:x1]
    grown = blur(sh.astype(np.float64)[..., None], feather)[..., 0] > 0.02     # the fill reaches past the mark's edge
    fill = diffuse(sub, grown)
    px0, py0, px1, py1 = mark["patch"]
    fill = fill + grain(img[py0:py1, px0:px1].astype(np.float64), sub.shape)
    # the mark wholly replaced, the blend feathering outward from its edge (inside it, nothing of the mark is kept)
    a = np.maximum(sh.astype(np.float64), np.clip(blur(sh.astype(np.float64)[..., None], feather)[..., 0] * 1.6, 0, 1))[..., None]
    out = img.copy().astype(np.float64)
    out[y0:y1, x0:x1] = sub * (1 - a) + fill * a
    return out, int(hole.sum())


def run(spec, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    rep = {"marks": [m["name"] for m in spec["marks"]], "maps": {}}
    for kind, path in spec["maps"].items():
        im = Image.open(path)
        mode = im.mode
        a = np.asarray(im.convert("RGB")).astype(np.float64)
        px = 0
        for mark in spec["marks"]:
            a, n = paint(a, mark, mark.get("feather", 6.0))
            px += n
        if kind == "normal":
            v = a / 127.5 - 1.0
            v /= np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-6)
            a = (v + 1.0) * 127.5
        res = Image.fromarray(np.clip(np.rint(a), 0, 255).astype(np.uint8))
        if mode == "L":
            res = res.convert("L")
        name = os.path.basename(path)
        res.save(os.path.join(out_dir, name), quality=97, subsampling=0)
        rep["maps"][kind] = {"file": name, "pixels_painted": px}
    json.dump(rep, open(os.path.join(out_dir, "marks.report.json"), "w"), indent=1)
    print("paint-out " + json.dumps(rep))


def selftest():
    ok = 0
    rng = np.random.default_rng(1)
    base = np.full((200, 200, 3), 120.0) + rng.normal(0, 8, (200, 200, 3))
    marked = base.copy()
    marked[80:120, 80:120] = 250.0
    mark = {"name": "t", "rect": [80, 80, 119, 119], "patch": [10, 10, 60, 60]}
    out, n = paint(marked, mark)
    ok += n == 1600
    ok += abs(out[80:120, 80:120].mean() - 120.0) < 6.0                       # the mark gone, the tone the surround's
    ok += 3.0 < out[85:115, 85:115].std() < 14.0                              # grain kept, not a flat smear
    ok += float(np.abs(out[:40, :40] - marked[:40, :40]).max()) == 0.0        # far pixels untouched
    print("paint_out_marks selftest: passed=%d/4 failed=%d" % (ok, 4 - ok))
    return 0 if ok == 4 else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    run(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2])
