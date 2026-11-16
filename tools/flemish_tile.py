#!/usr/bin/env python3
"""A WEATHERED FLEMISH-BOND BRICK TILE, DRAWN FROM TRUE SIZES, AND ITS CHECKS AGAINST THE N16-4 TARGET.

    python tools/flemish_tile.py --out F:/LedgerTools/game-inputs/brick-flemish-n16-4 [--seed 7] [--px 2048]
    python tools/flemish_tile.py --check F:/LedgerTools/game-inputs/brick-flemish-n16-4
    python tools/flemish_tile.py --selftest

WHY, 16 November 2026 (order item n16-4 part 2; target production/research/street-checks/N16-4-TARGET-2026-11-16.md,
section 1 and route section 2; the 11 Nov tile's review F:/LedgerTools/gate/new/brick-flemish-2026-11-11/review-brick):
the 11 Nov procedural tile had the right bond but read newly built (crisp arrises, thin pale flush mortar), a regular dot
grid of dark headers and slightly plum, at 75-80 mm courses. This one draws the bond at a course pitch inside 83-89 mm,
darker headers on 20-35% of headers placed by a cluster noise (no grid), greyer recessed mortar, chipped arrises and
2-4 tone families, and writes the three files the street's scan entry reads (diffuse sRGB, DirectX normal, roughness)
plus a header map for a later shader step. It changes nothing in the game by itself.

THE TILE IS SQUARE AND TILES SEAMLESSLY: 8 bond periods across and 32 courses up, so period = 4 x pitch. With pitch
85.0 mm and a 9.5 mm joint: stretcher + perpend 223.5 mm, header face 107 mm, tile 2.72 m (covers_m). All placement
noise wraps at the tile's edge.

--check measures the written files against the target's testable rows (pitch, header share, header darkness, anti-grid,
clustering, mortar against stretcher, mortar saturation, stretcher hue, brick-to-brick spread) and prints one line each
and a last line "flemishCheck failed=none" or the failing names.
"""
import argparse
import colorsys
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

PITCH_MM = 85.0
JOINT_MM = 9.5
PERIODS, COURSES = 8, 32
PERIOD_MM = 4 * PITCH_MM                       # stretcher unit + header unit
UNIT_MM = (PERIOD_MM - JOINT_MM / 2) / 1.5     # stretcher + perpend
STRETCH_MM = UNIT_MM - JOINT_MM
HEADER_MM = (UNIT_MM - JOINT_MM) / 2
TILE_MM = PERIODS * PERIOD_MM
# Target values (N16-4 target, section 1), linear albedo unless named.
STRETCH_LIN = np.array([0.262, 0.095, 0.061])
MORTAR_SRGB = np.array([150, 140, 128]) / 255.0  # warm grey, saturation about 0.15
DARK_SHARE = 0.27                               # of headers (target 20-35%)
DARK_LUM = 0.58                                 # of the stretcher mean (target 0.45-0.70)


def srgb_to_lin(c):
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(c):
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * c ** (1 / 2.4) - 0.055)


def wrap_noise(n, cells, rng):
    """Smooth tiling noise: random values on a cells x cells lattice, bicubic-ish upsampled with wrap."""
    g = rng.random((cells, cells))
    z = ndimage.zoom(np.tile(g, (3, 3)), n / cells, order=3, mode="grid-wrap")
    return z[n:2 * n, n:2 * n]


def layout():
    """Every brick: (x0, x1, y0, y1) in mm inside the tile (x may run past the edge and wraps), kind 'S' or 'H',
    course index, index along the course."""
    bricks = []
    for c in range(COURSES):
        shift = 0.0 if c % 2 == 0 else PERIOD_MM / 2
        y0 = c * PITCH_MM + JOINT_MM / 2
        y1 = y0 + PITCH_MM - JOINT_MM
        x = shift
        for p in range(PERIODS):
            bricks.append((x, x + STRETCH_MM, y0, y1, "S", c, 2 * p))
            x += UNIT_MM
            bricks.append((x, x + HEADER_MM, y0, y1, "H", c, 2 * p + 1))
            x += HEADER_MM + JOINT_MM
    return bricks


