line: instruments
spec: The determinism failure was reported from ONE camera-condition pair with no
  denominator. The 2026-09-10 ruling ordered the full matrix printed with its count
  and no item was ever filed, so the order has sat unexecuted for four days.
acceptance: the full camera-by-condition matrix printed with its count, and the
  shape of the spread across pairs stated, so "every cross-frame number in that run
  is void" is either confirmed or corrected against a denominator
max_sessions: 1
status: READY 2026-09-14. THIS IS INSTANCE 2 OF THE THREE THAT CAUSED D32, and it
  is filed only because a checker was built to find it and could not.

  WHAT THE RULING ORDERED, verbatim in substance from
  game-design/decision-2026-09-10-ruling-the-exposure-ladder-and-the-sheet.md:
  "The reported evidence is rigMeanLumaFirst=0.6102 against rigMeanLumaRepeat=0.9562
  on ONE camera and ONE condition. Rule 3b: that finding has no denominator. How
  many camera-by-condition pairs were compared? If the answer is one, then every
  cross-frame number in that run is void is an inference from a sample of one, and
  it may be generous or it may be understating the damage."

  WHY IT STILL MATTERS AFTER THE LEAK FIX. The leak is fixed and proven
  (expPinRowsLeaked=0/of=6 on the run from 32bae70f). But the claim that the leak
  VOIDED EVERY CROSS-FRAME NUMBER in run 41 is still an inference from one pair.
  The matrix decides whether the damage was adaptation carry-over between
  conditions, which would show on the pairs that follow a different condition, or
  something worse and wider. That answer is worth having before any conclusion is
  drawn from a pre-fix run.

  WHY THE NEW GATE CANNOT CATCH THIS. tools/docs-check.py now verifies that a
  ruling ordering queue work names the item by number and that the item exists. The
  2026-09-10 ruling carries NO marker for this order, and a checker cannot conjure
  an item that was never filed. The builder used this exact case as its planted
  rejecting fixture: the failure text appears the moment somebody files the item and
  writes the marker. THAT IS WHY THIS ITEM EXISTS AND WHY THE MARKER FOLLOWS IT,
  rather than the other way round.

  THE DENOMINATOR TO PRINT, per the instrument rules: pairs compared out of pairs
  available, and the statistic named. A spread summarised by one number is the fault
  this item is about.
