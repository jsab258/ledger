"""Nets, curtains and blinds of the house windows: their textures, made by script (numpy, PIL), no Blender needed.

Target section 6: all are cards behind the glass; their alpha is the weave and the folds. The lessons of the shops' reviews (14 October) are applied from the start: a fold is never a regular
corrugation (the pitch of each fold is drawn at random, nets 30 to 70 mm and curtains 55 to 95 mm, its depth too, the folds' profile a soft S, not a V), the normal maps are soft, the cloth is
see-through (alpha under 1: the room lights it from behind; the card's night emission is the target's), the hem is a scalloped lace border whose lobes hang DOWN, the head is a gathered casing with
a wire line under it.

Textures are packed in three atlases (net_voile, curtain, blind) so that each material is one image set; the card's UVs say which part of the atlas it takes. The sizes keep a kit glb under 400 KB.
All maps are written as PNG (base colour with alpha) and JPEG (the normal map: a real RGB tangent-space normal map, blue about 0.9).
"""
import json
import os

import numpy as np
from PIL import Image

NET_MM_PER_PX = 4.7        # 192 px for a 900 mm card: a 60 mm lace repeat is 12.8 px, a 30 mm fold 6.4 px


def pleats(width_mm, npx, pitch_rng, depth_rng, rng, shear=0.0):
    """A fold profile across a card: pleat boundaries at random pitches, each pleat a soft S (a raised cosine whose crest is pushed to one side), its depth drawn at random.
    Returns (height in mm, pleat index of each pixel)."""
    xs = (np.arange(npx) + 0.5) * width_mm / npx
    b = [-rng.uniform(0, pitch_rng[1])]
    while b[-1] < width_mm + pitch_rng[1]:
        b.append(b[-1] + rng.uniform(*pitch_rng))
    h = np.zeros(npx)
    idx = np.zeros(npx, int)
    pitches, depths = [], []
    for i in range(len(b) - 1):
        m = (xs >= b[i]) & (xs < b[i + 1])
        if not m.any():
            continue
        t = (xs[m] - b[i]) / (b[i + 1] - b[i])
        d = rng.uniform(*depth_rng)
        pitches.append(b[i + 1] - b[i])
        depths.append(d)
        skew = rng.uniform(-0.28, 0.28)
        tt = t + skew * np.sin(2 * np.pi * t) / (2 * np.pi) * 2.0
        h[m] = d * 0.5 * (1 - np.cos(2 * np.pi * np.clip(tt, 0, 1)))
        idx[m] = i
    pleats.last = {"pitch_min": float(min(pitches)), "pitch_max": float(max(pitches)), "pitch_std": float(np.std(pitches)), "depth_std": float(np.std(depths)), "n": len(pitches)}
    return h, idx


def normal_map(height_mm, mm_per_px_x, mm_per_px_z, strength=0.6):
    """A tangent-space normal map (OpenGL, +Y up in the image) from a height field in mm: soft (the strength is a fraction of the true slope)."""
    gy, gx = np.gradient(height_mm, mm_per_px_z, mm_per_px_x)
    nx, ny, nz = -gx * strength, gy * strength, np.ones_like(gx)
    n = np.sqrt(nx * nx + ny * ny + nz * nz)
    return np.stack([nx / n, ny / n, nz / n], axis=-1) * 0.5 + 0.5


def _blur(a, k=1):
    from scipy import ndimage
    return ndimage.gaussian_filter(a, k)


