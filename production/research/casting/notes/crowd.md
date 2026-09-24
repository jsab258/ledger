# Crowd variety from few bases: techniques, perception, cost (research notes, 2026-09-24)

Question: how games make a crowd of hundreds from a small set of faces and bodies without clones, and what it costs; target UE 5.8 + MetaHumans, a 1990 British port-town street, 200-500 people.

Labels: **OPENED** = page or PDF read directly; **SNIPPET** = only search-engine summary seen; **MEASURED** = a number someone measured; **CLAIM** = a statement or marketing figure. Nothing downloaded to the repo. Two PDFs (Clone Attack, Hitman slides) were fetched by the web tool into its cache and turned into text in the scratchpad only, to be read.

---

## 1. Perception science: what the eye catches

**McDonnell, Larkin, Dobbyn, Collins, O'Sullivan, "Clone Attack! Perception of Crowd Variety", SIGGRAPH 2008 / ACM TOG 27(3).** https://www.scss.tcd.ie/rachel.mcdonnell/papers/Siggraph08.pdf (OPENED, full text)
- Setup: 20 template models (6 F, 14 M, young/middle/elderly, formal/casual), 20 mocap walks; 32-36 colour "outfits" per model made by HSV tinting of body-part regions via an alpha mask. Crowds of 20 foreground characters. They call 20 templates "a reasonably conservative estimate of the number of foreground characters clearly visible", and say real-time systems then typically used 3-10 templates. (CLAIM for the 3-10; setup is fact)
- MEASURED: time to find one exact appearance clone pair among 12 = 5.7 s; with colour tinting = 12.3 s. Colour tint more than doubles time-to-spot.
- MEASURED: near clones found in ~7 s, far in ~10 s; side-by-side (horizontal) pairs found fastest.
- MEASURED: motion clones (same walk on a plain mannequin, in step) took ~18 s among six, ~28 s average in the multiple-clone test: motion clones are far harder to spot than appearance clones.
- MEASURED: one appearance clone static = 13 s to find; same with motion = 27 s. Random facing direction makes clones harder to find. Playing cloned walks **out of step** hides appearance clones; giving every clone a *different random* walk was **no better** than out-of-step characteristic walk, so "adding random motion would not warrant the extra storage and motion capture time".
- MEASURED: motion clones were **not** disguised by varied appearance (same detection time on mannequins and on varied models).
- MEASURED: false positives came from **clothing**: two different men in suits, two in checked shirts, three women in jeans were confused as clones "even though their faces and bodies were very different". Outfit silhouette/pattern reads before face.
- Threshold table (their Table 2, for a crowd of 20, clones not noticed within exposure time): 5 s → 8 appearance clones / 10 motion clones; 10 s → 4 / 10; 15 s → 2 / 9; 20 s → none / 7. (MEASURED, lab conditions)
- Future-work note: at a distance motion may dominate over appearance (CLAIM/hypothesis).

**McDonnell, Larkin, Hernández, Rudomin, O'Sullivan, "Eye-catching Crowds: Saliency based Selective Variation", ACM TOG 28(3) 2009.** https://www.researchgate.net/publication/231181066 (SNIPPET only; ResearchGate and academia.edu refused, 403)
- Eye-tracking: head and upper torso get most first fixations and most attention regardless of orientation, motion, sex, age, size, clothing; legs almost never looked at. (MEASURED per abstract)
- Head accessories, top (shirt/jacket) texture and face texture variation were **equally effective**; facial **geometry** alteration was **less** effective. Selective colour variation (only salient parts) as effective as full colour variation. (MEASURED per abstract)

**Vyas & O'Sullivan, "Shape Shifters: Does Body Shape Change the Perception of Small-Scale Crowd Motions?", arXiv 2412.16151, 2024-12-20.** https://pith.science/paper/2412.16151 (OPENED, summary page)
- 12-avatar crowds, 1/3/6/12 body shapes x 1/2/3/6 motions, 22 participants. Body-shape variety did **not** help hide motion clones (p=0.70); motion variety did (p=0.046, marginal). (MEASURED, small study)

