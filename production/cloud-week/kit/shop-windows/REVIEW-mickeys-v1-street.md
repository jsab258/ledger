FAIL

# Mickey's front, the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2; 15 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the front. I judged the street view only. I did not read the close review.

Jafar's ruling of 9 October applies: a piece that fails only on narrow points passes, with those points listed. This piece has two faults, so it fails.

**What I read:**
- CLAUDE.md and RULINGS.md (1, 2, 3 and 4 October).
- NOTES.md: "For the next nine shops", batch A's lessons 16 to 27, Mickey's own section (M1 to M6 and the known shortfalls), and "Try 2, Mickey's and the empty unit: NOT DONE".
- TARGET.md: section 3, table 5.1, and "Changes after the build" (A12 and A14).
- Rita's four reviews.
- `checks/check_mickeys_v1.json`, all 24 rows.
- 4.1's manifest for Mickey's (the fascia and the glass rows).
- The 3.2 spec of `stallriser.tile_patterned` (shopfronts target.json at dd706f6).
- The walked room's mickeys branch in `tools/art-recipes/shop-room.py`: its glass lettering and its frame.

**What I looked at:**
- The two street previews of 13 October.
- The four 2560 x 1440 gate frames (STREET_SQUARE and STREET_30, day and night_lit), at full size and in crops up to 6 times.
- `tile_pattern.png`.
- The Hook sheet.
- The walked front of 8 October (`production/previews/mickeys-front-day-night-2026-10-08.jpg`).

**What I measured:**
- My own pinhole projection from the gate's camera files. The street frame is left-handed, so +x is the viewer's left on this east front.
- Rec.709 luma (0 to 255) over the projected glass rectangles (inset 4 px), the brick beside, the fascia, the letters and the stallriser.
- A scan for dark patches on the front.
- The colours and the pitch of the stallriser's tiles.
- The exported fascia normal map.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview JPEG).

## Faults, worst first

### F1. Nothing on the front says "minicab": the trade does not read from the street (day and night, both cameras)

**Where:**
- STREET_SQUARE: the three lights, x 900 to 1660, y 511 to 923 (1600: x 563 to 1038, y 319 to 577).
- The shop door's fanlight, x 1680 to 1890, y 505 to 570.
- STREET_30: the same lights at x 1016 to 1590.

**What it looks like:**
- The only words on the front are MICKEY'S, the street number 1, and OPEN (day) or CLOSED (night).
- Through the glass the gate shows a flat card.
- Across the street the front reads as "a shop called Mickey's". It could be a café or an outfitter as easily as a cab office.

**Why:**
- The target's table 5.1 lists three glass rows: `'0632 960418'`, `'MINICABS · 24 HOURS'` and `'1'`.
- 4.1 drew only the "1". Its manifest (`not_drawn_here.existing_not_approved`) calls the other two "another family's" (shop-room.py) and not approved, because "24 HOURS" contradicts the cast's hours (7.00 to 3.00).
- The build placed neither row. NOTES (M1 to M6, the shortfalls) does not say so.
- GLS-02 counted the "1" alone (850 ink points). Mickey's check has no TRD-01 row, although A14 says that row applies to every shop.

**Why it is a fault:**
- The walked front that passed the phase-1 gate (8 October; GATE-1.1-REVIEW-3, V10) carried the firm's number and "MINICABS" on its glass.
- shop-room.py's own note says why: "the window is the sign" (the 1980 Brixton photograph).
- This front drops that, so the shop's trade has gone from the street.

**WHOSE:**
1. The target, first: it lists rows that 4.1 refuses, and never settles them.
2. The builder: dropped them without naming it.

**EXACT FIX:**
1. **His page, one line:** the words on Mickey's glass.
   - Recommended: "MINICABS" and "0632 960418", with "24 HOURS" dropped because it contradicts the cast's hours.
   - Alternatives: all three, as on 8 October; or "MINICABS · 7 AM TO 3 AM".
   - 0632 960418 is acceptable as a number. shop-room.py calls 0632 the code television used for numbers that rang nowhere, and its successor, 01632 960 000 to 960 999, is the drama range today.
