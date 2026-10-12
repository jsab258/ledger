#!/usr/bin/env python
"""Draw the shop-windows target from target.json ALONE.

    /home/user/.bpyenv/bin/python target_drawing.py OUT_DIR [--json drawing.json] [--shop ID ...] [--photo P1_CROP.jpg --overlay-out FILE]

Writes, per shop that needs a room: OUT_DIR/<id>-front.png (the bay's elevation in millimetres, the card and the display's footprint on it),
<id>-plan.png (plan: glass, display, card, room box, the render camera and the review cameras), <id>-room.png (the back wall and the two side walls
flat, each fixture drawn at its place with its stand-off class), <id>-picture.png (where the box's floor, back wall and corners land in the
4096-wide picture by the game's rule), and OUT_DIR/ten-fronts-sheet.png; the polygons as JSON (millimetres: u across the bay from the viewer's
left, z up from the footway; plan: u across, depth behind the wall face). With --photo and --overlay-out it also lays the target's T1 door, stallriser and glass lines on the main
photograph (the scale fitted on ONE dimension, the door leaf's height).
"""
import argparse
import json
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_common as S  # noqa: E402

T = None


def load():
    global T
    if T is None:
        T = json.load(open(os.path.join(HERE, "target.json")))
    return T


def rgb(t, shop, key, default=(180, 180, 180)):
    p = (shop["front"].get("paint_srgb") or {}).get(key)
    return tuple(p) if p else default


# ---- the bay elevation: polygons in mm, (u from the viewer's left, z up from the footway) -----------------------------------------
def rect(u0, z0, u1, z1):
    return [(u0, z0), (u1, z0), (u1, z1), (u0, z1)]


COVERING_LAYERS = ("part", "frame", "glass")      # what FRN-07 counts as standing in the opening: stallriser, sill, frame, glass, door, fanlight, transom, toplight, panel, head


