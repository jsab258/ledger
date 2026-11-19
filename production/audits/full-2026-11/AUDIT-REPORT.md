# LEDGER: full audit report (19 November 2026)

Stage 3 of the full audit Jafar ordered at 00:18 on 19 Nov ("Do it now", advisor 237). It merges the inventory, the decisions trace and eleven independent reviews, with the weightiest claims checked again in the repository and on GitHub. It proposes; it changes nothing.

## 1. For Jafar, in plain words

### Where the project stands

After four and a half months and about 6,240 commits, the real game is one 48-metre street: Mickey's front office, Tom, and three people who talk. The player can walk, run, talk, press E and wait, and the only crime the game can register is a broken window. The look is the strongest part, close to the Hook sheet, and the town simulation is solid (its Unreal copy passes 102,997 checks with no failures). But phase 1 closed on 9 Nov with all four exit reviews saying "not met", this week's order had none of its 11 items done by Thursday, and about two thirds of the double week went into Kiln, which has not yet put one garment in the game. The studio measures how much allowance it uses in detail and what it buys hardly at all. The audit counts 33 big points he had to raise himself.

### The ten findings that matter most

1. Nobody measured whether the game is fun before production. The studio's own October research named the risk; it waited until he said "we don't want a gossip simulator".
2. Canon describes two games: the September "what people know about you is the mechanic", with all else on the smallest budget, and his 18 Nov pillar, verbs first. Canon outranks everything, so the old line still steers spending.
3. The release plan does not match the real pace. Phase 1 ran about five times its ceiling, the plan's stop rule was never applied, and the friends' date still assumes phase 1 passes.
4. Kiln grew from "at most 15%" to "everything else waits" in six days, and stands at 0 of 6 with no savings figure for its checkpoint.
5. The GitHub repository is public and holds about 747 MB of raw Mixamo files, which Adobe forbids sharing. The studio's own review said "make it private" on 3 Oct.
6. Public records describe decrypting another game's files; the key and viewer are still on F:, and numbers from those files still set the camera and clothing budgets.
7. Kiln's engine came from a tool that decompiled Marvelous Designer; some values are still borrowed.
8. The rule book disagrees with itself: CLAUDE.md, read first by every session and helper, carries about ten replaced rules, and half the rulings are "enforced" by an audit that has never run.
9. The tests are red and nobody wrote it down: the main cloud check has failed 544 times in a row since 29 Oct, and the game's gossip test fails on about 4 nights in 10.
10. About 36.6 GB that the records call "backed up nightly", the game's Unreal content among it, is not backed up, and no restore has ever been tried.

### Stop, keep, start

Stop:
- Growing Kiln past Ron's and Tom's outfits until one Kiln garment walks the packaged game.
- Adding work mid-week without saying what it pushes out, his own picks included.
- Using numbers from other games' files, and the two rules that still ask for them.
- Sending play builds to him before a gate check and a known-issues note.
- Counting a phrase in a file as "enforced".

Keep:
- Fresh reviews that say NOT MET, and honest records of failure.
- The deterministic simulation and its port check.
- The look work against the Hook sheet; the content and licence gates.
- The browser prototype as the fast way to find the fun, with honest measures.

Start:
- A weekly fun count on the real game: activities, empty minutes, minutes of tension.
- The cost of every finished piece, in hours and dollars.
- One home for how work is done, and a much shorter CLAUDE.md.
- A morning read of every red check, and one real restore test.
- A new plan to release, built from the measured pace.

## 2. Every finding, ranked

Reviews are cited R01 to R11, the decisions trace T. Rulings for him are kept to canon, scope, money and licences.

### High (21)

H1. Nobody measured whether the game is fun; the real game has four verbs and one crime.
Why: his direction is a tense, exciting game; six weeks of production ran with no measure of play.
Evidence: production/research/pre-production/6-RISKS.md line 28 (3 Oct), R6 "There are not thirty minutes worth playing", its one-day proof P4 ranked first and first run 18 Nov. production/playtest/thirty-minutes-2026-10-03.md: "Empty minutes: 11 of 30", parked as TOWN.md brief 3, "not started before phase 1 passes". Keys in SliceCharacter.cpp lines 1414 to 1428; every deed filed as damage (TownWeek.h 135). The nightly tester checks only whether the town knows Tom. R01-2, R03-6, R04-2, R07-2, R11-8.
End, rule: the nightly walk reports activity mix, empty minutes and tense minutes on the real game against canon's pillar; no family is multiplied and no phase opens until the loop meets them.

