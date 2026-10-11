# Shopfront parts and Rita's front (kit unit 3.2): build notes

11 October 2026, cloud week 42. Built by script from `production/cloud-week/targets/shopfronts/target.json` (the second try with the fixes of section 18, not re-reviewed). Nothing committed or pushed; the target is untouched. No web request was made in this unit (the target's own photographs were enough; nothing was fetched).

## Files

| File | What |
|---|---|
| `build_shopfront.py` | builds the seven parts and the assembly (`--only pilaster,...`, `--shop ritas`) |
| `check_shopfront.py` | the automatic check; writes `checks/check_v1.json` (about 90 s; `--no-overlaps` skips the exact-boolean overlap test) |
| `render_shopfront.py` | the review pictures (calls `../tools/review_render.py`, 2 threads, adds a dark interior behind the opening in the scene only) |
| `checks/check_v1.json` | every row of the check |
| `build/` | the parts as `.npz` and `parts.json` (written by the build) |
| `production/assets/cloud-week/shopfront/` | `pilaster.glb`, `console.glb`, `fascia_board.glb`, `cornice.glb`, `sill.glb`, `stallriser.glb`, `window_frame.glb`, `shopfront_ritas.glb` |
| `production/previews/cloud-week/shopfront/shopfront-<street\|close>-v1-2026-10-11.jpg` | the two review views (full-size PNGs in the scratch folder `kit-shopfront/render/`) |

Rebuild and re-check: `/home/user/.bpyenv/bin/python build_shopfront.py`, then `check_shopfront.py` (it runs `target_drawing.py` itself into the scratch folder if no `--drawing` JSON is given), then `render_shopfront.py` (about 6 minutes a view on 2 threads at 64 samples).

## The models

| .glb | triangles | size | materials |
|---|---|---|---|
| pilaster | 1,762 | 88 KB | paint_oxblood |
| console | 5,428 | 199 KB | paint_oxblood |
| fascia_board | 76 | 6 KB | paint_oxblood |
| cornice | 328 | 20 KB | paint_oxblood |
| sill | 116 | 8 KB | paint_white_joinery |
| stallriser | 2,620 | 87 KB | paint_oxblood |
| window_frame | 2,756 | 189 KB | paint_white_joinery, glass |
| shopfront_ritas (the assembly) | 20,276 | 876 KB | paint_oxblood, paint_white_joinery, glass |

Metres, z up, scale 1, the street toward -y, UVs by cube projection at real scale (1 UV unit = 1 m), smooth shading by angle (35 degrees) with the arrises kept, no textures. Rita's variants: panel pilaster, scroll console, panel stallriser (3 panels), T1 window frame (3 lights, 8 toplights). Paints are read from `shops[ritas].paints` (target.json's `paints`: oxblood 93,46,49 on piers, consoles, board, cornice and stallriser; gloss white 226,224,214 on the window frame and the sill).

