Method researched: production/research/asset-plan/2-VEHICLES.md

# Plan: n16-9, parked cars, the hatchback first (17 November 2026)

Machine-free plan by a research helper; nothing built, downloaded or signed into. Sources are project files (dated) or web pages read in full on 17 Nov 2026. "Judgement" marks the helper's own reading; UNVERIFIED what no source confirms.

## 1. Where things stand

- Rulings: parked cars, fictional makes, with phase 2 (RULINGS 6 Nov); nothing bought for street or cars (16 Sep); no real car models or brands (license-allowlist, never-ship 5); no cars unless P9 passes (PLAN.md line 29). P9: an untextured body rendered side, front, rear, three-quarter; a blind reviewer names no model with confidence and places it in Britain or Europe, 1985-91 (pre-production/3-PROOFS.md).
- His note of 8 Nov: "one car first, the hatchback ... the other three after I've seen it" (answers/1VZHkCBAHdw8HBdNHrByL8/verdicts/parked-cars-route-2026-11-08.json). The session chose our own scripted Blender hatchback, no purchase, 24-40 h (archive/DECISIONS-to-2026-11-09.md, 8 Nov 20:30). Makes are the session's call; no tap unless a design is a whole frame (handover/DOUBLE-WEEK-PREP-2026-11-12.md, item 8).
- "His silhouette answer" (orders/2026-11-16.md): no recorded answer found in his page's answers or items; an archived page line reads "cars wait for the blind silhouette check, as you ruled on 2 October" (needs-you/archive.json). Judgement: the silhouette gate is P9's blind test by a fresh reviewer. UNVERIFIED that he expects more.
- Exists: tools/art-recipes/car-model.py, a bevelled-box hatchback (about 15,000 triangles, flat colours, no wear or interior); its kerb places held in production/specs/street-vehicles.json (period-vehicles-and-props/NOTE.md, 1 Oct). Budget: 40,000 triangles, 4 LODs, 2,048 px, simple collision, 6 hulls (production/specs/asset-budgets.json "car"); at most six cars in view, 0.5 ms (pre-production/4-BUDGETS.md line 99).

## 2. Reference games

