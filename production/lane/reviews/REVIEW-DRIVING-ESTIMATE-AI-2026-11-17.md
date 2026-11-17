# Review: driving estimate for an AI builder (17 Nov 2026)

Fresh, hostile reviewer, about 12 minutes. Reviewed DRIVING-ESTIMATE-AI-2026-11-17.md and the three changed lines in TRAFFIC-COST-2026-11-17.md. Estimate not edited.

## Verdict: PASS WITH FIXES

The method is sound and the recommendation (route B, the hybrid, guarded by a short trial on the PC) follows from the evidence. The measured rates are real. But two totals do not add up, one comparison is wrong, and stage 3 leaves out night and wet-road visuals and lumps police chases into one line.

## What was checked

- Measured rates against the time log (recomputed today): 395 windows, 240.5 h, 28 days: matches. Sit and seat: 20 windows, 13.4 h, median 0.57 (file says 19, 12.4, 0.55: close, depends on the word match). Talk camera 8 windows, 5.1 h: matches. Epic's walk route 24 Oct, 3.9 h: matches. Kiln rounds 0.72 to 1.70 h, median about 0.92: matches once the short non-round windows are left out. Phase 3 port windows: 0.05 to 0.32 h with a narrow match (file says 0.07 to 0.80, 15 windows): plausible with a wider match, not exact.
- RECIPE.md: section 8 "1 to 3.5 h a try", section 10 "0.25 to 1 h a rule; 0 mismatches", section 11 "4 to 12.5 h", section 12 "0.1 to 0.6 h a fix": all match.
- DECISIONS.md: parked car 25 to 41 h against 12 (16:24, 17 Nov), garments 17 to 21 against 10, scale-test core 14 against 8, Kiln M5 41.5 counted against 46: all present.
- Sums: stage 2 rows give 96 to 203: matches. Stage 2 and stage 3 human ceilings: match. Stage 3 rows: see fix 1.
- Web spot-checks (read 17 Nov 2026): Cyberpunk 2.0 notes say "All engines have torque curves now", "New speed-sensitive steering", "how we apply gravity as the suspension moves" [READ, Shacknews copy of the notes]. Epic's Assetto Corsa Competizione interview says "It also paired very well with our proprietary physics engine" [READ]. Both supported.
- No em-dashes, no italics, in the estimate or the changed lines. Plain words, mostly.

## Fixes

1. Stage 3 total is wrong. The rows with the shared shell add to 367 to 774, not 367 to 824. With four full interiors they add to 382 to 824. Change the total row to "367 to 774 (shared shell); 382 to 824 (four full interiors)" and keep the stated 400 to 900 only if fix 4 adds hours; otherwise state 370 to 830.
2. The lean stage 2 does not add up. Swapping getting in and out (20 to 40) for the cut (8 to 15) gives 84 to 178, not 70 to 130 (section 6 itself says it saves 12 to 25 h). Change "70 to 130" to "85 to 180" in the Summary, section 3 and TRAFFIC-COST line 13. Drop "cosmetic damage only" from the lean version: full stage 2 is already cosmetic damage only.
3. Summary, stage 3 comparison: 600 against 1,750 is about a third, not "about a quarter". Change to "about a third".
4. Stage 3 misses night and wet-road visuals. Add a row "Lights and weather on the player's car": working headlamps that light the road at night within the 1.4 ms night spare (TRAFFIC-COST bans shadow-casting headlamps, so say how the player's lamps light the road), brake and indicator lamps, police car lamps and siren, wet road spray and splash, rain on the windscreen and wipers, rear-view and wing mirrors. Est. and human ceiling to be given; carry it into the total.
5. Split "Traffic interplay" in stage 3 into two rows: "AI drivers who react" and "Police chases" (search pattern, roadblocks, losing the police, the town's simulation knowing the chase). One 60 to 120 line against a 3,000 to 6,000 ceiling is a ratio of 50, double any other row, which hides the second biggest item. Give each its own range and mark both [I].
6. Add pedestrians reacting to cars (stepping back, jumping clear, shouting) to stage 3, or name it as left out next to assumption 8. Hitting people is his canon question; people getting out of the way is not.
7. Section 2, the time-log line: 240.5 h is the whole log; the production kind alone is 224.9 h over 358 windows. Change "240.5 logged hours of the production session" to "240.5 logged hours, all kinds".
8. Section 2, the overrun line: Kiln M5 "41.5 against 46" is not an overrun (41.5 is under 46). Move it to the sentence about counted items landing near their count, or drop it.
9. State in the Summary that the old 1,000 to 2,500 did not say "on top of stage 2". Add: "If the old figure meant the whole job, the fair comparison is stage 2 plus stage 3: est. 500 to 1,120, still about half the old range."
10. TRAFFIC-COST lines 10, 53 and 85 still say Chaos Vehicles (or Modular Vehicles) carries stage 2 and the choice is made at stage 2's start. Add one line under the Summary: "Stage 2 route now recommended: the hybrid (DRIVING-ESTIMATE section 1); the kit's wheel bones still serve the wheel visuals." The table heading "ROUGH hours" (line 131) should read "Est. hours" for the two changed rows.
11. Section 6, "Procedural engine sound ... sidesteps the CC0-only sound rule": say instead that it needs no recordings, so the CC0-only rule is met by having nothing to license. "Sidesteps" reads as getting around a rule.
