FAIL

# The tea rooms (west_north bay 2, no. 14), the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target, build the shop or review any other shop. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit (the shop is lit and open to 22:00). I did not read the street review of this shop or any other shop's review.

Read: CLAUDE.md, RULINGS.md (1, 2, 3 and 9 October), NOTES.md (lessons 1 to 27 and the tea rooms' own section), TARGET.md sections 3, 4.2 and 5.7 and "Changes after the build" (A10, A11), target.json `shops.tea_rooms.display`, Rita's four reviews, `checks/check_tea_rooms_v1.json`, `sw_shops_tea.py`, and `sw_gen.cloth` and `card_atlas`.

Looked at: the two close previews; the four close gate frames (2560 x 1440) at 100 to 300 per cent; the three 4096 room pictures; the display glb's six embedded maps and the room models' 1k maps at 100 per cent.

Measured, all in my scratchpad (nothing in the repository or SCRATCH changed but this file):
- the display glb in Blender (sizes, seat and table heights, which way the chairs face, how the cards lean);
- the glass's mean luma, black patches, flat tones and burnt pixels in the four frames;
- the parallax, through `trace` itself and a projection of the same room points into both frames;
- the glbs' normal maps and UVs.

**In short:** the room behind the glass works. It is a deep, lit tea room's serving end (counter, cups on shelves, urn, cake domes, till, chalk menu, hatch). It moves exactly as the game's rule says, and no black slab or seam shows from either camera. The door is right, and nothing breaks the content rule's brand or period parts.

The near metre fails:
- the table set for tea is at child size: the table top 0.48 m off the bed, the chair seats 0.34, under a full-size teapot;
- both chairs stand with their backs to the table;
- the café curtains, the largest thing in the close view, read as corrugated plastic sheet, not cloth.

The first reads as a doll's tea party in a shop window: the content rule's "no children, no toys" and the real-size rule both fail.

**3 faults, 11 narrow points; 5 shared, known items named apart.**

## Faults, worst first

### 1. The table set is at child size (table top 0.48 m, chair seats 0.34 m, a full-size teapot)

- **Where:**
  - CLOSE_35 day: the table at x 1150-1420, y 845-1200; the chairs at 860-1165, 740-1290 and 1355-1600, 720-1125.
  - CLOSE_35_B day: the table at 1135-1420, 850-1210; the chairs at 945-1195, 720-1140 and 1400-1700, 740-1290.
  - The same in both night frames.
  - Each chair's seat is level with the upper part of the table's pedestal. The table top stands only a hand's height (0.14 m) above it; a real top stands 0.27 to 0.30 above the seat. The teapot is a third of the table's height.
- **Measured** on tea_rooms_display.glb (heights above the bed):

  | piece | built | real British size | what the target's own zones imply |
  |---|---|---|---|
  | round_wooden_table_02 | scale 0.628 on all three axes: wood top 0.469, laminate top **0.481**, 0.50 across | top 0.72 to 0.76; a café table for two 0.50 to 0.60 across | table zone w 0 to 0.75; tea set and sugar bowl zones w 0.75 to 0.85 (a top at 0.75) |
  | painted_wooden_chair_01 (x2) | scale 0.75: **seat 0.34** (the largest up-facing area, at z 0.33 to 0.34), overall 0.717 | seat 0.44 to 0.47, overall about 0.90 to 0.96 | chair zone w 0 to 0.90 (a full chair) |
  | tea_set_01 teapot, cups | scale 1.0: pot 0.164 tall, 0.257 with spout and handle; saucers 0.149, cup and saucer 0.083 | pot about 0.15; saucer 0.14 to 0.15 | |

  The model's own sizes are right (table 0.746 high at 0.80 across, seat 0.453). The build shrank them evenly to fit the 0.55 m deep window: the table to make it 0.50 across, the chairs by 0.75.
- **Whose:**
  - **The builder:** `sw_shops_tea.display` sets `ts = 0.50 / max(dims.x, dims.y)` as an even scale, and `cs = 0.75`.
  - **The check:** SO-06 counts only the room's models. Its limit is also now 0.60 to 1.1 (Rita's was 0.9 to 1.1), so 0.628 and 0.75 would pass even if counted. DSP-01 tests only the window box. NEV-02 and TRD-01 call the set "a 1980s cafe's", not its size.
  - **The target:** "scaled to a 0.55 m cafe table (the model is 0.80)" invites an even scale, though its own w zones put the top at 0.75.
