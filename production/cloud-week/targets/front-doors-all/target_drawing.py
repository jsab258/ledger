"""Draws the front-doors-all target from target.json ALONE as filled polygons in millimetres (an elevation of each kind in the 3.1 frame x, z; the
mouldings' and glass's sections; the street's rows) into a JSON file, and as pictures into a folder.
  /home/user/.bpyenv/bin/python target_drawing.py OUT_DIR [--json FILE] [--overlay KIND PHOTO OUT.jpg]
Pictures never go into git outside production/previews/. Reads nothing but target.json (and, for --overlay, one photograph and its recorded box)."""
import argparse
import json
import math
import os
import sys

from shapely.affinity import translate
from shapely.geometry import MultiPolygon, Point, Polygon, box
from shapely.ops import unary_union

from td_common import TARGET_JSON, load_json

sys.dont_write_bytecode = True


def circle(cx, cz, r, n=28):
    return Point(cx, cz).buffer(r, resolution=max(4, n // 4))


def rect(x0, z0, x1, z1):
    return box(min(x0, x1), min(z0, z1), max(x0, x1), max(z0, z1))


def arch_rect(x0, z0, x1, z1):
    """A rectangle whose head is a semicircle (T3's small light): the arch springs at z1 - half the width."""
    w = x1 - x0
    r = w / 2.0
    body = rect(x0, z0, x1, z1 - r)
    head = circle((x0 + x1) / 2.0, z1 - r, r, 40)
    return unary_union([body, head])


def poly_coords(g):
    if g.is_empty:
        return []
    if isinstance(g, (MultiPolygon,)) or g.geom_type == "GeometryCollection":
        out = []
        for p in g.geoms:
            out += poly_coords(p)
        return out
    if g.geom_type != "Polygon":
        return []
    return [{"exterior": [[round(x, 2), round(z, 2)] for x, z in g.exterior.coords], "holes": [[[round(x, 2), round(z, 2)] for x, z in h.coords] for h in g.interiors]}]


def frame_of(T, k):
    spec = T["kinds"][k]
    fs = T["frame_sets"]["FF6"] if k == "F6" else T["frame_sets"][spec["frame_set"][0]]
    return spec, fs


def head_polygon(fs):
    x0 = fs["jamb_x"]["left"][0]
    x1 = fs["jamb_x"]["right"][1]
    z0 = fs["head_z"][0]
    if fs["head_top"] == fs["head_ends"]:
        return rect(x0, z0, x1, fs["head_top"])
    # the cambered head of frame set T: a circle through (0, ends), (opening_w/2, crown), (opening_w, ends); the head's top is cut to it
    ow = fs["opening_w"]
    ends, crown = fs["head_ends"], fs["head_top"]
    sag = crown - ends
    R = ((ow / 2.0) ** 2 + sag ** 2) / (2.0 * sag)
    cx, cz = ow / 2.0, crown - R
    pts = [(x0, z0), (x1, z0)]
    n = 40
    for i in range(n + 1):
        x = x1 - (x1 - x0) * i / n
        zz = cz + math.sqrt(max(R * R - (x - cx) ** 2, 0.0))
        pts.append((x, min(zz, crown + 1.0)))
    return Polygon(pts)


def draw_kind(T, k):
    spec, fs = frame_of(T, k)
    lf = spec["leaf"]
    x0 = fs["leaf_x0"]
    z0 = fs["leaf_z0"]
    L = {}
    jl = rect(fs["jamb_x"]["left"][0], 0.0, fs["jamb_x"]["left"][1], fs["head_z"][0])
    jr = rect(fs["jamb_x"]["right"][0], 0.0, fs["jamb_x"]["right"][1], fs["head_z"][0])
    head = head_polygon(fs)
    tr = rect(fs["transom_x"][0], fs["transom_z"][0], fs["transom_x"][1], fs["transom_z"][1])
    L["frame"] = unary_union([jl, jr, head, tr])
    gx0, gx1 = fs["glass_opening_x"]
    gz0, gz1 = fs["glass_opening_z"]
    L["transom_glass"] = rect(gx0, gz0, gx1, gz1)
    leaf = rect(x0, z0, x0 + lf["w"], z0 + lf["h"])
    L["leaf"] = leaf
    L["visible"] = rect(fs["visible_leaf_x"][0], fs["visible_leaf_z"][0], fs["visible_leaf_x"][1], fs["visible_leaf_z"][1])
    ops = {}
    for o in lf["openings"]:
        ox0, ox1 = x0 + o["u0"], x0 + o["u1"]
        oz0, oz1 = z0 + o["v0"], z0 + o["v1"]
        if o["type"] == "arched_light":
            g = arch_rect(ox0, oz0, ox1, oz1)
        elif o["type"] == "spyhole":
            g = circle((ox0 + ox1) / 2.0, (oz0 + oz1) / 2.0, (ox1 - ox0) / 2.0)
        else:
            g = rect(ox0, oz0, ox1, oz1)
        ops[o["id"]] = g
    L["openings"] = ops
    # mouldings: a ring of the moulding's width inside each panel opening
    mw = spec["mouldings"]["outside"].get("width_on_face")
    rings = []
    for o in lf["openings"]:
        if o["type"] == "panel" and mw:
            outer = ops[o["id"]]
            inner = outer.buffer(-mw, join_style=2)
            rings.append(outer.difference(inner) if not inner.is_empty else outer)
        if o["type"] == "embossed_panel":
            outer = ops[o["id"]]
            inner = outer.buffer(-14.0, join_style=2)
            rings.append(outer.difference(inner) if not inner.is_empty else outer)
    L["mouldings"] = unary_union(rings) if rings else Polygon()
    # glazing bars of T2 and F4 are the framing between lights: nothing to add; the leaded fanlight's lattice lines
    came = Polygon()
    if spec["glass"].get("transom") == "leaded_diamond":
        g = T["glass"]["leaded_diamond"]
        dw, dh = g["diamond"]
        cw = g["came_w"]
        lines = []
        gx = gx0 - dw
        nx = int((gx1 - gx0) / (dw / 2.0)) + 4
        for i in range(-2, nx):
            xa = gx0 + i * dw / 2.0
            lines.append(Polygon([(xa, gz0), (xa + dw / 2.0, gz1), (xa + dw / 2.0 + cw, gz1), (xa + cw, gz0)]))
            lines.append(Polygon([(xa + dw / 2.0, gz0), (xa, gz1), (xa + cw, gz1), (xa + dw / 2.0 + cw, gz0)]))
        came = unary_union(lines).intersection(L["transom_glass"])
    L["lead_came"] = came
    # the ledged door's board joints and nail heads
    joints, nails = [], []
    if lf.get("board_edges_u"):
        for u in lf["board_edges_u"][1:-1]:
            joints.append(rect(x0 + u - 3.0, z0, x0 + u + 3.0, z0 + lf["h"]))
        for u, v in lf["nail_heads"]["at"]:
            nails.append(circle(x0 + u, z0 + v, lf["nail_heads"]["dia"] / 2.0, 12))
    L["board_joints"] = unary_union(joints) if joints else Polygon()
    L["nail_heads"] = unary_union(nails) if nails else Polygon()
    # furniture, from the first house of the kind (variants are per house; the kind's own default is its first house's)
    furn = {}
    h0 = [h for h in T["street"]["houses"] if h["kind"] == k][0]
    for slot, d in h0["furniture"].items():
        var, pl = d["variant"], d["place"]
        cat = T["furniture"][slot][var]
        if not pl:
            continue
        u = pl.get("u")
        if u == "leaf centre":
            u = lf["w"] / 2.0 if k not in ("T1", "T2", "T3") else lf["w"] / 2.0
        v = pl.get("v")
        g = None
        if slot == "letter_plate" and isinstance(u, (int, float)) and v is not None:
            w, h = cat["outer"]
            if cat["name"].startswith("brass plate, vertical"):
                g = rect(x0 + u - w / 2.0, z0 + v - h / 2.0, x0 + u + w / 2.0, z0 + v + h / 2.0)
            else:
                g = rect(x0 + u - w / 2.0, z0 + v - h / 2.0, x0 + u + w / 2.0, z0 + v + h / 2.0)
        elif slot == "handle" and isinstance(u, (int, float)) and v is not None:
            if "knob" in cat["name"]:
                g = circle(x0 + u, z0 + v, cat["dia"] / 2.0)
            elif "bar pull" in cat["name"]:
                g = rect(x0 + u - cat["size"][0] / 2.0, z0 + v - cat["size"][1] / 2.0, x0 + u + cat["size"][0] / 2.0, z0 + v + cat["size"][1] / 2.0)
            elif "thumb latch" in cat["name"]:
                g = rect(x0 + u - cat["plate"][0] / 2.0, z0 + v - cat["plate"][1] / 2.0, x0 + u + cat["plate"][0] / 2.0, z0 + v + cat["plate"][1] / 2.0)
            else:
                rose = circle(x0 + u, z0 + v, cat["rose_dia"] / 2.0)
                direction = 1.0 if lf.get("lock_side") == "left" else -1.0
                lever = rect(x0 + u, z0 + v - cat["lever"][1] / 2.0, x0 + u + direction * cat["lever"][0], z0 + v + cat["lever"][1] / 2.0)
                g = unary_union([rose, lever])
        elif slot == "latch" and v is not None:
            xs = fs["stop_edges_x"][1] - 46.6 if lf.get("lock_side") != "left" else fs["stop_edges_x"][0] + 46.6
            g = circle(xs, z0 + v, cat["collar"] / 2.0)
        elif slot == "bell" and var == "BL1":
            w, hh = cat["size"]
            cx = pl["x"]
            g = rect(cx - w / 2.0, pl["z_range"][0], cx + w / 2.0, pl["z_range"][1])
        elif slot == "number" and v is not None and isinstance(pl.get("v"), (int, float)):
            dh = cat.get("digit", [0, cat.get("digit_h", 60.0)])[1] if "digit" in cat else cat.get("digit_h", 60.0)
            n3 = 3
            wd = (cat.get("digit", [51.0, 56.0])[0] if "digit" in cat else 38.0) * n3 + 12.0 * (n3 - 1)
            g = rect(x0 + lf["w"] / 2.0 - wd / 2.0, z0 + v - dh / 2.0, x0 + lf["w"] / 2.0 + wd / 2.0, z0 + v + dh / 2.0)
        if g is not None:
            furn["%s:%s" % (slot, var)] = g
    L["furniture"] = furn
    return L


def sections(T):
    out = {}
    pr = T["kinds"]["T1"]["mouldings"]["outside"]["profile_dh"]
    out["bolection_T1_46"] = Polygon([(d, h) for d, h in pr] + [(4.8, -16.95 * 0 - 17.0)]) if False else Polygon([(d, h) for d, h in pr])
    out["stuck_ovolo_F3"] = Polygon([(d, h) for d, h in T["kinds"]["F3"]["mouldings"]["outside"]["profile_dh"]])
    out["embossed_step_T3"] = Polygon([(d, -h) for d, h in T["kinds"]["T3"]["mouldings"]["outside"]["profile_dh"]] + [(40.0, -8.0), (0.0, -8.0)])
    rs = T["glass"]["reeded_4mm"]
    pts = [[0.0, 4.0]]
    n = int(round(24.0 / rs["flute_pitch"]))
    for i in range(n):
        for j in range(0, 7):
            t = j / 6.0
            pts.append([i * rs["flute_pitch"] + t * rs["flute_pitch"], 4.0 + rs["flute_depth"] * math.sin(math.pi * t)])
    pts += [[24.0, 0.0], [0.0, 0.0]]
    out["reeded_glass"] = Polygon(pts)
    vj = T["kinds"]["F7"]["mouldings"]["outside"]["profile"]
    out["v_joint_F7"] = Polygon([[x, y] for x, y in vj] + [[vj[-1][0], -22.0], [vj[0][0], -22.0]])
    # the plan section through a jamb, the stop and the leaf's edge (T): x across, y into the wall (outside negative); used by the angle check
    fs = T["frame_sets"]["T"]
    j = fs["jamb_x"]["left"]
    out["plan_jamb_T"] = Polygon([(j[0], 0.0), (fs["stop_edges_x"][0], 0.0), (fs["stop_edges_x"][0], 74.0 - 74.0 + 0.0), (fs["stop_edges_x"][0], 0.0)]) if False else rect(j[0], 0.0, fs["stop_edges_x"][0], fs["jamb_depth"])
    return out


def street_rows(T):
    rows = {}
    for side in ("east", "west"):
        items = []
        for hid in T["street"]["order"][side]:
            h = [x for x in T["street"]["houses"] if x["house"] == hid][0]
            items.append({"house": hid, "kind": h["kind"], "x_centre_m": h["x_centre_m"], "paint": h["paint"], "condition": h["condition"]})
        rows[side] = items
    return rows


def drawing(T):
    D = {"units": "mm", "kinds": {}}
    for k in T["kinds"]:
        L = draw_kind(T, k)
        D["kinds"][k] = {"frame": poly_coords(L["frame"]), "transom_glass": poly_coords(L["transom_glass"]), "leaf": poly_coords(L["leaf"]), "visible": poly_coords(L["visible"]),
                         "openings": {i: poly_coords(g) for i, g in L["openings"].items()}, "mouldings": poly_coords(L["mouldings"]), "lead_came": poly_coords(L["lead_came"]),
                         "board_joints": poly_coords(L["board_joints"]), "nail_heads": poly_coords(L["nail_heads"]), "furniture": {n: poly_coords(g) for n, g in L["furniture"].items()}}
    D["sections"] = {n: poly_coords(g) for n, g in sections(T).items()}
    D["street_rows"] = street_rows(T)
    return D


# ---- pictures
def _paint_rgb(T, pid):
    for p in T["paints"]:
        if p["id"] == pid:
            return tuple(p["srgb"])
    return (120, 120, 120)


def picture_kinds(T, out_dir, scale=0.26):
    from PIL import Image, ImageDraw, ImageFont
    ks = list(T["kinds"].keys())
    pad = 14
    W = 1040
    H = 2420
    cw, ch = int(W * scale), int(H * scale)
    cols = 5
    rows = (len(ks) + cols - 1) // cols
    im = Image.new("RGB", (cols * (cw + pad) + pad, rows * (ch + pad + 16) + pad), (36, 36, 38))
    d = ImageDraw.Draw(im)
    for n, k in enumerate(ks):
        L = draw_kind(T, k)
        h0 = [h for h in T["street"]["houses"] if h["kind"] == k][0]
        col = _paint_rgb(T, h0["paint"])
        ox = pad + (n % cols) * (cw + pad)
        oy = pad + (n // cols) * (ch + pad + 16) + 14

        def P(g, fill, outline=None, hole_fill=(36, 36, 38)):
            for part in poly_coords(g):
                pts = [(ox + (x + 60) * scale, oy + (H - 40 - z) * scale) for x, z in part["exterior"]]
                d.polygon(pts, fill=fill, outline=outline)
                for hole in part["holes"]:
                    pts = [(ox + (x + 60) * scale, oy + (H - 40 - z) * scale) for x, z in hole]
                    d.polygon(pts, fill=hole_fill)
        d.text((ox, oy - 14), "%s %s" % (k, h0["paint"]), fill=(240, 240, 120))
        P(L["frame"], (226, 224, 214))
        P(L["transom_glass"], (60, 70, 80))
        P(L["lead_came"], (150, 152, 155))
        P(L["leaf"], col)
        for i, g in L["openings"].items():
            typ = [o for o in T["kinds"][k]["leaf"]["openings"] if o["id"] == i][0]["type"]
            P(g, (60, 70, 80) if typ in ("light", "slit_light", "arched_light", "spyhole") else tuple(int(c * 0.82) for c in col))
        for i, g in L["openings"].items():
            typ = [o for o in T["kinds"][k]["leaf"]["openings"] if o["id"] == i][0]["type"]
            if typ in ("panel", "embossed_panel"):
                P(g.difference(g.buffer(-(T["kinds"][k]["mouldings"]["outside"].get("width_on_face") or 14.0), join_style=2)), tuple(min(255, int(c * 1.35) + 18) for c in col))
                P(g.buffer(-(T["kinds"][k]["mouldings"]["outside"].get("width_on_face") or 14.0), join_style=2), (30, 30, 32) if k in ("T1", "F1", "F2", "F3") else tuple(int(c * 0.9) for c in col))
        for i, g in L["openings"].items():
            typ = [o for o in T["kinds"][k]["leaf"]["openings"] if o["id"] == i][0]["type"]
            if typ in ("light", "slit_light", "arched_light", "spyhole"):
                P(g, (60, 70, 80))
        P(L["board_joints"], tuple(int(c * 0.6) for c in col))
        P(L["nail_heads"], (170, 170, 165))
        for name, g in L["furniture"].items():
            P(g, (200, 170, 100) if "brass" in name or name.startswith("letter_plate:LP1") else (210, 210, 205), (30, 30, 30))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "kinds-elevations.png")
    im.save(path)
    return path


def picture_rows(T, out_dir, scale=0.055):
    from PIL import Image, ImageDraw
    pad = 20
    W = int(46000 * scale) + 2 * pad
    H = 2 * int(2600 * scale * 1.4) + 3 * pad + 60
    im = Image.new("RGB", (W, H), (36, 36, 38))
    d = ImageDraw.Draw(im)
    y0 = pad
    for side in ("east", "west"):
        d.text((pad, y0), side + " side, doors in street order (x along the street, m)", fill=(240, 240, 120))
        y0 += 14
        for hid in T["street"]["order"][side]:
            h = [x for x in T["street"]["houses"] if x["house"] == hid][0]
            k = h["kind"]
            spec, fs = frame_of(T, k)
            lf = spec["leaf"]
            col = _paint_rgb(T, h["paint"])
            cx = pad + h["x_centre_m"] * 1000.0 * scale
            top = y0 + 2400 * scale * 1.4
            px = cx - lf["w"] / 2.0 * scale * 1.4
            d.rectangle([px - 4, top - (lf["h"] + 120) * scale * 1.4, px + lf["w"] * scale * 1.4 + 4, top], fill=(226, 224, 214))
            d.rectangle([px, top - lf["h"] * scale * 1.4, px + lf["w"] * scale * 1.4, top], fill=col)
            for o in lf["openings"]:
                typ = o["type"]
                fillc = (60, 70, 80) if typ in ("light", "slit_light", "arched_light") else tuple(int(c * 0.8) for c in col)
                d.rectangle([px + o["u0"] * scale * 1.4, top - o["v1"] * scale * 1.4, px + o["u1"] * scale * 1.4, top - o["v0"] * scale * 1.4], fill=fillc)
            d.text((px, top + 2), "%s" % k, fill=(230, 230, 230))
        y0 += int(2600 * scale * 1.4) + pad + 30
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "street-rows.png")
    im.save(path)
    return path


def overlay(T, kind, photo_path, out_path, box_px, scale_fit="height"):
    """Draws the kind's visible-face drawing on a photograph: the scale is fitted on the visible HEIGHT only (box_px = the photograph's visible-face box)."""
    from PIL import Image, ImageDraw
    L = draw_kind(T, kind)
    spec, fs = frame_of(T, kind)
    vx0, vx1 = fs["visible_leaf_x"]
    vz0, vz1 = fs["visible_leaf_z"]
    x0, y0, x1, y1 = box_px
    s = (y1 - y0) / (vz1 - vz0)
    ux = x0 - 0.0
    im = Image.open(photo_path).convert("RGB")
    d = ImageDraw.Draw(im)

    def to_px(x, z):
        return (x0 + (x - vx0) * s, y1 - (z - vz0) * s)

    def outline(g, col, w=1):
        for part in poly_coords(g):
            pts = [to_px(x, z) for x, z in part["exterior"]]
            d.line(pts + [pts[0]], fill=col, width=w)
    outline(L["visible"], (255, 255, 0), 1)
    for i, g in L["openings"].items():
        outline(g, (255, 40, 40), 1)
    outline(L["mouldings"], (255, 140, 0), 1)
    for n, g in L["furniture"].items():
        outline(g, (40, 255, 40), 1)
    im.save(out_path, quality=88)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--json", default="")
    ap.add_argument("--overlay", nargs=4, metavar=("KIND", "PHOTO", "OUT", "BOX"), default=None, help="BOX as x0,y0,x1,y1 in the photograph's pixels")
    a = ap.parse_args()
    T = load_json(TARGET_JSON)
    D = drawing(T)
    if a.json:
        with open(a.json, "w") as f:
            json.dump(D, f)
    print(picture_kinds(T, a.out_dir))
    print(picture_rows(T, a.out_dir))
    if a.overlay:
        k, ph, out, bx = a.overlay
        print(overlay(T, k, ph, out, [float(v) for v in bx.split(",")]))
    print("polygons:", sum(len(v["leaf"]) for v in D["kinds"].values()), "kinds:", len(D["kinds"]))


if __name__ == "__main__":
    main()
