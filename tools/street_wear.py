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
import math
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
        if b["name"] in BRICK_STREAK_BAYS:
            # S3 (30 October): the brick's world-noise streaks, as strong as the house is worn, on this house's brick
            # rows only (VignetteShot.cpp PaintStreet), its tint untouched
            houses[-1]["streak"] = round(BRICK_STREAK_AMOUNT * wear, 3)
            houses[-1]["streak_also"] = list(BRICK_STREAK_BAYS[b["name"]])
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
            if b["name"] == CHANDLER:
                # THE CHANDLER'S STREAKS LENGTHENED TO ITS FASCIA (30 October, S1): drawn from the sill's own underside
                # (the picture is the right way up since 29 October, strongest in its first rows) and long enough to
                # run down to the cloud front's cornice, which takes no street marks, so the run ends there
                L = STREAK_LEN_M[0] + (STREAK_LEN_M[1] - STREAK_LEN_M[0]) * rnd(s, "len")
                d = wall_decal("streak", p["x_m"] + 0.08 * (rnd(s, "dx") - 0.5), top + STREAK_TUCK_M - L / 2.0, zf, facing,
                               p["sx_m"] * (0.8 + 0.3 * rnd(s, "w")), L, CHANDLER_STREAK_STRENGTH[0] + (CHANDLER_STREAK_STRENGTH[1] - CHANDLER_STREAK_STRENGTH[0]) * rnd(s, "st"), b["name"])
                d["picture"] = STREAK_PICTURES[int(rnd(s, "pic") * 3) % 3]
                decals.append(d)
                continue
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
    decals += chandler_marks(pieces, house)
    # Every ground mark stands at the ground's own height where it lies (ground_y).
    for d in decals:
        if d.get("pitch_deg") == 90.0:
            d["y_m"] = ground_y(d["z_m"])
    for d in decals:
        if d["on"] == CHANDLER:
            stain_chandler(d)
    decals += room_wear()
    decals += counter_marks()
    decals += office_marks()
    decals += office_smoke()
    for d in decals:
        if d["on"] == "mickeys_room":
            stain_office(d)
    # THE FRONTS' MARKS OF USE ARE NO LONGER DECALS (7 October, evening): projected onto paint they
    # land on nothing (TakesMarks) or streak (the try of that evening); the painted and tiled fronts
    # wear at the foot in their own material (make_base_material.py WEAR_PARAM). frontage_wear
    # stays for the record and for a later projection that can fade by angle.
    return houses, decals, coverage(bays, decals)


OFFICE = os.path.join(REPO, "production", "specs", "mickeys-office.json")
ROOM_FLOOR_M = 0.12     # the real room's floor stands 12 cm up (VignetteShot.cpp SpawnShopRoom)
NOTICE_WALL_X = 8.65    # the notice wall behind the bench (shop-room.py: the room's left wall, 5.3 m wide)


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
    # heads and hands print an oval smudge faded at every edge (26 October, item 5: the damp strip's
    # straight sides read as three stuck-on rectangles behind the bench; tools/make_wear_masks.py)
    smudge, rub, damp = "ours/wear_head", "ours/wear_splash", "ours/wear_damp_patch"
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
    if b:   # the room's side wall behind the bench (x 8.65, facing -x: yaw 270): where the heads of
        # three sitting people rest, three uneven patches, not one band (8 October, item 1.1's third
        # review, V9: the band's straight top read as a printed strip)
        s = seed_of("mickeys_bench_heads")
        for k in range(3):
            z = b["z0"] + (b["z1"] - b["z0"]) * (k + 0.5 + 0.3 * (rnd(s, "z%d" % k) - 0.5)) / 3.0
            out.append({"kind": "grime", "picture": smudge, "x_m": 8.65,
                        # a seated head rests about 1.05 m up, above the dado's top at 0.95 (26 October: at
                        # 0.9 the smudges sat on the dado's edge and read as dirt on the rail)
                        "y_m": round(ROOM_FLOOR_M + 1.02 + 0.08 * rnd(s, "y%d" % k), 4),
                        "z_m": round(z, 4), "w_m": round(0.38 + 0.14 * rnd(s, "w%d" % k), 4),
                        "h_m": round(0.32 + 0.12 * rnd(s, "h%d" % k), 4),
                        "yaw_deg": 270.0, "pitch_deg": 0.0, "strength": round(0.42 + 0.1 * rnd(s, "st%d" % k), 3),   # 29 October: 0.35 to 0.5 left their sheen under 0.1 (D11)
                        "on": "mickeys_room"})
    d = box.get("the back door, shut")
    if d:   # hands on the wall beside the back door's frame, off the opening itself (8 October, V9:
        # centred 15 cm inside the door, the patch ran across the frame once the room drew it open)
        out.append({"kind": "grime", "picture": smudge, "x_m": round(d["x1"] + 0.22, 4), "y_m": round(ROOM_FLOOR_M + 1.0, 4),
                    "z_m": d["z0"], "w_m": 0.26, "h_m": 0.4, "yaw_deg": 0.0, "pitch_deg": 0.0,
                    "strength": 0.6, "on": "mickeys_room"})
        out.append({"kind": "damp", "picture": damp, "x_m": 8.3, "y_m": round(ROOM_FLOOR_M + 2.62, 4),
                    "z_m": d["z0"], "w_m": 0.9, "h_m": 0.6, "yaw_deg": 0.0, "pitch_deg": 0.0,
                    "strength": 0.7, "on": "mickeys_room"})   # 29 October: 0.6 left its sheen under 0.1 (D11)
    return out


