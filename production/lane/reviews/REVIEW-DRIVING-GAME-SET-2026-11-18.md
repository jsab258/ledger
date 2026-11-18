# Review: the driving game set (advisor item 4j), 18 Nov 2026

Fresh reviewer, lane run of 13:16. Verdict: PASS WITH FIXES (three, applied).

- Every band matches his 18 Nov ruling exactly in the feel-targets file (sections c2 and f), the code's game set and the tests. The default set is "game"; "ordinary" and "fast" stay selectable and tested. 33 tests pass; tools/driving_feel_check.py finds no fault; RULINGS' Cars line agrees.
- Physics: M1 and M2 fit a power-limited car with drag. One corner pair cannot happen together (0-30 at 4.5 s with 0-60 at 10 s), harmless at band level. Braking at the short end needs about 1.14 g while steady cornering grip is 0.82 to 0.92 g: braking beats cornering by up to about 25%; the file already declares about 1.1 g as game licence. Front load, wet ratio, field of view and turning circle plausible.
- Footage method sound and outside-only (frame stepping and screenshots, scale from markings or car length, at least 3 games with 5 samples each, median of medians, stated half-widths, clip to the 1990 floor).
- Fixes in FOOTAGE-TO-GAME-SET-2026-11-18.md: "largest of" wording; the big saloon and fast hatch videos used only for the relative-speed check; M8's highest sample marked a lower bound.
- Open: the fast set overlaps the game set on braking and grip; the reference car is not tuned to the game set; the checker's "game band" word test would have passed before this change too (a weakness of tools/driving_feel_check.py, the main session's file).
