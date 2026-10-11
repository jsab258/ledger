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

## Re-review (try 2), 11 October 2026

FAIL

**One fault and six narrow points.** Try 2 answers the first review's three faults and nine narrow points as they were written. With the network open, though, the photographs show that variant C's bracket is wrong. C is now the main build, and the first review prescribed that bracket from memory: a thin black steel tube, bent round on a radius and rising from a cap. Every photograph of a concrete column with an angular arm shows instead an arm as thick as the column's top, joined to it in a sharp mitre and made of the column's own concrete. That is R1. The narrow points are the lantern's length, the lantern's rear boss passing through the bowl, one check's number, and three corrections to the text. The exact amendments follow, in the order they are to be applied.

Reviewer: a fresh reviewer who neither wrote nor will build this target. I read REVIEW-BRIEF.md, BRIEF.md, CLAUDE.md, the first review above, the whole of TARGET.md (try 2), target.json, period_photos.json, the lamp column row of SCENE-SLOTS.md, self_check.py and target_drawing.py, and every preview in production/previews/cloud-week/refs/lamp-posts/. Nothing in the target was edited and nothing was committed. Only this section was appended.

### What was re-run, and what was reached

- **self_check.py**, run on a scratch copy of target.json (`--target`, with TMPDIR in the scratchpad so that the US01 3D fit was computed afresh, not read from a cache): `SELF-CHECK PASS: 286 of 286 tests pass (A 75/75, B 35/35, C 41/41, D 27/27, E 64/64, T 26/26, W 18/18)`. The repository's target.json was byte-identical afterwards (md5 0b862162…). The fresh 3D fit agrees with what the target prints:
  - with the arm at bearing -147.8: a free rake of -0.15 degrees; a level arm fits to 4.19 mm and a 40-degree arm to 43.48 mm;
  - with the arm in the picture's plane: 42.41 degrees.
- **target_drawing.py** ran on target.json alone and wrote 22 views and the polygons file. I looked at C's side elevation, C's bracket detail and the lantern's long section (x = 0).
- **Geograph, reached 11 October 2026**, with a browser user agent: each photo page and its 640 px picture. The date taken and the licence were read on each page.

  **The target's five photographs.** All five agree with the target.

  | id | photo page | photographer | taken | licence |
  |---|---|---|---|---|
  | GG1 | 823762 | Peter Whatley | 1989-02-21 | CC BY-SA 2.0 |
  | GG2 | 823771 | Peter Whatley | 1989-04-18 | CC BY-SA 2.0 |
  | GG3 | 1485479 | Robert Lamb | 2008-06-14 | CC BY-SA 2.0 |
  | GG4 | 1479864 | Robert Lamb | 2009-06-14 | CC BY-SA 2.0 |
  | GG5 | 2049282 | John Brightley | 2010-08-31 | CC BY-SA 2.0 |

  **Seven more, from the feed's queries "concrete lamp post", "concrete lamppost", "concrete street light" and "concrete lamp standard" (259 results).** All are CC BY-SA 2.0, read on their pages.

  | photo page | photographer | taken | what the page and the picture give |
  |---|---|---|---|
  | 1485521 | Robert Lamb | 2008-06-14 | Its page calls the column a 1950s concrete column. The earlier research names this photograph, and try 2 did not open it. |
  | 5418611 | Christopher Hall | 2017-01-11 | "1960s concrete street light columns photographed just before their removal" (North Yorkshire) |
  | 7029133 | Stephen Craven | 2021-11-16 | "relatively low, concrete lamp post with what is probably a sodium lamp" (West Yorkshire) |
  | 6558618 | Graeme Paterson | 2019-11-09 | "Concrete lampposts with matching concrete outreach brackets" (Edinburgh) |
  | 6538305 | Graeme Paterson | 2020-07-12 | Concrete columns "from around 1970. Originally they were fitted with matching concrete outreach brackets. The lanterns fitted had low pressure sodium lamps". The picture shows later steel sleeves; only the words are used. |
  | 1581328 | John Baker | 1984 | A station's "distinctive concrete lamp-posts", "replaced by modern metal variants around 1990". A period photograph, but too small to measure. |
  | 1496139 | Robert Lamb | 2008-12-14 | The page says the lantern and bracket are not the original ones, so it was not used. |

  Their pages name the makers of the columns and lanterns. Those names are not repeated here.