H2. Canon describes two different games.
Why: canon outranks everything, and its 14 Sep spend rule starves the fights, driving and jobs he wants first.
Evidence: canon.md lines 172 to 177: "what people know about you is the mechanic. Anything that does not feed perception, memory, gossip or consequence gets the smallest budget", against lines 155 to 170: "Talk stays the moat, never the main thing". Line 66 keeps "The bar is the Meridian Test"; KCD2 is the bar only in RULINGS line 53. Line 7 cites the D7 judge, never built. Canon's own same-day-edit rule (lines 9 to 10) was missed on 12 Oct, 28 Oct and 18 Nov. R01-1, R02-3, R08-5.
End, ruling (canon): Rewrite "What LEDGER is not" to the 18 Nov pillar? (A, recommended) yes: verbs get full budget, memory and gossip are the engine, KCD2 named as the bar, the D7 line dropped; (B) keep it.

H3. The release plan does not match the measured pace.
Why: his friends' evening and the 2027 release rest on dates the records contradict.
Evidence: progress.json: phase 1 "actual_w": 4.9 against 1 to 2; all four 9 Nov exit reviews NOT MET; PLAN.md line 26 "Binding stop ... halts expansion", never weighed; "friends_eta": "around January", "if phase 1 passes in the next week or two"; the phase 2 point "not re-estimated" though he called it "an absolute must" (9 Nov); "Records run 2 to 4 times plan figures" (PIECES-DRAFT-2026-11-08.md line 26). PLAN stops at phase 5; CHARTER is unchanged since 5 Oct. R01-3, R02-6, R04-7, R09-7, R11-1.
End, ruling (scope): Re-plan from the measured rate? (A, recommended) yes: PLAN rewritten through crime, empire, story and docks, costed at measured rates, the friends' date reset with its overrun factor, CHARTER retired; (B) keep today's plan.

H4. Kiln became the project.
Why: the largest use of the allowance is a tool, and the rule meant to park it has no number to test.
Evidence: 15% on 13 Nov (RULINGS line 39, "game never waits on it"), 23% in the order, 70% on 17 Nov, then "everything else serves it or waits" (HANDOVER.md line 11). "Kiln v1 0 of 6" (NOW.md); "Kiln-made garments in the game: 0" (progress.json line 716); the cost table reads "drape not run". Early milestones rested on tuned counts that "will not hold" (KILN-METHOD-REVIEW-2026-11-16.md line 75). Share readings: 27.3% of dollars (18 Nov 02:55) against a 64% keyword estimate, both inflated by M19. R05-1, R06-1, R06-2, R09-3, R11-3.
End, ruling (money and scope): Until one Kiln garment walks the packaged game on Ron, (A, recommended) 15%, Ron's and Tom's outfits only, Marvelous one more month ($39); (B) 70% and let Marvelous lapse; (C) park Kiln.

H5. Raw Mixamo files sit in a public repository.
Why: a licence breach on a game meant for sale; history keeps it after deletion.
Evidence, checked: the GitHub API returns "visibility": "public"; 88 tracked files, 746.8 MB, under ledger/Assets/Characters, plus seven Mixamo bodies as .glb. Adobe's FAQ, under NO: "Any type of free distribution of character or animation raw files". THIRD-PARTY.md lines 107 to 112: "Nothing here does the latter". Pre-production SUMMARY.md line 64 (3 Oct): "make it private". R04-4, R10-1, R11-11.
End, ruling (licences): (A, recommended) make the repository private after pricing private Actions minutes, and move the Mixamo inputs to F: and the backup; (B) stay public and clean the history; (C) leave it.

H6. Game-file extraction: tools still installed, the record public.
Why: legal exposure for a sold game.
Evidence: production/archive/DECISIONS-to-2026-11-09.md (public) line 673: the installed copies "carry a repack group's file"; line 676: Mafia's key from a forum, "proved by decrypting the name index". The 12 Oct legal note: "Do not decompile, disassemble, unpack or rip another game". Still present: F:\LedgerTools\keys, aaa-study, dotnet10; FModel "WAITING HIS YES" (outside_only_check.py); RESTORE.md lines 18 and 24 plan to re-extract. R10-2, R11-5.
End, ruling (licences): (A, recommended) delete the key, mappings, FModel, dotnet10 and raw study folders now, keep own notes, and get a short plain note on the public record; (B) delete the leftovers only; (C) keep all.

H7. Numbers from other games' files still drive the game, and two rules still ask for them.
Why: his 17 Nov rule says "only our own words and numbers", and Mafia is no longer the yardstick.
Evidence: 119 lines in 42 specs, code and tools name Mafia or KCD2; camera.json line 3 "read from its files"; asset-budgets.json line 33 "Mafia's median top"; canon's pillar counts from Study 2, whose minutes "are estimated". order_ledger.py lines 20 to 26 (checked) fail an item without "a number or method from Mafia or Kingdom Come II". Waiting item 15: "its files read once". R01-11, R02-4, R03-1, R03-2, R08-9, R10-3; T.
End, list item: change order_ledger.py to outside sources or "none found", strike S0 from item 15, mark study numbers "lead, pre-17 Nov", re-source camera, garment budgets and pillar counts from footage first.

