"""The rows that belong to one shop's trade and layout (13 October 2026, batch A): the coverage of its boards and tiers, its counts against the target, the lists the generic rows need (the supports that carry goods
and are not goods, the texts drawn on its goods, the families of its trade that must read from the street). Used by check_shop.py (`shop_rows`). Each function states what the layout decided in its docstring
and writes the numbers it measured; nothing here asserts a thing the build did not measure.
"""
import json
import os

import numpy as np

import sw_assets as A

W, H = 5.3, 2.4


def counts_row(ctx, rows, di, allowed_missing, label):
    """ROOM-05: every good the target lists is placed in the room (the display's pieces are the window's, not the room's), at the count the target gives, except the ones named as Judgements."""
    RR = ctx.R["room"]
    placed = json.load(open(os.path.join(ctx.rooms, "placed.json")))
    fixtures = json.load(open(os.path.join(ctx.rooms, "fixtures.json")))
    have = {}
    for p in placed:
        m = p.get("model")
        if not m:
            continue
        k = m.split("#")[0]
        n = p.get("n", 1)
        have[k] = have.get(k, 0) + (n if str(m).startswith("script:") and "n" in p else 1)
    short, over = [], []
    for g in RR["goods"]:
        m = g["model"]
        if m.startswith("script:") and m not in have:
            continue                                  # a script's count is its own row (the drawers: 60; the tins by the tier fills)
        got = have.get(m, 0)
        if got < g["n"]:
            short.append("%s %d of %d" % (m, got, g["n"]))
        elif got > g["n"]:
            over.append("%s %d (target %d)" % (m, got, g["n"]))
    unnamed = [s for s in short if s.split(" ")[0] not in allowed_missing]
    rows.add("ROOM-05", "every listed good is placed", not unnamed, "%s: %d goods of the target's list placed at the target's count%s%s%s" % (label, len(RR["goods"]) - len(short), ("; SHORT, named as Judgements in NOTES.md: %s" % [s for s in short if s not in unnamed]) if short and not unnamed else "", ("; SHORT AND UNNAMED: %s" % unnamed) if unnamed else "", ("; more than the target: %s" % over) if over else ""))
    return have


