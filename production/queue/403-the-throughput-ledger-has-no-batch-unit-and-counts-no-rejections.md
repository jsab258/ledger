line: instruments (production/throughput.md, the measurement of the art pipeline)
spec: Jafar, 2026-09-21: "Before the window opens: queue 370's column is in
  place, and the throughput ledger takes a batch as its unit and counts
  rejected attempts, since the industry research found nobody measures
  rework and ours would be the instrument that does. Read both meters
  before and after." This is the second of the two preconditions his order
  names for queue 389 (the first authored facade); queue 370 is the first
  and is already filed and not this item's to rewrite.

  WHAT THE LEDGER MEASURES TODAY, read at production/throughput.md: three
  rows, each keyed to a named piece or package (pub-regular-v1,
  brand-bible-v1, A7_gully_grate, C15_fascia_cornice_console). Its own
  rule: "A piece counts when it passes station 3 (VERIFY) and lands at
  station 4 (INTEGRATE). Partial work counts zero." There is no BATCH row
  shape and no field anywhere in the file for an attempt that was
  REJECTED: today a facade that fails review leaves no mark on this ledger
  at all, which is the gap his instruction names.

  THE DELIVERABLE IS THE UNIT, NOT THE FIRST READING. Add to
  production/throughput.md: what a BATCH is for the facade line (the unit
  of work one authoring attempt produces), stated the way the existing "a
  piece counts when..." sentence states the piece unit; a field or row
  shape that records a REJECTED attempt as a count rather than as silence,
  so a batch that fails still leaves a mark on the ledger it failed
  against; and the BEFORE reading that queue 389 will need, taken now so
  there is a baseline to compare after. Follow the file's own existing
  discipline: a session denominator from agent-log rows, a runner-time
  denominator where measured, and UNDEFINED stated plainly where a
  denominator is zero, never a false zero (the file already does this for
  cost per verified piece, "the denominator is zero verified pieces, and a
  cost divided by no pieces is not a number").

  Do not author a facade here. That is queue 389, which reads this file
  before and after and is blocked until this item lands.
acceptance: production/throughput.md defines a batch unit for the facade
  line in the same style as its existing piece-unit sentence (quoted
  above); it names what makes an attempt REJECTED versus VERIFIED and
  carries a place to record a rejected count that is not silence; the file
  stays internally consistent, the new unit extends the ledger to a second
  unit rather than contradicting "partial work counts zero" for the piece
  unit; and the BEFORE reading queue 389 will quote is present in the file
  at the moment this item closes
max_sessions: 1
status: LANDED 2026-09-21 by the instrument line, uncommitted at the time of
  writing (the director commits). WHAT LANDED, three files:
  production/throughput.md gains the BATCH section (the unit sentence, the
  REJECTED sentence, the block shape, the five batch blocks and the BEFORE
  reading for the terrace front); tools/throughput-check.py is the checker and
  the series printer, 23 selftest checks, accepting case first and the
  accepting fixture is the live ledger; ledger/verify.py gains
  `throughput_batches` so the guard runs before every commit rather than in a
  workflow nobody dispatches, which is queue 416's fault class avoided.

  THE FIRST SERIES, printed rather than promised: batchesWalked=5
  batchesPriced=0/of=5 batchesCountingRejections=1/of=5
  deliverableListsFixedAtOpen=2/of=5. Four batches predate the field and read
  `nothing-measured` rather than a retrospective zero. NO BOUND IS SET: the
  printer ships first.

  TWO PLACES THE SPEC IS STALE OR WRONG, named rather than quietly worked
  around. (1) It says the batch is "the unit of work one authoring attempt
  produces". Built deliberately otherwise: a batch is the commission whose
  deliverable list is fixed at station 1, and attempts live INSIDE it. If one
  attempt were one batch, a rejected attempt would be its own batch and no row
  could ever carry the rework, which is the opposite of queue 369's "price a
  batch, end to end, including work that was rejected". (2) It names queue 389
  as the consumer of the BEFORE reading; 389 was SUPERSEDED the same evening,
  first by the kit-first ruling and then by
  game-design/decision-2026-09-21-ruling-the-terrace-fronts-are-authored-and-everything-else-comes-from-what-we-hold.md.
  The BEFORE reading is therefore opened as b005-terrace-front-01 for the
  terrace front, which is what he kept: "both meters read before and after,
  the BATCH as the throughput ledger's unit, and REJECTED ATTEMPTS COUNTED".

  Was: READY 2026-09-21, filed with the visual slice's order. BLOCKS
  queue 389 (the facade), which may not start authoring until this item
  lands; queue 389's own status line says so. Does not block on anything
  itself and may start this week.
