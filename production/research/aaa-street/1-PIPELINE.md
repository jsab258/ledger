<!-- Research note 1 of 5 for production/research/aaa-street (1 October 2026). Written by a separate research helper given the problem; checked by the research session, which re-read Epic's 5.8 pages on City Sample PCG and on shape grammar: the LLM skill is quoted correctly ("a dedicated Shape Grammar Definition skill designed to guide a LLM through the process of building a shape grammar from scratch"), shape grammar is not marked Experimental (its cross-section node is), and the <A,B,C> rule was corrected. The pixel arithmetic in step 5 holds (70 degrees across 2560 pixels: 5.5 mm a pixel at 10 m); the hook camera's 39-degree vertical view is about 64 degrees across, so slightly finer. D = documented in a source (numbered below); I = inference. -->

# Building a realistic street in Unreal 5: the professional method, and what one person with agents can do (research note, 1 October 2026)

**Problem.** Quay Street is laid out right but reads as boxes with tiling brick; every engine feature on changed 2.4% of pixels. How do AAA teams make a street hold up beside KCD2, and which steps can scripts do? About thirty minutes, separate helper. D = documented (source number); I = my inference.

**Limits, read first.** The proxy blocked 80.lv, ArtStation, GDC Vault, archive.org, Game Developer, Polycount, PlayStation Blog and Creative Bloq. Only Epic's UE 5.8 documentation was read in full; the rest is a search engine's summary, marked "summary" below. The search budget ran out before Hitman, AC Unity or Mafia breakdowns turned up.

## 1. The pipeline, in the order studios run it

**1. Target frame and loop.** One small area is polished to final quality first, Tim Cain's "beautiful corner", one screen's worth (D23). Blockout screenshots are painted over to plan the art pass; value and contrast are checked early under game lighting (D22). Cyberpunk's contractors began every location from a greybox agreed with level designers and art directors (D18). I: our beauty corner is three frontages, pavement, kerb and ten metres of road, through the game camera, against the KCD2 frames and Hook sheet, before anything is multiplied (already your rule).

**2. Kit on a grid.** Skyrim's kits used a 512-unit footprint, snapped at half; seven kits made 400+ interiors in about 2.5 years (D15). The Division's tool takes a footprint and a list of kits (wall panels with windows, doors) and picks a panel per wall tile (D16). City Sample splits each style per storey into Corner, Wall and Entrance modules, 2,000+ modules in all (D4). Warhorse built modular kits so level artists could make "as many different structures as possible with fewer elements", with tiling textures and an in-editor shader (D19). I, for an 1880s terraced parade: a 225 mm horizontal grid (brick plus joint) and 75 mm courses, so brick lines run across seams. Pieces: shopfront (pilasters, console brackets, fascia, cornice, stallriser, recessed door), brick bays, sash window bay (lintel, sill, reveal), corner, party-wall junction, string course, eaves and gutter, slate roof, ridge, chimney stack and pots, downpipe, back extension, yard wall, ginnel arch: 25 to 40 pieces per style.

**3. Trim sheets.** Insomniac's "Ultimate Trim": one standard UV layout, thin trims at top, thicker below, end pieces at bottom, 45-degree bevels baked into the normal map on every edge; each material has a trim and a plain tiling version, which together cover any surface (D14). A London brick study did its detail with "trim sheet material and vertex painting"; the artist spent almost half his time on the brick material (D21). I: we have only the tiling half. Missing: the trims (sills, lintels, copings, fascias, gutters), bevels that catch edge light, and a blend layer.

