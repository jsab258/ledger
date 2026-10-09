"""Draws the Quay Street pillar box from target.json ALONE, as filled polygons in millimetres.

    /home/user/.bpyenv/bin/python target_drawing.py --json OUT.json --pics PIC_DIR [--target target.json]

Writes
  OUT.json : every view as a list of polygons (name, material, exterior, holes), 1 mm a pixel
  PIC_DIR/ : front elevation, side elevation, axial section, a sheet of plans (horizontal sections), PNG, 1 mm a pixel
Pictures never go into git outside production/previews/ (make_previews.py reduces them there).

Frames: elevations and the section: x (or y for the side) across, z up; plans: x right, y up (the front is up the page).
Materials: red, black, iron, white (enamel), brass, interior, hole (the slot), line.
"""
import argparse
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont
from shapely.geometry import Polygon, box, Point, LineString, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

COL = {"red": (150, 30, 32), "black": (35, 35, 36), "iron": (96, 84, 76), "white": (232, 229, 218), "brass": (150, 125, 70),
       "interior": (8, 8, 8), "hole": (8, 8, 8), "cavity": (236, 233, 228), "reserved": (156, 36, 38), "line": (70, 12, 14), "door": (160, 36, 38), "pad": (162, 40, 42), "wall": (110, 100, 92),
       "knuckle": (140, 30, 32), "pin": (60, 52, 46), "wallcut": (60, 56, 52)}


# -----------------------------------------------------------------------------------------------------------------
def load(path):
    return json.load(open(path))


class Box:
    """geometry helpers built from target.json only"""

    def __init__(self, t):
        self.t = t
        self.prof = [tuple(p) for p in t["profile"]["outer_rz"]]
        P = t["parts"]
        self.R = t["overall"]["body_diameter"] / 2.0
        self.H = t["overall"]["total_height"]
        self.Rf = t["overall"]["foot_diameter"] / 2.0
        self.Rc = t["overall"]["cap_diameter"] / 2.0
        ap = P["aperture"]
        self.ap = ap
        self.slot = ap["slot"]
        self.hood = ap["hood"]
        self.sill = ap["sill"]
        self.door = P["door"]
        self.pan = P["panels"]
        self.pl = P["plates"]
        self.black_top = t["paint"]["black_base"]["top_z"]
        self.wall = t["profile"]["wall_thickness"]

    # radius of the lathe at z (the outermost radius at that height; the profile steps horizontally in places)
    def r_at(self, z):
        best = 0.0
        for (r0, z0), (r1, z1) in zip(self.prof[:-1], self.prof[1:]):
            lo, hi = min(z0, z1), max(z0, z1)
            if lo - 1e-9 <= z <= hi + 1e-9:
                if abs(z1 - z0) < 1e-9:
                    r = max(r0, r1)
                else:
                    r = r0 + (r1 - r0) * (z - z0) / (z1 - z0)
                best = max(best, r)
        return best

    def half_polygon(self):
        pts = list(self.prof)
        pts = [(0.0, pts[0][1])] + pts + [(0.0, pts[-1][1])]
        return Polygon(pts)

    def silhouette(self):
        h = self.half_polygon()
        return unary_union([h, affinity.scale(h, xfact=-1, yfact=1, origin=(0, 0))])


def rrect(x0, z0, x1, z1, r):
    b = box(x0, z0, x1, z1)
    if r <= 0:
        return b
    return b.buffer(-r).buffer(r)


def disc(cx, cz, d, n=48):
    return Point(cx, cz).buffer(d / 2.0, resolution=n)


def polys_of(geom):
    if geom.is_empty:
        return []
    if isinstance(geom, Polygon):
        return [geom]
    return [g for g in getattr(geom, "geoms", []) if isinstance(g, Polygon) and not g.is_empty]


