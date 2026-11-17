# K2: phase 3's simulation port and its two faults (18 November 2026)

## For Jafar, in plain words

1. The two faults are: the police file mishandles a serious crime (a stabbing, robbery or killing) in three small ways, and a person's suspicion of Tom is kept in two places that can disagree.
2. The police fault cannot show today: the only crime in play is Rita's window, and that path works; it matters once a serious crime is added. The suspicion fault can show now, in a small way: someone made uneasy by gossip can greet Tom coldly in the street, then talk to him as if nothing were wrong.
3. The police fix and its tests can all be done in the cloud: about 10 to 13 hours. All three slips were made to happen on demand here today. Connecting the detective's arrest to the game later also needs one game build and a test walk on his PC (about 1.5 to 2 hours of machine time).
4. The suspicion fault is half cloud (about 3 hours) and half his PC: one game build and a short live talk to see it works (about 1 to 2 hours of machine time).
5. Recommended: keep both for their phase; do the police fix in the cloud before the first serious crime is built.

## What K2 is

Order of 16 November, "Carried for his keep-or-drop", K2 points to three lines in production/orders/archive/2026-11-09.md (lines 246, 252, 255):

- o25-fallback-sim-port: the port itself (C# rules copied into the game's C++, checked row by row against the C# Core's answers). Last status there: 29 October, all of Reaction.cs ported, 69,186 rows agreeing, "not wired, the Unreal build not yet run".
- f-suspicion-port: FINDINGS.md line 9.
- f-police-file: FINDINGS.md line 18.

Port status today (measured here, 18 November): tools/port-golden-check.sh run on a scratch copy of the repository with the .NET 8 SDK (8.0.134, Ubuntu archive) and g++: "core-port-test: 102997 check(s), 0 failure(s) over 102953 golden row(s), 0 mismatch(es), 0 unanswered, 7 skipped", and "table matches the Core, and the port agrees with it". 51 s. So the whole port check runs in the cloud, no Unreal needed. Whether the port has since been built in Unreal and wired was not checked.

## Fault 1: three time-and-state slips in the police file

Source: FINDINGS.md line 18 (full text production/archive/FINDINGS-full-2026-11-04.md line 20; sweep of 30 September). Code: ledger/Assets/Scripts/Core/PoliceFile.cs, mirrored line for line in ue-probe/Source/LedgerProbe/Public/PoliceFile.h.

Reproduced today with a small probe program compiled against an unedited copy of the Core (kept only in the session scratch folder, not in the project). Output:

```
1a day2 Ellis: Wounding player.cut_d1  canArrest=False
1a statement day3; canArrest=True; day4 Ellis: null; day9 Ellis: null
1b day3 09:00 Ellis: Wounding player.cut_d2; TakeIn while held: null; day4 Ellis: null; canArrest still=True
2 visits before reload=1 after=0; day4 Ellis played=null reloaded=Wounding player.cut_d1
3b visits after reload=1; played WasTaken=True reloaded WasTaken=False reloaded CanArrest=True
control window reload WasTaken=True
```

### 1a and 1b: her visit is used up when she cannot take him

- Where: PoliceFile.cs 335 to 354. EllisWouldComeAll gives a crime as a reason only if no visit with the same text ("Wounding topic") exists. Unlike ConstableComes (101 to 113), EllisComes takes no time, so it does not wait while he is in the cells.
- Effect: if she comes when only a description is on file (1a), or while he is held for another deed (1b), the visit is recorded. When a naming statement arrives later, or he is released, she never comes again. The crime is never answered for.
- Also found: TownWeek.NineEllis (ledger/Assets/Scripts/Core/TownWeek.cs 121 to 131, port TownWeek.h 147 to 170) never calls TakeIn. The comment at PoliceFile.cs 99 to 100 says she takes him on her visit, but no code does that yet. That is the "wiring" the finding waits for.

### 2: a description raised to a statement takes the statement's day

- Where: PoliceFile.cs 261 (`e.Day = day` when raised); port PoliceFile.h 435.
- Effect: the load check VisitCouldBe (PoliceFile.cs 491 to 498) keeps a crime visit only if an entry for it has Day on or before the visit. After the raise, the entry's day is later than her visit, so a reload drops the visit and she comes again. Play and reload disagree.
- Side effect found today: this slip hides slip 3 when the same witness raises their own description (the probe's first try at 3 passed for that reason).

### 3: a spell in the cells must end by the day after its call or visit

- Where: PoliceFile.cs 500 to 515 (SpellCouldBe); port PoliceFile.h 729 to 739.
- Effect: it takes the latest call or visit day for that deed and rejects any spell ending more than a day and 22 hours after it. If her visit was days before the arrest (second witness names him later, then he is taken), a reload throws the arrest away and he can be arrested again for the same deed.

### Why it cannot show in the game today

- The game files only one kind of police report: TownWeek's nine o'clock reports step reports every deed as Offence::Damage (port TownWeek.h 135 to 136, `WouldReport(..., Offence::Damage, ...)` and `Police.Report(..., Offence::Damage, ...)`; Core TownWeek.cs 110 the same).
- Her visit for a crime is only for a crime a detective takes: `Detective(o) => o >= Offence.Wounding` (PoliceFile.cs 181), used in EllisWouldComeAll (PoliceFile.cs 351). Damage is below Wounding, so no game report can ever start the paths above. The slips sit in code nothing in play reaches.

### Can it be done without Unreal, a graphics card or his PC?

The fix and its tests: yes, all of it. The C# Core builds and runs here; the C++ port is checked here with g++ against the same golden table (tools/port-golden-check.sh, which needed only an empty package-source file to work offline). Only the next ordinary Unreal build on his PC compiles the changed header, as it does for every port change.

### The plan (exact changes; no edit made today)

A. Entry gets a second day (fixes 2):
- PoliceFile.Entry: add `public int First;` the day this person's account first went in the file. Report sets First = day on a new entry and leaves it alone on a raise; Day keeps meaning the statement's day (ConstableWouldCome 130 and SpellCouldBe use it so).
- ToJson writes "first"; FromJson reads it, defaulting to "day" for old saves.
- VisitCouldBe uses `e.First <= day` instead of `e.Day <= day`.

B. Her visit waits until she can act (fixes 1a and 1b):
- EllisComes and EllisWouldComeAll take `GameTime? now = null`, as ConstableComes does; with `now`, crime reasons are not given while InTheCells(now). Body and talk are unchanged.
- A crime is fresh again once a naming statement exists that came after her last visit for it and he has not been taken for it: Fresh-for-crime = no visit for this text on or after the earliest statement day, when CanArrest(topic); otherwise as now. This allows exactly one more visit.
- FromJson's visit loop: allow the same reason twice on different days (today line 551 drops any repeat), checked by VisitCouldBe as above.
- TownWeek.NineEllis passes `now`; when the reason is a crime and CanArrest(topic), call Police.TakeIn and record the custody as TenConstable does (TownWeek.cs 135 to 145). This step is the wiring itself; it can be held back until the first serious crime exists, but A, B's file changes and C should go in together.
- The game's handlers need changing for the wiring, which is PC work. In CrimeProbe.cpp 7793 to 7801 the Ellis handler only shows "DS Ellis is on Quay Street this morning, asking after you." and logs; only the Taken handler (7802) calls ConstableHour (7710), which plays out the custody. TownWeek.h 262 to 267 then overwrites Done.Taken with the ten o'clock constable's result. So the wiring needs: a separate field in HourDone for her arrest (Core TownWeek.cs and port TownWeek.h, cloud work), and the Ellis handler in CrimeProbe.cpp calling ConstableHour with it and showing a different line when she takes him (Unreal source, so built on his PC). The cloud can write the change (about 1 hour); proving it needs one Unreal build of both targets and a packaged walk in which she arrests him, on his PC.

C. The spell is checked by its own start (fixes 3):
- `_taken` keeps the minute he was taken in (Custody.TakenAt already exists, Custody.cs 81).
- ToJson writes [topic, out, in]; FromJson accepts it when `in` is on or after the earliest statement day's start and 0 < out minus in <= 22 hours (LongestSpellHours). Two-element old saves use today's rule.

D. Port and checks:
- Mirror A, B and C in ue-probe/Source/LedgerProbe/Public/PoliceFile.h and TownWeek.h.
- New golden rows in ledger/PerceptionGolden/Program.cs beside the "SweepArrest" rows (about line 1935): the five probe cases above, each played and reloaded, the expected answers being: 1a she comes on day 4; 1b she comes the morning after release; 2 visits after reload = 1 and no second visit; 3b reloaded WasTaken = True; control unchanged.
- CoreTests, Soak, SaveChaos (which already plants police saves, ledger/SaveChaos/Program.cs 158 to 161), PerceptionGolden, StrangerTest and a regression test, then tools/port-golden-check.sh --accept, then a fresh subagent asked to break it, as CLAUDE.md requires. One DECISIONS.md entry.

Cost: A 2.5 h, B 4 h (file 2.5, wiring 1.5), C 2.5 h, golden rows and the full check suite with the breaker 2 to 4 h. About 10 to 13 hours of cloud work, plus about 1 hour for the CrimeProbe.cpp handler change when the wiring is done. On his PC: for A to C, nothing beyond the next normal Unreal build, which compiles the header; for the wiring, 1.5 to 2 hours of machine time (one Unreal build of both targets and one packaged walk with an arrest by her). It can share a build with other work.

Not covered: the finding's "also unproven: his answer to Sheila overheard" was not looked at.

## Fault 2: suspicion kept in two places

Source: FINDINGS.md line 9; production/audits/rulings-sweep/TABLE.md 1625. The finding's own wording ("nothing in the game reads the port's number yet: RegardFor reads it") contradicts itself; the exact state is below.

- The game's C++ copy of the town raises each person's suspicion when gossip contradicts what Tom said or a night story leaks to a day person (ue-probe/Source/LedgerProbe/Public/Gossip.h 1111 and 1116, from Gossip.cs 496 and 501) and saves it. StreetVoice reads it for a person's manner in the street (StreetVoice.h 1205 Stance; 2135 who greets him).
- A conversation is answered by the C# helper (ledger/TalkHelper/Program.cs). The game sends what the person holds about the deed ("evidence", CrimeProbe.cpp 5913), and the helper works the suspicion out afresh (Suspecting.Derive; TalkHelper 785 and 1019 to 1024, which resets it to that derived value each turn). The street number is never sent.
- Effect: a person made uneasy by gossip can greet Tom coldly and then talk to him as if nothing were wrong, or the reverse. Small today; it grows with the town.

### Can it be done without his PC?

Half. The helper's side is plain C# and builds here (TalkHelper.csproj compiles the Core and needs no packages). The game's side is one field in CrimeProbe.cpp's request, an Unreal source file, so it needs an Unreal build on his PC and a short packaged talk to prove it.

### The plan

- Game (his PC): in CrimeProbe.cpp 5913, add `,"streetSuspicion":` with G->Suspicion.Value() to the talk request. The port keeps the number only, no reasons (Suspicion.h 14 to 18), so the reason given is a fixed line such as "what I've heard about him doesn't add up".
- Helper (cloud): read "streetSuspicion"; after the derived value is set (Program.cs 781 to 786), use the larger of the two, with the larger one's reason. The larger, not the sum, so a leak about the same deed is not counted twice. This is a design choice inside the pillars; record it in DECISIONS.md.
- Test (cloud): a TalkTests case (ledger/TalkTests) with noReply=true: evidence alone gives level X; the same with a higher streetSuspicion gives the street's level and reason; a lower one changes nothing.
- Proof (his PC): one packaged walk in which a person is made uneasy by gossip, then talked to; the helper's reply shows the raised level.

Cost: cloud 2.5 to 3 h (helper 1 h, test 1 h, record and review 0.5 to 1 h); his PC 1 to 2 h of machine time (one Unreal build of both targets, one packaged walk with live talk), done alongside any other build.

## Evidence and method

- Read: production/orders/2026-11-16.md 118 to 122; production/orders/archive/2026-11-09.md 246 to 255; production/orders/2026-10-25.md (the full port line); FINDINGS.md; production/archive/FINDINGS-full-2026-11-04.md; PoliceFile.cs (whole), TownWeek.cs 110 to 180, Custody.cs, Suspicion.cs, Gossip.cs, StreetVoice.cs; the port's PoliceFile.h, TownWeek.h, Gossip.h, Suspicion.h, CrimeProbe.cpp; TalkHelper/Program.cs; production/research/lane/SIM-IN-BROWSER-2026-11-17.md; tools/lane/simwasm/.
- DECISIONS.md was searched with grep only: nothing on how the two suspicion numbers should combine.
- Run here: .NET SDK 8.0.134 installed from Ubuntu's archive (Microsoft's own feeds are blocked from the cloud); the port check and the probe ran on a scratch copy, so nothing in the project was built or changed. The only project change is this file.

Review applied: production/lane/reviews/REVIEW-K2-SHARE-SYSTEMS-2026-11-18.md
