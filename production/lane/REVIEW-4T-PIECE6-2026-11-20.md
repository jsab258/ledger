# Review of 4t piece 6, the panel on recordings (20 Nov 2026)

Reviewer: one fresh helper, Opus at high effort, 20 Nov about 04:24 Swiss time, read only, no web. Files: tools/lane/prototype/reviewers/panel/ (panel.py, PANEL-PROMPT.md, ANCHORS.md), tests/test_panel.py, production/research/lane/PANEL-ON-RECORDINGS-2026-11-20.md, and the word-reading fix in tools/lane/gate/clumsy.py and players/play.py.

Verdict: PASS WITH FIXES. All tests passed; judges never see hidden state or the player's words.

## Must fix (all done once)
1. A pair leaked which version was which through the packet's label. Fixed: each copy's label becomes "version A" or "version B" everywhere; a test checks that no label word survives.
2. Single sessions were pooled into one table. Fixed: one table per session; dead stretches matched only within a session.
3. Pairs promised a winner per axis but never counted one. Fixed: each axis counted in both orders, ties when it flips.
4. Nothing named the pair for the judge. Fixed: PAIR.md carries "Pair: <name>/<order>", which the answer copies.
5. No code built the swapped order, and the judge was told it was swapped. Fixed: pair writes order1/ and order2/ itself, the key says which letter is the later version in each, and the judge is never told.
6. A wrong output folder would have been deleted. Fixed: the tool clears only an empty folder or one it made (its marker file); a test checks a foreign folder is kept.

## Should fix
Done: the strip's last frame always kept within 48; the 15 to 20 seconds figure now said to be our choice, with the real spacing past 12 minutes; overlapping dead stretches merged; true/false never counted as a score; half-typed talk counted once when picking clips; log lines kept to 600 characters; the note for piece 8 that clips partly follow the player's own best and worst minutes. Also softened: no source measures how well models judge pace or taste, so the prompt and the note no longer claim it.
Left open: a short line that begins a longer earlier one is not charged reading time in play.py (minor); boxes faded to invisible still count as shown.

## Found while building (fixed in the same step)
The words reader used by the clumsy newcomer, the machine checks, the AI players and the consequence checker never read the written scene's box (#dialog is a fixed box, so the old "is it on screen" test always said no). Every scene line was missing from the players' screen words, their reading time and the consequence checker's spoken lines until now. Machine, consequence, breaker and gate tests still pass; a fresh short session now reads Ron's lines and the consequence checker shows 0 faults on it.
