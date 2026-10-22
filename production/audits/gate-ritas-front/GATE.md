# Rita's front's gate (his order of 21 October, item 5; his ruling of the day: Rita's front as the family's sample)

The game's own cameras, 2560 x 1440: the vignette film's hook camera by day and at night and the reverse view, and the pavement views of her window (-PageShots=shop/shopnight -PageShop=pawnbroker -PageShopX=17.0: left, square on, right and from across the road). One fresh reviewer (Opus) a view, each beside its last good picture (the hook views: F:/LedgerTools/gate/last-good/lamp-post-C; the pavement views: F:/LedgerTools/gate/last-good/1.1, 7 October, the old front at 18.0) and against the Hook sheet and the KCD2 frames. The brief every reviewer read: the cloud's known shortfalls (production/cloud-week/kit/shop-windows/NOTES.md, "Known shortfalls now") and the rule that new faults block and known shortfalls are listed. Pictures: F:/LedgerTools/gate/new/ritas-front (round 1) and .../r2 (round 2).

## Before the gate: my own check

- The front, the display and the room stood where the shop file puts them (the log: front at 1800,530,10 cm; display at 1702,527,70 cm); the street's own panes in the front's 19 pane places.
- Found and fixed before any reviewer: the room pictures missing (the game read only the checkout; now the game inputs on F: too, and staging lists them by name); the display a lone alarm clock (330 loose parts had imported as 173 meshes and the game took the first; joined, and the import now refuses loose parts); the velvet tiers pale pink (the white sheen tinted to the velvet's own colour).

## Round 1, 16:50

- Hook by day: FAIL. The three-ball sign hung across its bracket, so a walker looking along the street saw two balls. Watch points: the fascia's words barely read by day (RITA'S just, PAWNBROKER not, the left 5 dark); a dark grey grille rail under the transom with its end cap over the door frame; the display's left return a cream block.
- Hook at night: FAIL. (1) The window blown to pure white (1,547 pure-white pixels against the last good's 21), brighter than the street lamp; (2) the pavement in front darker than before.
- Cause of the night faults, found by filming without the window's light (-ShopSpillLumens=0): the window's light panel stood at the room card's top, inside the cloud's display box (its back, returns and head reach the card), lighting the box from a few centimetres and shaded by it; and every interior actor, the new front with it, was on the light's channel, so the front's white bars a few centimetres away burned ("neon strips", the fault of 1 October).

## Fixes for round 2

- The balls in the bracket's plane, at the cloud's source (sw_front.py), the front rebuilt (5 s) and re-imported. Try 1.
- The window's light: placed by the shop file in the window head just behind the glass (spill_y 5.33, spill_up 2.42), over the window alone (spill_x 17.03, spill_width 2.6); shop fronts kept off its channel (tagged LedgerShopFront); the display's returns a darker cream at the source (sw_display.py, 176/158/120, about half the light). Try 2 on the blown window, after the diagnosis.
- Measured at night, Rita's window (x 1160 to 1280, y 760 to 950): mean 80 (round 1: 110; the last good's old front 40), pure-white pixels in the frame 1,014; the pavement in front 53 (the last good 38).

## Round 2, 17:50

