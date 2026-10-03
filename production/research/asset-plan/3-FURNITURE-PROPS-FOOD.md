# Asset plan 3: street furniture, shop goods and props, food

Research note, 3 October 2026, by a separate helper, about thirty minutes. Read only; nothing in the repository was changed.

Marks:
- **[READ]** read at the source, by me, today.
- **[READ earlier]** opened by an earlier helper from Jafar's PC (its note is named); not re-opened by me.
- **[SS]** search summary only.
- **[I]** my inference.
- **UNREACHED** the page refused me. Nothing rests on an unreached page.

Reached from here: WebSearch, and WebFetch on dev.epicgames.com and en.wikipedia.org. Refused: www.fab.com, media.gdcvault.com, aiandgames.com (WebFetch); api.polyhaven.com, ambientcg.com, api.sketchfab.com, 3d-api.si.edu and api.si.edu (curl, "CONNECT tunnel failed, 403"). I used 22 searches.

---

## 0. Read first: three licence facts that change the plan

### 0.1 The free Megascans may all be NoAI. Under the owner's rule that removes them.

- The GOODS note (3 October) read Fab's own data records from Jafar's PC: "Every Megascans record checked carries `isAiForbidden: true`" [READ earlier, GOODS-2026-10-03.md, section 2].
- The clothing screening of 2 October treated exactly that field as the NoAI tag and rejected 247 suits on it (production/art/clothing/SCREENING-2026-10-02.md). Two suits were rejected on 3 October for the same reason (DECISIONS.md).
- Fab's own words are narrower than our rule: "The NoAI meta tag indicates that an asset must not be used for generative AI data collection" [READ, source 1]. Our rule (the brief): NoAI assets are "never used, not even as references".
- **So, by the rule as written, every Megascans item in his library whose field is true is out.** That includes the food, rope coils, pallets and paint cans the GOODS note listed, and the decals, asphalt and brick of the proof frame (production/specs/fab-free-megascans.md). His library was filled today on the opposite assumption (DECISIONS.md, 3 October).
- I could not check the field: www.fab.com was refused (UNREACHED, source 3).
- **What is needed:**
  1. The builder reads `isAiForbidden` for every item in his Fab library, from his PC, and writes the list down.
  2. If any are true, it goes to Jafar as one licence question: (a) the rule as written: no NoAI asset, Megascans included, as with the suits; or (b) Fab's own meaning: NoAI forbids generative-AI data collection, so agents placing a Megascans asset by script may use it, but it is never fed into an image or 3D generator.
  3. **My recommendation: (a)**, for consistency with the suits. For my three families it costs little: everything below is planned so it works without Megascans. Megascans appear only in a column marked "only if (b)". It costs the proof frame's ground and wall materials much more; that is for the other notes to weigh.

### 0.2 A CC0 model on Sketchfab can still carry the NoAI tag

- Sketchfab lets creators put the NoAI tag on Creative Commons models. It says the tag "may not be enforceable" outside Sketchfab, because CC licences allow AI use [SS, source 4 and 5].
- Our rule bars anything *tagged* NoAI, whatever its licence. So every ffishAsia scan and every other Sketchfab CC0 model needs its tags read at download, not only its licence. The tags are in each model's record, which his token can read through the API.
- **Sketchfab changed owner.** Epic sold Sketchfab and ArtStation to KitBash, announced 10 August 2026 [SS, source 6]. Terms may change. Record the licence and the tags of each model on the day it is downloaded, in THIRD-PARTY.md, as the ruling of 3 October already asks.

### 0.3 Poly Haven and ambientCG are clean

- Poly Haven: everything CC0. Its API page explicitly allows bulk download as AI and machine-learning training data, and its blog "AI and Poly Haven" says it chose to be part of the source data for training [SS, source 7]. No AI clause.
- ambientCG: everything CC0 1.0 [SS, source 8]. No AI clause found.
- **These two, plus our own kits, are the safe backbone for all three families.**

---

## 1. What the earlier notes already found (summary only)

| Note | What it settled for these families |
| --- | --- |
| street-clutter-1990 (29 Sep) | Ten pieces with types, sizes, materials and photo leads: EIIR Type A pillar box (about 150 cm above ground, 49 cm across); KX100 in 1985 to 1991 livery (890 mm square, about 2,190 mm tall); concrete column with a Thorn Beta 5 SOX lantern; Belisha beacons and zebra; bus stop flag (diagram 970, 450 × 375 mm); Kindersley-style name plate; litter bin, bollard and grit bin (all weak); galvanised dustbin (about 575 mm tall). No allowlisted model of a KX100, beacon or sodium lantern. Pillar boxes and K6s on Sketchfab are CC BY only. |
| period-vehicles-and-props (1 Oct) and aaa-street note 4 | The method is mid-poly with a bevel on every edge, weighted normals, a few master materials with wear masks, and decals. "The gap is materials and wear, not triangles." Skip about 2.6 × 1.5 × 1.2 m; pallet 1,200 × 1,000 mm. No allowlisted British kiosk, pillar box or skip. Script all furniture. The kiosk's operator mark and the pillar box's cypher are owed by canon's brand bible. |
| aaa-street SUMMARY and 5-PROOF-FRAME | Set dressing in three tiers: primary (signs, blinds, A-boards, stalls: about ten hand-built assemblies); secondary (bins, posts, bollards, covers) and tertiary (litter, leaves, cigarette ends), both scattered by rule. The hook frame has about 10 props; KCD2's arcades frame has 40 or more. Proof-frame item 8 raises clutter to 40 to 60 items, 4 to 7 days. |
| shop-window-interiors GOODS (3 Oct) | Scans for organic goods; printed goods as simple meshes with our own labels from one atlas, a tile chosen per instance; paper needs real thickness; piles from three to six distinct pieces; faked glass jars. Lists ffishAsia CC0 fish, crab, prawns, fruit and veg, Poly Haven fruit and cakes, and Megascans food (now under 0.1). Gives methods for crushed ice, fillets, kippers, dressed crab, prawns, sweets, chocolate boxes, papers, paint tins, ropes, the sou'wester, scones and tomatoes. |
| FISHMONGER (3 Oct) | White glazed tiles, white serve-over counter, white trays, whitewash lettering on the glass (seen by the builder, Picture Sheffield t13140 and t13138). Cod fillet about £2.60 a pound in 1990 (ONS). Prices per pound were legal. |
| CLOSE-RANGE (3 Oct) | Real geometry for the near metre. KCD2's barrels "all in one texture atlas using HSL and blendmap variation"; its turnip is a "modified scan" (Svojša). Shelves: bevelled shapes plus one label atlas. |
| cab-office-interior-1990 (30 Sep) | A small provincial office in 1990 most likely ran on paper dockets and voice radio. Period objects: a BT Viscount phone, a Pye "Tulip" desk microphone (real products: shape reference only). Holes: the radio set, the wall map, the drivers' board, notices, kettle, ashtrays. |

