# Asset plan, families A and B: buildings and their parts; interiors

Research note, 3 October 2026, by a separate helper, about thirty-five minutes, read only. About 20 web searches.

**Marks**
- **[READ]**: read at the source, or a project file read here.
- **[SS]**: search summary only.
- **[I]**: my inference.
- **UNREACHED**: the page or host refused me. It is never evidence.

**What I read first, and do not repeat**
- production/research/aaa-street (SUMMARY, notes 1, 2 and 5).
- production/research/shop-window-interiors (NOTE, CLOSE-RANGE, GOODS).
- production/research/interior-blockout, cab-office-interior-1990 and third-person-camera-interiors.
- production/specs/fab-free-megascans.md.
- DECISIONS.md, the last forty lines.
- The recipes: terrace-front.py, shop-room.py and fascia-cornice-elevation.py, plus tools/street_wear.py.
- canon.md, on the town and the content rule.

---

## 0. The answer in brief

1. **No free, allowed, ready-made building or interior fits 1990 Britain at the bar.**
   - Everything British on Fab is either paid, which rule 3 forbids today, or modern London. All of it is UNREACHED, so its NoAI status is unknown.
   - The buildings and rooms stay ours. What is free and allowed is *surfaces* (CC0 from ambientCG and Poly Haven) and *small objects* (Poly Haven's CC0 models).
2. **Stop: the Megascans in his library may all be banned by today's rule.**
   - The GOODS note of today read Fab's own data on this PC. It found that every Megascans record it checked carries `isAiForbidden: true`.
   - Fab defines its NoAI tag as "must not be used for generative AI data collection" [2, READ].
   - The owner's rule bans any asset tagged NoAI outright, even as a reference.
   - Read as written, that removes the two brick walls, the leakage, oil and grunge decals, and the Megascans shop goods (fruit, baking, rope, smoked fish) from every plan.
   - The wear layer today uses only ambientCG and our own pictures (tools/street_wear.py, line 34), so nothing built is affected yet.
   - **This needs his ruling before anyone downloads them.**
3. **The method is the one AAA teams use, scaled to agents:**
   - one *style kit* per building age (parts on a brick grid, three shared trim sheets, our own brick-bond material);
   - assembly by rules with a seed per building;
   - wear by rule;
   - real rooms where the player stands within 3 m;
   - mapped rooms where he does not.

   It extends terrace-front.py; it does not replace it.
4. **A period fault in the street as it stands** [READ, I]. The generator lays every wall in **stretcher bond** (terrace-front.py, line 5672: "laid in stretcher bond"), and the held Poly Haven brick_4 is stretcher bond too.
   - Stretcher bond is the mark of a cavity wall, which became common only in the 1920s [19, READ].
   - A Victorian solid wall shows headers, as Flemish or English garden-wall bond [I; check by eye against R06 and Geograph].
   - At 10 m in the game's frame a header is about 19 pixels wide, so a British eye will see it. The fix belongs to the proof view's item 4 (brick).
5. **The two proofs.**
   - **Buildings:** do item 2's items 4 and 5 (the brick, and the facades' variety and trims) *as a kit*. That means the three near parade frontages and the three west_south houses opposite, from one kit with seeds. About 6 to 9 builder-days, almost all of it work item 2 needs anyway.
   - **Interiors:** one domestic room kit, shown as real rooms behind the terrace's ground-floor windows and as the mapped rooms behind the parade's upper windows. About 5 to 7 builder-days.

---

# Family A: buildings and their parts

## A1. How professional games make buildings

| Game | Method | Mark |
|---|---|---|
| **Watch Dogs: Legion** (London, 2020) | Modular kits assembled by level artists. Two industrial kits of 250+ modules made "many different variations of industrial style buildings throughout London" [5]. Pub facades and pub counters are modular kits too [7]. Interior kits (walls, windows, doorways) "allow for material swaps so you can interchange between plaster/wallpaper/wood" [6]. | [SS]; ArtStation UNREACHED |
| **KCD2** (Kuttenberg, 2025) | Kits built so level artists make "as many different structures as possible with fewer elements" [10]. Materials made in Substance Designer and Painter. The window counters are real models fitted to each house (CLOSE-RANGE note). | [SS] |
| **GTA V** (Los Santos, 2013) | Hand-built, not procedural. Buildings "were not copied around the map". The art director "compresses, edits and emphasises" a city so it feels like its popular image [11, 12]. It takes hundreds of artists, so it is not our route [I]. | [SS] |
| **Mafia: Definitive Edition** (1930s Lost Heaven, 2020) | Asset lists, references, greyboxes, then hero buildings (theatre, police station, hospital) modelled one by one [13, 14]. No public source on kits or trims. | [SS] |
| **Spider-Man; The Matrix Awakens / City Sample** | Rules over kits: Houdini for Manhattan; a shape grammar per style for City Sample, with a separate ground-floor style (aaa-street note 1). | [SS], already in the project |
| **Everybody's Gone to the Rapture** (1984 Shropshire, 2015) | In-house environment artists made the props, buildings, vehicles and tileable textures. The posters and the labels on food cans were made to the period [33]. The nearest precedent for a British 1980s place. | [SS] |
| **Unreal 5.8 PCG shape grammar** | Splines cut into segments. Modules are "user-defined symbols that represent assets". The grammar has `A*`, `A+`, `[A,B]2`, weighted `{[A,P]:2,[B,P]:1}` and the fallback `<A,B,C>`. "Tight corners might be underestimated and produce incorrect results". The Primitive Cross-Section node is "currently Experimental" [1]. | [READ] |