- Hook at night: FAIL. Fault (2), the pavement, gone: in front of Rita's 54.6 against the last good's 30.7. Fault (1) only partly gone: the fanlight row 632 pure-white pixels to 0, the fascia 537 to 0, but the glass itself still blown in three patches (the display's left return, x 1199 to 1216, y 814 to 862; the big vase; the china jug): 988 pure-white pixels in her glass against the last good's 4, its clear glass 1.5 times the fishmonger's and cooler. A second new fault named: the fishmonger's up-street pane lost its lit goods (mean 62 to 43). Tested: with Rita's window light off altogether (-ShopSpillLumens=0) that pane reads 30.0 (std 25.5), as now (33.6, std 25.6), and the last good's 49.3 (std 40.6) came only with the old light, which stood 3.7 m wide at the card's top and reached past the party wall. Not a fault of the new front: the old light leaked.
- THE BLOWN WINDOW SET ASIDE after two tries (CLAUDE.md; his rule that two means two): listed as a known shortfall in every view from here, in FINDINGS.md and on his page first. Research direction, not tried: the cloud's own lighting of the display (PC-07: two strip lights under the tiers' front edges, tipped back, 3000 K, the head light only for the top tier and the pavement), measured in lumens on the PC, and the glass's night exposure against the fishmonger's.
- Hook by day: PASS. The balls hang in the bracket's plane, two side by side along the arm and the third below, joined by their rod; no seam or void at either joint (the dark strip at the left is the TO LET shop's own console and pilaster end, the reverse view confirms); no clipping, floating or mis-scaled goods. Shortfalls listed: no wear; the paint uniform and a lighter pink than FRESH FISH's maroon; the balls matte mustard, not gilt; by day the display barely reads under the street's own mustard reflection (in the last good too). Watch points: PAWNBROKER (5 px) and the glass words (6 px) do not read at this distance; only the left 5 shows (the right one behind its console); a grey rail across the transom (the grille's top track); a faint seam round each ball; a few pale specks on the fascia.
- From the pavement by day, from the left: PASS. Every 640 x 480 tile looked at at 100 per cent and the joints at 200 to 500: the pilasters' edges closed (no sky or void in the bay's outline), both neighbours' junctions closed, nothing floating or clipping, the gilt words the right way round, the room picture meeting the display and the door-end wall without a step. Shortfalls listed: CG-clean joinery and an even oxblood with a fine speckle reading as sandpaper; the goods in tidy rows, not a crammed 1990 window; the models' own glass missing. Watch points: the glass's stepped reflection of the kerb under the middle tier (in the last good too); a 24 mm oxblood filler between the two door frames (the cloud's drawing); a dark slot where her right pilaster meets FRESH FISH's (no sky); pale chips on the fascia; the grille's box and track with no gate folded at their ends.
- From across the road by day: PASS. The balls hang on their rod, not floating; the cornice and plinths meet the street cleanly; all lettering legible; the scale right (doors about 1.95 m, the front about 3.4 m to the cornice top, the fascia in line with its neighbours). Shortfalls listed: factory-clean joinery, no grime in the corners or under the cornice; the balls matte yellow, not gilt; the grille's empty rails. Watch points: the kick plate now a dull brown; the fanlight reflects a sign across the road as smudged letters; near-black 6 px slits where her pilasters meet the neighbours'; the bracket thin and high, its rod near invisible against the TO LET fascia.
- From the pavement at night, square on: FAIL. (1) The camera stood 2 cm from the phone kiosk's side glass (the shot's fault: square on at street x 17.0 is inside the kiosk; the old window's 18.0 was clear); (2) a blocky "camouflage" of 8 to 15 px squares on the brass vase and the projector's side panel under the window's light (the textures themselves are smooth 1k Poly Haven maps with linear sampling, checked in the glb); (3) the brass vase looks a metre tall: it is Poly Haven's own scan at its real 0.694 m (its source glTF), standing on the top tier: a placement watch point, not a scale fault. The burned whites (the set-aside) worse here: 18,987 pure-white pixels.
- The fixes after the square night view: (1) the shot moved clear of the kiosk (-PageShopX=17.6: square on at 17.6, 0.64 m from its edge; nothing occludes the window from there). (2) The camouflage, try 1: the window light's shadows off (the display, one mesh, might have shadowed itself in the light's coarse local shadow map): the camouflage stayed and every white in the display burned (154,351 pure-white pixels), so undone. Diagnosis: the vase's material has the right maps (checked in the editor), the camouflage shows with Lumen's reflections off too, and the vase's normal map in the cloud's display file is a 512 px JPEG of 13,953 bytes (its 1k source 78,223): JPEG's 8 x 8 blocks, which a glossy metal shows as dents. Try 2: the cloud's display exported at JPEG quality 100: no change (the same bytes came through; the 512 maps are not re-encoded there). SET ASIDE after two tries: listed in FINDINGS.md; next, the goods' maps made lossless from their 1k sources.
- The reverse view by day: FAIL. A sliver of sky (a flat 242, about 4 x 28 px) in the joint between her right pilaster and FRESH FISH's, where the old front's own pilaster had closed it; the right-hand pavement view showed the same slit. The cloud's own owed point PC-04: its pilasters stop 30 mm short of the bay's edge (50 at the consoles and cornice). Fix, try 1: a brick pier behind each end pilaster, 80 mm in from each edge (terrace-front.py, cloud_pier_l/r; its self-test now 171/171): the reverse view closed, the right-hand view still showed a hair of light at the neighbour's side. Try 2: each pier reaches 60 mm past the bay's edge, behind the neighbour's own pilaster: closed in both views (F:/LedgerTools/gate/new/ritas-front/r5). Watch points: the shop's name no longer reads from this side (the balls hang in front of it); the glass words too small at this distance; the grille's track a hard dark bar.
- From the pavement at night, square on at 17.6, round 3: FAIL, on the window's light again: the middle shelf's white and pale goods turned red by the red velvet's bounce (25,231 strongly red pixels; the velvet's red channel clipped over 101,847 pixels against the last good's 22,013), the rings and chains reading black or orange at night (the old front's did too), and 123,456 pure-white pixels. One cause with the set-aside: the window's light is far too strong for the goods this close. NOT PASSED: the close night view of her window is listed with its lighting set aside (FINDINGS.md); the next direction stays the cloud's strip lights at a measured, lower strength. Watch points: the boombox's aerial a ruler-straight white line; the projector's lead dead straight; repeated goods in mirror places.
- The reverse view by day, round 2: PASS. The joint shows brick only, the sky sliver gone; nothing floating, clipping or missing at 300 to 1200 per cent. Watch points: the shop's name hidden behind the balls from this side (normal for such a sign); a faint seam round each ball at 400 per cent; the right-hand 5 a slit side-on.

