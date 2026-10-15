#!/usr/bin/env python
"""Rebuild the previews of the shopfront target in production/previews/cloud-week/refs/shopfronts/.

    make_previews.py [--work SCRATCH] [--previews DIR]

  P1-leadenhall-*.jpg                       the photograph's joinery crops (measure_leadenhall.py writes them)
  P1-leadenhall-*-target-on-photo.jpg       the drawing laid on each (target_drawing.py overlay)
  D1-ritas-bay-elevation.jpg                the target's elevation of Rita's whole bay (drawn at 1 mm to the pixel, reduced)
  D2-ten-fronts-sheet.jpg                   the ten fronts assembled from the table
  D3-parts-pilaster-console-fascia.jpg      pilaster variants, console, capital / console / fascia / cornice section
  D4-parts-sections.jpg                     sill, stallriser, transom, mullion, jamb, bead, threshold sections (x3)
  D5-cornice-ends-and-shutter.jpg           the cornice's mitred returns in plan; the roller shutter in section
JPEG, at most 1200 px on the long side, under 300 KB. Nothing here shows lettering, drink, gambling or children.
"""
import argparse
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import target_drawing as TD  # noqa: E402


def save_jpg(im, path, limit=295_000):
    if max(im.size) > 1200:
        s = 1200.0 / max(im.size)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    for q in (90, 86, 82, 78, 72, 66):
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) < limit:
            break
    print(path, im.size, os.path.getsize(path) // 1024, "KB")


def label(im, text):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 14], fill=(30, 30, 30))
    d.text((4, 2), text, fill=(240, 240, 240))
    return im


