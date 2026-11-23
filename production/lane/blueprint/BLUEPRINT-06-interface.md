# BLUEPRINT 06: The interface and the Ledger

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. What is on screen: almost nothing, plus Tom's notebook and a paper map.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 6.1 On screen in play

The minimal screen.


### 6.1.1 The prompt

- How it works: The prompt names the person ahead and in view, or what he can use, held 0.2 s before it changes. When two things share a key one prompt asks which, and a person with something to say is offered before a door. Every door, stair and person he walks up to has a prompt, and with two usable things in reach the wrong action never fires; a tester presses the key 500 times in crowded spots and counts misfires (pass: zero).
- Standard: ER-INPUT-02: held 0.2 s; everything usable has one. Raised by Y1.8 (GTA VI fails it): with two usable things in reach the wrong action never fires; a tester walk presses the key 500 times in crowded spots and counts misfires (pass: zero). Test: H: walk-up sweep
- Source: DESIGN §17 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §17 ER-INPUT-02; DESCRIPTION-2 §3; GTAVI-MAP-2026-11-21 Bars raised (Y1.8); PARTS-TREE 6.1.1
- Status: decided. Coverage row: 6.1.1.

### 6.1.2 Subtitles

- How it works: A subtitle appears only with its audio (ruling 23 Sep), large and never under 24 units, with no overlap at four window sizes. It stays for its line plus 0.3 s, size has three steps, background box off, half or full, speaker's name on by default, and street chatter subtitles can be switched off. Subtitles are on by default and offered before the first sound.
- Standard: A subtitle shows only with its audio (ruling 23 Sep); nothing under 24 units; no overlap at four window sizes (ER-SCREEN-02) Test: S: layout test at four sizes
- Source: RULINGS; DESIGN §17 (his ruling or canon). Designed in: RULINGS 23 Sep; DESIGN §17 ER-SCREEN-02; DEFINITIONS-2026-11-21 §AX-01, §AX-02; PARTS-TREE 6.1.2
- Status: measured. Coverage row: 6.1.2.

### 6.1.3 The belief line

- How it works: A line low on screen says when Tom comes to believe something new, for example 'Ada saw you at the yard gate, he thinks'. Every perceivable change is shown by the world within 3 s and written in the Ledger within a game minute. It is in words with no icon and no meter.
- Standard: Within 3 s of a perceivable change (ER-CORE-02) Test: S: trigger each perceivable change
- Source: DESIGN §10, §1 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §10, §1 ER-CORE-02; DESCRIPTION-2 §3; PARTS-TREE 6.1.3
- Status: decided. Coverage row: 6.1.3.

### 6.1.4 Light and sound cues

- How it works: The picture's corners darken and lift with the same light value the watchers use (daylight 1, lamp 0.7, unlit street 0.25, doorway 0.12); the cue is darkness at the frame's corners, no meter. It must be readable under simulated protanopia, deuteranopia and tritanopia.
- Standard: Cue matches the rule's light value (DESIGN §2) Test: H: ER-EYES-01 with the cue off and on
- Source: DESIGN §2 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2; DESCRIPTION-2 §3; DEFINITIONS-2026-11-21 §AX-11; PARTS-TREE 6.1.4
- Status: decided. Coverage row: 6.1.4.

### 6.1.5 Knowing the time

- How it works: There is no screen clock. N raises Tom's watch and the hour shows for 2 s; the clock over the Harbour Board and the office clock tell it, and the chapel bell strikes the hours by day. The hour can be known within 3 s anywhere. A game hour is 60 real seconds, so a game day is 24 real minutes.
- Standard: The hour known within 3 s anywhere (ER-TIME-01); no timers on screen (ruling 23 Sep) Test: S: the watch glance; H: 'what time is it?'; addendum rules ER-TIME-01
- Source: rulings; addendum (his ruling or canon). Designed in: ADDENDUM §A31; ONE-SHOT-PROMPT §8; RULINGS 21 Nov; DEFINITIONS-2026-11-21 The clock (version B); PARTS-TREE 6.1.5
- Status: measured. Coverage row: 6.1.5. Conflicts settled: C-120.