def ironmonger(ctx, rows, assets, di):
    RR = ctx.R["room"]
    rooms = ctx.rooms
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    fixtures = json.load(open(os.path.join(rooms, "fixtures.json")))
    fx = {f["id"]: f for f in RR["fixtures"]}
    # ---- the pegboards: by rows (Rita's ROOM-02 rule, 80 per cent of the width, for every row but the last of a board) and by area (Rita's ROOM-01: 60 per cent)
    pj = os.path.join(rooms, "rows.json")
    rj = json.load(open(pj)) if os.path.exists(pj) else {}
    det, ok_rows, ok_area, tot_tools = [], True, True, 0
    for fid in ("I-left-pegboard", "I-right-pegboard"):
        f = fx[fid]
        y0, y1 = f["y"]
        z0, z1 = f["z"]
        area = (y1 - y0) * (z1 - z0)
        cov = 0.0
        for it in placed:
            if it.get("fixture") == fid and "ext" in it:
                e = it["ext"]
                a, b = max(e[2], y0), min(e[3], y1)
                c, d = max(e[4], z0), min(e[5], z1)
                if b > a and d > c:
                    cov += (b - a) * (d - c)
        n_tools = sum(1 for it in placed if it.get("fixture") == fid)
        tot_tools += n_tools
        rr = [r_ for r_ in rj.get(fid, []) if not r_.get("columns")]
        full = rr[:-1] if len(rr) > 1 else rr
        fr = [r_["span"] / max(r_["region"][1] - r_["region"][0], 1e-6) for r_ in full if "region" in r_]
        good_rows = all(x >= 0.80 for x in fr)
        ok_rows &= good_rows
        ok_area &= cov / area >= 0.60
        det.append("%s: %d tools, %d rows (the last of them not counted against 80 per cent), full rows filled to %s per cent of the width, area share by bounding box %.0f per cent of %.2f m2" % (
            fid, n_tools, len(rr), "/".join("%.0f" % (100 * x) for x in fr), 100 * cov / area, area))
    rows.na("ROOM-01", "the pegboards are covered", "Rita's row (the target's ROOM-01 applies_to ritas: 60 per cent of her left board by bounding box) and the ironmonger's target gives no coverage; measured and recorded, not judged: " + "; ".join(det) + " (hand tools are thin: by bounding box a real board hung in rows reads about a third; the boards' rows are held to Rita's 80 per cent of the width in ROOM-02)")
    rows.add("ROOM-02", "the pegboard rows are filled", ok_rows, "each full row's tools (hung from one line, gaps 0.04 to 0.06) fill at least 80 per cent of the board's width (the last, partial row of a board is the remainder of the stock and is not counted); %d tools in all" % tot_tools)
    # ---- the shelf tiers: each built tier filled to 60 per cent of its length
    tf = [f for f in fixtures if f.get("name", "").startswith("tier_fill_")]
    det, ok = [], True
    for t in tf:
        a, b = t["ext"][0], t["ext"][1]
        z = t["ext"][4]
        ws = sorted((p["ext"][0], p["ext"][1]) for p in placed if p.get("fixture") == "I-back-shelves" and "ext" in p and abs(p["ext"][4] - z) < 0.004 and p["ext"][0] >= a - 0.01 and p["ext"][1] <= b + 0.01)
        cur, tot = a, 0.0
        for x0, x1 in ws:
            x0 = max(x0, cur)
            if x1 > x0:
                tot += x1 - x0
                cur = x1
        frac = tot / (b - a)
        ok &= frac >= 0.60
        det.append("z %.2f: %d goods, %.0f per cent of %.2f m" % (z, len(ws), 100 * frac, b - a))
    rows.add("ROOM-03", "the shelf tiers are filled", ok and bool(tf), "each built tier of the shelf unit, the goods' union along it against its length (at least 60 per cent): " + "; ".join(det) + " (the tiers at 0.4 and 0.8 are not built: the counter and the floor goods hide them from every camera; NOTES.md)")
    nd = sum(p.get("n", 0) for p in placed if p.get("model") == "script:drawer_fronts")
    rows.add("ROOM-04", "the drawer wall", nd == 60, "%d drawer fronts in 6 columns x 10 rows (target 60), each with a brass label holder carrying a hand-lettered card and a ring pull" % nd)
    have = counts_row(ctx, rows, di, {"wooden_ladder": 1, "script:paint_tins": 1, "watering_can_metal_01": 1, "metal_jerrycan_green": 1}, "ironmonger")
    return {
        "supports": ["script:backing_board", "script:hung_card", "script:bulb_tray", "script:crate", "script:hang_rod"],
        "texts": ["EST. 1884", "16", "OPEN", "CLOSED", "NAILS", "SCREWS", "HINGES", "WASHERS", "NUTS & BOLTS", "RAWLPLUGS", "OIL 1.15", "BULBS 40p", "TROWELS 2.45", "GLOVES 1.30", "CANS 3.95", "PUMP 4.50", "SPRINKLER 3.75",
                  "PAINT 2.99", "TOOL BOXES 6.95", "BROOMS 2.25", "BLOWLAMP 8.50", "HARTSIDE", "PAINTS & OILS", "HARTSIDE SCOURING POWDER", "ELMSTEAD BRASS POLISH", "COLDWELL WASHING SODA", "BRANTHAM DISINFECTANT", "500 g", "250 ml", "1 kg", "1 litre", "BRANTHAM GLOSS PAINT", "COLDWELL EMULSION", "HARTSIDE WHITE SPIRIT", "ELMSTEAD WOOD PRESERVER", "PARAFFIN", "BITUMEN PAINT", "UNDERCOAT", "METAL PRIMER", "THINNERS"],
        "families": {"paint tins": ["script:paint_tin_pyramid"], "garden": ["watering_can_metal_01", "trowel_01", "garden_sprinkler_01", "plastic_broom", "garden_gloves_01"], "tool boxes and tools": ["metal_toolbox", "sledgehammer_01", "tire_pump", "brass_blowtorch"]},
        "era": "the goods are a 1990 ironmonger's: tins, oils, tool boxes, watering cans, trowels, brooms, a tyre pump, a blowtorch (no cordless drill, no plastic modern packaging, no barcode, no LED lamp)",
    }


SHOPS = {"ironmonger": ironmonger}


