Front door (four-panel, in frame, with transom, brick head and step), amended 8 October 2026: the lab's proportions kept, every detail the two photographs show written down with a number or a profile; flat, square-edged frame, weathered projecting transom with a moulded nose, moulded lock-rail band and weatherboard, the ironmongery measured, a deep rounded-nosing stone step, a cambered buff-brick arch bearing on the brick; two variants (terrace T1, flat-over-shop F1) and six paint colours; self-check 230 of 231 pass, the one miss reported (P2's door is squatter than 0.838 x 1.981).

# Four-panel front door: amended target (cloud week 42)

Files in this folder: `TARGET.md` (this), `target.json` (the same numbers, profiles, variants, checks and the self-check result), `target_drawing.py` (draws target.json alone), `self_check.py`, `lab-start/` (the lab's files, untouched). Run: `python target_drawing.py OUT_DIR [--overlay PHOTO OUT.jpg]` and `python self_check.py` with `/home/user/.bpyenv/bin/python`. The reviewers' picture of the drawing on photograph 1 is `production/previews/cloud-week/refs/front-door/door-photo-01-teignmouth-target-on-photo.jpg`.

Axes (as the lab's): x across the opening left to right seen from outside, 0 at the left brick reveal; y into the wall, outside at -y, 0 at the wall's outside face; z up, 0 at the top of the threshold stone. Millimetres. Kinds: **Read** printed on a page; **Scaled** measured off a printed drawing against its own printed figure; **Photo** measured on a photograph (method and error given); **Derived** worked from other numbers; **Judgement** nothing else fits.

## 1. What changed from the lab's target (and why)

The lab's door passed every automatic check and failed two fresh reviews, because its target followed books against its own photographs and left out whole classes of detail. Changes, in the order of the reviews' faults:

| # | Lab's target | Amended target | Photograph says | Decision |
|---|---|---|---|---|
| 1 | Frame with a 19 mm ovolo on the outer arris, running down the jambs only: the jambs read as tubes | Flat, square-edged frame: every arris square (eased 1 mm), no ovolo, no round on jambs, head or transom; F1 adds a 5 x 2.5 quarter-round on each jamb's stop edge | P1 and P2 both show a flat face with crisp edges | D10 |
| 2 | Transom 65 mm, flush with the jambs, plain | Weathered transom: lip bead, cove, flat face, sloped top; T1 proud 8 (face) and 14 (nose) of the jamb faces, F1 10 and 22; ends overlap the jamb faces 10 / 16 mm; F1 102 high | P2 deep projecting transom with a sloped moulded nosing, P1 the same, lighter; Hasluck p.398 "weathered transom" | D11 |
| 3 | Band: a 79.5 x 19 box; weatherboard: a 72 x 30 wedge; both ran to the jambs | Band 72.5 high, 22 proud, a drawn profile of lip, cove, bead, groove and rounded nosing with a square underside; weatherboard 80 high, 26 proud, belly, hollow and rounded nose; both stop 2 mm short of the stops | P1 rows 363.5-377.5 and 513.7-529.7, highlights and shadows traced | D13 |
| 4 | No ironmongery | Letter plate (framed, flap), cylinder lock set 46.6 in, keep on the jamb, optional house number; F1 adds the turned centre knob, the knurled cylinder and the plugged keyhole; every size and place measured | P1 and P2 | D15, D16 |
| 5 | A thin 76 mm stone sill, flush with the opening | Threshold 76 with an 18 mm rounded nose, a recessed 72 mm riser, a deep step (960 wide, 312 proud, 30 mm bullnose, 40 mm plan corners); sill and step run past the opening into the brick | P1 rows 534-592 | D12 |
| 6 | Glass with no bead | Planted quarter-round bead 10 x 8 on all four sides; clear glass 752 x 247 inside the 772 x 267 opening | P1 glass foot and head lines | D7 |
| 7 | Muntin 132.2 (16%) | Muntin 120.0 (14.8% of the leaf; the visible gap between the mouldings 110.4 = 14.3% of the visible width) | P1 re-measured: gap 21.5 +-2 px, the review's 14% | D2 |
| 8 | Brick head flat; lintel flush with the opening | Cambered 18 mm (crown 2340, ends 2322); a 12-brick buff soldier ring 215 deep, ends 22 mm past each reveal and resting on the 112 mm quoin course; buff quoins both sides | P1 head rows 78 and 81.5; ring x 104.5-283.75; Ellis p.112 Fig. 355 | D17 |
| 9 | Left jamb foot had an odd step; hatching on the stonework | Feet square and alike (check C3, C4); nothing coplanar (check I1) | Review 2 faults 2 and 6 | checks |
| 10 | One door | Two variants and six colours (section 6) | the scene and the shopfront research | - |

## 2. Sources

All photographs are references for measuring only: never placed in the game, never traced into a texture, never fed to an image model. No NoAI source is used.

| Id | Source and what it is | URL | Read | Author, licence | Taken | Shows | Used |
|---|---|---|---|---|---|---|---|
| P1 | Photograph, 480 x 640, the full original, preview `door-photo-01-teignmouth-four-panel-red.jpg` | Wikimedia Commons file "Front door, 69 Lower Brimley Road - geograph.org.uk - 3157125.jpg" (Geograph 3157125) | Page read by the lab on 8 Oct 2026; **not reachable from this cloud** (403). I measured the preview JPEG itself. Author, licence and date as the lab recorded them | Robin Stott, CC BY-SA 2.0 | 2012-05-06 | 69 Lower Brimley Road, Teignmouth: red four-panel door with bolection mouldings, lock-rail band, weatherboard, white frame, single-pane transom light, buff-brick arch and quoins in red brick, stone threshold, riser and step | Yes, every elevation number. 2012, fresh gloss paint, build date not documented: it shows a late-Victorian type, "unchanged" cannot be proved |
| P2 | Photograph, preview 675 x 1200 (the lab measured a 619 x 1100 copy of the 1280 x 2275 original), `door-photo-02-tottenham-six-panel-black.jpg` | Wikimedia Commons "Doorway Philip Lane Tottenham London England.jpg" | as P1 | Acabashi, CC BY-SA 4.0 | 2024-02-03 | 178 Philip Lane, Tottenham: an old unrestored black six-panel door of a flat beside a shop, with a deep moulded transom, centre knob, cylinder lock, plugged keyhole, letter plate, worn timber threshold | Yes, for the transom, ironmongery, mouldings, threshold and wear, and for the flat-door variant. Not for four-panel proportions |
| P3 | Harrogate replacement door (lab's list) | Commons, Storye book, CC BY-SA 4.0 | lab | - | 2024-11-17 | a modern replacement | Not used |
| E | George Ellis, *Modern Practical Joinery* (1902) pp.92, 93, 111, 112; pages 89-91 and 93 crop in the folder | archive.org india.history.resource.100246 | Page images opened by me: pp.92, 93, 111, 112. Other readings are the lab's | public domain by age | 1902 | proportions, grooves, bolection lap, solid frames, sill horns, segmental arch | Yes |
| H | P. N. Hasluck, *Cassell's Carpentry and Joinery* (1907) pp.346, 347, 398 | archive.org cassellscarpentr00hasl | Opened by me: pp.346, 347, 398 | public domain | 1907 | outer door 2 ft 8 in, frame "beaded on the inside", ovolo outside, "weathered transom", "double rebated" | Yes; the ovolo is **not** followed |
| R | J. W. Riley, *A Manual of Carpentry and Joinery* (1905) p.357 Figs. 667-671; pp.353, 355 | archive.org amanualcarpentr01rilegoog | Opened by me: p.357; pp.353, 355 are the lab's readings | public domain | 1905 | 5 x 4 frame, transom 5 x 4, bolection outside, single inside | Yes |
| S | production/research/shopfronts/FRONTAGE-2026-10-06.md and production/art/shopfront-kit/README.md (this repository) | repo | Read by me | studio | 2026-10-06 | door colours of the period, side-door notes, kit sizes; cites First in Architecture (not reached by me) and BS EN 13724 | Colours, the scene's sizes |
| SS | production/cloud-week/targets/SCENE-SLOTS.md | repo | Read | studio | 2026-10-08 | the street's stand-in sizes | The F1 leaf, bay and plate size |

**Dating.** Neither photograph is from 1975-2000 and none could be reached. The objects are late-Victorian types that did not change: a bolection-moulded four-panel door with a weathered transom (the books of 1902-1907 draw the same members), and P2 is an unrestored door whose paint shows decades of wear. Whether P1's door is original or a replica is not documented. Both are acceptable only for proportions and detail, never for colour or condition in 1990.

**Unreached.** The Commons and Geograph file pages, archive.org, the wider web (403). Nothing from them is used beyond the lab's recorded author, licence and date.

## 3. The element-by-element reading of the photographs

This is the table the lab lacked. For every element of both photographs: where it is in the target and what number or profile it carries. "T1/F1" are the two variants; `json:` gives the path in target.json.

| Element | P1 (four-panel, red) | P2 (six-panel, black) | In the target |
|---|---|---|---|
| Overall form | Frame in a brick opening, leaf set back, fanlight above, step below | Doorway in a pilaster, leaf set back, transom light above, sill below | T1 and F1; sections 4 and 5 |
| Frame face | flat white, 55 mm showing past the brick | a flat strip about 49 mm (21 px) and a groove | `frame.jamb_*`, T1 55, F1 73.4 (bay 944; could-not-settle 1) |
| Frame arrises | crisp, square | crisp, square, a light line at the stop edge | square, eased 1; F1 stop bead 5 x 2.5; `edges` |
| Frame feet | hidden by the brick plinth | stand on the timber threshold | square, alike; C3, C4 |
| Frame head | cambered with the arch, 52-70 mm showing | out of frame | `opening.camber_rise_mm` 18; T1 only |
| Transom bar | 12.2 px = 63 mm: bright slope 25, face 25, crease 10, lip 4 | 46 px: slope 30%, face 33%, moulded nose 35%, nose throws a shadow | `frame.transom`, zones and profile, T1 65 / F1 102 |
| Transom projection | a light shadow line under the lip (rows 156-157) | the nose projects over the door head and the jamb stops | T1 14, F1 22 (Judgement); ends overlap the jambs 10 / 16 |
| Glass | single pane 764 wide, clear 245 high, thin pale line at the foot (the bead), dark line at the head | dirty clear glass, a putty line at the foot | `frame.glazing`: bead 10 x 8, clear glass 752 x 247 (F1 777.2 x 247) |
| Glass interior | a faint pale vertical strip 57 mm wide at x 197-208 px | reflections | an interior reflection, not a bar: **not modelled** |
| Leaf edges, gaps | a thin lit line at the stop, a dark line at the head | dark gaps | 1.6 mm gap, 1.5 mm ease; bottom gap 10 |
| Stiles, rails, muntin | stile 114.3, top 127, lock 228.6, bottom 192.8, muntin 120 | stile 35 px (10%), muntin 13%, lock rail 86 px | `leaf`; muntin revised to 120 |
| Panels | four, upper twice the lower; flat fields | six | `panels`; F1 four (option_six_panel in `variants`) |
| Panel mouldings | lit nose, crease, ogee and a fillet to the field; mitred; 34-54 px wide measures | bold bevel falling to the field, large lit lower lip, deep shadow under the top member | `mouldings.outside_bolection.profile_dh_mm`, width 36 (F1 42) |
| Lock-rail band | a moulded band, crisp shadow beneath | none | `lock_rail_band` profile (T1 only) |
| Weatherboard | rounded lit nose over a hollow, belly, edge | none | `weatherboard` profile (T1 only) |
| Letter plate | vertical, framed, flap, on the muntin, centre 1617 above the leaf bottom | horizontal 195 x 70 plate with a lifting bar, at 1.50 m, four screws | T1/F1 vertical plate; horizontal as `option_six_panel`; D15 |
| House number | brass "69" stacked, 39 x 72 each | "178" in a row on the top rail | optional, town-assigned |
| Lock | flush cylinder 43.5, centre 46.6 from the stop face, v 1235; keep on the jamb v 1147 | knurled cylinder 37, 46 from the edge, v 1040; plugged keyhole 110 above | `ironmongery.*` |
| Knob | none | turned centre knob, rings, 69 across, at the lock rail's centre, in a dark round rose | F1 `ironmongery.knob` (profile) |
| Knocker, bell, chain, hinges | none | none visible | `hinges`: inside only; none outside (check F10) |
| Threshold | stone, rounded nose, 13.5 px = 70 | worn painted timber sill 70 high, rounded front | T1 76 with nose r 18; F1 70 with r 8 |
| Riser and step | recessed riser 72, deep tread with a rounded nosing, wider than the opening, rounded plan corners | none: the sill meets the cracked paving | T1 `step`; F1 none |
| Head over the frame | buff soldier ring of 11-12 bricks on a cambered soffit | out of frame | T1 `brick.arch` |
| Reveal dressings | buff quoins, long and short, 30 courses | pilaster return, cracked render | T1 `brick.quoins` (wall detail); F1 the shopfront's |
| Paint | fresh gloss red (201,41,32), white frame (240,239,245) | crazed black (39,40,45), flaking white (222,225,229) | `door_colours`, `frame_colours`, `wear` |
| Wear | grime on nosings, stained step, dirty frame foot | crazing, bare patches on the bottom rail and the lower right panel, dirt in mouldings, peeling frame, plugged holes | `wear`, 1990 rule |
| Not part of the kit | wall lantern, railings, cable, plinth dog-tooth course | cables, junction box, stickers, shutter | excluded (listed so nobody builds them) |

## 4. The target, T1: the terrace four-panel front door (P1)

### 4.1 Opening and wall

| Item | Value (mm) | Source, kind |
|---|---|---|
| Opening width, between the brick reveals | 882.0 | Derived: clear between stops 772.0 + 2 x 55 |
| Head: crown z / ends z | 2340.0 / 2322.0 (camber 18) | Photo P1: head top rows 78.0 at the centre, 81.5 at the ends, +-1.5 px (+-8) |
| Reveal depth (frame's outside face behind the wall face) | 114.3 | Read: Hasluck p.346 |
| Frame set in a check behind the brick | 46.6 deep (the jamb's hidden part) | Derived |
| Wall thickness (context) | 342.9 | Judgement: 1 1/2 brick |
| Glb pivot | x 441, y 0, z -258 (the base's centre on the ground) | target.json `glb_pivot` |

### 4.2 Frame (flat, square)

| Item | Value | Source, kind |
|---|---|---|
| Jamb section | 101.6 across x 127.0 deep, every arris square, eased 1; the face one plane | Read: Riley p.357 "5 x 4 rebated frame"; Photo P1, P2 for the flat edges (D10) |
| Rebate | 22 wide x 53 deep; the stop (outside) 74 deep; leaf opens inwards | Scaled: Hasluck Fig. 1148 and Riley Fig. 671 |
| Jamb showing past the brick | 55.0 each side (x 0-55 and 827-882) | Photo P1 (left 10 px, right 11 px, +-10) |
| Head | 101.6 x 127; top edge cambered to follow the soffit; 70.4 shows at the crown, 52.4 at the ends | Photo P1 |
| Frame outside face y / inside face y | 114.3 / 241.3 | Derived |
| Stop's inner edge | square, no bead (F1 has one) | Photo P1 |

### 4.3 Transom (weathered, projecting, nosed) and glazing

Front profile `frame.transom.front_profile_yz_mm` (y from the jamb face plane, outwards negative; z up from the stop underside 1937.6): (0,0) (-12.5,0) (-13.8,1.2) (-14.0,2.6) (-13.4,4.0) (-10.5,6.0) (-8.6,9.0) (-8.0,14.0) (-8.0,40.0) (9.5,65.0), then the shelf at z 65 to the glass slot.

| Item | Value | Source, kind |
|---|---|---|
| Face height (lip + cove + face + slope seen from the front) | 65.0: lip 0-4, cove 4-14, face 14-40, slope 40-65 | Photo P1 column profile x 140-175: bar rows 143.3-155.5 (12.2 px), bright slope rows 143.5-147.9, face 148-152.9, crease 153-154.9, lip 155 (+-1 px) |
| Face plane proud of the jamb faces | 8 | Judgement (+-3) from P2's shadow and P1's lit lip |
| Nose (lip bead) proud | 14, bead radius 2.6 | Judgement (+-3) |
| Slope | from (y -8, z 40) to (y 9.5, z 65): 55 degrees | Derived; Read: Hasluck p.398 "weathered" |
| Transom x extent | 45 to 837 (the front member overlaps each jamb face by 10; the body runs between the jambs) | Photo P2 (nose ends beyond the stop edge), Judgement |
| Stop underside / rebate underside / top | z 1937.6 / 1959.6 / 2002.6 | Derived (leaf top 1958 + 1.6; 22 rebate) |
| Glass opening | x 55-827, z 2002.6-2269.6 (772 x 267) | Photo P1 rows 92.5-143.3 (lab D7) |
| Glazing bead | quarter-round, face 10 x 8 proud, 1.5 mm flat at the foot, mitred, all four sides, inside the opening | Photo P1: 2 px bright line at the glass foot, 2 px dark line at the head; profile Judgement |
| Clear glass | x 65-817, z 2012.6-2259.6 (752 x 247); glass 3 thick at y 133.3, in 6.4 deep slots 4 wide | Photo P1 clear rows 95.0-142.5 (245 +-10); slots Judgement |

### 4.4 Leaf, panels and mouldings

| Item | Value | Source, kind |
|---|---|---|
| Leaf | 812.8 x 1948.0 x 50.8, x0 34.6, bottom 10 above the threshold, outside face y 188.3 | Read: Hasluck p.347 (2 ft 8 in), Ellis p.93 (2 in); Photo P1 for the height (+-31, D1) |
| Stiles / top rail / lock rail / bottom rail | 114.3 / 127.0 / 228.6 / 192.8 | Read: Ellis p.93, Riley p.357; Photo P1 (bottom rail) |
| Muntin | 120.0 (revised from 132.2) | Photo P1 re-measured, +-10 (D2) |
| Lock rail centre | 787.0 above the leaf bottom | Photo P1 +-12 (D3) |
| Panel openings | 232.1 wide; upper 919.7 high (v 901.3-1821.0), lower 479.9 (v 192.8-672.7); u 114.3-346.4 and 466.4-698.5 | Derived |
| Panel | flat, 16.9 thick centred; grooves 12.7; play 3.2 | Read: Riley p.353; Ellis p.92 |
| Bolection (outside) | 36 on the face, 4.8 lap, 7.0 proud, panel face 16.95 below the framing; profile (d, h): (0,0) (0,3.5) (1.4,5.8) (3.5,6.9) (5.5,7.0) (7.5,6.4) (10.5,4.6) (14.5,1.0) (19,-4.5) (24,-10.5) (29,-14.5) (33,-16.3) (36,-16.95), closed by (4.8,-16.95) (4.8,0) | Scaled: Riley Fig. 671 (36 +-5), Read: Ellis p.92 (lap 3/16 in); Photo P1 34 +-8; profile shape Photo P1 and P2, Judgement |
| Single (inside) moulding | 22 wide, planted | Scaled: Riley Fig. 671 |

### 4.5 Lock-rail band and weatherboard (T1 only)

| Item | Value | Source, kind |
|---|---|---|
| Band z above the leaf bottom | 785.0 to 857.5 (72.5 high) | Photo P1 column x 145-175: top edge row 363.5, underside row 377.5 (+-1 px) |
| Band x | 57.0 to 825.0 (2 mm short of each stop face) | brief; review 2 fault 5 |
| Band projection / profile (z, p) | 22 max; (0,0) (0,17) (1.5,19.5) (4,20.5) (9,20.5) (14,19.5) (18,18) (22,15) (25,13) (28,14) (31,17.5) (34,20) (37,21) (40,20) (42,17) (45,16) (49,14.5) (52,15.5) (55,18.5) (58,20.5) (62,22) (66,21) (69.5,17) (71.5,10) (72.5,0) | Photo P1: highlights at rows 365.5, 371 and 374, dark creases 367.5 and 372.5, shadow rows 378-382 (L 60 against 100); projection Judgement (+-6) from the shadow |
| Weatherboard z | 0 to 80 above the leaf bottom, x 57.0-825.0 | Photo P1 rows 513.7-529.7 (16 px = 82 +-8); the lab's 72 came from rows 515-529 |
| Weatherboard projection / profile (z, p) | 26 max; (0,0) (0,12) (2,18) (6,22) (14,25) (26,26) (40,25.5) (50,23) (54,19) (57,17.5) (60,18.5) (63,22) (67,25.5) (72,25) (76,21) (78.5,13) (80,0) | Photo P1: highlight rows 514-517, hollow 518-519, face 520-527, edge 528-529; projection Judgement (+-6) |

### 4.6 Ironmongery (all brass or dark steel, no maker's mark)

| Item | Value | Source, kind |
|---|---|---|
| Letter plate | vertical on the muntin; outer 76 x 242, backplate 3, rim 13.5 wide raised 6 with a 45 degree outer chamfer; aperture 48 x 190, 22 below the plate's top; a sprung flap hinged along its top, 2 mm gap, dished 3; centre 1617 above the leaf bottom, on the leaf's centre line | Photo P1 16x crop: x 186.25-200.9, rows 192.5-239.4 (+-1.5 px); aperture rows 196.9-233.75; relief Judgement |
| House number (optional) | two stacked digits 39 x 72, stroke 7, relief 3, gap 22, v 1207-1277.6 and 1300-1373, on the muntin | Photo P1 rows 263.4-295.6; the number is the town's |
| Cylinder lock | flush; collar 43.5, plug 28, collar proud 1.5, vertical keyway 3 x 9; centre u 745.8 (46.6 from the stop face), v 1235 | Photo P1 16x crop: centre (258.75, 290.3), 8.4 px (+-1 px) |
| Keep | on the right jamb's stop face: 22 x 72.6, 3 proud, centre x 859.4, z 1120.3-1192.9; dark steel box keep with a slot | Photo P1 16x crop rows 300.3-314.4 |
| Knob, knocker, chain | none | Photo P1 |
| Hinges | none show; inside, three 100 mm steel butts on the left stile (optional) | Photo P1, P2; Judgement |

### 4.7 Setting: threshold, riser, step, arch, dressings

| Item | Value | Source, kind |
|---|---|---|
| Threshold stone | 76 thick, top z 0, front flush with the wall face (y 0), back y 241.3, rounded nose r 18 overhanging the riser by 18, length 1106 (882 + 112 bearing into the brick each side), top flat (a 3 mm fall may be added) | Photo P1 rows 534-547.5 (13.5 px = 70 +-10); Ellis p.111-112 (sill horns run into the wall) |
| Riser | z -148 to -76, face at y +18 (recessed) | Photo P1 rows 548-561.5 (14 px = 72 +-10) |
| Step tread | top z -148 (+-25), 960 wide (x -39 to 921, +-60), front at y -312 (+-80), 110 thick, bullnose r 30, plan corners r 40, top falls 6.6 to the front; ground z -258 | Photo P1: x 87-291 px (204 px, perspective), back edge row 561.5, front row 592; depth and thickness Judgement. Perspective check: 204 px at 960 mm puts the camera 5.8 m away, the brick courses 4.8 m (self-check) |
| Arch ring | 12 buff bricks on end, 215 deep at the crown, flat top z 2555, soffit cambered 18, joint 8; ends x -22 and 904 (22 past each reveal) resting on the top 112-wide quoin course | Photo P1 (c1_arch 4x: ring x 104.5-283.75, top row 32.5, intrados rows 71.5-77.5); Ellis p.112 Fig. 355 draws a brick arch on the head; the brick's 215 is Judgement |
| Quoins (wall detail) | buff, long and short: header 112, stretcher 225, 30 courses at a 77 gauge from z 12 to 2322 | Photo P1: stretchers 47 px, headers 22.5 px, course pitch 15.2-15.4 px (autocorrelation, three regions) |
| Plinth | three courses with a splayed and dog-tooth cap up to the leaf's bottom level, hiding the jamb feet | Photo P1; the wall's own, not specified |

## 5. The target, F1: the side door to a flat over a shop (0.838 x 1.981, P2)

F1 is the same door at the street's size with P2's transom and furniture. Full numbers are `variants.flat_door_over_shop.parts` in target.json (the same keys as T1).

| Item | Value | Source, kind |
|---|---|---|
| Leaf | 838.0 x 1981.0 x 50.8; x0 53.0; z0 10; members as T1 with the extra 25 mm of width in the panels (opening 244.7 wide) and the extra 33 mm of height in the upper panels (952.7 high) | SS (spec); Derived |
| Opening (bay) | 944.0 wide (the kit); clear between stops 797.2; jambs show 73.4 | SS; Derived; P2's jamb strip is 49 mm: could-not-settle 1 |
| Head | flat, top at z 2400.0 (the shop's transom line, SS); glass opening z 2072.6-2339.6 (777.2 x 267); head shows 60.4 | Derived |
| Transom | face 102 (nose 0-36, face 36-70, slope 70-102); face proud 10, nose proud 22; slope from (-10, 70) to (9.5, 102); ends overlap the jamb faces 16; x 57.4-886.6 | Photo P2 rows 75-121 of the 675 x 1200 preview (46 px = 13.4% of the visible leaf width = 107 mm, zones 30/33/35%); Read: Riley "Transome 5 x 4" (101.6); the projection Judgement (+-8) |
| Mouldings | bolection 42 on the face; no band, no weatherboard | Photo P2 (18.5 px = 43 mm) |
| Jamb stop bead | quarter-round 5 x 2.5 on each stop's inner edge | Photo P2; Read: Hasluck p.346 "beaded on the inside" |
| Letter plate | as T1 (vertical on the muntin, 76 x 242, centre 1617 above the leaf bottom, on the leaf's centre), with four 4 mm slotted screws at the rim's corners | P1 for size and place, P2 for the screws; D15 |
| Centre knob | turned, 69 across, 62 proud of a 76 dished rose sunk 3, at the lock rail's centre (v 787), five turned rings (profile in json), 4 mm brass cap | Photo P2 8x crop; Read: Ellis p.93 (handle in the middle of the rail) |
| Cylinder lock | knurled collar 37, plug 18, 12 serrations, centre 46.3 from the stop face, v 1040 | Photo P2 5x crop |
| Plugged keyhole | 23 x 32 dark recess, 34.8 from the stop face, v 1151 | Photo P2 |
| Keep | as T1, v 952 | Judgement |
| Threshold | painted softwood, 70 thick, rounded front r 8, top at z 0, ground z -70; no step | Photo P2 rows 945-975 (30 px x 2.3) |
| Arch, quoins, riser, step | none (the shopfront owns the head, the pilaster the sides) | - |

**Against SCENE-SLOTS (photographs win, the differences written down).**

| Scene stand-in | Against the photographs | Choice |
|---|---|---|
| Leaf 0.838 x 1.981 | visible proportion 2.46 lies inside P1's 2.47-2.50 (+-0.04) and 3% above P2's 2.39 (a squatter six-panel door) | kept |
| Letter plate 0.25 x 0.04 at 1.0 | P1's plate is 0.242 long x 0.076 wide with a 0.19 x 0.048 aperture, centre 1.617 above the leaf bottom; P2's horizontal plate is 0.195 x 0.070 at 1.50; the shopfront research's BS EN 13724 range 0.7-1.7 m (post-1990) contains both | size kept as the long side, height 1.617 (1.627 above the threshold), vertical on the muntin |
| Overall 0.944 wide | P2 shows the jamb strip 49 mm | kept as the bay; jambs 73.4 (could-not-settle 1) |
| Transom at 2.40 | consistent with F1's head at 2.40 | kept; the shopfront's own spandrel above is not this target's |

## 6. Variants, colours, materials

**Kinds.** T1 (terrace four-panel, brick opening, step) and F1 (flat over shop). An option, `option_six_panel`, gives P2's six-panel layout as fractions of the visible leaf for variety (not requested). Counts are the scene's.

**Door colours** (sRGB, as the game's base colour, gloss; roughness 0.35 new, 0.55 for 1990 weathered, 0.65 on the weather side low down; metal 0):

| id | Name | sRGB | Weight | Source |
|---|---|---|---|---|
| black | gloss black, faintly blue | 35, 36, 40 | 0.25 | Photo P2 median (39,40,45) |
| dark_green | dark green | 28, 59, 41 | 0.20 | shopfront research and kit (0.11,0.23,0.16) |
| maroon | maroon / oxblood | 92, 26, 32 | 0.15 | research names it; value Judgement |
| navy | dark blue | 24, 38, 78 | 0.15 | research names it; value Judgement |
| brown | dark brown | 74, 48, 34 | 0.15 | research names it; value Judgement |
| red | bright red | 201, 41, 32 (x 0.85 and chalked for 1990) | 0.10 | Photo P1 median; 2012 fresh paint |

F1 uses the same list without red (weights renormalised). **Frame:** gloss white, yellowed, sRGB 226, 224, 214 (P1 240,239,245 fresh; P2 222,225,229 old) weight 0.7; cream 222, 212, 184 weight 0.3 (Judgement). **Other surfaces:** brass sRGB 181, 150, 85, metal 1.0, roughness 0.4 (0.25 on worn edges; P1's plate reads pale gold-green 182,181,158); nickel or chrome 170, 170, 168, metal 1.0, roughness 0.35; dark steel 40, 40, 42, metal 1.0, roughness 0.6; glass roughness 0.05, IOR 1.5, reads 121,131,139 over a dark interior; step stone 156, 153, 149 roughness 0.85 (the threshold's front stained 142,127,111); arch bricks buff 219, 209, 190 roughness 0.9; quoins buff 200, 186, 158; F1 threshold 81, 72, 65 roughness 0.7.

## 7. Edges, joints, fixings, drips and ground

Written in full in target.json `edges`, `joints_and_seams`, `fixings` and `drips_and_throats`. In short:

- **Edges.** Frame: square (eased 1), no ovolo, no tube. Leaf: square (eased 1.5). Bolection: rounded nose 3.5, crease at the foot. Band: square underside, three crests and two coves, rounded top. Weatherboard: flat underside, belly, hollow, rounded nose. Transom: lip bead r 2.6. Threshold nose r 18, tread bullnose r 30, plan corners r 40. Bead: quadrant 10 x 8. Plate rim chamfered 45 degrees.
- **Joints.** Rail/stile hairlines 0.4 wide; mitres closed; 1.6 mm shadow gap round the leaf, 10 under it; band and weatherboard 2 short of the stops; 3 mm joint frame to brick.
- **Fixings.** Moulding screws hidden; plate screws only on F1 (four, 4 mm); no hinges, bolts, straps or knockers outside.
- **Drips and throats.** The weatherboard and its hollow, the transom's slope and nose, the threshold's 18 mm overhang.
- **Ground.** T1: a rounded-nosing stone step on the pavement, the threshold 258 above it; F1: a timber threshold 70 above it with a cracked slab in front.

## 8. Wear as the photographs show it (1990 rule)

P1: a fresh gloss coat with brush marks running with the grain, grime on the band's and weatherboard's top nosings and in the dark crease under the band, a brown-gold stained threshold and a pale worn step nosing, a dirty frame foot. P2: crazed paint over the whole leaf in 2-4 mm cells, bare pale patches and chips on the lower right panel's moulding and on the bottom rail, dirt packed in the moulding angles, a wet-grimed flaking bottom rail, peeling frame paint down to a darker undercoat, plugged holes, a worn bare threshold. **For the kit:** unrestored, not heritage-fresh; crazing and chips on arrises and the mouldings' lower lips; paint 15% duller; grime in angles and on upward faces; darker and flaking low down (the bottom rail, weatherboard, frame foot, threshold); brass dull with bright touched edges. Cables, junction boxes, stickers, tape and the wall lantern in the photographs are not part of the kit. (The shopfront research agrees: failure where water sits, chips on arrises and sills.)

## 9. The checks the builder's automatic check must pass

`target.json` `checks` lists 69, each with a name, what to measure, the expected value and the tolerance, and where it comes from. Groups: **A** the lab's pass rule (front view layer by layer, every section: IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm) plus **A4** profiles (outline p95 <= 1.5, worst <= 3); **B** dimensions; **C** frame edges (the jamb section is rectilinear, the face flat, feet square and alike); **D** transom (projection 14/8, slope 55 +-8 degrees, a lip bead, overlap 10, bead 10 x 8, not one flat plane); **E** and **W** band and weatherboard (heights, projections, crests and coves, end gaps 2 +-1.5); **F** ironmongery (plate 76 x 242 at 1617, lock 43.5 at 46.6 in, keep, knob, no outside hinges); **G** step, threshold, arch (bearing on the brick, camber, nothing floating); **H** the built elevation laid on P1 within 2.5 px; **I** surfaces (no coplanar overlaps, closed mitres, hard edges where the target has square arrises, colours, glb pivot). The faults that failed the lab's reviews each have a check: round jambs C1-C2, flush transom D1-D7, plain band and wedge weatherboard E3, W3, no ironmongery F1-F10, thin sill G1-G5, floating lintel G7-G9, hatching I1, dark hairlines I2.

## 10. Self-check result

`python self_check.py` (reads target.json and the drawing's polygons, writes `self_check` into target.json): **230 of 231 checks pass; the one miss is reported, not hidden** (group 4: the visible height-to-width of P2's six-panel door is 2.39, F1's 0.838 x 1.981 shows 2.46, so P2's door is 3% squatter than the street's size; kept, as the scene's size is no photograph's contradiction beyond its error). Groups: 1 printed (18), 2 photographs win (D1-D7, D10-D17), 3 P1 projected edges at a scale fitted on the visible width only (5.15 mm a pixel, anchors x 192.85 px = 441 mm and row 530.0 = z 10; 40 edge and perspective tests and 8 fractions), 4 P2 against F1 (12), 5 consistency by numbers and by shapely on the drawings (91: no overlaps, nothing floating, the 1.6 mm leaf gaps, the 2 mm band gaps), 6 the builder's checks evaluated on the drawing (47; they hold for the target).

**How to read it honestly.** The independent tests of the target against P1 are the panel mouldings, the transom, the glass, the head, the brick edges and the arch ends, all within 2 px. The band, weatherboard, plate, lock, keep and numerals were fitted to the same photograph, so their near-zero differences are by construction. The leaf's height depends on the scale (the left edge of P1 leans 2.6 px in 210 rows, so the width reads 149.7 at the top and 152.4 at the middle): the vertical scale carries +-1%.

## 11. Could not settle

1. **Jamb face on the flat door.** The bay's 0.944 gives 73.4 mm of jamb; P2 shows a 49 mm strip and a groove. If the bay can give 47 mm, set the jamb to 50 (opening 897 wide).
2. **Dated photographs.** None from 1975-2000 reachable; P1 2012 (original or replica not documented), P2 2024. The 1990 colours are the shopfront research's names with judged values.
3. **Mouldings' width and the band's and weatherboard's sections.** At 480 px the bolection reads 34 +-8 (the lab's 36 kept), and the band and weatherboard are drawn to reproduce their highlights and shadows, not measured outlines. The projections (band 22, weatherboard 26, transom 14 and 22) come from shadow lengths: +-6.
4. **The step.** Its depth (312), thickness (110) and the ground 258 below the threshold are perspective judgements: +-80, +-40, +-40.
5. **The leaf's height,** 1948 (1926 if the scale is fitted on the mid-door width): 1%.
6. **The transom's ends.** P2 shows the nose rolling over the stop's edge; a square end overlapping the jamb face is specified.
7. **F1's fanlight height.** The kit's side door rises to 2.85 with a fielded panel above; P2 is cropped at the glass. F1's head is at 2.40 (the shop transom line); anything above it is the shopfront's.
8. **Hinges, the plinth and dog-tooth course, an actual Hook door's colour in 1990:** hinges are inside, the plinth is the wall's, the colours judged.

## 12. Credits for the previews in `production/previews/cloud-week/refs/front-door/`

| File | Credit |
|---|---|
| door-photo-01-teignmouth-four-panel-red.jpg | Robin Stott, CC BY-SA 2.0, Geograph 3157125 via Wikimedia Commons, taken 2012-05-06 (reduced; for measuring only) |
| door-photo-02-tottenham-six-panel-black.jpg | Acabashi, CC BY-SA 4.0, Wikimedia Commons, taken 2024-02-03 (reduced; for measuring only) |
| ellis-1902-p089 to p093, p111, p112; hasluck-1907-p346, p347, p398; riley-1905-p353, p355, p357 (and the crops) | public domain by age (1902, 1907, 1905), archive.org page images, as the lab saved them |
| door-photo-01-teignmouth-target-on-photo.jpg | the target's drawing (own work) laid on Robin Stott's photograph (CC BY-SA 2.0); 900 x 1200, 203 KB; the step is drawn at the door plane's scale, so the stone, which is nearer the camera, reads wider |
| door-target-on-photo-2026-10-08.jpg, door-v2-*, door-v3-* | the lab's overlay and renders, kept for comparison |
