# Review 09: spending and pace

Fresh reviewer, read only, 19 November 2026. Sources: the token audits and DAILY files (production/research/token-audit/), the time log (production/time-log.jsonl, read through tools/timelog.py), the four orders and their archives (production/orders/), the progress page data (production/progress-page/progress.json), FOR-JAFAR.md, RULINGS.md, CLAUDE.md, DECISIONS.md, tools/pace_line.py, tools/token_measures.py, tools/lane/item_tags.py, production/api-spend.jsonl, and all 402 report rows sent to his page (4 to 19 November). Git history on this branch starts on 17 November, so older changes were read from the files themselves. Dollars below are the studio's own API-price measure of the PC's Claude Code logs, not his bill.

## Summary

The studio measures how much of the allowance it uses in great detail, and almost nothing about what that allowance buys. Rows carry the meter, the pace and the dollars every hour (300 of 402 rows), the DAILY files measure cache writes and start tokens, and the efficiency targets push towards using more (idle hours down, leftover week down). But the one number his scope rule of 5 and 6 November depends on, the cost of a finished piece, has not been measured: Ron's cost table is mostly "not recorded" and the progress page's person cost is null. Each Monday's costed order is replaced within days by picks that arrive through the advisor, so the hours in the order are not what the week spends. In the double week of 16 November, Kiln (the studio's own cloth tool) took an estimated 64% of the spend against 23% costed; by 01:32 on 19 November nothing from it was in the game, Kiln v1 stood at 0 of 6, and none of the week's eleven order items was done. The guards (pace bands, Fable cap, the 99% line) were each built after a breach that Jafar or the advisor raised, and their exceptions let the week run 17 to 24 points ahead of the line. The meter and the dollar measure have drifted about threefold apart since late October and no file reconciles them. Ten findings: four high, five medium, one low.

## The weeks in numbers

| Week | Meter used | Dollar measure | Order items | What he could see or play |
|---|---|---|---|---|
| 26 Oct to 1 Nov | about 83 points in four and a half days (orders/2026-11-02.md:127) | US$2,222 (AUDIT-2026-10-26_to_2026-11-02.md:5) | 47 done, 43 set aside, 165 carried (many were studies) | street at real values, Tom dressed, the camera, the sit (his own list, orders/2026-11-02.md:127) |
| 2 to 8 Nov | 89% at 12:29 on 9 Nov (row 2026-11-09-1229) | US$1,370 (MONDAY-AUDIT-2026-11-09.md:51) | 17 done, 6 set aside, 52 carried | Ron and Darren dressed in the packaged game; the corner passed packaged |
| 9 to 15 Nov | 97% (progress.json, weeks row) | US$930 (same) | 5 of 14 done | Tom's whole-person page, the scanned crate, lighter shop windows; Kiln garments in the game: 0 (progress.json:716) |
| 16 to 19 Nov, 01:32 | first leg to 100%, then 33% of the spare reset in ten hours | about US$983 for 16 to 18 Nov (DAILY-2026-11-16/17/18) | 0 of 11 done; 2 moved out on the first evening | new brick, compressed street pictures, Ron's "tonight" line built but unheard, the Quay Run driving study in a browser |

By the brief's kinds (art, Kiln, tools and process, research, prototype, the game): not recorded by any file. Nearest readings: 26 Oct week, 44% of dollars in no time-log task, research helpers 16%, reviewing helpers 14% (AUDIT-2026-10-26_to_2026-11-02.md:14-24). 9 Nov week: eight outside tool tests, an AI-video experiment, a texture test, a Fable replay and Kiln from 13 Nov, none in that week's order (orders/2026-11-09.md has no Kiln or tool-test item). 16 Nov week: Kiln about 64% (DECISIONS.md:398, an estimate); Fable helpers US$146 of US$503 on 18 Nov. The cloud lane's work is not in the PC's logs at all.

## Findings, ranked

### 1. No number says what the allowance buys (high)

Impact: his scope rule (RULINGS.md:15, "If cost per piece has not clearly fallen by 1 February, scope moves first") cannot be applied, and every budget decision he makes rests on spend, not on output.

