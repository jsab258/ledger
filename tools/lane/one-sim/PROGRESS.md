# one-sim: progress (task 4s, "one simulation in the browser")

Run 1, 19 November 2026, 13:19 to 14:12 UTC, in the cloud: the study and the first build (steps 1 and 2). A fresh reviewer checked them the same day (production/lane/REVIEW-ONE-SIM-STEP1-2.md: pass with fixes, 12 findings).

Run 2, 19 November 2026, 16:18 to about 17:15 UTC, in a fresh cloud machine: the 12 fixes, the bridge (step 3a) and the list of differences (step 3b). Everything was rebuilt from nothing. A fresh reviewer checked it the same day (production/lane/REVIEW-ONE-SIM-RUN2.md: pass with fixes, 3 must, 6 should, 4 minor).

Run 3, 19 November 2026, 18:18 to about 19:15 UTC, in a fresh cloud machine: the second review's 13 findings applied, a breaker pass over the bridge, and the licence wording brought up to date (both lines are now on the allowlist). Everything was rebuilt from nothing. Run 3's work has not had a fresh reviewer yet. Step 4, the swap, was not started: its plan is at the end of this file.

## Where it stands, in five lines

1. The game's own C++ town code runs in a real browser and gives the C# Core's answers: all 102,949 comparable golden rows, 8,568 routine hours, and 225 hours of six scripted weeks. Node and Chromium end with the same town, compared by the script.
2. Both reviews' fixes are in: the first review's 12 (run 2) and the second review's 13 findings (run 3, listed below). None of them changed a town: every digest is the same as before.
3. The bridge for the prototype is written and tested (BRIDGE.md, wasm/one-sim-bridge.mjs): the prototype hands over its clock, gets back what each hour did, and carries the town in its save. Played the reference week's way it gives the C# Core's rows at 225 of 225 hours; played the game's way (the default) 129 of 225, the rest differing only in the count of stories and at one hour in who found the damage (finding 6 for the Core's owner). A town saved in mid-week plays on the same in 6 of 6 weeks. Since run 3 it refuses what would leave the town wrong, a save from before the swap keeps loading, and a breaker's 191 tries to make it misbehave all hold.
4. The differences between the prototype's own town and the real rules are listed with what each changes for the player, three of them measured (DIFFERENCES.md). Run 3 added the ones the review found missing and one more of its own: the real week follows one deed, a thing damaged, only that deed reaches the police, and the prototype has no act that damages a thing. As the two stand, nothing he does in the prototype would bring a constable after the swap. The prototype's source is untouched: the swap is step 4.
5. No licence holds publishing any more: both lines are on the allowlist (item 17 the tools, item 18 the library pieces inside the simulation file, his yes of 19 November 17:29). What stands before a published swap: seven decisions of his (DIFFERENCES.md, the end), the credits file that item 18's "notices kept" asks for, and the swap round itself through the publish gate.

## Done, with evidence

One command, last run with the files as committed: `tools/lane/one-sim/one-sim.sh all`, 18:58 to 19:02 UTC, 226 s, exit 0, last line "one-sim: everything passed" (58 lines of ok, none failing: 13 checks under Node, the same 13 in the page, the Core's own three, the two port tests, the three source lists, the selftests' 22, the breaker and the comparison of the two engines). Logs are in /home/claude/one-sim-work/logs/ (outside the repository, so they do not last: the numbers are copied here).

Run 3 ran it four times. First as a baseline on a machine that had nothing installed, begun at 18:21 UTC with the files as run 2 left them (572 s): exit 1, with one failure, a check inside the Core's own CoreTests that depends on real time (finding 8 below). The machine was under heavy load from other helpers at that moment (load average 15 on two processors). That pass's later steps ran while the bridge was already being rewritten, so they are evidence for neither state of the files and are not counted. Then after the fixes and the first breaker (18:40 to 18:44 UTC, 241 s, exit 0, CoreTests "All 5255 checks passed"); after the breaker's awkward moments were added (18:47 to 18:55 UTC, 461 s on a loaded machine, exit 0); and the run named above, after the last hole was closed. In run 2 it was run four times, each time exit 0 (16:26, 16:46, 17:01, 17:07).

