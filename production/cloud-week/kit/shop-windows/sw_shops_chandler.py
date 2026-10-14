"""The ship chandler (east_chandler bay 0, "chandler"): the room's layout and the window display (14 October 2026, batch B). Read from `shops.chandler.room` and `.display` in target.json; every choice the target left
open is stated in the docstrings (each a Judgement in NOTES.md and a `Changes after the build` line).

Content rule: no drink, no explosives (the 3 Oct drum is out), no ship model, no hanging from the ceiling; every maker and every chart is the project's own. Rope and twine are ambientCG Rope001 and Rope002 (CC0) on
swept tubes; the sou'westers are a sewn pattern by script (the library's fishermans_hat is a boonie hat).
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw

import sw_assets as A
import sw_gen as GEN
import sw_goods_b as GB
from sw_gen import GM

rgb8 = None

TIN_DESIGNS = [("PENHALE", "MARINE VARNISH", "clear gloss", (120, 70, 30), (246, 232, 200), (246, 232, 200)),
               ("PENHALE", "ANTIFOULING", "red", (160, 40, 36), (246, 236, 214), (246, 236, 214)),
               ("TREGENNA", "DECK PAINT", "slate grey", (90, 100, 110), (240, 238, 228), (240, 238, 228)),
               ("TREGENNA", "WHITE SPIRIT", "", (236, 232, 218), (30, 60, 120), (30, 60, 120)),
               ("WESTHAVEN", "BILGE PAINT", "grey", (70, 80, 84), (236, 232, 216), (236, 232, 216)),
               ("PENHALE", "METAL PRIMER", "red oxide", (150, 70, 46), (246, 236, 214), (246, 236, 214)),
               ("WESTHAVEN", "TEAK OIL", "", (190, 140, 60), (60, 40, 20), (60, 40, 20)),
               ("TREGENNA", "HULL PAINT", "navy", (30, 50, 100), (240, 236, 220), (240, 236, 220)),
               ("PENHALE", "EPOXY FILLER", "", (220, 200, 90), (60, 50, 30), (60, 50, 30)),
               ("WESTHAVEN", "BOAT VARNISH", "yacht", (170, 110, 40), (250, 240, 210), (250, 240, 210)),
               ("TREGENNA", "BITUMEN PAINT", "black", (40, 40, 44), (230, 220, 190), (230, 220, 190)),
               ("PENHALE", "WHITE GLOSS", "", (236, 236, 230), (150, 40, 40), (150, 40, 40))]
ROPE_COLOURS = [(176, 146, 92), (52, 96, 162), (226, 120, 34), (226, 222, 210), (66, 128, 76)]          # natural, blue, orange, white, green


def _setup():
    global rgb8
    import sw_room as S
    rgb8 = S.rgb8


def _map_wall(gm, i0, f):
    """Move the vertices from index `i0` on through `f(x, y, z) -> (x, y, z)` (a local frame to a side wall's)."""
    for i in range(i0, len(gm.V)):
        gm.V[i] = tuple(float(c) for c in f(*gm.V[i]))


# ---------------------------------------------------------------------------------------------------------------------------------- the room
def room(r):
    """The chandler's room (target `shops.chandler.room`: fixtures C-*). What the target leaves open, and what this does:

    shelves C-back-shelves: tall shelving 0.30 deep, five tiers (board tops 0.4, 0.8, 1.2, 1.6, 2.0), from x -1.95 to 0.2 (the target's -2.6 to 0.2 is shared with the marker buoy at the left end, which stands
    against the wall at x -2.6 to -2.0: the shelves start where it ends). Floor level: four pairs of rubber_boots at 0.6 of their size; 0.4: oil_tin x5, small_oil_can_01 x4, cleaner_tin_01 x4; 0.8 and 1.2: paint tins
    (lathe, a rim and a wire bail, atlas labels: marine varnish, antifouling, deck paint, white spirit; makers PENHALE, TREGENNA, WESTHAVEN), two deep; 1.2 also four Lantern_01 (glass kept) and three signal_flashlight;
    1.6: six coils of rope standing on edge (swept tube, ambientCG Rope001 picture in five colours); 2.0: ten twine reels and more tins.
    counter C-back-counter (x 0.4 to 2.6, 0.6 deep, panelled, a brass edge, a chart drawer): CashRegister_01 at 0.42 (mark blanked), three seadogs_compass, the hurricane lamp (Lantern_01, lit at night: a warm
    point light 2200 K and a small flame).
    hooks C-back-hooks: a timber board over the counter (x 0.4 to 2.5, z 1.35 to 2.2, 0.18) carrying life_jacket x3 at 0.7, one lifebuoy at 0.8 and two sou'westers: the target's 4, 2 and 3 do not fit 2.1 m without
    one hanging through another (short, named in NOTES.md).
    left wall C-left-charts: six invented chart sheets and a tide-table card (paper, script) and a board with a flat coil of rope. right wall C-right-board: a pegboard 1.6 x 1.1 with 24 pieces of hardware (shackles,
    single blocks, horn cleats, chain), flat.
    buoy C-floor-buoy: ocean_buoy scaled to 1.5 m tall (its lamp unlit), standing on the floor against the back wall at the left end."""
    _setup()
    import sw_room_gen as RG
    import bpy
    D, W = RG.D, RG.W
    rr = r.RR
    fx = r.fxd
    rnd = r.rnd
    tex = r.tex
    GEN.TEXTS.clear()
    GB.fetch_ropes()
    steel = r.mat("hw_steel", rgb8(170, 172, 176), rough=0.3, metal=1.0)
    metal = r.mat("tin_metal", rgb8(168, 168, 164), rough=0.35, metal=0.85)
    tp = os.path.join(tex, "marine_tins.png")
    tuv = GB.tin_atlas(tp, TIN_DESIGNS, tile=(256, 128), cols=4)
    tin_label = r.image_mat("marine_tin_labels", tp, rough=0.5)
    rope_m = []
    for i, c in enumerate(ROPE_COLOURS):
        pth = os.path.join(tex, "rope_%d.png" % i)
        GB.rope_png(pth, c, which=1)
        rope_m.append(r.image_mat("rope_%d" % i, pth, rough=0.9))
    twine_pth = os.path.join(tex, "twine.png")
    GB.rope_png(twine_pth, (200, 178, 128), which=2)
    twine_m = r.image_mat("twine", twine_pth, rough=0.9)
    reel_wood = r.mat("reel_wood", rgb8(150, 110, 70), rough=0.6)
    # ---- the buoy at the left end
    bs = 1.5 / r.dims("ocean_buoy").z
    r.place("ocean_buoy", (-2.6 + 1.067 * bs / 2 + 0.01, D - 0.01, 0.0), rot=(0, 0, 0), scale=bs, fixture="C-floor-buoy", anchor=("c", "max", "min"), tag="buoy")
    # ---- the shelves
    sx0, sx1 = -1.95, fx["C-back-shelves"]["x"][1]
    tiers = fx["C-back-shelves"]["tiers"]
    r.shelf_unit("C-back-shelves", [(z, sx0 + 0.015, sx1 - 0.015) for z in tiers], depth=fx["C-back-shelves"]["depth_m"])
    xa, xb = sx0 + 0.04, sx1 - 0.04
    # floor level: four pairs of boots at 0.6 of their size
    bsc = 0.6
    bw = r.dims("rubber_boots").x * bsc
    xb0 = xa
    for k in range(4):
        r.place("rubber_boots", (xb0 + bw / 2 + k * (bw + 0.004), D - 0.02, 0.0), rot=(0, 0, 0), scale=bsc, fixture="C-back-shelves", anchor=("c", "max", "min"), tag="boots")
    # 0.4: oil tins, oil cans, cleaner tins in a row
    x = xa
    row = []
    row += [("oil_tin", 1.0)] * 5 + [("small_oil_can_01", 1.0)] * 4 + [("cleaner_tin_01", 1.0)] * 4
    rnd.shuffle(row)
    for asset, sc in row:
        d_ = r.dims(asset)
        if x + d_.x * sc > xb:
            break
        r.place(asset, (x + d_.x * sc / 2, D - 0.02, tiers[0]), rot=(0, 0, 0), scale=sc, fixture="C-back-shelves", anchor=("c", "max", "min"), tag=asset)
        x += d_.x * sc + rnd.uniform(0.01, 0.025)
    # tins, two deep, on 0.8 and 1.2 (1.2: the left part), 2.0 (the right part)

    def tins(gm, x0, x1, z, rows_y=(D - 0.080, D - 0.225), kinds=((0.07, 0.18), (0.062, 0.15), (0.055, 0.12))):
        n = 0
        for yc in rows_y:
            x = x0
            while True:
                rad, hh = rnd.choice(kinds)
                if x + 2 * rad * 1.035 > x1:
                    break
                if rnd.random() < 0.05:
                    x += 2 * rad * 1.035 + 0.006
                    continue
                GB.paint_tin(gm, x + rad * 1.035, yc, z, rad, hh, tuv[rnd.randrange(len(TIN_DESIGNS))], n=16)
                n += 1
                x += 2 * rad * 1.035 + 0.006
        return n
    n_tins = 0
    plan = {tiers[1]: [(xa, xb)], tiers[2]: [(xa, xa + 0.95)], tiers[4]: [(xa + 1.10, xb)]}
    for z, segs in plan.items():
        gm = GM()
        nt = 0
        for a_, b_ in segs:
            nt += tins(gm, a_, b_, z)
        o = gm.to_object("paint_tins_%.2f" % z, [metal, tin_label], r.sc)
        r.placed_rec("C-back-shelves", "script:paint_tins", gm.extents(), [o.name], tag="tins_%.2f" % z, n=nt)
        n_tins += nt
    # 1.2: four Lantern_01 and three signal flashlights, to the right of the tins
    x = xa + 1.00
    for k in range(4):
        r.place("Lantern_01", (x + 0.07, D - 0.10, tiers[2]), rot=(0, 0, rnd.uniform(-0.3, 0.3)), scale=1.0, fixture="C-back-shelves", anchor=("c", "c", "min"), tag="lantern")
        x += 0.16
    for k in range(3):
        r.place("signal_flashlight", (x + 0.04, D - 0.10, tiers[2]), rot=(0, 0, math.pi / 2 + rnd.uniform(-0.2, 0.2)), scale=1.0, fixture="C-back-shelves", anchor=("c", "c", "min"), tag="flashlight")
        x += 0.10
    # 1.6: six coils of rope standing on edge (axis along y), five colours, four layers deep
    gm_by = {}
    cnt_by = {}
    x = xa + 0.20
    for k in range(6):
        ci = k % len(ROPE_COLOURS)
        g = gm_by.setdefault(ci, GM())
        Rin = rnd.uniform(0.05, 0.075)
        rho, turns = 0.0095, 3.2
        Rout = Rin + 2 * rho * turns + rho
        GB.rope_coil(g, (x, D - 0.150, tiers[3] + Rout), Rin, turns, rho, axis="y", mi=0, layers=4)
        cnt_by[ci] = cnt_by.get(ci, 0) + 1
        x += 0.30
    for ci, g in gm_by.items():
        o = g.to_object("rope_coils_%d" % ci, [rope_m[ci]], r.sc, smooth=True)
        r.placed_rec("C-back-shelves", "script:rope_coils", g.extents(), [o.name], tag="coils_%d" % ci, n=cnt_by[ci])
    # 2.0: ten twine reels
    gm = GM()
    for k in range(10):
        GB.twine_reel(gm, xa + 0.07 + k * 0.105, D - 0.09, tiers[4], r=0.045, h=0.11, mi_wood=0, mi_twine=1)
    o = gm.to_object("twine_reels", [reel_wood, twine_m], r.sc)
    r.placed_rec("C-back-shelves", "script:twine_reels", gm.extents(), [o.name], tag="reels", n=10)
    # ---- the counter
    cx0, cx1, cy0, cy1, ch = r.counter("C-back-counter", panels=True)
    brass = r.brass_m
    r.box("counter_brass_edge", cx0, cx1, cy0 - 0.006, cy0 + 0.004, ch - 0.016, ch - 0.002, brass, fixture="C-back-counter")
    drawer_m = r.mat("chart_drawer", rgb8(130, 86, 50), rough=0.5)
    r.box("chart_drawer_front", cx0 + 0.55, cx0 + 1.35, cy0 - 0.012, cy0 - 0.001, 0.58, 0.84, drawer_m, fixture="C-back-counter")
    r.box("chart_drawer_pull", cx0 + 0.89, cx0 + 1.01, cy0 - 0.022, cy0 - 0.012, 0.69, 0.73, brass, fixture="C-back-counter")
    till_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "CashRegister_01") / max(r.dims("CashRegister_01"))
    r.place("CashRegister_01", (cx1 - 0.32, D - 0.02, ch), rot=(0, 0, 0), scale=till_s, fixture="C-back-counter", anchor=("c", "max", "min"))
    for k, xc in enumerate((cx0 + 0.25, cx0 + 0.50, cx0 + 1.60)):
        r.place("seadogs_compass", (xc, D - 0.25 - 0.05 * k, ch), rot=(0, 0, rnd.uniform(-0.6, 0.6)), scale=1.0, fixture="C-back-counter", anchor=("c", "c", "min"), tag="compass")
    lx, ly = cx0 + 1.05, D - 0.30
    ext = r.place("Lantern_01", (lx, ly, ch), rot=(0, 0, 0), scale=1.3, fixture="C-back-counter", anchor=("c", "c", "min"), tag="hurricane_lamp")
    flame_m = r.mat("lamp_flame", rgb8(255, 190, 90), rough=0.4, emit=(1.0, 0.62, 0.22), emit_strength=0.0)
    gm = GM()
    gm.lathe(lx, ly, ch + 0.07, [(0.0, 0.0), (0.006, 0.01), (0.007, 0.03), (0.003, 0.05), (0.0, 0.06)], mi=0, n=10)
    o = gm.to_object("lamp_flame", [flame_m], r.sc, smooth=True)
    r.fixture_rec("C-back-counter", "lamp_flame", gm.extents())
    ll = bpy.data.lights.new("lamp_light", "POINT")
    ll.energy = 0.0
    ll.color = (1.0, 0.62, 0.30)
    ll.shadow_soft_size = 0.02
    lo = bpy.data.objects.new("lamp_light", ll)
    r.sc.collection.objects.link(lo)
    lo.location = (lx, ly - 0.03, ch + 0.10)
    r.lamp = lo
    orig_set_state = r.set_state

    def set_state(state, P, _o=orig_set_state):
        _o(state, P)
        on = state == "night_lit"
        flame_m.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 30.0 if on else 0.0
        lo.data.energy = P.get("lamp", 6.0) if on else 0.0
    r.set_state = set_state
    # ---- the hooks board over the counter: life jackets, a lifebuoy, sou'westers on pegs
    hx0, hx1 = fx["C-back-hooks"]["x"]
    wood = r.mat("hooks_board", rgb8(112, 76, 46), rough=0.6)
    r.box("hooks_board", hx0, hx1, D - 0.030, D - 0.005, 2.04, 2.20, wood, fixture="C-back-hooks")
    pegs = []
    gm = GM()
    jx = [hx0 + 0.30, hx0 + 0.80, hx0 + 1.30]
    jsc = 0.7
    for k, xc in enumerate(jx):
        gm.rod((xc, D - 0.030, 2.12), (xc, D - 0.075, 2.12), 0.007, 0, 8)
        pegs.append(xc)
        jh = r.dims("life_jacket").z * jsc
        r.place("life_jacket", (xc, D - 0.075 - 0.0, 2.12 - 0.02), rot=(0, 0, 0), scale=jsc, fixture="C-back-hooks", anchor=("c", "max", "max"), tag="jacket")
    lsc = 0.8
    lbx = hx0 + 1.80
    gm.rod((lbx, D - 0.030, 2.12), (lbx, D - 0.065, 2.12), 0.007, 0, 8)
    r.place("lifebuoy", (lbx, D - 0.065, 2.12), rot=(math.pi / 2, 0, 0), scale=lsc, fixture="C-back-hooks", anchor=("c", "max", "max"), tag="lifebuoy")
    # sou'westers hang from pegs at the right end
    sg = GM()
    sw_m = [r.mat("oilskin_yellow", rgb8(214, 170, 30), rough=0.35), r.mat("oilskin_seam", rgb8(150, 110, 20), rough=0.5)]
    for k, xc in enumerate((hx1 - 0.18, hx1 - 0.02)):
        gm.rod((xc, D - 0.030, 2.12), (xc, D - 0.070, 2.12), 0.006, 0, 8)
    o = gm.to_object("hooks_pegs", [brass], r.sc)
    r.fixture_rec("C-back-hooks", "hooks_pegs", gm.extents())
    for k, xc in enumerate((hx1 - 0.16, hx1 - 0.02)):
        GB.souwester(sg, xc, D - 0.08, 1.72, s=1.0, mi=0, mi_seam=1, face=-1.0)
    o = sg.to_object("sou_westers", sw_m, r.sc, smooth=True)
    r.placed_rec("C-back-hooks", "script:oilskin_sou_wester", sg.extents(), [o.name], tag="sou_westers", n=2)
    # ---- the left wall: six chart sheets, a tide table card, a board with a flat coil of rope
    xl, xr = -W / 2, W / 2
    titles = ["HARBOUR\nAPPROACHES No.1", "THE WESTERN\nSOUNDS", "NORTH CHANNEL\nTO THE BAR", "INSHORE WATERS\nSOUTH COAST", "THE ESTUARY\nAND ROADS", "OFFSHORE BANKS\nSHEET 4", "TIDE TABLE\nFOR THE MONTH"]
    cp = os.path.join(tex, "charts.png")
    cuv = GB.chart_atlas(cp, [t.split("\n")[0] if t.startswith("TIDE") else t for t in titles[:6]] + ["TIDE TABLE"], cols=4)
    cm = r.image_mat("charts", cp, rough=0.8)
    GEN.TEXTS.extend(["HARBOUR", "APPROACHES No.1", "TIDE TABLE", "FOR THE MONTH"])
    cg = GM()
    cells = [(1.42, 1.65), (1.78, 1.65), (2.14, 1.65), (1.42, 1.15), (1.78, 1.15), (2.14, 1.15), (2.52, 1.70)]
    for k, (yc, zc) in enumerate(cells):
        w_, h_ = (0.30, 0.40)
        uvk = cuv[k]
        cg.box(xl + 0.0030, xl + 0.0050, yc - w_ / 2, yc + w_ / 2, zc - h_ / 2, zc + h_ / 2, 0, uv_front=uvk, front="+x", uv_other=(uvk[0] + 0.01, uvk[1] + 0.01))
    o = cg.to_object("chart_sheets", [cm], r.sc)
    r.placed_rec("C-left-charts", "script:chart_posters", cg.extents(), [o.name], tag="charts", n=7)
    board_m = r.mat("rope_board", rgb8(116, 80, 50), rough=0.6)
    r.box("rope_board", xl + 0.0005, xl + 0.012, 2.40, 2.95, 1.00, 1.50, board_m, fixture="C-left-charts")
    rg = GM()
    Rout = GB.rope_coil(rg, (xl + 0.012 + 0.0105, 2.675, 1.25), 0.045, 3.0, 0.0095, axis="x", mi=0, layers=1)
    o = rg.to_object("rope_flat_coil", [rope_m[0]], r.sc, smooth=True)
    r.fixture_rec("C-left-charts", "rope_flat_coil", rg.extents())
    # ---- the right wall: the pegboard and 24 pieces of hardware, flat
    r.make_pegboard_texture()
    top = r.pegboard_panels("C-right-board", "right")
    hw = GM()
    n_hw = 0
    rows_hw = [(1.88, "block", [0.15 + k * 0.25 for k in range(6)]), (1.62, "shackle", [0.12 + k * 0.19 for k in range(8)]), (1.36, "cleat", [0.20 + k * 0.30 for k in range(5)]),
               (1.12, "shackle", [0.20, 0.55]), (1.12, "chain", [0.95, 1.25, 1.50])]

    def to_wall(x_, y_, z_):
        return (top + y_, 2.8 - x_, z_)          # local (u, -d, z) -> the right wall: out of the board is -x; u runs along -y from the viewer's right
    for z, kind, us in rows_hw:
        for uu in us:
            i0 = len(hw.V)
            if kind == "block":
                GB.wooden_block(hw, 0.0, 0.0, 0.0, s=1.0, mi_wood=0, mi_steel=1)
            elif kind == "shackle":
                GB.shackle(hw, 0.0, 0.0, 0.0, s=1.0, mi=1)
            elif kind == "cleat":
                GB.horn_cleat(hw, 0.0, 0.0, 0.0, s=1.0, mi=1)
            else:
                GB.chain_run(hw, 0.0, 0.0, 0.0, 9, s=1.0, mi=1)
            _map_wall(hw, i0, lambda x_, y_, z_, uu=uu, z=z: to_wall(x_ + uu, y_, z_ + z))
            n_hw += 1
    block_wood = r.mat("block_wood", rgb8(130, 90, 56), rough=0.45)
    o = hw.to_object("rigging_hardware", [block_wood, steel], r.sc)
    r.placed_rec("C-right-board", "script:shackles_blocks", hw.extents(), [o.name], tag="hardware", n=n_hw)
    r.rows["counts"] = {"paint_tins": n_tins, "hardware": n_hw}
    r.notes.append("%d paint tins (target 40), 24 pieces of rigging on the pegboard, life jackets 3 of 4, lifebuoy 1 of 2, sou'westers 2 of 3 on the hooks board (no room for more without one through another); the hurricane lamp is lit in night_lit only" % n_tins)
    r.texts = list(GEN.TEXTS)
    return r


