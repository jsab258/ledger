# Definitions for the 44 undefined parts (design pass, run 2, written 20 to 21 November 2026)

What this file is. Run 1's coverage map left 44 rows UNDEFINED: needed, not written. Each is defined here in the design's own words, inside canon, his rulings and the game description (production/lane/ONE-SHOT-PROMPT.md, cited as "the description, section n"), with a standard a checker can pass or fail and the source that standard rests on. The synthesis and the parts tree stay read only; the giant prompt of about 1 December is to be rewritten from this file and the coverage map.

How each row's new status was set:
- MEASURED: the standard is pass or fail on a ruling, canon, the description's own numbers, a public guideline (the Xbox Accessibility Guidelines, XAG; the Game Accessibility Guidelines, GAG) or a design decision recorded here. Where it is a design decision, the row's basis says so: no reference game set it, and he may overturn it.
- PENDING: defined; a number in it waits on a named, dated study.
- UNMEASURED: defined; a number in it is judgement, and MEASUREMENTS-NEEDED.md now names how and when it is measured.
- OUT: left out by his ruling.
- OUTSIDE: shipping business, not a part a player meets, judged after the prototype like the other shipping rows.

Where GTA VI sets a higher bar than the row had (production/research/lane/gtavi/YARDSTICK.md, keys Y), the definition says "raised by Y..." No GTA VI story content is used anywhere. Mafia is never a reference. Mods are out by his ruling of 22:08, 20 November.

Design decisions taken here (within canon and his rulings; recorded so he can overturn any): no achievements at release (10.7); photo mode from the pause menu only (6.8); a fail-safe that brings Act III after eight game weeks of Act II (RT-04); Tom will not give an order that hurts anyone his line covers (RT-09); rung 3 and 4 thresholds (RT-04); the War trigger (RT-12); the missed-rent ladder (RT-16); the three pots (RT-17); the Ledger and map do not stop the clock (RT-18).

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
Standard. GAG basic and XAG 104: all five options present; first screen offers them; no subtitle without its audio; no subtitle shown under 1 s.
Test. B: every line played in a 2-hour soak logged with its subtitle on and off times.
Source. GAG (subtitles), XAG 104; the description, section 3; ruling 23 Sep (subtitle only with its audio).
Status: MEASURED.

