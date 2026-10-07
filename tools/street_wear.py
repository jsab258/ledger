"""The street's wear layer, placed by rule from the street's own pieces (D53; the proof frame, stage 1).

    python tools/street_wear.py            # writes production/specs/street-wear.json and prints the coverage
    python tools/street_wear.py --selftest

WHY, 1 October (Jafar's ruling on the AAA street research,
production/research/aaa-street): "the wear layer I ruled for on 21 September,
'grime is the strategy', D53, was never built, so build it, with per-house
variation seeds and wear masks emitted by the generator; replace the flat
decal pictures with Unreal's projected decals". The sameness of the street
comes from the generator, so the variety and the wear come from it too, by
rule, never painted by hand; the game spawns what this file lists
(VignetteShot.cpp, SpawnWear) and the town reuses the same rules.

WHAT IT READS: production/specs/vignette-pieces.json, the street as the game
builds it (bays, sills, downpipes and their shoes, chimney stacks, footways).
WHAT IT WRITES: production/specs/street-wear.json:
  houses: one per bay, keyed by the bay piece, with a seed from its name (so a
    house keeps its look whatever else changes), its brick set (0, 1 or 2), a
    tint (a small per-house shift of the brick's colour) and how worn it is
    (0.55 to 1.0, which scales every stain on it);
  decals: projected decals, each with its kind, the picture it uses, centre,
    size, facing and strength; the rules (the research's, section 1):
      splash  the lowest 300 mm of every street wall, splash-back from the road
      streak  under every sill, where rain runs off it
      algae   at every downpipe's shoe, and up the wall beside the pipe
      soot    on the upper face of every chimney stack
      oil     on the road by the kerbs where cars stand
      puddle  standing water along both gutters, where the crossfall sends it
              (M_LedgerWet: darker, a near mirror, the ground drowned flat)
  coverage: D53's printed quantity, per wall: the fraction of the wall's
    visible area under wear decals, `wearCoverage=<fraction>/<wall>`, with
    `wearCoverageN` and `wearCoverageMin=<fraction>/<wall>` for the batch.
The pictures are CC0 (ambientCG, already staged under
ledger/Assets/StreamingAssets/Decals/ambientcg) until the free Megascans are in
Jafar's library; a kind's picture is one line here to change.
"""
import json
import os
import sys
import zlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIECES = os.path.join(REPO, "production", "specs", "vignette-pieces.json")
OUT = os.path.join(REPO, "production", "specs", "street-wear.json")
STANDOFF_M = 0.01           # the scene file's decal standoff (decals.standoff_m)
END_WALL_T = 0.34           # a row's end wall, one and a half bricks (terrace-front.py END_WALL_T): the gable face stands this far past the end bay
DAMP_M = 1.0               # rising damp: the lowest metre of a solid wall darker and patchy (2 October)
ROAD_HALF_M, ROAD_CROSSFALL, FOOTWAY_ABOVE_CROWN_M = 3.0, 0.025, 0.10   # terrace-front.py ROAD_HALF_M, ROAD_CROSSFALL, THRESHOLD_ABOVE_CROWN_M
SPLASH_M = 0.60             # the splash-back band at the foot of a wall (2 October: 0.30 and faint did not show in the stage-1 frame)
STREAK_PICTURES = ("ours/wear_streak", "ours/wear_streak_b", "ours/wear_streak_c")
PICTURE = {"damp": "ours/wear_damp", "wash": "ours/wear_wash", "splash": "ours/wear_splash", "streak": "ours/wear_streak",
           "algae": "ours/wear_algae", "soot": "ours/wear_soot",
           "oil": "ours/wear_oil", "puddle": "ours/puddle_01"}   # 2 October: the packs' real masks (tools/make_wear_masks.py), not their preview renders
PUDDLES = ("ours/puddle_01", "ours/puddle_02", "ours/puddle_03")
CHANNEL_Z_M = 2.87         # the gutters, either side (ground_east_channel and ground_west_channel)


def rnd(seed, k):
    """A fixed number in [0, 1) from a seed and a key: the same house, the same look."""
    return (zlib.crc32(("%d/%s" % (seed, k)).encode()) & 0xFFFFFF) / float(0x1000000)


