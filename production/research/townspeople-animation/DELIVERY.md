# Townspeople animation: the detail

Research, 30 September 2026, by a separate research helper given the problem (about thirty minutes). It builds on the project's own notes: the hitman-density, unreal-frame-budget, hardware-floor, markerless-mocap (SUMMARY and RECHECK), gaze-and-knowing and character-pipeline topics, and the casting topic's crowd note, which already covers crowd tiers and MetaHuman crowd costs. None of that is repeated here beyond what the argument needs.

(The helper returned its text; the session that asked for it saved it here unchanged except for this note. That session checked the "current fault" in section (e) against the code: the walker's default is 1.2 m/s (StreetMeshes.h), overridable from the street file between 0.2 and 3 m/s; the body moves at that speed times the walk's blend weight, and the weight ramps at 2 per second, so about half a second in and out (PersonAnim.cpp). The clip speed of the walk loops was not checked.)

How the sources are marked:
- OPENED means I read the page.
- SNIPPET means I saw only a search engine's summary.
- "Mine" marks my inference or recommendation, not established practice.

Most outside hosts were refused by the proxy (see g). Epic's documentation site and the raw GitHub file host opened.

---

## (a) The professional pipeline, stage by stage

### a1. The move list per archetype (the "dance card")

- **Established practice.** The move list is written before any capture or purchase. Ubisoft's motion-matching team called theirs a "dance card": every action a character needs, planned as a capture shoot. Motion matching changed what goes on the card: instead of isolated loops, it lists long continuous takes of walking, turning, starting and stopping.
- **Street people as scenarios.** Street populations are organised as "scenarios" tied to places. GTA V's list, extracted by the community, includes these street ones:
  - stand, and stand impatient;
  - smoke; lean;
  - window-shop; hang out in the street;
  - wait to cross the road;
  - sit on a bench, chair, bus stop, steps, ledge or wall;
  - clipboard, janitor, musician.
  
  It also has drinking and phone scenarios, which our canon and period rule out. Red Dead Redemption 2 is reported to have "thousands" of NPC-only scenarios: leaning on walls and rails, sitting on ledges, working, watching livestock.
- **Idle variety.** The Witcher 3's dialogue system drew idles from a pool of 35 variations per skeleton type (male, female, dwarf), with sitting variants, grouped by emotional state and social status.
- **A vendor's rule of thumb** (vendor claim, not a study): 5–8 idle variants per archetype. A library of 20–40 ambient animations can be mixed across archetypes to fill a city. Reactions are "the most neglected" set.

Sources:
- Motion Matching – "Dance Card" Breakdown — Kristjan Zadziuk (Ubisoft Toronto) — 2016 — https://www.linkedin.com/pulse/motion-matching-dance-card-breakdown-kristjan-zadziuk — read 30 Sep 2026 — SNIPPET
- Motion Matching, The Future of Games Animation... Today (GDC 2016 slides) — Kristjan Zadziuk — March 2016 — https://media.gdcvault.com/gdc2016/Presentations/Zadziuk_Kristjan_MotionMatchingFutureOfGamesAnimation.pdf — read 30 Sep 2026 — SNIPPET
- GTAV-Scenarios README (community data dump) — DioneB — undated — https://github.com/DioneB/gtav-scenarios — read 30 Sep 2026 — OPENED (via its raw file)
- Red Dead Redemption 2 scenarios — Nexus Mods "Immersive Scenarios" and rdr2.org — undated — https://www.nexusmods.com/reddeadredemption2/mods/1889 ; https://www.rdr2.org/news/red-dead-redemption-2-ai-animations-physics-open-world-experience/ — read 30 Sep 2026 — SNIPPET
- Most of The Witcher 3's dialogue scenes were animated by an algorithm — PC Gamer (on Piotr Tomsiński, CD Projekt Red, GDC 2016) — March 2016 — https://www.pcgamer.com/most-of-the-witcher-3s-dialogue-scenes-was-animated-by-an-algorithm/ — read 30 Sep 2026 — SNIPPET
- Crowd & NPC Animation Guide / NPC Animation — MoCap Online (vendor) — undated — https://mocaponline.com/blogs/mocap-news/npc-animation — read 30 Sep 2026 — SNIPPET

### a2. The animation source

