# South quay kit: what Quay Street's south end looks out on

The closure the first gate review of item 1.1 asked for (production/audits/phase1-exit/
GATE-1.1-REVIEW-1.md, item 1: past the street's south end, flat grey ground and then the sky
photograph's own field). It is what the adopted atlas has there: Quay Street running on 28 m to its
junction, the road turning west for the jetty root and the Harbour Board approach leaving east, the
open quay apron with its granite edge at x = -70, the Old Basin, the stone jetty across it with a
harbour light, the sea to the horizon, the Hook's warehouses on the east land, and walled yards on
both corners. Research and every source: production/research/south-quay/METHOD-2026-10-06.md.
Built 6 October 2026.

Previews: production/previews/south-quay-from-mickeys-2026-10-06.jpg (Mickey's door, the street
appended) and production/previews/south-quay-plan-2026-10-06.jpg (top down, the atlas's coast,
roads, footways and massing blocks drawn over it).

## Files

- Recipe: tools/art-recipes/south-quay/south-quay.py (Blender entry, export, report, previews) and
  south_quay_geom.py (all the geometry, plain Python, so the selftest builds it without Blender).
- The glb (not in git): F:/LedgerTools/game-inputs/production/assets/south-quay/south-quay.glb,
  3.2 MB, and south-quay.report.json beside it (every piece, its triangles, the materials, levels).

## The frame, and how it meets the street

Built in terrace-front.py's frame: x along Quay Street (0 at its south end), y across it with east
+y, z up, metres, road crown z = 0. **Written to the glb reflected y to -y with every face re-wound,
exactly as the street's own export is** (quay-street.json "mirror"; Jafar's ruling of 23 September
that the mirror is fixed once at the crossing into Unreal). So south-quay.glb drops in beside
quay-street.glb with no transform: east arrives at Unreal +Y. Checked: the street glb puts Mickey's
sign at y = -5.0 in that frame, and the kit's own east side lands there too.

The street's road, kerbs and footways already run south to x = -2.0 (BACKDROP_ROAD_END), so the kit
starts there, not at 0, on the same section: crown 0, channels -0.075 (1 in 40), kerb top +0.050
(125 mm upstand), footways rising 1 in 40 to +0.100 at their backs (the street's threshold). The
selftest reads those constants from terrace-front.py and checks the kit's section against them and
against the street's exported glb (50 vertices at x = -2, worst 6 mm, the street's own bevels).

**For the session:** the street's _backdrop() (the stone apron x -16 to -2, the nine sheds, the
crane) stands on this kit's apron and basin and must go when the kit goes in; it is merged into
street_stone, street_brick_* and street_slate in the export, all of it at x < -2, so in the previews
those vertices were cut from the street's meshes (720 of them), nothing else. The north backdrop
(the rise) is untouched and out of these views.

## Measurements

| Piece | Built | Source (research section) |
|---|---|---|
| Road continued | 6.0 m, crowned 1 in 40, x -2 to the junction at x -30 | terrace-front.py; atlas quay (400,350)-(400,320) |
| Junction | Quay Street turns for atlas (310,300) = (-50,-90); Harbour Board approach (460,315), (510,320) = (-35,60), (-30,110), 6.0 m | atlas routes quay, harbourlink |
| Kerb radii | 8 m inside the turn, 6 m at the approach, 12 m outside | CHOSEN, no source reached (6) |
| Kerbs, footways | 125 x 125 mm upstand, 2.0 m footways on the north corners | terrace-front.py |
| Markings | double yellows and the 1008 centre line carried on; 1003 give-way: 600/300 mm marks, 200 mm lines 300 mm apart | TSM ch. 5 (2009), terrace-front.py (6) |
| Apron | granite setts, level with the kerb top (+0.05) | Charlestown list text; pavingexpert (2) |
| Quay edge | cope nose at x = -70 (north quay), y = +40 (east quay), y = -100 (west quay) | atlas land polygon, north 280, east 440, east 300 |
| Cope | 0.60 m across, 0.30 m deep, 50 mm proud of the wall, rounded nose | CHOSEN (2) |
| Quay wall | squared stone, batter 1 in 20, to 1.0 m under the water | CHOSEN (2) |
| Water | flat, z = -3.15: half-tide 3.20 m under the cope; to x = -8000, y -8000..+8000 | Newlyn 5.6/0.8 m CD; isurv cope rule (3) |
| Jetty | x -130 to -110, y -100 to -15, stone parapet 1.2 m on its seaward side | atlas land polygon, north 220-240, east 300-385 |
| Harbour light | hexagonal cast-iron tower 4.6 m on a 0.5 m plinth, gallery, lantern, dome: 7.0 m in all | Watchet 1862, 6.5 m (5) |
| Bollards | 10, cast iron, 0.72 m high, base 0.50, barrel 0.34, head 0.44 | Dimensions.com 0.76 m (4) |
| Mooring rings | 6, 0.25 m, under the cope | CHOSEN (4) |
| Ladder | 0.45 m wide, rungs 0.30 m apart, 0.15 m off the battered wall, handholds over the cope | CHOSEN (4) |
| Fish boxes | 840 x 510 x 248 mm, 18 mm boards, 14 in stacks | FAO type C (7) |
| Rope, fenders, dustbin | coils 0.5-0.75 m; fenders 0.30 x 0.80; dustbin 0.47 x 0.70 | atlas Hook objects; street clutter (7) |
| Boats alongside | 3, 10-13 m, beam 3.8-4.4 m, freeboard 1.1 m, wheelhouse aft, mast 6.4 m | CHOSEN (7) |
| Quay row | 4 ranges, x -61 to -160, fronts at y = +58 (behind the atlas's quayside walk at y = 55), 2-4 storeys, 10-14 m deep, one blank name band | Weymouth, Sunderland list texts (8) |
| Behind and around | a store and a back range in H04, two ranges and a far range in H05, the Harbour Board's office at the approach's end, the Old Basin Cold Stores at the west road's turn, a net store in the west yard | atlas blocks H04, H05, landmark H3, place WT_COLD (8) |
| Storeys, roofs | ground 3.4 m, upper 3.0 m; slate at 35 degrees, wide sheds 22-25 | CHOSEN (8) |
| Yard walls | brick 1.40 m over the footway, 0.34 m thick, stone cope, piers every 4.5 m, boarded gates | the brief's "low brick boundary wall" |

The highest point is 18.6 m (the four-storey warehouse's chimney pots).

## Materials

One material per node, named as the street names them, and each node "<material>__<piece>"
(182 nodes, no transforms). The glb carries each material's colour and roughness from
terrace-front.py's MATERIALS table as a target, not a result (the street's rule).

Street materials reused: asphalt, kerbstone, paving, paint_yellow, paint_white, stone, brick_red,
brick_grey, slate, glass, paint_joinery, paint_door, render_cream, prop_timber, pot_clay, lead,
galvanised, frame_painted, lamp_red.

**New (none fitted):**
- quay_stone, linear (0.150, 0.146, 0.138), roughness 0.80: setts, quay walls, the jetty's masonry.
- harbour_water, (0.014, 0.020, 0.019), 0.22: the basin and the sea.
- iron_black, (0.012, 0.012, 0.013), 0.50: bollards, rings, the light's ironwork.
- rope, (0.200, 0.150, 0.085), 0.90: rope coils, fenders, mooring lines.

No textures and nothing downloaded. Unreal will want a setts surface for quay_stone and a water
material for harbour_water; the project's CC0 library has neither today (each would need its
catalogue line). The harbour light's lantern should glow red at night (the light, not the mesh).