**4. Assembly and variety.** Every big city in the sources is assembled by rules from kits, then hand-polished. The Matrix Awakens city: 7,000 buildings, 8 million instances, 16 km², Houdini (D17); a shape grammar per style, with a separate ground-floor style (D3); very little custom geometry; all Nanite, no LODs (D3). Spider-Man's Manhattan, 800 tiles of 128 m, was generated in Houdini, with systems built so output takes manual polish and keeps hand edits on re-runs (D11, D13). Cyberpunk's contractors kitbashed assets into shared prefabs (D18). **Directly useful:** UE 5.8 PCG has shape grammar built in: `A*` fills a run with a module, `<A,B,C>` places A if there is room, otherwise B, then C (corrected by the research session from the page itself: a fallback, not a random pick), `{[A,P]:2,[B,P]:1}*` weights choices (D2). The PCG City Sample has 26 to 28 building styles, all American (Chicago, New York, San Francisco; two readings of the page counted differently), and the PCG Primitives plugin ships a "Shape Grammar Definition skill" to guide an LLM through writing a grammar over an MCP server (D1). PCG became production-ready in 5.7 (D24). Electric Dreams turns hand-placed mesh groups into PCG inputs and scatters them, children following parents (D7).

**5. Real depth.** Nanite tessellation (5.4+) displaces Nanite meshes at render time from a height map (D5, D25). Forum advice: brick walls once done with parallax occlusion are now better as Nanite; POM still suits gravel (D26). Nanite takes only opaque and masked materials, and **mesh decals do not work on Nanite meshes** (D5). I, for our camera: at 2560 pixels and a 70-degree view, a pixel is about 5.5 mm at 10 m and 1.6 mm at 3 m. A sash set 100 mm back is 18 pixels of shadow across the street; a 10 mm mortar recess is 2 pixels. So the value order is (1) silhouettes against the sky: chimneys, pots, ridges, gutters, uneven rooflines; (2) reveals, sills, lintels, cornices and kerbs as real geometry; (3) brick relief by tessellation only on walls nearest the player.

**6. Dirt and wear.** Leaks and grime are layered with vertex paint and decals to break tiling and tell use (D31); material-blend decals lay dirt through the DBuffer (D32). In 5.8 DBuffer decals are default, cost follows screen coverage, and only materials that need decals should receive them (D8). Nanite cannot show per-instance vertex colour; use Texture Color painting, which needs virtual textures (D10). Mesh decals wrap edges (D9) but not on Nanite (D5). I, rules a script can apply: splash-back on the lowest 300 mm of walls, streaks under sills and gutter joints, soot above chimneys and flues, algae under downpipes, oil and gum on road and pavement, worn paint on doors and sills, puddles in dips.

**7. Set dressing.** The documented order: walls and roofs; structural parts (pipes, gutters, corbels); small detail (D30). Clutter must stay readable (D22). Spider-Man filled windows with interior mapping, rooms faked from a cube-texture atlas (D33). I: hand-build primary dressing (signs, blinds, A-boards, fish stalls) as about ten assemblies; PCG scatters the secondary (bins, posts, bollards, drain covers) and tertiary (litter, leaves, cigarette ends) along the pavement spline.

## 2. Team sizes and time

| Work | Who, how long | |
|---|---|---|
| Skyrim, 7 kits, 400+ interiors | level design team, ~2.5 years | D15 |
| Matrix Awakens city | "relatively small core team"; lead procedural artist 1.5 years | D17 |
| KCD2 | Warhorse ~100 grew to 250 staff; ~7 years | D20 |
| Cyberpunk, 130+ locations | one outsourcing studio | D18 |
| Solo portfolio streets and towns | 1 to 4 months each, one artist, Megascans and trims | D29 |

I: a KCD2-grade block of ten frontages is several artist-months at AAA; nearly all of it is kit, trim sheet, brick material and dressing. Assembly by rules is quick once those exist. No figure for a hero building was found.

## 3. What one person directing agents can do (all I, except where marked)

