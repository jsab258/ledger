# Step 9 sheets reading: stone and metal, 3 November 2026

Read 3 November 2026. Allowlist read first (ledger-v2/research/license-allowlist.md, ship-safe item 2: CC0 libraries Poly Haven and ambientCG are allowed).

## 1. On disk
- production/assets/scanned/polyhaven/materials.json (2k maps; covers_m read from the file): brick_4 1.05 m; brick_wall_001 1.05 m; concrete_pavement_02 3.6 m (flags); asphalt_01 2.08 m; painted_concrete_02 4.0 m (smooth lightly worn paint; no covers_note). Folders hold diff, nor_dx, rough, ao at 2k. No stone, lead, cast-iron or metal texture there.
- ledger/Assets/StreamingAssets/CityPack/textures: concrete, plaster, metal, kerb, sidewalk, setts, roof, wood, brick_grey/red, glass, window, asphalt (each with _n, _r; some _b variants). Resolution and metres covered: not read, unverified.
- F:/LedgerTools/polyhaven: about 1,300 files, almost all 1k glTF props with texture maps (watch, camera, toolbox, etc.). Surface-like items: painted_plaster_wall (1k model, CC0, source.json), worn_metal_rack, metal_* props. No stone or gutter sheet found by a name search; the folder was not fully listed (only the first 100 of 1,302 files plus a name search), so unverified.
- F:/LedgerTools/fab: MetaHuman garment packages only. F:/LedgerTools/game-inputs: gasp, fab-check, pipeline caches, glass-bake; no textures.
- ps5-corner.json has covers_m on rows at lines 355, 389, 423, 439, 457, 475; 439 and 457 (1.0 m) were not opened.
- Result: the gap is real; nothing on disk serves as a stone or painted-metal sheet.

## 2. What the project's notes say
- production/research/asset-plan/1-BUILDINGS-AND-INTERIORS.md line 112: heads "stone lintel, concrete lintel"; sills "stone with drip, brick-on-edge, tile". Line 116: rainwater "cast-iron ogee and half-round gutters, grey or black plastic gutters (1970s on), downpipes with shoes and hopper heads". Lines 124-127: the three sheets (timber; stone, stucco and concrete; metal). Line 149: alterations include "a rendered or pebbledashed front, painted brick, a little stone cladding".
- TERRACE-KIT-TABLE-2026-10-29.md line 39: upper lintel "flat stone, about 330 mm deep"; line 58: sill 150 high (stone, SW 127 x 50.8); lines 61-62: gutter 112 half-round, downpipe 68; line 116: modular_metal_gutter a candidate. Gutter and downpipe sizes are marked U (unmeasured).
- FLAGS-BRICK-BANDS-2026-10-29.md line 42: sandstone reflectance 0.20 to 0.45.
- south-quay/METHOD-2026-10-06.md lines 122, 132: "stone sills" and "stone sills and lintels".
- No note found saying lead downpipes, nor that 1990 gutters were mostly cast iron or plastic on this street; terrace-front.py gives the downpipe a "lead" row (per STEP9-READING). Painted-stone sills and concrete lintels: only listed as options. Period gutter material for the corner: unverified, a project choice.

## 3. Outside candidates (pages read in full, 3 November 2026; all state CC0)
Stone:
- large_sandstone_blocks, https://polyhaven.com/a/large_sandstone_blocks : CC0; 3 m; 1k 3.4, 2k 6.8, 4k 13.7, 8k 27.3 px/cm (so 1k about 340 px/m, 2k about 680 px/m); tags include trimsheet, grey, stained; author Rob Tuytel (API info). Earlier note WINDOWS-FACADES-2026-10-04.md line 33 had already named it for sills and plinths.
Stucco and plaster:
- white_stucco, https://polyhaven.com/a/white_stucco : CC0; 2 m; 1k 5.1, 2k 10.2, 4k 20.5, 8k 41 px/cm (1k about 510 px/m, inside the 20% band). Author Amal Kumar.
- Other plaster ids from the API list (https://api.polyhaven.com/assets?t=textures&c=plaster), sizes in mm: worn_plaster_wall 1.8 m, plastered_wall_02 2.23 m, grey_plaster 1 m. Pages not opened; licence unverified for these.
Metal:
- rusty_painted_metal, https://polyhaven.com/a/rusty_painted_metal : CC0; 2.2 m; 1k 4.7, 2k 9.3 px/cm. Corrugated painted sheet, wrong profile for round gutters.
- painted_metal_shutter, https://polyhaven.com/a/painted_metal_shutter : CC0; 2 m; 1k 5.1 px/cm (1k about 510 px/m). Corrugated.
- modular_metal_gutter, https://polyhaven.com/a/modular_metal_gutter : CC0; model 2.3 m wide; 1k 2.7, 2k 5.4, 4k 10.9 px/cm. A model, so its own UVs, not a tiling sheet; its colour/material not inspected.
- ambientCG licence page (https://docs.ambientcg.com/license/): "All ambientCG assets are provided under the Creative Commons CC0 1.0 Universal License."

## 4. Not reached
- ambientCG asset listing pages returned only filter categories, no asset ids; no ambientCG stone or painted-metal asset page was read, so none is offered.
- Poly Haven API "info" field gave no licence (page text states CC0). Real-world size from the page; the API gives mm.
- Downloads not attempted. Pictures of the candidates were not looked at; "looked at before use" is still owed.

## 5. Gap
- Stone: no scanned stone sill/lintel sheet on disk; large_sandstone_blocks is the one CC0 candidate found. Stucco: white_stucco fits the density. Metal: no flat painted cast-iron texture found; the Poly Haven candidates are corrugated, and the gutter is a model.