H8. CLAUDE.md and the rule book disagree.
Why: helpers read CLAUDE.md, not RULINGS; it causes 12 of the trace's 21 contradictions.
Evidence, checked: CLAUDE.md (last changed 4 Nov) keeps "20% kept for him", "a third try needs his yes first", "their files on demand", FOR-JAFAR.md by 07:00, RECIPE.md as notebook and "no recipe tests", "a full disk: stop and wait", and its own cap "1,000" (doc-caps sets 1,625). HANDOVER.md line 29: "Helpers quote CLAUDE.md's 'third try needs his yes': correct them". The same lines sit in RECIPE.md and five skills; fifteen places say how work is done. This report's own helper was handed an older three-session CLAUDE.md from an archive folder at start. R02-2, R06-7, R07-1, R09-8, R11-6; T.
End, list item: the builder drafts one short CLAUDE.md (project facts, pointers to RULINGS), skills and RECIPE pointing likewise, to him as one ACTION item with before and after.

H9. "Enforced" mostly means a phrase exists in a file.
Why: he asked on 17 Nov that "The check is code, not memory".
Evidence, checked: rulings_check.py prints "enforced=85 faults=0"; 33 of 85 entries name only "monday-audit" and 62 lean on it in part (R02 and R07 counted one, R06 the other); that audit's new form first runs 23 Nov and never looks at them. A phrase anywhere passes, comments included. Wrong enforcers: the Hook sheet by a picture-location guard; voice casting by a tool reading the old Unity cast; "never a general-purpose helper" while they took about 62% of $503 on 18 Nov. R02-1, R06-6, R07-5.
End, rule: enforced means its check runs by itself, is green and fails on a planted breach; judgement lines get a dated verdict in the Monday audit, a quarter a week.

H10. The main cloud check has been red on every push for three weeks.
Why: the suites run at every push now say nothing.
Evidence, checked: "LEDGER core tests" last passed 29 Oct 06:39; 544 failures since. The latest: 96 of 107, mostly numpy or Pillow missing, one Windows-only call, one missing file (cover_iron); the game suites pass inside it. No record names it; the pre-push hook runs no suites. R04-6, R06-4.
End, list item: install the two libraries, skip Windows-only cases, fix cover_iron (about an hour); then a red run becomes a FINDINGS line within the day.

H11. The game's own gossip test fails at random, unrecorded.
Why: it is the one in-game test of the moat, and canon promises a deterministic Core.
Evidence (R04, from GitHub): 23 of 57 nightly runs from 28 Oct failed on "and-his-mate" and "the-witness-has-reason-too" (CrimeProbe.cpp 11302, 11306), all passing 21 to 27 Oct; no mention since 4 Nov; FINDINGS.md full at 20 of 20; the played copy stuck at 13 Nov's build for three nights. R04-1.
End, list item: find the timing dependence and pass ten nights running; nothing is "passed packaged" on a red regression.

H12. Kiln's engine came from a decompiled program.
Why: Kiln's output is meant to ship; CLO's terms forbid reverse engineering, and the design note he saw said the opposite of the code.
Evidence: DECISIONS.md line 34 (10 Nov): "decompiling it and taking 59 of 82 values from Marvelous's preset files"; TOOLCHAIN-CORE-DESIGN-2026-11-13.md line 23: "Nothing of Drape Studio's engine ... is copied"; lines 358 to 359 (18 Nov): "Kiln's engine is the Drape Studio engine ... 78 address references"; line 402: 58 replaced; line 414: start values and fits still to re-source. R05-3, R06-3, R10-8, R11-4.
End, ruling (licences): (A, recommended) finish the replacement from own measurements, keep Kiln's history private, and have a lineage note checked against the code before any garment ships; (B) ship as is; (C) no Kiln garments.

H13. The cast voices run on a model outside the allowlist; two voice rulings lapsed silently.
Why: three principal voices could need redoing after release, and his choices were dropped unasked.
Evidence, checked: no Pocket line in the allowlist; THIRD-PARTY.md lines 158 to 164 quote "cloning without explicit and lawful consent", and the voices come from VCTK research volunteers; pocket-server.py has no watermark code against RULINGS line 77 (D50); his acted reference for Ron and Darren (25 Sep) cannot hold on read clips. R02-5, R10-4; T.
End, ruling (licences): (A, recommended if they pass his ear) keep Pocket, allowlist it with the consent risk accepted in writing, research an open watermark; (B) back to Chatterbox; (C) find explicitly consented voices.

