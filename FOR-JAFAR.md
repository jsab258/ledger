# For Jafar

The overview first; then the day's summary, under 200 words. Earlier summaries are in git and in
production/archive/FOR-JAFAR-to-2026-10-04.md (and FOR-JAFAR-to-2026-09-24.md before that).

## Overview (Sunday 25 October, evening: your week's order)

**Your order of 25 October evening, to Monday 2 November 13:00** (production/orders/2026-10-25.md, every item and study with a status; 26 October: carrying on through the 13:00 reset, as you said).
- **Phase 1 is open, not closed.** It failed its first exit check on 22 October. Fresh reviewers re-run that check once the walk, the clothes and speech pass; phase 2 waits for it, and the shops already in the street stay.
- **Recorded:** your rulings (RULINGS.md and DECISIONS.md); the study's order for both weeks at the top of the study plan; the order ledger, seeded with everything still open from before (21 and 23 October's leftovers, the cloud week's four questions, the three shops not yet in the street, FINDINGS' twenty faults, your two clicks on the old archive). A new check fails any push where an item has no status or vanishes without being done or dropped.
- **Done:** the health check (production/audits/health-2026-10-25.md); your progress page now has the studies bar and the 33 carried items.

**The studies (16 of 16 done: this week's six, and the other ten pulled forward and finished on 28 October).**
- *Study 7, animation* (production/research/aaa-reference/studies/07-animation.md, passed its fresh review with fixes):
  - Neither game uses motion matching. Mafia walks on a layered state machine of single clips, Kingdom Come II on blend spaces. Both choose their starts, stops and turns rather than search for them: Kingdom Come II by distance, the stride's quarter and which leg.
  - Feet: Mafia traces the ground under each foot and locks a foot only in its duels; Kingdom Come II declares leg IK and a feet lock. The one perception figure found says viewers notice slides under about 2 cm, so our 3 cm bar is lenient.
  - For us: Epic's walk stays; its slides are in 134 of its 223 walking clips. If today's fixes fail by eye, stops and turns get chosen Kingdom Come II's way. Sitting can use the bench interaction already in Epic's sample. A first list of 14 street actions is drawn up, their sources still to check.
- *Study 6, characters and wardrobe* (studies/06-characters-wardrobe.md, passed its fresh review with fixes):
  - Both games dress people from a few shared bodies with skinned garments. Mafia: tops a median 22,000 triangles at full detail, trousers 9,600, four levels of detail. Kingdom Come II: one body per sex, 10 clothing layers.
  - Variety comes from material, not mesh: one layered material gives each garment 4 to 15 colourways, with grime and blood as values. Only hems, skirts and coat tails move; Mafia's crowd wears no cloth at all.
  - For us: Tom's jacket about 20,000 triangles, trousers about 9,000, 2048 textures, skinned, tails on a short bone chain. One base body per sex for the crowd. Mafia's own makers name Marvelous Designer.
- *Study 12, tech and budgets* (studies/12-tech-budgets.md, passed its fresh review with fixes):
  - Mafia runs the same lighting family as ours (software Lumen, virtual shadows, TSR); for 60 fps it lowers shadows, view, textures and reflections, keeps GI, and lets the picture size float between 40 and 83%.
  - Dense towns hold their frame by slowing what doesn't matter: Mafia freezes people unseen beyond 70 m and gives animation 3 ms; Kingdom Come II keeps 70 people in full detail within 150 m and budgets 8 shadow-casting lights a frame.
  - For us: those rules for phase 5's town; a shadow-light budget for the street's lamps; and our shop windows' reflections switch off below Mafia's reflection level 2, so a lower setting of ours needs a stand-in for glass.
- *Study 4, street and world building* (studies/04-street-world.md, passed its fresh review with fixes):
  - Mafia's dressed street: 14.7 m wide, 4.9 real props per 10 m (17 with ground dressing), all of it where the mission walks; its neighbours are nearly bare. Kingdom Come II's market street: 6 to 13 m wide, median 9.9.
  - Mafia builds streets from kit (433 meshes, each used about 78 times; one street, 2 house families) and keeps one-off buildings for its hero town; fake rooms behind windows are rare.
  - For us: Quay Street's 10.25 m is right. New checks for phase 2: at least 5 props per 10 m from a fixed list, kit reuse per street, every street view ending on a building.
- *Study 5, visuals* (studies/05-visuals.md, passed its fresh review with fixes):
  - Mafia's lamps are two lights each (a spot for the pool, a tiny bulb light), with light profiles and a little fog glow; its night is lit by contrast between lamp and dark, not by bright lamps.
  - Wet streets: one wetness value sets roughness 0.1 to 0.2, and puddles are decals; wear is mostly leak stains under sills and grime at wall bases.
  - For us: our shop glass stays as it is (our own research beats theirs here); windows get shaded frames first, fake rooms only higher up; lamps rebuilt Mafia's way.
- *Study 1, NPC life and AI* (studies/01-npc-life.md, passed its fresh review with fixes):
  - Kingdom Come II simulates its town: 1,354 people with homes, beds and working days; a crime becomes information a witness runs to a guard or a friend, kept 1 to 7 days. Mafia only stages people looping in place, and forgets.
  - LEDGER is already built the simulated way, with something both lack: who told whom, and talk that weakens as it travels.
  - For us: crime memory that lasts by kind (1 to 7 days); show a witness walking to tell someone; benches and beds as places in the routine; spreading only where people meet, as canon says.
- *Study 14, combat and violence* (studies/14-combat.md, passed its fresh review with fixes):
  - Kingdom Come II times every blow in its data: an unarmed blow lands about 0.75 s into the swing, which confirms our draft's 0.73 s. A fight ends by flight or surrender when morale falls to 0.2; the town warns, flees, reports and fines in set numbers (assault 1,500 and 5 days; unarmed costs half). Mafia gives the feel of contact: the body slides in to meet the target instead of locking on, a short freeze per kind of blow, a 0.8 s close-in of the camera, layered sounds, and paired moves against walls by height.
  - For us: the strike timing stays; recovery after a landed blow drops to 0.4 s; hit reactions made by side; the first fight test needs 22 animations; about 14 paired moves against walls, doorways and railings for the street.
  - Two questions for your next page: should fists be able to kill (Kingdom Come II says no)? Should the animation source test check 6 moves, not the design's 4 (I recommend 6)? Not reached: Mafia's combat files (drive F full).
- *Study 2, the first 30 minutes* (studies/02-first-30-minutes.md, passed its fresh review with fixes; from the games' files, no recording, so every minute is an estimate):
  - Both games fill their first half hour: something new about every three minutes, a fifth to two-fifths of it watched, one route, and no consequence the player caused. First control at 3.5 minutes (Kingdom Come II) and 1.4 (Mafia); about 3 saves in 30 minutes against about 20.
  - Mafia teaches each control when it is needed and saves every minute or two; Kingdom Come II shows a hint only when the player hesitates.
  - For us: hints on hesitation rather than by the clock, the screen revealed piece by piece, an autosave after every deed, a nudge after a minute idle. LEDGER's own last measure had 11 empty minutes of 30.
- *Study 3, dialogue and barks* (studies/03-dialogue-barks.md, passed its fresh review with fixes):
  - Kingdom Come II has about 138,000 written lines, a third said in the street; each crowd line recorded by four or five voices; how people greet him depends on his reputation, their anger, his renown and how he looks. Mafia's street is thin: 14 crowd voices, 2 or 3 lines per situation. Street lines run about 7 words, conversation 12; Kingdom Come II waits a median 32 s between street lines.
  - For us: our street lines already vary more than either game's (491 shared, 217 own, a 45 s floor). What is missing is situations: greeting Tom by how people see him and how he looks, bumping into people, neighbours greeting each other, talking to oneself at work, rain.
  - Its targets (about 30 own lines for each future regular, at least 6 lines per crowd situation, waits street-wide and per person) are phase 5 proposals for a later page: your 3 October ruling keeps the talk work closed until then.
- *Study 16, jobs and story* (studies/16-jobs-story.md, passed its fresh review with fixes):
  - Kingdom Come II builds each of its 135 jobs from saved steps, and failing one becomes part of the story (failure entries in 114 jobs); Mafia runs one straight line of 15 chapters and sends you back to the last of 402 checkpoints, no choice saved. Story scenes: a median 97 s against 62 s.
  - Kingdom Come II is not marker-free after all: 8 in 10 of its steps show a marker. So our jobs must say "where" in words: the giver's line, the Ledger, anyone asked on the street.
  - For the builder: a job template; every place named by a landmark and reached unaided within three minutes; cutscenes under a minute. Your question for the next page: may a job ever mark your paper map?
- *Study 8, sound* (studies/08-sound.md, passed its fresh review with fixes):
  - Both games make a street from a few quiet background loops, small sounds scattered around you that thin out at night, and fixed sources (windows, doors, bells, water), each heard within a set distance. Mafia's quiet street holds 0 to 3 distant voices at once through the day; footsteps 8 to 30 takes per set; Kingdom Come II's most-used music playlist is silence.
  - Our Quay Street has the loops; it lacks the scattered sounds, the echo of doorways and rooms, and dawn and evening. A layer-by-layer plan with distances and loudness is ready for the street's sound proof (P13).
  - Neither game's balance of voices, music and noise could be read: it is inside their sound banks, and there are no recordings.
- *Study 9, camera and controls* (studies/09-camera-controls.md, passed its fresh review with fixes):
  - Mafia's camera is close: an 82 degree lens 1.65 m behind a point 1.25 m up; it closes in for town walking, low rooms and talk, and a talk places the player 1.5 m from the speaker. Interaction reach 2.5 m (2.0 for talk) within a 60 degree cone.
  - Tom's camera hangs 3.2 m back with a 90 degree lens and has no talk framing.
  - For your next page: Tom's camera framing and lens (Mafia's recommended), shown in the game first.
- *Study 10, interface* (studies/10-interface.md, passed its fresh review with fixes):
  - Our subtitles are nearly twice Mafia's default size (39 against about 21 units), so ours stay; Mafia has 122 settings and 17 switches for what the screen shows.
  - Proposed: a choice of screen width (the corners, or 16:9 in the middle) with a 0.8, 1 or 1.2 scale; switches for prompts, hints and street chatter; prompts chosen by facing rather than distance.
  - For your next page: the width choice (the corners by default recommended).
- *Study 13, production pipeline* (studies/13-pipeline.md, passed its fresh review with fixes):
  - Both games keep their tuning in tables (Mafia 611 data tables and 3,748 data assets; Kingdom Come II 1,243 tables, 87,600 rows); 92% of Mafia's assets carry a type prefix in their names, 23% of ours.
  - Ours is half in specs, half in C++ constants.
  - Proposed: a tuning row in the catalogue, a naming rule for new Unreal assets with a check, settings as data.
- *Study 11, systems* (studies/11-systems.md, passed its fresh review with fixes):
  - Kingdom Come II has no wanted meter: guards' anger acts 12 hours late and fades in about a day and a half. Shops hold 35 to 1,500 coins and restock weekly; 686 quest save points.
  - For us: save at every job step but never refuse a save; shops run short of cash and restock weekly (we have this); rain drawn from weighted weather types for the weather proof.
  - A constable's beat before Ellis comes would be a new system, so it waits for a place in the plan.
- *Study 15, the crime toolkit* (studies/15-crime-toolkit.md, passed its fresh review with fixes):
  - Stolen goods stay marked for 9 minutes (cheap) to 6 days (a treasure), and less far from the theft. Rooms are private by the hour; a watcher warns, then acts within about half a minute. A search: an even chance every 3 minutes, 90 minutes apart.
  - For us: the hot mark, privacy by the hour and the warning count; the pawnbroker as the fence, paying 0.4 of the value to start. Pillory, branding and jail left out: in 1990 an arrest costs hours.
  - Kingdom Come II has no findable fence in its files; Mafia has no theft, fence, fine or jail.

**Your items (28 October, midday).**
- *The walk (item 2):* done on 27 October (15 of 15 packaged). Last night's walk made 13 of 15, both misses the tester's own steering (Ron missed by 20 cm, Darren gone home by the time it reached him). The tester now takes one more approach. The same walk found the talk box sending Tom's lines scrambled, its first letter at the end: fixed in the game, and the tester now checks every line.
- *Clothes (item 3):* Tom's sleeve ends are fixed in the drape. Marvelous wraps a sleeve round one straight guide per arm, and Tom's elbows bend, so his sleeves are now draped with the elbows straight, then bent back with his own skeleton, as the game moves clothes. His cuffs go round the wrist but are not clean (a lump at the seam, a little cloth through each wrist): set aside, your pick on today's page. Marvelous is closed.
- *Speech (item 4):* your three answers are in the game: the fast checker on, the wider name rule, and two copies of each check call (wrong refusals did not rise: 62 against 69 of 211). Measured together in 22 real turns: the first sentence ready at a median 2.1 s (3.1 s without the checker); no fact number ever said.
- *Mickey's office (item 5):* the back door is shut as the characters say, set in its frame, its knob and keyhole on its edge. Two of three fresh reviewers pass it; at night its panels read as dark slots, set aside after two tries (a third for your word on the next page). The grainy shadows: researched (Unreal's ordinary shadow blur cannot flicker, so Lumen's bounced light is the likeliest cause); the tests began and stopped when drive F filled.
- *Fallback work:* the port's hourly step now lives in the shared rules (174 new rows agree; two hidden faults now caught); its next piece, the deed's stories, is under way. Phase 5's research is written and reviewed. Studies 14, 2, 3, 11 and 15 are under way, read-only while drive F is full.
- *Drive F:* full since late morning (my helper's extracts); its delete is first on today's page.

<!-- retention -->Disk (10-22 04:32): C: 79.9 GB free, F: 48.4 GB free; grew most since 10-21 12:17: C:\actions-runner-ledger\_work\ledger +1.5 GB, F:\LedgerTools\uv\cache +1.4 GB, F:\LedgerTools\bpyenv\Lib +0.9 GB.

<!-- morning pictures: written by tools/morning_pictures.py -->

**Morning, Wednesday 28 October. Phase 1, Prove the bottlenecks. On: 3. Tom's outfit: zip jacket baked, skinned; cuffs' third try failed, his way next (RIB-CUFFS). Next: 4. Speech: cited facts, name rule in; checker built, off, his word (invented-claims/LOCAL-CHECKERS).**

| | Today, 28 Oct | Yesterday, 27 Oct |
|---|---|---|
| The hook camera by day | ![The hook camera by day, 2026-10-28](production/previews/morning-hook-day-2026-10-28.jpg) | ![The hook camera by day, 2026-10-27](production/previews/morning-hook-day-2026-10-27.jpg) |
| The reverse view | ![The reverse view, 2026-10-28](production/previews/morning-reverse-day-2026-10-28.jpg) | ![The reverse view, 2026-10-27](production/previews/morning-reverse-day-2026-10-27.jpg) |
| The street at night | ![The street at night, 2026-10-28](production/previews/morning-night-2026-10-28.jpg) | ![The street at night, 2026-10-27](production/previews/morning-night-2026-10-27.jpg) |

The Hook sheet, the bar they are held to: ![The Hook sheet](production/previews/hook-sheet-2026-10-05.jpg)

No decision asked: these are for watching the street change.

<!-- /morning pictures -->

**Your week's order, where it stands (23 October, 14:55; the 22 October overview is in git).**
- *1 to 4.* Done 21 October: health check, branches home, your rules and combat doc, the editor connection.
- *5, the cloud's pieces.* Done: the lamp and every shop whose design passed, each through the game's gate (fresh reviewers, one per view). The launderette's, the fish market's, Mickey's and the empty unit's designs failed their own reviews, so they come next as new work:
  - Lamp post C stands at the four lamp spots, stained: run-off and lime from its arm, rust at its door plate, algae at its foot.
  - **Rita's front** (the shops' sample, which you kept): her night light and her wear passed every view.
  - **The ironmonger's** (no. 16): the shop passed all eight views, and its wear too.
  - **The newsagent's** (no. 18): the shop and its wear passed all ten views. Its box sign now lights after dark.
  - **The tea rooms** (no. 14): the shop passed all ten views after eight rounds of night fixes, and its wear too. Every bay of the west row now has its designed front.
  - **The grocer's** (no. 11, on the parade): the shop and its wear passed all ten views in ten rounds. Fixed on the way: its design's toy tomatoes (now real onions), a grey glass sign, a floating roll, a cut-off letter, its opening hours hanging in the air in front of its recessed door, and tins striped under the night light.
    - Set aside after two tries: a faint grey smoke on the glass above the jar lids by day (listed; next, a frame capture to find its cause).
  - New fronts no longer take the street's old grime, which had landed on the newsagent's pale paint with hard edges; they carry their own. One rule now, checked by the build: each worn front states it (Rita's and the ironmonger's keep the old grime, as passed).
  - **The chandler's** (no. 13, at the parade's end): the shop and its wear, all ten views in nine rounds. Fixed on the way: its door's foot was black glass at night (now a solid aluminium panel), its CLOSED card unreadable (now faintly lit), and the walls seen through its door at a slant were black (now lit as the room). Its sou'westers read as hard hats, then pith helmets, so they left the window.
    - Set aside after two tries: one side lining glares near white at night from one slant. The cause is found (the design keeps that lining out of the window lamp's light); the fix is next.
  - **The west row's three fronts** are cut under their low eave: the tan strip on the slates is gone, all 26 views passed (production/previews/west-row-eaves-2026-10-23.jpg).
  - Listed:
    - deep shadows under the tea rooms' table at night (two tries at a fill light failed; set aside);
    - a faint smoke on shop glass over dark goods by day (the grocer's jars, two smears on the ironmonger's glass), cause not found;
    - the street lamp's orange glare on the pale newsagent;
    - the chandler's side lining at night (above).
  - Pictures: production/previews/ironmonger-2026-10-22.jpg, newsagent-2026-10-22.jpg, tea-rooms-2026-10-23.jpg, grocer-2026-10-23.jpg, chandler-2026-10-23.jpg.
- *6, frame rate.* Done: the packaged walk's worst frame 30.3 ms (it was 63), P1 closed by a fresh review (production/research/pre-production/P1-PACKAGED-2026-10-21.md).
- *7, the walk and the clothes.* The walk was rebuilt on Epic's sample with motion matching and measured on a set route. Starts, stops and turns slide 13 to 67 cm (the bar is 3), so it is set aside and off by default. Your current walk fails too: it slides on about half its steps, the right foot on every stride (production/research/sit-and-turn/TOM-MOTION-MATCHING-2026-10-22.md). Clothes: Epic's Fab items all load in 5.8, but the Techwear Outfit is modern sportswear and the Construction Presets are bare bodies, not clothes; none can dress the Hook sheet's people. Your answers: the walk's next go by Epic's MetaHuman route, begun 24 October; Marvelous Designer one month, paid by you when Tom's outfit is ready.
- *8, speech.* Done. **The Gemini test:** on the reply check, Gemini 3.5 Flash-Lite took 0.60 s at the median against Haiku's 0.97, but it let 3 invented details in 42 through where Haiku lets 1 (you kept Haiku); Gemini 3.8 Flash was the most accurate but slower, 1.8 s (production/research/voice-latency/GEMINI-CHECK-2026-10-22.md). **Pocket no longer stalls the walk:** run at lower priority, the walk's slowest 1% is 20.6 ms (it was 34) and its worst 47 ms (it was 175). The one frame left over the bar is a separate stall that the usual card voice shows too (87 ms today), so the frame-rate margin is thinner than P1's close said (listed). **The real path with Pocket:** 20 checked replies, with the game open, first sound heard at 2.41 s at the median, the best yet (3.25 s before) but over 2 s. The model's first checked sentence alone now takes 2.10 s, so the voice is no longer the bottleneck (about $0.15 of your measuring dollar).
- *9, closing phase 1.* Done. Four fresh reviewers, one for each exit, found that none passes (production/audits/phase1-exit/CLOSE-2026-10-22.md): Tom is still the stand-in body and slides; nobody sits in the game as played; first speech is 3.25 s at best; the frame bar held once and failed its repeat, and card memory with the voice is 7 to 9.9 GB against 6; there is no wear in the office or on Rita's front. They also caught four of my own records wrong, all corrected on 22 October. You held phase 2 on your page: next week goes on these failed capabilities first.

**Your order of 23 October afternoon, frame headroom, to Saturday 14:00 (24 October, 07:25).** Both parts are done: frame headroom as far as it goes, then the launderette.
- *The launderette* (no. 9, east parade): all ten views passed in five rounds (production/audits/gate-launderette/GATE.md; picture production/previews/launderette-2026-10-24.jpg). Its design's three faults are fixed: the towels; the washing, now made by cloth simulation; and a real firm's name. Its front is worn, and it is dark at night with its sign lit. The gate also caught a flat side wall seen through the lobby's glass, now tiled like its room.
- *Card memory with the voice on the processor:* the game alone a median of 5.0 GB, peaks 5.9 GB walking, under the 6 GB line; with Pocket beside it, 5.2 GB in all (peaks 6.5). With the cast voice on the card the card in all peaks 7.4 to 8.7 GB.
- *The 87 ms frame:* fixed. It was 13 of the engine's own screen passes built on first use; a bundled pipeline cache now compiles them before play, and no capture misses a pipeline. With the driver's cache cleared, as on a first launch, a player waits about 75 s at the title once.
- *The 38 ms frame with the voice:* partly. In half the walks the engine's first garbage collection, a minute after loading, cost one frame 31 to 50 ms; it is now collected behind the title, and walks with no voice hold every frame under 33.3 ms (worst 24 to 27). With Pocket working beside the game one frame still runs 42 to 55 ms at the day schedule's moment, when people move and shadows switch: the processor is crowded. Set aside after two tries; next, a trace of that moment.
- *The card's spare time:* at night back to 2.7 ms (it fell to 0.1 when today's shops came in: their window lamps' shadows); those lamps now cast only from their own shop and only within 15 m, which fresh reviewers passed on all four night street cameras. By day 1.7 to 1.8 ms against the plan's 2.5. The measure now sets the picture level (2.1 ms of the old "loss" was the Highest level).

**Your order of 24 October, the walk by Epic's MetaHuman route, to Saturday 18:00 (24 October, 11:49).** Built, measured, set aside on the bar after two tries, then judged by eye (production/research/sit-and-turn/METAHUMAN-ROUTE-2026-10-24.md, checked by two fresh reviewers).
- *How it works:* the sample's own character, unchanged and unseen, does the moving; Tom wears his MetaHuman (L1) over it through Epic's own retargeter, as the sample dresses its MetaHuman. Behind a switch, off by default; the packaged game builds and runs with the sample's parts in it (15 ms a frame, 5.5 GB on the card).
- *By eye:* ordinary steps hold their feet within 1.5 cm. But at about five moments a planted foot slides 10 to 15 cm: a stop where the front foot glides back flat about 13 cm (the one you might notice; picture below, the foot nearest the camera), a pivot, two turns from standing, a landing. The walk he has slides up to 50 cm.
- *Tried and failed (each shown to have taken):* the sample's own alternatives, and its foot lock held through each step.
- *Found on the way:* my height measure also counted swinging feet passing low as slides; a second reading from the animation's own marks passes (2.7 cm) but misses the real slides, so it is not taken. Nobody in the field publishes a pass mark; they judge by eye, so the worst steps are now judged in pictures.
- *Found since:* the slides are in the sample's own animation clips: Epic's foot lock holds each planted foot within half a centimetre, but some clips move a foot along the floor while marking it as lifting (the stop's glide is in Epic's own walk-stop clips: a flat foot travels 7 to 10 cm in the animation data itself). *Next go:* measure those clips, then choose between a stricter lock, leaving the sliding clips out, or a lock on Tom's own body.

![The stop: Tom's front foot glides back about 13 cm after he has stopped (side view, ten pictures a second)](production/previews/walk-stop-glide-2026-10-24.jpg)

**Your short job of 25 October.**
- *Disk:* Mafia: The Old Country is in C:/Games (49 GB), beside KCD2 (82 GB). C: has 209 GB free against its 40 floor, F: 31 against 20, so nothing was deleted.
- *The AAA study:* your plan is imported word for word (production/research/aaa-reference/STUDY-PLAN.md), and your amendment on Mafia's key is in the rulings and the legal file, with your word that you own both games.
  - *KCD2:* all 99 archives listed; its readable data unpacked to F: (31,150 files: tables, scripts, both regions' layers, English text). Schedules, crime and reputation each live in readable tables and scripts: Kuttenberg's schedule table alone holds 64,529 entries; there are 30 crimes, 308 crime behaviour trees and 203 reputation changes. Warhorse's official tools are not set up: they install only through a Steam account that owns the game, which I don't sign in to, and their licence covers individuals making mods only, "Companies are not entitled to use the Modding Tools". Their public wiki, which needs no account, documents where each system lives, and was read instead.
  - *Mafia:* **the published key was found** on a second search, in a public forum post of August 2025 (source in your study plan), and it opens the files. The first index now names all 139,791 packages and the sound files beside them: 45,898 map pieces, 22,781 animations, 19,396 environment pieces, 8,629 character assets, 595 AI assets. The game's 216 code modules are named too. The file viewer (FModel) runs on Microsoft's .NET 10 runtime on F: and, with the mappings file from TheNaeem's archive, opens every kind of package tried: data tables, animations and montages, a material instance, static and skeletal meshes, and an AI state tree. The file is from the game's December update and the installed game is newer, but it covers all the game's own gameplay classes.
  - *The coverage map:* 31 systems, each with where its logic lives in each game and which study covers it (production/research/aaa-reference/REFERENCE.md). Its open blind spots: Mafia's files are named but not yet read; how KCD2's code runs its tables; anything seen in play, until your recordings.

**The tester's walk (28 October, 02:14 to 02:25, the night's build with Epic's walk; production/playtest/nightly/2026-10-28.md).**
- The route ran 13 of 15 stages, the evening after a 15 of 15. It failed at Ron (never within reach, 3.7 m away) and at Darren (lost from sight): the tester's steering for Epic's walk is not yet reliable.
- Darren saw Rita's window broken; Rocco showed afterwards that he knew, as the night before.
- "That's all I know" to a newcomer's sixty first questions: 2 of 60 (the night before, 3).
- Replies first heard at 0.2 s: the stand-in's words with the real voice, not the real path.
- What broke the illusion:
  - everyone in the plain white base layer and barefoot; Ron and Sheila standing stiff;
  - a subtitle under Sheila's name reading "round here, Sheila?W": found this morning, the game's own fault (the talk box's cursor sat before a line's first letter, so Tom's words were sent scrambled); fixed in code, proved after the next build; the tester now fails a line not said as typed;
  - a man standing in the middle of the road, inside Tom.

**Risks, Monday's review (production/research/pre-production/6-RISKS.md).**
- R3, the street missing the bar: up, 25. The audit finds the visual method unproved: five proof-view steps were set aside, and Mickey's room failed three reviews. Phase 1's binding stop answers it.
- R1, empty or unchecked talk: level, 25. The bench's 23 to 25 empty answers have not been re-run; in play, 0 of 8 were empty (P4).
- R2, slow replies: level, 25. 7 October, the real path: first sound 4.6 s median. 21 October: on the processor the voice's own share is 0.13 s; the model's time is what remains (the Gemini test waits on your key).
- R10 and R7, the friends' evening: down, 9 and 10. It runs on your account with its $5 cap and no second account. The Shipping launch and the limits surviving a restart are proved in 0.6.
- R9, the way of working: level, 12. Orders now come weekly and there is one session, but that holds only if shown.

### Needs you

1. **Open Marvelous and click LEDGER bridge** (no page: a click on your PC). The cuff drape by the new garment skill (an elastic rib) is queued and starts on its own.
2. **Mickey's back door, a third try at its panels?** (next page) Chamfered mouldings with shaded corners, or panels sunk into the leaf. Yes (recommended), or leave them.
3. **Fists able to kill?** (next page; Study 14: Kingdom Come II says no) No (recommended), or yes.
4. **The animation source test at 6 moves, not the design's 4?** (next page) Yes (recommended), or 4.
5. **May a job ever mark your paper map?** (next page; Study 16) Words only; a pencil ring once someone has told Tom the place (recommended); or an optional marker, off by default.

No page yet for 2 to 5: they go on tomorrow's page, the interface's width (Study 10) after them. Your camera pick of 19:02 is recorded (between, feet in frame, the camera by situation). Today's page, answered at 12:35: https://claude.ai/artifact/TDpjTLydnfFBFfRPmavGpD

Your answers of 28 October morning are recorded and in the game: your new rule, the fallback order, the fast checker on, the wider rule, two copies (your condition met), Marvelous clicked. Your answers of 27 October are recorded: the cuffs' third try (failed), $4 more for speech tests (spent on the wording test and two copies), the bin emptied (the build re-run at 13:34), the checker's fourth try as you set it (failed; the small checker's cut-offs went to your page), no actor for Darren (Common Voice read, and failed), your evening order on invented sentences with its $20 ($17.86 spent), and tonight's page: the checker at the open cut-off (behind a switch until measured live), the cuffs by the sleeve first, Darren's voice kept, the cited instructions into the game.

### Road to worth playing (PLAN.md)

- **0. Recover control** (0.20W): done 6 October, passed by a fresh review with narrow points.
- **1. Prove the bottlenecks** (1.00W): Mickey's front office (passed 8 October), then a complete Tom and one speaker, the voice under two seconds, and P1 packaged (closed 21 October). If a sample fails within its ceiling, I report the failed capability.
- **2. Quay Street from proved families** (2.00W): the brick, the facades, the wet street's seam and the hill return here.
- **3. Thirty minutes that hold** (0.75W): N3 ported, the weather proof, P4's gaps.
- **4. The friends' candidate** (0.50W): on your own account, $5 an evening.
- **5. The first town:** after the pilot.
- **Friends:** eight to twelve weeks, if phase 1 passes; low confidence.

## Builder, Wednesday 28 October (evening)

**Failed:**
- Tom's jacket in the game, twice: first it hid his placeholder shorts (underwear), then it let Epic's white shirt through. Fixed by hiding only the shirt's sections.
- The jacket's street views: small holes in both cuffs, a step in the back hem, a ragged collar edge. Listed; the cuffs get rebuilt.
- Mafia's key sat in a helper's settings copy on drive C. Blanked.
- The night lamps' new bulbs save only 0.2 ms; the big saving was already made on 7 October.

**Done:**
- Your two orders and release rulings: in the ledger, RULINGS and CLAUDE.md, with a push check for "reference first". The progress page shows the docks, the story, late 2027.
- 145 study items in the ledger, reviewed.
- Hints on hesitation, talk to the person Tom faces, bulb lamps: in the packaged game.
- Seven researches, each reviewed: the garment pipeline (now a skill), a Mafia jacket, sitting, live talk, asset checks, wear and fog, the town kit.
- Sitting: the bench's clips measured; entries derived from them land on the seat to the centimetre, all ten.

**Act on:** open Marvelous and click LEDGER bridge (no page). Your camera choice: https://claude.ai/artifact/4e5QA1UFTEGLacF3Rm4wpE

## Builder, Wednesday 28 October (morning; late, my fault: due by 07:00)

**Failed:**
- Drive F filled with my helper's 26 GB of extracts; freed on your yes.
- Tom's cuffs: round his wrists now, but a lump at the seam and a little cloth through each wrist. Set aside; my third try broke your two-tries rule.
- The tester's walk: 13 of 15 (Ron just out of reach, Darren gone home), and a scrambled subtitle.
- Mickey's door at night: its panels read as dark slots. Set aside after two tries.

**Done:**
- Your rule, fallback order and three speech answers: in. Two copies wrongly refused 62 of 211 true sentences, one copy 69.
- Tom's sleeve ends: round to the wrist, draped with straight elbows and bent back.
- The door: shut, framed, brass on its edge; two of three views pass.
- The scrambled subtitle: the game's talk box; fixed, and the tester now checks it.
- The port: the town's hourly step in the shared rules; all 174 new rows agree.

**Act on:** nothing now: your page is answered (drive F freed, the cuffs by the bake, Tom dressed first). No page until tomorrow's.