def fit(im, w, h):
    s = min(w / im.width, h / im.height)
    return im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--previews", default=os.path.join(HERE, "..", "..", "..", "previews", "cloud-week", "refs", "shopfronts"))
    ap.add_argument("--work", default="/tmp/shopfront_previews")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    t = json.load(open(os.path.join(HERE, "target.json")))
    # overlays
    for p in TD.overlay(t, a.previews, a.previews):
        print("overlay", os.path.basename(p), os.path.getsize(p) // 1024, "KB")
    # Rita's bay and the ten fronts
    save_jpg(TD.draw_bay(t, "ritas").render(1.0), os.path.join(a.previews, "D1-ritas-bay-elevation.jpg"))
    sheet = TD.sheet_all_fronts(t, scale=0.115)
    save_jpg(sheet, os.path.join(a.previews, "D2-ten-fronts-sheet.jpg"))
    # parts sheet 1: pilaster variants, console, section stack
    cells = []
    for v, paint in (("panel", TD.rgb(t, "oxblood")), ("flute", TD.rgb(t, "dark_green")), ("render", TD.rgb(t, "cream")), ("clad", TD.rgb(t, "slate"))):
        cells.append((TD.draw_pilaster(t, v, False, paint).render(1.0), "pilaster " + v))
    cells.append((TD.draw_console(t).render(1.0), "console: two-volute scroll in side view, grooves and bosses; front + leaf"))
    cells.append((TD.draw_cornice_fascia(t).render(1.0), "capital / console / fascia / cornice, side section"))
    W, H = 1200, 1100
    out = Image.new("RGB", (W, H), (236, 234, 228))
    x = 0
    for im, lab in cells[:4]:
        c = fit(im, 285, 560)
        out.paste(c, (x + 5, 20))
        ImageDraw.Draw(out).text((x + 5, 4), lab, fill=(20, 20, 20))
        x += 300
    im, lab = cells[4]
    c = fit(im, 560, 520)
    out.paste(c, (5, 600)); ImageDraw.Draw(out).text((5, 584), lab, fill=(20, 20, 20))
    im, lab = cells[5]
    c = fit(im, 620, 520)
    out.paste(c, (580, 600)); ImageDraw.Draw(out).text((580, 584), lab, fill=(20, 20, 20))
    save_jpg(out, os.path.join(a.previews, "D3-parts-pilaster-console-fascia.jpg"))
    # parts sheet 2: small sections at x3
    secs = []
    P = t["parts"]
    for nm, pr, fill in [("sill", P["sill"]["profiles"]["section"], (200, 200, 195)), ("transom T1", P["window_frame"]["profiles"]["transom_t1"], (200, 200, 195)),
                         ("stallriser panel", P["stallriser"]["variants"]["panel"]["section"], (150, 60, 60)), ("stallriser tile", P["stallriser"]["variants"]["tile"]["section"], (150, 60, 60)),
                         ("plinth cap", P["pilaster"]["profiles"]["plinth_cap_side"], (150, 100, 95)), ("plinth stepped, hollow head", P["pilaster"]["profiles"]["plinth_stepped_side"], (150, 100, 95)),
                         ("base ogee", P["pilaster"]["profiles"]["base_ogee"], (150, 100, 95)),
                         ("capital (neck at z 2540)", P["pilaster"]["profiles"]["capital_side"], (150, 100, 95)),
                         ("cornice", P["cornice"]["profiles"]["section"], (170, 140, 100)), ("fascia + bed mould", P["fascia_board"]["profiles"]["section"], (190, 190, 186)),
                         ("mullion T1 plan", P["window_frame"]["profiles"]["mullion_t1_plan"], (200, 200, 195)), ("mullion T2 plan", P["window_frame"]["profiles"]["mullion_t2_plan"], (200, 200, 195)),
                         ("mullion M1 plan", P["window_frame"]["profiles"]["mullion_m1_plan"], (200, 200, 195)), ("jamb T1 plan", P["window_frame"]["profiles"]["jamb_t1_plan"], (200, 200, 195)),
                         ("toplight bar plan", P["window_frame"]["profiles"]["toplight_bar_plan"], (200, 200, 195)),
                         ("shaft panel plan", P["pilaster"]["profiles"]["shaft_panel_plan"], (150, 100, 95)), ("shaft flute plan", P["pilaster"]["profiles"]["shaft_flute_plan"], (150, 100, 95)),
                         ("glazing bead (ovolo)", P["window_frame"]["profiles"]["glazing_bead_ovolo"], (200, 200, 195)), ("door threshold", P["shop_door"]["profiles"]["threshold_section"], (190, 184, 170))]:
        secs.append((nm, TD.draw_section(t, nm, pr, fill).render(1.0)))
    cols = 6
    cw, chh = 196, 240
    rows = (len(secs) + cols - 1) // cols
    out = Image.new("RGB", (cols * cw, rows * chh), (236, 234, 228))
    for i, (nm, im) in enumerate(secs):
        s = min((cw - 12) / im.width, (chh - 30) / im.height, 3.0)
        c = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        x, y = (i % cols) * cw, (i // cols) * chh
        out.paste(c, (x + 6, y + 22))
        ImageDraw.Draw(out).text((x + 6, y + 5), "%s (x%.1f)" % (nm, s), fill=(20, 20, 20))
    save_jpg(out, os.path.join(a.previews, "D4-parts-sections.jpg"))
    # sheet 5: the cornice's mitred returns in plan, and the roller shutter's lowered curtain in section
    ce = TD.draw_cornice_end(t).render(1.0)
    ss = TD.draw_shutter_section(t).render(1.0)
    out = Image.new("RGB", (1200, 1100), (236, 234, 228))
    c1 = fit(ce, 640, 420)
    out.paste(c1, (10, 30)); ImageDraw.Draw(out).text((10, 12), "cornice ends in plan: the neighbour's right return, the party line (the pipe), this bay's left return (mitres 45 degrees)", fill=(20, 20, 20))
    c2 = fit(ss, 460, 1000)
    out.paste(c2, (700, 60)); ImageDraw.Draw(out).text((700, 12), "roller shutter, lowered (side section): curtain d 170", fill=(20, 20, 20))
    ImageDraw.Draw(out).text((700, 28), "rails d 150-190, hood 210 deep set into the toplight zone (head cut away)", fill=(20, 20, 20))
    save_jpg(out, os.path.join(a.previews, "D5-cornice-ends-and-shutter.jpg"))


if __name__ == "__main__":
    main()
