"""The newsagent and tobacconist (west_north bay 0): the room's layout and the window display (13 October 2026, batch A). Both read the target (`shops.newsagent.room`, `.display`) through the context
the builders carry and say, in words in each docstring, every choice the target left open (each is a Judgement in NOTES.md and a `Changes after the build` line).

Everything printed here is the project's own: invented papers, magazines, greetings cards, postcards and tobacco makers (sw_gen.py), nobody drawn. Tobacco is allowed (CLAUDE.md); the gantry holds fictional makers.
"""
import math
import os

import numpy as np

import sw_assets as A
import sw_gen as GEN
from sw_gen import GM

rgb8 = None          # set by the builders (sw_room.rgb8)


def _setup():
    global rgb8
    import sw_room as S
    rgb8 = S.rgb8


# ---------------------------------------------------------------------------------------------------------------------------------- the room
def room(r):
    """The newsagent's room (target `shops.newsagent.room`: fixtures N-*, goods by name and count). What the target leaves open, and what this does:

    gantry N-back-gantry (x -2.55 to 0.05, 0.12 deep, boards at 1.35, 1.7 and 2.0): packs of the project's fictional makers standing in columns across the whole length, two or three high (the bottom
    board has 0.30 clear, the middle 0.25, the top 0.15 more under the ceiling battens' reach), a few columns missing and a few packs pulled forward. The target counts 100 packs and 8 Poly Haven ones; 100
    packs fill about a third of 2.6 m of three boards, so the gantry is filled (about 300) and the Poly Haven cigarette_pack (7,582 triangles a pack, the real brand on its net) is not used: the packs are
    script boxes of its size (56 x 29 x 103 mm). The sliding glass front is not modelled (glass over goods is the black-void risk of Rita's close review; the room reads the same through it).
    counter N-back-counter (x -2.55 to 0.05, 0.6 deep, 1.0 high): at its left end a tray of three stationery_supplies lying flat, then ten sweet jars along the back (the gantry's bottom board is 0.325 over
    the counter: a jar with its lid is 0.23), a toast rack of cards, the till at the right end in front of the gantry (0.42 across: the target's size), four pads of office_notepads. The glass cabinet end
    of the target is a tray without glass sides (same reason).
    pensions N-back-pensions (x 0.45 to 1.6, 0.55 deep): a counter 1.0 high with a timber frame over it, a glass 1.0 x 0.8 in it (clear: it passes the light as the room's other glass does), the brass-edged
    slot in the bottom rail and the hours card on the glass: PENSIONS & ALLOWANCES, no shop's name, no real firm's.
    N-back-door (x 1.85 to 2.55): a plain painted door in a frame, flat 40 mm, two raised panels and a brass knob.
    racks: left wall, five rows of magazine covers, each row a ledge and twelve covers (60: the target's count), rows 0.235 apart so that each row hides the foot of the row above (the way a rack reads);
    right wall, the greetings cards in four rows of ten (40) on a ledge each, the postcard board (20 postcards) and the wall clock (0.3 across). Each wall stands off 0.04 at most.
    floor N-floor: the tiles are Poly Haven rubber_tiles tinted, a 300 mm checker; the rubber mat at the door is 12 mm thick."""
    _setup()
    import sw_room_gen as RG
    D = RG.D
    W = RG.W
    rr = r.RR
    fx = r.fxd
    rnd = r.rnd
    tex = r.tex
    GEN.TEXTS.clear()
    # ---- the pictures made by script
    mag_uv = GEN.cover_atlas(os.path.join(tex, "magazines.png"), "magazine")
    card_uv = GEN.card_art_atlas(os.path.join(tex, "cards.png"), GEN.CARD_WORDS)
    post_uv = GEN.card_art_atlas(os.path.join(tex, "postcards.png"), GEN.POSTCARD_WORDS, cols=4, rows=2, tile=(260, 180), postcard=True)
    pack_uv = GEN.pack_atlas(os.path.join(tex, "packs.png"))
    jar_uv = GEN.jar_atlas(os.path.join(tex, "jars.png"))
    mag_m = r.image_mat("magazines", os.path.join(tex, "magazines.png"), rough=0.5)
    card_m = r.image_mat("greeting_cards", os.path.join(tex, "cards.png"), rough=0.55)
    post_m = r.image_mat("postcards", os.path.join(tex, "postcards.png"), rough=0.55)
    pack_m = r.image_mat("packs", os.path.join(tex, "packs.png"), rough=0.4)
    jar_m = r.image_mat("jars", os.path.join(tex, "jars.png"), rough=0.3)
    lid_m = r.mat("jar_lid", rgb8(190, 190, 186), rough=0.3, metal=0.9)
    # ---- the counter and what stands on it
    cx0, cx1, cy0, cy1, ch = r.counter("N-back-counter", panels=True)
    # the gantry (above the counter: its uprights stand on the counter's top)
    gx0, gx1 = fx["N-back-gantry"]["x"]
    tiers = [(1.35, gx0, gx1), (1.70, gx0, gx1), (2.0, gx0, gx1)]
    r.shelf_unit("N-back-gantry", tiers, bottom=ch)
    gd = fx["N-back-gantry"]["depth_m"]
    pw, pd, ph = 0.056, 0.029, 0.103
    npacks = 0
    for z, high in ((1.35, 3), (1.70, 2), (2.0, 2)):
        gm = GM()
        n_here = 0
        x = gx0 + 0.04
        y0 = D - gd + 0.004                   # the front edge of the board, 4 mm in
        while x + pw <= gx1 - 0.04:
            if rnd.random() < 0.05:           # a column missing
                x += pw + 0.004
                continue
            k = rnd.randrange(len(pack_uv))
            hh = high if rnd.random() > 0.15 else high - 1
            for j in range(hh):
                pull = 0.012 if rnd.random() < 0.03 else 0.0
                gm.box(x, x + pw, y0 - pull, y0 - pull + pd, z + j * ph, z + (j + 1) * ph - 0.0005, 0, uv_front=pack_uv[k], uv_other=(pack_uv[k][0] + 0.01, pack_uv[k][1] + 0.01))
                n_here += 1
            x += pw + 0.002
        ob = gm.to_object("packs_%.2f" % z, [pack_m], r.sc)
        r.placed_rec("N-back-gantry", "script:cigarette_packs", gm.extents(), [ob.name], tag="gantry_%.2f" % z, n=n_here)
        npacks += n_here
    r.notes.append("gantry: %d fictional packs on the three boards (the target's 100 + 8 fill a third of the length); the Poly Haven cigarette_pack is not used; no sliding glass front" % npacks)
    # the jars: ten along the back of the counter, in front of the gantry
    gmj, gml, gmb = GM(), GM(), GM()
    jr, jh = 0.058, 0.20
    x = cx0 + 0.72
    y = D - gd - 0.065
    for k in range(10):
        xc = x + k * 0.135 + rnd.uniform(-0.002, 0.002)
        prof = [(0.0, 0.0), (jr * 0.92, 0.0), (jr, 0.006), (jr, jh * 0.80), (jr * 0.78, jh * 0.9), (jr * 0.66, jh * 0.94), (jr * 0.66, jh), (0.0, jh)]
        gmj.lathe(xc, y, ch, prof, mi=0, n=22, label=(1, 4), mi_label=0, label_uv=(jar_uv[k][0][0], jar_uv[k][0][1], jar_uv[k][0][2], jar_uv[k][0][3]))
        gml.lathe(xc, y, ch + jh, [(0.0, 0.0), (jr * 0.72, 0.0), (jr * 0.74, 0.004), (jr * 0.74, 0.030), (jr * 0.6, 0.032), (0.0, 0.032)], mi=0, n=22)
        gmb.band(xc, y, ch + 0.055, ch + 0.135, jr + 0.0012, -42, 42, 0, uv=jar_uv[k][1], n=10)
    o1 = gmj.to_object("sweet_jars", [jar_m], r.sc, smooth=True)
    o2 = gml.to_object("sweet_jar_lids", [lid_m], r.sc, smooth=True)
    o3 = gmb.to_object("sweet_jar_labels", [jar_m], r.sc)
    r.placed_rec("N-back-counter", "script:sweet_jars", gmj.extents(), [o1.name, o2.name, o3.name], tag="jars", n=10)
    # the till at the right end, in front of the gantry
    till_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "CashRegister_01") / max(r.dims("CashRegister_01"))
    r.place("CashRegister_01", (cx1 - 0.33, D - gd - 0.01, ch), rot=(0, 0, 0), scale=till_s, fixture="N-back-counter", anchor=("c", "max", "min"))
    # the stationery tray at the left end: a shallow tray, the three sets lying flat on it
    tray_m = r.mat("stationery_tray", rgb8(120, 84, 54), rough=0.6)
    tx0, tx1, ty0, ty1 = cx0 + 0.02, cx0 + 0.62, cy0 + 0.04, cy0 + 0.58
    r.box("stationery_tray_base", tx0, tx1, ty0, ty1, ch, ch + 0.004, tray_m, fixture="N-back-counter")
    for nm, (a, b, c_, d_) in (("l", (tx0, tx0 + 0.006, ty0, ty1)), ("r", (tx1 - 0.006, tx1, ty0, ty1)), ("f", (tx0 + 0.006, tx1 - 0.006, ty0, ty0 + 0.006)), ("b", (tx0 + 0.006, tx1 - 0.006, ty1 - 0.006, ty1))):
        r.box("stationery_tray_%s" % nm, a, b, c_, d_, ch + 0.004, ch + 0.016, tray_m, fixture="N-back-counter")
    pens = r.sub_template("stationery_supplies", "pens", lambda n: "pencilcup" not in n)
    cup = r.sub_template("stationery_supplies", "cup", lambda n: "pencilcup" in n)
    for k in range(3):
        yy = ty0 + 0.02 + 0.08 + 0.165 * k
        r.place(pens, (tx0 + 0.02 + 0.14, yy, ch + 0.004), rot=(math.pi / 2, 0, rnd.uniform(-0.04, 0.04)), scale=1.0, fixture="N-back-counter", anchor=("c", "c", "min"), tag="pens")
        r.place(cup, (tx1 - 0.06, yy, ch + 0.004), rot=(0, 0, 0), scale=1.0, fixture="N-back-counter", anchor=("c", "c", "min"), tag="cup")
    # the four pads of office_notepads (the model is a kit of loose pads: the stacks, one each) on the counter beside the till
    pads = ["office_notepads_a4_stack", "office_notepads_yellow_pad", "office_notepads_note_stack", "office_notepads_sticky_stack"]
    xp = cx0 + 0.74
    for nm in pads:
        key = r.sub_template("office_notepads", nm, lambda n, nm=nm: n == nm)
        d = r.dims(key)
        r.place(key, (xp + d.x / 2, cy0 + 0.03 + d.y / 2, ch), rot=(0, 0, 0), scale=1.0, fixture="N-back-counter", anchor=("c", "c", "min"))
        xp += d.x + 0.03
        if nm == "office_notepads_yellow_pad":
            xp += 0.02
    # the toast rack of cards: a wire rack on the counter's front edge, six cards standing in it
    rack = GM()
    rx0, ry = cx0 + 1.55, cy0 + 0.16
    wire = r.mat("rack_wire", rgb8(70, 70, 74), rough=0.4, metal=0.8)
    rack.box(rx0, rx0 + 0.34, ry - 0.045, ry + 0.045, ch, ch + 0.005, 0)
    for i in range(7):
        xx = rx0 + 0.02 + i * 0.05
        rack.rod((xx, ry - 0.04, ch + 0.005), (xx, ry - 0.04, ch + 0.09), 0.0015, 0, 6)
        rack.rod((xx, ry + 0.04, ch + 0.005), (xx, ry + 0.04, ch + 0.09), 0.0015, 0, 6)
    rack.rod((rx0 + 0.02, ry - 0.04, ch + 0.09), (rx0 + 0.32, ry - 0.04, ch + 0.09), 0.0015, 0, 6)
    rack.rod((rx0 + 0.02, ry + 0.04, ch + 0.09), (rx0 + 0.32, ry + 0.04, ch + 0.09), 0.0015, 0, 6)
    o = rack.to_object("toast_rack", [wire], r.sc)
    r.fixtures.append({"fixture": "N-back-counter", "name": "toast_rack", "ext": [round(v, 4) for v in rack.extents()]})
    cg = GM()
    for i in range(6):
        k = rnd.randrange(len(card_uv))
        cg.sheet((rx0 + 0.045 + i * 0.05, ry, ch + 0.006 + 0.07), 0.046, 0.14, 0.003, tilt=rnd.uniform(-3, 3), mi=0, uv=card_uv[k], uv_other=(card_uv[k][0] + 0.01, card_uv[k][1] + 0.01))
    oc = cg.to_object("toast_rack_cards", [card_m], r.sc)
    r.placed_rec("N-back-counter", "script:greeting_cards", cg.extents(), [oc.name], tag="toast_rack", n=6)
    # ---- the pension counter, its screen and its hours card
    px0, px1 = fx["N-back-pensions"]["x"]
    r.counter("N-back-pensions", top_h=1.0, panels=True)
    wood = r.mat("screen_wood", rgb8(96, 62, 38), rough=0.5)
    brass = r.brass_m
    ys = D - 0.46
    t = 0.04
    r.box("screen_post_l", px0, px0 + 0.05, ys - t / 2, ys + t / 2, 1.0, 1.95, wood, fixture="N-back-pensions")
    r.box("screen_post_r", px1 - 0.05, px1, ys - t / 2, ys + t / 2, 1.0, 1.95, wood, fixture="N-back-pensions")
    r.box("screen_top", px0 + 0.05, px1 - 0.05, ys - t / 2, ys + t / 2, 1.9, 1.95, wood, fixture="N-back-pensions")
    xm = (px0 + px1) / 2
    r.box("screen_sill_l", px0 + 0.05, xm - 0.15, ys - t / 2, ys + t / 2, 1.0, 1.10, wood, fixture="N-back-pensions")
    r.box("screen_sill_r", xm + 0.15, px1 - 0.05, ys - t / 2, ys + t / 2, 1.0, 1.10, wood, fixture="N-back-pensions")
    r.box("screen_slot_edge_l", xm - 0.15, xm - 0.14, ys - t / 2 - 0.002, ys + t / 2 + 0.002, 1.0, 1.10, brass, fixture="N-back-pensions")
    r.box("screen_slot_edge_r", xm + 0.14, xm + 0.15, ys - t / 2 - 0.002, ys + t / 2 + 0.002, 1.0, 1.10, brass, fixture="N-back-pensions")
    r.box("screen_slot_top", xm - 0.14, xm + 0.14, ys - t / 2 - 0.002, ys + t / 2 + 0.002, 1.095, 1.10, brass, fixture="N-back-pensions")
    gl = r.mat("screen_glass", (0.85, 0.9, 0.9), rough=0.02, glass=True)
    r.box("screen_glass", px0 + 0.05, px1 - 0.05, ys - 0.002, ys + 0.002, 1.10, 1.90, gl, fixture="N-back-pensions")
    hp = os.path.join(tex, "hours_card.png")
    huv = GEN.card_atlas(hp, ["PENSIONS &\nALLOWANCES", "MON-SAT\n9-5.30"], cols=1, tile=(300, 200), size=40)
    GEN.TEXTS.extend(["PENSIONS & ALLOWANCES", "MON-SAT 9-5.30"])
    hm = r.image_mat("hours_card", hp, rough=0.6)
    hc = GM()
    hc.box(xm - 0.15, xm + 0.15, ys - 0.0045, ys - 0.0025, 1.50, 1.70, 0, uv_front=huv[0])
    hc.box(xm - 0.15, xm + 0.15, ys - 0.0045, ys - 0.0025, 1.74, 1.84, 0, uv_front=huv[1])
    oh = hc.to_object("hours_cards", [hm], r.sc)
    r.fixtures.append({"fixture": "N-back-pensions", "name": "hours_cards", "ext": [round(v, 4) for v in hc.extents()]})
    # ---- the stockroom door (flat, 40 mm): the slab, two raised panels, an architrave and a brass knob
    dx0, dx1 = fx["N-back-door"]["x"]
    paint = r.mat("door_paint", rgb8(40, 52, 90), rough=0.4)
    r.box("door_slab", dx0, dx1, D - 0.04, D - 0.005, 0.0, 2.0, paint, fixture="N-back-door")
    r.box("door_panel_a", dx0 + 0.10, dx1 - 0.10, D - 0.048, D - 0.04, 0.12, 0.90, paint, fixture="N-back-door")
    r.box("door_panel_b", dx0 + 0.10, dx1 - 0.10, D - 0.048, D - 0.04, 1.05, 1.88, paint, fixture="N-back-door")
    arch = r.mat("architrave", rgb8(226, 224, 214), rough=0.5)
    r.box("architrave_l", dx0 - 0.06, dx0, D - 0.045, D - 0.005, 0.0, 2.06, arch, fixture="N-back-door")
    r.box("architrave_r", dx1, dx1 + 0.06, D - 0.045, D - 0.005, 0.0, 2.06, arch, fixture="N-back-door")
    r.box("architrave_head", dx0, dx1, D - 0.045, D - 0.005, 2.0, 2.06, arch, fixture="N-back-door")
    r.cyl("door_knob", dx1 - 0.08, D - 0.055, 1.0, 0.022, 0.022, brass, axis="y", verts=14)
    r.fixtures.append({"fixture": "N-back-door", "name": "door_knob", "ext": [dx1 - 0.102, dx1 - 0.058, D - 0.066, D - 0.044, 0.978, 1.022]})
    # ---- the left wall's magazine rack: a board, five rows of a ledge and twelve covers
    xl = -W / 2
    boardm = r.mat("rack_board", rgb8(120, 118, 112), rough=0.7)
    ledge = r.mat("rack_ledge", rgb8(150, 108, 70), rough=0.55)
    y0, y1 = fx["N-left-racks"]["y"]
    z0, z1 = fx["N-left-racks"]["z"]
    r.box("left_rack_board", xl, xl + 0.012, y0, y1, z0, z1, boardm, fixture="N-left-racks")
    n_cols, rows_n = 12, 5
    pitch = (y1 - y0) / n_cols
    cw, chh = 0.192, 0.255
    gmc = GM()
    # the covers face +x (into the room): a box with the picture on its +x face; built with GM.box and front "+x"
    for k in range(rows_n):
        zb = z0 + 0.02 + 0.235 * (rows_n - 1 - k)
        xp_ = xl + 0.014 + 0.005 * k
        for i in range(n_cols):
            yc = y0 + pitch * (i + 0.5)
            kk = (k * 5 + i * 3 + rnd.randrange(3)) % len(mag_uv)
            gmc.box(xp_, xp_ + 0.003, yc - cw / 2, yc + cw / 2, zb, zb + chh, 0, uv_front=mag_uv[kk], front="+x", uv_other=(mag_uv[kk][0] + 0.01, mag_uv[kk][1] + 0.01))
    oc = gmc.to_object("magazine_covers", [mag_m], r.sc)
    r.placed_rec("N-left-racks", "script:magazine_covers", gmc.extents(), [oc.name], tag="rack", n=n_cols * rows_n)
    # ---- the right wall: the greetings cards (four rows of ten), the postcard board and the clock
    xr = W / 2
    ry0, ry1 = fx["N-right-racks"]["y"]
    rz0, rz1 = fx["N-right-racks"]["z"]
    r.box("right_rack_board", xr - 0.012, xr, ry0, ry1, rz0, rz1, boardm, fixture="N-right-racks")
    gmk = GM()
    cwid, chei = 0.115, 0.16
    n40 = 0
    for k in range(4):
        zb = rz0 + 0.30 + 0.215 * (3 - k)
        xp_ = xr - 0.014 - 0.005 * k - 0.003
        r.box("right_ledge_%d" % k, xr - 0.038, xr - 0.012, ry0 + 0.03, ry0 + 1.52, zb - 0.012, zb, ledge, fixture="N-right-racks")
        for i in range(10):
            yc = ry0 + 0.075 + 0.145 * i
            kk = (k * 10 + i + rnd.randrange(4)) % len(card_uv)
            gmk.box(xp_, xp_ + 0.003, yc - cwid / 2, yc + cwid / 2, zb, zb + chei, 0, uv_front=card_uv[kk], front="-x", uv_other=(card_uv[kk][0] + 0.01, card_uv[kk][1] + 0.01))
            n40 += 1
    ok_ = gmk.to_object("greeting_cards", [card_m], r.sc)
    r.placed_rec("N-right-racks", "script:greeting_cards", gmk.extents(), [ok_.name], tag="rack", n=n40)
    # the postcard board: a cork board with 20 postcards in four rows of five
    cork = r.mat("cork", rgb8(170, 126, 84), rough=0.9)
    cy_a, cy_b = ry0 + 1.65, ry1 - 0.02
    r.box("postcard_board", xr - 0.026, xr - 0.012, cy_a, cy_b, rz0 + 0.08, rz0 + 0.74, cork, fixture="N-right-racks")
    gmp = GM()
    pcw, pch = 0.135, 0.094
    npost = 0
    for k in range(4):
        for i in range(5):
            yc = cy_a + 0.045 + 0.06 + i * 0.165 * 0.88 + rnd.uniform(-0.004, 0.004)
            zc = rz0 + 0.16 + k * 0.145 + rnd.uniform(-0.004, 0.004)
            kk = (k * 5 + i) % len(post_uv)
            gmp.box(xr - 0.031, xr - 0.027, yc - pcw / 2, yc + pcw / 2, zc, zc + pch, 0, uv_front=post_uv[kk], front="-x", uv_other=(post_uv[kk][0] + 0.01, post_uv[kk][1] + 0.01))
            npost += 1
    op = gmp.to_object("postcards", [post_m], r.sc)
    r.placed_rec("N-right-racks", "script:postcard_rack", gmp.extents(), [op.name], tag="board", n=npost)
    ck_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "wall_clock") / max(r.dims("wall_clock"))
    r.place("wall_clock", (xr - 0.0145, ry1 - 0.28, 1.86), rot=(0, 0, -math.pi / 2), scale=ck_s, fixture="N-right-racks", anchor=("max", "c", "c"), clock=r.next_clock(), tag="clock")
    # ---- the floor: the rubber mat at the door (the door's x is +1.2: its zone u 3700 to 4706)
    mat_m = r.mat("rubber_mat", rgb8(34, 34, 36), rough=0.9)
    r.box("door_mat", 0.72, 1.70, 0.14, 0.72, 0.0, 0.012, mat_m, fixture="N-floor")
    r.notes.append("the stock-room door, the pension screen, the gantry and both walls' racks are scripts from the target's dimensions; every printed thing is the project's own (sw_gen.TEXTS)")
    r.texts = list(GEN.TEXTS)
    # the hours card text is added to the list the checks read
    return r


