FAIL

# Front door target: fresh review (cloud week 42, 8 October 2026)

**How it was judged.** This cloud's network refuses Wikimedia Commons, Geograph and archive.org (403), so no source page could be opened today. The photographs were judged on the reduced copies in production/previews/cloud-week/refs/front-door/ (P1 480 x 640, P2 675 x 1200; pixel places below are in those copies), cropped and enlarged with PIL. The licences and dates are as the lab recorded them on 8 October (P1 Robin Stott, CC BY-SA 2.0, 2012-05-06; P2 Acabashi, CC BY-SA 4.0, 2024-02-03). The book pages were read from the lab's saved page images. self_check.py and target_drawing.py were run on a scratch copy. They reproduce exactly: 230 of 231, with the one reported miss, and an overlay identical to the committed one, pixel for pixel. The target itself was not touched.

## Faults, worst first

### 1. The quoins change every course; in P1 they change every three courses (T1, seen from the street)

- **P1, both reveals, rows 78 to 528.** The buff dressings are long-and-short blocks three courses high, and both sides are in step.
  - On the right side, the red brick starts at about x 304 for short blocks and x 328 for long ones.
  - The blocks run: short rows 80-118, long 120-163, short 166-213, long 214-253, short 254-301, long 302-349, short 350-397, long 398-437, short 438-485, long 486-527.
  - The left side matches: short 80-112, long 122-158, short 168-202, and so on.
  - Each block is 46-48 px, which is three courses of 15.3 px.
- **What the target draws instead.** target_drawing.py alternates long and short every single course (quoin_l29/r29, 225 wide, sits at the top, then 112, then 225 ...). That is a fine sawtooth where the photograph has bold blocks; the overlay shows the mismatch on every block.
- **target.json.** It never states the rhythm, so a script cannot build it from the json alone.
- **It contradicts itself.** brick.arch says the ring "bears on the top 112-wide quoin course", but the drawing puts a 225 course there. G9 still passes.
- **Amendment** (in `brick.quoins`):
  - Add `"block_courses": 3`, `"blocks": 10` (z 12 to 2322, each block 231 = 3 x 77), `"top_block": "short"` (z 2091-2322) and `"bottom_block": "long"` (z 12-243).
  - Add `"sides_in_phase": true`.
  - Keep the brick sizes 112 and 225 plus a 10 joint. P1's right side reads 25.5 px and 50 px from the reveal, about 127 and 250 mm, inside the error.
  - The reveal's return faces are the same buff brick.
- **New check, and a self-check test.** The red/buff boundary steps every 3 courses (231 +-8), with the top block short. In self_check, test the block boundary rows above on P1 within 2.5 px.

### 2. The arch is drawn flat-topped with 12 upright bricks; P1 and Ellis both show a segmental ring of 13 (T1, seen from the street)

- **P1, x 104-285, rows 25-78** (the c1 arch region): there are **13** bricks on end. The joints fall at about x 119, 132, 146, 160, 173, 187, 200, 213, 227, 241, 255 and 268, which is 13.7 px per brick.
- **The top of the ring is curved, not flat.** It sits at row 28.1-28.7 at the crown (x 160-210) and at 32.4-32.9 at both ends: it rises 4.5 px (about 22 mm), parallel to the soffit, which sits at rows 70 (crown) and 74-76 (ends).
- **This is not lens bow.** The mortar course above it, rows 16.4-17.9 from x 30 to 250, is straight.
- The end joints lean outwards, as a segmental arch's do.
- **Ellis p.112 Fig. 355,** the target's own source, draws the same: a segmental ring with radiating joints and a curved top.
- **What the target has.** target.json says "a flat-topped gauged arch", 12 bricks, top flat at z 2555. The drawing makes them upright rectangles.
- **Why the self-check missed it.** It allowed "11 or 12" bricks and tested the top at one point only (photograph 32.5, the end value) with a widened 5 px tolerance. It never tested the crown.
- **Amendment** (in `brick.arch`):
  - kind: "segmental ring of bricks on end, extrados parallel to the soffit".
  - `bricks` 13, joint 8, pitch 71.3 along the soffit.
  - The soffit is a circle through (0, 2322), (441, 2340) and (882, 2322): R 5411, centre (441, -3071).
  - The joints are radial to that centre.
  - The ring is 215 deep throughout, so its top is z 2555 at the crown and 2535.9 at the ring's ends (x -22 and 904); the soffit there is 2320.2.
  - Checks: replace "11 or 12" with 13. Test the ring's top at x 106, 184 and 280 px against rows 32.9, 28.5 and 32.7 (wall plane, 2.5 px). Add G11: the extrados rises 19 +-6 from the ends to the crown, with 13 bricks and the joints radial within 2 degrees.