def net_card(kind, width_mm, height_mm, seed, lace_share, torn=False):
    """One net card's base colour (grey brightness x 3 with the alpha) and normal map. kind N1/N2/N3 (the lace share is the target's: N1 0.30, N2 0.18, N3 0).
    Width 900 mm gathered at 200 per cent: pleats 30 to 70 mm apart, brightness modulation +-22 per cent, the mean covered share about 0.64 (voile) and 0.86 (lace band)."""
    rng = np.random.default_rng(seed)
    nx = int(round(width_mm / NET_MM_PER_PX))
    nz = int(round(height_mm / NET_MM_PER_PX))
    h1, idx = pleats(width_mm, nx, (30.0, 70.0), (7.0, 14.0), rng)
    fold_stats = dict(pleats.last, rng=[30.0, 70.0])
    # the pleats run down the net, a little askew and deeper toward the hem (a net hangs from its gathers and spreads at the foot)
    zz = (np.arange(nz) + 0.5) / nz
    X = np.arange(nx)[None, :].repeat(nz, 0).astype(float)
    shear_px = (zz[:, None] - 0.5) * 2.0 * (1.2 + rng.uniform(-0.4, 0.4))           # about 8 mm over the card: not ruler-straight
    h = np.empty((nz, nx))
    for j in range(nz):
        xs = np.clip(np.arange(nx) - shear_px[j, 0], 0, nx - 1)
        h[j] = np.interp(xs, np.arange(nx), h1)
    h *= (0.78 + 0.34 * zz)[:, None]
    h += (_blur(rng.normal(0, 1, (nz, nx)), 3) * 1.6)
    h = np.clip(h, 0.0, None)
    hmax = h.max()
    hn = h / hmax
    # brightness: lit from the left: the slope shades the folds, the valleys are darker; +-22 per cent
    gx = np.gradient(_blur(h, 0.8), axis=1)
    bright = 1.0 + 0.22 * np.clip(gx / (np.abs(gx).max() + 1e-6) * 1.6, -1, 1) - 0.07 * (1 - hn)
    # coverage: one layer 0.40, folds overlapping where the net is gathered: 0.40 + a share of the pleat's depth, its mean 0.64
    alpha = 0.55 + 0.36 * hn ** 1.2 + _blur(rng.normal(0, 0.02, (nz, nx)), 0.8)
    # the lace band at the foot (share of the height): a diamond lattice, a 60 mm repeat, coverage 0.86 on average
    band = int(round(lace_share * nz))
    if band > 0:
        px60 = 60.0 / NET_MM_PER_PX
        yy, xx = np.mgrid[0:band, 0:nx]
        p = 0.5 + 0.5 * np.cos(2 * np.pi * xx / px60) * np.cos(2 * np.pi * (yy + 0.5 * px60 * 0.25) / px60)
        lace = 0.72 + 0.28 * np.clip((p - 0.35) / 0.4, 0, 1)
        alpha[nz - band:] = np.clip(0.5 * alpha[nz - band:] + 0.5 * lace + 0.11, 0, 1)
        bright[nz - band:] *= 0.97
    # the hem: a 28 mm lace border, scalloped (period 35 mm), the lobes hanging down; the lower edge sags in a gentle sine (6 mm, wavelength 90 mm) between the folds
    hem_px = int(round(28.0 / NET_MM_PER_PX))
    xs_mm = (np.arange(nx) + 0.5) * NET_MM_PER_PX
    lobe = 8.0 * np.abs(np.sin(np.pi * xs_mm / 35.0)) ** 0.7
    sag = 6.0 * np.sin(2 * np.pi * xs_mm / 90.0 + rng.uniform(0, 6.28))
    edge_mm = height_mm - 1.0 - (8.0 - lobe) + sag * 0.5 * 0 + 0.0            # the lowest point of each lobe at the card's foot; the sag is applied to the whole border below
    edge_mm = (height_mm - 8.5) + lobe - 0.0 + sag * 0.5
    edge_mm = np.minimum(edge_mm, height_mm - 0.4)
    rows_mm = (np.arange(nz) + 0.5) * NET_MM_PER_PX
    outside = rows_mm[:, None] > edge_mm[None, :]
    alpha[outside] = 0.0
    border = (rows_mm[:, None] > edge_mm[None, :] - 28.0) & (~outside)
    alpha[border] = np.clip(alpha[border] * 0.45 + 0.55, 0, 1)
    bright[border] *= 1.04
    # the head: a 20 mm double-thickness casing (alpha 0.92), a one pixel dark wire line under it (alpha 0.5, luma 60)
    head_px = max(2, int(round(20.0 / NET_MM_PER_PX)))
    alpha[:head_px] = 0.92
    bright[:head_px] = 0.97 + 0.03 * rng.random((head_px, nx))
    alpha[head_px] = 0.5
    bright[head_px] = 60.0 / 238.0
    alpha[:2] = np.maximum(alpha[:2], 0.5)
    # a torn net: a notch cut from one lower corner (the hem is 80 mm out of true: the card's own geometry carries that), the tear's edge ragged
    if torn:
        nr = int(round(150 / NET_MM_PER_PX))
        nc = int(round(220 / NET_MM_PER_PX))
        yy, xx = np.mgrid[0:nr, 0:nc]
        tri = (xx / nc + (1 - yy / nr)) < 1.0 + 0.12 * rng.normal(0, 1, (nr, nc))
        alpha[nz - nr:, :nc][tri] = 0.0
    alpha = np.clip(alpha, 0.0, 1.0)
    # edges feather over a pixel so a sheet does not shimmer
    alpha = _blur(alpha, 0.5)
    bright = np.clip(bright, 0.25, 1.15) / 1.15
    nrm = normal_map(h, NET_MM_PER_PX, NET_MM_PER_PX, 0.5)
    g = np.clip(bright, 0, 1)
    rgba = np.stack([g, g, g, alpha], axis=-1)
    return rgba, nrm, {"fold": fold_stats, "mean_alpha": float(alpha[head_px + 1:nz - band if band else nz].mean()), "mean_alpha_lace": float(alpha[nz - band:].mean()) if band else None,
                      "pitches_mm": [30.0, 70.0], "size_px": [nx, nz]}