def to_json(name, material, geom):
    out = []
    for p in polys_of(geom):
        out.append({"name": name, "material": material,
                    "exterior": [[round(x, 2), round(y, 2)] for x, y in p.exterior.coords],
                    "holes": [[[round(x, 2), round(y, 2)] for x, y in h.coords] for h in p.interiors]})
    return out


# -----------------------------------------------------------------------------------------------------------------
# views
# -----------------------------------------------------------------------------------------------------------------
def lock_parts(b):
    lk = b.door["lock"]
    return lk


def front_elevation(b):
    t = b.t
    L = []  # (name, material, geometry), drawn in order
    sil = b.silhouette()
    ap_z0 = b.slot["z0"]; ap_z1 = b.slot["z1"]
    hood_x = b.hood["outer_radius"] * math.sin(math.radians(b.hood["half_angle_deg"]))
    sill_x = (b.R + b.sill["projection"]) * math.sin(math.radians(b.sill["half_angle_deg"]))
    L.append(("body_red", "red", sil.difference(box(-400, -400, 400, b.black_top))))
    L.append(("base_black", "black", sil.intersection(box(-400, -400, 400, b.black_top))))
    # the mouldings: a thin line across the elevation at each ring edge of the profile
    cap = t["parts"]["cap"]
    for z in [48, 60, 72, 140, cap["soffit_z"], cap["rim_z"][0], cap["rim_z"][1], cap["rim_z"][1] + 12, cap["dome_base_z"]]:
        r = b.r_at(z)
        if r > 0:
            L.append(("ring_line", "line", LineString([(-r, z), (r, z)]).buffer(0.9, cap_style=2)))
    # door: flush; the groove shows it
    d = b.door
    L.append(("door_joint", "line", rrect(d["x0"] - 3, d["z0"] - 3, d["x1"] + 3, d["z1"] + 3, d["corner_radius"] + 3).difference(rrect(d["x0"], d["z0"], d["x1"], d["z1"], d["corner_radius"]))))
    L.append(("door", "door", rrect(d["x0"], d["z0"], d["x1"], d["z1"], d["corner_radius"])))
    # FLUSH reserved areas for the lettering and the cypher: no geometry and painted the surrounding red (the body's, the door's);
    # only the thin outline below is an annotation of this DRAWING, not part of the box
    lt = b.pan["reserved_for_lettering"]
    ltb = box(lt["x0"], lt["z0"], lt["x1"], lt["z1"])
    L.append(("reserved_for_lettering_FLUSH", "red", ltb))
    L.append(("annotation_outline_reserved_for_lettering", "line", ltb.exterior.buffer(0.5).difference(box(lt["x0"] + 20, lt["z1"] - 1, lt["x0"] + 20.2, lt["z1"] + 1))))  # a 0.2 mm slit: no hole, so the picture does not paint the area
    cy = b.pan["reserved_for_cypher"]
    cyd = disc(cy["cx"], cy["cz"], cy["diameter"])
    L.append(("reserved_for_cypher_FLUSH", "door", cyd))
    L.append(("annotation_outline_reserved_for_cypher", "line", cyd.exterior.buffer(0.5).difference(box(cy["cx"] - 0.1, cy["cz"] + cy["diameter"] / 2 - 1, cy["cx"] + 0.1, cy["cz"] + cy["diameter"] / 2 + 1))))
    # the one plate frame and its plate
    fr = b.pl["collection_frame"]
    x0, x1 = fr["cx"] - fr["outer_w"] / 2, fr["cx"] + fr["outer_w"] / 2
    z0, z1 = fr["cz"] - fr["outer_h"] / 2, fr["cz"] + fr["outer_h"] / 2
    L.append(("collection_frame", "pad", rrect(x0, z0, x1, z1, 4)))
    L.append(("collection_plate", "white", box(x0 + fr["bezel"], z0 + fr["bezel"], x1 - fr["bezel"], z1 - fr["bezel"])))
    # lock: escutcheon, keyhole, painted shutter with a dark edge
    lk = d["lock"]
    L.append(("lock_escutcheon", "pad", disc(lk["x"], lk["z"], lk["escutcheon_diameter"])))
    L.append(("keyhole", "interior", box(lk["x"] - lk["keyhole_w"] / 2, lk["z"] - lk["keyhole_h"] / 2, lk["x"] + lk["keyhole_w"] / 2, lk["z"] + lk["keyhole_h"] / 2)))
    sx0, sx1 = lk["x"] - lk["shutter_w"] / 2, lk["x"] + lk["shutter_w"] / 2
    sz0 = lk["z"] + lk["keyhole_h"] / 2 - 1
    sz1 = sz0 + lk["shutter_h"]
    L.append(("keyhole_shutter", "door", box(sx0, sz0, sx1, sz1)))
    L.append(("keyhole_shutter_edge", "pin", box(sx0, sz1 - lk["shutter_edge_width"], sx1, sz1)))
    # aperture: sill, hood, slot
    L.append(("sill", "red", box(-sill_x, b.sill["section_rz"][0][1], sill_x, ap_z0)))
    L.append(("sill_line", "line", LineString([(-sill_x, b.sill["section_rz"][0][1]), (sill_x, b.sill["section_rz"][0][1])]).buffer(0.9, cap_style=2)))
    L.append(("hood", "red", box(-hood_x, b.hood["z0"], hood_x, b.hood["top_z"])))
    L.append(("hood_front_edge", "line", LineString([(-hood_x, b.hood["front_top_z"]), (hood_x, b.hood["front_top_z"])]).buffer(0.9, cap_style=2)))
    L.append(("slot", "hole", rrect(b.slot["x0"], ap_z0, b.slot["x1"], ap_z1, b.slot["corner_radius"])))
    fl = b.ap["flap"]
    L.append(("flap", "iron", box(-fl["width"] / 2, ap_z1 - fl["height"] * 0.66, fl["width"] / 2, ap_z1 - 1)))
    return L, (-340, -60, 340, b.H + 30)


