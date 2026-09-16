line: simulation (ledger/Assets/Scripts/Core/Gossip.cs, Game/LawHost.cs,
  Game/SimDirector.cs; ledger/CoreTests, ledger/PerceptionGolden)
spec: `LawHost.Claim` detected a contradiction with `Claims.Process` and then
  passed the same claim to `GossipMill.PlayerClaims`, which called
  `KnowledgeBase.Learn`, which does `Facts.RemoveAll(f => f.SameTopic(fact));
  Facts.Add(fact);`. So a lie the NPC had just caught REPLACED the witnessed
  truth that caught it. `KnowledgeBase`'s own class comment says "an NPC cannot
  be talked out of what it knows"; that is the invariant its code broke.

  THE LINK: `GossipDirector.cs` builds each mill agent with `host.Knowledge`, so
  `Claims.Process` reads and `PlayerClaims` writes ONE `KnowledgeBase`.

  THE ARITHMETIC: `Claims.cs` raises suspicion 0.15 on a contradiction and
  lowers 0.03 when consistent, and every repeat of a stored lie read Consistent.
  Five repetitions of a caught lie cancelled the penalty for being caught and
  the sixth was a net gain in trust.
acceptance: a caught claim is refused by the mill and the witnessed fact
  survives; an UNCAUGHT claim is still learned; the truth still lowers
  suspicion 0.03 afterwards; the five-repetition suspicion series is printed
  rather than only asserted
max_sessions: 1
status: FIX WRITTEN, NOT COMMITTED 2026-09-16, raised by Jafar from an external
  audit. Ruled in
  game-design/decision-2026-09-16-ruling-a-caught-claim-is-not-what-they-know-and-canon-follows-its-rulings.md,
  sections 3 and 4 (option B: refuse inside the mill; gating the call site and
  fixing inside `Learn` were both REJECTED there, with reasons).

  NUMBERED 350 AND NOT 345. The ruling's section 11 reserved 345 to 349 and
  said the resident renumbers if a concurrent lane takes one. A concurrent lane
  took 345 (the role-proxy split). 346 to 349 are untouched and still mean what
  the ruling says they mean.

  THE RED, RULE 5b. The new test was run once with the parent commit's one
  behavioural line restored (`n.Knowledge.Learn(claim);` unconditional, the
  signature kept so the test compiles), against 542804a1's behaviour:

      A caught claim is not what they know:
        ok - a claim about a topic the listener knows nothing about is Unknown, not refused
        ok - an uncaught claim STILL becomes what they know
        ok - and it is the one fact they hold on the subject
        ok - a stored claim is still exposed when the rumour reaches the person it was told to
        ok - repeating a claim they already hold is Consistent
        ok - and does not file a second copy
        ok - the lie is caught
        ok - and catching it costs the liar something
        ok - and the mill REFUSES it, and says so, so a caller can count refusals

      FAILED: the witnessed truth is still what she knows: she cannot be talked out of it

      [exited with code 1]

  READ THE ACCEPTING HALF OF THAT RED, because it is the half that matters:
  every accepting check passed against the OLD behaviour too. The guard does not
  fire on an honest claim, on a repeat of a claim they already hold, or on a
  claim nobody can contradict. It fires on exactly one thing, and that thing is
  the bug.

  THE GREEN: `All 4405 checks passed`, against a baseline of `All 4373 checks
  passed` on the same tree before the change. Plus 32, all of them the new test.

  THE SERIES, printed by the test rather than asserted blind (rule 2), being the
  running suspicion value after each of five repetitions of one caught lie:

      suspicion after each repetition of one caught lie (running value, 5 repetitions): 0.150 0.300 0.450 0.600 0.750

  Five times 0.15 with nothing given back. Under the old behaviour repetitions
  two onward read Consistent and each returned 0.03.

  WHAT IS NOT DONE, and it is the golden. `PerceptionGolden` gained the `claims`
  block section 4.2 ordered, and it was generated to scratch and diffed: the
  table gains 7 lines and changes 0, which is the acceptance shape the ruling
  named, and no `knowledge.*` row moved, so `Learn` was not touched.
  `ue-probe/perception-golden.txt` WAS DELIBERATELY NOT REGENERATED, because the
  question the ruling flagged as unresolved has an answer and the answer is bad:

  - `CoreGolden.h` does NOT fail on an unknown key. A key no scenario produces
    sets `A.Known = false` and returns, with the comment saying a missing key is
    UNKNOWN rather than wrong.
  - But `ue-probe/tests/core-port-test.cpp` asserts `Loud(TotalUnknown == 0,
    "no row in the table names a function this build cannot answer")`.

  Measured on the committed table before the block existed: `2517 check(s), 0
  failure(s) over 2498 golden row(s), 0 mismatch(es), 0 unanswered`. Measured on
  the regenerated table: `2517 check(s), 1 failure(s) over 2498 golden row(s), 0
  mismatch(es), 7 unanswered`. ZERO MISMATCHES BOTH TIMES: the port still agrees
  on everything it can answer, and the single failure is the unanswered-row
  assertion and nothing else.

  So landing the regenerated table turns `ledger/verify.py` red until the reader
  is taught to skip an unported scenario BY NAME and print the count it skipped,
  which is what the ruling ordered as the fallback. That edit is in `ue-probe/`,
  which this batch was told to stay out of and which another lane holds. The C#
  half is written and its comment names the cost so a regeneration is a
  signposted state rather than a surprise. THE REMAINING WORK IS ONE HUNK IN
  `core-port-test.cpp`.

  `PlayerClaims` cannot simply be answered instead: `ue-probe/.../Gossip.h`
  lists it under "OUT OF SCOPE AND NOT HERE", and porting it is queue 346's
  business, not this one's.
