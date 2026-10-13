House windows of Quay Street: twenty windows in ten houses (two over two, one over one, a replacement casement), each pane glass over a dark room with its box shaded and its lines drawn, nets and drapes by the photographs' mix, thirteen small rooms behind them in the game's own projection, and the white-board fault caught by measurement on 1979 to 1994 photographs.

# House windows of Quay Street: the exact target

**Status: written 13 October 2026, not yet reviewed.** Cloud week 42, part 2, unit 8, by the target writer, from sources reached that day. Nothing is built and nothing is committed. Every number below is in `target.json`; the checks that follow from it are its `checks` list and its `self_check` (not yet run).

The lessons of unit 7's fresh review (TARGET-REVIEW.md of the shop windows) are applied from the start: every opening is covered above and around its parts (section 4.5); the toplights of the replacement are one transom and equal lights (4.3); no real firm's name is on any model's texture (every model's 1k base colour was looked at, section 7.6, and the checks include a final-texture check PIC-07); the night wash is the game's colour; the projection rule `trace` is the only source of what a room shows, with stand-off budgets derived again for these smaller rooms (3.3); the numbers are exact and the checks measurable (section 10); and every preview was looked at after it was written.

## 0. Files, and how to read them

| file | what it is |
|---|---|
| TARGET.md | this page (made by make_doc.py from target.json) |
| target.json | the twenty sites, the kinds and their parts, the glass, the box's shade, the nets and drapes, the thirteen rooms with their objects and budgets, the inventory with each model's marks, the kit pieces' nodes, the gate, 44 checks, the photograph measurements, the overlay's edges, the lit table, `photographs_win`, `could_not_settle`, `owed_on_pc`, the self-check |
| target_drawing.py | draws target.json alone: each kind's elevation and sections, each room's picture layout and back wall, the row of twenty, and (with --photo) the 2/2 elevation laid on photograph P8; into a JSON of polygons (millimetres) and a folder of pictures |
| self_check.py | tests the target against its own sources (it writes into target.json only with --write); 14 negative controls |
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

**The twenty, by position.** *Kind by house* is what `_window_kind` gives the house; *built today* is what the recipe draws; *target* is what this unit makes. Every site gets the period opening 850 x 1676.4 (the ruling of 8 October: "1.68 m"), the head kept where it is, so the cottages' sills go from 1.0 to 0.8236 above the crown (0.7236 above the threshold; P6's ground sill stands 0.72 to 0.92 above the step, Photo ±0.1).

