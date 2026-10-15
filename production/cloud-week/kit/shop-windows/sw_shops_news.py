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
    # ---- the pictures: photographs and script (sw_prints; the same library as the window's)
    import sw_prints as PR
    PR.TEXTS.clear()
    PR.USED.clear()
    PR.FIT.clear()
    mag_uv = PR.magazine_atlas(os.path.join(tex, "magazines.png"), 24)
    card_uv = PR.card_atlas(os.path.join(tex, "cards.png"), 10)
    post_uv = PR.postcard_atlas(os.path.join(tex, "postcards.png"), 12)
    pack_uv = GEN.pack_atlas(os.path.join(tex, "packs.png"))
    jc_uv, jl_uv = PR.jar_atlases(os.path.join(tex, "sweets.png"), os.path.join(tex, "jar_labels.png"), 10)
    PR.write_used(os.path.join(r.work, "prints_used_room.json"))
    mag_m = r.image_mat("magazines", os.path.join(tex, "magazines.png"), rough=0.5)
    card_m = r.image_mat("greeting_cards", os.path.join(tex, "cards.png"), rough=0.55)
    post_m = r.image_mat("postcards", os.path.join(tex, "postcards.png"), rough=0.55)
    pack_m = r.image_mat("packs", os.path.join(tex, "packs.png"), rough=0.4)
    sweets_m = r.image_mat("sweets", os.path.join(tex, "sweets.png"), rough=0.35)
    jlab_m = r.image_mat("jar_labels", os.path.join(tex, "jar_labels.png"), rough=0.6)
    glass_m = r.mat("jar_glass", (0.96, 0.98, 0.98), rough=0.05, glass=True)
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
    # the jars: ten of glass along the back of the counter, in front of the gantry (try 2: 2 mm shell in the kit's goods-glass material, the sweets inside, a lid, the paper label on the outside of the glass)
    gl, ct, ld, lb = GM(), GM(), GM(), GM()
    x = cx0 + 0.72
    y = D - gd - 0.065
    for k in range(10):
        xc = x + k * 0.135 + rnd.uniform(-0.002, 0.002)
        GEN.glass_jar(gl, ct, ld, lb, xc, y, ch, uv_content=jc_uv[k], uv_label=jl_uv[k], n=22)
    o1 = gl.to_object("sweet_jars", [glass_m], r.sc, smooth=True)
    o2 = ct.to_object("sweet_jar_sweets", [sweets_m], r.sc, smooth=True)
    o3 = ld.to_object("sweet_jar_lids", [lid_m], r.sc, smooth=True)
    o4 = lb.to_object("sweet_jar_labels", [jlab_m], r.sc)
    r.placed_rec("N-back-counter", "script:sweet_jars", gl.extents(), [o1.name, o2.name, o3.name, o4.name], tag="jars", n=10)
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
    # try 2 (the street review, narrow 3): (40, 52, 90) read as a flat near-black slab through the glass, so it is (96, 110, 140), roughness 0.4; and (FLT-01: the door alone was 7.2 per cent of the glass at
    # STREET_30 with a 9 x 9 px standard deviation under 1) painted as a door is: a slow mottle (about 6 cm blotches, 10 per cent), a finer one (about 2 cm, 5 per cent) and vertical brush marks (3 per cent), a tileable 0.6 m map
    from scipy import ndimage as _ndi
    from PIL import Image as _Im
    _n = 512
    _rg = np.random.default_rng(41)

    def _nz(sy, sx):
        a_ = _ndi.gaussian_filter(_rg.normal(0.0, 1.0, (_n, _n)), (sy, sx), mode="wrap")
        return a_ / a_.std()
    _mott = 1.0 + 0.10 * _nz(16, 16) + 0.05 * _nz(5, 5) + 0.03 * _nz(30, 1.5)
    _img = np.array((96.0, 110.0, 140.0), np.float32)[None, None, :] * _mott[..., None]
    _pp = os.path.join(r.tex, "door_paint.png")
    _Im.fromarray(np.clip(_img, 0, 255).astype(np.uint8)).save(_pp)
    paint = r.image_mat("door_paint", _pp, tile_m=0.6, rough=0.4)
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
    r.texts = list(GEN.TEXTS) + list(PR.TEXTS)
    # the hours card text is added to the list the checks read
    return r