Evidence:
- progress.json:563 "person_hours": null, "One complete named person (Ron first...): not measured yet." The Ron item was costed at 16 h in the 9 Nov order (orders/2026-11-09.md:26), carried into n16-2 at 10 h, still open.
- RON-COST-TABLE-DRAFT-2026-11-09.md: body, hair, trousers, boots, sitting, office exit, voice after 1 October all "not recorded"; most other rows "bounded, indicative span" from git.
- progress.json:630 "The Second Suit" (cost of a repeat against the first), state "unchecked".
- tools/lane/item_tags.py:4 "since 9 November only about 40% of logged hours carried an item code, the time log has no entry after 17 Nov 14:30".
- Steps in no time-log task: 44% of dollars (26 Oct week), 33% (2 Nov week, MONDAY-AUDIT-2026-11-09.md:55); 18 Nov "Most of the week's steps had no time-log task" (row 2026-11-18-0850-main).
- The efficiency targets on the progress page measure use, not output: "The Idle Hours" target 95% of the day working, "The Leftover Week" target 5% unused (progress.json eff_bosses).

Jafar raised the need himself on 1 November ("By Wednesday, from the time log and the token audit, the cost of each finished piece type", orders/2026-11-02.md, section 7) and again through the blind-spots review he adopted on 18 November 08:05 (DECISIONS.md:396). The check that should have caught it: order_ledger.py accepting an item as done without hours and dollars.

Proposed end: rule. An order item counts as done only with its hours and dollars from the item tags; every Monday the progress page shows cost per finished piece beside the first of its kind, and "The Second Suit" replaces "The Leftover Week" as the lead efficiency number.

### 2. Each week's costed order is replaced within days (high)

Impact: the hours he approves on Monday are not what the week spends; his attention goes into approving plans that do not run.

Evidence:
- 9 Nov week: 14 costed items, 99 of 120 hours (orders/2026-11-09.md:20); 5 done. The spend went to tool tests, the texture test ("his adoption overrides the +7.2 small-pieces rule", DECISIONS.md:38), the AI-video experiment and Kiln, none costed in the order.
- 16 Nov week: Kiln costed at 46 h, 23% (orders/2026-11-16.md:15); his pick of 17 Nov 10:10 moved it to about 70% (orders/2026-11-16.md:81), with the street scale test, the corner copy and the rest waiting. Cars and the games' numbers were moved out at 21:16 on the day of adoption (lines 89, 91). By 19 Nov no n16 item is done.
- The waiting list, meant to hold everything new, grew from 12 to 24 lines in three days (orders/2026-11-16.md:36-59).
- The same cause was named before: "The main cause: mid-week orders that never said what they displaced" (orders/2026-11-02.md:127), and his rule "Nothing new between Mondays unless something is broken" (line 130). The rule is enforced against the sessions, not against picks that come through the advisor.
- Orders were to be "about 1,200 words at most" (line 140). Actual: 25 Oct 28,226 words; 2 Nov 8,026 plus 22,129 archived; 9 Nov 6,353 plus 12,348; 16 Nov 3,599 plus 6,157.

Raised by him on 1 November; repeated each week since. The check that should have caught it: a mid-week pick has no step that re-costs the order and names what it displaces.

Proposed end: ruling for him. "When a pick changes the running week's shares: A) it waits for Monday's order (recommended), B) it runs only with a written displacement in hours, re-costed in the order the same hour, C) as now."

### 3. Kiln took most of the double week; nothing from it is in the game yet (high)

Impact: the largest single use of the allowance is a tool, not the game; RULINGS.md:39 says "game never waits on it", yet the street and cars wait.

