# Independent review, 30 September 2026: time, saves, the route's logic, and the port

Reviewed `main` at 565e94ea (30 September, after the builder's continuous route and the town's time-and-state sweep). The code was read by this session and by four separate reviewers, one per area, each told to read only and to trace a small case for every fault. This session then re-read the deciding lines of every fault marked **checked** below. Nothing was fixed and no code was changed.

## How much of this was run

**Nothing was run on this machine.** The Core's tests need .NET 8, which was not installed:
- Microsoft's download host is refused by the network policy.
- Ubuntu's own .NET 8 package was reachable, but the session's disk allowance had 94 MB left: this session's own earlier fetch of repository history had filled it (28 GB).
- Removing that history was refused by the session's safety check, and further attempts to make room or to use the C++ compiler were refused too. This session stopped there rather than work round it.

So **every fault below is suspected from reading, not proved by running.** The evidence has three strengths:
- **checked**: this session read the deciding lines itself and they say what the case needs;
- **reported**: a reviewer traced it; this session did not re-read every line;
- a **golden row** means the committed port table already encodes the behaviour, so the tests pass *because* of it.

GitHub's own machine runs the Core's test table (CoreTests, Soak, SaveChaos, the port comparison, StrangerTest and the rest) on this branch's push; its result is given in the pull request. On the latest main, run 316 of that workflow passed. A pass does not contradict anything here: several faults below are pinned by the very rows the tests compare.

Severity, for a player: **High** means met in ordinary play of the first week, and it changes what the town knows or does. **Medium** means visible, or it needs a common but specific action. **Low** means rare, cosmetic, only in the tests, or outside the first week.

---

## A. The route's logic: the crime, its witnesses, gossip and the consequence

### A1. Every free-play smash gets an ear-only "witness" in Sheila, and what she files is a debug string. High; checked (the geometry is reported)
- **Where:**
  - `CrimeProbe.cpp` 2326: the summary starts as `UnreadableSummaryPrefix() + GOverheard.WhyNot`.
  - 2327-2358: it is replaced only if `BankPick` finds a line for the rung reached.
  - 2370: filed with `GMill->Witness` either way.
  - 2384-2389: `PlayShout()` for her whatever the rung.
  - `CrimeProbe.h` 503-507: a reading is filed whenever the observation is not empty.
  - `content/dialogue/crime-witness-v1.json` 12-23: witness lines exist for rungs 1 to 4 only.
  - The only readers that refuse the "bank-unreadable/" string are the overheard exchange (`CrimeProbe.h` 1205) and one verdict (`CrimeProbe.cpp` 5377). Gossip, memories, street remarks and the talk program take it as it is.
- **Case (reported geometry):**
  1. Sheila's stand-in body is spawned once at a fixed point and turned to face Mickey's window (2155-2157, 2172). Rita's window is behind her.
  2. At any hour, Tom breaks Rita's window. She cannot see it (about 150° off her axis), but the smash is in earshot (about 9.9 m against about 13 m).
  3. She gets a sound-only observation at rung 0. `BankPick` fails, so her story's summary is "bank-unreadable/…".
  4. Her memory reads "I think I saw it, couldn't swear to it: bank-unreadable/…".
  5. She shouts "Stop. I mean it. Stop.", and the story spreads.
- **Player impact:** every playthrough with the smash. A shout from a woman facing the other way, and a diagnostic string in the town's gossip and in what the talk program is sent. Whether she hears it against the real street meshes needs a run.

### A2. Who can witness ignores the hour, the routines and the light. High; checked
- **Where:**
  - `CrimeProbe.cpp` 2152-2175: two stand-in bodies, spawned once at fixed places and headings.
  - `CrimeProbe.h` 173: `kLightLevel = 1.0` ("overcast_day, lanterns off") for every reading, day or night.
  - Reported: no `PlaceOf` call moves the witnesses by routine in free play (`MoveBody` is only used by the scripted encounter).
- **Case:**
  - 02:00, dark street, both routines "off": Darren's body is still in the yard and judges the deed in daylight. A reported 40 m sight range against about 10 m at a night light.
  - 12:00: Rita's routine puts her at her counter behind the glass. She is never a witness; she only "finds" the damage at 13:00 (A9).
- **Player impact:** the town's witnesses never match the people the player sees on the street.