**What this means for a 1990 port town [I]**
- Every studio but Rockstar builds a town from **a kit per style, plus rules, plus hand polish on a few hero buildings**.
- Fictional towns read as their era through **types, not copies**. Each kind of building is made from several real ones of its class, as GTA does with its cars.
- For us, a hero building is Mickey's, the Tivoli, the police station or the chapel. It is still assembled from the kit, then given one or two pieces of its own.
- **Names and lettering are where brands slip in:** chain stores, breweries, cinema chains. Every name is fictional (canon). The Tivoli is minted; Odeon's name and lettering are not ours to use.

## A2. Free sources without AI restrictions

| Source | What fits | Licence, and any AI clause | Mark |
|---|---|---|---|
| **ambientCG** | 2,010 materials by id, committed 1 October: Bricks 115, PaintedBricks 5, RoofingTiles 27, Plaster 7, PaintedPlaster 18, Concrete 61, CorrugatedSteel 15, Facade 26, WoodSiding 13, Planks 59, Tiles 164, Terrazzo 21, Sign 26, plus decals outside that list. **The look of each is unverified.** Bricks and paving lean continental. Facade is photographed fronts, probably continental: test them for the hillside at distance only. Sign may hold real brands: check each. | CC0 1.0. No AI clause. Already in THIRD-PARTY.md | [READ] the catalogue (tools/citypack/catalogue.json); site UNREACHED |
| **Poly Haven** | Textures: brick_4 (stretcher bond, so right for 1930s and later only), brick_wall_001, painted_concrete_02, plaster. Models for building dressing: very few. | CC0. No AI clause | [READ] THIRD-PARTY.md; API UNREACHED |
| **Sketchfab, CC0 filter** | Nothing British and architectural was found. | CC0, but **a CC0 model may still carry a NoAI tag**: Sketchfab added NoAI tagging and moved free NoAI models to its Standard licence [4]. Check every item's tag; by our rule a tagged one is out even if it is CC0. | [SS]; API UNREACHED |
| **Fab, free** | Not found for 1990 British buildings. | Standard licence; NoAI possible on any listing | UNREACHED |
| **Fab, paid**: British City Pack, Victorian Street, Modular British Buildings (Facades), Stylized UK Modular House [32] | Modern London, 19th-century London or stylised. | Paid, which rule 3 forbids today. NoAI unknown | [SS]; UNREACHED |
| **Megascans in his library**: Brick Wall, Brick Wall Worn, Leakage ×4, Concrete Leakage ×2, Oil Stain ×2, Grunge ×2, Stains | Would serve the brick and the wear. | Fab Standard, **records flagged `isAiForbidden: true`** (GOODS note, read on this PC today) | Out by today's rule; needs his ruling |
| **Building Tools** (Blender add-on, ranjian0) | A blocky generator for floor plans, windows and roofs. Not needed: our recipe already goes further. | **MIT** (raw LICENSE read); v1.0.13, "Blender 4.0 Compatible", untested on 4.5 [16] | [READ] |
| **Buildify** (Blender geometry nodes) | A stylised kit library. Not needed. | GPL [17]. Run only as a tool, like Blender itself, its output is ours [I]. Nothing GPL ships | [SS] |
| **City Sample Buildings** | American high-rises | UE-only, outside the allowlist's animation-only entry | Already ruled out |

**In one line:** surfaces from ambientCG and Poly Haven; nothing ready-made at building scale.

## A3. The kit method: what we make

**What exists already** [READ]
- **terrace-front.py** (8,038 lines) builds one style, the 1880s parade with its plain and parapet variants, from vignette-scene.json:
  - panels around openings, with no booleans;
  - segmental arches, a dentil course, sashes, slate roofs, stacks, aerials, end walls;
  - a Blender wear layer.
- **Variation is thin:** per-bay door sides, one empty unit, one dish, fixed repair patches.
- **tools/street_wear.py** adds a seed per house (brick set 0 to 2, a tint, a wear level) and lays decals by rule.
- **fascia-cornice-elevation.py** already checks mouldings by shape under raking light.

**The step from here** is to turn the one style into **a style table plus modules plus rules**:
1. Each style is a JSON style sheet. It holds the dimension ranges taken from photographs, the module list, the rules (grammar), the palettes and the alterations.
2. A generator reads any style sheet. This is terrace-front.py, generalised.
3. It emits two things:
   - (a) **module meshes, once per style**;
   - (b) **a placement list per building**: which module, where, and which seed values.
4. Unreal places the modules as instances.

**The parts.** A full style kit has 25 to 40 pieces (aaa-street note 1). Shared pieces are marked S.

