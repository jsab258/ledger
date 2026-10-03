# Vegetation, the hillside and the distant town (asset-plan note 5, 3 October 2026)

Research helper. About thirty minutes, reading only. I used 25 web searches. Marks: **[READ]** read at the source; **[SS]** search summary only; **[I]** my inference; **UNREACHED** the page refused me. An unreached source is not evidence.

## Three findings that change the plan

1. **The AI field on Epic's own plants may rule them out.** Search summaries of several Megaplants listings on Fab report "Allows usage with AI: No" [SS, 9]. I could not open Fab to confirm (UNREACHED). Epic does tag some of its own content NoAI: our natural-idles note read that flag on the Game Animation Sample's own listing [13]. So treat Megaplants as **excluded** until the owner, signed in, reads "Allows usage with AI: Yes" on each listing. A summary of a Megascans listing (Asphalt Road) named the same field but gave no reliable value [SS, 10].
   - **Outside my families, but urgent:** the same check is owed on the 18 Megascans already in his library for the street (production/specs/fab-free-megascans.md) and on the Game Animation Sample. Under the brief's rule, which says "not even as references", any of them reading "No" cannot be used.
2. **The CC0 libraries cover vegetation's raw inputs.**
   - Poly Haven has scanned plants: nettle, dandelion, a weed clump, a grass tuft, four shrubs, a small tree, two windswept coastal trees and a mossy stump [SS, 14, 15].
   - ambientCG has scanned leaf atlases, including ivy and dandelion [SS, 16].
   - Blender's own Sapling Tree Gen and IvyGen turn those leaves into our own trees and ivy [READ, 18].
   - Nothing in this route needs a ruling.
3. **The hill is close, so it cannot be a painted card.** In the hook camera (about 64 degrees across 2,560 pixels, from 1-PIPELINE.md), one pixel covers about 4.8 cm at 110 m and 9 cm at 206 m. Those are the first and last of the rise's five tiers in terrace-front.py [I, arithmetic].
   - So a hill house is 65 to 125 pixels wide, a window 13 to 25 pixels, and a chimney pot about 6 pixels.
   - The hill must therefore be the street's own kit at lower detail, as real geometry. That fits his ruling of 3 October: "the hill built properly, never hidden in haze".
   - Only the town beyond, at 0.5 to 3 km (22 cm to 1.3 m a pixel), is cheap: impostors, merged meshes or cards.

---

## A. VEGETATION

### A1. How professional games make it

| Practice | What they do | Mark |
|---|---|---|
| **Scanned plant atlases** | Megascans plants are photographed leaves and stems on cards or in geometry. The street research found the same for its surfaces. | [SS, 8] |
| **Procedural trees in the engine (UE 5.7–5.8)** | The Procedural Vegetation Editor is "a node-based vegetation creation tool built on PCG". It "grows vegetation from scratch based on pseudo-botanical principles". Its output "is a Nanite asset that uses the latest Nanite Foliage technology, including instancing, GPU-based skeletal-driven animation, and voxel representation in the distance". | [READ, 2] |
| | In 5.8 it is "experimental. Substantial architectural changes can occur between releases", and "5.7 assets are not compatible with 5.8". A Growth Data Loader takes legacy Megaplants data. | [READ, 2] |
| **Nanite Foliage** | Three parts: assemblies (micro-instanced branches), skinning (wind on bones) and voxels for distance. Epic's roadmap calls it Experimental. | [SS, 6, 7] |
| | Nanite Assemblies are part of "experimental plugins". One tree went from 3.5 GB to 29 MB on disk, enabling "500k instances of dozens of tree variants". | [READ, 3] |
| **Data-driven scatter** | PCG Biome Core is a "data-driven biome creation tool made of native PCG Framework nodes". Biomes are defined "from volumes, splines, and textures", filtered by "height, density, and flow". It is **Experimental**: "use caution when shipping with it". | [READ, 4] |
| **KCD2** | "A heavily-customized version of the CryEngine". A team of about 250 by spring 2024. | [READ, 20] |
| | Vegetation is drawn "kilometers away", with subsurface light through leaves. | [SS, 27] |
| | How Warhorse authored its plants: **not found**. | — |
| **Ivy and urban weeds in portfolio streets** | Ivy is grown along the wall mesh, used as a force in SpeedTree. Moss decals break the hard line between ivy and wall. Weeds and cracks are placed as small dressing at the end. | [SS, 25] |
| **What our frames need from this** | KCD2's town frames carry one big tree behind the fountain and green at the wall feet. The Hook sheet has a dark tree at the bend, shrubs by the cottages on the right, and green among the hill's houses. The bar is a few well-made plants in the right places, not a forest. | [I] |

**The method in one line [I]:** scanned leaves and stems, grown into our own plants by a generator, placed by rule where water and neglect put them, varied by seed, and judged in the game's camera.