Takeaway: spend variety on **head, hair, headwear, and upper-body clothing colour/pattern**; face geometry matters less than people assume; body shape does not hide repeated walks; walks need their own variety plus phase offsets.

---

## 2. Shipped and published examples

**Hitman: Absolution (IO Interactive), GDC 2012, Kasper Fauerby, "Crowds in Hitman: Absolution".** https://media.gdcvault.com/gdc2012/slides/Programming%20Track/Fauerby_Kasper_CrowdsInHitman.pdf (OPENED, slides)
- ~1200 agents per crowd, 500 on screen, PS3, 30 fps (CLAIM of design goal; perf figures below are MEASURED on their build).
- PS3 cost at 1200 simulated / 500 visible: PPU 5 ms (anim ~2, AI ~2, framework ~1), SPU ~20 ms spread across SPUs, GPU 8 ms (vertex skinning the limit). Agent core 36 bytes; 1200 cores = 42 KB. (MEASURED)
- Visual variety, verbatim ideas: a **unique scale factor per agent, ~5%**, which "does wonders for perceived diversity"; **diffuse texture overrides** ("red shirt, yellow shirt"). No head/outfit counts given.
- Animation: first try = shared looping clips; looked "robotic" and "synchronized", so they added multiple loops per animation started at random times; final = motion-matching-style animation-driven locomotion, unique pose per visible agent. Upper-body overlay acts (cough, wave), and "crowd acts" (phone, smoking, sitting on bench) spawned near the player by upgrading an agent to a full NPC.
- Hitman 3 "up to 300 NPCs in a location": SNIPPET from search, source unverified (CLAIM).

**Assassin's Creed Unity (Ubisoft), GDC 2015, François Cournoyer, "Massive Crowd on Assassin's Creed Unity: AI Recycling".** https://archive.org/stream/GDC2015Cournoyer/GDC2015-Cournoyer_djvu.txt (OPENED, OCR of slides)
- Three tiers: low-res "bulk" >40 m, no entity, ~1700-2000 polys, hardware-instanced; "puppet" 12-40 m, real NPC mesh, most components off; "autonomous" <12 m, everything on, **max 40**. (MEASURED/design facts)
- Low-res crowd: **29 different meshes**, up to 1700 polys each, 300,000-poly total limit. Full NPCs: "infinite permutations", up to 20,000 polys, 300 bones.
- CPU per bulk: low-res ~25 µs, puppet ~150 µs. Pool: 160 spawned, 90 active. Memory: **230 MB for 2000 bulks vs 4.2 GB** without the system; +620 MB for 12,000. (MEASURED)
- Swapping low-res to real: find best-matching entity, **reapply colour**, **match hats and props**; "all hats spawned on real"; a colour-matching tool was used by character modellers because the two shaders differed; "less models means better matching". Crowd composition statistically based on the region.
- Headline: 10,000 on screen with 40 real AIs and 120 high-res models (SNIPPET, gamedeveloper.com / GDC Vault description, CLAIM).

**The Matrix Awakens / City Sample (Epic, Dec 2021; City Sample released Apr 2022).**
- 35,000 simulated MetaHuman pedestrians in the city. https://www.fxguide.com/fxfeatured/the-matrix-is-unreal/ 2021-12-09 (OPENED; CLAIM). "The ones nearest to us are actual metahumans and then out in the distance, they are actually vertex animated static meshes generated from the metahumans."
- Epic doc: "thousands of unique digital human characters adapted from a subset of MetaHumans and accessories"; near = full rigged MetaHumans, far = custom vertex-animated static meshes; Mass AI + StateTree. https://dev.epicgames.com/documentation/unreal-engine/city-sample-project-unreal-engine-demonstration (OPENED, 5.8 docs; CLAIM, no counts)
- **The actual kit** (Vrealmatic breakdown of the City Sample Crowds content, 2023-10-24): https://vrealmatic.com/unreal-engine/city-sample/crowd (OPENED; third party reading the project, treat as fact about the assets)
  - 2 skeletons (male/female) x 3 weights (Normal/Over/Under) = **6 bodies**
  - **12 heads** (6 per sex), "various nationalities", static-mesh heads in 4 LODs
  - hair slots: hair, eyebrows, fuzz, eyelashes, moustache, beard (Fab listing, SNIPPET: "10 hair grooms")
  - clothing: female 27 tops / 15 bottoms / 9 shoes; male 36 tops / 18 bottoms / 6 shoes
  - accessories: 3 briefcases, 3 purses, 1 phone, 1 coffee cup, 2 backpacks
  - material variation: skin texture atlas index 0-15, melanin, redness, roughness; clothing pattern colour + pattern option; per-character scale
  - far tier: 164 static meshes with baked bone animation (AnimToTexture), 155 AnimToTexture data assets; ISM rendering driven by Mass processors
  - Fab listing wording (SNIPPET): "six swappable bodies, 12 heads, 10 hair grooms, and a range of accessories and clothing". Fab page itself refused (403).
