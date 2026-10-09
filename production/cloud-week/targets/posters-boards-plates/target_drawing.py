"""Draws the posters, notices, cards, boards and plates of target.json, from target.json ALONE.

    /home/user/.bpyenv/bin/python target_drawing.py OUT_DIR [--fonts DIR] [--only ID[,ID...]] [--no-text]

Writes into OUT_DIR (never into git; pictures belong in production/previews/ only when reduced):
    drawing.json          the polygons in millimetres: every item's sheet, shapes, ink boxes, baselines, fixing holes and art slots;
                          the surfaces' elevations in metres; the cases
    items/<ID>.png        each item at 1 pixel to the millimetre: the ground colour (aged class B), the shapes, the lettering rendered clean
                          from its font where the font file is found, each block's INK BOX (magenta) and BASELINE (cyan), the safe zone (grey)
    sheet_*.png           contact sheets (bills, cards, boards and plates)
    elevation_*.png       SF1 (the quay gable with its downpipe), SF2 (the empty unit's glass), piers (the plain west row), plates (where the name plates stand); the default placements only
    case_*.png            the two notice cases and the photographed case's proportions

The fonts are looked up in DIR (--fonts, $PBP_FONTS), then production/fonts. A missing font is not an error: the block is drawn as a box.
"""
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SCRATCH_FONTS = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/posters/fonts"
FONT_DIR = os.environ.get("PBP_FONTS", SCRATCH_FONTS)
NO_TEXT = "--no-text" in sys.argv
if "--fonts" in sys.argv:
    FONT_DIR = sys.argv[sys.argv.index("--fonts") + 1]

T = json.loads((HERE / "target.json").read_text(encoding="utf-8"))
FONTS = T["fonts"]
_fcache = {}


def font_for(key, weight, px):
    k = (key, weight, round(px, 2))
    if k in _fcache:
        return _fcache[k]
    spec = FONTS[key]
    f = None
    for base in (Path(FONT_DIR), ROOT / "production" / "fonts"):
        for cand in (base / spec["file"], base / Path(spec["file"]).name):
            if cand.exists():
                try:
                    f = ImageFont.truetype(str(cand), px, layout_engine=ImageFont.Layout.RAQM)
                    if spec["axes"]:
                        vals = []
                        for a in f.get_variation_axes():
                            n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
                            v = spec["axes"].get(n, a["default"])
                            if v is None:
                                v = weight
                            vals.append(min(max(v, a["minimum"]), a["maximum"]))
                        f.set_variation_by_axes(vals)
                except Exception:
                    f = None
                break
        if f:
            break
    _fcache[k] = f
    return f


def rgb(c):
    return tuple(int(v) for v in c)


def ground_rgb(item):
    """The aged (class B) ground of a sheet, or of a painted board/plate its face colour."""
    pal = T["palette"]
    for sh in item["shapes"]:
        if sh["id"] == "face" and sh.get("fill_kind") == "paint":
            return rgb(pal["paints"][sh["fill"]]["aged"]["B"])
    if item["stock"]:
        return rgb(pal["stocks"][item["stock"]]["aged"]["B"])
    return (200, 200, 200)


def fill_rgb(sh):
    pal = T["palette"]
    f, k = sh.get("fill"), sh.get("fill_kind")
    if f == "paper" or f == "white":
        return None
    if f in pal["stocks"]:
        return rgb(pal["stocks"][f]["aged"]["B"])
    if k == "paint" and f in pal["paints"]:
        return rgb(pal["paints"][f]["aged"]["B"])
    if k == "ink" and f in pal["inks"] and pal["inks"][f]["fresh"]:
        return tuple(int(v * 0.9) for v in pal["inks"][f]["fresh"])
    if f in pal["inks"] and pal["inks"][f]["fresh"]:
        return rgb(pal["inks"][f]["fresh"])
    if f in pal["paints"]:
        return rgb(pal["paints"][f]["aged"]["B"])
    return (60, 60, 60)


def block_rgb(item, b):
    pal = T["palette"]
    k = b["ink"]
    if k in pal["paints"]:
        return rgb(pal["paints"][k]["aged"]["B"])
    if k == "paper":
        return rgb(pal["stocks"][item["stock"]]["aged"]["B"]) if item["stock"] else (240, 240, 240)
    if k in pal["inks"] and pal["inks"][k]["fresh"]:
        return rgb(pal["inks"][k]["fresh"])
    return (20, 20, 20)