def front_polys(shop):
    """The bay's elevation as polygons in millimetres (u from the viewer's left, z up from the footway), from target.json alone. Parts in the layers
    part / frame / glass are what stands between the pilasters (FRN-07 checks that nothing in u 350 to 5650, z 0 to 2850 is left open); furniture, overlay,
    bg, card and display are drawn but do not count."""
    f = shop["front"]
    z = f["zones_u_mm"]
    w0, w1 = z["window"]
    L = []

    def add(name, poly, colour, layer="part", dash=False):
        L.append({"name": name, "poly": [(round(a, 2), round(b, 2)) for a, b in poly], "colour": list(colour), "layer": layer, "dash": dash, "covers": layer in COVERING_LAYERS})
    pil = rgb(T, shop, "pilaster", (150, 150, 150))
    for side in ("L", "R"):
        m = (lambda u: u) if side == "L" else (lambda u: 6000 - u)
        add("plinth_" + side, [(m(20), 0), (m(330), 0), (m(330), 600), (m(20), 600)], pil, layer="pilaster")
        add("shaft_" + side, [(m(30), 600), (m(320), 600), (m(320), 2540), (m(30), 2540)], pil, layer="pilaster")
        add("capital_" + side, [(m(30), 2540), (m(320), 2540), (m(350), 2850), (m(0), 2850)], pil, layer="pilaster")
        if f.get("console_absent_viewer") != side:
            add("console_" + side, [(m(55), 2850), (m(295), 2850), (m(295), 3400), (m(55), 3400)], rgb(T, shop, "console", pil), layer="pilaster")
    add("fascia_board", rect(295, 2850, 5705, 3400), rgb(T, shop, "fascia_board", (200, 200, 200)), layer="pilaster")
    add("cornice", rect(54, 3400, 5946, 3550), rgb(T, shop, "cornice", pil), layer="pilaster")
    d = shop["door"]
    gl = f["glazing_layout"]
    wf = rgb(T, shop, "window_frame", (220, 220, 210))
    jf = gl["jamb_face"]
    mf = gl["mullion_face"]
    hood = d.get("shutter_hood")
    ztop = hood["z_mm"][0] if hood else Z_TOPLIGHT_TOP        # the roller-shutter hood cuts the toplights, bars and jambs away above 2550 (2.2)
    # ---- the window ---------------------------------------------------------------------------------------------------------------
    add("window_frame_bg", rect(w0, 525, w1, 2850), wf, layer="bg")
    add("stallriser", rect(w0, 0, w1, 600), rgb(T, shop, "stallriser", (120, 120, 120)))
    add("sill", rect(w0, 525, w1, 600), wf)
    add("window_jamb_L", rect(w0, 600, w0 + jf, ztop), wf, layer="frame")
    add("window_jamb_R", rect(w1 - jf, 600, w1, ztop), wf, layer="frame")
    add("window_seat_rail", rect(w0 + jf, 600, w1 - jf, 625), wf, layer="frame")
    for a, b in gl["lights"]:
        add("window_light", rect(w0 + a, 625, w0 + b, 2400), (150, 170, 180), layer="glass")
    for c in gl["mullion_centres"]:
        add("mullion", rect(w0 + c - mf / 2, 625, w0 + c + mf / 2, ztop), wf, layer="frame")
    add("window_transom", rect(w0 + jf, 2400, w1 - jf, 2480), wf, layer="frame")
    for a, b in gl["toplight_panes"]:
        add("window_toplight", rect(w0 + a, 2480, w0 + b, ztop), (150, 170, 180), layer="glass")
    for br in gl["toplight_bars"]:
        add("toplight_bar", rect(w0 + br["centre"] - br["face"] / 2, 2480, w0 + br["centre"] + br["face"] / 2, ztop), wf, layer="frame")
    if not hood:
        add("window_head", rect(w0, 2790, w1, 2850), wf, layer="frame")           # the head runs the full width of the frame, over the jambs
    else:
        add("roller_shutter_hood", rect(hood["u_mm"][0], hood["z_mm"][0], hood["u_mm"][1], hood["z_mm"][1]), (88, 90, 90), layer="part")
    # ---- the shop door and what stands over it ------------------------------------------------------------------------------------
    s0, s1 = z["shop_door"]
    cx = (s0 + s1) / 2
    leaf0, leaf1 = cx - 450, cx + 450
    dp = rgb(T, shop, "shop_door", wf)
    jb = 50.0
    add("shop_door_threshold", rect(s0, 0, s1, 25), (170, 168, 160))
    add("shop_door_jamb_L", rect(s0, 25, s0 + jb, ztop), dp, layer="frame")      # the door frame's jambs run up through the fanlight and the toplights to the head
    add("shop_door_jamb_R", rect(s1 - jb, 25, s1, ztop), dp, layer="frame")
    add("door_foot_clearance_seal", rect(s0 + jb, 25, s1 - jb, 28), (60, 60, 60), layer="frame")
    add("door_stop_L", rect(s0 + jb, 28, leaf0, 2068), dp, layer="frame")
    add("door_stop_R", rect(leaf1, 28, s1 - jb, 2068), dp, layer="frame")
    add("shop_door_leaf", rect(leaf0, 28, leaf1, 2068), dp, layer="part")
    gz = d["glass_foot_z_mm"]
    if d["variant"] == "T1":
        gtop = d["t1_rails_mm"]["glass"][1]
        bz = d["t1_rails_mm"]["glazing_bar"]["z"]
        add("door_glass_lower", rect(leaf0 + 115, gz, leaf1 - 115, bz - 14), (150, 170, 180), layer="overlay")
        add("door_glass_upper", rect(leaf0 + 115, bz + 14, leaf1 - 115, gtop), (150, 170, 180), layer="overlay")
    elif d["variant"] == "M1":
        add("door_glass", rect(leaf0 + 50, 198, leaf1 - 50, 1968), (150, 170, 180), layer="overlay")
    else:
        add("door_glass", rect(leaf0 + 40, 600, leaf1 - 40, 1968), (150, 170, 180), layer="overlay")
    lp = d["letter_plate"]
    add("letter_plate", rect(cx - 125, lp["z_mm"] - 20, cx + 125, lp["z_mm"] + 20), (160, 120, 55), layer="furniture")
    add("door_frame_head", rect(s0 + jb, 2068, s1 - jb, 2131), dp, layer="frame")
    fl = d["fanlight"]
    add("door_fanlight", rect(fl["u_mm"][0], fl["z_mm"][0], fl["u_mm"][1], fl["z_mm"][1]), (150, 170, 180), layer="glass")
    tr = d["transom"]
    add("door_transom", rect(tr["u_mm"][0], tr["z_mm"][0], tr["u_mm"][1], tr["z_mm"][1]), wf, layer="frame")
    ot = d["toplights_over_shop_door"]
    topz = ot.get("z_visible_mm", ot["z_mm"])[1]
    for a, b in ot["panes"]:
        add("door_toplight", rect(a, ot["z_mm"][0], b, topz), (150, 170, 180), layer="glass")
    for br in ot["bars"]:
        add("door_toplight_bar", rect(br["centre"] - br["face"] / 2, ot["z_mm"][0], br["centre"] + br["face"] / 2, topz), wf, layer="frame")
    hd = d["head"]
    add("door_head", rect(hd["u_mm"][0], hd["z_mm"][0], hd["u_mm"][1], hd["z_mm"][1]), wf, layer="frame")
    if hd.get("cut_away_behind_hood_mm"):
        pass                                                   # the hood stands where the head is cut away (drawn with the window)
    # ---- the side door (F1 from 3.1) and its panel -------------------------------------------------------------------------------
    if z.get("side_door"):
        a0, a1 = z["side_door"]
        ac = (a0 + a1) / 2
        sd = rgb(T, shop, "side_door", (200, 190, 170))
        add("side_door_threshold", rect(a0, 0, a1, 45), (170, 168, 160))
        add("side_door_filler_L", rect(a0, 45, a0 + 24.4, 2400), pil, layer="frame")
        add("side_door_filler_R", rect(a1 - 24.4, 45, a1, 2400), pil, layer="frame")
        add("side_door_F1", rect(a0 + 24.4, 45, a1 - 24.4, 2400), sd, layer="part")
        add("side_door_leaf", rect(ac - 419, 45, ac + 419, 2026), sd, layer="overlay")
        pn = d["panel_over_side_door"]
        add("panel_over_side_door", rect(pn["u_mm"][0], pn["z_mm"][0], pn["u_mm"][1], pn["z_mm"][1]), wf, layer="frame")
        add("panel_field", rect(pn["field_u_mm"][0], pn["z_mm"][0] + 12, pn["field_u_mm"][1], pn["z_mm"][1] - 12), tuple(min(255, c + 12) for c in wf), layer="overlay")
    # ---- the card and the display ---------------------------------------------------------------------------------------------------
    add("card_outline", rect(350, 550, 5650, 2950), (255, 255, 255), layer="card", dash=True)
    if shop.get("display"):
        dd = shop["display"]
        add("display_envelope", rect(w0 + dd["u_range"][0] * 1000, 600, w0 + dd["u_range"][1] * 1000, 600 + dd["height_max_w"] * 1000), (255, 200, 80), layer="display", dash=True)
    return L