| Group | Pieces |
|---|---|
| Wall | bay panel, pier, party-wall pier (S), plinth course in blue engineering brick (S), string course, dentil course (have), eaves (have), parapet and coping (have), quoins (stone styles) |
| Openings | sash 2/2 and 1/1 with horns (have), single-storey canted bay, replacement aluminium window (1970s-80s), 1930s steel-framed window, 1930s and 1950s timber casement, 1960s ribbon window; heads: segmental arch (have), flat gauged arch, stone lintel, concrete lintel; sills: stone with drip, brick-on-edge, tile |
| Doors (S) | 4-panel, 6-panel with fanlight, 1930s sunrise glazing, 1960s flush with a glazed slit, 1980s "Georgian" replacement, plywood boarding |
| Roofs | slate pitched (have), concrete interlocking tiles (re-roofed), clay pantiles (outbuildings, a Humber cue [I]), hipped (1930s), felt flat roof (1960s), parapet (have), roof lights |
| Chimneys (S) | stack (have), pots (have roll-top and weathertop; add 3 to 4), cowls, capped or lowered stacks |
| Rainwater (S) | cast-iron ogee and half-round gutters, grey or black plastic gutters (1970s on), downpipes with shoes and hopper heads, rear soil stack |
| Shopfront | pilasters, consoles, fascia, cornice (have, fascia-01), stallriser, recessed door, transom (have), metal refit (have), blind box, roller-shutter box |
| Rear and alley | outrigger or back extension, yard wall and coping, ledged yard gate, outside WC used as a store, coal hole, alley surface (setts or concrete), washing line, galvanised dustbin. Never a wheeled bin |
| Railings | cast iron (chapels, school, offices); cut stubs in dwarf walls, where railings were taken for scrap in the 1940s [I] |
| 1990 additions | TV aerial (have), a rare dish (have; never the shape of a real product), burglar-alarm box (fictional mark), meter box, letting and for-sale boards (have), name plate (have) |
| Industrial | stacked loading doors, hoist beam, cast-iron columns, louvred roof ventilator (smokehouse), corrugated cement sheeting, steel portal frame, roller door |
| 1930s and 1960s | render bands, a curved corner, faience panels, a fin or tower and a canopy (cinema); precast panels, exposed-aggregate concrete, concrete balconies, deck access, stair towers |