**Frame and pivots** (the existing kit's convention, `production/art/shopfront-kit/README.md`, which fits the street): y = 0 the wall face, z = 0 the footway, x = 0 at the middle of the piece's width on that datum. So a part drops into the bay with a shift along x only:

| part | pivot u (mm) | placed in Rita's bay at x (m, bay middle u 3000 = 0) |
|---|---|---|
| pilaster (left pier, slot u 0 to 350) | 175 | left -2.825; the right pier is the same piece mirrored about the bay's middle, +2.825 |
| console (symmetric, one piece) | 175 | -2.825 and +2.825 |
| fascia_board, cornice | 3000 | 0 |
| sill, stallriser, window_frame | 3975 (middle of the window zone u 2300 to 5650) | +0.975 |

The assembly's own pivot is the bay's middle (u 3000). Street x of the window centre 17.025 and of the side door's centre 20.178 follow (east parade: x = 21 - u/1000); the check proves both.

## How each part is made (all from target.json's points)

- **Pilaster** (`pil_*`): plinth body as a height-field slab (skirting 120, stiles 50, sunk panel 12 with a 12 quarter-round bead on its sides and 45 degree sticking top and bottom: `plinth_panel_side_through_field`), the cap (`plinth_cap_side`), a backing core, the shaft (a height-field: stiles 45, rails 80 and 110, the field 12 down behind a 10 cove, the target's `shaft_panel_plan` points), the base ogee (15 proud, 60 high, a mitred sweep returned both sides), the capital lofted from `capital_side` (astragal, fillet, die at d 144, hollow flare to d 172, abacus 175, ovolo) with the tablet 170 x 80 x 8, and the downpipe's chase (u under 38, d over 50) cut through plinth and capital at the party-wall side.
- **Console** (`con_*`): a loft of the 65-point `side_silhouette` with the 12 mm chamfer down each front edge; the grooves (5 wide, 4 deep, the target's two spiral centrelines, 8 inside the outline) cut by exact boolean, with 16 mm eye bosses standing 3 proud of the groove floor; the acanthus leaf as rows across `leaf_outline`.
- **Fascia board**: `section` (bed mould 40 high, front 132) extruded u 295 to 5705. **Cornice**: the 19-point `section` swept round the plan (front run and two mitred returns of the full section back to the wall: one closed mesh, the mitre on u + d = 269).
- **Sill**: `section` along u 2300 to 5647. **Stallriser** (panel): a height-field, skirting 135 stepping to the 125 face by the target's section, three raised and fielded panels (inset 14, bead 14, margin 35, field 12 proud of the panel) between 80 stiles and muntins on the mullion lines.
- **Window frame** (T1): jambs (`jamb_t1_plan`), the 25 seat (60 deep, on the sill's flat bed), the transom (`transom_t1`), the head (95 x 60), two oval mullions (`mullion_t1_plan`), seven toplight bars (`toplight_bar_plan`), 3 + 8 panes of 6 mm glass at d 30 to 36 in the rebates, an ovolo bead (`glazing_bead_ovolo`) mitred round every light.
- Timber arrises are eased 1 mm (a chamfer; the target: "eased 1 to 2.5 by repainting"). Members that overlap sit 0.3 to 12 mm into what they stand on, never in one plane with it; the loft rings that share a height are set 0.01 mm apart so no face has zero area.

The doors, the side door and the lobby are not in this unit: their openings are left plain (side door slot u 350 to 1294, shop door slot 1294 to 2300), empty. In the review renders a dark matt interior stands behind them (scene only, not in any .glb).

## The check: `checks/check_v1.json`

**162 of 162 required rows pass** (12 extras, 3 of which do not pass, below). The rule is the brief's: IoU at least 0.97, outline p95 at most 2 mm, worst at most 6 mm; every dimension within the check's own tolerance.

- **A, sections** (17 compared with the drawing at 0.1 to 0.25 mm a pixel): plinth cap, plinth through the panel, base ogee, capital, shaft plan, console side, fascia, cornice, sill, stallriser frame, mullion, jamb, toplight bar, transom, head, ovolo bead, cornice plan with its returns. IoU 0.987 to 0.9998 (the toplight bar compared from d 1), p95 at most 0.28 mm, worst at most 1.0 mm. The two returns turned (`return_left_uz`, `return_right_uz`, cut at d 0.5): Hausdorff 1.06.
- **B, elevations of the whole front** (1 mm a pixel, layer by layer): both pilasters, consoles, leaves, board, cornice, sill, stallriser, window joinery, window with glass (no hole): IoU 0.973 to 0.999, p95 at most 1 mm, worst at most 5.7 mm (the pilasters: the target's elevation draws the astragal as a 314 x 24 rectangle where its own section makes it a round bead; the corners are 5 to 6 mm off).
- **C, the target's checks** that apply: PIL-01 to 10, 12 to 15, 17; CON-01 to 09 (the volutes' eyes and radii by circle fit: 159.97 / 468.00 / 44.98 and 157.94 / 48.02 / 26.01; the console's least front 140.004); FAS-01 to 03; COR-01 to 06; SIL-01, 02; STA-01, 02; WIN-01 to 06; ZON-01, 02; ASM-ritas door and x; MAT-01, 02; NO-01; CLR-01 (every pair of objects whose boxes meet, tested by exact boolean: 54 pairs, 28 overlaps, all of them the declared enclosed ones listed below, nothing else).
- **D, joins**: 24 joins (shaft on cap, capital on shaft, console on capital, board on capital and between the consoles, cornice on board and consoles, stallriser under sill, seat on sill, jamb against core, transom against jambs, mullions, bead on glass): every gap 0.0 mm; the sill's end 3.0 mm short of the right plinth (the target's meets row).
- **E, the files**: every .glb under 1 MB (the assembly 876 KB), a UV set on every mesh, no images or textures, every object a closed solid, no two objects with coplanar same-facing faces overlapping by more than 1 mm2 (the hatching kind).

Enclosed overlaps built on purpose (CLR-01): toplight bars 6 into the transom's top and 3 into the head; the jambs' foot wedges 12 into the sill (scribed down to the weathering); the die's tablet 0.5 into the die; the leaf 0.4 into the console's face; the bosses 0.4 into the groove floor.

**Extras that do not pass** (not required; the drawing is simpler than the target's own text): the base ogee against the drawing's 320 x 60 rectangle (IoU 0.93, worst 15 mm: the target's own `base_ogee` profile narrows to the shaft's width at the top and is returned round the shaft, so its front outline tapers); and the cornice against the drawing's plain 5892 x 150 rectangle (worst 22 mm: the mitred returns' profile steps back at the wash and the cap). Both are compared instead against what the target's own profiles give (base ogee excluded and the shaft's foot behind it filled; the cornice as `return_left_uz` + run + `return_right_uz`), which pass.

**Not applicable here** (listed in the JSON): PIL-11, PIL-16, STA-03 (the fluted, render and tile variants are not built: Rita's is panel); DOR-*, SID-* (doors not in this unit); ALT-* (Rita's has only a repaint); the other nine fronts' ASM rows (nothing is multiplied).

## Where the target contradicts itself, and what the build followed

1. **The sill's length.** The text says 3430 (the window's 3350 plus 40 under each jamb); its meets row says the sill stops 3 short of the plinth; its drawing draws exactly the window's 3350. A 3430 sill would run 40 into the plinth, and 40 into the shop door's jamb at the other end. Built 3347 long (u 2300 to 5647): the window zone, 3 short of the right plinth. The drawing comparison for the sill reads this 3 mm end (IoU 0.973).
2. **The glass's plane.** WIN-05 says d 30; the drawing draws the pane d 30 to 36 (and the rebates are 24 to 36). Built d 30 to 36 (30 is its back face); the check says so.
3. **The leaf's relief.** "Relief 12 at the rib" and "a rib 4 proud of the dome" cannot both be 12 at the top. Built as a dome of 8 and the rib 4 more (12 at the rib, CON-06 within 0).
4. **The shaft's "bead".** The text calls the edge of the sunk field a quarter-round bead 10; its own plan polygon (the points) makes it a 10 mm cove (concave). Built to the polygon. The plinth's side bead is a true convex quarter-round (the `panel_bead` profile), the plinth's top and bottom 45 degree sticking (its section).
5. **The capital's flare.** The elevation draws straight sides (290 to 350 over 90 high); the section draws a hollow front. Built to both: the width runs linearly in z, the depth follows the hollow.
6. **The drawings' ogee and cornice rectangles** (extras above), and **the stallriser's two 80 end stiles** are left undrawn by the target's elevation (it draws panels from u 2380 to 5570 only); the build has them (the text says 80 stiles) and the comparison reads u 2380 to 5570.
7. **The backing core** is "330 wide x 140 deep" in the text (the kit's was 346 x 85, as deep as the window jamb); built as the kit meant it: 95 deep (the window jamb), from the shaft's party side (u 30) to the slot's free edge (350), plinth top to neck. A 330 x 140 core would put its face in the shaft's plane, and a core on the party side would block the downpipe's gap.
8. **MAT-01** "at most three plain materials per piece": per part one or two, the assembly three (two paints and glass). The window's lights and the sill need the white paint apart from the pier colour.
9. **The downpipe chase and the base ogee's party-side leg.** The chase (76 across, d 50 to the front, plinth and capital) leaves the ogee's party-side return (u 15 to 30) standing over the notch on the cap. The target asks for both; built as asked.
10. **The target's text on PIL-12** ("the pair's gap 0") is measured on the single pier: its party-side plinth, cap and capital run to u 0 (the neighbour is its mirror).

## Judgements the target did not settle

- **Pivots** (above): the brief says "the back face's bottom centre"; the existing kit puts every piece on the street datum (the window frame's foot is 0.6 above its origin). Chosen: the datum, so no part needs a z shift.
- **The core** (7 above), and the foot wedges under the jambs: the jamb's 95 overhangs the sill's 60 flat bed, so a wedge d 60.5 to 95, z 588 to 600 is scribed into the weathering under it.
- **The seat**: 25 high and 60 deep (the sill's flat bed); the target gives its height only. The lights' glass stands on it and the lowest bead lies on the glass above it.
- **The bead** sits on the glass's front face (d 36 to 48), 16 wide, its flat edge against the member; brass screws every 250 are not modelled.
- **Toplight bars** start 6 into the transom (the top slopes under the bar's front) and 3 into the head; their backs are 1 mm off the wall.
- **The leaf** as a mesh of rows (9 across, about 28 rows), dome by `(1 - s^2)`, a groove 3 deep across each notch between the lobes (not diagonal veins: no photograph shows a console, the target says Judgement).
- **The stallriser's panels**: the opening is bounded by an 80 stile and muntins on the mullion lines (as the drawing); the panel's profile is a 14 quarter-round bead, a flat margin 7, a bevel to the field at 35 in, the field 12 proud of the panel's floor (2 behind the frame's face); the end panels are therefore not equal (1002, 1026, 1002 wide).
- **The ogee's free-side leg** stops at the core's front (d 95); the party side leg starts at d 2.
- **The shop door and side door slots** are left empty (no head, no transom over them): the target puts the transom, a fielded panel and the head over the doors in the door family's work.
- **Chamfer** 1 mm on timber (the middle of the target's 1 to 2.5 band); none on the console (its front chamfer is the target's 12), the ogee and the glass.
- **Material values**: the target's `paints` rough 0.45 (oxblood) and 0.5 (white), metal 0; the glass the door's (transmission 1.0, IOR 1.5, base 121,131,139).

## Set aside / not built

Nothing was set aside. Not built, by the brief: the doors, the side door's F1, the lobby, the alterations, the other nine bays. Not modelled because the target says they are painted over or hidden: the screw pellets in the sill, the cut nails, the dowels and coach screws of the console, the stub tenons and pegs of the frame, the beads' brass screws.

## Renders

`render_shopfront.py`, 1600 x 1200, 64 samples, Cycles on the CPU with 2 threads, `LEDGER_REVIEW_HDRI=/home/user/cache/hdri/bethnal_green_entrance_2k.hdr`. Street view: 9 m out on the street side, 1.2 m toward the window end, eye 1.6 m, 38 mm lens, the whole front. Close view: 1.75 m out, left pilaster's capital, the console and the end of the fascia (30 mm lens, from the opening side so the console's side with its grooves shows). The pavement is review_render's; the dark interior behind the opening is this script's (a box, never in a .glb). The look is Unreal's work, not judged here.

## Limits

- The console and the leaf are Judgement (no photograph of a console was reached): the first part to check against one.
- The right pilaster in the assembly is a mirrored copy, not an instance (the glTF carries it twice; the assembly is 876 KB, so there is 14 per cent of the limit left).
- Wear, the party-wall downpipe, the neighbour's pilaster, the shutter and the paints of other shops are not here.