## 6.2 The Ledger notebook

Tom's notebook of people and events: the one place he sees where he stands.


### 6.2.1 People

- How it works: People holds what Tom knows of each person and what he believes they know of him, with how sure: said to his face is sure, saw them looking is 'thinks so', two heads together is 'guesses'. Tom's guess of what each holds of him is shown slot by slot in words, never icons. Any person is found in three inputs.
- Standard: Sure, thinks so, guesses by how learned (DESIGN §10). Raised by Y2.2: Tom's guess of what each person holds of him, slot by slot, in words (GV-02). Test: S: no entry without a source event
- Source: DESIGN §10 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §10 ER-LEDG-02; GTAVI-MAP-2026-11-21 GV-02; DESCRIPTION-2 §20; PARTS-TREE 6.2.1
- Status: decided. Coverage row: 6.2.1.

### 6.2.2 Day book

- How it works: The Day book lists events in order, each job step done or failed a line of about 22 words. Nothing is erased; a wrong belief is struck through with the day and the reason. Every entry traces to something Tom saw, heard or was told.
- Standard: ER-LEDG-01 Test: S: struck through, never removed
- Source: DESIGN §10 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §10 ER-LEDG-01, §4; DESCRIPTION-2 §20; PARTS-TREE 6.2.2
- Status: decided. Coverage row: 6.2.2.

### 6.2.3 Open

- How it works: Open lists jobs, debts, promises and appointments, each naming a person and a landmark, and what Tom carries, in words. A newcomer can answer 'what next, and where' from it alone, and every go-to step names its place by landmark.
- Standard: ER-LEDG-03; ER-JOB-01 Test: H: 'what next, and where' from the Ledger alone
- Source: DESIGN §10, §4 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §10 ER-LEDG-03, §4 ER-JOB-01; DESCRIPTION-2 §20; PARTS-TREE 6.2.3
- Status: decided. Coverage row: 6.2.3.

### 6.2.4 Money in words

- How it works: Money is said in words, for example 'Thirty-one pounds in your pocket. The tin has about forty. Rent, eighteen, Friday. Darren still owes twelve.' He always knows what he has and what is owed by Friday; Tom starts with 23.50 and the rent is 18 each Friday. A week of Tom's own fares pays it; doing nothing misses it.
- Standard: ER-MONEY-02 Test: H: asked what he has
- Source: DESIGN §9 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §9, §10 ER-MONEY-02; DESCRIPTION-2 §20; DEFINITIONS-2026-11-21 §G8; CLOUD-FIGURES-2026-11-21 B1
- Status: decided. Coverage row: 6.2.4. Conflicts settled: C-121.

### 6.2.5 Tom's reading

- How it works: On Full stop, and at each act's end, the Ledger gives Tom's reading: how things stand as he sees them, built only from the signs he was given, never the true state. A player who reads it can say how the game will end and why. No ending lands while his own reading says things are quiet.
- Standard: ER-END-02, 03 Test: H predicts the ending from it
- Source: DESIGN §10, §16 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §10, §16 ER-END-02, ER-END-03; DESCRIPTION-2 §33; RULINGS 28 Sep; PARTS-TREE 6.2.5
- Status: decided. Coverage row: 6.2.5.

## 6.3 The paper map

A map of the Hook that marks only places he has been or been told of.


### 6.3 The paper map

- How it works: The paper map is a drawn map of the Hook, not a list, marking only the places Tom has been or been told of; opened with Comma it stops Tom but pauses nothing. There is no minimap, and street-name plates sit at street ends. In the prototype it draws the whole town with no gating.
- Standard: No minimap (D37); only known places Test: S: no unknown place marked; H: finds a told place
- Source: D12, D20, D37; DESIGN §10 (his ruling or canon). Designed in: RULINGS D27, D30 (no minimap; a paper map and street signs); DESIGN §10; ADDENDUM §A9; PARTS-TREE 6.3
- Status: measured. Coverage row: 6.3.