- **Exact fix:**
  - **(a) The table.** Keep it 0.50 across, but at real height: scale round_wooden_table_02 by (0.628, 0.628, 0.965), so the wood top is at 0.720 and the 12 mm laminate surface at 0.732. The tea set, sugar bowl and menu stand ride on `top_z` as now.
    - The better fit to the target's research ("Formica tables") is a scripted café table instead: a 0.50 m round laminate top, 25 mm thick, with a 3 mm aluminium edge band, its surface at 0.732; a 50 mm chrome column; a black cast four-arm base 0.40 m across and 30 mm high.
    - Either way the LIT-08 pedestal (narrow 8) is re-measured.
  - **(b) The chairs** at scale 1.0 (seat 0.453, overall 0.957), turned as fault 2 says:
    - left chair centred at u 1.215 (u 0.945 to 1.485), right chair at u 2.135 (u 1.865 to 2.405), both at v 0.32 (v 0.104 to 0.536);
    - that leaves 11 mm to the curtain's back (v 0.093), 14 mm to the bed's back (0.55) and 45 mm to the strawberry cake's plate (u 2.45);
    - each seat's front edge stands 0.06 m in under the table's rim;
    - the chairs' outer halves stand behind the curtains' lower edge, which is right for a window seen through café curtains.
  - **(c) A new row, DSP-05, failing the build:**
    - every model on the bed is at scale 0.9 to 1.1 unless a Judgement in NOTES names it;
    - a table top is 0.72 to 0.76 above the floor it stands on;
    - a chair seat is 0.44 to 0.47;
    - SO-06 covers the display's models as well as the room's, and its limit goes back to 0.9 to 1.1 (a piece under 0.9 only as a named Judgement).

### 2. Both chairs stand with their backs to the table

- **Where:** CLOSE_35 day and CLOSE_35_B day (boxes as fault 1).
  - The left chair's back posts rise beside the table's left edge, and its seat runs away to the left.
  - The right chair's back is beside the table's right edge, and its seat runs away to the right.
  - Nobody sets a café table so. It reads as two chairs pushed back from the table, the wrong way round.
- **Measured** on the glb:
  - Left chair: x −0.664 to −0.260; its back (everything above z 0.45) at x −0.321 to −0.260, beside the table's rim at x −0.25; its seat runs from x −0.312 out to −0.664.
  - Right chair: back at x +0.260 to +0.321; seat from +0.312 out to +0.664.
- **Whose:** the builder. `d.piece("painted_wooden_chair_01", tu - 0.462, ..., rot=(0, 0, -pi/2))` and `tu + 0.462, ..., rot=(0, 0, +pi/2)` have the signs the wrong way round for this model. Its own docstring meant "their front legs under its edge".
- **Exact fix:**
  - Left chair `rot=(0, 0, +pi/2)`, right chair `rot=(0, 0, -pi/2)`, at the places fault 1(b) gives.
  - Add to DSP-05: the unit vector from each chair's back to its seat front points within 45 degrees of its table's centre.

### 3. The café curtains read as corrugated plastic sheet, not cotton (the largest thing in the near metre)

- **Where:** the two panels cover about 30 per cent of the glass in CLOSE_35.
  - CLOSE_35 day: left panel x 0-960, y 640-1280; right panel 1672-1960, 624-928.
  - CLOSE_35_B day: 552-880, 608-944 and 1624-2560, 640-1216.
  - Both night frames.
