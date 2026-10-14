"""The grocer (east_parade bay 5, "grocer", FAMILY GROCER): the room's layout and the window display (14 October 2026, batch B). Read from `shops.grocer.room` and `.display` in target.json; every choice the
target left open is stated in the docstrings (each a Judgement in NOTES.md and a `Changes after the build` line).

Content rule for this shop: no drink anywhere. The target's goods list the grocer's "tea and sugar" packets and "orange squash" bottles; both are changed here (dry goods and condiments only: sugar, flour,
oats, rice, pasta, custard, dried fruit; washing-up liquid, brown sauce, malt vinegar, salad cream), because a label of a drink is a label of a drink; no tin, jar, bottle or packet shows a bet, a barcode, a child or a
real maker (every name below is the project's own).
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

# ---- the project's own makers and products (none is a real firm; none is a drink)
TIN_DESIGNS = [("HOLMFIELD", "BAKED BEANS", "in tomato sauce", (196, 70, 44), (250, 240, 204), (250, 240, 204)),
               ("PENNYWELL", "TOMATO SOUP", "condensed", (186, 52, 52), (246, 240, 222), (246, 240, 222)),
               ("DALTREY", "GARDEN PEAS", "", (60, 130, 72), (250, 246, 226), (250, 246, 226)),
               ("KINGSMEAD", "SWEETCORN", "", (230, 190, 52), (70, 50, 30), (70, 50, 30)),
               ("HOLMFIELD", "SARDINES", "in oil", (44, 84, 142), (244, 238, 220), (240, 200, 84)),
               ("ASHBY", "CORNED BEEF", "", (150, 62, 42), (250, 236, 204), (250, 236, 204)),
               ("PENNYWELL", "PEACH SLICES", "in syrup", (230, 142, 52), (255, 250, 232), (255, 250, 232)),
               ("DALTREY", "PINEAPPLE RINGS", "", (240, 202, 62), (120, 44, 32), (120, 44, 32)),
               ("KINGSMEAD", "RICE PUDDING", "", (236, 230, 212), (60, 92, 142), (60, 92, 142)),
               ("ASHBY", "CHOPPED TOMATOES", "", (192, 52, 42), (250, 240, 212), (250, 240, 212)),
               ("HOLMFIELD", "MUSHY PEAS", "", (104, 152, 92), (250, 246, 232), (250, 246, 232)),
               ("PENNYWELL", "PINK SALMON", "", (212, 102, 92), (255, 246, 232), (255, 246, 232))]
PACKET_DESIGNS = [("MEADOWBANK", "GRANULATED\nSUGAR", "1 kg", (236, 232, 214), (40, 72, 142), (200, 60, 60), "star"),
                  ("STANWICK", "PLAIN FLOUR", "1.5 kg", (230, 222, 196), (120, 60, 40), (60, 100, 160), "ear"),
                  ("STANWICK", "SELF-RAISING\nFLOUR", "1.5 kg", (222, 200, 150), (150, 40, 40), (60, 100, 160), "ear"),
                  ("FERNLEY", "PORRIDGE\nOATS", "500 g", (70, 120, 150), (246, 240, 222), (240, 200, 80), "ear"),
                  ("FERNLEY", "LONG GRAIN\nRICE", "500 g", (220, 180, 80), (60, 40, 30), (60, 110, 60), "leaf"),
                  ("TRENTHAM", "SPAGHETTI", "500 g", (200, 62, 50), (246, 236, 212), (240, 200, 80), "wave"),
                  ("TRENTHAM", "MACARONI", "500 g", (60, 120, 92), (246, 240, 222), (240, 200, 80), "wave"),
                  ("OAKHAM", "CORNFLOUR", "250 g", (236, 232, 214), (40, 100, 72), (220, 60, 60), "sun"),
                  ("OAKHAM", "CUSTARD\nPOWDER", "300 g", (240, 212, 84), (150, 40, 40), (60, 60, 140), "sun"),
                  ("MEADOWBANK", "SEA SALT", "750 g", (100, 132, 172), (246, 244, 236), (240, 240, 240), "drop"),
                  ("LANGDALE", "SULTANAS", "500 g", (150, 72, 52), (250, 236, 204), (240, 192, 84), "sun"),
                  ("LANGDALE", "CURRANTS", "500 g", (72, 52, 82), (250, 240, 222), (230, 192, 92), "star")]
JAR_DESIGNS = [("STRAWBERRY JAM", "KINGSMEAD", (162, 32, 42), (112, 22, 32)), ("MARMALADE", "KINGSMEAD", (214, 142, 42), (162, 92, 22)), ("HONEY", "FERNLEY", (228, 172, 52), (192, 132, 32)),
               ("PICCALILLI", "ASHBY", (202, 172, 52), (122, 112, 32)), ("PICKLED ONIONS", "ASHBY", (222, 216, 182), (192, 182, 142)), ("BLACKCURRANT JAM", "KINGSMEAD", (62, 22, 52), (32, 12, 32))]
BOTTLE_DESIGNS = [("FERNSIDE", "WASHING-UP\nLIQUID", (40, 110, 70), (70, 150, 90)), ("LANGDALE", "BROWN\nSAUCE", (110, 40, 30), (150, 60, 40)),
                  ("ASHBY", "MALT\nVINEGAR", (70, 70, 40), (100, 100, 60)), ("LANGDALE", "SALAD\nCREAM", (150, 110, 30), (210, 170, 70))]
BOTTLE_COLOURS = [(66, 150, 96), (70, 34, 22), (124, 112, 70), (232, 226, 200)]          # the bottle's own colour: green plastic, brown glass, pale brown glass, cream glass


def _setup():
    global rgb8
    import sw_room as S
    rgb8 = S.rgb8


def _tin(gm, cx, cy, z0, r, h, luv, n=14):
    prof = [(0.0, 0.0), (r * 0.94, 0.0), (r, 0.004), (r, h - 0.010), (r * 1.035, h - 0.010), (r * 1.035, h - 0.002), (r * 0.90, h - 0.002), (r * 0.90, h - 0.006), (0.0, h - 0.006)]
    gm.lathe(cx, cy, z0, prof, mi=0, n=n, label=(2, 3), mi_label=1, label_uv=luv)


def _scale_picture(path):
    """The counter scale's dial: a brass plate with a white dial, ticks, the numbers 0 to 14 (pounds) and a red needle. No maker's name."""
    from sw_gen import font
    s = 512
    im = Image.new("RGB", (s, s), (170, 130, 62))
    d = ImageDraw.Draw(im)
    d.ellipse([20, 20, s - 20, s - 20], fill=(238, 234, 222), outline=(70, 50, 30), width=6)
    cx = cy = s // 2
    f = font("oswald", 34)
    for k in range(0, 57):
        a = math.radians(-150 + 300 * k / 56.0)
        r0 = s * 0.42 if k % 4 else s * 0.38
        r1 = s * 0.455
        d.line([(cx + r0 * math.sin(a), cy - r0 * math.cos(a)), (cx + r1 * math.sin(a), cy - r1 * math.cos(a))], fill=(40, 40, 50), width=3 if k % 4 else 5)
        if k % 4 == 0:
            t = str(k // 4)
            rr = s * 0.30
            d.text((cx + rr * math.sin(a) - d.textlength(t, font=f) / 2, cy - rr * math.cos(a) - 17), t, font=f, fill=(40, 40, 50))
    a = math.radians(-150 + 300 * 22 / 56.0)
    d.polygon([(cx - 8 * math.cos(a), cy - 8 * math.sin(a)), (cx + 8 * math.cos(a), cy + 8 * math.sin(a)), (cx + s * 0.40 * math.sin(a), cy - s * 0.40 * math.cos(a))], fill=(190, 30, 30))
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(60, 50, 40))
    f2 = font("oswald", 26)
    d.text((cx - d.textlength("LB", font=f2) / 2, cy + 70), "LB", font=f2, fill=(60, 50, 50))
    im.save(path)
    GEN.TEXTS.extend(["LB"] + [str(k) for k in range(15)])


# ---------------------------------------------------------------------------------------------------------------------------------- the room
def room(r):
    """The grocer's room (target `shops.grocer.room`: fixtures G-*). What the target leaves open, and what this does:

    gantry G-back-gantry (x -2.6 to 0.1, 0.25 deep): five tiers (board tops 0.45, 0.85, 1.25, 1.65, 2.05). Floor: three plastic_crate_03 at their own size (0.265 deep: inside the 0.30 rule; crate_02 is 0.41 deep) loaded with
    yellow_onion (the target loads them with potatoes, which are Sketchfab scans waiting for Jafar's login: onions are a CC0 model and a grocer's crate holds either); 0.45: tins two deep along the whole run; 0.85:
    two wicker_basket_01 and three sets of hamburger_buns at 0.9 (two sets lie across the baskets' rims, the third on the board), then tins; 1.25: tins and packets; 1.65: packets and tins; 2.05: tins and packets.
    The tins (12 designs) and packets (12) are the project's own makers' (HOLMFIELD, PENNYWELL, DALTREY, KINGSMEAD, ASHBY; MEADOWBANK, STANWICK, FERNLEY, TRENTHAM, OAKHAM, LANGDALE): no drink on any label.
    counter G-back-counter (x 0.2 to 2.6, 0.6 deep, 1.0 high, panelled): CashRegister_01 at 0.42 with its dial maker mark blanked, a counter scale (script: a brass and enamel scale with a dial picture).
    shelves G-back-shelves-right (x 0.2 to 2.6, 0.20 deep, tiers 1.40 and 1.78) ON the counter's top: jars (six products, two rows deep) and bottles (washing-up liquid, brown sauce, malt vinegar, salad cream: the
    target's "squash" is a drink and is out).
    left wall G-left-tins and right wall G-right-tins (0.10 deep, 4 tiers z 0.70 to 1.75, y 1.0 to 3.0): tins on the left, dry-goods packets on the right (the target's "tea" packets are out: a label of a drink).
    the clock: on the right wall above the right unit (the gantry has no clear wall above its top tier: 0.35 between the top board and the ceiling is less than the clock's 0.30 plus its hang).
    floor: brown linoleum (linoleum_brown), a darker worn path to the counter (decal). The till's glow lamp (night_dark): a small warm point light over the till."""
    _setup()
    import sw_room_gen as RG
    import bpy
    D, W = RG.D, RG.W
    rr = r.RR
    fx = r.fxd
    rnd = r.rnd
    tex = r.tex
    GEN.TEXTS.clear()
    metal = r.mat("tin_metal", rgb8(168, 168, 164), rough=0.35, metal=0.85)
    tp = os.path.join(tex, "food_tins.png")
    tuv = GB.tin_atlas(tp, TIN_DESIGNS, tile=(256, 128), cols=4)
    tin_label = r.image_mat("food_tin_labels", tp, rough=0.5)
    pk = os.path.join(tex, "food_packets.png")
    puv = GB.packet_atlas(pk, PACKET_DESIGNS, tile=(180, 280), cols=4)
    pack_m = r.image_mat("food_packets", pk, rough=0.7)
    # ---- the gantry
    gx0, gx1 = fx["G-back-gantry"]["x"]
    tiers = fx["G-back-gantry"]["tiers"]
    r.shelf_unit("G-back-gantry", [(z, gx0 + 0.015, gx1 - 0.015) for z in tiers], depth=fx["G-back-gantry"]["depth_m"])
    xa, xb = gx0 + 0.04, gx1 - 0.04
    shelf_d = fx["G-back-gantry"]["depth_m"]
    n_tins, n_pk = 0, 0

    def tins_row(gm, x0, x1, z, rows_y, kinds):
        """Tins along [x0, x1] in rows at the y of `rows_y` (back row first): sizes mixed, labels random, a few missing and a few pulled forward."""
        n = 0
        for ri, yc in enumerate(rows_y):
            x = x0
            while True:
                rad, hh = rnd.choice(kinds)
                if x + 2 * rad * 1.035 > x1:
                    break
                if rnd.random() < 0.035:
                    x += 2 * rad * 1.035 + 0.004                   # a gap: a tin sold
                    continue
                pull = 0.018 if (ri == len(rows_y) - 1 and rnd.random() < 0.06) else 0.0
                _tin(gm, x + rad * 1.035, yc - pull, z, rad, hh, tuv[rnd.randrange(len(TIN_DESIGNS))])
                n += 1
                x += 2 * rad * 1.035 + 0.003
        return n

    def packets_row(gm, x0, x1, z, rows_y):
        n = 0
        for ri, yc in enumerate(rows_y):
            x = x0
            while True:
                w_, d_, h_ = rnd.uniform(0.088, 0.104), rnd.uniform(0.042, 0.052), rnd.uniform(0.150, 0.196)
                if x + w_ > x1:
                    break
                k = rnd.randrange(len(PACKET_DESIGNS))
                uv = puv[k]
                gm.box(x, x + w_, yc - d_ / 2, yc + d_ / 2, z, z + h_, 0, uv_front=uv, uv_other=(uv[0] + 0.004, uv[1] + 0.5 * (uv[3] - uv[1])))
                n += 1
                x += w_ + rnd.uniform(0.003, 0.008)
        return n
    tin_kinds = [(0.0375, 0.100), (0.0425, 0.110), (0.045, 0.125), (0.0375, 0.078), (0.040, 0.095)]
    row_t = [D - 0.052, D - 0.140]
    row_p = [D - 0.035, D - 0.095]
    plan = {0.45: [("tins", xa, xb)], 0.85: [("baskets", xa, xa + 1.10), ("tins", xa + 1.12, xb)], 1.25: [("packets", xa, xb)],
            1.65: [("packets", xa, xa + 1.30), ("tins", xa + 1.32, xb)], 2.05: [("tins", xa, xa + 1.30), ("packets", xa + 1.32, xb)]}
    for z in tiers:
        gt, gp = GM(), GM()
        nt = npk = 0
        for kind, a_, b_ in plan[z]:
            if kind == "tins":
                nt += tins_row(gt, a_, b_, z, row_t, tin_kinds)
            elif kind == "packets":
                npk += packets_row(gp, a_, b_, z, row_p)
        n_tins += nt
        n_pk += npk
        if gt.V:
            o = gt.to_object("gantry_tins_%.2f" % z, [metal, tin_label], r.sc)
            r.placed_rec("G-back-gantry", "script:tins", gt.extents(), [o.name], tag="tins_%.2f" % z, n=nt)
        if gp.V:
            o = gp.to_object("gantry_packets_%.2f" % z, [pack_m], r.sc)
            GB.chamfer(o, 0.0025, 2)
            r.placed_rec("G-back-gantry", "script:packets", gp.extents(), [o.name], tag="packets_%.2f" % z, n=npk)
    # baskets with rolls on the 0.85 board (wicker_basket_01 at 0.9, hamburger_buns at 0.9: real size; the rolls lie across the baskets' rims, the third set beside them on the board)
    zb = 0.85
    bsc = 0.9
    bh = r.dims("wicker_basket_01").z * bsc
    bw_ = r.dims("wicker_basket_01").x * bsc
    bxs = [xa + 0.01 + bw_ / 2, xa + 0.02 + bw_ * 1.5]
    for xc in bxs:
        r.place("wicker_basket_01", (xc, D - 0.005, zb), rot=(0, 0, 0), scale=bsc, fixture="G-back-gantry", anchor=("c", "max", "min"), tag="basket")
    bun_s = 0.9
    for xc in bxs:
        r.place("hamburger_buns", (xc, D - 0.005 - 0.1325, zb + bh + 0.001), rot=(0, 0, 0), scale=bun_s, fixture="G-back-gantry", anchor=("c", "c", "min"), tag="rolls")
    r.place("hamburger_buns", (xa + 0.03 + bw_ * 2 + 0.19, D - 0.075, zb), rot=(0, 0, 0), scale=bun_s, fixture="G-back-gantry", anchor=("c", "c", "min"), tag="rolls")
    # three crates of onions on the floor under the first board (plastic_crate_03 at its own size: crate_02 is 0.41 deep and the gantry's goods stand at most 0.30 off the wall)
    cs = 1.0
    for k, xc in enumerate((gx0 + 0.30, gx0 + 0.86, gx0 + 1.42)):
        ext = r.place("plastic_crate_03", (xc, D - 0.005, 0.0), rot=(0, 0, 0), scale=cs, fixture="G-back-gantry", anchor=("c", "max", "min"), tag="crate")
        zt = ext[4] + 0.034
        cx_, cy_ = (ext[0] + ext[1]) / 2, (ext[2] + ext[3]) / 2
        for iy in range(3):
            for ix in range(4):
                r.place("yellow_onion", (cx_ + (ix - 1.5) * 0.085, cy_ + (iy - 1.0) * 0.075, zt), rot=(0, 0, rnd.uniform(0, 6.28)), scale=1.0, fixture="G-back-gantry", anchor=("c", "c", "min"), tag="onion")
        for iy in range(2):
            for ix in range(3):
                r.place("yellow_onion", (cx_ + (ix - 1.0) * 0.085, cy_ + (iy - 0.5) * 0.075, zt + 0.080), rot=(0, 0, rnd.uniform(0, 6.28)), scale=0.92, fixture="G-back-gantry", anchor=("c", "c", "min"), tag="onion")
    # ---- the counter, the till, the scale
    cx0, cx1, cy0, cy1, ch = r.counter("G-back-counter", panels=True)
    till_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "CashRegister_01") / max(r.dims("CashRegister_01"))
    r.place("CashRegister_01", (cx1 - 0.30, D - 0.02, ch), rot=(0, 0, 0), scale=till_s, fixture="G-back-counter", anchor=("c", "max", "min"))
    sp = os.path.join(tex, "scale_dial.png")
    _scale_picture(sp)
    sm = r.image_mat("scale_dial", sp, rough=0.45)
    enamel = r.mat("scale_enamel", rgb8(222, 218, 204), rough=0.3)
    brass = r.brass_m
    gm = GM()
    sx_, sy_ = cx1 - 0.78, D - 0.30
    gm.box(sx_ - 0.14, sx_ + 0.14, sy_ - 0.17, sy_ + 0.17, ch, ch + 0.045, 0)                         # the enamel base
    gm.box(sx_ - 0.05, sx_ + 0.05, sy_ - 0.04, sy_ + 0.04, ch + 0.045, ch + 0.30, 0)                   # the column
    gm.box(sx_ - 0.115, sx_ + 0.115, sy_ - 0.05, sy_ + 0.05, ch + 0.30, ch + 0.53, 1, uv_front=(0.0, 0.0, 1.0, 1.0), uv_other=(0.02, 0.02))       # the head, the dial on its front
    gm.lathe(sx_, sy_ + 0.01, ch + 0.53, [(0.0, 0.0), (0.10, 0.0), (0.10, 0.012), (0.0, 0.012)], mi=2, n=24)                                    # the brass cap
    gm.lathe(sx_, sy_ + 0.01, ch + 0.542, [(0.0, 0.0), (0.02, 0.0), (0.02, 0.06), (0.15, 0.062), (0.15, 0.072), (0.0, 0.072)], mi=2, n=24)       # the pan on its stem
    o = gm.to_object("counter_scale", [enamel, sm, brass], r.sc)
    r.placed_rec("G-back-counter", "script:counter_scale", gm.extents(), [o.name], tag="scale", n=1)
    # ---- the shelves over the counter: jars, two rows deep, and bottles
    sx0, sx1 = cx0 + 0.03, cx1 - 0.03
    sx_low = cx1 - 0.98                                   # the lower board ends where the scale and the till begin: they stand under the upper board only (as the tea rooms' till)
    r.shelf_unit("G-back-shelves-right", [(1.40, sx0, sx_low), (1.78, sx0, sx1)], depth=fx["G-back-shelves-right"]["depth_m"], bottom=ch)
    jl = os.path.join(tex, "jar_labels.png")
    juv = GB.jar_labels(jl, [(p_, m_, c1, c2) for p_, m_, c1, c2 in JAR_DESIGNS], tile=(256, 256), cols=3)
    jar_lab = r.image_mat("jar_labels", jl, rough=0.5)
    lid_m = r.mat("jar_lid", rgb8(196, 160, 60), rough=0.35, metal=0.8)
    bl = os.path.join(tex, "grocer_bottle_labels.png")
    buv = GB.bottle_atlas(bl, [(m_, p_, c_, b_) for m_, p_, c_, b_ in BOTTLE_DESIGNS])
    bot_lab = r.image_mat("grocer_bottle_labels", bl, rough=0.5)
    n_jar = n_bot = 0
    for z in (1.40, 1.78):
        zt = z
        sx_end = sx_low if z < 1.5 else sx1
        gjs = [GM() for _ in JAR_DESIGNS]
        gbs = [GM() for _ in BOTTLE_DESIGNS]
        cj = [0] * len(JAR_DESIGNS)
        cb = [0] * len(BOTTLE_DESIGNS)
        x = sx0 + 0.03
        fill = 0
        while x < sx_end - 0.08:
            if fill % 3 == 2:
                bi = rnd.randrange(len(BOTTLE_DESIGNS))
                rb, hb = 0.030, rnd.choice((0.19, 0.21))
                GB.bottle(gbs[bi], x + rb, D - 0.06, zt, rb, hb, mi=0, mi_cap=1, label=(3, 4), label_mi=2, label_uv=buv[bi], n=20)
                cb[bi] += 1
                x += 2 * rb + 0.012
            else:
                for row_y in (D - 0.05, D - 0.128):
                    if x + 0.075 > sx_end - 0.03:
                        break
                    ji = rnd.randrange(len(JAR_DESIGNS))
                    contents_uv, label_uv = juv[ji]
                    GB.jar(gjs[ji], x + 0.0375, row_y, zt, 0.0375, 0.115, 0, 1, label_uv, 2, n=20)
                    cj[ji] += 1
                x += 0.080
            fill += 1
        for ji, gmj in enumerate(gjs):
            if not gmj.V:
                continue
            fill_m = r.mat("jar_fill_%d" % ji, rgb8(*JAR_DESIGNS[ji][2]), rough=0.18)
            o = gmj.to_object("jars_%d_%.2f" % (ji, z), [fill_m, jar_lab, lid_m], r.sc, smooth=True)
            r.placed_rec("G-back-shelves-right", "script:jars", gmj.extents(), [o.name], tag="jars_%d_%.2f" % (ji, z), n=cj[ji])
            n_jar += cj[ji]
        for bi, gmb in enumerate(gbs):
            if not gmb.V:
                continue
            bm_ = r.mat("bottle_body_%d" % bi, rgb8(*BOTTLE_COLOURS[bi]), rough=0.12)
            cap_m = r.mat("bottle_cap_%d" % bi, rgb8(236, 232, 220), rough=0.4)
            o = gmb.to_object("bottles_%d_%.2f" % (bi, z), [bm_, cap_m, bot_lab], r.sc, smooth=True)
            r.placed_rec("G-back-shelves-right", "script:bottles", gmb.extents(), [o.name], tag="bottles_%d_%.2f" % (bi, z), n=cb[bi])
            n_bot += cb[bi]
    # ---- the side walls: a shallow shelf unit of tins on the left, one of packets on the right
    xl, xr = -W / 2, W / 2
    wood = r.mat("side_shelf", rgb8(120, 84, 54), rough=0.6)
    back = r.mat("side_shelf_back", rgb8(150, 108, 70), rough=0.7)

    def side_unit(fid, side, kind):
        f = fx[fid]
        y0, y1 = f["y"]
        z0, z1 = f["z"]
        tz = f["tiers"]
        dep = f["depth_m"]
        sgn = 1.0 if side == "left" else -1.0
        xw = xl if side == "left" else xr                         # the wall
        xa_ = xw if side == "left" else xw - dep
        xb_ = xw + dep if side == "left" else xw
        r.box("%s_back" % fid, xw if side == "left" else xw - 0.006, xw + 0.006 if side == "left" else xw, y0, y1, z0, z1, back, fixture=fid)
        xa_ = xw + 0.006 if side == "left" else xw - dep
        xb_ = xw + dep if side == "left" else xw - 0.006
        for z in tz:
            r.box("%s_board_%.2f" % (fid, z), xa_, xb_, y0 + 0.03, y1 - 0.03, z - 0.022, z, wood, fixture=fid)
        for yy in (y0 + 0.015, y1 - 0.015):
            r.box("%s_post_%.2f" % (fid, yy), xa_, xb_, yy - 0.015, yy + 0.015, z0, tz[-1], wood, fixture=fid)
        gm = GM()
        gp = GM()
        n = 0
        for z in tz:
            y = y0 + 0.04
            while True:
                if kind == "tins":
                    rad, hh = rnd.choice(((0.0375, 0.100), (0.0375, 0.078), (0.0375, 0.115)))
                    if y + 2 * rad * 1.035 > y1 - 0.03:
                        break
                    xc = (xw + 0.006 + rad * 1.035 + 0.004) if side == "left" else (xw - 0.006 - rad * 1.035 - 0.004)
                    # tins stand with their axis vertical; the lathe is about (cx, cy): the wall runs along y here
                    _tin(gm, xc, y + rad * 1.035, z, rad, hh, tuv[rnd.randrange(len(TIN_DESIGNS))])
                    y += 2 * rad * 1.035 + 0.003
                    n += 1
                else:
                    w_, d_, h_ = rnd.uniform(0.088, 0.104), 0.046, rnd.uniform(0.150, 0.190)
                    if y + w_ > y1 - 0.03:
                        break
                    uv = puv[rnd.randrange(len(PACKET_DESIGNS))]
                    # a packet standing on edge, its face toward the room: the face is the wall's +x (left) or -x (right) side
                    if side == "left":
                        xa2 = xw + 0.006 + 0.004
                        gp.box(xa2, xa2 + d_, y, y + w_, z, z + h_, 0, uv_front=uv, front="+x", uv_other=(uv[0] + 0.004, uv[1] + 0.5 * (uv[3] - uv[1])))
                    else:
                        xb2 = xw - 0.006 - 0.004
                        gp.box(xb2 - d_, xb2, y, y + w_, z, z + h_, 0, uv_front=uv, front="-x", uv_other=(uv[0] + 0.004, uv[1] + 0.5 * (uv[3] - uv[1])))
                    y += w_ + rnd.uniform(0.003, 0.007)
                    n += 1
        if gm.V:
            o = gm.to_object("%s_tins" % fid, [metal, tin_label], r.sc)
            r.placed_rec(fid, "script:tins", gm.extents(), [o.name], tag="side_tins", n=n)
        if gp.V:
            o = gp.to_object("%s_packets" % fid, [pack_m], r.sc)
            GB.chamfer(o, 0.0025, 2)
            r.placed_rec(fid, "script:packets", gp.extents(), [o.name], tag="side_packets", n=n)
        return n
    n_left = side_unit("G-left-tins", "left", "tins")
    n_right = side_unit("G-right-tins", "right", "packets")
    # the clock, on the right wall above the right unit
    ck_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "wall_clock") / max(r.dims("wall_clock"))
    r.place("wall_clock", (xr - 0.022, 2.0, 2.17), rot=(0, 0, -math.pi / 2), scale=ck_s, fixture="G-right-tins", anchor=("max", "c", "c"), clock=r.next_clock(), tag="clock")
    # ---- the floor: a darker worn path to the counter (a decal) and the till's glow lamp
    wp = os.path.join(tex, "worn_path.png")
    GB.worn_path_png(wp, shift=0.6, seed=9)
    GB.floor_decal(r, "worn_path", wp, -0.5, 2.2, 0.5, 3.8, fixture="G-floor")
    ld = bpy.data.lights.new("till_glow", "POINT")
    ld.energy = 0.0
    ld.color = (1.0, 0.72, 0.45)
    ld.shadow_soft_size = 0.04
    po_ = bpy.data.objects.new("till_glow", ld)
    r.sc.collection.objects.link(po_)
    po_.location = (cx1 - 0.40, D - 0.30, ch + 0.50)
    r.pilot = po_
    r.pilot_w = 5.0
    r.rows["counts"] = {"gantry_tins": n_tins, "gantry_packets": n_pk, "jars": n_jar, "bottles": n_bot, "left_tins": n_left, "right_packets": n_right}
    r.notes.append("tins %d and packets %d on the gantry (target 160 and 90), %d jars and %d bottles on the counter's shelves (24 and 12), %d tins on the left unit (40) and %d packets on the right (30): the units are filled, not counted out; no drink on any label" % (n_tins, n_pk, n_jar, n_bot, n_left, n_right))
    r.texts = list(GEN.TEXTS)
    return r


# ---------------------------------------------------------------------------------------------------------------------------------- the window
def display(d):
    """The grocer's window (target `shops.grocer.display`, 14 item rows; bed 4.294 x 0.55; 1.45 high at most). The target's three-tier stand and its zones overlap in volume and give the crates and the pyramids
    the same footprint; what this does (each a Judgement in NOTES.md):
    levels: the bed (the first tier, w 0); step A, a timber bank 0.18 high at the back (v 0.38 to 0.55) under the jars (u 1.55 to 3.15); step B, 0.36 high (v 0.45 to 0.55), three plinths under the three
    tin pyramids (28 tins each: 7 + 6 + ... + 1, one tin deep, a backing board behind each).
    bed, left to right: three plastic_crate_02 at 0.6 (apples heaped: 40 in all), a wicker_basket_02 with two sets of rolls (hamburger_buns), two plastic_crate_03 at 0.9 with the lemons (12), a low timber tray of 15
    onions, a tray of 30 tomatoes (script: glossy red flattened spheres with a calyx, one try), a crate of two bunches of bananas at 0.9 (the third does not fit at real size: two bunches fill the crate's 0.5 depth); every Poly Haven piece at 0.9 to 1.1 of its real size (DSP-06).
    PENDING, Sketchfab scans (Jafar's login): cabbage x4, potato x20, satsuma x12, pear x6 (the target's script:cabbage_potato_satsuma): not modelled, no stand-in; the window carries what has a CC0 model.
    price cards: 14, in front of each group, the project's own lettering: no drink, no brand."""
    _setup()
    import sw_room_gen as RG
    rr = d.RR
    walls = rr["walls"]
    d.start((130, 100, 66), RG._rgb(walls["above"]), RG._rgb(walls["dado"]))         # a stained deal bed
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    tex = d.tex
    GEN.TEXTS.clear()
    timber = d.mat("stand_timber", rgb8(140, 100, 62), rough=0.7)
    # ---- the stand: step A (jars) and three plinths (pyramids)
    gm = GM()
    gm.box(X(1.55), X(3.15), 0.38, 0.55, 0.0, 0.18, 0)
    ob, _ = d.gm_object("tiered_stand_a", gm, [timber], "scripted", "script:tiered_stand")
    GB.chamfer(ob, 0.003, 2)
    py_us = (0.50, 2.30, 3.75)               # the pyramids' centres
    for k, uc in enumerate(py_us):
        gm = GM()
        gm.box(X(uc - 0.37), X(uc + 0.37), 0.45, 0.55, 0.0, 0.36, 0)
        ob, _ = d.gm_object("tiered_stand_b%d" % k, gm, [timber], "scripted", "script:tiered_stand")
        GB.chamfer(ob, 0.003, 2)
    # ---- the pyramids: 28 tins each, one deep, a backing board
    tp = os.path.join(tex, "food_tins.png")
    tuv = GB.tin_atlas(tp, TIN_DESIGNS, tile=(256, 128), cols=4)
    tin_label = d.image_mat("food_tin_labels", tp, rough=0.5)
    metal = d.mat("tin_metal", rgb8(168, 168, 164), rough=0.35, metal=0.85)
    back_m = d.mat("pyramid_board", rgb8(150, 140, 120), rough=0.8)
    r_t, h_t = 0.0475, 0.086
    k_lab = 0
    for pi_, uc in enumerate(py_us):
        gm = GM()
        for row in range(7):
            nrow = 7 - row
            x_start = X(uc) - nrow * 2 * r_t * 1.02 / 2
            for i in range(nrow):
                cx = x_start + (i + 0.5) * 2 * r_t * 1.02
                _tin(gm, cx, 0.488, 0.36 + row * h_t, r_t, h_t, tuv[(k_lab + i + row) % len(TIN_DESIGNS)], n=16)
        k_lab += 5
        d.gm_object("tin_pyramid_%d" % pi_, gm, [metal, tin_label], "scripted", "script:tin_pyramids", tier="plinth")
        gm = GM()
        gm.box(X(uc - 0.36), X(uc + 0.36), 0.538, 0.55, 0.36, 0.36 + 0.62, 0)
        d.gm_object("pyramid_backing_%d" % pi_, gm, [back_m], "support", "script:backing_board")
    # ---- jars on step A (18, one row, six products)
    jl = os.path.join(tex, "jar_labels.png")
    juv = GB.jar_labels(jl, [(p_, m_, c1, c2) for p_, m_, c1, c2 in JAR_DESIGNS], tile=(256, 256), cols=3)
    jar_lab = d.image_mat("jar_labels", jl, rough=0.5)
    lid_m = d.mat("jar_lid", rgb8(196, 160, 60), rough=0.35, metal=0.8)
    gjs = [GM() for _ in JAR_DESIGNS]
    for k in range(18):
        ji = k % len(JAR_DESIGNS)
        GB.jar(gjs[ji], X(1.62 + k * 0.083), 0.465, 0.18, 0.0375, 0.115, 0, 1, juv[ji][1], 2, n=20)
    for ji, gmj in enumerate(gjs):
        fill_m = d.mat("jar_fill_%d" % ji, rgb8(*JAR_DESIGNS[ji][2]), rough=0.18)
        d.gm_object("jars_%d" % ji, gmj, [fill_m, jar_lab, lid_m], "scripted", "script:jars", tier="stand", smooth=True)
    # ---- apples in three crates at 0.9 of their size: 14, 13 and 13 (40)
    cs = 0.9
    apple_n = [14, 13, 13]
    for k, uc in enumerate((0.38, 0.88, 1.38)):
        ext, _ = d.piece("plastic_crate_02", uc, 0.205, 0.0, rot=(0, 0, 0), scale=cs, tier="bed", tris=None)
        cx_, cy_ = (ext[0] + ext[1]) / 2 + L / 2, (ext[2] + ext[3]) / 2
        zf = ext[4] + 0.018
        pos = [(ix, iy, 0) for iy in range(3) for ix in range(4)] + [(0.5, 0.5, 1), (2.5, 0.5, 1)]
        for (ix, iy, lay) in sorted(pos[:apple_n[k]], key=lambda p_: p_[2]):
            ax, ay = cx_ + (ix - 1.5) * 0.098, cy_ + (iy - 1.0) * 0.098
            az = GB.rest_z(d, ax - L / 2, ay, 0.047)
            _, nm_ = d.piece("food_apple_01", ax, ay, az, rot=(0, 0, rnd.uniform(0, 6.28)), scale=rnd.uniform(0.96, 1.0), tier="apples", tris=None)
            if lay:
                GB.settle_down(d, nm_)
    # ---- wicker_basket_02 with rolls across its rim, two crate_03 with lemons (all at their own size, DSP-06)
    ext, bn_ = d.piece("wicker_basket_02", 1.80, 0.18, 0.0, rot=(0, 0, 0), scale=1.0, tier="bed", tris=None)
    _, nm_ = d.piece("hamburger_buns", 1.80, 0.18, ext[5] + 0.001, rot=(0, 0, 0), scale=0.9, tier="basket", tris=None)
    GB.settle_down(d, nm_, max_drop=0.05)
    for k, uc in enumerate((2.19, 2.64)):
        ext, _ = d.piece("plastic_crate_03", uc, 0.14, 0.0, rot=(0, 0, 0), scale=0.9, tier="bed", tris=None)
        cx_, cy_ = (ext[0] + ext[1]) / 2 + L / 2, (ext[2] + ext[3]) / 2
        for j in range(6):
            ix, iy = j % 3, j // 3
            lx, ly = cx_ + (ix - 1.0) * 0.095, cy_ + (iy - 0.5) * 0.075
            _, nm_ = d.piece("lemon", lx, ly, GB.rest_z(d, lx - L / 2, ly, 0.034) + 0.004, rot=(0, 0, rnd.uniform(0, 6.28)), scale=1.0, tier="lemons", tris=None)
            GB.settle_down(d, nm_)
    # ---- onions in a low tray (15), tomatoes in a tray (30, script), bananas on a crate (three bunches at their own size)
    d.crate("onion_tray", 2.88, 3.24, 0.04, 0.34, 0.0, 0.07)
    for j in range(15):
        ix, iy = j % 5, j // 5
        ox, oy = 2.88 + 0.036 + ix * 0.0725, 0.0825 + iy * 0.080
        d.piece("yellow_onion", ox, oy, GB.rest_z(d, ox - L / 2, oy, 0.036) if False else 0.07, rot=(0, 0, rnd.uniform(0, 6.28)), scale=1.0, tier="onions", tris=None)
    d.crate("tomato_tray", 3.27, 3.72, 0.04, 0.30, 0.0, 0.06)
    tom = d.mat("tomato", rgb8(196, 40, 30), rough=0.22)
    calyx = d.mat("tomato_calyx", rgb8(70, 120, 50), rough=0.6)
    gm = GM()
    hz = 0.026
    for j in range(30):
        lay, k = divmod(j, 20)
        ix, iy = k % 4, k // 4
        if lay == 0:
            cx, cy, cz = X(3.27 + 0.06 + ix * 0.105), 0.075 + iy * 0.052, 0.06
        else:
            cx, cy, cz = X(3.27 + 0.11 + (ix % 3) * 0.105), 0.10 + (iy % 3) * 0.052, 0.06 + 0.040
        rx = 0.042 + rnd.uniform(-0.003, 0.003)
        ts = [-math.pi / 2 + math.pi * t / 8.0 for t in range(1, 8)]
        gm.lathe(cx, cy, cz, [(0.0, 0.0)] + [(rx * math.cos(t), hz * (1.0 + math.sin(t))) for t in ts] + [(0.0, 2 * hz)], mi=0, n=14)
        gm.lathe(cx, cy, cz + 2 * hz - 0.002, [(0.0, 0.0), (0.012, 0.0), (0.014, 0.003), (0.006, 0.006), (0.0, 0.006)], mi=1, n=8)
    d.gm_object("tomatoes", gm, [tom, calyx], "scripted", "script:tomatoes", tier="tray", smooth=True)
    d.crate("banana_crate", 3.74, 4.29, 0.02, 0.52, 0.0, 0.12)
    bd = d.dims("bananas")
    d.piece("bananas", 4.015, 0.145, 0.12, rot=(0, 0, 0), scale=1.0 if False else 0.9, tier="crate", tris=None)
    d.piece("bananas", 4.015, 0.385, 0.12, rot=(0, 0, 0), scale=0.9, tier="crate", tris=None)
    # ---- the price cards (14)
    texts = ["APPLES\n29p lb", "ONIONS\n19p lb", "LEMONS\n8p each", "TOMATOES\n45p lb", "BANANAS\n32p lb", "ROLLS\n6 for 55p", "BEANS\n21p", "SOUP\n18p", "PEAS\n19p", "SARDINES\n29p", "JAM\n59p", "HONEY\n69p", "MARMALADE\n55p", "SALMON\n79p"]
    path = os.path.join(tex, "price_cards.png")
    uvs = GEN.card_atlas(path, texts, cols=4, tile=(256, 128), size=42)
    pm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    spots = [(0.38, 0.0, 0.0), (0.88, 0.0, 0.0), (2.19, 0.0, 0.0), (3.06, 0.0, 0.0), (3.50, 0.0, 0.0), (4.10, 0.0, 0.0), (1.12, 0.0, 0.0), (1.80, 0.0, 0.0), (2.64, 0.0, 0.0),
             (1.70, 0.40, 0.18), (2.10, 0.40, 0.18), (2.50, 0.40, 0.18), (2.90, 0.40, 0.18), (0.20, 0.0, 0.0)]
    for k, (uc, vv, wz) in enumerate(spots):
        d.price_card(uc, 0.02 if vv == 0.0 else vv, wz, k, uvs, pm)
    d.display_texts = list(GEN.TEXTS) + [t.replace("\n", " ") for t in texts]