What the project already holds (read in the repository):
- **Poly Haven props fetched for the shop rooms** (tools/art-recipes/fetch_polyhaven.py): among them wooden_crate_01, cardboard_box_01, metal_jerrycan, oil_tin, cigarette_pack, tea_set_01, vintage_electric_kettle, vintage_radio_transceiver, standing_chalkboard_01, lifebuoy, life_jacket, ocean_buoy, lateral_sea_marker, rubber_boots, steel_frame_shelves_01, metal_tool_chest, many hand tools, office_notepads, stationery_supplies.
- **The scene file** (production/specs/vignette-scene.json) places a kiosk and a pillar box (both deliberately unlettered: canon), one guard-rail panel, two dustbins, lighting columns at 5 m spaced at four times their height, 34 pieces of litter and 60 of gum.
- **The label atlas** (tools/art-recipes/make_label_atlas.py): 8 × 4 tiles of invented 1990 packaging in OFL fonts.
- **Today's rulings:** the skip and the pallet stay off the street until made real; the cars are off; the kiosk stays.

**A small conflict to check [I].** The scene file's kiosk entry carries K6 proportions (0.914 m square, 2.515 m tall). The recipe draws a KX100 (its materials are named cl_kx100_*). A KX100 is about 0.89 m square and 2.19 m tall. Check which numbers the generator uses before the kiosk is re-materialled.

---

## 2. Family A: street furniture

### A1. How professional games make it

- **Few shapes, many conditions.** Studio furniture is a small kit of mid-poly parts (post, head, base, plate) on shared master materials. Variety comes from masks and per-instance data: paint fade, dirt from the ground up, rust streaks under fixings, chips, lean. KCD2 does this with one atlas and "HSL and blendmap variation" [READ earlier, CLOSE-RANGE]. Trim-sheet breakdowns report one artist texturing 30 models from 7 trim sheets, and trim sheets on 80% of a scene, with vertex paint and RGBA masks for variation [SS, source 18].
- **Placed by rule, then polished by hand.** Insomniac built Spider-Man's Manhattan with Houdini tools that placed ground, buildings, traffic, vignettes and props [SS, source 16; the GDC slides were UNREACHED]. Unreal 5.8's PCG has the same parts, documented [READ, source 15]:
  - Spline Sampler: "Samples points using the spline";
  - Static Mesh Spawner, with a weighted selector, a "By Attribute" selector, and material overrides per attribute;
  - Self Pruning: "Removes intersections between points";
  - Distance, Transform Points ("basic random rules"), Attribute Noise, Select Points, Match And Set Attributes.
- **Reference photography of the real place.** Forza Horizon 4's environment artists matched British locations side by side with photographs [SS, source 19].
- **Fictional marks on real forms.** GTA makes every brand up, with an in-house 2D design team (Stu Petri, vice-president of 2D/UI design) [SS, source 17]. Watch Dogs: Legion's London uses invented makes (period-vehicles note).
  - For us [I]: a period form such as a cylindrical pillar box or a stainless kiosk is fine to build. Its logo, crown, cypher and lettering are not. A KX100's design dates from 1985, so even a registered design (25 years at most) has lapsed (law section of aaa-street note 4).
- **Scans for surfaces, not for objects.** Studios scan the kerb, the drain and the asphalt, and model the furniture (aaa-street SUMMARY).

### A2. Free sources without AI restrictions

| Item | Source | Licence, exactly | AI tag or clause | Mark | Fit |
| --- | --- | --- | --- | --- | --- |
| Chain-link fence kit (posts, gate, panels) | Poly Haven `modular_chainlink_fence` | CC0 | none | [SS] | Yard and harbour fencing; check the posts read British |
| Weathered concrete barrier | Poly Haven `concrete_road_barrier_02` | CC0 | none | [SS] | Quay blocks at most; the shape may read American [I] |
| Oil drums, wooden crate | Poly Haven `Barrel_01`, `Barrel_02`, `wooden_crate_01` (held) | CC0 | none | [SS] | Yard and quay |
| Buoys, sea marker, lifebuoy | Poly Haven (held) | CC0 | none | [SS] | Quay edge |
| Ornate street lamp | Poly Haven `street_lamp_01` | CC0 | none | [SS] | Wrong: ornate cast iron |
| Materials: painted metal, rust, galvanised, concrete, timber, plastic | ambientCG | CC0 1.0 | none | [SS] | Every kit piece. The API was UNREACHED; pick by name on his PC |
| Iron mooring bollard and cleat (laser scans) | Gowanus Superfund site (Brooklyn), shown on Sketchfab | "free download"; licence field not seen | not seen | [SS] | Shape reference for quay ironwork; American canal |
| Lydney Harbour mooring bollard | Wessex Archaeology, Sketchfab | not seen; may not be downloadable | not seen | [SS] | British, the right kind of object. Read its licence and tags first |
| Mooring bollard | Lin14, Sketchfab | CC BY | not seen | [SS] | Off the allowlist for 3D |
| Yellow port bollard (Venice) | Blue Scans, Sketchfab Store | paid, "Royalty Free" | not seen | [SS] | Off the allowlist |
| Pillar boxes, K6 kiosks | Sketchfab | CC BY or CC BY-NC | not seen | [READ earlier, street-clutter] | Off the allowlist |
| KX100, Thorn Beta 5 column | SketchUp 3D Warehouse | 3D Warehouse's own licence | not seen | [SS earlier] | Dimensions only |
| Museum 3D | Smithsonian Open Access (2,200+ models on Sketchfab and 3d.si.edu) | CC0 | none stated | [SS, source 11] | Museum objects; no British street furniture found [I]. Its API was UNREACHED |
| Maritime 3D | Scottish Maritime Museum, 41 models | CC0 | not seen | [SS, source 12] | Vessels, a puffer's boiler, figureheads: for the harbour family, not furniture |
| Street props | Fab: Dekogon City Street Props, British City Pack, European Street Props | Fab Standard | not seen | [SS earlier, note 4] | Wrong period or country |
| Only if 0.1 is ruled (b) | Megascans drains, covers, kerb and asphalt materials | Fab Standard | `isAiForbidden: true` on the records checked | [READ earlier, GOODS] | |

**Plainly: nothing free fits as a finished piece of 1990 British furniture.** What is free is materials, a fence and a few quay objects. The furniture itself is ours.

### A3. The kit method for what we make

**The parts.**