def seed_of(name):
    return zlib.crc32(name.encode()) & 0x7FFFFFFF


def face_of(bay):
    """The wall facing the street: its z, and +1 for the west side (facing +z), -1 for the east."""
    z, sz = bay["z_m"], bay["sz_m"]
    return (z - sz / 2.0, -1.0) if z > 0 else (z + sz / 2.0, 1.0)


def wall_decal(kind, x, y, z_face, facing, w, h, strength, owner):
    # A wall decal stands STANDOFF_M proud of the face, toward the street;
    # yaw 0 faces -z (the east walls), 180 faces +z (the west walls), as the
    # scene file's own wall decals do.
    return {"kind": kind, "picture": PICTURE[kind], "x_m": round(x, 4), "y_m": round(y, 4),
            "z_m": round(z_face + facing * STANDOFF_M, 4), "w_m": round(w, 4), "h_m": round(h, 4),
            "yaw_deg": 0.0 if facing < 0 else 180.0, "pitch_deg": 0.0, "strength": round(strength, 3), "on": owner}


def ground_y(z):
    """The ground's height across the street at z (terrace-front.py road_z): 0 at the crown,
    falling 1 in 40 to each channel 3 m out; the footway 0.10 above the crown. A ground mark
    stands at it, since it reaches only 16 cm up and 6 cm down (2 October: placed at the
    crown's height, the gutter puddles fell out of reach)."""
    a = abs(z)
    return round(-min(a, ROAD_HALF_M) * ROAD_CROSSFALL, 4) if a <= ROAD_HALF_M + 0.15 else FOOTWAY_ABOVE_CROWN_M


def gable_decal(kind, x, y, z_mid, w, h, strength, owner):
    """A mark on a gable end facing south (yaw 270), across the block's depth."""
    return {"kind": kind, "picture": PICTURE[kind], "x_m": round(x, 4), "y_m": round(y, 4), "z_m": round(z_mid, 4),
            "w_m": round(w, 4), "h_m": round(h, 4), "yaw_deg": 270.0, "pitch_deg": 0.0,
            "strength": round(strength, 3), "on": owner}


