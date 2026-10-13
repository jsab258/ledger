"""The tea rooms (west_north bay 2): the room's layout and the window display (13 October 2026, batch A). Read from `shops.tea_rooms.room` and `.display` in target.json; every choice the target left open
is stated in the docstrings (each a Judgement in NOTES.md and a `Changes after the build` line).

The target's rule (changes): NO Gothic chairs, NO empty frames, NO free tables in the picture (they smeared): the room is the counter, the hatch and the shelves on the back wall and flat boards; the one table
set is in the window, in real geometry in the middle light, and the café curtain hides the two outer lights.
"""
import math
import os

import sw_assets as A
import sw_gen as GEN
from sw_gen import GM

rgb8 = None


def _setup():
    global rgb8
    import sw_room as S
    rgb8 = S.rgb8


def _cup_unit(gm, cx, cy, z0, scale=1.0, mi=0):
    """A saucer with a cup on it: lathe forms (the target's `script:cups_saucers`: stacked cups and saucers, a glaze, no CC0 model beyond tea_set_01)."""
    s = scale
    sau = [(0.0, 0.0), (0.035 * s, 0.0), (0.060 * s, 0.006 * s), (0.078 * s, 0.014 * s), (0.078 * s, 0.017 * s), (0.060 * s, 0.010 * s), (0.030 * s, 0.009 * s), (0.0, 0.009 * s)]
    gm.lathe(cx, cy, z0, sau, mi=mi, n=22)
    cup = [(0.0, 0.0), (0.020 * s, 0.0), (0.026 * s, 0.006 * s), (0.044 * s, 0.040 * s), (0.047 * s, 0.062 * s), (0.044 * s, 0.062 * s), (0.040 * s, 0.050 * s), (0.0, 0.012 * s)]
    gm.lathe(cx, cy, z0 + 0.009 * s, cup, mi=mi, n=22)
    gm.torus((cx + 0.052 * s, cy, z0 + 0.009 * s + 0.040 * s), 0.016 * s, 0.0035 * s, mi, axis="y", nm=12, nn=5)


def _plate_stack(gm, cx, cy, z0, n, r=0.10, mi=0):
    for k in range(n):
        z = z0 + k * 0.0125
        gm.lathe(cx, cy, z, [(0.0, 0.0), (r * 0.55, 0.0), (r * 0.62, 0.004), (r, 0.010), (r, 0.0125), (r * 0.62, 0.0065), (0.0, 0.0065)], mi=mi, n=26)


