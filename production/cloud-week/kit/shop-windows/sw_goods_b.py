"""Small shared pieces for the four shops of batch B (14 October 2026): pictures by script for the goods the CC0 libraries do not have (every maker and product name is the project's own: none is a real
firm, and no label shows a drink, a bet or a child), a chamfer for scripted boxes, a bottle, a heap of cloth. Nothing here knows a shop; the layouts (sw_shops_laundry.py, ...) read their numbers from target.json.

Every string drawn is added to `GEN.TEXTS`, which the checks (INV-05, NEV-01) read.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import bpy

import sw_gen as GEN
from sw_gen import GM, font


def chamfer(ob, width=0.003, segments=2, angle=30.0):
    """A bevel on a scripted box (applied when the glb is exported: export_apply)."""
    md = ob.modifiers.new("bevel", "BEVEL")
    md.width = width
    md.segments = segments
    md.limit_method = "ANGLE"
    md.angle_limit = math.radians(angle)
    return ob


def fit_text(d, text, fnt_name, max_w, start, lo=9):
    s = start
    f = font(fnt_name, s)
    while d.textlength(text, font=f) > max_w and s > lo:
        s -= 1
        f = font(fnt_name, s)
    return f


# ---------------------------------------------------------------------------------------------------------------------------------- packets and boxes
def packet_atlas(path, designs, tile=(180, 280), cols=4, seed=3):
    """Printed fronts of boxes and packets: `designs` = [(maker, product, detail, bg, fg, accent, picture), ...] with picture one of 'drop', 'star', 'wave', 'ear', 'sun', 'leaf', 'none'. Each tile is
    tile[0] x tile[1] px: a band in the accent colour at the top and foot, the maker's name in Alfa Slab One, the product in Oswald, a small flat picture, the detail line. The first row of the tile is the
    top of the pack. Returns {index: (u0, v0, u1, v1)} (v 0 at the bottom)."""
    rows = (len(designs) + cols - 1) // cols
    tw, th = tile
    W, H = cols * tw, rows * th
    im = Image.new("RGB", (W, H), (200, 200, 200))
    d = ImageDraw.Draw(im)
    out = {}
    rnd = random.Random(seed)
    for k, (maker, product, detail, bg, fg, accent, pic) in enumerate(designs):
        c, r = k % cols, k // cols
        x0, y0 = c * tw, r * th
        d.rectangle([x0, y0, x0 + tw - 1, y0 + th - 1], fill=bg)
        d.rectangle([x0, y0 + 8, x0 + tw - 1, y0 + 20], fill=accent)
        d.rectangle([x0, y0 + th - 20, x0 + tw - 1, y0 + th - 8], fill=accent)
        f = fit_text(d, maker, "alfa-slab-one", tw - 16, 32)
        d.text((x0 + (tw - d.textlength(maker, font=f)) / 2, y0 + 34), maker, font=f, fill=fg)
        lines = product.split("\n")
        yy = y0 + 34 + f.size + 8
        for ln in lines:
            f2 = fit_text(d, ln, "oswald", tw - 18, 22)
            d.text((x0 + (tw - d.textlength(ln, font=f2)) / 2, yy), ln, font=f2, fill=fg)
            yy += f2.size + 2
        cx, cy = x0 + tw / 2, y0 + th * 0.60
        rr = min(tw, th) * 0.17
        if pic == "drop":
            d.polygon([(cx, cy - rr * 1.2), (cx + rr * 0.85, cy + rr * 0.3), (cx, cy + rr), (cx - rr * 0.85, cy + rr * 0.3)], fill=accent)
            d.ellipse([cx - rr * 0.85, cy - rr * 0.35, cx + rr * 0.85, cy + rr * 1.0], fill=accent)
        elif pic == "star":
            pts = []
            for i in range(10):
                a = math.pi / 2 + i * math.pi / 5
                rad = rr * 1.1 if i % 2 == 0 else rr * 0.5
                pts.append((cx + rad * math.cos(a), cy - rad * math.sin(a)))
            d.polygon(pts, fill=accent)
        elif pic == "wave":
            for j in range(3):
                pts = [(x0 + 24 + i * 6, cy - 10 + j * 22 + 8 * math.sin(i / 2.5 + j)) for i in range(int((tw - 48) / 6))]
                d.line(pts, fill=accent, width=5)
        elif pic == "ear":
            d.line([(cx, cy + rr), (cx, cy - rr)], fill=accent, width=4)
            for j in range(4):
                d.ellipse([cx - 14, cy - rr + j * 18, cx - 2, cy - rr + 14 + j * 18], fill=accent)
                d.ellipse([cx + 2, cy - rr + 9 + j * 18, cx + 14, cy - rr + 23 + j * 18], fill=accent)
        elif pic == "sun":
            d.ellipse([cx - rr * 0.6, cy - rr * 0.6, cx + rr * 0.6, cy + rr * 0.6], fill=accent)
            for i in range(12):
                a = i * math.pi / 6
                d.line([(cx + rr * 0.8 * math.cos(a), cy + rr * 0.8 * math.sin(a)), (cx + rr * 1.15 * math.cos(a), cy + rr * 1.15 * math.sin(a))], fill=accent, width=4)
        elif pic == "leaf":
            d.polygon([(cx - rr, cy + rr * 0.6), (cx, cy - rr), (cx + rr, cy + rr * 0.6), (cx, cy + rr * 0.2)], fill=accent)
        if detail:
            f3 = fit_text(d, detail, "oswald", tw - 18, 14)
            d.text((x0 + (tw - d.textlength(detail, font=f3)) / 2, y0 + th - 46), detail, font=f3, fill=fg)
        GEN.TEXTS.extend([maker] + product.split("\n") + ([detail] if detail else []))
        out[k] = (x0 / W, 1.0 - (y0 + th) / H, (x0 + tw) / W, 1.0 - y0 / H)
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    im.save(path)
    return out


def tin_atlas(path, designs, tile=(256, 128), cols=4, seed=4):
    """Label strips for tins that wrap once round (a name repeated on two panels): `designs` = [(maker, product, detail, bg, ink, ink2), ...]; returns {index: (u0, v0, u1, v1)} (v 0 at the bottom)."""
    rows = (len(designs) + cols - 1) // cols
    tw, th = tile
    W, H = cols * tw, rows * th
    im = Image.new("RGB", (W, H), (200, 200, 200))
    d = ImageDraw.Draw(im)
    out = {}
    for k, (maker, product, detail, bg, ink, ink2) in enumerate(designs):
        c, r = k % cols, k // cols
        x0, y0 = c * tw, r * th
        d.rectangle([x0, y0, x0 + tw - 1, y0 + th - 1], fill=bg)
        d.rectangle([x0, y0 + 6, x0 + tw - 1, y0 + 12], fill=ink)
        d.rectangle([x0, y0 + th - 13, x0 + tw - 1, y0 + th - 7], fill=ink)
        for rep in (0, 1):
            ox = x0 + rep * (tw // 2)
            panel = tw // 2 - 8
            for txt, name, start, yy, col in ((maker, "alfa-slab-one", 34, 18, ink), (product, "oswald", 24, 62, ink2), (detail, "oswald", 20, 92, ink2)):
                if not txt:
                    continue
                f = fit_text(d, txt, name, panel, start, lo=8)
                d.text((ox + 4 + (panel - d.textlength(txt, font=f)) / 2, y0 + yy), txt, font=f, fill=col)
        GEN.TEXTS.extend([t for t in (maker, product, detail) if t])
        out[k] = (x0 / W, 1.0 - (y0 + th) / H, (x0 + tw) / W, 1.0 - y0 / H)
    im = im.filter(ImageFilter.GaussianBlur(0.5))
    im.save(path)
    return out


def jar_labels(path, designs, tile=(256, 256), cols=4):
    """Jars: `designs` = [(product, maker, fill_rgb, fill2_rgb), ...]: per tile the top 62 per cent is the contents' colour (flecked), the rest a paper label with the product and maker. Returns
    {index: ((cu0, cv0, cu1, cv1), (lu0, lv0, lu1, lv1))}: the contents' strip and the label's."""
    rows = (len(designs) + cols - 1) // cols
    tw, th = tile
    W, H = cols * tw, rows * th
    im = Image.new("RGB", (W, H), (200, 200, 200))
    d = ImageDraw.Draw(im)
    rnd = random.Random(8)
    out = {}
    for k, (product, maker, c1, c2) in enumerate(designs):
        c, r = k % cols, k // cols
        x0, y0 = c * tw, r * th
        hc = int(th * 0.60)
        d.rectangle([x0, y0, x0 + tw - 1, y0 + hc], fill=c1)
        for _ in range(140):
            xx, yy = x0 + rnd.randrange(tw), y0 + rnd.randrange(hc)
            rr = rnd.randint(2, 6)
            d.ellipse([xx - rr, yy - rr, xx + rr, yy + rr], fill=c2)
        d.rectangle([x0, y0 + hc, x0 + tw - 1, y0 + th - 1], fill=(238, 230, 208))
        d.rectangle([x0 + 8, y0 + hc + 6, x0 + tw - 9, y0 + th - 7], outline=(120, 40, 40), width=2)
        f = fit_text(d, product, "alfa-slab-one", tw - 30, 26)
        d.text((x0 + (tw - d.textlength(product, font=f)) / 2, y0 + hc + 12), product, font=f, fill=(120, 30, 40))
        f2 = fit_text(d, maker, "oswald", tw - 30, 18)
        d.text((x0 + (tw - d.textlength(maker, font=f2)) / 2, y0 + hc + 12 + f.size + 6), maker, font=f2, fill=(60, 50, 40))
        GEN.TEXTS.extend([product, maker])
        out[k] = ((x0 / W, 1.0 - (y0 + hc) / H, (x0 + tw) / W, 1.0 - y0 / H), (x0 / W, 1.0 - (y0 + th) / H, (x0 + tw) / W, 1.0 - (y0 + hc) / H))
    im.filter(ImageFilter.GaussianBlur(0.5)).save(path)
    return out


# ---------------------------------------------------------------------------------------------------------------------------------- forms
def bottle(gm, cx, cy, z0, r, h, mi=0, mi_cap=None, label=None, label_mi=None, label_uv=None, n=20):
    """A squat or tall bottle (a lathe): body with a rounded foot, a shoulder, a neck and a cap (the cap is a second lathe in material `mi_cap`). `label` = the profile segment indices that carry the label strip
    (label_uv = its picture rectangle, label_mi the material index of the label)."""
    sh = h * 0.70
    prof = [(0.0, 0.0), (r * 0.80, 0.0), (r * 0.96, 0.006), (r, 0.016), (r, sh * 0.96), (r * 0.82, sh), (r * 0.46, sh + (h - sh) * 0.35), (r * 0.30, sh + (h - sh) * 0.62), (r * 0.30, h * 0.93), (0.0, h * 0.93)]
    gm.lathe(cx, cy, z0, prof, mi=mi, n=n, label=label, mi_label=label_mi, label_uv=label_uv)
    if mi_cap is not None:
        gm.lathe(cx, cy, z0 + h * 0.90, [(0.0, 0.0), (r * 0.36, 0.0), (r * 0.36, h * 0.10), (r * 0.30, h * 0.115), (0.0, h * 0.115)], mi=mi_cap, n=n)


def heap(gm, cx, cy, z0, rx, ry, rz, seed=1, mi=0, nlat=8, nlon=22, amp=1.0):
    """A heap of soft cloth (a mound): the upper half of an ellipsoid whose radius is varied by a smooth noise (folds; `amp` scales the folds), the foot on z0. One closed surface."""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(8)]
    V, F = [], []
    for j in range(nlat + 1):
        phi = (math.pi / 2) * j / nlat
        for i in range(nlon):
            th = 2 * math.pi * i / nlon
            nz = 1.0 + amp * (0.16 * math.sin(3 * th + ph[0]) * math.cos(phi * 2 + ph[1]) + 0.11 * math.sin(5 * th + ph[2] + 2 * phi) + 0.09 * math.sin(2 * th + ph[3] - phi * 3)
                              + 0.07 * math.sin(7 * th + ph[4] + 4 * phi) + 0.06 * math.cos(4 * th - 3 * phi + ph[5]))
            V.append((cx + rx * nz * math.cos(phi) * math.cos(th), cy + ry * nz * math.cos(phi) * math.sin(th), z0 + rz * nz * math.sin(phi)))
    for j in range(nlat):
        for i in range(nlon):
            a = j * nlon + i
            b = j * nlon + (i + 1) % nlon
            c = (j + 1) * nlon + (i + 1) % nlon
            d = (j + 1) * nlon + i
            F.append((a, b, c, d))
    top = list(range(nlat * nlon, (nlat + 1) * nlon))
    F.append(tuple(top[::-1]))
    F.append(tuple(range(nlon)))
    gm.add(V, F, mi)


def ladder_towels(path, colours, tile=(256, 64), seed=2):
    """A picture of folded towels' edges: `colours` = [(rgb, border_rgb)]: each tile is the towel's colour with a woven grain, a narrow border stripe near each short end (in `border_rgb`) and a darker fold line
    along the top and the foot; returns {index: (u0, v0, u1, v1)}."""
    rnd = np.random.default_rng(seed)
    tw, th = tile
    H = th * len(colours)
    a = np.zeros((H, tw, 3), np.float32)
    for k, (c, b) in enumerate(colours):
        blk = np.empty((th, tw, 3), np.float32)
        blk[:] = c
        blk += rnd.normal(0, 3.0, blk.shape)
        grain = 3.0 * np.sin(np.arange(tw)[None, :] * 1.7)[..., None] + 2.0 * np.sin(np.arange(th)[:, None] * 2.3)[..., None]
        blk += grain
        for x0 in (int(tw * 0.10), int(tw * 0.88)):
            blk[:, x0:x0 + 6] = np.array(b, np.float32) + rnd.normal(0, 3.0, (th, 6, 3))
        blk[:6] *= 0.80
        blk[-5:] *= 0.88
        a[k * th:(k + 1) * th] = blk
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path)
    return {k: (0.0, 1.0 - (k + 1) / len(colours), 1.0, 1.0 - k / len(colours)) for k in range(len(colours))}


# ---------------------------------------------------------------------------------------------------------------------------------- folded towels from a real weave
FABRIC020 = os.environ.get("LEDGER_FABRIC020", "/home/user/ledger-scratch/polyhaven/_acg/Fabric020/Fabric020_1K-JPG_Color.jpg")


def fetch_fabric020(log=print):
    """ambientCG Fabric020 (CC0) colour map into SCRATCH/polyhaven/_acg (the target's towel weave): fetched once; only the colour map is kept."""
    import subprocess
    import zipfile
    if os.path.exists(FABRIC020):
        return FABRIC020
    d = os.path.dirname(FABRIC020)
    os.makedirs(d, exist_ok=True)
    zp = os.path.join(d, "f.zip")
    subprocess.check_call(["curl", "-sS", "-L", "-m", "180", "-o", zp, "https://ambientcg.com/get?file=Fabric020_1K-JPG.zip"])
    with zipfile.ZipFile(zp) as z:
        z.extract("Fabric020_1K-JPG_Color.jpg", d)
    os.remove(zp)
    log("fetched ambientCG Fabric020 colour map")
    return FABRIC020


def towel_atlas(path, bases, tile=256, seed=2):
    """One square tile per towel colour: the woven grain of ambientCG Fabric020 (its luminance, mean 1) times the colour, two darker border stripes near the short ends (at 8 and 90 per cent). `bases` = [rgb, ...];
    returns {index: (u0, v0, u1, v1)} (v up). The weave's own blue is taken out (only its luminance is used), so each tile is the colour asked for."""
    fetch_fabric020()
    src = np.asarray(Image.open(FABRIC020).convert("RGB"), np.float32) / 255.0
    lum = (0.2126 * src[..., 0] + 0.7152 * src[..., 1] + 0.0722 * src[..., 2])
    lum = lum / max(float(lum.mean()), 1e-6)
    n = len(bases)
    cols = 4
    rows = (n + cols - 1) // cols
    atlas = np.zeros((rows * tile, cols * tile, 3), np.float32)
    rng = np.random.default_rng(seed)
    out = {}
    for k, c in enumerate(bases):
        r_, c_ = k // cols, k % cols
        oy, ox = int(rng.integers(0, 1024 - tile)), int(rng.integers(0, 1024 - tile))
        g = lum[oy:oy + tile, ox:ox + tile]
        g = 0.55 + 0.45 * g                          # a softer weave (the map is strong at this size)
        blk = np.empty((tile, tile, 3), np.float32)
        blk[:] = np.array(c, np.float32)
        blk *= g[..., None]
        for x0 in (int(tile * 0.08), int(tile * 0.90)):
            blk[:, x0:x0 + 7] *= 0.72
        atlas[r_ * tile:(r_ + 1) * tile, c_ * tile:(c_ + 1) * tile] = blk
        out[k] = (c_ * tile / (cols * tile), 1.0 - (r_ + 1) * tile / (rows * tile), (c_ + 1) * tile / (cols * tile), 1.0 - r_ * tile / (rows * tile))
    Image.fromarray(np.clip(atlas, 0, 255).astype(np.uint8)).save(path)
    return out


def towel_box(gm, c, w, h, t, yaw_deg, mi, uvr, vband=(0.44, 0.56)):
    """A folded towel: a box w (x) by t (y) by h (z) centred on c, turned `yaw_deg` about the vertical, every face with the atlas tile `uvr` (the long faces take the tile's middle band, the top the whole tile)."""
    hx, hy, hz = w / 2.0, t / 2.0, h / 2.0
    L = [(-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz), (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz)]
    ya = math.radians(yaw_deg)
    V = [(c[0] + x * math.cos(ya) - y * math.sin(ya), c[1] + x * math.sin(ya) + y * math.cos(ya), c[2] + z) for x, y, z in L]
    F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    u0, v0, u1, v1 = uvr

    def q(a, b):
        return (u0 + (u1 - u0) * a, v0 + (v1 - v0) * b)
    b0, b1 = vband
    uv = [[q(0, 0), q(1, 0), q(1, 1), q(0, 1)], [q(0, 0), q(1, 0), q(1, 1), q(0, 1)], [q(0, b0), q(1, b0), q(1, b1), q(0, b1)],
          [q(0, b0), q(1, b0), q(1, b1), q(0, b1)], [q(1, b0), q(0, b0), q(0, b1), q(1, b1)], [q(0, b0), q(1, b0), q(1, b1), q(0, b1)]]
    gm.add(V, F, mi, uv)


# ---------------------------------------------------------------------------------------------------------------------------------- bottles with a label whose text faces the street
def bottle_atlas(path, tiles, tile=(512, 256)):
    """Labels for bottles made by `bottle` (a lathe wraps its label once round, ring 0 at +x, so the street faces u = 0.75): `tiles` = [(maker, product, colour_rgb, band_rgb)]: a paper label (cream) with a band top
    and foot in `band_rgb`, the maker in Alfa Slab One and the product (one or two lines) in Oswald in `colour_rgb`, drawn twice (at u 0.75 and 0.25: the two faces of the bottle) inside 40 per cent of the width.
    Returns {index: (u0, v0, u1, v1)}; every string is added to GEN.TEXTS."""
    tw, th = tile
    im = Image.new("RGB", (tw, th * len(tiles)), (200, 200, 200))
    dd = ImageDraw.Draw(im)
    out = {}
    for k, (maker, prod, colr, band) in enumerate(tiles):
        y0 = k * th
        dd.rectangle([0, y0, tw - 1, y0 + th - 1], fill=(240, 236, 220))
        dd.rectangle([0, y0, tw - 1, y0 + 26], fill=band)
        dd.rectangle([0, y0 + th - 26, tw - 1, y0 + th - 1], fill=band)
        for cxm in (int(tw * 0.75), int(tw * 0.25)):
            f1 = fit_text(dd, maker, "alfa-slab-one", int(tw * 0.40), 44)
            dd.text((cxm - dd.textlength(maker, font=f1) / 2, y0 + 40), maker, font=f1, fill=colr)
            yy = y0 + 40 + f1.size + 14
            for ln in prod.split("\n"):
                f2 = fit_text(dd, ln, "oswald", int(tw * 0.40), 34)
                dd.text((cxm - dd.textlength(ln, font=f2) / 2, yy), ln, font=f2, fill=(40, 40, 60))
                yy += f2.size + 4
        GEN.TEXTS.extend([maker] + prod.split("\n"))
        out[k] = (0.0, 1.0 - (y0 + th) / (th * len(tiles)), 1.0, 1.0 - y0 / (th * len(tiles)))
    im.filter(ImageFilter.GaussianBlur(0.5)).save(path)
    return out


def jar(gm, cx, cy, z0, r, h, mi_glass_fill, mi_label, label_uv, mi_lid, n=20):
    """A screw-lid jar (a lathe): the foot, the body with the contents (material `mi_glass_fill`, a flat colour), a paper label (`mi_label`, `label_uv` the picture's rectangle, one wrap) over the lower two thirds of the
    body, a shoulder, a lid in `mi_lid` (a rim and a flat top). British preserve jars are straight-sided with a gold or white metal lid."""
    prof = [(0.0, 0.0), (r * 0.90, 0.0), (r, 0.004), (r, h * 0.20), (r, h * 0.62), (r, h * 0.80), (r * 0.86, h * 0.86), (r * 0.80, h * 0.88)]
    gm.lathe(cx, cy, z0, prof, mi=mi_glass_fill, n=n, label=(3, 4), mi_label=mi_label, label_uv=label_uv)
    gm.lathe(cx, cy, z0 + h * 0.86, [(0.0, 0.0), (r * 0.84, 0.0), (r * 0.86, h * 0.02), (r * 0.86, h * 0.12), (r * 0.80, h * 0.14), (0.0, h * 0.14)], mi=mi_lid, n=n)


# ---------------------------------------------------------------------------------------------------------------------------------- floor decals
def worn_path_png(path, size=(1024, 768), seed=5, shift=0.0, tilt=0.0):
    """A darker worn path on a floor, as a soft RGBA decal (alpha only; colour (40, 42, 44)): an ellipse-shaped core, streaks along the walking direction from a blurred noise; `shift` moves the core
    sideways (-1 to 1 of the half width) at the far end and `tilt` is not used (a path to a counter at one side is a shifted core). One picture a shop (the launderette's, the grocer's)."""
    rnd = np.random.default_rng(seed)
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx / w - 0.5) * 2.0
    v = (yy / h - 0.5) * 2.0
    uc = u - shift * (v * 0.5 + 0.5)
    core = np.clip(1.0 - (uc ** 2 / 0.55 + v ** 2 / 0.95), 0.0, 1.0) ** 0.8
    streak = rnd.normal(0, 1, (h, w)).astype(np.float32)
    streak = np.asarray(Image.fromarray(((streak - streak.min()) / (streak.max() - streak.min()) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9)), np.float32) / 255.0
    a = np.clip(core * (0.55 + 0.9 * (streak - 0.5)), 0.0, 1.0) * 0.55
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 40, 42, 44
    rgba[..., 3] = (a * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(path)


def floor_decal(r, name, png, x0, x1, y0, y1, z=0.0015, fixture=None):
    """A flat decal quad on the floor (z a millimetre or two up) with the picture's alpha; registered as a fixture when `fixture` is given."""
    m = r.image_mat(name, png, rough=0.8, alpha=True)
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x0, y0, z), (x1, y0, z), (x1, y1, z), (x0, y1, z)], [], [(0, 1, 2, 3)])
    uvl = me.uv_layers.new(name="UVMap")
    for loop, (a, b) in zip(me.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        uvl.data[loop.index].uv = (a, b)
    ob = bpy.data.objects.new(name, me)
    r.sc.collection.objects.link(ob)
    ob.data.materials.append(m)
    if fixture:
        r.fixtures.append({"fixture": fixture, "name": name, "ext": [x0, x1, y0, y1, 0.0, z]})
    return ob


# ---------------------------------------------------------------------------------------------------------------------------------- the chandler's rope, tins, hats and hardware
ROPE001 = os.environ.get("LEDGER_ROPE001", "/home/user/ledger-scratch/polyhaven/_acg/Rope001/Rope001_1K-JPG_Color.jpg")
ROPE002 = os.environ.get("LEDGER_ROPE002", "/home/user/ledger-scratch/polyhaven/_acg/Rope002/Rope002_1K-JPG_Color.jpg")


def fetch_ropes(log=print):
    """ambientCG Rope001 and Rope002 (CC0) colour maps (the target's twisted rope and twine textures) into SCRATCH/polyhaven/_acg: fetched once; only the colour map is kept."""
    import subprocess
    import zipfile
    for nid, path in (("Rope001", ROPE001), ("Rope002", ROPE002)):
        if os.path.exists(path):
            continue
        d = os.path.dirname(path)
        os.makedirs(d, exist_ok=True)
        zp = os.path.join(d, "f.zip")
        subprocess.check_call(["curl", "-sS", "-L", "-m", "180", "-o", zp, "https://ambientcg.com/get?file=%s_1K-JPG.zip" % nid])
        with zipfile.ZipFile(zp) as z:
            z.extract("%s_1K-JPG_Color.jpg" % nid, d)
        os.remove(zp)
        log("fetched ambientCG %s colour map" % nid)


def rope_png(path, colour, which=1, size=512):
    """A rope's picture for one colour: the luminance of ambientCG Rope001 (manila fibre) or Rope002 (the finer twist) times `colour` (rgb 0-255), cropped to `size` px square (the picture repeats along the rope)."""
    fetch_ropes()
    src = np.asarray(Image.open(ROPE001 if which == 1 else ROPE002).convert("RGB"), np.float32) / 255.0
    lum = 0.2126 * src[..., 0] + 0.7152 * src[..., 1] + 0.0722 * src[..., 2]
    lum = lum / max(float(lum.mean()), 1e-6)
    crop = lum[:size, :size] if lum.shape[0] >= size and lum.shape[1] >= size else np.resize(lum, (size, size))
    img = np.clip(crop[..., None] * np.array(colour, np.float32)[None, None, :], 0, 255).astype(np.uint8)
    Image.fromarray(img).save(path)


def rope_coil(gm, c, R_in, turns, rho, axis="z", mi=0, uv_len=0.12, seg_per_turn=40, sides=8, layers=1):
    """A coil of rope: a tube of radius `rho` swept along a flat spiral (inner radius `R_in`, `turns` turns, one rope-diameter more radius a turn), centred on `c`, lying in the plane perpendicular to `axis` ('z': flat on
    a surface; 'y': standing on edge facing the street, as on a shelf; 'x': flat against a side wall). UVs: u along the rope (one picture repeat every `uv_len` m), v round it. `layers` > 1 stacks that many spirals one on
    another (each a rope diameter higher, the inner radius a little larger). Returns the coil's outer radius."""
    cx, cy, cz = c
    n_tot = int(turns * seg_per_turn)
    V, F, U = [], [], []
    L_acc = 0.0
    prev = None
    R_out = R_in
    for ly in range(layers):
        base = len(V)
        for i in range(n_tot + 1):
            phi = 2 * math.pi * i / seg_per_turn
            rad = R_in + ly * 0.4 * rho + (2.0 * rho * 1.0) * phi / (2 * math.pi)
            R_out = max(R_out, rad)
            h = ly * 1.7 * rho
            if axis == "z":
                p = (cx + rad * math.cos(phi), cy + rad * math.sin(phi), cz + h)
                t = (-math.sin(phi), math.cos(phi), 0.0)
                nrm = (0.0, 0.0, 1.0)
            elif axis == "y":
                p = (cx + rad * math.cos(phi), cy + h, cz + rad * math.sin(phi))
                t = (-math.sin(phi), 0.0, math.cos(phi))
                nrm = (0.0, 1.0, 0.0)
            else:
                p = (cx + h, cy + rad * math.cos(phi), cz + rad * math.sin(phi))
                t = (0.0, -math.sin(phi), math.cos(phi))
                nrm = (1.0, 0.0, 0.0)
            e1 = nrm
            e2 = (t[1] * nrm[2] - t[2] * nrm[1], t[2] * nrm[0] - t[0] * nrm[2], t[0] * nrm[1] - t[1] * nrm[0])
            if prev is not None:
                L_acc += math.dist(p, prev)
            prev = p
            for k in range(sides + 1):
                a = 2 * math.pi * k / sides
                V.append((p[0] + rho * (math.cos(a) * e1[0] + math.sin(a) * e2[0]), p[1] + rho * (math.cos(a) * e1[1] + math.sin(a) * e2[1]), p[2] + rho * (math.cos(a) * e1[2] + math.sin(a) * e2[2])))
                U.append((L_acc / uv_len, k / float(sides)))
        for i in range(n_tot):
            for k in range(sides):
                a = base + i * (sides + 1) + k
                b = a + 1
                c_ = a + (sides + 1) + 1
                d_ = a + (sides + 1)
                F.append((a, d_, c_, b))
    # one Blender face per quad with its own UVs
    off = len(gm.V)
    gm.V.extend(V)
    for f in F:
        gm.F.append(tuple(off + i for i in f))
        gm.M.append(mi)
        gm.U.append([U[i] for i in f])
    return R_out + rho


def twine_reel(gm, cx, cy, z0, r=0.045, h=0.11, mi_wood=0, mi_twine=1, uv_len=0.06, n=18):
    """A reel of twine: a wooden core with two flanges, the twine wound between them (a cylinder with the rope picture repeated round it)."""
    gm.lathe(cx, cy, z0, [(0.0, 0.0), (r * 1.05, 0.0), (r * 1.05, 0.006), (r * 0.55, 0.006), (r * 0.55, h - 0.006), (r * 1.05, h - 0.006), (r * 1.05, h), (0.0, h)], mi=mi_wood, n=n)
    # the twine: a band cylinder (UV round it, along it)
    V, F, U = [], [], []
    for k in range(n + 1):
        a = 2 * math.pi * k / n
        for zz in (z0 + 0.006, z0 + h - 0.006):
            V.append((cx + r * 0.98 * math.cos(a), cy + r * 0.98 * math.sin(a), zz))
            U.append((k * 2 * math.pi * r / n / uv_len, 0.0 if zz < z0 + h / 2 else (h - 0.012) / uv_len))
    off = len(gm.V)
    gm.V.extend(V)
    for k in range(n):
        a = off + 2 * k
        f = (a, a + 2, a + 3, a + 1)
        gm.F.append(f)
        gm.M.append(mi_twine)
        gm.U.append([U[f[0] - off], U[f[1] - off], U[f[2] - off], U[f[3] - off]])


def paint_tin(gm, cx, cy, z0, r, h, luv, n=16, mi_metal=0, mi_label=1, bail=True):
    """A paint tin: a lid rim, the body, a chime; the label on the wall (as tin_stack); a wire bail (a half ring over the top, held in two ears)."""
    prof = [(0.0, 0.0), (r * 0.94, 0.0), (r, 0.004), (r, h - 0.010), (r * 1.035, h - 0.010), (r * 1.035, h - 0.002), (r * 0.90, h - 0.002), (r * 0.90, h - 0.006), (0.0, h - 0.006)]
    gm.lathe(cx, cy, z0, prof, mi=mi_metal, n=n, label=(2, 3), mi_label=mi_label, label_uv=luv)
    if bail:
        gm.torus((cx, cy, z0 + h - 0.006), r * 0.98, 0.0022, mi_metal, axis="y", nm=14, nn=4)       # a ring over the lid: the bail (half of it is hidden in the lid and the other half stands as a loop)


def souwester(gm, cx, cy, z0, s=1.0, mi=0, mi_seam=1, n=24, face=-1.0):
    """A sou'wester (oilskin): a crown of six panels (a rounded dome, seams as thin dark bands), a brim that is short at the front and long at the back (the back drooping), a chin tie. Built about the vertical axis
    through (cx, cy), the front toward -y (`face` -1). The pattern is the target's `script:oilskin_sou_wester`: panels, brim, no CC0 model (the model in the library is a boonie hat)."""
    r_c, h_c = 0.095 * s, 0.105 * s
    V, F = [], []
    rings = []
    nlat = 7
    for j in range(nlat + 1):
        phi = (math.pi / 2) * j / nlat
        idx = []
        for i in range(n):
            th = 2 * math.pi * i / n
            rad = r_c * math.cos(phi)
            idx.append(len(V))
            V.append((cx + rad * math.cos(th), cy + rad * math.sin(th), z0 + 0.04 * s + h_c * math.sin(phi)))
        rings.append(idx)
    for j in range(nlat):
        for i in range(n):
            i2 = (i + 1) % n
            F.append((rings[j][i], rings[j][i2], rings[j + 1][i2], rings[j + 1][i]))
    gm.add(V, F, mi)
    # the brim: a ring from the crown's foot outward, drooping at the back (y > cy when the front is -y)
    nb = 5
    V, F = [], []
    ringsb = []
    for j in range(nb + 1):
        t = j / float(nb)
        idx = []
        for i in range(n):
            th = 2 * math.pi * i / n
            back = max(0.0, math.sin(th) * (-face))                    # 1 at the back
            ext = (1.0 + 0.55 * back + 0.15) if True else 1.0
            rad = r_c * (1.0 + t * (0.30 + 0.55 * back))
            z = z0 + 0.04 * s - t * (0.012 + 0.10 * back) * s
            idx.append(len(V))
            V.append((cx + rad * math.cos(th), cy + rad * math.sin(th), z))
        ringsb.append(idx)
    for j in range(nb):
        for i in range(n):
            i2 = (i + 1) % n
            F.append((ringsb[j][i], ringsb[j][i2], ringsb[j + 1][i2], ringsb[j + 1][i]))
    # a lower face (so the brim has a thickness): the same ring 3 mm under it
    base = len(gm.V)
    gm.add(V, F, mi)
    V2 = [(x, y, z - 0.003) for (x, y, z) in V]
    gm.add(V2, [tuple(reversed(f)) for f in F], mi)
    # the seams of the crown: six thin dark bands up the dome
    for k in range(6):
        th = 2 * math.pi * k / 6.0 + math.pi / 6.0
        pts = []
        for j in range(nlat + 1):
            phi = (math.pi / 2) * j / nlat * 0.98
            pts.append((cx + (r_c + 0.0012) * math.cos(phi) * math.cos(th), cy + (r_c + 0.0012) * math.cos(phi) * math.sin(th), z0 + 0.04 * s + h_c * math.sin(phi)))
        for a, b in zip(pts[:-1], pts[1:]):
            gm.rod(a, b, 0.0016 * s, mi_seam, 5)


def shackle(gm, cx, cy, z, s=1.0, mi=0, face_y=True):
    """A bow shackle seen from the front, lying flat on a wall (the ring in the xz plane): a U of steel rod (a torus half, two straight legs) and a pin across the open end with a head. `s` scales it."""
    R, rr = 0.022 * s, 0.0045 * s
    for k in range(13):
        a = math.pi + math.pi * k / 12.0
        a2 = math.pi + math.pi * (k + 1) / 12.0
        if k < 12:
            gm.rod((cx + R * math.cos(a), cy, z + R * math.sin(a)), (cx + R * math.cos(a2), cy, z + R * math.sin(a2)), rr, mi, 7)
    for sx in (-1, 1):
        gm.rod((cx + sx * R, cy, z), (cx + sx * R, cy, z + 0.030 * s), rr, mi, 7)
    gm.rod((cx - R - 0.005 * s, cy, z + 0.030 * s), (cx + R + 0.006 * s, cy, z + 0.030 * s), 0.0042 * s, mi, 7)
    gm.rod((cx - R - 0.0045 * s, cy, z + 0.030 * s), (cx - R - 0.010 * s, cy, z + 0.030 * s), 0.0065 * s, mi, 8)


def wooden_block(gm, cx, cy, z, s=1.0, mi_wood=0, mi_steel=1):
    """A single sheave block, flat on a wall: a rounded wooden shell (a box with a lathe-turned feel: an elongated hexagon), a steel sheave disc in the middle, a steel strap and eye at the head."""
    w, h, t = 0.034 * s, 0.075 * s, 0.026 * s
    pts = [(-w, -h * 0.55), (-w * 1.1, 0.0), (-w, h * 0.55), (0.0, h), (w, h * 0.55), (w * 1.1, 0.0), (w, -h * 0.55), (0.0, -h)]
    V, F = [], []
    for sgn in (0, 1):
        for (px, pz) in pts:
            V.append((cx + px, cy - sgn * t, z + pz))
    n = len(pts)
    F.append(tuple(range(n))[::-1] if False else tuple(range(n)))
    F.append(tuple(n + i for i in range(n))[::-1])
    for i in range(n):
        j = (i + 1) % n
        F.append((i, n + i, n + j, j))
    gm.add(V, F, mi_wood)
    gm.rod((cx, cy - t * 1.0 - 0.0005, z), (cx, cy - t * 1.0 - 0.003, z), w * 0.55, mi_steel, 14)
    gm.torus((cx, cy - t * 0.5, z + h), 0.011 * s, 0.0028 * s, mi_steel, axis="y", nm=12, nn=5)


def horn_cleat(gm, cx, cy, z, s=1.0, mi=0):
    """A horn cleat flat on a wall: a base bar with two horns reaching out to either side (boxes), two screw heads."""
    L, w, d = 0.075 * s, 0.014 * s, 0.012 * s
    gm.box(cx - L * 0.5, cx + L * 0.5, cy - d, cy, z - w * 0.5, z + w * 0.5, mi)
    gm.box(cx - L, cx - L * 0.5, cy - d * 1.6, cy - d * 0.6, z - w * 0.35, z + w * 0.35, mi)
    gm.box(cx + L * 0.5, cx + L, cy - d * 1.6, cy - d * 0.6, z - w * 0.35, z + w * 0.35, mi)
    for sx in (-0.5, 0.5):
        gm.rod((cx + sx * L * 0.5, cy - d, z), (cx + sx * L * 0.5, cy - d - 0.002, z), 0.004 * s, mi, 8)


def chain_run(gm, x, y, z_top, n, s=1.0, mi=0):
    """A short run of chain hung flat on a wall: `n` links (alternate links edge-on), each an oval torus 22 x 12 mm."""
    for k in range(n):
        zc = z_top - k * 0.017 * s
        if k % 2 == 0:
            gm.torus((x, y, zc), 0.007 * s, 0.0021 * s, mi, axis="y", nm=10, nn=5)
        else:
            gm.rod((x, y - 0.0035 * s, zc + 0.008 * s), (x, y - 0.0035 * s, zc - 0.008 * s), 0.0026 * s, mi, 6)


def chart_atlas(path, titles, tile=(256, 340), cols=3, seed=7):
    """Invented sea charts and a tide-table card: each tile a sheet of paper with a coast drawn from noise (no real coast), pale sea, soundings, a compass rose, a border, a title in the project's own place names. The
    last title that starts with 'TIDE' is drawn as a table of times and heights. Returns {index: (u0, v0, u1, v1)}; strings are added to GEN.TEXTS."""
    from sw_gen import font
    rnd = random.Random(seed)
    tw, th = tile
    rows = (len(titles) + cols - 1) // cols
    im = Image.new("RGB", (tw * cols, th * rows), (200, 200, 200))
    d = ImageDraw.Draw(im)
    out = {}
    for k, title in enumerate(titles):
        c, r = k % cols, k // cols
        x0, y0 = c * tw, r * th
        paper = (232, 224, 200)
        d.rectangle([x0, y0, x0 + tw - 1, y0 + th - 1], fill=paper, outline=(90, 80, 60), width=2)
        if title.startswith("TIDE"):
            f = font("oswald", 26)
            d.text((x0 + 14, y0 + 12), title, font=f, fill=(30, 40, 80))
            fs = font("oswald", 17)
            for i in range(14):
                yy = y0 + 56 + i * 20
                d.line([(x0 + 10, yy + 18), (x0 + tw - 10, yy + 18)], fill=(150, 140, 120), width=1)
                d.text((x0 + 14, yy), "%02d.%02d" % (rnd.randrange(0, 12), rnd.choice((5, 10, 25, 40, 55))), font=fs, fill=(40, 40, 60))
                d.text((x0 + 90, yy), "%.1f m" % rnd.uniform(0.6, 5.4), font=fs, fill=(40, 40, 60))
                d.text((x0 + 170, yy), "HW" if i % 2 == 0 else "LW", font=fs, fill=(150, 40, 40))
            GEN.TEXTS.extend([title, "HW", "LW"])
        else:
            m = 18
            d.rectangle([x0 + m, y0 + 46, x0 + tw - m, y0 + th - 18], fill=(196, 214, 218), outline=(60, 70, 90), width=2)
            # a coast: a polygon from a noisy line across the chart; land in buff
            pts = [(x0 + m, y0 + 46 + rnd.randrange(30, 120))]
            for i in range(1, 9):
                pts.append((x0 + m + i * (tw - 2 * m) / 8.0, y0 + 46 + rnd.randrange(30, 150)))
            land = pts + [(x0 + tw - m, y0 + 46), (x0 + m, y0 + 46)]
            d.polygon(land, fill=(222, 206, 160))
            d.line(pts, fill=(80, 70, 50), width=2)
            for i in range(30):
                px, py = x0 + m + 10 + rnd.randrange(tw - 2 * m - 20), y0 + 46 + 170 + rnd.randrange(th - 46 - 18 - 190) if th > 260 else y0 + 150
                if py > y0 + 46 + 40 + 100:
                    d.text((px, py), str(rnd.randrange(2, 38)), font=font("oswald", 11), fill=(60, 80, 110))
            # a compass rose
            cx, cy = x0 + tw - 62, y0 + th - 66
            d.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], outline=(120, 40, 40), width=2)
            d.polygon([(cx, cy - 34), (cx + 6, cy), (cx, cy + 34), (cx - 6, cy)], fill=(150, 50, 50))
            d.polygon([(cx - 34, cy), (cx, cy - 6), (cx + 34, cy), (cx, cy + 6)], fill=(90, 90, 110))
            d.text((cx - 4, cy - 50), "N", font=font("oswald", 14), fill=(120, 40, 40))
            for gx in range(1, 4):
                d.line([(x0 + m + gx * (tw - 2 * m) / 4.0, y0 + 46), (x0 + m + gx * (tw - 2 * m) / 4.0, y0 + th - 18)], fill=(150, 170, 176), width=1)
            f = fit_text(d, title.split("\n")[0], "alfa-slab-one", tw - 30, 24)
            d.text((x0 + (tw - d.textlength(title.split("\n")[0], font=f)) / 2, y0 + 10), title.split("\n")[0], font=f, fill=(30, 40, 80))
            if "\n" in title:
                f2 = fit_text(d, title.split("\n")[1], "oswald", tw - 30, 16)
                d.text((x0 + (tw - d.textlength(title.split("\n")[1], font=f2)) / 2, y0 + 28), title.split("\n")[1], font=f2, fill=(60, 60, 90))
            GEN.TEXTS.extend(title.split("\n"))
        out[k] = (x0 / (tw * cols), 1.0 - (y0 + th) / (th * rows), (x0 + tw) / (tw * cols), 1.0 - y0 / (th * rows))
    im.save(path)
    return out