def draw(px=2048, seed=7):
    rng = np.random.default_rng(seed)
    mm = TILE_MM / px
    ids = np.full((px, px), -1, dtype=np.int32)
    bricks = layout()
    yy, xx = np.mgrid[0:px, 0:px]
    # arris wear: each brick's edge pushed in by a warped amount (chips 3-15 mm), wrapping noise
    warp = (wrap_noise(px, 96, rng) - 0.5) * 2 + (wrap_noise(px, 384, rng) - 0.5)
    chip = np.clip(warp, 0, None) * (8.0 / mm)      # px pushed in where the noise is high
    for i, (x0, x1, y0, y1, k, c, j) in enumerate(bricks):
        a, b = int(np.floor(x0 / mm)), int(np.ceil(x1 / mm))
        r0, r1 = int(np.floor(y0 / mm)), int(np.ceil(y1 / mm))
        cols = np.arange(a, b) % px
        rows = np.arange(r0, r1) % px
        sub_x = (np.arange(a, b) + 0.5) * mm
        sub_y = (np.arange(r0, r1) + 0.5) * mm
        dx = np.minimum(sub_x - x0, x1 - sub_x)[None, :]
        dy = np.minimum(sub_y - y0, y1 - sub_y)[:, None]
        edge = np.minimum(dx, dy) / mm
        blk = chip[np.ix_(rows, cols)]
        inside = (dx > 0) & (dy > 0) & (edge > blk * 0.6)
        tgt = ids[np.ix_(rows, cols)]
        tgt[inside] = i
        ids[np.ix_(rows, cols)] = tgt
    brick = ids >= 0
    n = len(bricks)
    kinds = np.array([b[4] for b in bricks])
    # header darkening: a wrapping cluster field (0.5-2 m patches) times a per-brick draw, so dark headers come in
    # loose groups, never on a lattice
    # three non-commensurate scales (about 0.9, 0.5 and 0.3 m), so no one spacing dominates the dark map
    cluster = wrap_noise(px, 3, rng) * 0.4 + wrap_noise(px, 5, rng) * 0.35 + wrap_noise(px, 9, rng) * 0.25
    centres = np.array([((b[0] + b[1]) / 2 % TILE_MM, (b[2] + b[3]) / 2) for b in bricks]) / mm
    cl = cluster[centres[:, 1].astype(int) % px, centres[:, 0].astype(int) % px]
    score = np.where(kinds == "H", cl + rng.random(n) * 0.30, -1)
    hidx = np.where(kinds == "H")[0]
    cut = np.sort(score[hidx])[::-1][int(round(DARK_SHARE * len(hidx))) - 1]
    dark = (kinds == "H") & (score >= cut)
    # tone families (3) and a few lighter/yellower bricks (<= 3%)
    fam = rng.choice(3, n, p=[0.5, 0.3, 0.2])
    fam_gain = np.array([[1.0, 1.0, 1.0], [0.86, 0.84, 0.86], [1.10, 1.06, 0.98]])
    lum = np.exp(rng.normal(0, 0.10, n))
    col = STRETCH_LIN[None, :] * fam_gain[fam] * lum[:, None]
    light = rng.random(n) < 0.025
    col[light] = STRETCH_LIN * np.array([1.45, 1.35, 1.25])
    # dark headers: darker and toward purple-brown (hue lower by about 6 degrees)
    col[dark] = STRETCH_LIN * DARK_LUM * np.array([0.95, 1.0, 1.25]) * np.exp(rng.normal(0, 0.06, dark.sum()))[:, None]
    # paint
    albedo = np.zeros((px, px, 3))
    albedo[brick] = col[ids[brick]]
    grain = (wrap_noise(px, 512, rng) - 0.5) * 0.18 + (wrap_noise(px, 160, rng) - 0.5) * 0.10
    albedo[brick] *= (1 + grain[brick])[:, None]
    mortar_lin = srgb_to_lin(MORTAR_SRGB)
    mvar = 1 + (wrap_noise(px, 64, rng) - 0.5) * 0.25 + (wrap_noise(px, 300, rng) - 0.5) * 0.15
    albedo[~brick] = mortar_lin[None, :] * mvar[~brick][:, None]
    # height: brick face 1.0, its edges rounded over 2 mm, mortar recessed 3.5 mm below the face, pitted
    dist = ndimage.distance_transform_edt(brick) * mm
    h = np.where(brick, np.clip(dist / 2.0, 0, 1) * 1.0, 0.0) + (grain * 0.25)
    h = np.where(brick, h, -0.15 + (wrap_noise(px, 300, rng) - 0.5) * 0.1)
    # recess shading: mortar just inside a joint darker (occlusion), so the joint reads set back
    dm = ndimage.distance_transform_edt(~brick) * mm
    occl = np.where(~brick, 0.80 + 0.20 * np.clip(dm / (JOINT_MM / 2), 0, 1), 1.0)
    albedo *= occl[:, :, None]
    # normal (DirectX: green flipped), relief in mm over mm
    relief = h * 3.5
    gy, gx = np.gradient(ndimage.gaussian_filter(relief, 0.7, mode="wrap"), mm)
    nx, ny, nz = -gx, gy, np.ones_like(gx)
    ln = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    normal = np.stack([nx / ln, ny / ln, nz / ln], -1) * 0.5 + 0.5
    rough = np.where(brick, 0.84 + grain * 0.2, 0.95)
    rough = np.where(dark[np.clip(ids, 0, None)] & brick, rough - 0.08, rough)
    return dict(albedo=albedo, normal=normal, rough=np.clip(rough, 0, 1), ids=ids, bricks=bricks, dark=dark,
                kinds=kinds, mm=mm)