def build(pieces):
    P = pieces["pieces"]
    bays = [p for p in P if p["bom"] == "C1_terrace_carcass" and "_bay" in p["name"]]
    houses, decals = [], []
    by_block = {}
    for b in bays:
        block = b["name"].rsplit("_bay", 1)[0]
        by_block.setdefault(block, []).append(b)
    for b in sorted(bays, key=lambda q: q["name"]):
        s = seed_of(b["name"])
        wear = 0.55 + 0.45 * rnd(s, "wear")
        houses.append({"bay": b["name"], "seed": s, "brick_set": int(rnd(s, "set") * 3) % 3,
                       "tint": [round(0.92 + 0.16 * rnd(s, c), 3) for c in "rgb"], "wear": round(wear, 3)})
    house = {h["bay"]: h for h in houses}

    def owner_bay(x, block):
        for b in by_block.get(block, []):
            if abs(x - b["x_m"]) <= b["sx_m"] / 2.0 + 1e-6:
                return b
        return None

    for b in sorted(bays, key=lambda q: q["name"]):
        zf, facing = face_of(b)
        h = house[b["name"]]
        bottom = b["y_m"] - b["sy_m"] / 2.0
        # (4 October: at 0.5 to 0.9 the review measured the foot lighter than the wall above.)
        decals.append(wall_decal("splash", b["x_m"], bottom + SPLASH_M / 2.0, zf, facing, b["sx_m"], SPLASH_M,
                                 0.8 + 0.2 * h["wear"], b["name"]))
        # WEAR THAT READS AT A GLANCE ON EVERY FACADE (Jafar, 2 October, Friday's page:
        # "wear that reads at a glance across every facade, not faint marks"): the wash
        # the gables carry, down every bay's front from its top (rain off the eaves and
        # the gutter's overflow, darkest at the head), and rising damp in its lowest metre.
        top = b["y_m"] + b["sy_m"] / 2.0
        # THE WASH DOWN TO THE FOOT (4 October, the first fresh review of 2.4: its edge at a tenth
        # of the wall's height read as a straight line with clean brick below it).
        decals.append(wall_decal("wash", b["x_m"], top - b["sy_m"] * 0.5, zf, facing, b["sx_m"] * 1.02, b["sy_m"],
                                 0.45 + 0.35 * h["wear"], b["name"]))
        decals.append(wall_decal("damp", b["x_m"], bottom + DAMP_M / 2.0, zf, facing, b["sx_m"] * 1.02, DAMP_M,
                                 0.40 + 0.30 * h["wear"], b["name"]))
    # THE GABLE ENDS (2 October: the stage-1 frame's biggest wall, the side of Mickey's block,
    # carried no wear at all, since only the bays' fronts were marked): at each row's
    # south end, facing the camera's way (yaw 270), a splash band at its foot and a weathered
    # wash down the whole face to break the brick's tiling.
    for block, row in sorted(by_block.items()):
        g = min(row, key=lambda q: q["x_m"])
        hg = house[g["name"]]
        gx = g["x_m"] - g["sx_m"] / 2.0 - END_WALL_T - STANDOFF_M
        bottom = g["y_m"] - g["sy_m"] / 2.0
        decals.append(gable_decal("splash", gx, bottom + SPLASH_M / 2.0, g["z_m"], g["sz_m"], SPLASH_M,
                                  0.8 + 0.2 * hg["wear"], g["name"]))
        # THE GABLE'S WASH FLUSH WITH ITS CORNERS AND DOWN TO ITS FOOT (4 October: at 95% by 90%
        # its edges stood as a straight soot line by the corner and a clean band above the foot;
        # wider than the face it would smear round the corner onto the front).
        decals.append(gable_decal("wash", gx, bottom + g["sy_m"] * 0.5, g["z_m"], g["sz_m"], g["sy_m"],
                                  0.50 + 0.35 * hg["wear"], g["name"]))
        decals.append(gable_decal("damp", gx, bottom + DAMP_M / 2.0, g["z_m"], g["sz_m"] * 0.95, DAMP_M,
                                  0.40 + 0.30 * hg["wear"], g["name"]))
    for p in P:
        if p["bom"] == "C13_sills_lintels" and "_sill" in p["name"]:
            block = p["name"].split("_up")[0].split("_gf")[0]
            b = owner_bay(p["x_m"], block)
            if b is None:
                continue
            zf, facing = face_of(b)
            h = house[b["name"]]
            s = seed_of(p["name"])
            # 2 October: at 0.5 to 1.2 m and half strength the first frame showed none; the sheet's run long
            L = 0.8 + 0.6 * rnd(s, "len") * h["wear"]
            top = p["y_m"] - p["sy_m"] / 2.0
            # FROM THE SILL'S OWN EDGE (4 October, the first fresh review of 2.4: the streaks began
            # well below the sills): the picture fades in over its top fifth, so it starts a quarter
            # of its length up, on the stone sill, which takes no marks.
            # ONE OF THREE STREAKS a window, lighter and each its own (4 October: "one identical
            # decal under every window ... inky").
            d = wall_decal("streak", p["x_m"] + 0.08 * (rnd(s, "dx") - 0.5), top - L / 2.0 + 0.25 * L, zf, facing,
                           p["sx_m"] * (0.8 + 0.3 * rnd(s, "w")), L, 0.35 + 0.25 * rnd(s, "st") + 0.15 * h["wear"], b["name"])
            d["picture"] = STREAK_PICTURES[int(rnd(s, "pic") * 3) % 3]
            decals.append(d)
        elif p["bom"] == "D5_downpipe" and p["name"].endswith("_shoe"):
            block = p["name"].split("_dp")[0]
            b = owner_bay(p["x_m"], block)
            if b is None:
                continue
            zf, facing = face_of(b)
            h = house[b["name"]]
            # (4 October: at 0.65 and 0.3 the review found no algae anywhere on the dark brick.)
            decals.append(wall_decal("algae", p["x_m"], 0.35, zf, facing, 0.8, 1.0, 0.85 + 0.15 * h["wear"], b["name"]))
            decals.append(wall_decal("algae", p["x_m"] + 0.12, 1.3, zf, facing, 0.35, 1.5, 0.55 + 0.3 * h["wear"], b["name"]))
        elif p["bom"] == "D2_chimney_stack":
            block = p["name"].split("_stack")[0]
            b = owner_bay(p["x_m"], block)
            h = house[b["name"]] if b is not None else {"wear": 0.8}
            # the stack's street face (it stands on the ridge, its depth across the street)
            zf = p["z_m"] - p["sz_m"] / 2.0 if p["z_m"] > 0 else p["z_m"] + p["sz_m"] / 2.0
            facing = -1.0 if p["z_m"] > 0 else 1.0
            top = p["y_m"] + p["sy_m"] / 2.0
            decals.append(wall_decal("soot", p["x_m"], top - 0.6, zf, facing, p["sx_m"] * 1.05, 1.2,
                                     0.85 + 0.15 * h["wear"], p["name"]))
            # AND ITS SOUTH FACE, the one the hook camera sees (4 October: "the chimneys are clean").
            decals.append(gable_decal("soot", p["x_m"] - p["sx_m"] / 2.0 - STANDOFF_M, top - 0.6, p["z_m"],
                                      p["sz_m"], 1.2, 0.85 + 0.15 * h["wear"], p["name"]))
    # oil where cars stand: along both kerbs, a stain every few metres, by seed
    for side, z in (("east", 2.1), ("west", -2.1)):
        s = seed_of("oil_" + side)
        x = 4.0
        k = 0
        while x < 44.0:
            x += 3.5 + 4.0 * rnd(s, "gap%d" % k)
            if x >= 44.0:
                break
            w = 0.4 + 0.5 * rnd(s, "w%d" % k)   # 2 October: a drip under a parked car, not a slick
            decals.append({"kind": "oil", "picture": PICTURE["oil"], "x_m": round(x, 4),
                           "z_m": round(z + 0.6 * (rnd(s, "z%d" % k) - 0.5), 4), "w_m": round(w * 1.4, 4),
                           "h_m": round(w, 4), "yaw_deg": round(360.0 * rnd(s, "yaw%d" % k), 2), "pitch_deg": 90.0,
                           "strength": round(0.22 + 0.18 * rnd(s, "st%d" % k), 3), "on": "ground_" + side + "_carriageway"})
            k += 1
    # standing water along both gutters: the road's crossfall sends the rain there
    for side, sign in (("east", 1.0), ("west", -1.0)):
        s = seed_of("puddle_" + side)
        x = 2.0
        k = 0
        while True:
            x += 4.0 + 6.0 * rnd(s, "gap%d" % k)
            if x >= 46.0:
                break
            L = 0.9 + 1.4 * rnd(s, "len%d" % k)
            W = 0.22 + 0.12 * rnd(s, "wid%d" % k)
            # IN THE CHANNEL, between the double yellow lines and the kerb (3 October: laid
            # across the lines, the water greyed them into a smear; the fresh review's "blob")
            z = sign * (CHANNEL_Z_M + 0.01)
            decals.append({"kind": "puddle", "picture": PUDDLES[int(rnd(s, "pic%d" % k) * 3) % 3], "x_m": round(x, 4),
                           "z_m": round(z, 4), "w_m": round(L, 4), "h_m": round(W, 4),
                           "yaw_deg": round(-8.0 + 16.0 * rnd(s, "yaw%d" % k), 2), "pitch_deg": 90.0,
                           "strength": round(0.75 + 0.2 * rnd(s, "st%d" % k), 3), "on": "ground_" + side + "_channel"})
            k += 1
    # STANDING WATER ACROSS THE CARRIAGEWAY (Jafar, 2 October: "the wet street and its
    # reflections"): a worn British road ponds in its wheel tracks and its dips, not only
    # at the kerb, and those mirrors of the shopfronts are what make a street read wet at
    # a glance. Two tracks a side, a pool every few metres, long along the road.
    for side, sign in (("east", 1.0), ("west", -1.0)):
        s = seed_of("track_" + side)
        x = 3.0
        k = 0
        while True:
            x += 4.0 + 7.0 * rnd(s, "gap%d" % k)
            if x >= 42.0:
                break
            L = 1.2 + 1.8 * rnd(s, "len%d" % k)
            W = 0.5 + 0.7 * rnd(s, "wid%d" % k)
            track = 1.6 + 0.6 * rnd(s, "track%d" % k)   # the nearside wheel track, wandering (3 October: a centre row read as stamped)
            decals.append({"kind": "puddle", "picture": PUDDLES[int(rnd(s, "pic%d" % k) * 3) % 3], "x_m": round(x, 4),
                           "z_m": round(sign * track, 4), "w_m": round(L, 4), "h_m": round(W, 4),
                           "yaw_deg": round(-12.0 + 24.0 * rnd(s, "yaw%d" % k), 2), "pitch_deg": 90.0,
                           "strength": round(0.8 + 0.2 * rnd(s, "st%d" % k), 3), "on": "ground_" + side + "_carriageway"})
            k += 1
    # THE RECIPE'S PUDDLES ON THE FLAGS AND THE ROAD, 2 October: its mesh sheets are retired
    # (terrace-front.py WATER_AS_DECALS) and stand here as soft-masked water at the same spots,
    # the decal a little larger than the sheet because the mask's water fills about a third of it.
    for k, (cx, cz, rx, rz) in enumerate(recipe_puddles()):
        s = seed_of("recipe_puddle_%d" % k)
        decals.append({"kind": "puddle", "picture": PUDDLES[k % 3], "x_m": round(cx, 4), "y_m": 0.0,
                       "z_m": round(cz, 4), "w_m": round(2.0 * rx * 1.5, 4), "h_m": round(2.0 * rz * 1.7, 4),
                       "yaw_deg": round(-10.0 + 20.0 * rnd(s, "yaw"), 2), "pitch_deg": 90.0,
                       "strength": round(0.7 + 0.2 * rnd(s, "st"), 3),
                       "on": "ground_" + ("east" if cz > 0 else "west") + ("_footway" if abs(cz) > CHANNEL_Z_M + 0.2 else "_carriageway")})
    # Every ground mark stands at the ground's own height where it lies (ground_y).
    for d in decals:
        if d.get("pitch_deg") == 90.0:
            d["y_m"] = ground_y(d["z_m"])
    decals += room_wear()
    decals += counter_marks()
    decals += frontage_wear(pieces)
    return houses, decals, coverage(bays, decals)