def side_elevation(b):
    L = []
    sil = b.silhouette()
    ext = [sil]
    d = b.door
    Rd = b.R + d["proud"]
    ext.append(box(b.R - 5, d["z0"], Rd, d["z1"]))
    hd = b.hood
    ext.append(Polygon([(b.R - 5, hd["z0"]), (b.R + hd["projection"], hd["z0"]), (b.R + hd["projection"], hd["front_top_z"]), (b.R, hd["top_z"]), (b.R - 5, hd["top_z"])]))
    sl = b.sill
    ext.append(Polygon([(b.R - 5, sl["section_rz"][0][1]), (sl["section_rz"][0][0], sl["section_rz"][0][1])] + [tuple(p) for p in sl["section_rz"][1:]] + [(b.R - 5, sl["section_rz"][3][1])]))
    fr = b.pl["collection_frame"]
    ext.append(box(b.R - 5, fr["cz"] - fr["outer_h"] / 2, Rd + fr["bezel_proud_at_axis"], fr["cz"] + fr["outer_h"] / 2))
    S = unary_union(ext)
    L.append(("body_red", "red", S.difference(box(-400, -400, 400, b.black_top))))
    L.append(("base_black", "black", S.intersection(box(-400, -400, 400, b.black_top))))
    cap = b.t["parts"]["cap"]
    for z in [48, 72, 140, cap["soffit_z"], cap["rim_z"][1], cap["dome_base_z"]]:
        r = b.r_at(z)
        L.append(("ring_line", "line", LineString([(-r, z), (r, z)]).buffer(0.9, cap_style=2)))
    L.append(("casting_seam_back", "line", LineString([(-b.R, 150), (-b.R, cap["soffit_z"] - 5)]).buffer(0.6, cap_style=2)))
    return L, (-340, -60, 340, b.H + 30)


