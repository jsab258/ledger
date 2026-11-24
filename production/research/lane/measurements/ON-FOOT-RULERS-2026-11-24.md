# On-foot rulers: footage with readouts, world units, heights, repeating features (24 Nov 2026)

Built on: ON-FOOT-PUBLISHED-2026-11-24.md and ON-FOOT-FOOTAGE-QUESTIONS-2026-11-24.md (their sources are not repeated). All pages read 24 Nov 2026. CONFIRMED = read on the page's own text; UNVERIFIED = search-result summary only, or inference.

Overall: no clip was found that is shown to hold an on-screen speed or coordinate readout during on-foot movement. The fetch tool returns only YouTube's footer for watch pages (title only), so length, upload date and readout legibility of every clip below are UNVERIFIED; none was watched.

## Question 1. Footage with an on-screen readout

### GTA V
- Search (YouTube-only filter) returned one candidate for a position readout: "Player Location Display - GTA 5 PC Mod", https://www.youtube.com/watch?v=BX9IoxhCcTk . Title confirmed from the page header; length, date, content NOT read. The mod it names (PLD v3.50, https://www.gta5-mods.com/it/scripts/player-location-display-v3-50 , via search summary) shows street/area names bottom-left, not X/Y/Z, so it is a poor ruler. UNVERIFIED.
- A mod that does show X/Y/Z on screen: "Coordinates (X,Y,Z) and Angle Tracker 1.0", https://www.gta5-mods.com/scripts/coordinates-x-y-z-and-angle-tracker . Page text (read): "captures and displays your current X Y Z coordinates along with your angle"; F9 toggles; uploaded 21 Aug 2026, updated 22 Aug 2026; no video on the page. No YouTube clip of it found.
- "Coordinates & Heading dumper 1.1" (https://www.gta5-mods.com/ms/tools/coordinates-heading-dumper , search summary): writes coordinates to a .txt file on key press, no on-screen readout. UNVERIFIED.
- On-foot speedometers: search summaries state the speedometer mods found are vehicle-only (Complete SpeedoMeter, https://www.gta5-mods.com/cs/scripts/complete-speedometer ; Speedometer Simple, https://www.lcpdfr.com/downloads/gta5mods/scripts/53080-speedometersimple/ ); one user request for an on-foot readout was reported. UNVERIFIED (summary only).
- Simple Native Trainer coordinate option: only named by a search summary, not read.
- Clips usable as a ruler: none confirmed.

### RDR2
- Native trainer on Nexus, https://www.nexusmods.com/reddeadredemption2/mods/45 : page returned HTTP 403. A search summary says its options include "show coordinates and/or speed", infinite stamina, super jump, save/teleport coordinates (GTA IV-style simple native trainer). UNVERIFIED.
- YouTube trainer videos found by title only (no readout evidence in their titles): Rampage Trainer install https://www.youtube.com/watch?v=0QaVDLeYky0 ; jedijosh920 trainer/mod menu https://www.youtube.com/watch?v=dfzLH-Wj3oI ; "RDR 2 Lenny's Simple Trainer" https://www.youtube.com/watch?v=7FauOuWbAtE ; FLiNG https://www.youtube.com/watch?v=AH5mTi_nlkA ; "How to Use Trainer in RDR 2 PC" https://www.youtube.com/watch?v=K1J1lhR8rS0 . Whether any shows a coordinate or speed readout on foot: NOT known.
- Clips usable as a ruler: none confirmed.

### KCD2 (and KCD1)
- KCD2 console command for position: `wh_rpg_getLocation` (prints three comma-separated numbers; `goto x, y, z` teleports). Source is a search-result summary only; the PC Gamer page https://www.pcgamer.com/games/rpg/kingdom-come-deliverance-2-console-commands-cheats returned only navigation text in two fetches, and PCGamesN https://www.pcgamesn.com/kingdom-come-deliverance-2/console-commands-cheats (read) lists only `goto` ("Teleports you to entered coordinates") with no position print. So existence of a position print is UNVERIFIED. It prints on demand (one reading per command), not a live overlay.
- KCD1 command `wh_pl_fasttravelto x y z`, example for Rattay's Pillory "2534.91 568.23 80.54": https://kingdomcomedeliverance.wiki.gg/wiki/Cheat_codes (read). Takes coordinates, shows none. The page lists no on-screen position or speed command.
- `r_displayinfo`, `cl_showpos`: no source found for either in KCD1 or KCD2. UNVERIFIED (not found).
- YouTube console-command videos found by title only: https://www.youtube.com/watch?v=z9uY80RFRDA (title confirmed "Using Fun Console Commands in Kingdom Come Deliverance 2"), https://www.youtube.com/watch?v=z2DThiTMd1k , https://www.youtube.com/watch?v=qIrzoyzzGl8 , https://www.youtube.com/watch?v=9QCSQDjo348 . Content NOT read; no evidence of an on-foot run with a readout.
- Clips usable as a ruler: none confirmed.

## Question 2. World unit

- GTA III, Vice City, San Andreas: "Each standard unit is precisely one meter in length" (https://www.grandtheftwiki.com/Unit , read). The page does not cover GTA IV or V.
- GTA V: no page stating 1 unit = 1 m found. A search summary of the FiveM natives page for SET_ENTITY_COORDS (https://github.com/citizenfx/natives/blob/master/ENTITY/SetEntityCoords.md) says Z is ground level with an offset by the entity's radius; units not stated. UNVERIFIED. The two nearest facts: GET_DISTANCE_BETWEEN_COORDS exists as a native; no scale statement read.
- RDR2: a modding forum thread (https://www.rdr2mods.com/forums/topic/1486-placing-a-ped-at-a-location , read) logs "distance to trapdoor is 0.831077" via GET_DISTANCE_BETWEEN_COORDS; the thread does not state the unit. UNVERIFIED.
- KCD2: no statement found. CryEngine documentation says 1 metre = 1 unit (search summary of https://www.cryengine.com/docs/static/engines/cryengine-3/categories/1114113/pages/1310751 ; both CryEngine pages fetched returned only navigation within the first 100,000 characters, rest not read). Engine-level only; KCD2's own scale UNVERIFIED. KCD1 coordinate example above (x 2534.91, y 568.23, z 80.54 for Rattay) is consistent with a metre-scale map of several km but proves nothing alone.

## Question 3. Player character heights

All are community estimates; no official in-game unit figure found.
- GTA V: Gamerant, https://gamerant.com/gta-playable-characters-estimated-height/ (read): Franklin about 6'0" (183 cm), Michael 6'2" (page prints "180cm", which is inconsistent; 6'2" = 188 cm), Trevor about 6'1" (185 cm). The page states "Rockstar has never officially released information"; the figures come from Reddit comparisons; no game-file values.
- RDR2: Arthur about 6'1" (185 cm) in most search hits (e.g. https://expertbeacon.com/how-tall-is-arthur-morgan/ , summary only, SEO site); one hit says 6'2". John Marston 5'11" in one hit. No Rockstar figure; sources weak. UNVERIFIED.
- KCD2 Henry: no height found. The only figure surfaced is a collectible marionette, about 50 cm (https://henry.marionettes.cz/ , summary only), not the model. Not a ruler.
- Game-file model heights (ped bounding box, skeleton): not found for any game.

## Question 4. Repeating world features

- Nothing found for GTA V, RDR2, KCD1 or KCD2 (sleepers, lamp posts, fence posts, kerb stones). One search returned "Track Recorder" (https://www.gta5-mods.com/de/scripts/track-recorder) which records train track coordinates for GTA V (summary only; reported not working on game version 1.57); no spacing figure. UNVERIFIED.
- Real-world sleeper figures surfaced (not game data): TxDOT manual 18 or 19.5 in on centre (about 0.46 to 0.50 m), https://onlinemanuals.txdot.gov/TxDOTOnlineManuals/TxDOTManuals/rho/track_design.htm (summary only).

## Not reached
- YouTube: watch pages return footer only through the fetch tool (title only); search results page returned footer only. No length, date or readout check was possible on any clip. Search engine indexes few YouTube pages.
- https://www.nexusmods.com/reddeadredemption2/mods/45 (HTTP 403)
- https://www.pcgamer.com/games/rpg/kingdom-come-deliverance-2-console-commands-cheats (body not returned, two tries)
- https://www.gamesradar.com/games/action-rpg/kingdom-come-deliverance-2-cheats-console-commands (title only)
- https://www.deltiasgaming.com/?p=134584 (HTTP 405)
- CryEngine measurement-reference pages (body beyond 100,000 characters not read)
- GTA V ped capsule/bounding data; RDR2 and KCD2 world-unit statements; any KCD2 modding page with Henry's height.
