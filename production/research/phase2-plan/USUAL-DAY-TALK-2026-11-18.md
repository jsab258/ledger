Method researched: production/research/phase2-plan/RON-ROUTINE-TALK-2026-11-17.md (gap 1), production/specs/hook-cast.json (person "rocco", the week and days rules), ledger/Assets/Scripts/Core/CastDay.cs (WhereWords, OwnWeekWords), ledger/TalkHelper/Program.cs (the scene lines and their selftest), ledger/Assets/Scripts/Core/ClaimCheck.cs (KnownItems, CheckAsync, ParseItems, StatedIn), ledger/Assets/Scripts/Core/NameRules.cs, ledger/Assets/Scripts/Core/ConversationEngine.cs (what reaches the check), ledger/TalkTests/Program.cs, ledger/CoreTests/Program.Part2.cs, tools/ci-checks.sh, commit 4438999c0.

# His usual day in his talk, 18 Nov 2026

Bounded helper task for the session's decision of 18 Nov 06:50 (DECISIONS.md, waiting item 14). Read and run on wip in ledger-local, 18 Nov; no API call, no Unreal.

## Questions (written before reading code)

1. Does a "usual day" line already exist anywhere in the talk helper or the Core?
2. If so, does it reach the claim check, and as which of the check's numbered items?
3. Which parts of the claim check are code and which are the model, and does each accept a place or hour of the routine and refuse a place outside it?
4. Can the talk test project (which compiles only the Core) test the line's text as the helper sends it?
5. What still rests on the paid model and cannot be shown offline?

## Answers

1. Yes. Commit 4438999c0 (01:20 today, before the 06:50 decision) added CastDay.OwnWeekWords and a scene line "Your usual week: ..." beside "Where you are: ...", for every talker with a routine, tested in CoreTests (Ron's exact words) and the helper selftest. The line is named "week", not "day", and is kept so: it carries the weekday and Sunday hours the task asks for, and renaming would only move two passing tests. Assumption recorded here.
2. Yes, inside the scene: the helper passes the scene to the engine, and ClaimCheck.KnownItems gives it to the check as item S1 ("The scene: ... Where you are: ... Your usual week: ..."), which the check and its second look may cite like any of the speaker's facts.
3. Two code layers run before or beside the model. (a) The hard rule on names (NameRules, wider mode on): a sentence naming a place noun his facts have no word for is refused before any call, so "down the pier" or "up the station" is refused. It cannot judge hours: with the street's opening hours among his facts (the office "opens at seven, nine on a Sunday", every shop's hours), every hour word already passes, with or without his week (measured: "seven", "nine", "four", "eleven" all pass either way). (b) "Stated in so many words" (StatedIn) clears a detail whose words stand in order in the item cited; the week's order ("seven in the evening, the front room of Mickey's") seldom matches how a speaker puts it, so most routine claims go to the model's second look, shown S1. Everything else is the model's list and look.
4. Not before: the line was assembled in the helper. Now it has one home in the Core, CastDay.TalkLines, which the helper calls and the tests read.
5. Whether the paid check, shown S1, clears "at the office from seven most evenings" and refuses "at the chapel most evenings" (a street place Ron knows but does not keep, which passes the hard rule) is the model's judgement; not run (no API call).

## Change

- ledger/Assets/Scripts/Core/CastDay.cs: new TalkLines(id, day, hour): "Where you are: X." then "Your usual week: Y.", each only when it has words; null for somebody not in the cast. Derived from hook-cast.json through the existing readers; no new file, no copy, nothing to stage, no port (the helper is C#; the claim check has no C++ copy).
- ledger/TalkHelper/Program.cs: the two scene-building blocks replaced by one call to TalkLines; the scene the helper sends is unchanged word for word (its selftest compares it exactly and passes).
- ledger/TalkTests/Program.cs: TestUsualWeek, eight checks.

## Tests (TalkTests, TestUsualWeek)

- Ron on a Monday evening: the exact text, where he is then his whole week (Monday to Saturday, then Sundays).
- Ron on a Sunday morning: the allotments now, his Sundays in the same words, no ids.
- Off the street at two in the morning: no place, his week still said.
- A speaker with no routine in the cast (and a null id) gets no line.
- Every place and hour of his week (office from seven, till eleven, Sunday allotments from ten, the cafe at seven, the quay at five, the fish market at twelve) passes the hard rule on names, given everything the helper gives him.
- The pier and the station, outside his week and his facts, are refused by the hard rule.
- A whole turn, the check scripted: asked "Where will you be tonight?", "I'm at the office from seven most evenings." cited to S1 is said, and S1 holds his week.
- A whole turn: "I'm down the pier most evenings." is refused by code before any check call, whatever the scripted check would cite.

## Checks, run as tools/ci-checks.sh runs them (MSYS settings unset), 18 Nov

- CoreTests: All 5255 checks passed.
- TalkTests: ALL 140 TALK CHECKS PASSED (132 before).
- Talk helper selftest: passed=143/143 failed=0.
- Soak: all 9 checks passed.
- SaveChaos: all 149 checks passed.
- PerceptionGolden (port-golden-check.sh): table matches the Core, and the port agrees with it.
- StrangerTest selftest: 5 passed, 0 failed.
- Fake playtest (SimHarness): 89 passed, 0 deterministic fail.

## Unverified

- The paid check's verdicts on routine claims phrased freely, and on a known street place outside his routine (the chapel); a bench run with the check's model would show both. Not run: no API call in this task.
- A wrong hour at a routine place ("at the office from four") is not refused by code, since the opening hours hold most numbers; it rests on the model's look. Measured, not fixed.
- ClaimBench's own scene builders (Bait.cs, FastFirst.cs) still add only "Where you are"; bench numbers taken there do not include the week.

Reference: production/research/phase2-plan/RON-ROUTINE-TALK-2026-11-17.md