RINGS, BURNS, CHIPS = "ours/wear_rings", "ours/wear_burns", "ours/wear_chips"
PALE, KICK = "ours/wear_pale", "ours/wear_splash"
#: THE NOTICE WALL'S PAINT WHERE A NOTICE KEPT THE SMOKE OFF IT (29 October): the wall reads (0.156, 0.098, 0.038) in
#: the base-colour view (linear), a smoke-browned tan, so the cleaner paint behind a notice is about three fifths
#: lighter and a little less yellow; the first tint, 0.66, lightened it 227% (tools/stain_check.py, run 2).
PALE_TINT = [0.25, 0.165, 0.075]


def office_marks(spec_path=OFFICE):
    """THE OFFICE'S OTHER MARKS, 29 October (his order D11, the look; production/research/street-wear/
    MAFIA-WEAR-2026-10-28.md, Mickey's office, O2: 10 to 14 on its four walls and floor, at most 6 a wall):
    beside the heads, the hands and the damp, two pale oblongs on the notice wall where earlier notices hung
    and were taken down (clear of the prints now there: shop-room.py's fares, licence, accounts and calendar),
    two kicks at the foot of the stair-strip wall where people come in past it, and the carpet trodden flat
    on the way from the door to the counter and under the bench's waiting feet. Street metres (the office
    spec's: x = 6.0 - room x, z = 5.27 + room y, up = room z + 0.12); the notice wall stands at x 8.65."""
    if not os.path.isfile(spec_path):
        return []
    spec = json.load(open(spec_path, encoding="utf-8"))
    box = {b["name"]: b for b in spec.get("boxes", [])}
    door = spec.get("door", {})
    out = []
    s = seed_of("mickeys_office_marks")
    # above the accounts card, and past the calendar toward the counter
    for k, (z, y, w, h) in enumerate(((5.80, 1.86, 0.25, 0.33), (7.22, 1.60, 0.22, 0.30))):
        out.append({"kind": "pale", "picture": PALE, "tint": PALE_TINT, "x_m": NOTICE_WALL_X, "y_m": y,
                    "z_m": round(z, 4), "w_m": w, "h_m": h, "yaw_deg": 270.0, "pitch_deg": 0.0,
                    "strength": round(0.45 + 0.1 * rnd(s, "pale%d" % k), 3), "on": "mickeys_room"})
    st = box.get("stair strip wall")
    if st:   # its room face (x 4.19, facing +x: yaw 90), at a shoe's height
        for k, z in enumerate((5.75, 6.85)):
            out.append({"kind": "kick", "picture": KICK, "x_m": st["x1"], "y_m": round(ROOM_FLOOR_M + 0.13, 4),
                        "z_m": round(z + 0.2 * (rnd(s, "kz%d" % k) - 0.5), 4), "w_m": round(0.55 + 0.25 * rnd(s, "kw%d" % k), 4),
                        "h_m": 0.26, "yaw_deg": 90.0, "pitch_deg": 0.0,
                        # 0.78 (29 October): at the counter's 0.91 they darkened the stair wall's brown 43%, over the 40%
                        "strength": round(0.76 + 0.04 * rnd(s, "ks%d" % k), 3), "on": "mickeys_room"})
    c, b = box.get("counter"), box.get("bench")
    if door and c:   # from the doorway to the booking place, along the way walked
        x0, z0, x1, z1 = door["x"], door["z"] + 0.45, 6.0, c["z0"] - 0.25
        out.append({"kind": "path", "picture": "ours/wear_head", "x_m": round((x0 + x1) / 2, 4), "y_m": ROOM_FLOOR_M,
                    "z_m": round((z0 + z1) / 2, 4), "w_m": round(math.hypot(x1 - x0, z1 - z0) + 0.6, 4), "h_m": 0.8,
                    "yaw_deg": round(math.degrees(math.atan2(z1 - z0, x1 - x0)), 1), "pitch_deg": 90.0,
                    "strength": 0.55, "on": "mickeys_room"})
    if b:            # where the waiting feet rest, along the bench
        out.append({"kind": "path", "picture": "ours/wear_head", "x_m": round(b["x0"] - 0.35, 4), "y_m": ROOM_FLOOR_M,
                    "z_m": round((b["z0"] + b["z1"]) / 2, 4), "w_m": round(b["z1"] - b["z0"] + 0.2, 4), "h_m": 0.55,
                    "yaw_deg": 90.0, "pitch_deg": 90.0, "strength": 0.5, "on": "mickeys_room"})
    return out


