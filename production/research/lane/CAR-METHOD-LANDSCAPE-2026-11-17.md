# Parked cars, the method landscape, before the first Blender run (17 November 2026)

Research helper for the lane, n16-9. Question from the owner: "what approach would a pro take on the cars?". All pages read 17 Nov 2026 unless marked. Hours and judgements not taken from a source are marked "est.". Prices are what the pages showed (US dollars). Nothing was bought, installed or signed into.

Reviewed 17 Nov 2026: PASS WITH FIXES, applied.

## Questions

1. How do professional studios build vehicle models now, and how do open-world games get many parked-car variants?
2. Which ready-made routes could replace or start the scripted loft (tools/lane/car_loft.py, a pure-Python 12-station loft whose Blender side is untested)?
3. For each: cost, licence against the allowlist, whether an AI agent can drive it by script, likely P9 result, the 40,000-triangle budget, and hours saved against the prior estimate (first car 24-40 h, each further class 8-16 h; N09-13-CAR-COSTS-2026-11-08.md).

## Part A: how the professionals do it

1. Blockout to real dimensions, then refine. A senior vehicle artist with Forza, Forza Horizon, DiRT and F1 credits describes the steps: take the vehicle's dimensions, build a proxy box with cylinders for wheels, camera-match to references, start at the wheel arches, refine the main shape, then cut the body panels. The triangle budget is shared out per part (bonnet, doors) by percentage; silhouette parts keep detail, small ones lose it; each level of detail is judged at its viewing distance; livery is vector decals so it can be swapped when licences change [A1]. This is the same order as the loft: class numbers first, shape second, panels later.
2. Licensed real cars come from scans or CAD and are often outsourced. Gran Turismo's car models were reported in 2020 as made by izmo in Bangalore from Polyphony's own scans, about three months a car against the six months quoted for earlier games [A2]. Virtuos says it worked on roughly 90% of the vehicles in Forza Horizon 6: modelling, UVs, texturing, engine integration [A3]. Outsourcing is how big studios buy volume. It is a purchase, and it starts from real cars, so it is closed to LEDGER twice over (16 Sep ruling; never-ship item 5).
3. Fictional cars share underpinnings. A solo artist's original UE5 sedan (inspired by, not copied from, a real model) reused the engine bay, suspension and chassis parts of his earlier hatchback and says this saved about a week; the whole car took about a month at four hours a day [A4]. That is a platform kit at small scale: one set of hidden parts, several bodies.
4. Variety comes from data, not new meshes. In Cyberpunk 2077 each paint variant is a data record that inherits from the base vehicle; one mesh carries several named appearances, and colours are layered material setups picked by masks [A5]. The UE5 sedan above puts colours, livery colours, dust and mud into Unreal material controls driven by RGB masks [A4]. Naughty Dog's GDC 2021 talk on The Last of Us Part II says its new vehicle pipeline gave more variety with less texture memory and was faster to build; only the abstract was readable [A6]. Epic's City Sample spawns its parked cars and traffic with Mass spawners, gives every drivable car data-only wheel settings, and drives damage on all of them from one shared Control Rig [A7]. The pattern across all four: one body per class, everything else (paint, trim, wear, plates, dirt) as parameters.
5. Nanite and cars. Epic's Nanite page (now for UE 5.9) does not mention vehicles. It does cover the fallback mesh (made from LOD0, used for collision, lightmaps and ray-traced reflections, tuned by Fallback Triangle Percent and Fallback Relative Error, or replaced by hand-made LODs) [A8]. That matches the 1 Oct finding that the coarse fallback showed instead of the car. Whether glass and other see-through parts can be Nanite was not confirmed on a page read today (unverified). No page read today describes a "mid-poly for Nanite" car workflow; it is not claimed here.
6. Polygon practice. BeamNG's 2015 blog models curved interiors from a 500-600-triangle base under subdivision and lands full interiors at up to 20,000 triangles [A9]. A parked car seen through glass needs far less (est.).

What a pro would do with LEDGER's constraints (est.): exactly what the asset plan already says. One parametric body per class from measured class numbers, shared hidden parts (wheels, underside, interior shell), and variety by material parameters and a seeded wear layer. The loft is not an amateur shortcut; it is the professional platform approach done by script.

