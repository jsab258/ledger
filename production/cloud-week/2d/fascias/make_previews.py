#!/usr/bin/env python
"""make_previews.py: reduced pictures of the rendered fascia set for review (unit 4.1, cloud week 42).

    /home/user/.bpyenv/bin/python make_previews.py SETDIR [--out production/previews/cloud-week/fascias] [--date 2026-10-09]

Writes JPEGs, each at most 1600 px wide and under 500 KB (the push guard's reduced-preview rule), named fascias-<what>-v1-<date>.jpg:
  fascias-all-ten-v1-...          the ten boards in street order as the GAME shows them (each board's left is a viewer's left, facing it), labelled
  fascias-<board>-v1-...          each board alone: the whole board at 1600 px, and below it the middle 1600 mm at one pixel a millimetre
  fascias-mickeys-with-letters-v1 Mickey's board with the raised gilt letters laid flat over it where the geometry stands (the letters are NOT texture)
  fascias-signs-glass-v1-...      the four hanging signs' faces (the balls as lit spheres), the glass lettering rows on dark glass, the letting board,
                                  the hours plates and the empty unit's whitewashed window
The pictures are made from the PNGs only; nothing here is a render of the game.
"""
import argparse
import io
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fascia_common as fc      # noqa: E402

LABEL_FONT = fc.FONTS_DIR / "evening-paper" / "LibreFranklin-600.ttf"
BG = (24, 24, 26)
FG = (226, 224, 218)


def font(sz):
    return ImageFont.truetype(str(LABEL_FONT), sz)


def save_jpeg(img, path, max_kb=480):
    q = 90
    while q >= 55:
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=q, optimize=True, progressive=True, subsampling=0 if q >= 80 else 2)
        if buf.tell() <= max_kb * 1000:
            Path(path).write_bytes(buf.getvalue())
            return q, buf.tell()
        q -= 4
    Path(path).write_bytes(buf.getvalue())
    return q, buf.tell()


def load_board(setdir, bid):
    return Image.open(Path(setdir) / "fascias" / bid / f"{bid}_basecolour.png").convert("RGB")


def side_note(T, s):
    lo, hi = s["street_x_m"]
    if s["side"] == "east":
        return f"east parade, street x {lo:g} to {hi:g}: low x is on the viewer's RIGHT; door at the {'right' if s['door_end_street'] == 'low' else 'left'}"
    return f"west block, street x {lo:g} to {hi:g}: low x is on the viewer's LEFT; door at the {'left' if s['door_end_street'] == 'low' else 'right'}"


def street_sort(T):
    """the east parade by rising street x (a viewer facing east sees them right to left), then the west block by rising street x (left to right)"""
    return sorted(T["shops"], key=lambda s: (0 if s["side"] == "east" else 1, s["street_x_m"][0]))


def sheet_all(T, setdir, out, date):
    W = 1600
    pad = 10
    lab = 26
    bw = W - 2 * pad
    bh = int(round(bw * 550 / 5410))
    shops = street_sort(T)
    n = len(shops)
    H = pad + n * (lab + bh + 8) + 2 * 22
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)
    f1, f2, f0 = font(15), font(12), font(14)
    y = pad
    last = None
    for s in shops:
        if s["side"] != last:
            last = s["side"]
            d.text((pad, y), "EAST PARADE: a viewer facing it has low street x on the RIGHT" if last == "east" else "WEST BLOCK: a viewer facing it has low street x on the LEFT", font=f0, fill=(240, 220, 150))
            y += 22
        im = load_board(setdir, s["id"]).resize((bw, bh), Image.LANCZOS)
        lo, hi = s["street_x_m"]
        d.text((pad, y + 3), f"{s['id']}", font=f1, fill=FG)
        d.text((pad + 190, y + 6), f"street x {lo:g} to {hi:g}; door at the {'right' if (s['side'] == 'east') == (s['door_end_street'] == 'low') else 'left'} of the board", font=f2, fill=(170, 168, 160))
        sheet.paste(im, (pad, y + lab))
        y += lab + bh + 8
    q, sz = save_jpeg(sheet, Path(out) / f"fascias-all-ten-v1-{date}.jpg")
    return f"fascias-all-ten-v1-{date}.jpg", sheet.size, q, sz