- My measurements are on the 640 px pictures, with a luminance threshold against the sky. I worked in pixels, so only ratios are used. The pictures are in the session's scratchpad only, not in git.

### How try 2 answered the first review

| item | answered? | what I checked |
|---|---|---|
| F1 rake | yes | I recomputed the centreline: the stem rises vertically to 4800.8, the 90-degree bend has radius 130 about (130, 4800.8), and the level arm runs to (430, 4930.8). The boss is horizontal and coaxial with the arm. The checks arm_rake (0 +-5) and arm_lantern_coaxial (2 degrees) are in. The 3D fit holds on a fresh run, and the 40-degree wrong copy is refused. Of the 1989 photographs, GG1's arm rises 8 degrees in the picture and GG2's lantern top 11 degrees, with the lantern in line: they agree. |
| F2 concrete main | yes in its roles, no in its bracket | C is the main build, A is written out in full, and C has its own profile, door, plate, checks and wear. The swap is now supported by period words: concrete columns of the 1950s to about 1970 stood into the 2000s and later (5418611, 6538305, 1479864), and a station's concrete posts were replaced "around 1990" (1581328). But C's bracket contradicts the photographs: see R1. |
| F3 reach | yes | Reach 430, centre 705, front end 980, light (0, 705, 4850). The checks, placement text and handover are updated. |
| points 1 to 9 | yes | Each has its T row. Point 6's new number for the dome over the boss is wrong: see narrow point 3. |

### R1. Variant C's bracket: a thin black steel tube on a cap, where the photographs show a concrete arm as thick as the column's top, joined in a mitre

**Photographs and places.**
- **GG3** (Birchington, 2008): the target's own photograph for the angular form. The elbow is at x 343 to 354, y 76 to 100 of the 640 px picture.
  - The shaft's top is 10 to 11 px wide, rows 100 to 140.
  - The arm is 9 to 10 px thick measured vertically and rises 16 degrees, so it is about 9 px across, 0.85 to 0.9 of the top.
  - It meets the shaft in a sharp mitre: the inner corner is square and the outer corner rounded by about 2 px.
  - There is no cap, no separate stem and no bend radius. The arm's top line runs on into the canopy's.
- **1485521** (a 1950s concrete column, 2008), the column top at x 329 to 375, y 5 to 75:
  - the top is 7 to 8 px wide and the arm about 9 px across (1.0 to 1.2);
  - it has the same sharp mitre; its arm ends in a pendant lantern.
- **5418611, 7029133 and 6558618:** the shaft's own width and colour carry on into a curved arm.
- **6538305 and 6558618, in their photographers' words:** "matching concrete outreach brackets" on concrete columns of about 1970 with low-pressure sodium lanterns.
- **Thin steel brackets:** only GG4 and GG5 show one on a concrete column. Both are curved goosenecks or hooks, and GG5's rises from a pale socket cap.
- **The target's bracket appears on no concrete column.** No photograph of a concrete column shows a thin black tube with one round bend standing on a cap. That bracket is the steel stations' (GG1, GG2).

**What the target says.** It has a 48 OD black steel stem rising through a black cast cap 90 OD and 30 tall at z 4620 to 4650. The stem turns through one 90-degree bend of radius 130, and a 300 level arm follows. This is the first review's F2 amendment, written from memory before the network opened. TARGET.md 4.2 reads GG3 as agreeing, but it did not read the arm's thickness or the missing cap. The photographs win, element by element (8 October).

**From the street.** The column's head is seen against the sky by day and at dusk:
- arm to top width: the target's 0.38 against the photographs' 0.85 to 1.2;
- the target's black against concrete;
- a round bend standing on a cap against a mitre.

**Exact amendment.**

Keep the amended rake (0), the reach (430) and the lantern.

1. **`geometry.C.shaft.points_z_side_chamfer`.**
   - The points: (-150, 220, 15), (0, 220, 15), (4620, 125, 15), **(4985.8, 117.5, 15)**. This is the same straight taper carried up to the arm's top, so the checks at z 300, 2300 and 4300 do not change.
   - `top_z` 4985.8. The top face is flat with a 5 chamfer, and it is one face with the arm's top.