# ---------------------------------------------------------------------------------------------------------------------------------- resting goods (DSP-06: nothing floats)
def rest_z(d, x, y, R, ring=8, spread=0.75):
    """The height at which a roundish good of radius `R` standing at (x, y) of the display's frame comes to rest on what is already placed (the bed, a crate's floor, the goods under it): rays are cast down at its
    centre and at `ring` points round it (at `spread` x R); a point at distance rho from the centre of a sphere of radius R is R - sqrt(R^2 - rho^2) above its foot, so the foot rests at the highest of
    (hit - that rise). Nothing hit: the bed (0)."""
    import bpy
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    rho = spread * R
    rise = R - math.sqrt(max(R * R - rho * rho, 0.0))
    pts = [(x, y, 0.0)] + [(x + rho * math.cos(2 * math.pi * k / ring), y + rho * math.sin(2 * math.pi * k / ring), rise) for k in range(ring)]
    best = None
    for (px, py, under) in pts:
        z0 = 3.0
        for _ in range(8):
            hit, loc, nrm, idx, ob, mw = d.sc.ray_cast(dg, (px, py, z0), (0.0, 0.0, -1.0))
            if not hit:
                break
            if d.coll_t in ob.users_collection or ob.hide_render:          # the hidden templates of the models, at the origin, are not part of the display
                z0 = loc.z - 1e-4
                continue
            z = loc.z - under
            best = z if best is None else max(best, z)
            break
    return 0.0 if best is None else best


