# Shopfront kit for the east parade

A kit of period shopfront joinery, modelled by script in Blender, to replace the plain boxes the
street builds today (StreetVignette.cs, Shopfront(): brick pilasters, a concrete stallriser, a
brick transom, flat wood doors). First bay: Rita's pawn shop, the east parade's bay 2 (x 15.0 to
21.0). Research: production/research/shopfronts/FRONTAGE-2026-10-06.md. Method and kit block:
the same as Mickey's furniture set (production/art/mickeys-props/README.md, set 2). Built
6 October 2026.

## The pieces

Five scripts, one per piece (the stallriser has two variants). Sizes are metres, measured from
the built meshes (each piece's `.report.json`); "researched" gives the spec's figure and the
source that bears on it.

| Piece | Researched size (source) | Measured | Triangles | glb |
|---|---|---|---|---|
| Pilaster: panelled plinth, panelled shaft on a moulded base, necking bead, capital with a tablet and cap moulding (`--style fluted`: five flutes) | Height 2.85 to the fascia's bottom, width 0.35, 0.10 proud (spec C5; no source gives a pilaster's width or projection). Plinth at least the stallriser's height, about 450 mm (RBKC Shopfronts SPD) | Height 2.850, width 0.350, shaft 0.100 proud and 0.29 wide (all 0.0%); plinth 0.60 high, 0.15 proud; capital top 0.35 x 0.13 at 2.850 | 5,746 | 250 KB |
| Stallriser, panelled: plinth, three raised and fielded panels, weathered sill with a drip | 0.60 high (guides 450 to 700 mm, Brighton & Hove SPD02; 400 to 700, Coventry 2014), 0.15 proud at the sill's nose (spec); usually raised and fielded (Building Conservation Directory 1994) | 3.350 x 0.150 x 0.600 (0.0%); face 0.125 proud | 6,120 | 244 KB |
| Stallriser, glazed tile: skirting course, 152 x 72 mm brick-shaped tiles in stretcher bond, bullnose capping, timber sill | As above; tiles "usually in green but sometimes in brown or red" (Brighton & Hove SPD02); rich brown glazed tile at Skipton, c.1908 (Historic England 1488333) | 3.350 x 0.150 x 0.600 (0.0%) | 14,900 | 730 KB |
| Window frame: jambs, two round-nosed mullions, sill beads, transom, toplights with glazing bars, head | Sill 0.60 to head 2.85, transom 2.40 x 0.08 (spec); mullions "projecting about 40-70mm from the glass" (Cornwall Shopfront Design Guide 2017) | 3.350 long, 0.600 to 2.850, transom 2.400 x 0.080 (all 0.0%); mullions 48 mm in front of the glass | 5,948 | 250 KB |
| Shop door in its frame: half-glazed leaf (fielded panel, lock rail, glazing beads), kick plate, letter plate, lever handles on backplates, Yale-type rim cylinder and its latch case, three hinges; terrazzo threshold, jambs with stops, door head, fanlight, transom, toplight with two bars, head | Leaf 0.90 x 2.04, glazed from 1.00 (spec C8); bottom rail 9 in (Ellis 1902) | Leaf 0.900 x 2.040, glass from 1.000 (0.0%); overall 1.006 wide, 2.850 high | 10,026 | 432 KB |
| Side door to the flat in its frame: four-panel leaf (raised and fielded both sides), letter plate, knob, Yale-type rim cylinder, night latch case, three hinges; stone step, jambs with stops, door head, fanlight, transom, fielded panel above | Leaf 1981 x 838 mm, the imperial standard (spec C9; First in Architecture, Metric Data 12); solid panelled for the flat's door (Brighton & Hove SPD02); letter plate 0.25 x 0.04 at 1.0 (spec) | Leaf 0.838 x 1.981; letter plate 0.250 x 0.040, centre 1.000 (all 0.0%); overall 0.944 wide, 2.850 high | 12,908 | 539 KB |

