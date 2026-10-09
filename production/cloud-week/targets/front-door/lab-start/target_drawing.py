"""Turn target.json into the reference drawings the front door build is checked against.

Writes F:/LedgerTools/lab/door/target/target_drawings.json (filled polygons, mm) and
elevation.png, section_h.png, section_v.png at 1 mm a pixel.

(a) elevation: outside view, x across, z up (origin: left brick reveal, top of stone sill).
(b) section_h: plan cut at the middle of the lower panels, x across, y into the wall (outside at -y).
(c) section_v: cut on the centre line of the left-hand panels, y into the wall, z up.
"""
import json, math, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(r"F:/LedgerTools/lab/door/target")
T = json.loads((HERE / "target.json").read_text(encoding="utf-8"))

L, P, M, F, B, O = T["leaf"], T["panels"], T["mouldings"], T["frame"], T["brick"], T["opening"]
W, H, TH = L["width_mm"], L["height_mm"], L["thickness_mm"]
LX0, LZ0 = L["x0_mm"], L["z0_mm"]
LY0 = L["outside_face_y_mm"]; LY1 = LY0 + TH
FY0 = F["frame_outside_face_y_mm"]; FY1 = FY0 + F["jamb_depth_mm"]
STOP_Y = FY0 + F["stop_depth_mm"]
JL0, JL1 = F["jamb_x_mm"]["left"]; JR0, JR1 = F["jamb_x_mm"]["right"]
RW = F["rebate_width_mm"]
OW, OH = O["brick_width_mm"], O["brick_height_mm"]
REV, WALL = O["reveal_depth_mm"], O["wall_thickness_mm"]
tr, hd, sl, fl = F["transom"], F["head_section_mm"], F["sill"], F["fanlight"]
bol, sgl = M["outside_bolection"], M["inside_single"]
LAP, BW, BPROJ, SW = bol["lap_over_framing_mm"], bol["width_on_face_mm"], bol["projection_above_framing_mm"], sgl["width_on_face_mm"]
PT = P["thickness_mm"]; GR = P["groove_depth_mm"]; PLAY = P["side_play_mm"]
PY0 = LY0 + (TH - PT) / 2; PY1 = PY0 + PT          # panel faces (centred)
R_OV = M["frame_ovolo_radius_mm"]
BR = 300.0                                          # brick drawn round the opening

def rect(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]

def poly(name, layer, pts, holes=None):
    d = {"name": name, "layer": layer, "pts": [[round(a, 2), round(b, 2)] for a, b in pts]}
    if holes:
        d["holes"] = [[[round(a, 2), round(b, 2)] for a, b in h] for h in holes]
    return d

def arc(cx, cy, r, a0, a1, n=8):
    return [[cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))] for i in range(n + 1)]

def leaf_xz(u, v):
    return LX0 + u, LZ0 + v

# ---------------- (a) elevation ----------------
def elevation():
    out = []
    vis_x0, vis_x1 = JL1, JR0                       # stop faces: what of the leaf shows
    out.append(poly("brick_wall", "brick", rect(-BR, sl["top_z"] - sl["thickness_mm"], OW + BR, OH + BR),
                    holes=[rect(0, sl["top_z"] - sl["thickness_mm"], OW, OH)]))
    out.append(poly("stone_sill", "stone", rect(0, sl["top_z"] - sl["thickness_mm"], OW, sl["top_z"])))
    out.append(poly("jamb_left", "frame", rect(0, 0, JL1, OH)))
    out.append(poly("jamb_right", "frame", rect(JR0, 0, OW, OH)))
    out.append(poly("head", "frame", rect(JL1, hd["z0"], JR0, OH)))
    out.append(poly("transom", "frame", rect(JL1, tr["z_stop_underside"], JR0, tr["z_top"])))
    g = fl["glass_sight_mm"]
    out.append(poly("fanlight_glass", "glass", rect(g["x0"], g["z0"], g["x1"], g["z1"])))
    out.append(poly("leaf_visible", "leaf", rect(vis_x0, LZ0, vis_x1, tr["z_stop_underside"])))
    for k, o in P["openings_leaf_uv_mm"].items():
        x0, z0 = leaf_xz(o["u0"], o["v0"]); x1, z1 = leaf_xz(o["u1"], o["v1"])
        outer = rect(x0 - LAP, z0 - LAP, x1 + LAP, z1 + LAP)
        inner = rect(x0 - LAP + BW, z0 - LAP + BW, x1 + LAP - BW, z1 + LAP - BW)
        out.append(poly(f"bolection_{k}", "moulding", outer, holes=[inner]))
        out.append(poly(f"panel_field_{k}", "panel", inner))
    lb = M["lock_rail_band"]["z_above_leaf_bottom_mm"]
    out.append(poly("lock_rail_band", "moulding", rect(vis_x0, LZ0 + lb[0], vis_x1, LZ0 + lb[1])))
    wb = M["weatherboard"]["z_above_leaf_bottom_mm"]
    out.append(poly("weatherboard", "moulding", rect(vis_x0, LZ0 + wb[0], vis_x1, LZ0 + wb[1])))
    return out

