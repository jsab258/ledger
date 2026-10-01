# Independent review, 1 October 2026: the fixes of 30 September checked, and what they opened

Reviewed `main` at e42623c (1 October, after the builder's and the town's fixes of the 30 September review, their port into the game, and the three runs in the finished game recorded in production/playtest/review-runs-2026-09-30.md). The 30 September faults are in production/audits/review-2026-09-30/FAULTS.md; their letters are kept here.

The code was read by this session and by four separate readers, one per area (the route's logic, time and state, save and reload, the port and its tests), each told to read the diff since 84bfa83 (the reviewed tree) and to run small cases where it could. This session then ran its own proofs of every High fault of 30 September through the path the game now takes, re-ran the readers' cases that decide a verdict, and re-read the deciding lines. Nothing was fixed and no game code was changed; everything written is under this folder.

## How much of this was run

- **The repository's own test table** (`tools/ci-checks.sh`) passed 38 of 38 here: CoreTests 5,055 checks, SaveChaos 149, Soak 9, the port comparison 57,864 golden rows with 0 mismatches, crime-probe-test 300, the route week's 16 rows. A pass contradicts nothing below: several faults below sit in game-side code no test reaches, and the port reader found new branches the golden table never exercises (D1).
- **This session's proofs** (`probes/`, output in RESULTS.md):
  - `recheck.cpp`: the game's own C++ headers (g++ 13, the repository's Unreal shim), repeating the few lines of the Unreal-only `CrimeProbe.cpp` each case needs, named in the file. Sightlines are assumed open; people stand where the game's `OnlookersAt` puts them.
  - `EllisRecheck`: the C# Core and the real cast file.
  - `talk-continue.sh`: the game's talk program with its stand-in replies (no model, no key).
- **The readers' programs** are in `probes/readers/`, with their output. The time reader's `gamesim.cpp` mirrors the game's free-play clock (its hour, its minute rounds and its wait) over the game's own headers; its cases quoted here were re-run by this session.

The evidence has these strengths:
- **proved**: a program ran the game's own code on the case and printed the result; by this session unless it says "by a reader";
- **proved in part**: the Core or port half ran; the game file's half is from reading;
- **checked**: this session read the deciding lines itself;
- **reported**: a reader traced it; this session did not re-read every line.

Severity, as on 30 September, for a player: **High**: met in ordinary play of the first week, and it changes what the town knows or does. **Medium**: visible, or it needs a common but specific action. **Low**: rare, cosmetic, only in the tests, or outside the first week.

---

## Part 1. The 30 September faults, one by one

### A. The route's logic