2. **The builder** draws them as 4.1 glass rows: gold leaf with a black shade, Marcellus SC (the board's face and the walked room's), on the glass's inside face at d 29 like the "1".
   - "MINICABS", cap 110 mm, centred in the left light: u 924, street x 8.076.
   - "0632 960418", cap 90 mm, centred in the middle light: u 2025, street x 6.975.
   - Both baselines are 2150 above the footway, so the cap tops sit at or below 2260, clear of the transom's glass edge at 2400.
   - The rows are about 0.70 and 0.74 m wide in lights of 1.07 m. No bar crosses them.
   - The right light stays clear.
3. **One home for these words:** when the new front goes into the game, delete `glass_number`, `glass_word` and `fanlight_word` from shop-room.py's mickeys branch, or drop the target's rows. Either way the words exist once, not on two panes.
4. **Two check rows:**
   - GLS-02 counts every row the target lists, and fails on a listed row that is neither drawn nor named as dropped in NOTES.
   - TRD-01 runs for a front-only shop: at STREET_SQUARE by day, a trade word with a cap of 80 mm or more on the fascia or the glass, not crossed by a bar.

### F2. The stallriser's tiles are drawn at twice their size and stretched: a printed harlequin, not six-inch tiles

**Where:**
- STREET_SQUARE day and night: the patterned band, x 891 to 1660, y 949 to 1042, which is z 115 to 515 above the footway (1600: x 557 to 1038, y 593 to 651).
- STREET_30: x 1000 to 1590, y 900 to 1010.

**What it looks like:**
- Across the whole stallriser runs one bold lattice of big cream, blue and black triangles. It is the loudest thing in the picture.
- At 8.76 m it reads as a printed panel, not as tiles.
- The Hook sheet's Mickey's has cream tiles with a fine pattern under a dark skirting, and so did the walked front of 8 October.

**Measured:**
- The blue diamonds are about 70 px wide and 50 px tall at STREET_SQUARE: 308 x 220 mm. Each one should be a 152.4 mm square tile.
- The 400 mm band holds two rows of the motif, each about 200 mm.
- The 3.2 spec asks for two courses at a 155.4 pitch, then one plain half course of 79.2.
- The print's grout lines fall under one pixel, so no joint reads.
- The colours are right, under the sky: blue (41, 56, 110), cream (167, 164, 153) and black (32, 34, 38), on 24, 35 and 16 per cent of the panel.
- The panel's heights are right: black skirting z 0 to 110, the patterned band, the cap, the sill.

**Cause:**
- `tile_pattern.png` holds 3.2's 2 x 2 repeat (A B over B A), which is 304.8 mm square.
- NOTES M4 lays it at 609.6 mm across and stretches it to the band's height.
- FRN-05's paint check skips printed parts (its "paints used" are only pilaster, side door and window frame). So nothing checks the tile.

**WHOSE:** the builder (M4).

**EXACT FIX:**
1. Map the print in millimetres:
   - u_tex = (u − 350) / 304.8
   - v_tex = (z_cap_underside − z) / 304.8
   - This covers the two full courses: 310.8 mm down from the cap's underside, each a 152.4 tile plus a 3 mm joint.
2. Below them, add one plain half course 76.2 mm high in cream (222, 212, 184), with a 3 mm joint.
3. Keep the black skirting as built.
4. Draw the joints 3 mm wide in the print's own grout grey, so they read at the close camera. They are about 0.7 px at the street.
5. Add a row to FRN-01: on the STREET_SQUARE day render, the stallriser's motif pitch is 152.4 ± 5 mm across and up (35 ± 1 px).

## Narrow points, each with its exact fix

### N1. The glass shows the gate's flat stand-in card: a dim flat pane by day, a grey board at night