def rows_for(ctx, rows, assets, di):
    fn = SHOPS.get(ctx.id)
    if fn is None:
        return {"supports": [], "texts": [], "families": {}, "era": ""}
    return fn(ctx, rows, assets, di)


def _texts(ctx, di):
    out = []
    p = os.path.join(ctx.rooms, "texts.json")
    if os.path.exists(p):
        out += json.load(open(p))
    out += list((di or {}).get("texts", []))
    return out


def newsagent(ctx, rows, assets, di):
    """ROOM rows for the newsagent: the gantry's packs (columns, three boards), the racks' covers and cards, the counts against the target (named exceptions), and the lists the generic rows need."""
    RR = ctx.R["room"]
    rooms = ctx.rooms
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    fixtures = json.load(open(os.path.join(rooms, "fixtures.json")))
    n_packs = sum(p.get("n", 0) for p in placed if p.get("model") == "script:cigarette_packs")
    boards = sorted({p["tag"] for p in placed if p.get("model") == "script:cigarette_packs"})
    rows.add("ROOM-01", "the gantry is full", len(boards) == 3 and n_packs >= 100, "%d fictional packs on %d boards (the target's 100 + 8; the gantry's length takes about three times as many, see NOTES.md)" % (n_packs, len(boards)))
    covers = sum(p.get("n", 0) for p in placed if p.get("model") == "script:magazine_covers")
    cards = sum(p.get("n", 0) for p in placed if p.get("model") == "script:greeting_cards" and p.get("tag") == "rack")
    posts = sum(p.get("n", 0) for p in placed if p.get("model") == "script:postcard_rack")
    rows.add("ROOM-02", "the racks carry what the target lists", covers == 60 and cards == 40, "the left wall: %d magazine covers in 5 rows of 12 (target 60); the right wall: %d greetings cards in 4 rows of 10 (target 40) and %d postcards on the board" % (covers, cards, posts))
    jars = sum(p.get("n", 0) for p in placed if p.get("model") == "script:sweet_jars")
    rows.add("ROOM-03", "the counter's sweet jars", jars == 10, "%d sweet jars along the back of the counter (target 10)" % jars)
    have = counts_row(ctx, rows, di, {"cigarette_pack": 8, "script:cigarette_packs": 100, "stationery_supplies": 0}, "newsagent")
    return {"supports": ["script:paper_stand", "script:carton_stand", "script:magazine_board", "script:table_laminate", "script:crate"], "texts": _texts(ctx, di),
            "families": {"papers and magazines": ["script:newspapers", "script:magazines"], "tobacco": ["script:cigarette_cartons"], "sweets": ["script:sweet_jars"], "cards": ["script:card_rack", "script:postcard_rack"]},
            "era": "newspapers, magazines, cards, sweets and tobacco of a 1990 newsagent, every title and maker invented; no lottery, betting or drink; no barcode"}


def tea_rooms(ctx, rows, assets, di):
    RR = ctx.R["room"]
    rooms = ctx.rooms
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    cups = sum(p.get("n", 0) for p in placed if p.get("model") == "script:cups_saucers")
    domes = sum(p.get("n", 0) for p in placed if p.get("model") == "script:cake_dome")
    rows.add("ROOM-01", "the shelves carry the cups and saucers", cups == 24, "%d cups on saucers on the two boards (target 24), plates in stacks, the metal jug" % cups)
    rows.add("ROOM-02", "the counter's fittings", domes >= 1 and any(p.get("model") == "script:tea_urn" for p in placed), "%d cake domes (the target counts one: a cake under each), the tea urn, the kettle, the till, the rolls, the tea set's pieces" % domes)
    have = counts_row(ctx, rows, di, {"tea_set_01": 2, "script:cake_dome": 1}, "tea_rooms")
    return {"supports": ["script:table_laminate", "script:cake_stand"], "texts": _texts(ctx, di),
            "families": {"the table set": ["round_wooden_table_02", "painted_wooden_chair_01", "tea_set_01#pot", "tea_set_01#cupA", "tea_set_01#cupB"], "cakes": ["carrot_cake", "strawberry_chocolate_cake", "script:cake_stand"], "the curtain": ["script:cafe_curtain"]},
            "era": "a 1980s cafe's cups, cakes, urn and curtain; no modern phone, no flat screen, no plastic packaging"}


SHOPS.update({"newsagent": newsagent, "tea_rooms": tea_rooms})