### A3. The story key the talk, keep-quiet and owning-up use is not the key free play files. High; checked
- **Where:**
  - `CrimeProbe.cpp` 2364-2366: free play files `Fact("player", "window_d" + day, "ritas")`.
  - `CrimeProbe.h` 1615: `WindowDeedKey()` is fixed at `"player.window_d1"`.
  - `CrimeProbe.h` 1622-1626: with that key, `IsDeedStory` accepts only `broke_a_window` or the "near" predicate.
  - `CrimeProbe.cpp` 3607-3608: `DeedJson(*G, WindowDeedKey(), …)`.
  - `CrimeProbe.h` 1694-1701: `KeepQuiet` suppresses `player.broke_a_window`, the near story and `at_window_d1`, never `player.window_dN`.
  - `CrimeProbe.h` 1677-1688: `OwnedUpStory` files "he broke Mickey's window", not sensitive.
- **Case:**
  1. Day 0: Darren sees a shape at rung 1 and holds `player.window_d0`. Rung 1 files no sighting.
  2. Talking to him: `DeedJson` finds no deed story and no sighting, so no `deed` field is sent.
  3. He cannot be asked to keep quiet, threatened over it, or owned up to about it.
  4. Even with a deed field, `KeepQuiet` never suppresses `player.window_d0`, so the story keeps spreading, and `WouldReport` never sees it as kept quiet.
  5. Owning up files the wrong window, and not as sensitive.
- **Player impact:** the keep-quiet, owning-up and threat mechanics do not act on the real deed in free play.

### A4. No witness in free play can ever report him, and no constable can ever come. High; checked
- **Where:**
  - `CrimeProbe.h` 175: `kFamiliarity = 0.0` for every deed reading, on every day.
  - `Perception.cpp` 55: rung 4 (recognised) needs familiarity at least 0.35.
  - `PoliceFile.h` 425: a report is a Statement only at rung 4. 338 and 654: the constable comes only for a Statement.
  - `PoliceFile.h` 409: a damage report needs `Loyalty < 0.5`.
  - `Gossip.h` 284: loyalty defaults to 0.5. Nothing in `CrimeProbe.cpp` or `hook-cast.json` sets it; only Ada's tea moves Ada's.
- **Case:** any week, any choices. Sheila and Darren never report (loyalty 0.5 is not below 0.5), and no rung-4 reading exists, so the route's acceptance row "seen by Ada, stands her up, day 5, Charged" (ROUTE.md) cannot happen in the game. DS Ellis comes only for the street's talk.
- **Canon note:** a stranger on day 0 is canon (he has never been to the Hook). Familiarity that never rises after a week of talking to them is not.

### A5. Any witness's copy counts as "he did it", whatever the rung. High; reported (the mechanism is shared with the C# design, so this may want a ruling rather than a port fix)
- **Where:**
  - Only `Suspecting.h` 83-85 and 207-249 read the story's rung.
  - Regard remarks (`StreetVoice.h` 565-623), police loudness and `WhoSheAsks` (`PoliceFile.h` 438-444, 499-513, 728-739), and the leak's suspicion (`Gossip.h` 713-776) read only the subject "player".
- **Case:**
  1. A1's rung-0 story, or a shape at rung 1, reaches Ron at about 0.22.
  2. The regard code gives Ron familiarity 0.5 with Tom, so he "knows it is him". He says to Tom's face "Heard your name this week. More than once."
  3. With enough such stories, Ellis comes for talk and asks everyone who holds "nobody saw more than a shape".
- **Player impact:** the town behaves as if it knows who did it when nobody could say.

### A6. After a Continue before the deed, nobody can see it. Medium; checked
- **Where:**
  - `CrimeProbe.cpp` 327: `GWatchSlot = -1`.
  - 5764-5787: set to 0 only on the new-game path, which a successful load skips (5734-5754 sets the phase to `LiveWaitDeed` but leaves the slot).
  - 5871: watching time accrues only when the slot is 0 or more.
  - Reported: `Observation.h` 292-302 needs 0.35 s of watching before a sighting.
- **Case:** play past the hourly autosave, quit, Continue, break the window. Only hearing can file anything. Played straight through, the same smash can be seen. ROUTE.md section 3's "a save and load at any hour gives the same row" fails.

