# BLUEPRINT 08: Technical

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. Runs well on his PC and on players' PCs.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 8.1 Performance

Smooth play.


### 8.1.1 Frame, memory and crowd budget

- How it works: The only set figures: 60 frames a second at 3440 by 1440 on the RX 6700 with the voice running, never under 30, in rain and at night; the packaged walk draws at a fixed 55% and upscales; the 6 GB card line is for the game alone for now; the day's spare card time of 1.7 ms is accepted and revisited in phase 2. Study 12 gives LEDGER a median frame of 16.7 ms, worst 25 ms, ceiling 33.3 ms. People in full detail, a draw distance and shadow lights per frame have no value yet; Study 12 proposes freezing people unseen for 3 s beyond 70 m (never within 10 m), a 3 ms animation budget, a people update near 3.5 ms, and 8 shadow lights a frame as first caps, none adopted.
- Standard: 6 GB card line is the game alone (24 Oct); spare card time 1.7 ms Test: S: budget table per build
- Source: RULINGS 24 Oct; study 12 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 23 Sep, 24 Oct; DESIGN §17 (ER-PERF-01); Study 12 (production/research/aaa-reference/studies/12-tech-budgets.md); RECS-BY-PHASE s12-03
- Status: outside. Coverage row: 8.1.1. Conflicts settled: C-145.

### 8.1.2 Streaming and loading

- How it works: Named only; not designed beyond: no load time or hitch limit is set. What exists is the map size (the Hook and docks about 620 by 400 m), the rule that a trip past the soft edge is a time skip with nothing loading or failing on screen, and ER-PERF-01's floor of 30 frames. Study 4 only records how reference towns stream (Mafia 73 cells of 128 m; Kingdom Come II streams about 49,000 entity records).
- Standard: none yet: load and hitch limits to be set Test: S: hitch count on a scripted drive
- Source: study 04, 12 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: Study 4 (04-street-world.md); DEFINITIONS G3; DESIGN §17 (ER-PERF-01); COVERAGE row 8.1.2
- Status: outside. Coverage row: 8.1.2.

### 8.1.3 Player PCs and shader stutter