## Part B: ready-made routes checked

### Blender add-ons (all on Superhive, formerly Blender Market)

- Car Primitives (Wilphi Design) [B1]. $19.95 one commercial seat, $119.95 unlimited seats, $11.95 non-commercial. GPL. Parametric through a Geometry Nodes modifier: width, wheelbase, wheel size and offset, front and rear overhangs, bonnet and shoulder height, windscreen and rear-window offset and steepness, roof height and width; mirror and subdivision modifiers. Blender 3.5 or later; changelog to 4.4; first published almost four years ago; last version 1.1.4, undated; update notes mention Blender 4.0, 4.3 and 4.4. No Python API is stated; Geometry Nodes modifier inputs can normally be set from Blender's Python (est., not confirmed for this add-on). Body types are not named on the page and no picture was judged, so its P9 result is unknown. It does what the loft does, with almost the same parameters; it adds no class ranges, no P9 screen and no fixed-topology promise for shape keys.
- Vehicle Forge (Samuel Abyan) [B2]. $19, GPL, Blender 5.0 to 5.2, published about a month ago. 32 vehicle types, low poly (cars about 2,500-3,500 triangles), stylised, no logos, random roof, door, grille and lamp choices with seeds. No UVs, no textures, no interior, no LODs. Fails the 2026-grade look; fine for a placeholder only, and placeholders do not pass the gate.
- Vehicles Bundle, 10 generators (ZEG) [B3]. $59 personal, $118 commercial, GPL. Tags say "low poly" and "game ready"; style and polycount not stated. Not judged.
- 3D NPR Car Generator (Blender Artists, 16 Jun 2026) [B4]. Geometry Nodes, stylised with a "semi-realistic" option. Price and licence sit on a Gumroad page not read. Stylised: likely fails the look (est.).
- Search also returned Car Generator Stylized, Turbo Charged Custom Vehicle Generator, Car Scatter and wheel generators (Wheel Gen, Ultimate Wheel Kit) [S1]; their pages were not read and are not evidence.

### Houdini

