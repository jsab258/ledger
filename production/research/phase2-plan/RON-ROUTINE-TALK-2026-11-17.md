# Ron's routine and talk: what exists, what is missing (n16-2, machine-free part), 17 Nov 2026

Order item n16-2 (production/orders/2026-11-16.md): Ron as one complete person; this note covers only his routine and talk as data. Clothes and Unreal work are outside it. Reference: studies/01-npc-life.md (Kingdom Come II's scheduler: timed links with places; extras come out through a door) and studies/03-dialogue-barks.md. Read from ledger-local on wip, 17 Nov; no API call, no Unreal run.

## What already exists

| Piece | Home | State |
|---|---|---|
| Routine | production/specs/hook-cast.json, person "rocco" | Weekdays: 07 cafe, 08 rank, 12 fish market's pavement, 13 rank, 17 quay, 19 office, 23 off. Sundays: 10 allotments, 13 off, 19 office, 23 off. All seven places have spots (cafe and office with body spots). 13 ties (Sheila 0.7, Darren 0.8, and eleven townspeople), temperament, keepsQuiet "owner". Staged for the packaged game. |
| Routine, played | ue-probe CrimeProbe.cpp PlaceBodiesByRoutine (reads hook-cast.json, Sunday included) | Each hour Ron stands where his routine puts him, moved out of Tom's view. |
| Routine, in talk | ledger/TalkHelper (CastDay.WhereWords) | He is told where he is this hour ("Where you are: ..."), and the claim check reads that as the scene. |
| Talk card | production/cast/cards/rocco.md | Summary, speech style, what he notices first, four hard facts, and all seven own-word kinds (known-only, deflect, brush-off, opener, ask, told, refuse), the same set as Sheila's and Darren's cards. |
| Facts | ledger/Assets/Scripts/Core/StreetFacts.cs | died_heart (Ron found Mickey at the office), mickey_kept_ron, ron_rank, each with his own words and plain words. |
| Own street lines | ledger/Assets/Scripts/Core/OwnLines.cs; port ue-probe OwnLines.h; text production/casting/ron-kirby/STREET-LINES.md (approved 30 Sep) | 39 banks: every bank StreetVoice can fire (18 ambient states, 20 recognition moments, faint). No bank is missing. |
| The ask and the landing | Core Arrangement.cs, TheLanding; CrimeProbe "ron-ask" | Ron brings the envelope after dark at the office (his 19 to 23 office hours match), takes a no down to the landing at eleven; the man's lines there. |
| Office exit | CrimeProbe.cpp WalkPathOut (9 Nov) and the stand-up clip before a seated walk (11 Nov) | Coded; tries 2 of 2 used (DECISIONS 9 and 11 Nov); not yet shown in a packaged walk. |

## Gaps

1. His regular day is not in his talk. Only this hour's place reaches the model and the claim check. Asked where he will be tonight or on a Sunday, he has no source: the check refuses an answer or he says that is all he knows. The first-ask design makes finding Ron after dark matter to the player. Not filled here: it is a talk change for every named talker and touches n16-6's talk work. Shape proposed for the session: the talk helper adds one derived line, "Your usual day: ...", from CastDay's routine (home stays hook-cast.json, no new file, nothing to stage, no C++ port since the helper is C#), with a talk selftest that the words match the routine. Session's decision under its rulings, not his.
2. Office exit unproven (Unreal, the session's): one packaged walk across 19:00 to 23:00 or a seated move, read for "in 3 leg(s)" and no "cannot walk" for Ron. If it fails, a third try needs his yes.
3. quay-cast.json's copy of Ron's day (golden run only) has no 07:00 cafe and no Sunday. Not played; changing it moves the goldens, so left. Listed so nobody reads it as his day.
4. Still machine work: Ron's paid talk runs in the packaged game, per-speaker talk cost, prepared-line mouths (from RON-COST-INPUTS-2026-11-08.md).

## Added

Nothing to the game's or simulation's data. Every routine and talk slot n16-2 needs is filled; the open points are a talk design choice (gap 1), Unreal proof (gap 2) and the questions below. Nothing new to stage.

## Tests (17 Nov, wip, no change made)

All pass, run as tools/ci-checks.sh runs them: CoreTests 5,254 checks; TalkTests 132; Soak 9; SaveChaos 149; PerceptionGolden (port-golden-check.sh) table matches the Core and the C++ port agrees; StrangerTest selftest 5 of 5; the fake playtest (SimHarness) 89 passed, 0 failed. A baseline only, since no game data changed.

## Open questions (canon, story or scope)

- Does Ron go visibly down to the landing at eleven on a night he carries the answer, or simply leave the street as now (routine "off" at 23)? The design says he goes; whether the player sees it is scope. Recommended: leave him off the street until the office exit passes packaged.
- Years on the docks: the casting sheet's voice-test line says "Forty years on the docks"; the card, his street lines and OwnLines say thirty; canon says only "a docker until 1989". The game is consistent at thirty and the sheet's line is not in the game. Recommended: no change (his 8 Nov ruling: small canon details wait until judged in the game; editing the sheet lapses its approval).
- For the clothes lane, not this note: the sheet records jeans as passed on 8 Nov; n16-2 names trousers from the breadth set (the work trousers now in Kiln).

## For the session

- Office exit: the packaged proof above (gap 2), then Ron on his page with Tom's look.
- Gap 1: decide whether his usual day enters talk now or with n16-6.
- Not taken from the reference: Kingdom Come II varies about half its timed links by plus or minus 30 minutes; Ron's day runs on whole hours. A waiting-list idea, not n16-2.
