"""The corrections to the target that the two fresh try 1 reviews list (13 October 2026), applied to production/cloud-week/targets/front-doors-all/target.json.

    /home/user/.bpyenv/bin/python target_changes_try2.py            # applies them (idempotent: a second run changes nothing) and prints each change

Only target.json and TARGET.md are edited (TARGET.md: the superseded statements are patched in place, each marked, and a section 16, "Changes after the build", lists every change). The target's makers (td_*.py, make_target.py, make_doc.py) and its reference
drawing (target_drawing.py) are NOT changed: they are not this unit's files, and regenerating the target from them would undo these changes. Each change is also written into
target.json under "changes_after_the_build", dated "13 Oct, from the try 1 reviews".
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "..", "..", "targets", "front-doors-all", "target.json")
WHEN = "13 Oct, from the try 1 reviews"


def smooth_steps(d0, h0, h1, width, n=8):
    """A cove as a quarter circle, 6 mm across and 6 deep: its top edge a vertical tangent against the face (a crisp arris), its foot a horizontal tangent on the floor; n facets."""
    out = []
    for i in range(n + 1):
        a = math.radians(180.0 + 90.0 * i / n)
        out.append([round(d0 + width * (1.0 + math.cos(a)), 3) + 0.0, round(h0 + (h1 - h0) * (-math.sin(a)), 4) + 0.0])
    return out


def add_once(d, key, text):
    """Append text to d[key] once (a second run of this script changes nothing)."""
    if text not in d.get(key, ""):
        d[key] = d.get(key, "") + text


def main():
    raw = open(PATH, encoding="utf-8").read()
    N = json.loads(raw)
    log = []

    def note(what, why):
        log.append({"change": what, "why": why, "date": WHEN})

    # ---- T3: the panel profile (street review, fault 1) and the border (builder's point 1, close review 12a)
    t3 = N["kinds"]["T3"]
    prof = smooth_steps(0.0, 0.0, 6.0, 6.0) + [[60.0, 6.0]] + smooth_steps(62.5, 6.0, 12.0, 6.0) + [[110.0, 12.0]]
    t3["mouldings"]["outside"]["profile_dh"] = prof
    t3["mouldings"]["outside"]["note"] = (
        "each moulded panel has TWO outlines (D4): an outer and an inner outline, a margin of about 62.5 between them at the sides (the border); the margin is a flat raised border "
        "with a quirked (quarter-circle) cove at each line, each step 6 mm deep over 6 mm across, a quarter-circle cove whose top meets the face at a vertical tangent (steeper than 45 degrees: 13 Oct, from the try 1 reviews; the first numbers, two coves 3 mm deep over "
        "14, dipped 1 to 3 per cent in the street view against D4's 14 to 40): 6 mm down at the outer line to the margin, 6 mm more at the inner line to the field, which is 12 below "
        "the border face; the outlines and the 44 mm leaf are as they were; the upper panel's inner outline has a segmental head (crown v 1646, springing 22 lower) under a flat outer "
        "top; no applied mouldings")
    t3["leaf"]["border"] = 62.5
    for c in N["checks"]:
        if c["id"] == "PL-T3-members":
            c["expect"] = {"border": 62.5}
            c["src"] = ("kind spec; 13 Oct, from the try 1 reviews: the border is the flat margin between the outer and the inner outline at the sides, 182.4 less 119.9 = 62.5 "
                        "(the first target said 65, which no feature of its own outlines has)")
    note("T3: profile_dh: each of the two steps 6 mm deep over 6 mm across (the margin 6 below the face, the field 12 below); the outlines (u 119.9 / 182.4 / 630.4 / 692.9) and the 44 mm leaf are kept; the second cove at d 62.5 to 68.5",
         "street review, fault 1: the outlines dipped 1 to 3 per cent in the street view; D4's dip 14 to 40 per cent. Also narrow point 12(c) of the close review (the second cove at 62.5, not 76)")
    note("T3: border 65 becomes 62.5 (row PL-T3-members)", "street review point 10, close review 12(a): the flat margin of the target's own outlines is 62.5 at the sides")
    if not any(c["id"] == "PL-T3-street-dip" for c in N["checks"]):
        idx = [c["id"] for c in N["checks"]].index("PL-T3-framing") + 1
        N["checks"].insert(idx, {
            "id": "PL-T3-street-dip", "group": "PL", "name": "T3: every outline dips at least 10 per cent in the street view", "kind": "T3",
            "what": ("on the street picture (camera 3.5 m out, 2 m along, eye 1.6 m; 1600 x 1200), across each of the 16 outlines of the two panels (the outer and the inner outline, "
                     "both sides and top and foot, at each panel's middle) the brightness changes by at least 10 per cent of the leaf face's brightness within 4 px of where the outline "
                     "projects: (the greatest less the least of a 4-sample band averaged along 15 px) divided by the median of the leaf face"),
            "expect": {"min_dip_fraction": 0.10, "outlines": 16}, "tol": 0.0,
            "src": "street review of 13 Oct, fault 1 (D4's outlines dip 14 to 40 per cent in the same flat overcast light; the first build's dipped 1 to 3)", "type": "street_dip"})
    note("T3: new row PL-T3-street-dip: in the street view every outline dips at least 10 per cent of the face's brightness", "street review, fault 1")

    # ---- the moulding ring's lap (street 11, close 12b): data only; target_drawing.py is not this unit's file
    for k in ("T1", "F1", "F2"):
        o = N["kinds"][k]["mouldings"]["outside"]
        o["lap_over_framing_mm"] = 4.8
        o["ring_note"] = ("13 Oct, from the try 1 reviews: the bolection's ring stands 4.8 outside the opening's edge (its lap over the framing, as the passed 3.1 door builds it) and "
                          "reaches width_on_face less 4.8 inside it; the first drawing started the ring at the opening's edge")
    note("T1, F1, F2: the bolection ring starts 4.8 outside the opening's edge (lap_over_framing_mm 4.8)",
         "street review 11, close review 12(b); target_drawing.py (the reference drawing, not this unit's file) still draws the literal ring: the check's required rows read the lap from this field, its three literal extras keep failing for that reason only")

    # ---- F7's thickness (street 13, close 12d)
    f7 = N["kinds"]["F7"]["leaf"]
    f7["t"] = 47.0
    f7["construction"] = "ledged and braced matchboarding: boards 22, ledges 25, braces 25 behind them (47 thick: Hasluck's proportion; fits the F frame's rebate of 53)"
    f7["ledge_t"] = 25.0
    note("F7: leaf 47 thick (boards 22, ledges 25, braces 25) instead of 38 with thin ledges", "street review 13, close review 12(d): 22 + 25 cannot make 38; 16 mm ledges are thin against Hasluck's")

    # ---- the boot scraper (street 9, builder's 5; close 12e is wrong, see NOTES.md and D10)
    bs = N["furniture"]["scraper"]["BS1"]
    old = [list(p) for p in bs["standard_profile_xz"]]
    if old[0] == [0.0, 0.0] and old[1] == [25.0, 0.0]:
        bs["standard_profile_xz"] = [[round(25.0 - x, 2), z] for x, z in old]
    if True:
        bs["standards"] = ("two end standards 200 high, each a flat bar 25 x 12 rising from a splayed foot to a scroll of radius 35 that sits OUTSIDE the bar and curls outward at the top "
                           "(D10: the scrolls sit outboard of the blade's ends); the profile is the point list standard_profile_xz (x outward from the blade's end, the bar at 0 to 25, "
                           "the scroll to 62, z up, mm; 13 Oct, from the try 1 reviews: the first list had the scroll at negative x, over the blade), mirrored for the other end; the bars stand 10 mm "
                           "over the blade's ends; the feet stand 0.4 into the ground and the standards 0.55 (no two bottoms share a plane)")
        bs["size"] = [404.0, 130.0, 200.0]
        for c in N["checks"]:
            if c["id"] == "FU-T1-scraper-BS1":
                c["expect"]["size"] = [404.0, 130.0, 200.0]
    note("BS1: the point list is mirrored so each scroll sits outside its standard and curls outward; the overall length is 404 (the blade 300 between bars 140 either side of the middle, the scrolls to 202); the feet stand 0.4 into the ground and the standards 0.55",
         "street review 9 (D10's scrolls sit outboard of the blade's ends and curl outward; the photograph shows it); the close review's 12(e) reads D10 the other way, and is wrong: the left scroll's centre is about 70 px outboard of the blade's end in D10")

    # ---- reeded glass thickness (street 14, close 12f)
    g = N["glass"]["reeded_4mm"]
    g["base_thickness"] = 2.8
    g["section"] = "circular segments, vertical, standing 1.2 on a base 2.8 thick: 4.0 thick in all (13 Oct, from the try 1 reviews; the drawing's reeded_section, which has a 4.0 base, is not changed here)"
    note("reeded glass: a base 2.8 thick under flutes 1.2 deep (4.0 in all)", "street review 14, close review 12(f)")

    # ---- P2's plate is chrome-coloured (close 12h)
    lp2 = N["furniture"]["letter_plate"]["LP2"]
    lp2["material"] = "nickel or chrome-look"
    lp2["srgb"] = [170, 170, 168]
    lp2["metal"] = 1.0
    lp2["roughness"] = 0.35
    lp2.pop("worn_roughness", None)
    add_once(lp2, "src", "; 13 Oct, from the try 1 reviews: P2's plate is chrome-coloured, not brass (close review 12(h))")
    note("LP2: chrome (nickel or chrome-look, sRGB 170, 170, 168) instead of brass", "close review 12(h): P2's plate is chrome-coloured")

    # ---- F5's hairline (close 12h)
    n5 = N["kinds"]["F5"]["mouldings"]["outside"]
    n5["note"] = ("flat painted face; a 1 mm hairline round the lipping, 6 mm in from the edge (it lies under the stops' 20.4 mm lap on three sides, so it shows only at the foot: 13 Oct, "
                  "from the try 1 reviews, kept as built); the slit has a 15 mm square timber bead, 4 proud")
    note("F5: the hairline is kept and said to show only at the foot (under the stops' lap on three sides)", "close review 12(h)")

    # ---- levers, bar pull, thumb latch (close 3 4 5; street 2)
    hd = N["furniture"]["handle"]
    for k in ("HD2a", "HD2b", "HD2c"):
        hd[k]["lever_taper_mm"] = [16.0, 12.0]
        hd[k]["lever_bend"] = {"length_mm": 25.0, "back_toward_the_door_mm": 9.0}
    add_once(hd["HD2a"], "src", "; 13 Oct, from the try 1 reviews: the bar tapers from 16 at the neck to 12 at the end and its last 25 mm curve back 9 toward the door (close review 5); the round rose is kept (D5 shows it)")
    for k in ("HD2b", "HD2c"):
        hd[k]["backplate"] = {"size": [40.0, 170.0], "proud": 2.5, "top_above_lever_centre": 40.0, "keyhole_below_lever_centre": 57.0, "keyhole_head": 12.0, "keyhole_slot": 6.0,
                              "keyhole_h": 24.0, "boss_dia": 30.0, "boss_proud": 2.5}
        hd[k]["name"] = hd[k]["name"].replace("on a round rose", "on a long backplate with a keyhole")
        add_once(hd[k], "src", "; 13 Oct, from the try 1 reviews: a backplate 40 x 170 with a keyhole 57 below the lever's centre (sashlock furniture: the street review's dated 1990 photograph of a lever "
                               "on a long backplate, point 2) in place of the round rose; the bar tapers 16 to 12 and curves back (close review 5)")
    hd["HD3"]["name"] = "vertical bar pull on the lock stile: a round grip on two posts that flare into roses"
    hd["HD3"]["grip_dia"] = 19.0
    hd["HD3"]["stand_off"] = 30.0
    hd["HD3"]["rose_dia"] = 25.0
    hd["HD3"]["proud"] = 39.5
    add_once(hd["HD3"], "src", "; 13 Oct, from the try 1 reviews (close review 3): the grip is 19 across with domed ends, 270 long overall; the posts flare into roses 25 across; the stand-off is 30 "
                               "(face to the grip's axis, so the grip stands 39.5 proud; the first number was 35 for a flat bar)")
    hd["HD4"]["name"] = "thumb latch on a ledged door: a plate with cusped ends, a round bow on two posts, a flat thumb lever through a slot in the head"
    hd["HD4"]["plate"] = [38.0, 190.0]
    hd["HD4"]["plate_ends"] = "cusped (arrow-shaped) at both ends"
    hd["HD4"]["slot"] = [16.0, 4.0]
    hd["HD4"]["slot_z"] = 72.0
    hd["HD4"]["bow_len"] = 150.0
    hd["HD4"]["bow_sag"] = 4.0
    hd["HD4"]["bow_centre_z"] = 0.0
    hd["HD4"]["grip_dia"] = 19.0
    hd["HD4"]["stand_off"] = 30.0
    hd["HD4"]["post_gap"] = 120.0
    hd["HD4"]["thumb"] = {"length": 45.0, "width": 14.0, "angle_deg": 15.0}
    hd["HD4"]["thumb_piece"] = "a flat lever 14 wide and 45 long that rises through a slot in the plate's head at 15 degrees (13 Oct, from the try 1 reviews; was a 25 x 35 pressed piece)"
    hd["HD4"]["bar"] = "replaced by the bow: a round bar 19 across, 150 long with domed ends, bowed 4, its axis 30 off the plate, on posts 120 apart"
    add_once(hd["HD4"], "src", "; 13 Oct, from the try 1 reviews (close review 4): cusped plate ends, a 19 round bow standing 30 off on posts 120 apart, a thumb lever 14 x 45 at 15 degrees")
    note("HD2a, HD2b, HD2c: the lever bar tapers from 16 at the neck to 12 at the end and its last 25 mm curve back 9 toward the door", "close review 5")
    note("HD2b and HD2c: a backplate 40 x 170 with a keyhole 57 below the lever's centre in place of the round rose (HD2a, F6, keeps its rose)",
         "street review 2 (and its 1990 photograph); the close review's 'keep the round rose' rests on D5, which is F6's door, HD2a")
    note("HD3: a round grip 19 across on posts that flare into 25 roses, stand-off 30 (face to the grip's axis), 25 x 270 overall kept; HD4: cusped plate, a 19 round bow standing 30 off on posts 120 apart, a thumb lever 14 x 45 at 15 degrees through a slot in the head",
         "close review 3 and 4")

    # ---- a lever's u, v is the centre of its rose or boss (close 12g)
    for k in ("HD2a", "HD2b", "HD2c"):
        hd[k]["place_note"] = "u, v is the centre of the lever's rose (HD2b, HD2c: of its boss on the backplate): the pivot and the fitting's mount point; the bar points toward the door's middle from there (13 Oct, from the try 1 reviews)"
    for c in N["checks"]:
        if c["group"] == "FU" and c.get("variant") in ("HD2a", "HD2b", "HD2c"):
            c["what"] = "centre of the lever's rose or boss (its pivot, the mount point) in the leaf frame (u, v)"
    note("a lever's u, v (rows FU-*-handle-HD2a, HD2b, HD2c) is the centre of its rose, or of its boss on the backplate", "close review 12(g)")

    # ---- keyholes: KH1 sunk (close 10); on T2 and F3 below the bar pull (street 2)
    kh = N["furniture"]["keyhole"]["KH1"]
    kh["place"]["T2"] = {"u": 57.2, "v": 1031.6}
    kh["place"]["F3"] = {"u": 67.0, "v": 1050.0}
    kh["name"] = "plugged mortice keyhole: a round head over a parallel slot, SUNK in a blind pocket 2.2 deep (the dark plate's face 2.0 below the leaf's face), a pale metal blank filling the slot, its face 0.5 below the leaf's face"
    add_once(kh, "src", "; 13 Oct, from the try 1 reviews: sunk, not a raised plate (close review 10); T2 and F3 carry one 70 below the foot of the bar pull (street review 2 asked for 70 below the "
                        "pull's centre, which lies behind the 270 long bar: the foot is 135 below the centre, so the keyhole is placed 70 below the foot, where it shows)")
    for h in N["street"]["houses"]:
        if h["kind"] in ("T2", "F3"):
            h["furniture"]["keyhole"] = {"variant": "KH1", "place": dict(kh["place"][h["kind"]])}
    base = [c for c in N["checks"] if c["id"] == "FU-F1-keyhole-KH1"][0]
    for k, pl in (("T2", kh["place"]["T2"]), ("F3", kh["place"]["F3"])):
        rid = "FU-%s-keyhole-KH1" % k
        if not any(c["id"] == rid for c in N["checks"]):
            c = json.loads(json.dumps(base))
            c["id"], c["name"], c["kind"] = rid, "%s: keyhole KH1" % k, k
            c["expect"] = {"u": pl["u"], "v": pl["v"], "size": [23.0, 32.0], "place": dict(pl)}
            c["src"] = "street review 2 (13 Oct): a keyhole below the bar pull so that the door can be locked from the street"
            at = [i for i, x in enumerate(N["checks"]) if x["id"] == "FU-%s-handle-HD3" % k][0] + 1
            N["checks"].insert(at, c)
    note("KH1 is sunk (a blind pocket 2.2 deep in the leaf, plate face 2.0 and blank 0.5 below the leaf's face); T2 and F3 carry one, 70 below the foot of the bar pull",
         "close review 10; street review 2 (the keyhole 70 below the pull's CENTRE would lie behind the 270 mm bar, 135 each way: placed below its foot)")

    # ---- T2's hinge-stile fitting (street 5, close 1): a row
    if not any(c["id"] == "FU-T2-hinge_fixing" for c in N["checks"]):
        at = [i for i, x in enumerate(N["checks"]) if x["id"] == "FU-T2-number-NM6"][0] + 1
        N["checks"].insert(at, {"id": "FU-T2-hinge_fixing", "group": "FU", "name": "T2: the small dark two-part fitting on the hinge stile", "kind": "T2",
                                "what": "two steel_dark boxes 20 x 25, 10 apart, 8 proud, in the door file (parts iron_hinge_fixing_1 and _2): their centre in the leaf frame and their size together",
                                "expect": {"u": 753.0, "v": 1390.0, "size": [20.0, 60.0], "proud": 8.0, "parts": 2}, "tol": 3.0,
                                "src": "target kinds.T2.small_fixings (D3); street review 5 and close review 1: the first build left it out", "type": "kind_fixing"})
    note("T2: the hinge-stile fitting is built (two boxes 20 x 25, 10 apart, centred u 753, v 1390, 8 proud) and has a row, FU-T2-hinge_fixing", "street review 5, close review 1")

    # ---- the two neighbours and the twin F1s (street 7)
    for h in N["street"]["houses"]:
        if h["house"] == "west_north_bay1":
            h["paint"] = "brown"
            h["why"] = "a household door in the row: two long panels as D1's left door, a bar pull on the left stile; brown (13 Oct, from the try 1 reviews: dark green put it next to F7's deep teal at a colour difference of 8.4)"
        if h["house"] == "west_north_bay0":
            h["paint"] = "dark_green"
            h["why"] = h["why"].replace("maroon is the sheet's deep red", "dark green (13 Oct, from the try 1 reviews: it was maroon, the twin of east_parade_bay0)")
    note("west_north_bay1 (F3) is brown (was dark green); west_north_bay0 (F1) is dark green (was maroon)",
         "street review 7: F3 dark green next to F7 deep teal measured a colour difference of 8.4 against 15 to 60 for every other neighbouring pair; the two maroon F1s were twins")

    # ---- the numbers (street 3, 4; close 8): the digits stay placeholders, now British and round-bowled
    N["numbers_note"] = ("13 Oct, from the try 1 reviews: the placeholder digits are odd on the west (cottage) side and even on the east side, rising from the quay, two digits at most "
                         "(T1 17, T2 21, F3 29; F2 14), and drawn with round bowls (2, 3, 5, 6, 9, 0, 8 and a closed 4) in strokes 6 mm on the 56 mm digits. None is canon; the town assigns the real ones.")
    note("house numbers: odd on one side and even on the other, rising from the quay, two digits at most (T1 17, T2 21, F3 29, F2 14); strokes with round bowls", "street review 3 and 4, close review 8")

    # ---- the glass and the nets (street 1, close 7); the reeded glass's own material (street 6)
    N["glass"][[k for k in N["glass"] if k.startswith("plain")][0]]["base_srgb_note"] = "13 Oct, from the try 1 reviews: the clear glass of the kit's files has base colour (235, 238, 236); the first build inherited 3.1's (121, 131, 139), which tinted every pane dark"
    N["glass"]["reeded_4mm"]["material"] = "glass_reeded: its own material, rough in transmission (the PC gives it an obscure glass); no texture in the file"
    note("glass: base colour (235, 238, 236) for every clear pane; reeded glass its own material glass_reeded; T2's net cards take the windows' net material net_voile (white 238, 238, 232)",
         "street review 1 and 6, close review 7")

    N["status"] = "built; the try 1 reviews' corrections applied 13 Oct 2026 (see changes_after_the_build); try 2 awaiting its second fresh review"
    N["changes_after_the_build"] = log
    out = json.dumps(N, indent=1, ensure_ascii=False)
    if out != raw:
        open(PATH, "w", encoding="utf-8").write(out)
    for c in log:
        print("-", c["change"])
    print("target.json %s (%d changes)" % ("written" if out != raw else "unchanged", len(log)))


DOC = os.path.join(HERE, "..", "..", "targets", "front-doors-all", "TARGET.md")


def patch_doc(log):
    """TARGET.md: the statements the changes supersede are patched in place (each marked), and a section 16, "Changes after the build", lists every change. Idempotent."""
    t = open(DOC, encoding="utf-8").read()
    mark = " (%s)" % WHEN
    reps = [
        ("| west_north_bay1 | west 35.23 | a shop of the west shop row | 838, leaf 766 x 1981 | F3 | F | dark_green | tired | plate LP1, handle HD3, number NM3 |  |",
         "| west_north_bay1 | west 35.23 | a shop of the west shop row | 838, leaf 766 x 1981 | F3 | F | brown (13 Oct, from the try 1 reviews; was dark_green) | tired | plate LP1, handle HD3, number NM3, keyhole KH1 |  |"),
        ("| west_north_bay0 | west 41.23 | a shop of the west shop row (north end) | 838, leaf 678 x 1981 | F1 | F | maroon | kept |",
         "| west_north_bay0 | west 41.23 | a shop of the west shop row (north end) | 838, leaf 678 x 1981 | F1 | F | dark_green (13 Oct, from the try 1 reviews; was maroon) | kept |"),
        ("| T2 | T | maroon | tired | plate LP5, handle HD3, number NM6 |  |", "| T2 | T | maroon | tired | plate LP5, handle HD3, number NM6, keyhole KH1 |  |"),
        ("Members (structural, mm): border 65.\n\n| opening | type | u0 | u1 | v0 | v1 | moulding or glass |", "Members (structural, mm): border 62.5" + mark + ".\n\n| opening | type | u0 | u1 | v0 | v1 | moulding or glass |"),
        ("| a 14 mm cove at this line too |", "| a 6 mm step over 6 mm at this line too" + mark + " |"),
        ("a margin of about 70 to 85 between them; the margin is a flat raised border with a 14 mm cove at each line (3 mm down at the outer line to the margin, 3 mm more at the inner line to the field, which is 6 below the border face); the border is 65 wide all round;",
         "a margin of about 62.5 between them at the sides; the margin is a flat raised border with a quirked (quarter-circle) cove at each line, each step 6 mm deep over 6 mm across (6 mm down at the outer line to the margin, 6 mm more at the inner line to the field, which is 12 below the border face)" + mark + "; the border is 62.5 wide at the sides;"),
        ("Leaf 838 x 1981 x 38 mm, ledged and braced matchboarding,", "Leaf 838 x 1981 x 47 mm" + mark + ", ledged and braced matchboarding (boards 22, ledges 25, braces 25),"),
        ("| BS1 | cast-iron boot scraper beside the step | [330.0, 130.0, 200.0] |", "| BS1 | cast-iron boot scraper beside the step | [404.0, 130.0, 200.0]" + mark + " |"),
        ("| LP2 | brass plate, horizontal, above the lock rail | [195.0, 70.0] | F2: u leaf centre, v 1545 | brass (181,150,85) |", "| LP2 | chrome plate, horizontal, above the lock rail" + mark + " | [195.0, 70.0] | F2: u leaf centre, v 1545 | nickel or chrome-look (170,170,168) |"),
        ("| HD2b | lever handle on a round rose, chrome-look, left stile |", "| HD2b | lever handle on a long backplate 40 x 170 with a keyhole 57 below its centre" + mark + ", chrome-look, left stile |"),
        ("| HD2c | short lever at the lock edge of a moulded door |", "| HD2c | short lever on a long backplate 40 x 170 with a keyhole 57 below its centre" + mark + ", at the lock edge of a moulded door |"),
        ("| HD3 | vertical bar pull on the lock stile |", "| HD3 | vertical bar pull on the lock stile: a round grip 19 across on two posts flaring into roses, stand-off 30" + mark + " |"),
        ("| HD4 | thumb latch on a ledged door |", "| HD4 | thumb latch on a ledged door: a plate with cusped ends, a round bow 19 across on posts 120 apart, a thumb lever 14 x 45 at 15 degrees" + mark + " |"),
        ("| KH1 | plugged mortice keyhole: a round head over a parallel slot, a dark recess 2 mm sunk, a pale metal blank filling the slot | [23.0, 32.0] | F1: u 782.8, v 1151; F2: u 782.8, v 1188.1 |",
         "| KH1 | plugged mortice keyhole: a round head over a parallel slot, a dark recess 2 mm sunk (a blind pocket 2.2 deep in the leaf), a pale metal blank filling the slot | [23.0, 32.0] | F1: u 782.8, v 1151; F2: u 782.8, v 1188.1; T2: u 57.2, v 1031.6; F3: u 67, v 1050" + mark + " |"),
    ]
    for a, b in reps:
        if a in t:
            t = t.replace(a, b)
    import re
    prof = json.load(open(PATH, encoding="utf-8"))["kinds"]["T3"]["mouldings"]["outside"]["profile_dh"]
    line = ("Profile (d across the face from the moulding's outer edge, depth below the border face, mm)" + mark + ": " + " ".join("(%g,%g)" % (round(d, 2), round(h, 2)) for d, h in prof) + ".")
    a3, b3 = t.index("### T3:"), t.index("### F1:")                                   # only T3's section: the other kinds have profiles of their own
    t = t[:a3] + re.sub(r"Profile \(d across the face from the moulding's outer edge, [^\n]*", lambda m_: line, t[a3:b3], count=1) + t[b3:]
    head = "\n## 16. Changes after the build (13 Oct, from the try 1 reviews)\n"
    if head not in t:
        t = t.rstrip("\n") + "\n" + head
    else:
        t = t[:t.index(head)] + head
    t += ("\nThe doors were built (production/cloud-week/kit/front-doors-all/) and two fresh reviews, one of the street view and one of the close view (REVIEW-doors-v1-street.md and "
          "REVIEW-doors-v1-close.md in that folder), failed the first build. Each correction to THIS target that they list is made below, in `target.json` (its `status` and a "
          "`changes_after_the_build` list say so) and, where it superseded a statement, in the body above, marked \"(13 Oct, from the try 1 reviews)\". The kit's script "
          "`kit/front-doors-all/target_changes_try2.py` applies them and can be run again (it changes nothing the second time). The target's makers (`td_*.py`, `make_target.py`, `make_doc.py`) "
          "and its reference drawing (`target_drawing.py`) are NOT changed: they are not this unit's files, and regenerating the target from them would undo these changes; they are owed the "
          "same changes (the drawing's moulding ring starts 4.8 outside the opening's edge, its `reeded_section` has a 2.8 base).\n\n| change | why |\n|---|---|\n")
    for c in log:
        t += "| %s | %s |\n" % (c["change"].replace("|", "/"), c["why"].replace("|", "/"))
    t += ("\nStill as the first target had it, because the reviews found it right: T2's four lights and its fanlight, F2's plate (placed 5 mm above its number in the kit, see NOTES.md), the frame sets, "
          "F1, F4, F5, F6's plate, lever and lock, the 15 paints and the three conditions.\n")
    open(DOC, "w", encoding="utf-8").write(t)


if __name__ == "__main__":
    main()
    json_log = json.load(open(PATH, encoding="utf-8"))["changes_after_the_build"]
    patch_doc(json_log)
    print("TARGET.md patched")
