# Shop rooms seen from 1 to 3 m: what professionals do

Research note, 3 October 2026, by a separate helper, about thirty minutes. It follows NOTE.md (1 October) and GOODS-2026-10-03.md, and does not repeat them.

- OPENED means the page was read.
- SNIPPET means only a search summary was seen.
- UNREACHED means the page refused us. Nothing is concluded from it.
- "Mine" marks my own inference. Every cost figure here is mine and unmeasured unless a source is named. Measure before relying on any of them.

## 0. The answer in brief

1. **Interior mapping is a distance technique.** Shipped games use it where the camera stays several metres away or moves fast: from a car (Forza Horizon 4, Euro Truck Simulator 2), from a swinging hero high up (Spider-Man), on upper floors and across a city (SimCity, the Matrix demo). Every published account names close range and grazing angles as where it breaks.
2. **On foot, at 1 to 3 m, the things a player looks at are real geometry.** Kingdom Come: Deliverance II builds its window counters as real models fitted to each house's window, with real goods on them. Watch Dogs: Legion made its clothing storefronts real, interactive displays. Spider-Man 2 replaced painted rooms with 32 real, simple rooms that rays look into.
3. **Our failure is the method, not a bug.** Interior mapping paints the whole room onto the five walls of a box. Anything standing away from those walls (a counter, chairs, a dryer stack, a buoy) is painted onto the wall behind it, so it slides and stretches as the player walks. That is the "smear". The one shop that passed kept everything flat against the walls, which is exactly the case the technique handles.
4. **Recommendation:** make the ten ground-floor shop rooms real geometry in Unreal, exported from the Blender rooms we already have. Keep interior mapping only for the flats above and anything seen from far off. Cost: small on the graphics card if Lumen's rules are followed; the night lights and the glass reflections are the parts to measure. The main traps are Lumen's own rules for rooms (section 4).
5. **Stock on shelves:** never plain blocks. Front rows are simple bevelled shapes carrying printed labels from one shared texture atlas, varied per item. Organic goods are scans. Shelves high or far back can be one baked picture per shelf bay, flush with the shelf front.

## 1. Why our rooms smear (the mechanism)

- **The picture lives on the walls.** "What you see in the game isn't actual geometry, it's essentially a render projected onto the inner walls of a cube" (SCS Software, 15 February 2025, OPENED). They add that "at certain angles and in specific conditions, the illusion can break, revealing noticeable distortions in furniture".
- **Free-standing objects distort.** An Unreal tutorial on interior mapping warns to "be careful with prop placement, angle and distance from the walls as some shapes can distort incorrectly" (Martin Widdowson, 13 July 2020, OPENED).
- **Furniture is flat.** Van Dongen, who invented the technique: "Any furniture in the room has be in the texture and thus flat. This is visible in Spiderman in close-ups" (23 September 2018, OPENED).
- **Why the smear is diagonal (mine).** Our rooms are pre-rendered from one camera in front of the window. In that picture the side walls and the floor are thin, steep wedges with few pixels. When the player walks along the pavement and looks in at an angle, the shader shows those wedges nearly face-on. A few pixels stretch across a large area, along the camera's lines of sight, which are diagonal. A counter painted onto the floor and back wall stretches the same way, and reads as a ghost.
- **A second possible cause, to test (mine, unsourced).** The room moves inside a flat card. The card's motion vectors describe the card, not the painted room. Temporal anti-aliasing (TSR) may therefore blend the wrong history and leave trails while walking. Test: compare a still frame with one taken while moving. If the streaks shrink when still, this is part of it. Real geometry has correct motion vectors and does not have this fault.
- **Why the one shop passed (mine).** Everything sat on the walls, so the projection surface and the real surface were the same, and only the goods' own small depth was wrong.

## 2. The method in shipped games, by distance

### 2.1 Far, fast, or high up: interior mapping

