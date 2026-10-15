FAIL

# Rita's shop, the CLOSE view: fresh review, try 1 (cloud week 42, unit 7 part 2, 13 October 2026)

Reviewer: a fresh reviewer who did not write the target or build the shop. One view only: CLOSE_35 and CLOSE_35_B, day and night_lit. I did not read the street view's review.

Read: CLAUDE.md, RULINGS.md (2 Oct, 1 Oct, 9 Oct as briefed), the build's NOTES.md, TARGET.md sections 3, 4 and 6 (and 8 for the door), TARGET-REVIEW.md, sw_gate.py, sw_display.py, the parts of sw_room.py and of tools/art-recipes/shop-room.py named below, and the check's rows (checks/check_ritas_v1.json).

Looked at: the two close previews; the four close renders (2560 x 1440) in SCRATCH/shop-windows/gate at 100 to 300 per cent; the baked cards; the room pictures; the before-and-after sheet; the approved door picture rita-day-kit-2026-10-06.jpg; the dated photograph P1.

Measured: the parallax; the clipped and black pixels; every display piece's box against the tiers, the pedestals and the other pieces (display_work/display_items.json).

Tested: four night fixes and one day fix, each a 960 x 540 render at 16 samples from a copy of sw_gate.py in my scratchpad. Nothing in the repository or SCRATCH was changed.

**In short:** the projected room works. It moves exactly as the game's rule says, and it reads as a deep, lit room.

The near metre fails, and the near metre is what this view is for:
- goods are buried inside their own pedestals, and two vases pass through a shelf;
- the window has no rings, chains or wristwatches and reads as a sparse antiques shelf, not a pawnbroker's;
- from CLOSE_35_B, a third of the window shows a black slab instead of the room.

At night, the display's light is itself visible as a white arc. The front has two open slots beside the side door.

Five faults, 13 narrow points.

## Faults, worst first

### 1. Goods buried in their pedestals, and vases through a shelf

