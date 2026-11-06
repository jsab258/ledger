# inZOI clothes, read from its own files, 6 November 2026

Source: C:\Games\inZOI.v0.10.1\inZOI.v0.10.1\game (v0.10.1), packed containers opened with the Silent Hill 2 reader and the key file on F: (by path only). Study-only; nothing from the game is kept in LEDGER or git. "Measured" = read from the named file; "inferred" = reasoning, unverified. Counts here are for adult-body garments; folders for the youngest bodies exist and are left out. Extracted material (tables and Lua, about 60 MB) deleted after reading.

## Questions

1. Folder layout of garments. 2. One skeletal mesh per garment or per character. 3. Counts of garment meshes. 4. Triangles, levels of detail, bones, materials for a sample of about 20 garments. 5. Texture sizes. 6. Signs of simulated cloth. 7. Signs of morph fitting to bodies.

## Answers

### 1. Folder layout

- Measured (file listing of 258,469 files): garments live under BlueClient\Content\Characters\Costumes\{Female, Male}\ (plus folders for the youngest bodies, not read), 21,968 files in all there (12,337 of them material instances named MI_*, 1,896 skeletal meshes named SKM_*). Beside it Characters\Anims (14,651 files), Characters\AvatarParts (4,783), Characters\Materials (1,021), Characters\Skeletons (5), Characters\Meshes (1).
- Second level by use: Top, Bottom, Full (dress and one-piece), Outer, Shoes, Under, Acc (hats, scarves, gloves, necklaces and the like), Custom (the "CT" parts), Unique (job and event outfits).
- Third levels by type, for example Female\Top\Sweater\Knit\Knit012\, Female\Bottom\Pants\Long\Pants_L002\, Female\Bottom\Skirt\Short\Skirt_S007\, Female\Full\Dress\Long\Dress_L003\, Male\Outer\Jacket\JK010\. Each garment folder holds Mesh\, Materials\ and Textures\.
- Inside Mesh\, the garment is a file SKM_{F|M}_Costume_{kind}_{name}.uasset and, for most tops, bottoms and full garments, a second file with suffix _Jacket (316 such files across female and male) (measured by name).
- Inside Materials\, one MI_* file per colour variant (7 to 15 in the samples below; a variant name ends _001, _CT001 and so on). Inside Textures\, usually four maps per material by suffix: D (colour), N (normal), M (mask), ARM (ambient occlusion, roughness, metal packed).
- Data tables that list garments are in Content\Data\JsonResult\ (Garment*Mesh.json, Garment*.json, Costume.json, ClothingRackOutfitPool.json); layout of fields below.

### 2. One mesh per garment or per character

Measured: one skeletal mesh per garment (SKM_* files per folder above; the table field Mesh holds a skeletal mesh path per row), with SkinningTarget "Body" in every row of every garment table read (GarmentTopMesh.json 7,061,696 B; GarmentBottomMesh.json 4,130,170 B; GarmentFullMesh.json 5,489,264 B; GarmentJacketMesh.json 4,883,030 B; GarmentShoesMesh.json 3,196,748 B; GarmentHatMesh.json 3,316,066 B; GarmentScarfMesh.json 227,120 B; GarmentGlovesMesh.json 364,902 B; GarmentSocksMesh.json 1,292,656 B; GarmentInnerTopMesh.json 152,320 B; GarmentInnerUnderMesh.json 252,612 B). Gender and age have separate rows linked by two small maps (MatchingGenderId, MatchingBodyAgeId). The character's own body is separate: AvatarParts\Body\Female\Mesh\SKM_Female_Base.uasset (2,938,236 B), Male and further body parts, heads under AvatarParts\Heads (171 male, 165 female files), hair under AvatarParts\Groom\Hair (3,134 files). Measured, UB1AppearanceComponent.lua: the component holds a merged body mesh, merged head mesh, merged face-hair mesh and a merged garment mesh, and notes "when there is no mesh merge" separate foot, toe and face-hair mesh components exist. Body shape rows (AppearanceBodyShape.json, 71 rows) carry a flag bUseMeshMerge, true in all 71. Inferred: garments are merged with the body into one skeletal mesh at run time, with a non-merged fallback.

