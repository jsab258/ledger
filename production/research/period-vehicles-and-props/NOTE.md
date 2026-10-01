# Period cars, the phone box, the skip and the pallets (research note, 1 October 2026)

**Question.** Jafar, 1 October: "the cars are crude boxes, one untextured; the phone box, the skip and the pallets look like placeholders." The bar: they look like real 1990 things, or are removed. How do studios make such things, what free allowlisted sources exist, and what is the cheapest way to the bar? Separate helper, about 30 minutes; all sources read 1 October 2026.

## What we have (our files)

- **Cars.** car-model.py builds a generic hatchback: about 15,000 triangles of bevelled boxes in flat colours, with no textures, wear or interior. Until today's fix the import drew Nanite's coarse stand-in, 3,638 of 14,994 triangles. So part of "crude boxes" was a fault, not the model.
- **Skip and pallets.** The Base Mesh CC0 base meshes. These are blockouts by design. The skip has 928 triangles and was drawing 278.
- **Phone box.** A KX100 built from boxes in terrace-front.py, in flat colours.

## 1. Method: how studios do it

**The pipeline:**
1. Photographs and dimensions.
2. Blockout at true size.
3. Mid-poly modelling: a one-segment bevel on every hard edge, then weighted normals; no high-poly bake [2].
4. Two UV sets: a tiling base, and a set for masks.
5. A few master materials (paint, glass, rubber, chrome, painted steel, wood), with masks for edge wear, dirt, rust and mud [3].
6. Decals: plates, stains, rust streaks.
7. LODs or Nanite.

**Budget.** Background cars run 5,000–25,000 triangles on shared atlases [1]. Our 15,000 is enough. **The gap is materials and wear, not triangles.**

**What makes a car real at 5–20 m**, in order:
1. **Stance and wheels.** "The stance... sells character more than micro-detail" [1]. Tyre sidewalls, dark wheel wells, the arch gap, the right ride height.
2. **Reflections.** Clear-coat paint reflecting the sky, and glass reflecting over a dark interior. Without them a car is a painted box. Unreal's Clear Coat model and Epic's Automotive Materials provide both [4][5].
3. **Shading.** Bevels with weighted normals, so highlights run along the edges.
4. **Lines.** Panel gaps, door cuts, window rubbers, trim.
5. **Lamps.** Lenses with an inner pattern, amber indicators.
6. **Interior.** Seats, headrests and a wheel seen through the glass; a blockout is enough.
7. **Wear.** Grime on sills and arches, dusty glass, rust at the arch lips, faded paint.
8. **Period markers.** Black 1980s bumpers or 1970s chrome; white front and yellow rear plates, invented; period colours.
9. **Variety.** Identical cars read as set dressing.

**Fictional cars.** GTA and Watch Dogs: Legion (set in London) blend several real cars of one class into one fictional model [6]. Canon is met by a class-average shape that is not recognisable as one make.

**What 1990 held.** Ford, Vauxhall and Rover had 55% of 1990 sales. The top sellers were the Fiesta, Escort, Cavalier and Sierra, with the Metro sixth [7]. Parked cars were mostly built 1978–90 (my estimate, unsourced). So four generic classes cover the street:
- a small hatch, 3.6 m
- a medium hatch, 4.0 m (ours)
- a family saloon, 4.4 m
- an estate or small van

**Props work the same way.** A KX100 *is* a stainless box, so only its materials make it read. A skip is folded painted steel, chipped, rusted and dented, with rubble inside. Pallets are rough-sawn, greyed, and stacked or leaning.

## 2. Free sources

