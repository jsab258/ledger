#!/usr/bin/env python
"""Author tool: build target.json for the shop windows (unit 7) from the repository's own homes and sw_shops.py.

    /home/user/.bpyenv/bin/python make_target.py [--refresh]      # --refresh asks api.polyhaven.com again (else polyhaven_checked.json is used)

Reads (never copies by hand): production/specs/shop-interiors.json, vignette-scene.json, vignette-pieces.json, hook-cast.json,
production/cloud-week/targets/shopfronts/target.json (2.2: the ten fronts), targets/fascia-signs/target.json (4.1: the ten boards),
tools/ue/make_interior_material.py (the game's rule), sw_common.py (the budgets from that rule), sw_shops.py (rooms and displays).
"""
import argparse
import json
import math
import os
import sys
import time
import urllib.request

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_common as S  # noqa: E402
import sw_shops as SH  # noqa: E402

ROOT = S.ROOT
P22 = os.path.join(ROOT, "production", "cloud-week", "targets", "shopfronts", "target.json")
P41 = os.path.join(ROOT, "production", "cloud-week", "targets", "fascia-signs", "target.json")
SPEC = os.path.join(ROOT, "production", "specs", "shop-interiors.json")
CAST = os.path.join(ROOT, "production", "specs", "hook-cast.json")
LOOK = os.path.join(ROOT, "production", "specs", "unreal-look.json")
PIECES = os.path.join(ROOT, "production", "specs", "vignette-pieces.json")
PHCACHE = os.path.join(HERE, "polyhaven_checked.json")
DATE = "2026-10-12"
UA = "ledger-shop-windows-target/1.0"

# ------------------------------------------------------------------------------------------------------------------------------------
# who owns what, and the order the street lists the shops (production/specs/vignette-scene.json, DECISIONS 3 Oct, RULINGS 2 and 3 Oct)
OWNER = {"mickeys": "Mickey (Michael Suddaby, dead); Tom Nowak inherits; Ron Kirby and Sheila Dunn keep it (canon.md)",
         "ritas": "Rita (hook-cast.json: keeper 'rita'; no surname in canon)",
         "newsagent": "no keeper named; hook-cast.json puts Hal's shop (the coin shop, keeper 'hal', 10 to 18) at x 39, INSIDE this bay (x 36 to 42): a conflict, not resolved here"}
HAL_NOTE = ("hook-cast.json places 'Hals_shop' (keeper hal, hours 10 to 18, Wed 10 to 13) at street x 39, which is inside the newsagent's bay (x 36 to 42): "
            "either the coin shop is the newsagent's neighbour (there is none) or one of them is not on the street. Not resolved: the newsagent is built as ruled (3 Oct).")

# the 3.2 kit's built variants (kit/shopfront/NOTES.md: Rita's variants only)
KIT_BUILT = {"pilaster": ["panel"], "console": ["scroll"], "cornice": ["timber"], "stallriser": ["panel"], "window_frame": ["T1"], "sill": ["timber"],
             "fascia_board": ["plain"], "door_F1": ["F1"]}

# the toplights per light (3.2 kit departure D6: each mullion carried up as a bar, each light's toplight split equally by 28 wide bars); the lights' own count is the 2.2 pattern's
PER_LIGHT = {"mickeys": 1, "fish_market": 1, "ritas": 3, "empty_unit": 3, "steam_laundry": 1, "grocer": 2, "chandler": 1, "tea_rooms": 2, "ironmonger": 3, "newsagent": 3}
# the 2.2 target.json this target takes the nine other fronts from, at its commit (git log -1 -- production/cloud-week/targets/shopfronts/target.json)
P22_COMMIT = "dd706f6"
P22_FILE = "production/cloud-week/targets/shopfronts/target.json"
_PIL_PROFILE = {"panel": ["shaft_panel_plan", "plinth_panel_side_through_stile", "plinth_panel_side_through_field", "panel_bead"], "flute": ["shaft_flute_plan", "plinth_stepped_side"],
                "render": ["shaft_render_plan", "plinth_cap_side"], "clad": ["clad_plan", "plinth_cap_side"]}
_WIN_PROFILE = {"T1": ["mullion_t1_plan", "jamb_t1_plan", "transom_t1", "toplight_bar_plan", "glazing_bead_ovolo", "head_section"],
                "T2": ["mullion_t2_plan", "jamb_t1_plan", "transom_t1 (2.2 gives no T2 transom)", "toplight_bar_plan", "glazing_putty", "head_section"],
                "M1": ["mullion_m1_plan", "jamb_m1_plan", "transom_m1", "glazing_bead_gasket", "head_section"],
                "M2": ["bar_m2_plan", "transom_m1 (the only metal transom in 2.2: Judgement)", "glazing_bead_gasket", "head_section"]}


def build_from(f):
    """The exact keys of 2.2's target.json (at P22_COMMIT) a script reads to build every part of one front that the 3.2 kit lacks."""
    v = f["glazing"]["window_frame"]
    k = ["parts.pilaster.variants.%s with parts.pilaster.profiles %s and base_ogee, capital_side" % (f["pilaster"], _PIL_PROFILE[f["pilaster"]]),
         "parts.console.variants.%s" % f["console"], "parts.stallriser.variants.%s (and profiles.panel_bead for panel)" % f["stallriser"]["variant"],
         "parts.window_frame.dims, .variants.%s, .profiles %s" % (v, _WIN_PROFILE[v]),
         "parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door %s)" % f["shop_door"]]
    if f["side_door"]:
        k.append("parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it)")
    if f["lobby"]["kind"] != "flush":
        k.append("parts.lobby.dims.%s and parts.lobby.profiles.%s; alterations.recessed_lobby.numbers.%s" % ("grocer" if f["lobby"]["depth"] == 600 else "steam_laundry", "plan_grocer" if f["lobby"]["depth"] == 600 else "plan_laundry", "grocer" if f["lobby"]["depth"] == 600 else "steam_laundry"))
    for a_ in f["alterations"]:
        k.append("alterations.%s" % a_)
    return {"file": P22_FILE, "commit": P22_COMMIT, "keys": k,
            "rule": "a script builds this front from this target.json and that one versioned input (2.2's target.json at the commit named): no Markdown section is a source"}


LETTER_PLATE = {
    "T1": {"z": 678.0, "note": "T1: Photo, the plate sits 0.32 of the leaf up in a lock rail that runs 549 to 871 above the footway (520 to 843 above the leaf's foot); 2.2 had 545 in a lock rail 490 to 600"},
    "M1": {"z": 113.0, "note": "M1 (aluminium, glazed from 198): the plate is centred in the 170 high bottom rail (z 28 to 198), outside the glass; 2.2's 545 stood inside the glass (narrow point 7 of the review)"},
    "M2": {"z": 545.0, "note": "M2 (bronze, glazed from 600): the plate sits in the bronze kick panel (z 28 to 600), centred at 545 as 2.2, below the glass"},
}

