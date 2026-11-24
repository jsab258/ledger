# On-foot speeds: published figures (24 Nov 2026)

Reader's notes for ON-FOOT-FOOTAGE-QUESTIONS-2026-11-24.md, questions 1, 2, 3, 5 (question 4 only as a short list at the end). All pages read on 24 Nov 2026. Facts and sources only; no synthesis. Marking: CONFIRMED = read on the page itself; UNVERIFIED = seen only in a search result summary, or a player's own claim, or an inference.

Overall result: no published walk, run or sprint speed in m/s was found for RDR2, KCD2 or GTA IV. For GTA V one documented value (a native's description, second-hand through a forum post) and one listicle figure (not read on its page). Almost every page that was reached holds mod settings (multipliers), not speeds.

## Question 1. Published figures

### GTA V

1. Native SET_PED_MOVE_RATE_OVERRIDE, as quoted in a FiveM forum post.
   - Source: https://forum.cfx.re/t/ped-speed/4771125 , post by "Qubit", 18 Oct 2021, read 24 Nov 2026. The post cites the FiveM natives reference https://docs.fivem.net/natives/?_0x085BF80FA50A39D1 (that page did not render its entry through the fetch tool, so the reference itself was NOT read).
   - Figure as reported in the post: range "Min 0.00, Max 10.00"; at 10.00, "Sprinting without fast run cheat: 66 m/s", "Sprinting with fast run cheat: 77 m/s".
   - How obtained: native documentation text, written by the native-database contributors (method of their measurement not stated; game-file or in-game test unknown).
   - Conversion (arithmetic, not a published figure): 66 m/s / 10.0 = 6.6 m/s per unit rate; 77 / 10.0 = 7.7 m/s. If the effect is linear and the default rate is 1.0, sprint would be about 6.6 m/s without the cheat. Linearity and the default are UNVERIFIED; the same thread's other post says the rate resets to 1.0 unless re-called.
   - Status: second-hand, partly unverified.
2. Sportskeeda article (search-result text only; the page returned HTTP 405 and was not read): https://www.sportskeeda.com/gta/reasons-make-franklin-best-three-gta-5-protagonists . The search summary reported "normal" speeds of about 22, 23 and 24 km/h and "tab run" speeds of 26, 26 and 28 km/h for the three protagonists (order as the summary gave it: Trevor, Michael, Franklin).
   - Conversion if correct: 22 km/h = 22 / 3.6 = 6.11 m/s; 23 = 6.39; 24 = 6.67; 26 = 7.22; 28 = 7.78 m/s.
   - How obtained: not known. UNVERIFIED; not read in full; a listicle.
3. Mod multipliers (not speeds): the SetRunSprintMultiplierForPlayer native is described as capped at 1.49 ("1.49 is the maximum", user Fourthbeam, 21 Apr 2019) at https://forum.cfx.re/t/help-how-do-i-increase-the-players-run-walk-speed/260395 (read 24 Nov 2026). No default speed given.
4. Native signature page (search result only): https://www.lcpdfr.com/resources/nativedb/index/player/page/3/?d=39 - not read in full.

### RDR2

- No m/s, km/h or mph figure for Arthur's walk, run or sprint found.
- Nexus mod page https://www.nexusmods.com/reddeadredemption2/mods/6359?tab=docs returned HTTP 403 (not read). A search summary quoted its settings ranges "Walking Speed [Max 2.5, Min 0.1]; Running Speed [Max 10.0, Min 3.0]": multipliers/unknown units, UNVERIFIED, not a speed.
- Walk across the whole map, unhurried: 3 h 14 min by Reddit user GAME-LAPSE, reported on a mirror site (https://plumsweet.pages.dev/posts/gorgeous-red-dead-redemption-2-time-lapse-video-shows-walk-across-the-entire-map), via search summary only, no distance. UNVERIFIED, no speed derivable.
- Rockstar's GDC 2020 talk "Filling Marston's Boots: Player Locomotion in Red Dead Redemption 2", Mike Jones. Description read at https://gdconf.com/news/learn-secrets-red-dead-redemption-2s-player-locomotion-gdc (24 Nov 2026): no numbers on the page. Not confirmed that the talk was held or recorded (the page mixes GDC 2020 text with a 2027 header). Slides/video not found.

### Kingdom Come: Deliverance II

- Wiki page https://kingdomcomedeliverance.wiki.gg/wiki/Speed (read 24 Nov 2026): no numbers; says Speed derives from Agility, inventory weight, armour and weapons. Does not name KCD2.
- Steam discussion pages for KCD2 (app 1771300: 592892850991102651, 601895828709226977, 732501101224394925, 601895917151332854) loaded without any posts through the fetch tool; their content was NOT read. A search summary attributed to one of them a user claim "walking speed at Agility 30 is 2 m/s": UNVERIFIED, player claim, not read at source, thread not identified with certainty.
- Nexus page https://www.nexusmods.com/kingdomcomedeliverance2/mods/2148 : HTTP 403, not read. A search summary says it tells modders to edit soul_archetype_movement.xml (NPC walk, run, sprint speed). UNVERIFIED. No values seen.
- No developer statement on KCD2 on-foot speed found.

### KCD1 (related, not asked; included as the only nearby figures)

- Developer interview, GameBanshee write-up 4 May 2014 (interview 2 May 2014 per the page): an unnamed Warhorse developer: "In Kingdom Come: Deliverance it took 7 minutes to run from the city to stable, which is about 1.5 km." Source: http://www.gamebanshee.com/fc3a , read 24 Nov 2026 (the page quotes the developer; the 2 May date came from the page's link, read second-hand).
  - Conversion: 1500 m / (7 x 60 s = 420 s) = 3.57 m/s average (12.9 km/h). Pre-release 2014 build; the route is not stated as straight; "run" not defined. Not applicable to KCD2 without a check.
- Forum player estimate, https://forum.kingdomcomerpg.com/t/walking-pace-and-running/8533?page=2 (read 24 Nov 2026): user Jlyga_u_onacHa, 25 Oct 2014: alpha build default running speed "16-18 km/h", judged from the character's shadow. Conversion: 16 / 3.6 = 4.44 m/s; 18 / 3.6 = 5.00 m/s. Player estimate, alpha build, method loose: UNVERIFIED as a game value.
- Same thread: real-life walking, not game values: LordCrash (6 Apr 2014) 6 to 7 km/h = 1.67 to 1.94 m/s; Lieste (2 May 2014) 6.5 km/h = 1.81 m/s sustained, "around 8 km/h" downhill = 2.22 m/s. Real-life estimates; in the second case from GPS-tracked walks (also https://forum.kingdomcomerpg.com/t/terrain-influence-on-the-character-movement/17470, Lieste, 8 Sep 2014: 6.5 km/h level, up to about 8.5 km/h downhill, 3.2 km/h on a 40% uphill).

### GTA IV

- No on-foot speed figure found. Kotaku, 15 Oct 2015, https://kotaku.com/patient-man-walks-across-every-grand-theft-auto-game-1736620434 (read 24 Nov 2026): reader "Conor" walked each GTA map corner to corner as timelapse; GTA V (Los Santos) about 52 minutes, whole series about 4 h 40 min; no time or distance given for GTA IV, no distances for any game. No speed derivable.
- Nexus GTA IV mod https://www.nexusmods.com/gta4/mods/547 appeared in search; not read.

## Question 2. Standing to full run, and run to standing

Nothing published found for any of the four games (no time, distance or acceleration curve). Pages that could hold it and were not reached or not read: RDR2 GDC locomotion slides; Rockstar animation-pipeline documents (a site "rockstar-files.pages.dev" appeared in a search; it looks like leaked-document material and was deliberately not opened).

Method note from a search result (general, not game-specific): root-motion speed of a clip is the root-position difference over the frame time, per frame (https://forum.babylonjs.com/t/objects-movement/10054, not read in full). No source found that has done this for any of the four games' clips.

## Question 3. Known lengths on screen

- Nothing found with a published length for a pier, runway, bridge, street or rail sleepers in GTA V, RDR2, KCD2 or GTA IV.
- GTA V map scale, search result only (not read): a fan scale map by Reddit user CptLande (https://www.gtaboom.com/fan-creates-gta-v-map-correct-scale/); Los Santos land area about 29 sq mi vs Los Angeles 4,700 sq mi, ratio about 1:160 (expertbeacon / similar blog, unnamed method). UNVERIFIED.
- KCD1: 1.5 km city-to-stable route (above), a route not a visible feature.
- Character's own stride as ruler: no published stride length or step rate for any of the four games. The clip files (GTA V move_*.ycd names appear on mod pages such as https://www.gta5-mods.com/ca/misc/faster-player-movement, search result only) hold the data but no one's measurement was found.

## Question 5. Not reached, and unverified

Not reached or not readable (fetch refused, empty, or error):
- https://www.sportskeeda.com/gta/reasons-make-franklin-best-three-gta-5-protagonists (HTTP 405)
- https://www.nexusmods.com/kingdomcomedeliverance2/mods/2148 (HTTP 403)
- https://www.nexusmods.com/reddeadredemption2/mods/6359?tab=docs (HTTP 403)
- Steam KCD2 discussion pages (four listed above) and KCD1 Steam thread https://steamcommunity.com/app/379430/discussions/0/787664259085524724: loaded with no posts
- https://docs.fivem.net/natives/?_0x085BF80FA50A39D1 and https://nativedb.dotindustries.dev/gta5/natives/0x085BF80FA50A39D1 (no entry text returned); raw FiveM native-decls file (404). The alloc8or natives.json was returned only for the first 100,000 characters of 2.78 million, entry not reached.
- https://www.gta5-mods.com/scripts/simple-foot-controls (pending approval, no text)
- https://wiki.gtaboom.com/wiki/You_Can_Walk_Across_The_GTA_Franchise_In_5_Hours (host not found)
- RDR2 GDC locomotion slides or video; the GDC Vault was not searched.
- Rockstar internal documents (not opened on purpose).

Unverified: the 66 / 77 m/s native figures' origin and linearity; the Sportskeeda km/h values; the KCD2 "2 m/s" player claim; the KCD1 alpha 16-18 km/h; the RDR2 mod ranges; GAME-LAPSE 3 h 14 min.

Not searched at all: Nexus/GitHub datamines of KCD2's movement files (soul_archetype_movement.xml values), RDR2 native lists on GitHub, YouTube measurement videos with distances, speedrun.com GTA IV / GTA V resources, Reddit threads (search tool results rarely include them).

## Question 4 (short list, not watched)

Links met on the way: none for clips. Only the time-lapse mentions above (GAME-LAPSE RDR2 map walk, mirror link above; "Conor" GTA map walks, Kotaku link above). Neither verified as uncut, steady-camera or fit for timing.
