"""bench: writes target.json and TARGET.md (cloud week 42, unit 13, family 3: the council bench)."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_family as SF
from sd_lib import B, CY, PR

FAMILY = "bench"
PMF = json.load(open(os.path.join(HERE, "photo_measurements.json")))["P1"]
F = PMF["features"]
LEN = 1800.0          # bench length = slat length (Judgement: a three-seat council bench; it also sets P1's scale)
SW, SG, ST = 63.0, 23.5, 32.0     # slat width, gap, thickness (P1: slat 12.4 px and gap 4.6 px at 0.198 px per mm)
SEAT_TOP = 440.0
RAKE = 10.0
EX = 788.0            # end frames' inner x (ends 25 thick)
Z_BACK0 = 445.0


def slats_z(k):
    return Z_BACK0 + k * (SW + SG)


def end_frame(tag, sx0, sx1, px0, px1, bx0, bx1):
    """One support: a flared timber slab leg (sx), a seat bearer (bx) and a raked back post (px)."""
    P = []
    P.append(PR("%s_slab" % tag, "yz", [[-215.0, 0.0], [245.0, 0.0], [245.0, 60.0], [225.0, 372.0], [-195.0, 372.0], [-215.0, 60.0]], sx0, sx1, "timber_leg",
                edge="edges r 6, foot flared 20 each end over the lowest 60", note="slab leg, 372 high, flared at the foot"))
    P.append(B("%s_bearer" % tag, bx0, bx1, -225.0, 255.0, 372.0, 408.0, "timber_leg", edge="edges r 3", note="seat bearer, 36 deep, carries the slats and the post"))
    top = 860.0
    off = (top - 408.0) * math.tan(math.radians(RAKE))
    P.append(PR("%s_post" % tag, "yz", [[205.0, 408.0], [245.0, 408.0], [245.0 + off, top], [205.0 + off, top]], px0, px1, "timber_leg", edge="edges r 4", note="raked back post, 10 degrees, 40 deep, to z 860"))
    return P


def bench_parts(length=LEN):
    P = []
    hl = length / 2
    cx = hl - 146.0                    # the leg's centre: 146 mm in from the slat end (P1)
    P += end_frame("end_l", -cx - 50.0, -cx + 50.0, -hl + 25.0, -hl + 100.0, -hl + 25.0, -cx + 50.0)
    P += end_frame("end_r", cx - 50.0, cx + 50.0, hl - 100.0, hl - 25.0, cx - 50.0, hl - 25.0)
    if length > 1500:
        P += end_frame("mid", -25.0, 25.0, -25.0, 25.0, -25.0, 25.0)
    for k in range(5):
        y0 = -215.0 + k * (SW + SG)
        P.append(B("seat_slat_%d" % (k + 1), -hl, hl, y0, y0 + SW, 408.0, SEAT_TOP, "timber", edge="arrised 2 mm all round, ends square", note="iroko 63 x 32"))
    t = math.tan(math.radians(RAKE))
    for k in range(5):
        z0 = slats_z(k)
        zc = z0 + SW / 2
        yface = 205.0 + (zc - 408.0) * t        # the post's front face at that height
        yc = yface - ST / 2.0 / math.cos(math.radians(RAKE))
        P.append({"id": "back_slat_%d" % (k + 1), "type": "box", "c": [0.0, round(yc, 2), round(zc, 2)], "s": [length, ST, SW], "rot": [0, 0, -RAKE], "material": "timber",
                  "edge": "arrised 2 mm all round", "note": "iroko 63 x 32, raked 10 degrees with the posts"})
    posts = [("l", -hl + 62.5, "end_l"), ("r", hl - 62.5, "end_r")] + ([("m", 0.0, "mid")] if length > 1500 else [])
    for k in range(5):
        zc = slats_z(k) + SW / 2
        yface = 205.0 + (zc - 408.0) * t
        for nm, x, _ in posts:
            yc = yface - ST / math.cos(math.radians(RAKE)) - 3.0
            P.append(CY("bolt_%s%d" % (nm, k + 1), (x, yc - 4.0, zc), (x, yc + 4.0, zc), 10.0, "galvanised", note="coach-bolt head, 20 across"))
    return P


def joins_for(P):
    names = {p["id"] for p in P}
    J = []
    for e in ("end_l", "end_r", "mid"):
        if e + "_slab" in names:
            J += [[e + "_bearer", e + "_slab"], [e + "_post", e + "_bearer"]]
    J += [["seat_slat_1", "end_l_bearer"], ["seat_slat_5", "end_r_bearer"], ["back_slat_1", "end_l_post"], ["back_slat_5", "end_r_post"], ["bolt_l1", "back_slat_1"], ["bolt_r5", "back_slat_5"]]
    if "mid_slab" in names:
        J += [["seat_slat_3", "mid_bearer"], ["back_slat_3", "mid_post"], ["bolt_m3", "back_slat_3"]]
    return J


def embeds_for(P):
    names = {p["id"] for p in P}
    E = []
    for n in "lmr":
        post = {"l": "end_l", "m": "mid", "r": "end_r"}[n] + "_post"
        for k in range(1, 6):
            if "bolt_%s%d" % (n, k) in names:
                E += [["bolt_%s%d" % (n, k), "back_slat_%d" % k, 12.0], ["bolt_%s%d" % (n, k), post, 12.0]]
    return E


def build():
    P1 = bench_parts(LEN)
    P2 = bench_parts(1200.0)
    T = {
        "family": FAMILY,
        "title": "Quay Street's council bench",
        "units": "millimetres; angles in degrees; z up; the sitter faces -y; the pivot is the centre of the bench's length on the ground, midway front to back of the end frames' feet",
        "status": "fixes applied, not re-reviewed",
        "sample": "B1",
        "materials": {
            "timber": {"name": "iroko slats, weathered", "srgb": [122, 98, 70], "rough": 0.8, "rough_words": "rough, grained", "metal": False, "note": "silvering on the top faces, dark at the bolt holes, a green algal stain on the back slats' lower edges"},
            "timber_leg": {"name": "iroko legs and posts, stained dark", "srgb": [74, 58, 42], "rough": 0.8, "rough_words": "rough, grained", "metal": False, "note": "dark with water and ground dirt, lightest at the arrised edges; a green stain at the foot"},
            "galvanised": {"name": "galvanised bolt heads", "srgb": [138, 140, 138], "rough": 0.5, "rough_words": "satin", "metal": True, "note": "domed heads, rust rings"},
        },
        "variants": {
            "B1": {"name": "B1: three-support council bench, 1800 long, 5 + 5 slats (the sample)", "parts": P1, "overall": {"w": LEN, "d": 550.0, "h": 860.0}, "overall_tol": 12.0, "noground": [],
                   "joins": joins_for(P1), "embeds": embeds_for(P1), "overlap_allow": 6.0, "faces": []},
            "B2": {"name": "B2: the two-support short bench, 1200 long, same slats and ends", "parts": P2, "overall": {"w": 1200.0, "d": 550.0, "h": 860.0}, "overall_tol": 12.0,
                   "joins": joins_for(P2), "embeds": embeds_for(P2), "overlap_allow": 6.0, "faces": []},
        },
        "drawing": {"views": ["front", "back", "left", "plan"], "sections": [{"id": "x400", "axis": "x", "at": 400.0}, {"id": "z700", "axis": "z", "at": 700.0}]},
        "numbers": [
            {"id": "N1", "what": "bench length (slat length)", "value": LEN, "kind": "Judgement", "source": "a three-seat council bench; it also fixes P1's scale: P1's overall width 356.6 px = 1800 mm gives 0.198 px per mm; error 20 mm", "tol": 20.0, "measure": {"kind": "bbox", "axis": "x"}},
            {"id": "N2", "what": "seat height (top of the seat slats)", "value": SEAT_TOP, "kind": "Judgement", "source": "440 mm, the usual public-seat height; the seat is hidden behind the back on P1; error 30", "tol": 30.0, "measure": {"kind": "edge", "axis": "z", "part": "seat_slat_3", "side": "hi"}},
            {"id": "N3", "what": "slat width (the seat slat's depth)", "value": SW, "kind": "Photo", "source": "P1 slat height 12.4 px (pitch 17.0 px less gap 4.6 px) at 0.198 px per mm = 63 mm; error 5", "tol": 5.0, "measure": {"kind": "extent", "axis": "y", "part": "seat_slat_1"}},
            {"id": "N4", "what": "slat pitch on the back (centre to centre)", "value": SW + SG, "kind": "Photo", "source": "P1 gap tops at 197.7, 214.8, 232.4, 248.6: mean pitch 17.0 px = 86 mm; error 4", "tol": 4.0, "measure": {"kind": "centre_dx", "axis": "z", "a": "back_slat_1", "b": "back_slat_2"}},
            {"id": "N5", "what": "slat thickness", "value": ST, "kind": "Judgement", "source": "32 mm iroko, the usual section; not visible on P1; error 4", "tol": 4.0, "measure": {"kind": "extent", "axis": "z", "part": "seat_slat_1"}},
            {"id": "N6", "what": "top of the highest back slat above the ground", "value": 445.0 + 5 * SW + 4 * SG, "kind": "Judgement", "source": "five slats from 445 up (the bench's back top is not measurable against the ground on P1); error 40", "tol": 40.0, "measure": {"kind": "edge", "axis": "z", "part": "back_slat_5", "side": "hi"}},
            {"id": "N7", "what": "back post top above the ground", "value": 860.0, "kind": "Judgement", "source": "860 mm: the post stands a little above the highest slat; P1 is a back view; error 40", "tol": 40.0, "measure": {"kind": "edge", "axis": "z", "part": "end_l_post", "side": "hi"}},
            {"id": "N9", "what": "the end legs' centre line in from the slat end", "value": 146.0, "kind": "Judgement", "source": "P1's right end shows 146 mm (the leg's centre 29 px in at 0.198 px per mm); the left end is seen obliquely and its leg flares about 35 px further out, so the inset rests on the right end alone: Judgement, error 60", "tol": 60.0,
             "measure": {"kind": "edge_to_centre", "axis": "x", "edge_part": "seat_slat_1", "edge_side": "hi", "centre_part": "end_r_slab"}},
            {"id": "N8", "what": "centre support thickness along the bench", "value": 50.0, "kind": "Photo", "source": "P1 mid_left 325.4 to mid_right 335.3 (9.9 px) at 0.198 px per mm = 50 mm; error 10", "tol": 10.0, "measure": {"kind": "extent", "axis": "x", "part": "mid_post"}},
        ],
        "photos": [],
        "sources": [], "previews": [], "checks": [], "owed": [],
    }
    # the centre standard is 50 thick
    for p in T["variants"]["B1"]["parts"]:
        pass
    # the photograph counts slats from the top: its slat i is the part back_slat_(6 - i)
    refs = {"back_top": ("y", "back_slat_5", "hi"), "gap1_top": ("y", "back_slat_5", "lo"), "gap1_bottom": ("y", "back_slat_4", "hi"), "gap2_top": ("y", "back_slat_4", "lo"),
            "gap2_bottom": ("y", "back_slat_3", "hi"), "gap3_top": ("y", "back_slat_3", "lo"), "gap3_bottom": ("y", "back_slat_2", "hi"), "gap4_top": ("y", "back_slat_2", "lo"),
            "gap4_bottom": ("y", "back_slat_1", "hi"), "left_end": ("x", "back_slat_5", "hi"), "right_end": ("x", "back_slat_5", "lo"),
            "mid_left": ("x", "mid_post", "hi", {"add": 0.0}), "mid_right": ("x", "mid_post", "lo", {"add": 0.0})}
    ph = SF.photo_entry(PMF, "P1", "S1", "B1", refs, ["back_slat_5", "back_slat_2"], anchors=("back_top", "gap4_top"), boundary=("left_end", "right_end", "back_top"),
                        view="back", fit_top="back_top", fit_bottom="gap4_top", centre_from=lambda FF: (FF["left_end"]["px"] + FF["right_end"]["px"]) / 2.0, min_tol=5.0, file="P1.jpg",
                        method="each edge is the strongest grey-level step of the stated sign inside the recorded window, averaged over the recorded band; the scale is fitted on the one span from the back's top edge to the fourth slat's lower edge (62.4 px); the bench is seen from behind against the light (the sea is bright behind it, the gaps between the slats shine through) so the dark slats and the bright gaps give sharp edges; the width (356.6 px) is the unit that gives 0.198 px per mm if the bench is 1800 long (Judgement); the photograph's centre bar is 6 px right of the bench's centre (the camera is a little to the right), so the mid features carry 8 px; the tolerance is the measured spread times 3 plus 2 px, at least 5 px (25 mm)")
    for f in ph["features"]:
        if f["id"].startswith("mid"):
            f["tol_px"] = 8.0
        if f["id"] in ("left_end", "right_end"):
            f["tol_px"] = 7.0
    T["photos"].append(ph)
    return T


def finish(T):
    T["sources"] = [
        {"id": "S1", "url": "https://www.geograph.org.uk/photo/2693537", "read": "2026-10-13", "author": "Chris Downer", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2011-11-06", "kind": "photograph",
         "shows": "Poole: a long slatted timber bench seen from behind against a bright harbour: five back slats with their gaps shining through, a centre support about 50 mm wide, end uprights about 75 mm, and a broad flared timber leg about 100 mm thick under each end; the RIGHT end shows it 146 mm in from the slat end (the left end is seen obliquely and its leg flares outward at the slat end, about 35 px outside the drawn leg on the 420 px crop); the seat is hidden",
         "used": True, "not_used_for": "any absolute size (no scale object), the leg's depth and curve (a backlit silhouette), the colours", "period": "2011; a council bench pattern of long standing; used for the slat proportions only"},
        {"id": "S2", "url": "https://www.geograph.org.uk/photo/2672444", "read": "2026-10-13", "author": "Stefan Czapski", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2011-10-28", "kind": "photograph",
         "shows": "a cast-iron-ended slatted park bench in side view: raked back, seat bearer, legs joined by a floor stretcher, a scrolled arm",
         "used": False, "not_used_for": "everything: its cast ends are Victorian ornament (heritage, not a 1990 council bench) and S1 shows a different, timber-legged type, which wins", "period": "2011 heritage park bench"},
        {"id": "S3", "url": "https://www.geograph.org.uk/photo/2029816", "read": "2026-10-13", "author": "Chris Downer", "licence": "CC BY-SA 2.0 (read on the page)", "taken": "2010-08-20", "kind": "photograph",
         "shows": "benches in a row on a harbour wall: timber slat seat and back on painted cast end frames with arms, bolted to the paving",
         "used": False, "not_used_for": "everything (looked at: it supports benches standing on a harbour wall; they are single-seat cast-frame benches, a different type from S1)", "period": "2010"},
        {"id": "S4", "url": "https://api.polyhaven.com/assets?t=models", "read": "2026-10-13", "author": "Poly Haven artists", "licence": "CC0 1.0", "taken": "n/a (the list of 521 models)", "kind": "model list",
         "shows": "painted_wooden_bench (1165 x 497 x 889 mm, a farmhouse bench), modular_street_seating (4340 x 770 x 950, a modern set), wooden_picnic_table (a table with benches)",
         "used": False, "not_used_for": "everything: none is a 1990 council bench (painted farmhouse, modern, picnic)", "period": "n/a"},
        {"id": "S5", "url": "production/specs/vignette-scene.json (this repository)", "read": "2026-10-13", "author": "this project", "licence": "own work", "taken": "n/a", "kind": "own",
         "shows": "the held bench models (park_bench, garden_bench_01, ornate_bench, curved_stone_bench) are NOT placed: 'a bench belongs on a wide pavement or a quay, and this footway is 2.0 m'",
         "used": True, "not_used_for": "any shape", "period": "n/a"},
        {"id": "S6", "url": "https://api.geograph.org.uk/syndicator.php (terms bench, seat, slatted bench, harbour bench, wooden bench, iron bench; takenyear 1975 to 1996 and without a year)", "read": "2026-10-13", "author": "Geograph contributors", "licence": "CC BY-SA 2.0 (each page)",
         "taken": "1975 to 1996 searched", "kind": "search record",
         "shows": "for 1975 to 1995 only a 1990 white metal garden bench in a village and a 1993 timber bench in a park (looked at: tiny in frame, one with a person); about 250 later photographs, the survey 'bench marks' flooding the results; no period photograph of a council bench near a harbour was measurable",
         "used": False, "not_used_for": "measuring", "period": "n/a"},
    ]
    T["previews"] = [
        {"file": "p1-poole-bench-back.jpg", "source": "S1", "credit": "Chris Downer, Geograph 2693537, CC BY-SA 2.0, 2011-11-06, cropped to the bench",
         "masked": ["nothing to mask: a silhouette with a boat far behind"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
        {"file": "p1-poole-bench-target-on-photo.jpg", "source": "S1", "credit": "overlay of this target's back elevation (red) on the same crop, the scale fitted on the height from the back's top to the fourth slat's lower edge, measured edges in green",
         "masked": ["as p1"], "looked_at_full_size": True, "no_people_no_drink_no_betting_no_names": True},
    ]
    T["night"] = {"lantern_linear": L.LANTERN_LINEAR, "note": "the bench stands outside the street's lamp pools on the quay apron; the timber top faces catch the lantern colour (1, 0.25, 0) only as a glint; nothing on it lights"}
    T["placement"] = {
        "slot": "the quay apron, the bench's centre at x -40.0 m, z 0.0 m (on the street's axis), the sitter facing -x (south-west over the Old Basin, which lies beyond the cope at x -69.4), the back to the street; one bench. (The first version stood it at x -9.0, z 2.5: that point is on the road arm of Quay Street, 0.5 m inside the east kerb; the apron's setts begin at about x -33.1.)",
        "x_m": -40.0, "z_m": 0.0, "faces": "-x", "min_pavement_mm": 3000.0, "footway_mm": 2000.0, "bench_depth_mm": 550.0,
        "reasons": [
            "the scene file keeps benches off the street: 'a bench belongs on a wide pavement or a quay, and this footway is 2.0 m' (S5); a bench needs its 550 mm of depth plus 900 mm of leg room in front and 1000 mm of clear way behind it, about 2.4 m, against a 2.0 m footway",
            "the asset plan lists benches 'on the quay' (1 to 2). The apron was read from tools/art-recipes/south-quay/south_quay_geom.py (build(), 13 October): Quay Street runs on south of x 0 as its own 6 m carriageway (road_quay_street_south, x -2.0 to -21.2) to the junction, whose south kerb is at about x -33.0; the apron's setts (apron_setts, level 0.05 m above the crown) begin at about x -33.1 and run to the cope at x -69.4. The first version's point (-9.0, 2.5) lies on the road arm, 0.5 m inside the east kerb face, and its far end on footway_northeast_corner; the row that said 'it stands south' (x below 0) could not tell the apron from the road",
            "x -40.0, z 0.0: the footprint (600 x 1800) and 1.0 m round it lie only on apron_setts, 6.9 m from its edge at the junction's south kerb, 29.4 m from the cope, clear of the quay's fish boxes, rings and bollards (all beyond x -64); the sitter faces -x, over the basin",
            "the bench is far from both pictures: it is 78 m from the reverse camera (cam_reverse, x 38, z 1.6) and 37 m from the hook camera (x -3, z -1.6), small and seen from behind or from the side, if at all; it is not put there to be seen in the morning pictures but for the player who walks down to the quay",
            "clear of the quay's bollards (the bollards target stands them at the quay edge and the corners, 30 m away)",
        ],
        "poses": [{"id": "bench", "variant": "B1", "x_m": -40.0, "z_m": 0.0, "yaw_deg": -90.0, "zone": "quay_apron", "front_faces": "-x", "base_y_m": 0.05, "apron_margin_m": 1.0, "cope_min_m": 3.0}],
        "cam_reverse": {"x_m": 38.0, "z_m": 1.6, "distance_m": 78.0},
        "cam_hook": {"x_m": -3.0, "z_m": -1.6},
    }
    T["wear"] = [
        "the iroko is silvered on its top faces and weathered grey-brown on the back slats, with a darker band along each slat's lower edge where water sits; end grain checked and darker, one slat split 300 mm from an end",
        "the legs and posts are dark with water and ground dirt, green-stained over the lowest 120 mm, the arrised edges lighter; rust rings 20 to 40 mm round the bolt heads and short rust streaks below them",
        "dirt: a pale bird-lime splash on the top of the back and two on the seat; moss in the joint between end frame and slat; none of anyone's belongings",
        "carved or scratched marks on the back slats' upper edge (a few initials, never a word that is a name or a firm)",
        "NOT shown: a person, a bottle or can, any advertisement plate (a bench was often given in memory: no plaque)",
    ]
    T["disagreements"] = [
        {"id": "W1", "what": "where benches stand", "book": "the asset plan: benches 1 to 2 on the quay; the scene file's held benches are named for a street", "photo": "n/a (a placement fact)", "chose": "the quay apron only; never the 2.0 m footway"},
        {"id": "W2", "what": "the slat's size", "book": "none (the usual 70 x 32 iroko)", "photo": "P1: the slat reads 63 mm (12.4 px at 0.198 px per mm, the scale from an assumed 1800 length)", "chose": "63 x 32, gap 23.5, pitch 86.5 (Photo within 5 mm of the assumption)"},
        {"id": "W3", "what": "the ends", "book": "the asset plan: cast ends with timber slats; S2 and S3 show cast-iron ends", "photo": "S1: the end support is a broad flared timber leg about 100 mm thick (20 px at 0.198 px per mm), 146 mm in from the slat end on the right end ONLY (the left end is seen obliquely and its leg lies about 35 px further out), with a 75 mm upright at the end", "chose": "timber slab legs 100 thick, flared at the foot, a bearer, a 75 wide raked post; the inset 146 mm is a Judgement of plus or minus 60 resting on the right end alone; no cast iron (the photograph wins over the plan)"},
    ]
    T["variants_note"] = [
        "B1 (the sample): three supports, 5 + 5 slats, no arms; one on the quay apron (x -40.0, z 0.0).",
        "B2: a short bench, 1200 long, two supports, the same slats and ends (a second bench or the south quay's other end; not placed today).",
        "conditions (materials): C0 sound; C1 worn (the sample's wear); C2 one back slat missing at the right end (a gap 63 mm, a seed).",
        "colours: the iroko is left unpainted; a repainted bench is a seed (council green on the legs and posts, 40 percent), the slats stay bare.",
    ]
    T["owed"] = []
    T["handovers"] = [
        {"id": "H1", "place": {"file": "production/specs/hook-cast.json", "place": "quay", "x_m": -5.0, "z_m": 0.0}, "line": "For the town: hook-cast.json places.quay (x -5.0, z 0.0, 'the quay apron at the street's south end') lies on the road arm (road_quay_street_south spans x -21.2 to -2.0 and the apron's setts begin at about x -33.1), not on the apron; move the place onto the apron (the bench's slot, x -40.0, z 0.0, is on it) or say it is the road's end, and re-check the routines that use it."},
    ]
    T["not_settled"] = [
        "absolute sizes: S1 has no scale object; the 1800 length is Judgement (it sets the slat width at 63 mm); seat height 440, back height 854 and the 10 degree rake are Judgement",
        "the end frames' exact shape (S1's ends are in silhouette; S2 is ornate; S3 is a plain pedestal type): the plain straight-legged end is a Judgement from S2's construction and S3's plainness",
        "the apron's extents were read on 13 October from south_quay_geom.build() (setts from x -33.1 to the cope at x -69.4); the town's own quay place (hook-cast.json places.quay, x -5.0, z 0.0) lies on the road arm, not the apron: handover H1",
        "whether the street had any bench in 1990 (the scene says none on the footway); one on the quay is the asset plan's count",
    ]
    T["content_rule_note"] = "no person on the bench, no bottle or can, no memorial plaque (a statement of the content rule)."
    T["builder_notes"] = [
        "supports: each is a flared slab leg (prism in the y-z plane, points in the parts table, 100 thick; the centre one 50), a bearer and a raked post (end 75 wide, centre 50); build the two end supports identical, mirrored",
        "slats: 1800 long, arrised 2 mm; the back slats are rotated 10 degrees about the bench's length axis with the posts; the bolt heads on the back's face at each post, 20 across and 7 high, domed",
        "the seat slats sit on the bearers (z 408); the slats' underside is the bearer's top",
        "orientation: the local -y is the way the sitter faces; in the street's frame -y points -x (south-west, towards the basin): the pose is x -40.0, z 0.0, yaw -90 (the bench's length then runs along the street's z)",
    ]
    C = []
    for n in T["numbers"]:
        C.append({"name": "%s: %s" % (n["id"], n["what"]), "measure": "measure it on the built mesh in millimetres (%s)" % n["measure"].get("kind"), "expect": "%.1f mm" % n["value"], "tol": "+-%.1f mm" % n["tol"]})
    C += [
        {"name": "C1: five seat slats and five back slats, equal gaps", "measure": "count the slats and measure each gap", "expect": "5 + 5; gap 23.5 mm", "tol": "+-3 mm"},
        {"name": "C2: three identical end frames", "measure": "compare the three frames' parts", "expect": "identical", "tol": "exact"},
        {"name": "C3: no part floats and every join meets", "measure": "the contact graph of the meshes", "expect": "all parts reach the ground", "tol": "0 floating"},
        {"name": "C4: the bolts sit on the back slats' front faces", "measure": "each bolt head against its slat", "expect": "head proud 7 mm", "tol": "+-3 mm"},
        {"name": "C5: no plaque, no lettering", "measure": "the model's text", "expect": "none", "tol": "exact"},
    ]
    T["checks"] = C
    return T


SUMMARY = ("The council bench is 1800 mm long on three timber supports (a flared slab leg 100 mm thick under each end 146 mm in from the slat end, a 50 mm centre leg, a seat bearer and a back post raked 10 degrees), with five iroko seat slats and five back slats each 63 x 32 mm and 23.5 mm apart, bolted with domed coach-bolt heads, the seat 440 high and the back's top at 854; "
           "it does not stand on the 2.0 m footway (the scene file says so and the arithmetic agrees: it needs about 2.4 m) but on the quay apron at x -40.0, z 0.0 (the first version's x -9.0 was on the road arm), facing the basin, 78 m from the reverse camera, so small and seen from behind if at all: it serves the player's walk to the quay; "
           "no period bench photograph was measurable, so the slat proportions are measured on a 2011 photograph of the back of a council bench against the light and every absolute size is judged (the bench's length sets the scale).")


def story(T):
    S = {
        "no": "3", "title": "Quay Street's council bench: the exact target", "summary": SUMMARY,
        "previews_list": "p1 (S1 cropped) and its target-on-photo overlay",
        "rulings": {"ruling_2oct": "not a car, skip, pallet or kiosk; furniture the street may carry on its quay", "sources_order": "no free model fits (S4: a farmhouse bench, a modern set, a picnic table in 521 Poly Haven models); so own work by script",
                    "content": "nobody sits on it, no bottle, no plaque; the data scan finds none", "noai": "S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source; nothing is placed or traced",
                    "look": "dark timber, silvered slats and grime; no bright paint", "night": "the bench stands outside the lamp pools"},
        "searched": "What was searched: Geograph's feed for `bench`, `seat`, `slatted bench`, `harbour bench`, `wooden bench`, `iron bench` with each year 1975 to 1996 and without a year (about 250 later photographs; the survey benchmarks of the OS flood every query). Wikimedia Commons was not asked.",
        "reuse": [
            ["production/specs/vignette-scene.json held props: park_bench, garden_bench_01, ornate_bench, curved_stone_bench (not placed)", "four held bench models", "NOT USED", "each is a park, garden or ornate bench; the scene itself says none belongs on the footway"],
            ["production/research/asset-plan 3 (A3 assemblies: bench, cast ends with timber slats; A5: 2 models, 1 to 2 on the quay)", "the plan for the bench", "KEPT as the brief, its cast ends REPLACED", "S1 shows timber slab legs (W3)"],
            ["Poly Haven models painted_wooden_bench, modular_street_seating, wooden_picnic_table", "CC0 benches", "REJECTED", "S4: not a 1990 council bench"],
            ["tools/art-recipes/south-quay (the quay apron)", "the apron the bench stands on", "READ (build() run on 13 October) and the slot tested against its surfaces by the placement rows; not edited", "x -40.0, z 0.0 lies on apron_setts; the first version's x -9.0 was on the road"],
            ["git branches (git log --all for bench)", "none", "none to reuse", ""],
        ],
        "axes": "Axes: x along the bench (the length), y from the sitter's front (-y) to the back (+y), z up from the ground. Boxes, cylinders and one prism per end frame (the raked back post); the self-check measures every number back off the parts.",
        "assembly": [
            "**Three supports** (left, right, centre): a flared slab leg of timber (the ends 100 thick and centred 146 in from the slat end, the centre one 50 thick), 372 high, its foot flared 20 each end over the lowest 60; a seat bearer 36 deep at z 372 to 408 carrying the slats and the post; a back post raked 10 degrees from z 408 to 860, 40 deep and 75 wide at the ends (flush 25 in from the slat end), 50 wide at the centre; edges r 3 to 6.",
            "**The seat**: five iroko slats 63 x 32 x 1800 on the bearers, top at 440, gaps 23.5, arrised 2 mm; the front slat 215 in front of the middle.",
            "**The back**: five iroko slats 63 x 32 x 1800 raked 10 degrees on the front of the three posts, the lowest at z 445, pitch 86.5, the highest top at 854.",
            "**Fixings**: a domed coach-bolt head (20 across, 7 high) through each back slat at each post (15), square nuts behind; the seat slats are screwed from above with countersunk heads flush (not modelled).",
            "**B2** is the same bench 1200 long with two supports and no centre frame.",
        ],
        "own_rows": "the bench's depth against the footway (the arithmetic that keeps it off the 2.0 m footway), the pose against the south quay kit's surfaces (the footprint and 1 m round it on the apron's setts, no road or footway, nothing of the quay's furniture within 1 m, 3 m from the cope), the distance to the reverse camera, the slat counts and gaps, the three frames identical, the bolts on the back slats, the legs' inset",
    }
    return S


if __name__ == "__main__":
    T = finish(build())
    SF.write_all(HERE, T, story(T))