### A2. Free sources without AI restrictions

| Source | What | Licence, and AI tag or clause | Fit | Mark |
|---|---|---|---|---|
| **Poly Haven models** [14, 15] | nettle_plant, weed_plant_02, dandelion_01, grass_medium_01, shrub_01 to 04, tree_small_02, island_tree_01 and 03 (windswept coastal), tree_stump_02, dry_branches_medium_01 | CC0. No AI clause known [I]; pages unreached. Already used for the shop rooms; tools/art-recipes/fetch_polyhaven.py fetches by API on the builder's PC | **Good**: scans at 4K–8K. The island trees' species is unknown (check they are not Mediterranean). Skip jacaranda | [SS]; polyhaven.com UNREACHED |
| **ambientCG** [16] | LeafSet017 (ivy), LeafSet020 (dandelion), LeafSet001, 004, 005, 013 (green leaves), LeafSet021 (autumn), Foliage001 (grass); Moss001/002 already fetched (THIRD-PARTY.md) | CC0 | **Good**: leaf atlases are the input to our trees and ivy | [SS]; ambientcg.com UNREACHED (403 by curl) |
| **Megaplants on Fab** [8, 9]: English Oak, Common Hazel, European Beech, European Aspen, European Hornbeam, Black Alder, Black Poplar, Norway Maple, Ginkgo | Procedural trees for PVE, Nanite foliage | Fab Standard, free. **"Allows usage with AI: No" reported** [SS]. Experimental; built for 5.7 | Species right for Britain, but **excluded** unless the signed-in read says Yes | [SS]; Fab UNREACHED |
| **Megascans plants** (the free starter set) | Ferns, grasses, ground cover | Fab Standard. AI field unknown | Check each listing signed in | UNREACHED |
| **Sketchfab** [17] | "Ivy for walls" (arca_done) | CC-BY: **needs a ruling** for 3D. Sketchfab has its own NoAI tag (2023), so check the listing | Unseen | [SS] |
| | "Mossy old stone wall" | CC BY-NC-SA: **never** | — | [SS] |
| | Most plant scans found | CC-BY or NC | — | [SS] |
| **Quaternius and Kenney nature packs** (game-design/visual-bar-sources.md) | Low-poly trees and tufts | CC0 | **Fails the bar**: stylised | repo |
| **Tools: Sapling Tree Gen** [18] | Parametric trees, Add > Curve | GPL-3.0-or-later; Blender 4.4+; v0.3.7, 14 May 2024; formerly bundled with Blender | Yes, on our Blender 4.5 | [READ] |
| **Tools: IvyGen** [18] | "Adds generated ivy to a mesh object starting at the 3D cursor" | GPL-2.0-or-later; Blender 4.2+; v0.1.5; formerly bundled | Yes | [READ] |
| **Tools: Mtree (Modular Tree)** [19] | Tree library and Blender add-on | Add-on GPL-3.0; library MIT | Blender 4.5 support unchecked | [READ] README |
| **Tools: tree-gen (friggog)** [19] | Blender tree add-on | GPL-3.0. "Models generated using the tool are free for use without restriction in any context apart from direct sale as assets" | Age and Blender 4.5 support unchecked | [READ] |
| **Tools: ez-tree** [19] | JavaScript tree generator, exports GLB with LODs | MIT; npm 1.1.0 | Usable headless through Node; its bundled textures' origin unchecked, so use ambientCG leaves | [READ] |
| **Tools: BagaPie** [18] | Scatter and ivy | GPL-3.0; **needs Blender 5.0** | Not on our 4.5 | [READ] |

**A note on GPL [I]:** the GPL governs the add-ons' code, not the meshes they make. Nothing of the tools ships, as with Blender itself. If the allowlist is read as covering tools as well as shipped content, that reading is a ruling.

### A3. The kit we make

**What grows where in Meridian, October 1990.** The story puts Tom's arrival in October (game-design/warehouse-fire-2026-09-29.md).