OFFICE = os.path.join(REPO, "production", "specs", "mickeys-office.json")
ROOM_FLOOR_M = 0.12     # the real room's floor stands 12 cm up (VignetteShot.cpp SpawnShopRoom)


def room_wear(spec_path=OFFICE):
    """MICKEY'S OFFICE WORN BY USE, 6 October (phase 1, item 1.1; the third review: "no wear"): by
    rule from the office's own plan, never by hand, as the street's: shoes along the counter's
    front, heads and shoulders on the wall behind the waiting bench, hands round the back door's
    handle, and the damp that comes in at the back's top corner. Street metres, as the plan."""
    if not os.path.isfile(spec_path):
        return []
    spec = json.load(open(spec_path, encoding="utf-8"))
    box = {b["name"]: b for b in spec.get("boxes", [])}
    out = []
    # the street's own prepared masks (ours/), never ambientCG's folder previews, which are
    # sphere renders and stood in the room as round blobs (6 October, the first film)
    smudge, rub, damp = "ours/wear_damp", "ours/wear_splash", "ours/stain_Leaking005"
    c = box.get("counter")
    if c:   # the customers' face of the counter, toward the window (yaw 0 faces -z): a few uneven
        # patches where people stand to book, not one band (6 October: one decal the counter's
        # length read as a stripe from the street)
        x0, x1 = c["x0"], min(c["x1"], 8.65)
        s = seed_of("mickeys_counter_scuffs")
        for k in range(3):
            x = x0 + 0.4 + (x1 - x0 - 0.8) * (k + rnd(s, "x%d" % k)) / 3.0
            out.append({"kind": "scuff", "picture": rub, "x_m": round(x, 4),
                        "y_m": round(ROOM_FLOOR_M + 0.14, 4), "z_m": c["z0"],
                        "w_m": round(0.8 + 0.4 * rnd(s, "w%d" % k), 4), "h_m": 0.28,
                        "yaw_deg": 0.0, "pitch_deg": 0.0, "strength": round(FRONT_WEAR + 0.15 * rnd(s, "st%d" % k), 3),
                        "on": "mickeys_room"})
    b = box.get("bench")
    if b:   # the room's side wall behind the bench (x 8.65, facing -x: yaw 270)
        out.append({"kind": "grime", "picture": smudge, "x_m": 8.65, "y_m": round(ROOM_FLOOR_M + 0.95, 4),
                    "z_m": round((b["z0"] + b["z1"]) / 2, 4), "w_m": round(b["z1"] - b["z0"], 4), "h_m": 0.5,
                    "yaw_deg": 270.0, "pitch_deg": 0.0, "strength": 0.45, "on": "mickeys_room"})
    d = box.get("the back door, shut")
    if d:   # round the handle, on the door's left as the office sees it from the street
        out.append({"kind": "grime", "picture": smudge, "x_m": round(d["x0"] + 0.15, 4), "y_m": round(ROOM_FLOOR_M + 1.0, 4),
                    "z_m": d["z0"], "w_m": 0.35, "h_m": 0.45, "yaw_deg": 0.0, "pitch_deg": 0.0,
                    "strength": 0.7, "on": "mickeys_room"})
        out.append({"kind": "damp", "picture": damp, "x_m": 8.3, "y_m": round(ROOM_FLOOR_M + 2.62, 4),
                    "z_m": d["z0"], "w_m": 0.9, "h_m": 0.6, "yaw_deg": 0.0, "pitch_deg": 0.0,
                    "strength": 0.6, "on": "mickeys_room"})
    return out


