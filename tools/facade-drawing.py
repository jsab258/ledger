#!/usr/bin/env python3
"""A terrace facade as a dimensioned front elevation, drawn from the spec's numbers.

    python tools/facade-drawing.py --block east_parade --out DIR
    python tools/facade-drawing.py --selftest

WHY IT EXISTS, 24 September. Jafar's measurement sitting takes three facades
"from dimensioned drawing to accepted pair", and no dimensioned drawing of any
facade existed: the geometry was numbers in production/specs/vignette-scene.json,
turned into parts by tools/art-recipes/terrace-front.py. This draws those parts
flat, as seen from the street, with dimension chains in millimetres, so the
design is checked against the photographs BEFORE anything is built, and the
built facade has a drawing to be paired against after.

WHERE THE NUMBERS COME FROM. The recipe's own --plan (plain Python, no Blender)
prints every part it would build with its extents; this reads that and nothing
else, so the drawing and the build can never be two opinions of one facade. A
number changed after checking the photographs is changed in the spec, and the
drawing is drawn again.

AS SEEN FROM THE STREET. The east side is seen looking east, so north is on the
left and the block's first bay is on the RIGHT; the west side is seen looking
west, first bay on the left. Unreal's elevation shot looks the same way.

WRITES <block>-drawing.png and <block>-drawing.json (scale, origin, and every
dimensioned edge, which tools/facade-pair.py lays over the Unreal frame).
Curved parts (the arched heads) are listed as not drawn rather than guessed.
"""
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECIPE = os.path.join(ROOT, "tools", "art-recipes", "terrace-front.py")
SCENE = os.path.join(ROOT, "production", "specs", "vignette-scene.json")
PX_PER_M = 80
MARGIN = (260, 170, 120, 220)  # left, top, right, bottom, in px

#: Flat colours, one per material, only so parts can be told apart on paper.
COLOURS = {
    "brick_red": (156, 78, 58), "brick_grey": (118, 104, 98), "brick_rubbed": (176, 96, 70),
    "glass": (84, 104, 116), "glass_whitened": (200, 204, 204), "interior": (52, 50, 48),
    "interior_lit": (120, 110, 84), "frame_painted": (64, 74, 96), "frame_metal": (150, 154, 158),
    "paint_fascia": (70, 86, 112), "paint_joinery": (236, 234, 226), "paint_door": (48, 80, 64),
    "paint_stall": (90, 90, 96), "tile_patterned": (214, 206, 180), "tile_stall": (190, 186, 170),
    "slate": (86, 90, 100), "stone": (206, 200, 188), "lead": (110, 112, 118),
    "steel_dark": (60, 62, 66), "concrete": (170, 168, 160),
}

PART = re.compile(r"^tfPart id=(\S+) material=(\S+) kind=(\S+)(.*)$")
RANGE = re.compile(r"(xM|yM|zM)=(-?[\d.]+)\.\.(-?[\d.]+)")
BAY = re.compile(r"^tfBay (.*)$")


def parse_plan(text):
    """Parts with extents, the parts not drawn, and the bay line's numbers."""
    parts, skipped, bay = [], [], {}
    for line in text.splitlines():
        m = PART.match(line.strip())
        if m:
            pid, mat, kind, rest = m.groups()
            r = {k: (float(a), float(b)) for k, a, b in RANGE.findall(rest)}
            if kind == "box" and len(r) == 3:
                parts.append({"id": pid, "material": mat, "x": r["xM"], "y": r["yM"], "z": r["zM"]})
            else:
                skipped.append(pid)
            continue
        m = BAY.match(line.strip())
        if m:
            for kv in m.group(1).split():
                k, _, v = kv.partition("=")
                try:
                    bay[k] = float(v)
                except ValueError:
                    pass
    return parts, skipped, bay


def run_plan(block):
    out = subprocess.run([sys.executable, RECIPE, "--plan", "--block", block],
                         capture_output=True, text=True, timeout=120, cwd=ROOT)
    return out.stdout


def edges(parts, bay_index, ids):
    """The distinct x and z edges of the named parts in one bay, sorted."""
    xs, zs = set(), set()
    for p in parts:
        base = re.sub(r"_bay\d+$", "", p["id"])
        if not p["id"].endswith("_bay%d" % bay_index) or not any(base.startswith(i) for i in ids):
            continue
        xs.update(round(v, 3) for v in p["x"])
        zs.update(round(v, 3) for v in p["z"])
    return sorted(xs), sorted(zs)


