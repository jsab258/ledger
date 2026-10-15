Front door (four-panel, in frame, with transom, brick head, plinth and step), amended twice on 8 October 2026: the lab's proportions kept, every detail the two photographs show written down with a number or a profile; flat square-edged frame, weathered projecting transom, moulded band and weatherboard, measured ironmongery, buff quoins in blocks of three courses, a 13-brick segmental arch with a curved extrados, a splayed plinth, a full rounded step nose over an undercut; two variants (terrace T1, flat-over-shop F1 with 49 mm jambs, a full round transom nose with splayed ends and a threshold 45 above the paving) and six paint colours; self-check 303 of 304 pass, the one miss reported (P2's door is squatter than 0.838 x 1.981).

# Four-panel front door: amended target (cloud week 42, second try)

Files in this folder: `TARGET.md` (this), `target.json` (the same numbers, profiles, variants, 80 checks and the self-check result), `target_drawing.py` (draws target.json alone), `self_check.py`, `TARGET-REVIEW.md` (the fresh reviewer's, untouched), `lab-start/` (the lab's files, untouched). Run with `/home/user/.bpyenv/bin/python`: `target_drawing.py OUT_DIR [--overlay PHOTO OUT.jpg]` and `self_check.py`. The picture of the drawing on photograph 1 is `production/previews/cloud-week/refs/front-door/door-photo-01-teignmouth-target-on-photo.jpg`.