BLINDS = {
    "ritas": "a closed lattice grille outside the glass at night (4.3 of TARGET.md); by day the lattice is lifted out and stored inside, and the 40 x 40 top rail (at the transom) and the bottom channel stay, powder black",
    "fish_market": "a retractable awning's arms and blind rail across the front at the transom, canvas stowed or absent (Photo, P1: two diagonal arms and a black rail at about z 2080, +-40; the arms and the 40 mm rail are Judgement); no grille",
    "tea_rooms": "a half-height cafe curtain on a brass rod at z 1500 above the footway over the two outer lights (2.2's glazing note; the research)",
    "newsagent": "the roller shutter of 2.2 (hood 300 x 210 deep, rails, 77 mm slats): up by day, down in the shut-up variant",
    "chandler": "woven galvanised mesh screens inside the lower lights when shut (Photo, P4): three panels, wire 2 mm, mesh 12 mm, z 0.70 to 1.55 above the crown",
    "empty_unit": "every pane whitewashed from inside (4.1)",
    "mickeys": "none", "steam_laundry": "none (its lit box sign and hanging box are 4.1's)", "grocer": "none", "ironmonger": "none",
}
BRAND_BLOCKLIST = ["dixons", "currys", "comet", "rumbelows",           # the review's retailers (Dixons was on cassette_player's map)
                   "titch banks", "titch co", "leitz", "wetzlar", "summilux", "lanstey", "polyluft", "polyclean", "kolo", "steelbox", "lorex", "avventura", "sirius",
                   "solidus", "sdq", "q-tech", "jnl", "micky", "polyplast", "urban quartz", "nova presents",      # makers and look-alikes read off the 1k maps (inventory.polyhaven[id].marks)
                   "casio", "sony", "braun", "zippo", "leica", "vtech", "kentucky", "snap-on", "stanley", "wd-40", "ph 40", "galler", "philips", "panasonic", "sanyo", "ncr",
                   "coca", "pepsi", "heinz", "kellogg", "lipton", "tesco", "woolworth", "w h smith", "wh smith", "marlboro", "benson", "silk cut", "embassy", "players", "rizla", "post office", "royal mail", "bt "]
CONTENT_BLOCKLIST = {"alcohol": ["beer", "lager", "wine", "whisky", "whiskey", "vodka", "gin ", "brandy", "cider", "ale ", "pub ", "off-licence", "off licence", "spirits", "champagne", "bottle bank"],
                     "gambling": ["las vegas", "pools", "coupon", "lottery", "bet ", "bets", "betting", "odds", "bookmaker", "scratchcard", "scratch card", "casino", "gamble", "jackpot", "bingo"],
                     "children": ["child", "children", "kid", "kids", "toy", "toys", "baby", "pram", "school", "boy ", "girl "],
                     "people": ["person", "man_", "woman", "figure", "mannequin", "human", "armature", "head_", "character"]}

DENIED = {
    "digital_wrist_watch": "a Casio-style face with the maker's mark; the digital watch is also a 1980s-90s object but the mark is a real brand: not used",
    "Television_01": "a maker's name ('VTECH' look-alike) on the bezel: television_02 is used instead",
    "Drill_01": "a cordless drill printed '18V 1.3Ah LITHIUM-ION': after 1992 (rule: nothing after 1992)",
    "classic_laptop": "a notebook computer: not in a 1990 British shop window and arguably after 1992",
    "gaming_console": "a games console of the 2010s: after 1992", "gamepad": "a modern pad: after 1992",
    "korean_public_payphone_01": "a Korean payphone: wrong country and carrier mark",
    "plastic_crate_01": "a drinks crate lettered 'GALLER ...': a brewer's or bottler's crate (alcohol rule) and a maker's mark",
    "wine_bottles_01": "alcohol", "wine_barrel_01": "alcohol", "wooden_barrels_01": "cellar barrels: alcohol connotation", "bar_chair_round_01": "a pub stool",
    "brass_goblets": "drinking vessels", "dartboard": "a pub game", "chess_set": "kept out of the pawnbroker's display only if the builder reads it as a gambling table; allowed in the room (a board game)",
    "Barrel_01": "a drum printed with an explosives sign (the 3 Oct chandler fault)", "barrel_03": "an oil drum, fine, but 0.63 m deep (no room in the display) and not needed",
    "russian_food_cans_01": "Cyrillic labels (wrong country)", "CheeseBox_01": "a crate stencilled RADIO: not what its name says",
    "lubricant_spray": "a look-alike of a real spray ('PH 40'): a real brand", "leather_cleaner_can": "a branded spray can ('RAY'S LEATHER')",
    "plastic_jerrycan": "a modern fuel can lettered 'The Old Man'", "multi_cleaner_bottle": "modern cleaner packaging with a printed logo: replaced by the label atlas",
    "all_purpose_cleaner": "modern pink cleaner bottle with a printed name ('Planis'): replaced by the label atlas", "bleach_bottle": "modern thick-bleach bottle with a printed name",
    "rubber_duck_toy": "a toy (children rule)", "baseball_01": "a toy", "american_football": "a toy", "football": "a toy", "dirty_football": "a toy", "baseball_bat": "a toy",
    "SchoolChair_01": "a school chair (the school stands closed; children rule)", "SchoolDesk_01": "a school desk (children rule)",
    "WoodenChair_01": "a Gothic carved chair (the 3 Oct tea-room fault)", "GothicBed_01": "gothic furniture", "GothicCabinet_01": "gothic furniture", "ArmChair_01": "a Gothic armchair",
    "service_pistol": "a firearm: not in a shop window", "antique_katana_01": "a weapon", "antique_estoc": "a weapon", "ornate_medieval_dagger": "a weapon", "ornate_medieval_mace": "a weapon",
    "fishermans_hat": "a boonie hat, not a sou'wester (GOODS note)", "stick_grenade": "a weapon", "kite_shield": "a weapon",
    "vintage_grandfather_clock_01": "0.8 m deep as modelled: stands too far off the wall (budget); dropped from Rita's room",
    "vintage_cabinet_01": "0.67 m deep: too far off the wall; dropped from Rita's room", "painted_wooden_cabinet": "not needed",
    "camera_security_01": "CCTV is rare in 1990 (canon)", "security_camera_01": "CCTV is rare in 1990 (canon)", "security_camera_02": "CCTV is rare in 1990 (canon)",
    "gaming": "n/a", "vintage_radio_transceiver": "a military transceiver: not period stock for this window",
}

# every id the shops use that is NOT in a shop's goods/display but is named as a surface or fallback
SURFACES = {
    "polyhaven_textures": ["old_linoleum_flooring_01", "linoleum_brown", "painted_plaster_wall", "dirty_carpet", "long_white_tiles", "square_tiles", "terracotta_floor_tiles",
                           "marble_01", "marble_tiles", "rubber_tiles", "worn_tile_floor", "old_wooden_floor_02", "old_wooden_floor_03", "white_plaster_02", "ceiling_interior",
                           "terrazzo_tiles", "concrete_floor_painted"],
    "ambientcg": ["Ice001", "Ice002", "Marble012", "Rope001", "Rope002", "Candy001", "Candy002", "Fabric020", "Fabric021", "Fabric028", "Fabric029", "Cardboard002", "Wicker010B",
                  "Terrazzo004", "Tiles032", "Tiles040", "SurfaceImperfections001", "Smear001", "Fingerprints001", "Scratches001", "Leaking001", "Metal042A"],
}


