# The talk task of 7 October: the ladder, who told me, and two checks

For the builder, from the bounded talk task on branch `talk` (Jafar's brief of
7 October 2026). Measured in production/research/grounded-replies/LADDER-2026-10-07.md,
production/research/invented-claims/BAIT-2026-10-07.md and
production/research/invented-claims/SUCCESSORS-2026-10-07.md. His page of
numbers: NUMBERS_PAGE.

## 1. The ladder before "that's all I know"

**What the player gets.** A character whose reply the claim check refuses twice
no longer says "that's all I know" while they hold something that bears on his
question. One rung a turn: the next relevant fact they have not told him, said
plainly; then whom to ask; then who told them; and, when he presses on what they
have already given, a refusal in their own voice with a reason. A first question
they hold nothing on still gets their honest "that's all I know". Nothing on the
ladder is the model's: every line is a written fact or a written line.

**Wire it.** Nothing to wire in the game: it lives in the talk program, which
turns it on at start (`ConversationEngine.Ladder = true`, beside `UseRules` and
`PlainFallback`). The helper's reply now says `went: "ladder-fact" | "ladder-ask"
| "ladder-told" | "ladder-refuse"` in place of `fallback` on those turns;
`fellBack` is also true for `ladder-refuse`. Already done on this branch:
production/specs/talk-protocol.md, tools/session_read.py and tools/nightly_walk.py
know the four values, `ladder-refuse` counts as talk that broke, and a ladder
turn can earn Sheila's trust exactly where a `fallback` turn could.

**What changed in the code.**
- `Core/TalkLadder.cs` (new): the rungs, the shared lines, `HeardFrom` (who told
  them, read from the memory of a telling).
- `Core/ConversationEngine.cs`: `Ladder`, `Listener`, `HasTold`, `LastRung`,
  `LastWouldHaveSaid`, `LastLeads`; what each check's list cited this turn
  (`ClaimCheck.CitedItems`) are the leads; what was told is saved in
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

## 3. Two fixes found on the way

- **The key's cap charged every Haiku call at the dearest rate** (`BudgetedClient`:
  the API answers under the dated name `claude-haiku-4-5-20251001`, which the
  rate card does not hold). The friends' five-dollar evening was really about
  three. Fixed: the requested model's price when the reply's is unknown.
  Test in ledger/TalkTests.
- **`LlmRequest.Thinking` and `Effort`** (Core/LlmClient.cs), sent only when set:
  needed if the check moves to Haiku 5.5, which thinks unless told not to.

## 4. The checks

PENDING

## Tests

New project `ledger/TalkTests` (CoreTests' Program.cs is over the push guard's
1 MB and cannot be edited): 90 checks, written before the code. Add it to
tools/ci-checks.sh beside core-tests (done on this branch). Passing at the end
of the task: TalkTests, CoreTests, Soak, SaveChaos, PerceptionGolden (the port
agrees, no drift), StrangerTest, the talk program's selftest, the session and
nightly readers' selftests, the talk-protocol check, the catalogue and the
content gate.

## Merge

Branch `talk`, from main at 39ae711a. Rebase onto main and rerun the suites.
Time recorded in production/time-log.jsonl. Key spend logged in
production/playtest/talk-runs.jsonl under `"task": "talk-2026-10-07"`.
