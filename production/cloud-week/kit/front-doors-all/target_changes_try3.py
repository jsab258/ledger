"""The corrections to the target that the two fresh try 2 reviews list (14 October 2026), applied to production/cloud-week/targets/front-doors-all/target.json and TARGET.md.

    /home/user/.bpyenv/bin/python target_changes_try3.py            # applies them (idempotent: a second run changes nothing) and prints each change

Run after target_changes_try2.py (which holds the 13 October changes). target.json is the one home of the target's numbers: its makers (td_*.py, make_target.py, make_doc.py) hold the
FIRST draft, are frozen (they refuse to run without --first-draft and then write to target.first-draft.json) and are not changed any further. Each change is also written into
target.json under "changes_after_the_build", dated "14 Oct, from the try 2 reviews". The target's drawing (target_drawing.py) was changed to draw the bolection ring with its lap.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TD = os.path.join(HERE, "..", "..", "targets", "front-doors-all")
PATH = os.path.join(TD, "target.json")
DOC = os.path.join(TD, "TARGET.md")
WHEN = "14 Oct, from the try 2 reviews"


def add_once(d, key, text):
    if text not in d.get(key, ""):
        d[key] = d.get(key, "") + text


def spiral(cx, cz, r0, r1, a0_deg, sweep_deg, step_deg):
    """Points of a spiral about (cx, cz): the radius runs linearly from r0 to r1 while the angle runs from a0 through sweep (degrees, signed), every step_deg."""
    n = int(round(abs(sweep_deg) / step_deg))
    out = []
    for i in range(n + 1):
        t = i / float(n)
        a = math.radians(a0_deg + sweep_deg * t)
        r = r0 + (r1 - r0) * t
        out.append([round(cx + r * math.cos(a), 2), round(cz + r * math.sin(a), 2)])
    return out


def insert_after(checks, after_id, rec):
    if any(c["id"] == rec["id"] for c in checks):
        return
    at = [c["id"] for c in checks].index(after_id) + 1
    checks.insert(at, rec)


def main():
    raw = open(PATH, encoding="utf-8").read()
    N = json.loads(raw)
    log = []

    def note(what, why):
        if not any(c["change"] == what for c in log):
            log.append({"change": what, "why": why, "date": WHEN})

    # carry the try 2 log forward (its entries stay; these are added after them)
    log = list(N.get("changes_after_the_build", []))
    log = [c for c in log if c.get("date") != WHEN]

    # ---- the chrome colour (close review 4): one colour for the seven fittings and the spyhole ring
    F = N["furniture"]
    for slot, vid in (("letter_plate", "LP2"), ("letter_plate", "LP4"), ("handle", "HD2a"), ("handle", "HD2b"), ("handle", "HD2c"), ("latch", "LK1"), ("latch", "LK2")):
        F[slot][vid]["srgb"] = [196, 197, 196]
        F[slot][vid]["roughness"] = 0.35
        add_once(F[slot][vid], "src", "; 14 Oct, from the try 2 reviews (close review 4): chrome_nickel is sRGB (196, 197, 196), roughness 0.35 (170, 170, 168 is linear 0.40 against measured chromium's 0.55: the plates read at half P2's brightness)")
    N["chrome_nickel"] = {"srgb": [196, 197, 196], "roughness": 0.35, "metal": 1.0, "used_by": ["LP2", "LP4", "HD2a", "HD2b", "HD2c", "LK1", "LK2", "the spyhole ring of F6"],
                          "note": "one material, so one colour; the kit's make_mats reads it from the seven fittings' srgb and stops if they differ; judge it beside P2 in the game's light"}
    note("chrome_nickel (LP2, LP4, HD2a, HD2b, HD2c, LK1, LK2 and F6's spyhole ring) is sRGB (196, 197, 196), roughness 0.35, in place of (170, 170, 168)",
         "close review 4: the chrome-look parts read at about half the brightness of P2's plate (ratio to the black door 2.3 against P2's 3.7 to 4.1); (170, 170, 168) is linear 0.40, measured chromium 0.55")

    # ---- the grips' clear gap (close review 2): 30 behind the grip, so the axis stands 39.5 off the face (off the plate for HD4)
    hd3 = F["handle"]["HD3"]
    hd3["stand_off"] = 39.5
    hd3["proud"] = 49.0
    hd3["clear_gap_behind_grip"] = 30.0
    hd3["name"] = "vertical bar pull on the lock stile: a round grip on two posts that flare into roses, 30 clear behind the grip"
    add_once(hd3, "src", "; 14 Oct, from the try 2 reviews (close review 2): 'stand-off' means the clear gap behind the grip, 30 (a hand needs 30 to 40): the grip's axis stands 39.5 off the face and the grip 49 proud "
                         "(the first numbers read it as face to axis, 30, leaving 20.5 clear); the posts are lengthened to match")
    hd4 = F["handle"]["HD4"]
    hd4["stand_off"] = 39.5
    hd4["clear_gap_behind_grip"] = 30.0
    hd4["bar"] = "replaced by the bow: a round bar 19 across, 150 long with domed ends, bowed 4, 30 clear behind it (its axis 39.5 off the plate), on posts 120 apart"
    add_once(hd4, "src", "; 14 Oct, from the try 2 reviews (close review 2): the bow's axis stands 39.5 off the plate (30 clear behind it)")
    note("HD3: the grip's axis 39.5 off the face (stand_off), 49 proud, the clear gap behind the grip 30; HD4: the bow's axis 39.5 off the plate, 30 clear behind it",
         "close review 2: 'stand-off' is the clear gap behind the grip; the first build read it as face to axis and left 20.5 clear, too tight for a hand (30 to 40)")

    # ---- the thumb lever (close review 1)
    hd4["thumb"] = {"length": 45.0, "width": 14.0, "pad_dia": 20.0, "rise_deg": 15.0, "leaves_the_face_at_deg": 75.0}
    hd4["thumb_piece"] = ("a flat lever 14 wide and 45 long that leaves the plate through the slot in its head pointing out at the street and rising 15 degrees above the horizontal (75 degrees to the "
                          "face), its last 20 mm rounded into a pad 20 across; its end is about 43 out and 12 above the slot (14 Oct, from the try 2 reviews; the first build stood it upright, 17 degrees off the face)")
    add_once(hd4, "src", "; 14 Oct, from the try 2 reviews (close review 1): the thumb lever leaves the plate at 75 degrees to the face, 15 above the horizontal, 45 long, with a 20 pad")
    note("HD4: the thumb lever leaves the plate at 75 degrees to the face (15 above the horizontal), 45 long, its last 20 mm a pad 20 across; it reaches at least 40 out and rises at most 15 above its slot",
         "close review 1: it stood upright above the plate (13.7 out, 17 degrees off the face) like a fin; a thumb lever points at the street and is pressed down")

    # ---- T3: the quirk (street review 1; the close review's point 3 is met by the same grooves)
    q = N["kinds"]["T3"]["mouldings"]["outside"]
    q["quirk"] = {"width": 5.0, "depth": 3.0, "gap_to_outline": 0.1,
                  "where": "outside each of the four outlines (the outer and the inner outline of both panels), cut into the higher surface (the face at the outer outline, the margin 6 below the face at the inner outline), "
                           "square-bottomed, all the way round and following the upper panel's segmental head; its inner edge 0.1 mm off the outline, so a sliver of the arris stays between it and the cove",
                  "src": "street review of 14 Oct, narrow point 1: tested in the reviewer's own light, 5 x 3 grooves lifted the left-hand outlines from 3.0 and 2.2 per cent to 17.0 and 14.3 and the right-hand ones to 12.9 and 11.3"}
    add_once(q, "note", "; 14 Oct, from the try 2 reviews: a quirk, a square-bottomed groove 5 wide and 3 deep outside every outline (see `quirk`), because the left-hand outlines dipped 1 to 2 per cent in the street view")
    for c in N["checks"]:
        if c["id"] == "PL-T3-street-dip":
            add_once(c, "src", "; 14 Oct, from the try 2 reviews: the row stays at 10 per cent for every outline (the close review's 10 and 3 per cent split is not taken: the street view is where the lines are seen, and the street review's grooves give 11 to 17)")
    note("T3: a quirk, a groove 5 wide and 3 deep outside each of the four outlines of both panels (the head's arc included), its inner edge 0.1 off the outline; PL-T3-street-dip stays at 10 per cent",
         "street review 1 (left-hand outlines dip 1 to 2 per cent against D4's 22 and 5; tested 11 to 17 with the grooves); the close review's 3 (a 3 x 3 quirk on the outer outlines only, a 10 and 3 per cent split) is superseded by the street review's, the view the lines are seen from")

    # ---- the boot scraper's scrolls (close review 6): a point every 7.5 degrees
    bs = F["scraper"]["BS1"]
    pts = [[25.0, 0.0], [0.0, 0.0], [0.0, 154.0], [0.0, 169.0]]
    outer = spiral(35.0, 169.0, 35.0, 23.0, 180.0, -270.0, 7.5)             # radius 35 to 23 over 270 degrees, from the bar's top (0, 169) round the outside to (35, 146)
    inner = spiral(35.0, 169.0, 11.0, 23.0, -90.0, 270.0, 7.5)              # radius 11 to 23 back round the inside to (12, 169)
    bs["standard_profile_xz"] = pts + outer[1:] + inner + [[25.0, 154.0]]
    bs["scroll"] = {"centre": [35.0, 169.0], "outer_radius": [35.0, 23.0], "inner_radius": [11.0, 23.0], "step_deg": 7.5, "max_facet_mm": 5.0,
                    "note": "14 Oct, from the try 2 reviews (close review 6): a point every 7.5 degrees on both spirals (it was every 30), so no facet of the scroll is longer than 5 mm"}
    note("BS1: both spirals of the scroll resampled every 7.5 degrees (a point list of %d points; it was 24): no facet longer than 5 mm" % len(bs["standard_profile_xz"]),
         "close review 6: the scrolls read as 8 to 10 straight facets of 16 to 18 mm")

    # ---- new rows
    ck = N["checks"]
    base = {"tol": 1.0}
    for kind, vid, name in (("T2", "HD3", "T2: the bar pull's grip stands clear of the face"), ("F3", "HD3", "F3: the bar pull's grip stands clear of the face"),
                            ("F7", "HD4", "F7: the thumb latch's bow stands clear of its plate")):
        after = {"T2": "FU-T2-handle-HD3", "F3": "FU-F3-handle-HD3", "F7": "FU-F7-handle-HD4"}[kind]
        insert_after(ck, after, {"id": "FU-%s-grip_gap" % kind, "group": "FU", "name": name, "kind": kind, "slot": "handle", "variant": vid,
                                 "what": "the clear gap behind the grip: from the face (the plate's face for HD4) to the grip's nearest surface, measured on the built parts",
                                 "expect": {"gap": 30.0, "min_gap": 28.0}, "tol": 1.0, "src": "close review 2 (14 Oct): at least 28, as designed 30 (a hand needs 30 to 40)", "type": "grip_gap"})
    insert_after(ck, "FU-F7-grip_gap", {"id": "FU-F7-thumb", "group": "FU", "name": "F7: the thumb lever reaches out and does not stand upright", "kind": "F7", "slot": "handle", "variant": "HD4",
                                        "what": "the thumb lever's end stands at least 40 out from the plate's face and rises at most 15 above the slot's centre; it clears the bow by at least 2 where it passes over it",
                                        "expect": {"out_min": 40.0, "rise_max": 15.0, "clear_over_bow_min": 2.0}, "tol": 0.0,
                                        "src": "close review 1 (14 Oct): the first build's reached 13.7 out", "type": "thumb_reach"})
    insert_after(ck, "FU-T1-scraper-BS1", {"id": "FU-T1-scraper-facets", "group": "FU", "name": "T1: the scraper's scrolls are smooth", "kind": "T1", "slot": "scraper", "variant": "BS1",
                                           "what": "no straight facet of either scroll's spiral is longer than 5 mm in the built standard (the cut section of the part, outline segments between the scroll's two ends)",
                                           "expect": {"max_facet_mm": 5.0}, "tol": 0.0, "src": "close review 6 (14 Oct)", "type": "scraper_facets"})
    insert_after(ck, "PL-T3-street-dip", {"id": "PL-T3-quirk", "group": "PL", "name": "T3: a quirk groove 5 wide and 3 deep outside the outlines", "kind": "T3",
                                          "what": "in sections of the leaf (across the lower panel's left edge, its foot, the upper panel's head, and each panel's inner outline) the surface just outside the outline is a flat groove 3 below the "
                                                  "surface it cuts (the face at the outer outline, the margin at the inner), 5 wide within 0.6, and beyond it the surface is back at its level",
                                          "expect": {"width": 5.0, "depth": 3.0, "sections": 6}, "tol": 0.6, "src": "street review 1 (14 Oct)", "type": "quirk"})
    insert_after(ck, "GA-F7-views", {"id": "GA-T2-nets-lit", "group": "GA", "name": "T2: the nets read a little darker than the white frame", "kind": "T2",
                                     "what": "on the street picture the four lights' median brightness (less their bars) is 0.80 to 0.90 of the transom bar's front face (D3's nets read 0.84 to 0.87 of the stile's white)",
                                     "expect": {"ratio_of_transom_bar": [0.80, 0.90]}, "tol": 0.0,
                                     "src": "street review 2 (14 Oct): the nets read 0.95 to 1.0 of the transom bar, brighter than the white frame; in place of 'at least 0.75 of the jamb'", "type": "nets_lit"})
    insert_after(ck, "GA-T2-nets-lit", {"id": "MAT-chrome_nickel", "group": "MAT", "name": "chrome_nickel is one colour, the target's", "kind": "all",
                                        "what": "the base colour of the material chrome_nickel in every furniture file and in door_F6.glb (the spyhole ring) is the target's chrome_nickel srgb",
                                        "expect": {"srgb": [196, 197, 196]}, "tol": 2.0, "src": "close review 4 (14 Oct); the kit typed (170, 170, 168) in a second place", "type": "chrome_colour"})
    insert_after(ck, "MAT-chrome_nickel", {"id": "TG-makers-frozen", "group": "TG", "name": "the target's first-draft makers cannot overwrite target.json", "kind": "all",
                                           "what": "make_target.py and make_doc.py hold the guard (they exit with 'frozen' unless --first-draft is given) and running make_target.py leaves target.json byte for byte as it was",
                                           "expect": {"guard": "is frozen", "files": ["make_target.py", "make_doc.py"]}, "tol": 0.0,
                                           "src": "street review 3 and close review 7 (14 Oct): the makers hold the first draft's numbers and would undo the review fixes (a regenerated file differs from target.json in over 1,600 places); "
                                                  "frozen rather than rewritten, because target.json is the home since the 13 October fixes were made in it directly", "type": "makers_frozen"})
    note("new rows: FU-T2-grip_gap, FU-F3-grip_gap, FU-F7-grip_gap, FU-F7-thumb, FU-T1-scraper-facets, PL-T3-quirk, GA-T2-nets-lit (0.80 to 0.90 of the transom bar), MAT-chrome_nickel, TG-makers-frozen",
         "the reviews' tests for their points")
    note("the target's makers (make_target.py, make_doc.py) are frozen with a guard; target_drawing.py draws the bolection ring with its lap and the T3 section closes at 16 deep",
         "street review 3, close review 7: the makers hold the first draft and would undo the fixes (1,659 differences); the three literal moulding extras failed only because the drawing's ring started at the opening's edge")
    note("T2's nets (a render aid, not in any file): random folds 30 to 70 mm apart, brightness 0.78 plus or minus 0.11, scaled so the lights read 0.85 of the transom bar's face",
         "street review 2: they read 0.95 to 1.0 of the transom bar (brighter than the white frame) and the folds repeated every 48 mm like a pleated blind")

    N["status"] = "built; the try 1 reviews' corrections (13 Oct) and the try 2 reviews' narrow points (14 Oct) applied (see changes_after_the_build); fixes applied, not re-reviewed (Jafar, 11 October)"
    N["changes_after_the_build"] = log
    out = json.dumps(N, indent=1, ensure_ascii=False)
    if out != raw:
        open(PATH, "w", encoding="utf-8").write(out)
    for c in log:
        if c.get("date") == WHEN:
            print("-", c["change"])
    print("target.json %s" % ("written" if out != raw else "unchanged"))
    patch_doc(log)
    print("TARGET.md patched")


def patch_doc(log):
    """TARGET.md: the statements the changes supersede are patched in place (each marked) and a section 17, "Changes after the try 2 reviews", lists every change. Idempotent."""
    t = open(DOC, encoding="utf-8").read()
    mark = " (%s)" % WHEN
    reps = [
        ("a round grip 19 across on two posts flaring into roses, stand-off 30 (13 Oct, from the try 1 reviews)",
         "a round grip 19 across on two posts flaring into roses, 30 clear behind the grip (its axis 39.5 off the face)" + mark),
        ("a plate with cusped ends, a round bow 19 across on posts 120 apart, a thumb lever 14 x 45 at 15 degrees (13 Oct, from the try 1 reviews)",
         "a plate with cusped ends, a round bow 19 across on posts 120 apart, 30 clear behind it, a thumb lever 14 x 45 leaving the plate at 75 degrees to the face with a 20 pad" + mark),
        ("nickel or chrome-look (170,170,168)", "nickel or chrome-look (196,197,196; 14 Oct, from the try 2 reviews)"),
    ]
    for a, b in reps:
        if a in t:
            t = t.replace(a, b)
    head = "\n## 17. Changes after the try 2 reviews (14 Oct, from the try 2 reviews)\n"
    if head in t:
        t = t[:t.index(head)]
    t = t.rstrip("\n") + "\n" + head
    t += ("\nTwo fresh try 2 reviews (the street view and the close view, REVIEW-doors-v2-street.md and REVIEW-doors-v2-close.md in kit/front-doors-all/) passed the doors with no fault and 4 and 7 narrow "
          "points. Each correction to THIS target is made in `target.json` (its `status` and `changes_after_the_build` say so) by `kit/front-doors-all/target_changes_try3.py`, which can be run again "
          "(it changes nothing the second time). target.json is the home of the numbers: `make_target.py` and `make_doc.py` hold the first draft and are frozen (they refuse to run without "
          "`--first-draft`, which writes `target.first-draft.json` and `TARGET.first-draft.md` instead); `target_drawing.py` draws the bolection ring with its lap.\n\n| change | why |\n|---|---|\n")
    for c in log:
        if c.get("date") == WHEN:
            t += "| %s | %s |\n" % (c["change"].replace("|", "/"), c["why"].replace("|", "/"))
    open(DOC, "w", encoding="utf-8").write(t)


if __name__ == "__main__":
    main()