## Triangles

47,302 in all (budget 80,000): buildings 34,678; bollards 3,360; rope coils 2,400; yard walls
1,264; mooring rings 1,080; boats and lines 894; harbour light and parapet 838; fish boxes 728;
roads, kerbs, footways and markings 685; dustbin 580; fenders 288; ladder 228; copes and quay walls
168; grounds 63; water 48. Re-imported from the written glb: 182 objects, 47,302 triangles, every
name matching its material, no transforms.

## Checks

`--selftest` (plain Python): the kit meets the street at x = -2 on terrace-front's section and on
the street glb's own vertices; the quay edge at x = -70 from the atlas's north 280; the water to
x = -8000 and y +/-8000, 3.20 m under the cope; every node "<material>__<piece>" with a known
material, the only new ones the four above; triangles under budget; every ground face up, no
degenerate face; the junction and both roads read from the atlas; the apron at the kerb top and the
yards at the threshold; the reflection keeps every face's facing. All pass.

The previews render single-sided, as Unreal draws, so a face wound the wrong way would show as a
hole. Judged from Mickey's eye (x 4.6, y 4.3, 1.6 m over the footway, 60 degrees, looking south): no
world edge, empty field or sky below the horizon; the sea runs to the horizon across the whole
frame (at x = -4000 and y +/-2000, as first asked, the sky's lower half would show in the 0.07
degrees under the horizon and in the frame's corners past 26.6 degrees, so the water goes to 8 km).
The walk-in's frame (behind Tom at Mickey's window, looking south-east past the gable) now ends in
the yard wall and the H04 and quay-row buildings.

## What it does not do

- From the junction itself, looking west, the land ends about 200 m out past the cold stores, and
  looking east along the atlas's Sea Road line it ends at y = 220: the town beyond is phase 2's.
- The Sea Road (atlas proposal) is not built; its line crosses the east land as plain setts.
- The atlas's swing footbridge across the basin mouth (a proposal) is not built.
- The atlas has Quay Street running south along east 310, 10 m inside the basin's west edge; the
  kit stops the west road at the atlas corner (310, 300).
- No lamps (the scene file places the street's), no wear, no vertex masks, no textures.
- The boats are generic and simple: seen at half-tide from the street, only masts and wheelhouse
  tops show over the quay edge.
- No CATALOGUE.md line yet for production/art/south-quay and production/research/south-quay
  (tools/catalogue.py will ask for them); this task was not to edit outside its folders.

## How to run

Blender 4.5: `C:/LedgerTools/blender/4.5.13/blender-4.5.13-windows-x64/blender.exe`

- Selftest, no Blender: `python tools/art-recipes/south-quay/south-quay.py --selftest`
- Build, report and previews:
  `blender.exe -b --factory-startup -P tools/art-recipes/south-quay/south-quay.py -- --out <dir>`
  - `--out` (default F:/LedgerTools/game-inputs/production/assets/south-quay)
  - `--street <glb>` the street glb to append for the previews (default F:/LedgerTools/tmp/street-kit/quay-street.glb)
  - `--previews <dir>` (default production/previews), `--date yyyy-mm-dd`, `--no-render`
  - `--check-views <dir>` three work views (behind Tom at the window, the junction east and west), never into production/previews
- About 3.5 minutes with the previews. Renders use Cycles on the processor whenever UnrealEditor or
  the runner's worker is running (it was, on 6 October), otherwise EEVEE.