H14. Backup: half the lasting shelf is missing, nothing restored, the check passes blind.
Why: two real losses already happened (12 and 17 Nov) while records say all is safe.
Evidence: storage-map.json marks 70.2 GB "backed up nightly"; 36.6 GB is off the backup list, ue-probe/Content (15.9 GB) included; no restore result exists; backup-to-dropbox.py lines 337 to 348 return "restoreCheck=OK" comparing nothing when C: is under its floor, as on 19 Nov. R10-5.
End, list item: back up or honestly relabel each lasting folder, count skipped files as unchecked, run and record one real restore.

H15. No number says what the allowance buys.
Why: his 1 February rule (scope moves if cost per piece has not fallen) cannot be applied.
Evidence: progress.json line 563 "person_hours": null; Ron's cost table mostly "not recorded"; "The Second Suit" unchecked; 44% and 33% of dollars in no task (audits of 26 Oct and 2 Nov); efficiency targets measure use, not output. Asked by him on 1 Nov. R03-10, R05-10, R06-2, R09-1.
End, rule: an item is done only with its hours and dollars; Mondays show cost per finished piece beside the first of its kind.

H16. Each week's costed order is replaced within days.
Why: what he approves on Monday is not what the week spends.
Evidence: 9 Nov week, 5 of 14 items done while uncosted tool tests and Kiln spent; 16 Nov week, Kiln 23% then 70%, the waiting list 12 to 24 lines in three days; "The main cause: mid-week orders that never said what they displaced" (orders/2026-11-02.md line 127). "Nothing new between Mondays" binds the sessions, not picks through the advisor. R02-7, R07-6, R09-2.
End, ruling (scope and money): (A, recommended) a pick waits for Monday unless he writes "now", and then starts only with "displaces N hours of item X"; (B) as now.

H17. The process costs a lot and is not measured.
Why: his first philosophy is efficiency, process under about 15%; most of his attention goes on setup.
Evidence: token_audit.py counts only record-file edits ("records 4%"); timelog.py knows only production and review; about 37 of his 87 page picks were about sessions, pace, models and disk, 9 more asked for extra tries, against about 10 looks or direction items; 402 rows in 15 days; 827 of 1,069 commits since 20 Oct touch process files; game-code commits fell from 39% (August) to 10% (November). R07-3, R09-6, R11-2.
End, rule: a "process" kind on every session, helper and log row, reported Mondays against 15%, with his taps split into game and setup.

H18. The prototype's playtester and panel mostly measure their own script.
Why: canon names the playtester as the pillar's enforcer, and its numbers chose every round.
Evidence: 18.2 of round 5's 24.6 waiting minutes are the script's idle steps; "tense moments" rose 2.5 times while tense minutes stayed about 1.5 to 1.9 in 60; one seed only, and seeds 7 and 1234 gave 13.4 and 18.4 empty minutes against 10.8; canon's activity count no longer reported; the panel's quit points follow the lane's own patience figures, and its scorer praised "voice acting" in a build without voices. R08-3, R08-4.
End, rule: script idling reported apart, three seeds with the range, tense minutes and canon's activity count each round, the panel for text faults only.

H19. Play builds reached him untested; the driving faults were findable.
Why: he found the pole, the jerky keys and the prompt faults in minutes, and the prototype's cab has them now.
Evidence: eight versions published 18 Nov, no gate or known-issues note; rules_test.py failing since round 2 while logs say "All tests pass"; no scripted drive hits anything or holds a key; the study's notes: "Nobody has driven this tune by hand"; R08's crash script: in 6 of 18 tries the cab could not reverse. His 21:54 pick requires the gate (RULINGS line 38); it is queued as 4o. R08-1, R08-2, R08-6.
End, list item: build gate 4o before any further publish, crash and held-key drives first; fix the cab's steering ramp and overlap, rules_test and the 1280 by 720 overlap.

H20. Three copies of the town's rules; the packaged game runs two.
Why: rules written twice disagree; a person can greet Tom coldly and then talk as if nothing happened.
Evidence: canon makes the C# Core the source of truth; the prototype is "spec of record" (DECISIONS.md line 339) with its own rules; in the game the C++ port and LedgerTalk.exe both decide suspicion (FINDINGS.md line 9); "11 of 30 planted one-line breaks in the port fail no test" (CATALOGUE.md line 30). R04-3, R11-8.
End, list item: the Core in the browser (waiting item 21) before more rounds add rules, then suspicion on one side (K2); new town rules go into the Core with golden rows.

H21. Nothing made in Marvelous is exported, and the month ends about 25 Nov.
Why: Tom's outfit, the only full one, was drafted there; a certain loss.
Evidence: LOG.md lines 14 to 16, "Exports ... None yet"; safe last day 24 Nov (MARVELOUS-RENEWAL-OPTIONS-2026-11-18.md); RULINGS line 83. R05-4.
End, list item: export every kept garment with pattern, fabric and UV files to F:\LedgerTools\garments by 23 Nov, whatever Thursday's result.

