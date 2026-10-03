> **Helper evidence note** for the pre-production review of 3 October 2026, kept as written by a read-only helper. Corrections found on checking are listed in ../SOURCES.md, "Corrections to the helper notes"; where they differ, the numbered sections govern.

# H4a: the visual areas of LEDGER, where each stands (evidence, 3 October 2026)

Read-only evidence gathering on /home/user/ledger at main 79cf8db (3 October 2026, 10:46 UTC). Nothing in the repository was changed.

## How this was gathered, and its limits

- **Read in full or in the relevant parts:** NOW.md, FINDINGS.md, DECISIONS.md (all 262 lines, 24 September to 3 October), CLOTHES.md, FOR-JAFAR.md, ROADMAP.md, canon.md (visual target), every audit in production/audits/ (the four dated ones, the rulings sweep summary; the two fault reviews are simulation-only and have no visual findings), the research notes named in the brief and others (asset-plan SUMMARY, aaa-street SUMMARY + COMPOSITION-METHOD + SKY-AND-HAZE, shop-window-interiors CLOSE-RANGE + GOODS + FISHMONGER, interior-blockout, third-person-camera-interiors, period-vehicles-and-props, natural-idles, townspeople-animation, lip-sync, metahuman-audio-driven-animation, talking-face-faults, character-pipeline notes, free-garments PC-SUMMARY, voice-latency EVIDENCE, hardware-floor, unreal-frame-budget, evening-light-1990, broken-window-look), the specs that drive the game (unreal-look.json, street-people.json, street-vehicles.json, street-wear.json, garments.json, in-game.json, mickeys-office.json, shop-interiors.json, fab-noai-check-2026-10-03.md), and the game code where a record needed checking (CrimeProbe.cpp, SliceCharacter.cpp, PersonAnim.h, make_cast_metahumans.py, terrace-front.py).
- **Pictures looked at:** production/reference/hook-sheet.png; production/approvals/2026-10-02/street-stage1-day.webp, street-stage1-night-across.webp, rita-square-day.webp (Friday 2 October's page, the latest street frames in git).
- **Git history:** the local clone is shallow (back to 1 October). Commit subjects for 20 to 30 September (1,172 commits, 927 not automatic) were read from GitHub's API, and the full messages of about twenty key commits.
- **Not reachable from here:** anything only on Jafar's PC or drive F: (the 3 October shopfront frames, the two composition reviews of item 2.1, the cast rebuilt without Epic's clothes, the local branch shops-wip-2026-10-03, the town and clothing worktrees, the renders folders), the approval pages' stored answers, and Unreal itself. Where a conclusion depends on those, it says so.

## Cross-cutting facts that bear on every area

1. **The bar and the verdicts so far.** Every whole street frame put to a fresh reviewer or to Jafar since 1 October has failed against the Hook sheet and KCD2. Jafar's "no to all four of Wednesday's looks" (DECISIONS 2026-10-01, line 196) lists: black-void shop windows, crude box cars (one untextured), the hillside as identical boxes by day and black blocks by night, placeholder phone box, skip and pallets, a street too clean, night one flat orange with no pools, a shadow band across the shopfronts, people standing stiffly with arms held out, mouths that only open and close, Sheila's mouth twisting with a seam, clothes that read 2020s. On 2 October stage 1 was "not ready to judge" (line 235); only Rita's shop window got a yes (line 236). The 3 October fresh reviewer's first two faults were "the placeholder hill and a milky road" (commit 6ee0b84).
2. **The gap is art, not engine features** (production/research/aaa-street/SUMMARY.md, 1 October): the "PS5 corner" of 23 September switched every engine feature on and changed 2.4% of pixels at over twice the cost. What is missing is a kit with trims, non-repeating brick, wear, dense dressing and light set by values.
3. **Size of the job, by the project's own estimates (all unmeasured):** the proof view (one camera view, 13 items) 30 to 50 builder-days, "six to ten weeks" (aaa-street SUMMARY); the asset plan's per-family proofs add up separately (below). ROADMAP's friends' build waits on the proof view passing and then the street-wide pass (DECISIONS line 222).
4. **Where the one list stands (NOW.md, 3 October 11:45):** items 1 and 1b done; on item 2.1 (composition) after two failed fresh reviews; by the two-tries rule, research before the third attempt (production/research/aaa-street/COMPOSITION-METHOD-2026-10-03.md, written). Items 2.2 to 2.13 not started as list items, though much of 2.2, 2.3 and 2.12 was worked on 1 to 3 October as "stage 1".
5. **The NoAI ruling of 3 October** (DECISIONS lines 250 to 252, 262; production/specs/fab-noai-check-2026-10-03.md): 42 of 42 Fab listings read "Allows usage with AI: No". Out: 18 Megascans surfaces and decals (asphalt, concrete pavement and slab, two brick walls, leakage, oil, grunge, stains), 15 Megascans goods (fruit, veg, bakes, smoked fish, rope), Epic's Clothing Construction Presets, Epic's Game Animation Sample, and Epic's seven MetaHuman garment packs (the only ones that were actually in the game; 14.5 GB moved to F:/LedgerTools/quarantine-noai-2026-10-03). Reported NoAI from search summaries only and to be read on his PC: Epic's free automotive materials, Megaplants, City Sample, the MetaHuman Crowd Sample. None of the Megascans had ever been downloaded. Still clean: the engine's own MetaHuman plugin (bodies, faces, grooms, its default garment, 31 locomotion clips, the 5.8 crowd tools), Poly Haven and ambientCG (CC0), Sketchfab CC0 items only if each has no NoAI tag, Mixamo, Microsoft Rocketbox (MIT), OFL fonts, Blender.
6. **Open licence item touching every MetaHuman area:** the Unreal/MetaHuman licence forbids MetaHumans being used to train or test AI; the sessions send MetaHuman renders to Claude. Needs you 3 (FOR-JAFAR.md, 3 October) asks him to switch off "Help improve Claude"; DECISIONS line 262 says he "is switching it off". Whether it is off could not be confirmed here.
7. **Graphics memory is already tight.** On 1 October, with the game and the voice both on the RX 6700: the game held 4.8 to 6.1 GB, the card 7.7 to 9.3 GB in use, and the voice was given 1.40 GB of card memory plus 2.03 GB of slower shared memory and crashed in DirectML (production/research/voice-latency/EVIDENCE-2026-10-01.md). Every visual addition below competes with the voice for the same 10 GB until the voice moves to the processor (list item 3, unproven).
8. **The automated street frames show stand-ins, not the cast.** street-people.json (cast_what, 24 September): "the automation's shots keep the stand-ins, so the street's comparison frames do not move". The woman in a striped top at Mickey's window in the 2 October hook frame is the Mixamo "elizabeth" stand-in. The frames judged on his pages are therefore not the people the player meets.
9. **Gate and two-tries rule:** every family goes through the builder's check, a fresh reviewer, then (for people, whole frames and light) Jafar. Many areas below are already past two tries and set aside.