Z_TOPLIGHT_TOP = 2790.0


def covering_rects(polys):
    """The rectangles (ua, za, ub, zb) of the polygons that count as standing in the opening."""
    out = []
    for p in polys:
        if p.get("covers"):
            us = [a for a, b in p["poly"]]
            zs = [b for a, b in p["poly"]]
            out.append((min(us), min(zs), max(us), max(zs)))
    return out


def draw_polys(polys, size, scale, origin, title=None, bg=(238, 238, 232), labels=None):
    im = Image.new("RGB", size, bg)
    dr = ImageDraw.Draw(im)
    H = size[1]
    for p in polys:
        pts = [(origin[0] + a * scale, H - origin[1] - b * scale) for a, b in p["poly"]]
        if p.get("dash"):
            for i in range(len(pts)):
                a, b = pts[i], pts[(i + 1) % len(pts)]
                n = max(2, int(math.dist(a, b) / 8))
                for k in range(0, n, 2):
                    t0, t1 = k / n, min(1.0, (k + 1) / n)
                    dr.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=tuple(p["colour"]) if p["layer"] != "card" else (90, 90, 90), width=2)
        else:
            dr.polygon(pts, fill=tuple(p["colour"]), outline=(40, 40, 40))
    for (u, zz, text, col) in (labels or []):
        dr.text((origin[0] + u * scale, H - origin[1] - zz * scale), text, fill=tuple(col))
    if title:
        dr.rectangle([0, 0, size[0], 16], fill=(30, 30, 30))
        dr.text((6, 3), title, fill=(240, 240, 240))
    return im