#: TOBACCO SMOKE ON THE OFFICE'S WALLS, 29 October (his order D11, O1; MAFIA-WEAR-2026-10-28.md, Mickey's office:
#: "full at the ceiling, none 1.2 m above the floor, yellow-brown, roughness 0.1 lower"). Mafia paints a second layer
#: by vertex colour, which the room's export does not carry (the research's review), so each wall takes one mark the
#: wall's width, from 1.2 m up to 2 cm under the ceiling (shop-room.py: 2.9 m), its picture full at the top
#: (tools/make_wear_masks.py wear_smoke); the ceiling's own colour carries its full smoke (shop-room.py). A tar-brown
#: deposit laid at about 0.4 at its top (the picture's 0.9 x the stain grey's 0.75 x strength 0.6), so a wall at the
#: notice wall's (0.156, 0.098, 0.038) darkens about a quarter, under the layer recipe's 40%; its sheen target 0.6 so
#: the matt paint (0.85) shows about 0.1 less rough at the top. Street metres; 2 cm short of each corner.
SMOKE = "ours/wear_smoke"
SMOKE_TINT = [1.0, 0.65, 0.25]
SMOKE_FROM_M, CEILING_M = 1.2, 2.9
OFFICE_WALLS = (("notice wall", 8.65, None, 270.0), ("stair strip wall", 4.19, None, 90.0), ("back wall", None, 9.40, 0.0))
OFFICE_SPAN_X, OFFICE_SPAN_Z = (4.19, 8.65), (5.27, 9.40)


def office_smoke():
    y0, y1 = ROOM_FLOOR_M + SMOKE_FROM_M, ROOM_FLOOR_M + CEILING_M - 0.02
    out = []
    for name, x, z, yaw in OFFICE_WALLS:
        if x is not None:      # a side wall, running along z
            a, b = OFFICE_SPAN_Z
            cx, cz = x, (a + b) / 2
        else:                  # the back wall, running along x
            a, b = OFFICE_SPAN_X
            cx, cz = (a + b) / 2, z
        out.append({"kind": "smoke", "picture": SMOKE, "tint": SMOKE_TINT, "x_m": round(cx, 4), "y_m": round((y0 + y1) / 2, 4),
                    "z_m": round(cz, 4), "w_m": round(b - a - 0.04, 4), "h_m": round(y1 - y0, 4), "yaw_deg": yaw,
                    "pitch_deg": 0.0, "strength": 0.6, "on": "mickeys_room", "wall": name})
    return out