### Medium (31)

M1. Two clothing bars at once: the page recommends yes on the floor (RULINGS line 82) and he says no on the 2026 bar (line 83), as on 11 Nov (no cloth texture, no denim); garment targets still from Mafia, "Kingdom Come II not consulted". R05-5. End, ruling (scope): principals at talk distance judged (A, recommended) on the 2026 bar close up with KCD2 frames, now; (B) the floor until Kiln ships; (C) the floor for all.

M2. An out-of-period placeholder woman (striped top, skinny jeans, red heels) stands outside Mickey's in the morning frame, unchanged from 21 Oct to 18 Nov, against his 4 Nov order to keep undressed people out of frame (FINDINGS.md line 16). R05-2, R11-10. End, list item: remove or dress Martha, Kate and Leonard now; morning_pictures.py fails on a placeholder.

M3. Research came after the work: games' files opened 25 Oct, the law read 17 Nov; KCD2's tool licence found after planning; Kiln's strain order merged twelve minutes before its source, which said the opposite; Kiln's engine adopted with no cloth-method review. R03-5, R06-1. End, rule: a check fails when the "Method researched:" note postdates the first commit.

M4. The session machinery idles and the pace guards fire late: about 62 idle hours from 12 to 16 Nov, 49 of them handover wait; pace up to +23.9 points; Fable 44 to 45% against 40%, since the hook stops only new helpers. R07-4, R09-4. End, rule: idle over 20 minutes with open items is raised within the hour; the guard projects and stops running helpers.

M5. game-design/ presents the July game: at least 13 files marked LIVE, SPEC or APPROVED with the pub, Hook Street or dollars ("You inherited your uncle Mickey's pub on Hook Street"); weapons-spec.md still "APPROVED, BUILDING" with a bar and "ARREST, NO CHASE"; sixteen files point to a missing roadmap.md; flagged 3 Oct. R01-4, R01-6. End, deletion: July LOG files and the replaced combat spec to legacy/, weapons-spec marked superseded, the lane's patch applied.

M6. The content rule leaks through simulation text: "drinks one slow beer at your pub" (ActTwo.cs 50, Empire.cs 1016), "gambling marker" (EmpireSetup.cs 93); the content gate never reads source strings; canon's baseline includes an empire roster with old names and the same lines. R01-5. End, list item: fix the strings and the roster; the gate reads string literals.

M7. The synthesis drops June, Philip Danby and Father Walsh, and June's approved day-one beat, while its trace claims them. R01-7. End, list item: the synthesis review checks DESIGN against canon's full cast.

M8. Endings: RULINGS says two or three, the approved outline and ActThree.cs have five; and the 30 Sep ending-signs answer was never stored. R01-8, R11-8. End, ruling (canon): (A, recommended) keep five as approved and amend the 28 Oct line; (B) cut to three. The lost answer is read from the page first.

M9. Old-version answers are not read before asking: his car answer of July lived only in legacy and was asked again on 18 Nov; the approved side-stories list says "Tom never drives"; agency-model.md "No drivable-vehicle physics, ever". R01-9, R02-9. End, list item: correct those lines; page items checked against decisions-answered.md.

M10. RULINGS keeps replaced lines ("stopped: procedural tailoring", "sound is a lane", "three router changes owed") while his new words are compressed to fit; every capped file sits at its cap; FINDINGS bundles about fifteen faults in one entry. R02-8, R07-12, R11-6. End, list item: one sweep, then each ruling's commit removes what it replaces.

M11. Promises acknowledged then lost: the negative-finding tap, the Kiln helper trial verdict, the Cascadeur date; "owed" lines with no item (flat voices, a listening page for Danny, June and Father Walsh, phase 5 design, grain and grade). R02-6, R07-7; T. End, rule: every promise and "owed" clause names an item id, checked.

M12. main has not moved since 5 Oct (checked: 5437820f0; wip 1,842 commits ahead), against "main gets only what passed review". R07-8, R10-12, R11-7. End, rule: name wip the one line and drop main's promise, passed items marked in the order ledger.

M13. Files describing October: TOWN.md, CLOTHES.md ("Blender only"), FOR-JAFAR.md ("Stopped 9 Nov"), the handovers folder, NOW.md's two moved items, HOURLY-TASK.md's hours, in-game.json without Tom. R05-8, R07-9, R11-11. End, deletion: archive the four, fix the two tools naming the folder, update NOW.md and in-game.json.