def draw_text(img_draw, item, b, H):
    cap, key, wt = b["cap_mm"], b["font"], b["weight"]
    px = b["size_px_per_em"]
    f = font_for(key, wt, px)
    if f is None:
        return False
    trk = b["tracking_em"] * px
    text = b["text"]
    xs = [f.getlength(text[:i + 1]) - f.getlength(ch) + i * trk for i, ch in enumerate(text)]
    col = block_rgb(item, b)
    base_y = H - b["baseline_mm"]
    for i, ch in enumerate(text):
        if ch != " ":
            img_draw.text((b["origin_x_mm"] + xs[i], base_y), ch, font=f, fill=col, anchor="ls")
    return True


def polys_for(item):
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    P = [dict(kind="sheet", id="sheet", pts=[[0, 0], [W, 0], [W, H], [0, H]])]
    sx0, sy0, sx1, sy1 = item["safe_mm"]
    P.append(dict(kind="safe", id="safe", pts=[[sx0, sy0], [sx1, sy0], [sx1, sy1], [sx0, sy1]]))
    for sh in item["shapes"]:
        if sh.get("box_mm"):
            x0, y0, x1, y1 = sh["box_mm"]
            P.append(dict(kind="shape:" + sh["kind"], id=sh["id"], pts=[[x0, y0], [x1, y0], [x1, y1], [x0, y1]], fill=sh.get("fill")))
        elif sh.get("pts_mm"):
            P.append(dict(kind="shape:" + sh["kind"], id=sh["id"], pts=[list(p) for p in sh["pts_mm"]], fill=sh.get("fill")))
        elif sh.get("centre_mm"):
            P.append(dict(kind="shape:" + sh["kind"], id=sh["id"], centre=list(sh["centre_mm"]), r_inner_mm=sh.get("r_inner_mm"), r_outer_mm=sh.get("r_outer_mm"), length_mm=sh.get("length_mm"), width_mm=sh.get("width_mm"), fill=sh.get("fill")))
        elif sh.get("segments_mm"):
            P.append(dict(kind="shape:ticks", id=sh["id"], segments=sh["segments_mm"], width_mm=sh.get("width_mm")))
    for a in item["art"]:
        x0, y0, x1, y1 = a["box_mm"]
        P.append(dict(kind="art", id=a["id"], pts=[[x0, y0], [x1, y0], [x1, y1], [x0, y1]], describe=a["describe"]))
    for b in item["blocks"]:
        x0, y0, x1, y1 = b["ink_box_mm"]
        P.append(dict(kind="ink_box", id=b["id"], text=b["text"], pts=[[x0, y0], [x1, y0], [x1, y1], [x0, y1]]))
        P.append(dict(kind="baseline", id=b["id"], pts=[[x0, b["baseline_mm"]], [x1, b["baseline_mm"]]]))
    fx = item.get("fixing") or {}
    for i, (hx, hy) in enumerate(fx.get("holes_mm", [])):
        P.append(dict(kind="hole", id="hole%d" % i, pts=[[hx, hy]], diameter_mm=10))
    return P