### 3. Counts

- Skeletal meshes under Costumes, adult folders (measured, by folder from the file list): Custom 348 (female 211, male 137), Acc 268, Top 250, Full 167, Bottom 161, Shoes 118, Under 102, Outer 93, Unique 97; total 1,604 files. Files with the _Jacket suffix among all of them: 316.
- Table rows for adult bodies, and distinct skeletal meshes behind them (measured; a row is a colour or layer variant, many rows share a mesh): Top 1,792 rows, 295 meshes; Bottom 1,151 rows, 141; Full 1,152 rows, 170; Jacket 1,403 rows, 93; Shoes 874 rows, 122; Hat 811 rows, 152; Gloves 82 rows, 10; Socks 210 rows, 22; Scarf 48 rows, 8; Inner top 52 rows, 5; Inner under 90 rows, 9.
- Materials per row, all adult-or-youth rows of each table (measured, field OverrideMaterial): Top 0 to 2 (164 rows with 0 and "bRequireCustomParts" true), Full 1 to 3 (1,514 with 1, 165 with 2, 42 with 3), Jacket 1 or 2, Hat 1 or 2, Bottom 1, Shoes 1.

### 4. Triangles, levels of detail, bones, materials: sample of 20

Result: the numbers failed to read. Both engine settings tried on the first sample files (GAME_UE5_4 for the first 21, then GAME_UE5_5 and GAME_UE5_6 on three) gave: "Read size is bigger than remaining archive length" (UE5_4, UE5_5, at 99.7 percent of the file with UE5_5) or "Package has unversioned properties but mapping file is missing" (UE5_6). No mappings file exists on this PC and none was fetched, so triangles, levels of detail, bones and material slot counts of the 20 meshes below are unread. Textures failed the same way.

