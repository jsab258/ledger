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
    import sw_prints as PR
    PR.TEXTS.clear()
    mcp = PR.menu_card_png(os.path.join(tex, "menu_card.png"))                      # try 2 (the close review, narrow 6): paper (235, 232, 222), ink (25, 25, 50), one line of 14 characters at most
    mcm = r.image_mat("menu_card_paper", mcp, rough=0.8)
    pg = GM()
    pg.box(mx0 + 0.07, mx1 - 0.07, D - 0.0325, D - 0.0305, mz0 + 0.01, mz0 + 0.10, 0, uv_front=(0.0, 0.0, 1.0, 1.0))
    po = pg.to_object("menu_card", [mcm], r.sc)
    r.fixtures.append({"fixture": "T-back-menu", "name": "menu_card", "ext": [mx0 + 0.07, mx1 - 0.07, D - 0.0325, D - 0.0305, mz0 + 0.01, mz0 + 0.10]})
    # ---- the left wall: two frames and the clock; the right wall: a frame and a notice board
    xl, xr = -W / 2, W / 2
    ky0, ky1 = fx["T-left-frames"]["y"]
    r.place("hanging_picture_frame_02", (xl + 0.022, 1.50, 1.70), rot=(0, 0, math.pi / 2), scale=1.0, fixture="T-left-frames", anchor=("min", "c", "c"), tag="frame")
    r.place("hanging_picture_frame_03", (xl + 0.022, 2.30, 1.70), rot=(0, 0, math.pi / 2), scale=1.0, fixture="T-left-frames", anchor=("min", "c", "c"), tag="frame")
    ck_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "wall_clock") / max(r.dims("wall_clock"))
    r.place("wall_clock", (xl + 0.022, 2.95, 1.78), rot=(0, 0, math.pi / 2), scale=ck_s, fixture="T-left-frames", anchor=("min", "c", "c"), clock=r.next_clock(), tag="clock")
    r.place("hanging_picture_frame_01", (xr - 0.022, 2.30, 1.58), rot=(0, 0, -math.pi / 2), scale=1.0, fixture="T-right-frames", anchor=("max", "c", "c"), tag="frame")
    # the cork notice board (try 2, the close review narrow 7: "a flat orange slab"): a granular cork made by script, a 20 x 15 mm pine frame, a pin in each notice
    cork_p = PR.cork_png(os.path.join(tex, "cork.png"))
    cork = r.image_mat("cork", cork_p, tile_m=0.30, rough=0.95)
    pine = r.mat("pine_frame", rgb8(200, 160, 110), rough=0.5)
    bx0, bx1, bz0, bz1 = 1.15, 1.80, 1.30, 1.95
    r.box("notice_board", xr - 0.030, xr - 0.012, bx0 + 0.02, bx1 - 0.02, bz0 + 0.02, bz1 - 0.02, cork, fixture="T-right-frames")
    r.box("notice_frame_top", xr - 0.034, xr - 0.011, bx0, bx1, bz1 - 0.02, bz1, pine, fixture="T-right-frames")
    r.box("notice_frame_bottom", xr - 0.034, xr - 0.011, bx0, bx1, bz0, bz0 + 0.02, pine, fixture="T-right-frames")
    r.box("notice_frame_front", xr - 0.034, xr - 0.011, bx0, bx0 + 0.02, bz0 + 0.02, bz1 - 0.02, pine, fixture="T-right-frames")
    r.box("notice_frame_back", xr - 0.034, xr - 0.011, bx1 - 0.02, bx1, bz0 + 0.02, bz1 - 0.02, pine, fixture="T-right-frames")
    np_ = os.path.join(tex, "notices.png")
    nuv = PR.notice_atlas(np_, 6)
    nm_ = r.image_mat("notices", np_, rough=0.8)
    ng = GM()
    pin_cols = [rgb8(190, 40, 40), rgb8(40, 80, 170), rgb8(220, 190, 50), rgb8(40, 130, 70)]
    for k, (yy, zz) in enumerate(((1.28, 1.74), (1.52, 1.74), (1.28, 1.48), (1.52, 1.48), (1.66, 1.62), (1.38, 1.60))):
        ng.box(xr - 0.0338, xr - 0.0300, yy - 0.08 + 0.0 * k, yy + 0.08 - (0.03 if k == 4 else 0.0), zz - 0.05, zz + 0.05, 0, uv_front=nuv[k % 6], front="-x")
        r.cyl("pin_%d" % k, xr - 0.0338 - 0.002, yy - (0.015 if k == 4 else 0.0), zz + 0.04, 0.003, 0.004, r.mat("pin_%d" % k, pin_cols[k % 4], rough=0.3), axis="x", verts=10)
    no = ng.to_object("notices", [nm_], r.sc)
    r.placed_rec("T-right-frames", "script:window_card_menu", ng.extents(), [no.name], tag="notices", n=6)
    GEN.TEXTS.extend(list(PR.TEXTS))
    # ---- the counter's pilot lamp: a warm point light for night_dark (the target's `night_dark`: the counter's pilot lamp)
    ld = bpy.data.lights.new("pilot", "POINT")
    ld.energy = 0.0
    ld.color = (1.0, 0.72, 0.45)
    ld.shadow_soft_size = 0.05
    po_ = bpy.data.objects.new("pilot", ld)
    r.sc.collection.objects.link(po_)
    # try 2 (the close review, narrow 10: "a hot glow on the plaster with no fitting to cast it"): a 10 mm amber indicator lens on the tea urn's plinth, emission 2700 K, the light 0.02 m in front of it at 0.5 W
    lens_m = r.mat("pilot_lens", rgb8(255, 150, 40), rough=0.2, emit=(1.0, 0.6, 0.2), emit_strength=3.0)
    lens_x, lens_y, lens_z = ux, yc - 0.101, ch + 0.015
    r.cyl("pilot_lens", lens_x, lens_y, lens_z, 0.005, 0.004, lens_m, axis="y", verts=14)
    po_.location = (lens_x, lens_y - 0.02, lens_z)
    r.pilot = po_
    r.pilot_w = 0.5
    r.notes.append("two cake domes (a cake each: the target counts one dome), glass over the cakes with the shadow-ray trick; the tea set's loose pieces put together by `compose`; the pilot lamp is a point light in night_dark only")
    r.texts = list(GEN.TEXTS)
    return r