| Name in the output | What it checks | Result |
|---|---|---|
| source lists (run 2) | The lane's three project files list the same sources as ledger/PerceptionGolden, Soak and CoreTests | the same: 142, 142 and 153 files |
| reference: built | PerceptionGolden, Soak and CoreTests built from the real Core (140 files) by path, .NET SDK 8.0.428 | built, no errors |
| C# goldens | The table the Core writes today against the committed one (ue-probe/perception-golden) | 102,960 rows, 267 rules, identical byte for byte |
| Soak | The Core's own soak check | ok, all 9 checks passed |
| CoreTests | The Core's own tests | "All 5255 checks passed." |
| port-test-as-wasm-game-flags | The port's own golden test (ue-probe/tests/core-port-test.cpp, unchanged) as a WebAssembly program, built with the game's flags | 102,993 checks, 0 failures over 102,949 rows, 0 unanswered, 11 skipped by name (7 claims, 4 FactNull) |
| port-test-as-wasm-with-exceptions | The same with C++ exceptions on | 102,997 checks, 0 failures over 102,953 rows, 7 skipped (claims) |
| T1 golden rows through JavaScript | Every row asked through the loader, no files (data handed in as text) | 102,949 agree, 0 differ, 0 unanswered, 11 skipped by name |
| T1b, T1c | Only the two named holes are skipped; the 3,500 seeded GossipFuzz rows are among those checked | ok |
| T2 routines through the front door | Where each person is each hour, both cast files, against the Core's CastPlaceOf rows | 8,568 of 8,568 |
| T3 the week hour by hour through the front door | Six scripted weeks played by calls from JavaScript, each hour's 13 answers against the Core's TownWeekHour rows | 225 of 225 |
| T4 the same calls twice give the same town | A digest of every hour, the final state and every held story | 37e81244f129619f both times. Inside one engine this is almost certain by design. |
| T4x Node against the browser (run 2) | The real test of the same town: `all` compares Node's digest with Chromium's and fails if they differ | 37e81244f129619f in both, and the bridge's weeks d678e26b179e7b68 in both |
| T5 | Speed and size | 17 to 22 ms a game day on a quiet machine over run 2's and run 3's runs, 41 people (34 in one of run 3's passes, with the machine loaded); one-sim.wasm 423,015 bytes, 142,080 gzip, 108,526 Brotli (run 1, before the save routines: 301,665, 102,362, 79,767; run 3 did not change the front door, so the file is the same); loader 8,938 bytes; bridge 41,245 bytes, 13,733 gzip (14,960 before run 3) |
| T6 the front door takes rough handling | Calls before a town exists, broken cast files, times that are no time, answers outside the list, odd and long text, a thirty-day jump, a second town | nothing fell over |
| T7 the Ledger's facts through the front door | Who knows what and how, read back after every scripted hour | the count is the hour's own at all 225 hours; nobody but the witness is said to have seen the window go; the witness holds it first-hand, recognised, at 130 of 130 hours after the deed. The details of each fact are not yet compared with the C# Core; no golden rows exist for them. |
| T8 the bridge, talk by the hour (run 2) | The six weeks again, driven by a clock in steps of 7.3 game minutes through the bridge, with the prototype's own id for Darren | 225 of 225 hours agree with the C# Core's rows; the bridge's "held" agrees at all 225 |
| T9 the bridge, talk by the minute (run 2) | The packaged game's order, with the clock ticked every game minute, every 0.37 and every 7.3 | the same town in all three; 15 to 21 ms a game day on a quiet machine (46 to 54 in one of run 3's passes, loaded) |
| T10 a save in the middle (run 2) | Each week saved after two fifths of its hours, as text, loaded into a fresh module, played on | 6 of 6 end as the week played straight through; held in the cells at the save, still held after the load until the same minute; the biggest save 16,826 characters |
| T11 the bridge takes rough handling (run 2; run 3 the review's holes) | The prototype's start at 15:36, jumps, the prototype's own ids, a thirty-day jump, a save loaded and saved again; a deed's witnesses taken and dropped by name; the first deed's witness still going to the police after a second deed was refused; the cast file as Windows writes it; and 42 things that must be refused (run 2 had sixteen) | all as they should be |
| T12 a save from before the swap (run 3) | An old prototype save, written by hand in its own shape, opens a fresh town at its clock and tells it what its people saw | 4 told at the rungs their memories support, 8 left out each with its reason, the losses said in 7 lines; two days on the blow is held by 23 people, with no statement and no arrest; the town then saves and loads like any other |
| breaker (run 3) | 191 tries to make the bridge misbehave: opening it 16, the clock 23, bad calls 52, spoiled saves 59, spoiled old saves 11, and a sound save at 30 awkward moments, which must load and play on the same | 191 of 191 hold. The first pass (150 tries) had 13 not held, and a later look found one more hole: see "The breaker" below |
| selftest | Four rows spoiled on purpose must be caught, each by its own check; the three small comparers checked too | 9 of 9, 8 of 8, 5 of 5 |
| browser | The same checks inside a real page, headless Chromium 157.0.8103.78 | all passed |
| stale table (run 2, tried by hand) | `test`, `selftest`, `browser`, `breaks` with a table that is not the committed one | each stops with NOTHING MEASURED, exit 3 |
| breaks (run apart: `one-sim.sh breaks`) | Seven one-line breaks planted in a copy of the port; both browser builds made from each, every check run, the whole table included | 5 of 7 fail rows of the whole table (44, 9, 12, 145 and 2,812 of 102,949 rows); the same 5 fail T2 or T3, and the bridge's T8 sees them too; 2 are seen by nothing, the bridge's checks included. See findings 2 and 3. Run twice in run 2, before and after the bridge went in: the same counts. Run 2's last run 16:50 to 17:00 UTC, 10 minutes 31 s. Run again at the end of run 3 with the files as committed (19:03 to 19:13 UTC, 9 minutes 33 s, exit 0): the same counts, the same 5 seen, and the same 2 seen by nothing, T11 and T12 included. One thing is new: T11 now also sees the two breaks that move the witnesses' reports and the constable by an hour, through its check that Darren goes on Wednesday at nine and the constable comes on Thursday at ten. |
| differences (run apart: `one-sim.sh differences`) | The prototype's own rule files, unchanged, beside the real town: M1 where nine people are, M2 when people move, M3 how far one story travels; and since run 3 a check, M4: the bridge's table of the prototype's kinds of act against the prototype's own list | measured in 5 s; M1 to M3 the same numbers as run 2; M4: 53 kinds, 53 rows, none against the rule. The numbers are in DIFFERENCES.md |

The front door (wasm/one_sim.cpp) has 35 calls, four of them plumbing, no rule of its own. Run 2 added ten: a sighting that is no damage, "held until", and four calls each way for the save. The save calls hand out and take back the same texts the packaged game writes into its save folder, made and read by the port's own save routines.

The module now asks seven small things of the page, where run 1's asked four: printing, close, seek, the clock (answered with zero), and since the save was added the computer's list of settings (answered: none, two calls) and "stop" (answered with an error; no test ever reached it).

Run 2, the review's 12 fixes, each once:

1. `all` compares Node's digest with the browser's (T4x above; wasm/engines_agree.py).
2. breaks.py runs the whole table on every broken copy (the breaks row above).
3. The lane's project files against the originals: `reference` compares the two source lists on every run and stops if they differ. Invariant globalisation, which only the lane's files set, is removed: it was not needed here and no result changed. Finding 5 below is what it could have hidden.
4. `test`, `selftest`, `browser` and `breaks` stop when the table in the work folder is no longer the committed one.
5. The study's wrong count of files that mention Unity is corrected (25 of 140, none uses UnityEngine).
6. T7's limit is said where T7 is named (above, the study, the README).
7. The study's answer now says "thirteen answers for each hour", not the whole state.
8. The study's sources say how each web page was reached. No address was guessed in run 2. The tool downloads are recorded in the lane's log for the main session to confirm.
9. zstandard is pinned by version and checksum (reference/zstd-requirements.txt). Its licence was read: BSD 3-clause.
10. Licences: rows for the loader, the bridge and the cast file; the full texts read and what they add written into the study's section 4; the decision record handed to the main session (below).
11. A plain sentence stands in front of the licence line in the study's section 6.
12. The study's section 5 says that the game passes its own hooks into the hour and the front door none, and that "held" is the prototype's to keep. The bridge keeps it (BRIDGE.md).

## Run 3: the second review's 13 findings, each once

1. must, the police's reach. Fixed in the records and held by a check. DIFFERENCES.md says it in the short answer, in two new rows of section 5 and in decision 5; BRIDGE.md says it under the calls and in "Not done yet". T12 holds it: a blow seen by three people brings talk and DS Ellis, and no statement and no arrest.
2. must, one deed a week. Fixed. The bridge refuses a second deed with its reason and offers `deedHeld()`; T11 plays the reviewer's case and finds the first deed's witness at the police on Wednesday at nine and the constable on Thursday at ten. DIFFERENCES.md has the row. Finding 7 below is for the Core's owner.
3. must, old saves. Fixed. The recommendation "not offered" is withdrawn in both files. `openTownFromOldSave` opens a fresh town at the save's clock and tells it what the old save's people saw, with what is left out and what the player loses said plainly (T12). Left for step 4: the prototype's own old-save test in the page, with a save from a real older build.
4. should, unknown witnesses and areas. Fixed. `deed` returns who was taken and who was dropped, and refuses an unknown area; `tick` and `saw` refuse one too (T11).
5. should, the three acts that skipped the out-of-turn check. Fixed: `teaMinute`, `weekAsk` and `weekAsksNow` have the same two checks, without the talk call. T8 still gives 225 of 225.
6. should, a save whose pieces disagree. Fixed, and taken further: the minute must be whole, the next hour must follow it, every person must have a memory; and the clock is held against the town's own record of how far its talk has run, so a clock moved back or on with its next hour in step is refused too (T11).
7. should, the cast mark and line endings. Fixed: the mark is of the people, areas and places, not the file's text. The same file with a byte-order mark and CRLF, or with every space taken out, loads the save (T11). BRIDGE.md says what happens when the cast really changes. Not built: loading a save "with the people still present" after people are added or taken away; it is refused with a message that names them.
8. should, naming him later. Fixed: a row in section 4 and a line for the player.
9. should, what the town can be told. Fixed: DIFFERENCES.md section 10, with the table of the prototype's 53 kinds. The table lives in the bridge and `differences` checks it against the prototype's own list (M4). Decision 7 is the kinds with no home.
10. minor, the five-line summary. Fixed (line 3 above).
11. minor, two tools and one claim. Fixed: both tools are handed over in one line below, and the sentence about Playwright is corrected here and in the study.
12. minor, M3's denominator. Fixed: 26 who can hear a story, with the reason, in section 3; the script prints it.
13. minor, a batch of hours and a clock skip. Fixed: one line in BRIDGE.md and a comment on `tick`; the breaker tried it (every hour still comes once, the later ones first).

## The breaker (run 3)

wasm/breaker.mjs, run by `one-sim.sh breaker` and inside `all`. Each try names what a sound bridge does and is marked held or not held. After every refused call the town's save must be the same as before it.

First pass: 150 tries, 137 held, 13 not held. Eleven were real and are closed:

- a deed handed null fell over instead of refusing (1; a sighting had the same fault and is closed with it);
- a save was taken with its version as text; with no way of talking; with a way of talking it does not know; with its talk an empty object; with one person taken out of its talk; with its week's pieces an empty object; without the hours talked; with two people's memories changed over; with a memory that is no memory (9). The town's own readers take a piece that holds nothing as a town that knows nothing, so each of these would have lost part of the week without a word;
- an old memory with its certainty written as text was told to the town (1).

Found while closing those, and closed too: a save whose deed's witnesses did not read fell over inside the loader instead of being refused.

Two were the breaker's own wrong expectation: a town may start a thousand years on (the town's own save can record up to 600 million minutes), so that is taken, and the limit itself is now tried instead.