| Place | Plants | Basis |
|---|---|---|
| Gutters, flag joints, kerb foot, round covers, downpipe feet | Annual grass tufts, dandelion rosettes, plantain, moss cushions; Oxford ragwort in yellow flower ("from March to December") | [READ, 20] for ragwort; [I] for the rest |
| Wall mortar, damp patches, copings | Ivy-leaved toadflax ("very characteristic of the vegetation that grows on walls", lilac flowers); pellitory and wall-rue ferns [I]; moss on copings, sills and north roof slopes; lichen on slate [I] | [READ, 20] |
| Derelict buildings, chimney stacks, gutters, waste ground, yards | Buddleia: "along railway lines and on the sites of derelict factories and other walls and buildings", up to 5 m, grey-green leaves. Its six weeks of flowers are over by October, so brown seed spikes [I] | [READ, 20] |
| Gables, yard walls, the churchyard wall | Ivy (evergreen, so fully green in October) [I] | — |
| Front gardens (upper Fairview), back yards | Privet hedges, low brick walls, small lawns, a rose or hydrangea [I]; "narrow front gardens ... vegetation at the threshold" (Hull, 1989) | photographs.md R06 |
| Trees (few in the Hook, more on the hill) | Sycamore, ash, birch on waste ground, the odd lime as a street tree, hawthorn and elder in scrub, a yew in the churchyard [I]. October: still mostly green, yellowing, wet leaves in the gutters [I] | — |
| Verges, churchyard, allotments | Rough grass, mown grass; allotment rows, sheds, canes and water butts, seen only from distance [I] | — |

**The parts, about forty pieces [I]:**

| Group | Pieces | Made from |
|---|---|---|
| V1 crack weeds | 8 clumps × 3 variants: grass tuft, dandelion, plantain, ragwort, groundsel, moss cushion, pearlwort line for flag joints, dead stalks | Poly Haven scans, trimmed; cards cut from ambientCG atlases |
| V2 wall plants | Toadflax trail, fern tuft, moss decal set, lichen layer on slate | ambientCG moss (fetched); masks from our wear layer |
| V3 buddleia | Sprout from a gutter or stack (0.5 m); bush on a wall top (2 m); waste-ground bush (4 m) | Sapling, with a lanceolate leaf atlas and seed-spike cards |
| V4 ivy | Grown per chosen wall: about three masses at first | IvyGen on the generator's own wall mesh; ambientCG ivy atlas LeafSet017 |
| V5 gardens | Privet hedge block (two lengths), hawthorn hedge, lawn patch, two shrubs, an allotment set for distance | Poly Haven shrubs; our hedge as a box with leaf cards |
| V6 trees | Five species × three ages (sycamore, ash, birch, lime, hawthorn/elder) plus one yew | Sapling or Mtree, with ambientCG leaves, exported with LODs |
| V7 ground | Lawn, verge and rough grass materials, plus grass cards for PCG | ambientCG Foliage001 and grass |
| V8 leaf litter | Wet leaf decals for gutters and pavements | ambientCG LeafSet021, autumn |

**Variation [I]:**
- Per instance: a random seed for scale, rotation, a small hue shift and wetness. A season parameter covers greens to yellows, and a decal set for fallen leaves.
- **Where weeds grow follows the wear layer.** The generator already emits a wear seed per house (DECISIONS, 1 October). A neglected house gets more weeds, a buddleia in its gutter and moss on its sill; a kept one gets a swept step.
- The town form bible says grime "follows water paths, hands, deliveries and heating". So weeds follow water: gutters, downpipe feet, leaks, the north side.
- Density must stay low: a street of 1990 people is neglected in patches, never a ruin.

**Tools [I unless marked]:**
- **Blender 4.5:** Sapling and IvyGen [READ, 18], with Geometry Nodes to bake clumps.
- **Unreal:** PCG for the scatter along splines and surfaces. The street research says PCG became production-ready in 5.7 [SS, its D24].
- **Avoid for shipping:** PVE, Nanite Foliage and Biome Core, all Experimental in 5.8 [READ, 2, 3, 4].
- **Rendering:** the small plants as ordinary instanced static meshes with LODs. Nanite stays for opaque architecture.

**How the agent drives it [I]:**
1. terrace-front.py already knows every kerb line, wall foot, sill, coping, downpipe and cover. It writes a weed-and-moss points file beside the wear masks: position, kind, scale and seed, weighted by each house's wear.
2. An Unreal Python step, or a PCG graph reading that file, spawns the instances.
3. Trees: one JSON of Sapling settings per species and age, run headless (`blender -b -P`), exported with LODs into F:\LedgerTools.
4. Ivy: IvyGen called on the chosen wall objects by script. The exact operator is to be checked in 4.5.

**Where a human eye must judge:**
- whether the species read right (a sycamore, not "a tree");
- the density (film set against ruin);
- the greens against the Hook sheet's damp dark greens;
- the trees' silhouettes against the sky.

This goes first to our gate and a fresh reviewer, then to his page as a whole street frame, not item by item (his rule of 29 September: small assets pass the gate alone).

### A4. The reference that sets the bar

- **The Hook sheet:** a dark tree at the bend, shrubs at the cottages, a few trees among the hill's terraces. The KCD2 fountain frame: one broadleaf tree behind a wall, read by its crown against the sky.
- **Photographs** (links only; photographer copyright):
  - photographs.md R06, Princes Avenue, Hull, 1989: "narrow front gardens ... vegetation at the threshold";
  - R07, Newtown Square, 1989: a grass court.