# ---- the plan --------------------------------------------------------------------------------------------------------------------
def plan_polys(shop):
    """Plan in mm: u across the bay (viewer's left to right), y = depth BEHIND the wall face (negative toward the street). The wall face is the glass's
    datum (2.2: d = 0), the glass at d +30, the card 590 behind it."""
    D = (shop.get("room") or {}).get("d") or 4.5
    W = 5300
    L = []

    def add(name, poly, colour, dash=False, layer="plan"):
        L.append({"name": name, "poly": [(round(a, 1), round(b, 1)) for a, b in poly], "colour": list(colour), "layer": layer, "dash": dash})
    add("street_wall_line", rect(0, -150, 6000, 0), (180, 160, 140))
    add("glass", rect(350, -36, 5650, -30), (120, 160, 190))
    card_depth = 590
    add("display_zone", rect(shop["front"]["zones_u_mm"]["window"][0], 15, shop["front"]["zones_u_mm"]["window"][1], 535), (255, 215, 120), dash=True)
    add("card", rect(350, card_depth - 20, 5650, card_depth + 20), (60, 60, 60))
    add("room_box", rect(350, card_depth, 5650, card_depth + D * 1000), (200, 210, 220), dash=True)
    cam = -(S.CAMERA_D * 1000 - card_depth)
    add("render_camera", [(3000 - 60, cam - 60), (3000 + 60, cam - 60), (3000, cam + 60)], (200, 40, 40))
    return L


def draw_plan(shop, size=(1500, 1000)):
    polys = plan_polys(shop)
    D = (shop.get("room") or {}).get("d") or 4.5
    ymin, ymax = -(S.CAMERA_D * 1000 - 590) - 300, 590 + D * 1000 + 200
    sc = min((size[0] - 100) / 6000.0, (size[1] - 60) / (ymax - ymin))
    im = Image.new("RGB", size, (238, 238, 232))
    dr = ImageDraw.Draw(im)
    for p in polys:
        pts = [(50 + a * sc, 30 + (b - ymin) * sc) for a, b in p["poly"]]
        if p.get("dash"):
            dr.line(pts + [pts[0]], fill=(90, 90, 90), width=2)
        else:
            dr.polygon(pts, fill=tuple(p["colour"]), outline=(40, 40, 40))
    dr.rectangle([0, 0, size[0], 16], fill=(30, 30, 30))
    dr.text((6, 3), "%s: plan (mm; street at the top, the room runs down); render camera red, the card black, the display amber" % shop["id"], fill=(240, 240, 240))
    return im, polys


# ---- the room's walls flat -------------------------------------------------------------------------------------------------------
CLASS_COLOUR = {"true": (110, 170, 110), "tolerated": (225, 190, 90), "refused": (210, 70, 70), "flat": (150, 170, 200)}


def stand_class(rules, surface, depth):
    if surface == "back":
        return "true" if depth <= rules["shelf_goods_on_back_wall_m"] else ("tolerated" if depth <= rules["furniture_at_back_wall_m"] else "refused")
    if surface in ("left", "right"):
        return "flat" if depth <= rules["side_wall_flat_m"] else ("tolerated" if depth <= rules["side_wall_relief_m"] else "refused")
    return "flat" if depth <= rules["floor_and_ceiling_m"] else ("tolerated" if depth <= rules["floor_ceiling_tolerated_m"] else "refused")


