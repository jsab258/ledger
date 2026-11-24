# Review of EMERGENT-MEASURE.md

24 November 2026. Fresh reviewer, checked against PLAYERS-STORIES.md (STORY-01 to STORY-08 and its counts), WHERE-PLAYERS-QUIT.md, MEMORY-SYSTEMS.md, BLUEPRINT-09 (9.13, the test door), BLUEPRINT-03, BLUEPRINT-07 row 7.6, DEFINITIONS RT2-10, SYSTEMS-THE-STORY-NEEDS.md and STORY-FRAME-2026-11-26.md. Faults only, most serious first. 10 must-fix, 10 should-fix, 3 nits.

Numbers that trace correctly and need nothing: 21 came back; Nemesis 10; witnesses 7; physics 0 of 8; driving 0 of 5; 4 of KCD2's 7 comebacks; "totally unique to your game" (de Plater, PC Gamer, 19 Sep 2014); RDR2 31.2 points (72.7% to 41.5%); 6 of 8 panel players; one in five funny; a third on a mark; "within a game day" for said to his face; a third of the hours beside Ron; two real hours between heavy beats; three of seven shape fields. House style is clean: no em-dashes, no italics, British spelling throughout.

## Must fix

### M1. Test 2's replay cannot prove what it claims

Line: "For each candidate the checker replays from the save before the choice with the other option, to a fixed horizon (one game day or the comeback's time, whichever is later), and records whether the outcome differs. This is code, not judgement." (section 4, step 4; also section 1, test 2)

Fault: four gaps, any one of which makes test 2 pass on nearly everything. (a) After the choice the AI tester keeps playing, and a model's later play differs from run to run, so the outcome can differ because of the tester, not the choice. (b) There is no control run: nothing shows that replaying the same option reproduces the comeback, so ordinary run-to-run difference is read as "could have gone another way". (c) "Outcome differs" is not defined. Taking the other option always changes the state, so a raw state difference always passes. (d) The test door gives "saves as hand-overs" (9.13.3), not a snapshot before every choice, so "the save before the choice" may not exist.

Fix: "The Core snapshots the state at every logged choice point. The replay loads that snapshot, applies the other option, then plays the recorded inputs that followed (or holds Tom idle) to the horizon; a control replay with the original option must reproduce the comeback, or the candidate is void. The outcome differs when the linked comeback is absent, or comes from a different person or with a different content, in the other-option run."

### M2. Test 1 cannot be proved by code from the log described

Line: "The Core writes every deed with its seven slots, every witness, every telling with its chain print, every kept person's attitude change, and every beat the director plays with its carrier and cause." (section 4, step 2), with "tests 1, 2 and 4 are proved by code from the log and the replay" (section 7)

Fault: the log as listed has no choice points and no list of the options open at each one. STORY-01 requires both ("two or more options open, the one taken"). Without them no script can prove test 1, and the replay in M1 has no "other option" to apply.

Fix: add to step 2: "every choice point, with the options open to Tom at that moment and the one taken".

### M3. A nameless crowd extra passes "a named person was there"

Line: "A named person was there: by id, a kept person, not a crowd extra (a crowd extra who caught a slot becomes kept, RT2-10, and then counts)." (section 1, test 3)

Fault: under RT2-10 every crowd extra who catches any slot of a deed becomes kept, so any witnessed deed has a "kept person" by construction and test 3 passes almost automatically. A kept extra gets a face, a coat, a home and a routine, but not a name. MEMORY-SYSTEMS MEM-07 keeps the two apart: a regular has "at least one own line"; a raised extra has only "a describable role". The study's whole point is that the strong stories name the person (17 of 82 named; 7 of 82 named and came back), and T10 asks for a name.

Fix: "A named person was there: by id, a person with a name the player can learn (a regular, a core or supporting person, or a raised extra who has since been given a name and an own line). A raised crowd extra without a name makes the moment a near miss."

### M4. The senses rule contradicts the K2 kind and the report example

Line: "Fix: a comeback counts only if it reached Tom's senses (said to him, in his sight or hearing, or in the Ledger)." (section 7), against K2: "tells Ellis, refuses a fare, keeps quiet for a reason" (section 2) and the report line "...and told Brenda why" (section 4, step 6)

Fault: a witness telling Ellis out of Tom's sight, or keeping quiet, never reaches Tom, so under section 7 it cannot be a comeback; yet section 2 lists both as K2 comebacks. The rule also sits only in the list of risks, not in test 4 where the counting script reads it.