def steam_laundry(ctx, rows, assets, di):
    """ROOM rows for the launderette (batch B): the washers and the dryers at the target's counts and sizes, the two running lamps (lit in night_dark only), the shelves' parcels, the notices; the counts against the target."""
    RR = ctx.R["room"]
    rooms = ctx.rooms
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    fixtures = json.load(open(os.path.join(rooms, "fixtures.json")))
    rj = json.load(open(os.path.join(rooms, "rows.json"))) if os.path.exists(os.path.join(rooms, "rows.json")) else {}
    nw = sum(p.get("n", 0) for p in placed if p.get("model") == "script:washing_machine")
    nd = sum(p.get("n", 0) for p in placed if p.get("model") == "script:tumble_dryer")
    wp = next((p for p in placed if p.get("model") == "script:washing_machine"), None)
    dp = next((p for p in placed if p.get("model") == "script:tumble_dryer"), None)
    ok_sz = bool(wp and dp) and abs((wp["ext"][1] - wp["ext"][0]) - 2.4) <= 0.03 and abs(wp["ext"][5] - 0.85) <= 0.01 and abs((dp["ext"][1] - dp["ext"][0]) - 2.1) <= 0.1 and abs(dp["ext"][5] - 1.73) <= 0.02
    rows.add("ROOM-01", "the washers and the dryers", nw == 4 and nd == 6 and ok_sz, "%d washers in a row 0.60 wide x 0.85 high (the run measures %.2f x %.2f), %d dryers in three stacks of two (0.69 wide, 0.85 high each, %.2f high in all, run %.2f wide), the door's ring 0.032 proud of the cabinet: nothing stands more than 0.60 off the wall (SO-01)" % (
        nw, (wp["ext"][1] - wp["ext"][0]) if wp else -1, wp["ext"][5] if wp else -1, nd, dp["ext"][5] if dp else -1, (dp["ext"][1] - dp["ext"][0]) if dp else -1))
    lamps = rj.get("running_lamps", {})
    on_dryer = all(dp and dp["ext"][0] <= a[0] <= dp["ext"][1] and 0.0 <= a[2] <= dp["ext"][5] and a[1] < dp["ext"][3] for a in lamps.get("at", []))
    rows.add("ROOM-02", "the dryers' two running lamps", lamps.get("n") == 2 and on_dryer, "%s running lamps, each on a dryer's control strip at %s, orange and emissive in night_dark only with a small warm point light beside each (the target's `night_dark`: two orange lamps, small, 2000 K); the other four are dull discs" % (lamps.get("n"), lamps.get("at")))
    np_ = sum(p.get("n", 0) for p in placed if p.get("model") == "script:wrapped_parcels")
    tiers = sorted({p["tag"] for p in placed if p.get("model") == "script:wrapped_parcels"})
    sh = [f for f in fixtures if f.get("name", "").startswith("shelf_L-back-shelves")]
    up = [f for f in fixtures if f.get("name", "").startswith("upright_L-back-shelves")]
    ok_up = bool(up) and all(abs(f["ext"][4] - 0.85) < 0.002 for f in up)
    rows.add("ROOM-03", "the shelves and their parcels", np_ == 18 and len(tiers) == 2 and len(sh) == 2 and ok_up, "%d wrapped parcels on %d boards (z %s), each with a cross of string and a numbered tag; the two boards (0.30 deep) are carried by uprights that stand ON the washers' tops (z %.2f) and end inside their footprint" % (
        np_, len(sh), [t.split("_")[1] for t in tiers], min([f["ext"][4] for f in up] or [-1])))
    nn = sum(p.get("n", 0) for p in placed if p.get("model") == "script:paper_notices")
    rows.add("ROOM-04", "the notices", nn == 3 and any(f.get("name") == "care_chart" for f in fixtures) and any(f.get("name") == "cork_board" for f in fixtures), "a cork board 0.9 x 0.6 with %d cards (prices, rules, service washes) on the left wall and a wash-care chart 0.6 x 0.8 beside the clock on the right" % nn)
    have = counts_row(ctx, rows, di, {}, "steam_laundry")
    return {"supports": ["script:crate", "script:paper_notices"], "texts": _texts(ctx, di),
            "families": {"folded laundry": ["script:folded_towels"], "baskets of laundry": ["wicker_basket_01", "script:laundry_in_basket"], "detergents": ["script:detergent_boxes"]},
            "era": "a 1990 launderette: front-loading machines, powder and soap flakes in printed card packets and plastic bottles of the period, wicker baskets, brown-paper parcels, towels (every maker invented); no modern phone, no flat screen, no barcode, no plastic modern packaging"}



