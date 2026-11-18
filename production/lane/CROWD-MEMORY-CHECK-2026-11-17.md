# Crowd and card memory: paper check of the packing plan, 17 November 2026

Reviewed 17 Nov 2026: PASS WITH FIXES, applied.

Paper check; nothing run. Read: the packing plan and review, MEMORY-PLAN, MEMORY-WHERE, OWNER-DUMP-2026-11-16 (frame-headroom folder), PLAN.md's performance exit, 4-BUDGETS l.172-174.

## 1. Which number is which

- "About 15 h, 4.6 GB" (running list): the 15.5 h is the packing plan's steps 0 to 3. The 4.6 GB is older: the 8 Nov cooking plan's expected peak (DECISIONS archive to 9 Nov, 8 Nov entry, "peak expected about 4.6 GB from 6.15"). The plan now expects a walking peak of 3.8 to 4.3 GB (inferred).
- "6.0 GB": PLAN.md's performance exit, the game's dedicated card memory with the voice also on the card.
- "4,711 MB": Windows' budget for the game at the moment of the 16 Nov dump (D3D "Total Video Memory (Budget)"), with the voice resident. Over it, the dump shows 361 MB demoted (moved off the card). The plan's 4,870 is the same budget on 9 Nov; it moves.
- "5,072 MB": the engine's used video memory in the memreport at the walking peak (4,952 settled). Windows' own counter in the same walk read 5,213 median, 5,565 peak. The two counters differ by about 260 to 490 MB and the plan compares both against the budget at different points.

So the binding line on the 16 Nov reading was about 4.7 GB, not 6.0; it moves (risk 1).

## 2. Numbers and verdicts

