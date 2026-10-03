# One asset plan for the whole game (research and plan, 3 October 2026)

**The question (Jafar, 3 October).** LEDGER builds a whole 1990 British port town to the bar of the Hook sheet and the KCD2 frames, by one person directing AI, with almost no money. Every asset needs an allowed source.

**His source rule, in order:**
1. Free and unrestricted assets that fit the setting and the bar.
2. Assets we make ourselves, as kits with variation rather than one-offs.
3. Human-made inputs only by his explicit ruling, which today means none.

**Never used:**
- Assets tagged NoAI, not even as references, because our whole pipeline is AI.
- Real car models and brands (canon).

Clothing quality is a known exception for now.

**This plan covers thirteen families:**
- buildings and their parts;
- interiors;
- cars and other vehicles;
- street furniture;
- shop goods and props;
- food;
- signage and posters;
- decals and wear;
- vegetation;
- the hillside and distant town;
- people;
- clothes;
- accessories.

For each it sets out:
1. how professional games make it;
2. what is free without AI restrictions;
3. the kit method for what we make;
4. the reference that sets the bar;
5. the variety and the one proof before anything is multiplied.

Then come the cars in detail, the order in which the families go into the builder's work after the proof view, and what could not be verified.

**How it was done.** Seven separate helpers each took one area. Each was given the problem, not a theory, worked for about thirty minutes read-only, and gave dated sources. Their notes are beside this file:
- `0-SOURCES-AND-LICENCES.md`: the NoAI tag, every free library's terms, period pictures and fonts, terrain data.
- `1-BUILDINGS-AND-INTERIORS.md`
- `2-VEHICLES.md`
- `3-FURNITURE-PROPS-FOOD.md`
- `4-SIGNAGE-AND-WEAR.md`
- `5-VEGETATION-AND-DISTANCE.md`
- `6-PEOPLE-CLOTHES-ACCESSORIES.md`
- `METHOD-BRIEF.md`: the brief each helper worked to.

This session then checked the deciding facts itself ("Checked here", at the end).

**Marks:**
- **[READ]** read at the source.
- **[PC]** read on Jafar's PC by another session and recorded in this repository.
- **[SS]** search summary only.
- **[I]** inference.
- **UNREACHED** the host refused us. An unreached source is never used as evidence.

**Limits:**
- This cloud session's network refuses Fab, Sketchfab, Poly Haven's and ambientCG's live pages, Geograph, Historic England, archive.org and most other hosts.
- Reachable: Epic's developer documentation, Wikipedia, GitHub and npm.
- The helpers' web searches ran out near the end.
- Nothing was seen in Unreal.
- Every effort figure is an estimate.

## First: one decision that changes the plan (licence, his)

**His NoAI rule, applied as he stated it, removes three things already chosen by his rulings of 1 and 3 October.**

| Fact | Status |
|---|---|
| "The NoAI tag is required for all listings of MetaHuman compatible content. It is applied automatically to these listings." This covers clothing and grooms. | [READ], Epic's documentation, *Selling MetaHumans on Fab* |
| Fab: "The NoAI meta tag indicates that an asset must not be used for generative AI data collection." | [READ], Epic's documentation, *Licenses and Pricing in Fab* |
| The contract clause: no use of NoAI content "(iii) as inputs to Generative AI Programs". Every asset in our pipeline is seen by an AI, in the gate's frames if nowhere else. | [SS], note 0 |
| Epic's **Game Animation Sample**: "Allows usage with AI: No" | [PC], production/research/natural-idles/NOTE.md, read on its Fab page 1 October |
| **Every free Megascans record checked**: `isAiForbidden: true` | [PC], production/research/shop-window-interiors/GOODS-2026-10-03.md |
| Epic's free automotive materials, Megaplants, City Sample and the MetaHuman Crowd Sample: AI not allowed | [SS] only, notes 0, 2, 5 and 6; to be read on his PC |

**What this removes.** Today's plans use:
- the 18 Megascans in his library and the Megascans shop goods (fruit, baking, rope, smoked fish);
- the Game Animation Sample, for the people's poses in proof-view item 2.11;
- **Epic's free MetaHuman garments**, which Fab tags NoAI automatically, for the people's stopgap clothes (his ruling of 3 October).

None of the Megascans is built into the street yet. The wear layer uses ambientCG and our own pictures (tools/street_wear.py, per note 1).