| | Verdict | Evidence |
|---|---|---|
| **A1** an ear-only witness files a debug string | **Fixed** | Proved. Hearing alone now files the damage heard ("I heard glass go over at Rita's. I never saw who did it."), never a story about him and never the diagnostic's words; only a witness who saw something shouts (`WhatWitnessFiles`, `WitnessShouts`, CrimeProbe.h 1820-1826; CrimeProbe.cpp 2408-2436). Low leftovers: B-a and B-b in Part 2. |
| **A2** witnesses ignore the hour, the routines and the light | **Fixed** | Proved. `OnlookersAt` lists whoever the cast's day puts on Quay Street that hour, from where it puts them; the light is the game's night (19:00 to 07:00) and the lamps that reach him (`NightAt`, `LightOnHim`, CrimeProbe.h 1731-1817; CrimeProbe.cpp 5858-5897). At noon on Monday, Rita and her three staff behind her counter are the ones who see his face; at 21:00 only Ron is on the street; at 02:00 nobody. Leftover: Part 2, B-c. |
| **A3** the talk, keep-quiet and owning up use another key than free play files | **Partly fixed** | Proved. The deed field, keeping quiet and owning up now use the deed's own key, `player.window_dN`. **But the evidence the talk is sent with every line still asks for the scripted story's key**, so a witness who saw him is told she holds nothing: Part 2, **N1 (High)**. |
| **A4** nobody can ever report him; no constable | **Fixed** | Proved. Meeting him raises how well somebody knows his face (0.4 once met, +0.1 a further day met, to 0.7: `FamiliarityFromMeetings`, kept in the save as `met_` lines); a witness who has met him can recognise him (rung 4), and by Jafar's ruling of 1 October reports him unless on his side (`OnHisSide` 0.575). Darren recognising him on Monday reports on Tuesday at 09:00 and the constable takes him on Wednesday at 10:00, charged. What this opened: N2, N3, N4, M1 and M3 below. |
| **A5** any copy counts as "he did it" | **Fixed** | Proved. Only a story whose first teller recognised him, or one told as known, names him (`NamesHim`, Gossip.h 239); DS Ellis asks only the holders of such a story; the street's remarks, the leak and the contradiction read the same gate (reported for the remarks). |
| **A6** after a Continue before the deed, nobody can see it | **Fixed in free play** | Checked. Every onlooker now gets a fixed second of watching (`kDeedSeconds`, CrimeProbe.cpp 5858); the watching slot that a load left unset is not used in free play. |
| **A7** walking up to Darren after the deed files a sighting | **Fixed** | Checked. The yard's flight sighting runs only in the scripted story (`FleeSightingInPlay`, CrimeProbe.cpp 7725). |
| **A8** the bank's fixed details travel as fact | **Fixed** | Checked. No time, streetlight, lamp or "before he ran" is left in the witness lines (content/dialogue/crime-witness-v1.json). |
| **A9** Rita "finds" her own window, in the third person (golden row) | **Fixed** | Proved by the port reader. The keeper finds it in her own words ("Somebody put my window in while I wasn't there; I found it when I came in."; golden row 57055); C# and C++ give the same strings. Leftovers: B-a (she only heard it) and Part 2, B-c. |
| **A10** "couldn't swear to it" even for a full recognition | **Fixed** | Proved by the port reader (golden rows CertaintyFor 2055-56, 2071-72, 2151-52 now 1). |
| **A11** DS Ellis "on Quay Street" asks most of the town (golden row) | **Fixed** | Proved. At 09:00 on Wednesday, Thursday and Friday she asks 21, 21 and 19 people, none of them off Quay Street (on 30 September 15 to 17 were); her file takes no talk from the four who never go to the police. Those four are still asked, and remember being stopped; that is consistent with the street. |
| **A12** the hour's town talk runs at the start of the hour | **Fixed** | Reported by two readers, checked here. The game runs each six-minute round at its own minute (CrimeProbe.cpp 5954) and the hour before's rounds before an hour's events (5618); the reference week runs the rounds up to each event's minute. Leftovers, Low: D2 and D3 in Part 2. |
| **A13a** over 30 m from any place, the people at Mickey's see him taken | **Not fixed** | Reported. CrimeProbe.cpp 5413 still defaults to Mickey's. Low. |
| **A13b** two bank lines speak of a pub and opening time | **Fixed** | Checked. "the fella from the pub" is now "the fella from Mickey's"; "after opening time" is gone. |

### B. Time and state

| | Verdict | Evidence |
|---|---|---|
| **B1** Sheila's question only on Sunday from 10:00 to 11:59 | **Fixed** | Proved. Talking with her at the office, she asks on Sunday from ten till twelve, and on any later day the first time he talks with her there (`AsksNow`); she asks on Monday at 10:00. Leftover, Low: Part 2, L3. |
| **B2** the wait reads its stops once and jumps up to eight hours | **Partly fixed** | Proved by the time reader, re-run here. The wait now goes hour by hour: a visit made by the night's talk stops it, and the constable's warning comes before the arrest. **A false "DS Ellis is on Quay Street" remains**, in a new form: Part 2, **M2**. |
| **B3** a no, a winding-down or a night away reaches the town's talk only at dawn | **Partly fixed** | Reported, checked in part. His no and the winding down now reach the landing as each hour turns (`TellDue`, TownWeek.h 71-75). A night away is still filed at 06:00, stamped 01:00 (Arrangement.cs 337-343); a no confirmed just after 23:00 reaches the landing at midnight, stamped 23:00, after the rounds between have run (proved by the time reader). Low. |
| **B4** his no lost across 01:00, on walking off, or in a late reply | **Fixed** | Checked. The talk program reports when Ron's question was put (`refusedAt`) and the game answers as of then (CrimeProbe.cpp 4536-4552); walking off and a late reply now keep what the line settled (4755-4762, 4678-4690). Leftover, Low: two late replies in a row lose the first (L5). |
| **B5** a deed after midnight is reported a day late | **Fixed** | Proved by the time reader. A window at Tuesday 00:30 is reported on Tuesday at 09:00 and mended at 16:00 (`FirstReportMorning`). |
| **B6** Ada's tea: late but staying is "left early" (golden row) | **Fixed, as ruled** | Proved by the time reader. 21:45 to 22:40 is now "came late for his tea, but he sat with me till gone half ten", regard +0.25 (golden row 55658). Leftover for Jafar's eye: L6. |
| **B7** Sheila's answer and a threat remembered as "I saw it myself" | **Fixed** | Checked. Both are now remembered as said to their face (`WitnessRemembering`; golden rows 55718-55741, 57726-57727). |
| **B8** low time items | **Mostly not fixed** | Reported. (1) Ada's invitation and Ron's envelope do not check that he is in the cells: **now reachable in week one**, Part 2, **M3**. (2) A save without `clock=` jumps to the next day's 09:00: old saves only. (3) The answer stop on a weekday uses the Sunday rule: now reachable, harmless (at 17:30 on Monday she is on Rita's step till six). (4) His name fades like gossip, and (5) Ellis comes for talk once a game: outside week one. |
| the spell in the cells (`SpellCouldBe`) | **Not fixed** | Proved by the time reader: a hand-edited save can keep a 34-hour spell. Hand-edited saves only. |
| `Answer(Refused)` before Ron has brought the ask | **Partly fixed** | Proved by the time reader: refused with a time, still accepted without one, the path the save's replay takes. Play cannot reach it. |

