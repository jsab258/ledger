#!/usr/bin/env python
"""Writes TARGET.md from target.json (the numbers are read from it, not retyped) and the narrative below.

    /home/user/.bpyenv/bin/python make_doc.py        (run after make_target.py; run self_check.py; run this again to carry the last result line; run self_check.py again)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "target.json")))
N = T["numbers"]
V = lambda k: N[k]["value"]  # noqa: E731
G = T["geometry"]["A"]
GC = T["geometry"]["C"]
LB = T["geometry"]["lantern"]
BR = G["bracket"]
PER = T["period_photographs"]
SC = T.get("self_check", {}) or {}
FIT = SC.get("us01_3d_fit") or {}
LAST = T.get("self_check", {}).get("result_line", "(not yet run)")
LAID = (T.get("self_check", {}) or {}).get("laid_on_photograph") or {}
prof = G["lower"]["outer_rz"]
chk = {c["name"]: c for c in T["checks"]}
ZC0, ZC1 = prof[-5][1], prof[-1][1]
STEM_TOP = BR["stem_to_z"]
AS, AE = BR["arm_start"], BR["arm_end"]
TURN, RAKE = BR["bend_turn_deg"], BR["rake_deg"]
SCREW_Z = G["socket"]["set_screws"]["z"]
SW1, SW2, SW3 = chk["shaft_od_low"]["expected"], chk["shaft_od_mid"]["expected"], chk["shaft_od_high"]["expected"]


def table(rows, head):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "/") for c in r) + " |")
    return "\n".join(out)


chk_rows = [(c["name"], c["applies_to"], c["measure"], json.dumps(c["expected"]), c["tolerance"], c["kind"]) for c in T["checks"]]
per_rows = [(p["id"], p["file"], p["page"], p["title"], p["author"], p["licence"], p["taken"], p["date_read"], p["kind"], p["what_it_shows"], p["used"]) for p in PER]
el_rows = [(p["id"], p["elements"]["bracket"], p["elements"]["reach"], p["elements"]["lantern"], p["elements"]["shaft_taper"], p["elements"]["base_door"], p["elements"]["root"]) for p in PER]
num_rows = []
for k, v in N.items():
    if v["kind"] in ("Photo", "Derived"):
        num_rows.append((k, json.dumps(v["value"]), v["unit"], v["kind"], v["source"][:230]))

md = f"""# {T['title']}

**{T['summary_line']}**

Written 9 October 2026, rewritten 11 October 2026 (try 2: the review of 9 October applied) for the family "lamp posts on Quay Street" (scene lines E1 lighting column and E2 sodium lantern, four of each). Units are millimetres unless a line says otherwise; the .glb is metres, z up, scale 1, the pivot the column's axis on the footway. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, plans and sections as polygons in millimetres and pictures at 1 mm a pixel); `self_check.py` tests them; `make_target.py`, `lamp_numbers.py`, `measure_photos.py`, `make_previews.py`, `lamp_us01.py`, `period_photos.json` and `make_doc.py` re-make everything (the 2019 photographs are Poly Haven's CC0 panoramas and the 1989 to 2010 ones are Geograph's: neither is in git; only reduced crops are, in production/previews/cloud-week/refs/lamp-posts/). Last result: {LAST} (`/home/user/.bpyenv/bin/python -I self_check.py`; it re-measures the previews, runs the drawing, lays US01 on the picture in 3D, recomputes the derived numbers and tries eighteen deliberately wrong copies of target.json, all of which it must refuse).

## 0. Read this first

1. **No photograph of 1990 was reached, and none of 1975 to 1995 of a precast concrete column with a sodium lantern.** The network opened on 11 October and was searched (section 2.2b): Geograph's feed, Wikimedia Commons and archive.org. What came back is two dated photographs of 1989 (two railway stations' painted steel columns, Peter Whatley, Geograph) that show the bracket's form, and three of 2008 to 2010 of concrete columns that the photographers say are original or old (section 0.5). The 2019 Poly Haven panoramas (US01 and BGE, Andreas Mischok) still give the steel column's lower form. So nothing here is a 1990 measurement of a concrete column: every concrete length is Judgement within what the photographs allow, and says so.
2. **The approved Hook sheet shows no lighting column.** The brief's "slender, dark column with a small flat canopy" is the RETIRED sheet's. The approved street panel (production/reference/hook-sheet.png, approved 22 September; its reduced copy production/previews/hook-sheet-2026-10-05.jpg) shows no lighting column and no bracket lamp: read at full size on 9 October, the only vertical on its skyline is a mast on the far hill, as production/reference/retired-sheet-inheritance.md row 4 and game-design/research/GOVERNS.md already say. So no number below is read off a Hook sheet; the sheet governs mood (section 3).
3. **Kinds of number.** Every number in `target.json` `numbers` ({len(N)} of them) carries its kind: **Read** (printed in the repository or in a file this writer opened, with the file), **Photo** (measured on a photograph: method and error in section 4), **Derived** (computed from other numbers here; the formula is in its `source`), **Judgement** (a trade or period guess, said so). `number_kinds` counts them: {json.dumps(T['number_kinds']['counts'])}.
4. **The choice that is Judgement, reversed in try 2:** precast concrete (variant C) is the main build for all four places and painted steel (variant A) is the written-out alternative (review fault 2; DECISIONS.md 9 October 12:29, a session decision Jafar can overturn: one line on his page, "The street's lamp columns: concrete (recommended) or black steel"). Both share the bracket, the lantern, the light and the places.
5. **The photographs of try 2, and why the later ones count.** The brief accepts a later photograph "of an object unchanged since the period" when it says why. Here: GG1 and GG2 are of 1989 (steel, period). GG3 to GG5 are of 2008 to 2010 (concrete): their photographers call the column old, original or "vintage 1950s/60s" and one names an original low-pressure sodium lamp; precast columns of that kind stood unchanged until the late 1990s and 2000s (review fault 2), so the object is the one a 1990 street had; the lanterns are not all sodium or all original, and each page says what it says. They give the form of the bracket, the proportions of the column and the base, not paint, dirt or the date. **Each period photograph beats a book; a later one beats nothing but is a weaker witness**, and where one disagrees with the target the disagreement is written down (section 7, PW8 to PW12) and, if it could not be settled, listed (section 10).

## Try 2: the review's three faults and nine narrow points, and how each was answered