- Mafia: The Old Country parks no cars in its measured street; traffic is spawned (aaa-reference/studies/04-street-world.md, 25 Oct). Its vehicle meshes and paint masters were never extracted (field-scans/CARS-2026-11-08.md). Kingdom Come II's carts were not counted (studies/04, blind spots). Numbers: none found.
- Method copied: data-driven colour sets (GTA V), invented makers with an ethos (Cyberpunk), blend a class, never copy a car (2-VEHICLES.md §1, 3 Oct; search summaries there).
- Step 0 (Judgement): one capped look at Mafia's vehicle files on demand (one extractor, space checked, own folder, key blanked after) for one car's triangles, LODs and paint master; numbers used only if they fit a parked background car (Mafia's are driveable 1900s cars).

## 3. Target: the fictional 1990 small family hatch

- Sizes (2-VEHICLES.md §2.2, class ranges marked inferred, to check against blueprints, dimensions only): 3,950-4,200 mm long, 1,630-1,700 wide, 1,360-1,420 high, wheelbase 2,450-2,550, 13 in wheels. car-model.py: 4,120 x 1,640 x 1,420, wheelbase 2,500, 175/70 R13; inside the class. Height/length about 0.34; belt near 0.62 of height (about 880 mm; the script's 920, Judgement: lower); glass 0.35-0.40 of height.
- Silhouette: wedge nose, short bonnet, tall glasshouse with thin pillars narrowing to the roof, sloping hatch; echoing none of the named-at-a-glance list (Escort, Astra, Golf's rear pillar, Metro and others, 2-VEHICLES.md §3.6).
- Panel lines: 3 mm grooves for doors, bonnet, hatch, fuel flap (§3.3).
- Glass: separate thin-translucent mesh (Nanite takes no translucency), tint and grime over a dark interior blockout with right-hand wheel; black rubbers (§3.2-3.4; N09-13-CAR-COSTS review, 8 Nov).
- Lights and trim: rectangular headlamps beside a slot grille, amber indicators, ribbed horizontal tail band, rear fog lamp, patterned lenses; black wraparound bumpers with rubbing strip, black mirrors, steel wheels with plastic trims, invented tyre lettering, mast aerial, tax disc (§2.5, §3.4).
- Plates: white front, yellow rear, reflective; 520 x 111 mm front, rear the same or 533 x 152; year letter G to 31 July 1990, H from 1 August; I, O, U, Z never year letters (https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_the_United_Kingdom, read 17 Nov 2026, first half only). Registrations invented, no dealer name or strip, characters as our own geometry, no font file (§2.3; the letterforms' copyright UNVERIFIED).
- Wear (.claude/skills/street-weathering): in the material first, by age and care seeds on a second UV set (dirt on sills, arches and hatch panel, rust at arch lips; 2-VEHICLES.md §3.5); decals only for particular marks; wetness tied to the street's. Grime tints on M_LedgerGrime are four times the colour meant. The dry patch under the car cannot be a decal (no decal writes the ground's coat; skill §4-5): Judgement, a known shortfall, not a blocker.
- Parts under 10-20 cm drop at High: mirrors and aerial judged there (memory note, wet ground's coat). Stance and reflections first (NOTE.md).

## 4. Routes, cheapest that can pass first

| Rank | Route | Hours (est.) | Evidence | Risks | Licence |
|---|---|---|---|---|---|
| 1 | Own: car-model.py lofted (about 12 stations, mirrored, weighted normals), modules on sockets, two UV sets, own paint, glass, rubber, lens masters | 24-40 first car (NOTE.md; 2-VEHICLES.md §5.2: 4-6 days with a swapped variant) | Fictional by design; the scripted route passed accessories at blind review (asset-plan/SUMMARY.md) | Reads as no era or one real model; Nanite stand-in drawn (1 Oct); the box car failed his look | Ours |
| 2 | CC0 base adapted | n/a | None exists (NOTE.md; N09-13 and field scan, 8 Nov); Poly Haven's covered car fits a yard only | - | CC0 |
| 3 | Generated, Kiln-like | n/a | Kiln is clothing; vehicles after M7 (RULINGS 14 Nov); TRELLIS needs NVIDIA (card is AMD); Meshy is a purchase (N09-13) | Melted shells, real shapes | Unavailable or barred |
| 4 | Epic City Sample | n/a | Rejected 8 Nov: modern American, real-make shapes | Real model | Epic exception |

- Epic's Automotive Materials, read 17 Nov 2026 (https://www.fab.com/listings/5dd132fe-ee32-4e8c-9cd3-7496547dfb29): publisher Epic Games, free, "Allows usage with AI: No", set up for Unreal Engine 4, 164 materials (car paint, metals, lights, reflectors, interior); glass and rubber not mentioned. Judgement: inside the allowlist's Epic exception, but not held (none in ue-probe) and adding it needs his Fab sign-in; optional, never awaited.
- CarGen (GPL-3.0) and Car Primitives (paid): checklists only (2-VEHICLES.md §4; field scan §3).

## 5. Steps for the hatchback (Judgement, within the 24-40 h estimate)

0. Mafia's car files, capped: 1.5 h.
1. Brief (maker's ethos; three or more real cars for dimensions only, provenance line beside the asset; signature parts drawn fresh); loft generator: 6-10 h.
2. P9 renders and one blind reviewer: 2-3 h. A confident name: change that feature, one more try; then research.
3. Panel gaps, glass, lamps, bumpers, wheels, interior, plates: 6-10 h.
4. Masters and wear masks: 4-8 h.
5. Import; every triangle drawing; LODs or Nanite fallback; placed at the held kerb places: 3-5 h.
6. Gate and packaged walk: 2-4 h.

About 25-41 h. The order costs n16-9 at 12 h, enough for steps 0-2 and part of 3, not "one car passed packaged"; the session should restate the hours or the done line (Judgement).

## 6. The check

- First: P9 passed; all triangles draw; within asset-budgets.json.
- Gate (RULINGS 3 Nov, medium piece, two rounds at most): game camera at the played level, 5-20 m, day wetness; hook by day, reverse, night, each beside its last good picture; the Hook sheet for placement, density, wet roofs and glass, dark wheel wells (its cars look late-1990s, so design is judged against Marshall R07, R09 in production/reference/photographs.md); the KCD2 frames; NOTE.md's nine points (stance, reflections, shading, lines, lamps, interior, wear, period markers, variety).
- Packaged: passes the nightly walk; six cars in view within 0.5 ms. A frame with cars is a whole street frame, so his page (DOUBLE-WEEK-PREP item 8).

## 7. The other three (saloon, estate, van)

- Each further class 8-16 h on the kit (NOTE.md, est.): 24-48 h for three. Sizes: saloon 4,300-4,500 mm, estate 4,400-4,800, car-derived van 3,900-4,200 (2-VEHICLES.md §2.2).
- Re-costing (Judgement): split the hatchback's logged hours into kit (steps 1, 4, 5) and car-specific (2, 3, 6); each further car costs its car-specific share plus a quarter of the kit share, each with its own P9 test; none before he has seen the first (8 Nov).

## Unreached or not done

Mafia's vehicle files; Sketchfab's filtered CC0 search; The Base Mesh's vehicles; class blueprints; the Wikipedia page's second half; Fab terms as a signed-in buyer sees them; any record of his silhouette answer.