def write(out, d, seed):
    os.makedirs(out, exist_ok=True)
    Image.fromarray((lin_to_srgb(d["albedo"]) * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, "flemish_diff.png"))
    Image.fromarray((d["normal"] * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, "flemish_nor_dx.png"))
    Image.fromarray((d["rough"] * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, "flemish_rough.png"))
    hdr = np.zeros(d["ids"].shape, np.uint8)
    m = d["ids"] >= 0
    hdr[m] = np.where(d["kinds"][d["ids"][m]] == "H", 128, 64) + np.where(d["dark"][d["ids"][m]], 127, 0)
    Image.fromarray(hdr).save(os.path.join(out, "flemish_headers.png"))
    np.save(os.path.join(out, "flemish_ids.npy"), d["ids"])
    meta = dict(seed=seed, px=int(d["ids"].shape[0]), covers_m=round(TILE_MM / 1000, 4), pitch_mm=PITCH_MM,
                joint_mm=JOINT_MM, stretcher_unit_mm=round(UNIT_MM, 2), header_mm=round(HEADER_MM, 2),
                kinds=d["kinds"].tolist(), dark=d["dark"].astype(int).tolist(),
                centres_mm=[[round((b[0] + b[1]) / 2 % TILE_MM, 1), round((b[2] + b[3]) / 2, 1)] for b in d["bricks"]],
                course=[b[5] for b in d["bricks"]], along=[b[6] for b in d["bricks"]])
    json.dump(meta, open(os.path.join(out, "flemish_meta.json"), "w"))


def hue_deg(rgb):
    return colorsys.rgb_to_hsv(*np.clip(rgb, 0, 1))[0] * 360


def lum(c):
    return c[..., 0] * 0.2126 + c[..., 1] * 0.7152 + c[..., 2] * 0.0722