# ---------------------------------------------------------------------------------------------------------------------------------- the window
def display(d):
    """The tea rooms' window (target `shops.tea_rooms.display`, 10 item rows; bed 3.35 x 0.55), try 2 (14 Oct 2026: both fresh reviews of try 1; the brief's step 0 e, f, g, i and the tea rooms' list): the café curtain on its
    brass rod over the two outer lights (the rod at w 0.90, the cloth hangs 0.55), the table set for tea in the middle light, the cakes under the curtain's hem on the bed, the potted plant in the right light, the
    hand-lettered card on the glass. Everything at its own size (DSP-06):
    the table: a SCRIPTED Formica café table (the research's: a 1980s caff, not a walnut occasional table): a round laminate top 0.50 across, 25 mm thick (its surface at w 0.74), a 3 mm aluminium edge band, a 50 mm chrome
    column and a black cast base of four arms 0.40 across turned 45 degrees (so its tips stand clear of the chairs' front legs); the chairs: the model at 1.0 (0.956 high, the seat 0.453), left at u 1.215 (rot +90) and right
    at u 2.135 (rot -90), both at v 0.32, FACING the table, each seat's front edge 0.06 m under the table's rim; the teapot, cups and sugar bowl stand on the top at their own size; the menu stand is a tent card
    (two sheets leaning toward each other);
    the curtains: cream cotton (a weave picture, translucent: transmission 0.3, sheen) gathered in folds of random width and depth, a scalloped head on tabs folded over a brass rod (9 mm), a turned hem, brass end
    brackets (a 16 mm socket on a 70 mm arm, its plate on the back of the jamb or the mullion);
    the window card: 0.60 x 0.38 bowed 1.5 mm, hand lettering with a per-letter jitter on a paper with a grain, held by two clear PVC suction cups (30 mm, flat on the glass) with a steel hook each;
    the price cards: before their goods, none within 0.10 m of a chair or the table: CAKES 40p and HOME MADE at the carrot cake (u 0.50 and 0.30), TEAS 25p at u 0.80, GATEAU 45p at the strawberry cake's plate (u 2.62)."""
    _setup()
    from mathutils import Matrix
    import sw_room_gen as RG
    rr = d.RR
    walls = rr["walls"]
    d.tex_limit = 1024
    tex = d.tex
    bed_png = d.painted_png("bed_deal", "plywood", (122, 96, 64), grain=1.0)
    d.start((122, 96, 64), RG._rgb(walls["above"]), RG._rgb(walls["dado"]), bed_png=bed_png, board_png=d.painted_png("bed_edge_t", "plywood", (92, 62, 40), grain=0.8))
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    GEN.TEXTS.clear()
    china = d.mat("china", rgb8(208, 204, 194), rough=0.25)      # toned: pure white china burns under the gate's night spill (PIC-05g)
    steel = d.mat("stainless", rgb8(190, 192, 194), rough=0.28, metal=1.0)
    brass = d.mat("brass", rgb8(160, 120, 55), rough=0.45, metal=1.0)
    chrome = d.mat("chrome", rgb8(200, 200, 205), rough=0.25, metal=1.0)
    cast = d.mat("cast_black", rgb8(28, 28, 30), rough=0.5)
    alum = d.mat("alu_edge", rgb8(196, 198, 200), rough=0.3, metal=1.0)
    # ---- the table: a scripted Formica cafe table at real height (surface 0.74)
    tu, tv = 1.675, 0.27
    xt = X(tu)
    top_surface = 0.74
    lam_png = GEN.formica_png(os.path.join(tex, "formica.png"), (142, 126, 94))                  # toned to (142, 126, 94): the laminate burnt under the spill (PIC-05g read 0.0100 at CLOSE_35_B)
    lam = d.image_mat("laminate", lam_png, rough=0.35)
    lg = GM()
    rt = 0.25
    z0_, z1_ = top_surface - 0.025, top_surface
    nseg = 48
    ring_t = [(xt + rt * math.cos(2 * math.pi * k / nseg), tv + rt * math.sin(2 * math.pi * k / nseg)) for k in range(nseg)]
    V_ = [(xt, tv, z1_)] + [(x, y, z1_) for x, y in ring_t] + [(xt, tv, z0_)] + [(x, y, z0_) for x, y in ring_t]
    F_, U_ = [], []
    for k in range(nseg):
        k2 = (k + 1) % nseg
        F_.append((0, 1 + k, 1 + k2))                                                   # the top (faces up): a fan, the picture laid flat over it
        U_.append([(0.5, 0.5), (0.5 + (ring_t[k][0] - xt) / 0.5, 0.5 + (ring_t[k][1] - tv) / 0.5), (0.5 + (ring_t[k2][0] - xt) / 0.5, 0.5 + (ring_t[k2][1] - tv) / 0.5)])
        F_.append((nseg + 1, nseg + 2 + k2, nseg + 2 + k))                              # the underside
        U_.append([(0.5, 0.5)] * 3)
        F_.append((1 + k, nseg + 2 + k, nseg + 2 + k2, 1 + k2))                         # the side
        U_.append([(k / float(nseg), 0.0), (k / float(nseg), 0.05), ((k + 1) / float(nseg), 0.05), ((k + 1) / float(nseg), 0.0)])
    # 14 Oct, try 2 (DSP-03: the 3 mm edge band and the disc were two meshes in contact and read as intersecting): ONE mesh, the top laminate (material 0) over a disc whose side and underside are the aluminium edge (material 1)
    top_f = [f for f in F_ if f[0] == 0]
    top_u = [u for f, u in zip(F_, U_) if f[0] == 0]
    rest_f = [f for f in F_ if f[0] != 0]
    rest_u = [u for f, u in zip(F_, U_) if f[0] != 0]
    lg.add(V_, top_f, 0, top_u)
    lg.add(V_, rest_f, 1, rest_u)
    d.gm_object("table_laminate", lg, [lam, alum], "support", "script:table_laminate", smooth=False)
    cg = GM()
    cg.lathe(xt, tv, 0.03, [(0.0, 0.0), (0.025, 0.0), (0.025, top_surface - 0.025 - 0.03), (0.0, top_surface - 0.025 - 0.03)], mi=0, n=20)
    d.gm_object("table_column", cg, [chrome], "support", "script:table_column", smooth=True)
    bg = GM()
    bg.lathe(xt, tv, 0.0, [(0.0, 0.0), (0.05, 0.0), (0.045, 0.03), (0.0, 0.03)], mi=0, n=20)
    for ang in (45.0, 135.0):                                    # two crossed bars: four arms 0.40 across, 30 mm high, turned 45 degrees
        a_ = math.radians(ang)
        c_, s_ = math.cos(a_), math.sin(a_)
        hl, hw = 0.20, 0.022
        pts = [(-hl, -hw), (hl, -hw), (hl, hw), (-hl, hw)]
        V = [(xt + x * c_ - y * s_, tv + x * s_ + y * c_, z) for z in (0.0, 0.030) for (x, y) in pts]
        bg.add(V, [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)], 0)
    d.gm_object("table_base", bg, [cast], "support", "script:table_base")
    top_z = top_surface
    # ---- the chairs at their own size, facing the table
    d.piece("painted_wooden_chair_01", 1.215, 0.32, 0.0, rot=(0, 0, math.pi / 2), tier="bed", tris=None)
    d.tone(d.last_objs, 0.78)                   # the white paint burnt on the seats under the gate's night spill (PIC-05g)
    d.piece("painted_wooden_chair_01", 2.135, 0.32, 0.0, rot=(0, 0, -math.pi / 2), tier="bed", tris=None)
    d.tone(d.last_objs, 0.78)
    pot = d.sub_template("tea_set_01", "pot", lambda n: "teapot" in n)
    cupa = d.compose("tea_set_01", "cupA", [(("cup_small_01",), (0.0, 0.2335, 0.013)), (("saucer_circular_04",), (0.0, 0.0, 0.0))])
    cupb = d.compose("tea_set_01", "cupB", [(("cup_small_02",), (0.0, 0.2335, 0.013)), (("saucer_circular_03",), (0.0, 0.0, 0.0))])
    d.piece(pot, tu + 0.10, tv + 0.10, top_z, rot=(0, 0, 0.3), tier="table", tris=None)       # try 2: the pot at the back right and the second cup in front of it (DSP-03: cupB was seen 0.45 behind the pot)
    d.piece(cupa, tu + 0.12, tv - 0.12, top_z, rot=(0, 0, 0.5), tier="table", tris=None)
    d.piece(cupb, tu - 0.05, tv - 0.02, top_z, rot=(0, 0, -0.4), tier="table", tris=None)
    sg = GM()
    sg.lathe(X(tu - 0.16), tv + 0.14, top_z, [(0.0, 0.0), (0.025, 0.0), (0.040, 0.012), (0.042, 0.040), (0.030, 0.046), (0.0, 0.046)], mi=0, n=18)
    sg.lathe(X(tu - 0.16), tv + 0.14, top_z + 0.046, [(0.0, 0.0), (0.032, 0.0), (0.030, 0.012), (0.004, 0.018), (0.0, 0.026)], mi=0, n=18)
    d.gm_object("sugar_bowl", sg, [china], "scripted", "script:sugar_bowl_menu", tier="table", smooth=True)
    # the menu stand: a tent card, TEAS FROM 25p, two sheets leaning toward each other, the foot on the top
    mp = os.path.join(tex, "menu_stand.png")
    muv = GEN.card_atlas(mp, ["TEAS\nFROM 25p"], cols=1, tile=(256, 160), size=40, bg=(206, 200, 180))
    GEN.TEXTS.extend(["TEAS FROM 25p"])
    mm = d.image_mat("menu_stand", mp, rough=0.8)
    mg = GM()
    hc = 0.050 / 2 * math.cos(math.radians(12.0)) + 0.0005
    yc_ = tv - 0.19
    mg.sheet((X(tu - 0.10), yc_, top_z + hc), 0.070, 0.050, 0.002, tilt=12.0, mi=0, uv=muv[0], uv_other=(muv[0][0] + 0.01, muv[0][1] + 0.01))
    mg.sheet((X(tu - 0.10), yc_ + 2 * 0.025 * math.sin(math.radians(12.0)), top_z + hc), 0.070, 0.050, 0.002, tilt=-12.0, mi=0, uv=muv[0], uv_other=(muv[0][0] + 0.01, muv[0][1] + 0.01))
    d.gm_object("menu_stand", mg, [mm], "scripted", "script:sugar_bowl_menu", tier="table")
    # ---- the carrot cake on a two-tier china stand; the strawberry cake on a plate; the plant
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
    # ---- the cafe curtains: a brass rod at w 0.90 and two cotton panels hung 0.55, over the two outer lights (u 0.04 to 1.10 and 2.26 to 3.31)
    rod_w, rod_v = 0.90, 0.075
    weave = GEN.weave_png(os.path.join(tex, "cotton_weave.png"), (199, 192, 172))
    cur_m = d.image_mat("cafe_curtain", weave, rough=0.85)
    pb = [n_ for n_ in cur_m.node_tree.nodes if n_.type == "BSDF_PRINCIPLED"][0]
    for nm_, val in (("Transmission Weight", 0.3), ("Sheen Weight", 0.4)):
        if nm_ in pb.inputs:
            pb.inputs[nm_].default_value = val
    for si, (side, (ua, ub)) in enumerate((("l", (0.05, 1.10)), ("r", (2.26, 3.30)))):
        g = GM()
        g.rod((X(ua - 0.012), rod_v, rod_w), (X(ub + 0.012), rod_v, rod_w), 0.009, 0, 12)
        for xx, sgn in ((ua - 0.012, -1), (ub + 0.012, 1)):         # the end brackets: a 16 mm socket round the rod's end, a 70 mm arm along v to the plate on the back of the jamb or the mullion
            g.rod((X(xx) + sgn * 0.004, rod_v, rod_w), (X(xx) + sgn * 0.016, rod_v, rod_w), 0.0105, 0, 12)
            g.rod((X(xx) + sgn * 0.016, rod_v, rod_w), (X(xx) + sgn * 0.016, 0.006, rod_w), 0.004, 0, 8)
            g.box(X(xx) + sgn * 0.016 - 0.010, X(xx) + sgn * 0.016 + 0.010, 0.0, 0.006, rod_w - 0.03, rod_w + 0.03, 0)
        d.gm_object("curtain_rod_" + side, g, [brass], "support", "script:cafe_curtain")
        cg = GM()
        GEN.cafe_curtain(cg, X(ua), X(ub), rod_v, rod_w, 0.55 - 0.016, 31 + si)
        ob_, _ = d.gm_object("curtain_" + side, cg, [cur_m], "scripted", "script:cafe_curtain", tier="curtain", smooth=True)
    # ---- the hand-lettered card on the glass's inside (BREAKFASTS, LUNCHES, TEAS), on two clear suction cups with a steel hook each
    cp = os.path.join(tex, "window_card.png")
    cuv = GEN.card_atlas(cp, ["BREAKFASTS\nLUNCHES\nTEAS"], cols=1, tile=(512, 320), size=58, bg=(206, 200, 180))
    GEN.TEXTS.extend(["BREAKFASTS", "LUNCHES", "TEAS"])
    cm = d.image_mat("window_card", cp, rough=0.85)
    wg = GM()
    wg.csheet((X(2.80), 0.0185, 1.09), 0.60, 0.38, 0.003, tilt=0.0, bow=0.0015, nx=12, nz=4, mi=0, uv=cuv[0], uv_other=(cuv[0][0] + 0.01, cuv[0][1] + 0.01))
    d.gm_object("window_card_menu", wg, [cm], "scripted", "script:window_card_menu", tier="glass")
    pvc = d.mat("suction_pvc", rgb8(230, 230, 230), rough=0.2, glass=True)
    hook_m = d.mat("hook_steel", rgb8(150, 152, 154), rough=0.35, metal=1.0)
    sc_, hk = GM(), GM()
    for xx in (2.55, 3.05):
        # a clear disc 30 mm across and 3 mm thick flat on the glass (its axis along v), 12 mm under the card's top edge; the hook runs from its middle to the card
        zc = 1.28 - 0.012
        sc_.rod((X(xx), 0.0, zc), (X(xx), 0.003, zc), 0.015, 0, 20)           # a clear disc 30 mm across and 3 mm thick, its axis along v, flat on the glass
        hk.rod((X(xx), 0.003, zc), (X(xx), 0.0170, zc), 0.0015, 0, 6)
    d.gm_object("window_card_cups", sc_, [pvc], "support", "script:window_card_menu")
    d.gm_object("window_card_hooks", hk, [hook_m], "support", "script:window_card_menu")
    # ---- the price cards, each before its goods and none within 0.10 m of a chair or the table
    texts = ["CAKES 40p", "TEAS 25p", "GATEAU 45p", "HOME MADE"]
    path = os.path.join(tex, "price_cards.png")
    uvs = GEN.card_atlas(path, texts, cols=2, tile=(256, 128), size=46, bg=(206, 200, 180))
    pm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    for k, uc in enumerate((0.50, 0.80, 2.62, 0.30)):
        d.price_card(uc, 0.02, 0.0, k, uvs, pm)
    d.display_texts = list(GEN.TEXTS) + [t for t in texts]