def get_json(url, tries=3):
    for k in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5)
    raise last


def collect_ids():
    ids = set()
    for sid, sh in SH.SHOPS.items():
        for g in sh.get("goods", []):
            if not g["model"].startswith("script:"):
                ids.add(g["model"])
        d = sh.get("display")
        if d:
            for it in d["items"]:
                if not it["model"].startswith("script:"):
                    ids.add(it["model"])
    return sorted(ids)


def polyhaven_checked(refresh):
    if os.path.exists(PHCACHE) and not refresh:
        return json.load(open(PHCACHE))
    cat = get_json("https://api.polyhaven.com/assets?t=models")
    out = {"read": DATE, "catalogue_url": "https://api.polyhaven.com/assets?t=models", "catalogue_count": len(cat), "licence": "CC0 (https://polyhaven.com/license)", "models": {}}
    for i in collect_ids():
        if i not in cat:
            out["models"][i] = {"exists": False}
            continue
        v = cat[i]
        rec = {"exists": True, "name": v["name"], "dims_cm": [round(x / 10.0, 1) for x in v["dimensions"]], "polycount": v["polycount"], "categories": v["categories"],
               "tags": v["tags"][:8], "published": time.strftime("%Y-%m-%d", time.gmtime(v["date_published"])), "authors": list(v["authors"].keys())}
        try:
            f = get_json("https://api.polyhaven.com/files/" + i)
            g = (f.get("gltf") or {}).get("1k", {}).get("gltf", {})
            rec["gltf_1k"] = {"url": g.get("url"), "bytes": g.get("size"), "textures": len(g.get("include") or {})}
        except Exception as e:  # noqa: BLE001
            rec["gltf_1k"] = {"error": str(e)[:80]}
        out["models"][i] = rec
        time.sleep(0.2)
    json.dump(out, open(PHCACHE, "w"), indent=1)
    return out


# ------------------------------------------------------------------------------------------------------------------------------------
def srgb_luma_to_lin(l255):
    c = l255 / 255.0
    return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92


def lin_to_srgb255(x):
    return 255 * (12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055)