- **Forza Horizon 4 (Playground Games, 2018), a British town seen from a car.** Gareth Harwood (Game Developer, 10 December 2018, OPENED):
  - Rooms were "modelled in 3D using a uniform scale, and then rendered to a unique texture" (3ds Max and V-Ray).
  - Three layers: window (glass and frame), curtains or blinds, interior.
  - Atlases by style, including "commercial atlases that are on our shops, restaurants and the quintessential British pub", up to eight interiors per atlas.
  - A night texture per interior. Lights turn on at varied times per building.
  - Far away, the parallax fades to one flat image.
  - "Shopfronts that you can drive right up to had higher rendering budgets than roofs."
  - Chris Harper, who wrote the shader, lists a "Fresnel effect at grazing angles to blend out interior" and special handling for bay windows (ArtStation, 2 March 2019, OPENED).
  - Mine: the camera is a car on the road, several metres from the glass and moving. It is not a pedestrian at 1 m.
- **Euro Truck Simulator 2 / American Truck Simulator (SCS, 2025).** Renders projected onto a box; three lighting variations; 1 to 3 days per interior; the shader also handles glass and curtains (OPENED). Seen from a truck cab.
- **Marvel's Spider-Man (2018).** Interior-mapped rooms, flat furniture visible in close-ups (van Dongen, OPENED; Elan Ruskin's GDC 2019 postmortem, SNIPPET, not watched).
- **The Matrix Awakens / City Sample (Epic, December 2021).** Box projection for walls plus parallax against two depth maps for furniture, dithered between slices (Epic forum, explanation posted 25 August 2023 citing the State of Unreal 2022 talk, OPENED; the talk itself not watched). Built for a city seen from cars and at height. Its licence is not on our allowlist (NOTE.md, section 6).

### 2.2 Tricks games use to hide the limits