def curtain_card(width_mm, height_mm, seed, pelmet_mm=60.0):
    """A lined curtain drawn: pleats 55 to 95 mm apart (depth 12 to 28 mm drawn at random, a soft S), brightness modulation 0.25, opacity 0.97, a straight hem, a 60 mm pelmet band at the top.
    Grey brightness (the colour is the material's), 5 mm a pixel across, 18 mm down (the folds run straight down)."""
    rng = np.random.default_rng(seed)
    nx = int(round(width_mm / 5.0))
    nz = 96
    h1, idx = pleats(width_mm, nx, (55.0, 95.0), (12.0, 28.0), rng)
    fold_stats = dict(pleats.last, rng=[55.0, 95.0])
    zz = (np.arange(nz) + 0.5) / nz
    h = np.empty((nz, nx))
    for j in range(nz):
        sh = (zz[j] - 0.5) * 2.0 * 0.9
        xs = np.clip(np.arange(nx) - sh, 0, nx - 1)
        h[j] = np.interp(xs, np.arange(nx), h1) * (0.8 + 0.3 * zz[j])
    hn = h / h.max()
    gx = np.gradient(_blur(h, 0.8), axis=1)
    bright = 1.0 + 0.25 * np.clip(gx / (np.abs(gx).max() + 1e-6) * 1.5, -1, 1) - 0.12 * (1 - hn)
    # a turned hem 30 mm (a slightly darker stripe), the pelmet band at the head (a flat band, gathered tight above it)
    hem = max(1, int(round(30.0 / (height_mm / nz))))
    bright[nz - hem:] *= 0.9
    pel = max(1, int(round(pelmet_mm / (height_mm / nz))))
    bright[:pel] = np.clip(bright[:pel] * 0.5 + 0.5, 0, 1) * 0.95
    alpha = np.full((nz, nx), 0.97) - 0.05 * (1 - hn) + rng.normal(0, 0.01, (nz, nx))
    bright = _blur(np.clip(bright, 0.3, 1.2) / 1.2, 0.4)
    nrm = normal_map(h, 5.0, height_mm / nz, 0.45)
    g = np.clip(bright, 0, 1)
    return np.stack([g, g, g, np.clip(alpha, 0, 1)], axis=-1), nrm, {"fold": fold_stats, "size_px": [nx, nz], "pitches_mm": [55.0, 95.0]}


def blind_b1(width_mm=800.0, height_mm=990.0, seed=4):
    """A venetian blind: slats 25 mm apart, tilted closed 70 per cent: each pitch is 70 per cent slat (light on its upper edge, darker below) and 30 per cent gap (alpha 0.25). 16 px wide, 256 rows."""
    nx, nz = 16, 256
    pitch = nz * 25.0 / height_mm
    yy = (np.arange(nz) + 0.5)
    ph = (yy % pitch) / pitch
    g = np.where(ph < 0.7, 0.86 + 0.12 * (1 - ph / 0.7) - 0.10 * (ph / 0.7) ** 2, 0.25)
    a = np.where(ph < 0.7, 1.0, 0.25)
    # the ladder cords: a thin darker line at x +-0.38 of the half width
    img = np.empty((nz, nx, 4))
    for c in range(nx):
        img[:, c, 0:3] = g[:, None]
        img[:, c, 3] = a
    img[:, 2, 0:3] *= 0.7
    img[:, nx - 3, 0:3] *= 0.7
    return img


def blind_b3(width_mm=840.0, height_mm=1540.0):
    """Vertical louvres 89 mm apart turned 40 per cent open: each pitch is 60 per cent louvre (a soft cylinder shade) and 40 per cent gap (alpha 0.35). 128 columns, 8 rows."""
    nx, nz = 128, 8
    pitch = nx * 89.0 / width_mm
    xx = (np.arange(nx) + 0.5)
    ph = (xx % pitch) / pitch
    g = np.where(ph < 0.6, 0.92 - 0.18 * np.abs(ph / 0.6 - 0.5) * 2, 0.4)
    a = np.where(ph < 0.6, 1.0, 0.35)
    img = np.empty((nz, nx, 4))
    img[:, :, 0] = g[None, :]
    img[:, :, 1] = g[None, :]
    img[:, :, 2] = g[None, :]
    img[:, :, 3] = a[None, :]
    return img


