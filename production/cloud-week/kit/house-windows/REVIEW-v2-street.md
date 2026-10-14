PASS

# House windows (unit 8), the STREET view: fresh review, try 2 (cloud week 42, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the kit. I judged the street view only: the Hook view, cam_A and the reverse view, by day and at night, and the gate's street-distance frames (H_ACROSS_0 and 30 from the far kerb, the cottages' along-15, along-30 and road views). I did not read the close view's reviews. Jafar's ruling of 9 October applies: a piece failing only on narrow points passes, with the points listed.

**Verdict: PASS, no fault, nine narrow points.** Try 1's two faults are fixed where they show from the street. The glass no longer mirrors: its reflection now adds light, as glass does, and the nets and rooms show behind it. At night the lit windows are told from the dark ones in the Hook and the reverse view. What is left is the lit cottage room behind its clear upper sash, which is too dim against its own net. Each of the seven failing rows has an exact ruling below. Two of the builder's stated causes are wrong (WB-07, and the "world seen through the cottage card"). Neither hides a fault in the windows.

**Read:** CLAUDE.md; RULINGS.md (3 Oct white frames, 1 and 2 Oct, 8 Oct photographs win, 1 Oct night); TARGET.md sections 3.3, 5, 6, 7.1, 7.3, 9, 10 and 14; target.json's rows; NOTES.md, the try 2 section last, after my try 1 items; `checks/check_windows_v2.json` (all 73 rows); the code of `check_windows.py` (WB-07's brick ring, the night rows), `hw_gate.py` (the pane, the cloth colours, the card bake) and `hw_measure.py`; my own try 1 review.

**Looked at:** the six street previews of 14 October beside those of 13 October; the gate frames at 2560 x 1440, whole and in crops at 2x to 6x: Hook, reverse, cam_A day and night; H_ACROSS_0 parade and cottages, day and night; the along-30, along-15 and road views; the reflection-off night frames. I also looked at the Hook sheet, the 13 lit room pictures as a sheet, and the baked cards.