Evidence:
- Kiln's share by item since Monday 16 Nov: 64% (DECISIONS.md:398, "untimed steps by what they touch, a keyword estimate"); the order costed 23%.
- "Kiln-made garments in the game: 0" (progress.json:716); "STATE (18 Nov 23:32): Kiln v1 0 of 6" (NOW.md); Ron's Kiln trousers wait on a licence tap (rows 2026-11-17-2345-main to 2026-11-18-0100).
- Six hourly rows in a row on 18 Nov say "Nothing you'd see in the game changed this hour" (09:57, 10:47, 11:37, 12:31, 13:31, 14:28), while the meter went from 80% to 97% and one hour cost US$52.62 (row 2026-11-18-1137-main).
- Estimate misses: "Rigging Kiln's outfits to the cast (M5) is bigger than it looked: about 27 to 29 h against the 3 to 5 planned" (row 2026-11-17-0717).
- Fable at max on Kiln: US$146.09 of US$503.10 on 18 Nov (DAILY-2026-11-18.md:8).
- The 64% is inflated by an unknown amount: since 18 Nov every session start is tagged with the current item (item_tags.py hook_session), so 652 minutes of "n16-1 session startup (auto)" in the time log, including page, advisor and rulings work, count as Kiln.

Proposed end: ruling for him. "Kiln's share of the next order: A) 15% until one Kiln garment walks the packaged game (recommended), B) 30%, C) 70% again." Plus a rule: Kiln's share is counted only from Kiln-tagged helpers and windows, never from the default tag.

### 4. The guards fire after the money is gone (high)

Impact: the week runs far ahead of the line and also sits idle, so neither the pace nor the output is steady; each guard arrived after a breach he or the advisor found.

Evidence (pace from the 204 rows that carry it):
- RULINGS.md:37 "over 6: no new token-heavy work or helpers, his priority items and card or processor jobs excepted". The 9 Nov week ran above +6 for most of 10 to 15 Nov, peak +17.3 at 04:07 on 14 Nov (row 2026-11-14-0407). Kiln as "his priority" was the exception each time (rows 2026-11-13-1834, 2026-11-18 advisor 236 at DECISIONS.md:447).
- After the spare reset at 15:20 on 18 Nov: 33% by 01:32, +23.9 (row 2026-11-19-0132), about 3.2 points an hour against his "steady 1.4 points an hour" of 17 Nov (DECISIONS-TRACE D-B-003). The ceiling then set allows 25 points ahead (week-shape.json, advisor 237).
- The first leg reached 100% against his "never 100" (pace_line.py:25): "on 18 Nov it went from 97% to 100% between hourly rows, no warning" (orders/2026-11-16.md:58).
- Fable: the 9 Nov replay "overshot its 5% cap by about 3 points" (MONDAY-AUDIT-2026-11-09.md:57); the session ran on Fable from 13 Nov 17:21 for about 28 hours at twice the dollars per step "and nothing caught it" (tools/token_measures.py:462; his words 21:11 on 14 Nov, DECISIONS.md:156); the 40% cap's hook was built at 22:41 on 18 Nov, and Fable read 44% at 00:08 and 45% at 01:32 on 19 Nov (rows), because the hook refuses only new helpers.
- Idle at the same time: 336 minutes waiting on 12 Nov, "Most of it was the pace hold" (row 2026-11-12-2351); 49% of the day working (progress.json, The Idle Hours); no session 12:29 to 15:31 on 9 Nov because the start task named last week's order (row 2026-11-09-1536); nothing from 00:50 to 05:15 on 11 Nov after a setting lapsed (row 2026-11-11-0727). Eight of 48 lane rows are refills or pace-guard stops with no work (for example 2026-11-18-1416-lane, 2026-11-19-0016-lane).

