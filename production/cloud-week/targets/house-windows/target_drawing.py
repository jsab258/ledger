#!/usr/bin/env python3
"""Draws the house-windows target from target.json alone: filled polygons in millimetres (an elevation and the sections that matter for each kind; each room's
back wall, side wall and picture layout; the row of twenty windows) into a JSON file, and as pictures into a folder; and, with --photo, the 2/2 elevation laid on
photograph P8 (a scale fitted on the width only) into a preview.
usage: target_drawing.py OUT_DIR [--json FILE] [--photo FILE --overlay FILE]      Run with /home/user/.bpyenv/bin/python."""
import argparse
import json
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
from PIL import Image, ImageDraw

COL = {"paint": (236, 235, 230), "glass": (92, 108, 138), "net": (214, 210, 196), "brick": (150, 84, 62), "line": (30, 30, 30), "grey": (190, 190, 190), "room_back": (206, 196, 170)}


def rect_poly(x0, x1, z0, z1):
    return [[x0, z0], [x1, z0], [x1, z1], [x0, z1]]


def elevation(t, kind):
    """front elevation polygons (x, z in mm) of a kind from target.json."""
    k = t["kinds"][kind]
    polys = []
    if kind in ("S22", "S11"):
        for n in k["lab_nodes"]:
            mat = "glass" if n["name"].startswith("glass__") else "paint"
            polys.append({"name": n["name"], "material": mat, "poly": rect_poly(n["x"][0], n["x"][1], n["z_up"][0], n["z_up"][1]), "y_front": n["y_into_wall"][0]})
        # panes as the kit's pieces split them (the lab's sheets are one wide sheet a sash)
        polys = [p for p in polys if not p["name"].startswith("glass__")]
        for p in t["kit_pieces"]["per_kind"][kind]["added_nodes"]:
            if p["name"].startswith("glass__"):
                polys.append({"name": p["name"], "material": "glass", "poly": rect_poly(p["x"][0], p["x"][1], p["z_up"][0], p["z_up"][1]), "y_front": p["y_into_wall"][0]})
    else:
        for p in k["parts_mm"]:
            mat = "glass" if p.get("material") == "glass_house" else "paint"
            polys.append({"name": p["name"], "material": mat, "poly": rect_poly(p["x"][0], p["x"][1], p["z_up"][0], p["z_up"][1]), "y_front": p["y_into_wall"][0]})
    return polys


def hsection(t, kind, z):
    """horizontal section at height z (mm): the rectangles (x, y_into_wall) of every node the height crosses."""
    out = []
    k = t["kinds"][kind]
    if kind in ("S22", "S11"):
        src = [(n["name"], n["x"], n["y_into_wall"], n["z_up"], "glass" if n["name"].startswith("glass__") else "paint") for n in k["lab_nodes"]]
    else:
        src = [(p["name"], p["x"], p["y_into_wall"], p["z_up"], "glass" if p.get("material") == "glass_house" else "paint") for p in k["parts_mm"]]
    for name, x, y, zz, mat in src:
        if zz[0] <= z <= zz[1]:
            out.append({"name": name, "material": mat, "poly": rect_poly(x[0], x[1], y[0], y[1])})
    return out


def vsection(t, kind, x):
    out = []
    k = t["kinds"][kind]
    if kind in ("S22", "S11"):
        src = [(n["name"], n["x"], n["y_into_wall"], n["z_up"], "glass" if n["name"].startswith("glass__") else "paint") for n in k["lab_nodes"]]
    else:
        src = [(p["name"], p["x"], p["y_into_wall"], p["z_up"], "glass" if p.get("material") == "glass_house" else "paint") for p in k["parts_mm"]]
    for name, xx, y, zz, mat in src:
        if xx[0] <= x <= xx[1]:
            out.append({"name": name, "material": mat, "poly": rect_poly(y[0], y[1], zz[0], zz[1])})
    return out