| Step | Agents by script | Needs an eye |
|---|---|---|
| Blockout | All | Composition |
| Value check against target | Greyscale, histogram and difference against KCD2 frames | Whether it holds up: Jafar, fresh reviewer |
| Kit list, dimensions | From photos and brick sizes | Cornice and sill profiles |
| Modelling kit in Blender | High (extrusions, profiles, bevels) | Proportion, one round per piece |
| Trim sheet layout, bevel bake | High (method D14) | Brick colour, mortar, weathering |
| Facade assembly, variety | Full: PCG shape grammar with Epic's LLM skill (D1, D2) or Blender geometry nodes | Which styles exist |
| Depth | Settings, maps | Tuning at game camera |
| Dirt and wear | Rule-based decals | Density; "lived in" |
| Primary dressing | Placement | Choice, story |
| Secondary, tertiary scatter | Full, PCG (D6, D7) | Readability |

I: the eye is needed for the brick material, profiles, dirt density and primary dressing, each fit for a daily page; the rest is mechanical once one frontage is approved.

**Money or licences (Jafar's call):** Houdini, used by Epic, Insomniac and SideFX Labs' free building generator (D28), is paid for commercial use (I; price unchecked). UE 5.8 PCG shape grammar and Blender geometry nodes do the job free; Buildify, a free geometry-nodes kit library, targets Blender 3.2 (D27). City Sample buildings are American styles (D1); licence unchecked.

## Sources (accessed 1 October 2026)

1. City Sample PCG. Epic UE 5.8 docs, undated. https://dev.epicgames.com/documentation/unreal-engine/city-sample-pcg-for-unreal-engine (read)
2. Using Shape Grammar With PCG. Epic UE 5.8 docs. https://dev.epicgames.com/documentation/unreal-engine/using-shape-grammar-with-pcg-in-unreal-engine (read)
3. City Sample Project. Epic docs. https://dev.epicgames.com/documentation/en-us/unreal-engine/city-sample-project-unreal-engine-demonstration (read)
4. City Sample Buildings. Fab, Epic, undated. https://www.fab.com/listings/008fe959-5511-428e-93bd-f99b1179f6d5 (summary)
5. Nanite Virtualized Geometry. Epic UE 5.8 docs. https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-virtualized-geometry-in-unreal-engine (read)
6. PCG Overview. Epic UE 5.8 docs. https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview (read)
7. PCG in Electric Dreams. Epic docs. https://dev.epicgames.com/documentation/unreal-engine/procedural-content-generation-in-electric-dreams (read)
8. Decal Materials. Epic UE 5.8 docs. https://dev.epicgames.com/documentation/unreal-engine/decal-materials-in-unreal-engine (read)
9. Using Mesh Decals. Epic docs. https://dev.epicgames.com/documentation/en-us/unreal-engine/using-mesh-decals-in-unreal-engine (read)
10. Mesh Paint Mode. Epic UE 5.8 docs. https://dev.epicgames.com/documentation/en-us/unreal-engine/activating-and-using-mesh-paint-mode-in-unreal-engine (read)
11. D. Santiago, Procedurally Crafting Manhattan for Marvel's Spider-Man. GDC, March 2019. https://www.gdcvault.com/play/1026415/ (summary)
12. Benno, Mullen, McAuliffe, Look Creation of Manhattan. GDC 2019. https://gdcvault.com/browse/gdc-19/play/1026495 (summary)
13. Insomniac Interview: The Tech Behind Marvel's Spider-Man. PlayStation Blog, 6 Sep 2018. https://blog.playstation.com/2018/09/06/insomniac-interview-the-tech-behind-marvels-spider-man/ (summary)
14. M. Olsen, The Ultimate Trim. GDC 2015. https://www.nothing-is-3d.com/dropCenter/uploads/infographie/tutos/Olsen_Morten_TheUltimateTrim_trim_sheets_texturing_workflow.pdf (summary)
15. J. Burgess, Skyrim's Modular Level Design. GDC 2013, April 2013. http://blog.joelburgess.com/2013/04/skyrims-modular-level-design-gdc-2013.html (summary)
16. J. Böhm, Trade Secrets of Game City Building in The Division. 80.lv, undated. https://80.lv/articles/division-pt-1 (summary)
17. Creating The Matrix Awakens in Houdini & UE5. 80.lv, undated (2022). https://80.lv/articles/breakdown-creating-the-matrix-awakens-in-houdini-unreal-engine-5 (summary)
18. Treehouse Ninjas, Lighting and Environments for Cyberpunk 2077. 80.lv, undated. https://80.lv/articles/creating-lighting-and-environments-for-cyberpunk-2077 (summary)
19. Warhorse Studios' Successful Computer Game. Autodesk, undated. https://www.autodesk.com/support/partners/success-stories/warhorse-studios-successful-computer-game-kingdom-come-deliverance/7756 (summary)
20. Vávra on Warhorse's size. PC Gamer, 2025. https://www.pcgamer.com/gaming-industry/ubisoft-has-staff-for-70-warhorse-sized-studios-after-cuts-says-kingdom-come-director-that-could-be-10-kcd2-sized-games-released-every-year/ (summary)
21. Q. Godillon, Detailed London Environment in Unreal. 80.lv, Jan 2024. https://80.lv/articles/look-how-to-create-a-detailed-london-environment-in-unreal-engine (summary)
22. The Level Design Book, Environment Art; Blockout. Undated. https://book.leveldesignbook.com/process/env-art (summary)
23. 9 stages of game production according to Tim Cain. Game World Observer, 22 Nov 2023. https://gameworldobserver.com/2023/11/22/game-production-stages-prototype-alpha-beta-ship-tim-cain (summary)
24. UE 5.7 release. VideoCardz, Nov 2025. https://videocardz.com/newz/unreal-engine-5-7-rolls-out-with-new-pcg-nanite-foliage-and-metahuman-tools (summary)
25. UE 5.4 Nanite Tessellation in 10 Minutes. Evermotion, 2024. https://evermotion.org/tutorials/show/13200/unreal-engine-5-4-nanite-tessellation-in-10-minutes (summary)
26. Parallax mapping or Nanite mesh? Epic forum, undated. https://forums.unrealengine.com/t/what-is-better-for-performance-parallax-mapping-or-nanite-mesh-with-a-lot-of-polys/789211 (summary)
27. Free Blender building generator Buildify. CG Channel, July 2022. https://www.cgchannel.com/2022/07/download-free-blender-3d-building-generator-buildify/ (summary)
28. Labs Building Generator 4.0. SideFX docs, undated. https://www.sidefx.com/docs/houdini/nodes/sop/labs--building_generator-4.0.html (summary)
29. 80.lv solo breakdowns (Catalonia town, Wild West kit, desert scene). Undated. https://80.lv/articles/from-concept-art-to-ue5-building-a-stylized-catalonia-inspired-town (summary)
30. A Detailed Game Environment Built in UE 5.3. The Rookies, 3 Jul 2024. https://discover.therookies.co/2024/07/03/a-detailed-game-environment-built-in-unreal-engine-5-3/ (summary)
31. Modular Scene in UE4: Blockout, Vertex Paint, Decals. 80.lv, undated. https://80.lv/articles/001agt-004adk-005cg-modular-scene-in-ue4-blockout-vertex-paint-decals (summary)
32. Material Blend Decal. a-maze.games, undated. https://www.a-maze.games/blog/material-blend-decal (summary)
33. A. Zucconi, Shader Showcase #9: Interior Mapping. 10 Sep 2018. https://www.alanzucconi.com/2018/09/10/shader-showcase-9/ (summary)

## What I could not verify

- The primary slides (Spider-Man, Ultimate Trim, Skyrim): kit sizes, piece counts and texel densities came from summaries only.
- How KCD2's towns were built: environment team size, building count, scanning, dirt layering.
- How Hitman, AC Unity, Mafia: The Old Country, Still Wakes the Deep and Everybody's Gone to the Rapture built their streets (only general press).
- Whether Nanite tessellation is still experimental in 5.8 (the page came back empty); whether Epic's own MCP server ships in 5.8 (third-party blog only); whether Texture Color painting can be scripted from Python.
- Houdini prices; City Sample buildings' licence; time per hero building.