Fix: move the rule into section 1, test 4 ("...and the reaction reached Tom's senses: said to him, in his sight or hearing, or in the Ledger"). Rewrite K2 as "a person who saw or heard a deed acts on it later where Tom meets it: refuses his fare, or Ellis puts it to him". Keep the Brenda example only if Tom hears her.

### M5. One main kind, with Funny as a kind, makes T2 and T3 miscount

Lines: "Each full moment is tagged with one main kind (the log keeps every system involved)"; "K7 Funny | any of the above that the panel tags funny"; T2 "at least half of all full moments from witnesses, recognition or returning people (K2, K3, K4)"; T3 "at least a third turn on a mark (K3 or a marked K4)".

Fault: (a) K7 is "any of the above", so a funny witness moment tagged K7 drops out of T2 and T3. The funnier the town, the worse it scores. (b) STORY-04 counts every moment that turns on a mark "from the log's mark field". T3 counts only K3 and marked K4, so the KCD2 shape (a witness who connects stolen gear, tagged K2) is lost. (c) STORY-03's returning person includes "crew"; T2 leaves out K6, so a crewman who comes for Tom does not count. (d) K1 (a person saying the deed to his face) is usually also a witness, and which tag the Sonnet screen picks between K1 and K2 decides whether it counts for T2. The share swings with an arbitrary tag.

Fix: make Funny a separate yes/no flag, not a kind. Compute T2 from the systems field: "a full moment counts for T2 if its systems include witnesses, memory and recognition, or a returning person (rival's man, debtor, beaten man, crew)". Compute T3 from the mark field: "a full moment counts for T3 if its mark field is filled, whatever its kind". Keep the main kind for the report only.

### M6. "Real hours" are undefined for an AI tester on a stepped clock

Lines: "three real hours from New game"; "at least one full moment in the first 30 minutes, and at least two in every later hour"; "a stepped clock" (section 4, step 1)

Fault: the tester runs on a stepped clock and acts at machine pace. Its "hour" is neither a player's hour nor fixed. A tester that acts faster than a person makes more deeds and comebacks per hour and inflates T1 and T9. The opposite also happens: clock steps across a talk scene squeeze it to nothing. STORY-02's three real hours are a player's hours.

Fix: "An evening's time is game-clock time at the build's rate (60 s a game hour, 9.13), with the clock running during talk and menus as for a player, and the tester's action rate capped at a stated human pace, checked against one panel player's log once the panel exists. Each hour window is reported in this time."

### M7. T5 depends on the panel and is not marked PENDING

Lines: "T5 (STORY-06): at least one full moment in five is funny, tagged by panel players."; "Over five seeded first evenings ... all five must pass"; "Funny tags (T5) come only from panel players or a panel spot-check" (section 4, step 5)

Fault: the panel does not exist yet (STORY-08 and T10 are PENDING the panel). Five AI evenings per release candidate cannot be tagged by panel players, so T5 either fails every release or the checker's own tags slip in, which STORY-06 forbids.

Fix: "T5 ... PENDING the panel. Until it exists, the checker's funny tags are reported as screen only and T5 is neither passed nor failed."

### M8. "Five or six or seven" is misattributed twice

Line: "The players' stories study says so plainly: posts never count how often such moments happen in an ordinary evening, and Shadow of Mordor's designers aimed at "five or six or seven" memorable orcs a game as a focus, not a measured rate." (section 3)

Fault: the quote is not in the players' stories study. It is in MEMORY-SYSTEMS.md (Nemesis section, source M1), and M1 is de Plater speaking about Shadow of War (GameSpot, undated, around 2017), not Shadow of Mordor's designers.

Fix: "...in an ordinary evening; and the memory study notes that de Plater said the Nemesis team aimed at "five or six or seven" memorable orcs a game (GameSpot, around 2017, on Shadow of War; MEMORY-SYSTEMS M1), a design focus, not a measured rate."

### M9. T9 measures the wrong stretch for the danger it cites

Line: "T9 Later evenings too: after the first evening, at least two full moments an hour, measured on three seeded evenings taken from the middle of Act II (the danger point the players' quit study names: the hand-over from the guided week to the open rise; RDR2 loses 31.2 points of owners across chapter 2)."

Fault: the danger point the quit study names is the hand-over itself. WQ-01's window runs "from the end of Act I's first week to the first rung change of Act II". Evenings from the middle of Act II leave out exactly that stretch, so T9 can pass while the cited danger is never measured.

Fix: "...measured on three seeded evenings: one starting at the end of Act I's first week (the hand-over, WQ-01's window), one at the Landing, one in Act IIb ...". Keep the RDR2 basis.