def draw_elev(t, kind, path, scale=0.5):
    w, h = 1100, 1676.4
    W, Hh = int((w + 400) * scale), int((h + 300) * scale)
    im = Image.new("RGB", (W, Hh), (60, 52, 48))
    dr = ImageDraw.Draw(im)

    def P(x, z):
        return ((x + w / 2 + 200) * scale, Hh - (z + 150) * scale)
    # the brick opening
    dr.rectangle([P(-425, 1676.4)[0], P(-425, 1676.4)[1], P(425, 0)[0], P(425, 0)[1]], fill=(20, 20, 24))
    polys = elevation(t, kind)
    for p in sorted(polys, key=lambda p: -p["y_front"]):
        pts = [P(x, z) for x, z in p["poly"]]
        dr.polygon(pts, fill=COL[p["material"]], outline=COL["line"])
    # nets
    for nk in ("N1", "N2", "N3"):
        c = t["nets"][nk]["card"]
        pts = [P(x, z) for x, z in rect_poly(c["x"][0], c["x"][1], c["z"][0], c["z"][1])]
        dr.line(pts + [pts[0]], fill=(255, 170, 0) if nk == "N1" else (0, 200, 255) if nk == "N2" else (0, 255, 120), width=1)
    dr.text((8, 6), "%s elevation, mm: opening 850 x 1676.4; nets N1 orange, N2 cyan, N3 green (outlines)" % kind, fill=(255, 255, 255))
    im.save(path)


def draw_sections(t, kind, path):
    im = Image.new("RGB", (1500, 760), (40, 40, 44))
    dr = ImageDraw.Draw(im)
    dr.text((8, 4), "%s: horizontal sections at z=300 and z=1000 (x across, y into the wall: down); vertical section at x=-150 through a pane (y across, z up)" % kind, fill=(255, 255, 255))
    for i, z in enumerate((300, 1000)):
        ox, oy = 20 + i * 440, 60
        for p in hsection(t, kind, z):
            pts = [(ox + (x + 520) * 0.40, oy + y * 0.40 + 20) for x, y in p["poly"]]
            dr.polygon(pts, fill=COL[p["material"]], outline=COL["line"])
        dr.text((ox, oy - 14), "z=%d" % z, fill=(255, 255, 0))
    ox, oy = 900, 60
    for p in vsection(t, kind, -150.0):
        pts = [(ox + y * 1.6 + 60, oy + (1700 - z) * 0.40) for y, z in p["poly"]]
        dr.polygon(pts, fill=COL[p["material"]], outline=COL["line"])
    for nk, nm in (("N1", "N1"), ("N2", "N2")):
        c = t["nets"][nk]
        y = c["plane_mm"][kind]
        dr.line([(ox + y * 1.6 + 60, oy + (1700 - c["card"]["z"][0]) * 0.40), (ox + y * 1.6 + 60, oy + (1700 - c["card"]["z"][1]) * 0.40)], fill=(255, 170, 0) if nk == "N1" else (0, 200, 255), width=2)
    y = t["street"]["card_plane_behind_frontage_m"] * 1000
    dr.line([(ox + y * 1.6 + 60, oy), (ox + y * 1.6 + 60, oy + 700 * 0.40 * 1.7)], fill=(0, 255, 0), width=1)
    dr.text((ox, oy - 14), "vertical x=-150; nets orange/cyan; room card green (y=270)", fill=(255, 255, 0))
    im.save(path)


def project(x, y, z, w, h, d):
    """the render's rule (tools/ue/make_interior_material.py project): room point to picture (u, v up)."""
    return 0.5 + (x / w) * d / (d + y), 0.5 + ((z - h / 2.0) / h) * d / (d + y)


