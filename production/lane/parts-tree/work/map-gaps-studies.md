# Open items mapped to the parts tree (task d)

Built 19 November 2026 from the sources named in each table. Part ids are those of production/lane/parts-tree/SKELETON.txt. COVERED means a part exists whose job includes the item. GAP means no part holds it; the proposed new part and its parent follow (codes G1 to G12 are defined in the Gaps list at the end). A study "blind spot" about another game's data is covered when the LEDGER part it would inform exists; the hole itself is research, noted in the item.

Study short names: S01 npc-life, S02 first-30-minutes, S03 dialogue-barks, S04 street-world, S05 visuals, S06 characters-wardrobe, S07 animation, S08 sound, S09 camera-controls, S10 interface, S11 systems, S12 tech-budgets, S13 pipeline, S14 combat, S15 crime-toolkit, S16 jobs-story, S17 yakuza-shenmue, S18 gta6-first-read. All under production/research/aaa-reference/studies/.

## 1. The 18 studies (blind-spot, not-reached and unverified items)

| # | Source:line | Item | Parts | Status |
|---|---|---|---|---|
| 1.1 | S01:102 | Both engines' code: scheduler scoring, perception formula, time units in script settings | 2.1.1, 2.2 | COVERED (research hole) |
| 1.2 | S01:103 | Mafia reaction rules, bark table, faction attitudes, cooldowns (compiled, not exported) | 2.5.3, 3.6.4, 2.4.3 | COVERED |
| 1.3 | S01:104 | People on screen per street by hour | 2.1.2, 5.1.5 | COVERED |
| 1.4 | S01:104 | Usable objects per street | 1.6.8, 4.4 | COVERED |
| 1.5 | S01:104 | Reactions to the player (greetings, stepping aside) and to noise | 3.6.4, 2.12.4, 1.4.3 | COVERED |
| 1.6 | S01:104 | Mafia and weather (rain effect on people) | 2.1.4, 4.8 | COVERED |
| 1.7 | S01:105 | Only about 12 of KCD2's 308 crime behaviour trees read, as outlines | 2.6.2, 2.5.1 | COVERED |
| 1.8 | S01:106 | Wiki defaults may differ from shipped data | 9.11 | GAP G9 |
| 1.9 | S01:34, 37, 50 | Villager wake-up hour, extras' door hours, people's update-budget unit unverified | 2.1.2, 2.1.3, 8.1.1 | COVERED (8.1.1 GAP G2) |
| 1.10 | S02:121 | No real player's clock; every minute is an estimate, skipping compresses cutscenes | 7.1, 9.5 | COVERED |
| 1.11 | S02:122 | Mafia tutorial and failure triggers inferred, script logic not exported | 6.5, 7.9 | COVERED |
| 1.12 | S02:123 | KCD2 engine-fired tutorials, reload point, siege scenes, video order | 6.5, 7.8, 5.8.2 | COVERED |
| 1.13 | S02:124-126 | Not reached (disk): Mafia face-clip cross-check at 134 of 491; chapter 3 onward not exported | 5.2.4, 7.1 | COVERED |
| 1.14 | S02:127-130 | Not reached: Warhorse wiki page empty; HowLongToBeat; IGN, Polygon, Eurogamer, PC Gamer, GamesRadar, 2K support, Deltias, Sportskeeda blocked | 7.1, 7.5, 9.11 | GAP G9 (sources) |
| 1.15 | S03:97 | Mafia bark table, cooldowns, chances, ranges, whether crowd voices differ (not exported) | 3.6.3, 3.6.4, 5.6.1 | COVERED |
| 1.16 | S03:98 | Code: how either picks within a pool | 3.6.3, 3.6.4 | COVERED |
| 1.17 | S03:98 | KCD2's 51,000 camera commands with no named shot | 5.8.1, 5.8.2 | COVERED |
| 1.18 | S03:99 | Units of KCD2 per-line cooldowns (play time or world clock), line-length field and start delay meaning, line cap holds in 938 of 2,142 pools | 3.6.3, 9.6 | COVERED |
| 1.19 | S03:100 | Density, subtitle look, how barks land: only in play, no recordings | 3.6.3, 6.1.2 | COVERED |
| 1.20 | S04:74 | San Celeste actors, props, widths (map not exported) | 4.1.5, 4.4 | GAP G4 (street rules) |
| 1.21 | S04:75 | KCD2 loose meshes and so props per 10 m | 4.4, 4.1.5 | GAP G4 |
| 1.22 | S04:76 | Block lengths; sightlines; fog as an edge; KCD2 cell sizes | 4.1.2, 4.1.4, 4.1.5, 8.1.2 | GAP G4, G3 |
| 1.23 | S04:76 | Clutter by kind (bins, bikes, litter), parked carts | 4.4, 4.5 | COVERED |
| 1.24 | S04:77 | Mafia building heights come from kit heights, not building bounds | 5.3.1 | COVERED |
| 1.25 | S05:80 | KCD2 time of day, exposure, sun values (33 profile names only) | 5.4.1, 4.7 | COVERED |
| 1.26 | S05:81 | KCD2 material parameters and window depths | 5.3.2, 5.3.4 | COVERED (5.3.4 GAP G5) |
| 1.27 | S05:82 | Mafia master material graphs, lamp Blueprints (candela scaling), window-glass materials, front layer on windows | 5.3.2, 5.4.2, 5.3.4 | COVERED, GAP G5 for glass |
| 1.28 | S05:83 | Lights and decals per street; windows from a low angle; net curtains; cost figure for reflections | 5.4.2, 5.3.4, 5.3.3, 8.1.1 | GAP G5, G2 |
| 1.29 | S05:84 | What 6,374 of KCD2's 7,572 materials are | 5.3.2 | COVERED |
| 1.30 | S06:151 | Mafia body, head, hair triangle counts (not exported) | 5.1.2, 5.1.3, 5.1.1 | COVERED |
| 1.31 | S06:152 | How many looks one Mafia crowd spawner produces | 5.1.5 | COVERED |
| 1.32 | S06:153 | KCD2 level-of-detail switch distances | 5.1.4, 8.1.1 | COVERED (G2) |
| 1.33 | S06:154 | How either game's hiding maps to vertices | 5.1.4 | COVERED |
| 1.34 | S06:155, 123 | Lapel and collar modelling; which folds sit in mesh or texture | 5.1.4, 9.1 | COVERED |
| 1.35 | S06:156 | Mafia's shared MetaHuman face folder (not exported) | 5.1.1, 5.1.5 | COVERED |
| 1.36 | S06:157 | Marvelous Designer binding terms and monthly price | 9.1, 10.4 | GAP G6 (licence record) |
| 1.37 | S06:12, 13, 90, 92, 106, 107 | KCD2 hair cards, textures, caps, Hangar 13 and Warhorse talks known from excerpts only (unverified) | 5.1.3, 5.1.4, 5.1.1 | COVERED |
| 1.38 | S07:122 | How Mafia's walk times its stops (distance curves, transitions not decoded) | 5.2.1, 1.1.1 | COVERED |
| 1.39 | S07:123 | 144 of Mafia's animation classes, incl. female walk and strafe layers | 5.2.1 | COVERED |
| 1.40 | S07:124 | KCD2 foot-IK tuning (in code) | 5.2.1 | COVERED |
| 1.41 | S07:125 | Ambient animations per street, both games | 5.2.5 | COVERED |
| 1.42 | S07:126 | Locomotion and feet feel seen only in play, no talks reachable | 5.2.1, 9.9 | COVERED |
| 1.43 | S07:80 | Slide-notice figure of 21 mm is from a snippet, unverified (3 cm bar lenient) | 5.2.1, 9.9 | COVERED |
| 1.44 | S07:133 | Not reached: Hangar 13 Unreal Fest talk (video), Epic interview (403), GDC Vault down | 5.2.1, 9.11 | GAP G9 (sources) |
| 1.45 | S08:90 | Bus volumes, falloff, reverb, mastering, random rules, music transitions (binaries not parsed); relative loudness of ambience, voices, effects, music unmeasured | 5.5.7, 5.5.3, 5.7 | COVERED |
| 1.46 | S08:91 | KCD2 beds by daytime and rain inside each event; footstep set; puddle parameter use | 5.5.3, 5.5.4, 5.5.1 | COVERED |
| 1.47 | S08:92 | Mafia emitters beyond the opera level; systemic rain (none found) | 5.5.3, 5.5.4 | COVERED |
| 1.48 | S09:76 | Mafia default camera mode, hold length, probe and hide defaults; input buffering in both | 1.1.2, 5.8.1, 6.6 | COVERED |
| 1.49 | S09:77 | Epic sample camera rigs in our packaged game (editor files, no editor today); KCD2 default lens; Mafia input config | 5.8.1, 1.2.2 | COVERED |
| 1.50 | S09:78 | Feel in play; aim and camera sharing one sensitivity felt sluggish | 1.1.2, 6.6 | COVERED |
| 1.51 | S10:97 | Font sizes as played; KCD2 Scaleform sizes not unpacked | 6.1.2, 8.4 | COVERED |
| 1.52 | S10:98 | What KCD2's adaptive option hides and hardcore's full list (sources disagree) | 7.10, 8.4, 1.4.6 | COVERED |
| 1.53 | S10:99 | Mafia prompt position in play (left in layout, lower right in a review) | 6.1.1 | COVERED |
| 1.54 | S10:100 | Either game at 21:9 in play | 6.1, 8.1, 8.3 | COVERED |
| 1.55 | S11:75 | KCD2 barter formula, cash refills, save rules in play, decay time unit, weather choice, rain length; which multiplier is the player's; lesson, horse, barber, bath prices | 2.7.5, 7.8, 2.4.2, 4.8 | COVERED |
| 1.56 | S11:76 | Mafia loot sums, checkpoint counts, presets (not exported, disk) | 1.6.2, 7.8 | COVERED |
| 1.57 | S11:77 | What follows a game over; Mafia shop in use (only in play) | 7.9, 2.7.5 | COVERED |
| 1.58 | S11:17 | Whether a bought save is the only field save, unverified | 7.8 | COVERED |
| 1.59 | S12:92 | Cell sizes and loading distances in metres (Mafia's encrypted maps) | 8.1.2, 4.1.2 | GAP G3 |
| 1.60 | S12:93 | Measured frame times in a street for either game (one public test) | 8.1, 8.1.1 | GAP G2 |
| 1.61 | S12:94 | Mafia animation budget file not in files read | 8.1, 5.2.1 | COVERED |
| 1.62 | S12:95 | Shader counts for either game | 8.1, 5.3.2 | GAP G2 |
| 1.63 | S12:33 | Glass reflections lost at the 60 fps profile (reflection level 1) | 5.3.4, 5.3.3 | GAP G5 |
| 1.64 | S13:84 | Mafia source-side checks, folder rules; asset-registry tags hint (N) | 9.2, 9.7 | COVERED |
| 1.65 | S13:85 | How either studio tunes in the editor | 9.6, 9.9 | COVERED |
| 1.66 | S13:86 | KCD2: 8 tables that do not parse missing from the row count | 9.11 | GAP G9 |
| 1.67 | S14:108 | Mafia hit-stop lengths, damage, contact moments, knife timings, parry and dodge windows, attack-point regeneration, brawl coordination, shake and physics values (disk) | 1.3.1, 1.3.2, 1.3.6, 1.3.8, 5.8.1 | COVERED |
| 1.68 | S14:109 | KCD2 damage formula, perfect-block window, how a fight becomes a crime (code) | 1.3.7, 1.3.2, 2.6.2, 2.5.3 | COVERED |
| 1.69 | S14:110 | KCD2 timing fields, the 2 s gap, fine and jail units; 687 wiki-only constants; retail against 1.2 | 1.3.8, 2.6.4 | COVERED |
| 1.70 | S14:111 | Hit-pause feel, Mafia brawl spacing, police arrival (only in play) | 1.3.1, 1.3.8, 2.6.1 | COVERED |
| 1.71 | S14:15, 20, 25, 26 | Table cells "not reached (disk)": knife timing, hit-stop values, blows to put a man down, brawl attackers | 1.3.1, 1.3.6, 1.3.7, 1.3.8 | COVERED |
| 1.72 | S15:89 | Engines' code: lockpick formula; merchant suspicion; whether fence and 0.4 scripts run; how a witness chooses arrest, settle or report; class multipliers | 1.6.1, 2.7.5, 2.7.6, 2.5.1 | COVERED |
| 1.73 | S15:90 | Who fences (names only); buff and jail duration units; Trosky not counted; Mafia lockpick and loot tables (disk) | 2.7.6, 2.6.4, 1.6.1 | COVERED |
| 1.74 | S15:91 | How a search looks (only in play) | 1.6.2, 2.6.2 | COVERED |
| 1.75 | S16:101 | KCD2 hardcore and quest markers; when directions talk is on; the large job's 17 scene lengths; hibernation in code; job lengths in play | 3.5, 3.4.3, 6.2.3, 1.G1 (see G1), 2.1.3 | COVERED parents; job engine GAP G1 |
| 1.76 | S16:102 | Mafia objective instances in unexported level data (kinds, optional flags, timer seconds, stealth rules); skip default; 30 video-flagged triggers | 3.5, 5.8.2 | GAP G1 (job template) |
| 1.77 | S16:103 | Not reached: TechRaptor, Deltia's, Escorenews, X, Fandom, Nexus, GameSpot, PCGamingWiki; HowLongToBeat, Valnet, Polygon, RPS, Eurogamer; 2025 Prague cinematics talk; KM-A-29 and 83 empty | 5.8.2, 7.5, 9.11 | GAP G9 (sources) |
| 1.78 | S16:104 | PLAN.md has phases 0 to 5, no phase 9; the acts come from the 28 Sep outline | 3.1, 7.4 | COVERED (plan itself: G7) |
| 1.79 | S17:54 | HowLongToBeat and GameRant small-maps list not reached; side-story total (about 100) unconfirmed from a primary source | 3.3, 7.5 | COVERED |
| 1.80 | S17:55 | No number re-measured or reviewed against sources (importer note); no fresh review yet | 9.11, 3.5 | GAP G9 |
| 1.81 | S18:12 | No source says a person recalls an earlier meeting days later; Vice's line multiplier names no baseline | 2.3.1, 3.6.4 | COVERED |
| 1.82 | S18:19 | No source describes gossip in GTA VI (treat as absent until shown) | 2.4.1 | COVERED |
| 1.83 | S18:38 | A post-release patch, mod tool or deeper system could change the edge check; re-check at first month and after first big patch | 2.2, 2.4, 9.11 | GAP G9 (re-check) |
| 1.84 | S18:59, 83 | Store hours and frame-rate critic counts differ or are inconsistent (U) | 2.7.5, 8.1 | COVERED |
| 1.85 | S18:137 | Not reached: Rockstar pages and interviews, dotesports, LootLevelChill, Destructoid, Console Creatures, NPR, Gfinity, Digital Foundry page and video; no wiki counts for systems | 9.11 | GAP G9 |
| 1.86 | S18:137 | Not checked: Rockstar's generative-AI statement; whether any patch changed systems since release | 10.2, 9.11 | COVERED (10.2), G9 |
| 1.87 | S18:144 | Reactions to outfits, staring, crowding, eavesdropping, fighting passenger, police persistence after stars: pre-release only | 1.4.4, 2.6.5, 4.3.1 | COVERED |

## 2. TRACE.md (production/lane/synthesis/TRACE.md): conflicts, left-out, set-aside lines

Conflicts C1 to C18 (section 1, lines 16-33):

| # | Source:line | Item | Parts | Status |
|---|---|---|---|---|
| 2.1 | TRACE:16 C1 | Endings: 28 Oct ruling says two or three; approved outline and built story have five | 3.1.4, 3.1.5 | COVERED (his ruling open) |
| 2.2 | TRACE:17 C2 | Prototype rule: Tom never hits a woman, anyone sixty or over, or the priest | 1.3.4, 1.3.3 | COVERED (his ruling open) |
| 2.3 | TRACE:18 C3 | Each person's own nerve and loyalty open since 29 Sep; Core has everyone ordinary | 2.14, 2.11.2 | COVERED |
| 2.4 | TRACE:19 C4 | New systems need a place in PLAN.md before Unreal (beat constable, fares with wrinkles, wash, board, cars and people) | 2.6.1, 3.4.2, 2.7.3, 1.7.3, 1.2.5, 9.4 | COVERED parts; plan placement G7 |
| 2.5 | TRACE:20 C5 | Police after a witnessed killing: manhunt at once or a day of investigating | 2.6.5, 2.16 | COVERED (his call open) |
| 2.6 | TRACE:21 C6 | "Others drive traffic and the firm's cars" against "the player's car"; side stories' "Tom never drives" to correct | 1.2, 4.5, 3.3 | COVERED |
| 2.7 | TRACE:22 C7 | "The docks" is not one of canon's seven districts | 4.2, 4.1.4 | COVERED |
| 2.8 | TRACE:23 C8 | Armed cars in the weapons spec against no armed car in 1990 research | 2.6.6, 1.3.10, 4.6 | COVERED |
| 2.9 | TRACE:24 C9 | Hospital bill in combat design; care was free in 1990 | 4.3.8, 1.3.9, 1.3.7 | COVERED |
| 2.10 | TRACE:25 C10 | Staged accidents spec (no crime; one a moving car) not in DESIGN | 1.3.6, 1.2.5, 2.16 | COVERED (decided out) |
| 2.11 | TRACE:26 C11 | Clock speed (45 or 30 s) and how far a story travels | 7.13, 2.4.1 | COVERED (open) |
| 2.12 | TRACE:27 C12 | Sheila's trust (time and a clean week) built as option A | 2.12.1, 3.2.1 | COVERED |
| 2.13 | TRACE:28 C13 | Study 14 source test at 6 clips against his design's 4 | 9.9, 9.5 | COVERED (his yes) |
| 2.14 | TRACE:29 C14 | Shopkeeper naming the only person in the shop; guess is suspicion | 2.3.2, 3.6.2 | COVERED |
| 2.15 | TRACE:30 C15 | First hour: approved 29 Sep staging against restaged ferry, fare at 2:30, debt book | 7.1, 3.4, 2.8.1 | COVERED (open) |
| 2.16 | TRACE:31 C16 | Study 17's docks job made the firm's cold-store contract | 3.5.1, 4.2.2 | COVERED |
| 2.17 | TRACE:32 C17 | Cab as the day's main verb (22% of play) against canon "not a driving game" | 1.2, 3.4, 7.5, 0.1 | COVERED; canon basis G12 |
| 2.18 | TRACE:33 C18 | Canon describes two games (pillar against "What LEDGER is not") | 7.5, 0.1 | GAP G12 |

Left-out and set-aside study lines (section 2, lines 47-158):

| # | Source:line | Item | Parts | Status |
|---|---|---|---|---|
| 2.19 | TRACE:47 s01-07 | Detail by distance; unseen people freeze beyond 70 m (performance, left out) | 2.1.3, 8.1.1 | GAP G2 |
| 2.20 | TRACE:62-63 s03-05, s03-06 | Waits by kind on ambient lines and KCD2's waits as starting values (tuning table of the talk helper) | 3.6.3, 9.6, 9.8 | COVERED |
| 2.21 | TRACE:64 s03-07 | Camera alternation in talk left to craft | 5.8.1, 6.7 | COVERED |
| 2.22 | TRACE:67 s04-01 | Street width 9 to 15 m (street-building check, n16-4) | 4.1.1, 4.1.5 | GAP G4 |
| 2.23 | TRACE:68 s04-02 | Props per 10 m | 4.4, 4.1.5 | GAP G4 |
| 2.24 | TRACE:69 s04-03 | Dress where the player walks (craft; walked lines in DESIGN 15) | 4.4, 4.1.5 | GAP G4 |
| 2.25 | TRACE:70 s04-04 | Kit reuse check | 5.3.1, 4.1.5 | GAP G4 |
| 2.26 | TRACE:72 s04-06 | Street views end on a building or a turn | 4.1.1, 4.1.5 | GAP G4 |
| 2.27 | TRACE:73 s04-07 | Small life tied to weather and hour is craft | 4.8, 5.2.5, 5.9 | COVERED |
| 2.28 | TRACE:74 s04-08 | One switchable layer per street state (waits for more than one street) | 4.1.5, 4.7 | GAP G4 |
| 2.29 | TRACE:75 s05-01 | Window frames; fake rooms upper and distant | 5.3.4, 5.3.1 | GAP G5 |
| 2.30 | TRACE:76 s05-02 | Shop glass captures and dirt mask | 5.3.4 | GAP G5 |
| 2.31 | TRACE:77 s05-03 | Lamp build (key spot plus bulb, ratio) is craft | 5.4.2 | COVERED |
| 2.32 | TRACE:79-81 s05-05..07 | Wear decal mix; master materials; texture budget (done) | 5.3.2, 8.1.1 | COVERED |
| 2.33 | TRACE:82-85 s06-01..04 | Tom's outfit budget; four garment levels of detail; colour by material; one base body per sex for the crowd | 5.1.4, 5.1.2, 5.1.5, 9.1 | COVERED |
| 2.34 | TRACE:86 s06-05 | Crowd dressing recipe | 5.1.5 | COVERED |
| 2.35 | TRACE:87 s06-06 | His decision on the Marvelous month (done, his) | 9.1, 10.4 | GAP G6 (licence record) |
| 2.36 | TRACE:89-91 s07-01..03 | Stops and turns KCD2's way; clip rate; 3 cm foot-slide bar | 5.2.1 | COVERED |
| 2.37 | TRACE:92 s07-04 | Sitting as In, Loop, Out, set aside 6 Nov | 5.2.3, 1.1.3 | COVERED |
| 2.38 | TRACE:93-94 s07-05, s07-06 | Ambient clips beyond turn-and-look and startle; talk body language beyond staging (craft) | 5.2.5, 5.2.6 | COVERED |
| 2.39 | TRACE:95 s07-07 | Prepared lines on Epic's mouths, live on loudness (ruling 1 Oct stands) | 5.2.4, 5.6.3 | COVERED |
| 2.40 | TRACE:96 s07-08 | No animation sharing for now | 5.2 | COVERED |
| 2.41 | TRACE:100 s08-04 | Wet footstep layer and two shoe sets left to craft | 5.5.1, 5.5.4 | COVERED |
| 2.42 | TRACE:105-106 s08-09, s08-10 | No Wwise, FMOD, vehicles, extra animals; ambience plan's levels and distances (mix numbers for his ear) | 5.5.3, 5.5.5, 5.5.7 | COVERED |
| 2.43 | TRACE:114, 119 s10-01, s10-06 | Interface width and scale choice (look decision for his page); map not on screen | 6.1.2, 6.3 | COVERED |
| 2.44 | TRACE:121 s11-01 | A delay before police act; needs place in PLAN.md (C4) | 2.6.1, 2.5.1 | COVERED |
| 2.45 | TRACE:129-130 s11-09, s11-10 | Weather per checkpoint (advised against); clock, light, exposure, sky in one preset | 4.8, 4.7, 5.4.1 | COVERED |
| 2.46 | TRACE:131 s11-11 | Measure the clock by playing (BUILD-ORDER round 11) | 7.13, 9.9 | COVERED |
| 2.47 | TRACE:132-136 s12-01..05 | Significance and update budgets; load test; people in full detail, draw distance, shadow lights; texture pool figure; dynamic resolution range | 8.1, 8.1.1 | GAP G2 |
| 2.48 | TRACE:137 s12-06 | Stand-in shop-glass reflection at low quality | 5.3.4, 8.1.1 | GAP G5 |
| 2.49 | TRACE:140-143 s13-03..06 | Naming rule for Unreal assets; settings as data; snake_case; no binary twins or GUID names | 9.2, 8.3, 9.7 | COVERED |
| 2.50 | TRACE:158 s14-15 | Source test at 6 clips (a production test; C13) | 9.9, 9.5 | COVERED |
| 2.51 | TRACE:153-154 s14-10, s14-11 | KCD2 street numbers and weapon grading as leads for the Core, not design | 1.3.8, 1.3.6, 9.6 | COVERED |
| 2.52 | TRACE:187 | 41 lines left out: 33 craft for Unreal phases (his 8 Nov tap keeps them), 8 advised against or done | 5, 8, 9 | COVERED |

Rulings, canon, contradiction and tension lines (sections 3 to 5):

| # | Source:line | Item | Parts | Status |
|---|---|---|---|---|
| 2.53 | TRACE:198 | Story: one story with two or three endings (conflict C1) | 3.1.4 | COVERED |
| 2.54 | TRACE:202 | 29 Sep: no new system before its place in PLAN.md (conflict C4) | 9.4, 9.10 | GAP G7 |
| 2.55 | TRACE:216 | 3 Oct street's trades left out in detail (places that fares and jobs use) | 4.3.3, 3.4.1 | COVERED |
| 2.56 | TRACE:223 | D48 model chosen by moment left out (talk helper's design) | 9.8 | COVERED |
| 2.57 | TRACE:227 | 29 Sep: live talk names nothing real, nothing after 1992 (talk helper's rule) | 8.8, 3.6.1 | COVERED |
| 2.58 | TRACE:259 | Tone (grounded noir, dry wit) left to the writing | 3.6, 3.1 | COVERED |
| 2.59 | TRACE:260ff | Content rule: period swearing, no slurs; religion never a mechanic: left to writing rules | 8.8, 3.6.6 | COVERED |
| 2.60 | TRACE:276 | "What LEDGER is not" spend line conflicts with 18 Nov pillar (C18); cab as main verb (C17) | 0.1, 1.2, 7.5 | GAP G12 |
| 2.61 | TRACE:293 | Content-rule breaches in weapons spec, roster, how-to-play void; Wayne's hook to be rewritten | 1.3.6, 2.8.1, 8.8 | COVERED |
| 2.62 | TRACE:300 | Contradiction 14: witnessed killing, manhunt or investigation (C5) | 2.6.5 | COVERED |
| 2.63 | TRACE:307 | Contradiction 21: competence per domain cut (ruling 30 Oct) | 2.12.3 | COVERED |
| 2.64 | TRACE:332-342 | Tensions 7, 8, 10, 11, 16, 17 "Not design": dates, friends' build cadence, voice engine, local voice or server, weekly allowances, spend caps | 10.3, 5.6.2, 8.6, 8.7, 9.10 | GAP G7 (dates, allowances, caps) |
| 2.65 | TRACE:337 | Tension 12: July office design void under D19 and content rule | 4.3.1 | COVERED |
| 2.66 | TRACE:344 tension 19 | Second CCTV site: his to name, not needed in release map | 4.9 | COVERED |
| 2.67 | TRACE:10, 13 | "Not placed in design": craft lines are kept for Unreal phases, not dropped | 5, 9.2 | COVERED |

## 3. Risk registers

Levels: old register is L x C each 1 to 5 and score (3 Oct baseline; 5 Oct review changes noted); draft register is L, I as low, med, high.

### 3a. 6-RISKS.md (production/research/pre-production/6-RISKS.md)

| # | Source:line | Risk | Level stated | Parts | Status |
|---|---|---|---|---|---|
| 3.1 | 6-RISKS:23 R1 | Talk empty, wrong or unchecked; claim check bypass; only three people to talk to | 5x5=25 (level at 5 Oct) | 3.6.2, 3.6.1, 8.6, 3.6.3 | COVERED |
| 3.2 | 6-RISKS:24 R2 | Replies too slow (first sound 5.41 s median) | 5x4=20 (level 5 Oct) | 5.6.3, 5.6.2, 8.7, 3.6.1 | COVERED |
| 3.3 | 6-RISKS:25 R3 | Street does not reach the bar; whole street frames fail | 4x5=20, up to 25 on 5 Oct | 4.1.1, 5.3.1, 5.3.2, 5.4.2, 5.4.3 | COVERED |
| 3.4 | 6-RISKS:26 R4 | People break the illusion (Mixamo Tom, stiff idle, mouths, underlit faces) | 4x4=16 | 5.1.1, 5.1.4, 5.2.1, 5.2.4, 5.2.5 | COVERED |
| 3.5 | 6-RISKS:27 R5 | Frame rate and memory give way (16.7 ms slowest 1%; voice crash at 1.4 GB; Nanite off) | 4x4=16 | 8.1, 8.1.1, 8.7 | COVERED, GAP G2 |
| 3.6 | 6-RISKS:28 R6 | Not thirty minutes worth playing (Ada and June cannot be met, office not enterable, police are captions) | 4x4=16 | 7.1, 4.3.1, 3.2.1, 2.6.1 | COVERED |
| 3.7 | 6-RISKS:29 R7 | Build fails on the night (key read from user folder; Development packages) | 3x5=15, 10 on 5 Oct | 8.5, 10.1, 10.3, 8.6 | COVERED |
| 3.8 | 6-RISKS:30 R8 | Licence, terms or disclosure problem (EULA, MetaHuman, Mixamo, Steam survey unread; disclosure untrue today) | 3x4=12 | 10.2, 10.4, 5.1.1, 9.7.1 | GAP G6 |
| 3.9 | 6-RISKS:31 R9 | Way of working stalls the list (order replaced six times; two-tries breaches; no target date) | 4x3=12 | 9.7, 9.5 | GAP G7 |
| 3.10 | 6-RISKS:32 R10 | Friends' talk not covered (rulings conflict; money may run out; key cap unknown) | 4x4=16, 9 on 5 Oct | 8.6, 10.3 | COVERED |
| 3.11 | 6-RISKS:38 W1 | One PC is everything | 2x5=10 | 9.7, 10.3 | COVERED |
| 3.12 | 6-RISKS:39 W2 | F: is small | 3x3=9 | 9.7 | COVERED |
| 3.13 | 6-RISKS:40 W3 | The language model changes under us (Haiku 4.5 retirement) | 2x4=8 | 8.6, 9.8 | COVERED |
| 3.14 | 6-RISKS:41 W4 | Faces and bodies depend on Epic's cloud rigging service | 2x3=6 | 5.1.1, 5.1.2, 9.2 | COVERED |
| 3.15 | 6-RISKS:42 W5 | VCTK speaker consent unpublished | 2x3=6 | 5.6.1, 5.6.2, 9.7.1 | COVERED, G6 |
| 3.16 | 6-RISKS:43 W6 | His eye is the only final judge | 3x3=9 | 9.5 | COVERED |
| 3.17 | 6-RISKS:44 W7 | Content-rule breach reaches a friend's screen (back-bar decal, brand bible says pub) | 2x4=8 | 8.8, 4.9, 4.10, 4.3.3 | COVERED |
| 3.18 | 6-RISKS:72-75 | Could not verify: every likelihood; effort and dates (P21 not run); key's monthly cap and "Help improve Claude"; F: free space (two records disagree) | 8.6, 9.7, 9.10 | COVERED, G7 |

### 3b. RISK-REGISTER-WHOLE-GAME-DRAFT-2026-11-18.md (production/lane/)

| # | Source:line | Risk | Level stated | Parts | Status |
|---|---|---|---|---|---|
| 3.19 | Draft:9 risk 1 | Combat does not reach AAA; nothing thrown in Unreal; his option pick open (COMBAT-END-STATE-OPTIONS) | L high, I high; by 1 Feb 2027 | 1.3.1, 1.3.2, 1.3.9, 5.2.2, 5.5.6, 9.9 | COVERED |
| 3.20 | Draft:16 risk 2 | Scope outruns the date; cost of one complete person unmeasured (44 named people; phases 52 to 71 weeks against 54) | L high, I high; by 1 Feb 2027 | 3.2, 3.2.6, 9.10, 9.9 | GAP G11, G7 |
| 3.21 | Draft:23 risk 3 | Live talk costs too much per played hour at release ($0.12 an hour, counter says $0.327; replies per hour unmeasured) | L med, I high; by 7 Dec 2026 | 8.6, 9.8, 3.6.1 | COVERED |
| 3.22 | Draft:30 risk 4 | Accents fail a native ear (VCTK; consent a stated risk; no paid panel) | L med, I high; by 15 Jan 2027 | 5.6.1, 5.6.2, 9.5, 9.7.1 | COVERED |
| 3.23 | Draft:37 risk 5 | The recipe does not transfer (RECIPE.md never re-run without history) | L med, I high; by 21 Dec 2026 | 9.7.2, 9.2 | GAP G10 |
| 3.24 | Draft:44 risk 6 | Clothing stalls on the cloth engine (wrist tangle set aside; Tom's jacket, Sheila's collar set aside; M5 31 to 62 h) | L high, I med; by 14 Dec 2026 | 9.1, 9.1.1, 5.1.4 | GAP G8 |
| 3.25 | Draft:51 risk 7 | Card memory runs out (6,005 MB; binding line about 4.7 GB; crowd unpriced) | L high, I high; by 14 Dec 2026 | 8.1, 8.1.1, 5.1.5, 3.2.4, 8.7 | GAP G2 |
| 3.26 | Draft:58 risk 8 | Hair never passes (Houdini free licence cannot export hair; Indie about $299 a year, unverified) | L high, I med; by 1 Feb 2027 | 5.1.3, 9.2, 9.7.1 | COVERED, G6 |
| 3.27 | Draft:65 risk 9 | Estimates run two to five times over; 95% of logged hours uncoded | L high, I med; by 4 Jan 2027 | 9.10, 9.5 | GAP G7 |
| 3.28 | Draft:72 risk 10 | Process overhead eats production (records 13% and 11% of spend against 15% line) | L med, I med; by 7 Dec 2026 | 9.7, 9.10 | GAP G7 |
| 3.29 | Draft:87 | Old R6 (thirty minutes) retired to phase 3's exit; old R7 (the night's build) to phase 4's exit; R8 licences to allowlist checks, kept on watch list | L/I not restated | 7.1, 10.3, 9.7.1 | COVERED, G6 |
| 3.30 | Draft:93-94 | Watch list W1 to W7 kept; W5 merged into risk 4 | see 3a | as 3a | COVERED |
| 3.31 | Draft:98 | Not verified: every L and I; 44 is 14 plus "about 30"; talk cost assumes 15 replies an hour | 3.2, 8.6 | COVERED |

## 4. KILN-TO-GAME-PLAN-2026-11-17.md (production/research/phase2-plan/)

The skeleton's 9.1 "Kiln" has no children, so each stage below is covered only at the parent level; the stage list is proposed as G8 children of 9.1.

| # | Source:line | Stage or module the game needs | Parts | Status |
|---|---|---|---|---|
| 4.1 | Plan:9 | First garment: Ron's work trousers, skinned only; Sheila's skirt needs Chaos cloth hand-off, never run packaged | 5.1.4, 9.1 | GAP G8 (9.1.8 cloth hand-off in game) |
| 4.2 | Plan:23 chain step 1 | Drape (Marvelous job to OBJ, plan json) and Kiln's own drape | 9.1 | GAP G8 (9.1.1 Drape) |
| 4.3 | Plan:25 chain step 2; 91 Route B | Bend-back of a garment draped on a posed or standard body (unpose_garment.py, turns record per standard body) | 9.1, 5.1.2 | GAP G8 (9.1.7) |
| 4.4 | Plan:54-67 | Kiln-to-game adapter (tools/kiln_to_game.py): piece fit, UV rewrite, body group rename, refuse missing piece | 9.1, 9.2 | GAP G8 (9.1.2) |
| 4.5 | Plan:26-29 steps 3-7 | Weld and pattern layer; game mesh retopology (8,000 to 10,000 triangles); texture layout; bake (normal, occlusion, packed); game blend | 5.1.4, 9.2, 9.1 | GAP G8 (9.1.3 garment mesh chain) |
| 4.6 | Plan:32-33 steps 8-9; 77, 82-83 | Skinning from the wearer's body weights (8 influences, no-skirt, leg sides); weights-body match check; pose tests (walk, sit, stair); boots proxy shortfall | 5.1.4, 5.1.2, 5.2.1 | GAP G8 (9.1.4) |
| 4.7 | Plan:34, 84 step 10 / I | Into the game: row in production/specs/garments.json, import_garments.py, SKM in /Game/Ledger/MetaHumans/Garments, garments_shipped_check | 5.1.4, 9.2 | GAP G8 (9.1.5) |
| 4.8 | Plan:35, 85 step 11 / J | Packaged -WearHeld film, RUBRIC lines 9 to 11, fresh reviewer, parity list M7 reads 1 | 5.1.4, 9.5, 10.1 | GAP G8 (9.1.6) |
| 4.9 | Plan:37 | Import's "ok" is advisory; Tom's jeans went on with ok false (boundary 3.5 mm, fit 20 mm) | 5.1.4, 9.5 | COVERED |
| 4.10 | Plan:39-52 | Kiln against Marvelous mismatches: units, UVs, weld, body group name, no materials, pose, no weights, final OBJ gone | 9.1, 9.2 | GAP G8 |
| 4.11 | Plan:75 step A | Re-export the passing drape; U: whether a raw-FBX project passes the start check (else route B) | 9.1 | GAP G8 |
| 4.12 | Plan:76-84 | Steps B0 to H carry U or E tags (expected checks, 6.4 h estimate, 6 to 13 h with overrun) | 9.1, 9.10 | GAP G8, G7 |
| 4.13 | Plan:96 | Ron's whole look waits; his passed jeans replaced only on his whole-person page; proof row stays held | 5.1.4, 3.2.2, 3.2.6 | GAP G11 |
| 4.14 | Plan:97 | Keep the final OBJ; the 16 Nov final OBJ vanished; loss to be recorded in DECISIONS.md | 9.1, 9.7 | COVERED (9.7), GAP G8 |
| 4.15 | Plan:98 | Front-end licence: whether the Kiln front end's adoption tap was answered, before step I | 9.1, 10.4 | GAP G6 |
| 4.16 | Plan:17-19 | Skinning reference (Mafia triangles 8,000 to 10,000; KCD2 none found) | 5.1.4 | COVERED |
| 4.17 | Plan:28, 36 | Modules named later: M5 three garments, M7 the Hook's whole list (draft risk 6) | 5.1.4, 5.1.5, 9.1 | COVERED parent; G8 |

## 5. QUESTIONS.md and conflict lines (production/lane/synthesis/QUESTIONS.md)

| # | Source:line | Item | Parts | Status |
|---|---|---|---|---|
| 5.1 | QUESTIONS:5 Q1 | Endings: five built states against two or three ruled; recommended: three shown with variants | 3.1.4, 3.1.5 | COVERED |
| 5.2 | QUESTIONS:7 Q2 | Anyone Tom will not hit (woman, sixty or over, priest); priest touches "religion never a mechanic" | 1.3.4, 1.3.3, 3.2.1 | COVERED |
| 5.3 | QUESTIONS:9 Q3 | Each person's own temper, before the one-simulation switch | 2.14, 2.11.2, 9.3 | COVERED |
| 5.4 | QUESTIONS:11 Q4 | First hour restaged for the 18 Nov pillar (ferry, fare 2:30, debt book 4:30) | 7.1, 4.2.1, 3.4, 2.8.1 | COVERED |
| 5.5 | QUESTIONS:13 Q5 | Which game canon describes: rewrite "What LEDGER is not" to the pillar | 0.1, 7.5 | GAP G12 |
| 5.6 | QUESTIONS:15 Q6 | The cab as the day's main verb; driving under a quarter of play | 1.2, 3.4, 7.5, 0.1 | COVERED, G12 |
| 5.7 | QUESTIONS:17 | Open on his page: police after witnessed killing (C5) | 2.6.5 | COVERED |
| 5.8 | QUESTIONS:17 | Open on his page: clock and how far a story travels (C11) | 7.13, 2.4.1 | COVERED |
| 5.9 | QUESTIONS:17 | Open on his page: Sheila's trust (C12) | 2.12.1 | COVERED |
| 5.10 | QUESTIONS:17 | Open on his page: fight source test (C13) | 9.9 | COVERED |
| 5.11 | QUESTIONS:17 | His stored answer on the ending signs of 30 Sep was never stored; read from his page before Q1 | 3.1.5 | COVERED |
| 5.12 | QUESTIONS:3 | Order of asking: 4, 6, 5, 3, 2, 1 (not an item; process) | 9.10 | GAP G7 |

## Gaps (deduplicated)

- G1. 3.5.6 Job template and step states (parent 3.5): a job as a graph of saved states, windows and leashes, a Ledger line for every step state, steps that sleep, a tester's skip, hibernation. Raised by S16:101-102, TRACE s16-01 to s16-10 and DESIGN section 4.
- G2. 8.1.1 Frame, memory and crowd budget (parent 8.1): significance and update budgets, people in full detail, texture pool, dynamic resolution, shader counts, frame time measured in a street, crowd memory beyond named people. Raised by S01:50, S05:83, S06:153, S12:93 and 95, TRACE s01-07 and s12-01 to 05, 6-RISKS R5, draft risk 7.
- G3. 8.1.2 Streaming and loading of the Hook (parent 8.1): cells and loading distances. Raised by S04:76 and S12:92.
- G4. 4.1.5 Street build rules (parent 4.1): width, props per 10 m, kit reuse, dress where walked, view ends, block lengths, sightlines, fog edge, one switchable layer per street state. Raised by S04:74-76, TRACE s04-01 to s04-08.
- G5. 5.3.4 Shop glass and windows (parent 5.3): captures, dirt mask, fake rooms, window depth, net curtains, reflection cost at the 60 fps level. Raised by S05:81-83, S12:33, TRACE s05-01, s05-02, s12-06.
- G6. 9.7.1 Licence and terms record (parent 9.7): Marvelous binding terms and price, Unreal EULA, MetaHuman, Mixamo, Steam survey, VCTK consent, Houdini, Kiln front-end adoption tap, allowlist entries. Raised by S06:157, TRACE s06-06, 6-RISKS R8 and W5, draft risks 4, 8 and watch list, Kiln plan:98.
- G7. 9.10 Plan, forecast and spend (parent 9): dated plan, P80 forecasts, hour coding, record overhead, allowances and caps, PLAN.md placement of new systems, order of his questions. Raised by 6-RISKS R9, draft risks 2, 9 and 10, TRACE C4 and tensions 7, 16, 17, S16:104, Kiln plan:76-84, QUESTIONS:3.
- G8. 9.1.1 to 9.1.8 Kiln chain (parent 9.1): 9.1.1 Drape; 9.1.2 Kiln-to-game adapter; 9.1.3 Garment mesh chain (weld, retopology, layout, bake); 9.1.4 Skinning and pose tests; 9.1.5 Garment import to Unreal; 9.1.6 Packaged wear film and gate; 9.1.7 Bend-back for posed bodies; 9.1.8 Cloth hand-off in game (Chaos, for skirts and long parts). Raised by Kiln plan sections 1 to 5, draft risk 6.
- G9. 9.11 Reference studies and re-checks (parent 9): the 18 studies' unreached sources, unreviewed study 17, re-check of GTA VI at first month and after first patch, wiki defaults against shipped data. Raised by S01:106, S02:127-130, S07:133, S13:86, S16:103, S17:54-55, S18:38 and 137.
- G10. 9.7.2 Recipe and handover (parent 9.7): RECIPE.md and its skills usable without history. Raised by draft risk 5.
- G11. 3.2.6 Complete person (parent 3.2): the assembled unit (face, body, clothes, voice, card, lines) and its measured cost; nothing multiplied before one approved sample. Raised by draft risk 2, Kiln plan:96.
- G12. 0.1 Design pillars and canon basis (parent 0): verbs-first pillar against "What LEDGER is not", play-time budget, cab as main verb. Raised by TRACE C17, C18, QUESTIONS 5 and 6.

## Risks by part

- 0, 3.2, 3.2.6 (G11), 9.10 (G7): high/high (draft 2). Scope outruns the date; one complete person's cost not measured; phases forecast 52 to 71 weeks against about 54.
- 1.3, 1.3.1, 1.3.2, 5.2.2, 5.5.6, 9.9: high/high (draft 1). Combat has not been thrown in Unreal; bands rest on judgement.
- 3.6.2, 3.6.1, 3.6.3, 8.6: 25 of 25 (R1, level 5 Oct). Talk empty or unchecked; claim check bypassed under a budget; three people only.
- 8.6, 9.8, 3.6.1: med/high (draft 3); R10 16 (9 on 5 Oct). Cost per hour may be low by a quarter to a third; key cap and friends' cover rulings.
- 5.6.3, 5.6.2, 8.7, 3.6.1: 20 (R2). First sound 4.6 to 5.4 s against 2 s.
- 4.1.1, 5.3.1, 5.3.2, 5.4.2, 5.4.3: 25 (R3 at 5 Oct, 20 at baseline). Every whole street frame failed review.
- 5.1.1, 5.1.4, 5.2.1, 5.2.4, 5.2.5: 16 (R4). Stand-in Tom, shared stiff idle, mouths, underlit faces.
- 8.1, 8.1.1 (G2), 5.1.5, 3.2.4, 8.7: 16 (R5); high/high (draft 7). 16.7 ms slowest 1%, memory 6,005 MB against a 4.7 GB line, crowd unpriced.
- 7.1, 4.3.1, 2.6.1: 16 (R6). No thirty minutes ever played; office not enterable; police are captions.
- 8.5, 10.1, 10.3: 15 (R7; 10 on 5 Oct). Key read from user folder; Development packages.
- 9.7.1 (G6), 10.2, 10.4: 12 (R8). Licence terms unread; disclosure claims untrue today.
- 9.7, 9.5, 9.10 (G7): 12 (R9); high/med (draft 9); med/med (draft 10). Order churn, estimates two to five times over, overhead 11 to 13% of spend.
- 5.6.1, 5.6.2, 9.5: med/high (draft 4); W5 6. Accents judged by his ear only; VCTK consent unpublished.
- 9.7.2 (G10), 9.2: med/high (draft 5). Recipe never run without history.
- 9.1, 9.1.1 to 9.1.8 (G8), 5.1.4: high/med (draft 6). Wrist tangle and two garments set aside; M5 31 to 62 h.
- 5.1.3: high/med (draft 8). No hair has passed; Houdini export blocked on free licence.
- 9.7, 10.3: W1 10, W2 9. One PC is everything; F: is small.
- 8.6, 9.8: W3 8. Language model retirement.
- 5.1.1, 5.1.2, 9.2: W4 6. Epic cloud rigging timeouts.
- 9.5: W6 9. His eye is the only final judge.
- 8.8, 4.9, 4.10, 4.3.3: W7 8. Content-rule breach (back-bar decal, brand bible says pub).
