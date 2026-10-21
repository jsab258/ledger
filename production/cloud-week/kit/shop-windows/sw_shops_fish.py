"""The fishmonger (east_parade bay 1, "fish_market", FISH MARKET): the room's layout and the window display (14 October 2026, batch B). Read from `shops.fish_market.room` and `.display` in target.json; every
choice the target left open is stated in the docstrings (each a Judgement in NOTES.md and a `Changes after the build` line).

THE FISH ARE PENDING. The cod, mackerel, herring, plaice, crab and prawns of the target are Sketchfab scans (ffishAsia, CC0) whose download needs Jafar's login (his Needs-you item 3): nothing is hand-made in their
place (the 3 October failure). The trays of the room's chiller and the slab of the window carry ice, lemons and tickets only, and say so.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import sw_assets as A
import sw_gen as GEN
import sw_goods_b as GB
from sw_gen import GM

rgb8 = None

TIN_DESIGNS = [("SALTHOUSE", "PILCHARDS", "in tomato sauce", (196, 70, 48), (250, 240, 206), (250, 240, 206)),
               ("SALTHOUSE", "PINK SALMON", "", (212, 102, 92), (255, 246, 232), (255, 246, 232)),
               ("TIDEMARK", "SARDINES", "in oil", (44, 84, 142), (244, 238, 220), (240, 200, 84)),
               ("TIDEMARK", "KIPPER FILLETS", "", (150, 90, 44), (250, 238, 206), (250, 238, 206)),
               ("FENWICK", "HERRING FILLETS", "in tomato sauce", (170, 56, 44), (250, 240, 212), (250, 240, 212)),
               ("FENWICK", "SMOKED MUSSELS", "", (60, 78, 100), (240, 236, 220), (240, 200, 84)),
               ("BRIGHTWATER", "WHITE CRAB MEAT", "", (236, 232, 214), (150, 40, 40), (150, 40, 40)),
               ("BRIGHTWATER", "SHRIMPS", "in brine", (210, 120, 90), (255, 246, 232), (255, 246, 232))]
JAR_DESIGNS = [("CRAB PASTE", "SALTHOUSE", (206, 120, 100), (170, 90, 76)), ("SHRIMP PASTE", "SALTHOUSE", (200, 150, 130), (160, 110, 94)), ("ANCHOVY PASTE", "TIDEMARK", (150, 90, 70), (110, 60, 46)),
               ("PICKLED HERRING", "FENWICK", (216, 206, 180), (180, 170, 140)), ("SALMON PASTE", "BRIGHTWATER", (220, 140, 120), (180, 100, 84))]


def _setup():
    global rgb8
    import sw_room as S
    rgb8 = S.rgb8


def _chalk_board(path):
    """The blackboard price list: chalk numerals and the four fish of the target only (COD, HADDOCK, PLAICE, KIPPERS), a chalk underline, a border."""
    from sw_gen import font
    W, H = 640, 480
    rnd = random.Random(3)
    im = Image.new("RGB", (W, H), (36, 44, 40))
    d = ImageDraw.Draw(im)
    arr = np.asarray(im, np.float32)
    arr = arr + np.random.default_rng(2).normal(0, 4, arr.shape)
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(im)
    f = font("patrick-hand", 54)
    f2 = font("patrick-hand", 46)
    chalk = (232, 230, 218)
    d.text((W / 2 - d.textlength("TODAY'S FISH", font=f) / 2, 26), "TODAY'S FISH", font=f, fill=chalk)
    d.line([(60, 96), (W - 60, 96)], fill=chalk, width=3)
    for k, (nm, pr) in enumerate((("COD", "2.60 lb"), ("HADDOCK", "2.45 lb"), ("PLAICE", "2.90 lb"), ("KIPPERS", "1.80 lb"))):
        y = 120 + k * 80 + rnd.randint(-3, 3)
        d.text((70, y), nm, font=f2, fill=chalk)
        d.text((W - 70 - d.textlength(pr, font=f2), y), pr, font=f2, fill=chalk)
        d.line([(70, y + 62), (W - 70, y + 62)], fill=(150, 150, 140), width=1)
    d.rectangle([14, 14, W - 15, H - 15], outline=(180, 180, 170), width=2)
    im.save(path)
    GEN.TEXTS.extend(["TODAY'S FISH", "COD", "2.60 lb", "HADDOCK", "2.45 lb", "PLAICE", "2.90 lb", "KIPPERS", "1.80 lb"])


def _weights_chart(path):
    """A hanging scale's chart: a printed card with a table of pounds and ounces against the price per lb (arithmetic only: no fish, no firm)."""
    from sw_gen import font
    W, H = 360, 500
    im = Image.new("RGB", (W, H), (232, 226, 206))
    d = ImageDraw.Draw(im)
    f = font("alfa-slab-one", 32)
    d.text((W / 2 - d.textlength("PRICE CHART", font=f) / 2, 14), "PRICE CHART", font=f, fill=(30, 50, 110))
    fs = font("oswald", 24)
    d.text((24, 66), "OZ", font=fs, fill=(150, 40, 40))
    d.text((120, 66), "AT 1.80", font=fs, fill=(150, 40, 40))
    d.text((250, 66), "AT 2.60", font=fs, fill=(150, 40, 40))
    for i, oz in enumerate((4, 8, 12, 16, 24, 32, 48)):
        y = 104 + i * 52
        d.text((24, y), str(oz), font=fs, fill=(40, 40, 60))
        d.text((120, y), "%.2f" % (1.80 * oz / 16.0), font=fs, fill=(40, 40, 60))
        d.text((250, y), "%.2f" % (2.60 * oz / 16.0), font=fs, fill=(40, 40, 60))
        d.line([(16, y + 40), (W - 16, y + 40)], fill=(170, 160, 140), width=1)
    d.rectangle([6, 6, W - 7, H - 7], outline=(90, 80, 60), width=3)
    im.save(path)
    GEN.TEXTS.extend(["PRICE CHART", "OZ", "AT 1.80", "AT 2.60"] + ["%.2f" % (1.80 * oz / 16.0) for oz in (4, 8, 12, 16, 24, 32, 48)])


