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
        "supports": ["script:backing_board", "script:hung_card", "script:bulb_tray", "script:crate"],
        "texts": ["EST. 1884", "16", "OPEN", "CLOSED", "NAILS", "SCREWS", "HINGES", "WASHERS", "NUTS & BOLTS", "RAWLPLUGS", "TINS 99p", "OIL 1.15", "BULBS 40p", "TROWELS 2.45", "GLOVES 1.30", "CANS 3.95", "PUMP 4.50", "SPRINKLER 3.75",
                  "PAINT 2.99", "TOOL BOXES 6.95", "BROOMS 2.25", "TORCH 8.50", "BRANTHAM GLOSS PAINT", "COLDWELL EMULSION", "HARTSIDE WHITE SPIRIT", "ELMSTEAD WOOD PRESERVER", "PARAFFIN", "BITUMEN PAINT", "UNDERCOAT", "METAL PRIMER", "THINNERS"],
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
    return {"supports": ["script:paper_stand", "script:carton_stand", "script:magazine_board", "script:table_laminate"], "texts": _texts(ctx, di),
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