- So Epic's own answer: **12 faces** carried a 35,000-person city; the variety came from clothing combinatorics, colour, hair, skin tone, props and scale.

**Unreal 5.8 MetaHuman Crowd plugin / MetaHuman Collections (Experimental), released 2026-06-17.**
- Release notes: collections of modular components (head, body, hair, clothing) composed by hand or procedurally in Blueprints; "scaling from tens to thousands"; transitions between full actors and Instanced Skinned Meshes (ISKM) by distance; simulated with Mass; Nanite or dynamic LOD; "optimized face textures ... reduced memory footprint". https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine (OPENED; CLAIM)
- Press: "hundreds of characters on mobile and thousands on higher-end platforms". https://gamesbeat.com/epic-games-launches-metahuman-5-8-to-create-real-time-game-character-crowds/ 2026-06-17 (OPENED; CLAIM)
- Doc: crowd pipeline converts strand grooms to card skeletal meshes, strips high LODs, distant ISKM characters do **not** run the post-process Anim BP so **no correctives**; status "Experimental ... use caution when shipping". https://dev.epicgames.com/documentation/metahuman/metahuman-crowds-in-unreal-engine (OPENED)
- Doc: each "MetaHuman Instance" = one appearance (head/body character + groom + clothing), plus instance parameters "hair color and clothing tint"; LOD caps per tier, example "10 full-quality actors at close range but hundreds of instanced characters at a distance"; far range stops rendering. https://dev.epicgames.com/documentation/metahuman/create-metahuman-crowds-in-unreal-engine (OPENED)
- Known 5.8 bug report: Mass crowds on SkinnedMeshInstance never release animation tracks when entities die, GPU memory grows each spawn wave. https://forums.unrealengine.com/t/mass-crowds-using-skinnedmeshinstance-leak-gpu-memory-every-wave-of-spawned-and-killed-entities-permanently-grows-the-animation-track-pool-5-8/2742508 (SNIPPET; CLAIM, user report)
- User test: 1,000 MetaHumans in the Fab Crowds Sample at ~50-60 fps in editor with screen recording, hardware not stated. https://note.com/creator_gaku/n/n61bbff67b601 2026-06-19 (OPENED; loosely MEASURED, not a benchmark)

**Mutable (Customizable Object).** https://dev.epicgames.com/documentation/en-us/unreal-engine/mutable-overview-in-unreal-engine?application_version=5.6 (OPENED)
- Generates skeletal meshes, materials and textures at runtime; merges meshes to cut draw calls, removes hidden geometry, bakes texture layers, texture streaming on demand; once generated a character costs "only the resources of a pre-generated Skeletal mesh". **Beta**. Docs don't mention crowds or MetaHumans. (CLAIM)
- Epic's 5.5 description: runtime generation "optimizing memory usage, keeping shader cost low, and reducing the draw call count" (SNIPPET).

**Kingdom Come: Deliverance II (Warhorse).** GDC 2026 session, Petr Smrček, "Supporting Thousands of NPCs in KCD & KCD II": KCD2 "quadruples the number of NPCs on the map to nearly 2400 and concentrates around half of that into a single city", AI LOD to hold 60 fps. https://schedule.gdconf.com/session/supporting-thousands-of-npcs-in-kingdom-come-deliverance-kingdom-come-deliverance-ii/915120 (SNIPPET, page refused 403; CLAIM). About simulation LOD, not appearance. Clothing: 16 layered slots, items get worn/dirty/bloody (SNIPPET, wiki-level).