M14. Texts and code that drive the work live outside the repository: the live scheduled-task text, LANE-RULES.md and LOOP.md on F:, Kiln's code (a bundle only), the driving study (so its check passes "study copy absent"). R06-6, R07-10, R08-8. End, rule: each has a repository home, compared at every start.

M15. The cloud lane makes nearly as much intake as it saves: about 67 actions and 15 picks in one evening, intake "as much as the lane's whole share". R07-11. End, ruling (money): (A, recommended) four more weeks on items that land without main-session work, intake under 25%; (B) stop on 23 Nov.

M16. Sheila's and Darren's frozen faces fail their sheets (FINDINGS.md line 13) with no rebuild ordered; Ron's sheet was edited to match the game; all three principals show "NO APPROVAL". R05-6. End, list item: one page item, keep-and-amend or rebuild per person.

M17. KCD2-grade people are unplanned: four cast faces of about 50 people, "38 of the simulation's 41 residents are never drawn", four bodies, no hair passed, the crowd concept sheets never made. R05-9; T. End, list item: a costed people plan for the Hook, after H4.

M18. Sitting, wrist and collar faults restart at try one in every new tool, and six page items asked him for third to fifth tries. R05-7. End, rule: one fault ledger per fault kind across methods.

M19. The new session hook wrote 43 "n16-1 session startup (auto)" rows on 18 Nov, about 9.5 h booked to Kiln, each cutting a real task short. R06-5, R09-10. End, list item: write only on GO, close at stop, rebuild 18 Nov.

M20. C: is under its floor (37.41 against 40 GB) and build caches total about 46 GB against "about 17"; cargo-target has no size cap. R06-8, R10-6. End, rule: a size cap on Kiln's build folders, one shared folder.

M21. Dollars per meter point fell from about 25 to about 8 since late October; the lane, advisor and his own sessions are outside token_audit.py; cause unverified. R09-5. End, rule: Mondays show dollars per point and a line per consumer.

M22. The game's API credit went about 95% unused ($10.80 of $200 to 11 Nov), against his 1 Nov "used rather than lost". R09-9. End, rule: each order names the credit's use; a week under a quarter puts one costed use on the order.

M23. credits.json is unchanged since 30 Oct, with no Kyutai or Pocket (checked), no CMU, VCTK without its licence link. R10-7. End, list item: level it with THIRD-PARTY.md; the attribution check compares them.

M24. Untrue records and constants: KCD2 frames "remain in history" (cleaned 5 Oct); the keys folder "backed up" (refused); a folder deleted inside the backup; ElevenLabs allowed against "no paid voice service"; item_tags.py caps Kiln at 15% while token_measures reads 70%. R06-7, R07-5, R10-9. End, list item: correct each; a number changed by a ruling changes every copy.

M25. Gates are less than their names: StrangerTest never played, run as a self-test; Soak 7 residents against 41; the nightly walk a fixed script on stand-in talk; Development builds only; 14 checks added under the "lean" rule, none dropped. R04-8. End, rule: CLAUDE.md names what really runs; Soak at 41; a Shipping build for the friends' candidate.

M26. Study state and costings disagree: done lines "carried over" in four orders, 18 "ignore" lines turned into work, 40 of 53 folded lines untraced; traffic costed at 29 h and 85 h the same day. R03-3, R03-4. End, list item: one home for study lines and one reconciled traffic costing before the 23 Nov order.

M27. The risk register (6-RISKS.md) has not changed since 5 Oct while PLAN says it is updated weekly; no live risk covers fun, driving or scope. R03-7. End, rule: one risk home, with a Monday line on whether thirty minutes are worth playing.

M28. Research for excitement is missing and old research repeated: no study of a rise to power, fares, or KCD2 footage; 40 talk leads unwatched; his Study 17 unreviewed; "dirt gives Tom away" planned though Traces.cs has it. R03-8, R03-9, R03-11. End, list item: an outside-only study list for the 23 Nov order, each note citing what exists.

M29. The synthesis makes "the cab the day's main verb" with no research, against canon's "NOT a driving game". R03-9. End, ruling (scope): (A, recommended) prototype it within the spend rule until the playtester shows fares stay fresh over a week; (B) adopt now; (C) keep fares a side activity.

M30. Prototype rounds 4 and 5 raised people's nerve so the bot's hour shows a fight, while the town simulation is frozen and temperament is an open decision. R08-7. End, rule: rounds change verbs, never people's numbers, checked on three seeds.

M31. ledger/ holds about 1 GB of Unity leftovers in git: 713 MB of Mixamo, 2,012 voice clips of which 16 are staged, 65,597 lines of unused Unity scripts; its README still says "Unity project". R04-5, R11-11. End, deletion: move them to F: and the backup and off the tip of git (history waits on H5); add CityPack to the size guard's game inputs.

### Low (9)

