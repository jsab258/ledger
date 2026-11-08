# Run-time pictures: where the 353 transient textures come from (8 Nov 2026)

Read 8 Nov from the C++ in ue-probe/Source/LedgerProbe/Private, the specs, tools/ue/stage_game_data.py (the staged list is there, not under tools/) and the dump F:/LedgerTools/tmp/memwhere-2026-11-08/walk.log (353 rows, 1,951.7 MB). Pixel sizes read with PIL from the files (checkout, else F:/LedgerTools/game-inputs). Nothing run, nothing edited.

## 1. Call sites

Every site below ends in ImportTexture (VignetteShot.cpp:6132): LoadFileToArray, ImageWrapper decode to BGRA8, UTexture2D::CreateTransient (6182), one mip, then AddToRoot (6195). So every texture it makes is rooted and never released. No cache exists inside it; each caller decides whether to reuse.

| Site (VignetteShot.cpp unless named) | Function | Picture list | States | Cached? |
|---|---|---|---|---|
| 8446 (loop 8440-8447) | ApplyShopInteriors | production/specs/shop-interiors.json "pictures" + _day/_night_lit/_night_dark.png | all 3 of each (loaded together, 8 shops) | no; each rooted |
| 8037 | shop front builder (door_sign_closed) | shop-interiors.json front.door_sign_closed (one file, door-card-closed.png) | the CLOSED face, per shop | no: one new texture per shop (7) |
| 7472 | street material pass | production/assets/street/quay-street.json "decal" | one picture per row | no |
| 7501 / 7524 | same | quay-street.json "drawn_map" (png) / "surface_map" (jpg, CityPack/textures) | 3 maps (colour, _n, _r) | yes, by file (GStreetTex) |
| 8798 | scan pass | production/specs/ps5-corner.json "scanned" files | 3 maps per entry | no: a file named by two entries is decoded twice (inferred from the code) |
| 8825 | same | ps5-corner.json "ids" | brick map | yes, by file |
| 9069 | SpawnWear | production/specs/street-wear.json "picture" (21 unique) | one each | yes, per call |
| 6406 via LoadSkyPhoto | sky | vignette-pieces.json conditions "hdri" (.png beside the .hdr) | the named one | yes (GSkyPhotoCache) |
| 9363, 9561, 8918 | vignette surface bind, card decals, SpawnStain | CityPack/textures candidates; vignette scene decals; Decals/ours/stain_* | per piece | 9363 per surface; 8918 and 9561 not cached |
| SliceCharacter.cpp:726 | StartGaspMover | production/assets/people/tom/T_Head_LOD1_BC_scalp.png | one | static, rooted |
| LedgerPaper.cpp:70 (FImageUtils) | LoadPicture | production/art/ui/*.png (newsprint, edge, coupon-dash, halftones via TitleScreen.cpp:277, 316) | on use | rooted, cached per path |
| 6255, 9837 | MakeFlatTexture and a control texture | none (2x2, built in code) | n/a | rooted |

Other decoders (LedgerProbe.cpp:325, CrimeProbe.cpp:606, WalkProbe.cpp:486, VignetteShot.cpp:4913) were not read beyond their LoadFileToArray lines; Build.cs says ImageWrapper decodes "the still this probe commits". Unread.

## 2. Size rule found (inferred)

The dump's sizes equal the picture's width and height each rounded up to a multiple of 128, times 4 bytes, in MiB. Examples: 4096x1855 gives 30.00; 5650x460 gives 11.25; 878x878 gives 3.06; 682x1024 gives 3.00; 1024x102 gives 0.50. Raw w*h*4 is shown in section 3 only where it differs. The rule fits every bucket below that matched.

## 3. Groups against buckets (padded MB)

| Group | Files | Pixels | MB each | Dump bucket |
|---|---|---|---|---|
| Shop-room cards, 7 cloud shops x 3 states | 21 | 4096x1855 (raw 28.98) | 30.00 | 30 MB x21: matched |
| Street drawn maps (quay-street) | 6 / 6 / 6 | 2048x2048 / 1024x1024 / 512x512 | 16 / 4 / 1 | part of 16, 4, 1 |
| Street photo maps (CityPack jpg) | 15 / 3 | 2048x2048 / 2048x1024 | 16 / 8 | part of 16, 8 |
| Scan maps incl. duplicates (ps5-corner) | 14 / 9 / 3 / 3 | 2048x2048 / 1536x1536 / 878x878 / 416x416 | 16 / 9 / 3.06 / 1 | 14 of 16; 9 x 9 MB matched; 3.06 x3 matched |
| Street decal cards | 2 / 5 / 1 / 4 / 4 / 1 / 1 / 4 | 5650x460 / 2048x927 / 1024x2048 / 1024x1024 / 1152x512 / 900x450 / 900x260 / 508x762 | 11.25 / 8 / 8 / 4 / 2.25 / 2 / 1.5 / 1.5 | 11.25 x2, 2.25 x4, 1.5 (with wear_rust) matched |
| Mickey's room (3 states) | 3 | 2048x927 | 8 | part of 8 |
| Wear pictures (street-wear.json) | 3 / 2 / 1 / 11 / 3 / 1 | 682x1024 / 1024x512 / 268x1024 / 512x512 / 1024x(170,204,256) / 1024x102 | 3 / 2 / 1.5 / 1 / 1 / 0.5 | 3.00 x3 matched; 0.5 |
| Door card closed, one per shop | 7 | 400x220 | 0.50 | 0.5 x8 = 7 + wear_splash: matched |
| Scalp | 1 | 2048x2048 | 16 | part of 16 |
| Sky | 1 (maybe 2) | 2048x1024 | 8 | part of 8 |

Counts the groups add up to, against the dump:

| Bucket | Dump | Explained | Left |
|---|---|---|---|
| 30 | 21 | 21 | 0 |
| 16 | 60 (39 Resident, 21 None) | 36 (6 + 15 + 14 + 1) | 24 |
| 11.25 | 2 | 2 | 0 |
| 9 | 9 | 9 | 0 |
| 8 | 16 (10 Resident, 6 None) | 13 | 3 |
| 4 | 12 | 10 | 2 |
| 3.06 / 3.0 / 2.25 / 1.5 | 3 / 3 / 4 / 6 | same | 0 |
| 2 | 7 | 3 | 4 |
| 1 | 25 | 23 | 2 |
| 0.5 | 8 | 8 | 0 |

Explained in all: about 1,523 MB of 1,951.7 MB.

## 4. Not matched

- 24 x 16 MB, 3 x 8 MB, 2 x 4 MB, 4 x 2 MB, 2 x 1 MB: about 421 MB. Their owners are not named by any call site read. The 38 ambientCG 2048x2048 PNGs in ledger/Assets/StreamingAssets/Decals and the 45 + 9 CityPack jpgs are candidates (the vignette bind at 9363 and SpawnStain at 8918 read them), but which are loaded in the packaged game was not established. Whether the 21 "None"-flagged 16 MB rows are these was not checked.
- 3 x 0.69 MB (0.6875 padded) and 1 x 0.25 MB: no picture of that padded size found.
- 173 rows of 0.0 MB: no file matches (inferred: the 2x2 flat textures from MakeFlatTexture and similar, 16 bytes each, but the count was not tied to code).
- Not loaded at capture time (inferred from absence): the UI pictures (title halftones, 2144x840, would be 7.4 MB), the sky's second file.

## 5. Could not reach

- The owner names beyond "/Engine/Transient.Texture2D_n": the dump gives no path, so no row is tied to a file.
- Whether the packaged run reached the vignette bind (9363, 9561) and stain (8918) paths: not traced.
- Whether a second sky picture loads (day and night conditions): not traced.
- The four other decoders listed in section 1.
