# The talk task of 7 October: the ladder, who told me, and two checks

For the builder, from the bounded talk task on branch `talk` (Jafar's brief of
7 October 2026). Measured in production/research/grounded-replies/LADDER-2026-10-07.md,
production/research/invented-claims/BAIT-2026-10-07.md and
production/research/invented-claims/SUCCESSORS-2026-10-07.md. His page of
numbers: https://claude.ai/artifact/DKBhrC8w4s1uTQ5GM2krNq ("LEDGER Talk Before
and After", private to him until he shares it).

## 1. The ladder before "that's all I know"

**What the player gets.** A character whose reply the claim check refuses twice
no longer says "that's all I know" while they hold something that bears on his
question. One rung a turn: the next relevant fact they have not told him, said
plainly; then whom to ask; then who told them; and, when he presses on what they
have already given, a refusal in their own voice with a reason. A first question
they hold nothing on still gets their honest "that's all I know". Nothing on the
ladder is the model's: every line is a written fact or a written line.

**Measured** (production/research/grounded-replies/LADDER-2026-10-07.md): over
four question sets, 145 questions the character could answer, empty answers 35
today, 19 with the ladder (the fresh sixty: 22 to 12); 29 ladder lines, none
inventing anything, 7 beside the point.

**Wire it.** Nothing to wire in the game: it lives in the talk program, which
turns it on at start (`ConversationEngine.Ladder = true` and `JudgeLadder = true`,
beside `UseRules` and `PlainFallback`). The judge is one short call to the check's
model on the turns the ladder climbs (median 0.54 s, slowest 1.05 s, about
$0.0002); its step shows as `ladder-judged` in the reply's `steps`. The helper's reply now says `went: "ladder-fact" | "ladder-ask"
| "ladder-told" | "ladder-refuse"` in place of `fallback` on those turns;
`fellBack` is also true for `ladder-refuse`. Already done on this branch:
production/specs/talk-protocol.md, tools/session_read.py and tools/nightly_walk.py
know the four values, `ladder-refuse` counts as talk that broke, and a ladder
turn can earn Sheila's trust exactly where a `fallback` turn could.

**What changed in the code.**
- `Core/TalkLadder.cs` (new): the rungs, the shared lines, `Leads` (what bears
  on his line), the judge's request and reading, `HeardFrom` (who told them,
  read from the memory of a telling).
- `Core/ConversationEngine.cs`: `Ladder`, `Listener`, `HasTold`, `LastRung`,
  `LastWouldHaveSaid`, `LastLeads`; what each check's list cited this turn
  (`ClaimCheck.CitedItems`) are the leads, judged (`JudgeLadder`) or, if the
  judge fails, gated by a distinctive shared word (`ClaimCheck.SharesTellingWord`);
  what was told is saved in
  `CaptureTalk` under `"told"` and shown to the writer of later replies; today's
  fallback kept, untouched, as `TodaysFallback`.
- `Core/StreetFacts.cs`: `AboutOf`, `NameOf`, `IsIntroduction` (somebody else's
  job is a pointer: "You'd want Sheila for that").
- The three talking cards (production/cast/cards): new own words `ask`, `told`
  and `refuse`, in each voice. Each passes the content rule, the safety rule,
  the real-names list, the promise list and the reply guard (TalkTests).

**Port.** None: the talk runs beside the game as the tested C# helper (his
ruling of 23 September). Restage the friends' copy so it carries the new cards.

**Save.** The helper's talk save gains `"told"`: listener to what they were told.
Older saves read as nothing told.

**Walk it.** Ask Sheila, Ron and Darren a newcomer's questions they half know
(who has the keys, what time we open, did Mickey live round here) and press on
each twice. Expect a fact, then whom to ask, then a refusal with a reason; never
the same fact twice; never "that's all I know" while a relevant fact is unsaid.

## 2. Who told me

**What the player gets.** A character who heard a story can say who told them
("Sheila told me that ..."), at every retelling, not only who first saw it.

**Measured** (ClaimBench `whotold`, three seeded days of 14 people, no model):
who told them known for 0 of 177 second-hand copies before, 177 of 177 after,
all kept through a save; reasons naming the teller 0 of 115 before, 115 of 115
after.