RINGS, BURNS, CHIPS = "ours/wear_rings", "ours/wear_burns", "ours/wear_chips"
#: THE KIT BAY'S FRONT (6 October; tools/art-recipes/terrace-front.py KIT_BAYS, Rita's): its pieces'
#: faces in street metres, from the kit's layout (the window from the bay's left pier, then the shop
#: door, then the side door; production/art/shopfront-kit/README.md): the bay's x0, the window's run,
#: each door's centre and width, and the faces' depths in front of the wall (5.125).
KIT_FRONTS = {"east_parade_bay2": {"x0": 15.0, "window": (15.35, 18.70), "shop_door": (19.203, 0.90),
                                   "side_door": (20.178, 0.838), "stall_face": 4.975, "plinth_face": 4.975,
                                   "door_face": 5.05},
              # MICKEY'S FRONT TOO (7 October, the second review: "Mickey's ... front clean"): its own
              # front, not the kit's, measured off the exported street: the tiled stallriser x 5.1 to
              # 8.6 with its face at 5.1, the office door's middle 4.65 and the side door's 3.75, both
              # faces at 5.15, the piers' feet on the frontage at x 3.0 and 9.0.
              "east_parade_bay0": {"x0": 3.0, "window": (5.12, 8.61), "shop_door": (4.65, 0.90),
                                   "side_door": (3.75, 0.70), "stall_face": 5.10, "plinth_face": 4.975,
                                   "door_face": 5.15}}


