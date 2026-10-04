# Brick methods (research, 4 October 2026)

Extends BRICK-2026-10-04.md. O = opened, S = search summary only, I = inference; [n] = sources.

## What the failures say (I)

- The scan reads real through photographed pitting, chipped arrises and fire-flash per brick; ours lacks that, not the bond.
- DBuffer decal colour is a lerp, Source·α + Dest·(1−α); the multiplying Stain mode was UE4 [1 O]. Dark over dark changes nothing.
- Tint below in-house spread: shrink the spread; move houses in hue and mortar.

## Methods, ranked by fit, then cost

1. **Photographed bricks baked into our bond, offline.** Cut hundreds of stretcher and header faces (height, normal, roughness) from 8K CC0 scans; the generator pastes one per cell by ID (random pick, flip, graded), scan mortar between. This is Substance's Tile Sampler (image inputs picked at random per tile, six at most [2 O]); Adobe called re-laying bricks cut from a scan "pretty complicated" in Sampler [3 O]. Free equivalent: Material Maker (MIT), bricks node with Flemish and English Bond and per-brick UVs [4 O]. No extra runtime samples. VRAM (I): 8K set about 180 MB, 4K 45 MB. A wall 2 m off at 2560 px needs 0.64 to 0.9 px/mm (90° to 70° FOV) (I); 8K over 7 m gives 1.17, 4K 0.59.
2. **Runtime per-brick atlas.** ID texture gives brick index and local UV; the shader picks a cell from frac(id + seed), so each house gets different bricks. Engine BrickAndTileUVs is running bond only [5 O]. Use derivatives of the unbroken UV, as TextureVariation's note advises [5 O]; pad cells. About six samples against three (I). Only if 1 still repeats.
3. **Detail map near camera**: high-passed scan relief into albedo and normal (engine DetailTexturing [5 O]), faded beyond about 6 m. Two samples (I).
4. **Wear in the material**: generator masks in UV2 (soot, wash, algae, splash, repair), one sample (I). Pros paint vertex channels, red dirt and green weathering [6 O], "for creating variety among similar meshes" [7 O]. Physics: black crust where sheltered from rain, washed faces clean [8 O, 9 S]; limestone sills shed white lime run-off [8 O]. So: base albedo clean fired brick, lighter than now; soot darkens and mattes eaves, sill undersides, reveals; streaks under sills lighter; algae shifts hue; roughness moves with each.
5. **Decals for light or coloured specifics** (lime run-off, patches), writing colour, normal, roughness [1 O].
6. **Texture bombing, hex tiling**: mortar and grain only. Texture_Bombing "uses multiple offset texture samples" [5 O]; hex-tiling is wrong for brick courses [10 S]; code MIT [11 O]. Three or four samples a map (I).
7. **Mortar recess at the near corner**: engine POM [5 O] within about 8 m, costly per pixel (I); or geometry.
8. **A bigger scan alone**: largest true-scale CC0 is about 3 m; repeats on a 6 m front, bond fixed (I).

## Mortar and per-house reading

- Mortar is 17 to 19% of a face (215 × 65 brick, 10 mm joints) (I): its colour moves distant tone more than a 10% brick tint.
- Black ash mortar was real: Sheffield c.1880, "coal ash dust and quicklime" [12 O]; South Wales [13 O]; Yorkshire [14 S]. Ours failed by being flat, not dark (I). Per house: buff lime, grey, black ash, cement patches.
- Per house (I): one brick family (red, red-brown, buff, plum); in-house spread under half the step between neighbours; measure mean colour per front at 30 m on the hook frame.

## Free assets (CC0 [15 O, 16 O], via APIs [17 O]; bond from previews, I)

- Poly Haven brick_wall_006: 3 m (39 courses, consistent), 8K, diffuse JPG 47 MB; Flemish-like, irregular. Main donor.
- Poly Haven church_bricks_02: 2 m listed, 8K, 24 MB; headers and stretchers mixed.
- Poly Haven red_bricks_04: 2.5 m, 8K, 11 MB; headers present.
- Poly Haven brick_wall_001: 3 m listed, about 1.2 m by courses, 8K; stretcher; fire-flashed bricks.
- ambientCG Bricks026, Bricks077: size unlisted, 8K; English or Flemish, check full size.
- ambientCG Bricks104: 8K; English, clean modern.

Stretcher only: PH brick_wall_11 (4 m), red_brick (16K); ambientCG Bricks085, Bricks074. Nothing tagged Flemish. The API gives brick_4 as 0.5 m, not our 1.05 m: check. Poliigon's Flemish texture is off the allowlist (S).

## What to build, in order

1. Cut 300+ stretchers, 100+ headers from brick_wall_006 and church_bricks_02; grade neutral.
2. Generator pastes one per cell, scan mortar; 8K over 7 m; Flemish and garden-wall.
3. Lighter base, smaller spread; brick family and mortar per house (Custom Primitive Data).
4. UV2 wear: soot dark and matte, washes light.
5. Detail map near; POM if corner joints read flat.
6. Runtime atlas if a repeat remains.
7. stat gpu on the hook frame.

## Unreached

The Order: 1886 notes; Gears of War 4 layered-material talk; Spider-Man Manhattan talk; City Sample materials; KCD2 material talks; JCGT hex-tiling; ambientCG file sizes.

## Sources

1 Epic, Decal Materials (UE5). 2 Adobe, Tile Sampler docs. 3 Adobe Community, Extracting bricks from i2m, 2024. 4 Material Maker bricks3.mmg (GitHub). 5 UE_5.8 Engine/Content/Functions. 6 Godillon, 80.lv London, 2024. 7 Vinci, 80.lv Victorian street, 2017. 8 Designing Buildings, Pattern staining. 9 Bilbao black-crust study 2017; NPS Brief 1. 10 forge-engine issue 66. 11 mmikk/hextile-demo. 12 periodproperty.co.uk, black ash mortar. 13 rounded-developments.org.uk. 14 Yorkshire Lime Company. 15 polyhaven.com/license. 16 docs.ambientcg.com/license. 17 api.polyhaven.com; ambientcg.com/api/v2.
