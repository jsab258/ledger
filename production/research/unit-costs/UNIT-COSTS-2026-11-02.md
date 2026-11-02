# Unit costs of finished pieces, 2 November 2026

Item n02-7-1, for phases 6 to 10. Data: unit-costs-2026-11-02.json.

**Method and limits.** Hours are stop minus start in production/time-log.jsonl (166 windows since 5 October). Token dollars come from production/research/token-audit/audit-2026-10-26_to_2026-11-01.json, for 26 October to 1 November only. They are API-price equivalents, a measure and not a bill, and 43% of that week's dollars (US$917) fall outside any task window, so per-piece dollars are floors. The log has no entries for 9 to 22 October, 26 Oct 11:03 to 27 Oct 02:58 (DECISIONS.md, 27 Oct 04:39) or 31 October; there RECIPE.md "Cost" lines stand in. Windows overlap when helpers run in parallel; helpers' clock time is not logged; unlogged tasks are uncounted. Tags: **M** measured (summed or copied from a file); **I** inferred; **R** inferred from a RECIPE.md cost line (the session's rounded figure).

| Type | Finished examples | Hours each | Median h | Token US$ | Gate rounds | Set aside (h) | Confidence |
|---|---|---|---|---|---|---|---|
| Shop front | ironmonger, newsagent, tea rooms, grocer, chandler, launderette | 4.0 R, 3.0 R, 4.5 R, 4.5 R, 4.5 R, 3.6 M | 4.25 I | none | 7, 2, 8, 10, 9, 5 | Rita's wear try 1: 1 R; chandler joinery: 2.7 R | medium |
| Garment | Tom's jacket, jeans, jumper, boots | 6.8, 1.6, 2.8, 2.9 (M, shared windows split I) | 2.9 I | 220, 58, 60, 68 (M floors); 306, 74, 76, 88 (I, gaps filled) | jacket 3 (2 fail, 1 pass); outfit 2 | 4.1 M inside the rows; Ron's outfit, not itemised | medium |
| Person's routine | none | none measured | none | none | none | none | none |
| Talk feature | cited facts at source; two copies of each check; fast checker in game (off) | 1.0, 1.2, 2.7 (M, shares I) | 1.2 I | 6, 22, 18 (M floors) | not visual | fast checker's 4th try 2.1 M; early-reply lever 1.5 M, US$50 | low |
| Gate | office, glass, item 1.1 third review, Tom's outfit | 0.85, 0.50, 0.50, 0.07 (M, session time) | 0.5 I | outfit gate 3.3 M floor | 2, 3, 10 reviewers, 2 or more | none | low |

**Shop front.** Counted: six designed shops brought into the street and through a ten-view gate, 22 to 24 October, each worn. Hours are RECIPE.md lines except the launderette, whose log window (3.58 h) matches RECIPE.md's 3.5. Excluded: Rita's pilot (10.5 h R, first of its kind); the design side (3 to 4 h a shop, I, from 15 h for five and 16 h for four); the chandler wear redo of 30 Oct (1.77 h M, US$2.77); the west-eaves fix (1.7 h R for three). Biggest uncertainty: five hours are the session's own "about", and no front has dollars.

**Garment.** Counted: every window naming the jacket, jeans, jumper or boots; mixed task texts split equally by clause, outfit-level windows four ways (I); set-aside attempts inside the rows included. The outfit passed its editor gate on 30 Oct, not yet packaged (NOW.md). The jacket is first of its kind: its 3 h bake chain fell in the log's lapse, so about 9.8 h with it (I); RECIPE.md's jacket lines sum to 7.7 h (R). Biggest uncertainty: helper work for jeans and jumper sits partly outside the windows.

**Person's routine.** No finished example is timed. Cloud-week unit 11 (13 Oct) proposed schedules for nine people inside a larger batch, cost not recorded (RECIPE.md, "What came before"); TOWN.md holds no cost; no log window or audit item names a routine.

**Talk feature.** Counted: three features that reached the game, windows of 27 and 28 Oct; RECIPE.md says 1.5, 2.5 and 1.0 h. Game credit spent on their tests is separate: US$0.45 to 17.86 each, median 0.53 (R). Excluded: tries inside the lapse; the 1 Nov lever's window (shared with the Pocket-voice mend); the 7 Oct bundle (1.54 h M for four small features). Biggest uncertainty: windows mix several items.

**Gate.** Counted: review-kind windows, session time only (reviewers run beside it). A ten-view shop gate is already inside the shop-front hours: median 0.5 h a round all-in (I; 0.36 to 0.72), 5 to 10 rounds. Reviewer cost US$0.72 to 1.58, median 1.03 (I; four windows stating a reviewer count). Biggest uncertainty: the chandler's nine-reviewer gate shows only US$2.77, so reviewer dollars are undercounted.

## What the planner can multiply

- **Shop front:** 4.3 h (3.0 to 4.5) through its gate, plus 3 to 4 h if the design is also made; first of a new kind 10.5 h. Dollars unmeasured; stand-in US$22 to 38 per logged hour (M: US$1,212 over 55.4 in-window hours; US$2,130 over 56.7).
- **Garment:** first of a kind about 9.8 h, US$220 to 306; later ones 2.8 h (1.6 to 2.9), US$58 to 68 (floors) or 74 to 88.
- **Talk feature:** 1.2 h (1.0 to 2.7); token US$6 to 22, plus about US$0.5 of game credit.
- **Gate (three views):** about 2 rounds, 0.07 to 0.85 h session time, US$2 to 5 a round (I).

## Not measured yet

A person's routine (planned for bulk API work, item n02-6-4); shop-front dollars; helpers' clock time; the three log gaps; the outfit packaged and passed by Jafar; anything after 1 November.