Second pass, with saves at awkward moments added: 185 tries, 185 held. The 30 awkward moments (just opened, on the stroke of an hour, a minute before one, right after a deed or a sighting, after a no to Ron, in the middle of the tea, held in the cells, before and after his answer at the week's end, after a thirty-day jump, a town made from an old save; each with both ways of talking) are evidence, for those moments, that the new checks refuse no sound save: each loads, saves again the same, and plays on to the same town.

Third pass, after a second reading of the bridge's own code. A deed whose thing had no name, or with nothing said of the damage, was taken: tried by hand first, its witness went to the police on Wednesday at nine and he was arrested on Thursday at ten, but the town had kept no damage, so nobody ever found it. Closed: the thing, what is said of it and a story's words must be text with something in it. Witness ids that are JavaScript's own words (constructor, toString) were tried too and held. Six tries added: 191 tries, 191 held.

Measured on the way: an old save with 10,000 first-hand memories opens in about 5.5 s, and the town's save is then 2.9 million characters, since every sighting is a story and a line of memory. How many a real played week holds was not measured.

What the breaker does not try: calls made past the bridge on `town.sim` (the loader's own object, left open for reading and for the tests); a module that stops in the middle of a tick; a save spoiled by somebody who also rewrites the town's own texts to match. And it was written by the same hand as the fixes: a fresh helper as breaker is still owed (next, point 1).

## For the main session (things the lane may not write)

- DECISIONS.md has no entry for the two new tools (the allowlist's PROCESS 2 asks for one): wasi-sdk 34 with clang, and the .NET SDK 8.0.428 from conda-forge, both tools never shipped, his yes of 19 November 16:18 (allowlist item 17).
- (run 3) Both licence lines are on the allowlist as read on the lane's branch after the merge from wip: item 17 the tools, item 18 the pieces that ship inside the simulation file (his yes 17:29, 19 November). The README, this file and the study no longer say publishing is held for a licence. Item 18 says "notices kept": the credits file is still to write, and needs four notice files that have not been read (the study, section 4). Measured in run 2 with a link map, on the file as it stands (run 3 did not change it): 69 objects from wasi-libc, 10 from the C++ library, none of the helper routines (compiler-rt) and nothing from the BSD 3-clause part (musl-fts). production/licences/one-sim/README.md still describes the line as held; it is the main session's file.
- (run 3, the review's finding 11) Two tools of this lane are on no line of the allowlist and have no decision record: Playwright for Python 1.63.0 (Apache 2.0 by its own package), which runs this lane's page test, and the Python zstandard module 0.25.0 (BSD 3-clause), which unpacks the .NET SDK. Both are tools, never shipped. One line under item 17, or a PROCESS 2 record, is the main session's to write. Run 2 wrote here that Playwright also runs the prototype's tests. That was wrong: the prototype's own tests use puppeteer-core (its package.json), which item 13 names, and no file of the prototype names Playwright.
- RECIPE.md asks for a few lines from every finished unit. The lane may not write it. Offered: "One set of rules in two places: compile the shipped rule code for the second place instead of copying it; hold both to one table written by the reference; test the glue with a clock in odd steps and a save in the middle; plant small breaks to learn what the table does not see. Cost: two cloud runs of about an hour each. Failed: nothing; found two orders of the same hour that the table cannot tell apart. Evidence: tools/lane/one-sim/PROGRESS.md."
- Seven decisions for him before the swap, written out at the end of DIFFERENCES.md. Run 2's four: the names, what each person thinks of him, the week's length, the solicitor's bill and the chase. Run 3's three: whether violence is reported to the police through the bridge or the gap is accepted for the first swap; what the one deed is, since the prototype has no act that damages a thing; and the ten kinds of decent or open act that have no home in the real town.

## Findings for whoever owns the port, the table and the Core (not fixed here: nothing under ue-probe/ or ledger/ was touched)

1. FirstWeek.h declares AdasTea::Ada in a way the C++14 standard needs a second line for. g++ accepts it. clang does not link it under C++14 ("undefined reference to LedgerCore::AdasTea::Ada"). Tried in run 1 with this machine's clang++ 18 and the exact command tools/port-golden-check.sh uses when g++ is missing (-std=c++14 -O1): the port test does not link. So that script's clang path is broken; its g++ and MSVC paths are not affected as far as seen here (MSVC not tried). The browser build uses C++17, where it is fine.
2. Planted break, seen by nothing: removing `Week.Close(Now, Mill, Cast);` from TownWeek.h HourEnd fails no golden row (0 of 102,949, measured by breaks.py) and changes nothing in the six scripted weeks, through the front door or through the bridge. The week's end closing each hour is not pinned by any row.
3. Planted break, seen by nothing: swapping the two nine o'clock calls in TownWeek.h RunHour (DS Ellis before the witnesses' reports) fails no golden row (0 of 102,949). The TownWeekSteps rows record the step names, which are typed beside the calls, not the calls. Today the swap probably cannot change any outcome, because only damage is ever reported and she comes for a crime only from wounding up (K2's reading). It will matter with the first serious crime.
4. The golden reader asks for town-news.json through the same hook as the cast files. A host that hands in only the two cast files gets four rows unanswered (TownNewsWitnesses and three KeepsHisDeeds). Not a fault, but easy to trip on.
5. (run 2) The Core writes one number with the computer's own language settings. Suspicion.cs lines 122 and 176 build the lines of the suspicion trail with a plain number format, so on a computer set to a decimal comma they read "-0,05" where the tests expect "-0.05". Measured by running the Core's own checks under four settings: under German (Germany) and Turkish, CoreTests stops at its first failed check, "and a fall still reads as a fall" (CoreTests/Program.cs line 1625), after 237 passed lines, so the rest of its 5,255 checks were not run under those settings; under Swiss German and British, all 5,255 pass. The golden table came out identical to the committed one under all four, and Soak passed under the two it was run with. The port does not carry this trail. On his PC it shows only if Windows is set to a decimal comma.
6. (run 2) The golden table's scripted weeks and the packaged game run an hour in different orders. The table's weeks (ledger/PerceptionGolden/Program.cs, EmitTownWeek) run each hour's steps and then the talk since the hour before. The game runs the talk of the hour before first (CrimeProbe.cpp line 7956) and lets it follow the minutes. Both use the same rules, and the bridge can do both. Measured over the six scripted weeks: 129 of 225 hours come out identical; in the two weeks that hold a deed the count of stories differs at 96 hours from five in the afternoon of the deed's day, and at one hour somebody more finds the damage. Who goes to the police, DS Ellis's first visit and the first arrest are the same in all six. So the order the game really plays is held to the C# Core only through the same code proved in the other order. Golden rows played the game's way would close it.

7. (run 3, from the review's finding 2) TownWeek's Deed replaces the earlier deed. DeedTopic, DeedDay, DeedAt and Witnesses are overwritten (TownWeek.h lines 103 to 106), so after a second deed the first one's witnesses never go to the police. The reviewer measured it through run 2's bridge: Darren saw the window on Tuesday, a second unseen deed followed that evening, and Darren never went. A player who learned this could erase a seen deed with an unseen one. The bridge now refuses a second deed. No golden row covers two deeds. The packaged game makes one deed, so it does not show there today.
8. (run 3) One check of CoreTests depends on real time. ledger/CoreTests/Program.cs lines 6500 to 6513, "a draft that fails while its first sentence is still being checked hands nothing over afterwards, and nothing is remembered": a scripted check made slow by 300 ms is waited for with a fixed 400 ms. On run 3's first full pass the machine was under heavy load (load average 15 on two processors, other helpers' browsers) and the check failed with a sentence handed over and remembered ("True Couldn't say what he drove. True"). CoreTests stops at its first failure, so the checks after it did not run in that pass. With the machine quieter all 5,255 passed, twice. The Core's source had not changed since run 2 (no difference under ledger/). Whether this is only the test's waiting time or a real race in the talk engine was not looked into: talk is C# only and not this lane's.
9. (run 3) The town's own save keeps how far its talk has run only below 600 million minutes (TownRounds.h, TownHours FromValue): past that a saved town comes back with its talk started over. About 1,140 years, so of no weight for a week; the bridge refuses a clock beyond it so that a save always reads back.

## Next, in order

1. One fresh reviewer for run 3 (the bridge's refusals, the old-save reader, DIFFERENCES.md sections 5, 9 and 10, the table of kinds), and a fresh helper as breaker: run 3's breaker was written by the hand that wrote the fixes.
2. His word, through the main session, on the seven decisions at the end of DIFFERENCES.md. Decisions 5 to 7 are new and the swap is thin without them: as things stand the swapped prototype would have a street that talks and a police that never comes.
3. What step 4 needs that waits on no decision:
   - a call on the front door for how well a witness sees him (the port's Perception and Sighting), held to its golden rows through JavaScript as T2 holds the routines;
   - a call on the front door for an open act (a sighting that is not about his hidden life), if decision 7 goes that way: the mill's own Witness already takes it;
   - the table from the cast file's 30 places to spots on the prototype's map, and from where he stands, and from where an old event happened, to the cast file's 24 areas;
   - the words the screens need (Ada's line, the arrest's words).
4. Step 4, the swap, through the publish gate: the plan is the last section of this file.
5. For the C# side, so the main session's: golden rows for the week played the game's way (finding 6), for who knows what after each scripted hour (T7's limit), for two deeds (finding 7) and for a sighting that is no damage.
6. The credits file for the library pieces, once the four notice files are read (the study, section 4). Item 18's "notices kept" needs it before anything is published.
7. Firefox and Safari's engine: still not tried. The module asks for nothing beyond plain WebAssembly, which is a reason to expect it to work, not a test.
8. If he ever picks B in the study's section 6: a GitHub build machine job that builds the C# Core for the browser, behind the same front door, held to the same checks.

## Blocked, and why

- Publishing anything with one-sim.wasm inside: no longer held by a licence (item 18 of the allowlist, 19 November 17:29). It still waits on the credits file ("notices kept"), which needs the four notice files read, and on the swap round through the publish gate.
- The swap in the prototype (step 4): by the task's own order it is a later round through the publish gate, and it needs his decisions. Decisions 1 to 4 shape it; without 5 to 7 it can still be built, but the player then gets a town where no constable ever comes and no good deed travels.
- The C# Core compiled for the browser (way a): the cloud's network refused NuGet and Microsoft's download sites in run 1 (403 at the gate for api.nuget.org, www.nuget.org, globalcdn.nuget.org, dot.net, builds.dotnet.microsoft.com, dotnetcli.azureedge.net). Run 2 did not try them again: he chose way A, and the .NET SDK for the checks comes from conda-forge. Not a fault of the method.

## Exact commands

From the repository root, Linux, two processors are enough. Heavy steps run at low priority (nice 15) and one compile at a time.

    tools/lane/one-sim/one-sim.sh setup        # once (8 s here). Fetches, with checksums:
                                               #   dotnet-runtime-8.0.34 and dotnet-sdk-8.0.428 from conda-forge (157 MB)
                                               #   wasi-sdk-34.0-x86_64-linux.tar.gz from GitHub releases (192 MB)
                                               #   the zstandard 0.25.0 wheel for Python 3.13 from PyPI (5.5 MB)
    tools/lane/one-sim/one-sim.sh all          # reference, wasm, test, selftest, breaker, browser, Node against the browser: about 4 minutes (8 on a loaded machine)
    tools/lane/one-sim/one-sim.sh reference    # the C# Core: source lists, build, golden table, Soak, CoreTests (about 50 s)
    tools/lane/one-sim/one-sim.sh wasm         # the four WebAssembly builds (about 2.5 minutes)
    tools/lane/one-sim/one-sim.sh test         # under Node (18 s)
    tools/lane/one-sim/one-sim.sh selftest
    tools/lane/one-sim/one-sim.sh breaker      # the 191 tries on the bridge, each printed (12 s); add --brief for the count alone
    tools/lane/one-sim/one-sim.sh browser      # needs Python's playwright with Chromium, as the prototype's tests do
    tools/lane/one-sim/one-sim.sh breaks       # the seven planted breaks (about 10 minutes)
    tools/lane/one-sim/one-sim.sh differences  # the prototype's town against the real rules (6 s)

Things to know:

- Everything large is in /home/claude/one-sim-work (set ONE_SIM_WORK to move it): the downloads about 340 MB, the .NET SDK unpacked 555 MB, wasi-sdk unpacked 635 MB, build output. None of it is in git. tools/lane/one-sim holds text only, the largest file 52 KB (wasm/checks.mjs).
- `reference` needs the right to mount: the C# check programs look upward from their own folder for the repository's data files, so they run under a folder of links into a read-only view of the repository (a read-only bind mount at $ONE_SIM_WORK/ro-repo). The script takes the view down again after use. Without mount rights it says NOTHING MEASURED and runs nothing against a writable repository.
- `reference` also needs an ICU library on the machine, as .NET on Linux does by default (Ubuntu 24.04 has libicu74).
- Another Python than 3.13 needs its own line in reference/zstd-requirements.txt: pip refuses a file whose checksum is not listed.
- The built one-sim.wasm is at $ONE_SIM_WORK/wasm/one-sim.wasm (one-sim.full.wasm keeps the names for debugging).
- Exit codes: 0 good, 1 a check failed, 2 usage, 3 nothing measured. In `all`, a failed check outranks a check that could not run.
- Versions today: Node 22.23.5, Python 3.13.18, g++ 13.3.0, Chromium 157.0.8103.78 (Playwright 1.63.0), wasi-sdk 34.0 (LLVM 23.1.0), .NET SDK 8.0.428.

## The plan for the swap round (step 4; written in run 3, nothing of it started)

Read for this plan, in the prototype as it stands (tools/lane/prototype/project): BUILD.md, src/clock.js (simStep, skipTo), src/saving.js, src/events.js, src/kinds.js, src/seeing.js (identify, witness), src/gossip.js (pickStory, gossipTick, comeback), src/state.js (the save version, 4) and test/oldsave.mjs. Not read: routines.js beyond its use in clock.js, police.js, talk.js, the story scenes and the other tests. So the steps are in order and each has its check, but the sizes are guesses.

Before any code:

- His decisions 1 to 7 (DIFFERENCES.md). The round can start with 1, 2, 3 and 6 answered; 4, 5 and 7 only change what is switched on.
- A fresh review of run 3, and a fresh breaker.
- The front-door calls step 3 of "Next" lists (how well a witness sees him; an open act; a report of violence if decision 5 says so), each held to golden rows where rows exist. These are this lane's and need no page.

Then, in the prototype, one piece at a time, each with its own check before the next:

1. The simulation file in the build. tools/build.mjs copies one-sim.wasm, the loader, the bridge and the cast file into dist beside ledger.js; the page loads the town before the title screen; files.json gains their checksums; the credits file goes in beside them. Check: the page starts, and when the file is missing it says so plainly and does not fall back to the old town.
2. The clock. One call in clock.js simStep, after the clock has moved: `for (const hour of town.tick(G.t, area)) ...`, with the hours handled after the loop (BRIDGE.md). The prototype's own gossipTick and decay are switched off in the same change, never left running beside the town. skipTo needs nothing: it steps simStep. Check: the town's clock never goes back in the prototype's own tests of sleep and the cells.
3. Where people are. For the people of the real cast, the routine's place comes from `town.placeOf` through the table of places; the walking stays the prototype's. Check: the differences script's M1 against the swapped build reads the same place at every hour for the nine.
4. What he does. In events.js `act`, once the prototype's own geometry has said who saw it and how well, each witness goes to `town.saw` (or to `town.deed` for the one deed) by the table of kinds in the bridge. The story's own steps call the town instead of seeding stories: his answer to Ron (`answerAsk`), the minutes at Ada's (`teaMinute`), Sheila's question (`weekAsk`, `weekGive`). Check: a played week's acts appear in `town.knows()` as the table says, and nothing is told twice.
5. What comes back. Each hour's answer drives the prototype's scenes: who found the damage, who went to the police, DS Ellis on the street, the arrest and the cells (`held`, `heldUntil`), Ada's invitation, Ron at the door. The prototype's own police timetable goes; its chase and bill stay or go by decision 4.
6. What people know. His book, the names, the liking and the fear are fed from `town.knows()` as decision 2 says; the remarks to his face and "two people stop talking as he passes" need the design DIFFERENCES.md sections 8 and 10 describe.
7. Saves. saving.js keeps `town` with its other keys. Loading becomes a thing that waits: `openTown({ saved })`, or `openTownFromOldSave` when the save has no town. The save version stays 4. test/oldsave.mjs gains the case, with a save from the published build.
8. The gate. The prototype's own tests (about half an hour, Chrome), `one-sim.sh all`, a fresh reviewer, the playtester, then the publish gate.

What is likely bigger than it looks, said now: the prototype's tests. Several rest on the old town's own chance and timetable (the names say so: town.mjs, same_week.mjs, week.mjs, week_bot.mjs, nights.mjs) and will have to be rewritten against a town that is seeded, runs seven days and moves people on the hour. That was not counted. A guess, not a measurement: the round is two to four cloud runs of about an hour, most of it in steps 4 to 6 and the tests.

What stays the prototype's own throughout: money, debts, jobs, fares, fights and talk; the street, walking, light, lines of sight, weather, the cab and the screens.

