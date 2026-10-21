FAIL

# House windows target: fresh review (cloud week 42, unit 8, 13 October 2026)

Reviewer: a fresh target reviewer. I did not write this target and will not build it. I read REVIEW-BRIEF.md, the writer's BRIEF.md, TARGET.md in full, and target.json (kinds, sites, paints, box_shade, nets, rooms, inventory, gate, checks). I also read the scripts I used: hw_common, hw_measure and hw_photos. Beyond the target I read unit 7's TARGET-REVIEW.md, research note 1a, RULINGS.md, `trace` in make_interior_material.py, unreal-look.json, the window and arch code of terrace-front.py, and the cameras in vignette-scene.json.

**Verdict: three faults, twelve narrow points.**

- **Fault 1.** Half the houses get coloured frames (brown, olive, blue, cream, bronze). That goes against Jafar's standing ruling of 3 October: "windows with white frames". Nobody asked him, and check SITE-04 now enforces the colours.
- **Fault 2.** The white-board checks rest on photograph numbers that measured the white stone and the brick, not the frame. Measured the way the gate measures, the same photographs would fail WB-04. Separately, three of the four "bare" windows carry a blind or a drawn curtain, so WB-02 and WB-03 fail them by construction.
- **Fault 3.** A placed model, `television_02`, carries a maker's name on its front ("PARAGON Viewing System"). Its marks entry says "no text on the front". This is unit 7's Dixons fault again, on a smaller scale.

The method holds up: glass over a dark room, the shaded box, nets as cards, and rooms through `trace`. The unit 7 lessons on covering every opening, aligning the lights and using the night wash were applied and hold. The previews are clean.

## How this was checked

- **Scripts.**
  - `self_check.py` offline gave 342 pass, 0 fail, 14 of 14 controls caught. With `--live --previews` it gave 364 pass, 0 fail.
  - `target_drawing.py` drew 3 kinds and 13 rooms into scratch. I looked at the S22 and RC elevations and at the row of twenty.
  - Neither script changed target.json or target_drawing.json. The working tree is clean.