### M10. Pooled standards turned into per-evening ones, and T6 cannot apply per evening

Line: "Over five seeded first evenings (three real hours from New game, different first choices), all five must pass:" followed by T2 to T6.

Fault: STORY-03 is measured "of all full moments in those five evenings" and STORY-04 is pooled the same way. Requiring every evening to pass on its own changes both standards without saying so. T6 compares two evenings, so it cannot be passed "by each of five". Only STORY-02 is per evening.

Fix: "T1 must pass in each of the five evenings. T2, T3 and T5 are computed over all full moments of the five evenings together. T4 is checked in each evening where it applies. T6 must hold for every pair of the five." If per-evening T2 and T3 are wanted as a stricter choice, say so and mark it as this file's design choice.

## Should fix

### S1. S1 is the frame's rule, not WQ-01, and the personas miss the lazy player

Lines: "S1 The 30-minute rule (WQ-01): longest gap after Act I with nothing reaching Tom; target under 30 real minutes in every run." and "Three play styles ... rough ..., careful ..., and talker ..." (section 4, step 1)

Fault: WQ-01 is narrower and different. It is measured "in the lazy and greedy bot playthroughs", from the end of Act I's first week to the first rung change, it counts only "a main-story beat or a person bringing a job", and it also needs the next main step named in the Ledger's Open page. "Something reaches Tom" is the frame's pacing line (section 6). None of the three personas is the lazy player, which is the one that shows quiet gaps. Nor does the file say which personas play the five first evenings, although it says the careful run "matters most".

Fix: label S1 "(frame, section 6; WQ-01 tested separately in its own window and terms)" and add "S1b WQ-01 as written, including the Open page". Add a fourth persona, idle (does little, follows only what is brought to him), for S1 and WQ-01. State the persona mix for the five first evenings, for example "at least two careful, and one of each other".

### S2. Vacuous passes

Lines: T4 "once a rival has noticed Tom, ..."; T7 "target 100% where the witness is alive and free"

Fault: an evening where no rival notices Tom, or no witnessed deed of weight happens, passes T4 or T7 with nothing measured. The careful persona is the most likely to do this.

Fix: "A target whose condition never arose is reported NOT REACHED, not passed. A release needs each of T4 and T7 reached in at least three of its runs."

### S3. The counting unit is unclear, and edge effects are not handled

Line: "A moment is counted once, at its comeback; a comeback that links to two deeds counts once, under the earlier." (section 4)

Fault: (a) It does not say whether one deed with several comebacks by different people is one moment or several. The frame's worked example 2 is one debt with three returns, so the choice changes the count a lot. (b) Counting at the comeback loses deeds whose comeback falls after a three-hour run ends, and mid-Act II evenings collect comebacks of deeds done before the window, whose pre-choice snapshot must come from an earlier run. (c) It does not say where the mid-Act II evenings come from.

Fix: "One deed makes at most one full moment per person who brings it back, counted at that person's first qualifying comeback. Mid-game evenings are cut from the whole playthroughs, so earlier snapshots exist; comebacks of deeds before the window count, and each run's report lists deeds whose comeback fell after its end."

### S4. T1's hour windows are ambiguous

Line: "at least one full moment in the first 30 minutes, and at least two in every later hour. So at least 5 in a three-hour evening."

Fault: "every later hour" can mean clock hours 2 and 3 (total 5, with minutes 30 to 60 unguarded) or rolling hours after minute 30 (30 to 90, 90 to 150, plus a half hour). The total and the pass test change.

Fix: name the windows: "0 to 30 min: at least 1; 60 to 120: at least 2; 120 to 180: at least 2; 30 to 60 also at least 1", or whichever is intended, with the total recomputed.

### S5. The file's own additions in section 3 are not marked, and the reference band is not like for like

Lines: "So the targets below are the study's design choices, kept until the owed reference band exists (section 6), and then re-set to the higher of the two." and "That gives the band for T1, T2 and T9." (section 6)

Fault: (a) T1's rule is the game description's (STORY-02: "the description's rule"), not the study's choice. (b) "Re-set to the higher of the two" is this file's rule, not the study's, and it is not marked. (c) The reference band is counted with test 2 relaxed ("two options were open and the game visibly allowed each"), while LEDGER is counted with a replay. Comparing the two judges LEDGER more harshly without saying so. (d) The study's band is for STORY-02 and STORY-03 from "one ordinary evening". T9 is a mid-game target and needs a mid-game evening (for example RDR2 chapter 2), which section 6 does not ask for.

