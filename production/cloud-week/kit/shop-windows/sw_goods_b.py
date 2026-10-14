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
