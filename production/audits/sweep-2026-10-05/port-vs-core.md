# The C++ port against the C# Core, 5 October 2026

**What was compared.** The C# simulation (`ledger/Assets/Scripts/Core`) against its hand port in C++ (`ue-probe/Source/LedgerProbe/Public` and `Private`), at `main` d6a9e851a. No Core, port, golden-table or test file has changed since fcc10af, the commit the build machine last measured (`git diff fcc10af HEAD` on those paths is empty), so `production/d1-probe/ue-verdict.txt` describes this code.

**How.** Read-only; no Unreal, Blender or graphics card; nothing committed.

1. `bash tools/port-golden-check.sh` (MSVC, 1 min 27 s). Summary line: `core-port-test: 57913 check(s), 0 failure(s) over 57876 golden row(s), 0 mismatch(es), 0 unanswered, 7 skipped`, then `port-golden done: table matches the Core, and the port agrees with it.` (exit 0). The Core emits 57,884 rows and the committed table is identical (`goldenDrift=no`). Those 57,884 are 57,876 compared, 7 skipped by name and 1 that no reader looks at (rows H1 and H2 below). `tools/route_week_check.py` (16 rows and 11 stops equal the Core's week) and `tools/crime_probe_check.py` (354 checks) also pass.
2. Reading: every "to port" item in `production/archive/2026-10-05-retired/handovers-OPEN.md`, and the faults of `production/audits/review-2026-10-01/FAULTS.md` it points to, each followed into the code.
3. Names and literals: every public name of 26 Core files looked up in the C++, and every string and number literal compared.
4. Two checks written for this audit and kept in the session's scratch folder, not in the repository (`C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-local\7ec707fe-fd41-4a40-ac4f-b7fc4cc91e3b\scratchpad`: `fuzz.cpp`, `fuzz2.cpp`, `fuzz3.cpp`, `csprobe\*.cs`, `mutate.py`; temporary, copy them if they are wanted):
   - **Differential fuzzers.** The real Core compiled from its own source and the port, given the same random scripts and compared on the whole resulting state. Arrangement, Ada's tea and the week's end: 600,000 scripts, 0 differences. Police file, custody, damage, threats and the gossip mill: 48,000 scripts, 0 differences (one early run differed in the twelfth decimal place of one number, far inside the golden table's 1e-9). Town rounds (TownHours.RunTo, Hour, CatchUp) with saves: 3,000 scripts, 0 differences. The fuzzers do catch planted breaks (see "Planted breaks"), so a zero means something.
   - **Planted breaks.** 30 one-line breaks put into scratch copies of the port, each run through `core-port-test`, `route-week-test` and `crime-probe-test`.

**Result in one sentence.** Where the C++ port has a counterpart for a Core function, it agrees with it today, with one exception found (U2: the cast file's shop hours are not read, so bad ones are accepted). What is left are things the checks do not ask, things the Core has and the port does not, and rules that live only in C++ with no C# home.

**Not checked.** The packaged game and anything in `CrimeProbe.cpp` that needs Unreal (read, not run); the talk program (`ledger/TalkHelper`, C#, runs as it is); CoreTests (not rerun); items marked "not checked" in the rows.

Counts: 22 disagreement rows, 21 distinct (H1 repeats U1): 5 rules only in C++ (G), 8 not ported (U), 6 wired differently from ROUTE.md or the Core's plan (W), 3 holes in the checks (H). Two rows are High for the route: G1 and G2 (the same rules come up again as items 16 and 18 of section 3). 11 of the 30 planted breaks fail no repository test (section 2). 30 ported items listed (section 3).

---

## 1. Disagreements, most important first within each group

Route weight: how much it matters for the thirty-minute route (`production/handovers/ROUTE.md`, `production/playtest/thirty-minutes-2026-10-03.md`).

### 1a. Rules that live only in C++ (no C# source to agree with)

| # | What | C# | C++ | Test catches it? | Route |
|---|---|---|---|---|---|
| G1 | **Who sees the window, and what they do.** Who stands where at the hour, night from 19:00 to 07:00, the light on him, one second of watching, what a witness files by rung, who shouts. The Core puts the cast in places by hour (`CastDay`) but has no rule that fixes night at 19:00 to 07:00 for sight, a deed's watching time, or what a witness files by rung (searched `Core` for these; none found). | none (the nearest, `Reaction.Decide`, Reaction.cs:50-78, is not used) | `CrimeProbe.h`: `OnlookersAt` 2030, `NightAt` 1970, `LightOnHim` 1971, `kDeedSeconds` 1969, `WhatWitnessFiles` 2059, `WitnessShouts` 2081 (`Rung >= 1`); used `CrimeProbe.cpp` 2594, 6703, 6858, 6903. Only Sheila's body shouts (2652-2655). | Only the C++'s own self-test (`crime-probe-test`, 354 checks): planting night 19 to 20 or "shouts at rung 1" to "rung 2" fails it. No C# row compares them. | **High**: these rules decide who saw the window and so whether anyone reports him. |
| G2 | **How well each person knows his face.** 0.4 after the first meeting, 0.1 more each further day met, capped at 0.7. The Core has only the thresholds (Perception.RecognitionFamiliarity 0.35, Acquaintance.cs:24-85). | none | `CrimeProbe.h` 1674 `FamiliarityFromMeetings`, 1685 `RegardFamiliarity`; used `CrimeProbe.cpp` 2463, 6062-6064, 6909, 6928. | Self-test only (planting 0.4 to 0.3 fails `crime-probe-test`). | **High**: it decides rung 4 (recognised), so the report, the constable and the arrest. |
| G3 | **The shapes of the deed's stories and the talk's evidence.** `KeepQuiet`, `OwnedUpStory`, `SightingStory`, `ClaimStory`, `DeedJson`, `EvidenceAccount`. The C# has no such functions; the talk program (C#) reads what they write. | none (talk contract: `production/specs/talk-protocol.md`) | `CrimeProbe.h` 2195, 2167, 2133, 2150, 2260, 1634-1670 | `crime-probe-test` and `tools/talk-protocol-check.py` pin them against the written protocol, not against C# code. | Medium: these carry every talk reply into the town's memory. |
| G4 | **The game's hourly step and wait loop.** They mirror `ledger/TownReach/Program.cs` (a C# test program, not Core). | `TownReach/Program.cs` 365-477 | `TownWeek.h` 71-217; `CrimeProbe.h` 1699 `WaitHourByHour`; `CrimeProbe.cpp` 6455-6488, 7000-7059 | The 16 rows and 11 stops of `route-week-test`. Three calls in it are unpinned (planted breaks P1, P3, P11 below). | Medium: the rows hold, but three steps can vanish unseen. |
| G5 | **The clocks.** Two game minutes per real second, each hour handed back once; the fixed-step clock. | none (Core `GameTime` is a value type) | `LiveClock.h`, `FixedClock.h` | `core-port-test.cpp` 270-340 asserts them against themselves. | Low: self-consistent, and nothing in the Core to differ from. |

### 1b. In the Core, not in the port

| # | What | C# | C++ | Test catches it? | Route |
|---|---|---|---|---|---|
| U1 | **A player's claim caught or kept** ("a caught claim is remembered and never learned"). Seven golden rows `Scenario\|claims\|...` pin it and are skipped by name. The game files its own `ClaimStory` for any definite answer, whatever the verdict. | Gossip.cs:456 `PlayerClaims`; Claims.cs; rows `perception-golden.txt` 12497-12503 | none. `Gossip.h` 33-36 names it out of scope; skip list `CoreGolden.h` 1017, applied `core-port-test.cpp` 111-113 and `LedgerProbe.cpp` 733. Game: `CrimeProbe.cpp` 5057 files the claim as a story. | No. Counted and named ("SKIPPED scenario=claims rows=7"); the check only proves the port still cannot answer them. | Medium: any "where were you?" put to Tom (the talk's `claim` field) meets this rule; the game's version was not compared with it. |
| U2 | **Shop hours in the cast file.** The C# refuses bad `hours` and `hours_breaks`, and answers "open now". Run on 16 variants, the C# refuses 13 that the C++ accepts: a string for hours, an empty object, a misspelt weekday, close before open, close over 30, quarter hours, three numbers, text numbers, open at 24, longer than 24 hours, breaks without hours, breaks outside the hours, overlapping breaks. | CastDay.cs 119-124, 273-290, 295-315 (reading), 331 `OpenAt`, 379 `HoursWords`, 739 `HoursFor` | none: `CastDay.h` reads no `hours` at all | No: `CastRefused` has 39 files (`CoreGolden.h` 5042-5080), none about hours. | Low: the committed cast file is valid, and the talk program (C#) reads the hours itself. |
| U3 | **The reaction ladder** (ignore, notice, investigate, alarm, flee, go to the law), by severity and nerve. | Reaction.cs 50-78 `Decide`, 84-94 `Severity`, 98 `LoudnessOf`, 166 `AsVictim` | none (only the arrest part is ported, `Reaction.h`). A search of `CrimeProbe.cpp` for flee, alarm, investigate and `Reacted` finds no ladder: the one reaction is Sheila's shout (G1). | No | Medium: at the window nobody flees, investigates or fetches the law; Sheila shouts. |
| U4 | **A witness who walks to tell, can be stopped on the way, hardens by retelling, or names the wrong man.** | Observation.cs 364 `Willingness`, 410 `Misattribute`, 436 `Retell`, 478 `Delivery` | none. The game, like the Core's own reference week, reports at 09:00 the next morning (`TownWeek.h` 118-135). | No | Low: the route follows the reference week; it matters when threats and bribes reach a witness in transit. |
| U5 | **The damage-control verbs:** bribe, intimidate, discredit, forget, use a hook, `Contain`, `Backfire`, `KnowsSecret`, `DayCircleHeat`. The game's `KeepQuiet` is not `Contain`: `Contain` also cuts the held story to confidence 0.05; `KeepQuiet` only suppresses it. | Gossip.cs 194, 840, 849, 1026-1179 (verbs), 1262 `Contain` | none. `Gossip.h` 33-36 says so. Game: `CrimeProbe.h` 2195 `KeepQuiet`. | No | Medium: "keep it quiet" is a first-week action, and what the talk is then told about the witness differs (full confidence vs 0.05). |
| U6 | **The street's pace of talk** (`ChatterLevel`, `AmbientEverySeconds`, the 45-second floor of Jafar's 29 September ruling). | StreetVoice.cs 1571-1602 | none (`StreetVoice.h` 30 says out of scope). The game rests each person 45 s on their own (`CrimeProbe.cpp` 6119): the same number, a different rule. | No | Low: with three talkers the two paces are close. |
| U7 | **Sounds he makes** (footsteps, door slam, suppressed shot) and the noise ring. | Perception.cs 240-246, 272, 316-327 | none; only the window's sound (`LoudBottleSmash` 70) and shout and remark loudness are ported | No | Low: the first week's only loud act is the window. |
| U8 | **Refusing a save from a newer or older version, or a day past 100,000.** | SaveCodec.cs 26-29, 48, 66, 178-184 | none in `SaveCodec.h`. `TownSave.h` 107-110 has its own version gate; the game otherwise refuses another build by commit stamp (`CrimeProbe.h` 1846 `BuildStamp`, staged by `tools/ue/stage_game_data.py` 141-145). | No test of the C++ side. | Low: a different mechanism for the same aim. |

### 1c. In the Core's plan or the route's spec, wired differently in the game

| # | What | C# / spec | C++ | Test catches it? | Route |
|---|---|---|---|---|---|
| W1 | **One TownSave.** The game's `town.json` leaves `hints`, `heard` and `news` empty; the remarks and hints are kept in `remarks.json` and `hints.json`, so a save is still several files. | ROUTE.md section 3; TownSave.cs 60-90 | `TownSave.h` 48-49, 61-63 hold them; `CrimeProbe.cpp` 7799-7811 fills only asks, tea, police, damage, arrests, hours, week, shown | The review's 311 save-and-load runs kept the rows (1 October); no test in the repository does. Not rerun. | Medium: the pieces do survive; a cut between files is the risk (review C3). |
| W2 | **Ron's pending "tell them no?" and Sheila's pending question, and the line counters, are not saved.** Still the same code as the review found. | review C5(b), (d) | `CrimeProbe.cpp` 5036, 5102 (`GDealAsked`), 2983 and 3025 (`NextId`, `LinesSaid`): none is in the save at 7709-7830 | No | Medium: a "Yes." after Continue is not his no to the outfit. Not run. |
| W3 | **`acquaintance.trusts` and `acquaintance.calls`** ROUTE.md says to send. The game sends `met`, `heardOf`, `knowsName` only. | ROUTE.md section 2; `talk-protocol.md` 53, 92 (optional) | `CrimeProbe.cpp` 4805-4820 (`AcquaintanceJson`) | No | Low: the protocol makes them optional. |
| W4 | **Who sees him taken.** Over 30 m from any named place, the game says Mickey's. | Custody.cs 149 takes the area as a parameter | `CrimeProbe.cpp` 6388-6396 | No | Low: the arrest is on day 4 at the earliest. |
| W5 | **The town's own news** (`town-news.json`) is ported and parsed, but the game never loads or files it; only the golden run and `TownReach --town-news` do. | TownNews.cs 46-100; TownReach/Program.cs 75 | `TownNews.h` 76, 141 | Golden rows only | Low: the street has no news but the window. |
| W6 | **Who the talk's replies can act on.** `GossiperOfCard` maps three cards; a claim, a keep-quiet or an owning-up from any other person is dropped. | none | `CrimeProbe.cpp` 5029-5033 | No | Low: only Sheila, Darren and Ron can be talked to. |

### 1d. In the checks themselves

| # | What | C# | C++ | Test catches it? | Route |
|---|---|---|---|---|---|
| H1 | The seven `claims` rows (U1) are named and skipped. | see U1 | see U1 | The skip is the point; it is counted. | Medium (see U1) |
| H2 | **One golden row is neither compared nor skipped.** `FixPoliceOrder\|...` has two fields and both readers drop rows under three. Its C++ fixture is also a different test: it builds the save without `entries`, so every visit fails `VisitCouldBe` and the port would answer an empty list where the C# gives twenty visits in order. Given the C#'s input in a scratch copy, the port gives the C#'s answer: the logic agrees, the row proves nothing. | `perception-golden.txt` 57850; `PerceptionGolden/Program.cs` 1729-1735 | `core-port-test.cpp` 106, `LedgerProbe.cpp` 690, `CoreGolden.h` 4493 (guards); fixture `CoreGolden.h` 4229 | No | Low: it pins the order of Ellis's visits in a hand-edited save. |
| H3 | **The build machine's one-line verdict hides the holes.** It prints 57,872 rows and 0 unknown; the 7 `claims` rows, the 4 `FactNull` rows an engine build cannot answer, and the dropped row appear nowhere in it. The engine does count them (`perceptionSkipped=` in `golden-result.txt`). | none | `LedgerProbe.cpp` 152-157 (verdict line), 793 (skipped count, written to the other file) | No | Low: a reader sees green with no denominator. |

---

## 2. Planted breaks that no repository test notices

Thirty one-line breaks, each put into a scratch copy of the port. Nineteen fail a repository test. Eleven fail none of `core-port-test`, `route-week-test`, `crime-probe-test`:

| # | The break | Where | Caught by the fuzzers here? |
|---|---|---|---|
| P1 | The game's hour step stops calling `TellDue` (his no and a night away stop reaching the landing as hours turn) | `TownWeek.h` 74 | No: the fuzzers call `TellDue` directly, not through `TownWeek` (a no-op `TellDue` itself differs in 34,203 of 60,000 scripts) |
| P2 | `RunTo` treats any negative as "no round yet" (the 30 September "round before day 0" fix undone) | `TownRounds.h` 148 | No (needs a hand-edited save) |
| P3 | Ron brings the envelope while he is in the cells | `TownWeek.h` 184 | not fuzzed |
| P4 | The damage tick's "I was there" path off | `TownNews.h` 340 | Yes (1,875 of 3,000) |
| P5 | A pane mended within the deed's own hour is not still found | `TownNews.h` 329 | No (default mend is the next day) |
| P6 | The keeper's ", at my place" fallback removed | `TownNews.h` 297 | Yes (1,044 of 3,000) |
| P7 | StreetVoice `NamesHim` gate at 953 off | `StreetVoice.h` 953 | not fuzzed |
| P8 | StreetVoice `NamesHim` gate at 1058 off | `StreetVoice.h` 1058 | not fuzzed |
| P9 | StreetVoice `NamesHim` gate at 1182 off | `StreetVoice.h` 1182 | not fuzzed |
| P10 | StreetVoice `NamesHim` gate at 2133 off | `StreetVoice.h` 2133 | not fuzzed |
| P11 | The 06:00 `PassedTo` call removed (`TellDue` still runs hourly) | `TownWeek.h` 75 | not fuzzed |

The 1 October review listed twelve such lines (its D1). Re-tested: of them, the cast file's "inside" flag and slipping out of Ada's tea now fail tests; P1, P4, P5, P6 and P7 to P10 still pass everything (eight lines); the "I was there" text and the no-street-areas fallback were not tested separately. The nineteen that are caught: `TellDue` itself, the threat's silence (N3), Ada's invitation while held, Mickey's people never going to the police, the 0.575 line, the Ellis stop's "whether she came", the report morning, the 0.94 certainty cap, `NamesHim` at rung 4, a StreetVoice gate at 613, the week's end rule for a later day, the late-no window, Ellis asking those who never talk to police, talk through a wall, the cast file's "inside" flag, slipping out of the tea, and three game-only rules (familiarity from meetings, who shouts, night hours) caught by the C++'s own self-test only.

---

## 3. Items found ported (and what stops them being broken again)

Fuzz columns: "agree" means 0 differences in the fuzzers above.

| # | Item (handover or review letter) | C# | C++ | Test catches a break? | Route |
|---|---|---|---|---|---|
| 1 | **TellDue**: his no, the winding down and a night away reach the landing as each hour turns; each story stamped when filed (TO PORT; B3, L4) | Arrangement.cs 171 `TellDue`, 175-188, 344-358 `PassedTo` | Arrangement.h 169, 231-246, 417-428; game call `TownWeek.h` 74 | The function: yes (golden `TellDue\|...` rows; no-op fails 4). The game's call: no (P1). Agree, 600,000 scripts. | Medium |
| 2 | **RunTo**: only -1 means "no round yet" (TO PORT) | TownRounds.cs 111 | TownRounds.h 148 | No (P2). Agree, 3,000 scripts. | Low |
| 3 | **EvidenceFor / N1**: the witness's account is read under the deed's own key and sent with `topic` | Suspecting.cs 93-130 `AccountOf` | `CrimeProbe.cpp` 2897-2925 → `CrimeProbe.h` 1634-1670 (`"topic"` at 1660); `Suspecting.h` 116-160 | `crime-probe-test` (`CrimeProbe.h` 3275) and golden `OriginRung` rows | Medium |
| 4 | **N2**: no witness or overheard line says his surname | n/a (content) | `content/dialogue/crime-witness-v1.json` has no "Nowak"; `ue-probe/crime-witness-v1.json` is byte-identical; staged (`stage_game_data.py` 47) | Not checked which test pins it | Medium |
| 5 | **N3**: a threat talks a witness out of reporting | Silence.cs 279 | Silence.h 72; the game files it on the reply's `threatened` (`CrimeProbe.cpp` 5094) | Yes: golden `ThreatSilences` (removal fails 2) | Medium |
| 6 | **M3**: no tea invitation, and no envelope, while he is held | FirstWeek.cs 80-82 | FirstWeek.h 83-85; `TownWeek.h` 176, 184 | Ada's: yes (golden, fails 2). Ron's: no (P3). | Low |
| 7 | **Mickey's own never go to the police** | PoliceFile.cs 226, 323; CastDay.cs 540 | PoliceFile.h 403-405, 475; CastDay.h 381; `TownWeek.h` 131-133 | Yes (golden fails 2, route fails 4) | Medium |
| 8 | **A4's line**: loyalty above 0.575 is on his side | PoliceFile.cs 224, 244 | PoliceFile.h 401, 421 | Yes (golden fails 11) | Medium |
| 9 | **M1**: the regard's familiarity comes from his meetings, not fixed values | none (see G2) | `CrimeProbe.cpp` 6062-6064; `CrimeProbe.h` 1685 | Self-test only | Medium |
| 10 | **M2**: from nine on her day the Ellis stop asks "did she come", not "would she" | Waiting.cs 191-205 | Waiting.h 193-209 | Yes (golden fails 5) | Medium |
| 11 | **M4**: the acceptance rows use Darren (`sam`), not Ada | TownReach/Program.cs | `route-week-test.cpp` | Yes: 16 rows and 11 stops equal the Core's. `ROUTE.md`'s table equals the Core's today in every outcome column (wording aside). | Low |
| 12 | **B3 / L4** (see item 1) | | | | |
| 13 | **B2**: the wait reads its stops hour by hour | Waiting.cs 66-67 (the rule, in the class comment) | `CrimeProbe.cpp` 7000-7059; `CrimeProbe.h` 1699 `WaitHourByHour` | Self-test (`CrimeProbe.h` 3146-3160) | Medium |
| 14 | **B4 (b), (c)**: a no survives walking off and a late reply | none (game) | `CrimeProbe.cpp` 5108-5112 (`refusedAt`), 5264-5268 (`LateId`) | Not checked | Low |
| 15 | **A1, A8**: an ear-only witness files the damage heard, never a diagnostic; no pub or opening time in the bank | none | `CrimeProbe.h` 2059, 2075; `CrimeProbe.cpp` 2594; the bank has neither word | `crime-probe-test` | Medium |
| 16 | **A2**: witnesses by the hour, routine and light | none (see G1) | `CrimeProbe.h` 1970-2030; `CrimeProbe.cpp` 6703, 6903 | Self-test | High (see G1) |
| 17 | **A3**: the talk, keep-quiet and owning up use the deed's own key | none | `CrimeProbe.cpp` 404 `DeedKeyNow`, 2516-2518; `CrimeProbe.h` 2101-2117, 2195 | `crime-probe-test` | Medium |
| 18 | **A4 (familiarity), A6, A7**: meetings raise familiarity; the deed is watched one second after a Continue; no flight sighting in free play | none | `CrimeProbe.h` 1674; `CrimeProbe.cpp` 6858; `CrimeProbe.h` 1725, `CrimeProbe.cpp` 9304 | Self-test | High (see G2) |
| 19 | **A5**: a noise or a shape is suspicion, never "he did it" | Gossip.cs 64 | Gossip.h 241 (and the uses at 795, 935, 1126) | Yes (golden fails 233) | Medium |
| 20 | **A9**: the keeper finds her own window in her own words | TownNews.cs 193 | TownNews.h 279 | Night deed: yes. The noon "was there" path and the ", at my place" fallback: no (P4, P6). Agree in the police fuzzer. | Low |
| 21 | **A10**: a full, close, lit sighting is not "couldn't swear to it" | Observation.cs 353 | Observation.h 382 | Yes (golden fails 22) | Medium |
| 22 | **A11**: DS Ellis asks only the people on the street, and not those who never talk to police | PoliceFile.cs 323 | PoliceFile.h 475 | Yes (golden fails 3) | Medium |
| 23 | **A12**: the town's talk runs at each round's own minute; the reference week's order | TownRounds.cs 103-130; TownReach/Program.cs | TownRounds.h 140-170; `route-week-test.cpp` (the 21:45 "seen going" now filed in hour 21, the review's D2) | Yes (route rows) | Medium |
| 24 | **B1**: Sheila asks on a later day the first time he talks with her at the office | WeeksEnd.cs 165-170 | WeeksEnd.h 143-148; `CrimeProbe.cpp` 4847 | Yes (golden fails 3) | Medium |
| 25 | **B5**: a deed after midnight is reported that same morning | TownNews.cs 173 | TownNews.h 269 | Yes (golden fails 4) | Low |
| 26 | **B6 / B7**: a late arrival who stays is "stayed"; her answer and a threat are remembered as said to the face | FirstWeek.cs 108-116; Gossip.cs 299 | FirstWeek.h 222-231; Gossip.h 546 | B6: yes. B7: not tested here (golden rows 55718-55741 per the review). | Low |
| 27 | **CastDay.Together** has the same-area test (no talk through a wall) | CastDay.cs 496-503 | CastDay.h 322-334 | Yes (golden fails 11, route fails 16) | Medium |
| 28 | **Answer(Refused) before the ask** is accepted without a time, refused with one | Arrangement.cs 272 | Arrangement.h 183 | Both sides agree (fuzz); play cannot reach it | Low |
| 29 | **C1 to C4**: talk save stamped only when saved; `game.talk.json`; each file written whole; Ellis's and the arrest's first days saved | none (game) | `CrimeProbe.h` 2085-2098; `CrimeProbe.cpp` 7692, 7737, 7771, 7950-7951 | `crime-probe-test` for the stamp rule; the rest not tested in the repository | Medium |
| 30 | **C5 (a), (g)**: no flight sighting to lose; `SaveCodec` day 0 and `Nerve` | SaveCodec.cs 207; (Nerve not saved) | `SaveCodec.h` neither reads a day nor saves `Nerve`: same as the C# | n/a | Low |

Also found ported with no row above: `Arrangement`, `Waiting`, `PoliceFile`, `Custody`, `WeeksEnd`, `TownNews` (Aftermath), `TownRounds`, `TownSave`, `Silence.FileThreat`, `FirstWeek`, `FirstMoments`, `DayOne`, `Suspecting`, `Observation`, `Perception` (constants, sight, hearing), `Suspicion`, `MemoryStore`, `OwnLines` (generated from the C# by `tools/port_own_lines.py`, checked in CI), `PlayerIdentity.NameTold` and `HoldsHisName`, `StreetVoice` remarks and recognition, `Schedule` (from `Population.cs`), `CastDay` (places, routines, ties, weeks). Every one of ROUTE.md's calls (sections 0 to 3) has a C++ counterpart and the game calls each: `CrimeProbe.cpp` 6455-6488 (the hour), 6592-6593 (landing, envelope), 5128, 5139 (his no, Sheila's answer), 7059 (the wait), 7802-7811 (the save).

Left unported and not needed by the route's reference week or the talk program (not used by `TownReach` or `TalkHelper`): Reliability, Notice, Campaign, Beat, Informing, Household, Companionship, Economy, Wallet, Purses, Debts, Empire, Combat, Homicide, Harm, Press, Phones, Summons, ActTwo, ActThree and the other Unity-era systems. Of the C# `Population.cs` only the schedule is ported; the town's crowd bands (`AmbientCeiling`, `DistrictPulse`, `Residents`) are not, and the game places its walkers from its own `street-people.json`: not checked beyond that.
