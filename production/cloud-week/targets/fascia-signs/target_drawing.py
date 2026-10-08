"""Draws the fascia targets from target.json ALONE (no font, no photograph, no other file).

    /home/user/.bpyenv/bin/python target_drawing.py OUTDIR [--json drawing.json] [--sheet]

For every shop: the board (5410 x 550 mm) at ONE MILLIMETRE A PIXEL, y up in the data and the picture
upright, with the frame, the lettered field, the safe zone, each text block's ink box (and its
effects box: shade, outline, hand jitter), its baseline and its cap line, the border shapes in their
colours, and the painted-out patch on the empty unit. Also: the four projecting signs in side
elevation (millimetres, one a pixel), and the photo template (the ratios measured on P1 laid out as
a board). Everything is also written as filled polygons in millimetres into the JSON file.

Pictures go to OUTDIR (never into git unless OUTDIR is under production/previews/).
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw
from shapely.geometry import LineString, Point, box as sbox
from shapely.geometry import mapping

HERE = Path(__file__).resolve().parent
TJ = HERE / "target.json"


def load(path=TJ):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def col(T, key, which="srgb_1990"):
    return tuple(T["palette"][key][which])


def poly_from_box(b):
    x0, y0, x1, y1 = b
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def stroke_poly(pts, width):
    """The stroke as a filled polygon (with holes if the line closes on itself): {'poly': exterior, 'holes': [...]}"""
    g = LineString([tuple(p) for p in pts]).buffer(width / 2.0, cap_style=2, join_style=2)
    r = lambda ring: [[round(v, 2) for v in q] for q in ring.coords]
    return dict(poly=r(g.exterior), holes=[r(h) for h in g.interiors])


def cutcorner_pts(x0, y0, x1, y1, r, n=10):
    """Closed polyline of a rectangle whose four corners are cut by concave quarter circles centred on the corners (P1's keyline)."""
    pts = []

    def arc(cx, cy, a0, a1):
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append([round(cx + r * math.cos(a), 2), round(cy + r * math.sin(a), 2)])

    arc(x1, y0, 180, 90)
    arc(x1, y1, 270, 180)
    arc(x0, y1, 360, 270)
    arc(x0, y0, 90, 0)
    pts.append(pts[0])
    return pts


def circle_poly(c, r, n=48):
    return [[round(c[0] + r * math.cos(2 * math.pi * i / n), 2), round(c[1] + r * math.sin(2 * math.pi * i / n), 2)] for i in range(n)]


# --------------------------------------------------------------------------------------------
# data: one board
# --------------------------------------------------------------------------------------------
def board_data(T, s):
    B = T["board"]
    W, H = B["width_mm"], B["height_mm"]
    ground = s["ground"]["colour"]
    d = dict(id=s["id"], size_mm=[W, H], ground=ground, ground_srgb=list(col(T, ground)), layers=[], text=[])
    L = d["layers"]
    bd = s.get("border") or {}
    L.append(dict(role="board", kind="fill", colour=list(col(T, ground)), poly=poly_from_box([0, 0, W, H])))
    if bd.get("kind") == "box":
        # a box sign: old painted board (cream, chalked) shows round it; the face is the box
        L[0]["colour"] = list(col(T, "cream"))
    if bd.get("kind") == "glass_slab":
        L[0]["colour"] = list(col(T, "bare_timber"))
    L.append(dict(role="frame", kind="outline", poly=poly_from_box([0, 0, W, H]), inner=poly_from_box(B["field_mm"])))
    L.append(dict(role="field", kind="outline", poly=poly_from_box(B["field_mm"])))
    L.append(dict(role="safe", kind="outline", poly=poly_from_box(B["safe_mm"])))
    for sh in s.get("shapes", []):
        c = list(col(T, sh["colour"])) if sh.get("colour") else None
        if sh["kind"] == "rect":
            L.append(dict(role=sh["role"], kind="fill", colour=c, poly=poly_from_box(sh["box"])))
        elif sh["kind"] == "polyline":
            sp = stroke_poly(sh["pts"], sh["width_mm"])
            L.append(dict(role=sh["role"], kind="stroke", colour=c, poly=sp["poly"], holes=sp["holes"], width_mm=sh["width_mm"], centreline=sh["pts"]))
        elif sh["kind"] == "circle":
            L.append(dict(role=sh["role"], kind="fill", colour=c, poly=circle_poly(sh["c"], sh["r"]), outline_only=True))
    g = s.get("ghost")
    if g:
        L.append(dict(role="ghost_" + g["kind"], kind="hatch", box=g["box_mm"], poly=poly_from_box(g["box_mm"]),
                      colour=list(col(T, "painted_out")) if g["kind"] == "painted_out_patch" else None))
    for p in T.get("small_panels", []):
        if p.get("id") == "letting_board" and p["shop"] == s["id"]:
            cx, cy = p["centre_on_board_mm"]
            w, h = p["size_mm"]
            L.append(dict(role="letting_board", kind="fill", colour=[236, 234, 226], poly=poly_from_box([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]), text=p["text"], cap_mm=p["cap_mm"]))
    for b in s["blocks"]:
        x0, y0, x1, y1 = b["ink_box_mm"]
        d["text"].append(dict(
            id=b["id"], text=b["text"], font=b["font"], weight=b["weight"], cap_mm=b["cap_mm"], role=b["role"], technique=b["technique"],
            ink_box=poly_from_box(b["ink_box_mm"]), effects_box=poly_from_box(b["effects_box_mm"]),
            baseline=[[x0, b["baseline_mm"]], [x1, b["baseline_mm"]]], cap_line=[[x0, b["baseline_mm"] + b["cap_mm"]], [x1, b["baseline_mm"] + b["cap_mm"]]],
            face=list(col(T, b["face"])), shade=(list(col(T, b["shade"]["colour"])) if b["shade"] else None), shade_d_mm=(b["shade"]["d_mm"] if b["shade"] else 0)))
    return d


# --------------------------------------------------------------------------------------------
# data: projecting signs, side elevation (x out from the wall face, y up from the footway; mm)
# --------------------------------------------------------------------------------------------
def projecting_data(T, p):
    m = p["mount"]
    proj = m["projection_m"] * 1000
    ah = m["arm_height_m"] * 1000
    out = dict(id=p["id"], shop=p["shop"], layers=[])
    L = out["layers"]
    L.append(dict(role="wall_face", poly=[[0, 0], [0, 4200], [-40, 4200], [-40, 0]]))
    L.append(dict(role="plate", poly=poly_from_box([0, ah - 150, 18, ah + 150])))
    L.append(dict(role="arm", poly=poly_from_box([0, ah - 10, proj, ah + 10])))
    pa = p["parts"]
    if "balls" in pa:
        r = pa["balls"]["diameter_m"] * 500
        for c in pa["balls"]["centres_m"]:
            L.append(dict(role="ball", poly=circle_poly([c[0] * 1000, c[1] * 1000], r), c=[c[0] * 1000, c[1] * 1000], r=r))
        L.append(dict(role="hanger", poly=poly_from_box([pa["balls"]["centres_m"][0][0] * 1000 - 5, 2900, pa["balls"]["centres_m"][0][0] * 1000 + 5, ah])))
    if "box_m" in pa and p["id"] == "steam_laundry_box":
        w, h, t = [v * 1000 for v in pa["box_m"]]
        L.append(dict(role="box", poly=poly_from_box([0, ah - h, w, ah]), thickness_mm=t))
    if "board_m" in pa:
        w, h, t = [v * 1000 for v in pa["board_m"]]
        x0 = proj - w - 40
        L.append(dict(role="board", poly=poly_from_box([x0, ah - 60 - h, x0 + w, ah - 60]), thickness_mm=t))
    out["clearance_below_m"] = p.get("clearance_below_m")
    return out


# --------------------------------------------------------------------------------------------
# the photo template: P1's ratios as a board (field 502 mm high, as ours)
# --------------------------------------------------------------------------------------------
def template_data(T):
    R = T["photo_template"]["ratios"]
    fh = T["board"]["field_mm"][3] - T["board"]["field_mm"][1]
    fw = R["field_width_over_height"] * fh
    out = dict(id="photo_template", field_mm=[0, 0, fw, fh], layers=[], text=[])
    k = R["keyline_thickness"] * fh
    top = fh - R["keyline_top_inset"] * fh          # y of keyline centre, y up
    bot = R["keyline_bottom_inset"] * fh
    side = R["keyline_side_inset"] * fh
    out["keyline_top_y"] = round(top, 2)
    out["keyline_bottom_y"] = round(bot, 2)
    out["keyline_left_x"] = round(side, 2)
    out["keyline_right_x"] = round(fw - side, 2)
    out["layers"].append(dict(role="field", poly=poly_from_box([0, 0, fw, fh])))
    cl = cutcorner_pts(side, bot, fw - side, top, R["corner_radius"] * fh)
    sp = stroke_poly(cl, k)
    out["layers"].append(dict(role="keyline", width_mm=round(k, 2), centreline=cl, poly=sp["poly"], holes=sp["holes"]))
    cap = R["cap_over_field"] * fh
    cc = fh - R["cap_centre_over_field"] * fh      # y of the cap band's centre
    base = cc - cap / 2
    w = R["name_width_over_cap"] * cap
    cx = fw / 2 + R.get("name_centre_offset_over_panel", 0.0) * (fw - 2 * side)
    nm = dict(role="name", cap_mm=round(cap, 2), baseline_y=round(base, 2), cap_y=round(base + cap, 2), x0=round(cx - w / 2, 2), x1=round(cx + w / 2, 2))
    out["text"].append(nm)
    nh = R["numeral_over_cap"] * cap
    out["text"].append(dict(role="numeral_l", height_mm=round(nh, 2), x0=round(side + 25 / 147.0 * fh, 2)))
    out["shade_mm"] = round(R["shade_over_cap"] * cap, 2)
    return out


# --------------------------------------------------------------------------------------------
# pictures
# --------------------------------------------------------------------------------------------
def draw_board_png(T, d, path, scale=1):
    W, H = d["size_mm"]
    im = Image.new("RGB", (W * scale, H * scale), (40, 40, 40))
    dr = ImageDraw.Draw(im)

    def P(pt):
        return (pt[0] * scale, (H - pt[1]) * scale)

    for L in d["layers"]:
        r = L["role"]
        if L["kind"] == "fill" and L.get("colour") is not None:
            if L.get("outline_only"):
                dr.polygon([P(p) for p in L["poly"]], outline=tuple(L["colour"]), width=3)
            else:
                dr.polygon([P(p) for p in L["poly"]], fill=tuple(L["colour"]))
        elif L["kind"] == "stroke":
            pts = [P(p) for p in L["centreline"]]
            dr.line(pts, fill=tuple(L["colour"]), width=max(1, int(round(L["width_mm"] * scale))), joint="curve")
        elif r == "frame":
            dr.polygon([P(p) for p in L["inner"]], outline=(255, 255, 255), width=1)
        elif r == "field":
            pass
        elif r == "safe":
            xs = [p[0] for p in L["poly"]]
            ys = [p[1] for p in L["poly"]]
            x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
            for x in range(int(x0), int(x1), 24):
                dr.line([P((x, y0)), P((min(x + 12, x1), y0))], fill=(0, 220, 220), width=1)
                dr.line([P((x, y1)), P((min(x + 12, x1), y1))], fill=(0, 220, 220), width=1)
            for y in range(int(y0), int(y1), 24):
                dr.line([P((x0, y)), P((x0, min(y + 12, y1)))], fill=(0, 220, 220), width=1)
                dr.line([P((x1, y)), P((x1, min(y + 12, y1)))], fill=(0, 220, 220), width=1)
        elif L["kind"] == "hatch":
            b = L["box"]
            if L.get("colour"):
                dr.rectangle([P((b[0], b[3])), P((b[2], b[1]))], fill=tuple(int(v * 0.9) for v in L["colour"]))
            xs0, ys0, xs1, ys1 = b
            step = 30
            for k in range(int(xs0 - (ys1 - ys0)), int(xs1), step):
                a = (max(xs0, k), ys0 + max(0, xs0 - k))
                c = (min(xs1, k + (ys1 - ys0)), ys0 + min(ys1 - ys0, xs1 - k))
                if a[0] < c[0]:
                    dr.line([P(a), P(c)], fill=(255, 255, 255), width=1)
            dr.rectangle([P((b[0], b[3])), P((b[2], b[1]))], outline=(255, 140, 0), width=2)
    for t in d["text"]:
        b = t["ink_box"]
        xs = [p[0] for p in b]
        ys = [p[1] for p in b]
        e = t["effects_box"]
        exs = [p[0] for p in e]
        eys = [p[1] for p in e]
        if t["shade"]:
            dr.rectangle([P((min(exs), max(eys))), P((max(exs), min(eys)))], outline=tuple(t["shade"]) if sum(t["shade"]) > 90 else (140, 140, 140), width=1)
        dr.rectangle([P((min(xs), max(ys))), P((max(xs), min(ys)))], outline=tuple(t["face"]), width=2)
        dr.line([P(t["baseline"][0]), P(t["baseline"][1])], fill=(255, 0, 255), width=2)
        dr.line([P(t["cap_line"][0]), P(t["cap_line"][1])], fill=(255, 255, 0), width=1)
        dr.text(P((min(xs) + 6, max(ys) - 4)), f'{t["text"]}  cap {t["cap_mm"]:g} mm  {t["font"]}', fill=(255, 255, 255))
    im.save(path)
    return im.size


def draw_projecting_png(p, path, scale=1):
    xs = [pt[0] for L in p["layers"] for pt in L["poly"]]
    ys = [pt[1] for L in p["layers"] for pt in L["poly"]]
    x0, x1, y0, y1 = min(xs) - 60, max(xs) + 60, min(ys) - 60, max(ys) + 60
    W, H = int((x1 - x0) * scale), int((y1 - y0) * scale)
    im = Image.new("RGB", (W, H), (222, 220, 214))
    dr = ImageDraw.Draw(im)

    def P(pt):
        return ((pt[0] - x0) * scale, (y1 - pt[1]) * scale)

    colours = dict(wall_face=(120, 80, 70), plate=(40, 40, 40), arm=(30, 30, 30), hanger=(30, 30, 30), ball=(190, 150, 70), box=(236, 236, 228), board=(90, 90, 110))
    for L in p["layers"]:
        dr.polygon([P(q) for q in L["poly"]], fill=colours.get(L["role"], (128, 128, 128)), outline=(0, 0, 0))
    im.save(path)
    return im.size


def draw_sheet(T, outdir, ids_sizes, path, width=1200):
    """All ten boards stacked, in street order, at a reduced scale (for the previews)."""
    ims = []
    for sid, p in ids_sizes:
        ims.append((sid, Image.open(p)))
    k = width / ims[0][1].size[0]
    hh = int(ims[0][1].size[1] * k) + 14
    sheet = Image.new("RGB", (width, hh * len(ims)), (24, 24, 24))
    dr = ImageDraw.Draw(sheet)
    for i, (sid, im) in enumerate(ims):
        t = im.resize((width, int(im.size[1] * k)), Image.LANCZOS)
        sheet.paste(t, (0, i * hh + 12))
        dr.text((4, i * hh + 1), sid, fill=(255, 255, 255))
    sheet.save(path, quality=88)


def main(argv):
    outdir = Path(argv[1]) if len(argv) > 1 and not argv[1].startswith("--") else Path("drawings")
    outdir.mkdir(parents=True, exist_ok=True)
    jpath = None
    if "--json" in argv:
        jpath = Path(argv[argv.index("--json") + 1])
    T = load()
    out = dict(units="mm", y_up=True, px_per_mm=1, boards={}, projecting={}, template=None)
    pics = []
    for s in T["shops"]:
        d = board_data(T, s)
        out["boards"][s["id"]] = d
        p = outdir / f'board-{s["order"]:02d}-{s["id"]}.png'
        draw_board_png(T, d, p)
        pics.append((s["id"], p))
    for pr in T["projecting_signs"]:
        d = projecting_data(T, pr)
        out["projecting"][pr["id"]] = d
        draw_projecting_png(d, outdir / f'projecting-{pr["id"]}.png')
    out["template"] = template_data(T)
    if "--sheet" in argv:
        draw_sheet(T, outdir, pics, outdir / "layout-sheet.jpg")
    if jpath:
        jpath.parent.mkdir(parents=True, exist_ok=True)
        jpath.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"drew {len(pics)} boards and {len(out['projecting'])} projecting signs into {outdir}" + (f"; polygons in {jpath}" if jpath else ""))
    return out


if __name__ == "__main__":
    main(sys.argv)
