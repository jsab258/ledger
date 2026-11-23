# Craft standards from LEDGER's reference-game studies (side by side)

Prepared 23 Nov 2026. Read only; nothing committed. Everything below is copied from the studies, with their own tags, and not re-measured.

## How to read this

- Short names for files, all under /home/claude/wip: **04** = production/research/aaa-reference/studies/04-street-world.md, **05** = 05-visuals.md, **06** = 06-characters-wardrobe.md, **07** = 07-animation.md, **08** = 08-sound.md, **12** = 12-tech-budgets.md, **13** = 13-pipeline.md, **CENSUS** = production/research/aaa-reference/CENSUS.md, **FULL** = ledger-v2/research/full/kcd2-rdr2-teardown-FULL.md, **SUM** = ledger-v2/research/kcd2-rdr2-summary.md, **TRACE** = /home/claude/ledger/production/lane/synthesis/TRACE.md. "l.N" is the line number inside that file.
- Tags are the studies' own: **M** counted from game files, **R** read (a value in a game file or on Warhorse's wiki; the studies do not say which), **I** inferred, **public** developer talk, published article or wiki page. "(helper)" and "unverified" are the studies' own hedges and are kept.
- The last column, **Basis**, is mine, set against the ruling of 17 Nov (RULINGS.md l.54: other games studied from outside only). **FILE** = taken from the game's own files (M, or R from a file): a lead only now, not evidence to build on. **PUBLIC** = from a talk, article, official page or wiki. **FILE?** = tagged R and the study does not say whether file or wiki. **OWN** = LEDGER's own figure or my arithmetic, marked as such.
- Mafia is a study of how Unreal is used, never a design reference. RDR2 appears in none of the craft studies; the only RDR2 numbers in the sources are content-mass counts (see the end of heading 5).
- Checked and empty: the coverage-audit-kcd2 files (SUMMARY.md, DELIVERY.md) hold no craft numbers at all (they map systems, not assets). SUM and FULL hold only AI and content-mass figures. The file studies are therefore the main source. Gaps are named heading by heading.
- Study 4 to 7 were read 25 Oct 2026, before the 17 Nov ruling, from the games' files. Every FILE row therefore sits on the wrong side of that ruling.

## 1. Triangles per kind of asset

