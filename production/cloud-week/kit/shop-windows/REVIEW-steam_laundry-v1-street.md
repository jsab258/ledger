PASS

# The launderette (steam_laundry, east_parade bay 4, no. 9), the STREET view: fresh review, try 1 (cloud week 42, unit 7 part 2, stage 2, 14 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. I judged the street view only: STREET_SQUARE and STREET_30, by day, in night_lit (the tests' state) and in night_dark (the shop's real night, rendered at STREET_SQUARE only). I did not read the close review of this shop or any other shop's review. Jafar's ruling of 9 October applies: a piece that fails only on narrow points (each a small detail with an exact fix) passes, with those points listed for the builder.

**What I read:** CLAUDE.md; RULINGS.md (1, 2, 3 and 8 October); NOTES.md ("For the next nine shops", batch A's and batch B's lessons 16 to 41, and the whole Batch B section with the launderette's own part); TARGET.md section 3, table 5.4 and the 14 October batch B changes (B1 to B4, B13); Rita's four reviews; `checks/check_steam_laundry_v1.json` (all 73 rows); 4.1's manifest entries for this shop; and the parts of `sw_gate.py`, `sw_ctx.py` and `check_try2.py` that make what I saw.

**What I looked at:** the three street previews (`steam_laundry-street-square-{day,night-lit,night-dark}`) and the three room pictures; the 2560 x 1440 gate frames STREET_SQUARE (day, night_lit, night_dark) and STREET_30 (day, night_lit), at full size and in crops up to 8 times; the gate's check renders (glass mask, room mask, front mask, white backdrop); 4.1's board, emissive map and box-sign faces; the Hook sheet; Rita's approved v3 street front.

**What I measured:** Rec.709 luma (0 to 255) over the gate's own glass masks (eroded 3 px), the brick, the board, the lobby and the pavement; ray casts from the STREET_SQUARE eye into `steam_laundry_front.glb` and `steam_laundry_display.glb` (imported with bpy, the gate's own reveal slab and piers added as `sw_gate.py` builds them); the glbs' JSON (UVs, normal maps); the bounds of the fascia, box sign, lobby and pilaster parts.

Pixel boxes are in the 2560 x 1440 gate frame unless marked "1600" (the preview JPEG, 0.625 of them).

**In short:** from across the street this is a British launderette of about 1990 in a Victorian parade. The kit's front is all there and meets: pilasters, scroll consoles, cornice, a lit box fascia, a white-tiled stallriser, a bronze aluminium window, the shop door in a recessed lobby, and the side door with its band and fanlight. The window is glass with a lit room of washers and stacked dryers behind it by day, and an honestly dark room at night. The fascia, SERVICE WASHES and the 9 read. Nothing breaks the content rule, and no real firm's name appears.

No fault blocks. There are nine narrow points. The first must be fixed before these pictures go on Jafar's page: a flat grey slab from the gate stands in the shop's doorway and hides the lobby floor and the foot of the door. The second corrects the builder's notes: the dark block on the board at night is 4.1's "dead tube", not the box sign's shadow.

0 faults, 9 narrow points.

## Faults, worst first

None.

## Narrow points, most visible first (each with its exact fix)

### 1. A flat grey slab fills the foot of the shop doorway (the gate's reveal cuts through the lobby), and what the door's lower glass would show is not defined

- **Where:**
  - STREET_SQUARE day: x 670 to 885, y 932 to 1060 (1600: x 419 to 553, y 583 to 663). A flat dark-grey box 0.55 m high across the whole lobby. Luma 42.2, standard deviation 1.5: a flat card.
  - STREET_30 day: x 880 to 1000, y 884 to 988. Here it reads as a solid box with a lit top standing in the doorway.
  - STREET_SQUARE night_dark: the same place at luma 1.1.
  - It hides all of the lobby floor but its front 120 mm (the brass nosing and a strip of tile still show), the threshold, the door's 170 mm bottom rail with its letter plate (z 113), and the lowest 0.35 m of the door's glass.