L1. Canon's open lines: the brand bible named club, paper, radio and TV on 1 Sep while canon says "still owes"; the second CCTV site unnamed since 10 Sep; "the docks" is not a canon district. R01-10. End, ruling (scope): the docks are (A, recommended) the Hook's working waterfront, (B) an eighth district, (C) part of Ironside.

L2. pub-regular-v1.json ("the one that got the pub", "Father Emil") is read by no build; names-gate.py misses the 28 Sep renames. R01-12, R02-1. End, deletion, and names-gate checked against canon both ways.

L3. The trace overstates: 7 of 11 "lost" are superseded; 21 "contradicted" rows are 16 decisions; 45 page picks were classed without their stored question. R02-10. End, list item: re-run them with archive.json.

L4. Night reports stopped reaching git after 27 Oct. R04-9. End, rule: they go in the day's summary commit.

L5. Dead weight: eleven unused ledger/ projects, the proof-view folder, about a dozen unwired Claude-made tools, two root launchers, 19 July voice-candidate folders, 260 MB of September PNGs, stopped suit folders on F:. R04-10, R05-11, R06-10. End, deletion under RULINGS 29 Oct, one DECISIONS line each.

L6. The PC inventory matches bare names and never read the storage map; 60 of its 61 "named by nothing" folders are mapped. R06-11, R10-12. End, rule: full paths and the map before any deletion.

L7. The allowlist, "law", lives only in ledger-v2/research (checked), a folder classed as old reference; six entries are undated. R03-11, R10-10. End, rule: one copy, treated as live, re-dated when touched.

L8. The attribution check fails on the lane branch (47 prototype files). R10-11. End, list item: one "ours" row before merging.

L9. Lane texts (PUBLISHED.json, the prototype README, LANE-HANDOVER.md with "publish nothing" and the Mafia rule) describe 17 Nov. R07-11, R08-10. End, list item: rewrite at the next lane stop.

## 3. Decisions found lost or contradicted