def axial_section(b):
    """the plane x = 0, looking from +x: y (front to the right) across, z up. Wall 12 mm; slot open; hood, sill, door and plate frame added."""
    L = []
    sil = b.silhouette()
    inner = sil.buffer(-b.wall, join_style=2)
    wall = sil.difference(inner)
    slot_cut = box(b.R - b.wall - 5, b.slot["z0"], b.R + 40, b.slot["z1"])
    wall = wall.difference(slot_cut)
    hd = b.hood
    wall = unary_union([wall, Polygon([tuple(p) for p in hd["section_rz"]])])
    sl = b.sill
    wall = unary_union([wall, Polygon([tuple(p) for p in sl["section_rz"]])])
    d = b.door
    Rd = b.R + d["proud"]
    wall = unary_union([wall, box(b.R - 2, d["z0"], Rd, d["z1"])])
    plates = []
    fr, pl = b.pl["collection_frame"], b.pl["collection_plate"]
    face = Rd + fr["bezel_proud_at_axis"]
    z0, z1 = fr["cz"] - fr["outer_h"] / 2, fr["cz"] + fr["outer_h"] / 2
    wall = unary_union([wall, box(b.R - 2, z0, face, z1)])
    wz0, wz1 = z0 + fr["bezel"], z1 - fr["bezel"]
    wall = wall.difference(box(face - fr["plate_recess"], wz0, face + 5, wz1))
    plates.append(box(face - fr["plate_recess"] - 2, wz0, face - fr["plate_recess"], wz1))
    interior = inner.intersection(box(-400, -300, 400, b.H + 50))
    L.append(("interior", "cavity", interior))
    L.append(("wall_red", "red", wall.difference(box(-400, -400, 400, b.black_top))))
    L.append(("wall_black", "black", wall.intersection(box(-400, -400, 400, b.black_top))))
    for p in plates:
        L.append(("plate", "white", p))
    fl = b.ap["flap"]
    ap_z1 = b.slot["z1"]
    tilt = math.radians(fl["tilt_deg"])
    hinge_y = b.R - b.wall + 4
    flap = Polygon([(hinge_y, ap_z1 - 2), (hinge_y + fl["thickness"], ap_z1 - 2), (hinge_y + fl["thickness"] + fl["height"] * math.sin(tilt), ap_z1 - 2 - fl["height"] * math.cos(tilt)), (hinge_y + fl["height"] * math.sin(tilt), ap_z1 - 2 - fl["height"] * math.cos(tilt))])
    L.append(("flap", "iron", flap))
    L.append(("footway_line", "line", box(-400, -1.0, 400, 1.0)))
    return L, (-340, -170, 340, b.H + 30)


def sector(ro, ri, ha_deg, n=24):
    ha = math.radians(ha_deg)
    pts = [(ro * math.sin(a), ro * math.cos(a)) for a in [(-ha + 2 * ha * i / n) for i in range(n + 1)]]
    pts += [(ri * math.sin(a), ri * math.cos(a)) for a in [(ha - 2 * ha * i / n) for i in range(n + 1)]]
    return Polygon(pts)