def plan_drawing(block_id, plan_text, scene):
    blk = next(b for b in scene["blocks"] if b["id"] == block_id)
    parts, skipped, bay = parse_plan(plan_text)
    width = blk["bays"] * blk["bay_width_m"]
    top = max([p["z"][1] for p in parts] + [bay.get("ridgeM", 0.0)])
    mirror = blk["side"] == "east"
    gx, _ = edges(parts, 0, ("pilaster", "shop_door_leaf", "side_door_leaf", "display_glazing",
                             "gf_pier", "front_door"))
    ux, _ = edges(parts, 0, ("upper_glass", "upper_net"))
    _, gz = edges(parts, 0, ("pilaster", "shop_door_leaf", "side_door_leaf", "display_glazing",
                             "stallriser", "transom_bar", "fascia_band", "upper_glass", "parapet",
                             "coping", "gf_band_above"))
    levels = sorted(set([0.0] + [z for z in gz if z > 0.0] + [bay.get("groundFloorM", 0.0),
                    bay.get("eavesM", 0.0), bay.get("ridgeM", 0.0)]))
    return {
        "block": block_id, "side": blk["side"], "mirror": mirror, "width_m": width,
        "top_m": top, "bays": blk["bays"], "bay_width_m": blk["bay_width_m"],
        "px_per_m": PX_PER_M, "parts": parts, "not_drawn": skipped, "bay": bay,
        "x_edges_bay0": sorted(set([0.0, blk["bay_width_m"]] + [x for x in gx if 0.0 <= x <= blk["bay_width_m"]])),
        "x_edges_upper_bay0": sorted(set([0.0, blk["bay_width_m"]] + [x for x in ux if 0.0 <= x <= blk["bay_width_m"]])),
        "z_levels": [z for z in levels if z <= top + 1e-6],
        "roof": blk["roof"]["kind"],
    }


def to_px(d, x, z):
    """Block-local metres to drawing pixels, as seen from the street."""
    xx = (d["width_m"] - x) if d["mirror"] else x
    return (MARGIN[0] + xx * d["px_per_m"], MARGIN[1] + (d["top_m"] - z) * d["px_per_m"])


def render(d, out_png):
    from PIL import Image, ImageDraw, ImageFont
    s = d["px_per_m"]
    W = int(MARGIN[0] + d["width_m"] * s + MARGIN[2])
    H = int(MARGIN[1] + d["top_m"] * s + MARGIN[3])
    im = Image.new("RGB", (W, H), (250, 248, 242))
    g = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("arial.ttf", 15)
        big = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        f = big = ImageFont.load_default()
    ink = (30, 30, 34)
    # The pitched roof's front slope, seen square on, is a band from the eaves
    # to the ridge; the plan gives it as a slope with no box extents.
    if d["roof"] == "pitched" and d["bay"].get("ridgeM"):
        a = to_px(d, 0.0, d["bay"]["ridgeM"]); b = to_px(d, d["width_m"], d["bay"]["eavesM"])
        g.rectangle([min(a[0], b[0]), a[1], max(a[0], b[0]), b[1]], fill=COLOURS["slate"], outline=ink)
    # What stands back from the frontage (a stack on the ridge) shows only
    # above the roof or parapet in front of it.
    front_top = max([p["z"][1] for p in d["parts"] if p["y"][0] <= 0.5] +
                    [d["bay"].get("ridgeM", 0.0) if d["roof"] == "pitched" else 0.0])
    # Far parts first, so what stands proud of the frontage is drawn over them.
    for p in sorted(d["parts"], key=lambda p: -p["y"][0]):
        z0 = p["z"][0]
        if p["y"][0] > 0.5:
            if p["z"][1] <= front_top + 0.01:
                continue  # the carcass behind the rooms is not part of the front
            z0 = max(z0, front_top)
        a = to_px(d, p["x"][0], p["z"][1]); b = to_px(d, p["x"][1], z0)
        box = [min(a[0], b[0]), a[1], max(a[0], b[0]), b[1]]
        if box[2] - box[0] < 1 or box[3] - box[1] < 1:
            continue
        g.rectangle(box, fill=COLOURS.get(p["material"], (160, 160, 160)), outline=ink)
    ground = to_px(d, 0.0, 0.0)[1]
    g.line([(MARGIN[0] - 40, ground), (MARGIN[0] + d["width_m"] * s + 40, ground)], fill=ink, width=3)

    def hdim(x0, x1, y, label_above=True):
        p0 = to_px(d, x0, 0)[0]; p1 = to_px(d, x1, 0)[0]
        l, r = min(p0, p1), max(p0, p1)
        g.line([(l, y), (r, y)], fill=ink, width=1)
        for q in (l, r):
            g.line([(q, y - 7), (q, y + 7)], fill=ink, width=1)
        t = "%d" % round(abs(x1 - x0) * 1000)
        tw = g.textlength(t, font=f)
        if r - l > tw + 4:
            g.text(((l + r - tw) / 2, y - 20 if label_above else y + 4), t, fill=ink, font=f)

    # Chains along the bottom: the whole block, each bay, and bay 0's openings.
    y1 = ground + 40; y2 = ground + 90; y3 = ground + 140
    hdim(0.0, d["width_m"], y3)
    for i in range(d["bays"]):
        hdim(i * d["bay_width_m"], (i + 1) * d["bay_width_m"], y2)
    xe = d["x_edges_bay0"]
    for a, b in zip(xe, xe[1:]):
        hdim(a, b, y1)
    # The upper windows' chain goes above the roofline, where nothing else is.
    ue = d["x_edges_upper_bay0"]
    yu = MARGIN[1] - 24
    for a, b in zip(ue, ue[1:]):
        hdim(a, b, yu)
    # And the levels up the side, each from the pavement, as a builder reads them.
    side_x = MARGIN[0] - 60 if not d["mirror"] else MARGIN[0] + d["width_m"] * s + 30
    for z in d["z_levels"]:
        py = to_px(d, 0, z)[1]
        g.line([(side_x - 6, py), (side_x + 6, py)], fill=ink, width=1)
        g.text((side_x - 58 if not d["mirror"] else side_x + 10, py - 8), "%d" % round(z * 1000), fill=ink, font=f)
    g.line([(side_x, to_px(d, 0, d["z_levels"][-1])[1]), (side_x, ground)], fill=ink, width=1)
    g.text((MARGIN[0], 24), "%s - front elevation, as seen from the street (%s side)" % (d["block"], d["side"]),
           fill=ink, font=big)
    g.text((MARGIN[0], 56), "millimetres; levels from the pavement; drawn from the recipe's plan of "
           "production/specs/vignette-scene.json; 1 m = %d px" % s, fill=ink, font=f)
    if d["not_drawn"]:
        g.text((MARGIN[0], 78), "not drawn (curved): %d parts, e.g. %s" % (len(d["not_drawn"]), d["not_drawn"][0]),
               fill=ink, font=f)
    im.save(out_png)
    origin = to_px(d, 0.0, 0.0)
    return {"png": os.path.basename(out_png), "size_px": [W, H], "origin_px": list(origin),
            "x_axis": "block-local x runs %s on the drawing" % ("right-to-left" if d["mirror"] else "left-to-right")}