### 3. F1's jambs are 73.4 mm wide where P2 shows 49 (photographs-win not applied; seen from the street)

- **P2, both jambs, rows 300-900** (left about x 140-162, right about x 508-530): the jamb strip is 21 px, about 49 mm, then a groove and the pilaster. The writer read the same.
- **What the target does.** It keeps the 944 bay, which makes the jambs 73.4, and leaves the choice as "could not settle 1".
- **Nothing stands against the photograph.** The 944 is not a photograph or a printed figure. It comes from the shopfront research's own arithmetic, "with 50 mm jambs and 3 mm gaps the side door is 0.944" (FRONTAGE-2026-10-06, point 4). It already assumes a 50 mm jamb, and SCENE-SLOTS says the photographs win.
- **Amendment** (F1):
  - `jamb_showing_past_brick_mm` 49.0.
  - Opening 895.2 (797.2 + 2 x 49).
  - jamb_x left [-52.6, 49.0], right [846.2, 947.8].
  - Leaf x0 28.6.
  - Glazing opening x [49.0, 846.2]; clear glass [59.0, 836.2].
  - Keep centre x 878.6.
  - glb_pivot x 447.6.
  - B13 becomes 49.
  - The shop bay's remaining 48.8 mm (24.4 each side) belongs to the shopfront's pilaster return, which is the groove and pilaster P2 shows.
  - Close could-not-settle 1.

### 4. F1's transom nose is half the height P2 shows, and its ends are square where P2's are splayed (close up)

- **P2, mid-transom, x 250-400.**
  - There is a dark quirk at rows 105-107.
  - Under it, the nose is one full round from row 107 to row 121 (14-16 px, about 32-37 mm). It is lit at 108-110 and darkens through 111-116 to its underside at 117-120. Black shadow follows from row 121.
- **What target.json has.** Its F1 profile is convex only from z 0 to about 16 and flat at y -10 from z 22. The listed "nose 0-36" zone therefore reads half as plain face, and there is no quirk.
- **P2's ends** (x 150-162 left, 508-520 right):
  - the face runs 11-12 px (about 28 mm) past each stop edge;
  - the nose is cut back on a 45-degree splay, from the face's end at row 106 down to the stop edge at its underside (row 117).
- The target specifies square ends with a 16 mm overlap. Its could-not-settle 6 admits that P2 shows otherwise.
- **Amendment** (F1 `transom.front_profile_yz_mm`):
  - Points: (0,0) (-12,0) (-16,1.5) (-19.5,4.5) (-21.5,9) (-22,14) (-21.5,19) (-19.5,24) (-16,28.5) (-12,31.5) (-9,33) (-7,34.5) (-10,36) (-10,70) (9.5,102). That is a 33 mm round, fullest 22 proud at z 14, with a 3 mm quirk at z 33-36.
  - Ends: the face and the nose's top run 28 +-5 past each stop edge.
  - The nose is returned on a 45-degree splay in elevation, from (stop edge + 28, z 32) to (stop edge, z 4).
  - D5 becomes "face 28 +-5, nose underside 0 +-3".
  - D4 and E-style crest checks follow the new points.
  - T1 may take the same end treatment at its 10 mm overlap (Judgement: P1 is too small to show it).

### 5. The door's foot: the plinth is named but not specified, and the tread's front does not match P1 (T1, seen from the street)

- **P1, rows 527-600, both sides** (x 60-117 and 265-480).
  - The wall has a projecting red-brick plinth. Its top is a course of splayed headers (not "dog-tooth"), and the splay's top sits at the leaf's bottom (about z 12, where the quoins begin).
  - It returns into the reveal on both sides, and the splay stops against the white jamb's foot (right foot about x 268-275, row 529).
  - The tread's ends run past the reveals in front of it.
