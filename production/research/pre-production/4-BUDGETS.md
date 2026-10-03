# 4. Budgets for every kind of asset

Derived from Jafar's target: 60 frames a second at 3440 by 1440 on the RX 6700 (10 GB), with the voice running, never below 30, met by drawing smaller and upscaling (his rulings of 23 and 24 September).

Marks:
- **[M]** measured on his PC and recorded in the repository (the file is named);
- **[R]** read at the source, 3 October 2026;
- **[SS]** search summary only, a lead and not evidence;
- **[I]** this review's inference or estimate.

Every allocation below is **[I] and provisional** until proof P1 (3-PROOFS.md) profiles the hook camera. The budgets are written so that one profile confirms or cuts them.

## 4.1 The target in the build's own terms

`tools/slice-perf.py` already turns the ruling into a test: **MEETS when the median frame is at or under 16.7 ms and the slowest 1% at or under 33.3 ms** [M, the script's verdict rule].

This review plans inside that with a margin:

| Measure | The ruling's line | Planning line [I] | Why the margin |
|---|---|---|---|
| Median frame | 16.7 ms | **16.0 ms** | Today's frame median runs 1.9 ms above the GPU median (13.32 against 11.43 ms) [M]. A 14.0 ms GPU median then lands near 15.9 ms. |
| GPU median | not set | **14.0 ms** | This is the number the asset families share. |
| Slowest 1% | 33.3 ms | **25 ms** | The walk already shows hitches (4.2). A margin is cheaper than a hunt later. |
| Graphics memory, game | not set | **6.0 GB** (Windows' dedicated counter) | See 4.4: the voice needs 2.8 GB of the 9.4 GB usable. |

## 4.2 What is measured today

| What | Number | Conditions | Source |
|---|---|---|---|
| The slice, standing | median 13.32 ms, GPU 11.43 ms, slowest 1% 16.73 ms, worst 19.62, 75.1 fps, 3,681 MB | 3 Oct 12:35; the street, 3 cast MetaHumans, 3 Mixamo stand-ins and the player; 3440×1440 at 50% scale with TSR; off-screen; Nano speaking on the same card | [M] production/d1-probe/ue-perf-verdict.txt |
| The same, 20 runs, 1 to 3 Oct | median 12.7–13.4, GPU 11.2–11.8, slowest 1% 16.1–17.4 ms, 3.6–4.1 GB; one run BELOW-30 (2 Oct 16:15, slowest 1% 67.7 ms, cause not recorded) | as above | [M] H3's history of the verdict |
| Whether the voice ran | yes: the step starts Nano on the card and records `slicePerfVoice=nano-built-in-voice-on-the-card lines=9` | the workflow's comment "The voice is not running here" is stale | [M] .github/workflows/ledger-probe-unreal.yml, step "Time the slice", read here |
| Full resolution, packaged, 30 Sep | Epic 26.3 ms, High 15.1 ms, Medium 7.9 ms | 3440×1440 at 100% | [M] TitleScreen.cpp comments |
| One MetaHuman at 3.5 m | +0.31 to +0.36 ms GPU, +27 to +43 MB textures; all three +0.63 ms | run date and resolution not recorded | [M] production/d1-probe/metahuman-cast/ue-mhcost.txt |
| Day against night | day 8.1–9.1 ms, wet night 10.2–10.7 ms | 1280×720 | [M] ue-vignette-verdict.txt |
| Voice beside the game, 24 Sep | 11.8 ms without, 12.5 ms with (median), slowest 1% 16.0 | 3440×1440 at 50% | [M] production/research/nano-listening-test/card-timing-2026-09-24.md |
| Walking | median 6.89 ms, worst 88.21 ms, **23 of 847 frames over 33 ms** | 960×540; the probe takes screenshots during the walk, which may cause the hitches | [M] production/d1-probe/ue-walk-verdict.txt, read here |
| Memory, 1 Oct | game 4.8–6.1 GB; card 7.7–9.3 GB in use; the voice got 1.4 GB plus 2.03 GB shared and crashed | packaged game beside the AI tester | [M] production/research/voice-latency/EVIDENCE-2026-10-01.md |
| Memory, the voice alone | 2.7–2.8 GB dedicated | Chatterbox Nano on DirectML | [M] same |
| A 600 MB texture pool | the voice ran three times faster (35 against 12 tokens a second) | 2 Oct | [M] same |
| Usable card memory | about 9.4 GB | 24 Sep | [M] card-timing note |

**Not measured anywhere:**
- a per-pass breakdown (Lumen, shadows, base pass, translucency, TSR);
- draw calls or triangles in frame;
- the hook camera;
- shop rooms, night with lit windows, cloth, cars, moving crowds;
- the cast voice server, as opposed to Nano's built-in voice;
- system memory.

## 4.3 Three facts that shape every budget

1. **Nanite and virtual shadows are off.** Every mesh under /Game/Ledger has Nanite switched off (`tools/ue/nanite_audit.py`, "naniteAuditOn=0"), and the probe prints `cvarVirtualShadows=0` [M]. So every triangle is drawn in the base pass and again into each shadow cascade, and every mesh needs a level-of-detail chain. **The asset plan and the street research assume Nanite buildings and car bodies, and virtual shadows** (asset-plan notes 1 and 2; aaa-street). The two cannot both stand. Proof P1 settles it by measuring the same frame both ways. The tables below are written for **Nanite off**, today's state. If P1 turns Nanite on, triangle caps for static meshes relax and the per-family memory rises (4.6).
2. **The voice shares the card.** It needs 2.7–2.8 GB to run at speed and loses two-thirds of its speed beside the game [M]. Until list item 3 moves it, every budget here reserves its memory and some GPU time for it.
3. **The sparse street already uses most of the frame.** The GPU median is 11.4 ms with six people and almost no dressing [M]. The planning line is 14.0 ms. That leaves **2.6 ms** for everything the proof view adds, unless a lever pays for more (4.5).

## 4.4 The memory envelope (graphics card)

| Share | GB | Basis |
|---|---|---|
| Usable on the card | 9.4 | [M] |
| The voice, reserved while it runs on the card | 2.8 | [M] alone 2.7–2.8 |
| Margin for the driver, fragmentation and spikes | 0.6 | [I] |
| **The game** | **6.0** | the rest; today 3.6–4.1 GB by the engine's counter, 4.8–6.1 GB by Windows' [M] |

The game's 6.0 GB, by kind [I]:

| Kind | GB | Note |
|---|---|---|
| Engine and render targets at 3440×1440 output (TSR history, GBuffer at the internal size, Lumen caches, shadow maps) | 1.6 | to be read off `memreport -full` in P1 |
| Textures: a **fixed** streaming pool of 1,500 MB plus non-streamed textures | 2.4 | today's texture memory is already 2.38–2.43 GB with a sparse street [M]. Without a fixed pool, textures crowd out the voice [M]. |
| Static meshes with their LODs | 0.6 | Nanite off |
| Skinned meshes, MetaHumans, grooms, clothes | 0.5 | |
| Lumen scene and distance fields | 0.3 | |
| Audio, interface, physics, slack | 0.6 | |

Texture memory is the binding limit [I]. Twelve shop rooms, a kit's trim sheets, props, cars and more people all arrive inside the same 2.4 GB. The per-asset texture caps in 4.7 are set so that the families fit it.

**When the voice leaves the card** (list item 3), the game's envelope rises to about 8.4 GB. Only then should any family's texture cap be raised.

System memory: the PC has 32 GB (production/research/hardware-floor/SUMMARY.md). Planning line [I]: game at most 12 GB, voice and talk helper at most 5 GB. **Never measured** (H3); P1 reads it.

## 4.5 The frame-time envelope (GPU, hook camera, walking, by day)

| Share | GPU ms [I] | Basis |
|---|---|---|
| The lit, fogged, upscaled frame with the street's shell: sky, Lumen lighting and reflections, fog, cascaded shadows, TSR, post-process with the owed grade | **7.5** | today's equivalent is about 9.5 ms [I]: 11.4 measured, less about 0.9 for the three MetaHumans, 0.3 for the stand-ins and 0.7 for the voice [M] |
| Building detail beyond today: trims, reveals, kit variety, wear decals | 1.0 | |
| Shop rooms and glass: real rooms where seen at 1–3 m, mapped rooms elsewhere, front-layer reflections | 0.8 | |
| Props, food, signage: 40 to 60 objects in view | 0.7 | |
| The hill and distance, as merged geometry | 0.4 | |
| Parked cars, at most six in view | 0.5 | |
| People: up to three principals near (1.0 ms), up to twelve passers-by at distance (0.7 ms) | 1.7 | 0.31–0.36 ms per MetaHuman at 3.5 m [M] |
| Clothes and cloth on the GPU (skinning; the simulation is on the processor) | 0.2 | |
| Reserve: the voice, night's lamps, spikes | 1.2 | the voice added 0.7 ms on 24 Sep [M]; night adds about 1.5 ms at 720p [M] |
| **Total** | **14.0** | |

**The base share does not fit today.** It is 7.5 ms against about 9.5. Three levers can pay for it, and P1 measures each:

| Lever | What it saves | Status |
|---|---|---|
| Scalability Epic to High | at full resolution 26.3 to 15.1 ms [M]. Epic says Epic quality targets 30 fps and High 60 fps on consoles [R, Lumen performance guide]. The street research found the "every feature on" corner changed 2.4% of pixels at over twice the cost (aaa-street/SUMMARY.md). | at 50% scale, unmeasured |
| The voice off the card (list item 3) | about 0.7 ms GPU, 2.8 GB of memory | the delay moves to the processor; see risk R2 |
| Nanite on static meshes, with or without virtual shadows | unknown, either way. Epic: non-Nanite geometry is "much more expensive" in virtual shadows [R]; virtual shadows themselves cost more than cascades | unmeasured |

**If none of the three pays,** every family's share shrinks to fit 2.6 ms. Then the proof view's dressing has to be cut, or the render scale lowered below 50%, which the ruling's "drawing smaller" allows and the look may not.

At night, the people share drops (fewer passers-by) and the lamps come out of the reserve. **At most six shadow-casting lights in view [I]**: lit windows are emissive and cast no shadow.

## 4.6 Processor (Ryzen 5 5600X, 6 cores, 12 threads)

- Today the frame is GPU-bound: the frame median is only 1.9 ms over the GPU median [M].
- **Planning lines [I]:**
  - game thread at most 8 ms and render thread at most 8 ms;
  - animation inside the engine's Animation Budget Allocator (default 1.0 ms of game thread) [SS via the repository];
  - the town's simulation ticked by distance: 0.07 ms a person a frame was measured in Unity, not here [M, old];
  - cloth only on loose parts, on at most two people in view.
- **The risk:** list item 3 moves the voice's decoder onto the processor. Four cores gave first sound in 4.40 s [M]. Four of six cores busy while a character speaks leaves the game two. **Nobody has measured the game's frame with the voice on the processor.** It is proof P2.

## 4.7 Per-asset budgets

### What the screen can show (derived from the target)

The game camera uses the engine's default field of view, 90 degrees across: `SliceCharacter.cpp` sets no field of view, and its arm is 320 cm (read here). The project sets no aspect-ratio axis rule (ue-probe/Config and Source searched). The engine's default is taken to hold the horizontal angle at 21:9 [I; BaseEngine.ini not read here]. If it held the vertical angle instead, the view would be wider and every density below would fall by about a quarter [I]. At 3440 pixels across, a surface at distance d metres spans about **1720 ÷ d pixels per metre** of output [I, geometry]. TSR rebuilds toward the output size, so textures are sized to the output, not to the 50% internal frame.

| Distance | Output pixels per metre | Texture density that is enough |
|---|---|---|
| 1 m (a shopfront Tom stands at) | 1,720 | 1,024 px/m, with a detail normal |
| 2 m | 860 | 1,024 px/m |
| 3.2 m (Tom's back, the camera arm) | 538 | 512 px/m |
| 5 m | 344 | 512 px/m |
| 10 m | 172 | 256 px/m |
| 25 m | 69 | 128 px/m |
| 110–206 m (the hill) | 8–16 | 16 px/m |

So: **512 px/m for street surfaces, 1,024 px/m for what is read at arm's length** (shopfronts, doors, signs, goods), and the hill at 16 px/m. A 2048² tiling texture covers 4 m at 512 px/m.

Memory per texture [I, from Epic's figures of 4 and 8 bits a pixel, R]: a 2048² colour (BC7), normal (BC5) and packed mask (BC1) set with mips is about **14 MB**. A 1024² set is about 3.5 MB.

### Budgets by kind (Nanite off; LOD0 triangles; each LOD about half the last, Epic's rule [R])

| Kind | LOD0 triangles | LODs | Materials (each a draw per pass) | Textures | Memory per unique asset | In view (hook camera) | GPU share | Collision | Today's reference [M] |
|---|---|---|---|---|---|---|---|---|---|
| **Building module** (a window bay, a door, a shopfront bay) | ≤ 8,000 | 3, then the merged distance version | ≤ 4, from the shared trim sheets | none of its own: three shared 4096×2048 trim sheets at 1,024 px/m, tiling sets at 2048² (512 px/m) | ≤ 1 MB geometry | | inside 7.5 + 1.0 ms | simple boxes for walls, plinths, steps; none per brick | the whole street is 183,416 triangles over 112 meshes |
| **A whole frontage** (one house or shop, with chimneys, gutters, pipes) | ≤ 150,000 | as its modules | ≤ 12 across its modules | shared | | about 6 near frontages | | | |
| **Hill house** (110–206 m away) | ≤ 2,000; rows merged | 1 merged distance version per row | 1, the kit's atlas | 256–512 px a face | small | dozens | 0.4 ms in all | none | the hill today is boxes |
| **Mapped room** (behind upper and far windows) | 2 (one card) | none | 1 | one 2048² room atlas or cube | ≤ 12 MB | many | inside 0.8 ms | none | Rita's projected room |
| **Real room behind glass** (seen at 1–3 m) | ≤ 100,000 | 2 | ≤ 12, shared finishes | ≤ 40 MB | ≤ 40 MB | at most 4 at once | inside 0.8 ms | none (not entered) | the pipeline exists, never measured |
| **A window display** (the goods in the near metre) | ≤ 60,000 | 2 | **≤ 8** | an atlas, ≤ 2048² | ≤ 20 MB | 1–3 | | none | **the pawnbroker's display: 203,355 triangles, 48 materials, 83 textures**: 3, 6 and 10 times over. Merge it to an atlas first. |
| **Small prop** (under 0.5 m: litter, a paper, a cup) | ≤ 1,500 | 2 | ≤ 2 | 512² | ≤ 1 MB | instanced, hundreds | inside 0.7 ms | none, or one box | |
| **Medium prop** (0.5–2 m: bin, crate, A-board, bollard) | ≤ 5,000 | 3 | ≤ 3 | 1024², or a shared trim | ≤ 4 MB | 20–40 | | ≤ 10 convex hulls [R, Epic]; most one box | clutter 950–7,548 each |
| **Large prop** (the kiosk, the bus stop, the pillar box) | ≤ 15,000 | 3 | ≤ 4 | 2048² or the shared trim | ≤ 14 MB | 3–6 | | ≤ 10 hulls; the camera blocked by it | |
| **Food** (one piece of a pile) | ≤ 2,000 (a scan cut down) | 2 | 1 | 512²–1024² | ≤ 3.5 MB per kind | piles by instancing, ≤ 30,000 a slab | | none | none fetched yet |
| **Sign, poster, fly-post** | a plane or a decal | none | 1, from a template | our own text at 1,024 px/m; posters in a shared atlas | ≤ 4 MB per atlas page | 20–40 | | none | |
| **Parked car** | ≤ 40,000, with wheels and a simple interior | 4 | ≤ 8: one car-paint master (colour from data), glass, trim, lamps, tyres, interior, plate, underside | 2048² for trims and lamps, 1024² interior; plates as decals | ≤ 20 MB per platform | ≤ 6 | 0.5 ms in all | one box and the wheel arches, ≤ 6 hulls | the scripted hatchback: 15,294 triangles, 9 materials, kept off the street |
| **Principal person** (Tom; whoever he talks to) | MetaHuman, Optimized, High: head 24,000 vertices and body 30,500 at LOD0 [R, Epic's LOD table] | the MetaHuman's own 8 head and 4 body LODs | MetaHuman's own | 2K maximum (Optimized) [R] | ≤ 100 MB (Optimized) [R]; measured 27–43 MB of textures [M] | ≤ 3 near | ≤ 0.35 ms each [M] | capsule | Ron, Sheila, Darren |
| **Passer-by and regular** | MetaHuman at LOD ≥ 2 beyond 5 m; the 5.8 crowd tools' instanced meshes far [R, Epic] | as above | MetaHuman's own | 1K | ≤ 50 MB [I] | ≤ 12 | ≤ 0.06 ms each [I] | capsule | the Mixamo stand-ins: 48–59k triangles, 1K textures |
| **Hair** | strands only on two people within 5 m; cards beyond (`r.HairStrands.UseCardsInsteadOfStrands` for crowds) [R, Epic] | the groom's own | | | ≤ 16 MB per card groom [SS] | | inside people | none | the plugin's library grooms |
| **Principal's outfit** | ≤ 25,000 across all garments | follows the body's 4 LODs | ≤ 3 | 2048² tiling cloth with 1024² masks | ≤ 15 MB | ≤ 3 | inside people | none; the body's capsule | none passes the floor today |
| **Crowd outfit** (judged at 8 m) | ≤ 8,000 | 3 | 1 | 1024² | ≤ 4 MB | ≤ 12 | inside people | none | |
| **Cloth simulation** | loose parts only (coat tails, a skirt hem), ≤ 300 simulated points a garment [SS, forum: about 0.35 ms each] | | | | | at most 2 garments in view | processor | | never measured |
| **Accessory** (bag, hat, spectacles, watch) | 500–4,000 (the asset plan's estimates) | 2 | 1 | 512² | ≤ 1 MB | | | none | four passed blind review |
| **Weed, ivy, buddleia** | ≤ 1,000 a clump; masked leaves kept small on screen | 2 | 1, from one 2048² atlas | | ≤ 14 MB for the atlas | dozens | inside building detail | none | none in the street |

In-view totals [I], to be checked in P1:
- **at most 3 million triangles at LOD0-equivalent**, about four times today;
- **at most 2,000 mesh sections** (mesh × material) before instancing.

There is no reachable primary source for a PC draw-call ceiling [SS only]. Epic's only number is for tablets [R].

## 4.8 How the budgets are policed

A budget nobody checks is a wish. Three cheap checks, in the order they pay:

1. **The perf step at the hook camera, walking, with the cast voice server.** Keep the slice step. Add the proof view's camera and a 30-second walk, and log GPU median, slowest 1%, graphics memory and system memory per run, as the slice already does. Today only the standing slice is timed [M].
2. **An asset audit script.** Read every placed mesh's triangles, LOD count, material count and texture sizes against this table and print the over-budget list. It follows the pattern of `tools/ue/nanite_audit.py`. Epic's Data Validation can do the same on save and in the build [R].
3. **One capture per milestone.** `ProfileGPU` and `memreport -full` at the hook camera, day and night. The allocations in 4.4 and 4.5 are then revised from it, not from this page.

## 4.9 What could not be verified

- **Every allocation in 4.4 and 4.5** is this review's [I]. No per-pass profile exists.
- **The cost of High against Epic at 50% scale.** Only full-resolution figures exist.
- **The per-MetaHuman figure's resolution and date** (not recorded in the file).
- **The cause of the walk's hitches** (screenshots or streaming).
- **The cause of the 2 October BELOW-30 run.**
- **Every third-party benchmark** for the RX 6700 class: the hardware sites were UNREACHED, and the snippets are not evidence.
- **Triangles for MetaHumans.** Epic gives vertices only.
- **Shop rooms, garments and the current MetaHumans** are not in git, so they were not counted.
- **Cloth, hair-strand and draw-call figures** are forum or search-summary only.