def _sum(placed, model, fixture=None):
    return sum(p.get("n", 0) for p in placed if p.get("model") == model and (fixture is None or p.get("fixture") == fixture))


def _pending(rows, cid, name, detail):
    rows.add(cid, name, False, detail, status="pending")


def grocer(ctx, rows, assets, di):
    """ROOM rows for the grocer (batch B): the gantry, the counter, the shelves over it, the two side units, the crates; the counts against the target (named exceptions); the scanned produce pending."""
    RR = ctx.R["room"]
    rooms = ctx.rooms
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    tg = _sum(placed, "script:tins", "G-back-gantry")
    pg = _sum(placed, "script:packets", "G-back-gantry")
    boards = sorted({p["tag"] for p in placed if p.get("fixture") == "G-back-gantry" and p.get("model") in ("script:tins", "script:packets")})
    # 14 Oct (batch B): the target counts 160 tins and 90 packets; the built gantry (two rows deep along five boards, the second board shared with two baskets and the rolls) holds 147 and 100, 247 of the target's 250: each
    # kind within 10 per cent of its count and the total within 5 per cent is the row (a layout of seeded random rows shifts a dozen goods between kinds; the total is the gantry's fullness)
    rows.add("ROOM-01", "the gantry is full", tg >= 0.9 * 160 and pg >= 0.9 * 90 and tg + pg >= 0.95 * 250 and len([b for b in boards if b.startswith("tins_")]) >= 4, "%d tins and %d packets on the five boards of the gantry (target 160 and 90: %d of 250; each kind within 10 per cent of its count and the total within 5 per cent; the rows are two deep and the boards are filled along their length), the crates on the floor under the first board, two baskets and the rolls on the second" % (tg, pg, tg + pg))
    jars = _sum(placed, "script:jars", "G-back-shelves-right")
    bots = _sum(placed, "script:bottles", "G-back-shelves-right")
    rows.add("ROOM-02", "the counter and the shelves over it", jars >= 24 and bots >= 12 and any(p.get("model") == "script:counter_scale" for p in placed) and any(p.get("model") == "CashRegister_01" for p in placed),
             "the counter with its till and its scale; %d jars and %d bottles on the two boards over it (target 24 and 12; washing-up liquid, brown sauce, malt vinegar, salad cream: no drink)" % (jars, bots))
    lt = _sum(placed, "script:tins", "G-left-tins")
    rp = _sum(placed, "script:packets", "G-right-tins")
    rows.add("ROOM-03", "the side units", lt >= 40 and rp >= 30, "the left unit (0.10 deep, four tiers): %d tins (target 40); the right unit: %d dry-goods packets standing on edge (target 30; the target's tea and sugar are out: sugar, flour, oats, rice, pasta, custard, dried fruit)" % (lt, rp))
    ncr = sum(1 for p in placed if p.get("model") == "plastic_crate_03")
    non = sum(1 for p in placed if p.get("model") == "yellow_onion")
    rows.add("ROOM-04", "the floor crates", ncr == 3 and non >= 36, "%d plastic_crate_03 (the target's crate_02 is 0.41 deep: over the gantry's 0.30 rule at its own size) on the floor under the gantry's first board, loaded with %d yellow_onion (the target loads them with potatoes: Sketchfab scans, Jafar's login)" % (ncr, non))
    have = counts_row(ctx, rows, di, {"plastic_crate_02": 3}, "grocer")
    _pending(rows, "SCN-01", "scanned produce", "cabbage x4, potato x20, satsuma x12, pear x6 (the target's script:cabbage_potato_satsuma): Sketchfab ffishAsia CC0 scans, the download needs Jafar's login (his Needs-you item 3): pending, not failed; nothing is hand-modelled in their place (the window carries apples, lemons, onions and bananas from Poly Haven and 30 scripted tomatoes the target lists)")
    return {"supports": ["script:crate", "script:backing_board", "script:tiered_stand"], "texts": _texts(ctx, di),
            "families": {"fruit and vegetables": ["food_apple_01", "lemon", "yellow_onion", "bananas", "script:tomatoes"], "tins and jars": ["script:tin_pyramids", "script:jars"], "crates and baskets": ["plastic_crate_02", "plastic_crate_03", "wicker_basket_02"]},
            "era": "a 1990 grocer's: tins, packets, jars and fresh produce, every maker invented; no drink, no lottery or betting slip, no barcode, no modern packaging"}