- **What is wrong, part by part:**
  - **The folds** are sharp, evenly spaced V ridges in flat-shaded bands.
    - `sw_gen.cloth` samples each 0.085 m fold at only 6 points (nx = width / (wave / 6)).
    - The object is not smooth-shaded (`gm_object(... "curtain_" ...)` has no `smooth=True`).
    - The fold depth is the same across the whole panel.
  - **The hem is a ragged saw edge**, like torn paper (CLOSE_35 day 0-900, 1090-1280; CLOSE_35_B day 1640-2560, 1090-1260).
    - The scallop is inverted: `hem = 0.03 |sin(pi x / 0.10)|` puts the lowest points at the cusps.
    - Its 0.10 period does not match the 0.085 folds, so the points fall anywhere.
  - **The head is a straight cut edge hanging 14 mm under the rod,** with nothing joining them: the cloth's top is at w 0.89, the rod's underside at 0.904.
    - It shows as a dark band 5 to 7 px high along every rod: CLOSE_35 day 1600-2000, y 620-627; CLOSE_35_B day 560-960, y 612-617.
    - The target asks for "cream cotton gathered on a brass rod, scalloped head".
  - **The rod floats.** It hangs 70 mm behind the glass on two 4 mm pins that rise 40 mm into nothing. The left pin shows at CLOSE_35_B day x 547-550, y 588-605.
    - At night the brass, metal 1.0 and roughness 0.3, mirrors the black stand-in world. It reads as a black line: 5,030 px under luma 8 in CLOSE_35 night, x 0-940, y 632-664.
  - **The cloth is a flat colour** (208, 200, 178), roughness 0.9: no weave, no sheen, no light through it.
    - At night the room's tubes are behind it, but it reads as a grey-brown pleated screen (CLOSE_35 night 0-940, 660-1270), lit only by a row of hot spots along its head from the spill.
- **Whose:** the builder (`sw_gen.cloth` and `sw_shops_tea.display`), against the target's own row ("gathered on a brass rod, scalloped head").
- **Exact fix:**
  - **(a) The head.** Scallops cut into the top edge: arcs 0.10 wide and 0.035 deep, between 25 mm tabs that wrap the rod (each tab a 25 x 60 mm strip folded round it, inner radius 11 mm). The cloth meets the rod with no gap (at most 2 mm).
  - **(b) The folds.** A smooth gather, 1.6 times fullness:
    - each fold a sine of 0.09 to 0.13 m, the period varied ±15 per cent fold to fold, at least 16 vertices a fold;
    - depth 0.022 at the head growing to 0.030 at the hem;
    - smooth shading (auto-smooth 60 degrees).
  - **(c) The hem.** Straight, with a 30 mm turned hem (a second layer 3 mm proud). If a scalloped hem is kept as well, the arcs bulge DOWN, with the points up at the joins, and their period equals the fold period.
  - **(d) The cloth.**
    - Cream cotton (226, 218, 196), held at the window's 0.88 toning: about (199, 192, 172).
    - Roughness 0.85, sheen 0.4.
    - ambientCG Fabric034's normal map (already Rita's velvet's, already catalogued) at strength 0.15 and a 0.08 m tile.
    - A Translucent BSDF mixed in at 0.3, so the lit room glows through it at night.
  - **(e) The rod.** Remove the two up-pins. At each end of each rod, a brass end bracket (a 16 mm round socket on a 70 mm arm, its plate screwed to the back face of the jamb or mullion). Brass roughness 0.45, so the rod is not a black line at night.
  - **(f) A row.**
    - The cloth's head touches its rod (gap at most 2 mm).
    - No visible face of the cloth is flat-shaded.
    - In the close day frames, the share of 32-pixel blocks on the cloth with a standard deviation under 0.8 is under 2 per cent.

## Narrow points, each with its exact fix

