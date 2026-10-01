# Shop windows: fake interiors by interior mapping (UE 5.8, 1990 Britain)

Research note, 1 October 2026, by a separate research helper, about thirty minutes. The problem as given: the owner judged the street and said "the shop windows are black voids in every view". He asked for fake interiors by interior mapping, as games do it, before a build friends will play. The player walks the pavement past about twelve shopfronts by day and by night. Only the minicab office is enterable. Materials and meshes are made by script. All sources were accessed on 1 October 2026. "Mine" marks the helper's own inference. Photographs are links only and are never textures (production/reference/photographs.md).

## 0. The answer in brief

- **Method (what studios do, fitted to us).** Each shop gets one authored room. A script builds it in Blender and renders it as a single pre-projected 2D image (the SimCity 2013 / Matrix Awakens variant, not a cubemap), in two or three lighting states. A material we write ourselves (one Custom HLSL node, created by script) shows that image on the existing interior card behind the glass, with correct perspective as the player walks past.
- **The near metre is real geometry.** The window display in the first 0.6 to 1 m behind the glass is real meshes: the pawn trays, the fish slab, the laundry parcels. Interior mapping fails at close range and at grazing angles, and that is exactly where a pavement walker looks. In front of that sit the existing translucent glass, with Lumen front-layer reflections, and real meshes for blinds, grilles and lettering.
- **Night.** Each shop has a second image with its tubes on. Which shops are lit comes from the town's shop hours. Each lit window gets one real rect light, so its light spills onto the pavement.
- **Buy nothing and import nothing.** Every ready-made shader we found is paid, Unity-only, or under a licence that is not on our allowlist (section 6). The math is public (2008 paper) and is about 30 lines.
- **GPU cost is negligible** for twelve windows. The cost that needs watching is the glass reflections and the extra lights (section 5).
- **Scope flag.** Twelve bespoke rooms with real display props is several days, not one (section 7). Per the rules, one complete shop goes to his page as whole street frames before the other eleven are made.

## 1. How interior mapping works, and its variants

**The original.** Joost van Dongen, "Interior Mapping: A new technique for rendering realistic buildings", CGI 2008, Istanbul, June 2008. For each pixel of a flat facade, the shader casts the view ray into a virtual grid of rooms and intersects it with floor, ceiling and wall planes. The nearest hit picks the surface and its texture coordinates, so there is no interior geometry and no extra memory.
- Paper: https://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.pdf
- His own account (23 September 2018), with the limits: rooms are boxes; "any furniture in the room has be in the texture and thus flat"; close-ups and grazing angles give it away; extra furniture layers are possible "at an additional performance cost". It names users: Spider-Man (2018), SimCity (2013), Watch Dogs, Robo Recall, and Gears of War for shop fronts. http://joostdevblog.blogspot.com/2018/09/interior-mapping-real-rooms-without.html (reposted 25 September 2018: https://www.gamedeveloper.com/programming/interior-mapping-rendering-real-rooms-without-geometry)
- Alan Zucconi, 10 September 2018, adds Destiny, Overwatch, BioShock Infinite, Saints Row and Assassin's Creed. https://www.alanzucconi.com/2018/09/10/shader-showcase-9/

