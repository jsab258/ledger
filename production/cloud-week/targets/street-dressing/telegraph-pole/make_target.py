"""telegraph-pole: writes target.json and TARGET.md (cloud week 42, unit 13, family 8: a wooden telegraph pole with its wires)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B, CY, WIRE, PR

FAMILY = "telegraph-pole"
H = 8000.0
R0, R1 = 115.0, 75.0         # radius at the ground and at the top (230 and 150 across)
SPAN = 8850.0                # pole to the east building line (z 5.125 less the pole at z -3.725)
SAME = 1400.0                # pole to its own building line (the west one)
PAVEMENT_AT_POLE_M = 0.05 + 0.025 * (3.725 - 3.125)     # the footway's height above the crown at the pole (0.065)
EAVES_E = round((0.1 + 3.4 + 2.8 - PAVEMENT_AT_POLE_M) * 1000.0)   # east parade: threshold 0.1 + 3.4 + 2.8 = 6.30 m above the crown
EAVES_W = round((0.1 + 3.4 - PAVEMENT_AT_POLE_M) * 1000.0)         # west_north drawn: ONE storey of 3.4 m: 3.50 m above the crown
TAN35 = math.tan(math.radians(35.0))
OVERHANG = 300.0
RIDGE_BACK = 4000.0
ANCHOR_W = 3200.0              # the west anchors: on the eaves course, under the gutter and clear of the 300 overhang's sloping soffit (3.31 m at 90 mm out; the review said about 3.3 m); eaves 3435 above the pavement at the pole


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
    P.append(B("bracket", -150.0, 150.0, R1 - 1.0, R1 + 30.0, H - 330.0, H - 160.0, "iron_dark", edge="corners r 6", note="distribution bracket 300 x 22 x 170, galvanised iron painted black, two bolts into the pole, on the pole's street (east) face"))
    for i in range(2):
        for j in range(3):
            x = -100.0 + 100.0 * j
            z = H - 285.0 + 85.0 * i
            P.append(CY("knob_%d%d" % (i + 1, j + 1), (x, R1 + 30.0, z), (x, R1 + 76.0, z), 20.0, "porcelain", r1=15.0, note="porcelain insulator knob 40 across, 46 long"))
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
    wall_e = [B("facade_east", -9000.0, 15000.0, SPAN, SPAN + 300.0, 0.0, EAVES_E, "wall_brick", note="the east parade's front to its eaves (6.30 m above the crown, two storeys; a stand-in slab)")]
    wall_w = [B("facade_west", -9000.0, 15000.0, -SAME - 300.0, -SAME, 0.0, EAVES_W, "wall_brick", note="the west row's drawn front: ONE storey since 3 October (vignette-scene.json west_north drawn: storey 3.4 m), its eaves 3.5 m above the crown, 3435 above the pavement at the pole"),
              PR("roof_west", "yz", [(-SAME + OVERHANG, EAVES_W - OVERHANG * TAN35), (-SAME - RIDGE_BACK, EAVES_W + RIDGE_BACK * TAN35), (-SAME - RIDGE_BACK, EAVES_W + RIDGE_BACK * TAN35 - 60.0), (-SAME + OVERHANG, EAVES_W - OVERHANG * TAN35 - 60.0)], -9000.0, 15000.0, "roof_slate", note="the drawn roof plane: 35 degrees from the eaves up to the ridge 4.0 m back (about 6.3 m above the crown), its eaves overhanging 300 (a stand-in plane)")]
    anchors = []
    wires = []
    tips = lambda i, j: [-100.0 + 100.0 * j, R1 + 76.0, H - 285.0 + 85.0 * i]
    spec = [("w1", (0, 1), [-3000.0, SPAN, 6100.0], 280.0, "across to the east parade (the launderette's bay)"), ("w2", (0, 2), [2500.0, SPAN, 6100.0], 270.0, "across to the east parade (the grocer's bay)"),
            ("w3", (1, 0), [-4500.0, -SAME, ANCHOR_W], 150.0, "down to the west row's eaves course, a bay down the street"), ("w4", (1, 2), [3500.0, -SAME, ANCHOR_W], 130.0, "down to the west row's eaves course, the other way")]
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
        "units": "millimetres; angles in degrees; z up from the pavement; the bracket is on the +y face; the pivot is the pole's centre at the pavement; in the street (yaw 0) local +y is street +z: across the street, to the east parade, and the bracket faces the street's axis",
        "status": "written 13 October 2026, not yet reviewed", "sample": "TP1",
        "materials": {
            "creosote_timber": {"name": "creosoted pine, grey-brown, weathered", "srgb": [92, 78, 62], "rough": 0.85, "rough_words": "rough, checked", "metal": False, "note": "darker brown-black with tar at the foot (lowest 1.5 m), silvered grey above with vertical checks 100 to 400 long; a dark stain below the bracket where rain runs"},
            "galvanised": {"name": "galvanised steel, dull", "srgb": [128, 130, 128], "rough": 0.55, "rough_words": "matt satin", "metal": True, "note": "steps, cap: white rust, never bright"},
            "iron_dark": {"name": "bracket iron, black paint, rusted", "srgb": [30, 30, 32], "rough": 0.55, "rough_words": "semi-matt", "metal": True, "note": ""},
            "porcelain": {"name": "porcelain knob, brown glaze, dirty", "srgb": [112, 80, 56], "rough": 0.25, "rough_words": "glazed", "metal": False, "note": "a brown glaze (period) darkened with soot; cracked glaze at the neck"},
            "wire_black": {"name": "drop wire, black sheath", "srgb": [18, 18, 18], "rough": 0.6, "rough_words": "matt", "metal": False, "note": "the sheath chalks grey in sun, 6 mm across"},
            "wall_brick": {"name": "soot-blackened brick (the street's)", "srgb": [78, 64, 58], "rough": 0.9, "rough_words": "rough", "metal": False, "note": "stand-in slabs for the two facades"},
            "roof_slate": {"name": "slate roof, wet grey (the street's)", "srgb": [62, 64, 68], "rough": 0.7, "rough_words": "rough", "metal": False, "note": "stand-in plane for the west row's drawn roof"},
        },
        "variants": {
            "TP1": {"name": "TP1: the pole with its bracket, 6 knobs, 11 steps and four drop wires (two across the street, two to its own side) (the sample)", "parts": P, "overall_exclude": ["facade_east", "facade_west", "roof_west", "anchor_w1", "anchor_w2", "anchor_w3", "anchor_w4", "w1", "w2", "w3", "w4"],
                    "overall": {"w": 2 * (R0 + 130.0), "d": 266.0, "h": H + 45.0}, "overall_tol": 40.0, "contact_tol": 3.0,
                    "joins": [["cap", "pole"], ["bracket", "pole"], ["knob_11", "bracket"], ["knob_23", "bracket"], ["step_01", "pole"], ["step_11", "pole"], ["w1", "knob_12"], ["w1", "anchor_w1"], ["w2", "knob_13"], ["w2", "anchor_w2"], ["w3", "knob_21"], ["w3", "anchor_w3"], ["w4", "knob_23"], ["w4", "anchor_w4"],
                              ["anchor_w1", "facade_east"], ["anchor_w2", "facade_east"], ["anchor_w3", "facade_west"], ["anchor_w4", "facade_west"], ["facade_west", "roof_west"]],
                    "embeds": [["facade_west", "roof_west", 25.0], ["roof_west", "anchor_w3", 0.0], ["roof_west", "anchor_w4", 0.0]] + [["step_%02d" % i, "pole", 9.0] for i in range(1, 12)] + [["bracket", "pole", 20.0]] + [["knob_%d%d" % (i, j), "bracket", 10.0] for i in (1, 2) for j in (1, 2, 3)] + [["cap", "pole", 10.0], ["w1", "knob_12", 6.0], ["w2", "knob_13", 6.0], ["w3", "knob_21", 6.0], ["w4", "knob_23", 6.0],
                               ["w1", "anchor_w1", 6.0], ["w2", "anchor_w2", 6.0], ["w3", "anchor_w3", 6.0], ["w4", "anchor_w4", 6.0]],
                    "overlap_allow": 6.0, "faces": []},
        },
        "drawing": {"views": ["front", "left"], "sections": [{"id": "z7800", "axis": "z", "at": 7800.0}]},
        "numbers": [
            {"id": "N1", "what": "pole height above the pavement (to the cap's foot)", "value": H, "kind": "Read", "source": "Wikipedia 'Utility pole' (read raw 13 Oct): UK poles are typically 8 to 10 m long (a pole's length is marked on it); 8.0 m above the ground is the lowest of that range for a terraced street (error 500)", "tol": 500.0, "measure": {"kind": "edge", "axis": "z", "part": "pole", "side": "hi"}},
            {"id": "N2", "what": "pole diameter at the ground", "value": 2 * R0, "kind": "Judgement", "source": "230 across at the ground and 150 at the top, a stout tapered pine; P2 (Selborne) and P1 (Wilmott Close) both show a visibly tapered pole; error 30", "tol": 30.0, "measure": {"kind": "extent", "axis": "x", "part": "pole"}},
            {"id": "N3", "what": "step pitch", "value": 450.0, "kind": "Judgement", "source": "pole steps every 450 mm on alternate sides from 2.4 m (Wikipedia 'Utility pole': the UK has standard brackets up the pole as hand and foot holds); P1's pegs read about 0.5 m apart; error 60", "tol": 60.0, "measure": {"kind": "centre_dx", "axis": "z", "a": "step_01", "b": "step_02"}},
            {"id": "N4", "what": "lowest point of the across wires (at the east parade, their ends)", "value": 6100.0, "kind": "Judgement", "source": "the two across wires land on the east parade's eaves course at 6.1 m (its eaves are 6.30 m above the crown, so 6.215 m with the pavement at the pole; above the 5.5 m a wire must keep over a road, a figure from memory: no page for the regulation was reached, kept in not_settled); error 300", "tol": 300.0, "measure": {"kind": "wire_min_z", "parts": ["w1", "w2"]}},
            {"id": "N6", "what": "height of the west anchors above the pavement at the pole (under the drawn eaves)", "value": ANCHOR_W, "kind": "Derived", "source": "vignette-scene.json west_north.drawn: ONE storey of 3.4 m since 3 October, so the eaves stand 0.1 + 3.4 = 3.50 m above the crown, 3435 above the pavement at the pole (0.065 above the crown); the anchors (100 high) sit at 3150 to 3250, under the gutter and the overhang's soffit; error 100", "tol": 100.0,
             "measure": {"kind": "centre", "axis": "z", "part": "anchor_w3"}},
            {"id": "N7", "what": "the west row's eaves above the pavement at the pole (the drawn wall's top)", "value": EAVES_W, "kind": "Derived", "source": "vignette-scene.json west_north.drawn.storey_heights_m [3.4] plus the threshold 0.100 less the pavement's 0.065 at the pole", "tol": 2.0,
             "measure": {"kind": "edge", "axis": "z", "part": "facade_west", "side": "hi"}},
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
         "shows": "an earlier pole: 8.5 m, 0.24 across at the foot and 0.17 at the top, steps from 2.4 m every 0.45 m, a steel ring with seven 1.6 m stub wires, a number plate; stood at the west kerb, x 12 (terrace-front.py) until 3 October, when it was taken off the street", "used": True, "not_used_for": "its ring and its stubs", "period": "n/a"},
        {"id": "S7", "url": "https://api.geograph.org.uk/syndicator.php (terms telegraph pole, telegraph poles, wooden telegraph pole, overhead wires, poles and wires; takenyear 1975 to 1996 and without a year)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "for 1975 to 1996 about 55 photographs with poles in railway and moorland scenes, none a street pole close up; for no year about 300 'Telegraph pole in ...' photographs of 2007 to 2022 of surviving creosoted poles in streets", "used": False, "not_used_for": "measuring", "period": "n/a"},
    ]
    T["previews"] = [{"file": "p1-wilmott-close-pole-top.jpg", "source": "S1", "credit": "Basher Eyre, Geograph 2630310, CC BY-SA 2.0, 2011-09-21, cropped to the pole and its wires; the cars at the foot of the picture and their plates are below the crop", "masked": ["the cars and their number plates are below the crop (cut by script)"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True}]
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the pole stands between the lamp columns at x 28 east and 38 west: its lower 4 m catch the lantern colour (1.0, 0.25, 0.0) on the road-side face; the wires vanish at night except where a lamp is behind them"}
    T["placement"] = {
        "slot": "OFF THE STREET until Jafar rules (owed line O1): the pole came off the street on 3 October and this target does not put it back. The slot it would take: west side, pole centre x 32.4 m, z -3.725 (0.60 m behind the kerb's back edge), the bracket on its street face (+z in the street's frame), two wires across to the east parade (the launderette's bay x 27 to 33 and the grocer's bay x 33 to 39) and two down to the west row's eaves; the foot stands 0.32 m clear of the west shops' litter bin (x 33.0, z -3.65)",
        "on_street": False,
        "conflict": {"ruling": "DECISIONS 2026-10-03 (the proof view, step 2.1, composition, under his order of 3 October): the telegraph pole and its drop wires were taken off the street; the pole was the strongest vertical in the left third of the hook frame, with wires across the sky the sheet does not have; tools/art-recipes/terrace-front.py keeps the note THE TELEGRAPH POLE IS OFF THE STREET above CLUTTER_ADDED and says the props step (2.8) decides the street's furniture again",
                     "hook_sheet": "the Hook sheet (the governing composition, RULINGS 21 Sep) has no pole and no wires across the sky",
                     "geometry": "at x 32.4 the pole stands about 35 m from the hook camera (x -3, z -1.6, yaw 20.4), about 24 degrees left of its axis, in the left third again, 8 m tall (about 12.5 degrees of a 46 degree frame) with two wires across the street at 6.1 m against the sky, and 5 m in front of the reverse camera, on its right",
                     "status": "the pole stays off the street until he rules; the pictures he needs (the hook camera and the reverse view, each with and without the pole and its wires) are made by the builder when he asks; none was made here (nothing is built or rendered by this target)"},
        "x_m": 32.4, "z_m": -3.725, "kerb_back_z_m": -3.125, "set_back_mm": 600.0, "footway_mm": 2000.0, "min_clear_mm": 1000.0, "span_to_east_mm": SPAN, "to_own_side_mm": SAME, "east_building_z_m": 5.125, "lamp_columns": {"east_x_m": 28.0, "west_x_m": 38.0, "mounting_m": 5.0},
        "litter_bin": {"piece": "prop_swing_bin_1", "x_m": 33.0, "z_m": -3.65, "note": "the west shops' own bin (held_props DRESSING, 24 September; drawn as the litter-bin model by terrace-front.py CLUTTER_FOR_HELD)"},
        "reasons": [
            "the pole is OFF the street (3 October, see the conflict above); this slot is only where it would stand if he says yes. It is not at x 12: that pole has been off since 3 October too",
            "x 32.4 is 0.32 m clear of the west shops' litter bin (the scene's prop_swing_bin_1 at x 33.0, z -3.65, 0.33 by 0.32: the first version's x 33.0 put the 230 mm foot inside it), 5.6 m from the lamp column at x 38 west and 4.4 m from the one at x 28 east, in front of the ironmonger's window (x 30.35 to 33.70) and 1.3 m short of its shop door (x 33.70 to 34.706)",
            "the pole is set back 0.60 m so its 230 mm foot leaves 2.0 - 0.60 - 0.115 = 1.29 m of footway clear (at least 1.0 m); the shared placement rows (sd_place.py) also test it against every piece of vignette-pieces.json and the shopfronts' door zones",
            "its two across wires land on the east parade's eaves course at 6.1 m (the launderette's bay at x 29.4 and the grocer's bay at x 34.9: bay 4 is x 27 to 33, bay 5 x 33 to 39), never lower than 6.1 m: above the lamp columns' 5.0 m mounting height with 0.9 m to spare, and clear of the lamp column at x 28; the 5.5 m a wire must keep over a road is a figure from memory, no page for it was reached (not_settled)",
            "its two west wires land on the west row's eaves course at 3.2 m above the pavement (the review said about 3.3 m; at 3.3 the 100 mm anchor stands in the soffit of the roof's 300 mm overhang), under the gutter of the drawn one-storey row (eaves 3.5 m above the crown: vignette-scene.json west_north drawn), at x 27.9 and 35.9; the first version landed them at 6.5 m, 3 m above that row's eaves, in the air",
            "the wires carry no lettering or mark; the real poles' owner marks are left off (S4 lists them; none is copied)",
        ],
        "poses": [{"id": "pole", "variant": "TP1", "x_m": 32.4, "z_m": -3.725, "yaw_deg": 0.0, "zone": "west_footway",
                   "ignore_parts": ["w1", "w2", "w3", "w4", "anchor_", "facade_", "roof_west"],
                   "wires": {"anchors": [{"part": "anchor_w1"}, {"part": "anchor_w2"}, {"part": "anchor_w3"}, {"part": "anchor_w4"}], "wire_parts": ["w1", "w2", "w3", "w4"],
                             "under_eaves_min_m": 0.05, "wire_clear_m": 0.5, "over_road_min_m": 5.5}}],
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
        "TP1 (the sample): the pole with 4 wires (two across, two to its own side). One, and OFF the street until Jafar rules (owed line O1).",
        "wear states (materials and seeds): C0 sound; C1 worn (the sample); C2 leaning 2 degrees with one wire slack (a transform seed).",
        "a pole with two more wires or one fewer is a seed on the wire list: the rule is each wire sags 1.5 to 3.5 percent of its span and keeps 5.5 m over the carriageway.",
        "NOT written: a crossarm pole (the electricity kind), a stay wire, a transformer pole: none stands in the street.",
    ]
    T["owed"] = [
        {"id": "O1", "line": "Put a telegraph pole with two wires across the street back at the far end, though it came off on 3 October because the Hook sheet has none?",
         "recommended": "No, unless the hook picture shows it does not cross the sky"},
    ]
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
        "the facades in the file are stand-ins for the street's own walls: the east one runs to the parade's eaves (6.30 m above the crown), the west one is the DRAWN one-storey row (wall 3.5 m above the crown and its 35 degree roof plane); the anchors bolt to the eaves course at the stated heights, under the gutter",
        "do NOT place the pole in the street until Jafar says yes (owed line O1): it is off since 3 October",
        "no lettering, no plate, no mark",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.0f mm" % n["value"], "tol": "+-%.0f mm" % n["tol"]})
    C += [
        {"name": "C1: each wire sags 1.5 to 3.5 percent of its span and ends on a knob and an anchor", "measure": "the polyline's deepest drop below the chord over its length", "expect": "1.5 to 3.5 percent", "tol": "exact"},
        {"name": "C2: the wires over the carriageway stay above 5.5 m (a figure from memory: no page for the regulation was reached)", "measure": "the lowest z of the across wires", "expect": ">= 5500", "tol": "exact"},
        {"name": "C3: no part floats; every wire touches a knob and an anchor", "measure": "the contact graph", "expect": "connected", "tol": "0 floating"},
        {"name": "C4: no lettering, no plate", "measure": "textures and text", "expect": "none", "tol": "exact"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The telegraph pole is a creosoted pine pole 8.0 m above the pavement, 230 mm across at the ground tapering to 150, with a galvanised cap, a distribution bracket of six porcelain knobs on its street face just under the top, eleven climbing pegs every 450 mm on alternate sides from 2.4 m, and four black drop wires of real length (two across the street to the east parade's eaves course at 6.1 m, two down to the west row's eaves course at 3.2 m, each sagging about 3 percent of its span); "
           "it is OFF THE STREET: it came off on 3 October because the Hook sheet has no pole and no wires across the sky, and this target does not put it back; the slot it would take is west x 32.4, z -3.725 (0.32 m clear of the west shops' litter bin), and putting it back is one owed line for Jafar with a recommendation of No; "
           "it replaces the 29 September pole's ring and stubs, which the photographs do not show; no period street-pole photograph exists in the feed and the two 2009 and 2011 photographs have no scale, so the height rests on a written range and every other number is judged, checked for consistency only.")


def story(T):
    return {
        "no": "8", "title": "Quay Street's telegraph pole with its wires: the exact target", "summary": SUMMARY, "previews_list": "p1 (S1 cropped to the pole's upper part)",
        "rulings": {"ruling_2oct": "not a car, skip or pallet; plain street furniture", "sources_order": "no CC0 telephone pole exists (S5: electricity poles with crossarms only); so own work by script",
                    "content": "no notice or person; the data scan finds none of what the rule forbids", "noai": "S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to look at; no NoAI source",
                    "look": "grey-brown timber, black wires against a grey sky: the street's vertical grain", "night": "the wires vanish; the road-side face of the pole catches the lantern light"},
        "searched": "What was searched: Poly Haven's models (modular_electricity_poles and modular_electric_cables: electricity kinds, not used); Geograph's feed for `telegraph pole`, `telegraph poles`, `wooden telegraph pole crossarm insulators`, `overhead wires`, `poles and wires`, `telephone pole` with each year 1980 to 1995 and without a year. Wikimedia Commons was not asked.",
        "reuse": [
            ["tools/meshgen/blender/clutter/telegraph_pole.py and production/assets/street/clutter/telegraph-pole.glb (29 Sep)", "an 8.5 m pole with steps, a steel ring and seven stubs", "MENDED: the pole, taper and steps are kept (230 and 150 across, steps from 2.4 m every 0.45 m) but the height is 8.0, the ring and stubs are REPLACED by the bracket and the wires", "W1, W2, W3"],
            ["tools/art-recipes/terrace-front.py: the pole formerly placed at the west kerb x 12", "OFF THE STREET since 3 October (CLUTTER_ADDED holds only the grit bin; the note above it says so)", "NOT RESTORED here: the slot is west x 32.4 and it stays off until Jafar rules", "the conflict above, owed line O1"],
            ["Poly Haven modular_electricity_poles, modular_electric_cables", "electricity poles with crossarms", "NOT USED", "S5"],
            ["git branches (git log --all for telegraph, pole)", "the 29 September commit only", "none other", ""],
        ],
        "axes": "Axes: z up from the pavement at the pole's centre; the bracket is on the +y face; in the street (yaw 0) local +y points across the street, to the east parade. The pole and knobs are cylinders (frustums), the bracket and anchors boxes, the wires polylines of cylinders with the sag as a parabola.",
        "placement_extra": [
            "**The conflict, recorded.** DECISIONS 2026-10-03 (the proof view, step 2.1, composition, under his order of 3 October) took the telegraph pole and its drop wires off the street: laid beside the Hook sheet, the pole was the strongest vertical in the left third and its wires crossed the sky, where the sheet has neither. The Hook sheet governs composition (RULINGS 21 September). This target's first version put the pole back (at x 33.0) without saying so and without asking him; it is now off the street until he rules, and the owed line below carries the question with its recommendation. At west x 32.4 the pole would stand about 35 m from the hook camera, about 24 degrees left of its axis, in the left third again, and 5 m in front of the reverse camera. The pictures that go with the line (the hook camera and the reverse view, each with and without the pole and its wires) are made by the builder; none was made here.",
        ],
        "assembly": [
            "**Pole**: a frustum 230 across at the ground and 150 at 8000, a galvanised cap 45 high (162 across at its foot, 100 at the top).",
            "**Bracket**: a plate 300 x 22 x 170 on the pole's street face (+y) just under the top (z 7670 to 7840) with six porcelain knobs 40 across and 46 long in two rows of three at 100 centres and 85 apart.",
            "**Steps**: eleven galvanised pegs 16 across and 150 out of the pole, on alternate sides from 2400 to 6900 every 450.",
            "**Wires**: four drop wires 6 across from knobs to wall brackets 80 x 90 x 100 on the facades (the stand-in slabs): two to the east parade 8850 away at 6100 high (its eaves course, eaves 6.30 m above the crown), sag 280 and 270; two to the west row 1400 away at 3200 high, under the gutter of the drawn ONE-storey row (eaves 3435 above the pavement at the pole, a 35 degree roof plane above it), sag 150 and 130.",
            "**Edges and fixings**: bracket corners r 6; two bolts through the bracket; knob necks r 15; the pole's butt square-cut.",
        ],
        "own_rows": "each wire's sag as a percent of its span from its own polyline, the clearance over the carriageway, the taper and step pitch from the parts, the foot's footway clearance and the distance to the lamp columns, the foot and steps against every piece of the scene within 1 m, every anchor on a drawn wall under its eaves, and the pole staying off the street with its owed line",
    }


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