- Houdini Indie: $299 a year, revenue under $100,000; Apprentice is free but non-commercial (a third-party pricing page dated 19 Aug 2026 [B5]; SideFX's own price page was not reached). SideFX Labs (free game tools) exists as a public repository [S2]; no car body generator was found in it, and its licence was not read. Houdini has a scriptable Python side (unverified today). No ready car tool, a new program to learn, and a purchase: no gain over the loft (est.).

### Image-to-3D from our own concept pictures

- TRELLIS.2 is on the allowlist (MIT). The official release needs an NVIDIA card of 24 GB (N09-13). A community ROCm port for AMD exists, MIT, tested only on an RX 7900 XTX under Ubuntu; it lists "8 GB+ workable" with a reduced model but says RDNA2 (the RX 6700's family) is untested and may hit kernel problems; Windows is not covered [B6]. So it may not run on this PC at all.
- The 22 Sep ruling still reads "image-to-3D waits until hand-made props are the bottleneck" (RULINGS.md line 61). It is not lifted.
- Using our own concept pictures removes the "photo of a real car" problem only if the concept itself is fictional; a picture made by an image generator can still echo one real model (est.). Output is generated topology; it needs retopology to fit 40,000 triangles, separate wheels, glass and lamps, and new UVs. N09-13 estimated 12-30 h per car of cleanup; nothing read today changes that.
- Meshy Pro $20 a month; Tripo Pro $20 a month billed yearly ($240) (third-party page, prices checked 1 Nov 2026 [B7]). Both are purchases. Hunyuan3D stays banned.

### Base meshes and kits

- Fab cars: all NoAI-tagged in N09-13; refused. Not redone.
- CGTrader: its licence is refused (2 Oct ruling), so its many "generic" and "brandless" hatchbacks are out.
- Sketchfab: the search hits for 1980s cars are named real models (a Polski Fiat 126p, a Toyota AE86) [S3]; real shape, refused for the body.
- An itch.io "Base car mesh" page failed to load; unreached.
- Epic's City Sample Vehicles: Epic's own, "UE-Only Content", usable inside an Unreal game combined with your own content, never sold alone (forum answer, Dec 2023 [B8]). Not on the allowlist by name, so a record would be needed. Their shape and period were not judged (no picture read); a 2020s American city is the source demo, so they are unlikely to read as Britain 1990 (est.). Their method (Mass parked spawning, shared damage rig, data-only wheels) is worth copying.
- Epic's free automotive Substrate materials (a 2 Mar 2026 news headline says 280 for UE 5.7 [S4]; page not read). N09-13 already names Epic's Automotive Materials as free; they fit the "variety by data" pattern.

## Rulings applied

- 16 Sep: purchases and accounts are his alone; nothing for the street or cars. Every paid row below is a page DECISION only, and only if he changes that ruling.
- GPL used as a tool, never shipped, output ours (as the brief states his ruling; the same reading is in asset-plan 1-BUILDINGS-AND-INTERIORS.md; the line was not found by that word in RULINGS.md). Open point for any decision record: Car Primitives ships its own base meshes inside the add-on; whether a body grown from them counts as "our output" should be stated in the record before use.
- 3 Oct and 13 Oct: no NoAI content, even as reference, except Epic's own.
- Never-ship item 5: no real car models or brands. 22 Sep: image-to-3D held. Allowlist process 2: any new tool needs a decision record naming its licence.

## Table

| Route | Cost | Licence vs allowlist | Script-drivable | P9 (no named model; Britain/Europe 1985-91) | 40k tris | Hours vs loft (est.) |
|---|---|---|---|---|---|---|
| Scripted loft (current) | 0 | ours | yes, pure Python plus Blender script | two outline rounds passed the numbers, read as saloon then estate; Blender run untested | about 16,800 est. by the script | baseline: 24-40 h first, 8-16 h each class |
| Car Primitives | $19.95 one seat (purchase) | GPL tool; base-mesh question for the record | likely, modifier inputs (unverified) | unknown, not judged | fits with subdivision (est.) | saves 2-6 h on the first car's body bridge at best; nothing on classes (est.) |
| Vehicle Forge | $19 (purchase) | GPL tool | seeds and panel (API not stated) | stylised; fails the look | 2.5-3.5k, far under | none; rework exceeds the saving (est.) |
| Vehicles Bundle | $59-118 (purchase) | GPL tool | not stated | not judged | not stated | none shown |
| Houdini Indie | $299/yr (purchase) | commercial licence, record needed | yes (unverified) | no car tool found | n/a | negative: learning cost |
| TRELLIS.2 own concepts | 0 software | MIT, allowlisted; held by 22 Sep ruling (image-to-3D) | yes, but this card unproven (RDNA2 untested) | risk of echoing a real model | needs retopology | none: 12-30 h cleanup per car (N09-13) |
| Meshy / Tripo paid | $20/mo; Tripo $240/yr | allowlisted paid tiers (purchase); held by 22 Sep ruling (image-to-3D) and 16 Sep (nothing bought for cars) | web API | same risk | needs retopology | none, as above |
| Base meshes (Fab, CGTrader, Sketchfab) | various | NoAI, refused licence, or real shape | n/a | real shape fails | n/a | closed |
| City Sample Vehicles (Epic) | 0 | Epic UE-only; record needed | in Unreal | period and country unlikely (est.) | not read | method only |

## Recommendation

Keep the scripted loft and run its first Blender pass now with the round-3 shape the two outline rounds pointed to (set in car_loft.py, not yet tried in a blind round). It is what a professional would do under these rules: a class platform from measured numbers, fictional by construction, no money, fully allowlisted. Copy the professionals' variety method on top: one body per class, shared hidden parts, and paint, trim, wear, dirt and plates as material parameters (Cyberpunk's appearance records, Epic's materials, the seeded wear layer of 21 Sep); panel lines and trim as a trim sheet and decals, not modelled cuts; and a few fixed-topology shape keys per class (bumpers, ride height, door count) as the only mesh variety. The first Blender pass exports glass, wheels and body as separate meshes, and the export step checks the Nanite fallback or hand-made LODs at street distance; whether see-through glass can be Nanite in UE 5.8 is researched from Epic's 5.8 page before that export. No ready-made tool found today would pass P9 with more certainty or save meaningful hours.

Cheapest route that would pass P9 and the budget: the loft plus Epic's free automotive materials (free and Epic's own per N09-13; their page was not read today, so check the Fab licence and tag and whether they load in UE 5.8 at download, and name them in THIRD-PARTY.md) plus the seeded wear layer. Money 0. Hours as N09-13: 24-40 h for the first car; further classes 8-16 h each, possibly lower if they share the wheels, underside and interior shell (est.). P9 is not yet passed: only flat outlines have been screened.

Possible page DECISION (only if he wishes to revisit the 16 Sep ruling): one Car Primitives commercial seat, $19.95, as a cross-check body for P9. Gain: at most a few hours on the first car, unproven shape. Recommendation: no; leave 16 Sep as it stands.

## Sources (all read 17 Nov 2026)

- [A1] https://80.lv/articles/modeling-vehicles-for-aaa-games/ (Irfan Haider interview, 1 Jul 2019)
- [A2] https://www.gtplanet.net/polyphony-outsource-car-model-20200913/ (12 Sep 2020)
- [A3] https://www.virtuosgames.com/success-stories/forza-horizon-6/ (undated)
- [A4] https://80.lv/articles/creating-a-sedan-like-3d-car-using-unreal-engine-5 (23 May 2025)
- [A5] https://wiki.redmodding.org/cyberpunk-2077-modding/modding-guides/vehicles/boe6s-guide-new-car-from-a-to-z/boe6s-vehicles-paint-colors-and-varients
- [A6] https://gdcvault.com/play/1027001/Driving-Innovation-A-New-Vehicle (abstract only); https://trevelyan.artstation.com/projects/v2gRrO
- [A7] https://dev.epicgames.com/documentation/unreal-engine/city-sample-project-unreal-engine-demonstration
- [A8] https://dev.epicgames.com/documentation/unreal-engine/nanite-technical-details
- [A9] https://beamng.com/game/news/blog/a-look-at-vehicle-workflow-part-2 (16 Aug 2015)
- [B1] https://superhivemarket.com/products/car-primitives
- [B2] https://superhivemarket.com/products/vehicle-forge
- [B3] https://superhivemarket.com/products/vehicles-bundle-10-blender-generator-addons/docs
- [B4] https://blenderartists.org/t/procedural-npr-car-generator/1645186
- [B5] https://shade.inc/blog/sidefx-houdini-pricing-2026-fx-core-indie-license-costs (19 Aug 2026, third party)
- [B6] https://github.com/toastmanAu/trellis-2-rocm-comfyui
- [B7] https://www.3daistudio.com/3d-generator-ai-comparison-alternatives-guide/ai-3d-generator-pricing-compared (prices checked 1 Nov 2026, third party)
- [B8] https://forums.unrealengine.com/t/can-i-use-the-vehicles-in-city-sample-vehicles-in-my-own-game/1528806 (16 Dec 2023)
- Local: RULINGS.md (lines 46, 49-51, 61), ledger-v2/research/license-allowlist.md, N09-13-CAR-COSTS-2026-11-08.md, P9-BLIND-BRIEF.md, P9-OUTLINE-ROUNDS-2026-11-17.md, tools/lane/car_loft.py docstring.

Search results only, not read (not evidence): [S1] Superhive search listing (Car Generator Stylized, Turbo Charged Custom Vehicle Generator, Car Scatter, Wheel Gen, Ultimate Wheel Kit); [S2] github.com/pumachen/SideFXLabs and SideFX Labs installation page; [S3] Sketchfab 1980s car results; [S4] digitalproduction.com, "280 free automotive Substrate materials for UE 5.7" (2 Mar 2026).

## Unreached

- The GDC 2021 Naughty Dog talk itself (video, Vault); only the abstract was read.
- SideFX's own price page and SideFX Labs licence; Houdini prices rest on a third-party page.
- https://vladislive-dev.itch.io/base-car-mesh: fetch failed.
- 3D NPR Car Generator's Gumroad page (price, licence).
- Readray/lilys.ai notes on "Nanite for characters and vehicles": redirected, not followed (aggregator).
- Pictures of any add-on's output and of City Sample's cars: none judged, so no P9 claim is made for them.
- Meshy and Tripo paid-tier licence terms (the comparison page did not state them).
