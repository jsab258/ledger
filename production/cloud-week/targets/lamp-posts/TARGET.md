# Quay Street's lamp posts: the target (cloud week 42, 9 October 2026)

**Quay Street's four lamp posts (x 8, 18, 28, 38, alternate sides) are painted-steel stepped columns of the kind the 2019 photographs show: a black sleeve 124 mm across and 978 high with a 60 mm cone and a ring line, a shaft tapering from 68 to 60 mm to a collar at 4.6 m, a plain bent-arm bracket (a 42 mm stem, one 90 mm bend, a straight arm raked 40 degrees) entering the rear boss of a boat-shaped aluminium canopy (550 x 300 x 200, its top at 5000, centred 500 out) over a yellowed clear bowl with a 54 x 310 sodium lamp inside it, the lantern's long side along the arm (the scene had it along the street), a flush door 100 x 500 at z 400, a 90 x 45 reference plate 'LC n' and no maker's mark; the lit lantern is orange (255, 137, 0) with a yellower lamp, the scene's (255, 219, 0) being the colour of 585 nm, not 589; the approved Hook sheet shows no column at all, and no reachable photograph is of 1990, so every length from the photographs is +-7 % and the choice of steel over the earlier research's concrete is Judgement (concrete is written out as variant C).**

Written 9 October 2026 for the family "lamp posts on Quay Street" (scene lines E1 lighting column and E2 sodium lantern, four of each). Units are millimetres unless a line says otherwise; the .glb is metres, z up, scale 1, the pivot the column's axis on the footway. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, plans and sections as polygons in millimetres and pictures at 1 mm a pixel); `self_check.py` tests them; `make_target.py`, `lamp_numbers.py`, `measure_photos.py`, `make_previews.py` and `make_doc.py` re-make everything (the photographs themselves are Poly Haven's CC0 panoramas and are not in git). Last result: SELF-CHECK PASS: 231 of 231 tests pass (A printed numbers 75/75, B photographs 31/31, C drawing 35/35, D internal consistency 26/26, E text, canon and previews 54/54, W wrong copies refused 10/10) (`/home/user/.bpyenv/bin/python -I self_check.py`; it re-measures the previews, runs the drawing, recomputes the derived numbers and tries ten deliberately wrong copies of target.json, all of which it must refuse).

## 0. Read this first

1. **No photograph of 1990 was reached.** The cloud's network refuses Wikimedia, Geograph, Flickr, archive.org and the rest (section 2.3). The only photographs reachable are Poly Haven's CC0 panoramas of London and Cambridge taken in 2019 (all by Andreas Mischok). Of the seventeen British ones, two show a steel lighting column well enough to measure (urban_street_01, called US01 below, and bethnal_green_entrance, BGE); none is shown to be older than 2019, and a 2019 column in Tower Hamlets may be a replacement. So nothing here is a 1990 measurement. What the photographs give is the FORM of a painted-steel stepped column and its bracket, the sizes of the lower column to +-7 %, the colour and wear of its paint, and the colour of a lit lantern; the rest is the project's earlier reading, the scene's numbers, or Judgement, each marked.
2. **The approved Hook sheet shows no lighting column.** The brief's "slender, dark column with a small flat canopy" is the RETIRED sheet's. The approved street panel (production/reference/hook-sheet.png, approved 22 September; its reduced copy production/previews/hook-sheet-2026-10-05.jpg) shows no lighting column and no bracket lamp: read at full size on 9 October, the only vertical on its skyline is a mast on the far hill, as production/reference/retired-sheet-inheritance.md row 4 and game-design/research/GOVERNS.md already say. So no number below is read off a Hook sheet; the sheet governs mood (section 3).
3. **Kinds of number.** Every number in `target.json` `numbers` (130 of them) carries its kind: **Read** (printed in the repository or in a file this writer opened, with the file), **Photo** (measured on a photograph: method and error in section 4), **Derived** (computed from other numbers here; the formula is in its `source`), **Judgement** (a trade or period guess, said so). `number_kinds` counts them: {"Read": 57, "Photo": 29, "Derived": 21, "Judgement": 23}.
4. **The choice that is Judgement:** painted steel (variant A) is the main build; the earlier research's precast concrete column (variant C) is written out but not built unless ruled in. Both share the bracket, the lantern, the light and the places.

## 1. What today's stand-in gets right, and what this target changes

Today's stand-in (SCENE-SLOTS.md; production/specs/vignette-scene.json `lighting`; StreetVignette.cs `Columns()`, read 9 October): a base cylinder 200 across and 300 high, ONE 114 mm shaft from 300 to 5000, a swan neck of three short cylinders (0.8 x the shaft) on a quarter circle rising over the lantern, a box lantern 550 along the street x 300 x 200 with its top at 5000 and its centre 500 from the axis, emissive, colour (255, 219, 0). "Trade-standard guesses, not photographs".