def plan_at(b, z):
    """horizontal section at height z: x right, y up (the front)."""
    L = []
    r = b.r_at(z)
    outer = disc(0, 0, 2 * r, n=96)
    inner = disc(0, 0, 2 * (r - b.wall), n=96) if r > b.wall else Point(0, 0).buffer(0.01)
    wall = outer.difference(inner)
    extras = []
    d = b.door
    Ro = b.R + d["proud"]
    if d["z0"] <= z <= d["z1"]:
        extras.append(("door", "door", sector(Ro, b.R, d["half_angle_deg"])))
        lk = d["lock"]
        if abs(z - lk["z"]) <= lk["escutcheon_diameter"] / 2:
            hw = math.sqrt((lk["escutcheon_diameter"] / 2) ** 2 - (z - lk["z"]) ** 2)
            ang = math.atan2(lk["x"], math.sqrt(Ro ** 2 - lk["x"] ** 2))
            seg = box(-hw, Ro - 2, hw, Ro + lk["proud"])
            seg = affinity.rotate(seg, -math.degrees(ang), origin=(0, 0))
            extras.append(("lock_escutcheon", "pad", seg))
    fr = b.pl["collection_frame"]
    if fr["cz"] - fr["outer_h"] / 2 <= z <= fr["cz"] + fr["outer_h"] / 2:
        face = Ro + fr["bezel_proud_at_axis"]
        hx = fr["outer_w"] / 2
        boss = box(-hx, 0, hx, face).difference(inner)
        extras.append(("collection_frame_boss", "pad", boss))
        wz0, wz1 = fr["cz"] - fr["outer_h"] / 2 + fr["bezel"], fr["cz"] + fr["outer_h"] / 2 - fr["bezel"]
        if wz0 <= z <= wz1:
            whx = hx - fr["bezel"]
            extras.append(("collection_plate_recess", "white", box(-whx, face - fr["plate_recess"] - 2, whx, face - fr["plate_recess"])))
    if b.slot["z0"] <= z <= b.slot["z1"]:
        ha = math.radians(b.slot["half_angle_deg"])
        cut = Polygon([(0, 0)] + [((r + 20) * math.sin(a), (r + 20) * math.cos(a)) for a in [(-ha + 2 * ha * i / 24) for i in range(25)]])
        wall = wall.difference(cut)
        L_extra_hole = ("slot", "cavity", cut.intersection(outer.buffer(5)).difference(inner))
    else:
        L_extra_hole = None
    if b.hood["z0"] <= z <= b.hood["front_top_z"]:
        extras.append(("hood", "red", sector(b.hood["outer_radius"], b.R, b.hood["half_angle_deg"])))
    sl = b.sill["section_rz"]
    if sl[0][1] <= z <= sl[3][1]:
        zb = sl[0][1]; zt = sl[1][1]
        pr = b.sill["projection"] * min(1.0, (z - zb) / max(zt - zb, 1e-6))
        if pr > 0.2:
            extras.append(("sill", "red", sector(b.R + pr, b.R, b.sill["half_angle_deg"])))
    mat = "black" if z <= b.black_top else "red"
    L.append(("interior", "cavity", inner))
    L.append(("wall", mat, wall))
    if L_extra_hole is not None:
        L.append(L_extra_hole)
    for n, m, g in extras:
        L.append((n, m, g))
    return L, (-340, -340, 340, 340)


def plan_levels(b):
    cap = b.t["parts"]["cap"]
    return [("foot", 24), ("door", round(b.door["z0"] + 140)), ("lock", b.door["lock"]["z"]), ("collection_frame", b.pl["collection_frame"]["cz"]),
            ("slot", b.slot["centre_z"]), ("hood", round(b.hood["z0"] + 12)), ("cap_rim", round((cap["rim_z"][0] + cap["rim_z"][1]) / 2)),
            ("dome", round((cap["dome_base_z"] + cap["apex_z"]) / 2))]




# -----------------------------------------------------------------------------------------------------------------
def raster(layers, bounds, mmpp=1.0, flip_x=False, title=None, extra=None):
    x0, z0, x1, z1 = bounds
    W = int(round((x1 - x0) / mmpp)); H = int(round((z1 - z0) / mmpp))
    im = Image.new("RGB", (W, H), (244, 241, 236))
    dr = ImageDraw.Draw(im)
    # grid every 100 mm
    gx = math.ceil(x0 / 100.0) * 100
    while gx <= x1:
        px = (gx - x0) / mmpp
        dr.line([(px, 0), (px, H)], fill=(224, 220, 214) if gx != 0 else (200, 196, 190), width=1)
        gx += 100
    gz = math.ceil(z0 / 100.0) * 100
    while gz <= z1:
        py = (z1 - gz) / mmpp
        dr.line([(0, py), (W, py)], fill=(224, 220, 214), width=1)
        gz += 100

    def pix(p):
        return ((p[0] - x0) / mmpp, (z1 - p[1]) / mmpp)

    for name, mat, geom in layers:
        for p in polys_of(geom):
            dr.polygon([pix(c) for c in p.exterior.coords], fill=COL.get(mat, (128, 128, 128)))
            for h in p.interiors:
                dr.polygon([pix(c) for c in h.coords], fill=(244, 241, 236))
    if extra:
        extra(dr, pix)
    return im


