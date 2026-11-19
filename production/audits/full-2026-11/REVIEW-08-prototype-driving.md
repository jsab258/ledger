# Review 08: the loop prototype and the driving study

Full audit, stage 2, area 8, 19 Nov 2026: branch lane-2026-11 (commit 80e3bb433), the prototype page (lane round 5) and the driving study page (round 3), both read only. The prototype was built here byte for byte, its tests run, the playtester run on two extra seeds and a crash test run on its cab. Nothing in the repository was changed.

## Summary

The prototype and the driving study are the right tools for his question (what LEDGER feels like, fast and cheap), and the lane moved the prototype quickly toward tension: a night carry under a constable's eye, fists with weight, a debtor who stands. But the numbers used to steer it measure the test machinery more than the game. Most of the playtester's "waiting" is its own script standing still, its "tense moments" rose two and a half times while the time spent in tense play stayed about 2 minutes in 60, and the reviewer panel's quit points follow directly from patience figures the lane chose. Both of his driving complaints sat in blind spots built into the method: every scripted drive steers by smooth script on an empty test ground, none hits anything or holds a key, and the study's own notes said "Nobody has driven this tune by hand" and named key steering "the first thing to try by hand". The prototype's own cab has the same two faults today. Three times on 18 Nov he found the faults first (the prompts and repeats at 13:02, too much talk by 15:19, the pole and the keys that evening), and each time a cheap check could have found them before he did. The rise to power, half of what he says the game is, is not tested at all and is scheduled last.

The brief's questions: same game, findings 5 and 7; still true, 6 and 10; used, 4; cost, the last section; missing, 1, 5 and 8; contradictions, 5 and 7; what he raised himself, 1, 5 and 6.

## Findings, ranked

### 1. The driving measures could not see either of his complaints (high)

Impact: high for him, because he found both faults in about three minutes of play, and high for the game, because canon wants AAA driving as the end state and the same method is meant to carry the Unreal car.

Evidence:
- All nine scripted drives (tools/lane/DRIVING-DRIVES-README.md, table D1 to D9) run on an empty test ground under script steering: none hits a wall, post or car, and none uses key input. Steering response, M5, is measured by "step the steering to a 2 degree road-wheel angle" (D5; FEEL-TARGETS-DRIVING-2026-11-17.md line 240). A held key drives the wheels toward full lock (38.5 degrees), not 2.
- The game set made response quicker on purpose: "yaw to 63% after a 30 mph step 0.15 to 0.25 s ... May answer quicker than real" (FEEL-TARGETS line 108). The study's keys ramp to full input at keySteerIn 6 per second (full lock in about 0.17 s) and snap back at 12 per second (page file source/src/params.js lines 130 to 131). No target exists for these rates. The lane's own research had the lesson ("a buffer sits between stick and physics so quick taps do not spin the car", FEEL-TARGETS line 144) and the round 2 prompt asked only that keys be "smoothed ... at set rates" (FABLE-DRIVING-NEXT-ROUND.md line 168), with no number.
- The study's keysteer test prints numbers with no pass line; its keylap test models a player who "taps about six times a second", never one who holds a key.
- Damage is designed so that "one big hit ends it" (page file source/src/damage.js header: "about 35 mph and over the car will not drive on"). A post takes the full closing speed, so a 35 mph pole hit strands the car by design; only R, a test-ground repair key, recovers it. Round 3 added "four light poles" (driving-round3-CHANGELOG.md line 185) with no check that a car hitting them can carry on.
- The study warned in writing: "Nobody has driven this tune by hand or played part B" and the low yaw inertia "may feel darty on the keys at speed ... that is the first thing to try by hand" (driving-round3-CHANGELOG.md lines 222 to 223). Nobody in the studio tried it; the lane may not play games (LANE-HANDOVER.md, rules) and the warning did not reach him as a known-issues note.
- He raised both on 18 Nov in the evening (synthesis/DESIGN.md line 183, "after the pole and the jerky keys"; his 21:54 pick, D-E-135). Which build he drove is not recorded; his desktop copy predates round 3 (tools/driving_feel_check.py).

