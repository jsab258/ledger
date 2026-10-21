#!/usr/bin/env python
"""make_previews.py: the review previews of the paper set (units 4.2 to 4.4): contact sheets and 1:1 crops, JPEG, 1600 px at most, under 500 KB.

    /home/user/.bpyenv/bin/python make_previews.py OUTDIR PREVIEW_DIR [--tag v1] [--date 2026-10-12]

OUTDIR is what make_paper.py wrote. A sheet lays the delivered pictures of one group at one scale on a mid-grey ground (so that a torn edge, a hole or a sleeve's clear band shows as
grey), each labelled with its id and class. Crops are one pixel to the millimetre (or the item's own scale where that is smaller).
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_common as pc          # noqa: E402

GREY = (112, 108, 104)
MAXW = 1600

GROUPS = [
    ("bills-poll-tax-market", "poll tax, market, jumble and dance: the bills and the A3 photocopies", ["P01", "P02", "P03", "P04", "M01", "J01", "D01", "B01", "G02", "W01", "T03"], 0.40),
    ("bills-tivoli-ferry", "the Tivoli's quads and strip, the ferry sheets (A2)", ["T01", "T01s", "T02", "T02s", "F01", "F02", "G01"], 0.40),
    ("notices", "council, police and Harbour Board notices (A3 and A4), the sleeved ones", ["C01a", "C01b", "C01c", "C02", "C03", "H03", "H04", "H05"], 0.42),
    ("stickers-plates-boards", "stickers, enamel signs, letting boards and street name plates", ["P05", "P06", "K04", "K06b", "H01", "H02", "L02", "L03n", "L04", "L01", "L03", "S01n", "S01d", "S02n", "S02d", "S03n", "S03d"], 0.30),
    ("cards-shop", "shop-window cards: felt pen, printed, fish tickets, stars", ["K01", "K02", "K03a", "K03b", "K05", "K06a", "K06c", "K07a", "K07b", "K07c", "K07d", "K08", "K09a", "K09b", "K09c", "K09d", "K09e", "K09f", "SA15"], 1.0),
    ("cards-newsagent", "the newsagent's board: ballpoint record cards", ["SA%02d" % i for i in range(1, 15)], 1.6),
]


def font(px):
    for p in (pc.FONT_SRC / "archivo" / "Archivo-var.ttf", pc.FONT_SRC / "courier-prime" / "CourierPrime-Regular.ttf"):
        if p.exists():
            f = ImageFont.truetype(str(p), px)
            return f
    return ImageFont.load_default()


def load_item(out, row, cls=None):
    cls = cls or list(row["classes"])[0]
    c = row["classes"][cls]
    im = Image.open(Path(out) / c["basecolour"]["file"]).convert("RGBA")
    return im, cls


def save_jpeg(im, path, limit=500_000):
    q = 90
    while True:
        im.save(path, "JPEG", quality=q, optimize=True)
        if Path(path).stat().st_size <= limit or q <= 50:
            return
        q -= 5


def sheet(out, rows, ids, scale, title):
    f = font(15)
    items = []
    for i in ids:
        r = rows.get(i)
        if not r:
            continue
        im, cls = load_item(out, r)
        w = max(8, int(round(r["format_mm"][0] * scale)))
        h = max(8, int(round(r["format_mm"][1] * scale)))
        # sRGB-correct, premultiplied-free reduction: composite on the grey ground first
        bg = Image.new("RGBA", im.size, GREY + (255,))
        bg.alpha_composite(im)
        items.append((i, cls, bg.convert("RGB").resize((w, h), Image.LANCZOS)))
    pad = 10
    x, y, rowh = pad, pad + 24, 0
    placed = []
    for i, cls, im in items:
        if x + im.width + pad > MAXW:
            x, y, rowh = pad, y + rowh + 22 + pad, 0
        placed.append((x, y, i, cls, im))
        x += im.width + pad
        rowh = max(rowh, im.height)
    H = y + rowh + 22 + pad
    canvas = Image.new("RGB", (MAXW, H), (72, 70, 68))
    d = ImageDraw.Draw(canvas)
    d.text((pad, 6), title, font=f, fill=(235, 235, 230))
    for x, y, i, cls, im in placed:
        canvas.paste(im, (x, y))
        d.text((x, y + im.height + 3), "%s %s" % (i, cls), font=font(13), fill=(235, 235, 230))
    return canvas


def crop_mm(out, row, cls, box_mm, scale):
    """A crop of one picture, box_mm = (x0, y0, x1, y1) in the item's frame (y up from the bottom), shown at `scale` pixels to the millimetre on the grey ground."""
    im, cls = load_item(out, row, cls)
    ppm = row["px_per_mm"]
    W, H = row["format_mm"]
    x0, y0, x1, y1 = box_mm
    c = im.crop((int(x0 * ppm), int((H - y1) * ppm), int(x1 * ppm), int((H - y0) * ppm)))
    bg = Image.new("RGBA", c.size, GREY + (255,))
    bg.alpha_composite(c)
    c = bg.convert("RGB")
    return c.resize((max(1, int(round((x1 - x0) * scale))), max(1, int(round((y1 - y0) * scale)))), Image.LANCZOS)