- **Leads I could not open:** the Geograph Whitby set [28]; "Whitby quayside in 1985" (Philip Pankhurst, Geograph 8402777) [SS, 28]. Geograph has a date filter for photographs taken 1988–1992 (UNREACHED; Geograph is CC BY-SA, so links only).
- **Botany:** Wikipedia's species pages [READ, 20] give habitat, size and season. They govern where each plant grows and what it looks like in October.

### A5. Variety, and the one proof

**Variety:** about 24 weed variants, 4 wall-plant pieces, 3 buddleias, 3 ivy masses, 5 garden pieces, 16 trees and 3 ground materials. **Why [I]:** a repeat reads once three identical copies share a frame. The hook view shows about 60 m of street, so each kind needs three variants, and the trees need species as well as ages.

**The proof:** "the neglect pass" on the proof frame's three near frontages and the bend, built inside the street research's items 7 (ground) and 9 (hill), not as a new item.
- **Contents:**
  - weeds in the gutter, the flag joints and around covers;
  - moss on sills and copings, toadflax in one damp wall;
  - one buddleia from a gutter or stack;
  - ivy on one gable or yard wall;
  - wet leaf litter;
  - one sycamore at the bend where the sheet has its tree.
- **Judged:** side by side with the Hook sheet and both KCD2 frames, in the hook camera by day and at night. The question: does the street now read as lived in and weathered, not swept, without reading as derelict? Then a fresh reviewer.
- **Effort [I]:** about 2–3 days. One day for the trees and ivy, one for the weed kit and placement file, half a day for judging and fixing.

---

## B. THE HILLSIDE AND THE DISTANT TOWN

### B1. How professional games make it

| Game or tool | Method | Mark |
|---|---|---|
| **GTA V** | Several LOD tiers (ILOD, LOD, SLOD): only objects with an SLOD are seen from far. Distant lights are tiny quads with a 32×32 texture, "heavily batched into instanced geometry". At range, a car is two headlights. | [SS, 21]; Courrèges' study UNREACHED |
| **Marvel's Spider-Man** | "3D IG-Impostors" for "the mid to distant cityscape" in "an efficient and persistent cache"; "no 2D impostors". Manhattan generated procedurally in Houdini. | [SS, 22] |
| **The Matrix Awakens / City Sample** | Nanite throughout, assembled by rule; HLOD for distance (the street research's note 1). | repo |
| **Unreal 5.8 HLOD** | Three layer types. **Instancing** replaces meshes with instanced components at their lowest LOD and suits "imposter meshes, such as trees and foliage". **Merged Mesh** makes one proxy. **Simplified Mesh** merges and simplifies. Both merged types can "Generate Nanite Enabled Mesh". | [READ, 1] |
| **Impostor Baker** | Ryan Brucks's octahedral impostors are built into UE5 as a plugin (Fortnite's). Forum reports of material faults in UE5. | [SS, 24] |
| **The Source engine's 3D skybox** | Distant scenery "modeled at a smaller scale, typically 1/16th", moving slower than the level, "far away, but not infinitely so". | [READ, 20] |
| **The Last of Us** | One matte-painted sky, animated with flow fields. | [SS, 23] |
| **Our own sky research** | A CC0 overcast sky photograph on a dome, the fog cut off before the dome, local exposure for the clouds (SKY-AND-HAZE-2026-10-02.md). | repo |

**The method in one line [I]:** detail falls with distance in bands. Near: the real kit, instanced. Middle: the same kit merged and simplified. Far: impostors or cards made from that kit. Horizon: a photographed sky. Fog and light values tie the bands together, and at night, lights become cheap instanced dots.

### B2. Free sources

| Source | Use | Licence | Mark |
|---|---|---|---|
| **The street's own kit** (terrace-front.py) | Every hill house, wall and roof | Ours | repo |
| **Poly Haven HDRI skies** (belfast_open_field and others) | Sky and horizon light | CC0. Already fetched (THIRD-PARTY.md, ledger/Assets/Sky/polyhaven) | repo; SKY note |
| **Unreal's HLOD, ISM/HISM, PCG and Impostor Baker** | Building and drawing the distance | Part of the engine | [READ, 1]; [SS, 24] |
| **Poly Haven and our own trees** (family A) | The hill's gardens and trees | CC0, ours | [SS] |
| **Environment Agency LIDAR, 1 m DTM** | Real slope profiles | Open Government Licence, attribution "© Environment Agency copyright and/or database right" [SS, 26]. Not on the allowlist, so **needs a ruling**. A real town's landform would also cut against a fictional town [I] | [SS]; environment.data.gov.uk and data.gov.uk UNREACHED |
| **Electric Dreams PCG graphs; City Sample** | Method only | UE-only content, so a ruling (street research note 2). City Sample's art is American, so no | repo |
| **Megaplants for hill trees** | — | Excluded while "Allows usage with AI: No" stands [SS, 9] | — |
| **Kenney Industrial** ("the docklands skyline", visual-bar-sources.md) | — | CC0 but low-poly: **fails the bar** | repo |