def sheet_board(T, setdir, out, date, bid, extra_overlay=None, name=None, centre=2705):
    s = fc.shop_by_id(T, bid)
    im = load_board(setdir, bid)
    W = 1600
    bh = int(round(W * 550 / 5410))
    top = im.resize((W, bh), Image.LANCZOS)
    mid = im.crop((centre - 800, 0, centre + 800, 550))
    if extra_overlay:
        im2 = extra_overlay(im)
        top = im2.resize((W, bh), Image.LANCZOS)
        mid = im2.crop((centre - 800, 0, centre + 800, 550))
    cap = 24
    H = cap + bh + 6 + cap + 550
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)
    f1 = font(14)
    tag = "  ·  PREVIEW ONLY: the raised gilt letters laid flat over the texture where the geometry stands" if extra_overlay else ""
    d.text((8, 4), f"{bid}  ·  the whole board, 5410 x 550 mm, left = the viewer's left  ·  {side_note(T, s)}{tag}", font=f1, fill=FG)
    sheet.paste(top, (0, cap))
    d.text((8, cap + bh + 6 + 4), f"1600 mm of the board at one pixel a millimetre (board x {centre - 800} to {centre + 800})", font=f1, fill=FG)
    sheet.paste(mid, (0, cap + bh + 6 + cap))
    fn = name or f"fascias-{bid.replace('_', '-')}-v1-{date}.jpg"
    q, sz = save_jpeg(sheet, Path(out) / fn)
    return fn, sheet.size, q, sz


def mickeys_overlay(T, setdir):
    """the raised letters laid flat over the texture: face brass_gilt, flanks brass_side 3 mm, where the geometry stands"""
    import fascia_paint as fp
    s = fc.shop_by_id(T, "mickeys")
    b = [x for x in s["blocks"] if not x["in_texture"]][0]
    face, _, win = fp.text_layers(T, dict(b, jitter=None), None, hand=False, shade=False, extra_pad=30)
    from scipy import ndimage as ndi
    m = ndi.binary_dilation(face > 0.5, iterations=2)
    # a little relief: the flank is the lower-left rim lit darker
    flank = ndi.binary_dilation(m, iterations=2) & ~m
    r0, r1, c0, c1 = win

    def f(im):
        arr = np.asarray(im).astype(np.float32).copy()
        sub = arr[r0:r1, c0:c1]
        gilt = np.array(fc.pal(T, "brass_gilt"), np.float32)
        side = np.array(fc.pal(T, "brass_side"), np.float32)
        sub[flank] = sub[flank] * 0.5 + side * 0.5
        sub[m] = gilt[None, :] * (1.0 + 0.04 * np.random.default_rng(1).standard_normal(sub[m].shape[0]))[:, None]
        arr[r0:r1, c0:c1] = sub
        return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    return f


