#!/usr/bin/env python3
"""The street's drawn surfaces as seamless textures, for Unreal.

    python tools/props/make_street_surfaces.py            # writes production/assets/street/surfaces/
    python tools/props/make_street_surfaces.py --selftest

WHY THIS EXISTS, 23 September. The look moved into Unreal (Jafar's ruling of
the morning), and Blender's walls, flags and stallriser tile are not
photographs: tools/art-recipes/terrace-front.py DRAWS them from numbers - a
215 x 65 mm brick in stretcher bond, a 10 mm joint darkened to 0.45, each
brick a tone drawn from the range measured off the sheet's gable, faint
staining over the top; 900 x 600 mm flags in 12 mm dark joints mixed between
two tones; 150 mm quartered tiles. The pack's "brick" photograph that the
first Unreal pass used is a sandy random stone and read as rubble. So the
same numbers are drawn here into images Unreal can wear.

THE NUMBERS ARE READ FROM THE RECIPE, not copied: importing it pure (no
Blender) hands over BRICK_W_M, BRICK_TONES, FLAG_W_M and the rest, and the
authored colours from its MATERIALS table, so a change there is a change
here on the next run.

SEAMLESS BY CONSTRUCTION. Each texture covers a whole number of periods, and
a brick or flag is identified by its index MODULO the tile, so the one
crossing the tile's edge is the same brick on both sides and keeps one tone.
The staining is periodic value noise from a fixed seed. Nothing is fetched:
every pixel is computed from this file's numbers, so the output is ours.

WHAT IT WRITES, per surface: <name>.png (albedo, sRGB, carrying the authored
colour, so Unreal grades it by 1), <name>_n.png (tangent-space normal, the
joints recessed, DirectX green as Unreal reads it) and <name>_r.png
(roughness), plus manifest.json with each tile's size in metres, which the
street export copies into its sidecar.
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_REL = os.path.join("production", "assets", "street", "surfaces")
PX = 1024
SEED = 20260923


def recipe():
    spec = importlib.util.spec_from_file_location(
        "terrace_front", os.path.join(ROOT, "tools", "art-recipes", "terrace-front.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def authored(tf, name):
    for n, rgb, rough in tf.MATERIALS:
        if n == name:
            return rgb, rough
    raise KeyError(name)


def tone_through(stops, u):
    """A uniform u through the (position, value) stops, piecewise linear."""
    import numpy as np
    xs = [p for p, _v in stops]
    vs = [v for _p, v in stops]
    return np.interp(u, xs, vs)


def hash01(i, j, salt):
    """A repeatable 0..1 per integer cell."""
    import numpy as np
    h = (i.astype(np.int64) * 73856093) ^ (j.astype(np.int64) * 19349663) ^ (salt * 83492791)
    h = (h ^ (h >> 13)) * 1274126177
    h = h ^ (h >> 16)
    return (h & 0xFFFFFF).astype(np.float64) / float(0x1000000)


def periodic_noise(n, cells, seed):
    """Smooth value noise on an n x n grid that wraps, with `cells` lattice cells."""
    import numpy as np
    rng = np.random.RandomState(seed)
    lat = rng.rand(cells, cells)
    t = np.arange(n) * cells / float(n)
    i0 = np.floor(t).astype(int)
    f = t - i0
    f = f * f * (3 - 2 * f)
    i1 = (i0 + 1) % cells
    a = lat[np.ix_(i0, i0)]; b = lat[np.ix_(i0, i1)]
    c = lat[np.ix_(i1, i0)]; d = lat[np.ix_(i1, i1)]
    fy = f[:, None]; fx = f[None, :]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def periodic_noise_xy(n, cells_x, cells_y, seed):
    """Smooth value noise that wraps, with different cell counts across and
    down, so it can be stretched tall as a streak is."""
    import numpy as np
    rng = np.random.RandomState(seed)
    lat = rng.rand(cells_y, cells_x)

    def axis(cells):
        t = np.arange(n) * cells / float(n)
        i0 = np.floor(t).astype(int)
        f = t - i0
        return i0, (i0 + 1) % cells, f * f * (3 - 2 * f)
    y0, y1, fy = axis(cells_y)
    x0, x1, fx = axis(cells_x)
    a = lat[np.ix_(y0, x0)]; b = lat[np.ix_(y0, x1)]
    c = lat[np.ix_(y1, x0)]; d = lat[np.ix_(y1, x1)]
    fy = fy[:, None]; fx = fx[None, :]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def blender_fac(v):
    """Value noise is spread 0..1 where Blender's noise Fac sits mostly in
    0.3..0.7; pulled toward the middle so the recipe's own ramp positions
    mean what they meant there."""
    return 0.5 + (v - 0.5) * 0.55


def ramp(v, lo, hi, a, b):
    import numpy as np
    t = np.clip((v - lo) / (hi - lo), 0.0, 1.0)
    return a + (b - a) * t


def wall_wear(tf, n, tile_w, tile_h, salt, splash=True):
    """THE RECIPE'S WEAR, as one multiplier over the wall, rows running UP
    from the foot (the last row is z = 0): patches through the recipe's ramp,
    the splash up the foot of the wall, and rain streaks from the wall head
    that fade in above the sills. Height is real because the street's wall
    UVs are metres of height."""
    import numpy as np
    cells = max(1, int(round(tf.WEAR_PATCH_SCALE * tile_w)))
    patch = ramp(blender_fac(periodic_noise_xy(n, cells, cells, SEED + salt)),
                 0.35, 0.62, tf.WEAR_PATCH_DEPTH, 1.0)
    if not splash:
        return patch
    z = (n - 1 - np.arange(n)[:, None] + 0.5) * tile_h / n
    foot = ramp(z, 0.0, tf.WEAR_SPLASH_M, tf.WEAR_SPLASH_DEPTH, 1.0)
    sx = max(1, int(round(tf.STREAK_ACROSS * tile_w)))
    sy = max(1, int(round(tf.STREAK_DOWN * tile_h)))
    streaks = ramp(blender_fac(periodic_noise_xy(n, sx, sy, SEED + salt + 5)),
                   0.40, 0.62, tf.STREAK_DEPTH, 1.0)
    head = ramp(z, tf.STREAK_FROM_Z, tf.STREAK_FULL_Z, 0.0, 1.0)
    streak = 1.0 + (streaks - 1.0) * head
    return patch * foot * streak


def bond(n, tile_w, tile_h, unit_w, unit_h, joint):
    """Stretcher bond over a tile: (cell index i, row j, in-joint mask, height).

    Row j is offset by half a unit on odd rows; i is taken modulo the units per
    row so the unit crossing the tile edge is one unit. Joint on the left of
    each unit and along the top of each row."""
    import numpy as np
    per_row = int(round(tile_w / unit_w))
    ys = (np.arange(n) + 0.5) * tile_h / n
    xs = (np.arange(n) + 0.5) * tile_w / n
    Y, X = np.meshgrid(ys, xs, indexing="ij")
    j = np.floor(Y / unit_h).astype(int)
    off = (j % 2) * unit_w * 0.5
    xx = X - off
    i = np.floor(xx / unit_w).astype(int) % per_row
    fx = np.mod(xx, unit_w)
    fy = np.mod(Y, unit_h)
    jmask = (fx < joint) | (fy < joint)
    # HEIGHT: the face at 1, the joint at 0, with a one-pixel bevel so the
    # normal map has an edge rather than a cliff.
    dist = np.minimum(np.minimum(fx, unit_w - fx), np.minimum(fy, unit_h - fy))
    px = tile_w / n
    height = np.clip((dist - joint * 0.5) / (1.5 * px), 0.0, 1.0)
    return i, j, jmask, height


def normal_from_height(h, strength):
    """Tangent-space normal, DirectX convention (green down), as 0..255."""
    import numpy as np
    dx = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)) * 0.5 * strength
    dy = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)) * 0.5 * strength
    nx, ny, nz = -dx, dy, np.ones_like(h)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    rgb = np.stack([nx / ln, ny / ln, nz / ln], axis=-1)
    return np.clip((rgb * 0.5 + 0.5) * 255.0 + 0.5, 0, 255).astype(np.uint8)


def to_srgb8(lin):
    import numpy as np
    c = np.clip(lin, 0.0, 1.0)
    s = np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)
    return np.clip(s * 255.0 + 0.5, 0, 255).astype(np.uint8)


#: THE BRICK TILE IS A WHOLE WALL HIGH, 23 September, because the wear on it
#: is: the splash at the foot and the streaks from the wall head depend on
#: height, and the street's wall UVs are metres of height, so a tile 7.2 m
#: tall lays them where they belong on a wall up to its eaves. 32 bricks by
#: 96 courses at 2048 px: a brick is 64 px long, its joint just under 3.
BRICK_TILE = (32, 96)
BRICK_PX = 2048


def brick(tf, name, salt, n=None, worn=True):
    import numpy as np
    n = n or BRICK_PX
    per_row, rows = BRICK_TILE
    tw, th = per_row * tf.BRICK_W_M, rows * tf.BRICK_H_M
    i, j, jm, h = bond(n, tw, th, tf.BRICK_W_M, tf.BRICK_H_M, tf.BRICK_JOINT_M)
    wear = wall_wear(tf, n, tw, th, salt, splash=tf.WEARS.get(name, False)) if worn else 1.0
    tone = tone_through(tf.BRICK_TONES, hash01(i, j % rows, salt))
    base, rough = authored(tf, name)
    stain = 1.0 + tf.BRICK_STAIN * (periodic_noise(n, 24, SEED + salt) * 2.0 - 1.0) * 0.6
    img = np.zeros((n, n, 3))
    for c in range(3):
        face = tone * tf.BRICK_FACE_LIFT * tf.BRICK_FACE_HUE[c]
        v = np.where(jm, tf.BRICK_JOINT_TONE, face)
        img[..., c] = base[c] * v * stain * wear
    r = np.where(jm, min(1.0, rough + 0.08), rough) * (0.96 + 0.08 * hash01(i, j % rows, salt + 7))
    return img, normal_from_height(h, 6.0), r, (tw, th)


def flags(tf):
    import numpy as np
    per_row, rows = 4, 6
    tw, th = per_row * tf.FLAG_W_M, rows * tf.FLAG_H_M
    i, j, jm, h = bond(PX, tw, th, tf.FLAG_W_M, tf.FLAG_H_M, tf.FLAG_JOINT_M)
    mix = hash01(i, j % rows, 31)
    base, rough = authored(tf, "paving")
    grain = 1.0 + 0.10 * (periodic_noise(PX, 64, SEED + 3) * 2.0 - 1.0)
    # THE PAVEMENT TAKES THE PATCHES AND NOT THE SPLASH, as the recipe says:
    # a pavement's wear is trodden in, not run down it.
    worn = wall_wear(tf, PX, tw, th, 41, splash=False)
    img = np.zeros((PX, PX, 3))
    for c in range(3):
        t = tf.FLAG_TONE_A[c] * mix + tf.FLAG_TONE_B[c] * (1.0 - mix)
        v = np.where(jm, tf.FLAG_JOINT_DARK, t * grain)
        img[..., c] = base[c] * v * worn
    r = np.where(jm, min(1.0, rough + 0.1), rough) * np.ones((PX, PX))
    return img, normal_from_height(h, 3.0), r, (tw, th)


def tiles(tf):
    import numpy as np
    n, tw = PX // 2, 2 * tf.TILE_M
    ys = (np.arange(n) + 0.5) * tw / n
    Y, X = np.meshgrid(ys, ys, indexing="ij")
    fx, fy = np.mod(X, tf.TILE_M), np.mod(Y, tf.TILE_M)
    jm = (fx < tf.TILE_JOINT_M) | (fy < tf.TILE_JOINT_M)
    quarter = ((fx < tf.TILE_M / 2) ^ (fy < tf.TILE_M / 2))
    base, rough = authored(tf, "tile_patterned")
    img = np.zeros((n, n, 3))
    for c in range(3):
        v = np.where(jm, 0.55, np.where(quarter, tf.TILE_DARK, 1.0))
        img[..., c] = base[c] * v
    dist = np.minimum(np.minimum(fx, tf.TILE_M - fx), np.minimum(fy, tf.TILE_M - fy))
    h = np.clip((dist - tf.TILE_JOINT_M * 0.5) / (1.5 * tw / n), 0.0, 1.0)
    r = np.where(jm, min(1.0, rough + 0.2), rough) * np.ones((n, n))
    return img, normal_from_height(h, 2.0), r, (tw, tw)


#: THE KERB AS ITS OWN CONCRETE, 23 September. In Unreal the kerb took the
#: texture pack's "kerb" photograph, whose relief is a rough broken stone,
#: and beside the sheet's kerb - a neat grey precast block with a clean top -
#: it read as a concrete ramp. The scene file says what a British kerb is:
#: precast concrete, 915 mm blocks, "which is why a British kerb line has a
#: joint every 915 mm". Four blocks to a tile so neighbours differ, a fine
#: aggregate, a thin dark joint, and next to no relief.
KERB_BLOCKS = 4


def kerb_spec():
    with open(os.path.join(ROOT, "production", "specs", "vignette-scene.json"), encoding="utf-8") as fh:
        k = json.load(fh)["street"]["kerb"]
    return float(k["block_length_m"])


def kerb(tf):
    import numpy as np
    n = PX
    block = kerb_spec()
    tw = KERB_BLOCKS * block
    xs = (np.arange(n) + 0.5) * tw / n
    X, Y = np.meshgrid(xs, xs)
    i = np.floor(X / block).astype(int) % KERB_BLOCKS
    fx = np.mod(X, block)
    joint = 0.006
    jm = (fx < joint) | (fx > block - joint * 0.5)
    base, rough = authored(tf, "kerbstone")
    # ONE TONE PER BLOCK, as precast units from different pours are; a fine
    # aggregate over it, and soft blotches a few blocks across.
    tone = 0.92 + 0.16 * hash01(i, np.zeros_like(i), 53)
    I, J = np.meshgrid(np.arange(n), np.arange(n))
    grain = 1.0 + 0.07 * (hash01(I, J, 59) * 2.0 - 1.0)
    blotch = 1.0 + 0.08 * (periodic_noise(n, 5, SEED + 61) * 2.0 - 1.0)
    img = np.zeros((n, n, 3))
    for c in range(3):
        img[..., c] = base[c] * np.where(jm, 0.42, tone * grain * blotch)
    dist = np.minimum(fx, block - fx)
    h = np.clip((dist - joint * 0.5) / (1.5 * tw / n), 0.0, 1.0)
    r = np.where(jm, min(1.0, rough + 0.12), rough) * (0.97 + 0.06 * hash01(i, np.ones_like(i), 67))
    return img, normal_from_height(h, 1.5), r, (tw, tw)


SURFACES = ("brick_red", "brick_grey", "paving", "tile_patterned", "kerbstone")


def make(out_dir):
    import numpy as np
    from PIL import Image
    tf = recipe()
    os.makedirs(out_dir, exist_ok=True)
    manifest = {"what": "Seamless drawn surfaces for the Unreal street, made by "
                        "tools/props/make_street_surfaces.py from the numbers in "
                        "tools/art-recipes/terrace-front.py. Every pixel is computed; "
                        "nothing is fetched. tile_m is the width and height one copy covers.",
                "surfaces": {}}
    for name in SURFACES:
        if name == "brick_red":
            img, nrm, r, tile = brick(tf, name, 11)
        elif name == "brick_grey":
            img, nrm, r, tile = brick(tf, name, 23)
        elif name == "paving":
            img, nrm, r, tile = flags(tf)
        elif name == "kerbstone":
            img, nrm, r, tile = kerb(tf)
        else:
            img, nrm, r, tile = tiles(tf)
        Image.fromarray(to_srgb8(img)).save(os.path.join(out_dir, name + ".png"))
        Image.fromarray(nrm).save(os.path.join(out_dir, name + "_n.png"))
        Image.fromarray(np.clip(r * 255.0 + 0.5, 0, 255).astype(np.uint8)).convert("RGB").save(
            os.path.join(out_dir, name + "_r.png"))
        mean = [float(img[..., c].mean()) for c in range(3)]
        manifest["surfaces"][name] = {"tile_m": [round(tile[0], 4), round(tile[1], 4)],
                                      "px": list(img.shape[1::-1]),
                                      "mean_linear": [round(m, 4) for m in mean]}
        print("streetSurface %s tile=%.3fx%.3fm px=%dx%d mean=%.3f,%.3f,%.3f"
              % (name, tile[0], tile[1], img.shape[1], img.shape[0], mean[0], mean[1], mean[2]))
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    return manifest


def selftest():
    import numpy as np
    passed = failed = 0

    def ok(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("FAILED - %s : %s" % (name, detail))

    tf = recipe()
    # THE BOND AND ITS RELIEF on a clean wall at the size it is drawn, so the
    # wear cannot be mistaken for joints; the wear on its own below.
    img, nrm, r, tile = brick(tf, "brick_red", 11, worn=False)
    worn_img, _wn, _wr, _wt = brick(tf, "brick_red", 11)
    ok("the brick tile is a whole number of bricks and courses",
       abs(tile[0] / tf.BRICK_W_M - round(tile[0] / tf.BRICK_W_M)) < 1e-9
       and abs(tile[1] / (2 * tf.BRICK_H_M) - round(tile[1] / (2 * tf.BRICK_H_M))) < 1e-9, tile)
    # SEAMLESS: the last column and the first are one brick where they meet,
    # so their difference is no bigger than the difference between two
    # neighbouring columns inside the tile.
    edge = np.abs(worn_img[:, -1] - worn_img[:, 0]).mean()
    inner = np.abs(worn_img[:, BRICK_PX // 2] - worn_img[:, BRICK_PX // 2 - 1]).mean()
    ok("the tile wraps across its left and right edges without a seam", edge <= inner * 1.5 + 1e-6,
       "edge %.4f inner %.4f" % (edge, inner))
    # NOT ACROSS TOP AND BOTTOM ANY MORE, and on purpose: the tile is a whole
    # wall high, its foot splashed and its head streaked, and no wall on the
    # street is taller than it. What is checked instead is that the wear is
    # where the recipe puts it.
    nb = worn_img.shape[0]
    foot = worn_img[-nb // 20:, :, 0].mean()
    middle = worn_img[nb // 2 - nb // 20: nb // 2 + nb // 20, :, 0].mean()
    ok("the foot of the wall is darker than its middle, the recipe's splash",
       foot < middle * 0.9, "foot %.4f middle %.4f" % (foot, middle))
    fi_, _n, _r, _t = flags(tf)
    edge_v = np.abs(fi_[-1] - fi_[0]).mean()
    inner_v = np.abs(fi_[PX // 2] - fi_[PX // 2 - 1]).mean()
    ok("the flags wrap across their top and bottom", edge_v <= inner_v * 1.5 + 1e-6,
       "edge %.4f inner %.4f" % (edge_v, inner_v))
    base, _r = authored(tf, "brick_red")
    m = img[..., 0].mean() / base[0]
    ok("the wall averages near its authored colour less its wear, as the recipe's tones are built to",
       0.55 < m < 1.25, "%.3f" % m)
    joints = (img[..., 0] < base[0] * 0.5).mean()
    ok("the joints are there and dark, about a sixth of the wall", 0.08 < joints < 0.35, "%.3f" % joints)
    ok("the normal map is mostly flat and bends at the joints",
       np.median(nrm[..., 2]) > 250 and nrm[..., 2].min() < 230)
    fi, _fn, _fr, ft = flags(tf)
    ok("the flag tile is whole flags", abs(ft[0] / tf.FLAG_W_M - round(ft[0] / tf.FLAG_W_M)) < 1e-9, ft)
    ki, kn, _kr, kt = kerb(tf)
    kbase, _r = authored(tf, "kerbstone")
    dark_cols = (ki[..., 0] < kbase[0] * 0.6).mean(axis=0) > 0.9
    runs = int(np.sum(dark_cols & ~np.roll(dark_cols, 1)))
    ok("the kerb has a joint every block the scene file gives, and no more",
       runs == KERB_BLOCKS and abs(kt[0] - KERB_BLOCKS * kerb_spec()) < 1e-9,
       "%d joints over %.3f m" % (runs, kt[0]))
    ok("and next to no relief between its joints, which is what the pack's kerb had too much of",
       np.percentile(kn[..., 2], 90) > 250, "%.1f" % np.percentile(kn[..., 2], 90))
    print("make_street_surfaces selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    make(os.path.join(ROOT, OUT_REL))