Fix: "T1 is the game description's rule; T2 to T6 are the study's choices; re-setting to the higher of target and band is this file's design choice. When compared with the band, LEDGER's counts are also reported with test 2 relaxed the same way." Either add "and one evening in each game's first open stretch (RDR2 chapter 2) for T9" to section 6, or drop T9 from the band.

### S6. T10 is filed among the additions, and two related decided standards are left out

Lines: "Added here for the frame (design choices, same standing):" followed by "T10 The panel retells it (STORY-08): ... it outranks T1 to T9 when it disagrees with them."

Fault: T10 is STORY-08, not an addition. "Outranks T1 to T9" is this file's choice and is not marked. Row 7.6 also has its own panel test (5 of 8 name a retellable moment as the most exciting thing, ER-TENS-02; conflict C-244 says both stand). And MEM-10 ("within the first two real hours at least three different named people" say a deed to his face, DECIDED, row 7.6) bears directly on T7 and K1. The file mentions neither.

Fix: move T10 up with T1 to T6. Mark "the outranking is this file's design choice". Add one line: "Measured beside T10: ER-TENS-02 (5 of 8, most exciting) and MEM-10 (three named people say a deed to his face within two hours of the first evening)."

### S7. The authored-beat rule and T8 disagree, and the rule rests on a missing system

Lines: "A moment that is part of an authored beat counts only if the beat's outcome came from play (the carrier was cast from the returning pool, or the outcome turned on a choice)" (section 2), and T8 "at least one K5 that no authored beat caused" and "K5 counts only with no authored cause in the log" (section 7)

Fault: Danny's turn is a director beat whose cause is play ("a cause the player made and saw", frame section 3). Section 2 counts it as K5; section 7 and T8 exclude it. The returning-people pool the rule depends on is MISSING (SYSTEMS-THE-STORY-NEEDS, system 24), so until it exists no beat moment can count by that route.

Fix: choose one rule and state it in both places, for example "K5 counts when its cause in the log is a play event, even if a beat carried it; it is excluded when its only cause is a fail-safe or a scripted wake". Add "the returning-pool clause applies once system 24 exists".

### S8. Replay cost is unbounded

Lines: "to a fixed horizon (one game day or the comeback's time, whichever is later)" with "one whole playthrough per style (T7, T8)"

Fault: in a whole seven-week playthrough a K4 comeback can come weeks after the deed, so each such candidate needs a replay of weeks. Nothing bounds the number of candidates or the hours of runs. CLAUDE.md asks for costed items.

Fix: cap the horizon (for example 7 game days; past it, test 2 is judged by the open-options rule of section 6 and the moment is flagged), and give an estimate of candidates per evening and replay hours per release.

### S9. Which build is measured

Line: "The AI tester plays seeded evenings through the test door (seeded launch, stepped clock, saves as hand-overs; blueprint 09)."

Fault: the test door is the browser build's (9.13, window.LEDGER). The house rule is that a piece passes only in the night's packaged build and offline checks are screens. The file does not say that browser-build counts are screens.

Fix: "Counts from the browser build are screens; a release's result is the same runs in the packaged build, or is reported as screen only."

### S10. Clauses dropped from STORY-03, STORY-05 and STORY-06

Lines: T2 "none whose only systems are physics or driving"; T4 "at least one of that rival's men meets him twice"; T5 "at least one full moment in five is funny"

Fault: STORY-03's "unless a person saw it and it came back" (the study's lesson: tie every gag system to a witness, 2.18) is dropped. STORY-05's "not of Tom's own firm" is dropped, so Tom's own crewman, once a rival's, could satisfy T4. STORY-06's "within the tone of the game (dry wit, never satire)" is dropped.

Fix: restore each clause word for word.

## Nits

### N1. Wrong section pointer
Line: "PLAYERS-STORIES.md, section 3". The study has no numbered sections. Fix: "section 'Standards for LEDGER: emergent moments per evening'".

### N2. The four tests are the description's, not the study's
Line: "A full moment passes the study's four tests". The study says "The game's description already sets the measure (section 2)". Fix: "the game description's four tests (section 2), as the study makes them countable".

### N3. Dates
The file is dated 24 November 2026 and builds on STORY-FRAME-2026-11-26.md, which is dated 26 November. Fix: date the file on or after the frame it extends, or say which draft of the frame it read.

## Seen in a source, not this file's fault

MEMORY-SYSTEMS.md, point 5, still says "25 stories that came back"; PLAYERS-STORIES.md recomputed it to 21 after recoding. EMERGENT-MEASURE uses 21, which is correct. The memory study's figure should be corrected at its home.