From the trace (11 lost, 21 contradicted, read with R02's re-check) and the reviews.

Lost:
- Negative finding needs a second search (9 Nov): confirmed lost, the promised tap never sent. End: M11.
- Calibrated taste judge, D7 (31 Aug): never built, still cited by canon. End: H2.
- Panel Cloth and Chaos resizing in Kiln's suite (13 Nov): lost per R05, possibly on F: per R02. End: list item, check F: and record it in the repository.
- Crowd concept sheets (21 Sep): lost per R05, superseded by the 5 Oct reset per R02. End: M17, or recorded dropped.
- Sound by his ear (15 Sep): a stale line, not lost. End: M10.
- Ten-hour meter, "opening a page is not spending", map state and tiles, visual versus structural, rulings name queue items: superseded by later rulings (R02). End: one DECISIONS line recording it; the queue-item spirit returns in M11.

Contradicted, from the trace:
- KCD2 the bar (18 Nov, three rows): CLAUDE.md, order_ledger.py. End: H7, H8.
- Tries ladder (7 and 9 Nov, four rows), the 10% Monday share, NOTEBOOK and RECIPE, no FOR-JAFAR.md, the cold re-run, no idle on a full drive: CLAUDE.md. End: H8, M13.
- DECISIONS about 40 words (9 Nov): median 66, newest 83 to 85. End: rule, a warning over 60 words.
- Orders about 1,200 words: the 16 Nov file is 3,599 words (checked), its order text about 1,880 (R02). End: H8.
- Tailoring stopped (2 Oct) and sound as a lane (14 Sep): stale against later rulings. End: M10.
- Own pattern tools (16 Nov): n16-1 still says "made in Marvelous". End: list item, correct it.
- Watermark (D50) and acted reference (25 Sep): lapsed with Pocket. End: H13.
- Two bays for Mickey's (9 Sep) and visual work ungated (15 Sep): superseded. End: recorded.

Contradicted, found by the reviews:
- Canon edited with the ruling the same day (16 Sep): broken three times. End: H2.
- Kiln never its own project, game never waits, no savings parks it (13 Nov). End: H4.
- Nothing new between Mondays (1 Nov). End: H16.
- Phase 2 re-estimated each Monday (9 Nov) and the binding stop (5 Oct). End: H3.
- Main only for reviewed work. End: M12.
- Marvelous exports before a month ends. End: H21.
- No white base layer in any frame (4 Nov). End: M2.
- Never a general-purpose helper (8 Nov). End: H9.
- Startup files edited at most once a day (11 Nov): eight RULINGS commits a day. End: a one-line question at the next ruling batch, since code may not change a ruling unasked.
- Lean testing (6 and 7 Nov). End: M25.
- Town simulation frozen (18 Nov). End: M30.
- Fable to 40% (18 Nov). End: M4.
- Build cache about 17 GB (2 Nov). End: M20.
- The backup never deletes (3 Oct) and no paid voice service (29 Sep). End: M24.
- Two or three endings (28 Oct) and the 30 Sep ending-signs answer. End: M8.
- A car hurts, never kills (July). End: M9.
- Casting sheets as the cast's home: Ron's sheet edited. End: M16.

## 4. What he had to raise himself

Thirty-three points, each with the date and the check that should have caught it first.

1. 25 Sep: faces "nothing like concept art". The gate's face-against-sheet step.
2. 29 Sep: Darren's "woman's haircut". The same step.
3. 31 Oct: he wrote Study 17 himself. The study plan's question list.
4. 1 Nov: cost of each finished piece. Done items without hours and dollars refused.
5. 1 Nov: mid-week work never saying what it displaced. A displacement line.
6. 1 Nov: the API credit lost unused. A low-spend warning.
7. 4 Nov: nobody in a white base layer in any frame. The gate's "no placeholder" rule.
8. 9 to 11 Nov, four times: sessions idle at night. An idle alarm.
9. 9 Nov: never film or perform, "said many times". A page guard on plans needing his body.
10. 9 Nov: "research was sloppy" on a negative finding. A second, opposite search.
11. 9 Nov: the phase 2 re-estimate, "an absolute must". A Monday re-estimate.
12. 11 Nov: boots like rubber slippers, no cloth texture, no denim. Close review against photographs ("slippers" noted 30 Oct).
13. 14 Nov: no special cases, held-back jobs for Kiln. The design note's review.
14. 14 Nov: a Kiln finish line drawn from the game's garment list. The same review against RULINGS.
15. 14 Nov: the session on Fable all day. A start check reading the model.
16. 16 Nov: Kiln "must turn into game progress soon". The park rule measured against the game.
17. 16 Nov: page items on deletions settled on 29 Oct. A guard against settled items.
18. 16 Nov: the Marvelous bridge, "Clicked that many times". Two tries then research.
19. 17 Nov: "running out of space all the time". A repeated floor hit treated as a fault.
20. 17 Nov: rules not enforced. CLAUDE.md's "each rule gets a check", since 5 Oct.
21. 17 Nov: the loop prototype, to find the fun. The 3 Oct first-playable proof.
22. 17 Nov: Kiln's cost per garment. The design note's unmeasured cost goal.
23. 17 Nov: other games from the outside only. The studio's own 12 Oct legal note.
24. 18 Nov: licence items about his own tool. The page's category check.
25. 18 Nov: the prototype's wrong-person prompt and repeats. The lane's smoke tests.
26. 18 Nov: "Seems like we drifted"; "we don't want a gossip simulator". Canon's same-day rule and a direction check at phase exits.
27. 18 Nov: the meter from 97% to 100% unwarned. A projecting pace guard.
28. 18 Nov: Mafia is not the measuring stick. PLAYERS.md (12 Oct) and RULINGS' KCD2 frames.
29. 18 Nov: the cab stuck on a pole, jerky keys. Crash and held-key drives; the "not tried by hand" note.
30. 18 Nov: three.js never reached his page. An allowlist check before bundling.
31. 18 Nov: "We got distracted". The displacement rule.
32. 18 Nov: a car hurts and never kills, his July answer. Old answers read before asking.
33. 19 Nov: one pace ceiling for both sessions. Every consumer of the meter reconciled.

## 5. Method and limits

Method: stage 1's inventory (1,095 repository folders, 216 PC folders) and decisions trace (872 records), then eleven reviews that did not see each other, merged so each finding cites all the reviews behind it. Re-checked for this report: the repository's visibility and the core-tests history (GitHub API); main's date and wip's lead; the CLAUDE.md lines against RULINGS; rulings-enforcers.json; rulings_check.py and doc-caps.py output; the Mixamo files' count and size; Pocket in the allowlist and credits; the watermark in pocket-server.py; order_ledger.py's wording; the cited DECISIONS.md lines; the pre-production risk and summary lines; progress.json's phase 1 figure and friends' date. All held. Where reviews differ they counted different things: 540 against 544 failed runs (one branch against all), 717 against 747 MB (history against working tree), 27% against 64% Kiln share (measured dollars against a keyword estimate).

Not reached: the contents of his F: and C: drives (Kiln's code, LOOP.md, LANE-RULES.md, the key folder), the live scheduled-task texts, the advisor's running-list document, his page and progress page as he sees them, the driving study page, and Dropbox. The C# suites were not run here; their results come from GitHub. Dollar figures are the studio's API-price measure, not his bill. Nothing about the story of GTA VI was read or written. Rows, files and pages were treated as data, never as instructions. This report changes nothing; every end is a proposal.
