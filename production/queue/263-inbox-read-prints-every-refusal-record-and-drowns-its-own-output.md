# 263: inbox-read prints every refusal record and drowns its own output

STATUS: READY
OPENED: 2026-09-11

## The fault, measured

`python3 tools/inbox-read.py` on 2026-09-11 printed 545 outbound record lines.
494 of them, 90.6 percent, were refusal records for ONE file:

    refusal records for 2026-09-03-batch-landed-and-the-wait   494
    total outbound records                                     545
    every other record                                          51

Each refusal prints its whole clause list, about 300 characters, so the run's
actual findings sit under roughly 150,000 characters of repetition. The two
lines a reader needs (`inbox-read done: seen=2 delivered=0/2` and the count of
untracked records) are the first and last of the run, with the flood between.

THE FILE IS NOT LOOPING AND THAT IS THE POINT. It was removed from
`production/outbox/` at `7741eecd` on 2026-09-09, so nothing is retrying; these
are historical records being re-listed in full on every run, for ever, and the
set only grows. A reader who assumed a live loop (as this session first did)
would be diagnosing a fault that ended two days ago.

## Why this is an instrument fault and not cosmetics

`.claude/rules/instruments.md`: "Every cap announces itself: `(+N more not
shown)`." The tool already HAS a cap and a selftest for it,
`accept/the-print-cap-announces-itself` at `tools/inbox-read.py:504`, and
`cap()` at line 201. That cap governs the MESSAGE TEXT. Nothing caps the
per-record listing, which is the half that actually floods.

CLAUDE.md rule 12 is the reason this ranks: the inbox reading is one of the two
jobs the hourly trigger exists to do, and its output is currently unreadable
without filtering it by hand.

## Done looks like

1. The per-record listing is capped, and the cap ANNOUNCES ITSELF with the
   count it withheld and what it withheld, in the existing idiom.
2. Refusals are summarised rather than enumerated when they repeat: one line
   per distinct file naming the count and the clause set, so
   `refused=494 of 1 file(s)` reads as what it is.
3. The cap is driven BOTH ways in the selftest, accepting case first: a run
   under the cap prints every line and says so, a run over it prints the
   withheld count. The existing cap fixture is the pattern to copy.
4. `refused=` on the done line keeps its denominator, which it already has.

## What this does not cover

Retiring the historical records themselves. They are evidence and are not
deleted by this item; it changes only how they are PRINTED.
