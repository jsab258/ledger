"""The launderette (east_parade bay 4, "steam_laundry"): the room's layout and the window display (14 October 2026, batch B). Read from `shops.steam_laundry.room` and `.display` in target.json; every choice
the target left open is stated in the docstrings (each a Judgement in NOTES.md and a `Changes after the build` line).

The shop is dark at night (the target: `night_dark` is its real night): the room's night_dark picture is the sodium wash and the dryers' two orange running lamps.
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

# material slots shared by the machines' two meshes (boxes, flat shaded; curved parts, smooth)
(M_ENAMEL, M_PANEL, M_PLASTIC, M_DARK, M_STEEL, M_RUBBER, M_SMOKED, M_LAMP, M_LAMP_ON, M_PLINTH) = range(10)


def _setup():
    global rgb8
    import sw_room as S
    rgb8 = S.rgb8


def _dome_y(gm, cx, y0, cz, r, bulge, mi, n=32, nr=5):
    """A closed shallow dome facing -y (a machine's glass door): its base disc (radius r) at y0, the crown `bulge` in front of it (smaller y). A spherical-cap profile."""
    V, F = [], []
    rings = []
    for j in range(nr):
        rad = r * (1.0 - j / float(nr))
        y = y0 - bulge * (1.0 - (rad / r) ** 2)
        idx = []
        for i in range(n):
            a = 2 * math.pi * i / n
            V.append((cx + rad * math.cos(a), y, cz + rad * math.sin(a)))
            idx.append(len(V) - 1)
        rings.append(idx)
    V.append((cx, y0 - bulge, cz))
    apex = len(V) - 1
    for j in range(nr - 1):
        for i in range(n):
            i2 = (i + 1) % n
            F.append((rings[j][i], rings[j][i2], rings[j + 1][i2], rings[j + 1][i]))
    for i in range(n):
        F.append((rings[nr - 1][i], rings[nr - 1][(i + 1) % n], apex))
    F.append(tuple(rings[0]))
    gm.add(V, F, mi)


# ---------------------------------------------------------------------------------------------------------------------------------- pictures by script
def _care_chart(path):
    """The wash-care chart on the right wall (0.6 x 0.8 m): a header band and six rows, each a plain symbol (a tub with a number, a crossed triangle, an iron, a circle, a square with a circle, a tub with a hand) and
    its words. The symbols are the plain international care signs drawn by hand here; no maker's name."""
    from sw_gen import font
    W, H = 480, 640
    im = Image.new("RGB", (W, H), (236, 234, 222))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, 70], fill=(34, 76, 128))
    f = font("alfa-slab-one", 40)
    d.text((W / 2 - d.textlength("WASH CARE", font=f) / 2, 14), "WASH CARE", font=f, fill=(240, 236, 220))
    ink = (40, 44, 56)
    rows = [("wash40", "WASH 40"), ("nobleach", "NO BLEACH"), ("iron", "IRON COOL"), ("dry", "DRY CLEAN"), ("tumble", "TUMBLE DRY"), ("hand", "HAND WASH")]
    fl = font("oswald", 34)
    for k, (sym, label) in enumerate(rows):
        y0 = 86 + k * 90
        cx, cy = 80, y0 + 38
        if sym in ("wash40", "hand"):
            d.polygon([(cx - 40, cy - 22), (cx + 40, cy - 22), (cx + 30, cy + 26), (cx - 30, cy + 26)], outline=ink, width=4)
            for i in range(3):
                d.arc([cx - 30 + i * 20, cy - 16, cx - 10 + i * 20, cy - 4], 200, 340, fill=ink, width=3)
            if sym == "wash40":
                d.text((cx - 12, cy - 2), "40", font=font("oswald", 24), fill=ink)
            else:
                d.line([(cx - 8, cy + 20), (cx - 8, cy - 2), (cx + 12, cy - 2), (cx + 12, cy + 20)], fill=ink, width=4)
        elif sym == "nobleach":
            d.polygon([(cx, cy - 34), (cx + 38, cy + 28), (cx - 38, cy + 28)], outline=ink, width=4)
            d.line([(cx - 38, cy - 30), (cx + 38, cy + 30)], fill=ink, width=4)
            d.line([(cx + 38, cy - 30), (cx - 38, cy + 30)], fill=ink, width=4)
        elif sym == "iron":
            d.polygon([(cx - 40, cy + 24), (cx + 40, cy + 24), (cx + 40, cy - 4), (cx + 10, cy - 26), (cx - 40, cy - 26)], outline=ink, width=4)
            d.ellipse([cx - 4, cy - 2, cx + 4, cy + 6], fill=ink)
        elif sym == "dry":
            d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], outline=ink, width=4)
            d.text((cx - 9, cy - 20), "P", font=font("oswald", 34), fill=ink)
        elif sym == "tumble":
            d.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], outline=ink, width=4)
            d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=ink, width=4)
        d.text((150, y0 + 22), label, font=fl, fill=ink)
        d.line([(24, y0 + 80), (W - 24, y0 + 80)], fill=(180, 176, 160), width=2)
        GEN.TEXTS.append(label)
    GEN.TEXTS.append("WASH CARE")
    im.save(path)


