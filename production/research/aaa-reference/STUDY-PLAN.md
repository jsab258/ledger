<!-- Imported 25 October 2026 from his Claude Docs doc "LEDGER AAA Reference Study" (https://claude.ai/artifact/Bk6Tfpg4wRusZi2p3AEhXE, revision 29), his order of 25 October. His words, unchanged; the doc is the source, this a copy. -->

# LEDGER: AAA Reference Study

Mafia: The Old Country and Kingdom Come: Deliverance II, studied end to end · Oct 11, 2026 · @Jafar

## Purpose

One full AAA game, opened up through its files, its code and its play, gives LEDGER measured answers instead of guesses for every discipline a town-scale crime game needs.

- **Why Mafia: The Old Country.** Unreal Engine 5, third-person, crime, a period town with people living in its streets, period clothes. It is the closest match to LEDGER in engine and look. Kingdom Come: Deliverance II, already installed, is the closest match in systems and takes those studies (see its section).
- **What we want out of it.** Numbers, structures and setups that become exact targets for the builder: the decompilation lesson of 7 and 8 October (exact target, automatic check, rebuild until it matches), applied to every discipline at once.
- **Every finding is tied to LEDGER.** Each one names the plan phase, item or risk it serves, and says adopt, adapt or ignore.
- **Not only visuals.** NPC life, the first 30 minutes, dialogue, world building, characters, animation, sound, camera, interface, systems, combat, crime, jobs, budgets and pipeline are all in scope.

**Guardrail: study only.** Nothing from the game goes into LEDGER: no file, texture, mesh, sound, animation, code or text, not even as a stand-in. Exported material stays on the PC's F: drive in a study folder outside git. Only our own written findings, measurements and comparison notes go into the repository.

Legal risk: accepted by Jafar on 11 October 2026.

## Method

Three ways in, used in this order: the game's files first, its code only where the files are silent, and recorded play for everything that only shows in motion.

1. **The game's files (main source).** FModel, a free open-source viewer for Unreal packages, opens what the game ships: meshes, materials and their parameters, textures, animation assets, Blueprints (the game's visual scripts), data tables, curves, behaviour trees, sound setups, config files and level layouts.
   - It needs the game's encryption key, usually published by the modding community, and a mapping file for the game's engine version.
   - Exports go to F:\\LedgerTools\\aaa-study\\mafia, never into git.
2. **The code (where the files are silent).** REA with Ghidra reads systems compiled into the game's program in C++, such as NPC perception or crime detection, when they are not in Blueprints.
   - Time-boxed: the first hour decides how readable the code is. If it isn't, we rely on files and play.
3. **Recorded play.** Jafar records the opening and a few chosen scenes with Windows Game Bar or AMD's recorder. The AI analyses frames and timing from the video.
   - Optional: an Unreal console tool for a free camera and view modes (wireframe, lighting only), to see how scenes are built.
   - Fixed-position screenshots with the HUD off, for comparing with our own street.

**Who does it:** the lab session, as bounded studies of three to four hours, so the builder is never interrupted. Each study ends in a page for Jafar and a markdown file in the repository.

**No blind spots: the coverage map.** Before the first study, the lab lists every system each game has and where its logic lives, so nothing is missed just because it sits in code.

- The list comes from three sources: the game's own names for its systems (Mafia's Unreal class names stay readable even in the shipped game; KCD2's script and table names), the file index, and every behaviour seen in Jafar's recordings.
- Each system gets one line: what it does, where its logic lives (data, Blueprint or script, or compiled code), and which study covers it.
- Any system LEDGER needs whose logic lives only in compiled code gets a targeted code read, whatever the one-hour readability test said.
- Anything seen in play that no file or code read explains is listed as an open blind spot, never quietly dropped.
- Each study ends by ticking its systems off the map. The map lives in REFERENCE.md, and the checkpoint after the first four studies shows Jafar the open blind spots.

**Set-up, once:**

- [ ] Mafia: The Old Country installed on the PC, after a disk-space check against the retention floors
- [ ] FModel installed and set to the game's engine version, key entered by Jafar
- [ ] A first export index: a list of every package and asset type, to plan where each study looks, then the coverage map
- [ ] Jafar's recording of the first hour of a new game, without skipping

