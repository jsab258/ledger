# Door passage for townspeople: method research, 9 Nov 2026

Nothing here is a project decision except the one recommendation at the end. "Read" means fetched or opened in full on 9 Nov 2026. Builds on RON-OFFICE-EXIT-2026-11-09.md, ROOM-EXITS-READING-2026-11-09.md (same folder) and production/research/field-scans/STREET-LIFE-2026-11-09.md; their content is not repeated.

## Questions

1. How is Unreal 5.x meant to route people through doors: navigation mesh with nav links and modifiers, Smart Objects, Mass ZoneGraph lanes, Detour crowd (docs and installed 5.8 source)?
2. Which capsule radius and cell size rules fit an 80 to 90 cm door?
3. How do shipped games (Kingdom Come II, Mafia, Hitman, RDR2) pass crowds through doors?
4. What is the smallest professional method for one street of about 30 people, and its cost?

## 1. Unreal's door routing

Engine source (C:\Program Files\Epic Games\UE_5.8\Engine, headers read 9 Nov; the .cpp files are not in the install, so generation internals are unread):

- Nav link proxy: Runtime\AIModule\Classes\Navigation\NavLinkProxy.h lines 25 to 32: simple links (PointLinks, point to point, static, an area class each) and at most one smart link per proxy. Smart links "can be dynamically toggled between enabled and disabled and provide different area classes for both cases ... without navmesh rebuilds". Lines 101 to 114: event ReceiveSmartLinkReached(Agent, Destination) when an agent reaches the link, ResumePathFollowing(Agent) hands control back, IsSmartLinkEnabled and a setter exist. So a door is: a smart link across the doorway; when the walker arrives, play the door clip, then resume. This is the engine's own pattern (matches Epic's page summary in ROOM-EXITS-READING).
- Runtime\NavigationSystem\Public\NavLinkCustomComponent.h lines 43, 69, 73, 101, 104: OnLinkMoveStarted, SetLinkData(start, end, direction), SetEnabledArea (swap area class, e.g. to a null area for a locked door), IsEnabled, SetMoveReachedLink delegate. Same mechanism in C++.
- Nav modifier volume: Runtime\NavigationSystem\Public\NavModifierVolume.h line 21 (class ANavModifierVolume). Epic's page (read, per ROOM-EXITS-READING): NavArea_Null blocks, an area class with extra cost discourages.
- Detour crowd: Runtime\AIModule\Classes\Navigation\CrowdManager.h lines 179 (UCrowdManager), 293 to 298 (MaxAgents, MaxAgentRadius, config); CrowdFollowingComponent.h line 38 (UCrowdFollowingComponent). Per-agent avoidance on top of an ordinary nav path; it needs a nav mesh and AI controllers. Defaults of MaxAgents were not read (unverified).
- Mass Smart Objects: Plugins\Runtime\MassGameplay\Source\MassSmartObjects\Public\ (13 headers: behaviour definition, fragments, user trait, request, SmartObjectZoneAnnotations). A search of these headers for "door", "building", "interior" finds nothing (grep 9 Nov): no door-specific support. Epic's Mass overview (https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-mass-gameplay-in-unreal-engine, read 9 Nov) says the SmartObject module "provides the required Traits, Fragments, and Processors to perform Smart Object queries"; it does not mention doors, buildings or ZoneGraph.
- ZoneGraph: Plugins\Runtime\ZoneGraph\Source\ZoneGraph\Public\ZoneGraphTypes.h exists (lane and tag types). Epic's ZoneGraph page returned only a contents heading (unread). ZoneGraph lanes are authored splines, so a lane could be drawn from a counter through a door; whether Mass is meant to cross interior thresholds this way is not stated in anything read (unverified).
- Project note (inference): the game's people are custom walkers (CrimeProbe.cpp straight-line capsule tests), not AI controllers. Nav mesh, smart links and Detour all assume a path-following component, so using them means either moving walkers onto it or sampling the nav mesh only as a path planner and keeping the existing walk for motion.

## 2. Radius and cell size for an 80 to 90 cm door

