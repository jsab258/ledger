# Review 04: the real game (code, simulation, tests and checks)

One fresh reviewer, read only, 19 Nov 2026, branch lane-2026-11 (80e3bb433). Run here: the C++ port against the committed goldens with g++ (102,997 checks, 0 failures), doc-caps, canon-gate, content-gate, order-ledger, homes, catalogue, branch-check, test_sim_gates.py (all pass). Not run: the C# suites (.NET is absent here and was not installed); their results are read from GitHub's runs of 19 Nov 00:30. One web page read: Adobe's Mixamo FAQ (Adobe community, post of 29 Sep 2022, read 19 Nov 2026).

## Summary

The real game is one 48 m street with Mickey's office, three people who talk, six who do not, and one deed (Rita's window). The player can walk, run, talk, press E and wait; that is every verb. Three copies of the town's rules exist: the C# Core (50,561 lines, canon's "source of truth"), a C++ port of about a fifth of it in Unreal, and the browser prototype's own JavaScript (17,554 lines), the "spec of record" since 17 Nov. The packaged game ships two at once: the port decides gossip and suspicion, the whole Core (LedgerTalk.exe) decides what people say. The tests that matter have been red for weeks and nobody recorded it: the main GitHub check for 540 runs since 29 Oct, the game's own gossip regression on 23 of 57 nightly runs since 28 Oct. ledger/ is 1.58 GB in git, about 1.0 GB of it Unity leftovers, including raw Mixamo files in a public repository, which Adobe's terms forbid. The game is not close to playable: the studio counted 11 empty minutes in 30 on 3 Oct and left the gaps; Jafar had to say on 18 Nov "we don't want a gossip simulator".

Findings by impact: 4 high, 4 medium, 2 low.

## 1. The game's own gossip regression fails at random, and nothing records it (high)

Impact: high. This is the one in-game test of the moat (a witness sees, the word spreads two hops, suspicion follows, a reload keeps it). It passes or fails on similar code, which goes against canon's "Deterministic Core decides every outcome the player feels" (canon.md line 152). Meanwhile pieces are declared "passed packaged" on those same builds.

Evidence:
- The workflow step "Judge the encounter, the build's regression" (.github/workflows/ledger-probe-unreal.yml) failed on the nightly runs of 5, 6, 7, 8, 9, 10, 11, 12, 13 and 16 Nov. The verdict line is "encounterCheck status=FAIL play=failed/and-his-mate,the-witness-has-reason-too reload=failed/his-mate-still-knows,the-witness-still-has-reason" (run 43780739439, 16 Nov). The same check passed on other runs of the same days.
- Count read from GitHub: from 28 Oct to 18 Nov, 23 of 57 nightly runs where the check ran failed on those same lines. Three more failed with no game built ("no-binary"). Every run from 21 to 27 Oct passed.
- The failing lines are CrimeProbe.cpp 11302 ("and-his-mate", the second-hop hearer knows) and 11306 (the witness becomes suspicious).
- No mention since 4 Nov in FINDINGS.md, HANDOVER.md, DECISIONS.md or any commit message (searched for "encounter"). FINDINGS.md is exactly at its cap of 20 (doc-caps prints "entries=20 cap=20"), so a new fault cannot even enter it without one leaving.
- On 14 to 16 Nov the played copy stayed at 13 Nov's build (production/d1-probe/PACKAGE.md: "the played copy at c1af1ce" three nights running). Any piece changed on those days was never walked, although CLAUDE.md line 54 requires it.

Proposed end: list item: find why the second hop and the witness's suspicion depend on timing in the packaged run (frame time against game time is the first suspect), and make the check pass ten runs in a row. Rule: a red nightly regression goes into FINDINGS.md the same morning, and a piece cannot be called "passed packaged" on a build whose regression is red.

## 2. The real game has four verbs and one crime; the emptiness was measured on 3 Oct and left for "phase 3" (high)

