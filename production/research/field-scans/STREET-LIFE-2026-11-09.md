# Field scan: street life at density, 9 November 2026

Read 9 Nov 2026. Not repeated: CROWD-2026-11-08, CROWD-DISTANCE-2026-11-09, PEOPLE-IN-MOTION-2026-11-08. Nothing decided here.

## Questions

1. How do studios keep routines (who is where, when) cheap for many people?
2. How do people enter, leave and use shops and doors, and idle or stand in groups?
3. How do they react to the player or to events?
4. What does Epic's Mass stack offer for 1 to 3, and what does it cost?
5. What is the cost per person, and what fits a 6 GB card?

## Findings

**Routines (Q1).** Kingdom Come II: nearly 2,400 NPCs on the map, about half in one city, all "doing their daily routines and reacting to player actions even when the player is long gone". Warhorse's answer is an AI level of detail that scripts do not see, so content authors write one routine and the engine changes fidelity underneath. The slides and any frame or memory figures are members-only: not reached [1]. Reading of this for a one-street game: the routine is data (place, time, action), and detail is only added near the player.

**Doors, shops, idling (Q2).** Epic's Mass SmartObject module supplies traits, fragments and processors for Smart Object queries and "simple agent behaviors". Smart Objects are "a set of activities in the level that can be used through a reservation system" [2][3]. That is the documented route for a counter, a bench, a doorway or a shop window. The pages read are landing pages: no slot, claim or door-entry detail, no numbers. The Smart Objects overview and quick-start pages loaded blank: unreached [2][4]. No source reached shows people going inside a building in Mass; a search found none (unverified). A community MIT project shows an entity claiming a Smart Object, using it and releasing it, and a wander task; no routines [5].

**Reactions (Q3).** Mass StateTree gives each entity its own StateTree, updated by named signals from other systems; signals carry no payload [3]. Hitman: Absolution's crowd agents are reported as each having a "mini AI brain" (press, secondary) [6], and Intel's Hitman deck is said to describe agents that can be upgraded on demand to full NPCs for scripted acts (via search summary only, deck too large to open: unverified) [7]. Reading: cheap shared state for the many, a promotion to a full character for the few who talk or react visibly.

**Counts and LOD (Q4, Q5).** Mass Gameplay picks per LOD one of four forms: high-resolution Actor, low-resolution Actor, instanced static mesh (cheapest, vertex animation possible, experimental) or nothing. Simulation LOD groups entities into chunks and varies update rate. Each LOD level has a configurable distance and a maximum count; the page gives no values [3]. Hitman: Absolution: 1,200 characters at 30 fps on consoles (GDC 2012 abstract) [8]. The MIT demo shows about 50,000 entities with 3 LODs in Niagara, a static display, author's figure, hardware not stated [5]. A community Mass tutorial (ICVR, 18 Dec 2025) lists ZoneGraph, StateTree, Smart Objects and AnimToTexture but its body was not reached [9].

**Cost per person.** No source reached gives milliseconds or megabytes per person for a skinned character on an RX 6700-class card. Earlier scans give Kingdom Come II 70 people at full detail within 150 m and a 3.5 ms budget (local study, unverified here), and a 5.8 report that Mass skinned instances leak animation tracks (unverified). One street holds perhaps 20 to 40 people, far below every count above: the open risk is memory per distinct look, not routine logic.

## Not reached

KCD2 talk slides; Intel Hitman deck (10 MB limit); Epic Smart Objects overview and quick-start (blank); Zone Graph page; Mafia: The Old Country (no public technical talk found); City Sample crowd documentation; recent research papers (not searched to a primary source). Absence of evidence for door entry in Mass is unverified.

## Sources (read 9 Nov 2026)

1. https://gdcvault.com/play/1035718/Supporting-Thousands-of-NPCs-in (abstract page only)
2. https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine
3. https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-mass-gameplay-in-unreal-engine
4. https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-overview-in-unreal-engine (blank)
5. https://github.com/Ji-Rath/MassAIExample
6. https://gdcvault.com/play/1015315/Crowds-in-Hitman (abstract); "mini AI brain" from a search summary of press coverage
7. Intel deck, URL via search only, not opened
8. same as 6
9. https://forums.unrealengine.com/t/community-tutorial-designing-scalable-crowds-with-mass-ai-a-comprehensive-ue-guide/2686225 (summary post only)

## Recommendation

Choose the method by measurement, not by source: build one street-life test with 10 to 20 people on Mass with Smart Objects (one shop door, one bench, one pair talking) and StateTree routines from a time table, record milliseconds and card megabytes per person on the RX 6700 class, and try door entry first because no source shows it working. Keep the routine table as plain data so it survives a change of engine route. Estimated cost, unsourced: two to four days.