def room_layout(t, rid, path):
    r = t["rooms"]["rooms"][rid]
    fam = t["rooms"]["families"][r["family"]]
    w, h, d, camd = fam["w"], fam["h"], fam["d"], fam["camd"]
    px_w, px_h = r["picture_px"]
    s = 0.34
    W, Hh = int(px_w * s) * 2 + 30, int(px_h * s) + 24
    im = Image.new("RGB", (W, Hh), (50, 50, 54))
    dr = ImageDraw.Draw(im)
    # left: the picture layout
    ox, oy = 8, 20
    dr.rectangle([ox, oy, ox + px_w * s, oy + px_h * s], fill=(70, 66, 60))

    def PP(x, y, z):
        u, v = project(x, y, z, w, h, camd)
        return (ox + u * px_w * s, oy + (1 - v) * px_h * s)
    # the back wall, the side walls, the floor and ceiling lines
    corners_back = [PP(-w / 2, d, 0), PP(w / 2, d, 0), PP(w / 2, d, h), PP(-w / 2, d, h)]
    dr.polygon(corners_back, fill=COL["room_back"], outline=(0, 0, 0))
    for a, b in ((PP(-w / 2, 0, 0), PP(-w / 2, d, 0)), (PP(w / 2, 0, 0), PP(w / 2, d, 0)), (PP(-w / 2, 0, h), PP(-w / 2, d, h)), (PP(w / 2, 0, h), PP(w / 2, d, h))):
        dr.line([a, b], fill=(0, 0, 0))
    for o in r["objects"]:
        pl = o["place"]
        if o["surface"] == "back":
            x0, x1 = pl["x_across"]
            z0, z1 = pl["z"]
            y_front = pl["y_back"][0]
            front = [PP(x0, y_front, z0), PP(x1, y_front, z0), PP(x1, y_front, z1), PP(x0, y_front, z1)]
            dr.polygon(front, fill=(170, 120, 60) if o["class"] == "true" else (200, 90, 60), outline=(0, 0, 0))
        else:
            xw = -w / 2 if o["surface"] == "left" else w / 2
            y0, y1 = pl["y_back"]
            z0, z1 = pl["z"]
            sign = 1 if o["surface"] == "left" else -1
            xf = xw + sign * pl["x_from_wall"][1]
            front = [PP(xf, y0, z0), PP(xf, y1, z0), PP(xf, y1, z1), PP(xf, y0, z1)]
            dr.polygon(front, fill=(150, 150, 190), outline=(0, 0, 0))
    # the window's hole as seen square on from the render camera: nothing (the picture has no front wall)
    dr.text((ox + 4, oy + 2), "%s: picture %d x %d (back wall %s)" % (rid, px_w, px_h, [round(v) for v in t["rooms"]["pictures_by_family"][r["family"]]["back_wall_rect_px_x0y0x1y1"]]), fill=(255, 255, 255))
    # right: back wall elevation in metres
    ox2 = px_w * s + 22
    sc = (px_w * s - 10) / w
    dr.rectangle([ox2, oy, ox2 + w * sc, oy + h * sc], fill=COL["room_back"], outline=(0, 0, 0))
    for o in r["objects"]:
        pl = o["place"]
        if o["surface"] == "back":
            x0, x1 = pl["x_across"]
            z0, z1 = pl["z"]
            dr.rectangle([ox2 + (x0 + w / 2) * sc, oy + (h - z1) * sc, ox2 + (x1 + w / 2) * sc, oy + (h - z0) * sc], fill=(170, 120, 60) if o["class"] == "true" else (200, 90, 60), outline=(0, 0, 0))
            dr.text((ox2 + (x0 + w / 2) * sc + 2, oy + (h - z1) * sc + 2), o["model"][:14], fill=(0, 0, 0))
    dr.text((ox2 + 4, oy + 2), "back wall elevation (m): brown true, red tolerated", fill=(0, 0, 0))
    im.save(path)


def draw_row(t, path):
    sites = t["sites"]
    xs = [s["x_centre"] for s in sites]
    x0, x1 = min(xs) - 1.5, max(xs) + 1.5
    sc = 24.0
    W = int((x1 - x0) * sc) + 20
    im = Image.new("RGB", (W, 520), (50, 48, 46))
    dr = ImageDraw.Draw(im)
    dr.text((8, 4), "the twenty windows by x (east row above the line, west below); kind, net, room; lit at 20:30 outlined", fill=(255, 255, 255))
    lit = set(t["rooms"]["lit_share"]["lit_by_hour"]["20:30"]["windows"])
    for s in sites:
        cx = (s["x_centre"] - x0) * sc + 10
        up = s["side"] > 0
        y0 = 40 if up else 290
        kcol = {"S22": (236, 235, 230), "S11": (225, 222, 205), "RC": (200, 205, 215)}[s["kind"]]
        dr.rectangle([cx - 0.425 * sc, y0, cx + 0.425 * sc, y0 + 1.676 * sc * 2], fill=(30, 34, 44), outline=kcol if s["paint"] != "bronze" else (110, 90, 70), width=3)
        nk = s["net"]["kind"]
        if nk != "N0":
            c = t["nets"][nk]["card"]
            dr.rectangle([cx - 0.425 * sc, y0 + (1676 - c["z"][1]) / 1000 * sc * 2, cx + 0.425 * sc, y0 + (1676 - c["z"][0]) / 1000 * sc * 2], fill=(210, 206, 190))
        if s["id"] in lit:
            dr.rectangle([cx - 0.425 * sc - 3, y0 - 3, cx + 0.425 * sc + 3, y0 + 1.676 * sc * 2 + 3], outline=(255, 190, 70), width=2)
        dr.text((cx - 12, y0 + 1.676 * sc * 2 + 4), "%s %s" % (s["kind"], nk), fill=(255, 255, 255))
        dr.text((cx - 14, y0 + 1.676 * sc * 2 + 16), s["room"].replace("up_", "").replace("gf_", "")[:12], fill=(200, 200, 160))
    im.save(path)


