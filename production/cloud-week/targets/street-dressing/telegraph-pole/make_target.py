"""telegraph-pole: writes target.json and TARGET.md (cloud week 42, unit 13, family 8: a wooden telegraph pole with its wires)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B, CY, WIRE

FAMILY = "telegraph-pole"
H = 8000.0
R0, R1 = 115.0, 75.0         # radius at the ground and at the top (230 and 150 across)
SPAN = 8850.0                # pole to the east building line (z 5.125 less the pole at z -3.725)
SAME = 1400.0                # pole to its own building line (the west one)


def radius_at(z):
    return R0 + (R1 - R0) * z / H


def sag_line(a, b, sag, n=5):
    """a catenary approximated by a parabola: n+1 points from a to b with the stated sag at the middle (mm)."""
    pts = []
    for k in range(n + 1):
        t = k / n
        p = [a[i] + (b[i] - a[i]) * t for i in range(3)]
        p[2] -= 4 * sag * t * (1 - t)
        pts.append([round(v, 1) for v in p])
    return pts


def build():
    P = []
    P.append(CY("pole", (0, 0, 0), (0, 0, H), R0, "creosote_timber", r1=R1, n=20, note="creosoted pine pole, 8.0 m above the ground, 230 across at the ground, 150 at the top; the buried 1.6 m is not modelled"))
    P.append(CY("cap", (0, 0, H), (0, 0, H + 45.0), R1 + 6.0, "galvanised", r1=R1 - 25.0, note="galvanised cap, 45 high, 162 across at its foot, shed-roofed"))
    # the bracket: a plate on the pole's front at the top carrying six porcelain knobs in two rows
    P.append(B("bracket", -150.0, 150.0, -R1 - 30.0, -R1 + 1.0, H - 330.0, H - 160.0, "iron_dark", edge="corners r 6", note="distribution bracket 300 x 22 x 170, galvanised iron painted black, two bolts into the pole"))
    for i in range(2):
        for j in range(3):
            x = -100.0 + 100.0 * j
            z = H - 285.0 + 85.0 * i
            P.append(CY("knob_%d%d" % (i + 1, j + 1), (x, -R1 - 30.0, z), (x, -R1 - 76.0, z), 20.0, "porcelain", r1=15.0, note="porcelain insulator knob 40 across, 46 long"))
    # climbing steps: galvanised pegs on alternate sides from 2.4 m every 450 mm
    k = 0
    z = 2400.0
    while z <= 7200.0:
        side = 1 if k % 2 == 0 else -1
        r = radius_at(z)
        P.append(CY("step_%02d" % (k + 1), (side * (r - 20.0), 0, z), (side * (r + 130.0), 0, z), 8.0, "galvanised", note="pole step: a 16 mm peg, 150 out of the pole, alternate sides"))
        k += 1
        z += 450.0
    # the wires: four drops from knobs to brackets on the buildings' fronts
    wall_e = [B("facade_east", -9000.0, 15000.0, SPAN, SPAN + 300.0, 0.0, 9000.0, "wall_brick", note="the east parade's front (a stand-in slab)")]
    wall_w = [B("facade_west", -9000.0, 15000.0, -SAME - 300.0, -SAME, 0.0, 8500.0, "wall_brick", note="the west block's front (a stand-in slab)")]
    anchors = []
    wires = []
    tips = lambda i, j: [-100.0 + 100.0 * j, -R1 - 76.0, H - 285.0 + 85.0 * i]
    spec = [("w1", (0, 1), [-3000.0, SPAN, 6100.0], 280.0, "across to the east parade"), ("w2", (0, 2), [2500.0, SPAN, 6200.0], 270.0, "across to the east parade"),
            ("w3", (1, 0), [-4500.0, -SAME, 6500.0], 140.0, "along to the west block, a bay down the street"), ("w4", (1, 2), [3500.0, -SAME, 6600.0], 120.0, "to the west block, the other way")]
    for wid, (i, j), end, sag, note in spec:
        a = tips(i, j)
        sgn = 1 if end[1] > 0 else -1
        e = [end[0], end[1] - sgn * 0.0, end[2]]
        # the anchor: a bracket on the facade; the wire ends at its outer face
        by = end[1] - sgn * 40.0
        anchors.append(B("anchor_%s" % wid, end[0] - 40.0, end[0] + 40.0, (end[1] - 90.0) if sgn > 0 else end[1], end[1] if sgn > 0 else end[1] + 90.0, end[2] - 50.0, end[2] + 50.0, "iron_dark", note="wall bracket 80 x 90 x 100 with an insulator eye, on the eaves course"))
        e = [end[0], (end[1] - 90.0) if sgn > 0 else (end[1] + 90.0), end[2]]
        wires.append(WIRE(wid, sag_line(a, e, sag), 3.0, "wire_black", note="drop wire 6 across, black PVC over copper, " + note, hangs=True))
    P += wall_e + wall_w + anchors + wires
    ps = L.PartSet(P)
    T = {
        "family": FAMILY, "title": "Quay Street's telegraph pole with its wires",
        "units": "millimetres; angles in degrees; z up from the pavement; the bracket faces -y here; the pivot is the pole's centre at the pavement; in the street the local +y points across the street, to the east parade",
        "status": "written 13 October 2026, not yet reviewed", "sample": "TP1",
        "materials": {
            "creosote_timber": {"name": "creosoted pine, grey-brown, weathered", "srgb": [92, 78, 62], "rough": 0.85, "rough_words": "rough, checked", "metal": False, "note": "darker brown-black with tar at the foot (lowest 1.5 m), silvered grey above with vertical checks 100 to 400 long; a dark stain below the bracket where rain runs"},
            "galvanised": {"name": "galvanised steel, dull", "srgb": [128, 130, 128], "rough": 0.55, "rough_words": "matt satin", "metal": True, "note": "steps, cap: white rust, never bright"},
            "iron_dark": {"name": "bracket iron, black paint, rusted", "srgb": [30, 30, 32], "rough": 0.55, "rough_words": "semi-matt", "metal": True, "note": ""},
            "porcelain": {"name": "porcelain knob, brown glaze, dirty", "srgb": [112, 80, 56], "rough": 0.25, "rough_words": "glazed", "metal": False, "note": "a brown glaze (period) darkened with soot; cracked glaze at the neck"},
            "wire_black": {"name": "drop wire, black sheath", "srgb": [18, 18, 18], "rough": 0.6, "rough_words": "matt", "metal": False, "note": "the sheath chalks grey in sun, 6 mm across"},
            "wall_brick": {"name": "soot-blackened brick (the street's)", "srgb": [78, 64, 58], "rough": 0.9, "rough_words": "rough", "metal": False, "note": "stand-in slabs for the two facades"},
        },
        "variants": {
            "TP1": {"name": "TP1: the pole with its bracket, 6 knobs, 11 steps and four drop wires (two across the street, two to its own side) (the sample)", "parts": P, "overall_exclude": ["facade_east", "facade_west", "anchor_w1", "anchor_w2", "anchor_w3", "anchor_w4", "w1", "w2", "w3", "w4"],
                    "overall": {"w": 2 * (R0 + 130.0), "d": 266.0, "h": H + 45.0}, "overall_tol": 40.0, "contact_tol": 3.0,
                    "joins": [["cap", "pole"], ["bracket", "pole"], ["knob_11", "bracket"], ["knob_23", "bracket"], ["step_01", "pole"], ["step_11", "pole"], ["w1", "knob_12"], ["w1", "anchor_w1"], ["w2", "knob_13"], ["w2", "anchor_w2"], ["w3", "knob_21"], ["w3", "anchor_w3"], ["w4", "knob_23"], ["w4", "anchor_w4"],
                              ["anchor_w1", "facade_east"], ["anchor_w3", "facade_west"]],
                    "embeds": [["step_%02d" % i, "pole", 9.0] for i in range(1, 12)] + [["bracket", "pole", 20.0]] + [["knob_%d%d" % (i, j), "bracket", 10.0] for i in (1, 2) for j in (1, 2, 3)] + [["cap", "pole", 10.0], ["w1", "knob_12", 6.0], ["w2", "knob_13", 6.0], ["w3", "knob_21", 6.0], ["w4", "knob_23", 6.0],
                               ["w1", "anchor_w1", 6.0], ["w2", "anchor_w2", 6.0], ["w3", "anchor_w3", 6.0], ["w4", "anchor_w4", 6.0]],
                    "overlap_allow": 6.0, "faces": []},
        },
        "drawing": {"views": ["front", "left"], "sections": [{"id": "z7800", "axis": "z", "at": 7800.0}]},
        "numbers": [
            {"id": "N1", "what": "pole height above the pavement (to the cap's foot)", "value": H, "kind": "Read", "source": "Wikipedia 'Utility pole' (read raw 13 Oct): UK poles are typically 8 to 10 m long (a pole's length is marked on it); 8.0 m above the ground is the lowest of that range for a terraced street (error 500)", "tol": 500.0, "measure": {"kind": "edge", "axis": "z", "part": "pole", "side": "hi"}},
            {"id": "N2", "what": "pole diameter at the ground", "value": 2 * R0, "kind": "Judgement", "source": "230 across at the ground and 150 at the top, a stout tapered pine; P2 (Selborne) and P1 (Wilmott Close) both show a visibly tapered pole; error 30", "tol": 30.0, "measure": {"kind": "extent", "axis": "x", "part": "pole"}},
            {"id": "N3", "what": "step pitch", "value": 450.0, "kind": "Judgement", "source": "pole steps every 450 mm on alternate sides from 2.4 m (Wikipedia 'Utility pole': the UK has standard brackets up the pole as hand and foot holds); P1's pegs read about 0.5 m apart; error 60", "tol": 60.0, "measure": {"kind": "centre_dx", "axis": "z", "a": "step_01", "b": "step_02"}},
            {"id": "N4", "what": "lowest point of the across wires (at the east parade, their ends)", "value": 6100.0, "kind": "Judgement", "source": "the wires land on the first-floor eaves brackets of the east parade at 6.1 and 6.2 m (above the 5.5 m a wire must keep over a road: the regulation was not reached on a page this session); error 300", "tol": 300.0, "measure": {"kind": "wire_min_z", "parts": ["w1", "w2"]}},
            {"id": "N5", "what": "the pole's own height to the bracket's lower edge", "value": H - 330.0, "kind": "Photo", "source": "P1 (Wilmott Close): the bracket (the dark box at the top) lies in the top 8 percent of the pole; error 120", "tol": 120.0, "measure": {"kind": "edge", "axis": "z", "part": "bracket", "side": "lo"}},
        ],
        "photos": [], "sources": [], "previews": [], "checks": [], "owed": [],
    }
    ex = [n for n in ps.names if n not in T["variants"]["TP1"]["overall_exclude"]]
    lo, hi = ps.bbox(only=ex)
    T["variants"]["TP1"]["overall"] = {"w": round(float(hi[0] - lo[0]), 1), "d": round(float(hi[1] - lo[1]), 1), "h": round(float(hi[2] - lo[2]), 1)}
    T["variants"]["TP1"]["overall_tol"] = 6.0
    return T


def finish(T):
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/2630310", "read": "2026-10-13", "author": "Basher Eyre", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2011-09-21", "kind": "photograph",
         "shows": "a tall slender creosoted pole on a pavement beside a road of brick houses, tapered, a small cap, a dark bracket box at the top from which about ten wires fan out and down to houses on both sides, and climbing pegs on alternate sides; a car with a number plate on the left (outside the crop)",
         "used": True, "not_used_for": "any measured number (no scale object, the pole's foot is out of frame); the car and its plate; the colours (a bright day)", "period": "2011; the pole is a pre-1990 creosoted pine of the standard kind (they stand for 40 to 60 years)"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/1385902", "read": "2026-10-13", "author": "Basher Eyre", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2009-06-21", "kind": "photograph",
         "shows": "a pole on the pavement in a terraced street (Percy Road): the pole stands level with the front wall of the terrace, wires leave its top to houses on both sides, the pole's top reaches above the first-floor windows' heads",
         "used": True, "not_used_for": "any number; the cars and their number plates (below the crop)", "period": "2009; a terraced street of the same period as Quay Street"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/2775748", "read": "2026-10-13", "author": "Basher Eyre", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2012-01-17", "kind": "photograph",
         "shows": "a pole with a cross-bracket and wires to a cottage's eaves in a village; the wire fans leave one bracket",
         "used": False, "not_used_for": "everything (looked at only)", "period": "2012"},
        {"id": "S4", "url": "https://en.wikipedia.org/wiki/Utility_pole", "read": "2026-10-13 (raw wikitext)", "author": "Wikipedia contributors", "licence": "CC BY-SA 4.0", "taken": "n/a (a text)", "kind": "book",
         "shows": "UK poles typically 8 to 10 m long; marked with the owner, the length and the preservative; creosote was the traditional preservative; the UK sets brackets up the pole as hand and foot holds", "used": True, "not_used_for": "any picture, any owner's mark", "period": "n/a"},
        {"id": "S5", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "modular_electricity_poles (13119 x 1957 x 7000: a run of poles with crossarms on a wire layout, an electricity kind) and modular_electric_cables (2077 x 215 x 757); no British telephone pole",
         "used": False, "not_used_for": "everything: the crossarm electricity poles are not the street's telephone pole and no check of their lettering was needed", "period": "n/a"},
        {"id": "S6", "url": "tools/meshgen/blender/clutter/telegraph_pole.py and production/assets/street/clutter/telegraph-pole.glb (this repository); production/specs (the street's stand)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "29 September 2026", "kind": "own",
         "shows": "an earlier pole: 8.5 m, 0.24 across at the foot and 0.17 at the top, steps from 2.4 m every 0.45 m, a steel ring with seven 1.6 m stub wires, a number plate; stands at the west kerb, x 12 (terrace-front.py)", "used": True, "not_used_for": "its ring and its stubs", "period": "n/a"},
        {"id": "S7", "url": "https://api.geograph.org.uk/syndicator.php (terms telegraph pole, telegraph poles, wooden telegraph pole, overhead wires, poles and wires; takenyear 1975 to 1996 and without a year)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "for 1975 to 1996 about 55 photographs with poles in railway and moorland scenes, none a street pole close up; for no year about 300 'Telegraph pole in ...' photographs of 2007 to 2022 of surviving creosoted poles in streets", "used": False, "not_used_for": "measuring", "period": "n/a"},
    ]
    T["previews"] = [{"file": "p1-wilmott-close-pole-top.jpg", "source": "S1", "credit": "Basher Eyre, Geograph 2630310, CC BY-SA 2.0, 2011-09-21, cropped to the pole and its wires; the cars at the foot of the picture and their plates are below the crop", "masked": ["the cars and their number plates are below the crop (cut by script)"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True}]
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the pole stands between the lamp columns at x 28 east and 38 west: its lower 4 m catch the lantern colour (1.0, 0.25, 0.0) on the road-side face; the wires vanish at night except where a lamp is behind them"}
    T["placement"] = {
        "slot": "west side, pole centre x 33.0 m, z -3.725 (0.60 m behind the kerb's back edge), the bracket facing the street's axis (+z in the street's frame), wires to the east parade (the bays at x 30 to 36) and to the west block; the earlier pole at x 12 west is dropped",
        "x_m": 33.0, "z_m": -3.725, "kerb_back_z_m": -3.125, "set_back_mm": 600.0, "footway_mm": 2000.0, "min_clear_mm": 1000.0, "span_to_east_mm": SPAN, "to_own_side_mm": SAME, "east_building_z_m": 5.125, "lamp_columns": {"east_x_m": 28.0, "west_x_m": 38.0, "mounting_m": 5.0},
        "reasons": [
            "the earlier pole stood at x 12 on the west kerb, beside the poster wall at x 11.4 and 8 m from the lamp column at 18; x 33.0 is 5 m from both the lamp column at 28 east and at 38 west, in the span of the grocer's bay (east x 27 to 39)",
            "the pole is set back 0.60 m so its 230 mm foot leaves 2.0 - 0.60 - 0.115 = 1.29 m of footway clear (at least 1.0 m)",
            "its wires cross the street at 6.1 and 6.2 m at the east parade, never lower than 6.1 m: above the lamp columns' 5.0 m mounting height with 1.1 m to spare, and clear of the lamp column at x 28 (the wires land at x 30 and 35.5)",
            "the wires carry no lettering or mark; the real poles' owner marks are left off (S4 lists them; none is copied)",
        ],
    }
    T["wear"] = [
        "the pole: silver-grey weathered above 2 m with vertical checks, dark tar-brown and sticky below 1.5 m, a green-black damp stain at the foot, a pale rub where people lean; nails and staples (old notices, never legible) at 1.4 to 1.8 m; a split along 800 mm near the top",
        "the steps: white-rust, bent a few degrees; the lowest two missing (a seed): the climbing pegs start at 2.4 m so nobody climbs from the pavement",
        "the bracket and knobs: rust runs 100 to 300 below the bracket's bolts; bird lime on the cap and the bracket's top face; a cracked knob glaze",
        "the wires: drooping unevenly (the sag seeds 100 to 300 mm), one slack; bird lime on the lowest span; none touching any wall except at the anchors",
        "NOT shown: any owner's tag or number plate, any notice with lettering",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "the pole's top", "book": "the 29 September script: a steel band and ring with seven 1.6 m stub wires fanning from just under the top", "photo": "S1 and S2: a small capped top, a dark bracket box with insulator knobs, wires leaving from the knobs to the houses; no ring", "chose": "cap, bracket with six knobs, four full wires to the buildings"},
        {"id": "W2", "what": "the height", "book": "the script: 8.5 m", "photo": "S2: the pole's top reaches above the terrace's first-floor window heads; S4: 8 to 10 m", "chose": "8.0 m above the pavement (the buried length not modelled)"},
        {"id": "W3", "what": "the wires", "book": "the script: the wires drawn by the street to each house (short stubs only)", "photo": "S1: about ten wires reach well beyond the pole in a fan across the road", "chose": "four modelled wires of real length with sag; the street may add more by the same rule (sag 1.5 to 3.5 percent of the span)"},
    ]
    T["variants_note"] = [
        "TP1 (the sample): the pole with 4 wires (two across, two to its own side). One on the street.",
        "wear states (materials and seeds): C0 sound; C1 worn (the sample); C2 leaning 2 degrees with one wire slack (a transform seed).",
        "a pole with two more wires or one fewer is a seed on the wire list: the rule is each wire sags 1.5 to 3.5 percent of its span and keeps 5.5 m over the carriageway.",
        "NOT written: a crossarm pole (the electricity kind), a stay wire, a transformer pole: none stands in the street.",
    ]
    T["owed"] = []
    T["not_settled"] = [
        "no 1975 to 1995 street pole photograph was reached; S1 and S2 are 2009 and 2011 photographs of surviving poles; the pole's foot is out of frame in S1 and no scale object stands beside it in either, so no number is measured on pixels: the height (8.0 m) rests on the Wikipedia range, the rest is Judgement",
        "the bracket's exact shape (S1 shows a dark box about 8 percent of the pole's height; modelled as a plate with six knobs: Judgement)",
        "the minimum height of wires over a road (5.5 m is from memory: the regulation was not reached on a page)",
        "how many wires a real terrace pole carried (S1 shows about ten): four are modelled, more are a seed",
        "the pole's lean and the buried depth (not modelled)",
    ]
    T["content_rule_note"] = "no notice, no person, no vehicle plate in any preview (a statement of the content rule)."
    T["builder_notes"] = [
        "pole: a 20-sided tapered cylinder (230 at the ground, 150 at the top), UVs along its length with vertical checks in the height map; the cap and bracket separate meshes; the steps as pegs",
        "wires: tubes of 6 mm along the polylines in target.json (each point listed), the sag a parabola; hang them as splines in the engine if it prefers; the two ends are on a knob tip and on the wall bracket's face",
        "the two facades in the file are stand-ins for the street's own walls; the anchors bolt to the eaves course at the stated heights",
        "no lettering, no plate, no mark",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.0f mm" % n["value"], "tol": "+-%.0f mm" % n["tol"]})
    C += [
        {"name": "C1: each wire sags 1.5 to 3.5 percent of its span and ends on a knob and an anchor", "measure": "the polyline's deepest drop below the chord over its length", "expect": "1.5 to 3.5 percent", "tol": "exact"},
        {"name": "C2: the wires over the carriageway stay above 5.5 m", "measure": "the lowest z of the across wires", "expect": ">= 5500", "tol": "exact"},
        {"name": "C3: no part floats; every wire touches a knob and an anchor", "measure": "the contact graph", "expect": "connected", "tol": "0 floating"},
        {"name": "C4: no lettering, no plate", "measure": "textures and text", "expect": "none", "tol": "exact"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The telegraph pole is a creosoted pine pole 8.0 m above the pavement, 230 mm across at the ground tapering to 150, with a galvanised cap, a distribution bracket of six porcelain knobs just under the top, eleven climbing pegs every 450 mm on alternate sides from 2.4 m, and four black drop wires of real length (two across the street to the east parade at 6.1 and 6.2 m, two to its own side) each sagging about 3 percent of its span and never below 6.1 m; "
           "it stands on the west pavement at x 33.0, 0.60 m behind the kerb (the earlier pole at x 12 is dropped), 5 m from both lamp columns; it replaces the 29 September pole's ring and stubs, which the photographs do not show; no period street-pole photograph exists in the feed and the two 2009 and 2011 photographs have no scale, so the height rests on a written range and every other number is judged, checked for consistency only.")


def story(T):
    return {
        "no": "8", "title": "Quay Street's telegraph pole with its wires: the exact target", "summary": SUMMARY, "previews_list": "p1 (S1 cropped to the pole's upper part)",
        "rulings": {"ruling_2oct": "not a car, skip or pallet; plain street furniture", "sources_order": "no CC0 telephone pole exists (S5: electricity poles with crossarms only); so own work by script",
                    "content": "no notice or person; the data scan finds none of what the rule forbids", "noai": "S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to look at; no NoAI source",
                    "look": "grey-brown timber, black wires against a grey sky: the street's vertical grain", "night": "the wires vanish; the road-side face of the pole catches the lantern light"},
        "searched": "What was searched: Poly Haven's models (modular_electricity_poles and modular_electric_cables: electricity kinds, not used); Geograph's feed for `telegraph pole`, `telegraph poles`, `wooden telegraph pole crossarm insulators`, `overhead wires`, `poles and wires`, `telephone pole` with each year 1980 to 1995 and without a year. Wikimedia Commons was not asked.",
        "reuse": [
            ["tools/meshgen/blender/clutter/telegraph_pole.py and production/assets/street/clutter/telegraph-pole.glb (29 Sep)", "an 8.5 m pole with steps, a steel ring and seven stubs", "MENDED: the pole, taper and steps are kept (230 and 150 across, steps from 2.4 m every 0.45 m) but the height is 8.0, the ring and stubs are REPLACED by the bracket and the wires", "W1, W2, W3"],
            ["tools/art-recipes/terrace-front.py: the pole placed at the west kerb x 12", "its stand", "REPLACED by x 33.0", "the placement reasons"],
            ["Poly Haven modular_electricity_poles, modular_electric_cables", "electricity poles with crossarms", "NOT USED", "S5"],
            ["git branches (git log --all for telegraph, pole)", "the 29 September commit only", "none other", ""],
        ],
        "axes": "Axes: z up from the pavement at the pole's centre; the bracket faces -y; in the street local +y points across the street. The pole and knobs are cylinders (frustums), the bracket and anchors boxes, the wires polylines of cylinders with the sag as a parabola.",
        "assembly": [
            "**Pole**: a frustum 230 across at the ground and 150 at 8000, a galvanised cap 45 high (162 across at its foot, 100 at the top).",
            "**Bracket**: a plate 300 x 22 x 170 on the pole's front just under the top (z 7670 to 7840) with six porcelain knobs 40 across and 46 long in two rows of three at 100 centres and 85 apart.",
            "**Steps**: eleven galvanised pegs 16 across and 150 out of the pole, on alternate sides from 2400 to 6900 every 450.",
            "**Wires**: four drop wires 6 across from knobs to wall brackets 80 x 90 x 100 on the facades (the stand-in slabs): two to the east parade 8850 away at 6100 and 6200 high, sag 280 and 270, two to the west block 1400 away at 6500 and 6600, sag 140 and 120.",
            "**Edges and fixings**: bracket corners r 6; two bolts through the bracket; knob necks r 15; the pole's butt square-cut.",
        ],
        "own_rows": "each wire's sag as a percent of its span from its own polyline, the clearance over the carriageway, the taper and step pitch from the parts, the foot's footway clearance and the distance to the lamp columns",
    }


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