#: EACH OFFICE MARK'S SHEEN, 29 October (D11, the layer recipe's step 1: a stain differs from its wall by at least
#: 0.1 in the roughness view). The decal blends its sheen by the same coverage as its colour, at most about a fifth
#: to a third of the way at a mark's strongest (its picture's coverage times its strength), so each target stands
#: well away from its surface: the cream paint and the carpet are near matt (shop-room.py: 0.85, 0.95), and hands,
#: heads, fresh damp and the trodden pile polish them; paint a notice kept from the light has not chalked; rubber
#: kicks and dried tea dull a surface, burns char it. First values, fixed by tools/stain_check.py's first run.
STAIN_ROUGH = {"grime": 0.3, "damp": 0.35, "scuff": 0.95, "kick": 0.95, "pale": 0.55, "path": 0.45, "smoke": 0.6}
STAIN_ROUGH_PICTURE = {RINGS: 0.8, BURNS: 1.0}   # burns 1.0 (29 October): their thin lines read under 0.1 at 0.9


def stain_office(d):
    """The office's marks laid with M_LedgerStain (colour and sheen), the street's with M_LedgerGrime until their own gate."""
    d["material"] = "stain"
    d["rough"] = STAIN_ROUGH_PICTURE.get(d["picture"], STAIN_ROUGH.get(d["kind"], 0.6))
    return d


#: ONE SHOP FRONT WORN BY THE LAYER RECIPE: THE CHANDLER'S (30 October 2026, his order D11; production/research/street-wear/
#: MAFIA-WEAR-2026-10-28.md, "One shop front: the chandler", S1 and S3). Its bay keeps its eight marks (the splash and
#: damp bands at the foot, the wash from the eaves, on its front and its south gable, and its two sill streaks) and
#: gains two: one rust leak under the gutter's end (Mafia's 2.1 m by 0.55 m) and the dirt trodden onto the footway at
#: its two doors. All ten are laid with M_LedgerStain, each with a sheen of its own, so a mark differs from the brick in
#: roughness as well as colour (the layer recipe's step 1). Ten on the bay, six on its front, three on its gable, one
#: on the ground; leaks and streaks three of the nine wall marks (Mafia's street: 38%, about two in five; five of nine
#: if the full-height washes are counted as Mafia's full-height leak stains, which they resemble). The cloud's front
#: takes no street marks (shop-interiors.json "street_decals": false), so every mark lands on the street's own brick
#: and paving around it.
CHANDLER = "east_chandler_bay0"
CHANDLER_FRONT_Z = 5.295        # shop-interiors.json: the cloud front's wall face, its doors in it
#: the sill streaks' length: the study's 1.5 to 2.5 m (I), kept to where the streak pictures' 1,024 rows give 512 px/m
#: within 20% (C6: 427 to 602); each runs from its sill to the cornice, about 0.75 m down, and the rest falls on the
#: cloud front, which takes none
STREAK_LEN_M = (1.7, 2.4)
STREAK_TUCK_M = 0.02            # the mark's top this far up under the sill's nose (concrete: it takes no marks)
RUST = "production/assets/street-wear/wear_rust"
THRESHOLD = "production/assets/street-wear/wear_threshold"
#: Mafia's rust leaks' tint (R; the study, layer 3), over their own picture; ours is CHANDLER_TINT's, over our picture's
#: own rust brown (tools/make_wear_masks.py), measured against this brick
RUST_TINT_MAFIA = [0.78, 0.69, 0.64]
#: the gutter's end the leak hangs from: the gutter runs x 40 to 46 at the eaves (vignette-pieces.json
#: east_chandler_gutter), and the bay has no downpipe, so it discharges at its end by the alley (x 46)
RUST_X_M, RUST_TOP_M, RUST_W_M, RUST_H_M = 45.70, 6.25, 0.55, 2.1
#: the threshold: both of the cloud front's doors (its shop door x 43.76 to 44.63, its side door 44.73 to 45.55, read off
#: its pictures: the piece list's doors at x 40.8 and 41.6 are the old refit's, and try 2 laid it before the window),
#: out 0.9 m from the front's face
THRESHOLD_X_M, THRESHOLD_W_M, THRESHOLD_D_M = 44.65, 1.9, 0.9
CLOUD_DOORS_X_M = ((43.76, 44.63), (44.73, 45.55))
#: EACH MARK'S SHEEN (the layer recipe's step 1: at least 0.1 off its wall in the roughness view). Measured in the game's
#: roughness view before any change (F:/LedgerTools/gate/new/chandler-wear/before/buffers), the bay's brick reads 0.90
#: (decoded; 0.96 as shown, p10 to p90 0.93 to 0.97) and the paving at its doors 0.58, so no matt mark could stand 0.1
#: off the brick; on this wet day the marks water lays are wet and the smoother ones: the wash off the eaves, the sill
#: streaks and the rust run, the splash from the wet road, rising damp the most. The dirt trodden onto the wet flags
#: is the one matt mark (mud breaks the water's sheen). TRY 2 (30 October, after try 1's measure and its lit picture):
#: at 0.40 to 0.55 the marks stood 0.26 to 0.40 off the brick, well past the 0.1, and their sheen caught the sky, so in
#: the lit view the bay read cleaner than before; eased to 0.55 to 0.7, about 0.15 off.
CHANDLER_ROUGH = {"splash": 0.6, "wash": 0.7, "damp": 0.55, "streak": 0.65, "rust": 0.7, "threshold": 0.95}
#: EACH MARK'S COLOUR (the layer recipe's step 1: a mark darkens its base colour by at most 40%): a mark lays its picture's
#: colour (the grey 64 of 255, 0.051 linear, or the rust's own) times its tint over the surface by its coverage, which
#: the overlapping wash, damp and splash raise to about 0.95 at the wall's foot. The kinds' street tints (VignetteShot.cpp
#: TintOf, 0.10 to 0.20) are near black over this dark brick (the bay's brick measured (0.19, 0.061, 0.032) linear, mean
#: 0.094; the paving at the doors (0.138, 0.120, 0.102)): the old wash darkened it about 70% at its strongest. TRY 1 laid
#: about 0.6 to 0.7 of each surface's mean (tint = colour / 0.051) and measured at the marks' strongest fiftieth: the wash
#: 27% darker, the sill streaks 10 and 16%, the rust 40%, the threshold 5%, and the bay read clean in the lit view (the
#: old wash was much darker). TRY 2 aims each at about a third: the wash's grey a seventh darker, the streaks' 0.6 of
#: try 1's and laid stronger (CHANDLER_STREAK_STRENGTH), the rust a tenth lighter, the threshold's mud 0.72 of try 1's.
CHANDLER_TINT = {"splash": [1.52, 1.05, 0.76], "wash": [1.44, 0.87, 0.64], "damp": [2.11, 0.67, 0.35],
                 "streak": [1.0, 0.6, 0.44], "rust": [1.38, 1.21, 1.1], "threshold": [1.26, 1.09, 0.91]}