| Game | Kind | Number | Source | Tag | Basis |
|---|---|---|---|---|---|
| KCD2 | Hero/standard male body | 17,318 full (five parts); 8,268 and 3,868 at next two levels | 06 l.9 | M | FILE |
| KCD2 | Female body | 16,588 (one mesh) | 06 l.10 | M | FILE |
| KCD2 | Head | median 19,455, unique per head | 06 l.11 | M | FILE |
| KCD2 | Distance whole-character merged mesh | 2,597 to 3,100 | 06 l.12 | M (texturing from names, unverified) | FILE |
| KCD2 | Whole visible man, full detail, head, hair, hands, before hiding | about 71,000 | 06 l.84 | I (study's own sum) | OWN |
| KCD2 | Whole outfit (44-preset sample) | median 24,532 men, 16,548 women | 06 l.80 | M | FILE |
| KCD2 | Hair cards | median 9,700 per haircut (39 haircuts, 9 colours) | 06 l.90 | unverified helper reading | FILE |
| KCD2 | Beards | 1,445 beard meshes, fitted per head (no triangle figure) | 06 l.91 | M | FILE |
| Mafia | Body, head, hair | not exported, no figure | 06 l.20, 151 | gap | none |
| Mafia | Whole outfit | median about 43,000 | 06 l.80 | M | FILE |
| Mafia | Hero-grade tailed jacket | 25,422 on its own 244-bone skeleton | 06 l.42 | M | FILE |
| Epic MetaHuman | Body | 30,500 vertices at full detail (vertices, not triangles) | 06 l.85 | public (Epic specification) | PUBLIC |
| Mafia | Crowd, far | single-mesh puppets (14 male, 7 female) and baked vertex-animated crowds (13 assets); no triangle counts | 06 l.70; 07 l.67 | M | FILE |
| Mafia | Garment: vest-jacket | 19,131, then 8,509, 4,781, 1,505 | 06 l.37 | M | FILE |
| Mafia | Garment: trousers | 7,906 down to 750 | 06 l.41 | M | FILE |
| Mafia | Garment medians at full detail (range) | top or jacket 21,994 (6,112 to 57,369; 87 tops); trousers 9,566 (5,396 to 23,022; 61); shoes 6,718 (1,780 to 9,964; 18); hat 4,495 (1,578 to 14,797; 59) | 06 l.76 to 79 | M | FILE |
| Mafia | Garment, detail levels keep | median 47%, 25%, 9% of full | 06 l.82 | M | FILE |
| KCD2 | Garment: plain tunic | torso 3,734 + arms 2,824 + short skirt 904 = 7,462 | 06 l.44 to 45 | M | FILE |
| KCD2 | Garment: hose | 6,806 | 06 l.47 | M | FILE |
| KCD2 | Garment: caps | median about 5,400 | 06 l.79, 92 | unverified | FILE |
| KCD2 | Cloth proxy for the tunic skirt | 270 triangles | 06 l.46 | M | FILE |
| Mafia | Building (whole) | "can have more than one million triangles", against 20,000 to 30,000 in its earlier games; the census notes this measures detail, not count | CENSUS l.46 (source M6, 2K dev diary 2) | public (official) | PUBLIC |
| Mafia / KCD2 | Prop, building piece, car | no triangle figure for any of the three in any source read | 04, 05, 12 | gap | none |
| LEDGER (context only) | Tom's outfit target, our own pick | jacket 18,000 to 22,000; jumper 15,000 to 20,000; trousers 8,000 to 10,000; shoes about 6,000 | 06 l.113 to 122 | OWN (study says "our choice, not a measured target") | OWN |

## 2. Texture sizes per kind

| Game | Kind | Number | Source | Tag | Basis |
|---|---|---|---|---|---|
| Mafia | All own textures (about 350 each of colour, normal, mask) | 4096 px 21%, 2048 px 36%, 1024 px 38% | 05 l.42 | M | FILE |
| Mafia | In-game cap | not known (the engine's size bias applies to groups these do not use); 110 textures carry bias -1 | 05 l.42 | R | FILE? |
| Mafia | Decals | mostly 1024 | 05 l.42 | M | FILE |
| Mafia | Main master | three textures (colour; packed height, roughness, occlusion; normal) plus a tint; 307 instances | 05 l.38 | R | FILE? |
| Mafia | Vest-jacket | shipped 2048, authored 4096; colour with occlusion, normal, one packed specular-roughness | 06 l.39 | M | FILE |
| Mafia | Trousers | 1024 | 06 l.41 | M | FILE |
| Mafia | Garments in general | most tops and bottoms 1024 (up to 4096 and 2048); shoes and hats 512 | 06 l.83 | M | FILE |
| KCD2 | Textures by archive bytes | building median 2.8 MB (a tenth above 11), people 1.4, furniture 0.7, small props 0.35 | 05 l.43 | M | FILE |
| KCD2 | Body / head | body 2048; heads 1024 colour, 2048 normal, two wrinkle maps | 06 l.13 | unverified (header reads not saved) | FILE |
| KCD2 | Tunic | colour 1024, normal 2048, plus an ID mask that colours each part | 06 l.46 | M | FILE |
| KCD2 | Decal atlas | 256 px, 12 slices; 212 decal materials | 05 l.34 | M | FILE |
| KCD2 | Reflection probes | about 0.10 MB a pair; 23,270 files in Kuttenberg's region, 7,893 in Trosecko; baked at 11 times of day; about 7.2 GB both | 05 l.17 | M | FILE |
| Mafia | Texture pool by quality level (low to top) | 1,200 / 1,500 / 2,000 / 2,000 MB; a 6 GB card sits at level 1 (1,500 MB) | 12 l.11, 82 | R | FILE? |
| Mafia | Other pools at top level | virtual textures 323 MB; Nanite streaming 300 MB | 12 l.31, 38 | R | FILE? |
| KCD2 | Texture pool by card memory | 4,096 MB at 6 GB, 5,120 at 8 GB, 8,192 at 12 GB; PS5 2,240 | 12 l.41 | R (from its comments) | FILE |
| KCD2 | Mesh stream pool | 768 MB | 12 l.42 | R | FILE? |
| KCD2 | Materials | 7,572, one per asset, over 135 shared surface materials (26 ground, 24 wall, 19 wood, 8 stone, 5 metal, 2 glass) | 05 l.39 | M | FILE |
| Mafia | Materials | 253 masters, 1,189 instances in Palermo; 1,213 of 1,416 garment materials share one layered master | 05 l.38; 06 l.63 | M | FILE |
| LEDGER (context) | Own budget | 512 px a metre; 2048 tiling sets; 4096 x 2048 trim sheets (4-BUDGETS.md) | 05 l.62, 72 | OWN | OWN |

## 3. Kit reuse per block or street

| Game | Number | Source | Tag | Basis |
|---|---|---|---|---|
| Mafia | Measured street (Palermo main, 73 m segment): about 2,350 kit placements of about 150 meshes, about 15 uses per mesh; 18 to 19 facade pieces from 2 families | 04 l.29 | M | FILE |
| Mafia | Main-street group (about 100 buildings): 33,986 placements of 433 meshes, 78.5 uses per mesh; 88% kit elements; 32 meshes used once | 04 l.28 | M | FILE |
| Mafia | Facades: 299 pieces of 26 meshes in about 11 house families, each of about 3 stacked floor types | 04 l.28 | M | FILE |
| Mafia | Generator output game-wide: 540 facade, 585 roof, 60 interior, 1,163 distant meshes | 04 l.27 | R, M | FILE |
| Mafia | Windows: about 8,100 window pieces in Palermo; windows, doors, balconies, corbels instanced on top | 04 l.27, 39 | M | FILE |
| Mafia | Plot module 7.8 to 8.3 m; one ground-floor door per 8 m plot (13 doors in 146 m of frontage) | 04 l.14, 16 | M | FILE |
| Mafia | Hero town (San Celeste): about one shape mesh per building (111 for 13 hand-built blocks); 134 packed kit actors | 04 l.31 | M, I | FILE |
| Mafia | Storey step: facade 18 m and 22 m over 4 to 5 storeys (from kit heights). No storey step is stated; 18 over 4 and 22 over 5 gives about 4.4 m a storey (my arithmetic) | 04 l.13 | M (storey step OWN) | FILE / OWN |
| KCD2 | City: 232 placeable building instances from 77 meshes, about 3 uses each; most reused: sheds and lean-tos 11 to 19 times, most reused house 7 | 04 l.33 to 34 | M | FILE |
| KCD2 | Library: 465 building templates; 5,553 structure meshes, 1,873 of them houses | 04 l.35 | M | FILE |
| KCD2 | Houses are whole-building meshes plus placed window and doorway pieces; ridge 18.5 m, two storeys; plot 12.6 to 12.9 m, gable to street; windows about 3.2 m apart upstairs | 04 l.13 to 15, 32 | M, R | FILE |
| KCD2 | Windows kit: about 219 window and 38 shutter mesh names; 290 plane lights in the openings in Kuttenberg's region | 05 l.12 | M | FILE |
| Mafia | Street width 14.7 m (windows 14.5 to 14.9); alleys 3 to 9 m; wide streets 20.5 and 28 m | 04 l.12, 20 | M | FILE |
| KCD2 | Tarmark width: narrowest 5.9 to 6.8 m, median 9.9 m (20 of 49 stations measurable), over 20 m at the square; length about 191 m | 04 l.11 to 12 | M | FILE |
| Mafia | Props per 10 m of street: 4.9 true props (one 73 m sample; neighbours 2.2 and 0); 17.4 with ground dressing; 21 with decals and add-ons; 91 pieces of ground dressing, 8 decals, 18 balconies in 73 m | 04 l.17 to 18, 22, 60 | M | FILE |
| KCD2 | Props per 10 m | not countable (loose meshes stored apart); the 15.8 count was every entity and is withdrawn | 04 l.17, 23 | gap | none |
| Mafia | Fake rooms: 3 shapes placed 24 times in Palermo against about 8,100 window pieces; 60 interior meshes in the whole game | 04 l.39 | M, R | FILE |
| KCD2 | Interiors: of 166 city houses 88 furnished, 78 shells; 619 working doors, 95 shops | 04 l.40 | M | FILE |
| Mafia | Decals: 2,461 on 180 materials in Palermo; 41 cells, median 11 a cell; 232 puddle decals | 05 l.33, 29 | M | FILE |
| Mafia | Own content counts: 10,637 static meshes, 12,632 textures, 11,805 material instances; kit names carry size (803 names such as 90x240cm) | 13 l.47, 20 | M | FILE |
| Mafia | Streaming: Palermo main grid 73 cells at 128 m, plus 33 always-loaded and 7 coarser; props grid 32 m; 130 cells carry 50 data layers | 04 l.46 | M | FILE |
| KCD2 | Streaming: about 96,000 entity records always loaded, about 49,000 streamed; town 34,167 always-on | 04 l.46 | M (helper counted 90,294 and 48,537) | FILE |
| Both | Kit reuse is the shared method; the studies give LEDGER's own street as 43 props and 10 decals on a 48 m road (about 9 per 10 m, from the scene file, not the built level) | 04 l.57 | OWN | OWN |

## 4. Detail distances

| Game | Number | Source | Tag | Basis |
|---|---|---|---|---|
| Mafia | Garment detail levels at screen sizes 1.0, 0.4, 0.15, 0.08 (about half, a quarter, a tenth of the triangles) | 06 l.18 | M | FILE |
| KCD2 | Three mesh levels plus a merged distance mesh; switch distances not read | 06 l.12, 152 | M; gap | FILE |
| Mafia | Civilians freeze when unseen for 3 s and beyond 70 m, never within 10 m | 12 l.50 | R (by setting names) | FILE |
| Mafia | Hair shadows to half its distance, props to a quarter | 12 l.51 | R (by names) | FILE |
| KCD2 | AI detail reduced beyond 150 m; at most 70 to 80 people in full detail | 07 l.68; 12 l.53 | M, R (by names) | FILE |
| KCD2 | 70 in full detail within 150 m; 80 within 180 to 220 m at the top levels | 12 l.53 | R (by names) | FILE |
| KCD2 | View-distance ratio 50 / 100 / 180 (low, default, top); detail ratio 10 / 25 / 300; vegetation ratio 70 / 110 / 250; PS5 performance mode view ratio 80 | 12 l.19 to 24, 26 | R | FILE |
| Mafia | World-partition loading ranges x0.8, 1, 1, 1.5 across levels; distant-detail ranges x0.75 to 1.5 | 12 l.9 | R | FILE |
| Mafia | Distant detail: six layers, nine levels deep; 20,202 distant files in two layers (instanced and merged) | 04 l.46; 12 l.39 | R, M | FILE |
| KCD2 | Distant-detail tree: 8,000 m layer roots; median radii 33 m, 181 m, 45 m, 12 m, 6 m by depth | 12 l.43 | M | FILE |
| Mafia | Nanite visible-cluster cap 1,048,576 to 2,000,000; console 60 fps profile detail bias 1.5 | 12 l.10, 16 | R | FILE |
| Mafia | Light medians: spot reach 8 m, 70 degrees, drawn to 30 m; street lamp spot 20 m, 80 degrees; bulb point 1 m | 05 l.23 to 24 | R, M | FILE |
| KCD2 | Light reach median 4.3 m (a tenth 8 m) | 05 l.26 | R, M | FILE |
| KCD2 | Rain layer drawn to 150 m (40 m at low) | 05 l.30 | R | FILE |
| KCD2 | Local lights' shadow distance cut 20 to 30% inside Kuttenberg ("performance-demanding area") | 12 l.55 | R (by names) | FILE |
| Mafia | Foot IK (5 cm sphere trace, pelvis offset up to 40 cm, feet up to 50 cm) runs at close range only; control-rig feet stop beyond the near level | 07 l.34, 67 | M, R | FILE |
| Mafia | Sound: placed ambience heard to a median 30 m (p25 15, p75 60); footsteps to 30 m; doors 30 m; spawned sounds 20 to 70 m off | 08 l.18, 26 | R, M | FILE |
| KCD2 | Sound: others' steps 15 to 20 m; beds fade over a median 10 m (p75 15) | 08 l.18, 20 | R, M | FILE |
| Mafia | Lumen reflection level 2 needed for front-layer glass reflections (PC default); the 60 fps profile runs level 1 | 12 l.33 | R | FILE |
| LEDGER (context) | Draw distance and people-in-full-detail: "not set" | 12 l.64 to 66 | OWN | OWN |

## 5. Crowd and traffic counts against frame time

Neither game's data gives a cost per person. The studies give budgets for a whole system, and a count beside it.

| Game | Number | Source | Tag | Basis |
|---|---|---|---|---|
| KCD2 | People update budget 3.5 ms (2.5 ms in PS5 performance mode), with at most 70 people in full detail within 150 m | 12 l.53 to 54 | R (by names) | FILE |
| KCD2 | Cost per full-detail person: not stated. Dividing 3.5 ms by 70 gives about 0.05 ms, but the 3.5 ms is for all people's update, so this is only a ceiling-style guess (my arithmetic) | 12 l.53 to 54 | OWN | OWN |
| Mafia | Animation budget 3 ms | 12 l.49 | R (by names) | FILE |
| Mafia | Set-piece crowds: 14 animation-sharing setups, 745 randomised instances (parades, spectators, miners); 13 vertex-animated crowd assets | 07 l.67 | M | FILE |
| Mafia | Palermo main: 191 cells, 7,555 runtime actors; the measured street holds 134 placed actors, its neighbours 6 and 4 | 04 l.5, 20 | M | FILE |
| KCD2 | Ships a performance-test quest in Kuttenberg with 1,000 to 2,500 people | 12 l.56 | R | FILE |
| KCD2 | Shadow-casting lights at most 10 / 16 / 32 (low, default, top), budget 8 per frame, 6 in PS5 performance mode | 12 l.25, 26, 66 | R | FILE |
| KCD2 | Town animals: chickens 51, rats 32, horses 21, dogs 11, cats 8; weather effects 1,883 (rain 1,168, flies 571, smoke 120, leaves 15) | 04 l.52 to 53 | M | FILE |
| KCD2 | Nearly 2,400 NPCs on two maps (2048 x 2048 m and 4096 x 4096 m), about half in Kuttenberg, at a 60 fps target by AI level of detail; Warhorse's GDC 2025 abstract (Smrcek) | FULL l.10, 21; SUM l.12 | public (developer talk abstract) | PUBLIC |
| KCD2 | Sound: ambience timed calls every 22 to 97 s | 08 l.15 | R | FILE |
| Mafia | Sound: spawned voices at once, dawn/morning/day/evening/night: quiet street 0/1/3/2/0; crowded 4/12/18/10/6; market 4/14/25/12/6; water lapping up to 14 within 25 m | 08 l.15, 26 | R | FILE |
| Mafia | Cars: none parked in the measured street; traffic is spawned | 04 l.50 | M, R | FILE |
| KCD2 | Cars: none (horses and carts; parked carts not measured) | 04 l.76 | gap | none |
| Mafia | Frame: console 60 fps profile; PC runs dynamic resolution off | 12 l.14 to 18 | R | FILE |
| Mafia (public test) | 42 to 51 fps, RTX 4090 and 5080, "1440p/Epic Settings"; native or upscaled and build not stated; which card gave which figure not re-checked | 12 l.35 | public (DSOGaming, 8 Aug 2025) | PUBLIC |
| Epic (Lumen) | About 8 ms at the top level for GI and reflections at 1080p internal; the page's context is 30 fps consoles | 12 l.34 | public (Epic page) | PUBLIC |
| LEDGER (context) | Median 16.7 ms, worst 25 (33.3 ceiling); phase 5 load test at 0, 5, 10 and 20 visible people; first street 10 to 25 on screen; front-layer glass cost about 0.06 ms (own measure) | 12 l.62; CENSUS l.110; 05 l.67 | OWN | OWN |

RDR2 in the craft sources: none. The only RDR2 numbers are developer-stated content mass (about 300,000 animations, 500,000 lines, 1,200 actors, 2,200 mocap days; Houser, Vulture, Oct 2018) at FULL l.4, 12 and SUM l.6; they are public and not craft.

## 6. How clothes and faces are built

| Game | Number | Source | Tag | Basis |
|---|---|---|---|---|
| KCD2 | Bodies: one shared body per sex for ordinary people, plus an old man's body and a few named bodies | 06 l.8 | M | FILE |
| Mafia | Bodies: male 32 body meshes in five families (base, hero, brute, fat, one named); female 21; pre-cut variants hide the covered skin | 06 l.15 to 16 | M | FILE |
| Mafia | Garment fitting: each mesh made for one body type; 126 of 176 tagged meshes for the base body; four meshes carry morph targets (purpose not read) | 06 l.28 | M | FILE |
| KCD2 | Layers and slots: 10 body layers (underwear to outer decoration), 22 equipment slots | 06 l.30 | M | FILE |
| KCD2 | Hiding and morphs: 53 named hiding groups, 35 named morphs (about 19 and 10 are for animals) | 06 l.31 to 32 | M | FILE |
| Mafia | Outfit slots: up to 12 (body, head, hair, three groom slots, hat, top, bottom, one-piece, shoes, prop); median preset fills 8; 780 presets; nine skinned pieces follow one invisible leader skeleton | 06 l.24 to 27 | M | FILE |
| KCD2 | Heads: unique, facial rig about 360 bones | 06 l.11 | M | FILE |
| Mafia | Heads: unique (101 male, 20 female), each on a MetaHuman head animation blueprint; shared MetaHuman face folder (29 textures) not exported | 06 l.17 | M, R | FILE |
| Mafia | Male skeleton 272 bones, 28 of them coat-flap bones; tailed jacket skeleton 244 bones | 06 l.19, 42 | M | FILE |
| Mafia | Tails on rigid bodies: 30-body physics asset (22 flap, 8 colliders); second asset 20 bodies, two chains of 11 and 5 bones | 06 l.42 | M | FILE |
| Mafia | Cloth: Chaos cloth on only 10 meshes (8 garments, 9 named characters' pieces), top two detail levels; no crowd garment; rigid-body bones in 68 of 74 garment animation blueprints; 239 of 1,416 garment materials add a shader wobble | 06 l.50 to 52 | M | FILE |
| KCD2 | Cloth: only hems and skirts (173 male, 29 female elements); belts, pouches, straps on 1,926 pendulum joints | 06 l.53 | M | FILE |
| Mafia | Hair: strand grooms (183 male rows on about 24 grooms) plus hair-card meshes; beards and brows strands, bound per head; a hat swaps in a cap-hair mesh (147 of 269 hatted male presets) | 06 l.88 to 89 | M | FILE |
| KCD2 | Hair: alpha-tested cards (39 haircuts, 9 colours; median 9,700 triangles, unverified); caps morph the hair beneath; helmets hide face and beard | 06 l.90 to 92 | unverified | FILE |
| Mafia | Wardrobe: base garments male tops 62, bottoms 39, hats 49, one-pieces 14, shoes 14; female tops 25, bottoms 17, hats 10 | 06 l.57 | M | FILE |
| Mafia | Garment-and-colour rows (male): 1,010 (tops 338, bottoms 255, hats 229, one-pieces 103, shoes 85); median colourways per mesh 4 to 10; jacket 15 colourways, trousers 8; whole looks not counted | 06 l.37, 41, 58 to 59 | M | FILE |
| Mafia | Colour: 1,213 of 1,416 garment materials are children of one layered master; hat left out by chance (empty chance 20 to 80%) in 326 presets | 06 l.60, 69 | M | FILE |
| KCD2 | Wardrobe: 2,139 human garment variants on about 513 meshes, 4 to 6 colourways each; tree of 2,661 materials (hue, saturation, brightness, grime, scratch over an ID mask); hose 25+ colourways; 2,518 clothing presets, median 5 items | 06 l.47, 62 to 64 | M | FILE |
| KCD2 | Crowd dressing: 1,354 soul slots in Kutna Hora but only 139 hand-set appearances using 90 heads; class picks an inventory preset, which picks an outfit at random | 06 l.66 to 67 | M | FILE |
| Mafia | Crowd dressing: presets tagged by sub-class (peasant 72, townsfolk 65, farmer 52, merchant 50, rich 42); spawners drawing from them is inferred | 06 l.68 | M; I | FILE |
| KCD2 | Dirt and blood: on every garment material (blood, grime, scratch); 54 blood-mask spheres (24 human, six body zones) | 06 l.100 to 101 | M | FILE |
| Mafia | Dirt: grime on 880 garment materials, scratch on 801, five blood masks; clean/dirty/damaged as tags | 06 l.97 to 99 | M | FILE |
| Mafia | Faces speak by one pre-baked face clip per line (12,802) | 07 l.63 | M | FILE |
| KCD2 | Faces: one facial file per scene and speaker (18,449 files, 8.2 GB), own layer, no phoneme data | 07 l.64 | M | FILE |
| KCD2 | Wiki: armour pieces 361 (body 129, head 122, leg 73, arm 37) | CENSUS l.32 (K15) | public (Fandom wiki, "one wiki, a rough floor") | PUBLIC |
| Mafia | Official post-launch: Free Ride update 16 outfits, 3 hats; Man of Honor 3 outfits, 5 hats | CENSUS l.48 (M2, M3) | public (official) | PUBLIC |
| Mafia | How made: 2K Valencia names Marvelous Designer, ZBrush and MetaHuman facial rigging | 06 l.105 | public | PUBLIC |
| Mafia | Hangar 13 Unreal Fest 2025 talk, excerpts only: MetaHuman because scanning NPCs was not feasible; more than 100 NPC assets in about three months | 06 l.106 | public, unverified | PUBLIC |
| KCD2 | Warhorse GDC 2025 abstract, search excerpt only: material atlasing, ID maps, UV-space decals, hiding groups, armour layering | 06 l.107 | public, unverified | PUBLIC |
| KCD2 | An executive producer said every male character wears clothes sized to the player (translated interview) | 06 l.33 | public | PUBLIC |
| Mafia | Animation: 54 classes read; 59 state machines, 239 states, 563 transitions; no motion matching; stride warping clamp 0.5 to 1.5 | 07 l.12 to 13, 29 | M | FILE |
| KCD2 | Animation: 842 blend-space files, 94 databases, 22,342 options; stop chosen by remaining distance (walk 0.6 to 2.1 m), travel angle (5 degrees) and stride quarter | 07 l.14, 20 | M, I (stride reading) | FILE |
| Public | Foot slide: play-rate change within about 10% faster or 20% slower (Clavet, For Honor, GDC 2016); viewers noticed slides below 21 mm (Prazak, Hoyet, O'Sullivan 2011, search snippet only) | 07 l.43 to 44 | public (second unverified) | PUBLIC |

## 7. Internal render resolution and upscaling

| Game | Number | Source | Tag | Basis |
|---|---|---|---|---|
| Mafia | TSR for anti-aliasing and upscaling; software Lumen (hardware ray tracing off), virtual shadow maps, Nanite with tessellation | 12 l.29 to 32 | R | FILE |
| Mafia | 60 fps console profile: TSR at 83% with dynamic resolution 40 to 83%, aiming at 60 fps; shadows down two levels, view distance and textures down one, reflections down one, GI unchanged | 12 l.15 to 17 | R | FILE |
| Mafia | PC Windows profile: dynamic resolution off; PC ships at top level with GI and reflections at 2; auto-detect memory thresholds 3, 7, 15 GB | 12 l.8, 18 | R | FILE |
| Mafia | 10% spare on the card in the base console profile (whether the 60 fps profile inherits it is not shown) | 12 l.18 | R | FILE |
| KCD2 | PS5 performance mode: 60 fps, 2560 x 1440 output, FSR at 0.75 (so about 1920 x 1080 inside, my arithmetic), no motion blur | 12 l.26 | R | FILE |
| KCD2 | Screen-space reflections half resolution by default, full at its two top levels | 05 l.17 | R | FILE |
| Both | Study's own reading: both about 1080p internal; at 3440 x 1440 (2.39 times the pixels of 1080p) matching means about 65% per axis (2,236 x 936) | 12 l.68 | OWN | OWN |
| LEDGER (context) | Packaged walk draws at a fixed 55% (r.ScreenPercentage=55), no dynamic resolution | 12 l.68, 102 | OWN | OWN |
| Mafia (public test) | See heading 5 (DSOGaming 42 to 51 fps, native or upscaled not stated) | 12 l.35 | public | PUBLIC |
| Epic (public) | See heading 5 (Lumen about 8 ms at 1080p internal) | 12 l.34 | public | PUBLIC |

## 8. Left-out TRACE lines (section 2 of TRACE.md, 28 Oct)

41 lines have a verdict that begins "Left out"; the line numbers are TRACE.md's own. Two more are left out only in part: aaa-s03-05 (l.62, the waits by kind, a tuning table for the talk helper) and aaa-s03-07 (l.64, the camera's alternation, left to craft). Lines whose verdict reads "Left out" inside the third section (3 Oct trades, 1 Oct D48, 29 Sep) are not study lines and are not counted.

- aaa-s01-07 (l.47): Detail by distance; unseen people freeze beyond 70 m. Verdict: Left out: a performance rule for the first town. §2 asks only that unseen people go on perceiving and remembering.
- aaa-s03-06 (l.63): KCD2's waits as starting values. Verdict: Left out: leads for that same table, not design.
- aaa-s04-01 (l.67): Street width within 9 to 15 m. Verdict: Left out: a street-building check (in hand, n16-4).
- aaa-s04-02 (l.68): Props per 10 m. Verdict: Left out: street dressing.
- aaa-s04-03 (l.69): Dress where the player walks. Verdict: Left out as craft; §15 gives the walked lines (the quay, the yard lane, the landing).
- aaa-s04-04 (l.70): Kit reuse check. Verdict: Left out: craft (in hand, n16-4).
- aaa-s04-06 (l.72): Street views end on a building or a turn. Verdict: Left out: craft (in hand, n16-4).
- aaa-s04-08 (l.74): One switchable layer per street state. Verdict: Left out: waits for more than one street.
- aaa-s05-01 (l.75): Window frames; fake rooms upper and distant. Verdict: Left out: look. §6 needs only the lit-window rule (ER-NIGHT-02).
- aaa-s05-02 (l.76): Shop glass captures and a dirt mask. Verdict: Left out: look.
- aaa-s05-05 (l.79): Wear decal mix. Verdict: Left out: look.
- aaa-s05-06 (l.80): Master materials. Verdict: Left out: look.
- aaa-s05-07 (l.81): Keep the project's own texture budget. Verdict: Left out: craft, done.
- aaa-s06-01 (l.82): Tom's outfit budget. Verdict: Left out: clothing craft.
- aaa-s06-02 (l.83): Four levels of detail per garment. Verdict: Left out: clothing craft.
- aaa-s06-03 (l.84): Colour by material. Verdict: Left out: clothing craft.
- aaa-s06-04 (l.85): One base body per sex for the crowd. Verdict: Left out: clothing craft.
- aaa-s06-05 (l.86): Crowd dressing recipe. Verdict: Left out: craft. DESIGN asks of the crowd only the content rule and an identity for every visible person.
- aaa-s06-06 (l.87): His decision on the Marvelous month. Verdict: Left out: done, his.
- aaa-s07-01 (l.89): Stops and turns chosen KCD2's way. Verdict: Left out: animation craft, done.
- aaa-s07-02 (l.90): Clip play rate near authored speed. Verdict: Left out: animation craft.
- aaa-s07-03 (l.91): 3 cm as a lenient foot-slide bar. Verdict: Left out: animation craft.
- aaa-s07-04 (l.92): Sitting as In, Loop, Out. Verdict: Left out: set aside 6 Nov.
- aaa-s07-07 (l.95): Prepared lines on Epic's mouths, live on loudness. Verdict: Left out: his ruling of 1 Oct stands.
- aaa-s07-08 (l.96): No animation sharing for now. Verdict: Left out, as the study advises.
- aaa-s08-09 (l.105): No Wwise, FMOD, vehicles or extra animals. Verdict: Left out, as the study advises (outside the allowlist). Vehicle sound now follows the car rulings.
- aaa-s08-10 (l.106): The ambience plan's levels and distances. Verdict: Left out: mix numbers for his ear.
- aaa-s10-01 (l.114): Interface width and scale choice. Verdict: Left out: a look decision for his page.
- aaa-s11-09 (l.129): No weather set per checkpoint. Verdict: Left out, as the study advises.
- aaa-s11-10 (l.130): Clock, light, exposure, sky in one preset. Verdict: Left out: look craft.
- aaa-s12-01 (l.132): Significance rules and update budgets. Verdict: Left out: performance, the first town.
- aaa-s12-02 (l.133): A load test far beyond play. Verdict: Left out: performance.
- aaa-s12-03 (l.134): People in full detail, draw distance, shadow lights. Verdict: Left out: performance (in hand, n16-3).
- aaa-s12-04 (l.135): A texture pool figure. Verdict: Left out: performance.
- aaa-s12-05 (l.136): A dynamic resolution range. Verdict: Left out: performance. ER-PERF-01 names the bar only.
- aaa-s12-06 (l.137): Stand-in shop-glass reflection at low quality. Verdict: Left out: look and performance.
- aaa-s13-03 (l.140): Naming rule for Unreal assets. Verdict: Left out: pipeline.
- aaa-s13-04 (l.141): Settings as data. Verdict: Left out: pipeline. §17 lists the switches.
- aaa-s13-05 (l.142): snake_case for new tools. Verdict: Left out: pipeline, done.
- aaa-s13-06 (l.143): No binary twins, GUID names or data tables. Verdict: Left out, as the study advises.
- aaa-s14-15 (l.158): His decision: the source test at 6 clips. Verdict: Left out: a production test. Conflict C13.

## 9. Where the games disagree

- Bodies and cloth: KCD2 builds from one shared body per sex and simulates only hems and skirts (173 male and 29 female cloth elements), so a plain tunic is about 7,500 triangles and a whole man about 25,000 in a median outfit; Mafia cuts 32 male and 21 female body meshes in five families, makes each garment for one body type, uses no cloth on any crowd garment (rigid-body bones instead), and its median outfit is about 43,000 triangles, with a plain jacket alone at about 19,000 (06 l.8 to 16, 50 to 53, 74 to 80).
- People in full detail and frame cost: KCD2 caps full detail at 70 to 80 people inside 150 m with a 3.5 ms update and 8 shadow lights a frame, and has no crowd animation system; Mafia freezes unseen people beyond 70 m (never within 10 m), spends 3 ms on animation, and fills set pieces with shared animation and vertex-animated meshes (07 l.67 to 68; 12 l.49 to 56). Neither source gives a cost per person.
- Kit and street: Mafia reuses about 15 times per mesh on the measured street (78.5 across the district), two facade families, generator-baked; KCD2 about 3 uses per building mesh, with mostly unique numbered houses. The two disagree about width as well (Mafia median 14.7 m, KCD2 9.9 m) and about glass and light (Mafia: Lumen, spot plus bulb per lamp, no captures; KCD2: baked probes at 11 times of day and plane lights set in the openings) (04 l.12, 28 to 34; 05 l.12 to 24, 17).