2. **`geometry.C.cap`:** deleted. There is no cap.
3. **`geometry.C.bracket`** is replaced by a precast concrete arm cast as one with the shaft:
   - Section and axis: **square, 110 x 110**, its four arrises chamfered 10, its axis level at **z 4930.8** (top 4985.8, underside 4875.8).
   - Length and end: from the shaft's -y face (y -58.7) along +y to a flat end face at **y 400** (edge chamfer 5).
   - **The joint is a mitre, with no bend.** The outer corner, where the top face meets the shaft's -y face, is rounded to **radius 20**. The inner corner, where the arm's underside meets the shaft's +y face at (59.9, 4875.8), is a **fillet of radius 10**.
   - Material: concrete_C, unpainted.
   - Data: `centreline_yz` [[0, 4930.8], [400, 4930.8]]; `section` {"square": 110, "chamfer": 10}; `joint` "mitre"; `bend_turn_deg` 90; `rake_deg` 0.
   - Kind: Photo (GG3 and 1485521, the arm about 0.85 to 1.2 of the top; the mitre) + Judgement (110, 10, 20).
4. **New `geometry.C.spigot`:**
   - a steel tube, **OD 42**, painted black (31, 31, 34), on the arm's axis from **y 340** (60 cast into the arm) to **y 485** (inside the lantern's boss);
   - **30 of it shows between the arm's end (400) and the boss (430)**;
   - the boss, the lantern and the light are unchanged.
5. **Checks.**
   - `arm_stem_od_c` becomes `c_arm_section`: {"width": 110, "height": 110, "chamfer": 10, "axis_z": 4930.8, "end_y": 400}, +-5.
   - `c_top_cap` becomes `c_mitre`: {"outer_corner_radius": 20, "inner_fillet_radius": 10, "top_face_z": 4985.8}, +-5.
   - `c_stem_entry` becomes `c_spigot`: {"od": 42, "y": [340, 485], "exposed_y": [400, 430]}, +-3.
   - `arm_bend_turn`, `arm_bend_radius` and `arm_continuity` apply to A only.
   - `arm_rake`, `arm_reaches_boss` and `arm_lantern_coaxial` apply to both, measured for C on the arm's and spigot's common axis.
   - `c_albedo` and `c_roughness` cover the arm.
   - `c_no_paint` reads "the shaft and arm carry no paint; only the spigot is black".
6. **Materials.** `c_cap_stem_arm` becomes `c_spigot`: (31, 31, 34), roughness 0.42, metal 0, "the steel spigot from the concrete arm into the lantern's boss".
7. **Wear (C).** Add:
   - an algae film on the arm's top face;
   - 2 to 4 lime streaks from the arm's underside and end face, 30 to 150 long, 4 to 12 wide, (190, 188, 180);
   - one rust streak 20 to 60 long under the spigot at the arm's end.
8. **Words.**
   - `variants.C.name`: "precast concrete column with a cast concrete arm, the lantern".
   - TARGET.md, summary line: "a black cast cap carrying a plain bent-arm bracket (a 48 stem, ONE 90 degree bend of radius 130, a straight LEVEL arm reaching 430 from the axis)" becomes "a precast concrete arm of the shaft's own width (110 square) leaving its top in a mitre and running LEVEL to 400, a 42 steel spigot carrying the lantern's rear boss at 430".
   - TARGET.md 5.2: the "Cap and stem" bullet becomes the arm and spigot above.
   - TARGET.md 5.3: C's half is reworded the same way.
   - TARGET.md section 7: add a **PW13** row. What: the arm on a concrete column. The book or stand-in: the first review's 48 steel stem, cap and bend. The photographs: GG3 and 1485521 (a mitred arm 0.85 to 1.2 of the top); 5418611, 7029133 and 6558618 (curved arms of the shaft's width); 6538305 ("matching concrete outreach brackets", about 1970, low-pressure sodium). Chosen: the mitred concrete arm. Kind: Photo.
   - TARGET.md section 10: the arm bullet becomes "concrete arms of the shaft's own width, mitred (GG3, 1485521) or curved (5418611, 7029133, 6558618); thin steel goosenecks also stood on concrete columns (GG4, GG5); the mitred concrete arm is built".