def write_all(t, json_path, pic_dir):
    b = Box(t)
    os.makedirs(pic_dir, exist_ok=True)
    out = {"title": t["title"], "mm_per_px": 1.0, "views": {}}
    font = ImageFont.load_default()

    def label(dr, pix, items):
        for (x, z, s) in items:
            px, py = pix((x, z))
            dr.text((px + 3, py - 10), s, fill=(40, 40, 44), font=font)

    # front elevation
    L, bd = front_elevation(b)
    out["views"]["front_elevation"] = {"bounds_mm": bd, "axes": "x right, z up; z = 0 the footway surface", "polygons": sum([to_json(*l) for l in L], [])}
    def ex(dr, pix):
        dr.line([pix((-340, 0)), pix((340, 0))], fill=(30, 30, 30), width=2)
        label(dr, pix, [(250, 0, "footway z=0"), (250, b.H, f"top {b.H:g}"), (250, b.t["overall"]["aperture_centre_z"], f"slot {b.t['overall']['aperture_centre_z']:g}"),
                        (250, b.black_top, f"black band {b.black_top:g}"), (-330, b.door["z0"], f"door {b.door['z0']:g}"), (-330, b.door["z1"], f"door {b.door['z1']:g}")])
    raster(L, bd, extra=ex).save(os.path.join(pic_dir, "front_elevation.png"))
    # side
    L, bd = side_elevation(b)
    out["views"]["side_elevation"] = {"bounds_mm": bd, "axes": "y across (front to the right), z up", "polygons": sum([to_json(*l) for l in L], [])}
    raster(L, bd, extra=lambda dr, pix: dr.line([pix((-340, 0)), pix((340, 0))], fill=(30, 30, 30), width=2)).save(os.path.join(pic_dir, "side_elevation.png"))
    # axial section
    L, bd = axial_section(b)
    out["views"]["axial_section"] = {"bounds_mm": bd, "axes": "y across (front to the right), z up; plane x = 0", "polygons": sum([to_json(*l) for l in L], [])}
    raster(L, bd, extra=lambda dr, pix: dr.line([pix((-340, 0)), pix((340, 0))], fill=(30, 30, 30), width=2)).save(os.path.join(pic_dir, "axial_section.png"))
    # plans
    tiles = []
    out["views"]["plans"] = {}
    for name, z in plan_levels(b):
        L, bd = plan_at(b, z)
        out["views"]["plans"][name] = {"z_mm": z, "bounds_mm": bd, "axes": "x right, y up (the front is up the page)", "polygons": sum([to_json(*l) for l in L], [])}
        im = raster(L, bd, extra=lambda dr, pix, n=name, z=z: dr.text((8, 8), f"plan at z={z}  ({n})", fill=(30, 30, 30), font=font))
        tiles.append(im)
    cols = 4
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (tiles[0].width * cols, tiles[0].height * rows), (244, 241, 236))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * im.width, (i // cols) * im.height))
    sheet.save(os.path.join(pic_dir, "plans.png"))
    os.makedirs(os.path.dirname(os.path.abspath(json_path)) or ".", exist_ok=True)
    json.dump(out, open(json_path, "w"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "target.json"))
    ap.add_argument("--json", required=True)
    ap.add_argument("--pics", required=True)
    a = ap.parse_args()
    out = write_all(load(a.target), a.json, a.pics)
    n = sum(len(v["polygons"]) for k, v in out["views"].items() if k != "plans") + sum(len(p["polygons"]) for p in out["views"]["plans"].values())
    print("wrote", a.json, "and pictures in", a.pics, "-", n, "polygons")


if __name__ == "__main__":
    main()