**Measured** (luma Rec.709 on sRGB, 0 to 255. P is the pane median and L the joinery's 90th percentile, as the gate measures them. "Clear" and "cloth" are told apart by the mask with the glass clear. Boxes are in the 2560 frame, then "1600" for the preview):
- every window in the six street frames and in all 14 night frames, from the frames and their masks;
- two test renders of my own (1280 x 720, 16 samples, niced, the builder's own scene code, my own folder). They show the bare window east_parade_bay3_upper_w1 in the along-30 view with the glass's reflection off and on;
- the trace rule at six card points against two newly baked lit cards;
- the four glbs' JSON: normal maps, UVs, the glass, the part planes after the 0.5 mm moves;
- the brick ring of WB-07, the clip share of the lit pictures under a higher gain, and burnt and black joinery pixels.

## Try 1's items, one by one

| try 1 item | now | evidence |
|---|---|---|
| **F1, the pane a mirror by day** | **FIXED** | Hook day, east_parade_bay0_upper_w0, box (1898, 147, 1996, 464), 1600 (1186, 92, 1248, 290): the full-height net shows with soft folds and a lace band, P/L 0.72 (was 0.52). Its neighbour bay0_w1, (1624, 305, 1677, 543), shows its voile and the cream curtain at the upper sash's left, P/L 0.64. cam_A day, west_south_bay0: gf_w1 (281, 546, 347, 726) 0.46 (was 0.07) and gf_w0 (417, 558, 465, 713) 0.49 (was 0.11), each a net and a dim room in the upper sash. **The reflection now adds light:** my render of the bare window at 19 degrees reads P/L 0.423 with the reflection off and 0.509 with it on. In try 1 the reflection took light away (104 against 55). GLS-06 passes on the kit's own slab (0.705 at 15 degrees, need 0.678). NEG-01 fails the old pane, as it must. |
| F1 acceptance: WB-01 to WB-05 and WB-09 re-measured | **FIXED** | All re-measured on the corrected glass (rulings below). |
| **F2, night: lit not told from dark** | **FIXED in the street's views, PARTLY in its causes** | Hook night: the lit lounges read 109 and 81 over the six dark windows' median 36, 2.65 times (NIGHT-08; my acceptance 2.5). Reverse night: the lit pair of west_south_bay2, (1029, 779, 1033, 866) and (1050, 776, 1054, 869), 1600 (643, 487, 646, 541) and (656, 485, 659, 543), reads 56 and 83 above every dark cottage window (at most 46, NIGHT-09). In the target's night views (windows seen at 45 degrees or more) every lit reading (79 to 144) is above every dark one (29 to 65). |
| F2 cause 1, the back face mirroring the night sky | **FIXED** | H_ACROSS_0 night, the dark empty flat's clear sash (east_parade_bay3_upper_w0): 28 (was 75). Dark windows' clear glass 23 to 29 in every view. |
| F2 cause 2, the lit room a quarter of its net | **PARTLY** | Fixed in the parade's lounges: clear over cloth (linear means) 0.66 at H_ACROSS_0, 0.53 and 0.68 in the Hook (was 0.26 to 0.31). **Not fixed in the lit cottage:** west_south_bay2_gf_w0 reads 0.19 at H_ACROSS_0 (narrow point 1). |
| F2 cause 3, the dark band no net window can meet | **FIXED** | NIGHT-01 reworded as asked. The dark nets read 0.56 to 0.66 of their frames' L (limit 0.7) and the clear glass 23 to 29 (8 to 35). |
| N1, WB-03 band | **FIXED** | Passes: P/L 0.57, blue minus red +2. |
| N2, WB-07 floor | **PARTLY** | Applied, but the row still fails for a reason the builder misread (narrow point 4). |
| N3, burnt cottage frames, GLS-05 | **FIXED** | The joinery's burnt share (R 250 or more, B under 140) is at most 0.04 per cent of any window in 14 night frames (was 11.2 per cent on west_south_bay2_gf_w1). The frames by the lamp read orange (R 200 or more on 33 to 43 per cent of that window's joinery) but are not clipped: the lamp's own colour. |
| N4, the shops' night pane | not for this verdict | Shop folder; not seen in my pictures. |

### The builder's claims "a review was wrong", judged

- **"NIGHT-07's figures are means, not medians": right.** For the lit lounge at H_ACROSS_0 I measure clear over cloth 0.66 by the mean and 0.27 by the median, with the median glass at 0.054 under a bright transom and ceiling. My try 1 figures fit the mean. The target's row already says MEAN.
- **"NIGHT-02's 2.6 to 2.8 holds for the parade, not the whole set": right.** I measure the Hook at 2.65 and H_ACROSS_0's parade at 2.55, but the parade's two across views together at 2.49 and the whole set at 2.36. Ruled below.
- **"WB-02 is the day room plus the sky": right.** My own render reads 0.423 with the reflection off and 0.509 with it on.
- **"MAT-04 alone cannot see the mirror": right.** The energy reading (GLS-06 and MAT-04's second reading) is the test that sees it.

## Faults

None.

## Narrow points, most important first, each with its exact fix

### 1. The lit cottage room behind its clear upper sash is a fifth of its own net (NIGHT-07). Move the cottage rooms' brightness, not the gain or the row

- **Where:** H_ACROSS_0 night of the cottages (`frame_h-across0-gf2w1_night`), west_south_bay2_gf_w0, box (762, 525, 956, 914), 1600 (476, 328, 598, 571).
  - The lit net glows 136 (linear 0.266). The room behind the clear upper sash reads 62 (linear 0.050): 0.19 of the net. That is about the level of a dark window's lamp-lit net (58).
  - The other views read 0.16 to 0.44.
  - From the street it still reads as lit (the warm net glows), but its upper half looks like a dim room behind a bright net.
- **Why it is the room, measured:**
  - My trace check of that card puts the centre of the view on the back wall, which reads (64, 49, 25) in the lit picture.
  - The same pendant lights the net and the back wall from about the same distance (2.1 m each). A wall (albedo about 0.4) and a voile's diffuse transmission give luminances within about 1.5 times of each other. So the clear glass should read about 0.5 to 1.0 of the net, as the band says.
  - The parade's lounges pass only because from the street they show the ceiling round the rose. Their walls are as dim (median 0.27).
- **Why not the other two knobs:**
  - **The lit gain of 2 to 2.5 for all rooms:** applied after the roll-off, it would clip 3.4 to 6.9 per cent of every lit picture's pixels (a channel over 1.0). That brings back the clipped and yellowed ceiling of the close review. It would also push the parade's lit windows to 1.08 to 1.30 of their nets, over the band.
  - **The cottage rows:** the band is physical, as above.
- **WHOSE:** the target (7.1, the picture standard "night_lit mean luma 70" applied to the cottage rooms, which are seen at eye level), then the builder.
- **EXACT FIX:**
  - The three cottage rooms' night_lit pictures (gf_front_1, 2 and 3) are scaled x 3.0 in linear on the float render, BEFORE the roll-off (knee 0.60 toward 0.85, unchanged).
  - Their standard becomes mean luma 115 +-15 per cent. The upper rooms stay at 70.
  - The card gain stays 1.0.
  - My estimate on the present pictures: the means become 113 to 116; no pixel reaches 250 (PIC-13 holds); no clear-glass pixel of that window reaches the knee; NIGHT-07 for west_south_bay2_gf_w0 reaches about 0.57 (0.5 or more once the room seen through the net lifts the cloth a little).
  - Re-render the three pictures, re-bake the cottage night cards, re-render the cottage night frames and re-run the check.
  - **Acceptance:** NIGHT-07 is 0.5 to 1.0 at H_ACROSS_0 for every lit window.

### 2. NIGHT-01's LIT line is mis-set: it fails half of any set that sits at NIGHT-02's limit (target)

- **What:** LIT is "the pane median at least 2.5 times the dark windows' median". That is the same number as NIGHT-02's ratio of the two medians, so when the medians stand 2.5 apart, about half the lit windows fall under the line by construction. Today 7 of 9 lit readings fail it, including the parade's lounges (120 and 122 against the 125 line).
- **The data:** the lowest lit reading (79, the cottage net under a clear sash) is above the highest dark one (65, a cream roller blind of a dark landing). No window is "neither".
- **EXACT FIX (NIGHT-01):** a window is LIT when its pane median is at least 1.5 times the dark windows' median (1.58 is the geometric midpoint of 1 and NIGHT-02's 2.5, rounded down) AND above every dark window's pane median, with r > g > b. DARK stays as it is. Measured today: 9 of 9 lit (line 75; lowest 79), 8 of 8 dark, none neither.

### 3. NIGHT-02 reads 2.36 (linear 5.6) against 2.5 (6): a stand-in's limit; carry it to the PC (kit and target)

- **What:**
  - The Hook reads 2.65 and H_ACROSS_0's parade 2.55, but the parade's two across views together read 2.49 and the whole set 2.36.
  - The dark side is set by cloth that the gate's light lights: the dark nets read 0.56 to 0.66 of their own frames and the blinds 0.73, in every view alike. The cottages' two dark net readings (49 and 51) stand 1 to 2 m from the gate's cottage lamps.
  - So the dark level follows the stand-in lamps' power. The lit glow (net 0.48, card x 1.0) does not.
  - The research (NIGHT-2026-10-08) puts real lit windows at 10 to 100 times the lit paving. The cloud's Standard view, with the paving at 150, cannot draw that. It is the game's exposure (OWED-07).
  - Narrow point 1's fix does not move this median (the lit cottage readings rise to about the median, 118).
- **EXACT FIX:**
  - In the cloud, NIGHT-02 is reported, not failed, with the parade's figure and the whole set's beside.
  - On the PC it stands at linear 6 or more (2.5 in sRGB), measured in the packaged game under the game's lamps and exposure. Add it to OWED-07's list.

### 4. WB-07: the check's "brick beside the window" takes in the stone sill and head; and my try 1 floor for flaking paint was rounded wrongly (the builder's check, then the target)

- **The builder's cause is wrong.**
  - NOTES says the 90th percentile of so few joinery pixels takes in the anti-aliased edge. Eroding the joinery by one pixel moves L by at most 2 levels (east_parade_bay3_upper_w1 in `h-along15-gf2w1_day`: 163 to 164).
  - The cause is the ring. `check_windows.py` takes mask material 4 with G 0, and the stone sill and head are material 4 with G 0: at (1280, 896 to 920) in `h-across0-bay3w1_day` the "brick" reads (186, 184, 175).
  - In a small far window the stone and the brick-and-mortar blend lift the ring's median from 97 to 101 to 107 to 112.
- **Measured:** with the ring cut to the window's own rows (one window width each side, sill and head left out), the low readings become 2.43 (east_parade_bay3_upper_w1, road view of the cottages, 1,030 joinery px), 2.83 (the same window, along-15) and 2.49 (east_parade_bay5_upper_w0, 492 px).
- **And the floor:** white_flaking's linear albedo is 0.60, so 3.0 x 0.60 / 0.82 = 2.2, not the 2.5 I wrote (that rounding was for grimy, 0.66: 2.41).
- **EXACT FIX:**
  1. In `check_windows.py`, the brick ring takes only the rows y0 to y1 of the window's outline (no sill, no head).
  2. WB-07's floor is 3.0 for white_fresh and white_upvc, 2.4 for white_grimy and 2.2 for white_flaking (each 3.0 x the paint's linear albedo / 0.82); the ceiling stays 9.0.
  3. With both changes every reading passes: the lowest are 2.43 against 2.2 (flaking) and 2.49 against 2.4 (grimy).

