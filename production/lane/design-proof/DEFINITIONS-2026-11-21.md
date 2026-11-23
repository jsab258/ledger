# Definitions for the 44 undefined parts (design pass, run 2, written 20 to 21 November 2026)

What this file is. Run 1's coverage map left 44 rows UNDEFINED: needed, not written. Each is defined here in the design's own words, inside canon, his rulings and the game description (production/lane/ONE-SHOT-PROMPT.md, cited as "the description, section n"), with a standard a checker can pass or fail and the source that standard rests on. The synthesis and the parts tree stay read only; the giant prompt of about 1 December is to be rewritten from this file and the coverage map.

How each row's new status was set:
- MEASURED: the standard is pass or fail on a ruling, canon, the description's own numbers, a public guideline (the Xbox Accessibility Guidelines, XAG; the Game Accessibility Guidelines, GAG) or a design decision recorded here. Where it is a design decision, the row's basis says so: no reference game set it, and he may overturn it.
- PENDING: defined; a number in it waits on a named, dated study.
- UNMEASURED: defined; a number in it is judgement, and MEASUREMENTS-NEEDED.md now names how and when it is measured.
- OUT: left out by his ruling.
- OUTSIDE: shipping business, not a part a player meets, judged after the prototype like the other shipping rows.

Where GTA VI sets a higher bar than the row had (production/research/lane/gtavi/YARDSTICK.md, keys Y), the definition says "raised by Y..." No GTA VI story content is used anywhere. Mafia is never a reference. Mods are out by his ruling of 22:08, 20 November.

Point for his ruling (canon, rulings): a field-of-view setting (AX-03) would change the 86 degree ruling of 28 Oct; recommended yes, 75 to 100 with 86 the default; meanwhile not built.

Reviewed 21 Nov by a fresh Opus reviewer against canon, RULINGS and the description; its 22 points were fixed in this version (GD-08, RT-04, RT-09, RT-17, RT-16, RT-12, RT-03, GD-07, AX-02, 10.9, RT-19, RT-18, RT-02, AX-05, AX-07, GD-02, AX-10, AX-03).

Design decisions taken here (within canon and his rulings; recorded so he can overturn any): no achievements at release (10.7); photo mode from the pause menu only (6.8); a fail-safe that brings the sit-down after eight game weeks of Act II and the state-based roads to rung 2 (RT-04); Tom will not give an order that hurts anyone his line covers (RT-09); the War trigger (RT-12); the missed-rent ladder (RT-16); the three pots (RT-17); the Ledger and map do not stop the clock (RT-18).

---

## The interface and the screen

### 6.8 Photo mode
Definition. From the pause menu only, "Photograph" freezes the town and frees the camera within 10 m of Tom and never through a wall, body or car (the camera rule ER-CAM-02). All interface is hidden. The player can tilt, roll, change the lens between 24 and 85 mm, focus and exposure, and save a picture at the window's size. No posing, no filters that break the grey range, no stickers or text. The content rule holds: nothing the photo mode can show is anything the game could not show. Leaving it returns the frozen moment exactly.
Standard. (1) Reachable only from pause; (2) camera never more than 10 m from Tom and never inside geometry; (3) no interface element in a saved picture; (4) the town state after leaving equals the state before (save hash). 
Test. B (bot): 200 random photo-mode sessions with clip detector and before and after save hashes; S: a saved picture has no interface pixel.
Source. Ruling 23 Sep (optional presentation allowed); the camera rule; GTA V and RDR2 photo modes as the common PC expectation [I: widely known, not measured here].
Status: MEASURED (design decision, pass or fail).

### 8.2.1 Crash and bug reporting
Definition. When the game crashes, it writes a local report (build, time, last 200 log lines, hardware summary) and, on next launch, asks once: "LEDGER closed unexpectedly. Send the report? It holds no save, nothing you typed and no name." Yes, No, Always, Never. Default is No until the player chooses. A save is attached only when the player ticks it, per report. Typed talk text is never sent in a crash report. A "Report a problem" item in the pause menu writes the same report plus the player's own words.
Standard. (1) Nothing leaves the PC without a yes; (2) the report contains no typed talk and no save unless ticked; (3) the choice is remembered and changeable in Settings; (4) the game never crashes while writing its own report (a forced crash test).
Test. B: forced crashes x 50 with traffic capture; no outbound packet without consent; report contents checked against the list.
Source. UK GDPR and EU GDPR consent and data minimisation (Articles 5, 6, 7) as generally understood [I]; to be checked against the ICO's published guidance by the cloud privacy check (MEASUREMENTS-NEEDED B5).
Status: PENDING (cloud privacy check, by Tue 24 Nov).

### AX-01 Text and interface size, contrast and font
Definition. All game text (prompts, subtitles, the belief line, the Ledger, menus) is at least the description's 24 units (the prototype's unit, 24 px at 1080p) and scales from 100% to 200% in Settings without overlap or leaving the screen at any window size. Body text has a contrast of at least 4.5 to 1 against what is behind it (subtitles have an optional background box). One plain, readable face; no all-capitals body text.
Standard. XAG 101 (text display) and 102 (contrast): text at 200% never clipped; contrast at least 4.5 to 1 measured on 50 frames by day, night and rain.
Test. S: screenshots at 100, 150 and 200% at 1280x720, 1920x1080 and 3440x1440; contrast measured by script on the subtitle and prompt regions.
Source. XAG 101, 102 (sources/a11y-pc.json); the description, section 3 ("nothing under 24 units"); GTA VI's text size setting (Y1.9).
Status: MEASURED.