# ---------------------------------------------------------------------------------------------------------------------------------- the window
def display(d):
    """The newsagent's window (target `shops.newsagent.display`, 8 item rows; bed 3.35 x 0.55), try 2 (14 Oct 2026: both fresh reviews of try 1; the brief's step 0 e, f, i). Every printed good is made from a photograph
    (sw_prints), every sheet is bent (GM.csheet), leans BACK and rests on what is behind it (DSP-05), every support has a picture (DSP-09), every Poly Haven piece is at its own size (DSP-06). u along the window, v the
    depth from the glass, w the height above the bed:
    the newspapers: eight, the visible half of a folded tabloid (0.29 x 0.19, the top edge a fold, bent 6 mm over its height), two to a step and four to a stand on two stands (u 0.10 to 0.68 and 0.70 to 1.28; a lower
    step v 0.04 to 0.24 high 0.055 and an upper step v 0.24 to 0.37 high 0.24, a back board over it); each leans 18 degrees back with its foot on the step and its top 1 mm from the riser or the back board;
    the cartons: six of 280 x 90 x 50 mm on the shelf of a timber stand (u 0.20 to 0.88, v 0.39 to 0.55, shelf w 0.46), two columns of three, their fronts to the street;
    the magazines: twelve distinct covers on the front face of a sloping board (u 1.30 to 2.20) with side cheeks, leaning 35 degrees (try 1: 40; the pads at their own size need a plinth 0.225 deep, which moves the
    board's foot back to v 0.235, and the top must stay under 0.56): each cover 2 mm off the board along its normal, each lower row 4.5 mm further out, so no row is behind the board; in front, a plinth 0.06 high
    (u 1.29 to 2.22, v 0.01 to 0.235) with the pens' pot and the three pads at 1.0 of their size;
    the sweet jars: six of glass (2 mm shell, the sweets inside, a lid), two rows of three (u 2.50 to 2.85);
    the postcard rack at u 2.38 (try 1: 2.30: its pole stood on the mullion's edge) and the card spinner at u 3.12: chrome wire, a wire pocket for each face (a 2 mm rod bent in a U, 20 mm deep, 0.8 of the card's width),
    three cards deep, the two behind each front card 6 mm apart and 15 mm higher."""
    _setup()
    import random as _random
    from mathutils import Matrix, Vector
    import sw_prints as PR
    import sw_room_gen as RG
    rr = d.RR
    walls = rr["walls"]
    wall_rgb = RG._rgb(walls["above"])
    dado_rgb = RG._rgb(walls["dado"])
    d.tex_limit = 2048
    tex = d.tex
    bed_png = d.painted_png("bed_grey", "plywood", (150, 152, 150), grain=0.55)
    edge_png = d.painted_png("bed_edge", "plywood", (92, 62, 40), grain=0.8)
    d.start((150, 152, 150), wall_rgb, dado_rgb, bed_png=bed_png, board_png=edge_png)
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    GEN.TEXTS.clear()
    PR.TEXTS.clear()
    PR.USED.clear()
    PR.FIT.clear()
    # ---- the pictures: photographs and script (sw_prints)
    mag_p, pap_p, card_p, post_p, cart_p = [os.path.join(tex, n) for n in ("magazines.png", "papers.png", "cards.png", "postcards.png", "cartons.png")]
    mag_uv = PR.magazine_atlas(mag_p, 24)
    pap_uv = PR.paper_atlas(pap_p, 8)
    card_uv = PR.card_atlas(card_p, 10)
    post_uv = PR.postcard_atlas(post_p, 12)
    cart_uv = PR.carton_atlas(cart_p, 6)
    jc_uv, jl_uv = PR.jar_atlases(os.path.join(tex, "sweets.png"), os.path.join(tex, "jar_labels.png"), 10)
    PR.write_used(os.path.join(d.work, "prints_used.json"))
    # the white of the printed goods is held at about 0.86 of full in the window (newsprint is not paper white): under the gate's night spill the white card, paper and carton tops burnt (PIC-05g)
    from PIL import Image as _Im
    for _p, _k in ((pap_p, 0.86), (card_p, 0.80), (post_p, 0.82), (cart_p, 0.88), (mag_p, 0.80)):                 # try 2: the covers (a board leaning 35 degrees faces the ceiling lamps), the cards and the postcards are held lower: PIC-05g read 0.0100 to 0.0156 at the close cameras
        _a = np.asarray(_Im.open(_p).convert("RGB")).astype(np.float32) * _k
        _Im.fromarray(np.clip(_a, 0, 255).astype(np.uint8)).save(_p)
    mag_m = d.image_mat("magazines", mag_p, rough=0.45)
    pap_m = d.image_mat("papers", pap_p, rough=0.75)
    card_m = d.image_mat("greeting_cards", card_p, rough=0.55)
    post_m = d.image_mat("postcards", post_p, rough=0.55)
    cart_m = d.image_mat("cartons", cart_p, rough=0.5)
    sweets_m = d.image_mat("sweets", os.path.join(tex, "sweets.png"), rough=0.35)
    jlab_m = d.image_mat("jar_labels", os.path.join(tex, "jar_labels.png"), rough=0.6)
    glass_m = d.mat("jar_glass", (0.96, 0.98, 0.98), rough=0.05, glass=True)
    lid_m = d.mat("jar_lid", rgb8(190, 190, 186), rough=0.3, metal=0.9)
    chrome = d.mat("chrome_wire", rgb8(200, 200, 205), rough=0.25, metal=1.0)
    # supports: painted board (grey) and deal, both from the plywood map
    grey_png, grey_strips = d.wood_strips("news_grey", 6, (150, 146, 136), var=0.04, seed=12)
    deal_png, deal_strips = d.wood_strips("news_deal", 6, (150, 108, 70), var=0.06, seed=13)
    grey_m = d.image_mat("stand_grey", grey_png, rough=0.7)
    deal_m = d.image_mat("stand_wood", deal_png, rough=0.55)
    # ---- the two paper stands (a lower step, a higher step, a back board) and the eight papers, two to a step
    stands = []
    for ri, u0 in enumerate((0.10, 0.70)):
        gm = GM()
        x0, x1 = X(u0), X(u0 + 0.58)
        d.tex_box(gm, x0, x1, 0.04, 0.24, 0.0, 0.055, grey_strips, 6, rnd)           # the lower step (55 mm: a paper's top then stands under the riser's top edge)
        d.tex_box(gm, x0, x1, 0.24, 0.37, 0.0, 0.24, grey_strips, 6, rnd)            # the upper step
        d.tex_box(gm, x0, x1, 0.37, 0.382, 0.24, 0.46, grey_strips, 6, rnd)          # the back board over it
        d.gm_object("paper_stand_%d" % ri, gm, [grey_m], "support", "script:paper_stand")
        stands.append(u0)
    for ri, u0 in enumerate(stands):
        for st in range(2):
            for col in range(2):
                k = ri * 4 + st * 2 + col
                xc = X(u0 + 0.145 + 0.29 * col) + rnd.uniform(-0.0015, 0.0015)
                lean = 18.0 + rnd.uniform(-1.0, 1.0)
                yaw = rnd.uniform(-1.0, 1.0)
                foot_w = 0.055 if st == 0 else 0.24
                top_v = 0.24 if st == 0 else 0.37
                tile = pap_uv[k]
                make = lambda c, tile=tile, lean=lean, yaw=yaw: _csheet(c, 0.280, 0.19, 0.004, lean, yaw, 0.002, 0.006, 10, 6, mi=0, uv=tile, uv_other=(tile[0] + 0.01, tile[1] + 0.01), fold_top=True, curl=0.002)
                gm = d.lean_fit(make, xc, lean, foot_w, top_v)
                d.gm_object("newspaper_%d" % k, gm, [pap_m], "scripted", "script:newspapers", tier="bed" if st == 0 else "step")
    # ---- the stand with the cartons: a timber shelf on four legs, six cartons of 280 x 90 x 50 in two columns of three, fronts to the street
    sx0, sx1, sv0, sv1, sw = X(0.20), X(0.88), 0.39, 0.55, 0.46
    gm = GM()
    for xx in (sx0 + 0.015, sx1 - 0.015):
        for vv in (sv0 + 0.015, sv1 - 0.015):
            d.tex_box(gm, xx - 0.015, xx + 0.015, vv - 0.015, vv + 0.015, 0.0, sw, deal_strips, 6, rnd)
    d.tex_box(gm, sx0, sx1, sv0, sv1, sw, sw + 0.02, deal_strips, 6, rnd)
    d.gm_object("carton_stand", gm, [deal_m], "support", "script:carton_stand")
    xmid = (sx0 + sx1) / 2
    for col in range(2):
        for lay in range(3):
            kk = col * 3 + lay
            cg = GM()
            x0 = xmid - 0.285 + col * 0.290
            z0 = sw + 0.02 + lay * 0.09
            tu_, te_ = cart_uv[6 + kk], cart_uv[12 + kk]
            top_r = (tu_[0], tu_[3] - (100.0 / 180.0) * (tu_[3] - tu_[1]), tu_[2], tu_[3])                                         # the tile's top 560 x 100 px
            end_r = (te_[0], te_[3] - (100.0 / 180.0) * (te_[3] - te_[1]), te_[0] + (180.0 / 560.0) * (te_[2] - te_[0]), te_[3])        # the tile's top-left 180 x 100 px
            cg.box(x0, x0 + 0.28, sv0 + 0.04, sv0 + 0.09, z0, z0 + 0.0895, 0, uv_front=cart_uv[kk], uv_top=top_r, uv_ends=end_r, uv_other=(cart_uv[kk][0] + 0.01, cart_uv[kk][1] + 0.01))
            d.gm_object("carton_%d" % kk, cg, [cart_m], "scripted", "script:cigarette_cartons", tier="stand")
    # ---- the magazine board (a slab leaning 35 degrees back with a side cheek at each end), the plinth in front of it, the twelve covers
    mx0, mx1 = X(1.30), X(2.20)
    lean_b = 35.0
    vb, blen = 0.238, 0.56                                         # try 2: the foot at 0.238 (was 0.235): the top v 0.559 stays under 0.56
    cb, sb = math.cos(math.radians(lean_b)), math.sin(math.radians(lean_b))
    gm = GM()
    gm.sheet(((mx0 + mx1) / 2, vb + blen / 2 * sb, 0.004 + blen / 2 * cb), mx1 - mx0, blen, 0.012, tilt=lean_b, mi=0, uv=grey_strips[0], uv_other=(0.5, grey_strips[0][1] + 0.01))
    for xa in (mx0, mx1 - 0.012):                                  # the cheeks: triangles under the board's ends, sunk 3 mm into it (one mesh, so no overlap to test)
        vf, vt, wt, vbk = vb - 0.004, vb + blen * sb - 0.006, 0.004 + blen * cb - 0.004, 0.55
        gm.add([(xa, vf, 0.0), (xa + 0.012, vf, 0.0), (xa + 0.012, vt, wt), (xa, vt, wt), (xa, vbk, 0.0), (xa + 0.012, vbk, 0.0)],
               [(0, 3, 2, 1), (0, 1, 5, 4), (1, 2, 5), (0, 4, 3), (3, 4, 5, 2)], 0, [[(0.5, grey_strips[1][1] + 0.01)] * n_ for n_ in (4, 4, 3, 3, 4)])
    d.gm_object("magazine_board", gm, [grey_m], "support", "script:magazine_board")
    plg = GM()
    d.tex_box(plg, X(1.29), X(2.22), 0.032, 0.228, 0.0, 0.06, deal_strips, 6, rnd)            # 14 Oct, try 2 (DSP-03): the front edge 0.032 (the price cards stand at v 0.02), the back edge 0.228 (the lowest covers' foot is at 0.2327)
    d.gm_object("stationery_plinth", plg, [deal_m], "support", "script:crate")
    for row in range(3):
        for i in range(4):
            kk = row * 4 + i
            xc = (mx0 + mx1) / 2 + (i - 1.5) * 0.225
            s0 = 0.015 + row * 0.14 + 0.125
            off = 0.008 + 0.0045 * (2 - row)                          # from the board's middle: half its 12 mm, then the cover's middle plane 2 mm off its face; each LOWER row (row 0, the nearer to the street) 4.5 mm further out: it hides the foot of the row above and its own top rests 1.5 mm from that foot
            zc = 0.004 + s0 * cb + off * sb
            vc = vb + s0 * sb - off * cb
            tile = mag_uv[kk]
            gm = GM()
            gm.csheet((xc, vc, zc), 0.19, 0.25, 0.003, tilt=lean_b, yaw=rnd.uniform(-0.8, 0.8), bow=0.003, bend=0.0, nx=6, nz=4, mi=0, uv=tile, uv_other=(tile[0] + 0.01, tile[1] + 0.01))
            d.gm_object("magazine_%d" % kk, gm, [mag_m], "scripted", "script:magazines", tier="board")
    # ---- on the plinth: a pot of pens, then the yellow pad, the A4 stack and the note stack, each at its own size
    meshes_t, lo_t, hi_t = d.template("stationery_supplies")
    cupm = [m for m in meshes_t if "pencilcup" in m.name][0]
    cpts = [cupm.matrix_world @ Vector(c) for c in cupm.bound_box]
    ccx = (min(p.x for p in cpts) + max(p.x for p in cpts)) / 2
    ccy = (min(p.y for p in cpts) + max(p.y for p in cpts)) / 2
    cfloor = min(p.z for p in cpts) + 0.004
    pen_names = ["pen_blue", "pen_fancy", "pen_red", "pencil_new_a", "pencil_new_b", "pencil_old", "pencil_used"]
    parts = [(("pencilcup",), Matrix.Identity(4))]
    for i, nm in enumerate(pen_names):
        m = [mm for mm in meshes_t if mm.name.endswith(nm)][0]
        pts = [m.matrix_world @ Vector(c) for c in m.bound_box]
        piv = Vector((min(p.x for p in pts), (min(p.y for p in pts) + max(p.y for p in pts)) / 2, (min(p.z for p in pts) + max(p.z for p in pts)) / 2))
        phi = 2 * math.pi * i / 7
        base = Vector((ccx + 0.017 * math.cos(phi), ccy + 0.017 * math.sin(phi), cfloor))
        ax = Vector((-math.sin(phi), math.cos(phi), 0.0))
        xf = Matrix.Translation(base) @ Matrix.Rotation(math.radians(5.0 + 2.0 * (i % 3)), 4, ax) @ Matrix.Rotation(-math.pi / 2, 4, "Y") @ Matrix.Translation(-piv)
        parts.append(((nm,), xf))
    pot = d.compose("stationery_supplies", "pot0", parts)
    x_pad = 1.30
    for nm in ("office_notepads_yellow_pad", "office_notepads_a4_stack", "office_notepads_note_stack"):
        key = d.sub_template("office_notepads", nm, lambda n, nm=nm: n == nm)
        rt = (0, 0, math.pi / 2) if "note_stack" not in nm else (0, 0, 0)
        dd = d.dims(key, rt)
        psc = 0.95 if "note_stack" not in nm else 1.0                # try 2: a pad at 0.95 of the model's size (DSP-06 allows 0.9 to 1.1): its back edge must stay in front of the lowest covers (DSP-03)
        _, nms_ = d.piece(key, x_pad + dd.x * psc / 2, 0.035 + dd.y * psc / 2, 0.06, rot=rt, scale=psc, tier="plinth", tag=nm, tris=None)
        d.tone(nms_, 0.70)                                       # the pads burnt at night (the newsagent's close review, narrow 4): their white and yellow held at 0.86 (try 1) and at 0.70 (try 2: still burnt at 0.86 under the night spill, PIC-05g)
        x_pad += dd.x * psc + 0.006
    d.piece(pot, x_pad + 0.045, 0.10, 0.06, rot=(0, 0, 0), tier="plinth", tris=None)
    # ---- the sweet jars: glass, the sweets inside, a lid, the paper label outside
    gl, ct, ld, lb = GM(), GM(), GM(), GM()
    for k in range(6):
        row, col = divmod(k, 3)
        xc = X(2.50 + col * 0.14 + (0.07 if row else 0.0))
        yc = 0.20 + row * 0.12
        kj = (3, 5, 1, 0, 2, 4)[k]                        # 15 Oct, try 2 (the newsagent's street review, narrow 2: the front row read pale grey, saturation p90 0.19): FRUIT DROPS, SHERBET LEMONS and PEAR DROPS in front, HUMBUGS, MINT IMPERIALS and TOFFEES behind
        GEN.glass_jar(gl, ct, ld, lb, xc, yc, 0.0, uv_content=jc_uv[kj], uv_label=jl_uv[kj], n=24)
    d.gm_object("sweet_jar_glass", gl, [glass_m], "scripted", "script:sweet_jars", tier="bed", smooth=True)
    d.gm_object("sweet_jar_sweets", ct, [sweets_m], "support", "script:sweet_jars", smooth=True)
    d.gm_object("sweet_jar_lids", ld, [lid_m], "support", "script:sweet_jars", smooth=True)
    d.gm_object("sweet_jar_labels", lb, [jlab_m], "support", "script:sweet_jars")
    # ---- the postcard rack (u 2.38) and the card spinner (u 3.12): chrome wire, a pocket for each face, three cards deep
    for name, u, vc, w0, w1, n_face, tiers, uvs, tile_m_, cw_, ch_, rad in (("card_rack", 3.12, 0.36, 0.30, 1.10, 4, 4, card_uv, card_m, 0.115, 0.16, 0.09), ("postcard_rack", 2.38, 0.42, 0.50, 1.20, 8, 3, post_uv, post_m, 0.135, 0.094, 0.12)):
        xc = X(u)
        g = GM()
        g.rod((xc, vc, 0.0), (xc, vc, w1 + 0.05), 0.006, 0, 8)
        g.cylinder(xc, vc, 0.0, 0.012, 0.12, 0, 20)
        cgm = GM()
        cnt = 0
        zr_list = [w0 + (w1 - w0 - ch_) * ri / max(tiers - 1, 1) for ri in range(tiers)]
        for ri, zr in enumerate(zr_list):
            g.torus((xc, vc, zr - 0.002), rad, 0.0018, 0, axis="z", nm=24, nn=5)
            for sp in range(4):
                a_ = math.radians(90 * sp)
                g.rod((xc, vc, zr - 0.002), (xc + math.sin(a_) * rad, vc - math.cos(a_) * rad, zr - 0.002), 0.0015, 0, 6)
            for fi in range(n_face):
                ang = 360.0 * fi / n_face + (22.5 if n_face == 8 else 11.0) * ri                 # 15 Oct, try 2 (the newsagent's close review, narrow 1): the postcard rack's tiers are turned 22.5 degrees more each, so the pockets do not stand in columns
                a_ = math.radians(ang)
                ox, oy = math.sin(a_), -math.cos(a_)
                pw = 0.8 * (cw_ if n_face == 4 else cw_ * 0.8)
                d.wire_pocket(g, (xc + ox * rad, vc + oy * rad, zr - 0.0005), ang, pw, 0.020)
                for dep in range(3):                                  # three cards: the front one, two behind it 6 mm apart and 15 mm higher
                    rr_ = rad - 0.0045 - 0.006 * dep
                    kk = (ri * n_face * 3 + fi * 3 + dep) % len(uvs) if n_face != 8 else (8 * ri + fi + 4 * dep) % len(uvs)          # the postcard rack: the front card of pocket p on tier t is design (8t + p) mod 12, the two behind (+4, +8) (the same three cards stood on every tier)
                    cwid = cw_ if n_face == 4 else cw_ * 0.8
                    cgm.sheet((xc + ox * rr_, vc + oy * rr_, zr + ch_ / 2 + 0.0075 * dep + 0.0005), cwid, ch_ + 0.015 * dep, 0.003, tilt=0.0, yaw=ang, mi=0, uv=uvs[kk], uv_other=(uvs[kk][0] + 0.01, uvs[kk][1] + 0.01))
                    cnt += 1
        d.gm_object(name + "_frame", g, [chrome], "support", "script:" + name)
        d.gm_object(name, cgm, [tile_m_], "scripted", "script:" + ("card_rack" if n_face == 4 else "postcard_rack"), tier="rack")
    # ---- the price cards (hand cards on the bed's front edge)
    cards = [("PAPERS\nORDERED", 0.40), ("SWEETS\n2oz 25p", 2.69), ("CARDS\nFROM 25p", 3.12), ("MAGAZINES", 1.50), ("STATIONERY", 2.10), ("PENS & PADS", 1.80)]
    texts = [c[0] for c in cards]
    path = os.path.join(tex, "price_cards.png")
    uvs = GEN.card_atlas(path, texts, cols=3, tile=(256, 128), size=46)
    pm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    for k, (_, uc) in enumerate(cards):
        d.price_card(uc, 0.02, 0.0, k, uvs, pm)
    d.display_texts = list(GEN.TEXTS) + list(PR.TEXTS) + [t.replace("\n", " ") for t in texts]


def _csheet(c, w, h, t, tilt, yaw, bow_, bend_, nx, nz, mi=0, uv=None, uv_other=None, fold_top=False, curl=0.0):
    g = GM()
    g.csheet(c, w, h, t, tilt=tilt, yaw=yaw, bow=bow_, bend=bend_, nx=nx, nz=nz, mi=mi, uv=uv, uv_other=uv_other, fold_top=fold_top, curl=curl)
    return g