### C. Save and reload

| | Verdict | Evidence |
|---|---|---|
| **C1** after Continue, everything said in conversation can be lost: the stamp renewed before the talk program was ready | **Fixed** | Proved (this session and the save reader). A save made before the talk program is ready, or before it has loaded the save's own talk, keeps the stamp it had and sends no talk save (CrimeProbe.cpp 6399-6427; CrimeProbe.h 1835-1844). The review's case, talk at 14:57, Continue, the 15:00 autosave before the program is ready, then the load: "loaded, people 1", and Darren still holds "the pictures" after the next save. Leftovers: L1 and S2 below. |
| **C1**, second cause found by the review runs: the game asked for "talk.json", which the talk program refuses | **Fixed** | Proved. The game's file is now "game.talk.json" (`TalkSaveFile`); the talk program still refuses "talk.json" (`path-must-end-.talk.json`), and the game now logs the talk program's every save and load answer, a refusal included (CrimeProbe.cpp 4651-4660). |
| **C2** a failed Continue lays a new game over the old town | **Fixed for the reported cases** | Checked. A missing clock, agents or memory file, or another build's save, is refused before anything is restored (CrimeProbe.cpp 6476-6503). Leftovers (reported, rare): a file that exists but fails to read after that check still leaves the old mill and deed flags under the new game (6522-6531, 7019-7050); a refused Continue becomes a new game without a word, and its first autosave writes over the old save. And since every package stamps its commit SHA-UNKNOWN, the "another build's" refusal never fires in Jafar's builds (S5). |
| **C3** the save is seven files written in turn, and a load accepts any mix | **Partly fixed** | Checked. Each file is now written whole, to a .tmp and moved over in one step (`SaveWhole`, 6354-6366). Nothing ties the files to one save: a cut between clock.txt (6429) and town.json (6453) loads the clock and the town's people from one save and the police, the arrangement and the damage from the one before, so an hour's rounds and a 09:00 report can run twice (reported). And an unreadable town.json is still read as a fresh town save, whose tea is none: Ada's tea is gone for the week (TownSave.h 103; CrimeProbe.cpp 6549; a missing file, by contrast, gives a fresh week with its tea). Low, now that each file is written whole. |
| **C4** when DS Ellis first came and when he was first taken are not saved | **Fixed** | Proved by the save reader; the 171 hour-end reloads re-run here. Saved and read back (6413, 6587-6588). Its copy of the route's week saved and reloaded the town the way the game does (agents.json, each memory file, TownSave, the clock file's lines) at every hour's end, 171 points, and at 140 points inside an hour (after the 06:00 step, the deed, the 09:00 reports, Ellis, Ada's invitation, his no at 22:30, the landing, Sunday's answer): all 311 runs give the same sixteen rows and the same end state as the straight week, every story to 1e-6. ROUTE.md section 3's acceptance holds for the town itself. **No test in the repository checks it.** |
| **C5** other save items | **Mostly not fixed** | (a) A Continue within the 40 s after the deed: no longer reachable (no flight sighting in free play). (b) **Ron's pending "tell them no?" and Sheila's pending question are forgotten across a Continue**: proved by the save reader, re-run here (`talk-continue` style, `readers/save/talk-probe.sh` cases 2 and 3): straight, "Yes." is his no and her "Take it over, then?" takes his answer; after an autosave and Continue, neither. Low. (c) A quit within about 3 s of a timed-out reply can still lose the talk save: the game waits 3 s, the talk program up to 10 s (reported). (d) Line choice after a reload still differs (`LinesSaid`, `NextId` not saved). (e) Memory importance still rounded to two places. (f) One-off notices shown just before an autosave are still never shown again after Continue. (g) C#: `SaveCodec` now takes day 0 (fixed); `Nerve` still not saved (no killings in week one). (h) town.json is still not the single save ROUTE.md describes. |
| **B8** a save without "clock=" jumps to 09:00 the next day | **Not fixed** | Reported. Only an older build's save lacks it; see S5. |