**What stays clean:**
- **The engine's own MetaHuman Creator and plugin.** They come under the Unreal licence, not a Fab listing. Its AI clause bars training, testing or building a database, and allows "workflows that incorporate artificial intelligence technology" [SS, note 6].
- **The CC0 libraries:**
  - Poly Haven: "licensed as CC0", and it names AI researchers using its assets with approval [READ from the site's published source, note 0].
  - ambientCG: CC0 [SS].
  - Sketchfab CC0 items, but only those without a NoAI tag, since a CC0 model can still carry one [SS, notes 0 and 3].
- **Others:**
  - Mixamo: a training clause only.
  - Microsoft Rocketbox: MIT [READ].
  - OFL fonts.
  - Blender's own tools.

**The decision.** Does the NoAI rule remove these, against his rulings of 1 and 3 October?
- **(A, recommended)** Yes, the rule as written. They leave the plan:
  - the people's poses come from the engine's own MetaHuman clips and Mixamo;
  - the stopgap clothes come from what passes our gate;
  - the wear, ground and food come from Poly Haven, ambientCG and the CC0 scans.

  The plan below is written for (A). It loses little: every family's free base is already CC0.
- **(B)** An exception for Epic's own content used only inside the game.
- **(C)** Keep them, as now.

Whatever he picks, the builder should open each listing in his library signed in and record its "Allows usage with AI" line. Most of the evidence above is two days old or a search summary.

## The plan, family by family

What is common to every family (notes 1 to 6, and the street research):

**The kit method.**
- Few parts on a grid.
- Shared trim sheets.
- Variety from data: seeds, swaps, colour sets, wear masks.
- Placement by rule.
- Wear by rule.

**How an agent drives it.** It writes and runs Blender recipes headless (tools/art-recipes/, as terrace-front.py and shop-room.py do now). It drives Unreal by script: placement lists, PCG, and 5.8's shape grammar, for which Epic ships a skill "designed to guide a LLM" (street research).

**What the agent cannot do is judge.** Every proof is judged in the game's camera at 2560 by 1440:
1. by the builder, beside the Hook sheet and the KCD2 frames;
2. then by a fresh reviewer;
3. then by Jafar, on whole frames.

**Words and pictures.**
- **The image model never draws words.** The batch of 3 September printed "BRITHH WORIKER" (checked here).
- It may draw pictures with no words. Every word is our own text layer, set in OFL fonts.

### 1. Buildings and their parts (note 1)

1. **Professional practice.** Modular kits on a grid with three or so trim sheets, assembled by rules with a seed per building. A "style sheet" per building age. Real depth where the camera looks. Watch Dogs: Legion, the Mafia remakes and KCD2 work this way [SS]; 5.8's shape grammar does it in the engine [READ, street research].
2. **Free.** Surfaces only: CC0 bricks, concretes, plasters and stone from ambientCG and Poly Haven. **No free building or building kit fits 1990 Britain.** British packs on Fab are paid or modern London, and unreached.
3. **We make.** One style kit per building age, extending terrace-front.py:
   - parts on the brick grid;
   - three shared trim sheets: sills, lintels and copings; window and door joinery; shopfront mouldings;
   - **our own brick-bond material**;
   - a seed per house for its height, door, paint, pots, alterations and wear.

   The agent writes the modules and the placement list; the eye judges.
4. **Reference.** Dated period photographs (production/reference/photographs.md) for proportions, reveals, bonds, shopfront mouldings and alterations; the Hook sheet for massing and mood. Designs are never copied.
5. **Variety and proof.**
   - **Variety:** about 15 to 17 styles in three tiers:
     - **Quay Street needs four:** the Victorian shop parade, the by-law terrace, the dock warehouse and the quay shed.
     - The rest of the Hook adds five: a corner pub as a place, a chapel, the Harbour Board offices, a smokehouse and lock-ups.
     - The town adds eight: the Tivoli, the closed school, 1930s council houses, postwar council flats, a 1960s precinct with the police station, Edwardian offices, resort terraces and industrial sheds.
     - About 350 to 500 modules in all; six brick sets.
   - **The proof:** Quay Street's six facing frontages, Mickey's and the next two plus the three west_south houses opposite, as two styles of one kit. It is proof-view items 2.4 and 2.5, done as a kit, about 6 to 9 builder-days.
   - **The test of the method:** the same kit, with new seeds, builds a hillside row with no new pieces.

### 2. Interiors (note 1)

1. **Professional practice.** Real rooms only where the player stands close. Everywhere else, "interior mapping": a room rendered once and shown in the window's depth (Spider-Man, City Sample). A trade template dressed per shop (GTA).
2. **Free.** CC0 small objects and surfaces (Poly Haven, ambientCG). The free interior shaders and kits are UE-only, paid or unreached, so they need a ruling.
3. **We make.** One room kit with three uses: walk-in rooms, rooms behind glass at 1 to 3 m, and rendered rooms for the upper and far windows.
   - **Parts:** a shell from the plan, one trim sheet, six finishes (wallpapers, carpets, lino, paint), about 15 furniture pieces from dimensions or Poly Haven, and nets, curtains and blinds.
   - **Shop rooms:** tools/art-recipes/shop-room.py, the method of Rita's window, which he called the best thing on the page.
4. **Reference.** Dated photographs of 1990 front rooms, shops and offices. Note 1 found no photograph of a 1990 provincial police station inside.
5. **Variety and proof.**
   - **Variety:**
     - the 12 shop rooms on Quay Street (his trades of 3 October);
     - about 20 mapped rooms: 8 room types × 2 or 3 seeds, lit and unlit;
     - 6 to 10 walk-in spaces later: Mickey's three rooms, a terraced home, the police station, the tea room, the pub without drink.
   - **The proof:** one domestic room kit, three households, two distances:
     - real rooms behind west_south's ground-floor windows;
     - mapped rooms behind the parade's first floor, lit at night by the town's hours.

     About 5 to 7 builder-days. Mickey's front office is then dressed from the same kit's office set, not as a one-off.

### 3. Cars and other vehicles (note 2; the full section on cars is below)

1. **Professional practice.** GTA, Sleeping Dogs, Watch Dogs: Legion and Cyberpunk invent the maker and the badge, blend cues from a class, and drive variety from data. GTA V gives each model up to 25 colour sets, plus parts, liveries and dirt [SS]. Cyberpunk gives each invented maker an ethos [SS].
2. **Free.**
   - **Nothing free fits:** no free, allowed, fictional period car, van, bus or boat exists.
   - Epic's free automotive materials were recommended on 1 October. They are now reported NoAI [SS], so out under (A) until read otherwise.
   - Free and allowed: Poly Haven's CC0 covered car, old tyre and rusted rims, for a yard.
3. **We make.**
   - **Platforms:** a loft generator per body type, with swappable noses, tails, bumpers, lamps and wheels, and paint and wear from data.
   - **Our own car-paint master material:** a clear coat with fade and wetness.
   - **A canon test,** below.
4. **Reference.** Dated photographs of 1990 British streets (photographs.md R07, R09) for period markers. Dimensions only from class blueprints, never shapes. **The Hook sheet's cars look late-1990s** [I, note 2]: the sheet governs where cars stand and how they sit wet in the frame; the photographs govern their design.
5. **Variety and proof.**
   - **Variety, staged:**
     - the proof view: 1 platform, 3 cars;
     - the street-wide pass: 4 platforms, about 12 looks;
     - the town: about 20 more kinds (vans, lorries, buses, police, ambulance, milk float, two-wheelers);
     - the harbour: about 8 boats.
   - **The proof:** proof-view item 2.10. One small family hatchback built the whole way, then a second made only by swapping parts, at the rank. About 4 to 6 days.
   - Until it passes, the street has no cars (his ruling of 2 October).

### 4. Street furniture (note 3)

1. **Professional practice.** Modelled kits on trim sheets, a few master materials with wear masks, many instances placed by rule. Scanned hero pieces only where a scan exists.
2. **Free.** CC0 materials (Poly Haven, ambientCG), a chain-link fence and a few quay objects. **No allowed free period British furniture.**
3. **We make.** About 25 kinds and 30 models:
   - the lamp column (exists), bollards, litter bins, the galvanised dustbin;
   - the KX100 kiosk, re-materialled: brushed stainless, grimy glass, the payphone;
   - the pillar box;
   - the bus stop, benches and railings;
   - name plates and road signs;
   - Belisha beacons, grit bins, telegraph poles and wires;
   - covers and gratings, kerbs, mooring bollards and cleats.

   Each has two to four material states with wear.
4. **Reference.** Period photographs of each piece (note 3 names them) and dimensions from the standards: the KX100's drawings, the pillar box's size.
5. **Variety and proof.**
   - **The proof:** the kerbside run, about 10 m of pavement nearest the hook camera, all from the kit, wet, by day and night. It is the furniture half of proof-view item 2.8, about 4 to 6 days.
   - **Canon owes** the kiosk operator's mark, the pillar box's cypher and a council name.

### 5. Shop goods and props (note 3)

1. **Professional practice.** Scanned hero goods with instancing. Printed goods as simple meshes carrying good graphics (Naughty Dog's tagged one-off library [SS]).
2. **Free.** Poly Haven's CC0 crates, drums, tools, buoys, kettle, tea set, chalk board and an office desk.
3. **We make:**
   - **Containers, about 12:** wooden and plastic fish boxes, market crates, pallets, milk crates, boxes, sacks.
   - **Soft goods,** each with 4 to 6 baked shapes: bin bags, tarpaulins, nets.
   - **Paper,** as atlas tiles: bundles, bills, tickets, chip papers.
   - **Litter:** about 10 kinds, hundreds of instances.
   - **The cab office's props, about 15:** radio, phones, ledgers, typewriter, board.
   - **Household props:** about 10.
4. **Reference.** Dated photographs of Grimsby and Hull fish docks and shop doorways (note 3).
5. **Variety and proof.** The proof is the fishmonger's pavement:
   - a stack of fish boxes, one with ice and fish;
   - a pallet;
   - bin bags;
   - a milk crate at the next door;
   - the newsagent's A-board;
   - gutter litter.

   All placed by the generator. About 3 to 4 days.

### 6. Food (note 3; shop-window-interiors notes)

1. **Professional practice.** Photoreal games scan food (Final Fantasy XV, Resident Evil 7 [SS]). Hand-painted food is the stylised route and reads as toys against our bar.
2. **Free:**
   - **Poly Haven's CC0 fruit and cakes.**
   - **ffishAsia's CC0 fish, crab and prawn scans on Sketchfab,** with each one's tags read at download for NoAI.
   - Out under (A): the Megascans food in his library.
3. **We make:**
   - crushed ice, fillets, kippers, dressed crab;
   - a pile generator that places 3 to 6 distinct pieces a pile;
   - takeaway food, scones, pies and sweets.
4. **Reference.** Dated photographs of 1990 fishmongers' slabs and greengrocers (Picture Sheffield t13140, note 3).
5. **Variety and proof.**
   - **Variety:** about 9 fish kinds, 14 fruit and vegetables, 8 baked goods, 6 tea-room dishes, 6 takeaway and 5 sweets.
   - **The proof:** the fishmonger's slab, his next shop after Rita's, about 3 to 4 days.

### 7. Signage and posters (note 4)

1. **Professional practice.** In-house graphic design of every fictional brand, then templates with a text layer, aged in the material (GTA, L.A. Noire, Mafia [SS]).
2. **Free.** About 40 OFL fonts whose licences were read, close to period lettering:
   - Marcellus SC, already ruled, for name plates and Mickey's;
   - Jost for Futura-like fascias;
   - Libre Franklin for newspaper bills;
   - Courier Prime for police forms;
   - and others (note 0's table).

   **No 1990 poster is public domain:** Crown copyright on a 1990 government poster runs to the end of 2040 [READ].
3. **We make.** Every fascia, projecting sign, window lettering, card, ticket, notice, bill, poster and graffiti tag:
   - from data-driven templates, with our own text layer;
   - the image model for pictures with no words;
   - aged by its wall's seed.

   Graffiti uses canon's five minted tags, which no longer block the bill of materials' G7 row.
4. **Reference.**
   - Dated photographs of 1990 shopfronts, newsagents' boards and fly-posted walls.
   - The Hook sheet for Mickey's: gilt capitals standing out from a slate-blue board. **The game's Mickey's is flat PT Sans** [READ, note 4].
5. **Variety and proof.**
   - **Variety:**
     - 12 fascias on Quay Street, 60 to 80 town-wide from 6 styles;
     - about 300 cards and tickets from 25 templates;
     - about 30 notices;
     - about 40 fly-posters;
     - 15 poll-tax and election bills;
     - about 100 graffiti placements.
   - **The proof:** Mickey's and the next two fronts signed to the bar:
     - Mickey's in Marcellus SC gilt;
     - the fishmonger sign-written;
     - one fly-posted wall with three templates in two seeds;
     - one QUAY FIRM tag.

     It belongs to proof-view item 2.6, about 3 to 4 days.

### 8. Decals and wear (note 4)

1. **Professional practice.** Four layers:
   - dirt in the materials;
   - rule-placed decals on walls;
   - ground marks cached in a virtual texture;
   - a few hand-placed.

   Grunge masks and vertex blends. D53, "grime is the strategy".
2. **Free:** ambientCG's CC0 decals and imperfections, 16 sets already staged. Out under (A): the Megascans leakage, oil and grunge decals in his library.
3. **We make.** About 18 kinds of wear, from today's 8, each with 4 to 6 seeded masks of our own, coloured by surface and placed by rule. The rules need no handwork, so the town costs no more than the street.
4. **Reference.** The Hook sheet's wall feet, streaks and wet pavement; KCD2's streaks under every ledge; his words of 2 October: wear that reads at a glance across every facade.
5. **Variety and proof.** The same three near frontages with their pavement and gutter, all four layers, wet. It belongs to proof-view items 2.4 and 2.7, about 3 to 5 days.

### 9. Vegetation (note 5)

1. **Professional practice.** Scanned plant atlases on our own meshes, Nanite foliage, placement by rule where water and neglect put plants.
2. **Free:**
   - Poly Haven's CC0 plant scans: nettle, dandelion, weed clumps, a grass tuft, shrubs, a small tree, two windswept coastal trees, a mossy stump [SS].
   - ambientCG's CC0 ivy and leaf atlases [SS].
   - Blender's own Sapling Tree Gen and IvyGen [READ].
   - Megaplants are reported NoAI [SS], so out under (A).
3. **We make.** Every tree, ivy mass, hedge and weed clump as a seeded kit, placed from the street generator's own kerb, joint and wall lines.
4. **Reference.** Dated photographs of northern port towns: buddleia on derelict sites, weeds in flag joints, moss on copings, sycamores.
5. **Variety and proof.**
   - **Variety:** about 24 weed variants, 4 wall plants, 3 buddleias, 3 ivy masses, 5 garden pieces, 16 trees.
   - **The proof:** "the neglect pass" on the three near frontages and the bend: gutter weeds, moss, one buddleia, ivy on a gable, wet leaves, the sycamore where the sheet has its tree. Inside proof-view items 2.7 and 2.9, about 2 to 3 days.

### 10. The hillside and the distant town (note 5)

1. **Professional practice.** The street's own kit reused at distance. HLOD and instancing for the middle distance; impostors and cards only far away (GTA V's distant LODs, Spider-Man's skyline [SS]).
2. **Free:**
   - **The engine's own HLOD, instancing and impostor tools.**
   - **The CC0 skies already fetched.**
   - **Terrain.** The Environment Agency's LIDAR and Ordnance Survey data are under the Open Government Licence, which would need a ruling. They are not needed: the atlas sets a 45 m crest.
3. **We make.** The hill from the building kit at lower detail, as real geometry:
   - The hill sits 110 to 206 m from the hook camera, so a house there is 55 to 125 pixels wide. It cannot be a painted card, as his ruling says: "the hill built properly".
   - Then about eight far landmarks (a church tower, cranes) and cards for the town at 0.5 to 3 km.
4. **Reference.** Dated photographs of British port towns with terraced hills, for massing in haze.
5. **Variety and proof.**
   - **Variety:** 6 house bodies × materials; 3 roofs; 3 stacks; walls; stairs; 8 landmarks; 3 card layers.
   - **The proof:** proof-view item 2.9 by this method, about 2 to 4 days plus a day of planting.

### 11. People (note 6; wardrobe-at-scale, casting, natural-idles)

1. **Professional practice.** Every game studied uses the same method:
   - a few bodies and heads;
   - garments in fixed slots, fitted to every body;
   - variety from material, colour, accessories and scale;
   - a written recipe per kind of person;
   - walks out of step.

   Studied: City Sample, RDR2, KCD2, Mafia, Watch Dogs: Legion.
2. **Free:**
   - **MetaHuman Creator and the engine:** bodies, faces, 31 locomotion clips, the 5.8 crowd tools.
   - **Mixamo.**
   - **CC0 MPFB2 heads.**
   - **Out under (A):** the Game Animation Sample, the MetaHuman Crowd Sample, City Sample Crowds and Fab grooms.
3. **We make:**
   - faces aged and varied by script;
   - period hair from Blender curves;
   - idle sets;
   - the recipe system.
4. **Reference.** The Hook sheet's people: older men and women in dark wool, mostly seen from behind at 8 to 40 m. Dated photographs of 1990 northern street crowds.
5. **Variety and proof.**
   - **Variety:** 14 principals, about 30 regulars, 30 to 40 passers-by, 10 to 25 on screen; later 200 to 500.
   - **The proof:** three passers-by from one recipe, "older man, out on foot". Each has a different face, build, groom, coat cloth, headwear and hand item, with walks out of step. Judged beside the sheet's two foreground men. About 8 to 14 days, **the coat being the risk**.

### 12. Clothes (note 6; free-garments, wardrobe-at-scale)

1. **Professional practice.** Base garments as skinned meshes, a cloth library, recipes. The ten tailored silhouettes need professional patterns, which we cannot author (his rulings of 2 and 3 October).
2. **Free:**
   - CC0 and CC-BY meshes: CC-BY garments are allowed with credit (2 October), but are weak.
   - CC0 fabric textures.
   - CLO's free patterns are allowed, but draping is stopped.
   - Out: Epic's free MetaHuman garments (NoAI automatically, [READ]) under (A), and every ready-rigged suit read at $40 or under (NoAI).
3. **We make.** The simple base garments, with fabric, colour and wear variants. **Tailoring stays a blocked capability**, the known exception.
4. **Reference.** Dated photographs of British suits and coats, 1987 to 1991.
5. **Variety and proof.**
   - **Variety:** about 40 base garments for the first street (note 6).
   - **The proof:** the coat inside the people proof above. A crowd-distance rubric (decision 3 below) would let one coat dress the crowd before tailoring is solved for the principals.

### 13. Accessories (note 6)

1. **Professional practice.** Parametric pieces on sockets, many variants from one base.
2. **Free:** almost nothing allowed. Poly Haven's suitcase; MakeHuman's CC0 glasses and hats, unseen.
3. **We make.** Parametric Blender kits on sockets: caps, hats, bags, umbrellas, spectacles, cigarettes and lighters, newspapers, carrier bags, watches. Four have already passed blind review: Sheila's handbag and spectacles, Darren's belt and pager (tools/meshgen/blender/model_accessory.py).
4. **Reference.** The same dated photographs as clothes.
5. **Variety and proof.** Inside the people proof: a flat cap, a woolly hat, a folded paper, a cigarette, a carrier bag.

## Cars specifically: what a 1990 British street had, and how to make fictional ones (note 2)

**The body types, with a mix for Quay Street.** The shares are estimates for parked vehicles on a working port street [I]. The sizes are class ranges [I], to be checked against blueprints for dimensions only.

| Body type | Share | Length (m) | What reads 1990 |
|---|---|---|---|
| Supermini, 3- or 5-door | 25–30% | 3.40–3.75 | Tall upright glasshouse, thin pillars, black wraparound bumpers, rectangular lamps beside a slot grille |
| Small family hatch or short saloon | 25–30% | 3.95–4.20 | Wedge nose, black bumpers with a rubbing strip, black mirrors, ribbed horizontal tail bands |
| Large family hatch or saloon | 15–20% | 4.30–4.50 | The newest "aero" (flush glass, wraparound lamps) beside older square three-boxes |
| Estate | 8–10%, more on the rank | 4.40–4.80 | Long flat roof, upright tailgate, roof bars |
| Executive saloon | 3–5% | 4.65–4.90 | Long bonnet and boot, upright grille |
| 1970s survivor | 5–8% | 4.0–4.5 | Chrome bumpers, round lamps, suffix plate, rust: right as a minority, wrong as the majority |
| Car-derived van | 2–4% | 3.9–4.2 | The car's front, a tall box behind, no rear side glass |
| Panel van | 4–6% | 4.6–5.3 | Snub nose, sliding side door, twin rear doors |
| Luton van; 7.5 t box lorry | 1–2%; 0–1 at a time | 6.0–6.5; 7.0–8.5 | The box over the cab; a fish lorry on the quay |
| Minibus; single- and double-deck buses | on routes | 5.5–7; 10.3–11.9; 9.5–11.1 | Minibuses are the post-1986 deregulation tell [READ]. Rear-engined deckers. The operator is invented |

**The period markers**: black plastic bumpers, rectangular headlamps, steel wheels with plastic trims, red, blue and white paint with faded reds, a paper tax disc, a mast aerial, rust at the arch lips of older cars.

**1990 plates** [READ, the standard]:
- Prefix plates such as "G123 ABC". G until 31 July 1990, H from 1 August.
- About half the street on older suffix plates [I].
- White at the front, yellow at the rear.
- Characters 79 mm high on a 520 × 111 mm plate.
- Note 2 proposes drawing the characters as geometry from the standard's dimensions, to need no font licence [I, not checked against the standard's own copyright terms]. Every plate is invented.

**Special vehicles:**
- **Police:** the white "jam sandwich" stripe. Battenburg came only in the mid-1990s [READ].
- **Ambulance:** a white van conversion.
- **Postal van:** red, with no cypher until canon mints one.
- **Milk float:** a dairy name, invented.
- **Minicabs:** ordinary saloons and estates with a council plate, a whip aerial and a door sticker. One or two on the rank (his ruling of 22 September).
- **No ice-cream van** (no children) and **no brewery dray** (no alcohol).

**How to make fictional ones that read as their era without resembling any real model:**
1. **Invent about four makers, each with an ethos,** as Cyberpunk does. For example: "the cheap British family maker", "the solid Swedish-style box maker", "the French soft-rider". Badges are abstract and illegible at game distance. Canon mints the names.
2. **Blend a class; never copy a car.** Each variant's brief names three or more real cars of its class for **dimensions only** (its provenance line, kept beside the asset). It draws fresh the grille, headlamp graphic, tail-lamp graphic, window outline and rear pillar. It picks the bumper era. Proportions for the agent: height over length about 0.38 for a supermini and 0.31 for a family saloon; wheelbase 0.60 to 0.66 of the length; glass about 0.35 to 0.40 of the height, taller than in 2000.
3. **The named-at-a-glance list.** No variant echoes a signature a British eye names at once: the Mini, Metro, Sierra, Escort, Cortina, Capri, Cavalier, Golf's rear pillar, Volvo 240, Mercedes W123, Land Rover, black cab, Routemaster, and the rest in note 2.
4. **The blind test.** A fresh reviewer, with no provenance, gets side, front, rear and three-quarter renders and is asked: "What make and model is this? What country and years?"
   - **Pass:** no model named with confidence, and placed in Britain or Europe, 1985 to 1991.
   - **Fail:** a confident name. Change that feature and run again.

   One test checks both halves: it reads as its era, and it resembles no model.
5. **Kit and agent.** A loft generator per platform, with swappable nose, tail, bumpers, lamps and wheels. Paint, colour set, plate, dirt and dents come from data, as GTA V's colour sets do. The agent writes the brief, builds by script and runs the blind test. The eye judges stance and reflections first: "stance sells character more than micro-detail" (1 October note).

## Faults found on the way (for the builder; read and checked here)

1. **The street's brick is laid in stretcher bond** (terrace-front.py, line 5672: "laid in stretcher bond"; the held Poly Haven brick_4 too). Stretcher bond belongs to the twentieth century's cavity walls. A Victorian solid wall shows headers, in Flemish or English garden-wall bond (note 1; standard building history [I]; check against dated photographs). The fix belongs to proof-view item 2.4.
2. **The generated sign batch of 3 September breaks canon and spells badly.**
   - Rita's picture reads "BRITHH WORIKER" (looked at here).
   - The batch also holds a bingo poster, a pub darts sheet, a pub's back bar and a "MARQUEE" sign (ledger/Assets/StreamingAssets/Decals/generated).
   - The scene file still names the fish market, Rita's and Steam Laundry fascias from that batch (vignette-scene.json, lines 680 to 698). By its crop numbers, Rita's misspelt band is cut off [I].
   - **Recommended:** retire every picture in the batch that carries words, and every one that breaks the content rule.
3. **The brand bible still says "MICKEY'S IS A PUB AND STAYS A PUB"** (content/brands/brand-bible-v1.json). Found by the rulings sweep too; still unchanged.
4. **Mickey's fascia is flat PT Sans,** not the sheet's gilt capitals. Marcellus SC is closer and already ruled.
5. **Graffiti is no longer blocked:** the bill of materials still holds row G7 "HELD", though canon minted the five tags on 2 September.
6. **The phone kiosk's size in the scene file is 0.914 m square by 2.515 m** ("3 ft square in plan and 8 ft 3 in tall"), which note 3 reads as the older K6's size, while the recipe draws a KX100 [I]. Check against the KX100's drawings.

## The order in which the families go into the builder's work

The proof view (item 2 of his one ordered list) already holds the first proof of nine families, in his order: brick, facades, shopfronts with signs and interiors, ground, props, hill, cars, people's poses, night, grade. The voice test (item 3) comes next, then **the street-wide pass (item 4)** and **the friends' build (item 5)**.

**Order for planning the families into the builder's work,** with reasons:

1. **Before item 4, his ruling on NoAI (decision 1).** Several proof-view items name sources it removes: 2.6 and 2.8 the Megascans goods, 2.11 the Game Animation Sample.
2. **Buildings and wear, together (families 1 and 8).** They fill most of every frame, and every other family sits on them. Their proofs are proof-view items 2.4, 2.5 and 2.7 done as kits. The street-wide pass is then mostly re-seeding the same kit along the whole street. The brick bond is fixed here.
3. **Signage and interiors behind glass (families 7 and 2).**
   - Every shop on the street needs a fascia and a room.
   - His ruling is that "the other eleven shopfronts are made like" Rita's.
   - Cheap, high in the frame, and it retires the faulty sign batch.
   - Then the mapped rooms for every upper window.
4. **Street furniture, props and food (families 4, 5 and 6).** The kerbside run, every doorway's two to four objects, and the fishmonger's slab, then the grocer and tea room. They make the street lived in at the friends' walking distance.
5. **Vegetation, and the hillside (families 9 and 10).** The neglect pass along the whole street, and the hill finished by the building kit. Planting is cheap once the kit exists.
6. **People and accessories (families 11 and 13), with clothes at crowd distance (12).** The friends' build needs people in the street, but the coat is the risk and tailoring is blocked. Prove the three passers-by, then multiply recipes only after his yes in the game.
7. **Cars (family 3).** Only once the proof car passes; the street has none until then (his ruling). The street-wide pass then has 4 platforms and about 12 looks.

**After the friends' build** (ROADMAP stages 2 to 6):
- moving traffic (stage 2, his G4) from the same car kit, with vans and buses;
- walk-in interiors for the story: a home, the police station, the tea room;
- the rest of the Hook's buildings and the harbour's boats;
- the far town seen from the quay;
- then the town's other districts, tier by tier;
- tailoring, whenever it is unblocked.

## Decisions for Jafar

1. **Licence: NoAI and the content already chosen** (above): (A, recommended) the rule as written; (B) an exception for Epic's own content inside the game; (C) keep them as now.
2. **Canon: names still owed**, now needed by several families:
   - the car makers;
   - the police force, bus operator, ambulance service and dairy;
   - the kiosk operator's mark and the pillar box's cypher;
   - a council;
   - the local paper.

   Options: (A, recommended) the town session mints them within canon, as the graffiti tags were on 2 September, struck on sight if he disagrees; (B) he names each.
3. **Scope: a crowd-distance rubric for clothes:** (A, recommended) passers-by judged from 8 m out, so one coat can dress the crowd before tailoring is solved; (B) one rubric for everyone.
4. **Canon: the 1990 poll-tax posters:** (A, recommended) no party names and no real people, with generic slogans from an invented local campaign; (B) real party names; (C) no political posters.

5. **Licence: his Claude account's "Help improve Claude" setting:** (A, recommended) switched off, so the MetaHuman renders our sessions send to Claude are never used to train a model, which MetaHuman's licence forbids [SS, note 6]; (B) leave it.

**Rulings needed later, not now:**
- **The Open Government Licence,** for road-sign lettering when road signs are made. The free versions of the Transport typeface are either non-commercial or derived from the Department for Transport's drawings under the OGL (note 4). Without it, road signs use a near OFL face and read less true [I].

**Rulings the plan does not need:** the OGL for terrain, CC-BY for boats and props, and every paid pack.

## Checked here (this session, 3 October 2026)

- **Epic, *Selling MetaHumans on Fab*** [READ]: "The NoAI tag is required for all listings of MetaHuman compatible content. It is applied automatically to these listings." The CC BY licence is disabled for them, and it covers clothing and grooms.
- **Epic, *Licenses and Pricing in Fab*** [READ]: "The NoAI meta tag indicates that an asset must not be used for generative AI data collection." The tag requires the Standard licence.
- **Our own notes:**
  - the Game Animation Sample's "Allows usage with AI: No" (production/research/natural-idles/NOTE.md, line 43, read on Fab on 1 October);
  - Megascans' `isAiForbidden: true` (production/research/shop-window-interiors/GOODS-2026-10-03.md, line 93).
- **The brick bond in the code** (terrace-front.py, line 5672) and the flags' stretcher layout (line 5497).
- **The generated Rita's sign,** looked at: "BRITHH WORIKER". Its crop in vignette-scene.json, and the batch's bingo, darts, bar-back and marquee files.
- **The kiosk's size note** in vignette-scene.json, and the G7 graffiti row still "HELD" in vignette-bill-of-materials.json.
- **Poly Haven's CC0 terms,** from the site's published source (note 0), and the OFL fonts' licence files (note 0).

## What could not be verified

- **Every Fab listing at its source:** the "Allows usage with AI" line on each of the 18 Megascans in his library, the food scans, Epic's automotive materials, the Game Animation Sample (read on 1 October; to be re-read), Megaplants, City Sample and the Crowd Sample.
- **Fab's full EULA wording** behind the NoAI tag and `isAiForbidden`. The "(iii) as inputs to Generative AI Programs" clause is from search summaries.
- **The MetaHuman licence's AI clause** in full. "Workflows that incorporate artificial intelligence technology" is from search summaries.
- **Anything seen by eye** on Poly Haven, ambientCG or Sketchfab. Every free item here is known by its id, title and licence only. Each must be looked at against its photograph before use, which is the gate's first check.
- **Each ffishAsia scan's tags** (a CC0 model can carry NoAI), and Sketchfab's ownership. A search summary says Epic sold Sketchfab to KitBash in August 2026, unverified.
- **Period photographs:** Geograph, Historic England, Picture Sheffield, Flickr and the national archives were unreached. The photographs named in the notes are leads from summaries and photographs.md.
- **Car class dimensions and market shares,** from memory and summaries [I]. Check against blueprints before modelling.
- **Professional practice** for KCD2, Watch Dogs: Legion, Mafia and GTA: from articles seen as search summaries, not primary sources.
- **Not tested in 5.8 here:** shape grammar facades, Packed Level Actors, PCG clutter, the Crowd plugin, interior mapping on the RX 6700.
- **The brick bonds of northern Victorian terraces,** to be checked by eye against dated photographs.
- **Every effort figure** is an estimate.