Raised by him or the advisor: 14 Nov 21:11 (Fable all day), 18 Nov 15:23 (advisor 225, the 100%), 19 Nov 00:18 (advisor 237, one ceiling). What would have caught it earlier: a projection from the real meter every 15 minutes (the reading is typed by hand from the app's usage tool, pace_line.py:8), a guard that stops running helpers rather than only new ones, and a written list of exceptions that cannot exceed a stated number of points.

Proposed end: rule. The pace guard projects, not compares; above the line plus 6 even priority items run with at most two helpers; a cap breach stops running helpers of that model within the hour.

### 5. The meter and the dollar measure have drifted apart and nobody reconciles them (medium)

Impact: if a large part of the meter is used outside the PC's logs, the studio's audits explain only part of where his allowance goes.

Evidence: dollars per meter point fell from about 25 (US$2,222 for about 83 points, late October) to about 15 (US$1,370 for about 89, 2 Nov week), about 10 (US$930 for 97, 9 Nov week) and about 8 (about US$983 for about 124 points, 16 to 18 Nov). No file relates the two (searched token-audit, orders, DECISIONS, handover). On 18 Nov at 00:30 to 01:25 "Fable's weekly meter 43% (not used by this session)" (rows), so another consumer was drawing on it. The cloud lane, the advisor chat and his own tool-making sessions are all outside tools/token_audit.py, which reads only this PC's logs. The cause is unverified.

Proposed end: rule. The Monday audit adds dollars per meter point and a line per consumer (main session, its helpers, the lane, the advisor, anything else on the account); a change of a third is flagged.

### 6. Process overhead is measured narrowly and is probably well above 15% (medium)

Impact: RULINGS.md:23 sets "Records and process under about 15% of spend"; the readings of 4% to 13% count only steps that touch record files, so the line is checked against a floor.

Evidence:
- The audit itself says the scope is partial: reviews of records and records written inside building steps "not measured" (MONDAY-AUDIT-2026-11-09.md:10-13).
- Not counted at all: 402 rows to his page in 15 days (48,412 words; 58 rows on 18 Nov), 237 advisor messages (DECISIONS.md cites advisor 14 to 237), DECISIONS.md 31,096 words in ten days with 111 entries on 18 Nov alone, at about 68 words each against RULINGS' "about 40 words" (RULINGS.md:36), RULINGS held at 4,899 of 4,900 words by repeated condensing, 146 scripts in tools/, eight DAILY files and 19,560 words of token-audit research.
- The time log's labelled minutes in the 16 Nov week: page, advisor, rows and rules tasks about 300 of about 1,500 labelled minutes, about 20% (time log tasks such as "his page, advisor 171-172, rows, the week's numbers", 73 min).
- The DAILY measures found savings of about US$3.50 a day, 2% (DAILY-2026-11-11.md:35), while the measuring runs every day.

Proposed end: rule. A "process" item tag (advisor, page, rows, rules, records, measures, checks) on every session and helper, its share shown each Monday against the 15% line; rows to him shrink to what changed in the game, with the meter in one daily line.

### 7. Estimates and the progress page tell a better story than the records (medium)

Impact: he plans the release on numbers that the studio's own files say run two to four times short.

Evidence:
- "Records run 2 to 4 times plan figures" (production/research/phase2-plan/PIECES-DRAFT-2026-11-08.md:26); phase 2 "does not fit even at plan figures" (line 103).
- Orders assume 120 and 205 "main-line hours" a week (orders/2026-11-09.md:20, orders/2026-11-16.md:5); the one measured week logged 57 h (PIECES-DRAFT line 106); timelog.py reads 1,461 and 2,226 minutes for the last two weeks.
- The 2027 line read 2.4 weeks behind on 9 Nov (PIECES-DRAFT line 101) and 0.5 weeks ahead on 17 Nov (progress.json:537), after phase 1 closed with four of six bosses "listed at the exit", not beaten (progress.json bosses_closed).
- His 9 Nov order: phase 2's estimate "re-estimated every Monday" (DECISIONS-TRACE D-E-032). The page's second point is "last point less the 21 h of phase 2 work in the time log; not re-estimated" (progress.json:650).
- "friends_eta": "around January", "if phase 1 passes in the next week or two" (progress.json:4-5), unchanged after phase 1 closed unpassed.

Proposed end: rule. Every estimate shown to him carries the measured overrun factor beside it; the 2027 line counts listed, unbeaten exits as weeks owed; the Monday point is re-estimated or marked "not re-estimated" in his view, not only in the data.

### 8. The 70/10/20 rule is dead but still written in CLAUDE.md (medium)

Impact: the startup file every session reads describes a budget nobody runs; reviewers and new sessions follow the wrong one.

Evidence: CLAUDE.md:16 "70% production, 10% independent review, 20% kept for him; he reads the meter and stops the session". Since then: "stop you near 85%" (orders/2026-11-02.md:170), "Use the whole week's allowance" (his yes, 6 Nov, items/whole-allowance-2026-11-06.json), the line to 90% with the last 10% shared (RULINGS.md:37), "the allowance fully used" (RULINGS.md:23). Weeks now end at 97% to 100%. Review share: 13%, 0%, 0%, 4%, 6%, 3%, 1% of logged minutes by week (timelog.py week) and 4% to 18% of dollars (audits, DAILY), never measured against 10% by any check. FOR-JAFAR.md was stopped on 9 Nov (its line 1) yet CLAUDE.md still requires it and the file still holds 3,511 words. The settings check calls the reviewers' high effort "wrong" (DAILY-2026-11-18.md:38) although his 18 Nov pick set high effort to 23 Nov.

Proposed end: ruling for him (CLAUDE.md is his). "Replace CLAUDE.md's 70/10/20 line with: A) the pace line plus a measured review floor of 10% of dollars (recommended), B) the pace line alone, C) keep 70/10/20." Deletion: move FOR-JAFAR.md to production/archive/ (safe: stopped by RULINGS 9 Nov, nothing writes to it). Rule: settings_check reads the week's effort picks.

### 9. The game's API credit was about 95% lost (medium)

Impact: money already paid for went unused while the subscription allowance carried bulk work.

Evidence: "the credit's month ends today with US$10.80 of US$200 spent since 12 Oct" (orders/2026-11-16.md:100, 11 Nov 08:50); n09-14, "The month's API credit used before it ends", set aside after US$1.15 (same line); "Game's own API credit: US$0 this week" for 9 to 15 Nov (progress.json weeks row); production/api-spend.jsonl holds 28 paid runs, about US$13.50 in all since 1 Nov. His correction of 1 Nov said the ceiling exists "so the credit is used rather than lost" (orders/2026-11-02.md:177 onward). RULINGS.md:48 allows the credit for bulk text and scripted checks, including Kiln's render checks.

Raised by him on 1 November. The check that should have caught it: the day's ceiling is logged, but nothing warns when spend sits far below it.

Proposed end: rule. Each order names the credit's planned use in dollars; the Monday audit shows used, left and lost, and a week under a quarter of the ceiling puts one costed use on the order.

### 10. The time log is partial and now default-tagged (low)

Impact: the studio's only per-task hours cannot cost a piece and now leans the Kiln share upward.

Evidence: no entries in the week of 12 Oct (timelog.py week 2026-10-12: 0 minutes); two single tasks of 12.5 and 13 hours, one "recorded afterwards from the commit time"; 43 automatic "session startup" lines on 18 Nov, about one every 15 minutes, each tagged n16-1 whatever the session did; only two kinds, production and review, so research, process, prototype and tools cannot be told apart. The advisor said on 31 Oct "the time log holds only about half the running hours" (orders/2026-11-02.md:127).

Proposed end: list item. Tag every session and helper at start with item and kind (game, Kiln, tools, research, prototype, process), never a default; drop the time log once item tags cover 90% of dollars for two weeks.

## The brief's questions, briefly

Same game: spending serves the meter; nothing ties spend to his 18 Nov direction. Still true: not CLAUDE.md's budget line, the FOR-JAFAR rule, the 2027 line or the friends' date. Dead weight: FOR-JAFAR.md, most DAILY micro-measures. Cost: findings 1 to 6; hours per finished piece not recorded. Missing: cost per piece, meter against dollars, spend by kind, the lane's spend. Contradictions: findings 2, 3, 4 and 8. Raised by him first: 1 Nov (half-empty time log, mid-week displacement, cost per piece, lost credit), 14 Nov (a day on Fable), 18 Nov (Kiln undercount, 97% to 100% unwarned), 19 Nov (one ceiling).
