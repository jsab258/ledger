# 258. Recover the return half from the archive's pc-inbox

STATUS: READY, 2026-09-10, after queue 257. Ruled by
`game-design/decision-2026-09-10-ruling-the-move-batch-and-the-fleet-left-behind.md`
section 5, finding 7.

## What is wrong

The old fleet still pushes the return half (delivery receipts, inbound
messages, brief taps) to the ARCHIVE's `pc-inbox`. Measured tonight: the
archive's `pc-inbox` is at 2ca5cc39, ahead of this repository's 2a7a234c, with
two delivery receipts landing at 18:55:55Z. Repointing the daemons stops the
bleeding once the fleet moves and recovers nothing: every tool here that reads
receipts and taps (`tools/inbox-read.py`, `tools/producer-day.py --streak`)
reads `ledger`'s `pc-inbox` and will never see them. The channel's only
measure, seven consecutive readable briefs tapped by him, is counted off
those files. `pc-results` may carry the same shape of loss if any job ran on
the old fleet since the move; measure it, do not assume either way.

## The deliverable

One session, read-only against the archive, write-only against `ledger`:

1. Order: after queue 257 has stopped the old fleet, or the archive branch is
   a moving target and the recovery is stale the moment it lands.
2. Fetch the archive's `pc-inbox` and `pc-results` tips by URL (never by a
   remote named `origin`, never with a push), print both shas and both of
   ours, and print `merge-base --is-ancestor` for each pair. Our
   `pc-inbox` may already carry the new fleet's first pushes by then.
3. Fast-forward only if ancestry says so. Otherwise merge, never force: a
   force push over `ledger`'s `pc-inbox` would discard exactly the first
   receipts the new fleet delivered. `inbox.py` pushes with plumbing and
   `--force` from the PC side, so the recovery lands BEFORE the new fleet's
   first push where possible, and as a merge where not.
4. Print the count of recovered files by kind (receipts, inbound messages,
   taps) with the denominator of files examined on the archive branch, and
   `production/producer-day.py --streak` before and after so the measure
   moves for a reason that is on the page.

## What it must not assume

That the studio may write to the archive (it never does, not even a tag);
that the session's GitHub access reaches the archive at all (measure with one
`ls-remote` and say "nothing measured" if refused); that the two branches are
fast-forwards of each other; that the archive has stopped moving; that the
recovered receipts are for messages the new repository sent (they are for
messages the OLD fleet sent from the frozen checkout, and the caption of each
says which).

## Done looks like

`ledger`'s `pc-inbox` contains 2ca5cc39 or a merge of it, the counts printed,
the streak reading explained, and the same measurement for `pc-results`
printing either the recovered job outputs or `pc-results=nothing-to-recover
archiveTip=<sha> oursContainsIt=true`.

## Dependencies and risk

Queue 257. Risk: recovering into a branch the new fleet is writing to; step 3
is the guard.
