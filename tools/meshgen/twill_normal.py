#!/usr/bin/env python3
"""A tiling normal map of a woven twill (denim's 3/1 weave), drawn by script, for a garment material's detail normal.

    python tools/meshgen/twill_normal.py OUT.png [--size 512] [--wales 10] [--depth 0.6]
    python tools/meshgen/twill_normal.py --selftest

WHY, 30 October 2026 (his order C9; the fresh reviewer of Tom's jeans in the game: they "read as plain blue trousers",
the twill a known gap): denim reads by its diagonal wales, too fine to bake at the jeans' 1.43 px/mm, so, as Mafia
carries a knit's rib as a tiling detail normal (production/research/game-clothing-pipeline/MAFIA-SWEATER-2026-10-29.md),
the weave is a small tiling map the garment material repeats (import_garments.py, "detail" in a garment's maps).

WHAT IT DRAWS: WALES diagonal ribs across the tile, rising one thread per pick as a 3/1 twill does (the warp floats over
three picks and under one), each float a rounded bump with a groove where the weft shows; a height field turned into a
tangent-space normal map (OpenGL green up, and a DirectX copy beside it, OUT_dx.png). It tiles: the diagonals meet at the
edges. Nothing here is a photograph or anyone's texture.
"""
import os
import sys

import numpy as np
from PIL import Image


def height(size=512, wales=10, threads=None):
    """The twill's height field, 0..1, tiling: warp floats raised, a 3/1 step per pick."""
    threads = threads or wales * 4             # four picks to one wale's repeat
    y, x = np.mgrid[0:size, 0:size] / float(size)
    warp = (x * threads) % 1.0                 # across a warp thread
    pick = np.floor(y * threads).astype(int)   # which weft pick
    col = np.floor(x * threads).astype(int)
    over = ((col - pick) % 4) != 3             # the warp floats over three picks, under one: the twill's step
    bump = np.sin(np.pi * warp) ** 0.7         # a rounded thread across
    along = (y * threads) % 1.0
    ends = np.sin(np.pi * along) ** 0.35       # the float's ends dip where it passes under
    h = np.where(over, bump * (0.75 + 0.25 * ends), 0.25 * bump)
    return h


def normal_map(h, depth=0.6):
    gx = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)) * 0.5
    gy = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)) * 0.5
    n = np.dstack((-gx * depth * 8.0, gy * depth * 8.0, np.ones_like(h)))
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return n


def to_image(n, directx=False):
    m = n.copy()
    if directx:
        m[..., 1] = -m[..., 1]
    return Image.fromarray(np.clip(np.rint((m * 0.5 + 0.5) * 255), 0, 255).astype(np.uint8), "RGB")


def run(out, size, wales, depth):
    n = normal_map(height(size, wales), depth)
    to_image(n).save(out)
    root, ext = os.path.splitext(out)
    to_image(n, directx=True).save(root + "_dx" + ext)
    flat = float((n[..., 2] > 0.999).mean())
    print("twill: %s and %s_dx%s, %d px, %d wales a tile, %.0f%% flat" % (out, root, ext, size, wales, 100 * flat))


def selftest():
    ok = 0
    h = height(256, 8)
    seam = float(np.abs(h[:, 0] - h[:, -1]).mean())                       # the tile's sides meet: the step across
    inner = float(np.abs(h[:, 8] - h[:, 7]).mean())                        # the same step at a thread's edge inside
    ok += abs(seam - inner) < 0.02                                         # (8 px a thread: 256 px, 32 threads)
    ok += 0.2 < float(h.mean()) < 0.8
    n = normal_map(h)
    ok += bool(np.allclose(np.linalg.norm(n, axis=2), 1.0, atol=1e-6))
    ok += float(n[..., 2].min()) > 0.2                                     # no normal lies down flat
    print("twill_normal selftest: passed=%d/4 failed=%d" % (ok, 4 - ok))
    return 0 if ok == 4 else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())

    def opt(name, default, kind):
        return kind(a[a.index(name) + 1]) if name in a else default
    run(a[0], opt("--size", 512, int), opt("--wales", 10, int), opt("--depth", 0.6, float))