**Nothing for the hill or the far town needs buying or a ruling** [I]. The LIDAR is not needed: the atlas already fixes the rise at a 45 m crest (DISTRICTS.md, TOWN-FORM-BIBLE.md rule 6). That matches a real northern port: at North Shields the bank top stands "some 150 ft higher (46 m)" than the quay [READ, 20].

### B3. The kit, by distance band

Pixel sizes are for the hook camera at 2560 × 1440 [I].

| Band | Distance | One pixel | A 6 m house | Method |
|---|---|---|---|---|
| **The near hill** (lower Fairview; the rise's five tiers today) | 100–250 m | 4–11 cm | 55–125 px | The street's kit as instanced modules, Nanite on, HLOD Instancing layer |
| **The upper hill and crest** | 250–500 m | 11–22 cm | 27–55 px | The same modules; HLOD Simplified Mesh; trees at their lowest LOD or as impostors |
| **The far town** (Copper Row roofs, Ironside, Gullwing across the water, from the street and the quay) | 0.5–3 km | 22 cm–1.3 m | 5–27 px | Impostors baked from our kit, or cards rendered in Blender from our kit in 2–3 depth layers; landmarks as simple meshes |
| **The sky line** | horizon | — | — | CC0 overcast dome; a far ridge as a low silhouette mesh; fog cut off before the dome (SKY note) |

**Parts for the hill, about thirty pieces [I]:**
- **House bodies (6):**
  - two-storey brick terrace, flat front;
  - the same with a bay;
  - rendered (cream, white, grey pebbledash);
  - stone;
  - a 1930s hipped semi;
  - a post-war block for Foundry Court (DISTRICTS.md).
- **Roofs (3):** slate pitches with ridge tiles.
- **Stacks (3):** each with pot sets **and a TV aerial on the chimney**, the strongest 1990 roofline cue [I].
- **Windows:** inset, so the reveal reads as a 1–2 pixel shadow at 110 m; sash, casement and a little uPVC; nets and some lit rooms.
- **Doors and paint:** 6 colour sets.
- **Gutters and downpipes.**
- **Front walls (4):** brick, stone, railings stub, hedge.
- **Steps, retaining walls (stone, brick) and "bank" stairs:** "a series of steep stairs linked the upper and lower parts" of North Shields [SS, 29].
- **Planting:** gardens and allotments from family A; lamp columns along the contour roads.

**Landmarks for the far town, about eight [I], each our own design:**
- a church tower with a spire;
- a chapel;
- two dockside cranes;
- a gasholder;
- two works chimneys;
- warehouse and shed blocks;
- the resort front's pier.

Never a real silhouette: no Whitby Abbey, no Humber Bridge (canon: everything fictional). Nothing that reads as a pub sign or a bookmaker's at any distance (canon's content rule).

**Variation [I]:**
- A seed per terrace: house count, step up the slope, wall material, door colour, roof colour.
- A seed per house: lit or unlit, nets, aerial angle, chimney smoke on a few. The rise's code already does much of this (_north_rise) but as unique boxes.
- Wear from the street's own wear layer, scaled to distance.