def draw_item(item, out, with_text=True):
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    img = Image.new("RGB", (W, H), ground_rgb(item))
    d = ImageDraw.Draw(img)
    for a in item["art"]:
        x0, y0, x1, y1 = a["box_mm"]
        if a.get("nominal_rgb"):
            d.rectangle([x0, H - y1, x1, H - y0], fill=tuple(a["nominal_rgb"]))
    for sh in item["shapes"]:
        c = fill_rgb(sh)
        k = sh["kind"]
        if k == "scrim":
            x0, y0, x1, y1 = sh["box_mm"]
            ov = Image.new("RGB", (int(x1 - x0), int(y1 - y0)), tuple(sh["rgb"]))
            mask = Image.new("L", ov.size, 0)
            md = ImageDraw.Draw(mask)
            for yy in range(ov.size[1]):
                t = yy / max(1.0, ov.size[1] - 1)          # 0 at the top of the image box
                a = sh["alpha_top"] * (1 - t) + sh["alpha_bottom"] * t if sh["alpha_top"] is not None else 0.5
                md.line([(0, yy), (ov.size[0], yy)], fill=int(255 * a))
            img.paste(ov, (int(x0), int(H - y1)), mask)
            continue
        if k in ("rect", "rule") and sh.get("box_mm"):
            x0, y0, x1, y1 = sh["box_mm"]
            if c is not None:
                d.rectangle([x0, H - y1, x1, H - y0], fill=c)
        elif k == "frame" and sh.get("box_mm"):
            x0, y0, x1, y1 = sh["box_mm"]
            wdt = int(sh.get("width_mm", 3))
            if c is not None:
                for i in range(wdt):
                    d.rectangle([x0 + i, H - y1 + i, x1 - i, H - y0 - i], outline=c)
        elif k == "roundel" and sh.get("box_mm"):
            x0, y0, x1, y1 = sh["box_mm"]
            if c is not None and sh.get("fill_kind") in ("ink", "paint") and sh.get("fill") not in ("white",):
                d.ellipse([x0, H - y1, x1, H - y0], fill=c)
            elif c is not None:
                d.ellipse([x0, H - y1, x1, H - y0], outline=c, width=max(2, int((x1 - x0) * 0.08)))
            else:
                d.ellipse([x0, H - y1, x1, H - y0], outline=(40, 40, 40), width=2)
        elif k == "star" and sh.get("pts_mm"):
            d.polygon([(x, H - y) for x, y in sh["pts_mm"]], fill=None, outline=(120, 120, 120))
        elif k == "ring" and sh.get("centre_mm"):
            cx, cy = sh["centre_mm"]
            ro, ri = sh["r_outer_mm"], sh["r_inner_mm"]
            col = c if c is not None else ground_rgb(item)
            d.ellipse([cx - ro, H - cy - ro, cx + ro, H - cy + ro], outline=col, width=max(1, int(round(ro - ri))))
        elif k == "poly" and sh.get("pts_mm"):
            d.polygon([(x, H - y) for x, y in sh["pts_mm"]], fill=c if c is not None else (60, 60, 60))
        elif k == "ticks" and sh.get("segments_mm"):
            for sg in sh["segments_mm"]:
                d.line([(sg["p0"][0], H - sg["p0"][1]), (sg["p1"][0], H - sg["p1"][1])], fill=(20, 20, 20), width=max(1, int(sh.get("width_mm", 2))))
        elif k == "hand" and sh.get("centre_mm"):
            cx, cy = sh["centre_mm"]
            d.line([(cx, H - cy), (cx, H - cy - sh["length_mm"])], fill=c or (224, 204, 160), width=max(2, int(sh["width_mm"])))
    for a in item["art"]:
        x0, y0, x1, y1 = a["box_mm"]
        d.rectangle([x0, H - y1, x1, H - y0], outline=(150, 110, 200), width=2)
        d.text((x0 + 8, H - y1 + 8), "ART SLOT " + a["id"], fill=(150, 110, 200))
    sx0, sy0, sx1, sy1 = item["safe_mm"]
    d.rectangle([sx0, H - sy1, sx1, H - sy0], outline=(150, 150, 150))
    for b in item["blocks"]:
        drawn = with_text and not NO_TEXT and draw_text(d, item, b, H)
        x0, y0, x1, y1 = b["ink_box_mm"]
        d.rectangle([x0, H - y1, x1, H - y0], outline=(220, 0, 220))
        d.line([(x0 - 6, H - b["baseline_mm"]), (x1 + 6, H - b["baseline_mm"])], fill=(0, 170, 220))
    fx = item.get("fixing") or {}
    for hx, hy in fx.get("holes_mm", []):
        d.ellipse([hx - 5, H - hy - 5, hx + 5, H - hy + 5], outline=(0, 0, 0), fill=(90, 90, 90))
    img.save(out)
    return img


def contact_sheet(imgs, labels, out, cols, cell):
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell[0], rows * cell[1]), (235, 235, 235))
    d = ImageDraw.Draw(sheet)
    for n, (im, lab) in enumerate(zip(imgs, labels)):
        r, c = divmod(n, cols)
        t = im.copy()
        t.thumbnail((cell[0] - 16, cell[1] - 30))
        sheet.paste(t, (c * cell[0] + 8, r * cell[1] + 22))
        d.text((c * cell[0] + 8, r * cell[1] + 6), lab, fill=(0, 0, 0))
    sheet.save(out)


def _label(d, x, y, text):
    d.text((x + 3, y + 3), text, fill=(0, 0, 0))