---

## 1. Street and building exteriors, facades

**Exists today.** One street, Quay Street: about 44 m of road, then a climb from 48 m (the gap joined 3 October, c46abaa), generated in Blender by tools/art-recipes/terrace-front.py (8,038 lines) and exported to Unreal; both sides built (east parade of six bays with Mickey's at bay 0, the ship chandler's added 24 September, west_north and west_south terraces). Windows set back 102.5 mm (vignette-scene.json reveal_depth_m). Per-house seeds for brick set, tint and wear (production/specs/street-wear.json, generator tools/street_wear.py). Wear decals since 2 October: streaks under sills, splash, gables weathered, rain wash on every bay, rising damp in the lowest metre, algae at downpipes, soot at stacks (164 marks; commits 1e4a3d8, 86b8fc5). Chimneys, pots, aerials, gutters, downpipes, telegraph wires in the 2 October frame.

**Tried and failed.** The wear layer of D53 ("grime is the strategy", 21 September) was never built until 1 to 2 October, and when it was, every mark had been drawn wrongly since it was added (turned a quarter, printing ambientCG's lit-sphere preview images instead of masks), found and fixed 2 October (1e4a3d8). On 3 October the wash marks were found landing on painted frames and sills as grey "marble" on Rita's approved window; restricted to brick, render and ground (e521a66). The stage 1 frame went to Jafar 2 October and was sent back.

**NoAI dependencies.** The plan to use Megascans leakage, grunge and stain decals, and the Megascans brick walls, is gone; wear comes from ambientCG (16 sets staged) and masks the project makes (tools/make_wear_masks.py).

**Open faults and audit findings.**
- Every bay in the parade is identical: same windows, chimneys and pots (aaa-street SUMMARY, 1 October). Seeds now vary brick and wear, not geometry; proof-view item 2.5 (reveals reading, arch heads, drip sills, sash detail, nets, plinths, varied doors, heights and pots, one stone and one painted house) is not started.
- The reveals exist but do not read: nothing darkens them (aaa-street SUMMARY).
- No trim sheets: "we have only the tiling half" (aaa-street SUMMARY).
- The ship chandler's has no name board (FINDINGS.md).
- D53's own requirements (a wear floor in numbers, coverage printed per surface) are on no list; "THE FLOOR HAS NO NUMBER" (rulings sweep item 13).
- Asset plan: "No free building or building kit fits 1990 Britain" (asset-plan SUMMARY, family 1). Plan: one style kit per building age, three trim sheets, our own brick bond, ~15 to 17 styles for the town, 350 to 500 modules; Quay Street needs four styles. Proof (six facing frontages as two styles of one kit) estimated 6 to 9 builder-days.

**Hard under the constraints.** Everything must be made: no free period kit exists and paid British packs are out of budget. Agents can script the kit and placement (5.8's shape grammar has an Epic "skill designed to guide a LLM", untested here); judging needs the eye, and every frame so far has failed it.

**Reading.** Works: the generator, per-house seeds, a wear layer that now draws. Unproven: a kit with trims and variety (2.5), the wear at a glance that Jafar asked for. Failed: stage 1 as a whole frame (2 October), the identical parade.

**Not determined:** how the 3 October fixes look; no frame after 2 October is in git.

## 2. Shopfronts and the rooms behind the glass

**Exists today.** Rita's (the pawnbroker, east_parade bay 2): a room rendered in Blender from Poly Haven CC0 models (tools/art-recipes/shop-room.py), projected with depth in the window (M_LedgerInterior), a real display of models in the near metre, Thin Translucent glass with Lumen front-layer reflections, a lit window at night with a 350 lm tube light (707b60e, 1 October). Jafar: "yes, the best thing on the page; the other eleven shopfronts are made like it" (DECISIONS line 236, 2 October). The empty unit (bay 3) whitewashed with a TO LET board. Trades for the rest decided 3 October (line 243): fishmonger, launderette, grocer, newsagent-tobacconist, ironmonger, tea room, ship's chandler; Mickey's window to show its office.

**Tried and failed.** Seven more shopfronts built "Rita's way" on 3 October failed three fresh reviews (goods made in code read as toys; then named faults; then what a projected room cannot do at 1 to 2 m) and were set aside under the two-tries rule, kept only on the local branch shops-wip-2026-10-03 (e521a66; FOR-JAFAR Builder 3 October). The research (CLOSE-RANGE-2026-10-03.md) says interior mapping is a distance technique that smears anything standing off the walls; on foot at 1 to 3 m games build real rooms. A real-room pipeline is in the code but "inert until a shop asks for one" (shop-room.py --export-room, tools/ue/import_shop_rooms.py, SpawnShopRoom). List item 2.6 now requires "a real room behind every window in view".

**NoAI dependencies.** The Megascans goods (produce, bakes, rope) planned for the windows are out; Rita's own stock is Poly Haven CC0 and our Blender code (5db99d5).

**Open faults and audits.** Mickey's window is black (Friday's page note); Mickey's two tubes switched off at night until the shop has a room (6ee0b84). The other windows are "still the old flat pictures" (Friday's page). Jafar's 1 October verdict: "the shop windows are black voids". Rita's own shortfalls named on the page: sparse display, room and velvet too clean and evenly lit, soft reflections, unreadable wall notices.