9. **Sources and credits.**
   - Add the seven photographs above to TARGET.md 2.1, each with page, date read 2026-10-11, photographer, CC BY-SA 2.0, date taken, what it shows and how it is used, and to period_photos.json.
   - Make one preview: **gg1485521-essex-gardens-concrete-column-mitred-arm-2008.jpg**, the 640 px picture cropped to x 290 to 410, y 0 to 130 and enlarged 3 x. It shows sky, the column top, the arm and the lantern, with no lettering.
   - Credit the preview in section 13.
10. **Drawing and tests.**
    - target_drawing.py draws C's arm as the 110 band with its mitre and the spigot (side elevation, bracket detail, z 4620 plan).
    - self_check.py's rows that test the 48 stem and the cap test these numbers instead.
    - Add one wrong copy that self_check.py must refuse: "C with a 48 tube bracket on a cap".

### Narrow points (each a small detail with an exact fix; apply 1 before 2 and 3)

1. **The lantern's length: 550 is shorter than every source.**
   - **The evidence:**
     - The earlier research (Read) gives 600 to 700.
     - GG3's lantern is about 62 px long, about 6 times its arm (680 at the amended 110). Foreshortening only makes it longer.
     - GG1 and GG2's lanterns are 12 to 14 tube widths, against A's 9 (550 / 60).
   - **Exact fix: length 650.** Every lantern y station becomes 430 + (y - 430) x 13/11, and the boss stays at y 430 to 485. The station lists:
     - `canopy.plan_half_width`: [[430, 0], [435.9, 30], [453.6, 58], [483.2, 86], [518.6, 108], [565.9, 128], [636.8, 144], [695.9, 150], [778.6, 150], [873.2, 146], [955.9, 134], [1020.9, 108], [1062.3, 62], [1080, 0]].
     - `canopy.top_z_along_y`: [[430, 4937], [471.4, 4962], [542.3, 4990], [636.8, 5000], [755, 4998], [873.2, 4985], [967.7, 4963], [1032.7, 4945], [1080, 4937]].
     - `bowl.base_plan_half_width`: [[518.6, 0], [522.2, 22], [542.3, 52], [577.7, 70], [636.8, 80], [755, 82], [873.2, 80], [932.3, 70], [967.7, 52], [987.8, 22], [991.4, 0]]. The base is then 473 long and 164 wide.
   - **The lamp:** the lamp and its arc tube keep their sizes, centred at y 755:
     - jacket y 600 to 910;
     - holder y 555 to 600 (x +-30, z 4852 to 4892);
     - arc tube y 605 to 895, straight to 876.
   - **The lantern's other parts and the light:**
     - catches at y 932.3;
     - envelope y [430, 1080], centre (0, 755, 4900);
     - light (0, 755, 4850);
     - bowl emissive about 4,800 cd/m2 (its area about 0.24 m2).
   - **Checks:**
     - `lantern_bounding_box` {"y": 650, "x": 300, "z": 200};
     - `lantern_centre` [0, 755, 4900];
     - `lamp_in_bowl` centre [0, 755, 4872];
     - `lamp_arc_tube` y [605, 895];
     - `bowl_base` length 473;
     - `light_position` [0, 755, 4850];
     - `glow_strength` bowl 4800.
   - **Placement:** the lantern's centre stands 15 mm behind the kerb face and its front end 310 mm over the channel.
   - **Handover:** `outreach_m` 0.755. A's and W1's lantern is the same.