def sphere_view(tex, size=260):
    """a lit sphere from an equirectangular texture (u round, v pole to pole), seen from the front, light up-left"""
    H, W = tex.shape[:2]
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    cx = cy = (size - 1) / 2.0
    X = (xx - cx) / (size / 2.0 - 2)
    Y = -(yy - cy) / (size / 2.0 - 2)
    r2 = X * X + Y * Y
    inside = r2 <= 1.0
    Z = np.sqrt(np.clip(1.0 - r2, 0, 1))
    lon = np.arctan2(X, Z)                     # -pi..pi, 0 facing us
    lat = np.arcsin(np.clip(Y, -1, 1))
    u = ((lon / (2 * np.pi) + 0.5 + 0.25) % 1.0) * (W - 1)
    v = (0.5 - lat / np.pi) * (H - 1)
    col = tex[v.astype(int), u.astype(int)].astype(np.float32)
    L = np.array([-0.45, 0.55, 0.70], np.float32)
    L /= np.linalg.norm(L)
    nd = np.clip(X * L[0] + Y * L[1] + Z * L[2], 0, 1)
    spec = np.clip(nd, 0, 1) ** 24
    out = col * (0.25 + 0.85 * nd[..., None]) + 90.0 * spec[..., None]
    out[~inside] = BG
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def sheet_signs_glass(T, setdir, out, date):
    man = json.loads((Path(setdir) / "manifest.json").read_text(encoding="utf-8"))
    W = 1600
    f1, f2, f3 = font(15), font(12), font(11)
    items = []
    # 1. the hanging signs
    row = []
    for h in man["hanging_signs"]:
        if h["id"] == "ritas_three_balls":
            for f in h["faces"][:3]:
                tex = np.asarray(Image.open(Path(setdir) / f["files"]["basecolour"]["file"]).convert("RGB"))
                row.append((sphere_view(tex), f"{h['id']}: ball {f['id'][-1]} (0.26 m, lit sphere)"))
        else:
            for f in h["faces"]:
                row.append((Image.open(Path(setdir) / f["files"]["basecolour"]["file"]).convert("RGB"), f"{h['id']}: face {f['id'][-1]}  {f['size_mm'][0]} x {f['size_mm'][1]} mm" + (f"  (cap {f['cap_mm_built']:g}, the target's {f['cap_mm_target']:g} will not fit)" if f["cap_mm_built"] != f["cap_mm_target"] else "")))
    # layout: flow into rows of 1600 px
    pad = 10
    pieces = []
    x, y, rowh = pad, pad + 20, 0
    placements = []
    for im, cap in row:
        w, h = im.size
        sc = 1.0 if w <= 430 else 430.0 / w
        if sc != 1.0:
            im = im.resize((int(w * sc), int(h * sc)), Image.LANCZOS)
            w, h = im.size
        if x + w + pad > W:
            x = pad
            y += rowh + 34
            rowh = 0
        placements.append((im, cap, x, y))
        x += w + pad
        rowh = max(rowh, h)
    y_signs_end = y + rowh + 40
    # 2. the glass rows on dark glass, grouped by shop
    glass_by = {}
    for g in man["glass_lettering"]:
        glass_by.setdefault(g["shop"], []).append(g)
    gy = y_signs_end + 24
    glass_rows = []
    gx, gh = pad, 0
    gy0 = gy
    for shop, rows in glass_by.items():
        for g in rows:
            im = Image.open(Path(setdir) / g["files"]["rgba"]["file"]).convert("RGBA")
            w, h = im.size
            if shop == "empty_unit" and g["kind"] == "glass_wash":
                im = im.resize((int(w * 0.28), int(h * 0.28)), Image.LANCZOS)
                w, h = im.size
            note = ""
            if w > W - 2 * pad - 8:   # the newsagent's line is 1686 mm wide: shrink it to the sheet (preview only)
                k = (W - 2 * pad - 8) / w
                im = im.resize((int(w * k), int(h * k)), Image.LANCZOS)
                w, h = im.size
                note = f" (shown at {k * 100:.0f} per cent)"
            bgc = (46, 52, 56) if shop != "empty_unit" else (40, 44, 46)
            tile = Image.new("RGBA", (w + 8, h + 8), bgc + (255,))
            tile.alpha_composite(im, (4, 4))
            cap = f"{shop}: {(g['string'] or 'whole window')[:28]}" + note
            if gx + tile.width + pad > W:
                gx = pad
                gy += gh + 20
                gh = 0
            glass_rows.append((tile.convert("RGB"), cap, gx, gy))
            gx += tile.width + pad
            gh = max(gh, tile.height)
    gy_end = gy + gh + 20
    # 3. panels
    px, py, ph = pad, gy_end + 24, 0
    panels = []
    for p in man["small_panels"]:
        im = Image.open(Path(setdir) / p["files"]["basecolour"]["file"]).convert("RGB")
        w, h = im.size
        if w > 460:
            im = im.resize((460, int(h * 460 / w)), Image.LANCZOS)
            w, h = im.size
        if px + w + pad > W:
            px = pad
            py += ph + 20
            ph = 0
        panels.append((im, p["id"].replace("hours_plate.", "plate ") + (f" (cap {p['cap_mm']:g})" if p.get("lines") else ""), px, py))
        px += w + pad
        ph = max(ph, h)
    H = py + ph + 24
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)
    d.text((pad, 4), "the hanging signs (each face reads left to right from its own side)", font=f1, fill=FG)
    for im, cap, x, y in placements:
        sheet.paste(im, (x, y))
        d.text((x, y + im.height + 3), cap, font=f3, fill=(170, 168, 160))
    d.text((pad, y_signs_end - 6), "glass lettering rows on dark glass (as seen from the street) and the empty unit's whitewashed window", font=f1, fill=FG)
    for im, cap, x, y in glass_rows:
        sheet.paste(im, (x, y))
        d.text((x, y + im.height + 2), cap, font=f3, fill=(170, 168, 160))
    d.text((pad, gy_end), "the letting board and the hours plates", font=f1, fill=FG)
    for im, cap, x, y in panels:
        sheet.paste(im, (x, y))
        d.text((x, y + im.height + 2), cap, font=f3, fill=(170, 168, 160))
    fn = f"fascias-signs-glass-v1-{date}.jpg"
    q, sz = save_jpeg(sheet, Path(out) / fn)
    return fn, sheet.size, q, sz


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("setdir")
    ap.add_argument("--out", default=str(fc.ROOT / "production" / "previews" / "cloud-week" / "fascias"))
    ap.add_argument("--date", default="2026-10-09")
    a = ap.parse_args(argv)
    T = fc.load_target()
    Path(a.out).mkdir(parents=True, exist_ok=True)
    res = [sheet_all(T, a.setdir, a.out, a.date)]
    for s in T["shops"]:
        res.append(sheet_board(T, a.setdir, a.out, a.date, s["id"]))
    res.append(sheet_board(T, a.setdir, a.out, a.date, "mickeys", extra_overlay=mickeys_overlay(T, a.setdir), name=f"fascias-mickeys-with-letters-v1-{a.date}.jpg", centre=4055))
    res.append(sheet_signs_glass(T, a.setdir, a.out, a.date))
    for fn, size, q, sz in res:
        print(f"{fn}  {size[0]}x{size[1]}  q{q}  {sz // 1000} KB")


if __name__ == "__main__":
    main()
