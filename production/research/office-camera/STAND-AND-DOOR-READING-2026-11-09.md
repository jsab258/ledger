# Stand up and door: first reading, 9 Nov 2026

No synthesis or decision. All links read 9 Nov 2026. Caveat: the fetch tool returns a model summary of a page, not raw text, so "read" below means the page was fetched and summarised, not seen verbatim (unverified wording).

## 1. Kingdom Come (CryEngine): seated NPC to walking

Not found. No Warhorse wiki page, devblog or talk reached says how a seated NPC rises: no stand-up clip length, no statement on whether navigation starts during it. Unverified either way.

Only indirect evidence, all community, not Warhorse:
- Nexus forum thread summarised through a search result (the page itself returned 403, so it is a snippet, unverified): a reply says which side an NPC rises from looks hard-coded; an exit animation plays, after which the NPC stands at the furniture's "entry/exit" marker. https://forums.nexusmods.com/topic/9417698-make-npcs-player-use-furniture-without-the-enter-furniture-animation
- The project's own studies (read earlier): KCD2 furniture and doors are smart-object kinds with a use action (aaa-reference/studies/01-npc-life.md lines 44 to 45; 07-animation.md line 53). This is data, not method.

## 2. Kingdom Come: doorway handling

Not confirmed. From the project's studies (see ROOM-EXITS-READING-2026-11-09.md): doors have 2 sets of 6 animation stages, front and back; a door smart-object use distance of 2.0 (Lua default); 4 door interactions. Door link, approach points and width: none found.
- GDC 2026 talk "Supporting Thousands of NPCs in KCD and KCD II" (Smrcek): the vault page gives only an overview (about 2,400 NPCs in KCD2, AI level of detail); nothing on doors, interiors or sitting. Full talk members-only, not reached. https://gdcvault.com/play/1035718/Supporting-Thousands-of-NPCs-in
- modding.wiki scripting tutorial returned only a title; the CrumblyLiquid resource list names no furniture, door or navigation page. https://modding.wiki/en/kingdomcomedeliverance/developers/scripting-tutorial ; https://gist.github.com/CrumblyLiquid/a7d9c6d9077ae362b2b7deaad8259409
- Warhorse's modding tools were not used, as ordered.

## 3. Unreal Engine 5 Smart Objects, nav links

Smart Objects overview (Epic), https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine---overview :
- Slot states: Free, Claimed, Occupied.
- Pattern: the agent searches, calls ClaimSmartObject and gets a claim handle (an invalid handle means try another result); asks the slot's location or transform from the handle; "The Agent can use any desired navigation method to reach its destination"; on arrival calls Use (Claimed becomes Occupied) and receives the Behavior Definition; releases when done or aborted ("Agents are responsible for releasing their claimed Slots"). If the object's state changes, the engine releases the slots and notifies through OnSlotInvalidatedDelegate.
- A slot has only a transform relative to its anchor; no separate entry or exit point is described. Behavior Definitions (Mass Entity or Gameplay Behavior) hold the data; smart objects "do not contain execution logic".
- Version warning (search result, unverified): later versions deprecate Release for MarkSmartObjectSlotAsFree; call names differ by engine version. Community advice (not official): release on every exit path.
- The page says nothing about doors or stand-up timing.

Nav Link Proxy, smart links (Epic): the dedicated page returned only a table of contents (https://dev.epicgames.com/documentation/en-us/unreal-engine/using-smart-links-in-unreal-engine), unread. The earlier reading (ROOM-EXITS-READING-2026-11-09.md section 2) holds what was read: a Nav Link Proxy joins two areas, one-way or two-way, and a Smart Link runs Blueprint logic on "Smart Link Reached" before path following resumes. Mass and ZoneGraph pages: unread.

## 4. Other methods for leaving small rooms without a navmesh

No studio talk or postmortem found. Only forum advice:
- A* Pathfinding Project forum, Aron Granberg: keep doors out of the navmesh entirely; the mover checks the full path for doors it will cross and opens them within a set distance when heading for them; one-way doors use navmesh links, with tags for keys. https://forum.arongranberg.com/t/rooms-doors-and-walls-question/4340
- Same forum (search result, unverified): waypoint-following agents cut corners if the "pick next waypoint distance" is too large; lowering it to about 0.5 to 1 is suggested.
- GameDev.net navmesh article (search result, unverified): waypoint networks were used in the past to save resources; an agent may leave the network to reach a destination.

## Project's own measurements already on file (read)

- SIT-BOW-2026-10-30.md lines 35 and 77: Epic's stand-up clip (out_to_stand) head height 87.8 cm; the table at line 77 lists Epic's stand-up at 0.43 s and 0.86 s (column meaning not confirmed by this reading).
- 07-animation.md line 84: Epic's sample bench is built on smart objects: approach clips from five sides, an idle loop and a stand-up.
- RON-OFFICE-EXIT-2026-11-09.md: the walk code has no stand-up step; door at the west end; inside point about 6.0, outside about 4.35.

## Could not be reached

- Warhorse GDC 2026 talk body (members-only); GDC schedule page; gamedev.net write-up (403).
- Smrcek 2018 navigation slides (redirected away).
- Nexus furniture thread (403).
- modding.wiki scripting tutorial body (title only); the unofficial KCD docs and Warhorse's own modding wiki pages (not fetched).
- Epic Nav Link Proxy / smart links page (table of contents only); Mass and ZoneGraph pages (not tried).
- Any studio postmortem on waypoint graphs for rooms.