# ---------------- (b) horizontal section ----------------
def jamb_plan(left):
    if left:
        x_stop, x_reb, x_back = JL1, JL1 - RW, JL0
        pts = [[x_back, FY0]] + [[x_stop - R_OV, FY0]] + arc(x_stop - R_OV, FY0 + R_OV, R_OV, -90, 0)[1:] + \
              [[x_stop, STOP_Y], [x_reb, STOP_Y], [x_reb, FY1], [x_back, FY1]]
    else:
        x_stop, x_reb, x_back = JR0, JR0 + RW, JR1
        pts = [[x_back, FY0]] + [[x_stop + R_OV, FY0]] + arc(x_stop + R_OV, FY0 + R_OV, R_OV, -90, -180)[1:] + \
              [[x_stop, STOP_Y], [x_reb, STOP_Y], [x_reb, FY1], [x_back, FY1]]
    return pts

def bolection_profile(xe, side):
    """Outside bolection at a framing edge xe; side=+1 when the panel is at +x."""
    s = side
    pts = [[xe - s * LAP, LY0], [xe - s * LAP, LY0 - BPROJ], [xe + s * 8.0, LY0 - BPROJ],
           [xe + s * 14.0, LY0 - BPROJ + 2.5], [xe + s * 20.0, LY0 + 2.0], [xe + s * 26.0, PY0 - 3.0],
           [xe + s * (BW - LAP), PY0], [xe, PY0], [xe, LY0]]
    return pts

def single_profile(xe, side):
    s = side
    return [[xe, LY1], [xe + s * 4.0, LY1], [xe + s * 10.0, LY1 - 6.0], [xe + s * 16.0, PY1 + 4.0],
            [xe + s * SW, PY1], [xe, PY1]]

def section_h():
    out = []
    v_mid = (P["openings_leaf_uv_mm"]["bottom_left"]["v0"] + P["openings_leaf_uv_mm"]["bottom_left"]["v1"]) / 2
    out.append(poly("brick_left", "brick", [[-BR, 0], [0, 0], [0, REV], [JL0, REV], [JL0, WALL], [-BR, WALL]]))
    out.append(poly("brick_right", "brick", [[OW, 0], [OW + BR, 0], [OW + BR, WALL], [JR1, WALL], [JR1, REV], [OW, REV]]))
    out.append(poly("jamb_left", "frame", jamb_plan(True)))
    out.append(poly("jamb_right", "frame", jamb_plan(False)))
    o_l, o_r = P["openings_leaf_uv_mm"]["bottom_left"], P["openings_leaf_uv_mm"]["bottom_right"]
    xs = [LX0, LX0 + o_l["u0"], LX0 + o_l["u1"], LX0 + o_r["u0"], LX0 + o_r["u1"], LX0 + W]
    gy0, gy1 = PY0, PY1
    def member(name, x0, x1, groove_left, groove_right):
        pts = [[x0, LY0], [x1, LY0]]
        if groove_right:
            pts += [[x1, gy0], [x1 + GR, gy0], [x1 + GR, gy1], [x1, gy1]]
        pts += [[x1, LY1], [x0, LY1]]
        if groove_left:
            pts += [[x0, gy1], [x0 - GR, gy1], [x0 - GR, gy0], [x0, gy0]]
        return poly(name, "leaf", pts)
    # grooves drawn as the panel's tongue occupying the slot: members are solid outside the slot
    out.append(poly("stile_left", "leaf", [[xs[0], LY0], [xs[1], LY0], [xs[1], gy0], [xs[1] - GR, gy0], [xs[1] - GR, gy1], [xs[1], gy1], [xs[1], LY1], [xs[0], LY1]]))
    out.append(poly("muntin", "leaf", [[xs[2], LY0], [xs[3], LY0], [xs[3], gy0], [xs[3] - GR, gy0], [xs[3] - GR, gy1], [xs[3], gy1], [xs[3], LY1], [xs[2], LY1], [xs[2], gy1], [xs[2] + GR, gy1], [xs[2] + GR, gy0], [xs[2], gy0]]))
    out.append(poly("stile_right", "leaf", [[xs[4], LY0], [xs[5], LY0], [xs[5], LY1], [xs[4], LY1], [xs[4], gy1], [xs[4] + GR, gy1], [xs[4] + GR, gy0], [xs[4], gy0]]))
    for nm, a, b in (("panel_bottom_left", xs[1], xs[2]), ("panel_bottom_right", xs[3], xs[4])):
        out.append(poly(nm, "panel", rect(a - GR + PLAY / 2, gy0, b + GR - PLAY / 2, gy1)))
        out.append(poly(nm + "_bolection_l", "moulding", bolection_profile(a, +1)))
        out.append(poly(nm + "_bolection_r", "moulding", bolection_profile(b, -1)))
        out.append(poly(nm + "_single_l", "moulding", single_profile(a, +1)))
        out.append(poly(nm + "_single_r", "moulding", single_profile(b, -1)))
    return out, LZ0 + v_mid

