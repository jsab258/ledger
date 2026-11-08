# Review: legs that never arrived (commit 276d2f423), 8 Nov 2026

Verdict: PASS WITH FIXES (no code fault; the commit message and session claims are wrong in their numbers and must be corrected before they are relied on).

## 1. Code against spec
tools/route_walk.py stuck_runs (line 345) matches Step 1: run = consecutive same "to"; end = next entry's "at"; last run goes to end_unread and never fires; min_legs 6, tol 0.5, strict ">". Empty or None path returns a "no path" note. nightly_walk.legs_never_arrived (line 140) handles no walk, and older verdicts with no "stuck" by calling stuck_runs on the path. Nothing contradicts the spec.

Minor, not blocking:
- route_walk.py:~360: an entry missing "to" or "at" is read as [0,0], which could fire a false alarm. The real files never lack them.
- Two separate go_to calls in a row with the same target (by_road's road leg, then the final leg, when z equals ROAD_Z 1.2) merge into one run. A run of 6 or more could be two short calls. No false fire was seen from this.

## 2. Real nights (F:/LedgerTools/nightly, 23 verdicts, read-only)
- 3 verdicts have an empty path (10-07, 10-31, 11-03), so 20 have a path, not 21.
- No kept verdict carries "stuck"; every night was computed from its path.
- Fires on 16 of 20 nights (not 18 of 21). No fire: 10-04, 10-05, 10-06, 10-26.
- Sheila's spot (7.9, 4.6) is missed by 1.31 m on 10-29, 11-01, 11-02, 11-04 and 11-07 (5 nights), and 1.44 m on 10-24. That is 6 of the 13 nights with a path since 24 Oct, so "every morning since 24 Oct" is wrong. On 10-26 and 11-06 he arrived (at 7.85, 4.61 and 7.75, 4.56). 10-28, 10-30 and 11-05 show no fire at that spot. The 1.31 figure is exact on all five nights.
- Hand check 11-07: run is entries 5 to 18 (14 legs to 7.9, 4.6); entry 19 "at" is (8.45, 3.41); hypot(0.55, 1.19) = 1.31. Correct.
- Hand check 11-06: entries 54 to 67 are 14 legs to (7.96, 4.31). The "at" values bounce between (8.45, 3.41) and (8.0 to 8.3, 2.3 to 2.5), and entry 68 reads (9.89, 2.5), 2.65 m off. A true non-arrival. The 7.9, 4.6 run that morning was only 10 legs and arrived, so correctly silent.
- 11-08 has 4 fires, of 4.3 to 7.0 m, all with a flat "at" (jump 0 to 0.4 m), so he did not move. These are true. 10-27 has 9 fires of 0.7 to 1.2 m with about 1.8 m jumps (overshoot oscillation), real but not a wall.

## 3. False positives and negatives
- No false positive found among the 16 fire nights: every fire has its last leg's "at" over go_to's tol from the target, so none arrived.
- Gap: the run's end is the next entry's "at", which may include movement made between go_to calls (sit, talk). Seen as a jump of 1 to 4 m on 10-21, 10-22, 10-23, 10-27 and 11-05, where the next "at" is further from or closer to the target than the last leg's "at". It cannot be told apart from a last leg that overshot. The fire is still right in each case, because the last read of every run was already over the tolerance.
- False negatives: none found. Every go_to cap is at least 6, so a stuck run always reaches min_legs.

## Fix asked
Correct the commit/DECISIONS/RECIPE wording to "16 of 20 nights" and "6 of the 13 mornings since 24 Oct" (five at 1.31 m, one at 1.44 m).