def draw_room(shop, size=(1500, 760)):
    rules = load()["method"]["standoff_rules_m"]
    room = shop["room"]
    D = room["d"]
    im = Image.new("RGB", size, (238, 238, 232))
    dr = ImageDraw.Draw(im)
    sc = 150.0                                   # px per metre for the back wall
    ox, oy = 20, size[1] - 40
    dr.rectangle([ox, oy - 2.4 * sc, ox + 5.3 * sc, oy], outline=(60, 60, 60))
    for fx in room["fixtures"]:
        if fx["surface"] != "back" or not fx.get("x"):
            continue
        cls = stand_class(rules, "back", fx["depth_m"])
        x0, x1 = fx["x"]
        z0, z1 = fx["z"]
        dr.rectangle([ox + (x0 + 2.65) * sc, oy - z1 * sc, ox + (x1 + 2.65) * sc, oy - z0 * sc], fill=CLASS_COLOUR[cls], outline=(40, 40, 40))
        for tz in fx.get("tiers") or []:
            dr.line([ox + (x0 + 2.65) * sc, oy - tz * sc, ox + (x1 + 2.65) * sc, oy - tz * sc], fill=(60, 60, 60), width=1)
        dr.text((ox + (x0 + 2.65) * sc + 3, oy - z1 * sc + 2), "%s %.2f" % (fx["id"], fx["depth_m"]), fill=(20, 20, 20))
    dr.text((ox, 4), "%s: back wall (x across, 5.3 m; z up, 2.4 m); green = true, amber = tolerated, red = refused (stand-off from the budget table)" % shop["id"], fill=(20, 20, 20))
    # the side walls: y (0..D) across, z up
    for k, side in enumerate(("left", "right")):
        bx = ox + 5.3 * sc + 30 + k * (D * 70 + 20)
        dr.rectangle([bx, oy - 2.4 * 70, bx + D * 70, oy], outline=(60, 60, 60))
        for fx in room["fixtures"]:
            if fx["surface"] != side:
                continue
            cls = stand_class(rules, side, fx["depth_m"])
            y0, y1 = fx["y"]
            z0, z1 = fx["z"]
            dr.rectangle([bx + y0 * 70, oy - z1 * 70, bx + y1 * 70, oy - z0 * 70], fill=CLASS_COLOUR[cls], outline=(40, 40, 40))
        dr.text((bx, oy + 6), side + " wall", fill=(20, 20, 20))
    return im


# ---- where the box lands in the picture -------------------------------------------------------------------------------------------
def picture_corners(D, pw=4096):
    ph = int(round(pw * S.H / S.W))
    pts = {}
    for name, (x, y, z) in {"back_left_bottom": (-S.W / 2, D, 0), "back_right_bottom": (S.W / 2, D, 0), "back_left_top": (-S.W / 2, D, S.H), "back_right_top": (S.W / 2, D, S.H)}.items():
        u, v = S.project(x, y, z, S.W, S.H, S.CAMERA_D)
        pts[name] = (round(u * pw, 1), round((1 - v) * ph, 1))
    return pts, (pw, ph)


def draw_picture(shop, size=(1500, 700)):
    D = shop["room"]["d"]
    pts, (pw, ph) = picture_corners(D)
    sc = size[0] / float(pw)
    im = Image.new("RGB", (size[0], int(ph * sc)), (238, 238, 232))
    dr = ImageDraw.Draw(im)
    dr.rectangle([0, 0, pw * sc - 1, ph * sc - 1], outline=(60, 60, 60))
    bl, br, tl, tr = pts["back_left_bottom"], pts["back_right_bottom"], pts["back_left_top"], pts["back_right_top"]
    dr.rectangle([tl[0] * sc, tl[1] * sc, br[0] * sc, br[1] * sc], outline=(200, 40, 40), width=2)
    for a, b in ((tl, (0, 0)), (tr, (pw, 0)), (bl, (0, ph)), (br, (pw, ph))):
        dr.line([a[0] * sc, a[1] * sc, b[0] * sc, b[1] * sc], fill=(200, 40, 40), width=1)
    # what the street's doors hide: zones of the card (bay u 350 to 5650 across the picture's 0 to 1)
    z = shop["front"]["zones_u_mm"]
    east = shop["side"] == "east"
    for nm, (a0, a1), col in (("window", z["window"], (150, 190, 220)), ("shop door glass", z["shop_door"], (200, 220, 160)), ("side door (solid)", z.get("side_door") or (0, 0), (220, 160, 160))):
        if a1 <= a0:
            continue
        # the picture's left is the viewer's left, which is u = 0 (the 2.2 frame is the viewer's)
        x0 = (a0 - 350) / 5300.0
        x1 = (a1 - 350) / 5300.0
        dr.rectangle([x0 * pw * sc, 0, x1 * pw * sc, 14], fill=col)
        dr.text((x0 * pw * sc + 3, 2), nm, fill=(20, 20, 20))
    dr.text((6, 20), "%s: the picture (4096 x %d): back wall red, its corners by the camera rule; zones across the top from the 2.2 bay frame" % (shop["id"], ph), fill=(20, 20, 20))
    return im, pts


