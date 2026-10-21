PASS

# The tea rooms (west_north bay 2, no. 14), the CLOSE view: fresh review, try 2 (cloud week 42, unit 7 part 2, stage 2, 15 October 2026)

Reviewer: a fresh reviewer who did not build the shop or write the target. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit (the shop is lit and open to 22:00), with CLOSE_35 night_dark looked at too. I read the try 1 close review only, and not the street reviews.

Read: CLAUDE.md, the brief, `REVIEW-tea_rooms-v1-close.md`, and NOTES.md (the tea rooms' section, "Try 2 shared fixes", "Try 2, tea rooms" and its "What did not pass"). Also `checks/check_tea_rooms_v2.json` (made 15 Oct 06:21: 71 of 74 pass, 6 n/a; FLT-01, FLT-02 and CUR-01 fail).

Looked at:
- the v2 close previews (CLOSE_35 day, night_lit and night_dark) and the three v2 room previews;
- the 2560 x 1440 gate frames rendered 15 Oct 05:29 to 06:19 (CLOSE_35 and CLOSE_35_B, day and night_lit; CLOSE_35 night_dark), at 100 to 300 per cent;
- the 4096 room pictures.

Measured in my scratchpad (nothing else was changed):
- `tea_rooms_display.glb` (15 Oct 01:41), parsed directly;
- the glass by the check's own glass and room masks;
- the parallax, by `trace` itself.

**In short:** all three try 1 faults are fixed.
- The table set is real size: the laminate top at 0.740, seats about 0.45, chairs 0.956 high.
- Both chairs face the table.
- By day, the café curtains read as gathered cloth on tabs over a brass rod.

All eleven narrow points are fixed or answered, except two that are partly fixed: the window card's paper, and the curtain at night. The room behind still moves exactly by the game's rule, with no slab and no seam. The door now carries its hours plate and says OPEN at night. Nothing breaks the content rule.

What is left are four narrow points, each with an exact fix. The one new item is a pure black dado-rail end in the night room picture. It shows as a thin black strip in the left light and in the door's upper pane at CLOSE_35_B night.

**0 faults, 4 narrow points.** By Jafar's ruling of 9 October this is a PASS, with the points below for the builder.

## Try 1 items, one by one

| try 1 item | now | where, and the measurement |
|---|---|---|
| F1 table set at child size | **FIXED** | glb: `table_laminate` top 0.740 (0.715 to 0.740), 0.50 across. A 50 mm chrome column and a black four-arm base 0.314 across, 30 mm high. Chairs at scale 1.0, 0.956 high; the seat band is densest at 0.432 to 0.442, so the seat surface is about 0.45. Teapot 0.740 to 0.904 (0.164 with lid). CLOSE_35 day: table 1120-1420, 700-1210; chairs 1300-1600, 590-1150 and 1050-1210, 880-1220. The top now stands well above both seats. DSP-06 agrees. |
| F2 chairs back to the table | **FIXED** | glb: left chair back at x −0.730 to −0.663, seat running in to −0.190; right chair mirrored (back +0.663 to +0.730). The table rim is at ±0.25, so each seat front is 0.06 m under the rim. Seen so in CLOSE_35 day and CLOSE_35_B day (left chair 935-1255, 590-1100). DSP-08 (6 degrees) agrees. |
| F3 curtains read as corrugated plastic | **FIXED by day, PARTLY at night** | (a) Head: tabs wrap the rod with a scallop between them, and the cloth's head is 2.0 mm from the rod (CUR-01a). CLOSE_35 day 0-980, 640-720. (b) Folds: irregular, smooth-shaded, deeper toward the hem. 6 of 449 flat blocks in CLOSE_35 and 0 of 429 in CLOSE_35_B (CUR-01c). (c) Hem: follows the folds, with no saw edge (CLOSE_35 day 0-980, 1090-1290). (d) Cloth: cream with a faint weave by day. At night it is grey satin, not lit cotton: narrow point 2. (e) Rod: the up-pins are gone, and its ends are behind the jamb and mullion. At night the rod reads dark bronze with a highlight: 759 px under luma 8 (CLOSE_35 night 36-315, 663-674) against 5,030 at try 1. Acceptable. |
| N1 hours plate missing | **FIXED** | CLOSE_35_B day, the door's lower pane at about 340-418, 660-750, reading "MON-SAT 6.30 AM - 10 PM / SUN 8 AM - 12 NOON". FRN-12. |
| N2 price cards before the wrong goods | **FIXED** | GATEAU 45p before the strawberry cake (CLOSE_35_B day about 1864-1936, 1344-1384; glb x +0.91 to +0.98). HOME MADE at u 0.30 and CAKES 40p at u 0.50, at the carrot cake. TEAS 25p at u 0.80, the street review's place. The builder's reason for not using 1.60 (within 0.10 m of the table) holds. |
| N3 black upright suction cups | **FIXED** | clear discs flat on the glass with steel hooks (glb `window_card_cups` z −0.003 to 0; CLOSE_35_B day about 1880-1910, 290-320 and 2510-2545, 240-275). |
| N4 window card flat and perfect | **PARTLY** | the bow and the letter jitter are there, but the paper still reads as one flat tone: narrow point 3. |
| N5 the same print twice | **FIXED** | three different pictures. Left wall: the landscape frame and the oval. Right wall: the tall frame, a cliff and sea seen through its glass (room picture day about 3380-3600, 440-960). |
| N6 illegible card under the chalk menu | **FIXED** | "TEAS FROM 25p", paper and dark ink, legible at CLOSE_35 day 695-785, 470-490 and CLOSE_35_B day 1670-1760, 470-495. |
| N7 cork board a flat orange slab | **FIXED** | granular cork, pine frame, a coloured pin on each of six notices (room picture day about 3620-3760, 450-870). |
| N8 pedestal dark at night | **FIXED** (the pedestal is replaced) | the chrome column reads as chrome by day and at night. LIT-08 now measures furniture by its top. |
| N9 PIC-05g at its limit | **FIXED** | measured 0.0078 (CLOSE_35 night_lit) and 0.0064 (CLOSE_35_B night_lit), as the check. See narrow point 4 for where the rest lies. |
| N10 pilot lamp with no lamp | **FIXED** | an amber point at the urn's plinth: CLOSE_35 night_dark about 615-635, 565-580. |
| N11 no seating in the room | **not for this verdict** | written as a Judgement for the target's owner, as offered. |
| shared (a) orange bar in the night glass | **FIXED** | no bar. GLS-04's largest patch is 393 px at CLOSE_35 and 43 at CLOSE_35_B. The burnt clusters are all display pieces (point 4). |
| shared (c) glass parts dropped | **FIXED** | the cake domes, the clock, the frames and the till's readout all show glass. DSP-07. No new fault from it. |
| shared (e) menu stand leans forward | **FIXED** | glb `menu_stand` z −0.097 to −0.074, standing back from the table's front. DSP-05. |
| shared (f) CLOSED at night | **FIXED** | OPEN in both night_lit frames (CLOSE_35_B night about 345-395, 585-630). SIGN-01. |

## Faults

None.

## Narrow points, each with its exact fix

1. **New: the night room picture's dado-rail ends are pure black and show as black strips.**
   - In `tea_room_night_lit.png` the side walls' dado rail meets the picture's two edge columns at rows 971 to 1004, about 9 px wide, in (0, 0, 0). The same pixels are (110, 72, 50) by day. The rail's front end face gets no light at night.
   - The game's rule stretches those edge columns along the side walls, so they show as:
     - CLOSE_35_B night_lit, the left light: a strip at 546-751, 520-543 (3,832 px under luma 8) between the plaster and the dado;
     - CLOSE_35_B night_lit, the shop door's upper pane: 301-433, 527-544 (2,144 px). The gate's `hall_face_dado` takes the same column;
     - CLOSE_35 night_lit, the right edge of the right light: 1934-1970, 525-544 (679 px).
   - It reads as a dark rail line, not a slab, but it is the only pure black run in the lit glass.
   - **Whose:** the builder (the room's rail) and the kit (the gate's hall-face column).
   - **Fix:**
     - run the side walls' dado rail and boards on 0.10 m in front of the card plane, so the picture never draws the rail's end face;
     - make the gate's `hall_face_dado` and `hall_face_plaster` take the picture's column 24 px in from the edge, not the edge column;
     - draw night_lit again (the room, and the two close night_lit frames);
     - a row: no pixel under luma 8 in a lit room picture's outer 16 columns.
2. **The curtains at night read as grey satin, not lit cotton** (the builder's named shortfall, CUR-01 (d)).
   - Where: CLOSE_35 night_lit 0-980, 660-1250 and CLOSE_35_B night_lit 1620-2560, 650-1230. Each fold's ridge carries a bright specular streak with a dark trough beside it. Nothing of the tubes behind glows through.
   - At close range the cloth is as bright as the room round it (LIT-08 0.98 and 1.27). At STREET_SQUARE the left panel is 0.66 of the glass above it (0.8 asked).
   - By day the cloth is right.
   - **Whose:** the builder.
   - **Fix:**
     - sheen 0.4 to 0.1, roughness 0.9, specular 0.3;
     - the Translucent mix 0.3 to 0.5;
     - behind each panel, a warm (2900 K) area light 1.0 x 0.5 m facing the glass, 0.3 m behind the cloth at its mid-height, 40 W, invisible to the camera and to glossy rays. This is the stand-in for the room's tubes, which the picture cannot light through;
     - set it by one 16-sample test of the two close night_lit frames and STREET_SQUARE night_lit (lesson 26), so that CUR-01 (d) reaches 0.8 or more and PIC-05g stays at 0.008 or under.
3. **The window card still reads as one flat white tone** (the builder's named FLT-01; try 1 N4, partly fixed).
   - Where: CLOSE_35_B day 1872-2512, 256-640. 62 of 240 32-px blocks have a standard deviation under 0.8, at luma 191. At STREET_SQUARE it is FLT-01's 2.16 per cent.
   - The 1 mm grain of 4 levels is lost to the denoiser.
   - **Whose:** the builder.
   - **Fix:** a card-stock grain of ±8 levels at a 3 mm feature size, plus a mottle of ±4 levels at 40 mm, roughness 0.85. The check: FLT-01 under 1 per cent, and under 5 per cent flat blocks on the card in CLOSE_35_B day.
4. **The white chair seats and the china stand are the hottest things at night.** PIC-05g passes, so this is narrow.
   - Burnt clusters (a channel at 250):
     - the left chair's seat, CLOSE_35_B night_lit 957-1122, 837-895 (5,154 px);
     - the table top, 1134-1438, 709-746 (3,922 px);
     - the carrot cake's china stand, CLOSE_35 night_lit 310-520, 1245-1347 (4,706 px);
     - the teapot's top, CLOSE_35 1222-1350, 650-685.
   - The left seat is the brightest object in CLOSE_35_B night.
   - **Whose:** the builder.
   - **Fix:**
     - the chairs' paint toning 0.78 to 0.68 of the model's;
     - the china stand's base colour to (200, 196, 186);
     - or the spill 150 to 125 W;
     - set in the same 16-sample test as point 2, to PIC-05g 0.005 or under at both close night frames.

## What is right

- **The near metre is a 1990 tea-room window at real size.**
  - A Formica café table with an aluminium edge, a chrome column and a black cast base.
  - Two painted slat chairs facing it.
  - The scanned teapot, cups and saucers and sugar bowl, and a tent card, on a 0.74 top.
  - The carrot cake on its stand, the strawberry gateau on its plate, the haworthia.
  - Price cards before the right goods.
  - Nothing buried or through a part (DSP-03, DSP-05). The chairs stand 4 mm clear of the curtain's back (glb).
- **The curtains by day** read as gathered cloth hung by tabs on a brass rod, with soft irregular folds and a natural hem.
- **The room**, at 100 per cent: a deep, lit serving end.
  - The matchboard dado with its rail; 24 cups on two shelves; two glass cake domes, rolls, the tea set, a kettle and a till.
  - The urn with its amber lens, the chalk menu and its legible card, the hatch.
  - Three different framed photographs under glass, the clock under glass, a real cork board.
- **The parallax, by `trace` itself** (west card, side −1, W 5.3, H 2.4, D 4.5, camera_d 5.3). I used the chalk menu frame's top-left corner (room hx 3.20, height 1.94, depth 4.47):
  - it crosses the card at street x 27.126 from CLOSE_35 and at 28.483 from CLOSE_35_B: 1.357 m apart for 2.0 m of eye travel;
  - both card points trace back to picture px (2279.1, 616.5) and (2275.3, 616.5); the render rule gives (2278.6, 617.2);
  - in the new frames, the board's top-left corner is at (674, 378) and (1661, 387), against the projected (672, 376) and (1661, 386). Its bottom-right corner is at (799, 469) and (1776, 469), against (801, 472) and (1773, 467). All within 3 px.
  - So the back wall moves by about 990 px between the cameras, as the rule says.
  - No black slab, no end of the picture, and no seam where the bed meets the room's floor, from either camera.
- **The door:**
  - the cream leaf, the OPEN card (OPEN by day and in night_lit);
  - the hours plate in the lower pane, the lever on the left stile;
  - the letter plate, the kick plate, the gilt 14;
  - the dark side door.
  - No black strip in any joint by day: 0 px under luma 8 in the door box at CLOSE_35_B day. The night strip is point 1.
  - Through the door glass: the hall face and the room, never a reveal slab (FRN-13, 0 of 2,240 close rays).
- **The night:** no arc, no orange bar, no glowing head band; the lit room is warm and bright behind the glass. night_dark (looked at, not this shop's open night): the sodium wash lights the curtain's head a little more than its body (luma 44 against 34), like a street lamp above, with nothing burnt (0.0000).
- **Rita's export faults are not repeated:**
  - no height map as a normal map, and no textured primitive without UVs;
  - no coplanar black strip, and no see-through slot at either camera.

## Measured

**The glass's mean luma** (all window glass by the check's own mask, full gate frame):

| frame | left light | middle | right | all glass | wall beside | room part / display part |
|---|---|---|---|---|---|---|
| CLOSE_35 day | 99.5 | 79.5 | 111.2 | 95.1 | brick 88.4 | 60.5 / 140.8 |
| CLOSE_35 night_lit | 79.8 | 74.3 | 63.0 | 76.0 | brick 18.0 | 72.5 / 81.4 |
| CLOSE_35 night_dark | 24.6 | 19.1 | 20.0 | 22.4 | | 15.9 / 31.3 |
| CLOSE_35_B day | 95.7 | 74.4 | 122.4 | 103.9 | pilaster 84.6 | 55.9 / 147.9 |
| CLOSE_35_B night_lit | 66.2 | 82.0 | 66.5 | 71.2 | pilaster and door 15.8 | 68.3 / 74.2 |

- The target's floors are day 33 and night 45. The lit room at night is 4.2 to 4.5 times as bright as the wall beside it, and the day room reads plainly.
- The check's room-only composites agree (LIT-02 CLOSE_35: 50.2 by day, 68.0 at night).

**Black and flat regions inside the glass:**
- Under luma 8 by day:
  - CLOSE_35: 15 px;
  - CLOSE_35_B: 1,591 px, the largest 919 (1101-1125, 617-664: the shade beside the counter's left end, as at try 1).
- At night (night_lit):
  - CLOSE_35: 3,172 px, the largest 793 (a picture frame's dark side, 1329-1334, 332-522);
  - CLOSE_35_B: 14,432 px, the largest 3,832 (point 1's rail strip) and 3,602 (the same counter-end shade, 1100-1126, 583-737).
- No void and no slab. LIT-02b passes.
- Flat 32-px blocks (standard deviation under 0.8):
  - by day, 47 of 2,173 at CLOSE_35 (2.2 per cent) and 97 of 2,222 at CLOSE_35_B (4.4 per cent), most of them the window card (point 3);
  - at night, 12 to 18 per cent: the room's even plaster and ceiling in low light, and the dark dado.

**Burnt** (a channel at 250 or above): CLOSE_35 day 0.0014, night_lit 0.0078; CLOSE_35_B day 0.0001, night_lit 0.0064. The clusters are in point 4.

**Every legible word at 100 per cent** (both close frames, day and night):
- Window card: BREAKFASTS, LUNCHES, TEAS.
- Price cards: CAKES 40p, TEAS 25p, HOME MADE (small), GATEAU 45p.
- The table's tent card: TEAS FROM 25p (just legible).
- Door: OPEN, MON-SAT 6.30 AM - 10 PM, SUN 8 AM - 12 NOON, 14.
- Room: TODAY'S MENU, TEA 25p, COFFEE 35p, TOAST 30p, TEAS FROM 25p, and the clock's numerals.
- The cork board's six notices (TEAS FROM 25p, TABLES BOOKED, THANK YOU, LUNCH 12 - 2, CAKES MADE HERE, OPEN 6.30 - 10) and the till's readout are legible only in the room picture, not from the close cameras.
- **All are the project's own words and numbers, and acceptable.**
- The OCR of the source maps (`ocr_out.json`) finds only the till's readout digits and the kettle's THERMOMETER dial. No maker, firm or modern mark.

**Content rule:**
- No drink, gambling or children's things. The table set is now adult size.
- Tobacco: none.
- Nothing after 1992.

## The builder's named shortfalls, judged

| shortfall | judgement |
|---|---|
| CUR-01 (d): the left curtain 0.66 of the glass above it at STREET_SQUARE night | **Narrow** (point 2). At close range it is as bright as the room; the fault is its satin look. |
| FLT-01: the window card's flat paper | **Narrow** (point 3) |
| FLT-02: a counter panel in shade and the right wall's plaster at the street cameras | **Not this view.** At close range the counter fronts and plaster read as painted wood and plaster (flat blocks above). |
| Close 11: no seating in the room | **Not for this verdict** (a Judgement for the target's owner) |
| Fabric034 not used; a generated weave instead | **Acceptable**: the weave reads by day |
| The night_dark card left off the wash | **Acceptable**: the card is not hot in CLOSE_35 night_dark |
| 48 samples; the steamed glass; the game's glass, Lumen, exposure and TSR | **Owed** to the PC, not points |

## The check rows: which I trust

**Trust** (re-measured or seen):
- DSP-06 and DSP-08 (my glb parse agrees), DSP-03, DSP-05, DSP-07;
- FRN-12, FRN-13, SIGN-01;
- PRJ-01 to PRJ-03 (my `trace` agrees);
- PIC-01 to PIC-06, PIC-05g (my numbers agree);
- GLS-01, GLS-02, GLS-04;
- INV-01 to INV-07, NEV-01, TRD-01, SO-01 to SO-07;
- CUR-01 (a) to (c).

**Pass, but blind:**
- LIT-02b and FRN-13 do not see point 1's black rail strip: it is under LIT-02b's share limit, and FRN-13 counts the hall face as good wherever its picture is black.
- LIT-08 now leaves the chairs and the table out, so a burnt white seat (point 4) is seen only by PIC-05g.

**The cloud's stand-ins only:**
- LIT-01, LIT-02, LIT-02b, LIT-05, LIT-07, LIT-08;
- GLS-03, GLS-04, PIC-05g;
- CUR-01 (d), FLT-01, FLT-02 (they depend on the denoiser and the stand-in lights);
- PRJ-02 (PC-01 owed).

## What I cannot judge from the files, and what I could not repeat

- **Not repeated:** GLS-03's p95, LIT-08's per-piece rings and DSP-03's silhouette shares. The object-index and reflection-off renders are there, but I did not re-run those rows in the time. The try 1 frames are overwritten, so I compared against the try 1 review's numbers, not its pictures.
- **Cannot judge:**
  - the game's own glass (reflections, Fresnel), Lumen, exposure and TSR;
  - the steamed glass and the curtain's sway;
  - the shop-door bell, which neither close camera sees;
  - wear and wet;
  - the street view.