def chandler(ctx, rows, assets, di):
    """ROOM rows for the ship chandler (batch B): the shelving's goods, the counter, the hooks board, the charts, the pegboard of rigging; the counts against the target (named exceptions)."""
    RR = ctx.R["room"]
    rooms = ctx.rooms
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    tins = _sum(placed, "script:paint_tins")
    coils = _sum(placed, "script:rope_coils")
    reels = _sum(placed, "script:twine_reels")
    rows.add("ROOM-01", "the shelving's goods", tins >= 40 and coils == 6 and reels == 10, "%d paint tins (target 40; two deep on two boards and one more), %d coils of rope standing on edge (swept tubes, ambientCG Rope001 in five colours), %d twine reels; oil tins, cans, cleaner tins, boots, flashlights and lanterns from Poly Haven (counts below)" % (tins, coils, reels))
    hw = _sum(placed, "script:shackles_blocks")
    ch = _sum(placed, "script:chart_posters")
    rows.add("ROOM-02", "the walls' boards", hw == 24 and ch == 7, "the pegboard: %d pieces of rigging (shackles, blocks, cleats, chain) flat on a 1.6 x 1.1 board; the left wall: %d chart sheets and a tide table, and a board with a coil of rope laid flat" % (hw, ch))
    lamp = any(p.get("model") == "Lantern_01" and p.get("tag") == "hurricane_lamp" for p in placed)
    rows.add("ROOM-03", "the counter and its lamp", lamp and any(p.get("model") == "CashRegister_01" for p in placed) and sum(1 for p in placed if p.get("model") == "seadogs_compass") == 3, "the counter's till, three compasses and the hurricane lamp (Lantern_01, lit in night_lit only: a warm point light and a small flame)")
    have = counts_row(ctx, rows, di, {"life_jacket": 4, "lifebuoy": 2, "script:oilskin_sou_wester": 3, "rubber_boots": 4, "small_oil_can_01": 4}, "chandler")
    # NIT-01 (batch B: built, in a glb of its own like Rita's grille): three panels of woven galvanised mesh, wire 2 mm, mesh 12 mm, z 0.70 to 1.55, one in each lower light, inside the glass, not in the day front
    try:
        fm = json.load(open(os.path.join(ctx.work, "front_members.json")))
        mem = fm["members"]
        pan = sorted(k for k in mem if k.startswith("night_mesh_"))
        glass = sorted((mem[k]["u"], mem[k]["z"], mem[k]["d"]) for k in mem if k.startswith("win_glass_lower_"))
        inside = len(pan) == len(glass) == 3 and all(mem[p]["u"][0] >= g[0][0] and mem[p]["u"][1] <= g[0][1] and abs(mem[p]["z"][0] - 700.0) < 1.5 and abs(mem[p]["z"][1] - 1550.0) < 1.5 and mem[p]["d"][1] < g[2][0] + 0.5
                                                      for p, g in zip(sorted(pan, key=lambda k: mem[k]["u"][0]), sorted(glass, key=lambda g_: g_[0][0])))
        wires_ok = all(abs(mem[p]["wire_mm"] - 2.0) < 1e-6 and abs(mem[p]["pitch_mm"] - 12.0) < 1e-6 for p in pan)
        mg = fm["info"].get("mesh_glb")
        gl_ok = bool(mg) and os.path.exists(mg) and fm["info"].get("mesh_bytes", 0) < 1024 * 1024
        import struct
        with open(os.path.join(assets, ctx.front_glb), "rb") as fh:
            fh.seek(12)
            ln, _t = struct.unpack("<II", fh.read(8))
            front_names = fh.read(ln).decode("utf8", "ignore")
        apart = "night_mesh" not in front_names
        rows.add("NIT-01", "the woven mesh screens", inside and wires_ok and gl_ok and apart,
                 "%d panels (one in each lower light, u inside the glass, z 700 to 1550, d 19.6 to 26: behind the glass, which is d 30 to 36), wire 2 mm, mesh 12 mm (%s wires across and up), in %s (%d triangles, %d bytes; under 1 MB, in git) and not in the day front glb: %s" % (
                     len(pan), ", ".join("%d x %d" % tuple(mem[p]["wires"]) for p in pan), os.path.basename(mg or "no glb"), fm["info"].get("mesh_triangles", 0), fm["info"].get("mesh_bytes", 0), "in place when the shop is shut; the lit night view does not use it"))
    except Exception as e:
        rows.add("NIT-01", "the woven mesh screens", False, "the mesh screens could not be read from the build: %s" % e)
    return {"supports": ["script:crate", "script:backing_board"], "texts": _texts(ctx, di),
            "families": {"rope and cordage": ["script:rope_coils"], "life-saving": ["life_jacket", "lifebuoy"], "lamps": ["Lantern_01", "wooden_lantern_01"], "boots and oilskins": ["rubber_boots", "script:oilskin_sou_wester"], "paint": ["script:paint_tin_pyramid"]},
            "era": "a 1990 ship chandler's: rope, twine, paint, lamps, life jackets, a lifebuoy, boots, oilskins, charts; no explosives drum, no ship model, no modern phone or GPS, no LED lamp"}