# ---------------- (c) vertical section ----------------
def section_v():
    out = []
    o_b, o_t = P["openings_leaf_uv_mm"]["bottom_left"], P["openings_leaf_uv_mm"]["top_left"]
    u_mid = (o_b["u0"] + o_b["u1"]) / 2
    zs = [LZ0, LZ0 + o_b["v0"], LZ0 + o_b["v1"], LZ0 + o_t["v0"], LZ0 + o_t["v1"], LZ0 + H]
    gy0, gy1 = PY0, PY1
    # stone sill with rounded nose (y, z)
    sz0, sz1 = sl["top_z"] - sl["thickness_mm"], sl["top_z"]
    r = 19.0
    out.append(poly("stone_sill", "stone", [[sl["front_y_mm"], sz0]] + arc(sl["front_y_mm"] + r, sz1 - r, r, 180, 90)[0:] + [[sl["back_y_mm"], sz1], [sl["back_y_mm"], sz0]]))
    # rails (solid outside the panel slots)
    def rail(name, z0, z1, slot_below, slot_above):
        pts = [[LY0, z0]]
        if slot_below:
            pts = [[LY0, z0], [gy0, z0], [gy0, z0 - GR], [gy1, z0 - GR], [gy1, z0], [LY1, z0]]
        else:
            pts = [[LY0, z0], [LY1, z0]]
        if slot_above:
            pts += [[LY1, z1], [gy1, z1], [gy1, z1 + GR], [gy0, z1 + GR], [gy0, z1], [LY0, z1]]
        else:
            pts += [[LY1, z1], [LY0, z1]]
        return poly(name, "leaf", pts)
    out.append(poly("bottom_rail", "leaf", [[LY0, zs[0]], [LY1, zs[0]], [LY1, zs[1]], [gy1, zs[1]], [gy1, zs[1] - GR], [gy0, zs[1] - GR], [gy0, zs[1]], [LY0, zs[1]]]))
    out.append(poly("lock_rail", "leaf", [[LY0, zs[2]], [gy0, zs[2]], [gy0, zs[2] + GR], [gy1, zs[2] + GR], [gy1, zs[2]], [LY1, zs[2]], [LY1, zs[3]], [gy1, zs[3]], [gy1, zs[3] - GR], [gy0, zs[3] - GR], [gy0, zs[3]], [LY0, zs[3]]]))
    out.append(poly("top_rail", "leaf", [[LY0, zs[4]], [gy0, zs[4]], [gy0, zs[4] + GR], [gy1, zs[4] + GR], [gy1, zs[4]], [LY1, zs[4]], [LY1, zs[5]], [LY0, zs[5]]]))
    out.append(poly("panel_bottom_left", "panel", rect(gy0, zs[1] - GR, gy1, zs[2] + GR)))
    out.append(poly("panel_top_left", "panel", rect(gy0, zs[3] - GR, gy1, zs[4] + GR)))
    # mouldings at the four rail edges: bolection outside, single inside (same profiles, turned)
    def turn(pts, ze, side):
        # profile functions give (x, y); here x is along z
        return [[y, ze + (x - ze)] for x, y in pts]
    for nm, ze, side in (("bottom_panel_lower", zs[1], +1), ("bottom_panel_upper", zs[2], -1),
                         ("top_panel_lower", zs[3], +1), ("top_panel_upper", zs[4], -1)):
        out.append(poly(nm + "_bolection", "moulding", [[y, x] for x, y in bolection_profile(ze, side)]))
        out.append(poly(nm + "_single", "moulding", [[y, x] for x, y in single_profile(ze, side)]))
    lb = M["lock_rail_band"]; wb = M["weatherboard"]
    out.append(poly("lock_rail_band", "moulding", rect(LY0 - lb["projection_mm"], LZ0 + lb["z_above_leaf_bottom_mm"][0], LY0, LZ0 + lb["z_above_leaf_bottom_mm"][1])))
    wz0, wz1 = LZ0 + wb["z_above_leaf_bottom_mm"][0], LZ0 + wb["z_above_leaf_bottom_mm"][1]
    out.append(poly("weatherboard", "moulding", [[LY0, wz0], [LY0 - wb["projection_mm"], wz0], [LY0 - wb["projection_mm"], wz0 + 12.0], [LY0, wz1]]))
    # transom (stop part outside, rebated for the leaf inside, slot for the glass)
    gy_a, gy_b = fl["glass_y_mm"] - fl["glass_thickness_mm"] / 2, fl["glass_y_mm"] + fl["glass_thickness_mm"] / 2
    gr = fl["glass_rebate_mm"]
    out.append(poly("transom", "frame", [[FY0, tr["z_stop_underside"]], [STOP_Y, tr["z_stop_underside"]], [STOP_Y, tr["rebate_underside_z"]],
                                          [FY1, tr["rebate_underside_z"]], [FY1, tr["z_top"]], [gy_b, tr["z_top"]], [gy_b, tr["z_top"] - gr],
                                          [gy_a, tr["z_top"] - gr], [gy_a, tr["z_top"]], [FY0, tr["z_top"]]]))
    g = fl["glass_sight_mm"]
    out.append(poly("fanlight_glass", "glass", rect(gy_a, g["z0"] - gr, gy_b, g["z1"] + gr)))
    hz0, hz1 = hd["z0"], hd["z0"] + hd["height"]
    out.append(poly("head", "frame", [[FY0, hz0], [gy_a, hz0], [gy_a, hz0 + gr], [gy_b, hz0 + gr], [gy_b, hz0], [FY1, hz0], [FY1, hz1], [FY0, hz1]]))
    out.append(poly("brick_over_head", "brick", [[0, OH], [FY0, OH], [FY0, hz1], [WALL, hz1], [WALL, OH + BR], [0, OH + BR]]))
    return out, LX0 + u_mid