**How the agent places it [I]:**
1. **Change _north_rise from emitting boxes to emitting a placement file:** module id, transform and seed per house, along contour lines at the atlas's heights. Then the hill is the street's modules, instanced, and improves whenever the street's kit improves.
2. **In Unreal**, a Python step or a PCG graph reads the file and spawns instanced kit meshes. UE 5.8's shape grammar can later fill each contour row with modules, which the street research already lists as a trial once the kit has passed [repo, 1-PIPELINE.md].
3. **HLOD:** build by commandlet, Instancing near and Simplified far [READ, 1].
4. **The far town:** lay it out in plan from the atlas. Then either bake impostors with the Impostor Baker, or render our kit in Blender to 2–3 cards (colour, alpha and depth at full 2,560 width) at 0.6, 1.2 and 2.5 km, and place them facing the quay [I].
5. **Night:** about three in ten hill windows lit (already in the code). Street lamps as instanced orange quads along the contour roads, and the far town as GTA-style batched light quads [SS, 21].
6. **Where a human eye must judge:**
   - the roofline's rhythm of stacks and pots against the sheet's;
   - whether the hill reads as a town in mist or stacked boxes (the street research's test);
   - its contrast against the street by day;
   - the night's scatter of lights.

**Cost on the RX 6700 [I]:** the hill as instanced Nanite modules costs far less than unique meshes. HLOD keeps draw calls down. Cards and light quads cost almost nothing. Measure the frame time in the hook camera before and after.

### B4. The reference that sets the bar

- **The Hook sheet's right half:** contour terraces stepping up behind the bend, retaining walls, mixed brick and pale render, slate, trees between rows, all softened by mist but legible.
- **The KCD2 arcades frame:** depth carried by a distant tower against a graded sky.
- **North Shields Fish Quay** [READ, 20]: the low town at the river, the bank top 46 m above, the 1980s decline. The best fit to a northern port with a hill [I].
  - Lead: "Fish Quay North Shields, unknown, 1990s" (co-curate, Newcastle) [29], UNREACHED.
  - Lead: Newcastle Libraries and North Tyneside libraries on Flickr [29], UNREACHED.
- **Whitby** (houses stacked on the cliffs above the harbour) and **Scarborough** [28], UNREACHED; links only, and never a copied skyline.
- **Hull and Grimsby** for the flat working water and a distant crane: photographs.md R08, River Hull, 1989.
- **Welsh valley terraces** for contour-following rows: not searched further. **Plymouth R11** is already cited by the atlas for the rise.

### B5. Variety, and the one proof

**Variety:**
- 6 house bodies × materials and paint gives dozens of distinct houses from a small kit;
- 3 roofs, 3 stacks, 4 front walls, 2 retaining walls, 1 stair;
- 8 far landmarks;
- 3 card layers for the far town.

**Why [I]:** at 55–125 pixels a house, the eye catches identical neighbours. The variation must sit in the modules' seeds, not in more modules.

**The proof:** the street research's **item 9**, "Hillside", rebuilt by this method in the hook frame.
- **Contents:**
  - the first two tiers as instanced kit houses with inset windows, stacks with pots and aerials, gutters, front walls and gardens with hedges and two tree species;
  - stone retaining walls with one bank stair;
  - the upper tiers simplified by HLOD;
  - a far ridge with a church tower and a crane;
  - day and night.
- **Judged:** laid over the Hook sheet's right half, then beside the KCD2 frames, by my check and a fresh reviewer. Does it read as a town in mist and not stacked boxes, legible, never hidden in haze?
- **Effort:** 2–4 days (the street research's estimate), plus a day for its planting from family A [I].
- **Later, not now:** the quay's view across the harbour (the far town's cards). The one list puts the hook view first.

---

## Per family, in one line

- **Vegetation:**
  - *Free:* Poly Haven's plant scans and ambientCG's leaf and moss sets (CC0), and Blender's own Sapling and IvyGen.
  - *We make:* every tree, ivy mass, hedge and weed clump, as a seeded kit placed from the generator's own lines.
  - *Impossible without a ruling:* Megaplants and Megascans plants unless his signed-in read shows AI allowed (if "No", never); Sketchfab CC-BY plants.
- **Hillside and distance:**
  - *Free:* the engine's HLOD, instancing and impostor tools, and the CC0 skies already fetched.
  - *We make:* the hill and the far town from the street's own kit, plus about eight landmarks and the night's light dots.
  - *Would need a ruling, and not needed:* the Environment Agency LIDAR (OGL) and Epic's UE-only samples (Electric Dreams, City Sample).

## What I could not reach or verify

- **Fab** (every listing, so every AI field) and **support.fab.com**, **quixel.com**, **polyhaven.com** and **api.polyhaven.com**, **ambientcg.com**: UNREACHED. Every Fab AI value above is a search summary, and the summaries disagree in quality.
- **Geograph, Flickr, co-curate.ncl.ac.uk, environment.data.gov.uk, data.gov.uk, wiki.openstreetmap.org, adriancourreges.com**: UNREACHED. No period photograph was seen by eye.
- **Epic's Nanite Foliage page** returned an empty contents list; its status comes from the roadmap and summaries [SS]. The Assemblies and PVE pages were read [READ].
- **Not checked:**
  - how Warhorse made KCD2's vegetation;
  - whether Mtree and tree-gen run on Blender 4.5;
  - IvyGen's scripting operator in 4.5;
  - the species of Poly Haven's island trees;
  - the origin of ez-tree's bundled textures;
  - the Impostor Baker's state in 5.8.
- **Cost figures:** none measured on the RX 6700.

## Sources

All read or searched on 3 October 2026.

1. Epic, "World Partition – Hierarchical Level of Detail", UE 5.8, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition---hierarchical-level-of-detail-in-unreal-engine [READ]
2. Epic, "Procedural Vegetation Editor in Unreal Engine", UE 5.8, undated. https://dev.epicgames.com/documentation/unreal-engine/procedural-vegetation-editor-in-unreal-engine?lang=en-US [READ]
3. Epic, "Nanite Assemblies", UE 5.8, undated. https://dev.epicgames.com/documentation/unreal-engine/nanite-assemblies [READ]
4. Epic, "PCG Biome Core and Sample Plugins Overview", UE 5.8, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-pcg-biome-core-and-sample-plugins-overview-guide-in-unreal-engine [READ]
5. Epic, "Nanite Foliage", undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-foliage-in-unreal-engine (fetched; no content returned)
6. Epic public roadmap, "Nanite Foliage & Skinning (Experimental)", undated. https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/2219-nanite-foliage-skinning-experimental- [SS]
7. Third Space Interactive, "Unreal Engine 5.7 Nanite Foliage", Medium, undated, https://medium.com/@thirdspaceinteractive/unreal-engine-5-7-nanite-foliage-a-game-changer-for-real-time-vegetation-c8e9692df3b5 ; Digital Production, 12 November 2025, https://digitalproduction.com/2025/11/12/unreal-engine-5-7-foliage-pcg-and-in-editor-ai/ [SS]
8. Quixel, Megaplants announcement on X, undated, https://x.com/quixeltools/status/1988631738340474924 [SS]; Quixel, "Discover the latest Quixel Megascans and free Megaplants", undated, https://quixel.com/news/discover-the-latest-quixel-megascans-and-free-megaplants UNREACHED; 80.lv, "Free Quixel Vegetation Assets Now Available For UE5.7", undated, https://80.lv/articles/create-lush-nanite-foliage-ready-forests-with-this-free-quixel-asset-pack [SS]
9. Fab listings, Megaplants, all undated: English Oak https://www.fab.com/listings/83642c38-7661-4df1-8629-0422e1898d26 (UNREACHED); Common Hazel https://www.fab.com/listings/27ded0d2-8bb2-4e44-a795-3a35725af218 ; European Beech https://www.fab.com/listings/cefe5722-9c31-4aa2-9ee2-e5426610d5e6 ; European Aspen https://www.fab.com/listings/ffa90e1a-e420-43d6-ade3-daa4bc189a0a ; Ginkgo https://www.fab.com/listings/53f033c3-00ec-425b-b44e-65c04fdbd2b0 ; Black Poplar https://www.fab.com/listings/6b22075c-53b6-4973-a6a5-9f4ccd6a72a8 [SS: "Allows usage with AI" reported No]
10. Fab listing, Megascans "Asphalt Road", undated. https://www.fab.com/listings/ab56bd64-6bd4-4882-8a02-86826355a8dd [SS; AI value unreliable]
11. Fab support, "NoAI meta tags and Created with AI self-declaration", January 2025. https://support.fab.com/s/article/Introducing-NoAI-meta-tags-and-Created-with-AI-self-declaration UNREACHED; [SS]: a seller's "Disallow use by generative AI" checkbox
12. Epic forums, "Introducing the NoAI and CreatedWithAI tags", undated. https://forums.unrealengine.com/t/introducing-the-noai-and-createdwithai-tags/774788/1 (cited by production/audits/2026-10-02-clothing-plan.md; not read by me)
13. This repository: production/research/natural-idles/NOTE.md (GASP's NoAI flag on Epic's own listing), read
14. Poly Haven, undated: https://polyhaven.com/a/nettle_plant , /a/weed_plant_02 , /a/dandelion_01 , /a/grass_medium_01 ; category https://polyhaven.com/models/nature/plants [SS; site UNREACHED]
15. Poly Haven, undated: https://polyhaven.com/a/shrub_01 to shrub_04, /a/tree_small_02 , /a/island_tree_01 , /a/island_tree_03 , /a/tree_stump_02 , /a/dry_branches_medium_01 [SS]
16. ambientCG, undated: https://ambientcg.com/view?id=LeafSet017 (ivy), LeafSet020, LeafSet001, LeafSet004, LeafSet005, LeafSet013, LeafSet021, https://ambientcg.com/view?id=Foliage001 [SS; site UNREACHED]
17. Sketchfab, undated: "Ivy for walls" https://sketchfab.com/3d-models/ivy-for-walls-b5e66f95a4de4cc19e68596f489eeaac ; "Mossy old stone wall" https://sketchfab.com/3d-models/mossy-old-stone-wall-5071918b66d541f5b41629167de55f7c ; CG Channel, "Sketchfab introduces NoAI and CreatedWithAI tags", February 2023, https://www.cgchannel.com/2023/02/sketchfab-introduces-noai-and-createdwithai-tags/ [SS]
18. Blender Extensions: Sapling Tree Gen https://extensions.blender.org/add-ons/sapling-tree-gen/ (v0.3.7, 14 May 2024); IvyGen https://extensions.blender.org/add-ons/ivygen/ (v0.1.5, 14 May 2024); BagaPie https://extensions.blender.org/add-ons/bagapie/ (v11.0.12, about September 2026); search https://extensions.blender.org/search/?q=ivy [READ]
19. GitHub (raw): Mtree README https://raw.githubusercontent.com/MaximeHerpin/modular_tree/master/README.md ; tree-gen README and LICENSE https://raw.githubusercontent.com/friggog/tree-gen/master/README.md ; ez-tree LICENSE, README and package.json https://raw.githubusercontent.com/dgreenheck/ez-tree/main/LICENSE ; all undated [READ]
20. Wikipedia: Buddleja davidii https://en.wikipedia.org/wiki/Buddleja_davidii ; Senecio squalidus https://en.wikipedia.org/wiki/Senecio_squalidus ; Cymbalaria muralis https://en.wikipedia.org/wiki/Cymbalaria_muralis ; North Shields Fish Quay https://en.wikipedia.org/wiki/North_Shields_Fish_Quay (edited 1 August 2026); Skybox (video games) https://en.wikipedia.org/wiki/Skybox_(video_games) ; Kingdom Come: Deliverance II https://en.wikipedia.org/wiki/Kingdom_Come:_Deliverance_II (edited 21 September 2026) [READ]
21. Cfx.re forum, "LOD and SLOD", undated, https://forum.cfx.re/t/lod-and-slod/2550075 [SS]; A. Courrèges, "GTA V – Graphics Study – Part 2", 2 November 2015, https://www.adriancourreges.com/blog/2015/11/02/gta-v-graphics-study-part-2/ UNREACHED, mirror summary https://jaytaylor.com/notes/node/1446501199000.html [SS]
22. Insomniac, "Spider-Man IG-impostors: cityscapes and beyond", ACM, 2018, https://dl.acm.org/doi/abs/10.1145/3283254.3283259 [SS]; GDC Vault, "Procedurally Crafting Manhattan for Marvel's Spider-Man", 2019, https://www.gdcvault.com/play/1026415/Procedurally-Crafting-Manhattan-for-Marvel [SS]
23. GDC Vault, "Moving the Heavens: An Artistic and Technical Look at the Skies of The Last of Us", undated. https://www.gdcvault.com/play/1020146/Moving-the-Heavens-An-Artistic [SS]
24. Epic forums, "Impostor Baker (UE5) materials are incorrect for foliage actor", undated. https://forums.unrealengine.com/t/impostor-baker-ue5-materials-are-incorrect-for-foliage-actor/531646 [SS]
25. 80.lv, "Breakdown: Realistic Environment in UE4", https://80.lv/articles/004adk-breakdown-realistic-environment-in-ue4 ; "Creating Realistic Vegetation with SpeedTree & Substance 3D", https://80.lv/articles/creating-a-mysterious-scene-with-lifelike-foliage-using-speedtree ; both undated [SS]
26. Environment Agency, "LIDAR Composite Digital Terrain Model (DTM) – 1m", undated, https://environment.data.gov.uk/dataset/13787b9a-26a4-4775-8523-806d13af58fc UNREACHED; UKAuthority, "Environment Agency makes LiDAR data open", 2015, http://www.ukauthority.com/data4good/entry/5439/environment-agency-makes-lidar-data-open [SS]
27. GameGPU, "Kingdom Come: Deliverance 2 – Review and Comparison of Graphic Settings", undated. https://en.gamegpu.com/test-gpu/rpgrolevye/kingdom-come-deliverance-2-obzor-i-sravnenie-graficheskikh-nastroek [SS]
28. Geograph: "Photos of whitby", https://www.geograph.org.uk/of/whitby ; "Whitby quayside in 1985" (Philip Pankhurst), https://www.geograph.org.uk/photo/8402777 ; both undated, UNREACHED [SS]
29. North Shields: co-curate, "Fish Quay North Shields unknown 1990s", https://co-curate.ncl.ac.uk/resources/view/26796 UNREACHED; North Tyneside Council, "The New Quay and The Fish Quay Conservation Areas" (character appraisal PDF, undated), https://legacy.northtyneside.gov.uk/sites/default/files/web-page-related-files/Fish%20Quay%20and%20New%20Quay%20Character%20Appraisal_0.pdf [SS]; Flickr, "Old North Shields" (Steve Ellwood), https://www.flickr.com/photos/steve-ellwood/albums/72157654403338309/ UNREACHED
30. This repository, read: production/reference/hook-sheet.png and both KCD2 frames (viewed); production/reference/photographs.md (R06, R07, R08); production/research/atlas-01/DISTRICTS.md and TOWN-FORM-BIBLE.md; tools/art-recipes/terrace-front.py (_north_rise, _tree, RISE_* constants); production/specs/unreal-look.json (fog_note); production/research/aaa-street/ (SUMMARY, 1, 2, 5, SKY-AND-HAZE); game-design/visual-bar-sources.md; game-design/warehouse-fire-2026-09-29.md (October); DECISIONS.md (last forty lines)