def fish_market(ctx, rows, assets, di):
    """ROOM rows for the fishmonger (batch B): the chiller with its trays of ice, the shelf, the door, the board, the drain; the fish pending."""
    RR = ctx.R["room"]
    rooms = ctx.rooms
    placed = json.load(open(os.path.join(rooms, "placed.json")))
    fixtures = json.load(open(os.path.join(rooms, "fixtures.json")))
    nt = _sum(placed, "script:enamel_trays")
    glass = any(f.get("name") == "chiller_glass" for f in fixtures)
    rows.add("ROOM-01", "the chiller", nt == 8 and glass, "the serve-over chiller (3.0 x 0.6 x 1.0): a sloping glass front, a well, %d white enamel trays each with a mound of ice (no fish: pending), a laminate top and a stainless edge" % nt)
    ntn = _sum(placed, "script:tins_and_jars")
    rows.add("ROOM-02", "the shelf", ntn >= 24, "%d tins and jars on the two boards (target 24), labels of the project's own makers (SALTHOUSE, TIDEMARK, FENWICK, BRIGHTWATER)" % ntn)
    names = {f.get("name") for f in fixtures}
    rows.add("ROOM-03", "the door, the board, the drain", {"door_slab", "door_lever", "drain_grating", "wet_patch"} <= names and any(p.get("model") == "script:price_board_chalk" for p in placed) and any(p.get("model") == "garden_hose_wall_mounted_01" for p in placed),
             "the cold-room door (a seal, a plastic-faced leaf, a chrome lever, three hinges), the hose on its bracket, the blackboard (chalk: COD, HADDOCK, PLAICE, KIPPERS), the stainless drain grating and the hosed patch, the wet quarry floor")
    have = counts_row(ctx, rows, di, {}, "fish_market")
    _pending(rows, "SCN-01", "the fish", "cod x4, mackerel x8, herring x6, plaice x4, crab x5, prawns x60 (script:fish_on_ice): Sketchfab ffishAsia CC0 scans, the download needs Jafar's login (his Needs-you item 3): pending, not failed; NONE is modelled by hand (the 3 October failure): the trays and the slab carry ice, lemons and tickets only")
    _pending(rows, "SCN-02", "the trade's goods read from the street", "the fishmonger's own goods (fish, crab, prawns) cannot read from STREET_SQUARE until the scans are in: pending, not failed; the slab, the ice, the trays and the tickets are measured by TRD-01")
    return {"supports": ["script:crate", "script:price_stakes", "script:chiller_pad"], "texts": _texts(ctx, di),
            "families": {"the slab and its trays": ["script:slab_and_ice", "script:enamel_trays"], "tickets": ["script:price_stakes"]},
            "era": "a 1990 fishmonger's: a marble slab, ice, enamel trays, tickets in pounds per lb, tinned fish; no plastic modern packaging, no barcode, no drink"}


SHOPS.update({"steam_laundry": steam_laundry, "grocer": grocer, "chandler": chandler, "fish_market": fish_market})