LAYER_RGB = {"brick": (176, 96, 72), "stone": (190, 190, 180), "frame": (235, 235, 228), "glass": (150, 190, 205),
             "leaf": (170, 30, 30), "panel": (205, 60, 55), "moulding": (120, 15, 15)}

def render(polys, axes, path, flip=True):
    from PIL import Image, ImageDraw
    xs = [p[0] for d in polys for p in d["pts"]]; ys = [p[1] for d in polys for p in d["pts"]]
    x0, x1, y0, y1 = min(xs) - 20, max(xs) + 20, min(ys) - 20, max(ys) + 20
    w, h = int(math.ceil(x1 - x0)), int(math.ceil(y1 - y0))
    im = Image.new("RGB", (w, h), (255, 255, 255)); dr = ImageDraw.Draw(im)
    def tp(p):
        return (p[0] - x0, (y1 - p[1]) if flip else (p[1] - y0))
    for d in polys:
        dr.polygon([tp(p) for p in d["pts"]], fill=LAYER_RGB[d["layer"]], outline=(0, 0, 0))
        for hole in d.get("holes", []):
            dr.polygon([tp(p) for p in hole], fill=(255, 255, 255), outline=(0, 0, 0))
    im.save(path)
    return w, h, [x0, y0]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    el = elevation()
    sh, z_cut = section_h()
    sv, x_cut = section_v()
    # elevation: holes punched in brick must be refilled by later polygons; render order = list order
    doc = {"source": "target.json (" + T["status"][:40] + "...)", "units": "mm",
           "elevation": {"axes": "x across, z up; origin left brick reveal, top of sill", "polygons": el},
           "section_h": {"axes": "x across, y into the wall (outside -y)", "cut_z_mm": round(z_cut, 1), "polygons": sh},
           "section_v": {"axes": "y into the wall (outside -y), z up", "cut_x_mm": round(x_cut, 1), "polygons": sv}}
    (OUT / "target_drawings.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
    info = {}
    info["elevation"] = render(el, "xz", OUT / "elevation.png", flip=True)
    info["section_h"] = render(sh, "xy", OUT / "section_h.png", flip=False)   # outside at top of the picture
    info["section_v"] = render(sv, "yz", OUT / "section_v.png", flip=True)    # outside at left
    for k, v in info.items():
        print(k, "png", v[0], "x", v[1], "px (1 mm/px), origin offset", [round(a, 1) for a in v[2]])
    print("cut planes: section_h z =", round(z_cut, 1), "mm; section_v x =", round(x_cut, 1), "mm")

if __name__ == "__main__":
    main()