def _worn_path(path, size=(1024, 768), seed=5):
    """A darker worn path on the grey vinyl, as a soft RGBA decal: lighter alpha at the edges, streaks along the walking direction (y), a few scuffs."""
    rnd = np.random.default_rng(seed)
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    u = (xx / w - 0.5) * 2.0
    v = (yy / h - 0.5) * 2.0
    core = np.clip(1.0 - (u ** 2 / 0.95 + v ** 2 / 0.95), 0.0, 1.0)
    core = core ** 0.8
    streak = rnd.normal(0, 1, (h, w)).astype(np.float32)
    streak = np.asarray(Image.fromarray(((streak - streak.min()) / (streak.max() - streak.min()) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(9)), np.float32) / 255.0
    a = np.clip(core * (0.55 + 0.9 * (streak - 0.5)), 0.0, 1.0) * 0.55
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 40, 42, 44
    rgba[..., 3] = (a * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(path)


# ---------------------------------------------------------------------------------------------------------------------------------- the room
def _cork_png(path, w=1024, h=683, seed=11):
    """A cork board's picture by script: two tones ((176, 132, 88) and (150, 108, 70)) in soft patches, a 2 mm grain (1024 px over 0.9 m is 0.9 mm a pixel), pale and dark flecks, a few pin holes."""
    import numpy as np
    from PIL import Image, ImageFilter
    rng = np.random.default_rng(seed)
    a = np.array((176, 132, 88), float)
    b = np.array((150, 108, 70), float)
    lo = Image.fromarray((rng.random((h // 8, w // 8)) * 255).astype("uint8")).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    m = np.asarray(lo, float) / 255.0
    m = np.clip((m - 0.35) * 3.0, 0.0, 1.0)[..., None]
    img = a * (1 - m) + b * m
    gr = rng.normal(0.0, 1.0, (h, w))
    gr = np.asarray(Image.fromarray(np.clip(gr * 40 + 128, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.0)), float) - 128.0
    img = img + gr[..., None] * 0.9
    fl = rng.random((h, w))
    dark = (fl < 0.012)[..., None]
    pale = (fl > 0.992)[..., None]
    img = np.where(dark, img * 0.62, img)
    img = np.where(pale, np.minimum(img * 1.25 + 14, 255), img)
    im = Image.fromarray(np.clip(img, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(im)
    for _ in range(26):
        x, y = int(rng.integers(8, w - 8)), int(rng.integers(8, h - 8))
        d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(96, 66, 40))
    im.save(path)


def _machine(gb, gc, cx, w, y_f, y_b, z0, kind, plinth, lamp_on=False):
    """One front-loading washer or tumble dryer: a cabinet, a control strip (a drawer and a dial and a blank coin plate for the washer; two dials, a coin plate and a lamp for the dryer), a round door (a rubber seal,
    a chrome ring, a smoked glass dome). `y_f` is the cabinet's front face; nothing stands more than 0.033 in front of it. Returns the lamp's centre (x, y, z) for a dryer."""
    hw = w / 2.0
    if plinth:
        gb.box(cx - hw + 0.015, cx + hw - 0.015, y_f + 0.025, y_b, z0, z0 + 0.07, M_PLINTH)
        z_b = z0 + 0.06
    else:
        z_b = z0
    gb.box(cx - hw, cx + hw, y_f, y_b, z_b, z0 + 0.85, M_ENAMEL)
    gb.box(cx - hw + 0.025, cx + hw - 0.025, y_f - 0.004, y_f + 0.01, z0 + 0.70, z0 + 0.82, M_PANEL)
    zc = z0 + (0.39 if kind == "washer" else 0.38)
    big = 0.185 if kind == "washer" else 0.18
    gc.rod((cx, y_f - 0.006, zc), (cx, y_f + 0.004, zc), big + 0.02, M_RUBBER, 36)
    gc.torus((cx, y_f - 0.012, zc), big, 0.02, M_STEEL, axis="y", nm=40, nn=8)
    _dome_y(gc, cx, y_f - 0.008, zc, big - 0.019, 0.016, M_SMOKED, n=36, nr=5)
    zd = z0 + 0.76
    lamp_at = None
    if kind == "washer":
        gb.box(cx - hw + 0.045, cx - 0.10, y_f - 0.008, y_f, zd - 0.035, zd + 0.035, M_PLASTIC)                      # the powder drawer
        gb.box(cx - hw + 0.065, cx - 0.12, y_f - 0.0095, y_f - 0.006, zd - 0.006, zd + 0.006, M_DARK)                # its finger slot
        gc.rod((cx + 0.10, y_f - 0.004, zd), (cx + 0.10, y_f - 0.024, zd), 0.027, M_STEEL, 20)                        # the programme dial
        gb.box(cx + 0.0955, cx + 0.1045, y_f - 0.0255, y_f - 0.0235, zd + 0.004, zd + 0.026, M_DARK)
        gb.box(cx + 0.185, cx + 0.245, y_f - 0.007, y_f - 0.004, zd - 0.035, zd + 0.035, M_STEEL)                    # a blank coin plate
        gb.box(cx + 0.208, cx + 0.222, y_f - 0.0085, y_f - 0.0065, zd - 0.014, zd + 0.016, M_DARK)
    else:
        gc.rod((cx - hw + 0.095, y_f - 0.004, zd), (cx - hw + 0.095, y_f - 0.024, zd), 0.027, M_STEEL, 20)           # the timer dial
        gb.box(cx - hw + 0.0905, cx - hw + 0.0995, y_f - 0.0255, y_f - 0.0235, zd + 0.004, zd + 0.026, M_DARK)
        gc.rod((cx - 0.02, y_f - 0.004, zd), (cx - 0.02, y_f - 0.019, zd), 0.018, M_STEEL, 16)                         # the heat switch
        gb.box(cx - 0.0245, cx - 0.0155, y_f - 0.0205, y_f - 0.0185, zd + 0.003, zd + 0.016, M_DARK)
        gb.box(cx + 0.10, cx + 0.16, y_f - 0.007, y_f - 0.004, zd - 0.035, zd + 0.035, M_STEEL)                      # a blank coin plate
        gb.box(cx + 0.123, cx + 0.137, y_f - 0.0085, y_f - 0.0065, zd - 0.014, zd + 0.016, M_DARK)
        lx = cx + hw - 0.065
        gc.rod((lx, y_f - 0.004, zd), (lx, y_f - 0.012, zd), 0.011, M_LAMP_ON if lamp_on else M_LAMP, 14)           # the "running" lamp
        lamp_at = (lx, y_f - 0.012, zd)
    return lamp_at


def room(r):
    """The launderette's room (target `shops.steam_laundry.room`: fixtures L-*). What the target leaves open, and what this does:

    washers L-back-washers: four, each 0.60 x 0.585 x 0.85 (the cabinet's front face stands 0.565 off the wall so that the door's ring, 0.032 proud, reaches the 0.60 limit and no more): white enamel (196, 198, 194:
    pure white burns under the battens), a blue control strip with a powder drawer, a programme dial and a blank coin plate, a round door 0.37 across (a rubber seal, a chrome ring, a smoked glass dome); a dark plinth.
    dryers L-back-dryers: three stacks of two, each 0.69 wide x 0.85 high with a 0.03 stacking gap between (1.73 in all), the same depth, a door 0.40 across, a timer dial, a heat switch, a coin plate and a lamp. Two lamps
    (the lower dryer of the first stack and the upper of the third) are the "running" ones: orange and emissive in night_dark only (a warm point light 2000 K, radius 0.01 m, beside each), dull orange discs otherwise.
    shelves L-back-shelves: the target's two tiers (z 1.30 and 1.70, 0.30 deep) over the washers, standing ON the washers' tops (the uprights start at z 0.85) and ending inside their footprint; 18 wrapped parcels in all,
    nine a tier (seven in a row and two on top), brown and tan paper and one blue-grey, a cross of string, a numbered tag (invented numbers), sizes 0.27 to 0.31 x 0.18 to 0.22 x 0.10 to 0.14.
    notices L-left-notices: a cork board 0.9 x 0.6 (28 mm) with three cards: PRICES, RULES, SERVICE WASHES (the project's own words). L-right-notices: a wash-care chart 0.6 x 0.8 (a script picture) and the wall clock.
    floor: the grey vinyl tile (rubber_tiles tinted to (92, 94, 96)), a black rubber mat 1.0 x 0.6 at the door and a soft darker worn path (a decal 1.5 mm up)."""
    _setup()
    import sw_room_gen as RG
    import bpy
    D, W = RG.D, RG.W
    rr = r.RR
    fx = r.fxd
    rnd = r.rnd
    tex = r.tex
    GEN.TEXTS.clear()
    mats = [
        r.mat("machine_enamel", rgb8(196, 198, 194), rough=0.3),
        r.mat("machine_panel", rgb8(84, 110, 140), rough=0.45),
        r.mat("machine_plastic", rgb8(172, 176, 176), rough=0.4),
        r.mat("machine_dark", rgb8(26, 28, 30), rough=0.5),
        r.mat("machine_steel", rgb8(196, 198, 200), rough=0.22, metal=1.0),
        r.mat("machine_rubber", rgb8(34, 36, 38), rough=0.7),
        r.mat("machine_smoked", rgb8(72, 80, 90), rough=0.06),         # smoked glass over the drum: lifted from (22, 28, 34), whose mirror took the floor and went under luma 12 in the window (LIT-02b)
        r.mat("lamp_off", rgb8(122, 62, 28), rough=0.4),
        r.mat("lamp_on", rgb8(255, 130, 40), rough=0.4, emit=(1.0, 0.36, 0.06), emit_strength=0.0),
        r.mat("machine_plinth", rgb8(70, 72, 74), rough=0.6),
    ]
    y_b = D - 0.005
    y_f = D - 0.565
    # ---- the four washers
    xw0, xw1 = fx["L-back-washers"]["x"]
    wpitch = (xw1 - xw0) / 4.0
    gb, gc = GM(), GM()
    for k in range(4):
        _machine(gb, gc, xw0 + wpitch * (k + 0.5), wpitch - 0.01, y_f, y_b, 0.0, "washer", True)
    ob1 = gb.to_object("washers_body", mats, r.sc)
    GB.chamfer(ob1, 0.004, 2)
    ob2 = gc.to_object("washers_doors", mats, r.sc, smooth=True)
    ext = [min(gb.extents()[0], gc.extents()[0]), max(gb.extents()[1], gc.extents()[1]), min(gb.extents()[2], gc.extents()[2]), max(gb.extents()[3], gc.extents()[3]), 0.0, max(gb.extents()[5], gc.extents()[5])]
    r.placed_rec("L-back-washers", "script:washing_machine", ext, [ob1.name, ob2.name], tag="washers", n=4)
    # ---- the six dryers
    xd0, xd1 = fx["L-back-dryers"]["x"]
    dpitch = (xd1 - xd0) / 3.0
    gb, gc = GM(), GM()
    lamps = []
    for k in range(3):
        cx = xd0 + dpitch * (k + 0.5)
        for lvl in range(2):
            on = (k == 0 and lvl == 0) or (k == 2 and lvl == 1)
            la = _machine(gb, gc, cx, dpitch - 0.01, y_f, y_b, 0.0 if lvl == 0 else 0.88, "dryer", lvl == 0, lamp_on=on)
            if on:
                lamps.append(la)
        gb.box(cx - dpitch / 2 + 0.02, cx + dpitch / 2 - 0.02, y_f + 0.03, y_b - 0.01, 0.848, 0.882, M_PLINTH)         # the stacking frame between the two
    ob1 = gb.to_object("dryers_body", mats, r.sc)
    GB.chamfer(ob1, 0.004, 2)
    ob2 = gc.to_object("dryers_doors", mats, r.sc, smooth=True)
    ext = [min(gb.extents()[0], gc.extents()[0]), max(gb.extents()[1], gc.extents()[1]), min(gb.extents()[2], gc.extents()[2]), max(gb.extents()[3], gc.extents()[3]), 0.0, max(gb.extents()[5], gc.extents()[5])]
    r.placed_rec("L-back-dryers", "script:tumble_dryer", ext, [ob1.name, ob2.name], tag="dryers", n=6)
    # the two running lamps: warm point lights for night_dark only
    r.run_lamps = []
    for k, (lx, ly, lz) in enumerate(lamps):
        ld = bpy.data.lights.new("running_lamp_%d" % k, "POINT")
        ld.energy = 0.0
        ld.color = (1.0, 0.52, 0.16)
        ld.shadow_soft_size = 0.01
        lo = bpy.data.objects.new("running_lamp_%d" % k, ld)
        r.sc.collection.objects.link(lo)
        lo.location = (lx, ly - 0.05, lz)
        r.run_lamps.append(lo)
    r.run_lamp_w = 0.9
    r.rows["running_lamps"] = {"n": len(lamps), "at": [[round(a, 3), round(b, 3), round(c, 3)] for a, b, c in lamps], "lit_in": "night_dark only"}
    orig_set_state = r.set_state

    def set_state(state, P, _o=orig_set_state):
        _o(state, P)
        on = state == "night_dark"
        mats[M_LAMP_ON].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 7.0 if on else 0.0
        for lo_ in r.run_lamps:
            lo_.data.energy = P.get("run_lamp", r.run_lamp_w) if on else 0.0
    r.set_state = set_state
    # ---- the shelves over the washers: standing on their tops
    a_, b_ = -2.50, -0.20
    r.shelf_unit("L-back-shelves", [(1.30, a_, b_), (1.70, a_, b_)], bottom=0.85)
    sd = fx["L-back-shelves"]["depth_m"]
    # parcels: kraft brown, tan, blue-grey, string, a numbered tag
    paper = [r.mat("parcel_kraft", rgb8(150, 110, 72), rough=0.85), r.mat("parcel_tan", rgb8(178, 146, 104), rough=0.85), r.mat("parcel_blue", rgb8(112, 122, 134), rough=0.85)]
    string_m = r.mat("parcel_string", rgb8(206, 188, 146), rough=0.9)
    tags = ["No.%d" % n for n in (14, 27, 31, 42, 58, 63, 75, 81, 96)]
    tp = os.path.join(tex, "parcel_tags.png")
    tuv = GEN.card_atlas(tp, tags, cols=3, tile=(192, 128), size=46, bg=(226, 214, 184))
    GEN.TEXTS.extend(tags)
    tag_m = r.image_mat("parcel_tags", tp, rough=0.8)
    n_tag = 0
    for z, nrow in ((1.30, 7), (1.70, 7)):
        gm = GM()
        xs = a_ + 0.03
        for i in range(nrow):
            wd, dp, ht = rnd.uniform(0.27, 0.31), rnd.uniform(0.18, 0.22), rnd.uniform(0.10, 0.14)
            xc = xs + 0.155 + i * 0.318 + rnd.uniform(-0.004, 0.004)
            yb = D - 0.04
            stack = 2 if i in (1, 4) else 1
            zz = z
            for lay in range(stack):
                if lay:
                    wd, dp = wd * 0.9, dp * 0.92
                    ht = rnd.uniform(0.10, 0.12)
                mi = rnd.choice((0, 0, 1, 2)) if lay == 0 else rnd.choice((1, 2, 0))
                gm.box(xc - wd / 2, xc + wd / 2, yb - dp, yb, zz, zz + ht, mi)
                # a cross of string: one band round the width, one round the depth (the bands stand 1.5 mm proud)
                gm.box(xc - 0.004, xc + 0.004, yb - dp - 0.0015, yb + 0.0, zz - 0.0005, zz + ht + 0.0015, 3)
                gm.box(xc - wd / 2 - 0.0015, xc + wd / 2 + 0.0015, yb - dp * 0.5 - 0.004, yb - dp * 0.5 + 0.004, zz - 0.0005, zz + ht + 0.0015, 3)
                tg = tuv[n_tag % 9]
                n_tag += 1
                gm.box(xc + wd * 0.12, xc + wd * 0.12 + 0.045, yb - dp - 0.0035, yb - dp - 0.0015, zz + ht * 0.25, zz + ht * 0.25 + 0.03, 4, uv_front=tg)
                zz += ht
        o = gm.to_object("parcels_%.2f" % z, paper + [string_m, tag_m], r.sc)
        r.placed_rec("L-back-shelves", "script:wrapped_parcels", gm.extents(), [o.name], tag="parcels_%.2f" % z, n=9)
    # ---- the left wall: the cork board and three cards
    xl, xr = -W / 2, W / 2
    # 14 Oct (the tea rooms' close review, narrow 7: "the cork notice board is a flat orange slab"): a granular cork picture made by script (two tones, a 2 mm grain), a 20 x 15 mm pine frame, a coloured pin in each card
    cork_p = os.path.join(tex, "cork.png")
    _cork_png(cork_p)
    cork = r.image_mat("cork", cork_p, rough=0.95)
    pine = r.mat("cork_frame_pine", rgb8(200, 160, 110), rough=0.6)
    cg_ = GM()
    cg_.box(xl + 0.002, xl + 0.030, 1.60, 2.50, 1.25, 1.85, 0, uv_front=(0.0, 0.0, 1.0, 1.0), front="+x", uv_other=(0.01, 0.01))
    fx_ = xl + 0.002
    cg_.box(fx_, xl + 0.045, 1.58, 1.60, 1.23, 1.87, 1)
    cg_.box(fx_, xl + 0.045, 2.50, 2.52, 1.23, 1.87, 1)
    cg_.box(fx_, xl + 0.045, 1.60, 2.50, 1.23, 1.25, 1)
    cg_.box(fx_, xl + 0.045, 1.60, 2.50, 1.85, 1.87, 1)
    cob = cg_.to_object("cork_board", [cork, pine], r.sc)
    r.fixture_rec("L-left-notices", "cork_board", cg_.extents())
    npth = os.path.join(tex, "notices.png")
    ntxt = ["PRICES\nWASH  90p\nDRY  20p\nSOAP  15p\nSERVICE\n35p a lb", "PLEASE\nREMOVE YOUR\nWASH AT ONCE\nAND TAKE CARE\nOF THE DOORS", "SERVICE\nWASHES\nLEAVE IT WITH US\nREADY NEXT DAY"]
    nuv = GEN.card_atlas(npth, ntxt, cols=3, tile=(256, 340), size=34, bg=(232, 226, 204), ink=(30, 40, 80))
    GEN.TEXTS.extend(["PRICES", "WASH 90p", "DRY 20p", "SOAP 15p", "SERVICE", "35p a lb", "PLEASE", "REMOVE YOUR", "WASH AT ONCE", "AND TAKE CARE", "OF THE DOORS", "SERVICE", "WASHES", "LEAVE IT WITH US", "READY NEXT DAY"])
    nm_ = r.image_mat("notices", npth, rough=0.8)
    ng = GM()
    pg = GM()
    for k, (yc, zlo) in enumerate(((1.80, 1.33), (2.05, 1.35), (2.30, 1.32))):
        ng.box(xl + 0.0300, xl + 0.0322, yc - 0.105, yc + 0.105, zlo, zlo + 0.38, 0, uv_front=nuv[k], front="+x", uv_other=(nuv[k][0] + 0.01, nuv[k][1] + 0.01))
        pg.rod((xl + 0.0322, yc, zlo + 0.345), (xl + 0.0362, yc, zlo + 0.345), 0.0032, k, 12)
    no = ng.to_object("notices", [nm_], r.sc)
    pins_m = [r.mat("pin_%s" % n_, rgb8(*c_), rough=0.35) for n_, c_ in (("red", (196, 48, 40)), ("blue", (48, 78, 168)), ("yellow", (226, 188, 48)))]
    pgo = pg.to_object("notice_pins", pins_m, r.sc, smooth=True)
    r.fixture_rec("L-left-notices", "notice_pins", pg.extents())
    r.placed_rec("L-left-notices", "script:paper_notices", ng.extents(), [no.name], tag="notices", n=3)
    # ---- the right wall: the care chart and the clock
    cp = os.path.join(tex, "care_chart.png")
    _care_chart(cp)
    cm = r.image_mat("care_chart", cp, rough=0.7)
    cg = GM()
    cg.box(xr - 0.0105, xr - 0.0085, 1.20, 1.80, 1.12, 1.92, 0, uv_front=(0.0, 0.0, 1.0, 1.0), front="-x")
    co = cg.to_object("care_chart", [cm], r.sc)
    r.fixtures.append({"fixture": "L-right-notices", "name": "care_chart", "ext": [xr - 0.0105, xr - 0.0085, 1.20, 1.80, 1.12, 1.92]})
    ck_s = next(g["size_m"] for g in rr["goods"] if g["model"] == "wall_clock") / max(r.dims("wall_clock"))
    r.place("wall_clock", (xr - 0.022, 2.02, 1.78), rot=(0, 0, -math.pi / 2), scale=ck_s, fixture="L-right-notices", anchor=("max", "c", "c"), clock=r.next_clock(), tag="clock")
    # ---- the floor: the black rubber mat at the door and the worn path
    rubber = r.mat("door_mat", rgb8(26, 26, 28), rough=0.85)
    r.box("floor_mat", -0.5, 0.5, 0.2, 0.8, 0.0, 0.012, rubber, fixture="L-floor-mat")
    wp = os.path.join(tex, "worn_path.png")
    _worn_path(wp)
    wm = r.image_mat("worn_path", wp, rough=0.8, alpha=True)
    me = bpy.data.meshes.new("worn_path")
    x0_, x1_, y0_, y1_, zf = -1.7, 1.7, 0.9, 3.9, 0.0015
    me.from_pydata([(x0_, y0_, zf), (x1_, y0_, zf), (x1_, y1_, zf), (x0_, y1_, zf)], [], [(0, 1, 2, 3)])
    uvl = me.uv_layers.new(name="UVMap")
    for loop, (a, b) in zip(me.loops, ((0, 0), (1, 0), (1, 1), (0, 1))):
        uvl.data[loop.index].uv = (a, b)
    wo = bpy.data.objects.new("worn_path", me)
    r.sc.collection.objects.link(wo)
    wo.data.materials.append(wm)
    r.fixtures.append({"fixture": "L-floor-mat", "name": "worn_path", "ext": [x0_, x1_, y0_, y1_, 0.0, zf]})
    r.notes.append("four washers and six dryers (two stacks' lamps are the running ones, emissive in night_dark only); the shelf uprights stand on the washers' tops; 18 parcels, nine a tier; a care chart by script; the clock's glass kept as a see-through pane")
    r.texts = list(GEN.TEXTS)
    return r


# ---------------------------------------------------------------------------------------------------------------------------------- the window
def display(d):
    """The launderette's window (target `shops.steam_laundry.display`, 6 item rows; bed 3.35 x 0.55; "SERVICE WASHES" is lettered on the glass, 4.1): a 20 mm laminate bed cover (script:laundry_shelf_board), and on it
    left to right five stacks of folded towels (0.30 x 0.45 footprint, 6 to 9 towels of 0.05, each stack leaning 1 to 3 degrees, mixed colours, the folded edge and a coloured border to the street), two wicker baskets
    (wicker_basket_01 at its own size, a heap of laundry in each), the hand-lettered SERVICE WASHES card on two posts behind the baskets (in the right-hand light: the mullion stood across it in the middle), and ten detergent items on the right (four large boxes on a low step at the back, in
    front three packets, two washing-up bottles and a bleach bottle; every maker invented: HOLME, BRIGHTWELL, FERNSIDE, LINDEN, ASHDOWN, MEADOWS). Whites are toned (0.85): pure white packaging burns under the gate's night
    spill (PIC-05g). The shop is dark at night, so nothing here is lit by the shop."""
    _setup()
    import sw_room_gen as RG
    rr = d.RR
    walls = rr["walls"]
    d.start((118, 120, 124), RG._rgb(walls["above"]), (210, 208, 198))         # the bed: a mid grey (the cover is laminate); the dado is the white tile, toned (the target gives no colour for it)
    rnd = d.rnd
    L = d.L
    X = lambda u: u - L / 2
    tex = d.tex
    GEN.TEXTS.clear()
    # ---- the laminate bed cover (20 mm): everything stands on it
    lam = d.mat("laminate_cover", rgb8(150, 152, 156), rough=0.35)
    gm = GM()
    gm.box(X(0.0), X(L), 0.0, 0.55, 0.0, 0.02, 0)
    ob, _ = d.gm_object("laundry_shelf_board", gm, [lam], "support", "script:laundry_shelf_board")
    GB.chamfer(ob, 0.003, 2)
    z0 = 0.02
    # ---- five stacks of folded towels
    base = [(176, 104, 96), (96, 128, 150), (206, 180, 124), (108, 140, 112), (184, 142, 152), (160, 122, 92)]
    cols = []
    for c in base:
        cols.append(c)
        cols.append(tuple(min(255, int(v * 1.14)) for v in c))
    tp = os.path.join(tex, "towel_tiles.png")
    tuv = GB.towel_atlas(tp, cols)
    tm = d.image_mat("towel_tiles", tp, rough=0.95)
    stacks = [(0.17, 8, 0), (0.47, 6, 1), (0.77, 9, 2), (1.07, 7, 3), (1.37, 6, 4)]
    gm = GM()
    for si, (uc, n, bi) in enumerate(stacks):
        lean = rnd.uniform(1.0, 3.0) * rnd.choice((-1, 1))
        yaw = rnd.uniform(-2.5, 2.5)
        for k in range(n):
            uv = tuv[bi * 2 + (k % 2)]
            off = math.tan(math.radians(lean)) * (z0 + 0.05 * k)
            xj = rnd.uniform(-0.004, 0.004)
            GB.towel_box(gm, (X(uc) + off + xj, 0.31 + rnd.uniform(-0.004, 0.004), z0 + 0.05 * k + 0.0245), 0.30, 0.049, 0.45, yaw + rnd.uniform(-1.2, 1.2), 0, uv)
    ob, _ = d.gm_object("folded_towels", gm, [tm], "scripted", "script:folded_towels", tier="board")
    GB.chamfer(ob, 0.012, 3, angle=20.0)
    # ---- two wicker baskets with laundry heaped in each (three lumps of cloth in two or three colours: sheets and a towel)
    cloth = [[d.mat("laundry_a1", rgb8(176, 196, 210), rough=0.95), d.mat("laundry_a2", rgb8(226, 214, 190), rough=0.95), d.mat("laundry_a3", rgb8(176, 104, 96), rough=0.95)],
             [d.mat("laundry_b1", rgb8(214, 176, 124), rough=0.95), d.mat("laundry_b2", rgb8(150, 176, 154), rough=0.95), d.mat("laundry_b3", rgb8(216, 206, 196), rough=0.95)]]
    for k, uc in enumerate((1.95, 2.37)):
        ext, names = d.piece("wicker_basket_01", uc, 0.26, z0, rot=(0, 0, rnd.uniform(0, 6.28)), scale=1.0, tier="board", tris=None)
        gm = GM()
        bx = (ext[0] + ext[1]) / 2
        by = (ext[2] + ext[3]) / 2
        # the basket's opening is 0.13 in radius (the weave's inner face) under a flat rim lip out to 0.225: the first lump of cloth stands on the basket's floor inside the opening (radius 0.085 at the foot), the next two
        # lie over the lip, their feet 1 mm above its top (a sheet over the edge), so that no cloth passes through the wicker (DSP-03)
        rin = 0.072
        rout = 0.165
        # the cloth stands on the basket's floor: the highest point of the weave under its foot (the floor is not flat: its bumps rise 15 mm), found by rays
        zt = max(GB.rest_z(d, bx + 0.065 * math.cos(a_), by + 0.065 * math.sin(a_), 0.002, ring=4) for a_ in [2 * math.pi * i / 10 for i in range(10)] + [0.0]) + 0.0015
        zl = ext[5] + 0.012
        GB.heap(gm, bx, by, zt, rin, rin, 0.15, seed=3 + k, mi=0, amp=1.2)
        GB.heap(gm, bx - 0.30 * rout, by + 0.15 * rout, zl, rout * 0.9, rout * 0.9, 0.085, seed=7 + k, mi=1, amp=1.2)
        GB.heap(gm, bx + 0.45 * rout, by - 0.10 * rout, zl + 0.03, rout * 0.55, rout * 0.55, 0.07, seed=11 + k, mi=2, amp=1.2)
        d.gm_object("laundry_in_basket_%d" % k, gm, cloth[k], "scripted", "script:laundry_in_basket", tier="basket", smooth=True)
    # ---- the SERVICE WASHES card on two posts, behind the baskets
    cpth = os.path.join(tex, "service_card.png")
    cuv = GEN.card_atlas(cpth, ["SERVICE WASHES\nLEAVE IT WITH US"], cols=1, tile=(768, 240), size=70, bg=(232, 226, 204), ink=(150, 30, 40))
    GEN.TEXTS.extend(["SERVICE WASHES", "LEAVE IT WITH US"])
    cm = d.image_mat("service_card", cpth, rough=0.8)
    post_m = d.mat("easel_wood", rgb8(120, 84, 54), rough=0.7)
    gm = GM()
    gm.box(X(1.76), X(2.32), 0.505, 0.508, 0.52, 0.70, 0, uv_front=cuv[0])
    d.gm_object("service_card", gm, [cm], "scripted", "script:paper_card_service_washes", tier="stand")
    gm = GM()
    for uc in (1.81, 2.27):
        gm.box(X(uc) - 0.01, X(uc) + 0.01, 0.508, 0.528, z0, 0.60, 0)
    d.gm_object("service_card_posts", gm, [post_m], "support", "script:crate")
    # ---- the detergents: four large boxes on a low step at the back, in front three packets, two washing-up bottles and a bleach bottle
    designs = [("HOLME", "SOAP FLAKES", "for woollens", (60, 110, 170), (244, 240, 224), (220, 70, 60), "drop"),
               ("BRIGHTWELL", "WASHING\nPOWDER", "2 kg", (200, 60, 50), (246, 240, 220), (240, 200, 70), "star"),
               ("MEADOWS", "BIOLOGICAL\nPOWDER", "1.5 kg", (60, 130, 90), (246, 242, 226), (236, 200, 80), "leaf"),
               ("ASHDOWN", "FABRIC\nSOFTENER", "1 litre", (226, 170, 190), (70, 40, 70), (90, 150, 200), "wave"),
               ("HOLME", "SOAP FLAKES", "1 kg", (236, 200, 70), (50, 70, 130), (200, 60, 60), "drop"),
               ("BRIGHTWELL", "AUTOMATIC", "3 kg", (50, 90, 150), (244, 240, 224), (240, 190, 60), "sun"),
               ("LINDEN", "WASHING SODA", "1 kg", (120, 170, 190), (30, 50, 90), (240, 240, 230), "wave"),
               ("MEADOWS", "STARCH", "500 g", (236, 232, 214), (150, 40, 50), (60, 100, 150), "ear")]
    pk = os.path.join(tex, "detergents.png")
    puv = GB.packet_atlas(pk, designs, tile=(180, 280), cols=4)
    pm = d.image_mat("detergents", pk, rough=0.6)
    d.crate("detergent_step", 2.62, 3.30, 0.30, 0.50, z0, z0 + 0.08)
    gm = GM()
    for k, uc in enumerate((2.70, 2.87, 3.04, 3.21)):
        uv = puv[k % 4]
        gm.box(X(uc) - 0.080, X(uc) + 0.080, 0.34, 0.44, z0 + 0.08, z0 + 0.34, 0, uv_front=uv, uv_other=(uv[0] + 0.004, uv[1] + 0.5 * (uv[3] - uv[1])))
    d.gm_object("detergent_boxes_large", gm, [pm], "scripted", "script:detergent_boxes", tier="step")
    gm = GM()
    for k, uc in enumerate((2.76, 2.90, 3.04)):
        uv = puv[4 + k]
        gm.box(X(uc) - 0.055, X(uc) + 0.055, 0.20, 0.265, z0, z0 + 0.19, 0, uv_front=uv, uv_other=(uv[0] + 0.004, uv[1] + 0.5 * (uv[3] - uv[1])))
    d.gm_object("detergent_packets", gm, [pm], "scripted", "script:detergent_boxes", tier="board")
    # bottles: label atlas with the text in the front's quarter of the wrap (the lathe's u = 0.75 faces the street)
    bp = os.path.join(tex, "bottle_labels.png")
    from sw_gen import font
    btiles = [("FERNSIDE", "WASHING-UP\nLIQUID", (70, 150, 90)), ("FERNSIDE", "WASHING-UP\nLIQUID", (230, 190, 60)), ("LINDEN", "BLEACH", (60, 100, 170))]
    tw, th = 512, 256
    im = Image.new("RGB", (tw, th * len(btiles)), (200, 200, 200))
    dd = ImageDraw.Draw(im)
    buv = {}
    for k, (maker, prod, colr) in enumerate(btiles):
        y0 = k * th
        dd.rectangle([0, y0, tw - 1, y0 + th - 1], fill=(240, 236, 220))
        dd.rectangle([0, y0, tw - 1, y0 + 26], fill=colr)
        dd.rectangle([0, y0 + th - 26, tw - 1, y0 + th - 1], fill=colr)
        for cxm in (int(tw * 0.75), int(tw * 0.25)):
            f1 = GB.fit_text(dd, maker, "alfa-slab-one", int(tw * 0.40), 44)
            dd.text((cxm - dd.textlength(maker, font=f1) / 2, y0 + 40), maker, font=f1, fill=colr)
            yy = y0 + 40 + f1.size + 14
            for ln in prod.split("\n"):
                f2 = GB.fit_text(dd, ln, "oswald", int(tw * 0.40), 34)
                dd.text((cxm - dd.textlength(ln, font=f2) / 2, yy), ln, font=f2, fill=(40, 40, 60))
                yy += f2.size + 4
        GEN.TEXTS.extend([maker] + prod.split("\n"))
        buv[k] = (0.0, 1.0 - (y0 + th) / (th * len(btiles)), 1.0, 1.0 - y0 / (th * len(btiles)))
    im.filter(ImageFilter.GaussianBlur(0.5)).save(bp)
    bm_ = d.image_mat("bottle_labels", bp, rough=0.5)
    plastic = [d.mat("bottle_plastic_g", rgb8(60, 130, 80), rough=0.3), d.mat("bottle_plastic_y", rgb8(220, 180, 60), rough=0.3), d.mat("bottle_plastic_b", rgb8(60, 100, 170), rough=0.3), d.mat("bottle_cap", rgb8(236, 232, 220), rough=0.4)]
    # a washing-up bottle 0.20 tall, r 0.032; a bleach bottle 0.24 tall, r 0.04
    for k, (uc, vv, hh, rr_, bi, pi_) in enumerate(((3.135, 0.20, 0.20, 0.032, 0, 0), (3.205, 0.20, 0.20, 0.032, 1, 1), (3.285, 0.245, 0.24, 0.040, 2, 2))):
        gm = GM()
        GB.bottle(gm, X(uc), vv, z0, rr_, hh, mi=0, mi_cap=1, label=(3, 4), label_mi=2, label_uv=buv[bi], n=24)
        d.gm_object("detergent_bottle_%d" % k, gm, [plastic[pi_], plastic[3], bm_], "scripted", "script:detergent_boxes", tier="board", smooth=True)
    # ---- the price cards
    texts = ["TOWELS\n£3.50", "BASKETS\n£4.25", "POWDER\n49p", "SOAP FLAKES\n58p", "BLEACH\n42p", "SERVICE WASH\n35p a lb"]
    path = os.path.join(tex, "price_cards.png")
    uvs = GEN.card_atlas(path, texts, cols=3, tile=(256, 128), size=42)
    pmm = [d.image_mat("price_cards", path, rough=0.8), d.mat("stake", rgb8(60, 60, 62), rough=0.5, metal=0.7)]
    for k, (uc, vv) in enumerate(((0.45, 0.05), (2.16, 0.06), (2.78, 0.12), (3.04, 0.115), (3.22, 0.12), (1.20, 0.05))):
        d.price_card(uc, vv, z0, k, uvs, pmm)
    d.display_texts = list(GEN.TEXTS) + [t.replace("\n", " ") for t in texts]
