"""skip: writes target.json and TARGET.md (cloud week 42, unit 13, family 6: the builder's skip)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B, PR

FAMILY = "skip"
PM = json.load(open(os.path.join(HERE, "photo_measurements.json")))["P1"]
F = PM["features"]
S = (F["bottom_y"]["px"] - 197.5) / 1200.0          # px per mm if the skip is 1200 high (its top edge at row 197.5 in the turned copy)
HALF_W = round((F["tip_right_x"]["px"] - F["tip_left_x"]["px"]) / 2 / S, 0)       # widest half length (3.0 m long)
XC = (F["tip_right_x"]["px"] + F["tip_left_x"]["px"]) / 2
HALF_B = round((XC - F["bottom_left_x"]["px"]) / S, 0)         # bottom half length
Z_RIM = round((F["bottom_y"]["px"] - F["rim_under_y"]["px"]) / S, 0)       # the rim bar's lower edge
Z_RIB = round((F["bottom_y"]["px"] - F["rim_line_y"]["px"]) / S, 0)        # the stiffening rib's centre
H = 1200.0
Z_W = 793.0                      # height of the widest line (tips at row 243 of the turned copy)
HALF_T = 1160.0                  # top half length (the upper trapezium's short edge)
W = 1700.0                       # width across (Judgement: a 6-yard builder's skip)
TH = 5.0                         # plate thickness
# the end marking (Builders' Skips (Markings) Regulations 1984, SI 1984/1933, Schedules 1 and 2; read 13 October 2026)
MK_W, MK_L, MK_T = 270.0, 380.0, 3.0   # each plate: 270 wide (140 to 280), 380 long (350 to 700), 3 thick; 270 x 380 = 1026 square cm (at least 980)
MK_GAP = 4.0                     # the plate's upper edge stands 4 mm below the top rim bar's lower edge
MK_EDGE = 5.0                    # the plate's outer edge stands 5 mm inside the end plate's outer edge (nothing projects beyond the end)
MK_ANGLE, MK_BREADTH = 45.0, 140.0     # stripe angle to the vertical (40 to 50) and breadth up the plate (133 to 147)


def build_parts():
    P = []
    prof = [[-HALF_B, 0.0], [HALF_B, 0.0], [HALF_W, Z_W], [HALF_T, H], [-HALF_T, H], [-HALF_W, Z_W]]
    P.append(PR("side_f", "xz", prof, -W / 2, -W / 2 + TH, "skip_paint", edge="folded top edge, corners r 12", note="side plate, 5 mm, hexagonal profile"))
    P.append(PR("side_b", "xz", prof, W / 2 - TH, W / 2, "skip_paint", edge="folded top edge", note="the other side plate"))
    P.append(B("floor", -HALF_B, HALF_B, -W / 2 + TH, W / 2 - TH, 0.0, TH, "skip_paint", note="floor plate 5 mm"))
    # end plates: lower sloping from the floor edge to the widest line, upper sloping inward to the top
    ang_l = math.degrees(math.atan2(Z_W, HALF_W - HALF_B))
    len_l = math.hypot(HALF_W - HALF_B, Z_W)
    ang_u = math.degrees(math.atan2(H - Z_W, HALF_W - HALF_T))
    len_u = math.hypot(HALF_W - HALF_T, H - Z_W)
    for nm, sx in (("r", 1), ("l", -1)):
        P.append({"id": "end_low_%s" % nm, "type": "box", "c": [sx * (HALF_B + HALF_W) / 2, 0.0, Z_W / 2], "s": [len_l, W - 2 * TH, TH], "rot": [0, -sx * ang_l, 0], "material": "skip_paint", "note": "lower end plate, sloping out and up to the widest line"})
        P.append({"id": "end_up_%s" % nm, "type": "box", "c": [sx * (HALF_W + HALF_T) / 2, 0.0, (Z_W + H) / 2], "s": [len_u, W - 2 * TH, TH], "rot": [0, sx * ang_u, 0], "material": "skip_paint", "note": "upper end plate, sloping in and up to the top rim"})
    # the end markings: two plates on each end's UPPER end plate (the skip has no lid and no door), upper edges level, as near the
    # outer edges as the end allows, mirror images about the skip's axis. The south end faces the hook camera: with the pose's yaw 180
    # the local +x end is the street's south end (-x). Plate frame: local x along the slope (the plate's length), y across, z out.
    dx, dz = HALF_W - HALF_T, H - Z_W
    for tag, sx in (("s", 1), ("n", -1)):
        s_rim = (Z_RIM - Z_W) / dz * len_u
        s_c = s_rim - MK_GAP - MK_L / 2.0
        tx, tz = -sx * dx / len_u, dz / len_u            # up the slope
        nx, nz = sx * dz / len_u, dx / len_u             # outward normal of the upper end plate
        off = TH / 2.0 + MK_T / 2.0
        cx = sx * HALF_W + s_c * tx + off * nx
        cz = Z_W + s_c * tz + off * nz
        for k, side in ((1, -1), (2, 1)):
            P.append({"id": "mark_%s%d" % (tag, k), "type": "box", "c": [round(cx, 2), side * (W / 2 - TH - MK_EDGE - MK_W / 2), round(cz, 2)], "s": [MK_L, MK_W, MK_T], "rot": [0, sx * ang_u, 0],
                      "material": "marking_red_yellow", "edge": "corners r 5, a 2 mm yellow border", "stripe": {"angle_deg": MK_ANGLE, "breadth_mm": MK_BREADTH, "rise": "toward the inner edge"},
                      "note": "end marking plate %d of 2 on the %s end (Schedule 1: red fluorescent stripes on yellow reflex), %d x %d x 3, upper edge 4 mm under the rim bar" % (k, "south" if tag == "s" else "north", MK_W, MK_L)})
    # top rim: a folded bar 50 wide and 86 deep along both long edges and across both ends
    for nm, y0, y1 in (("f", -W / 2 - 5.0, -W / 2 + 45.0), ("b", W / 2 - 45.0, W / 2 + 5.0)):
        P.append(B("rim_%s" % nm, -HALF_T, HALF_T, y0, y1, Z_RIM, H, "skip_paint", edge="outer corners r 8", note="top rim bar 86 deep, 50 wide, folded"))
    for nm, sx in (("r", 1), ("l", -1)):
        P.append(B("rim_end_%s" % nm, sx * HALF_T - 25.0, sx * HALF_T + 25.0, -W / 2 + 45.0, W / 2 - 45.0, Z_RIM, H, "skip_paint", note="top rim across the end"))
    # a stiffening rib along each side at the rib line
    xr = HALF_W - (Z_RIB - Z_W) * (HALF_W - HALF_T) / (H - Z_W)
    P.append(B("rib_f", -xr, xr, -W / 2 - 10.0, -W / 2, Z_RIB - 25.0, Z_RIB + 25.0, "skip_paint", note="stiffening rib 50 high, 10 proud, along the side (P1's line below the rim)"))
    P.append(B("rib_b", -xr, xr, W / 2, W / 2 + 10.0, Z_RIB - 25.0, Z_RIB + 25.0, "skip_paint"))
    # lifting lugs: two on each side near the top, 80 x 60 x 25 with a 30 hole (the hole is a texture/opacity)
    for nm, y0, y1 in (("f", -W / 2 - 25.0, -W / 2), ("b", W / 2, W / 2 + 25.0)):
        for k, x in enumerate((-990.0, 990.0)):
            P.append(B("lug_%s%d" % (nm, k + 1), x - 40.0, x + 40.0, y0, y1, 1090.0, 1150.0, "skip_paint", edge="corners r 10", note="chain lug, 80 x 60 x 25"))
    # two battery lamps on the road side at the ends (amber, lit at night in the lantern colour)
    for k, x in enumerate((-1100.0, 1100.0)):
        P.append(B("lamp_%d" % (k + 1), x - 45.0, x + 45.0, -W / 2 - 100.0, -W / 2 - 5.0, 1000.0, 1150.0, "lamp_amber", note="amber battery lamp 90 x 95 x 150 hung on the rim bar at the end"))
        P.append(B("lamp_hook_%d" % (k + 1), x - 15.0, x + 15.0, -W / 2 - 8.0, -W / 2 + 5.0, 1140.0, 1200.0, "galvanised", note="hook over the rim"))
    return P


def build():
    P = build_parts()
    T = {
        "family": FAMILY, "title": "Quay Street's skip", "units": "millimetres; angles in degrees; z up; the long side with the firm's name faces -y; the pivot is the floor's centre on the ground",
        "status": "fixes applied, not re-reviewed", "sample": "SK1",
        "materials": {
            "skip_paint": {"name": "skip yellow, chalked and dented", "srgb": [226, 188, 24], "rough": 0.6, "rough_words": "semi-matt", "metal": True, "note": "steel under paint: dents, chipped to rust at the rim, mud to knee height, black rubber and tar splashes; yellow in the sample (variants: orange, blue-green)"},
            "lamp_amber": {"name": "amber battery lamp lens", "srgb": [220, 120, 20], "rough": 0.2, "rough_words": "glossy", "metal": False, "note": "emissive at night: the lantern colour (1.0, 0.25, 0.0) linear; off by day"},
            "galvanised": {"name": "galvanised hook", "srgb": [140, 142, 140], "rough": 0.5, "rough_words": "satin", "metal": True, "note": ""},
            "marking_red_yellow": {"name": "end marking plate: red fluorescent stripes on yellow reflex-reflecting sheet", "srgb": [243, 205, 24], "stripe_srgb": [226, 52, 36], "rough": 0.3, "rough_words": "smooth, retro-reflective sheet", "metal": False,
                                   "note": "the yellow is the plate's reflex ground (a little brighter and cleaner than the skip's chalked yellow), the red the fluorescent stripes: 45 degrees to the vertical, 140 mm breadth up the plate, rising toward the plate's inner edge (the two plates of an end make a chevron pointing up); the stripe pattern is a texture (numbers in marking); the colours are Judgement from the regulation's words; scuffed, dirt-streaked, the red faded toward orange-red, one plate cracked across a corner"},
        },
        "variants": {
            "SK1": {"name": "SK1: a 6-yard builder's skip, 3.0 m long, yellow, empty (the sample)", "parts": P, "overall": {"w": 2 * HALF_W, "d": W + 20.0, "h": H}, "overall_tol": 12.0, "overall_exclude": ["lamp_1", "lamp_2", "lamp_hook_1", "lamp_hook_2", "lug_f1", "lug_f2", "lug_b1", "lug_b2", "mark_s1", "mark_s2", "mark_n1", "mark_n2"],
                    "joins": [["side_f", "floor"], ["side_b", "floor"], ["end_low_r", "floor"], ["end_low_l", "floor"], ["end_up_r", "end_low_r"], ["end_up_l", "end_low_l"], ["rim_f", "side_f"], ["rim_b", "side_b"], ["rim_end_r", "rim_f"],
                              ["rim_end_l", "rim_b"], ["rib_f", "side_f"], ["rib_b", "side_b"], ["lug_f1", "side_f"], ["lug_b2", "side_b"], ["lamp_hook_1", "rim_f"], ["lamp_1", "lamp_hook_1"], ["mark_s1", "end_up_r"], ["mark_s2", "end_up_r"], ["mark_n1", "end_up_l"], ["mark_n2", "end_up_l"]],
                    "embeds": [["rim_f", "side_f", 5.0], ["rim_b", "side_b", 5.0], ["rim_end_r", "end_up_r", 5.0], ["rim_end_l", "end_up_l", 5.0], ["rim_end_r", "side_f", 5.0], ["rim_end_l", "side_b", 5.0], ["rim_end_r", "side_b", 5.0], ["rim_end_l", "side_f", 5.0],
                               ["end_low_r", "side_f", 5.0], ["end_low_r", "side_b", 5.0], ["end_low_l", "side_f", 5.0], ["end_low_l", "side_b", 5.0], ["end_up_r", "side_f", 5.0], ["end_up_r", "side_b", 5.0], ["end_up_l", "side_f", 5.0], ["end_up_l", "side_b", 5.0],
                               ["floor", "side_f", 5.0], ["floor", "side_b", 5.0], ["rib_f", "lug_f1", 5.0], ["lamp_hook_1", "rim_f", 8.0], ["lamp_hook_2", "rim_f", 8.0], ["lamp_1", "lamp_hook_1", 8.0], ["lamp_2", "lamp_hook_2", 8.0]],
                    "overlap_allow": 10.0,
                    "faces": [{"id": "side plate", "o": [-1000.0, -W / 2 - 1.0, 300.0], "u": [1, 0, 0], "v": [0, 0, 1], "n": [0, -1, 0], "nu": 2000.0, "nv": 600.0, "depth": 10.0, "blockers": ["side_f"]}]},
        },
        "drawing": {"views": ["front", "left", "plan"], "sections": [{"id": "x0", "axis": "x", "at": 0.0}, {"id": "y0", "axis": "y", "at": 0.0}]},
        "numbers": [
            {"id": "N1", "what": "overall height", "value": H, "kind": "Judgement", "source": "1200 mm: the research note and the scene's earlier skip give about 1.2 m; it also fixes P1's scale (the skip's height from its top edge row 197.5 to its foot row 331.5 = 134 px, 0.1117 px per mm); error 100", "tol": 100.0, "measure": {"kind": "bbox", "axis": "z"}},
            {"id": "N2", "what": "widest length (at the junction of the two trapezia)", "value": 2 * HALF_W, "kind": "Photo", "source": "P1 tip_left_x %.1f to tip_right_x %.1f = %.1f px at 0.1117 px per mm (the height is the assumed unit); error 150" % (F["tip_left_x"]["px"], F["tip_right_x"]["px"], F["tip_right_x"]["px"] - F["tip_left_x"]["px"]), "tol": 150.0, "measure": {"kind": "extent", "axis": "x", "part": "side_f"}},
            {"id": "N3", "what": "floor length (the bottom edge)", "value": 2 * HALF_B, "kind": "Photo", "source": "P1 bottom_left_x %.1f from the centre %.1f = %.0f mm half length (the right corner is faint; symmetry assumed); error 120" % (F["bottom_left_x"]["px"], XC, HALF_B), "tol": 120.0, "measure": {"kind": "extent", "axis": "x", "part": "floor"}},
            {"id": "N4", "what": "rim bar depth", "value": H - Z_RIM, "kind": "Photo", "source": "P1 rim_under_y 207.1 below the top edge 197.5: 9.6 px = 86 mm; error 20", "tol": 20.0, "measure": {"kind": "extent", "axis": "z", "part": "rim_f"}},
            {"id": "N5", "what": "stiffening rib centre above the floor", "value": Z_RIB, "kind": "Photo", "source": "P1 rim_line_y 228.4 above the foot 331.5: 103.1 px = 923 mm; error 40", "tol": 40.0, "measure": {"kind": "centre", "axis": "z", "part": "rib_f"}},
            {"id": "N6", "what": "height of the widest line", "value": Z_W, "kind": "Photo", "source": "P1 tips at row 243 of the turned copy: (331.5 - 243) / 0.1117 = 792; error 50", "tol": 50.0, "measure": {"kind": "edge", "axis": "z", "part": "end_low_r", "side": "hi"}},
            {"id": "N7", "what": "width across the skip (between the side plates' outer faces)", "value": W, "kind": "Judgement", "source": "a 6-yard builder's skip is about 1.7 m wide; the photograph is a side view and gives none; error 150", "tol": 150.0, "measure": {"kind": "extent", "axis": "y", "part": "floor", "plus": 10}},
        ],
        "photos": [], "sources": [], "previews": [], "checks": [], "owed": [],
    }
    T["numbers"][3]["value"] = H - Z_RIM
    T["numbers"][6] = {"id": "N7", "what": "width across the skip (the floor plus the side plates)", "value": W - 2 * TH, "kind": "Judgement", "source": "a 6-yard builder's skip is about 1.7 m wide over its side plates; the photograph is a side view and gives none; error 150", "tol": 150.0, "measure": {"kind": "extent", "axis": "y", "part": "floor"}}
    # source errors: the height 1200 is an assumption (+-100, 8.3 percent) and every other photographed length is scaled on it, so each
    # carries at least that relative error as what the SOURCE can tell; the builder's tolerance (tol) stays a separate field
    for n in T["numbers"]:
        if n["id"] == "N1":
            n["source_error"] = 100.0
        elif n["id"] in ("N2", "N3", "N4", "N5", "N6"):
            n["scaled_on"] = "N1"
            n["source_error"] = max(n["tol"], math.ceil(100.0 / H * n["value"] / 5.0) * 5.0)
            n["kind"] = "Photo, scaled on the assumed height"
        elif n["id"] == "N7":
            n["source_error"] = n["tol"]
    refs = {"rim_under_y": ("y", "rim_f", "lo"), "rim_line_y": ("y", "rib_f", "lo", {"add": 25.0}), "bottom_y": ("y", "floor", "lo"),
            "tip_left_x": ("x", "side_f", "lo"), "tip_right_x": ("x", "side_f", "hi"), "bottom_left_x": ("x", "floor", "lo")}
    ph = SF.photo_entry(PM, "P1", "S1", "SK1", refs, ["rim_f", "floor"], anchors=("rim_under_y", "bottom_y"), boundary=("tip_left_x", "tip_right_x", "bottom_left_x", "bottom_y"),
                        fit_top="rim_under_y", fit_bottom="bottom_y", centre_from=lambda FF: (FF["tip_left_x"]["px"] + FF["tip_right_x"]["px"]) / 2.0, min_tol=6.0, file="P1rot.jpg",
                        method="the photograph is turned 7.2 degrees about (730, 270) because the skip stands tilted on a slope (the top rim's slope), then each edge is the strongest grey-level step inside the recorded window on the turned copy; the scale is fitted on the one span from the rim bar's lower edge to the foot (124.4 px for 1114 mm if the skip is 1200 high: 0.1117 px per mm); the height of 1200 is Judgement (it sets the scale), so the proportions are checked and the absolute lengths are judged; the right bottom corner and the top corners are against fence wire and sky and faint, so they are not used; the tolerance is the measured spread times 3 plus 2 px, at least 6 px (54 mm)")
    ph["fit"]["top_ref"] = {"part": "rim_f", "side": "lo"}
    ph["fit"]["bottom_ref"] = {"part": "floor", "side": "lo"}
    ph["fit"]["centre_parts"] = ["side_f"]
    ph["rotated"] = PM["rotated"]
    T["photos"].append(ph)
    return T


def finish(T):
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/6875634", "read": "2026-10-13", "author": "Ian Taylor", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2021-06-15", "kind": "photograph",
         "shows": "a yellow builder's skip standing tilted on a grass slope, seen from its long side: the hexagonal side profile (two stacked trapezia, widest at about two thirds up), a folded top rim, a stiffening rib below it, two lifting lugs near the top, a stencilled firm's name and telephone number; behind it a temporary fence panel; two walkers and a dog on the left (outside the crop)",
         "used": True, "not_used_for": "absolute size (no scale object; the height 1200 is assumed), the firm's name and number (painted out), the people, the fence", "period": "2021; the builder's skip's shape has not changed since the 1960s (cantilever-lorry skips)"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/1144136", "read": "2026-10-13", "author": "Rossographer", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2009-01-26", "kind": "photograph",
         "shows": "a yellow skip from its end in a terraced street at the kerb: the end plates slope inward, a painted FILL LEVEL line below the rim, a telephone number, traffic cones at the end",
         "used": True, "not_used_for": "any number (oblique, with a number and a house for sale in the frame); the number and the street (not previewed)", "period": "2009"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/1116404", "read": "2026-10-13", "author": "David Wright", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2009-01-11", "kind": "photograph",
         "shows": "an orange skip beside a kerb on double yellow lines at a crossroads with a firm's name on its side (the orange colour variant)", "used": False, "not_used_for": "everything (looked at only: it carries a firm's name)", "period": "2009"},
        {"id": "S4", "url": "https://en.wikipedia.org/wiki/Skip_(container)", "read": "2026-10-13 (raw wikitext)", "author": "Wikipedia contributors", "licence": "CC BY-SA 4.0", "taken": "n/a (a text)", "kind": "book",
         "shows": "the skip's side is a trapezium or two stacked trapezia, the smaller edge at the bottom of the lower one and at the top of the upper one; usually two lugs on each side for chains; drop-door skips; sizes from 2 to 40 cubic yards (mini to roll-on)", "used": True, "not_used_for": "any picture", "period": "n/a"},
        {"id": "S5", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "no skip; concrete_road_barrier, industrial_storage_cart, plastic_container: none a skip", "used": False, "not_used_for": "everything: no CC0 skip exists, so it is made by script", "period": "n/a"},
        {"id": "S6", "url": "production/specs/vignette-scene.json and production/research/period-vehicles-and-props (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the held skip (stood at x 22.5 in the west carriageway, off since 2 October: 'a granite box in the carriageway'); the research note's skip 'about 2.6 x 1.5 x 1.2 m'; two cones at x 21.3 and 23.7 at 0.35 m from the kerb; a crowd-control barrier across the yard mouth", "used": True, "not_used_for": "the box shape", "period": "n/a"},
        {"id": "S8", "url": "https://www.legislation.gov.uk/uksi/1984/1933/made", "read": "2026-10-13 (the made text and the original print PDF, page 5686 for Schedule 1's diagram)", "author": "the Secretary of State for Transport and the Secretary of State for Wales (a statutory instrument: The Builders' Skips (Markings) Regulations 1984, SI 1984/1933)",
         "licence": "Open Government Licence v3.0 (legislation.gov.uk)", "taken": "1984-12-11 (made; in force 21 January 1985; the marking required from 1 January 1986)", "kind": "book",
         "shows": "every end of a builder's skip any part of which stands on a highway other than a footway or verge must from 1 January 1986 carry a marking of two plates of equal size and shape (BS AU 152: 1970, the rear marking plate standard), red fluorescent stripes and yellow reflex-reflecting ground as Schedule 1's diagram shows (each plate 140 to 280 wide, 350 to 700 long, area at least 980 square cm, stripes 40 to 50 degrees to the vertical and 133 to 147 broad, rising toward the inner edge); Schedule 2 places them: as near an outer edge as the skip allows, innermost edges equidistant from the skip's axis, upper edges level with each other and not lower than the skip's upper edge unless the construction needs it, at most 1.5 m above the ground, never on a lid, on a door only if nowhere else will do",
         "used": True, "not_used_for": "BS AU 152 itself (not freely readable: the plate's own small marking is a Judgement); no picture", "period": "in force in 1990: a skip in Quay Street's road carries these plates on both ends"},
        {"id": "S7", "url": "https://api.geograph.org.uk/syndicator.php (terms skip, skip hire, builders skip, skip in the street; takenyear 1980 to 1996 and without a year)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)", "taken": "1980 to 1996 searched", "kind": "search record",
         "shows": "no skip photograph before 1998 (a 1998 hit is a house named Skipness); about 100 photographs from 2009 on, most of Skip Bridge (a place name)", "used": False, "not_used_for": "measuring", "period": "n/a"},
    ]
    T["previews"] = [
        {"file": "p1-grass-skip-side-elevation.jpg", "source": "S1", "credit": "Ian Taylor, Geograph 6875634, CC BY-SA 2.0, 2021-06-15, turned 7.2 degrees and cropped to the skip; the stencilled firm's name and telephone number painted out; the walkers are outside the crop",
         "masked": ["the firm's name and telephone number (painted out)"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
        {"file": "s8-si1984-1933-schedule-1.jpg", "source": "S8", "credit": "The Builders' Skips (Markings) Regulations 1984, SI 1984/1933, Schedule 1 (the made version's print page 5686, legislation.gov.uk, Open Government Licence v3.0), cropped to the diagram of the two marking plates and its notes (a) to (e)",
         "masked": ["nothing to mask: a printed statutory diagram, no person, no firm"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
        {"file": "p1-grass-skip-target-on-photo.jpg", "source": "S1", "credit": "overlay of this target's side elevation (red) on the same crop, the scale fitted on the height from the rim's lower edge to the foot, measured edges in green; same masks",
         "masked": ["as p1"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
    ]
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "a skip in the highway carries two battery lamps (amber) at its ends; they glow in the lantern colour (1.0, 0.25, 0.0) linear, emissive 4 on a 90 mm lens; the yellow paint under the lantern reads orange-brown and the dents catch the glow"}
    T["text"] = {"hire_firm": "TIDEWAY SKIP HIRE", "number_line": "TEL. 0632 960142", "stencil": "stencilled capitals on the side plate between z 450 and 760, black, name 120 mm tall, number 90 mm tall, centred; a second line 'FILL LEVEL' 40 mm tall painted on the end plates 120 below the rim",
                 "note": "invented hire firm (a fictional placeholder until the town mints one) and an invented British number: an STD code of the period with the exchange 960, a block no exchange was given (the range British drama has used); no real firm; the stencil is a texture; the name sits on the side facing the road and again on the other side; none on the ends but FILL LEVEL"}
    T["marking"] = {
        "regulation": {"title": "The Builders' Skips (Markings) Regulations 1984 (SI 1984/1933), made 11 December 1984 under s.139(4) of the Highways Act 1980, in force 21 January 1985; the marking required from 1 January 1986", "url": "https://www.legislation.gov.uk/uksi/1984/1933/made", "kind": "Read",
                       "read": "2026-10-13: the made text and the original print PDF (Schedule 1's diagram, page 5686)",
                       "plate_width_mm": [140.0, 280.0], "plate_length_mm": [350.0, 700.0], "stripe_angle_deg": [40.0, 50.0], "stripe_breadth_mm": [133.0, 147.0], "min_area_cm2": 980.0,
                       "upper_edge_max_above_ground_mm": 1500.0, "plates_per_end": 2, "standard": "BS AU 152: 1970 (rear marking plates for vehicles); the Standard itself was not read"},
        "chosen": {"plate_width_mm": MK_W, "plate_length_mm": MK_L, "plate_thickness_mm": MK_T, "area_cm2": MK_W * MK_L / 100.0, "stripe_angle_deg": MK_ANGLE, "stripe_breadth_mm": MK_BREADTH, "stripe_period_mm": 2 * MK_BREADTH,
                   "stripe_rise": "toward the plate's inner edge (the two plates of an end make a chevron pointing up, as Schedule 1's two halves do)", "red": "fluorescent, srgb (226, 52, 36)", "yellow": "reflex-reflecting, srgb (243, 205, 24)",
                   "pattern": "plate frame: v down from the upper edge, d from the inner edge; red where ((v - d x tan 45) - 70) mod 280 lies within 70 of zero, yellow elsewhere; the first stripe at the upper edge is partial, as in the diagram; a 2 mm yellow border",
                   "size_reason": "the upper end plate is 535 mm along its slope and 422 mm of it lie under the rim bar's lower edge: a 380 long plate fits with 38 mm to spare, 270 wide takes 1026 square cm, over the 980 minimum",
                   "mark_text": "the Standard's paragraph 5 marking (BS AU 152 and a maker's mark) was not read: a small 'BS AU 152' in 8 mm capitals on the lower yellow margin is a Judgement, with no maker's mark"},
        "diagram": "Schedule 1 shows two halves, mirror images: stippled stripes (red fluorescent) alternate with unstippled (yellow reflex), 40 to 50 degrees to the vertical, 133 to 147 broad measured up the plate; each half 140 to 280 wide and 350 to 700 long; the stripes rise toward the inner edges, so the two plates of an end make a chevron pointing up",
    }
    T["placeholders"] = [
        {"name": "Tideway Skip Hire", "marked": "fictional placeholder", "kind": "the hire firm's name on the stencil", "where": "text.hire_firm, the stencil's separate texture layer", "until": "the town mints the firm (handover H1)"},
        {"name": "0632 960142", "marked": "fictional placeholder", "kind": "the firm's telephone number on the stencil", "where": "text.number_line", "until": "the town mints the firm and a number in its own code (handover H1)"},
    ]
    T["handovers"] = [
        {"id": "H1", "line": "For the town: mint the skip hire firm's name and a telephone number in the town's own STD code for the skip's stencil (now the placeholders 'Tideway Skip Hire' and 'TEL. 0632 960142', kept in the stencil's own texture layer and never shown on Jafar's page)."},
    ]
    T["placement"] = {
        "slot": "west carriageway, the long side parallel to the kerb, centre x 22.5 m (in front of the yard mouth, x 21 to 24), 0.30 m from the kerb face (the skip's near side at z -2.70, its centre line at z -1.85), the firm's name and the lamps on the road side (street +z); its floor lies on the road's camber, tilted 1.4 degrees with the kerb side low; the south end (street -x) faces the hook camera with two striped marking plates on each end",
        "x_m": 22.5, "z_near_m": -2.70, "z_centre_m": -1.85, "kerb_face_z_m": -3.0, "gap_to_kerb_mm": 300.0, "lane_mm": 3000.0, "min_pass_mm": 2800.0, "yard_x_m": [21.0, 24.0],
        "cones_scene_x_m": [21.3, 23.7], "cones_scene_z_m": -3.35,
        "cones_optional": {"x_m": [20.7, 24.3], "z_m": -1.85, "note": "if cones are wanted at the skip's road ends they stand in the carriageway on the skip's centre line, 0.2 to 0.3 m beyond its ends; the scene's own cones stay where they are (on the west footway); the cones are off the drawn street since 3 October (terrace-front.py HELD_PROPS_OFF_STREET)"},
        "tilt": {"deg": 1.43, "low_side": "the kerb side (z -2.70)", "drop_across_mm": 42.0, "rule": "the floor lies on the road's camber (1 in 40) and tilts with it, so the builder neither sinks one side into the road nor floats the other (42 mm across the 1690 width)"},
        "accent": {"hook_frame_share": 0.0036, "ceiling": 0.078, "method": "pinhole projection of the skip's parts at its pose into the hook camera (x -3, z -1.6, eye 2.2 m above the crown, yaw 20.4, pitch -3.4 up, 46 degrees vertical, 16:9), nothing in front hiding it, so an upper bound; a projection of this target's own parts, not a render",
                   "verdict": "about 0.4 percent of the frame against the 7.8 percent ceiling of art-direction R-B4 (the frame's share above saturation 0.6): small, so the sample stays yellow; the orange and faded blue-green stay colour variants"},
        "reasons": [
            "the 2 October ruling took the skip off the street 'until real'; the scene's story ('the yard is shut': a barrier across the mouth, cones, a skip) places it before the yard mouth, one event with the pallets behind the barrier (the pallets target)",
            "the near lane is 3.0 m: a skip %d mm wide at 0.30 m from the kerb leaves 3.0 - 0.30 - 1.70 = 1.0 m in its own lane and the whole 3.0 m other lane: the street stays passable (2.8 m is the least a bus needs; cars are off in any case); the shared placement rows measure the widest free width across the road" % W,
            "its length is 3.0 m, the width of the yard mouth: it fills the street frontage of the gap without crossing a shop front",
            "THE CONES DO NOT MOVE. The first version moved the scene's two cones to x 20.7 and 24.3 on a misreading: they stand on the west FOOTWAY, 0.35 m behind the kerb face (vignette-pieces.json prop_traffic_cone_01_0 and _02_0 at z -3.35), not inside the skip's length; the skip (z -2.70 to -1.00) does not touch them, and cones moved to x 20.7 and 24.3 at that depth would stand inside the bollards there (prop_decorative_bollard_02_0 and _1, z -3.40 to -3.60). If cones are wanted at the skip's road ends they go at z -1.85, in the carriageway on the skip's centre line, at x 20.7 and 24.3; the cones are off the drawn street since 3 October",
            "a skip on the highway needs lamps at night and a permit: the two amber lamps are on the skip; the double yellow lines (0.25 m from the kerb) lie under it: a skip on the lines is a street fact (a permit, Judgement)",
            "a skip any part of which stands on the carriageway carried, from 1 January 1986, a marking of two striped plates on each end (SI 1984/1933, S8): the south end faces the hook camera, about 24 m away and 20 degrees off its axis, well inside the frame, so four striped plates are among the first things a 1990 skip in the road shows; they are on the upper end plates, level with each other (their upper edges 4 mm under the rim bar, about 1.1 m above the road), 270 wide, 380 long, 5 mm inside the end's outer edges and mirror images about the skip's axis",
            "the floor lies on the road's camber: 1 in 40 is 1.43 degrees, the kerb side low, 42 mm across the 1690 width",
        ],
        "poses": [{"id": "skip", "variant": "SK1", "x_m": 22.5, "z_m": -1.85, "yaw_deg": 180.0, "zone": "west_carriageway", "front_faces": "+z", "walk_check": False, "head_check": False}],
        "hook_camera": {"x_m": -3.0, "z_m": -1.6, "eye_y_m": 2.2, "yaw_deg": 20.4, "pitch_deg": -3.4, "fov_vertical_deg": 46.0},
    }
    T["wear"] = [
        "yellow paint chalked, dented along the rim and the lower plates (a hundred dents 20 to 80 mm, seeds), chipped to rust at the rim's top edge and the lugs, rust runs 30 to 120 mm below the chipped places",
        "mud and cement to knee height (a mask from the floor up, 0.4 m on the side plates), black tar and bitumen splashes, lime-white splashes",
        "the stencilled name worn, a few letters chipped; the paint on the end plates scraped by the lorry's chains",
        "the lamps: dirty lenses, one cracked (a seed)",
        "the four end marking plates: scuffed and dirt-streaked (the regulation asks them to be clean and efficient, so a dirty one is a street fact, not the target), the fluorescent red faded toward orange-red, one plate cracked across a corner (a seed), mud splashes on the lowest 100 mm",
        "contents: empty in the sample (a variant carries a heap of plasterboard, bricks and timber lath, never a person or a drink container: a seed in the builder's decals)",
        "NOT shown: a real firm's name or number, a person, any drink container",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "the skip's size and shape", "book": "the research note and the scene: about 2.6 x 1.5 x 1.2 m, a plain box ('a granite box in the carriageway')", "photo": "S1: a hexagonal side profile, widest at 793 up, 3.0 m long at its widest if 1.2 m high (the ratio 2.5 holds in S1), bottom 1.85 m long, top 2.3 m long", "chose": "the S1 profile at 3015 x 1200 (a 6-yard); a mini skip is a scale of the same profile (variant)"},
        {"id": "W2", "what": "the rim", "book": "none", "photo": "S1: a folded rim bar about 86 mm deep, a stiffening rib line 190 below it (923 above the floor)", "chose": "rim 86 deep and 50 wide, a rib 50 high 10 proud"},
        {"id": "W3", "what": "the lugs", "book": "S4: usually two on each side", "photo": "S1: two small lugs near the top at about x -990 and +990", "chose": "two on each side at x -990 and +990, 80 x 60 x 25"},
        {"id": "W4", "what": "the end markings", "book": "the first version: none (it named lamps and a permit for a skip on the highway and nothing else)", "photo": "S2 shows a skip from its end in a terraced street with its end plates and a FILL LEVEL line; the law (S8, Schedules 1 and 2) puts two striped plates on each end of a skip standing on a highway from 1 January 1986", "chose": "two plates 270 x 380 on each end's upper end plate, red fluorescent stripes on yellow reflex, 45 degrees, 140 broad, rising toward the inner edges (the review of 13 October found their absence)"},
    ]
    T["variants_note"] = [
        "SK1 (the sample): the 6-yard skip, yellow, empty, on the road at the yard mouth.",
        "colours: yellow (the sample), orange, blue-green; each firm paints all its skips one colour.",
        "SK2 (not written as geometry): the 4-yard skip is SK1 scaled by 0.8 in x and y and 0.85 in z; its lugs move with it.",
        "contents (seeds, never a mesh in the target): empty; half full of rubble; full with a heap above the rim. Nothing else.",
    ]
    T["owed"] = [
        {"id": "O1", "line": "Put the skip back in the road before the yard, with its two lamps lit at night, the striped end plates the law asked for, and a made-up hire firm's name on it, now that it is a real skip?", "recommended": "Yes, put it back"},
    ]
    T["not_settled"] = [
        "absolute size: S1 has no scale object, the height 1200 is assumed and sets 0.1117 px per mm; the profile's proportions are measured, its lengths follow",
        "the width across (1700, Judgement: no end view was measured; S2's end view is oblique)",
        "the right bottom corner and the top corners (faint against fence and sky in S1): the profile is taken symmetric about the centre of the widest line",
        "whether a skip stood on Quay Street in 1990 (the scene's story says one did; the ruling put it back as soon as it is real)",
        "the marking plates' own colours and small mark: the regulation names red fluorescent and yellow reflex-reflecting and the Standard BS AU 152: 1970, which was not read; the sRGB values and the small 'BS AU 152' marking are Judgements",
        "the skip's share of the hook frame is a projection of the target's own parts with nothing hiding it, not a render",
        "the lamps' exact fixing (a hook over the rim: Judgement)",
    ]
    T["content_rule_note"] = "no firm's real name, no person, no drink container in the contents (a statement of the content rule)."
    T["builder_notes"] = [
        "build by script: the two side plates are prisms of the hexagonal profile in the x-z plane (5 mm), the floor and the four end plates are boxes (the end plates' rotations are in target.json), the rim a folded bar along the top edge",
        "texture: yellow paint with the stencil on the side plate as a SEPARATE texture layer, blank in any picture for his page (the firm and the number are fictional placeholders in text.hire_firm and text.number_line); the marking plates have their own texture (see marking); no real mark",
        "lamps: emissive amber (1.0, 0.25, 0.0) linear at night, off by day; the lens 90 across",
        "keep the hexagonal profile exact: its widest line is at 793 and its bottom edge shorter than its top",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.0f mm" % n["value"], "tol": "+-%.0f mm" % n["tol"]})
    C += [
        {"name": "C1: the side profile has six corners, the widest line at 793 up", "measure": "the side plate's outline", "expect": "hexagon", "tol": "+-50 mm"},
        {"name": "C2: no part floats; the end plates meet the floor and the sides", "measure": "the contact graph", "expect": "connected", "tol": "0 floating"},
        {"name": "C3: the side plate is closed from the side at 0, 30 and 45 degrees", "measure": "rays at the side plate", "expect": "0 get through", "tol": "exact"},
        {"name": "C4: the name and number are the invented ones", "measure": "the stencil text layer", "expect": "the placeholder firm and a British number of the form TEL. 0632 960nnn (no 555)", "tol": "exact"},
        {"name": "C6: both ends carry two marking plates", "measure": "count the marking plates on each end plate; their size, stripe angle and breadth, their upper edges", "expect": "2 + 2 plates, 270 x 380 (140 to 280 by 350 to 700, area at least 980 square cm), stripes 45 degrees (40 to 50), breadth 140 (133 to 147), upper edges level, under 1500 above the ground", "tol": "exact"},
        {"name": "C5: two lamps lit at night in the lantern colour", "measure": "emissive colour", "expect": "(1.0, 0.25, 0.0)", "tol": "+-0.02"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The skip is a 6-yard builder's skip with the hexagonal side profile of the photograph (3015 mm long at its widest line 793 up, 1850 along the floor, 2320 along the top, 1200 high, 1700 wide), 5 mm plates, an 86 mm folded top rim, a stiffening rib at 923, four chain lugs, two amber lamps lit in the lantern colour at night, two red-and-yellow striped marking plates on each end (the plates the Builders' Skips (Markings) Regulations 1984 required from 1 January 1986: 270 x 380 mm, stripes at 45 degrees and 140 mm broad) and the invented stencil of a placeholder hire firm and a British telephone number, yellow; it stands in the west carriageway before the yard mouth at x 22.5, 0.30 m off the kerb on the road's camber, "
           "which puts the 2 October ruling's skip back as a real skip (owed: one line); the scene's two cones stay where they are (on the west footway; the first version's move of them was a misreading); the profile is measured on a 2021 side view (turned 7.2 degrees to level it) and the scale is the assumed height of 1.2 m, so the lengths are judged; no period skip photograph exists in the feed.")


def story(T):
    return {
        "no": "6", "title": "Quay Street's skip: the exact target", "summary": SUMMARY, "previews_list": "p1 (S1 turned and cropped, the firm's name painted out), its target-on-photo overlay, and s8 (Schedule 1 of the 1984 Regulations: the marking plate diagram)",
        "rulings": {"ruling_2oct": "'skip and pallets off until real': this target is the skip made real; it goes back to the street only after the gate, and the owed line asks for the yes", "sources_order": "no CC0 skip exists (S5); so own work by script from S1's profile",
                    "content": "no person, no drink container; an invented firm and number; the data scan finds none of what the rule forbids", "noai": "S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source",
                    "look": "yellow paint, grime, dents and mud: a saturated patch in a grey street", "night": "its two amber lamps are the only lit things on it"},
        "searched": "What was searched: Poly Haven's model list (no skip); Geograph's feed for `skip`, `skip hire`, `builders skip`, `skip in the street` with each year 1980 to 1996 and without a year (none before 2009 apart from a house called Skipness). Wikimedia Commons was not asked.",
        "reuse": [
            ["vignette-scene.json: the held skip (off since 2 Oct), its cones and its barrier", "a granite box, two cones, a crowd-control barrier", "REPLACED (the box); the cones and the barrier KEPT where they are (the cones stand on the footway at z -3.35, clear of the skip)", "W1; the cones' z"],
            ["production/research/period-vehicles-and-props NOTE.md and asset-plan: skip 2.6 x 1.5 x 1.2 m", "a size", "REPLACED by the photograph's profile (6-yard); the 4-yard is a scale", "W1"],
            ["Poly Haven models", "no skip", "NOT USED", "S5"],
            ["git branches (git log --all for skip)", "none", "none to reuse", ""],
        ],
        "axes": "Axes: x along the skip (the firm's name faces -y), y across, z up from the floor's underside on the ground. The side plates are prisms of the hexagonal profile in the x-z plane; everything else is boxes (the end plates rotated about y).",
        "assembly": [
            "**Profile (x, z)**: floor edge (+-%d, 0) up to the widest line (+-%d, 793) up to the top (+-1160, 1200): two stacked trapezia, the lower one's smaller edge at the bottom, the upper one's at the top." % (HALF_B, HALF_W),
            "**Plates**: two side plates 5 mm at y -850 to -845 and 845 to 850, a floor 5 mm, four end plates 5 mm (lower: floor edge to the widest line, upper: widest line to the top) sloping out and in with the sides.",
            "**Rim**: a folded bar 50 wide and 86 deep along both top edges and across the ends, its lower edge at 1114.",
            "**Rib**: a bar 50 high, 10 proud along each side at 923 (P1's line under the rim).",
            "**Lugs**: four, 80 x 60 x 25 at x -990 and 990, z 1090 to 1150, corners r 10 with a 30 mm hole (a texture mask).",
            "**Lamps**: two amber battery lamps 90 x 95 x 150 hung on the road side's rim by a hook, at x -1100 and 1100, z 1000 to 1150.",
            "**Edges and fixings**: plate edges folded or square, corners r 12 at the profile's points (a bevel on the mesh), welds not modelled (a seam texture along every plate joint, 6 mm wide).",
        ],
        "lettering": ["Firm: %s (invented: a fictional placeholder until the town mints one, kept in the stencil's own texture layer and blank in any picture for his page), number: %s (invented, a British number: the period STD code 0632 and the exchange 960, the range British drama uses): stencilled black capitals, name 120 mm and number 90 mm tall, on the side plate between z 450 and 760, centred; FILL LEVEL 40 mm tall 120 below the rim on the end plates." % (T["text"]["hire_firm"], T["text"]["number_line"])],
        "own_rows": "the profile against the photograph's edges, the lengths from the parts, the width and gaps in the lane, the scene's cones against the skip, the optional road-end cones, the stencil text and its placeholders, the lamps' colour, the four marking plates against the regulation's ranges (size, area, stripe angle and breadth, symmetry, level upper edges, height), the camber, the skip's share of the hook frame by projection",
    }


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