def elevation(surface_id, placements, items, out, scale_mm_per_px=4):
    """SF1 (the quay gable, u 0 to 4.5 m, z 0 to 3.2 m) and SF2 (the empty unit's glass): the DEFAULT placements to scale, held twins left out; the gable shows its downpipe, the paste zone and the plates."""
    S = T["surfaces"][surface_id]
    if surface_id == "SF1":
        ur, zr = [0.0, 4.5], [0.0, 3.2]
    else:
        ur, zr = S["u_range"], S["z_range"]
    W = int((ur[1] - ur[0]) * 1000 / scale_mm_per_px)
    H = int((zr[1] - zr[0]) * 1000 / scale_mm_per_px)
    img = Image.new("RGB", (W, H), (150, 110, 96) if surface_id == "SF1" else (205, 205, 200))
    d = ImageDraw.Draw(img)
    by = {i["id"]: i for i in items}
    pal = T["palette"]
    k = 1000.0 / scale_mm_per_px
    if surface_id == "SF1":
        for f in S["fixtures"]:
            if f["id"] == "downpipe":
                x0 = (f["u_m"] - f["diameter_mm"] / 2000.0) * k
                d.rectangle([x0, 0, x0 + f["diameter_mm"] / scale_mm_per_px, H], fill=(24, 24, 26))
                cl = f["keep_paper_clear_mm"] / scale_mm_per_px
                d.rectangle([x0 - cl, 0, x0 + f["diameter_mm"] / scale_mm_per_px + cl, H], outline=(255, 255, 255))
            if f["id"] == "damp_foot":
                d.rectangle([0, H - 0.45 * k, W, H], fill=(80, 64, 56))
    pls = [p for p in placements if not p.get("held_until_minted") and (p["surface"] == surface_id or (surface_id == "SF1" and p.get("host") == "SF1"))]
    for p in sorted(pls, key=lambda p: p["layer"]):
        if p.get("u_m") is None:
            continue
        x0 = (p["u_m"] - ur[0]) * k
        x1 = x0 + p["w_m"] * k
        y1 = H - (p["z_bottom_m"] - zr[0]) * k
        y0 = y1 - p["h_m"] * k
        it = by.get(p["item"])
        col = (225, 225, 215)
        if it and it.get("stock") and it["kind"] in ("sheet", "card", "sticker"):
            col = rgb(pal["stocks"][it["stock"]]["aged"][p["age_class"]])
        elif it and it["kind"] == "plate":
            col = rgb(pal["paints"]["plate_white"]["aged"][p["age_class"]])
        d.rectangle([x0, y0, x1, y1], fill=col, outline=(30, 30, 30))
        _label(d, x0, y0, "%s %s" % (p["item"], p["age_class"]))
    if surface_id == "SF1":
        z = S["paste_zone"]["z"]
        d.rectangle([S["paste_zone"]["u"][0] * k, H - z[1] * k, min(W - 1, S["paste_zone"]["u"][1] * k), H - z[0] * k], outline=(255, 255, 0))
    img.save(out)
    return img


def elevation_piers(placements, items, out, scale_mm_per_px=8):
    """The plain west row (street x 3 to 21): brick, the openings between the piers, and what is placed on the piers, in the window at x 12.3 and on the corner pier. z 0 to 3.2 m."""
    x0m, x1m, zmax = 3.0, 21.2, 3.2
    k = 1000.0 / scale_mm_per_px
    W, H = int((x1m - x0m) * k), int(zmax * k)
    img = Image.new("RGB", (W, H), (150, 110, 96))
    d = ImageDraw.Draw(img)
    by = {i["id"]: i for i in items}
    pal = T["palette"]
    piers = T["west_piers"]
    # openings: the gaps between the piers inside each bay
    for bay in range(3):
        s0 = 3.0 + 6.0 * bay
        ps = sorted([p for p in piers if p["bay"] == bay], key=lambda p: p["x0"])
        edges = [s0] + [v for p in ps for v in (p["x0"], p["x1"])] + [s0 + 6.0]
        for a, b in zip(edges[0::2], edges[1::2]):
            if b > a:
                d.rectangle([(a - x0m) * k, H - 2.4 * k, (b - x0m) * k, H], fill=(60, 62, 70))
    for p in piers:
        d.rectangle([(p["x0"] - x0m) * k, 0, (p["x1"] - x0m) * k, H], outline=(255, 255, 0))
        d.text(((p["x0"] - x0m) * k + 3, H - 14), p["id"], fill=(255, 255, 255))
    for p in placements:
        if p.get("held_until_minted") or p["surface"] not in ("WEST_PIER", "SF9", "SF7") or p.get("street_x_m") is None:
            continue
        w = p["w_m"] * k
        xc = (p["street_x_m"] - x0m) * k
        y1 = H - p["z_bottom_m"] * k
        y0 = y1 - p["h_m"] * k
        it = by.get(p["item"])
        col = (225, 225, 215)
        if it and it.get("stock") and it["kind"] in ("sheet", "card", "sticker"):
            col = rgb(pal["stocks"][it["stock"]]["aged"][p["age_class"]])
        elif it and it["kind"] == "plate":
            col = rgb(pal["paints"]["plate_white"]["aged"][p["age_class"]])
        d.rectangle([xc - w / 2, y0, xc + w / 2, y1], fill=col, outline=(30, 30, 30))
        _label(d, xc - w / 2, y0, "%s %s" % (p["item"], p["age_class"]))
    img.save(out)
    return img