## 6.4 Menus

Title, pause, settings, save and load, credits.


### 6.4 Menus

- How it works: Menus are title, pause, settings, save and load, credits. It starts from its shortcut, shows progress while it prepares, opens at a sensible size, offers quality presets and New game, Continue and Quit. Esc pauses everywhere and no destructive choice sits one press from Resume. Saves: at least eight manual slots with picture, day, hour, place and rung, three rotating autosaves, written to a new file and swapped in once complete.
- Standard: ER-START-01; ER-SAVE-02 (Esc pauses everywhere, no destructive choice one press from Resume) Test: S and B: pause, continue, quit on every device
- Source: DESIGN §17; basics 1 to 5, 19 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §17 ER-START-01, ER-SAVE-02; DEFINITIONS-2026-11-21 §AX-06, §AX-07, §AX-10; PARTS-TREE 6.4
- Status: decided. Coverage row: 6.4.

## 6.5 Teaching the player

Hints on first need or hesitation, each once; the interface appears piece by piece.


### 6.5 Teaching the player

- How it works: A hint fires only the first time it can mean something or when the player hesitates, each once and never on the clock, never two within 12 s. At the quay a hint comes after standing still for 4 s, and Ron or Pauline nudge after a minute of standing about. The interface appears piece by piece as each part is first used, and 'hints again' brings them back from the Ledger.
- Standard: ER-FIRST-03: never two hints within 12 s; never on the clock Test: S: idle test
- Source: DESIGN §15 (no reference figure yet). Designed in: DESIGN §15 Teaching, ER-FIRST-03; ONE-SHOT-PROMPT §4; DESCRIPTION-2 §3; PARTS-TREE 6.5
- Status: unmeasured. Coverage row: 6.5.

## 6.6 Controls

Keyboard with mouse and a pad each drive everything; rebinding.


### 6.6 Controls

- How it works: Keyboard with mouse and a pad each reach every verb and prompts follow the device last used. Every action answers within 100 ms, a press 100 ms early still counts, keys can be rebound per device with reset, and every hold has a toggle. Fixed keys include Z slow, M manners, B sit, N watch, O stone, I torch, Comma map, Full stop reading, Tab suggested lines; the first hour must complete on pad alone.
- Standard: ER-INPUT-03; ER-INPUT-01 Test: S: the same scripted evening by each device
- Source: DESIGN §17 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §17 ER-INPUT-01, ER-INPUT-03; DESCRIPTION-2 §3; DEFINITIONS-2026-11-21 §AX-05; PARTS-TREE 6.6
- Status: decided. Coverage row: 6.6.

## 6.7 Talk screen

Typing, suggested lines, the game's own decision lines, Leave always there.


### 6.7 Talk screen

- How it works: The player types or picks suggested lines (Tab on a keyboard, shown at once on a pad; about 4 words each); every decision is the game's own yes or no, only a plain yes is taken, and what cannot be undone asks twice. Typing never moves Tom, the clock stops in talk, Leave is always offered, and no talk scene runs 60 s without a choice or control. Each typed line is read into one act (offer, threat, promise, claim and so on).
- Standard: ER-TALK-03, 05, 06 Test: S: typing never moves Tom; Leave always offered
- Source: DESIGN §11 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §11 ER-TALK-03, ER-TALK-05, ER-TALK-06; DEFINITIONS-2026-11-21 §RT-14; RULINGS 1 Oct; PARTS-TREE 6.7
- Status: decided. Coverage row: 6.7.

### RT-14 Typed-talk interpretation