def overlay(t, photo, out):
    """the 2/2 elevation laid on photograph P8's left window at the scale fitted on the WIDTH only (850 mm = the photograph's outline width)."""
    ov = t["overlay"]
    x0, y0, x1, y1 = ov["outline_px"]
    s = (x1 - x0) / 850.0
    im = Image.open(photo).convert("RGB")
    sc = ov["preview_scale"]
    big = im.crop(ov["crop"]).resize((int((ov["crop"][2] - ov["crop"][0]) * sc), int((ov["crop"][3] - ov["crop"][1]) * sc)), Image.LANCZOS)
    dr = ImageDraw.Draw(big)

    def Pp(xmm, zmm):
        # x from the window's middle, z up from the opening's bottom; the bottom edge is the photograph's sill line; the width scale s everywhere
        px = (x0 + x1) / 2.0 + xmm * s
        py = y1 - zmm * s
        return ((px - ov["crop"][0]) * sc, (py - ov["crop"][1]) * sc)
    polys = elevation(t, "S22")
    for p in polys:
        # only what shows in the opening: the linings and the pulley stiles lie behind the brick beyond +-425 mm
        p = dict(p, poly=[[max(-425.0, min(425.0, x)), z] for x, z in p["poly"]])
        if p["poly"][0][0] == p["poly"][1][0]:
            continue
        if p["material"] == "paint" and p["name"].split("__")[-1].startswith(("upper_stile", "lower_stile", "upper_top_rail", "lower_bottom_rail", "lower_top_rail", "upper_bottom_rail", "lower_bar", "upper_bar", "inner_lining", "outer_lining", "head_lining", "head_outer")):
            pts = [Pp(x, z) for x, z in p["poly"]]
            dr.line(pts + [pts[0]], fill=(255, 40, 40), width=1)
        elif p["material"] == "glass":
            pts = [Pp(x, z) for x, z in p["poly"]]
            dr.line(pts + [pts[0]], fill=(40, 255, 40), width=1)
    ow = [Pp(-425, 0), Pp(425, 0), Pp(425, 1676.4), Pp(-425, 1676.4)]
    dr.line(ow + [ow[0]], fill=(255, 255, 0), width=2)
    big.save(out, quality=88)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--json", default=os.path.join(HERE, "target_drawing.json"))
    ap.add_argument("--photo", default="")
    ap.add_argument("--overlay", default="")
    a = ap.parse_args()
    t = json.load(open(os.path.join(HERE, "target.json")))
    os.makedirs(a.out_dir, exist_ok=True)
    drawing = {"units": "millimetres; elevations (x across, z up) and sections (x or y, y or z) in the kit frame", "kinds": {}}
    for kind in ("S22", "S11", "RC"):
        drawing["kinds"][kind] = {"elevation": elevation(t, kind), "hsection_z300": hsection(t, kind, 300), "hsection_z1000": hsection(t, kind, 1000), "vsection_x_minus150": vsection(t, kind, -150.0)}
        draw_elev(t, kind, os.path.join(a.out_dir, "E-%s-elevation.png" % kind))
        draw_sections(t, kind, os.path.join(a.out_dir, "S-%s-sections.png" % kind))
    for rid in t["rooms"]["rooms"]:
        room_layout(t, rid, os.path.join(a.out_dir, "R-%s-layout.png" % rid))
    draw_row(t, os.path.join(a.out_dir, "D-twenty-windows.png"))
    json.dump(drawing, open(a.json, "w"))
    if a.photo and a.overlay:
        overlay(t, a.photo, a.overlay)
    print("drew", len(drawing["kinds"]), "kinds,", len(t["rooms"]["rooms"]), "rooms ->", a.out_dir)


if __name__ == "__main__":
    main()
