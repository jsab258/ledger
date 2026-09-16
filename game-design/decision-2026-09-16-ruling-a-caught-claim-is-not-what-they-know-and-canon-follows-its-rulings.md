# Ruling, 2026-09-16 (07:30Z): a claim that is caught out does not become what they know, the fix lives in the mill and not at the call site, the 2026-09-06 sweep is NOT explained by it, and canon is corrected at seven sites with a gate to keep it corrected

STATUS: LOG, 2026-09-16. NOT CURRENT once queue 345 has landed with its
tests green and the canon edits in section 9 are in the tree; from then the
tests, the golden file and canon.md are the reading copies and this is the
record of what was ruled and why.

Director ruling, two mechanical triggers folded into one spawn: a SIMULATION
change to Core (the claim path) and a CANON edit (two decided rulings canon
still contradicts). Jafar's words this morning, verbatim, are the brief for
both halves: "a claim that is caught out does not become what they know. It
is unported, so this is the cheap moment." and "a ruling that changes canon
edits canon in the same batch."

Every line number below was read in the working tree during this spawn, not
quoted from the brief. Where the brief's trace and the tree differ, the tree
is stated and the difference is named.

---

## PART ONE: THE CLAIM BUG

### 1. The chain, re-verified, with one correction to the trace

1. `ledger/Assets/Scripts/Game/LawHost.cs:234` calls `Claims.Process(...)`
   and captures `was`. Confirmed.
2. `:235` reads `if (was == ClaimResult.Contradiction) ClaimsCaught++;`.
   Confirmed. THE TRACE SAID THIS IS THE LAST READ OF `was`; IT IS NOT: `:298`
   returns it (`return was;`), which is how `SimDirector.cs:6143-6146` and
   `DialogueUI.cs:2090` learn the verdict. The correction changes nothing
   about the bug: nothing between `:235` and `:240` consults the verdict, and
   that is the fault.
3. `:240` calls `game.Gossip?.Mill?.PlayerClaims(host.Card?.Name ?? "",
   claim, game.Now)` unconditionally. Confirmed.
4. `ledger/Assets/Scripts/Core/Gossip.cs:333` is `n.Knowledge.Learn(claim);`
   and `:334-335` appends a 0.4-salience memory line. Confirmed.
5. `ledger/Assets/Scripts/Core/Suspicion.cs:53-58`: `Learn` is
   `Facts.RemoveAll(f => f.SameTopic(fact)); Facts.Add(fact);`. Confirmed.
   The class comment at `:47-48` says "an NPC cannot be talked out of what it
   knows". The code says otherwise.

THE LINK THE TRACE DID NOT CHECK, and the one the whole finding rests on:
`Claims.Process` reads `host.Knowledge` and `PlayerClaims` writes
`mill.Get(npcId).Knowledge`. If those were two objects the lie would be
filed beside the truth rather than over it. They are one object:
`ledger/Assets/Scripts/Game/GossipDirector.cs:181`, `:185` and `:188` each
build the mill agent as `new Gossiper(walkerName, walkerName, host.Memory,
host.Knowledge, host.Suspicion, ...)`, and `Gossip.cs:97` stores that
reference (`Knowledge = knowledge ?? new KnowledgeBase()`).
`ConversationHost.cs:78-80` states the intent in words: "One knowledge base
for the character's whole life: the conversation engine checks claims against
it AND the gossip mill shares it". So a lie caught at `:234` is written over
the fact that caught it at `:240`. The bug is real end to end.

The arithmetic is exact, not rhetorical. `Claims.cs:86` raises by 0.15 times
weight on a contradiction; `Claims.cs:95` lowers by 0.03 times weight when
consistent. Once the lie is stored, every repeat of it returns Consistent
(`Suspicion.cs:64`). 0.15 divided by 0.03 is five: the fifth repetition of a
caught lie returns the listener to where they stood before catching it, and
the sixth is a net gain in trust for having lied. That is the moat inverted:
consequence persistence 95 against best-in-class 85 is the number this project
claims, and this path makes a caught lie the one thing in the town that does
NOT persist.