# ---------------------------------------------------------------------------------------------------------------------------------- the window
def display(d):
    """The chandler's window (target `shops.chandler.display`, 12 item rows; bed 3.35 x 0.55; 1.55 high at most). What this does (each a Judgement in NOTES.md):
    lifebuoy leaning on its edge against a timber chock at the glass side (u 0.2 to 1.0); two life jackets and two sou'westers hang from a timber rail at w 1.40 on two cords from the window head (u 1.0 to 2.0:
    jackets behind, hats in front); boots x3 (0.6), Lantern_01 x2, wooden_lantern_01, seadogs_compass x2, oil_tin x4, small_oil_can_01 x3 and the blowtorch on the bed; five coils of rope (natural, blue, orange,
    white, green: swept tubes with ambientCG Rope001), a pyramid of 21 paint tins (6 + 5 + ... + 1). The woven galvanised mesh screens of the night (target `night`) are a night furniture: not in the day glb, not in the lit
    night view. Nothing hangs from the ceiling: the rail hangs from the window's head."""
    _setup()
    import sw_room_gen as RG
    rr = d.RR
    walls = rr["walls"]
    d.start((126, 92, 60), RG._rgb(walls["above"]), RG._rgb(walls["dado"]))
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    tex = d.tex
    GEN.TEXTS.clear()
    GB.fetch_ropes()
    # ---- lifebuoy on a chock
    ext, _ = d.piece("lifebuoy", 0.62, 0.20, 0.0, rot=(math.radians(-12), 0, 0), scale=1.0, tier="bed", tris=None)
    chock = d.mat("chock", rgb8(120, 84, 54), rough=0.7)
    gm = GM()
    gm.box(X(0.62) - 0.10, X(0.62) + 0.10, 0.23, 0.36, 0.0, 0.05, 0)
    ob, _ = d.gm_object("lifebuoy_chock", gm, [chock], "support", "script:crate")
    # ---- the rail with the jackets and hats
    rail_w = 1.40
    rail_m = d.mat("rail_timber", rgb8(120, 84, 54), rough=0.6)
    gm = GM()
    gm.rod((X(0.95), 0.34, rail_w), (X(2.05), 0.34, rail_w), 0.014, 0, 12)
    for xx in (0.98, 2.02):
        gm.rod((X(xx), 0.34, rail_w), (X(xx), 0.34, 1.55), 0.002, 0, 6)
    d.gm_object("rail", gm, [rail_m], "support", "script:crate")
    for k, uc in enumerate((1.20, 1.62)):
        jh = d.dims("life_jacket").z * 0.7
        d.piece("life_jacket", uc, 0.40, rail_w - jh + 0.02, rot=(0, 0, 0), scale=0.7, tier="rail", tris=None)
    sg = GM()
    sw_m = [d.mat("oilskin_yellow", rgb8(214, 170, 30), rough=0.35), d.mat("oilskin_seam", rgb8(150, 110, 20), rough=0.5)]
    for uc in (1.30, 1.72):
        GB.souwester(sg, X(uc), 0.20, rail_w - 0.20, s=1.0, mi=0, mi_seam=1, face=-1.0)
    d.gm_object("sou_westers", sg, sw_m, "scripted", "script:oilskin_sou_wester", tier="rail", smooth=True)
    # ---- the bed: boots, lanterns, compasses, oil tins, cans, blowtorch
    for k, uc in enumerate((0.35, 0.75, 1.15)):
        d.piece("rubber_boots", uc, 0.42, 0.0, rot=(0, 0, 0), scale=0.5, tier="bed", tris=None)
    for k, uc in enumerate((1.35, 1.60)):
        d.piece("Lantern_01", uc, 0.34, 0.0, rot=(0, 0, rnd.uniform(-0.3, 0.3)), scale=1.0, tier="bed", tris=None)
    d.piece("wooden_lantern_01", 1.95, 0.32, 0.0, rot=(0, 0, 0.3), scale=1.0, tier="bed", tris=None)
    for k, uc in enumerate((2.45, 2.70)):
        d.piece("seadogs_compass", uc, 0.18, 0.0, rot=(0, 0, rnd.uniform(-0.6, 0.6)), scale=1.0, tier="bed", tris=None)
    for k, uc in enumerate((0.35, 0.50, 0.65, 0.80)):
        d.piece("oil_tin", uc, 0.14, 0.0, rot=(0, 0, math.pi / 2), scale=1.0, tier="bed", tris=None)
    for k, uc in enumerate((1.35, 1.65, 1.95)):
        d.piece("small_oil_can_01", uc, 0.12, 0.0, rot=(0, 0, 0), scale=1.0, tier="bed", tris=None)
    d.piece("brass_blowtorch", 0.98, 0.14, 0.0, rot=(0, 0, math.pi / 2), scale=1.0, tier="bed", tris=None)
    # ---- coils of rope: two big on the bed, two small on them, one small in front
    rm = []
    for i, c in enumerate(ROPE_COLOURS):
        pth = os.path.join(tex, "rope_%d.png" % i)
        GB.rope_png(pth, c, which=1, size=512)
        rm.append(d.image_mat("rope_%d" % i, pth, rough=0.9))
    coils = [(2.22, 0.36, 0.16, 0.0, 0), (2.58, 0.36, 0.16, 0.0, 1), (2.22, 0.36, 0.09, 0.034, 2), (2.58, 0.36, 0.09, 0.034, 3), (2.40, 0.10, 0.085, 0.0, 4)]
    for k, (uc, vc, Rin, zc, ci) in enumerate(coils):
        g = GM()
        Ro = GB.rope_coil(g, (X(uc), vc, 0.0 + zc + 0.0095), Rin * 0.55, 2.4 if Rin > 0.12 else 1.8, 0.0095, axis="z", mi=0, layers=2 if Rin > 0.12 else 1)
        d.gm_object("rope_coil_%d" % k, g, [rm[ci]], "scripted", "script:rope_coils", tier="bed", smooth=True)
    # ---- the pyramid of 21 paint tins
    tp = os.path.join(tex, "marine_tins.png")
    tuv = GB.tin_atlas(tp, TIN_DESIGNS, tile=(256, 128), cols=4)
    tin_label = d.image_mat("marine_tin_labels", tp, rough=0.5)
    metal = d.mat("tin_metal", rgb8(168, 168, 164), rough=0.35, metal=0.85)
    r_t, h_t = 0.0475, 0.086
    gm = GM()
    u_c = 3.03
    for row in range(6):
        nrow = 6 - row
        x_start = X(u_c) - nrow * 2 * r_t * 1.02 / 2
        for i in range(nrow):
            GB.paint_tin(gm, x_start + (i + 0.5) * 2 * r_t * 1.02, 0.42, row * h_t, r_t, h_t, tuv[(row * 3 + i) % len(TIN_DESIGNS)], n=16, bail=False)
    d.gm_object("paint_tin_pyramid", gm, [metal, tin_label], "scripted", "script:paint_tin_pyramid", tier="bed")
    back_m = d.mat("pyramid_board", rgb8(150, 140, 120), rough=0.8)
    gm = GM()
    gm.box(X(u_c - 0.31), X(u_c + 0.31), 0.50, 0.515, 0.0, 0.54, 0)
    d.gm_object("pyramid_backing", gm, [back_m], "support", "script:backing_board")
    # ---- price cards
    texts = ["LIFEBUOY\n£12.50", "JACKETS\n£9.95", "ROPE\n85p a metre", "BOOTS\n£6.75", "LAMPS\n£4.20", "COMPASS\n£5.50", "OIL\n£1.60", "PAINT\n£3.45", "SOU'WESTERS\n£2.95", "BLOWTORCH\n£7.25"]
    path = os.path.join(tex, "price_cards.png")
    uvs = GEN.card_atlas(path, texts, cols=4, tile=(256, 128), size=40)
    pm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    spots = [(0.35, 0.03), (1.50, 0.50), (2.40, 0.03), (0.35, 0.03), (1.47, 0.03), (2.58, 0.03), (0.65, 0.03), (3.03, 0.03), (1.72, 0.50), (0.98, 0.03)]
    for k, (uc, vv) in enumerate(spots):
        d.price_card(uc, vv, 0.0, k, uvs, pm)
    d.display_texts = list(GEN.TEXTS) + [t.replace("\n", " ") for t in texts]
