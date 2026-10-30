#!/usr/bin/env python3
"""A garment's packed map given real roughness variation: its drawn seams and thread a little smoother than the cloth,
and the cloth itself unevenly worn, the part ID (green) and metal (blue) left as they are.

    python tools/meshgen/packed_roughness.py PACKED.png DETAIL_NORMAL.png PLAIN_NORMAL.png OUT.png
            [--thread -0.07] [--wear 0.025] [--seed 1990]
    python tools/meshgen/packed_roughness.py --selftest

WHY, 30 October 2026 (his order D13, the asset checks on Tom's jeans): their packed map came out of the bake one flat
roughness (0.82 everywhere), which the checks rightly read as a placeholder; real denim is not uniform, its thread runs
smoother than the twill and its cloth wears unevenly. The drawn construction (tools/meshgen/garment_details.py) is found
where the detailed normal map leaves the plain bake's (more than 3 levels apart), and lowered by THREAD; the whole cloth
takes a soft, two-scale fade of WEAR either way, fixed by SEED so a rebuild draws the same.
"""
import sys

import numpy as np
from PIL import Image


def blur(a, r):
    out = a.astype(np.float64)
    for _ in range(3):
        for ax in (0, 1):
            c = np.cumsum(np.pad(out, [(r + 1, r) if i == ax else (0, 0) for i in range(out.ndim)], mode="wrap"), axis=ax)
            n = out.shape[ax]
            out = (np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=ax) - np.take(c, np.arange(0, n), axis=ax)) / (2 * r + 1)
    return out


def fade(shape, seed):
    """A soft two-scale field, mean nil, at most about 1 in size."""
    rng = np.random.default_rng(seed)
    big = blur(rng.standard_normal(shape), max(4, shape[0] // 40))
    small = blur(rng.standard_normal(shape), max(2, shape[0] // 256))
    f = big / (np.abs(big).max() or 1.0) * 0.7 + small / (np.abs(small).max() or 1.0) * 0.3
    return f - f.mean()


def vary(packed, detail_normal, plain_normal, thread=-0.07, wear=0.025, seed=1990):
    out = packed.astype(np.float64).copy()
    drawn = np.abs(detail_normal.astype(np.float64) - plain_normal.astype(np.float64)).max(axis=2) > 3.0
    r = out[..., 0] / 255.0
    r = r + wear * fade(r.shape, seed) + thread * drawn
    out[..., 0] = np.clip(np.rint(r * 255.0), 0, 255)
    return out.astype(np.uint8), float(drawn.mean())


def selftest():
    ok = 0
    p = np.zeros((256, 256, 3), np.uint8)
    p[..., 0] = 209
    plain = np.full((256, 256, 3), 128, np.uint8)
    det = plain.copy()
    det[100:104, :] = 160
    out, share = vary(p, det, plain)
    ok += abs(share - 4 / 256) < 1e-6                                  # the drawn rows found, nothing else
    ok += float(out[101, :, 0].mean()) < float(out[50, :, 0].mean()) - 10  # thread smoother than cloth
    ok += float(out[..., 0].std()) > 1.0                                # no longer one flat value
    ok += int(out[..., 1].max()) == 0 and int(out[..., 2].max()) == 0   # ID and metal untouched
    print("packed_roughness selftest: passed=%d/4 failed=%d" % (ok, 4 - ok))
    return 0 if ok == 4 else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())

    def opt(name, default, kind=float):
        return kind(a[a.index(name) + 1]) if name in a else default
    packed = np.asarray(Image.open(a[0]).convert("RGB"))
    out, share = vary(packed, np.asarray(Image.open(a[1]).convert("RGB")), np.asarray(Image.open(a[2]).convert("RGB")),
                      opt("--thread", -0.07), opt("--wear", 0.025), opt("--seed", 1990, int))
    Image.fromarray(out, "RGB").save(a[3])
    r = out[..., 0] / 255.0
    print("packed roughness: %s, drawn %.1f%% of texels, roughness %.3f to %.3f (mean %.3f, spread %.3f)" % (
        a[3], 100 * share, r.min(), r.max(), r.mean(), r.std()))