- **Fade the room out at grazing angles with the glass's Fresnel** (Forza Horizon 4, OPENED; BioShock Infinite, in NOTE.md). Cheap, and we should keep it on any mapped window.
- **Extra flat layers for furniture.** Van Dongen: extra texture layers are possible "at an additional performance cost" (OPENED). A search summary says an old Gears of War used "a far wall, and one or two alpha layers for furniture" for shop fronts (SNIPPET). Mine: a layer is still a flat cut-out, and at 1 m and an angle it reads as cardboard.
- **Depth for furniture** (the Matrix's two depth maps). Mine: a height field cannot show a gap under a chair or the far side of a buoy, and it still breaks at grazing angles. It is also the most complex shader to write.
- **Pixel depth offset to tuck objects into the room** (Widdowson, OPENED). It sorts things; it does not make them solid.
- **Keep the room's contents on the walls** (consistent with SCS and Widdowson; our own passed shop shows it).
- **Window dressing that hides the room:** curtains, blinds, lace, translucent blinds (Forza Horizon 4, OPENED); "dress the shop window appropriately and be done with it" (The Division, Johannes Böhm, 80.lv, 28 February 2017, OPENED). Mine, for 1990 Britain: half-height café curtains, roller blinds part down, a full window display, stickers and price cards on the glass, sign-written lettering, a steamed lower pane on the caff, a lattice grille at night.

### 2.3 Close, on foot: real geometry

- **Kingdom Come: Deliverance II (Warhorse, 2025), our bar.** Luca Eliseo made two kinds of stall for Kuttenberg: market stalls, and those "used to sell directly from the inside of their house to the people in the street". The second kind was modelled to "follow specific measurement in order to correctly fit the window", open and closed, with LODs and collision (ArtStation, published 5 March 2025, OPENED from this PC). The pictures credit real fruit and vegetables to Tomáš Svojša. No source says how Warhorse treats the room behind those windows. Mine: the player sees real goods on a real counter in the opening, and the room behind is dark and shallow.
- **Watch Dogs: Legion (Ubisoft, 2020).** Clothing shops were not entered. Their storefronts were real, interactive displays with mannequins on sockets (SNIPPET).
- **Marvel's Spider-Man 2 (Insomniac, 2023).** They moved from painted rooms to 32 simple real rooms that the window rays look into (Digital Foundry interview with Mike Fitzgerald, December 2023, SNIPPET; also NOTE.md). Mine: the studio that made the best-known interior mapping left it when it could afford real geometry.
- **No source** was found for Cyberpunk 2077, GTA V, Red Dead Redemption 2 or Hitman. We do not guess.

**The pattern (mine, from the above):** interior mapping where the camera is far, high or fast; real geometry where a walking player stops and looks; window dressing in between to hide whichever is used.

## 3. Unreal 5.8 facts that decide the method

From Epic's UE 5.8 Lumen pages (OPENED, undated pages):

- "Only meshes with simple interiors can be supported — walls, floors, and ceilings should all be separate meshes. Importing an entire room, which includes furniture, in a single mesh is not expected to work with Lumen."
- "Walls should be no thinner than 10 centimeters (cm) to avoid light leaking."
- Lumen places 12 cards on a mesh by default ("Max Lumen Mesh Cards" raises it). Areas without cards "will not bounce light and will appear black in reflections" (pink in the Surface Cache view).
- "Lumen culls small objects from Lumen Scene for performance." Small emissive meshes are then seen only by screen traces, which "leads to inconsistency in their lighting".
- Emissive light costs nothing extra, "however, there's a limit to how small and bright emissive areas can be before they begin to cause noise".
- "Pay particular attention to the quality of window meshes, these can have a huge impact on the brightness of the room's interior."
- "A mesh that is imported very small and then scaled up on the component will not have sufficient distance field resolution."
- Software ray tracing traces each mesh's distance field for the first two metres, then the merged global distance field.
- High-quality translucency reflections apply to "the frontmost layer of translucent surface materials" and increase GPU cost.

From other sources:

- **MegaLights is production-ready in 5.8** (Guru3D, 18 June 2026, OPENED). It needs hardware ray tracing (SNIPPET; the RX 6700 has it). Not needed for ten rooms with one or two lights each (mine).
- **Lumen Lite, new in 5.8,** is claimed to be up to twice as fast as the High Quality preset (Guru3D, OPENED). Relevant to the frame budget as a whole, not to this choice.
- **Translucency:** only the front translucent layer gets good reflections, and translucent objects are composited late, outside the ray-traced scene (SNIPPET). So the shop glass must be the only translucent layer in the line of sight. Everything behind it stays opaque (the GOODS note's faked jars already follow this).

## 4. Recommendation for our case

### 4.1 The method

**Real rooms for the ten ground-floor shops. Interior mapping stays for the flats above, and as a far fallback.**

1. **Export each Blender room as separate pieces**, in real units (centimetres), never scaled up afterwards:
   - shell: floor, ceiling, back wall, two side walls, each its own mesh, each at least 10 cm thick; the room is closed on all sides but the window;
   - fixtures: counter, shelving runs, chairs, the dryer stack, the buoy, each its own mesh;
   - goods: merged per shelf run (one mesh per run, see section 5), or instanced where repeated.
2. **Use Nanite** for the shell, fixtures and decimated scans. Small goods may stay non-Nanite and instanced.
3. **No collision and no navigation** on anything inside; the glass or a blocking volume stops the player. The room is sealed and never entered.
4. **Light each room inside Unreal, not by the Blender bake:**
   - by day: the sky and sun through the window, plus the tubes if the shop is open;
   - the tubes: an emissive mesh for the visible tube, plus one rect light for the real light (the emissive alone is small and bright and would be noisy);
   - at night: the same rect light, which also spills through the glass onto the pavement;
   - one shadow-casting light per room; any second light without shadows;
   - attenuation radius no bigger than the room, so light stays out of the neighbours.
5. **Front to back:** glass (the only translucent layer, with signwriting and a dirt mask in its own material), window dressing (blinds, curtains, cards: real meshes), the display in the first metre, then the room.
6. **Fallback, mine:** the existing pre-rendered interior images can stay as a far version, shown instead of the room beyond about 25 to 30 m, with a cull distance on the room. On a 42 m street this may never be needed. Decide after measuring.

**A cheaper middle path, if time is short (mine):** real geometry for everything that stands away from the walls (counter, chairs, dryer, buoy, display), and the old picture kept only on the back wall, re-rendered without those objects so they are not doubled. It works because the back wall's contents are flat against the wall, as in the shop that passed. The trap: the picture's baked light must match Lumen's light on the real objects in front of it, in all three states. Full real rooms avoid that, and the rooms are already modelled, so I recommend full rooms.

### 4.2 What it costs (all mine, unmeasured)

- **Geometry.** Ten rooms at about 100,000 to 300,000 triangles each after decimation is 1 to 3 million triangles. Nanite cost follows pixels on screen, not triangles, and the rooms show only through the windows. Expected to be small.
- **Lumen.** Window pixels change from a cheap emissive card to lit opaque surfaces. Lumen's cost per pixel indoors is higher than outdoors (more noise to clean). Expected small at window size, but measure.
- **Lights.** Ten shadow-casting rect lights at night are the largest new item. Measure them one by one at 3440 x 1440.
- **Glass reflections.** Already flagged in NOTE.md; Epic says they add GPU cost.
- **Memory.** Textures dominate, not meshes. One material of three maps is about 13 MB at 2048 and about 3.3 MB at 1024 (block-compressed, with mips). Share one library of materials across all rooms (painted plaster, tiles, lino, wood, enamel), mostly at 1024; give 2048 only to hero goods in the display. Ten rooms on a shared library of about 40 materials plus hero goods is roughly 0.3 to 0.5 GB on disk, of which streaming keeps only the near shops resident. The RX 6700 has 10 GB.
- **Draw calls.** Not a concern with Nanite. Without Nanite, merge goods per shelf run and instance repeats, so each room is a few dozen draws (mine).
- **HLOD and World Partition streaming:** not needed for one 42 m street (mine).

### 4.3 The traps

1. **One merged room mesh.** Epic says it "is not expected to work with Lumen". Black patches, wrong bounce light. Export the pieces separately.
2. **Thin walls and gaps.** Walls under 10 cm leak light, into the street, the flats above and the next shop. Close every corner; overlap the shell pieces slightly.
3. **Thin shelves and small goods.** They may get poor distance fields and self-shadow oddly. Raise the per-mesh distance field resolution on shelves; let tiny goods be culled from the Lumen scene (they are then lit on screen only, which is fine for them).
4. **Small bright emissive tubes** make noise. Real rect lights do the lighting.
5. **Glass behind glass.** Jars, display cases, a glass counter top: no true translucency behind the shop window. Fake them opaque or with a thin additive shell (GOODS note).
6. **Signwriting on the glass** belongs in the glass material, or on a masked mesh, not a second translucent sheet.
7. **Exposure.** By day the rooms will look dark from the street, because the street is far brighter. That is correct. Do not brighten rooms to make them "read"; judge through the game camera (NOTE.md, section 3).
8. **The rooms will look different from the Cycles pictures** the reviewers have seen. They must be judged again from scratch, by the gate, in the game.
9. **Light spill through the glass is wanted at night, and leaks are not.** Check the pavement and the neighbours at night with each light on alone.
10. **Interior mapping, where it stays (the flats):** keep the Fresnel fade at grazing angles, keep the furniture on the walls, and put net curtains or blinds over it.

### 4.4 Order of work (mine)

1. One shop first, the one that failed hardest (the launderette, with the dryer stack). Export, light, put in the street.
2. Measure frame time with the room on and off, day and night, at 3440 x 1440.
3. Gate it: against the Hook sheet and the KCD2 frames, then a fresh reviewer, then his page as whole street frames (CLAUDE.md: nothing is multiplied before one sample is approved).
4. Then the other nine.

## 5. Stock on shelves at 1 to 3 m

**What reads as toy bricks (mine):** one flat colour per block, no print, perfectly square edges, perfect alignment, identical sizes, no contact shadow between items.

**How games do it:**
- **One atlas of labels, many simple shapes.** Kingdom Come: Deliverance II's barrels are "all in one texture atlas using HSL and blendmap variation in weathering and colour" (Tomáš Svojša, ArtStation, 21 February 2025, OPENED from this PC). The same artist's fruit and vegetable bundles start from scans: "Turnip is modified scan" (OPENED).
- A Polycount thread on dense supermarket shelves was UNREACHED (a bot check, which we did not try to pass). Its search summary mentions a shared 2k atlas, grouping items into larger meshes and tint variants (SNIPPET only; nothing rests on it).
- GOODS-2026-10-03.md already covers scans for organic goods, the per-instance atlas tile through custom data, thin real paper for papers and magazines, and faked glass jars.

**The method for our shelves (mine, from the above):**
1. **Shapes.** Tins as 12- to 16-sided cylinders with a rim; packets and boxes as bevelled boxes (a 2 to 3 mm bevel catches the light); jars per the GOODS note. Real 1990 sizes.
2. **One label atlas for the whole street**, about 2048 or 4096 px, 30 to 60 invented 1990 labels: tins of peas, soup and polish; packets of tea and soap powder; tobacco and matches (allowed); no real brands, no alcohol, no gambling, no children in any picture.
3. **Variation per item:** atlas tile, a slight hue and value shift, ±2 to 4 degrees of turn, small gaps, one or two missing or pulled forward, worn edges from a roughness mask.
4. **Merge each shelf run into one mesh** after layout, so a shelf is one draw.
5. **Back and high shelves:** one picture per shelf bay, rendered in Blender from the front, on a card flush with the shelf front. It holds because it is flat and far (4 m or more from the glass).
6. **Organic goods:** scans only (GOODS note).
7. **Contact shadows:** Lumen's screen traces and the shelf's own shadow do this, once the goods are real geometry rather than painted.

## 6. What this could not establish

- How Warhorse treats the rooms behind its window counters in KCD2.
- How Cyberpunk 2077, GTA V, Red Dead Redemption 2 and Hitman show shop interiors.
- The Matrix and Spider-Man 2 talks themselves (only summaries were seen).
- Any measured frame cost for a small lit room behind glass in UE 5.8. Measure it.
- Whether TSR contributes to the streaks (section 1). Test it.

## 7. Flags

- **Money:** none.
- **Licences:** none new. City Sample stays off (NOTE.md).
- **Canon:** none new; labels follow the content rules.
- **Scope:** about one day for the first real room, lit and measured; then perhaps half a day per room, since the rooms already exist (mine). Smaller than the 4 to 6 days NOTE.md gave for the mapped rooms with displays, because most of that work is done.

## Sources (accessed 3 October 2026)

1. Joost van Dongen, "Interior Mapping: rendering real rooms without geometry", blog, 23 September 2018, http://joostdevblog.blogspot.com/2018/09/interior-mapping-real-rooms-without.html, OPENED. Game Developer repost, https://www.gamedeveloper.com/programming/interior-mapping-rendering-real-rooms-without-geometry (Gears of War layers line), SNIPPET.
2. Gareth Harwood (Playground Games), "Game Tech Deep Dive: A window into Playground Games' latest shader development", Game Developer, 10 December 2018, https://www.gamedeveloper.com/design/game-tech-deep-dive-a-window-into-playground-games-latest-shader-development, OPENED.
3. Chris Harper, "Forza Horizon 4: Interior Mapping", ArtStation, 2 March 2019, https://www.artstation.com/artwork/581r9O, OPENED (data record, browser pane on this PC).
4. Nathan Doye, "Forza Horizon 4 - Parallax Interiors", ArtStation, 27 January 2019, https://www.artstation.com/artwork/xzOo4r, OPENED (data record).
5. SCS Software, "Under the Hood: Parallax Interiors", 15 February 2025, https://blog.scssoft.com/2025/02/under-hood-parallax-interiors.html, OPENED.
6. Martin Widdowson, "Interior mapping and building tile-able rooms - UE4", 13 July 2020, https://martinwiddowson.artstation.com/blog/ZP4V/interior-mapping-and-building-tile-able-rooms-ue4, OPENED (browser pane; WebFetch was refused).
7. Epic forum, "Fake 3D geometry with parallax in the Matrix Awakens", 21 May 2022 to 25 August 2023, https://forums.unrealengine.com/t/fake-3d-geometry-wtih-parallax-in-the-matrix-awakens/562469, OPENED.
8. Epic forum, "City Sample: how are the 'Holographic' building windows made?", 13 to 14 January 2023, https://forums.unrealengine.com/t/city-sample-how-are-the-holographic-building-windows-made/748544, OPENED.
9. Epic, "Lumen Technical Details" (UE 5.8 documentation, undated), https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine, OPENED.
10. Epic, "Lumen Global Illumination and Reflections" (UE 5.8 documentation, undated), https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine, OPENED.
11. Guru3D, "Unreal Engine 5.8 Debuts Lumen Lite and Production-Ready MegaLights", 18 June 2026, https://www.guru3d.com/story/unreal-engine-58-debuts-lumen-lite-and-productionready-megalights/, OPENED. MegaLights hardware requirements: search summary only, SNIPPET.
12. Epic forum threads on Lumen and translucent glass, e.g. https://forums.unrealengine.com/t/raytracing-translucency-opaque-glass-interreflection/503648 (2022), SNIPPET.
13. Luca Eliseo, "Kingdom Come: Deliverance 2 - Kutna Hora - City Shops", ArtStation, published 5 March 2025, https://www.artstation.com/artwork/JrgVkR, OPENED (data record, browser pane; WebFetch was refused).
14. Tomáš Svojša, "Kingdom Come: Deliverance II Buildings and Props", ArtStation, published 21 February 2025, https://www.artstation.com/artwork/3EZkZJ, OPENED (data record).
15. Johannes Böhm (Ubisoft Massive), "Trade Secrets of Game City Building in The Division", 80.lv, 28 February 2017, https://80.lv/articles/division-pt-1, OPENED.
16. Watch Dogs: Legion storefronts: Windows Central, https://www.windowscentral.com/watch-dogs-legion-list-clothes-shops-and-easy-places-find-them, and Lilian Chow's "Interactive storefront" breakdown (via Pinterest), SNIPPET only; dates not seen.
17. Marvel's Spider-Man 2: Digital Foundry interview with Mike Fitzgerald, December 2023, via https://www.resetera.com/threads/digital-foundry-inside-marvels-spider-man-2-the-insomniac-games-tech-breakdown.777950/, SNIPPET.
18. Elan Ruskin, "Marvel's Spider-Man: A Technical Postmortem", GDC, March 2019, https://www.gdcvault.com/play/1026496/-Marvel-s-Spider-Man, SNIPPET (not watched).
19. Polycount, "Management of large, open, densly packed supermarket store with hundreds of products", https://polycount.com/discussion/223179, UNREACHED (bot check, not attempted); search summary only.
20. Searches for Cyberpunk 2077, GTA V, Red Dead Redemption 2 and Hitman shop-window methods: nothing technical found (SNIPPET only).
21. Project files: production/research/shop-window-interiors/NOTE.md (1 October 2026), GOODS-2026-10-03.md, FISHMONGER-2026-10-03.md; production/art/shop-rooms/*.json (room sizes, e.g. the chandler at 5.3 x 2.4 x 4.5 m); production/research/unreal-frame-budget/SUMMARY.md.