### AX-03 Motion and comfort settings
Definition. Each motion effect has its own switch: camera shake (the hit shake and the car's), head bob, motion blur, the brief camera close-in on a landed blow, and depth of field. The field of view can be set from 75 to 100 degrees; the default stays the ruled 86 degrees, and the car camera follows the same offset. A "reduce flashing" switch dims muzzle flashes and lightning, beside the photosensitivity line the description already shows.
Standard. XAG 117 and GAG: every listed effect can be turned off alone; field of view range present with 86 as default; flashing reduced below three flashes a second when switched.
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
Standard. XAG 107 (input), 110: all items present; the game completes the first hour with every hold set to tap and on pad alone.
Test. B: the first-hour bot run with all toggles on, pad only; a rebind of every key with no conflict left unflagged.
Source. XAG 107, 110; GAG; the description, section 3 (controls); Y1.9.
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
Source. The description, section 3 (saving); ER-SAVE-01; XAG 112 (save clarity); PC players' expectation from the players study (bugs and broken saves punished).
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
Status: MEASURED.

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
Definition. "Report a problem" in the pause menu (with 8.2.1's consent), one support address in the menus and on the store page, the Steam forum as the community place, and a known-issues page kept current by the release team. Any live line can already be reported (section 34). A report gets an automatic reply naming what was received.
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
Standard. Things per street minute within the band the teardown's town pieces show (to come); at least 25 distinct people in the busiest view of the Hook at its busiest hour (judgement until the footage pass counts GTA VI's and KCD2's); no shared street line heard twice in one real hour (raised from the description's "a shared line once a week per street", which allowed repeats across streets).
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
Standard. The players study punishes money with nothing to buy (GTA V and RDR2 late game). Pass: in a bot playthrough at a fast pace, the spare money at the end of each Act II week never exceeds the price of the next named purchase on the rung ladder; numbers from the reference games' money over a playthrough.
Test. B: an economy bot playing greedy and lazy; the curve plotted against the rung ladder.
Source. The description, sections 24, 28, 31, 32; MEASUREMENTS-NEEDED A (money over a playthrough); PLAYERS-KCD2-GTAV-RDR2 complaints.
Status: PENDING (PC measuring, 23 to 28 Nov).

### GD-08 The catalogue of jobs and stories per act
Definition. Every job has a named giver, a place by landmark, an hour, at least two ways to do it, and a return (somebody tells it back). Kinds: carries, collections, break-ins, lifts, tails, minding, fares with a wrinkle, sit-downs, and from Act II the eight sent verbs. Act II has no dead weeks (a rival rung, a firm change and a return every week).
Standard. Jobs per real hour and kinds per act inside the band the teardown and the reference games' mission counts show; no kind twice in a row (ER-JOB-06).
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
Definition. Each of Act II's eight beats (the description, section 37) has a written scene: who, where, what is at stake, what the player can choose, what comes back. The old firm's hand-over names three things handed over (the landing, its men, its night custom); Mickey's real book holds the arrangements and debts Tom can take up (at least five new names); the envelopes of nights five and seven carry what the measured story says; the collision is written for each pairing of a day appointment and a night job the state allows.
Standard. Every beat has its scene; every scene names at least one choice and one return; none needs a system the game lacks.
Test. Trace check: beat to scene to system (TRACE style), by a fresh reviewer.
Source. The description, section 37; the story measure's bible (current version STORY-BIBLE-M1).
Status: PENDING (story measure, by Sat 28 Nov).

### RT-03 Job and mission catalogue after week one
Definition. As GD-08 for kinds and counts, plus places: the dock gate (Act II from rung 3: tax collected on his drivers, a man posted, smuggled loads seen), the Harbour Board's counter (an account, a clerk who sells times of shipments), customs (an officer who never reports, by trade; the bonded store as a place of risk).
Standard. Each place has at least two jobs and one person with a word; counts as GD-08.
Test. Catalogue count; bot visits each place and finds something to do within 30 s (section 40).
Source. The description, sections 14, 28, 29, 40; the story measure.
Status: PENDING (story measure and PC measuring, by Sat 28 Nov).

### RT-04 Act transitions and stall paths
Definition. Act II opens on the Monday of the second week whatever Sunday's answer was: "wind it down" opens it with the arrangement ended, "take it over" with it kept, and "refuse to say" lets the street decide by his deeds (more night jobs done than refused in week one counts as kept). Rung 2 comes with Sheila's answer, or, if he refused, with the third car or the first recruit, whichever first. Rung 3 when he holds four of the five things in the rung table (five cars, a night desk, a first front, a first round, the cold-store contract); rung 4 when he holds at least two fronts and two rounds and has men at two of the three places (the dock gate, the cold store, the landing). If Act II never reaches a sit-down, the inspection letter comes at the end of the eighth game week of Act II all the same (the description puts Act II at about seven), so no player is stuck in Act II.
Standard. Every Sunday answer reaches Act II; every Act II reaches Act III by week eight; rung changes fire exactly on these conditions.
Test. B: three week-one bots (each answer) and a do-nothing Act II bot; the act and rung log checked.
Source. The description, sections 32, 36, 37, 38 (Act II about seven weeks); ER-CORE-04 (no dead end).
Status: MEASURED (design decision, pass or fail).

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
Definition. If someone his line covers attacks him, Tom guards, slips and backs off; the strike input does nothing and he says so. In a fight that includes them, he can strike only the others; a grab of their weapon is allowed. Tom will not give a send that hurts a person his line covers: the order is refused in his own words. A rival's men are not bound by his line.
Standard. Zero strikes by Tom or his sent men on anyone covered, in any fight, hold-up or send.
Test. B: seeded fights and sends including covered people; any such strike fails.
Source. The description, section 10 (Tom's own line); RULINGS (the line); the conflicts note on hold-ups.
Status: MEASURED (design decision within his ruling).

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
Definition. Fired moves to War when the town learns of either: a second shooting by a different side from the first (two firms have now fired), or a named man of one firm wounded or killed by a shot from another. Tom arming more than two of his own men also moves it, because the town learns who carries. Nothing moves it that nobody saw or heard. It falls one step after about two quiet game weeks, never back to 0.
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
Definition. Rent is owed to the landlord's agent, a named man who calls at the counter. A missed Friday becomes arrears said in words in the Ledger and by the agent on Monday. Two missed: a letter, notice to quit the flat above in a fortnight. Three: the flat is let to someone else and Tom sleeps in the office. The office itself is never lost in Act I, and arrears can be paid at any time, which ends the ladder. No game over, no dead end.
Standard. Each step on its Friday; paying clears it; the office never lost before Act III.
Test. B: the do-nothing run through three Fridays; a pay-late run.
Source. The description, sections 24 (rent), 3 (no game over); the doing-nothing run of S23.
Status: MEASURED (design decision).

### RT-17 Money pots in practice
Definition. Three places money is: the pocket (cash on Tom), the tin (night money at the office) and the book (clean money). Rent, drivers' wages, buying a car and a front's share come from the book. Bribes, men's cuts, the fence, the doctor and the shops come from cash, from the pocket or the tin. Cash moves between pocket and tin by hand at the office; the book becomes cash only through the count. The tin can be stolen in an office break-in (a rival's threat, or a thief) and is then gone, said in words. A constable's search finds the pocket; over about £50 on him at night is asked about and, without an answer, kept.
Standard. Every payment draws from the right place; the flows ledger balances (ER-MONEY-01).
Test. B: every kind of payment from each place; a break-in; a night search with cash.
Source. The description, sections 21, 24, 26, 27.
Status: MEASURED (design decision).

### RT-18 Pause and clock
Definition. The clock stops in talk (section 34) and in the pause menu, and nowhere else. Opening the Ledger, the paper map or a letter stops Tom but not the town, as the description already says of the map: KCD2's immersion. Getting ready takes a game minute, never a screen. An assist "the Ledger pauses the town" is offered, off by default.
Standard. Clock frozen only in talk and pause (and with the assist on, in the Ledger); time passes at the clock rate otherwise.
Test. B: clock read before and after each screen.
Source. The description, sections 24, 27, 34; KCD2's open journal does not stop the world [I].
Status: MEASURED (design decision).

### RT-19 Content supply at night and late in Acts II and III
Definition. Street happenings are authored (ruling 13 Nov), each with a spec and a check, never rolled at random. Nights without a job hold: a fare with a wrinkle on the radio, a rival's man seen, a crewman with a problem, a happening on the street, a call on someone whose routine allows it. Never five minutes with nothing new (S41); by day something within 30 real seconds (section 40).
Standard. The library holds enough happenings that none repeats on one street within a game week; the count per hour inside the teardown's band (GD-02).
Test. B: a do-nothing-but-walk night in Act II and in Act III: the five-minute rule and the repeat rule logged.
Source. The description, sections 40, S41; ruling 13 Nov; MEASUREMENTS-NEEDED A (density).
Status: PENDING (PC measuring for the band, 23 to 28 Nov; the story measure for Act III's nights, by Sat 28 Nov).