**Hard under the constraints.** Ten real rooms with Lumen-safe walls and night lights, plus glass reflections switched on project-wide, are unmeasured on the 10 GB card (CLOSE-RANGE section 4.2: "all mine, unmeasured"). Goods need scans, and the scan sources are thin after NoAI (area 6).

**Reading.** Works: one window (Rita's) by projection, approved. Unproven: real rooms behind the glass (pipeline exists, never shown), their cost. Failed: seven projected windows with code-made goods (3 October).

**Not determined:** what the seven failed windows look like (frames on F: and the local branch only).

## 3. Interiors (Mickey's office and others in scope)

**Exists today.** A grey blockout of Mickey's office from production/specs/mickeys-office.json (front office with bench and notices, counter with the book and phone, radio desk, staff side, back room merged with the rear lobby to 3.45 m deep on 1 October, WC closet, yard gates, locked stair), built by CrimeProbe.cpp BuildMickeysOffice, with an indoor camera arm. It is built only with the command-line flag -MickeysInside; no launcher, workflow or script passes it (searched). In normal play Mickey's is "a solid block behind its shopfront with a painted card for an inside", and Sheila's office hours are shown on its pavement "until interiors exist" (DECISIONS line 178). Brief: game-design/mickeys-office/BRIEF.md.

**Tried and failed.** The third-person camera in the blockout: at the front door the arm collapses and Tom vanishes, in corners his back fills half the screen, between counter and wall a near wall fills a third of the frame; arm lengths 1.6, 2.0 and 2.4 m made no difference (production/research/third-person-camera-interiors/NOTE.md, 1 October). The note gives an eight-step order; the spec now holds pivot 0.6 m and lift 0, which matches its step 1, but no record of the result was found.

**Scope.** Mickey's office was "kept for later" on 1 October (DECISIONS line 202) and is not on the one list of 3 October. The asset plan puts walk-in interiors (a home, the police station, the tea room, the pub without drink) after the friends' build; Mickey's front office is to be dressed "from the same kit's office set" after a domestic room kit proof (5 to 7 builder-days). No photograph of a 1990 provincial police station interior was found.

**NoAI dependencies.** None specific; furniture would come from Poly Haven CC0 or dimensions.

**Hard under the constraints.** Camera in tight period rooms; the shipped fix (wider doors, roomier rooms) changes the period look and goes to Jafar as a look decision (camera note, "Not recommended" section).

**Reading.** Works: a grey blockout built from data, behind a flag. Unproven: the camera indoors, any dressing, any lighting. Failed: the first camera trial (1 October).

## 4. Ground and materials (brick, flags, wet street, wear)

**Exists today.** Brick drawn per brick with a tone range measured off the Hook sheet, dark joints (terrace-front.py, 22 September), over Poly Haven's brick_4 for large-scale staining; two or three brick sets with per-house tint (street-wear.json). Flags 900 by 600 mm with dark joints, regraded grey-tan on 2 October (they had been orange: their texture was never redrawn after two colour passes). Road: crowned, near-mirror wet floor 0.07 by a fresh reviewer's choice; puddles as decals with an opaque water core after research (production/research/aaa-street/PUDDLES-2026-10-02.md; c46abaa); gutter water in the channel; oil where cars stood; a repair patch. Decals are now Unreal projected decals (the 1 October finding was flat quads 1 cm off the ground).

**Tried and failed.** Mesh water sheets read as "opaque grey polygons and holes" and were retired (DECISIONS line 233). Puddles past two tries before the research. Centre-line dashes floated 8 cm above the road as lit planks (fixed 3 October). Litter drawn in plaster read as white chips (fixed).

**NoAI dependencies.** Megascans asphalt, cracked asphalt, concrete pavement and slab, oil-stain and leakage decals are out. Ground now rests on Poly Haven (asphalt_01, concrete_pavement_02) and ambientCG.

**Open faults.**
- **The brick is laid in stretcher bond** (terrace-front.py line 5672; also the Poly Haven brick_4 pack): a twentieth-century cavity-wall bond, wrong for a Victorian solid wall (asset-plan fault 1). The fix is list item 2.4.
- The brick repeats about every 2 m at the near corner (aaa-street SUMMARY, 1 October); "no repeat at the near corner at 2560 by 1440" is item 2.4's test.
- Friday's page: "the pavements still read as glossy tiles, warmer than the sheet's grey stone; the road's cracks repeat everywhere". The 3 October reviewer: "a milky road".
- Kerbs are not separate blocks with chips; no drain grates, covers, gum, worn lines as a system (item 2.7 not started; plan family 8, 3 to 5 days).

**Reading.** Works: projected decals, a wet road by the researched method, per-house tint. Unproven: our own brick bond (2.4), the ground kit (2.7). Failed: the stretcher bond (a fault in the code), the repeating cracks and tile-like pavement as judged 2 October.

## 5. Props and street clutter

**Exists today.** Nine 1990 pieces made by script and passed by the gate on 29 September (production/art/clutter-2026-09-29/README.md): pillar box, KX100 kiosk, Belisha beacon, bus stop, galvanised dustbin, cannon bollard, telegraph pole with wires, grit bin, litter bin; seven stand in the street (784f41d). Lamp column authored earlier. QUAY STREET name plate in Marcellus SC (a2dc18b, 30 September). Litter as timber and sodden card. About ten props in the hook view against forty or more in the KCD2 arcades frame (aaa-street SUMMARY).

**Removed.** The skip and pallet (Base Mesh CC0 blockouts) came off the street on 2 October under Jafar's "real 1990 things or removed" (DECISIONS line 239); the skip was the "black slab" across Friday's night frame. The fish market's two crates came off 3 October (they hid its window, read blocky).

**Open faults.** The pillar box's cypher and the kiosk's operator mark are owed by canon (they stand plain); the town is to mint names on Monday 5 October (line 255). The kiosk's scene-file size may be the older K6's, not the KX100's (asset-plan fault 6). The dustbin reads as polished aluminium. The 1990 types of grit and litter bin are uncertain. The fish market crate and parked cars walled off the pavement (FINDINGS, 1 October; the cars are now gone).

**NoAI dependencies.** Megascans crates and props were never used; plan is Poly Haven CC0 (crates, drums, buoys, chalk board) plus our own kits.

**Plan and cost.** Item 2.8 (10 to 40 to 60 objects, two to four at every doorway) not started; plan families 4 and 5: about 25 kinds and 30 models of furniture, ~12 containers, soft goods, paper atlases, litter; proofs 4 to 6 days (kerbside run) and 3 to 4 days (fishmonger's pavement).

**Reading.** Works: scripted clutter through the gate (nine pieces). Unproven: dense dressing in three tiers. Failed: the skip, pallets and crates as placeholders (removed).

## 6. Food and shop goods

**Exists today.** Rita's display of Poly Haven CC0 models (vases, jugs, clocks, cameras, frames; production/assets/shop-displays/pawnbroker-display.glb). The grocer's printed labels with made-up makers in OFL fonts (production/assets/shop-goods/labels.jpg, 3 October).

**Tried and failed.** The seven new windows' goods (fish, fruit, cakes, sweet jars, rope) made as shapes in code failed review as "toys beside Rita's scanned stock" (FOR-JAFAR Builder 3 October). The research says photoreal food is scanned (GOODS-2026-10-03.md).

**NoAI dependencies.** The research's main source for fruit, veg, bakes, smoked fish and rope was the free Megascans; all 15 are NoAI and out. Left: Poly Haven CC0 (apple, bananas, lemon, the wrong pear) and ffishAsia's CC0 scans on Sketchfab (cod, mackerel, herring, flatfish, crabs, prawns, apples, pears, mandarins), each to be checked for a NoAI tag at download, needing Jafar's Sketchfab token, which he has given (DECISIONS line 248). No ffishAsia scan has been fetched (none in tools or THIRD-PARTY.md). No allowed source at all for sweets in jars, sou'wester, scones, tomatoes, fillets, dressed crab, crushed ice (GOODS section 0). No dated photograph of a Hull or Grimsby fishmonger 1985 to 1995 was found; Picture Sheffield t13140 and t13138 were looked at (FISHMONGER note).

**Reading.** Works: Rita's non-food stock from CC0. Unproven: scanned food from Sketchfab CC0 (not fetched), the pile generator, printed goods. Failed: goods modelled in code (3 October).

## 7. Signage and text

**Exists today.** Mickey's fascia in plain PT Sans capitals laid by the recipe (terrace-front.py SIGN_OVERRIDE, "fascia_mickeys_plain"); TO LET board in PT Sans; QUAY STREET plate in Marcellus SC; "Telephone" on the kiosk. Rita's, Fish Market and Steam Laundry fascias are still the 3 September image-model batch (ledger/Assets/StreamingAssets/Decals/generated, Z-Image-Turbo, Apache-2.0; asset-plan fault 2, vignette-scene.json lines 680 to 698). OFL fonts held: Marcellus SC, Libre Franklin, League Gothic, Old Standard, UnifrakturMaguntia (production/fonts).

**Open faults.**
- The image-model batch spells badly ("BRITHH WORIKER" on Rita's picture) and includes a bingo poster, a pub darts sheet, a back bar of spirits and a MARQUEE sign, against canon's content rule (asset-plan fault 2). A back-bar picture is still placed in production/specs/vignette-pieces.json line 657, hidden only while the Blender street loads (rulings sweep, "built against a ruling" 12).
- The brand bible still says "MICKEY'S IS A PUB AND STAYS A PUB" (content/brands/brand-bible-v1.json line 11; confirmed here), against canon's minicab office.
- Mickey's is flat PT Sans, not the sheet's gilt capitals (asset-plan fault 4); item 2.6 asks for Marcellus SC gilt.
- No graffiti (QUAY FIRM tag missing), though canon minted the tags on 2 September; the bill of materials still holds G7 "HELD" (asset-plan fault 5).
- No 1990 poster is public domain (Crown copyright runs to 2040): all posters must be our own; poll-tax bills from an invented campaign (line 254).
- Names owed by canon (car makers, police force, bus company, dairy, council, paper, kiosk mark, pillar-box cypher): the town mints them Monday 5 October; placeholders meanwhile.
- Road signs in the period's Transport lettering would need an Open Government Licence ruling (later).

**Reading.** Works: our own text layer in OFL fonts (plates, boards, labels). Unproven: the sign-written and gilt fascias, the poster and fly-post templates. Failed: the image model drawing words (3 September batch), still in the street.

## 8. Vegetation, the hill and distance

**Exists today.** The hill is "stepped boxes" with "blob trees" (Friday's page note; aaa-street SUMMARY: "stepped boxes at the same contrast as the foreground"), its fifth try judged on 24 September. Day haze: fog four to nine times the scene file's density from 25 m, cutoff at 900 m (unreal-look.json, 2 to 3 October). About three in ten hillside windows lit at night (29 September). No weeds, moss, ivy or buddleia in the street.

**Tried and failed.** The hill's mist: two tries (fog cap, height falloff) changed nothing (luma std 73.3/72.8/73.4) and were set aside on 24 September (5b0574a); still in FINDINGS. The 2 October fog changes did make "the far end and the hill fall back" (86b8fc5), so that FINDINGS line may be stale. Jafar on 1 October: "the hillside is identical boxes by day and black blocks by night". His 3 October ruling: "the hill built properly, never hidden in haze" (line 245).

**NoAI dependencies.** Megaplants reported NoAI (search summary only), out. Plan: Poly Haven CC0 plant scans, ambientCG ivy and leaf atlases, Blender's Sapling and IvyGen; the hill from the building kit at lower detail as real geometry (110 to 206 m from the camera; a house there is 55 to 125 pixels wide, so no painted card), then landmarks and cards at 0.5 to 3 km. Estimates: hill 2 to 4 days plus a day of planting; neglect pass 2 to 3 days. Both depend on the building kit (area 1) existing first.

**Reading.** Works: haze that separates near and far (as of 2 October). Unproven: the hill as real kit geometry, any vegetation. Failed: the boxes hill (Jafar 1 October, reviewer 3 October), the two mist tries of 24 September.

## 9. Sky, atmosphere, weather

**Exists today.** A 2 km unlit dome with Poly Haven CC0 overcast sky images (THIRD-PARTY.md, "Skies"), captured in real time as the sky light; dome dimmed and sky light raised by the same factor (6 and 1.25), fog cutoff 900 m, local exposure highlight contrast 0.8, all 2 October (unreal-look.json, per SKY-AND-HAZE-2026-10-02.md). Two lighting states, an overcast wet day and a wet night; the game's clock switches between them in play. Wetness 0.85.

**Tried and failed.** Cloud shapes in the sky: "set aside after two tries; the next direction is known" (Friday's page). The 2 October frame's sky is flat white-grey (looked at). The Hook sheet's sky is also near white, so the bar is a structured overcast, not a dramatic one (item 2.2: "the sky not white").

**Not present.** No rain, no rain particles, no weather change, no dusk state (the evening-light research proposed dusk and night presets; only day and night were found in the code). Chimney smoke (item 2.2) not built. canon.md: "Weather and grime are the strategy".

**NoAI dependencies.** None; the skies are CC0.

**Reading.** Works: overcast light and distance haze. Unproven: clouds in the dome, chimney smoke, any rain or dusk. Failed: cloud structure, two tries.

## 10. Lighting by day and at night; the grade

**Exists today.** Day: soft sun at 0.1 of the scene file, sky light from the dome, fixed exposure by value. Night: low-pressure sodium colour (linear 1.0, 0.25, 0.0), a downward cone of 750 lm per lamp (cut from 1,800 to 1,100 to 750 for burnt-out pools), fog 0.2 of day, sky light 0.15, exposure bias -1 and pin 0.4; pools 9 to 11 stops from pool to gap (Friday's page); Rita's lit window; a third of upstairs nets glowing; shop glass reflecting at 0.2 at night (unreal-look.json). The conversation light on the face being spoken to (28 September; 0.20 to 0.33 ms). Grade: Unreal's filmic tonemapper only; no grain, vignette, LUT, chromatic aberration or depth of field (none in unreal-look.json or the code; rulings sweep item 25, D28 owed). Night and day exposure shared between approval frames and play since 29 September (771de38).

**Tried and failed.** "Night is one flat orange with no pools" (Jafar, 1 October). The night test of 1 October (sky light off, then fog off) found the fog was the orange haze; values changed. Friday's night frame carried a test chart, black squares and a black slab (the skip), which produced his rule that nothing with a visible fault reaches his page (line 238). The quay at the south end is almost black at night, no lamp reaches it (FINDINGS, 30 September).

**Open faults.** A face seen outside a conversation is underlit and reads East Asian in the street's daylight (FINDINGS, 26 September; the conversation light fixes only the face being spoken to). Items 2.12 (night) and 2.13 (grade) not started as list items. The night exposure value is disputed in the research (EV100 3 to 4 against 2 to 3; "a grey card in the game's camera settles it").

**Reading.** Works: the night's pools and gaps by value (as of 2 October), the conversation light, shared exposure. Unproven: the grade, a night that passes a reviewer, daylight that lights faces in passing. Failed: the orange-wash night of 1 October.

## 11. Cars (parked and moving traffic)

**Exists today.** No cars on the street. tools/art-recipes/car-model.py made one generic hatchback (about 15,000 triangles of bevelled boxes, flat colours, no textures, wear or interior); two variants (hatch-navy, hatch-bluegrey) are kept off the street with their places held (production/specs/street-vehicles.json). Part of "crude boxes" was a fault: they drew Nanite's 3,638-triangle stand-in until 1 October (707b60e).

**Rulings.** Jafar 2 October: "no cars is better than box cars" (line 237). Canon: every vehicle fictional; no real model or brand. Item 2.10: one fictional small family hatchback built the whole way, a second by swapping parts, a blind test that no model is named; makers named by the town on Monday.

**Moving traffic.** Ruled in on 23 September (G4: "a street with no traffic feels dead"); the model exists only in the C# Core (Traffic.cs) and the old Unity build, not ported (ROADMAP "Owed to the stages"; rulings sweep item 7). The asset plan puts moving traffic after the friends' build.

**NoAI dependencies.** Epic's free automotive materials (recommended 1 October) reported NoAI, search summary only: out under (A); a car-paint master material must be made.

**Hard under the constraints.** "No free, allowlisted, British period car, van, bus" exists (aaa-street SUMMARY; asset-plan family 3). Paid packs refused (no purchases; partly American). AI 3D generators give melted shells; TRELLIS needs an NVIDIA card. Estimates: proof car 4 to 6 days (asset plan) or 3 to 5 (aaa-street); 4 platforms and ~12 looks for the street-wide pass. The Hook sheet's cars look late-1990s [inference, asset plan].

**Reading.** Works: removing them. Unproven: a fictional car at the bar, the blind test, moving traffic in the game. Failed: the scripted box hatchback (Jafar, 1 October).

## 12. Faces (approved heads; casting sheets still to cast)

**Exists today.** Three MetaHumans, faces approved and frozen: Ron Kirby MH_RoccoP2 (picked 26 September), Sheila Dunn MH_LenaS4 (29 September), Darren Milner MH_SamS6 (30 September; in the game since 2 October, 4d55809). Built by script from plugin presets with landmark moves (tools/ue/make_cast_metahumans.py); Epic's cloud rigging service is a dependency (a 300 s timeout outside the US is noted). Each costs about 0.3 ms and 27 to 43 MB of textures on the card (production/d1-probe/metahuman-cast/ue-mhcost.txt, 24 September).

**Tried and failed.** Sheila's and Darren's faces failed blind reviews through a researched third attempt and four measured passes S1 to S4 (DECISIONS line 81, 28 September); S4 went to Jafar with the reviewer's notes under his "gate stops obvious failures, not imperfection" ruling. Every candidate's eyes came out green (misread eye chart, 26 September). Only three shipped female presets read white European; candidates leaned East Asian (faces-and-hair note). FINDINGS still says "Sheila's and Darren's faces themselves still fail their sheets (eyes green, Sheila's lean East Asian from the front, the haircuts)". The adversarial audit (30 September) called the portrait iteration the wrong method and asked to freeze the heads, which Jafar did.

**Still to cast.** Eleven casting sheets approved as text only on 28 September (Tom Nowak, Carol Ellis, Geoffrey Agar, Maureen Jensen, Danny Cammack, Ada, June Suddaby, Father Walsh, Alison Sedman, Philip Danby, Keith Garbutt), none built. **Tom, the player, is still Mixamo's "Adam" in a grey tracksuit**, a stand-in chosen 23 September (production/archive/DECISIONS-to-2026-09-24.md line 191; SliceCharacter.cpp MeshPath "tom-player"). The thirty regulars (production/casting/regulars/REGULARS.md, approved text) and sixteen crowd faces (CASTING.md) are unbuilt. The untried alternative route is MPFB2 heads (CC0 output) conformed with Mesh to MetaHuman (candidates-2026-09-28/gate.json "next").

**Approvals.** tools/approvals.py, run read-only by the rulings sweep, reported all eight things placed in the game with no current approval (rulings sweep, "built against a ruling" 10).

**Reading.** Works: three approved, frozen heads in the game. Unproven: a face pipeline that passes a reviewer for the next eleven principals, Tom, regulars and crowd. Failed: Sheila's and Darren's faces against their sheets by blind review (accepted by Jafar's eye instead).

## 13. Hair

**Exists today.** Grooms from the MetaHuman plugin's own library (/MetaHumanCharacter/Optional/Grooms), not Fab, so clean under NoAI: Sheila S4 "with the hair it wears", Darren S6 "Epic's short cut", Ron bald with a moustache groom. Colour set by script; MetaHuman grooms expose colour only, no curl (faces-and-hair note).

**Tried and failed.** Curls made in Blender (Sheila's shampoo-and-set) set aside after three attempts, the third after research; "each fails at a glance" (DECISIONS line 129; production/art/hair-2026-09-29). Darren's S4 got "woman's haircut" (line 128). The hair call was then settled by Jafar's picks (line 184).

**Gaps.** Darren's sheet wants a bleached-tip grown-out perm; he has a short library cut. Sheila's set is "the hair it wears", not the research's roller set. The library has no 1990 set or perm (faces-and-hair note); Fab's perms are NoAI and paid. Hair for the other principals, regulars and crowd (perms or sets on half of women over 45 per CASTING.md) has no proven source. The audit of 24 September rated hair "P/—/—/—/E/—/P/P" (inherited presets, no hair pipeline).

**Cost.** Unmeasured for our grooms; research cites "card hair for 50 people took about 800 MB on an 8 GB card" (townspeople-animation).

**Reading.** Works: library grooms on the three. Unproven: period hair for anyone else, strand-versus-card cost. Failed: scripted curls in Blender (three tries).

## 14. Bodies and builds

**Exists today.** Ron, Sheila and Darren's bodies, set by body constraints and re-rigged by Epic's service (the cast script), exported to F:/LedgerTools/bodies (Ron MH_RoccoP2, Sheila MH_LenaS4 with MH_LenaC1's body, Darren MH_SamC5 whose body S6 keeps). Tom: Mixamo Adam.

**Tried and failed.** Three spare 178 cm male builds (slim, average, heavy) for the clothing session came out identical, as the Walter preset's body, three times; set aside 29 September (DECISIONS line 129; research metahuman-builds-2026-09-29.md finds the cause: the export reads the saved body rig unless re-rigged in the same session; the fix needs the cloud rig per build). The clothing session's handovers still name the superseded MH_LenaC1 body in one line (rulings sweep, "built against a ruling" 8).

**Wanted.** Bodies for Tom, then Carol Ellis, Geoffrey Agar and Maureen Jensen (clothing session, Handovers 1 October); none exported.

**Reading.** Works: three cast bodies. Unproven: varied builds for crowds and principals, Tom's body. Failed: the three spare builds (three tries).

## 15. Clothes

**Exists today in the game (by the files, not seen).** After the NoAI ruling the three were rebuilt in the MetaHuman plugin's own default garment (WI_DefaultGarment; make_cast_metahumans.py OUTFITS "plain", 5db99d5). On 24 September that garment was described as "a white T-shirt and shorts", barefoot (da863c1). The script's recolouring applies only to the removed Fab items (cloth_materials looks for MI_WI_OA_). Worn on top, per production/specs/garments.json: Ron's boots and Sheila's handbag only; Sheila's spectacles and chain held (they sit 2 to 3 cm high on S4), Darren's belt and pager held, Ron's jackets and shirt-front held. Sheila's skirt, her blouse and Darren's T-shirt are not in garments.json at all. **The overview (FOR-JAFAR, 3 October 12:15) says the rebuilt cast wear "Sheila's blouse, skirt and handbag, Ron's boots, Darren's T-shirt and belt"; the garments file disagrees, and the blouse and T-shirt were withdrawn by the clothing session on 1 October as failing the bar.** Which is true in the build could not be determined here.

**Tried and failed (since 24 September).** The donkey jacket by script (24 September), as simulated cloth from Ron's skin (three blind reviews, fourteen rounds, set aside 29 September), from FreeSewing patterns sewn in Blender (sleeves failed by two methods), "the game way" (three reviews), MakeHuman's CC0 suit jacket (three reviews; Ron failed on two local breaks, Darren on shape), and the Marvelous Designer proof jacket (failed on the cut and the lapel, 2 October; nine drapes). Darren's lace-up boots (placeholder against the bar), the cardigan, Ron's jumper and work trousers, the flat cap (Jafar: "not like this"), Darren's shell-suit jacket, trainers and jeans, Sheila's shoes: all set aside (CLOTHES.md). The outside clothing review (production/audits/2026-10-02-clothing-plan.md): "parameter search is substituting for garment construction and visual judgement"; it recommended buying one ready-rigged suit (max $40) and a commissioned correction ($75 to $150), which the NoAI screening then ruled out: 247 of 387 Fab suits under $40 NoAI, every rigged one readable NoAI.

**NoAI dependencies.** Epic's seven garment packs were the cast's trousers, jumpers and shoes until 3 October; out. Epic's Clothing Construction Presets: out. Every ready-rigged Fab suit read: out. CGTrader "Royalty Free (no AI)": out.

**Rulings now (3 October).** Clothes are the one exception to the visual bar; the floor is plain, period-plausible, no contrast stitching or trainers, nothing clipping, no holes, nobody frozen stiff (line 249); passers-by judged from 8 m (line 253); tailoring waits "until the tools catch up"; no purchases or commissions. The clothing session is asked for plain trousers and a jumper or shirt for Ron and Darren and plain shoes for Sheila and Darren, from MakeHuman CC0 or Blender (NOW.md Handovers to clothing, 3 October). CLO's free CONNECT patterns cover all ten silhouettes and are licence-allowed, but draping them was stopped on 2 October.

**Measured distances** (production/art/clothing/RUBRIC.md, one walk 2 October): talk at 4.4 m camera-to-face, a jacket about 230 pixels tall; street 3 to 28 m.

**Reading.** Works: accessories and one skirt through blind review; Ron's boots and Sheila's handbag worn. Unproven: anything that clothes the cast to the floor today; a crowd coat. Failed: every tailored garment by six routes, and the stop-gap (Epic's garments) by licence.

## 16. Animation (walking, idles, poses)

**Exists today.** The cast all play the same idle, the MetaHuman plugin's female-template "Technical_Loops" body and face idle (CrimeProbe.cpp kLiveIdles, lines 878 to 890), at each person's own pace 0.92 to 1.08 since 3 October; production/specs/street-people.json still names the old Mixamo "elizabeth" idle (stale; the code comment says it "put the hands through the body"). The head and neck are held 70% to their bind rotation (PersonAnim.h CalmAlpha 0.7), suspected of the rigid look (natural-idles NOTE section 3b). Tom: Mixamo stand, walk and run clips with footsteps timed to them. Three Mixamo stand-ins (Martha, Kate, Leonard); Kate and Leonard pace their pavement in free play at fixed speeds (Leonard 1.5 m/s against his clip's 1.65). People turn toward the smash and, since 2 October, walkers within 35 m go to look for 40 to 110 s (two came in the film).

**Tried and failed.** The plugin's own neutral stand idle was tried and kept off on 3 October: it set Ron and Sheila "wide-legged and braced, a game hero's ready pose" (CrimeProbe.cpp comment; 8c546fe). Jafar 1 October: "people stand stiffly, arms held out". The smoking clip he said was wrongly dropped is still marked rejected; nobody smokes (rulings sweep item 36).

**NoAI dependencies.** Epic's Game Animation Sample (500+ clips at launch, 400 more in 5.7, look-at and bench sitting in 5.8) was the planned source for item 2.11 and the friends' build bar ("natural idles and walks from Epic's free animation sample", line 201). It is NoAI and out (line 252). The replacement named by his ruling: MetaHuman's own movement clips (31 locomotion clips including walk starts and stops, one standing idle already rejected) and Mixamo (uneven quality; "its starts, stops and turns rarely match its walks", townspeople research). The natural-idles research wants 15 to 25 clips per sex (4+ base idles, 8 to 12 breaks, breathing, speaker and listener loops, gestures). UE 5.8's experimental video-to-animation exists but was judged "a lot of work, not now".

**Open items.** Walkers' feet slide (fixed speed); the 0/5/10/20-people measurement and the walkers' feet were ruled on 30 September (line 166) and are on no list (rulings sweep item 17). Women's moves: no separate source confirmed.

**Reading.** Works: one shared technical idle, two pacing walkers, the gathering after a smash. Unproven: a varied idle set from MetaHuman clips and Mixamo, natural walks with planted feet. Failed: the people's stiffness (Jafar, 1 October), the plugin's stand idle (3 October); the planned source lost to NoAI.

## 17. Townspeople and crowds

**Exists today.** In play: Ron, Sheila and Darren as MetaHumans, and three Mixamo stand-ins (Martha, Kate, Leonard) "stylised and out of period" that "jump out at night" (FINDINGS); the night's Michelle is barred from play. The automated street frames still show the six original Mixamo stand-ins (cross-cutting fact 8). The street's people are "seen and not simulated: no collision, no perception, nothing a system reads" (street-people.json), against D25 that everyone perceives, remembers and gossips (rulings sweep item 8). No street voice rides on a cast MetaHuman (FINDINGS). The town's simulation has forty people in its routines (hook-cast.json), most with no body.

**Plan.** Asset plan family 11: 14 principals, ~30 regulars, 30 to 40 passers-by, 10 to 25 on screen; proof "three passers-by from one recipe, older man, out on foot", 8 to 14 days, "the coat being the risk". The 5.8 Crowd plugin and Collections are engine features (clean); the MetaHuman Crowd Sample and City Sample Crowds are reported NoAI (search summary).

**Cost.** Research estimate for twenty people: 1 to 3 ms CPU, 2 to 5 ms GPU, 2 to 3 GB of graphics memory, none measured; "on a 10 GB card everyone must be the game version" (townspeople-animation SUMMARY). Measured: 0.3 ms and 27 to 43 MB a MetaHuman, standing (24 September).

**Reading.** Works: three cast MetaHumans in the street. Unproven: any crowd beyond them, its cost, its clothes. Failed: the Mixamo stand-ins as period people (FINDINGS, Jafar 1 October).

## 18. Mouths and facial animation during speech

**Exists today.** Live replies: a mouth driven by the loudness of the voice, through the face rig's jaw and lip controls (DECISIONS line 134, 30 September; his blind picks on 1 October chose it for thinking sounds, line 192). Prepared lines (thinking sounds, and Sheila's two from 2 October): Epic's MetaHuman Animator faces made offline from the sound, by default since 2 October (V8, 463bc6e; his ruling of 1 October, line 201). Sheila's twisting mouth and cheek seam fixed by holding every idle mouth, jaw, teeth and tongue curve at zero while a line plays (V7, 707b60e; a fresh reviewer found the twist gone); diagnosed in production/research/talking-face-faults/NOTE.md. Subtitles now wait for their sound (4d55809).

**Tried and failed.** Jafar 1 October: "the mouths only open and close with loudness"; Sheila's mouth twisted with a seam. Thinking sounds once froze the mouth driver (fixed c7ab538, 30 September).

**Not tried.** Epic's streaming speech-to-face solver hidden in the 5.8 install (StreamingADA, 81 controls at 50 frames a second, CPU or DirectML) was recommended on 30 September (lip-sync NOTE; metahuman-audio-driven-animation SUMMARY) as the route for live lines; no code or measurement references it (searched). Its cost, packaging and AMD route are unknown. The adversarial audit (30 September): "Amplitude jaws are acceptable placeholders, not completed acting."

**NoAI dependencies.** None; the solver and Animator are engine parts. NVIDIA Audio2Face needs an NVIDIA card.

**Reading.** Works: loudness mouths without the twist; offline-made faces on prepared lines. Unproven: the streaming solver for live replies, eyes and head moving with speech. Failed: the loudness mouth as acting (Jafar, 1 October).

## 19. Performance and graphics memory of the street as it stands

**Measured.**
- The build machine's standing check (3 October, run of 5db99d5): MEETS, median 13.32 ms, p95 15.05, p99 16.73, worst 19.62, 75.1 fps, GPU median 11.43 ms, 3,681 MB GPU memory, at 3440 by 1440 drawn at half resolution and upscaled, standing still (production/d1-probe/ue-perf-verdict.txt; the workflow's comment says the voice is not running in that step, though the file also carries a separate voice line, nanoRtfMedian 1.36; workflow step "sliceperf", which "reports and never turns the run red"). So the rulings sweep's "nothing checks it" (item 26) is contradicted for the standing view; a walking measure with the voice was not found.
- First launch on his screen (30 September, 1d74cf3): Highest 26.4 ms a frame at 3440 by 1440, High 15.1, Medium 7.9; the game now draws Highest at 55% and upscales, 14.1 ms in the editor.
- MetaHumans: about 0.3 ms and 27 to 43 MB each; the street alone 9.3 to 9.5 ms at 1080p; whole game 4.3 to 4.4 GB (24 September).
- With the voice: game 4.8 to 6.1 GB, card 7.7 to 9.3 GB in use; the voice squeezed to 1.4 GB plus 2.03 GB shared and crashed; the voice's loop runs at 12 steps a second beside the game against 80 to 93 idle (1 October, voice-latency EVIDENCE).

**Target.** 60 fps at 3440 by 1440 with the voice running, never below 30 (Jafar, 23 September; ROADMAP).

**What is coming that is unmeasured.** Real shop rooms with lights, Lumen front-layer glass reflections (already on project-wide), the proof view's kit geometry and decals, 40 to 60 props, the hill as real geometry, cars with clear-coat, 10 to 25 people on screen, volumetric fog at night, possibly volumetric clouds (1 to 2 ms on a 3080 Ti, research). The hardware-floor research (19 September, older) put a dense street at about 6 GB and found the three consumers "do not fit" on 9.98 GB; the voice is smaller now (Nano), and list item 3 may move it to the processor.

**Reading.** Works: today's sparse street meets 60 fps standing, at half resolution. Unproven: the street at the bar, walking, with people and the voice, inside 10 GB. Failed: the voice sharing the card with the game (crash, half speed, 1 October).

---

## Table: one line each

| Area | Known to work | Unproven | Failed |
|---|---|---|---|
| Exteriors, facades | generator, per-house seeds, wear that draws | trims, kit variety (2.5) | stage 1 frame (2 Oct); identical parade |
| Shopfronts and rooms | Rita's projected window (his yes) | real rooms, their cost | seven projected windows (3 Oct) |
| Interiors | Mickey's grey blockout behind a flag | indoor camera, dressing | first camera trial (1 Oct) |
| Ground, materials | projected decals, wet road method | own brick bond, ground kit | stretcher bond; repeat; tile-like flags |
| Props, clutter | nine scripted pieces through the gate | dense three-tier dressing | skip, pallets, crates (removed) |
| Food, goods | Rita's CC0 stock | Sketchfab CC0 scans (not fetched) | code-made goods (3 Oct) |
| Signage, text | own text layer in OFL fonts | gilt and sign-written fascias, posters | image-model words still in the street |
| Vegetation, hill | haze separating near and far | hill as kit, any planting | boxes hill; mist tries |
| Sky, weather | overcast light, haze | clouds, smoke, rain, dusk | clouds (two tries) |
| Light, grade | night pools by value; talk light | grade; faces in passing; night pass | orange-wash night (1 Oct) |
| Cars | taking them off | fictional car at the bar; traffic | box hatchback |
| Faces | three frozen heads | next eleven principals; Tom; crowd | Sheila, Darren by blind review |
| Hair | library grooms | period hair for others; cost | Blender curls (three tries) |
| Bodies | three cast bodies | varied builds; Tom | three spare builds |
| Clothes | accessories, skirt; boots and handbag worn | anything to the floor today | every tailored route; Epic's (licence) |
| Animation | one shared technical idle; two walkers | varied idles from MH clips and Mixamo | stiffness; plugin stand idle; GASP lost |
| Townspeople | three cast MetaHumans | any crowd, its cost and clothes | Mixamo stand-ins |
| Mouths | loudness mouth without twist; offline faces | streaming solver for live lines | loudness as acting |
| Performance | 75 fps standing, half res, 3.7 GB | the street at the bar with people and voice | voice sharing the card |

## What could not be determined

- The look of anything made on 3 October (the seven shopfronts, the composition attempts of item 2.1, the stage 1 fixes, the cast rebuilt in the plugin garment): the frames are on F: or the local branch, not in git.
- What the three cast actually wear in today's build: garments.json and the overview disagree.
- Whether the -MickeysInside camera steps were run and with what result.
- Whether Jafar has switched off "Help improve Claude".
- Whether the NoAI status of Epic's automotive materials, Megaplants, City Sample and the MetaHuman Crowd Sample holds (search summaries only).
- GPU and memory cost of real shop rooms, props at density, crowds, cars, the hill, the streaming face solver: none measured.
- Every effort estimate quoted here is the project's own, unmeasured.
