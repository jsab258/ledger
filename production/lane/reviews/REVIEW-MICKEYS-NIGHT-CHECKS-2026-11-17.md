# Review: Mickey's night checks (17 Nov 2026)

Verdict: PASS WITH FIXES

Checked against TARGET-MICKEYS-NIGHT-2026-11-17.md. The 13-point count (1 settled, 2 corrected, 2 partly, 8 open) matches. 500 to 167 lm is log2(2.99) = 1.58 stops: correct. EN 13201-2 is a 2003 standard: correct. The street door is the only dark key in mickeys-office.json line 16: correct. Glass: one WebSearch (read 17 Nov 2026) found the Scheuten Float January 2018 datasheet; its results gave titles only, so 91% and 8% are not confirmed from the search, though they agree with clear float's usual values.

Findings and fixes:

1. The window ratio uses the wrong pavement. It keeps EN 13201's 2 to 15 lux, the standard the same file throws out. With BS 5489-3's 3.5 to 10 lux at albedo 0.15 (0.17 to 0.48 cd/m2), a lit window at 6 is 3.6 to 5.2 stops. Fix: work it out again on BS 5489.
2. The 9-stop top end uses 50 cd/m2, which the file itself says covers advertisements, not just shop windows. Mickey's is an office window anyway. Fix: give 6 cd/m2 as the main figure and call 50 an upper bound you cannot fully rely on.
3. Paint: the fascia's 0.085 is above both cited samples (0.0385 and 0.05), so "in range" goes further than its sources. Fix: "brighter than the modern dark samples read".
4. Summary point 4: "a small sign lamp fits" rests on one modern London source with no date. Fix: "matches modern fronts; 1990 not checked".
5. Novak is cited as read today, but the parent could not open that PDF. Fix: say how it was read.
6. BS 5489-3:1992 falls inside canon's window but is not a 1990 standard. Fix: say so.