def main(argv):
    if "--selftest" in argv:
        return selftest()
    block = argv[argv.index("--block") + 1] if "--block" in argv else "east_parade"
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(ROOT, "production", "art", "facades")
    os.makedirs(out, exist_ok=True)
    scene = json.load(open(SCENE, encoding="utf-8"))
    d = plan_drawing(block, run_plan(block), scene)
    if not d["parts"]:
        print("facadeDrawing status=NO-PARTS block=%s (the recipe's --plan printed none)" % block)
        return 1
    png = os.path.join(out, "%s-drawing.png" % block)
    meta = render(d, png)
    side = {k: d[k] for k in ("block", "side", "mirror", "width_m", "top_m", "bays", "bay_width_m",
                              "px_per_m", "x_edges_bay0", "x_edges_upper_bay0", "z_levels", "not_drawn", "bay")}
    side.update(meta)
    json.dump(side, open(os.path.join(out, "%s-drawing.json" % block), "w", encoding="utf-8"), indent=1)
    print("facadeDrawing status=DRAWN block=%s parts=%d notDrawn=%d widthM=%.3f topM=%.3f png=%s"
          % (block, len(d["parts"]), len(d["not_drawn"]), d["width_m"], d["top_m"], png))
    return 0


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("facade-drawing selftest FAIL " + name)
    plan = ("tfBay widthM=6.000 eavesM=6.200 ridgeM=9.001 groundFloorM=3.400\n"
            "tfPart id=pilaster_left_bay0 material=frame_painted kind=box xM=0.000..0.350 yM=-0.1000..0.0000 zM=0.000..3.400 note=x\n"
            "tfPart id=side_door_leaf_bay0 material=paint_door kind=box xM=0.386..1.152 yM=0.1200..0.1600 zM=0.000..1.981 note=x\n"
            "tfPart id=upper_arch_0_bay0 material=brick_rubbed kind=mesh verts=44 faces=24\n")
    parts, skipped, bay = parse_plan(plan)
    check("two boxes read", len(parts) == 2)
    check("the curved part is listed, not drawn", skipped == ["upper_arch_0_bay0"])
    check("the bay line is read", abs(bay.get("ridgeM", 0) - 9.001) < 1e-9)
    xs, zs = edges(parts, 0, ("pilaster", "side_door_leaf"))
    check("bay 0 edges", xs == [0.0, 0.35, 0.386, 1.152] and 1.981 in zs)
    check("the chain closes on the bay's own width", plan_drawing("b", plan, {"blocks": [{"id": "b", "side": "west", "bays": 1, "bay_width_m": 6.0, "roof": {"kind": "pitched"}}]})["x_edges_bay0"][-1] == 6.0)
    scene = {"blocks": [{"id": "b", "side": "east", "bays": 2, "bay_width_m": 6.0, "roof": {"kind": "pitched"}}]}
    d = plan_drawing("b", plan, scene)
    check("the east side is drawn mirrored", d["mirror"] and to_px(d, 0.0, 0.0)[0] > to_px(d, 12.0, 0.0)[0])
    check("the ridge sets the top", abs(d["top_m"] - 9.001) < 1e-9)
    print("facade-drawing selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