What was measured instead, per sample (package file bytes of the mesh's .uasset; no separate .ubulk exists for any of them; number of meshes in the Mesh folder; number of MI files in Materials):

| Garment (under Costumes) | Mesh file | Bytes | Meshes in folder | MI files |
|---|---|---|---|---|
| Female\Top\Sweater\Knit\Knit012 | SKM_F_Costume_Top_SW_Knit012_Jacket | 764,025 | 2 | 7 |
| Male\Top\Shirt\Short\Shirt_S005 | SKM_M_Costume_Top_Shirt_S005 | 377,933 | 1 | 0 |
| Female\Bottom\Skirt\Short\Skirt_S007 | SKM_F_Costume_Bottom_Skirt_S007_Jacket | 3,822,140 | 2 | 7 |
| Female\Bottom\Pants\Long\Pants_L002 | SKM_F_Costume_Bottom_Pants_L002_Jacket | 768,472 | 2 | 14 |
| Male\Bottom\Skirt\Short\Skirt_S001 | SKM_M_Costume_Bottom_Skirt_S001_Jacket | 1,435,916 | 2 | 15 |
| Female\Full\Dress\Long\Dress_L003 | SKM_F_Costume_Full_Dress_L003 | 3,015,122 | 2 | 7 |
| Male\Full\Dress\Long\Dress_L001 | SKM_M_Costume_Full_Dress_L001 | 4,404,454 | 2 | 15 |
| Female\Outer\Vest\Vest004 | SKM_F_Costume_Outer_Vest004 | 988,051 | 1 | 1 |
| Male\Outer\Jacket\JK010 | SKM_M_Costume_Outer_JK010_Open | 869,185 | 2 | 14 |
| Female\Shoes\Sneakers\SNK006 | SKM_F_Costume_Shoes_SNK006 | 413,690 | 1 | 7 |
| Male\Shoes\Swim\Swim003 | SKM_M_Costume_Shoes_Swim003 | 251,196 | 1 | 2 |
| Male\Acc\Hat\Hat023 | SKM_M_Costume_Acc_Hat023_Gem | 195,504 | 3 | 5 |
| Female\Under\Top\Top003 | SKM_F_Costume_Under_Top003 | 192,601 | 1 | 7 |
| Male\Under\Socks\Socks_012 | SKM_M_Costume_Under_Socks012_Heel03 | 210,729 | 4 | 0 |
| Female\Unique\Job\Repair\Repair001 | SKM_F_Costume_Unique_Job_Repair001_Hat | 234,148 | 2 | 5 |
| Male\Unique\Job\Repair\Repair002 | SKM_M_Costume_Unique_Job_Repair002 | 1,394,748 | 2 | 2 |
| Female\Custom\Necklace\Pendant | SKM_F_Costume_CT_Necklace_Pendant005 | 75,825 | 16 | 8 |
| Male\Acc\Scarf\Scarf001 | SKM_M_Costume_Acc_Scarf001 | 1,435,522 | 1 | 15 |
| Male\Acc\Gloves\Gloves004 | SKM_M_Costume_Acc_Gloves004 | 309,952 | 2 | 10 |
| Female\Acc\Necklace\Neck002 | SKM_F_Costume_Acc_Neck002 | 536,673 | 2 | 14 |
| Female\Bottom\Pants\Long\Pants_L011 | SKM_F_Costume_Bottom_Pants_L011 | 392,770 | 2 | 7 |

(The MI count of 0 for some rows is a counting miss: the shirt row's material folder is spelled "Materilas" in the game, and the socks folder lists meshes only; so the counts for those rows are unread, not zero. Measured for the shirt: 4 MI files in "Materilas".) The mesh file sizes run from 75,825 to 4,404,454 bytes; dresses and skirts are the largest of the sample (3.0 to 4.4 MB), shoes and hats the smallest garments (195,504 to 413,690). The player body mesh SKM_PlayerMale.uasset is 6,243,072 B; SKM_Female_Base 2,938,236 B. Bytes are not triangles.

### 5. Texture sizes

- Not read as dimensions (the texture packages failed as above). Measured, byte sizes of the .ubulk bulk files beside each texture package, per type across the 15 of the 20 samples that have textures (Swim003 has three maps, Scarf001 none): D (colour) from 147,972 to 1,701,640 B; N (normal) from 221,956 to 1,701,640 B; M (mask) from 110,980 to 850,824 B; ARM from 110,980 to 850,824 B. The values cluster at 110,980, 221,956, 258,948, 517,892, 850,824 and 1,701,640 B; each step is roughly 2 to 3.3 times the last. Inferred and unverified: these are about 512, 1024 and 2048 pixel class maps, the colour and normal maps being the larger; the format was not read.
- Usually four maps per material (D, N, M, ARM), measured by file names; the colour variants share the maps of their garment (the MI files are 1,377 to 3,207 bytes each; one set of maps beside 7 to 15 MI files) (inferred from sizes and counts).

### 6. Signs of simulated cloth

- Measured: no physics asset or cloth asset file sits beside the garment meshes: among all Costumes files only one file name contains "Physics" (Female\Unique\Event\Costume\Cat001\Mesh\SKM_F_Costume_Unique_Event_Costume_Cat001_Cloth_Test_Physics.uasset, 11,746 B, a test file of an event costume). The word "Cloth" in file names there is part of the costume name.
- Measured: physics assets do exist for hair: 39 files ending _Physics under AvatarParts\Groom\Hair (female long, medium, bob and others), plus HairRigidBody.json (42,830 B) mapping each hair mesh to its physics asset; one for a wolf mesh; and Characters\Skeletons\Body_Custum_Physics.uasset (7,861 B).
- Measured, Lua type definitions (luals-defs, names only): game option ClothSimulation (3 choices, default 1; GameOption.json); scalability groups ClothPhysicsQuality 0, 1, Cine (DefaultScalability.ini, entries at lines 1036 to 1043, B1.ClothPhysicsQuality 0, 1, 2); user setting ClothPhysics "0 off, 1 only player, 2 depends on distance, others all" with ClothPhysicsDistance (UB1GameUserSettings.lua); UB1AppearanceComponent holds ClothPhysicsAssetCacheMap (FB1ClothPhysicsAssetCache: original and duplicated physics asset, last applied scale per bone name) and the call RecreateClothingActors is named in a note on ClothCapsuleScaleChangeThreshold, in the customisation data asset; FB1Packet_S_UpdateClothingPhysicsCapsules carries an entity id. Cloth weathering (stat-driven wear) has its own data asset and packet (UB1WeatheringDataAsset.lua, FB1Packet_S_SetClothWeatheringIntensity.lua); this is a material effect by name, not simulation (inferred).
- Garment table tags (GarmentFullMesh.json): "CLO" on 26 rows; "MannequinFemaleCloth" 134, "MannequinMaleCloth" 80 (by their names, outfits for shop mannequins: a reading, not measured); "NoOuter" 519. The plugin CLOConnect (CLO Virtual Fashion, Plugins\CLOConnect\CLOConnect.uplugin) is installed (inferred: garments made or pre-fitted in CLO).
- Not read: whether skirts and dresses use cloth simulation or bone chains in the skeleton; the meshes' cloth data (the tool's cloth-buffer check failed with the mesh).
- Inferred and unverified: since no garment-side physics file was found, any garment motion comes from skeleton bones or from capsules on a per-character cloth physics asset scaled by body shape.

### 7. Signs of morph fitting to bodies

- Measured: every row of Top, Bottom and Full tables has a second skeletal mesh path, DeformedMesh (rows with it set, adult: Top 1,792 of 1,792, 165 distinct paths; Bottom 1,151, 77 distinct; Full 1,152, 71 distinct; Gloves 82, 7 distinct). Jacket, Shoes, Hat, Scarf, Socks and the Inner tables have none. In the Lua note "skeletal mesh used when deformation is enabled" (FB1GarmentFullMeshTableRow.lua, 988 B). The deformed path is the mesh path plus _Jacket for 1,516 of 1,792 Top rows, 989 of 1,151 Bottom and 610 of 1,152 Full; fourteen Top rows point at the mesh itself, and meshes in the Jacket table never end in _Jacket (its review). Inferred, weakly: the _Jacket mesh is a pre-shaped variant used when another layer sits over it.
- Measured flags: bDeformingHead, bDeformingNecklace, bDeformingGloves on Top and Full rows (Top: head 1,636 rows, necklace 658, gloves 830, bDeformingBottom 983; Full: head 431, necklace 68, gloves 435, all youth and adult rows); bDeformingTop, bDeformingBottom, bDeformingGloves on Jacket rows (gloves 1,554). So a garment can shape the head, neck and glove meshes.
- Measured: each row carries layer priority, "drawing regions", "covering regions" and "body regions" lists (for example upper body closed, arms short, belly upper), used to hide body parts under a garment and layer garments (inferred).
- Measured: body shape: AppearanceBodyShape.json (107,854 B, 71 rows) has MuscleDefinition, BodyMassRatio and a list of 17 BodyModifierParameters; FB1ClothCapsuleScaleSetup scales cloth collision capsules between MinScale and MaxScale from a body-shape parameter index. Aging morph curves (AgingOlderMorphCurve, AgingYoungerMorphCurve) are named in the customisation asset. The size of the morph target lists on garment meshes: unread (mesh parse failed).
- Not read: the skin weights, the number of body-shape morph targets, and whether garments carry their own morph targets.

## Unreached, with why

- Corrected by CLOTHES-FILES-2026-11-06-REVIEW.md, 6 November; it did not re-run a package parse, the Custom split, hair physics contents or the Cat001 size.

- Triangle, level-of-detail, bone, material-slot counts of any garment mesh; texture dimensions and formats: package parse failed (no mappings file; three engine settings tried on three files; no further tries).
- Cloth data inside meshes; morph targets inside meshes; physics asset contents: same reason.
- The youngest-body garment folders: left out on purpose.