1. **The hours plate is missing from the shop door.**
   - Target 4.2 (which the tea rooms' row adopts "as 4.2") puts "the hours plate (4.1) on the glass beside" the OPEN sign.
   - The 4.1 set made it, `hours_plate.tea_rooms`: MON-SAT 6.30 AM - 10 PM, SUN 8 AM - 12 NOON, 300 x 190 mm, files in fascias/panels/hours_signs. But front_members.json has no hours member, and CLOSE_35_B day shows none (the door leaf at x 224-480).
   - Whose: the builder.
   - Fix:
     - place the panel inside the door's lower pane, centred across the leaf (u 1797), its centre at z 1.300 (1.205 to 1.395, 14 mm under the glazing bar), d 39;
     - GLS-01 lists it;
     - a door row checks that the 4.2 set (bell, OPEN/CLOSED card, hours plate) is present.
2. **The price cards stand before the wrong goods.** At 100 per cent:
   - "TOAST 30p" stands between the strawberry cake and the plant (u 2.90; CLOSE_35_B day x 2150-2240, y 1400-1440, cut by the frame), though there is no toast in the window;
   - "HOME MADE" stands before the left chair (u 1.25; CLOSE_35 day 1078-1125, 1215-1260);
   - "TEAS 25p" stands before the right chair (u 2.00).
   - Fix:
     - "TOAST 30p" becomes "GATEAU 45p", at u 2.62 before the strawberry cake's plate;
     - "HOME MADE" moves to u 0.30, beside CAKES 40p before the carrot cake;
     - "TEAS 25p" moves to u 1.60, under the table's front rim;
     - each card stays at v 0.02, and SO-07 / DSP-03 run again.
3. **The window card's suction cups are black upright cylinders.** Each is 28 mm across and 30 mm tall, in (60, 60, 62), with its axis vertical, and reads as a black square clip: CLOSE_35 day 1750-1768, 417-433 and 1917-1933, 432-447; CLOSE_35_B day 1880-1912, 312-344 and 2499-2544, 256-296.
   - Fix: two clear PVC discs, 30 mm across and 3 mm thick, flat on the glass's inside face (axis along v): base (230, 230, 230), transmission 0.6, roughness 0.2. Each carries a 15 mm steel hook through a punched hole 12 mm below the card's top edge.
4. **The window card is a flat, perfect board.** It is 0.60 x 0.38 m in one flat tone (206, 200, 180) with no grain, and in a typeface whose repeated letters are identical: 124 flat 32-px blocks in CLOSE_35_B day at x 1872-2512, y 256-656.
   - Fix:
     - card grain: a 1 mm fibre noise of ±4 levels on the base colour, roughness 0.85;
     - a 1.5 mm bow along its width;
     - for the hand lettering, a per-letter jitter of rotation ±2 degrees, baseline ±1.5 mm and size ±4 per cent.
5. **The same flat clip-art print hangs twice in the room** (repeats Rita's v1 narrow 7).
   - hanging_picture_frame_01 (right wall) and _03 (the oval, left wall) both carry `invented_print(kind=0)`: a banded gradient sky, a flat green hill and a white inverted triangle for a sail. In the tall frame it is stretched.
   - Seen at CLOSE_35 day 1248-1336, 320-544 (the right wall), and in the room picture at about (3380-3520, 470-900) and (600-675, 520-795).
   - Fix: frame_01 a portrait (1 : 2.4) crop and frame_03 an oval-masked crop, each of a different CC0 Poly Haven HDRI of a coast or harbour (not lake_pier, which frame_02 already shows). Saturation 0.7, a slight warm cast, paper grain, no person, each with a catalogue line. Never the same print twice in one room.
6. **The card under the chalk menu is illegible.** It is a black card with cream text about 12 mm high (CLOSE_35 day 695-785, 470-490; CLOSE_35_B day 1670-1760, 470-495; a smear at 100 per cent also in the room picture). This repeats Rita's v2 narrow 10.
   - Fix: paper (235, 232, 222), ink (25, 25, 50), one line of at most 14 characters at a 30 mm cap (for example TEAS FROM 25p, which the board's notices already use). Or drop the card: the window card says the rest.
7. **The cork notice board is a flat orange slab:** (170, 126, 84), no grain, no frame, sharp corners (room picture about 3550-3760, 460-880; CLOSE_35 day about 1360-1480, 296-496).
   - Fix: a granular cork made by script (two tones, (176, 132, 88) and (150, 108, 70), a 2 mm grain, roughness 0.95), a 20 x 15 mm pine frame (200, 160, 110), and a 6 mm coloured pin head on each notice.
8. **The pedestal is dark at night** (LIT-08, the builder's named shortfall). The walnut pedestal reads 0.28 (CLOSE_35) and 0.21 (CLOSE_35_B) of the room behind it, against 0.6.
   - It looks like a dark wooden pedestal, not a fault in the picture.
   - Fix: with fault 1(a)'s scripted table, the chrome column and black base replace it. With the model kept, re-measure after the height change, and if it still fails, name it again.
9. **PIC-05g sits at its limit at CLOSE_35_B night** (0.0100; CLOSE_35 night 0.0089).
   - Burnt clusters: the laminate top (CLOSE_35_B night 1135-1423, 859-926: 5,902 px with a channel at 250), the teapot (1212-1357, 775-867) and the strawberry plate (1796-2010, 1263-1363). Another 6,141 px are the shared orange bar.
   - Fault 1 raises the top 0.25 m toward the spill.
   - Fix: tone the laminate to (142, 126, 94), and set the spill by one 16-sample test of the two close night frames before the gate (lesson 26), so that PIC-05g is at most 0.008 and LIT-08 holds.
10. **night_dark's pilot lamp has no lamp.** A 6 W point light 0.20 above the counter's left end makes a hot glow on the plaster beside the first cake dome, with no fitting to cast it: room picture, night_dark, about 870-975, 845-1000.
    - night_dark is not in the close view, since the shop is lit until 22:00.
    - Fix: a 10 mm amber indicator lens on the tea urn's plinth (emission 2700 K), with the light moved 0.02 m in front of it at 0.5 W. Or a 15 W pygmy bulb in a small brass wall bracket at room x −2.45, z 1.55, with the light inside its shade.
11. **No seating in the room (the target's rule; the builder's named shortfall).** The room is a counter end: a tea room's floor with no table reads as a take-away counter, and only the window's table says "sit down".
    - It is narrow because the counter, cups, urn, domes and chalk menu carry the trade, and the target bars free tables in the picture (they smeared).
    - Fix, for the target's owner: record it in 5.7 as a Judgement ("the room is the serving end; seating is the window's"), or move real-geometry tables into the game in the first metre behind the card. That changes the method for every shop, so it is his call, not this build's.

**Owed, not counted:** 48 samples (128 on the PC); the steamed glass and the curtain's sway; the game's glass, Lumen, exposure and TSR; the joinery's wear (W1).

## Shared, known (the gate's and the kit's; not counted in the verdict)

- **(a) The far pavement's lamp pool shows in the night glass as a burnt orange bar:**
  - CLOSE_35 night 1040-1920, 672-752 (across the middle light, behind the table);
  - CLOSE_35_B night 560-1150, 664-728 (the left light).
  - It is 6,141 of the burnt pixels in CLOSE_35_B night.
- **(b) night_dark's top corners are hot orange:** the room picture's two top corners, about 0-400 and 3700-4096, y 0-120. The sodium wash is the card's full width.
- **(c) Glass parts of models dropped:** the room picture's three frames, the wall clock and the till show no glass at all (room picture 370-565, 450-780; 600-675, 520-795; 715-780, 565-715).
  - All five source glTFs have a glass primitive (`*_glass`, BLEND).
  - placed.json lists one object per frame.
  - The scripted cake domes render as glass (lesson 19 holds).
- **(e) Sheet orientation:** the menu stand on the table leans toward the glass. Its top edge is at v 0.075 and its foot at v 0.085, 12 degrees forward instead of back.
- **(f) CLOSED on the door at night** although the shop is lit and open to 22:00: CLOSE_35_B night 345-395, 585-630.
- **(d) Maker's marks: checked fully; none found** (see "Measured").

## The builder's named shortfalls, judged

| shortfall (NOTES, check file) | judgement |
|---|---|
| The room is sparse, with no tables or chairs | **Narrow** (11), the target's rule |
| Two cake domes (the target counts one) | **Right**: they read well and render as glass |
| The tea set's plates on the shelf as scripts | **Right** |
| The table 0.50 m across, not 0.55 | **Right**: 0.50 is a real café table. Its **height** is fault 1 |
| The steamed glass not modelled | **Owed** to the PC, not a point |
| The window card and the chalk menu in the project's lettering | **Acceptable** (narrow 4 asks only for grain and jitter) |
| The whites and the bed toned for the night gate (china and curtain 0.88, chairs 0.78, bed (122, 96, 64), laminate (160, 142, 106)) | **Acceptable** look decisions. The chairs read pale grey-blue, which is fine |
| LIT-08: the walnut pedestal at 0.28 and 0.21 | **Narrow** (8). Fault 1's fix replaces or re-measures it |
| GLS-03 fails at STREET_30 (16.7) | **Not this view.** The close frames pass (10.3, 10.5). I could not re-measure (see the last section) |
| night_dark's wash 70 per cent stronger | **Acceptable** (PIC-03 21.7, within 12.4 to 40). Not seen from the close view |
| The stand-in lamps left out of glossy rays; spill 150 W | **Acceptable**: gate stand-ins |
| 48 samples | **Owed** (128 on the PC) |

## The check rows: which I trust

**Trust:**
- PIC-01 to PIC-06 and X-NOISE;
- PRJ-01 to PRJ-03 (my own projection agrees, below);
- SO-01 to SO-05 and SO-07;
- DSP-02, DSP-04;
- INV-01 to INV-06, NEV-01;
- GLB-01, FAS-01, FAS-01n, FAS-01c, FAS-03 (I re-ran the normal-map and UV tests on both glbs: normal blue means 236 to 254, 0 textured primitives without TEXCOORD_0, 0 negative texCoord);
- FRN-01 to FRN-05, FRN-07 to FRN-10;
- GLS-01, GLS-02, CAM-01, LIT-06.

**Pass, but blind to this shop's faults:**
- **SO-06** counts only the room's models, and its limit is 0.60 to 1.1; the display's 0.628 and 0.75 escape it (fault 1).
- **DSP-01** tests the window box, not real sizes.
- **DSP-03** tests intersections and silhouettes, not which way a chair faces (fault 2).
- **NEV-02 and TRD-01** call the table set a café's at any size.
- **FRN-03** checks the door's bell and plates but not that the hours plate exists (narrow 1).
- **No row** looks at a cloth's head, folds or shading (fault 3).

**The cloud's stand-ins only (they prove the gate, not the game):**
- LIT-01, LIT-02, LIT-02b, LIT-05, LIT-07, LIT-08, GLS-03, PIC-05g;
- PRJ-02 (the gate's own bake; PC-01 owed).

## Measured

**Furniture and crockery against real British sizes** (display glb, above the bed): see fault 1's table.
- Also measured: the carrot cake 0.31 across on a 0.32 china stand 0.115 high; the strawberry cake 0.25 on a 0.34 plate; the plant 0.27; cups and saucers as the teapot row.
- In the room: counter 1.0 high and 0.55 deep; shelf boards at 1.35 and 1.75; urn 0.50 high and 0.26 across; till 0.42; kettle 0.30; cake domes 0.28 across and 0.265 high; shelf cups on 0.156 saucers; wall clock 0.30.
- All are real-size, but the window's table and chairs.

**The glass's mean luma** (rectangles inside each light, the full gate frame with its reflection and goods):

| frame | left | middle | right | all glass | wall beside |
|---|---|---|---|---|---|
| CLOSE_35 day | 116.4 | 71.7 | 123.2 | 103.7 | brick 89.0 |
| CLOSE_35 night_lit | 70.0 | 75.0 | 56.9 | 69.8 | brick 20.1 |
| CLOSE_35_B day | 105.9 | 71.1 | 145.0 | 115.4 | pilaster 100.1 |
| CLOSE_35_B night_lit | 65.1 | 77.4 | 55.6 | 64.0 | pilaster and door 28.5 |

- The rectangles are: CLOSE_35 at x 32-944, 1056-1616, 1712-2000; CLOSE_35_B at 544-864, 960-1520, 1648-2528.
- The target's composite floors are day 33 and night 45. The build's own LIT-02 at CLOSE_35 reads 50.3 and 67.8 on the room-only composite.
- **The lit room at night is 2.2 to 3.5 times as bright as the wall beside it, and the day room reads plainly.**

**Black and flat regions inside the glass:**
- The largest patch under luma 8:
  - by day, 866 px (CLOSE_35_B, 1102-1126, 584-665: shade under the counter's end);
  - at night, the black curtain rod's line (fault 3) and 1,966 px of shade in the middle light (CLOSE_35_B).
- No void and no slab.
- Flat 32-px blocks (standard deviation under 0.8) are 1 to 13 per cent of a light's blocks: the window card (narrow 4), the cloth's flat facets (fault 3), the plain dado and the ceiling.
- The door joints: lowest luma 31 in the CLOSE_35_B day door area. No black strips; 114 px under luma 8 in the whole door area.

**Burnt pixels** (a channel at 250): CLOSE_35 day 0.0014, night 0.0089; CLOSE_35_B day 0.0001, night 0.0100. Where they fall is in narrow 9 and shared (a).

**Parallax, by `trace` itself** (tools/ue/make_interior_material.py, imported; west card, side −1, card x 24.35 to 29.65 at y −5.875, z 0.65 to 3.05; W 5.3, H 2.4, D 4.5, camera_d 5.3):
- **The point:** the top-left corner of the chalk menu's frame (back wall, 0.03 off: room hx 3.20, height 1.94, depth 4.47).
- **On the card:**
  - from CLOSE_35 it crosses the card at street x 27.126 (card px 2145.4);
  - from CLOSE_35_B it crosses at x 28.483 (card px 3193.8);
  - that is 1.357 m apart for 2.0 m of eye travel (2.0 x 4.47 / 6.59 = 1.357).
- **Back through `trace`:** both card points return to picture px (2279.1, 616.5) and (2275.3, 616.5). The render rule's own place is (2278.6, 617.2); the 3.8 px is the frame's 0.03 stand-off.
- **In the frames:** projected into the gate frames, the point falls at (672, 376) in CLOSE_35 and (1661, 386) in CLOSE_35_B. Looked at 300 per cent, the board's corner is within 2 px of each.
- **Two more points** land the same: the board's bottom-right corner (801, 472) / (1773, 467) and the hatch frame's top-left (821, 404) / (1797, 395).
- **The wall clock** (left wall, 0.066 off): from CLOSE_35_B it lands at (979, 422), where the clock is. From CLOSE_35 its card point (x 25.876) is behind the door, outside the window, so it is rightly not seen.
- **So the back wall's parallax differs between the two cameras exactly as the rule says.** No black slab, no end of the picture, and no seam where the bed meets the room's floor from either camera.

**Every legible word at 100 per cent** (both close frames, day and night):
- Window card: BREAKFASTS, LUNCHES, TEAS.
- Price cards: CAKES 40p, HOME MADE, TEAS 25p, TOAST 30p (cut by the frame at CLOSE_35_B).
- The menu stand: TEAS FROM 25p (small, just legible).
- Door: OPEN by day, CLOSED at night, 14 on the fanlight.
- Room: TODAY'S MENU, TEA 25p, COFFEE 35p, TOAST 30p (soft), and the clock's numerals.
- The room's notices (TABLES BOOKED, TEAS FROM 25p, OPEN 6.30 - 10, CAKES MADE HERE, THANK YOU, LUNCH 12 - 2) and the till's key labels are not legible from the close cameras.
- **All are the project's own words and numbers, and acceptable.** The prices fit a 1990 café.

**(d) Maker's marks, every placed model's base colour at 100 per cent, region by region:**
- **The display glb's six embedded 512-px maps:** round_wooden_table_02, painted_wooden_chair_01, tea_set_01, potted_plant_04, carrot_cake, strawberry_chocolate_cake.
- **The room's maps at 1k,** in quadrants or halves:
  - CashRegister_01 (the cleaned map and its glass map);
  - wall_clock (cleaned);
  - vintage_electric_kettle, metal_jug, tea_set_01;
  - the three frames' timber maps and their three art maps;
  - hamburger_buns, carrot_cake, strawberry_chocolate_cake.
- **No maker's name, firm, logo or modern mark survives.** Only generic marks remain:
  - the till's key labels (TOTAL, numerals, X Y Z, A B R, and tiny key tabs illegible even in the map);
  - a mirrored readout number (0 2 1 3 7 7 0);
  - the kettle's thermometer dial (THERMOMETER, °F, °C, numerals).
  - None of these is legible in the room picture.
- **The blanked regions read clean:** the till's TITCH plate and slips, and the clock's URBAN / quartz.
- **The rest of the content rule:** no drink, gambling or weapon, and no tobacco. Nothing after 1992 (no barcodes, flat screens or modern packaging). The only breach is fault 1's child-size table set, which reads as a toy.

## What is right

- **The room behind the glass.**
  - It is a deep, lit room that moves exactly as the game's rule says (above).
  - It reads as a 1990 tea room's serving end: cups on saucers along two shelves, plates in stacks, a milk churn, two cake domes that read as glass, rolls on a board, the teapot and cups, a vintage kettle, an old till, a stainless urn, a chalk menu, a hatch with its roller half down, a chequered floor, and a cream and brown dado.
  - It is sharp at 4096 pixels.
  - The return walls close both ends. LIT-02b at CLOSE_35_B is 0.27 per cent, with no slab.
- **The goods are scans, not props:**
  - the teapot and cups with their grey floral print;
  - the carrot cake with a slice out;
  - the strawberry and chocolate cake;
  - the haworthia in its white pot;
  - the painted slat chairs.
  - Each stands on its support; nothing is buried or through a board (DSP-03 and SO-07 agree with the glb).
- **The door matches the target:**
  - T1 cream leaf, glass from 871 with the bar at 1423;
  - the lever on the left stile, the brass letter plate in the lock rail, the brass kick plate and foot strip;
  - the green OPEN card by day;
  - the gilt 14 on the fanlight;
  - the band above both doors;
  - the dark-brown F1 side door with its vertical letter plate in the muntin and its centre knob;
  - no black strips in any joint.
  - The bell hangs on the top rail, 90 mm in from the hanging stile (FRN-03). It is hidden by the stile's depth from both close cameras (see the last section).
- **The night:** no arc, no burnt head band, no glowing frame; the mullions are lit only by the street. The lit room is bright and warm behind the glass (narrow 9 and shared (a) aside).
- **Rita's export faults are not repeated:** normal maps are true normal maps, every textured primitive has UVs, no coplanar black strips, no see-through slot.

## What I cannot judge from the files, and what I could not repeat

**Could not repeat** (the check renders were removed from SCRATCH, and only their camera files remain):
- GLS-03's p95 against the reflection-off renders;
- LIT-02's and LIT-02b's room-only composites (my glass lumas above are on the full frames instead);
- LIT-08's per-piece rings (no object-index pass);
- FRN-10's front mask;
- DSP-03's silhouette shares;
- PRJ-02's and PRJ-03's correlation of the baked cards: the baked cards are gone. I checked the projection instead through `trace` and the frames themselves (above).

**Cannot judge:**
- the game's own glass (reflections, the Fresnel hand-over at 61 degrees), Lumen's light on the window, the exposure, the card under TSR;
- the steamed glass and the curtain's sway;
- the bell: it is not seen from either close camera (the hinge stile's depth hides it at about 64 degrees off the door), and its swing and sound are not in the files;
- wear and wet (the game's layers);
- the street view.