This is the builder's own named shortfall (M1). It is not a fault alone, because the real room is walked and lives in the game. But the night pictures are not fit for Jafar's page.

**Measured, over the window's glass (the three lights and the toplights):**

| | STREET_SQUARE | STREET_30 | brick beside |
|---|---|---|---|
| **day:** mean luma | 44.0 (p5 40.2, p95 58.0, sd 5.2) | 43.5 | 84.1. The glass is 0.52 of the wall: dimmer, as daylit glass should be |
| **night_lit:** mean luma | 61.2 (p5 61.5, p95 62.5) | 62.4 | 21.8. The glass is 2.8 times the wall, so it reads as a lit shop |
| share of the glass at one flat tone (9 px, sd under 1), day / night | 81 / 91 per cent | 82 / 82 per cent | |
| largest single flat patch in a light, day / night | 73 / 93 per cent | 73 / 92 per cent | |

- No pixel is under 3, and none is at 250 or above.
- The target's composite floors (day 33 or more, night_lit 45 or more) are met. But they are met by a flat card.
- At night every pane is one grey: the "white board" of the 3 October failure.

**WHOSE:** the builder (the gate). Owed on the PC (PC-01).

**EXACT FIX:**
1. Before any Mickey's picture goes to his page, render the gate with the walked room behind the new front: shop-room.py's mickeys branch (`room_3d`, the spec's lamps), its front plane at the card's plane.
2. Re-render the four street frames.
3. Day is lit by daylight only, with the tubes off (`lit_at_start` false). night_lit is the after-the-key state.
4. Until then, label the frames on any page "stand-in glass; the room is the walked one". Better, keep them off his page.

### N2. Under the card, the shop door's lower glass shows a black band at night and a floor edge by day

**Where:** STREET_SQUARE, the door's glass below z 640: x 1691 to 1880, y 919 to 1023 (1600: x 1057 to 1175, y 574 to 639).
- **Night:** luma 7.7; 97 per cent of it under 12 and 11 per cent under 3.
- **Day:** a grey-blue zone, (58, 61, 66), under a hard horizontal edge.
- **Cause:** the M1 door is glazed from z 198, but the card stops at 550 above the footway (its floor is "the window bed carried back, which the stallriser hides"). Nothing hides it at a glazed door.
- **What it is:** the gate's, and the game's far fallback would show the same hole. The near game has the walked room.

**WHOSE:** the target (section 3 assumes a stallriser in front of every card) and the gate.

**EXACT FIX:**
- In the gate: a backing plane at the card's depth, over the door's width (u 3797 to 4609), from the footway to the card's bottom edge, in the room's trodden brown carpet (sRGB about 86, 68, 55).
- On the PC: one row (the far fallback shows no gap below the card at a door glazed lower than 550).

### N3. The door's sign contradicts the state it is shown in

- **night_lit** reads CLOSED (x 1750 to 1820, y 700 to 740). But night_lit is the after-the-key state: "open to 3 am" (table 5.1).
- **day** reads OPEN. But the office is locked since Mickey died, until Tom's key (`lit_at_start` false; shop-interiors.json's note).
- NOTES lists "the sign logic" among the try 2 shared fixes not yet applied here.

**WHOSE:** the builder.