- **Cause (ray casts):**
  - `sw_gate.py` builds `reveal_floor` across the full card width: x_m -2.65 to 2.65, y 0.02 to 0.60, z 0 to 0.55.
  - This shop's recessed lobby occupies x_m -1.706 to -0.700 from y -0.10 to the door at y 0.23 to 0.30.
  - So the slab's front face stands 20 mm behind the frame line, inside the lobby, and passes through the lobby's lining (x -1.706) and the window-side return's tiled kick panel (x -0.72 to -0.70).
  - Every ray through the door's foot ends on it. At pixel (780, 1000), for example, the ray hits the slab at y 0.020, z 0.28 before it reaches the door.
- **What lies behind it is a target question.**
  - The M1 door is glazed from 198 mm. The card's bottom edge is 0.55 m above the footway (section 3).
  - From STREET_SQUARE the door's glass from z 0.20 up to about z 0.60 looks UNDER the card. The target says nothing about what stands there, in the gate or in the game (its X1 leaves "the card's bottom to the footway" to the target's owner).
  - If the slab is simply clipped, the gate will show the sky or the void there instead.
- **Why narrow and not a fault:**
  - The game's own asset, the front glb, is built to the target: the lobby, threshold, nosing and door are all there.
  - From 8.76 m the slab can pass for a kick panel.
  - But the gate shows something the game will not show and hides what it will. These street pictures are not fit for Jafar's page until it is fixed. The same rule is in every shop's gate that has a recessed lobby.
- **WHOSE:**
  - the builder, for the gate's slab (the shared kit's `sw_gate.py`);
  - the target, for the door's glass foot against the card's bottom edge.
- **EXACT FIX:**
  1. **Gate.** In `sw_gate.py`, build `reveal_floor` over the window zone only: x_m from (window_u[0] - 3000) / 1000 to (window_u[1] - 3000) / 1000, which for this shop is -0.700 to 2.650. Leave it out where the lobby or a door is.
  2. **Target (recommended).** Give this shop's shop door the M2 leaf's foot: glass from 600 with a kick panel, and the letter plate at 545 in the kick panel (the numbers FRN-03 already holds for M2). From STREET_SQUARE the ray through a glass foot at 600 meets the card's plane at z 0.566, above the card's 0.55 edge, so neither street camera sees under the card. An aluminium shop door with a solid kick panel is the period's usual refit.
     - **Or**, if the owner keeps glass from 198: this shop's card bottom goes to the footway (X1, shop-interiors.json), and the gate gets a floor plane of the room's vinyl from the door to the card.
  3. **Check.** Add a row like FRN-09 for the shop door. Cast 560 rays from each street camera's eye through the shop door's glass. Each must end on the card, the hall or lobby floor, or the room's own geometry: none on the reveal, the sky or nothing.
  4. Re-render the two street day views and the night_dark view.

### 2. The dark block on the board at night is 4.1's "dead tube", not the box sign's shadow; its hard edges read as a shadow patch

- **Where:** STREET_SQUARE night_dark, the upper half of the board over "LAUNDRY": x 1190 to 1545, y 282 to 322 (1600: x 744 to 966, y 176 to 201). It is in night_lit too.
  - It reads 100.7 against the lit ground's 124 to 137, and its two ends are hard vertical edges.
- **Cause:**
  - 4.1's manifest for this board has `emissive.dead_tube`: upper row, x 3300 to 4800 mm, level 60 per cent, "the lower row still lights it".
  - `steam_laundry_emissive.png` carries exactly this rectangle. Mapped onto the board it falls at x 1184 to 1526 in the frame.
  - The box sign cannot shadow the board:
    - it stands above the cornice (z 3.60 to 4.05);
    - the cornice (z 3.40 to 3.55, 0.30 deep) is between them;
    - the stand-in lamp 10 m off at z 4.78 throws the box's shadow onto the brick above the cornice. That is the soft smudge on the brick left of the box (x 1600 to 1690, y 80 to 230), and it is right.
  - NOTES.md ("Known shortfalls") and the brief both name the wrong cause.
- **What it is:**
  - A failed tube is good 1990 grime.
  - A real dead tube behind an opal acrylic face is a soft dim band, because its neighbours' light spreads through the diffuser. A crisp rectangle reads as a shadow or a missing panel.