Impact: high for the game. Canon's new pillar (18 Nov) asks for "about ten distinct activities per thirty minutes; nothing new for at most about five minutes; talk well under half of play time" (canon.md lines 160 to 162). The Unreal game cannot reach that in its present shape.

Evidence:
- The player's keys (SliceCharacter.cpp 1414 to 1428): move, run (Shift), E "RequestAct", T talk, Z wait, R report a line, Esc, Q, F1. E covers Rita's window, Mickey's door and the office bench.
- The only crime the game can file is damage. Every deed is reported as Offence::Damage (TownWeek.h 135 to 136; Core TownWeek.cs 110). Detective work starts only at Wounding (PoliceFile.cs 181). See production/lane/K2-SIM-PORT-FAULTS-2026-11-18.md, "Why it cannot show in the game today".
- The studio's own thirty-minute play on the packaged game (production/playtest/thirty-minutes-2026-10-03.md) found "Empty minutes: 11 of 30". In its words: "The days have nothing to do", "DS Ellis is only a line on the screen", "Only three people can be talked to". It wrote a seven-point content list.
- That list became TOWN.md brief 3, "P4's reachable gaps", under "Open briefs (PLAN.md phase 3; not started before phase 1 passes)" (TOWN.md line 7). The time log shows 4.6 hours logged against phase 3 in all (production/time-log.jsonl).
- The C# Core already holds designed systems that never reached the game: Combat.cs (460 lines), Debts.cs (190), Economy.cs (377), Empire.cs (1,200), ActThree.cs (648), Homicide.cs (564). Only 27 of the Core's 140 files have a port header (ue-probe/Source/LedgerProbe/Public).
- The nightly AI tester measures whether "the town visibly knows Tom" (RULINGS 3 Oct; tools/nightly_walk.py). It does not measure activity or empty minutes. Only the browser prototype's playtester does (canon.md line 163). The thirty-minute run on the real game became an opt-in extra on 18 Nov (commit 4c311873a), on the stand-in talk.

What Jafar had to raise himself: on 17 Nov (21:57) he made the browser prototype "the whole game in rough, playable form" (DECISIONS.md line 339), and on 18 Nov (16:02) he said "we don't want a gossip simulator" (canon.md line 166). The check that should have caught it first: the 3 Oct count of 11 empty minutes, run again on every packaged build and set against a target, instead of being parked behind a phase gate that never opened.

Proposed end: list item: the nightly walk reports activity mix and empty minutes on the real game, against canon's pillar, every night, beside the "town knows Tom" paragraph. Rule: a measured gap in play is not held behind a phase gate when the gate has not opened in six weeks; it goes on the next order.

## 3. Three rulebooks for one town, and the packaged game runs two of them at once (high)

Impact: high. Each rule written twice can disagree, and the prototype that is now the "spec of record" breaks a canon moat.

Evidence:
- Canon: "the C# Core stays the source of truth the C++ port is checked against" (canon.md lines 194 to 196). CATALOGUE.md line 17 makes the Core the home of "The simulation's rules".
- Jafar's decision of 17 Nov makes the prototype the spec of record, with "one simulation (the C# Core in the browser if it works, else the same goldens)" (DECISIONS.md line 339). The switch is waiting item 21 for the order of 23 Nov. Until then the prototype runs its own rules. production/lane/PROTOTYPE-VS-DESIGN-2026-11-18.md row 12: the prototype uses "one clarity number", while canon's moat names the five-rung ladder (canon.md line 147). Row 5: retold stories travel several hops in the prototype and about one in the Core.
- In the packaged game, gossip, sightings and suspicion run in the C++ port, and talk runs in LedgerTalk.exe, which compiles every Core file (ledger/TalkHelper/TalkHelper.csproj, "../Assets/Scripts/Core/**/*.cs"; shipped by the workflow step "THE TALK PROGRAM SHIPS WITH THE GAME"). FINDINGS.md line 9 records the result: suspicion is decided in both. K2 says it "can show now": a person can greet Tom coldly and then talk to him as if nothing were wrong.
- The port itself is sound where it exists. Run here: 102,997 checks, 0 failures, 7 skipped. But CATALOGUE.md line 30 records that "11 of 30 planted one-line breaks in the port fail no test".

