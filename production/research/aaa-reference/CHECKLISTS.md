# AAA study checklists, the other twelve

13 October 2026. Cloud week 42, queue unit 6.1b. KIT.md holds the checklists for studies 1, 3, 11 and 15 and the routes into both games. This file holds one page for each of the other twelve studies in his doc "LEDGER AAA Reference Study": 2, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14 and 16.

In plain words: each page says which game to open, where to look first, when to stop, what to count, and what the finished page must look like. Nothing here was taken from either game. The lab session reads this before a study, so that three to four hours go to the study and not to finding the door.

Marks: **[doc]** the study doc's own words (questions, "where it lives", outputs); **[K]** KIT.md's maps and reading list; **[I]** inference from general Unreal or CryEngine knowledge, to be confirmed at the PC. Nothing here is marked as read in a game, because no game file was opened.

## The rules every page shares

- **Study only.** Nothing from either game enters LEDGER or git: no file, texture, mesh, sound, animation, code or text, not even as a stand-in [doc]. Only our own written findings and numbers go into the repository.
- **Exports stay on the PC** under `F:\LedgerTools\aaa-study\` (mafia and kcd2 beneath it), outside git [doc, K]. A note written afterwards says what the idea is, in its own words.
- **The key is his step.** If FModel asks for one, the lab asks him. It never searches for one and never follows a link to a forum [K].
- **KCD2 goes through Warhorse's own modding tools** wherever they cover the need, and by hand-opened paks (zip files) where they do not [K].
- **Time box.** Each study is three to four hours [doc]. The first hour decides how readable the code is; if it is not readable, the study leans on files and play [doc]. Where a page says "stop after an hour", the note says "not there" and moves on.
- **A finding is not finished until it names** the plan item, phase or risk it serves and says adopt, adapt or ignore [doc].
- **Recorded play:** Jafar records with the Windows Game Bar or the AMD recorder [doc]. The lab session logs the video in frames and times. Fixed screenshots are taken with the HUD off. Recordings stay on F:, outside git.
- **No children, no drink, no gambling in anything kept.** Where a game's feature touches the content rule, the note names the feature in one line and records no detail.

## Study 2: The first 30 minutes

- **Game and source:** both games, mostly recorded play [doc]. KCD2 shows an open-world start, Mafia a story start.
- **Before it:** Jafar starts a new game and records the first 60 minutes without skipping anything, cutscenes included [doc]. No recording, no study.
- **Look first:** the recording, in 10-second steps [doc]. Beats are logged in a table: time, what the player does, what is on screen, who is talking, what is being taught, play or cutscene, tension rising, falling or quiet.
- **Then the files, only to date things:** KCD2's quest data for the first quest's opening states (Skald shows them) [K]; Mafia's mission assets, only by name, to learn how many beats the opening has [I].
- **Measure:** time to first control, first free movement, first conversation, first choice, first conflict, first reward; cutscene against play minute by minute; control prompts (type, count, when they stop); distinct activities in 30 minutes and the longest stretch with nothing new; when each interface piece first appears; checkpoints, saves, the first way to fail and what it costs [doc].
- **Stop rule:** the log stops at minute 60 of the recording. The 30-minute measures are taken from minutes 0 to 30.
- **Output:** a drawn timeline of the opening beats, a table of the measures, and a side by side with the phase 3 exit (two newcomer routes, at most five empty minutes, a consequence seen and kept) [doc]. It becomes the benchmark the friends' build is judged against.
- **Our own screenshots:** only our own game's. A frame from the other game's video is looked at, never saved into git.

## Study 4: Street and world building

- **Game and source:** Mafia first, KCD2 second; files and play [doc].
- **Look first, Mafia:** the level and world files. FModel's package list for the maps, and the asset names inside one representative street [I]. The aim is counts and distances, so an actor list per street is the first export (kept on F:).
- **Look first, KCD2:** `Data\Levels\<level>\level.pak` (the two levels are trosecko and kutnohorsko) for object counts and the town's layout [K]; the engine's own sandbox in the modding tools shows a level in place [K].
- **Measure:** street widths, block lengths, building heights, door and window spacing; unique buildings against kit pieces and variants; props per 10 metres by kind (bins, signs, crates, bikes, litter); which interiors can be entered, which are faked behind glass, which are closed; landmarks and sightlines; how the edges are hidden; streaming cell sizes and distant versions; parked vehicles, vegetation, weather dressing [doc].
- **Pick one representative street** in each game before counting, and say why. One street counted well beats a district counted loosely.
- **Stop rule:** if an actor list cannot be read inside the first hour, count by walking the street in recorded play with a free camera where the game allows one, and mark the numbers "play count".
- **Output:** target numbers for phase 2 (props per metre, unique pieces per street, variants per piece, interior strategy) that become automatic checks on Quay Street [doc].
- **Ties to our own work:** Quay Street is 48 m, with ten shop units as built [DECISIONS.md]. The numbers are compared per 10 metres so the street sizes do not matter.

## Study 5: Visuals

- **Game and source:** Mafia; files [doc].
- **Look first:** the post-process and lighting setups in the levels; material instances and their parameters; the config files [doc]. In FModel, search the names for glass, window, wet, puddle, decal, fog and exposure [I].
- **One problem at a time, as the doc lists them:** windows (ours read as white boards): frame depth, glass material, fake rooms behind the glass, curtains and nets; shop glass (ours costs frames): reflection method and cost; light (ours lacked pools at night): exposure, sky, fog, Lumen settings, lamp values and profiles, lights per street; wet streets: puddles, wet stone, rain in the materials; wear: decals, vertex paint, grime masks; materials: structure, variants, layering; texture sizes per kind of object [doc].
- **Measure:** the settings themselves (exposure, light values, reflection settings), decal counts per street, texture sizes, material counts [doc].
- **Stop rule:** one hour per problem. A problem that shows only in motion goes to a recording with the HUD off, at fixed positions beside our street.
- **Output:** a settings sheet set beside our look file, and one target per open visual problem [doc]. Shop windows tie to unit 7 and unit 8 of this week's queue: their targets say what a window must hold, and this study says how a shipped game holds it.
- **Rule to keep:** a setting written down is a number and a name. A texture, a material graph or a screenshot of the game is not copied.

## Study 6: Characters and wardrobe

- **Game and source:** Mafia for the garment as an asset, KCD2 for wardrobe as a system; files [doc].
- **Look first, Mafia:** character and outfit assets, skeletal meshes, cloth assets, material instances, crowd appearance tables [doc]. Search the names for outfit, clothing, hat, hair, crowd and cloth [I]. Open one period jacket and count: triangles, texture sizes, cloth parts.
- **Look first, KCD2:** the layered-clothes tables, with the Lua binding docs that ship in the modding tools (`Tools\modding\docs\`) naming the clothing and dirt calls [K]. The tables sit under `Libs\Tables\rpg\` [K].
- **Measure:** garment counts by slot, variants per garment, triangle and texture budgets, cloth-simulated parts, unique looks in a street crowd and how repeats are hidden, body type (custom or MetaHuman-based) [doc].
- **Stop rule:** one jacket, one trouser, one hat, then stop. Three garments measured fully teach more than thirty counted by name.
- **Output:** the clothing target in numbers and structure (what our jumper, trousers and jacket must be), a crowd-dressing recipe, and the facts for the clothes decision [doc]. Jafar's 13 October ruling already puts Epic's MetaHuman garments first and Marvelous Designer second, so the page says what this study adds to that order, not whether to reopen it.
- **Content rule:** no child garments are measured, because no child exists in the game.

## Study 7: Animation

- **Game and source:** Mafia; files and play [doc].
- **Look first:** the animation blueprints, pose search databases, animation montages, IK rigs and facial animation assets [doc]. Search the names for locomotion, pose search, motion matching, stride, foot and IK [I].
- **Walking first:** decide motion matching or a classic state machine, count clips, and write down how starts, stops and turns are handled and how feet are kept planted (foot locking, leg IK, stride warping) [doc].
- **Then:** interactions (sitting, standing up, opening doors, leaning, smoking, carrying) with a count of ambient animations a street uses; talking (gestures, facing, lip sync audio driven or authored); crowds (shared or simplified animation at a distance) [doc].
- **Measure:** clip counts by category, the locomotion setup and its settings, foot sliding where visible, interaction types per street [doc].
- **Recorded play:** a short walk start, stop and turn, filmed from the side at the game's own camera, to see foot sliding by frame.
- **Output:** the method for our walk and a list of the ambient animations Quay Street needs, each with its source route (Mixamo or our own) [doc]. Jafar's 13 October ruling already rebuilds the walk on Epic's Game Animation Sample with motion matching, so the page compares the shipped game's settings against that sample's, and flags where they differ.
- **Rule to keep:** no animation clip is copied, not as a stand-in either.

## Study 8: Sound

- **Game and source:** Mafia first, KCD2 second; files [doc].
- **Look first:** sound cues and their wave files, audio volumes in the levels, mix settings [doc]. Search for ambience, loop, footstep, reverb, attenuation, and for the names of surfaces and shoe types [I].
- **Measure:** file counts by category, layers per area, reverb settings per space type (street, alley, interior, doorway), loudness targets; footstep variants per surface and shoe type, wet and dry; the objects that make sounds (doors, shop bells, cars, phone boxes); music start, fade and tension; the relative mix of ambience, voices, effects and music [doc].
- **Loudness from play:** a recorded two-minute stand in one street, by day and by night, measured in loudness units by a script on the PC. The numbers go in the page, the audio stays on F:.
- **Stop rule:** counts by file names only, never opening a wave in the repository. If a cue cannot be read in the first hour, take the layer count by ear from play.
- **Output:** an ambience plan for Quay Street (proof P13) with layer lists and loudness targets [doc]. Unit 10 of this week's queue built street sound from CC0 recordings (production/cloud-week/sound/), so the page is set against its manifest: which layers it has, which it lacks, and what level each should sit at.

## Study 9: Camera, controls and feel

Run with studies 10, 12 and 13 in one session of about three hours [doc].

- **Game and source:** Mafia; files and play [doc].
- **Look first:** the camera setup (spring arm length, height, shoulder offset, field of view, lag and smoothing) in the player's Blueprint and its camera manager; the input mapping assets [I].
- **Measure:** camera distance, height, shoulder offset, field of view; lag and smoothing; what the camera does near walls; field of view changes when running, aiming or talking; interaction distance and angle, how prompts appear, input buffering [doc].
- **Recorded play:** a walk along a wall and into a corner, filmed with the HUD off, to see the camera pushed in. Our camera ended up inside Tom's back once, so this is the point of the study [doc].
- **Stop rule:** a number not found in the files within the first hour is measured from the recording by frame and marked "measured from play".
- **Output:** camera and input numbers for Tom [doc].

## Study 10: Interface

- **Game and source:** Mafia; play first, then files [doc].
- **Look first:** a recording of the opening hour with the interface on (the same recording as study 2); then the interface assets by name (widgets, fonts, subtitle settings) [I].
- **Measure:** which elements show and when they hide; prompts; map and menus; fonts and sizes at 1920 by 1080 and 3440 by 1440; subtitles; accessibility settings [doc].
- **Screenshots:** fixed positions at both screen sizes, HUD on, kept on F:. Only our own game's interface is ever shown in a page.
- **Stop rule:** menus are listed by screen, not by option. Each screen is one line.
- **Output:** a side by side with our interface design, and what to change [doc].

## Study 12: Tech and budgets

Run with studies 9, 10 and 13 [doc].

- **Game and source:** Mafia; files [doc].
- **Look first:** the config files (scalability settings and their defaults), the streaming and memory settings, the levels' culling and distance setups, shader counts by name [doc, I].
- **Measure:** scalability defaults; memory and streaming budgets; how a dense town holds its frame rate (distant buildings, culling, shader counts, loading) [doc]. For the shop glass, one worked example: what the glass costs in the game and how it was kept cheap.
- **Our own numbers beside them:** the performance exit is a median frame of 16.7 ms and a worst of 25 ms [doc, PLAN.md].
- **Recorded play:** a frame time overlay in one dense street and in one empty one, with the game's own console command for statistics where it works, written down as a number.
- **Stop rule:** one hour for the config files. If a budget is not written anywhere, it is measured from the overlay and marked as measured.
- **Output:** a budget table beside our performance exit, and the shop glass example [doc].

## Study 13: Production pipeline

Run with studies 9, 10 and 12 [doc]. It is the cheapest study and the most useful for the catalogue.

- **Game and source:** Mafia; files [doc].
- **Look first:** the file index FModel builds (the first export index of the set-up [doc]): the folder tree, the prefixes and suffixes of names, asset counts by type [doc].
- **Measure:** the folder structure, the naming convention (write the rule as a pattern, with no example names copied wholesale), asset counts by type, which tuning lives in data tables and curves instead of code [doc].
- **Stop rule:** the study ends when the naming rule can be stated in five lines and the count table is filled. No asset is opened for its content.
- **Output:** improvements to our catalogue, naming and data-driven tuning [doc]. CATALOGUE.md's homes table is the thing it is set against.

## Study 14: Combat and violence

- **Game and source:** both games, files and play [doc]. KCD2 for melee timing, stamina and what the town does about a fight. Mafia for how two bodies connect and for knife duels, brawls and guns.
- **Before it:** read COMBAT.md (this folder), which holds the public numbers already found and a list of 39 rows of what the design still lacks; and his design, LEDGER Combat: Final State. This study answers the gaps and does not repeat the public pass.
- **Look first, KCD2:** the combat tables and scripts (moves, weapons, stamina, perks) [doc]. In the table list, the groups on combat, weapons and perks under `Libs\Tables\rpg\` [K, I].
- **Look first, Mafia:** animation montages, motion warping and hit reaction setups, the combat AI Blueprints and the damage tables [doc].
- **Measure:** wind-up, strike and recovery times (frames and seconds); hit pause in frames; hit reactions by type; attackers at once; blows and stamina per knockdown; paired move counts; how fast witnesses and police respond [doc].
- **Recorded play:** one duel and one three-on-one in each game, filmed at the game's own camera, logged in single frames around each contact.
- **Content rule:** fights in a tavern are noted by their mechanics only. No drink and no gambling appear in any note.
- **Stop rule:** one hour for the first read of the tables. Whatever is missing after that is measured from the recordings.
- **Output:** the numbers the combat design still lacks, the move and reaction list for the first combat test, and the move count the animation source test must reach [doc]. Jafar's rulings of 12 October stand: Tom does not improve at fighting, he cannot die, guns come after melee works, and fighting must look and feel AAA. The page says which numbers serve each.

## Study 16: Jobs and story

- **Game and source:** KCD2 first, Mafia for staging and cutscenes; files and play [doc].
- **Look first, KCD2:** quest data and scripts. Skald, Warhorse's own quest and dialogue editor, shows quests as a concept graph, from the quests folder under `data\Quests\Final` down [K]. The Lua scripts for quests are in `Scripts.pak` [K].
- **Look first, Mafia:** mission Blueprints and Sequencer assets [doc]; names only at first, to count missions and cutscenes [I].
- **Measure:** job counts and lengths; branches and failure states per job; cutscene counts and lengths; journal entry types [doc].
- **Questions to answer for LEDGER:** what happens when the player is late, caught or hurts the wrong man (failure that continues); how directions are given without waypoints (dialogue, notes, landmarks, the journal); how consequences are stored and return later [doc].
- **Recorded play:** one full job from the first word to the last in each game, with the journal open at each step.
- **Stop rule:** pick three jobs of different sizes (small, middle, large) and take them apart in full. Counts for the rest come from the quest list.
- **Output:** a job template for the builder, targets for jobs without waypoints, and inputs for the three acts [doc]. The template is set against the town content of unit 11 (production/cloud-week/town/), where each person's facts and errands already exist.

## Not reached and not done

- No game, tool or page was opened for this file. Everything marked [doc] comes from his study document, which was read in full on 13 October 2026; everything marked [K] from KIT.md; every [I] is general knowledge to be confirmed at the PC.
- KIT.md's own list of pages not reached still stands (the Warhorse and Epic talks, Steam's licence terms for the modding tools).
- Whether the lab session may read exported tables and text itself, or only the numbers and structures it counts, is still his to answer (KIT.md section 0). Until he answers, every page above assumes counts and structures only.