#: HOW STRONGLY A FRONT'S USE SHOWS (7 October, item 1.1's second fresh review, point 6: "Rita's
#: stallriser, sills and door bottoms pristine; Mickey's counter top and front clean", after the
#: first review's same words; his order of 2 October: wear that reads at a glance, not faint marks).
#: The pictures' masks average under a third opaque, so at 0.55 a mark darkened or lightened its
#: paint by about a sixth; from 0.85 it reads. The door scuffs reach a boot's kick, 0.34 m.
FRONT_WEAR = 0.85


def frontage_wear(pieces):
    """A SHOPFRONT WORN BY USE, by rule (6 October; item 1.1's first gate: "Rita's stallriser,
    pilaster feet, sills and door bottoms pristine", the research naming exactly those as the most
    worn by 1990, production/research/shopfronts/FRONTAGE-2026-10-06.md): dried road splash and dust
    up the stallriser's foot and the piers' plinths, paint chipped to the undercoat along the sill's
    nosing and round the shop door's handle, and boots' scuffs on both doors' bottoms. Paint wears
    lighter, so the dust and the chips are light marks (M_LedgerGrime's TintOnly)."""
    by = {p["name"]: p for p in pieces["pieces"]}
    out = []
    for bay, f in KIT_FRONTS.items():
        b = by.get(bay)
        if b is None:
            continue
        g = b["y_m"] - b["sy_m"] / 2.0
        s = seed_of(bay + "_kit_wear")
        w0, w1 = f["window"]

        def put(kind, pic, x, y, z, w, h, strength):
            out.append({"kind": kind, "picture": pic, "x_m": round(x, 4), "y_m": round(y, 4), "z_m": round(z - STANDOFF_M, 4),
                        "w_m": round(w, 4), "h_m": round(h, 4), "yaw_deg": 0.0, "pitch_deg": 0.0,
                        "strength": round(strength, 3), "on": bay})
        put("dust", PICTURE["splash"], (w0 + w1) / 2.0, g + 0.22, f["stall_face"], w1 - w0, 0.44, FRONT_WEAR + 0.15 * rnd(s, "st"))
        for px in (f["x0"], f["x0"] + 6.0):
            put("dust", PICTURE["splash"], px, g + 0.22, f["plinth_face"], 0.72, 0.44, FRONT_WEAR + 0.15 * rnd(s, "p%.0f" % px))
            put("chip", CHIPS, px, g + 0.55, f["plinth_face"], 0.72, 0.30, FRONT_WEAR)
        put("chip", CHIPS, (w0 + w1) / 2.0, g + 0.61, f["stall_face"], w1 - w0, 0.09, FRONT_WEAR)
        sx, sw = f["shop_door"]
        put("chip", CHIPS, sx + 0.30, g + 1.02, f["door_face"], 0.30, 0.32, FRONT_WEAR)
        for x, w in (f["shop_door"], f["side_door"]):
            put("scuff", PICTURE["splash"], x, g + 0.17, f["door_face"], w * 0.95, 0.34, FRONT_WEAR + 0.15 * rnd(s, "d%.1f" % x))
    return out