- How it works: Each typed line is read into one act: question, agree, refuse, offer, threat, promise, claim, insult, small talk or leave. An offer's amount is read exactly ('a tenner' is 10 pounds), an offer above what Tom carries fails in character, and offers, threats, promises and lies are acts the hearer remembers. The bar is a 300-line labelled set (period, modern, terse and misspelt; 65 hard): the reader's act matches the label or an allowed alternative on at least 95% of all lines and 90% of hard lines. Two blind human labellers agreed 295 of 300 (98.3%).
- Standard: On the labelled set typed-talk/RT14-SET-2026-11-21.jsonl (300 lines, period, modern, terse and misspelt, 66 hard), the reader's act matches the label or an allowed alternative on at least 95% of lines and 90% of hard lines; every amount read exactly; every offer, threat, promise and lie enters the hearer's memory. Test: A labelled set of 300 lines (period and modern phrasing) run through the reader; memory checked after each.
- Source: typed-talk/README.md and agreement-2026-11-21.json: two blind labellers agreed 98.3% (kappa 0.98), hard lines 63 of 65, amounts 28 of 28 (real-world figure or published standard). Designed in: DEFINITIONS-2026-11-21 §RT-14; typed-talk/README.md and agreement-2026-11-21.json; DESCRIPTION-2 §28
- Status: measured. Coverage row: RT-14. Conflicts settled: C-122.

## 6.8 Photo mode

Optional presentation: a free camera to take pictures, off the play path.


### 6.8 Photo mode

- How it works: From the pause menu only, Photograph freezes the town and frees the camera within 10 m of Tom and never through a wall, body or car. All interface is hidden; the player can tilt, roll, set the lens from 24 to 85 mm, focus and exposure, and save a picture at the window's size; no posing, filters, stickers or text. Leaving returns the frozen moment exactly (save hash equal).
- Standard: (1) Reachable only from pause; (2) camera never more than 10 m from Tom and never inside geometry; (3) no interface element in a saved picture; (4) the town state after leaving equals the state before (save hash). Test: B (bot): 200 random photo-mode sessions with clip detector and before and after save hashes; S: a saved picture has no interface pixel.
- Source: Ruling 23 Sep (optional presentation allowed); the camera rule; GTA V and RDR2 photo modes as the common PC expectation [I: widely known, not measured here]. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS-2026-11-21 §6.8; DESCRIPTION-2 §35; RULINGS 23 Sep (genre)
- Status: decided. Coverage row: 6.8. Conflicts settled: C-123.

## 6.9 Finding the way

Addresses, house numbers, street-name plates, passengers' 'left here', asking a stranger, a nudge when lost.


### 6.9 Finding the way

- How it works: Every door that matters has a number and every street a name plate at its ends; jobs, fares and letters give an address and a landmark. Asked the way, people give it by landmark or say 'no idea, try the caff'; in the car a fare says 'left here' a junction before, and Pauline repeats the way on R. Lost for 90 s, Tom's own line repeats the landmark once; after three minutes the next person within 5 m offers the way. A newcomer reaches ten named places unaided within 3 minutes each.
- Standard: A newcomer reaches a named place unaided within 3 minutes (ER-JOB-01); no markers (ruling 23 Sep) Test: H: ten named places reached unaided; S: every place has an address and a landmark; addendum rules ER-WAY-01 to 03
- Source: DESIGN §4; rulings (his ruling or canon). Designed in: ADDENDUM §A9; DESIGN §4 Guidance, ER-JOB-01, ER-DRIVE-09; PARTS-TREE 6.9
- Status: measured. Coverage row: 6.9.

## 6.10 Letters and papers in hand

Things to read: the paper, Agar's solicitor's letters, the VAT letter, notes, posters.


### 6.10 Letters and papers in hand

- How it works: The local paper comes out twice a week and carries what Alison Sedman knows and chose to write; a story about Tom is only as sure as what she was told. Letters (the solicitor's from Agar's side, the VAT letter in Act III, notes left at the office) open on screen as a page and go into the Ledger; no real people, events or brands are in print, and every printed line traces to what Alison saw or was told.
- Standard: Nothing Tom could not know on screen (ER-SCREEN-01) Test: S: each letter opens and goes in the Ledger
- Source: DESIGN §17 (DECIDED by the design proof, for him to overturn). Designed in: ADDENDUM §A19 ER-PAPER-01; DESCRIPTION-2 §5; DESIGN §17 ER-SCREEN-01
- Status: decided. Coverage row: 6.10.
