# Study 12: Tech and budgets (25 October 2026)

How Mafia: The Old Country (Unreal 5.4) and Kingdom Come: Deliverance II (CryEngine) hold their frame rate and memory in dense towns, read from their own configuration files. Our own words and numbers only. The raw extracts are on F:/LedgerTools/aaa-study/study-12/. All read 25 October 2026. Where a meaning is read from a setting's name rather than from documentation, it says "by its name".

## Answers

**Quality levels.**
- **Mafia** has four levels (0 to 3) plus a cinematic one; a PC ships at the top level, with GI and reflections a step lower (2). Its auto-detect reads the card's speed and memory, with memory thresholds at 3, 7 and 15 GB. From low to top:
  - world-partition loading ranges ×0.8, 1, 1, 1.5 (distant-detail ranges ×0.75 to 1.5);
  - Nanite's visible-cluster cap 1,048,576 to 2,000,000;
  - texture pool 1,200, 1,500, 2,000, 2,000 MB;
  - a foliage reduction value of 80, 60 and 30, then none: it falls as quality rises, so most likely foliage thinned *by* 80, 60 and 30% (a setting of its own, meaning inferred);
  - the two lower shadow levels use Unreal's many-lights path with Lumen's direct lighting.
- **Mafia's 60 fps console profile**, against the PC default:
  - shadows two levels down (to 1); view distance and textures one down (to 2); reflections one down (to 1); GI unchanged;
  - Nanite's detail bias set to 1.5 (0.5 over its base of 1);
  - TSR at 83% with dynamic resolution between 40 and 83%, aiming at 60 fps.
  - A 10% spare on the card is set in the base console profile; whether the 60 fps profile inherits it is not shown (it names no parent). The PC's Windows profile has dynamic resolution off.
- **Kingdom Come II** has five levels (default 3); its menu's low to ultra specs map to levels 1 to 5 (experimental is also 5). Three of them (low / default / top):
  - view-distance ratio 50 / 100 / 180; detail ratio 10 / 25 / 300;
  - sun cascades 4 / 5 / 5;
  - shadow pool 2,048 / 4,096 / 16,384;
  - lighting voxels 100 / 300 / 700 (by its name, the GI's voxel cap);
  - vegetation ratio 70 / 110 / 250.
  - Shadow-casting lights: at most 10 / 16 / 32, with a budget of 8 per frame (r_ShadowCastingLightsBudgetWH).
- **Kingdom Come II's PS5 performance mode:** 60 fps at 2560×1440 output with FSR at 0.75, view ratio 80, a light budget of 6, no motion blur.

**Mafia's lighting.**
- Software Lumen for GI and reflections: hardware ray tracing is off, distance fields kept.
- Virtual shadow maps with a separate static cache.
- Nanite on, with tessellation; a Nanite streaming pool of 300 MB.
- TSR for anti-aliasing and upscaling.
- **Glass:** Lumen's front-layer reflections on see-through surfaces are allowed only from reflection level 2, the PC default; the 60 fps profile runs reflections at 1, so its glass loses them.
- Epic's own Lumen page puts its top level at about 8 ms for GI and reflections at 1080p internal (the page's context is 30 fps consoles).
- One public test (DSOGaming, 8 August 2025; an RTX 4090 and an RTX 5080; "1440p/Epic Settings", native or upscaled not stated, build not stated): 42 to 51 fps as read; which card gave which figure not re-checked.

**Memory and streaming.**
- **Mafia's** memory and CPU budget files hold no limits, only tag rules: 158 named memory categories, 20 at the top level (character, environment, distant detail, lighting, shaders, world...), and 14 CPU categories (engine, character, AI, gameplay, effects...). Its explicit pools at the top level are textures 2,000 MB, virtual textures 323 MB and Nanite 300 MB.
  - The open world streams through 27,680 runtime cells. Its distant detail is 20,202 files (12,274 packages and 7,928 bulk-data files) in two layers (instanced and merged).
  - Cell size and loading distance in metres are in the encrypted maps, not the config.
- **Kingdom Come II** sizes its texture pool to the card's memory (by its comments): 4,096 MB at 6 GB, 5,120 at 8 GB, 8,192 at 12 GB; PS5 2,240.
  - Its mesh stream pool is 768 MB.
  - Its distant-detail tree (Kuttenberg's region, 6,920 nodes) is not a regular ladder: 8,000 m layer roots, then mixed nodes with median radii of 33 m (depth 2, though a tenth reach 724 m), 181 m (depth 3), 45 m (depth 4, 5,063 nodes, mostly vegetation), 12 m (depth 5) and 6 m (depth 6, mostly interiors).

**Shaders.** Mafia turns on Unreal's pipeline precaching (r.PSOPrecaching, with objects shown only once their shaders are ready, and the driver's cache used). Shader counts were not read.

**How a dense town holds its frame.**
- **Mafia** has a significance system that, by its settings' names, rates each character by distance, visibility and detail level, and slows or stops what does not matter.
  - Animation has a 3 ms budget.
  - By its names, civilians freeze when unseen for 3 s and farther than 70 m, but never within 10 m.
  - Hair casts shadows to half its distance, props to a quarter.
  - Set-piece crowds are vertex-animated meshes with animation sharing.