### AX-02 Subtitle options
Definition. Subtitles are on by default and offered before the first sound of the game (the first menu). Options: size (three steps), background box (off, half, full), speaker's name (on by default for named people), and street chatter subtitles (on or off, already in the description). A subtitle appears only with its audio and stays at least as long as the line plus 0.3 s.
Standard. GAG basic and XAG 104: the four options (size, background box, speaker's name, street chatter) present; the first screen offers them; no subtitle without its audio; every subtitle stays for its line plus 0.3 s.
Test. B: every line played in a 2-hour soak logged with its subtitle on and off times.
Source. GAG (subtitles), XAG 104; the description, section 3; ruling 23 Sep (subtitle only with its audio).
Status: MEASURED.

### AX-03 Motion and comfort settings
Definition. Each motion effect has its own switch: camera shake (the hit shake and the car's), head bob, motion blur, the brief camera close-in on a landed blow, and depth of field. The field of view stays at the ruled 86 degrees (ruling 28 Oct); a field-of-view setting, which the guidelines recommend, would change that ruling and is listed in DESIGN-COMPLETE.md as a point for his ruling, not built meanwhile. A "reduce flashing" switch dims muzzle flashes and lightning, beside the photosensitivity line the description already shows.
Standard. XAG 117 and GAG: every listed effect can be turned off alone; flashing reduced below three flashes a second when switched.
Test. S: each switch toggled and the frames checked; a flash-rate script on a gunshot clip with the switch on.
Source. XAG 117, GAG (motion); ruling 28 Oct (86 degree lens); GTA VI's settings list (Y1.9).
Status: MEASURED.

### AX-04 Audio options
Definition. Sliders for master, voices, effects, the street (ambience) and music, each 0 to 100; a mono switch; a "voices clear" switch that lifts voices over the street by 6 dB; and, raised by Y1.9, a "loud noise softening" switch that clips gunshots and explosions to the level of a door slam (GTA VI's tinnitus reduction in LEDGER's form). The sound-shown assist already in the description stays.
Standard. XAG 105: five sliders, mono, voices clear and loud noise softening present and each changes only its own thing.
Test. B: level meters on each bus with each slider at 0 and 100.
Source. XAG 105, GAG (audio); the description, section 3 (sound shown); Y1.9.
Status: MEASURED.

### AX-05 Input options beyond rebinding
Definition. Every action rebindable on keys and on the pad, with "reset to defaults" per device; mouse and stick sensitivity separately for X and Y; invert per axis per device; every hold has a toggle (the description has this); no action needs repeated pressing (mashing in fights is a choice the breath rule punishes, never a requirement); raised by Y1.9: an aim-assist strength in three steps once guns exist (off, light, strong; the dot stays optional and off by default), and a "hold becomes tap" switch for every hold.
Standard. XAG 107 (input): all items present; the game completes the first hour with every hold set to tap and on pad alone.
Test. B: the first-hour bot run with all toggles on, pad only; a rebind of every key with no conflict left unflagged.
Source. XAG 107; GAG; the description, section 3 (controls); Y1.9.
Status: MEASURED.

### AX-06 Menu usability
Definition. Menu targets are large and never move; Back always goes one level up and never quits; the focused item is always visible; Settings are reachable before play and from pause; every setting is remembered between sessions and survives an update; nothing destructive sits one press from Resume (already in the description).
Standard. XAG 112 to 115 checks pass on every menu screen.
Test. S: a menu walk by pad, keys and mouse, logging focus and Back on every screen; settings file compared before and after a restart.
Source. XAG 112 to 115; the description, section 3 (menus).
Status: MEASURED.

### AX-07 Save thumbnails, rotating autosaves, never losing the only save
Definition. At least eight manual slots, each with a picture, the game day and hour, the place and Tom's rung in words. Autosaves rotate through three; a save is written to a new file and swapped in only once complete, so a crash during a save never loses the last good one. Quitting saves. A crash loses at most the last deed.
Standard. (1) Eight manual slots with picture, day, hour, place; (2) three rotating autosaves; (3) power cut during save x 100: a good save always loads.
Test. SaveChaos style: kill the process at random points during 100 saves; every time a save loads and equals one of the last two good states.
Source. The description, section 3 (saving); ER-SAVE-01; PC players' expectation from the players study (bugs and broken saves punished).
Status: MEASURED.

### AX-08 Accessibility listed in game and on the store
Definition. An "Accessibility" page in Settings lists every assist and option with one plain line on what each does; the same list is on the store page.
Standard. GAG basic, XAG 121: every option present on both; none missing (a script compares the settings file's keys with the page).
Test. Script diff of settings keys against the page text.
Source. GAG, XAG 121.
Status: MEASURED.

### AX-09 Screen narration of menus
Definition. A "read menus aloud" switch speaks the focused menu item, its value and the Ledger's headings and lines through the system's speech voice; prompts in play can also be read aloud. Off by default; offered on the first menu.
Standard. XAG 106: every menu item and every Ledger line is spoken when focused with the switch on.
Test. B: a menu walk with speech events logged; any focused item without a speech event fails.
Source. XAG 106; Y1.9 (screen narration).
Status: MEASURED.

### AX-10 Pause and focus safety
Definition. When the window loses focus, the game pauses (Esc menu shown) unless the player turns this off; alt-tab and a change of window size never crash, never lose input and never change the town's state.
Standard. 100 alt-tabs and 50 window resizes in a soak: no crash, no stuck key, no town state change while paused (save hash).
Test. B: scripted focus loss and resize during walking, driving, a fight and talk.
Source. PC players' expectations (sources/a11y-pc.json, PC section); the description, section 3 (Esc pauses everywhere).
Status: MEASURED (design decision, pass or fail).

### AX-11 Never by colour alone
Definition. No information is carried by colour alone: the light cue is darkness at the frame's corners, the belief line has words, the seeing outline is a shape. Key objects (doors usable, the cab of the firm, a constable) are told apart by shape and light, never only hue. Raised by Y1.9: three colour-blind filters (red-green two ways, blue-yellow) are offered, though the design does not rely on them.
Standard. Every cue passes a check under simulated protanopia, deuteranopia and tritanopia: the meaning is still readable.
Test. S: 40 frames with cues, put through the three simulations; a fresh reviewer names each cue's meaning.
Source. XAG 103, GAG (colour); Y1.9.
Status: MEASURED.

---

## Shipping and support

### 10.7 Platform account, cloud saves and achievements
Definition. Steam first. Every save slot and the settings file sync through Steam Cloud; a clash shows both saves with their day, hour and place and lets the player pick. No achievements at release: a pop-up in play is a marker, and the vision has none (no meters, no rewards counted); this is a decision he can overturn. No account other than Steam's.
Standard. (1) Two PCs, same account: a save made on one loads on the other; (2) a forced clash shows both and loses neither; (3) no achievement or pop-up appears in play.
Test. Two-machine sync test x 10; clash test x 5.
Source. The description, section 3 (no meters); VISION (no stats or counts); Steamworks Cloud as commonly used [I].
Status: MEASURED (design decision).

### 10.9 Player support and community
Definition. "Report a problem" in the pause menu (with 8.2.1's consent), one support address in the menus and on the store page, and the Steam forum as the community place. Any live line can already be reported (section 34).
Standard. Every route present; a test report reaches the support inbox with its build and the player's words within 5 minutes.
Test. Ten test reports from the pause menu.
Source. The description, section 34 (line report); sources/a11y-pc.json (PC expectations).
Status: MEASURED (design decision).

### 10.11 Player data and privacy
Definition. Before the first talk, beside the AI notice, a short plain privacy note: what typed talk is sent to the talk service, how long it is kept, that no name or account detail is sent, and that offline play is possible with the written street. A privacy page in Settings repeats it and offers deletion of anything the game holds about the player off the PC.
Standard. (1) The note is shown before the first typed line; (2) offline mode plays the whole first hour; (3) the service's retention and the deletion route are as stated (checked against the service's terms).
Test. B: first-hour run offline; S: note present before first talk.
Source. UK GDPR and EU GDPR transparency and erasure (Articles 12, 13, 17) as generally understood [I]; the description, section 34 (AI notice); ruling 23 Sep (offline carries on).
Status: PENDING (cloud privacy check, by Tue 24 Nov).

### 10.12 Demo, price and wishlists
Definition. A store page with wishlists opens when the Unreal build has the first street frame he approves; a demo, if any, is the first evening only; the price is his money decision. None of this is a part a player meets in the design; it is shipping business like the store and rating rows already outside this proof.
Standard. None at this gate.
Source. CLAUDE.md (money is his); the shipping rows 10.1 to 10.5 already OUTSIDE.
Status: OUTSIDE (shipping business; price is his, later).

---

## The game's shape

### GD-01 Travel time across the playable map
Definition. The Hook is crossed end to end (ferry landing to the north road) on foot at a walk in a set number of real minutes and by car at ordinary speed in a set number; every go-to step is reachable unaided in 3 minutes (ER-JOB-01) and nothing to do is more than 30 real seconds away by day (section 40). Raised by Y4.1: the bar is density over size, so the crossing must be short and full rather than long.
Standard. Provisional bands until measured: on foot 3 to 5 real minutes, by car 60 to 100 s; to be replaced by the reference games' town crossings (KCD2's Kuttenberg, RDR2's Saint Denis, a GTA V district, GTA VI's Vice City streets as a fourth).
Test. B: timed crossings by the walk and drive bots on the prototype map.
Source. ER-JOB-01; the description, section 40; MEASUREMENTS-NEEDED A (travel time).
Status: PENDING (PC measuring, 23 to 28 Nov).

### GD-02 Density
Definition. Something to do or notice every so many seconds of street walking: a person with a word, a fare, a debt, a happening, a lit window with a life, a thing to touch. Raised by Y2.5 and Y4.1: distinct people in one busy view, and no street line repeated within an hour of play.
Standard. Things per street minute within the band the teardown's town pieces show (to come); at least 25 distinct people in the busiest view of the Hook at its busiest hour (a judgement figure, replaced by the footage pass's count of GTA VI's and KCD2's busiest views); no shared street line heard twice in one real hour (raised from the description's "a shared line once a week per street", which allowed repeats across streets).
Test. B: a one-hour walk logging every line and every meetable thing per minute.
Source. MEASUREMENTS-NEEDED A (density); Y2.5, Y4.1.
Status: PENDING (PC measuring, 23 to 28 Nov).

### GD-03 Jobs done out of order and sequence breaks
Definition. Every job is a set of step states (the description's job template), never a script with an order. A step met early (the key found before the job is offered), late (after the hour), skipped by another route (in through the yard instead of the door) or done by someone else (a crewman sent) counts as met. A job never waits on a step already made impossible: it moves to failed with a state the town can talk about, and control is never stuck.
Standard. For every job, the AI tester runs all orders of its steps it can reach plus one skip by each other route; no run ends stuck or waiting for something that cannot happen.
Test. B: permuted step runs on every authored job.
Source. The description, sections 14 and 3 (no game over, never stuck); the review studies (missions on rails punished in 5 of 8 games, STORY-PATTERNS rank 5).
Status: MEASURED (pass or fail).

### GD-04 A second playthrough
Definition. A replay that answers differently meets named differences: Sunday's three answers; the arrangement kept or ended (rivals a rung sooner); which rival notices first; the five debtors each paid another way; the fronts and men chosen; the endings, three with a better and a plainer turn each; and whatever branches the measured story keeps.
Standard. A replay with a different Sunday answer and a different first rival meets at least eight named differences a player can point to in its first five hours. The figure is judgement until checked against KCD2's and RDR2's published branch counts.
Test. Two bot playthroughs with opposite choices; a fresh reviewer lists the differences from both logs.
Source. The description, sections 36, 37, 39; MEASUREMENTS-NEEDED A (replay branch counts).
Status: UNMEASURED (figure by judgement; measured by the cloud branch count, by Wed 25 Nov).

### GD-05 Humour and a mix of tones
Definition. Canon's tone: grounded noir with dry British wit and seaside-postcard smut, sparingly, so the noir holds; never American satire. Every evening holds at least one light moment carried by a person (Darren, Pauline on the radio, a fare), and every act holds at least one scene written to be funny (the current bible's inspector ride-along is the model).
Standard. Humour is praised in 5 of 8 games' story reviews (6% of story sub-themes); a clash of tone is punished. Pass: each act has at least one comic scene and each evening at least one light moment; no comic scene sits inside a scene of death or grief.
Test. Story measure readers mark comic scenes per act on the summary; the bot logs light lines per evening.
Source. canon.md, Tone; STORY-PATTERNS-STEAM-2026-11-20 (rank 7 humour; tone clash a single mention).
Status: PENDING (story measure, by Sat 28 Nov, for the scene count per act).

### GD-06 Mods and community content
Definition. No mods at release.
Status: OUT (his ruling, 22:08, 20 Nov).

### GD-07 Economy over weeks
Definition. Money buys position, never numbers (the description, section 24). The curve: Act I, £23.50 and rent at £18 a week, a week of fares pays it, the debts at £156; Act II, what money buys rises with the rung (a third car, a driver's wage, men's cuts, a front's share, a bribe to a bought man, the decent jacket, the good overcoat, the doctor); Act III, money cannot buy the books clean. Sinks never run dry before Act III: at every act's end there is a named thing the player wants and cannot yet afford.
Standard. The players study punishes money with nothing to buy (GTA V and RDR2 late game). Pass: at each act's end, in both a greedy and a lazy bot playthrough, at least one named thing on the rung ladder he does not yet hold is still out of reach of his money; the curve's shape is set from the reference games' money over a playthrough.
Test. B: an economy bot playing greedy and lazy; the curve plotted against the rung ladder.
Source. The description, sections 24, 28, 31, 32; MEASUREMENTS-NEEDED A (money over a playthrough); PLAYERS-KCD2-GTAV-RDR2 complaints.
Status: PENDING (PC measuring, 23 to 28 Nov).

### GD-08 The catalogue of jobs and stories per act
Definition. Every job has a named giver, a place by landmark, an hour, three keys to every lock (the description, section 14: no job needs talk, a fight or a car to finish), and a return (somebody tells it back). Kinds: carries, collections, break-ins, lifts, tails, minding, fares with a wrinkle, sit-downs, and from Act II the eight sent verbs. Act II has no dead weeks (a rival rung, a firm change and a return every week).
Standard. Jobs per real hour and kinds per act inside the band the teardown and the reference games' mission counts show; no set piece twice in thirty minutes (section 14).
Test. A count of the authored catalogue per act against the band; the bot's job log for kind repeats.
Source. The description, sections 14, 37; MEASUREMENTS-NEEDED A (jobs per hour).
Status: PENDING (PC measuring, 23 to 28 Nov; the story measure for the story jobs).

---

## Red team 1 gaps

### RT-01 Act III morning grading
Definition (for the design's Act III; the story measure may reshape Act III, and then this is rewritten to its version). Each of the five mornings the inspector asks for one item. Each item is graded in three degrees, read from the books: holds (no week in that item over the wash limit of £10 plus 80% of real fares), thin (one or two weeks over by less than a quarter), falls (any week over by a quarter or more, or three weeks over at all). A thin grade colours the inspector's manner colder; a fall also withdraws the successor's offer (if made) and tells Sheila, who says so. The books open on the last day: the business survives if no item fell and at most two were thin.
Standard. Every morning's grade traces to named weeks of the book; the player's Tom's reading predicts the outcome (ER-END-02).
Test. B: seeded books with known over-limit weeks; grades and ending checked.
Source. The description, sections 26, 38, 39; DESIGN §16.
Status: PENDING (story measure, by Sat 28 Nov: Act III's shape; the rule above stands if Act III keeps the mornings).

### RT-02 Main-story beat content
Definition. Each of Act II's eight beats (the description, section 37) has a written scene: who, where, what is at stake, what the player can choose, what comes back. The old firm's hand-over names three things handed over (the landing, its men, its night custom); Mickey's real book holds the arrangements and debts Tom can take up (at least five new names); the envelopes of Act I's nights five and seven (section 36) carry what the measured story says; the collision is written for each pairing of a day appointment and a night job the state allows.
Standard. Every beat has its scene; every scene names at least one choice and one return; none needs a system the game lacks.
Test. Trace check: beat to scene to system (TRACE style), by a fresh reviewer.
Source. The description, sections 36 and 37; the story measure's bible (current version STORY-BIBLE-M1).
Status: PENDING (story measure, by Sat 28 Nov).

### RT-03 Job and mission catalogue after week one
Definition. As GD-08 for kinds and counts, plus places: the dock gate (Act II from rung 3: tax collected on his drivers, a man posted, smuggled loads seen), the Harbour Board's counter (an account, a clerk who sells times of shipments), customs (an officer who never reports, by trade; the bonded store, holding tobacco and boxed goods and never drink, as a place of risk).
Standard. Each place has at least two jobs and one person with a word; counts as GD-08.
Test. Catalogue count; bot visits each place and finds something to do within 30 s (section 40).
Source. The description, sections 14, 28, 29, 40; the story measure.
Status: PENDING (story measure and PC measuring, by Sat 28 Nov).

### RT-04 Act transitions and stall paths
Definition. Act II opens on its state, as the description has it: Sheila has her answer and the firm is his (rung 2). Every road reaches that state. "Take it over" gives it on Sunday; "wind it down" gives it on Sunday with the arrangement ended; "refuse to say" leaves Sheila to read his deeds, and the firm becomes his on the first of these states: a third car, a first recruit, or the outfit's ask taken twice in the second week. Rung 3 is the rung table as written: five cars, a night desk, a first front, a first round and the cold-store contract, all held. Rung 4 likewise: fronts and rounds across the Hook (at least two of each) and men at the dock gate, the cold store and the landing. If no rival's ladder has reached its top rung by the end of the eighth game week of Act II (the description puts Act II at about seven), the rival highest on its ladder climbs its remaining rungs one a game day, each said to his face as the ladder requires, so Act II still ends at a sit-down and no player is stuck in Act II.
Standard. Every Sunday answer reaches rung 2 by a state; every Act II reaches a sit-down by about week eight without a rung skipped unseen; rung changes fire exactly on the table's conditions.
Test. B: three week-one bots (each answer) and a do-nothing Act II bot; the act, rung and ladder log checked.
Source. The description, sections 29 (ladder never skips a rung), 30 (Act II ends at a sit-down), 32 (the rung table), 36, 37 (opens on rung 2; beats on states); ER-CORE-04 (no dead end).
Status: MEASURED (design decision, pass or fail, built on the description's states).

### RT-05 The two rivals not met at Act II's end
Definition. The two rivals whose ladders did not reach the sit-down keep their rung into Act III and keep pressing (their pressure at that rung stays part of every week); neither is absorbed or defeated by the story alone. Act III's close names each: what they hold and what they call him.
Standard. After the sit-down, both other rivals' rungs are unchanged by it, their weekly pressure continues, and the close names both.
Test. B: an Act III run checking the other two ladders' state and pressure each day.
Source. The description, sections 29, 37, 39.
Status: MEASURED (design decision, pass or fail; the story fills the scenes).

### RT-06 Rival threat rung and counters
Definition. The threat rung is a named harm said to his face or shown on his property, never yet done to a person: the Widow's men put the office window in, or tell a driver he will not drive again; Agar's solicitor names a date for the licence hearing; Cammack's boys slash the tyres of car two on the rank. Property harm is repaired by people for money and a day (the glazier, the tyre man), and the street sees it. "Counter with what he knows" is spending a hook (RT-07) on the rival's man who made the move, or on the rival. The Fixer's truce holds one rival at its rung for two game weeks, once a game.
Standard. Each rival's threat rung shows one harm in its own style; every harm repairable; a counter needs a hook Tom holds; a truce holds exactly two game weeks.
Test. B: ladder runs to the threat rung for each rival; counter with and without a hook.
Source. The description, sections 29, 30.
Status: MEASURED (design decision).

### RT-07 Hooks and knowledge as leverage
Definition. A hook is a fact Tom holds (a Ledger "People" line he is sure of) about a person, which that person would not want told to a named other (his wife, his guv'nor, the police, a rival). Tom gets one by being told (Darren sells what he hears), by seeing it himself, or from Mickey's real book. Spending it is one line of talk: it buys a recruit (quick and brittle: that man's loyalty ceiling is lower and he breaks sooner), an answer to a pressure, or a counter at a sit-down. A hook is spent once: the person now knows Tom knows, and remembers it. A "guesses" line is no hook; using it as one is a bluff, which works only if the person believes it.
Standard. Hooks exist only from a perceived source; spent once; a hook recruit breaks sooner than a need recruit under the same pressure.
Test. B: recruit two men by each road and apply the same pressure; hook use logged.
Source. The description, sections 24 (Ledger certainty), 27, 29, 30.
Status: MEASURED (design decision).

### RT-08 Sending verbs in play
Definition. A send is given in talk with the man (or by the board's line for him): two inputs, the verb, then a target from the Ledger (a person or place Tom knows). The man does it on the next night his routine allows. Its outcome is decided by the same rules as Tom's own deeds: the man's nerve against the target's, the watchers there, light and noise. The player learns it the morning after from the man's own line and, later, from the town's version. Each send leaves a chain the town can trace, and the man knows.
Standard. Every send resolves within two game nights; its result runs the same perception and memory as a deed by Tom; nothing is shown at length.
Test. B: each of the eight verbs sent twenty times with seeds; outcomes traced to watchers.
Source. The description, section 27.
Status: MEASURED (design decision).

### RT-09 Tom's line against women, the over-sixties and the priest
Definition. If someone his line covers attacks him, Tom guards, slips and backs off; the strike input does nothing and he says so. In a fight that includes them, he can strike, shove or grab only the others; he does not grab a covered person even to take a weapon, and steps away instead. Tom will not give a send that hurts a person his line covers: the order is refused in his own words. A rival's men are not bound by his line.
Standard. Zero strikes, shoves or grabs by Tom on anyone covered, and zero sends that hurt one, in any fight, hold-up or send.
Test. B: seeded fights and sends including covered people; any such strike fails.
Source. The description, section 10 (Tom's own line) and its conflicts note on hold-ups.
Status: MEASURED (design decision within the description).

### RT-10 Firearms as a verb
Definition. Late and rare (the dial). Held semicolon draws the gun from under the coat; the camera moves to the aim row; the mouse or stick aims with no crosshair (an optional dot, off by default; AX-05's aim assist steps). A shot's hit depends on aim, distance and whether Tom moved. Before War a hit wounds (arm, leg or body) and never kills; at War a body hit can kill, a named and permanent event. Raised by Y1.5: an aimed shot to the arm disarms, and a shot to the leg stops a man running. A revolver holds six and reloads in a shown action after the sixth; no count on screen. Men with guns shoot from where they stand, never use cover, and run when outmatched. A shot Tom goes down, comes round in hospital (days, never money) and never dies. Nobody shoots from a moving car.
Standard. The rules above pass or fail; draw, aim and hit timings within the band of the firearms footage measuring.
Test. B: a gun range scene with timings; S: no on-screen count.
Source. The description, sections 3, 33; ruling 18 Nov (guns rare and late); MEASUREMENTS-NEEDED A (firearms feel); Y1.5.
Status: PENDING (PC measuring, 23 to 28 Nov, firearms after the rest).

### RT-11 Hidden damage and injury states
Definition. Each man has a hidden capacity by fighter type (big man most, knife man least); a jab takes little, a heavy blow about three jabs' worth, a weapon more (bat more than cosh), a blow from behind with a cosh or fist knocks out for 10 to 30 s. A man is down when his capacity is spent; down is out, never dead from fists. Tom has three states, shown only in his body: fresh, hurt (guard slower to rise, breath shorter, a stagger), beaten (down). A knife wound on Tom bleeds (blood on the coat, a give-away) until stitched by the retired doctor or the hospital; a bat leaves a limp for a day. Hurt does not stack past beaten; he can fight on hurt.
Standard. Blows to put a man down per type within the band of the damage footage measuring (KCD2, Sleeping Dogs, RDR2); "who was winning?" answered right by 4 of 5 testers from the body alone.
Test. B: fixed-seed fights counting blows to down per type; P: the five-friend question.
Source. The description, section 10; MEASUREMENTS-NEEDED A (damage model).
Status: PENDING (PC measuring, 23 to 28 Nov).

### RT-12 Escalation dial: what takes Fired to War
Definition. Fired moves to War when the town learns of either: a second shooting by a different side from the first (two firms have now fired), or a named man of one firm wounded by a shot from another. Tom's men seen carrying (more than two of them, each seen by someone) also moves it, because the town then knows who carries. Nothing moves it that nobody saw or heard. It falls one step after about two quiet game weeks, never back to 0.
Standard. War only on these learned events; never on an unseen one; the fall rule as the description.
Test. B: seeded sequences of shootings seen and unseen; the dial's state checked.
Source. The description, section 33.
Status: MEASURED (design decision).

### RT-13 Ellis's case model
Definition. The case is a list of charges and talk. Charges accumulate one per arrest that ends in a charge; an office-search find adds one (possession or handling, by what is found). Her interest falls one stage after two quiet game weeks with no new reported deed and no new charge, never below asking round once she has reached investigating. A manhunt ends with an arrest, or after three game days with no sighting it falls to investigating. Tom's "day world" is the named people of his day life: Ada, Alison Sedman, Philip Danby, Father Walsh, June Suddaby, Darren, and any regular he has called on or carried as a fare twice.
Standard. Stages move only on these rules, each with its sign; the charges list read at the ending equals the arrests and finds.
Test. B: seeded deeds and quiet stretches; the stage log against the rules.
Source. The description, sections 20, 21.
Status: MEASURED (design decision).

### RT-14 Typed-talk interpretation
Definition. Each typed line is read into one act: a question, agree, refuse, an offer (with the amount read: "a tenner" is £10, "twenty quid" £20; an offer over what Tom carries fails in character), a threat, a promise (with what and when), a claim (a statement; a lie when it contradicts what Tom knows), an insult, small talk, or leave. Offers, threats, promises and lies are acts with the seven slots and are remembered by the hearer like any deed; a broken promise comes back.
Standard. On a hand-labelled set of typed lines, the reading agrees with the label on at least the agreed share; amounts read exactly; every offer, threat, promise and lie enters the hearer's memory.
Test. A labelled set of 300 lines (period and modern phrasing) run through the reader; memory checked after each.
Source. The description, sections 34 and the moat (seven slots).
Status: UNMEASURED (the agreement share is judgement; measured by a labelled test set, cloud, by Thu 26 Nov).

### RT-15 Live-talk abuse and off-limits input
Definition. Any typed line that is abusive, off topic, out of period, against the content rule, or tries to steer the model ("ignore your instructions") is answered in character: puzzlement for the out-of-period ("you what?"), a cold end for abuse (the person ends the talk and remembers the rudeness), a refusal in his own words for the content rule. Text that claims to do something ("I hit him", "I take the money") is talk, never an act: only inputs act. Nothing after 1992, no real brand or person, no slur, no drink or gambling is ever voiced, whatever the player types.
Standard. Zero breaches of the content rule, era or brand rules on a red-team set; every reply in character.
Test. A red-team set of 300 lines through live talk; the content gate and claim check over every reply; a fresh reviewer reads 50.
Source. canon.md content rule; the description, section 34 (claim check); 8.8 runtime guards.
Status: MEASURED (guard, zero tolerance).

### RT-16 Missed rent
Definition. Rent is owed to the landlord's agent, a named man who calls at the counter. A missed Friday becomes arrears said in words in the Ledger and by the agent on Monday. Two missed: a letter, notice to quit the flat above in a fortnight. Three: the flat is let to someone else and Tom sleeps in the office. The office itself is never lost, and arrears can be paid at any time, which ends the ladder. No game over, no dead end.
Standard. Each step on its Friday; paying clears it; the office itself is never lost at any point in the game (only the flat above).
Test. B: the do-nothing run through three Fridays; a pay-late run.
Source. The description, sections 24 (rent), 3 (no game over); the doing-nothing run of S23.
Status: MEASURED (design decision).

### RT-17 Money pots in practice
Definition. Three places money is: the pocket (cash on Tom), the tin (night money at the office, which cannot be explained) and the book (clean money, which can be spent anywhere, as the description says). Rent and drivers' wages come out of the book weekly; a car, a front's share, shops and the doctor can be paid from the book or from cash. Night money paid where it can be seen to be explained (a car bought, a front's share) is a lie someone may one day have to hold up, as any fare written for an hour he was elsewhere. Bribes and men's night cuts come from cash, as the description has the cut paid from the tin. The count turns tin money into book money within the wash limit; nothing turns the book back into tin. The tin can be stolen in an office break-in (a rival's threat, or a thief) and is then gone, said in words. A constable's search finds what is under the coat and in the hand, cash included, and what he finds he keeps.
Standard. Every payment draws from a place the rules allow; the flows ledger balances (ER-MONEY-01); a search keeps exactly what was found.
Test. B: every kind of payment from each place; a break-in; a night search with cash on Tom.
Source. The description, sections 21 (what he finds he keeps), 24 (two pots; clean money spent anywhere), 26 (the count), 27 (cut from the tin).
Status: MEASURED (design decision).

### RT-18 Pause and clock
Definition. The clock stops in talk (section 34) and in the pause menu, and nowhere else. Opening the Ledger, the paper map or a letter stops Tom but not the town, as the description already says of the map (section 24). Getting ready takes a game minute, never a screen. An assist "the Ledger pauses the town" is offered, off by default.
Standard. Clock frozen only in talk and pause (and with the assist on, in the Ledger); time passes at the clock rate otherwise.
Test. B: clock read before and after each screen.
Source. The description, sections 24 (the map stops Tom but pauses nothing), 27, 34.
Status: MEASURED (design decision).

### RT-19 Content supply at night and late in Acts II and III
Definition. Street happenings are authored (ruling 13 Nov), each with a spec and a check, never rolled at random. Nights without a job hold: a fare with a wrinkle on the radio, a rival's man seen, a crewman with a problem, a happening on the street, a call on someone whose routine allows it. Never five minutes with nothing new (section 40, and the guard S41); by day something within 30 real seconds (section 40).
Standard. The library holds enough happenings that none repeats on one street within a game week; the count per hour inside the teardown's band (GD-02).
Test. B: a do-nothing-but-walk night in Act II and in Act III: the five-minute rule and the repeat rule logged.
Source. The description, sections 14 (happenings) and 40; ruling 13 Nov; MEASUREMENTS-NEEDED A (density).
Status: PENDING (PC measuring for the band, 23 to 28 Nov; the story measure for Act III's nights, by Sat 28 Nov).

---

# Design pass 2: tests for the rows whose standard was only a pointer (run 2, 21 November)

Fifteen rows had a definition in the description but a standard that was only a pointer to a section. Each now has a pass-or-fail test from the description's own words. Where a balance number in it (a price, a share) is judgement, it follows the economy curve of GD-07 and the row says so.

### 2.4.3 Showing what people know
Definition. As the description, section 5: one ladder (notice, watch, comment, avoid, refuse, confront), posture first; witnesses talk quieter for a game hour after a deed.
Standard. Every person who knows something of Tom shows it on that ladder before any line; nobody who knows nothing shows it; the step shown matches what they hold (a told version never above a seen one).
Test. B: seeded deed, then a walk past 30 people: each one's shown step is checked against their memory store.
Source. The description, section 5 (What a person catches; Who tells whom).
Status: MEASURED (pass or fail on the description).

### 2.6.6 Armed response and the dial's police
Definition. As the description, sections 21 and 33: at Fired, armed officers come from the station for gun calls, slowly; at War, armed cars, stop and search on the street, everyone jumpier.
Standard. No armed officer before Fired; at Fired every reported gun call brings armed officers later than an ordinary call; at War at least one armed car is on the Hook's streets and searches happen on the street; none of it shown on any map.
Test. B: the dial forced through each state with seeded gun calls; police responses logged.
Source. The description, sections 21, 33; RT-12.
Status: MEASURED (pass or fail on the description).

### 2.7.1 Clean money and the fare book
Definition. As the description, section 24: clean money is in the fare book and can be spent anywhere; rent £18 every Friday; drivers' wages weekly from the book.
Standard. Every fare driven, by Tom or the firm's drivers, enters the book; rent and wages leave it on their days; the book's balance always equals its flows (ER-MONEY-01).
Test. B: a week of fares and wages; the book audited against the flows.
Source. The description, section 24; RT-17.
Status: MEASURED.

### 2.7.2 Night money and the tin
Definition. As the description, section 24: night money is in the tin at the office and cannot be explained.
Standard. Every night job's take goes to the tin or the pocket, never the book except through the count; the tin can be lost only by being stolen or searched, said in words.
Test. B: night jobs then the count; a break-in on the tin.
Source. The description, sections 24, 26; RT-17.
Status: MEASURED.

### 2.7.3 The wash
Definition. As the description, section 26: at the count the book can hide £10 plus 80% of the fares really driven since the last wash; over that Sheila warns first and thinks less of him; a front's till raises the limit by a set amount a week.
Standard. The count never washes over the limit without Sheila's warning first; each week over is recorded for Act III; a front raises the limit by its set amount. The 80% and the front's amount are balance figures checked against GD-07's money curve.
Test. B: counts at, under and over the limit; the record read by RT-01's grading.
Source. The description, sections 26, 31; GD-07.
Status: PENDING (the balance figures with GD-07, PC measuring 23 to 28 Nov).

### 2.8.2 Partial payment and the book
Definition. As the description, section 25: a debtor pays what his purse holds and the rest stays on the book; squeezing and letting go are told on the street.
Standard. A payment never exceeds the debtor's purse; the remainder stays and is said in the Ledger's Money page; a squeeze or a let-off produces a told version within a game day.
Test. B: each of the five debtors fronted up with different purses.
Source. The description, section 25.
Status: MEASURED.

### 2.9.2 Keeping or ending the arrangement
Definition. As the description, sections 36 and 37: kept, the landing men hand over their end of the Hook in Act II and fade; ended, the ground is open and the rivals' ladders start a rung sooner. Both reach Act II.
Standard. Kept gives the hand-over beat; ended starts every rival one rung up; both reach rung 2 (RT-04).
Test. B: week-one runs kept and ended; the Act II state compared.
Source. The description, sections 36, 37; RT-04.
Status: MEASURED.

### 2.10.4 The Fixer
Definition. As the description, section 29: Keith Garbutt sells true reads of a rival (true to what the town really holds), a meeting, and one truce (RT-06: holds a rival at its rung for two game weeks, once a game).
Standard. Every read he sells is true to the town's memory at that moment; a meeting he brokers happens; the truce holds exactly two game weeks and is offered once. His prices follow GD-07's curve.
Test. B: reads compared with the rival's true state; truce timing.
Source. The description, sections 29, 30; RT-06.
Status: MEASURED (prices follow GD-07).

### 2.11.1 Recruiting
Definition. As the description, section 27 and RT-07: from the thirty regulars by meeting a need (slow, holds) or spending a hook (quick, brittle); each recruit brings a use the firm lacks.
Standard. A need recruit's loyalty ceiling is higher than a hook recruit's; each named recruit brings the use the description gives (locks, fists, nights on the warehouse row, the ferry, paint); boxing club men can be recruited there.
Test. B: both roads on two men; the same pressure applied; who breaks first.
Source. The description, section 27; RT-07.
Status: MEASURED.

### 2.11.3 Crew fates
Definition. As the description, section 27: poached (the Widow takes his least loyal man), frightened off, arrested, docked or expelled by Tom, killed for good; each fate a town fact.
Standard. Each fate reachable in play; each produces a told version and a Ledger line; a poach always takes the least loyal man.
Test. B: seeded runs for each fate.
Source. The description, section 27.
Status: MEASURED.

### 2.12.2 Rung table
Definition. The rung table of the description, section 32, with the conditions of RT-04.
Standard. As RT-04: each rung on exactly its holdings; what opens at each rung opens then and not before.
Test. B: rung climbs with holdings added one at a time.
Source. The description, section 32; RT-04.
Status: MEASURED (design decision via RT-04).

### 2.12.3 Access and soft keys
Definition. As the description, section 32: standing, dress, an introduction, an appointment the Fixer brokers; a filthy man is refused where he would be let in clean; a decent jacket gets him past the Harbour Board's counter.
Standard. Each soft key opens exactly its doors: the Harbour Board's counter refuses him in the arrival clothes and lets him in with the decent jacket; any door that opens to him clean refuses him bloodied or filthy.
Test. B: the same doors tried in each outfit and state.
Source. The description, section 32.
Status: MEASURED.

### 2.15.2 Ranks and accounts
Definition. As the description, section 28: the rank outside Mickey's is his; the ferry rank and a second rank are won by being there with a car on the board enough days, or by a word with whoever holds them; accounts in order: the cold-store contract, the Harbour Board's late men, a solicitor's office.
Standard. A rank is won by either road and never otherwise; accounts open in that order, each at its rung (the cold store at rung 3); "enough days" is five days in a fortnight (a balance figure checked with GD-07).
Test. B: rank presence runs; account order.
Source. The description, sections 28, 31.
Status: MEASURED.

### 3.5.5 Sit-downs
Definition. As the description, section 30: in talk with a rival head, in a back room, at the Fixer's table or in the back of Tom's own cab; accept, defy, or counter with what he knows; only a plain yes taken; what cannot be undone asks twice; Leave always there; Act II ends at one.
Standard. Each answer leads to a different following state; counter needs a hook Tom holds (RT-07); what was said is what the town then believes (a told version within a game day).
Test. B: a sit-down played each way; the following state and the town's version compared.
Source. The description, section 30; RT-06, RT-07.
Status: MEASURED.

### 8.10 Collision and physics
Definition. Nothing passes through walls, bodies or cars; nobody and nothing is ever stuck for more than 5 s (ER-CORE-01); no car launches into the air or spins on a touch; a struck person falls as the hit's direction says; things to hand break by the description's blow counts.
Standard. In a 2-hour soak of walking, driving and fights: zero pass-throughs, zero stuck over 5 s, zero launches.
Test. B: the soak with a clip and pass-through detector.
Source. ER-CORE-01; ER-FIGHT-06; the description, sections 10, 11.
Status: MEASURED (guard).

---

# Design pass 3: red team 2's gaps, the fit check's gaps and text fixes, and the clock (run 4, 21 November)

What this part is. Red team 2 left 22 rows UNDEFINED (RT2-01 to RT2-22, redteam2/real-gaps-v2.md). The fit check of 21 Nov (FIT-CHECK-2026-11-21.md) found ten number gaps (G1 to G10), four text faults (F03, F13, F15, F20), clock misfits (F07 to F13) and seven players' gaps not on any list. Each is defined here in the design's own words, inside canon and his rulings, with a pass-or-fail standard and its source. The same headings as above: Definition, Standard, Test, Source, Status.

Statuses follow the guard written into DESIGN-COMPLETE.md on 21 Nov (G-A): MEASURED only where the standard rests on a reference game's number, a dated real-world figure or published standard, or a rule of his; DECIDED where the standard is a design decision taken here, his to overturn; PENDING where a number waits on a named, dated study or on his answer.

Reviewed 21 Nov by a fresh Opus reviewer against canon, RULINGS, the description, the fit check and red team 2's list: 30 points, fixed once in this version (the road plan rebuilt on the built 48 m Quay Street and its bend, the walk crossing, L-01's people, P09's music, G8's takings against the missed rent, G4's holdall speed, RT2-11's single-press rule and the water, RT2-04's wound-down road, RT2-01 and RT2-18 on suspension, RT2-06's way back and Sheila's return, F13's fail-safe start, G5's beat, the junction spacing, the docks fallback, CLK-01 and CLK-06, the running-clock hours, F15's split, RT2-07's one rung at a time, Cammack's base, RT2-12's edges, RT2-14's dial and stolen guns, G3's one rule, the status calls, RT2-05's fallbacks, G6, G7, G8, G10, F03 and RT2-21's wording). Kept as written: D-Q2 to D-Q4 stay DECIDED, as this run's brief directs (the reviewer would have marked them PENDING his answer).

His rulings applied: the map is the Hook plus its docks; length 15 to 20 hours; mods out; GTA VI first where it sets the higher bar, no GTA VI story; Mafia is never a reference (the fit check's F04 now names GTA IV in Mafia DE's place); a field-of-view setting 75 to 100 degrees, default 86 (his ruling of 21 Nov; AX-03 now builds it, which closes the point carried since run 2).

## The advisor's decisions of 21 Nov, inside his rulings (DECIDED, his to overturn)

- D-Q2 (fit check question 2, answer A). Car chases get a drivable loop of 1.5 km or more inside the Hook and the docks (Quay Street, the cold-store road, the dock road and the quay), with the parade's back lane, the yards and the Old Basin to break sight, and one rule for a chase at the soft edge (G3 below). The map ruling is untouched: no road past the soft edge is made drivable.
- D-Q3 (question 3, answer A). Side stories count inside the ruled 15 to 20 hours: about 25 side stories at about 12 minutes each (about 5 hours) and the main line about 12 hours (F15 below).
These three were his scope questions in the fit check; the advisor took them inside his rulings, as this run's brief records, and each stays his to overturn.
- D-Q4 (question 4, answer B). 60 written street lines each for the 12 people seen most, 30 for the rest (L-01 below).

## The Hook's road plan in metres (G1)

### G1 The road plan
Definition. The Hook and its docks on one plan, in metres, origin at the ferry landing, x to the east and y to the north. The water lies south of the quay road and fills the Old Basin. Quay Street is the built street of his atlas ruling (5 Oct): 48 m from the quay, climbing, with Mickey's at the quay end and the six bays of the parade on its east side, bending east behind the parade at its far end; the plan keeps it exactly so and joins the rest of the Hook to it. Every road is drivable both ways at its width; lanes marked foot only are bollarded or gated at both ends, so a car cannot follow.

| Road | From (x, y) | To (x, y) | Length | Width | What is on it |
|---|---|---|---|---|---|
| The quay road | ferry landing (0, 0) | fish dock (540, 0) | 540 m | 9 m, quay edge on the south side | the landing and its rank (0 to 30), the foot of Quay Street (120), the chandler's and the boxing club's hall (190 to 230 on the north side), the Old Basin's mouth (250 to 480, crossed on the fixed basin bridge), the fish dock (480 to 540) |
| Quay Street (built, 48 m) | quay road (120, 0) | its bend (120, 48) | 48 m, climbing about 3 m | 11 m with both pavements | Mickey's on the east side at the quay end, the six bays above it (bay 1 fishmonger, bay 3 the empty unit, bay 4 launderette, bay 5 grocer); plain terraces on the west side across from Mickey's, the shops (newsagent, ironmonger, tea room) across from the parade's north half |
| The bend behind the parade | (120, 48) | the north road's foot (160, 62) | 42 m | 9 m | the parade's back doors and yard gates on its south side |
| The north road | (160, 62) | the soft edge (160, 400) | 338 m | 9 m | Chapel Lane's corner (260), the cold-store road's junction (350), Cammack's lock-ups (east side, y 290 to 320), the used-car lot (y 360 to 395) |
| Chapel Lane (the west road) | the north road (160, 260) | the soft edge (-80, 260) | 240 m | 7 m | the chapel and the closed school (x -20 to 60), the retired doctor's terrace |
| The cold-store road | the north road (160, 350) | the dock road (540, 350) | 380 m | 9 m | Basin Road's top (210), the cold stores' loading yard mouth (340), the cold stores (x 300 to 470, north side), the warehouse row's top (480) |
| The dock road | the cold-store road (540, 350) | the fish dock (540, 0) | 350 m | 10 m | the dock gate and its yard mouth (y 210), customs and the Harbour Board (y 20 to 80) |
| Basin Road | the quay road (250, 0) | the cold-store road (210, 350) | 353 m | 7 m | the Old Basin's west quay (y 30 to 250), Iveson's yard (y 260 to 320) |
| The basin's north road | Basin Road (220, 255) | the warehouse row (480, 255) | 260 m | 7 m | the burned warehouse (x 300 to 360) |
| The warehouse row | the quay road (480, 0) | the cold-store road (480, 350) | 350 m | 7 m | Norman Dent's warehouses, the basin's east quay (y 30 to 250) |
| The yards' lane, foot only | the quay road (175, 0) | the bend (150, 58) | 63 m | 2.5 m | Mickey's yard and the parade's yards, one vault place (the back fence) |
| The terraces' ginnel, foot only | the quay road (60, 0) | the north road (160, 330), diagonally through the yards | 345 m | 1.5 m | Ada's back gate, Chapel Lane crossed at (139, 260), three vault places |
| The warehouse cuts, foot only | Basin Road | the north road, at y 150 and y 300 | 50 m each | 2 m | one vault place each |

Numbers that follow from the plan:
- The Hook's footprint is about 620 m by 400 m (x -80 to 540, y 0 to 400), about 0.25 square kilometres, all of it reachable.
- Crossing by car, the ferry landing to the north road's edge: 120 + 48 + 42 + 338 = 548 m with three corners. The ordinary-driving bot (20 mph, 8.9 m/s, on straights, 10 mph through each corner) takes about 66 s; at 28 mph throughout about 44 s. The provisional band 60 to 100 s (GD-01) holds for the bot's profile; GD-01's band stays PENDING the reference crossings.
- Crossing on foot, the landing to the north road's edge: 60 m of quay, the ginnel's 345 m, and 70 m of the north road make 475 m. At Tom's walk of 1.6 m/s (G4) that is 4.9 real minutes, inside 3 to 5. A walking crossing, the notice unit of CLK-04, is taken as 5 real minutes.
- The chase loop (D-Q2): the quay road from the fish dock to Quay Street's foot 420 m, Quay Street 48 m, the bend 42 m, the north road to the cold-store road 288 m, the cold-store road 380 m, the dock road 350 m: 1,528 m. A second loop, the basin ring (Basin Road, the basin's north road, the warehouse row and the quay road between them), about 1,000 m; a third, the north road, the cold-store road's first 50 m, Basin Road, the quay road back to Quay Street, Quay Street and the bend, about 910 m. They share six junctions, so a chase can change loop.
- At chase speed (16 to 20 m/s, 35 to 45 mph) one lap of the 1,528 m loop takes 76 to 96 s, about one 90 s chase (F02). The longest stretch with no junction or yard mouth is 280 m (the quay road across the basin bridge; the dock road is cut at y 210 by the dock gate yard and the cold-store road at x 340 by the loading yard), 14 to 18 s at chase speed; the 7 s unseen rule is met by turning off at a junction or a yard mouth, or round the basin's warehouses (F03).
- Sight breakers on the loops: the cold stores (a 170 m block), the warehouse row, the basin's warehouses, the dock gate's sheds, and the bend behind the parade.
- The foot chase's back ways: the ginnel (345 m), the yards' lane and the two warehouse cuts, with six vault places; a 90 s foot chase at 5 to 6 m/s covers 450 to 540 m, about the ginnel and a street (F22).
- The busiest view (F31): Quay Street's 48 m, both pavements.
- If the docks are cut, as his map ruling allows when time runs short, the loop goes with them (it uses the dock road and the cold-store road): car chases then shorten to 45 s, the fit check's option C, and this line is rewritten.
Standard. (1) Every road and lane in the table exists in the map data at its length within 5% and its width within 1 m, and Quay Street matches the built 48 m street; (2) the ordinary-driving bot crosses landing to the north edge in 60 to 100 s; (3) the walking bot at Tom's walk crosses in 3 to 5 real minutes; (4) the chase loop is at least 1,500 m, drivable at 45 mph with no corner tighter than a handbrake turn needs; (5) no car can enter a foot-only lane.
Test. B: the map data read by a script for lengths and widths; the drive and walk bots timed on both crossings; a car bot sent down each foot-only lane must stop at the bollards.
Source. Fit check F01, F02, F22 and question 2; RULINGS 5 Oct (the atlas updated to the built street: 48 m, its climb, its bend east behind the parade), 3 Oct (the trades by bay), the map ruling (the Hook plus the docks, the docks cut first); the description, sections 1, 11, 22; D-Q2.
Status: DECIDED (the plan is a design decision inside his atlas ruling; its crossing bands stay PENDING with GD-01 until the reference crossings are measured, 23 to 28 Nov).

## The fit check's other gaps (G2 to G10)

### G2 Car speeds and the stop band
Definition. The Hook is a 30 mph town (the built-up limit in Britain in 1990). Traffic drives at 20 to 28 mph. The firm's cars and every car in the Hook reach 60 mph on the 420 m straights and no more there; a patrol car is no faster than Tom's car on a straight (as section 22 says of pursuers on foot). The patrol car stops a driver it sees at 50 mph or more, or doing any reckless act of section 21 (a hit, the pavement, a red light at speed); 31 to 49 mph in its sight draws a look and a noted plate, never a stop. Nobody steps out within the stopping distance of a car at 30 mph, 23 m (the Highway Code's figure).
Standard. (1) Traffic bots never exceed 30 mph; (2) the patrol never out-accelerates or out-runs the firm's cab on a straight; (3) the patrol stops at 50 mph or more in sight and never below it without a reckless act; (4) no person steps into the road within 23 m of an oncoming car at 30 mph or less.
Test. B: speed logs of traffic and the patrol; a seeded run of the cab passing the patrol at 35, 45, 50 and 60 mph; the step-out rule logged against distance.
Source. Road Traffic Regulation Act 1984, section 81 (30 mph on restricted roads; in force in 1990); the Highway Code's stopping distance at 30 mph, 23 m (the edition in print in 1990 gives the same figure); the description, sections 12, 21, 22; fit check F33.
Status: DECIDED (the 50 mph stop band is the design's; it sits on two dated real-world figures, the 30 mph limit and the 23 m stopping distance).

### G3 A chase at the soft edge
Definition. One rule for any chase, by car or on foot, that reaches the soft edge (the north road at y 440 or Chapel Lane at x -80). The chase ends there as lost: the pursuer turns back at the edge, and Tom's car or Tom goes out of the Hook and comes back as time passed, the way a fare does (30 game minutes out and back, nothing on screen). The edge is the last place the pursuer saw Tom, so by section 21's search rule the patrol waits on that road for the rest of the night, and Tom must come back past it: the same rule as any lost chase, only at a road he cannot avoid. What happens next follows what the officer saw and noted, wherever the chase was lost: a plate read (within 18 m in light 0.7 or more, RT2-16) is noted, and a deed the officer saw (a refused stop, a hit-and-run in sight) brings a constable to the office the next morning at ten (go with him, or run), by section 20's arrest rule. Driving to the edge with no fare and no chase offers the six districts by landmark, as a fare does, and comes back as time passed.
Standard. (1) Every chase that reaches the edge ends there as lost within 2 s; (2) after an edge escape the patrol is at that road's edge on Tom's way back that night; (3) the next morning's visit comes exactly when an officer saw the deed, wherever the chase was lost, and the plate is noted exactly when it was read; (4) nothing loads or fails at the edge.
Test. B: seeded chases driven straight to each edge and others lost round the loop; the next morning's events logged.
Source. Fit check F34 and question 2; the description, sections 2 (every reaction traces to a chain of sightings), 11 (the soft edge), 20, 21 (the search of the last place seen), 22; D-Q2.
Status: DECIDED.

### G4 Tom's speeds, the constables' and the runner's
Definition. Tom walks at 1.6 m/s, walks slowly (Z) at 0.9 m/s, runs at 5.5 m/s, and carrying a holdall runs at 5.3 m/s, still just faster than a constable. A constable walks his beat at 1.1 m/s and runs at 5.2 m/s; he vaults the set places in 1.2 s (Tom 0.8 s). A runner fleeing Tom runs at 5.2 m/s, Tom's run less about 5% (section 22). So Tom outruns a constable on a straight by 0.3 m/s and gains on the vaults; from 10 m behind a runner on a straight he closes in about 33 s, and a gap over about 25 m is closed only by a better line through the back ways, as the description intends. Speeds never depend on the frame rate.
Standard. (1) Speeds within 3% of the figures in the tuning table; (2) a constable never catches Tom on a straight with no obstacle; (3) a runner from 10 m is caught on a 200 m straight by a bot running flat out; (4) the vault time difference holds at every vault place.
Test. B: speed probe on flat ground for every gait; seeded straight and back-way chases.
Source. Fit check F21; the description, sections 6, 22; British walking pace about 1.4 m/s (the common figure; Tom's 1.6 m/s is a brisk walk, a design choice so the walk crossing stays inside 5 minutes); beat pace about 2.5 mph (1.1 m/s), the traditional police figure [I: widely stated, not checked against a primary source today].
Status: PENDING (the reference games' walk and run speeds from footage, PC measuring 23 to 28 Nov, block 2; the figures above stand until then).

### G5 The beat constable's round
Definition. At night (22:00 to 06:00 on the clock) the beat constable walks a fixed two-part beat at 1.1 m/s. The short round, about 200 m: up Quay Street past Mickey's, round the bend behind the parade to the yards' lane, down the yards' lane to the quay road and back to Quay Street's foot (about 3 real minutes, Mickey's door tried on the way). Then the landing leg: along the quay road to the landing and back, 240 m (about 3.6 real minutes, the landing looked over for 15 s). Short round, landing leg, again, all night; the whole cycle about 7 real minutes, the same under either clock answer, because his pace is in real time. Mickey's door is in his sight on the short round and again as he passes Quay Street's foot on each end of the landing leg; the yards' lane once a cycle. The beat never changes by chance, so the player can learn it and use its gaps; with the street on edge (section 19) a second constable walks the same beat half a cycle behind, which halves every gap. By day he walks Quay Street and the north road to the cold-store road and back. This is a design choice against the fit check's suggested 2 to 3 minutes: a beat that is everywhere at once leaves the night nothing to read.
Standard. (1) At night Mickey's door is in his sight at least once every 4 real minutes, the yards' lane and the landing at least once every 7.5; with the street on edge every 2 and 4; (2) the beat is identical on two runs from the same save; (3) a rattled bin (section 8) moves him off it and he rejoins it where he left.
Test. B: a night's position log; the gaps at the three points measured; the same save twice.
Source. Fit check F06 and P53; the description, sections 4 (the carry), 8, 19, 21; beat pace about 2.5 mph (1.1 m/s), the traditional figure [I: not checked against a primary source today].
Status: DECIDED.

### G6 How many street happenings are written
Definition. At least 60 written happenings across at least 8 kinds (at one about every 15 real minutes, about 70 meet the player in 17 hours): the six of section 14 (the row, the breakdown, the shoplifter, the lost man with a suitcase, the dog loose, the woman locked out) and two more, a man fallen on the cobbles (help him up, rob him or walk on) and a crate off a lorry at the dock gate (goods spilled: help, take or walk on, a lift if taken). Each is placed by state and hour as section 14 says. No single scene is seen twice within 3 real hours of play, and none twice in the whole game unless its people have changed (a new state, a new temper, a new relation to Tom). The kinds rule of section 14 stays (none twice in 30 minutes, or twice in a week on one street).
Standard. (1) At least 60 scenes and 8 kinds in the library; (2) in a 17-hour bot playthrough no scene repeats within 3 real hours and no scene repeats with unchanged people; (3) every scene passes the content gate.
Test. B: the library counted; the playthrough's happening log checked for repeats.
Source. Fit check F17 and P11; the description, section 14.
Status: DECIDED.

### G7 How many fare people are written
Definition. At least 40 written fare people (Tom is offered about 40 to 80 fares in a playthrough at about a fifth of play spent driving), each a named person going where their routine takes them, each with lines for at least two fares (a first ride and a later one that has changed by what Tom has done). Every fare Tom is offered after the first teaching fare carries one wrinkle, none twice running (text fix F20 below).
Standard. (1) At least 40 fare people with at least two fares each; (2) in a 17-hour playthrough no fare person rides with the same lines twice; (3) every offered fare after the first has a wrinkle and no wrinkle comes twice running.
Test. B: the fare table counted; the playthrough's fare log checked.
Source. Fit check F20 and G7; the description, section 13; canon's line of 19 Nov (fares few and chosen).
Status: DECIDED.

### G8 Amounts for what money is spent on
Definition. Every item on section 16's spending list has a price, spoken by the seller and never shown as a table. The 1990 prices (to be checked against dated 1990 sources before the gate): 20 cigarettes £1.70; the paper 25p; tea at the caff 30p; a caff meal £2.50; a crowbar £6; a torch £4; a key cut £1.50; a second-hand coat £15; the decent jacket £45; the good overcoat £90; the barber £4; a used car at the lot £600 to £1,200; the doctor's stitches £20; a brief on call £50 a week; a bought officer £50 to look away from a car once, £200 to lose a statement once. A driver's wage £90 a week from the book; a man's cut on a night job agreed in talk, £10 to £40. In Act I each driver's own fares bring the book about £85 to £95 a week, so the two drivers about cover their wages and the book alone does not pay Friday's rent: doing nothing misses it, as section 24 says, and a week of Tom's own fares pays it. From rung 2 each car on a good rank brings £110 to £140, and the contract adds its fares.
Standard. (1) Every listed item has a price in the tuning table; (2) the economy bot (GD-07) shows at each act's end at least one wanted thing out of reach; (3) every price is within 25% of a dated 1990 figure; (4) the do-nothing bot misses the first Friday's rent and the fares-only bot pays it.
Test. B: the economy bot, greedy and lazy; the prices checked against the 1990 sources.
Source. Fit check F24, G8 and P15; the description, sections 16, 24, 27; GD-07; London's 1990 cab rate (CLD:13) for the scale of fares.
Status: PENDING (1990 prices checked from dated sources, cloud, by Thu 26 Nov; with GD-07's money curve, PC measuring 23 to 28 Nov).

### G9 Crowd counts by hour and place
Definition. People in view on Quay Street's parade front (100 m, both pavements), by band: 05:30 to 07:00, 6 to 10 (the dock shift passing); the busy bands 08:00 to 09:30, 12:00 to 14:00 and 16:30 to 18:00, 25 to 35; other daytime hours, 12 to 20; 18:00 to 22:00, 8 to 14; 22:00 to 01:00, 3 to 6; 01:00 to 05:30, 0 to 2 besides the constable. On the quay road by the fish dock 05:30 to 07:00, 15 to 25. Rain halves each band; Thursday's market takes a third off the shops' daytime bands; Saturday's match doubles the street at 15:00 and 17:00 for half an hour.
Standard. Counts in the busiest view sampled every game hour fall inside each band in dry weather and inside half the band in rain.
Test. B: crowd counts sampled by hour across a week.
Source. Fit check F12, F31 and G9; the description, sections 5, 30 (at least 25 in the busiest view, DEF:159); 2.1.2 (who is out by hour).
Status: PENDING (2.1.2's hourly figure from the ONS time in and out of home tables, cloud by Thu 26 Nov; the bands are scaled to it then).

### G10 Opening hours, day and night
Definition. Shops on Quay Street 09:00 to 17:30 Monday to Saturday, shut on Sunday; the newsagent 06:00 to 18:00 and Sunday 07:00 to 12:00; the caff 06:00 to 15:00 Monday to Saturday (the dock shift's breakfast) and to 22:00 on Friday and Saturday; the chip shop on the parade 11:30 to 14:00 and 17:00 to 23:30, to 00:30 on Friday and Saturday; the launderette 08:00 to 23:00; the pawn 10:00 to 17:00, its back room by knock to 22:00; the boxing club 18:00 to 21:30 on Monday, Wednesday and Friday and 10:00 to 13:00 on Saturday; the chapel hall's evening on Tuesday 19:00 to 21:30 (tea and talk); a tea stall at the dock gate 22:00 to 06:00 for the night shift; the ferry landing's window 22:00 to 01:00. Nothing serves drink and nobody plays for money anywhere.
Standard. Each place's door opens and shuts on its hours (open by hours, section 9); at 23:00 on any night at least three places on the map are open with people in them.
Test. B: doors probed by hour across a week; the 23:00 count.
Source. Fit check F11, G10 and P28; the description, sections 9, 16; canon's content rule; the Shops Act 1950 (Sunday trading restricted in 1990).
Status: DECIDED (the Sunday closing rests on the 1950 Act; the hours are the design's).

## The fit check's text fixes

### F03 What the 70 m means
Definition. "Lost after 7 s or 70 m out of sight" means: a chase is lost when the pursuer has not seen Tom for 7 s, or the gap between pursuer and Tom is over 70 m while Tom is out of his sight. For car chases the distance is 200 m (at 16 to 20 m/s a car covers 70 m in about 4 s, which would end every car chase at the first corner). On foot the two run within 0.3 m/s of each other, so the gap rarely reaches 70 m inside 90 s and foot chases are lost by the 7 s unseen, as now. The description's sections 22 (both chase paragraphs) take these words.
Standard. Losing is decided only by time unseen (7 s) or the gap while unseen (70 m on foot, 200 m by car); distance driven alone never loses a chase.
Test. B: seeded chases where Tom drives 100 m unseen with the pursuer 50 m behind (not lost) and 8 s unseen (lost).
Source. Fit check F03; the description, section 22.
Status: DECIDED.

### F20 Which fares carry a wrinkle
Definition. Every fare Tom is offered after the first teaching fare carries one wrinkle (the description's resolved conflict, canon's line of 19 Nov). S07's "about half" is replaced by "every"; Kevin and Terry's ordinary fares are driven off screen and have none.
Standard. As G7 (3).
Test. As G7.
Source. Fit check F20; the description, section 13 and its conflicts note; canon 19 Nov (few and chosen).
Status: DECIDED (the description's reading of canon's line).

### F13 Act II's week count
Definition. One week number. Act II is about seven game weeks (under clock A) and its fail-safe (RT-04) starts four game days before the end of Act II's seventh week, so the remaining climbs (one a game day) bring the sit-down by that week's end, so Act III always opens by the start of the calendar's ninth week. Under clock B the same with five (see the clock below). RT-04's "by the end of the eighth game week" is replaced by "from four game days before the end of the seventh" (A) or "of the fifth" (B).
Standard. No Act II runs past its fail-safe week; the calendar's last week is Act III's.
Test. B: the do-nothing Act II bot under the chosen clock.
Source. Fit check F13; RT-04; the description, section 37.
Status: PENDING (his C11 decides which number).

### F15 What the act hours include
Definition. Each act's hours count everything played in it: main beats, jobs, side stories, fares, happenings and free time. Under D-Q3: the main line about 12 hours, about 25 side stories at about 12 minutes (about 5 hours), and the rest (fares, happenings, free time) inside the acts' hours, so the whole lands at 15 to 20. The main line's 12 hours include its own jobs, the fares and travel inside its beats; side stories about 5; happenings and free time the remaining 0 to 3. Act I about 2 hours, Act II 11 to 14, Act III 2 to 3. D-Q3 cuts the story bible's main line from about 14 hours to about 12: noted for the story session. Section 14's "25 to 40 side stories" becomes "about 25 (at least 22, at most 28)".
Standard. A median panel playthrough lands at 15 to 20 hours; the side-story count in the library is 22 to 28 at a median 10 to 14 minutes each.
Test. B: the hour log of three bot playthroughs (lazy, median, greedy); the library counted and its side stories timed.
Source. Fit check F15 and question 3; his length ruling (15 to 20 hours); the story bible's main line (story/measure NOTES-V2-PASSENGER-v5k6); D-Q3.
Status: MEASURED on his length ruling (the split inside it is the advisor's decision D-Q3).

## The fit check's open pairs, given a measurement (all PENDING on a named study)

- F04 Chase length against reference chases: time 10 police chases each in GTA V, RDR2 (lawmen), GTA VI footage (no story) and GTA IV, start to caught or lost (PC 2 h, block 4, 26 to 28 Nov). Mafia DE is never a reference; GTA IV takes its place by his ruling.
- F05 How often the one-hit wreck happens: bot chases and an hour of ordinary fast driving on the prototype counting hits of 35 mph or more; pass if ordinary driving at under 30 mph wrecks the car less than once an hour (cloud 1 h, with the next prototype build).
- F16 Act hours against places and people: the teardown's density band (GD-02; PC block 3, 25 to 27 Nov).
- F19 Shared street lines against how often they are said: count the situations in the line table; pass if at least 14 situations are live in every hour of a week (cloud 0.5 h, by Thu 26 Nov).
- F21 Tom's speeds against references: G4's footage figures (PC block 2).
- F24 and F25 Money over nine weeks: the economy bot once G8's prices are in (cloud 2 h, by Sat 28 Nov).
- F32 Something within 30 s by day: the 20 idle moments test on the prototype (cloud 0.5 h, with the next prototype build).

## The players' gaps not on any other list

### P04 The struck person's fall
Definition. A person hit by Tom's car falls by speed: under 10 mph a stagger and a hand on the bonnet; 10 to 25 mph knocked down, rolls once, sits up within 5 s holding the hurt; over 25 mph thrown down, lies still up to 20 s, then moves and calls out. Never a body flung through the air, never limp as dead, nothing shown at length; the choice of section 12 comes within 2 s.
Standard. Every hit plays one of the three falls by speed band; the person moves within 20 s every time; no fall reads as a death (panel question).
Test. B: seeded hits at 8, 20 and 40 mph; H: "did anyone look dead?" never yes.
Source. Fit check P04; canon (a car hurts, never kills); the description, section 12.
Status: DECIDED (inside canon's rule that a car hurts and never kills).

### P17 How many kinds of fighter
Definition. At least five kinds: the boxer who guards, the brawler who rushes, the big man slow to drop, the man with a knife who keeps his distance, and the wiry one who slips and runs. No two fights in a row use the same mix (section 10).
Standard. Five kinds in the fighter table; no repeated mix in consecutive fights in a playthrough.
Test. B: the fight log of a playthrough.
Source. Fit check P17; the description, section 10; 1.3.12.
Status: DECIDED.

### P18 Two against one
Definition. Two against one stays deadly: a skilled player, patient and using the street, wins a fair two against one about one time in four; a masher about one in twenty. Running and backing off are always there, and the street's places count double in such a fight (a man put into railings is out of it for 4 s).
Standard. In bot fights, the skilled bot wins 15 to 35% of two-against-one fights, the masher under 10%.
Test. B: 200 two-against-one fights per bot.
Source. Fit check P18; the description, section 10 (odds and nerve).
Status: DECIDED.

### P34 How many rooms open
Definition. At least 24 rooms can be entered: the 8 named places of section 15 with their back rooms and upstairs (at least 14 rooms between them) and at least 10 break-in rooms that jobs name. Every other door says it is locked. Every enterable room has something to use with the key.
Standard. Room count in the map data at least 24; every enterable room has at least one usable object.
Test. B: the map data counted; a walker bot opens every door.
Source. Fit check P34; the description, section 15.
Status: DECIDED.

### P45 Birds and animals
Definition. Gulls on the fish dock and the quay (flocks of 5 to 20 in daylight, crying, rising when someone runs at them), pigeons on the parade, a few cats in the yards at night, the yard dogs, and the one dog loose on the quay as a happening. No animal is ever hurt by any verb; a gull rising is a small noise that draws a glance.
Standard. Gulls present on the fish dock every daylight hour in dry weather; no verb harms an animal.
Test. B: an animal count by hour; S: every verb tried on an animal does nothing harmful.
Source. Fit check P45; the description, section 8 (dogs are never hurt).
Status: DECIDED.

### P52 What an ordinary drawer holds
Definition. Outside jobs, an ordinary drawer or cupboard in an enterable room holds one of a small written set (letters, a bill, a photograph, a few coins up to £2, cigarettes, a spare key to that room), never a job's thing, and searching it is the same act with the same noise and the same memory as in a job.
Standard. Every searchable container outside a job returns an item from the written set; nothing found there is worth more than £2.
Test. B: a bot searches every container outside jobs.
Source. Fit check P52; the description, section 15.
Status: DECIDED.

### P09 Music
Definition. No music station in the cab. Music is heard only where it plays in the world (a radio in the caff, the chapel's organ, a record through a window), and every piece is made for the game: canon makes every band fictional with no real lyrics, so no period recording is licensed.
Standard. Every piece of music in the build is made for the game and listed with its maker; every music source is placed in the world.
Test. S: the audio files listed against the licence allowlist and canon's fictional-brands rule.
Source. Fit check P09; canon (every band fictional, no real lyrics); the licence allowlist.
Status: MEASURED (canon and the allowlist; placing it in the world is the design's).

### L-01 Street lines for the people seen most (D-Q4)
Definition. The 12 people seen most often (Ron, Pauline, Darren, Kevin, Terry, the beat constable, the caff's owner, Brenda Laverack, Wayne Harrison, Rita Welburn, Lee Drewery and Father Walsh, or whoever the routine log shows most seen in the first two weeks, leaving out Sheila, Alison and Ada, who keep the shared lines by his street-lines ruling) each have 60 street lines of their own; everyone else keeps 30. A person's own line still comes at most once a day, so the 12 do not repeat within 60 game days, about the whole calendar (fit check F18).
Standard. The 12 most-seen people in the routine log of a two-week bot run each have at least 60 own lines; no own line repeats within 60 game days.
Test. B: routine log ranked; line table counted; a playthrough's line log checked.
Source. Fit check F18 and question 4; RULINGS street lines (Sheila, Alison and Ada keep the shared ones); the description, sections 5, 34; D-Q4.
Status: DECIDED.

## Red team 2's gaps (RT2-01 to RT2-22)

### RT2-01 The cold-store contract and rung 3
Definition. The contract comes before rung 3, never from it. The cold stores' shift manager (a named minor man) offers it once the firm has met the packing shift on time on five mornings in one game week (the packing-shift fares of section 13, driven by Tom, Kevin, Terry or any driver on the board) and holds at least four cars. Winning it opens the dock gate, as section 37 says. Rung 3 is reached when the firm holds five cars, a night desk, a first front, a first round and the contract (the rung table unchanged). Section 31's "won at rung 3" becomes "won on the way to rung 3 and held at it"; section 37's beat fires "on the contract won". The contract is open on every road out of Act I, wound down included, because winding down ends only Mickey's arrangement, never the cab trade. It is lost after three missed mornings in one game week, and it is paused (not lost) while Agar's licence hearing (RT2-18) has the licence suspended; lost, its fares stop and the dock gate's daily pass goes with it, but no rung or name ever goes back. It can be won again once, the same way.
Standard. (1) The rung conditions form no circle (a script reads them as a graph and finds no cycle); (2) the contract is reachable on all three Sunday answers; (3) three missed mornings lose it and five on time win it.
Test. B: the rung graph checked; three week-one bots carried to the contract; a missed-mornings run.
Source. Red team 2 (A16, B12; v3 B18); the description, sections 31, 32, 36, 37; RT-04.
Status: DECIDED.

### RT2-02 Attacking the police
Definition. An officer struck by Tom is a deed with the seven slots, and the officer is a witness who knows it was him, so an arrest needs no statement (section 20). Striking an officer: arrested when next met (go with him, or run), 8 hours and always a charge, never a caution; Ellis's interest rises one stage, its sign shown first. Knocking an officer out and getting away: the same, and the manhunt's sign (his description said aloud) shows within the game hour. Beat officers carry only a truncheon (British police were routinely unarmed in 1990; armed officers come only as section 21's dial says), so there is no gun to take from a constable; a truncheon taken is a carried weapon. Killing an officer: the manhunt at once (its sign still shows at least one game hour before an arrest can land), 22 hours and a charge, read at the ending; it removes the best turn of every ending. A bought officer struck stops being bought for good and acts as an honest one. Tom's line holds for officers it covers: he never lays hands on a woman officer or on Ellis, and sends against them are refused (RT-09).
Standard. Each of strike, knock-out, kill and the bought officer struck ends in its stated hours, charge and stage, with control back within 2 real minutes and no game over.
Test. B: seeded attacks on the beat constable, the patrol, a bought man; the police state and arrest hours logged.
Source. Red team 2 (A8; v3 A18, B32); the description, sections 3, 20, 21, 39; PACE custody limits (2.6.4, CLOUD-FIGURES B2); unarmed British policing in 1990 (2.6.6).
Status: DECIDED (the custody hours rest on 2.6.4's dated figures; the rest is the design's).

### RT2-03 What makes a person know Tom
Definition. A person knows Tom, for good, once any of these happens: Tom speaks to them face to face in talk; they ride as his fare; somebody they know names him to them while Tom is in their sight; or they see his face (8 m or less, light 0.7 or more) at the office counter or Mickey's door on two different days. Everyone staged in the first hour as meeting him knows him from that meeting. Knowing gates recognition at 25 m and the name ladder (section 32). A person who saw his face once but does not know him can, on seeing that face again within 8 m, say "that's the man" (a face rung matched), and can point him out to the police, but cannot name him until told the name; that is how a face seen at 8 m is later known at 25 m only after knowing.
Standard. (1) Knowing is set only by the four triggers and the first hour's staged meetings, and the test hook prints which one; (2) no person who does not know Tom ever names him; (3) recognition at 25 m only by people who know him.
Test. B: seeded meetings of each kind and a stranger who saw his face; recognition and naming logged.
Source. Red team 2 (A22; v3 B46); canon (the moat); the description, sections 5 (recognition gated by knowing), 7, 32.
Status: DECIDED (inside canon's rule that recognition is gated by knowing).

### RT2-04 How the ending is chosen
Definition. A fixed rule, read when the books open on Act III's last day, using RT-01's grading:
1. The business survives when Tom still holds the firm (the licence not revoked, at least car two running) and the books hold (no morning fell and at most two were thin, RT-01).
2. A friendship holds when the friend (Alison or Philip Danby) has been called on at least three times without a cooler door at the last, and has not learned as fact of a killing by Tom.
3. Business survives: the Kingdom. Its best turn (the built "Both") when a friendship holds, the street does not hold any of his rackets as fact (no telling of a hold-up, a killing or the night trade at fact strength among at least three of the nine principals), no serious charge (wounding, robbery, a killing, an officer struck) is outstanding and Tom gave nobody to Ellis. Otherwise its plain turn.
4. No business at the close (handed on, revoked, closed by Tom, or fallen books) and a friendship holds: the Straight Life. Its best turn (the built "Quiet") when he accepted the successor's offer and it was not withdrawn, and he is not hunted for a killing. Otherwise its plain turn.
5. Otherwise: Burn Both.
Charges and bail are read in the close (who waits for a court date) and weigh only through rule 3's best turn and rule 4's hunted test. Ellis's trade (giving her a rival) removes one charge, and the street learns who talks. Rivals' rungs weigh only through what they did to the business (a revoked licence, the contract lost, posts lost). Every condition shows its sign before it decides (3.1.5).
Standard. (1) The ending is a pure function of the save at the books' opening; (2) all five built states are reached by five scripted routes; (3) every condition that decided has a sign the player was shown, and Tom's reading named it.
Test. B: five route bots; the ending function run on 100 seeded saves twice, same result; the sign log checked against the deciding conditions.
Source. Red team 2 (A2, A52, B2, B32; v3 B4); the description, sections 38, 39; RT-01; 3.1.4, 3.1.5 (his ending rulings).
Status: PENDING (the story measure's Act III, by Sat 28 Nov, as RT-01; the rule is a design decision inside his ending rulings).

### RT2-05 Killing or hospitalising people the story needs
Definition. Tom's line already keeps Sheila, Pauline, Ada, June, Alison, Ellis, the Widow, Father Walsh and anyone of sixty or over from his hands and his sends. Anyone else can be killed or put in hospital, and the story falls back by role:
- Ron: the asks come by the outfit's man at the office door instead; the door and the rank go to a crewman or nobody.
- Darren: tips come through Pauline's radio talk and the caff; his debt is closed.
- Kevin or Terry: a car short until a driver is hired.
- A rival head (Agar or Cammack): his lieutenant (RT2-08) takes the ladder at the same rung and counts as having seen the deed; the sit-down is with the lieutenant.
- Keith Garbutt: no reads and no truce; sit-downs are in a back room or Tom's cab.
- Philip Danby: that friendship ends; Alison's stays possible.
- Anyone in hospital: absent for the days their hurt sets, the same fallback for those days, back after.
- The beat constable: the second constable takes the beat (G5) from the next night.
- The cold stores' shift manager: his deputy holds the contract and its terms (RT2-01).
- The man at the car lot: cars are bought from a man selling one (section 28's other road).
- Dennis Iveson: the fire thread runs on through Alison and Ellis; his debt is closed.
- The gun seller at the docks: guns come only by the other three ways (RT2-14).
- The landlord's agent: the landlord's letters come by post instead (RT-16).
Act II's beats, the sit-down and Act III never depend on one killable person being alive.
Standard. With each killable principal killed in week one and again in week four, a bot reaches Act III and an ending every time.
Test. B: one run per killable principal and week.
Source. Red team 2 (A7, B8); the description, sections 5, 10 (Tom's line), 36, 37; RT-09; ER-CORE-04 (no dead end).
Status: DECIDED.

### RT2-06 The firm failing for good
Definition. The firm has a floor: the office (RT-16), Pauline's radio and car two are never lost. Car two is Mickey's own, held in the estate: it cannot be sold, seized or wrecked for more than a day. The fare book never goes below zero; unpaid wages make drivers leave (section 27); Pauline leaves after two unpaid weeks and comes back when paid, and until then fares come only by the office phone when Tom is there. Sheila leaves if asked to put the books off three counts running; without her there is no count and no wash, and every week without her reads as put off; she comes back if Tom calls at her house after a game week in which he asked nobody to put the books off. From any failed state but a revoked licence (RT2-18) the way back is the same: Tom drives car two for fares, pays Pauline, hires a driver, buys a car at the lot.
Standard. From the worst state (no drivers, no Pauline, no Sheila, all other cars gone, rent missed twice), a bot driving fares alone has the radio back and one driver hired within two game weeks.
Test. B: the worst-state save and the recovery bot.
Source. Red team 2 (A6); the description, sections 3 (no game over, never a dead end), 24, 26, 27, 28; RT-16.
Status: DECIDED.

### RT2-07 What moves a rival up his ladder
Definition. Each rung on a state, never on a day (the fail-safe of RT-04 aside):
Every trigger lifts a rival one rung, from the rung below, never two (section 29):
- noticed: the first thing its people see or hear of Tom;
- a visit: two more sightings or tellings of Tom's firm working that rival's ground (the Widow's docks, Agar's clean money and ranks, Cammack's Quay Street nights), or Tom reaching rung 2;
- pressure: Tom refusing the visit, Tom reaching rung 3, or any deed against that rival's men or property;
- a threat: Tom defying or countering a pressure, or a second deed against that rival;
- the sit-down: Tom defying the threat, Tom reaching rung 4, or one of that rival's men killed.
Paying at a rung holds that rival on it for two game weeks, unless Tom does a deed against him in that time, which ends the hold. A deed against a rival lifts him one rung at once. Each climb is said to Tom's face or shown on his street within a game day.
Standard. Every climb in a playthrough's log names its triggering state; no climb happens on time alone except the fail-safe; a payment holds the rung two game weeks.
Test. B: seeded runs per rival with pay, defy and counter at each rung.
Source. Red team 2 (B3); the description, sections 29, 30; RT-04, RT-06.
Status: DECIDED.

### RT2-08 Rivals as actors
Definition. Each rival has a base inside the map, a named lieutenant and three named men with routines (names from the casting sheet, within canon): the Widow a dock office over the fish dock's net store; Agar an estate agent's office on the cold-store road that holds his papers; Cammack the lock-ups on the north road (east side, y 290 to 320). Sending men at a rival's property (one of the eight sending verbs) hits one thing: the base's windows and door, a vehicle (the Widow's van, Cammack's car) or a front or round of theirs. Each hit is a deed against that rival (RT2-07 lifts him a rung), leaves a mark until mended, and points his next pressure at the crewman who did it. A raid by Tom at night is a break-in with the base's men inside by routine (two or three at night): what is found there (the rival's book, a letter) is knowledge Tom can use to counter at the sit-down (RT-07).
Standard. (1) Each rival has its base, lieutenant and three men, each with a routine; (2) every send at a rival's property produces a climb and a mark; (3) a raid ends in a stated outcome (found, beaten off, caught, a body) with control back within 2 minutes.
Test. B: sends and raids against each base; the ladder and marks logged.
Source. Red team 2 (A18); the description, sections 27, 29, 31; RT-07, RT-08.
Status: DECIDED.

### RT2-09 Turf: the posts held and lost
Definition. The three posts (the dock gate, the cold store, the landing) are held by one crewman each, standing there by his routine in his hours (the dock gate and cold store 06:00 to 22:00, the landing 22:00 to 02:00). Held: the man is at his post. Contested: a rival's men stand there too; it is a stare on the ladder each time Tom or his man arrives. Lost: the post's man poached, frightened off, arrested or killed, or the post empty three game days, or a sit-down defied and lost on it. Retaken by putting a man there and winning the stare or the fight. Holding all three is part of reaching rung 4; losing one later never drops the rung, but costs: the landing loses the night runs, the cold store puts the contract at risk (RT2-01), the dock gate brings the Widow's tax back.
Standard. Each post's state in the log changes only on the stated events; each loss brings its stated cost.
Test. B: seeded poaching and contesting at each post.
Source. Red team 2 (A19); the description, sections 1, 27, 29, 32.
Status: DECIDED.

### RT2-10 Crowd extras as witnesses
Definition. A crowd extra who catches any slot of a deed becomes kept: given a fixed face, a coat and a home (a terrace in the Hook, or a district at the soft edge) and a routine from the crowd's hour windows, saved with the town. A kept extra remembers for good, can walk to the phone like any witness, can be found later at his routine's places, and can be reached, paid or talked round. A kept extra whose memory touches no open matter after seven game days lives at the soft edge and comes into the Hook only on his routine's days, but the police can still find and ask him.
Standard. An extra who saw a deed is in the save with his memory, is at his routine place the next day, and tells what he caught when asked.
Test. B: a deed in a crowd; the next day's search for each extra who caught a slot.
Source. Red team 2 (A23); the description, sections 5 (memory permanent, per person), 18, 19.
Status: DECIDED.

### RT2-11 Finishing a downed man, kicks and bodies
Definition. No kick input and no finisher (section 3). Finishing a man who is down is a decision in the quiet afterwards: with nobody else standing in the fight, Tom stands over him and holds the strike key for 2 s; the game asks once ("Finish him?") and twice, because it cannot be undone. With fists, yes is a serious beating (hospital, days), never a death; with a weapon it is a killing. The camera turns away and the sound carries it; nothing at length. A man down or a body is dragged with the use key held, at 0.9 m/s, both hands busy; loaded into a car's boot in 4 s (GV-01); a body put in the dock from the quay edge in 3 s (gone, never found, remembered by anyone who saw); a living man put in the water climbs out at the nearest ladder, as section 6 says. A knife used in a fight wounds (rung 7): hospital 5 game days, blood on Tom, 8 hours if arrested; apart from the fall rule (RT2-12), it kills only by the finishing decision.
Standard. (1) No single press kills except the fall rule (RT2-12) and a shot at War (section 33); (2) the double ask always comes before a finish; (3) fists never kill on open ground; (4) the drag, the boot and the dock work at the stated times; (5) a living man put in the water climbs out (section 6).
Test. B: seeded fights finished with fists, a knife, a bat; drag, boot and dock timed.
Source. Red team 2 (A27, B19); canon's content rule (no cruelty as spectacle); the description, sections 3, 10, 27; GV-01.
Status: DECIDED (inside canon's rule and the description's: no finishers, fists never kill).

### RT2-12 The rare fatal fall
Definition. A fall kills only when all hold: a heavy blow or a weapon blow knocks the man down; his head lands within 0.4 m of a kerb's edge, a step's edge or a wall's foot; and he was already spent in that fight (at least three heavy blows or one weapon blow taken before). Before such a blow he shows it: unsteady on his feet, guard down. Never in the boxing club, never by a car, never to Tom, never from fists alone on open ground.
Standard. (1) Deterministic: the same fight replayed gives the same result; (2) in bot street fights near the three edges (a kerb, a step, a wall's foot), a fall kills in 1 in 50 to 1 in 20 knockdowns; away from any edge, never.
Test. B: 1,000 seeded street fights; the rate counted by place.
Source. Red team 2 (B18); the description, sections 3 (no chance in the town), 10 (a fall within 3 s of a blow can kill, rarely).
Status: DECIDED.

### RT2-13 Robbed when beaten
Definition. Tom is robbed when he is beaten by men who rob for a living (a rival's men, the dockers by car two, a robber), never by a constable, at the boxing club, or by a debtor standing his ground. They take the paper money in his pocket (coins are left) and anything in his hand or under the coat they want (the envelope, a weapon, goods); never the Ledger, never his coat, never the office keys. The takers are named men with routines: Tom can front them up, send men, or let it go; a taken envelope becomes a debt to the landing men of what it held, said by Ron the next day.
Standard. Every beating by a robbing kind takes exactly the stated things; every other beating takes nothing; the takers can be found by routine.
Test. B: seeded beatings by each kind; pockets before and after.
Source. Red team 2 (B34); the description, sections 3 (no chance), 10 (sometimes robbed).
Status: DECIDED.

### RT2-14 How guns reach Tom
Definition. Two kinds of gun exist, both of fictional make: a service revolver (six rounds) and a sawn-off shotgun (two). The game starts with none in the Hook. Mickey's revolver lies in his inner office's desk under the real book, found once when the locked office opens on Sheila's trust (section 37). One seller at the docks, a deckhand off a coaster in on Tuesdays and Fridays, sells at the fish dock after midnight to a man introduced by Rita at rung 3 or by Darren's tip: a revolver £150, a shotgun £90, rounds £10 a box. A gun can also be taken from a man who drew one (the grab, at dial Shown or higher) or from a body. Rounds are reloaded from a box kept in the office drawer or under the coat (one of the two places), in a shown action; no count on screen. Guns are also stolen: from a rival's lock-up or base on a raid (RT2-08). A gun moves the dial only when it is seen or heard, as section 33 says (it never moves on a deed nobody saw or heard); Mickey's revolver found in private moves nothing until it is shown.
Standard. (1) No gun in anyone's hands before the first one reaches the Hook through a person (Mickey's revolver lies unfound in the desk till then); (2) every gun traces to one of the four ways: bought, stolen, taken, found once at Mickey's; (3) the dial moves only on a gun seen or heard.
Test. B: a run that takes each way to a gun; the dial log.
Source. Red team 2 (A62, B20); the description, sections 33, 37; ruling 18 Nov (guns rare and late); RT-10.
Status: PENDING (the prices checked against dated 1990 figures with G8, cloud, by Thu 26 Nov).

### RT2-15 The successor's offer and the last day
Definition. The crewman who asks is the most loyal man with at least three game weeks in the crew who is not past his nerve; a tie goes to the longest served. If none qualifies there is no offer. Its sign comes first: he stays late at the office on Act III's first evening. Accepting means Tom hands him the firm at the close (the Straight Life's best turn if not withdrawn and Tom is not hunted for a killing); refusing keeps the firm with Tom. It is withdrawn if a morning falls (RT-01). On the last day Tom can call on three people at most before the books open at five in the afternoon: each a short scene, chosen from people whose routine has them in the Hook that day and whom he has called on or spoken to before; other doors are shut.
Standard. The asker is chosen by the stated rule; at most three calls happen on the last day; the offer is withdrawn on a fallen morning.
Test. B: seeded crews; the last day's calls counted.
Source. Red team 2 (A51, B36); the description, sections 38, 39; RT-01.
Status: PENDING (the story measure's Act III, by Sat 28 Nov, with RT-01).

### RT2-16 Police memory and arrest hours for road deeds
Definition. Each officer remembers like anyone else, for good; the station keeps what was signed, every plate noted and every description reported. A patrol acts on a description only while the deed is hot in talk (cooling by kind, 2.4.2: a hit-and-run 3 game days, an officer struck 7, a killing never cools). An officer who knows Tom recognises him at 25 m; one who has only the description stops a man who matches two marks (the coat and the car, the coat and a limp) within 18 m in light 0.7 or more, while the deed is hot. A noted plate is known for good; while its deed is hot the car is stopped on sight. Arrest hours: a hit-and-run 8 hours and a charge; striking an officer 8 hours and a charge (RT2-02); a refused stop with no deed behind it 2 hours and a caution, a charge if it is the second.
Standard. Recognition, description stops and plate stops follow the stated thresholds; arrest hours as listed.
Test. B: seeded road deeds with Tom matching one or two marks; stops logged.
Source. Red team 2 (A53); the description, sections 7 (sight bands), 20, 21; 2.4.2 (cooling, KCD2's few game days); Road Traffic Act 1988, section 170 (failing to stop after an accident, an offence in 1990).
Status: DECIDED.

### RT2-17 A gun found in a stop at War
Definition. At War the police stop cars at two fixed points (the dock gate and the north road's junction at Quay Street's top) between 18:00 and 02:00, so the player can learn them. A gun found on Tom or in the cab at any stop: arrest on the spot, 12 hours, always a charge, the gun kept, Ellis's interest up one stage. A crewman driving a firm car with a gun in it is arrested instead, and may break past his nerve (section 27).
Standard. Stops at War happen only at the two points in the stated hours; a found gun always gives the stated result.
Test. B: seeded runs through the points with and without a gun, Tom and a crewman driving.
Source. Red team 2 (A86); the description, sections 21, 33; Firearms Act 1968 (carrying a firearm in public, an offence in 1990).
Status: DECIDED.

### RT2-18 The licence hearing
Definition. Agar's ladder: the licence letter is his pressure; his threat is a hearing at the council's licensing committee (in the Exchange, an appointment reached at the soft edge, a scene in talk of under 2 real minutes). The firm keeps its licence if at least two hold: every car passed Agar's inspection (no unmended damage), the fare book's last four weeks have no week put off, Tom attends dressed in the decent jacket or better, and no road deed charge is outstanding. Otherwise the licence is suspended for two game weeks: the firm may take no bookings (a minicab never plies for hire in the street), Pauline cannot dispatch, the contract is paused and the count washes only the £10. A firm car seen carrying a booked fare while suspended is stopped, and a second such stop revokes the licence for good: the business does not survive (RT2-04), and RT2-06's way back does not apply (Tom keeps the office and car two as a private man). Not attending counts as one condition failed.
Standard. The hearing's result follows the four conditions; suspension and revocation have the stated effects.
Test. B: seeded hearings with each count of conditions; a suspended firm driven for hire twice.
Source. Red team 2 (A94); the description, sections 29 (Agar's paper pressure), 26, 31.
Status: DECIDED.

### RT2-19 The phone
Definition. Phones are the office's (the desk phone and Pauline's line), three phone boxes (by the landing, at the parade's north end, at the dock gate) and some homes' own. From a box a call costs 10p from Tom's pocket. Tom can ring the office, anyone whose number he has (numbers are facts in the Ledger, from a card, from being told, from the real book, or businesses from the directory in the box: the caff, the pawn, the solicitor, the station, the hospital), and 999, free: an anonymous call brings a constable to the spot that night but is never a statement, so it never makes an arrest alone. A rival head can be rung only once Tom has the number (from Garbutt or the real book). Calls are talk, with the clock stopped as talk stops it. The office answering machine takes messages when nobody is in; Tom plays them with the use key and each goes into the Ledger (a job channel). Garbutt carries a pager: paged from a box, he rings that box back within half a game hour. Tom never carries a pager.
Standard. Each phone does exactly the stated things; a 999 call never alone makes an arrest; numbers are known only from the stated sources.
Test. B: calls of each kind from each phone; the answering machine with three messages.
Source. Red team 2 (A41, B30); the description, sections 2 (late analogue: landlines, boxes, machines, pagers for fixers), 14, 19.
Status: DECIDED.

### RT2-20 The clock in moving talk
Definition. One rule: the clock stops in talk only when Tom is standing and the talk screen is up (section 34, RT-18). Talk staged while walking or driving (a fare's talk, a sit-down in the cab, a witness walked with) runs the clock at its rate and the world runs on: the lines show as subtitles, choices as suggested lines, and Tom or the car keeps moving. A witness stopped with "Oi!" and talked to is standing talk: the clock stops and so does her walk.
Standard. Clock read before and after every talk: stopped in standing talk, running in moving talk.
Test. B: a fare talk, a cab sit-down and a stopped witness, clock logged.
Source. Red team 2 (A102, B17); the description, sections 11, 30, 34; RT-18.
Status: DECIDED.

### RT2-21 After the ending, and past the calendar
Definition. After the ending the clock runs on from the ending's day. Side stories not finished stay open; fares, happenings, rent and the dial run as before; fronts and rounds keep paying if the business survived; rivals stay on their rungs and climb no more; Ellis's stage holds. No new main beats (section 39). In Burn Both Tom keeps car two and the office. The calendar cannot overrun: the fail-safe ends Act II on time (F13) and Act III is one week, so the ending falls by the calendar's last week; after it, the town repeats its ordinary weeks (Thursday market, Saturday match, Sunday) with no further special days beyond Christmas Day, which keeps Sunday's routines with the chapel busy and the shops shut.
Standard. In post-ending play every listed system runs or stops as stated for 14 game days without a fault.
Test. B: 14 game days of play after each of the five endings.
Source. Red team 2 (A69, A70, B28, B29); the description, sections 5 (calendar), 39; 7.15 (ruling 23 Sep).
Status: DECIDED.

### RT2-22 A foot chase caught by a constable
Definition. Caught (his hand on Tom's collar), the constable searches as if Tom had stood (section 21). Found nothing and no cause beyond the running: Tom's name taken (the constable now knows him) and a word; no arrest. Found a weapon, stolen goods or the envelope, or Tom is wanted on a signed statement, or the constable saw the deed: arrest with that deed's hours. Running is not a crime, but the next challenge by that officer is on cause: he searches without being talked round. Seen again the same night or while the deed is hot, he calls out and a new chase starts.
Standard. Every caught chase ends in exactly one of the stated outcomes by what Tom carries and what the officer knows.
Test. B: seeded caught chases with and without carried things and statements.
Source. Red team 2 (v3 A19, B29); the description, sections 20, 21, 22.
Status: DECIDED.

## The clock (his open C11): both versions written, PENDING his answer

The question as put to him on 21 Nov: A) keep 45 s a game hour with the fixes F07 to F10; B) 60 s a game hour, the calendar about 7 weeks and Act II about 5; C) 90 s a game hour. The fit check recommended B. Below are the design fixes for A and for B, each complete, so whichever he picks drops into the description the same day (C, if he picks it, needs a third pass: about 4 weeks, Act II about 2.5, too short for the two-week cooling rules, so those rules would change too). The rows they touch (7.13 and CLK-01 to CLK-07 in the map) are PENDING his answer. Arithmetic: under A one real second is 80 game seconds and a day is 18 real minutes; under B one real second is 60 game seconds and a day is 24 real minutes.

| Row | What | Version A (45 s an hour) | Version B (60 s an hour) |
|---|---|---|---|
| CLK-01 (F07) | The staged first hour against the landing's window (22:00 to 01:00) | Continuous at 45 s the clock reads about 03:30 to 07:00 at play minute 11:30. Fix: the first evening runs slower, 105 s a game hour from the first fare (play 2:30, about 18:30 on the clock) until the hand-over at the landing or 01:00, then 45 s again; with about 1.5 real minutes stopped in talk, Ron's ask lands about 20:30 and the landing about 22:45. Said nowhere on screen; it is the only place the rate changes | Continuous at 60 s, with about 2.5 real minutes stopped in talk, play minute 7:00 reads about 21:10 and 11:30 about 00:40: inside the window with no special rule. Fix: none, beyond keeping the first hour's talk stops at 2.5 to 3.5 real minutes so the landing falls between 22:00 and 01:00 (with 2 minutes it would read about 01:10) |
| CLK-02 (F08) | The hurry wrinkle | Given in clock terms, 2 game hours ahead ("the last ferry's at ten, it's gone eight"), 90 real s, about one car crossing with 20 s spare | 1.5 game hours ahead ("it's gone half eight"), 90 real s, the same real time |
| CLK-03 (F09) | Routines against walking | Each person's places within about 150 m walking (about 95 real s, 2 game hours); longer moves as a few blocks of several game hours | Within about 200 m (about 125 real s, 2 game hours); longer moves the same way |
| CLK-04 (F10) | Job windows against the walk to them | Windows at least 3 game hours (2.25 real min); every timed step known at least 7 game hours (5.25 real min, one walking crossing) before it opens; "wait until" for all | Windows at least 2 game hours (2 real min); known at least 5 game hours (5 real min) before; "wait until" for all |
| CLK-05 (F11) | The evening (18:00 to 24:00) and the shop day | Evening 4.5 real min; shop day 6.4 real min; dark about 10.5 of 18 real min | Evening 6 real min; shop day 8.5 real min; dark about 14 of 24 real min (GTA V's evening about 12 real min, KCD's about 24, CLD:54 to 56) |
| CLK-06 (F13, F14) | Calendar and acts | 9 game weeks from Mon 15 Oct to about 16 Dec: Act I 1 week (1.4 to 2.1 h), Act II 7 weeks (11 to 14 h with most nights played), Act III 1 week (1.4 to 2.1 h, short of the description's 2 to 3); fail-safe at the end of Act II's week 7 | 7 game weeks from Mon 15 Oct to about 2 Dec: Act I 1 week (1.9 to 2.8 h), Act II 5 weeks (9.3 to 14 h), Act III 1 week (1.9 to 2.8 h, inside 2 to 3); fail-safe at the end of Act II's week 5. Bonfire Night (Monday of week 4) and Remembrance Sunday (11 Nov, the Sunday of week 4) stay inside the calendar; the 7-week total is 13 to 20 h against his 15 to 20 |
| CLK-07 (weekly rhythms) | Rent each Friday, two quiet weeks to cool the dial, a rival rung a week, talk cooling 1 to 7 game days | Unchanged: Act II's 7 weeks hold up to 3 dial falls and every rival's 4 climbs | Unchanged in game days: Act II's 5 weeks hold 2 dial falls and the 4 climbs (RT2-07 climbs on states, not weeks); talk cools in 24 real min to 2.8 real h, a third longer than A |

Act hours in CLK-06 count only time with the clock running. Talk stops the clock (aimed at about 19% of play) and adds real time on top, while waits and sleeps skip it; so a played act runs up to about a quarter longer than the table's running hours, and under either version a player who skips few nights can pass 20 hours. Standard (3) below, three bot playthroughs, decides; if the median runs over, the fix is more nights skipped by default (sleep offered at every home-coming), never a shorter calendar.

Rules that are the same under both: the beat constable's round in real minutes (G5); the busy bands by hour (G9); fares 1 to 2 real minutes; the description's section 3 sentence "A game hour is 45 real seconds, so a game day is 18 real minutes" becomes "A game hour is 60 real seconds, so a game day is 24 real minutes" under B and stays under A with CLK-01's first-evening rate added.

Standard (either version). (1) In the staged first hour the hand-over at the landing falls between 22:00 and 01:00 on the clock for a bot playing the staged order at median speed; (2) no job window is shorter than one walking crossing's notice plus the window's minimum; (3) a median bot playthrough's total lands at 15 to 20 hours and each act inside its band; (4) the clock value lives once in the tuning table.
Test. B: the first-hour bot with the clock read at each mark; the job-window lint over the job library; three bot playthroughs (lazy, median, greedy) for act hours.
Source. Fit check F07 to F14 and question 1; his C11 (open since the feel decisions); 7.13's references (GTA V and RDR2 48 real minutes a day, CLOUD-FIGURES C2); the description, sections 3, 4, 36 to 38.
Status: PENDING (his answer to C11).

# Design pass 4: his clock, the chase against the chase sheet, the crowd against the counted views, and the first solid numbers (run 5, 23 November)

Written 23 Nov 2026 from 13:18 Swiss (Opus 5.5). Sources new since run 4: his clock ruling of 21 Nov (RULINGS on wip: "clock 60 s a game hour, Act II about 5 game weeks"); mods out at release (RULINGS 23 Sep, confirmed 22:08, 20 Nov); the order of 23 Nov (a number is measured for the gate only on five uncut, dated samples read at a finer step than what it measures; installed games used first); the measuring sheets on wip to 22 Nov (STATUS.md, car-chases-sheet, the GTA VI being-seen, driving and G-row sheets, small-district, street-life, port-towns). Two numbers there are solid by the five-sample rule: GTA VI's whole wanted spell at two stars ended by escaping in a car, and a parked-car entry. Everything else below is a lead and is named as one.

Reviewed 23 Nov by a fresh Opus reviewer against the sheets, the clock table, RT-04, F13, G1, G3, G9 and the description's sections 21 to 23: 14 points, fixed once in this version (the G5 figure is the whole wanted spell, not the search, so the search band is a judgement and PENDING; section 21's search and new-chase wording replaced; the return rule four of five, a lead; 1.2.3 limited to cars Tom may open, carjacking out by section 23; both caveats on the entry figure; G9's bands rescaled; one named busiest view on the right day; GTA VI's beach count stated; the archive's 15 to 30 quoted; every line that said 90 s listed; the chase sheet's narrow-street reading followed; C-02's band explained; F13's fail-safe wording; CLK-06's low end left to the bots).

## The clock: version B taken (his ruling, 21 Nov)

The table in design pass 3 ("The clock") is settled: column B is the design, column A is withdrawn. In words:
- One game hour is 60 real seconds; a game day is 24 real minutes. The description's section 3 sentence reads "A game hour is 60 real seconds, so a game day is 24 real minutes". No first-evening rate change (CLK-01's A fix is not built).
- CLK-01: the staged first hour's talk stops total 2.5 to 3.5 real minutes, so the hand-over at the landing falls between 22:00 and 01:00 on the clock.
- CLK-02: the hurry wrinkle is given 1.5 game hours ahead ("it's gone half eight"), 90 real s.
- CLK-03: each person's places within about 200 m walking (about 125 real s, 2 game hours).
- CLK-04: job windows at least 2 game hours (2 real min), every timed step known at least 5 game hours (5 real min) before it opens; "wait until" for all.
- CLK-05: the evening (18:00 to 24:00) is 6 real minutes, the shop day 8.5, dark about 14 of 24.
- CLK-06 and F13: 7 game weeks, Mon 15 Oct to about 2 Dec 1990: Act I one week, Act II five weeks, Act III one week. RT-04's "by the end of the eighth game week" becomes F13's B wording: the fail-safe starts four game days before the end of Act II's fifth week, so the sit-down falls by that week's end. Bonfire Night and Remembrance Sunday stay inside week 4. Column B gives 13 to 20 running hours against his 15 to 20: the low end may fall short, and standard (3) below (three bot playthroughs) decides; if the median falls short, the fix is fewer nights skipped by default, never a longer calendar.
- CLK-07: unchanged in game days; Act II's five weeks hold two dial falls and the four rival climbs (RT2-07 climbs on states).
- 7.13: 24 real minutes a day. Against the references (GTA V and RDR2 48, KCD about 96, GTA VI about 144 unconfirmed; CLOUD-FIGURES C2) LEDGER's day stays shorter than all of them, by his choice; the evening at 6 real minutes against GTA V's about 12 is where a player will feel it, and CLK-04's windows are set so nothing is missed for it.
- Section 21's search: "looks round there for about a game hour (half a real minute at most on the spot)" becomes the search of C-03 below; under clock B a game hour is 60 real s.
Standard. As design pass 3's clock standard (1) to (3), with B's numbers; and (4) no file of the game or the giant prompt still carries 45 s, 18 real minutes, 9 weeks, "eighth game week" for the fail-safe, or "within 90 real seconds" for a chase (a text search over the prompt and the data).
Test. B: the first-hour bot, the job-window lint, three bot playthroughs; the text search.
Source. His ruling of 21 Nov (RULINGS, the 18 to 21 Nov line); design pass 3's clock table and F13; CLOUD-FIGURES C2.
Status: MEASURED for CLK-01 to CLK-05, CLK-07, 7.13 and FIT-F13 (his ruling, by guard G-A). CLK-06 MEASURED on the ruling for the calendar; its act hours are proved by the bots, and a short median comes back as a finding.

## The chase against the chase sheet (F02, F04, P13)

What the sheets show, all leads (car-chases-sheet-2026-11-21 on wip, 19 chases: GTA VI 5, GTA V 5, GTA IV 4, Sleeping Dogs 5; every number a floor at 7 to 67 s steps; uploaders' choice, so long chases are over-represented):
- Most chases ran 2 to 8 minutes; the shortest escapes, about 1 minute, came at the lowest level with sight broken early (GTA VI chase 1, GTA V chase 5).
- Escape needs sight broken and then the search outlasted. Police cars in frame were few: usually 0 or 1, at most about 4 (GTA VI).
- The sheet reads GTA IV's and Sleeping Dogs' narrow streets as the closest fit to the Hook; GTA VI's chases ran mostly on big roads and open ground. That reading is followed: LEDGER's chases are narrow-street chases through the parade's lanes and the yards, with the quays as the open stretches between.
- Searches after sight was lost: about 20 s, 50 s, 68 s and once at least 6 minutes (being-seen and chase sheets), all leads.
Solid (five uncut, dated samples): GTA VI's whole wanted spell at two stars, star lit to cleared when the player escapes by car in free roam, about 27 to 122 s, median about 47 s (g5-heat-samples, reviewed three times; four of five samples from one player). It holds the chase and the search together. A lead: a return into the pursuer's sight resumes the pursuit at the level held (four of five returns; one, iWrYrsVXTS0, added a star).

Against our design: "within 90 real seconds" (description, sections 22 and 23 and the lines at 143, 175, 242, 372 and 1255 of the prompt) is shorter than every reference chase except the lowest-level escapes, and the players' panel named the fit problem (P13: "chases feel timed and polite"). GTA VI sets the higher bar: a chase is a contest that ends by losing or being caught, never by a clock. So the bar is raised:
- C-01 The pursuit, car and foot alike. No timer. A chase ends lost (7 s unseen, or the gap over 200 m by car or 70 m on foot while unseen: design pass 3, F03), caught, wrecked, or at the soft edge (G3). The description's one patrol car stays, so pressure comes from where he waits and what he knows, not numbers. Lines that change: the prompt's "it ends within 90 real seconds" and "always ends, caught or lost, within 90 real seconds" (sections 22, 23 and lines 143, 175, 242, 372), the experience rule "every chase ends within 90 s" (line 1255) which becomes "every chase ends caught, lost, wrecked or at the edge, and none passes 4 real minutes"; in design pass 3, G1's "about one 90 s chase" becomes "one lap is one short chase", F03's "inside 90 s" becomes "in a typical chase", and the docks fallback's "car chases then shorten to 45 s" becomes "car chases then run the 910 m parade loop, shorter by about half".
- C-02 Its length. For a seeded bot that drives the loops well, a lost car chase runs a median of 60 to 120 s and the 90th percentile under 4 minutes (about two and a half laps of the 1,528 m loop at chase speed); a foot chase a median of 30 to 90 s (the ginnel and a street, F22). Below the sheet's 2 to 8 minutes on purpose: those are uploaders' chosen chases at three stars and more, on maps many times the Hook, while LEDGER's is one patrol car on a map whose loop is a lap in about 90 s; the band is a judgement until block 1's five-sample lengths, which may raise it. A bot that drives straight and never breaks sight is caught or reaches an edge, never chased past 4 minutes.
- C-03 The search after it is lost. The patrol searches the last-seen streets for 30 to 120 real s, slowly, lamp on the turnings, then waits on that road for the rest of the night as section 21 says. Seen again inside the search, the same chase resumes with what he already knows; seen after it, a new chase starts. Section 21's text "looks round there for about a game hour (half a real minute at most on the spot)" and "Seeing Tom again starts a new chase" take these words. The band is a judgement between the search leads (20 s to 6 minutes) and inside GTA VI's solid whole-spell figure; PENDING on five-sample search lengths.
Standard. (1) No chase ends while the pursuer can see Tom, except caught, wrecked or at the edge; (2) over 50 seeded chases by the good-driver bot, median lost car chase 60 to 120 s and 90th percentile under 240 s, foot chase median 30 to 90 s; (3) the search lasts 30 to 120 s in every lost chase, and a sighting inside it resumes the same chase; (4) no chase of any bot passes 240 s.
Test. B: the seeded chase set on the prototype map, chase and search lengths logged.
Source. car-chases-sheet-2026-11-21 and gtavi-being-seen-builder (leads); g5-heat-samples-m_2RP-2026-11-22 and its three reviews (solid, the whole spell); FIT-CHECK F02 to F04, F22 and P13; GTA VI YARDSTICK (being seen); design pass 3, G1, G3 and F03.
Status: C-01 DECIDED (raised by GTA VI's bar; his to overturn). C-02, C-03 and FIT-F04 PENDING on the five-sample chase and search lengths of block 1 and the feel block.

## The crowd against the counted views (GD-02, G9)

What the sheets show, all leads (lower bounds from small frames, fewer than five samples each): GTA VI's town streets about 10 at the busiest, pavements 3 to 8, quiet streets 0, night alike; its beach 10 to 18 (10 to 12 on the release-day clip), left out because the Hook has no beach crowd (G7); Sleeping Dogs' day streets 4 to 10, night about 2; Yakuza 0's day streets 0 to 3, once 9; the 1990 archive's event night 15 to 30 along the route and about 20 walkers on the shopping street, an indoor centre about 6; the archive's ordinary daytime counts are not yet read (port-towns sheet).
The design's "at least 25 distinct people in the busiest view" was a judgement figure. It is above every counted game street view, GTA VI's included, and nearer the archive's event night than an ordinary day.
- GD-02 is changed: the busiest view (Quay Street's parade front, the 100 m G9 names) at its busiest hour holds 12 to 20 distinct people. The floor of 12 sits above GTA VI's counted street views (about 10), so GTA VI's bar is met; the ceiling of 20 sits inside the archive's event-night range, kept for the match and the market. The blueprint preparation's performance budget (frame time with 25 or more people on screen) stays, so the view has headroom.
- G9's bands are rescaled to match: 05:30 to 07:00, 5 to 8; the busy bands 08:00 to 09:30, 12:00 to 14:00 and 16:30 to 18:00, 12 to 20; other daytime hours 6 to 12; 18:00 to 22:00, 5 to 10; 22:00 to 01:00, 2 to 5; 01:00 to 05:30, 0 to 2 besides the constable; the quay road by the fish dock 05:30 to 07:00, 10 to 18. Rain halves each band; Thursday's market takes a third off the shops' daytime bands; Saturday's match doubles the street at 15:00 and 17:00 for half an hour (the one time the view may pass 20, up to 30, the archive's event-night top).
Standard. (1) Counts in the parade front sampled every game hour fall inside each rescaled band in dry weather and inside half the band in rain; (2) the bands are replaced by the five-sample counts of GTA VI's and KCD2's busiest town views (KCD2 from our own recordings in the installed game) and the archive's daytime counts when solid: the higher game count sets the busy floor, the archive the ceiling.
Source. gtavi-g-rows-builder (G7), small-district, street-life and port-towns sheets (leads); design pass 3, G9 and G1; the blueprint preparation's performance budget.
Status: PENDING (the counts are leads); the bands are DECIDED in the meantime.

## Getting in and out (1.2.3): the first solid feel number

GTA VI, five parked-car entries from uncut, dated, post-release footage, door to seated 1 to 2.5 s, about 2 s typical (STATUS.md, driving; SOLID; all five from one stream and one player); a sixth agrees; a seventh, a parked SUV read at 2 s steps, gave 2 to 4 s. Section 23 allows no carjacking ("only parked cars, never a car with somebody in it", by force in about 6 s), so the carjack leads have no LEDGER part. The row's standard "in or out in under 2 s" is reset on the figure for a car Tom may open (the firm's cars, his own, an unlocked one): door to seated 1.5 to 2.5 s, moving within 1 s after; out under 2 s; a blocked door never traps him (ER-DRIVE-07). Taking a locked parked car stays at section 23's about 6 s.
Standard. Entry door to seated 1.5 to 2.5 s from both sides; out under 2 s; forced entry about 6 s; a blocked door never traps.
Test. S: timed from both sides, door blocked, a locked car forced.
Source. STATUS.md and gtavi-driving-builder-2026-11-21 (five samples, SOLID, one player); the description, section 23.
Status: MEASURED (reference game; the one-player caveat beside the number).

## What this pass did not change

The 44 parts that were undefined at run 1 were all defined in run 2 (above), red team 2's 22 in run 4; none is undefined today. GTA VI's mechanics and yardstick were mapped in full in run 2 (GTAVI-MAP-2026-11-21.md); the gtavi/ files have not changed since 20 Nov, so the map stands. The six walkthrough games' themes (44 WT rows) and the story patterns (14 SP rows) were mapped in run 2 and stand. Mods are out at release (GD-06, OUT, since run 2). Mafia appears nowhere as a reference (F04 names GTA IV).