# ---- the overlay on the main photograph ------------------------------------------------------------------------------------------
def overlay(photo_path, meas, shop, out_path):
    """Lay the target's door, stallriser and glass lines on the fish-shop photograph at the scale fitted on ONE dimension (the leaf's height)."""
    im = Image.open(photo_path).convert("RGB")
    dr = ImageDraw.Draw(im)
    top, bot = meas["leaf_top_y"], meas["leaf_bottom_y"]
    k = (bot - top) / 2040.0                        # px per mm from the leaf's height
    base = bot + 28 * k                             # the leaf's foot stands 28 above the footway: pavement line
    x_cl = meas["leaf_centre_x"]
    d = shop["door"]
    lines = {"stallriser top 600": base - 600 * k, "sill seat 625": base - 625 * k, "door glass foot": base - d["glass_foot_z_mm"] * k, "glazing bar": base - d["t1_rails_mm"]["glazing_bar"]["z"] * k,
             "leaf top 2068": base - 2068 * k, "transom 2400": base - 2400 * k}
    for name, y in lines.items():
        dr.line([(x_cl - 190, y), (x_cl + 190, y)], fill=(255, 40, 40), width=1)
        dr.text((x_cl + 192, y - 5), name, fill=(255, 40, 40))
    dr.rectangle([x_cl - 450 * k, base - 2068 * k, x_cl + 450 * k, base - 28 * k], outline=(40, 200, 40))
    dr.text((10, 10), "target on photo: scale from the leaf height 2040 mm = %d px (%.3f px/mm)" % (bot - top, k), fill=(255, 255, 0))
    im.save(out_path, quality=88)
    return {n: round(float(y), 1) for n, y in lines.items()}, k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--json")
    ap.add_argument("--shop", nargs="*")
    ap.add_argument("--photo", help="the main photograph (a crop below the fascia, as P1) to lay the target on")
    ap.add_argument("--overlay-out", help="where to write the overlay")
    a = ap.parse_args()
    t = load()
    os.makedirs(a.out, exist_ok=True)
    allp = {}
    sheet = []
    for s in t["shops"]:
        if a.shop and s["id"] not in a.shop:
            continue
        polys = front_polys(s)
        allp[s["id"] + "-front"] = polys
        im = draw_polys(polys, (1500, 760), 0.24, (30, 30), s["id"] + ": the bay in millimetres (u from the viewer's left, z from the footway; 4.1's board is a texture, here a flat colour)")
        im.save(os.path.join(a.out, s["id"] + "-front.png"))
        sheet.append((s["id"], im))
        if s.get("room"):
            pim, pp = draw_plan(s)
            allp[s["id"] + "-plan"] = pp
            pim.save(os.path.join(a.out, s["id"] + "-plan.png"))
            draw_room(s).save(os.path.join(a.out, s["id"] + "-room.png"))
            pic, pts = draw_picture(s)
            allp[s["id"] + "-picture"] = {k: list(v) for k, v in pts.items()}
            pic.save(os.path.join(a.out, s["id"] + "-picture.png"))
    if sheet:
        cols, cw, ch = 2, 750, 380
        rows = (len(sheet) + 1) // 2
        sh = Image.new("RGB", (cols * cw, rows * ch), (240, 240, 240))
        for n, (i, im) in enumerate(sheet):
            sh.paste(im.resize((cw, ch)), ((n % cols) * cw, (n // cols) * ch))
        sh.save(os.path.join(a.out, "ten-fronts-sheet.png"))
    if a.photo and a.overlay_out:
        rows = {r_["what"]: r_ for r_ in t["photographs"]["rows"]}
        crop_top = 108   # the crop's offset in the original photograph's rows
        meas = {"leaf_top_y": rows["door leaf top (underside of the transom's board)"]["y_px"] - crop_top, "leaf_bottom_y": rows["door leaf bottom / threshold"]["y_px"] - crop_top,
                "leaf_centre_x": (rows["leaf left edge"]["x_px"] + rows["leaf right edge"]["x_px"]) / 2}
        lines, k = overlay(a.photo, meas, next(s for s in t["shops"] if s["id"] == "ritas"), a.overlay_out)
        print("overlay lines (crop px):", lines, "scale px/mm %.4f" % k)
    if a.json:
        json.dump(allp, open(a.json, "w"))
    print("drew", len(sheet), "fronts into", a.out)


if __name__ == "__main__":
    main()