def _grating(path):
    """A stainless drain grating, seen from above: a steel frame, parallel slots (dark) between bars (steel)."""
    s = 256
    im = Image.new("RGB", (s, s), (176, 180, 184))
    d = ImageDraw.Draw(im)
    for k in range(10, s - 10, 18):
        d.rectangle([k, 16, k + 8, s - 17], fill=(24, 26, 30))
    d.rectangle([0, 0, s - 1, s - 1], outline=(120, 124, 130), width=8)
    im.save(path)


def _wet_patch(path, size=512, seed=6):
    """A hosed dark patch on the quarry: an irregular soft-edged alpha (dark, 0.35) round the drain."""
    rnd = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    u, v = (xx / size - 0.5) * 2, (yy / size - 0.5) * 2
    core = np.clip(1.0 - (u * u + v * v) * 1.05, 0, 1)
    noise = np.asarray(Image.fromarray((rnd.random((size // 16, size // 16)) * 255).astype(np.uint8)).resize((size, size), Image.BICUBIC), np.float32) / 255.0
    a = np.clip(core * (0.6 + 0.8 * noise), 0, 1) * 0.55
    rgba = np.zeros((size, size, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 20, 14, 12
    rgba[..., 3] = (a * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(path)


def _slab_png(path, size=1024):
    """The slab's marble: Poly Haven marble_01's base colour (a cream limestone) lightened and desaturated toward white marble (the target: 'a white marble slab'), kept under luma 215."""
    src = Image.open(os.path.join(A.POLY, "marble_01", "1k", "textures", "marble_01_diff_1k.jpg")).convert("RGB").resize((size, size))
    a = np.asarray(src, np.float32)
    g = a.mean(axis=2, keepdims=True)
    a = g + (a - g) * 0.35
    a = a * 0.98 + 24.0
    Image.fromarray(np.clip(a, 0, 214).astype(np.uint8)).save(path)


# ---------------------------------------------------------------------------------------------------------------------------------- the room
def room(r):
    """The fishmonger's room (target `shops.fish_market.room`: fixtures F-*). What the target leaves open, and what this does:

    chiller F-back-counter (x -2.45 to 0.55, 0.60 deep, 1.0 high): built here (the generic counter has no well): a white laminate body with raised panels and a dark plinth, a well at z 0.78 under a sloping glass
    front (from z 0.80 at the front to the 1.0 top, 0.42 back; the room's glass with the shadow-ray trick), a laminate top behind it with a stainless edge; eight white enamel trays 0.35 x 0.30 x 0.05 (the target's 0.45
    leaves 6 in 3.0 m), each with a mound of ice. NO FISH: they are Sketchfab scans (Jafar's login), the target's `script:fish_on_ice`, pending; nothing is made by hand in their place.
    shelf F-back-shelf (x -2.45 to 0.55, 0.15 deep, tiers 1.55 and 1.90, standing on the chiller's top): tins (eight designs: pilchards, salmon, sardines, kippers, herring, mussels, crab, shrimps) and jars (crab,
    shrimp, anchovy, salmon paste, pickled herring), one row, in the project's own makers' names (SALTHOUSE, TIDEMARK, FENWICK, BRIGHTWATER).
    door F-back-door: the cold-room door 0.9 x 2.0, white plastic-faced in a grey rubber seal, a chrome lever and three hinges, flat (70 mm). hose F-back-hose: garden_hose_wall_mounted_01.
    left board F-left-board: a blackboard 0.8 x 0.6 (chalk: TODAY'S FISH, COD, HADDOCK, PLAICE, KIPPERS and the prices). right F-right-clock: the clock and a printed price chart.
    floor: terracotta_floor_tiles, wet (roughness 0.16), a stainless grating 0.3 x 0.3 flush (decal) and a hosed dark patch. The chiller's pilot lamp (an amber indicator lens on its front, with a warm point light 0.02 m before it) is the night_dark picture's one warm point."""
    _setup()
    import sw_room_gen as RG
    import bpy
    D, W = RG.D, RG.W
    rr = r.RR
    fx = r.fxd
    rnd = r.rnd
    tex = r.tex
    GEN.TEXTS.clear()
    # the wet quarry
    pb = r.floor_m.node_tree.nodes.get("Principled BSDF")
    if pb is not None:
        for l in list(pb.inputs["Roughness"].links):
            r.floor_m.node_tree.links.remove(l)
        pb.inputs["Roughness"].default_value = 0.16
    white = r.mat("chiller_laminate", rgb8(198, 200, 196), rough=0.3)
    white2 = r.mat("chiller_panel", rgb8(208, 210, 206), rough=0.3)
    dark = r.mat("chiller_plinth", rgb8(70, 72, 76), rough=0.5)
    steel = r.mat("stainless", rgb8(190, 192, 194), rough=0.25, metal=1.0)
    enamel = r.mat("enamel", rgb8(214, 216, 212), rough=0.2)
    ice_m = r.mat("ice", rgb8(178, 198, 210), rough=0.2)
    glass = r.mat("chiller_glass", (0.9, 0.95, 0.95), rough=0.02, glass=True)
    cx0, cx1 = fx["F-back-counter"]["x"]
    ch = 1.0
    cy0 = D - fx["F-back-counter"]["depth_m"]
    cy1 = D - 0.005
    r.box("chiller_plinth", cx0, cx1, cy0 + 0.06, cy1, 0.0, 0.07, dark, fixture="F-back-counter")
    r.box("chiller_body", cx0, cx1, cy0 + 0.03, cy1, 0.07, 0.76, white, fixture="F-back-counter")
    npan = int(round((cx1 - cx0) / 0.6))
    wp = (cx1 - cx0) / npan
    for k in range(npan):
        r.box("chiller_panel_%d" % k, cx0 + k * wp + 0.04, cx0 + (k + 1) * wp - 0.04, cy0 + 0.018, cy0 + 0.03, 0.14, 0.70, white2, fixture="F-back-counter")
    r.box("chiller_well_floor", cx0 + 0.02, cx1 - 0.02, cy0 + 0.03, cy0 + 0.42, 0.76, 0.78, enamel, fixture="F-back-counter")
    r.box("chiller_back_block", cx0, cx1, cy0 + 0.42, cy1, 0.76, 0.97, white, fixture="F-back-counter")
    r.box("chiller_top", cx0, cx1, cy0 + 0.42, cy1, 0.97, 1.0, white2, fixture="F-back-counter")
    r.box("chiller_top_edge", cx0 + 0.02, cx1 - 0.02, cy0 + 0.428, cy0 + 0.442, 1.0, 1.004, steel, fixture="F-back-counter")
    r.box("chiller_rail", cx0, cx1, cy0, cy0 + 0.03, 0.76, 0.80, steel, fixture="F-back-counter")
    for xe in (cx0, cx1 - 0.02):
        r.box("chiller_end_%d" % int(xe * 10), xe, xe + 0.02, cy0 + 0.03, cy0 + 0.42, 0.78, 1.0, white2, fixture="F-back-counter")
    # the sloping glass front
    gm = GM()
    slope = math.degrees(math.atan2(0.20, 0.39))
    gm.sheet(((cx0 + cx1) / 2, cy0 + 0.03 + 0.195, 0.81 + 0.10), cx1 - cx0 - 0.04, math.hypot(0.20, 0.39), 0.006, tilt=90.0 - slope, mi=0)
    o = gm.to_object("chiller_glass", [glass], r.sc)
    r.fixture_rec("F-back-counter", "chiller_glass", gm.extents())
    # eight trays with ice
    gt, gi = GM(), GM()
    tw, td = 0.35, 0.30
    tpitch = (cx1 - cx0 - 0.10) / 8.0
    tray_y = cy0 + 0.25
    for k in range(8):
        xc = cx0 + 0.05 + tpitch * (k + 0.5)
        GB.enamel_tray(gt, xc, tray_y, 0.78, w=tw, d=td, h=0.05, mi=0, mi_rim=0)
        GB.ice_mound(gi, xc, tray_y, 0.781, 0.140, 0.115, 0.045, 260, 11 + k, mi=0)
    o1 = gt.to_object("trays", [enamel], r.sc)
    ip_r = os.path.join(tex, "ice.png")
    GB.ice_png(ip_r)
    o2 = gi.to_object("tray_ice", [r.image_mat("ice_chunks", ip_r, rough=0.22)], r.sc, smooth=False)
    ext = [min(gt.extents()[0], gi.extents()[0]), max(gt.extents()[1], gi.extents()[1]), gt.extents()[2], gt.extents()[3], 0.78, max(gt.extents()[5], gi.extents()[5])]
    r.placed_rec("F-back-counter", "script:enamel_trays", ext, [o1.name, o2.name], tag="trays", n=8)
    # ---- the shelves on the counter's top: tins and jars, one row
    sx0, sx1 = cx0 + 0.015, cx1 - 0.015
    r.shelf_unit("F-back-shelf", [(1.55, sx0, sx1), (1.90, sx0, sx1)], depth=fx["F-back-shelf"]["depth_m"], bottom=1.0)
    metal = r.mat("tin_metal", rgb8(168, 168, 164), rough=0.35, metal=0.85)
    tp = os.path.join(tex, "fish_tins.png")
    tuv = GB.tin_atlas(tp, TIN_DESIGNS, tile=(256, 128), cols=4)
    tin_label = r.image_mat("fish_tin_labels", tp, rough=0.5)
    jl = os.path.join(tex, "fish_jars.png")
    juv = GB.jar_labels(jl, [(p_, m_, c1, c2) for p_, m_, c1, c2 in JAR_DESIGNS], tile=(256, 256), cols=3)
    jar_lab = r.image_mat("fish_jar_labels", jl, rough=0.5)
    lid_m = r.mat("jar_lid", rgb8(196, 160, 60), rough=0.35, metal=0.8)
    n_tin = n_jar = 0
    for z in (1.55, 1.90):
        gtn = GM()
        gjs = [GM() for _ in JAR_DESIGNS]
        cj = [0] * len(JAR_DESIGNS)
        x = sx0 + 0.04
        nt = 0
        yc = D - 0.085
        while x < sx1 - 0.09:
            if rnd.random() < 0.3:
                ji = rnd.randrange(len(JAR_DESIGNS))
                GB.jar(gjs[ji], x + 0.0375, yc, z, 0.0375, 0.115, 0, 1, juv[ji][1], 2, n=20)
                cj[ji] += 1
                x += 0.085
            else:
                rad = rnd.choice((0.0375, 0.0425))
                hh = rnd.choice((0.075, 0.095, 0.11))
                if x + 2 * rad * 1.035 > sx1 - 0.03:
                    break
                GB.paint_tin(gtn, x + rad * 1.035, yc, z, rad, hh, tuv[rnd.randrange(len(TIN_DESIGNS))], n=14, bail=False)
                nt += 1
                x += 2 * rad * 1.035 + 0.004
        if gtn.V:
            o = gtn.to_object("shelf_tins_%.2f" % z, [metal, tin_label], r.sc)
            r.placed_rec("F-back-shelf", "script:tins_and_jars", gtn.extents(), [o.name], tag="tins_%.2f" % z, n=nt)
            n_tin += nt
        for ji, gmj in enumerate(gjs):
            if not gmj.V:
                continue
            fill_m = r.mat("fish_jar_fill_%d" % ji, rgb8(*JAR_DESIGNS[ji][2]), rough=0.18)
            o = gmj.to_object("shelf_jars_%d_%.2f" % (ji, z), [fill_m, jar_lab, lid_m], r.sc, smooth=True)
            r.placed_rec("F-back-shelf", "script:tins_and_jars", gmj.extents(), [o.name], tag="jars_%d_%.2f" % (ji, z), n=cj[ji])
            n_jar += cj[ji]
    # ---- the cold-room door: a grey rubber seal, a white plastic-faced door, a chrome lever, three hinges, a steel kick plate
    seal = r.mat("door_seal", rgb8(62, 64, 66), rough=0.7)
    dwhite = r.mat("door_white", rgb8(206, 208, 204), rough=0.35)
    dx0, dx1 = fx["F-back-door"]["x"]
    r.box("door_seal_l", dx0 - 0.04, dx0, D - 0.068, D - 0.005, 0.0, 2.04, seal, fixture="F-back-door")
    r.box("door_seal_r", dx1, dx1 + 0.04, D - 0.068, D - 0.005, 0.0, 2.04, seal, fixture="F-back-door")
    r.box("door_seal_t", dx0, dx1, D - 0.068, D - 0.005, 2.0, 2.04, seal, fixture="F-back-door")
    r.box("door_slab", dx0, dx1, D - 0.070, D - 0.02, 0.0, 2.0, dwhite, fixture="F-back-door")
    r.box("door_kick", dx0 + 0.02, dx1 - 0.02, D - 0.0725, D - 0.0705, 0.02, 0.22, steel, fixture="F-back-door")
    r.box("door_lever_stem", dx1 - 0.14, dx1 - 0.12, D - 0.108, D - 0.0705, 1.00, 1.02, steel, fixture="F-back-door")
    r.box("door_lever", dx1 - 0.26, dx1 - 0.10, D - 0.118, D - 0.108, 0.995, 1.025, steel, fixture="F-back-door")
    for k, zh in enumerate((0.30, 1.00, 1.70)):
        r.box("door_hinge_%d" % k, dx0 + 0.005, dx0 + 0.045, D - 0.0725, D - 0.0705, zh, zh + 0.12, steel, fixture="F-back-door")
    r.place("garden_hose_wall_mounted_01", (1.05, D - 0.005, 1.1), rot=(0, 0, 0), scale=1.0, fixture="F-back-hose", anchor=("c", "max", "c"), tag="hose")
    # ---- the left wall: the blackboard
    xl, xr = -W / 2, W / 2
    cb = os.path.join(tex, "chalk_board.png")
    _chalk_board(cb)
    cbm = r.image_mat("chalk_board", cb, rough=0.9)
    frame_m = r.mat("board_frame", rgb8(120, 84, 54), rough=0.6)
    fb0, fb1, fz0, fz1 = 1.40, 2.20, 1.20, 1.80
    r.box("blackboard_frame_t", xl + 0.001, xl + 0.025, fb0 - 0.03, fb1 + 0.03, fz1, fz1 + 0.03, frame_m, fixture="F-left-board")
    r.box("blackboard_frame_b", xl + 0.001, xl + 0.025, fb0 - 0.03, fb1 + 0.03, fz0 - 0.03, fz0, frame_m, fixture="F-left-board")
    r.box("blackboard_frame_l", xl + 0.001, xl + 0.025, fb0 - 0.03, fb0, fz0, fz1, frame_m, fixture="F-left-board")
    r.box("blackboard_frame_r", xl + 0.001, xl + 0.025, fb1, fb1 + 0.03, fz0, fz1, frame_m, fixture="F-left-board")
    bg = GM()
    bg.box(xl + 0.001, xl + 0.020, fb0, fb1, fz0, fz1, 0, uv_front=(0.0, 0.0, 1.0, 1.0), front="+x", uv_other=(0.02, 0.02))
    o = bg.to_object("blackboard", [cbm], r.sc)
    r.placed_rec("F-left-board", "script:price_board_chalk", bg.extents(), [o.name], tag="board", n=1)
    # ---- the right wall: the clock and the price chart
    ck_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "wall_clock") / max(r.dims("wall_clock"))
    r.place("wall_clock", (xr - 0.022, 1.16, 1.95), rot=(0, 0, -math.pi / 2), scale=ck_s, fixture="F-right-clock", anchor=("max", "c", "c"), clock=r.next_clock(), tag="clock")
    cpng = os.path.join(tex, "weights_chart.png")
    _weights_chart(cpng)
    cm = r.image_mat("weights_chart", cpng, rough=0.7)
    cg = GM()
    cg.box(xr - 0.0105, xr - 0.0085, 1.30, 1.50, 1.80, 2.10, 0, uv_front=(0.0, 0.0, 1.0, 1.0), front="-x")
    o = cg.to_object("weights_chart", [cm], r.sc)
    r.fixture_rec("F-right-clock", "weights_chart", cg.extents())
    # ---- the floor: the drain and the hosed patch
    gp = os.path.join(tex, "drain_grating.png")
    _grating(gp)
    wpth = os.path.join(tex, "wet_patch.png")
    _wet_patch(wpth)
    GB.floor_decal(r, "wet_patch", wpth, -0.75, 0.25, 2.30, 3.20, z=0.0010, fixture="F-floor-drain")
    gm_ = r.image_mat("drain_grating", gp, rough=0.35)
    me = bpy.data.meshes.new("drain_grating")
    x0_, x1_, y0_, y1_, zf = -0.40, -0.10, 2.60, 2.90, 0.0030
    me.from_pydata([(x0_, y0_, zf), (x1_, y0_, zf), (x1_, y1_, zf), (x0_, y1_, zf)], [], [(0, 1, 2, 3)])
    uvl = me.uv_layers.new(name="UVMap")
    for loop, (a, b) in zip(me.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        uvl.data[loop.index].uv = (a, b)
    ob = bpy.data.objects.new("drain_grating", me)
    r.sc.collection.objects.link(ob)
    ob.data.materials.append(gm_)
    r.fixtures.append({"fixture": "F-floor-drain", "name": "drain_grating", "ext": [x0_, x1_, y0_, y1_, 0.0, zf]})
    # the chiller's pilot lamp (night_dark). 14 Oct (the tea rooms' close review, 10): a point light with no fitting is a glow from nowhere; the light now stands 0.02 m in front of a 10 mm amber indicator
    # lens on the chiller's front (emissive in night_dark only), at the left end under the rail, 0.5 W
    lens_m = r.mat("chiller_pilot_lens", rgb8(255, 160, 60), rough=0.3, emit=(1.0, 0.55, 0.15), emit_strength=0.0)
    lx_ = cx0 + 0.14
    lgm = GM()
    lgm.rod((lx_, cy0 + 0.030, 0.73), (lx_, cy0 + 0.0235, 0.73), 0.005, 0, 14)
    lo_ = lgm.to_object("chiller_pilot_lens", [lens_m], r.sc, smooth=True)
    r.fixture_rec("F-back-counter", "chiller_pilot_lens", lgm.extents())
    ld = bpy.data.lights.new("chiller_pilot", "POINT")
    ld.energy = 0.0
    ld.color = (1.0, 0.62, 0.30)
    ld.shadow_soft_size = 0.008
    po_ = bpy.data.objects.new("chiller_pilot", ld)
    r.sc.collection.objects.link(po_)
    po_.location = (lx_, cy0 + 0.0035, 0.73)
    r.pilot = po_
    r.pilot_w = 0.5
    orig_ss_ = r.set_state

    def set_state_(state, P, _o=orig_ss_, _m=lens_m):
        _o(state, P)
        _m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0 if state == "night_dark" else 0.0
    r.set_state = set_state_
    r.rows["counts"] = {"tins": n_tin, "jars": n_jar}
    r.notes.append("%d tins and %d jars on the shelves (target 24); eight trays of ice, no fish (pending: Sketchfab scans, Jafar's login); the floor is wet (roughness 0.16)" % (n_tin, n_jar))
    r.texts = list(GEN.TEXTS)
    return r


# ---------------------------------------------------------------------------------------------------------------------------------- the window
def display(d):
    """The fishmonger's window (target `shops.fish_market.display`, 6 item rows; bed 3.35 x 0.55; 1.1 high at most). What this does (each a Judgement in NOTES.md):
    slab: a white marble slab (marble_01 lightened toward white) sloping 12 degrees up toward the back (the glass side low: 0.03 at the front to 0.14 at the back) with a 40 mm lip at the front; crushed ice: a
    lumpy bed 0.03 deep (a picture by script, not ambientCG Ice002, a frozen lake) with 300 chunks of four shapes in the gaps between the trays, all one mesh; six white enamel trays 0.40 x 0.30 x 0.05 laid on the slope
    (the front rank is the same slope), each with a mound of ice; eight whole lemons (lemon, Poly Haven) beside the trays; fourteen tickets (40 x 25 mm cards on 100 mm stakes, prices per lb in hand lettering);
    a white laminate back panel (the chiller pad). PENDING: the fish (cod x4, mackerel x8, herring x6, plaice x4, crab x5, prawns x60): Sketchfab scans behind Jafar's login; none is modelled by hand, the trays carry
    ice and tickets only."""
    _setup()
    import sw_room_gen as RG
    rr = d.RR
    walls = rr["walls"]
    d.start((236, 236, 232), (206, 204, 196), (206, 204, 196))
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    tex = d.tex
    GEN.TEXTS.clear()
    # ---- the slab
    sp = os.path.join(tex, "slab_marble.png")
    _slab_png(sp)
    slab_m = d.image_mat("slab_marble", sp, rough=0.25)
    tan = math.tan(math.radians(12.0))
    z_f, z_b = 0.03, 0.03 + 0.52 * tan
    x0, x1 = X(0.02), X(L - 0.02)
    v0, v1 = 0.02, 0.52                     # the slab ends 4 mm short of the laminate pad (0.524), so that the two do not pass through each other (DSP-03)
    V = [(x0, v0, 0.0), (x1, v0, 0.0), (x1, v1, 0.0), (x0, v1, 0.0), (x0, v0, z_f), (x1, v0, z_f), (x1, v1, z_b + 0.0), (x0, v1, z_b + 0.0)]
    z_at = lambda v: z_f + (v - v0) * tan
    V[6] = (x1, v1, z_at(v1))
    V[7] = (x0, v1, z_at(v1))
    F = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    ta = 0.9
    uvt = [[(x / ta, y / ta) for (x, y, _) in [V[4], V[5], V[6], V[7]]]]
    U = [None, uvt[0], [(0.1, 0.1)] * 4, [(0.1, 0.1)] * 4, [(0.1, 0.1)] * 4, [(0.1, 0.1)] * 4]
    gm = GM()
    gm.add(V, F, 0, U)
    # the lip: a bar 40 mm over the surface at the front
    gm.box(x0, x1, v0, v0 + 0.018, z_f, z_f + 0.040, 0, uv_front=(0.0, 0.0, 0.2, 0.05), uv_other=(0.1, 0.1))
    ob, _ = d.gm_object("slab", gm, [slab_m], "support", "script:slab_and_ice")          # the table the goods stand on: a support (the sill and the trays hide most of it from the far pavement; DSP-03 is for goods)
    GB.chamfer(ob, 0.002, 2)
    # ---- the ice bed (lumpy, peaks at 0.03) and chunks in the gaps between the trays; one mesh
    ip = os.path.join(tex, "ice.png")
    GB.ice_png(ip)
    ice_m = d.image_mat("ice", ip, rough=0.22)
    tray_us = [0.25, 0.66, 1.25, 1.86, 2.30, 2.90]                 # six trays 0.40 wide, placed in the lights (the mullions stand at u 0.825 to 0.875, 1.65 to 1.70 and 2.475 to 2.525: a tray under a mullion showed 0.47 of its ice from STREET_SQUARE, DSP-03)
    tray_v0, tray_v1 = 0.12, 0.42
    nx, ny = 70, 11
    gi = GM()
    verts = []
    for j in range(ny + 1):
        for i in range(nx + 1):
            u = 0.06 + (L - 0.12) * i / nx
            v = 0.06 + (0.50 - 0.06) * j / ny
            h = 0.0282 + 0.0018 * (0.5 + 0.5 * math.sin(i * 1.7 + j * 2.3) * math.cos(j * 1.3 - i * 0.9))
            verts.append((X(u), v, z_at(v) + h))
    F2, U2 = [], []
    for j in range(ny):
        for i in range(nx):
            a = j * (nx + 1) + i
            F2.append((a, a + 1, a + nx + 2, a + nx + 1))
            u0_, v0_ = (i % 8) / 8.0, (j % 8) / 8.0
            U2.append([(u0_, v0_), (u0_ + 0.125, v0_), (u0_ + 0.125, v0_ + 0.125), (u0_, v0_ + 0.125)])
    # a closed solid: the bed's underside on the slab (a flat copy), so the mesh has volume
    n0 = len(verts)
    under = [(x, y, z_at(y) - 0.0005) for (x, y, z) in verts]
    F3 = [tuple(n0 + k for k in reversed(f)) for f in F2]
    gi.add(verts + under, F2 + F3, 0, U2 + U2)
    n_chunks = 0
    for k in range(300):
        u = rnd.uniform(0.10, L - 0.10)
        v = rnd.uniform(0.07, 0.49)
        if any(abs(u - tu) < 0.215 for tu in tray_us) and tray_v0 - 0.02 < v < tray_v1 + 0.02:
            continue
        sz = rnd.uniform(0.018, 0.034)
        ice_chunk_u = ((k % 4) * 0.25, 0.0, (k % 4) * 0.25 + 0.2, 0.5)
        GB.ice_chunk(gi, (X(u), v, z_at(v) + 0.020 + 0.0 * sz), sz, seed=k % 4 + 7 * (k % 7), mi=0, uv=(ice_chunk_u[0], ice_chunk_u[1] + 0.2, ice_chunk_u[2], ice_chunk_u[3] + 0.2))
        n_chunks += 1
    d.gm_object("ice_bed", gi, [ice_m], "support", "script:slab_and_ice", tier="slab", smooth=False)          # the bed the trays stand in (support)
    # ---- six trays laid on the slope, each with a mound of ice
    tw, td = 0.40, 0.30
    enamel = d.mat("enamel", rgb8(210, 212, 208), rough=0.2)
    for k, uc in enumerate(tray_us):
        gt = GM()
        vc = 0.5 * (tray_v0 + tray_v1)
        zc = z_at(vc) + 0.0292
        GB.enamel_tray(gt, X(uc), vc, zc, w=tw, d=td, h=0.05, mi=0, mi_rim=0)
        GB.rot_x(gt, 0, (vc, zc), 12.0)
        d.gm_object("tray_%d" % k, gt, [enamel], "scripted", "script:enamel_trays", tier="slab")
        gh = GM()
        gh_i0 = len(gh.V)
        GB.ice_mound(gh, X(uc), vc, zc + 0.003, 0.160, 0.110, 0.042, 380, 21 + k, mi=0)
        GB.rot_x(gh, gh_i0, (vc, zc), 12.0)
        d.gm_object("tray_ice_%d" % k, gh, [ice_m], "scripted", "script:slab_and_ice", tier="slab", smooth=False)
    # ---- eight lemons between and beside the trays (resting on the ice bed)
    # (each in a light of the window, clear of the mullions at u 0.825 to 0.875, 1.65 to 1.70 and 2.475 to 2.525 and of the trays: a lemon behind a mullion showed 0.49 of itself, DSP-03; two lay on one another at u 1.60 before)
    for k, (lu, lv) in enumerate([(0.55, 0.48), (0.20, 0.07), (1.00, 0.47), (1.52, 0.27), (1.95, 0.48), (2.20, 0.07), (2.60, 0.27), (3.22, 0.30)]):
        lz = GB.rest_z(d, X(lu), lv, 0.034)
        _, nm_ = d.piece("lemon", lu, lv, lz + 0.003, rot=(0, 0, rnd.uniform(0, 6.28)), scale=1.0, tier="slab", tris=None)
        GB.settle_down(d, nm_, max_drop=0.03)
    # ---- the chiller pad: a white laminate panel at the back
    lam = d.mat("chiller_pad", rgb8(206, 208, 204), rough=0.3)
    gm = GM()
    gm.box(X(0.0), X(L), 0.524, 0.549, 0.0, 0.30, 0)
    ob, _ = d.gm_object("chiller_pad", gm, [lam], "support", "script:chiller_pad")          # the back panel behind the goods (support)
    GB.chamfer(ob, 0.002, 2)
    # ---- fourteen tickets on 100 mm stakes, prices per lb in hand lettering
    names = ["COD\n2.60 lb", "HADDOCK\n2.45 lb", "PLAICE\n2.90 lb", "KIPPERS\n1.80 lb", "WHITING\n1.60 lb", "SKATE\n2.20 lb", "HERRING\n1.20 lb", "MACKEREL\n1.10 lb", "CRAB\n3.40 lb", "PRAWNS\n4.80 lb", "COCKLES\n1.00 pt", "SMOKED COD\n2.90 lb", "LEMONS\n8p each", "ICE\nFREE"]
    tp = os.path.join(tex, "tickets.png")
    tuv = GEN.card_atlas(tp, names, cols=4, tile=(256, 160), size=40, bg=(244, 242, 232))
    tm = d.image_mat("tickets", tp, rough=0.7)
    stake_m = d.mat("ticket_stake", rgb8(190, 192, 196), rough=0.4, metal=0.6)
    sg, cg = GM(), GM()
    for k in range(14):
        uc = 0.22 + 0.22 * k
        vc = 0.10 + 0.0 * k + (0.0 if k % 2 == 0 else 0.34)
        z0 = z_at(vc) + 0.0296                # the stake stands ON the ice bed (its top is 0.0282 to 0.030 over the slab), not in it (DSP-03)
        sg.rod((X(uc), vc, z0 - 0.0006), (X(uc), vc, z0 + 0.100), 0.0012, 0, 6)
        cg.sheet((X(uc), vc - 0.0024, z0 + 0.100 + 0.0125 - 0.003), 0.040, 0.025, 0.002, tilt=6.0, mi=0, uv=tuv[k], uv_other=(tuv[k][0] + 0.01, tuv[k][1] + 0.01))
    d.gm_object("ticket_stakes", sg, [stake_m], "support", "script:price_stakes")
    d.gm_object("tickets", cg, [tm], "scripted", "script:price_stakes", tier="slab")
    d.display_texts = list(GEN.TEXTS) + [n.replace("\n", " ") for n in names]
