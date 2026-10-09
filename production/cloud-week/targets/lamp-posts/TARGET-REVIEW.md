FAIL

# Lamp posts: the target's review (cloud week 42, 9 October 2026)

**Three faults and nine narrow points.** Worst first:

1. The bracket's 40-degree rake comes from reading perspective as rake. US01's arm points about 40 degrees toward the camera, so its true rake is about 0 to 7 degrees. The photograph also shows the lantern lying in line with its arm, so a 40-degree arm entering a level lantern is contradicted.
2. Making steel the main model and concrete the unbuilt variant is backwards. The choice rests on 2019 London photographs that the brief does not accept as period evidence.
3. The bracket reaches only 225 mm to the lantern. The target's own Read source says 406 to 457 mm.

The lower column (sleeve, cone, taper), the paint and wear, the four places, the lit colour and the light block are right, and I re-measured or recomputed them.

Reviewer: a fresh reviewer who neither wrote nor will build this target. I read REVIEW-BRIEF.md, BRIEF.md, canon.md and RULINGS.md (1 October night ruling, 8 October photographs-win ruling, 21 September Hook sheet ruling), the whole of TARGET.md and target.json, the scene file, StreetVignette.cs Columns(), the night note, the earlier research, the recipe's notes, R07 in photographs.md and the approved Hook sheet at full size. I worked on a scratch copy of the target folder. Nothing in the target was edited, and nothing was committed.

## What was re-run, and what was reached

- **self_check.py**, run on a scratch copy (python -I, with TMPDIR in the scratchpad): `SELF-CHECK PASS: 231 of 231 tests pass (A 75/75, B 31/31, C 35/35, D 26/26, E 54/54, W 10/10)`. Apart from the result block, target.json was byte-identical afterwards. **target_drawing.py** ran on target.json alone and wrote 16 views and the polygons file. I looked at the side elevation and the bracket detail: the drawing is what the text says.
- **Poly Haven, reached 9 October 2026.** I read api.polyhaven.com/info and /files for bethnal_green_entrance and urban_street_01, and downloaded both 8192 x 4096 tone-mapped JPGs (md5 83de5627… and 42eba208…, as the API lists).
  - Author: Andreas Mischok.
  - Taken: 2019-08-18 at 07:01 and 07:09 UTC (date_taken 1566111660 and 1566112140).
  - Both are in Bethnal Green (51.527 N and 51.528 N, 0.054 W).
  - Licence page (polyhaven.com/license): "Our assets are all licensed as CC0".
- **Refused by the proxy (CONNECT 403):** commons.wikimedia.org, www.geograph.org.uk, www.flickr.com and archive.org. I tested each on 9 October. **Where that limits this review:**
  - No dated photograph of a 1990 British column of either material could be opened, so fault 2 is a judgement from the project's own research and from memory.
  - R07 (Hull, 1989, "plain bent-arm lighting") could not be seen.
  - The rake and reach of a 5 m bracket of the period cannot be checked against a period photograph. Fault 1's correction rests on the geometry of one 2019 photograph of an 11 m column. That is enough to refute the 40 degrees, but not to fix the period value better than "near horizontal".