| site | x | floor | kind by house | built today | target | paint | net | drape | room | lit 20:30 |
|---|---|---|---|---|---|---|---|---|---|---|
| east_parade_bay0_upper_w0 | 4.5 | upper | 2/2 | S22 kit | S22 | white_grimy (grimy) | N2/greyed | - | up_landing_1 | no |
| east_parade_bay0_upper_w1 | 7.5 | upper | 2/2 | S22 kit | S22 | white_grimy (grimy) | N1/white | C2/cream | up_lounge_1 | yes |
| east_parade_bay1_upper_w0 | 10.5 | upper | 1/1 | S11 kit | S11 | cream | N0 | B2/cream | up_landing_2 | no |
| east_parade_bay1_upper_w1 | 13.5 | upper | 1/1 | S11 kit | S11 | cream | N1/white | C2/brown | up_bedroom_1 | no |
| east_parade_bay2_upper_w0 | 16.5 | upper | replacement | box replacement (frame_bronze) | RC | white_upvc | N1/greyed | C2/green | up_lounge_2 | no |
| east_parade_bay2_upper_w1 | 19.5 | upper | replacement | box replacement (frame_bronze) | RC | white_upvc | N2/greyed | - | up_landing_1 | yes |
| east_parade_bay3_upper_w0 | 22.5 | upper | 2/2 | S22 kit | S22 | white_flaking (flaking) | N1/yellowed | - | up_empty_1 | no |
| east_parade_bay3_upper_w1 | 25.5 | upper | 2/2 | S22 kit | S22 | white_flaking (flaking) | N0 | - | up_empty_2 | no |
| east_parade_bay4_upper_w0 | 28.5 | upper | replacement | box replacement (frame_bronze) | RC | white_upvc | N2/white | C1/green | up_bedroom_2 | no |
| east_parade_bay4_upper_w1 | 31.5 | upper | replacement | box replacement (frame_bronze) | RC | white_upvc (grimy) | N1/yellowed | - | up_landing_2 | yes |
| east_parade_bay5_upper_w0 | 34.5 | upper | 1/1 | S11 kit | S11 | olive | N1/white | C2/floral_cream | up_lounge_3 | no |
| east_parade_bay5_upper_w1 | 37.5 | upper | 1/1 | S11 kit | S11 | olive | N3/white | - | up_landing_1 | no |
| east_chandler_bay0_upper_w0 | 41.5 | upper | replacement | box replacement (frame_bronze) | RC | bronze | N0 | B1/white | up_bedroom_3 | no |
| east_chandler_bay0_upper_w1 | 44.5 | upper | replacement | box replacement (frame_bronze) | RC | bronze (grimy) | N2/yellowed | - | up_landing_2 | yes |
| west_south_bay2_gf_w0 | 6.3 | ground | 2/2 | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | S22 | cream | N1/white | - | gf_front_3 | yes |
| west_south_bay2_gf_w1 | 8.1 | ground | 2/2 | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | S22 | cream | N1/white | B3/white | gf_front_3 | yes |
| west_south_bay1_gf_w1 | 9.9 | ground | replacement | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | RC | white_upvc | N0 | C1/brown | gf_front_2 | yes |
| west_south_bay1_gf_w0 | 11.7 | ground | replacement | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | RC | white_upvc | N2/white | - | gf_front_2 | no |
| west_south_bay0_gf_w1 | 15.9 | ground | 1/1 | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | S11 | blue (grimy) | N1/white | - | gf_front_1 | no |
| west_south_bay0_gf_w0 | 17.7 | ground | 1/1 | box 2/2 (55 mm frame, 22 mm bars: _plain_ground draws every cottage window as a 2/2 whatever the house's kind) | S11 | blue (grimy) | N1/white | - | gf_front_1 | no |

Kinds: **six two-over-two (S22), six one-over-one (S11), eight replacement casements (RC).** Upper floors 14, ground 6. The landing windows (the window on the side-door's side of each flat: bays 0, 1, 2 (right), 4 (right), 5 (right), the chandler's right one, and the empty flat's left) light the stair; the others light a lounge or a bedroom. The unlet flat above the empty shop (bay 3) is empty at both windows.

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

**Research and project files read:** production/cloud-week/research/1a-sash-windows-low-angles.md (the fix, cheapest first); production/research/aaa-street/WINDOWS-FACADES-2026-10-04.md; WINDOWS-GRAZING-2026-10-08.md; WINDOWS-OTHER-DIRECTION-2026-10-04.md; production/cloud-week/targets/shop-windows/TARGET.md sections 3 and 4 and TARGET-REVIEW.md (the lessons applied here); production/art/sash-window/target.json and TARGET-NOTES.md (the lab's sash, amended 8 October); tools/art-recipes/terrace-front.py (the sites, the kinds, the nets, the lit rule); tools/ue/make_interior_material.py `trace`; production/specs/shop-interiors.json; production/specs/unreal-look.json; production/specs/vignette-scene.json, vignette-pieces.json; production/research/evening-light-1990/SUMMARY-2026-09-29.md and production/research/shop-glass-reflections/NIGHT-2026-10-08.md (lit windows 6 cd/m2); RULINGS.md 3 and 8 October; production/cloud-week/HANDOVER.md.

**Libraries:** Poly Haven API (api.polyhaven.com assets and files), 13 October 2026: every model and texture named exists, CC0; the 1k base colour of each looked at (inventory).

**Not reached (nothing rests on them):** Wikimedia Commons (not asked: Geograph's feed answered); archive.org (not asked); any 1975 to 1995 night photograph of a terrace (none found: no Geograph result before 1996 for night, dusk or lit windows); any period photograph of a 1980s brown anodised aluminium house window (none among the 14 photographs; none searched by image: Geograph is searchable by words only); Epic's pages (not needed: the engine facts come from the repository's notes).

## 3. The method, in the game's own numbers

### 3.1 Why the windows read as white boards, and what the photographs say

Research 1a found the cause: the pane was a pale lit card (not glass over a dark room), the box was lit flat with no dark lines, and the upper panes reflected no shapes. This unit builds 1a's fix as numbers a builder can follow (sections 5 and 6). **What the photographs add** (14 photographs, 1979 to 1994; 18 windows measured, section 3.2): at 15 to 40 degrees from the wall the real windows are *not* uniformly dark. A window with a net reads **0.83 to 0.87** of its frame's brightness (P1, three windows at 31 to 37 degrees); a window with bare glass and a dark room reads **0.19 to 0.36**; seen nearly square from below, glass over a dark room under a blue sky reads **0.51 to 0.62** (P8). The white-board fault is therefore not 'a pane as bright as its frame' but **a pane that is one even tone with no dark line round it**: the old build's pane read 157 to 175 against paint 178 to 205 (0.85) with no corner line (D/L 0.85, a spread of 14 levels), where the photographs' tight outlines read D/L 0.47 to 0.50 and a spread of 85 levels or more. The checks of section 9 test the lines and the spread by window state, not one pane ratio.

### 3.2 What was measured on the photographs (Photo)

The pane-to-frame measurements on the photographs (Photo kind). Each window: an outline box (jamb to jamb, head to sill top), the pane boxes (the glass or net inside the sash), its state, and the proportion w/h its true window would have (0.50 for the period sash; 0.33 for P9's tall arched ones). Luma is sRGB-coded 0.2126 R + 0.7152 G + 0.0722 B (1a's measure). L = the outline's 90th percentile, P = the pane median, D = the outline's 5th percentile. The angle from the wall is estimated from the window's apparent proportion: sin(angle) = (w_app / h_app) / a_true; its error is +-5 degrees (the true proportion varies 0.40 to 0.62 between windows). The outline boxes are by eye on the photographs' own pixels (hw_photos.PHOTOS ids); a few include the dark reveal at their edge, so D is a floor: the tight outlines (P1) are the ones to compare with a render's D/L.

| window | photo | state | angle from wall (deg, +-5) | L (p90) | P (median) | D (p5) | P/L | D/L | pane spread | what |
|---|---|---|---|---|---|---|---|---|---|---|
| P1_a | P1 | net_full | 34.8 | 233.6 | 202.0 | 117.3 | 0.865 | 0.502 | 85.8 | upstairs, white frame, white voile both sashes |
| P1_b | P1 | net_full | 31.1 | 244.8 | 202.8 | 114.0 | 0.828 | 0.466 | 87.0 | upstairs, white frame, white voile |
| P1_c | P1 | bare_dark | 22.2 | 228.5 | 73.0 | 27.3 | 0.32 | 0.12 | 102.0 | upstairs, dark-brown frame, bare glass, dark room |
| P1_e | P1 | net_full | 36.9 | 226.6 | 192.6 | 110.1 | 0.85 | 0.486 | 110.9 | ground, white frame, white voile |
| P4_C | P4 | net_full | 68.5 | 254.0 | 247.0 | 36.0 | 0.972 | 0.142 | 173.0 | upstairs, full white net (black and white print) |
| P4_G | P4 | bare_dark | 46.0 | 215.0 | 41.0 | 2.0 | 0.191 | 0.009 | 208.0 | ground, bare, the room black, a pot plant |
| P4_E | P4 | net_half | 35.1 | 218.0 | 122.0 | 31.0 | 0.56 | 0.142 | 148.8 | ground, a net over the lower half |
| P3_a | P3 | net_full | 90.0 | 175.3 | 105.6 | 5.4 | 0.602 | 0.031 | 130.9 | upstairs, cream frame, lower sash voile, near square |
| P3_b | P3 | net_full | 61.5 | 192.5 | 162.0 | 38.0 | 0.842 | 0.197 | 113.2 | upstairs, red-brown frame, voile |
| P3_c | P3 | net_full | 51.3 | 170.7 | 124.7 | 26.5 | 0.731 | 0.155 | 116.0 | ground, red-brown frame, voile |
| P3_d | P3 | bare_dark | 90.0 | 167.2 | 60.7 | 12.0 | 0.363 | 0.072 | 148.9 | ground, cream frame, bare lower sash, dark room, near square |
| P3_e | P3 | net_full | 64.8 | 211.6 | 167.4 | 32.2 | 0.791 | 0.152 | 150.1 | ground, white frame, voile |
| P3_f | P3 | net_full | 61.8 | 212.3 | 190.6 | 32.5 | 0.897 | 0.153 | 96.0 | upstairs, white frame, voile |
| P9_a | P9 | glass_bright | 29.8 | 208.8 | 155.0 | 62.8 | 0.742 | 0.301 | 105.6 | tall sash in shade, panes pale (sky), bars as dark lines |
| P9_b | P9 | glass_bright | 28.7 | 215.7 | 166.3 | 58.5 | 0.771 | 0.271 | 120.3 | tall sash in shade |
| P9_c | P9 | glass_bright | 33.3 | 254.2 | 251.9 | 96.1 | 0.991 | 0.378 | 138.8 | tall sash in sun, panes bright |
| P6_up | P6 | glass_sky_room | 90.0 | 251.9 | 225.4 | 72.2 | 0.895 | 0.287 | 174.9 | replacement window: sky in the top light, dark room and a net edge below |
| P8_L | P8 | glass_dark_room | 90.0 | 164.4 | 101.2 | 93.5 | 0.616 | 0.569 | 19.4 | original 2/2, near square from below, panes blue-grey over a dark room |
| P8_R | P8 | glass_dark_room | 90.0 | 170.4 | 86.8 | 83.3 | 0.51 | 0.489 | 52.7 | original 2/2, near square from below |

| state | n | P/L range | P/L median | D/L median | angles |
|---|---|---|---|---|---|
| bare_dark | 3 | 0.19 to 0.36 | 0.32 | 0.07 | 22.2, 46.0, 90.0 |
| glass_bright | 3 | 0.74 to 0.99 | 0.77 | 0.30 | 28.7, 29.8, 33.3 |
| glass_dark_room | 2 | 0.51 to 0.62 | 0.56 | 0.53 | 90.0, 90.0 |
| glass_sky_room | 1 | 0.90 to 0.90 | 0.90 | 0.29 | 90.0 |
| net_full | 9 | 0.60 to 0.97 | 0.84 | 0.15 | 31.1, 34.8, 36.9, 51.3, 61.5, 61.8, 64.8, 68.5, 90.0 |
| net_half | 1 | 0.56 to 0.56 | 0.56 | 0.14 | 35.1 |

Brick beside the windows: median luma {'P1': 119.1, 'P8': 92.1} (P1, P8); the frame's linear brightness over the brick's is **{'P1': 4.3, 'P8': 3.72}** (P1, P8): frames are about 4 times the wall on a photograph (film contrast included); the concept sheet's 7 is outside it (D9). The game's albedos give 0.82 / 0.13 = 6.3.

**Nets, curtains, blinds** (a hand count of every window whose state could be read, 60 windows in P1, P2, P3, P4, P6, P7, P12; Photo ±8 points): lower_sash_voile 28 (47%), full_height_net 13 (22%), cafe_net 1 (2%), curtains_drawn_or_open 6 (10%), blind 1 (2%), bare_dark_room 11 (18%). a net is a lower-sash voile in nearly half the windows and the upper sash is then clear: the room shows through it. The two held net pictures of the street (net_curtain_a, _b: a coarse square mesh of 7 to 10 mm, mean alpha 0.53, over the whole pane) match none of them (D2) **Paint** (60 windows, by eye): white 55%, cream or ivory 12%, dark or red-brown 13%, olive green 7%, blue 8%.

**What the photographs show in each window, element by element** (the list the build is judged against): the white frame member at each jamb 37 to 47 mm on a rear (P8) and 76 to 79 mm on a front (the lab's P6); a meeting rail that reads 34 mm of face and more with its shade (P8: 62 mm with the underside); a glazing bar of 22 to 27 mm (P8: 27 ±6); panes that differ from one another by up to 10 per cent in brightness (P8: six panes 86 to 105) and are smooth inside (std 4 to 5 levels); a dark edge between frame and net where the net hangs back from the glass (P1, P4); the near jamb's dark reveal beside a white lining at 10 to 20 degrees (P1, P13); a white painted sill and head in stone (P1, P3, P4); at under 10 degrees a white slit beside a dark void (P13). The nets: a gathered voile on the lower sash only with a lace band at the foot (P6, P7, P12), the upper sash clear, a full-height net on the tall windows (P4, P3), a net hanging a little askew or yellowed in an empty house (P14: no net at all, ply boarding), vertical louvres (P2, P11).

### 3.3 The game's rule for a room behind a house window

**The rule** (production/specs/shop-interiors.json, `tools/ue/make_interior_material.py` `trace`, imported by `hw_common.py` and never rewritten): on the room's centre line, d in front of the card plane, a camera frames the card rectangle W x H exactly; a room point (x, y, z) lands at u = 0.5 + (x / W) d / (d + y), v = 0.5 + (z / H - 0.5) d / (d + y). The material finds for each pixel where the eye's ray meets the room's box behind the card and looks that point up in the picture. d = W for every room here, as for the shops.

**The card is the room's front wall, not the window's glass.** The shops' card is the glass rectangle. A house window is a small hole (0.85 m) in the front wall of a room 2.8 or 3.4 m wide; a box as small as the hole would be a corridor. So the card here is **the whole room's front plane, 0.270 m behind the brick face**: the wall (215 mm of brick, the kit's box to 250.8) hides every part of the card outside the opening; the eye sees the room through the hole. 0.270 is 16 mm behind the nets (254) and 80 mm behind the lower glass (190); a ray through the window meets the card plane displaced sideways by 0.08 m x tan(angle off the normal), 0.30 m at 15 degrees from the wall, so every window stands at least 0.3 m inside its card (checked). The card's front face must not stand in front of the kit's box (250.8) and the carcass behind it starts at 0.29 or more.

| room family | W x H x D (m) | camd | floor above crown | window above the floor | picture | back wall in the picture (px, x0 y0 x1 y1) | who |
|---|---|---|---|---|---|---|---|
| UP (a first-floor room: one window centred in it; the flat's bay split in two rooms of 2.8 m) | 2.8 x 2.55 x 4.2 | 2.8 | 3.75 | 0.4736 to 2.15 | 1536 x 1399 | [460.8, 419.7, 1075.2, 979.2] | the 14 upper windows |
| GF (a cottage's front room: both windows look into the one room, 1.8 m apart) | 3.4 x 2.6 x 4.2 | 3.4 | 0.45 | 0.3736 to 2.05 | 3072 x 2349 | [848.8, 649.1, 2223.2, 1700.1] | the 6 cottage windows |

**Where the floors are** (Derived): a first-floor floor stands 0.25 above the shop's ceiling (3.5 above the crown: 3.4 + 0.1) at 3.75 and the ceiling at the eaves, 6.3; so the sill is 0.4736 above the floor and the head 2.15, leaving the 0.4 m of wall `head_below_ceiling_m` the scene file gives. A cottage's floor stands 0.35 above the footway (0.45 above the crown) and its ceiling at 3.05, under the eaves at 3.1 (Judgement).

**Why the pictures are 1536 wide (upper rooms) and 3072 wide (cottage rooms).** The window shows 0.85 / 2.8 = 30 per cent of an upper room's picture and 0.85 / 3.4 = 25 per cent of a cottage's. An upper window is never nearer than 2.6 m (standing 0.8 m out from the wall, the sill 2.5 m above the eye): a screen pixel is 2.3 mm at the game's 60 degrees over 1440 lines, the glass (0.78 m) about 340 pixels wide, over 427 texels at 1536 (548 a metre): 1.3 texels a pixel, sharp. From across the street (8.8 m, 39 degrees) it is 180 pixels over the same 427. A cottage's window is met at eye level, as near as 1.5 m from the glass (as the shops' honest range: nearer than that the nets, a real card, and the glass's own Fresnel carry the view): a pixel is 1.2 mm, the glass 650 pixels wide, over 704 texels at 3072 (903 a metre): 1.1 texels a pixel, just sharp; at 2048 it would be 1.4 pixels a texel and soft. The sizes are Derived; the picture heights follow from the card's proportions (1399 and 2349).

**What can be painted on a surface** (the third failure of 3 October, answered). An object painted on a surface that stands off it by s metres slides, as the eye moves, by the angle between the eye's ray to the object and to its painted place. `hw_common.budgets_for` computes, for the review cameras below and both mirror images of each pavement position, the greatest stand-off at which the slide stays within 20 pixels (reads true) and 40 pixels (tolerated) of a 2560 x 1440 frame, at the points the window actually shows (144 rays through the glass), the 15th percentile of the points, the smallest over the cameras:

| family | surface | reads true (20 px), m | tolerated (40 px), m |
|---|---|---|---|
| UP | back | 0.594 | 1.159 |
| UP | side | 0.035 | 0.068 |
| UP | ceiling | 0.032 | 0.064 |
| UP | floor | None | None |
| GF | back | 0.41 | 0.803 |
| GF | side | 0.03 | 0.061 |
| GF | ceiling | 0.021 | 0.042 |
| GF | floor | 0.018 | 0.037 |

**The rule the rooms keep** (the smaller of the two families' figures, rounded down; `rooms.budget_rule`): back 0.400 true, 0.800 tolerated; side 0.030 true, 0.060 tolerated; ceiling 0.020 true, 0.040 tolerated; floor 0.018 true, 0.037 tolerated. (An upper room's floor is never seen from the street; the cottages' floor figure stands.) Anything that would stand further off its surface is not drawn in the picture: a bed, a table, a free-standing chair are dropped; a chimney breast, a radiator, a stair's stringer are drawn flat (`rooms.forms`). **A pendant light's shade is the one real object in a lit room** (kit node `pendant__shade`), because it is what a lit upstairs window shows. The checks PIC-05 and the self-check test every object's and every form's stand-off against these numbers.

**What shows of a room, and so where its picture needs detail** (`rooms.visible_zone`, computed): 

- UP from H_ACROSS_0: back y [4.2, 4.2] z [1.78, 2.41]; ceiling y [0.85, 4.16] z [2.55, 2.55]
- UP from H_ACROSS_30: left y [1.55, 3.22] z [1.01, 2.54]; ceiling y [0.85, 2.95] z [2.55, 2.55]
- UP from H_ALONG_15_NEAR: left y [0.18, 0.46] z [0.97, 2.54]; ceiling y [0.08, 0.41] z [2.55, 2.55]
- UP from H_ALONG_30_NEAR: left y [0.47, 1.1] z [1.41, 2.55]; ceiling y [0.08, 1.21] z [2.55, 2.55]
- UP from H_ALONG_15_ROAD: left y [0.18, 0.42] z [0.79, 2.55]; ceiling y [0.2, 0.36] z [2.55, 2.55]
- UP from H_UNDER: ceiling y [0.0, 0.66] z [2.55, 2.55]
- GF from H_ACROSS_0: back y [4.2, 4.2] z [0.02, 2.37]; right y [2.83, 3.76] z [0.06, 2.33]
- GF from H_ACROSS_30: back y [4.2, 4.2] z [0.02, 2.37]; left y [4.19, 4.19] z [0.02, 2.37]
- GF from H_ALONG_15_NEAR: left y [0.63, 1.04] z [0.02, 2.52]; floor y [0.75, 0.75] z [0.0, 0.0]
- GF from H_ALONG_30_NEAR: left y [1.68, 3.64] z [0.02, 2.59]; floor y [0.75, 3.36] z [-0.0, 0.0]; ceiling y [1.23, 3.4] z [2.6, 2.6]
- GF from H_ALONG_15_ROAD: left y [0.57, 0.87] z [0.13, 2.26]
- GF from H_UNDER: right y [0.22, 2.06] z [0.02, 2.54]; floor y [0.39, 1.9] z [0.0, 0.0]; ceiling y [0.67, 1.93] z [2.6, 2.6]

an upper room is seen from the street as its ceiling and the top 0.6 m of its back wall (from across) or the first 0.5 m of one side wall (along the street, near): so its picture's detail is ceiling, cornice, picture rail, wall tops and tall furniture tops; a cottage's front room is seen at eye level: the whole back wall and the side walls.

**The review cameras** (street frame; eye 1.60 above the footway = 1.70 above the crown; 2560 x 1440): 

| camera | where | vertical field (deg) |
|---|---|---|
| H_ACROSS_0 | from the far pavement's kerb edge, square on to the window | 39.0 |
| H_ACROSS_30 | from the far pavement's kerb edge, 30 degrees off the window's normal toward the quay end | 39.0 |
| H_ALONG_15_NEAR | on the house's own footway 1.5 m from the wall, the window seen 15 degrees from the wall (5.6 m along) | 46.0 |
| H_ALONG_30_NEAR | on the house's own footway 1.5 m from the wall, the window seen 30 degrees from the wall (2.6 m along) | 46.0 |
| H_ALONG_15_ROAD | 2.6 m from the wall (the kerb edge of the road), the window seen 15 degrees from the wall (9.7 m along) | 39.0 |
| H_UNDER | 0.8 m from the wall, directly below the window (looking up) | 60.0 |

H_ACROSS_0 stands on the far pavement's kerb edge (8.8 m from the glass: the brief's 'about 8 m' is the nearest the far pavement allows); H_ALONG_15_NEAR and H_ALONG_30_NEAR are on the house's own footway 1.5 m from the wall, 5.6 and 2.6 m short of the window, which is the angle where 1a found the white boards; H_ALONG_15_ROAD is 9.7 m along from 2.6 m out (the road's kerb edge); H_UNDER is 0.8 m from the wall, looking up. For the cottages the far pavement is the east footway.

## 4. The kinds

### 4.1 Two over two (S22) and one over one (S11): the lab's checked sash, reused

The sash is the lab's, amended on 8 October for Jafar's ruling (`production/art/sash-window/target.json`, models `production/assets/sash-window/sash_window.glb` and `sash_window_1over1.glb`, reviewed on narrow points). Nothing is redrawn: this unit changes its glass (section 5), shades its box (5.4), adds its nets and its room (6, 7), and applies it to every row. **Numbers read from the lab's file** (the self-check re-reads them): opening 850.0 x 1676.4; frame reveal 114.3; outer lining margin 42.9 (so each jamb shows 3 in of painted timber, 76.2); head visible 44.5; stile 50.8, top rail 50.8, bottom rail 101.6, meeting rail 38.1 deep, glazing bar 22.2 (one vertical bar in each sash of the S22; none on the S11), thickness 34.9, horns 76.2 long on the upper sash only, glass 2.5.

**Glass planes** (Read from the lab's glb; 1a): the upper glass 142.0 mm behind the brick face, the lower 190.0. The sill: an oak sill 41.3 high at the front; the stone sill and the segmental arch belong to the wall kit (stone sill 127 high, 50.8 proud, 76.2 wider than the opening each side; the arch ring 215, rise one seventh of the span, 12 proud: terrace-front.py). **Horns:** ogee horns on the upper sash's stiles (76.2 below the meeting rail), none on the lower. **Reveal:** the brick reveal is half a brick, 102.5 (the street file), the lab's frame stands 114.3 back from the face.

The lab's kit has **41 nodes** in the S22 (1068 triangles, 72988 bytes) and 35 in the S11 (860 triangles). Each node's bounds in the kit frame are in `kinds.S22.lab_nodes` and `kinds.S11.lab_nodes` (the self-check re-reads the glb and compares). **Photographs win** where they disagree with the book: the lab already followed P6 for the frame; P8 reads the bar at 27 ±6 (22.2 kept, D6), the jamb of a rear at 37 to 47 mm (the front's 76.2 kept, D7) and the meeting rail with its shade at 62 mm (38.1 kept, D10).

### 4.2 Paint, colour and condition by house

| paint | sRGB | linear | roughness | note |
|---|---|---|---|---|
| white_fresh | [234, 233, 229] | [0.82, 0.812, 0.78] | 0.42 | the street's paint_joinery as it stands (terrace-front.py MATERIALS); the lab's sash and the 4.1/3.2 kits use it |
| white_grimy | [214, 212, 205] | [0.68, 0.66, 0.62] | 0.48 | weathered 1990 gloss white, 1a's 0.72 to 0.80 less the dirt in the lower rails and the sill: the lower rail and sill at x 0.85, the rest 1.0 |
| white_flaking | [205, 202, 192] | [0.6, 0.58, 0.53] | 0.55 | an unlet house's paint: 12 per cent of the area on the lower rails, sill and stiles' feet is flaked to grey primer (66, 60, 54) or bare timber (96, 66, 40) |
| cream | [222, 204, 164] | [0.73, 0.6, 0.37] | 0.45 | P3's cream-painted sashes (frame sampled 181, 163, 131 in the sun and shade of the photograph, so the paint is lighter), P2's cream render |
| olive | [136, 140, 64] | [0.246, 0.262, 0.052] | 0.45 | P12's two olive-green sashes (sampled 148, 153, 70); a painted window of a house that chose its own colour |
| blue | [56, 92, 160] | [0.04, 0.107, 0.352] | 0.42 | P2's blue sashes (sampled 61, 87, 136), the tenants' own paint on a terrace of one owner |
| bronze | [74, 60, 52] | [0.05, 0.038, 0.03] | 0.35 | the street's frame_bronze (terrace-front.py): dark anodised aluminium; NOT seen in any reached photograph (D1), kept for the one metal-refit house |
| white_upvc | [232, 231, 225] | [0.8, 0.792, 0.762] | 0.3 | white replacement frame, satin: P6, P7, P11 show white in every case (4 of 4) |

| house | kind | paint | condition |
|---|---|---|---|
| east_chandler_bay0 | RC | bronze | sound |
| east_parade_bay0 | S22 | white_grimy | grimy |
| east_parade_bay1 | S11 | cream | sound |
| east_parade_bay2 | RC | white_upvc | sound |
| east_parade_bay3 | S22 | white_flaking | flaking |
| east_parade_bay4 | RC | white_upvc | sound |
| east_parade_bay5 | S11 | olive | sound |
| west_south_bay0 | S11 | blue | grimy |
| west_south_bay1 | RC | white_upvc | sound |
| west_south_bay2 | S22 | cream | sound |

**Which the photographs support.** White paint is 55 per cent of the 60 windows; cream or ivory 12, dark or red-brown 13, olive 7, blue 8 (a council terrace painted by its tenants: P2). The 1980s and 1990s replacement is **white** in every photograph reached (P6, P7, P11): the brown or bronze anodised frame the street file draws for every replacement is not in one of them (D1). So the replacement is white satin by default and bronze for one house only, the ship chandler's (a metal-refit shop; Judgement, marked). A council replacement in the photographs is the Newburn casement (P11): a fixed light under a top-hung light, white, with nets and vertical drapes: it is the RC kind. **Condition:** `sound` is the paint as in the table; `grimy` multiplies the lower rail and sill by 0.85 and darkens the box's inside corners (the shade already does it) with a grime band 30 mm high along the sill; `flaking` (the unlet flat): 12 per cent of the area on the lower rails, the sill and the stiles' feet is flaked to grey primer (66, 60, 54) or bare timber (96, 66, 40).

### 4.3 The replacement casement (RC)

A fixed light under a top-hung light, no bars, in the same 850 x 1676.4 opening (the street's `REPLACEMENT_TRANSOM` 0.72 and the photographs' 0.66 (P6), 0.72 (P7), 0.75 (P11): the street's value stands). **One transom and equal lights** (unit 7's toplight fault does not arise: there are no bars, one transom, and the top light is a single pane). The parts, in the kit frame (mm): frame face 60, depth 70, front 72.5 behind the brick face (the reveal's 102.5 less 30 proud); transom face 70, centred at 1207.0 above the opening's bottom; the top-hung light's sash stiles 45 with a 4 dark gap; glass 4 mm (a sealed unit drawn as one pane, section 5.5) at 112.5 behind the face; a gasket line 3 wide at luma x 0.30 and a welded-corner groove 2 wide at x 0.35 at each corner of each sash.

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
| glass_lower | [-347.0, 347.0] | [112.5, 116.5] | [78.0, 1154.0] | glass_house |
| glass_top | [-316.0, 316.0] | [112.5, 116.5] | [1291.0, 1567.4] | glass_house |

Glass sightlines: lower [694.0, 1076.0], top [632.0, 276.4] (mm). The top light is hinged at its head and opens outward in the photographs (P11, P14: one stands open): a closed light is drawn; the open one is a variant the PC may add (not required).

### 4.4 Sills, heads and arches, and what the kit does not carry

The stone sill (127 high, 50.8 proud, 76.2 wider each side than the opening), the segmental arch (ring 215, rise one seventh, 12 proud) and the brick returns of the reveal are the wall kit's, not this unit's; this target names the shade the wall kit must give the returns (section 5.4). **Brick returns**: 0.8 of the wall's value at the face falling to 0.6 at the sash, 0.7 under the head.

### 4.5 Nothing left open

Every opening is covered above and around its parts: the opening is 850 x 1676.4 and the frame's outer lining runs 65 mm beyond it each side behind the brick (S22/S11), or the RC's jambs fill it to the brick (60 face); the head is the lab's head lining (S22/S11) or the RC's head rail; nothing is left bare between the head and the stone arch (the arch's soffit and the brick return are the wall kit's, as the shopfront's were), and between the sill and the oak sill the sash's bottom rail runs to the stone sill. The self-check KIT rows confirm that every pane and every net lies inside the opening and that no RC member overlaps another; the drawing (target_drawing.py) shows the opening covered.

## 5. The glass: the 1a fix as numbers

### 5.1 The pane

**The game's pane** (research 1a, step 1): one opaque Default Lit material on the pane (research 1a, step 1): base colour = lerp(room 0.03, lace x 0.6, the net's alpha) with the alpha WIRED; Specular 1.0 (F0 0.08, standing for both faces of a single pane); roughness 0.03; metallic 0; day emissive 0. The pane is a real glass surface: its reflectance and roughness are the game's. **What the cloud render uses to stand in for it:** Cycles Principled BSDF, NOT Glass BSDF: Base Color 0.03 (linear grey) with the net card's alpha as the mix, Specular IOR Level 1.0, Roughness 0.03, Transmission 0, Metallic 0, the room card (baked through `trace`) as Emission x (1 - Fresnel) x brightness; the opposite row and the sky dome are what it reflects (Cycles traces them; Lumen's reflections and the box-projected street cube are the game's).

**Two-face reflectance of float glass** (n 1.52, unpolarised, the reflections between the faces counted: Derived, recomputed by the self-check; 1a's table is 0.02 to 0.03 higher at 16 to 30 degrees) by the angle from the wall: 90 degrees 0.082, 30 degrees 0.157, 24 degrees 0.215, 18 degrees 0.314, 16 degrees 0.360, 10 degrees 0.544, 8 degrees 0.622. angle from the wall; float glass n 1.52, both faces, unpolarised, the reflections between the faces counted (Derived, recomputed by self_check.py: 1a's table is 0.02 to 0.03 higher at 16 to 30 degrees); Unreal's Specular 1 (F0 0.08, Schlick) gives 0.26 at 16 degrees, about three quarters of true: close enough

### 5.2 Old glass's waviness

per-pane tilt, not a wave texture: each pane mesh is rotated by a seeded angle uniform in +-0.5 degrees about the vertical axis and +-0.3 degrees about the horizontal one (never zero, the spread of a window's panes at least 0.3 degrees) **Photographs:** P8 (Oxford rear, 1987): six panes of two original sashes read mean luma 86, 87, 99, 102, 105 (neighbouring panes differ by up to 19 levels, 10 per cent) and a smooth tone inside each pane (std 4 to 5 levels at 70 px a window): the glass is flat to the eye and each pane catches the sky differently. No wave normal map: the glass looks flat on the photographs.

### 5.3 Dirt and reflections

a 6 mm band round every pane's edge is roughened (roughness 0.35, base colour x 0.8): the putty line's dirt; the lowest 25 mm of each pane carries the same (water and dust on the bottom rail) **Reflections by floor:** upper panes: from across the street a ray off an upper pane goes up at the eye's own elevation (18 to 22 degrees) and meets only sky (the west row's roofs are 3 m eaves; the ray is 9 m up by the west frontage): the pane carries the SKY at 8 per cent and the room at 92 per cent; P8 (blue-grey 87, 99, 135) shows it. Ground panes: a ground pane across the street reflects the opposite row at eye height: the parade's dark fascias and the hill's trees: a darker band; the room dominates.

### 5.4 The box shaded and its dark lines drawn

1a step 2 as numbers, put in the joinery's vertex colour (COLOR_0 red channel multiplies the paint; not the AO pin). Numbers (1a step 2, Judgement from 1a's photograph-9 figures; the check KIT-09 reads them back from the exported file):

| part | red channel of COLOR_0 (x paint) | note |
|---|---|---|
| lining, from the brick edge to the glass | 1.0 at y = 0 falling linearly to 0.6 at the glass plane | the sash's own lining and the outer lining's face |
| the track faces | 0.5 | the faces of the pulley-stile track between the parting bead and the staff bead |
| inside corners | 0.3 within 8 mm of a concave edge | photograph 9's corner line 105 to 125 against a lining of 220 to 250 |
| the putty and shadow line round each pane | 0.35, 6 mm wide | the kit's putty strips (14 on a 2/2) are 6.4 mm wide: painted 0.35 |
| the meeting rail's underside | 0.4 | the lower rail of the upper sash seen from below |
| the parting bead's gap | 0.10 over 6 mm | the gap itself is a 2 mm geometric gap |
| the brick returns of the reveal (wall kit) | 0.6 to 0.8 | in the wall mesh, not the kit; stated so the wall kit takes it: 0.8 at the face falling to 0.6 at the sash, and 0.7 under the head |

Keep the paint's albedo at [0.78, 0.8] and roughness 0.40 (try 0.35 once: a traced sheen). **Every dark line of the box is at least 6 mm wide** (1 pixel at 10 m is 5.9 mm at 1440 lines and 46 degrees): the lab's putty strips are 6.4 wide, the parting bead's gap is 2 mm but its shade is painted over 6 mm each side, the RC's gasket and weld groove are shaded over 6 mm. Check KIT-10.

### 5.5 What this cannot reach

The real sealed unit of the replacement reflects from four faces (about 0.14 at normal incidence); Unreal's Specular 1.0 caps at F0 0.08, so the replacement's pane under-reflects; and the game's own reflections (Lumen, the box-projected street cube, the Fresnel hand-over) are not in the cloud. Both are in `could_not_settle` and `owed_on_pc`.

## 6. Nets, curtains and blinds

All are **cards** (two triangles each) behind the glass, in front of the room's card; their alpha is the weave. Planes are in millimetres behind the brick face; z is up from the opening's bottom edge. The two held net pictures (`net_curtain_a`, `_b`: a coarse square mesh of 7 to 10 mm, mean alpha 0.53) match none of the photographs' nets and are not used (D2).

| net | name | what | card (mm) | plane (mm behind the face) | voile coverage | lace band share of height | share of the photographs' windows |
|---|---|---|---|---|---|---|---|
| N0 | bare glass | no net: the room is seen (dark by day) | - | - | - | - | 18% |
| N1 | lower-sash voile | a gathered voile on a wire at the meeting rail, hem near the sill; the upper sash clear | x [-450, 450], z [60, 880] | S22/S11 254, RC 235 | 0.4 | 0.3 | 47% |
| N2 | full-height net | a gathered net from a rod at the head to a hem near the sill | x [-450, 450], z [60, 1630] | S22/S11 254, RC 235 | 0.4 | 0.18 | 22% |
| N3 | cafe net | a half-height net on a rod across the lower sash: covers the lower third of the window only | x [-430, 430], z [100, 500] | S22/S11 254, RC 235 | 0.45 | 0.0 | 2% |

**The fabric** (all nets): plain voile: threads under 1 mm, a pitch of 1.2 mm, so under one pixel from 1.5 m outwards: the net reads as an even translucent sheet with fold shading; only the lace band shows a pattern (repeat 60 mm) and only from under 3 m. one layer covers 0.40 (voile) to 0.62 (lace band) of its area; gathered at 200 per cent fullness the folds overlap so the mean covered share of the sheet is 1 - (1 - 0.40)^2 = 0.64 voile, 0.86 lace band (Derived); the card's alpha is the weave and folds. Gathered at 200 per cent fullness, the fold wavelength [40, 55] mm, depth 12 mm (a normal and brightness map, not geometry), brightness modulation ±22 per cent. Hem: a lace border 28 mm high, scalloped, period 35 mm; the hem sags up to 12 mm between folds (the lower edge is a gentle sine of amplitude 6 mm and wavelength 90 mm). Head: a 20 mm double-thickness casing at the top (alpha 0.92) with a 2 mm dark wire line under it (alpha 0.5, luma 60). **Colours** (sRGB): white [238, 238, 232], greyed [208, 208, 200], yellowed (nicotine) [222, 206, 158]: P1 sampled a sunlit white net at (208, 201, 181); nets read 0.60 to 0.97 of the frame's luma in the photographs (n=9). **By day:** lit from outside by daylight: albedo x lit by the street's sky and the window's own shadow; the net is NOT emissive by day (net_day_gain 0.0, unreal-look.json). **Night, lit:** emissive warm tungsten: linear (1.0, 0.714, 0.344) (vignette-pieces window_practicals gamma (1, 0.86, 0.62); the street's interior_lit) x the lit-net strength 1.2 x room_glow_gain_night 0.4 = 0.48 (unreal-look.json); folds darker, the room's pendant and furniture seen through it. **Night, dark:** unlit: net emissive 0.05 x 0.4 = 0.02 (the street's NET_EMIT_NIGHT 0.05): only the sodium lamp's colour on its fabric. a net 65 mm behind the glass moves under a pixel at 10 m (1a): a flat card, not geometry

| kind | name | what | card (mm) | plane | opacity | folds or slats | colours | night, lit |
|---|---|---|---|---|---|---|---|---|
| C1 | curtains drawn | lined curtains drawn across the whole window, in front of the net | {'x': [-480, 480], 'z': [0, 1780]} | 262 | 0.97 | wavelength 70 to 90 mm, brightness modulation 0.25, straight hem, a pelmet band 60 mm high at the top | {'cream': [214, 198, 166], 'brown': [110, 82, 62], 'green': [72, 98, 74]} | colour x warm light x 0.35 transmission: the curtain glows its own colour, folds dark |
| C2 | curtains open | a pair drawn back to the sides, two cards each 170 wide | {'x': [-480, -310], 'z': [0, 1780]} | 262 | 0.97 | as C1 | {'cream': [214, 198, 166], 'brown': [110, 82, 62], 'green': [72, 98, 74], 'floral_cream': [224, 210, 180]} | as C1 |
| B1 | venetian blind | a white aluminium venetian blind lowered 60 per cent of the height (z 660 to 1650), slats 25 mm, tilted closed 70 per cent | {'x': [-400, 400], 'z': [660, 1650]} | 240 | slat gaps 0.25 | slat pitch 25 mm | [210, 210, 205] | slat gaps glow warm: stripes of light at the 25 mm pitch (visible under 8 m) |
| B2 | roller blind | a cream roller blind half down (z 700 to 1660) with a pull cord and a 20 mm bottom batten | {'x': [-390, 390], 'z': [700, 1660]} | 240 | 0.9 | slat pitch - mm | [226, 214, 176] | an even warm sheet of colour x 0.5 transmission, a dark bottom batten |
| B3 | vertical louvre blind | white vertical louvres 89 mm, turned 40 per cent open (P2's ground window) | {'x': [-420, 420], 'z': [100, 1640]} | 240 | slat gaps 0.35 | slat pitch 89 mm | [226, 226, 220] | vertical stripes of warm light at the 89 mm pitch |

**Per house** the street's mix is in the table of section 1 (net kind and colour, drape): the upper sash is clear wherever the net is N1, N3 or none, so the room shows through it; a torn yellowed net hangs askew in the empty flat (one lower corner off its wire, the hem 80 mm out of true). **Drawn curtains** stand in front of the net and cover the window; open curtains stand 170 mm wide at each side. A lit room behind a lit net reads as the net's own glow (emissive 0.48) with the room's pendant and the top of the back wall seen through it.

## 7. The rooms behind the windows

### 7.1 The format

Each room is built by script from CC0 models in Blender (Cycles), rendered to the shop rooms' picture format: <room_id>_<state>.png with <room_id>.json beside them (room, w, h, d, camera_d, pixels, states, made_by, samples); 8-bit sRGB PNG; Cycles 128 samples, denoised; masters on F:/LedgerTools/house-rooms. Three states: `day`, `night_lit`, `night_dark`. the render camera stands on the room's centre line d = W in front of the card, framing the card rectangle W x H exactly; the game's `trace` is imported, not rewritten. **Brightness** (the game's emissive scale): day 0.12, night 0.7 (day 0.12 (a front room by day is a dim ceiling and a dark wall; the shops' 0.15 is for a lit display), night 0.7 as the shops (shop-interiors.json); the pane composite measured in the gate decides). **Picture standards** (Judgement, scaled from the approved pawnbroker pictures' 119.5 / 79.8 / 17.7): mean luma day 105.0, night_lit 70.0, night_dark 15.0, within ±15 per cent; the checks' floors are 0.7 of them (Judgement, scaled from the approved pawnbroker pictures (119.5, 79.8, 17.7 measured 12 October) by the rooms' smaller windows and fewer lights: the checks' floors are 0.7 of these).

**Lights per state:** day: an overcast area light the size of the card on its plane (6500 K), strength set so the picture's mean luma meets the day standard; no tungsten. Night, lit: the pendant (a paper shade, a 60 W tungsten bulb 2700 K, linear (1.0, 0.714, 0.344)) at the ceiling rose, 0.30 below the ceiling, and in the front rooms a table lamp's glow on the back wall; a television glow (cool 6500 K, emissive screen) where tv_glow; landings and empty rooms: a bare 40 W bulb or none (empty: night_lit = night_dark). Night, dark: the sodium wash through the window: linear (1.0, 0.25, 0.0) = production/specs/unreal-look.json lantern_linear_rgb (NOT the scene file's stale (1, 0.7055, 0)), at 6 per cent of night_lit's energy; nothing else.

### 7.2 The thirteen rooms

**Variants so a row does not repeat visibly:** three lounges, three bedrooms, two landings, two empty rooms, three cottage front rooms; no (room, net, drape) triple repeats within three places on a row (checked); the three lounges and the three bedrooms differ in their walls and in their back-wall pieces (checked).

| room | type | W x H x D (m) | walls / ceiling / floor | objects (class, stand-off m) | scripted flat forms | light | picture px |
|---|---|---|---|---|---|---|---|
| up_lounge_1 | lounge | 2.8 x 2.55 x 4.2 | wallpaper_floral / ceiling_white / boards | wooden_bookshelf_worn (tolerated 0.58), ornate_mirror_01 (true 0.03), hanging_picture_frame_03 (tolerated 0.03) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_lounge_2 | lounge | 2.8 x 2.55 x 4.2 | emulsion_magnolia / ceiling_white / boards | vintage_cabinet_01 (tolerated 0.67), mantel_clock_01 (tolerated 0.67), hanging_picture_frame_01 (true 0.02) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_lounge_3 | lounge | 2.8 x 2.55 x 4.2 | wallpaper_stripe / ceiling_white / carpet_brown | Shelf_01 (true 0.26), hanging_picture_frame_02 (true 0.03), wall_clock (tolerated 0.05) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_bedroom_1 | bedroom | 2.8 x 2.55 x 4.2 | wallpaper_floral / ceiling_white / carpet_brown | vintage_cabinet_01 (tolerated 0.67), hanging_picture_frame_03 (true 0.03) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_bedroom_2 | bedroom | 2.8 x 2.55 x 4.2 | emulsion_cream / ceiling_white / boards | drawer_cabinet (tolerated 0.49), ornate_mirror_01 (true 0.03), hanging_picture_frame_01 (true 0.02) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_bedroom_3 | bedroom | 2.8 x 2.55 x 4.2 | wallpaper_stripe / ceiling_white / carpet_brown | Shelf_01 (true 0.26), hanging_picture_frame_03 (true 0.03), wall_clock (tolerated 0.05) | skirting, picture_rail, coving, ceiling_rose | pendant | 1536 x 1399 |
| up_landing_1 | landing | 2.8 x 2.55 x 4.2 | emulsion_pale_green / ceiling_white / lino | hanging_picture_frame_01 (true 0.02), wall_clock (true 0.05) | skirting, picture_rail, coving, stair_flat, internal_door_flat, bare_bulb | bare bulb | 1536 x 1399 |
| up_landing_2 | landing | 2.8 x 2.55 x 4.2 | emulsion_cream / ceiling_white / lino | Shelf_01 (true 0.26), hanging_picture_frame_02 (true 0.03) | skirting, picture_rail, coving, radiator_flat, bare_bulb | bare bulb | 1536 x 1399 |
| up_empty_1 | empty | 2.8 x 2.55 x 4.2 | stripped_paper / ceiling_white / boards | none | skirting, coving, chimney_breast_flat, bare_bulb, picture_ghost | bare bulb | 1536 x 1399 |
| up_empty_2 | empty | 2.8 x 2.55 x 4.2 | peeling_paint / ceiling_white / boards | none | skirting, coving, bare_bulb, radiator_flat | bare bulb | 1536 x 1399 |
| gf_front_1 | front_room | 3.4 x 2.60 x 4.2 | wallpaper_floral / ceiling_white / carpet_brown | Sofa_01 (tolerated 0.66), side_table_01 (tolerated 0.45), television_02 (tolerated 0.45), hanging_picture_frame_02 (true 0.03), hanging_picture_frame_03 (tolerated 0.03) | skirting, picture_rail, coving, ceiling_rose, fire_surround_flat | pendant | 3072 x 2349 |
| gf_front_2 | front_room | 3.4 x 2.60 x 4.2 | emulsion_magnolia / ceiling_white / boards | wooden_bookshelf_worn (tolerated 0.58), ArmChair_01 (tolerated 0.77), potted_plant_01 (tolerated 0.64), ornate_mirror_01 (true 0.03) | skirting, picture_rail, coving, ceiling_rose, internal_door_flat | pendant | 3072 x 2349 |
| gf_front_3 | front_room | 3.4 x 2.60 x 4.2 | wallpaper_stripe / ceiling_white / carpet_brown | painted_wooden_cabinet (tolerated 0.62), mantel_clock_01 (tolerated 0.62), vintage_oil_lamp (tolerated 0.62), painted_wooden_bench (tolerated 0.50), hanging_picture_frame_01 (true 0.02) | skirting, picture_rail, coving, ceiling_rose, fire_surround_flat | pendant | 3072 x 2349 |

**Finishes** (Poly Haven textures at 1k, tinted; roughness in words and 0-1): emulsion_magnolia: matt magnolia emulsion (linear [0.6, 0.52, 0.38], roughness 0.8); emulsion_cream: matt cream emulsion (linear [0.66, 0.6, 0.42], roughness 0.8); emulsion_pale_green: pale green emulsion (a landing) (linear [0.4, 0.48, 0.36], roughness 0.8); wallpaper_floral: a damask-pattern paper from the jacquard texture tinted fawn (linear [0.42, 0.33, 0.26], roughness 0.7); wallpaper_stripe: a script-drawn vertical stripe: cream and fawn, 90 mm period (linear [0.55, 0.5, 0.36], roughness 0.7); stripped_paper: old paper stripped in strips, bare plaster between (linear [0.3, 0.27, 0.22], roughness 0.9); peeling_paint: paint peeling to grey plaster (linear [0.38, 0.22, 0.2], roughness 0.9); ceiling_white: white emulsion on a textured ceiling, yellowed by tobacco in the lived-in rooms (x 0.92) (linear [0.72, 0.7, 0.64], roughness 0.9); boards: dark-stained floorboards (linear [0.2, 0.12, 0.06], roughness 0.6); carpet_brown: a worn brown carpet tinted from the dirty-carpet texture (linear [0.12, 0.08, 0.05], roughness 0.95); lino: brown linoleum (a landing) (linear [0.3, 0.2, 0.1], roughness 0.5).

**Scripted flat forms** (every one inside the budgets of its surface): skirting: painted white, on all three walls; picture_rail: ; coving: a cove drawn as a 55 mm band shaded like a cove, 0.02 proud (a real 55 mm cove is over the ceiling budget); ceiling_rose: a plaster rose at the pendant's place: tolerated class on the ceiling (0.03 over 0.02, under 0.04); bare_bulb: a flat glowing disc (a pendant of bare bulb on its flex: the flex is not drawn); fire_surround_flat: a tiled fire surround drawn flat (the real one stands 0.18 off the wall: over the budget); internal_door_flat: a four-panel internal door, panels 0.02 proud; radiator_flat: a pressed-steel radiator drawn flat (the real one stands 0.08 off: over the budget); stair_flat: the stringer and handrail of the flight along the side wall drawn as flat strips (the handrail 0.9 to 1.0 above the nosings, rising 36 degrees); balusters not drawn; chimney_breast_flat: a chimney breast drawn flat (the real one stands 0.23 off the wall); picture_ghost: a pale rectangle on a stripped wall where a picture hung (painted, no stand-off).

**What each type shows from the street.** *Upper lounges and bedrooms*: the ceiling with its rose, cove and pendant, the wall tops under the picture rail, the tops of tall furniture, a picture hung high; at night, a warm ceiling and the shade. *Landings*: the stair's flat stringer and handrail up the side wall, a half-glazed door at the back, a bare bulb. *Empty rooms*: stripped paper or peeling paint, a flat chimney breast, a pale ghost where a picture hung, bare boards, a bare bulb flex; by night they are dark whatever the table says. *Cottage front rooms*: eye-level: sofa or armchair against the back wall, a cabinet with a clock and a lamp, the television on a small table (a cool glow at night in front room 1), pictures, a fire surround drawn flat.

### 7.3 Which windows are lit at night

Judgement. production/research/evening-light-1990 gives no share (its windows line: 'whitish fluorescent from shops, warm tungsten behind house curtains', marked its own inference); the street already lights one in three at 20:30 (terrace-front.py NET_LIT_EVERY = 3) and two cottage windows always (NET_LIT_ALWAYS). No 1975 to 1995 night photograph of a terrace was reached (no Geograph result before 1996 for night, dusk or lit windows). Kept near the street's one in three; the rest of the day follows habit (lights on at dusk, out by midnight).

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

a window is lit at hour h when its place in the lit order is below round(share(h) x 20); the order is fixed (below) and never reshuffled, so a window lit at 23:00 is lit at 20:30; empty rooms are never lit; the two cottage windows of the always-lit house are lit from 18:00 to 23:00 whatever the share **At 20:30, seven lit (35 per cent):** east_chandler_bay0_upper_w1, east_parade_bay0_upper_w1, east_parade_bay2_upper_w1, east_parade_bay4_upper_w1, west_south_bay1_gf_w1, west_south_bay2_gf_w0, west_south_bay2_gf_w1. **The fixed lit order** (after the always-lit pair): west_south_bay1_gf_w1 > east_parade_bay4_upper_w1 > east_parade_bay2_upper_w1 > east_parade_bay0_upper_w1 > east_chandler_bay0_upper_w1 > east_chandler_bay0_upper_w0 > east_parade_bay4_upper_w0 > east_parade_bay0_upper_w0 > east_parade_bay2_upper_w0 > west_south_bay1_gf_w0 > east_parade_bay1_upper_w0 > west_south_bay0_gf_w1 > east_parade_bay5_upper_w0 > east_parade_bay1_upper_w1 > east_parade_bay5_upper_w1 > west_south_bay0_gf_w0. no window is lit by day; a lit room by day would be invisible in the glass's reflection.

### 7.4 The inventory

**44 Poly Haven models were looked at at 1k (base colour map, 13 October); 18 are used in the rooms; 17 textures.** Every id exists in the live catalogue (`self_check.py --live` re-reads it) and is CC0. A mark found on a map is blanked (painted out to the surface's own colour) before the model is used, or the model is not used; every framed picture's artwork is replaced by a script-drawn print (flat grey-green landscape band under a pale sky, no text). Never used: `fancy_picture_frame_02` (its painting shows a group of figures including children).

| model | dims mm (x y z) | polycount | used in | status | marks seen at 1k |
|---|---|---|---|---|---|
| ArmChair_01 | [848.4, 765.8, 1065.1] | 5626 | gf_front_2 | none | none |
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
| drawer_cabinet | [1141.1, 488.1, 1881.3] | 26406 | up_bedroom_2 | none | none |
| fancy_picture_frame_01 | [603.0, 20.0, 464.1] | 938 | - | looked at, not used | artwork is a landscape painting with tiny riders: NOT USED (the frames above are enough) |
| fancy_picture_frame_02 | [660.6, 89.0, 771.0] | 35102 | - | excluded: children | artwork is a street scene painting with a group of figures including children: NEVER USED (content rule: no children, even painted) |
| hanging_picture_frame_01 | [594.0, 15.7, 841.0] | 2586 | gf_front_3, up_bedroom_2, up_landing_1, up_lounge_2 | replace_artwork | artwork map reads 'Ray Homes / Photo: 76cm x 51cm / Frame: 84cm x 59cm' (a maker's name): the whole artwork map is REPLACED by a script-drawn print (a flat grey-green landscape band under a pale sky), no text |
| hanging_picture_frame_02 | [751.8, 33.1, 500.0] | 3678 | gf_front_1, up_landing_2, up_lounge_3 | replace_artwork | artwork map is a painting of a palace signed 'Celine.F' (an artist's signature and a royal building): REPLACED by a script-drawn print |
| hanging_picture_frame_03 | [385.0, 31.8, 502.4] | 24348 | gf_front_1, up_bedroom_1, up_bedroom_3, up_lounge_1 | replace_artwork | artwork map is a photograph of a Japanese castle (not 1990 Britain): REPLACED by a script-drawn print |
| mantel_clock_01 | [483.7, 250.8, 160.9] | 29742 | gf_front_3, up_lounge_2 | none | none (a plain dial) |
| modern_wooden_cabinet | [2440.0, 520.0, 680.1] | 24976 | - | looked at, not used | none; a modern piece: NOT USED |
| old_bed_frame | [904.7, 2001.7, 1201.5] | 49990 | - | looked at, not used | none; its headboard is under the visible zone: NOT USED |
| ornate_mirror_01 | [486.5, 26.0, 744.2] | 14246 | gf_front_2, up_bedroom_2, up_lounge_1 | none | none |
| painted_wooden_bench | [1164.9, 496.5, 889.3] | 630 | gf_front_3 | none | none |
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
| television_02 | [399.7, 350.2, 411.4] | 2310 | gf_front_1 | blank | a small rating plate on the back panel: blanked; no text on the front |
| throw_pillows_01 | [1021.6, 627.5, 450.2] | 6362 | - | looked at, not used | none |
| vintage_cabinet_01 | [2021.8, 669.8, 2235.1] | 61096 | up_bedroom_1, up_lounge_2 | none | none (a cream paper sheet with a hexagon pattern on map a) |
| vintage_day_bed | [1972.6, 854.8, 1127.3] | 2715 | - | looked at, not used | none; 0.855 deep: NOT USED |
| vintage_oil_lamp | [220.0, 220.0, 801.6] | 7208 | gf_front_3 | none | none |
| vintage_suitcase | [1608.2, 239.2, 567.9] | 16474 | - | looked at, not used | the second suitcase's map carries about a dozen travel stickers (real places or lines): NOT USED |
| vintage_wooden_drawer_01 | [1715.1, 1006.9, 1090.8] | 5184 | - | not used | not looked at (1.0 deep: over budget) |
| wall_clock | [320.5, 47.2, 320.5] | 3658 | up_bedroom_3, up_landing_1, up_lounge_3 | blank | 'URBAN quartz' on the dial: painted out to the dial's white (a maker's name) |
| wicker_basket_01 | [383.2, 295.0, 117.4] | 22276 | - | looked at, not used | none |
| wooden_bookshelf_worn | [1374.0, 581.3, 2063.4] | 10106 | gf_front_2, up_lounge_1 | none | none |

**Textures** (1k base colour looked at, no marks seen): ceiling_interior, decrepit_wallpaper, dirty_carpet, floral_jacquard, linoleum_brown, old_wooden_floor_02, painted_plaster_wall, peeling_painted_wall, plastered_wall_04. **Brand blocklist** (the self-check scans every string of target.json outside a marks entry for these): dixons, currys, comet, rumbelows, vtech, ray homes, celine, lorex, ingrid, radolier, hotpoint, kenwood, ekco, anglian, royal mail, post office, tesco, woolworth, sainsbury, ikea, dulux. every model's base colour map was looked at at 1k on 13 October 2026 before it was named; a model with a mark is blanked in its map (the mark painted out to the surface's own colour) before it is used, or not used; every framed picture's artwork is replaced by a script-drawn print.

## 8. As kit pieces

**Frame and pivot.** kit frame (units): x across the window, y into the wall (0 at the brick face), z up (0 at the opening's bottom edge); the lab glb's frame is glTF y-up with the wall at negative z: kit (x, y, z) = (x_glb, -z_glb, y_glb). the opening's bottom-edge centre on the brick face: (0, 0, 0); the street toward -y; z up; metres, scale 1. **Placement:** east: translate (x_centre, +5.125, sill_z_above_crown); the street is at -y, no turn; west: turn 180 degrees about z, then translate (x_centre, -5.125, sill_z_above_crown); above the crown: the site's `sill_z_above_crown` (the opening's bottom edge); the stone sill and the arch ring belong to the wall kit.

**Files:** S22 = production/assets/cloud-week/house-windows/hw_S22.glb; S11 = production/assets/cloud-week/house-windows/hw_S11.glb; RC = production/assets/cloud-week/house-windows/hw_RC.glb; production/assets/cloud-week/house-windows/hw_room_card_gf.glb (the cottages' shared room card, one per house, placed between its two windows). **Budget:** 6000 triangles and 400000 bytes each; the lab's 2/2 is 2,000 or so triangles; nets, curtains and blinds are cards (2 triangles each); the push guard allows 1 MB a model in git

**S22: added nodes** (the lab's 41 nodes are reused as they are for S22 and S11; the RC's parts are in section 4.3):

| node | material | x (mm) | y into the wall (mm) | z up (mm) | note |
|---|---|---|---|---|---|
| glass__lower_L | glass_house | [-357.3, -4.7] | [189.6, 192.1] | [134.4, 835.6] | the lab's glass sheet split at the bar: each pane runs to the bar's fillet (4.7 from the middle, the putty's inner edge), 2.5 thick |
| glass__lower_R | glass_house | [4.7, 357.3] | [189.6, 192.1] | [134.4, 835.6] | the lab's glass sheet split at the bar: each pane runs to the bar's fillet (4.7 from the middle, the putty's inner edge), 2.5 thick |
| glass__upper_L | glass_house | [-357.3, -4.7] | [142.0, 144.5] | [856.7, 1608.7] | the lab's glass sheet split at the bar: each pane runs to the bar's fillet (4.7 from the middle, the putty's inner edge), 2.5 thick |
| glass__upper_R | glass_house | [4.7, 357.3] | [142.0, 144.5] | [856.7, 1608.7] | the lab's glass sheet split at the bar: each pane runs to the bar's fillet (4.7 from the middle, the putty's inner edge), 2.5 thick |
| net__N1 | net_voile | [-450, 450] | [254, 255] | [60, 880] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N2 | net_voile | [-450, 450] | [254, 255] | [60, 1630] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N3 | net_voile | [-430, 430] | [254, 255] | [100, 500] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| curtain__C1_drawn | curtain | [-480, 480] | [262, 263] | [0, 1780] | drawn across; colour per house |
| curtain__C2_open_L | curtain | [-480, -310] | [262, 263] | [0, 1780] | drawn back, left |
| curtain__C2_open_R | curtain | [310, 480] | [262, 263] | [0, 1780] | drawn back, right |
| blind__B1 | blind | [-400, 400] | [240, 241] | [660, 1650] | venetian blind |
| blind__B2 | blind | [-390, 390] | [240, 241] | [700, 1660] | roller blind |
| blind__B3 | blind | [-420, 420] | [240, 241] | [100, 1640] | vertical louvre blind |
| pendant__shade | pendant_shade | [-170, 170] | [650, 990] | [1536, 1776] | a paper shade 340 across and 240 high, 0.55 behind the card, its top 0.30 below the ceiling; emissive only in a lit room; present where the room's `pendant` is true; the one real object in the room (the picture's ceiling carries its rose) |

**S11: added nodes** (the lab's 35 nodes are reused as they are for S22 and S11; the RC's parts are in section 4.3):

| node | material | x (mm) | y into the wall (mm) | z up (mm) | note |
|---|---|---|---|---|---|
| glass__lower | glass_house | [-357.3, 357.3] | [189.6, 192.1] | [134.4, 835.6] | the lab's sheet, one pane a sash |
| glass__upper | glass_house | [-357.3, 357.3] | [142.0, 144.5] | [856.7, 1608.7] | the lab's sheet, one pane a sash |
| net__N1 | net_voile | [-450, 450] | [254, 255] | [60, 880] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N2 | net_voile | [-450, 450] | [254, 255] | [60, 1630] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N3 | net_voile | [-430, 430] | [254, 255] | [100, 500] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| curtain__C1_drawn | curtain | [-480, 480] | [262, 263] | [0, 1780] | drawn across; colour per house |
| curtain__C2_open_L | curtain | [-480, -310] | [262, 263] | [0, 1780] | drawn back, left |
| curtain__C2_open_R | curtain | [310, 480] | [262, 263] | [0, 1780] | drawn back, right |
| blind__B1 | blind | [-400, 400] | [240, 241] | [660, 1650] | venetian blind |
| blind__B2 | blind | [-390, 390] | [240, 241] | [700, 1660] | roller blind |
| blind__B3 | blind | [-420, 420] | [240, 241] | [100, 1640] | vertical louvre blind |
| pendant__shade | pendant_shade | [-170, 170] | [650, 990] | [1536, 1776] | a paper shade 340 across and 240 high, 0.55 behind the card, its top 0.30 below the ceiling; emissive only in a lit room; present where the room's `pendant` is true; the one real object in the room (the picture's ceiling carries its rose) |

**RC: added nodes** (the lab's 0 nodes are reused as they are for S22 and S11; the RC's parts are in section 4.3):

| node | material | x (mm) | y into the wall (mm) | z up (mm) | note |
|---|---|---|---|---|---|
| glass__lower | glass_house | [-347.0, 347.0] | [112.5, 116.5] | [78.0, 1154.0] | 4 mm, one pane drawn for the sealed unit |
| glass__top | glass_house | [-316.0, 316.0] | [112.5, 116.5] | [1291.0, 1567.4] | 4 mm, one pane drawn for the sealed unit |
| net__N1 | net_voile | [-450, 450] | [235, 236] | [60, 880] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N2 | net_voile | [-450, 450] | [235, 236] | [60, 1630] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| net__N3 | net_voile | [-430, 430] | [235, 236] | [100, 500] | a flat card, alpha = the weave and folds (NET_COMMON); one of N1, N2, N3 or none is switched on per house |
| curtain__C1_drawn | curtain | [-480, 480] | [262, 263] | [0, 1780] | drawn across; colour per house |
| curtain__C2_open_L | curtain | [-480, -310] | [262, 263] | [0, 1780] | drawn back, left |
| curtain__C2_open_R | curtain | [310, 480] | [262, 263] | [0, 1780] | drawn back, right |
| blind__B1 | blind | [-400, 400] | [240, 241] | [660, 1650] | venetian blind |
| blind__B2 | blind | [-390, 390] | [240, 241] | [700, 1660] | roller blind |
| blind__B3 | blind | [-420, 420] | [240, 241] | [100, 1640] | vertical louvre blind |
| pendant__shade | pendant_shade | [-170, 170] | [650, 990] | [1536, 1776] | a paper shade 340 across and 240 high, 0.55 behind the card, its top 0.30 below the ceiling; emissive only in a lit room; present where the room's `pendant` is true; the one real object in the room (the picture's ceiling carries its rose) |

**The room card:** upper windows: node `room__card`, plane 270 mm, x [-1400, 1400], z [-473.6, 2076.4] (size [2.8, 2.55] m): centred on the window; floor level 473.6 below the opening's bottom, ceiling 2076.4 above it. Cottages: room_card_gf: 3.4 x 2.6, centred between the house's two windows (each window's place in it is sites[].card.window_in_card_m), its floor 373.6 mm below the opening's bottom and its ceiling 2226.4 mm above it; both windows look into the same card and the same picture.

**Materials:** paint_<paint name>: per house, colour from `paints`; roughness per paint; vertex colour R multiplies (BOX_SHADE); glass_house: the pane material (GLASS.pane): one per pane id so each pane's tilt is its own node; net_voile: alpha-textured card: the weave and folds (NET_COMMON), colour white, greyed or yellowed per house; curtain: colour per house (CURTAINS), folds as a normal and a brightness map, opacity 0.97; blind: slat texture with the gap alpha (BLINDS); pendant_shade: paper, emissive in night_lit only; room_card: plain quad; the game's M_LedgerInterior takes CardOrigin, RoomSize, CamD, Side, three textures and Night, LitOn, Brightness: the quad has no UVs that matter.

**How a piece goes into the game** (HANDOVER.md's route, and what is different here):

- terrace-front.py: SASH_KIT_ROWS to None (every row takes the period opening 850 x 1676.4: the cottages' sill goes to 0.8236 above the crown, 0.7236 above the threshold, the head kept at 2.5), and `_plain_ground` to follow `_window_kind` (it draws every cottage window as a 2/2 today)
- HOUSE_PANE_TRANSLUCENT stays False: the glass is the pane material, the net card behind it; the translucent pane stays shops' only
- held props: one glb per kind, placed by `sites[]` (HANDOVER.md steps 1 to 4); the room pictures are rebuilt on the PC by their one command and imported as textures (sRGB, no mips below 256)
- M_LedgerInterior parameters per site from `sites[].card` (CardOrigin, RoomSize, CamD, Side) and the picture ids; Night and LitOn from the lit table; Brightness day 0.12, night 0.7
- the wall kit takes the reveal's brick returns' shade (BOX_SHADE.brick_returns_of_the_reveal) and the carcass behind the card (its front face at 0.29 m or more)

**The room card's parameters per site** are in `sites[].card`: CardOrigin (cm: low-x corner, front y, floor z), RoomSize (cm), CamD (cm), Side (+1 east, -1 west), and the picture ids by the site's `room`. Example, `east_chandler_bay0_upper_w0`: CardOrigin [4010.0, 539.5, 375.0], RoomSize [280.0, 254.99999999999997, 420.0], CamD 280.0, Side 1, window in the card (m) {'x0': 0.975, 'x1': 1.825, 'z0': 0.4736, 'z1': 2.15}.

## 9. The gate, in the cloud (no Unreal)

what the cloud shows without Unreal: a house front built from the kit pieces, its neighbours, the opposite row as proxies, the street's lamps and sky, the room cards baked through the game's `trace`, the pane drawn as the game draws it (GLASS.pane.cloud_stand_in).

**Scene.** engine: Blender 5.2 Cycles, CPU, 2560 x 1440 (the dark lines are 6 mm: 1.4 pixel at 8.8 m; do not render smaller), 48 samples, OpenImageDenoise, Standard view transform, film not transparent; opposite_row_proxies: boxes at the street file's numbers: east parade eaves 6.3 above the crown, pitch 35 degrees, depth 8; west cottages eaves 3.1 above the crown, pitch 40; the hill and sky as the dome; street: road 6 m crowned 0.075, footways 2 m at crown + 0.10, kerb 0.125 up; the four lamp columns at x 8, 18, 28, 38 (stand-ins); sky: the overcast dome (Poly Haven belfast_open_field_2k, CC0, the scene file's own), sun off; the world's strength is calibrated so that a Lambertian grey card (albedo 0.18) facing the street reads linear 0.18 +- 0.01 (sRGB 118 +- 4) in the render's own pixels; night: dome x 0.15 (unreal-look.json sky_seen_gain_night), the four lamps: point lights (linear (1.0, 0.25, 0.0) = lantern_linear_rgb) at 4.78 m, power set so the paving under the near lamp reads sRGB 150 +- 20; the lit windows by the table at 20:30 (`rooms.lit_share.lit_by_hour`): lit room card (night_lit picture x 0.7 x room_glow_gain_night 0.4), lit net emissive 0.48; the rest night_dark; room_cards: for every window and every camera the card's emission picture is computed per pixel through `tools/ue/make_interior_material.py` `trace` (imported, not rewritten) from the room's picture and set as the card's emission; a lit room has its net and curtain cards emissive as NET_COMMON says; a dark one is lit by the sodium wash only; passes: Cycles passes: Material Index (pane = 1 glass_house, frame = 2 paint_*, net/curtain/blind = 3, brick/wall = 4, card = 5), Object Index per window (id), Z; the masks come from these, never by eye. **House sets:** GS_A: east_parade bays 1, 2, 3 and neighbours (bay 0 and 4 as plain blocks): the S11, RC and S22 houses; the unlet house; the wall kit's brick, sills and arches (stand-ins from the street file's materials are enough); GS_B: west_south bays 0, 1, 2 (the three cottages) with the door, the plinth and the wall, and one house of the east parade opposite as proxy.

**Views:** GS_A: H_ACROSS_0, H_ACROSS_30, H_ALONG_15_NEAR, H_ALONG_30_NEAR, H_ALONG_15_ROAD by day and by night (20:30), H_UNDER by day; GS_B: from the east footway's kerb edge (H_ACROSS_0, H_ACROSS_30), and along the cottages' own footway (H_ALONG_15_NEAR, H_ALONG_30_NEAR, H_ALONG_15_ROAD), by day and by night; 22 renders.

**What is measured** (from the Material Index and Object Index passes, never by eye):

- **P:** the median sRGB luma of a window's pane pixels (material index 1 and 3 inside the window's outline: glass and net together as the eye sees them)
- **L:** the 90th percentile of the luma of the window's joinery pixels (material index 2: the sash members, linings, beads, sill)
- **D:** the 5th percentile of the luma over the window's outline (joinery and pane pixels, no brick)
- **spread:** the pane pixels' 95th minus 5th percentile
- **angle:** the angle from the wall at which the window's centre is seen from the camera, from the scene's geometry (not from the picture)
- **window_state:** its net class (sites[].net.kind with N0 = bare) and its time (day, or night lit or dark)
- **bands_come_from:** photo_measurements.bands_by_state (Photo, +-5 degrees on the angle, outlines by eye)

**Bands** (from the photographs, section 3.2; the check numbers of section 10 quote them):

- **net_N1_N2_in_15_to_30_deg:** {"P_over_L": [0.55, 0.95], "D_over_L_max": 0.55, "spread_min": 40, "photo": "P1_a, P1_b, P1_e at 31 to 37 degrees: 0.83, 0.87, 0.85 (D/L 0.47 to 0.50); the nine net windows 0.60 to 0.97"}
- **net_N3_cafe:** {"P_over_L": [0.35, 0.75], "photo": "P4_E (a net over the lower half, 35 degrees): 0.56"}
- **bare_N0_in_15_to_30_deg:** {"P_over_L": [0.1, 0.45], "spread_min": 20, "photo": "P1_c (22 degrees) 0.32; P4_G 0.19; P3_d 0.36"}
- **bare_N0_over_60_deg_from_across:** {"P_over_L": [0.35, 0.7], "blue_over_red_min": 10, "photo": "P8_L, P8_R (near square, from below, sky over a dark room): 0.62, 0.51; the pane's colour (87, 99, 135): blue over red 48"}
- **old_fault_to_fail:** {"P_over_L": 0.85, "D_over_L": 0.85, "spread": 14, "source": "1a: pane 157 to 175 against paint 178 to 205, the lace uniform, no corner line; the checks below must fail this"}

**What the gate cannot show:** the game's glass reflections (Lumen, the cube), the exposure, the motion vectors of the card under TSR, the real glass hand-over: owed on the PC (section 10, OWED rows).

## 10. Checks (target.json `checks`; the cloud gate and the build run them)

44 checks. Kinds of number: Read, Scaled, Photo, Derived, Judgement.

| id | name | measure | expected | tolerance | applies to | kind | source |
|---|---|---|---|---|---|---|---|
| KIT-01 | the opening | bounding box of the glass-plus-frame nodes' outer lining in x and z of each kit | 850.0 wide, 1676.4 high (the frame's outer lining at the brick line) | +-0.5 mm | S22 S11 RC | Read | lab target.json opening; ruling of 8 October |
| KIT-02 | pivot | the bounding box of the whole piece in the kit frame | x centred on 0 (+-1 mm), z min 0 (+-0.5 mm), nothing in front of the brick face (y into the wall min >= 0: the lab sash 108.3, RC 72.5) | +-1 mm | S22 S11 RC | Derived | HANDOVER.md pivot rule |
| KIT-03 | glass planes | the y (into the wall) of each pane node's front face | S22/S11: upper panes 142.0, lower panes 190.0; RC: both 112.5 | +-1.0 mm | S22 S11 RC | Read | 1a section 2; the lab glb; RC Judgement from the photographs' frames |
| KIT-04 | one mesh a pane | count of nodes named glass__* | S22 4, S11 2, RC 2 | exact | S22 S11 RC | Derived | per-pane tilt needs per-pane meshes |
| KIT-05 | pane tilt | the rotation of each glass node about the vertical and horizontal axes | each within +-0.5 degrees vertical axis and +-0.3 degrees horizontal, none exactly zero, a window's panes spread at least 0.3 degrees | exact bounds | S22 S11 RC | Photo | P8: panes 86 to 105 mean luma, +-10 per cent; 1a step 3 0.5 to 1 degree |
| KIT-06 | net cards | the node `net__N1`, `N2`, `N3`: x and z extents and the y plane | N1 x +-450, z 60 to 880; N2 x +-450, z 60 to 1630; N3 x +-430, z 100 to 500; planes S22/S11 254, RC 235 behind the face | +-1 mm | S22 S11 RC | Judgement | NETS; photographs P1 to P7 |
| KIT-07 | net inside the box | the net plane minus the pane's rear face | S22/S11 lower pane: 254 - 190 = 64 mm or more; no net node crosses a joinery node | no intersection | S22 S11 RC | Derived | 1a: nets behind the sashes |
| KIT-08 | the room card | node `room__card` (upper windows): size, plane, UV range and the world's CardOrigin from sites[].card | 2.8 x 2.55 m, plane 270 +-1 mm behind the face, centred on the window (+-1 mm), floor 473.6 below the opening's bottom | +-1 mm | S22 S11 RC (upper) | Derived | trace rule; shop-windows target 3 |
| KIT-09 | vertex colour on the joinery | COLOR_0 on every joinery vertex; the red channel's values | present on all; min >= 0.25; lining faces 1.0 at the brick edge falling to 0.6 +-0.05 at the glass; track faces 0.50 +-0.08; inside corners within 8 mm: 0.30 +-0.10; putty strips 0.35 +-0.05; meeting rail underside 0.40 +-0.08 | as stated | S22 S11 RC | Judgement | 1a step 2, BOX_SHADE |
| KIT-10 | the dark lines are wide enough | every shade step or gap that the box draws as a line (putty strip, parting bead gap, weld groove, gasket) | at least 6 mm wide (the putty strip 6.4, the parting bead gap 2.0 stays a geometric gap of 2 mm with its shade painted 0.10 over 6 mm of each side) | >= 6 mm | S22 S11 RC | Derived | 1a: 1 px = 5.9 mm at 10 m |
| KIT-11 | budget | triangles and file size per kit glb | <= 6,000 triangles and <= 400,000 bytes | limit | S22 S11 RC | Judgement | push guard 1 MB |
| KIT-12 | RC parts | the RC nodes' bounds against target.kinds.RC.parts_mm | every part within | +-0.5 mm | RC | Judgement | photographs P6, P7, P11 |
| KIT-13 | paint and material names | material names on the nodes | paint_<name> per `paints`, glass_house, net_voile, curtain, blind, pendant_shade | exact | all | Derived | HANDOVER.md step 3 |
| MAT-01 | the pane material | the pane material's inputs in the build and in the cloud stand-in | specular 1.0 (F0 0.08; Cycles specular IOR level 1.0), roughness 0.03, metallic 0, transmission 0, base colour 0.03 where the net's alpha is 0 | +-0.02 (roughness 0.02 to 0.04) | all panes | Read | 1a step 1; unreal-look.json glass_roughness 0.02 |
| MAT-02 | no day glow | the pane's emission by day | 0 (the net is not emissive by day: net_day_gain 0.0) | exact | all | Read | unreal-look.json net_day_gain |
| MAT-03 | the alpha is wired | the net material's alpha input | linked to the weave texture (not a constant) | exact | net cards | Read | 1a: 'the lace's alpha is not wired' was the fault |
| MAT-04 | reflectance at a grazing angle | render a flat pane at 16 degrees from the wall against a uniform sky of luma 1.0 with the room black | the pane's luma 0.26 of the sky with F0 0.08 (Schlick at 74 degrees from the normal: Unreal's own figure for Specular 1, 1a section 2); Cycles' dielectric Fresnel at specular level 1.0 may read up to 0.31 | +-0.05 | the pane material | Derived | 1a Fresnel table: true two-face 0.38, Unreal 0.26 |
| WB-01 | net windows are darker than their frames | P/L of every net N1 or N2 window seen at 15 to 30 degrees from the wall (day, the gate's five views) | 0.55 to 0.95 and the median of the set at most 0.92 | bands | GS_A GS_B | Photo | P1_a, P1_b, P1_e (31 to 37 degrees) 0.83 to 0.87; nine net windows 0.60 to 0.97 |
| WB-02 | bare windows are much darker | P/L of every bare (N0) window seen at 15 to 30 degrees from the wall, by day | 0.10 to 0.45 | band | GS_A GS_B | Photo | P1_c 0.32, P4_G 0.19, P3_d 0.36 |
| WB-03 | bare windows from across, near square | P/L of every N0 window seen from H_ACROSS_0 by day (over 60 degrees), and the pane's blue minus red | 0.35 to 0.70 and blue over red at least 10 levels | bands | GS_A | Photo | P8_L, P8_R: 0.62, 0.51; (87, 99, 135) |
| WB-04 | the dark lines are present | D/L of every window (net or bare) seen at 15 to 30 degrees | at most 0.55 | limit | GS_A GS_B | Photo | P1 tight outlines 0.47 to 0.50; 1a D/L <= 0.6; the fault was 0.85 |
| WB-05 | the pane is not one tone | the pane spread (95th minus 5th percentile) of every net window; of every bare window | net at least 40 levels; bare at least 20 | limit | GS_A GS_B | Photo | nets 85 to 173 on the photographs; 1a: at least 20; the fault 14 |
| WB-06 | something is behind the glass by day | for every N0, N3 or N1 window seen from H_ACROSS_0 by day: the clear pane's pixels (upper sash for N1, whole pane for N0) | at least two tonal regions (the ceiling and the back wall, or the net's edge) whose medians differ by 10 levels or more, from the room picture through `trace` | 10 levels | GS_A GS_B | Derived | brief item 6 |
| WB-07 | the frame is brighter than the wall | L (linear) over the brick's median (linear) beside the window, by day | 3.0 to 9.0 | band | GS_A GS_B | Photo | P1 4.3 and P8 3.7 on photographs (film contrast); the game's albedos give 0.82/0.13 = 6.3; the concept sheet's 7 is outside the photographs |
| WB-08 | the old fault fails | run WB-01 to WB-05 on a render with the old pane (a lit lace card, F0 0.04, no lines) in the same views | WB-04 and WB-05 and WB-02 must FAIL (D/L 0.85, spread 14, bare windows lighter than 0.45) | must fail | GS_A | Derived | 1a section 3; a check that cannot fail checks nothing |
| WB-09 | the window under 10 degrees | a window seen under 10 degrees from the wall (the far end of H_ALONG_15_ROAD) | reads as a white lining edge at least 1 px wide beside a dark void; the reveal's brick return 0.8 of the wall's luma or less; no pane luma above the lining's | as stated | GS_A | Photo | P13: a white slit beside a dark void; 1a |
| NIGHT-01 | lit and dark windows at night | count of windows with pane median luma >= 100 (lit) and <= 30 (dark) at 20:30 over the 20 street windows (GS_A and GS_B together, rendered from the one camera that sees each squarely) | 7 lit (+-1), the rest dark; none between 30 and 100 | +-1 | all 20 | Judgement | rooms.lit_share |
| NIGHT-02 | lit against dark | the median pane luma of the lit windows over that of the dark windows, night | at least 4 (linear at least 10) | limit | GS_A GS_B | Judgement | NIGHT-2026-10-08.md: real lit windows are 10 to 100 times the lit paving; the game's gain gives 0.4 |
| NIGHT-03 | the lit net glows its own colour | a lit net or curtain's mean colour (linear) ratio r:g:b | r > g > b, g/r 0.55 to 0.80, b/r 0.20 to 0.45 (tungsten 2700 K and the fabric) | band | lit windows | Read | interior_lit (1.0, 0.714, 0.344) |
| NIGHT-04 | a dark window shows only the sodium wash | the dark rooms' mean colour (linear) | b/r under 0.05 (the wash is (1.0, 0.25, 0.0)); luma 8 to 30 sRGB | limit | dark windows | Read | unreal-look.json lantern_linear_rgb |
| NIGHT-05 | the lit order is nested | the set lit at 23:00 is a subset of the set lit at 20:30 except the always-lit pair's end; empty rooms never lit | true | exact | table | Derived | lit_share.rule |
| PIC-01 | size and states | each room's three PNGs | 1536 x 1399 (UP) or 3072 x 2349 (GF), 8-bit sRGB, named <room>_<state>.png, with <room>.json | exact | 13 rooms x 3 states = 39 | Derived | shop-windows target 3 |
| PIC-02 | mean luma | the mean sRGB luma of each picture | day 105, night_lit 70, night_dark 15 (landings and empty rooms at night_lit: bare bulb: 40) | +-15 per cent | all | Judgement | picture_standards |
| PIC-03 | no black void | the share of pixels under luma 8 and the largest dark region | day and night_lit: under 25 per cent and the largest region under 15 per cent of the picture; the composite (x brightness) day >= 14, night_lit >= 40 | limits | all but night_dark | Derived | the 3 October failure |
| PIC-04 | the back wall lands where the rule puts it | the back wall's corners in the picture by edge detection | UP (1536 wide): (461, 420) to (1075, 979); GF (3072 wide): (849, 649) to (2223, 1700) | +-8 px | all | Derived | trace/project rule, camd = W |
| PIC-05 | stand-off | every object's and every form's stand-off from its surface (rooms.rooms[].objects, rooms.forms) | back wall <= 0.80 (true <= 0.40), side walls <= 0.06 (true <= 0.03), ceiling <= 0.04 (true <= 0.02), floor <= 0.037 (true <= 0.018) | limit | all | Derived | hw_common budgets |
| PIC-06 | parallax | from H_ACROSS_0 and the same point moved 2.0 m along the street, a marker at the picture's centre | moves as `trace` predicts | +-20 px of 2048 | UP and GF samples | Derived | shop-windows PRJ-02 (proves the gate, not the game) |
| PIC-07 | no marks | every picture searched by eye at full size, and the final base colour of every model used | no maker's name, brand, logo, barcode, person or child; every `marks` entry blanked or the model not used | none | all | Derived | TARGET-REVIEW of unit 7, fault 2 |
| PIC-08 | the room is lit as the table says | the picture used for each window in each state | lit windows night_lit, the others night_dark, day for all by day | exact | 20 sites | Derived | lit_share |
| SITE-01 | the twenty openings | the derived list of terrace-front.py's windows re-derived live | 20 sites, centres and kinds as sites[]; the cottage windows' kind by house | +-1 mm | 20 sites | Read | terrace-front.py plan_street, _window_kind |
| SITE-02 | no visible repeat | along each row, any two windows within three places | never the same (room, net kind, curtain) triple, never the same paint on neighbouring houses unless white | exact | sites | Judgement | variants |
| SITE-03 | the mix | the street's twenty windows by net class | N0 4 to 5, N1 8 to 10, N2 3 to 5, N3 1; curtains (open beside a net, or drawn) and blinds 6 to 10 of the 20 | counts | 20 sites | Photo | tally |
| SITE-04 | paint | houses by paint | white (any kind) 5 to 7 of 10, cream 2, olive 1, blue 1, bronze 1 | counts | 10 houses | Photo | paint_tally |
| CONTENT-01 | the content rule | every string of target.json, every picture, every preview | no alcohol, gambling, child; no real firm's name; tobacco allowed | none | all | Derived | canon.md; CLAUDE.md |

**Owed on the PC** (the cloud cannot show them):

- **OWED-01** the pane in the game: Specular 1.0 at roughness 0.03 with the net's alpha wired, the opaque Default Lit material, seen at 15 to 30 degrees with Lumen's own reflections. Check: WB-01 to WB-05 on the packaged game's frames at the Hook camera and the reverse view (1a's step 1 test).
- **OWED-02** the joinery's shade as vertex colour (BOX_SHADE) read by M_LedgerSurface (not the AO pin). Check: 1a section 5: D/L <= 0.6, T/L 0.65 to 0.85, P/L 0.6 to 0.9 and a pane spread of 20 levels in the hook frame's near-left terrace and Mickey's row.
- **OWED-03** a marker at the room picture's centre moves as `trace` predicts from two eyes 2.0 m apart, in the packaged game. Check: PIC-06 on the PC: 20 px of 2048.
- **OWED-04** the room pictures rebuilt on the PC (`python make_house_rooms.py`: not written here), the masters on F:/LedgerTools/house-rooms, imported as sRGB textures. Check: PIC-01 to PIC-05, PIC-07 at full size.
- **OWED-05** Jafar's page: the house windows as a sample (the look): one page with the 15 and 30 degree frames, day and night, and the old frame beside. Check: nothing is multiplied before his yes (CLAUDE.md).

## 11. Photographs win: each disagreement

| id | what | the file, book or research said | the photographs say | chosen |
|---|---|---|---|---|
| D1 | the replacement frame's colour | dark anodised bronze (frame_bronze) for every replacement (terrace-front.py _sash) | white in all four replacement windows reached (P6, P7, P11, and P6's ground bay): none brown or bronze | white satin (white_upvc) by default; bronze kept for the one metal-refit house (the ship chandler's, whose front is aluminium: Judgement, D06 'Hook shops receive metal frames'); not Jafar's ruling: the asset plan's |
| D2 | the nets | one square mesh picture over the whole pane (net_curtain_a, _b: 7 to 10 mm squares, mean alpha 0.53), alternated by house | about half the windows have a voile on the lower sash only (47 of 60), the upper sash clear; full nets 22 per cent; bare 18 per cent; curtains 10; blinds 2 | six net and drape kinds, per house, with the mix of the photographs; the two held pictures are not used |
| D3 | the pane | the net card is the pane: lit lace over a pale card, F0 0.04 (the 8 October note) | every bare window reads dark (0.19 to 0.36 of its frame) and the room shows; a net reads 0.6 to 0.97 of the frame with lines round it | glass over a dark room, the net a separate card (1a) |
| D4 | the cottages' windows | all six drawn as 2/2 box sashes 1.5 high (the per-house kind is not read on the ground floor) | the ground windows of P1, P3, P4, P12 are the same sashes as the floor above; P6's ground sill stands 0.72 to 0.92 above the step (Photo: door leaf 195 px = 1.98 m) | the house's own kind and the period opening 1676.4 with the head kept (sill 0.7236 above the threshold) |
| D5 | six over six | none | P10 (Copenhagen Street, Georgian, 1983) and P13 (Prince Street, Hull, 1982) show it, on Georgian terraces; no house of Quay Street is Georgian | not built; listed as the sash kind a Georgian house would need |
| D6 | the glazing bar | 22.2 mm (the lab's amended value) | P8 (Oxford, 1987): the bar is 2.3 px wide on a window 71.9 px wide = 27 mm (+-6) | 22.2 kept: inside the error |
| D7 | the frame's visible width | 76.2 (3 in, the ruling) | P8, the BACK of a terrace (plain, no outer lining): the visible white jamb is 3.1 to 4.0 px of 71.9 = 37 to 47 mm; the lab's P6 (a front, Tottenham) 79 mm | 76.2 kept for the fronts (the ruling); a rear window narrower, not on this street |
| D8 | the lit share | one in three of the upstairs nets lit at night, two cottage windows always | none reached (no night photograph of a terrace before 1996) | kept near the street's one in three (0.35 at 20:30); a Judgement |
| D9 | frame to wall ratio | WINDOWS-OTHER-DIRECTION: frames about 7 times the wall | P1 4.3, P8 3.7 (linear, display values of film scans) | the check's band is 3 to 9; the game's own albedos give 6.3 |
| D10 | the meeting rail | 38.1 mm (the lab kept it) | P8: the rail with its shade reads 5 px of 134 = 62 mm; the lab's note (P6 Tottenham 24 to 28 mm face) stands for the face; the rest is the underside's shade | 38.1 kept; the shade is BOX_SHADE.meeting_rail_underside |
| D11 | the top light of the replacement | the transom at 0.72 of the opening (REPLACEMENT_TRANSOM) | P6 0.66, P7 0.72, P11 0.75 | 0.72 kept (inside the three) |
| D12 | the white-board look at 15 to 30 degrees | the panes should be darker than the frame by about 0.6 to 0.9 | net windows read 0.83 to 0.87 of the frame at 31 to 37 degrees: nets ARE nearly white; bare windows 0.19 to 0.36 | the bands above are by state; the fault is the missing lines and the uniform tone, not a bright net |

## 12. What the target could not settle

- No 1975 to 1995 night photograph of a terraced street was reached: the lit share by hour is a Judgement (anchored on the street's own one in three).
- No period photograph of a brown or bronze anodised aluminium window on a house was reached: the bronze replacement is kept for one house only, marked Judgement.
- The photograph measurements are on 640 to 1024 px scans: a window is 15 to 100 px wide, so D (the darkest line) is a floor, and the angle from the wall is +-5 degrees from the window's proportion; the bands are wide for that reason.
- A sealed double-glazed unit's four reflecting faces (about 0.14 at normal incidence) cannot be reached by Unreal's Specular 1.0 (F0 0.08): the replacement's pane under-reflects; the cure (an emissive sky term) is a PC tuning, listed in owed_on_pc.
- How the game's Lumen reflections and the street cube show on the pane (the box projection, the Fresnel hand-over) is not shown by the cloud: the cloud's pane reflects the proxies and the dome through Cycles.
- The rooms' contents were chosen from 44 Poly Haven models and 17 textures; none shows a period British room: no 1975 to 1995 photograph of a domestic interior was reached, so the rooms rest on the photographs' windows (nets, drapes, a pot plant, a dark room) and on the budgets, not on a room photograph.
- Whether Jafar wants the kit for the whole street at the period height (the cottages' sills lowered by 0.176 m) is his: the ruling of 8 October is followed here for every row; the PC session widens SASH_KIT_ROWS.
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
| sheet | measured-windows-sheet.jpg | the 18 windows measured, outline red and pane green | none |