### 5. WB-04b fails on a window cut by the picture's top edge (the builder's check)

- **Where:** `h-along15road-bay3w1_day`, east_parade_bay2_upper_w1, box (1830, 0, 2038, 324): the outline starts at y 0. The near reveal also hides its right side, so one pane edge was profiled, reading 0.62.
- **Why:** the builder's decision 3 leaves out a window cut by the picture's edge for WB-06 and WB-07, but not for WB-04b. The night rows also take in two cut windows (east_parade_bay3_upper_w0 at x 0 and bay1_upper_w0 at x 2559 in `h-across0-bay2w0_night`). Without them the dark median is unchanged (50).
- **EXACT FIX:** one rule for every per-window row (WB-01 to WB-07, NIGHT-01 to NIGHT-02, NIGHT-07): a window whose outline touches the picture's edge (x 2 or less, or 2557 or more; y 2 or less, or 1437 or more) is not measured. WB-04b then passes 12 of 12 (0.19 to 0.34).

### 6. WB-02's band does not allow for the reflection a bare upper window carries at 15 to 30 degrees from the footway (target)

- **Measured:** the bare window reads 0.48 (`h-along30-bay3w1_day`, 19 degrees). My render with the reflection off reads 0.423, inside the old band, so the room is right. The reflection adds 0.06 to 0.09. Target 5.1's own two-face table asks 0.21 to 0.31 of what lies opposite at 18 to 24 degrees.
- **Why the band is wrong:** its three photographs are not at this geometry. P1_c is at 22 degrees with a dark-brown frame, and its L includes the white stone (3.2's own note). P4_G is a ground window at 46 degrees, P3_d square on.
- **EXACT FIX (WB-02):**
  - An upper window seen from its own footway at 15 to 30 degrees: P/L 0.10 to 0.55. Other cases keep 0.10 to 0.45.
  - Readings with under 5,000 glass pixels (today 0.53 and 0.58, from 1,539 and 625 px) are reported, not failed.
  - 0.55 still fails the old white-board pane (WB-08, 0.84).

### 7. WB-01: the floor sits on one photograph with no margin for a lower-sash net (target)

- **What:** east_parade_bay1_upper_w1 (S11, a voile on the lower sash only, the clear upper sash half the pane) reads 0.545 against 0.55 (`h-along30-bay1w1_day`, 28,559 glass px). The band's floor is P4_E's 0.555, the only photographed net on a lower half. The other N1 photograph, P1_e, reads 0.897. The second failing reading is a far window, east_parade_bay4_upper_w1, 434 glass px (0.458).
- **EXACT FIX (WB-01):**
  - The floor for a lower-sash net (N1) window is 0.50 (0.9 x P4_E's 0.555, a margin like WB-07's floor at 0.8 of its lowest photograph). The floor for a full-height net (N2) stays 0.55.
  - Readings with under 5,000 glass pixels are reported, not failed.
  - Today WB-01 then passes.

### 8. The lit green curtain reads as two flat lime bars, and the target says no green curtain is lit at 20:30 (target text, then the builder)

- **Where:** H_ACROSS_0 night, east_parade_bay2_upper_w0, the two strips beside the lower light above the net, (1203 to 1211, 668 to 725) and (1347 to 1354, 668 to 725), 1600 (752 to 757, 418 to 453) and (842 to 846, 418 to 453). They read (115, 131, 73) with no folds: the side cloth's luma spans only 113 to 142 (5th to 95th percentile).
- **Why:** target 6's C2 asks "folds dark" and a brightness modulation of 0.25. A green curtain lit from behind may glow yellow-green. But NIGHT-03's text says none is lit at 20:30, and 7.3's order lights this window.
- **EXACT FIX:**
  1. **Target, NIGHT-03:** "a green curtain's g > r is its own colour (east_parade_bay2_upper_w0 is lit at 20:30 with one); its blocks are read against r and g of the curtain's own colour x the warm light, not against g/r 0.85".
  2. **Builder, `hw_gate.py`:** a lit curtain's emission is multiplied by the curtain's own fold brightness map (the +-25 per cent its base colour carries by day), so the folds read dark at night as the target asks.

### 9. The "world's dusk landscape" seen through the near cottage window is the framed print on the back wall, not a slot past the card (the builder's notes)

- **Where:** `h-along30-gf2w1_night`, west_south_bay2_gf_w0, the lower left of the upper-left pane, about (0 to 100, 408 to 666), 1600 (0 to 62, 255 to 416).
- **Measured:** the mask with the glass clear shows the room card (5) on every one of those pixels, and no glass pixel of that window has background behind it. The trees stay with the reflection off. The card baked for that view shows the field-and-trees print (a crop of belfast_open_field) hanging under the picture rail, in the same place. **There is no see-through slot.**
- **EXACT FIX:** correct NOTES ("Known shortfalls" and decision 19) and the reason NIGHT-03 gives for skipping those 14 blocks: "a print's own colour (a green field), as the green curtain". Nothing in the build changes.

## What is right

- **Frames and joinery.** Every frame is white (the 3 October ruling): white_fresh, grimy, flaking and the satin upvc are distinct but all white.
  - The 2/2 and 1/1 sashes read as Victorian box sashes at street distance: meeting rail, glazing bar, horns, a dark line round each pane, stone sills.
  - No black strip at any sill.
  - No joinery pixel under luma 10 in the Hook, reverse, cam_A or across views (5 of 64,631 in one along view).
  - The 0.5 mm moves are in the glbs (head outer lining at -113.8 against the side linings' -114.3; the head beads likewise). No gap or seam shows at any distance.
- **Glass with a room behind, by day.** The Hook's near windows show their nets as pale veils with soft folds and a lace band, as the Hook sheet's upper windows do. Far along the wall the panes carry the sky.
  - cam_A's cottages show a net and a dim room through the upper sash.
  - From across, the bare window shows a dim room under a little sky.
  - Parallax: I traced six card points (the Hook's lit lounge and the lit cottage from across). The baked cards match the room pictures at the traced places within 5 levels (mip filtering).
- **Night.** The lit windows are warm (r > g > b, no clip: no glass pixel at 250 or more in four night frames; the cards' maximum is 237).
  - The dark windows are honestly dark: clear glass 23 to 29, and the night_dark rooms' sodium wash below the wall's level (the landing behind the blind in the Hook, 31 to 34 against brick 41).
  - No orange bar in any pane (GLS-04 0.0000 per cent), no lit stand-in lamp, no burnt frame, no hot corner.
- **The soffit** under both eaves reads pale grey, not black, in the frames and in the upper panes.
- **Rooms.** The 13 lit pictures were looked at as a sheet: same furniture as try 1, nothing new; the content rule holds (no drink, no betting, no toy, no lettering); nothing after 1992; no child-size piece.
- **Exports.**
  - Every normal map is a real RGB normal map (blue 0.98 to 0.99). Every textured primitive has TEXCOORD_0.
  - Net 254, curtain 262 and card 270 mm (RC 235), each its own plane.
  - No see-through slot in any street mask.
  - The glbs' glass_house stays opaque (base 0.03, specular), as before: OWED-01.

## Rows: what each failing row is, and which rows I trust

| row | ruling | point |
|---|---|---|
| WB-01 | a mis-set row: N1 floor 0.50; under 5,000 glass px reported | 7 |
| WB-02 | a mis-set row: 0.10 to 0.55 for an upper window from its footway at 15 to 30 degrees; under 5,000 px reported | 6 |
| WB-04b | the builder's check: a window cut by the picture's edge | 5 |
| WB-07 | the builder's check (the stone in the brick ring) and a mis-set floor (flaking 2.2, grimy 2.4) | 4 |
| NIGHT-01 | a mis-set row: LIT at 1.5 times the dark median and above every dark window | 2 |
| NIGHT-02 | a stand-in's limit: reported in the cloud, linear 6 on the PC (OWED-07) | 3 |
| NIGHT-07 | a fault in the target's cottage picture standard: the cottage rooms x 3.0 before the roll-off, mean luma 115 | 1 |

- **Trusted:**
  - **The kit and glass rows:** KIT-01 to KIT-19 (I re-read the normal maps, UVs, planes and the moves); MAT-01 to MAT-04, GLS-06, NEG-01 to NEG-03.
  - **The day rows:** WB-03 and WB-05, WB-06, WB-08 and WB-09; ACC-01 and ACC-02 (I measure the same figures).
  - **The night rows:** NIGHT-03 (with point 8's wording), NIGHT-04 to NIGHT-06, NIGHT-08 and NIGHT-09 (the same figures).
  - **The rest:** GLS-04, JNR-01, FRM-01, PIC-01 to PIC-13, SITE-01 to SITE-04, CONTENT-01.
- **Stand-ins only, whatever they read:** WB-03 and WB-07 (the dome and the stand-in brick); GLS-05 (the stand-in lamps); NIGHT-02 and every absolute night level (the gate's lamps, sky and Standard view).

## Seen in my pictures, not for this verdict

The gate's stand-in lamps still throw sharp orange cones on the cottage wall above the window heads. Reverse night, 1600 about (635 to 680, 455 to 500) and (735 to 790, 450 to 500); hot, not clipped. The cottage lamps at x 0.7 are now dimmer than the parade's. Both are the street's shared lamp calibration, which is another builder's.

## What I cannot judge from the files

- **The game's pane.** The glbs' glass_house is opaque, and the nets and room card stand behind it as separate cards. In Unreal they show only if the PC builds the pane as target 5.1 says (OWED-01). This is the largest risk left before the first Unreal frame.
- **Lumen's reflections, the street cube and the night exposure** (OWED-06, OWED-07), and so the true lit-to-dark ratio.
- **The rooms at the target's 128 samples** (cottages 16, others 24 here).
- **The wall kit.** The reveals' brick returns read as alternating grey and red blocks in the reverse view, day and night (1600 about 729 to 735, 476 to 553). The Hook sheet's arched heads are not this unit's.
- **The street itself.** It is stand-in boxes, so only the windows were set beside the Hook sheet.