|  | the stand-in | this target | kind |
|---|---|---|---|
| the place | x 8, 18, 28, 38; east, west, east, west; axis 0.6 m behind the kerb's back face | the same (the code's loop; SCENE-SLOTS.md's 'every 20 m' is 20 m on one side) | Read |
| lower column | base 200 x 300, then a 114 shaft to 5000 | a 124 sleeve 978 high, a 60 mm cone with a ring line, a shaft 68 tapering to 60 at 4560, a 67 collar to 4620 | Photo (BGE), the scene's 114 lies at the sleeve's lower error edge |
| bracket | a swan neck: three cylinders rising over the lantern and dropping into it | a plain bent arm: a 42 stem, one 90 mm bend, an arm raked 40 degrees into the lantern's rear boss | Photo (US01) + Read (R07 'plain bent-arm lighting') |
| lantern | a box 550 along the street x 300 x 200 | a boat-shaped canopy over a deep yellowed bowl, the same 550 x 300 x 200 envelope turned so the long side lies ALONG THE ARM | Photo (US01 from below) + Read (the research's wording) |
| the glow | one emissive box (255, 219, 0) | the lamp (54 x 310) and the bowl glow; (255, 137, 0) and (255, 176, 28) | Derived + Photo |
| door, plate, fixings | none | a flush door 100 x 500 at z 400, a 90 x 45 plate 'LC n', two collar set screws, hinge and catches on the bowl, grub screws on the boss | Judgement |
| light | one light 18 m range, intensity 3.2; scene colour (1, 0.7055, 0) | the night note's pool, skirt and glow at (0, 500, 4850); colour (1, 0.25, 0) | Read (night note) |

What the stand-in gets right: the four places and sides, the mounting height 5.0 (the lantern's top), the outreach 0.5 to the lantern's centre, the lantern's box size, the 589 nm lamp, the point light 0.05 below the centre, and the rule that the column is plain steel with no ornament.

## 2. Sources

### 2.1 What was read, and what for

| id | where | date read | author | licence | date taken | what it shows or gives | used |
|---|---|---|---|---|---|---|---|
| S1 | production/specs/vignette-scene.json (lighting.column, lighting.lantern, street, blocks, cameras) and production/specs/vignette-pieces.json (column0..3, lantern0..3) | 2026-10-09 | the project | the project's own | 2026-09-02 to 2026-10-08 | the stand-in's sizes and places; the lantern's colour, xy and range | yes: Read numbers |
| S2 | ledger/Assets/Scripts/Core/StreetVignette.cs Columns() (lines 1196 to 1262) | 2026-10-09 | the project | the project's own | 2026-09 | the placement loop (x 8 while x <= 46, step 10, alternate sides, z = 3.125 + 0.6 = 3.725), the swan neck, the lantern's centre 0.5 out | yes |
| S3 | production/cloud-week/targets/SCENE-SLOTS.md; BRIEF.md | 2026-10-09 | the project | the project's own | 2026-10-08 | the row for the lamp column; the brief's rules | yes |
| S4 | production/research/street-clutter-1990/SUMMARY-2026-09-29.md section 3 (the project's earlier reading, made on the PC from its sources) | 2026-10-09 | a helper, saved by the builder | the project's own | 2026-09-29 | concrete columns with sodium lanterns; 4.6 to 6 m; 20 to 25 cm at the foot; a door plate about 50 cm up; an arm 40 to 45 cm; the lantern 7 3/4 in tall, 60 to 70 cm long (uncertain); a boat-shaped canopy over a deep clear trough bowl with a U-shaped tube; 'photographs 1985 to 1995 not found'. Its photograph links are links only (Geograph, Flickr, a lighting enthusiasts' site), all unreached from this cloud; the makers it names are not repeated here and appear on nothing | yes: Read numbers, with its caution |
| S5 | production/research/evening-light-1990/SUMMARY-2026-09-29.md | 2026-10-09 | a helper | the project's own | 2026-09-29 | 589 nm (0.569, 0.430), about sRGB (255, 140, 0), linear about (1, 0.25, 0); warm-up; 35 W SOX 4,550 lm | yes |
| S6 | production/cloud-week/research/1c-night-pools-lumen.md and production/audits/night-2026-10-08/GATE-NIGHT.md; DECISIONS.md 7 and 8 October | 2026-10-09 | the night note's writer | the project's own | 2026-10-08 | the lamp's lumens, the pool, skirt and glow, the cones, the colour, the clipped red, the 4.78 m | yes: the light block |
| S7 | production/previews/morning-night-evening-2026-10-08.jpg (the street at night now) | 2026-10-09 | the project | the project's own | 2026-10-08 | the stand-in at night: slim dark columns with long gooseneck arms over small boxes; pools on the flags | looked at; no number taken |
| S8 | production/reference/hook-sheet.png (2048 x 1088, read in four tiles at full size), production/previews/hook-sheet-2026-10-05.jpg, production/reference/hook-sheet-2026-09-09-retired.png, hook-sheet-audit.md, retired-sheet-inheritance.md, game-design/research/GOVERNS.md, photographs.md | 2026-10-09 | the project | the project's own | 2026-09-09 to 2026-10-05 | the approved sheet shows no column and no bracket lamp (section 3); the retired poster shows a black post-top globe lantern and two box wall lanterns, each a few pixels wide | yes: section 3 |
| S9 | production/cloud-week/targets/kerbs-and-covers/ and bollards/ (target.json, TARGET.md) | 2026-10-09 | their writers | the project's own | 2026-10-09 | the corrected kerb (granite top 170, flags +110) and the camera heights of BGE (1.02 +-0.07) and US01 (1.16 above the footway) | yes |
| S10 | https://polyhaven.com/a/bethnal_green_entrance (BGE); https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/bethnal_green_entrance.jpg (8192 x 4096) | 2026-10-09 | Andreas Mischok | CC0 1.0 (read at https://polyhaven.com/license, 9 October 2026: 'CC0 means absolute freedom') | 2019-08-18 | the Bethnal Green estate path; a black steel column with a post-top dish lantern at 4.4 m, 2.7 m from the camera | yes: Photo numbers (sleeve, cone, shaft, pod width, paint, wear) |
| S11 | https://polyhaven.com/a/urban_street_01 (US01); the same host's Tonemapped JPG urban_street_01.jpg | 2026-10-09 | Andreas Mischok | CC0 1.0 (as S10) | 2019-08-18 | a steel stepped column about 11 m high with a bent-arm bracket and an amber lit cobra-head lantern, 8.8 m from the camera | yes: ratios, the lit colour |
| S12 | https://polyhaven.com/a/urban_street_02, urban_street_03, urban_street_04, birbeck_street_underpass, limehouse, cambridge, greenwich_park, greenwich_park_02, greenwich_park_03, epping_forest_01, epping_forest_02, roof_garden, canary_wharf, adams_place_bridge, leadenhall_market (the same Tonemapped JPG host) | 2026-10-09 | Andreas Mischok | CC0 1.0 | 2019-02-09 to 2019-12-17 (us02 2019-08-18; us03 2019-09-07; us04 2019-09-14; cambridge 2019-12-17; the parks 2019-02-09 to 2019-09-07; the rest 2019-05-19 and 2019-08-31) | searched for lamp columns and wall lanterns (section 2.2) | us02: a wall bulkhead measured (W1's note); the rest looked at only |
| S13 | https://api.polyhaven.com/assets?type=hdris and https://api.polyhaven.com/files/<id>, /info/<id> | 2026-10-09 | Poly Haven | CC0 | n/a | the catalogue with coordinates and dates taken; the file URLs | yes |

All Poly Haven material is used for measuring and looking only: not placed in the game, not traced into a texture, not fed to an image model.

### 2.2 The search of the panoramas

Poly Haven lists seventeen HDRIs with coordinates in Britain (the Dublin sets at 53.3 N 6.2 W are not British and were left out; `st_fagans_interior` is a Welsh interior). Each of the seventeen was looked at as its 2k tone-mapped copy and, where a column showed, at 8192 px:

| panorama | what it shows | result |
|---|---|---|
| urban_street_01 | one steel stepped column with a bent-arm bracket and a lit amber cobra-head lantern (US01) | measured: ratios, lit colour, form of bracket and base |
| bethnal_green_entrance | one black steel stepped column with a post-top dish lantern, 2.7 m away (BGE), signs bolted on its shaft | measured: the lower column, the pod's width, the paint and wear |
| urban_street_04 | a decorative black column with a scroll bracket and a round glass lantern (Kensington) | looked at: a 2000s heritage replacement, wrong for 1990 and for a northern port; not used |
| urban_street_03 | one steel column with a raked arm, 6 px wide at 40 m | looked at; too small to measure |
| urban_street_02 | a black-backed opal wall bulkhead on a 1970s-80s brick block | measured roughly (235 x 210 mm, brick courses): an estate fitting, W1's note |
| cambridge | two bespoke wrought-iron glazed wall lanterns of a college | looked at: a one-off heritage piece, not a street fitting; a college's sign is in frame, so no preview |
| birbeck_street_underpass, limehouse | fluorescent battens under a viaduct; bollards and chain on a marina | no column |
| greenwich_park, _02, _03, epping_forest_01, _02, roof_garden, canary_wharf, adams_place_bridge | parks, woods, a roof garden, offices, a footbridge | no column |
| leadenhall_market | a covered market with ornate hanging lamps and shop lettering the content rule bars | not used and not previewed (the content rule) |

None of the lamp columns is shown to be from 1990 or earlier, and none is a concrete column. The brief's expected case ("if no reachable photograph shows a period column, write the target from the earlier research, the existing recipe and the Hook sheet, and say plainly which numbers rest on what") is therefore the case, with the difference that the Hook sheet gives nothing and two 2019 photographs give the lower column's form.

### 2.3 Unreached

Wikipedia, Wikimedia Commons, Geograph, Flickr, archive.org, HathiTrust, the National Archives, Historic England, legislation.gov.uk, and the lighting enthusiasts' and makers' sites the earlier research cites: `curl` returned 000 (refused at the proxy) on 9 October 2026, 20 s each. Nothing was taken from any of them. WebSearch was used only for the leads of section 2.4; no number was taken from a search summary.

### 2.4 Leads (WebSearch summaries of 9 October 2026: leads, never numbers)

- the SOX 35 W lamp is listed as 311 mm long and 52 mm across by a maker's datasheet and 310 x 54 by a catalogue table; 4,550 lm, 1,700 to 1,800 K (WebSearch summary, a lamp maker's datasheet and a trade catalogue table; the lamp's 54 x 310 sits inside both; not changed)
- a modern 5 m stepped root-mounted steel column is listed with a 76 mm shaft, a 140 mm base, a 500 x 100 door 400 above the ground, a 150 x 75 cable slot, an 800 mm planting depth and a bitumen-coated root; its standard (the 1978 BS 5649 series, current to 2006) was not reached (WebSearch summary, three makers' catalogues (modern); the door is 100 x 500 at 400 (a width of 100 and a base zone to 900 agree with the sleeve's 978 and US01's door outline); the photographed sleeve 124 and shaft 68 to 60 are smaller than that catalogue's 140 and 76 (BGE's is a post-top column) and are kept; a bracket column's top may be 76)
- enthusiasts' pages describe 1960s to 1970s 5 m precast concrete columns carrying 35 W SOX lanterns on 'angular top-entry brackets', a maker's mark cast into the inspection door, and two 5 m tubular steel columns with 'angular' brackets with a vertical and a horizontal section, the lantern steeply tilted; install dates not stated (WebSearch summary of streetlightonline.co.uk pages (unreached); both types existed with the same lantern (A and C stand); a 5 m bracket may be more horizontal than US01's 40 degree arm; a real door might carry a maker's mark: ours is blank by rule)
- no source for a bracket's upsweep angle was found (the results were Australian and modern) (WebSearch summary; the rake rests on US01's photograph alone)

## 3. The Hook sheet and the column

The brief says the Hook sheet's foreground column is slender and dark with a small flat canopy, and that tools/art-recipes/lighting-column.py records that crop. The recipe's own notes say the crop is the RETIRED Codex sheet's (production/art/atlas-01/concepts/hook.png on a branch that is not in this checkout; "three traces of one lamp crop gave three answers"), that the approved pass 4 street panel "shows NO street lighting column anywhere in it", and that the column's shape is "governed by R07's 1989 photograph, 'plain bent-arm lighting'" (production/reference/photographs.md; a Hull photograph that is under photographer copyright and was not reached). This writer re-read the approved sheet at full size in four tiles: it shows the brick terrace, the wet street, parked cars, and no lighting column and no wall lamp (a small white fitting at the gable's corner and the dish above Mickey's fascia are not lamps). The retired in-house poster (688 x 1024) is an image model's drawing from a prompt that asked for a pub (retired-sheet-inheritance.md): its post-top lamp's pole is 3 to 4 px wide and its two box wall lanterns are about 20 x 40 px, so there is nothing to measure (hook-sheet-audit.md: under about four pixels is noise) and, being a pub's, nothing citable.

So: the sheet governs mood (wet, grey, low contrast, dark metalwork) and the night frame's pools, and decides nothing about the column's shape. The slot overlay `hook-sheet-slot-x8-east-target-on-sheet.jpg` lays variant A at its scene slot (x 8, east) on the sheet's reduced copy with the sheet's own lens (production/reference/hook-sheet-lens.md; the scene's cam_hook: x -3.0, z -1.6, eye 2.2, yaw 20.4, pitch -3.4, 46 degrees vertical): it checks scale and place, not a measurement. The lens puts Mickey's pilasters within 45 px of the sheet's on 1600, as the lens note says; the sheet draws the east footway visibly wider than the scene, so the column's foot lands at the shopfronts' base rather than at the kerb, and its top stands above the sheet's first-floor window heads although 5.0 m is under the scene's 6.3 m eaves: the sheet's terrace is drawn lower than the scene's. The sheet is a picture an image model made; the target does not follow it there.

## 4. How the photographs were measured

**Camera heights.** The panoramas record none. This target uses the heights the bollards' target measured and its reviewer re-measured, each at the object's own ground (production/cloud-week/targets/bollards/TARGET.md section 3): **BGE 1.02 +-0.07 m** (brick-course horizon method on the planter wall of the same block paving; the writer 0.96, the reviewer 1.03 to 1.04) and **US01 1.16 +-0.07 m above the footway** (the garden wall and gate pier; 1.23 above the bed). Every BGE and US01 length is therefore **+-7 % in absolute size**; proportions are exact to the pixel. If BGE's sleeve is the standard 114.3 mm tube, the camera was 0.95 m (this writer's own horizon fit gave 0.96) and every BGE length is 7 % smaller; the stated error covers it.

**Distance.** The column's horizontal distance gives the picture its scale. BGE: the sleeve's front foot at row 2524 of 4096 (-20.9 degrees) gives 1.02 / tan 20.9 = 2.665 m; its radius 0.062 puts the axis at 2.73 m, bearing 138.5 degrees; the base then appears at z = -23 mm in the elevation, as the geometry says. US01: the column's foot is hidden by a car; the gate pier beside it gives 8.4 m and the lowest visible sleeve point 9.2 m: 8.8 +-0.6 m, so only RATIOS are taken from US01 (its column is an 11 m class).

**Re-projection.** `lamp_lib.elevation` makes a flat, square-on picture of the vertical plane through the column's axis at a stated millimetres a pixel (1.2 mm for the BGE strips, 3 mm for US01); edges are found by the strongest luminance gradient in a window round the expected edge (`measure_photos.py`; raw rows are in `photo_measurements.json` and copied into target.json). The native resolution is 2 mm a pixel at 2.7 m and 7 mm at 8.8 m.

| measurement | reading | error | the target's value |
|---|---|---|---|
| BGE sleeve OD | 123.6 (rows 120 to 128, z 100 to 800) | +-9 | 124 |
| BGE sleeve's straight side ends | z 978 (read on a 4 x gridded crop) | +-10 | 978 |
| BGE cone top, a thin ring line | z 1035 to 1040 | +-10 | 1038 (ring 6 tall) |
| BGE shaft OD | 66 (z 1100, by eye), 67/69/69 (z 1700 to 1900), 61/61/61 (z 3800 to 4000) | +-6 | 68 at the cone, 60 at 4560 |
| BGE pod, widest run | 417 (x -193 to +223) | +-30 | 420 (variant P) |
| BGE pod's centre height | 4410 from the limbs' angles (53.8 and 48.5 degrees) | +-300 | 4375 (P) |
| BGE paint, median sRGB | sleeve 31/31/33 (p10 19, p90 44); lowest 250 mm 49/46/42; shaft 44/45/51 (sky-tinted) | +-3 | 31/31/34; splash 49/46/42 |
| US01 shaft top / stem / arm | 89.1 / 42.0 / 59.9 | +-8 / +-5 / +-6 | ratios 0.47 to 0.67; stem OD 42 |
| US01 sleeve / shaft | 232 / 113 at 8.8 m (by eye): 2.05 | +-0.2 | BGE's own 1.8 used |
| US01 lit lantern, median sRGB (66,611 orange pixels) | 251/152/14 (p10 229/105/0, p90 255/208/77; the clipped core 252/251/180) | +-8 | bowl (255, 137, 0); lamp (255, 176, 28) |

**The drawing laid on the photograph.** The overlay `bge-bethnal-green-column-target-on-photo.jpg` draws target.json's lower column (the sleeve, cone, ring and shaft, z 0 to 4280) over the four BGE strips at a scale fitted on ONE dimension only, the sleeve's width (123.6 measured, 124 in the target: scale s = 0.9992). The self-check re-measures the preview and tests it: the sleeve's two edges over 32 rows, mean absolute error 1.72 mm (none over 8; the pixel is 1.2 mm); the shaft's width over 57 rows, median absolute error 3.49 mm, upper quartile 6.83 (the rows against the sky are within 2 mm; the rows against ivy and brick scatter); the cone and ring by the same method, with the ivy behind them confusing the edge finder (the picture shows the fit). Above z 4300 the photograph's column carries a post-top pod (variant P), not A's collar and bracket, so no outline is drawn there.

## 5. The target, part by part (variant A, the main build)

### 5.1 Frame

Origin on the column's vertical axis at the footway surface; **+y points at the carriageway** (the lantern side), x runs along the street, z up. For the west side's columns the whole piece is turned 180 degrees about z so that +y still points at the road. The column stands plumb (the footway falls 1 in 40, 3 mm across the sleeve). The pivot is the axis at z = 0; the sleeve runs 150 mm below it (hidden) so that the footway's fall never shows a gap. One mesh for the column, one for the lantern (the lamp and the bowl as emissive material slots).

### 5.2 The lower column: sleeve, cone, shaft, collar

Profile (radius, z) in mm, revolved about the axis (`geometry.A.lower.outer_rz`, authoritative):

| (r, z) | what |
|---|---|
| (0, -150) | axis at the hidden foot |
| (62.0, -150) | hidden skirt: sleeve radius |
| (62.0, 978) | sleeve top: the straight side ends (Photo, BGE 978) |
| (34.0, 1038) | cone top, shaft radius 34 (OD 68) |
| (35.5, 1038) | the weld ring: 1.5 proud ... |
| (35.5, 1044) | ... 6 tall (z 1038 to 1044) |
| (34.0, 1044) | back to the shaft |
| (30.0, 4560) | shaft radius 30 (OD 60) at the collar's foot (z 4560): a straight taper of 2.3 mm a metre |
| (33.5, 4560) | collar radius 33.5 (OD 67) |
| (33.5, 4620) | collar top (z 4620) |
| (0, 4620) | the axis |

- **Sleeve** 124 across (Photo, +-9; the scene's 114 is at its lower error edge and 114.3 is a standard tube: the tolerance covers it), 978 high above the footway and 150 below it. A 1 mm groove round it at z 978 where the cone cap is welded on (Photo: a dark line under the cone).
- **Cone** 60 mm tall, 24 degrees off the vertical, from OD 124 to OD 68; **ring** 1.5 proud and 6 tall at its top (Photo: a thin ring line there).
- **Shaft** a plain round steel tube tapering in one straight line from OD 68 at z 1044 to OD 60 at z 4560 (Photo: 66 to 69 at z 1.1 to 1.9 m, 61 at z 3.8 to 4.0 m). A longitudinal weld line 1.5 wide and 0.5 proud on the -y face (Photo: a faint vertical line near the edge; qualitative). No flutes, no ornament, no finial.
- **Collar** OD 67, z 4560 to 4620, the bracket's socket (US01 and BGE end in a short collar a little wider than the shaft; qualitative). Two M8 socket set screws, round heads 10 across and 3 proud, at z 4590, azimuth 45 and 135 degrees from +y (Judgement).
- **Root.** The sleeve runs straight into the footway: the paving is cut round it with a 10 to 15 mm joint of dark grit mortar; no base plate, no collar, no bolts show (Photo, BGE: block paving cut round the sleeve, no plate).
- **Door** (Judgement; the research says "a door plate about 50 cm up", US01's sleeve shows a rectangular door outline whose top edge is at about 86 % of the sleeve's height, and a search lead, never a number, gives a 500 x 100 door opening 400 above the ground on a modern 5 m stepped steel column; the sleeve's 978 holds a door from 400 to 900): on the -y face (away from the carriageway), a curved plate rolled to the sleeve, **100 mm of arc (92 degrees) by 500 tall, z 400 to 900, 1.5 proud**, a 2.5 wide and 2 deep joint groove (black) all round it, two round-headed hex-socket captive screws 12 across and 2 proud on its centre line at z 425 and 875, no hinge showing, no lock, **no lettering and no plate on it** (the leads say real doors of the kind could carry a maker's mark: ours is blank).
- **Number plate** on the +y face of the shaft at z 2160 (BGE has a larger flat reference plate at z 2115 to 2200, 125 x 85, white with black letters: a sign's, not copied): a curved aluminium plate **90 x 45 x 1.2** wrapped on the shaft (65 across seen square on), 1.4 proud, two domed rivets 5 across at 8 from each end, white (214, 212, 205) with black (30, 30, 32) upright sans letters 24 high reading **LC n** (n = 1 to 4, the column's number in the street). Generic: no authority's name, no crest, no maker.

### 5.3 The bracket

A plain bent arm of one tube, **OD 42** (US01: the stem is 0.47 of the shaft's top and the arm 0.67; this slimmer 4.6 m shaft's top is 60, so 42 is 0.70), in the y-z plane: it rises vertically from inside the collar (its lowest 60 mm are inside it) to z 4700 (80 above the collar's top), turns through **50 degrees on a centreline radius of 90** to a straight arm **raked 40 degrees above horizontal** (the bend ends at y 32.1, z 4768.9), and runs straight 251.8 mm to its end at **y 225, z 4930.8**, inside the lantern's rear boss (the canopy's lip band is z 4925 to 4937). The centreline is stored at 40 mm steps on the stem, 6.25 degrees on the bend and about 35 mm on the arm (`geometry.A.bracket.centreline_yz`).

Where the numbers come from: **US01's arm** (11 m column) shows 41.7 degrees in the picture's plane (fitted centreline over x -1150 to -350 of the 3 mm elevation; 43.6 over another range); the lantern seen from below is nearly side-on (its visible length 0.78 m of about 0.9), so the arm points within about 30 degrees of the picture's plane and the true rake is **36 to 44: 40 +-6** (Photo). The arm does not point much out of the plane: the lit view shows the lantern nearly full length. **The bend** on US01 is 435 mm in radius (tangent lengths 147 along the stem and 244 along the arm from their corner, the turn 48.3 degrees; about 9 arm diameters) on a reach from the stem to the boss of 1117 mm; scaled by the reach to this column's 225 it is 87.6, rounded to 90 (a tight bend: the 9-diameter bend of a big column cannot fit a short bracket). The stem's 80 mm and the collar's top at 4620 are Judgement chosen so that the arm arrives at the boss. A 5 m column's own rake is not photographed (this writer recalls standard raked brackets of 5 to 15 degrees; a search found no source for it, and a lead says 5 m brackets had a vertical and a horizontal section: the photograph is followed, the rake's tolerance is wide, and section 10 lists it).

### 5.4 The lantern

**Envelope 550 x 300 x 200** (the scene's box: Read), top at z 5000 (the mounting height), bottom 4800, centre (0, 500, 4900), **long side along y**, level. Photograph US01 from below shows the arm entering the lantern's rear end and the lantern lying along the arm; the scene had it along the street. All coordinates below are in the column's frame.

- **Canopy** (painted aluminium, shell 2.5): plan half-widths at y 225 / 230 / 245 / 270 / 300 / 340 / 400 / 450 / 520 / 600 / 670 / 725 / 760 / 775 = 0 / 30 / 58 / 86 / 108 / 128 / 144 / 150 / 150 / 146 / 134 / 108 / 62 / 0 (a boat: narrow at the rear where the arm enters, full and round at the front); a down-turned lip 12 tall from the rim z 4925 to z 4937; above it a half-ellipse dome whose crown follows z = 4937, 4962, 4990, 5000, 4998, 4985, 4963, 4945, 4937 at y = 225, 260, 320, 400, 500, 600, 680, 735, 775 (the dome is 61 high at y 500; the highest part, y 400 to 500, is the gear tray: **there is no separate gear box**). Underside white (226, 224, 216) reflector, with a lamp-holder 60 x 45 x 40 at the rear (x +-30, y 300 to 345, z 4852 to 4892).
- **Bowl** (clear acrylic, yellowed, shell 3, a 6 x 6 bead on its rim): rim at z 4925 following the canopy's plan 8 inside it (y 233 to 767); a flat refractor base at **z 4800, 400 long (y 300 to 700) and 164 wide**, plan half-widths 0 / 22 / 52 / 70 / 80 / 82 / 80 / 70 / 52 / 22 / 0 at y 300 / 303 / 320 / 350 / 400 / 500 / 600 / 650 / 680 / 697 / 700; the sides bulge outward from base to rim by the section at y 500 (half-width, z): (82, 4800), (90, 4806), (100, 4815), (118, 4842), (130, 4872), (138, 4900), (142, 4925); the ends follow the long section's rear curve (y, z): (233, 4925), (240, 4890), (262, 4850), (285, 4818), (300, 4800), the front its mirror about y = 500. `bowl.loft` gives the one formula that joins them. Fine prismatic grooves 2 mm apart across the base's underside. Hinged at the rear (two knuckles 22 x 22 x 14 at x +-60, y 262, on the rim) and closed by **two spring catches** 30 x 14 x 7 proud on the long sides at y 650, x +-136, on the rim line (Judgement; US01 shows only the canopy over a glowing bowl).
- **Lamp**: one glass jacket **54 across and 310 long** lying along y, centre (0, 500, 4872), a 35 W low-pressure sodium lamp (Judgement: a search lead lists 311 x 52 and 310 x 54, within 2 mm of these) with its lamp-holder at the rear end. The bowl's lit surface and the jacket are the only emissive parts.
- **Rear boss**: a cast sleeve **OD 60, 55 long**, axis from the arm's end (225, 4930.8) forward at 40 degrees, a visible cast boss on the canopy's rear tip (its lower edge hangs up to 17 mm below the rim at its start and its upper edge stands 17 to 24 mm above the dome); two M8 round-headed grub screws 10 across, 3 proud, at 90 and 270 degrees about its axis.
- No photocell, no ornament, no ladder bar, no finial (the recipe's rule, kept).

### 5.5 Materials and paint

| part | sRGB | plain name | roughness in words | roughness 0-1 | metal | kind |
|---|---|---|---|---|---|---|
| paint_black | [31, 31, 34] | lamp-post black, gloss worn to semi-gloss | semi-gloss, the gloss worn (the upper shaft chalky and duller) | 0.42 | 0.0 | Photo colour; roughness Judgement (the recipe's 0.42) |
| splash | [49, 46, 42] | road film over the black, z 0 to 250 | matt, dirty | 0.8 |  | Photo |
| primer | [112, 110, 106] | grey primer in chips | matt | 0.85 | 0.0 |  |
| bare_steel_rust | [94, 58, 40] | rust brown | rough, matt | 0.9 | 0.0 |  |
| canopy | [118, 116, 112] | weathered painted aluminium, mid grey | satin, dirty | 0.55 | 0.0 | Judgement |
| bowl | [190, 182, 160] | yellowed clear acrylic | glossy, slightly hazed | 0.15 |  | Judgement |
| reflector | [226, 224, 216] | white-painted reflector inside the canopy | satin white | 0.35 | 0.0 |  |
| lamp_glass | [200, 196, 180] | the lamp's glass jacket, pale when cold, glowing when lit | glossy | 0.1 | 0.0 |  |
| bowl_emissive_lit | [255, 137, 0] | the bowl lit: sodium orange | glossy | 0.15 | 0.0 |  |
| plate | [214, 212, 205] | aged white enamel number plate | semi-gloss enamel | 0.3 | 0.0 |  |
| concrete_C | [146, 143, 136] | weathered grey precast concrete (variant C) | rough matt | 0.9 | 0.0 |  |

Painted steel is not metal for shading (metal 0: a painted surface); roughness 0.42 is the recipe's and the photograph shows gloss worn to semi-gloss (the upper shaft rougher by 0.15). The bowl's transmission 0.85, IOR 1.49 (acrylic). Concrete grey (146, 143, 136) belongs to variant C only. The only high-chroma surfaces are the lamp and the bowl: the paint, canopy, plate and primer are within 16 per channel of grey (the accent budget, art-direction R-B4).

### 5.6 Wear

State: a tired column, twenty years since it was last painted, in a port town's wet air. Placed per column by its seed; positions on the sleeve are on the **carriageway face (+y)** unless said.

| feature | where, how big, colour | kind |
|---|---|---|
| splash_band | the sleeve, z 0 to 250, all round (1.0 on the carriageway face, 0.6 elsewhere), top edge soft over 60 | Photo (BGE) |
| chips | the sleeve, carriageway face, z 150 to 900: 12 to 20 chips of 2 to 10 mm showing primer, 20 % with a rust speck; plus 5 to 8 chips of 4 to 15 mm on the sleeve's top lip and the cone | Photo (US01: pale patches at the shoulder) + Judgement |
| scratches | the sleeve's carriageway face, z 380 to 430: 6 to 10 hairlines of 30 to 120 mm in light grey, no letters | Photo (BGE) |
| rust_streaks | under each collar set screw (two, 80 to 200 long, 3 to 6 wide, strength 0.6); from the door's two lower corners (two, 40 to 120); under the boss's two grub screws (two, 40 to 100) | Judgement |
| dent | LC 2 only (x 18, west): the sleeve's carriageway face at z 480 +-30, an oval 45 wide x 70 tall, 3 deep, paint cracked at its centre with a rust speck | Judgement (a vehicle's knock) |
| sticker_remnants | z 1450 +-60: a torn white sticker 40 x 25 and a smear of adhesive 15 x 60 on LC 1 and LC 3; two cable-tie stubs at z 1700 on LC 3 | Judgement; the posters target (SF4) places its own bills and stickers on these shafts |
| upper_shaft_dulling | z above 3000: roughness +0.15, a chalky bloom (albedo +6) | Judgement |
| canopy_streaks | 8 to 12 vertical grime streaks from the canopy lip down the bowl, black (40, 38, 36) at 0.35 | Judgement |
| bowl_yellowing | the whole bowl, tint to bowl_unlit_srgb; 12 to 25 dark specks 1 to 3 mm inside it (dead insects) | Judgement |
| bird_marks | the canopy's top, 2 to 3 patches of 20 to 60 mm, white-grey (205, 205, 190) | Judgement; the wear target lists lamp tops as perches |

Not present: lettering graffiti, posters of this target's own (the posters target places bills and stickers on these shafts), reflective or coloured bands, a maker's plate.

### 5.7 The lit lamp: numbers that agree with the night note

The lamp is a 35 W low-pressure sodium lamp, 4,550 lm (Read: the night note, a maker's datasheet by search summary). The game's light for each column, at **(0, 500, 4850)** in the column's frame (the scene's rule: a point light 0.05 m below the centre of the emissive piece), is the night note's:

| light | current game (8 October) | the night note's proposal (section 4 steps 4 and 5) |
|---|---|---|
| pool spot (shadows on, straight down) | 500 lm, inner 22, outer 46 degrees: 261 cd, 11.4 lx straight down from 4.78 m | 350 lm, inner 15, outer 55: 130.6 cd |
| skirt spot (no shadows, straight down, source radius 5 to 10 cm) | none | 800 lm, inner 45, outer 80: 154.1 cd |
| glow (all round, no shadows) | 40 lm (3.2 cd) | 40 lm |
| sum straight down | 11.4 lx | 12.46 lx (the note's 'about 12.5') |
| total lumens | 540 | 1,190, 26 % of the lamp's 4,550 (the note cut the pool on purpose to cure the clipped red; it adds the skirt for the gaps) |
| range | 18 m | 18 m |
| colour (linear) | (1.0, 0.25, 0.0) | (1.0, 0.25, 0.0); the note's try (1.0, 0.40, 0.03) = sRGB (255, 170, 48) |

The cone arithmetic (cd = lumens / (2 pi (1 - cos outer half-angle))) is recomputed in the self-check and reproduces the note's 261 cd, 11.4 lx and 12.5 lx. These are the note's intent, to be tried and measured in the game's own camera (its section 5); this target adds no number the note does not have.

**The colour, and the scene file's mistake.** The scene file's lantern is linear (1.0, 0.7055, 0.0), gamma (255, 219, 0), xy (0.5467, 0.4526), "589 nm". That xy is the colour of about **585 nm** (the printed CIE value at 585 nm is (0.5448, 0.4544); a multi-lobe fit of the colour matching functions, recalled from memory and checked against that value to 0.002, gives (0.5436, 0.4562) at 585 and **(0.5667, 0.4332) at 589**, (0.5684, 0.4315) for the sodium D lines). And its normalisation divided red by the peak but left green and blue undivided: clipped and divided by 2.3766 the scene's own xy gives (1.0, 0.2969, 0.0), not (1.0, 0.7055, 0.0). At 589 nm the same matrix gives (2.731, 0.600, -0.130), clipped and divided by its peak **(1.0, 0.2195, 0.0)** linear = **(255, 129, 0)**: the evening note's (255, 140, 0) and the night note's (1.0, 0.25, 0.0) are within 0.04 and 11. The night note says the game's lamp already is (1, 0.25, 0); the scene file is stale and wrong, and correcting it is a ruling (asked first).

**Glow surfaces.** Bowl: emissive (255, 137, 0) = the night note's lamp gamma-encoded (the lit US01 lantern's median is 251/152/14: within 15). Lamp jacket: emissive (255, 176, 28), brighter and yellower than the bowl (the photograph's clipped core is over-exposure; a sodium lamp's own light is one orange); the bowl at 0.45 of the jacket's brightness. The canopy, the arm and the column stay unlit paint, lit only by the pools. Warm-up (optional): a freshly lit lamp glows dim red-pink for a few minutes before turning orange (evening note section 1). Unlit by day: the bowl clear-yellowed (190, 182, 160) with the jacket (200, 196, 180) and the white reflector seen through it.

### 5.8 Placement

| column | x (m) | side | scene z (m) | z with the corrected 170 kerb (m) | plate | wear seed | dent |
|---|---|---|---|---|---|---|---|
| LC 1 | 8.0 | east | 3.725 | 3.77 | LC 1 | 11 |  |
| LC 2 | 18.0 | west | -3.725 | -3.77 | LC 2 | 18 | yes |
| LC 3 | 28.0 | east | 3.725 | 3.77 | LC 3 | 25 |  |
| LC 4 | 38.0 | west | -3.725 | -3.77 | LC 4 | 32 |  |

The code's loop gives four columns, **20 m apart on each side, 10 m apart along the street, alternating** (SCENE-SLOTS.md's "every 20 m" is the spacing on one side; the posters target's SF4 'x 8, 28, 48' misreads it: the street has columns at 8, 18, 28 and 38 and none at 48). The axis stands 600 mm behind the kerb's BACK face: the scene's kerb top is 125 wide so z = 3.125 + 0.6 = 3.725; the corrected granite kerb top is 170 so the same rule gives 3.77. The rule governs, within a 40 mm tolerance. The arm points at the carriageway, square to the kerb; the door faces the building line; the plate faces the road. The lantern's centre is 0.27 m behind the kerb face (0.5 out from an axis 0.77 behind it), so its pool lands on the flags and the channel.

### 5.9 Edges, bevels, size

Every hard edge is bevelled (mid-poly; the asset plan's method): sleeve top lip (z 978) 1.5, collar top and bottom edges 1.5, door perimeter (outer) 1.0, plate perimeter 0.8, canopy lip's lower edge 1.5, bowl rim bead 3.0, boss end 1.5, catches 2.0, sleeve bottom (z -150, hidden) 2.0 (radii in mm). Triangle budget 3000 to 12000 per column with its lantern at LOD0 (Judgement; four columns are a small share of a frame).

## 6. Variants

| id | name | build | difference and basis |
|---|---|---|---|
| A | steel bent-arm column (this document) | main: 4 of 4 places | all numbers above |
| C | precast concrete shaft, steel bracket and the same lantern | alternative, built only if ruled in | the research's type; NO photograph; every number Judgement or the research's: a square section 220 at the foot (the research's 20 to 25 cm) tapering to 125 at 4700, arrises chamfered 15, the shaft planted (150 hidden) with the paving cut round it; a door recess 120 x 330 x 14 at z 450 to 780 on the -y face with a steel door plate 132 x 342 x 3, 3 proud, two screws, blank; the bracket tube OD 48 entering the top face (top entry), the same bend, rake, boss and lantern; the plate 'LC n' as A; colour (146, 143, 136) with green algae to z 700 on the -y face and rust bleed from the plate's screws; no paint |
| P | post-top dish on the same lower column | not placed (the scene's lamps are bracket lamps) | what BGE shows: the lower column to z 4300 and a dish 420 across (Photo, +-30) of Judgement height 150 centred at 4375; shell dark, underside pale |
| W1 | a wall bracket for the same lantern | optional, not placed; if wanted, a plain gable end, never a shopfront | Judgement only: a wall plate 150 x 220 x 8 with four bolts (domed nuts 24 across), a 42 arm raked 10 degrees from z 4350 to the lantern's boss at y 225 from the wall, a 25 strut from z 4130 to 140 along the arm; the lantern 540 lower than on A (top at 4460). The two wall lanterns reached are a one-off college lantern (Cambridge) and a 2019 estate bulkhead (US02, 235 x 210): neither is a street fitting |

How many the street needs: one column type per scheme (a street's lamps were fitted together), so the four places take A, or all four take C if ruled; the lantern is one pattern in both. The variation between the four is the wear (their seeds, the dent on LC 2), not the form.

## 7. The photographs-win disagreements

| id | what | the stand-in or book says | the photograph or the record says | chosen | kind |
|---|---|---|---|---|---|
| PW1 | the sleeve and the shaft | a base 200 across and 300 high and ONE 114 mm shaft to the top | BGE: a 124 mm black sleeve 978 mm high, a 60 mm cone with a ring line, a shaft 68 mm at the cone tapering to 61 at 3.9 m; US01 the same form (sleeve 2.05 x the shaft) | the photograph's, with the scene's 114 left inside the sleeve's +-9 | Photo |
| PW2 | the bracket | a swan neck of three short cylinders on a quarter circle, rising over the lantern and dropping into it (the code's comment: 'a straight bracket reads as a modern column') | US01: a vertical stem, one tight bend, a straight raked arm entering the lantern's rear end; R07 reads 'plain bent-arm lighting' (production/reference/photographs.md) | the bent arm | Photo + Read |
| PW3 | the lantern's long axis | 0.55 along the street | US01 seen from below: the arm enters the lantern's rear end and the lantern lies along it | along the arm (y); the box's size is kept | Photo |
| PW4 | the lantern's form | a box | US01 lit lantern: a boat-shaped canopy over a bowl that glows orange round a brighter core; the research: 'a boat-shaped canopy 60 to 70 cm long over a deep clear trough-shaped bowl' | canopy over bowl, the lamp visible inside | Photo + Read |
| PW5 | the lantern's colour | linear (1.0, 0.7055, 0.0), gamma (255, 219, 0): a yellow | US01 lit: median 251/152/14 (orange); the night note's lamp (1, 0.25, 0); derived 589 nm: (1, 0.2195, 0) linear = 255/129/0 | (255, 137, 0) for the bowl (the night note's lamp gamma-encoded); the scene's xy is 585 nm, not 589, and its normalisation skipped the division in green | Photo + Derived |
| PW6 | the column's concrete or steel | steel (surface 'metal') | none of the period; the 2019 photographs show steel; the earlier research says concrete | steel main, concrete as variant C: unsettled | Judgement |
| PW7 | the count and places | SCENE-SLOTS.md 'every 20 m, alternate sides, first at 8 m' | the code and pieces file: x 8, 18, 28, 38, east, west, east, west | the code's four | Read |

## 8. The checks for unit 3.8

`target.json` `checks` lists 54: each a name, what to measure, the expected value and the tolerance. Those that matter from the street are the lantern's box (550 x 300 x 200 +-8, centre (0, 500, 4900) +-12, long axis along the arm +-3 degrees, top at 5000 +-10), the sleeve (124 +-9, 978 +-15 high), the shaft's width at 1200, 2500 and 3900 (67.6 / 64.7 / 61.5 +-6), the bracket (stem 42 +-4, rake 40 +-6, bend radius 90 +-40, end at (225, 4930.8) +-12), the door (100 x 500 at z 400 +-10, facing away from the road +-12), the plate, the colours (paint (31, 31, 34) +-12, the bowl's glow (255, 137, 0) +-12), no maker's mark and no lettering but the plate's, the light's place and numbers, and the four places. The profile and silhouette checks are two-way nearest distances (every point of the built outline to the target's outline and back, at most 4 to 6 mm), as the pillar box's.

| name | applies to | measure | expected | tolerance | kind |
|---|---|---|---|---|---|
| pivot_and_datum | whole piece | the pivot (origin) lies on the shaft's axis at the footway surface (z = 0) and the lowest vertex lies between z = -160 and z = -140 | {"origin_xy_mm": [0, 0], "lowest_z_range": [-160, -140]} | 3 | Read (brief: pivot at the base's centre on the ground); the hidden skirt is 150 |
| lantern_top_z | A, C | max z of the lantern's mesh above the footway, mm | 5000 | 10 | Read (scene: mounting height 5.0 m to the lantern's top) |
| lantern_bounding_box | A, C | extent of the lantern mesh (canopy, bowl, catches, hinge; not the boss) along y, x, z, mm | {"y": 550, "x": 300, "z": 200} | 8 | Read (scene 0.55 x 0.30 x 0.20), turned so the long side lies along y |
| lantern_centre | A, C | the lantern's bounding-box centre (x, y, z), mm | [0, 500, 4900] | 12 | Read (scene outreach 0.5 to the centre; top 5000, 200 tall) |
| lantern_axis | A, C | angle between the lantern's long axis and the arm's direction in plan (+y), degrees | 0.0 | 3.0 | Photo (US01: the lantern lies along its arm) |
| lantern_tilt | A, C | angle between the bowl's base plane and the horizontal, degrees | 0.0 | 1.5 | Judgement (level, as the scene) |
| lantern_canopy_rim_z | A, C | z of the canopy's lower edge, mm | 4925 | 6 | Judgement |
| lantern_dome_height | A, C | max z of the canopy minus the z of its lip's top, at y = 500, mm | 63 | 6 | Judgement |
| lantern_plan_silhouette | A, C | largest nearest distance (both ways) between the lantern's plan outline at z = 4925 and the polygon in target.json geometry.A.lantern.plan, mm | 0.0 | 6.0 | Derived from the plan stations |
| lantern_section_silhouette | A, C | the same, for the cross-section at y = 500 and the long section at x = 0, against target_drawing.py's polygons | 0.0 | 6.0 | Derived |
| bowl_base | A, C | the bowl's flat base: z 4800, length (y) and width (x), mm | {"z": 4800, "length": 400, "width": 164} | 8 | Judgement |
| lamp_in_bowl | A, C | the lamp's axis: parallel to y, centre (x, y, z), diameter and length, mm | {"centre": [0, 500, 4872], "od": 54, "length": 310} | 6 | Judgement (a 35 W SOX lamp) |
| lamp_inside_bowl_and_canopy | A, C | the lamp's whole volume lies inside the bowl's and canopy's inner shell: no vertex of the lamp outside the lantern's envelope | true | 0 | Derived |
| glow_surface | A, C | the emissive surface is the lamp's jacket (full strength) and the bowl (translucent, 45 % of the jacket's brightness), nothing else emits: no emissive vertex outside them | {"emissive_parts": ["lamp", "bowl"]} | 0 | Judgement; Photo (US01 lit: the bowl glows orange round a brighter core) |
| glow_colour_bowl | A, C | the bowl's emissive colour, sRGB 8-bit | [255, 137, 0] | 12 | Derived (the night note's lamp (1, 0.25, 0) gamma-encoded); Photo US01 251/152/14 |
| glow_colour_lamp | A, C | the lamp jacket's emissive colour, sRGB 8-bit | [255, 176, 28] | 14 | Judgement |
| arm_stem_od | A | outer diameter of the bracket's stem, mm | 42 | 4 | Photo ratio (US01 0.47 to 0.67 of the shaft's top) + Judgement |
| arm_rake | A, C | angle of the straight arm above horizontal, degrees | 40 | 6.0 | Photo (US01: 41.7 degrees in the picture; true 36 to 44) |
| arm_bend_radius | A, C | centreline radius of the bend, mm | 90 | 40 | Photo-scaled by reach (US01 435 / 1117 x 225 = 88) + Judgement |
| arm_reaches_boss | A, C | the straight arm's end point (y, z), mm | [225, 4930.8] | 12 | Derived |
| arm_continuity | A, C | no gap and no kink: the arm's centreline sampled every 10 mm is continuous (largest step under 12 mm; largest turn between consecutive samples under 8 degrees) | true | 0 | Derived |
| arm_direction | A, C | the arm's plan direction against the carriageway's normal, degrees | 0.0 | 3.0 | Read (scene: the lantern 0.5 out toward the road) |
| sleeve_od | A, P | outer diameter of the sleeve at z = 300 and z = 800, mm | 124 | 9 | Photo (BGE 123.6 +-9; the scene's 114 is inside) |
| sleeve_height | A, P | z where the sleeve's straight side ends, mm | 978 | 15 | Photo (BGE 978 +-10) |
| cone | A, P | outer diameter at z = 1010 (about half way up the cone), mm | 94.1 | 8 | Derived from the profile |
| shaft_od_low | A, P | outer diameter of the shaft at z = 1200, mm | 67.6 | 6 | Photo (BGE 66 to 69) |
| shaft_od_mid | A, P | outer diameter of the shaft at z = 2500, mm | 64.7 | 6 | Derived (linear between the two photographed heights) |
| shaft_od_high | A, P | outer diameter of the shaft at z = 3900, mm | 61.5 | 6 | Photo (BGE 61) |
| shaft_taper_monotone | A, P | outer diameter never increases between z = 1044 and z = 4560 (steps of 100 mm) | true | 0 | Derived |
| collar | A | collar outer diameter and z range, mm | {"od": 67, "z": [4560, 4620]} | 4 | Judgement |
| lower_profile_silhouette | A, P | largest nearest distance (both ways) between the built lower column's outline in the y-z plane and geometry.A.lower.outer_rz mirrored, mm | 0.0 | 4.0 | Derived; the profile is Photo (BGE) |
| door | A | door arc width, height, bottom z, proud, mm | {"arc_width": 100, "height": 500, "z_bottom": 400, "proud": 1.5} | 10 | Judgement (a lead: a modern 5 m stepped column has a 500 x 100 door 400 above the ground; US01: the door outline's top at about 86 % of the sleeve; the research: a door plate about 50 cm up) |
| door_face | A | azimuth of the door's centre against +y, degrees | 180 | 12 | Judgement |
| door_groove | A | joint groove width and depth round the door, mm | {"width": 2.5, "depth": 2.0} | 1.0 | Judgement |
| number_plate | A, C | plate size (arc x height), centre z, face (+y), mm | {"size": [90, 45], "z": 2160, "face": "+y"} | 8 | Photo (BGE: a reference plate at z 2115 to 2200) |
| plate_text_only_lc_n | A, C | the only characters on any surface of the piece are 'LC' and one digit 1 to 4, on the plate | true | 0 | Judgement: no maker, no council, no crown |
| no_maker_marks | all | no text, logo or relief lettering on any mesh or texture except the plate's; in particular none of the makers' names in the earlier research, none on the door, the lantern or the base | true | 0 | Rulings 8 October and brief |
| collar_screws | A | two set screws at azimuth 45 and 135 degrees from +y, heads 10 across, proud 3, mm | {"count": 2, "head_od": 10, "proud": 3} | 1.5 | Judgement |
| boss | A, C | the lantern's rear boss: outer diameter, length, axis rake, mm and degrees | {"od": 60, "length": 55, "rake_deg": 40} | 5 | Judgement |
| paint_black | A, P | mean albedo of the sleeve's undamaged paint, sRGB 8-bit | [31, 31, 34] | 12 | Photo (BGE 31/31/33) |
| paint_gloss | A, P | roughness of the undamaged paint on the sleeve (0 to 1); the upper shaft is 0.15 higher | {"sleeve": 0.42, "upper_shaft_plus": 0.15} | 0.1 | Judgement (the recipe's 0.42; BGE shows gloss worn to semi-gloss) |
| splash_band | A, P | the splash band's height above the footway where the albedo returns to the paint, mm | 250 | 60 | Photo (BGE: z 0 to 250 is 49/46/42) |
| canopy_colour | A, C | mean albedo of the canopy's undamaged paint, sRGB 8-bit | [118, 116, 112] | 18 | Judgement |
| placement_xs | street | the four columns' x, m | [8.0, 18.0, 28.0, 38.0] | 0.05 | Read (pieces file and code) |
| placement_sides | street | the four columns' sides, east first | ["east", "west", "east", "west"] | 0 | Read |
| placement_setback | street | the axis's distance behind the kerb's BACK face, mm | 600 | 40 | Read (scene 0.6) |
| placement_vertical | street | the axis's lean from vertical, degrees (the footway falls 1 in 40 toward the road; the column stands plumb) | 0.0 | 0.3 | Derived |
| light_position | A, C | the point light's position (x, y, z), mm, and the count per column | {"pos": [0, 500, 4850], "count_per_column": 1} | 12 | Read (scene: 0.05 m below the centre) |
| light_pool | A, C | the pool spot: lumens, inner and outer cone, degrees, aimed straight down, shadows on | {"lm": 350, "inner": 15, "outer": 55} | 0 | Read (night note step 4) |
| light_skirt | A, C | the skirt spot: lumens, inner and outer cone, degrees, straight down, no shadows | {"lm": 800, "inner": 45, "outer": 80} | 0 | Read (night note step 4) |
| light_glow | A, C | the all-round glow: lumens, no shadows | {"lm": 40} | 0 | Read (night note, DECISIONS 7 October) |
| light_colour | A, C | the lights' colour, linear sRGB (the night note's lamp, one number to be tried at (1, 0.40, 0.03)) | [1.0, 0.25, 0.0] | 0.03 | Read (night note); NOT the scene's (1, 0.7055, 0) |
| triangles | A | triangle count of one column with its lantern at LOD0 | [3000, 12000] | 0 | Judgement (mid-poly, a bevel on every edge: the asset plan; four columns are about 4 % of a frame) |
| bevels | A, C | every hard edge has a bevel; radii in `bevels` | true | 0 | Judgement (the asset plan's method) |

## 9. What the self-check does

`self_check.py` (A to E and W): **A** every printed number comes back from its file (the scene, the pieces file, the code's loop, the earlier research, the evening and night notes, DECISIONS.md, the kerbs target) and every derived number recomputes (the colour matching functions' fit, the 589 nm colour, the cone arithmetic); **B** the raw photograph rows give the printed numbers; the numbers are re-measured from the reduced previews; the lower column is laid on the BGE strips at a scale fitted on the sleeve alone and its edges fall on the photograph's within the stated error; **C** the drawing runs on target.json alone and its polygons give the target's numbers; **D** the bracket's geometry recomputes, nothing floats (column, arm, boss and lantern are one connected shape), the lamp lies inside the bowl, the light inside the bowl, the wear zones lie on the right faces; **E** no maker, brand, crown or authority's name on any part, only the plate carries letters, none of the content rule's words, the previews obey the brief, this file carries its summary line, the plain statement and every preview's credit; **W** ten deliberately wrong copies of target.json (a 114 sleeve, an untapered shaft, a 30 degree rake, a narrower lantern, the lamp above the bowl, the scene file's yellow, a maker's name on the plate, an arm that misses the boss, columns at 8, 28 and 48, a light above the lantern) must each be refused by at least one test.

## 10. What the target could not settle

- whether 1990's minor street in a northern port town had precast concrete or painted tubular steel columns: no 1990 photograph was reached; steel is the main variant because the only column photographs reached (2019, London) are steel and the scene and recipe assume it; the earlier research says concrete (variant C is written out)
- every BGE and US01 length is +-7 % in absolute size (camera height 1.02 +-0.07 m, 1.16 +-0.07 m); if the BGE sleeve is the standard 114.3 mm tube, all BGE lengths are 7 % smaller
- the bracket's rake (40 degrees is the 11 m column's, from its apparent 41.7 degrees and a nearly side-on lantern; a 5 m column's own rake is not photographed and this writer recalls 5 to 15 for standard raked brackets, no source found, and a search lead says 5 m brackets had a vertical and a horizontal section) and the bend's radius (scaled by the reach)
- the lantern's real length (the research estimates 600 to 700; the scene's 550 is kept) and its canopy and bowl proportions: read from one photograph from below and from the earlier research's words
- the door's real size and place on the steel sleeve (only a faint outline on US01)
- the 35 W SOX lamp's physical size: 54 x 310 is a catalogue table's figure by search lead (a maker's datasheet lead says 52 x 311); no datasheet was reached
- the shaft's top diameter on a BRACKET column: 60 is a post-top column's (BGE); a bracket column of this height may be 76 at the top (a modern catalogue's), the collar then 83 and the stem 48
- the real light: the night note's numbers are its own intent, not measured in the game; whether the orange (255, 137, 0) reads right in the game's camera is for a fresh reviewer to judge against photographs from the PC
- no photograph of a council wall bracket lantern was reached: W1 is entirely Judgement

## 11. To read once the network opens

- dated photographs, 1975 to 2000, of provincial British streets with precast concrete and tubular steel lighting columns and sodium lanterns on brackets, with a person or a kerb in frame for scale: the column's shape, the base (sleeve or concrete foot), the door, the bracket's rake and bend, the lantern's canopy and bowl, their paint (Geograph and Wikimedia Commons, CC BY or CC BY-SA, by date taken)
- the 1989 code for minor roads (BS 5489-3, current from 31 August 1989 to August 1992) for the column heights and spacing the street would have used
- the standard tube sizes of tubular steel columns (BS 1308 / BS 5649 families) and the maker-neutral root-section proportions of a 5 m stepped column
- a SOX 35 W lamp's datasheet: jacket diameter and length, lumens, warm-up curve
- the Middlesbrough Council, Tyne and Wear Archives and North Tyneside albums on Flickr that the earlier research lists (street scenes, for the lamps in the background; licences to be read on each page)
- the earlier research's Geograph 1485521 (a 1950s concrete column), read at its page for the licence and date

## 12. Handover

- **for scene file**: furniture E1 and E2: replace the base 0.2 x 0.3, the 0.114 shaft, the three-cylinder swan neck and the box lantern by the kit piece A at the same four places (x 8 E, 18 W, 28 E, 38 W; axis 0.6 m behind the kerb's back); the lantern's top stays at 5.0 and its centre 0.5 out; its long side now lies along the arm
- **for the night scene**: the point light and the two spots at (0, 500, 4850) in the piece's frame; colour (1, 0.25, 0) linear, not the scene file's (1, 0.7055, 0); the lantern's lamp and bowl are the emissive parts; the scene file's lantern colour needs correcting (a ruling, so asked first)
- **for the wear target**: the lamp-column base foot-splash is the splash_band here (z 0 to 250); the wear target's iron_wear tone row applies to the chips
- **for the posters target**: its SF4 puts bills on the shafts at x 8, 28, 48: the street has columns at 8, 18, 28, 38; the shaft is 61 to 68 across at the bill's height, not 114 (so 'the middle 0.17 m of an A3 shows face-on' becomes the middle 0.09 m)
- **pivot**: the axis at the footway surface; z up; scale 1; one mesh for the column and one for the lantern (the lantern's emissive parts as separate material slots)

## 13. Previews and credits

All photographs: Poly Haven, CC0 1.0, Andreas Mischok, taken 2019-08-18 (BGE and US01); used for measuring only, never placed in the game, traced into a texture or fed to an image model. Each crop is of the object only: the signs on BGE's shaft that carry text, a telephone number or a hand-painted picture are masked flat grey, a parked car is cropped out of US01's base, and nothing else is in frame (no people, no shop names, nothing the content rule bars). The drawings are this target's.

| file (production/previews/cloud-week/refs/lamp-posts/) | what it shows | used for |
|---|---|---|
| bge-bethnal-green-column-strips.jpg | BGE, four strips of the rectified column, z 0 to 4800, 1.2 mm a pixel, signs masked grey | the lower column's measurements (section 4) |
| bge-bethnal-green-column-target-on-photo.jpg | the same with target.json's lower column drawn over it (red lines), scale fitted on the sleeve only; no outline above z 4280 | the drawing check |
| bge-bethnal-green-column-pod.jpg | BGE, the post-top dish seen from below, rectified, 1.5 mm a pixel | the pod's width (variant P) |
| us01-bethnal-green-bent-arm-elevation.jpg | US01, the shaft's top, stem, bent arm and lantern, rectified at 8.8 m, 3 mm a pixel | the bracket's form and ratios |
| us01-bethnal-green-lit-lantern-from-below.jpg | US01, the lit lantern seen from below, 5 degrees wide | the glow's colour; the arm entering the rear end |
| us01-bethnal-green-sleeve-and-shoulder.jpg | US01, the sleeve, shoulder and shaft's foot, rectified, 2 mm a pixel | the stepped form; the door outline |
| hook-sheet-slot-x8-east-target-on-sheet.jpg | variant A at its scene slot laid on the Hook sheet's reduced copy with the sheet's own lens; a placement test, not a measurement | section 3 |

## 14. The numbers that are not printed in the repository

| id | value | unit | kind | source (first 230 characters) |
|---|---|---|---|---|
| bge_sleeve_od_measured | 123.6 | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: left and right edges at z 100 to 800 each 100 mm, mean of 8 rows (120 |
| bge_sleeve_top_z | 978 | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: the sleeve's straight side ends at z 978 (+-10) where the cone begins |
| bge_cone_top_z | 1040 | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: the cone meets the shaft at z 1040 (+-10), a thin ring line there |
| bge_shaft_od_low | 68 | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: 67 at z 1700, 69 at 1800 and 1900 (strong edges against brick), 66 re |
| bge_shaft_od_high | 61 | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: 61 at z 3800, 3900 and 4000 (strong edges against the sky); +-5 |
| bge_pod_diameter_measured | 417 | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: widest run of the pod's silhouette against the sky, 417 (x -193 to +2 |
| bge_pod_centre_height | 4410 | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: from the angles of the pod's limbs (el 53.8 and 48.5 degrees) at the  |
| bge_paint_black_srgb | [31, 31, 33] | sRGB | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: median of the sleeve's face, z 500 to 900 (p10 19, p90 44; the gloss  |
| bge_splash_srgb | [49, 46, 42] | sRGB | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: median of the lowest 250 mm of the sleeve (warm grey-brown road film  |
| bge_scratch_zone | [380, 430] | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: hairline scratches on the sleeve's face at z 380 to 430, no letters |
| bge_plate_z | 2160 | mm | Photo | Photo BGE (bethnal_green_entrance, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.02 +-0.07 m at the column's ground; photo_measurements.json: a small white plate with a short letter-and-number reference at z 211 |
| us01_shaft_top_od | 89.1 | mm | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: mean width of the shaft's top 0.9 m against the sky, z  |
| us01_stem_od | 42.0 | mm | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: the vertical stem above the shaft's collar at z 9800 to |
| us01_arm_od | 59.9 | mm | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: the raked arm's thickness taken vertically 80, times co |
| us01_arm_to_shaft_ratio | 0.67 | ratio | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: arm 59.9 / shaft top 89.1; the stem 42.0 / 89.1 = 0.47  |
| us01_sleeve_to_shaft_ratio | 2.05 | ratio | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: sleeve 232 / shaft 113 read by eye on the gridded eleva |
| us01_lit_median_srgb | [251, 152, 14] | sRGB | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: median of the 66,611 orange pixels of the lit lantern s |
| sleeve_od | 124 | mm | Photo | BGE sleeve 123.6 +-9, rounded to 124 (the scene's 114 lies at its lower edge: kept as a tolerance, not as the value; 114.3 is a standard tube) |
| sleeve_height | 978 | mm | Photo | BGE sleeve top 978 +-10 |
| cone_top | 1038 | mm | Photo | BGE cone top 1035 to 1040 (+-10) |
| shaft_od_at_cone | 68 | mm | Photo | BGE shaft 66 to 69 at z 1100 to 1900 |
| shaft_od_at_top | 60 | mm | Derived | linear taper from 68 at z 1044 to 61 at z 3900 (BGE), carried to the collar's foot (z 4560): 68 - 7 x (4560 - 1044) / (3900 - 1044) = 59.4; set to 60 (60.3 is a standard 2 in tube) |
| weld_ring_height | 6 | mm | Photo | BGE: a thin ring line at the cone's top, z 1036 to 1042 (read by eye on the 4 x crop) |
| us01_arm_apparent_slope_deg | 41.7 | deg | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: the straight arm's centreline fitted over x -1150 to -3 |
| us01_bend_tangent_lengths | [147, 244] | mm | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: from the corner where the stem's line meets the arm's l |
| us01_bend_radius | 435 | mm | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: R = mean tangent length 195 / tan(24 degrees) = 435 (th |
| us01_reach_to_boss | 1117 | mm | Photo | Photo US01 (urban_street_01, Poly Haven CC0, Andreas Mischok, taken 18 August 2019), camera 1.16 +-0.07 m above the footway, column 8.8 +-0.6 m away; photo_measurements.json: from the stem's axis to the arm's end at the lantern's  |
| bend_radius_scaled_by_reach | 87.6 | mm | Derived | 435 / 1117 x 225 (the target's reach to the boss): the bend scales with the reach, not with the tube's diameter (a 9-diameter bend cannot fit 225 mm of reach) |
| rake_deg | 40 | deg | Photo | US01: the arm's apparent slope in the picture is 41.7 degrees; the lantern, seen from below, is nearly side-on (its visible length 0.78 m of about 0.9), so the arm points within about 30 degrees of the picture's plane and the true |
| lantern_rear_end_y | 225 | mm | Derived | lantern centre 500 - length 550 / 2 |
| lantern_front_end_y | 775 | mm | Derived | lantern centre 500 + length 550 / 2 |
| lamp_centre_y | 500 | mm | Derived | the lantern's centre |
| light_z | 4850 | mm | Derived | the lantern's centre z (4900) minus the scene's rule 50 below the centre of the emissive piece |
| paint_black_srgb | [31, 31, 34] | sRGB | Photo | BGE sleeve median 31/31/33 and US01 sleeve 32/33/38 (the sky tints the shaft): 31/31/34 |
| splash_srgb | [49, 46, 42] | sRGB | Photo | BGE lowest 250 mm |
| glow_bowl_srgb | [255, 137, 0] | sRGB | Derived | the night note's lamp (1.0, 0.25, 0.0) linear gamma-encoded: 1.0, 0.537, 0.0; the photograph's lit lantern median 251/152/14 is 15 higher in green |
| derived_xy_585 | [0.5436, 0.4562] | CIE 1931 | Derived | fit of the colour matching functions at 585 nm (compare the scene's 0.5467, 0.4526) |
| derived_xy_589 | [0.5667, 0.4332] | CIE 1931 | Derived | fit at 589.0 nm |
| derived_xy_d_lines | [0.5684, 0.4315] | CIE 1931 | Derived | equal-weight mean of the sodium D lines at 589.0 and 589.6 nm: (0.5684, 0.4315); the evening note's 0.569, 0.430 agrees |
| derived_scene_raw_linear | [2.3764, 0.7055, -0.1351] | linear sRGB, unclipped | Derived | the scene's xy through the sRGB D65 matrix: (2.3766, 0.7055, -0.1351), as the scene's note says |
| derived_scene_clipped_normalised | [1.0, 0.2969, 0.0] | linear | Derived | clip the negative blue and divide by the peak 2.3766 -> (1, 0.2969, 0): the scene's (1, 0.7055, 0) skipped the division in green |
| derived_589_linear | [1.0, 0.2195, 0.0] | linear | Derived | 589 nm (D lines) through the same matrix, clipped and divided by its peak 2.7312: (1, 0.2195, 0) |
| derived_589_gamma_8bit | [255, 129, 0] | sRGB 8 bit | Derived | the same, gamma-encoded: 255, 129, 0 (the evening note's 255, 140, 0) |
| cd_current_pool | 260.6 | cd | Derived | 500 lm / (2 pi (1 - cos 46 deg)) = 260.7: the night note's 261 |
| lux_current_pool | 11.41 | lx | Derived | 261 cd / 4.78 m squared = 11.41: the night note's 11.4 |
| cd_proposed_pool | 130.6 | cd | Derived | 350 lm / (2 pi (1 - cos 55 deg)) = 130.6 |
| cd_skirt | 154.1 | cd | Derived | 800 lm / (2 pi (1 - cos 80 deg)) = 154.1 |
| lux_proposed_peak | 12.46 | lx | Derived | (130.6 + 154.1) / 4.78 squared = 12.46: the night note's 'about 12.5 lx' |
| proposed_total_lumens | 1190 | lm | Derived | pool 350 + skirt 800 + glow 40 = 1190 lm, 26 % of the lamp's 4,550 lm (the night note cut the pool on purpose; see TARGET.md section 8) |
| proposed_share_of_lamp | 0.262 | ratio | Derived | 1190 / 4550 |