**Red Dead Redemption 2.** 1,200 actors in mocap, 700 with dialogue, 2,200 mocap days (SNIPPET, Wikipedia "Development of RDR2"); "over a thousand actors ... for all the NPCs" via Rockstar Intel, GamingBolt 2018-10-07 https://gamingbolt.com/red-dead-redemption-2-new-details-over-1000-actors-used-for-npcs-musical-score-and-more (OPENED; CLAIM). The brute-force end: not a recipe for a small team.

**Watch Dogs: Legion.** Census system generates appearance, demographics, schedules, relationships consistently with role; GDC 2021 "Census" talk. No head/outfit counts published in what was opened. https://www.gamedeveloper.com/design/how-watch-dogs-legion-s-play-as-anyone-simulation-works 2020-12-09 (OPENED); https://news.ubisoft.com/en-us/article/4po3S9Pwp1YcgBmGPmQxAh/watch-dogs-legion-the-tools-that-built-london 2021-03-30 (OPENED). Useful pattern for LEDGER: appearance chosen *from* the person's role and life, so the look is consistent with what the simulation says about them.

**Cyberpunk 2077.** Criticism is behavioural sameness: crowds "very one-track", uniform paths, "endless-mindless stream" that despawns round corners (mod author quoted, PCGamesN 2023-01-08 https://www.pcgamesn.com/cyberpunk-2077/mod-npc-the-matrix, OPENED; CLAIM). Lesson: identical routing reads as clones even with varied looks. No official appearance count found.

---

## 3. Unreal machinery and its cost

- **Animation Budget Allocator**: throttles skeletal mesh ticking to a fixed game-thread budget, default `a.Budget.BudgetMs=1.0`, examples 1.0-2.5 ms by scalability; nearest/most significant animate every frame, others every N frames with interpolation. https://dev.epicgames.com/documentation/unreal-engine/animation-budget-allocator-in-unreal-engine (OPENED)
- **Modular character assembly**: Leader Pose cuts game-thread cost but not render cost (each part still drawn, more draw calls per section); Copy Pose most expensive; **Skeletal Mesh Merge** lowest cost on both threads. https://dev.epicgames.com/documentation/en-us/unreal-engine/working-with-modular-characters-in-unreal-engine (SNIPPET of 5.8 doc)
- **MetaHuman LODs**: face up to 8 LODs, body 4; setting Forced LOD 0 or 1 "for a large number of MetaHumans (for example, a crowd) can negatively affect your game's performance"; dozens of strand-groom MetaHumans run poorly, cards/meshes boost performance. https://dev.epicgames.com/documentation/metahuman/controlling-metahuman-levels-of-detail-lods-in-unreal-engine (OPENED; no triangle counts on page)
- **Groom VRAM**: 50 cards-only MetaHumans = ~800 MB VRAM for grooms (400 MB assets + 400 MB runtime buffers), ~16 MB each, RTX 3070 8 GB. Epic staff (2026-03-16): "There is no existing code dedicated for crowd usage. We are working on this at the moment, but there is no ETA." https://forums.unrealengine.com/t/groom-lod-data-remains-fully-resident-in-vram-regardless-of-distance-lod-level/2715458 (OPENED; MEASURED by user). Note: predates the 5.8 crowd plugin, which converts grooms to card skeletal meshes.
- **Correctives**: turning off MetaHuman correctives gave ~40% editor FPS, body correctives ~90% of that; 32 LOD0 MetaHumans test; Skeletal Mesh Merge "ridiculous gains"; finger-bone removal cut bones ~60%; MH 3.0 character 339 MB → 42-67 MB on disk. Ryzen 5800X / 4070 Ti Super. https://forums.unrealengine.com/t/the-new-3-0-metahumans-40-performance-gains-tutorial-inside/1777726 2024-03/04 (OPENED; MEASURED by users)
- LOD0 strand-hair MetaHuman "3-6 ms GPU per character at 1080p on RTX 3070/4070", "1-4 heroes" at 60 fps: Medium post by James Roha (SNIPPET only, page refused 403; CLAIM, unverified, sourcing unknown). Do not rely on it.
- **AnimToTexture** (vertex-animation textures) was built for City Sample, ships as a plugin since UE 5.1; bakes skeletal animation into textures on a static mesh for background crowds. https://forums.unrealengine.com/t/community-tutorial-animtotexture-plugin-how-to-use-it-to-make-vertex-animation-textures-for-crowds/746648 (SNIPPET)
- **Authoring time**: MetaHuman Creator pitched as taking digital humans "from weeks or months to less than an hour" (Epic, 2021-02-10). https://www.epicgames.com/site/en-US/news/announcing-metahuman-creator-fast-high-fidelity-digital-humans-in-unreal-engine (SNIPPET; CLAIM). Clothing is the real authoring cost: every garment has to be fitted to every body type (City Sample fitted its wardrobe to 6 bodies). No published per-character hour figures found.

---

## 4. What the ratios look like

| Source | On screen | Faces/heads | Bodies | Outfits / pieces | Other levers |
|---|---|---|---|---|---|
| Clone Attack 2008 (lab) | 20 foreground | 20 templates | (in template) | 32-36 colour tints each | out-of-step walks, random facing |
| Hitman Absolution 2012 | 500 of 1200 | not given | not given | diffuse swaps | ±5% scale, random-start loops, overlay acts |
| AC Unity 2015 | up to 10,000 | 29 low-res meshes; 40 full | - | colour reapplied on swap | hats/props matched, regional mix |
| City Sample 2022 | thousands of 35,000 | **12** | **6** (2 sex x 3 weight) | 63 tops, 33 bottoms, 15 shoes; pattern + colour | 16 skin atlases + melanin/redness, ~10 grooms, 10 props, scale |
| UE 5.8 MH Crowd doc | "10 full ... hundreds instanced" | user-supplied | user-supplied | user-supplied + tint | hair colour, clothing tint |

---

## 5. Recommended recipe for LEDGER (my synthesis, not a source)

For 200-500 people on the street, 1990 British port town:

1. **Tiers**: named cast and the nearest ~10-20 as full MetaHuman actors (cards grooms, LOD capped, correctives off beyond a few metres, Animation Budget Allocator on); everyone else on the 5.8 MetaHuman Crowd plugin ISKM tier with Mass. Fallback if the Experimental plugin bites: City Sample's AnimToTexture VAT path, which shipped.
2. **Heads 12-16**, half men half women, spread across age with more over-40s than City Sample; face geometry is the least effective lever, so don't overspend here.
3. **Bodies 6** (2 x 3 weights) plus **±5% random scale**.
4. **Hair 10-12 card grooms** + facial hair + **hair colour param**; **skin 12-16 tones** with melanin/redness params.
5. **Upper body is where the eye goes**: ~30 period tops/jackets, ~15 bottoms, ~8 shoes; each with 6-12 colour/pattern tints drawn from a 1990 palette. Avoid near-duplicate silhouettes (two suits, two check shirts got confused as clones).
6. **Head accessories ~10** (flat cap, woolly hat, headscarf, glasses, hood) - rated as effective as face variation. **Hand props ~10** (carrier bag, newspaper, cigarette, umbrella, pushchair, dog lead).
7. **Walks 6-10 distinct gaits** (sex/age matched), **random phase** and **±10% speed**; 4-6 idles; upper-body overlay acts. Out-of-step is as good as random at hiding face clones, but body shape does not hide repeated walks.
8. **Behaviour**: routes and destinations drawn from each person's routine (our simulation already has this); uniform flow is what Cyberpunk players read as clones.

Counting only pieces: 14 heads x 6 bodies x 11 grooms x ~3,600 outfit combos (30 x 15 x 8) x tints x props = far past "no visible repeats" for 500; the risk is not the count but a few loud items (a red anorak) repeating, so cap distinctive items per scene.

Caveats: City Sample wardrobe and props are 2020s (phone, coffee cup, backpacks), so only its heads/bodies/method carry over; its licence must be checked against LEDGER's allowlist before any use. The 5.8 crowd plugin is Experimental and has an open GPU-memory leak report.
