line: instrument (a selftest nothing runs)
spec: tools/runner/cards.py --selftest has been failing since 2026-09-10 and
  nothing notices, because verify.py does not run it. The failing case asserts
  a heading that was DELIBERATELY RETIRED on the same day, so the fixture is
  stale and the file is right. Re-point the fixture at what the file now does,
  and decide whether this selftest joins the gate.
acceptance: cards.py --selftest at 72 of 72, and a stated decision on whether
  verify.py runs it. Both outcomes on the re-pointed case, accepting first: a
  decision-queue that carries whatever shape the fixture now asserts passes,
  and one that does not fails. If the answer is that it should NOT join the
  gate, that is a legitimate answer and it is written down with the reason,
  because an untested guard nobody runs is the thing this item is about.
max_sessions: 1
status: READY 2026-09-15. Found while checking a builder's claim rather than
  while looking for it, which is worth saying: the builder reported the failure
  as pre-existing and outside its work, and the check that confirmed it is what
  turned it up.

  PROVEN PRE-EXISTING, NOT INHERITED FROM THE BATCH IN FLIGHT. Run at HEAD in a
  detached worktree and on the dirty tree in the same minute: both read
  "cards selftest: 71 passed, 1 failed (72 case(s) run)". Identical. So it is
  not the site-link move and not the grade.

  THE FAILING CASE: accept/the-live-queue-has-a-ruled-this-week-section, which
  asserts production/decision-queue.md carries a RULED THIS WEEK heading.

  AND THE FILE IS RIGHT WHILE THE FIXTURE IS WRONG. decision-queue.md:168 says
  in its own words: "The heading `RULED THIS WEEK` is retired: a card that is
  ruled leaves this file." That retirement landed in cd55a79c on 2026-09-10.
  So an ACCEPTING fixture has been asserting the presence of a heading the
  project deliberately removed, for five days.

  WHY NOBODY SAW IT, AND THAT IS THE REAL FINDING. verify.py runs a long list
  of tool selftests by name (inbox, inbox-read, bot config, outbox, supervise,
  executor, wake queue, checkout gate, brief, producer day, budget log, and
  more). CARDS IS NOT ON IT. So cards.py's selftest is a guard that runs only
  when somebody types it, and nobody had typed it since the retirement. A
  selftest outside the gate is a selftest that reports to nobody.

  WHAT THIS ITEM IS NOT. It is not a licence to delete the case. The case
  exists to prove the live decision queue has the shape the card writer
  expects, and that is worth keeping; what it asserts has simply gone stale. Do
  not answer a stale accepting fixture by removing it, which is the reflex this
  project keeps having to correct.

  A QUESTION THE TAKER MUST ANSWER RATHER THAN ASSUME: how many OTHER tool
  selftests are outside verify's list. The list above is what verify names;
  nobody has counted it against the tools that HAVE a --selftest. That count,
  with its denominator, is the thing that says whether this is one stale
  fixture or a class.