**Variant A: cubemap interiors (Unreal's own).** Unreal has shipped an `InteriorCubemap` material function since UE4. You build a room, capture it with a SceneCaptureCube, and turn the render target into a static TextureCube. A "Cube Scale" input was added for non-cubic rooms (Epic forum, posts of 30 and 31 May 2017): https://forums.unrealengine.com/t/using-textures-on-the-new-interiorcubemap-mf/78464
- The capture step can be scripted with Render Target Cube Create Static Texture Cube Editor Only (Kismet Rendering Library): https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/EditorScripting/Rendering/RenderTargetCube-
- Weakness (mine): the capture is taken from the room centre. Furniture painted into it is seen as if from the middle of the room, so it looks wrong from the pavement.
- UE 5.8's "Texturing material functions" page does not list InteriorCubemap: https://dev.epicgames.com/documentation/en-us/unreal-engine/texturing-material-functions-in-unreal-engine
- **No newer native interior-mapping node was found** in the 5.5 to 5.7 release notes. The "newer interior mapping nodes" in the brief do not appear to exist; marketplace shaders fill the gap.

**Variant B: the pre-projected 2D atlas (SimCity 2013, then Matrix Awakens).** Andrew Willmott (Maxis) used one perspective image per room, with room depth in the alpha channel and many rooms in one atlas. He called it highly authorable and only slightly worse than full cubemaps ("From AAA to Indie: Graphics R&D", TPCG 2013, Bath). The talk page now returns 404: http://www.andrewwillmott.com/talks/from-aaa-to-indie
- Ben Golus rebuilt it on 14 August 2016 and gave the authoring rule. Render each room with a 53.13° field of view (2·atan 0.5), the camera one room-width back from the opening, so for a cubic room the back wall fills half the tile. Alpha 128 means a cube-deep room. Rooms are picked at random per window. https://discussions.unity.com/t/interior-mapping/635709
- Andrew Gotow, 9 September 2018: a tangent-space version that follows the mesh surface, with per-building atlases. https://andrewgotow.com/2018/09/09/interior-mapping-part-2/
- Golus on the tangent-space approach, 26 December 2021: https://discussions.unity.com/t/attempt-at-tangent-space-interior-shading/866230/11

**Variant C: depth for the furniture (Matrix Awakens / City Sample, December 2021).** It uses the SimCity-style box projection for the walls and dual depth relief mapping for the furniture (Ben Golus's thread, not opened because x.com is paywalled: https://x.com/bgolus/status/1469364901126676482). The YouTube analysis https://www.youtube.com/watch?v=1vQc4OS9n-I and the Polycount thread https://polycount.com/discussion/228885/how-are-the-building-interiors-of-matrix-awakens-made (403) were not readable. The method is known from search summaries only.

**Variant D: parallax offset only, and layered cards.** Simon Schreibt compared three games on 2 April 2014: https://simonschreibt.de/gat/windows-ac-row-ininite/
- Assassin's Creed 3 slides a blurred, tiling texture by bump offset: cheap, with a frosted look.
- Saints Row 3 uses a sharp room texture with poster decals over it.
- BioShock Infinite uses two parallax layers moving at different speeds, billboarded foreground figures, and total internal reflection at grazing angles to hide the stretching.
- Mine: the grazing-angle trick is the one to copy. Glass's own Fresnel reflection does it for free.

**Variant E: Spider-Man.**
- 2018: interior-mapped rooms behind the windows. Elan Ruskin, "Marvel's Spider-Man: A Technical Postmortem", GDC, 21 March 2019: https://www.gdcvault.com/play/1026496/-Marvel-s-Spider-Man
- Spider-Man 2 (2023): 32 simple proxy rooms are kept in the ray-tracing structure underground. A window's ID picks one room, with variations of furniture and characters. Rays cast back out through the real window give the room its key light and shadows.
- That account comes from Digital Foundry's interview with Mike Fitzgerald, Insomniac's director of core technology: https://www.youtube.com/watch?v=fuu_wseJnIE. It is reported by Automaton on 1 December 2023: https://automaton-media.com/en/news/20231201-23558/ (the page did not fully load for us), and in the ResetEra thread: https://www.resetera.com/threads/digital-foundry-inside-marvels-spider-man-2-the-insomniac-games-tech-breakdown.777950/

**Variant F: a studio pipeline written up. SCS Software (Euro Truck Simulator 2 / American Truck Simulator), "Under the Hood: Parallax Interiors", 15 February 2025.** https://blog.scssoft.com/2025/02/under-hood-parallax-interiors.html
- Interiors are renders projected onto the inner walls of a box and kept in atlases by building type (offices, restaurants, shops, flats) and by "price range".
- Each interior has **three lighting variations** for times of day.
- One room takes **1 to 3 days** of artist time.
- The shader also handles glass perturbation, curtains, blinds, shutters and decals, and turning the glass off for broken or open windows.

**Cyberpunk 2077 and GTA.** No reliable public technical source was found for either; we say so rather than guess.

## 2. Which variant for LEDGER, and why

- **Pre-projected 2D, not cubemap.** The image is a plain perspective render from in front of the window, the direction the player actually looks from, so furniture reads correctly from the pavement. It is one 2D texture per state, easy to make from a Blender camera, and simple to compress and stream. A cubemap's centre capture smears furniture across the walls (mine, from Willmott via Golus above).
- **One room per shop, not random.** The twelve shops are different trades, so each gets its own room, with its depth and size as material parameters. No alpha depth and no atlas are needed for the shops; each material instance points at its own textures.
- **Hybrid with real display geometry.** Every source names close range and grazing angles as where the illusion breaks, and flat furniture as the giveaway (van Dongen 2018; SCS 2025). Our player is 1 to 3 m from the glass. So the display, which is what a shop window is for, is real meshes in the near metre, and the mapped room starts behind it.
- **The construction is already there.** The street already has an interior card about a metre behind the glass (the smashed-window note of 29 September 2026; tools/art-recipes/terrace-front.py, "interior card behind the glazing ... BOM C11"). That card becomes the mapped surface.
- **Dual depth relief for furniture: not now.** It adds a second authored depth pass per room, and the real display already covers the near field. Revisit only if the deep room still reads flat in review (mine).

## 3. Making the interior images by script (Blender)

1. **One spec row per shop:** trade; room width, height and depth (from the street recipe's real frontage, so the room matches the facade); and the window and door rectangles in that front plane.
2. **A Blender recipe builds the room**, using the same pattern as tools/art-recipes/:
   - **Shell:** walls, floor, ceiling and a back door or stair.
   - **Fittings:** counter, shelving and the trade's fittings (section 9), modelled from dimensions.
   - **Materials:** CC0 from ambientCG and Poly Haven, both on the allowlist. Poly Haven licence: https://polyhaven.com/license
3. **The camera follows Golus's rule, generalised (mine).** Put the camera on the room's centre line at a distance d in front of the front plane, with the frustum exactly framing the front rectangle W × H (horizontal FOV = 2·atan(W/2d)).
   - A room point (x, y, z), with z the depth behind the front plane, lands at u = 0.5 + (x/W)·d/(d+z) and v = 0.5 + (y/H)·d/(d+z).
   - With d = W and a cube-deep room, the back wall fills half the image, as Golus states.
   - Write d, W, H and D (depth) beside the image as JSON. The shader needs them.
4. **Three lighting states, as SCS does:**
   - **Day:** sky light through the front opening, with tubes on if open.
   - **Night, lit:** tubes on and no sky.
   - **Night, dark:** only a faint street-light spill through the front, sodium-coloured, plus perhaps a small back light.
   - Render in Cycles with denoising, about 2048 px wide (a 3 m window seen from 2 m covers well over 1,500 px at 3440 × 1440; mine).
5. **Physical brightness: bake in real units and do not brighten the interiors to make them "read".**
   - Unreal's emissive is in cd/m² (UE 5.8 "Using Physical Lighting Units": https://dev.epicgames.com/documentation/en-us/unreal-engine/using-physical-lighting-units-in-unreal-engine).
   - A shop lit to the 300 lx that today's EN 12464-1 asks for sales areas (500 to 1,500 lx for windows; e.g. https://luxmeterpro.com/lux-levels/retail-store-lighting-lux-levels, undated) gives mid-grey surfaces of roughly 50 to 100 cd/m² (L = E·ρ/π; mine). A small 1990 shop was probably dimmer (mine).
   - A daylit street is hundreds to thousands of cd/m², so **by day the windows look dark and the reflection dominates**. At night, under sodium lamps, a lit shop glows (mine).
   - Over-bright daytime interiors are the commonest giveaway of the trick (mine).
6. **What the images must never contain:**
   - **No people.** The town is simulated and the player reads witnesses; a painted shopkeeper who never moves is a false witness (mine).
   - **No real brands** (allowlist, NEVER SHIP 5).
   - **No alcohol and no gambling.** A 1990 newsagent would have shown football-pools coupons and often an off-licence shelf; both are left out.
   - **No children.**
7. **The flats above, if their windows are visible.** A pool of about eight domestic rooms, each with net-curtain and blind variants, mirrored at random and lit or unlit, chosen by a hash of the window's position so no two neighbours match. This one needs an atlas or a Texture2DArray. Spider-Man 2 needed only 32 rooms for a city (mine, scaled down).
8. **Memory.** 12 shops × 2 to 3 states × 2048² BC1 with mips (about 2.8 MB each) is roughly 70 to 100 MB (mine), streamed. None of the images reaches the 100 MB large-file threshold.

## 4. In Unreal 5.8, front to back

1. **Glass.** Keep M_LedgerGlass (translucent, per-pixel lit; tools/ue/make_glass_material.py).
   - Turn on Lumen's high-quality translucency reflections (front layer only; `r.Lumen.TranslucencyReflections.FrontLayer.Enable 1`, or the post-process setting). It costs GPU time, so profile it. Lumen docs: https://dev.epicgames.com/documentation/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
   - Translucent glass with default Lumen gives poor reflections (forum, 2022): https://forums.unrealengine.com/t/bad-reflections-with-lumen-on-translucent-glass/566095
   - Add a faint smear and dirt mask. Signwritten lettering on the glass (a gilt or white shop name, "Service Wash", "Pledges") goes as a masked layer.
2. **Window furniture as real meshes:** frames, transom and mullions (the recipe already makes these); a roller blind part-down; a café curtain on a rod; the pawnbroker's lattice grille at night; postcards and price tickets as decal cards.
3. **The display zone**, 0.6 to 1.0 m deep, on the stallboard bed: real props, lit by Lumen by day and by one rect light per lit window at night. Small bright emissive surfaces make Lumen noisy, so use real lights for the spill (evening-light-1990 note, 29 September 2026).
4. **The interior card, now the mapped surface.** Opaque (no sorting, no Lumen translucency problems), default lit, base colour black, rough, with emissive = the interior image × state × brightness. One Custom HLSL node does all of it:
   - (a) take the camera vector in the card's tangent or object space;
   - (b) intersect the ray with the box W × H × D behind the card;
   - (c) project the hit point with the formula in section 3;
   - (d) sample with gradients taken from the card's flat UVs (`SampleGrad`). Plain mipmapping draws seams along the room's corners, where the UVs jump (mine; a known interior-mapping artefact).
   - The box starts at the card. The card's UVs are set in the Blender recipe to span the shop's whole front rectangle, so two windows and the door glazing look into one continuous room.
5. **Per-shop material instances, made by script from the spec:** the day, night-lit and night-dark textures; W, H, D and d; LitAtNight; and an optional failing-tube flicker, used once on the street at most. A Material Parameter Collection carries the day-to-night blend from the game clock. The lit state comes from the town's shop hours (production/research/shop-hours-1990/NOTE-2026-09-29.md: everything shut by 8 pm, or 9 pm on the late day). Which closed shops keep a display light on is decided within canon and written in DECISIONS.md.
6. **Scripting.** A new tools/ue/make_interior_material.py follows make_glass_material.py:
   - **Material:** `MaterialEditingLibrary.create_material_expression(mat, unreal.MaterialExpressionCustom, ...)`, then `set_editor_property('code', ...)` and `('inputs', ...)` (Python API: https://docs.unrealengine.com/en-US/PythonAPI/class/MaterialExpressionCustom.html).
   - **Textures:** imported with AssetImportTask.
   - **Flats' pool:** if it needs a Texture2DArray, its `source_textures` property is scriptable (https://docs.unrealengine.com/en-US/PythonAPI/class/Texture2DArray.html). Whether setting it from Python rebuilds the array in 5.8 is unverified; the fallback is a 2D atlas assembled outside Unreal, with gutters between tiles.
   - **Staging:** if the game reads the spec at runtime, it goes into stage_game_data.py's list.
7. **Smashed windows come for free.** When the glass is hidden, the display and the room remain, which also answers the smashed-window note's complaint that the backdrop looked unchanged.
8. **The minicab office is real geometry.** It is enterable, so its window looks into the built room, not a mapped one (production/research/cab-office-interior-1990/).

## 5. GPU cost

- **The mapped card is cheap.** It costs one ray-box intersection and one or two texture samples per pixel, over the window area only. Van Dongen's paper reports a mapped building at 10 polygons and 1 draw call, against 158 polygons and 5 draw calls modelled, and the shader is faster than modelled interiors once there are many buildings. That figure comes from a search summary of the paper; the PDF text was not readable here. For twelve windows it is noise beside Lumen (mine).
- **The real costs are elsewhere:** the front-layer translucency reflections on the glass, the extra rect lights at night, and the display props. Measure the frame time before and after at 3440 × 1440, against production/research/unreal-frame-budget/.

## 6. Ready-made assets and their licences

| asset | what it is | licence and price, as listed | verdict |
| --- | --- | --- | --- |
| Unreal's InteriorCubemap function | engine content, cubemap variant | part of the engine | usable, but we do not need it |
| City Sample Buildings (Epic, Fab), the Matrix interiors | 2,000+ modules with the interior material; published 4 March 2022, updated 12 March 2025 | free; "UE-Only Content - Licensed for Use Only with Unreal Engine-based Products". https://www.fab.com/listings/008fe959-5511-428e-93bd-f99b1179f6d5 | **NOT on the allowlist** (its Unreal-only entry, SHIP-SAFE 8, covers Epic's animation only). Shipping it needs his ruling. Not needed |
| "Interior Mapping Shader", Marko Margeta (Fab) | cross-layout cubemap shader, UE 4.26 to 5.3; updated 9 October 2024 | free; licence terms "UE Marketplace" (the old Marketplace licence, not the Fab Standard License the allowlist names). https://www.fab.com/listings/0790debf-d144-4523-a6e9-ee73a82ff30d | **not plainly on the allowlist**, and not built for 5.8. Skip |
| "Interior Cubemap System", Roberto Filip (Fab) | Texture2DArray rooms, four foreground layers, day/night, UE 5.1 to 5.8; published 16 September 2026 | **paid**, CHF 27.08 to 63.21, Standard License. https://www.fab.com/listings/428d45ff-e4e8-456a-84f4-ab7009b9dc7c | **money.** Covered by the allowlist if bought, but not needed |
| "Interior cubemap master material", TexelForgeLab (Fab) | cubemap master material, UE 4.27 to 5.7 | **paid**, CHF 35.21 to 45.15, Standard License. https://www.fab.com/listings/db6b050b-c242-45ae-aa2d-6dee6529c56d | **money**; not needed |
| "Fake Interior Window with CubeMap" / "Fake Interiors FREE" (Fab) | Unity packages | Standard License, paid / free | Unity only. Irrelevant |
| wParallax maps (free samples of March 2021; the rest paid) | EXR 2D interior maps, modern rooms | wParallax's own licence ("private or commercial projects"; derivatives may not be redistributed as your own; may change without notice). https://license-agreement.wparallax.com/ ; https://www.cgchannel.com/2021/03/download-six-free-parallax-maps/ | **NOT on the allowlist**, and the wrong period. Skip |
| GitHub shaders | mostly Unity or three.js (e.g. https://github.com/codedgar/three-fenestra, https://github.com/GeorgeDaniel012/Interior_Mapping). One UE5 material set is reported as AGPL-3.0 (https://github.com/motionforge/Unreal_Engine_Essential_Materials_UE5, not opened) | various | Do not take code; AGPL would be copyleft in the game. **We need no code: the math is published** |
| Poly Haven / ambientCG | CC0 materials and props for the Blender rooms | CC0 | on the allowlist. Use |

**Patent awareness (not legal advice).** Robert Bosch holds US10380790B2 (granted 13 August 2019), "procedural window lighting effects". Its claim works out room and floor boundaries from the window transparency in a facade texture and adds a lighting layer. https://patents.google.com/patent/WO2016106365A1/en
- Our rooms are authored explicitly from the street recipe, not inferred from textures.
- Interior mapping itself was published in 2008 and ships with Unreal.
- Noted for completeness only; mine: low relevance.

## 7. Steps for about twelve shopfronts, in order

1. **Spec.** One file listing each shop's trade, room size, window and door rectangles, states, display props and night rule.
2. **Material.** The make_interior_material.py script, a checker-grid test room, and a walk past it in the game camera to check perspective, corners and mips (about half a day; mine).
3. **One complete shop first** (the pawnbroker is the best test: the densest display, the grille at night):
   - the room, its three renders, the display props, the glass reflections and its night light, in the game;
   - judged through the game's own camera and exposure, by day and night;
   - the gate: a check against period photographs, then a fresh reviewer.
   - CLAUDE.md says nothing is multiplied until one complete sample is approved by him in the assembled game. The street's look in whole frames is his to see, so this shop goes on his page as whole street frames, day and night.
4. **The other eleven,** as soon as the sample passes. Each is a room from dimensions plus a display, roughly 2 to 4 hours of script work each (mine; SCS's artists take 1 to 3 days per room). Keep each room beyond the display simple (shelving, counter, back door, light) and put the detail in the display.
5. **Wire the lit state to the town's shop hours,** add the rect lights, measure the frame time, and have the AI tester walk the street in the packaged build by day and by night.

**Scope (for him only if the date is tight):** about 4 to 6 working days in all (mine). A cheaper first pass is the mapped room with no bespoke display props, using generic shop shelving. It removes the black voids in about two days but will read flat at close range.

## 8. Judging it against the owner's bar (Kingdom Come: Deliverance II)

Judge it from the game's own camera and exposure, walking past at 1.5 m and from across the road, overcast and sunny, at dusk and at night, in motion, beside production/reference/kcd2-town-*.jpg. It fails if any of these is true:
- any window still reads as a black or flat void;
- an interior glows in daylight;
- the room fails to show depth as the player walks, or swims or stretches at grazing angles (the glass's Fresnel should take over there);
- corner seams show;
- display goods look like a flat picture;
- there are no street reflections by day;
- two neighbouring windows look identical;
- at night every shop is lit, or none is, or the lit ones leave no light on the pavement;
- fluorescent white and sodium orange are not told apart;
- anything breaks the content rules;
- the frame time rises noticeably.

Then the fresh reviewer is told to find the trick. Only frames that pass go to his page.

## 9. What a 1990 English shop interior looked like

**General (links only).**
- Peter Marshall's Hull photographs, already the project's shopfront reference: "metal shopfront, fluorescent strips, stacked goods". https://www.flickr.com/photos/petermarshall/51039473258 ; Hull album: https://www.flickr.com/photos/petermarshall/albums/72157715385264687/
- His **1990 London album** (1,544 photographs taken in 1990): https://www.flickr.com/photos/petermarshall/albums/72157719013554962/
- His Tottenham shopfronts with dated captions (cafés 1989 and 1991, bakers and butcher 1989): https://www.bygonely.com/tottenham-1980s-peter-marshall/
- Historic England, "100 Years of High Street Shopping from 1880 to 1980" (7 July 2022): https://heritagecalling.com/2022/07/07/100-years-of-high-street-shopping-from-1880-to-1980/
- Typical fittings (mine, consistent with the photographs above): bare fluorescent battens on the ceiling; painted walls; vinyl or quarry tiles; pegboard and wall shelving; handwritten price cards.

**By trade:**
- **Newsagent:** counter at the front, cigarettes on a gantry behind it, jars of sweets, magazine racks, bundled papers, a postcard-advert board in the window. Wikipedia: https://en.wikipedia.org/wiki/Newsagent%27s_shop ; Sheffield retro gallery: https://www.thestar.co.uk/news/sheffield-retro-17-nostalgic-photos-of-citys-corner-shops-and-newsagents-and-the-people-who-ran-them-4433588
  - Leave out pools coupons, lottery and alcohol (content rule).
- **Pawnbroker:** three gold balls outside; a window crammed with rings and watches on trays and pads, plus cameras, instruments and electronics, all with tickets; a grille at night. Stock searches only, e.g. https://www.gettyimages.com/photos/pawn-shop-uk ; the museum shop (1930s layout): https://en.wikipedia.org/wiki/Black_Country_Living_Museum_Pawnbrokers_Shop
  - **No dated 1990 photograph was found.**
- **Laundry:** the street's research calls it a steam laundry, which is a service counter with wrapped parcels on shelves, not a coin launderette (shop-hours-1990). **No 1990 source was found.**
  - For a launderette: My Beautiful Laundrette (1985) https://en.wikipedia.org/wiki/My_Beautiful_Laundrette ; surviving older fittings, Modern Mooch, 6 May 2020: https://modernmooch.com/2020/05/06/eight-laundrettes/
  - Which kind of laundry it is, is canon's to say, and settled within canon.
- **Fish shop:** white tiles, a sloping slab with crushed ice, enamel trays, price tickets. Hackney Museum, "Wet Fish", early 1980s: https://museum-collection.hackney.gov.uk/object-2015-30
- **Caff:** Formica tables, steamed glass, a menu board, a half-height café curtain (Marshall's 1989 and 1991 cafés, above).
- **Night shutters and grilles** were common on shops by the 1980s. The only sources found are trade blogs (e.g. https://sdg.uk/history-of-roller-shutters-uk/, undated), so treat this as weak. Mine: a solid shutter at night would cover a window entirely; a lattice grille over a lit display is the period's look.

## What this could not establish

- Dated 1990 interior photographs of a northern pawnbroker, laundry or fish shop.
- How Cyberpunk 2077 and GTA do their windows.
- The text of the Matrix Awakens breakdowns.
- Whether a Texture2DArray rebuilds from Python in 5.8.
- What Lumen's front-layer reflections cost on this street. Measure it.

## Flags

- **Money:** the two paid Fab shaders (CHF 27 to 63 and CHF 35 to 45). Not recommended; nothing needs buying.
- **Licences:** City Sample (Unreal-only, beyond the allowlist's animation-only entry); the free Marketplace-licence shader; wParallax; anything AGPL. None is recommended. The Bosch patent is noted only.
- **Canon, decided within canon (DECISIONS.md):** steam laundry or launderette; which closed shops keep a display light on; shutters or grilles at night.
- **Scope:** 4 to 6 days for all twelve with real displays; about 2 days for a flat first pass.