def layout(crops, labels, gap=8):
    """Crops side by side, wrapping at MAXW, each labelled underneath."""
    f = font(13)
    x, y, rowh = gap, gap, 0
    placed = []
    for im, lab in zip(crops, labels):
        if x + im.width + gap > MAXW and x > gap:
            x, y, rowh = gap, y + rowh + 20 + gap, 0
        placed.append((x, y, im, lab))
        x += im.width + gap
        rowh = max(rowh, im.height)
    width = max(x + im.width for x, y, im, lab in placed) + gap
    canvas = Image.new("RGB", (width, y + rowh + 20 + gap), (72, 70, 68))
    d = ImageDraw.Draw(canvas)
    for x, y, im, lab in placed:
        canvas.paste(im, (x, y))
        d.text((x, y + im.height + 3), lab, font=f, fill=(235, 235, 230))
    return canvas


CROPS = [
    ("close-bill-poll-tax", "the head of a letterpress bill and the foot of a screen-printed one, 3 px/mm", [("P03", "B", (0, 540, 508, 762), 3.0), ("P01", "B", (0, 0, 508, 200), 3.0)]),
    ("close-bill-ferry", "the ferry sheet (litho, two colours), the table and the foot, 3 px/mm", [("F01", "B", (0, 0, 420, 330), 3.0)]),
    ("close-notice-typed", "an A4 typed notice and the planning notice in its sleeve, 4 px/mm", [("H03", "B", (0, 170, 210, 297), 4.0), ("C02", "A", (0, 170, 210, 297), 4.0)]),
    ("close-notice-photocopy", "the police appeal (A3 photocopy, four tabs) and the road closure notice (sleeve, beads), 3 px/mm", [("C01a", "B", (0, 210, 297, 420), 3.0), ("C03", "A", (0, 0, 297, 210), 3.0)]),
    ("close-cards", "felt-pen cards, a star, a ballpoint card and the string-hung card, 5 px/mm", [("K05", "B", (0, 0, 210, 148), 4.0), ("K09a", "B", (0, 0, 105, 74), 6.0), ("K07a", "B", (0, 0, 170, 170), 3.5), ("SA06", "B", (0, 0, 148, 105), 6.0), ("SA06", "C", (0, 0, 148, 105), 6.0), ("K01", "A", (0, 0, 210, 148), 3.0)]),
    ("close-plates", "the cast street plate (class D), an enamel sign (B) and a pressed plate (C), 1.5 px/mm", [("S01n", "D", (0, 0, 980, 200), 1.5), ("H01", "B", (0, 0, 600, 450), 1.5), ("S02n", "C", (0, 0, 1360, 200), 1.1)]),
    ("close-boards", "letting boards at class C, 2 px/mm", [("L01", "C", (0, 0, 1200, 450), 1.2), ("L03n", "C", (0, 0, 600, 400), 2.0)]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("prev")
    ap.add_argument("--tag", default="v1")
    ap.add_argument("--date", default="2026-10-12")
    a = ap.parse_args()
    out, prev = Path(a.out), Path(a.prev)
    prev.mkdir(parents=True, exist_ok=True)
    man = json.loads((out / "manifest.json").read_text())
    rows = {r["item"]: r for r in man["items"]}
    for name, title, ids, scale in GROUPS:
        ids = [i for i in ids if i in rows]
        if not ids:
            continue
        im = sheet(out, rows, ids, scale, title + "  (scale %.2f px/mm)" % scale)
        p = prev / ("paper-%s-%s-%s.jpg" % (name, a.tag, a.date))
        save_jpeg(im, p)
        print(p.name, im.size, p.stat().st_size // 1024, "KB")
    for name, title, parts in CROPS:
        crops = [crop_mm(out, rows[i], c, b, s) for i, c, b, s in parts if i in rows]
        labels = ["%s %s" % (i, c) for i, c, b, s in parts if i in rows]
        if not crops:
            continue
        im = layout(crops, labels)
        # a title strip
        strip = Image.new("RGB", (im.width, 24), (72, 70, 68))
        ImageDraw.Draw(strip).text((8, 4), title, font=font(14), fill=(235, 235, 230))
        full = Image.new("RGB", (im.width, im.height + 24))
        full.paste(strip, (0, 0))
        full.paste(im, (0, 24))
        if max(full.size) > MAXW:
            full.thumbnail((MAXW, MAXW), Image.LANCZOS)
        p = prev / ("paper-%s-%s-%s.jpg" % (name, a.tag, a.date))
        save_jpeg(full, p)
        print(p.name, full.size, p.stat().st_size // 1024, "KB")
    sb = out / "SB1" / "SB1_B_basecolour.png"
    if sb.exists():
        im = Image.open(sb).convert("RGBA")
        bg = Image.new("RGBA", im.size, (150, 170, 175, 255))
        bg.alpha_composite(im)
        bg = bg.convert("RGB")
        bg.thumbnail((MAXW, 1200))
        p = prev / ("paper-board-sb1-%s-%s.jpg" % (a.tag, a.date))
        save_jpeg(bg, p)
        print(p.name, bg.size, p.stat().st_size // 1024, "KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