def ground_piece(d, names, z_target=0.0, top=False):
    """Move a placed piece (its object names) straight down or up so that its lowest vertex (its highest, with `top`: a jacket hung under a rail) is at `z_target`: for a piece that was turned about x or y (a
    leaning lifebuoy), whose bounding box is lower than its mesh."""
    import bpy
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    lo = -1e9 if top else 1e9
    for n in names:
        ob = bpy.data.objects[n]
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ob.matrix_world
        zs = [(mw @ v.co).z for v in me.vertices]
        lo = max(lo, max(zs)) if top else min(lo, min(zs))
        ev.to_mesh_clear()
    dz = z_target - lo
    for r_ in {bpy.data.objects[n].parent for n in names if bpy.data.objects[n].parent is not None}:
        r_.location.z += dz
    if getattr(d, "items", None):
        d.items[-1]["ext"][4] = round(d.items[-1]["ext"][4] + dz, 4)
        d.items[-1]["ext"][5] = round(d.items[-1]["ext"][5] + dz, 4)
    return dz


def settle_down(d, names, max_drop=0.06, step=0.0005, touch=0.0012):
    """Lower a placed piece (its object names) until it touches what is under it: the piece's mesh vertices (a sample of 300) are tested against the other parts of the display (not the hidden templates, not
    itself) with a nearest-surface query; it stops when one is within `touch` (1.2 mm), or after `max_drop`. For a roundish good set on others (a nestled apple) whose resting height the sphere model of
    `rest_z` only approximates. Returns the drop in metres."""
    import bpy
    from mathutils.bvhtree import BVHTree
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    own = set(names)
    pts = []
    for n in names:
        ob = bpy.data.objects[n]
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ob.matrix_world
        pts.extend([tuple(mw @ v.co) for v in me.vertices])
        ev.to_mesh_clear()
    if not pts:
        return 0.0
    P = np.array(pts)
    lo, hi = P.min(axis=0), P.max(axis=0)
    if len(P) > 300:
        P = P[np.random.default_rng(1).choice(len(P), 300, replace=False)]
    trees = []
    for ob in bpy.data.objects:
        if ob.type != "MESH" or ob.name in own or d.coll_t in ob.users_collection or ob.hide_render:
            continue
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        mw = ob.matrix_world
        V = [tuple(mw @ v.co) for v in me.vertices]
        me.calc_loop_triangles()
        T = [tuple(t.vertices) for t in me.loop_triangles]
        ev.to_mesh_clear()
        if not V or not T:
            continue
        Va = np.array(V)
        if np.any(Va.max(axis=0) < lo - 0.05) or np.any(Va.min(axis=0) > hi + 0.05):
            continue
        trees.append(BVHTree.FromPolygons(V, T, epsilon=0.0))
    drop = 0.0
    while drop < max_drop:
        best = 1e9
        for p_ in P:
            q = (p_[0], p_[1], p_[2] - drop)
            for t_ in trees:
                hit = t_.find_nearest(q)
                if hit[0] is not None and hit[3] < best:
                    best = hit[3]
        if best <= touch:
            break
        drop += max(step, min(best - touch, 0.004) * 0.9)
    roots = {bpy.data.objects[n].parent for n in names if bpy.data.objects[n].parent is not None}
    for r_ in roots:
        r_.location.z -= drop
    if getattr(d, "items", None) and d.items and d.items[-1]["objs"] == list(names):
        d.items[-1]["ext"][4] = round(d.items[-1]["ext"][4] - drop, 4)
        d.items[-1]["ext"][5] = round(d.items[-1]["ext"][5] - drop, 4)
    return drop