- **What the target says.** "Wall detail, not specified." Yet it builds the quoins above the plinth "so the opening is built right" and stands the jamb feet bare on the threshold. The foot will not look like P1, and where the tread meets the plinth is left undefined.
- **The tread's front.** In P1 (rows 562-600) it is a full rounded nosing: lit crest at row 581-582, turning under by 592, then a dark undercut shadow at rows 593-599 across the whole width. The target's 30 mm quarter-round over a plain face would show no such shadow.
- **Amendment:**
  - Add `brick.plinth` for T1: red brick (159,113,85).
  - Its top course is a splayed header course 77 high, the splay 45 degrees, its top edge on the wall face at z 12.
  - The plinth face is 56 +-20 proud of the wall face (Judgement: P1 is frontal).
  - It returns into the reveal both sides, the splay stopping square against the jamb face at the foot.
  - The tread's ends butt against the plinth's face.
  - Tread front: a full half-round of radius 45 +-15, overhanging a 20 +-10 undercut. Update G4.

### 6. F1's threshold is set 70 above the pavement where P2 shows about 45 (close up)

- **P2, x 300-400:**
  - rows 946-959 are the sill's top, seen from above;
  - rows 960-979 are its front face, 20 px, about 46 mm;
  - the concrete starts at row 981.
- target.json's own source line says "top about 40 above the paving", yet it sets ground_z -70, and G6 says "top 70 above the pavement".
- **Amendment:** F1 `ground_z_mm` -45 (+-10), with the 70 mm sill bedded 25 below the paving. G6 becomes "top 45 above the pavement"; glb_pivot z becomes -45.

### 7. Checks that would fail a correct build or pass a wrong one

- **B17** gives the head's top as 2371.2, but the head is cut to the soffit at 2340/2322 (frame.head_section_mm, G8). Set B17's z to 2340 at the crown.
- **G10** ("check 46.6 behind the brick") and **I5** ("x 975.2") apply to both variants, but F1 has no brick: its jambs hide 28.2 behind the pilaster (52.6 after fault 3) and its frame is 1000.4 wide. Give F1 its own values.
- **Nothing checks faults 1, 2 or 5:** the quoin rhythm, the arch's curved top, its brick count, the plinth. Add checks as listed under each fault.

## What is right

- **The leaf and frame proportions hold, re-checked independently.**
  - The band is at rows 363.5-377.5 and the weatherboard at 513.7-529.7, both confirmed by column profiles.
  - The jambs are 9-11 px.
  - The plate, lock, keep and moulding edges all fall within 2 px on P1.
- **Every fault in the lab's two reviews is answered:**
  - the frame is square and flat (D10, C1-C2);
  - the T1 transom projects, with lip, cove, face and slope traced from P1 rows 143-156;
  - the band and weatherboard are moulded profiles from P1 with a crisp underside, stopping short of the stops;
  - the ironmongery is measured: plate 76 x 242 at 1617, cylinder 43.5 at 46.6 in, the dark plate on the jamb;
  - there is a deep stone step with a recessed riser;
  - the arch bears on the brick;
  - the muntin is 120;
  - there is a glazing bead;
  - coplanar faces and dark hairlines each have a check (I1, I2).
- **The printed numbers were confirmed on the pages:**
  - Ellis p.93: 4 1/2 in stiles; 9 in middle and bottom rails; lock rail 2 ft 8 in to its centre, 6 in lower from a step.
  - Hasluck p.347: 2 ft 8 in.
  - Hasluck p.398: "double rebated and weathered transom".
  - Riley p.357: "5 x 4 rebated frame", "Transome 5 x 4", bolection outside and a single moulding inside.
- **The record keeping is sound.**
  - Disagreements D1-D17 are written down, each with its choice.
  - The element-by-element table exists.
  - Unreached pages are stated, and nothing from them is used.
- **The other rules are kept.**
  - Licences are free (CC BY-SA), with nothing NoAI.
  - There is no brand, cypher or maker's mark, and the house numbers are optional and left to the town.
  - The 1990 wear rule puts the fresh P1 red down to a minor weight.
  - Colours are given in sRGB with roughness and metal.
- **F1's furniture follows P2 closely:** the turned knob, the knurled cylinder at 46.3 in, the plugged keyhole and the screws.

## Narrow notes (not faults)

- **P1's dark plate on the right jamb** (rows 300-314) may be a bell push rather than a keep. An inward-opening door's latch keep sits in the rebate, out of sight. As drawn it matches the picture either way.
- **P2's fanlight** shows a chipped putty line at the glass foot, with no planted bead distinguishable. F1 could take putty glazing instead of the 10 x 8 bead.
- **The house numerals'** letter form is not specified (optional).
- **The tread's width check** compares camera distances only "within a factor 1.8". It holds (941 to 960 mm for a camera 4.8 to 5.8 m away), but the test is too loose to catch anything.