def build():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    scene = S.load_scene()
    t22 = json.load(open(P22))
    t41 = json.load(open(P41))
    spec = json.load(open(SPEC))
    cast = json.load(open(CAST))
    look = json.load(open(LOOK))
    pieces = json.load(open(PIECES))
    ph = polyhaven_checked(a.refresh)
    lit_names = pieces["window_practicals"]["lit_names"]
    s22 = {s["id"]: s for s in t22["shops"]}
    s41 = {s["id"]: s for s in t41["shops"]}
    glass_rows = {}
    for g in t41["glass_lettering"]:
        glass_rows.setdefault(g["shop"], []).append(g["text"])
    hang = {p["shop"]: p for p in t41["projecting_signs"]}

    shops_out = []
    spec_entries = []
    order = ["mickeys", "fish_market", "ritas", "empty_unit", "steam_laundry", "grocer", "chandler", "tea_rooms", "ironmonger", "newsagent"]
    for sid in order:
        f = s22[sid]
        fas = s41[sid]
        sh = SH.SHOPS[sid]
        card = S.card_of(scene, f["block"], f["bay"])
        side = card["side"]
        wc = f["centres_street_x_m"]["window"]
        D = sh.get("room_D")
        card_out = {"x0": card["x0"], "x1": card["x1"], "bottom": card["bottom"], "top": card["top"], "z": card["z"],
                    "rule": "terrace-front.py 2405-2417: x from bay start + 0.35 to bay end - 0.35, z 0.65 to 3.05, y %+.3f; the empty unit has none (bay 3 of 6 is skipped)" % card["z"]}
        gl0, lay0 = f["glazing"], f["glazing_layout"]
        wv = gl0["window_frame"]
        per = PER_LIGHT[sid]
        n_lights = len(lay0["mullion_centres"]) + 1
        tl = S.toplight_layout(f["window_length"], lay0["jamb_face"], lay0["mullion_centres"], lay0["mullion_face"], per, S.BAR_FACE[wv])
        glz = dict(gl0)
        glz["pattern"] = "%dL-%dT" % (n_lights, tl["toplights"]) + ("-aligned" if per == 1 else "") + ("-sunrise" if sid == "grocer" else "")
        glz["toplights"] = tl["toplights"]
        glz["toplight_aligned"] = True
        glz["from_2_2"] = {"pattern": gl0["pattern"], "toplights": gl0["toplights"], "toplight_aligned": gl0["toplight_aligned"],
                           "why_changed": "3.2 street review fault 1 and kit departure D6: each mullion is carried up through the toplight row as a bar of its own width and each light's toplight is split equally by bars; "
                                          "2.2's unaligned table (bars on a fixed pitch, slivers beside the mullions) is replaced on every front"}
        if sid == "grocer":
            glz["glazing"] = ("plate glass in bronze-plated bars; each light's toplights are etched with one sunrise of 5 rays, across its two toplights (the 28 bar hides 28 mm of the middle ray): "
                              "Judgement, because 2.2's '5 toplights of a sunrise' cannot stay with aligned bars")
        if sid == "steam_laundry":
            glz["glazing"] = ("gasket, snap-in bead, 6 mm plate; the mullion is carried up: two toplights of 1600, one over each light (P5, the type photograph, shows the upper lights divided on the lower lights' lines; "
                              "2.2 had one long pane: disagreement D11)")
        lay = dict(lay0)
        lay.update({"lights": tl["lights"], "toplights_per_light": per, "toplight_bar_face": S.BAR_FACE[wv], "toplight_bars": tl["toplight_bars"],
                    "toplight_bar_centres": [b["centre"] for b in tl["toplight_bars"] if b["kind"] == "toplight_bar"],
                    "toplight_panes": tl["toplight_panes"], "toplight_width": tl["toplight_width"], "toplights": tl["toplights"], "mullion_carried_up": True,
                    "rule": "u from the window frame's left edge (mm). toplight_bar_centres are the %g mm bars BETWEEN a light's toplights; every mullion line also carries a bar of the mullion's own face "
                            "(toplight_bars lists both, kind mullion_carried_up and toplight_bar); each light's toplight is split equally; no toplight is narrower than 250" % S.BAR_FACE[wv],
                    "from_2_2": {"toplight_bar_centres": lay0["toplight_bar_centres"], "toplight_width": lay0["toplight_width"], "toplights": lay0["toplights"]}})
        front = {
            "bay_mm": 6000, "pilaster_slot_mm": 350, "opening_mm": 5300, "zones_u_mm": f["zones_u"], "window_length_mm": f["window_length"],
            "door_end_viewer": f["door_end_viewer"], "door_end_street": f["door_end_street"], "centres_street_x_m": f["centres_street_x_m"],
            "variants": {"pilaster": f["pilaster"], "console": f["console"], "cornice": f["cornice"], "stallriser": f["stallriser"]["variant"],
                         "window_frame": f["glazing"]["window_frame"], "shop_door": f["shop_door"], "side_door": f["side_door_variant"]},
            "glazing": glz, "glazing_layout": lay, "lobby": f["lobby"], "paints": f["paints"], "paint_srgb": f.get("paint_srgb"), "paint_names": f.get("paint_names"),
            "alterations": f["alterations"], "console_absent_viewer": f.get("console_absent_viewer"),
            "built_by_3_2": {"pilaster": f["pilaster"] in KIT_BUILT["pilaster"], "console": f["console"] in KIT_BUILT["console"], "cornice": True,
                             "stallriser": (f["stallriser"]["variant"] == "panel" and f["stallriser"].get("panels") == 3), "window_frame": (wv == "T1" and n_lights == 3 and per == 3 and f["window_length"] == 3350.0),
                             "shop_door": False, "side_door_F1": True, "lobby": f["lobby"]["kind"] == "flush"},
        }
        front["toplights_as_built"] = tl["toplights"]
        front["build_from"] = build_from(f)
        front["missing_from_3_2"] = [k for k, v in front["built_by_3_2"].items() if not v and not (k == "lobby" and f["lobby"]["kind"] == "flush")]
        # the assembly order: bottom to top, left (viewer's) to right, as the builder places them
        order_parts = ["pilaster (two, mirrored; plinth 600, shaft 290 x 140 proud)", "stallriser (%s, z 0 to 600, window zone)" % f["stallriser"]["variant"], "sill (75 thick, nose 150, window zone)",
                       "window_frame (%s %s, %.0f mm long, z 600 to 2850)" % (wv, glz["pattern"] + ((" (3.2 kit departure D6; the 2.2 table said %s)" % gl0["pattern"]) if gl0["pattern"] != glz["pattern"] else ""), f["window_length"]),
                       "shop door (%s, slot 1006, hinge on the %s)" % (f["shop_door"], {"L": "viewer's left", "R": "viewer's right"}[f["shop_door_hinge_viewer"]]),
                       ("side door F1 from 3.1 (slot 944, hinge on the %s)" % {"L": "viewer's left", "R": "viewer's right"}[f["side_door_hinge_viewer"]]) if f["side_door"] else "no side door (the flat is reached from the rear yard)",
                       "the band above the doors: transom (z 2400 to 2480) across the door slots, the fanlight under it, three toplights over the shop door, %s, the head (z 2790 to 2850): `door.fanlight`, `.transom`, `.toplights_over_shop_door`, `.panel_over_side_door`, `.head`" % ("a raised-and-fielded panel over the side door" if f["side_door"] else "no side door, so no panel"),
                       "console (%s, two; %s)" % (f["console"], ("the %s one is absent" % {"L": "viewer's left", "R": "viewer's right"}[f["console_absent_viewer"]]) if f.get("console_absent_viewer") else "both present"),
                       "fascia_board (5410 x 550 x 120 proud, bed mould 40) carrying the 4.1 board %s_basecolour/height/orm/wear.png" % sid,
                       "cornice (5892 x 150 x 215 deep, broken forward 85 over each console; 12 Oct ruling: 150 mm as built)"]
        if sid == "mickeys":
            order_parts.append("raised gilt letters MICKEY'S (geometry from the 4.1 manifest: cap 330, 14 off the board)")
        if f.get("fascia_sign"):
            order_parts.append("fascia sign %s: u %s, z %s, %s deep (4.1 geometry)" % (f["fascia_sign"]["kind"], f["fascia_sign"]["u"], f["fascia_sign"]["z"], f["fascia_sign"]["depth"]))
        front["assembly_order"] = order_parts
        door = {
            "variant": f["shop_door"], "slot_mm": 1006, "leaf_mm": [900, 2040], "hinge_viewer": f["shop_door_hinge_viewer"], "lever_viewer": f["shop_door_lever_viewer"],
            "paint": f["paints"]["shop_door"],
            "from": "%s at commit %s: parts.shop_door (dims, furniture, handing, variants T1 / M1 / M2 and its profiles), parts.side_door_slot, parts.window_frame (the transom, head and toplight bars) and, for the lobby fronts, parts.lobby: "
                    "numbers read from that JSON, not from its Markdown; this target changes and adds what the photographs show (D1, D12) and puts the band above the doors in (`fanlight`, `transom`, `toplights_over_shop_door`, `panel_over_side_door`, `head`)" % (P22_FILE, P22_COMMIT),
            "glass_foot_z_mm": 871.0 if f["shop_door"] == "T1" else f["shop_door_glass_foot_z"],
            "glass_foot_note": ("T1: 871 +-30 above the footway (843 above the leaf's foot) by Photo (Geograph 2192169, a fish shop's unaltered timber front, read 12 Oct: glass foot 0.413 of the leaf), SUPERSEDING 2.2's 600 (Leadenhall 2019, a heritage restoration); see disagreement D1"
                                if f["shop_door"] == "T1" else "as 2.2 (aluminium and bronze doors are glass from the bottom rail)"),
            "letter_plate": {"size_mm": [250, 40], "z_mm": LETTER_PLATE[f["shop_door"]]["z"], "centre": True, "note": LETTER_PLATE[f["shop_door"]]["note"], "outside_glass": True},
            "glass_z_mm": {"T1": [871.0, 1973.0], "M1": [198.0, 1968.0], "M2": [600.0, 1968.0]}[f["shop_door"]],
            "t1_rails_mm": ({"bottom_rail": [28, 228], "lower_panel_field": [241, 549], "lock_rail": [549, 871], "glass": [871, 1973], "glazing_bar": {"z": 1423, "width": 28, "note": "one horizontal bar dividing the glass into two panes of about 540 (Photo)"}, "top_rail": [1973, 2068], "kind": "Photo, heights above the footway (the leaf stands at 28), scale from the leaf height 2040 (one dimension), error +-30"} if f["shop_door"] == "T1" else None),
            "threshold": "terrazzo 25 high at the leaf falling to 12, nose out to d 130 (flush) or at the lobby's floor level (recessed): 2.2 section 10",
            "furniture": {"T1": "brass lever on a 240 x 40 backplate at 1000, rim latch and escutcheon at 950, brass kick plate 770 x 170, three 100 x 75 butts",
                          "M1": "chrome D pull 300, push plate, floor spring, rubber tape at the foot", "M2": "bronze D pull, bronze kick panel to 600"}[f["shop_door"]],
            "bell": {"kind": "a spring-arm shop bell: a 20 x 3 mm steel strip curved 220 long fixed to the INSIDE face of the leaf's top rail 90 from the hanging stile at z 1950 to 2050, carrying a 70 mm brass bell hung 80 below it; it rings on the door's swing against a fixed clapper on the frame",
                     "kind_of_number": "Judgement: no 1975 to 1995 photograph of a shop-door bell was reached; the part is seen through the door's glass from the street and from the close view",
                     "size_mm": {"strip": [220, 20, 3], "bell_diameter": 70, "drop": 80}, "material": "steel (60, 60, 62) rough 0.5 metal 0.7; brass (160, 120, 55) rough 0.38 metal 1.0"},
            "sign": "the plastic OPEN / CLOSED sign from 4.2 (the paper unit) on the inside of the door's glass at z 1500, hung by a suction cup: closed when the shop is shut; the hours plate (4.1) on the glass beside it",
        }
        door.update(S.band_above_doors(f["zones_u"], f["door_end_viewer"], wv, f["shop_door"], f["paint_srgb"]["window_frame"], f["paint_srgb"]["shop_door"],
                                       newsagent_hood=("roller_shutter" in f["alterations"]), recessed=(f["lobby"]["kind"] != "flush")))
        door["fanlight"]["street_number"] = {
            "text": fas.get("street_number"), "cap_mm": 110, "x_street_m": f["centres_street_x_m"]["shop_door"], "baseline_z_above_footway_mm": 2200.0,
            "from_4_1": "glass_lettering, surface 'side-door fanlight', z_m 2.18, x_street_m %s (the side door's centre)" % next((g["x_street_m"] for g in t41["glass_lettering"] if g["shop"] == sid and "fanlight" in g["surface"]), None),
            "frame_of_z": ("4.1's z 2.18 is in the street frame, metres above the road crown: 2.18 above the crown is 2080 above the footway (crown + 0.10 = footway), which is BELOW this fanlight (z 2131 to 2400 above the footway). "
                           "The number is therefore set in the fanlight: baseline 2200 above the footway, cap 110 (2200 to 2310, centred in the pane) = 2.30 above the crown: Judgement, 0.12 m above 4.1's z"),
            "where": ("on the SHOP door's fanlight, as the review reads it, at the shop door's centre (street x %s), not at 4.1's x (the side door's centre): a move of 4.1's x recorded for its owner; "
                      "the side door's fanlight carries no number here" % f["centres_street_x_m"]["shop_door"])}
        glass = {"panes": "single 6 mm plate per light, no astragal bars; lights = n_mullions + 1 over the lower row; toplights as the glazing layout (glazing_layout.toplight_panes); the door glazed in two panes with the bar at 1423 (T1: Photo, D1) or one pane (M1, M2)",
                 "lights": f["glazing"]["n_mullions"] + 1, "toplights": tl["toplights"], "thickness_mm": 6, "d_mm": 30, "glass_y_street_m": [S.GLASS_Y_FRONT, S.GLASS_Y_BACK],
                 "reflectance": "the game's (M_LedgerGlass, thin translucent; night 0.2 of day: look file): not set here", "lettering": glass_rows.get(sid, [])}
        fascia = {"board": "fascias/%s/%s_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm)" % (fas["id"], fas["id"]) + (", _emissive.png" if fas.get("lit") else ""),
                  "made_by": "python production/cloud-week/2d/fascias/make_fascias.py OUTDIR --seed-base 1", "street_number": fas.get("street_number"),
                  "name_blocks": [(b.get("role"), b.get("text")) for b in fas["blocks"] if b.get("text") and b.get("role") in ("name", "trade", "end")],
                  "hanging_sign": ({"id": hang[sid]["id"], "kind": hang[sid]["kind"], "mount": hang[sid]["mount"]} if sid in hang else None),
                  "construction": fas.get("construction_kind"), "lit": fas.get("lit")}
        night_note = (sh.get("display") or {}).get("night") if sh.get("display") else None
        if sid == "empty_unit":
            night_note = "dark; the whitewash tile (glass/empty_unit/window_whitewash, 3250 x 1800 mm) over every pane and the door's glass; no grille"
        owner = OWNER.get(sid)
        lit = sid not in ("fish_market", "empty_unit", "steam_laundry", "ironmonger") and sid != "mickeys"
        e = {
            "blinds_grilles_shutters": BLINDS.get(sid, "none"),
            "id": sid, "spec_id": sh["spec_id"], "trade": f["trade"], "owner": owner, "block": f["block"], "bay": f["bay"], "side": f["side"], "street_x_m": f["street_x_m"],
            "street_number": fas.get("street_number"), "needs_room": sh["needs_room"], "room_is_real_already": bool(sh.get("room_real")),
            "lit_at_night": sh["lit_at_night"], "lit_why": sh["lit_why"], "hours": sh["hours"], "hours_source": sh["hours_source"],
            "front": front, "door": door, "glass": glass, "fascia": fascia, "night_furniture": night_note, "card": None if sid == "empty_unit" else card_out,
            "keeps": sh["keeps"], "changes": sh["changes"], "notes": f.get("notes"),
        }
        if sid == "newsagent":
            e["conflict"] = HAL_NOTE
        if sh["needs_room"]:
            lights = dict(sh["lights"])
            lights["night_dark_wash_linear_rgb"] = look["lantern_linear_rgb"]
            lights["night_dark_wash_source"] = "production/specs/unreal-look.json lantern_linear_rgb: the game's scene colour for sodium (the scene file's (1, 0.7055, 0) is stale: QUEUE.md 9 Oct 12:10)"
            fixtures_out = []
            for fxx in sh["fixtures"]:
                fxx = dict(fxx)
                if fxx["id"].endswith("-ceiling-tubes"):
                    fxx["x"], fxx["y"], fxx["z"] = S.tube_box(lights)       # the battens' own box, from lights.tubes
                fixtures_out.append(fxx)
            room = {"w": S.W, "h": S.H, "d": D, "camera_d": S.CAMERA_D, "floor": sh["floor"], "walls": sh["walls"], "ceiling": sh["ceiling"], "box_floor_above_crown": S.CARD_BOTTOM,
                    "box_ceiling_above_crown": S.CARD_TOP, "frame": "room frame of sw_shops.py (x 0 at the card's centre, +x the picture's right; y back; z up from the box floor)",
                    "fixtures": fixtures_out, "goods": sh["goods"], "lights": lights}
            e["room"] = room
            e["display"] = sh["display"]
            e["pictures"] = {"pixels": [4096, int(round(4096 * S.H / S.W))], "states": {"day": "%s_day.png" % sh["spec_id"], "night_lit": "%s_night_lit.png" % sh["spec_id"], "night_dark": "%s_night_dark.png" % sh["spec_id"]},
                             "json_beside": "%s.json" % sh["spec_id"], "folder": "production/art/shop-rooms/ (masters on F:/LedgerTools/shop-rooms; 2048-wide copies in git as for the pawnbroker)",
                             "json_fields": {"shop": sh["spec_id"], "w": S.W, "h": S.H, "d": D, "camera_d": S.CAMERA_D, "pixels": [4096, int(round(4096 * S.H / S.W))],
                                             "states": {"day": "%s_day.png" % sh["spec_id"], "night_lit": "%s_night_lit.png" % sh["spec_id"], "night_dark": "%s_night_dark.png" % sh["spec_id"]},
                                             "made_by": "tools/art-recipes/shop-room.py", "samples": 128},
                             "brightness": {"day": 0.15, "night": 0.7, "note": "the game's (shop-interiors.json: day 0.15, night 0.7): kept for every shop"},
                             "mean_luma_target": lights["mean_luma_target"], "composite_luma_floor": {"day": 33, "night_lit": 45, "night_dark_min": 10, "night_dark_max": 35}}
            if sh["spec_id"] != "mickeys":
                disp = sh["display"]
                u0 = f["zones_u"]["window"][0]
                spec_entries.append({
                    "id": sh["spec_id"], "block": f["block"], "bay": f["bay"], "trade": f["trade"] + ", per production/cloud-week/targets/shop-windows/TARGET.md", "room": {"w": S.W, "h": S.H, "d": D},
                    "card": {"x0": card["x0"], "x1": card["x1"], "bottom": card["bottom"], "top": card["top"], "z": card["z"]}, "decal": "production/art/shop-rooms/%s_day" % sh["spec_id"], "decal_in_the_spec_today": next((x_.get("decal") for x_ in spec["shops"] if x_["id"] == sh["spec_id"]), None),
                    "pictures": "production/art/shop-rooms/%s" % sh["spec_id"], "side": side, "camera_d": S.CAMERA_D, "pixels_wide": 4096, "lit_at_night": sh["lit_at_night"],
                    "brightness_day": 0.15, "brightness_night": 0.7, "spill_lumens": 350 if sh["lit_at_night"] else 0,
                    "display": {"glb": "%s-display" % sh["spec_id"], "x0": None, "x1": None, "front": round(side * S.DISPLAY_FRONT_FROM_GLASS + side * S.GLASS_Y_BACK, 3),
                                "bed": S.BED_Z, "depth": S.DISPLAY_DEPTH,
                                "measured": "window zone u %.0f to %.0f of the bay (2.2), glass y %.3f to %.3f, stallriser top 0.70 above the crown" % (f["zones_u"]["window"][0], f["zones_u"]["window"][1], S.GLASS_Y_FRONT, S.GLASS_Y_BACK)},
                    "sources": "production/cloud-week/targets/shop-windows/TARGET.md"})
                # street x of the display's ends from the window zone (east parade: x = bay high end - u/1000; west: bay low end + u/1000)
                lo, hi = f["street_x_m"]
                ux0, ux1 = f["zones_u"]["window"]
                xs = [(hi - ux0 / 1000.0 if side > 0 else lo + ux0 / 1000.0), (hi - ux1 / 1000.0 if side > 0 else lo + ux1 / 1000.0)]
                spec_entries[-1]["display"]["x0"], spec_entries[-1]["display"]["x1"] = round(min(xs), 3), round(max(xs), 3)
        e["cameras"] = {}
        if sh["needs_room"] or sid in ("mickeys", "empty_unit"):
            for cname in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
                eye, aim = S.camera_pose(cname, card, wc)
                e["cameras"][cname] = {"eye_street_m": [round(float(v), 3) for v in eye], "aim_street_m": [round(float(v), 3) for v in aim]}
        shops_out.append(e)

    # ---- method numbers, computed from the game's rule -----------------------------------------------------------------------------
    tab20 = S.standoff_table(4.5, 20)
    tab40 = S.standoff_table(4.5, 40)

    def pick(tab, keys):
        return round(min(tab[k]["budget_m"] for k in keys), 3)
    budget = {"reads_true_20px": {"back_wall": pick(tab20, ["back wall, left third", "back wall, middle", "back wall, right third"]), "back_wall_middle": pick(tab20, ["back wall, middle"]),
                                   "side_walls": pick(tab20, [k for k in tab20 if "wall," in k and "back" not in k]), "floor_and_ceiling": pick(tab20, ["floor, near", "floor, middle", "floor, far"])},
              "tolerated_40px": {"back_wall": pick(tab40, ["back wall, left third", "back wall, middle", "back wall, right third"]),
                                 "side_walls": pick(tab40, [k for k in tab40 if "wall," in k and "back" not in k]), "floor_and_ceiling": pick(tab40, ["floor, near", "floor, middle", "floor, far"])},
              "method": "sw_common.standoff_table: an object painted on a surface at stand-off s slides from its true place by the angle between the eye's rays to the object and to the point where the "
                        "render camera's ray through it meets the surface; the budget is the greatest s that keeps the slide within N pixels of a 2560 x 1440 frame, the smallest over STREET_SQUARE, "
                        "STREET_30 and CLOSE_35 and their mirror images",
              "tables": {"20px": tab20, "40px": tab40}}
    # the integer rules the target writes (rounded down to 5 mm): back wall shelving and goods; counters at the back wall; side walls; floor and ceiling
    rules = {"shelf_goods_on_back_wall_m": 0.30, "furniture_at_back_wall_m": 0.60, "side_wall_relief_m": 0.10, "side_wall_flat_m": 0.05, "floor_and_ceiling_m": 0.025, "floor_ceiling_tolerated_m": 0.05}
    rules["shelf_named_exceptions"] = [{"fixture": "R-back-tv-tiers", "depth_m": 0.35,
                                        "limit": "at most the 20 px budget at the card's middle: method.standoff_budget.reads_true_20px.back_wall_middle (sw_common's measure, %.3f) and at most 0.36 (the review's independent measure of 12 October)" % budget["reads_true_20px"]["back_wall_middle"],
                                        "why": "television_02 is 0.35 deep at its size; the two tiers above the counter carry them (mid height), where 0.35 stays under 20 px; every other back-wall shelf unit is 0.30 or less"}]
    rules["derivation"] = ("true (20 px): back wall %.2f, sides %.2f, floor/ceiling %.2f; tolerated (40 px): back wall %.2f, sides %.2f, floor/ceiling %.2f; the rules are those figures rounded down to 5 mm and "
                           "to the nearest builder-friendly depth: a shelf (0.30) is true, a counter or machine against the back wall (0.60) is tolerated, a side wall carries only boards and 0.10 "
                           "racks, the floor only flat things" % (budget["reads_true_20px"]["back_wall"], budget["reads_true_20px"]["side_walls"], budget["reads_true_20px"]["floor_and_ceiling"],
                                                                 budget["tolerated_40px"]["back_wall"], budget["tolerated_40px"]["side_walls"], budget["tolerated_40px"]["floor_and_ceiling"]))
    # honest range: resolution, the window's far end angle, slide of the standard objects at the review cameras
    texel = {}
    for pw in (2048, 4096):
        for g in (0.5, 1.0, 1.5, 1.9):
            texel["%d px wide, %.1f m from the glass, 35 deg" % (pw, g)] = S.texel_stats(g, 35.0, pw, 4.5)
    far_end = {}
    for g in (0.5, 1.0, 1.5, 1.9):
        lat = g * math.tan(math.radians(35))
        far_end["%.1f m" % g] = round(math.degrees(math.atan2(1.675 + lat, g)), 1)
    card = S.card_of(scene, "east_parade", 2)
    slide = {}
    cx = (card["x0"] + card["x1"]) / 2.0
    for cname in ("STREET_SQUARE", "STREET_30", "CLOSE_35"):
        eye, _ = S.camera_pose(cname, card, 17.025)
        ep = S.eye_in_picture(eye, card)
        vf = S.CAMERAS[cname]["vfov_deg"]
        rows = {}
        for lab, obj, pl in (("shelf goods 0.25 off the back wall (middle)", (2.65, 4.25, 1.2), ("back", 4.5)), ("counter 0.60 against the back wall (middle)", (2.65, 3.9, 0.9), ("back", 4.5)),
                             ("a free item 1.5 off the back wall", (2.65, 3.0, 0.9), ("back", 4.5)), ("a unit 0.30 off the right wall, mid depth", (5.0, 2.2, 1.2), ("right", 5.3)),
                             ("a board 0.05 off the right wall", (5.25, 2.2, 1.2), ("right", 5.3)), ("a floor item 0.03 high, mid", (2.65, 2.2, 0.03), ("floor", 0.0))):
            rows[lab] = round(S.slide_px(ep, obj, pl, 4.5, vf), 1)
        slide[cname] = rows
    honest = {"resolution": {"what": "screen pixels per picture texel over the glass area at the game's 1440 lines (more than 2 is soft)", "table": texel,
                              "reading": "at 4096 wide the picture is never softer than 1.2 screen pixels a texel from 0.5 m; at 2048 it is soft over 13 per cent of the glass at 0.5 m and 4 per cent at 1.5 m: the picture is made 4096 wide"},
              "window_far_end_angle_deg": {"table": far_end, "reading": "the angle off the glass normal at which the window's far end is seen from a pavement point 35 degrees off the window centre: at 1.5 m it is %.0f degrees, where the research puts the glass's own Fresnel hand-over (about 60); nearer than 1.5 m part of the window is in the hand-over and the review would judge the glass, which is the game's, not the room" % far_end["1.5 m"]},
              "slide_px_at_2560x1440": {"table": slide, "reading": "the same object slides by about the same number of pixels from 0.5 to 1.9 m (the angle sets it, not the distance): the 20 px line is held by back-wall shelf goods and flat boards at the CLOSE camera, a counter against the back wall is tolerated, a free item or a deep side unit is not"},
              "nearest_honest_close_distance_m": 1.5,
              "why": ("the method holds from the far pavement (8.75 m) and from the near pavement down to 1.5 m from the glass at 35 degrees, with 4096-wide pictures and the stand-off rules: there the room's surfaces "
                      "are sharp (median %.2f screen pixel a texel at 4096), back-wall stock 0.25 deep slides %.0f to %.0f px, a 0.05 board %.0f to %.0f px, a floor item 0.03 high %.0f to %.0f px (so the floor's rule is 0.025), "
                      "and the whole window is seen at under 62 degrees. Nearer than 1.5 m the window's far end passes 62 degrees (%.0f at 1.0 m, %.0f at 0.5 m), where the glass's own Fresnel takes over, so part of every nearer view is "
                      "the glass's and the display's, not the room's. The near 0.55 m is therefore real geometry, and the review's CLOSE view stands at 1.5 m." % (
                          texel["4096 px wide, 1.5 m from the glass, 35 deg"]["median"],
                          min(slide[c]["shelf goods 0.25 off the back wall (middle)"] for c in slide), max(slide[c]["shelf goods 0.25 off the back wall (middle)"] for c in slide),
                          min(slide[c]["a board 0.05 off the right wall"] for c in slide), max(slide[c]["a board 0.05 off the right wall"] for c in slide),
                          min(slide[c]["a floor item 0.03 high, mid"] for c in slide), max(slide[c]["a floor item 0.03 high, mid"] for c in slide), far_end["1.0 m"], far_end["0.5 m"]))}

    # ---- the inventory ---------------------------------------------------------------------------------------------------------------
    allowed = {}
    for i in collect_ids():
        r = ph["models"].get(i, {"exists": False})
        shops_using = [sid for sid, sh in SH.SHOPS.items() if any(g["model"] == i for g in sh.get("goods", [])) or any(it["model"] == i for it in (sh.get("display") or {}).get("items", []))]
        allowed[i] = {"exists": r.get("exists"), "dims_cm": r.get("dims_cm"), "polycount": r.get("polycount"), "published": r.get("published"), "page": "https://polyhaven.com/a/" + i,
                      "gltf_1k_bytes": (r.get("gltf_1k") or {}).get("bytes"), "shops": shops_using, "licence": "CC0"}
    scripted = {}
    for sid, sh in SH.SHOPS.items():
        for g in sh.get("goods", []):
            if g["model"].startswith("script:"):
                scripted.setdefault(g["model"], {"why": g.get("why"), "shops": []})["shops"].append(sid)
        for it in (sh.get("display") or {}).get("items", []):
            if it["model"].startswith("script:"):
                scripted.setdefault(it["model"], {"why": it.get("why"), "shops": []})["shops"].append(sid)
    for k, v in scripted.items():
        v["shops"] = sorted(set(v["shops"]))

    sk = json.load(open(os.path.join(HERE, "sketchfab_checked.json"))) if os.path.exists(os.path.join(HERE, "sketchfab_checked.json")) else {}
    amb = json.load(open(os.path.join(HERE, "ambientcg_checked.json"))) if os.path.exists(os.path.join(HERE, "ambientcg_checked.json")) else {}
    t = {
        "schema": "ledger-shop-windows-target/1",
        "family": "shop-windows",
        "summary_line": "",
        "status": "target for unit 7 of cloud week 42, part 2; written 12 October 2026 by the target writer; its fresh review (TARGET-REVIEW.md) failed it with 3 faults and 15 narrow points, every exact amendment is applied: FIXES APPLIED, NOT RE-REVIEWED (Jafar's 11 October rule: no more polishing of targets); nothing built, nothing committed",
        "units": {"length": "metres (frames: street, card, picture, room, display: see TARGET.md section 3); front parts in millimetres in the 2.2 bay frame (u, d, z)", "colour": "sRGB 0 to 255",
                  "luma": "Rec. 709 weights on the 8-bit sRGB values"},
        "street": {"ten_units_as_built": True, "twelve_not_found": True,
                   "what_is_found": "east_parade bays 0 to 5 (x 3 to 39, 6 m each), east_chandler bay 0 (x 40 to 46), west_north bays 0 to 2 counted from the high-x end (x 36 to 42, 30 to 36, 24 to 30). "
                                    "'Twelve' is the old atlas proposal (production/specs/terrace-fronts.md:290-322, superseded) and the words 'the other eleven' in RULINGS 2 Oct; canon.md names no count; DECISIONS 3 Oct lists ten.",
                   "needs_room": [s["id"] for s in shops_out if s["needs_room"]], "no_room": ["empty_unit (whitewashed; bay 3 has no card)", "mickeys (a real walked room already)"], "hal_conflict": HAL_NOTE},
        "shops": shops_out,
        "method": {
            "game_rule": {"file": "tools/ue/make_interior_material.py", "function": "trace(p, c, size, camd, side)", "camera_rule": spec["camera"],
                          "card": {"w": S.W, "h": S.H, "bottom_above_crown": S.CARD_BOTTOM, "top_above_crown": S.CARD_TOP, "y": S.CARD_Y, "glass_y": [S.GLASS_Y_FRONT, S.GLASS_Y_BACK], "gap_glass_to_card_m": round(S.GLASS_TO_CARD, 3)},
                          "camera_d": S.CAMERA_D, "never": spec["never"], "states": spec["states"],
                          "picture_orientation": "u from the viewer's left: on an east card the picture's left is the card's HIGH street x; on a west card its LOW x (make_interior_material.py selftest checks it)"},
            "floor_and_back_wall": {"box_floor": "the card's bottom edge, 0.65 above the crown: the picture's floor is the window bed carried back, 0.55 above the shop's real floor (which is hidden behind the stallriser from the street)",
                                    "back_wall_in_picture": {"u": [round(0.5 - 0.5 * S.CAMERA_D / (S.CAMERA_D + 4.5), 4), round(0.5 + 0.5 * S.CAMERA_D / (S.CAMERA_D + 4.5), 4)],
                                                             "v_up": [round(0.5 - 0.5 * S.CAMERA_D / (S.CAMERA_D + 4.5), 4), round(0.5 + 0.5 * S.CAMERA_D / (S.CAMERA_D + 4.5), 4)], "for_D": 4.5,
                                                             "px_4096": [[round((0.5 - 0.5 * S.CAMERA_D / (S.CAMERA_D + 4.5)) * 4096), round((1 - (0.5 + 0.5 * S.CAMERA_D / (S.CAMERA_D + 4.5))) * 1855)],
                                                                         [round((0.5 + 0.5 * S.CAMERA_D / (S.CAMERA_D + 4.5)) * 4096), round((1 - (0.5 - 0.5 * S.CAMERA_D / (S.CAMERA_D + 4.5))) * 1855)]]}},
            "standoff_budget": budget, "standoff_rules_m": rules, "honest_range": honest,
        },
        "cameras": {"definitions": S.CAMERAS, "eye_height": {"above_footway_m": S.EYE_ABOVE_FOOTWAY, "above_crown_m": S.EYE_Z}, "far_pavement_y_m": S.PAVEMENT_FAR_Y,
                    "rule": "STREET_*: on the OPPOSITE pavement, 8.76 m from the glass (the far pavement's kerb edge: the brief's 'about 8 m' is the nearest the far pavement allows); lateral offset toward low street x; "
                            "CLOSE_*: on the shop's own pavement 1.5 m from the glass; aimed at the window centre; 2560 x 1440; night views use night_lit for the lit shops and night_dark for the dark ones",
                    "which_to_render": {"each_shop": ["STREET_SQUARE", "STREET_30", "CLOSE_35"], "states": ["day", "night"], "parallax_pair": ["CLOSE_35", "CLOSE_35_B"]}},
        "pictures": {"pixels_wide": 4096, "pixels_high": int(round(4096 * S.H / S.W)), "states": ["day", "night_lit", "night_dark"], "file_names": "<spec_id>_<state>.png, <spec_id>.json (shop, w, h, d, camera_d, pixels, states, made_by, samples)",
                     "brightness": {"day": 0.15, "night": 0.7}, "colour": "8-bit sRGB PNG, no alpha", "samples": 128, "denoise": True,
                     "never_baked": "no real people, brands, drink, betting, children, nothing after 1992 (the spec's never list)", "rig": "shop-room.py's camera rule; Cycles; the rig per state is in each shop's room.lights"},
        "gate_in_the_cloud": {
            "how": ("The builder shows what the game will show without Unreal: the shop's front is assembled in Blender from the 3.2 parts (and the door and lobby of this target), the display's real meshes stand in front of the card "
                    "where the display is, and the card is a flat quad with an emission picture computed PER CAMERA by tools/ue/make_interior_material.py's `trace` (the Python function, imported, not rewritten): "
                    "for every pixel of the card the card point and the eye go through `trace` and the picture is sampled at the returned (u, v), bilinear with mips, times the state's brightness (day 0.15, night 0.7). "
                    "That picture is baked to an image for the camera and set as the card's emission in Cycles, so what is judged is the game's rule pixel for pixel; the glass is the game's job and is left out "
                    "(a clear 6 mm pane with no reflection) or drawn at the game's day value only if the review asks."),
            "check": "PRJ-03: the baked card picture equals the trace-sampled picture for the same camera to within 1 level",
            "views": "per shop: STREET_SQUARE, STREET_30, CLOSE_35, by day and by night (six renders); the review of two views is STREET and CLOSE",
            "what_it_cannot_show": "the game's glass reflections, Lumen's light on the display, the card's motion vectors under TSR, the exposure: those stay owed on the PC"},
        "inventory": {"polyhaven": allowed, "polyhaven_read": DATE, "scripted": scripted, "denied": DENIED, "surfaces": SURFACES, "sketchfab_checked": sk, "ambientcg_checked": amb,
                      "brand_blocklist": BRAND_BLOCKLIST, "content_blocklist": CONTENT_BLOCKLIST,
                      "rule": "every model a build places is listed in its inventory.json; each must be in `polyhaven`, `scripted` or a Sketchfab uid of `sketchfab_checked`; none in `denied`; no object, material or text "
                              "contains a word of the blocklists; every Poly Haven model is inspected at 1k for lettering and any maker's mark is painted out of its base-colour map (thumbnails only were looked at on 12 October: "
                              "the gate's first check is by eye)"},
        "spec_entries": spec_entries,
        "photographs": {},
        "checks": [],
        "disagreements_photographs_win": [],
        "previous_failures_answered": [],
        "reuse": [],
        "could_not_settle": [],
    }
    return t


if __name__ == "__main__":
    tt = build()
    # the parts that are prose live in make_doc.py's data module and are merged by extras.py
    import extras
    extras.merge(tt)
    json.dump(tt, open(os.path.join(HERE, "target.json"), "w"), indent=1, ensure_ascii=False)
    print("wrote target.json", os.path.getsize(os.path.join(HERE, "target.json")) // 1024, "KB; shops", len(tt["shops"]), "spec entries", len(tt["spec_entries"]), "models", len(tt["inventory"]["polyhaven"]))
