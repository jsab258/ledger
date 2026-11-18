# Digest 03: Studies 9 to 17 (aaa-reference studies)

Source folder: production/research/aaa-reference/studies/ (files 09 to 17). Each section below gives (a) the study's "For LEDGER" section verbatim, (b) key measured numbers, (c) blind spots, (d) any "twenty basics" mention.

Marking rule used throughout: any number read from a game's own files (Mafia: The Old Country, Kingdom Come: Deliverance II, "KCD2" or "Kingdom Come II"; Studies 9 to 16 were read 25 to 28 October 2026) is marked "(lead, from game files)". It is a lead, not evidence. Numbers from Warhorse's public modding wiki, reviews, talks, videos and public pages stand as they are and say so. Study 17 used public sources only, so nothing in it is a lead. Source tags in the studies: M measured, R read, I inferred, N a name only; these tags are kept in brackets where useful.

Blanket note for every verbatim "For LEDGER" block: numbers inside it that came from game files carry the lead status even where the verbatim text does not repeat the mark.

Twenty basics: a search of all nine files for "basics" and "twenty" found no mention. Section (d) of every study below says so.

---

## Study 9: Camera, controls and feel (path: production/research/aaa-reference/studies/09-camera-controls.md; dated 28 October 2026)

Method: Mafia (Unreal 5.4, third person) and KCD2 (first person) from their own files; public pages for play.

### a. For LEDGER (verbatim, section "For LEDGER")

