# Review of CLOTHES-FILES-2026-11-06.md, 6 November 2026

Checked against the packed files (reader's list command, 258,469 files, matches; tables and Lua read; extracts about 70 MB, deleted).

| Claim | Verdict | Why |
|---|---|---|
| Section 1 and 3 file counts (adult 1,604 skeletal, 316 _Jacket, folder counts, 21,968 files) | holds | Reproduced; the 21,968 and 12,337 include the youngest-body folders, which the intro says are left out |
| Row and distinct-mesh counts, all 11 tables, Top and Jacket included | holds | Exact |
| Materials per row | holds | Exact |
| SkinningTarget "Body" in every row | holds | All 11 tables |
| DeformedMesh counts, none on other tables | holds | 1,792/165, 1,151/77, 1,152/71, 82/7 |
| Deforming flags | holds | Counts exact; Top also has bDeformingBottom (983), not listed |
| "The deformed file is the sibling with suffix _Jacket" (under Measured) | fails | Only 1,516 of 1,792 Top, 610 of 1,152 Full, 989 of 1,151 Bottom; 14 Top rows point at the mesh itself. The Jacket table's own meshes never end _Jacket |
| Tags (CLO 26, Mannequin 134/80, NoOuter 519) | holds | Exact; "shop mannequins" is name-reading, unlabelled |
| Lua names and cloth settings (ini lines 1036 to 1043, GameOption, capsule, cache, packets) | holds | RecreateClothingActors sits in the CustomizeDataAsset, not the AppearanceComponent |
| Physics: one costume file, 39 hair, 17 other body-shape facts | holds | Exact (71 rows, 17 values each, bUseMeshMerge true in all 71, not only the default) |
| Section 4 byte rows and folder mesh counts | holds | All 20 byte values exact |
| Section 4 "sample of 21" | fails | The table has 20 rows |
| Pants_L011 MI count 2 | fails | 7 |
| Repair002 MI 0 | fails | 2 (not mentioned as a miss) |
| MI files "2,222 to 2,404 bytes" | fails | 1,377 to 3,207 across the samples |
| Textures: ".ubulk ranges", "21 samples that have textures", "four maps" | partly fails | Ranges exact; only 15 of 20 have textures; Swim003 has three maps, Scarf001 none |
| Merged at run time; colour variants share maps | unsure | Labelled inferred, and fair: one set of maps beside 7 to 15 MIs; nothing in the files proves merging happens |

Not checked: Custom female/male split, parse failures and their error texts (no parse run), hair-physics file contents, Cat001 file size.