**EXACT FIX:**
- Drive the sign by the key: CLOSED in every state before the key; after it, OPEN from 7.00 to 3.00 and CLOSED from 3.00 to 7.00 (hook-cast's hours).
- The gate's night_lit frame shows OPEN.
- The day frame shows the state the picture claims, named in its caption.

### N4. MICKEY'S stands at the right-hand end of the board; three metres of it are blank, against the Hook sheet's centred name

**Where:**
- STREET_SQUARE: the board's blank part is x 888 to 1574 and the letters are x 1574 to 2066, both at y 268 to 395 (1600: blank x 555 to 984; letters x 984 to 1291, y 188 to 238).

**Why:**
- 4.1's layout `name_only_offset` put the new name over the door, beside a ghost of the older, centred name.
- 4.1's A7 then dropped the ghost and the pin holes, because "the Hook sheet shows gilt capitals on a clean slate-blue board".
- So the reason for the offset is gone. The Hook sheet's name is centred, and so was the 8 October front's.
- The letters themselves are right: FAS-04 is within 12 mm, and they read by day and by night (below).

**WHOSE:** the target (4.1).

**EXACT FIX:** a look line on his page; recommended: centre the name on the board.
- The ink's centre goes to board x 2705: u 3000, street x 6.000.
- The letters then run u 1944 to 4057, at the same size, baseline and stand-off.
- Re-run FAS-04 against the new place.

### N5. The street number stands on the shop door's fanlight, not 4.1's side-door fanlight, and the change is not named

**Where:**
- Built: u 4159 to 4250, z 2163 to 2354; STREET_SQUARE x 1786 to 1807, y 520 to 565.
- 4.1's place: the side door's fanlight, street x 3.82 (u 5180).

**What it is:** either place reads. But a change to 4.1's place must be a named judgement, and F1's fix may want the shop door's fanlight for "MINICABS", as the walked room had it.

**WHOSE:** the builder.

**EXACT FIX:**
- Move the "1" to the side door's fanlight: centre u 5180, the same z, on that pane's inside face (d 80).
- Or name the judgement in NOTES and amend 4.1's place.

### N6. Four check rows say less than they claim

**GLS-02** counts the "1" only. See F1 for the fix.

**TRD-01** is absent from Mickey's check, although A14 says it applies to every shop. See F1.

**FRN-05** does not check printed parts.
- The stallriser's cream, blue and black are not in its "paints used".
- Fix: add the 3.2 tile colours, ±12 per channel, measured on the baked print, and F2's pitch row.

**FAS-01n** reports the normal map's blue mean as "256.0".
- That cannot be an 8-bit value: the file reads (127.5, 127.5, 255.0), sd about 1.
- It is a real but flat map, so the pass stands.
- Fix: round before printing, and report the map's sd. A flat map carries none of 4.1's relief, which does not read at 8.76 m anyway.

## The builder's named shortfalls, judged at street distance

| builder's shortfall | my judgement |
|---|---|
| Only the front; the glass shows a flat card | **narrow (N1)**. It is known and honest, but the night frames are not for his page until the walked room is rendered behind the front |
| The door shut; the night lit from the card only | **narrow (N3)** for the sign. The game's night and the key's state are owed (PC) |
| The gilt letters are plain gilt, with no gilding wear | **not a point from the street.** They read clean, as the Hook sheet's do |
| The tile pattern is the 4.1 print | **FAULT (F2)**, but not because it is the print. It is laid at twice its size, stretched, with no half course |
| The room's rows are n/a | **right**, except TRD-01, which should run for a front (N6) |

## The export faults found in Rita's shop, checked here

| Rita's fault | Mickey's |
|---|---|
| Height map exported as a normal map | **No.** The one normal map is a real RGB map (GLB-01, FAS-01n; my read: 127.5, 127.5, 255). The board shows no streaks at either camera |
| A textured primitive without UVs | **No.** FAS-03 passes, and Mickey's has no hanging sign |
| Two parts sharing one face plane, giving black strips | **None seen.** My scan of the front by day (glass and fanlights out) found 928 pixels under luma 8 at STREET_SQUARE and 653 at STREET_30, all in lines 2 to 5 px tall: the shade under the cornice, the transom and the side door's head. The largest patch is 12 x 12 px in the side door's top-right rebate, x 2098 to 2110, y 600 to 612, a natural shadow at 6x. No strip beside the side door (try 2's narrow point 1) |
| A see-through slot from an angle | **None at STREET_30.** Brick shows beside both pilasters (the gate's piers; FRN-07 and FRN-08). The game's facade must still close the bay's outer 30 mm (PC-04) |
| The stand-in night light or glass visible | **The spill is not seen.** Nothing in the glass is at 250 or above, and no frame member glows. The pool on the pavement is the stand-in's. The stand-in card is seen (N1, N2) |

## What is right

**The front reads as a 3.2 front of a Victorian parade, refitted:**
- clad slate pilasters in three sheets;
- scroll consoles;
- the cornice;
- a 550 board;
- the M1 steel window, three lights with three aligned toplights and the mullions carried up;
- the 80 mm transom band;
- the band over both doors (three toplights over the shop door, a fielded panel over the side door, the head);
- the sill, and the tiled stallriser on a black skirting.

**The proportions and colours sit beside the Hook sheet's Mickey's:**
- slate (62, 75, 87) and gilt;
- an oxblood side door (93, 46, 49) against red brick.

**MICKEY'S reads by day and by night.**
- My measure at STREET_SQUARE: gilt 118.5 against a board ground of 74.6 by day (1.59), and 30.9 against 14.8 at night (2.09).
- STREET_30: 1.31 by day and 1.87 at night.
- The gilt reads lighter than its board at night, unlike Rita's try 2.
- Nothing cuts a letter.

**The doors are handed right, and nothing is mirrored:**
- the shop door hinges on the viewer's left, with the D pull on the right and the chrome letter plate in the bottom rail;
- the side door has its centre knob, a vertical plate on the muntin and the latch on the pier side;
- the bell hangs inside the shop door.

**The side door's fanlight** shows the dark hall: 25.9 by day and 7.2 at night. Its walls and ceiling read at 4x, and no card is seen (FRN-09).

**Content:**
- The only legible words in the four frames at full size are MICKEY'S, 1, OPEN and CLOSED. All are acceptable.
- No drink, betting, child or person.
- No maker's name, barcode or post-1992 thing.

## The check rows: which I trust

**Trusted (15):**
- GLB-01, FAS-01n (the pass; its printout is in N6), FAS-03, FAS-04;
- FRN-01 to FRN-04, FRN-07, FRN-08, FRN-09, FRN-10 (my scan agrees);
- GLS-01, NEV-01, CAM-01.

**Pass but do not prove what they say (4):**
- FAS-01: the maps are on the board, but it does not say the board reads; I measured that myself.
- FRN-05: the printed stallriser is outside it (F2, N6).
- GLS-02: one row of the target's three (F1).
- NEV-02: it is the builder's statement, with no measure. I agree with it from the frames.

**The cloud's stand-ins only:** every glass and night number above, including the target's composite floors, is measured on the gate's flat card and its stand-in spill (N1).

**Missing:** TRD-01 (N6). The four n/a rows (FRN-06, FAS-02, FAS-01c, PRV-01) are rightly n/a. X-PRV passes.

## What I cannot judge from these files

**What the street really sees through the glass:** the walked room by daylight, and lit after the key. That is owed on the PC.

**The game's glass:** the street and the sky in it, the dirt, the night hand-over, Lumen, the exposure and TSR.

**Whether the walked room still carries its own glass words** (shop-room.py's `glass_number`, `glass_word` and `fanlight_word`) behind the new glass in the game. If it does, they would show on a second plane.

**Whether the new front's doors meet the walked room.**
- The room's street door (doormat at room x 0.95 to 1.78) and its stair wall (x 1.81, the viewer's right positive) do not obviously line up with the new shop door (bay-centred 0.70 to 1.71) and side door (1.71 to 2.65).
- If the room's x origin is the bay's centre, they are 70 to 100 mm apart.
- This is for the close view and the PC walk.

**Wear on the front:** it is spotless here, and the game's M_LedgerSurface dust band is owed. Also the sign's night lighting, which the hours put open to 3 am.

**Next:**
1. Settle F1's words on his page.
2. Fix F2 and N2 to N6.
3. Render the four street frames with the walked room behind the glass (N1).
4. Send it to try 2 of the street view.