#: the chandler's sill streaks laid stronger than the street's (0.35 to 0.75) in try 2: at try 1's 0.53 and 0.56 they
#: darkened the brick only 10 and 16% where they are strongest, under the wash, and did not read
CHANDLER_STREAK_STRENGTH = (0.75, 0.9)
#: S3, THE BRICK'S STREAKS (30 October): Mafia's facade masters tint their colour by a world-position noise, its tiling
#: (10.7, 11.1) across the two level axes and 1 up, so it varies ten times faster along a wall than up it (streaks),
#: raised to the power 0.56 (the study, layer 2; R). Here only the chandler's house carries it (nothing is multiplied
#: before he approves one sample), on its front's and its north wall's brick rows; the amount is the most the streaks
#: darken, times the house's wear. The shape's scale is tools/ue/make_base_material.py's.
BRICK_STREAK_BAYS = {CHANDLER: ("east_chandler_bay_north",)}
BRICK_STREAK_AMOUNT = 0.25


def chandler_marks(pieces, house):
    """The chandler's two new marks (its eight are made with the street's rules, its streaks lengthened in the sill loop)."""
    by = {p["name"]: p for p in pieces["pieces"]}
    b = by.get(CHANDLER)
    if b is None:
        return []
    zf, facing = face_of(b)
    h = house[CHANDLER]
    out = []
    rust = wall_decal("streak", RUST_X_M, RUST_TOP_M - RUST_H_M / 2.0, zf, facing, RUST_W_M, RUST_H_M, 0.7 + 0.2 * h["wear"], CHANDLER)
    rust.update({"kind": "rust", "picture": RUST})
    out.append(rust)
    out.append({"kind": "threshold", "picture": THRESHOLD, "x_m": THRESHOLD_X_M, "y_m": 0.0,
                "z_m": round(CHANDLER_FRONT_Z - THRESHOLD_D_M / 2.0, 4), "w_m": THRESHOLD_W_M, "h_m": THRESHOLD_D_M,
                "yaw_deg": 0.0, "pitch_deg": 90.0, "strength": round(0.75 + 0.2 * h["wear"], 3), "on": CHANDLER})
    return out


