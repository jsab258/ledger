line: engine and instruments (conversation pillar; gates the hardware floor)
spec: Jafar, 2026-09-21 ("THE MEASUREMENTS"): "Caching on, the cost per
  hour printed, then a small model behind the existing conversation
  interface, run against a set of cases and scored on a bar that counts a
  well-formed wrong answer as a failure rather than a pass. If the model
  has to run locally, dispatch it to the PC like any other machine job. It
  gates the hardware floor... Its size is the measurement ordered above,
  and no hardware floor is written before that number exists."

  WHY A WELL-FORMED WRONG ANSWER MUST FAIL: his ruling withdrawing the
  conversation pillar's old reasoning, same message: the constraint-tax
  paper "measures... that constraining output to a closed set takes schema
  validity to one hundred percent and answer accuracy from 19.7 down to
  11, with wrong-but-valid answers at 88.9 percent. A small model would
  confidently return well-formed wrong choices, which is the one failure
  the deterministic core cannot catch, since it checks that an output is
  in the set and not that it is the right member." A bar that only checks
  well-formedness would pass exactly the failure mode this test exists to
  catch.

  THE LIVE INTERFACE, confirmed present by grep at filing time:
  ledger/Assets/Scripts/Core/LlmClient.cs,
  ledger/Assets/Scripts/Game/ConversationHost.cs, and
  ledger/ConvoProbe/Program.cs. ConvoProbe/Program.cs carries no existing
  case set or scoring harness (grepped for case and eval at filing time,
  no hits), so the set of cases and the scoring bar are this item's to
  build, not to find.

  NO TIERING BY WHO SPEAKS: his ruling, same message: "No resident speaks
  through a worse model than another because of who they are... If
  tiering is needed, it follows the interaction rather than the person...
  Choose between those only when the small-model test and the cost per
  hour exist." So this test runs ONE small model against the interface as
  it exists for anyone, not a crowd-tier versus named-cast comparison.
acceptance: caching is on and stated as on, not inferred, for the run;
  cost per hour is printed as a number with what it is a statistic of
  (per-call, per-session or per-wall-hour, named); a small model is run
  behind LlmClient.cs and ConversationHost.cs with their public contract
  unchanged, dispatched to the PC if it cannot run in the container, with
  the dispatch route stated; a set of cases, its size stated, is scored on
  a bar where a well-formed-but-wrong answer scores FAIL, not PASS, and
  the bar's own logic is printed or quoted so a reader can check a
  wrong-but-valid case was actually scored a failure and not skipped; and
  the pass and fail counts are printed with their denominator (N of M
  cases), never a bare percentage
max_sessions: 2
status: READY 2026-09-21, filed with the visual slice's order. Runs in
  parallel with the slice, behind it on the runner per his ordering; may
  be picked up once a runner slot is free behind slice items 1 and 2. If
  the model must run locally, dispatch per the PC job route rather than
  waiting for a container capability that does not exist; if no PC
  dispatch route is free either, that is a blocker and the item returns to
  the queue with what was tried. This is this week's work.
