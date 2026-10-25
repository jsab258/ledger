# Study 6: Characters and wardrobe (25 October 2026)

What a finished, game-ready period garment is, and how a whole crowd is dressed from few pieces, in Mafia: The Old Country and Kingdom Come: Deliverance II. Our own words and numbers only; raw counts on F: (aaa-study/mafia/study-6, aaa-study/kcd2/study-6, public/study-6-sources.md). All read 25 October 2026; revised the same evening after its fresh review (appended).

## Answers

**Bodies and heads.**
- **Kingdom Come II: one shared body per sex for ordinary people,** plus an old man's body and a few named characters' bodies.
  - The male body is five parts, 17,318 triangles at full detail (8,268 and 3,868 at the next two levels).
  - The female body is one mesh of 16,588.
  - Heads are unique, a median of 19,455 triangles with a facial rig of about 360 bones.
  - Three mesh levels of detail, plus a pre-merged whole-character mesh of 2,597 to 3,100 triangles for distance, coloured flat by each garment (its texturing read from names, unverified).
  - Texture sizes (from the helper's header reads, not saved on disk: unverified): body 2048; heads 1024 colour and 2048 normal, with two wrinkle maps.
- **Mafia: shared bodies by body type, cut per outfit.**
  - Male: 32 body meshes in five families (base, hero, brute, fat, one named). Female: 21.
  - Pre-cut variants hide the skin each outfit covers.
  - Heads are unique (101 male, 20 female), every one driven by a MetaHuman head animation blueprint. The name index lists a shared MetaHuman face folder (an archetype face skeleton, a control-board rig, 29 textures); it was not exported, so how far the heads are MetaHuman was not read. 2K's own page names MetaHuman facial rigging.
  - Four levels of detail at screen sizes 1.0, 0.4, 0.15 and 0.08 (about half, a quarter and a tenth of the triangles).
  - The male skeleton has 272 bones, 28 of them coat-flap bones.
  - Its body, head and hair triangle counts were not exported (a gap).

**How an outfit is put together.**
- **Mafia:**
  - An outfit preset fills up to 12 slots: body, head, hair, three groom slots, hat, top, bottom, one-piece, shoes, prop. The median preset fills 8; there are 780 presets.
  - Each slot names a row in a table. A row is a mesh, a material override and tags: body type, social standing, clean/dirty/damaged, social class, age.
  - A blank row means a random pick by tags.
  - In the game, nine skinned pieces follow one invisible leader skeleton.
  - Each garment mesh is made for one body type: 126 of 176 tagged meshes for the base body, a few each for brute, fat and hero. Four meshes carry morph targets whose purpose was not read.
- **Kingdom Come II:**
  - 10 body layers, from underwear to outer decoration, and 22 equipment slots; plate needs padded cloth beneath.
  - Garments are made to the one body per sex. What lies beneath is hidden by 53 named hiding groups and reshaped by 35 named morphs: a cap flattens the hair, a hood extends over the collar.
  - About 19 of the hiding groups and 10 of the morphs are for animals; some morphs fit named bodies.
  - A Warhorse executive producer has said every male character wears clothes sized to the player (via a translated interview).

**One jacket and one pair of trousers.**
- **Mafia's plain vest-jacket:**
  - 19,131 triangles at full detail, then 8,509, 4,781 and 1,505.
  - One material, 15 colourways.
  - Textures shipped at 2048 (authored at 4096): colour with ambient occlusion, normal, and one packed specular and roughness map.
  - It does not simulate.
- **Mafia's trousers:** 7,906 triangles down to 750, 8 colourways, 1024 textures.
- **Mafia, a jacket with tails:** 25,422 triangles on its own 244-bone skeleton. Its tails swing on rigid bodies in a 30-body clothing physics asset (22 flap bodies, 8 body colliders), not on cloth; a second, 20-body asset drives two chains of 11 and 5 bones.
- **Kingdom Come II's plain tunic:**
  - Three pieces: torso 3,734, arms 2,824, a short skirt 904 (7,462 in all).
  - Only the skirt is simulated, through a 270-triangle proxy.
  - Colour 1024, normal 2048, and an ID mask that lets the material colour each part.
- **Kingdom Come II's hose:** 6,806 triangles, with 25 or more colourways from pattern masks.

**What moves.**
- **Mafia** uses Chaos cloth on only 10 meshes (8 garments), 9 of them named characters' pieces: 5 skirts (2 iterations; 2 substeps on 4), ribbons, a vest, a necklace and a cassock, at the top two detail levels. No crowd garment uses cloth.
  - Coat tails, flaps and holsters swing on rigid-body bones (68 of its 74 garment animation blueprints).
  - 239 of 1,416 garment materials add a small shader wobble.
- **Kingdom Come II** simulates only hems and skirts (173 male, 29 female cloth elements). Belts, pouches and straps swing on 1,926 pendulum joints.

**Variety from few meshes.**
- **Mafia:**
  - Base garments: male tops 62, bottoms 39, hats 49, one-pieces 14, shoes 14; female tops 25, bottoms 17, hats 10.
  - These make 1,010 male garment-and-colour rows: tops 338, bottoms 255, hats 229, one-pieces 103, shoes 85. How many whole looks they combine into was not counted.
  - The median colourways per mesh run from 4 to 10.
  - 1,213 of its 1,416 garment materials are children of one layered master.
- **Kingdom Come II:**
  - 2,139 human garment variants on about 513 meshes, 4 to 6 colourways each.
  - Colour comes from a tree of 2,661 materials with hue, saturation, brightness, grime and scratch values over an ID mask.
  - 2,518 clothing presets, a median of 5 items.
- **How crowds are dressed:**
  - Kingdom Come II: a person's social class picks an inventory preset, which picks an outfit at random.
  - Kutná Hora has 1,354 soul slots but only 139 hand-set appearances, using 90 heads.
  - Mafia tags its presets by social sub-class (peasant 72, townsfolk 65, farmer 52, merchant 50, rich 42). That its crowd spawners draw from these is inferred: the spawner files were not exported.
  - Mafia leaves a hat out by chance: an empty chance of 20 to 80% on the hat slot in 326 presets.
  - Far away, Mafia drops to single-mesh puppets (14 male, 7 female) and baked vertex-animated crowds.

**Budgets at full detail, garments only.**

| Piece | Mafia median | Mafia range | Kingdom Come II |
|---|---|---|---|
| Top or jacket | 21,994 (87 tops) | 6,112 to 57,369 | tunic set 7,462 |
| Trousers or hose | 9,566 (61) | 5,396 to 23,022 | 6,806 |
| Shoes | 6,718 (18) | 1,780 to 9,964 | |
| Hat | 4,495 (59) | 1,578 to 14,797 | caps median 5,400 |
| A whole outfit | about 43,000 | | median 24,532 men, 16,548 women (a sample of 44 presets) |

- Mafia's levels of detail keep a median 47%, 25% and 9% of full detail.
- Its textures are 1024 for most tops and bottoms (up to 4096 and 2048) and 512 for shoes and hats.
- A visible Kingdom Come II man adds up to about 71,000 triangles at full detail with head, hair and hands, before what clothes hide is removed (our sum).
- Epic's MetaHuman specification gives the body 30,500 vertices at full detail.

**Hair and hats.**
- **Mafia** uses strand grooms (183 male rows on about 24 grooms) and hair-card meshes; beards and brows are strands, bound per head.
  - A hat swaps the hair for a short cap-hair mesh (147 of 269 male hatted presets).
- **Kingdom Come II** uses alpha-tested hair cards (the helper's reading, not saved on disk, unverified: median 9,700 triangles, 39 haircuts in 9 colours).
  - Its beards are fitted per head: 1,445 beard meshes.
  - Caps morph the hair beneath (caps about 5,400 triangles, unverified); helmets hide face and beard.

**Dirt, blood and wear.**
- Both games keep these as material values, not separate meshes.
- **Mafia:**
  - Grime level on 880 garment materials, scratch on 801, five blood masks.
  - A runtime component for blood, water, dirt, wetness and drying.
  - Clean, dirty and damaged states as tags.
- **Kingdom Come II:**
  - Blood, grime and scratch on every garment material, and 54 blood-mask spheres (24 human, on six body zones).
  - Dirt and blood are gameplay numbers: past 0.9 dirtiness people refuse a greeting, and blood is one term of crime suspicion.

**How they were made (public sources).**
- 2K Valencia names Marvelous Designer, ZBrush and MetaHuman facial rigging for Mafia's characters.
- Hangar 13's Unreal Fest 2025 talk is known only from excerpts (unverified): MetaHuman because scanning its NPCs was not feasible, and more than 100 NPC assets in about three months.
- Warhorse's GDC 2025 talk is known only from a search excerpt of its abstract (unverified): material atlasing, ID maps, UV-space decals, hiding groups, armour layering, blood, grime and damage.

## For LEDGER

**The clothing target for Tom's outfit** (item 3):

| Piece | Full-detail triangles | Textures | Moves |
|---|---|---|---|
| Jacket | 18,000 to 22,000 | 2048: colour and occlusion, normal, packed roughness | skinned; tails or vents on a short rigid-body chain, not cloth |
| Jumper | 15,000 to 20,000 | 2048 | skinned only |
| Trousers | 8,000 to 10,000 | 1024 to 2048 | skinned only |
| Shoes | about 6,000 | 512 to 1024 | rigid |

- The jacket and trousers are anchored on Mafia's medians; the jumper and shoes are our pick within Mafia's ranges.
- These rows sum to 47,000 to 58,000 with the jumper under the jacket; Mafia's median outfit is about 43,000, so the jumper is the piece to trim if the budget is tight. All of this is our choice, not a measured target.
- Four levels of detail at about 50%, 25% and 10%.
- Mafia imports its textures at 4096 and ships 2048. Whether its small folds are baked from a finer model is not shown by the files (an unverified artist's note says so); which folds sit in the mesh and which in the texture, and how lapels and collars are modelled, were not read: open blind spots.
- The ruling of 30 September already matches both games: garments are skinned meshes, and only loose parts move.

**Colour by material, not by mesh.** One layered garment material with tint, grime, scratch and wet values, as both games do. One jumper mesh then gives four to eight period colourways. Its grime value can follow our street's grime.

**Fit to our bodies (our choice).** LEDGER's people are MetaHumans. His ruling of 2 October stopped fitting every garment to six bodies, and Mafia makes most garments for its one base body. So: one base body per sex for the crowd, garments made to it, the skin under each garment cut away or hidden; a second body type only where a cast member needs one.

**The crowd recipe for Quay Street:**
- presets with slots and tag filters (social standing, age, clean or worn), a random pick per slot, colourways from the material;
- a pool of about 10 tops, 8 bottoms, 6 coats, 6 hats and 5 shoes, at 4 to 8 colourways each. This gives hundreds of looks for a street of a few dozen, with Tom and the cast hand-set;
- a hat left out by chance (Mafia: 20 to 80% per preset).
- These are a first figure scaled down from both games, to be tested on the street.

**The facts for the clothes decision (the Marvelous month):**
- Mafia's own character pipeline names Marvelous Designer.
- Both games ship baked, skinned garments, which is the target above.
- Marvelous Designer's vendor guide says its Personal plan "permits commercial use for eligible freelancers and sole proprietors". Its binding terms could not be reached (404 and 403).
- So the licence for game use is still to be read in full before anything made in it goes into the game, as his order says.
- Money: his ruling names 39 USD for one month; the pricing page read today shows 23.3 a month billed yearly for an individual. The monthly price and his eligibility for the Personal plan ("eligible freelancers and sole proprietors") are still to be checked. Both go on his page with the sign-up.

**Dirt as gameplay:** Kingdom Come II's "too dirty to greet" and "blood raises suspicion" are taken up by Studies 11 and 15.

## Coverage map

Ticked: characters, faces and clothes (both games). Dirt as gameplay is left to Studies 11 and 15.

## Open blind spots

- Mafia's body, head and hair triangle counts (not exported).
- How many looks one Mafia crowd spawner produces.
- Kingdom Come II's level-of-detail switch distances.
- How either game's hiding maps to vertices (read from names only).
- Lapel and collar modelling; which folds sit in the mesh and which in the texture.
- Mafia's shared MetaHuman face folder (not exported).
- Marvelous Designer's binding terms and monthly price.

## Sources

- **Mafia's own files:** FModel property exports of Characters (Male and Female Clothing, OutfitPresets, OutfitDataTables, Accessories, GroomsPerHead, CharData, Blueprints, CrowdVAT) and the name index. Raw counts in F:/LedgerTools/aaa-study/mafia/study-6/ (study6_summary.json first).
- **Kingdom Come II's own files:** tables, Storm rules, character definition files and mesh and texture headers read from its archives. Raw counts in F:/LedgerTools/aaa-study/kcd2/study-6/ (study6_key_numbers.json first).
- **Public sources:** F:/LedgerTools/aaa-study/public/study-6-sources.md, with links and read dates: 2K Valencia's character page, the Hangar 13 talk (excerpts), Warhorse's GDC 2025 abstract, Epic's MetaHuman specifications, Marvelous Designer's guide and pricing.

Cost, from the clock: 20:21 to 20:42 for the exports, three helpers in parallel and the synthesis; its fresh review after.

## The fresh review (25 October, Opus; verdict: pass with fixes, all applied above)

- **Confirmed: 34 of 41 claims, all against the raw files.**
  - Both games' body and head counts; Mafia's detail levels, presets, follower pieces and the jacket's and trousers' triangles;
  - the KCD2 tunic and hose; the garment animation blueprints, materials and grime values;
  - the cloth elements and joints; the variety counts; Kutná Hora's souls and appearances; the budget rows.
- **Wrong, fixed:**
  - the jacket tails' physics asset;
  - "no MetaHuman source assets" (a face folder exists, unexported);
  - blood-mask spheres (54, 24 human);
  - the distance mesh's lowest count;
  - the hat-hair count.
- **Unsupported, now marked unverified:** KCD2's hair-card and texture figures; the visible-man total, now our own sum.
- **Misleading, fixed:**
  - "looks" (they are garment-and-colour rows);
  - per-body-type making;
  - the Chaos cloth meshes;
  - KCD2's extra bodies and animal hiding groups;
  - missing hedges (a 44-preset sample, inferred spawners, an excerpt for the GDC talk).
- **For LEDGER, fixed:**
  - the outfit total;
  - the body-fit advice, which clashed with his 2 October ruling: now one base body per sex;
  - the fold-baking claim.
- **Gaps added:** lapels and folds as blind spots; the hat's empty chance in the recipe; the price and eligibility questions for the Marvelous month.
