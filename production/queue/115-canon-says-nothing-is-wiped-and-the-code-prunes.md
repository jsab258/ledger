line: simulation (Core, and canon)
spec: external audit 2026-09-06, P1. canon.md outranks every document and every agent, so this is a canon conflict rather than a bug report
acceptance: a stated ruling on which is true, the OTHER one changed to match, and the change recorded; if pruning stays, canon.md and every public claim about permanent memory change with it, and the claims are found by grep rather than by memory
max_sessions: 1
status: REOPENED 2026-09-14 by director ruling,
  game-design/decision-2026-09-14-ruling-the-marker-batch-lands-and-115-is-a-live-canon-violation.md.
  P1; MANDATORY DIRECTOR RULING stands and the ruling is Jafar's, pillar 1.

  A LIVE CANON VIOLATION: canon.md line 99 against MemoryStore.cs lines 62 to 97, in
  the tree since the 2026-07-27 audit the code's own comment cites; CoreTests
  Program.cs:1712 asserts the prune fires, so the violation sits inside a GREEN
  SUITE and the suite passing is not evidence against it.

  Was: CLOSED 2026-09-10 by cd55a79c with no ruling (see production/queue/275); the
  2026-09-14 closure audit wrote "not reopened" on it, which the ruling above
  reverses. That audit call was worse than the sweep it was correcting, because the
  sweep never claimed to have looked.

  THE LANDING OF THE 2026-09-14 BATCH IS NOT ACCEPTANCE OF THE PRUNE. Nothing in
  MemoryStore.cs, CoreTests 1706 to 1715 or canon.md 99 changes before he rules,
  INCLUDING no "disable the prune to be safe": disabling it is also a decision about
  pillar 1 and it is also his.

  Jafar put this on his own list on 2026-09-14: "Rule the memory prune against canon,
  open since 5 September: canon says nothing is ever wiped, MemoryStore prunes at 600
  events, one of them changes. Pillar 1 is the thing being decided, so this is a
  ruling and not a tidy-up." Quoted from the message as received; it is recorded
  nowhere else in the tree, and this line is that record.

## The conflict

`canon.md` says nothing is ever wiped. `MemoryStore` prunes at 600 events,
under a comment saying that is not forgetting.

Both cannot be true. A comment asserting that a prune is not forgetting is the
shape this project has a rule about: the code's own words are not evidence
about the code.

## Why this is P1 and not a tidy

PERMANENT MEMORY IS THE MOAT. The project's own framing is social memory at 93
against a best-in-class of 60, and consequence persistence at 95. If events are
pruned at 600, then the claim is bounded in a way no public statement about it
currently mentions, and every score resting on "nothing is ever wiped" rests on
something narrower.

## What a ruling has to decide, and it is not a preference

Which is TRUE, then change the other. The two honest outcomes:
- PRUNING IS WRONG: canon holds, the prune goes, and something has to answer
  what happens at scale instead. That answer must be measured, not asserted,
  and note queue 116: the soak that would be cited as evidence ran on seven
  agents.
- PRUNING IS RIGHT: canon changes, and so does every public claim about
  permanent memory. Find them by grep, not by memory, and print the count of
  files changed against the count that mentioned it.

## Both halves

Accepting: whichever way it goes, a test proves the behaviour the ruling
chose, and it fails if the other behaviour returns.
Rejecting: a state that satisfies neither, or a canon edit with no
corresponding code test, is the failure. A ruling that changes only the
comment has changed nothing.