The first review (TARGET-REVIEW.md, 9 October 2026) FAILED the target on three faults and listed nine narrow points. Each is applied as the review writes it, in the makers (`lamp_numbers.py`, `make_target.py`, `target_drawing.py`, `make_doc.py`) and regenerated, and `self_check.py` has a part T with at least one test row for each (the part's rows are named by the fault or point). Where a photograph of 11 October shows otherwise the disagreement is written down and not silently followed.

{table([
    ("F1", "the bracket's 40 degree rake is perspective read as rake: US01's arm points about 42 degrees toward the camera, its true rake is 0 to 7 and the lantern lies on the arm's line", f"rake 0 (+-5): the stem vertical to z 4800.8, ONE 90 degree bend of radius 130, a level arm to (430, 4930.8); the boss horizontal and coaxial with the lantern; new check arm_lantern_coaxial (at most 2 degrees); US01 laid on the picture in 3D with the arm at bearing -147.8 in self_check part B (free rake {FIT.get('street_free_rake_deg', 'n/a')} degrees, a level arm fits to {FIT.get('street_rake0_median_mm', 'n/a')} mm, a 40 degree arm to {FIT.get('street_rake40_median_mm', 'n/a')} mm; read in the picture's plane it gives {FIT.get('plane_free_rake_deg', 'n/a')} degrees, the apparent slope); the 1989 photographs agree (arms rising 8 to 10 degrees or less in the picture, the lantern in line); wrong copy: a 40 degree rake into a level lantern", "5.3, 7 (PW8), 10"),
    ("F2", "steel as the main build and concrete as the unbuilt variant is backwards, and rests on 2019 photographs the brief does not accept as period evidence", "the roles swapped: C (precast concrete) is the main build for all four places, A stays in full as the alternative; C brought to A's standard: geometry.C.shaft as the point list (z, side, chamfer) (-150, 220, 15), (0, 220, 15), (4620, 125, 15), the top face flat with a 5 chamfer; geometry.C.bracket (a 48 stem through a 30 tall, 90 OD cast-steel cap, the same bend and level arm); geometry.C.door (recess 120 x 330 x 14 at z 450 to 780, plate 132 x 342 x 3, 3 proud, two screws 10 across at 25 from its ends, blank); its own checks (the shaft side at z 300, 2300 and 4300: 213.8 / 172.7 / 131.6, chamfer, section square to the street, door, cap and stem entry, albedo (146, 143, 136) +-12, roughness 0.9 +-0.1, no paint); concrete wear (algae to z 700 on -y, lime streaks from the top, rust bleed under the plate's screws, one chipped arris on LC 2 only); recorded in DECISIONS.md; checked against photographs from the network (section 0.5): the straight taper, the plain planted foot and the angular elbow agree, two curved-arm photographs do not (PW10)", "0.4, 0.5, 5.2, 6, 7 (PW6, PW10), 12"),
    ("F3", "the bracket reaches only 225 to the lantern, against the target's own Read source (406 to 457)", "reach to the spigot 430 (Read); the lantern's rear end at y 430, centre (0, 705, 4900), front end y 980; every canopy, bowl, lamp, holder, hinge and catch station +205; the light at (0, 705, 4850); checks lantern_centre, arm_reaches_boss and light_position updated; the centre then stands 65 mm behind the kerb face and the front end 210 mm over the channel; scene file handover: outreach_m 0.5 becomes 0.705; the 1989 steel columns show shorter reaches (2.8 and 5 tube widths, scale unknown) and Birchington (2008) a reach of 4.3 top widths: listed, not followed (PW9)", "5.4, 5.8, 7 (PW9), 12"),
    ("Point 1", "the socket: US01's shaft top is the bracket's socket sleeve, not a 60 mm collar", "variant A: socket z 4370 to 4620, OD 64, top edge chamfered 3, a seam at its foot, two M8 set screws on -y at z 4580 and 4420; the check collar is {od 64, z [4370, 4620]} +-4. With the shaft left as it is (60.4 at z 4370) the socket stands 3.8 proud, not 2: said in the numbers", "5A, checks"),
    ("Point 2", "the door's corners: US01's flush door has rounded top corners", "variant A: radius 15 on all four corners of the door and of its joint groove; check door_corner_radius 15 +-3 (the concrete door plate's corners are 10: Judgement)", "5A, checks"),
    ("Point 3", "the lamp's U-tube", "an arc tube inside the 54 x 310 jacket: two legs of 16 OD at x +-11 running y 555 to 845 (straight to 826, a half-torus of centreline radius 11 at the front), the full-strength emissive part, the jacket glass at 0.3 of it", "5.4, 5.7"),
    ("Point 4", "emissive strength in units", "the jacket about 27,500 cd/m2 (4,550 lm over its 0.0526 m2), the bowl about 5,500 (80 % of the flux through about 0.21 m2, Lambertian), the tube 27,500 / 0.3 about 91,700; or both follow VignetteShot.cpp's kLampEmissiveUnitless = 1.0 times the lantern colour in linear (1, 0.25, 0) until the night audit; both stated", "5.7"),
    ("Point 5", "the jacket's colour (255, 176, 28) contradicts 'a sodium lamp's own light is one orange'", "the first of the review's two options: the jacket is (255, 137, 0) at full strength like the tube and the bowl; the yellow core is the camera's clipping, left to the grade; the check glow_colour_lamp is (255, 137, 0) +-12", "5.5, 5.7"),
    ("Point 6", "the check lantern_dome_height reads 'at y = 500' but expects 63, the geometry gives 61 there", "'the maximum over y, 63 +-6' (the maximum is 63 at y 605; at the lantern's centre y 705 it is 61)", "checks"),
    ("Point 7", "the cone's angle: the text says 24 degrees, the profile gives 25.0", "the text says 25 degrees off the vertical", "5A"),
    ("Point 8", "W1's 10 degree arm enters a level lantern, the same kink as F1", "W1's arm is level and coaxial with the lantern (rake 0), reaching 430, the lantern's rear boss on its end; the lantern then stands 581 lower than on the column", "6"),
    ("Point 9", "the shaft's top on a bracket column is 60 (BGE's post-top column's)", "left as it is, with the review's note on variant A: if A is built (C ruled out), use 64 to 68 at z 4560 (a straight taper from 68, nearly parallel), the socket then made 4 to 6 larger than the shaft top so that the stem and socket do not look heavier than the shaft; not applied to A's numbers now that C is the main build", "6, 10"),
], ("id", "the review's finding", "how it was answered", "where"))}

**Photographs that disagree with the review's amendments, and what was chosen** (the brief: the photograph wins, element by element; with five 640 px photographs and unknown scales the choice is written, not hidden): the bend's radius is 130 as the review gives it (three diameters) although Birchington's elbow reads about 55 and Appley Bridge's about 2 diameters, so the check's tolerance is +-75 (PW11); the reach is 430 as the research and the review say although the two 1989 steel columns (railway fittings, scale unknown) show 170 to 300 (PW9); the lantern is 550 long as the scene and the review say although three photographs show 12 to 14 widths of a slim steel tube and 7 widths of a concrete top, 700 to 880 (PW12); the arm is angular as the review says although two of the three concrete photographs show a curved gooseneck (PW10). Each is on the list of what the PC should settle first (section 10).

## 1. What today's stand-in gets right, and what this target changes

Today's stand-in (SCENE-SLOTS.md; production/specs/vignette-scene.json `lighting`; StreetVignette.cs `Columns()`, read 9 October): a base cylinder 200 across and 300 high, ONE 114 mm shaft from 300 to 5000, a swan neck of three short cylinders (0.8 x the shaft) on a quarter circle rising over the lantern, a box lantern 550 along the street x 300 x 200 with its top at 5000 and its centre 500 from the axis, emissive, colour (255, 219, 0). "Trade-standard guesses, not photographs".

{table([
    ("the place", "x 8, 18, 28, 38; east, west, east, west; axis 0.6 m behind the kerb's back face", "the same (the code's loop; SCENE-SLOTS.md's 'every 20 m' is 20 m on one side)", "Read"),
    ("lower column", "base 200 x 300, then a 114 shaft to 5000", "C (main): a SQUARE precast shaft 220 at the foot tapering to 125 at 4620, arrises chamfered 15, planted, a cast cap on top; A (alternative): a 124 sleeve 978 high, a 60 mm cone with a ring line, a shaft 68 tapering to 60, a socket 64 from 4370 to 4620", "Judgement (C: the research's 20 to 25 cm, the photographs of 2008 to 2010); Photo (A: BGE; the scene's 114 lies at the sleeve's lower error edge)"),
    ("bracket", "a swan neck: three cylinders rising over the lantern and dropping into it", "a plain bent arm: a stem (48 on C, 42 on A), ONE 90 degree bend of radius 130, a straight LEVEL arm 300 long reaching 430 from the axis into the lantern's rear boss", "Photo (US01 in 3D; the 1989 and 2008 photographs) + Read (the research's 406 to 457; R07 'plain bent-arm lighting')"),
    ("lantern", "a box 550 along the street x 300 x 200, centre 500 out", "a boat-shaped canopy over a deep yellowed bowl, the same 550 x 300 x 200 envelope turned so the long side lies ALONG THE ARM, its rear end 430 out, its centre 705, its front end 980", "Photo (US01 from below) + Read (the research's wording and reach)"),
    ("the glow", "one emissive box (255, 219, 0)", "the U-shaped arc tube, the jacket (54 x 310) and the bowl glow, all (255, 137, 0): about 91,700, 27,500 and 5,500 cd/m2", "Derived + Photo"),
    ("door, plate, fixings", "none", "C: a door recess 120 x 330 with a blank steel plate at z 450 to 780, a 90 x 45 plate 'LC n'; A: a flush door 100 x 500 at z 400 with rounded corners, the same plate, two socket set screws; both: hinge and catches on the bowl, grub screws on the boss", "Judgement"),
    ("light", "one light 18 m range, intensity 3.2; scene colour (1, 0.7055, 0)", "the night note's pool, skirt and glow at (0, 705, 4850); colour (1, 0.25, 0)", "Read (night note)"),
], ("", "the stand-in", "this target", "kind"))}

What the stand-in gets right: the four places and sides, the mounting height 5.0 (the lantern's top), the lantern's box size, the 589 nm lamp, the point light 0.05 below the centre, and the rule that the column is plain with no ornament. What it gets wrong: the outreach (0.5 to the lantern's CENTRE; the research's reach to the spigot is 0.43 and the centre then 0.705).

## 2. Sources

### 2.1 What was read, and what for

{table([
    ("S1", "production/specs/vignette-scene.json (lighting.column, lighting.lantern, street, blocks, cameras) and production/specs/vignette-pieces.json (column0..3, lantern0..3)", "2026-10-09", "the project", "the project's own", "2026-09-02 to 2026-10-08", "the stand-in's sizes and places; the lantern's colour, xy and range", "yes: Read numbers"),
    ("S2", "ledger/Assets/Scripts/Core/StreetVignette.cs Columns() (lines 1196 to 1262)", "2026-10-09", "the project", "the project's own", "2026-09", "the placement loop (x 8 while x <= 46, step 10, alternate sides, z = 3.125 + 0.6 = 3.725), the swan neck, the lantern's centre 0.5 out", "yes"),
    ("S3", "production/cloud-week/targets/SCENE-SLOTS.md; BRIEF.md", "2026-10-09", "the project", "the project's own", "2026-10-08", "the row for the lamp column; the brief's rules", "yes"),
    ("S4", "production/research/street-clutter-1990/SUMMARY-2026-09-29.md section 3 (the project's earlier reading, made on the PC from its sources)", "2026-10-09", "a helper, saved by the builder", "the project's own", "2026-09-29", "concrete columns with sodium lanterns; 4.6 to 6 m; 20 to 25 cm at the foot; a door plate about 50 cm up; an arm 40 to 45 cm; the lantern 7 3/4 in tall, 60 to 70 cm long (uncertain); a boat-shaped canopy over a deep clear trough bowl with a U-shaped tube; 'photographs 1985 to 1995 not found'. Its photograph links are links only (Geograph, Flickr, a lighting enthusiasts' site), all unreached from this cloud; the makers it names are not repeated here and appear on nothing", "yes: Read numbers, with its caution"),
    ("S5", "production/research/evening-light-1990/SUMMARY-2026-09-29.md", "2026-10-09", "a helper", "the project's own", "2026-09-29", "589 nm (0.569, 0.430), about sRGB (255, 140, 0), linear about (1, 0.25, 0); warm-up; 35 W SOX 4,550 lm", "yes"),
    ("S6", "production/cloud-week/research/1c-night-pools-lumen.md and production/audits/night-2026-10-08/GATE-NIGHT.md; DECISIONS.md 7 and 8 October", "2026-10-09", "the night note's writer", "the project's own", "2026-10-08", "the lamp's lumens, the pool, skirt and glow, the cones, the colour, the clipped red, the 4.78 m", "yes: the light block"),
    ("S7", "production/previews/morning-night-evening-2026-10-08.jpg (the street at night now)", "2026-10-09", "the project", "the project's own", "2026-10-08", "the stand-in at night: slim dark columns with long gooseneck arms over small boxes; pools on the flags", "looked at; no number taken"),
    ("S8", "production/reference/hook-sheet.png (2048 x 1088, read in four tiles at full size), production/previews/hook-sheet-2026-10-05.jpg, production/reference/hook-sheet-2026-09-09-retired.png, hook-sheet-audit.md, retired-sheet-inheritance.md, game-design/research/GOVERNS.md, photographs.md", "2026-10-09", "the project", "the project's own", "2026-09-09 to 2026-10-05", "the approved sheet shows no column and no bracket lamp (section 3); the retired poster shows a black post-top globe lantern and two box wall lanterns, each a few pixels wide", "yes: section 3"),
    ("S9", "production/cloud-week/targets/kerbs-and-covers/ and bollards/ (target.json, TARGET.md)", "2026-10-09", "their writers", "the project's own", "2026-10-09", "the corrected kerb (granite top 170, flags +110) and the camera heights of BGE (1.02 +-0.07) and US01 (1.16 above the footway)", "yes"),
    ("S10", "https://polyhaven.com/a/bethnal_green_entrance (BGE); https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/bethnal_green_entrance.jpg (8192 x 4096)", "2026-10-09", "Andreas Mischok", "CC0 1.0 (read at https://polyhaven.com/license, 9 October 2026: 'CC0 means absolute freedom')", "2019-08-18", "the Bethnal Green estate path; a black steel column with a post-top dish lantern at 4.4 m, 2.7 m from the camera", "yes: Photo numbers (sleeve, cone, shaft, pod width, paint, wear)"),
    ("S11", "https://polyhaven.com/a/urban_street_01 (US01); the same host's Tonemapped JPG urban_street_01.jpg", "2026-10-09", "Andreas Mischok", "CC0 1.0 (as S10)", "2019-08-18", "a steel stepped column about 11 m high with a bent-arm bracket and an amber lit cobra-head lantern, 8.8 m from the camera", "yes: ratios, the lit colour"),
    ("S12", "https://polyhaven.com/a/urban_street_02, urban_street_03, urban_street_04, birbeck_street_underpass, limehouse, cambridge, greenwich_park, greenwich_park_02, greenwich_park_03, epping_forest_01, epping_forest_02, roof_garden, canary_wharf, adams_place_bridge, leadenhall_market (the same Tonemapped JPG host)", "2026-10-09", "Andreas Mischok", "CC0 1.0", "2019-02-09 to 2019-12-17 (us02 2019-08-18; us03 2019-09-07; us04 2019-09-14; cambridge 2019-12-17; the parks 2019-02-09 to 2019-09-07; the rest 2019-05-19 and 2019-08-31)", "searched for lamp columns and wall lanterns (section 2.2)", "us02: a wall bulkhead measured (W1's note); the rest looked at only"),
    ("S13", "https://api.polyhaven.com/assets?type=hdris and https://api.polyhaven.com/files/<id>, /info/<id>", "2026-10-09", "Poly Haven", "CC0", "n/a", "the catalogue with coordinates and dates taken; the file URLs", "yes"),
] + [("S%d / %s" % (14 + i, p["id"]), p["page"] + " (" + p["title"] + "); the reduced crop " + p["file"], p["date_read"], p["author"], p["licence"], p["taken"], p["kind"] + ": " + p["what_it_shows"], p["used"]) for i, p in enumerate(PER)]
 + [("S19", "https://api.geograph.org.uk/syndicator.php?q=<words>&orderby=imagetaken&format=JSON (the feed: title, author, imageTaken, licence) and the photo pages https://www.geograph.org.uk/photo/<id> (read with a browser user agent)", "2026-10-11", "Geograph and its photographers", "CC BY-SA 2.0 per page", "n/a", "the search of section 2.2b; the date taken and the licence of each photograph read on its own page", "yes"),
    ("S20", "https://commons.wikimedia.org/w/api.php (search and categorymembers) and https://archive.org/advancedsearch.php", "2026-10-11", "n/a", "n/a", "n/a", "searches only (section 2.2b)", "no number taken")], ("id", "where", "date read", "author", "licence", "date taken", "what it shows or gives", "used"))}

All Poly Haven and Geograph material is used for measuring and looking only: not placed in the game, not traced into a texture, not fed to an image model. The Geograph pictures are 640 px copies; the crops in git are reduced to the object (a station sign is masked grey) and credited in section 13.

### 2.2 The search of the panoramas

Poly Haven lists seventeen HDRIs with coordinates in Britain (the Dublin sets at 53.3 N 6.2 W are not British and were left out; `st_fagans_interior` is a Welsh interior). Each of the seventeen was looked at as its 2k tone-mapped copy and, where a column showed, at 8192 px:

{table([
    ("urban_street_01", "one steel stepped column with a bent-arm bracket and a lit amber cobra-head lantern (US01)", "measured: ratios, lit colour, form of bracket and base"),
    ("bethnal_green_entrance", "one black steel stepped column with a post-top dish lantern, 2.7 m away (BGE), signs bolted on its shaft", "measured: the lower column, the pod's width, the paint and wear"),
    ("urban_street_04", "a decorative black column with a scroll bracket and a round glass lantern (Kensington)", "looked at: a 2000s heritage replacement, wrong for 1990 and for a northern port; not used"),
    ("urban_street_03", "one steel column with a raked arm, 6 px wide at 40 m", "looked at; too small to measure"),
    ("urban_street_02", "a black-backed opal wall bulkhead on a 1970s-80s brick block", "measured roughly (235 x 210 mm, brick courses): an estate fitting, W1's note"),
    ("cambridge", "two bespoke wrought-iron glazed wall lanterns of a college", "looked at: a one-off heritage piece, not a street fitting; a college's sign is in frame, so no preview"),
    ("birbeck_street_underpass, limehouse", "fluorescent battens under a viaduct; bollards and chain on a marina", "no column"),
    ("greenwich_park, _02, _03, epping_forest_01, _02, roof_garden, canary_wharf, adams_place_bridge", "parks, woods, a roof garden, offices, a footbridge", "no column"),
    ("leadenhall_market", "a covered market with ornate hanging lamps and shop lettering the content rule bars", "not used and not previewed (the content rule)"),
], ("panorama", "what it shows", "result"))}

None of the 2019 lamp columns is shown to be from 1990 or earlier, and none is a concrete column. The brief's expected case ("if no reachable photograph shows a period column, write the target from the earlier research, the existing recipe and the Hook sheet, and say plainly which numbers rest on what") is therefore the case, with the difference that the Hook sheet gives nothing and two 2019 photographs give the lower column's form.

### 2.2b The search of Geograph, Wikimedia Commons and archive.org (11 October 2026, the network open)

**Geograph** (the feed `syndicator.php`, `perpage=100`, `orderby=imagetaken`, the saved search's `i=` for page 2): about forty queries (lamp post, lamp-post, lamppost, street light, street lamp, lamp standard, lighting column, concrete lamp post / lamp standard / lighting column / column, sodium, sodium light, sodium lamp, low pressure sodium, bracket lamp and the years 1986 to 1991 beside 'lamp'); ordered by the date taken the first 200 hits of each query reach 2000, and about 350 photographs of 1970 to 2000 were listed and their titles and descriptions read; about forty were looked at as pictures. **Result:** the pre-2000 Geograph photographs that mention street lighting are few and are almost all railway stations, trams, buses and terraces with a lamp in a corner; the ones that show a lamp column well enough to read are Peter Whatley's two of Orrell station and one of Appley Bridge (1989: GG1, GG2; steel). No photograph of 1975 to 1995 showing a precast concrete column with a sodium lantern close enough to read was found. The concrete ones used (GG3 to GG5) are of 2008 to 2010. **Wikimedia Commons** (api.php search and category listings): reached, but the shared address answered 429 to most requests and the searches that returned gave no British lamp column of 1975 to 2000 (nothing used). **archive.org** (advancedsearch.php): reached once, 'street lighting column' returned books and reports, no period street photograph (nothing used).

### 2.3 Unreached

{chr(10).join('- ' + u['what'] + ': ' + u['result'] + '; used: ' + u['used'] for u in T['unreached'])}

WebSearch was used only for the leads of section 2.4 (9 October); no number was taken from a search summary.

### 2.4 Leads (WebSearch summaries of 9 October 2026: leads, never numbers)

{chr(10).join('- ' + l['text'] + ' (' + l['via'] + '; ' + l['effect'] + ')' for l in T['leads'])}

## 3. The Hook sheet and the column

The brief says the Hook sheet's foreground column is slender and dark with a small flat canopy, and that tools/art-recipes/lighting-column.py records that crop. The recipe's own notes say the crop is the RETIRED Codex sheet's (production/art/atlas-01/concepts/hook.png on a branch that is not in this checkout; "three traces of one lamp crop gave three answers"), that the approved pass 4 street panel "shows NO street lighting column anywhere in it", and that the column's shape is "governed by R07's 1989 photograph, 'plain bent-arm lighting'" (production/reference/photographs.md; a Hull photograph that is under photographer copyright and was not reached). This writer re-read the approved sheet at full size in four tiles: it shows the brick terrace, the wet street, parked cars, and no lighting column and no wall lamp (a small white fitting at the gable's corner and the dish above Mickey's fascia are not lamps). The retired in-house poster (688 x 1024) is an image model's drawing from a prompt that asked for a pub (retired-sheet-inheritance.md): its post-top lamp's pole is 3 to 4 px wide and its two box wall lanterns are about 20 x 40 px, so there is nothing to measure (hook-sheet-audit.md: under about four pixels is noise) and, being a pub's, nothing citable.

So: the sheet governs mood (wet, grey, low contrast, dark metalwork) and the night frame's pools, and decides nothing about the column's shape. The slot overlay `hook-sheet-slot-x8-east-target-on-sheet.jpg` lays variant A at its scene slot (x 8, east) on the sheet's reduced copy with the sheet's own lens (production/reference/hook-sheet-lens.md; the scene's cam_hook: x -3.0, z -1.6, eye 2.2, yaw 20.4, pitch -3.4, 46 degrees vertical): it checks scale and place, not a measurement. The lens puts Mickey's pilasters within 45 px of the sheet's on 1600, as the lens note says; the sheet draws the east footway visibly wider than the scene, so the column's foot lands at the shopfronts' base rather than at the kerb, and its top stands above the sheet's first-floor window heads although 5.0 m is under the scene's 6.3 m eaves: the sheet's terrace is drawn lower than the scene's. The sheet is a picture an image model made; the target does not follow it there.

## 4. How the photographs were measured

**Camera heights.** The panoramas record none. This target uses the heights the bollards' target measured and its reviewer re-measured, each at the object's own ground (production/cloud-week/targets/bollards/TARGET.md section 3): **BGE 1.02 +-0.07 m** (brick-course horizon method on the planter wall of the same block paving; the writer 0.96, the reviewer 1.03 to 1.04) and **US01 1.16 +-0.07 m above the footway** (the garden wall and gate pier; 1.23 above the bed). Every BGE and US01 length is therefore **+-7 % in absolute size**; proportions are exact to the pixel. If BGE's sleeve is the standard 114.3 mm tube, the camera was 0.95 m (this writer's own horizon fit gave 0.96) and every BGE length is 7 % smaller; the stated error covers it.

**Distance.** The column's horizontal distance gives the picture its scale. BGE: the sleeve's front foot at row 2524 of 4096 (-20.9 degrees) gives 1.02 / tan 20.9 = 2.665 m; its radius 0.062 puts the axis at 2.73 m, bearing 138.5 degrees; the base then appears at z = -23 mm in the elevation, as the geometry says. US01: the column's foot is hidden by a car; the gate pier beside it gives 8.4 m and the lowest visible sleeve point 9.2 m: 8.8 +-0.6 m, so only RATIOS are taken from US01 (its column is an 11 m class).

**Re-projection.** `lamp_lib.elevation` makes a flat, square-on picture of the vertical plane through the column's axis at a stated millimetres a pixel (1.2 mm for the BGE strips, 3 mm for US01); edges are found by the strongest luminance gradient in a window round the expected edge (`measure_photos.py`; raw rows are in `photo_measurements.json` and copied into target.json). The native resolution is 2 mm a pixel at 2.7 m and 7 mm at 8.8 m.

{table([
    ("BGE sleeve OD", "123.6 (rows 120 to 128, z 100 to 800)", "+-9", "124"),
    ("BGE sleeve's straight side ends", "z 978 (read on a 4 x gridded crop)", "+-10", "978"),
    ("BGE cone top, a thin ring line", "z 1035 to 1040", "+-10", "1038 (ring 6 tall)"),
    ("BGE shaft OD", "66 (z 1100, by eye), 67/69/69 (z 1700 to 1900), 61/61/61 (z 3800 to 4000)", "+-6", "68 at the cone, 60 at 4560 (the line's end inside the socket; 60.4 at its foot, z 4370)"),
    ("BGE pod, widest run", "417 (x -193 to +223)", "+-30", "420 (variant P)"),
    ("BGE pod's centre height", "4410 from the limbs' angles (53.8 and 48.5 degrees)", "+-300", "4375 (P)"),
    ("BGE paint, median sRGB", "sleeve 31/31/33 (p10 19, p90 44); lowest 250 mm 49/46/42; shaft 44/45/51 (sky-tinted)", "+-3", "31/31/34; splash 49/46/42"),
    ("US01 shaft top / stem / arm", "89.1 / 42.0 / 59.9", "+-8 / +-5 / +-6", "ratios 0.47 to 0.67; stem OD 42"),
    ("US01 sleeve / shaft", "232 / 113 at 8.8 m (by eye): 2.05", "+-0.2", "BGE's own 1.8 used"),
    ("US01 lit lantern, median sRGB (66,611 orange pixels)", "251/152/14 (p10 229/105/0, p90 255/208/77; the clipped core 252/251/180)", "+-8", "bowl (255, 137, 0); lamp (255, 176, 28)"),
], ("measurement", "reading", "error", "the target's value"))}

**The drawing laid on the photograph.** The overlay `bge-bethnal-green-column-target-on-photo.jpg` draws target.json's lower column (the sleeve, cone, ring and shaft, z 0 to 4280) over the four BGE strips at a scale fitted on ONE dimension only, the sleeve's width (123.6 measured, 124 in the target: scale s = {LAID.get('scale_s', 'n/a')}). The self-check re-measures the preview and tests it: the sleeve's two edges over {LAID.get('rows_sleeve', '?')} rows, mean absolute error {LAID.get('sleeve_edge_mean_abs_mm', '?')} mm (none over 8; the pixel is 1.2 mm); the shaft's width over {LAID.get('rows_shaft', '?')} rows, median absolute error {LAID.get('shaft_width_median_abs_mm', '?')} mm, upper quartile {LAID.get('shaft_width_p75_abs_mm', '?')} (the rows against the sky are within 2 mm; the rows against ivy and brick scatter); the cone and ring by the same method, with the ivy behind them confusing the edge finder (the picture shows the fit). Above z 4300 the photograph's column carries a post-top pod (variant P), not A's collar and bracket, so no outline is drawn there.

### 4.1 US01 laid on the picture in 3D (review fault 1)

The US01 elevation is the vertical plane through the column's axis, square to the line of sight, drawn flat. An arm that points out of that plane, toward the camera, shows extra rise in it, and the camera looks UP at the bracket (about 45 degrees). The street's own direction gives the arm's plan direction: its kerbs and parked cars vanish at bearing -57.8 (the reviewer's reading, taken as read: `photo_measurements.json` `us01_street_vp`), the column stands on the street's right-hand footway and its arm reaches over the carriageway, square to the kerb, so the arm points at bearing -57.8 - 90 = -147.8, **42.1 degrees out of the plane toward the camera** (the plane's left direction is -105.7). `lamp_us01.py` projects a 3D bracket (stem height, bend radius and arm length free, the rake free or fixed) onto the picture from the camera (centre projection, the same as made the picture) and fits the stem and arm points read off the preview; `self_check.py` part B runs it. Result: with the arm at -147.8 the free-rake fit gives **{FIT.get('street_free_rake_deg', 'n/a')} degrees** (median error {FIT.get('street_free_median_mm', 'n/a')} mm), a level arm fits to {FIT.get('street_rake0_median_mm', 'n/a')} mm and an arm forced to 40 degrees to {FIT.get('street_rake40_median_mm', 'n/a')} mm; with the arm in the picture's plane (-105.7, the first try's reading) the fit gives {FIT.get('plane_free_rake_deg', 'n/a')} degrees and a level arm fails ({FIT.get('plane_rake0_median_mm', 'n/a')} mm). So the 41.7 degrees of the first try is perspective and the true rake is about 0 (the review's table: a level line along the arm appears at 36 to 42 degrees for an arm turned 35 to 42 degrees toward the camera). The lantern's silhouette lies on the arm's line within a few degrees (the reviewer's reading: its midline stays 17 to 54 mm from the arm line over 1.1 m, drifting under 2 degrees), so the lantern is coaxial with the arm.