| Kit | Parts | Builds |
| --- | --- | --- |
| Posts | tube (60 to 114 mm), tapered square concrete shaft, timber pole; base flange, root, collar, door plate; height as a parameter | lamp columns, sign posts, bus-stop pole, beacon posts, signal poles, telegraph poles |
| Heads | sodium lantern (lighting-column.py has one), Belisha globe with collar and cap, three-aspect signal head with backboard, bus flag, sign faces (circle, triangle, rectangle, supplementary plate) | everything mounted on a post |
| Bodies | lathe and box primitives with caps, rims, slots, hinges, lettering panels | pillar box, litter bins (pole-mounted open bin; free-standing hooded bin), grit bin, dustbin, 1,100-litre bin, bollards (cast-iron cannon, concrete, steel tube), mooring bollard, cleat |
| Linear (along a spline) | 2 m guard-rail panel (posts, rails, infill); two-rail tube railing with chain; chain-link (Poly Haven); kerb blocks of 915 mm with an upstand of 125 mm (the street's own standard), drop kerb, corner; quay edge with timber fender; overhead wire as a sagging curve | railings, fences, kerbs, quay edge, telegraph wires |
| Flat on the ground | cast covers (four patterns), the 0.40 m gully grate, zebra stripes and zigzags as decals | manholes, gratings, crossing |
| Assemblies | the KX100 (frame, panes, chest-height band, door, handle panel, payphone, roof slab); bus shelter (steel frame, glass panels, advert case, seat rail); bench (cast ends with timber slats; a concrete-and-timber council bench); telegraph pole (pole, crossarm, insulators, step bolts, drop wires to the houses) | the hero pieces |

**The variation.**
- **Shape:** two to four models per kind at most. Real councils fitted one design per street, so repeats of one bollard are true to life. Variety comes from age and condition, not from shape [I].
- **Seeds per instance:** lean of 1 to 3 degrees on poles and bollards; dents; paint fade; dirt height; rust amount; a missing or replaced part (a bin liner, a cap).
- **Swaps:** head type, plate set, base type, lid open or shut.
- **Materials:** one master material per substance (painted steel, galvanised steel, cast iron, concrete, timber, glass-fibre, glass). Masks from a curvature and occlusion bake per asset: edge chips to red-oxide primer, rust streaks down from fixings, grime from the ground up, rain streaks from the top.
- **Decals:** fly-posters, stickers, the five minted crew tags as graffiti, gum, bird droppings on caps.

**The tools.**
- **Blender 4.5 by Python**, as lighting-column.py and terrace-front.py already do: bmesh building from a dimension table; bevel plus weighted normals; UVs by script onto a shared trim sheet; a curvature and occlusion bake to one mask texture per asset; export with a JSON sidecar giving dimensions, the photographs it was checked against and the licence of every input.
- **Geometry Nodes** for the parametric kits (posts, railings, fences, kerbs), one node group per kit, its inputs set from Python [I].
- **Unreal PCG** for secondary and tertiary scatter along the kerb spline: Spline Sampler, then Transform Points, then Self Pruning, then a weighted Static Mesh Spawner with material overrides [READ, source 15].
- **The scene law still holds** ("every object arrives via that engine's generator reading THIS file", asset-packs note). PCG may scatter only from seeds and rules written in the scene file, not from hand placement [I].
- **Example rules:** lamps every four times the mounting height on alternate sides (already in the file); a bin within 3 m of each shop door and at the bus stop; bollards at corners and the quay edge; a name plate at each terrace end; gully grates at the low points of the camber.

**Where the agent works and where an eye must judge.**
- The agent writes the kits from dimension tables and builds the variants. It renders each piece in the game camera at 2,560 × 1,440, by day and at night. It checks every bounding box against the spec numerically, and it carries out the gate's first check against the photographs.
- **An eye must judge** three things:
  1. the silhouette at the game's distances;
  2. paint colour under overcast light;
  3. whether the wear reads as years of weather or as a pattern.

  That eye is my check and then a fresh reviewer. Under his rule, props are approved by the gate alone. Jafar sees them only in street frames.
- **Canon goes to Jafar:** the kiosk's operator mark and the pillar box's cypher (owed by the brand bible). Any council name on bins and grit bins is also new canon: none is minted. Until they are, unlettered is correct; generic words such as "LITTER", "GRIT" and "BUS STOP" carry no brand.
- **Lettering** must be set in OFL fonts. An OFL face close to the road signs' Transport and to Kindersley's street-name capitals was not found in this pass (unchecked).

### A4. The reference that sets the bar

Links only; proportions and period feel, never copied designs.
- **The earlier notes' leads stand:** the Maaraig KX100 in 1985 livery (Twentieth Century Society, 6 June 2024); Geograph's KX100 tag; the streetlightonline Beta 5 pages; Commons "Belisha beacons"; Beauty of Transport on bus flags (2016) and street-name lettering (2021); PostboxMap's identification guide (street-clutter-1990).
- **Pelican crossings** (in case the street has signals) [READ, source 20]:
  - introduced in 1969;
  - "two poles on either side of the road, each containing three signal heads (one in each direction for drivers and one facing pedestrians)";
  - flashing amber while the green man flashes; a call button;
  - zigzag markings at pelicans from 1989, after the 1987 regulations;
  - an audible bleep and a tactile cone are "normally present" today. Whether they were there in 1990 is uncertain, so leave the cone off.
- **Bus shelters:**
  - Adshel supplied shelters free to councils in exchange for advertising, from the 1960s [SS, source 22].
  - Flickr's "The Pre-Adshel British Bus Shelters" pool and Beauty of Transport's "Vernacular Spectacular" (17 May 2017) show council-built shelters [SS, source 22].
  - [I] A 1990 port town plausibly has both. Any advert in a shelter is invented, with no alcohol and no children.
- **Litter bins:** Glasdon's "Topsy 65" marks 65 years in 2024, which puts the hooded glass-fibre bin's design at about 1959 [SS, source 23]. So a hooded glass-fibre bin is period-plausible in 1990. Build a generic hooded bin, not the Topsy's exact form [I].
- **Quay ironwork:**
  - North Shields Fish Quay: the Tyne and Wear Historic Environment Record describes its conservation area and a "dolphin mooring post"; search summaries say the quay keeps "a variety of mooring bollards along the quay edge" [SS, source 21].
  - The quay "declined in the 1980s as a result of problems in the fishing industry" [READ, source 21].
  - Marshall's River Hull photograph (R08 in photographs.md) shows a "chain-edged quay".
- **Archives:** the Historic England Archive holds more than 1.6 million photographs from the 1850s on, but its "Picturing High Streets" collection is of the 2020s, not the period [SS, source 26]. Search it by place and date from his PC. Geograph (CC BY-SA, mostly 2005 on) is good for shape, weak for period.
- **The bar itself:**
  - The Hook sheet: its foreground column is slender and dark, with a small flat canopy (lighting-column.py records that crop).
  - The KCD2 arcades frame: the density of objects, and the dirt and wear on every one.

### A5. The variety the town needs, and the one proof

| Kind | Models | Variants (materials and wear) | On Quay Street (42 m) [I] |
| --- | --- | --- | --- |
| Lamp column and lantern | 1 (steel, as the Hook sheet) | 3 | 4 |
| Bollards (cannon, concrete, steel) | 3 | 3 each | 6 to 10 |
| Litter bins | 2 | 3 | 2 to 3 |
| Galvanised dustbin; 1,100-litre bin | 1; 1 | 4 (dents, lid off); 2 | 4 to 8 in the yard; 1 to 2 |
| KX100 kiosk; pillar box | 1; 1 | 2; 2 | 1; 1 |
| Bus stop flag and pole; shelter | 1; 1 | 2; 2 | 1; 0 to 1 |
| Bench | 2 | 2 | 1 to 2 (the quay) |
| Guard railing; quay railing with chain; fences | 1 kit; 1 kit; 2 (chain-link, palisade) | per panel | 1 to 3 panels; along the quay; the yard |
| Name plates; road signs | 1 kit; about 6 faces | names as decals | 2 to 4; 3 to 6 |
| Belisha beacons and zebra (if there is a crossing) | 1 | 2 | 1 crossing |
| Grit bin | 1 | 2 | 1 (on the hill) |
| Telegraph poles and wires | 1 kit | 3 | 2 to 3 |
| Covers and gratings | 4 covers, 1 grate | 3 | 10 to 15 |
| Kerbs | granite and concrete, drop and corner | wear per block | the whole street |
| Mooring bollards and cleats | 2 and 1 | 3 | along the quay |

About 25 kinds and 30 models, each with two to four material states. That is enough for the street, the quay and the hill, because the shapes repeat in life too [I].

**The one proof: the kerbside run.**
- **What:** one stretch of about 10 m of the pavement nearest the hook camera, all from the kit, with wear, placed by the generator:
  - the existing lamp column;
  - the KX100, re-materialled: brushed stainless, glass with grime, the band, the handle panel, the payphone;
  - the pillar box;
  - two bollards and a litter bin;
  - the railing panel, kerbs, a gully grate and a cover;
  - a name plate, plus the street's litter and gum.
- **How it is judged:**
  - in the game camera at 2,560 × 1,440, wet day and night, side by side with the Hook sheet (the column, the kerb, the wet pavement) and the KCD2 arcades frame (material richness, dirt, density);
  - each piece against its period photograph (Maaraig, PostboxMap, Beta 5);
  - then a fresh reviewer.
- **When:** this is the furniture half of proof-frame item 8. It waits its turn in the ordered list.
- **Effort [I]:** 4 to 6 days. The kiosk's materials take 1 to 2 (period-vehicles note); the pillar box 1; bollards, bin, plates and covers 1 to 2; the master materials and wear 1; placing and judging 1.

---

## 3. Family B: shop goods and props

### B1. How professional games make it

- **Hard props** (crates, boxes, pallets, skips, bins, A-boards) are kit-modelled mid-poly on trim sheets and master materials with masks. That is the same method as the furniture and the cars (period-vehicles note), and the trim-sheet practice of source 18 [SS].
- **Printed things** are simple meshes. The effort goes on the graphics:
  - Naughty Dog outsourced "signs, branding, and unique assets" into a tagged library [READ earlier, GOODS];
  - Rockstar's brands come from an in-house 2D team [SS, source 17];
  - for us, our own generated graphics (make_label_atlas.py), all invented.
- **Soft things** (bags, nets, tarpaulins, sacks) are simulated once, then baked into a few static shapes, then instanced [I; common practice, no source read in this pass].
- **Piles** are a few distinct pieces with per-instance variation. They are never one copy (GOODS).
- **Scanned hero props** are kept for the few things seen at 1 m that carry history: a crate, a drum, a tool. KCD2 credits its produce to scans [READ earlier, CLOSE-RANGE].

### B2. Free sources without AI restrictions

| Item | Source | Licence | AI tag or clause | Mark | Fit |
| --- | --- | --- | --- | --- | --- |
| Grey double-pedestal metal office desk | Poly Haven `metal_office_desk` | CC0 | none | [SS] | The cab office: "worn grey finish, dual pedestal drawers… mid-century" |
| Clamp desk lamp | Poly Haven `desk_lamp_arm_01` | CC0 | none | [SS] | The cab office |
| Radio, kettle, tea set, notepads, stationery, files | Poly Haven (held) | CC0 | none | [SS] | The cab office and tea room; check `vintage_radio_transceiver` against a period base set [I] |
| Chalk A-board | Poly Haven `standing_chalkboard_01` (held) | CC0 | none | [SS] | The café's menu board |
| Crates, drums, jerrycan, cardboard box | Poly Haven (held) | CC0 | none | [SS] | Yard, quay, back stock |
| Tools, buoys, lifebuoy, life jacket, boots | Poly Haven (held) | CC0 | none | [SS] | Ironmonger and chandler |
| Cigarette pack | Poly Haven `cigarette_pack` (held) | CC0 | none | [SS] | Tobacco is allowed; check it carries no real brand |
| Rope, rough wood, cardboard, paper, plastic, fabric textures | ambientCG | CC0 1.0 | none | [SS] | All our own containers, ropes and papers |
| Maritime objects | Scottish Maritime Museum | CC0 | not seen | [SS, source 12] | Few chandlery-sized objects listed; check |
| Pallets, rope coils, paint and oil cans, junkyard pack, cardboard boxes | Megascans on Fab | Fab Standard, price 0 | `isAiForbidden: true` on the records checked | [READ earlier, GOODS and period-vehicles] | **Only if 0.1 is ruled (b)** |
| Construction props | Dekogon Construction Vol. 1, Fab (free) | Fab Standard | not seen | [SS earlier] | American |
| UK skip | BlenderKit "Industrial Skip" | BlenderKit Royalty Free | not seen | [SS earlier] | Off the allowlist |
| UK skip | Sketchfab "Old Rubbish Skip", Fab "Dirty Rusty Skip" | CC BY | not seen | [SS earlier] | Off the allowlist |
| Fish boxes, milk crates, bin bags, newspaper bundles, A-boards, British litter | none found on any allowlisted source | | | [I] | Ours |

### B3. The kit method for what we make

**The parts.**

| Kit | Parts | Builds |
| --- | --- | --- |
| Timber containers | rough-sawn board (trim sheet: grain, paint, stencil), cleat, corner post, nails; length, width, height and board count as parameters | wooden fish boxes, market crates, slatted fruit and tomato trays, the UK pallet (1,200 × 1,000 mm, nine blocks or three stringers) |
| Moulded plastic | box with inset ribs, drain holes (Geometry Nodes array), handles, stacking lugs, a stencilled owner's name from an atlas | plastic fish boxes ("kits"), milk crates, trays |
| Steel containers | tapered plates, lugs, chain hooks, a hire name from an atlas | the 6-yard skip (about 2.6 × 1.5 × 1.2 m), the 1,100-litre bin, dustbins (furniture kit) |
| Soft goods | cloth simulation in Blender, run once, baked to four to six static shapes per kind | black bin bags, hessian sacks, tarpaulins, fishing nets (a knotted mesh draped over a pile, with floats and weights) |
| Rope | a curve with a three-strand twisted profile and ambientCG rope textures (the GOODS method) | coils, rope along the quay, mooring lines |
| Paper | thin slabs with real thickness, string ties, generated pages (GOODS) | newspaper bundles at the newsagent's door, the A-board's headline bill, posters, bus tickets |
| Litter | tiny meshes from an atlas | cigarette ends (bent, filter colours), crisp packets, sweet wrappers, chip papers, polystyrene trays, soft-drink cans and 2-litre pop bottles (invented makes; never beer), leaves |
| Cab office | Poly Haven desk and lamp; our own radio base set and desk microphone (generic form, Pye Tulip as shape reference only); a generic 1980s push-button phone with a curly cord; a ledger and the book of fares (cloth-covered boxes with page edges); a generic electric typewriter, no make; a drivers' board (pegboard with numbered tags); the wall map; ashtrays; mugs | the one room |
| Household | milk bottles on steps, door mats, net curtains, plant pots, a washing line | terraces and the yard |

- **The wall map** can be drawn by script from the town's own data: an invented map of Meridian, no Ordnance Survey tracing [I].
- **Canon is owed** for the local paper's name, which appears on the A-board and the bundles. The brand bible still owes it (canon.md, Brands and law). Until then, a headline bill without a masthead is canon-safe [I].

**The variation.**
- Dimensions within the real ranges.
- Board count and gaps.
- Paint and plastic colours from a period palette.
- Stencils and hire names from an atlas of invented merchants (for example a Meridian fish merchant's initials).
- Wear masks; wetness; fish scales and ice melt on fish boxes.
- Fill states: empty, iced, full.
- Stacking rules: three to eight high, offsets of ±2 cm, turns of ±3 degrees, an occasional box turned askew.
- Bin bags are split, tied or knotted; there are more of them on bin day.

**The tools.**
- Blender Python with Geometry Nodes for the parametric kits.
- Rigid-body drops by script for piles and stacks, merged into one mesh per pile (as GOODS does for the sweets).
- Cloth simulation baked to static meshes.
- make_label_atlas.py, extended into atlases for stencils, mastheads and litter.
- In Unreal: instanced meshes with per-instance custom data for the atlas tile; PCG scatter for litter and cigarette ends, weighted to doorways, the kerb and the bus stop, seeded from the scene file.

**Where the agent works and where an eye must judge.**
- The agent builds, places and renders.
- An eye judges four things:
  1. whether a stack reads as fish boxes at 3 m;
  2. whether the plastic colours are of the period;
  3. whether bags read as polythene, not stone (the third review of 2 October read the skip as "a granite box");
  4. whether the invented graphics feel like 1990. That is typography and print quality, and it is subtle.
- **Content checks on every graphic and prop:**
  - no beer cans, bottles or crates;
  - no betting slips, pools coupons, scratchcards or fruit machines (fruit machines stood in many chip shops and cafés: leave them out);
  - no toys, prams, school bags or children's clothes on washing lines;
  - tobacco is allowed.
- **On milk crates [I]:** the street-clutter note excluded "beer or milk crates". Milk is not alcohol, so milk crates and bottles are within canon. The exclusion seems to have been over-cautious.

### B4. The reference that sets the bar

- **Fish boxes:**
  - plastic boxes are known to fishermen as "kits";
  - one supplier's page mentions "old style wooden fish boxes from the 70's & 80's";
  - PPS East supplies a returnable box pool at Grimsby [SS, source 24].
  - So both kinds were plausibly in use in 1990. **Let a photograph decide** before building: Steve Thornton's "Fish Town", Grimsby docks, 1990 (FISHMONGER note, link 5).
- **Skip and pallets:** the sizes above (period-vehicles note); Geograph skip photographs for shape.
- **The cab office:**
  - BT Viscount (MoDiP) and the Pye Tulip (Science Museum Group): forms only;
  - Pinter's controller alone at a microphone, Minder's office swamped by phones (cab-office note).
- **The working quay:** Marshall R08; Homer Sykes, Hastings, c.1985, fishermen's huts with price boards (FISHMONGER note).
- **Shopfronts and stacked goods:** Marshall R05, "stacked goods" (photographs.md). Sainsbury Archive's JS Journal of 1989 is a link for research only, never a source of packaging (NC/ND).
- **Milk [I, unverified]:** glass pint bottles with coloured foil caps, delivered to the doorstep; plastic crates by 1990. Check the cap colours against a dated photograph before making labels.
- **The bar:** the KCD2 arcades frame's 40 or more objects, each worn and each sitting on the ground with a contact shadow; the Hook sheet's doorways.

### B5. The variety the town needs, and the one proof

| Group | Kinds | Variants | Why |
| --- | --- | --- | --- |
| Containers | about 12 (wooden and plastic fish boxes, market crate, fruit tray, pallet, milk crate, three cardboard boxes, sack, drum, jerrycan) | 2 to 4 each, plus fill states | doorways, the yard, the quay; stacks of one kind are true to life, so the variety lives in stencils, dirt and fill |
| Soft goods | 4 (bin bags, sacks, tarpaulins, nets) | 4 to 6 baked shapes each | bin day, the quay; a single shape repeated reads at once |
| Paper | 5 (bundles, A-board bill, posters, tickets, chip papers) | atlas tiles | the newsagent, the bus stop, the gutter |
| Litter | about 10 kinds | hundreds of instances | the scene file already scatters 34; KCD2 density asks for more at doorways and gutters |
| Cab office | about 15 distinct props | one each | one room, seen up close |
| Chandlery and ironmongery | about 30, mostly held from Poly Haven | | two shop rooms |
| Household | about 10 | | terraces and the yard |

**The one proof: the fishmonger's pavement.**
- **What:** at east_parade bay 1, the most visible shop from the hook view (ruling of 3 October):
  - a stack of fish boxes (wooden or plastic as the Grimsby photograph shows), one with ice and fish;
  - a pallet with boxes on it;
  - two bin bags;
  - a milk crate with bottles at the next door;
  - the newsagent's A-board;
  - cigarette ends and litter in the gutter.

  All from the kits, placed by the generator.
- **How it is judged:** in the hook camera and at 1 to 3 m, wet, by day; side by side with the Hook sheet's doorways and the KCD2 arcades frame; then a fresh reviewer. If a bag or a box reads as stone, that is the method failing, not the material: ask why before tuning.
- **Effort [I]:** 3 to 4 days: the timber and plastic kits 1.5; the bags 0.5; the paper and litter atlases 0.5 to 1; placing and judging 1.

---

## 4. Family C: food

### C1. How professional games make it

The GOODS note covers this.
- Photoreal games scan food: Final Fantasy XV cooked and scanned its dishes; Resident Evil 7 used photogrammetry for over half its assets, meat included.
- Hand-painted food is the stylised route.
- KCD2's produce starts from modified scans.

Two additions [I]:
- **Prepared food is a composition of simple parts.** Chips are an instanced chip shape; a fish supper is a battered fillet, chips and peas on a sheet of paper. The surface carries it: subsurface, a grease sheen, a little steam at most.
- **Wet and fresh is a material property.** Fish and fruit read as real through roughness, specular and subsurface under the window light, more than through triangles.

### C2. Free sources without AI restrictions

| Goods | Source | Licence | AI tag or clause | Mark | Note |
| --- | --- | --- | --- | --- | --- |
| Apples, bananas, lemons, onions; carrot cake, chocolate cake, croissant, buns; tea set | Poly Haven | CC0 | none | [READ earlier, GOODS; SS today] | The safest food source |
| Cod, mackerel ×3, herring, flatfish ×4, crabs ×3, prawns ×2; apples ×2, pear, satsumas ×2, lemon, cabbage, potato | Sketchfab, ffishAsia-and-floraZia | "CC0 Public Domain"; each description says "License: CC0" | **NoAI tag unknown: read each record's tags** | [READ earlier, GOODS; SS today, source 10] | 0.5 to 2.9 million triangles each; decimate and bake |
| Japanese Sea Fish Pack, Japanese River Fish Pack | Fab | a search summary says CC BY 4.0 | not seen | [SS, source 10] | If CC BY, off the allowlist; not needed |
| Multi Grain Bread | Sketchfab, plaggy | titled "CC0"; licence field not seen | not seen | [SS, source 14] | The same author's "CC0 – Jar" is CC BY in its licence field (GOODS), so read the field |
| Baked goods (4 breads, 4 rolls, 4 pastries) | Sketchfab, Rigsters | not seen | not seen | [SS, source 14] | Check |
| Homemade Bread RAWscan | Sketchfab, Spogna | not seen | not seen | [SS, source 14] | Check |
| Ice, snow, candy stripes | ambientCG | CC0 1.0 | none | [READ earlier, GOODS] | Crushed ice bed; humbugs |
| Natural-history specimens | Smithsonian | CC0 | none stated | [SS, source 11] | Preserved specimens, not market food [I] |
| Breads, pork pies, tea cake, muffin, smoked fish, fruit, veg, Bazaar stalls | Megascans on Fab | Fab Standard, price 0 | `isAiForbidden: true` on the records checked | [READ earlier, GOODS] | **Only if 0.1 is ruled (b)** |
| NOAA fish photographs | NOAA | US public domain, credit asked | none | [READ earlier, GOODS] | Not on the allowlist by name; not needed |

**Without Megascans, the gaps grow:** bread, pies, tea cakes, muffins, cabbage, carrots and grapes. Bread and pies would come from a checked Sketchfab CC0 scan or be made. Cabbage and potato come from ffishAsia. Carrots, grapes and pies must be made [I].

### C3. The kit method for what we make

The GOODS note's section 4 stands for: whole fish on ice, crushed ice, fillets, kippers, dressed crab, prawns, sweets in jars, chocolate boxes, scones and tomatoes. Additions:

- **The display kit.** Each piece is a few hundred triangles from dimensions:
  - white plastic and enamel trays; the tilted white slab; plastic grass (weakly sourced);
  - slatted greengrocer's crates lined with paper; wicker baskets; baker's trays;
  - the cake stand and glass dome for the tea room (the dome faked, as the GOODS jars are);
  - price tickets: hand-lettered cards per pound, at ONS prices (cod about £2.60 a pound).
- **The pile generator.** One Blender script for all heaped goods: three to six source pieces per kind, dropped by rigid body into a tray or crate, with scale ±10%, a tint and a turn per piece, then merged per container. The same script lays fish in rows (roll and sink), prawns (40 to 80) and sweets.
- **Prepared food** for the chip shop or takeaway and the tea room [I]:
  - **Chips:** four to six chip shapes (about 1 cm square, 5 to 8 cm long), golden subsurface and a fat sheen, piled by the generator.
  - **Battered fish:** a fillet outline displaced into a batter crust with noise.
  - **Mushy peas:** a displaced green mound.
  - **Wrapping:** a sheet of paper draped by cloth simulation, baked; a polystyrene tray; a wooden chip fork.
  - **Chinese takeaway:** foil containers with card lids.
  - **Pies, pasties, sausage rolls:** reshaped from bread scans, or made.
  - **Sandwiches:** slices from a bread scan.
  - **Tea room:** scones (GOODS), toast, a sponge from Poly Haven's cakes, and the tea set (held).
- **Materials.** Subsurface for fish flesh, fruit and batter. Roughness 0.15 to 0.25 on wet fish skin (GOODS). A grease sheen on fried food. Faked glass only behind the shop window.
- **Content.** No wine, beer or spirits in any shop, menu or window. Drinks are tea, coffee, milk and invented pop. No children on any packet. No fruit machine in the chip shop.
- **The agent and the eye.** Food is where "toy" shows first. Every food piece is judged at 1 m in the game's light by my check, then a fresh reviewer. One try for each hard case, then set aside (GOODS).

### C4. The reference that sets the bar

- **Fishmonger:** the FISHMONGER note's dated photographs (Picture Sheffield t13140 and t13138, c.1989 and 25 August 1990; Marshall, Brixton, 1987; Thornton, Grimsby, 1990), the ONS cod price, and prices per pound.
- **Fish and chips:**
  - Newspaper wrapping against the food "largely ended in the 1980s".
  - A greaseproof inner layer was required between food and newsprint [SS, source 25; the sources are popular articles and the legal date is unconfirmed].
  - [I] For 1990: white paper against the food, with plain or newspaper outer sheets possible. Check against a dated photograph before a newspaper outer appears. Any outer newspaper is our invented paper, whose name is owed by the brand bible.
- **Greengrocer:** Marshall R05, "stacked goods" (photographs.md); price tickets per pound.
- **Tea room:** no dated photograph was found in this pass (a hole). Leads: Picture Sheffield, and the Historic England Archive searched by place.
- **The bar:** Rita's window, approved on 2 October ("the best thing on the page"); the Hook sheet; KCD2's market goods at close range.

### C5. The variety the town needs, and the one proof

| Group | Kinds | Distinct pieces per kind | Where |
| --- | --- | --- | --- |
| Fish and shellfish | about 9 (cod, haddock by recolouring cod, plaice, mackerel, herring and kippers, smoked haddock, crab, prawns, fillets) | 1 to 3 scans; fillets and crab made | fishmonger |
| Fruit and veg | about 14 (two kinds of apple, pears, oranges, bananas, lemons, potatoes, onions, carrots, cabbage, tomatoes, grapes, cauliflower, sprouts) | 3 to 6 per pile | grocer |
| Baking | about 8 (loaves, rolls, scones, tea cakes, pies, pasties, sausage rolls, cakes) | 2 to 4 | tea room, grocer |
| Tea room | about 6 dishes | 1 to 2 | tea room |
| Takeaway | about 6 | chips by generator | chip shop, if the street has one; litter |
| Sweets | about 5 | made | newsagent |

Why: each window is seen at 1 to 3 m, where one repeated piece shows at once. The GOODS rule of three to six distinct pieces per pile sets the counts.

**The one proof: the fishmonger's slab.** It is the next shop after Rita's (ruling of 3 October), so it is already due.
- **What:** whole fish on a crushed-ice bed (decimated ffishAsia scans, tags checked), a heap of prawns, one dressed crab, hand-lettered price tickets and white trays.
- **How it is judged:**
  - at 1 to 3 m and from the hook view, in the game camera at 2,560 × 1,440, by day and lit at night;
  - beside Rita's approved window, the Hook sheet, the KCD2 frames and Picture Sheffield t13140;
  - then a fresh reviewer;
  - then whole street frames to Jafar, as his rule on shopfronts asks.
- **Effort [I]:** 3 to 4 days: downloading, checking, decimating and baking the scans 1; the ice 1; layout, tickets and materials 1; the gate 0.5 to 1.

---

## 5. Per family, in one line

- **A, street furniture:** free are materials (Poly Haven, ambientCG), a chain-link fence and a few quay objects; we make every piece of furniture as kits with wear; impossible without a ruling are the kiosk's operator mark and the pillar box's cypher (canon), a council name (canon), and any Megascans surface (0.1).
- **B, shop goods and props:** free are Poly Haven's held crates, drums, tools, buoys, kettle, tea set, chalk board and the office desk; we make the containers, the skip, bags, nets, rope, papers, litter and the cab office's radio, phones, ledgers and board; impossible without a ruling are the Megascans pallets, rope and junk (0.1), CC BY or Royalty Free skips (licence), and the local paper's name (canon).
- **C, food:** free are Poly Haven fruit and cakes and the ffishAsia CC0 scans (each one's tags checked); we make the ice, fillets, kippers, dressed crab, the pile generator, takeaway food, scones, pies, carrots and grapes; impossible without a ruling are the Megascans food (0.1), CC BY fish packs and NOAA photographs (licence).

## 6. What I could not reach or verify

- **The Megascans NoAI field.** Fab was refused, so I could not confirm `isAiForbidden` on the items in his library. The finding rests on the GOODS note's reading from his PC. Check it there.
- **Sketchfab NoAI tags** on the ffishAsia scans, Gowanus, Wessex Archaeology and the bread scans, and their licence fields. Sketchfab's API was refused (403).
- **Poly Haven's and ambientCG's catalogues.** Both APIs were refused. Items are named from search summaries and the project's own fetch list.
- **Smithsonian Open Access item by item.** Its APIs were refused.
- **Spider-Man's GDC slides** and the AI and Games article on them: refused. Only summaries were seen.
- **Period facts left unverified:**
  - wooden against plastic fish boxes in 1990;
  - milk bottle cap colours;
  - the newspaper-wrapping rule's date;
  - whether pelicans had tactile cones in 1990;
  - the height and form of British cast-iron mooring bollards;
  - telegraph pole heights;
  - OFL fonts near Transport and Kindersley.
- **No dated 1985 to 1995 photograph** was found for a tea room, a chip shop interior, a ship chandler's or a council litter bin.

## 7. Sources

All accessed 3 October 2026.

1. Epic, "Licenses and Pricing in Fab", undated. https://dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab [READ]
2. Fab support, "Introducing NoAI meta tags and Created with AI self-declaration", undated. https://support.fab.com/s/article/Introducing-NoAI-meta-tags-and-Created-with-AI-self-declaration?language=en_US [SS]
3. Fab listing record, Smoked Fish. https://www.fab.com/i/listings/e0b85907-6447-4538-a4b7-6bd2a82d3e22 UNREACHED (egress blocked)
4. Sketchfab, "Restricting Generative AI Use of Free Models", undated. https://sketchfab.com/blogs/community/restricting-generative-ai-use-of-free-models/ [SS]
5. Sketchfab, "Introducing the NoAI and CreatedWithAI tags". https://sketchfab.com/blogs/community/introducing-the-noai-createdwithai-tags/ ; CG Channel, February 2023. https://www.cgchannel.com/2023/02/sketchfab-introduces-noai-and-createdwithai-tags/ [SS]
6. Game Developer, "Epic sells ArtStation and Sketchfab to KitBash", August 2026. https://www.gamedeveloper.com/business/epics-sells-artstation-and-sketchfab-to-kitbash ; Game World Observer, 11 August 2026. https://gameworldobserver.com/2026/08/11/epic-games-has-sold-artstation-and-sketchfab [SS]
7. Poly Haven, "AI and Poly Haven", undated. https://blog.polyhaven.com/ai-and-poly-haven/ ; API page, https://polyhaven.com/our-api ; licence, https://polyhaven.com/license [SS]. The API at api.polyhaven.com was UNREACHED (403).
8. ambientCG, "License", undated. https://docs.ambientcg.com/license/ [SS]. The API at ambientcg.com was UNREACHED (403).
9. Poly Haven model pages, undated: https://polyhaven.com/a/metal_office_desk , https://polyhaven.com/a/desk_lamp_arm_01 , https://polyhaven.com/a/modular_chainlink_fence , https://polyhaven.com/a/concrete_road_barrier_02 , https://polyhaven.com/a/wooden_crate_01 , https://polyhaven.com/a/Barrel_02 ; categories https://polyhaven.com/models/office-stationery , https://polyhaven.com/models/industrial/props , https://polyhaven.com/models/containers-storage [SS]
10. ffishAsia-and-floraZia on Sketchfab, for example https://sketchfab.com/3d-models/cc0-striped-sole-zebrias-zebrinus-263f887e0c3f4649ad9764603cb4f95e ; Fab "Japanese Sea Fish Pack", https://www.fab.com/listings/f8d3000f-5418-4499-bdbb-8009a19319df ; "Japanese River Fish Pack", https://www.fab.com/listings/560eafd1-c315-436e-b750-351727c1beda [SS]. The Sketchfab API was UNREACHED (403).
11. Smithsonian Open Access, https://www.si.edu/openaccess/updates/21st-century-diffusion ; CG Channel, March 2020, https://www.cgchannel.com/2020/03/get-2000-free-3d-models-from-the-smithsonian-collection/ ; https://sketchfab.com/Smithsonian [SS]. 3d-api.si.edu and api.si.edu were UNREACHED (403).
12. Scottish Maritime Museum CC0 collection, https://sketchfab.com/ScottishMaritimeMuseum/collections/scottish-maritime-museum-cc0-b367fa03fcea40279a5470eea7872709 ; Go Industrial, "Scanning the Horizon", https://www.goindustrial.co.uk/our-blog/blog-post/scanning-the-horizon [SS]
13. Gowanus Superfund 3D models, https://gowanussuperfund.com/3d-models/ ; Wessex Archaeology, "Lydney Harbour mooring bollard", https://sketchfab.com/3d-models/lydney-harbour-mooring-bollard-daa6ae33220b4f4c8181911e1713f9b6 ; Lin14, https://sketchfab.com/3d-models/bollard-mooring-dd4a62e0ddb74a48abbd4e982541a671 ; Blue Scans, https://sketchfab.com/3d-models/yellow-mooring-port-bollard-photogrammetry-4ae3cea6d4e34a07bd0fd408a6d2c185 [SS]
14. plaggy, "CC0 – Multi Grain Bread", https://sketchfab.com/3d-models/cc0-multi-grain-bread-c03ae9c6b4014506bb98193cc85d11bd ; Rigsters, "Baked goods", https://sketchfab.com/3d-models/baked-goods-d1ae09e3cb8343bc8790b15928452906 ; Spogna, "Homemade Bread RAWscan", https://sketchfab.com/3d-models/homemade-bread-rawscan-f95a2e18d8454902a779360306d680c5 [SS]
15. Epic, "Procedural Content Generation Framework Node Reference" (UE 5.8), undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine [READ]
16. David Santiago, "Procedurally Crafting Manhattan for Marvel's Spider-Man", GDC, March 2019, https://media.gdcvault.com/gdc2019/presentations/santiago_david_procedurally_crafting_manhattan.pdf UNREACHED; summary at cgrecord.net, April 2019, https://www.cgrecord.net/2019/04/how-houdini-was-used-to-create.html [SS]; https://www.aiandgames.com/p/how-manhattan-is-built-using-procedural UNREACHED
17. gta.guide, "Rockstar Reveals New GTA VI Details in Dazed Interview", undated, https://gta.guide/article/rockstar-dazed-interview ; SVG, "The Real Reason GTA Makes Up Its Own Products", undated, https://www.svg.com/867642/the-real-reason-gta-makes-up-its-own-products/ [SS]
18. 80.lv, "Kaer Morhen: Trim Sheets & Interior Lighting in UE4", https://80.lv/articles/kaer-morhen-trim-sheets-interior-lighting-in-ue4 ; "The Workflow Behind an Abandoned Bar Modular Environment", https://80.lv/articles/the-workflow-behind-an-abandoned-bar-modular-environment ; both undated [SS]
19. PCGamesN, "Forza Horizon 4 environment artist shows off real life inspiration", 2018, https://www.pcgamesn.com/forza-horizon-4/forza-horizon-4-environment-artist-shows-off-real-life-inspiration ; Vincent Moubeche, "Watch Dogs Legion: Random London Environment", https://www.artstation.com/artwork/w69aew [SS]
20. Wikipedia, "Pelican crossing". https://en.wikipedia.org/wiki/Pelican_crossing [READ]
21. Wikipedia, "North Shields Fish Quay", https://en.wikipedia.org/wiki/North_Shields_Fish_Quay [READ]; Tyne and Wear HER, "Fish Quay Conservation Area", https://www.twsitelines.info/smr/11867 , and "Fish Quay, Dolphin Mooring Post", https://sitelines.newcastle.gov.uk/SMR/10897 ; Geograph, "North Shields" tag, https://www.geograph.org.uk/tagged/North+Shields [SS]
22. Flickr, "The Pre-Adshel British Bus Shelters" pool, https://www.flickr.com/groups/1392763@N25/ ; The Beauty of Transport, "Vernacular Spectacular", 17 May 2017, https://thebeautyoftransport.com/2017/05/17/vernacular-spectacular-bus-shelters-which-break-the-mould/ ; Prepressure, "Adshel", https://www.prepressure.com/printing/products/adshel [SS]
23. Glasdon UK, litter bins, https://uk.glasdon.com/litter-bins ; "Topsy 65" retail listing, https://www.amazon.co.uk/Glasdon-TopsyTM-Outdoor-Litter-Weather-resistant/dp/B0DDXVD9B6 [SS]
24. World Fishing, "PPS East fish boxes for Grimsby", undated, https://www.worldfishing.net/pps-east-fish-boxes-for-grimsby/128963.article ; PPS Equipment blog, August 2012, http://blog.ppsequipment.co.uk/2012/08/plastic-fish-boxes-for-sale.html [SS]
25. The Takeout, "Why Old-School Fish And Chips Were Wrapped In Newspaper", undated, https://www.thetakeout.com/2175905/why-old-school-fish-chips-wrapped-newspaper/ ; paper-world.com, https://www.paper-world.com/en/newsdetail/fish-und-chips-in-newspaper [SS]
26. Historic England, "Photographs" collections, https://historicengland.org.uk/images-books/archive/collections/photographs/ ; "Picturing High Streets", https://historicengland.org.uk/images-books/archive/collections/photographs/picturing-high-streets/ [SS]
27. Fab, "Quixel to Fab Transition FAQs", https://support.fab.com/s/article/Fab-Transition-FAQs?language=en_US ; CG Channel, October 2024, https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/ [SS]
28. Project files, read in the repository:
    - CLAUDE.md, canon.md (Brands and law), DECISIONS.md (last forty lines);
    - production/research/street-clutter-1990/SUMMARY-2026-09-29.md, period-vehicles-and-props/NOTE.md, aaa-street/SUMMARY.md and 4-VEHICLES-AND-FURNITURE.md and 5-PROOF-FRAME.md (in part);
    - shop-window-interiors/GOODS-2026-10-03.md, FISHMONGER-2026-10-03.md and CLOSE-RANGE-2026-10-03.md;
    - cab-office-interior-1990/NOTE-2026-09-30.md (in part), asset-packs/SUMMARY.md, asset-coverage/SUMMARY.md;
    - production/specs/fab-free-megascans.md, production/specs/vignette-scene.json (furniture, scatter, held props);
    - production/art/clothing/SCREENING-2026-10-02.md;
    - production/reference/photographs.md and README.md;
    - tools/art-recipes/fetch_polyhaven.py, make_label_atlas.py, lighting-column.py (header) and terrace-front.py (kiosk lines).