### A7. Walking up to Darren after the deed files a sighting that names "the new owner". Medium; reported
- **Where:** `CrimeProbe.cpp` 6446-6457, 2566-2620, 2281-2297; `CrimeProbe.h` 1646-1656, 197, 202.
- **Case:**
  1. For 80 game minutes after the deed, any 0.35 s of Tom in Darren's view counts as the man fleeing.
  2. Within 8 m, facing him, that reaches rung 3 and files "a man came through the yard at a run… I'd know his face again", plus "the new owner was at <area> on <day>".
  3. Nothing checks that Darren heard or saw the deed (reported 14.4 m from the glass, beyond earshot) or that Tom ran.
- **Player impact:** "he was at the deed" enters the town with no witness to the deed. The unwitnessed version does not stay unwitnessed if he walks straight to Darren.

### A8. The line bank's fixed details travel as fact. Medium; checked
- **Where:** `crime-witness-v1.json` 12-13 and 18: "about half nine", "against the streetlight", "under the lamp", filed as the story's clause (A1's path).
- **Case:** a deed at 12:30 in daylight, seen at rung 1. The town repeats "about half nine… a shape against the streetlight", while the deed field sent to the talk program says hour 12.

### A9. Rita "finds" her own window an hour later, in the third person. Medium; checked; **golden row**
- **Where:**
  - `TownNews.cs` 190-216 (`Tick`): every cast member in the area finds the damage except the witnesses. The owner is not left out.
  - 168: the memory is "I came by and saw it for myself: somebody put Rita's window in. I never saw who did it."
  - The same in `TownNews.h` 224-258.
  - Golden row `Aftermath|tick to noon` (perception-golden.txt 56962) is that memory.
- **Case:** a noon smash. Rita is behind the glass at 12:00 and is not a witness (A2). At 13:00 she "comes by", remembers the line above, and passes it on as the street's news.

### A10. Every witness remembers "couldn't swear to it", even a full, close, lit recognition. Medium; checked
- **Where:**
  - `Observation.cs` 334-348: every observation is clamped to 0.94. The comment at 330-333 says the cap is for "anything short of a full sighting".
  - `Gossip.cs` 377-379: "I saw it myself" needs 0.95 or more.
  - The same in `Observation.h` 361-377 and `Gossip.h` 646-648.
- **Case:** rung 4, act, victim and actor seen, in light. Certainty sums to 1.04 and is clamped to 0.94. The witness gives a Statement ("names him, and will sign it") yet remembers "I think I saw it, couldn't swear to it".

### A11. DS Ellis "on Quay Street" asks and hears most of the town. High; checked; **golden row**
- **Where:**
  - `PoliceFile.cs` 368-369: `OnTheStreet` means only that the routine's place is not "off".
  - It is used by `WhoSheAsks` (351-364) and `HearTheStreet` (293-302). The same in `PoliceFile.h` 682-687.
  - Each person asked remembers "DS Ellis, the detective, stopped me on Quay Street…" (339).
  - Golden row `SweepAsked|2` (perception-golden.txt 57662) lists 36 people asked at one visit, including `rita` (police "never") and `outfit_man` (the landing).
- **Case:** Ellis comes at 09:00 on day 3. People at the chapel, the docks and the customs shed, reported 40 to 150 m away, are "asked" and each remembers being stopped on Quay Street. `HearTheStreet` also ignores the people who never talk to police.
- **Player impact:** every visit of hers. False memories of the detective spread across the Hook.

### A12. The hour's town talk runs at the start of the hour, so talk runs ahead of, or behind, what happened. Medium; checked in part
- **Where:**
  - The live game: `CrimeProbe.cpp` 4648-4684 and 4780-4818 run all ten six-minute rounds as the clock enters the hour (`TownRounds.h` 67-81).
  - The reference week: `TownReach/Program.cs` 443-450 files Sheila's 10:40 answer, then runs the 10:00 rounds, and `route-week-test.cpp` 136-141 copies that order.
- **Case:**
  - In the game, a deed at 12:05 is first passed on at 13:00, and a talk at 13:01 can include a memory stamped 13:54.
  - In the reference, hearers get a 10:00 memory of a 10:40 answer.
  - The two orders cannot give the same rows, which ROUTE.md requires. Hour 9 of day 0 is reported never run.