What would have caught them: a crash-and-drive-away drive (each solid at 10, 20, 35 and 50 mph, then 5 s of reverse and steering; fail if the car has not moved 2 m or offered a way on) and a held-key drive (hold left 0.3 s and 1 s at 30 and 60 mph; time to full lock and peak yaw jerk against a band). DESIGN.md now writes both as rules (ER-DRIVE-01, ER-INPUT); no check exists yet (LANE-QUEUE.md item 4o).

Proposed end: list item: build the driving gate (4o) with those two drives first, run on every Fable driving page before he is told it is ready. Rule: any line in a build's notes saying "not tried by hand" or "may feel" goes to the top of the known-issues note he sees before playing.

### 2. The prototype's own cab has the same two faults now (high)

Impact: high. The prototype is the spec of record (D-E-114), and its cab is the one his next prototype session will drive.

Evidence:
- Keys go straight to the wheel: player.js line 389 turns A and D into -1, 0 or 1; drive.js lines 86 to 97 turn the car at that value times turnRadiansPerSecond 1.75 (rules.js line 972) from the first frame. No ramp in or out.
- On a hit, drive.js lines 102 to 121 refuse the move and reverse the speed at a quarter (bouncesBackShare 0.25), but the turn on line 86 is applied regardless. Steering while touching a post can turn the car into the post, after which every small move forward or back is refused.
- Scripted test, this review (headless; the cab placed 8 m before each of the map's free-standing posts at three offsets; W, then W with D, then S for 4 s, then S with A and W with A): 18 tries; in 6 the car did not move at all in 4 s of reverse; in 2 it was still within 1 m after 10 s. About three minutes to run; indicative only, as damage carried over between tries.

Proposed end: list item: before the prototype is next published, ramp key steering, push the cab out of overlap instead of refusing the move, never turn into a solid, and offer "get out" when the cab cannot move; keep the crash script as the gate's first prototype test.

### 3. The playtester's numbers mostly measure its own script (high)

Impact: high. Canon names it as the pillar's enforcer ("Enforced by the prototype's AI playtester, which measures the activity mix and empty minutes", canon.md line 163), and its numbers chose every round.

Evidence:
- Waiting is mostly the bot: in round 5, 24.6 minutes "waiting" are 18.2 of "nothing to do" (the script's own 15 s idle steps, playtest.py lines 945 to 946) and 6.2 in the cab, where the script sits two minutes every ten (lines 913 to 920). Rounds 2 to 4 are the same shape (18.0, 24.0, 18.2 minutes of "nothing to do"; production/lane/playtest-round2 to 5, report.json). The first report said so ("15 of the 23.5 minutes are 'nothing to do' steps ... it does not measure how long a human would stand idle", PROTOTYPE-PLAYTEST-1 fault 9), yet later rounds reported waiting as the game's.
- Walking and driving are teleports at assumed speeds (playtest.py lines 597 to 604, 726 to 735): the tester never meets a wall, a post or a key, as its own report admits.
- "Tense moments" rose from 7.5 to 19.5 per 30 minutes over rounds 2 to 5, while minutes in tense verbs (job actions, fronting up, fighting, running) went 1.6, 1.4, 1.5, 1.9 of 60. The count includes driving the cab at night ("cab_night, 1 witness") and counts each rung of one fronting-up as its own moment (round 5 newcomer.md: stare, threat, shove, strike, debt_paid at 21.1 min).
- Every round used the same seed (19901120). Run here on the round 5 build with seeds 7 and 1234: longest stretch with nothing new 13.4 and 18.4 minutes, against 10.8 on the published seed; waiting 46% and 40%. The lane's "run-to-run noise about 3 min" (REVIEWS-round4.md) is too small, and the round-on-round moves it reported (13.5 to 7.9 to 10.8) sit inside the real spread.
- Canon's first target, "about ten distinct activities per thirty minutes", is no longer reported (round 4 and 5 packets carry no activity-kind count; round 3 said 5 to 6).

Proposed end: rule: the playtester reports script idling apart from game idling, runs three seeds and gives the range, reports minutes in tense verbs rather than event counts, and prints canon's activity count each round; a round "moves a measure" only when it leaves the seed range.

### 4. The reviewer panel's numbers are not evidence about players (high)

Impact: high: its top complaint picked the topic of rounds 2 to 5 (LANE-QUEUE.md items 95, 97 to 99).

Evidence:
- Each reviewer reads only a text packet of the bot's hour and is told: "if the record shows a stretch with nothing happening longer than your patience, you would have quit there" (reviewers/PROMPT.md line 5). The patience figures are the lane's own, "an estimate, not a measurement" (CARDS.md line 3). Quit points and "hours before stopping" are therefore set by the bot's idle stretches and the lane's figures. Hours cannot exceed 1.0, since the record is one hour.
- Eight answers move a share by 12.5 points each, yet REVIEWS-round1 to 5 set them beside KCD2 and Mafia shares from 9,335 Steam reviews. The scorer's own notes say the original matched a hand reading "53 to 65 times in 100; use the order, not the sizes" (themes.py lines 7 to 8). Round 5 shows "Voice acting and performances" praised by 38% for a build with no voices, because the word list counts "dialogue" and "lines" (themes.py line 27).
- The calibration (REVIEWS-round1.md) proved only that a reader of transcripts notices repeated text; the theme scorer could not see even that.
- Cost: 48 panel helper runs (16 in round 1, 8 in each of rounds 2 to 5); tokens not recorded.

Proposed end: rule: the panel screens text faults only (repeats, period slips, lines out of character); round topics come from the design question and his own play. Deletion: the KCD2 and Mafia share columns in REVIEWS files and themes.py's comparison output; safe because nothing reads them and their own calibration shows they cannot separate builds.

### 5. The prototype tests the first hour of the gossip engine, not tension and a rise to power (high)

Impact: high. His direction (canon pillar, 18 Nov 16:02: "we don't want a gossip simulator ... what the player feels is tension, risk and a rise to power") is not what the prototype's checks or schedule test.

Evidence:
- Before his words, every lane check of the prototype tested the engine: seeing, naming, the Ledger, money, saving, gossip, police (tools/lane/prototype/README.md, "Per-system checks"). Study 2's adopt line of 28 Oct, "something new at least every three minutes, counted in the tester's log" (studies/02-first-30-minutes.md line 84), reached the prototype only after his 13:02 playtest (playtester README).
- Even after five rounds aimed at tension, the bot's hour is 92% talk, walking and waiting, and 3% tense verbs (round 5 newcomer.md share table).
- The rise is unmeasured: the prototype is one week (Monday 15 to Friday 19 Oct 1990), the playtester plays its first hour, and nothing counts name rung, money, crew, property or doors opened. BUILD-ORDER.md puts the rise in stage C, rounds 21 to 28 of 29 (lines 77 to 88).
- Canon still says the opposite in D24: "a small dense town where what people know about you is the mechanic", and anything that does not feed perception, memory, gossip or consequence "gets the smallest budget" (canon.md lines 173 to 177), beside the 18 Nov pillar that makes memory "the engine under the hood, not the show" (lines 166 to 170).

Proposed end: ruling for him: "Canon's D24 line and the 18 Nov pillar pull apart: A) rewrite D24 to the pillar (tension, risk and a rise felt; memory and gossip the engine) (recommended); B) keep both as written; C) keep D24 first." List item: a rise measure in the playtester (name rung, money, crew, doors, per played week) and one rise round brought forward before stage B.

### 6. Builds reached him untested by a person and with a failing check (medium)

Impact: medium to high for his attention: the faults he found were findable, and the "all tests pass" lines he could read were not true.

Evidence:
- Eight prototype page versions on 18 Nov, five lane rounds between 16:16 and 21:25 (PUBLISHED.json "previous"; LANE-LOG lines 52 to 59), each published within the hour, with no gate and no known-issues note. The gate is item 4o, queued after the synthesis, and round 6 in BUILD-ORDER.md line 37, though his 21:54 pick (RULINGS line 38) already requires it.
- The lane's own rule check has failed since round 2: rules_test.py line 407 asserts 52 kinds of act, and round 2 added "bag_taken" (commit 9cddcafc9, 18 Nov 16:44). Run here: 164 pass, 1 fail. Yet LANE-LOG and LANE-QUEUE say "All tests pass" for rounds 2 to 5: run_proto_tests.py runs only Fable's suite, so the lane's pytest checks were never in the publish path.
- Fable's layout test fails at 1280 by 720 (talk box over the subtitles; reproduced here), filed as a timing effect.
- He found the wrong-person prompt and the repeated lines first (13:02, 18 Nov; PROTOTYPE-PLAYTEST-1: "His three findings are confirmed"), though the lane had a test hook and smoke tests from 00:20.

Proposed end: rule: a prototype or study build is published only when the lane's pytest checks, Fable's suite and the gate all pass, a red test blocks, and the known-issues note goes on the page; the gate (4o) comes before any further publish. List item: fix rules_test (53 kinds) and the 1280 by 720 overlap.

### 7. Rounds 4 and 5 tuned people's nerve so the bot's hour shows a fight (medium)

Impact: medium. The rounds bent the town to the scripted path, and touched a question the lane itself left open.

Evidence: round 4 added "face (0.06 nerve a watcher within 12 m, at most 0.24), corners (+0.2 shoved into a wall)" and round 5 gave Lee 0.3 nerve backed by Cammack's lads (LANE-QUEUE.md items 4l-4 and 4l-5), after the panel complained that every debtor gave way to the bot. RULINGS line 38 freezes the town simulation until the C# one replaces it; each person's temperament is still decision 3 in PROTOTYPE-VS-DESIGN-2026-11-18.md (line 38), where the Core keeps everyone at 0.5. The lane checked the freeze for talk lines (item 98) but not for nerve. The panel's top moment in round 5 was then that fight (5 of 8).

Proposed end: rule: a round changes no person's nerve, loyalty or other town numbers while the freeze and decision 3 stand; a round meant to make a fight possible changes the verb, not the people, and is checked on three seeds.

### 8. The driving study has no home in the repository (medium)

Impact: medium. RULINGS (17 Nov): "His driving study tunes to the sheet; the game adopts it", yet the study lives only on a claude.ai page and an older desktop copy.

Evidence: the repository holds only round 3's changelog (production/lane/synthesis/pack/sources/); the page carries about 80 source and test files under source/. tools/driving_feel_check.py passes with "study copy absent (no shortcut copy to judge) faults=0", so its enforcement does nothing where the copy is missing. The prototype got a source project with a byte-for-byte build on 18 Nov; the study did not.

Proposed end: list item: bring the study's source into the repository beside the prototype's, with the same byte-for-byte build, and run its keysteer, keylap and partb tests in the cloud each round.

### 9. Canon's "ten activities" target rests on a number read from the games' files (low)

Impact: low to medium: a canon target enforced every round has a weak base.

Evidence: canon.md line 160 takes "about ten distinct activities per thirty minutes" from Study 2; Study 2 gives "~10 (I)", inferred, with "no recording", rebuilt from KCD2's and Mafia's own files (studies/02-first-30-minutes.md lines 3 to 5, 65, 134 to 135). His 17 Nov outside-only rule makes such numbers leads, and Mafia is no longer the yardstick (18 Nov).

Proposed end: list item: re-count from public footage of KCD2 and GTA (the footage and blind line-up plans already exist) and restate the target with its source.

### 10. Stale texts in the lane (low)

Impact: low, but these are the files a fresh session starts from.

Evidence: PUBLISHED.json's note says "Fable's second round of 18 Nov" while its version is lane round 5; tools/lane/prototype/README.md reports results of "18 Nov 12:20 to 12:50" and "126 tests ... all pass"; LANE-HANDOVER.md, "the one file a lane session starts from", still lists the PC lane's five queue items of 17 Nov, "Done: (nothing yet)" and "publish nothing", while the cloud lane publishes the prototype by his decision of 18 Nov 15:23 (D-B-030).

Proposed end: list item: rewrite the three at the next lane stop, the handover naming the cloud lane's own rules.

## Costs, as far as recorded

- Lane runs touching the prototype on 18 Nov: about 7 to 8 hours of wall clock across 13 runs (LANE-LOG lines 18 to 59); driving targets and the game set about 45 minutes (17 Nov 23:17 to 23:42, 18 Nov 13:20 to 13:40).
- Helpers: 48 panel reviews and a fresh review per round. Tokens and dollars: not recorded in the repository (spend rows went to his page).
- His attention: his 13:02 playtest, about three minutes of driving, the 21:54 pick, and three Fable prompts relayed by hand (3,049, 1,174 and 930 words). The Fable driving rounds ran on his own plan; their cost is not recorded.

## Runs made for this review

All outside the repository: Fable's suite 16 pass, layout fail, eyes prints, oldsave skipped; the lane's checks 164 pass, 1 fail, 4 skipped; driving and car scripts 87 pass.
