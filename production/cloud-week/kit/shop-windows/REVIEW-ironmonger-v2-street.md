PASS

# The ironmonger (west_north bay 1, no. 16), the STREET view: fresh review, try 2 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. I judged the street view only (STREET_SQUARE and STREET_30, eye 1.6 m above the footway, 8.76 m from the glass). I did not read either close review. Jafar's ruling of 9 October applies: a piece that fails only on narrow points (each a small detail with an exact fix) passes, with those points listed for the builder. This is try 2 of the street view.

**What I read:**
- CLAUDE.md; RULINGS.md (1, 2, 3 and 8 October).
- My try 1 review, `REVIEW-ironmonger-v1-street.md`, first; then NOTES.md ("For the next nine shops", the ironmonger's batch A section, "Try 2 shared fixes", "Try 2, ironmonger").
- TARGET.md section 3, 5.8 and 13 (rows A1 to A6, T2-1 to T2-6, T2-15, T2-16).
- Rita's four reviews.
- `checks/check_ironmonger_v2.json` (made 22:51 on 14 October: 73 of 74 rows pass, FLT-01 fails, 6 n/a).
- The parts of `sw_front.py` (`make_hanging_board`), `sw_gate.py` (the night lights, `street_glossy`, the return walls) and `check_try2.py` (LIT-02b, FAS-01c) that make or test what I saw.

**What I looked at:**
- The v2 previews of 14 October: street square day, night_dark and night_lit, and the room day. I set them beside the 13 October v1 files.
- The new gate frames (21:32 to 22:18 on 14 October) at 2560 x 1440, whole and in crops up to 10 times: STREET_SQUARE day, night_lit and night_dark, and STREET_30 day and night_lit.
- The gate's check renders: the glass masks, the reflection-off renders and the cards.
- The Hook sheet, and Rita's approved street front (`ritas-street-square-day-v3`).

**What I measured:**
- Rec.709 luma (0 to 255) over the gate's own glass mask (73,486 px at 1280, doubled), the toplight panes, the brick, the front's paint and the pavement.
- The same boxes on the v1 and v2 previews, where the v1 frames no longer exist.
- The 9 x 9 px uniform-patch test and connected dark patches, both inside the glass.
- `ironmonger_front.glb` imported with bpy: part bounds, and a triangle-overlap (BVH) test of every sign part against every front part and against each other.
- Both glbs' normal maps, UVs and transmission materials, read from the files.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview JPEG). "Model frame" is the front glb's own: y negative is out from the wall.

**Verdict: no fault blocks.**
- Of try 1's ten narrow points, eight are fixed and two partly: point 9's NOTES wording, and point 10's check-file sentence.
- The three new narrow points worth fixing first are these:
  - The bracket's scroll now floats under the arm, threaded on the near chain, in the game's own glb.
  - In the real night (night_dark), the bottom of the left light is a pure-black patch of 8.3 per cent of the glass.
  - At night, the lamp-pool setting also took the street's reflection out of the front's paint, so the doors and pilasters read almost black.
- Each has an exact fix. Seven narrow points in all.

## 1. Try 1, item by item

| try 1 point | now | where, and the measure |
|---|---|---|
| 1. The sign's near chain ran through the cornice and the console; the board cut into the capital | **FIXED** (but see new narrow point 1) | **Glb:** the board spans y -0.330 to -0.880 (30 mm clear of the cornice's 0.300, 37 mm of the leaf's 0.293, 155 mm of the capital's 0.175). The chains hang at y -0.39 and -0.82, the arm runs to -0.840, and the near chain is 79 mm clear of the cornice (my nearest-point test). The BVH test finds 0 sign parts touching a front part. **Pictures:** STREET_30 day, the near chain hangs clear right of the cornice and console (x 1880, y 345 to 455); STREET_SQUARE day, it hangs in front of them (x 2200, y 200 to 360). T2-4 records the 0.84 |
| 2. Hot orange corners in the night_dark toplights | **FIXED** | **Toplights:** the six strips read 17.3, 18.6, 21.4, 22.7, 23.6 and 22.6, against the brick above the fascia's 25.5. The first toplight's left end (x 905 to 940, y 425 to 485) reads 7.2 (try 1: 75.1). **Picture:** its top front corner columns read 5.6 and 5.6 against a mean of 18.1. **Left return wall:** it still reads 29.1 (x 905 to 940, y 520 to 700; try 1: 38). That is the wash on the walls' middle band (the picture's side wedges read 27 to 29), not a hot corner: not a point |
| 3. The brooms lay heads down and read as white poles | **FIXED** | **STREET_SQUARE day:** the three red-and-black heads stand up against the right return wall (x 1580 to 1655, y 630 to 650). At STREET_30 they read plainly as push brooms. DSP-03's part rule sees the bristles at 0.55, 0.71 and 0.76 |
| 4. The pyramid's backing board was primer grey | **FIXED** | **STREET_SQUARE day:** the board reads grey-green (RGB 34, 43, 40): luma 40.7 left of the pyramid (x 945 to 1010, y 760 to 850), 47.3 right of it, and 59.8 at its lit lower left. DSP-11's mean is 44.5. The tins' labels now stand out against it |
| 5. The stepped crate was one flat box | **FIXED** | **STREET_SQUARE day:** the front face (x 1335 to 1500, y 860 to 900) reads luma 120.7 with an sd of 16.6. No 9 px uniform pixel is left on it. The planks' grain and the HARTSIDE stencil read. The display's largest uniform patch is 0.91 per cent (the board) |
| 6. A paint flake on the S of TOOLS | **FIXED** | **Both cameras at 100 to 500 per cent:** the S is clean, with no patch where the flake was. The nearest flake (x 978, y 305) is about 46 mm from any letter |
| 7. The sledgehammer's yellow shaft read modern | **FIXED** | **STREET_SQUARE day:** an ash shaft against the right return wall (x 1635 to 1655, y 700 to 915); no yellow left on it. The only yellow now is the sprinkler's sled (x 1525 to 1595, y 882 to 915), a plausible 1980s plastic sprinkler |
| 8. The night_lit preview is not this shop's night | **FIXED** in the notes | NOTES names night_dark as the picture to show and night_lit as the tests' state. No page has been made yet, so the caption is still owed when one is |
| 9. Three rule changes (FRN-10, LIT-02b, LIT-08) | **FIXED** in the check; **PARTLY** in the words | **FRN-10:** passes with 0 dark patches of 35 mm or more. **LIT-08:** n/a. **LIT-02b:** the code (`check_try2.py` lines 874 to 892) drops a dark patch over a picture of luma 40 or more, which is my rule. But NOTES says the opposite twice ("counts a dark patch only where the card's picture under it averages luma 40 or more"): narrow point 7 |
| 10. NOTES' check section out of date; FAS-01c's sentence the wrong way round | **PARTLY** | **NOTES:** the batch A section is marked superseded. **FAS-01c:** the code's sentence was corrected at 01:23 on 15 October. But `check_ironmonger_v2.json` (22:51 on 14 October) still says "The stallriser's luma 55.6 ... (225 per cent of the ground's)", which NOTES says is fixed: narrow point 7 |

The builder states no "a review was wrong" for this view. The one question it hands me (FLT-01's counter panel) is narrow point 6. I could not repeat try 1's measures on the 13 October frames: they are overwritten. Where I compare v1 with v2, I used the two preview JPEGs at the same 1600 boxes.

## Faults, worst first

None.

## Narrow points, each with its exact fix (most visible first)

### 1. New: the bracket's scroll floats under the arm, threaded on the near chain (the game's glb)

- **Where:**
  - STREET_SQUARE day, x 2196 to 2212, y 186 to 206 (1600: x 1373 to 1382, y 116 to 129).
  - STREET_30 day, x 1877 to 1893, y 332 to 346.
  - In both it is a black "C" hanging in the air 43 mm under the arm, with the near chain running through it. It is plain at 100 per cent and reads as a stray hook. From the pavement under the sign it will plainly look wrong.
- **Measured on `ironmonger_front.glb` (model frame):**
  - `sign_scroll_0` spans y -0.347 to -0.461 and z 3.636 to 3.697. `sign_arm`'s underside is at z 3.740.
  - `sign_brace` now ends at y -0.206, 141 mm short of the scroll.
  - The near chain hangs at y -0.379 to -0.401: links 00, 01 and 03 intersect the scroll (BVH: 24, 24 and 22 triangle pairs). The scroll touches nothing else.
- **Cause:**
  - In `sw_front.make_hanging_board` (line 846), the scroll is placed at d = 300 x k_ (k_ = 1.27, my try 1 fix's "scale the scroll by 1.27"). The brace is shortened by its own factor kb until it passes under the first ring (lines 834 to 843). I replayed the loop: kb = 0.396, and the brace ends at d 204.
  - The same code with k_ = 1 (try 1) puts the scroll at d 245 to 355, just under the brace. Now the brace has left it, and the scroll stands on the chain's line.
  - The comment at line 833 says the ironmonger's brace "is unchanged". It was shortened from d 420 (the same code at k_ = 1) to d 204.
  - FRN-11 tests sign parts against the other front parts only, not against each other, so it passes.
- **WHOSE:** the kit (`make_hanging_board`), and my try 1 fix's wording.
- **EXACT FIX:**
  1. In `make_hanging_board`, build the scroll's points with `kb` in place of `k_` (keep `foot + 50.0`). Its centre is then d 119, and it spans d 90 to 184 under the brace.
  2. The scroll's top then comes within about 1 mm of the brace's underside: a contact, inside FRN-11's 2 mm. Its outer edge stays 195 mm clear of the near chain (whose near side is d 379).
  3. Correct the line 833 comment: the ironmonger's brace is shortened to d 204.
  4. Extend FRN-11 to test the sign's parts against each other (each mesh inset 1 mm), allowing only these designed joints: ring on arm, link on link, chain in ring, chain in eye, eye in board, bolt in plate, brace on plate and arm, scroll on brace.
  5. Add to FRN-11: every sign part lies within 2 mm of another sign part or the plate (nothing floats).
  6. Re-export the front, and re-render the two street day frames.

### 2. New: at night_dark the bottom of the left light is a pure-black patch, darker than the room behind it

- **Where:** STREET_SQUARE night_dark, x 906 to 1268, y 753 to 920 (1600: x 566 to 793, y 470 to 575).
  - One connected patch under luma 3 covers 8.3 per cent of the glass. The 9 px uniform test finds 8.7 per cent at luma 2.0.
  - The backing board reads 1.3 and the pyramid 6.3.
- **Measured:**
  - **The display band (y 760 to 915):** 5.0 in the left light and 7.6 in the right. The room above it (y 530 to 740) reads 15.1 and 17.7. By day the band is the brighter (63.2 against 47.1).
  - **Over the whole glass:** under luma 3 is now 17.5 per cent (try 1: 12.6).
  - **The previews:** the left light's glass reads 11.1 (v1: 12.0).
- **Cause:**
  - The room picture's night_dark is lit by the kit's sodium wash "through the front". The display, a metre nearer the street, gets no part of it. In the gate it is lit only by the two stand-in lamps 10 m along the street, which the pilasters and the sill shade.
  - My try 1 fix 4 (the board in dark green) and shared fix a (the night glass reflects a black street) took away the last grey in that corner.
- **WHOSE:** the kit (the gate's night_dark lights). The game's own lamps are owed (PC-02).
- **EXACT FIX:**
  1. In `sw_gate`, for night_dark only, add one area light that matches the room rig's wash:
     - sodium, linear (1.0, 0.25, 0.0), 4.3 x 0.5 m;
     - centred on the window, 0.02 m outside the glass at z 2.09 (0.6 of the card's height above its foot), tipped 30 degrees below the horizontal into the window;
     - invisible to the camera, glossy and transmission rays;
     - on the display's light channel (`spill_receivers`) only.
  2. Set its strength so the display band's mean at STREET_SQUARE night_dark is 0.8 to 1.0 times the room's band above it (today's room: 15 to 18).
  3. Add to LIT-01c: at STREET_SQUARE night_dark, no connected glass patch under luma 3 covers more than 1 per cent of the glass, and the display band reads at least 0.6 of the room above it.
  4. Re-render the two night_dark frames.

### 3. New: the lamp-pool setting also darkened the front's paint at night (the code's "nothing else changes" is not so)

- **Where:**
  - STREET_SQUARE night_dark, gate frame: the side door (x 1945 to 2090, y 630 to 1030) reads 2.2, the pilaster shafts (x 822 to 875 and 2145 to 2195, y 500 to 880) 4.2 and 4.1, and the stallriser 1.7. The brick beside reads 17.7.
  - The same 1600 boxes on the two previews:

    | part | v1 | v2 |
    |---|---|---|
    | side door | 7.9 | 2.1 |
    | pilasters | 11.8 and 10.8 | 4.2 and 4.3 |
    | shop door's lower panel | 4.0 | 1.9 |

  - The black side door all but vanishes; the lower half of the front is one dark mass. The brick, fascia and glass are unchanged (brick 18.5 to 17.9, fascia 37.7 to 36.4).
- **Cause:** shared fix a (`sw_gate.py` lines 585 to 595) sets `visible_glossy = False` on the road and the far footway for every shop but Rita's. That takes the lit street out of the paint's reflection as well as the glass's. The code's comment (line 584) says "the glass reflects the dark street there and nothing else changes".
- **What it is:** a stand-in either way. In the game, the wet street and its lamp pools will show in the gloss paint (Lumen, PC-02); the 3 October bar is "the wet street dark, glistening, mirroring". It matters only for the night picture on his page.
- **WHOSE:** the kit (the gate, and its comment).
- **EXACT FIX:**
  1. Replace "nothing else changes" in `sw_gate.py` (line 584) with, and add to NOTES step 0 a: "the front's paint loses the street's reflection too: at STREET_SQUARE night_dark the pilasters read 4.2 (were 11.8) and the side door 2.2 (7.9)".
  2. Caption the night picture on his page: "the front's night reflections are the gate's stand-in; the game's wet street is owed (PC-02)".
  3. Add a row owed on the PC (the next free number, PC-12): at night in the packaged game, from STREET_SQUARE, the pilaster faces read at least 0.4 of the brick beside them. By day it is 0.58; the gate's v1 read 0.64 and v2 0.23.

### 4. New: the six gloves read as dark cuffs, like shoes, from the far pavement

- **Where:** STREET_SQUARE day, the hung shelf, x 955 to 1115, y 712 to 745 (1600: x 597 to 697, y 445 to 466); STREET_30 day, x 985 to 1126, y 715 to 747.
- **What it looks like:** each glove lies with its cuff opening toward the street. What reads is six black openings rimmed in green, in three stacks: shoes or galoshes more than gloves. The trade does not suffer (tins, cans, tools and brooms carry it), but the shelf says nothing.
- **WHOSE:** the builder (the try 2 layout, "three same-turn stacks").
- **EXACT FIX:**
  1. Turn each stack 180 degrees about the vertical, so the fingers point at the glass and the cuffs into the shop. The u, v and w extents stay as now (the stacks' footprints are symmetric).
  2. Check from STREET_SQUARE: no cuff opening's normal points within 60 degrees of the eye.
  3. The close reviewer confirms the arrangement.

### 5. New: the crate's rear stencil shows only "O_S", which reads "ONS"

- **Where:** STREET_SQUARE day, x 1430 to 1462, y 815 to 840. The rear step's "PAINTS & OILS" is hidden but for O and S, and the blowtorch's lever crosses the I and L. At 100 per cent it reads as a word "ONS".
- **WHOSE:** the builder.
- **EXACT FIX:** drop the rear step's stencil (plain planks, as the rest of the crate). Keep HARTSIDE on the front step, which reads whole above the cans.

### 6. FLT-01's one failure is the room's counter panel, not a flat display piece: change the rule

- **Where:** STREET_30 day, x 1139 to 1184, y 735 to 822, luma 40.8. My test gives 1.98 per cent of the glass; the row gives 2.06 on a slightly smaller glass count.
- **What it is:** the end panel of the room's counter in shade. It has its frame and fielded edge in the room picture, and at 8.76 m it reads as varnished joinery.
  - In try 1 the same camera's largest patch was the return wall's plaster, 2.6 per cent, and I did not call it a fault.
  - The display's own largest patch is 0.67 per cent (STREET_30) and 0.91 per cent (STREET_SQUARE, the backing board, luma 33), both under the 1 per cent.
- **WHOSE:** the check: my try 1 acceptance line was worded over the whole glass, when it was meant for the display.
- **EXACT FIX:**
  1. FLT-01 counts only the display's own pieces (the object-index mask), with a limit of 1 per cent of the glass.
  2. The room picture's flat tone stays with PIC-06 and the eye.
  3. For the record, give the counter's three front panels the room's own CC0 wood map at 1k, the next time the room is drawn for another reason. Not on its own.

### 7. The records: three sentences the wrong way round or out of date

1. **LIT-02b in NOTES.** Two places ("Try 2 shared fixes", the paragraph after the table; and the street 9 row) say a dark patch counts "only where the card's picture under it averages luma 40 or more". The check does the opposite, as asked: patches over a picture of 40 or more are paint in shade and are not counted.
   **Fix:** "counts a dark patch only where the card's picture under it averages under luma 40".
2. **FAS-01c in `check_ironmonger_v2.json`.** It still says "(225 per cent of the ground's)", because the code's corrected sentence came at 01:23 on 15 October, after the check ran.
   **Fix:** re-run the check's FAS-01c (no render needed) so the file says "the ground is 225 per cent of the stallriser's", or say in NOTES that the v2 file predates the wording fix.
3. **The comments on narrow points 1 and 3** (`sw_front.py` line 833, `sw_gate.py` line 584): correct them as given there.

**WHOSE:** the builder.

## The builder's named shortfalls, judged at street distance

| builder's item | my judgement |
|---|---|
| FLT-01 fails (STREET_30, 2.06 per cent, the counter panel) | **Narrow, and only the rule's** (point 6). Not a fault |
| PIC-05g and DSP-11 pass narrowly (board 44.5 against 45) | **Not a point.** The board reads dark green beside the pyramid (41 and 47). Only its lit lower left reaches 60 |
| every display piece now at 0.9 to 1.1 of real size; the second toolbox straddles the mullion | **Not a point from the street.** Nothing reads small or crowded. A box behind a mullion is what a real window does. The close view judges the scales |
| no step ladder, one paraffin can fewer, tiers 0.4 and 0.8 not built, pegboards a third covered | **Not a point from the street** (unchanged from try 1). The counter and the display hide them, and both boards read as tool boards |
| dark at night: night_lit is the tests' state, night_dark the real night | **Right, per the target.** The night_dark glass reads 12.3, 0.70 of the brick beside it. But see narrow points 2 and 3 for its two dark patches |
| 64 samples, not 128 | **Owed on the PC**, not a point. No noise shows at street distance |
| the hanging board black iron, unlit | **Right for a day shop.** Its geometry is narrow point 1 |

## What is right

**The front.** From the far pavement it is a British Victorian parade's timber ironmonger, built from the 3.2 kit, and it sits beside Rita's approved front as one family:
- dark-green fluted pilasters on plinths, with scroll consoles;
- the cream 4.1 board under the timber cornice;
- the sill and the two-panel stallriser;
- the T2 window: two lights, six toplights, the mullion carried up;
- the band over both doors: the fanlight with 16 and three toplights; the panel, transom and head;
- the half-glazed T1 shop door: hinges on the viewer's left, lever on the right, letter plate in the lock rail, brass kick plate;
- the black F1 side door, with its knob, lock and vertical letter plate.

Nothing is mirrored and nothing floats but the scroll (point 1). The pilasters meet the wall at both cameras, with no slot at STREET_30. The front is as clean as Rita's: the wear is owed (PC-05). The hours plate now matches Rita's in style and place, and the board, at 0.84 out, hangs clear of the joinery.

**The lettering.** These read at 100 per cent from both cameras:
- IRONMONGER; TOOLS & HARDWARE (the S clean); PAINTS & PARAFFIN;
- KEYS CUT, on face a;
- EST. 1884, whole in its toplight (GLS-02: 0 of 3,458 ink points behind a bar);
- the 16 on the fanlight;
- OPEN by day, CLOSED at night (SIGN-01);
- MON-SAT 8.30-5.30 / WED 8.30-1 / SUN CLOSED, which matches the target's hours with its Wednesday half day.

FAS-01c: letters 60.7 to ground 125.3, ratio 2.06. At night_dark the painted letters still read (fascia 36.4 against brick 25.5).

**The window: glass with a lit, stocked room by day and an honestly dark one at night.**

| measure | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, glass mean (p5, p95) | 59.4 (25.5, 125.3) | 60.5 (20.7, 125.9) |
| day, brick beside | 84.0 and 83.1: the glass is 0.71 of the wall | 84.0 and 87.5: 0.72 |
| day, glass under 3 / under 12 / any channel at 250 or more | 0 / 0.31% / 0.014% | 0 / 0.76% / 0.024% |
| day, largest connected patch under 12 | 0.09% | 0.16% |
| day, largest 9 px uniform patch | 0.88%, the backing board (luma 33) | 1.98%, the counter panel (point 6) |
| night_lit (the tests' state), glass; brick beside | 72.3; 20.6 and 18.1 | 72.7; 20.8 |
| night_lit, GLS-03 p95 / GLS-04 px 40 or more over the reflection-off render | 2.1 / 0 (my measure, eroded mask) | 2.7 / 0 |
| **night_dark (the real night)**, glass mean (p5, p95) | **12.3 (1.1, 26.6)**: 0.70 of the brick beside (17.7, 17.2), under the brick above (25.5) | not rendered (target) |
| night_dark, toplight strips | 17.3 to 23.6, none above the brick above | |

Against the target's composite floors (day 33, night_lit 45, night_dark 10 to 35), the frames give 59.4, 72.3 and 12.3. The day room reads:
- the 60-drawer wall;
- the shelves of tins and oils;
- the counter with its till and toolboxes;
- both pegboards (the right one at STREET_30);
- the bin and the paraffin cans.

The night_dark room reads, dimly, under the sodium wash.

**The trade reads from the street.** These say "ironmonger" before the board is read:
- the 36-tin pyramid on its green board;
- the stepped crate (four oil tins, four labelled cleaner tins, the blowtorch, HARTSIDE);
- two galvanised watering cans and two grey toolboxes;
- the trowels on their trays;
- the sprinkler, the pump and the ash-handled sledgehammer;
- three push brooms heads up;
- a row of bulbs, and twelve price cards.

TRD-01's three families are confirmed by eye. Nothing anachronistic stands out. A plastic broom and a plastic sprinkler are both plausible for 1990.

**Content.**
- No drink, gambling, child, toy or person is shown.
- **Legible at 100 per cent in the five street frames**, all the project's own words and acceptable:
  - IRONMONGER; TOOLS & HARDWARE; PAINTS & PARAFFIN;
  - KEYS CUT; EST. 1884; 16;
  - OPEN, CLOSED;
  - MON-SAT 8.30-5.30, WED 8.30-1, SUN CLOSED;
  - HARTSIDE (the crate's stencil, the project's invented maker; I know of no firm of that name that matters here);
  - "ONS" (point 5).
- **Not legible at 100 per cent:**
  - the price cards (not even at 350 per cent);
  - the tins' and cleaner tins' labels (at 400 per cent, fragments of the invented HARTSIDE, COLDWELL, ELMSTEAD and BRANTHAM);
  - the drawer labels and the till's keys.
- No firm's name, maker's mark, barcode or modern packaging shows anywhere.
- PARAFFIN is lamp and heater fuel.

**Rita's export faults, checked on the files:**
1. **A height map exported as a normal map:** none. All 13 normal maps are real. The fascia's mean is (127.5, 127.5, 254.9), with blue at 160 or more on 100 per cent. The display's twelve have blue means of 211 to 254; the glove's is a true steep map.
2. **A textured primitive without UVs:** none (275 and 77 primitives; no negative texCoord).
3. **Two parts sharing a face plane:** no black strip on the front or in the display at either street camera. The only dark patch on the front is the side door's shaded corner (FRN-10's rule).
4. **A see-through slot at STREET_30:** none.
5. **The stand-in night light or glass in view:**
   - the spill is off in night_dark;
   - no bar or ghost shows in the night glass (GLS-03 2.1 and 2.7, GLS-04 0 px, measured by me);
   - the bulbs' kept glass (`pane_see_through`, the only transmission material in the display) reads as glass.

The new parts show no fault of their own from the street: the kept glass, the doorway floor (through the door glass, the shop's shelves, plaster and dado; no dark box) and the night sign (CLOSED).

## The check rows: which I trust

**Re-measured, and I agree:**
- GLB-01, FAS-01n, FAS-03 (both glbs read by me);
- PIC-03 (the corners, and the toplights against the brick);
- GLS-02, GLS-03 and GLS-04 at the street cameras;
- FAS-02 (0.84, the board 0.33 out);
- DSP-11 (the mean; my areas 41 to 60);
- FLT-01's numbers;
- SIGN-01, FRN-13 at the street cameras (by eye), TRD-01, CAM-01 and X-PRV.

**Trusted as written, not re-measured** (the room and the display's inner rules are the close view's):
- PIC-01, PIC-02, PIC-04 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
- SO-01 to SO-07;
- DSP-01, DSP-02, DSP-04 to DSP-10;
- ROOM-02 to ROOM-05, INV-01 to INV-07;
- NEV-01, NEV-02, LIT-06, FRN-01 to FRN-05, FRN-07, FRN-09.

**Pass, but do not prove what they say (4):**
- **FRN-11:** sign against front only. It misses the scroll in the chain (point 1).
- **FAS-01c:** passes, but its detail is the old sentence (point 7).
- **DSP-03:** right for the heads, but it does not see that the gloves read as cuffs (point 4).
- **FRN-08:** passes on the gate's piers; the game's facade is owed (PC-04).

**The cloud's stand-ins only:**
- LIT-01, LIT-01c and LIT-02 (the card's composite alone);
- LIT-02b, LIT-05, LIT-07 and PIC-05g (gate renders with stand-in glass, lamps and spill);
- PRJ-02 (the gate's own `trace`);
- FRN-10's pixel half (shade on the gate's light).

**The failing row:** FLT-01 is judged in point 6. Not a fault.

## What I cannot judge from these files

- **The game's glass:** the street and the sky in the panes, the dirt, and the night hand-over. Here the night glass reflects a black world on purpose.
- **The game's light at night:** Lumen and the real lamps.
  - Whether the display is as dark as point 2's gate shows.
  - Whether the paint reflects the wet street, as point 3 expects.
  - The exposure.
- **Wear, grime and wet on the front and the pavement** (PC-05). The Hook sheet's fronts are grimier than this one.
- **The pictures in motion:** the card's parallax, TSR, and the hanging board's sway (none is modelled).
- **Whether the game's street facade closes beside the pilasters** (PC-04).
- **The 13 October frames:** overwritten. My v1-to-v2 comparisons use the preview JPEGs.
- **Taste, for his page:** whether he wants the window fuller toward its head. The target fills the lower 0.96 m and lets the room carry the upper half.

**Next:** this is try 2 of the street view, and it passes on narrow points.
1. Before any picture of this shop goes to Jafar, fix point 1 (the scroll, in the game's glb) and point 2 (the night_dark display).
2. Then fix points 3 to 7. Point 3 needs only words and a PC row.
3. Then re-render the two street day frames and the night_dark frame.
