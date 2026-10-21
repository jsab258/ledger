"""pallets: writes target.json and TARGET.md (cloud week 42, unit 13, family 5: timber pallets)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B

FAMILY = "pallets"
PM = json.load(open(os.path.join(HERE, "photo_measurements.json")))["P1"]
RATIO = PM["ratio"]
PL, PW = 1000.0, 1200.0          # stringer length (x), deck board length (y): the 1000 x 1200 pallet of P1
BW, NB = 85.0, 7                 # top board width, count
GAP = (PL - NB * BW) / (NB - 1)
PITCH = BW + GAP
BOT, STR, TOP = 22.0, 100.0, 22.0
H = BOT + STR + TOP
LEAN = 12.0                      # degrees from the vertical
TZ = round(PW / 2 * math.sin(math.radians(90 - LEAN)), 1)   # the lean's lift so the lowest edge rests on the ground
WALL_Y = round(PW / 2 * math.cos(math.radians(90 - LEAN)), 1)


def pallet(tag, dy=0.0, lean=False, worn=False):
    P = []
    xf = {"rot": [0, 0, 90 - LEAN], "t": [0, 0, TZ], "pivot": [0, 0, 0]} if lean else None

    def add(d):
        if xf:
            d["xf"] = xf
        P.append(d)

    for i in range(NB):
        x0 = -PL / 2 + i * PITCH
        add(B("%s_top%d" % (tag, i + 1), x0, x0 + BW, -PW / 2 + dy, PW / 2 + dy, BOT + STR, H, "pallet_wood", edge="arrised 1 mm, ends chamfered 15 x 15 on the underside", note="top deck board 85 x 22 x 1200, softwood"))
    for k, (y0, y1) in enumerate(((-PW / 2, -PW / 2 + 95.0), (-47.5, 47.5), (PW / 2 - 95.0, PW / 2))):
        add(B("%s_str%d" % (tag, k + 1), -PL / 2, PL / 2, y0 + dy, y1 + dy, BOT, BOT + STR, "pallet_wood", edge="arrised 1 mm", note="stringer 95 x 100 x 1000, softwood"))
    for k, (x0, x1) in enumerate(((-PL / 2, -PL / 2 + 100.0), (-50.0, 50.0), (PL / 2 - 100.0, PL / 2))):
        add(B("%s_bot%d" % (tag, k + 1), x0, x1, -PW / 2 + dy, PW / 2 + dy, 0.0, BOT, "pallet_wood", edge="arrised 1 mm, ends chamfered", note="bottom board 100 x 22 x 1200"))
    return P


def build():
    P1 = pallet("p1")
    P2 = pallet("p1") + pallet("p2")
    for p in P2:
        if p["id"].startswith("p2_"):
            p["c"][2] += H
    # PA3 (the sample): one pallet flat at the foot, one leaning on the gable wall
    flat = pallet("p1", dy=0.0)
    # the flat one lies in front of the leaning one's foot: its back edge at local y = -(WALL_Y) - ... ; shift in y by -(600 + WALL_Y + 5)
    sh = -865.0
    for p in flat:
        p["c"][1] += sh
    lean = pallet("p2", lean=True)
    wall = [B("wall_gable", -1500.0, 1500.0, WALL_Y, WALL_Y + 200.0, 0.0, 2600.0, "wall_brick", note="the gable end of the west block (a stand-in slab; the building is the street's)")]
    P3 = flat + lean + wall
    T = {
        "family": FAMILY, "title": "Quay Street's pallets", "units": "millimetres; angles in degrees; z up; the stringers run along x; the deck boards along y; the pivot is the flat pallet's centre on the ground",
        "status": "fixes applied, not re-reviewed", "sample": "PA3",
        "materials": {
            "pallet_wood": {"name": "softwood pallet timber, grey-brown, weathered", "srgb": [150, 124, 92], "rough": 0.85, "rough_words": "rough, fibrous", "metal": False,
                            "note": "new boards pale (190, 165, 120) at the ends, weathered grey-brown (130, 112, 90) on the faces; nail heads rust-stained; NO printed mark, no stamp, no brand (a real pallet carries IPPC and owner marks: left off)"},
            "wall_brick": {"name": "soot-blackened brick (the street's)", "srgb": [78, 64, 58], "rough": 0.9, "rough_words": "rough", "metal": False, "note": "a stand-in for the gable wall"},
        },
        "variants": {
            "PA1": {"name": "PA1: one pallet, flat", "parts": P1, "overall": {"w": PL, "d": PW, "h": H}, "overall_tol": 1.0, "joins": [["p1_top1", "p1_str1"], ["p1_top4", "p1_str2"], ["p1_top7", "p1_str3"], ["p1_str1", "p1_bot1"], ["p1_str2", "p1_bot2"], ["p1_str3", "p1_bot3"]], "embeds": [], "overlap_allow": 3.0,
                    "faces": [{"id": "stringer end", "o": [-PL / 2, -PW / 2 - 0.0, BOT + 2], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, -1, 0], "nu": PL, "nv": STR - 4, "depth": 6.0, "blockers": ["p1_str1"]}]},
            "PA2": {"name": "PA2: two pallets stacked flat", "parts": P2, "overall": {"w": PL, "d": PW, "h": 2 * H}, "overall_tol": 1.0, "joins": [["p2_bot1", "p1_top1"], ["p2_bot2", "p1_top4"]], "embeds": [], "overlap_allow": 3.0, "faces": []},
            "PA3": {"name": "PA3: one flat at the foot and one leaning 12 degrees on the gable wall (the sample)", "parts": P3, "joins": [["p2_bot2", "wall_gable"]], "embeds": [], "overlap_allow": 3.0, "faces": []},
        },
        "drawing": {"views": ["front", "left", "plan"], "sections": [{"id": "x0", "axis": "x", "at": 0.0}, {"id": "y0", "axis": "y", "at": 0.0}]},
        "numbers": [
            {"id": "N1", "what": "stringer length (the pallet's width)", "value": PL, "kind": "Read", "source": "Wikipedia 'Pallet' (read raw, 13 Oct): the standard European sizes 1200 x 1000 (EUR 2) and 1000 x 1200 (EUR 3) and their 144 mm height; P1's pallet is the 1000 x 1200 kind (boards 1200, stringers 1000: the board length is 1.2 times the width in the photograph)", "tol": 1.0, "measure": {"kind": "bbox", "axis": "x", "parts": ["p1_top1", "p1_top7", "p1_str1"]}, "variant": "PA1"},
            {"id": "N2", "what": "deck board length", "value": PW, "kind": "Read", "source": "same", "tol": 1.0, "measure": {"kind": "extent", "axis": "y", "part": "p1_top1"}, "variant": "PA1"},
            {"id": "N3", "what": "overall height", "value": H, "kind": "Read", "source": "same: 144 mm = 22 + 100 + 22", "tol": 0.5, "measure": {"kind": "bbox", "axis": "z"}, "variant": "PA1"},
            {"id": "N4", "what": "top board width", "value": BW, "kind": "Photo", "source": "P1 board width over pitch 0.545 mean (0.59, 0.53, 0.53, 0.53 over five boards: the near boards are nearer the camera) at the 152.5 pitch that 7 boards on 1000 give: 83 mm; 85 chosen (+-6)", "tol": 6.0, "measure": {"kind": "extent", "axis": "x", "part": "p1_top1"}, "variant": "PA1"},
            {"id": "N5", "what": "top board pitch", "value": PITCH, "kind": "Derived", "source": "7 boards of 85 across 1000 leave 6 gaps of 67.5; pitch 152.5", "tol": 1.0, "measure": {"kind": "centre_dx", "axis": "x", "a": "p1_top1", "b": "p1_top2"}, "variant": "PA1"},
            {"id": "N6", "what": "stringer section height", "value": STR, "kind": "Read", "source": "EUR pallet: boards 22 each, stringers 100 (the 144 total)", "tol": 1.0, "measure": {"kind": "extent", "axis": "z", "part": "p1_str1"}, "variant": "PA1"},
            {"id": "N7", "what": "the middle stringer's centre from the pallet's centre", "value": 0.0, "kind": "Photo", "source": "P1: the middle cross member of the leaning pallet sits at 345 to 390 px of a 345 px board length: its centre at 0.49 of the board length (+-0.03)", "tol": 12.0, "measure": {"kind": "centre", "axis": "y", "part": "p1_str2"}, "variant": "PA1"},
            {"id": "N8", "what": "lean from the vertical", "value": LEAN, "kind": "Judgement", "source": "a pallet stands at 10 to 15 degrees against a wall (P1 about 12 by eye); encoded in the part transforms (90 - 78)", "tol": 0.5, "measure": {"kind": "count", "prefix": "unused"}, "variant": "PA3"},
        ],
        "photos": [], "sources": [], "previews": [], "checks": [], "owed": [],
    }
    T["numbers"] = T["numbers"][:7]
    return T


def finish(T):
    T["photo_ratio"] = {"photo": "P1", "board_px": [round(x, 2) for x in RATIO["board_px"]], "pitch_px": [round(x, 2) for x in RATIO["pitch_px"]], "board_over_pitch": [round(x, 3) for x in RATIO["board_over_pitch"]],
                        "mean": round(RATIO["mean"], 3), "tol": 0.06, "method": "five deck boards on a band of rows 296 to 304 of the 1024 px copy, each edge found by the grey-level step in a window of +-4 px; ratio of board width to pitch is the number a perspective view cannot change much: the camera is to the right so the near (right) boards are drawn larger (the pitch grows 30 to 36 px) but the ratio holds within 0.06"}
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/2660949", "read": "2026-10-13", "author": "Brian Robert Marshall", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2011-10-20", "kind": "photograph",
         "shows": "three timber pallets standing on their long edges against a wall beside a doorway on a paved pavement, one leaning about 12 degrees with seven deck boards seen from the front and three cross members (stringers) between; beside them a stack of plastic fish boxes carrying real firms' names",
         "used": True, "not_used_for": "any absolute size (no scale object); the fish boxes and their lettering (masked); the plastic crates", "period": "2011; a softwood stringer pallet is the same object in 1990"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/3572620", "read": "2026-10-13", "author": "Jonathan Billinger", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2013-07-21", "kind": "photograph",
         "shows": "heaps of old pallets in an outhouse yard: the edges of stacked pallets show a bottom board, stringer blocks and a top board; boards split and grey",
         "used": True, "not_used_for": "any number", "period": "2013, old pallets of the 1980s and 1990s kind"},
        {"id": "S3", "url": "https://en.wikipedia.org/wiki/Pallet", "read": "2026-10-13 (raw wikitext)", "author": "Wikipedia contributors", "licence": "CC BY-SA 4.0", "taken": "n/a (a text)", "kind": "book",
         "shows": "stringer pallets (three or more stringers, deck boards on top); the pallet measurement convention (first number the stringer length, second the deckboard length); the European sizes EUR 1 800 x 1200 x 144, EUR 2 1200 x 1000 x 144, EUR 3 1000 x 1200 x 144", "used": True, "not_used_for": "any picture", "period": "n/a"},
        {"id": "S4", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "no pallet; wooden_crate_01, wooden_crate_02 and wooden_military_crate (crates, not pallets)", "used": False, "not_used_for": "everything: no CC0 pallet exists, so it is made by script", "period": "n/a"},
        {"id": "S5", "url": "production/specs/vignette-scene.json (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the held pallet (stood at x 21.8 west, off since 2 October: 'it read as a slab at the yard mouth'), large_pallet 2.00 x 1.10 m and small_pallet (neither placed)", "used": True, "not_used_for": "any shape", "period": "n/a"},
        {"id": "S6", "url": "https://api.geograph.org.uk/syndicator.php (terms pallets, wooden pallets, stack of pallets, pallets yard; takenyear 1980 to 1995 and without a year)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1980 to 1995 searched", "kind": "search record",
         "shows": "for 1980 to 1995 one photograph (a 1977 feed hit that is not a pallet photograph); about 250 photographs from 2006 on; no period pallet photograph", "used": False, "not_used_for": "measuring", "period": "n/a"},
    ]
    T["previews"] = [{"file": "p1-maiden-street-pallets-leaning.jpg", "source": "S1", "credit": "Brian Robert Marshall, Geograph 2660949, CC BY-SA 2.0, 2011-10-20, cropped to the leaning pallets (the fish boxes are outside the crop)",
                      "masked": ["the fish boxes and their printed names are outside the crop"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True}]
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the yard mouth is between lamp pools; the pallets read as pale vertical slats catching the lantern colour (1, 0.25, 0) on their weathered faces and black in the gaps"}
    T["texture"] = {"maps": ["colour", "normal", "roughness"], "decals": [], "marks": [], "note": "grain, weathering, nail stains and grime only: no stamp, no owner's or hire company's mark, no IPPC mark (the plain board is a choice for the no-real-marks rule: 1990 pallets mostly carried owners' marks)"}
    T["handovers"] = [{"id": "H1", "line": "For the scene's owner: the yard mouth (x 21.0 to 24.0, between the two west blocks) has no floor in the data (vignette-scene.json west_north's note calls it 'a gap in the data rather than a modelled object'; vignette-pieces.json has no piece under x 21.5 to 23.0, z -5.6 to -6.8). Give it a floor of setts at the footway's back level, 0.100 above the crown (the level of the ground plots either side), from x 21.0 to 24.0 and from z -5.125 back to the blocks' depth (z -13.125), built before the pallets return."}]
    T["placement"] = {
        "slot": "west side, in the yard mouth (x 21 to 24), behind the crowd-control barrier the scene puts across it, ON A YARD FLOOR OF SETTS AT 0.100 ABOVE THE CROWN (the footway's back level and the ground plots' top: a JUDGEMENT, because the scene models no floor there: handover H1 asks for it, to be built before the pallets return): the leaning pallet against the gable end of the west_south block (its wall face at x 21.0, facing +x), centred at z -6.2; one pallet flat on the yard floor in front of its foot (street x 21.39 to 22.59); the boards are plain, a choice for the no-real-marks rule (1990 pallets mostly carried owners' marks)",
        "floor": {"level_m": 0.100, "kind": "Judgement", "x_m": [21.0, 24.0], "z_m": [-13.125, -5.125], "reason": "the scene's own note calls the yard 'a gap in the data rather than a modelled object'; the ground plots either side top out at 0.100 (vignette-pieces.json ground_plot_2 and _3), the footway's back is 0.100 (the threshold), so the setts are laid level with them; owed to the scene's owner as H1",
                  "modelled_today": False},
        "x_wall_m": 21.0, "yard_x_m": [21.0, 24.0], "z_centre_m": -6.2, "frontage_z_m": -5.125, "barrier_z_m": [-5.0, -5.125], "local_to_street": "local +y points into the gable wall (street -x); local x runs across the yard mouth (street z)", "pallet_width_mm": PL,
        "reasons": [
            "the scene's story is that the yard is shut (a barrier across the mouth, cones, a skip): the pallets behind the barrier are the yard's stuff, one event with the skip; the 2 October ruling took the pallet off the street until real, and this target is the 'real' (RULINGS 2 Oct): a decision for DECISIONS, not a question",
            "the earlier slot (x 21.8 on the west pavement, a flat slab) is dropped: a flat pallet on the footway read as a slab; leaning on a wall it reads as a pallet (S1)",
            "THE FLOOR: the first version put the pallets at z -5.7 to -6.7 behind the building line with no floor under them (the scene file calls the yard mouth 'a gap in the data': vignette-pieces.json has no piece under x 21.5 to 23.0, z -5.6 to -6.8, and its ground plots stop at x 21.0 and start at x 24.0), and its rows tested only the barrier line and the crates; the floor is now stated (setts at 0.100, a Judgement) and handed to the scene's owner (H1), and the shared placement rows check that every pallet foot lies on a modelled surface or on the floor the slot owes, at the stated level",
            "the scene's two wooden crates stand on the pavement at z -4.3 (far edges at -4.76), the pallets inside the yard from z -5.7: 0.94 m clear; the self-check reads the crates' places from the scene and measures the clearance",
            "the scene's large_pallet (2.00 x 1.10) is not a British pallet and is not used",
        ],
        "poses": [{"id": "pallets", "variant": "PA3", "x_m": round(21.0 + WALL_Y / 1000.0, 4), "z_m": -6.2, "yaw_deg": 90.0, "zone": "yard_floor", "base_y_m": 0.100, "ignore_parts": ["wall_gable"], "leans_on": ["C1_terrace_carcass"], "contact_tol_m": 0.03,
                   "floor_owed": {"x": [21.0, 24.0], "z": [-13.125, -5.125], "level_m": 0.100}, "walk_check": False, "head_check": False}],
    }
    T["wear"] = [
        "boards: weathered grey-brown on the faces, paler at freshly broken or sawn ends; one board split along 400 mm; one board missing on the flat pallet's top deck (a gap of 85 mm: a seed), edges rounded by use and grey with grime on the underside",
        "nail heads (not modelled) rust-stained with a 15 mm brown halo; a few sawn-off nail stubs standing 3 mm proud",
        "damp green stain along the lowest 120 mm of the leaning pallet and on the flat pallet's bottom boards; wet-street darkening on everything below 150 mm",
        "NOT shown: any owner's brand, any stamp, any hire company's colour (a real pallet carries marks; this one is plain)",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "the pallet's size and form", "book": "the scene file's held large_pallet 2.00 x 1.10 m and small_pallet (a slab)", "photo": "S1: a 1000 x 1200 stringer pallet with seven boards, three stringers (a middle one at the middle of the boards), the usual look", "chose": "1000 x 1200 x 144, 7 top boards of 85, 3 stringers, 3 bottom boards"},
        {"id": "W2", "what": "where it stands", "book": "the scene: flat on the west pavement at x 21.8", "photo": "S1: leaning on a wall beside a door", "chose": "leaning on the gable wall in the yard mouth, one flat at its foot"},
        {"id": "W4", "what": "the yard's floor", "book": "the scene file: the yard mouth 'is a gap in the data rather than a modelled object' (west_north's note); no piece under x 21.5 to 23.0, z -5.6 to -6.8", "photo": "n/a (a placement fact; S1 shows pallets leaning on a wall beside a door, on a paved ground)", "chose": "a floor of setts at 0.100 above the crown, a Judgement, owed to the scene's owner (H1); the pallets do not return before it is built"},
        {"id": "W3", "what": "block or stringer", "book": "the asset plan's pallet 1,200 x 1,000", "photo": "S2 shows both stringer pallets and some with block feet; S1's is a stringer pallet", "chose": "stringer pallet; a block-footed pallet is not written"},
    ]
    T["variants_note"] = [
        "PA3 (the sample): one flat, one leaning on the gable wall.",
        "PA1: a single flat pallet (for the loading aprons and the chandler's).",
        "PA2: two stacked flat pallets.",
        "conditions (materials and seeds): C0 new and pale (a few), C1 weathered (the sample), C2 one board broken and one missing. A leaning pallet's lean is 10 to 14 degrees by seed.",
    ]
    T["owed"] = [
        {"id": "O1", "line": "Put the pallets back at the yard mouth, one leaning on the gable end and one flat before it, with no owner's mark on any board, now that they are real pallets?", "recommended": "Yes, put them back"},
    ]
    T["not_settled"] = [
        "absolute size: S1 has no scale object, so the 1000 x 1200 x 144 is the European standard (Read), supported by S1's proportions (board length to width of the pallet 1.2), not measured",
        "the board width (85 mm, error 6) comes from a ratio on a perspective view",
        "whether pallets of 1990 were mostly hire pallets with owners' marks (they were; the target leaves every mark off)",
        "the exact yard-mouth clearance: it depends on the crates' places at x 22.4 and 23.1 and the barrier at 22.5, which the scene owns",
        "the yard floor: not in the scene (its note calls the yard a gap in the data); level 0.100 and the setts are a Judgement and the floor is owed (H1)",
    ]
    T["content_rule_note"] = "no person, no drink, no betting: plain timber (a statement of the content rule)."
    T["builder_notes"] = [
        "one mesh per pallet by script: 7 + 3 boards and 3 stringers, boards arrised 1 mm, ends chamfered 15 on the underside; the nails are texture",
        "the leaning pallet is the flat one rotated 78 degrees about its stringer axis (x) with its lowest edge on the ground; the transform is in the part xf of target.json",
        "the gable wall in PA3 is a stand-in: the street's own wall carries the contact",
        "no mark of any kind on any board (texture.marks and texture.decals are empty)",
        "stand the pallets at the pose in target.json (x 21.1247, z -6.2, yaw 90) on the owed yard floor at 0.100 above the crown; do not place them before the floor exists",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.1f mm" % n["value"], "tol": "+-%.1f mm" % n["tol"]})
    C += [
        {"name": "C1: seven top boards, three stringers, three bottom boards", "measure": "count them", "expect": "7, 3, 3", "tol": "exact"},
        {"name": "C2: board width over pitch matches P1", "measure": "top board width / pitch", "expect": "%.3f" % (BW / PITCH), "tol": "+-0.06 of the photograph's %.3f" % RATIO["mean"]},
        {"name": "C3: the leaning pallet rests on the ground and touches the wall", "measure": "the contact graph", "expect": "connected", "tol": "0 floating"},
        {"name": "C4: no mark on any board", "measure": "textures and text", "expect": "none", "tol": "exact"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The pallets are the plain softwood stringer pallet, 1000 x 1200 x 144 mm (seven 85 x 22 top boards 67.5 apart, three 95 x 100 stringers, three 100 x 22 bottom boards), unmarked: the sample is one leaning 12 degrees on the gable wall of the west block in the yard mouth with one flat at its foot (variants: one flat, two stacked), "
           "which replaces the flat slab the 2 October ruling took off the street; the board proportion is measured on a 2011 photograph of a leaning pallet (width over pitch 0.545, spread 0.06) because no period pallet photograph exists in the feed; the size is the European standard, not measured.")


def story(T):
    return {
        "no": "5", "title": "Quay Street's pallets: the exact target", "summary": SUMMARY, "previews_list": "p1 (S1 cropped to the leaning pallets)",
        "rulings": {"ruling_2oct": "'skip and pallets off until real': this target is the pallet made real (a form from a photograph, no mark), to go back into the scene only after the gate, and the owed line asks for the yes", "sources_order": "no CC0 pallet exists (S4); so own work by script",
                    "content": "no person, no drink, no betting; the data scan finds none of what the rule forbids", "noai": "S1 and S2 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source",
                    "look": "weathered grey-brown timber and grime", "night": "the pallets read as pale slats and black gaps"},
        "searched": "What was searched: Poly Haven's model list (no pallet); Geograph's feed for `pallets`, `wooden pallets`, `stack of pallets`, `pallets yard` with years 1980 to 1995 and without a year (none before 2006 measurable). Wikimedia Commons was not asked.",
        "reuse": [
            ["vignette-scene.json: held pallet (off since 2 Oct), large_pallet 2.00 x 1.10, small_pallet", "slab-like stand-ins", "REPLACED", "W1"],
            ["Poly Haven models", "no pallet; wooden crates only", "NOT USED", "S4"],
            ["production/research/period-vehicles-and-props NOTE.md (pallet 1,200 x 1,000)", "the size", "KEPT as a Read number (S3 confirms it)", "oriented 1000 x 1200 after S1"],
            ["git branches (git log --all for pallet)", "none", "none to reuse", ""],
        ],
        "axes": "Axes: x along the stringers (1000), y along the deck boards (1200), z up; the stringers sit on the bottom boards and carry the top boards. Boxes; the leaning pallet is the same parts with one transform (a roll of 78 degrees about x and a lift of %.1f mm)." % TZ,
        "assembly": [
            "**Top deck**: seven boards 85 wide, 22 thick, 1200 long, at a 152.5 pitch across 1000 (gaps 67.5), arrised 1 mm, the underside of each end chamfered 15 x 15.",
            "**Stringers**: three, 95 wide, 100 high, 1000 long, along x: one flush with each board end and one in the middle (P1's middle member sits at the middle of the board length).",
            "**Bottom deck**: three boards 100 x 22 x 1200 under the stringers' crossings, at the two edges and the middle.",
            "**Fixings**: two ring-shank nails through each board into each stringer (not modelled: texture and decals); nail heads 6 mm.",
            "**PA3**: the leaning pallet rests on its lower edge on the ground and on the gable wall at its upper edge (12 degrees from the vertical); the flat pallet lies in front of its foot, touching it.",
        ],
        "own_rows": "the board width over pitch against P1's measured edges, the board and stringer counts, the pallet's size against the standard and against the scene's large pallet read from its model, the lean from the transform, the contact with the wall and the ground, no mark in the texture spec or the materials' notes, the pallets in the yard mouth against the scene's barrier and crates, and every foot on a modelled surface or on the owed floor at its stated level",
    }


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