**Trim sheets: three, shared across every style** (Insomniac's method, aaa-street note 1)
1. **Painted timber and joinery:** glazing bars, sash stiles, door panels and mouldings, fascias, architraves, bargeboards.
2. **Stone, stucco and concrete:** sills with drip, lintels, copings, string courses, cornices, keystones.
3. **Metal:** gutters, downpipes, railings, shutter slats, the edges of sheeting.

How each sheet is made (all by script) [I]:
- Each is 4096 by 2048.
- Its bevels are baked in Blender's Cycles from high-poly profile strips, which are the same profiles the fascia recipe already draws.
- Each comes with its tiling partner (brick, render, slate, concrete).
- This answers aaa-street's finding that "we have only the tiling half".

**The brick: our bond, CC0 surface** [I]
- The generator writes a **brick-ID mask** for each bond at the British size (215 × 65 mm, with 10 mm joints [20, READ]):
  - Flemish bond and English garden-wall bond (three or five stretchers to a header course) for the Victorian styles;
  - stretcher bond for 1930s and later;
  - engineering brick for plinths and dock walls.
- The mask's random channel gives each brick its own tone, and the per-building tint sits on top. The recipe already has BRICK_TONES; this moves it into Unreal's material.
- Only the brick face's fine detail and its roughness come from a CC0 scan. That avoids ambientCG's continental bonds altogether.
- Relief from Nanite displacement goes only on the nearest walls (aaa-street).

**Variation: one seed per building chooses, within the style sheet's ranges**
- Brick set and tint; mortar tone.
- Door type, and its colour from a period paint palette. BS 4800 was Britain's standard paint range for building in that era; it is a standard, not a brand [I].
- Window type per floor (original, replacement or boarded), in proportions set per district.
- Roof covering; pots per flue; capped stacks; aerial or dish.
- Alterations: a rendered or pebbledashed front, painted brick, a little stone cladding, a bricked-up window, a 1960s shopfront in a Victorian bay.
- Wear: age, which way the wall faces (north-facing soot, as west_south already has), algae under leaks.
- Empty or lived-in, read from the town's simulation, as the empty unit is today.

Rules the generator can test:
- No two neighbours share a signature (door, windows, pots, tint).
- Each style holds its proportions.

**The tools**

| Step | Tool | Who |
|---|---|---|
| Style sheet from photographs | JSON, by hand from dated photographs | agent drafts; **eye judges proportions once per style** |
| Modules, trims and bond masks | Blender 4.5 by Python, as terrace-front.py does; Cycles bake | agent |
| Assembly | the Python grammar, testable by selftest; later, if it pays, Unreal 5.8 PCG shape grammar with Epic's LLM skill for the hillside and the districts | agent |
| In Unreal | Nanite static meshes; instanced by a placement list (ISM/HISM or one Packed Level Actor per building, not verified in 5.8 [I]); per-instance custom data feeding one master material for the tint and wear seeds (GOODS note); projected decals from street_wear.py's rules, extended per style; HLOD for the far town | agent |
| Judging | the elevation sheet per style; the hook camera's frame beside the Hook sheet and the KCD2 frames; numeric checks (repeats by autocorrelation; value and warmth against the sheet, as the recipe already measures) | **builder's eye, then a fresh reviewer, then whole frames to Jafar** |

**Of two fine ways, the cheaper** [I]
- Keep the grammar in Python, where it is already deterministic and tested.
- Let Unreal only *place* what it is told to place.
- PCG shape grammar becomes worth trying when a whole district must be filled, not before. aaa-street says the same.

## A4. The reference that sets the bar

These are links only, for proportions and period feel, never designs (production/reference/photographs.md).

| Building | Reference | Mark |
|---|---|---|
| Victorian terraces and shops | Peter Marshall, Hull (R05, R06, R09), already held; Alec Gill's Hessle Road archive, Hull fishing community, 1970s-80s [31] | held; [SS] |
| A port town's main shopping street, 1970s-90s | Grimsby Telegraph, "Freeman Street from the 1970s to the 1990s" [30] | [SS] |
| Postwar council | Marshall, Newtown Square (R07), held | held |
| Dock buildings | Grimsby Ice Factory, built 1898-1901, 4,350 m², closed in **1990** with its machinery inside [21]. A type for Meridian, never a copy | [READ] |
| 1960s concrete in a port | Portsmouth's Tricorn Centre, 1966: rusting steel bursting the concrete, "small stalactites" off ledges, voted third ugliest building in the UK in 1988 [22]. The wear rules for concrete come from this | [READ] |
| Terrace types and their 1970s improvement | Wikipedia [18]; cavity walls common from the 1920s [19] | [READ] |
| Cinemas, chapels, police and fire stations, schools | Historic England's Listing Selection Guides (Culture and Entertainment; Law and Government; Places of Worship) and its Nonconformist Places of Worship introduction [24] | UNREACHED; [SS] |
| Surviving buildings | Geograph, CC BY-SA 2.0. Mostly photographed after 2005, so check every frame for later changes [I] | not opened |

Canon notes for the variety:
- **The Tivoli.** By 1990 many 1930s cinemas had become bingo halls. Rank ran bingo in its cinemas from the 1960s [23, READ, partly; I]. Bingo is gambling, so the Tivoli is either still a cinema or closed. Never bingo, and no bingo lettering anywhere.
- **Pubs** follow production/specs/the-pub-without-drink.md: no brewery names and no drink lettering.
- **The closed school:** no lettering that names children [I, to keep well clear of the rule].

## A5. The variety the town needs, and the one proof

**The styles in three tiers.** Each is a style sheet with 15 to 40 modules; about 60 parts are shared.

| Tier | Styles | Why |
|---|---|---|
| **1. Quay Street and the hook view** (the friends' build) | (1) Victorian shop parade (exists); (2) Victorian by-law terrace (west_south, and reused small on the hillside); (3) dock warehouse; (4) quay shed; plus the rear elevations seen through the yard gap | what the frame and the thirty-minute walk see |
| **2. The rest of the Hook** | (5) Victorian corner pub; (6) nonconformist chapel, closed or turned into a store; (7) Harbour Board offices in stone; (8) smokehouse, and the ice factory as a type; (9) lock-up garages | a port's old quarter: work, chapel and the pub as a place |
| **3. The town** (seven districts) | (10) the 1930s Tivoli; (11) the closed board school; (12) 1930s council semis and short terraces; (13) postwar council flats and houses; (14) a 1960s concrete precinct with flats over it, a multi-storey car park and the police station; (15) Edwardian Exchange offices and a bank; (16) Gullwing's stuccoed resort terraces; (17) Ironside's sheds | a 1990 town shows four building ages side by side on one walk |

In numbers [I]:
- About 15 to 17 styles; about 350 to 500 modules in all.
- Six brick sets: red stock, sooted grey, buff, blue engineering, painted, rendered or pebbledashed.
- Three trim sheets.
- With seeds, every street has two or three ages in it and no two neighbours alike.
- Tier 1 needs only 4 styles.

**The one proof: Quay Street's six facing frontages, from one kit**
- **What it is.** Rebuild the three near parade frontages (Mickey's and the next two) and the three west_south houses opposite as **two styles of one kit**:
  - modules exported once;
  - the three trim sheets;
  - the bond material (Flemish or English garden-wall bond for these Victorian walls);
  - a seed per house;
  - the wear decals by rule;
  - in Unreal, by placement list.

  This is item 2's items 4 and 5 done as a kit, so it adds little to work already on the list.
- **How it is judged.**
  - The hook camera at 2560 by 1440, by day, beside the Hook sheet, and beside the KCD2 arcades frame for edge light, depth and wear.
  - Fails if any of these is true: a visible repeat at the near corner; two neighbours alike at a glance; flat edges; stretcher bond on a Victorian wall; anything out of period (wheeled bin, uPVC everywhere, a modern door); wear too faint to read across the frame (his note of 2 October).
  - Then a fresh reviewer told to find the copy-paste, then the whole frame to Jafar with its shortfalls named first.
  - **The test of the method:** the same kit, with new seeds and at lower detail, also builds one hillside row in haze (item 9) with no new pieces.
- **Effort** [I, estimate]: 6 to 9 builder-days.
  - module export and generator refactor 2;
  - trim sheets 1.5;
  - bond material 1.5;
  - seeds and alterations 1;
  - Unreal placement and the master material 1;
  - the judging loop 1 to 2.

---

# Family B: interiors

## B1. How professional games make interiors

**By distance, as the 3 October notes found** (CLOSE-RANGE, not repeated)
- **Far, fast or high:** interior mapping. SimCity, Forza Horizon 4 (British towns, with atlases that include shops and pubs, night textures and a Fresnel fade), Spider-Man, Euro Truck Simulator.
- **On foot within 3 m:** real geometry, as in KCD2's window counters and Spider-Man 2's 32 real rooms.

**Rooms the player walks into, at scale**
- **Watch Dogs: Legion.** Modular interior kits for walls, windows and doorways, with material swaps between plaster, wallpaper and wood [6]. "Dozens" of fully realised interiors in all [9]. [SS]
- **Skyrim.** Seven kits made 400+ interiors (aaa-street note 1). [SS]
- **GTA V.** Shops of one chain appear to share one interior: modders remake "all 9" 24/7 stores as one [15]. [SS, weak]. So a template per trade, dressed differently, is accepted practice [I].
- **Every studio blocks out first, then dresses** (interior-blockout). Third-person rooms run larger than life and doors wider (third-person-camera-interiors).
- **KCD2's rooms** read through dense hand-placed clutter and practical light (judged from its frames, not a source) [I].

## B2. Free sources without AI restrictions

| Source | What fits | Licence, and any AI clause | Mark |
|---|---|---|---|
| **Poly Haven models** | Already held for the shop rooms: WoodenChair_01, painted_wooden_chair_01, round_wooden_table_01, vintage_cabinet_01, wooden_bookshelf_worn, drawer_cabinet, Television_01 and _02, wall_clock, mantel_clock_01, CashRegister_01, steel_frame_shelves_01, wooden_display_shelves_01, tea_set_01, potted plants, picture frames, metal_toolbox, and more (tools/art-recipes/fetch_polyhaven.py). **Sofas, beds and kitchen fittings in the 1990 British style were not checked.** | CC0. No AI clause | [READ] the project's list; site UNREACHED |
| **ambientCG** | Carpet 16, Wallpaper 6, WoodFloor 74, Tiles 164 (quarry and wall tiles), OfficeCeiling 6 (suspended grid), Terrazzo 21, Fabric 87, Leather 50, Chipboard 8, PaintedPlaster 18, PaintedWood 17. **The look of each is unverified;** carpets and wallpapers are probably modern | CC0 | [READ] catalogue; site UNREACHED |
| **Sketchfab CC0** (for example ffishAsia's scans, for shop goods) | goods, not rooms | CC0; **check each for a NoAI tag** [4] | [SS] |
| **Megascans goods** in the shop plans (fruit, baking, rope, smoked fish) | the grocer, the tea room, the chandler | flagged `isAiForbidden` | out by today's rule; needs his ruling |
| **Fab interior kits, wParallax, the paid interior shaders** | — | paid, or licences outside the allowlist (NOTE.md) | out |

**In one line:** CC0 small objects and surfaces. Rooms, furniture in the 1990 British style, wallpapers and carpets are ours to make.

## B3. The kit method: what we make

**What exists already** [READ]
- **shop-room.py** builds a shop room from production/specs/shop-interiors.json, renders its three lighting states, and exports real rooms (`--export-room`: 12 cm walls, as Lumen wants).
- **Rita's window** passed; the other eleven are being made like it.
- **mickeys-blockout.py** renders Mickey's authored layout.
- The street's upper windows show held interior pictures with net curtains on every third window (terrace-front.py, INTERIOR_PICTURE, NET_LIT_EVERY).

**The step from here: one room kit, used three ways**
1. **Walked into:** Mickey's now; homes and the police station later.
2. **Real rooms behind ground-floor glass**, seen at 1 to 3 m.
3. **Rendered into a mapped atlas** for upper and far windows.

The same pieces serve all three, so a household looks the same whether it is seen from the pavement or entered [I].

**The parts**

| Group | Pieces |
|---|---|
| Shell | made from the building's own plan, on the same bay grid; wall, floor and ceiling as separate meshes at least 10 cm thick (Lumen); window and door openings taken from the exterior's data, so inside and outside line up; stairs (straight and widened where walked; a steep terrace stair left unwalked) |
| Trims (a fourth trim sheet) | skirting, dado rail, picture rail, architrave, coving; doors and frames (widened to about 1.1 m only where walked); fireplace surrounds (Victorian cast iron, 1950s tiled, 1970s-80s stone-faced) |
| Finishes, as material instances | walls: woodchip painted magnolia, our own wallpapers (stripes, small florals, borders), embossed paper, gloss below and emulsion above in institutions, glazed tiles. Ceilings: swirled plaster, polystyrene tiles, suspended grid. Floors: patterned carpet, cushion lino, quarry tiles, carpet tiles, terrazzo, bare boards |
| Fittings | wall gas fire, night-storage heater, radiator, pendant lamp with shade, fluorescent batten, square 1990 British switches and sockets, meters, a fictional phone, a TV and video recorder |
| Furniture sets | **domestic:** three-piece suite, sideboard or wall unit, coffee and dining tables, bed, wardrobe, chest of drawers, kitchen units, cooker, fridge. **office:** desk, swivel chair, filing cabinet, letter trays, typewriter (Anna Fox, 1987, already held). **institutional:** stacking chairs, a counter with a glazed screen, a notice board, benches. **shop:** counter, shelving runs (exists) |
| Clutter | papers with real thickness (GOODS), mugs, ashtrays (tobacco is allowed), fictional papers and magazines (the brand bible still owes the local paper), ornaments, framed pictures (as in the shop displays) |
| Window dressing | nets, curtains, venetian and roller blinds, as real meshes |

**Variation: one seed per room chooses a household or office profile**
- Age, means, tidiness, smoker or not.
- From that profile: the finishes, the furniture set and the clutter density.
- Then the wear:
  - nicotine-yellowed ceilings in a smoker's room, a period cue that the content rule allows;
  - damp in the corners, which a port town has;
  - sun-faded curtains, worn carpet paths, scuffed doors.
- A household profile never shows alcohol or children: no toys, no school photographs.

**The tools**
- **Blender:** shells from plans, furniture from dimensions, Poly Haven pieces, Cycles for the atlas renders.
- **Unreal:**
  - real rooms under Lumen's rules (CLOSE-RANGE);
  - room prefabs placed per building (Packed Level Actors or Level Instances, not verified in 5.8 [I]);
  - clutter scattered on surfaces by PCG, or simply by the Python placer [I];
  - the interior-mapping material for far windows (NOTE.md's plan; furniture kept against the walls, the Fresnel fade on).

**Where the eye is needed**
- **The agent does:** the shells, the rule-based furniture placement (against walls, clear of the camera's path) and the renders.
- **The eye judges:**
  - each room set's period truth and taste: wallpapers, carpets, the overall palette;
  - the walk-in layout, by blockout and a walk first;
  - whole frames.

## B4. The reference that sets the bar

These are links only; nothing is copied.

| Room | Reference | Mark |
|---|---|---|
| A council flat, about 1990 | Richard Billingham, *Ray's a Laugh*, taken 1990 to 1996 in a Cradley Heath council tower block [27]. For surfaces and furniture only; it shows drink, which we never show | [SS] |
| Public waiting rooms and counters | Paul Graham, *Beyond Caring*, DHSS and unemployment offices, 1984-85 [25, 26]: the police station's front office and the institutional set | [SS] |
| Homes and shops in the consumer boom | Paul Reas, *I Can Help*, 1985-88 [28] | [SS] |
| Front rooms | Museum of the Home: a 1976 front room and a 1990s loft conversion, both London [29]. The loft is a better-off home than the Hook's | [SS] |
| Offices | Anna Fox, *Work Stations*, 1987 (already in the cab-office note) | held |
| The police station | **No photograph of a 1990 provincial station has been found** (british-policing-1988-1992 says so too). Next best: TV of the window, *The Bill* (1990) and *Prime Suspect* (1991), as sets, plus PACE 1984's custody layout (police-response-1990). Never *Life on Mars*, which is 1973 and the wrong decade | [I] |

## B5. The variety the town needs, and the one proof

| Kind | How many | Why |
|---|---|---|
| Shop rooms seen through glass | 12 on Quay Street (the spec); later about 15 trades × 2 | one per shop; a trade template dressed per shop, the GTA way |
| Mapped rooms for upper and far windows | about 20 renders: 8 room types (front room, back kitchen, front bedroom, landing, office over a shop, stockroom, stripped and empty, a frosted bathroom) × 2 to 3 seeds, lit and unlit, with nets, curtains, blinds or boards chosen by hash | Spider-Man 2 needed 32 rooms for a city; a street needs fewer, but no two neighbours alike |
| Walk-in spaces | now: Mickey's (front office, radio room, back room). Later: a terraced home of two rooms, the police station (front office, interview room, custody desk and a cell), the tea room, the pub-without-drink; about 6 to 10 in all | what the story uses; each assembled from the kit's domestic, office, institutional or shop set |

**The one proof: one domestic room kit, three households, two distances**
- **What it is.** The kit's first room type, the 1990 front room of a terrace or flat:
  - its shell from west_south's plan;
  - one trim sheet;
  - six finishes;
  - about 15 furniture pieces, made from dimensions or taken from Poly Haven;
  - nets and curtains.

  It is built for three seeded households and shown two ways:
  - (a) as **real rooms** behind west_south's three ground-floor windows, seen from the pavement at 1 to 3 m;
  - (b) **rendered into the mapped atlas** behind the parade's first-floor windows, lit or unlit at night by the town's hours.
- **How it is judged.**
  - In the hook camera, and walking past, by day and at night, beside the Hook sheet's upper windows and KCD2's dark, shallow windows with real things in them.
  - Fails if: a room glows by day; two neighbours look alike; a mapped room smears or stretches; nets do not read; anything breaks the content rule; the frame time rises noticeably at 2560 by 1440.
  - A fresh reviewer is told to find the trick.
  - Then Mickey's front office is dressed from the same kit's office set as the second sample, not as a one-off.
- **Effort** [I, estimate]: 5 to 7 builder-days.
  - shell generator and trims 1.5;
  - finishes and furniture 2 to 3;
  - atlas renders and material instances 1;
  - the judging loop 1.

---

## Per family, in one line

- **A, buildings and their parts:**
  - *Free:* CC0 surfaces only (ambientCG, Poly Haven).
  - *We make:* every building as style kits (modules, three trim sheets, our own brick bonds, seeds, wear by rule).
  - *Impossible without a ruling:* any Megascans (flagged NoAI), any paid Fab building pack (rule 3), CC-BY or UE-only building content.
- **B, interiors:**
  - *Free:* CC0 small objects (Poly Haven) and surfaces (ambientCG).
  - *We make:* one room kit for walk-in, through-glass and mapped rooms, plus our own wallpapers, carpets and 1990 furniture.
  - *Impossible without a ruling:* the Megascans goods in today's shop plans, paid interior shaders and kits, wParallax and City Sample interiors.

## What I could not reach or verify

- **UNREACHED:**
  - fab.com and the Fab support pages;
  - api.polyhaven.com and ambientcg.com (curl, CONNECT 403);
  - api.sketchfab.com;
  - ArtStation (dluka.artstation.com);
  - news.ubisoft.com and Medium;
  - historicengland.org.uk;
  - the GitHub API (403), though raw.githubusercontent.com worked.
- **The NoAI flag:** the exact Fab EULA wording behind `isAiForbidden`, and whether every Megascans item carries it. The GOODS note checked the items it listed, not the whole library.
- **Looks unverified:** every ambientCG and Poly Haven id named above is checked by id, not by eye. Nobody here has seen them.
- **Method sources unread:** Watch Dogs: Legion's, Mafia's and KCD2's building kits are known from summaries only. No primary source on GTA's interiors.
- **Not verified in 5.8:** Packed Level Actors, PCG surface sampling for clutter, and per-instance custom data on HISM, as used here.
- **Brick bonds:** the claim that northern Victorian terraces show Flemish or English garden-wall bond is mine. It must be checked against dated photographs before the bond material is built.
- **No photograph found** of a 1990 provincial police station inside.
- **Estimates:** every effort figure here is mine.

## Sources (all read or searched on 3 October 2026)

1. Epic, "Using Shape Grammar With PCG", UE 5.8 docs, undated. https://dev.epicgames.com/documentation/unreal-engine/using-shape-grammar-with-pcg-in-unreal-engine [READ]
2. Epic, "Licenses and Pricing in Fab", undated. https://dev.epicgames.com/documentation/en-us/fab/licenses-and-pricing-in-fab [READ]
3. Fab support, "NoAI meta tags and Created with AI self-declaration", undated. https://support.fab.com/s/article/Introducing-NoAI-meta-tags-and-Created-with-AI-self-declaration [SS]
4. Sketchfab, "Restricting Generative AI Use of Free Models", undated. https://sketchfab.com/blogs/community/restricting-generative-ai-use-of-free-models/ [SS]
5. Daniel Luka, "Watch Dogs Legion – Industrial Building Kits", ArtStation, undated. https://www.artstation.com/artwork/48kakl [SS; UNREACHED]
6. Daniel Luka, "Watch Dogs Legion – Interior Building Kits", undated. https://www.artstation.com/artwork/nYN4y4 [SS; UNREACHED]
7. Daniel Luka, "Watch Dogs Legion – Pub Facades, Pub Counters and Pub Interiors", undated. https://dluka.artstation.com/projects/lxyrXJ [SS]
8. Ubisoft News, "Watch Dogs: Legion – The Tools That Built London", undated. https://news.ubisoft.com/en-us/article/4po3S9Pwp1YcgBmGPmQxAh/watch-dogs-legion-the-tools-that-built-london [UNREACHED; its summary was about Census, not buildings]
9. GamingBolt, "Watch Dogs: Legion's World Will Have 'Dozens' of Fully Fleshed Out Explorable Interiors", undated. https://gamingbolt.com/watch-dogs-legions-world-will-have-dozens-of-fully-fleshed-out-explorable-interiors [SS]
10. Luca Eliseo, "Kingdom Come: Deliverance 2 – Modular kit – Weir", ArtStation, undated. https://www.artstation.com/artwork/wryZ6V [SS]
11. DualShockers, "Grand Theft Auto V's Art Director on Creating Los Santos", undated. https://www.dualshockers.com/grand-theft-auto-vs-art-director-on-creating-los-santos-id-never-want-to-rebuild-a-city/ [SS]
12. BuzzFeed News, "'Way Beyond Anything We've Done Before': Building The World Of Grand Theft Auto V", undated. https://www.buzzfeednews.com/article/josephbernstein/way-beyond-anything-weve-done-before-building-the-world-of-g [SS]
13. Alper Isler, "Mafia: Definitive Edition – The City of Lost Heaven", ArtStation, undated. https://artizan.artstation.com/projects/q9oO6e [SS]
14. PlayStation Blog, "How Hangar 13 remade Mafia", 24 September 2020. https://blog.playstation.com/2020/09/24/how-hangar-13-remade-mafia/ [SS]
15. Cfx.re forum, "24/7 supermarket MLO interior remake for FiveM, all 9 stores", undated. https://forum.cfx.re/t/paid-24-7-supermarket-mlo-interior-remake-for-fivem-gta-v-all-9-stores/5263621 [SS, weak]
16. ranjian0, Building Tools, LICENSE (MIT, 2019) and README (v1.0.13). https://raw.githubusercontent.com/ranjian0/building_tools/master/LICENSE [READ]
17. CG Channel, "Download free Blender 3D building generator Buildify", July 2022. https://www.cgchannel.com/2022/07/download-free-blender-3d-building-generator-buildify/ [SS]
18. Wikipedia, "Terraced houses in the United Kingdom", undated revision. https://en.wikipedia.org/wiki/Terraced_houses_in_the_United_Kingdom [READ]
19. Wikipedia, "Cavity wall". https://en.wikipedia.org/wiki/Cavity_wall [READ]
20. Wikipedia, "Brickwork". https://en.wikipedia.org/wiki/Brickwork [READ]
21. Wikipedia, "Grimsby Ice Factory". https://en.wikipedia.org/wiki/Grimsby_Ice_Factory [READ]
22. Wikipedia, "Tricorn Centre". https://en.wikipedia.org/wiki/Tricorn_Centre [READ]
23. Wikipedia, "Bingo (British version)". https://en.wikipedia.org/wiki/Bingo_(British_version) [READ, partly]
24. Historic England, Listing Selection Guides: Culture and Entertainment; Law and Government; Places of Worship. Also its Nonconformist Places of Worship introduction. Undated. https://historicengland.org.uk/images-books/publications/dlsg-culture-entertainment/ (and the sibling pages) [UNREACHED; SS]
25. RISD Museum, Paul Graham, "Waiting Room, Poplar DHSS, East London", undated. https://risdmuseum.org/art-design/collection/waiting-room-poplar-dhss-east-london-1988038 [SS]
26. Huck, "Stark photos of unemployment offices in Thatcher's Britain", undated. https://www.huckmag.com/article/photos-of-unemployment-offices-in-thatchers-britain [SS]
27. Wikipedia, "Richard Billingham". https://en.wikipedia.org/wiki/Richard_Billingham [SS]
28. British Photography, "Paul Reas", undated. https://britishphotography.org/artists/40-paul-reas/series/other-works/ [SS]
29. Wikipedia, "Museum of the Home". https://en.wikipedia.org/wiki/Museum_of_the_Home [SS]
30. Grimsby Live, "Looking back at Freeman Street from the 1970s to the 1990s", undated. https://www.grimsbytelegraph.co.uk/news/nostalgia/freeman-street-how-it-looked-1453870 [SS]
31. Yorkshire Post, "The story of Hull's Hessle Road community told in 50 years of remarkable photos", undated. https://www.yorkshirepost.co.uk/heritage-and-retro/heritage/the-story-of-hulls-hessle-road-community-told-in-50-years-of-photos-3456518 [SS]
32. Fab listings: British – City Pack https://www.fab.com/listings/cd93dec3-bb73-4a5e-b621-e420d66b1eb6 ; Victorian Street https://www.fab.com/listings/9e1179af-5a01-47cf-9195-e08228d83dbf ; Modular British Buildings (Facades) https://www.fab.com/listings/46798d0d-9450-497c-b004-62c448ea4b4d ; Stylized UK Modular House and Road https://www.fab.com/listings/e1c5d097-5f29-41c3-bf91-a4a6a17a9ae7 . Undated. [SS; UNREACHED]
33. Wikipedia, "Everybody's Gone to the Rapture" https://en.wikipedia.org/wiki/Everybody%27s_Gone_to_the_Rapture ; Richard Court, ArtStation https://www.artstation.com/artwork/qKlXn . Undated. [SS]
34. Project files read here:
    - tools/citypack/catalogue.json (ambientCG, 2,010 material ids, last committed 1 October 2026);
    - THIRD-PARTY.md;
    - tools/art-recipes/terrace-front.py, shop-room.py, fetch_polyhaven.py, mickeys-blockout.py;
    - tools/street_wear.py;
    - production/specs/vignette-scene.json;
    - production/research/shop-window-interiors/GOODS-2026-10-03.md (the `isAiForbidden` finding) and CLOSE-RANGE-2026-10-03.md. [READ]