- **My measurements on the full-resolution panoramas** use each object's own camera height: BGE 1.02 m at the column's paving; US01 1.16 m above the footway (the bollards' calibration, as the target uses). I found BGE's foot at row 2527 (the target says 2524), which puts the axis 2.71 m away (the target says 2.73). The pictures are in the session's scratchpad only, not in git.

| quantity | target | my reading | verdict |
|---|---|---|---|
| BGE sleeve OD | 124 (123.6 measured) | 122.5 to 123.0 at z 100 to 400, edges against the paving (0.5 mm elevation, strongest gradient, my own unconstrained finder) | agrees (+-9) |
| BGE sleeve's straight side ends | 978 | about 975, with a dark joint line there | agrees |
| BGE cone top, with its ring | 1038 | about 1035; a straight cone (not convex) about 60 tall, from about 120 to about 70 across | agrees |
| BGE shaft OD | 68 at 1044, 60 at 4560 | 67.0 at z 1700 (against brick); 60.5 at z 3800 to 4000 (against the sky) | agrees: the taper is real, about 3 mm a metre |
| US01 shaft top and stem | 89.1 and 42.0 (gradient edges) | 72 to 76 and 30 to 36 (half-level edges, 2 mm elevation; the native pixel there is about 10 mm) | absolute sizes are blur-limited; the ratio (about 0.45) agrees, and the target uses only ratios from US01 |
| US01 arm's apparent slope | 41.7 | 41.6 (centreline fit, x -1100 to -350, 3 mm elevation) | agrees as an apparent slope, but see fault 1 |
| scene lantern xy (0.5467, 0.4526) | "about 585 nm, not 589" | the CIE 1931 table gives (0.5448, 0.4547) at 585 nm and (0.5752, 0.4242) at 590 nm, so the scene's point is 585.3 nm; 589 nm interpolates to (0.569, 0.430) | the writer's finding holds |
| scene lantern's linear triple | "green left undivided" | through the sRGB D65 matrix, xy gives (2.376, 0.706, -0.135); clipped and divided by the peak, that is (1, 0.297, 0), not the file's (1, 0.7055, 0) | the writer's finding holds |
| 589 nm, gamma-encoded | (255, 129, 0) | (255, 128, 0) | agrees |
| cone arithmetic of the night note | 130.6 / 154.1 cd, 12.46 lx | the same | agrees |

## Faults, worst first

### F1. The bracket's rake and the lantern's junction contradict US01 once its camera is accounted for

**Photograph:** US01, the column at bearing -15.7 degrees, the bracket and lantern at elevation 44 to 50 degrees. My elevation used the target's own frame: lamp_lib.elevation(img, -15.7, 8.8, 1.16, -2300, 300, 9300, 12300, 3).

**What the target says.** The arm is raked 40 degrees (+-6) and enters a LEVEL lantern through a boss raked 40 degrees that pokes 17 to 24 mm above the dome. TARGET.md 5.3 reasons that "the lantern seen from below is nearly side-on, so the arm points within about 30 degrees of the picture's plane and the true rake is 36 to 44".

**What the photograph shows.**

1. **The lantern lies on the arm's line.** I extended the fitted arm line (41.6 degrees) through the lantern. The midline of the lantern's silhouette stays 17 to 54 mm from that line over its whole 1.1 m apparent length, and drifts less than 2 degrees from it. The silhouette's principal axis is at 45.6 degrees, and the line from the boss to the silhouette's centroid at 37.8 degrees.
   - The arm and the lantern's long axis lie in one vertical plane: the target's own PW3, the lantern lies along its arm.
   - Two lines in one plane that project onto one line are one line in 3D. So **the lantern is coaxial with the arm, to within a few degrees.**
   - A level lantern on a 40-degree arm would show a 40-degree kink at the boss. There is none.
2. **The 41.6 degrees is mostly perspective.** The camera looks UP at the bracket (about 45 degrees above the horizon, about 9 m above the camera at 8.8 m). Any part of the arm that points toward the camera therefore shows as extra rise in the picture.
   - In a view down the street (yaw -40, pitch -15, 90 degrees wide), the kerbs and the parked cars of the street the column stands on vanish at bearing -57.8 degrees, pitch -0.3.
   - The column stands on that street's right-hand footway, and its arm reaches over that street.
   - Square to the kerb, the arm points at bearing -147.8 degrees. That is **42 degrees out of the picture's plane, toward the camera**.
   - I projected an arm through the two measured apparent points (the bend's end at about (-200, 10230) and the boss at about (-1190, 11070), mm in the elevation), solving for its true rake at each angle out of plane (φ):

     | φ | true rake | a level line along the arm appears at |
     |---|---|---|
     | 0 | 40.3 | 0 |
     | 10 | 33.4 | 11 |
     | 20 | 24.3 | 21 |
     | 30 | 12.9 | 31 |
     | 35 | 6.6 | 36 |
     | 40 | 0.0 | 40 |
     | 42 | -2.6 | 42 |

   - The writer's "within 30 degrees of the plane, so 36 to 44" holds only at φ = 0. Within 30 degrees, the true rake is anything from 13 to 40.
   - Two readings agree on φ about 35 to 42, and so on a **true rake of about 0 to 7 degrees with the lantern near level and coaxial**:
     - the street's direction gives φ about 42;
     - a level, coaxial lantern gives φ about 35 to 40.
   - So does the lantern's apparent length (about 1.15 m): that is about 0.9 m pointing 40 degrees toward the camera, a normal size for that 11 m lantern. At φ = 0 it would be a 1.2 m lantern tilted 40 degrees, which no street lantern is.
   - So does the target's own lead: "5 m brackets had a vertical and a horizontal section".
3. **The target's combination is physically odd.** A side-entry boss is coaxial with the lantern it carries; it is not raked through the canopy's dome.

From the street this is the column's whole silhouette against the sky, by day and by night: a steep swoop into a flat box, against a level arm carrying its lantern.

**Exact amendment** (with F3's reach: the numbers below assume F3 is accepted; if not, keep the reach 225 and the bend 90 and apply only the rake and coaxial lines):

- **Rake:** `geometry.A.bracket.rake_deg` 0. The arm is horizontal, because the photograph gives 0 to 7. Tolerance in check `arm_rake`: expected 0, +-5. The kind: "Photo (US01, corrected for the arm's 35 to 42 degree turn toward the camera: true rake 0 to 7) + lead (vertical and horizontal sections)".
- **Centreline (y, z), in the column's frame:**
  - the stem vertical from z 4560 (inside the socket) to **z 4800.8**;
  - one bend of **90 degrees on centreline radius 130** (3 tube diameters) from (0, 4800.8) to (130, 4930.8);
  - a straight level arm from (130, 4930.8) to **(430, 4930.8)**, 300 long.
  - Regenerate `centreline_yz` at the same steps. `bend_turn_deg` becomes 90 and `arm_length` 300.
- **Boss:** axis horizontal along +y from (0, 430, 4930.8) forward 55, coaxial with the lantern's long axis on its centreline (`axis_deg_above_horizontal` 0). Its top stands 24 mm above the canopy's rear crown at 4937 and nothing pokes through the dome.
- **Lantern:** stays level (`tilt_deg` 0, check `lantern_tilt` 0 +-1.5 kept).
- **New check `arm_lantern_coaxial`:** the angle between the arm's last 50 mm, the boss axis and the lantern's long axis (all in the y-z plane) is at most 2 degrees.
- **New self-check B test:** lay the bracket and lantern on US01's elevation in 3D, with the arm's plan direction taken from the street's vanishing point (bearing -147.8), not in the picture's plane.
- **Wrong copy:** replace W's "a 30 degree rake" with "a 40 degree rake" and "a level lantern on a raked arm".
- **TARGET.md:** rewrite 5.3, 7 (add a PW8: the rake) and 10 to match. The section 10 line "the photograph is followed" becomes "the photograph, read in 3D, gives 0 to 7 degrees".

### F2. Steel as the main model, concrete as an unbuilt variant: backwards in my judgement, and chosen on evidence the brief does not accept

**Where:** TARGET.md 0.4, 6 and PW6; target.json `variants` (A build, C "build": false).

**My judgement.** A minor street in the old quarter of a northern British port in 1990 would more likely have had **precast concrete columns** with 35 W low-pressure sodium lanterns on short brackets than painted tubular steel:

- Concrete was the usual minor-road column from the 1950s into the 1970s, when most such streets were first lit by sodium.
- Most of it was still standing in 1990; mass replacement came in the late 1990s and 2000s.
- Tubular steel became the usual NEW column from the 1970s. It is likely on a street relit after about 1975, and on main roads.
- This is the project's own period reading (production/research/street-clutter-1990, section 3: "Columns were precast concrete … into the 1980s"; "Wrong for 1990: … modern galvanised columns").
- The counter-reading, art-direction.md line 346's "sodium lanterns on swan-neck steel columns", is marked [inference] and sits in a list of American-versus-British tells. It is not period research.
- My judgement is from memory and that research. The network refuses every source that could settle it.

**Why it is a fault, not only a judgement.** The writer chose steel because "the only column photographs reached are steel". The brief accepts a later photograph only "of an object unchanged since the period … when you say why it is unchanged". The target says the opposite: "none is shown to be older than 2019, and a 2019 column in Tower Hamlets may be a replacement". Photographs win over books, but these photographs are not period evidence for the column's TYPE. They can only give the form of a steel column if steel is chosen. Choosing the main build's material on them reverses the rule's intent, and risks the "modern replacement stock" look the brief forbids. From the street the material is the column's most visible property: a slim black tube against a thick pale square post.

**Exact amendment:**

1. **Swap the roles.** C (precast concrete, the same lantern and light) becomes the main build for all four places; A stays fully written as the alternative. Record the swap in DECISIONS.md as a session decision Jafar can overturn. One line on his page if the builder wants it confirmed: "The street's lamp columns: concrete (recommended) or black steel".
2. **Bring C up to A's standard, so that unit 3.8 can build it from target.json alone.** As it stands, C has words and a few numbers, no profile list, no bracket centreline and no check of its own:
   - `geometry.C.shaft` as a point list of (z, side, chamfer): (-150, 220, 15), (0, 220, 15), (4620, 125, 15). The taper is linear, the arrises chamfered 15 throughout, and the top face is flat with a 5 mm chamfer.
   - `geometry.C.bracket`: a 48 OD steel stem rising from the top face's centre (a 30 tall, 90 OD cast-steel cap seated on the top) to the same 90-degree bend and level arm as amended A in F1, with its own `centreline_yz`.
   - `geometry.C.door`: the recess 120 x 330 x 14 at z 450 to 780 on -y; the plate 132 x 342 x 3, 3 proud, two screws 10 across at 25 from its ends, blank.
   - Checks for C: shaft side at z 300, 2300 and 4300 (213.8 / 172.7 / 131.6, +-6); chamfer 15 +-3; the section square to the street +-2 degrees; the door recess and plate (+-5); the top cap and stem entry (+-5); albedo (146, 143, 136) +-12; roughness 0.9 +-0.1; no paint.
   - Wear for concrete: green algae to z 700 on -y; lime streaks from the top; rust bleed under the door plate's two screws; and on LC 2 only, one chipped arris 60 long x 25 wide x 8 deep at z 400 to 460 on +y (replacing A's dent).
3. **Before C is built, check its form from the PC** against dated photographs (the research's Geograph 1485521 and the lighting-enthusiast pages it names; Geograph and Wikimedia photographs of 1975 to 2000 by date taken), as CLAUDE.md says for what the cloud cannot reach. Until then, every C number keeps its Judgement mark.

### F3. The bracket's reach follows the stand-in against the target's own Read source

**Where:** target.json `numbers.lantern_centre_outreach` (500, "Read", "kept") and `numbers.research_bracket_projection` (406 to 457, Read); TARGET.md 5.3 and 5.8. The result is a reach of 225 mm from the axis to the lantern's rear (the boss).

**The issue.**

- The earlier research (Read) gives the period bracket's projection as "1 ft 4 in to 1 ft 6 in" (406 to 457 mm) and "an arm reaching out 40 to 45 cm".
- The writer's own note says this is the projection "to the spigot", but then keeps the stand-in's 0.5 m to the lantern's CENTRE. That halves the spigot reach to 225.
- The 0.5 is the stand-in's trade guess (the scene file's own words), not a measurement or a ruling.
- US01's proportion agrees with the research and not with the stand-in: reach to the boss about 0.12 to 0.14 of the column's height, which is 0.6 to 0.7 m at 5 m.
- From the street, a 225 mm reach puts the lantern almost on the column's top: the rear of the canopy is 190 mm from the socket's face. It reads like a post-top lamp knocked sideways, not a bracket lamp.

**Exact amendment.**

- **Reach to the spigot:** 430 (Read, the research's 406 to 457).
- **Lantern:** rear end at y 430, centre (0, 705, 4900), front end at y 980. Update the `envelope` and the canopy, bowl, lamp, hinge and catch y stations by +205.
- **Light position:** (0, 705, 4850).
- **Checks:** `lantern_centre` [0, 705, 4900] +-12; `arm_reaches_boss` [430, 4930.8] +-12; `light_position` [0, 705, 4850].
- **Placement:** the lantern's centre then stands 65 mm behind the kerb face, and its front end 210 mm over the channel. That is the usual place for the pool, so the placement table's text changes accordingly.
- **Handover for the scene file:** `outreach_m` 0.5 becomes 0.705. The night note's pool and skirt numbers are unchanged; the pool moves 0.2 m toward the road.

## Narrow points (each a small detail with an exact fix)

1. **The socket ("collar").** US01's shaft top is not a 60 mm collar 3.5 mm proud. It is the bracket's socket sleeve:
   - about 450 mm long on that 11 m column;
   - no step from the shaft that a 7 mm pixel can see;
   - a flat top with a small chamfer into the stem, a seam at its foot, and two set screws one above the other on one side.

   Amend: a socket z 4370 to 4620, OD 64 (2 proud of the shaft), its top edge chamfered 3, the two M8 set screws on -y at z 4580 and 4420. Check `collar` becomes {"od": 64, "z": [4370, 4620]} +-4.
2. **The door's corners.** US01's flush door has rounded top corners. Add a corner radius of 15 (Photo, US01, about 2 px at 7 mm) to all four corners of the door and of its joint groove.
3. **The lamp's U-tube.** The research says "a glowing U-shaped tube", and US01's lit lamp shows bright stripes. Inside the 54 x 310 jacket, model the arc tube:
   - two legs of 16 OD with centres at x +-11, running y 350 to 640 (y 555 to 845 after F3);
   - joined by a half-torus at the front end.

   The tube is the full-strength emissive part, and the jacket glass glows at 0.3 of it.
4. **Emissive strength in units.** Only colours and the 0.45 ratio are given, so the builder would set the glow by eye; the night note asks for units. Add:
   - the jacket at about 27,500 cd/m² (4,550 lm / (π x its 0.0526 m² surface));
   - the bowl at about 5,500 cd/m² (80 % of the flux through about 0.21 m² of bowl, Lambertian);
   - or state that both follow VignetteShot.cpp's `kLampEmissiveUnitless` rule until the night audit puts them in units.
5. **The jacket's colour.** (255, 176, 28) contradicts the text's own "a sodium lamp's own light is one orange": the photograph's yellow core is the camera's clipping. Either set the jacket to (255, 137, 0) at full strength and leave the yellow core to the grade (the night note's step 2), or keep (255, 176, 28) and label it "a camera-highlight look, not the lamp's colour".
6. **Check `lantern_dome_height`.** It reads "at y = 500" but expects 63, while the geometry gives 61 there (4998 - 4937); 63 is the maximum, at y 400. Change it to "the maximum over y, 63 +-6" or "at y = 500, 61 +-6".
7. **The cone's angle.** The text says 24 degrees; the profile (62 to 34 over 60) gives 25.0. Change the text to 25 degrees.
8. **W1, the wall bracket.** Its 10-degree arm enters a level lantern, the same kink as F1. Make W1's arm level and coaxial with the lantern (rake 0), or tilt W1's lantern 10 degrees with its arm.
9. **The shaft's top on a bracket column.** It is 60 (from BGE's post-top column). The target already lists that a bracket column may be 76 there. Leave it as it is, but if C is ruled out and A is built, use 64 to 68 at 4560 (a straight taper from 68, nearly parallel), so that a 48 stem and the socket do not look heavier than the shaft.

## What is right

- **The lower column, measured honestly.** The sleeve (124, +-9) and its 978 height, the 60 mm straight cone with its ring, and the shaft's taper (68 to 60) all come back on my own full-resolution readings within 2 mm. The overlay on the BGE strips is fitted on the sleeve alone, as the brief asks, and the stated +-7 % camera-height error is right and said plainly.
- **The paint and wear** are read off BGE and are plausible for a tired 1990 column: black (31, 31, 34) gone to semi-gloss, the road-film band to 250, chips to primer, hairline scratches, rust at fixings and sticker remnants. So are the root (paving cut round the sleeve, no base plate) and the generic plate "LC n" with no maker, council or crown.
- **The lantern's long axis along the arm** (PW3) is right: side-entry lanterns lie along their brackets. So is the boat-shaped canopy over a trough bowl from the research, with no gear box, no photocell and no ornament.
- **The writer's three findings hold against the files:**
  - The approved Hook sheet shows no lighting column: I read it at full size, and the only vertical on its skyline is a mast on the far hill.
  - The four columns stand at x 8 east, 18 west, 28 east and 38 west. StreetVignette.cs gives first 8 and step 10 up to 46, alternating sides; the pieces file has column0 to column3 at those x with z +-3.725. SCENE-SLOTS.md's "every 20 m" is the spacing on one side.
  - The scene file's lantern colour is wrong twice: about 585 nm, not 589, and green left undivided.
- **The lit colour agrees with the night note.**
  - The light is (1, 0.25, 0), and the bowl's (255, 137, 0) is that colour gamma-encoded.
  - The pool, skirt and glow (350, 800 and 40 lm; 15/55 and 45/80 degree cones) are the note's step 4.
  - The note's colour try (1, 0.40, 0.03) is recorded as a try.
  - The lit US01 lantern's median (251, 152, 14) supports the orange.
  - It keeps the night ruling: pools with dark between, the column and canopy unlit paint.
- **Rules:**
  - Only reached sources are used. The refused hosts are listed as unreached, and no search summary is used as a number.
  - CC0 licences are read on the page, and the dates are given as 2019, with the possibility of replacement said.
  - No maker's name appears on any part (the self-check's test names are the only mentions).
  - The previews are cropped to the object, under 300 KB and at most 1200 px, with no content-rule material.
- **Buildability.** Apart from F1 to F3 and the narrow points, a script can build every part of A from target.json alone: the revolved profile, door, plate, screws, bracket centreline, canopy and bowl lofts (their formulas are given), lamp, hinge, catches, boss, materials, wear zones, bevels and triangle budget. The 54 checks cover what matters from the street, except the arm-to-lantern junction and the reach, which F1 and F3 add.