1. **Adopt, through his page:** Mafia's street, room and talk framing for Tom. It changes the look of every frame, so it goes on one page as one decision (CLAUDE.md). It serves phase 1's packaged walk and the friends' build.
2. **Adapt, small:** the four proposed modes (street, run, room, talk) as rows in one spec, read by the existing camera arm. This is not a new camera system (29 September ruling). It also serves Study 13's tuning home.
3. **Adopt: tagged rooms** after NOW item 5. The office now passes its back wall through Epic's camera, so the room's numbers are tried there as a gate, not slipped into it.
4. **Adopt: Tom placed at 1.5 m for a talk.** It closes the 3 October camera fault, and goes on the same page as item 1.
5. **Adapt: choose the person ahead and in view,** held 0.2 s. It closes the 4 October fault and meets the style guide.
6. **Ignore:** aiming, cover, car and horse cameras (not a shooter, 12 October); the first-person camera; shots authored per line (LEDGER's talk is live). Camera shake goes under Reduce motion (Study 10), not a switch of its own.

### b. Key measured numbers

Comparison table (Mafia and KCD2 columns are all from game files unless stated):
- Lens on foot: Mafia 82 degrees, slider 50 to 120 (R) (lead, from game files); KCD2 slider 75 to 110 (R, public); LEDGER as coded 90 degrees (M, packaged walks 21 to 28 Oct; LEDGER's own game, not a lead); proposed for Tom 82 degrees, slider 70 to 110.
- On 3440x1440: Mafia about 99 x 52 degrees (I, Unreal's rule; PCGamingWiki "Hor+" agrees, public); LEDGER about 107 x 59 (I).
- Pivot: Mafia 1.25 m above feet, crouched 0.90 (R) (lead, from game files); LEDGER hip 0.88, office +0.6.
- Camera from pivot, back/side/up: Mafia 1.65, 0.45, 0.35 (R) (lead, from game files); LEDGER 3.20, 0.45, 0.55; proposed street 1.55, 0.40, 0.35 at 79 degrees.
- Town or walking, calm only: -3 degrees, 0.10 closer, 0.05 less to the side; blend 1.3 s in, 2.0 s out (R) (lead, from game files).
- Running: 85 degrees, 1.40 back, 0.2 s blend (R) (lead, from game files). KCD2 look range -35 to 45 degrees (R) (lead, from game files; perhaps an engine leftover, I).
- Rooms: standard ceiling 1.40 back; low ceiling calm only 1.20, 0.35 side, 78 degrees (R) (lead, from game files); LEDGER office arm 2.0.
- Pitch: Mafia -70 to 70, fully up the camera comes 0.9 in (R) (lead, from game files); KCD2 -70 to 80 (R) (lead, from game files).
- Lag: pivot spring up to 0.30 m; no auto-follow on foot by default (R) (lead, from game files).
- Blends: 1.0 s walking mode, 0.75 s transitions table (R, I) (lead, from game files); LEDGER arm eases at rate 4.
- Talk: Mafia player placed 1.5 m away; 63 degrees, pivot 1.50; 2 s blends (R) (lead, from game files); KCD2 a camera command on 80,812 of 147,859 lines (M) (lead, from game files).
- Target choice: Mafia body shapes to 2.75 m ahead; 60 degree camera cone to 5 m; choice held 0.2 s (R) (lead, from game files); LEDGER nearest.
- Reach: Mafia 2.5 default, 2.0 for talks; KCD2 doors 2.0, stashes 2.5, locks 1.5 (R) (lead, from game files); LEDGER talk 3.5, use 2.2.
- Holds: Mafia 0.2 to 4 s, taps within 0.15 to 0.3 s (R); KCD2 0.25 s on 48 actions, 0.5 s on 16 (M) (both lead, from game files).
- Mafia mode tables: 83 of 116 camera modes picked from one table by player state, 15 more from a table of paired moves (lead, from game files). Plain walking is row 82 with an empty rule (default picked in code, I).
- Walking: pivot spring at most 0.30 m; at 5 m/s lens widens 2%, camera eases up to 12 cm back (I) (lead, from game files).
- Layers on walking: alert 4 cm lower in 0.6 s; fight 15 cm lower in 0.4 s; focus 25 cm closer (lead, from game files).
- Lenses by state: sprint 85, talk 63, walk-and-talk 70 (10 narrower while lines play), aim 65 (lead, from game files).
- Collision safe point 1.95 m above feet, traced from 0.90 m (R) (lead, from game files).
- Mafia talk: five shots; from a 1.50 m pivot at 63 degrees: close 0.80 back 0.30 side; far 1.20 and 0.25; distant 1.70 and 0.45 (lead, from game files). A talk starts only with the camera within about 18 degrees of the speaker (I, from a 0.95 dot product).
- KCD2 shots per line (M): custom 28,819; close shot 14,135; close-up 12,496; medium 3,975 (lead, from game files). Placed scene cameras median vertical angle 22 degrees (M) (lead, from game files).
- KCD2 acts at screen centre (I); no angle limit on 91% of 1,375 placed objects (M) (lead, from game files).
- Mafia sprint toggles by default; neither game shows an input buffer in data.
- LEDGER current (own measurements, not leads): one spring arm, 12 cm probe from the hip, Tom hidden within 55 cm; packaged, Epic's sample camera hangs further back than the editor's (27 October, cause not found).
- Review: fresh reviewer checked about 115 numbers across Studies 9, 10 and 13, re-measuring 34: pass with fixes, all applied.

### c. Open blind spots (verbatim)

- Code: Mafia's default mode, hold length, probe and hide defaults; input buffering in both games.
- Epic's sample camera rigs in our packaged game (editor files, no editor today); Kingdom Come II's default lens; Mafia's input config (its raw export saved nothing).
- Feel in play: no recordings. One review found aim and camera share one sensitivity, making the camera "too sluggish" (Jimquisition, 19 August 2025).

### d. Twenty basics

None mentioned.

---

## Study 10: Interface (path: production/research/aaa-reference/studies/10-interface.md; dated 28 October 2026)

Method: Mafia and KCD2 own files (layout files read as text, settings tables, presenters) and public pages, beside LEDGER's style guide and code. A "unit" is a pixel on a 1080-tall screen.

### a. For LEDGER (verbatim, section "For LEDGER")

1. **Adopt, through his page:** the width and scale choice, which changes every screen on his monitor; it serves the friends' build, and the guide plans it "later".
2. **Adopt:** the three switches for the friends' build: small additions to existing screens, not new systems (29 September ruling).
3. **Adapt** prompts by facing (the FINDINGS fault "T opens the talk with whoever is nearest"); **adopt** shake under Reduce motion; **adapt** a photosensitivity line only if something flashes.
4. **Ignore:** markers, timers and a map (nothing he could not know), subtitle colours and colour-blind modes (no meaning rests on colour), aim assist (not a shooter).
5. **Keep the sizes:** larger than Mafia's, whose small default its critics named; Kingdom Come II's are not in its data.

### b. Key measured numbers

- Subtitle size: Mafia 26 x 0.8 / 1.0 / 1.2, default about 21 units (R) (lead, from game files); LEDGER 34 / 39 / 46 / 54, default 39 (LEDGER's own). On his 3440x1440: Mafia about 28 px, LEDGER about 52 px (I).
- Subtitle place: Mafia centre 51% of width, 60 up, split past 120 characters (lead, from game files); LEDGER last line 104 up, two lines at most.
- Backing: Mafia off (default), 50%, 100% (lead, from game files); LEDGER 80%, 0 to 100%.
- Colour: Mafia yellow default plus 4 more (lead, from game files); LEDGER one.
- Subtitle timing: Mafia in 0.2 s after 0.2 s, out 0.2 s after 1.0 s (lead, from game files); LEDGER in at once, out 150 ms, held at least 1 s.
- Reading text: Mafia body and prompts 20, titles 48 (lead, from game files); LEDGER key hints 30, choices 48 to 50, nothing under 24.
- HUD parts: Mafia 17 presenters, 17 switches (lead, from game files); KCD2 27 UI elements, HUD 70 clips (M) (lead, from game files).
- Wide screens: Mafia corners or fixed, safe zone 80 to 100%, HUD scale 0.8 / 1 / 1.2 (lead, from game files); KCD2 none in data.
- Settings: Mafia 122 in 14 groups (10 ungrouped), 12 under accessibility (M); KCD2 88 buttons on 18 pages (M) (both lead, from game files); LEDGER 22 lines on 4 tabs (picture 10, sound 4, controls 2, subtitles and reading 6).
- Mafia HUD logic (decoded from presenters): weapons, items and health hide only in calm; objectives Always On by default, Automatic shows 30 s (text) and 5 s (marker) on change; subtitles hide only while loading (lead, from game files).
- KCD2 before patch 1.4: compass and bottom bars always on (R, public: UI designer teardown, 8 July 2025); patch 1.4 (9 September 2025) added adaptive option (public).
- KCD2 146 verb strings (M) (lead, from game files); map fog of war 2,601 cloud pieces (lead, from game files).
- At 1080: subtitles Mafia 21 default, 31 largest; LEDGER 39 and 54. Prompts Mafia 20, LEDGER 30.
- Public reviews: button prompts lower right, hard to read on light ground (Can I Play That?, 29 August 2025); Mafia subtitles may be small for low vision (Thumb Culture, 19 August 2025).
- Review: pass with fixes, all applied.

### c. Open blind spots (verbatim)

- Font sizes as played, and all of Kingdom Come II's sizes: its Scaleform files are not unpacked.
- What Kingdom Come II's adaptive option hides, and hardcore's full list: the public sources disagree.
- Mafia's prompt position in play: left in the layout, lower right in a review.
- Either game at 21:9 in play: no recordings.

### d. Twenty basics

None mentioned.

---

## Study 11: Systems (path: production/research/aaa-reference/studies/11-systems.md; dated 28 October 2026)

Method: KCD2 and Mafia data plus Warhorse's public modding wiki, not code. KCD2 money is in tenths of a groschen; figures in groschen (gr).

### a. For LEDGER (verbatim, section "For LEDGER")

1. **Propose: a delay before the police act, read from the talk.** LEDGER's heat is the street's talk (fading on a 96 h half-life, 144 h while Ellis is in town: Gossip, EllisSetup), and Ellis comes for talk from day 4 once three people pass it round (PoliceFile Loudness). Kingdom Come II's 12 h delay and two posture steps suggest a constable's beat on Quay Street at a lower loudness, before Ellis. A new system: under the 29 September ruling it waits for a place in PLAN.md. **Ignore** faction anger as a number: the town has no opinion, only people (D34).
2. **Adopt: money that runs out at the counter and restocks weekly.** Already built (Purses; Economy's weekly suppliers); Kingdom Come II confirms the shape. **Adapt** hours from people and doors, Meridian's from LEDGER's own 1990 research (owed). Serves D24 (trade must not look broken) and the 23 September ruling (buying, selling).
3. **Adopt: a save at every job step, held during a fight.** LEDGER saves after each committed decision (GameController) and keeps state only (SaveCodec), as Kingdom Come II does for quests. For the Unreal port: save on every change of a job's state; in a fight or scripted moment the save waits, never refused. Serves phase 3's exit (kept after restart). **Ignore** the bought save and the checkpoint restart: reloading is never stopped and the game says what is permanent (D35, D58); an arrest costs hours, not the game (Custody).
4. **Adopt for jobs: four job states and five step states,** limits on the town's clock (median 4 h), cancelled steps. To Study 16's job template (jobs, no waypoints: 23 September).
5. **Adopt: weather as weighted profiles feeding routines,** for phase 3's weather proof: one saved wetness value, drizzle and rain profiles changing who is out; no sunshine in the friends' build. **Ignore** Mafia's weather set per checkpoint.
6. **Adapt Mafia's presets for light:** clock, light, exposure and sky in one preset. LEDGER's day and night (7 October: four or five states later, no moving sun) can be two presets, then four.
7. **Measure the clock against the thirty minutes.** The C# game runs a day in 12 real minutes (GameController), Kingdom Come II in 96: phase 3's thirty minutes are two and a half days in LEDGER, under eight hours there. Playing them answers it; noted, not decided.

### b. Key measured numbers

KCD2 (all lead, from game files unless marked wiki):
- Heat: no meter; anger 0 to 1 per person and faction (theft +0.1 to 0.2, killing +0.8); a faction's change acts 12 h late, clears in about 34.7 h (R, I). Nervousness gone in 2.8 h (R, I).
- Police posture: all arm at anger 0.67; extra guards at 0.8; guards low under 0.3, middle to 0.6, high to 0.9; extra guards at most every 300 s (R).
- 119 anger event rows (51 animal reactions, 31 hostile-faction copies, 37 others, two lower it); lock heard picked 0.15 (0.4 among bandits), gunshot nearby 0.9.
- Reputation: 203 change rows, 166 losses, 30 gains; a charge talked away costs 0.18 (0.25 if the talk fails); reconciliation +1.2; paid indulgence 1 to 1,000 gr.
- Merchant cash 35 to 1,500 gr; restock 7 days across all 168 shops (M); up to about 212 gr in the median shop.
- Prices: food median 6.5 gr; clothing and armour 120 (p90 1,662); helmets 2,059.
- Autosaves: 686 save points in 126 of 135 quests, median 4 a quest; 33 important, 607 tied to an objective, 7 on area entry; after 1 h of sleep; 31 block saving (23 scripted scenes, 6 combat, 2 minigames). Bought save item 25 to 55 gr (four grades).
- Quests: 135; median 11 objectives (2 to 52); 45 micro, 43 side, 32 main or untyped, 15 activities; objectives median micro 4, side 16, main 17.5; 70 (52%) can fail; 119 can cancel an objective; 1,061 timers, 338 on world time, median 4 h, longest 336 h (14 days). 62 kinds of game over (11 general, 51 quest).
- Money in: 191 reward points, about 16,665 gr; 74 quests carry one (171 points, 16,100 gr); 11 fixed sums 5 to 1,000 gr; loot 14 presets 2 to 500 gr. Out: repairs 0.45 of value (0.6 hardcore); bed 5 gr a night or 50 gr to keep; fines median 75 gr.
- Shops: 168 (innkeepers 21, smiths 15, merchants 10, armourers 8; 58 in Kutná Hora). Buy and sell multipliers medians 0.8 and 0.5 over 2,840 rows. Townsfolk work 08 to 20, villagers 07 to 19, village services 08:00 to 22:30, town services 09:00 to 01:00; 1,053 of 1,249 placed doors unlocked 05:00 to 21:00.
- Clock: 15 x real time, a day in 96 min (R, I; a developer's comment beside the setting); night 21:18 to 04:42, 2.6 h fade. Weather: 31 profiles a level, 15 weighted (weights sum 5.1), rain chance 0.3 to 1.0; rain-capable about 35% of weighted draws, about 25% weighted by rain chance (M, I). Dirt 100% after 35 km at full speed or about 7.9 h of work; 86 kinds of time skip; sleep needs 1 h and 30% health.
Mafia (lead, from game files): no heat, wanted level or fine; 11 carabinieri class names (N); 199 shop items (98 free; 105 unlock at story chapter, 41 free ride, 17 challenges; 27 edition items no unlock); priced medians outfits 500, weapons 1,000, vehicles 1,500, horses 200, top 8,000; 15 main checkpoint tables; nine save slots in five files; failure 3 s screen then checkpoint; out-of-bounds fails mission after 15 s; 12 folders carry 65 custom mission scripts; 103 time-of-day presets by name; 4 phases.
LEDGER (own): heat fades on a 96 h half-life (144 h while Ellis in town); C# day is 12 real minutes.
Public wiki (stands as read): Warhorse wiki KM-A-12, 20, 21, 27, 30, 32 to 34, 84, 89, 90 (only states saved; effects rebuilt, KM-A-30).
Review: about 60 numbers, 26 re-measured: pass with fixes, all applied.

### c. Open blind spots (verbatim)

- **Kingdom Come II's code:** the barter formula, cash refills, saving rules in play, the decay rates' time unit, weather choice and rain length. **Its data:** which multiplier is the player's; lesson, horse, barber and bath prices.
- **Mafia:** loot sums, checkpoint counts and presets, names only: not exported, as the F: drive filled on 28 October.
- **Shown only in play:** what follows a game over; Mafia's shop in use. No recordings (25 October).

### d. Twenty basics

None mentioned.

---

## Study 12: Tech and budgets (path: production/research/aaa-reference/studies/12-tech-budgets.md; dated 25 October 2026)

Method: Mafia (Unreal 5.4) and KCD2 (CryEngine) configuration files. Where a meaning is read from a setting's name, the study says "by its name". Nothing here is play-measured.

### a. For LEDGER (verbatim, section "For LEDGER")

- **Adopt the significance rules for phase 5's town, and for Quay Street once it holds a crowd:**
  - people unseen for 3 s beyond 70 m freeze, never within 10 m;
  - a 3 ms animation budget, and a people-update budget near Kingdom Come II's 3.5 ms;
  - small things stop casting shadows at a fraction of their distance.
  - Our Unreal 5.8 has the Significance Manager and Animation Budget Allocator plugins these rest on (both in its Engine/Plugins/Runtime, checked on disk).
  - Phase 5's load test can borrow Kingdom Come II's idea: a test scene that fills the town with far more people than play needs.
- **Set the numbers LEDGER does not have yet, in phase 2's street budget:**
  - people in full detail (Kingdom Come II's 70 within 150 m is a ceiling far above a street's needs);
  - a draw distance;
  - a shadow-light budget per frame. Kingdom Come II's 8 a frame (6 in its performance mode) is a sane first cap for the street's lamp shadows (our window lamps now cast within 15 m).
- **Texture pool:** Mafia's memory thresholds put a 6 GB card at its texture level 1, a 1,500 MB pool; Kingdom Come II gives 4,096 MB at the same tier. Our 6 GB line for the whole game leaves room for either; 1.5 to 2 GB of textures is the comparable figure for our "High".
- **Lighting:** Mafia ships software Lumen with virtual shadow maps and TSR, the same family as LEDGER. Its 60 fps profile lowers shadows, view, textures and reflections, keeps GI, and gives the upscaler a 40 to 83% range. LEDGER draws at a fixed 55%; a dynamic range with headroom on the card is worth trying once the voice shares it (the accepted 1.7 ms of headroom).
- **Shop glass:** our windows reflect through Lumen's front layer (production/research/shop-glass-reflections). Mafia allows that only from reflection level 2, so any lower quality level of ours turns the shop windows flat; a lower level needs a stand-in reflection for glass. How Mafia makes its glass look is Study 5's.

### b. Key measured numbers

Mafia (lead, from game files, config read 25 October):
- Four quality levels (0 to 3) plus cinematic; PC ships at top, GI and reflections at 2; auto-detect memory thresholds 3, 7 and 15 GB.
- Low to top: world-partition loading ranges x0.8, 1, 1, 1.5; Nanite visible-cluster cap 1,048,576 to 2,000,000; texture pool 1,200, 1,500, 2,000, 2,000 MB; foliage reduction value 80, 60, 30, none (meaning inferred: foliage thinned by that percent).
- 60 fps console profile: shadows to 1, view distance and textures to 2, reflections to 1, GI unchanged; Nanite detail bias 1.5; TSR at 83% with dynamic resolution 40 to 83%; 10% spare on the card in the base console profile (inheritance not shown). Windows profile has dynamic resolution off.
- Nanite streaming pool 300 MB; virtual textures 323 MB; texture pool 2,000 MB at top; 158 named memory categories (20 top level), 14 CPU categories; 27,680 runtime cells; distant detail 20,202 files (12,274 packages, 7,928 bulk-data).
- Glass: front-layer reflections only from reflection level 2.
- Significance (by its names): animation 3 ms budget; civilians freeze when unseen 3 s and farther than 70 m, never within 10 m; hair shadows to half distance, props a quarter.
KCD2 (lead, from game files):
- Five levels (default 3). Low / default / top: view-distance ratio 50 / 100 / 180; detail ratio 10 / 25 / 300; sun cascades 4 / 5 / 5; shadow pool 2,048 / 4,096 / 16,384; lighting voxels 100 / 300 / 700; vegetation ratio 70 / 110 / 250; shadow-casting lights at most 10 / 16 / 32, budget 8 per frame.
- PS5 performance mode: 60 fps, 2560x1440 output, FSR 0.75, view ratio 80, light budget 6, no motion blur.
- Texture pool 4,096 MB at 6 GB, 5,120 at 8 GB, 8,192 at 12 GB; PS5 2,240; mesh stream pool 768 MB.
- Distant-detail tree (Kuttenberg region, 6,920 nodes): 8,000 m layer roots; median radii 33 m (depth 2), 181 m (depth 3), 45 m (depth 4, 5,063 nodes), 12 m (depth 5), 6 m (depth 6).
- At most 70 people in full detail within 150 m (80 within 180 to 220 m at top levels); people's update budget 3.5 ms (2.5 ms PS5 performance); performance-demanding area cuts local shadow distance 20 to 30%; performance-test quest with 1,000 to 2,500 people.
Public: Epic's Lumen page puts its top level at about 8 ms for GI and reflections at 1080p internal (30 fps console context). One public test (DSOGaming, 8 August 2025; RTX 4090 and RTX 5080; "1440p/Epic Settings", native or upscaled not stated): 42 to 51 fps as read; which card gave which figure not re-checked.
LEDGER (own): median 16.7 ms, worst 25 (33.3 ceiling); 6 GB card memory for the game alone; packaged walk draws at fixed 55% (r.ScreenPercentage=55); 3440x1440 is 2.39 times the pixels of 1080p; matching about 1080p internal means about 65% per axis (2,236 x 936).
Review: 34 numbers against extracts and 14 against config files: pass with fixes, all applied.

### c. Open blind spots (verbatim)

- Cell sizes and loading distances in metres (in Mafia's encrypted maps).
- Measured frame times in a street for either game (only one public test).
- Mafia's animation budget file (not in the files read).
- Shader counts for either game.

### d. Twenty basics

None mentioned.

---

## Study 13: Production pipeline (path: production/research/aaa-reference/studies/13-pipeline.md; dated 28 October 2026)

Method: file indexes and tables of both games beside LEDGER's repository, Unreal project and specs.

### a. For LEDGER (verbatim, section "For LEDGER")

1. **Adopt: a "tuning numbers" row in CATALOGUE.md's homes table.**
   - Home: production/specs/tuning/ (camera, input, interface, talk), staged with the game as stage_game_data.py requires.
   - A check fails the build when a spec's number is also a C++ constant.
   - It serves CLAUDE.md's "one home per fact"; Study 9's camera numbers go there first.
2. **Adopt: rows in order, each a rule over Tom's state and its numbers.** This is our design, after Mafia's tables, for Study 9's four camera rows; the same shape later suits prompts and the interface's visibility.
3. **Adopt: a naming rule for new Unreal assets of our own, with a check in CI.**
   - Epic's prefixes (T_, M_, MI_, SM_, SK_, AS_, AM_, BP_, DA_, DT_, NS_), then family, variant, _NN, and sizes in kit names.
   - Case is checked.
   - Imports (MetaHumans, Megascans, Epic's sample) keep their names in their own folders.
   - Rules alone have not held (CLAUDE.md); it serves the catalogue and RECIPE.md's scaling.
4. **Adapt: settings as data.** A settings spec (default, range, step, help text) read by LedgerSettings, in place of 22 hard-coded lines, before Study 10's width and scale come.
5. **Adapt: snake_case for new tools only;** renaming old ones would be churn.
6. **Ignore:** binary twins and GUID layer names (an engine's need), and Unreal data tables for now. JSON is diffable in git and readable by the C# Core; tables pay only when designers tune in the editor.

### b. Key measured numbers

Mafia (lead, from game files; counts from the package index and exports):
- 139,154 packages in one game folder plus plugins; 51 top folders, median depth 5, deepest 10.
- 91.7% of non-map assets carry a type prefix; 60.1% Epic's usual ones; 185 prefixes; 16 prefixes written two ways (MI 11,805, Mi 30).
- Variants: _a to _z 12,973; _NN 3,770; sizes such as 90x240cm 803.
- Tables: 3,064 (text 2,453, others 611, "most of them tuning" inferred); data assets 3,748; curves 149; 122 settings rows in 4 tables; game code 216 modules.
- By discipline: maps 45,898, animation 22,781, environment 19,396, audio 15,429, text 9,238, characters 8,629.
- Counts by type: textures 12,632; material instances 11,805; static meshes 10,637; animation sequences 7,204; montages 2,974; Blueprints 3,892; voice lines 25,360; input actions 166; mapping contexts 22.
- Difficulty is six tables (player, enemy, aim assist, wingman, loot, duels).
KCD2 (lead, from game files): 809,387 files, 111.85 GB, 89 own archives; dialog 280,344, textures 166,432, objects 127,804; 1,243 XML tables, 87,600 rows, 13 schemas; 98.7% snake_case; 35.1% of names have capitals; _diff on 42% of textures, _lodN on 22% of meshes; 14 texture suffixes cover 99.6%; 363 binary twins (I, caches); rpg_param 323 values in 93 families (sight radius 50, pickpocketing distance 2.4, attack charging cooldown 1.4); 3,562 of 3,562 layers named by GUID; 8 tables that do not parse are missing from the count.
LEDGER (own measurements, not leads): 2,565 Unreal assets in Content/Ledger (about 2,050 more in Epic's sample, MetaHuman and character folders not counted); 23% (582) carry a type prefix; no data tables or curves; 22 settings lines in C++; about 220 numeric constants in the game's C++, 356 in the C# Core (by declaration lines); production/specs 42 entries, 55 files, 18 JSON; 125 research folders, 127 tools, 32 production entries; tools mix underscores (41) and hyphens (65); camera arm 3.2 m, offsets 0.45 and 0.55 m, hide within 55 cm; reaches 3.5 and 2.2 m.
Review: pass with fixes, all applied.

### c. Open blind spots (verbatim)

- Mafia's source-side checks and folder rules do not ship. Asset-registry tags such as asset status and validation hint at them (N).
- How either studio tunes in the editor: no talk was read for it.
- Kingdom Come II: 8 tables that do not parse are missing from the row count.

### d. Twenty basics

None mentioned.

---

## Study 14: Combat and violence (path: production/research/aaa-reference/studies/14-combat.md; dated 28 October 2026)

Method: KCD2 own files (1.2, unpacked) and Warhorse's public wiki; Mafia from earlier exports and the package index only, because the F: drive filled and Mafia's combat folders (close-combat plug-in, abilities, camera, hit reactions, coordination) were never exported.

### a. For LEDGER (verbatim, section "For LEDGER" plus the following section "The first combat test and the source test", which carries the recommendation)

1. **Adopt B01's contact at 0.73 s:** KCD2's unarmed median is 0.75 s; Mafia's windows open earlier, at an action game's pace. (Readable; the first combat test.)
2. **Adapt the recovery:** free 0.4 s after a landed blow (KCD2); 0.8 s after a miss, by judgement. (A miss leaves you open.)
3. **Adapt the reactions:** by side, D03 front, left and right, D04 left and right. D03 keeps 0.6 s (KCD2's weak class); D04's 1.0 s matches the games' ordinary 1.06 to 1.18 s. Physics blended over authored clips, as the design says. (The animation question; risk R4.)
4. **Adapt Mafia's contact kit, our values:** a hit-stop per kind, a brief camera close-in (about 0.8 s), offsets by hit direction, a shake from the swing. Hit-pause stays 2 frames until a value is read. (Weight; no mode.)
5. **Adopt motion warping for lock-on:** slide to a set distance in the wind-up (Mafia 1 m, at most 2 m). Unreal 5.8 ships Motion Warping; Mafia's class is its own, so the settings are ours. (No lock-on.)
6. **Adopt the four sound layers,** our own or CC0 recordings (D26). (Weight.)
7. **Adopt KCD2's morale for other men's endings:** back off, run or yield at 0.2, moved mostly by events. (How fights end.)
8. **Keep the attacker offset:** KCD2 caps nothing; Mafia's attack points are an option against NPC mashing. (Two against one; the gaps stage.)
9. **Adapt Mafia's surface method:** each paired move in both facings, fitted by height. Seven places, each with a shove-into and a pin, make 14 designs, 28 with facings, against Mafia's 19 and 36 (I). (The street is a weapon.)
10. **Adopt KCD2's street numbers as first values:** watchers flee within 3 m; all flee once a weapon is out (rung 6); 2 to 8 react; a drawn weapon brings a warning, then arrest at 30 s. Police arrival: judgement. (The ladder; police arriving.)
11. **Adopt the grading:** an unarmed hit costs a third of an armed one in reputation, half in fines. (Rungs 5 and 7.)
12. **Adapt KCD2's beaten player for Tom:** robbed by chance, no game over. (Tom cannot die.)
13. **Ignore** lock-on, first person, Mafia's duel mode, finishing clips, skill-widened windows (Tom does not improve).
14. **For Jafar:** whether fists can kill (KCD2: no) is a violence line, his to rule; the source test's 6 clips change his design's 4.

Section "The first combat test and the source test" (verbatim): The first combat test needs **22 clips**, shared by both men: COMBAT.md's 19 (sections 5.2 and 5.6) with B01's and B02's recovery changed and D03, D04 made by side.

Clip table: Stance: A01 square up, A02 hold, A03 stand down. Blows: B01 strike lands (contact 0.73 s, free 0.4 s after), B02 misses (free 0.8 s after), C01 shove. Guard: E01 raise, E02 hold, E03 takes a blow. Reactions: D01 shoved, D02 shoved and falls, D03 struck steady x3 (front, left, right), D04 struck reeling x2 (left, right), D05 reeling, D06 knocked down, D07 down, D08 gets up. The wall: G01 shoved into a wall, G02 rebound.

**Recommended: the animation source test reaches 6 clips**, each within one frame of its timing: B01, C01, G01 and D03 in three sides. One hit reaction cannot show that a source makes a family; both games author reactions by side. The design says 4, so this waits for his yes.

Note: the source's item 9 reads "**Adapt Mafia's surface method:**" as shown; the study's numbering has 14 items.

### b. Key measured numbers

KCD2 (lead, from game files unless marked wiki; some derived by inference "I"):
- Unarmed swing start to contact: 0.75 s median, range 0.63 to 0.80; 10 hooks and 6 kicks (M). Hooks land at 0.70 s, kicks 0.78 s; swing live about 0.17 s before contact. Contact to end of blow about 0.4 s (I).
- Sword 0.70 s and blunt 0.93 s to contact; a miss 0.67 s clip (weapons only).
- Hit reaction: 1.27 s median of 132; to unarmed blows 1.18 s; weak class 0.6 s. By side: head 25, upper left 27, upper right 27, lower 53.
- 221 blow options; 1,683 paired-move options; 1 of 762 fragment records checks for an obstacle; 11 push-out-of-clinch options (unarmed 1.6 s, contact 0.73 s).
- Unarmed hit distance 1.0 m, reach 1.6 m; mace reach 2.1 m; stamina 26 a swing (R), regen 22 a second (wiki, public); health 100 (wiki, public); slashes, smashes, kicks cost 1.2 times stamina.
- 10 combat shouts; 294 impact sound triggers, 168 with a controller pulse; 129 combat deaths to ragdoll, 132 combat reactions not; ragdoll allowed on 85 of 91 major reactions and 101 paired hits.
- No cap, token or slot on attackers (M); at most 2 s between a man's blows (R; a maximum-delay field, unverified); +0.8 s gap per extra attacker (wiki, public).
- Morale (R): landed hit 0.02, ally's death 0.2, ally fleeing 0.1, outnumbered 0.05 to 0.2; surrender at morale 0.2 (kneels up to 550 s game time; spared, no yield or run for 30 s); flight 30 m off, 420 s.
- Escalation: drawn weapon brings guard warning, arrest after 30 s (nearest man within 2 m); arrest repeated every 6 s (plus or minus 2); four unanswered demands or one refusal bring force; anger bands 0.3, 0.6, 0.9. Fist fight: five fouls end it; opponent arms at health 30; quest knock-out 10 s.
- Beaten player robbed by chance (0.9, 0.5 or 0.1 by anger) of 5 to 15% of money.
- Street response: 10 witness reactions; watchers keep 3 m; computed cap 2 to 8 react; crime carries 10 m, alarm 25 m; reporter seeks guard within 150 m; extra guards at faction anger 0.8, checked each minute. Murder 20,000 and 7 days; unarmed hit costs 0.15 reputation, armed 0.45; reaches faction in about three hours (wiki, public). Assault fine 1,500 (tenths of a groschen), 5 days, kept 5 days; unarmed half.
Mafia (lead, from game files; many by names only):
- Unarmed hit window open 0.39 to 0.66 s (right), from 0.27 s (left); three-blow combo window opens 0.04 to 0.08 s. Hit reaction 1.06 s to blend-out; flinch 0.9 s. 4 directions by 7 body parts: 53 hits, 14 stuns, 6 flinches. Civilian shove reactions 2.8 to 3.9 s from 4 sides.
- 11 hit-stop curves (N, values not reached); melee camera held 0.8 s; 13 melee shakes (N); shake fires at 0.19 to 0.21 s in alert-stance swing.
- Motion warp up to 2 m, to 1 m off, in 0.42 to 0.52 s. Stamina pool 1.0, opponent regains 0.18 a second. Health ordinary man 5, brute 10, duel opponents 10 to 35. Duel opponents start with 1 to 5 attack points (maxima 6 to 16).
- 19 takedown designs, 13 fitted to cover (heights about 110 and 140 cm); 20 weapon curves (N); pain sounds in three sizes, 60 events each.
LEDGER now (own): B01 0.73 s, contact to end 0.60 s; B02 1.20 s after; D01 0.83 s, D03 0.60 s, D04 1.00 s; hit-pause 2 frames (judgement); camera nudge 1.5 degrees; reach 1.6 m; stamina swing 0.34, regen 0.09; health floor 2.8; 4 blows to put a man down (Combat.cs).
Review: about 45 numbers confirmed; pass with fixes, all applied.

### c. Open blind spots (verbatim)

- **Not reached (disk):** Mafia's hit-stop lengths, damage, contact moments, knife timings, parry and dodge windows, attack-point regeneration, brawl coordination, shake and physics values.
- **In code:** KCD2's damage formula, perfect-block window, how a fight becomes a crime.
- **Unverified:** KCD2's timing fields, the 2 s gap (a maximum-delay field), fine and jail units; 687 wiki-only constants; retail against 1.2.
- **Only in play:** hit-pause feel, Mafia's brawl spacing, police arrival; no recording or public source measured them (COMBAT.md).

### d. Twenty basics

None mentioned.

---

## Study 15: The crime toolkit (path: production/research/aaa-reference/studies/15-crime-toolkit.md; dated 28 October 2026)

Method: KCD2 data and Warhorse's public modding wiki, not code; Mafia as second opinion. Prices in groschen (gr).

### a. For LEDGER (verbatim, section "For LEDGER")

Every item below is a target for the crime layer when it is built (D56, stage 3), not work for now: new systems wait for a place in PLAN.md (29 September ruling).

**Buying, selling and fencing (the 23 September ruling):**
1. **Adopt: a hot mark on goods, fading by value and distance, while the memory never fades.** Hot to those who know it: owner, household, anyone told. Start from 0.015 h per tenth of its value, rescaled to LEDGER's 1990 prices; full in the theft's district, gone across town. The moat holds (memory permanent, remedies behavioural): the item cools, the owner never forgets; the crime itself stays known as the moat says, not 4 days. Serves the Coat and the ruling.
2. **Adapt: three answers at the counter:** buy at the honest rate; haggle harder once the goods are a little hot (Kingdom Come II: 0.1); refuse once plainly hot (0.5) or when the buyer knows the owner. Plus a fourth: he remembers, and may tell (Gossip). Serves D24 (trade must not look broken) and D25.
3. **Adapt: the fence is a person,** which Kingdom Come II lacks. The pawnbroker (Empire's fencing line already needs the pawnshop) buys hot goods at 0.4 of an honest sale to start, pays only what is in his drawer (Purses), and becomes a second person who knows, with his nerve and loyalty: D56's rule that the accomplice is the risk. 0.4 is Kingdom Come II's figure; the 1990 rate is owed to LEDGER's own research.
4. **Buying:** shops with opening hours from their people and doors, finite cash and a weekly restock (Study 11).

**The crime layer:**
5. **Adopt: privacy by place and hour.** Each room on Quay Street gets a label (private, personal, semi-public, forbidden) and a night rule; Access already gates rooms by hour and has a person say the refusal. Serves Access, phase 3's prompts and P4.
6. **Adopt: the warning counter as the refusal's escalation:** warn, warn again, call someone or act; a tick every few seconds, faster at night and with a weapon, under half a minute at worst; semi-public places warn but never escalate. **Adapt** the 2-hour memory: the counter resets, the sighting is kept for good (the moat). Serves the 23 September ruling on deeds seen, and D25.
7. **Adapt locks:** one key among several (Access: nothing is simply locked), forced at a cost: noise, a door that shows it for a day, a crime. No lockpicking minigame (D24's spend rule).
8. **Adopt the search's reasons, not its chance roll:** a search follows suspicion, never chance (Coat); a stranger and an angry or unfriendly officer feed it. Refusing is not an offence in LEDGER, but people see it (Coat); hot goods found are kept as evidence, as Custody keeps the coat.
9. **Ignore** the fines, pillory, beating, branding, jail days and execution: in 1990 an arrest means hours, a caution, or a charge and bail (Custody, from LEDGER's research), and canon's endings hold (D58).
10. **Ignore** reputation numbers (D33, D34): a talked-away charge costs that the person remembers.

**The owed verbs (D56):**
- **Verb 4, lean on a witness:** in neither game. LEDGER's rulings already let a witness be talked round or threatened (1 and 3 October); Kingdom Come II's nearest, a victim paid to settle privately, shows the bought retraction's simplest form.
- **Verb 5, move or hide a body:** Kingdom Come II carries bodies (Mafia has carry-body tags, N); an undiscovered one vanishes after an hour; a missing-person record (not a crime) exists. **Ignore** the vanishing (a killing is remembered forever; a body never fades in Gossip). **Adopt** the missing person: a resident who stops keeping his routine (CastDay) becomes a question the town asks, the gap between act and finding.
- **Verbs 1, 2, 3, 6, 7, 8:** in neither game (M); LEDGER's own design.

### b. Key measured numbers

KCD2 (lead, from game files unless marked; the study mixes R reads of data with I inferences; wiki items are public):
- Stolen mark: 0.015 h per tenth of a groschen (1 gr item 9 min; 10 gr 1.5 h; 100 gr 15 h; 1,000 gr 6.25 days; an item coefficient also enters in code). By distance: full within 600 m of the theft; 0.15 at 1,800 m; under 0.15 counts as clean. 16 of 5,184 items never fade (money, keys).
- Crime known: theft, pickpocketing, lockpicking 4 days; trespass 2; murder 7 (from Study 1's table). Stolen keys: lock changed after 3 days.
- Search: calm guard and stranger 0.5 a roll, a roll every 3 min, 90 min between searches (R, I). Refusing a search is a crime (10 gr, 1 day); takes every marked item on him, his horse and within 3 m.
- Selling marked goods: haggles harder from suspicion 0.1, refuses from 0.5; a first-game script pays 0.4 (whether the sequel runs it is unverified). Shop stock weighs 10 in the suspicion sum. Honest sale about 0.85 of value for rings and loot, 0.3 to 0.5 for gear (I). Merchant cash 35 to 1,500 gr. No fence identifiable (M).
- Trespass counter: every 6 to 9 s, + place severity 0 to 3, +1 night, +1 weapon drawn, +1 hostile, +1 angry watcher; personal and forbidden escalate past 12, camps past 25; semi-public and semi-personal stop at 3. Starts at 1 to 3; 20 s grace on leaving. Fastest escalation about 27 s (21 s with nervous watcher) (I). Counter memory 10 min; trespasser remembered 2 h.
- Labels: 2,910 labelled areas on the whole Kuttenberg map (private 1,176, semi-personal 585, personal 382, semi-public 171, forbidden 29, interior 586).
- Doors: 1,098 doors graded 1 to 5: 528 / 301 / 42 / 93 / 134 (grade 1 includes 170 without a model); chests with a known model 1,042: 3 / 250 / 448 / 282 / 59. Unlocked 07:30 to 19:30 by default, 05:00 to 21:00 on most placed doors; 44% start locked; door marker 24 h; door difficulty 0.17 to 0.94.
- Pickpocketing: within 2.4 m, charged 2 to 30 s; 0.0027 a degree off behind; 0.05 per earlier robbery; sleepers x 0.5; victim searches up to 4 hiding places within 40 m; anger +0.1, 0.15 or 0.2 for loss under 50, under 500, above.
- Fines: trespass 25; theft 50 + item's value; pickpocketing 55 (2 days); lockpicking 60 (3 days); assault 150; murder 2,000; victim class multiplier 0.5, 1, 2, 4 in parameters but 0.5, 1.5, 2, 6 in a script (which applies unknown). Talking away: 6 grades; from 2,000 gr cannot pass. Jail 1 to 7 days, then three stats x 0.6 for a fifth of the time served (days I).
- Reputation: witnesses median -0.1, murder -0.45; theft -0.25 with victim, -0.15 once reported; a talked-away charge costs 0.18. No fading parameter found.
Mafia (lead, from game files): people notice ten times faster in a trespass zone; three trespass and three confront levels then a drawn weapon; apprehender grab distances default 2.5 and 3 m (I); no theft, fence, fine or jail.
Review: about 45 numbers, 22 re-measured: pass with fixes, all applied.

### c. Open blind spots (verbatim)

- **The engines' code:** the lockpicking formula; how a merchant judges suspicion; whether the fence and 0.4 scripts run; how a witness chooses to arrest, settle or report; which class multipliers apply.
- **Not in the data:** who fences (the traffickers by name only); units of buff and jail durations; Trosky not counted. **Mafia:** lockpick and loot tables not exported, as the F: drive filled on 28 October.
- **Shown only in play,** such as how a search looks. No recordings (25 October).

### d. Twenty basics

None mentioned.

---

## Study 16: Jobs and story (path: production/research/aaa-reference/studies/16-jobs-story.md; dated 28 October 2026)

Method: KCD2 quest graphs, level sequences and English text; Mafia exported mission and cinematic files (the exports were removed from F: during the study, so Mafia numbers rest on derived tables in the session's raw notes); Warhorse's public wiki and public pages read in full; no recordings. Left unstudied under the content rule: one KCD2 side quest, two threads of a main quest, one Mafia step.

### a. For LEDGER (verbatim, section "For LEDGER", with its sub-blocks)

1. **Adopt: a job as a graph of saved states.** Study 11's four job and five step states; every change kept in the save data, effects rebuilt (SaveCodec does). Serves phase 3's "kept after restart", ROUTE.md section 3, D35.
2. **Adopt: failure that continues.** Every failure ends in a world state the town can talk about, never a game over; flags record "failed" as well as "done". The first ask already works so; make it every job's rule. Serves the outline's "no single beat can fail the run", D35, D58, RULINGS 12 Oct. **Ignore** Mafia's restart.
3. **Adapt: patience on people, not deadlines.** A window on the town's clock (KCD2 2 to 6 h; the ask's 22:00 to 01:00), then "stayed away"; a 10 s follow leash after which the leader waits, without KCD2's fail. Serves RULINGS 23 Sep (jobs).
4. **Adapt: the journal as the Ledger.** A line for every step state, failures included, and each finding; about 22 words, naming the person and the place by a landmark, which KCD2 leaves to its marker. Serves D12, phase 3's "useful office and ledger".
5. **Adapt: KCD2's guidance minus the marker.** The giver names place and landmark; anyone asked the way answers from authored facts (KCD2's directions talk); a leader may walk him; signs do the rest. Serves RULINGS 23 Sep, D20, D37, risk R6 (PLAYERS.md: players punish no direction).
6. **Adapt: sleeping steps and skip hooks.** Steps sleep while Tom is away and settle by the clock; each has a debug skip the AI tester can call. Serves RULINGS 3 Oct, phase 3.
7. **Adopt with numbers: few short cutscenes** (RULINGS 23 Sep). Proposed: each at most 60 s, skippable, a cut every 5 to 6 s; under 5% of the first hour watched (KCD2 a tenth, Mafia a quarter; Study 2's "well under 29%"). The producer decides.
8. **Ignore:** Mafia's fixed chapters and choiceless story (canon D24; the outline: beats fire on states); KCD2's markers (RULINGS 23 Sep) and faction numbers (D34).

**The job template (for the builder).**
- Job: id; giver (cast id); offered on a state, never the clock alone (the outline); state none, active, done or failed, with an outcome name (the ask's three).
- Each step: state (the five); the place, named with a landmark; who is there; a clock window and the person's patience; the act the town perceives (canon's seven slots); two or more outcomes where it decides; a Ledger line per state; two or more sources of direction (giver, a person asked, a sign, a note); a debug skip.
- Failure routes: late, caught, wrong man hurt, refused; each to a named outcome and a world state.
- Memory: flags the acts read; every state change kept in the save data; steps that sleep.
- Acceptance: every outcome reached in the Core's week like ROUTE.md section 4's rows; the AI tester reaches each from a fresh game with no marker.

**Targets for jobs without waypoints (proposed).** Every go-to step names its place by a landmark in the giver's line and the Ledger (KCD2's journal: about a quarter). Anyone who knows a destination says it when asked (RULINGS 25 Sep). The tester and P4's newcomers reach each place unaided within three minutes; misses are R6's evidence. No lateness fail inside a window of at least 2 h.

**Inputs for the three acts (proposed).**
- **Act I:** the ask, Ada's tea, Alison's question and Ellis's visit micro-sized (about 5 steps); the real book and the week's end side-sized (11 to 16). Act II reads their flags (ROUTE.md's table).
- **Act II:** each rival's attack a job whose failure continues; the sit-down one deciding step with three outcomes, like the large job's graded report.
- **Act III:** the inspection one step a morning, each with a day's window, graded by what the books hold. Scene candidates: the arrival and the books opening.

### b. Key measured numbers

KCD2 (lead, from game files unless marked public):
- 135 quests (32 main or untyped, 43 side, 45 micro, 15 activities); files per quest median 72 (micro 26, side 106, main 196). Main quest about 1.3 to 1.9 h in play (I, from CENSUS's 40 to 60 h over 32).
- Branches: 199 objectives with two or more completed outcomes, in 78 quests (58%). Optional steps 360 of 1,711 (21%). Cancelled-step entries at least 698 in 114 quests (84%).
- Lateness: patience 2 to 6 world hours; a 10 s follow leash; one 5 h deadline on errands.
- Markers: on 1,371 of 1,713 objective starts (80%). Journal: at least 4,464 step entries, median 22 words, p90 49; 84% use first-person words. Journal names a way in only 3 of 12 and 11 of 44 entries in two jobs (I).
- Cutscenes: 194 sequences (328 min); about 164 story scenes, 304 min, median 97 s, longest 342 s (duplicates removed, I); 13 videos, 18.6 min; main 138 (258 min), side 26 (46 min); about 5.3 h with videos (I). Median 16 camera cuts, median shot 6.3 s. Share watched about 8 to 11% of main story (I).
- Memory: 1,202 out ports (468 yes/no, 734 triggers), 1,158 read elsewhere; permanent deaths in 76 quests; 754 death watches in 119 quests; 2,258 wires; reputation to people in 34 quests, to factions in 30; crime nodes in 57 quests; 36 quests with sub-graphs named for what follows a fail; 74 quests with hibernation part; 2,364 developer skip nodes across all 135; 55 quests switch townspeople's directions talk off for some steps; guidance by walk-up talk 84 nodes in 41 quests, guided tours 94 in 24, notes and quest items 310 in 72.
- Three jobs (all M): small (stolen horse): 25 files, 5 objectives (0 optional), 4 dialogues, 2,669 spoken words, 9 journal entries, 309 words, 2 timers, 1 fail route; middle (captured brother): 98 files, 11 objectives (1 optional), 39 dialogues, 6,280 words, 36 journal entries, 1,092 words, 6 timers, 1 branch step, 7 fail routes, 12 failure entries, 4 out ports, one cutscene of 113 s with 25 cuts; large (scouting a fortress): 316 files, 27 objectives (18 optional), 158 dialogues, 24,625 words, 90 journal entries, 2,650 words (11 findings), 35 timers, 5 branch steps, 9 fail routes, 11 failure entries, 19 out ports, 17 cutscenes (lengths not on disk).
Mafia (lead, from game files; rests on derived tables in raw notes):
- 15 chapters; 42 free-ride challenges (2K says 24, public); 402 checkpoints, median 23 a chapter; 675 objective lines; 83 scripts; 3 of 675 optional; 5 fail reasons over 92 fail conditions (I); a chapter about 40 to 60 min (I, from CENSUS's 10 to 15 h over 15).
- 15 s out of bounds; companion 50 m and 10 s; 74 beat entries and 15 chapter blurbs, median 35 words; 143 in-engine scenes, 185 min, median 62 s, longest 297 s; median 14 cuts, median shot 4.7 s; share watched about 21 to 31% (I); go-to 151 lines, follow 64 (I); 33 of 141 triggers forbid skipping.
Public (stand as read): hardcore mode (patch 1.2.4, 15 Apr 2025) removes map position, compass and fast travel (Deep Silver; VGC); patches 1.4 and 1.5 added fails for a crime or killing; Warhorse's cinematic director's talk listing says five hours (Kino Art, 3 Oct 2025); skip implied not confirmed (Gamereactor, 16 Dec 2025); Shacknews 17 Sep 2024 and Destructoid 19 Sep 2024 on banishment and silence; wiki KM-A-30, 55, 74 to 76.
Review: fresh reviewer re-measured KCD2 counts and checked Mafia tables, public pages and every LEDGER tie: pass with fixes, all applied.

### c. Open blind spots (verbatim)

- **KCD2:** hardcore mode and quest markers; when the directions talk is on; the large job's 17 scene lengths; hibernation in code; job lengths in play.
- **Mafia:** objective instances sit in unexported level data (kinds, optional flags, timer seconds, stealth rules); the skip default; whether 30 video-flagged triggers play film.
- **Not reached:** TechRaptor, Deltia's Gaming, Escorenews, X, Fandom, Nexus, GameSpot, PCGamingWiki (refused; the first four on skipping, markers and an "almost six hours" figure); HowLongToBeat, Valnet sites, Polygon, Rock Paper Shotgun, Eurogamer (not tried, by their notices); any report of the 2025 Prague cinematics talk. Warhorse's KM-A-29 and 83 are empty.
- **LEDGER:** PLAN.md has phases 0 to 5, no phase 9; the acts come from game-design/story-outline-2026-09-28.md.

### d. Twenty basics

None mentioned.

---

## Study 17: Yakuza 0 and Shenmue, one small district and a long game (path: production/research/aaa-reference/studies/17-yakuza-shenmue.md; dated 31 October 2026, imported 2 November 2026)

Method: Jafar's own study ("Study C", his Claude doc "LEDGER Study 17: One small district, a long game", revision 5), imported read-only. Public sources only, no game files, so nothing here is a lead. His tags: U unverified, I inferred. Six details were cut from his text under canon's content rule (D18) and are marked [cut: content rule] in the source. The pairing of lessons to findings and to design documents is the importer's (unverified).

### a. For LEDGER (verbatim, section "For LEDGER"; italic marks removed)

His words: "Design inputs for the phases 6 to 10 plan, recorded in the design documents; no build work from them yet." Each lesson is his; the finding each rests on, and where it is now recorded, are the importer's pairing (importer, unverified).

| # | His lesson | Rests on (his finding above) | Recorded in |
|---|---|---|---|
| 1 | **Room enough.** The Hook plus the docks can carry 15 to 20 hours if packed densely. | Yakuza 0 about 30 h of story in two districts each about 8 min across (I); Shenmue 20 to 40 h in a few streets and a harbour (Findings, Length and District size). | game-design/agency-model.md |
| 2 | **An hour budget by activity,** as Suzuki planned his 45 hours (film, fighting, searching, moving and talking, training, other), set for LEDGER's 15 to 20. | Shenmue: Suzuki planned 45 h in 11 chapters (Findings, Length). | game-design/agency-model.md |
| 3 | **Side stories found on foot, no markers,** matching the ruling "jobs, no waypoints": about 25 to 40 (scaled from Yakuza; U), many light in tone against the main story. | Yakuza 0's side stories stumbled into on foot, no markers early on, most comic; about 100 (U) (Density; Side content). | game-design/agency-model.md |
| 4 | **Far more named residents** than the 30 regulars, each with a daily routine and one private secret. AI writes these cheaply; the cost is faces and clothes, so a variety kit for both is needed. Routines carry occupancy limits. | Shenmue's over 300 named characters, each with a routine and backstory, and the familiarity they build (Side content; People); the breakfast-shop jam fixed by a door and a limit (A schedule bug). | game-design/agency-model.md |
| 5 | **Never force waiting:** keep "wait a while"; appointments with a window, not a minute. | Shenmue's most criticised side: waiting for set hours with no skip, nightly trips home (The day and its tedium). | game-design/agency-model.md |
| 6 | **A legitimate docks job** as an early daily loop and cover, with a small daily competition. | Shenmue's part-time docks job, crates by forklift, forklift races each morning (The harbour job). | game-design/agency-model.md |
| 7 | **The street as a weapon:** bins, crates, signs, bicycles, walls, kerbs, shop windows, the harbour edge. Not Yakuza's frequent random fights. | Yakuza 0's street objects, finishers and alley moves; its frequent random fights (I) (Fighting with the street). | game-design/combat-design.md |
| 8 | **Empire as a management game on the street,** like Yakuza's real-estate business; **[cut: content rule]** (canon). | Yakuza 0's two business games, called the best part by reviewers (Density). | game-design/agency-model.md |
| 9 | **Density up and back, not out:** upstairs flats, back rooms, yards, alleys, cellars. The districts after release reuse the Hook's kit, as Kamurocho was reused. | Kamurocho reused for about 20 years; compact and dense stays memorable; density from going up (Reuse). | game-design/agency-model.md |
| 10 | **Progression (his ruling of 30 October):** Tom rises in position, never in numbers. He starts with nothing and nobody; by the end people step aside. | His ruling (RULINGS.md, What the game is, 30 October), not a finding of this study. | game-design/agency-model.md; combat-design.md |

### b. Key measured numbers (all public sources, none from game files; his tags kept)

- Yakuza 0 (2015): Tokyo and Osaka, Dec 1988 to Jan 1989; Kamurocho modelled on Kabukicho, about 0.36 km2; about 8 min to walk end to end (I; a walking video, How Big is the Map, 27 Jun 2020); story about 30 h (listed 20 to 40); about 100 side stories, 50 per lead (U); two business games.
- Shenmue (1999): Yokosuka 1986, Dobuita Street and the harbour; 20 to 40 h; Suzuki planned 45 h in 11 chapters (Game Developer, 19 Mar 2014); over 300 named characters, each with a routine and backstory (PC Gamer, 29 Aug 2018).
- Shenmue clock: 24-hour routines, home by 11:30 pm, appointments at set hours (Push Square, 20 Aug 2018); a schedule bug sent every warehouse worker to one shop for breakfast; fix was an automatic door and an entry limit.
- Sega reused most of Kamurocho for about 20 years (PC Gamer, 25 Mar 2025; 80.lv, 26 Mar 2025, GDC 2025 session).
- Hour split Suzuki used: film, fighting, searching, moving and talking, training, other (named, no figures given).
- Review status: no number was re-measured or re-read from its source in the import; no fresh review yet (importer, unverified).

### c. Not reached, and open (verbatim)

- **His:** HowLongToBeat and GameRant's small-maps list not reached (blocked). The side-story total (about 100) is not confirmed from a primary source.
- (importer, unverified) No number above was re-measured or re-read from its source in this import; the study has had no fresh review against its sources yet, which the research method asks of anything that becomes a design (CLAUDE.md, How the work is done).

### d. Twenty basics

None mentioned.
