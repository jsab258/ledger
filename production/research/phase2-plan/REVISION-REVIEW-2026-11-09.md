# Fresh review of the 9 Nov revision of PIECES-DRAFT-2026-11-08.md (9 November 2026)

One fresh reviewer. Read 9 Nov 2026: the draft in full, git's previous version (HEAD) beside it, FOR-ORDER-16-NOV-2026-11-09.md, SCOREBOARD-2026-11-08.md §4, PS5-GAP-LIST-2026-11-08.md, progress.json, and each source the revision newly cites (orders/2026-11-09.md line 24, EXIT-D-REVIEW and EXIT-A-REVIEW of 9 Nov, RECS-BY-PHASE line 62, MEMORY-PLAN §2 and §5, studies/04 line 57, aaa-street SUMMARY lines 39 to 48 and 96, asset-plan 1-BUILDINGS line 61, QUAY-END-DIAGNOSIS §1, the street-weathering skill line 15, tools/order_ledger.py). Sums re-done by hand. Nothing outside the repository was read; nothing unreached.

**Verdict: pass with fixes.**

## What holds

- Every new hour figure reproduces. The 8 Nov rows sum to 239.8 to 383.6 h without cars (stated 240 to 385). Pieces 1 and 2 add 26 to 52 h (16 to 32 plus 10 to 20). Plan figures 266 to 437 h, with cars 316 to 527 h. Guesses at twice: 395 + 52 = 447 and 660 + 104 = 764 h; with cars (50 to 90 h doubled) 547 to 944 h. People rows 78.3 to 100.6 h (stated 78 to 101).
- Every weeks figure reproduces at 57 h: 4.67 to 7.67, 5.54 to 9.25, 7.84 to 13.40, 9.60 to 16.56, 6.93 to 11.58.
- SCOREBOARD §4: 53.53 production, 3.49 review, 57.03 total, as cited. progress.json line 131 is planned_w 3.0 to 4.0, as cited.
- No double count: n09-3's 14 h stays once (in Budget and exit), and the scale test is added on top. P20's 3 to 5 h stays once in the Light rows.
- The newly cited sources say what the draft says they say: 0.21 and 0.19 ms; 6,145 and 6,151 MB; n09-3 14 h; scale test 2 to 4 days, may grow; World Partition unsized; RECS line 62 has no values; 48 m street; the blockout step; the camera in the office's walls; chart before wear.
- Nothing from the 8 Nov piece list was dropped. P20 and the checks were moved, and each move is marked. Every 8 Nov order step has a new place, except the one in fix 10.
- Pieces 1 and 2 each name a reference (Kingdom Come II's scale test; Mafia's greybox step). The second is weak (fix 7).

## Fixes

1. **The order breaks its own rule at step 3.** §3 says it follows the PS5 gap list's ranking: street life 1, distance 2, people 3, buildings 4, night 5, daylight 6. Shells (buildings, rank 4) come at step 3, ahead of street life and distance, and no reason is given. Either state the exception in §3 (for example, wear goes on once after P20, and the corner's copy is the scale test's unit), or move shells after step 5. P20 (daylight, rank 6) also comes early, in piece 2. The reason for that is given only in §1 (the chart before base colour and wear), so repeat it in §3.
2. **The first paragraph of §2 is stale.** "Its low end only meets it" and "About 155 to 280 h are guesses" describe the 8 Nov list. The revised list's low end, 266 h, is above the roughly 240 h ceiling, and its guesses are now about 181 to 332 h. Label that paragraph as the 8 Nov list, or restate it. The old "4 to 7 weeks" and "5 to 8.5 weeks" were removed without a line saying what replaced them.
3. **The totals leave out two pieces without saying so.** Distance beyond the crowns and the crowd beyond the named people are unpriced and not in the total (§1). Add a line under §2's table saying that every range there excludes them.
4. **"The likeliest range" is too strong.** The records run 2 to 4 times plan figures, so "at twice" is the records' low end, not the likeliest point. Reword, or add a line at three or four times.
5. **Name the pace basis.** 57.03 h includes 3.49 h of review. At production hours alone (53.53 h), the main row is 8.4 to 14.3 weeks. Say which hours the plan's figures are measured against.
6. **Piece 2 has no check.** "Walked at the three views" sets no pass mark, and §4 has no weekly line for piece 2. Add a done line, for example: walkers complete each route end to end, no frame has the camera inside a wall in a free walk at the three views, and the crowd count stands within piece 1's budget. Add the matching §4 line.
7. **Piece 2's reference rests on search snippets.** aaa-street SUMMARY marks Mafia's "greyboxes, then hero buildings" [SS], and no study under aaa-reference/studies mentions a greybox (searched 9 Nov). Under the research rule a snippet is not evidence. Write "Reference: none found" for piece 2, giving Mafia's step as an unverified lead, or read a primary source. When pieces go into an order, tools/order_ledger.py needs the words "Reference:" (a Mafia or Kingdom Come II method, or "none found"). The many "None." rows must be carried over in that form.
8. **Say whether the checks are inside the greybox's hours.** The width and street-end checks (3 to 5 h) are "done inside" piece 2 but still priced separately. Say that the greybox's 10 to 20 h excludes them, or merge the two figures.
9. **Piece 1 should name its precondition.** MEMORY-PLAN §5 step 3 requires a DECISIONS.md entry, made against "nothing is multiplied", before the scale test's switch is built. Today that is only in FOR-ORDER item 8. Add one clause to piece 1.
10. **The kit-reuse check has lost its place in the order.** The kit-reuse check (s04-04) was in the 8 Nov order's step 2 with the other checks. In the revision only width and the street's ends move into piece 2, and s04-04 has no step. Place it, for example with shells at step 3.
11. **Two stale lines from before the revision.** "The 2027 line already reads 2.2 weeks behind" is now 2.4 (progress.json line2027.behind_w, as of 9 Nov). Question 1 (the fishmonger and the empty unit) is settled: RULINGS line 17 says "8 Nov: the fishmonger and the empty unit to let are built in phase 2", and progress.json says "your yes, 8 Nov". Remove the question, and the fronts row's "Question 1".
12. **The progress page now disagrees with the draft beyond planned_w.** progress.json's plan_note (240 to 385 h) and its piece order are the 8 Nov list's. FOR-ORDER item 3 names only planned_w. Add the hours and the order there.
13. **The word note is stale.** The 8 Nov fixes note says the body is under 1,300 words. The body above the review now counts about 2,380 words (wc), and HEAD's about 1,390. Correct the note, or shorten the body.
