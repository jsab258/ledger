FAIL

# The newsagent and tobacconist, the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2; 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit (the shop is lit at night). I did not read the street review of this shop or any review of the ironmonger.

Read: CLAUDE.md; RULINGS.md (1, 2, 3 and 8 Oct); NOTES.md (the opening, "For the next nine shops", the newsagent's section, lessons 16 to 27); TARGET.md sections 3, 5.9 and 13 (A7 to A9, A14); Rita's four reviews; `checks/check_newsagent_v1.json`; `MANIFEST-newsagent.json`; the parts of `sw_shops_news.py`, `sw_gen.py` (`GM.sheet`) and `sw_room.py` named below; `tools/ue/make_interior_material.py` (`trace`).

Looked at: the two close previews; the four close gate frames (2560 x 1440) at 100 to 500 per cent; the three room pictures (4096) at 100 to 300 per cent; the display's own textures (`display_work/tex`, and the 13 images inside `newsagent_display.glb`); every placed model's base-colour map at 100 per cent, in 512 px quarters.

Measured, all in my scratchpad (nothing in the repository or in SCRATCH was changed): the glass luma, dark, flat and clipped pixels in the frames; the parallax, through `trace` itself, checked against the frames; every mesh of `newsagent_display.glb` (bounds and vertices, by importing it); the normal maps and texture coordinates of both glbs; MANIFEST against the files (all five sha256 match).

**In short.** The projected room works: it moves exactly as the game's rule says and reads as a deep, lit shop with a gantry, a counter, a pension counter and a back door. The door, the side door and the glass lettering are right, and nothing in this shop breaks the content rule. The near metre fails, which is what this view is for:

- the magazine board is built leaning the wrong way, toward the glass: the magazines hang in the air under it and a third of them are hidden behind it, and the newspapers lean forward off their steps (the same sign error);
- every printed good (the papers, the magazines, the cards, the postcards, and the covers and cards in the room) carries the same eight flat clip-art pictures, and the sweet jars are opaque painted cylinders, so at 100 per cent the window reads as placeholder stock, not a newsagent's of 1990.

**2 faults, 9 narrow points.** This is try 1 of the CLOSE view.

## Faults, worst first

### 1. The magazine board leans toward the glass; the magazines hang under it, four are hidden behind it, and the papers lean forward off their steps

- **Where:**
  - CLOSE_35 day: the board is the pale slab from about (1085, 940) to (1545, 867) up to (1060-1640, 1000). The top row's four magazines (green, red, navy, white) show only as edges above its top edge at (1050-1475, 870-930). Two rows hang below it with their shadows on its underside (1060-1640, 900-1280).
  - CLOSE_35_B day: the slab runs from (1070, 887) to (1530, 953). Hidden row edges at (1137-1530, 887-947). The hanging rows at (1110-1530, 953-1173). The gap between the magazines and the board shows plainly.
  - At night, the pocket under the board is the largest near-black patch in the window: CLOSE_35 night_lit (1168-1388, 951-1099) has 3,737 px under luma 8, and CLOSE_35_B night_lit (1235-1359, 970-1112) has 2,739 px.
  - The papers: CLOSE_35_B day (640-1100, 830-1080). Each folded paper tips toward the glass with nothing in front of it.
- **Measured** (vertices of `newsagent_display.glb`; v is the depth from the glass, w the height above the bed):
  - `magazine_board`: its foot is at the BACK (v 0.538-0.547, w 0.000-0.008) and its top edge at the FRONT (v 0.165-0.175, w 0.444-0.452). It is a lean-to over the plinth whose underside faces the street.
  - The 12 magazines lie parallel to it, in three rows:
    - **row 2** (STAMP CORNER, PUZZLE BOOK, MODEL RAILWAY NEWS, THE WALKER) lies about 0.10 m BEHIND the board, unseen;
    - **row 1** hangs about 18 mm in front of the underside, touching nothing;
    - **row 0** stands on the bed and leans 40 degrees toward the glass, 0.16 m clear of the board, held by nothing.
  - TRD-01's "57 per cent seen" for the magazines is the hidden row.
  - Every `newspaper_*` has its top 66 to 70 mm nearer the glass than its foot (newspaper_0: foot v 0.202, w 0.063; top v 0.136, w 0.254). That is about 19 degrees forward, away from the riser behind it.
  - LIT-08's one failure (the magazines at 0.54 of the room at CLOSE_35 night) is this board's shadow, not the covers' colour.
    - The head spill (v about 0.07, w 1.65) reaches row 1's centre (v 0.33, w 0.20) only through the board: the ray crosses the board's plane at v 0.315.
    - The builder's judgement N10 blames the navy and green covers. Lifting them 1.35 times treated the wrong cause.
- **Cause:**
  - `sw_gen.py` line 68, `GM.sheet`: `y, z = y*cos(t) - z*sin(t), y*sin(t) + z*cos(t)` sends a sheet's top to -y (toward the glass). Its own docstring (line 61) and the comment on that very line say "the top toward +y".
  - `sw_shops_news.py` computes every centre for a back lean:
    - line 325: `vc = foot_v - 0.01 + hh/2*sin(lean)`;
    - line 387: the board's centre at `vb + blen/2*sb`;
    - line 397: `vc = vb + s0*sb - off*cb`.
  - So every leaning sheet is mirrored about its own centre.
  - Line 396 also has the wrong sign on the magazines' offset off the board: `zc = 0.004 + s0*cb - off*sb`.
  - DSP-03 cannot see this. It tests only intersection, and these meshes float without touching anything. DSP-01 tests only the 5 Poly Haven pieces.
- **Whose:** the kit (`GM.sheet`'s sign) and the builder (the offset sign; no test that a leaning sheet rests on its support).
- **Exact fix:**
  1. `sw_gen.py` line 68: `y, z = y*math.cos(ta) + z*math.sin(ta), -y*math.sin(ta) + z*math.cos(ta)`, so that a positive tilt sends the top to +y, as the docstring says. The other caller in another shop (`sw_shops_tea.py` 265, the menu card, tilt 12) then leans back too. Run its `scenecheck`.
  2. `sw_shops_news.py` line 396: `zc = 0.004 + s0*cb + off*sb`. The offset runs along the board's front normal (-cos, +sin) in (v, w). With `off` 0.0095 + 0.0045 x row, row 0 clears the 12 mm board by 2 mm.
  3. Lines 382 and 384: `vb = 0.18` (the foot 10 mm behind the plinth's back face at v 0.17; at 0.17 the foot cuts 5 mm into the plinth) and `blen = 0.56`. The top edge is then at v 0.54, w 0.43, inside the 0.55 window. Row 2 still fits (it reaches 0.545 of 0.56 along the slope).
  4. The papers, line 318 to 325: each paper's top edge rests 2 mm off what is behind it:
     - the riser at v 0.24 (top at v 0.238), or the back board at v 0.37 (top at v 0.368);
     - the feet stay 12 mm apart in depth;
     - a paper whose top would then cut the paper behind it takes 1 degree less lean.
  5. A new check, DSP-05, failing the build:
     - every display sheet with a lean over 3 degrees leans back (its top's v is greater than its foot's);
     - its top is within 5 mm of a support behind it (the board, a riser, the paper behind);
     - no display piece's lowest point is more than 2 mm above the support under it;
     - DSP-01 then covers the scripted pieces too.
  6. Re-render the gate and re-measure LIT-08 with the covers at their own colour (lift 1.0). If they still read under 0.6, then lift them.

### 2. The printed goods read as clip-art placeholders at 100 per cent, and the jars as painted plastic

- **Where:** the whole near metre and the room's walls.
  - CLOSE_35 day:
    - the ten papers (0-1150, 780-1440);
    - the magazines (1060-1640, 900-1280);
    - the postcard rack (1416-1592, 456-824);
    - the card spinner (1725-1869, 520-877).
  - CLOSE_35_B day:
    - the card spinner (2300-2560, 440-1240);
    - the jars (1740-2200, 1090-1440);
    - the room's left wall of 60 covers (992-1361, 242-636).
  - The textures: `display_work/tex/{magazines,papers,cards,postcards,jars}.png`, the same atlases inside the glb.
- **What the eye sees:**
  - **One small set of pictures.** Every cover, card, postcard and front page uses one of about eight flat vector pictures in four or five flat colours: a row of round flowers, a cartoon car, a cartoon train with wheels, a sailboat, a lighthouse of three blocks, a red house, two triangles, a duck.
  - **The papers** are rigid 4 mm boxes (12 triangles each) printed with a masthead and a headline over a grey copy of the same pictures. There is no body text and no fold or curl; target 4.5 asks for "a curl and a fold".
    - They are 0.22 m wide. A tabloid is 0.29 m, so next to the 0.20 m cartons they read as placards.
  - **The postcards' captions do not match their pictures:**
    - THE HARBOUR AT DUSK is a bed of flowers in daylight;
    - WEST COAST BEACH is a red house on grass;
    - MERIDIAN FROM THE HILL is a duck.
  - **The cards** on the spinner are the same flowers and house.
  - **The sweet jars** are opaque lathes with a flat sweets pattern on the outside. There is no glass, no depth and no single sweet; the humbug jar reads as a zebra-striped bottle. In the room the brown, red and black jars read at a glance as coloured bottles behind a counter.
  - The 5 Poly Haven pieces (the pens, the pots, the pads) read as real objects beside them, which makes the contrast plainer.
  - The game is photoreal; the bar is "yes only for what would pass in a 2026 game". Rita's close review (try 1, narrow 7) made the same call on two clip-art prints. Here it is most of the window, so it is a fault.
- **Whose:**
  - **The builder:** the picture generator in `sw_gen.py` (`TEXTS` and the atlases) and `sw_shops_news.py`'s jars.
  - **The target:** 4.5 asks only for "fictional" covers and "invented" titles, and never says photographic.
- **Exact fix:**
  1. **One picture library for every printed good**, from CC0 photographs: crops of Poly Haven HDRIs and texture photographs (harbour, coast, boats, gardens, roads, countryside, a lighthouse, a mill). Make them as Rita's harbour prints were made (`sw_assets.harbour_print`): tone-mapped, saturation 0.7, a slight warm cast, paper grain, no person.
     - At least 16 distinct pictures, each with a catalogue line.
     - The room's covers and cards (`sw_room_gen`) use the same library.
  2. **Magazines** (the 12 in the window and the 60 in the room):
     - the photograph full-bleed over the whole cover;
     - the masthead across the top 18 per cent;
     - three to five cover lines in two sizes over the photograph;
     - a price (95p to £1.50) and OCTOBER 1990 in a top corner;
     - no barcode;
     - a 2 mm spine and a bow of 3 mm across the width.
  3. **Papers:**
     - the visible half of a folded tabloid at 0.29 x 0.19 m: two papers a step, four a stand, eight in all, overlapping under a third (lesson 22);
     - the masthead, then a headline that fits (see narrow 1), a halftone of a library photograph in greys (a 1.2 mm dot screen), and 3 mm body text in four columns below it;
     - the top edge a fold (a half-round of 2 mm radius);
     - the sheet bent 4 to 8 mm over its height (6 segments, not 12 triangles).
  4. **Cards:** a library photograph or a CC0 painted-flower crop on the front, with the greeting in a serif or script in gilt (200, 160, 70) or deep red.
  5. **Postcards:** the photograph full-bleed inside a 3 mm white border. The caption names what that photograph shows; a check compares the two lists.
  6. **Sweet jars:**
     - an outer shell 2 mm thick, in the kit's goods-glass material (`sw_room.py` line 305: white, roughness 0.05, IOR 1.5, transmission 1, not blended);
     - inside, a lathe of the contents at 0.94 of the radius, filled to 0.80 of the height, with a domed top;
     - the sweets texture on it with a 1 mm bump;
     - the paper label on the outside of the glass;
     - the same in the room's ten jars.

## Narrow points, each with its exact fix

1. **Two headlines lose their last word in the texture.**
   - "RAIN FORECAST FOR THE" (…WEEKEND): CLOSE_35 day (420-560, 1280-1340) and (735-830, 1025-1080).
   - "NEW LIBRARY OPENS ON" (…FRIDAY): CLOSE_35 day (685-790, 1205-1255).
   - A player reads them as unfinished.
   - Fix: the paper generator shrinks the headline type in 2 px steps until every word fits in three lines. A check compares the drawn words with `TEXTS`.
2. **"MERIDIAN MORNING STAR"** (CLOSE_35 day, about 330-535, 1050-1080) carries the title of a real national daily, the Morning Star.
   - Fix: rename it, for example THE MERIDIAN COURIER (test the name against the brand blocklist), and add "MORNING STAR" to the blocklist.
3. **The cartons read as big packets.**
   - Each says "20 CIGARETTES", and the bottom band says only "HEALTH WARNING" (CLOSE_35 day 175-745, 785-975).
   - Their faces are 200 x 100 mm. A carton of 200 shows about 280 x 90.
   - Fix:
     - "200 CIGARETTES";
     - the band carries the 1990 wording in 2.5 mm type: "MIDDLE TAR As defined by H.M. Government. DANGER: Government Health WARNING: CIGARETTES CAN SERIOUSLY DAMAGE YOUR HEALTH";
     - six cartons of 280 x 90 x 50 mm, two columns of three laid flat on the stand.
4. **The pads burn at night.**
   - The yellow pad is a flat (255, 254, 145) block at CLOSE_35 night_lit (1209-1361, 1127-1188, 4,149 px) and CLOSE_35_B night_lit (1132-1270, 1118-1183, 4,340 px).
   - The white A4 stack is flat white beside it (CLOSE_35 night 1328-1461, 1101-1159).
   - The printed goods were toned to 0.86 (N10), but these Poly Haven pads were not.
   - Fix: multiply the display copy's `office_notepads` base colour by 0.86, as the printed whites. Then add to PIC-05g: no piece with more than 20 per cent of its own pixels at 250 or more.
5. **The racks hold their cards on a 1.8 mm wire ring, with no pockets,** four to eight to a tier. A 1990 spinner is wire pockets packed three to five deep.
   - Fix:
     - a wire pocket per card: a 2 mm rod bent in a U, 20 mm deep, 0.8 of the card's width;
     - two more cards behind each front card, 6 mm apart, whose top 15 mm shows.
6. **The checks cannot see fault 1, and two records carry Rita's words.**
   - Add DSP-05 (fault 1, fix 5).
   - DSP-03's detail names "the scripted trays, pads and chains" of Rita's front row: word it for this shop.
   - `MANIFEST-newsagent.json`'s "what" is Rita's sentence ("the narrow-points build … v3 … rebuilt by build_ritas.py"). Write this shop's: "the newsagent's batch A build, 13 Oct; rebuilt by `build_shop.py --shop newsagent`".
7. **The till's readout keeps a "Y" glyph left of the amount.** In the room picture it reads as a yen sign: "¥ 0 2 1 3.7 7 0" at 200 per cent, about (1865-1882, 838-852).
   - Fix: paint it out as the $ was, box (500, 228, 514, 248) of `CashRegister_01_diff_1k.jpg`, and the matching boxes of its normal and ARM maps.
8. **48 samples, not 128** (named). Owed on the PC before his page.
9. **Each named change must be in NOTES** (the papers 0.22 wide, the pads at 0.6, no curl or fold). The curl and the fold are missing from NOTES and from the target's A9. Write them there; fault 2's fix 3 then removes them.

## Shared, known (the gate and the kit; not counted in this verdict)

- **(a) The stand-in lamp's pool shows in the night glass as a burnt orange bar.**
  - CLOSE_35 night_lit (1494-1898, 670-750), clipped (255, 184-194, 64-85), 9,368 px.
  - CLOSE_35_B night_lit (699-1021, 674-725), 5,886 px.
  - Close-35-night-lit preview (820-1210, 420-460).
- **(b) night_dark's sodium wash burns the top corners orange.** In `newsagent_night_dark.png` (preview: top-left 0-120, 0-60 and top-right 1480-1600, 0-60). This shop's night is night_lit, so it is not in my frames.
- **(c) The loader dropped the glass of two room models.** `CashRegister_01_glass` (the readout's cover) and `wall_clock_glass` (the dial's cover) are absent. The till's readout and the clock's dial in the room picture have no pane. The build is of 13 Oct, before the kit's `keep_glass` change of 14 Oct.

## Maker's marks (d): checked fully, none survives

Each placed model's base colour at 100 per cent, in four 512 px quarters, with the original beside the clean map where marks were found:

- **CashRegister_01** (clean map):
  - the $ is gone from the readout; TITCH BANKS, the I-heart stickers and the banknote are gone;
  - what is left: the key letters X, Y, Z, A, B, R, TOTAL and the key numbers, which are generic;
  - four tiny tags on the paper strip (map x 985-1000, y 240-395), illegible at 400 per cent and not a maker's;
  - and the "Y" glyph (narrow 7).
- **office_notepads** (original map): no print of any kind.
- **stationery_supplies** (clean map): the pencils' maker and grades are gone, and the boxes' lettering column (x 820-1024) is replaced. The smeared residue at map (100-240, 662-732) and (0-270, 822-912) is not legible.
- **wall_clock** (clean map): numerals and minute marks only. URBAN and quartz are gone.

The display glb embeds `stationery_supplies_*_clean` and the unmarked `office_notepads` maps. The room picture shows the clean till (no $) and the clean dial. `cigarette_pack` ('Kentucky Ace') is not placed.

## Legible words at 100 per cent, both close cameras, day and night

| where | words | acceptable? |
|---|---|---|
| Papers | THE QUAYSIDE MAIL; MERIDIAN MORNING STAR; WEST COAST DAILY; THE MERIDIAN HERALD; MERIDIAN EVENING NEWS; THE WEST COUNTRY CHRONICLE (partly); TRAWLER BACK IN PORT; BUS FARES TO RISE IN MAY; RAIN FORECAST FOR THE; COUNCIL APPROVES NEW BRI(DGE) (the rest under the next paper); HARBOUR REPAIRS TO BEGIN; NEW LIBRARY OPENS ON | yes, but MORNING STAR (narrow 2) and the two cut headlines (narrow 1) |
| Cartons | ALDERLEY, GOLD FILTER; CASTLEMERE, EXTRA MILD; HOLLINGWORTH, KING SIZE FILTER; BRANSTONE, FULL FLAVOUR; DEVEREUX, SPECIAL FILTER; AVONLEA, LIGHTS; "20 CIGARETTES" and "HEALTH WARNING" (soft) | yes: the project's own makers; tobacco is allowed; the wording is narrow 3 |
| Magazines | MOTOR WORLD; CRAFT & MAKING; THE GARDENER'S YEAR; WEEKEND COOK; YACHT AND DINGHY; COUNTRY DIARY; COAST & SEA; GARDEN LOG | yes |
| Price cards | STATIONERY; PENS & PADS; MAGAZINES; SWEETS 2oz 25p | yes, of the period |
| Jars | HUMBUGS; PEAR DROPS; MINT IMPERIALS; SHERBET LEMONS, FRUIT DROPS, TOFFEES (partly) | yes, generic sweets |
| Cards | GET WELL SOON; HAPPY RETIREMENT; HAPPY ANNIVERSARY; BIRTHDAY GREETINGS; WITH SYMPATHY | yes |
| Door | 18; TOBACCONIST & CONFECTIONER; OPEN by day, CLOSED at night; MON-SAT 6-5.30, SUN 7-12 (the target's hours) | yes |
| Room | none at 100 per cent; PENSIONS & ALLOWANCES at 300 per cent | yes |

Nothing else is legible. There is no real firm's name or mark, no barcode, no drink, no betting slip or coupon, no toy and no person. Only MORNING STAR names a real title (narrow 2).

## Measured

**Glass luma** (the three main lights, the polygon from the camera files eroded 4 px; these frames include the stand-in reflection, since the reflection-off renders were deleted):

| frame | glass mean | per light (L, M, R) | under 8 | under 12 | any channel at 250+ (glass) |
|---|---|---|---|---|---|
| CLOSE_35 day | 76.8 | 77.9, 70.8, 85.1 | 0.02% | 0.05% | 0.14% |
| CLOSE_35 night_lit | 75.0 | 73.3, 74.9, 83.9 | 0.40% | 0.69% | 1.12% |
| CLOSE_35_B day | 73.8 | 90.1, 65.4, 74.3 | 0.01% | 0.11% | 0.34% |
| CLOSE_35_B night_lit | 82.1 | 74.3, 67.9, 91.2 | 0.51% | 0.82% | 1.38% |

- **Against the target's floors:**
  - Every frame is far above the composite floors (day 33, night_lit 45).
  - The stallriser below the glass reads about 128 by day and 46 at night (medians). So at night the lit room is 1.6 to 1.8 times the wall beside it, and by day the room is readable under the stand-in reflection.
- **Whole-frame PIC-05g:** 0.0031, 0.0070, 0.0047 and 0.0088, the check's own numbers. At night about two thirds of that is shared (a) and the pads (narrow 4).
- **Black:**
  - By day the largest patch under luma 8 is the gantry upright's shade in the room (252 px at 374-384, 420-496).
  - At night it is the pocket under the magazine board (fault 1).
  - There is no slab.
- **Flat regions:** the largest flat regions (local deviation under 1 level over 24 px) are the ceiling at night and the painted dado in shade by day (luma 47 to 75). These are surfaces, not voids. The only flat white is the burnt pads (narrow 4).

**Parallax** (`trace` imported; the camera files' eyes; the card x 36.35 to 41.65, z 0.65 to 3.05, plane y -5.875, side -1):

| point | picture px | card point (x, z) from CLOSE_35 | from CLOSE_35_B | shift |
|---|---|---|---|---|
| PENSIONS & ALLOWANCES notice (back wall) | (2496, 753) | 1.6167, 1.2317 | 2.9763, 1.2317 | 1.360 m |
| back door's architrave, top right (back wall) | (3115, 573) | 2.0910, 1.3696 | 3.4505, 1.3696 | 1.360 m |
| wall clock (right wall) | (3309, 608) | 2.4510, 1.3708 | 3.6698, 1.3708 | 1.219 m |

- The back wall moves 1.360 m on the card for 2.0 m of eye travel: 2.0 x 4.5 / 6.62. The side wall moves a different amount, so the room has depth.
- `trace` sends each card point back to its picture pixel exactly.
- Projected through the camera, the notice lands at frame (1152, 468) in CLOSE_35 and (2267, 427) in CLOSE_35_B. In both frames the notice is there, within 2 px.
- There is no black slab at either end:
  - From CLOSE_35_B the window's left end is the return wall, plaster over the grey dado, meeting the room's left wall with the dado line unbroken (CLOSE_35_B 500-1000, 120-640).
  - From CLOSE_35 the right end is the right return wall (mean 84 by day, standard deviation 37).
- There is no seam where the bed meets the room's floor (CLOSE_35_B 1580-2400, 1050-1330).

## Rita's export faults, looked for here

- **A height map as a normal map:** none. The display's two normal maps have means (128.2, 128.1, 251.4) and (127.3, 126.6, 252.0), blue 160+ on 99.9 and 100 per cent. The fascia's map is flat (127.5, 127.5, 255).
- **A textured primitive without texture coordinates:** none (53 and 213 primitives, 0 without TEXCOORD_0, 0 negative).
- **Black strips where two parts share a plane:** none at the doors (CLOSE_35 day 1980-2560, 120-1160). FRN-10 agrees.
- **A see-through slot from an angle:** none in either close frame. FRN-08 agrees.
- **The stand-in night light or glass visible:** no arc, no burnt head, no glowing frame. The only burn is shared (a).

## The builder's named shortfalls

| shortfall | verdict |
|---|---|
| about 265 invented packs, not 100 + 8 Poly Haven packs; no sliding glass | right, not a fault (the Poly Haven pack carries a real brand) |
| 12 magazines, papers 0.22 wide, pads at 0.6 on a plinth, the eraser left out | the count of 12 is right. The board they stand on is fault 1. The 0.22 papers are part of fault 2 (0.29 is real). The pads at 0.6 are a narrow point I accept |
| the shutter up, the shut-up variant not built | not this view; right for the lit view |
| the box sign's day face, letters to ground 1.87 (FAS-01c) | not seen from the close cameras; for the street review. By its nature narrow (a colour) |
| the pension counter has no firm's name | right |
| nobody behind the counter | right |
| 48 samples | narrow 8 |
| the spill at 105 W and the covers lifted 1.35 times | the toning of the printed whites works. The covers' lift treats the wrong cause (fault 1) |
| LIT-08 fails at CLOSE_35 (0.54) | not a narrow point on its own: a symptom of fault 1. Re-measure after the fix |

## Check rows: which I trust

- **Trusted** (data and geometry, and the ones I repeated):
  - PIC-01, PIC-04, PIC-06, PRJ-01;
  - PRJ-02 and PRJ-03, confirmed independently through `trace` against the frames;
  - SO-01 to SO-07; ROOM-01 to ROOM-05;
  - INV-01 to INV-06; NEV-01, NEV-02;
  - GLB-01 and FAS-03 (repeated);
  - FRN-01 to FRN-05, FRN-07, FRN-09; CAM-01; X-PRV.
  - **DSP-03** I trust only as an intersection test: it passed a display where a third of the magazines float and a third are hidden.
  - **DSP-01** tests only the 5 Poly Haven pieces.
- **Only the cloud's stand-ins** (the gate's light, glass and lamp; the game's own are owed): LIT-01, LIT-02, LIT-02b, LIT-05, LIT-07, LIT-08, GLS-03, PIC-05g, FAS-01c, TRD-01, and the pixel halves of FRN-08 and FRN-10.
- **X-NOISE:** measured on the ceiling, as A14 rules.

## What is right

- **The room obeys the game's rule pixel for pixel, and reads as a deep, lit newsagent's:**
  - the cigarette gantry of fictional packs across the back wall;
  - the counter with ten jars and the till;
  - the pension counter with its screen, brass slot and hours card;
  - the blue back door;
  - the magazine and card walls;
  - the wall clock;
  - the slate-and-grey chequer floor.
- **The room's layout holds:** there is no slab at either end and no seam at the bed. At night the battens light the whole shop and the room is clearly brighter than the front.
- **The door matches the target:**
  - glass from 871 with the bar at 1423;
  - the hinge on the viewer's left;
  - a brass lever on the right stile;
  - the brass letter plate in the lock rail at 678;
  - the brass kick plate;
  - OPEN by day and CLOSED at night, 3 mm behind the glass;
  - TOBACCONIST & CONFECTIONER and the hours on the glass, 1 mm behind it;
  - 18 on the fanlight.
  - The bell hangs on the top rail, as FRN-03 says. From both close cameras it is behind the hinge stile (it hangs 0.12 to 0.19 m behind the glass), so I could not see it.
- **The side door:** dark blue F1 with its knob, plate and fanlight, with no black strips beside it.
- **The rest of the display:**
  - the pens stand in their pots and the pads on a 60 mm plinth (lesson 22 kept);
  - the hand-lettered price cards are of the period;
  - the paper stands, carton stand and jars stand clear of each other;
  - nothing passes through anything.
- **The content rule holds** in every frame and texture: tobacco only, and every name invented but one (narrow 2).

## What I cannot judge from the files

- **The measurements that need the deleted check renders:**
  - LIT-01, LIT-02, LIT-02b, GLS-03, LIT-05, LIT-07 (the reflection-off renders, the room-only composites and the masks);
  - LIT-08's per-piece numbers (the pieces' index pass);
  - DSP-03's silhouettes and TRD-01;
  - FRN-10's mask;
  - PRJ-02's mean card difference and PRJ-03's recomputation (the baked cards). The parallax itself I confirmed another way.
- **The game's own glass, Lumen, exposure and TSR**, and the box sign's glow (PC-08).
- **The bell** (hidden from both close cameras), its swing and its sound.
- **Wear, grime and wet** (the D53 layer).
- **Anything of the street view.**