Every piece is generic: no maker's name, badge or lettering. No textures, no downloaded files,
nothing for drink, betting or children.

## The bay, and where the pieces go

All pieces share one datum: x along the street, left to right seen from the street; y = 0 the
wall face, which is the back of every piece, the street toward -Y; z = 0 the pavement. Each
piece's origin is on that datum at the middle of its width, so it drops into a bay with no
offset (the window frame's foot is 0.60 above its origin, on the stallriser's sill).

Rita's bay, in the bay's own x (street x = 15.0 + x): pilasters at 0.175 and 5.825; side door at
0.822; shop door at 1.797; window frame and stallriser at 3.975, 3.35 long. The neighbours'
pilasters stand at -0.175 and 6.175, so each party wall has a pair, each under its own console,
as the street already places the consoles. The pieces meet the existing meshes: the capital's
top is the fascia's bottom, 2.85, and is 0.35 x 0.13, so the console's foot (0.24 x 0.06,
fascia_console_01) stands wholly on it; the frames' heads stop at 2.85 under the fascia band
(2.85 to 3.40, 0.12 proud); the cornice (fascia_cornice_01) sits on the band. In the bay view
the consoles, cornice and fascia band take the shop's paint (the street overwrites their one slot
with its own surface). Measured in the assembled bay (bay-meet.json): all four
pilaster-to-console gaps 0.0 mm, all 40 points of each console's foot on its capital, the
furthest 2.7 mm above it (the capital's rounded arris).

The glass is not in the kit: Unreal draws it. Each piece's report lists its openings; the glass
plane is y = -0.03 (30 mm in front of the wall face, 0.12 behind the sill's nose), and the shop
door's own glass is in its leaf at y = -0.047.

**For the session (not changed here):**
- The spec's widths count the door leaves only (0.838 + 0.90 + 3.562). With their frames the
  side door is 0.944 and the shop door 1.006, so the window and stallriser are 3.35, not 3.562.
- The street today puts the shop glass 0.12 to 0.16 m in front of the wall, ahead of the 0.10 m
  pilasters; the kit's glass is 0.03 in front, recessed behind them.
- The street's fascia box runs the bay's full width across the pilaster heads, 0.12 proud. A
  console's foot is 0.06 deep and it reaches 0.12 only about 0.29 m up, so the box buries the
  lower half of every console. The guides put the fascia between the consoles (the fascia sits
  between the consoles, Coventry 2014); the bay view does so (0.295 to 5.705 in Rita's bay),
  and that is what lets the console be seen standing on the capital.
- The existing console mesh is coarse beside the kit: its scroll is a few flat-shaded steps
  (visible in the close view). It would repay remaking by the kit's method.
- The D5 downpipes at the party walls (0.094 m from the wall, 68 mm across) would run through
  the paired pilasters' capitals (0.13 proud) and plinths (0.15), which butt at the party line.
- Facing: the kit faces -Y in Blender, which is glTF +Z, as the brief and set 2 say.
  production/specs/asset-interface.md names glTF -Z as forward, and the fascia's console and
  cornice follow it (they project toward +Y in Blender; the bay view turns them 180 degrees).
  So each kit piece wants the opposite yaw to the consoles when the street places them; the
  scene's yaw_rule already writes the yaw per prop for exactly this.

## Materials

At most three plain PBR materials per piece (base colour, roughness, metallic), no textures:

- **painted_timber**: every piece. Its colour is set per shop with `--paint r,g,b` (sRGB, 0 to 1
  or 0 to 255); the default is a dark green, sRGB 0.11, 0.23, 0.16 ("dark green", Brighton & Hove
  SPD02; Westminster lists maroon, dark green, black, dark blue and brown). In the game the paint
  colour belongs per placed piece (a material instance or Custom Primitive Data, research
  section 5); the glb carries the default.
- **brass** (or **chrome** with `--metal chrome`): the doors' fittings.
- **glazed_tile** and **grout**: the tiled stallriser (`--tile r,g,b`, default a rich brown).
- **terrazzo** (the shop door's threshold) and **stone_step** (the side door's step).

## Wear masks

As set 2: Cycles bakes ambient occlusion and Pointiness into the colour attributes "ao" and
"edges"; the glb's COLOR_0 carries red = ao, green = edges, blue 0, alpha 1, so one master
material reads the furniture and the shopfront alike. Every piece is baked with the wall behind
it, the pavement under it and its neighbours (fascia, console, stallriser, door frame) standing
by as occluders, which are removed before export. In the .blend the preview materials show the
wear the masks make: paint chipped to a pale undercoat on arrises, beads and sills, grime in the
panels' angles, brass bright on its edges. The splash band low on the stallriser and doors and
the sun-fade on south fronts (research section 3) are the master material's work, by height and
by a per-shop tint, not the meshes'.

## Checks

- **Clean rebuilds.** Every script ran headless from a clean start (`--factory-startup`, an empty
  scene) and rebuilt its glb, .blend and report: 45 to 85 s each with its preview (Cycles on the
  processor), 5 to 25 s without. Their arguments were tried into `F:\LedgerTools\shopfront-kit\test\`: a fluted
  pilaster 0.40 x 3.00 (5,830 triangles); window frames 4.50 m (three mullions, 7,790) and 2.00 m
  (one, 4,070); a 2.00 m tiled stallriser in green (9,430); a right-hinged shop door in red with
  chrome and a panel above (10,662); a right-hinged side door with a glazed toplight (12,416).
  All built, no UV overlap, all sizes as asked.
- **Sizes.** Every target in the table measured from the built mesh at 0.0% error (limit 2%).
- **UVs.** One UV map ("UVMap") per object, all inside 0 to 1; every UV triangle rasterised at
  2048 x 2048: 0 overlapping pixels on every piece, as built and again on re-import.
- **Masks.** Every object carries "ao", "edges" and the packed "ao_edges"; each glb's COLOR_0 read
  back: red (ao) means 0.25 to 0.59, green (edges) 0.21 to 0.57, blue 0, alpha 1, each matching
  the .blend's bake to within 0.034 (corner against vertex averages).
- **glb.** 244 KB to 730 KB, all under 1 MB, no images inside. Each re-imported into an empty
  scene (`check-glbs.py`, results in `glb-check.json`): its objects (the doors' leaves still
  parented to their frames), one UV map, one colour set, custom normals, sizes as the report,
  base on the datum (the window frame's at 0.60 by design).
- **The meet.** In the assembled bay all four pilaster-to-console gaps are 0.0 mm; each console's
  foot (40 points) stands wholly on its capital, the furthest point 2.7 mm above it where the
  capital's arris is rounded (limit 5 mm). `bay-meet.json`.
- **Shading.** Workbench checks (studio light, single grey, specular) of every piece, whole and
  close (the pilaster's base and capital, a stallriser panel, the tiles, the transom and mullions,
  the shop door's lever and fanlight, the side door's panels, letter plate and knob), looked at:
  no faceting, no dark or inverted faces, bevels and mouldings shade smoothly
  (`previews\checks\`). Rendered by `shading-checks.py` at 13:36, in a moment the card was free
  (the pieces' own Workbench step had been skipped while it was busy); Cycles grey studio checks
  on the processor, before and after, agree.
- **Faults found and fixed on the way:** a coplanar overlap that drew a black strip down the
  shaft's side (the sunk field now sits between the stiles); the same overlap hidden in the
  stallriser's ends; a hollow capital (its block stopped under the cap moulding, so the console
  had nothing to stand on: found by the meet check); a 30 mm slot of daylight between the shaft
  and the frames beside it (now a backing board as deep as the frames' jambs); the panel boards,
  hidden under the fields and beads on both faces, removed (the side door fell from 15,432 to
  12,908 triangles).
- **Graphics card.** The pieces were built and baked on the processor while Unreal and the build
  machine held the card. While either ran, the previews and the bay views were rendered with
  Cycles on the processor (four threads, processor denoising); nothing was rendered on the card.
  One exception to note: the pilaster's Workbench check (one still, under a second) rendered at
  13:14 in the gap between one UnrealEditor closing and the next starting, when the check found
  neither running.

## How to run

Blender 5.2: `F:\LedgerTools\blender52\blender-5.2.2-windows-x64\blender.exe`.

- Each piece: `blender.exe -b --factory-startup -P tools/art-recipes/shopfront-kit/<piece>.py -- [arguments]`
  - `pilaster.py`: `--height 2.85 --width 0.35 --projection 0.10 --plinth-height 0.60 --plinth-projection 0.15 --style panelled|fluted`
  - `stallriser.py`: `--length 3.35 --height 0.60 --projection 0.15 --variant panelled|tile --panels 0 --tile r,g,b` (the glb is `stallriser_<variant>` unless `--name` is given)
  - `window_frame.py`: `--length 3.35 --mullions 0 --toplight-pane 0.36 --sill 0.60`
  - `shop_door.py`: `--width 0.90 --height 2.04 --glazed-from 1.00 --hinge left|right --metal brass|chrome --upper glazed|panel`
  - `side_door.py`: `--width 0.838 --height 1.981 --letterplate-width 0.25 --letterplate-height 0.04 --letterplate-at 1.0 --hinge left|right --metal brass|chrome --upper panel|glazed`
  - all: `--paint r,g,b --name <name> --no-render --out-dir <folder>`
- Every render first checks that neither UnrealEditor nor Runner.Worker is running. If one is,
  nothing is rendered on the graphics card: a piece's preview is rendered by Cycles on the
  processor instead and its Workbench check is skipped; the bay script stops unless given
  `--cpu`. The piece is built, baked, exported and saved either way.
- The glb re-import check: `blender.exe -b --factory-startup -P tools/art-recipes/shopfront-kit/check-glbs.py`
- The Workbench checks alone, from the saved .blends, in seconds: `blender.exe -b --factory-startup -P tools/art-recipes/shopfront-kit/shading-checks.py`
- The bay, the meet check and the contact sheet: `python tools/art-recipes/shopfront-kit/bay-contact-sheet.py` (`--check-only` measures the meet without rendering; `--cpu` renders with Cycles on the processor).

Each script carries the set 2 kit block (copied from tools/art-recipes/mickeys-props/counter.py;
its few changes marked SHOPFRONT: the paths, the graphics-card check before any render with
Cycles on the processor while the card is busy, the preview's ground height, no .blend1 copies)
and the shopfront kit block (the datum, the profiles and sweeps, the door frame), so each stands
alone.

## Paths

- Scripts: `tools/art-recipes/shopfront-kit/` (`pilaster.py`, `stallriser.py`, `window_frame.py`, `shop_door.py`, `side_door.py`, `check-glbs.py`, `shading-checks.py`, `bay-contact-sheet.py`).
- glb: `F:\LedgerTools\game-inputs\production\assets\shopfront-kit\<piece>.glb`
- blend and measured report: `F:\LedgerTools\shopfront-kit\blend\<piece>.blend` and `<piece>.report.json`; `glb-check.json`, `bay-meet.json`
- Previews (800 px; Eevee when the card is free, else Cycles on the processor; today's are Cycles) `F:\LedgerTools\shopfront-kit\previews\<piece>.png`, Workbench shading checks in its `checks` folder, the bay views `bay-rita.png` and `bay-rita-meet.png` (Cycles on the processor, `--cpu`)
- Argument trials: `F:\LedgerTools\shopfront-kit\test\`
- Contact sheet: `production/previews/shopfront-kit-2026-10-06.jpg`