- Engine defaults, BaseEngine.ini lines 3053 to 3061 and RecastNavMesh.h 559 (CellSize 25 default in the struct), 566 to 567: CellSize 19, CellHeight 10, AgentRadius 34, AgentHeight 144, AgentMaxStepHeight 35, MaxSlope 44. Radius is documented "Radius of smallest agent to traverse this navmesh" (RecastNavMesh.h 728). A 34 cm radius needs 68 cm clear width, so an 80 cm door leaves 12 cm, less than one 19 cm cell.
- Mikko Mononen (Recast author), reply of 16 May 2013 23:34, https://groups.google.com/g/recastnavigation/c/k3jAZFAisDE (read 9 Nov): narrow-space handling "depends a lot on the ratio between the cell size and agent radius"; at least 2 to 3 voxels across a narrow space are needed to form a sliver of mesh; set cell size at least half the agent radius, giving a narrowest passable gap of about 1.5 times the radius. His first reply names aliasing of door frames against the voxel grid and an arch at head height failing the clearance test as other causes. A 2013 post: unchecked against current Recast.
- Reading (inference, not measured): with radius 34 and cell 19, an 80 cm door is within the aliasing risk. Two documented ways: a smaller radius and finer cell for the people (for example radius 25 to 30, cell 8 to 10, so the door spans 8 or more cells), or a link placed in the doorway that does not depend on mesh generation. The project's own capsule (30 cm, per RON-OFFICE-EXIT; whether this is radius or half-height is unverified) passes Tom's 34 cm one through the frame.
- Cost of finer cells: forum reports only (a Unreal thread says cell size 1 makes generation take too long; search summary, thread not opened, unverified). No figure for a 50 m street was found.

## 3. Shipped games

- Project studies (via ROOM-EXITS-READING, not repeated): Kingdom Come II doors are smart-object kinds with 2 sets of 6 stages from both sides; Mafia street doors mostly do not open and its civilians are removed 5 m out of view.
- Aron Granberg's A* Project docs, https://arongranberg.com/astar/docs/example_recast_doors.html (read 9 Nov): doors made as a navmesh cut over the opening, switched off when the opening animation begins. A middleware example, not a shipped game.
- Hitman: Absolution crowd talk abstract, https://gdcvault.com/play/1015315/Crowds-in-Hitman (read 9 Nov): 1,200 characters at 30 fps; the abstract says nothing about doors, buildings, spawn or despawn.
- Kingdom Come II: the GDC 2026 talk "Supporting Thousands of NPCs" (https://schedule.gdconf.com/session/supporting-thousands-of-npcs-in-kingdom-come-deliverance-kingdom-come-deliverance-ii/915120, https://gdcvault.com/play/1035718/Supporting-Thousands-of-NPCs-in) is listed; only a search summary, no doors content reached. Matej Marko's panel on the "Long Distance Move" behaviour is mentioned in press only.
- RDR2: a search found interiors coverage and horse/animal talks only; no source on townsperson door use or despawn (https://gamingbolt.com/red-dead-redemption-2-rockstar-talks-about-player-choice-dynamic-npc-interactions-indoor-environments-and-more is about player interiors; snippet only).
- Result: no shipped-game statement on how a crowd passes a door was reached. The methods above are Unreal's and middleware's, and the games' door clip sets exist, but "enter, hide, despawn" for these four games is unverified.

## 4. Smallest professional method for one street of about 30 people

Assembled from the sources above; the cost figures are estimates, not measured or sourced.

A. Authored door points, not a general nav mesh: each room gets a route graph in data (marks inside, a door mark, a street mark), as the diagnosis already outlines (inside point, door point, outside point, each leg through the existing walk). Same shape as an Unreal smart link and as Kingdom Come II's "link to a smart-object place" (study 01-npc-life.md lines 44 to 45), without needing path-following components. About 1 day for the route legs plus the seated stand-up; a person who cannot reach the door is a data fault caught by a test that walks every room's marks to the door.
B. Door passage: walk to the door mark, play the door clip (or none on a door left open), continue. Hide-or-despawn out of view is the fallback for rooms that fail the test (Mafia's method per the study). Half a day per door type.
C. Only if streets multiply or people must path around each other across open ground: add a nav mesh with Dynamic Modifiers Only, smart links at doors, Detour crowd; Epic's page says that mode is up to 50% cheaper in tile processing than Dynamic. Estimate 3 to 5 days; unmeasured; the radius/cell issue in section 2 applies.
D. Mass with ZoneGraph and Smart Objects: the STREET-LIFE note already says no source shows door entry working there; est. 2 to 4 days to find out.

## Not reached or unverified

- Epic pages blank on 9 Nov: ZoneGraph, Using NavLinkProxy and Smart Links, Smart Objects overview; Smrcek slides (redirect to an unrelated page); GDC KCD2 talk content; any Mafia or RDR2 technical talk on doors.
- Engine .cpp files for navmesh generation not in the install; Crowd manager default values not read.
- No project measurement of nav mesh build time, memory or Detour cost.

## Recommendation

Use method A and B: a data route per room (inside point, door point, street point) walked by the existing walker, a door clip at the door, an every-room test that walks marks to the door, and out-of-view removal as the fallback; keep the nav mesh with smart links (C) as the upgrade, with a finer cell and smaller radius for the people, only if open-ground crowd avoidance becomes needed. About 1.5 days for one street, estimated.