| Plan number | Verdict | Note |
|---|---|---|
| Steps 0-3 about 15.5 h | Holds, shrinking | Step 0 (1.5 h) done; step 1 trialled. About 12 to 13 h left (step 2 about 10 h, step 3 1.5 h, step 1's three-run check). |
| 4.6 GB expected peak (running list) | Wrong, corrected | Stale 8 Nov figure. Plan's own: 3.8 to 4.3 GB walking peak (inferred). |
| 6.0 GB line | Needs the PC | Windows granted 4,711 on 16 Nov. Measure the budget with only game and voice running, three times. |
| 5,072 used against 4,711 (360 over) | Holds | Measured, OWNER-DUMP l.141-148. |
| Step 1 saves about 160 MB | Holds | Measured once (4,952 to 4,792 settled); three runs still owed. |
| Step 2 saves about 1,060-1,080 MB | Holds on paper | Dump confirms 1,351 MB of uncompressed, unstreamed run-time pictures. |
| Step 3 hair voxel saves about 256 MB | Holds, peak only | Only while strands are drawn; fixed, not per person. |
| Room left about 800 MB | Needs the PC | True on the engine's counter (4,711 less about 3,850); about 390 after the 10% spare (section 4). On Windows' counter (5,505, already with step 1, less about 1,070 for step 2) only about 280 MB, and below zero after the 10% spare. Measure which counter Windows judges against. |
| Ceilings: pictures 450, cooked 600, Lumen 500, distance fields 300, heaps 640, people 800, reserve 600 | Wrong against the real line | They sum to 3,890 before TSR (156), shadows, the 570 to 670 MB outside the dump, and street copies. That fits 6.0 GB, not 4.7 GB. Against 4,711 the people ceiling cannot be 800. |
| Principal person up to 100 MB, 3 near (4-BUDGETS, "Optimized" [R, Epic]) | Needs the PC; Epic's basis not found | Epic gives no MB per MetaHuman; Optimized tops out at 2K textures. The 16 Nov dump holds Rocco's body maps at 4096 when near (T_Body_N and T_Body_SRMF 21.4 MB each, T_Body_BC 10.7): about 53 MB for one body set, so the cast is not at 2K today. Cap Character textures at 2048. |
| Passer-by 15 to 20 MB, card grooms up to 16 MB | Needs the PC | Inferred; textures only, leaving out mesh buffers (669 head blendshapes at LOD0, per Epic), skin cache and groom data. |
| Skin cache about 2.5 MB at LOD0 | Holds roughly, still a forum figure | Forum test, 50 NPCs: about 2.7 MB each, 0.6 at forced LOD3. Unverified for 5.8. |
| Each further MetaHuman +5 to +8 MB textures (24 Sep) | Needs the PC | |
| About 28 people in 800 MB (3 x 100 + 25 x 20) | Holds as arithmetic, wrong as a promise | Only inside a 6.0 GB grant, and 25 passers-by exceeds 4-BUDGETS' cap of 12; at 15 MB plus a card groom up to 16 MB, 20 MB each is low. See section 4. |
| 165 MB per street copy, "street copies the rest" | Needs the PC | Under 4,711 there is no rest after people. |
| Pool 800 MB guards textures | Wrong as a guard | Epic lists the pool as holding NeverStream and streamed textures; in practice (MEMORY-WHERE s2) the 1,351 MB of run-time pictures sit outside its cap. Step 2 keeps them unstreamed. |

## 3. Assumptions against Epic's current docs

- MetaHuman LODs: head 24,000 to 130 vertices over LOD0-7; body 30,500 to 1,507 over LOD0-3; strands at LOD0-1 only, cards to LOD4. Epic gives no memory per LOD or per character, so the plan's per-person MB is project inference.
- LODSync: forcing LOD 0 or 1 on many people is warned against; switching is by screen size, not distance. Cards instead of strands: r.HairStrands.UseCardsInsteadOfStrands 1, or minimum LOD 3.
- Crowds: Epic's 5.8 MetaHuman Crowds is marked Experimental. Epic's Create MetaHuman Crowds page gives about 10 full actors near as an example; the Crowds page draws the rest as instanced skinned meshes with high LODs stripped, card hair and no correctives. An Epic engineer on the forum suggests about 8 full actors, the rest Mass with vertex animation (City Sample).
- Animation Budget Allocator (default 1.0 ms) and Animation Sharing save game-thread time only. Neither saves card memory.
- Nanite for skeletal meshes: listed by Epic (animation LODs, no geometry LODs, streamed on demand), no memory figures; the street has Nanite off. Not a saving to count on.
- Virtual textures: fixed pools per format; not needed now.
- Shipped UE5 games, 20 to 40 people in view: no published memory budget found. Mafia: The Old Country's sources give none.

## 4. People the line supports

By the plan's own arithmetic against 6.0 GB: about 28 people (3 near at 100 MB, 25 passers-by at 20 MB) in an 800 MB people ceiling.

4-BUDGETS caps the street anyway at 3 near plus 12 passers-by (15 people); at up to 31 MB a passer-by that is about 670 MB, inside 800.

Against the 16 Nov grant of 4,711 MB, after steps 1 and 2, peak about 3,850 on the engine's counter (inferred: 5,072 less 160 less about 1,070), today's cast included, keeping 10% (about 470) spare: about 390 MB for added people and street copies. That is either up to 3 more near people plus 2 to 4 passers-by (at 31 or 20 MB), or the full 12 passers-by (the cap; 12 x 20 = 240, 12 x 31 = 372) with no added principal, and no further street copies. On Windows' counter the room is below zero until steps 3 and 4 land.

## 5. Risks

1. The line moves (Windows' budget read 9,427, 7,128, 5,771, 4,870, 4,711).
2. Two counters, about 260 to 490 MB apart; the plan mixes them.
3. Per-person cost counts textures only and is unmeasured on today's cast; 4K body maps are already in.
4. Strand hair is a fixed 256 to 392 MB peak whenever anyone with strands is near.
5. Epic's crowd tools are Experimental in 5.8.

## 6. Recommendation

Finish steps 1 and 2. Before adding people, run the 30 Sep ladder (0, 5, 10, 20 people) in the packaged walk, logging memreport, r.SkinCache.PrintMemorySummary, and Windows' budget and usage side by side; cap Character textures at 2048 first. Set the people ceiling from that ladder against the measured grant, not against 6.0 GB. Plan the passers-by as Epic's pattern: about 8 to 10 full MetaHumans near, the rest instanced at high LODs with card hair; strands only within 5 m (4-BUDGETS).

## Sources (read 17 Nov 2026)

- Platform support and LOD specifications for MetaHumans: https://dev.epicgames.com/documentation/metahuman/platform-support-and-lod-specifications-for-metahumans
- MetaHuman materials and textures: https://dev.epicgames.com/documentation/metahuman/metahuman-materials-and-textures?lang=en-US
- Controlling MetaHuman LODs: https://dev.epicgames.com/documentation/metahuman/controlling-metahuman-levels-of-detail-lods-in-unreal-engine
- MetaHuman Crowds in Unreal Engine: https://dev.epicgames.com/documentation/metahuman/metahuman-crowds-in-unreal-engine?lang=en-US
- Create MetaHuman Crowds: https://dev.epicgames.com/documentation/metahuman/create-metahuman-crowds-in-unreal-engine
- Texture streaming configuration: https://dev.epicgames.com/documentation/unreal-engine/texture-streaming-configuration-in-unreal-engine
- Virtual texture memory pools: https://dev.epicgames.com/documentation/unreal-engine/virtual-texture-memory-pools-in-unreal-engine
- Nanite virtualized geometry: https://dev.epicgames.com/documentation/unreal-engine/nanite-virtualized-geometry-in-unreal-engine
- Animation Budget Allocator: https://dev.epicgames.com/documentation/unreal-engine/animation-budget-allocator-in-unreal-engine
- Animation Sharing plugin: https://dev.epicgames.com/documentation/unreal-engine/animation-sharing-plugin-in-unreal-engine
- Forum, skin cache retains LOD0 entries (Epic staff reply): https://forums.unrealengine.com/t/metahuman-skin-cache-retains-lod0-entries-for-every-npc-regardless-of-camera-distance/2728166
- Mafia: The Old Country interview: https://www.unrealengine.com/developer-interviews/mafia-the-old-country-making-the-old-feel-new-with-unreal-engine-5?lang=ja
- PC Games Hardware, Mafia: The Old Country tech test: https://www.pcgameshardware.de/Mafia-The-Old-Country-Spiel-74877/Specials/Test-Grafikkarte-CPU-Systemanforderungen-Release-1479397/

## Unreached (not evidence)

- Performance and scalability settings for MetaHumans: the page body is a video only; no numbers read.
- City Sample page: body did not load.
- MetaHuman Crowds platform spawn limits: referenced, not shown.
