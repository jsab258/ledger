"""Poly Haven models and textures (CC0) for the shop rooms, fetched by script (item 2a, 1 October).

    python tools/art-recipes/fetch_polyhaven.py [--res 1k] [--out F:/LedgerTools/polyhaven] ID [ID ...]
    python tools/art-recipes/fetch_polyhaven.py --set pawnbroker
    python tools/art-recipes/fetch_polyhaven.py --selftest

WHY. Jafar's bar (CLAUDE.md, 1 October): a room judged beside the KCD2 frames
cannot be built from boxes and spheres; the first render read as placeholder
boxes. Poly Haven's library is CC0 (https://polyhaven.com/license), on the
allowlist, and his standing permission covers free content on it. This asks
Poly Haven's public API (api.polyhaven.com/files/<id>) for each asset's glTF
(models) or its texture maps (textures) at the given resolution and saves them
under OUT/<id>/<res>/, with a source.json naming the asset, its page and its
licence. Nothing is sent but the asset's name.
"""
import json
import os
import sys
import urllib.request

API = "https://api.polyhaven.com/files/"
OUT = "F:/LedgerTools/polyhaven"
SETS = {
    # A 1990 pawnbroker's stock (production/research/shop-window-interiors/NOTE.md, section 9):
    # watches, cameras, radios and cassette players, a television, clocks, binoculars, tools, a suitcase.
    "pawnbroker": ["pocket_watch", "vintage_pocket_watch", "Camera_01", "vintage_video_camera", "boombox",
                   "cassette_player", "portable_cassette_player", "television_02", "wall_clock", "mantel_clock_01",
                   "vintage_binocular", "vintage_suitcase", "pipe_wrench", "vintage_hand_drill",
                   "brass_vase_01", "steel_frame_shelves_01", "wooden_bookshelf_worn",
                   "cardboard_box_01", "vintage_cabinet_01",
                   # the second pass (1 October, judged in the game against the bar: the room read
                   # sterile and sparse): the floor stock, the right wall, the till and the instruments
                   "Ukulele_01", "CashRegister_01", "Television_01", "vintage_grandfather_clock_01",
                   "metal_tool_chest", "metal_toolbox", "wooden_display_shelves_01", "worn_metal_rack",
                   "vintage_radio_transceiver", "filmstrip_projector_8mm", "vintage_electric_kettle",
                   "tea_set_01", "alarm_clock_01", "vintage_telephone_wall_clock", "fancy_picture_frame_01",
                   "ornate_mirror_01", "bench_vice_01", "handsaw_wood", "hand_plane_no4", "chess_set"],
    # THE WINDOW DISPLAY, the near metre behind the glass as real meshes (the note, section 7):
    # small valuables on a stepped velvet bed, each ticketed. No weapons, no drink, no toys.
    "pawnbroker_display": ["pocket_watch", "vintage_pocket_watch", "digital_wrist_watch", "alarm_clock_01",
                           "Camera_01", "binoculars", "round_spectacles", "vintage_lighter", "cigarette_case",
                           "magnifying_glass_01", "brass_vase_01", "mantel_clock_01", "portable_cassette_player",
                           # the third pass (the fresh reviewer: "copy-pasted ... identical cameras, clocks"):
                           # more distinct pieces, each used once or twice
                           "brass_vase_02", "brass_vase_03", "ceramic_vase_01", "ceramic_vase_03",
                           "antique_ceramic_vase_01", "standing_picture_frame_01", "standing_picture_frame_02",
                           "carved_wooden_elephant", "horse_statue_01", "seadogs_compass", "vintage_flashlight",
                           "measuring_tape_01", "jug_01", "vintage_video_camera", "vintage_radio_transceiver"],
    # THE OTHER SHOPFRONTS (V1, 3 October; his yes to Rita's window: "make the other eleven like it").
    # An ironmonger's: hand tools, cleaners and oils, a watering can, brooms, a blowtorch, a ladder.
    "ironmonger": ["adjustable_wrench", "combination_wrench", "cross_pein_hammer", "wooden_hammer_01", "pliers",
                   "tongue_groove_pliers", "screwdriver", "screwdrivers_02", "flathead_screwdriver", "handsaw_wood",
                   "hatchet", "measuring_tape_01", "vintage_hand_drill", "watering_can_metal_01", "small_oil_can_01",
                   "oil_tin", "brass_blowtorch", "lubricant_spray", "bleach_bottle", "multi_cleaner_bottle",
                   "all_purpose_cleaner", "drain_cleaner", "cleaner_tin_01", "plastic_broom", "wooden_broom", "dustpan",
                   "trowel_01", "garden_gloves_01", "mousetrap", "lightbulb_01", "metal_jug", "wooden_ladder",
                   "metal_toolbox", "pot_enamel_01", "metal_jerrycan", "rubber_boots", "drawer_cabinet"],
    # A ship's chandler's: buoys and a lifebuoy, a life jacket, lanterns, boots, oilskin hats, oil, crates.
    "chandler": ["lifebuoy", "life_jacket", "ocean_buoy", "lateral_sea_marker", "seadogs_compass", "Lantern_01",
                 "caged_hanging_light", "signal_flashlight", "rubber_boots", "fishermans_hat", "small_oil_can_01",
                 "metal_jerrycan", "wooden_crate_01", "Barrel_01", "brass_blowtorch", "vintage_flashlight",
                 "oil_tin", "industrial_wall_lamp", "wooden_bucket_01"],
    # A tea room's: tables and chairs, cakes, a teapot and cups, pictures on the walls, a plant.
    "tea_room": ["WoodenChair_01", "painted_wooden_chair_01", "round_wooden_table_01", "tea_set_01", "carrot_cake",
                 "strawberry_chocolate_cake", "croissant", "metal_jug", "CashRegister_01", "potted_plant_01",
                 "potted_plant_02", "hanging_picture_frame_01", "hanging_picture_frame_02", "hanging_picture_frame_03",
                 "wall_clock", "vintage_electric_kettle", "standing_chalkboard_01"],
    # A newsagent and tobacconist's: postcards, notepads and stationery, cigarettes (tobacco is allowed), a till.
    "newsagent": ["cigarette_pack", "postcard_set_01", "office_notepads", "stationery_supplies", "binder_notebook",
                  "CashRegister_01", "vintage_lighter", "wall_clock", "cardboard_box_01"],
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "LEDGER-shop-rooms/1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def files_for(asset, res):
    """(relative path, url) pairs for one asset at one resolution: a model's glTF and what it includes."""
    meta = json.loads(get(API + asset))
    if "gltf" in meta:
        g = meta["gltf"].get(res) or next(iter(meta["gltf"].values()))
        g = g["gltf"]
        pairs = [(os.path.basename(g["url"]), g["url"])]
        for rel, inc in (g.get("include") or {}).items():
            pairs.append((rel, inc["url"]))
        return "model", pairs
    pairs = []
    for mapname, byres in meta.items():
        if not isinstance(byres, dict) or res not in byres:
            continue
        fmt = byres[res].get("png") or byres[res].get("jpg")
        if fmt:
            pairs.append((os.path.basename(fmt["url"]), fmt["url"]))
    return "texture", pairs


def fetch(asset, res, out):
    kind, pairs = files_for(asset, res)
    root = os.path.join(out, asset, res)
    total = 0
    for rel, url in pairs:
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            data = get(url)
            open(path, "wb").write(data)
        total += os.path.getsize(path)
    json.dump({"asset": asset, "kind": kind, "page": "https://polyhaven.com/a/" + asset, "licence": "CC0 1.0",
               "licenceUrl": "https://polyhaven.com/license", "resolution": res, "files": [p for p, _ in pairs]},
              open(os.path.join(root, "source.json"), "w", encoding="utf-8"), indent=1)
    return kind, len(pairs), total


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("fetch_polyhaven selftest FAIL " + name)
    check("every set names assets", all(SETS[s] for s in SETS))
    check("no asset twice in a set", all(len(v) == len(set(v)) for v in SETS.values()))
    print("fetch_polyhaven selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    res = a[a.index("--res") + 1] if "--res" in a else "1k"
    out = a[a.index("--out") + 1] if "--out" in a else OUT
    ids = SETS[a[a.index("--set") + 1]] if "--set" in a else [x for x in a if not x.startswith("--") and x not in (res, out)]
    grand = 0
    for asset in ids:
        try:
            kind, n, size = fetch(asset, res, out)
            grand += size
            print("fetched %s (%s, %d files, %.1f MB)" % (asset, kind, n, size / 1e6), flush=True)
        except Exception as e:
            print("FAILED %s: %s" % (asset, e), flush=True)
    print("fetch_polyhaven: %d assets, %.1f MB under %s" % (len(ids), grand / 1e6, out))
