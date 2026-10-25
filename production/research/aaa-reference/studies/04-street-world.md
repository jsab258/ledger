# Study 4: Street and world building (25 October 2026)

What makes a dense, believable street, in numbers, measured from the level files of Mafia: The Old Country (Unreal 5.4) and Kingdom Come: Deliverance II (CryEngine). Our own words and numbers only. Raw counts are on F:/LedgerTools/aaa-study/mafia/study-4/ and F:/LedgerTools/aaa-study/kcd2/study-4/. All read 25 October 2026. Tags: **M** measured from the data, **R** read in a file, **I** inferred; "(helper)" marks a helper's measure the fresh review could not reproduce from the saved files.

**What could be measured.** Mafia's one readable town level is Palermo_Main (191 runtime cells, 7,555 actors). San Celeste, its main town, exported only ground meshes and layer states, so it is covered by names only. Kingdom Come II's town, Kuttenberg, was read from its level's text files; its loose meshes (barrels, crates, signs, carts) are stored apart from those files, so its props could not be counted.

## The two streets measured

| | Mafia: Palermo main street | Kingdom Come II: Tarmark, Kuttenberg |
|---|---|---|
| Length | 73 m segment (M) | about 191 m, curved (M) |
| Width, building to building | 14.7 m (facing windows 14.5 to 14.9; facades 14.9) (M) | narrowest 5.9 to 6.8 m; median 9.9 m (20 of 49 stations measurable; a tenth above 12.7); over 20 m at the square (M) |
| Building height | 18 m and 22 m of facade, 4 to 5 storeys (M, from kit heights) | two-storey townhouses, ridge 18.5 m (M); small houses 8.7 to 11.5 m (helper) |
| Plot width | 7.8 to 8.3 m module (M) | 12.6 to 12.9 m, gable to the street (M); small houses about 7 m (helper) |
| Window spacing | 3.2 m and 2.6 m (helper) | 3.2 m upstairs, three per front (M) |
| Doors | 13 ground-floor doors in 146 m of frontage: one per 8 m plot where houses stand (M) | one or two per house front (M) |
| True props | 4.9 per 10 m of street (M) | not countable (see above) |
| Props plus ground dressing | 17.4 per 10 m; 21 with decals and facade add-ons (M) | not countable |

Across Palermo the facing-window pairs give a median width of 14.7 m, alleys of 3 to 9 m and wide streets of 20.5 and 28 m (M). Mafia's dressing sits where its mission walks: the measured street has 134 placed actors, its two neighbours 6 and 4 (M); Kingdom Come II gave no evidence either way.

**What Mafia's 4.9 props per 10 m are (M):** plant pots 1.2, boxes and buckets 1.0, laundry 0.7, lamps 0.5, signs and post boxes 0.5, seating 0.4, ropes 0.4. Under them in 73 m: 91 pieces of ground dressing (paving, kerbs, moss, debris), 8 decals and 18 facade add-ons (balconies).
**Kingdom Come II's street entities:** a first count of 15.8 per 10 m counted every entity in the corridor (walk points, cameras, triggers, the seats and slots of a few tables); it is not a prop count and is not used.

## Unique buildings against kit

- **Mafia** builds a street from kit. A hand-made shape mesh goes through a Houdini building generator, which bakes facade, roof, interior and distant-detail meshes (game-wide 540 facade, 585 roof, 60 interior and 1,163 distant meshes) (R, M). Windows, doors, balconies and corbels are instanced on top.
  - Palermo's main-street group (about 100 buildings): 33,986 placements of 433 meshes, 78.5 uses per mesh; 88% kit elements; 32 meshes used once (M). Its facades: 299 pieces of 26 meshes in about 11 house families, each built of about 3 stacked floor types (M).
  - **The measured street alone:** about 2,350 kit placements of about 150 meshes (about 15 uses per mesh), and 18 to 19 facade pieces from 2 families (M).
  - Each street group is packed into one actor with a medium-distance twin and distant versions (M).
  - **San Celeste, the hero town,** runs through the same generator and also holds 134 packed kit actors, but its 13 hand-built blocks have about one shape mesh per building (111 in all) (M, I).
- **Kingdom Come II** builds each house as one whole-building mesh plus placed window and doorway pieces, with floors and cellars as nested parts (R).
  - City: 232 placeable building instances from 77 meshes, about 3 uses each (M); its distant tree lists 387 city buildings with 221 names, mostly numbered unique houses (M).
  - Reused most: sheds and lean-tos, 11 to 19 times each; the most-reused house appears 7 times (M).
  - Library: 465 building templates; 5,553 structure meshes, 1,873 of them houses (M).

## Interiors

- **Mafia:** only 60 interior meshes are baked (R). Fake rooms are rare: 3 shapes placed 24 times in Palermo, against about 8,100 window pieces (M). Hero interiors are separate modules (Town Hall 381 assets, Opera 462). Locked and open states are data layers; most street doors are leaves that do not open (R, I).
- **Kingdom Come II:** of 166 city houses, 88 are furnished, 78 are shells (M); 80 have door entities, 71 have beds. The city has 619 working doors and 95 shops (M).

## Edges, landmarks and streaming

