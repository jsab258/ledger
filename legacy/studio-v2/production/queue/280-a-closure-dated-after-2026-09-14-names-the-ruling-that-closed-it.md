line: instruments
spec: D32 catches an order that never became an item. It cannot catch the inverse,
  work that stops being work with no ruling, which is what happened to 182 items on
  2026-09-10 and to queue 115, a P1 canon item, among them.
acceptance: a CLOSED status dated after 2026-09-14 names its ruling record, the 182
  closed before that date are grandfathered BY DATE and the grandfathered count is
  printed, and the check lives inside tools/queue-check.py
max_sessions: 1
status: READY 2026-09-14, named by number in the ruling that shipped D32's checker,
  because leaving the rule's third reason unaddressed and unnamed is what would have
  made that checker dishonest.

  THE DIRECTION D32 CANNOT SEE. The marker check verifies that an order to the queue
  resolves to an item. It reads markers, not prose, and it says so on every run. But
  two of the three instances Jafar cited were orders that never landed, and the third
  was the opposite: 182 items that stopped being work under an archiving commit with
  no ruling naming what went with them. No marker can see that, because there is no
  order to mark.

  WHY GRANDFATHERING BY DATE AND NOT BY EXEMPTION LIST. The 182 are corrected in
  place to name cd55a79c and point at 275, but they were closed before this rule
  existed and requiring a ruling record for each retroactively would be a ratchet
  that punishes the correction. A date cut is legible, ages out on its own, and
  cannot be quietly widened the way a name list can. PRINT THE GRANDFATHERED COUNT so
  a zero is never mistaken for coverage.

  NO NEW INSTRUMENT. tools/queue-check.py already calls itself the one counter of the
  work queue and already walks queue, done and blocked. This is a check inside it.