def stain_chandler(d):
    """The chandler's marks laid with M_LedgerStain, each with its kind's sheen and colour."""
    d["material"] = "stain"
    d["rough"] = CHANDLER_ROUGH[d["kind"]]
    d["tint"] = list(CHANDLER_TINT[d["kind"]])
    return d
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
    # ON THE BARE LAMINATE (29 October, D11's O2: measured in the base-colour view, the fare book and the papers lie
    # at x 5.3 to 5.8 and 7.1 to 8.0, and two rings and a burn had printed on them): each mark's x where the top is bare
    # (29 October, the office gate's back view: the first ring, 0.32 m across at x 6.05, reached the papers' edge at 5.8 and
    # printed onto the sheet beside them; moved to 6.08 and drawn at 0.24 m, nearer a mug's ring, its second and last move)
    for k, (bx, size, pic, strength) in enumerate(((6.08, 0.24, RINGS, 0.7), (6.85, 0.30, RINGS, 0.6), (8.35, 0.34, RINGS, 0.65),
                                                   (6.30, 0.22, BURNS, 0.85), (6.55, 0.20, BURNS, 0.8))):
        x = bx + 0.06 * (rnd(s, "x%d" % k) - 0.5)
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
    street_front = [d for d in decals if d["kind"] in ("dust", "chip") or (d["kind"] == "scuff" and d["on"] != "mickeys_room")]
    check("no shopfront marks are projected onto the street's paint (7 October: they wear in their material)", not street_front)
    counter = [d for d in decals if d["kind"] == "scuff" and d["on"] == "mickeys_room"]
    check("the office counter's scuffs read, at FRONT_WEAR or more (7 October)",
          counter and all(d["strength"] >= FRONT_WEAR for d in counter))
    office = [d for d in decals if d["on"] == "mickeys_room"]
    # the smoke is O1's layer, not one of O2's marks
    walls_floor = [d for d in office if d["picture"] not in (RINGS, BURNS) and d["kind"] != "smoke" and not (d["kind"] == "scuff" and d["yaw_deg"] == 0.0)]
    smoke = [d for d in office if d["kind"] == "smoke"]
    check("smoke on each of the office's three walls, from 1.2 m up to the ceiling (O1)",
          len(smoke) == 3 and len({d["wall"] for d in smoke}) == 3
          and all(abs(d["y_m"] - d["h_m"] / 2 - (ROOM_FLOOR_M + SMOKE_FROM_M)) < 1e-3 and d["y_m"] + d["h_m"] / 2 <= ROOM_FLOOR_M + CEILING_M for d in smoke))
    check("the office's walls and floor carry 10 to 14 marks (O2), at most 6 a wall",
          10 <= len(walls_floor) <= 14 and max(sum(1 for d in walls_floor if (d["pitch_deg"], d["yaw_deg"], round(d["x_m"], 2) if d["yaw_deg"] in (90.0, 270.0) else round(d["z_m"], 2)) == k)
                                                for k in {(d["pitch_deg"], d["yaw_deg"], round(d["x_m"], 2) if d["yaw_deg"] in (90.0, 270.0) else round(d["z_m"], 2)) for d in walls_floor if d["pitch_deg"] == 0.0}) <= 6)
    check("every office mark is laid with the stain material and a sheen of its own",
          office and all(d.get("material") == "stain" and 0.0 <= d.get("rough", -1) <= 1.0 for d in office))
    check("the street's marks keep the grime material until their own gate", not any(d.get("material") for d in decals if d["on"] not in ("mickeys_room", CHANDLER)))
    # THE CHANDLER'S BAY (30 October, S1 and S3)
    ch = [d for d in decals if d["on"] == CHANDLER]
    walls = {}
    for d in ch:
        if d["pitch_deg"] == 0.0:
            walls.setdefault(d["yaw_deg"], []).append(d)
    leaks = [d for d in ch if d["kind"] in ("streak", "rust")]
    on_walls = sum(len(v) for v in walls.values())
    check("the chandler's bay carries 8 to 10 marks, at most 6 a wall", 8 <= len(ch) <= 10 and max(len(v) for v in walls.values()) <= 6)
    check("its leaks and streaks about two in five of its wall marks (a third to a half)", 1 / 3.0 - 1e-9 <= len(leaks) / float(on_walls) <= 0.5)
    check("its base band kept: a splash and a damp band at the foot of its front and its gable",
          all(sum(1 for d in v if d["kind"] == k) == 1 for v in walls.values() for k in ("splash", "damp")))
    st = [d for d in ch if d["kind"] == "streak"]
    sills = [p for p in pieces["pieces"] if p["bom"] == "C13_sills_lintels" and p["name"].startswith("east_chandler_up") and "_sill" in p["name"]]
    check("its sill streaks drawn 1.5 to 2.5 m long from their sills' undersides",
          len(st) == len(sills) == 2 and all(1.5 <= d["h_m"] <= 2.5 for d in st)
          and all(min(abs(d["y_m"] + d["h_m"] / 2 - STREAK_TUCK_M - (p["y_m"] - p["sy_m"] / 2)) for p in sills) < 1e-3 for d in st))
    rust = [d for d in ch if d["kind"] == "rust"]
    check("one rust leak, Mafia's 2.1 by 0.55 m, hanging from the eaves", len(rust) == 1 and (rust[0]["h_m"], rust[0]["w_m"]) == (2.1, 0.55)
          and abs(rust[0]["y_m"] + rust[0]["h_m"] / 2 - RUST_TOP_M) < 1e-3)
    thr = [d for d in ch if d["kind"] == "threshold"]
    check("the threshold's dirt on the footway before both doors, up to the front's face",
          len(thr) == 1 and thr[0]["pitch_deg"] == 90.0 and abs(thr[0]["y_m"] - FOOTWAY_ABOVE_CROWN_M) < 1e-6
          and abs(thr[0]["z_m"] + thr[0]["h_m"] / 2 - CHANDLER_FRONT_Z) < 1e-3
          and thr[0]["x_m"] - thr[0]["w_m"] / 2 <= min(a for a, _b in CLOUD_DOORS_X_M) and thr[0]["x_m"] + thr[0]["w_m"] / 2 >= max(b for _a, b in CLOUD_DOORS_X_M))
    check("every chandler mark is laid with the stain material, a sheen and a tint of its own",
          all(d.get("material") == "stain" and 0.0 <= d["rough"] <= 1.0 and len(d.get("tint", [])) == 3 for d in ch))
    streaked = [h for h in houses if h.get("streak")]
    check("the brick's streaks on the chandler's house alone, as strong as it is worn (S3)",
          [h["bay"] for h in streaked] == [CHANDLER] and abs(streaked[0]["streak"] - round(BRICK_STREAK_AMOUNT * streaked[0]["wear"], 3)) < 1e-9)
    pale = [d for d in office if d["kind"] == "pale"]
    prints = [(6.32, 1.70, 0.30, 0.42), (6.89, 1.82, 0.21, 0.148), (5.75, 1.54, 0.30, 0.10), (6.89, 1.34, 0.30, 0.42)]   # shop-room.py, street metres
    check("the pale oblongs keep clear of the notices hanging now",
          len(pale) == 2 and all(abs(d["z_m"] - z) * 2 >= d["w_m"] + w or abs(d["y_m"] - y) * 2 >= d["h_m"] + h for d in pale for z, y, w, h in prints))
    pud = [d for d in decals if d["kind"] == "puddle"]
    check("puddles stand along both gutters", any(d["z_m"] > 2 for d in pud) and any(d["z_m"] < -2 for d in pud))
    print("street_wear selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    write()
