House windows of Quay Street: twenty windows in ten houses, every frame white (Jafar's ruling of 3 October), four kinds (two over two, one over one, and two replacement casements), each pane glass over a dark room with its box shaded and its lines drawn, nets and drapes by the photographs' mix, thirteen small rooms behind them in the game's own projection, and the white-board fault caught by measurement on 1979 to 1994 photographs, measured the way the gate measures.

# House windows of Quay Street: the exact target

**Status: fixes applied, not re-reviewed (13 October 2026).** Cloud week 42, part 2, unit 8: written by the target writer from sources reached that day, failed its fresh review (TARGET-REVIEW.md: three faults, twelve narrow points), and corrected as FIXES-APPLIED.md lists, one line per fault and point. Nothing is built and nothing is committed. Every number below is in `target.json`; the checks that follow from it are its `checks` list and its `self_check` (self_check.py --live --previews --photos (the re-measure row counted): 424 pass, 0 fail; negative controls: 27 of 27 caught).

The lessons of unit 7's fresh review (TARGET-REVIEW.md of the shop windows) are applied from the start: every opening is covered above and around its parts (section 4.5); the toplights of the replacement are one transom and equal lights (4.3); no real firm's name is on any model's texture (every model's 1k base colour was looked at, section 7.4, and the checks include a final-texture check PIC-07); the night wash is the game's colour; the projection rule `trace` is the only source of what a room shows, with stand-off budgets derived again for these smaller rooms (3.3); the numbers are exact and the checks measurable (section 10); and every preview was looked at after it was written.

**What the fresh review found and what changed** (FIXES-APPLIED.md has the line for each): every house's frame is now white, as Jafar ruled on 3 October (a coloured frame needs his answer, OWED-05); the white-board bands are measured from the photographs the way the gate measures (L over the joinery, D with no brick), with a new line check WB-04b and the window states bare, net and draped; television_02's maker's name on its front bezel is painted out and the maker is on the blocklist; the cottage rooms' stand-off budgets put the eye at the window (back wall 0.38 true, 0.71 tolerated); the P6 replacement form is built (RC2); the lit order puts lounges before landings. **The lessons of this review**, kept for the next target: a number measured from photographs must be measured the way the gate will measure it; and a design is checked against the owner's standing rulings, not only the latest one.

## 0. Files, and how to read them

| file | what it is |
|---|---|
| TARGET.md | this page (made by make_doc.py from target.json) |
| target.json | the twenty sites, the kinds and their parts, the glass, the box's shade, the nets and drapes, the thirteen rooms with their objects and budgets, the inventory with each model's marks, the kit pieces' nodes, the gate, 47 checks, the photograph measurements, the overlay's edges, the lit table, `photographs_win`, `could_not_settle`, `owed_on_pc`, the self-check |
| target_drawing.py | draws target.json alone: each kind's elevation and sections, each room's picture layout and back wall, the row of twenty, and (with --photo) the 2/2 elevation laid on photograph P8; into a JSON of polygons (millimetres) and a folder of pictures |
| self_check.py | tests the target against its own sources (it writes into target.json only with --write); 27 negative controls |
| TARGET-REVIEW.md, FIXES-APPLIED.md | the fresh review of this target (FAIL: 3 faults, 12 narrow points) and one line per fault and point saying what was changed and where |
| hw_common.py, hw_data.py, hw_rooms.py, hw_sites.py, hw_photos.py, hw_measure.py, hw_checks.py, make_target.py, make_doc.py, make_previews.py | author tools: the game's rule and the stand-off budgets; the glass, nets, paints; the rooms; the sites derived from terrace-front.py; the photographs, their crops and masks; the pane-to-frame measurement; the kit nodes, gate, checks; the builders of target.json, TARGET.md and the previews |
| polyhaven_models_checked_raw.json, polyhaven_textures_checked_raw.json, geograph_pages_read.json | what the Poly Haven API and the 14 Geograph pages answered on 13 October |
| production/previews/cloud-week/refs/house-windows/ | P1 to P14 (the photographs measured, cropped to the windows, masked where a crop would show a plate or a sign), the overlay of the drawing on P8, and the sheet of measured windows |

Run with `/home/user/.bpyenv/bin/python`: `make_target.py [--photos DIR]`, `self_check.py [--photos DIR] [--previews DIR] [--live] [--write]`, `target_drawing.py OUT_DIR [--photo FILE --overlay FILE]`, `make_doc.py`, `make_previews.py [--photos DIR] [--out DIR]`.

**Units and frames.** Windows in millimetres in the *kit frame*: x across the window (0 at its middle, positive to the viewer's right), y *into the wall* from the brick face (0 at the face), z *up* from the opening's bottom edge. Rooms in metres in the *room frame*: x across from the room's centre (positive toward the picture's right), y back from the card plane, z up from the floor. The street in metres as the scene file has it (x along, y across, east positive, z above the road crown; the footway is crown + 0.10). **Kinds of number:** Read (printed in a file), Scaled, Photo (measured on a photograph: method and error given), Derived, Judgement.

## 1. The street's windows as found

The street has **twenty house windows in ten houses**, and 48 more on the hill's rows. They come from `tools/art-recipes/terrace-front.py` (`plan_street`, re-derived by `hw_sites.py` and compared by the self-check, so the table cannot drift from the recipe). `production/assets/street/quay-street.json` holds only their materials (`frame_painted`, `frame_bronze`, `glass_eu_*`, `glass_wg_*`, the net cards), not their kinds. The shops' own ground-floor glass (east parade, west_north, east_chandler) is unit 7's and is not here.

**What the recipe draws today, and what is wrong with it** (each is a finding the PC session acts on, section 8):

- East parade, six houses, **upper floor only** (the ground floor is a shopfront): twelve windows at bay start + 1.5 and + 4.5 m, the opening 850 wide, head 5.9 above the crown. The kit's checked sash (the lab's, 8 October) is used there: a two-over-two on bays 0 and 3, a one-over-one on bays 1 and 5 (`SASH_KIT_ROWS = ("east_parade",)`), opening 1676.4 high (sill 4.2236). Bays 2 and 4 draw a 1980s replacement as a box of `frame_bronze` (anodised) with a transom at 0.72 of the height and no bars.
- East chandler, one house (a metal-refit shop below): two upper windows, a replacement in bronze, **1500** high (sill 4.4): not the period opening.
- West south, three single-storey cottages: six **ground-floor** windows (door at 1.5, windows at 3.3 and 5.1 m of the bay, mirrored with the door), the opening 1500 high (z 1.0 to 2.5). **`_plain_ground` draws every one as a 2/2 box sash (55 mm frame, 22 mm bars), whatever `_window_kind` says of the house** (finding D4).
- West north, three shops of one storey: no upper windows; nothing here.
- The hill: `backdrop_rise_approach_e`, `_w` and `_x` stand 2, 5 and 5 houses of CLIMB_HOUSE (two storeys, a 'plain' ground floor) through `plan_parts`: 48 windows by the same code, with a flat net card (one in three the lit `window_far_lit`). The north rise's framed windows (`_framed_window`, 125 m out) are two pixels of frame and stay flat cards.
- **Six over six does not occur on the street** (no house is Georgian); two photographs show it on Georgian terraces (P10, 1983; P13, 1982). It is not built.