def elevation_plates(placements, items, out, scale_mm_per_px=2):
    """Where the name plates stand: the west corner pier (street x 19.92 to 21.0, brick to 3.12 m) and the quay gable's first 2.6 m; the yard entrance (x 21 to 24) carries none. z 2.0 to 3.4 m."""
    k = 1000.0 / scale_mm_per_px
    by = {i["id"]: i for i in items}
    pal = T["palette"]
    panels = []
    for title, x0m, x1m, key in (("west corner pier, street x 19.92 to 21.0", 19.6, 21.3, "street"), ("quay gable, u 0 to 2.6 m", 0.0, 2.6, "u")):
        W, H = int((x1m - x0m) * k), int(1.5 * k)
        img = Image.new("RGB", (W, H), (150, 110, 96))
        d = ImageDraw.Draw(img)
        d.text((4, 4), title, fill=(255, 255, 255))
        if key == "street":
            d.rectangle([(19.92 - x0m) * k, int(0.4 * k), (21.0 - x0m) * k, H], outline=(255, 255, 0))
            d.line([(21.0 - x0m) * k, 0, (21.0 - x0m) * k, H], fill=(255, 255, 255))
        for p in placements:
            if p.get("held_until_minted") or p["surface"] != "SF7":
                continue
            if key == "street" and p.get("street_x_m") is not None:
                xc = (p["street_x_m"] - x0m) * k
            elif key == "u" and p.get("host") == "SF1":
                xc = (p["u_m"] + p["w_m"] / 2 - x0m) * k
            else:
                continue
            w = p["w_m"] * k
            y1 = H - (p["z_bottom_m"] - 1.9) * k
            y0 = y1 - p["h_m"] * k
            it = by[p["item"]]
            d.rectangle([xc - w / 2, y0, xc + w / 2, y1], fill=rgb(pal["paints"]["plate_white"]["aged"][p["age_class"]]), outline=(30, 30, 30))
            _label(d, xc - w / 2, y0, "%s centre z %.2f" % (p["item"], p["z_bottom_m"] + p["h_m"] / 2))
        panels.append(img)
    Wt = max(p.size[0] for p in panels)
    sheet = Image.new("RGB", (Wt, sum(p.size[1] for p in panels) + 8), (255, 255, 255))
    y = 0
    for p in panels:
        sheet.paste(p, (0, y))
        y += p.size[1] + 8
    sheet.save(out)
    return sheet


def polys_case(case):
    ow, oh = case["outer_mm"]
    f = case["frame_mm"]
    iw, ih = ow - f["left"] - f["right"], oh - f["top"] - f["bottom"]
    return dict(id=case["id"], outer=[[0, 0], [ow, 0], [ow, oh], [0, oh]], window=[[f["left"], f["bottom"]], [f["left"] + iw, f["bottom"]], [f["left"] + iw, f["bottom"] + ih], [f["left"], f["bottom"] + ih]],
                radius_mm=case["window_radius_mm"], children=case["children"])


def draw_case(case, items, out):
    ow, oh = case["outer_mm"]
    f = case["frame_mm"]
    img = Image.new("RGB", (ow, oh), (74, 50, 34) if case["id"] == "HC1" else (24, 68, 140))
    d = ImageDraw.Draw(img)
    x0, y0 = f["left"], f["top"]
    x1, y1 = ow - f["right"], oh - f["bottom"]
    d.rounded_rectangle([x0, y0, x1, y1], radius=case["window_radius_mm"], fill=(176, 138, 96) if case["id"] == "HC1" else (236, 236, 232))
    by = {i["id"]: i for i in items}
    for ch in case["children"]:
        it = by[ch["item"]]
        w, h = it["format"]["w_mm"], it["format"]["h_mm"]
        px0, py0 = x0 + ch["x_mm"], y1 - ch["y_mm"] - h
        col = rgb(T["palette"]["stocks"][it["stock"]]["aged"]["C"])
        d.rectangle([px0, py0, px0 + w, py0 + h], fill=col, outline=(40, 40, 40))
        d.text((px0 + 4, py0 + 4), ch["item"], fill=(0, 0, 0))
    img.save(out)