- **WHOSE:**
  - the kit (4.1's `make_fascias.py`), for the edges;
  - the builder, for the cause written in NOTES.md.
- **EXACT FIX:**
  1. In 4.1's emissive map for this board, feather the dead zone. Ramp it from 60 to 100 per cent over 250 mm at each end (u 3050 to 3300 and 4800 to 5050), and over 120 mm along its lower edge toward the lower tube row.
  2. Rewrite NOTES.md's shortfall line: "the darker upper-right of the lit board at night is 4.1's dead tube (dead_tube, 60 per cent); the box sign's shadow falls on the brick above the cornice".

### 3. FAS-01c fails on a misregistered measurement; the board reads

- **Where:** STREET_SQUARE day, the board: x 432 to 1665, y 285 to 395.
- **Measured in the frame:**
  - STEAM LAUNDRY: ground 174 (sd 2.5), letters 67 (median), ratio **2.58**. At STREET_30 the ratio is 2.77. Linear-light contrast is 4.3 to 1.
  - The trade panel's cream letters on red: 173 against 70, ratio 2.49 (STREET_30: 2.60).
  - At night (the lit box): name 2.64, panel 2.79.
  - Both blocks read from both cameras, by day and by night.
- **Cause of the row's 1.88:**
  - `check_try2.py` projects the 4.1 map onto a plane at Rita's board face, `d_face = 120.0` (hard-coded), z 2.850 to 3.400.
  - This shop's fascia is 4.1's `box_sign` construction. Its face (`box_sign_face`) stands at d 264, z 2.897 to 3.353.
  - The sampled map therefore lands about 6 px and 35 to 47 mm off the face. "Ground" samples fall on letter edges, the bronze frame and the shade under the box, so the row reads a ground of 126.7 against the 174 seen.
- **WHOSE:** the check (the kit's `check_try2.py`).
- **EXACT FIX:**
  1. FAS-01c takes the face's plane and rectangle from the front's members: `box_sign_face` when it exists, else `fas_board` at d 120. Map 4.1's `face_texture_rect_mm` (105, 35, 5305, 515) onto it.
  2. Measure each name block against the ground inside its own ink box dilated by 40 mm. The limit stays 2.0.
  3. Re-run the check. On my measure the row passes at 2.5 or more.
  4. Strike "FAS-01c" from the shortfall list. (The newsagent's 1.87 has the same cause if its fascia is a box sign.)

### 4. A see-through notch between the window's right jamb and the right pilaster's capital (STREET_SQUARE)

- **Where:** STREET_SQUARE day and night: x 1670 to 1674, y 437 to 476 (1600: x 1044 to 1046, y 273 to 298). A 3 to 4 px dark sliver beside the head of the window.
- **Cause (ray casts):**
  - The window's right jamb `win_jamb_r` ends at x_m 2.650.
  - The capital `pilR_capital` is coved on its inner side, so between z 2.55 and 2.72 its side face stands at x_m 2.680.
  - The 30 mm slot between them runs from the jamb's front (y -0.075) back to the wall line (y 0). Rays at x 1671 to 1673 pass through it and end on the gate's brick pier at y 0.
  - FRN-08's white backdrop sees exactly this: 40 px at 1280, at x 835 to 836, y 216 to 238.
  - The row's text calls it "the bay's outer sliver beside the right pilaster, which the gate's pier closes". It is the INNER side of the pilaster. The pier hides it only because the gate's pier happens to start at x 2.65.
  - In the game the wall opening is the whole bay, and PC-04 asks the street facade to close only the bay's outer strip. This slot would show the room's edge or the void.
- **WHOSE:**
  - the builder (the front: the kit's capital beside an M1 jamb);
  - the check (FRN-08's allowance and its wording).
- **EXACT FIX:**
  1. In the front, add a cream backing strip `pilR_cap_back`: x_m 2.650 to 2.700, y -0.011 to -0.001, z 2.500 to 2.850, paint_cream. It is set 1 mm off every neighbour's face, so FRN-10 sees no coplanar face. Add the mirror on the left if FRN-08 ever shows one there.
  2. FRN-08 allows 0 backdrop pixels at the street cameras, as at the close ones, and its text names the place it finds.

### 5. SERVICE WASHES is crowded against the mullion; the 9 stands away from 4.1's place, unrecorded

- **Where:** STREET_SQUARE day, the left light: ink x 1022 to 1260, y 593 to 618 (1600: x 639 to 788, y 371 to 386).
  - It stands 487 mm from the left jamb's glass edge and 64 mm from the mullion's. It reads as pushed against the bar.
  - It is clear of every bar (GLS-02 is right) and reads whole by day at both cameras, and in night_lit and night_dark at STREET_SQUARE.
- **Cause:**
  - 4.1 places its ink centre at street x 29.625 (u 3375).
  - This M1 window's left light is glass from u 2350 to 3950, centred at u 3150.
  - 4.1 also places the 9 on the side door's fanlight (x 32.18). The build puts it on the shop door's fanlight, as Rita's approved 5. That is right, but no Judgement line records it.
- **WHOSE:** the kit (4.1's places for this shop); the builder (the unrecorded move).
- **EXACT FIX:**
  1. 4.1's SERVICE WASHES row: `x_street_m_of_ink_centre` 29.850 (u 3150), baseline z 2.05 kept. That gives 275 mm of glass each side.
  2. 4.1's 9: surface "shop-door fanlight", x 31.203.
  3. Add an L-line to NOTES.md for the 9.
  4. GLS-02 also asks that each row's ink stand at least 150 mm from the bars on both sides.

### 6. The two "orange" running lamps read pale yellow-white at street distance

- **Where:** STREET_SQUARE night_dark, (1490, 606) and (1266, 743).
  - Peak pixels are (207, 207, 157) and (208, 208, 145): a warm-white point with an orange halo.
  - In the room picture both lens cores sit at the highlight shoulder: (242, 242, 201) and (242, 242, 205).
  - The 0.9 W light 50 mm in front lights a patch of the cabinet about 0.14 x 0.20 m to near-burnt: blob mean (224, 175, 99) at picture (3029, 693, 59 x 82 px).
- **What it is:**
  - They read as small lit indicators, which carries the night.
  - The target asks for orange. A lamp lighting its own cabinet that much reads like a torch.
- **WHOSE:** the builder (the room).
- **EXACT FIX:**
  1. Lens emission colour linear (1.0, 0.18, 0.0) at strength 2 (was 7). Point light 0.3 W (was 0.9).
  2. ROOM-02 gains a test: in night_dark each lens's peak pixel has G at most 0.75 of R, and no pixel within 0.15 m of it is over 200 luma.
  3. Re-render night_dark and the night_dark street view.

### 7. The shop's real night is rendered from one street camera only

- **What:** STREET_30 exists in night_lit, the tests' state with the room lit, which this shop never shows. Its real night, night_dark, is rendered only at STREET_SQUARE.
  - The lobby slab (point 1), the box sign's face reading LAUNDERETTE, and the lit board seen at an angle are therefore judged at the shop's real night from one camera only.
- **WHOSE:** the builder (the kit's dark-shop gate: "one extra STREET_SQUARE view").
- **EXACT FIX:** add STREET_30:night_dark to the gate views of every dark shop (about 450 s at 32 samples), and a preview `steam_laundry-street-30-night-dark-<date>.jpg`.

### 8. The previews of a 14 October build are named 13 October

- **What:** all eight `steam_laundry-*-2026-10-13.jpg` were written on 14 October at 12:34, from frames rendered between 10:31 and 11:59 that day. `sw_ctx.DATE` is hard-coded to "2026-10-13". The morning pictures and Jafar's page date their pictures by name.
- **WHOSE:** the kit (`sw_ctx.py`).
- **EXACT FIX:** `DATE = os.environ.get("LEDGER_SW_DATE") or time.strftime("%Y-%m-%d")`. Rename this shop's eight previews to `-2026-10-14`, and X-PRV checks that the name's date equals the file's day.

### 9. The cloth in the baskets reads as smooth pastel lumps from the street

- **Where:** STREET_SQUARE day: x 1292 to 1475, y 860 to 892 (1600: x 808 to 922, y 538 to 558).
  - Two wicker baskets, which read as baskets, each with white, pink, mint and white lumps that could be buns or meringues.
  - The towel stacks beside them read as folded towels because of the weave and the folded edge.
  - This is the builder's own named shortfall.
- **What it is:** narrow. The baskets and the towels together still say "laundry" from 8.76 m. The close view judges the cloth itself.
- **WHOSE:** the builder.
- **EXACT FIX:**
  1. Give each heap the towels' method: the ambientCG Fabric020 weave on every lump, and a folded edge (a 0.30 x 0.25 x 0.04 folded garment as in L6) lying over each basket's lip.
  2. Replace the smooth top lump with two flatter, creased pieces 0.03 to 0.05 thick.
  3. TRD-01's "baskets of laundry" family stays as it is.

## The builder's named shortfalls, judged at street distance

| builder's shortfall (check file and NOTES.md) | my judgement |
|---|---|
| FAS-01c, 1.88 against 2.0 | **narrow (point 3)**. The board reads at 2.5 or more; the row measures the wrong plane |
| washers and dryers are scripted boxes | **not a point from the street.** Front-loaders with round doors, control strips and blank coin plates, the dryers in stacks of two: a plausible 1990 launderette's machines. No maker's name, no display. The close view judges the detail |
| the cloth in the baskets | **narrow (point 9)** |
| printed goods drawn by script; CC0 photographic prints owed | **not a point from the street.** The packets read as period card packets with invented makers. Owed, as the target says |
| the shop is dark at night; night_lit is only the tests' state | **right, per the target** (hours Mon to Sat 8:00 to 17:30, `lit_at_night` false). The night_dark view shows a lit fascia and box sign over a dark shop, with CLOSED on the door |
| the hard-edged darker block on the board at night "is the sign's shadow" | **narrow (point 2), and the cause is wrong:** it is 4.1's dead tube |
| room pictures at 48 samples | **not visible from the street**; 128 is owed on the PC |

## Shared, known

- (a) The stand-in lamp's pool as a burnt orange bar in the night glass: **not seen.** GLS-04 reads 0 px at both street cameras. I see no bar in night_lit or night_dark.
- (b) Hot orange top corners in night_dark: **not seen.** PIC-03 corners read 5.4 and 4.9, and the street night_dark glass shows none.
- (c) Glass parts of models dropped: **not seen.** The wall clock keeps its glass (DSP-07). Nothing else placed has glass.
- (e) Sheets leaning toward the glass: **not seen from the street.** The SERVICE WASHES card stands upright on its posts. Its lean is the close view's to measure.
- (f) CLOSED at night for a lit shop: **not this shop's case.** It is dark at night, so CLOSED in night_dark is right. The night_lit frames read OPEN.
- (g) Child-size furniture, chairs facing away, plastic curtains: **none in this shop.** No furniture or curtains. The baskets are at 1.0 (DSP-06).

## What is right

**The front:**
- It reads as a British Victorian parade's shopfront refitted in about the 1970s, which is what the target's alterations ask for:
  - cream render pilasters on plinths;
  - scroll consoles;
  - a timber cornice;
  - a lit box fascia (bronze returns, acrylic face, red trade panel and blue name);
  - a white square-tiled stallriser with a black base band;
  - a two-light bronze aluminium window with two toplights, the mullion carried up;
  - the shop door in a 300 mm recessed lobby;
  - the dark brown F1 side door at the door end (the viewer's left), with its raised-and-fielded panel, transom and fanlight;
  - three toplights over the shop door, with the 9 on its fanlight.
- Proportions are the kit's and Rita's: the same board, cornice, sill and window heights. It sits beside Rita's approved front and the Hook sheet's painted fronts as a plainer, brighter commercial refit.
- Nothing floats:
  - The box sign hangs on two plates on the brick, 50 mm clear of the cornice, over the right console (u 5755 to 5895), as 4.1 places it (FRN-11, FAS-02).
  - The SERVICE WASHES card stands on its two posts.
- Nothing is mirrored and no text reads backwards: the board, both box-sign faces (each seen from its own side), the glass row, the OPEN / CLOSED card, the hours plate and the display card.

**Rita's lessons, each checked here:**
- **Height map as normal map: no.** The fascia's normalTexture in the glb is RGB (127.5, 127.5, 255.0), sd under 1 (a flat, real map). The basket's is (127.4, 127.4, 253.2).
- **Textured primitive without UVs: none**, in either glb (I parsed both).
- **Coplanar black strips: none.**
  - The day frames' front pixels under luma 8 lie in thin lines of real shade: under the box fascia and the transom, and the corner of the lobby lining.
  - No strip stands beside either door.
  - FRN-10 agrees.
- **See-through slot at STREET_30: none.** At STREET_SQUARE there is one small notch (point 4).
- **Stand-in night light or glass visible: no.**
  - Head band at 250 or above: 0.
  - Mullion fronts 4.2 against the glass's 72.
  - GLS-03 p95 is 2.4 and 2.7. I see no ghosting at the display's edges in either night_lit frame.
  - The night_dark frame has the spill off.
- **Front row below the sight line: no.** The towel stacks, boxes and baskets stand above the sill from STREET_SQUARE (DSP-03 0.73 or more).
- **Fascia unreadable at night: no.** It is a lit box, and it reads at 2.6 or more at night.
- **Side door's fanlight shows the shop: no.** It shows a dark hall (luma 27.8 by day, 7.6 at night; FRN-09 0 of 560 rays).

**The window is glass with a lit room behind it by day, and an honestly dark one at night.**

| measure (glass of the two main lights, the gate's mask eroded 3 px) | STREET_SQUARE | STREET_30 |
|---|---|---|
| day, glass mean luma | 71.5 (p5 27, p95 183) | 70.8 (p5 25, p95 183) |
| day, the room's part / the display's part | 52.9 / 140.1 | 52.3 / 140.6 |
| day, under 3 / under 12 / 250 or above | 0 / 0.58% / 0 | 0 / 0.51% / 0 |
| day, largest uniform patch (9 px, sd under 1) | 3.9%: the plain back wall above the dryers, luma 42 | 4.1%: the room's plain upper wall in the left light, luma 39 |
| day, brick beside | 84.3: the glass is 0.85 of the wall, dimmer, as D5 has it | 84.1 |
| night_dark (the shop's night), glass mean | 16.1 (p5 3, p95 34), against brick 18.6 | not rendered (point 7) |
| night_dark, under 12 | 32% (drum interiors, floor, the unlit display; brightened 4 times, every part has content: no void) | |
| night_lit (tests' state), glass mean | 79.4 against brick 19.9 (4 times the wall) | 78.9 against 20.2 |

- **The target's floors are met:**
  - day composite at least 33 (my frame: room part 52.9; LIT-02's card-only figures 48.0 and 45.4);
  - night_lit at least 45;
  - night_dark 10 to 35 (16.1 in the frame; LIT-01's 14.8).
- **The day room is readable:** washers, stacked dryers, the parcel shelf on the washers, the right wall's clock and chart, and the T12 battens through the left toplight.
- **The night_dark room** is the machines in the street's sodium light, with the two lit lenses and a reflection of the window in each dryer's dome.

**The trade reads from the street.**
- The fascia (STEAM LAUNDRY / LAUNDERETTE / SERVICE WASHES / DRY CLEANING) and the box sign say it.
- So does the window: five stacks of folded towels, two baskets, the SERVICE WASHES card, washing powders and bottles, and the machines behind.

**Every word legible:**
- **At 100 per cent in the street frames:**
  - STEAM LAUNDRY, LAUNDERETTE, SERVICE WASHES, DRY CLEANING (board);
  - LAUNDERETTE (box sign, STREET_30);
  - SERVICE WASHES (glass);
  - 9;
  - OPEN / CLOSED;
  - MON-SAT 8-5.30 / SUN CLOSED (hours plate, at the limit);
  - SERVICE WASHES / LEAVE IT WITH US (display card);
  - HOLME, MEADOWS, ASHDOWN and, at the limit, BRIGHTWELL (packets).
- **At 400 to 800 per cent:** SOAP FLAKES, WASHING POWDER, BIOLOGICAL POWDER, FABRIC SOFTENER, LINDEN, WASHING SODA, LINDEN on the blue bottle. The price tickets and the washing-up bottles' small lines cannot be read from the street.
- **All are the project's own words or invented makers: acceptable.** No real firm's name, maker's mark, barcode or modern pack.
- **Content:**
  - The three small bottles are washing-up liquid and bleach in period squeeze bottles: no drink.
  - No gambling, no child, no toy, no person.
  - The machines carry no maker's name, and nothing is later than 1992.

## The check's rows: which I trust (70 counted, 3 n/a)

- **Trusted (55)**, measured on the real meshes, pictures or files and agreeing with what I see:
  - PIC-01 to PIC-06, X-NOISE, PRJ-01, PRJ-03;
  - SO-01 to SO-04, SO-06, SO-07, DSP-01 to DSP-07;
  - ROOM-01, ROOM-03, ROOM-04, ROOM-05;
  - INV-01 to INV-06, NEV-01, NEV-02, GLB-01;
  - FRN-01 to FRN-06, FRN-09, FRN-11, FRN-12;
  - FAS-01, FAS-01n, FAS-02, FAS-03;
  - GLS-01, GLS-02, GLS-05, LIT-06, TRD-01, CAM-01, X-PRV.
  - FAS-01n prints a blue mean of "256.0", which an 8-bit map cannot have. The glb's map is (127.5, 127.5, 255.0): the row is right and its printout is a slip.
- **Pass but do not prove all they say (4):**
  - FRN-07: an elevation cannot see the capital notch (point 4).
  - FRN-08: it saw the notch, but its text puts it on the wrong side of the pilaster and the row lets it pass.
  - FRN-10: true of the front, but its mask leaves out the shop door's glass, so the gate's slab in the lobby (point 1) is outside it.
  - ROOM-02: it proves the lamps' places and states, not their colour (point 6).
- **Fails on the wrong plane (1):** FAS-01c (point 3).
- **The cloud's stand-ins only (10):**
  - LIT-01 and LIT-02 are computed on the card's bake alone.
  - LIT-02b, LIT-05, LIT-07, LIT-08, PIC-05g, GLS-03 and GLS-04 are measured on gate renders, whose glass, lamps and 70 W spill are stand-ins set by eye.
  - PRJ-02 is the gate's own `trace`.
  - I repeated the glass, black-pixel and uniform-patch measures on the frames. I did not repeat GLS-03 and GLS-04 numerically: I compared by eye, and the reflection-off renders are still in the gate folder.

## What I cannot judge from these files

- **The game's glass:** the street and the sky in the panes (RULINGS 3 October), dirt on the glass, and the night hand-over. Here the glass reflects only the empty gate.
- **The game's light:** Lumen on the display, the game's spill and its pool (PC-02), exposure, the lamps' pools (the gate's two lamps are assumed), and the box fascia's and box sign's real glow (PC-08; here 4.1's emissive map at 0.5).
- **Wear:**
  - The front is spotless: clean cream render, bright white stallriser tiles, a fresh board. The Hook sheet's fronts are grimy.
  - The game's wear layer is owed (D53, PC-05). Until then this front is the brightest and cleanest in the parade.
  - The room is spotless too: no scuffs on the machines, no customers' bench.
- **What the game shows under the card through the shop door's lower glass, and whether the game's facade closes the capital notch** (points 1 and 4; PC-04).
- **The shop's real night from STREET_30** (point 7).
- **The pictures at true size and in motion:** TSR, the card's parallax as the player walks, and the 32-sample softness of the gate frames.

**Next:**
1. Fix point 1 (the gate's slab, and the owner's choice for the door's glass foot) and re-render the street views before anything goes to Jafar.
2. Then points 2 to 8, then 9.
3. None of this blocks the pass.