- **Edges.** Mafia hides its edge behind a belt of generated foliage, a boundary manager and a slowing material for the horse (R); its distant set pieces (Etna, cliffs, hills) are 74 assets game-wide (20 meshes with 8 distant versions, plus materials and textures) (M). Kingdom Come II rings its town with walls (542 entities), gates and 14 bastions (M); its gates stand 30 to 33 m (helper).
- **Landmarks.** Kingdom Come II's town-hall tower tops out about 42 m above the street (helper); four churches stand in different quarters (M). Visibility from the street was not computed; no Mafia landmarks were measured.
- **Streaming.** Mafia's Palermo main grid has 73 cells at 128 m, plus 33 always-loaded and 7 coarser cells; its props grid is 32 m (M). 130 cells carry 50 data layers (M). Its open world's distant detail has six layers, nine levels deep (R). San Celeste switches its streets by time and story: 21 day states, night variants, a market day, blocked streets and chapter states (R). Kingdom Come II keeps about 96,000 entity records always loaded and streams about 49,000 (M; the helper counted 90,294 and 48,537); the town is 34,167 always-on (M). It switches layers for open and closed, siege, looting and battle (R); 523 merged distant meshes (helper).

## Vehicles, plants and weather

- **Vehicles:** none parked in Mafia's street; traffic is spawned (M, R).
- **Plants:** 9 pots on Mafia's street (M).
- **Weather dressing:** Mafia, none found by name (unverified). Kingdom Come II places 1,883 weather effects in the town: rain 1,168, flies 571, smoke 120, leaves 15; flies by day, fireflies by night, bees and butterflies only when warm and dry (M, R).
- **Animals in the town (Kingdom Come II, M):** chickens 51, rats 32, horses 21, dogs 11, cats 8.

## Targets for LEDGER's phase 2

Quay Street today: a 48 m road with 36 m of frontage, 10.25 m from front to front, two-storey terraces; its scene file places 43 props and 10 decals (about 9 per 10 m of street, read from production/specs/vignette-scene.json, not counted in the built level).

1. **Width:** a check that every street's front-to-front width lies between 9 and 15 m (Kingdom Come II's median 9.9 m to Mafia's 14.7 m); Quay Street's 10.25 m passes.
2. **Props per 10 m of street:** counted in the built level, both sides, per 10 m of street length, from a fixed list of kinds: bins, signs, boxes and crates, pots and planters, seating, lamps and posts, bikes, litter heaps, post boxes and kiosks. At least 5 per 10 m (Mafia's 4.9, from one 73 m sample; its neighbouring streets run 2.2 and 0). Ground dressing (kerbs, paving breaks, moss, stains) is counted apart and has no bar yet.
3. **Dress where the player walks:** Mafia concentrates its dressing on the mission's path. Quay Street is that path; streets beyond it can be thinner. A rule, not a check.
4. **Kit and its reuse:** a check counting, per street, the distinct facade meshes and the placements per kit mesh. Mafia's measured street: 18 to 19 facade pieces from 2 families, kit meshes used about 15 times each. For Quay Street: the terraces share one family with stacked floor types; the shops and Mickey's are the one-offs, as San Celeste's hero blocks are.
5. **Interiors:** enterable only where the story goes (Mickey's office); fake rooms sparingly (Mafia: 24 in about 8,100 windows); shells for the rest. A rule.
6. **Street ends:** every fixed camera's view along the street ends on a building or a turn, never open ground. A check on the camera views.
7. **Weather dressing:** small life tied to weather and hour (flies, smoke, leaves, drips, birds), as Kingdom Come II does; none in Quay Street yet. No number yet.
8. **Layers by time and story:** one switchable layer per street state (day, night, market, blocked), as San Celeste does, once the town grows past one street.

## Coverage map

Ticked: the street and world-building side of world building, streaming (layers and cells), interiors' strategy. Open: San Celeste's own street measures.

## Open blind spots

- San Celeste's actors, props and widths (its map was not exported).
- Kingdom Come II's loose meshes (barrels, crates, carts, signs) and so its props per 10 m.
- Block lengths; sightlines; fog as an edge; Kingdom Come II's cell sizes; clutter by the brief's kinds (bins, bikes, litter) and parked carts.
- Building heights in Mafia come from kit heights, not building bounds.

## Sources

- Mafia: Palermo_Main's exported level actors and packed level actors, the name index of all packages, the world-partition and data-layer assets; F:/LedgerTools/aaa-study/mafia/study-4/.
- Kingdom Come II: Kuttenberg's level text files (level.pak), the building templates, compiled-mesh headers (read only), weatherprofiles.xml; Warhorse's modding wiki article on level data (KM-A-92, read 25 October 2026); F:/LedgerTools/aaa-study/kcd2/study-4/.
- LEDGER: production/specs/vignette-scene.json; SliceCharacter.cpp (frontages at 5.125 m either side).

## Review

A fresh reviewer (25 October, evening) re-measured from the exports and the saved files: pass with fixes. Corrected here: Kingdom Come II's street count (it was every entity, not props), Tarmark's median width, Mafia's grid cells, the most-reused pieces, the distant set pieces, three small counts; Mafia's doors measured; the dressing figures split; families, San Celeste and fake rooms read rightly; Quay Street per 10 m of street; targets 1, 2, 4 and 6 rewritten as checks with fixed counting rules. Measures the review could not reproduce are marked "(helper)".

Cost, from the clock: the Kingdom Come helper earlier on 25 October, the Mafia helper to about 21:40, this synthesis to 21:47, the review to about 21:58, its fixes to 22:02.