def counter_marks(spec_path=OFFICE):
    """THE COUNTER'S TOP WORN BY USE (6 October; item 1.1's first gate: "the counter top clean: no
    scuffs, rings, burns"): tea rings where the mugs stand, cigarette burns along its customers'
    edge by the ashtray, and the laminate rubbed at the booking place; on the top's own height
    (the room's floor at ROOM_FLOOR_M, the top 0.985 above it), facing up."""
    if not os.path.isfile(spec_path):
        return []
    box = {b["name"]: b for b in json.load(open(spec_path, encoding="utf-8")).get("boxes", [])}
    c = box.get("counter")
    if not c:
        return []
    top = ROOM_FLOOR_M + 0.985 + 0.002
    x0, x1 = c["x0"], min(c["x1"], 8.65)
    z0, z1 = c["z0"], c["z1"]
    out = []
    s = seed_of("mickeys_counter_top")
    for k, (fx, size, pic, strength) in enumerate(((0.18, 0.32, RINGS, 0.7), (0.47, 0.30, RINGS, 0.6), (0.78, 0.34, RINGS, 0.65),
                                                   (0.30, 0.22, BURNS, 0.85), (0.62, 0.20, BURNS, 0.8))):
        x = x0 + (x1 - x0) * fx + 0.1 * (rnd(s, "x%d" % k) - 0.5)
        z = z0 + 0.12 + (z1 - z0 - 0.24) * rnd(s, "z%d" % k) * (0.5 if pic == BURNS else 1.0)
        out.append({"kind": "grime", "picture": pic, "x_m": round(x, 4), "y_m": round(top, 4), "z_m": round(z, 4),
                    "w_m": size, "h_m": size, "yaw_deg": round(360.0 * rnd(s, "yaw%d" % k), 1), "pitch_deg": 90.0,
                    "strength": strength, "on": "mickeys_room"})
    return out