### A13. Low-severity route items (reported)
- If Tom is more than 30 m from any named place, the people at Mickey's are the ones who see him taken (`PoliceFile.h` 517-541).
- Two bank lines break the content rule, "no alcohol… spoken of": `cw-ws-r4-03` ("the fella from the pub") and `cw-ov-r2-02` ("after opening time"). Only the scripted encounter can reach them. **Checked** that both lines exist.

---

## B. Time and state

### B1. Sheila's week's-end question can only be put on Sunday between 10:00 and 11:59. High; checked
- **Where:**
  - `CrimeProbe.cpp` 3554: she asks only when `GWeek.Week.Waits(GNow)`.
  - `WeeksEnd.h` 131-137: `Waits` is false on any other day, and false from 12:00 unless she has already asked.
  - The Core's own rule (`WeeksEnd.cs` 27-29): "if he does not come, she asks the next time he talks with her". `Ask` accepts any later day (`WeeksEnd.h` 140-146).
- **Case:**
  1. Day 6 passes 12:00 with no talk at the office.
  2. At 12:05 he talks to her there. `Waits` is false, so `Ask` is never called.
  3. On day 7, `Waits` is false again (a different day).
  4. She never asks; nothing is filed. The route row "his answer held by Monday noon" reads 0 of 41.
  - Reported second way in: a constable call at 10:00 on the Sunday holds him until 16:00.
- **Player impact:** the week's climax can be missed for good by being an hour late.

### B2. The wait reads its stops once, then jumps up to eight hours. Medium; checked
- **Where:**
  - `CrimeProbe.cpp` 4859-4868: one `Waiting::Next(GNow, Until)`, then `GClock.JumpTo(To)`, then `ClockHours`, then the stop's line.
  - The Core's own note (`Waiting.cs` 66-68, reported) says the game should call `Next` before each hour, as the reference week does.
- **Cases (reported):**
  - **A missed visit:** Z at 02:00, loudness 2. The night's rounds raise it to 3; Ellis comes at 09:00 and asks the street; the wait runs on to 10:00 with no stop.
  - **A false alarm:** Z at 09:20 after the 09:00 rounds raised loudness. "DS Ellis is on Quay Street, asking after you", when she comes only the next day.
  - **After the arrest:** the constable's warning "There's a constable asking for you" is shown after `ClockHours` has already arrested him at 10:00 and released him at 16:00.
- **Player impact:** a warning that is missing, false, or shown after the event; the route's stop table cannot be reproduced by the game.

### B3. A no, a winding-down or a night away reaches the town's talk only at dawn, backdated. Low; checked in part
- **Where:**
  - `Arrangement.cs` 162-173 (`TellWoundDown`) runs from `Answer`, `WoundDown` and `PassedTo`.
  - The game calls `PassedTo` only at 06:00 (`TownWeek.h` 67-70, reported).
- **Case:**
  1. He says no at 21:30, so Ron is due down at 23:00.
  2. Nothing calls `TellWoundDown` until 06:00.
  3. The outfit's man's story is filed then, stamped 23:00, after the 23:00 to 05:00 rounds have run without it.

### B4. His no can be lost at the edges. Low; reported
- **(a) Across 01:00:** a confirming "Yes." at 01:02 files `Answer(NightOf = d+1)`, which fails, although Ron has already said "I'll take your no down the landing".
- **(b) Walking off mid-reply:** the walked-off branch skips `refusedAsk`, `ownedUp` and `keepsQuiet` (`CrimeProbe.cpp` 3951-3957).
- **(c) A late reply:** one arriving after the 30 s timeout is ignored.

### B5. A deed after midnight is reported a day late. Low; reported
- **Where:** `TownWeek.h` 107 counts from the calendar day (`Now.Day < DeedDay + 1`). `DefaultMend` (`TownNews.cs` 157-162) treats before 06:00 as the night before.
- **Case:** a deed at day 2, 00:30. Witnesses first report at day 3, 09:00, although the pane is mended at day 2, 16:00.

### B6. Ada's tea: arriving after half past nine, or one gap over ten minutes, is "left early". Medium; checked; **golden row**
- **Where:** `FirstWeek.cs` 91-105 and 125-130. Golden row `TeaClosed|late|LeftEarly` (perception-golden.txt 55650).
- **Case:** with her from 21:45 to 22:40. Judged LeftEarly: she remembers "came for his tea and was off again before the pot was cold", and her regard gains 0.05, not 0.25.
- **Note:** the three-way judgement may be meant; the memory is wrong for a late arrival who stayed.