The project has already met this exact shape once and ordered against it, in
the same file: `Gossip.cs:416-423`, "AFTER the contradiction check, never
before ... Learning it first would make the listener's own new fact agree with
itself and swallow the very contradiction the killing is supposed to expose."
`Tick` was written to avoid it. `PlayerClaims` was not.

### 2. Three shapes, priced

A. GATE THE CALL SITE. In `LawHost.Claim`, call `PlayerClaims` only when
`was != Contradiction`. One line. What it sacrifices: the same pair of calls
is hand-sequenced at three sites, `LawHost.cs:234-240`,
`ledger/StrangerTest/Program.cs:517-518` and
`ledger/StrangerTest/Sweep.cs:556-557` (the last two are the harness that
produced the 2026-09-06 numbers, and `Sweep.cs:547-549` promises "Same order
as `Play` and `LawHost`"). A call-site fix is three edits today and a fourth
the next time anyone writes the pair, which is the "one idea, two
implementations" fault `Gossip.cs:459-466` records costing a day. REJECTED.

B. REFUSE INSIDE THE MILL. `GossipMill.PlayerClaims` re-checks the claim
against the listener's knowledge and does not `Learn` on a Contradiction. It
still appends the memory line (the town keeps "he told me X" as a memory) and
returns what it did, so callers can count. `Learn` is untouched. What it
sacrifices: `CheckClaim` runs twice per claim (a list scan over a handful of
facts; nothing). What it buys: every caller, present and future, inherits the
rule; the harness inherits it without an edit; the ported `Learn` and its
golden row do not move. RULED.

C. HOLD CLAIMS AS CLAIMS. A separate store on the agent for "he told me X at
t", distinct from `Facts`; `Tick`'s Consequence 1 and `CompareNotes` check
rumours against the CLAIMS store, and a rumour colliding with WITNESSED
knowledge gets its own reason. This is the moat's own subject matter (D11:
each NPC weighs a claim against their own record of promises kept, lies
caught, alibis that checked out; that record is a claims ledger) and it is the
right end state. What it costs: a new field on `Gossiper`, the save codec
(`SaveCodec.cs:341` restores knowledge today and would restore claims), new
golden rows, the C++ `Gossiper` and `Tick` (both ported, `Gossip.h:18-22`),
and tests for both contradiction sources. Not the cheap moment. QUEUED as
346, and it is the next rung on the ladder for this aspect, not a blank.

WHICH LAYER OWNS THE DISTINCTION. The mill's `PlayerClaims` is the ONLY writer
of a player claim into knowledge (grep of `PlayerClaims(` over `ledger/`: one
definition, callers in LawHost, the two harness sites and CoreTests). `Learn`
is correct for witnessing (`Gossip.cs:290`, `:311`, `:423`), for restore
(`SaveCodec.cs:341`) and for planting (`LenaSetup.cs:48-50`, `GameController`
at four sites); the replace-on-topic rule is what "people update" means and
`PerceptionGolden` pins it (`knowledge.consistentAfterRelearn`, consumed by
`ue-probe/Source/LedgerProbe/Public/CoreGolden.h:583`). The distinction
between "learned" and "told" belongs to the one method that knows the fact
arrived by being told. That is `PlayerClaims`.

### 3. The change, dictated in shape (the builder writes it)

In `Gossip.cs`, `PlayerClaims(string npcId, Fact claim, GameTime now)`:

- Look up `n`; return as today if null.
- `var verdict = n.Knowledge.CheckClaim(claim);`
- If `verdict != ClaimResult.Contradiction`, `n.Knowledge.Learn(claim)` as
  today. If it IS a contradiction, do not touch `Facts`.