- **Kingdom Come II**, by its settings' names, keeps at most 70 people in full detail within 150 m (80 within 180 to 220 m at the top levels).
  - Its people's update has a budget of 3.5 ms (2.5 in the PS5 performance mode).
  - Inside Kuttenberg, a "performance-demanding area" setting cuts the local lights' shadow distance by 20 to 30%. Its own Kuttenberg override file has every line commented out. The cut to 6 shadow lights is in the battle overrides.
  - It ships a performance-test quest in Kuttenberg with 1,000 to 2,500 people.

## Budget table, beside LEDGER's targets

| Item | Mafia | Kingdom Come II | LEDGER |
|---|---|---|---|
| Frame | 60 fps profile with dynamic resolution 40 to 83% | 60 fps, 1440p output at 0.75 | median 16.7 ms, worst 25 (33.3 ceiling) |
| Card memory | pools 2,000 + 323 + 300 MB (top level) | 4,096 MB of textures at the 6 GB tier | 6 GB for the game alone |
| Draw distance | loading ranges ×0.8 to 1.5 | view ratio 100 (80 in performance) | not set |
| People | freeze unseen beyond 70 m; 3 ms animation | 70 in full detail within 150 m; 3.5 ms update | not set |
| Shadows and light | virtual shadow maps, software Lumen | cascades; 8 shadow lights a frame (6 in performance) | not set |

3440×1440 is 2.39 times the pixels of 1080p. Matching their roughly 1080p internal resolution means drawing at about 65% per axis (2,236 × 936). LEDGER's packaged walk draws at a fixed 55% (no dynamic resolution).

## For LEDGER

- **Adopt the significance rules for phase 5's town, and for Quay Street once it holds a crowd:**
  - people unseen for 3 s beyond 70 m freeze, never within 10 m;
  - a 3 ms animation budget, and a people-update budget near Kingdom Come II's 3.5 ms;
  - small things stop casting shadows at a fraction of their distance.
  - Our Unreal 5.8 has the Significance Manager and Animation Budget Allocator plugins these rest on (both in its Engine/Plugins/Runtime, checked on disk).
  - Phase 5's load test can borrow Kingdom Come II's idea: a test scene that fills the town with far more people than play needs.
- **Set the numbers LEDGER does not have yet, in phase 2's street budget:**
  - people in full detail (Kingdom Come II's 70 within 150 m is a ceiling far above a street's needs);
  - a draw distance;
  - a shadow-light budget per frame. Kingdom Come II's 8 a frame (6 in its performance mode) is a sane first cap for the street's lamp shadows (our window lamps now cast within 15 m).
- **Texture pool:** Mafia's memory thresholds put a 6 GB card at its texture level 1, a 1,500 MB pool; Kingdom Come II gives 4,096 MB at the same tier. Our 6 GB line for the whole game leaves room for either; 1.5 to 2 GB of textures is the comparable figure for our "High".
- **Lighting:** Mafia ships software Lumen with virtual shadow maps and TSR, the same family as LEDGER. Its 60 fps profile lowers shadows, view, textures and reflections, keeps GI, and gives the upscaler a 40 to 83% range. LEDGER draws at a fixed 55%; a dynamic range with headroom on the card is worth trying once the voice shares it (the accepted 1.7 ms of headroom).
- **Shop glass:** our windows reflect through Lumen's front layer (production/research/shop-glass-reflections). Mafia allows that only from reflection level 2, so any lower quality level of ours turns the shop windows flat; a lower level needs a stand-in reflection for glass. How Mafia makes its glass look is Study 5's.

## Coverage map

Ticked: streaming the open world and budgets, the budget side (both games). The look side stays with Study 5.

## Open blind spots

- Cell sizes and loading distances in metres (in Mafia's encrypted maps).
- Measured frame times in a street for either game (only one public test).
- Mafia's animation budget file (not in the files read).
- Shader counts for either game.

## Sources

- Mafia's config files read through the viewer and saved on F: (aaa-study/mafia/config/): DefaultEngine, DefaultScalability, DefaultDeviceProfiles, DefaultGameUserSettings, DefaultH13MemoryBudget, DefaultH13CpuBudget, DefaultGame. Its class names and name index on F:.
- Kingdom Come II's engine configs (Engine.pak: CVarGroups, spec files, console profiles, per-area and battle overrides, AutoTestChain.cfg) and Study 4's streaming counts.
- Epic's Lumen and virtual shadow map pages for 5.8 (read 25 October). DSOGaming's test of 8 August 2025.
- LEDGER: tools/p1-packaged.ps1 (r.ScreenPercentage=55), production/research/shop-glass-reflections.

## Review

A fresh reviewer (25 October, 21:30) checked 34 numbers against the extracts and 14 against the config files: pass with fixes. Corrected here: the 60 fps profile's levels, Nanite's bias, the foliage reading, the distant-detail count, the Kuttenberg file, the shadow-light figures, LEDGER's fixed draw size, the public test's description, the distant-detail tree's radii, the texture paragraph, the menu names. Removed: "its benchmark turns the AI off" (its test chain sets the AI on). Hedged: readings of setting names. Added: glass, shaders, people's update budget, the performance-test quest.

Cost, from the clock: 20:58 to 21:25 (the helper and this synthesis), the review and its fixes to 21:45.