def blind_b2(width_mm=780.0, height_mm=960.0):
    """A roller blind: a plain cream sheet (opacity 0.9) with a 20 mm bottom batten (darker) and a pull cord line near the left. 8 px wide, 128 rows."""
    nx, nz = 24, 128
    img = np.empty((nz, nx, 4))
    img[:, :, 0:3] = 0.95
    img[:, :, 3] = 0.9
    bat = max(1, int(round(20.0 / (height_mm / nz))))
    img[nz - bat:, :, 0:3] = 0.6
    img[nz - bat:, :, 3] = 1.0
    img[:nz - bat, 3, 0:3] = 0.55                       # the pull cord (a darker line)
    img[:nz - bat, 3, 3] = 1.0
    # a soft darkening toward the top where the sheet comes off the roller
    img[:, :, 0:3] *= (0.9 + 0.1 * np.linspace(0, 1, nz))[:, None, None]
    return img


def save_rgba(arr, path):
    a = np.clip(np.round(arr * 63.0) / 63.0 * 255 + 0.5, 0, 255).astype(np.uint8)          # 6 bits a channel: smooth maps compress to a third
    Image.fromarray(a, "RGBA").save(path, optimize=True)


def save_rgb_jpg(arr, path, q=88):
    a = np.clip(arr * 255 + 0.5, 0, 255).astype(np.uint8)
    Image.fromarray(a, "RGB").save(path, quality=q, subsampling=0, optimize=True)


def atlas(blocks, pad=2):
    """Pack the blocks (name -> array h x w x C) into one image, top to bottom, left aligned; returns (image, {name: (u0, v0, u1, v1)} with v up from the bottom)."""
    wmax = max(b.shape[1] for b in blocks.values())
    h = sum(b.shape[0] + 2 * pad for b in blocks.values())
    c = next(iter(blocks.values())).shape[2]
    img = np.zeros((h, wmax + 2 * pad, c), np.float32)
    rects = {}
    y = 0
    for name, b in blocks.items():
        y += pad
        # replicate the edge into the padding so filtering never pulls in a neighbour
        bh, bw = b.shape[:2]
        img[y - pad:y + bh + pad, :bw + 2 * pad] = np.pad(b, ((pad, pad), (pad, pad), (0, 0)), mode="edge")
        rects[name] = (pad / (wmax + 2 * pad), 1 - (y + bh) / h, (pad + bw) / (wmax + 2 * pad), 1 - y / h)
        y += bh + pad
    # pad every block's rows to the atlas width by edge replication (done above for its own width)
    return img, rects


def build_all(out_dir, seed0=20):
    """The three atlases of a kit: net_voile (N1, N2, N3 and the torn N1), curtain (C1 and a pair), blind (B1, B2, B3). Returns {file paths, rects, stats}."""
    os.makedirs(out_dir, exist_ok=True)
    stats = {}
    nets = {}
    nrms = {}
    for i, (k, w, h, lace) in enumerate((("N1", 900, 820, 0.30), ("N2", 900, 1570, 0.18), ("N3", 860, 400, 0.0), ("N1_torn", 900, 820, 0.30))):
        rgba, nrm, st = net_card(k, w, h, seed0 + i, lace, torn=(k == "N1_torn"))
        nets[k] = rgba
        nrms[k] = nrm
        stats[k] = st
    img, rects = atlas(nets)
    nimg, _ = atlas(nrms)
    save_rgba(img, os.path.join(out_dir, "net_voile_basecolour.png"))
    save_rgb_jpg(nimg, os.path.join(out_dir, "net_voile_normal.jpg"))
    out = {"net": {"rects": rects}}
    c1, cn1, st1 = curtain_card(960, 1780, seed0 + 10)
    stats["C1"] = st1
    img, rects = atlas({"C1": c1})
    nimg, _ = atlas({"C1": cn1})
    save_rgba(img, os.path.join(out_dir, "curtain_basecolour.png"))
    save_rgb_jpg(nimg, os.path.join(out_dir, "curtain_normal.jpg"))
    out["curtain"] = {"rects": rects}
    b1, b2, b3 = blind_b1(), blind_b2(), blind_b3()
    img, rects = atlas({"B1": b1, "B2": b2, "B3": b3})
    save_rgba(img, os.path.join(out_dir, "blind_basecolour.png"))
    out["blind"] = {"rects": rects}
    out["stats"] = stats
    out["dir"] = out_dir
    json.dump({k: dict(v["fold"]) for k, v in stats.items()}, open(os.path.join(out_dir, "stats.json"), "w"), indent=1)
    return out


if __name__ == "__main__":
    import json
    import sys
    o = build_all(sys.argv[1] if len(sys.argv) > 1 else "/tmp/hw_cloth")
    print(json.dumps(o["stats"], indent=1))
    for f in sorted(os.listdir(o["dir"])):
        print(f, os.path.getsize(os.path.join(o["dir"], f)))