## Where it stands (21 October, 19:50)

- PASSED: the hook camera by day; the pavement by day from the left; the whole front from across the road by day; the reverse view by day.
- LISTED, NOT PASSED, set aside after two tries each (FINDINGS.md, shown first on his page): at night her window's light is far too strong for the goods (in the hook camera her glass burns white in three patches; close up the whites burn, the red velvet clips and stains the pale goods red, the rings read black); close up her glossy goods show the cloud's JPEG blocks. Next direction for both: the cloud's own strip lights under the tiers at a measured, lower strength, and the goods' maps lossless from their 1k sources.
- Known shortfalls listed throughout: no wear; the balls matte, not gilt; PAWNBROKER and the glass words too small to read from the hook camera; tidy rows of goods rather than a crammed window; the models' own glass missing; the grille's empty rails.
- These views (round 5, and round 3's close night) are now Rita's last good pictures: F:/LedgerTools/gate/last-good/ritas-front. Packaged and walked: owed to tonight's package.

## 22 October: the night light (his order: "work on Rita's night light")

**The change.** The cloud's own design for the display's light (NOTES.md rule 4, PC-07), in the game:
- two strip lights, one 8 mm under the front edge of each tier's board, 3.20 m long, tipped 30° toward the back, 3000 K, on the display's channel only, with no shadow and no highlight of their own (VignetteShot.cpp SpawnDisplayStrips; shop-interiors.json display_lights);
- the head light lowered to light only the top tier and the pavement.

**The strengths, measured** in the game's square-on night camera against the cloud's burnt-pixel bar (any channel at 250 on at most 1% of the window):

| strips (lm) | head (lm) | top tier burnt | middle tier burnt | bed burnt |
|---|---|---|---|---|
| none | 350 (before) | 10.7% | 10.0% | 20.6% |
| 40 | 160 | 5.6% | 26.9% | 41.7% |
| 20 | 120 | 4.2% | 21.1% | 38.2% |
| 10 | 100 | 3.5% | 9.6% | 28.1% |
| 0 | 100 | 3.5% | 3.5% | 0.3% |
| 3 | 80 | 2.8% | 3.5% | 1.8% |
| 1.5 | 80 | 2.8% | 1.8% | 0.3% |
| **1.5** | **60** | **1.8%** | **0.01%** | **0.13%** (the window as a whole 0.6%) |

These are game lumens, not a shop's: the night exposure sets the scale.

**A fault in the camera, found and fixed on the way.** The first hook review failed the view because the whole frame came out 54% brighter than "before". Three night runs of one street, shot 6 s after the clock's jump to 22:00, gave the frame's mean 44, 56 and 68: the night's global light was still settling. Night shots now wait 30 s (CrimeProbe.cpp, PageShotSettle). Two runs then gave 16.2 and 16.2, as the vignette film's own night (15.6). The glass was rebaked with the settled night, and every view was reshot before and after.

**The gate** (one fresh reviewer, Opus, a view, each beside the same camera's before; the brief: F:/LedgerTools/gate/new/ritas-night-2026-10-22/BRIEF.md):
- **Hook camera at night: PASS.** In her glass, burnt pixels went 11.5% to 0% and the mean 134 to 88, just below the fish shop's 98.5 and the launderette's 108. The white pool on the pavement is gone. "A warm lit 1990 shop window, neither too dark nor a light box." (The first hook review, on unsettled shots, failed it for the whole frame's change; that was the camera, fixed above.)
- **Square on: PASS.** Burnt pixels went 8.2% to 0.2% of the frame. The goods show their own colours (the radios cream, the clocks green and cream), and the red staining is gone.
- **From the left: PASS.** Burnt pixels in the window went 89,155 to 4,487. The staining is gone.
- **From the right: PASS.** Nothing in the window clips; the pavement under it went 216 to 105.
- **From across the road: PASS.** The window reads warm and lit below the fish shop's glare; the floodlit pavement is gone (164 to 60).

**Listed, not failing:**
- the white vase's top and the projector's pink reel still clip a little under the head light (about 7% of the right vase);
- her gilt letters read dull bronze at night from the side, and the door's opening hours can no longer be read from across the road;
- the strips stop short of the display's left end, so the low tier's back-left corner is darker;
- the kiosk now reads unlit inside;
- older, and not hers: the fish shop's bright window throws almost no light on its own pavement.

The earlier known shortfalls stand.

**Last good pictures:** F:/LedgerTools/gate/last-good/ritas-front (cam_hook-night and the four pawnbroker *-shopnight, 22 October). **Seen packaged** (711cc3c, the played copy, 22 October 14:20): the square-on night view measures as the editor's within one level (burnt 1.81, 0.01 and 0.13 per cent by tier; the log names the head light at 60 lm and two display strips). Walked by the AI tester: owed to tonight's walk.

## 22 October: the front's wear at the foot, try 1 (failed; set aside for research)

**The try.** Her front's painted slots (oxblood, the cream joinery, the buttermilk side door) were drawn in the street's own surface material, in their own colours, with the street's foot wear (WearAmount: dust up about 0.4 m with a ragged top), as the street's painted fronts wear (VignetteShot.cpp SpawnShopFront, "worn_paints"; make_base_material.py WEAR_PARAM).

**The gate** (one fresh reviewer, Opus, a view, beside the same camera's before; brief F:/LedgerTools/gate/new/ritas-wear-2026-10-22/BRIEF.md):
- **Square on by day: PASS**, with no evidence either way: the foot is out of frame.
- **From across the road by day: FAIL.**
  - The stallriser and pilaster bases read as splash dirt, matching the neighbours'.
  - But the side door's foot reads as frost or foam: pale blotches as light as the cream, grey between them.
  - The shop door's frame shows marble-like veins.
  - The oxblood shifted colour over its full height: ΔE 6 on the pilasters, 10 on the cornice.
- **From the left by day: FAIL.** The doorway's wear reads as marble veining, not dirt.

**The two causes, measured.**
1. **The street's dust on pale paint.** The material's dust is a cool pale grey through a 3D noise. On dark oxblood it reads as dirt; on cream and buttermilk it reads as frost, foam or veins.
2. **The street's material draws the same flat colour darker and redder, by different amounts from view to view.** On her oxblood, measured in linear light:
   - from across the road, red 8%, green and blue 17% darker;
   - from the left, only 2 to 6%.
   
   The two views measured different parts of the front, so the difference may be by angle or by place (a large-scale variation in the material, for example); not separated. So one tint is not known to correct it. The cause is not found: the material's specular is the glTF's 0.5, and its roughness is set from the same 0.45.

The game is back on the front's own paints (the shop entry restored; the code stays, off without "worn_paints").

**Next, after research:**
- why the street material and the imported material differ on the same colour (compare the two material graphs and the look's colour chain);
- a grime for pale paints (warm, darker, damp-edged, as the reviewers describe real door feet), or wear baked into the front's own model in Blender.

The cloud's W1 items (the band round the lever, the chipped rails and the sill's nose) are still owed.