- **Previews.** I looked at all 16 images, zooming on every door, plate and dark figure. P2's dark shape is washing on a line. I found:
  - no person, child, drink or betting sign;
  - no firm's name, house number or vehicle plate;
  - the masks in place (P2's sign; P7's plate and door plate; P12's three).
- **Geograph.** I opened the pages of P1, P3, P4, P6 and P8 myself. Title, author, date taken and CC BY-SA 2.0 are as stated; P1's page also shows its 2013 upload date, which is not the taken date. I downloaded the same originals (1024 px; P4 640 px) for the re-measure below.
- **Poly Haven.**
  - The live catalogue (`assets?t=models`) has 521 models. All 44 inventory ids exist, which covers the 15 spot checks the task asked for.
  - The licence page (polyhaven.com/license) states that every asset is CC0.
  - I downloaded and looked at every 1k base-colour map of all 18 models used: 25 maps, including the three artwork maps. I also looked at six thumbnails at 640 px.
- **Stand-off budgets.** I wrote my own slide measure, importing only `trace`. For each eye I solve on the card for the point whose `trace` returns the object's picture place. The slide is the angle at the eye between that point and the true object, with exact pixel angles. I ran it for both room families.
- **White-board numbers.** With the writer's own boxes I reproduce P8_L, P8_R, P1_a, P1_b, P1_c and P1_e exactly. I then measured them again the way the gate measures (section 9): L over the joinery only, D over joinery and pane with no brick.

## Faults, worst first

### 1. Coloured window frames against Jafar's ruling of 3 October, without asking him

- **Where.**
  - TARGET.md 4.2 and `houses[].paint` give brown to east_parade_bay1, olive to bay5, blue to west_south_bay0, cream to west_south_bay2 and bronze to the chandler.
  - Check SITE-04 requires "cream 1, brown 1, olive 1, blue 1, bronze 1".
- **The ruling.** RULINGS.md, 3 October, sets the proof view's bars: "windows with white frames, sash bars, sky in the glass". terrace-front.py records the approved Hook sheet the same way: "every upstairs window is PALE - white frames over white nets".
- **Who sees it.**
  - The Hook camera (cam_A) stands on the east footway at x 4 looking north. Its near-left terrace is the east parade, whose first two houses are bay 0 (white) and **bay 1 (brown)**.
  - The reverse view's Mickey's row is the same parade, with bay 5 olive.
- **Why it is a fault.**
  - The writer read the 3 October rulings (section 2) but recorded no conflict.
  - The 8 October ruling ("photographs win") settles books against photographs. It does not settle a photograph tally against an explicit ruling of his.
  - CLAUDE.md: "if code must change a ruling, ask him first". Anything touching the look also reaches him on one page before merging.
- **Amendment.**
  - **Paints.**
    - east_parade_bay1: `white_fresh` (sound).
    - east_parade_bay5: `white_grimy`.
    - west_south_bay0: `white_grimy` (grimy kept).
    - west_south_bay2: `white_fresh`.
    - the chandler: `white_upvc`.
    - The other five are unchanged (white_grimy, white_flaking, and three white_upvc).
  - **Check SITE-04:** "white (white_fresh, white_grimy, white_flaking, white_upvc) 10 of 10 until Jafar's page rules otherwise".
  - **Jafar's page (OWED-05):** add one line with the 15 and 30 degree frames. "Window frames: all white as you ruled on 3 October (recommended), or the 1980s photographs' mix (white 55%, brown 13, cream 12, blue 8, olive 7: one house each)?"
  - **Records:** add `D13` to `photographs_win` saying that the ruling stands over the tally until he answers. Move the D1 bronze question onto the same line.

### 2. The white-board bands rest on the stone and the brick, and three "bare" windows can never pass

**(a) The photographs' L and D are not the gate's L and D.**

- The P1 boxes (hw_measure.WINDOWS) include the white-painted stone head and sill. That makes L 233 to 245 (the stone's paint reads 248 to 254).
- They also include a column of brick at the jamb. That makes D 110 to 117, which is P1's own brick median of 119.1. The "tight outlines' D/L 0.47 to 0.50" is brick over painted stone.
- The gate takes L from the joinery only (material index 2) and D with no brick (section 9). Measured that way on the 1024 px original:

| window | box (outline; pane), px | P/L | D/L | spread |
|---|---|---|---|---|
| P1_a | (435,396,451,447); (437,399,449,444) | 0.93 | 0.65 | 76 |
| P1_a, top rows out | (435,399,451,447); (437,402,449,444) | 0.93 | 0.71 | 68 |
| P1_b | (405,402,418,452); (406,405,417,449) | 0.94 | 0.65 | 64 |
| target (stone and brick in) | as hw_measure | 0.83 to 0.87 | 0.47 to 0.50 | 85 to 111 |

- So the real net windows would **fail WB-04** (D/L at most 0.55) and **fail WB-01's median cap** (at most 0.92).
- The old fault (D/L 0.85, spread 14) still fails WB-04 and WB-05. WB-05 alone tells them apart properly: the photographs measured this way give spreads of 64 to 76, the fault 14.
- No net window was measured inside WB-01's own range of 15 to 30 degrees. All of P1's are at 31 to 37.
- At P1's scale (a window 15 to 18 px wide) a 6 mm line cannot be resolved. So no outline percentile there can set a limit for the box's dark lines. 1a's D/L of 0.6 came from a profile across the lining (photograph 9: 105 to 125 against 220 to 250).

**(b) N0 is treated as bare, but three of the four N0 sites carry a drape.**

- The N0 sites with drapes are:
  - east_parade_bay1_upper_w0 (B2, a cream roller blind);
  - east_chandler_bay0_upper_w0 (B1, a white venetian blind);
  - west_south_bay1_gf_w1 (C1, a drawn brown curtain).
- A cream or white blind cannot read 0.10 to 0.45 of its frame (WB-02).
- A brown curtain cannot read blue over red by 10 levels (WB-03).
- The P/L and D/L bands were also taken from white and cream frames. A bronze frame (linear 0.05) or a brown one (0.09) gives a dark L, so P/L of 1 or more is correct for them and still fails.

**Amendment.**

- **hw_measure.** Use the boxes above for P1_a, P1_b and P1_e (P1_e the same way: stone head and sill and the brick column out). Take L over the outline minus the pane boxes. Record the new rows; P1_c keeps its band.
- **WB-01:** P/L 0.55 to 0.97, with no median cap.
- **WB-04:** D/L at most 0.72 on the outline (photographs 0.62 to 0.71, the fault 0.85).
- **New WB-04b (1a section 5):** on a horizontal profile across each stile-to-pane edge and a vertical profile across each rail-to-pane edge, a dip at least 1 px wide to at most 0.60 of L. The old fault (no line) fails it.
- **Window state for every WB check:**
  - `bare` = N0 with no curtain or blind;
  - `draped` = any B1 to B3 or C1 (no P/L band; spread at least 20 only);
  - C2 counts by its net.
- **Frame class:** the P/L and D/L bands apply to white and cream frames only. Under fault 1's amendment, every frame is one of those.
- **WB-08:** add WB-04b to the checks that must fail on the old pane.

### 3. A maker's name on the front of a placed model: `television_02` (gf_front_1)

- **Where.**
  - `television_02_diff_1k.jpg`, at about x 272 to 300, y 450 to 560 (lettered at 90 degrees), reads **"PARAGON Viewing System"**.
  - Poly Haven's own thumbnail shows it on the **front** bezel, left of the control buttons.
  - The inventory's entry says "a small rating plate on the back panel: blanked; no text on the front". A builder blanking only the listed marks would leave it.
  - The TV faces the cottage window at eye level (gf_front_1, the cool glow at night).
- **Size.** On the 3072 px picture the lettering is about 3 px high, so it is not readable from the street. It is still a maker's name on a model in the game, which the content rule forbids on anything. It also shows that "every model's 1k base colour was looked at" missed one, which is unit 7's fault 2 and the lesson this target says it applied.
- **Amendment.**
  - Change `inventory.polyhaven_models.television_02.marks` to: "a small rating plate on the back panel; 'PARAGON Viewing System' on the front bezel, left of the buttons: both painted out to the bezel's grey". Its status stays `blank`.
  - Add `paragon` to `brand_blocklist`.
  - Add to PIC-07: "the base-colour maps of every placed model checked at 1k against its marks entry, region by region, before the room is rendered".
  - I looked at the other 24 maps of the used models. Their entries are right: Ray Homes, Celine.F and the castle are replaced; URBAN quartz is blanked; the rest have no lettering. One exception is narrow point 2.

## Narrow points (each with its exact fix)

1. **The cottage rooms' budgets put the cameras at the card's centre, 0.9 m from the window.**
   - **The fault.**
     - `budgets_for` is called with `card_cx=0` for a window at `win_off_x` 0.9. So every review camera stands relative to the card's centre, not the window. That is why the H_UNDER visible zone "sees the right wall", which a camera 0.8 m in front of a ground window at eye level cannot.
     - With the eye at the window, as the camera table says, my `trace` run gives:
       - GF back: 0.381 true, 0.712 tolerated (H_UNDER);
       - side: 0.035 and 0.069;
       - ceiling: 0.024 and 0.048;
       - floor: 0.021 and 0.042.
     - The UP figures agree with the target: back 0.617 and 1.20, side 0.036 and 0.071, ceiling 0.034 and 0.067, against the target's 0.594, 1.159, 0.035, 0.068, 0.032 and 0.064. The 3 to 4 per cent difference is my exact pixel angle against `px x vfov / 1440`.
   - **Fix.**
     - Place the eye at the window (pass the window's street x as `xc`).
     - `budget_rule.back`: 0.38 true, 0.71 tolerated.
     - In gf_front_2, replace `ArmChair_01` (0.77 deep, over 0.71) with `painted_wooden_bench` (0.50).
     - Recompute the GF `visible_zone` rows.
2. **`drawer_cabinet` (up_bedroom_2) is a 2010s piece.**
   - **The fault.** It is a black steel frame with open oak shelves and drawers (thumbnail). Its top shows in the band of back wall seen from across (z 1.78 to 2.41). Its navy side strip carries three rows of faint lettering-like marks, while its entry says "none".
   - **Fix.** Replace it with `wooden_bookshelf_worn` (0.58, tolerated). The three bedrooms then still differ.
3. **`visible_zone`'s x is measured from the picture's left wall, not from the room's centre as section 3.3 says.**
   - **The fault.** It reads x 0.84 to 1.96 in a 2.8 m room and 2.48 to 3.32 in a 3.4 m one. The objects' `x_across` is from the centre.
   - **Fix.** Write "x from the picture-left wall" in 3.3 and in `rooms.visible_zone`, or convert the values to the centre frame.
4. **`box_shade` contradicts the paints, and its depth law darkens the frame's face.**
   - **The fault.**
     - `keep_paint` (albedo 0.78 to 0.80, roughness 0.40) disagrees with `paints`. For example, white_grimy is 0.66 with roughness 0.48.
     - "1.0 at y = 0 falling linearly to 0.6 at the glass" would paint the outer lining's street face (y 114.3) at about 0.68. That darkens L itself.
   - **Fix.**
     - `keep_paint` applies to `white_fresh` only; the paints table governs every house.
     - Faces whose normal points to the street take 1.0.
     - The depth law applies only to faces running into the wall: the reveal-facing sides of the linings, beads, pulley stiles and sash stiles.
5. **NIGHT-01's threshold of 100 cannot be met by some lit windows.**
   - **The fault.**
     - west_south_bay1_gf_w1 is lit at 20:30 behind a drawn brown curtain at 0.35 transmission. By the target's own factors that reads about 30 to 50.
     - The landings' bare 40 W bulb (PIC-02 night_lit 40) is marginal too.
   - **Fix.**
     - Give `curtains.night_lit` and the landing bulb an absolute linear emission, set so the gate's pane median reads 100 to 140.
     - Or make NIGHT-01 "lit = pane median at least 4 x the dark windows' median and r > g > b".
6. **The lit order lights landings before lounges.**
   - **The fault.** At 20:30 three of the five lit upper windows are landings (bay2_w1, bay4_w1, chandler_w1) and one is a lounge. In 1990 the evening's light is in the front room or lounge, and landings are lit briefly.
   - **Fix (Judgement).**
     - Order after the always-lit pair: west_south_bay1_gf_w1, east_parade_bay0_upper_w1 (lounge_1), east_parade_bay2_upper_w0 (lounge_2), east_parade_bay5_upper_w0 (lounge_3), east_chandler_bay0_upper_w1, then the bedrooms, then the landings.
     - The counts by hour stay as they are.
7. **P6's replacement form is named but not built, and all eight RC windows are identical.**
   - **The fault.** P6 (1994) shows a fixed top light across over **two** lower lights: a side-hung casement beside a fixed light, with the mullion near the middle. The source table describes it, but the RC is P7's form only.
   - **Fix.**
     - Add `RC2`: transom centred at 0.66 x 1676.4 = 1106.4 (face 70), a top light of one fixed pane, and a 70 mm mullion at x 0 from 60 to 1071.4.
     - The left light is a side-hung casement: stiles and rails 45, a 4 mm gap, the hinge on the jamb side. The right light is fixed.
     - Assign it to east_parade_bay4 (both windows). Add RC2 to KIT-12, KIT-14 and KIT-15.
8. **The segment under the arch.**
   - **The fault.** P8, the main photograph, shows the space between the flat sash head and the segmental brick arch filled by a cream-painted timber head that follows the arch. The street fills it with brick (terrace-front.py, ARCH_FANLIGHT False, 4 October). The target says only "the wall kit's" and does not record the disagreement.
   - **Fix.** Add `photographs_win` D14: brick kept by the 4 October decision; P8 shows a painted segmental head. Say which is built, and that it reaches Jafar's page if it changes.
9. **The cottage sill (D4) is "Jafar's to choose" but is not on his page.**
   - **Fix.** Add one line to OWED-05: "Cottage windows: head kept, sill 0.72 above the step (recommended), or sill 0.9 with 9 cm of brick under the eaves?"
10. **1a step 3 (reflections of the street in the upper panes) is deferred without its check.**
    - **Fix.** Add OWED-06 with 1a's check: "in the reverse view at least 2 of 3 upper panes show a horizontal edge with a step of at least 30 levels, moving when the camera moves 1 m".
11. **H_ALONG_15_ROAD stands in the road, not at the kerb.**
    - **The fault.** It is said to be at "2.6 m from the wall (the kerb edge of the road)". By the target's own numbers the footway is 5.125 − 3.505 = 1.62 m wide, so 2.6 m is 1 m into the carriageway.
    - **Fix.** Call it "in the road, 1 m out from the kerb", or move it to 1.62 m.
12. **Counts that do not match.**
    - **The fault.** Section 7.4 says "17 textures", but the inventory lists 9. The summary's "362 pass" is 342 offline and 364 with `--live --previews`.
    - **Fix.** Correct the count, and give the self-check line with the options it was run with.

## What is right

- **Unit 7's lessons.**
  - **Night wash:** it is unreal-look.json's `lantern_linear_rgb` (1.0, 0.25, 0.0) in the rooms' night_dark, the gate's lamps and NIGHT-04. The stale (1, 0.7055, 0) appears only as "not used".
  - **No hole between parts:**
    - Every point of the S22 and S11 opening (850 x 1676.4) lies on a lab node. The meeting rails close the gap between the panes, and the head lining closes the gap above the top rail. The 1.6 mm side clearance sits behind the staff bead.
    - The RC's only gaps are its 4 mm vent gaps.
    - The wall's piers run the full brick thickness, so the linings beyond the opening are buried.
  - **Bars and lights:** the S22 bar and its putty strips are centred on x 0, and the four panes are 352.6 each. The RC has one transom at 1207.0 and one top light. Nothing is unaligned.
  - **Marks and previews:** the marks found are right apart from fault 3. The previews are clean.
- **The method.**
  - Glass over a dark room, with the 1a pane values and the Fresnel table, which the self-check recomputes.
  - Nets as cards behind the glass, with the photographs' net mix (47/22/18 per cent).
  - The room card as the room's front plane, 0.27 behind the face, with `trace` imported, never rewritten.
  - The UP stand-off budgets, confirmed independently.
- **The photograph measurements are honestly reproducible.**
  - Every row recomputes exactly from the writer's boxes.
  - P8 measured the gate's way (all four panes, joinery-only L) gives P/L 0.57 and blue over red 46, inside WB-03.
  - The licences and dates are as stated.
- **Photographs win, D1 to D12.** Each disagreement is recorded with its choice: the bar 22.2 against 27 ±6, the front frame 76.2 by the ruling, the meeting rail, the transom 0.72 inside 0.66 to 0.75, and the six-over-six not built.
- **The lit table.**
  - It is nested and empty rooms are never lit.
  - The research gives no share, and it is marked as Judgement.
  - It is anchored on the street's one in three.
- **Building from target.json.**
  - The RC's parts, the added nodes (glass split at the bar, nets, drapes, the pendant) and the room cards' parameters are complete in numbers.
  - The sashes reuse the committed lab models, whose node bounds the self-check re-reads.
