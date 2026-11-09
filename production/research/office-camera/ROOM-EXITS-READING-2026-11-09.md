# Room exits: how the references and Unreal 5.8 move people through doors (read 9 Nov 2026)

No decision here. "Read" means fetched in full by the helper on 9 Nov 2026; "snippet" means seen only in search results (unverified).

## 1. How Kingdom Come II and Mafia move townspeople between inside and outside

Found in the project's own studies (read in full for the cited lines, 9 Nov):

- **Kingdom Come II, daily life.** People sleep indoors (1,256 beds for about 1,320 people); the 726 fillers "come out through a door by day", hours unverified. Source: production/research/aaa-reference/studies/01-npc-life.md line 37. Doors are 619 working ones in the city (04-street-world.md line 40) and each opens to a keep-unlocked window, default 07:30 to 19:30 (F:/LedgerTools/aaa-study/kcd2/study-11-15/s11/NOTES.md line 61). Moving between rooms is a scheduler "link" to a smart-object place, with a use action (01-npc-life.md lines 44 to 45).
- **Kingdom Come II, animation.** Doors have 2 sets of 6 stages, from front and back (07-animation.md line 53; kcd2/study-7/FINDINGS.md line 34: 120 rows). The male set holds 21 door fragment ids with 108 options. Doors are a smart-object kind, with a use distance of 2.0 (kcd2/study-9-10-13/NOTES.md line 110, a Lua default). The interaction filter lists 4 door interactions (line 45).
- **Kingdom Come II, navigation.** The studies hold no navigation or door-link data. Search results (snippet, unverified) say the original game used a nav mesh with A* (Smrcek's 2018 slides, not readable: the PDF redirected away) and a "Long Distance Move" behaviour; a GDC talk, "Supporting Thousands of NPCs in KCD and KCD II" (Smrcek), covers AI level of detail. Its pages (GDC schedule, gamedev.net) returned 403, so what it says about doors, teleporting or interiors is not confirmed.
- **Mafia (Definitive/Old Country, whichever the study used).** Most street doors are leaves that do not open (04-street-world.md line 39, "R, I"). People loop a scene on a smart object (389 scenes, 478 slots); 374 scenes carry their own person, who appears when the scene streams in (01-npc-life.md line 39). Civilians are removed 5 m out of view or with their streamed cell, and freeze unseen beyond 70 m (line 51). Mafia has no schedule (line 38). Its checkpoint rows carry a teleport flag (19 of the rows; kcd2/study-16/mafia/NOTES.md line 18), which concerns the player, not townspeople.
- **Not confirmed in any source read:** whether either game uses nav-mesh door links, teleport-while-unseen, or scripted routes for a person leaving a room. The data show smart objects and door animation sets, which fits "walk to the door point, play the door clip", but this is an inference (I), not a statement by the developers. No developer talk or article was reached that says it.

## 2. What Unreal 5.8 offers

Read in full, 9 Nov 2026:

- Navigation System overview, https://dev.epicgames.com/documentation/en-us/unreal-engine/navigation-system-in-unreal-engine : mesh built from collision geometry in tiles of polygons; three modes (Static, Dynamic, Dynamic Modifiers Only); agent avoidance by RVO or Detour Crowd. The page gives no memory or build-time figures.
- How to modify the navigation mesh, https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-how-to-modify-the-navigation-mesh-in-unreal-engine : Nav Modifier Volumes (NavArea_Null blocks, Obstacle raises cost, LowHeight blocks agents that do not fit). Nav Link Proxy joins two areas with no direct path, one-way or both ways; the link must touch the mesh and join adjacent tiles. A Smart Link is a Nav Link Proxy with Blueprint logic (event "Smart Link Reached", then resume path following). Static mode: built offline, never changes. Dynamic Modifiers Only: modifiers and links update at runtime, with collision cached, "up to 50% cheaper" tile processing. Dynamic: most expensive; Epic says the guide's examples are for demonstration only.
- Smart Objects landing page, https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine : "a set of activities in the level that can be used through a reservation system"; the page itself has no detail on doors. Its Overview and Quick Start sub-pages came back empty (table of contents only) and are unread.
- Nav Link Proxy overview page, and Mass / ZoneGraph pages: the fetch returned only a table of contents or was not tried. Unread. Search snippets only: smart links are created through a nav link custom component; a runtime toggle exists (Set Smart Link Enabled).
- **Documented cost of a small nav mesh for a 50 m street:** no Epic page read gives one. Unverified. Not measured in the project.

## 3. Do the NPCs open doors on screen?

- Both games carry door animation: Kingdom Come II's 2 x 6 stages from both sides, and Mafia's roughly 190 door-named clips (18 in its world folder) (07-animation.md lines 49 and 53). Whether townspeople, not only the player, use them is not stated in any source read. The 726 "extras" coming out through a door (01-npc-life.md line 37) suggests it for Kingdom Come II, as an inference.
- No documented counts or timings of a person passing a doorway, with or without animation, were found. For Mafia, the street doors that do not open (04-street-world.md line 39) point to people appearing or being removed out of view, not crossing a threshold; this is inferred.
- The gap is a test case: a short film of a Kingdom Come II townsperson leaving a house would settle it; the project's extracted data cannot.

## Unreached or unread

- GDC schedule page and gamedev.net write-up of the Warhorse NPC talk (403). GDC Vault page (not fetched).
- Smrcek's navmesh slides (redirected away).
- Epic: Smart Objects Overview and Quick Start, Nav Link Proxy page, Mass and ZoneGraph pages.
- Mafia developer talks: none searched for successfully.

Relevant local diagnosis: production/research/office-camera/RON-OFFICE-EXIT-2026-11-09.md (read 9 Nov).