- How it works: Named only; not designed beyond: shader stutter is to be fixed by Unreal's PSO precaching (researched in frame-headroom PSO-AND-VRAM-METHOD, 23 Oct, from Epic's 5.8 documentation: hold the first loading screen until precache work is done). The packaged first launch already shows 'Getting the street ready for this PC's graphics card' with progress (5 Oct). No minimum machine or scaling steps are set; the preset ladder Low, Medium, High exists with only High measured.
- Standard: Epic's PSO precaching for shader stutter; minimum spec to be set Test: S: hitch count on first run of a clean install
- Source: Epic tech blog on shader stutter (red team source) (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COVERAGE row 8.1.3; frame-headroom/PSO-AND-VRAM-METHOD-2026-10-23; production/friends-build/MAP.md (basics 2 to 4); Study 12
- Status: outside. Coverage row: 8.1.3. Conflicts settled: C-146.

## 8.2 Stability and saves that never break

No crashes, no corrupt saves, long sessions safe.


### 8.2.1 Crash and bug reporting

- How it works: After a crash the game has written a local report (build, time, last 200 log lines, a hardware summary with no serial, machine id, user name or named path) and asks once on the next launch whether to send it, saying what is sent, why, to whom and how long it is kept. Yes, No, Always and Never are equal in size and place, the default is No, no save goes unless ticked, typed talk is never in it, and nothing is read or sent before the yes. An unsent report is deleted after 30 days; 'Report a problem' in the pause menu writes the same report plus the player's own words. The choice can be changed in Settings, and a forced crash while writing the report must not crash.
- Standard: (1) Nothing leaves the PC without a yes, and nothing is read or sent before it; (2) the question says what is sent, why, to whom and how long it is kept; No and Never as easy as Yes and Always; withdrawable in Settings; (3) the report contains no typed talk, no save unless ticked, no serial, machine id, user name or named path; (4) an unsent local report is deleted after 30 days; (5) the game never crashes while writing its own report (a forced crash test). Test: B: forced crashes x 50 with traffic capture; no outbound packet without consent; report contents checked against the list.
- Source: PRIVACY-CHECK-2026-11-21.md: ICO storage and access guidance (13 May, 29 Apr 2026), ICO blog 11 Sep 2025; consent route as fault reports are not strictly necessary (real-world figure or published standard). Designed in: DEFINITIONS 8.2.1; PRIVACY-CHECK-2026-11-21 (the four points added); GAME-DESCRIPTION-COPY-2 §35
- Status: measured. Coverage row: 8.2.1. Conflicts settled: C-147.

### GV-05 Bugs at release

- How it works: The release build has no blocking fault: never stuck, no lost save, no crash in a whole evening. Pass: three nights running the AI tester's whole-evening and whole-week walks in the packaged build find zero blocking faults and zero crashes. The bar was raised because players punish bugs and ports most (GTA IV port 25.9% and bugs 12.7%, Forza Horizon 4 port 22.0%) while critics found almost none in GTA VI.
- Standard: Three nights running, the AI tester's whole-evening and whole-week walks in the packaged build find zero blocking faults and zero crashes. Test: The nightly tester walk, three nights in a row before the gate is called.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP-2026-11-21 GV-05, Y8.2; YARDSTICK.md Y8.2; DESIGN §4 (ER-CORE-01)
- Status: decided. Coverage row: GV-05. Conflicts settled: C-148.

## 8.3 Settings

Graphics, audio and controls settings, presets.


### 8.3.1 PC display options

- How it works: The settings offer resolution including 21:9 at 3440 by 1440; windowed, borderless and full screen; V-sync; a frame cap of 30, 60, 120 or none; a quality preset with per-option overrides; a resolution scale; an upscaler where the engine has one; motion blur off by default; and a benchmark or a settings preview. Field of view is a setting from 75 to 100 degrees with 86 the default. HDR is judged with Unreal. The first launch finds a picture the PC can keep smooth, then offers presets, brightness and scale.
- Standard: Resolution incl. 21:9 at 3440x1440; windowed, borderless, full screen; V-sync; frame cap 30/60/120/none; a quality preset with per-option overrides; resolution scale; an upscaler where the engine has one; motion blur off by default; a benchmark or settings preview; HDR and field of view judged with Unreal (field of view his point AX-03) Test: S: each option applies
- Source: CLOUD-FIGURES-2026-11-21.md C3: RDR2 PC options (Shacknews 19 Nov 2019; PC Gamer 30 Dec 2019); sources/a11y-pc.json (reference game). Designed in: CLOUD-FIGURES C3; RULINGS 28 Oct camera line (21 Nov edit); DEFINITIONS 'Design pass 3' preamble (AX-03); DESIGN §17 (ER-START-01); friends-build MAP basics 2 to 4
- Status: measured. Coverage row: 8.3.1. Conflicts settled: C-149.

## 8.4 Accessibility

Text, hearing, motor and cognition options.


### 8.4.1 Visual stand-ins for sound cues

- How it works: Sound shown, an assist off by default for deaf and hard-of-hearing players: a short word at the screen's edge when Tom makes a loud noise ('door forced', 'glass', 'running on cobbles'), when the street goes quiet, or when a shout or a car is heard. It shows what Tom hears and never what anyone knows or thinks, and no ring, gauge or other measure is drawn. With only this assist on, every other measure is unchanged.
- Standard: ER-SND-01's information reachable without sound, never as a meter of others' minds (D33) Test: H: ER-EYES-01 with sound off and the option on; addendum rules ER-ASSIST-01
- Source: DESIGN §17; D33 (his ruling or canon). Designed in: DESIGN-ADDENDUM §A6 (ER-ASSIST-01); GAME-DESCRIPTION-COPY-2 §3; DESIGN §17 (ER-SND-01); DESIGN-ADDENDUM §A6 (D33)
- Status: measured. Coverage row: 8.4.1.

### AX-01 Text and interface size, contrast and font

- How it works: All text (prompts, subtitles, the belief line, the Ledger, menus) is at least 24 units (24 px at 1080p) and scales from 100% to 200% in Settings without overlap or leaving the screen at any window size. Body text has at least 4.5 to 1 contrast against what is behind it; subtitles have an optional background box. One plain face and no all-capitals body text. Checked by screenshots at 100, 150 and 200% at 1280 by 720, 1920 by 1080 and 3440 by 1440, and by contrast measured on 50 frames by day, night and rain.
- Standard: XAG 101 (text display) and 102 (contrast): text at 200% never clipped; contrast at least 4.5 to 1 measured on 50 frames by day, night and rain. Test: S: screenshots at 100, 150 and 200% at 1280x720, 1920x1080 and 3440x1440; contrast measured by script on the subtitle and prompt regions.
- Source: XAG 101, 102 (sources/a11y-pc.json); the description, section 3 ("nothing under 24 units"); GTA VI's text size setting (Y1.9). (real-world figure or published standard). Designed in: DEFINITIONS AX-01; sources/a11y-pc.json (XAG 101, 102); GAME-DESCRIPTION-COPY-2 §3, §35; DESIGN §17 (ER-SCREEN-02)
- Status: measured. Coverage row: AX-01. Conflicts settled: C-150.

### AX-02 Subtitle options

- How it works: Subtitles are on by default and offered on the first menu before any sound. Four options: size (three steps), background box (off, half, full), the speaker's name (on by default for named people) and street-chatter subtitles on or off. A subtitle appears only with its audio and stays for the line plus 0.3 s. Tested by logging every line in a 2-hour soak with subtitle on and off times.
- Standard: GAG basic and XAG 104: the four options (size, background box, speaker's name, street chatter) present; the first screen offers them; no subtitle without its audio; every subtitle stays for its line plus 0.3 s. Test: B: every line played in a 2-hour soak logged with its subtitle on and off times.
- Source: GAG (subtitles), XAG 104; the description, section 3; ruling 23 Sep (subtitle only with its audio). (real-world figure or published standard). Designed in: DEFINITIONS AX-02; sources/a11y-pc.json (XAG 104, GAG); RULINGS 23 Sep
- Status: measured. Coverage row: AX-02.

### AX-03 Motion and comfort settings (shake, bob, blur, field of view, background movement)

- How it works: Each motion effect has its own switch: camera shake (hit and car), head bob, motion blur, the brief camera close-in on a landed blow, and depth of field. A 'reduce flashing' switch dims muzzle flashes and lightning to under three flashes a second, beside the photosensitivity line shown once guns flash. Field of view is a setting from 75 to 100 degrees, default 86.
- Standard: XAG 117 and GAG: every listed effect can be turned off alone; flashing reduced below three flashes a second when switched. Test: S: each switch toggled and the frames checked; a flash-rate script on a gunshot clip with the switch on.
- Source: XAG 117, GAG (motion); ruling 28 Oct (86 degree lens); GTA VI's settings list (Y1.9). (real-world figure or published standard). Designed in: DEFINITIONS AX-03 and Design pass 3 preamble; RULINGS 28 Oct camera line (21 Nov edit); sources/a11y-pc.json (XAG 117); LOG.md 21 Nov
- Status: measured. Coverage row: AX-03. Conflicts settled: C-151.

### AX-04 Audio options (separate sliders, mono, speech clarity)

- How it works: Five sliders (master, voices, effects, the street, music) each 0 to 100, a mono switch, a 'voices clear' switch that lifts voices over the street by 6 dB, and a 'loud noise softening' switch that clips gunshots and explosions to the level of a door slam. The sound-shown assist stays. Each control changes only its own bus, checked with level meters at 0 and 100.
- Standard: XAG 105: five sliders, mono, voices clear and loud noise softening present and each changes only its own thing. Test: B: level meters on each bus with each slider at 0 and 100.
- Source: XAG 105, GAG (audio); the description, section 3 (sound shown); Y1.9. (real-world figure or published standard). Designed in: DEFINITIONS AX-04; sources/a11y-pc.json (XAG 105); GAME-DESCRIPTION-COPY-2 §35
- Status: measured. Coverage row: AX-04. Conflicts settled: C-152.

### AX-05 Input options beyond the rebinding and toggles already in the description (reset to defaults, separate mouse and pad sensitivity and invert, no mashing)

- How it works: Every action is rebindable on keys and on the pad with 'reset to defaults' per device; mouse and stick sensitivity are set separately for X and Y, with invert per axis per device. Every hold has a toggle and a 'hold becomes tap' switch, and no action needs repeated pressing (mashing in fights is something the breath rule punishes, never a requirement). Once guns exist an aim-assist strength has three steps (off, light, strong) and the dot stays optional and off. Pass: the first hour completes with every hold on tap, on pad alone.
- Standard: XAG 107 (input): all items present; the game completes the first hour with every hold set to tap and on pad alone. Test: B: the first-hour bot run with all toggles on, pad only; a rebind of every key with no conflict left unflagged.
- Source: XAG 107; GAG; the description, section 3 (controls); Y1.9. (real-world figure or published standard). Designed in: DEFINITIONS AX-05; sources/a11y-pc.json (XAG 107); GAME-DESCRIPTION-COPY-2 §3
- Status: measured. Coverage row: AX-05.

### AX-06 Menu usability (large stationary targets, back goes one level, focus visible, settings before play and from pause, all remembered)

- How it works: Menu targets are large and never move; Back always goes one level up and never quits; the focused item is always visible; Settings are reachable before play and from pause; every setting is remembered and survives an update; nothing destructive sits one press from Resume. Checked by a menu walk by pad, keys and mouse logging focus and Back, and the settings file compared across a restart.
- Standard: XAG 112 to 115 checks pass on every menu screen. Test: S: a menu walk by pad, keys and mouse, logging focus and Back on every screen; settings file compared before and after a restart.
- Source: XAG 112 to 115; the description, section 3 (menus). (real-world figure or published standard). Designed in: DEFINITIONS AX-06; sources/a11y-pc.json (XAG 112 to 115); GAME-DESCRIPTION-COPY-2 §3
- Status: measured. Coverage row: AX-06.

### AX-07 Save thumbnails, rotating autosaves and never losing the only save (slots and autosave are already in the description)

- How it works: At least eight manual slots, each with a picture, the game day and hour, the place and Tom's rung in words, and three rotating autosaves. A save is written to a new file and swapped in only once complete; quitting saves, and a crash loses at most the last deed. Pass: kill the process at random points during 100 saves and a good save always loads and equals one of the last two good states.
- Standard: (1) Eight manual slots with picture, day, hour, place; (2) three rotating autosaves; (3) power cut during save x 100: a good save always loads. Test: SaveChaos style: kill the process at random points during 100 saves; every time a save loads and equals one of the last two good states.
- Source: The description, section 3 (saving); ER-SAVE-01; PC players' expectation from the players study (bugs and broken saves punished). (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS AX-07; GAME-DESCRIPTION-COPY-2 §3, §35; DESIGN §17 (ER-SAVE-01); GTAVI-MAP (GTA VI: 15 manual slots, one autosave)
- Status: decided. Coverage row: AX-07. Conflicts settled: C-153.

### AX-08 Accessibility features listed in game and on the store page

- How it works: An Accessibility page in Settings lists every assist and option with one plain line on what each does, and the same list is on the store page. A script compares the settings file's keys with the page text and any missing option fails.
- Standard: GAG basic, XAG 121: every option present on both; none missing (a script compares the settings file's keys with the page). Test: Script diff of settings keys against the page text.
- Source: GAG, XAG 121. (real-world figure or published standard). Designed in: DEFINITIONS AX-08; sources/a11y-pc.json (XAG 121, GAG basic)
- Status: measured. Coverage row: AX-08.

### AX-09 Screen narration of menus

- How it works: A 'read menus aloud' switch, off by default and offered on the first menu, speaks the focused menu item, its value and the Ledger's headings and lines through the system's speech voice; prompts in play can also be read aloud. Pass: every menu item and Ledger line focused with the switch on produces a speech event in the menu walk log.
- Standard: XAG 106: every menu item and every Ledger line is spoken when focused with the switch on. Test: B: a menu walk with speech events logged; any focused item without a speech event fails.
- Source: XAG 106; Y1.9 (screen narration). (real-world figure or published standard). Designed in: DEFINITIONS AX-09; sources/a11y-pc.json (XAG 106); GTAVI-MAP Y1.9
- Status: measured. Coverage row: AX-09.

### AX-10 Pause and focus safety (pause on losing focus, alt-tab safe)

- How it works: When the window loses focus the game pauses (Esc menu shown) unless the player turns that off; alt-tab and a change of window size never crash, lose input or change the town's state. Pass: 100 alt-tabs and 50 resizes during walking, driving, a fight and talk give no crash, no stuck key and an unchanged save hash while paused.
- Standard: 100 alt-tabs and 50 window resizes in a soak: no crash, no stuck key, no town state change while paused (save hash). Test: B: scripted focus loss and resize during walking, driving, a fight and talk.
- Source: PC players' expectations (sources/a11y-pc.json, PC section); the description, section 3 (Esc pauses everywhere). (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS AX-10; sources/a11y-pc.json (PC section); GAME-DESCRIPTION-COPY-2 §3
- Status: decided. Coverage row: AX-10.

### AX-11 Information never by colour alone; key objects distinct

- How it works: No information is carried by colour alone: the light cue is darkness at the frame's corners, the belief line has words, the seeing outline is a shape, and key objects (usable doors, the firm's cab, a constable) differ by shape and light. Three colour-blind filters (red-green two ways, blue-yellow) are offered though the design does not rely on them. Pass: 40 frames with cues through protanopia, deuteranopia and tritanopia simulations, and a fresh reviewer still names each cue's meaning.
- Standard: Every cue passes a check under simulated protanopia, deuteranopia and tritanopia: the meaning is still readable. Test: S: 40 frames with cues, put through the three simulations; a fresh reviewer names each cue's meaning.
- Source: XAG 103, GAG (colour); Y1.9. (real-world figure or published standard). Designed in: DEFINITIONS AX-11; sources/a11y-pc.json (XAG 103); GTAVI-MAP Y1.9
- Status: measured. Coverage row: AX-11.

## 8.5 Install and launch

Starts from its shortcut, shows progress, opens at a sensible size.


### 8.5 Install and launch

- How it works: The game starts from its shortcut with its talk program and voice inside, shows progress while shaders and the street prepare, and opens at a sensible window or full screen size. It then offers quality presets, brightness and scale, and a title screen with New game, Continue and Quit; Esc pauses everywhere. On 5 Oct the packaged Shipping build did this from a copy of the shortcut: full screen at 3440 by 1440 after 'Finding the picture this PC can keep smooth', and Continue returned him beside Ron as saved.
- Standard: ER-START-01 (basics 1 to 5) Test: S on the packaged build
- Source: DESIGN §17 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN §17 (ER-START-01); friends-build MAP (basics 1 to 5, 19, 20); GAME-DESCRIPTION-COPY-2 §3
- Status: outside. Coverage row: 8.5. Conflicts settled: C-154.

## 8.6 Live talk service

The server relay, the key never shipped, each copy's allowance, a spending stop, offline fallback.


### 8.6.1 Talk service longevity and offline

- How it works: Live talk at release goes through the studio's own server: the game is sold once, the key never shipped, each copy has an allowance set above a playthrough's measured cost, then a spending stop and the written lines carry on; an own-key mode comes later. Offline or slow, the authored street carries on with an in-character brush-off and a small sign; a reply is heard within 2 s or the written line plays, and a line slower than 8 s is dropped. Typing is for talk only; on a pad suggested lines show at once with an on-screen keyboard, and a whole talk can be done by pad. For friends' evenings his key is capped at 5 dollars an evening.
- Standard: Offline: the written street carries on (ruling 23 Sep); allowance above a playthrough's measured cost (24 Sep) Test: the game played whole with the service off
- Source: RULINGS 23, 24 Sep (his ruling or canon). Designed in: RULINGS 23, 24 Sep, 4 Oct; GAME-DESCRIPTION-COPY-2 §28; friends-build MAP; store/steam-ai-disclosure.md
- Status: measured. Coverage row: 8.6.1. Conflicts settled: C-155.

## 8.7 Local models on the card

Voice and fallback talk on the player's card, re-tested every three months.


### 8.7 Local models on the card

- How it works: The voices are made on the player's own computer (Pocket, from VCTK reference recordings) and a local model on the card is the later offline fallback for talk. The voice moves into the game only with evidence it shortens the delay. The card's cast voice was judged to suit it (25 Oct). Models are re-checked monthly from 7 Dec on the talk bench, three candidates at most, a win going to him as one tap.
- Standard: RULINGS 28 Oct Test: talk bench
- Source: RULINGS 28 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 24 Sep, 1 Oct, 25 Oct, 28 Oct, 12 Nov, 19 Nov; THIRD-PARTY.md
- Status: outside. Coverage row: 8.7. Conflicts settled: C-156.

## 8.8 Runtime content guards

The content rule on live speech and crowd generation.


### 8.8 Runtime content guards

- How it works: The content rule is held by six sites: the rule itself, every image spec's content clause, the word-list gate over dialogue and spoken lines, crowd generation (the one site that is code), the brand bible and the animation library walked by clip and slot name. Live speech is checked before it is shown or spoken and a failing line is replaced by the written fall-back; the speaker names no real make, brand, shop, club, programme, paper or public figure and nothing after 1992. The model is told never to mention alcohol, gambling or children.
- Standard: canon content rule's six enforcement sites; live talk names no real brand or anything after 1992 Test: content gate; planted bad replies
- Source: canon D18; RULINGS 29 Sep (his ruling or canon). Designed in: canon.md content rule (D18); RULINGS 29 Sep, 3 Oct, 7 to 28 Oct (speech); G4-RATING-AND-STORE s2; GAME-DESCRIPTION-COPY-2 §28; DEFINITIONS RT-15
- Status: measured. Coverage row: 8.8.

### RT-15 Live-talk abuse and off-limits input

- How it works: Any typed line that is abusive, off topic, out of period, against the content rule or tries to steer the model is answered in character: puzzlement for the out-of-period ('you what?'), a cold end for abuse (the person ends the talk and remembers the rudeness), a refusal in his own words for the content rule. Text that claims to do something ('I hit him') is talk, never an act. Pass: zero breaches of the content, era or brand rules on a 300-line red-team set, with the content gate and claim check over every reply and a fresh reviewer reading 50.
- Standard: Zero breaches of the content rule, era or brand rules on a red-team set; every reply in character. Test: A red-team set of 300 lines through live talk; the content gate and claim check over every reply; a fresh reviewer reads 50.
- Source: canon.md content rule; the description, section 34 (claim check); 8.8 runtime guards. (his ruling or canon). Designed in: DEFINITIONS RT-15; canon.md content rule; GAME-DESCRIPTION-COPY-2 §28; RULINGS 29 Sep, 3 Oct
- Status: measured. Coverage row: RT-15.

## 8.9 Text and language

English only; text out of code.


### 8.9 Text and language

- How it works: The game is in English only and every line of text lives in data, not in code. There is no localisation work. The Ledger, subtitles, prompts and menus are all English, and screen narration uses the system's speech voice.
- Standard: Ruling 23 Sep Test: S: no player-facing string in code
- Source: RULINGS 23 Sep (his ruling or canon). Designed in: RULINGS 23 Sep; map-departments (localisation: none); DEFINITIONS AX-09
- Status: measured. Coverage row: 8.9.

## 8.10 Collision and physics

Bodies, props, cars and doors colliding believably; ragdoll blended with authored falls.


### 8.10 Collision and physics

- How it works: Nothing passes through walls, bodies or cars; nobody and nothing is stuck for more than 5 s; no car launches or spins on a touch; a struck person falls as the hit's direction says. Pass: a 2-hour soak of walking, driving and fights with a clip and pass-through detector shows zero pass-throughs, zero stuck over 5 s and zero launches. A person hit by Tom's car falls by speed band: under 10 mph a stagger, 10 to 25 mph knocked down and up within 5 s, over 25 mph thrown down and still for up to 20 s, never limp as dead.
- Standard: In a 2-hour soak of walking, driving and fights: zero pass-throughs, zero stuck over 5 s, zero launches. Test: B: the soak with a clip and pass-through detector.
- Source: ER-CORE-01; ER-FIGHT-06; the description, sections 10, 11. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS 8.10, P04; DESIGN §1 (ER-CORE-01), §7 (ER-FIGHT-06); GAME-DESCRIPTION-COPY-2 §40
- Status: decided. Coverage row: 8.10.
