# Owner minutes a week: a measure for Monday's audit

Written 18 November 2026 by the lane, for blind-spots recommendation 8 (adopted 18 Nov 08:05). A design only: no code was written.

## Why

His attention is the scarcest input and no audit line counts it. Last week's audit found 21 of 36 asks were not his and four days had more than two batches (from the blind-spots brief; that audit file is not in the repository, so unverified here).

## What is counted, and where it comes from

| Event | Data source | Minutes per event |
|---|---|---|
| Page item read | production/approvals/needs-you/items.json and archive.json (title, text, why, steps, options, recommendation, detail) | its words ÷ 200 |
| Tap (his pick) | stored answers: production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8/ (field "at"), mirrored from the page's database | 10 seconds a tap (estimate) |
| Picture looked at | "pictures" on the item | 20 seconds a picture (estimate) |
| Hands at the PC (ACTION, his_hands) | the same items: "tag", "his_hands", "steps" | 5 minutes to reach the PC plus 30 seconds a numbered step (estimate) |
| NEEDS YOU messages and reports | the page database's "reports" rows (artifact 1VZHkCBAHdw8HBdNHrByL8) | words ÷ 200, counted once each |
| Pages he is pointed to (progress page, recipe map, a review page) | production/progress-page/progress.json; links on items | words of the visible text ÷ 200, once a week |
| Advisor chats | the database's "advisor" rows, numbered (RULINGS 4 Nov); his_answer marks his own word | 2 minutes a numbered row (estimate) |

Reading speed: 238 words a minute is the average silent reading rate across 190 studies (Brysbaert's meta-analysis, reported by BPS Research Digest, 13 June 2019: https://www.bps.org.uk/research-digest/most-comprehensive-review-date-finds-average-persons-reading-speed-slower). On phones, hard text took about 30 milliseconds more a word than on a desktop (Nielsen Norman Group, 11 December 2016: https://www.nngroup.com/alertbox/mobile-content-comprehension.html). The lane recommends 200 words a minute: rounded down for a phone, for text that is partly technical, and for a reader whose first language may not be English (that last point unverified).

## What cannot be measured, and is estimated

- Whether he opened a report or page: no read receipt, so each counts as read once (an upper bound).
- Thinking before a tap, and typing to the advisor: the chat is not in the repository; fixed estimates above.
- Time at the PC for an ACTION: no timer; the step estimate stands until he says how long one took.
- Rereads: not counted.

## A worked check on last week's records

From items.json and archive.json, 9 to 15 November: 49 items added, 7,253 words (median 116 words an item), so about 36 minutes of reading at 200 words a minute; 46 stored answers dated that week, about 8 minutes of taps. That is about 44 minutes before reports, pages, pictures and advisor chats. The items came at 12 separate times on 9 Nov and 10 on 11 Nov (distinct "added" stamps, open and done together). Advisor rows ran from about 75 (10 Nov, production/research/ai-video-motion/SOLVE-CPU-ROUTE-2026-11-10.md) to about 177 (16 Nov audit, tools/needs_you_page.py), roughly 100 a week, which at 2 minutes each would be over three hours (estimate, unverified: the row count was not read from the database for this paper). The true weekly total is likely well over an hour.

## Monday's line (one line, beside the process share)

`Owner minutes 9 to 15 Nov: 44 measured (asked 44: items 36, taps 8, hands 0; chosen n.m.: advisor rows; reports n.m.); 1.9 a finished piece; target 30 | process share 13%`

"Asked" is what the sessions put to him; "chosen" is what he starts (advisor chats). The target applies to asked minutes; chosen minutes are shown, not judged. "n.m." means not measured that week. In the sample line only items, taps and hands come from the records; the per-piece figure, the target and the process share are illustrative.

## The recipe number

Owner minutes per finished piece: asked minutes ÷ units marked finished in NOTEBOOK.md that week (RULINGS 9 Nov: each finished or set-aside unit gets its lines there). It belongs in RECIPE.md beside each chapter, so a piece type that keeps pulling him in (garments, faces) shows it.

## Suggested target, for him to set

The blind plans used about 10 minutes a week of samples plus one 20-minute playtest a month (about 15 minutes a week), on one phone screen a week. His rulings allow one standing page with items in up to two batches a day (RULINGS 2 and 8 Nov), which is far more. Options:

- A. 20 asked minutes a week: matches the blind plans; would force most items into the sessions' own decisions.
- B. 30 asked minutes a week, at most two batches a day, ACTION items counted in full (recommended): about a third below last week's 44 asked minutes, room for the monthly playtest and a real trade-off each day.
- C. 45 minutes: little change from now.

Over the target two weeks running, the audit names the three costliest item types and who sent them.

## What ask_minutes already does, and what to extend

tools/token_measures.py ask_minutes(day) measures minutes from an item being added to his answer: waiting time (cycle time, measure 5), not his effort. Its join of items to stored answers and its Swiss-time reading are the right base. Extend it, or add a sister function, to cover a week, count words, pictures, ACTION steps and taps, and read the "reports" and "advisor" collections. tools/needs_you_page.py --action-week already lists ACTION items; its batch check counts only open items, so done items that came in extra batches slip through.

## Function spec (spec only)

owner_minutes(week_start, items, answers, reports, advisor_rows, finished_units, wpm=200, tap_s=10, pic_s=20, pc_walk_min=5, step_s=30) returns {asked, chosen, items_min, taps_min, pictures_min, hands_min, reports_min, advisor_min, per_piece, estimated_parts, batches_by_day}.

- Only events with dates in [week_start, week_start + 7 days), Swiss time.
- One 200-word item, answered: 1.0 + 0.17 = 1.17 minutes.
- One ACTION with 10 steps: reading its words plus 5 + 5 = 10 minutes more.
- An answer with no matching item: tap counted, item minutes 0, listed in estimated_parts.
- No finished units: per_piece is "none finished", never a division by zero.
- Three items added at 09:00, 12:00 and 18:00 on one day, two already done: batches_by_day shows 3.
