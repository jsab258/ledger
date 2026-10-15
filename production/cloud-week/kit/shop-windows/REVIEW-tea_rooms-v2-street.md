PASS

# The tea rooms (west_north bay 2, no. 14), the STREET view: fresh review, try 2 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

Reviewer: a fresh reviewer who did not write the target, build the shop or review try 1. I judged the street view only (STREET_SQUARE and STREET_30, day and night_lit, and the new STREET_SQUARE night_dark). I read the try 1 street review and not either close review. Jafar's ruling of 9 October applies: a piece failing only on narrow points passes, with the points listed for the builder. This is try 2 of this view.

**Read:** CLAUDE.md; RULINGS.md (the parts the brief names); REVIEW-tea_rooms-v1-street.md, item by item; NOTES.md "Try 2 shared fixes" and "Try 2, tea rooms"; TARGET.md 5.7 (hours: open to 22:00, so night_lit is its real night; night_dark is after closing); `checks/check_tea_rooms_v2.json` (made 15 Oct 06:07, 71 of 74 rows pass, 6 n/a).

**Looked at:** the v2 previews `tea_rooms-street-square-{day,night-lit,night-dark}-2026-10-14-v2.jpg`, which match the gate frames (mean difference 1.9, 1.1 and 1.35 levels after resizing). Also the gate frames of 15 October, 05:15 to 06:12 (STREET_SQUARE day, night_lit and night_dark; STREET_30 day and night_lit), at 2560 x 1440, whole and in crops at 2x to 8x.

**Measured:** luma is Rec.709 on the sRGB values, 0 to 255. The glass mask is the check's own `check_<cam>_day_mask.png`, scaled to 2560 by nearest and eroded 3 px. On it I measured the glass, the brick, the curtains, the house number, the fascia, flat patches (9 x 9 windows with a standard deviation under 1), dark patches and burnt pixels. I compared the glass with the no-reflection renders where they exist. Pixel boxes are in the 2560 x 1440 frame.