### D. Where the C# and the C++ agreed and were both wrong

Proved by the port reader: the golden table regenerated from the C# is byte-identical to the committed one (57,872 rows), and the port answers all 57,864 compared rows the same.

| | Verdict |
|---|---|
| A11 `SweepAsked` | **Fixed**: rows 57847-57852 list 20, 18 and 1 people, all in the street's areas |
| B6 `TeaClosed\|late` | **Fixed**: row 55658 |
| A9 `Aftermath\|tick to noon` | **Fixed**: rows 57053-57058; the noon "there" case has no golden row (D4) |
| B7 `WeekFiled` | **Fixed**: rows 55718-55741 |
| A10 the certainty cap | **Fixed**: the CertaintyFor rows |
| A12 the reference week's order | **Fixed** in the C#; one step left in the C++ copy (D2) |
| town talk through walls (`CastDay.Together`) | **Fixed**: the office and the fish counter, 6.0 m apart through a wall, no longer talk (row 48149 and others) |
| the C++ cast reader never checks "hours" | **Not fixed**: the C++ accepts five bad files the C# refuses. Low; the committed file is valid |

No golden row the port reader found encodes a 30 September fault any more.

---

## Part 2. New faults, and old ones the fixes have made reachable

### High

**N1. A witness who saw him do it is told, every line, that she holds nothing about it. High; proved (this session and the route reader).** *(A3's leftover; already wrong on 30 September, missed then too.)*
- **Where:** `EvidenceFor` (CrimeProbe.cpp 2730) asks `Suspecting::AccountOf(G, "player.broke_a_window")`, the scripted story's key. Free play files `player.window_dN`. `AccountOf` matches the key exactly (Suspecting.h 128). The talk program derives the speaker's suspicion from that evidence and restores it at the start of every turn (TalkHelper/Program.cs 520, 663, 899).
- **Case:** Darren sees him put Rita's window in, at rung 1 or at rung 4. Asked under the game's key, his account is `held=false`; under the key he holds, `held=true`. In the route reader's run the talk derives "Trusting 0.00" from the first, "Confronting 0.89" ("I saw it myself... it was him, I would swear to it") from the second.
- **Player impact:** the witness's suspicion of him is reset to nothing at every line, so the people who watched him do it talk to him as if they had not, while the deed field the same request carries says where they saw him. Every free-play smash with a witness he then talks to.

**N2. A recognition names him "Nowak", whether or not anybody knows his name, and the town passes it on. High; proved.** *(New: rung 4 was out of reach before A4's fix.)*
- **Where:** all three rung-4 witness clauses in content/dialogue/crime-witness-v1.json say "Nowak" (cw-ws-r4-01 to -03); the game files the clause as the story's summary unchanged (CrimeProbe.cpp 2371-2405, `SummaryToFile`). Canon: what the town calls him reads out his standing, "the new owner, then Nowak", and the gate is knowing (canon.md 88-91); the game learns his name only when he gives it (`PlayerIdentity::NameTold`, `InTalk`).
- **Case (proved):** Darren has met him (a word on Monday, no name given) and sees him do it at 1.5 m: rung 4. He files "it was Nowak that put the window in on Quay Street, the new owner up at Mickey's, and there's no mistaking him". An hour of talk later Ron holds "I heard from Darren that it was Nowak that put the window in...", and neither of them holds his name.
- **Player impact:** the surname spreads through the street's memories, and so into what the talk program is sent, ahead of anybody being told it; the readout of standing that canon names is broken for everybody who hears the story. The review runs of 30 September had exactly this witness (Darren, rung 4, at 1.5 m).

### Medium

**N3. A threat never stops a report, against Jafar's ruling of 1 October. Medium; proved (this session and the route reader).**
- **The ruling** (his page of 1 October, police-witness): "seeing him do it is enough, unless he has won them over (tea, a friend) or talks them round (keep it quiet, a threat)".
- **Where:** `WouldReport` (PoliceFile.h 403-424, PoliceFile.cs 226-247) reads loyalty, nerve, a leash and a suppressed topic; `FileThreat` only files a story (Silence.h 43-58); the game's own comment says a threat "buys no silence" (CrimeProbe.cpp 4524). The talk program refuses any later keep-quiet from somebody he has threatened (TalkHelper/Program.cs 854, 866-868).
- **Case:** Darren saw it at rung 4; Tom threatens him over it. Before: would report, yes; after: yes. He reports on Tuesday and the constable takes Tom on Wednesday. Threatening a witness guarantees the report, and closes off keeping quiet.

**N4. Nobody he can talk to can be "on his side", and Mickey's own two report him. Medium; for Jafar's ruling; proved in part.**
- **Where:** `OnHisSide` reads loyalty alone (PoliceFile.h 401, 421). In free play the only change to anybody's loyalty is Ada's tea (FirstWeek.h 109-126; nothing in CrimeProbe.cpp). Sheila's trust (`bSheilaTrusts`, CrimeProbe.cpp 4574) is not loyalty; Darren and Ron have no way to be won over.
- **Case (proved):** at the middle (0.5) Sheila, Darren and Ron each would report; Ron recognising him on Monday has him taken in on Wednesday, charged. Canon calls Ron and Sheila Mickey's "inherited loyalists" (canon.md 77-79); Ron is the door man who brings the outfit's envelope.
- **Why it is his:** the page of 1 October put the rule for "a neighbour"; it did not show that the people most likely to see the deed are the three bodies on the street, two of them Mickey's own, and that Sheila trusting him does not count as "won over". The "friend" half of "a tea, a friend" has nothing in play behind it.

**M1. How well the three know his face is used two ways. Medium; proved by the route reader for the regard, reported for the game lines.**
- **Where:** the street's regard (looks, remarks, what the talk is told he knows) still uses fixed values, Sheila 0.50, Darren 0.20, Ron 0.50 (CrimeProbe.cpp 5085-5087); the witness reading and the talk's evidence use his meetings (5909, 4308).
- **Cases:** Darren, met once, recognises him at the deed (rung 4) but at 0.20 his regard says he cannot tell it is him: no look, no remark, and the talk is sent `"knowing":{"level":"nothing"}` (CrimeProbe.cpp 4309; at 0.40 the regard is "Comments"). Ron, never met, cannot recognise him at the deed on Monday (0.0), yet his regard treats him as known by sight from the first minute; canon has Tom a stranger to everybody on day 0.

**M2. The wait warns "DS Ellis is on Quay Street, asking after you" on a morning she does not come. Medium; proved by the time reader, re-run here.** *(B2's false alarm, in a new form.)*
- **Where:** at 09:00 `NineEllis` decides on the talk heard up to 08:54; the 09:00 round runs after it, in `HourEnd` (TownWeek.h 196-200; CrimeProbe.cpp 5510). The wait's Ellis stop (Waiting.h 188-202) asks whether she *would* come that day and stays live until 09:59.
- **Case:** he never takes the envelope; on Thursday at 17:00 Sheila, on Rita's step by her own day, sees the window at rung 4. On Friday the street's loudness is 2 at 08:59 and 3 after the 09:00 round, with no visit. A wait from 09:05, or one from 02:00, stops on the Ellis line; she comes only on Saturday.

**M3. Ada asks him to tea in the hour he is arrested. Medium; proved by the time reader, re-run here.** *(B8's first item, reachable now.)*
- **Where:** `TenTea` and `TwentyRon` do not check that he is held (TownWeek.h 172-183); `ConsequenceHour` runs the constable, then Ada's invitation (CrimeProbe.cpp 5495-5497).
- **Case:** Monday's window recognised by Darren; he reports on Tuesday; the constable comes on Wednesday at 10:00, the tea's day. The arrest words are followed by "Ada, from her step: There'll be a pot on at nine tonight..." while he is in the cells until 16:00.

**M4. The route's acceptance rows "window seen by Ada" cannot happen in play. Medium for the route's acceptance, Low for a player; checked, with the cast proved.**
- Ada has no body, so she can witness only from behind a window: the fish counter at 11:00 each day, and the pension counter on Thursday at 09:00 (proved from the cast file). From the fish counter Rita's glass is about 62° off her line, outside the 60° she sees; from the pension counter it is 17 m away, and before the tea she has never met him, so a face (rung 3) at best: a description, no constable.
- ROUTE.md section 4's four "Ada" rows (taken in on day 4, charged; the reference week has her at rung 4, TownReach Program.cs 408) have no counterpart in the game, so "the route played the same way must give the same" cannot be shown for them.

### Save and reload (Low)

- **S1. Who is standing where is not saved, so a Continue can change who sees the deed.** Reported. A person whose day has moved on stays put while he talks with them or looks at them (CrimeProbe.cpp 5724-5735), and the deed's reading measures whoever still stands there (5916-5932); after a load they are placed by their day at once (`bPlaceNow`, 6511). Case: he talks with Sheila on Rita's step at 17:55; the 18:00 autosave; straight on, she is still there at 18:02 and sees him break the window; after a Continue she has gone.
- **S2. The clock file takes the new talk stamp whether or not the talk is saved, and a failed talk save deletes the good file.** Proved by the save reader, re-run here (`talk-probe.sh` case 4). The game writes the new stamp and only logs the talk program's answer (CrimeProbe.cpp 6400-6429, 4651-4660); a talk save that cannot write removes the slot file by design (TalkHelper/Program.cs 266-274). The next Continue loads nobody ("missing"), while the game's own state, Sheila's trust among it, survives.
- **S3. A late reply's effects are in the talk program's save but not the game's.** Reported. A reply past 30 s is applied without a save (4678-4690); an autosave in between already queued a talk save that, answered in order, includes it. Quit before the next save: after Continue, Darren's talk believes he agreed to keep quiet, and the town's gossip has no such agreement.
- **S4. The talk's "met" comes from who he has talked to this session, not from the saved meetings.** Reported. `AcquaintanceJson` reads `GLive.Talked` (4265), which no save keeps; after Continue everybody but Sheila is sent `"met":false`, while the witness reading (5909) says they know his face. Even straight through, Ron after the envelope and Ada after her tea are sent `"met":false` on their first line.
- **S5. Saves from older builds are always taken.** Reported; the builder's own note says the same. Every package stamps its commit SHA-UNKNOWN (CrimeSha 471-478), so a save made before the meetings were kept loads with nobody knowing his face, `ellisFirst` reading "never", and, before `clock=`, B8's jump.

### Low

- **B-a. Rita only hearing her own window remembers it in the third person.** Proved in part by the route reader. The hearing-only path files "I heard glass go over at Rita's" for everybody, the keeper too, and leaves them out of the damage's tick, so she never gets her own words (CrimeProbe.cpp 2413-2427). Reached when the line from her eye to his head meets the shopfront pier, which only the real street can say.
- **B-b. Somebody who saw the glass go but not him is filed as having heard it.** Proved. Rung 0 is "nothing of the actor", not "nothing seen": Hal, 23 m away behind his window, sees the act and the window go but not who did it (slots 12, certainty 0.80, rung 0) and is given "I heard glass go over at Rita's".
- **B-c. People on Rita's step with no body "were there" and "never saw who did it".** Proved (this session, both readers). The onlooker rule leaves out anybody without a body outdoors (CrimeProbe.h 1807); the damage's tick in the deed's own hour gives everybody in Rita's area "I was there when somebody put Rita's window in. I never saw who did it." (TownNews.h 340, 361). A smash at 17:30 on Monday: Joey, Victor, Tibor and Ines get that line, and Rita "Somebody put my window in while I was there". The story names nobody and they cannot be talked to; it contradicts an empty pavement and spreads the news up to an hour sooner.
- **L1. A lost talk save still loses every conversation.** Proved for the talk program's half. C1's own case is fixed (Part 1, C). But if the talk save sent with a save never lands (the game closed before the talk program has written it), the clock file names the new stamp, the load is refused as stale, the talk program forgets everyone first, and the next save writes the loss over the good file (`talk-continue.sh`, case 2). The game saves after every reply, so a quit straight after a reply is the window; whether Unreal ends the talk program with the game is not checked here.
- **L2. Sheila can put her question at the fish market "over the book".** Reported by the time reader. The gate measures *him* within 6 m of the office's point (CrimeProbe.cpp 4286, `NearPlace`), not where she is; on Monday from 12:00 to 13:00 she stands at the fish front, 3 m from a spot 4.3 m from that point.
- **L3. On Monday there is no wait stop for her question.** Reported. The wait stops for her only on her Sunday (Waiting.h 211); a player who misses Sunday morning has no prompt.
- **L4. A no confirmed just after 23:00 reaches the landing at midnight, stamped 23:00.** Proved by the time reader (B3's class).
- **L5. Two timed-out replies in a row lose the first one's effects.** Reported. One `LateId` (CrimeProbe.cpp 4855).
- **L6. Ada's tea: a short late visit counts for more than a long early one.** Proved by the time reader. 21:00 to 22:29 is "left early", +0.05; 22:00 to 22:30 is "stayed", +0.25. With the line at 0.575, the 89-minute guest's Ada still reports a later deed she sees; the 31-minute guest's does not. It follows the 30 September ruling; it needs his eye.
- **L7. A body is held where it stands while he stays within earshot after talking.** Checked. `PlaceBodiesByRoutine` never moves somebody he has talked with until he walks out of earshot (CrimeProbe.cpp 5726, 4829-4836); waiting beside Sheila past six keeps her on the street at night, where the witness reading measures her.

### Tests (Low)

- **D1. The golden table never exercises much of the new code.** Proved by the port reader with one-line mutations of the C++: these were broken and the comparison still passed: the "there" path and its text (TownNews.h 340, 274), the mended-within-the-hour clause (329), the ", at my place" fallback (297), slipping out of the tea (FirstWeek.h 119), the cast file's "inside" check (CastDay.h 140), the no-street-areas fallback (375), the four `NamesHim` gates in StreetVoice.h (953, 1058, 1182, 2133), and `TellDue` (TownWeek.h 73). They rest on the C# CoreTests alone.
- **D2. The C++ reference week still files Ada's 21:45 "seen going" in hour 22's pass.** Reported. route-week-test.cpp 128-131 against TownReach's `Before(45)`; the rows agree only because Ada is off by then.
- **D3. The route check cannot see a missing step.** Proved by the port reader: deleting `TellDue` from the C++ changed 96 lines of the town's state and none of the 16 rows.
- **D4. The A9 golden rows cover only a night deed.** The noon case with Rita there, the review's own, is covered by CoreTests and not compared with the port.
- Latent, not reachable with today's files: the C++ capitalises only ASCII in the keeper's line, and its sort of more than sixteen area names differs from .NET's; the keeper's line can come out as "The my door kicked"; "I heard from Zlata that The new owner told Sheila..." keeps a capital mid-sentence; the onlooker rule has its own indoor test (`|Z| >= 7`) beside the cast file's "inside"; the KeeperHeardFirst fixture does not match its comment.

---

## Part 3. What still needs the game itself

The proofs ran the Core, the port and the talk program. What they cannot run is the Unreal-only game file against the real street. Short runs of the packaged game would settle:

1. **The evidence (N1):** break the window in front of Darren, talk to him, and read the reply's suspicion in the session record.
2. **The surname (N2):** the same, with Darren recognising him; read the memory files an hour later for "Nowak".
3. **Where the three face (all of A2's table):** the reading takes each body's heading from its actor; whether the person the player sees faces the same way is set by `SyncVisual`, which cannot run here.
4. **A quit straight after a reply, then Continue (L1):** whether the talk program is ended before it writes.
5. **A wait on the Friday morning of M2's case**, to see the false Ellis line in the game.
6. **Sheila on Rita's step at 17:55, the 18:00 autosave, a quit and Continue, then the window at 18:02 (S1):** whether she is still there to see it.

The four readers' own summaries of what each ran are kept with their programs in `probes/readers/` (README.md there).
