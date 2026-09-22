line: sim (ledger/Assets/Scripts/Core/ActThree.cs; the endings' eligibility rule)
spec: Jafar, 2026-09-21 (second message, "What is checkpoint work NOW"):
  "Confirm that the two endings left to a hunted player, keeping
  everything with nobody who knew you before and giving up the business to
  keep the people, are reachable FROM A HUNTED STATE. The audit read only
  the first gate of the eligibility rule and says it is one method away
  from certain. IF EITHER IS UNREACHABLE THAT IS THE FAULT AND IT GOES TO
  HIM AS A CARD."

  READ IN FULL AT FILING TIME, ledger/Assets/Scripts/Core/ActThree.cs. The
  two endings are Kingdom, "You kept everything you built, and nobody is
  left who knew you before it" (lines 36-37), and StraightLife, "You gave
  up the business to keep the people" (line 39). Eligible(LedgerState s)
  (line 267) gates them:

      line 287: Quiet needs s.HandedOver && s.HasReadySuccessor && !s.Hunted
      line 345: StraightLife needs !empireSurvives && lifeSurvives
      line 358: Kingdom needs empireSurvives && booksHold

  NEITHER Kingdom's NOR StraightLife's own condition mentions s.Hunted at
  all. s.Hunted is checked ONLY in Quiet's gate, line 287, which is
  textually the FIRST of the four if-statements in Eligible and is very
  likely "the first gate" the audit read. THE ONLY EXISTING TEST that
  exercises Hunted, ledger/CoreTests/Program.cs around lines 11554-11560,
  also only checks it against Quiet: it asserts Quiet is eligible when
  handed over, then sets Hunted = true and asserts Quiet is NOT eligible.
  No existing test constructs a Hunted state and checks Kingdom or
  StraightLife.

  So a formula not mentioning Hunted is necessary but not sufficient for
  "reachable": the open question is whether becoming Hunted has any
  coupled side effect elsewhere that makes empireSurvives && booksHold, or
  !empireSurvives && lifeSurvives, unreachable in practice even though the
  boolean formula admits them. Hunted is set at exactly one live call
  site, ledger/Assets/Scripts/Game/ActThreeHost.cs:46, Hunted =
  Police.BarsQuietExit(PoliceInquiry); trace what PoliceInquiry and
  Police.BarsQuietExit depend on, and whether reaching that state forces
  any other LedgerState field, BusinessesOwned, RacketsEstablished,
  EmpireDissolved, BestDayLifeLoyalty, the strain fields behind
  booksHold, away from what each ending needs.
acceptance: two new CoreTests, or one test with two checks clearly
  labelled, construct a LedgerState with Hunted = true plus Kingdom's own
  gate conditions satisfied, and separately with Hunted = true plus
  StraightLife's own gate conditions satisfied, and assert
  ActThreeState.Eligible(s) contains each ending; `dotnet run -c Release
  --project CoreTests` is run and its full count reported, matching
  ledger/verify.py's own "N CoreTests" parsing, with the new checks
  included in that count; and every call site that sets Hunted, grepped,
  count stated, is checked for a coupled side effect that would make
  either ending's OTHER conditions unreachable in real play, with the
  finding stated either way. IF EITHER ENDING IS FOUND UNREACHABLE from a
  real Hunted state, by the test or by a traced coupling, this item's own
  status is changed to name that as a fault and a card is written for
  Jafar per his own instruction, rather than the item being closed as
  passing.
max_sessions: 1
status: READY 2026-09-21, CHECKPOINT WORK NOW per his explicit marking.
  MAY START THIS WEEK, one of the two exceptions his second message
  names.

  RULED BY: `ledger-v2/respec/decision-register/D58-the-endings-hold-five-no-redemption-path-two-conditions.md`, condition 1, which names THIS item. Jafar 2026-09-21: "confirm that the two endings left to a hunted player ... are actually reachable from a hunted state", and "If either is unreachable, that is the fault, and it comes to me as a card." CHECKPOINT WORK NOW, one of exactly two he marked so.