### B7. Sheila's own answer, and the person threatened, are filed as "I saw it myself". Low; checked for Sheila, reported for threats
- **Where:**
  - `WeeksEnd.cs` 200-206: her conversation memory, then `mill.Witness(Sheila, …, 1.0)`, which adds "I saw it myself: The new owner told Sheila he's…" (`Gossip.cs` 377-379).
  - Golden rows `WeekFiled|WindDown` (55712-55716).
  - Reported: `Silence.FileThreat` does the same.

### B8. Low-severity time items (reported)
- `TwentyRon` and `TenTea` do not check that he is in the cells. That cannot happen in week one.
- A save without "clock=" jumps to 09:00 the next day and can skip the tea's 23:00 close.
- The answer stop on a weekday uses the Sunday office rule (`Waiting.cs` 207-214). On Monday she has left at 17:00.
- His name, as the street's plain fact, fades like gossip and is forgotten after about two to three weeks (`Gossip.cs` 1131-1157).
- Ellis comes for talk once a game (`PoliceFile.cs` 324).

### Time fixes of 30 September: checked and holding
From the time reviewer, with this session re-reading the Arrangement lines:
- **`Arrangement.Answer` only on its own night:**
  - the envelope only while the landing is open, 22:00 to 00:59;
  - a night away only after 01:00;
  - a plain no down with Ron at 23:00, or at once after;
  - C# 242-273, C++ 156-191.
- **Holding in both:**
  - `ConstableComes(day, now)`;
  - the ageing clock never running back;
  - `Waiting` near the largest day;
  - the tea not judged before its evening;
  - the police file's same-day order;
  - far-future `PassedTo` capped;
  - the clock held during talk (`CrimeProbe.cpp` 4812).
- **Partly holding:** the spell in the cells. Its length is bounded, but `SpellCouldBe` checks the call's day, not its hour. Only a hand-edited save reaches it.
- **Not a game fault:** `Arrangement.Answer(Refused)` accepts a no on an ask day before Ron has delivered the ask, in both C# and C++, and Ron then remembers "He told me no". The talk program reads a no only while the ask stands (`TalkHelper/Program.cs` 783), so play cannot reach it. It is a gap in the Core's own rule, in the same class as the audit's Monday-for-Wednesday fault.

---

## C. Save and reload

### C1. After Continue, everything said in conversation can be lost for good. High; checked (how often is reported)
- **Where:**
  - `CrimeProbe.cpp` 5193: every save makes a new talk stamp and writes it to clock.txt.
  - 5213-5217: the talk program is told to save only if it is started and ready.
  - 5324: Continue reads the old stamp.
  - 4032-4038: the load is sent, once the talk program is ready, with the stamp as it is then.
  - `TalkHelper/Program.cs` 240-246: a load forgets everyone first.
  - 290-292: talk under another stamp is not loaded.
- **Case:**
  1. Talk to Sheila at 14:57; the save writes stamp G1 to both files. Quit.
  2. Continue. The clock crosses 15:00 about 1.5 real seconds later, and the hourly save writes stamp G2 with no talk save.
  3. The talk program becomes ready and loads with G2. talk.json says G1, so it reports "stale" and loads nobody.
  4. Its next save writes empty talk under G3.
- **Player impact:** everyone forgets what he told them, Sheila's days towards trust, his answers and any keep-quiet agreements. The game's own "Sheila trusts him" survives, so the two disagree.
- **How often:** depends on the talk program's start-up time, which is not measured; a reviewer guessed about one Continue in ten after a conversation.

### C2. A failed Continue lays a new game over the old town. Medium; reported by two reviewers
- **Where:**
  - `CrimeProbe.cpp` 5264-5287: the mill's agents and memories are restored.
  - 5318-5337: clock.txt sets the deed flags.
  - Only then (5341-5345) can the load be refused: a missing memory file, a missing clock, or a commit mismatch.
  - The new-game path (5764-5786) resets the clock, the week, remarks and the talk, but not the mill, memories, `bDeedDone`, `GDeedDay` or `GFiledSummaryA`.
