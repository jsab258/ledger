Method researched: BRICK-METHODS-2026-10-04.md (method 1), N16-4-TARGET-2026-11-16.md section 1, license-allowlist.md; sources below. All read 16 Nov 2026.

# N16-4 photographic brick reading (16 Nov 2026)

First-pass reading, no synthesis. Tags: **R** read on the page named; **I** inference; **U** unverified. No picture was looked at (the fetch tool returns text), so bond and colour judged "by eye" are all U unless a page states them. Nothing downloaded.

## 0. Licences as read

- Poly Haven: "Our assets are all licensed as CC0"; no credit needed; any purpose incl. commercial. The page says nothing on AI use. https://polyhaven.com/license (R, 16 Nov).
- ambientCG: "Creative Commons CC0 1.0 Universal License"; raw files in a game allowed; credit optional; no AI restriction mentioned. https://docs.ambientcg.com/license/ (R, 16 Nov).
- Fab, Quixel Megascans "Brick Facade": price free; page field "License terms" shows only "-"; page states "Allows usage with AI: Yes". https://www.fab.com/listings/0300d8e5-4ec6-4342-9afe-d2f54cc709e4?lang=en (R, 16 Nov). The allowlist already admits Epic-published Megascans even if NoAI-tagged.
- Poliigon is not on the allowlist; its "old English bond brick wall" page (https://www.poliigon.com/texture/old-english-bond-brick-wall-texture/10102) appeared in a search only and was not opened (not used as evidence).

## 1. Q1: CC0 / allowlisted photographic brick sources

**Finding that matters first:** Poly Haven's whole Clay Brick category (about 70 assets, API list read 16 Nov) has bond sub-categories Running-Bond, Herringbone, Basketweave and Decorative Bond only; no Flemish and no English-bond category exists. ambientCG: no asset tagged "flemish" or "english" among the Bricks entries read (about 40 of the API list; page text was cut, 535 kB unread). (R)  Sources: https://api.polyhaven.com/assets?type=textures&category=brick-block/clay-brick ; https://ambientcg.com/api/v2/full_json?q=bricks&type=Material&limit=100&include=tagData,dimensionsData (offset 100000 chunk).

Bond for every row below is the site's category (Running-Bond) or untagged; whether a given scan is truly stretcher-only or contains headers is U (not seen). BRICK-METHODS (4 Oct) judged brick_wall_006 "Flemish-like, irregular" from a preview (I, not re-checked).

| Name | Link | Licence (R) | Resolution | Stated real size | Bond / colour / condition | Separable bricks |
|---|---|---|---|---|---|---|
| Brick Wall 006 (Jan Burghardt) | https://polyhaven.com/a/brick_wall_006 | CC0 | 1K-8K; 27.3 px/cm at 8K | 3 m wide | Category Running-Bond; tags red, chipped, worn, cracked, discolored, scratched, uneven; "weathered red brick wall with chipped, cracked, uneven bricks ... discolored, scratched mortar" | U (not seen; tags suggest distinct chipped bricks) |
| Church Bricks 02 (Rob Tuytel) | https://polyhaven.com/a/church_bricks_02 | CC0 | 1K-8K; 41 px/cm at 8K | 2 m wide | Running-Bond category; "aged red church bricks, rough chipped faces, irregular mortar joints" | U |
| Red Bricks 04 (Rob Tuytel, 30 Sep 2021) | https://api.polyhaven.com/info/red_bricks_04 | CC0 (site-wide) | 8192 | API dimensions 2500 (mm, I) | Running-Bond; "uneven, baked red bricks, rough surface, worn edges, tidy mortar" | U |
| Brick Wall 001 (Tuytel, Savva, 13 Mar 2021) | https://api.polyhaven.com/info/brick_wall_001 | CC0 | 8192 | API "Scale 1.5x1.5" and dimensions 3000; BRICK-METHODS said 3 m listed, about 1.2 m by courses; conflict, U | Running-Bond; red, "baked-in grime, chipped edges, varied mortar tones" | U |
| Brick 4 (Tuytel, 18 Jun 2018) | https://api.polyhaven.com/info/brick_4 | CC0 | 8192 | API dimensions 500 = 0.5 m (I; TARGET brief says 1.05 m, conflict) | Running-Bond; red, moss, damp, wet | today's scan, already tried |
| Red Bricks 02 | https://api.polyhaven.com/assets?type=textures&category=brick-block/clay-brick | CC0 | 8192 | dimensions 2500 | "rough, broken, red ... crumbling, plaster" | U |
| Church Bricks 03 | same list | CC0 | 8192 | dimensions 1200 | red, uneven, "mortar lines, weathered, crumbling" | U |
| Mixed Brick Wall | same list | CC0 | 8192 | dimensions 1700 | "mixed brick", red, weathered, old | U |
| Worn Brick Wall | same list | CC0 | 8192 | dimensions 2000 | "rough, weathered, old, worn, stained, mortar, mossy" | U |
| Factory Brick, Brown Brick 02, Red Brick 03, Dark Brick Wall, Random Bricks Thick, Brick Wall 07, 12, 13 | same list | CC0 | 8192 | 1000-1900 | tags only (brown, red, rough, old, discolored) | U |
| ambientCG Bricks 094 | https://ambientcg.com/view?id=Bricks094 | CC0 | 8K (JPG 178 MB) | ca. 180 x 90 cm; released 2024-06-05 | Surface photogrammetry; tags brown, dirty, medieval, old, red; bond not stated | U |
| ambientCG Bricks 097 | https://ambientcg.com/view?id=Bricks097 | CC0 | 8K (JPG 199 MB) | not stated | tags brown, red, damaged, dirty, old, factory; bond not stated | U |
| ambientCG Bricks 085 | API list | CC0 | not read | 240 x 120 cm (API) | red, factory, stone, wall | U |
| ambientCG Bricks 092 / 059 / 051 / 071 | API list | CC0 | not read | 110 / 105 / 125 / 145 cm | orange or red, modern or plain tags | U (modern-leaning) |
| ambientCG Bricks 042, 046, 047 | API list | CC0 | not read | size 0 (not stated) | "sloppy", "old", "broken" with mortar tags; 047 orange | U |
| Megascans "Brick Facade" (Quixel, via Fab) | link above | Fab listing; allowlist admits Epic-published Megascans | texel density 8192 px/m | 1 x 1 m scan area | not described beyond "photorealistic brick facade"; bond U | U |

Not found: any CC0 or allowlisted scan stated to be Flemish or English bond. Sketchfab: one candidate, "17th century building scan" (https://sketchfab.com/3d-models/17th-century-building-scan-6093b3299e0845a8a534a6bae5ac5391, Skidoosh, 15.6k triangles, red brick early 1600s): the page text shows no licence, so unverified and not usable as evidence; a 1600s building, not a terrace. No Sketchfab CC0 brick scan was confirmed. A search for free Megascans brick atlases or decals found no listing (the free "Derelict Corridor" sample project is said to hold 34 decals, bond not stated, U).

Not reached for Q1: Fab and Sketchfab search pages (not fetched); ambientCG list pages (empty without scripts; "flemish" search returned nothing renderable); the unread 535 kB of ambientCG API text; pixel-level look at any texture.

## 2. Q2: How professionals build a wall from photographed bricks

Closest primary account found, **not opened**: Matt Taylor, Poliigon bricks on ArtStation (https://matt-taylor.artstation.com/projects/aoDl6z) returned 403. Only a search summary exists (U): fully 3D photo-scanned bricks (scans by Joe Kachnic) arranged procedurally as instances in Designer model graphs into layouts that tile, baked down to a plane; mortar then generated procedurally, and colour and detail variation layered on to hide the repetition of a limited brick set. No brick counts known.

Read in full:
- Adobe Community, "Extracting bricks from I2M to make a larger area?", 6-12 Apr 2024 (https://community.adobe.com/t5/substance-3d-sampler-discussions/extracting-bricks-from-i2m-to-make-a-larger-area/m-p/14541722/highlight/true, read 16 Nov). A user wants to cut about 40 bricks out of an Image-to-Material result across all channels, assign them at random to Brickwall cells, and fix grout continuity with a secondary grout overlay. A community manager (12 Apr) answers there is "no straightforward solution", it would be complicated, and Designer is better suited. (R) One reply was hidden behind "show 1 more".
- Adobe Sampler Brickwall filter (https://experienceleague.adobe.com/en/docs/substance-3d-sampler/using/filters/generators/brickwall, read 16 Nov): breaks the underlying material into bricks and rearranges them; Tile 1-25; Offset 0-1 (row shift); Cement Interstice, Level, Disorder, Color, Roughness (0-1); Brick Disorder (random 3D rotation), Shatter, Edge, Unstuck, Color Variation, Dirtiness (0-1); a Mix Mode adds a second brick set. No stated brick counts; bond limited to its "Brick Bond" setting. (R)
- Material Maker bricks3.mmg (https://github.com/RodZill4/material-maker/blob/master/addons/material_maker/nodes/bricks3.mmg, read 16 Nov): bond enum includes Running, English, Flemish ("each running-bond brick split into thirds"), Herringbone, Basket Weave, Spanish; outputs a bricks pattern, a Brick Fill (per-brick local UV and size) and a Corner Fill; per-brick vec4 holds edge mask, centre UV and an ID (tiled_x + 7 * tiled_y); rows and columns 1-64, mortar 0-0.5, default 0.1. (R) Code licence not re-read here.
- 80.lv, "Creating mortar covered bricks in Substance Designer" (https://80.lv/articles/creating-mortar-covered-bricks-in-substance-designer, read 16 Nov): procedural method; a Tile Sampler makes a mortar-block mask; mortar in two layers (clean top of small squares, damaged noisy middle) blended by a mask, the transition "hardest to get right" because blurred masks look soft; edge damage by Multi-Directional Warp and sharpened distorted Perlin. No numbers, no photo inputs. (R)
- 80.lv, "Breakdown: Clay Bricks in Substance" (https://80.lv/articles/breakdown-clay-bricks-in-substance, read 16 Nov): fully procedural; no Tile Sampler, per-brick variation or edge-wear detail. (R, little use)
- 80.lv "Creating a layered alley wall" (read 16 Nov): no brick content (planks and wire); Tile Sampler places random pieces by seed. Immersion VR "White Brick Wall 01" (https://cgbookcase.com/learn/immersion-vr-substance-designer-material-breakdowns, read 16 Nov): fully procedural Brick Generator, no photo bricks, no numbers. (R, little use)

Tile Sampler documentation: the Adobe pages (helpx and experienceleague URLs) returned 403 or 404, so not read this time. BRICK-METHODS (4 Oct) records it as read then: image inputs picked at random per tile, six at most (R by that note, not re-verified today). A search summary of Adobe community posts also says up to 6 pattern inputs (U, snippet only). A community answer says to colour each input first, then use Tile Sampler Color to get a per-input map (https://community.adobe.com/t5/substance-3d-designer-discussions/extracting-inputs-from-a-tile-sampler-texture/m-p/14582198, R, 16 Nov).

Megascans atlas: Quixel Mixer's atlas layer is a decal layer of scanned assets with three placement modes (Tiling, Freeform, Box Projection), height frequency and channel controls; no numbers (https://docs.quixel.com/mixer/1/en/topic/atlas-layer.html, R, 16 Nov). Nothing read ties it to individual-brick atlases.

Not found: any GDC or ArtStation breakdown that states a brick count for no visible repeat; any published numbers for mortar handling or edge wear from photographed bricks. Search summaries only, not opened: ArtStation projects by Quentin Go (403), Arilehtiniemi, gbaran; Polycount threads (403). Statements from them in the search digest (tiling in Photoshop; Agisoft or Metashape reconstruction; Designer baking) are U.

## 3. Q3: Mortar and weathered-joint textures

- No CC0 texture sold as lime mortar or joint-only was found. Poly Haven "Slumped Mortar Brick" (Dimitrios Savva, published 31 May 2026; 8192; about 1770 mm; tags mortar, loose mortar, cracking, painted, deteriorating; https://api.polyhaven.com/info/slumped_mortar_brick, R) is a painted or rendered brick surface; fit U.
- ambientCG "mortar"-tagged Bricks (size 0 = not stated): 104 (clean, modern, orange), 042 (red, sloppy), 050 (orange, sloppy), 043 (beige), 040 (grey), 046 (old), 047 (broken, old, orange), 049 (dark), 045 (brown), 039, 021, 022, 005, 048 (white) (R tags, https://ambientcg.com/api/v2/full_json?q=mortar&limit=50&include=tagData,dimensionsData,displayData; two of the 16 results cut off). Whether any has recessed grey lime joints is U; each would be a whole brick surface, so the mortar would be cut from it (I).
- Poly Haven descriptions mention mortar: brick_wall_006 "discolored, scratched mortar"; church_bricks_02 "irregular mortar joints"; red_bricks_04 "tidy mortar"; brick_wall_001 "varied mortar tones"; brick_wall_08 tagged "mortar, raw, grey, coarse" (R tags; look not taken). Colour and recess depth U.
- Nothing read gives measured colour or recess for any of these joints.

## 4. Unreached or not used

Adobe Tile Sampler pages (403/404); Matt Taylor ArtStation (403); Quentin Go ArtStation (403); Polycount thread comment 2324366 (403); the 535 kB tail of the ambientCG bricks API list, and the cut-off tail of the Poly Haven list was complete for the clay-brick category but not for the unfiltered list; ambientCG list and search pages (script-only); Fab and Sketchfab search pages (not fetched); Poliigon (off the allowlist, not opened); Adobe community reply hidden in the I2M thread. No cookies, logins or workarounds used; nothing downloaded.
