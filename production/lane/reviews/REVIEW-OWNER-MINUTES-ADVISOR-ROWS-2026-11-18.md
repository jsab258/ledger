Verdict: PASS WITH FIXES

Fresh review, 18 Nov, of the two passages added today to production/lane/OWNER-MINUTES-MEASURE-2026-11-18.md: the paragraph starting "Measured 18 Nov 09:45" and the line starting "With the advisor rows measured (18 Nov)". Recounted independently in Python from the 212 advisor rows in the lane's scratch copy (numbered row = id ending in -number; date from "at"; words = text split on whitespace; his_answer non-empty after trimming).

Recount, all matching the paper:
- 9 to 15 Nov: 129 numbered rows, ids 41 to 169 with no gaps or repeats, 30,469 words, 30 with his_answer.
- 16 to 18 Nov (last at 08:20): 49 numbered rows, 170 to 218, 12,966 words, 46 with his_answer.
- Every file's date agrees with its "at"; every numbered row has from = advisor.
- Arithmetic: 129 x 2 = 258; 30,469 / 200 = 152.3, so "about 152" is right; 30 x 2 = 60; 46 x 2 = 92.
- Plain words: no em-dashes, no italics.

Findings

1. The range is exact, so "about" misleads. Replace "(about 41 to 169)" with "(41 to 169)".

2. The list of unnumbered rows leaves out one kind: the rows also include "eff-missing". Replace "(night, pace, eff, quiet, model, reset, backstop)" with "(night, pace, eff, eff-missing, quiet, model, reset, backstop)".

3. Fairness: the first reading is labelled an upper bound but the recommended third is not labelled at all, and it is a floor (it gives nothing for reading the advisor's replies, or for rows he read and did not answer). After "only rows carrying his words at 2 minutes each, 60 minutes" add ": a lower bound, since reading the replies is not counted". The recommendation's reason stands: his_answer is the only field that proves he spent the time, and the floor is the honest number to show beside a "shown, not judged" figure.

4. The earlier paragraph now contradicts the measurement (it gives rows "from about 75 to about 177, roughly 100 a week, over three hours"). At the end of that paragraph add: "Superseded by the measurement below: last week held 129 numbered rows (41 to 169)."

5. Fit with tools/lane/owner_minutes.py: owner_minutes(advisor_rows=30) gives chosen 60, so the number fits, but only if the caller passes rows with his_answer, not all rows; the tool's docstring says "advisor rows (2 minutes each" and would read as all 129 (258). Also audit_line prints "chosen 60 (advisor)", not the promised "(30 advisor rows with his words of 129)", and the command line has no way to pass advisor rows at all, so it always prints "n.m.". Add after the "With the advisor rows measured" line: "To produce this, the caller passes advisor_rows = the number of numbered rows with his_answer (30, not 129); the tool's line shows only the minutes, so the row counts are added by hand until the tool takes a total as well." (The tool fix itself is a list item for the main session, not part of this paper.)