**What changed in the code (C#).** `Rumor.ToldById` (Core/Gossip.cs): set by
`Tick` (the speaker) and `CompareNotes` (the partner asked); cleared when a heard
copy becomes their own sighting (`Witness`, `PlayerIdentity`). `SaveCodec` writes
`"teller"` only when it is not the first witness, and reads a story one telling
out as told by the witness (so every older save, and the golden table, read
correctly). `Suspecting.AccountOf(g, topic, nameOf)` fills `DeedAccount.ToldBy`;
`Derive` then says "Sheila told me that ..." instead of "I heard that ...". The
talk program reads `evidence.account.toldBy`.

**Port (C++, ue-probe, never opened here).**
1. `Public/Gossip.h`: `std::string ToldById` on `Rumor`; in `Tick` (line ~783)
   `Heard->ToldById = Speaker->Id`; in `CompareNotes` (line ~929)
   `Heard->ToldById = PartnerId`; in `Witness`, wherever a copy is set to
   `Hops = 0`, clear it. `Public/PlayerIdentity.h`: the same where the name story
   is made first-hand.
2. `Public/SaveCodec.h` (beside `"rung"`, line ~883): write `"teller"` when set
   and different from `OriginId`; read it, else the origin for `hops == 1` when the
   origin is not the holder, else empty (`SaveCodec.TellerOf` in the C#).
3. `Public/Suspecting.h`: `ToldBy` on `DeedAccount`; `AccountOf` takes a name
   lookup (the mill's `DisplayName`); `Derive` (line ~201) says
   `ToldBy + " told me that " + Summary` when set.
4. `Public/CrimeProbe.h` `EvidenceAccountFields` (line ~1658): add
   `,"toldBy":"<name>"` when `A.ToldBy` is set; `EvidenceAccount` passes the
   mill's name lookup.
5. Golden rows: none change today (the port check passes, 57,914 checks, 0
   failures, no drift). When the port carries the teller, add it to
   `GossipFuzz`'s `R` and `E` rows in both engines in one commit. NOTE: the
   committed table is 2.7 MB, and the push guard refuses any changed file over
   1 MB, so `--accept` can no longer be pushed; that needs your call (move it to
   F: game-inputs as the big meshes were, or split it).

**Walk it.** After a deed, ask a second-hand hearer why they look at him like
that: the reason names who told them.

## 3. Fixes found on the way

- **The key's cap charged every Haiku call at the dearest rate** (`BudgetedClient`:
  the API answers under the dated name `claude-haiku-4-5-20251001`, which the
  rate card does not hold). The friends' five-dollar evening was really about
  three. Fixed: the requested model's price when the reply's is unknown.
  Test in ledger/TalkTests.
- **`LlmRequest.Thinking` and `Effort`** (Core/LlmClient.cs), sent only when set:
  needed if the check moves to Haiku 5.5, which thinks unless told not to.
- **Real places, writers and works** (Core/RealWorld.cs): the talk's rule and
  code's list now cover them (the bait found London, Westminster and Shakespeare
  said back); towns that are ordinary words (Hull, Bath) only as names; not
  Madonna (the chapel's).
- **"Stay in character"** is refused by the reply guard (Core/ResponseValidator.cs).
- **The racing page** (Core/ContentWords.cs `racingpage`): Ron read "the racing
  results"; canon keeps gambling out of speech. The content gate finds no written
  line it touches.

## 4. The checks

**Songs, poems, quotes and real names** (production/research/invented-claims/BAIT-2026-10-07.md):
forty bait questions to each of the three. Before: 4 of 120 replies named
something real, all echoes. After the fix: 0 of 120, and 0 of 40 on LEDGER's key
through the API. Nothing to wire beyond this branch.

**The check's successor** (production/research/invented-claims/SUCCESSORS-2026-10-07.md):
recommended, Haiku 5.5 with the list's thinking off and the second looks'
thinking at low effort: as accurate as Haiku 4.5 over 238 labelled details and
60 labelled replies, the same median speed, up to 0.9 s slower in the slowest
tenth, a tenth of the price. To switch, when you choose: set the talk program's
`CheckerModel` apart from `Models.Ambient` (which also writes small talk); send
`Thinking = "disabled"` on the list (`ClaimCheck.RequestItems`) and
`Thinking = "adaptive", Effort = "low"` on the looks (`RequestVerify`), with room
in `MaxTokens` for the thinking (+4000 in the bench); let the relay pass
`thinking` and `output_config` (Relay.cs strips every other field today); time
the first sentence's check on the real path before and after.

## Tests

New project `ledger/TalkTests` (CoreTests' Program.cs is over the push guard's
1 MB and cannot be edited): 121 checks, each written before its code. Add it to
tools/ci-checks.sh beside core-tests (done on this branch). Passing at the end
of the task: TalkTests, CoreTests, Soak, SaveChaos, PerceptionGolden (the port
agrees, no drift), StrangerTest, the talk program's selftest, the session and
nightly readers' selftests, the talk-protocol check, the catalogue and the
content gate.

## Open, for you

- The 19 still empty are mostly a knowledge gap: say the people lines (P items)
  plainly next ("Who's the priest round here?" has no plain fact today).
- The judge passes 7 of 29 facts about the same thing that do not answer (how
  the drivers are paid, answered with how many there are): a stricter judgement
  prompt, measured on the recorded turns with `ladder-replay --judge`.

## Merge

Branch `talk`, from main at 39ae711a. Rebase onto main and rerun the suites.
Time recorded in production/time-log.jsonl. Key spend logged in
production/playtest/talk-runs.jsonl under `"task": "talk-2026-10-07"`.