# ---------------------------------------------------------------------------------------------------------------------------------- the fishmonger's slab, ice and trays
def rot_x(gm, i0, pivot, deg):
    """Rotate the vertices of `gm` from index `i0` on about the x axis through `pivot` (y, z) by `deg` degrees (positive: a point further back (+y) goes higher), as a tray laid on a sloping slab."""
    a = math.radians(deg)
    py, pz = pivot
    for i in range(i0, len(gm.V)):
        x, y, z = gm.V[i]
        dy, dz = y - py, z - pz
        gm.V[i] = (x, py + dy * math.cos(a) - dz * math.sin(a), pz + dy * math.sin(a) + dz * math.cos(a))


def ice_png(path, size=512, seed=4):
    """Crushed ice, a picture by script: pale blue-white with cloudy mottling, small bright facets and a few grey-blue cracks (no CC0 photograph of ice is in the set: ambientCG Ice002 is a frozen lake). Tone: kept under 205
    so that the ice does not burn under the gate's night spill."""
    rnd = np.random.default_rng(seed)
    base = np.zeros((size, size, 3), np.float32)
    base[:] = (196, 210, 220)
    cloud = rnd.normal(0, 1, (size // 8, size // 8)).astype(np.float32)
    cloud = np.asarray(Image.fromarray(((cloud - cloud.min()) / (cloud.max() - cloud.min()) * 255).astype(np.uint8)).resize((size, size), Image.BICUBIC), np.float32) / 255.0
    base *= (0.82 + 0.20 * cloud)[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for _ in range(260):
        x, y = rnd.integers(0, size), rnd.integers(0, size)
        pts = [(x + rnd.integers(-18, 18), y + rnd.integers(-18, 18)) for _ in range(3)]
        c = int(rnd.integers(0, 2))
        d.polygon(pts, fill=(222, 232, 238) if c else (150, 170, 188))
    for _ in range(40):
        x, y = rnd.integers(0, size), rnd.integers(0, size)
        d.line([(x, y), (x + rnd.integers(-60, 60), y + rnd.integers(-60, 60))], fill=(134, 156, 176), width=1)
    img.filter(ImageFilter.GaussianBlur(0.7)).save(path)


def ice_chunk(gm, c, s, seed, mi=0, uv=None):
    """A chunk of crushed ice: a random convex-ish polyhedron (an irregular octahedron with moved corners), `s` across, one of a few shapes by `seed`; UVs from a tile of the ice picture (`uv` = (u0, v0, u1, v1))."""
    rnd = random.Random(seed)
    cx, cy, cz = c
    pts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    V = [(cx + s * 0.5 * (p[0] * rnd.uniform(0.6, 1.2)), cy + s * 0.5 * (p[1] * rnd.uniform(0.6, 1.2)), cz + s * 0.5 * (p[2] * rnd.uniform(0.5, 1.0))) for p in pts]
    F = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
    U = None
    if uv:
        u0, v0, u1, v1 = uv
        tri = [(u0, v0), (u1, v0), ((u0 + u1) / 2, v1)]
        U = [tri for _ in F]
    gm.add(V, F, mi, U)


def enamel_tray(gm, cx, cy, z0, w=0.37, d=0.30, h=0.05, mi=0, mi_rim=0):
    """A white enamel tray (a box open on top: a floor 3 mm and four walls 3 mm, rounded rim as a rod along each top edge) centred at (cx, cy) on a floor z0. One mesh; the rim rods are thicker than the walls."""
    t = 0.003
    gm.box(cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, z0, z0 + t, mi)
    gm.box(cx - w / 2, cx + w / 2, cy - d / 2, cy - d / 2 + t, z0, z0 + h, mi)
    gm.box(cx - w / 2, cx + w / 2, cy + d / 2 - t, cy + d / 2, z0, z0 + h, mi)
    gm.box(cx - w / 2, cx - w / 2 + t, cy - d / 2, cy + d / 2, z0, z0 + h, mi)
    gm.box(cx + w / 2 - t, cx + w / 2, cy - d / 2, cy + d / 2, z0, z0 + h, mi)
    r_ = 0.004
    for (a, b) in (((cx - w / 2, cy - d / 2), (cx + w / 2, cy - d / 2)), ((cx - w / 2, cy + d / 2), (cx + w / 2, cy + d / 2)), ((cx - w / 2, cy - d / 2), (cx - w / 2, cy + d / 2)), ((cx + w / 2, cy - d / 2), (cx + w / 2, cy + d / 2))):
        gm.rod((a[0], a[1], z0 + h), (b[0], b[1], z0 + h), r_, mi_rim, 8)