def check(out, shuffles=200, seed=11):
    meta = json.load(open(os.path.join(out, "flemish_meta.json")))
    ids = np.load(os.path.join(out, "flemish_ids.npy"))
    srgb = np.asarray(Image.open(os.path.join(out, "flemish_diff.png")), dtype=np.float64) / 255
    lin = srgb_to_lin(srgb)
    kinds, dark = np.array(meta["kinds"]), np.array(meta["dark"], bool)
    res = []

    def row(name, ok, text):
        res.append((name, ok))
        print("%-22s %s  %s" % (name, "PASS" if ok else "FAIL", text))

    row("course pitch", 83 <= meta["pitch_mm"] <= 89, "%.1f mm (83-89)" % meta["pitch_mm"])
    row("stretcher unit", 216 <= meta["stretcher_unit_mm"] <= 224, "%.1f mm (216-224)" % meta["stretcher_unit_mm"])
    row("joint", 7 <= meta["joint_mm"] <= 11, "%.1f mm (7-11)" % meta["joint_mm"])
    hs = dark[kinds == "H"].mean()
    row("dark header share", 0.20 <= hs <= 0.35, "%.0f%% of headers (20-35)" % (100 * hs))
    # per-brick mean colours from the written picture
    n = len(kinds)
    m = ids >= 0
    cnt = np.bincount(ids[m], minlength=n)
    mean = np.stack([np.bincount(ids[m], lin[..., k][m], minlength=n) for k in range(3)], 1) / np.maximum(cnt, 1)[:, None]
    st = (kinds == "S")
    smean = mean[st].mean(0)
    dl = lum(mean[dark]) / lum(smean)
    row("dark header darkness", 0.45 <= np.median(dl) <= 0.70 and dl.min() >= 0.35,
        "median %.2f, min %.2f of stretcher luminance (0.45-0.70, never <0.35)" % (np.median(dl), dl.min()))
    dh = hue_deg(lin_to_srgb(smean)) - hue_deg(lin_to_srgb(mean[dark].mean(0)))
    row("dark header hue", 3 <= dh <= 10, "%.1f deg lower than stretchers (3-10)" % dh)
    sh = hue_deg(lin_to_srgb(smean))
    row("stretcher hue", 12 <= sh <= 18, "%.1f deg sRGB (12-18)" % sh)
    cv = lum(mean[st]).std() / lum(mean[st]).mean()
    row("stretcher spread", 0.10 <= cv <= 0.20, "CV %.2f (0.10-0.20)" % cv)
    mort = lin[~m]
    ml = lum(mort.mean(0)) / lum(smean)
    row("mortar/stretcher", 1.5 <= ml <= 3.2, "linear luminance ratio %.2f (1.5-3.2)" % ml)
    msat = colorsys.rgb_to_hsv(*lin_to_srgb(mort.mean(0)))[1]
    row("mortar saturation", msat <= 0.25, "%.2f (<=0.25)" % msat)
    # anti-grid and clustering on the header lattice (course, header index along it)
    course, along = np.array(meta["course"]), np.array(meta["along"])
    hi = np.where(kinds == "H")[0]
    grid = np.zeros((32, 8))
    grid[course[hi], along[hi] // 2] = dark[hi]
    rng = np.random.default_rng(seed)

    def ac_peak(g):
        f = np.fft.fft2(g - g.mean())
        ac = np.real(np.fft.ifft2(f * np.conj(f)))
        ac /= ac[0, 0] or 1
        best = 0.0
        for dy in range(-6, 7):
            for dx in range(-3, 4):
                if max(abs(dy), abs(dx)) < 2:
                    continue
                v = ac[dy % 32, dx % 8]
                nb = [ac[(dy + a) % 32, (dx + b) % 8] for a in (-1, 0, 1) for b in (-1, 0, 1) if a or b]
                if v > max(nb):
                    best = max(best, v)
        return best

    def win_var(g):
        # windows of about 1 m: 12 courses x 3 headers (36 headers), wrapping
        s = [g[np.ix_([(r + i) % 32 for i in range(12)], [(c + j) % 8 for j in range(3)])].mean()
             for r in range(0, 32, 4) for c in range(8)]
        return np.var(s)

    peak = ac_peak(grid)
    null = [ac_peak(rng.permutation(grid.ravel()).reshape(grid.shape)) for _ in range(shuffles)]
    row("anti-grid", peak <= np.percentile(null, 99), "peak %.3f against shuffles' 99th %.3f" % (peak, np.percentile(null, 99)))
    p = grid.mean()
    v, binom = win_var(grid), p * (1 - p) / 36
    row("clustering", v >= 1.5 * binom, "window variance %.4f, %.1fx binomial (>=1.5)" % (v, v / binom))
    bad = [k for k, ok in res if not ok]
    print("flemishCheck failed=%s" % (",".join(bad) if bad else "none"))
    return 0 if not bad else 1


def selftest():
    import tempfile
    d = tempfile.mkdtemp()
    dd = draw(512, 3)
    write(d, dd, 3)
    ok = abs(UNIT_MM - 223.5) < 0.1 and abs(TILE_MM - 2720) < 0.1
    # a chequer of dark headers must fail anti-grid; written and checked through the same reader
    meta = json.load(open(os.path.join(d, "flemish_meta.json")))
    kinds = np.array(meta["kinds"])
    course, along = np.array(meta["course"]), np.array(meta["along"])
    meta["dark"] = [int(k == "H" and (c + a // 2) % 2 == 0 and c % 2 == 0) for k, c, a in zip(kinds, course, along)]
    json.dump(meta, open(os.path.join(d, "flemish_meta.json"), "w"))
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        check(d, shuffles=50)
    grid_fails = "anti-grid              FAIL" in buf.getvalue()
    print("flemish_tile selftest: %s (sizes %s, chequer fails anti-grid %s)" % ("passed" if ok and grid_fails else "FAILED", ok, grid_fails))
    return 0 if ok and grid_fails else 1


def main(a):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--check")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--px", type=int, default=2048)
    ap.add_argument("--selftest", action="store_true")
    o = ap.parse_args(a)
    if o.selftest:
        return selftest()
    if o.check:
        return check(o.check)
    if o.out:
        write(o.out, draw(o.px, o.seed), o.seed)
        print("flemishTile out=%s covers_m=%.3f" % (o.out, TILE_MM / 1000))
        return check(o.out)
    ap.print_usage()
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