def photo_ref_polys():
    r = T["photo"]["ratios"]
    return r


def overlay_on_photo(photo_path, out_path):
    """Lay the photograph-proportion drawing of the glazed case on the saved preview: scale fitted on ONE dimension (the outer height of case 2),
    the other edges tested. Returns the mean absolute error in view pixels over the four horizontal edges that depend only on height fractions."""
    P = T["photo"]["P1"]
    px = P["px"]["c2"]
    img = Image.open(photo_path).convert("RGB")
    ox0, oy0, ox1, oy1 = px["outer"]
    Hh = oy1 - oy0
    r = T["photo"]["ratios"]
    d = ImageDraw.Draw(img)
    # offsets are in the crop's own pixels: the preview stores its crop origin in the JSON
    cx, cy = P.get("crop_origin", [0, 0])
    sc = P.get("crop_scale", 1.0)
    X0, Y0, X1, Y1 = [(ox0 - cx) * sc, (oy0 - cy) * sc, (ox1 - cx) * sc, (oy1 - cy) * sc]
    H = Y1 - Y0
    edges = [Y0, Y0 + r["top_band_over_h"] * H, Y0 + (r["top_band_over_h"] + r["window_over_h"]) * H, Y1]
    for y in edges:
        d.line([(X0 - 20, y), (X1 + 20, y)], fill=(255, 40, 40), width=2)
    W = X1 - X0
    sb = r["side_bands_sum_over_w"] * W / 2.0
    for x in (X0, X0 + sb, X1 - sb, X1):
        d.line([(x, Y0 - 10), (x, Y1 + 10)], fill=(40, 200, 255), width=1)
    img.save(out_path, quality=88)
    return edges


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else None
    if out is None:
        print(__doc__)
        sys.exit(2)
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
    (out / "items").mkdir(parents=True, exist_ok=True)
    items = T["items"]
    J = dict(units="mm per item (x from the viewer's left, y up); metres for surfaces", items={}, surfaces={}, cases={})
    imgs = {}
    for it in items:
        if only and it["id"] not in only:
            continue
        J["items"][it["id"]] = dict(title=it["title"], format=it["format"], px_per_mm=it["px_per_mm"], polys=polys_for(it))
        imgs[it["id"]] = draw_item(it, out / "items" / (it["id"] + ".png"))
    groups = {"bills": [i for i in items if i["part"] in ("poll_tax_bills", "chapel_hall", "fights", "market", "goods", "tivoli") and i["format"]["w_mm"] >= 300],
              "notices": [i for i in items if i["part"] in ("council_police", "harbour_and_ferry", "chapel_hall")],
              "cards": [i for i in items if i["part"] in ("window_cards", "newsagent_board") or i["format"]["w_mm"] < 300 and i["part"] == "poll_tax_bills"],
              "boards_plates": [i for i in items if i["part"] in ("letting_boards", "street_name_plates")]}
    if not only:
        for g, lst in groups.items():
            contact_sheet([imgs[i["id"]] for i in lst], [i["id"] for i in lst], out / ("sheet_%s.png" % g), cols=6 if g != "boards_plates" else 3, cell=(220, 300) if g != "boards_plates" else (440, 200))
    for sid in ("SF1", "SF2"):
        elevation(sid, T["placements"], items, out / ("elevation_%s.png" % sid))
    elevation_piers(T["placements"], items, out / "elevation_piers.png")
    elevation_plates(T["placements"], items, out / "elevation_plates.png")
    for c in T["cases"]:
        J["cases"][c["id"]] = polys_case(c)
        draw_case(c, items, out / ("case_%s.png" % c["id"]))
    J["surfaces"] = {k: v for k, v in T["surfaces"].items()}
    J["west_piers"] = T["west_piers"]
    J["placements"] = T["placements"]
    (out / "drawing.json").write_text(json.dumps(J, separators=(",", ":")), encoding="utf-8")
    print("drew %d items, %d cases into %s" % (len(J["items"]), len(J["cases"]), out))


if __name__ == "__main__":
    main()