**Verdict: no fault; five narrow points, each with an exact fix.** The try 1 fault (the doll's tea table) is fixed. A café table and two full-size chairs now stand under the china, and the table's top is above the door's lever. Four of the seven try 1 narrow points are fixed; two are partly fixed and stay narrow; one was the check's and is fixed. One new narrow point comes from the changed doorway: a black slot through the shop door at night. One comes from the night frame: the house number all but vanishes.

## Try 1 items, one by one

| try 1 item | now | where and measured |
|---|---|---|
| **F1** table and chairs at children's sizes | **FIXED** | <ul><li>STREET_SQUARE day, middle light, x 1150 to 1415, y 750 to 925.</li><li>A scripted Formica café table: a pale laminate top with an aluminium edge, a chrome column and a black cross base. The two painted chairs are at full size.</li><li>The top's front rim is at y 762 and the door's lever at y 837. The rim is 75 px above the lever (about 0.33 m at the glass), as the try 1 acceptance asked: 1.34 m against 1.0 m above the footway.</li><li>The teapot is now about a fifth of the table's height.</li><li>DSP-06 reads the top at 0.740 m and the chairs at 0.96 m.</li><li>At STREET_30 both chairs read as spindle-back chairs facing the table (DSP-08: 6 degrees off). At STREET_SQUARE they are seen side-on, their backs behind the curtains, and only the finials show above the rod. That is right for a café window.</li></ul> |
| **N1** CLOSED at night while open | **FIXED** | <ul><li>STREET_SQUARE and STREET_30 night_lit: OPEN on the door's upper pane. The camera files say `door_sign: OPEN`.</li><li>night_dark shows the red CLOSED card (SIGN-01).</li><li>At night the OPEN card is unlit: dull orange letters on near-black, still legible. That is right for a hanging card.</li></ul> |
| **N2** hours card missing | **FIXED** | <ul><li>STREET_SQUARE day, the door's lower pane, x 740 to 812, y 748 to 792: 4.1's card, "MON-SAT 6.30 AM - 10 PM / SUN 8 AM - 12 NOON", in marker pen.</li><li>It can just be read at 3x; at street distance it reads as a taped white card, as wanted.</li><li>Present at both cameras, day and night.</li></ul> |
| **N3** curtains corrugated by day, opaque grey band at night | **PARTLY** | <ul><li>**By day: fixed.** Scalloped tab heads over a brass rod, folds of unequal pitch and depth, a hem. The left curtain's column profile has no dominant period (the strongest takes 22 per cent of the power). Curtain 158 against a room of 60 above it (left) and 155 against 115 (right).</li><li>**At night: not fixed, and changed in kind.** See narrow point 1.</li></ul> |
| **N4** flat brown dado behind the table | **PARTLY** | <ul><li>The largest flat patch at STREET_SQUARE is 2.59 per cent of the glass by day (x 1290 to 1390, y 727 to 831, luma 28) and 2.74 at night (try 1: 3.98 and 3.65).</li><li>At STREET_30 it is 5.84 by day (the right wall's plaster, x 1387 to 1529, y 552 to 678, luma 76) and **5.86 at night (x 1195 to 1357, y 698 to 847, luma 46.7: the same dado behind the table as in try 1)** (try 1: 5.48 and 5.49).</li><li>The matchboard and rail exist (the rail shows at y 727 at STREET_SQUARE). But the 3 mm V-joints at 0.6 of a dark brown are under one pixel at 8.76 m and are lost to the card and the denoiser. The lower dado still reads as a smooth brown field.</li><li>The builder's claim that "the matchboard dado is no longer among the patches" holds by day at STREET_SQUARE. It does not hold at STREET_30 night. Narrow point 4.</li></ul> |
| **N5** price tickets at the chairs' feet | **FIXED** | <ul><li>Three tickets by the carrot cake (x 960 to 1080, y 905 to 918) and one before the strawberry cake (x 1490 to 1505).</li><li>The nearest is about 48 px, 0.2 m, from a chair's leg.</li></ul> |
| **N6** a walnut occasional table | **FIXED** | See F1: Formica, chrome and a black cast base. |
| **N7** LIT-08 measured a table's base as goods | **FIXED** | LIT-08 now measures furniture by its top and names the chairs. Its lowest ratio is the window card, 0.68 (limit 0.6). |
| shared (a): the orange bar at STREET_30 night | **FIXED** | <ul><li>Box x 1385 to 1535, y 822 to 858 now reads luma 43.9, RGB (62, 40, 25): the curtain's hem and the floor. There is no bar.</li><li>GLS-03 p95 5.8 (try 1: 16.7). GLS-04 largest patch 3 px.</li></ul> |
| shared (b): night_dark's hot corners | **not in a street frame of the lit state** | The new STREET_SQUARE night_dark frame's toplights are dark brown, under the brick above the fascia. |

## Faults, worst first

None.

## Narrow points, each with its exact fix (most important first)

### 1. At night the café curtains read as dark grey satin, almost sheet metal, not backlit cotton (CUR-01 (d) fails; try 1 N3, partly fixed)

- **Where:**
  - STREET_SQUARE night_lit, left light x 912 to 1135 and right light x 1425 to 1648, y 735 to 845 (1600 preview: y 459 to 528).
  - In the preview this is the brightest-edged thing in the window after the china.
- **Measured** (mine):
  - Curtain mean 57.8 against 96.2 for the room above it in the left light (0.60). Right: 58.4 against 63.8 (0.92). The builder's CUR-01 reads 0.66 and 1.00; the target is 0.8.
  - Each fold carries a hard vertical highlight from the tab down: p95 133 against the mean 58, max 252 (burnt on the tabs).
  - Mean colour (67, 56, 46): a dull brown-grey, not the cloth's cream.
  - It is better than try 1's 50.2 and 50.0. But the sheen of 0.4 has turned the dull board into a glossy pleated sheet, which from the far pavement reads as satin or corrugated tin.
  - At STREET_30 night the same cloth reads as satin. In night_dark, under the warm wash, it reads as cloth, which is right.
- **Why only narrow:**
  - By day the cloth is right. The room, the table and the trade all read at night.
  - The builder named it (CUR-01).
  - The fix is a material change with numbers.
  - It is the first thing to fix before Jafar sees the night picture.
- **WHOSE:** the builder (`script:cafe_curtain`'s material).
- **EXACT FIX:**
  1. Sheen 0.0.
  2. Specular IOR level 0.25.
  3. Roughness 0.9.
  4. Mix a Translucent BSDF at 0.35 into the cotton, colour the cloth's cream (235, 228, 210). Transmission stays 0.
  5. In the game: the two-sided foliage (subsurface) model, the same cream.
- **Acceptance:** at STREET_SQUARE night_lit:
  - each curtain's mean at least 0.8 of the glass above it;
  - each curtain's p95 at most 1.6 times its mean (now 2.3);
  - no curtain pixel at 250;
  - day frames unchanged within 5 levels.

### 2. The house number 14 all but vanishes at night (new in try 2)

- **Where:** STREET_SQUARE night_lit, the shop door's fanlight, figures x 750 to 800, y 530 to 560 (1600: x 470 to 500, y 331 to 350). The 1600 preview's night picture reads it as a faint orange "24".
- **Measured:**
  - The figures read 63.1, RGB (86, 59, 36), against the fanlight's 65.2, RGB (79, 63, 46): a luma ratio of 0.97. They are told apart only by a slight orange cast.
  - Try 1 read dark figures of 26.1 on a lit fanlight of 65.4, a ratio of 0.40.
  - By day it reads well: 201 against 52.
  - The figures' fronts are now lit warm (from the stand-in spill or the gate's light linking; I could not trace which) as bright as the hall behind them.
- **WHOSE:** the builder or the kit's gate lights, whichever lights the figures' faces.
- **EXACT FIX:**
  1. Take the fanlight's numerals off the spill light's channel, as the kit already does for the window card's cups and hooks for the night_dark wash.
  2. Or, if the spill must reach them, give the numerals' backs an opaque black (20, 20, 20) layer 0.5 mm behind the paint, so that the lit hall shows them as a silhouette.
- **Acceptance:** at STREET_SQUARE and STREET_30 night_lit, the figures' mean luma is at most 0.5 of the fanlight's ground. The day frames are unchanged.

### 3. A black slot through the shop door's glass at night (new in try 2, from the doorway's changed floor and hall faces)

- **Where:**
  - STREET_SQUARE night_lit, the shop door's lower pane: a vertical strip x 733 to 741, y 745 to 855, mean luma 5.6, with a core under 3 (755 px). It lies between the brown hall face on the left and the counter-coloured panel on the right.
  - A shorter piece above the glazing bar, x 733 to 741, y 716 to 730 (97 px).
  - STREET_30 night_lit: a 10 x 10 px black square at the right edge of the door's upper pane, x 914 to 924, y 680 to 690, luma 0. It sits at the end of the dado rail.
- **Measured:**
  - The no-reflection render reads the strip at 6.0, so the glass is not causing it: the strip is a black part of the scene.
  - By day the same strip reads 35.6, dark but not black.
  - Try 1's door showed no black pixel. FRN-13 passes because its rays end on the hall face and the card, but a ray grid misses a strip 9 px wide and a face that is simply unlit.
  - Small at street distance (5 px in the preview), but it is the void the brief names, in the most-looked-at door.
- **WHOSE:** the kit (`sw_gate.reveal_specs`, the hall face behind the shop door).
- **EXACT FIX:**
  1. Give the hall face's end, and the return face between it and the card, the dado's material: (120, 74, 44) below z 1.10 and the room picture's wall column above.
  2. Or carry the hall face 50 mm further into the shop, so that its end sits behind the card's edge and cannot be seen past the door's lever stile.
  3. FRN-13 gains a luma test: in each review camera's night_lit frame, no pixel seen through the shop door's glass under luma 12. Now 852 px at STREET_SQUARE; the test wants 0.

### 4. The dado behind the table and the right wall's plaster are still flat fields at STREET_30 (FLT-02 fails; try 1 N4, partly fixed)

- **Where:**
  - STREET_30 night_lit x 1195 to 1357, y 698 to 847 (5.86 per cent of the glass, luma 46.7: the dado).
  - STREET_30 day x 1387 to 1529, y 552 to 678 (5.84 per cent, luma 75.8: the right wall's plaster).
  - STREET_SQUARE 2.59 and 2.74 per cent.
- **Why only narrow:**
  - Neither is a void or a white board: they are honestly lit paint and plaster that read as a wall.
  - The builder named it.
  - It is half what try 1 was at STREET_SQUARE.
- **WHOSE:** the builder (the room picture).
- **EXACT FIX** (the try 1 acceptance stands, at most 2.5 per cent at both cameras, day and night):
  1. Draw the matchboard joints at a width the street camera keeps: 6 mm V-joints at 0.5 of the paint's value. That is about 1.5 px at STREET_30.
  2. Add a per-board tone of plus or minus 6 per cent (seeded), so the boards read even when the joints blur.
  3. Raise the plaster map's grain on the walls from 0.3 to 0.6, with a 400 mm mottling of plus or minus 4 per cent.
  4. Re-render the room and the four street frames.

### 5. FLT-01 counts the window card's plain white paper as a flat field (FLT-01 fails)

- **Where:** STREET_SQUARE day, x 1476 to 1604, y 637 to 714, luma 191 (2.16 per cent of the glass); STREET_30 1.41 per cent.
- **What it is:**
  - A plain white card at 8.76 m is uniform in a real photograph too. Its lettering, its two cups and its 1.5 mm bow read.
  - It does not look like the "white board" void: it is a sign that carries words.
- **WHOSE:** the check.
- **EXACT FIX:** FLT-01 leaves out printed cards and signs whose lettering covers at least 8 per cent of their face. It counts the card's paper at FLT-02's 2.5 per cent limit instead, and names the piece in the row. No rebuild.

## What is right

**The front** (unchanged from try 1, and still right):
- the fluted brown pilasters on plinths with capital blocks;
- the leaf-carved consoles;
- the cornice;
- the brown acrylic panel in a white frame over the old flaking board;
- the rendered stallriser and sill;
- a 3L-6T window with the mullions carried up;
- the band over both doors.

It reads as a 1980s caff in a Victorian parade, beside Rita's approved front. Nothing floats, nothing is mirrored, and no text reads backwards. At STREET_30 both ends show brick (no see-through slot). No two parts share a face plane: the only dark lines on the front are the shade lines under the cornice's end blocks.

**Lettering:**

| what | value |
|---|---|
| fascia by day: ground (p40) / letters (p95) / ratio | 68.8 / 184.8 / 2.69 |
| fascia at night_lit: ground / letters / ratio | 17.4 / 58.2 / 3.35 |
| fascia at night_dark: ratio | 3.37 |

- No bar crosses a letter.
- The window card, the chalk menu (TODAY'S MENU / TEA 25p / COFFEE 35p / TOAST 30p) and TEAS FROM 25p read at 100 per cent.

**The glass and the room:**

| measure | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, glass mean | 84.8 (p5 28, p95 176) | 83.3 (p5 27, p95 181) |
| day, brick beside | 84.0 / 84.4 | 84.0 / 87.7 |
| day, under 3 | 0 | 0 |
| night_lit, glass mean | 76.6 (p5 34, p95 149) | 70.7 (p5 35, p95 128) |
| night_lit, brick beside | 16.4 / 18.6 | 16.9 / 21.0 |
| night_lit, window against wall | 4.4 times | 3.7 times |
| night_lit, under 12 | 0.17% | 0.48% |
| night_lit, largest dark patch | 0.07% | 0.23% |
| burnt pixels (night) | 1,101: 0.03 per cent of the frame (the teapot's lid, a cup, a chair's seat edge, curtain tabs). PIC-05g passes | |

- **By day:** the room above the curtains reads 60 (left), 59 (middle) and 115 (right, the white card and the hatch) against the brick's 84. The room reads dimmer than the wall where it should, readable throughout.
- **At night_lit:** the room is lit at about four times the wall. There is no void and no white board.
- **The new night_dark:** an honestly dark, shut café, glass 20.5 against the brick's 16.2.
  - The curtains glow warm in the sodium wash.
  - The urn's pilot lamp shows.
  - The cups, menu, card, table and cakes can be made out.
  - Its dark back (12 per cent of the glass under 12, in the middle light) is the unlit room after hours, not a hole. The shop is shut at that hour (22:00), so this is the honest state.

**The trade reads from the street:**
- the fascia and the window card;
- a café table laid for two, now at real size;
- cakes at both ends of the bed with their tickets;
- behind them a counter with cups on two shelves, a kettle, a mechanical till, a tea urn, the chalk menu, the hatch and, through the door, glass cake domes. The models' glass is now kept and reads as glass.

**Period and content:**
- 1990 prices; a mechanical till, an urn, T12 battens and a chequer floor.
- No barcode, screen or modern packaging.
- No drink, betting, children's things or person.
- The two framed pictures are landscape photographs with no person.

**Every word legible at 100 per cent in the five frames** is the project's own and acceptable:
- BREAKFASTS, LUNCHES & TEAS and Tea Rooms;
- 14;
- OPEN (day and night_lit) and CLOSED (night_dark);
- BREAKFASTS / LUNCHES / TEAS;
- TODAY'S MENU / TEA 25p / COFFEE 35p / TOAST 30p;
- TEAS FROM 25p;
- the hours card, at 3x only.

The price tickets, the table's menu card, the cork board's notices and the till's keys cannot be read from the street. No maker's name or mark is visible anywhere.

**Rita's export faults, none repeated:**
- **Height map as normal map:** none. FAS-01n reads mean (128, 128, 256), blue 200 or more on 100 per cent.
- **Textured primitive without UVs:** none (GLB-01).
- **Coplanar black strips on the front:** none.
- **See-through slot at STREET_30:** none at the window's ends. The door's black slot (narrow point 3) is inside the doorway, not between front parts.
- **Stand-in night light or glass visible:** none on the front. The head band reads 0 at 250, and the mullions read 56 against the glass's 65. The door's lower pane by day shows a grey band (x 705 to 790, y 842 to 856, RGB (45, 43, 43) against (22, 11, 5) without reflection). That is the stand-in glass reflecting the pavement, which real glass does: not a point.

**The new pieces:**
- **The sheets' lean:** the window card hangs flat on its cups; the table's menu card stands square.
- **The lamp-pool setting:** no bar.
- **The night sign:** OPEN.
- **Furniture sizes:** right.

None of them adds a fault seen from the street.

## The builder's named shortfalls, judged from the street

| shortfall | judgement |
|---|---|
| FLT-01 (the window card's flat paper) | narrow, the check's (point 5) |
| FLT-02 (2.59 and 5.84 per cent) | narrow, the builder's (point 4) |
| CUR-01 (d) (the left curtain 0.66 at night) | narrow, the builder's, the most important (point 1); my own reading 0.60 |
| no seating in the room (close 11, a Judgement for the target's owner) | not a point from the street: the window's table and the counter say café |
| the window card's and the night_dark frames' changes | not a point: the night_dark card reads as a card, not a hot panel |
| Fabric034's normal map not used | not a point |

## The check rows: which I trust

- **Trusted, and matching my own numbers:**
  - GLS-03 and GLS-04 (no bar seen);
  - FAS-01, FAS-01n, FAS-01c and FAS-03 (my fascia ratios agree);
  - FRN-12 (the card is where it says);
  - SIGN-01 (the camera files agree);
  - DSP-06 and DSP-08 (agree with what the frames show);
  - LIT-05 and LIT-07 (my night glass 76.6, mullions under the glass);
  - LIT-02b (my under-3 shares are of the same order);
  - PIC-05g (my burnt count agrees);
  - FLT-02 (my 2.59 and 5.84 equal its numbers) and CUR-01 (my 0.60 and 0.92 against its 0.66 and 1.00, on a slightly different zone; both fail the left curtain);
  - FLT-01 (I did not separate the display's own pieces, but its patch is the white card, which my day frame shows);
  - X-PRV (the previews match the frames).
- **Passes, but does not prove what it says:** FRN-13. Its rays end on faces, but it cannot see an unlit face or a slot narrower than its grid (point 3).
- **The cloud's stand-ins only:**
  - LIT-01, LIT-02 and PRJ-02 (the card composites and the gate's trace);
  - LIT-05, LIT-07 and PIC-05g are measured on gate renders, whose glass, lamps and spill are stand-ins (PC-02);
  - GLS-05 tests the gate's glass, not the game's.
- **Not repeated by me:** INV-01 to INV-08 (I did not re-read every map; nothing legible shows from the street); DSP-03, DSP-05, DSP-07 and DSP-09; SO-01 to SO-07.

## What I could not repeat, and what I cannot judge

- **Not repeatable:**
  - The try 1 frames were overwritten. My try 1 comparisons use the try 1 review's numbers, and the v1 previews of 13 October where a picture was needed.
  - I did not trace the cause of narrow points 2 and 3 in the scene file. Their fixes are written as acceptance numbers so that either route passes.
- **The game's glass:** the street and sky in the panes, dirt and the steam the target asks for ("the steam-warm window").
  - The gate still lights cloth behind clear glass as bright as paint outside: by day the curtains are 155 to 158 against the brick's 84.
  - The try 1 review's suggested PC row stands: by day from STREET_SQUARE, the curtain band reads at most 0.9 of the outside cream paint.
- **The game's light:** Lumen, the spill's real pool on the pavement (the gate's footway reads 125 at night: a stand-in), the exposure and the hand-over between night_lit and night_dark at 22:00.
- **Wear:** the front is spotless. The Hook sheet's grime and wet are owed to the PC (PC-05).
- **Motion:** TSR, the card's parallax as the player walks, and the curtains' sway.
- **The close view's matters:** the models' small glass parts (the till's readout, the clock), the cork board, the suction cups and the china's detail.

**Next for the builder:**
1. Point 1 (the curtain's material).
2. Points 2 and 3 (the night house number; the door's black slot, the kit's).
3. Point 4 (the room's grain).
4. Point 5 (FLT-01 wording).
5. Re-render the street frames and the close frames, and re-run CUR-01, FLT-01, FLT-02 and FRN-13.