- **Big studios capture their own.** Red Dead Redemption 2 used over a thousand actors for its NPCs (from the casting topic's crowd note).
- **Smaller teams** use bought or free libraries plus procedural layers: look-at, IK and additive layers.
- **Own capture is ruled "not now"** by the markerless-mocap topic, for labour and not licence. What is new since that ruling: MetaHuman 5.8 turns single-camera video into body animation on the MetaHuman skeleton. It is experimental, runs on Windows only and processes offline on the machine. That changes the tools, not the cleanup labour (mine).

Sources:
- MetaHuman Animation from Mono Video Capture in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine — read 30 Sep 2026 — OPENED
- MetaHuman 5.8 Release Notes — Epic Games — undated (MetaHuman 5.8 released 17 June 2026 per the crowd note) — https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine — read 30 Sep 2026 — OPENED

### a3. Retargeting

In Unreal the tool is the IK Retargeter; see section d. Studios check feet after every retarget. Foot sliding is the standard tell of amateur animation (markerless-mocap topic).

### a4. Runtime systems and layers

- **Layer stacks are the norm.** Ubisoft described Watch_Dogs' shared animation architecture as the "M-A-S-K" stack: Motion, Action, Stance, Kinesic, the last being body language and gestures. It was shared by player, combat and crowd characters.
- **Epic's Lyra** is the reference layered graph:
  - a locomotion state machine;
  - upper body layered over lower body with "Layered blend per bone";
  - distance matching, which drives play-rate from distance so starts and stops land;
  - stride warping, which adjusts stride length to the actual speed;
  - orientation warping, for 360-degree movement;
  - turn-in-place with yaw-offset modes;
  - everything evaluated on worker threads rather than the game thread.
- **Motion matching** is Unreal's query-based alternative to state machines and blend spaces. It needs a Pose Search schema, a database and a trajectory component, and costs more as channels and samples grow. Fortnite has run motion matching and procedural layering on all players on all platforms since December 2023.
- **Dialogue gestures** were generated at The Witcher 3's scale. An algorithm placed body animations, facial animation and look-ats from markers extracted from the voice-over; some minor dialogues were never touched by hand.

Sources:
- In Your Hands: The Character (of Watch_Dogs) — Ubisoft Montreal, GDC 2015 (speaker not captured) — 2015 — https://www.gdcvault.com/play/1022074/In-Your-Hands-The-Character — read 30 Sep 2026 — SNIPPET
- Animation in Lyra Sample Game in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/animation-in-lyra-sample-game-in-unreal-engine — read 30 Sep 2026 — OPENED
- Distance Matching in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/distance-matching-in-unreal-engine — read 30 Sep 2026 — OPENED
- Motion Matching in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/motion-matching-in-unreal-engine — read 30 Sep 2026 — OPENED
- Post on X: "Motion Matching and Procedural layering running on all players on all platforms" — Laurent Delayen (Epic) — 3 Dec 2023 (date from the post ID) — https://x.com/LDelayen/status/1731344144352874641 — read 30 Sep 2026 — SNIPPET
- The Witcher 3 Dialogue System / Cinematic Dialogue in The Witcher 3 — Game Anim (Jonathan Cooper) — 23 Mar 2016 — https://www.gameanim.com/2016/03/23/cinematic-dialogue-witcher-3/ — read 30 Sep 2026 — SNIPPET

### a5. Reactions

- **Hitman: Absolution.** Crowds had two regimes. "Ambient": mill around, notice points of interest, react to the player. "Panic": evacuate, never get in the way. The system ran 1,200 agents with 500 on screen at 30 fps on PS3/Xbox 360 consoles. The gaze-and-knowing topic already notes the response scaling "from a few heads turning to the whole crowd scattering".
- **Timings for a startle** (to a smash): the eyeblink comes at about 20–40 ms and the head moves at about 60–120 ms. A deliberate orienting turn comes later, in voluntary reaction time. So a believable reaction is a head snap and flinch in the first tenth of a second, then a chosen action (mine, from these figures).

Sources:
- Crowds in Hitman: Absolution (GDC 2012 slides) — Kasper Fauerby, IO Interactive — 7 Mar 2012 — https://media.gdcvault.com/gdc2012/slides/Programming%20Track/Fauerby_Kasper_CrowdsInHitman.pdf — read 30 Sep 2026 — SNIPPET (a mirror answered 403)
- Startle response — Wikipedia — undated — https://en.wikipedia.org/wiki/Startle_response — read 30 Sep 2026 — SNIPPET

### a6. Placement: Smart Objects and scenario points

- **Smart Objects** are "a set of activities in the level that can be used through a reservation system". Only the introduction opened; details of slots and StateTree were not read.
- **GASP 5.7** added a Smart Object level where NPCs sit on benches from several approach angles, using State Tree tasks and warping.
- **GTA-style scenario points** are the older, simpler form: an authored point with a facing and an activity.

Sources:
- Smart Objects in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/smart-objects-in-unreal-engine — read 30 Sep 2026 — OPENED (introduction only)
- Explore the updates to the Game Animation Sample Project in UE 5.7 — Epic Games tech blog — about 3 Dec 2025 (date of Unreal Engine's X post announcing it) — https://www.unrealengine.com/tech-blog/explore-the-updates-to-the-game-animation-sample-project-in-ue-5-7 — read 30 Sep 2026 — SNIPPET
- Game Animation Sample Project Receives UE5.7 Update — 80.lv — Dec 2025 — https://80.lv/articles/game-animation-sample-project-updated-for-unreal-engine-5-7 — read 30 Sep 2026 — SNIPPET

### a7. Optimisation

- **Tiers by distance** are established practice. Assassin's Creed Unity: at most 40 full "autonomous" NPCs, a cheaper "puppet" tier, and a far "bulk" tier. City Sample: full MetaHumans near, vertex-animated static meshes far. Both are in the crowd note.
- **Unreal's levers:**
  - Update Rate Optimisations: Epic recommends target update rates of "15Hz and under" at distance.
  - The Animation Budget Allocator.
  - Multi-threaded update and the fast path.
  - Fixed skeletal bounds.
  - The visibility-based tick option.
  - The Animation Sharing plugin, still documented for 5.8, for large crowds that share poses.
  - MetaHuman LODs and the 5.8 MetaHuman Crowds plugin (experimental). Distant instanced characters there skip the post-process AnimBP and so the correctives.

Sources:
- Animation Optimization in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/animation-optimization-in-unreal-engine — read 30 Sep 2026 — OPENED
- Animation Budget Allocator in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/animation-budget-allocator-in-unreal-engine — read 30 Sep 2026 — OPENED
- Animation Sharing Plugin in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-sharing-plugin-in-unreal-engine — read 30 Sep 2026 — SNIPPET
- MetaHuman Crowds in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/metahuman/metahuman-crowds-in-unreal-engine — read 30 Sep 2026 — OPENED

### a8. Judging

- **Established practice.** Animation is reviewed in the game and in context, at gameplay distance and through the gameplay camera. That is the house rule here too: lighting and look are judged through the game's own camera.
- **Objective foot checks exist.** Research uses a "foot-skating ratio": the share of ground-contact frames in which a foot moves faster than a small threshold, with contact defined by foot height (the thresholds vary by paper). The ACM IMX 2023 paper below found that a popular overall quality metric did not reliably capture foot skating. So foot skating needs its own check.

Sources:
- Validating Objective Evaluation Metric: Is Fréchet Motion Distance able to Capture Foot Skating Artifacts? — ACM IMX 2023 — 2023 — https://dl.acm.org/doi/fullHtml/10.1145/3573381.3596460 — read 30 Sep 2026 — SNIPPET
- Game Anim: Video Game Animation Explained (2nd ed.) — Jonathan Cooper, Routledge — 2021 — https://www.routledge.com/Game-Anim-Video-Game-Animation-Explained/Cooper/p/book/9780367707651 — read 30 Sep 2026 — SNIPPET (book listing only; its review practice was not read)

---

## (b) Epic's free assets and systems

### Game Animation Sample Project (GASP)

- **Versions:**
  - Launched for 5.4, announced at GDC 2024 and released about June 2024, with over 500 animations.
  - The 5.7 update (about 3 Dec 2025) added a Mover-based character with a new locomotion dataset and 400 new animations. It also added a slide, "locomotion styles", a Smart Object level where NPCs sit on benches, and an experimental Pose Search column in Choosers, which brings Choosers and motion matching together.
  - The 5.8 update (about August 2026) added Pose Search Interaction assets, which search poses across several skeletal meshes at once with motion warping for two-character moves. It also added an experimental additive Look-At solver built in Control Rig, and new physics features.
- **Contents:** motion matching with Choosers, traversal (vault, climb), leg IK, orientation warping. There are playable UEFN mannequin and MetaHuman variants, and you can swap MetaHuman body types.
- **Skeleton and MetaHumans.** The data is authored on the UEFN (Fortnite) mannequin. The MetaHuman variant uses a runtime-retarget AnimBP ("ABP_GenericRetarget"). A tag on the body mesh names the retarget relationship for each body type, e.g. "RTG_UEFN_to_Metahuman_nrw".
- **Licence:** "only licensed for use with Unreal Engine, but can be used in commercial projects". This is CG Channel's paraphrase of Epic, a SNIPPET. Fab's listing could not be opened. If the Fab listing says Fab Standard License, it is already on our allowlist. If it says Unreal-only or Epic content licence, it is not, and it needs Jafar's ruling.

Sources:
- Game Animation Sample Project in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/game-animation-sample-project-in-unreal-engine — read 30 Sep 2026 — OPENED
- Adding a MetaHuman to the Game Animation Sample Project in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/en-us/unreal-engine/adding-a-metahuman-to-the-game-animation-sample-project-in-unreal-engine — read 30 Sep 2026 — OPENED
- Get over 500 free animations with the Game Animation Sample Project — Epic Games blog — 2024 — https://www.unrealengine.com/blog/game-animation-sample — read 30 Sep 2026 — SNIPPET
- Get over 500 free game-ready animations to use in Unreal Engine — CG Channel — June 2024 — https://www.cgchannel.com/2024/06/get-500-free-game-ready-animations-for-use-in-unreal-engine/ — read 30 Sep 2026 — SNIPPET
- Post on X announcing the GASP 5.7 update — Unreal Engine — 3 Dec 2025 (date from the post ID) — https://x.com/UnrealEngine/status/1996265197951132062 — read 30 Sep 2026 — SNIPPET
- Download the latest Game Animation Sample Project, now updated for UE 5.8 — Epic Games tech blog — about Aug 2026 — https://www.unrealengine.com/tech-blog/download-the-latest-game-animation-sample-project-now-updated-for-ue-5-8 — read 30 Sep 2026 — SNIPPET

### MetaHuman animation assets and retargeting setup

- **Custom animation import.** Animations are imported onto "metahuman_base_skel".
- **Retargeter.** The retarget page names "RTG_MH_IKRig", "optimized for MetaHuman full body IK solve". Our retarget script uses the plugin's IK rig "IK_MH_IKRig".
- **Ground offset.** From 5.6, MetaHumans lost the +2 cm skeleton offset that assumed a shoe sole: "all MetaHuman animation content is now standardized as barefoot". Older animation needs retargeting to remove the offset. Offsets can be set per character. This matters when the clothing session's shoes add a sole (mine).

Sources:
- Play a Custom Animation — Epic Games — undated — https://dev.epicgames.com/documentation/metahuman/play-a-custom-animation — read 30 Sep 2026 — OPENED
- Retarget MetaHuman Creator Animation — Epic Games — undated (links to 5.6) — https://dev.epicgames.com/documentation/metahuman/retarget-metahuman-creator-animation — read 30 Sep 2026 — OPENED
- Base Skeleton Offset Update — Epic Games — undated — https://dev.epicgames.com/documentation/metahuman/base-skeleton-offset-update — read 30 Sep 2026 — OPENED

### MetaHuman skeleton versus the UE5 Manny

- **Epic's statement:** the UE5 mannequins "share the same core skeleton hierarchy as MetaHumans, with a compatible animation system".
- **Community reports** (SNIPPET) say the MetaHuman body has many extra small bones and lacks the mannequin's IK helper bones (ik_foot_root and similar), which foot-IK setups expect.
- **Answer to "no retarget needed?"** The hierarchy is compatible, so a Manny clip can play on a MetaHuman body. But the proportions differ, each MetaHuman build differs, and Epic's own sample still retargets for each body type. For our street people: retarget offline once per body build (mine).
- **GASP needs a retarget anyway**, because it is on the UEFN mannequin, not UE5 Manny.

Sources:
- Lyra Sample Game in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/en-us/unreal-engine/lyra-sample-game-in-unreal-engine — read 30 Sep 2026 — OPENED
- Making Metahuman use UE5 MannyQuinn Skeleton (forum thread) — Epic Developer Community — 2022 onward — https://forums.unrealengine.com/t/making-metahuman-use-ue5-mannyquinn-skeleton/536769 — read 30 Sep 2026 — SNIPPET

### City Sample crowds

- **Method.** Near people are full MetaHumans; far people are vertex-animated static meshes baked with AnimToTexture and driven by Mass AI and StateTree.
- **Kit.** 12 heads and 6 bodies, with 2020s clothing (crowd note).
- **Licence.** Reported as Unreal-only (SNIPPET, forum summary).
- **Usefulness.** Its method is useful; its wardrobe and props are not (period).

Source:
- the casting topic's crowd note, which opened Epic's City Sample page and a third-party breakdown of its crowd content (September 2026).

### Lyra

- **Contents.** State machine, linked anim layers, distance matching, stride warping, orientation warping, turn-in-place, multi-threaded update (OPENED).
- **Licence.** The README states "UE-Only Content - Licensed for Use Only with Unreal Engine-based Products". I read this on a GitHub mirror of Lyra, not on Epic's own page.

Source:
- Lyra README (mirror) — johnlogostini/Lyra on GitHub, copying Epic's README — undated — https://github.com/johnlogostini/Lyra — read 30 Sep 2026 — OPENED (via its raw file)

### Motion Matching and Choosers, 5.4 to 5.8

- **5.4:** motion matching shipped in the Pose Search plugin, with GASP as the example.
- **5.7:** Pose Search column in Choosers (experimental).
- **5.8:** Pose Search Interaction assets. Epic's page marks some features experimental (Motion Matched Stitching, some channels) but does not label the core system either way.

### Other 5.7 and 5.8 changes that matter here

- **Retargeting (5.8):**
  - "Foot Definition for Retargeting", which defines "a foot plane and toes for the target character for better controlled transfers". Auto-retargeting templates were updated for it.
  - Retarget Override Sets.
  - An option to prevent damping of vertical pelvis motion on shorter characters.
- **Mass (5.8):** entities created off the game thread.
- **StateTree (5.8):** start-state and compiler improvements.
- **Animation Mixer** (experimental, for Sequencer).
- **MetaHuman Crowds** (experimental).
- **Mono-video body capture** (experimental).

Source:
- Unreal Engine 5.8 Release Notes — Epic Games — undated (UE 5.8 released June 2026) — https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes — read 30 Sep 2026 — OPENED

---

## (c) Other animation sources

| What | Size | Quality | Licence for a shipped game | Cost | Allowlist |
|---|---|---|---|---|---|
| Mixamo (Adobe) | about 2,500 clips (markerless-mocap topic) | Uneven. Single moves from different performers; starts, stops and turns rarely match their walks (mine). | Royalty-free for commercial games; no redistribution of raw files; no credit required (SNIPPET of Adobe's FAQ) | Free with an Adobe account | Yes, with Jafar's account (D46) |
| Fab free animation packs | varies | varies | Fab Standard License permits commercial games in any engine; Personal tier up to $100,000 revenue in 12 months, Professional above (Fab docs OPENED; Fab EULA SNIPPET) | Free | Yes (Fab Standard License) |
| Fab paid packs, e.g. "MC Idles" (238 NPC idles in 22 sets, including smoking a cigarette, shifting weight, crossing arms, shivering), "Conversation Gesture MoCap Pack" (82 gesture clips), "Character Conversation" (28) | as stated (SNIPPET) | mocap, on the UE5 mannequin, said to retarget to MetaHuman (vendor) | Fab Standard License | not seen (Fab refused) | Yes, but a purchase is a money decision |
| GASP / Lyra / City Sample (Epic) | over 900 (GASP after 5.7) | high, consistent, made for motion matching | Unreal-only, commercial allowed (SNIPPET; Lyra's Unreal-only line read on a mirror) | Free | Not named: Jafar decides |
| CMU Graphics Lab mocap | about 2,500 sequences | early-2000s capture, noisy, needs cleanup | "You may include this data in commercially-sold products, but you may not resell this data directly, even in converted form" (SNIPPET; site refused, as it was on 19 Sep) | Free | Not named: decision if used |
| Rokoko Motion Library, free clips | 150 free moves (2020) and 100 on sign-up (SNIPPET) | mocap suit data | Reported usable in commercial games; paid clips licensed for 3 years, output keeps working (SNIPPET) | Free / $3–20 per paid clip | Not named |
| Move.ai | no free library found | capture service | not surveyed | n/a | n/a |
| Bandai Namco Research Motiondataset | two sets: 36,673 and 384,931 frames, 3 actors, BVH | good, stylised | CC BY-NC 4.0 (non-commercial) on both datasets (OPENED) | Free | Never ship |
| MoCap Online packs | hundreds per pack | studio mocap | Royalty-free Standard License to 1 million end users and $1M revenue (vendor, SNIPPET) | Vendor says $300–1,500 for an indie library | Money decision |
| AMASS, LAFAN1 | large | good | Non-commercial (markerless-mocap topic) | n/a | Never ship |
| Own capture: MetaHuman 5.8 mono-video body capture | as captured | experimental; cleanup labour unknown | our own footage, under the MetaHuman licence (never to train AI) | Free tool, labour cost | MetaHuman is allowed; the capture route was ruled "not now" |

Sources:
- Mixamo FAQ — Adobe — undated — https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html — read 30 Sep 2026 — SNIPPET
- Licenses and Pricing in Fab — Epic Games — undated — https://dev.epicgames.com/documentation/en-us/fab/licenses-and-pricing-in-fab — read 30 Sep 2026 — OPENED
- Fab Standard License — Epic Games — undated — https://www.fab.com/eula — read 30 Sep 2026 — SNIPPET
- Epic Content License ("UE-Only Content") — Epic Games — undated — https://www.unrealengine.com/eula/content — read 30 Sep 2026 — SNIPPET
- MC Idles Animation Pack — Fab listing — undated — https://www.fab.com/listings/a14e1356-8a12-492a-8312-accecfbbc6f0 — read 30 Sep 2026 — SNIPPET
- Conversation Gesture MoCap Animation Pack — Fab listing — undated — https://www.fab.com/listings/c3a1ed6f-022a-49ef-a942-1bfee0a151b6 — read 30 Sep 2026 — SNIPPET
- Character Conversation – MoCap Pack — Fab listing — undated — https://www.fab.com/listings/7cba719d-f7aa-49f2-bd87-444003cd8d24 — read 30 Sep 2026 — SNIPPET
- CMU Graphics Lab Motion Capture Database (terms as quoted by mirrors) — Carnegie Mellon University — undated — http://mocap.cs.cmu.edu/ — read 30 Sep 2026 — SNIPPET
- Get 150 free mocap moves from Rokoko's Motion Library — CG Channel — March 2020 — https://www.cgchannel.com/2020/03/get-150-free-mocap-moves-from-rokokos-motion-library/ — read 30 Sep 2026 — SNIPPET
- Bandai-Namco-Research-Motiondataset README — Bandai Namco Research — undated — https://github.com/BandaiNamcoResearchInc/Bandai-Namco-Research-Motiondataset — read 30 Sep 2026 — OPENED (via its raw file)
- Animation Licenses — MoCap Online (vendor) — undated — https://mocaponline.com/pages/licensing — read 30 Sep 2026 — SNIPPET

---

## (d) Retargeting to MetaHumans in 5.8, and foot-contact checks

### The recommended 5.8 path (Epic docs, OPENED)

1. **Source IK rig.** Auto-generate the source's IK rig. The Python calls are "apply_auto_generated_retarget_definition()" for the retarget chains and "apply_auto_fbik()" for a full-body IK solver with goals. Epic's auto-retarget templates list only "UE4 and UE5 Mannequins, Metahumans, Stack O Bot". Mixamo is not named, so check the chains on a Mixamo rig by hand, or use a community Mixamo IK rig.
2. **Target rig.** Use the MetaHuman plugin's IK rig as the target, as our script already does.
3. **Retarget poses.** Build a retargeter with matched retarget poses using Auto Align: "Matching these retarget poses increases the accuracy of the retargeting."
4. **Op stack (5.8):** Pelvis Motion, FK Chains, Root Motion, Remap Curves, Retarget Pose, Additive Pose, Pin Bones, Filter Bones, Scale Source, Stretch Chains, Pole Vector Alignment, Copy Base Pose, Run IK Rig. Its foot sub-operations are:
   - Floor Constraint: "Constrains IK goals to the floor".
   - Speed Plant IK Goals.
   - Stride Warp IK Goals.
5. **Foot Definition (new in 5.8):** set the foot plane and toes for the target.
6. **Speed Planting, following Epic's recipe:**
   - add a Motion Extractor modifier per foot to each source clip, on bones ball_l and ball_r, Translation Speed, axis XYZ, which creates curves such as "ball_l_translation_speed_XYZ";
   - give the target IK rig a full-body IK solver with foot goals;
   - in the retargeter, enable Speed Planting on each leg chain with that curve and a threshold "slightly higher than where the curve stays flat" (Epic's example: 30).
7. **Batch retarget.** Use a saved retargeter, not an auto-generated one, and pick the override set.
8. **One retargeter per body build.** Retarget each clip to each body build, meaning our cast plus the slim, average and heavy builds, rather than trusting one body for all (mine). The alternative is Epic's runtime retarget, which costs a second pose evaluation per person every frame (unmeasured).

Sources:
- IK Rig Animation Retargeting in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/ik-rig-animation-retargeting-in-unreal-engine — read 30 Sep 2026 — OPENED
- Retargeting Operation Stack in Unreal Engine 5.8 — Epic Games — undated — https://dev.epicgames.com/documentation/unreal-engine/retargeting-operation-stack-in-unreal-engine-5-8 — read 30 Sep 2026 — OPENED
- Fix Foot Sliding with IK Retargeter in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/en-us/unreal-engine/fix-foot-sliding-with-ik-retargeter-in-unreal-engine — read 30 Sep 2026 — OPENED
- Auto Retargeting in Unreal Engine — Epic Games — undated (5.8) — https://dev.epicgames.com/documentation/unreal-engine/auto-retargeting-in-unreal-engine — read 30 Sep 2026 — OPENED
- Using Python to create and edit IK Rigs in Unreal Engine — Epic Games — undated (5.7) — https://dev.epicgames.com/documentation/en-us/unreal-engine/using-python-to-create-and-edit-ik-rigs-in-unreal-engine — read 30 Sep 2026 — OPENED

### Foot-contact checks (mine, built from the research metric and Epic's recipe)

The checks run by script on every retargeted clip for every body build, and fail the clip before any person reaches the gate.

1. **Sample every frame** in component space: the heel (foot) and ball bone positions, and the root or actor motion the game will apply.
2. **Define contact** as a bone within about 3 cm of that foot's lowest point in the loop, or of the ground plane once the shoe-sole offset is known.
3. **Skating:** horizontal speed of a contact foot relative to the ground. For in-place loops, add the actor speed the game will use. Report:
   - the share of contact frames above about 5 cm/s;
   - the worst slide per footfall in cm.
4. **Penetration and float:** the lowest stance height below 0 (sinking) or above about 1.5 cm (floating). Shoes matter: MetaHumans are barefoot-aligned since 5.6.
5. **Speed match.** The clip's own ground speed is stride length times steps per second, or its root motion. The game must move the person at that speed times the play rate. Keep play rates within about 0.8 to 1.2, or change the clip.
6. **Thresholds.** Start with these numbers. Tune them by eye on the first approved sample, then freeze them.

**Current fault (from reading the code).** The street walkers move at a set speed: 1.2 m/s by default, or a value from the street file. The walk loop plays at its own natural rate, whatever its feet travel. During the roughly half-second start and stop, the body moves at a fraction of full speed while the walk is only partly blended over the idle. Both will show as sliding unless the clip happens to travel at 1.2 m/s. This is unmeasured and should be the first check.

---

## (e) What twenty people cost on this PC

### Published figures, each with its hardware

| Figure | Source | Hardware | Mark |
|---|---|---|---|
| Animation Budget Allocator default budget 1.0 ms on the game thread. Other defaults: a.Budget.MinQuality 0, MaxTickRate 10, InterpolationMaxRate 6. | Epic doc | none given | OPENED |
| Update Rate Optimisations: aim for update rates of 15 Hz and under at distance | Epic doc | none given | OPENED |
| MetaHuman head LOD0: 24,000 vertices, 713 joints, 669 blendshapes. Blendshapes at LOD0 only; joints fall to 26 at LOD7. Body LOD0: 30,500 vertices, down to 1,507 at LOD3; correctives on LOD0–1. Hair strands on LOD0–1 only; hair physics LOD0–2. | Epic LOD spec | n/a | OPENED |
| Memory per MetaHuman: Cinematic "between 1–2 GB" on average, UE Optimized "under 100 MB". Optimized switches correctives by LOD; Low quality means cards, no correctives, no physics. | Epic assembly doc | n/a | OPENED |
| Card hair for 50 MetaHumans: about 800 MB of graphics memory, about 16 MB each | forum user, 16 Mar 2026 | RTX 3070 8 GB | via the crowd note |
| Correctives off: about 40% more editor fps with 32 LOD0 MetaHumans | forum users, 2024 | Ryzen 5800X, RTX 4070 Ti Super | via the crowd note |
| 1,000 crowd MetaHumans at about 50–60 fps in the editor | blog, 19 Jun 2026 | not stated | via the crowd note |
| Assassin's Creed Unity: about 25 µs of CPU per far "bulk" NPC and about 150 µs per "puppet"; at most 40 full NPCs | GDC 2015 | PS4 and Xbox One | via the crowd note |
| Hitman: Absolution: 1,200 agents, 500 on screen, 30 fps | GDC 2012 | PS3 and Xbox 360 | SNIPPET |
| Our simulated people: 0.07 ms each | the project's frame-budget topic | this PC | measured (simulation only, not bodies) |
| Motion matching "0.1–0.5 ms per character" | MoCap Online blog (vendor) | not stated | SNIPPET, unverified: do not use |
| RigLogic (face rig) per character | not published | n/a | unmeasured |
| Chaos cloth per character | not published | n/a | unmeasured |

### My estimate for twenty people on the Ryzen 5 5600X and RX 6700, unmeasured

Assumptions: 20 MetaHuman-like people on Quay Street, built with the UE Optimized pipeline, card hair, body LOD1–2 beyond a few metres, face LOD0 only for whoever is speaking, and our native anim graph (two clips, a look-at, curves).
- **Processor:** about 1–3 ms of work per frame across worker and game threads.
- **Graphics card:** about 2–5 ms at 1080p, mostly shadows for moving people, skin and hair shading.
- **Graphics memory:** about 2–3 GB.
- **Cloth:** Chaos cloth on everyone could add several ms of processor time. Keep it to the nearest few people.

Against the frame budget, that is affordable at 30 fps (33 ms) and tight at 60 fps (16.7 ms). This estimate must not go into the overview as a number (the house rule on the real path).

### Levers, cheapest first

1. UE Optimized assembly for every street person. Check what the principals use: Cinematic cannot scale on 10 GB.
2. Card hair beyond close range. Epic names a switch that forces cards instead of strands.
3. Correctives only where Epic's Optimized pipeline keeps them (LOD-based).
4. Face LOD capped for people who are not speaking.
5. Update Rate Optimisations on for everyone except speakers and the nearest two or three.
6. Animation Budget Allocator at 1 ms.
7. Tick only when rendered for people off screen. The probe currently forces an always-tick option in places, which is needed for its renders, not for play.
8. Cloth only near the camera.
9. For more than a few dozen people, the 5.8 MetaHuman Crowds instanced tier. It is experimental and has an open memory-leak report.

### Measurement plan for this PC

- **Setup.** Packaged build, Quay Street, the game's own camera and exposure, the evening light fixed.
- **Runs.** Spawn 0, 1, 5, 10 and 20 dressed people, half idling and half walking. Capture 30 seconds each with Unreal Insights (CPU, GPU, memory, animation channel).
- **Record for each run:** game-thread, render-thread and GPU ms; animation evaluation ms; graphics memory used.
- **Levers.** Repeat at 20 with each lever switched on in turn.
- **Report:** the cost per extra person for each lever, labelled "measured in the packaged build on RX 6700 / 5600X".
- **Time:** about half a day to a day (mine).

---

## (f) Concrete steps for this project, in order

House rules that shape the order:
- the playable route comes first, so only the moves the route needs;
- nothing is multiplied until one sample is approved in the game;
- faces are frozen, so the animation work never touches head shape;
- two tries, then research, then set aside;
- judged through the game camera; the AI tester walks it.

1. **Measure** as in section e. About 0.5–1 day.

2. **Fix the walking feet now:**
   - work out each walk clip's own ground speed and set the play rate from the person's speed, or pick the walk whose speed fits;
   - during starts and stops, move the body only as fast as the blended pose shows;
   - add the foot-contact check from section d as a script that fails clips.
   
   About 1 day. It needs nothing new.

3. **Licence question to Jafar**, one multiple-choice question: may Epic's own free Unreal-only animation content (GASP, Lyra, City Sample animations) be used inside the Unreal game?
   - **(A) Yes, only inside the game. Recommended**: consistent, high-quality walks, turns, starts, stops and bench-sitting.
   - (B) No; Mixamo only.
   - (C) Buy Fab packs (money).
   
   First check the GASP listing's licence line on Fab from Jafar's PC: if it is the Fab Standard License, no question is needed.

4. **Retarget pipeline.** Extend the existing Mixamo-to-MetaHuman script to:
   - GASP clips (if A);
   - the 5.8 foot definition, Speed Planting and Floor Constraint;
   - one batch per body build;
   - the shoe-sole offset, checked against the clothing session's current shoes (name the exact file, per the handover rule).
   
   About 1–2 days.

5. **The first move set**, for one archetype: an ordinary adult man of the town. Then a woman and an older person.

| Move | Why | First source | Fallback |
|---|---|---|---|
| Stand: 3 idle variants (weight shift, hands in pockets, arms folded, look at watch) | standing people are most of the street | GASP idles (if A), or Mixamo idles | Fab idles pack (paid) |
| Walk at two speeds: about 1.3 m/s, and 1.0 m/s for older people | the street's main motion | GASP walk set (if A) | Mixamo walks |
| Start and stop | kills the slide at each end | GASP (if A) | speed-matched blend from step 2 |
| Turn in place, 90 and 180 degrees | a head turn past about 60 degrees should bring the body | GASP (if A) | Mixamo turns (names unverified) |
| Look | the gaze research: the head must turn, the eyes alone are invisible from behind | our look-at, extended to share the turn down the spine and to the eyes | GASP 5.8 look-at solver (experimental) |
| Talk gestures: listen, explain, point, shrug, nod (4–6, upper body) | conversations in the street | Mixamo talking clips | Fab conversation-gesture pack (82 clips, paid) |
| Smoke a cigarette: standing loop, plus an upper-body version for walking | tobacco allowed; period | Mixamo "Smoking" (name unverified) plus a cigarette prop on a hand socket | Fab idles pack (includes smoking, paid) |
| React to a smash: head snap and flinch in the first 0.1 s, then glance and resume, step back, or move away, staggered by distance and by what they know | the route's event; Hitman's "few heads to whole crowd" | our look-at plus an additive flinch, with Mixamo reaction clips for the full-body step | Fab |
| Lean on a wall, wait at the kerb, sit on a step | spots in the street | Mixamo (sit, lean) or GASP bench (if A) | Fab |

Excluded by canon or period: drinking, phones, anything with children or gambling.

6. **Layering, in our own native anim instance.** Recommended: extend it rather than switch to Epic's Blueprint systems for the street's people. It is built by script and cheap, and its gaze and mouth layers already work. The layers, bottom to top, using engine nodes that exist for native use:
   - locomotion: idle variants through a random player, and walk speeds through a blend space or play-rate matching;
   - turn-in-place;
   - a full-body montage slot for reactions and spot actions;
   - an upper-body slot through layered blend per bone from the spine, for gestures and the cigarette;
   - an additive layer for flinch and breathing;
   - leg IK to the pavement and kerbs;
   - the look-at chain;
   - the face as its own layer (the existing mouth curves; faces frozen).
   
   This is exactly the audit's "compose body, gaze and facial layers". About 2–4 days.
   
   Motion matching (GASP) is the big-studio standard. Consider it later only for the player character, if his walk is judged unconvincing. Its cost for NPCs is unmeasured, and its data comes under the licence question.

7. **Variety:**
   - random start phase and ±5–10% play rate;
   - a different idle and walk per person;
   - mirrored idles;
   - cap the distinctive moves per scene (crowd note).
   
   About half a day.

8. **Spots.** Authored points with a facing and an activity, as GTA-style scenarios: the door, kerb, shop window, wall, step. Unreal's Smart Objects when benches or queues need reserving. About 1 day.

9. **Cost levers** from section e, switched on and measured again. About half a day.

10. **Judging:**
    - a short clip of the street, from the game camera at the standard distance with the approved light;
    - the gate: the automatic foot check, a check for identical idles playing in step, and a comparison with real British street footage from 1988–92 (links only, in production/reference);
    - then a fresh reviewer;
    - then the clip on Jafar's page as a whole-street item, with the one complete sample person approved before any copying;
    - then the AI tester walks it in the packaged build.

**Rough total (mine):** about 9–14 session-days to one approved sample, then 2–3 days to twenty.

---

## (g) What could not be verified or reached

- **Refused by the proxy:** unrealengine.com (tech blogs, the EULA, the Epic content licence), cdn2.unrealengine.com, fab.com, helpx.adobe.com, mocap.cs.cmu.edu, rokoko.com, www.gdcvault.com, media.gdcvault.com, gameaipro.com, archive.org (the RigLogic white paper), forums.unrealengine.com, 80.lv, cgchannel.com, therookies.co, projprod.com, gamedev.net, awn.com, gameanim.com, biunivoca.com, data.4tu.nl, apjcriweb.org, ohyecloudy.com. A mirror of the Hitman slides answered 403.
- **Therefore unverified:**
  - the exact licence text for GASP and City Sample;
  - the Fab listing licences;
  - Mixamo's current terms;
  - CMU's and Rokoko's terms;
  - GASP's animation list by category;
  - which Mixamo clip names exist today ("Smoking", turns, reactions);
  - whether 5.8's auto-retarget recognises Mixamo rigs;
  - what the conference talks say beyond their summaries.
- **No published figure found** for the cost per character of motion matching, RigLogic, Chaos cloth, or runtime retargeting. The only motion-matching figure is a vendor's unsourced claim.
- **Not checked in the project:** which MetaHuman assembly quality the principals use; the clip speed of the current walk loops. Both are cheap to check on the build PC.