Axes (as the lab's): x across the opening left to right seen from outside, 0 at the left brick reveal; y into the wall, outside at -y, 0 at the wall's outside face; z up, 0 at the top of the threshold stone. Millimetres. Kinds: **Read** printed on a page; **Scaled** measured off a printed drawing against its own printed figure; **Photo** measured on a photograph (method and error given); **Derived** worked from other numbers; **Judgement** nothing else fits.

## 1. What changed from the lab's target

First amendment (against the lab's two reviews), then the second (against the fresh target review, section 2).

| # | Lab's target | Amended target | Photograph says | Decision |
|---|---|---|---|---|
| 1 | Frame with a 19 mm ovolo on the outer arris | Flat, square-edged frame, every arris square (eased 1 mm); F1 adds a 5 x 2.5 quarter-round on each jamb's stop edge | P1, P2 | D10 |
| 2 | Transom 65 mm, flush, plain | Weathered transom: lip bead, cove, flat face, 55 degree slope; T1 face 8 and nose 14 proud of the jamb faces; F1 102 high with a full round nose 22 proud | P2 (bold), P1 (light); Hasluck p.398 "weathered" | D11, D21 |
| 3 | Band 79.5 x 19 box; weatherboard 72 x 30 wedge; both to the jambs | Band 72.5 high, 22 proud, drawn profile with a square underside; weatherboard 80 high, 26 proud, belly, hollow and rounded nose; both stop 2 mm short of the stops | P1 rows 363.5-377.5, 513.7-529.7 | D13 |
| 4 | No ironmongery | Letter plate, cylinder lock 46.6 in, keep, optional number; F1 adds turned knob, knurled cylinder, plugged keyhole | P1, P2 | D15, D16 |
| 5 | Thin 76 mm sill | Threshold 76 with an r18 nose, recessed riser, a step whose nose is a full half-round (r45) over a 20 undercut, running past the opening; ground 318 below the threshold | P1 rows 534-610 | D12, D22 |
| 6 | Glass with no bead | T1 planted quarter-round bead 10 x 8; F1 putty fillet; clear glass 752 x 247 inside 772 x 267 | P1 glass foot and head lines; P2 putty | D7 |
| 7 | Muntin 132.2 | 120.0 (visible gap 110.4 = 14.3% of the visible width) | P1 re-measured | D2 |
| 8 | Brick head flat, stopping flush | Cambered 18 mm (a circle through (0, 2322), (441, 2340), (882, 2322)); a ring of 13 buff bricks on end, radial joints, a curved extrados, resting on the top quoin block | P1; Ellis p.112 Fig. 355 | D17, D19 |

## 2. Answers to the fresh target review (TARGET-REVIEW.md, 7 faults)

Each amendment was checked against the photograph before it was made. Where I differ from the reviewer's number, the measurement is given.

| # | Fault | How answered | Where I differ, and why |
|---|---|---|---|
| 1 | Quoins alternate every course; P1 changes every three | `brick.quoins`: `block_courses` 3, `blocks` 10, `block_height_mm` 231, `bottom_block` long, `top_block` short, `sides_in_phase` true, `block_z_mm` listed; the drawing builds 10 blocks of 3 courses, both sides alike; the reveal's return faces are buff; checks Q1-Q3; self-check fits the nine block boundaries on P1 (worst residual 3.0 px, wall-plane scale 5.03 mm a pixel) and tests the drawing's widths change only at courses 3, 6 ... 27 | Widths 122 and 237 (not 112 and 225): P1 reads 25.3 and 48.2 px from the reveal = 127 and 242 mm at 5.02; a header's 4 1/2 in and a stretcher's 9 in each with the 10 mm joint are 124 and 239. I re-scanned the right reveal by blue and green-to-red ratio per row: boundaries 119, 164.5, 210, 254, 301.5, 349.5, 397, 437.5, 486 (+-3), a 46.4 px (231 mm) pitch, as the reviewer reads |
| 2 | Arch flat-topped, 12 upright bricks | `brick.arch`: segmental ring, `bricks` 13, joint 8, radial joints about the soffit's centre (441, -3071.25), R 5411.25, extrados concentric (rise 19.1 from ends to crown); the drawing builds 13 wedge bricks; checks G11, G12; self-check tests the count exactly (13, and 12 joints read), the extrados at x 106, 184, 280 px (rows 32.9, 28.5, 32.7) and the soffit rows 73.5, 69.5, 73.5 on the wall-plane mapping fitted on the quoin blocks (all within 2.5 px), the drawing's joints within 2 degrees of radial and its rings concentric | Depth 207, not 215: crown 28.5 to soffit 69.5 is 41 px at 5.03 = 206 +-7 (215 is inside the error, 207 is the photograph); the soffit's ends lie at x -4.9 and 886.9 (the extrados corners at -22 and 904 are the photograph's widest x, 104.5 and 283.75 px, on the same radial lines), so the pitch along the soffit is 68.7, matching 13.7 px x 5.02 = 68.8 (the reviewer's 71.3 assumed the soffit's ends at -22) |
| 3 | F1 jambs 73.4, P2 shows 49 | F1 `jamb_showing_past_brick_mm` 49.0; opening 895.2; jamb x left [-52.6, 49.0], right [846.2, 947.8]; leaf x0 28.6; glazing opening x [49.0, 846.2], clear glass [59.0, 836.2]; keep 878.6; glb pivot x 447.6; B13 49; could-not-settle 1 closed; the bay's remaining 48.8 is the shopfront's pilaster return; self-check tests every coordinate that follows | none |
| 4 | F1 nose half the height, ends square | F1 profile as P2: a 3 mm quirk then one full round (z 0-33, 22 proud at z 14), the reviewer's points; the face and the nose top run 28 past each stop edge; the nose is cut on a 45 degree splay from (stop edge + 28, z 32) to (stop edge, z 4); D4, D5, D8 rewritten; T1 takes the same treatment at its 10 mm overlap (Judgement). I re-read P2 column x 250-400: slope rows 76-90, face 91-104, quirk 105-107, lit round 108-110, dark 111-120 | none (P2's 12 px overrun = 27.8 mm; the splay rows 106-117 over 12 px = 45 degrees) |
| 5 | Plinth unspecified, step nose a quarter-round | `brick.plinth`: red brick, front 60 proud, splayed top course (45 degrees from (y -60, z -48) to (y 0, z 12), bricks 65 wide at a 75 pitch, course 77), vertical face below in 77 courses to the ground, returns level at z 12 through the reveal to the jamb's foot, the tread's plan steps back to y -60 beside it; tread `nosing_radius_mm` 45 over a 20 undercut, base in shadow; G4 rewritten, checks L1-L5 | Ground -318, not -258: P1 shows the base face in shade for rows 600-610 (70 mm and more) under the nose; 258 left it no height. The photograph's splay band is 13 px (65 mm), the reviewer's 56 +-20 proud agrees with a 45 degree splay of 60 |
| 6 | F1 threshold 70 above the pavement, P2 about 45 | F1 `ground_z_mm` -45, sill 70 thick bedded 25 below the paving, visible front 45; G6 "top 45 above the pavement"; pivot z -45; self-check tests it against P2 rows 960-979 (19.5 px x 2.317 = 45) | none |
| 7 | Checks that fail a correct build | B17 gives the crown 2340 (2322 at the ends) and the frame widths T1 975.2, F1 1000.4; G10 and I5 per variant; new checks Q1-Q3 (quoins), G11-G12 (arch), L1-L5 (plinth), D8 (splayed ends); the tread-width test is tightened (camber distances within a factor 1.3, and the width the photograph implies at the courses' distance, 960 +-40) | none |

Also taken from the reviewer's notes: F1 is putty-glazed (P2 shows a chipped putty line, no planted bead); P1's dark plate on the jamb may be a bell push (recorded in section 11, drawn as photographed); the house numerals' form is now specified (section 4.6).

## 3. Sources

All photographs are references for measuring only: never placed in the game, never traced into a texture, never fed to an image model. No NoAI source is used.

| Id | Source and what it is | URL | Read | Author, licence | Taken | Shows | Used |
|---|---|---|---|---|---|---|---|
| P1 | Photograph, 480 x 640, the full original, preview `door-photo-01-teignmouth-four-panel-red.jpg` | Wikimedia Commons file "Front door, 69 Lower Brimley Road - geograph.org.uk - 3157125.jpg" (Geograph 3157125) | Page read by the lab on 8 Oct 2026; **not reachable from this cloud** (403). I measured the preview JPEG itself. Author, licence and date as the lab recorded them | Robin Stott, CC BY-SA 2.0 | 2012-05-06 | 69 Lower Brimley Road, Teignmouth: red four-panel door with bolection mouldings, lock-rail band, weatherboard, white frame, single-pane transom light, buff arch and quoins in red brick, stone threshold, riser and step, a splayed brick plinth | Yes, every elevation number. 2012, fresh gloss paint, build date not documented |
| P2 | Photograph, preview 675 x 1200 (the lab measured a 619 x 1100 copy of the 1280 x 2275 original), `door-photo-02-tottenham-six-panel-black.jpg` | Wikimedia Commons "Doorway Philip Lane Tottenham London England.jpg" | as P1 | Acabashi, CC BY-SA 4.0 | 2024-02-03 | 178 Philip Lane, Tottenham: an old unrestored black six-panel door of a flat beside a shop, deep moulded transom with a full round nose, centre knob, cylinder lock, plugged keyhole, letter plate, worn timber threshold | Yes, for the transom, ironmongery, mouldings, jamb strip, threshold and wear, and for the flat-door variant. Not for four-panel proportions |
| P3 | Harrogate replacement door (lab's list) | Commons, Storye book, CC BY-SA 4.0 | lab | - | 2024-11-17 | a modern replacement | Not used |
| E | George Ellis, *Modern Practical Joinery* (1902) pp.92, 93, 111, 112 | archive.org india.history.resource.100246 | Page images opened by me: pp.92, 93, 111, 112 (Fig. 355 a segmental brick arch with radiating joints over a solid frame whose sill's horns run into the wall). Other readings are the lab's | public domain by age | 1902 | proportions, grooves, bolection lap, solid frames, sill horns, segmental arch | Yes |
| H | P. N. Hasluck, *Cassell's Carpentry and Joinery* (1907) pp.346, 347, 398 | archive.org cassellscarpentr00hasl | Opened by me | public domain | 1907 | outer door 2 ft 8 in, frame "beaded on the inside", ovolo outside, "weathered transom", "double rebated" | Yes; the ovolo is **not** followed |
| R | J. W. Riley, *A Manual of Carpentry and Joinery* (1905) p.357 Figs. 667-671; pp.353, 355 | archive.org amanualcarpentr01rilegoog | Opened by me: p.357; pp.353, 355 are the lab's readings | public domain | 1905 | 5 x 4 frame, transom 5 x 4, bolection outside, single inside | Yes |
| S | production/research/shopfronts/FRONTAGE-2026-10-06.md and production/art/shopfront-kit/README.md (this repository) | repo | Read by me | studio | 2026-10-06 | door colours of the period, side-door notes, kit sizes; cites First in Architecture (not reached by me) and BS EN 13724 | Colours, the scene's sizes |
| SS | production/cloud-week/targets/SCENE-SLOTS.md | repo | Read | studio | 2026-10-08 | the street's stand-in sizes | The F1 leaf and plate size |

**Dating.** Neither photograph is from 1975-2000 and none could be reached. The objects are late-Victorian types that did not change: a bolection-moulded four-panel door with a weathered transom (the books of 1902-1907 draw the same members), and P2 is an unrestored door whose paint shows decades of wear. Whether P1's door is original or a replica is not documented. Both serve proportions and detail, never colour or condition in 1990.

**Unreached.** The Commons and Geograph file pages, archive.org, the wider web (403). Nothing from them is used beyond the lab's recorded author, licence and date.

## 4. The target, T1: the terrace four-panel front door (P1)

### 4.1 Opening and wall

| Item | Value (mm) | Source, kind |
|---|---|---|
| Opening width, between the brick reveals | 882.0 | Derived: clear between stops 772.0 + 2 x 55 |
| Head: crown z / ends z | 2340.0 / 2322.0 (camber 18), a circle R 5411.25 centre (441, -3071.25) | Photo P1: head top rows 78.0 at the centre, 81.5 at the ends, +-1.5 px (+-8) |
| Reveal depth (frame's outside face behind the wall face) | 114.3 | Read: Hasluck p.346 |
| Frame set in a check behind the brick | 46.6 deep (the jamb's hidden part) | Derived |
| Wall thickness (context) | 342.9 | Judgement: 1 1/2 brick |
| Ground | z -318; glb pivot x 441, y 0, z -318 | Judgement (section 4.7) |

### 4.2 Frame (flat, square)

| Item | Value | Source, kind |
|---|---|---|
| Jamb section | 101.6 across x 127.0 deep, every arris square, eased 1; the face one plane | Read: Riley p.357 "5 x 4 rebated frame"; Photo P1, P2 for the flat edges (D10) |
| Rebate | 22 wide x 53 deep; the stop (outside) 74 deep; leaf opens inwards | Scaled: Hasluck Fig. 1148, Riley Fig. 671 |
| Jamb showing past the brick | 55.0 each side (x 0-55 and 827-882) | Photo P1 (left 10 px, right 11 px, +-10) |
| Head | 101.6 x 127; top edge cut to the soffit's circle; 70.4 shows at the crown, 52.4 at the ends | Photo P1 |
| Frame outside face y / inside face y | 114.3 / 241.3 | Derived |
| Stop's inner edge | square, no bead (F1 has one) | Photo P1 |

### 4.3 Transom (weathered, projecting, nosed) and glazing

Front profile `frame.transom.front_profile_yz_mm` (y from the jamb face plane, outwards negative; z up from the stop underside 1937.6): (0,0) (-12.5,0) (-13.8,1.2) (-14.0,2.6) (-13.4,4.0) (-10.5,6.0) (-8.6,9.0) (-8.0,14.0) (-8.0,40.0) (9.5,65.0), then the shelf at z 65 to the glass slot.

| Item | Value | Source, kind |
|---|---|---|
| Face height | 65.0: lip 0-4, cove 4-14, face 14-40, slope 40-65 | Photo P1 column profile x 140-175: bar rows 143.3-155.5 (12.2 px), bright slope rows 143.5-147.9, face 148-152.9, crease 153-154.9, lip 155 (+-1 px) |
| Face / nose proud of the jamb faces | 8 / 14, bead radius 2.6 | Judgement (+-3) from P2's shadow and P1's lit lip |
| Slope | from (y -8, z 40) to (y 9.5, z 65): 55 degrees | Derived; Read: Hasluck p.398 "weathered" |
| Transom x extent | 45 to 837: the face and the nose's top run 10 past each stop edge; the body runs between the jambs | Photo P2 (the same, 28 there), Judgement |
| Ends | the nose is cut at 45 degrees from the stop edge at z 2 to (stop edge - 10, z 12) | Judgement scaled from P2 (P1 is too small to show it) |
| Stop underside / rebate underside / top | z 1937.6 / 1959.6 / 2002.6 | Derived |
| Glass opening | x 55-827, z 2002.6-2269.6 (772 x 267) | Photo P1 rows 92.5-143.3 |
| Glazing bead | quarter-round, face 10 x 8 proud, mitred, four sides, inside the opening | Photo P1: 2 px bright line at the glass foot, 2 px dark line at the head; profile Judgement |
| Clear glass | x 65-817, z 2012.6-2259.6 (752 x 247); 3 thick at y 133.3 in 6.4 deep, 4 wide slots | Photo P1 clear rows 95.0-142.5 (245 +-10) |

### 4.4 Leaf, panels and mouldings

| Item | Value | Source, kind |
|---|---|---|
| Leaf | 812.8 x 1948.0 x 50.8, x0 34.6, bottom 10 above the threshold, outside face y 188.3 | Read: Hasluck p.347 (2 ft 8 in), Ellis p.93 (2 in); Photo P1 for the height (+-31, D1) |
| Stiles / top rail / lock rail / bottom rail | 114.3 / 127.0 / 228.6 / 192.8 | Read: Ellis p.93, Riley p.357; Photo P1 (bottom rail) |
| Muntin | 120.0 | Photo P1 re-measured, +-10 (D2) |
| Lock rail centre | 787.0 above the leaf bottom | Photo P1 +-12 (D3) |
| Panel openings | 232.1 wide; upper 919.7 high (v 901.3-1821.0), lower 479.9 (v 192.8-672.7); u 114.3-346.4 and 466.4-698.5 | Derived |
| Panel | flat, 16.9 thick centred; grooves 12.7; play 3.2 | Read: Riley p.353; Ellis p.92 |
| Bolection (outside) | 36 on the face, 4.8 lap, 7.0 proud, panel face 16.95 below the framing; profile (d, h): (0,0) (0,3.5) (1.4,5.8) (3.5,6.9) (5.5,7.0) (7.5,6.4) (10.5,4.6) (14.5,1.0) (19,-4.5) (24,-10.5) (29,-14.5) (33,-16.3) (36,-16.95), closed by (4.8,-16.95) (4.8,0) | Scaled: Riley Fig. 671 (36 +-5), Read: Ellis p.92 (lap 3/16 in); Photo P1 34 +-8; profile shape Photo P1 and P2, Judgement |
| Single (inside) moulding | 22 wide, planted | Scaled: Riley Fig. 671 |

### 4.5 Lock-rail band and weatherboard (T1 only)

| Item | Value | Source, kind |
|---|---|---|
| Band z above the leaf bottom | 785.0 to 857.5 (72.5 high), x 57.0 to 825.0 (2 mm short of each stop face) | Photo P1 column x 145-175: top edge row 363.5, underside row 377.5 (+-1 px) |
| Band projection / profile (z, p) | 22 max; (0,0) (0,17) (1.5,19.5) (4,20.5) (9,20.5) (14,19.5) (18,18) (22,15) (25,13) (28,14) (31,17.5) (34,20) (37,21) (40,20) (42,17) (45,16) (49,14.5) (52,15.5) (55,18.5) (58,20.5) (62,22) (66,21) (69.5,17) (71.5,10) (72.5,0) | Photo P1: highlights at rows 365.5, 371 and 374, dark creases 367.5 and 372.5, shadow rows 378-382; projection Judgement (+-6) |
| Weatherboard | z 0 to 80 above the leaf bottom, x 57.0-825.0; 26 max proud; (0,0) (0,12) (2,18) (6,22) (14,25) (26,26) (40,25.5) (50,23) (54,19) (57,17.5) (60,18.5) (63,22) (67,25.5) (72,25) (76,21) (78.5,13) (80,0) | Photo P1 rows 513.7-529.7 (16 px = 82 +-8); highlight rows 514-517, hollow 518-519, face 520-527, edge 528-529; projection Judgement (+-6) |

### 4.6 Ironmongery (brass or dark steel, no maker's mark)

| Item | Value | Source, kind |
|---|---|---|
| Letter plate | vertical on the muntin; outer 76 x 242, backplate 3, rim 13.5 wide raised 6 with a 45 degree outer chamfer; aperture 48 x 190, 22 below the plate's top; a sprung flap hinged along its top, 2 mm gap, dished 3; centre 1617 above the leaf bottom, on the leaf's centre line | Photo P1 16x crop: x 186.25-200.9, rows 192.5-239.4 (+-1.5 px); aperture rows 196.9-233.75; relief Judgement |
| House number (optional) | two stacked digits 39 x 72, stroke 7, relief 3, gap 22, v 1207-1277.6 and 1300-1373, on the muntin; plain upright sans-serif numerals with open round curves and no serifs (no real typeface); the number is the town's | Photo P1 rows 263.4-295.6 |
| Cylinder lock | flush; collar 43.5, plug 28, collar proud 1.5, vertical keyway 3 x 9; centre u 745.8 (46.6 from the stop face), v 1235 | Photo P1 16x crop: centre (258.75, 290.3), 8.4 px (+-1 px) |
| Keep | on the right jamb's stop face: 22 x 72.6, 3 proud, centre x 859.4, z 1120.3-1192.9; dark steel box keep with a slot (it may be a bell push; drawn as photographed) | Photo P1 16x crop rows 300.3-314.4 |
| Knob, knocker, chain | none | Photo P1 |
| Hinges | none show; inside, three 100 mm steel butts on the left stile (optional) | Photo P1, P2; Judgement |

### 4.7 Setting: threshold, riser, step, plinth, arch, quoins

| Item | Value | Source, kind |
|---|---|---|
| Threshold stone | 76 thick, top z 0, front flush with the wall face (y 0), back y 241.3, rounded nose r 18 overhanging the riser by 18, length 1106 (882 + 112 bearing into the brick each side) | Photo P1 rows 534-547.5 (13.5 px = 70 +-10); Ellis p.111-112 (sill horns run into the wall) |
| Riser | z -148 to -76, face at y +18 (recessed) | Photo P1 rows 548-561.5 (14 px = 72 +-10) |
| Step tread | top z -148 (+-25), falling 6.6 to the front; 960 wide (x -39 to 921, +-60); front at y -312 (+-80); a full half-round nose, radius 45 (+-15): the arc runs from the top to 236 degrees, then the base face stands 20 (+-10) behind the front-most point down to the ground in shadow; plan corners r 40; the tread's plan steps back to y -60 beside the plinth for x -39 to 0 and 882 to 921 | Photo P1 (c1_tread 6x; column x 215-245): flat top lit rows 562-580, lit crest 581-585, turning under to 592, dark undercut 593-599 (L 41-62), base face in shade 600-610; x 87-291 px (204 px, perspective). Camera 5.8 m away from the tread's 204 px, 5.7 m from the courses (self-check) |
| Ground | z -318 (the base below the nose, 81 high, shows 70+ mm on P1) | Judgement (+-40) |
| Plinth (each side of the opening and step; 300 of it drawn) | red brick (159,113,85, darker with damp), front 60 (+-20) proud of the wall face; the top course is splayed: 45 degrees from (y -60, z -48) to (y 0, z 12), bricks 65 wide at a 75 pitch, the course 77; the face below is vertical to the ground in 77 courses (lines at -65, -142, -219, -296); its top, z 12, runs level through the reveal (y 0 to 114.3) to the frame's front face on both sides, the splay stopping square against the jamb's foot; nothing of it in the clear opening | Photo P1 rows 527-600 (c1_plinthR 5x): splay band 13 px, 14 px pitch, vertical face 11 px, plain courses below; "dog-tooth" (the lab's word) is wrong: the heads are splayed. Projection Judgement |
| Arch ring | 13 buff bricks on end, 207 deep, joint 8 (dark, recessed 4); soffit the circle above; joints radial to its centre; extrados concentric: z 2547 at the crown, 2527.9 at the corners (x -22 and 904); the soffit ends at x -4.9 and 886.9 (z 2321.6); pitch along the soffit 68.7; the end bricks rest on the top quoin block (short, 122 wide) with their corners 22 past each reveal; the soffit between ring and frame head is the same buff brick ends in deep shadow | Photo P1 (c1_arch2 6x): 13 bricks (joints at x 119, 132, 146, 160, 173, 187, 200, 213, 227, 241, 255, 268), 13.7 px a brick; extrados rows 28.1-28.7 at the crown and 32.4-32.9 at the ends, soffit 69-70 and 73-74; the mortar course above is straight (not lens bow); Ellis p.112 Fig. 355 |
| Quoins | buff blocks of three courses (231 = 3 x 77), long (237 from the reveal) and short (122) alternating, bottom long (z 12-243) and top short (z 2091-2322), 10 blocks, both reveals in step; course joints 10; the reveal's return faces are the same buff | Photo P1 right reveal rows 73-528 and the left; see section 2 fault 1 |
| Joints | wall and quoins pale grey-cream, 10 wide, struck 2 back; arch and soffit dark brown-grey, recessed 4 | Judgement (lines too thin to sample on P1) |

## 5. The target, F1: the side door to a flat over a shop (0.838 x 1.981, P2)

F1 is the same door at the street's size with P2's transom, furniture and threshold. Full numbers are `variants.flat_door_over_shop.parts` in target.json (the same keys as T1).

| Item | Value | Source, kind |
|---|---|---|
| Leaf | 838.0 x 1981.0 x 50.8; x0 28.6; z0 10; members as T1 with the extra 25 mm of width in the panels (opening 244.7 wide) and the extra 33 mm of height in the upper panels (952.7 high) | SS (spec); Derived |
| Jambs | 49.0 showing each side (jamb x left [-52.6, 49.0], right [846.2, 947.8]; the frame is 1000.4 wide, 895.2 showing); a 5 x 2.5 quarter-round on each stop's inner edge | Photo P2 rows 300-900 (left strip x 142-163, right 508-530: 21 px x 2.317 = 49), then a groove and the pilaster |
| Opening | 895.2 wide (797.2 clear between stops); the shop bay's 944 (the research's own sum for 50 mm jambs) leaves 24.4 a side to the shopfront's pilaster return | Derived; D20 |
| Head | flat, top at z 2400.0 (the shop's transom line, SS); glass opening x 49.0-846.2, z 2072.6-2339.6 (797.2 x 267); clear glass x 59.0-836.2, z 2082.6-2329.6; head shows 60.4 | Derived |
| Glazing | putty fillet, 10 across x 8 proud, a straight bevel, all four sides | Photo P2: a chipped putty line at the glass foot, no planted bead |
| Transom | 102 high; profile (y, z) (0,0) (-12,0) (-16,1.5) (-19.5,4.5) (-21.5,9) (-22,14) (-21.5,19) (-19.5,24) (-16,28.5) (-12,31.5) (-9,33) (-7,34.5) (-10,36) (-10,70) (9.5,102): one full round 33 high, 22 proud at z 14, a 3 mm quirk at z 33-36, the flat face to z 70, the weathered slope to 102 at 58.6 degrees; x 21.0-874.2 (the face and nose top run 28 past each stop edge); the nose is cut on a 45 degree splay from (stop edge + 28, z 32) to (stop edge, z 4); nose underside ends at the stop edge | Photo P2 (column x 250-400: slope rows 76-90, face 91-104, quirk 105-107, round 108-121; ends c2_endL, c2_endR at 12x: overrun 12 px = 28 mm, splay rows 106-117); Riley "Transome 5 x 4" (101.6); projection 22 +-8 Judgement |
| Mouldings | bolection 42 on the face; no band, no weatherboard | Photo P2 (18.5 px = 43 mm) |
| Letter plate | as T1 (vertical on the muntin, 76 x 242, centre 1617 above the leaf bottom, on the leaf's centre), with four 4 mm slotted screws at the rim's corners | P1 for size and place, P2 for the screws; D15 |
| Centre knob | turned, 69 across, 62 proud of a 76 dished rose sunk 3, at the lock rail's centre (v 787), five turned rings (profile in json), 4 mm brass cap | Photo P2 8x crop; Read: Ellis p.93 (handle in the middle of the rail) |
| Cylinder lock | knurled collar 37, plug 18, 12 serrations, centre 46.3 from the stop face, v 1040 | Photo P2 5x crop |
| Plugged keyhole | 23 x 32 dark recess, 34.8 from the stop face, v 1151 | Photo P2 |
| Keep | on the right jamb's stop face, centre x 878.6, z 925.7-998.3 | Judgement |
| Threshold | painted softwood, 70 thick, rounded front r 8, top at z 0, the paving at z -45: 45 of its front face shows, the sill bedded 25; no step; glb pivot x 447.6, z -45 | Photo P2 (x 300-400): top rows 946-959, front face rows 960-979 (19.5 px x 2.317 = 45), concrete from row 981 |
| Arch, quoins, riser, step, plinth | none (the shopfront owns the head; the pilaster's return is painted render, cracked, 222,225,229) | - |

**Against SCENE-SLOTS (photographs win, the differences written down).**

| Scene stand-in | Against the photographs | Choice |
|---|---|---|
| Leaf 0.838 x 1.981 | visible proportion 2.46 lies inside P1's 2.47-2.50 (+-0.04) and 3% above P2's 2.39 (a squatter six-panel door) | kept |
| Letter plate 0.25 x 0.04 at 1.0 | P1's plate is 0.242 long x 0.076 wide with a 0.19 x 0.048 aperture, centre 1.617 above the leaf bottom; P2's horizontal plate is 0.195 x 0.070 at 1.50; the shopfront research's BS EN 13724 range 0.7-1.7 m (post-1990) contains both | size kept as the long side, height 1.617 (1.627 above the threshold), vertical on the muntin |
| Overall 0.944 wide (kit) | the 944 is the research's own sum ("with 50 mm jambs and 3 mm gaps"); P2's jamb strip is 49 | not kept: the frame shows 895.2; the bay's 944 stays the bay, the 24.4 a side is the pilaster's return |
| Transom at 2.40 | consistent with F1's head at 2.40 | kept; the shopfront's own spandrel above is not this target's |

## 6. Variants, colours, materials

**Kinds.** T1 (terrace four-panel, brick opening, plinth, step) and F1 (flat over shop). An option, `option_six_panel`, gives P2's six-panel layout as fractions of the visible leaf for variety (not requested). Counts are the scene's.

**Door colours** (sRGB, gloss; roughness 0.35 new, 0.55 for 1990 weathered, 0.65 on the weather side low down; metal 0):

| id | Name | sRGB | Weight | Source |
|---|---|---|---|---|
| black | gloss black, faintly blue | 35, 36, 40 | 0.25 | Photo P2 median (39,40,45) |
| dark_green | dark green | 28, 59, 41 | 0.20 | shopfront research and kit (0.11,0.23,0.16) |
| maroon | maroon / oxblood | 92, 26, 32 | 0.15 | research names it; value Judgement |
| navy | dark blue | 24, 38, 78 | 0.15 | research names it; value Judgement |
| brown | dark brown | 74, 48, 34 | 0.15 | research names it; value Judgement |
| red | bright red | 201, 41, 32 (x 0.85 and chalked for 1990) | 0.10 | Photo P1 median; 2012 fresh paint |

F1 uses the same list without red (weights renormalised). **Frame:** gloss white, yellowed, sRGB 226, 224, 214 (P1 240,239,245 fresh; P2 222,225,229 old) weight 0.7; cream 222, 212, 184 weight 0.3 (Judgement). **Other surfaces:** brass sRGB 181, 150, 85, metal 1.0, roughness 0.4 (0.25 on worn edges); nickel or chrome 170, 170, 168, metal 1.0, roughness 0.35; dark steel 40, 40, 42, metal 1.0, roughness 0.6; glass roughness 0.05, IOR 1.5; step stone 156, 153, 149 roughness 0.85 (the threshold's front stained 142,127,111); arch bricks buff 219, 209, 190 roughness 0.9; quoins buff 200, 186, 158; red wall and plinth 159, 113, 85; F1 threshold 81, 72, 65 roughness 0.7.

## 7. Edges, joints, fixings, drips and ground

Written in full in target.json `edges`, `joints_and_seams`, `fixings` and `drips_and_throats`. In short:

- **Edges.** Frame square (eased 1), no ovolo, no tube. Leaf square (eased 1.5). Bolection: rounded nose 3.5, crease at the foot. Band: square underside, crests and coves, rounded top. Weatherboard: flat underside, belly, hollow, rounded nose. Transom: T1 lip bead r 2.6; F1 a full round with a 3 mm quirk; both with 45 degree splayed ends. Threshold nose r 18; tread a half-round r 45 with an undercut, plan corners r 40. Bead: quadrant 10 x 8 (F1 a putty bevel). Plate rim chamfered 45 degrees. Plinth: 45 degree splay on bricks 65 wide at a 75 pitch.
- **Joints.** Rail/stile hairlines 0.4 wide; mitres closed; 1.6 mm shadow gap round the leaf, 10 under it; band and weatherboard 2 short of the stops; 3 mm joint frame to brick.
- **Fixings.** Moulding screws hidden; plate screws only on F1 (four, 4 mm); no hinges, bolts, straps or knockers outside.
- **Drips and throats.** The weatherboard and its hollow, the transom's slope and nose, the threshold's 18 mm overhang, the tread's undercut.
- **Ground.** T1: the step on the pavement, the threshold 318 above it; F1: a timber threshold 45 above the paving.

## 8. Wear as the photographs show it (1990 rule)

P1: a fresh gloss coat with brush marks running with the grain, grime on the band's and weatherboard's top nosings and in the dark crease under the band, a brown-gold stained threshold and a pale worn step nosing, a dirty frame foot, a damp-darkened plinth. P2: crazed paint over the whole leaf in 2-4 mm cells, bare pale patches and chips on the lower right panel's moulding and on the bottom rail, dirt packed in the moulding angles, a wet-grimed flaking bottom rail, peeling frame paint down to a darker undercoat, plugged holes, a worn bare threshold. **For the kit:** unrestored, not heritage-fresh; crazing and chips on arrises and the mouldings' lower lips; paint 15% duller; grime in angles and on upward faces; darker and flaking low down; brass dull with bright touched edges. Cables, junction boxes, stickers, tape, railings and the wall lantern in the photographs are not part of the kit.

## 9. The element-by-element reading of the photographs

| Element | P1 | P2 | In the target |
|---|---|---|---|
| Frame face and edges | flat white, 55 mm showing, crisp | a flat strip 49 mm (21 px), a groove, the pilaster; a light line at the stop edge | `frame.*`; T1 55, F1 49 and a stop bead; square, eased 1 |
| Frame feet | hidden by the plinth | on the timber threshold | square, alike; the plinth's top 12 meets the jamb's foot |
| Frame head | cambered with the arch | out of frame | circle R 5411.25; T1 only |
| Transom | bar 12.2 px: slope, face, crease, lip | slope 31%, face 29%, quirk, full round nose 36%, ends splayed 45 degrees, face 28 mm past the stops | T1 and F1 profiles, end splay |
| Glass | single pane, bead lines | dirty glass, putty line | bead (T1), putty (F1); clear glass 752 x 247 / 777.2 x 247 |
| Glass interior | a faint pale vertical strip 57 mm wide at x 197-208 px | reflections | an interior reflection, not a bar: **not modelled** |
| Leaf, panels, mouldings | stile 114.3 ... muntin 120; bolection | six panels, bold bevel | `leaf`, `panels`, `mouldings` |
| Band, weatherboard | moulded, crisp shadow | none | T1 only |
| Letter plate, number | vertical 76 x 242, "69" stacked | horizontal 195 x 70 at 1.50, "178" in a row | T1/F1 vertical; horizontal as an option; numbers optional |
| Lock, keep, knob, keyhole | cylinder 43.5 at v 1235, keep v 1147 | cylinder 37 at v 1040, centre knob at the lock rail, plugged keyhole | `ironmongery.*` |
| Threshold, riser, step | stone threshold, riser, full-round tread nose over an undercut | worn timber sill 45 above the paving | T1 `step`; F1 threshold |
| Plinth | splayed top course, projecting, damp-dark | none | T1 `brick.plinth` |
| Head over the frame | 13-brick segmental ring, curved extrados | out of frame | T1 `brick.arch` |
| Reveal dressings | buff blocks of three courses, long and short, both sides in step | cracked pilaster render | T1 `brick.quoins`; F1 the shopfront's |
| Hinges, knocker, bell, chain | none | none | none outside |
| Excluded | lantern, railings, cable | cables, box, stickers, shutter | listed so nobody builds them |

## 10. The checks the builder's automatic check must pass

`target.json` `checks` lists 80, each with a name, what to measure, the expected value and the tolerance, and where it comes from. Groups: **A** the lab's pass rule (front view layer by layer, every section: IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm) plus **A4** profiles; **B** dimensions (B13 49 for F1, B17 the crown 2340 and the frame widths 975.2 / 1000.4); **C** frame edges; **D** transom (projection T1 8/14 and F1 10/22, slope, the lip or the full round, the overrun 10 / 28, splayed ends D8); **E** and **W** band and weatherboard; **F** ironmongery; **G** step, threshold (G4 nose r 45 over a 20 undercut, G6 45 above the paving), arch (G7, G9, G11 exactly 13 bricks with radial joints and a curved extrados, G12 against P1), setting (G10 per variant); **Q1-Q3** the quoins (blocks every three courses, widths, buff returns); **L1-L5** the plinth (front 60, 45 degree splay, returns into the reveal, the tread butts, the jamb feet); **H** the built elevation on P1 within 2.5 px; **I** surfaces (I5 per variant: 975.2 and 1000.4).

## 11. Self-check result

`python self_check.py` (reads target.json and the drawing's polygons, writes `self_check` into target.json): **303 of 304 checks pass; the one miss is reported, not hidden** (group 4: the visible height-to-width of P2's six-panel door is 2.39, F1's 0.838 x 1.981 shows 2.46: P2's door is 3% squatter than the street's size; kept, the scene's size being no photograph's contradiction beyond its error). Groups: 1 printed (18), 2 photographs win (D1-D7, D10-D17: 15), 3 P1 (53 edge, quoin, arch, plinth and perspective tests and 8 fractions), 4 P2 against F1 (17), 5 consistency by numbers and by shapely on the drawings (111: no overlaps, nothing floating, the 1.6 mm leaf gaps, the 2 mm band gaps, the quoin rhythm, the arch's 13 radial bricks and concentric rings, the plinth, the F1 coordinates that follow the 49 mm jamb), 6 the builder's checks evaluated on the drawing (82).

**How to read it honestly.** The tests that are independent of the numbers drawn from them are the panel mouldings, transom, glass, head, brick edges, the quoin boundaries (nine rows on a fitted 231 mm pitch, worst 3.0 px), the arch's extrados and soffit rows (within 2.5 px on the wall-plane mapping fitted on the quoins), the arch's width ratio, the brick pitch and the tread width at a consistent camera distance. The band, weatherboard, plate, lock, keep and numerals were fitted to the same photograph, so their near-zero differences are by construction. The leaf's height depends on the scale (P1's left edge leans 2.6 px in 210 rows): the vertical scale carries +-1%.

## 12. Could not settle

1. **Dated photographs.** None from 1975-2000 reachable; P1 2012 (original or replica not documented), P2 2024. The 1990 colours are the shopfront research's names with judged values.
2. **Mouldings' width and the band's and weatherboard's sections.** At 480 px the bolection reads 34 +-8 (the lab's 36 kept), and the band and weatherboard are drawn to reproduce their highlights and shadows, not measured outlines. The projections (band 22, weatherboard 26, transom 14 and 22) come from shadow lengths: +-6.
3. **The step, plinth and ground.** The step's depth (312), the plinth's projection (60 +-20) and the ground (-318, +-40) are perspective judgements; the quoins' lowest 20 mm, where the splay hides the wall's foot, are a 3 px question.
4. **The leaf's height,** 1948 (1926 if the scale is fitted on the mid-door width): 1%.
5. **T1's transom ends** (a 10 mm overrun with P2's 45 degree splay is specified; P1 is too small to show it) and the arch ring's depth (207 on the photograph, a brick on end being 215).
6. **F1's fanlight height.** The kit's side door rises to 2.85 with a fielded panel above; P2 is cropped at the glass. F1's head is at 2.40 (the shop transom line); anything above it is the shopfront's.
7. **Hinges and an actual Hook door's colour in 1990:** hinges are inside; the colours judged. P1's dark jamb plate may be a bell push, not a keep.

## 13. Credits for the previews in `production/previews/cloud-week/refs/front-door/`

| File | Credit |
|---|---|
| door-photo-01-teignmouth-four-panel-red.jpg | Robin Stott, CC BY-SA 2.0, Geograph 3157125 via Wikimedia Commons, taken 2012-05-06 (reduced; for measuring only) |
| door-photo-02-tottenham-six-panel-black.jpg | Acabashi, CC BY-SA 4.0, Wikimedia Commons, taken 2024-02-03 (reduced; for measuring only) |
| ellis-1902-p089 to p093, p111, p112; hasluck-1907-p346, p347, p398; riley-1905-p353, p355, p357 (and the crops) | public domain by age (1902, 1907, 1905), archive.org page images, as the lab saved them |
| door-photo-01-teignmouth-target-on-photo.jpg | the target's drawing (own work) laid on Robin Stott's photograph (CC BY-SA 2.0); 900 x 1200, about 205 KB; the quoin blocks, the 13-brick arch and the plinth are drawn at the door plane's scale, and the stone step, being nearer the camera, reads wider |
| door-target-on-photo-2026-10-08.jpg, door-v2-*, door-v3-* | the lab's overlay and renders, kept for comparison |