**The twenty, by position.** *Kind by house* is what `_window_kind` gives the house; *built today* is what the recipe draws; *target* is what this unit makes. Every site gets the period opening 850 x 1676.4 (the ruling of 8 October: "1.68 m"), the head kept where it is, so the cottages' sills go from 1.0 to 0.8236 above the crown (0.7236 above the threshold). P6's ground bay window's sill stands 0.85 ±0.05 above its step (the door leaf 193 px = 1981 mm, the sill 83 px up): the cottages' sills are 0.13 lower than that, to keep the head and the arch clear of the eaves (D4; Jafar's to choose).

| site | x | floor | kind by house | built today | target | paint | net | drape | room | lit 20:30 |
|---|---|---|---|---|---|---|---|---|---|---|
| east_parade_bay0_upper_w0 | 4.5 | upper | 2/2 | S22 kit | S22 | white_grimy (grimy) | N2/greyed | - | up_landing_1 | no |
| east_parade_bay0_upper_w1 | 7.5 | upper | 2/2 | S22 kit | S22 | white_grimy (grimy) | N1/white | C2/cream | up_lounge_1 | yes |
| east_parade_bay1_upper_w0 | 10.5 | upper | 1/1 | S11 kit | S11 | white_fresh | N0 | B2/cream | up_landing_2 | no |
| east_parade_bay1_upper_w1 | 13.5 | upper | 1/1 | S11 kit | S11 | white_fresh | N1/white | C2/brown | up_bedroom_1 | no |
| east_parade_bay2_upper_w0 | 16.5 | upper | replacement | box replacement (frame_bronze) | RC | white_upvc | N1/greyed | C2/green | up_lounge_2 | yes |
| east_parade_bay2_upper_w1 | 19.5 | upper | replacement | box replacement (frame_bronze) | RC | white_upvc | N2/greyed | - | up_landing_1 | no |
| east_parade_bay3_upper_w0 | 22.5 | upper | 2/2 | S22 kit | S22 | white_flaking (flaking) | N1/yellowed | - | up_empty_1 | no |
| east_parade_bay3_upper_w1 | 25.5 | upper | 2/2 | S22 kit | S22 | white_flaking (flaking) | N0 | - | up_empty_2 | no |
| east_parade_bay4_upper_w0 | 28.5 | upper | replacement | box replacement (frame_bronze) | RC2 | white_upvc | N2/white | C1/green | up_bedroom_2 | no |
| east_parade_bay4_upper_w1 | 31.5 | upper | replacement | box replacement (frame_bronze) | RC2 | white_upvc (grimy) | N1/yellowed | - | up_landing_2 | no |
| east_parade_bay5_upper_w0 | 34.5 | upper | 1/1 | S11 kit | S11 | white_grimy | N1/white | C2/floral_cream | up_lounge_3 | yes |
| east_parade_bay5_upper_w1 | 37.5 | upper | 1/1 | S11 kit | S11 | white_grimy | N3/white | - | up_landing_1 | no |
| east_chandler_bay0_upper_w0 | 41.5 | upper | replacement | box replacement (frame_bronze) | RC | white_upvc | N0 | B1/white | up_bedroom_3 | yes |
| east_chandler_bay0_upper_w1 | 44.5 | upper | replacement | box replacement (frame_bronze) | RC | white_upvc (grimy) | N2/yellowed | - | up_landing_2 | no |
| west_south_bay2_gf_w0 | 6.3 | ground | 2/2 | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | S22 | white_fresh | N1/white | - | gf_front_3 | yes |
| west_south_bay2_gf_w1 | 8.1 | ground | 2/2 | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | S22 | white_fresh | N1/white | B3/white | gf_front_3 | yes |
| west_south_bay1_gf_w1 | 9.9 | ground | replacement | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | RC | white_upvc | N0 | C1/brown | gf_front_2 | yes |
| west_south_bay1_gf_w0 | 11.7 | ground | replacement | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | RC | white_upvc | N2/white | - | gf_front_2 | no |
| west_south_bay0_gf_w1 | 15.9 | ground | 1/1 | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | S11 | white_grimy (grimy) | N1/white | - | gf_front_1 | no |
| west_south_bay0_gf_w0 | 17.7 | ground | 1/1 | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | S11 | white_grimy (grimy) | N1/white | - | gf_front_1 | no |

Kinds: **6 two-over-two (S22), 6 one-over-one (S11), 6 replacement casements of P7's form (RC) and 2 of P6's form (RC2: east_parade_bay4).** Upper floors 14, ground 6. The landing windows (the window on the side-door's side of each flat: bays 0, 1, 2 (right), 4 (right), 5 (right), the chandler's right one, and the empty flat's left) light the stair; the others light a lounge or a bedroom. The unlet flat above the empty shop (bay 3) is empty at both windows.

## 2. Sources

Only sources reached on 13 October are used. Photographs are for measuring and for the reviewers only: never placed in the game, never traced into a texture, never fed to an image model. Each Geograph page was opened (title, author, date taken, licence CC BY-SA 2.0 read on the page). Every preview was looked at after it was written; each is cropped to the windows and any plate or sign the crop would still show is masked flat grey (the masks are read back from the JPEG by the self-check). No person, child, firm's name, door or house number is in any preview.

| id | page | title | author | taken (page) | shows | period? |
|---|---|---|---|---|---|---|
| P1 | [3380884](https://www.geograph.org.uk/photo/3380884) | John Street, Kingston upon Hull | Bernard Sharp | Tuesday, 5 March, 1985 | a port town's 1850s terrace seen along the street at 10 to 35 degrees: white-painted 1/1 and 2/2 sashes and dark-brown ones, white voile nets in the lower sash, stone-painted sills and heads | the period itself (1985) |
| P2 | [3462979](https://www.geograph.org.uk/photo/3462979) | Durham Street, Kingston upon Hull | Bernard Sharp | Sunday, 17 August, 1986 | a brick terrace with each house's frames painted its own colour (white, blue, olive, cream render), lower-sash voile nets with the upper sash clear, a louvre blind in one ground window | the period itself (1986) |
| P3 | [2738668](https://www.geograph.org.uk/photo/2738668) | Penchwintan Terrace, Bangor | Chris Andrews | Sunday, 29 May, 1988 | a stone terrace with 2/2 and 1/1 sashes in white, cream and red-brown, lace and voile nets, a bare ground window with a dark room, seen from 30 degrees to square on | the period itself (1988) |
| P4 | [566077](https://www.geograph.org.uk/photo/566077) | Oswald Street, Rochdale, Lancashire | Dr Neil Clifton | Saturday, 15 September, 1979 | black-and-white: a brick terrace's sashes seen at 20 to 40 degrees: full white nets, a half net, a bare ground window with the room black and a pot plant | the period itself (1979) |
| P5 | [566265](https://www.geograph.org.uk/photo/566265) | Tanfield Road, Croydon - North side | Dr Neil Clifton | Sunday, 14 October, 1979 | black-and-white: a Victorian terrace's bay and upper sashes at 15 to 40 degrees, white nets, dark glass | the period itself (1979) |
| P6 | [2321423](https://www.geograph.org.uk/photo/2321423) | Terraced House - Ratcliffe Street, Levenshulme | Anthony Parkes | Friday, 10 June, 1994 | a terrace front square on: a replacement upper window (white, a top light across and two lower lights, the transom at 0.66 of the height), a ground bay with a full net and a side light with lace | the period itself (1994); the upper window is a replacement |
| P7 | [689253](https://www.geograph.org.uk/photo/689253) | Nos. 34, 32 and 30, Frederick Street, Barnoldswick | Dr Neil Clifton | Tuesday, 10 April, 1990 | black-and-white: stone terrace 'mostly modernised with double glazing' (the page): white replacement frames with a top light, half-height and full nets | the period itself (1990) |
| P8 | [3499732](https://www.geograph.org.uk/photo/3499732) | Back of terraced houses, Sunningwell Road, Oxford, 1987 | Christopher Hilton | Tuesday, 30 June, 1987 | the back of a Victorian terrace seen nearly square on from below: two 2/2 sashes, white frames, the panes dark blue-grey (sky over a dark room), a net at the right of one | the period itself (1987); the sashes are original (the page: Victorian) |
| P9 | [3466378](https://www.geograph.org.uk/photo/3466378) | Boundary Street Estate, 1989 | Christopher Hilton | Sunday, 4 June, 1989 | tall arched sashes of a brick estate at 25 to 40 degrees, sunlit and shaded faces: panes pale, frames white, the bars as dark lines | the period itself (1989) |
| P10 | [361082](https://www.geograph.org.uk/photo/361082) | Copenhagen Street, Islington | Tom Jolliffe | October 1983 | a Georgian terrace: 6/6 sashes seen at 20 to 35 degrees with pale blue panes, boarded windows beside them | the period itself (1983) |
| P11 | [2876894](https://www.geograph.org.uk/photo/2876894) | Newburn Council Houses | Kevin Hall | Tuesday, 1 August, 1989 | 1960s council houses in 1989: white casement windows, a fixed light and a top-hung light, net and vertical drapes; the council replacement kind | the period itself (1989) |
| P12 | [2238747](https://www.geograph.org.uk/photo/2238747) | Terraced housing in Railway Street | P L Chadwick | Sunday, 9 August, 1987 | a stone terrace with white and olive-green sashes, lower-sash voile nets, an open curtain, leaded top lights | the period itself (1987) |
| P13 | [3379651](https://www.geograph.org.uk/photo/3379651) | Prince Street, Kingston upon Hull | Bernard Sharp | Sunday, 25 July, 1982 | a narrow street: the windows of the right-hand wall seen at under 10 degrees read as a white slit beside a dark void (the 1a finding), boarded and blank windows opposite | the period itself (1982) |
| P14 | [674344](https://www.geograph.org.uk/photo/674344) | Derelict council houses, Milan Avenue, Burnley, Lancashire | Dr Neil Clifton | Friday, 29 July, 1988 | empty houses of 1988: windows boarded with plywood, broken lights, no nets | the period itself (1988) |

The Geograph syndicator feed (`api.geograph.org.uk/syndicator.php`, ordered by date taken through the search id's pages) was used to find them: about 1,200 photographs taken 1975 to 1996 came back for terrace, street, sash, council, harbour and night queries; none of the night, dusk or lit-window queries returned a photograph of a terrace before 1996. Wikimedia Commons and archive.org were not asked (the feed answered).

**Research and project files read:** production/cloud-week/research/1a-sash-windows-low-angles.md (the fix, cheapest first); production/research/aaa-street/WINDOWS-FACADES-2026-10-04.md; WINDOWS-GRAZING-2026-10-08.md; WINDOWS-OTHER-DIRECTION-2026-10-04.md; production/cloud-week/targets/house-windows/TARGET-REVIEW.md (the fresh review of 13 October: its fixes are applied, FIXES-APPLIED.md); production/cloud-week/targets/shop-windows/TARGET.md sections 3 and 4 and TARGET-REVIEW.md (the lessons applied here); production/art/sash-window/target.json and TARGET-NOTES.md (the lab's sash, amended 8 October); tools/art-recipes/terrace-front.py (the sites, the kinds, the nets, the lit rule); tools/ue/make_interior_material.py `trace`; production/specs/shop-interiors.json; production/specs/unreal-look.json; production/specs/vignette-scene.json, vignette-pieces.json; production/research/evening-light-1990/SUMMARY-2026-09-29.md and production/research/shop-glass-reflections/NIGHT-2026-10-08.md (lit windows 6 cd/m2); RULINGS.md 3 and 8 October; production/cloud-week/HANDOVER.md.

**Libraries:** Poly Haven API (api.polyhaven.com assets and files), 13 October 2026: every model and texture named exists, CC0; the 1k base colour of each looked at (inventory).

**Not reached (nothing rests on them):** Wikimedia Commons (not asked: Geograph's feed answered); archive.org (not asked); any 1975 to 1995 night photograph of a terrace (none found: no Geograph result before 1996 for night, dusk or lit windows); any period photograph of a 1980s brown anodised aluminium house window (none among the 14 photographs; none searched by image: Geograph is searchable by words only); Epic's pages (not needed: the engine facts come from the repository's notes).

## 3. The method, in the game's own numbers

### 3.1 Why the windows read as white boards, and what the photographs say

Research 1a found the cause: the pane was a pale lit card (not glass over a dark room), the box was lit flat with no dark lines, and the upper panes reflected no shapes. This unit builds 1a's fix as numbers a builder can follow (sections 5 and 6). **What the photographs add** (14 photographs, 1979 to 1994; 18 windows measured, section 3.2, the way the gate measures): at 15 to 40 degrees from the wall the real windows are not uniformly dark. A window with a net reads **0.90 to 0.94** of its frame's brightness (P1, three windows at 31 to 39 degrees, boxed without the white-painted stone head and sill and without the brick column, L taken over the joinery); a window with bare glass and a dark room reads **0.18 to 0.36**; seen nearly square from below, glass over a dark room under a blue sky reads **0.49 to 0.59** (P8; **0.57** for all four panes together, blue over red 48). The white-board fault is therefore not 'a pane as bright as its frame' but **a pane that is one even tone with no dark line round it**: the old build's pane read 157 to 175 against paint 178 to 205 (0.85) with no corner line (D/L 0.85, a spread of 14 levels), where the photographs' tight outlines read D/L 0.52 to 0.71 (P1_a with its top rows out 0.71) and a pane spread of 64 to 109 levels. **The first version of these numbers measured the stone and the brick, not the frame:** it boxed the white-painted stone head and sill and a column of brick into P1's outlines, so L read 233 to 245 (the stone's paint reads 248 to 254) and D/L 0.47 to 0.50 (the brick's own 119 over the stone). Measured the way the gate measures, the same photographs would have failed WB-04 and WB-01's median cap; this is the review's fault 2 and the first lesson at the top of this page. The checks of section 9 test the lines and the spread by window state (bare, net, draped), not one pane ratio.

### 3.2 What was measured on the photographs (Photo)

The pane-to-frame measurements on the photographs (Photo kind). Each window: an outline box (jamb to jamb, head to sill top), the pane boxes (the glass or net inside the sash), its state, and the proportion w/h its true window would have (0.50 for the period sash; 0.33 for P9's tall arched ones). Luma is sRGB-coded 0.2126 R + 0.7152 G + 0.0722 B (1a's measure).  MEASURED THE WAY THE GATE MEASURES (TARGET-REVIEW of 13 October, fault 2; TARGET.md section 9): P = the pane boxes' median; L = the 90th percentile of the OUTLINE MINUS THE PANE BOXES (the joinery: the stile, rail and lining pixels, no brick, no stone); D = the outline's 5th percentile (joinery and pane together, no brick); spread = the pane's 95th minus 5th percentile. The first version of this file took L over the whole outline and drew P1's outlines to include the white-painted stone head and sill and a column of brick at the jamb: that made L 233 to 245 (the stone's paint, 248 to 254) and D/L 0.47 to 0.50 (the brick's own 119 over the stone), neither of which the gate can read off a render. P1_a, P1_b and P1_e are now boxed without the stone and the brick; the other outlines are as they were and a few still include the dark reveal or a little stone at their edge, so for them D is a floor (and L, now taken from the joinery alone, is a little nearer the frame's own luma). The angle from the wall is estimated from the window's apparent proportion: sin(angle) = (w_app / h_app) / a_true; its error is +-5 degrees (the true proportion varies 0.40 to 0.62 between windows). The outline boxes are by eye on the photographs' own pixels (hw_photos.PHOTOS ids). P1_c's frame is dark brown and its outline still includes the white stone head and sill: its L is the stone's paint, so its row reads a bare dark room against white, as the bare band wants (fault 1's amendment makes every street frame white or cream: the bands apply to white and cream frames only).

**P1_a, P1_b and P1_e** (the three net windows that set the bands) are boxed as the review boxes them: P1_a outline (435, 396, 451, 447) and pane (437, 399, 449, 444); P1_b outline (405, 402, 418, 452) and pane (406, 405, 417, 449); P1_e the same way, from 5 rows under the stone head's end to the stone sill's start (outline (435, 489, 451, 540), pane (437, 492, 449, 537)); P1_a is also given with its top three rows out (outline (435, 399, 451, 447), pane (437, 402, 449, 444): P/L 0.94, D/L 0.71, spread 68). The first version's boxes (P1_a (433, 392, 451, 455), P1_b (403, 396, 419, 458), P1_e (433, 485, 451, 545)) are kept in `photo_measurements.boxes_of_the_first_version` with their old figures. The angle from the wall is now taken from the tight boxes (31 to 39 degrees, inside the +-5 degrees of the method).

| window | photo | state | angle from wall (deg, +-5) | L (p90) | P (median) | D (p5) | P/L | D/L | pane spread | what |
|---|---|---|---|---|---|---|---|---|---|---|
| P1_a | P1 | net_full | 38.9 | 215.9 | 201.3 | 139.7 | 0.932 | 0.647 | 76.1 | upstairs, white frame, white voile both sashes; boxed without the stone head and sill and without the brick column (the review's box) |
| P1_b | P1 | net_full | 31.3 | 218.7 | 204.5 | 141.7 | 0.935 | 0.648 | 64.1 | upstairs, white frame, white voile; boxed without the stone and the brick (the review's box) |
| P1_c | P1 | bare_dark | 22.2 | 247.4 | 73.0 | 27.3 | 0.295 | 0.111 | 102.0 | upstairs, dark-brown frame, bare glass, dark room (the outline still includes the white stone: see the note at the top) |
| P1_e | P1 | net_full | 38.9 | 215.3 | 193.1 | 111.4 | 0.897 | 0.517 | 109.0 | ground, white frame, voile on the lower sash and the upper sash clear and dark; boxed the same way as P1_a: from 5 rows under the stone head's end (y 484) to the stone sill's start (y 540), jamb to jamb (x 435 to 450) |
| P4_C | P4 | net_full | 68.5 | 254.0 | 247.0 | 36.0 | 0.972 | 0.142 | 173.0 | upstairs, full white net (black and white print) |
| P4_G | P4 | bare_dark | 46.0 | 223.0 | 41.0 | 2.0 | 0.184 | 0.009 | 208.0 | ground, bare, the room black, a pot plant |
| P4_E | P4 | net_half | 35.1 | 220.0 | 122.0 | 31.0 | 0.555 | 0.141 | 148.8 | ground, a net over the lower half |
| P3_a | P3 | net_full | 90.0 | 177.2 | 105.6 | 5.4 | 0.596 | 0.03 | 130.9 | upstairs, cream frame, lower sash voile, near square |
| P3_b | P3 | net_full | 61.5 | 177.8 | 162.0 | 38.0 | 0.911 | 0.214 | 113.2 | upstairs, red-brown frame, voile |
| P3_c | P3 | net_full | 51.3 | 168.0 | 124.7 | 26.5 | 0.742 | 0.158 | 116.0 | ground, red-brown frame, voile |
| P3_d | P3 | bare_dark | 90.0 | 170.8 | 60.7 | 12.0 | 0.356 | 0.07 | 148.9 | ground, cream frame, bare lower sash, dark room, near square |
| P3_e | P3 | net_full | 64.8 | 210.3 | 167.4 | 32.2 | 0.796 | 0.153 | 150.1 | ground, white frame, voile |
| P3_f | P3 | net_full | 61.8 | 207.5 | 190.6 | 32.5 | 0.918 | 0.157 | 96.0 | upstairs, white frame, voile |
| P9_a | P9 | glass_bright | 29.8 | 213.5 | 155.0 | 62.8 | 0.726 | 0.294 | 105.6 | tall sash in shade, panes pale (sky), bars as dark lines |
| P9_b | P9 | glass_bright | 28.7 | 217.3 | 166.3 | 58.5 | 0.765 | 0.269 | 120.3 | tall sash in shade |
| P9_c | P9 | glass_bright | 33.3 | 253.7 | 251.9 | 96.1 | 0.993 | 0.379 | 138.8 | tall sash in sun, panes bright |
| P6_up | P6 | glass_sky_room | 90.0 | 253.9 | 225.4 | 72.2 | 0.888 | 0.285 | 174.9 | replacement window: sky in the top light, dark room and a net edge below |
| P8_L | P8 | glass_dark_room | 90.0 | 171.9 | 101.2 | 93.5 | 0.589 | 0.544 | 19.4 | original 2/2, near square from below, panes blue-grey over a dark room |
| P8_R | P8 | glass_dark_room | 90.0 | 178.0 | 86.8 | 83.3 | 0.488 | 0.468 | 52.7 | original 2/2, near square from below |

| state | n | P/L range | P/L median | D/L median | angles |
|---|---|---|---|---|---|
| bare_dark | 3 | 0.18 to 0.36 | 0.29 | 0.07 | 22.2, 46.0, 90.0 |
| glass_bright | 3 | 0.73 to 0.99 | 0.77 | 0.29 | 28.7, 29.8, 33.3 |
| glass_dark_room | 2 | 0.49 to 0.59 | 0.54 | 0.51 | 90.0, 90.0 |
| glass_sky_room | 1 | 0.89 to 0.89 | 0.89 | 0.28 | 90.0 |
| net_full | 9 | 0.60 to 0.97 | 0.91 | 0.16 | 31.3, 38.9, 38.9, 51.3, 61.5, 61.8, 64.8, 68.5, 90.0 |
| net_half | 1 | 0.56 to 0.56 | 0.56 | 0.14 | 35.1 |

Brick beside the windows: median luma 119.1 in P1 and 92.1 in P8; the frame's linear brightness over the brick's is **3.75 in P1 and 4.1 in P8**: frames are about 4 times the wall on a photograph (film contrast included; L is now the joinery's 90th percentile); the concept sheet's 7 is outside it (D9). The game's albedos give 0.82 / 0.13 = 6.3.

**Nets, curtains, blinds** (a hand count of every window whose state could be read, 60 windows in P1, P2, P3, P4, P6, P7, P12; Photo ±8 points): lower sash voile 28 (47%), full height net 13 (22%), cafe net 1 (2%), curtains drawn or open 6 (10%), blind 1 (2%), bare dark room 11 (18%). A net is a lower-sash voile in nearly half the windows and the upper sash is then clear: the room shows through it. The two held net pictures of the street (net_curtain_a, _b: a coarse square mesh of 7 to 10 mm, mean alpha 0.53, over the whole pane) match none of them (D2). **Paint** (60 windows, by eye): white 55%, cream or ivory 12%, dark or red-brown 13%, olive green 7%, blue 8%.

**What the photographs show in each window, element by element** (the list the build is judged against): the white frame member at each jamb 37 to 47 mm on a rear (P8) and 76 to 79 mm on a front (the lab's P6); a meeting rail that reads 34 mm of face and more with its shade (P8: 62 mm with the underside); a glazing bar of 22 to 27 mm (P8: 27 ±6); panes that differ from one another by up to 10 per cent in brightness (P8: four panes, mean luma 86 to 105) and are smooth inside (P8: three of the four flat to 1.4 levels over the central 60 per cent of the box); a dark edge between frame and net where the net hangs back from the glass (P1, P4); the near jamb's dark reveal beside a white lining at 10 to 20 degrees (P1, P13); a white painted sill and head in stone (P1, P3, P4); at under 10 degrees a white slit beside a dark void (P13). The nets: a gathered voile on the lower sash only with a lace band at the foot (P6, P7, P12), the upper sash clear, a full-height net on the tall windows (P4, P3), vertical louvres (P2, P11). P14 (boarded houses) shows plywood in the openings and no nets: the empty flat's torn, yellowed net (section 6) is a Judgement, not a photograph's.

### 3.3 The game's rule for a room behind a house window

**The rule** (production/specs/shop-interiors.json, `tools/ue/make_interior_material.py` `trace`, imported by `hw_common.py` and never rewritten): on the room's centre line, d in front of the card plane, a camera frames the card rectangle W x H exactly; a room point (x, y, z) lands at u = 0.5 + (x / W) d / (d + y), v = 0.5 + (z / H - 0.5) d / (d + y). The material finds for each pixel where the eye's ray meets the room's box behind the card and looks that point up in the picture. d = W for every room here, as for the shops.

**The card is the room's front wall, not the window's glass.** The shops' card is the glass rectangle. A house window is a small hole (0.85 m) in the front wall of a room 2.8 or 3.4 m wide; a box as small as the hole would be a corridor. So the card here is **the whole room's front plane, 0.270 m behind the brick face**: the wall (215 mm of brick, the kit's box to 250.8) hides every part of the card outside the opening; the eye sees the room through the hole. 0.270 is 16 mm behind the nets (254) and 80 mm behind the lower glass (190); a ray through the window meets the card plane displaced sideways by 0.08 m x tan(angle off the normal), 0.30 m at 15 degrees from the wall, so every window stands at least 0.3 m inside its card (checked). The card's front face must not stand in front of the kit's box (250.8) and the carcass behind it starts at 0.29 or more.

| room family | W x H x D (m) | camd | floor above crown | window above the floor | picture | back wall in the picture (px, x0 y0 x1 y1) | who |
|---|---|---|---|---|---|---|---|
| UP (a first-floor room: one window centred in it; the flat's bay split in two rooms of 2.8 m) | 2.8 x 2.55 x 4.2 | 2.8 | 3.75 | 0.4736 to 2.15 | 1536 x 1399 | [460.8, 419.7, 1075.2, 979.2] | the 14 upper windows |
| GF (a cottage's front room: both windows look into the one room, 1.8 m apart) | 3.4 x 2.6 x 4.2 | 3.4 | 0.45 | 0.3736 to 2.05 | 3072 x 2349 | [848.8, 649.1, 2223.2, 1700.1] | the 6 cottage windows |

**Where the floors are** (Derived): a first-floor floor stands 0.25 above the shop's ceiling (3.5 above the crown: 3.4 + 0.1) at 3.75 and the ceiling at the eaves, 6.3; so the sill is 0.4736 above the floor and the head 2.15, leaving the 0.4 m of wall `head_below_ceiling_m` the scene file gives. A cottage's floor stands 0.35 above the footway (0.45 above the crown) and its ceiling at 3.05, under the eaves at 3.1 (Judgement).

**Why the pictures are 1536 wide (upper rooms) and 3072 wide (cottage rooms).** The window shows 0.85 / 2.8 = 30 per cent of an upper room's picture and 0.85 / 3.4 = 25 per cent of a cottage's. An upper window is never nearer than 2.6 m (standing 0.8 m out from the wall, the sill 2.5 m above the eye): a screen pixel is 2.3 mm at the game's 60 degrees over 1440 lines, the glass (0.78 m) about 340 pixels wide, over 427 texels at 1536 (548 a metre): 1.3 texels a pixel, sharp. From across the street (8.8 m, 39 degrees) it is 180 pixels over the same 427. A cottage's window is met at eye level, as near as 1.5 m from the glass (as the shops' honest range: nearer than that the nets, a real card, and the glass's own Fresnel carry the view): a pixel is 1.2 mm, the glass 650 pixels wide, over 704 texels at 3072 (903 a metre): 1.1 texels a pixel, just sharp; at 2048 it would be 1.4 pixels a texel and soft. The sizes are Derived; the picture heights follow from the card's proportions (1399 and 2349).

**What can be painted on a surface** (the third failure of 3 October, answered). An object painted on a surface that stands off it by s metres slides, as the eye moves, by the angle between the eye's ray to the object and to its painted place. `hw_common.budgets_for` computes, for the review cameras below and both mirror images of each pavement position, the greatest stand-off at which the slide stays within 20 pixels (reads true) and 40 pixels (tolerated) of a 2560 x 1440 frame, at the points the window actually shows (144 rays through the glass), the 15th percentile of the points, the smallest over the cameras. **The eye stands by the window**, as the camera table says (the fixes of 13 October, narrow point 1: the first version stood every cottage eye at the card's centre, 0.9 m from its window, which over-stated the back wall's budget, 0.41 against 0.38), the mirror image is taken about the window, and one pixel is the exact angle at the frame's centre, atan(tan(vfov / 2) / 720), not vfov / 1440 (4 per cent small at 39 degrees, 10 per cent at 60):

| family | surface | reads true (20 px), m | tolerated (40 px), m |
|---|---|---|---|
| UP | back | 0.617 | 1.203 |
| UP | side | 0.036 | 0.072 |
| UP | ceiling | 0.034 | 0.067 |
| UP | floor | not seen from the street | not seen from the street |
| GF | back | 0.387 | 0.723 |
| GF | side | 0.035 | 0.068 |
| GF | ceiling | 0.024 | 0.048 |
| GF | floor | 0.022 | 0.043 |

**The rule the rooms keep** (the smaller of the two families' figures, rounded down; `rooms.budget_rule`): back 0.380 true, 0.710 tolerated; side 0.030 true, 0.060 tolerated; ceiling 0.020 true, 0.040 tolerated; floor 0.018 true, 0.037 tolerated. (An upper room's floor is never seen from the street; the cottages' floor figure stands. The back wall's 0.38 and 0.71 are the review's own, from its slide measure; this unit's recomputation gives 0.387 and 0.723, so the rule is the smaller, as the others are. A cottage's back wall seen from H_UNDER, 0.8 m from the wall and looking up, is the binding view.) Anything that would stand further off its surface is not drawn in the picture: a bed, a table, a free-standing chair are dropped; a chimney breast, a radiator, a stair's stringer are drawn flat (`rooms.forms`). **A pendant light's shade is the one real object in a lit room** (kit node `pendant__shade`), because it is what a lit upstairs window shows. The checks PIC-05 and the self-check test every object's and every form's stand-off against these numbers.

**What shows of a room, and so where its picture needs detail** (`rooms.visible_zone`, computed; metres in the picture frame, x from the PICTURE-LEFT WALL (not from the room's centre: the objects' x_across is from the centre, so add half the room's width to compare), y back from the card, z up from the floor; the eye stands by the window, as the camera table says):

- UP from H_ACROSS_0: the back wall (x 0.84 to 1.96, z 1.78 to 2.41); the ceiling (x 0.84 to 1.96, y 0.85 to 4.16)
- UP from H_ACROSS_30: the left wall (y 1.55 to 3.22, z 1.01 to 2.54); the ceiling (x 0.02 to 1.26, y 0.85 to 2.95)
- UP from H_ALONG_15_NEAR: the left wall (y 0.18 to 0.46, z 0.97 to 2.54); the ceiling (x 0.01 to 1.21, y 0.08 to 0.41)
- UP from H_ALONG_30_NEAR: the left wall (y 0.47 to 1.1, z 1.41 to 2.55); the ceiling (x 0.0 to 1.53, y 0.08 to 1.21)
- UP from H_ALONG_15_ROAD: the left wall (y 0.18 to 0.42, z 0.79 to 2.55); the ceiling (x 0.04 to 0.76, y 0.2 to 0.36)
- UP from H_UNDER: the ceiling (x 0.73 to 2.07, y 0.0 to 0.66)
- GF from H_ACROSS_0: the back wall (x 2.04 to 3.16, z 0.02 to 2.37)
- GF from H_ACROSS_30: the back wall (x 0.12 to 0.67, z 0.02 to 2.37); the left wall (y 3.48 to 4.16, z 0.02 to 2.36)
- GF from H_ALONG_15_NEAR: the left wall (y 0.52 to 0.84, z 0.02 to 2.43); the floor (x 0.01 to 0.3, y 0.75 to 0.75)
- GF from H_ALONG_30_NEAR: the left wall (y 1.14 to 2.13, z 0.02 to 2.59); the floor (x 0.05 to 1.84, y 0.75 to 1.61); the ceiling (x 0.02 to 1.2, y 1.23 to 1.72)
- GF from H_ALONG_15_ROAD: the left wall (y 0.51 to 0.78, z 0.16 to 2.24)
- GF from H_UNDER: the back wall (x 0.55 to 3.11, z 0.18 to 2.47); the right wall (y 0.99 to 3.05, z 0.1 to 2.49); the floor (x 1.04 to 3.38, y 0.39 to 2.94); the ceiling (x 1.06 to 3.38, y 0.67 to 2.89)

An upper room is seen from the street as its ceiling and the top 0.6 m of its back wall (from across) or the first 0.5 m of one side wall (along the street, near): so its picture's detail is ceiling, cornice, picture rail, wall tops and tall furniture tops; a cottage's front room is seen at eye level: the whole back wall and the side walls.

**The review cameras** (street frame; eye 1.60 above the footway = 1.70 above the crown; 2560 x 1440): 

| camera | where | vertical field (deg) |
|---|---|---|
| H_ACROSS_0 | from the far pavement's kerb edge, square on to the window | 39.0 |
| H_ACROSS_30 | from the far pavement's kerb edge, 30 degrees off the window's normal toward the quay end | 39.0 |
| H_ALONG_15_NEAR | on the house's own footway 1.5 m from the wall, the window seen 15 degrees from the wall (5.6 m along) | 46.0 |
| H_ALONG_30_NEAR | on the house's own footway 1.5 m from the wall, the window seen 30 degrees from the wall (2.6 m along) | 46.0 |
| H_ALONG_15_ROAD | in the road, 1 m out from the kerb (2.6 m from the wall: the footway is 5.125 - 3.505 = 1.62 m wide), the window seen 15 degrees from the wall (9.7 m along) | 39.0 |
| H_UNDER | 0.8 m from the wall, directly below the window (looking up) | 60.0 |

H_ACROSS_0 stands on the far pavement's kerb edge (8.8 m from the glass: the brief's 'about 8 m' is the nearest the far pavement allows); H_ALONG_15_NEAR and H_ALONG_30_NEAR are on the house's own footway 1.5 m from the wall, 5.6 and 2.6 m short of the window, which is the angle where 1a found the white boards; H_ALONG_15_ROAD is 9.7 m along from 2.6 m out: in the road, 1 m out from the kerb (the footway is 5.125 - 3.505 = 1.62 m wide); H_UNDER is 0.8 m from the wall, looking up. For the cottages the far pavement is the east footway.

## 4. The kinds

### 4.1 Two over two (S22) and one over one (S11): the lab's checked sash, reused

The sash is the lab's, amended on 8 October for Jafar's ruling (`production/art/sash-window/target.json`, models `production/assets/sash-window/sash_window.glb` and `sash_window_1over1.glb`, reviewed on narrow points). Nothing is redrawn: this unit changes its glass (section 5), shades its box (5.4), adds its nets and its room (6, 7), and applies it to every row. **Numbers read from the lab's file** (the self-check re-reads them): opening 850.0 x 1676.4; frame reveal 114.3; outer lining margin 42.9 (so each jamb shows 3 in of painted timber, 76.2); head visible 44.5; stile 50.8, top rail 50.8, bottom rail 101.6, meeting rail 38.1 deep, glazing bar 22.2 (one vertical bar in each sash of the S22; none on the S11), sash thickness 34.9, horns 76.2 long on the upper sash only, glass 2.5 thick.

**Glass planes** (Read from the lab's glb; 1a): the upper glass 142.0 mm behind the brick face, the lower 190.0. The sill: an oak sill 41.3 high at the front; the stone sill and the segmental arch belong to the wall kit (stone sill 127 high, 50.8 proud, 76.2 wider than the opening each side; the arch ring 215, rise one seventh of the span, 12 proud: terrace-front.py). **Horns:** ogee horns on the upper sash's stiles (76.2 below the meeting rail), none on the lower. **Reveal:** the brick reveal is half a brick, 102.5 (the street file), the lab's frame stands 114.3 back from the face.

The lab's kit has **41 nodes** in the S22 (1068 triangles, 72988 bytes) and 35 in the S11 (860 triangles). Each node's bounds in the kit frame are in `kinds.S22.lab_nodes` and `kinds.S11.lab_nodes` (the self-check re-reads the glb and compares). **Photographs win** where they disagree with the book: the lab already followed P6 for the frame; P8 reads the bar at 27 ±6 (22.2 kept, D6), the jamb of a rear at 37 to 47 mm (the front's 76.2 kept, D7) and the meeting rail with its shade at 62 mm (38.1 kept, D10).

### 4.2 Paint, colour and condition by house

| paint | sRGB | linear | roughness | note |
|---|---|---|---|---|
| white_fresh | [234, 233, 229] | [0.82, 0.812, 0.78] | 0.42 | the street's paint_joinery as it stands (terrace-front.py MATERIALS) and the lab sash's paint: the kit pieces' default; sound gloss white: east_parade_bay1 and west_south_bay2 take it as it is (the box shade's keep_paint rule applies to this paint only) |
| white_grimy | [214, 212, 205] | [0.68, 0.66, 0.62] | 0.48 | weathered 1990 gloss white, 1a's 0.72 to 0.80 less the dirt in the lower rails and the sill: the lower rail and sill at x 0.85, the rest 1.0; east_parade_bay0, east_parade_bay5 and west_south_bay0 |
| white_flaking | [205, 202, 192] | [0.6, 0.58, 0.53] | 0.55 | east_parade_bay3's paint (the unlet house): 12 per cent of the area on the lower rails, sill and stiles' feet is flaked to grey primer (66, 60, 54) or bare timber (96, 66, 40) |
| cream | [222, 204, 164] | [0.73, 0.6, 0.37] | 0.45 | NOT USED ON ANY HOUSE until Jafar's page rules otherwise (his ruling of 3 October is white frames; D13). Kept as data for the photographs' mix: P3's cream-painted sashes (frame sampled 181, 163, 131 in the sun and shade of the photograph, so the paint is lighter), P2's cream render |
| olive | [136, 140, 64] | [0.246, 0.262, 0.052] | 0.45 | NOT USED ON ANY HOUSE until Jafar's page rules otherwise (D13). Kept as data: P12's two olive-green sashes (sampled 148, 153, 70); a painted window of a house that chose its own colour |
| blue | [56, 92, 160] | [0.04, 0.107, 0.352] | 0.42 | NOT USED ON ANY HOUSE until Jafar's page rules otherwise (D13). Kept as data: P2's blue sashes (sampled 61, 87, 136), the tenants' own paint on a terrace of one owner |
| brown | [84, 58, 42] | [0.089, 0.042, 0.023] | 0.42 | NOT USED ON ANY HOUSE until Jafar's page rules otherwise (D13). Kept as data: P1's four dark-brown sashes and P3's red-brown frames (sampled 141, 131, 115 and 162, 129, 119 in the sun): an oxide or brown gloss, the second commonest painted colour after white |
| bronze | [74, 60, 52] | [0.05, 0.038, 0.03] | 0.35 | NOT USED ON ANY HOUSE until Jafar's page rules otherwise (D13: the question of the chandler's bronze is on that line). The street's frame_bronze (terrace-front.py): dark anodised aluminium; NOT seen in any reached photograph (D1) |
| white_upvc | [232, 231, 225] | [0.8, 0.792, 0.762] | 0.3 | white replacement frame, satin: P6, P7, P11 show white in every case (4 of 4); the four replacement houses (east_parade_bay2, east_parade_bay4, west_south_bay1, east_chandler_bay0) |

| house | kind | paint | condition |
|---|---|---|---|
| east_chandler_bay0 | RC | white_upvc | sound |
| east_parade_bay0 | S22 | white_grimy | grimy |
| east_parade_bay1 | S11 | white_fresh | sound |
| east_parade_bay2 | RC | white_upvc | sound |
| east_parade_bay3 | S22 | white_flaking | flaking |
| east_parade_bay4 | RC2 | white_upvc | sound |
| east_parade_bay5 | S11 | white_grimy | sound |
| west_south_bay0 | S11 | white_grimy | grimy |
| west_south_bay1 | RC | white_upvc | sound |
| west_south_bay2 | S22 | white_fresh | sound |

**Every house is white** (the review's fault 1). Jafar's ruling of 3 October is 'windows with white frames, sash bars, sky in the glass', and the approved Hook sheet is recorded the same way ('every upstairs window is PALE - white frames over white nets'). The first version of this target gave five houses coloured frames (brown, olive, blue, cream, bronze) from the photographs' tally; the review found that against his ruling, with no question put to him. **The ruling stands over the tally until he answers on his page** (OWED-05, first line; D13; CLAUDE.md: if code must change a ruling, ask him first). The ten houses: white_flaking 1 (east_parade_bay3); white_fresh 2 (east_parade_bay1, west_south_bay2); white_grimy 3 (east_parade_bay0, east_parade_bay5, west_south_bay0); white_upvc 4 (east_chandler_bay0, east_parade_bay2, east_parade_bay4, west_south_bay1). The cream, olive, blue, brown and bronze paints stay in the table above as unused data for his answer. **What the photographs say, for his page:** white paint is 55 per cent of the 60 windows; cream or ivory 12, dark brown or red-brown 13, blue 8, olive 7 (a council terrace painted by its tenants: P2). The 1980s and 1990s replacement is white in every photograph reached (P6, P7, P11): the brown or bronze anodised frame the street file draws for every replacement is in none of them (D1), and the first version's bronze chandler is on the same question to Jafar, not decided here. A council replacement in the photographs is the Newburn casement (P11): a fixed light under a top-hung light, white, with nets and vertical drapes: the RC kind; P6's replacement is the other form (RC2, section 4.3). **Condition:** `sound` is the paint as in the table; `grimy` multiplies the lower rail and sill by 0.85 and darkens the box's inside corners (the shade already does it) with a grime band 30 mm high along the sill; `flaking` (the unlet flat): 12 per cent of the area on the lower rails, the sill and the stiles' feet is flaked to grey primer (66, 60, 54) or bare timber (96, 66, 40).

### 4.3 The replacement casements: RC (P7's form) and RC2 (P6's form)

**RC (P7's and P11's form):** a fixed light under a top-hung light, no bars, in the same 850 x 1676.4 opening (the street's `REPLACEMENT_TRANSOM` 0.72 and the photographs' 0.66 (P6), 0.72 (P7), 0.75 (P11): the street's value stands). **One transom and equal lights** (unit 7's toplight fault does not arise: there are no bars, one transom, and the top light is a single pane). The parts, in the kit frame (mm): frame face 60, depth 70, front 72.5 behind the brick face (the reveal's 102.5 less 30 proud); transom face 70, centred at 1207.0 above the opening's bottom; the top-hung light's sash stiles 45 with a 4 dark gap; glass 4 mm (a sealed unit drawn as one pane, section 5.5) at 112.5 behind the face; a gasket line 3 wide at luma x 0.30 and a welded-corner groove 2 wide at x 0.35 at each corner of each sash.

| part | x (mm) | y into the wall (mm) | z up (mm) | material |
|---|---|---|---|---|
| frame_jamb_L | [-425.0, -365.0] | [72.5, 142.5] | [60.0, 1616.4] | paint |
| frame_jamb_R | [365.0, 425.0] | [72.5, 142.5] | [60.0, 1616.4] | paint |
| frame_sill_rail | [-425.0, 425.0] | [72.5, 142.5] | [0, 60.0] | paint |
| frame_head_rail | [-425.0, 425.0] | [72.5, 142.5] | [1616.4, 1676.4] | paint |
| transom | [-365.0, 365.0] | [72.5, 142.5] | [1172.0, 1242.0] | paint |
| vent_sash_stile_L | [-361.0, -316.0] | [80.5, 135.5] | [1246.0, 1612.4] | paint |
| vent_sash_stile_R | [316.0, 361.0] | [80.5, 135.5] | [1246.0, 1612.4] | paint |
| vent_sash_bottom_rail | [-316.0, 316.0] | [80.5, 135.5] | [1246.0, 1291.0] | paint |
| vent_sash_top_rail | [-316.0, 316.0] | [80.5, 135.5] | [1567.4, 1612.4] | paint |
| glass_lower | [-383.0, 383.0] | [112.5, 116.5] | [42.0, 1190.0] | glass_house |
| glass_top | [-334.0, 334.0] | [112.5, 116.5] | [1273.0, 1585.4] | glass_house |

Glass sightlines (width x height, mm): lower 730.0 x 1112.0, top 632.0 x 276.4. The top light is hinged at its head and opens outward in the photographs (P11, P14: one stands open): a closed light is drawn; the open one is a variant the PC may add (not required).

**RC2 (P6's form, added by the fixes of 13 October: narrow point 7).** P6 (Levenshulme, 1994) shows a replacement with a fixed top light across the whole width over two lower lights: a side-hung casement beside a fixed light, the mullion near the middle. RC is P7's form only, so the street's replacement houses were all identical; RC2 is built for east_parade_bay4 (both windows). Same opening, frame section (face 60, depth 70, front 72.5 behind the brick face), glass plane (112.5) and white upvc as RC. **Parts** (kit frame, mm): the transom's face is 70, centred at 0.66 x 1676.4 = 1106.4 above the opening's bottom (P6's 0.66); the top light is one fixed pane; a 70 mm mullion is centred at x 0 from z 60 (the sill rail's top) to 1071.4 (the transom's underside); the left light is a side-hung casement, its stiles and rails 45 with a 4 mm gap all round and the hinge on the jamb side (the left jamb); the right light is fixed. The two lower lights' openings are equal, 330.0 x 1011.4 each. **Glass sightlines** (width x height, mm): casement [232.0, 913.4], fixed light [330.0, 1011.4], top light [730.0, 475.0]. KIT-12, KIT-14 and KIT-15 cover RC2 as they cover RC.

| part | x (mm) | y into the wall (mm) | z up (mm) | material |
|---|---|---|---|---|
| frame_jamb_L | [-425.0, -365.0] | [72.5, 142.5] | [60.0, 1616.4] | paint |
| frame_jamb_R | [365.0, 425.0] | [72.5, 142.5] | [60.0, 1616.4] | paint |
| frame_sill_rail | [-425.0, 425.0] | [72.5, 142.5] | [0.0, 60.0] | paint |
| frame_head_rail | [-425.0, 425.0] | [72.5, 142.5] | [1616.4, 1676.4] | paint |
| transom | [-365.0, 365.0] | [72.5, 142.5] | [1071.4, 1141.4] | paint |
| mullion | [-35.0, 35.0] | [72.5, 142.5] | [60.0, 1071.4] | paint |
| casement_stile_L | [-361.0, -316.0] | [80.5, 135.5] | [64.0, 1067.4] | paint |
| casement_stile_R | [-84.0, -39.0] | [80.5, 135.5] | [64.0, 1067.4] | paint |
| casement_bottom_rail | [-316.0, -84.0] | [80.5, 135.5] | [64.0, 109.0] | paint |
| casement_top_rail | [-316.0, -84.0] | [80.5, 135.5] | [1022.4, 1067.4] | paint |
| glass_casement | [-334.0, -66.0] | [112.5, 116.5] | [91.0, 1040.4] | glass_house |
| glass_fixed | [17.0, 383.0] | [112.5, 116.5] | [42.0, 1089.4] | glass_house |
| glass_top | [-383.0, 383.0] | [112.5, 116.5] | [1123.4, 1634.4] | glass_house |

### 4.4 Sills, heads and arches, and what the kit does not carry

The stone sill (127 high, 50.8 proud, 76.2 wider each side than the opening), the segmental arch (ring 215, rise one seventh, 12 proud) and the brick returns of the reveal are the wall kit's, not this unit's; this target names the shade the wall kit must give the returns (section 5.4). **Brick returns**: 0.8 of the wall's value at the face falling to 0.6 at the sash, 0.7 under the head.

### 4.5 Nothing left open

Every opening is covered above and around its parts: the opening is 850 x 1676.4 and the frame's outer lining runs 65 mm beyond it each side behind the brick (S22/S11), or the jambs of RC and RC2 fill it to the brick (60 face); the head is the lab's head lining (S22/S11) or the RC's head rail; nothing is left bare between the head and the stone arch (the arch's soffit and the brick return are the wall kit's, as the shopfront's were), and between the sill and the oak sill the sash's bottom rail runs to the stone sill. The self-check KIT rows confirm that every pane and every net lies inside the opening and that no RC member overlaps another; the drawing (target_drawing.py) shows the opening covered.

## 5. The glass: the 1a fix as numbers

### 5.1 The pane

**The game's pane:** One opaque Default Lit material on the pane (research 1a, step 1): base colour = lerp(room 0.03, lace x 0.6, the net's alpha) with the alpha WIRED; Specular 1.0 (F0 0.08, standing for both faces of a single pane); roughness 0.03; metallic 0; day emissive 0. The pane is a real glass surface: its reflectance and roughness are the game's. **What the cloud render uses to stand in for it:** Cycles Principled BSDF, NOT Glass BSDF: Base Color 0.03 (linear grey) with the net card's alpha as the mix, Specular IOR Level 1.0, Roughness 0.03, Transmission 0, Metallic 0, the room card (baked through `trace`) as Emission x (1 - Fresnel) x brightness; the opposite row and the sky dome are what it reflects (Cycles traces them; Lumen's reflections and the box-projected street cube are the game's).

**Two-face reflectance of float glass** (n 1.52, unpolarised, the reflections between the faces counted: Derived, recomputed by the self-check; 1a's table is 0.02 to 0.03 higher at 16 to 30 degrees) by the angle from the wall: 90 degrees 0.082, 30 degrees 0.157, 24 degrees 0.215, 18 degrees 0.314, 16 degrees 0.360, 10 degrees 0.544, 8 degrees 0.622. Unreal's Specular 1 (F0 0.08, Schlick) gives 0.26 at 16 degrees from the wall, about three quarters of the true two-face figure (0.36): close enough.

### 5.2 Old glass's waviness

Per-pane tilt, not a wave texture: each pane mesh is rotated by a seeded angle uniform in +-0.5 degrees about the vertical axis and +-0.3 degrees about the horizontal one (never zero, the spread of a window's panes at least 0.3 degrees). **Photographs:** P8 (Oxford rear, 1987): the four panes of the two windows measured (the boxes of section 3.2) read mean luma 86, 100, 100 and 105 (19 levels apart, 18 per cent of the brightest); inside, three are flat to 1.2 to 1.4 levels (the central 60 per cent of the box) and the fourth, the right window's upper pane, carries a brighter patch (95th percentile 176): the glass is flat to the eye and each pane catches the sky differently. No wave normal map: the glass looks flat on the photographs.

### 5.3 Dirt and reflections

A 6 mm band round every pane's edge is roughened (roughness 0.35, base colour x 0.8): the putty line's dirt; the lowest 25 mm of each pane carries the same (water and dust on the bottom rail). **Reflections by floor.** Upper panes: from across the street a ray off an upper pane goes up at the eye's own elevation (18 to 22 degrees) and meets only sky (the west row's roofs are 3 m eaves; the ray is 9 m up by the west frontage): the pane carries the SKY at 8 per cent and the room at 92 per cent; P8 (blue-grey 87, 99, 135) shows it. Ground panes: a ground pane across the street reflects the opposite row at eye height: the parade's dark fascias and the hill's trees: a darker band; the room dominates.

### 5.4 The box shaded and its dark lines drawn

1a step 2 as numbers, put in the joinery's vertex colour (COLOR_0 red channel multiplies the paint; not the AO pin). Numbers (1a step 2, Judgement from 1a's photograph-9 figures; the check KIT-09 reads them back from the exported file):

| part | red channel of COLOR_0 (x paint) | note |
|---|---|---|
| faces whose normal points to the street | 1.0 (not darkened) | faces whose normal points to the street (the outer lining's street face at y 114.3, the sash rails' fronts, the sill's top) take 1.0: they are L itself, and darkening them would darken the frame the gate measures (TARGET-REVIEW narrow point 4) |
| the faces that run into the wall: the reveal-facing sides of the linings, the beads, the pulley stiles and the sash stiles | 1.0 at y = 0 falling linearly to 0.6 at the glass plane | the sash's own lining and the outer lining's face |
| the track faces | 0.5 | the faces of the pulley-stile track between the parting bead and the staff bead |
| inside corners | 0.3 within 8 mm of a concave edge | photograph 9's corner line 105 to 125 against a lining of 220 to 250 |
| the putty and shadow line round each pane | 0.35, 6 mm wide | the kit's putty strips (14 on a 2/2) are 6.4 mm wide: painted 0.35 |
| the meeting rail's underside | 0.4 | the lower rail of the upper sash seen from below |
| the parting bead's gap | 0.10 over 6 mm | the gap itself is a 2 mm geometric gap |
| the brick returns of the reveal (wall kit) | 0.6 to 0.8 | in the wall mesh, not the kit; stated so the wall kit takes it: 0.8 at the face falling to 0.6 at the sash, and 0.7 under the head |

**The paint:** only the sound gloss white (`white_fresh`, east_parade_bay1 and west_south_bay2) keeps 1a's albedo [0.78, 0.8] and roughness 0.40 (try 0.35 once: a traced sheen); every other house takes its own paint from the `paints` table, which governs (white_grimy is 0.66 at roughness 0.48, for example), not this line (the review's narrow point 4). **Every dark line of the box is at least 6 mm wide** (1 pixel at 10 m is 5.9 mm at 1440 lines and 46 degrees): the lab's putty strips are 6.4 wide, the parting bead's gap is 2 mm but its shade is painted over 6 mm each side, the RC's gasket and weld groove are shaded over 6 mm. Check KIT-10.

### 5.5 What this cannot reach

The real sealed unit of the replacement reflects from four faces (about 0.14 at normal incidence); Unreal's Specular 1.0 caps at F0 0.08, so the replacement's pane under-reflects; and the game's own reflections (Lumen, the box-projected street cube, the Fresnel hand-over) are not in the cloud. Both are in `could_not_settle` and `owed_on_pc`.

## 6. Nets, curtains and blinds

All are **cards** (two triangles each) behind the glass, in front of the room's card; their alpha is the weave. Planes are in millimetres behind the brick face; z is up from the opening's bottom edge. The two held net pictures (`net_curtain_a`, `_b`: a coarse square mesh of 7 to 10 mm, mean alpha 0.53) match none of the photographs' nets and are not used (D2).

| net | name | what | card (mm) | plane (mm behind the face) | voile coverage | lace band share of height | share of the photographs' windows |
|---|---|---|---|---|---|---|---|
| N0 | bare glass | no net: the room is seen (dark by day) | - | - | - | - | 18% |
| N1 | lower-sash voile | a gathered voile on a wire at the meeting rail, hem near the sill; the upper sash clear | x -450 to 450, z 60 to 880 | S22/S11 254, RC 235 | 0.4 | 0.3 | 47% |
| N2 | full-height net | a gathered net from a rod at the head to a hem near the sill | x -450 to 450, z 60 to 1630 | S22/S11 254, RC 235 | 0.4 | 0.18 | 22% |
| N3 | cafe net | a half-height net on a rod across the lower sash: covers the lower third of the window only | x -430 to 430, z 100 to 500 | S22/S11 254, RC 235 | 0.45 | 0.0 | 2% |

**The fabric** (all nets):

- **Weave:** Plain voile: threads under 1 mm, a pitch of 1.2 mm, so under one pixel from 1.5 m outwards: the net reads as an even translucent sheet with fold shading; only the lace band shows a pattern (repeat 60 mm) and only from under 3 m.
- **Layers and coverage:** One layer covers 0.40 (voile) to 0.62 (lace band) of its area; gathered at 200 per cent fullness the folds overlap so the mean covered share of the sheet is 1 - (1 - 0.40)^2 = 0.64 voile, 0.86 lace band (Derived); the card's alpha is the weave and folds.
- **Gathering:** At 200 per cent fullness, fold wavelength 40 to 55 mm, depth 12 mm (a normal and brightness map, not geometry), brightness modulation +-22 per cent.
- **Hem:** A lace border 28 mm high, scalloped, period 35 mm; the hem sags up to 12 mm between folds (the lower edge is a gentle sine of amplitude 6 mm and wavelength 90 mm).
- **Head:** A 20 mm double-thickness casing at the top (alpha 0.92) with a 2 mm dark wire line under it (alpha 0.5, luma 60).
- **Colours** (sRGB): white (238, 238, 232), greyed (208, 208, 200), and yellowed by nicotine (222, 206, 158). P1 sampled a sunlit white net at (208, 201, 181); nets read 0.60 to 0.97 of the frame's luma in the photographs (n=9).
- **By day:** Lit from outside by daylight: albedo x lit by the street's sky and the window's own shadow; the net is NOT emissive by day (net_day_gain 0.0, unreal-look.json).
- **Night, lit:** Emissive warm tungsten: linear (1.0, 0.714, 0.344) (vignette-pieces window_practicals gamma (1, 0.86, 0.62); the street's interior_lit) x the lit-net strength 1.2 x room_glow_gain_night 0.4 = 0.48 (unreal-look.json); folds darker, the room's pendant and furniture seen through it.
- **Night, dark:** Unlit: net emissive 0.05 x 0.4 = 0.02 (the street's NET_EMIT_NIGHT 0.05): only the sodium lamp's colour on its fabric.
- **Parallax:** A net 65 mm behind the glass moves under a pixel at 10 m (1a): a flat card, not geometry.

| kind | name | what | card (mm) | plane | opacity | folds or slats | colours | night, lit |
|---|---|---|---|---|---|---|---|---|
| C1 | curtains drawn | lined curtains drawn across the whole window, in front of the net | x -480 to 480, z 0 to 1780 | 262 | 0.97 | wavelength 70 to 90 mm, brightness modulation 0.25, straight hem, a pelmet band 60 mm high at the top | cream (214, 198, 166), brown (110, 82, 62), green (72, 98, 74) | colour x warm light x 0.35 transmission: the curtain glows its own colour, folds dark |
| C2 | curtains open | a pair drawn back to the sides, two cards each 170 wide | left: x -480 to -310, z 0 to 1780; right: x 310 to 480, z 0 to 1780 | 262 | 0.97 | as C1 | cream (214, 198, 166), brown (110, 82, 62), green (72, 98, 74), floral cream (224, 210, 180) | as C1 |
| B1 | venetian blind | a white aluminium venetian blind lowered 60 per cent of the height (z 660 to 1650), slats 25 mm, tilted closed 70 per cent | x -400 to 400, z 660 to 1650 | 240 | slat gaps alpha 0.25 | slat pitch 25 mm | (210, 210, 205) | slat gaps glow warm: stripes of light at the 25 mm pitch (visible under 8 m) |
| B2 | roller blind | a cream roller blind half down (z 700 to 1660) with a pull cord and a 20 mm bottom batten | x -390 to 390, z 700 to 1660 | 240 | 0.9 | a plain sheet | (226, 214, 176) | an even warm sheet of colour x 0.5 transmission, a dark bottom batten |
| B3 | vertical louvre blind | white vertical louvres 89 mm, turned 40 per cent open (P2's ground window) | x -420 to 420, z 100 to 1640 | 240 | slat gaps alpha 0.35 | slat pitch 89 mm | (226, 226, 220) | vertical stripes of warm light at the 89 mm pitch |

**Per house** the street's mix is in the table of section 1 (net kind and colour, drape): the upper sash is clear wherever the net is N1, N3 or none, so the room shows through it; a torn yellowed net hangs askew in the empty flat (one lower corner off its wire, the hem 80 mm out of true: a Judgement). **Drawn curtains** stand in front of the net and cover the window; open curtains stand 170 mm wide at each side. A lit room behind a lit net reads as the net's own glow (emissive 0.48) with the room's pendant and the top of the back wall seen through it.

## 7. The rooms behind the windows

### 7.1 The format

Each room is built by script from CC0 models in Blender (Cycles), rendered to the shop rooms' picture format: <room_id>_<state>.png with <room_id>.json beside them (room, w, h, d, camera_d, pixels, states, made_by, samples); 8-bit sRGB PNG; Cycles 128 samples, denoised; masters on F:/LedgerTools/house-rooms. Three states: `day`, `night_lit`, `night_dark`. The render camera stands on the room's centre line d = W in front of the card, framing the card rectangle W x H exactly; the game's `trace` is imported, not rewritten. **Brightness** (the game's emissive scale): Day 0.12 (a front room by day is a dim ceiling and a dark wall; the shops' 0.15 is for a lit display), night 0.7 as the shops (shop-interiors.json); the pane composite measured in the gate decides. **Picture standards** (Judgement): mean luma day 105, night_lit 70, night_dark 15, within ±15 per cent. Scaled from the approved pawnbroker pictures (119.5, 79.8, 17.7 measured 12 October) by the rooms' smaller windows and fewer lights: the checks' floors are 0.7 of these.

**Lights per state.** Day: an overcast area light the size of the card on its plane (6500 K), strength set so the picture's mean luma meets the day standard; no tungsten. Night, lit: the pendant (a paper shade, a 60 W tungsten bulb 2700 K, linear (1.0, 0.714, 0.344)) at the ceiling rose, 0.30 below the ceiling, and in the front rooms a table lamp's glow on the back wall; a television glow (cool 6500 K, emissive screen) where tv_glow; landings and empty rooms: a bare 40 W bulb or none (empty: night_lit = night_dark); a lit landing's emission is the absolute one of `landing_bulb`. Night, dark: the sodium wash through the window: linear (1.0, 0.25, 0.0) = production/specs/unreal-look.json lantern_linear_rgb (NOT the scene file's stale (1, 0.7055, 0)), at 6 per cent of night_lit's energy; nothing else.

### 7.2 The thirteen rooms

**Variants so a row does not repeat visibly:** three lounges, three bedrooms, two landings, two empty rooms, three cottage front rooms; no (room, net, drape) triple repeats within three places on a row (checked); the three lounges and the three bedrooms differ in their walls and in their back-wall pieces (checked).

| room | type | W x H x D (m) | walls / ceiling / floor | objects (class, stand-off m) | scripted flat forms | light | picture px |
|---|---|---|---|---|---|---|---|
| up_lounge_1 | lounge | 2.8 x 2.55 x 4.2 | wallpaper_floral / ceiling_white / boards | wooden_bookshelf_worn (tolerated 0.58), ornate_mirror_01 (true 0.03), hanging_picture_frame_03 (tolerated 0.03) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_lounge_2 | lounge | 2.8 x 2.55 x 4.2 | emulsion_magnolia / ceiling_white / boards | vintage_cabinet_01 (tolerated 0.67), mantel_clock_01 (tolerated 0.67), hanging_picture_frame_01 (true 0.02) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_lounge_3 | lounge | 2.8 x 2.55 x 4.2 | wallpaper_stripe / ceiling_white / carpet_brown | Shelf_01 (true 0.26), hanging_picture_frame_02 (true 0.03), wall_clock (tolerated 0.05) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_bedroom_1 | bedroom | 2.8 x 2.55 x 4.2 | wallpaper_floral / ceiling_white / carpet_brown | vintage_cabinet_01 (tolerated 0.67), hanging_picture_frame_03 (true 0.03) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_bedroom_2 | bedroom | 2.8 x 2.55 x 4.2 | emulsion_cream / ceiling_white / boards | wooden_bookshelf_worn (tolerated 0.58), ornate_mirror_01 (true 0.03), hanging_picture_frame_01 (true 0.02) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_bedroom_3 | bedroom | 2.8 x 2.55 x 4.2 | wallpaper_stripe / ceiling_white / carpet_brown | Shelf_01 (true 0.26), hanging_picture_frame_03 (true 0.03), wall_clock (tolerated 0.05) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_landing_1 | landing | 2.8 x 2.55 x 4.2 | emulsion_pale_green / ceiling_white / lino | hanging_picture_frame_01 (true 0.02), wall_clock (true 0.05) | skirting, picture_rail, coving, stair_flat, internal_door_flat, bare_bulb | bare bulb | 1536 x 1399 |
| up_landing_2 | landing | 2.8 x 2.55 x 4.2 | emulsion_cream / ceiling_white / lino | Shelf_01 (true 0.26), hanging_picture_frame_02 (true 0.03) | skirting, picture_rail, coving, radiator_flat, bare_bulb | bare bulb | 1536 x 1399 |
| up_empty_1 | empty | 2.8 x 2.55 x 4.2 | stripped_paper / ceiling_white / boards | none | skirting, coving, chimney_breast_flat, bare_bulb, picture_ghost | bare bulb | 1536 x 1399 |
| up_empty_2 | empty | 2.8 x 2.55 x 4.2 | peeling_paint / ceiling_white / boards | none | skirting, coving, bare_bulb, radiator_flat | bare bulb | 1536 x 1399 |
| gf_front_1 | front_room | 3.4 x 2.60 x 4.2 | wallpaper_floral / ceiling_white / carpet_brown | Sofa_01 (tolerated 0.66), side_table_01 (tolerated 0.45), television_02 (tolerated 0.45), hanging_picture_frame_02 (true 0.03), hanging_picture_frame_03 (tolerated 0.03) | skirting, picture_rail, coving, ceiling_rose, fire_surround_flat | pendant | 3072 x 2349 |
| gf_front_2 | front_room | 3.4 x 2.60 x 4.2 | emulsion_magnolia / ceiling_white / boards | wooden_bookshelf_worn (tolerated 0.58), painted_wooden_bench (tolerated 0.50), potted_plant_01 (tolerated 0.64), ornate_mirror_01 (true 0.03) | skirting, picture_rail, coving, ceiling_rose, internal_door_flat | pendant | 3072 x 2349 |
| gf_front_3 | front_room | 3.4 x 2.60 x 4.2 | wallpaper_stripe / ceiling_white / carpet_brown | painted_wooden_cabinet (tolerated 0.62), mantel_clock_01 (tolerated 0.62), vintage_oil_lamp (tolerated 0.62), painted_wooden_bench (tolerated 0.50), hanging_picture_frame_01 (true 0.02) | skirting, picture_rail, coving, ceiling_rose, fire_surround_flat | pendant | 3072 x 2349 |

**Finishes** (Poly Haven textures at 1k, tinted; roughness in words and 0-1): emulsion_magnolia: matt magnolia emulsion (linear [0.6, 0.52, 0.38], roughness 0.8); emulsion_cream: matt cream emulsion (linear [0.66, 0.6, 0.42], roughness 0.8); emulsion_pale_green: pale green emulsion (a landing) (linear [0.4, 0.48, 0.36], roughness 0.8); wallpaper_floral: a damask-pattern paper from the jacquard texture tinted fawn (linear [0.42, 0.33, 0.26], roughness 0.7); wallpaper_stripe: a script-drawn vertical stripe: cream and fawn, 90 mm period (linear [0.55, 0.5, 0.36], roughness 0.7); stripped_paper: old paper stripped in strips, bare plaster between (linear [0.3, 0.27, 0.22], roughness 0.9); peeling_paint: paint peeling to grey plaster (linear [0.38, 0.22, 0.2], roughness 0.9); ceiling_white: white emulsion on a textured ceiling, yellowed by tobacco in the lived-in rooms (x 0.92) (linear [0.72, 0.7, 0.64], roughness 0.9); boards: dark-stained floorboards (linear [0.2, 0.12, 0.06], roughness 0.6); carpet_brown: a worn brown carpet tinted from the dirty-carpet texture (linear [0.12, 0.08, 0.05], roughness 0.95); lino: brown linoleum (a landing) (linear [0.3, 0.2, 0.1], roughness 0.5).

**Scripted flat forms** (every one inside the budgets of its surface): skirting: painted white, on all three walls; picture_rail: a 40 mm timber rail painted white round the side and back walls at 2.15 m, 0.02 proud, with a dark shade line under it; coving: a cove drawn as a 55 mm band shaded like a cove, 0.02 proud (a real 55 mm cove is over the ceiling budget); ceiling_rose: a plaster rose at the pendant's place: tolerated class on the ceiling (0.03 over 0.02, under 0.04); bare_bulb: a flat glowing disc (a pendant of bare bulb on its flex: the flex is not drawn); fire_surround_flat: a tiled fire surround drawn flat (the real one stands 0.18 off the wall: over the budget); internal_door_flat: a four-panel internal door, panels 0.02 proud; radiator_flat: a pressed-steel radiator drawn flat (the real one stands 0.08 off: over the budget); stair_flat: the stringer and handrail of the flight along the side wall drawn as flat strips (the handrail 0.9 to 1.0 above the nosings, rising 36 degrees); balusters not drawn; chimney_breast_flat: a chimney breast drawn flat (the real one stands 0.23 off the wall); picture_ghost: a pale rectangle on a stripped wall where a picture hung (painted, no stand-off).

**What each type shows from the street.** *Upper lounges and bedrooms*: the ceiling with its rose, cove and pendant, the wall tops under the picture rail, the tops of tall furniture, a picture hung high; at night, a warm ceiling and the shade. *Landings*: the stair's flat stringer and handrail up the side wall, a half-glazed door at the back, a bare bulb. *Empty rooms*: stripped paper or peeling paint, a flat chimney breast, a pale ghost where a picture hung, bare boards, a bare bulb flex; by night they are dark whatever the table says. *Cottage front rooms*: eye-level: sofa or armchair against the back wall, a cabinet with a clock and a lamp, the television on a small table (a cool glow at night in front room 1), pictures, a fire surround drawn flat.

### 7.3 Which windows are lit at night

Judgement. The research file production/research/evening-light-1990 gives no share (its windows line: 'whitish fluorescent from shops, warm tungsten behind house curtains', marked its own inference); the street already lights one in three at 20:30 (terrace-front.py NET_LIT_EVERY = 3) and two cottage windows always (NET_LIT_ALWAYS). No 1975 to 1995 night photograph of a terrace was reached (no Geograph result before 1996 for night, dusk or lit windows). Kept near the street's one in three; the rest of the day follows habit (lights on at dusk, out by midnight).

| hour | share of the 20 windows | windows lit |
|---|---|---|
| 05:00 | 0.05 | 1 |
| 06:00 | 0.10 | 2 |
| 07:00 | 0.15 | 3 |
| 08:00 | 0.05 | 1 |
| 17:00 | 0.05 | 1 |
| 18:00 | 0.15 | 3 |
| 19:00 | 0.30 | 6 |
| 20:00 | 0.35 | 7 |
| 20:30 | 0.35 | 7 |
| 21:00 | 0.35 | 7 |
| 22:00 | 0.30 | 6 |
| 23:00 | 0.20 | 4 |
| 00:00 | 0.10 | 2 |
| 01:00 | 0.05 | 1 |

A window is lit at hour h when its place in the lit order is below round(share(h) x 20); the order is fixed (below) and never reshuffled, so a window lit at 23:00 is lit at 20:30; empty rooms are never lit; the two cottage windows of the always-lit house are lit from 18:00 to 23:00 whatever the share. THE ORDER (TARGET-REVIEW narrow point 6, Judgement): in 1990 the evening's light is in the front room or the lounge and a landing is lit briefly; after the always-lit pair: the cottage front room west_south_bay1_gf_w1, then the three lounges, then a bedroom (the chandler's), then the other cottage front rooms, then the other bedrooms, then the landings. The review's text names east_chandler_bay0_upper_w1 as the fifth, but that window is a landing (up_landing_2, as the review's own fault text says): the chandler's bedroom window, _w0, stands there. **At 20:30, seven lit (35 per cent):** east_chandler_bay0_upper_w0, east_parade_bay0_upper_w1, east_parade_bay2_upper_w0, east_parade_bay5_upper_w0, west_south_bay1_gf_w1, west_south_bay2_gf_w0, west_south_bay2_gf_w1. **The fixed lit order** (after the always-lit pair): west_south_bay1_gf_w1 > east_parade_bay0_upper_w1 > east_parade_bay2_upper_w0 > east_parade_bay5_upper_w0 > east_chandler_bay0_upper_w0 > west_south_bay1_gf_w0 > west_south_bay0_gf_w1 > west_south_bay0_gf_w0 > east_parade_bay1_upper_w1 > east_parade_bay4_upper_w0 > east_parade_bay0_upper_w0 > east_parade_bay1_upper_w0 > east_parade_bay2_upper_w1 > east_parade_bay4_upper_w1 > east_parade_bay5_upper_w1 > east_chandler_bay0_upper_w1. No window is lit by day; a lit room by day would be invisible in the glass's reflection.

### 7.4 The inventory

**44 Poly Haven models were looked at at 1k (base colour map, 13 October); 16 are used in the rooms; 9 textures.** Every id exists in the live catalogue (`self_check.py --live` re-reads it) and is CC0. A mark found on a map is blanked (painted out to the surface's own colour) before the model is used, or the model is not used; every framed picture's artwork is replaced by a script-drawn print (flat grey-green landscape band under a pale sky, no text). Never used: `fancy_picture_frame_02` (its painting shows a group of figures including children).

| model | dims mm (x y z) | polycount | used in | status | marks seen at 1k |
|---|---|---|---|---|---|
| ArmChair_01 | [848.4, 765.8, 1065.1] | 5626 | - | looked at, not used | none; 0.77 deep, over the tolerated back-wall budget of 0.71 once the cottage eye stands at the window: NOT USED (painted_wooden_bench serves in gf_front_2) |
| CoffeeTable_01 | [1540.0, 972.8, 523.2] | 10404 | - | looked at, not used | none; free-standing: NOT USED |
| Shelf_01 | [1003.4, 257.0, 2080.3] | 182 | up_bedroom_3, up_landing_2, up_lounge_3 | none | none |
| Sofa_01 | [1571.5, 658.0, 796.5] | 4101 | gf_front_1 | none | none |
| Television_01 | [600.0, 470.8, 456.8] | 1918 | - | looked at, not used | 'VTECH' logo on the front panel, a 'WARNING' label, a 'TRRA' plate: painted out to the case's grey; NOT USED (television_02 serves) |
| WoodenChair_01 | [688.2, 658.5, 2273.5] | 19992 | - | looked at, not used | none; free-standing: NOT USED |
| alarm_clock_01 | [227.7, 168.4, 174.2] | 13006 | - | looked at, not used | none (a plain dial with numerals) |
| book_encyclopedia_set_01 | [551.3, 163.1, 237.4] | 67306 | - | looked at, not used | spines read 'ENCYCLOPEDIA' and volume letters: a generic word, no firm; NOT USED in a room |
| ceramic_vase_01 | [204.9, 206.4, 401.4] | 2548 | - | looked at, not used | a barcode sticker on the body: painted out; NOT USED in a room (ceramic_vase_03 clean)  |
| ceramic_vase_03 | [112.5, 112.5, 414.4] | 2784 | - | none (looked at; in no room) | none seen |
| desk_lamp_arm_01 | [617.3, 408.0, 879.0] | 25710 | - | looked at, not used | a small label reading 'MAX 15W' on the base: blanked; NOT USED (the rooms' lamps are the pendant and the oil lamp) |
| dining_chair_02 | [433.6, 576.4, 973.4] | 22013 | - | looked at, not used | none; free-standing: NOT USED |
| dining_table | [2255.9, 1390.2, 877.0] | 1048 | - | looked at, not used | none; free-standing: NOT USED |
| drawer_cabinet | [1141.1, 488.1, 1881.3] | 26406 | - | looked at, not used | a 2010s piece (a black steel frame with open oak shelves and drawers); its navy side strip carries three rows of faint lettering-like marks (the review of 13 October; the writer's entry said none): NOT USED (wooden_bookshelf_worn serves in up_bedroom_2) |
| fancy_picture_frame_01 | [603.0, 20.0, 464.1] | 938 | - | looked at, not used | artwork is a landscape painting with tiny riders: NOT USED (the frames above are enough) |
| fancy_picture_frame_02 | [660.6, 89.0, 771.0] | 35102 | - | excluded: children | artwork is a street scene painting with a group of figures including children: NEVER USED (content rule: no children, even painted) |
| hanging_picture_frame_01 | [594.0, 15.7, 841.0] | 2586 | gf_front_3, up_bedroom_2, up_landing_1, up_lounge_2 | replace_artwork | artwork map reads 'Ray Homes / Photo: 76cm x 51cm / Frame: 84cm x 59cm' (a maker's name): the whole artwork map is REPLACED by a script-drawn print (a flat grey-green landscape band under a pale sky), no text |
| hanging_picture_frame_02 | [751.8, 33.1, 500.0] | 3678 | gf_front_1, up_landing_2, up_lounge_3 | replace_artwork | artwork map is a painting of a palace signed 'Celine.F' (an artist's signature and a royal building): REPLACED by a script-drawn print |
| hanging_picture_frame_03 | [385.0, 31.8, 502.4] | 24348 | gf_front_1, up_bedroom_1, up_bedroom_3, up_lounge_1 | replace_artwork | artwork map is a photograph of a Japanese castle (not 1990 Britain): REPLACED by a script-drawn print |
| mantel_clock_01 | [483.7, 250.8, 160.9] | 29742 | gf_front_3, up_lounge_2 | none | none (a plain dial) |
| modern_wooden_cabinet | [2440.0, 520.0, 680.1] | 24976 | - | looked at, not used | none; a modern piece: NOT USED |
| old_bed_frame | [904.7, 2001.7, 1201.5] | 49990 | - | looked at, not used | none; its headboard is under the visible zone: NOT USED |
| ornate_mirror_01 | [486.5, 26.0, 744.2] | 14246 | gf_front_2, up_bedroom_2, up_lounge_1 | none | none |
| painted_wooden_bench | [1164.9, 496.5, 889.3] | 630 | gf_front_2, gf_front_3 | none | none (looked at again at 1k on 13 October after the fix) |
| painted_wooden_cabinet | [1194.7, 616.6, 1181.9] | 2227 | gf_front_3 | none | none (knobs only) |
| potted_plant_01 | [588.9, 636.6, 1350.8] | 96030 | gf_front_2 | none | none |
| potted_plant_02 | [701.2, 657.4, 841.2] | 69806 | - | looked at, not used | none |
| round_wooden_table_01 | [1399.3, 1399.3, 1005.0] | 8640 | - | looked at, not used | none; free-standing: NOT USED |
| side_table_01 | [550.0, 450.0, 550.7] | 2756 | gf_front_1 | none | an ornamental gold script-like band on the top edge of the map: decoration, no text read; kept |
| small_wooden_table_01 | [916.2, 440.0, 533.1] | 3410 | - | looked at, not used | none; free-standing: NOT USED |
| sofa_02 | [1807.2, 817.8, 709.5] | 2728 | - | looked at, not used | none; 0.818 deep, over the tolerated back-wall budget: NOT USED |
| sofa_03 | [2731.2, 925.1, 1118.3] | 8004 | - | looked at, not used | none (a cushion pattern square); 1.12 deep: NOT USED |
| standing_picture_frame_01 | [200.8, 100.3, 249.7] | 1634 | - | looked at, not used | artwork is a modern canal photograph with a car of the 2010s: NOT USED |
| standing_picture_frame_02 | [216.9, 102.3, 266.4] | 2986 | - | looked at, not used | artwork is a beach scene with small figures: NOT USED |
| television_02 | [399.7, 350.2, 411.4] | 2310 | gf_front_1 | blank | a small rating plate on the back panel; 'PARAGON Viewing System' on the front bezel, left of the buttons: both painted out to the bezel's grey (map at 1k, about x 272 to 300, y 450 to 560, lettered at 90 degrees: found by the review of 13 October; the first look had missed it) |
| throw_pillows_01 | [1021.6, 627.5, 450.2] | 6362 | - | looked at, not used | none |
| vintage_cabinet_01 | [2021.8, 669.8, 2235.1] | 61096 | up_bedroom_1, up_lounge_2 | none | none (a cream paper sheet with a hexagon pattern on map a) |
| vintage_day_bed | [1972.6, 854.8, 1127.3] | 2715 | - | looked at, not used | none; 0.855 deep: NOT USED |
| vintage_oil_lamp | [220.0, 220.0, 801.6] | 7208 | gf_front_3 | none | none |
| vintage_suitcase | [1608.2, 239.2, 567.9] | 16474 | - | looked at, not used | the second suitcase's map carries about a dozen travel stickers (real places or lines): NOT USED |
| vintage_wooden_drawer_01 | [1715.1, 1006.9, 1090.8] | 5184 | - | not used | not looked at (1.0 deep: over budget) |
| wall_clock | [320.5, 47.2, 320.5] | 3658 | up_bedroom_3, up_landing_1, up_lounge_3 | blank | 'URBAN quartz' on the dial: painted out to the dial's white (a maker's name) |
| wicker_basket_01 | [383.2, 295.0, 117.4] | 22276 | - | looked at, not used | none |
| wooden_bookshelf_worn | [1374.0, 581.3, 2063.4] | 10106 | gf_front_2, up_bedroom_2, up_lounge_1 | none | none (looked at again at 1k on 13 October after the fix) |

**Textures** (1k base colour looked at, no marks seen): ceiling_interior, decrepit_wallpaper, dirty_carpet, floral_jacquard, linoleum_brown, old_wooden_floor_02, painted_plaster_wall, peeling_painted_wall, plastered_wall_04. **Brand blocklist** (the self-check scans every string of target.json outside a marks entry for these): paragon, dixons, currys, comet, rumbelows, vtech, ray homes, celine, lorex, ingrid, radolier, hotpoint, kenwood, ekco, anglian, royal mail, post office, tesco, woolworth, sainsbury, ikea, dulux. Every model's base colour map was looked at at 1k on 13 October 2026 before it was named; a model with a mark is blanked in its map (the mark painted out to the surface's own colour) before it is used, or not used; every framed picture's artwork is replaced by a script-drawn print; the base colour of every placed model is checked region by region against its marks entry before its room is rendered (PIC-07). The first look missed television_02's maker's name on its front bezel: the placed models' maps were looked at again at 100 per cent after the review (FIXES-APPLIED.md).

## 8. As kit pieces

**Frame and pivot.** Kit frame (units): x across the window, y into the wall (0 at the brick face), z up (0 at the opening's bottom edge); the lab glb's frame is glTF y-up with the wall at negative z: kit (x, y, z) = (x_glb, -z_glb, y_glb). The opening's bottom-edge centre on the brick face: (0, 0, 0); the street toward -y; z up; metres, scale 1.

**Placement.** East: translate (x_centre, +5.125, sill_z_above_crown); the street is at -y, no turn. West: turn 180 degrees about z, then translate (x_centre, -5.125, sill_z_above_crown). Height: above the road's crown, the site's `sill_z_above_crown` (the opening's bottom edge); the stone sill and the arch ring belong to the wall kit.

**Files:**

- S22: `production/assets/cloud-week/house-windows/hw_S22.glb`
- S11: `production/assets/cloud-week/house-windows/hw_S11.glb`
- RC: `production/assets/cloud-week/house-windows/hw_RC.glb`
- RC2: `production/assets/cloud-week/house-windows/hw_RC2.glb`
- room_card_gf: `production/assets/cloud-week/house-windows/hw_room_card_gf.glb` (the cottages' shared room card, one per house, placed between its two windows)

**Budget:** 6000 triangles and 400000 bytes each. The lab's 2/2 is 1068 triangles and 72988 bytes; nets, curtains and blinds are cards (2 triangles each); the push guard allows 1 MB a model in git.

**S22: added nodes** (the lab's 41 nodes are reused as they are; the RC's parts are in section 4.3):

| node | material | x (mm) | y into the wall (mm) | z up (mm) | note |
|---|---|---|---|---|---|
| glass__lower_L | glass_house | -357.3 to -4.7 | 189.6 to 192.1 | 134.4 to 835.6 | the lab's glass sheet split at the bar: each pane runs to the bar's fillet (4.7 from the middle, the putty's inner edge), 2.5 thick |
| glass__lower_R | glass_house | 4.7 to 357.3 | 189.6 to 192.1 | 134.4 to 835.6 | as `glass__lower_L` |
| glass__upper_L | glass_house | -357.3 to -4.7 | 142.0 to 144.5 | 856.7 to 1608.7 | as `glass__lower_L` |
| glass__upper_R | glass_house | 4.7 to 357.3 | 142.0 to 144.5 | 856.7 to 1608.7 | as `glass__lower_L` |
| net__N1 | net_voile | -450 to 450 | 254 to 255 | 60 to 880 | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N2 | net_voile | -450 to 450 | 254 to 255 | 60 to 1630 | as `net__N1` |
| net__N3 | net_voile | -430 to 430 | 254 to 255 | 100 to 500 | as `net__N1` |
| curtain__C1_drawn | curtain | -480 to 480 | 262 to 263 | 0 to 1780 | drawn across; colour per house |
| curtain__C2_open_L | curtain | -480 to -310 | 262 to 263 | 0 to 1780 | drawn back, left |
| curtain__C2_open_R | curtain | 310 to 480 | 262 to 263 | 0 to 1780 | drawn back, right |
| blind__B1 | blind | -400 to 400 | 240 to 241 | 660 to 1650 | venetian blind |
| blind__B2 | blind | -390 to 390 | 240 to 241 | 700 to 1660 | roller blind |
| blind__B3 | blind | -420 to 420 | 240 to 241 | 100 to 1640 | vertical louvre blind |
| pendant__shade | pendant_shade | -170 to 170 | 650 to 990 | 1536 to 1776 | a paper shade 340 across and 240 high, 0.55 behind the card, its top 0.30 below the ceiling; emissive only in a lit room; present where the room's `pendant` is true; the one real object in the room (the picture's ceiling carries its rose) |

**S11: added nodes** (the lab's 35 nodes are reused as they are; the RC's parts are in section 4.3):

| node | material | x (mm) | y into the wall (mm) | z up (mm) | note |
|---|---|---|---|---|---|
| glass__lower | glass_house | -357.3 to 357.3 | 189.6 to 192.1 | 134.4 to 835.6 | the lab's sheet, one pane a sash |
| glass__upper | glass_house | -357.3 to 357.3 | 142.0 to 144.5 | 856.7 to 1608.7 | the lab's sheet, one pane a sash |
| net__N1 | net_voile | -450 to 450 | 254 to 255 | 60 to 880 | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N2 | net_voile | -450 to 450 | 254 to 255 | 60 to 1630 | as `net__N1` |
| net__N3 | net_voile | -430 to 430 | 254 to 255 | 100 to 500 | as `net__N1` |
| curtain__C1_drawn | curtain | -480 to 480 | 262 to 263 | 0 to 1780 | drawn across; colour per house |
| curtain__C2_open_L | curtain | -480 to -310 | 262 to 263 | 0 to 1780 | drawn back, left |
| curtain__C2_open_R | curtain | 310 to 480 | 262 to 263 | 0 to 1780 | drawn back, right |
| blind__B1 | blind | -400 to 400 | 240 to 241 | 660 to 1650 | venetian blind |
| blind__B2 | blind | -390 to 390 | 240 to 241 | 700 to 1660 | roller blind |
| blind__B3 | blind | -420 to 420 | 240 to 241 | 100 to 1640 | vertical louvre blind |
| pendant__shade | pendant_shade | -170 to 170 | 650 to 990 | 1536 to 1776 | a paper shade 340 across and 240 high, 0.55 behind the card, its top 0.30 below the ceiling; emissive only in a lit room; present where the room's `pendant` is true; the one real object in the room (the picture's ceiling carries its rose) |

**RC: added nodes** (the RC has no lab model: its frame parts are the table in section 4.3; these are its glass, nets, drapes, blinds and pendant):

| node | material | x (mm) | y into the wall (mm) | z up (mm) | note |
|---|---|---|---|---|---|
| glass__lower | glass_house | -383.0 to 383.0 | 112.5 to 116.5 | 42.0 to 1190.0 | 4 mm, one pane drawn for the sealed unit |
| glass__top | glass_house | -334.0 to 334.0 | 112.5 to 116.5 | 1273.0 to 1585.4 | 4 mm, one pane drawn for the sealed unit |
| net__N1 | net_voile | -450 to 450 | 235 to 236 | 60 to 880 | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N2 | net_voile | -450 to 450 | 235 to 236 | 60 to 1630 | as `net__N1` |
| net__N3 | net_voile | -430 to 430 | 235 to 236 | 100 to 500 | as `net__N1` |
| curtain__C1_drawn | curtain | -480 to 480 | 262 to 263 | 0 to 1780 | drawn across; colour per house |
| curtain__C2_open_L | curtain | -480 to -310 | 262 to 263 | 0 to 1780 | drawn back, left |
| curtain__C2_open_R | curtain | 310 to 480 | 262 to 263 | 0 to 1780 | drawn back, right |
| blind__B1 | blind | -400 to 400 | 240 to 241 | 660 to 1650 | venetian blind |
| blind__B2 | blind | -390 to 390 | 240 to 241 | 700 to 1660 | roller blind |
| blind__B3 | blind | -420 to 420 | 240 to 241 | 100 to 1640 | vertical louvre blind |
| pendant__shade | pendant_shade | -170 to 170 | 650 to 990 | 1536 to 1776 | a paper shade 340 across and 240 high, 0.55 behind the card, its top 0.30 below the ceiling; emissive only in a lit room; present where the room's `pendant` is true; the one real object in the room (the picture's ceiling carries its rose) |

**RC2: added nodes** (the RC2 has no lab model: its frame parts are the table in section 4.3; these are its glass, nets, drapes, blinds and pendant):

| node | material | x (mm) | y into the wall (mm) | z up (mm) | note |
|---|---|---|---|---|---|
| glass__casement | glass_house | -334.0 to -66.0 | 112.5 to 116.5 | 91.0 to 1040.4 | 4 mm, one pane drawn for the sealed unit |
| glass__fixed | glass_house | 17.0 to 383.0 | 112.5 to 116.5 | 42.0 to 1089.4 | 4 mm, one pane drawn for the sealed unit |
| glass__top | glass_house | -383.0 to 383.0 | 112.5 to 116.5 | 1123.4 to 1634.4 | 4 mm, one pane drawn for the sealed unit |
| net__N1 | net_voile | -450 to 450 | 235 to 236 | 60 to 880 | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N2 | net_voile | -450 to 450 | 235 to 236 | 60 to 1630 | as `net__N1` |
| net__N3 | net_voile | -430 to 430 | 235 to 236 | 100 to 500 | as `net__N1` |
| curtain__C1_drawn | curtain | -480 to 480 | 262 to 263 | 0 to 1780 | drawn across; colour per house |
| curtain__C2_open_L | curtain | -480 to -310 | 262 to 263 | 0 to 1780 | drawn back, left |
| curtain__C2_open_R | curtain | 310 to 480 | 262 to 263 | 0 to 1780 | drawn back, right |
| blind__B1 | blind | -400 to 400 | 240 to 241 | 660 to 1650 | venetian blind |
| blind__B2 | blind | -390 to 390 | 240 to 241 | 700 to 1660 | roller blind |
| blind__B3 | blind | -420 to 420 | 240 to 241 | 100 to 1640 | vertical louvre blind |
| pendant__shade | pendant_shade | -170 to 170 | 650 to 990 | 1536 to 1776 | a paper shade 340 across and 240 high, 0.55 behind the card, its top 0.30 below the ceiling; emissive only in a lit room; present where the room's `pendant` is true; the one real object in the room (the picture's ceiling carries its rose) |

**The room card.** Upper windows: node `room__card`, plane 270 mm behind the brick face, x -1400 to 1400, z -473.6 to 2076.4 (2.8 x 2.55 m): centred on the window; floor level 473.6 below the opening's bottom, ceiling 2076.4 above it. Cottages (glb `room_card_gf`): 3.4 x 2.6 m, centred between the house's two windows (each window's place in it is sites[].card.window_in_card_m), its floor 373.6 mm below the opening's bottom and its ceiling 2226.4 mm above it; both windows look into the same card and the same picture.

**Materials:**

- `paint_<paint name>`: Per house, colour from `paints`; roughness per paint; vertex colour R multiplies (BOX_SHADE).
- `glass_house`: The pane material (GLASS.pane): one per pane id so each pane's tilt is its own node.
- `net_voile`: Alpha-textured card: the weave and folds (NET_COMMON), colour white, greyed or yellowed per house.
- `curtain`: Colour per house (CURTAINS), folds as a normal and a brightness map, opacity 0.97.
- `blind`: Slat texture with the gap alpha (BLINDS).
- `pendant_shade`: Paper, emissive in night_lit only.
- `room_card`: Plain quad; the game's M_LedgerInterior takes CardOrigin, RoomSize, CamD, Side, three textures and Night, LitOn, Brightness: the quad has no UVs that matter.

**How a piece goes into the game** (HANDOVER.md's route, and what is different here):

- In terrace-front.py set SASH_KIT_ROWS to None (every row takes the period opening 850 x 1676.4: the cottages' sill goes to 0.8236 above the crown, 0.7236 above the threshold, the head kept at 2.5), and make `_plain_ground` follow `_window_kind` (it draws every cottage window as a 2/2 today).
- HOUSE_PANE_TRANSLUCENT stays False: the glass is the pane material, the net card behind it; the translucent pane stays the shops' only.
- Held props: one glb per kind, placed by `sites[]` (HANDOVER.md steps 1 to 4); the room pictures are rebuilt on the PC by their one command and imported as textures (sRGB, no mips below 256).
- M_LedgerInterior parameters per site from `sites[].card` (CardOrigin, RoomSize, CamD, Side) and the picture ids; Night and LitOn from the lit table; Brightness day 0.12, night 0.7.
- The wall kit takes the reveal's brick returns' shade (BOX_SHADE.brick_returns_of_the_reveal) and the carcass behind the card (its front face at 0.29 m or more).

**The room card's parameters per site** are in `sites[].card`: CardOrigin (cm: low-x corner, front y, floor z), RoomSize (cm), CamD (cm), Side (+1 east, -1 west), and the picture ids by the site's `room`. Example, `east_chandler_bay0_upper_w0`: CardOrigin [4010.0, 539.5, 375.0], RoomSize [280.0, 255.0, 420.0], CamD 280.0, Side 1, the window in the card (m): x 0.975 to 1.825, z 0.4736 to 2.15.

## 9. The gate, in the cloud (no Unreal)

What the cloud shows without Unreal: a house front built from the kit pieces, its neighbours, the opposite row as proxies, the street's lamps and sky, the room cards baked through the game's `trace`, the pane drawn as the game draws it (GLASS.pane.cloud_stand_in).

**Scene.**

- **engine:** Blender 5.2 Cycles, CPU, 2560 x 1440 (the dark lines are 6 mm: 1.4 pixel at 8.8 m; do not render smaller), 48 samples, OpenImageDenoise, Standard view transform, film not transparent.
- **opposite row proxies:** Boxes at the street file's numbers: east parade eaves 6.3 above the crown, pitch 35 degrees, depth 8; west cottages eaves 3.1 above the crown, pitch 40; the hill and sky as the dome.
- **street:** Road 6 m crowned 0.075, footways 2 m at crown + 0.10, kerb 0.125 up; the four lamp columns at x 8, 18, 28, 38 (stand-ins).
- **sky:** The overcast dome (Poly Haven belfast_open_field_2k, CC0, the scene file's own), sun off; the world's strength is calibrated so that a Lambertian grey card (albedo 0.18) facing the street reads linear 0.18 +- 0.01 (sRGB 118 +- 4) in the render's own pixels.
- **night:** Dome x 0.15 (unreal-look.json sky_seen_gain_night), the four lamps: point lights (linear (1.0, 0.25, 0.0) = lantern_linear_rgb) at 4.78 m, power set so the paving under the near lamp reads sRGB 150 +- 20; the lit windows by the table at 20:30 (`rooms.lit_share.lit_by_hour`): lit room card (night_lit picture x 0.7 x room_glow_gain_night 0.4), lit net emissive 0.48; the rest night_dark.
- **room cards:** For every window and every camera the card's emission picture is computed per pixel through `tools/ue/make_interior_material.py` `trace` (imported, not rewritten) from the room's picture and set as the card's emission; a lit room has its net and curtain cards emissive as NET_COMMON says; a dark one is lit by the sodium wash only.
- **passes:** Cycles passes: Material Index (pane = 1 glass_house, frame = 2 paint_*, net/curtain/blind = 3, brick/wall = 4, card = 5), Object Index per window (id), Z; the masks come from these, never by eye.

**House sets:**

- **GS_A:** east_parade bays 1, 2, 3 and neighbours (bay 0 and 4 as plain blocks): the S11, RC and S22 houses; the unlet house; the wall kit's brick, sills and arches (stand-ins from the street file's materials are enough).
- **GS_B:** west_south bays 0, 1, 2 (the three cottages) with the door, the plinth and the wall, and one house of the east parade opposite as proxy.

**Views:** GS_A: H_ACROSS_0, H_ACROSS_30, H_ALONG_15_NEAR, H_ALONG_30_NEAR, H_ALONG_15_ROAD by day and by night (20:30), H_UNDER by day; GS_B: from the east footway's kerb edge (H_ACROSS_0, H_ACROSS_30), and along the cottages' own footway (H_ALONG_15_NEAR, H_ALONG_30_NEAR, H_ALONG_15_ROAD), by day and by night, and H_UNDER by day; 22 renders (11 + 11).

**What is measured** (from the Material Index and Object Index passes, never by eye):

- **P:** The median sRGB luma of a window's pane pixels (material index 1 and 3 inside the window's outline: glass and net together as the eye sees them).
- **L:** The 90th percentile of the luma of the window's joinery pixels (material index 2: the sash members, linings, beads, sill).
- **D:** The 5th percentile of the luma over the window's outline (joinery and pane pixels, no brick).
- **spread:** The pane pixels' 95th minus 5th percentile.
- **angle:** The angle from the wall at which the window's centre is seen from the camera, from the scene's geometry (not from the picture).
- **window state:** Bare, net or draped (`window_states`: N0 with no curtain or blind is bare; any B1 to B3 or C1 is draped; C2 counts by its net) and its time (day, or night lit or dark).
- **line profile:** For WB-04b: a horizontal luma profile across each stile-to-pane edge (through the pane's mid-height) and a vertical profile across each rail-to-pane edge (through the pane's mid-width), the pane's edges found from the Material Index pass (pane 1 against frame 2); the dip is the darkest run of at least 1 pixel next to the edge, its value over L.
- **bands come from:** photo_measurements.bands_by_state (Photo, +-5 degrees on the angle, outlines by eye).

**Bands** (from the photographs, section 3.2; the check numbers of section 10 quote them; P is the pane median, L the frame's 90th percentile, D the outline's 5th percentile):

- **net_N1_N2_in_15_to_30_deg:** P/L 0.55 to 0.97; D/L at most 0.72; pane spread at least 40 levels. Photographs: P1_a, P1_b, P1_e at 31 to 39 degrees, boxed without the stone head and sill and without the brick column and measured the gate's way (L over the outline minus the pane boxes, D over the outline with no brick): P/L P1_a 0.93, P1_b 0.94, P1_e 0.90; D/L P1_a 0.65, P1_b 0.65, P1_e 0.52 (P1_a with its top rows out 0.71); pane spread 76, 64, 109; the nine net windows 0.60 to 0.97. No net window was measured inside WB-01's own range of 15 to 30 degrees (the three are at 31 to 39): the band is carried down to 15 to 30 as a Judgement. No median cap (the first version's cap of 0.92 would have failed the real net windows).
- **net_N1_N2_line_check:** line dip at least 1 px wide; line dip at most 0.6 of L. Photographs: 1a section 5: photograph 9's inside corner and lining edge 105 to 125 against 220 to 250 (a profile across the lining, 0.5 of L); at P1's scale (a window 15 to 18 px wide) a 6 mm line cannot be resolved, so no outline percentile there can set a limit for it. The old fault (no line, a uniform pane against the paint) has no dip and fails.
- **net_N3_cafe:** P/L 0.35 to 0.75. Photographs: P4_E (a net over the lower half, 35 degrees): 0.56.
- **bare_N0_in_15_to_30_deg:** P/L 0.1 to 0.45; pane spread at least 20 levels. Photographs: P1_c (22 degrees) 0.29; P4_G 0.18; P3_d 0.36.
- **bare_N0_over_60_deg_from_across:** P/L 0.35 to 0.7; pane blue minus red at least 10 levels. Photographs: P8_L, P8_R (near square, from below, sky over a dark room): 0.59, 0.49; all four panes together over the joinery of both windows (the gate's way) 0.57, the pane's colour (85, 100, 133): blue over red 48 (the review reads 46, a mean; both inside the band).
- **draped_any_in_15_to_30_deg:** pane spread at least 20 levels. Photographs: No band on P/L or D/L (a blind or a drawn curtain is its own sheet); the pane spread of at least 20 levels (1a section 5) is the one test.
- **old_fault_to_fail:** P/L 0.85; D/L 0.85; pane spread 14 levels. Source: 1a: pane 157 to 175 against paint 178 to 205, the lace uniform, no corner line; the checks below must fail this.

**Window states for every WB check** (the review's fault 2(b)): **bare**: N0 with no curtain and no blind (on the street: east_parade_bay3_upper_w1, the unlet flat's second window, the only one; the other three N0 sites carry a blind or a curtain); **net**: N1, N2 or N3 with no C1 and no B1 to B3; a C2 (curtains drawn back to the sides) counts by its net; **draped**: any B1, B2, B3 or C1 (a blind or a drawn curtain over the pane: east_parade_bay1_upper_w0 B2, east_chandler_bay0_upper_w0 B1, west_south_bay1_gf_w1 C1, east_parade_bay4_upper_w0 C1, west_south_bay2_gf_w1 B3): NO P/L band; a pane spread of at least 20 levels only. TARGET-REVIEW fault 2(b): a cream or white blind cannot read 0.10 to 0.45 of its frame (WB-02), a drawn brown curtain cannot read blue over red by 10 levels (WB-03); the bands were taken from white and cream frames and bare or net panes.

**Frame class:** The P/L and D/L bands apply to white and cream frames only: a bronze frame (linear 0.05) or a brown one (0.09) gives a dark L, so P/L of 1 or more is correct for them and still fails. Under fault 1's amendment every street frame is one of those (white_fresh, white_grimy, white_flaking, white_upvc).

**What the gate cannot show:** the game's glass reflections (Lumen, the cube), the exposure, the motion vectors of the card under TSR, the real glass hand-over: owed on the PC (section 10, OWED rows).

## 10. Checks (target.json `checks`; the cloud gate and the build run them)

47 checks. Kinds of number: Read, Scaled, Photo, Derived, Judgement.

| id | name | measure | expected | tolerance | applies to | kind | source |
|---|---|---|---|---|---|---|---|
| KIT-01 | the opening | bounding box of the glass-plus-frame nodes' outer lining in x and z of each kit | 850.0 wide, 1676.4 high (the frame's outer lining at the brick line) | +-0.5 mm | S22 S11 RC RC2 | Read | lab target.json opening; ruling of 8 October |
| KIT-02 | pivot | the bounding box of the whole piece in the kit frame | x centred on 0 (+-1 mm), z min 0 (+-0.5 mm), nothing in front of the brick face (y into the wall min >= 0: the lab sash 108.3, RC 72.5) | +-1 mm | S22 S11 RC RC2 | Derived | HANDOVER.md pivot rule |
| KIT-03 | glass planes | the y (into the wall) of each pane node's front face | S22/S11: upper panes 142.0, lower panes 190.0; RC and RC2: every pane 112.5 | +-1.0 mm | S22 S11 RC RC2 | Read | 1a section 2; the lab glb; RC and RC2 Judgement from the photographs' frames |
| KIT-04 | one mesh a pane | count of nodes named glass__* | S22 4, S11 2, RC 2, RC2 3 (casement, fixed, top) | exact | S22 S11 RC RC2 | Derived | per-pane tilt needs per-pane meshes |
| KIT-05 | pane tilt | the rotation of each glass node about the vertical and horizontal axes | each within +-0.5 degrees vertical axis and +-0.3 degrees horizontal, none exactly zero, a window's panes spread at least 0.3 degrees | exact bounds | S22 S11 RC RC2 | Photo | P8: panes 86 to 105 mean luma, +-10 per cent; 1a step 3 0.5 to 1 degree |
| KIT-06 | net cards | the node `net__N1`, `N2`, `N3`: x and z extents and the y plane | N1 x +-450, z 60 to 880; N2 x +-450, z 60 to 1630; N3 x +-430, z 100 to 500; planes S22/S11 254, RC and RC2 235 behind the face | +-1 mm | S22 S11 RC RC2 | Judgement | NETS; photographs P1 to P7 |
| KIT-07 | net inside the box | the net plane minus the pane's rear face | S22/S11 lower pane: 254 - 190 = 64 mm or more; no net node crosses a joinery node | no intersection | S22 S11 RC RC2 | Derived | 1a: nets behind the sashes |
| KIT-08 | the room card | node `room__card` (upper windows): size, plane, UV range and the world's CardOrigin from sites[].card | 2.8 x 2.55 m, plane 270 +-1 mm behind the face, centred on the window (+-1 mm), floor 473.6 below the opening's bottom | +-1 mm | S22 S11 RC (upper) | Derived | trace rule; shop-windows target 3 |
| KIT-09 | vertex colour on the joinery | COLOR_0 on every joinery vertex; the red channel's values | present on all; min >= 0.25; faces whose normal points to the street 1.0 (not darkened); the faces that run into the wall (the reveal-facing sides of the linings, beads, pulley stiles and sash stiles) 1.0 at the brick edge falling to 0.6 +-0.05 at the glass; track faces 0.50 +-0.08; inside corners within 8 mm: 0.30 +-0.10; putty strips 0.35 +-0.05; meeting rail underside 0.40 +-0.08 | as stated | S22 S11 RC RC2 | Judgement | 1a step 2, BOX_SHADE; TARGET-REVIEW narrow point 4 |
| KIT-10 | the dark lines are wide enough | every shade step or gap that the box draws as a line (putty strip, parting bead gap, weld groove, gasket) | at least 6 mm wide (the putty strip 6.4, the parting bead gap 2.0 stays a geometric gap of 2 mm with its shade painted 0.10 over 6 mm of each side) | >= 6 mm | S22 S11 RC RC2 | Derived | 1a: 1 px = 5.9 mm at 10 m |
| KIT-11 | budget | triangles and file size per kit glb | <= 6,000 triangles and <= 400,000 bytes | limit | S22 S11 RC RC2 | Judgement | push guard 1 MB |
| KIT-12 | RC and RC2 parts | the RC and RC2 nodes' bounds against target.kinds.RC.parts_mm and target.kinds.RC2.parts_mm | every part within | +-0.5 mm | RC RC2 | Judgement | photographs P6 (RC2), P7, P11 (RC) |
| KIT-14 | equal lights, centred bars | the x extents of every pane node, the bar's centre, the RC's transom, RC2's top light, transom and mullion and its two lower lights' openings | S22: four panes of equal width (352.6 +-0.5), the bar and the putty strips centred on x = 0 (+-0.5); S11: two panes equal; RC: both lights centred on x = 0 (+-0.5), the transom's centre at 0.72 x 1676.4 = 1207.0 (+-1); RC2: the top light, the transom and the mullion centred on x = 0 (+-0.5), the two lower lights' openings equal (330.0 +-0.5 each), the transom's centre at 0.66 x 1676.4 = 1106.4 (+-1), the mullion 70 wide from z 60 to 1071.4 (+-0.5) | +-0.5 mm | S22 S11 RC RC2 | Photo | P8: the bar at 0.500 of the width; unit 7's review, narrow point 1 (unaligned toplights) |
| KIT-15 | no opening in the front | rasterise the elevation drawn from the kit's nodes at 1 mm: every point of the opening 850 x 1676.4 lies on a part (frame, sash, lining, bead, glass sheet) | the largest uncovered square is at most 5 x 5 mm (the S22's 1.6 side clearance and the RC's and RC2's 4 mm gaps are the only gaps) | <= 5 mm | S22 S11 RC RC2 | Derived | unit 7's review, fault 1 (a 1.95 m x 0.45 m hole) |
| KIT-13 | paint and material names | material names on the nodes | paint_<name> per `paints`, glass_house, net_voile, curtain, blind, pendant_shade | exact | all | Derived | HANDOVER.md step 3 |
| MAT-01 | the pane material | the pane material's inputs in the build and in the cloud stand-in | specular 1.0 (F0 0.08; Cycles specular IOR level 1.0), roughness 0.03, metallic 0, transmission 0, base colour 0.03 where the net's alpha is 0 | +-0.02 (roughness 0.02 to 0.04) | all panes | Read | 1a step 1; unreal-look.json glass_roughness 0.02 |
| MAT-02 | no day glow | the pane's emission by day | 0 (the net is not emissive by day: net_day_gain 0.0) | exact | all | Read | unreal-look.json net_day_gain |
| MAT-03 | the alpha is wired | the net material's alpha input | linked to the weave texture (not a constant) | exact | net cards | Read | 1a: 'the lace's alpha is not wired' was the fault |
| MAT-04 | reflectance at a grazing angle | render a flat pane at 16 degrees from the wall against a uniform sky of luma 1.0 with the room black | the pane's luma 0.26 of the sky with F0 0.08 (Schlick at 74 degrees from the normal: Unreal's own figure for Specular 1, 1a section 2); Cycles' dielectric Fresnel at specular level 1.0 may read up to 0.31 | +-0.05 | the pane material | Derived | 1a Fresnel table: true two-face 0.38, Unreal 0.26 |
| WB-01 | net windows are darker than their frames | P/L of every net window (N1 or N2; a C2 counts by its net; not draped) seen at 15 to 30 degrees from the wall (day, the gate's five views); P over the pane's median, L over the joinery (the outline minus the pane); white and cream frames only (every street frame is one: frame_class) | 0.55 to 0.97, no median cap | band | GS_A GS_B | Photo | P1_a, P1_b, P1_e boxed without the stone and the brick, measured the gate's way: 0.93, 0.94, 0.90 (at 31 to 39 degrees); the nine net windows 0.60 to 0.97; TARGET-REVIEW fault 2 |
| WB-02 | bare windows are much darker | P/L of every BARE window (N0 with no curtain and no blind: on the street east_parade_bay3_upper_w1 only) seen at 15 to 30 degrees from the wall, by day; draped windows have no P/L band | 0.10 to 0.45 | band | GS_A GS_B | Photo | P1_c 0.29, P4_G 0.18, P3_d 0.36 |
| WB-03 | bare windows from across, near square | P/L of every BARE window (as WB-02) seen from H_ACROSS_0 by day (over 60 degrees), and the pane's blue minus red; draped windows are not tested here | 0.35 to 0.70 and blue over red at least 10 levels | bands | GS_A | Photo | P8_L, P8_R: 0.59, 0.49, all four panes together 0.57; (85, 100, 133) |
| WB-04 | the dark lines are present | D/L of every bare and net window seen at 15 to 30 degrees: D the outline's 5th percentile (joinery and pane, no brick), L the joinery's 90th percentile; white and cream frames only; draped windows have no D/L band | at most 0.72 | limit | GS_A GS_B | Photo | P1_a 0.65 (0.71 with its top rows out), P1_b 0.65, P1_e 0.52 measured the gate's way; the fault was 0.85; 1a's 0.6 is a profile across the lining (photograph 9), see WB-04b |
| WB-04b | the dark line round each pane | on a horizontal profile across each stile-to-pane edge and a vertical profile across each rail-to-pane edge of every bare and net window seen at 15 to 30 degrees (the gate's line_profile): the dip next to the edge | a dip at least 1 px wide to at most 0.60 of L | limit | GS_A GS_B | Photo | 1a section 5 and photograph 9 (the inside corner 105 to 125 against a lining of 220 to 250: 0.5); at P1's scale (15 to 18 px a window) a 6 mm line cannot be resolved, so the photographs measured here cannot set it; the old fault (no line) fails it |
| WB-05 | the pane is not one tone | the pane spread (95th minus 5th percentile) of every net window; of every bare window; of every draped window | net at least 40 levels; bare at least 20; draped at least 20 | limit | GS_A GS_B | Photo | nets 64 to 173 on the photographs (the three P1 windows 76, 64, 109 measured the gate's way); 1a: at least 20; the fault 14 |
| WB-06 | something is behind the glass by day | for every bare, N3 or N1 window seen from H_ACROSS_0 by day (and a draped window whose blind leaves the upper sash clear: B1, B2): the clear pane's pixels (upper sash for N1, B1, B2; whole pane for a bare window) | at least two tonal regions (the ceiling and the back wall, or the net's edge) whose medians differ by 10 levels or more, from the room picture through `trace` | 10 levels | GS_A GS_B | Derived | brief item 6 |
| WB-07 | the frame is brighter than the wall | L (linear) over the brick's median (linear) beside the window, by day | 3.0 to 9.0 | band | GS_A GS_B | Photo | P1 3.75 and P8 4.1 on photographs (film contrast; L the joinery's 90th percentile); the game's albedos give 0.82/0.13 = 6.3; the concept sheet's 7 is outside the photographs |
| WB-08 | the old fault fails | run WB-01 to WB-05 and WB-04b on a render with the old pane (a lit lace card, F0 0.04, no lines) in the same views | WB-04 and WB-04b and WB-05 and WB-02 must FAIL (D/L 0.85, no dip at the pane edges, spread 14, bare windows lighter than 0.45) | must fail | GS_A | Derived | 1a section 3; a check that cannot fail checks nothing |
| WB-09 | the window under 10 degrees | a window seen under 10 degrees from the wall (the far end of H_ALONG_15_ROAD) | reads as a white lining edge at least 1 px wide beside a dark void; the reveal's brick return 0.8 of the wall's luma or less; no pane luma above the lining's | as stated | GS_A | Photo | P13: a white slit beside a dark void; 1a |
| NIGHT-01 | lit and dark windows at night | at 20:30 over the 20 street windows (GS_A and GS_B together, rendered from the one camera that sees each squarely): a window is LIT when its pane median luma is at least 4 times the dark windows' median luma and the pane's mean linear colour has r > g > b; DARK when its pane luma is 8 to 30 (NIGHT-04). The absolute emissions of the curtains, blinds and the landing bulb (`night_lit_emission_linear`, `landing_bulb`) are set to read 100 to 140 and are the starting values, not the pass line | 7 lit (+-1), the rest dark; none that is neither | +-1 | all 20 | Judgement | rooms.lit_share; TARGET-REVIEW narrow point 5 (the absolute 100 cannot be met behind a drawn brown curtain at 0.35 transmission, or by a bare 40 W landing bulb) |
| NIGHT-02 | lit against dark | the median pane luma of the lit windows over that of the dark windows, night | at least 4 (linear at least 10) | limit | GS_A GS_B | Judgement | NIGHT-2026-10-08.md: real lit windows are 10 to 100 times the lit paving; the game's gain gives 0.4 |
| NIGHT-03 | the lit net glows its own colour | a lit net's mean colour (linear) ratio r:g:b; a lit curtain's or blind's mean colour | net: r > g > b, g/r 0.55 to 0.80, b/r 0.20 to 0.45 (tungsten 2700 K and the fabric); curtain or blind: its own colour x that light (curtains.*.night_lit_emission_linear): r > g > b for the cream and brown curtains and the white and cream blinds (the brown curtain's g/r is 0.39); a green curtain's g > r is its own colour and none is lit at 20:30 | band | lit windows | Read | interior_lit (1.0, 0.714, 0.344) |
| NIGHT-04 | a dark window shows only the sodium wash | the dark rooms' mean colour (linear) | b/r under 0.05 (the wash is (1.0, 0.25, 0.0)); luma 8 to 30 sRGB | limit | dark windows | Read | unreal-look.json lantern_linear_rgb |
| NIGHT-05 | the lit order is nested | the set lit at 23:00 is a subset of the set lit at 20:30 except the always-lit pair's end; empty rooms never lit | true | exact | table | Derived | lit_share.rule |
| PIC-01 | size and states | each room's three PNGs | 1536 x 1399 (UP) or 3072 x 2349 (GF), 8-bit sRGB, named <room>_<state>.png, with <room>.json | exact | 13 rooms x 3 states = 39 | Derived | shop-windows target 3 |
| PIC-02 | mean luma | the mean sRGB luma of each picture | day 105, night_lit 70, night_dark 15 (landings and empty rooms at night_lit: bare bulb: 40) | +-15 per cent | all | Judgement | picture_standards |
| PIC-03 | no black void | the share of pixels under luma 8 and the largest dark region | day and night_lit: under 25 per cent and the largest region under 15 per cent of the picture; the composite (x brightness) day >= 14, night_lit >= 40 | limits | all but night_dark | Derived | the 3 October failure |
| PIC-04 | the back wall lands where the rule puts it | the back wall's corners in the picture by edge detection | UP (1536 wide): (461, 420) to (1075, 979); GF (3072 wide): (849, 649) to (2223, 1700) | +-8 px | all | Derived | trace/project rule, camd = W |
| PIC-05 | stand-off | every object's and every form's stand-off from its surface (rooms.rooms[].objects, rooms.forms) | back wall <= 0.80 (true <= 0.40), side walls <= 0.06 (true <= 0.03), ceiling <= 0.04 (true <= 0.02), floor <= 0.037 (true <= 0.018) | limit | all | Derived | hw_common budgets |
| PIC-06 | parallax | from H_ACROSS_0 and the same point moved 2.0 m along the street, a marker at the picture's centre | moves as `trace` predicts | +-20 px of 2048 | UP and GF samples | Derived | shop-windows PRJ-02 (proves the gate, not the game) |
| PIC-07 | no marks | every picture searched by eye at full size, and the final base colour of every model used; the base-colour maps of every placed model checked at 1k against its marks entry, region by region, before the room is rendered | no maker's name, brand, logo, barcode, person or child; every `marks` entry blanked or the model not used; no lettering readable at 100 per cent on any map of a placed model once its marks are painted out | none | all | Derived | TARGET-REVIEW of unit 7, fault 2; TARGET-REVIEW of unit 8, fault 3 (television_02's maker's name on its front bezel, missed by the first look) |
| PIC-08 | the room is lit as the table says | the picture used for each window in each state | lit windows night_lit, the others night_dark, day for all by day | exact | 20 sites | Derived | lit_share |
| SITE-01 | the twenty openings | the derived list of terrace-front.py's windows re-derived live | 20 sites, centres and kinds as sites[]; the cottage windows' kind by house | +-1 mm | 20 sites | Read | terrace-front.py plan_street, _window_kind |
| SITE-02 | no visible repeat | along each row, any two windows within three places | never the same (room, net kind, curtain) triple, never the same paint on neighbouring houses unless white | exact | sites | Judgement | variants |
| SITE-03 | the mix | the street's twenty windows by net class | N0 4 to 5, N1 8 to 10, N2 3 to 5, N3 1; curtains (open beside a net, or drawn) and blinds 6 to 10 of the 20 | counts | 20 sites | Photo | tally |
| SITE-04 | paint | houses by paint | white (white_fresh, white_grimy, white_flaking, white_upvc) 10 of 10 until Jafar's page rules otherwise | counts | 10 houses | Read | RULINGS.md 3 October (windows with white frames) over the photographs' tally (white 55 per cent), D13 |
| CONTENT-01 | the content rule | every string of target.json, every picture, every preview | no alcohol, gambling, child; no real firm's name; tobacco allowed | none | all | Derived | canon.md; CLAUDE.md |

**Owed on the PC** (the cloud cannot show them):

- **OWED-01** The pane in the game: Specular 1.0 at roughness 0.03 with the net's alpha wired, the opaque Default Lit material, seen at 15 to 30 degrees with Lumen's own reflections. Check: WB-01 to WB-05 on the packaged game's frames at the Hook camera and the reverse view (1a's step 1 test).
- **OWED-02** The joinery's shade as vertex colour (BOX_SHADE) read by M_LedgerSurface (not the AO pin). Check: 1a section 5: D/L <= 0.6, T/L 0.65 to 0.85, P/L 0.6 to 0.9 and a pane spread of 20 levels in the hook frame's near-left terrace and Mickey's row.
- **OWED-03** A marker at the room picture's centre moves as `trace` predicts from two eyes 2.0 m apart, in the packaged game. Check: PIC-06 on the PC: 20 px of 2048.
- **OWED-04** The room pictures rebuilt on the PC (`python make_house_rooms.py`: not written here), the masters on F:/LedgerTools/house-rooms, imported as sRGB textures. Check: PIC-01 to PIC-05, PIC-07 at full size.
- **OWED-05** Jafar's page: the house windows as a sample (the look): one page with the 15 and 30 degree frames, day and night, and the old frame beside, and two one-line questions with a recommendation (picks stored). Check: Nothing is multiplied before his yes (CLAUDE.md).
    - Line for his page: Window frames: all white as you ruled on 3 October (recommended), or the 1980s photographs' mix (white 55%, brown 13, cream 12, blue 8, olive 7: one house each)?
    - Line for his page: Cottage windows: head kept, sill 0.72 above the step (recommended), or sill 0.9 with 9 cm of brick under the eaves?
- **OWED-06** 1a step 3, the upper panes reflecting the street (a cube of the street box-projected onto the pane): deferred, not built in the cloud. Check: In the reverse view at least 2 of 3 upper panes show a horizontal edge with a step of at least 30 levels, moving when the camera moves 1 m.

## 11. Photographs win: each disagreement

| id | what | the file, book or research said | the photographs say | chosen |
|---|---|---|---|---|
| D1 | the replacement frame's colour | dark anodised bronze (frame_bronze) for every replacement (terrace-front.py _sash) | white in all four replacement windows reached (P6, P7, P11, and P6's ground bay): none brown or bronze | white satin (white_upvc) for EVERY replacement house, the ship chandler's too: none is bronze. The first version kept bronze for the chandler (a metal-refit shop, the asset plan's D06 'Hook shops receive metal frames'): that is a question for Jafar, not decided here, and it now stands on D13's line (TARGET-REVIEW fault 1) |
| D2 | the nets | one square mesh picture over the whole pane (net_curtain_a, _b: 7 to 10 mm squares, mean alpha 0.53), alternated by house | about half the windows have a voile on the lower sash only (47 of 60), the upper sash clear; full nets 22 per cent; bare 18 per cent; curtains 10; blinds 2 | six net and drape kinds, per house, with the mix of the photographs; the two held pictures are not used |
| D3 | the pane | the net card is the pane: lit lace over a pale card, F0 0.04 (the 8 October note) | every bare window reads dark (0.18 to 0.36 of its frame) and the room shows; a net reads 0.60 to 0.97 of the frame with lines round it | glass over a dark room, the net a separate card (1a) |
| D4 | the cottages' windows | all six drawn as 2/2 box sashes 1.5 high (the per-house kind is not read on the ground floor); sill 0.9 above the threshold, head 2.4 (the 3 October rule: arches clear the eaves) | the ground windows of P1, P3, P4, P12 are the same kinds of sash as the floor above; P6's ground bay window's sill stands 0.85 +-0.05 above the step (Photo: the door leaf is 193 px = 1981 mm, the sill 83 px above the step) | the house's own kind and the period opening 1676.4 with the head kept at 2.5 above the crown: the sill 0.7236 above the threshold, 0.13 lower than P6's 0.85; the alternative (sill 0.9, head 2.676, the arch's top at 3.01 under the eaves at 3.1) leaves 9 cm of brick under the eaves and is Jafar's to choose (could_not_settle) |
| D5 | six over six | none | P10 (Copenhagen Street, Georgian, 1983) and P13 (Prince Street, Hull, 1982) show it, on Georgian terraces; no house of Quay Street is Georgian | not built; listed as the sash kind a Georgian house would need |
| D6 | the glazing bar | 22.2 mm (the lab's amended value) | P8 (Oxford, 1987): the bar is 2.3 px wide on a window 71.9 px wide = 27 mm (+-6) | 22.2 kept: inside the error |
| D7 | the frame's visible width | 76.2 (3 in, the ruling) | P8, the BACK of a terrace (plain, no outer lining): the visible white jamb is 3.1 to 4.0 px of 71.9 = 37 to 47 mm; the lab's P6 (a front, Tottenham) 79 mm | 76.2 kept for the fronts (the ruling); a rear window narrower, not on this street |
| D8 | the lit share | one in three of the upstairs nets lit at night, two cottage windows always | none reached (no night photograph of a terrace before 1996) | kept near the street's one in three (0.35 at 20:30); a Judgement |
| D9 | frame to wall ratio | WINDOWS-OTHER-DIRECTION: frames about 7 times the wall | P1 3.75, P8 4.1 (linear, display values of film scans; L now the joinery's 90th percentile) | the check's band is 3 to 9; the game's own albedos give 6.3 |
| D10 | the meeting rail | 38.1 mm (the lab kept it) | P8: the rail with its shade reads 5 px of 134 = 62 mm; the lab's note (P6 Tottenham 24 to 28 mm face) stands for the face; the rest is the underside's shade | 38.1 kept; the shade is BOX_SHADE.meeting_rail_underside |
| D11 | the top light of the replacement | the transom at 0.72 of the opening (REPLACEMENT_TRANSOM) | P6 0.66, P7 0.72, P11 0.75; P6 also shows the other FORM: a fixed top light across over two lower lights, a side-hung casement beside a fixed light, the mullion near the middle | two forms are built: RC (P7's: a fixed light under a top-hung light, the transom at 0.72, kept, inside the three) on east_parade_bay2, east_chandler_bay0 and west_south_bay1, and RC2 (P6's, the transom at 0.66, a fixed top light, a 70 mm mullion at x 0, a side-hung left casement and a fixed right light) on east_parade_bay4 (TARGET-REVIEW narrow point 7) |
| D12 | the white-board look at 15 to 30 degrees | the panes should be darker than the frame by about 0.6 to 0.9 | net windows measured the gate's way read 0.90 to 0.94 of the frame at 31 to 39 degrees (the first version's 0.83 to 0.87 took L from the white-painted stone and the brick at the jamb): nets ARE nearly white; bare windows 0.18 to 0.36; the dark line round each pane is a dip of 0.5 of L on a profile across the lining (photograph 9), not resolvable at P1's scale | the bands above are by window state (bare, net, draped); the fault is the missing lines and the uniform tone, not a bright net: WB-04 at most 0.72 and the new WB-04b (the dip at the pane edges) |
| D13 | the frame colour of the ten houses | terrace-front.py draws every timber sash `frame_painted` white and every replacement `frame_bronze` | white 55 per cent of 60 windows, cream or ivory 12, dark or red-brown 13, blue 8, olive 7 (the first version of this target gave one house each to brown, olive, blue, cream and bronze); every replacement white in the four reached (D1) | ALL TEN HOUSES WHITE (white_fresh 2, white_grimy 3, white_flaking 1, white_upvc 4): Jafar's standing ruling stands over the photographs' tally until he answers (OWED-05's first line; CLAUDE.md: if code must change a ruling, ask him first, and anything touching the look reaches him on one page). The cream, olive, blue, brown and bronze paints stay in `paints` as unused data. The question D1 left (the chandler's bronze: the asset plan's D06) is on the same line |
| D14 | the segment under the arch | brick fills the space between the flat sash head and the segmental brick arch (terrace-front.py: ARCH_FANLIGHT False, the 4 October decision) | P8 shows that space filled by a cream-painted timber head that follows the arch | BRICK is built: the 4 October decision stands (the segment is the wall kit's, not this unit's). If it changes to a painted segmental head it reaches Jafar's page first (CLAUDE.md: anything touching the look) |

## 12. What the target could not settle

- No 1975 to 1995 night photograph of a terraced street was reached: the lit share by hour is a Judgement (anchored on the street's own one in three).
- No period photograph of a brown or bronze anodised aluminium window on a house was reached; and Jafar's ruling of 3 October is white frames: no house takes bronze, brown, olive, blue or cream. Whether the street takes the photographs' mix (white 55 per cent, one house each of the others) or the bronze chandler is his, on OWED-05's first line (D13).
- The photograph measurements are on 640 to 1024 px scans: a window is 15 to 100 px wide, so D (the darkest line) is a floor, and the angle from the wall is +-5 degrees from the window's proportion; the bands are wide for that reason.
- A sealed double-glazed unit's four reflecting faces (about 0.14 at normal incidence) cannot be reached by Unreal's Specular 1.0 (F0 0.08): the replacement's pane under-reflects; the cure (an emissive sky term) is a PC tuning, listed in owed_on_pc.
- How the game's Lumen reflections and the street cube show on the pane (the box projection, the Fresnel hand-over) is not shown by the cloud: the cloud's pane reflects the proxies and the dome through Cycles.
- The rooms' contents were chosen from 44 Poly Haven models and 9 textures; none shows a period British room: no 1975 to 1995 photograph of a domestic interior was reached, so the rooms rest on the photographs' windows (nets, drapes, a pot plant, a dark room) and on the budgets, not on a room photograph.
- Whether the cottages take the period height with the head kept (sill 0.7236 above the threshold: 0.13 under P6's 0.85) or with the sill kept (0.9, the head raised to 2.676 above the threshold, the arch left 9 cm of brick under the eaves) is Jafar's: the ruling of 8 October (1.68 m) is followed for every row with the head kept; the PC session widens SASH_KIT_ROWS.
- Only one street window is BARE in the sense of the gate's window states (N0 with no curtain and no blind): east_parade_bay3_upper_w1, the unlet flat's. The other three N0 windows carry a blind or a drawn curtain (draped: no P/L band, a spread of at least 20 only), so WB-02 and WB-03 have a sample of one on the street.
- No net window was measured inside WB-01's own range of 15 to 30 degrees: the three P1 windows are at 31 to 39. The band is carried down as a Judgement; at P1's scale the box's 6 mm dark lines cannot be resolved, so WB-04b (the dip at the pane edges) has no photograph's number, only 1a's profile across a lining (0.5 of L).
- Six over six is not on the street and was not built.
- The backdrop rows (48 windows) take the same pieces with no pictures: their paint and lit pane are rules, not a table.

## 13. Previews

In `production/previews/cloud-week/refs/house-windows/` (JPEG, at most 1200 px, under 300 KB; Geograph photographs CC BY-SA 2.0, credited in the table of section 2; the drawing's overlay is ours):

| ref | file | crop | masked |
|---|---|---|---|
| P1 | p1-hull-john-street-1985-oblique-sashes-nets.jpg | crop [330, 370, 700, 545] | none needed |
| P2 | p2-hull-durham-street-1986-painted-frames-nets.jpg | crop [0, 240, 1000, 440] | street-name sign |
| P3 | p3-bangor-penchwintan-terrace-1988-stone-terrace-nets.jpg | crop [440, 265, 1024, 535] | none needed |
| P4 | p4-rochdale-oswald-street-1979-bw-oblique-nets.jpg | crop [380, 60, 640, 480] | none needed |
| P5 | p5-croydon-tanfield-road-1979-bw-bays-nets.jpg | crop [270, 110, 640, 390] | none needed |
| P6 | p6-levenshulme-ratcliffe-street-1994-replacement-window-bay.jpg | crop [270, 60, 658, 575] | none needed |
| P7 | p7-barnoldswick-frederick-street-1990-bw-double-glazing-nets.jpg | crop [195, 195, 640, 440] | street-name plate; small plate on the dark door (a house number's place) |
| P8 | p8-oxford-sunningwell-road-rear-1987-rear-sashes-from-below.jpg | crop [280, 270, 680, 470] | none needed |
| P9 | p9-shoreditch-boundary-street-1989-tall-sashes-oblique.jpg | crop [280, 30, 560, 430] | none needed |
| P10 | p10-islington-copenhagen-street-1983-georgian-6over6-boarded.jpg | crop [0, 0, 640, 442] | none needed |
| P11 | p11-newburn-council-houses-1989-council-casements.jpg | crop [0, 370, 700, 690] | none needed |
| P12 | p12-railway-street-terrace-1987-sashes-olive-white.jpg | crop [80, 100, 800, 400] | street-name plate; notice board on a post; oval plate on the white door (a house number's place) |
| P13 | p13-hull-prince-street-1982-under-10-degrees-slit.jpg | crop [600, 0, 766, 620] | none needed |
| P14 | p14-burnley-milan-avenue-1988-boarded-houses.jpg | crop [330, 100, 640, 360] | none needed |
| overlay | p8-oxford-sunningwell-road-rear-1987-target-on-photo.jpg | P8's left window with the S22 elevation laid on at the width scale (yellow: the opening; red: the sash members; green: the panes) | none |
| sheet | measured-windows-sheet.jpg | the 18 windows measured, outline red and pane green (P1_a, P1_b and P1_e boxed without the stone head and sill and the brick column, as the review boxes them) | none |