2. **The rear boss passes through the bowl.**
   - **The clash:** the boss (OD 60, axis z 4930.8, y 430 to 485) hangs 24 mm below the rim (z 4925). The bowl's rear wall (rim at y 438, falling to the base at 505) cuts through the boss's lower part, as the long section at x 0 shows.
   - **Why it matters:** seen from below through the clear bowl, the bowl's shell slices the boss.
   - **Exact fix**, in the coordinates after point 1:
     - `bowl.long_section_rear_curve_yz` [[488, 4925], [492, 4890], [500, 4850], [510, 4818], [518.6, 4800]];
     - a new `bowl.long_section_front_curve_yz` [[991.4, 4800], [1009.1, 4818], [1036.3, 4850], [1062.3, 4890], [1070.5, 4925]];
     - in `bowl.loft`, "for y from y_rear(z) to 1410 - y_rear(z)" becomes "for y from y_rear(z) to y_front(z)";
     - `bowl.rim_plan` runs between y 488 and 1070.5;
     - the hinge knuckles move to y 497;
     - a flat cast soffit (canopy material) closes the canopy's underside at z 4925 from y 430 to 488, and the boss's lower 24 mm hang below it.
   - **New check `boss_clear_of_bowl`:** the nearest distance between the boss and the bowl is at least 3 mm.
3. **The check `boss_top_and_dome` has the wrong dome height.**
   - It expects the dome over the boss's front end (y 485) at 4976.3, and TARGET.md 5.4 and the boss's note say 4976.
   - Linear between the stations, the dome there is **4971.3** today and **4967.4** after point 1. Use 4967.4 in the check and "4967" in the words.
   - The conclusion holds: the boss's top, 4960.8, stays under it.
4. **The photographers' words, and the count of 1989 photographs.**
   - **The summary line** (TARGET.md and target.json `summary_line`):
     - "original lanterns by their photographers' word" becomes "old by their photographers' word (GG4's 'looks to still retain its original low pressure sodium lamp'; GG3's lantern 'old', its decade not stated; GG5's lantern not dated)";
     - "three of 1989 show steel columns" becomes "two of 1989 (GG1, GG2) show steel columns".
   - **TARGET.md section 10:** "three photographs of 1989" also becomes "two photographs of 1989 (GG1, GG2)".
   - **S16 / GG3:**
     - "its original 1960s lantern" becomes "an old lantern (the photographer's word; its decade is not stated)";
     - "a mid-1960s to 1970s fitting" is deleted.
5. **The bend's readings disagree with each other.** TARGET.md 4.2 reads GG1 at about 3 tube diameters and GG2 at about 2. PW11 says Orrell is about 2 and Appley Bridge 2 to 3. PW11 becomes "Orrell (1989): about 3 tube diameters; Appley Bridge (1989): about 2", which matches 4.2 and the `arm_bend_radius` check. This applies to A only after R1.
6. **GG3's arm rise.** PW8 and 4.2 explain GG3's 19-degree rise as "a level arm pointing partly toward the camera". But the column stands near the picture's centre line and the photographer looked along the road, so the arm, across the road, may lie near the picture's plane. 1485521's arm rises about 18 degrees in the same way. Replace those words with: "GG3's arm rises 16 to 19 degrees in the picture (1485521's about 18); the arm's plan direction cannot be read off one 640 px picture, so its true rake is 0 to about 18; the level arm of US01 read in 3D and the 1989 photographs is kept (rake 0 +-5)". This changes no number.

### What is right

- **F1, F3 and points 1 to 9 are applied as written.** I checked the arithmetic myself:
  - the bend stations;
  - C's sides 213.8, 172.7 and 131.6;
  - the boss's top 23.8 above the crown;
  - 770 - 705 = 65 and 980 - 770 = 210;
  - the jacket's 27,500 cd/m2 (4,550 / (π x 0.0526)) and the bowl's 5,500.
- **A's lower column, paint and wear, the light block and the colour finding** are unchanged from try 1 and stay right, as the first review found.
- **Rules.** The rules all hold:
  - Every photograph's page, date and licence agree with what I read on 11 October.
  - The crops mask GG2's station sign and GG4's bus-stop sign. No preview shows anything the content rule bars.
  - No maker's name appears in TARGET.md, target.json or period_photos.json, although the photographers' pages name makers.
  - The unreached sources are listed as unreached.
  - The later photographs are argued as unchanged objects, and the new pages strengthen that argument.
- **Buildability.** With R1 and the narrow points applied, a script can build C and A from target.json alone. The checks then catch what matters from the street:
  - the head's silhouette (the arm's section, mitre and spigot);
  - the lantern's box and place;
  - the shaft's taper and chamfers;
  - the door, plate and colours;
  - the light.