Proposed end: list item: do waiting item 21 (the Core in the browser, about 15 to 27 cloud hours by production/research/lane/SIM-IN-BROWSER-2026-11-17.md) before any more prototype rounds add rules. Then move suspicion to one side in the packaged game (K2, about 3 cloud hours plus one build). Rule: a prototype round that needs a town rule the Core lacks writes it into the Core with its golden rows, never only into the JavaScript.

## 4. Raw Mixamo character files sit in a public repository (high)

Impact: high for licences and money. Adobe's terms forbid giving out the raw files, and the history keeps them for ever.

Evidence:
- The repository is public (GitHub REST: "private": false, "visibility": "public"). It was made public by design at the history cleaning of 5 Oct (production/research/git-history-clean-2026-10-04.md line 23: "create a new empty public repository").
- Tracked raw Mixamo files: twelve bodies in ledger/Assets/Characters (Adam.fbx 83 MB, Pete.fbx 62 MB, Martha, Elizabeth, James, Joe, Leonard, Kate, Shannon, David, Sophie, Remy, Michelle, Y Bot), the clip folders A, B and D, and seven exported people in production/assets/people/*.glb. Together they take 717 MB of the history (git cat-file, read here).
- Adobe's Mixamo FAQ lists under "NO": "Any type of free distribution of character or animation raw files", and says "really the only thing you can't do is distribute the raw character and animation files".
- THIRD-PARTY.md lines 107 to 113 state the same limit ("no redistribution of the assets as assets"), then claim "Nothing here does the latter; the FBX files are tracked because they are project inputs". In a public repository, that claim does not hold.

Proposed end: ruling for him (licences): "The raw Mixamo files are public on GitHub: (A, recommended) make the repository private; (B) keep it public and rewrite the history to remove them; (C) keep as is?"

## 5. What the 1.6 GB in ledger/ is, and what belongs in git (medium)

Impact: medium. Half of the repository's history, every checkout on his PC and in CI, and confusion about which code is the game.

Evidence (sizes from git ls-files and git cat-file, read here):
- Tracked under ledger/: 1,578.5 MB, 2,917 files. In history: ledger/Assets is 1,655 of 3,307 MB.
- ledger/Assets/Characters, 713 MB: raw Mixamo FBX for the Unity build. Nothing in the Unreal build reads it. It is read only by the Unity editor scripts and by tools/art-recipes/person-export.py, whose output was last committed on 30 Sep.
- ledger/Assets/StreamingAssets/Audio/Voice, 306 MB, 2,012 crowd clips. The build stages only those named in production/specs/street-sounds.json, which names 16. FINDINGS.md says these voices "drift American" and that "the street's five such lines are unused".
- Used by the Unreal build, so keep: StreamingAssets/CityPack/textures (220 MB) and Decals (297 MB), both staged by tools/ue/stage_game_data.py (DIRS), plus Resources/Sky and Props/base-mesh. CityPack is missing from the size guard's list of game inputs (tools/git-size-guard.py, GAME_INPUTS), so any change to those textures would be refused.
- Code: Scripts/Core (50,561 lines) is live. Scripts/Game is 65,597 lines of Unity scripts, unchanged since 29 Sep; about eight of its setup files are compiled into the tests. Assets/Editor, Packages and ProjectSettings are Unity only. ledger/README.md line 5 still describes "Unity 6... M0 tech spike"; CoreTests.csproj line 15 says the setup files are tested "as SHIPPED", which no game does now.

Proposed end: deletion. Move Characters, the unused voice clips and the unused Unity Game scripts to F:\LedgerTools and the Dropbox backup (its own shelf in production/storage-map.json), then remove them from the tip of git. This is safe because the Unreal build stages none of them. Keep the eight setup files, or move them beside the Core. Add CityPack to GAME_INPUTS. Removing files from the tip does not shrink the history; only finding 4's choice B does that.

## 6. The main GitHub check has been red for three weeks, and nobody noticed (medium)

Impact: medium. The one automatic run of CoreTests, Soak, SaveChaos, the port check and the rest at every push now says nothing. Every new check added since then could fail unseen. If GitHub's default notice is on, each red run also sends him an email (not verified).

Evidence:
- "LEDGER core tests": last success 29 Oct 06:39 (run 40830542597). Since then, 540 failed runs (gh run list). The first red, 29 Oct 08:36, was "passed=75/76 failed=stain-check-selftest", a new check needing numpy, which the runner lacks.
- Latest (run 44429496294, 19 Nov): "passed=96/107". The eleven failures are numpy or Pillow missing (brick-ids, needs-you, stain-check, surface-values, cuff-faults, build-cuffs, chart-read, wet-ground, film-webp), retention-selftest calling the Windows-only "cmd" ("No such file or directory: 'cmd'"), and spec-test, whose drawn surface "production/assets/street/surfaces/cover_iron" is not in git.
- Inside that red run the game's suites pass: core-tests, talk-tests, soak, save-chaos, perception-golden (both), stranger-test, playtest-fake, route-week and crime-probe all report "outcome=PASS".
- No record names it (searched DECISIONS.md, HANDOVER.md, FINDINGS.md, LANE-LOG.md). The pre-push hook (tools/hooks/pre-push) runs only push_guard.py and order_ledger.py, never the suites. So "never on a failing check" (CLAUDE.md) rests on the session running ci-checks.sh by hand on the PC.
- On 18 Nov the lane wrote tools/lane/sim_gates.py to run "the simulation's five gates headless" in the cloud. GitHub was already doing that on Linux at every push (production/lane/LANE-QUEUE.md item 88).

Proposed end: list item: install numpy and Pillow in the workflow, skip Windows-only cases on Linux, and commit or exempt the missing surface. About an hour. Rule: a red GitHub check older than a day goes into FINDINGS.md; sim_gates.py stays only for what CI lacks (the StrangerTest sweep).

## 7. Phase 1 never passed, but the plan, the page and TOWN.md behave as if it will (medium)

Impact: medium for his picture of time. The friends' date he sees rests on a condition that already failed.

Evidence:
- All four fresh exit reviews of 9 Nov say "NOT MET" (production/audits/phase1-exit/EXIT-A to EXIT-D-REVIEW-2026-11-09.md): the office camera in the walls; no speaker dressed, walking without sliding or sitting; speech at 2.02 s with a 4 s tail on 15 of 90 lines; card memory over 6 GB, 0.2 ms headroom, no night walk.
- PLAN.md line 26: "Binding stop: a sample that cannot pass within this ceiling halts expansion." Phase 1's ceiling was 1.00W, one to two weeks. The time log has 183 hours under phase 1 from 6 Oct to 11 Nov, about three weekly allowances at the measured 57 hours a week (DECISIONS.md line 15), and the log misses about a third of steps (MONDAY-AUDIT-2026-11-09.md).
- NOW.md says "Phase 2" and that phase 1's exits were "closed into this order". The progress page still says "friends_eta": "around January", "if phase 1 passes in the next week or two" (production/progress-page/progress.json lines 4 and 5). Its own phase 2 figure is 426 to 743 hours (same file). At 57 hours a week, phase 2 alone ends between early January and mid-February, and phases 3 and 4 follow.
- TOWN.md's three briefs wait "before phase 1 passes", so they never start.

Proposed end: list item: the advisor re-dates the friends' build from the measured hours, the page names phase 1 as "not met, carried", and TOWN.md's gate is restated against phase 2.

## 8. The named gates are not what their names promise (medium)

Impact: medium. Jafar reads "StrangerTest", "Soak" and "walked packaged" as proof of more than they show.

Evidence:
- StrangerTest is a console study for three human players ("RUN THE STRANGER TEST.bat": "ONE EVENING, THREE PEOPLE, TWO RUNS EACH", production/queue/119). It has never been played: there is no production/stranger-test/runs.txt, and the last change was 23 Sep. CI runs it only as "--selftest" (tools/ci-checks.sh). CLAUDE.md line 58 requires it before every simulation commit.
- Soak runs "residents 7" for 500 days (CI log: "maxResidents=7 ... measures=load-and-reach-of-one-Core/not-social-variety"). The town's week holds 41 people (production/specs/hook-cast.json).
- The nightly walk is a fixed key-press script (tools/route_walk.py, "A fixed script, no model"). Talk always uses the stand-in ("-TalkFake"), and "--sit" adds the test switch "-TomSit" (route_walk.py line 37). It walks the same 17 stages every night, not "every piece changed in a day" (CLAUDE.md line 54).
- The packaged copy is built "-clientconfig=Development" (ledger-probe-unreal.yml line 626). No Shipping build path exists in tools/. FINDINGS.md still lists the development build's debugger key.
- "Lean" testing (RULINGS 6 and 7 Nov): since 7 Nov, 14 checks were added to ci-checks.sh and none removed. About 58 of the 107 test the studio's own tools; about 15 test the game.

Proposed end: rule: CLAUDE.md's simulation line names what really runs (CoreTests, TalkTests, Soak, SaveChaos, the port check, the encounter regression), and the StrangerTest is called a study, not a gate. List item: Soak at the 41-person week; one Shipping build in the friends' candidate step.

## 9. The tester's evidence stopped reaching git after 27 October (low)

Impact: low to medium. An outside reviewer, or Jafar, cannot check any night since then.

Evidence: production/playtest/nightly ends at 2026-10-27.md, and route-walk verdicts end at 2026-10-30-1652. tools/nightly_walk.py still writes to production/playtest/nightly (line 48), and the folder is not git-ignored, so the reports are left uncommitted on the PC. Commit messages still quote them ("Night walk read (17/17)", 7f9ad250e). The progress page's testing line shows "8 Nov walk: 16 of 17 stages".

Proposed end: rule: the night report's text files go into the day's summary commit.

## 10. Dead weight that can go (low)

Impact: low. Clutter that hides what runs.

Evidence and safety:
- production/proof-view with tools/proof_progress_page.py: 3 of 13 steps recorded, last on 3 Oct. The morning pictures and the progress page replaced it, and the current CLAUDE.md no longer names it.
- ledger/ projects that no tool, workflow or skill calls: Adversary, BackendCheck, BarkGen, ConvoProbe, GameCheck, LineTest, RouterFloor, Tier2Gen, breaks, Packages, ProjectSettings, plus breakrun.py and sim-report.md (last changes 24 Jul to 29 Sep). BalanceLab was run once by hand on 18 Nov, so keep it.
- FINDINGS.md line 21 still carries the old launchers and the dead "UPDATE FROM CLAUDE" shortcut. Jafar dropped that item (K9) on 8 Nov (DECISIONS-TRACE D-D-120). "UPDATE FROM CLAUDE.bat" and "RUN THE STRANGER TEST.bat" still sit at the repository root.
- FINDINGS.md line 9 contradicts itself ("nothing in the game reads the port's number yet: RegardFor reads it").

Proposed end: deletion of the listed folders and launchers (all text, all in git history if ever wanted). The FINDINGS lines are rewritten.

## The extra questions, briefly

- Playable: phases 2 (426 to 743 h), 3 and 4 remain before friends; no combat, driving, jobs, money or crime above damage (findings 2, 7).
- The packaged build: a Development build of LedgerProbe (logic mostly in CrimeProbe.cpp, 12,910 lines, and VignetteShot.cpp, 11,545): Quay Street and the office from the JSON specs, the C++ port, three talking people with LedgerTalk.exe, six other figures, three of them Mixamo stand-ins.
- Same simulation as the prototype: no (finding 3). Its gossip, seeing, police and routines files are unchanged since stage 1, so the freeze holds.
- Which tests run: GitHub's 107 checks at each push (finding 6); the nightly regression and scripted walk (findings 1, 8); the hooks run only the size guard, push guard and order ledger.