- Append the memory line in both cases (the existing 0.4-salience
  "The new owner told me: ..." line). `Claims.Process` already writes the
  0.8-salience "They lied to me" line, so a caught lie is remembered twice, at
  two saliences, which is right: what was said, and what it was worth.
- Return the verdict (or a two-value result: recorded / refused). The method
  is `void` today; it becomes something a gate can count. `LawHost` gains
  `ClaimsRefused` beside `ClaimsCaught`, and the two must agree on every run
  (the same shape as `Denounced` against `MarksFiled`, `LawHost.cs:30-36`).
- Update the method's summary: "Recorded so a later rumor can contradict it"
  stays true; add that a claim already known to be false is remembered and
  never learned.

Two comments must change with the code (rule 1, "changing code changes the
comments about it"):

- `LawHost.cs:236-239` says `PlayerClaims` is "the half `Informing` accuses
  from". It is not, on the code: `Denounce` reads `g.Best(topic)`
  (`LawHost.cs:90`, `Gossip.cs:108-109`), which is RUMOURS, and `PlayerClaims`
  writes knowledge and memory only. The half `Informing` accuses from is the
  overheard `Witness` at `LawHost.cs:292`. Correct the comment; do not change
  the behaviour it describes.
- `Suspicion.cs:47-48` becomes true again once B lands. Leave it; it is the
  invariant, and after this change the code meets it.

NO NEW BOUND. 0.15 and 0.03 are not moved. Under B a repeated caught lie
returns Contradiction every time and raises 0.15 each time; five repetitions
are plus 0.75, not zero. That is the existing constant applied the way its
author meant, and the test in section 4 PRINTS the five-step series so the
next reader sets a bound from evidence if one is ever wanted (rule 2).

### 4. What proves it: the tests, accepting case first

Core is the gate that runs on every push (`ledger-core-tests.yml` runs
`tools/ci-checks.sh`, which carries CoreTests). D16 keeps CoreTests,
PerceptionGolden and StrangerTest running; the Unity sim is legacy and runs
only on the opt-in Windows stream. So the proof is ordered Core first, sim
last.

4.1 `CoreTests`, one new test method, beside `TestConversationEngine`
(`Program.cs:3656`, which already plants "warehouse" and catches "cinema"):

    ACCEPTING, first: a fresh mill, listener with empty knowledge.
      PlayerClaims("lena", home) -> CheckClaim(home) == Consistent,
      Facts.Count == 1. A claim that is NOT caught still becomes what they
      know. Then Tick with a "warehouse" rumour from rocco -> Contradiction
      fires exactly as `TestCompareNotes` (`:3354-3358`) and the homicide
      denial test (`:11213-11219`) require today. Those two existing tests
      are the second half of the accepting case and must stay green
      unchanged.
    REJECTING (the planted case): Learn(warehouse); Process(cinema) ->
      Contradiction, suspicion s1 > 0; PlayerClaims(cinema) ->
      CheckClaim(warehouse) == Consistent, CheckClaim(cinema) ==
      Contradiction, Facts.Count == 1. Repeat Process+PlayerClaims(cinema)
      four more times: each returns Contradiction; print the five suspicion
      values on one line as a series; the fifth is >= s1.
    THE RATCHET GUARD: after the lies, Process(warehouse) -> Consistent and
      lowers by 0.03 times weight. Truth still buys what it bought.
    THE SECOND SOURCE: PlayerClaims alone on a listener holding a
      0.95-confidence witnessed fact from `Witness` (not a planted Learn)
      also refuses, so the fix is not specific to how the truth arrived.

    THE TEST IS RUN ONCE AGAINST THE PARENT COMMIT AND ITS RED IS PASTED
    INTO THE QUEUE ITEM before the fix is reviewed. A guard that has never
    been seen to fail is a guard nobody knows can fail (rule 5b).

4.2 `PerceptionGolden`: a new `claims` block after the `knowledge` block
(`Program.cs:656-674`), driven through a real `GossipMill.PlayerClaims` on a
planted fact: `claims.uncaughtLearned`, `claims.caughtKeepsTruth`,
`claims.caughtVerdictRepeat`, `claims.countAfterCaught`. ACCEPTANCE IS A
DIFF SHAPE: `ue-probe/perception-golden.txt` gains lines and changes none.
Any changed `knowledge.*` row means `Learn` was touched, which this ruling
forbids. The builder checks what the C++ consumer (`CoreGolden.h`) does with
rows it does not implement; if it fails on unknown keys, the rows land under a
prefix it is taught to skip, with the skip counted and printed.

4.3 `StrangerTest`: `Days.Morning` and `Play` inherit B with no edit. The
sweep verdict line gains a tally of `Claims.Process` verdicts over ALL seeds
(`claimUnknown=N/M claimConsistent=N/M claimContradiction=N/M`), and the
sweep is re-run. THE EXPECTED READING IS NO CHANGE: `lieCaught=90/648` and
`lieHeard=0/90` reproduce exactly, because section 5 shows the bug never
fired in that grid. If either number moves, the instrument or the fix is
wrong, and that is found before anything is believed.

4.4 The sim gate (legacy Unity, opt-in stream): after `_claimCaught` at
`SimDirector.cs:6145`, `_claimTruthKept = listener.Knowledge.CheckClaim(the
docks fact) == Consistent`, printed on the done line at `:15448` as
`truthKept=` beside `caught=`, and folded into `claimsOk` at `:14893`. Third
proof, not first.

### 5. Does this explain the 2026-09-06 measurement? NO, and here is the number

Queue 138 and queue 127 record the sweep's finding: "caught lies did not
change the spoken responses ... overheard gossip is a separate working route".
The loop was then built on gossip. The question was whether that decision
routed around this bug.

It did not, and the sweep's own output says so:

- `Sweep.cs:292` defines a caught lie as `Tick1Contra + Tick2Contra > 0`: a
  RUMOUR colliding with the stored claim in `Tick` (`Gossip.cs:400`). That
  route REQUIRES the lie to have been stored by `PlayerClaims`. It never
  counts `Claims.Process` at all.
- `production/stranger-test/study-sweep.txt`, the committed output of the
  run stamped `atUtc=20260906-142553`: the per-path chain prints the
  `Claims.Process` verdict as `claim=<value>/<verdict>`. Counted this
  morning: 72 lines carry a verdict, 72 read `/Unknown`, 0 read
  `/Contradiction`, 0 read `/Consistent` (36 further paths are `none/none`,
  the silent answer). The verdict line reads `lieCaught=90/648
  lieHeard=0/90`.
- Why Unknown every time: Lena never holds hard knowledge in that harness.
  `Program.cs:449` and `Sweep.cs:538` file sightings at confidence 0.9
  (0.55 with the coat), and `Gossip.cs:290` promotes to knowledge only at
  0.95. Nobody in the grid could be lied to about something they KNEW, so
  the overwrite had nothing to overwrite. Queue 127's "suspicion moved 0.060
  to 0.176" is the `Tick` collision magnitude (0.35 times passed), not the
  0.15 of a catch at the moment of telling.

So: ESTABLISHED for seed 107 by the printed chain (0 of 72), and for the
other five seeds by construction (the seed changes the job's dice, not
whether a 0.9 can become a 0.95). What settles it fully rather than by
argument is the tally in 4.3 over all six seeds, and it costs one sweep run.

WHAT THE SWEEP THEREFORE COULD NOT SEE, which is the finding that matters:
the grid never put a lie in front of an eyewitness. The at-the-moment catch,
the route this bug sits on and the route a player feels most directly ("I
was there, I saw you"), was 0 of 648 sessions. The gossip decision stands on
its own evidence (queue 127's arithmetic of the Comments rung is untouched by
this), but the instrument that produced it has a blind spot exactly where
this bug lives. Queue 348 adds the eyewitness arm.

### 6. The cost after the port, stated from what is ported today

Measured this morning in `ue-probe/Source/LedgerProbe/Public/`:
`Suspicion.h:154-192` ports `ClaimResult`, `KnowledgeBase.Learn` and
`CheckClaim`; `Gossip.h:18-22` ports `Gossiper`, `Witness` and `Tick`
including Consequence 1 at `:596`; `CoreGolden.h:577-583` consumes the four
`knowledge.*` golden rows. `Gossip.h:24-28` lists `PlayerClaims` under "OUT
OF SCOPE AND NOT HERE", and `Claims.Process` has no C++ site at all.

So Jafar's "it is unported" is exactly true of the two methods B touches and
exactly false of `Learn`. That settles the layer question a second way: a fix
inside `Learn` would change ported code and a consumed golden row today, in
two languages, and is refused on cost as well as on semantics. B costs one C#
edit, one test method, added golden rows and no C++ line.

After the port, the same fix is two edits in two languages, a regenerated
golden with a changed row, and a port-equivalence run. Worse: if the port
copies the pair as it stands, every C++ test written against it pins the bug,
and the reference the port is "checked against" (D16) would be checking that
the bug was faithfully reproduced. That is the ratchet in its purest form, and
it is why the cheap moment is now and not after the next port batch.

### 7. What this does not decide, and what goes to the queue with a name

- 345: the fix in section 3 and the proofs in section 4. THE BUILDER IS
  WAITING ON THIS ITEM; it is dispatched first.
- 346: claims held as claims, separate from knowledge (option C), including
  one Core entry for the Process+PlayerClaims pair so three call sites cannot
  drift. Design and cost first; it is the next rung.
- 347: `Gossip.cs:400-405` and `:498-501` raise suspicion of the player with
  the reason "contradicts what the new owner told me" whenever a rumour
  contradicts KNOWLEDGE, including witnessed knowledge the player never
  spoke about. A rumour disagreeing with what I saw is not a lie by the
  player. Found in this read; not measured; 346 fixes it structurally, and
  347 is the finding on its own so it is not lost if 346 waits.
- 348: the sweep gains an eyewitness arm (one witness filed at confidence
  0.95 or above) and the `claimVerdict` tally on its verdict line.

Nothing here touches the visual slice ruled at 06:35Z; the two builders on
it are not blocked by this and do not block it.

---

## PART TWO: CANON FOLLOWS ITS RULINGS

### 8. The standing rule, its wording, and where it lives

Jafar's sentence is the canon form of D21 (a decision names the tiles it
changes and they are re-typed in the same batch). It is recorded in three
places, each for a reader who would otherwise miss it:

In `canon.md`, appended to the STATUS block at the top, the two lines that
every agent reads before anything else:

    A ruling that changes canon edits canon in the same batch (Jafar,
    2026-09-16). A DECIDED record whose subject is a world fact names the
    canon lines it changes, and canon cites the record at those lines.

In `ledger-v2/respec/decision-register/rulings-log.md`, under "Why this
shape", one paragraph: the register is the spine and canon is its reader;
a decided world fact that is not in canon is a violation the next session
will act against, as happened on 2026-09-16 with D16, D19 and D24.

And as a GATE, because a rule written down is a rule a busy session forgets,
and the two cases that fired this ruling were each two to six days old.
Ordered to the queue as 349, modelled on `tools/goal-block-check.py`
(same shape: selftest, accepting case is the live tree, rejecting fixture is
synthetic, the source wins):

`tools/canon-register-check.py` asserts three things, each with its
denominator printed:

1. NO OPEN ITEM IS DECIDED. Every `Dn` cited under canon's `## OPEN` heading
   resolves to a register record whose status line is not DECIDED, APPROVED
   or SUPERSEDED. (D1 under OPEN 1 fails this today.)

   AMENDED 2026-09-16 by section 3.1 of
   game-design/decision-2026-09-16-ruling-wire-or-delete-the-last-instrument-and-seven-settlements.md,
   so that the spec and the tool do not disagree: THE UNIT OF THIS ASSERTION
   IS THE ITEM, NOT THE CITATION. An OPEN item is red when the item as a
   whole is a decided thing still filed as open, not when any `Dn` inside it
   resolves to a DECIDED record. The reason is in that ruling and is not a
   preference: section 9.2 of THIS record dictated item 1 under `## OPEN` as
   "Engine: DECIDED, Unreal (D16 ...)", kept numbered so that "OPEN 2" keeps
   its meaning, so a per-citation unit would have arrived red on the very
   line this ruling dictated. A gate red on its own spec's text is the 06:35Z
   failure. Both modes print and both are counted.
2. NO SUPERSEDED RECORD IS CITED WITHOUT ITS SUCCESSOR. Every `Dn` cited
   anywhere in canon whose record carries "SUPERSEDED ... BY Dm" is cited
   beside `Dm`. (Nothing fails this today; D15 is not cited by number.)
3. EVERY RECORD THAT NAMES CANON IS IN CANON. Every DECIDED or APPROVED
   record whose text says it applies to canon (today D17, D18, D19, D24, by
   the phrases "canon.md, as a rule", "Apply it to canon", "Recorded in
   canon") has its `Dn` present in canon.md. (D19 and D24 fail this today.)
   The phrase list is the weak link and the tool prints which phrase matched
   which record, so a record that says it in new words is visible as
   unmatched rather than silently passing. From this ruling on, a new
   D-record carries one machine-readable line, `CANON: none` or
   `CANON: edits <lines or heading>`, and the tool reads that line first
   and the phrases only for records older than today.

What the tool does NOT claim: that canon's sentences AGREE with the ruling.
It checks citation and status, the same way `content-gate.py --enforceable`
says which clauses it can read. Agreement is a reading, and the reading is
the resident's on every canon edit.

Wired into `ledger/verify.py` beside `goal-block-check` and into
`tools/ci-checks.sh`. It lands AFTER the corrections in section 9 are in the
tree, so its accepting case (the live canon) is green on the commit that
introduces it; a gate that arrives red teaches everyone to ignore it.

### 9. The corrections, dictated verbatim for the resident (D43: applied, not re-ruled)

Line numbers are canon.md as read at 07:30Z this morning. Apply top to
bottom; each edit is one line or one block, and nothing else on the file
moves.

9.1 D19 (Mickey's is a minicab office), FOUR sites, not two:

Line 10, `the Hook (old port, the player's pub)` becomes:

    the Hook (old port, Mickey's, the player's minicab office)

Line 24, `street, Quay Street, the Hook, the player's pub on it.` becomes:

    street, Quay Street, the Hook, the player's minicab office on it.

After line 24, one new bullet in the Game section:

    - MICKEY'S IS A MINICAB OFFICE (D19, decided 2026-09-14, supersedes
      D15's pub; D15's siting on Quay Street stands). Its information room
      is the business: a book of every fare, a radio nobody can help
      overhearing, a yard with two escapes, a rank outside. Other pubs
      remain as buildings on the street, boarded or serving food, never
      entered for drink.

Line 49, `has died and left him the pub, Mickey's, in the Hook, plus a` becomes:

    has died and left him Mickey's, a minicab office in the Hook (D19), plus a

Line 108, `Minted: Mickey's (the pub), the Tivoli (cinema),` becomes:

    Minted: Mickey's (the minicab office; a pub until D19), the Tivoli (cinema),

9.2 D16 (the engine is Unreal), ONE site. Lines 115-116 under `## OPEN`,
item 1, become:

    1. Engine: DECIDED, Unreal (D16, 2026-09-10; closes D1). Unity is the
       legacy reference build; the C# Core stays the source of truth the C++
       port is checked against. Kept as item 1 so that "OPEN 2" above keeps
       its meaning; it is not open.

9.3 D24 (what LEDGER is not), ABSENT. D24 line 4 says "Recorded in canon
beside the pillars"; canon has no such lines (searched for "sandbox",
"shooter", "story-first": nothing). Insert after the `## The moat
(unchangeable)` section and before `## Brands and law`:

    ## What LEDGER is not (D24, decided 2026-09-14)
    - NOT an open-world sandbox, NOT a shooter, NOT a driving game, NOT an
      economy simulation, NOT a story-first narrative game. It is a small
      dense town where what people know about you is the mechanic.
    - Anything that does not feed perception, memory, gossip or consequence
      gets the smallest budget that keeps it from looking wrong. A spend
      rule, not a ban: driving, fighting and trade may exist and must not
      look broken.

9.4 The STATUS block, lines 3-5, gains the two lines in section 8.

9.5 Register-side, same batch, because the staleness has a mirror there:
`D1-engine-probe.md:2` still reads `Status: OPEN, probe authorized`; append
one line, `CLOSED 2026-09-10 BY D16: the engine is Unreal.` And
`rulings-log.md:46` gains `(CLOSED by D16)` in the form lines 50 and 60
already use for D5 and D15.

### 10. The sweep: what was examined, what hit, what did not

DENOMINATOR: 45 D-records exist in `ledger-v2/respec/decision-register/`
(D1 to D45), plus two non-D files (`rulings-log.md`, `queue-rulings-2026-09.md`)
which are indexes and logs, not decisions, and were used as the index.

- 16 records read in full or to their ruling text: D1, D2, D3, D11, D12,
  D14, D16, D19, D24, D25, D29, D30, D33, D34, D35, D40.
- 29 records examined by title and status line and classified as process,
  scheduling or scope rulings that state no world fact canon carries: D4,
  D5 (superseded), D6, D7, D8, D9, D10, D13, D15 (superseded), D17, D18,
  D20, D21, D22, D23, D26, D27, D28, D31, D32, D36, D37, D38, D39, D41,
  D42, D43, D44, D45. D8, D9, D17 and D18 are cited in canon and their
  text there was read against the records: consistent.

HITS, 3 records, 6 canon sites plus one absent section: D19 (lines 10, 24,
49, 108), D16 (lines 115-116), D24 (no section). Jafar named two records;
the sweep found the third, and D19 had four sites where two were named.

JUDGEMENT ITEMS, not applied, for the owner: D29 rules body language "part
of the MOAT, not polish"; canon's moat list (lines 95-103, headed
"unchangeable") does not list it, and D29 does not instruct a canon edit.
D30 records the narrative as owed and opens a writing lane after the visual
slice; canon's OPEN 2 says survival of the baseline "is decided in Phase 1
planning". Not a contradiction; a stale pointer at most. Neither is edited
by this ruling; both are named so the next reader does not rediscover them.

NOT EXAMINED: the 71 director rulings under `game-design/decision-*.md`.
They are operational and do not decide world facts (rulings-log.md:13-18),
and a full read is not owed by this spawn; if one of them minted a world
fact outside a D-record, that is itself the violation section 8 now names.

---

## 11. Dispatch order and what the next reader does

1. Queue 345 to a systems-builder now, with sections 3 and 4 as the brief
   and the standing instruction not to commit. The reviewer opens the red
   run against the parent commit before reading the green one.
2. The resident applies section 9 in one commit, then files 349 with
   section 8 as the brief. Section 9 before 349, never after.
3. 347 and 348 filed with their sections as the finding; 346 filed as a
   research task with option C's cost list as its first paragraph.
4. This record is indexed in `rulings-log.md` under 2026-09-16.

Queue numbers 345 to 349 were the next free at 07:30Z (344 was the highest
in `production/queue/`); if a concurrent lane has taken one, the resident
renumbers and notes the substitution here.

<!--RULING spawn=2026-09-16T07:30:50Z-->