def recipe_puddles():
    """FOOTWAY_PUDDLES + ROAD_PUDDLES from tools/art-recipes/terrace-front.py, (x, z across, rx, rz)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("terrace_front", os.path.join(REPO, "tools", "art-recipes", "terrace-front.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return tuple(mod.FOOTWAY_PUDDLES) + tuple(mod.ROAD_PUDDLES)


def coverage(bays, decals):
    """D53's quantity, per street wall: the share of its area under wear decals (overlaps counted once
    as a cap: never above 1)."""
    rows = []
    for b in sorted(bays, key=lambda q: q["name"]):
        area = b["sx_m"] * b["sy_m"]
        under = sum(d["w_m"] * d["h_m"] for d in decals if d["on"] == b["name"])
        rows.append((min(1.0, under / area), b["name"]))
    return rows


def write():
    pieces = json.load(open(PIECES, encoding="utf-8"))
    houses, decals, cov = build(pieces)
    out = {"schema": "ledger.street-wear/1", "source": "production/specs/vignette-pieces.json",
           "generator": "tools/street_wear.py", "ruled": "D53 (21 September) and Jafar's ruling of 1 October on the proof frame",
           "houses": houses, "decals": decals,
           "coverage": [{"wall": w, "wearCoverage": round(c, 4)} for c, w in cov]}
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    kinds = {}
    for d in decals:
        kinds[d["kind"]] = kinds.get(d["kind"], 0) + 1
    for c, w in cov:
        print("wearCoverage=%.4f/%s" % (c, w))
    lo = min(cov)
    print("wearCoverageN=%d wearCoverageMin=%.4f/%s" % (len(cov), lo[0], lo[1]))
    print("streetWear houses=%d decals=%d %s" % (len(houses), len(decals), " ".join("%s=%d" % kv for kv in sorted(kinds.items()))))


def selftest():
    ok = bad = 0

    def check(what, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("street_wear selftest FAIL " + what)
    pieces = json.load(open(PIECES, encoding="utf-8"))
    houses, decals, cov = build(pieces)
    houses2, decals2, _ = build(pieces)
    check("the same pieces give the same wear (seeded, never random)", houses == houses2 and decals == decals2)
    check("every bay is a house with its own seed", len(houses) == len({h["seed"] for h in houses}) and len(houses) >= 10)
    check("houses differ: more than one brick set and tint", len({h["brick_set"] for h in houses}) > 1 and len({tuple(h["tint"]) for h in houses}) > 1)
    sills = [p for p in pieces["pieces"] if p["bom"] == "C13_sills_lintels" and "_sill" in p["name"]]
    check("a streak under every sill", sum(1 for d in decals if d["kind"] == "streak") == len(sills))
    for d in decals:
        if d["kind"] == "streak":
            sill = min(sills, key=lambda p: abs(p["x_m"] - d["x_m"]) + abs(p["z_m"] - d["z_m"]) + abs(p["y_m"] - (d["y_m"] + d["h_m"] / 2)))
            # (4 October) its faded top quarter lies over the sill and the window above, which
            # take no marks; its body hangs below the sill's underside.
            under = sill["y_m"] - sill["sy_m"] / 2.0
            if not (d["y_m"] + d["h_m"] / 2.0 <= under + 0.25 * d["h_m"] + 1e-3
                    and d["y_m"] - d["h_m"] / 2.0 < under):
                check("a streak hangs below its sill", False)
                break
    splash = [d for d in decals if d["kind"] == "splash"]
    check("a splash band at the foot of every street wall and each row's gable end, 600 mm tall",
          len([d for d in splash if d["yaw_deg"] != 270.0]) == len(houses) and len([d for d in splash if d["yaw_deg"] == 270.0]) >= 1 and all(abs(d["h_m"] - SPLASH_M) < 1e-9 for d in splash))
    check("wall decals stand off the wall toward the street", all(d.get("yaw_deg") == 270.0 or abs(abs(d["z_m"]) - 5.125) <= STANDOFF_M + 1e-6
                                                                  for d in splash))
    check("every wall's coverage is printed and between 0 and 1", len(cov) == len(houses) and all(0.0 < c <= 1.0 for c, _ in cov))
    check("every decal names a picture", all(d["picture"] for d in decals))
    front = [d for d in decals if d["kind"] in ("dust", "chip", "scuff")]
    check("a front's use reads: its dust, chips and scuffs at FRONT_WEAR or more (7 October)",
          front and all(d["strength"] >= FRONT_WEAR for d in front))
    pud = [d for d in decals if d["kind"] == "puddle"]
    check("puddles stand along both gutters", any(d["z_m"] > 2 for d in pud) and any(d["z_m"] < -2 for d in pud))
    print("street_wear selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    write()