# ---------------------------------------------------------------------------------------------------------------------------------- the room
def room(r):
    """The tea rooms' room (target `shops.tea_rooms.room`: fixtures T-*). What the target leaves open, and what this does:

    counter T-back-counter (x -2.55 to 0.45, 0.55 deep, 1.0 high; panelled front): left to right a cake dome over the carrot cake and another over the strawberry cake (the target counts one dome: two, one a
    cake), a board of two rolls of hamburger_buns, the tea set (the model is a kit of loose pieces laid in rows: a teapot, a sugar bowl, and two cups each on its own saucer, put together here), the
    vintage kettle, the till (0.42) and the tea urn (a script, 0.5 tall) at the right end where the upper shelf is the only thing above.
    shelf T-back-shelf (0.20 deep): the lower board (z 1.35) runs x -2.55 to -0.35 so that the urn (0.5 tall) and the till (0.42) stand under the upper one only (z 1.75, the whole 3.0 m); 24 cups
    and saucers (12 a board: script lathe forms), three stacks of plates on each and the metal jug.
    hatch T-back-hatch (x 1.2 to 2.4, z 0.95 to 1.85, 80 mm): a timber frame, the recess's tiled back, a ledge and the roller flap half down (slats).
    menu T-back-menu: a hung black board with the day's menu in chalk (a script picture) and a price card.
    left wall: the two hanging frames (picture_frame_02, _03: their prints are the project's own, made by the blanking step) and the wall clock; right wall: picture_frame_01 and a cork notice board.
    floor: the chequer (the cream and brown 300 mm). The counter's pilot lamp is the night_dark state's one warm point of light."""
    _setup()
    import sw_room_gen as RG
    from mathutils import Vector
    import bpy
    D, W = RG.D, RG.W
    rr = r.RR
    fx = r.fxd
    rnd = r.rnd
    tex = r.tex
    GEN.TEXTS.clear()
    china = r.mat("china", rgb8(236, 232, 220), rough=0.25)
    china_b = r.mat("china_band", rgb8(214, 206, 188), rough=0.25)
    steel = r.mat("stainless", rgb8(190, 192, 194), rough=0.28, metal=1.0)
    glass = r.mat("dome_glass", (0.9, 0.95, 0.95), rough=0.02, glass=True)
    brass = r.brass_m
    cream = r.mat("hatch_cream", rgb8(226, 216, 190), rough=0.5)
    # ---- the counter
    cx0, cx1, cy0, cy1, ch = r.counter("T-back-counter", panels=True)
    sx0, sx1 = fx["T-back-shelf"]["x"]
    r.shelf_unit("T-back-shelf", [(1.35, sx0, -0.60), (1.75, sx0, sx1)], bottom=ch)
    sd = fx["T-back-shelf"]["depth_m"]
    yb = D - sd - 0.02                       # in front of the shelf
    yc = D - 0.30                            # the middle of the counter's top
    # cake domes (glass over a cake on a stand plate), two
    cakes = [("carrot_cake", cx0 + 0.17), ("strawberry_chocolate_cake", cx0 + 0.59)]
    for nm, xc in cakes:
        gm = GM()
        gm.lathe(xc, yc, ch, [(0.0, 0.0), (0.05, 0.0), (0.06, 0.016), (0.15, 0.020), (0.15, 0.024), (0.0, 0.024)], mi=0, n=30)
        o = gm.to_object("cake_plate_%s" % nm, [china], r.sc, smooth=True)
        r.placed_rec("T-back-counter", "script:cake_dome", gm.extents(), [o.name], tag="plate")
        r.place(nm, (xc, yc, ch + 0.024), rot=(0, 0, rnd.uniform(0, 6.28)), scale=1.0, fixture="T-back-counter", anchor=("c", "c", "min"), tag="cake")
        dm = GM()
        prof = [(0.140, 0.024), (0.140, 0.130)] + [(0.140 * math.cos(a), 0.130 + 0.135 * math.sin(a)) for a in [math.pi / 2 * k / 12.0 for k in range(1, 13)]]
        dm.lathe(xc, yc, ch, prof, mi=0, n=30)
        o = dm.to_object("cake_dome_%s" % nm, [glass], r.sc, smooth=True)
        rim = GM()
        rim.lathe(xc, yc, ch, [(0.142, 0.024), (0.142, 0.036), (0.138, 0.036), (0.138, 0.024)], mi=0, n=30)
        rim.lathe(xc, yc, ch, [(0.0, 0.262), (0.014, 0.262), (0.014, 0.278), (0.0, 0.278)], mi=0, n=14)
        o2 = rim.to_object("cake_dome_rim_%s" % nm, [steel], r.sc, smooth=True)
        r.placed_rec("T-back-counter", "script:cake_dome", dm.extents(), [o.name, o2.name], tag="dome", n=1)
    # a board with two rolls of hamburger_buns
    x_b = cx0 + 0.80
    board_m = r.mat("bread_board", rgb8(176, 140, 92), rough=0.6)
    r.box("bread_board", x_b, x_b + 0.42, yc - 0.16, yc + 0.16, ch, ch + 0.016, board_m, fixture="T-back-counter")
    for k in range(2):
        r.place("hamburger_buns", (x_b + 0.21 + rnd.uniform(-0.005, 0.005), yc - 0.07 + 0.14 * k, ch + 0.016), rot=(0, 0, 0), scale=1.0, fixture="T-back-counter", anchor=("c", "c", "min"), tag="rolls")
    # the tea set, put together: a teapot, the sugar bowl, two cups on their saucers (the kit's pieces are laid in rows; the cups are moved onto the saucers)
    pot = r.sub_template("tea_set_01", "pot", lambda n: "teapot" in n)
    sug = r.sub_template("tea_set_01", "sugar", lambda n: "sugar" in n)
    cups = r.compose("tea_set_01", "cupA", [(("cup_small_01",), (0.0, 0.2335, 0.013)), (("saucer_circular_04",), (0.0, 0.0, 0.0))])
    cups2 = r.compose("tea_set_01", "cupB", [(("cup_small_02",), (0.0, 0.2335 - 0.0, 0.013)), (("saucer_circular_03",), (0.0, 0.0, 0.0))])
    xs = cx0 + 1.37
    r.place(pot, (xs, yc - 0.02, ch), rot=(0, 0, 0.3), scale=1.0, fixture="T-back-counter", anchor=("c", "c", "min"), tag="teapot")
    r.place(sug, (xs + 0.15, yc + 0.11, ch), rot=(0, 0, 0), scale=1.0, fixture="T-back-counter", anchor=("c", "c", "min"), tag="sugar")
    r.place(cups, (xs + 0.27, yc - 0.12, ch), rot=(0, 0, 0.5), scale=1.0, fixture="T-back-counter", anchor=("c", "c", "min"), tag="cup")
    r.place(cups2, (xs + 0.27, yc + 0.11, ch), rot=(0, 0, -0.4), scale=1.0, fixture="T-back-counter", anchor=("c", "c", "min"), tag="cup")
    # the kettle, the till, the urn
    r.place("vintage_electric_kettle", (cx0 + 2.00, yc - 0.04, ch), rot=(0, 0, math.radians(200)), scale=1.0, fixture="T-back-counter", anchor=("c", "c", "min"), tag="kettle")
    till_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "CashRegister_01") / max(r.dims("CashRegister_01"))
    # (the kettle is at x -0.05; the till and the urn follow it to the right under the upper board)
    # the urn: a stainless cylinder on a plinth, a lid with a knob, a tap with a lever, two side handles
    ux = cx1 - 0.15
    ug = GM()
    ug.lathe(ux, yc, ch, [(0.0, 0.0), (0.10, 0.0), (0.10, 0.03), (0.0, 0.03)], mi=0, n=26)
    ug.lathe(ux, yc, ch + 0.03, [(0.0, 0.0), (0.12, 0.0), (0.13, 0.02), (0.13, 0.36), (0.115, 0.40), (0.0, 0.40)], mi=0, n=26)
    ug.lathe(ux, yc, ch + 0.43, [(0.0, 0.0), (0.12, 0.0), (0.12, 0.02), (0.06, 0.04), (0.0, 0.045)], mi=0, n=26)
    ug.cylinder(ux, yc, ch + 0.475, ch + 0.495, 0.018, 0, 12)
    ug.rod((ux - 0.0, yc - 0.13, ch + 0.12), (ux - 0.0, yc - 0.18, ch + 0.12), 0.012, 0, 8)
    ug.rod((ux - 0.0, yc - 0.18, ch + 0.12), (ux - 0.0, yc - 0.18, ch + 0.17), 0.008, 0, 8)
    ug.rod((ux - 0.08, yc - 0.19, ch + 0.17), (ux + 0.08, yc - 0.19, ch + 0.17), 0.006, 0, 8)
    o = ug.to_object("tea_urn", [steel], r.sc, smooth=True)
    r.placed_rec("T-back-counter", "script:tea_urn", ug.extents(), [o.name], tag="urn")
    r.place("CashRegister_01", (cx1 - 0.55, D - 0.01, ch), rot=(0, 0, 0), scale=till_s, fixture="T-back-counter", anchor=("c", "max", "min"))
    # ---- the shelf's goods: 24 cups and saucers (12 a board), three stacks of plates a board, the metal jug
    glaze = r.mat("cup_glaze", rgb8(238, 234, 222), rough=0.2)
    for z, xa, xb, n_units, plates_at in ((1.35, sx0 + 0.04, -0.62, 10, (-0.88, -0.72)), (1.75, sx0 + 0.04, sx1 - 0.04, 14, (-0.32, -0.12, 0.08))):
        gm = GM()
        yb_ = D - sd + 0.085
        pitch = 0.15 if z < 1.5 else 0.145
        for k in range(n_units):
            _cup_unit(gm, xa + 0.08 + k * pitch + rnd.uniform(-0.002, 0.002), yb_, z)
        o = gm.to_object("cups_%.2f" % z, [glaze], r.sc, smooth=True)
        r.placed_rec("T-back-shelf", "script:cups_saucers", gm.extents(), [o.name], tag="cups_%.2f" % z, n=n_units)
        pg = GM()
        for xp in plates_at:
            _plate_stack(pg, xp, yb_, z, rnd.randint(4, 6), 0.095)
        o = pg.to_object("plates_%.2f" % z, [glaze], r.sc, smooth=True)
        r.placed_rec("T-back-shelf", "script:cups_saucers", pg.extents(), [o.name], tag="plates_%.2f" % z, n=0)
    r.place("metal_jug", (sx1 - 0.13, D - sd + 0.10, 1.75), rot=(0, 0, 0.4), scale=1.0, fixture="T-back-shelf", anchor=("c", "c", "min"), tag="jug")
    # ---- the hatch (flat, 80 mm): frame, tiled recess, ledge, the roller flap half down
    hx0, hx1 = fx["T-back-hatch"]["x"]
    hz0, hz1 = fx["T-back-hatch"]["z"]
    fm = 0.07
    r.box("hatch_frame_l", hx0, hx0 + fm, D - 0.08, D - 0.005, hz0, hz1, cream, fixture="T-back-hatch")
    r.box("hatch_frame_r", hx1 - fm, hx1, D - 0.08, D - 0.005, hz0, hz1, cream, fixture="T-back-hatch")
    r.box("hatch_frame_t", hx0 + fm, hx1 - fm, D - 0.08, D - 0.005, hz1 - fm, hz1, cream, fixture="T-back-hatch")
    r.box("hatch_frame_b", hx0 + fm, hx1 - fm, D - 0.08, D - 0.005, hz0, hz0 + 0.03, cream, fixture="T-back-hatch")
    tile = r.mat("hatch_tile", rgb8(232, 230, 220), rough=0.35)
    r.box("hatch_back", hx0 + fm, hx1 - fm, D - 0.012, D - 0.008, hz0 + 0.03, hz1 - fm, tile, fixture="T-back-hatch")
    r.box("hatch_ledge", hx0 + fm, hx1 - fm, D - 0.08, D - 0.02, hz0 + 0.03, hz0 + 0.045, cream, fixture="T-back-hatch")
    fl = GM()
    z_flap_top = hz1 - fm
    for k in range(9):
        za = z_flap_top - 0.045 * (k + 1)
        fl.box(hx0 + fm + 0.01, hx1 - fm - 0.01, D - 0.074, D - 0.060, za + 0.004, za + 0.043, 0)
    fl.box(hx0 + fm + 0.01, hx1 - fm - 0.01, D - 0.076, D - 0.058, z_flap_top - 0.045 * 9 - 0.014, z_flap_top - 0.045 * 9 - 0.002, 0)
    flap_m = r.mat("hatch_flap", rgb8(196, 196, 188), rough=0.35, metal=0.6)
    o = fl.to_object("hatch_flap", [flap_m], r.sc)
    r.fixtures.append({"fixture": "T-back-hatch", "name": "hatch_flap", "ext": [round(v, 4) for v in fl.extents()]})
    # ---- the menu board (flat 30 mm) and its price card
    mx0, mx1 = fx["T-back-menu"]["x"]
    mz0, mz1 = fx["T-back-menu"]["z"]
    mp = os.path.join(tex, "menu.png")
    muv = GEN.card_atlas(mp, ["TODAY'S MENU\nTEA 25p\nCOFFEE 35p\nTOAST 30p", "EGG & CHIPS £1.80\nSOUP 65p\nTEACAKE 40p", "BREAKFASTS\nLUNCHES\nTEAS"], cols=1, tile=(420, 420), size=44, bg=(34, 36, 38), ink=(236, 232, 220))
    GEN.TEXTS.extend(["TODAY'S MENU", "TEA 25p", "COFFEE 35p", "TOAST 30p", "EGG & CHIPS", "SOUP 65p", "TEACAKE 40p", "BREAKFASTS", "LUNCHES", "TEAS"])
    mm = r.image_mat("menu_board", mp, rough=0.8)
    frame_m = r.mat("menu_frame", rgb8(110, 70, 42), rough=0.5)
    r.box("menu_frame", mx0, mx1, D - 0.03, D - 0.018, mz0 + 0.12, mz1 - 0.06, frame_m, fixture="T-back-menu")
    mg = GM()
    mg.box(mx0 + 0.02, mx1 - 0.02, D - 0.0325, D - 0.0305, mz0 + 0.14, mz1 - 0.08, 0, uv_front=muv[0])
    r.fixtures.append({"fixture": "T-back-menu", "name": "menu_chalk", "ext": [mx0 + 0.02, mx1 - 0.02, D - 0.0325, D - 0.0305, mz0 + 0.14, mz1 - 0.08]})
    mo = mg.to_object("menu_chalk", [mm], r.sc)
    pg = GM()
    pg.box(mx0 + 0.07, mx1 - 0.07, D - 0.0325, D - 0.0305, mz0 + 0.01, mz0 + 0.10, 0, uv_front=muv[2])
    po = pg.to_object("menu_card", [mm], r.sc)
    r.fixtures.append({"fixture": "T-back-menu", "name": "menu_card", "ext": [mx0 + 0.07, mx1 - 0.07, D - 0.0325, D - 0.0305, mz0 + 0.01, mz0 + 0.10]})
    # ---- the left wall: two frames and the clock; the right wall: a frame and a notice board
    xl, xr = -W / 2, W / 2
    ky0, ky1 = fx["T-left-frames"]["y"]
    r.place("hanging_picture_frame_02", (xl + 0.022, 1.50, 1.70), rot=(0, 0, math.pi / 2), scale=1.0, fixture="T-left-frames", anchor=("min", "c", "c"), tag="frame")
    r.place("hanging_picture_frame_03", (xl + 0.022, 2.30, 1.70), rot=(0, 0, math.pi / 2), scale=1.0, fixture="T-left-frames", anchor=("min", "c", "c"), tag="frame")
    ck_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "wall_clock") / max(r.dims("wall_clock"))
    r.place("wall_clock", (xl + 0.022, 2.95, 1.78), rot=(0, 0, math.pi / 2), scale=ck_s, fixture="T-left-frames", anchor=("min", "c", "c"), clock=r.next_clock(), tag="clock")
    r.place("hanging_picture_frame_01", (xr - 0.022, 2.30, 1.58), rot=(0, 0, -math.pi / 2), scale=1.0, fixture="T-right-frames", anchor=("max", "c", "c"), tag="frame")
    cork = r.mat("cork", rgb8(170, 126, 84), rough=0.9)
    r.box("notice_board", xr - 0.034, xr - 0.012, 1.15, 1.80, 1.30, 1.95, cork, fixture="T-right-frames")
    np_ = os.path.join(tex, "notices.png")
    nuv = GEN.card_atlas(np_, ["TABLES\nBOOKED", "TEAS FROM\n25p", "OPEN\n6.30 - 10", "CAKES\nMADE HERE", "THANK\nYOU", "LUNCH\n12 - 2"], cols=3, tile=(256, 160), size=34)
    GEN.TEXTS.extend(["TABLES BOOKED", "TEAS FROM 25p", "OPEN 6.30 - 10", "CAKES MADE HERE", "THANK YOU", "LUNCH 12 - 2"])
    nm_ = r.image_mat("notices", np_, rough=0.8)
    ng = GM()
    for k, (yy, zz) in enumerate(((1.28, 1.74), (1.52, 1.74), (1.28, 1.48), (1.52, 1.48), (1.66, 1.62), (1.38, 1.60))):
        ng.box(xr - 0.0385, xr - 0.0345, yy - 0.08 + 0.0 * k, yy + 0.08 - (0.03 if k == 4 else 0.0), zz - 0.05, zz + 0.05, 0, uv_front=nuv[k % 6], front="-x")
    no = ng.to_object("notices", [nm_], r.sc)
    r.placed_rec("T-right-frames", "script:window_card_menu", ng.extents(), [no.name], tag="notices", n=6)
    # ---- the counter's pilot lamp: a warm point light for night_dark (the target's `night_dark`: the counter's pilot lamp)
    ld = bpy.data.lights.new("pilot", "POINT")
    ld.energy = 0.0
    ld.color = (1.0, 0.72, 0.45)
    ld.shadow_soft_size = 0.05
    po_ = bpy.data.objects.new("pilot", ld)
    r.sc.collection.objects.link(po_)
    po_.location = (cx0 + 0.10, D - 0.30, ch + 0.20)
    r.pilot = po_
    r.pilot_w = 6.0
    r.notes.append("two cake domes (a cake each: the target counts one dome), glass over the cakes with the shadow-ray trick; the tea set's loose pieces put together by `compose`; the pilot lamp is a point light in night_dark only")
    r.texts = list(GEN.TEXTS)
    return r


