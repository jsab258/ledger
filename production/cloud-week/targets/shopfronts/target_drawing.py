#!/usr/bin/env python
"""Draw the shopfront target from target.json ALONE, as filled polygons in millimetres, at 1 mm to the
pixel: each part's elevation and sections, an elevation of Rita's whole bay, and (optionally) the
Leadenhall instance laid on the photograph's previews.

    target_drawing.py OUT_DIR [--json drawing.json] [--target target.json] [--shop ritas]
                      [--all-fronts] [--sections-x4] [--photos PREVIEW_DIR --overlay-out DIR]

Pictures go to OUT_DIR (never into git except production/previews/). drawing.json holds every polygon
that was drawn: {"drawings": {name: {"px_per_mm": 1, "bbox": [...], "polygons": [{"name", "pts", "fill"}]}}}.
Elevation frame: u across the bay from the viewer's left, z up. Section frames: d-z with the wall at
the left and the street to the right; u-d plans with the street at the bottom.
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))


def rgb(t, paint_id, default=(160, 160, 160)):
    p = t["paints"].get(paint_id) if paint_id else None
    return tuple(p["srgb"]) if p else default


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


class Sheet:
    """A drawing: polygons in mm, painted in order, y flipped so that z (or -d) goes up the page."""

    def __init__(self, name, bbox, flip="z", margin=20, bg=(236, 234, 228)):
        self.name, self.bbox, self.flip, self.margin, self.bg = name, bbox, flip, margin, bg
        self.polys = []

    def add(self, name, pts, fill, outline=None):
        self.polys.append({"name": name, "pts": [[round(float(a), 2), round(float(b), 2)] for a, b in pts], "fill": list(fill),
                           "outline": list(outline) if outline else None})

    def rect(self, name, x0, y0, x1, y1, fill, outline=None):
        self.add(name, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, outline)

    def size(self):
        x0, y0, x1, y1 = self.bbox
        return int(round(x1 - x0)) + 2 * self.margin, int(round(y1 - y0)) + 2 * self.margin

    def to_px(self, p, scale=1.0):
        x0, y0, x1, y1 = self.bbox
        x = (p[0] - x0 + self.margin) * scale
        if self.flip == "z":
            y = (y1 - p[1] + self.margin) * scale
        else:                       # plan: second axis grows DOWN the page (street at the bottom)
            y = (p[1] - y0 + self.margin) * scale
        return (x, y)

    def render(self, scale=1.0):
        w, h = self.size()
        im = Image.new("RGB", (int(w * scale), int(h * scale)), self.bg)
        d = ImageDraw.Draw(im)
        for p in self.polys:
            pp = [self.to_px(q, scale) for q in p["pts"]]
            d.polygon(pp, fill=tuple(p["fill"]), outline=tuple(p["outline"]) if p["outline"] else None)
        return im

    def record(self):
        return {"px_per_mm": 1, "bbox": [round(v, 1) for v in self.bbox], "margin_px": self.margin, "frame": "u-z elevation" if self.flip == "z" else "plan or section",
                "polygons": self.polys}


GLASS = (178, 190, 196)
DARK = (70, 72, 74)


def poly_section(sheet, name, pts, fill, outline=(30, 30, 30)):
    sheet.add(name, pts, fill, outline)


# ---- parts ---------------------------------------------------------------------------------------
def draw_pilaster(t, variant, mirror=False, paint=(150, 40, 45), name=None):
    P = t["parts"]["pilaster"]
    sh = Sheet(name or "pilaster_" + variant, (-30, -20, 380, 2880))
    for q in P["variants"][variant]["elevation"]:
        pts = q["pts"]
        if mirror:
            pts = [[350 - a, b] for a, b in pts]
        f = paint
        if q["kind"] == "sunk":
            f = shade(paint, 0.72)
        elif q["kind"] == "raised":
            f = shade(paint, 1.12)
        sh.add(q["name"], pts, f, shade(paint, 0.5))
    return sh


def draw_section(t, name, prof, fill=(150, 120, 90), scale_note=""):
    pts = prof["points"]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    flip = "z" if prof["plane"] in ("d-z", "a-p", "u-z") else "plan"
    sh = Sheet(name, (min(xs) - 4, min(ys) - 4, max(xs) + 4, max(ys) + 4), flip=flip, margin=12)
    sh.add(name, pts, fill, (20, 20, 20))
    return sh


def draw_console(t):
    C = t["parts"]["console"]
    sh = Sheet("console_side_and_front", (-300, -20, 330, 580), margin=20)
    side = C["profiles"]["side_silhouette"]["points"]
    sh.add("side", [[a + 20, b] for a, b in side], (150, 120, 90), (20, 20, 20))
    vol = C["profiles"]["volute_spiral"]["points"]
    for i in range(len(vol) - 1):
        a, b = vol[i], vol[i + 1]
        sh.add("volute_%d" % i, [(a[0] + 20 - 1.5, a[1]), (b[0] + 20 - 1.5, b[1]), (b[0] + 20 + 1.5, b[1] + 1.5), (a[0] + 20 + 1.5, a[1] + 1.5)], (80, 55, 40))
    for q in C["variants"]["scroll"]["elevation"]:
        pts = [[a - 150, b] for a, b in q["pts"]]
        sh.add("front_" + q["name"], pts, (160, 130, 100) if q["kind"] == "face" else (190, 160, 125), (20, 20, 20))
    return sh


def draw_cornice_fascia(t):
    Co = t["parts"]["cornice"]["profiles"]["section"]["points"]
    Fa = t["parts"]["fascia_board"]["profiles"]["section"]["points"]
    Cn = t["parts"]["console"]["profiles"]["side_silhouette"]["points"]
    Pi = t["parts"]["pilaster"]["profiles"]["capital_side"]["points"]
    sh = Sheet("fascia_cornice_console_capital_section", (-10, 2540, 230, 3560), margin=20)
    sh.add("capital", [[a, b + 2540] for a, b in Pi], (130, 60, 60), (20, 20, 20))
    sh.add("console", [[a, b + 2850] for a, b in Cn], (150, 120, 90), (20, 20, 20))
    sh.add("fascia_board", [[a, b + 2850] for a, b in Fa], (190, 190, 186), (20, 20, 20))
    sh.add("cornice", [[a, b + 3400] for a, b in Co], (170, 140, 100), (20, 20, 20))
    return sh


def draw_sill_stallriser(t):
    Si = t["parts"]["sill"]["profiles"]["section"]["points"]
    Sp = t["parts"]["stallriser"]["variants"]["panel"]["section"]["points"]
    Tp = t["parts"]["window_frame"]["profiles"]["transom_t1"]["points"]
    Pl = t["parts"]["pilaster"]["profiles"]["plinth_panel_side_through_stile"]["points"]
    sh = Sheet("sill_stallriser_transom_section", (-10, -10, 210, 2500), margin=20)
    sh.add("stallriser", Sp, (150, 60, 60), (20, 20, 20))
    sh.add("sill", Si, (200, 200, 195), (20, 20, 20))
    sh.add("transom", [[a, b + 2400] for a, b in Tp], (200, 200, 195), (20, 20, 20))
    sh.add("glass", [(30, 690), (36, 690), (36, 2400), (30, 2400)], GLASS)
    return sh


def stall_panels(sh, t, shop, w0, w1, cols):
    sv = shop["stallriser"]["variant"]
    c = cols["stallriser"]
    if sv == "panel":
        n = shop["glazing_layout"]["mullion_centres"]
        xs = [w0] + [w0 + m for m in n] + [w1]
        sh.rect("stall_plinth", w0, 0, w1, 120, shade(c, 0.9), shade(c, 0.5))
        sh.rect("stall_bottom_rail", w0, 120, w1, 200, c, shade(c, 0.5))
        sh.rect("stall_top_rail", w0, 445, w1, 525, c, shade(c, 0.5))
        for k in range(len(xs) - 1):
            a = xs[k] + (80 if k == 0 else 40)
            b = xs[k + 1] - (80 if k == len(xs) - 2 else 40)
            sh.rect("stall_panel_%d" % k, a, 200, b, 445, shade(c, 0.78), shade(c, 0.5))
            sh.rect("stall_field_%d" % k, a + 35, 235, b - 35, 410, shade(c, 1.1), shade(c, 0.5))
        for m in n:
            sh.rect("stall_muntin", w0 + m - 40, 200, w0 + m + 40, 445, c, shade(c, 0.5))
    elif sv in ("tile_square", "tile_patterned"):
        sh.rect("stall_tiles", w0, 0, w1, 525, c, shade(c, 0.5))
        sh.rect("stall_skirting", w0, 0, w1, 100, rgb(t, shop["stallriser"].get("skirting", "tile_black")), (20, 20, 20))
        rows = [(100.0, 255.4), (255.4, 410.8), (410.8, 490.0)]          # two full courses and a half course
        for (za, zb) in rows:
            sh.rect("stall_joint_h", w0 + 2, za - 1.5, w1 - 2, za + 1.5, (110, 108, 100))
            x = w0 + 155.4
            while x < w1 - 4:
                sh.rect("stall_joint_v", x - 1.5, za, x + 1.5, zb, (110, 108, 100))
                x += 155.4
        sh.rect("stall_joint_h", w0 + 2, 488.5, w1 - 2, 491.5, (110, 108, 100))
        sh.rect("stall_cap", w0, 490, w1, 525, shade(c, 1.05), shade(c, 0.5))
        if sv == "tile_patterned":
            blue = rgb(t, shop["stallriser"].get("motif"))
            k = 0
            xx = w0
            while xx + 155.4 <= w1:
                for r, (za, zb) in enumerate(rows[:2]):
                    cx, cz = xx + 77.7, (za + zb) / 2
                    dark = (k + r) % 2 == 0
                    sh.add("stall_motif", [(cx, cz - 58), (cx + 58, cz), (cx, cz + 58), (cx - 58, cz)], blue if dark else (30, 30, 32))
                xx += 155.4
                k += 1
    elif sv == "slab":
        sh.rect("stall_slabs", w0, 0, w1, 525, c, shade(c, 0.4))
        for k in (1, 2):
            x = w0 + (w1 - w0) * k / 3
            sh.rect("slab_joint", x - 1.5, 0, x + 1.5, 525, (20, 20, 20))
        sh.rect("chrome_cap", w0, 507, w1, 525, rgb(t, "chrome"))
    elif sv == "boarded":
        sh.rect("ply", w0, 0, w1, 525, shade(c, 1.5), shade(c, 0.6))
        for k in range(12):
            sh.add("screw", [(w0 + 60 + k * (w1 - w0 - 120) / 11 - 4, 60 if k % 2 else 460), (w0 + 60 + k * (w1 - w0 - 120) / 11 + 4, 60 if k % 2 else 460), (w0 + 60 + k * (w1 - w0 - 120) / 11, 68 if k % 2 else 468)], (30, 30, 30))
    else:
        sh.rect("stall_render", w0, 0, w1, 525, c, shade(c, 0.5))
        sh.rect("stall_plinth", w0, 0, w1, 120, shade(c, 0.85))
    sh.rect("sill", w0, 525, w1, 600, shade(cols["window_frame"], 1.0), shade(cols["window_frame"], 0.5))
    sh.rect("sill_shadow", w0, 525, w1, 535, shade(cols["window_frame"], 0.55))


def window(sh, t, shop, w0, w1, cols):   # every name starts win_
    g = shop["glazing_layout"]
    c = cols["window_frame"]
    jw, mw = g["jamb_face"], g["mullion_face"]
    sh.rect("win_glass_lower", w0, 600, w1, 2400, GLASS)
    sh.rect("win_glass_top", w0, 2480, w1, 2790, GLASS)
    sh.rect("win_bottom_rail", w0, 600, w1, 690, c, shade(c, 0.5))
    sh.rect("win_jamb_l", w0, 600, w0 + jw, 2850, c, shade(c, 0.5))
    sh.rect("win_jamb_r", w1 - jw, 600, w1, 2850, c, shade(c, 0.5))
    for m in g["mullion_centres"]:
        sh.rect("win_mullion", w0 + m - mw / 2, 690, w0 + m + mw / 2, 2400, c, shade(c, 0.5))
    sh.rect("win_transom", w0, 2400, w1, 2480, c, shade(c, 0.5))
    bw = 28.0 if shop["glazing"]["window_frame"] != "M1" else 50.0
    for b in g["toplight_bar_centres"]:
        sh.rect("win_toplight_bar", w0 + b - bw / 2, 2480, w0 + b + bw / 2, 2790, c, shade(c, 0.5))
    sh.rect("win_head", w0, 2790, w1, 2850, c, shade(c, 0.5))


def shop_door(sh, t, shop, s0, s1, cols):
    c = cols["shop_door"]
    var = shop["shop_door"]
    D = t["parts"]["shop_door"]["dims"]
    sh.rect("door_frame_l", s0, 25, s0 + 50, 2400, cols["window_frame"] if var != "T1" else c, shade(c, 0.5))
    sh.rect("door_frame_r", s1 - 50, 25, s1, 2400, cols["window_frame"] if var != "T1" else c, shade(c, 0.5))
    sh.rect("door_head", s0 + 50, 2071, s1 - 50, 2131, c, shade(c, 0.5))
    sh.rect("door_fanlight", s0 + 50, 2131, s1 - 50, 2400, GLASS)
    sh.rect("door_transom_over_door", s0, 2400, s1, 2480, cols["window_frame"], shade(c, 0.5))
    sh.rect("door_toplight", s0, 2480, s1, 2790, GLASS)
    for k in (1, 2):
        x = s0 + (s1 - s0) * k / 3
        sh.rect("door_toplight_bar", x - 14, 2480, x + 14, 2790, cols["window_frame"])
    sh.rect("door_head", s0, 2790, s1, 2850, cols["window_frame"], shade(c, 0.5))
    lu0, lu1 = s0 + 53, s1 - 53
    lz0, lz1 = 28, 2068
    sh.rect("door_leaf", lu0, lz0, lu1, lz1, c, shade(c, 0.5))
    if var == "T1":
        gf = D["glazed_from"] + lz0
        sh.rect("door_glass", lu0 + 115, gf, lu1 - 115, lz1 - 115, GLASS, shade(c, 0.5))
        sh.rect("door_lower_panel", lu0 + 115, lz0 + 230, lu1 - 115, lz0 + 590, shade(c, 0.78), shade(c, 0.5))
        sh.rect("door_lower_field", lu0 + 150, lz0 + 262, lu1 - 150, lz0 + 560, shade(c, 1.1), shade(c, 0.5))
        sh.rect("door_kick_plate", lu0 + 65, lz0, lu1 - 65, lz0 + 170, rgb(t, shop["paints"].get("metal", "brass")), (60, 50, 20))
    else:
        sh.rect("door_glass", lu0 + 50, lz0 + 170, lu1 - 50, lz1 - 100, GLASS, shade(c, 0.5))
        sh.rect("door_kick_plate", lu0 + 50, lz0, lu1 - 50, lz0 + 170, shade(c, 0.9), shade(c, 0.5))
    hx = lu1 - 62
    sh.rect("door_handle_backplate", hx - 20, 880, hx + 20, 1120, rgb(t, shop["paints"].get("metal", "brass")), (60, 50, 20))
    sh.rect("door_foot_strip", lu0, lz0, lu1, lz0 + 30, rgb(t, "brass"), (60, 50, 20))
    sh.rect("door_threshold", s0, 0, s1, 25, rgb(t, "terrazzo"), (90, 90, 90))


def side_slot(sh, t, shop, a0, a1, cols):
    S = t["parts"]["side_door_slot"]["dims"]
    c = cols["side_door"] or (60, 60, 60)
    pier = cols["pilaster"]
    ca, cb = a0 + 24.4, a1 - 24.4
    sh.rect("slot_filler_l", a0, 0, ca, 2400, pier, shade(pier, 0.5))
    sh.rect("slot_filler_r", cb, 0, a1, 2400, pier, shade(pier, 0.5))
    sh.rect("slot_f1_frame", ca, 45, cb, 2400, shade(c, 0.9), shade(c, 0.5))
    mid = (a0 + a1) / 2
    lu0, lu1 = mid - 419, mid + 419
    lz0 = 55
    sh.rect("slot_leaf", lu0, lz0, lu1, lz0 + 1981, c, shade(c, 0.5))
    for (u0, u1, v0, v1) in S["leaf_panels_uv_mm"]:
        sh.rect("slot_panel", lu0 + u0, lz0 + v0, lu0 + u1, lz0 + v1, shade(c, 0.8), shade(c, 0.5))
    sh.rect("slot_f1_transom", ca, 2015.6, cb, 2117.6, c, shade(c, 0.5))
    sh.rect("slot_fanlight", ca + 49 - 24.4 + 10, 2117.6, cb - 49 + 24.4 - 10, 2330, GLASS)
    sh.rect("slot_transom", a0, 2400, a1, 2480, cols["window_frame"], shade(c, 0.5))
    sh.rect("slot_head_panel", a0 + 50, 2480, a1 - 50, 2790, shade(cols["window_frame"], 0.85), shade(c, 0.5))
    sh.rect("slot_head", a0, 2790, a1, 2850, cols["window_frame"], shade(c, 0.5))
    sh.rect("slot_letter_plate", mid + 70, lz0 + 1000 - 20, mid + 70 + 250, lz0 + 1000 + 20, rgb(t, "brass"), (60, 50, 20))


def draw_bay(t, shop_id, with_neighbours=True):
    shop = [s for s in t["shops"] if s["id"] == shop_id][0]
    cols = {k: rgb(t, v) for k, v in shop["paints"].items() if v}
    cols.setdefault("side_door", None)
    cols.setdefault("window_frame", rgb(t, "white_joinery"))
    cols.setdefault("fascia_board", cols.get("cornice"))
    ex = 420 if with_neighbours else 0
    sh = Sheet("bay_" + shop_id, (-ex, -30, 6000 + ex, 3600), margin=20, bg=(120, 116, 108))
    P = t["parts"]
    pv = shop["pilaster"]
    wall = (150, 70, 58)
    sh.rect("wall", -ex, 0, 6000 + ex, 3600, wall)
    # neighbours (grey, the party-wall pair)
    if with_neighbours:
        for (ox, mir) in ((-350, True), (6000, False)):
            for q in P["pilaster"]["variants"]["panel"]["elevation"]:
                pts = [[(350 - a if mir else a) + ox, b] for a, b in q["pts"]]
                sh.add("nb_" + q["name"], pts, (110, 108, 104), (70, 70, 70))
        for (cx) in (-175, 6175):
            sh.rect("nb_console", cx - 120, 2850, cx + 120, 3400, (110, 108, 104), (70, 70, 70))
    # pilasters
    for ox, mir in ((0, False), (5650, True)):
        for q in P["pilaster"]["variants"][pv]["elevation"]:
            pts = [[(350 - a if mir else a) + ox, b] for a, b in q["pts"]]
            f = cols["pilaster"]
            if q["kind"] == "sunk":
                f = shade(f, 0.72)
            elif q["kind"] == "raised":
                f = shade(f, 1.12)
            sh.add(("pil_" + q["name"]), pts, f, shade(cols["pilaster"], 0.5))
    # layout
    z = shop["zones_u"]
    w0, w1 = z["window"]
    # backdrop between piers
    sh.rect("opening", 350, 0, 5650, 2850, (60, 58, 56))
    stall_panels(sh, t, shop, w0, w1, cols)
    window(sh, t, shop, w0, w1, cols)
    s0, s1 = z["shop_door"]
    shop_door(sh, t, shop, s0, s1, cols)
    if z["side_door"]:
        side_slot(sh, t, shop, z["side_door"][0], z["side_door"][1], cols)
    # fascia, consoles, cornice
    sh.rect("fascia_board", 295, 2850, 5705, 3400, cols["fascia_board"], shade(cols["fascia_board"], 0.5))
    sh.rect("bed_mould", 295, 2850, 5705, 2890, shade(cols["fascia_board"], 0.8))
    for cx in (175, 5825):
        absent = shop.get("console_absent_viewer") == "L" and cx == 175
        if absent:
            sh.rect("console_stump", cx - 120, 2850, cx + 120, 2940, cols["console"], shade(cols["console"], 0.5))
        elif shop["console"] == "scroll":
            sh.rect("console", cx - 120, 2850, cx + 120, 3400, cols["console"], shade(cols["console"], 0.5))
            leaf = P["console"]["variants"]["scroll"]["elevation"][1]["pts"]
            sh.add("console_leaf", [[a + cx, b + 2850] for a, b in leaf], shade(cols["console"], 1.18), shade(cols["console"], 0.6))
        else:
            sh.rect("console_block", cx - 120, 2850, cx + 120, 3400, cols["console"], shade(cols["console"], 0.5))
    sh.rect("cornice", 54, 3400, 5946, 3550, cols["cornice"], shade(cols["cornice"], 0.5))
    sh.rect("cornice_shadow", 54, 3400, 5946, 3425, shade(cols["cornice"], 0.55))
    # the downpipe at the party lines, over the pair
    if with_neighbours:
        for px in (0, 6000):
            sh.rect("downpipe", px - 34, 0, px + 34, 3700 if False else 3550, (70, 72, 74), (30, 30, 30))
    # alterations that show in elevation
    if "roller_shutter" in shop["alterations"]:
        sh.rect("shutter_hood", w0 if w0 < s0 else s0, 2550, max(w1, s1), 2850, rgb(t, "steel_grey"), (30, 30, 30))
        for gx in (w0, max(w1, s1) - 50):
            sh.rect("guide_rail", gx, 0, gx + 50, 2550, rgb(t, "steel_grey"), (30, 30, 30))
    return sh


def sheet_all_fronts(t, scale=0.16):
    ims = []
    for s in t["shops"]:
        ims.append((s["id"], draw_bay(t, s["id"], with_neighbours=False).render(scale)))
    w, h = ims[0][1].size
    cols = 2
    rows = (len(ims) + 1) // 2
    out = Image.new("RGB", (cols * w, rows * (h + 18)), (236, 234, 228))
    d = ImageDraw.Draw(out)
    for i, (n, im) in enumerate(ims):
        x, y = (i % cols) * w, (i // cols) * (h + 18)
        out.paste(im, (x, y + 18))
        d.text((x + 6, y + 3), "%s (%s)" % (n, t["shops"][i]["kind"][:60]), fill=(20, 20, 20))
    return out


def overlay(t, photo_dir, out_dir):
    ph = t["photo"]
    written = []
    for inst in ph["instance_polys_px"]:
        cn = inst["crop"]
        src = os.path.join(photo_dir, ph["previews"][cn])
        if not os.path.exists(src):
            continue
        x0, y0, w, h = ph["crops"][cn]
        im = Image.open(src).convert("RGB")
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        for q in inst["polys"]:
            pts = [(a - x0, b - y0) for a, b in q["pts"]]
            d.polygon(pts, fill=(0, 255, 255, 46), outline=(0, 255, 255, 255))
        im2 = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
        name = ph["previews"][cn].replace(".jpg", "-target-on-photo.jpg")
        p = os.path.join(out_dir, name)
        for q in (88, 82, 76, 70):
            im2.save(p, quality=q, optimize=True)
            if os.path.getsize(p) < 295000:
                break
        written.append(p)
    return written


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--target", default=os.path.join(HERE, "target.json"))
    ap.add_argument("--json", default=None)
    ap.add_argument("--shop", default="ritas")
    ap.add_argument("--all-fronts", action="store_true")
    ap.add_argument("--photos", default=None, help="folder holding the P1 previews")
    ap.add_argument("--overlay-out", default=None)
    a = ap.parse_args()
    t = json.load(open(a.target))
    os.makedirs(a.out_dir, exist_ok=True)
    rec = {}

    def save(sh, name=None, scale=1.0):
        name = name or sh.name
        rec[name] = sh.record()
        im = sh.render(scale)
        im.save(os.path.join(a.out_dir, name + ".png"), optimize=True)
        return im
    P = t["parts"]
    # part elevations and sections at 1 mm to the pixel
    for v, paint in (("panel", rgb(t, "oxblood")), ("flute", rgb(t, "dark_green")), ("render", rgb(t, "cream")), ("clad", rgb(t, "slate"))):
        save(draw_pilaster(t, v, False, paint))
    save(draw_console(t))
    save(draw_cornice_fascia(t))
    save(draw_sill_stallriser(t))
    pr = P["pilaster"]["profiles"]
    for k in ("plinth_cap_side", "plinth_panel_side_through_field", "plinth_stepped_side", "capital_side", "shaft_panel_plan",
              "shaft_flute_plan", "shaft_render_plan", "clad_plan"):
        save(draw_section(t, "pilaster_section_" + k, pr[k], (150, 100, 95)))
    for k, v in P["window_frame"]["profiles"].items():
        save(draw_section(t, "window_section_" + k, v, (200, 200, 195)))
    save(draw_section(t, "cornice_section", P["cornice"]["profiles"]["section"], (170, 140, 100)))
    save(draw_section(t, "sill_section", P["sill"]["profiles"]["section"], (200, 200, 195)))
    save(draw_section(t, "fascia_section", P["fascia_board"]["profiles"]["section"], (190, 190, 186)))
    save(draw_section(t, "console_leaf_outline", P["console"]["profiles"]["leaf_outline"], (190, 160, 125)))
    for k, v in P["stallriser"]["variants"].items():
        if "section" in v:
            save(draw_section(t, "stallriser_section_" + k, v["section"], (150, 60, 60)))
    save(draw_section(t, "shop_door_threshold_section", P["shop_door"]["profiles"]["threshold_section"], (190, 184, 170)))
    # Rita's whole bay at 1 mm to the pixel, then the ten fronts
    bay = draw_bay(t, a.shop)
    save(bay, "bay_elevation_" + a.shop)
    if a.all_fronts:
        for s in t["shops"]:
            if s["id"] != a.shop:
                rec["bay_" + s["id"]] = draw_bay(t, s["id"]).record()
        sheet_all_fronts(t).save(os.path.join(a.out_dir, "ten_fronts_sheet.png"), optimize=True)
    if a.photos:
        od = a.overlay_out or a.out_dir
        os.makedirs(od, exist_ok=True)
        for p in overlay(t, a.photos, od):
            print("overlay", p)
    if a.json:
        json.dump({"drawings": rec, "target": os.path.basename(a.target), "units": "mm"}, open(a.json, "w"))
    print("drew %d drawings into %s" % (len(rec), a.out_dir))


if __name__ == "__main__":
    main()
