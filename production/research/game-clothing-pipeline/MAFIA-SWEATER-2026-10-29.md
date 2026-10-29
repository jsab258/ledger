# One Mafia knitted top, for Tom's plain jumper (29 October 2026)

Reference first: Tom's jumper starts from Mafia: The Old Country's one knitted top. Method and numbers only.

**Status: partial.** The property files answer questions 1, 4 (density) and 5. The mesh was not exported, so rib edges (2), weights (3) and ridges per cm (4) are not measured.

## Questions

1. Sweater_001_Hero_Race: triangles per level of detail (LOD), materials, textures; is it worn under a jacket (outfit tables)?
2. Rib cuffs, hem and neck band: separate pieces or one shell; geometry (lip, facing, cap) or only the normal map; the cuff's stand-off from the wrist?
3. Weights at wrist and hem: bones and shares in the last 2 cm.
4. Texel density, and the knit's normal-map scale (ridges per cm).
5. Other knitted tops in Male/Clothing/Top.

## Sources

S1 to S5, S7 and S8 sit under F:\LedgerTools\aaa-study\mafia\exports\MafiaTheOldCountry\Content\Nero\ (Study 6's exports, 25 October). All figures read or computed on 29 October 2026.

| Tag | File |
|---|---|
| S1 | Characters\Male\Clothing\Top\Sweater_001_Hero_Race\SK_Ma_Sweater_001_Hero_Race.json |
| S2 | its Materials\*.json (colourways a to f, glove, scarf) |
| S3 | its Textures\*.json |
| S4 | Materials\Functions\Characters\OutfitMatLayerLibrary\Fabric\MLI_CharacterWoolKnit_01a*.json |
| S5 | Materials\Base\Character\CharacterArrays\T_Character_Atlas_N.json |
| S6 | F:\LedgerTools\aaa-study\mafia\study-6\presets.csv, outfit_datatable_rows.csv, garment_meshes.csv |
| S7 | Top_008_Hero, VestJacket_004 (mesh; MI _l), Top_004_Bandit, Top_003_* under Characters\Male\Clothing\Top |
| S8 | the sweater's skeleton, post-process graph and Control Rig; Shirt_002_Hero\SK_Ma_Shirt_002_Hero_Physics.json; Skeleton\SKEL_Male_Skeleton.json |
| J | production/research/game-clothing-pipeline/MAFIA-JACKET-2026-10-28.md |

## 1. Counts, materials, textures, outfits

**One mesh, eight sections and eight material slots at every LOD** [S1]: body, gloves, scarf, rifle strap, two holsters, long sleeves, rolled-up sleeves.

| Triangles | LOD0 | LOD1 | LOD2 | LOD3 |
|---|---|---|---|---|
| Whole mesh | 41,204 | 18,879 | 10,300 | 3,560 |
| Body | 16,526 | 6,720 | 3,691 | 1,320 |
| Long sleeves | 2,880 | 1,388 | 761 | 312 |
| **Jumper (body + long sleeves)** | **19,406** | **8,108 (42%)** | **4,452 (23%)** | **1,632 (8%)** |
| Rolled-up sleeves | 2,449 | 1,230 | 640 | 278 |
| Gloves / scarf | 6,376 / 6,141 | 3,098 / 3,170 | 1,684 / 1,767 | 510 / 572 |

- Jumper vertices: 11,050, 4,946, 2,869, 1,202. Screen sizes 1.0, 0.4, 0.15, 0.08 [S1].
- LOD1 to LOD3 are engine reductions of LOD0: 50% of vertices, 25% of triangles, 12% of vertices [S1].
- At most 8 influences at LOD0 and LOD1 (gloves 7), 4 at LOD2 and LOD3 [S1].
- No cloth asset, no morph targets [S6].

**Material** [S2]:
- One layered master; body and both sleeve slots share one instance; six colourways.
- Cloth shading, masked blend (clip 0.333).
- Five layers: wool knit (base), cotton canvas, plastic, stitches, leather, picked by ID masks (IDs 1 to 4).

**Textures** [S3]: colour with occlusion (DXT5), normal (BC5), one packed map (BC7). All imported at 4096, shipped at 2048; the gloves' normal ships at 1024.

**Outfits** [S6]:
- 18 rows: Sweater_001 shows everything; Sweater_002 sets the scarf slot to an invisible material (MI_InvisibleDummyFast); Sweater_003 hides scarf and gloves. Six colourways each.
- 10 presets, all the player's racing outfits (OP_Ma_Player_006_Racer_*) on the hero body, with Pants_034_Hero.
- **Never under a jacket:** the Top slot holds one garment, and none of the ten has a one-piece.

## 2. Rib edges (not measured)

- **No rib section or material** [S1, S2]. Cuffs, hem and neck band sit inside the body or sleeve sections (inferred from slot names; UNVERIFIED).
- **One knit layer, tiled evenly** [S2, S4]. A rib that differs from the body knit must come from the baked normal or from geometry; which is UNVERIFIED.
- Lip, facing, cap, wall and stand-off: UNVERIFIED. No male body mesh is kept (the jacket extract was deleted on 28 October, DECISIONS.md 16:38).

## 3. Weights (not measured)

- **Own skeleton** [S8]: 271 bones, the male skeleton less 20 gameplay helpers (camera, alignment, foot-contact, asset bones) plus 19 strap and holster bones. The 20 flap bones the jacket weights at its hem (J) are present; whether the sweater uses them is UNVERIFIED.
- **LOD3 removes 187 bones** [S1]: both forearm twist joints, wrist and forearm helpers, upper-arm twist and corrective joints, many other helpers, and three fingers. Thumb, middle finger and flap bones stay. At LOD3 the cuff follows lower arm and hand only. (The engine hands a removed bone's weight to a kept parent: engine behaviour, not read here.)
- **Skinning only.** Its post-process graph [S8] copies the body's pose, runs a Control Rig of aim and parent constraints on the strap's bones (purpose inferred) and a rigid-body node simulating the holster.
- Shares in the last 2 cm: UNVERIFIED.

## 4. Density and knit scale

**Density** from the engine's stored UV density per slot (cm per UV unit) [S1]:

| Slot | cm per unit | px/cm at 2048 |
|---|---|---|
| Body | 127.5 | 16.1 |
| Long sleeves | 130.2 | 15.7 |
| Rolled-up sleeves | 137.0 | 14.9 |
| Scarf | 128.0 | 16.0 |
| Gloves | 42.3 | 48.5 (24 at the shipped 1024 normal) |

- **Checked:** the jacket's stored figure, 172.9 (11.85 px/cm) [S7], matches its measured 11.9 (J); first UV set only (its second set measured 79, stored 2,171).
- About 35% denser than the jacket.

**Knit** [S4, S5]:
- The wool knit is tiled **18 times per UV unit** in all six colourways; normal strength 3 (base 5).
- It reads slice 49 of a 65-slice fabric array, **256 px per slice** as shipped.
- **If it tiles on the first UV set** (UNVERIFIED: the graph is cooked out), one repeat is 127.5 / 18 = **7.1 cm**, about 36 px/cm of knit detail.
- **Ridges per cm: not measured.**
- **Method:** the knit is a shared tiling layer; the garment's own normal map carries its folds and seams.

## 5. Other knitted tops

- **None.** The knit layer appears only in the sweater and in one VestJacket_004 colourway (_l), as its base layer; which part that covers was not read [S7].
- Top_004_Bandit's "Wool" slot is named "haircards": fleece from hair cards, not knit [S6, S7].
- Top_003_Bandit and Top_003_Hero use felt and poplin layers [S7].
- **Top_008_Hero has the same sleeve pair** (long 3,454, rolled-up 2,407, body 21,112 triangles): swappable sleeve sections are a hero-garment method [S7].

## What could not be reached

- **The mesh, its normal map and the knit slice.** FModel exports only from right-click menus; its menu bar and buttons hold no export command. Simulated mouse input to open those menus was refused by the session's permission guard on 29 October, so nothing was exported.
- How the game picks the sleeves (both slots carry the sweater material in every row); the knit's UV set; the Control Rig's purpose; the hero body.

## For Tom's jumper

1. **About 19,400 triangles at LOD0, then about 42%, 23% and 8%** (8,100, 4,450, 1,630), at screen sizes 1.0, 0.4, 0.15, 0.08: Mafia's jumper is 19,406 [S1], inside Tom's 15,000 to 20,000.
2. **Sleeves in their own section; cuffs and collar band apart from what the zip jacket covers.** Mafia hides parts by setting a slot to an invisible material [S1, S6]; under Tom's jacket the covered parts can be hidden while cuff and collar show (LEDGER's choice, from that method).
3. **Author at 4096, ship at 2048, about 16 px/cm** (127.5 cm per UV unit); colour with occlusion, normal (BC5), one packed map [S1, S3].
4. **The knit as a tiling detail normal, not baked:** about 18 repeats per UV unit, about 7.1 cm each (UV set UNVERIFIED), a 256 px tile, about 36 px/cm; bake only the jumper's folds and seams; cloth shading [S2, S4, S5].
5. **Influences 8 at LOD0 and LOD1, 4 below.** By LOD3 drop the forearm twist and wrist helpers, and check the cuff still holds on lower arm and hand [S1].
6. **Skinning only:** no cloth, no morphs; a post-process graph only for attachments [S1, S6, S8].
7. **The rib edge stays open until the mesh is measured.** Meanwhile start the cuff from the jacket's sleeve end: a rounded lip about 0.45 cm, a turned-in facing, a hidden cap, rings about 1 cm apart in the last 2.5 to 5 cm (J, sections 2 and 3). Then measure this sweater by the jacket's method (section, ray, crossings, shares).

## Record

- **Extract folder** F:\LedgerTools\aaa-study\mafia\sweater-2026-10-29: 0 bytes, nothing exported. F: had 28.7 GB free (retention.py: GO).
- **The key:** set in FModel's settings by script for one run, blanked after FModel closed. Check: main key empty, no dynamic keys, no 64-hex string in the file or in the scratch, extract and log folders.
- **One misplaced click:** the first right-click hit the title bar of a LedgerProbe window over FModel; a capture showed no menu left open.