# ---------------------------------------------------------------------------------------------------------------------------------- the window
def display(d):
    """The tea rooms' window (target `shops.tea_rooms.display`, 10 item rows; bed 3.35 x 0.55): the café curtain on its brass rod over the two outer lights (z 1.50 above the footway, so w 0.90 above the bed;
    it hangs 0.55 to w 0.35), the table set for tea in the middle light (u 1.16 to 2.19), the cakes under the curtain's hem on the bed, the potted plant in the right light, the hand-lettered card on the
    glass. What the target left open: the table is scaled to 0.50 m (the target asks 0.55, which leaves no air at the glass and none at the back), the chairs to 0.75 (a cafe pair for a window 0.55 deep: at the table's sides, their front legs under its edge), the
    cakes on the bed under the curtain (the carrot cake on a two-tier china stand, the strawberry cake on a plain plate), a sugar bowl and a menu stand."""
    _setup()
    import sw_room_gen as RG
    rr = d.RR
    walls = rr["walls"]
    d.start((122, 96, 64), RG._rgb(walls["above"]), RG._rgb(walls["dado"]))      # a dark stained deal bed: the first (176, 144, 100) burnt under the gate's night spill (PIC-05g read 0.028)
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    tex = d.tex
    GEN.TEXTS.clear()
    china = d.mat("china", rgb8(208, 204, 194), rough=0.25)      # toned: pure white china burns under the gate's night spill (PIC-05g)
    steel = d.mat("stainless", rgb8(190, 192, 194), rough=0.28, metal=1.0)
    brass = d.mat("brass", rgb8(160, 120, 55), rough=0.3, metal=1.0)
    # the table (a cafe table 0.55 across), its laminate top, two chairs, the tea set in pieces
    ts = 0.50 / max(d.dims("round_wooden_table_02").x, d.dims("round_wooden_table_02").y)
    tu, tv = 1.675, 0.27
    d.piece("round_wooden_table_02", tu, tv, 0.0, rot=(0, 0, 0), scale=ts, tier="bed", tris=None)
    d.tone(d.last_objs, 2.2)                    # the walnut's pedestal read 0.18 to 0.25 of the room at night (LIT-08): a pale-stained oak
    tab_ext = d.items[-1]["ext"]
    top_z = tab_ext[5]
    lam = d.mat("laminate", rgb8(160, 142, 106), rough=0.35)
    lg = GM()
    rt = 0.25
    lg.lathe(X(tu), tv, top_z, [(0.0, 0.0), (rt, 0.0), (rt, 0.008), (rt - 0.004, 0.012), (0.0, 0.012)], mi=0, n=36)
    d.gm_object("table_laminate", lg, [lam], "support", "script:table_laminate", smooth=True)
    top_z += 0.012
    cs = 0.75
    d.piece("painted_wooden_chair_01", tu - 0.462, tv, 0.0, rot=(0, 0, -math.pi / 2), scale=cs, tier="bed", tris=None)
    d.tone(d.last_objs, 0.78)                   # the white paint burnt on the seats under the gate's night spill (PIC-05g)
    d.piece("painted_wooden_chair_01", tu + 0.462, tv, 0.0, rot=(0, 0, math.pi / 2), scale=cs, tier="bed", tris=None)
    pot = d.sub_template("tea_set_01", "pot", lambda n: "teapot" in n)
    sug = d.sub_template("tea_set_01", "sugar", lambda n: "sugar" in n)
    cupa = d.compose("tea_set_01", "cupA", [(("cup_small_01",), (0.0, 0.2335, 0.013)), (("saucer_circular_04",), (0.0, 0.0, 0.0))])
    cupb = d.compose("tea_set_01", "cupB", [(("cup_small_02",), (0.0, 0.2335, 0.013)), (("saucer_circular_03",), (0.0, 0.0, 0.0))])
    d.piece(pot, tu - 0.05, tv + 0.0, top_z, rot=(0, 0, 0.3), tier="table", tris=None)
    d.piece(cupa, tu + 0.12, tv - 0.12, top_z, rot=(0, 0, 0.5), tier="table", tris=None)
    d.piece(cupb, tu + 0.10, tv + 0.12, top_z, rot=(0, 0, -0.4), tier="table", tris=None)
    # the sugar bowl and the menu stand (script: small lathe and card)
    sg = GM()
    sg.lathe(X(tu - 0.16), tv + 0.14, top_z, [(0.0, 0.0), (0.025, 0.0), (0.040, 0.012), (0.042, 0.040), (0.030, 0.046), (0.0, 0.046)], mi=0, n=18)
    sg.lathe(X(tu - 0.16), tv + 0.14, top_z + 0.046, [(0.0, 0.0), (0.032, 0.0), (0.030, 0.012), (0.004, 0.018), (0.0, 0.026)], mi=0, n=18)
    d.gm_object("sugar_bowl", sg, [china], "scripted", "script:sugar_bowl_menu", tier="table", smooth=True)
    mp = os.path.join(tex, "menu_stand.png")
    muv = GEN.card_atlas(mp, ["TEAS\nFROM 25p"], cols=1, tile=(256, 160), size=40, bg=(206, 200, 180))
    GEN.TEXTS.extend(["TEAS FROM 25p"])
    mm = d.image_mat("menu_stand", mp, rough=0.8)
    mg = GM()
    mg.sheet((X(tu - 0.10), tv - 0.19, top_z + 0.045), 0.070, 0.050, 0.002, tilt=12.0, mi=0, uv=muv[0], uv_other=(muv[0][0] + 0.01, muv[0][1] + 0.01))
    d.gm_object("menu_stand", mg, [mm], "scripted", "script:sugar_bowl_menu", tier="table")
    # the carrot cake on a two-tier china stand; the strawberry cake on a plate
    ug = GM()
    ux = X(0.40)
    ug.lathe(ux, 0.32, 0.0, [(0.0, 0.0), (0.12, 0.0), (0.12, 0.012), (0.03, 0.02), (0.012, 0.055), (0.012, 0.09), (0.02, 0.095), (0.16, 0.105), (0.16, 0.115), (0.0, 0.115)], mi=0, n=30)
    d.gm_object("cake_stand", ug, [china], "scripted", "script:cake_stand", tier="bed", smooth=True)
    d.piece("carrot_cake", 0.40, 0.32, 0.115, rot=(0, 0, 1.0), tier="stand", tris=None)
    pg = GM()
    px = X(2.62)
    pg.lathe(px, 0.30, 0.0, [(0.0, 0.0), (0.06, 0.0), (0.07, 0.016), (0.17, 0.020), (0.17, 0.024), (0.0, 0.024)], mi=0, n=30)
    d.gm_object("cake_plate", pg, [china], "support", "script:cake_stand", smooth=True)
    d.piece("strawberry_chocolate_cake", 2.62, 0.30, 0.024, rot=(0, 0, 0.7), tier="plate", tris=None)
    d.piece("potted_plant_04", 3.10, 0.28, 0.0, rot=(0, 0, 0.3), tier="bed", tris=None)
    # the café curtain: a brass rod at w 0.90 and two panels (cream cotton gathered in folds, a scalloped hem) hung 0.55, over the two outer lights (u 0.05 to 1.09 and 2.27 to 3.30)
    rod_w = 0.90
    cur_m = d.mat("cafe_curtain", rgb8(208, 200, 178), rough=0.9)
    for side, (ua, ub) in (("l", (0.04, 1.10)), ("r", (2.26, 3.31))):
        g = GM()
        g.rod((X(ua - 0.01), 0.07, rod_w + 0.012), (X(ub + 0.01), 0.07, rod_w + 0.012), 0.008, 0, 10)
        for xx in (ua - 0.01, ub + 0.01):
            g.rod((X(xx), 0.07, rod_w + 0.012), (X(xx), 0.07, rod_w + 0.012 + 0.04), 0.004, 0, 6)
        d.gm_object("curtain_rod_" + side, g, [brass], "support", "script:cafe_curtain")
        cg = GM()
        cg.cloth(X(ua), X(ub), rod_w - 0.01, 0.55, 0.075, 0.016, 0.085, 0.10, nz=10, mi=0)
        d.gm_object("curtain_" + side, cg, [cur_m], "scripted", "script:cafe_curtain", tier="curtain")
    # the hand-lettered card on the glass's inside (BREAKFASTS, LUNCHES, TEAS), on two suction cups
    cp = os.path.join(tex, "window_card.png")
    cuv = GEN.card_atlas(cp, ["BREAKFASTS\nLUNCHES\nTEAS"], cols=1, tile=(512, 320), size=58, bg=(206, 200, 180))
    GEN.TEXTS.extend(["BREAKFASTS", "LUNCHES", "TEAS"])
    cm = d.image_mat("window_card", cp, rough=0.7)
    wg = GM()
    wg.box(X(2.50), X(3.10), 0.040, 0.044, 0.90, 1.28, 0, uv_front=cuv[0])
    d.gm_object("window_card_menu", wg, [cm], "scripted", "script:window_card_menu", tier="glass")
    cupm = d.mat("suction", rgb8(60, 60, 62), rough=0.4)
    sc_ = GM()
    for xx in (2.55, 3.05):
        sc_.cylinder(X(xx), 0.020, 1.24, 1.27, 0.014, 0, 10)
        sc_.rod((X(xx), 0.02, 1.255), (X(xx), 0.0395, 1.255), 0.003, 0, 6)
    d.gm_object("window_card_cups", sc_, [cupm], "support", "script:window_card_menu")
    # the price cards
    texts = ["CAKES 40p", "TEAS 25p", "TOAST 30p", "HOME MADE"]
    path = os.path.join(tex, "price_cards.png")
    uvs = GEN.card_atlas(path, texts, cols=2, tile=(256, 128), size=46, bg=(206, 200, 180))
    pm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    for k, uc in enumerate((0.70, 2.00, 2.90, 1.25)):
        d.price_card(uc, 0.02, 0.0, k, uvs, pm)
    d.display_texts = list(GEN.TEXTS) + [t for t in texts]