# ---------------------------------------------------------------------------------------------------------------------------------- the window
def display(d):
    """The newsagent's window (target `shops.newsagent.display`, 8 item rows; bed 3.35 x 0.55, the 4.2/4.4 window board SB1 not built here: it is a card on the glass, the build's glass rows are the lettering).
    The zones of the target overlap (the newspapers' u 0.1 to 1.2 under the cartons' u 0.2 to 0.9; the magazines' u 1.3 to 2.3 over the notepads' u 1.0 to 1.7; the postcard rack's v 0.35 to 0.5 over the
    magazines'), so every piece has a place of its own on a surface that exists:
    the newspapers: ten, in two shingled rows of five on two low ramps in front (u 0.10 to 0.62 and 0.66 to 1.18, v 0.05 to 0.28; the ramp rises 0.12 toward the back and leans each row 20 degrees to the
    street), folded once so that the masthead and the headline show; the stationery sets (2) lie flat in front of the cartons' stand and the pads (3) at the right of the ramps.
    the cartons: six, in three stacks of two on the shelf of a timber stand (shelf at w 0.40, four legs to the bed; u 0.20 to 0.88, v 0.34 to 0.50).
    the magazines: twelve, not 24 (the zone is 1.0 wide: 24 at 0.19 across would be five rows deep and would hide each other), on a sloping board (u 1.30 to 2.20, v 0.20 to 0.46, leaning 60 degrees), four across,
    three rows each showing at least 0.7 of its height.
    the sweet jars: six on the bed in two rows of three (u 2.45 to 2.88, v 0.12 to 0.32), the spinner card rack at u 3.12 (a pole from the bed with four faces of four cards, w 0.30 to 1.10), the postcard rack
    at u 2.30 (a pole from the bed with three rings of eight postcards, w 0.50 to 1.20)."""
    _setup()
    rr = d.RR
    walls = rr["walls"]
    import sw_room_gen as RG
    wall_rgb = RG._rgb(walls["above"])
    dado_rgb = RG._rgb(walls["dado"])
    d.start((150, 152, 150), wall_rgb, dado_rgb)
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    tex = d.tex
    GEN.TEXTS.clear()
    mag_uv = GEN.cover_atlas(os.path.join(tex, "magazines.png"), "magazine")
    paper_uv = GEN.cover_atlas(os.path.join(tex, "papers.png"), "paper", cols=3, rows=2)
    card_uv = GEN.card_art_atlas(os.path.join(tex, "cards.png"), GEN.CARD_WORDS)
    post_uv = GEN.card_art_atlas(os.path.join(tex, "postcards.png"), GEN.POSTCARD_WORDS, cols=4, rows=2, tile=(260, 180), postcard=True)
    pack_uv = GEN.pack_atlas(os.path.join(tex, "packs.png"))
    jar_uv = GEN.jar_atlas(os.path.join(tex, "jars.png"))
    # the white of the printed goods is held at about 0.86 of full in the window (a sheet of newsprint is not paper white): under the gate's night spill the white card, paper and carton tops burnt
    # 3.5 per cent of the close frames (PIC-05g; the room's pictures use the atlases at full white, they are lit differently)
    from PIL import Image as _Im
    # and the magazines' dark covers (navy, green, dark red) are lifted 1.35 times: they read 0.60 of the room round them at night (LIT-08) at the spill this shop's gate now has
    for _nm, _k in (("papers.png", 0.86), ("cards.png", 0.86), ("postcards.png", 0.86), ("packs.png", 0.86), ("magazines.png", 1.35)):
        _p = os.path.join(tex, _nm)
        _a = np.asarray(_Im.open(_p).convert("RGB")).astype(np.float32) * _k
        _Im.fromarray(np.clip(_a, 0, 255).astype(np.uint8)).save(_p)
    mag_m = d.image_mat("magazines", os.path.join(tex, "magazines.png"), rough=0.5)
    pap_m = d.image_mat("papers", os.path.join(tex, "papers.png"), rough=0.7)
    card_m = d.image_mat("greeting_cards", os.path.join(tex, "cards.png"), rough=0.55)
    post_m = d.image_mat("postcards", os.path.join(tex, "postcards.png"), rough=0.55)
    pack_m = d.image_mat("packs", os.path.join(tex, "packs.png"), rough=0.4)
    jar_m = d.image_mat("jars", os.path.join(tex, "jars.png"), rough=0.3)
    lid_m = d.mat("jar_lid", rgb8(190, 190, 186), rough=0.3, metal=0.9)
    wood = d.mat("stand_wood", rgb8(150, 108, 70), rough=0.55)
    board = d.mat("slope_board", rgb8(150, 146, 136), rough=0.7)
    wire = d.mat("rack_wire", rgb8(70, 70, 74), rough=0.4, metal=0.8)
    # ---- the two paper stands (a lower step, a higher step and a back board each) and the ten papers, folded once: three on the lower step, shingled 12 mm apart in depth, two on the higher step between
    # their gaps, so that every paper shows at least half to the far pavement
    for ri, u0 in enumerate((0.10, 0.70)):
        gm = GM()
        x0, x1 = X(u0), X(u0 + 0.58)
        gm.box(x0, x1, 0.04, 0.24, 0.0, 0.06, 0)            # the lower step
        gm.box(x0, x1, 0.24, 0.37, 0.0, 0.24, 0)            # the upper step
        gm.box(x0, x1, 0.37, 0.382, 0.24, 0.46, 0)          # the back board over it
        d.gm_object("paper_stand_%d" % ri, gm, [board], "support", "script:paper_stand")
    lean = 18.0
    for pi in range(10):
        ri, k = divmod(pi, 5)
        u0 = (0.10, 0.70)[ri]
        if k < 3:
            xc = X(u0 + 0.15 + k * 0.16) + rnd.uniform(-0.004, 0.004)
            foot_v, foot_w = 0.150 - 0.012 * k, 0.06
        else:
            xc = X(u0 + 0.23 + (k - 3) * 0.16) + rnd.uniform(-0.004, 0.004)
            foot_v, foot_w = 0.295 - 0.012 * (k - 3), 0.24
        hh = 0.20
        zc = foot_w + hh / 2 * math.cos(math.radians(lean)) + 0.003
        vc = foot_v - 0.01 + hh / 2 * math.sin(math.radians(lean))
        gm = GM()
        tile = paper_uv[pi % 6]
        top = (tile[0], tile[1] + (tile[3] - tile[1]) * 0.38, tile[2], tile[3])
        gm.sheet((xc, vc, zc), 0.22, hh, 0.004, tilt=lean + rnd.uniform(-1.0, 1.0), yaw=rnd.uniform(-1.0, 1.0), mi=0, uv=top, uv_other=(tile[0] + 0.01, tile[1] + 0.01))
        d.gm_object("newspaper_%d" % pi, gm, [pap_m], "scripted", "script:newspapers", tier="bed" if k < 3 else "step")
    # ---- the stand with the cartons
    sx0, sx1, sv0, sv1, sw = X(0.20), X(0.88), 0.39, 0.55, 0.46
    gm = GM()
    for xx in (sx0 + 0.015, sx1 - 0.015):
        for vv in (sv0 + 0.015, sv1 - 0.015):
            gm.box(xx - 0.015, xx + 0.015, vv - 0.015, vv + 0.015, 0.0, sw, 0)
    gm.box(sx0, sx1, sv0, sv1, sw, sw + 0.02, 0)
    d.gm_object("carton_stand", gm, [wood], "support", "script:carton_stand")
    cg = GM()
    k = 0
    for col in range(3):
        for lay in range(2):
            kk = rnd.randrange(len(pack_uv))
            cg.box(sx0 + 0.04 + col * 0.215, sx0 + 0.04 + col * 0.215 + 0.20, sv0 + 0.04, sv0 + 0.04 + 0.055, sw + 0.02 + lay * 0.10, sw + 0.02 + (lay + 1) * 0.10 - 0.001, 0, uv_front=pack_uv[kk], uv_other=(pack_uv[kk][0] + 0.01, pack_uv[kk][1] + 0.01))
    d.gm_object("cigarette_cartons", cg, [pack_m], "scripted", "script:cigarette_cartons", tier="stand")
    # ---- the plinth along the front of the magazine board (60 mm high: the sill hides the lowest 40 mm of the bed from the far pavement, and a pad lies 30 mm high): two pots of pens and three pads
    d.crate("stationery_plinth", 1.36, 2.20, 0.03, 0.17, 0.0, 0.06)
    from mathutils import Matrix, Vector
    meshes_t, lo_t, hi_t = d.template("stationery_supplies")
    cupm = [m for m in meshes_t if "pencilcup" in m.name][0]
    cpts = [cupm.matrix_world @ Vector(c) for c in cupm.bound_box]
    ccx = (min(p.x for p in cpts) + max(p.x for p in cpts)) / 2
    ccy = (min(p.y for p in cpts) + max(p.y for p in cpts)) / 2
    cfloor = min(p.z for p in cpts) + 0.004
    pen_names = ["pen_blue", "pen_fancy", "pen_red", "pencil_new_a", "pencil_new_b", "pencil_old", "pencil_used"]
    pots = []
    for pot in range(2):
        parts = [(("pencilcup",), Matrix.Identity(4))]
        order = pen_names if pot == 0 else pen_names[3:] + pen_names[:3]
        for i, nm in enumerate(order):
            m = [mm for mm in meshes_t if mm.name.endswith(nm)][0]
            pts = [m.matrix_world @ Vector(c) for c in m.bound_box]
            piv = Vector((min(p.x for p in pts), (min(p.y for p in pts) + max(p.y for p in pts)) / 2, (min(p.z for p in pts) + max(p.z for p in pts)) / 2))
            phi = 2 * math.pi * i / 7 + 0.9 * pot
            base = Vector((ccx + 0.017 * math.cos(phi), ccy + 0.017 * math.sin(phi), cfloor))
            ax = Vector((-math.sin(phi), math.cos(phi), 0.0))
            lean_ = math.radians(5.0 + 2.0 * (i % 3))
            xf = Matrix.Translation(base) @ Matrix.Rotation(lean_, 4, ax) @ Matrix.Rotation(-math.pi / 2, 4, "Y") @ Matrix.Translation(-piv)
            parts.append(((nm,), xf))
        pots.append(d.compose("stationery_supplies", "pot%d" % pot, parts))
    d.piece(pots[0], 1.43, 0.10, 0.06, rot=(0, 0, 0), tier="plinth", tris=None)
    x_pad = 1.43 + 0.05 + 0.03
    for nm in ("office_notepads_yellow_pad", "office_notepads_a4_stack", "office_notepads_note_stack"):
        key = d.sub_template("office_notepads", nm, lambda n, nm=nm: n == nm)
        rt = (0, 0, math.pi / 2) if "note_stack" not in nm else (0, 0, 0)
        dd = d.dims(key, rt)
        sc_ = 0.6
        d.piece(key, x_pad + dd.x * sc_ / 2, 0.10, 0.06, rot=rt, scale=sc_, tier="plinth", tag=nm, tris=None)
        x_pad += dd.x * sc_ + 0.03
    d.piece(pots[1], x_pad + 0.05, 0.10, 0.06, rot=(0, 0, 0), tier="plinth", tris=None)
    # ---- the magazines on a sloping board (leaning 40 degrees from the vertical, 0.58 long)
    mx0, mx1, vb = X(1.30), X(2.20), 0.17
    lean_b = 40.0
    blen = 0.58
    gm = GM()
    cb, sb = math.cos(math.radians(lean_b)), math.sin(math.radians(lean_b))
    gm.sheet(((mx0 + mx1) / 2, vb + blen / 2 * sb, 0.004 + blen / 2 * cb), mx1 - mx0, blen, 0.012, tilt=lean_b, mi=0)
    d.gm_object("magazine_board", gm, [board], "support", "script:magazine_board")
    mg = GM()
    for row in range(3):
        for i in range(4):
            kk = (row * 4 + i * 5) % len(mag_uv)
            xc = (mx0 + mx1) / 2 + (i - 1.5) * 0.225
            s0 = 0.015 + row * 0.14 + 0.125
            off = 0.0095 + 0.0045 * row                                 # each row 4.5 mm in front of the one above: they do not touch
            zc = 0.004 + s0 * cb - off * sb
            vc = vb + s0 * sb + off * cb * -1.0
            mg.sheet((xc, vc, zc), 0.19, 0.25, 0.003, tilt=lean_b, yaw=rnd.uniform(-1.5, 1.5), mi=0, uv=mag_uv[kk], uv_other=(mag_uv[kk][0] + 0.01, mag_uv[kk][1] + 0.01))
    d.gm_object("magazines", mg, [mag_m], "scripted", "script:magazines", tier="board")
    # ---- the sweet jars
    gmj, gml, gmb = GM(), GM(), GM()
    jr, jh = 0.058, 0.20
    for k in range(6):
        row, col = divmod(k, 3)
        xc = X(2.50 + col * 0.14 + (0.07 if row else 0.0))
        yc = 0.20 + row * 0.12
        prof = [(0.0, 0.0), (jr * 0.92, 0.0), (jr, 0.006), (jr, jh * 0.80), (jr * 0.78, jh * 0.9), (jr * 0.66, jh * 0.94), (jr * 0.66, jh), (0.0, jh)]
        gmj.lathe(xc, yc, 0.0, prof, mi=0, n=22, label=(1, 4), mi_label=0, label_uv=jar_uv[k][0])
        gml.lathe(xc, yc, jh, [(0.0, 0.0), (jr * 0.72, 0.0), (jr * 0.74, 0.004), (jr * 0.74, 0.030), (jr * 0.6, 0.032), (0.0, 0.032)], mi=0, n=22)
        gmb.band(xc, yc, 0.055, 0.135, jr + 0.0012, -42, 42, 0, uv=jar_uv[k][1], n=10)
    d.gm_object("sweet_jars", gmj, [jar_m], "scripted", "script:sweet_jars", tier="bed", smooth=True)
    d.gm_object("sweet_jar_lids", gml, [lid_m], "support", "script:sweet_jars", smooth=True)
    d.gm_object("sweet_jar_labels", gmb, [jar_m], "support", "script:sweet_jars")
    # ---- the spinner rack (greetings cards) and the postcard rack
    for name, u, vc, w0, w1, n_face, rows_, tile_m_, uvs, cw_, ch_ in (("card_rack", 3.12, 0.36, 0.30, 1.10, 4, 4, card_m, card_uv, 0.115, 0.16), ("postcard_rack", 2.30, 0.42, 0.50, 1.20, 8, 3, post_m, post_uv, 0.135, 0.094)):
        xc = X(u)
        g = GM()
        g.rod((xc, vc, 0.0), (xc, vc, w1 + 0.05), 0.006, 0, 8)
        g.cylinder(xc, vc, 0.0, 0.012, 0.12, 0, 20)
        rad = 0.09 if n_face == 4 else 0.12
        for ri in range(rows_ + 1):
            zr = w0 + (w1 - w0 - ch_) * ri / max(rows_ - 1, 1) if ri < rows_ else w1 + 0.010
            g.torus((xc, vc, zr - 0.004), rad, 0.0018, 0, axis="z", nm=24, nn=5)
        d.gm_object(name + "_frame", g, [wire], "support", "script:" + name)
        cgm = GM()
        cnt = 0
        for ri in range(rows_):
            zr = w0 + (w1 - w0 - ch_) * ri / max(rows_ - 1, 1)
            for fi in range(n_face):
                ang = 2 * math.pi * fi / n_face + 0.2 * ri
                kk = (ri * n_face + fi) % len(uvs)
                # a card standing on edge on the ring, face outward, leaned 8 degrees back
                cgm.sheet((xc + math.sin(ang) * rad, vc - math.cos(ang) * rad, zr + ch_ / 2), cw_ if n_face == 4 else cw_ * 0.8, ch_, 0.003, tilt=8.0 * 0.0, yaw=-math.degrees(ang), mi=0, uv=uvs[kk], uv_other=(uvs[kk][0] + 0.01, uvs[kk][1] + 0.01))
                cnt += 1
        d.gm_object(name, cgm, [tile_m_], "scripted", "script:" + ("card_rack" if n_face == 4 else "postcard_rack"), tier="rack")
    # ---- the price cards (hand cards on the bed's front edge)
    cards = [("PAPERS\nORDERED", 0.40), ("SWEETS\n2oz 25p", 2.69), ("CARDS\nFROM 25p", 3.12), ("MAGAZINES", 1.95), ("STATIONERY", 1.50), ("PENS & PADS", 1.75)]
    texts = [c[0] for c in cards]
    path = os.path.join(tex, "price_cards.png")
    uvs = GEN.card_atlas(path, texts, cols=3, tile=(256, 128), size=46)
    pm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    for k, (_, uc) in enumerate(cards):
        d.price_card(uc, 0.02, 0.0, k, uvs, pm)
    d.display_texts = list(GEN.TEXTS) + [t.replace("\n", " ") for t in texts]
