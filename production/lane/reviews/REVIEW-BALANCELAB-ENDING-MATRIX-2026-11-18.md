# Review: BalanceLab ending-matrix bullet (SKELETON-FIRST-OPTIONS-2026-11-18.md, "Open points", line 48)

Fresh reviewer, 18 Nov 2026. Checked against BALANCELAB-RUN-2026-11-18.txt (ending matrix and notes), BalanceLab/Program.cs RunEndingLab, Core/ActThree.cs, story-outline-2026-09-28.md, RULINGS.md.

**Verdict: PASS WITH FIXES**

Confirmed: Control 49.2% Straight / 50.8% Burn in all four rows; Aggressive Burn 69 to 100%, Kingdom 9.6% answered and 31.0% answered+deflect, 0% otherwise; Cautious Kingdom 82.2% max, 2.0% stonewalled; Both 5.1 to 12.7%, 12.7% only with deflection; Burn the most common result in 10 of 12 rows (not in Cautious answered or answered+deflect); Quiet needs HandedOver (ActThree.cs line 294) and the bot never hands over; meetings are chance-based (talk 0.10 an hour, witness 0.5); ActTwo.cs and ActThree.cs exist.

## Fixes

1. Wrong: "200 runs a policy". The matrix rows have n = 197: 200 seeds a plan, of which 3 never reach the open city (reach 98.5%). Correct to "200 runs a plan, 197 of which reach Act III".
2. Wrong: "about 9 seconds". The run file records no time. Add the timing to the run file, or mark it "(timed by hand, not in the file)".
3. Wrong: "rare enough for his July ruling", with RULINGS.md implied as its home. RULINGS.md has no line for it. The ruling appears only in story-outline-2026-09-28.md: Both is "rare, and by the July ruling not meant to be reached on a first playthrough (aimed at by the balance, not enforced)". Cite the outline. Also say that a cautious first-time player gets Both 5.6% of the time even without the deflection.
4. Missing: the outline says Burn Both is "what doing nothing produces", but the passive plan gets Straight Life 49% of the time. Name this conflict in the Burn Both question, because it is a mismatch between the design text and the code, not only a balance question.

Rounding Aggressive Kingdom 9.6% to "10" is acceptable.