- **Where (positions in the 2560 renders; the 1600 previews are 0.625 of these):**
  - **Radio cassettes.** Both portable cassette players (the display's only radio cassettes) stand 92 per cent inside other pieces' pedestals and the step. Only their black tops show, as a "black pad":
    - one under the binoculars: CLOSE_35 day (1265-1470, 1040-1120); CLOSE_35_B day (1280-1420, 1020-1120);
    - one under the red flashlight, whose pedestal it pokes out of at the side: CLOSE_35_B day (1480-1500, 1020-1110).
  - **Pocket watches.** Both `pocket_watch` pieces are wholly inside the two Camera_01 pedestals (CLOSE_35_B day, 50-750, 1120-1400). They cannot be seen at all.
  - **Magnifying glass.** More than half of it is inside a camera pedestal and the step. Its red rim shows under the pedestal at CLOSE_35_B day (560-620, 1360-1400).
  - **Cigarette case.** One end is inside the measuring tape's pedestal.
  - **brass_vase_01** stands on the middle tier and passes through the top tier: CLOSE_35 day (1830-2000, 490-1020). The tier cuts it at y ≈ 750.
  - **brass_vase_02** (the ewer) does the same: CLOSE_35 day (2210-2400, 630-1090). Its neck also runs through standing_picture_frame_02: their boxes overlap by 107 x 96 x 179 mm.
  - brass_vase_01 and antique_ceramic_vase_01 overlap by 41 mm.
- **Measured** from display_items.json against the boxes that sw_display.py builds:

  | piece | inside | share of its height inside |
  |---|---|---|
  | pocket_watch (both) | Camera_01 pedestals | 100% |
  | portable_cassette_player (both) | pedestals and step | 92% |
  | magnifying_glass_01 | pedestal and step | 100% (over half its area) |
  | cigarette_case | tape pedestal | 100% (45 mm of its length) |
  | brass_vase_01, brass_vase_02 | w 0.75 tier | pass through it |

- **Whose:**
  - **The builder:** sw_display.py puts a pedestal (0 to 0.12 high, the piece's footprint plus 15 mm) under every w 0.12 piece that overhangs the step, without looking at what lies on the bed there. The top tier runs the whole 3.35 m.
  - **The target:** its own zones overlap in volume. In section 4.5:
    - brass_vase_01 is at w 0.40-1.10 and antique_ceramic_vase_01 at w 0.75-1.20, over u 2.40-2.70;
    - brass_vase_02 is at w 0.40-0.95 and standing_picture_frame_02 at w 0.75-1.00, over u 2.90-3.10.
- **Exact fix:**
  - **(a) No pedestals.** Every w 0.12 zone moves onto the step: v 0.26 to 0.52, each piece turned so its longest side runs along the window. The bed's front strip, v 0.04 to 0.22, carries only bed pieces (w 0). This is also the strip that fault 2 fills.
  - **(b) Tier rule:** a piece on the w 0.40 tier is at most 0.32 tall. Taller pieces stand on the top tier (w 0.75, up to the target's 1.55). In the target's table:
    - brass_vase_01 to u 2.75-3.05, w 0.75-1.45;
    - brass_vase_02 to u 3.05-3.30, w 0.75-1.30;
    - standing_picture_frame_02 to the w 0.40 tier, u 2.50-2.80.
  - **(c) A new check DSP-03, failing the build:**
    - no display mesh (piece, tier, post, step, bed, ticket) intersects another (BVH overlap test, 2 mm tolerance);
    - every piece shows at least half its silhouette from CLOSE_35 or STREET_SQUARE (an object-index pass).

### 2. The near metre does not read as a pawnbroker's window

- **Where:** both close views, the whole display.
  - CLOSE_35 day, preview:
    - The middle tier (420-1600, 505-700) holds a mantel clock, two alarm clocks and the two brass vases over 3.25 m.
    - The top tier holds six vases, a china horse and two framed prints.
    - The bed's front row (430-1250, 680-800) is single pieces on navy boxes.
  - Across the four close renders there is not one ring, chain or wristwatch. The four pocket watches are 47 mm discs on the bed, and two of them are buried (fault 1).
  - Vases and ornaments take most of the display's visible area. The glass above them says WATCHES and JEWELLERY.
  - The display is open shelving with long empty runs. You see the room's floor through it between the tiers.
- **Whose:**
  - **The target:** 4.5 says it "Keeps" the approved pawnbroker-display.glb, but its table of 31 pieces has no jewellery.
  - **The builder:** sw_display.py's docstring says the approved display's ring trays, watch pads and chains "are not made again". The approved recipe (tools/art-recipes/shop-room.py, the front row before "THE MIDDLE AND BACK STEPS") was written to fix exactly this. Its comment reads: "THE FRONT ROW, on the bed, CRAMMED as a pawnbroker's was (the first build stood each thing alone on bare velvet)". That lesson is lost again.
  - CLAUDE.md says to reuse what exists or record why it is replaced; there is no entry in DECISIONS.md.
- **Exact fix:**
  - **(a) The front row.** Restore the approved front-row generator: `ring_tray`, `watch_pad`, `chain`, `wristwatch`, `pocketwatch` and the crammed loop at pitches 0.255, 0.275 and 0.16. Lay it along the bed's front strip, v 0.04 to 0.22, from u 0.14 to 3.20.
    - It gives at least 4 ring trays of 24 rings, 4 watch pads of 8 wristwatches and pocket watches, and 2 chains.
    - The cigarette case, the lighter, the spectacles and the magnifier go in among them, as the approved loop places them.
  - **(b) The target's table.** In 4.5, add `script:ring_tray` n 4, `script:watch_pad` n 4 and `script:chain` n 2, each in zone u 0.14-3.20, v 0.04-0.22, w 0.00-0.03. Add the three to `inventory.scripted` with the approved why: "a watch three centimetres across is modelled, not scanned" (1 October).
  - **(c) The middle tier.** It takes the stock a pawnbroker's window showed, at real size (scale 1.0), from models the room already uses: boombox 1, cassette_player 2, vintage_binocular 1. The portable cassette players stand here too, now that they are out of the pedestals.
  - **(d) The top tier** keeps at most three vases: antique_ceramic_vase_01, ceramic_vase_01 and one brass.
  - **(e) A new check DSP-04:** on the bed, the step and each tier, no free run along the window longer than 0.20 m.

### 3. From CLOSE_35_B a third of the window is a black slab, not the room

- **Where:** CLOSE_35_B day, the far light, x 1830-2050, y 100-1020 (preview 1145-1280, 60-640).
  - The room's plaster stops on a vertical line at x ≈ 1820. To its right the glass shows a flat dark surface.
  - Its mean luma is 36, and only the stand-in's reflection of the trees lifts it that far; the room beside it is at 75.
  - At night the same place is a dark grey block behind the lattice (CLOSE_35_B night, preview 1125-1280, 95-310).
- **Why:**
  - From CLOSE_35_B, the glass from street x 15.40 to 16.12 looks past the card's low-x edge (15.35). That is 0.72 m of the far light's 1.04 m.
  - Those rays go into the 0.61 m gap between the glass and the card. The gap's side is sw_gate.py's `reveal_r`, base colour 0.02.
  - LIT-02 measures only CLOSE_35, and only on the room-only composite, so it cannot see this.
  - The CLOSE_35 side is safe, because the card runs on behind the doors to x 20.65.
- **Whose:**
  - **The target:** sections 3 and 4.4 do not say what stands between the glass and the card at the window's ends.
  - **The builder:** made the reveals black.
- **Exact fix:**
  - **(a) Target, section 3 and 4.4.** Add a return wall at each end of the window zone:
    - from the back of the glass to the card plane (0.61 deep), over the card's full height (street z 0.65 to 3.05);
    - finished as the room's side wall: plaster (0.95, 0.86, 0.66) above the dado line, brown dado (0.42, 0.27, 0.17) below it (1.0 m above the room's floor = street z 1.65);
    - part of the display glb, so the game has it too.
  - **(b) Builder.** `reveal_l` and `reveal_r` take that finish. In the gate, make each an emission of the room picture's own side-wall front column (picture u 0-8 px for one side and 4088-4096 px for the other, at the same v), times the state's brightness, so it meets the card without a step.
  - **(c) Check.** Run LIT-02 also on the rendered CLOSE_35_B and STREET_30 frames, with the glass reflection off. At most 1 per cent of the window-glass pixels may be under luma 12.

### 4. At night the display's light is seen as a white arc, and the window frame burns

- **Where:**
  - **CLOSE_35 night_lit:**
    - a white arc from about (1090, 110) to (1060, 400);
    - a clipped white band under the window head, x 480-1600, y 120-180;
    - the frame's inner faces (jambs, mullions, head) burnt white.
  - **CLOSE_35_B night_lit:** the same arc at (1300-1550, 80-250).
  - In each night frame, 3.3 and 3.1 per cent of the pixels are at luma 250 or more.
- **Cause (tested):**
  - The arc and the band are the spill's rect light itself. It hangs 10 mm behind the glass, visible to camera and transmission rays.
  - The burnt frame is the spill lighting the window frame. The game keeps the frame off that light's channel. shop-interiors.json's lit_note says: "the window bars are not on that channel, so they no longer flare".
  - sw_gate.py read "the window bars" as the night grille's lattice. The lit_note was written on 1 October, before the grille existed.
  - The builder's shortfall "the window frame is bright at night ... the game's own light will light the frame differently" is this misreading, not the game.
- **Test result:** in my copy, the spill invisible to camera, glossy and transmission rays, with the frame out of `spill_receivers`.
  - The arc and the band are gone.
  - The clipped share falls from 3.4 to 0.5 per cent. What is left is the white vases and the white print.
  - The display stays lit.
- **Whose:** the builder.
- **Exact fix in sw_gate.py, after the spill is made:**
  - Make the spill invisible: `ro.visible_camera = False`, `ro.visible_glossy = False`, `ro.visible_transmission = False`.
  - Leave out of `spill_receivers` the window frame and the door frame: `win_*`, `frame_*`, `door_jamb_*`, `door_frame_head`, `band_*` and `sil_sill`. The lattice stays out as now.
  - Re-measure LIT-05 afterwards; it was 47.9 against a floor of 45.
  - Add PIC-05's limit (at most 1 per cent at 250 or more) to the gate's rendered review frames.

### 5. Two open slots beside the side door

- **Where:** CLOSE_35 day.
  - A pure black slot (luma 0 to 2) runs the full height between the side door and the shop door's left jamb: x 268 at y 300, 296 at y 600, 324 at y 900 (preview x 167 to 202, y 190 to 560).
  - A thinner one (luma 0 to 15) runs between the left pilaster and the side door (x 128 to 195).
- **Cause:**
  - The side door's leaf (`leaf_frame`, 838 wide) sits between fillers that stop at front-model x −2.626 and −1.730, leaving it at −2.597 to −1.759.
  - That leaves two open slots, 29 mm wide and 100 deep, onto the unlit space behind the front.
  - FRN-07 draws the front square on, where parts further back cover the slots, so it passes.
- **Whose:** the builder. F1's own frame jambs were left out.
- **Exact fix:**
  - Put back F1's frame jambs, 28.6 a side (838 + 2 x 28.6 + 2 x 24.4 = 944), or widen each filler to 53.0 mm (x −2.650 to −2.597 and −1.759 to −1.706). Either way: d 0 to 100, z 25 to 2400, white joinery (226, 224, 214).
  - FRN-07 also looks from CLOSE_35 and CLOSE_35_B: render the front alone against a white emissive backdrop. No backdrop pixel may show inside the front's outline.

## Narrow points (each with its fix; none blocks alone)

1. **The day glass shuts the sky out of the display.**
   - The gate's glass is a full Glass BSDF by day, and Cycles stops shadow rays at it. The display gets no direct sky light.
   - The pedestal tops render near black (CLOSE_35_B day, 60-750, 1140-1370), and the window bed reads darker than the room behind it.
   - Tested: a Light Path "Is Shadow Ray" mix to a Transparent BSDF on `gate_glass`. The display brightens and the light falls off front to back, as in a shop. The room's glass already does this (NOTES judgement 16).
   - Builder. The game's Lumen is owed.
2. **The room's walls are bare at close range.** This is the builder's known shortfall, caused by the target's goods table.
   - In CLOSE_35 the left board is the largest part of the room seen. It is plain pegboard with 90 ticket specks, 2 clocks, 2 prints and a notice (preview 360-740, 170-420). The right board is about 15 per cent covered.
   - Fix, target 4.4: cover at least 60 per cent of each board with goods at real size and at most 0.08 off the wall.
   - Left board: add 4 wall_clock, 3 hanging_picture_frame_02, 2 ornate_mirror_01, 2 Ukulele_01, and 40 scripted watch-and-chain cards (0.10 x 0.14 x 0.01, ticketed).
   - Right board: double each tool's count (pipe_wrench 2, adjustable_wrench 4, combination_wrench 6, pliers 6, handsaw_wood 4, cross_pein_hammer 4).
3. **Stock-wall scales, 0.45 to 1.45** (known; placed.json).
   - A boombox at 0.66 next to a cassette_player at 1.31 makes the boombox the size of a cassette recorder.
   - Camera_01 is 1.24 and mantel_clock_01 1.45 on the wall, against 1.0 in the display.
   - Fix:
     - scales only from 0.9 to 1.1;
     - the TV tiers 0.45 apart (z 1.35 and 1.80), so television_02 stands at 1.0;
     - each shelf filled by count, not by scale: the target's counts raised until the tiers run shoulder to shoulder at 1.0, about 12 more pieces from the same pool.
   - Builder (scales) and target (counts).
4. **The room is seen from 1.05 m above its floor.** For the target's owner, all shops.
   - The box's floor is the window bed (street z 0.65), so the eye (1.70) is 1.05 above it.
   - The counter's top sits on the horizon, and the back door's head is 0.95 above the eye instead of 0.40.
   - Fix (section 3 and shop-interiors.json):
     - the card's bottom to the footway (street z 0.10), H 2.95, pictures 4096 x 2280, `trace` unchanged;
     - from every review camera the bed and stallriser hide the card below about street z 0.67 (computed from CLOSE_35's eye over the bed's back edge), so nothing new shows.
   - The counter's case is still seen low from the render camera. Rake its velvet bed 25 degrees up toward the back so the jewellery (now "a row of points", known) shows as rings.
5. **The counter's parallax.** By the method, the counter's top is painted on the back wall and moves with it. Its foot is painted on the floor.
   - So between CLOSE_35 and CLOSE_35_B the counter's front shears rather than moving apart from the stock wall: its top is about 35 px off (the target's tolerated 0.60 class: 38 by the target, 34.5 by its review).
   - At CLOSE_35 it is mostly behind the top-tier vases.
   - Accepted. If the room is rendered again, move the CASH LOANS card from the counter's front to the back wall above the counter, so the card moves true.
6. **The display's furniture reads as plain computer-made boxes:** flat colour, sharp edges, square black posts.
   - Fix: velvet as a Principled BSDF with sheen weight 0.8 and sheen roughness 0.3; base colour varied ±5 per cent at 0.05 m; a CC0 fabric normal map (ambientCG) at strength 0.2 and a 0.25 m tile.
   - A 4 mm bevel on every tier, step and bed edge.
   - The posts become 12 mm round rods, brass or black lacquer.
   - Builder.
7. **The two standing frames' invented prints read as flat clip-art.** They are the largest pictures in the near metre: CLOSE_35 day (2135-2360, 570-785), CLOSE_35_B day (120-345, 570-785).
   - Fix: a crop of a CC0 Poly Haven HDRI of a coast or harbour, tone-mapped and cut to 3:4, saturation 0.7, a slight warm cast, paper grain, a 6 mm white mount, no person. Give it a catalogue line.
   - Builder; the target allows "invented print".
8. **The bell** is there on its spring strip with its clapper, but its body is a straight cone and reads as a small lampshade (CLOSE_35 day, 570-605, 380-480, seen past the door's jamb through the window glass).
   - Fix: a bell profile with a crown loop and a dome to a flared lip, 70 mm across the lip, 55 high, 3 mm wall, the clapper showing under the lip.
   - Builder.
9. **Paint and wear.** The shop door, its frame and the window joinery are even, clean gloss. P1, the dated photograph that D1 rests on, shows dirt at the foot, chipped rails and grime round the handle.
   - The wear is owed to the game's seeded wear layer (D53; look development is Unreal's), but target 4.3 names no wear for the joinery.
   - Fix, target 4.3, applied by the D53 layer:
     - foot grime to 150 mm (paint 20 per cent darker, roughness +0.15);
     - a band 150 mm round the lever, 10 per cent darker;
     - chipped edges on the bottom rail, the lock rail and the sill's nose (chip mask 3 per cent).
10. **The room pictures carry an unrecorded highlight shoulder.** sw_room.py `rolloff` compresses everything above 232 so that 255 becomes 242. PIC-05 (at most 1 per cent at 250) therefore cannot fail. NOTES does not mention it.
    - Fix: measure PIC-05 on the render before the shoulder, and name the shoulder as a Judgement in NOTES and in the target's picture fields.
11. **64 samples** (known). The final pictures go to 128 on the PC before his page, as the target says.
12. **Files out of git** (known). The three glbs and the 4096 pictures are rebuilt by script, which is fine. But nothing in git names the versions reviewed.
    - Fix: a manifest beside NOTES.md giving each file's bytes and sha256 (ritas_front.glb, ritas_grille_night.glb, ritas_display.glb, the three pictures).
13. **The ceiling battens read as broad flat panels at close range.** Their 0.045 m drop is painted on the ceiling, stretched about 0.2 m in depth (CLOSE_35 day, 1000-1700, 20-290).
    - Fix: none now. If the room is rendered again, make the fittings 0.025 deep in all.

## What is right

- **The projection follows the game's rule exactly.**
  - The card's centre samples the picture 1322.1 px (of 4096) apart between CLOSE_35 and CLOSE_35_B. My own ray-box gives the same u (0.17180 and 0.49459), so PRJ-02 is confirmed.
  - One stock-wall point, picture pixel (1630, 635), should land on the card at column 1790.2 from CLOSE_35 and 1133.5 from CLOSE_35_B. That is 656.7 card px, or 1.36 m on the card for 2.0 m of eye travel (= 2.0 x 4.5 / 6.62).
  - Matching that patch in the gate's baked cards finds it at offset (0, 0) in both (correlation 0.96 and 0.97). A second point, the back door's pane at (2842, 802), is at (0, 0) and (−1, 0). So PRJ-03's bake is confirmed too.
- **The room reads as a deep, lit room, not a flat picture.**
  - The stock wall, the back door and the side boards shift correctly between the two cameras.
  - There is no seam where the display's bed meets the room's floor: the 0.12 m step hides the 0.06 m gap.
  - The room is sharp at 4096 pixels.
- **The door matches the target and the photograph:**
  - glass from 871 with the bar at 1423;
  - the lever on the viewer's left stile;
  - the brass letter plate in the lock rail;
  - the green OPEN card on its suction cup by day, a red CLOSED card at night;
  - the gilt hours plate;
  - the gilt 5 on the fanlight;
  - the band above the doors (fanlight, transom, three toplights, panel, head);
  - the bell on its strip with its clapper;
  - the brass kick plate.
- **The Poly Haven models read as real objects:** the mantel clock, the alarm clocks, the cameras, the compass, the brass vases and the binoculars.
- **No maker's name or modern mark is legible** in the close views at 100 per cent. I looked closely at the cameras, the compass, the lighter, the measuring tape, the flashlight, the clocks, the till and the stock wall at 200 per cent.
  - Distinct legible words: OPEN, CLOSED, MON-SAT, WED, SUN, WATCHES, LOANS (cut to "…ANS" by a bar in CLOSE_35_B), CASH (from CASH LOANS on the counter), and "No." on the tickets.
  - Numbers: 5, 9-5.30, 9-1, and the tickets' four-digit numbers, which are soft.
  - All are the project's own and acceptable.
- **The content rule holds.** No drink, gambling, child or weapon, and nothing after 1992. The tobacco items (the cigarette case and the lighter) are allowed.

## What I cannot judge from the files

- **The game's own light and glass:** the glass's reflections and its Fresnel hand-over at 61 degrees, Lumen's light on the display, the exposure, the card under TSR, and the frame time.
- **The far end in the game.** Whether the game shows the same black gap at the window's far end depends on what the street model has between the glass and the card, and I could not see that in these files.
- **Wear, grime and wet**, which come from the game's own layers.
- **The bell's swing and sound.**
- **The new door against Jafar's open question** on the glass foot (871, 600 or about 1000). That is his choice.