- **Case:** Continue a save from an older build (the build machine and tester pass `-LedgerCommit`).
  1. The walk-round starts at day 0, 09:00, with the old window stories in the town.
  2. Ellis can come for talk with no deed this run.
  3. The talk is told of a deed not yet done.
  4. When he breaks the window, `MarkDeedTime` returns early, so the old day and hour are reported.

### C3. The save is seven files written in turn, and a load accepts any mix. Medium to low; reported
- **Where:** `CrimeProbe.cpp` 5165-5253, with no write-then-rename. `TownSave.h` 97-105: an empty or unreadable town.json gives a fresh `TownWeek`.
- **Case:** an autosave cut off during town.json.
  - Continue brings back the town and the clock, but the asks restart from night 0, the police file is empty, Rita's window is whole, and a witness can report the same window again.
  - A save cut between clock.txt and town.json replays an hour's rounds twice.

### C4. ROUTE.md section 3's acceptance cannot pass after some events. Low for play (test-only); reported
- **Where:** `TownWeek.h` 54, 133 and 151: `EllisFirst` and `TakenFirst` are not saved.
- **Case:** save after Ellis's visit and load; the row reads "never" instead of "day 4, for talk".
- **Not covered by any test:** a straight week against the same week with a save and load in the middle.

### C5. Other save items. Low; reported
- **A Continue inside the 40 s after the deed** loses Darren's chance to see him run, since `bFleeFiled` and `GFleeSeconds` are not saved.
- **Continue always starts a new conversation:**
  - Ron's pending "tell them no?" is forgotten, so a "Yes." after Continue is not his no.
  - Sheila's pending question is forgotten too, and the day closes as "won't say".
- **A quit within about 3 s of a timed-out reply** may lose the talk save, as in C1. This depends on how Unreal ends child processes, which is not checked.
- **Line choice after a reload:** it changes because `GLive.LinesSaid` and `NextId` restart at 0 and 1. That breaks exact comparison of a reloaded run with a straight one.
- **Memory importance is rounded to two decimals** in the game's memory files, which can swap the eighth memory sent.
- **One-off notices shown just before an autosave** (Ellis, Ada's invitation, Ron's envelope) are not shown again after Continue.
- **C# only:**
  - `SaveCodec` refuses day 0, the new game's first day.
  - `Gossiper.Nerve` is changed by `Homicide.Watched.Saw` but not saved (no killings in week one).
- **The game's town.json is not the single save ROUTE.md describes:** its "heard", "hints" and "news" are always empty; the real ones are in remarks.json and hints.json.

---

## D. Where the C# and the C++ agree, and both are wrong

These pass the port comparison because the golden table encodes them:
- A11 (`SweepAsked`);
- B6 (`TeaClosed|late`);
- A9 (`Aftermath|tick to noon`);
- B7 (`WeekFiled`);
- A10, the certainty cap, the same in both;
- A12, the reference week's order, copied into `route-week-test.cpp`.

Also agreeing and wrong: the Core's `Answer(Refused)` without a delivered ask (above, under B).

Two more (reported):
- **Town talk passes through walls:** `CastDay.Together` (C# 444-451, C++ 289-295) lacks the same-area test that `PeopleFor` has (657-662). Mickey's office and the fish counter, 6.0 m apart through a wall, gossip an hour before they meet.
- **A real divergence:** the C++ `CastDay::Parse` never checks the cast file's "hours". The C# refuses bad ones. Low impact; the committed file is valid.

Compared and found sensible (reported by the port reviewer):
- Arrangement and the landing;
- Waiting's bounds;
- PoliceFile and Custody (apart from A11);
- WeeksEnd's bounds;
- Ada's tea apart from B6;
- Aftermath's bounds;
- TownHours;
- the TownSave round trip;
- Gossip's `Witness`, `Tick` and `Age`;
- PlayerIdentity, Silence and OwnLines.

---

## What would turn these into proofs

Each case above is written so that a test could be made from it. The cheapest proofs, in order:

1. **C1:** a Continue with the talk program started a few seconds late. One scripted run, and the talk program's reply shows "stale".
2. **A1, A3 and A4:** one free-play smash in the packaged game, with the session record and the witnesses' memories read afterwards.
3. **B1:** a Core test of `TownWeek.Week.Waits(GameTime(6,12,0))` against `WeeksEnd.Ask(GameTime(7,10,0))`.
4. **A11, B6, A9 and B7:** already visible in the committed golden rows cited.