> *Set-up record (the session, 25 October 2026; his order of that day):*
> - **Mafia's file key:** published on 8 August 2025 by the user JimCollin in the public thread "Mafia: The Old Country" on Gildor's Forums (UE Viewer's forum), https://www.gildor.org/smf/index.php?topic=9279.0, read without an account on 25 October 2026. The same post gives the engine as Unreal 5.4.
> - **Kept and checked:** the key is kept in F:\LedgerTools\keys\mafia-aes.txt, never in git. It decrypts the name index of all eight encrypted containers and of every .pak file, and the names found match the package count taken before the key, container by container (139,791).
> - **FModel:** set to Unreal 5.4 with the key. It runs on Microsoft's .NET 10.0.13 runtime, downloaded on his yes from Microsoft's own release list (both zips' SHA-512 checked) to F:\LedgerTools\dotnet10, installed into nothing. It mounts 18 of the 19 archives with the key (372,542 files; the global container needs no key) and reads the game's 26,273 English text entries.
> - **Packages do not open yet:** opening one (a difficulty data table) stops at "Package has unversioned properties but mapping file (.usmap) is missing". A mappings file describes the game's own classes; none is published (searched the same day), and making one means running a dump tool inside the game, which is extraction, so it is his call (FOR-JAFAR, Needs you 2).
> - **Where the rest stands:** the first index and the coverage map are in REFERENCE.md.

## The studies at a glance

Sixteen studies cover everything an AAA game is made of; the first four and combat (14) are the ones LEDGER needs most.

| # | Study | The main question | Where it helps LEDGER | Priority | Game | Main source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | NPC life and AI | How does the town live, notice crimes and react? | The crime sim's core: witnesses, rumours, a living town (phase 3) | Highest | KCD2, then Mafia | Files, code |
| 2 | The first 30 minutes | What happens minute by minute, and why does it hold? | Phase 3 exit, the friends' build | Highest | Both | Play |
| 3 | Dialogue and barks | How much is written, how is it triggered and kept varied? | Authored facts, the talk's content needs | High | KCD2, then Mafia | Files |
| 4 | Street and world building | What makes a street dense and believable, in numbers? | Phase 2: Quay Street, then the town | High | Mafia, KCD2 second | Files, play |
| 5 | Visuals | How are windows, glass, light, wet streets and wear done? | Our open visual problems, the look file | High | Mafia | Files |
| 6 | Characters and wardrobe | What is a game-ready period garment, and how is a crowd dressed? | Clothes, crowds | High | Mafia (assets), KCD2 (system) | Files |
| 7 | Animation | How do people walk, sit, open doors and talk? | The walk, the speaker | High | Mafia | Files, play |
| 8 | Sound | How is a street made to sound alive? | Ambience (P13), phase 2 | Medium | Mafia, KCD2 second | Files |
| 9 | Camera, controls and feel | What are the camera and input numbers? | Every minute of play | Medium | Mafia | Files, play |
| 10 | Interface | What shows on screen, when, and how? | The friends' interface | Medium | Mafia | Play, files |
| 11 | Systems | How do crime, reputation, money, saves and missions work? | Phase 3 and later | High | KCD2 | Files, code |
| 12 | Tech and budgets | How do they hold the frame rate in a dense town? | Performance exit, the shop glass | Medium | Mafia | Files |
| 13 | Production pipeline | How are thousands of assets named, organised and tuned? | Catalogue, naming, data-driven tuning | Low, cheap | Mafia | Files |
| 14 | Combat and violence | How does a fight read, land and end, and what does the street do? | The combat design, the first combat test | Highest | Both | Files, play |
| 15 | The crime toolkit | How do theft, trespass, locks, stolen goods, fencing, fines and jail work? | The crime layer's owed verbs, fencing | High | KCD2 | Files |
| 16 | Jobs and story | How are jobs built, failed and guided without waypoints? | Jobs without waypoints, the three acts | High | KCD2, then Mafia | Files, play |

## Study 1: NPC life and AI

The most important study: how a professional game makes a town feel lived in, and how its people notice, remember and report what the player does.

**Questions**

- **Daily life:** do townspeople follow schedules (home, work, shop, pub), or only loop where the player can see them? How fine is the schedule: hours, places, activities?
- **Smart objects:** how are benches, counters, doorways, stalls and lamp posts made usable by NPCs? How many per street, and how does an NPC claim one?
- **Crowds:** how many people are on screen in a street by day and at night? How are they spawned and removed around the player, by area, time and weather?
- **Perception:** sight cones and distances, hearing radii, how long it takes to notice something, what counts as a crime.
- **Witnesses:** what happens after a crime is seen: flee, report, phone, gossip? How long do they remember, and does it spread?
- **Reactions:** to the player (looking, stepping aside, fleeing), to weather (shelter, umbrellas), to noise and events.
- **Principals and crowd:** how do named characters differ from passers-by in their logic and data?

**What to measure:** NPC counts per street by time of day, perception distances and timings, activities and smart objects per street, schedule granularity, memory and decay times.

**Where it lives:** behaviour trees and their blackboards, state trees, smart object definitions, environment queries, crowd and density settings, AI perception settings, data tables of schedules and activities. C++ code only if those are thin.

**Output for LEDGER:** a page "How Mafia's town lives", with a drawing of the NPC loop and a table of the numbers. A list of what LEDGER already does differently (our simulation, witnesses, rumours, who-told-me) and what to adopt: for example smart objects for benches and doors, density by time and weather, perception timings. Feeds TOWN.md, phase 3 and the proof P4.

## Study 2: The first 30 minutes

A minute-by-minute breakdown of how an AAA game opens, as the benchmark for LEDGER's phase 3 goal of thirty minutes that hold a newcomer.

**How:** Jafar starts a new game and records the first 60 minutes without skipping anything, cutscenes included. The AI logs the recording in 10-second steps.

**What to log for each beat**

- What the player does, sees and learns, and what the game is teaching at that moment
- Who is on screen and talking; what the player is told to do, and how (prompt, objective text, a character's line)
- Play or cutscene; tension rising, falling or quiet

**What to measure**

- Time to first control, first free movement, first conversation, first choice, first conflict, first reward
- Cutscene time against play time, minute by minute
- How controls are taught: prompt types, how often, when they stop
- How many distinct activities happen in 30 minutes, and the longest stretch with nothing new
- When each piece of interface first appears
- How the world opens up: gated, guided or free
- Checkpoints and saves; the first way to fail and what it costs

**Output for LEDGER:** a drawn timeline of the opening's beats, a table of the measurements, and a side-by-side with LEDGER's phase 3 exit (two newcomer routes, at most five empty minutes, a consequence seen and kept). It becomes the benchmark the friends' build is judged against.

## Study 3: Dialogue and barks

How much a believable town has to say, and how a shipped game stores, triggers and varies it; barks are the short ambient lines people say in passing.

**Questions**

- How is dialogue stored: string tables, dialogue assets, data tables? How are conversations and choices structured?
- How many lines in total; per main character; per passer-by?
- Which bark situations exist: greetings, bumping into someone, weather, seeing a crime, being threatened, the player's clothes or reputation?
- How is repetition avoided: cooldowns, variants per situation, voice sets per type of person?
- How are conversations staged: camera, positions, gestures, who looks at whom?
- How long is a typical line, in words and in seconds; how are subtitles shown?

**What to measure:** line counts by character and situation, variants per situation, cooldown times, average line length, number of distinct voices.

**Where it lives:** the localisation and string tables (often the complete text), dialogue data, voice file names (which reveal line counts by speaker), bark logic in Blueprints.

**Output for LEDGER:** numbers for how much authored content each kind of character needs, a model for ambient lines that need no model call and play instantly, and staging rules for conversations. Feeds the talk, authored facts and the casting sheets.

## Study 4: Street and world building

The numbers behind a dense, believable street, measured from the game's own level files, to set targets for Quay Street and the town after it.

**Questions**

- Street widths, block lengths, building heights, door and window spacing
- How many unique buildings, against kit pieces and their variants
- How much clutter: props per 10 metres of street, by kind (bins, signs, crates, bikes, litter)
- Which interiors can be entered, which are faked behind glass, which are closed
- Sightlines and landmarks: how the player finds their way without a map
- How the edges of the world are hidden: hills, fog, blocked streets
- How the world is streamed: cell sizes, distant versions of buildings, layers switched by time of day or story
- Parked vehicles, vegetation, weather-dependent dressing

**What to measure:** actor counts by type in one representative street, distances, unique meshes against instances, interior counts, streaming cell size.

**Where it lives:** level and world partition files, data layers, prefab-like assemblies, the mesh library.

**Output for LEDGER:** target numbers for phase 2 (props per metre, unique pieces per street, variants per piece, interior strategy) that become automatic checks on our street.

## Study 5: Visuals

How a shipped Unreal 5 game solves the exact visual problems LEDGER is stuck on, read as settings and setups the builder can compare line by line with our look file.

**Questions, by problem**

- **Windows** (ours read as white boards): frame depth, glass material, fake rooms behind the glass, curtains and nets, how they look from a low street angle.
- **Shop glass** (ours costs frames): reflection method (captures, screen-space, Lumen) and what it costs.
- **Light** (ours lacked pools at night): exposure, sky, fog, Lumen settings; night lamps' brightness, reach and light profiles; how many lights per street.
- **Wet streets** (ours mirrored the sky): how puddles, wet stone and rain are built into the materials.
- **Wear:** decals, vertex painting, grime masks, how dirt gathers at the foot of walls.
- **Materials:** the structure of the main materials, how many variants, how surfaces are layered.
- **Texture budgets:** texture sizes and detail per kind of object.

**What to measure:** the settings themselves (exposure, light values, reflection settings), decal counts per street, texture sizes, material counts.

**Where it lives:** post-process and lighting setups in the levels, material instances and their parameters, config files, textures.

**Output for LEDGER:** a settings sheet set beside our look file, and one target per open visual problem.

## Study 6: Characters and wardrobe

What a finished, game-ready period garment actually is, and how a whole crowd is dressed from a small set of pieces, so our clothing work finally has a real target.

**Questions**

- **Bodies:** custom or MetaHuman-based? Detail levels, polygon counts, texture sizes per character.
- **Wardrobe structure:** which slots (shirt, trousers, jacket, coat, hat, shoes), how pieces combine, how one garment fits different bodies.
- **One period jacket in detail:** its shape, polygon count, how the lapel and collar are modelled, which folds are in the mesh and which only in the texture, which parts move as cloth.
- **Variety:** how many base garments, how many colour and fabric variants, how many unique looks in a street crowd, how repeats are hidden.
- **Hair, hats and accessories:** how they are made and fitted.

**What to measure:** garment counts by slot, variants per garment, polygon and texture budgets, cloth-simulated parts.

**Where it lives:** character and outfit assets, skeletal meshes, cloth assets, material instances, crowd appearance tables.

**Output for LEDGER:** the clothing target in numbers and structure (what our jumper, trousers and jacket must be), a crowd-dressing recipe, and the facts for the clothes decision (keep the base layer, or the Marvelous month).

## Study 7: Animation

How the game makes people move naturally: the walk we keep failing at, plus everything else a street full of people does.

**Questions**

- **Walking:** motion matching or a classic state machine? How many clips, how starts, stops and turns are handled, how feet are kept planted (foot locking, leg IK, stride warping).
- **Interactions:** sitting, standing up, opening doors, leaning on walls, smoking, carrying things; how many ambient animations a street uses.
- **Talking:** gestures during conversation, how speakers face each other, facial animation and lip sync (audio-driven or authored).
- **Crowds:** how animation is shared and simplified at a distance.

**What to measure:** clip counts by category, locomotion setup and its settings, foot-sliding tolerances where visible, interaction types per street.

**Where it lives:** animation blueprints, pose search databases, animation montages, IK rigs, facial animation assets.

**Output for LEDGER:** the method for our walk, and a list of the ambient animations Quay Street needs, each with its source route (Mixamo or our own).

## Study 8: Sound

How a street is made to sound alive; sound is half of what makes a place feel real, and LEDGER has barely started on it.

**Questions**

- **Ambience:** which layers make up a street (distant traffic, gulls, harbour, voices, radios through windows), and how they change by day, night and weather.
- **Footsteps:** how many variants per surface and shoe type; wet and dry.
- **Spaces:** echo and muffling per space (street, alley, interior, doorway).
- **Objects:** doors, shop bells, cars, phone boxes.
- **Music:** how it starts, fades and reacts to tension.
- **Mix:** relative loudness of ambience, voices, effects and music.

**What to measure:** sound file counts by category, layers per area, reverb settings, loudness targets.

**Where it lives:** sound cues and their wave files, audio volumes in the levels, mix settings.

**Output for LEDGER:** an ambience plan for Quay Street (proof P13) with layer lists and loudness targets.

## Studies 9 to 13

Five smaller studies, run together in one session, each giving numbers LEDGER can copy as targets with little effort.

**Study 9: Camera, controls and feel**

- Camera distance, height, shoulder offset, field of view, lag and smoothing; what happens near walls (our camera ended up inside Tom's back).
- Field-of-view changes when running, aiming or talking.
- Interaction distance and angle, how prompts appear, input buffering.
- Output: camera and input numbers for Tom.

**Study 10: Interface**

- Which elements show, when, and when they hide; prompts; map; menus.
- Fonts and sizes at 1920 by 1080 and 3440 by 1440; subtitles; accessibility settings.
- Output: a side-by-side with our interface design, with what to change.

**Study 11: Systems**

- Heat and police: what raises it, how it falls, how witnesses feed it.
- Money: where it comes from and where it goes.
- Saves: when, what is kept, how restarts work.
- Missions: how they are structured as states; time of day and weather systems.
- Output: inputs for phase 3 and the systems after it.

**Study 12: Tech and budgets**

- Scalability settings and their defaults; memory and streaming budgets.
- How a dense town holds its frame rate: distant buildings, culling, shader counts, loading.
- Output: a budget table beside our performance exit (median frame 16.7 ms, worst 25 ms), and the shop glass example.

**Study 13: Production pipeline**

- Folder structure, naming conventions, asset counts by type.
- How tuning lives in data tables and curves instead of code.
- Output: improvements to our catalogue, naming and data-driven tuning.

## Study 14: Combat and violence

How the best grounded melee in games reads, lands and ends, measured so LEDGER's combat design (LEDGER Combat: Final State, 12 October 2026) gets exact targets instead of guesses.

**Questions**

- **The read:** how long are the wind-up, strike and recovery; how does the body show what is coming; how does the camera behave in a fight without lock-on?
- **The contact:** hit-pause length, camera jolt, sound layers; how many hit reactions, how they vary by blow and body part, and how much is physics and how much authored.
- **The odds:** stamina per blow, blows to put a man down, how many attackers swing at once while the others wait, how one man fares against three.
- **The surroundings:** paired moves against walls, doors, railings and the ground; picking up improvised weapons; how many such moves exist.
- **Before the blows:** stand-offs, threats and intimidation; how fights start and how they end (backing off, fleeing, surrender, knockout, death).
- **The street's response:** what witnesses, guards and police do during and after, and how a fight becomes a report, a crime and a reputation.
- **Weapons:** how one system stretches from fists to knives, clubs and Mafia's guns, and what changes in timing and lethality.

**What to measure:** wind-up, strike and recovery times; hit-pause frames; reaction counts by type; attackers at once; blows and stamina per knockdown; paired-move counts; how fast witnesses and police respond.

**Where it lives:** KCD2's combat tables and scripts (moves, weapons, stamina, perks); Mafia's animation montages, motion warping and hit-reaction setups, its combat AI Blueprints and damage tables.

**Output for LEDGER:** the numbers the combat design still lacks, the move and reaction list for the first combat test, and the move count the animation source test must reach.

## Study 15: The crime toolkit

How a game makes small crimes work as systems: stealing, trespassing and getting caught, the half of LEDGER's crime layer that is not violence.

**Questions**

- **Theft and pickpocketing:** how ownership is marked, how stolen goods are flagged, who recognises them and for how long.
- **Trespass:** which places are private at which hours, how warnings escalate, locked doors and lockpicking.
- **Fencing:** who buys stolen goods, at what discount and with what risk.
- **Getting caught:** searches, fines, bribes, jail, and what the player loses.
- **Reputation:** how standing in each place changes after each kind of crime.

**What to measure:** discounts, fines, search chances, how long a stolen flag lasts, warning steps, jail lengths.

**Where it lives:** KCD2's item, faction, crime and shop tables and scripts.

**Output for LEDGER:** targets for buying, selling and fencing (the 23 September ruling) and for the crime layer's owed verbs.

## Study 16: Jobs and story

How a big game builds its quests as data, keeps them going when the player fails, and guides him without waypoints, which is how LEDGER's jobs must work.

**Questions**

- **Structure:** how a job is built from states, conditions, branches and timers, as data or as script.
- **Scale:** how many jobs, how long each, how many branches and endings.
- **Failure that continues:** what happens when the player is late, caught or hurts the wrong man.
- **No waypoints:** directions in dialogue, notes, landmarks and the journal; how a game without markers stays playable.
- **Cutscenes:** how many, how long, how they are staged and skipped.
- **Memory:** how consequences are stored and come back later.

**What to measure:** job counts and lengths, branches and failure states per job, cutscene counts and lengths, journal entry types.

**Where it lives:** KCD2's quest data and scripts; Mafia's mission Blueprints and Sequencer assets.

**Output for LEDGER:** a job template for the builder, targets for jobs without waypoints, and inputs for the three acts.

## Beyond the studies: four project-level uses

Four uses look at the whole project rather than one discipline. All four need only public sources, so the cloud session started them on 12 October (unit 7b), with a first public pass on combat beside them.

| Use | What it gives LEDGER | File |
| --- | --- | --- |
| The credits as an org chart | Every AAA role mapped to who covers it in our AI studio; every "nobody" is a gap, and the list becomes the recipe's role list | CREDITS-MAP.md |
| A content census | Counts of people, lines, jobs, buildings, interiors and items per km² and per hour of play: the town's size targets and the recipe's scaling rule | CENSUS.md |
| What players noticed | The twenty things players praised and the twenty they punished, each tied to a gate, proof or risk | PLAYERS.md |
| Developer talks | How and why the two studios built things, and where the lab should look in the files | TALKS.md |
| Combat, public pass | KCD2's melee and Mafia's knife duels and brawls from guides and talks, set against the combat design | COMBAT.md |

All five files land in production/research/aaa-reference/.

## Outputs

Every study ends in measured findings the builder can turn into exact targets, kept in one reference file it checks before building anything new.

- **A page per study for Jafar:** findings, our own comparison screenshots, and a "for LEDGER" list where each finding says adopt, adapt or ignore, and names the plan item, phase or risk it serves.
- **The reference file in the repository:** production/research/aaa-reference/mafia/, one markdown file per study plus REFERENCE.md as the index. Numbers, structures and descriptions only; no extracted content.
- **How the builder uses it:** before building a new family (a door, a crowd, an ambience, a camera), it looks up the matching numbers; every target cites the reference line it came from; fresh reviewers get the reference beside the result.
- **How findings become checks:** a number such as props per 10 metres or footstep variants per surface becomes an automatic check on our own street, the same way the window and door targets were checked.

## Order, time and cost

About 45 to 50 hours of lab time in all, run beside the builder over four to five weeks once the PC is back online. KCD2 goes first because it is already installed; the first four studies and combat come first, then Jafar decides on the rest.

1. **KCD2 set-up**, about 1 hour of lab time; Jafar records the first hour of a new KCD2 game.
2. **Study 1, NPC life and AI (KCD2)**, about 4 hours.
3. **Mafia set-up**, about 1 hour of lab time; about 15 minutes for Jafar (install, key), plus the first hour of a new Mafia game recorded.
4. **Study 2, the first 30 minutes (both games)**, about 4 hours.
5. **Study 4, street and world building (Mafia, KCD2 second)**, about 3 hours.
6. **Study 5, visuals (Mafia)**, about 4 hours.
7. **Study 14, combat and violence (both games)**, about 4 hours, before the first combat test.
8. **Checkpoint:** Jafar reads the first five pages and decides whether to run the rest, in this order:
9. **Studies 11 and 15, systems and the crime toolkit (KCD2)**, about 5 hours.
10. **Study 6, characters and wardrobe (both)**, about 4 hours.
11. **Study 7, animation (Mafia)**, about 3 hours.
12. **Study 3, dialogue and barks (KCD2, then Mafia)**, about 4 hours.
13. **Study 16, jobs and story (KCD2, then Mafia)**, about 3 hours.
14. **Study 8, sound (Mafia, KCD2 second)**, about 2 hours.
15. **Studies 9, 10, 12 and 13 together (Mafia)**, about 3 hours.

**Meter:** measured on the first study, then each study's cost is estimated before it starts; the builder keeps priority.

**Prerequisites:** the PC online; KCD2 already installed; Mafia owned and installed with enough disk space; FModel and Mafia's key; Jafar's recording of the first hour of each game; the lab session free.

## Second full study: Kingdom Come: Deliverance II

KCD2 is already installed on the PC and is the closest match to LEDGER's systems, so it takes the systems studies, while Mafia keeps the Unreal-specific craft.

- **Why KCD2:** a large town (Kuttenberg) where people follow daily routines, notice crimes, report them to guards and remember the player's reputation place by place. Layered clothes, dirt and blood change how people treat you, and conversations depend on reputation and appearance. That is LEDGER's social crime simulation in another century.
- **Mafia's limit:** it is reportedly a more linear, story-led game, so its town life is partly staged. It stays the best reference for Unreal 5 craft, a weaker one for a living town.
- **Engine:** CryEngine, not Unreal. Its game data sits in .pak archives, which are ordinary zip files. In the first game most data was readable tables and scripts; KCD2 is expected to be similar, to be confirmed at set-up. Systems and data carry over to LEDGER fully; engine settings much less.

**Which game for which study**

- **Study 1, NPC life and AI:** KCD2 first; Mafia second, for how Unreal's own tools are used.
- **Study 2, the first 30 minutes:** both. KCD2 shows an open-world start, Mafia a story start.
- **Study 3, dialogue:** KCD2 first for checks, reputation and appearance in conversation; Mafia for staging and barks.
- **Study 6, characters and wardrobe:** Mafia for the garment as an Unreal asset; KCD2 for wardrobe as a system (layers, dirt, how clothes change reactions).
- **Study 11, systems:** KCD2, for crime, fines, reputation per place, economy, time and needs.
- **Study 14, combat:** both. KCD2 for melee timing, stamina and what the town does about a fight; Mafia for how Unreal makes two bodies connect.
- **Study 15, the crime toolkit:** KCD2.
- **Study 16, jobs and story:** KCD2 first; Mafia for staging and cutscenes.
- **Studies 4, 5, 7, 8, 9, 10, 12 and 13:** Mafia, with KCD2 as a second opinion on street density and sound.

**KCD2 set-up**

- [ ] Unpack its .pak archives with 7-Zip into F:\\LedgerTools\\aaa-study\\kcd2, never into git
- [ ] A first index of the data: which tables and scripts exist, and where schedules, crime and reputation live, then KCD2's coverage map
- [ ] Jafar's recording of the first hour of a new KCD2 game

## Beyond Mafia

Mafia covers the whole craft; a few other games are each the best reference for one system LEDGER depends on, and the same method works outside games too.

**Reference games, one system each**

| Game | What to study | Why it matters for LEDGER | How readable |
| --- | --- | --- | --- |
| Kingdom Come: Deliverance II | Crime, witnesses, reputation, daily schedules, layered period clothing | The closest match to our crime, witness and clothing rules | Installed: now a second full study (section above) |
| Watch Dogs: Legion | Every passer-by generated with a job, schedule, relations and history | Our rule that every visible person has a simulation identity | Harder; mostly play and documented findings |
| RimWorld | Social simulation, relationships, a storyteller that paces events | Our town simulation and consequences | Written in C#, which REA's .NET analysis reads well |
| The Sims 4 | Social interactions, needs, moods, relationships | How small talk and relationships are modelled | Its tuning files are readable data |
| Hitman (World of Assassination) | Crowd suspicion, witnesses, disguises, who notices what | Witnesses and noticing, done to a very high standard | Harder; mostly play and documented findings |
| Disco Elysium | Dialogue writing, skill checks, a town told through conversation | Our talk and authored facts | Its dialogue database has been extracted by fans before |
| Red Dead Redemption 2 | Ambient life, NPCs who remember the player | The bar for a living world | Hardest; mostly play and documented findings |

**AI characters, for the talk and the town**

| Reference | What to study | Why it matters for LEDGER | How |
| --- | --- | --- | --- |
| inZOI | A city life sim on Unreal 5 whose characters reportedly think with a small AI model on the player's graphics card; how needs, relationships and AI thoughts fit together, and what it costs the card | The closest existing game to LEDGER's town and talk together | Its Unreal files (FModel) and play |
| AI character toolkits: Inworld, Convai, NVIDIA ACE | How their Unreal plugins and demos get a character speaking quickly: streaming, chunked voice, filling the first second, lip sync | Our failed speech target, 3.3 seconds against 2 | Plugin files, and what their demos send and receive (REA's network capture) |
| Where Winds Meet, Whispers from the Star | Shipped games with AI-driven conversation: keeping characters grounded, stopping invented facts, hiding the wait | Our claim check and the ladder | Play, and what the games send and receive |

**Uses outside games**

- **Sentrax:** competitors' RTLS apps and device firmware (REA reads Android apps and firmware): how they position, which protocols they use, how their apps present it.
- **Sentrax website:** take apart the best interactive 3D product sites to see how their scenes, loading and interaction are built, before building ours.
- **Trovu:** what competitors' outbound web apps reveal about how they enrich data and send messages.
- **Not for 2BCS work:** client and vendor systems are bound by contracts that put the risk on the employer, not on you.