**Allowlist.**
- On it: CC0 (Poly Haven, ambientCG, Sketchfab's CC0 filter) and the Fab Standard Licence.
- Not on it: CC-BY (most free Sketchfab and Fab models), BlenderKit "Royalty Free", and Epic "UE-only" content (the allowlist covers only Epic animation).
- Fab's free "Personal" tier requires under $100,000 a year of digital-content revenue [8]. Taking only items free at both tiers avoids the question.
- Fab downloads need Jafar signed in. BlenderKit probably needs a free account (unverified).

**Cars**
- **Vehicle Variety Pack 1 and 2** (Switchboard, Fab Standard, free at both tiers). Late-1980s style, but the coupé-hatch reads as a Japanese make and the Vol. 2 saloon as a late-1990s Honda. Wrong country, canon risk.
- **City Sample Vehicles** (Epic). UE-only, and modern American.
- **Kenney Car Kit** (held) and **Quaternius** (CC0). Toys.
- **Poly Haven "Covered Car"** (CC0, 12.6k triangles). It has no make; fits a yard, not the kerb.
- **Sketchfab CC0:** nothing. **BlenderKit:** real makes only.
- **Epic Automotive Materials** (164) and **Automotive Substrate Materials** (280+) (Fab Standard, free at both tiers). Car paint with clear coat, glass, lamps, rubber, chrome. **Materials only, and exactly what our cars lack.**
- **No free, canon-safe, period British car exists.**

**Phone box**
- **Period.** About 73,000 K6s stood in 1980. BT began replacing them in 1985, making about 3,000 KX100s a month in 1987–89. By 1996 there were 80,000 KX kiosks against 15,000 red [9]. Both kiosks are right for 1990; the KX100 (our earlier choice) suits a modernised high street.
- **Canon.** The 1985–91 KX100 livery carries the real British Telecom "T" logo. Canon says the operator's mark is still owed by the brand bible.
- **Free models.**
  - Fab K6 (ModelVault3D, July 2026, Standard): Blender-viewport quality.
  - BlenderKit CC0 booth: 702 faces.
  - Sketchfab K6s: all CC-BY.
  - **No KX100 on any allowlisted source.**

**Skip**
- **Period size.** The 6-yard builder's skip is about 2.6 × 1.5 × 1.2 m at the base [10]. The flared top length is uncertain; measure it from a photograph.
- **BlenderKit "Industrial Skip"** (2024, 4,810 faces). The right UK shape, yellow, with a hire name to paint out, but Royalty Free, so **not allowlisted**.
- **Sketchfab "Old Rubbish Skip" and Fab "Dirty Rusty Skip".** CC-BY.
- **Dekogon Construction Vol. 1** (Fab, free). American; possibly a yellow container, unconfirmed.
- **No CC0 or Standard UK skip found.**

**Pallets**
- **Period size.** The UK standard is 1200 × 1000 mm, 9-block or 3-stringer [11].
- **Megascans "Wooden Pallet" on Fab** (Standard, free at both tiers). Scans at about 5,000 px/m, 1.18 × 1.24 m and 0.71 × 1.02 m: the 2026 bar. Check the blocks for brand stamps.
- **BlenderKit "Scan Wooden Pallet"** (CC0, 2025, 142k faces). Needs decimating.
- **Poly Haven** has no pallet but CC0 wood; ambientCG has CC0 PaintedMetal and Rust.
- **Megascans in 2026.** Free to all only until the end of 2024 [12]; now sold on Fab, with a large set still free under Standard (the pallets, the 96-asset Junkyard pack).

## 3. Cheapest way to the bar

| Thing | Route | Effort (one person, script plus AI) | Judged against |
|---|---|---|---|
| Cars | Improve the script (below) | 3–5 days to the first car through the gate; 1–2 days per extra class | Marshall R07 and R09 (photographs.md), in the game camera at 5–20 m; then the Hook sheet and KCD2 |
| Phone box | Keep the scripted KX100 and give it real materials: brushed stainless, glass with grime, the band, the yellow handle, a payphone, a lit header | 1–2 days | The Maaraig 1985-livery photo and Geograph KX100s (street-clutter-1990) |
| Skip | Script it: tapered plates, lugs and hooks, ambientCG painted metal and rust under wear masks, rubble inside | 1–1.5 days | Geograph UK skip photos; the size above |
| Pallets | Megascans from Fab; fallback is to script them with Poly Haven wood | Half a day (script: 0.5–1 day) | UK pallet photos |

**The car script:** three classes, mid-poly with weighted normals; Epic's paint and glass; an interior blockout, tyre sidewalls, lamp lenses, panel gaps, invented plates; vertex-colour dirt and rust; varied paint and age.

**Before judging a car, confirm all 14,994 triangles draw.** After two failed tries, research; after a third, remove the cars.

## Decisions for the owner

1. **Licence.** Add CC-BY or BlenderKit Royalty Free to the allowlist? Only the skip gains, and it can be scripted. *Recommend no.*
2. **Canon.** The kiosk's operator mark. Options: a minted fictional mark; a plain "TELEPHONE"; or a K6 instead. *Recommend minting one and keeping the KX100.*
3. **Scope.** If the cars still fail the gate, remove them, or show one covered car in the yard? *Recommend removing them.*
4. **Fab.** Jafar signs in once to collect the Megascans pallets and Epic's Automotive Materials. Take only items free at both tiers.

## Sources (read 1 October 2026)

1. Sunstrike Studios, 11 May 2026: https://sunstrikestudios.com/en/blog/car_modeling_for_games/
2. 80.lv, mid-poly in UE5, 27 Sep 2022: https://80.lv/articles/creating-assets-within-the-mid-poly-workflow-in-ue5
3. 80.lv, sedan-like car, 23 May 2025: https://80.lv/articles/creating-a-sedan-like-3d-car-using-unreal-engine-5
4. Epic, Automotive Materials Pack: https://dev.epicgames.com/documentation/en-us/unreal-engine/automotive-materials-pack-in-unreal-engine ; Fab listings https://www.fab.com/listings/5dd132fe-ee32-4e8c-9cd3-7496547dfb29 and https://www.fab.com/listings/1272587c-1431-4878-9d78-2a6b84ebe839
5. Epic, Shading Models: https://dev.epicgames.com/documentation/unreal-engine/shading-models-in-unreal-engine
6. https://www.sportskeeda.com/gta/why-fictional-car-brands-make-sense-real-ones-gta-series ; https://watchdogs.fandom.com/wiki/Fairlight
7. https://bestsellingcarsblog.com/1992/01/uk-1990-1991-ford-fiesta-grabs-the-pole-position/
8. Fab EULA: https://www.fab.com/eula
9. https://en.wikipedia.org/wiki/Red_telephone_box ; https://en.wikipedia.org/wiki/KX_telephone_boxes
10. https://www.lovejunk.com/news/skip-size-guide
11. https://www.palltechpallets.co.uk/guides/pallet-sizes-uk
12. https://www.cgchannel.com/2024/10/epic-games-has-made-megascans-free-to-all-but-only-until-the-end-of-2024/

13. Fab listings, each at https://www.fab.com/listings/ followed by: Vehicle Variety Pack dc1ada50-2523-44b1-b0e2-a72d14076fb4; Vol. 2 591e3b3f-9d49-4cd2-8e28-d471c1a10cab; Megascans pallets 6622c5d8-691b-4f1b-a29c-80c0e9d54af8; K6 10e69852-4823-40ce-b854-256717c679c2; Dekogon ba44a508-bfa5-444c-bbf4-69e8b5dee530.
14. https://polyhaven.com/a/covered_car ; https://www.blendkit.com/docs/licenses/ ; BlenderKit skip https://www.blenderkit.com/asset-gallery-detail/8446211a-d8e0-4b15-b52a-ef5d982d83bf/ ; Kenney https://kenney.nl/assets/car-kit