### 4.2 The photographs of 1989 and of 2008 to 2010 (try 2)

Read on 640 px copies by eye on a 5 x or 6 x grid (pixel coordinates read to +-1 px; no scale is known, so lengths are in widths of the column's own tube, and a width of a 60 mm tube or a 100 to 125 mm concrete top turns them into millimetres). The five crops are in section 13. Element by element (bracket, reach, lantern, shaft taper, base and door, root at the ground):

{table(el_rows, ("photograph", "bracket", "reach", "lantern", "shaft and taper", "base and door", "root at the ground"))}

What they settle: **the arm is near level with the lantern in line** (GG1, GG2, GG3: rises of 8 to 19 degrees in pictures taken looking up, which a level arm pointing partly toward the camera shows; true rake 0 to 10), **the elbow is one bend** (radius 1 to 3 tube diameters), **the steel column is stepped** (GG1, GG2: a dark sleeve at the foot and a step in the tube), **a concrete column's foot is a plain square planted into the paving** (GG5; GG3's foot is out of frame), **the shaft tapers in a straight line** (GG3, GG5: a foot 1.6 to 2 times the top, the target's 220 over 125 is 1.76). What they do not settle: the reach (shorter on the two steel columns), the lantern's length (longer than 550 on all three), the arm's form on every concrete column (curved on GG4 and GG5), and anything of 1990.

## 5. The target, part by part (variant C, the main build; variant A in section 5A)

### 5.1 Frame

Origin on the column's vertical axis at the footway surface; **+y points at the carriageway** (the lantern side), x runs along the street, z up. For the west side's columns the whole piece is turned 180 degrees about z so that +y still points at the road. The column stands plumb (the footway falls 1 in 40: 5 mm across the 210 mm concrete shaft, 3 across A's sleeve). The pivot is the axis at z = 0; the shaft runs 150 mm below it (hidden) so that the footway's fall never shows a gap. One mesh for the column, one for the lantern (the arc tube, jacket and bowl as emissive material slots).

### 5.2 The concrete shaft, cap, door and plate (variant C)

`geometry.C.shaft.points_z_side_chamfer` (z, side across the faces, arris chamfer), in mm: **(-150, 220, 15), (0, 220, 15), (4620, 125, 15)**; the section is square to the street (faces at +-x and +-y); the taper is linear in z (the side narrows 20.6 mm a metre, both pairs of faces alike); the arrises are chamfered 15 throughout (a 15 mm leg on each face, the same at every height); the top face (z 4620) is flat with a **5 mm chamfer** all round its edge. The side is 213.8 at z 300, 172.7 at z 2300 and 131.6 at z 4300 (+-6). Kind: Judgement. The foot is the research's "20 to 25 cm at the foot" (Read: 220), the top 125 is the review's; GG3 and GG5 agree with a foot 1.6 to 2 times the top (1.76) and a straight taper; GG3's top reads 100 to 125 by its own lantern's proportions (unsettled).

- **Root.** The shaft is planted: the lowest 150 mm are hidden below the footway; **no base plate, no collar, no bolts**: the paving is cut round it with a 10 to 15 mm joint of dark grit mortar (GG5: a plain square foot planted into the pavement; the BGE sleeve on block paving shows the same joint). Kind: Photo (GG5, qualitative) + Judgement (the figures).
- **Cap and stem.** A cast-steel cap, **90 OD and 30 tall (z 4620 to 4650)**, black, seated on the top face; the **48 OD steel stem** rises from the top face's centre through the cap (its lowest 60 mm, z 4560 up, are cast into the concrete). Kind: Judgement (review F2).
- **Door.** On the -y face (away from the carriageway, toward the building line): a **recess 120 wide x 330 tall x 14 deep at z 450 to 780**, 6 mm radii in its corners; a **steel plate 132 x 342 x 3 (z 444 to 786), 3 proud**, corners rounded 10, held by **two round-headed hex-socket screws 10 across at 25 from its ends (z 469 and 761)**, no hinge showing, no lock, **blank: no lettering, no maker's mark, no cast name** (the leads say real doors of the kind carried a maker's mark: ours is blank by rule). Kind: Judgement (review F2; the research: "a door plate about 50 cm up"; GG3 shows a small pale plate low on the shaft, unreadable).
- **Number plate** on the +y face at z 2160 (BGE's reference plate was at z 2115 to 2200): a flat aluminium plate **90 x 45 x 1.2**, 1.4 proud, two domed rivets 5 across at 8 from each end, white (214, 212, 205) with black (30, 30, 32) upright sans letters 24 high reading **LC n** (n = 1 to 4). Generic: no authority's name, no crest, no maker.
- No flutes, no ornament, no finial, no paint on the concrete.

### 5.3 The bracket (both variants)

A plain bent arm of one steel tube (**OD 48 on C**, 42 on A) in the y-z plane: it rises **vertically from inside the column's top (z 4560) to z 4800.8**, makes **ONE bend of 90 degrees on a centreline radius of 130** (three tube diameters) from (0, 4800.8) to (130, 4930.8), and runs **straight and LEVEL (rake 0) 300 mm to its end at (430, 4930.8)** inside the lantern's rear boss: **a reach of 430 from the axis to the lantern's rear spigot** (Read: the research's 1 ft 4 in to 1 ft 6 in, 406 to 457). The centreline is stored at 40 mm steps on the stem, 7.5 degrees on the bend and about 33 mm on the arm (`geometry.C.bracket.centreline_yz`, `geometry.A.bracket.centreline_yz`; identical above z 4560).

Where the numbers come from. **The rake:** US01 (an 11 m column) shows 41.7 degrees in the picture, but the arm points 42 degrees toward the camera; read in 3D (section 4.1) the true rake is 0 to 7, the lantern lies on the arm's line, and the 1989 photographs GG1 and GG2 show arms rising 8 to 10 degrees or less in the picture with the lantern in line, GG3 a mitred elbow and an arm that a level arm pointing partly toward the camera explains; a lead says 5 m brackets had "a vertical and a horizontal section". So **rake 0 (+-5)**, the arm angular. **The bend's radius:** 130 is the review's (three diameters of 42); the photographs read 1 diameter (GG3 about 55), 2 (GG2) and 3 (GG1): inside their span, the check +-75. **The reach:** 430 is the research's (Read) and the review's; it is the distance to the spigot, the lantern's rear end, so the lantern's centre is 705 out. The stem height 4800.8 and the arm height 4930.8 (inside the canopy's lip band 4925 to 4937, so that the boss is cast on the canopy's rear tip) are Judgement. **Not settled:** the two curved-arm concrete photographs (GG4, GG5) show a gooseneck, not an angular arm (PW10): the review's form is built.

### 5.4 The lantern (both variants)

**Envelope 550 x 300 x 200** (the scene's box: Read), top at z 5000 (the mounting height), bottom 4800, **rear end y 430, centre (0, 705, 4900), front end y 980**, **long side along y**, level. US01 from below shows the arm entering the lantern's rear end and the lantern lying along the arm; so do the 1989 stations and Birchington. All coordinates below are in the column's frame; every y is the first try's plus 205 (review fault 3).

- **Canopy** (painted aluminium, shell 2.5): plan half-widths at y 430 / 435 / 450 / 475 / 505 / 545 / 605 / 655 / 725 / 805 / 875 / 930 / 965 / 980 = 0 / 30 / 58 / 86 / 108 / 128 / 144 / 150 / 150 / 146 / 134 / 108 / 62 / 0 (a boat: narrow at the rear where the arm enters, full and round at the front); a down-turned lip 12 tall from the rim z 4925 to z 4937; above it a half-ellipse dome whose crown follows z = 4937, 4962, 4990, 5000, 4998, 4985, 4963, 4945, 4937 at y = 430, 465, 525, 605, 705, 805, 885, 940, 980 (the dome is 61 high at the centre y 705 and **63 at its highest, y 605**; the highest part, y 605 to 705, is the gear tray: **there is no separate gear box**). Underside white (226, 224, 216) reflector, with a lamp-holder 60 x 45 x 40 at the rear (x +-30, y 505 to 550, z 4852 to 4892).
- **Bowl** (clear acrylic, yellowed, shell 3, a 6 x 6 bead on its rim): rim at z 4925 following the canopy's plan 8 inside it (y 438 to 972); a flat refractor base at **z 4800, 400 long (y 505 to 905) and 164 wide**, plan half-widths 0 / 22 / 52 / 70 / 80 / 82 / 80 / 70 / 52 / 22 / 0 at y 505 / 508 / 525 / 555 / 605 / 705 / 805 / 855 / 885 / 902 / 905; the sides bulge outward from base to rim by the section at the centre (half-width, z): (82, 4800), (90, 4806), (100, 4815), (118, 4842), (130, 4872), (138, 4900), (142, 4925); the ends follow the long section's rear curve (y, z): (438, 4925), (445, 4890), (467, 4850), (490, 4818), (505, 4800), the front its mirror about y = 705. `bowl.loft` gives the one formula that joins them. Fine prismatic grooves 2 mm apart across the base's underside. Hinged at the rear (two knuckles 22 x 22 x 14 at x +-60, y 467, on the rim) and closed by **two spring catches** 30 x 14 x 7 proud on the long sides at y 855, x +-136, on the rim line (Judgement).
- **Lamp**: one glass jacket **54 across and 310 long** lying along y, centre (0, 705, 4872), a 35 W low-pressure sodium lamp (Judgement: a search lead lists 311 x 52 and 310 x 54) with its lamp-holder at the rear end; **inside it the arc tube (review point 3): a glowing U, two legs of 16 OD with centres at x +-11, z 4872, running y 555 to 845 (straight to 826, then a half-torus of centreline radius 11 at the front), the full-strength emissive part; the jacket glass glows at 0.3 of it.** The tube, the jacket and the bowl are the only emissive parts.
- **Rear boss**: a cast sleeve **OD 60, 55 long, HORIZONTAL**, axis along +y from (0, 430, 4930.8) forward to y 485, coaxial with the lantern's long axis on its centreline; a visible cast boss on the canopy's rear tip (its lower edge hangs 24 below the rim at its start; its top (4960.8) stands 24 above the canopy's rear crown (4937) and nothing pokes through the dome: the dome is 4976 over the boss's front end); two M8 round-headed grub screws 10 across, 3 proud, at 90 and 270 degrees about its axis.
- No photocell, no ornament, no ladder bar, no finial (the recipe's rule, kept).

### 5.5 Materials and paint

{table([(k, json.dumps(v.get('srgb') or v.get('srgb_unlit') or v.get('srgb_white') or v.get('emissive_srgb_lit')), v.get('name', ''), v.get('roughness_words', ''), v.get('roughness', v.get('roughness_new', '')), v.get('metal', ''), v.get('kind', '')) for k, v in T['materials'].items()], ("part", "sRGB", "plain name", "roughness in words", "roughness 0-1", "metal", "kind"))}

Concrete (146, 143, 136), roughness 0.9, no paint (variant C). Painted steel is not metal for shading (metal 0: a painted surface); roughness 0.42 is the recipe's and BGE shows gloss worn to semi-gloss (the upper shaft rougher by 0.15). The bowl's transmission 0.85, IOR 1.49 (acrylic). The jacket and the arc tube are (255, 137, 0) lit (review point 5): the yellow core of the photograph is the camera's clipping, left to the grade. The only high-chroma surfaces are the arc tube, the jacket and the bowl: the paint, canopy, plate and primer are within 16 per channel of grey (the accent budget, art-direction R-B4).

### 5.6 Wear

State: a tired column of twenty or thirty years in a port town's wet air. Placed per column by its seed; positions are on the **carriageway face (+y)** unless said.

{table([(w['id'], w['where'], w.get('kind', '')) for w in T['wear']['features']], ("feature (variant C, the main build)", "where, how big, colour", "kind"))}

Not present: lettering graffiti, posters of this target's own (the posters target places bills and stickers on these shafts), reflective or coloured bands, a maker's plate or cast mark.

### 5.7 The lit lamp: numbers that agree with the night note

The lamp is a 35 W low-pressure sodium lamp, 4,550 lm (Read: the night note, a maker's datasheet by search summary). The game's light for each column, at **(0, 705, 4850)** in the column's frame (the scene's rule: a point light 0.05 m below the centre of the emissive piece), is the night note's:

{table([
    ("pool spot (shadows on, straight down)", "500 lm, inner 22, outer 46 degrees: 261 cd, 11.4 lx straight down from 4.78 m", "350 lm, inner 15, outer 55: 130.6 cd"),
    ("skirt spot (no shadows, straight down, source radius 5 to 10 cm)", "none", "800 lm, inner 45, outer 80: 154.1 cd"),
    ("glow (all round, no shadows)", "40 lm (3.2 cd)", "40 lm"),
    ("sum straight down", "11.4 lx", "12.46 lx (the note's 'about 12.5')"),
    ("total lumens", "540", "1,190, 26 % of the lamp's 4,550 (the note cut the pool on purpose to cure the clipped red; it adds the skirt for the gaps)"),
    ("range", "18 m", "18 m"),
    ("colour (linear)", "(1.0, 0.25, 0.0)", "(1.0, 0.25, 0.0); the note's try (1.0, 0.40, 0.03) = sRGB (255, 170, 48)"),
], ("light", "current game (8 October)", "the night note's proposal (section 4 steps 4 and 5)"))}

The cone arithmetic (cd = lumens / (2 pi (1 - cos outer half-angle))) is recomputed in the self-check and reproduces the note's 261 cd, 11.4 lx and 12.5 lx. These are the note's intent, to be tried and measured in the game's own camera (its section 5). Since the lantern now stands 205 further out, **the pool moves 0.2 m toward the road**; the night note's pool and skirt numbers are unchanged.

**Emissive strength in units (review point 4).** The jacket about **27,500 cd/m2** (4,550 lm over its 0.0526 m2 surface: pi x 0.054 x 0.310), the bowl about **5,500 cd/m2** (80 % of the flux, 3,640 lm, through about 0.21 m2 of bowl, Lambertian), the arc tube the jacket over 0.3, about **91,700 cd/m2** (stated, not measured). Or, until the night audit puts the glow in units, all three follow `VignetteShot.cpp`'s `kLampEmissiveUnitless` = 1.0 times the lantern colour in linear (1, 0.25, 0): the builder says which.

**The colour, and the scene file's mistake.** The scene file's lantern is linear (1.0, 0.7055, 0.0), gamma (255, 219, 0), xy (0.5467, 0.4526), "589 nm". That xy is the colour of about **585 nm** (the printed CIE value at 585 nm is (0.5448, 0.4544); a multi-lobe fit of the colour matching functions, recalled from memory and checked against that value to 0.002, gives (0.5436, 0.4562) at 585 and **(0.5667, 0.4332) at 589**, (0.5684, 0.4315) for the sodium D lines). And its normalisation divided red by the peak but left green and blue undivided: clipped and divided by 2.3766 the scene's own xy gives (1.0, 0.2969, 0.0), not (1.0, 0.7055, 0.0). At 589 nm the same matrix gives (2.731, 0.600, -0.130), clipped and divided by its peak **(1.0, 0.2195, 0.0)** linear = **(255, 129, 0)**: the evening note's (255, 140, 0) and the night note's (1.0, 0.25, 0.0) are within 0.04 and 11. The night note says the game's lamp already is (1, 0.25, 0); the scene file is stale and wrong, and correcting it is a ruling (asked first).

**Glow surfaces.** Arc tube, jacket and bowl: emissive (255, 137, 0) = the night note's lamp gamma-encoded (the lit US01 lantern's median is 251/152/14: within 15); the yellow core of that photograph is over-exposure and is left to the grade. The canopy, the arm and the column stay unlit paint or concrete, lit only by the pools. Warm-up (optional): a freshly lit lamp glows dim red-pink for a few minutes before turning orange (evening note section 1). Unlit by day: the bowl clear-yellowed (190, 182, 160) with the jacket (200, 196, 180), the grey tube (170, 166, 158) and the white reflector seen through it.

### 5.8 Placement

{table([(c['id'], c['x_m'], c['side'], c['scene_z_m'], c['corrected_z_m'], c['plate_text'], c['wear_seed'], 'yes' if c['chipped_arris'] else '') for c in T['placement']['columns']], ("column", "x (m)", "side", "scene z (m)", "z with the corrected 170 kerb (m)", "plate", "wear seed", "chipped arris (C) / dent (A)"))}

The code's loop gives four columns, **20 m apart on each side, 10 m apart along the street, alternating** (SCENE-SLOTS.md's "every 20 m" is the spacing on one side; the posters target's SF4 'x 8, 28, 48' misreads it: the street has columns at 8, 18, 28 and 38 and none at 48). The axis stands 600 mm behind the kerb's BACK face: the scene's kerb top is 125 wide so z = 3.125 + 0.6 = 3.725; the corrected granite kerb top is 170 so the same rule gives 3.77. The rule governs, within a 40 mm tolerance. The arm points at the carriageway, square to the kerb; the door faces the building line; the plate faces the road. With the axis 770 behind the kerb face (the corrected kerb) **the lantern's centre stands 65 mm behind the kerb face (770 - 705) and its front end 210 mm over the channel (980 - 770)**, which is the usual place for the pool: the pool lands on the flags and the channel, 0.2 m nearer the road than the first try's.

### 5.9 Edges, bevels, size

Every hard edge is bevelled (mid-poly; the asset plan's method): {", ".join(f"{b['edge']} {b['radius']}" for b in T['bevels'])} (radii in mm). Triangle budget {T['triangle_budget']['lod0'][0]} to {T['triangle_budget']['lod0'][1]} per column with its lantern at LOD0 (Judgement; four columns are a small share of a frame).

## 5A. Variant A, the painted-steel stepped column (the alternative, built only if ruled in)

The bracket, lantern, light, plate and places are the same (sections 5.3 to 5.8); only the column differs.

### 5A.1 The lower column: sleeve, cone, shaft, socket

Profile (radius, z) in mm, revolved about the axis (`geometry.A.lower.outer_rz`, authoritative):

{table([(f"({p[0]}, {p[1]})", d) for p, d in zip(prof, ("axis at the hidden foot", "hidden skirt: sleeve radius", "sleeve top: the straight side ends (Photo, BGE 978)", "cone top, shaft radius 34 (OD 68)", "the weld ring: 1.5 proud ...", "... 6 tall (z 1038 to 1044)", "back to the shaft", f"the shaft's straight taper, the same line as before (34 to 30 at z 4560), here at the socket's foot (z {ZC0:.0f})", "socket radius 32 (OD 64)", "the socket's straight side ends 3 below its top", "the 3 chamfer into the stem", "the axis"))], ("(r, z)", "what"))}

- **Sleeve** 124 across (Photo, +-9; the scene's 114 is at its lower error edge and 114.3 is a standard tube: the tolerance covers it), 978 high above the footway and 150 below it. A 1 mm groove round it at z 978 where the cone cap is welded on (Photo: a dark line under the cone). GG1 and GG2 (1989) show the same stepped form: a dark sleeve at the foot.
- **Cone** 60 mm tall, **25 degrees off the vertical** (atan(28 / 60); review point 7), from OD 124 to OD 68; **ring** 1.5 proud and 6 tall at its top (Photo: a thin ring line there).
- **Shaft** a plain round steel tube tapering in one straight line from OD 68 at z 1044 to OD 60 at z 4560 (Photo: 66 to 69 at z 1.1 to 1.9 m, 61 at z 3.8 to 4.0 m; the line is drawn to the socket's foot, 60.4 at z {ZC0:.0f}). A longitudinal weld line 1.5 wide and 0.5 proud on the -y face. No flutes, no ornament, no finial.
- **Socket** (review point 1): the bracket's socket sleeve, **z {ZC0:.0f} to {ZC1:.0f} (250 long), OD 64**, standing {G['socket']['proud_of_shaft_at_foot_mm']} proud of the shaft at its foot (the review says 2 for a 62 shaft; with the shaft left as it is it is that), no step a 7 mm pixel could see on US01, its **top edge chamfered 3** into the stem, a 1 mm seam groove round its foot, and **two M8 socket set screws on the -y face one above the other at z {SCREW_Z[0]:.0f} and {SCREW_Z[1]:.0f}**, round heads 10 across and 3 proud. Kind: Photo qualitative (US01) + Judgement.
- **Root.** The sleeve runs straight into the footway: the paving is cut round it with a 10 to 15 mm joint of dark grit mortar; no base plate, no collar, no bolts show (Photo, BGE: block paving cut round the sleeve, no plate; GG1: the sleeve stands in the paving).
- **Door** (Judgement; the research says "a door plate about 50 cm up", US01's sleeve shows a rectangular door outline whose top edge is at about 86 % of the sleeve's height with **rounded top corners**, and a search lead, never a number, gives a 500 x 100 door opening 400 above the ground on a modern 5 m stepped steel column; the sleeve's 978 holds a door from 400 to 900): on the -y face, a curved plate rolled to the sleeve, **100 mm of arc (92 degrees) by 500 tall, z 400 to 900, 1.5 proud, all four corners rounded to radius 15 (review point 2)**, a 2.5 wide and 2 deep joint groove (black) all round it with the same corner radius, two round-headed hex-socket captive screws 12 across and 2 proud on its centre line at z 425 and 875, no hinge showing, no lock, **no lettering and no plate on it**.
- **Number plate** on the +y face of the shaft at z 2160 (BGE has a larger flat reference plate at z 2115 to 2200, 125 x 85, white with black letters: a sign's, not copied): a curved aluminium plate **90 x 45 x 1.2** wrapped on the shaft (65 across seen square on), 1.4 proud, two domed rivets 5 across at 8 from each end, white (214, 212, 205) with black (30, 30, 32) upright sans letters 24 high reading **LC n**. Generic: no authority's name, no crest, no maker.

### 5A.2 Variant A's wear

{table([(w['id'], w['where'], w.get('kind', '')) for w in T['wear']['features_A']], ("feature (variant A)", "where, how big, colour", "kind"))}

## 6. Variants

{table([
    ("C", "precast concrete column, steel bracket, the lantern (section 5)", "MAIN: 4 of 4 places", "the numbers of sections 5.2 to 5.9: Judgement and the research's, checked against the photographs of 2008 to 2010 (taper, plain planted foot, angular elbow agree; two curved arms do not)"),
    ("A", "painted-steel stepped column (section 5A)", "alternative, built only if ruled in", "all numbers of section 5A: Photo (BGE, US01 ratios, GG1, GG2) and Judgement; if A is built, review point 9: the shaft's top 64 to 68 at z 4560 (a nearly parallel taper from 68) and the socket 4 to 6 larger"),
    ("P", "post-top dish on the same lower column", "not placed (the scene's lamps are bracket lamps)", "what BGE shows: the lower column to z 4300 and a dish 420 across (Photo, +-30) of Judgement height 150 centred at 4375; shell dark, underside pale"),
    ("W1", "a wall bracket for the same lantern", "optional, not placed; if wanted, a plain gable end, never a shopfront", "Judgement only: a wall plate 150 x 220 x 8 with four bolts (domed nuts 24 across), a 42 arm LEVEL (review point 8) from z 4350 to the lantern's rear boss at y 430 from the wall, coaxial with the lantern, a 25 strut from z 4130 to 140 along the arm; the lantern 581 lower than on the column (top at 4419). The two wall lanterns reached are a one-off college lantern (Cambridge) and a 2019 estate bulkhead (US02, 235 x 210): neither is a street fitting"),
], ("id", "name", "build", "difference and basis"))}

How many the street needs: one column type per scheme (a street's lamps were fitted together), so the four places take C, or all four take A if ruled; the lantern is one pattern in both. The variation between the four is the wear (their seeds, the chipped arris on LC 2), not the form. Not written out: a curved gooseneck arm on the concrete column (GG4, GG5; PW10), because no number could be read off the two photographs.

## 7. The photographs-win disagreements

{table([(w['id'], w['what'], w['scene'], w['photograph'], w['chose'], w['kind']) for w in T['photographs_win']], ("id", "what", "the stand-in or book says", "the photograph or the record says", "chosen", "kind"))}

## 8. The checks for unit 3.8

`target.json` `checks` lists {len(T['checks'])}: each a name, what to measure, the expected value and the tolerance (checks for variant C say "C", for A "A", the lantern, bracket and light "A, C"). Those that matter from the street are the lantern's box (550 x 300 x 200 +-8, centre (0, 705, 4900) +-12, long axis along the arm +-3 degrees, top at 5000 +-10, arm, boss and lantern coaxial within 2 degrees), the bracket (rake 0 +-5, bend radius 130 +-75, end at (430, 4930.8) +-12, the boss horizontal and its top 24 above the rear crown without piercing the dome), the concrete shaft (213.8 / 172.7 / 131.6 across at z 300 / 2300 / 4300 +-6, chamfer 15 +-3, section square to the street, the door recess and plate, the cap and the stem's entry, albedo (146, 143, 136) +-12, no paint), A's sleeve (124 +-9, 978 +-15 high), shaft width at 1200, 2500 and 3900 ({SW1} / {SW2} / {SW3} +-6), socket (64 from z 4370 to 4620 +-4) and door with its 15 mm corners, the plate, the colours (A's paint (31, 31, 34) +-12, the glow (255, 137, 0) +-12 on the tube, jacket and bowl), no maker's mark and no lettering but the plate's, the light's place (0, 705, 4850) and numbers, and the four places. The profile and silhouette checks are two-way nearest distances (every point of the built outline to the target's outline and back, at most 4 to 6 mm), as the pillar box's.

{table(chk_rows, ("name", "applies to", "measure", "expected", "tolerance", "kind"))}

## 9. What the self-check does

`self_check.py` (A to E, T and W): **A** every printed number comes back from its file (the scene, the pieces file, the code's loop, the earlier research, the evening and night notes, DECISIONS.md, the kerbs target) and every derived number recomputes (the colour matching functions' fit, the 589 nm colour, the cone arithmetic); **B** the raw photograph rows give the printed numbers; the numbers are re-measured from the reduced previews; the lower column of A is laid on the BGE strips at a scale fitted on the sleeve alone and its edges fall on the photograph's within the stated error; **US01 is laid on its picture in 3D** with the arm at the street's bearing and the free-rake fit must give 0 +-7 degrees; **C** the drawing runs on target.json alone (22 views) and its polygons give the target's numbers (A's and C's shafts, the bracket, the lantern 430 to 980, the arc tube, the door's rounded corners); **D** the bracket's geometry recomputes, nothing floats (column, arm, boss and lantern are one connected shape), the lamp lies inside the bowl, the light inside the bowl, the wear zones lie on the right faces; **E** no maker, brand, crown or authority's name on any part, only the plate carries letters, none of the content rule's words, the previews (the 1989 to 2010 crops too) obey the brief, this file carries its summary line, the plain statement, every preview's credit and every Geograph photograph's page, author, date and licence, and its Try 2 section; **T** at least one row for each of the three faults and nine narrow points (the rake and the coaxial lantern; C's shaft, cap, door, checks and wear; the reach and every lantern station +205; the socket, the door corners, the arc tube, the units, the jacket's colour, the dome check, the cone's 25 degrees, W1 level, the note on the shaft's top); **W** eighteen deliberately wrong copies of target.json (a 114 sleeve, an untapered shaft, a 40 degree rake into a level lantern, a narrower lantern, the lamp above the bowl, the scene file's yellow, a maker's name on the plate, an arm that misses the boss, columns at 8, 28 and 48, a light above the lantern, steel as the main build, a reach of 225, a lantern 500 out, a 114 concrete top, a short door recess, a 67 socket, a yellow jacket, square door corners) must each be refused by at least one test.

## 10. What the target could not settle

{chr(10).join('- ' + c for c in T['could_not_settle'])}

## 11. To read once the network opens

{chr(10).join('- ' + c for c in T['to_read_when_the_network_opens'])}

## 12. Handover

{chr(10).join(f"- **{k.replace('_', ' ')}**: {v}" for k, v in T['handover'].items())}

## 13. Previews and credits

Poly Haven (BGE and US01): CC0 1.0, Andreas Mischok, taken 2019-08-18; Geograph (GG1 to GG5): CC BY-SA 2.0, each page's author, taken date and licence read on 11 October 2026 (table below); all used for measuring only, never placed in the game, traced into a texture or fed to an image model. Each crop is of the object only: the signs on BGE's shaft that carry text, a telephone number or a hand-painted picture are masked flat grey, a parked car is cropped out of US01's base, a station's name sign is masked grey in GG2's crop, and nothing else is in frame (no people, no shop names, nothing the content rule bars). The Geograph crops are enlarged 2 x from the 640 px originals (GG3 is whole at 640 px) and credited here as the licence asks: photograph by the named author, CC BY-SA 2.0, changed (cropped and enlarged). The drawings are this target's.

{table([
    ("bge-bethnal-green-column-strips.jpg", "BGE, four strips of the rectified column, z 0 to 4800, 1.2 mm a pixel, signs masked grey", "the lower column's measurements (section 4)"),
    ("bge-bethnal-green-column-target-on-photo.jpg", "the same with target.json's lower column (variant A) drawn over it (red lines), scale fitted on the sleeve only; no outline above z 4280", "the drawing check"),
    ("bge-bethnal-green-column-pod.jpg", "BGE, the post-top dish seen from below, rectified, 1.5 mm a pixel", "the pod's width (variant P)"),
    ("us01-bethnal-green-bent-arm-elevation.jpg", "US01, the shaft's top, stem, bent arm and lantern, rectified at 8.8 m, 3 mm a pixel", "the bracket's form and ratios; laid on in 3D (section 4.1)"),
    ("us01-bethnal-green-lit-lantern-from-below.jpg", "US01, the lit lantern seen from below, 5 degrees wide", "the glow's colour; the arm entering the rear end"),
    ("us01-bethnal-green-sleeve-and-shoulder.jpg", "US01, the sleeve, shoulder and shaft's foot, rectified, 2 mm a pixel", "the stepped form; the door outline"),
    ("us01-bethnal-green-bent-arm-3d-fit-on-photo.jpg", "the US01 elevation with the 3D fits laid on it: the observed stem and arm points (green rings), the free fit with the arm at the street's bearing -147.8 and a LEVEL arm (red: it lies on the arm), the same forced to 40 degrees (blue: it misses), and the in-plane free fit (yellow, hidden under the red)", "the drawing check of fault 1 (section 4.1)"),
    ("hook-sheet-slot-x8-east-target-on-sheet.jpg", "variant C (the main build) at its scene slot (x 8, east) laid on the Hook sheet's reduced copy with the sheet's own lens, re-made in try 2 (the arm level, the lantern 205 further out); a placement test, not a measurement", "section 3"),
] + [(p["file"], p["id"] + ", " + p["title"] + " by " + p["author"] + ", " + p["licence"] + ", taken " + p["taken"] + ", " + p["page"] + ": " + p["what_it_shows"], "section 4.2: the bracket, the reach, the lantern, the taper, the base and the root") for p in PER], ("file (production/previews/cloud-week/refs/lamp-posts/)", "what it shows", "used for"))}

## 14. The numbers that are not printed in the repository

{table(num_rows, ("id", "value", "unit", "kind", "source (first 230 characters)"))}
"""
open(os.path.join(HERE, "TARGET.md"), "w", encoding="utf-8").write(md)
print("wrote TARGET.md", len(md), "bytes")
