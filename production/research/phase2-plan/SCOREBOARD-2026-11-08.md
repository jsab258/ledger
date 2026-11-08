# Efficiency scoreboard, first table (8 November 2026)

For n09-4. Extraction only: counted and quoted, no judgement. Read on 8 Nov 2026.

**Sources.** production/time-log.jsonl (596 lines: 303 starts, 293 stops; 303 windows; read whole by a throwaway script run read-only). UNIT-COSTS-2026-11-02.md ("UC") and unit-costs-2026-11-02.json ("JSON"). RON-MEASURES-2026-11-08.md ("RM"). PIECES-DRAFT-2026-11-08.md ("PD").

**Tags.** M measured (a time-log window, stop minus start, or to the next start where no stop exists). R from a RECIPE.md Cost line, as copied in UC/JSON (RECIPE.md itself not re-read). I inferred (arithmetic on the above). E estimate only. "Not logged": no window names it. Time-log line numbers are file lines (a window "88-89" is its start line and stop line). Hours are task-hours; windows can overlap, so sums are not wall clock.

## 1. Kinds of work done more than once

| Kind | First instance (name, date, hours) | Latest instance (name, date, hours) | Ratio latest/first | Source rows |
|---|---|---|---|---|
| Shop front, from the pilot | Rita's front (pilot), 21-22 Oct, 10.5 R (incl. 1.0 set aside) | launderette, 24 Oct, 3.58 M | 0.34 | JSON lines 90-92 (pilot); time-log 88-89 (launderette) |
| Shop front, from the first of the six counted | ironmonger, 22 Oct, 4.0 R | launderette, 24 Oct, 3.58 M | 0.90 (R against M) | JSON lines 31-32; time-log 88-89. Between them, all R: newsagent 3.0, tea rooms 4.5, grocer 4.5, chandler 4.5 (UC line 9). Nothing logged 8 Oct 16:10 to 23 Oct 15:15 (JSON time_log_limits) |
| Garment | Tom's zip jacket, 28-30 Oct, 6.78 M share-weighted (at least 9.78 I with the bake chain outside the log) | Tom's jeans, 30 Oct, 1.61 M/I share-weighted | 0.24 (0.16 against 9.78) | JSON lines 167-168, 207-208; UC lines 10, 17. Jumper 2.81 and boots 2.95 between (UC line 10). Jeans windows in the log: 270-271 (0.12), 304-305 (1.53, shared with jumper and boots) |
| Dressing a man (outfit) | Tom's whole outfit (jacket, jeans, jumper, boots), 26-30 Oct, 14.15 M/I (unfinished, editor gate only) | Darren and Ron, dress-the-cast, 7-8 Nov, six windows, 5.81 M (names both men, front-edge wear and hair in the first window) | 0.41 | JSON line 284 (total_outfit); RM 1a rows, time-log 547-548 (1.77), 549-550 (0.47), 551-552 (1.49), 553 (1.15, no stop), 555-556 (0.63), 557-558 (0.30) |
| Dressing a man, the one person | same first | Darren alone, 7 Nov, 1.96 M (the two windows naming only him); his third try (1.15) is shared with Ron's collar | 0.14 | time-log 549-552 (0.47 + 1.49); RM 1a and "Darren's same rows" |
| Talk feature | two copies of each check call, 27-28 Oct, 2.8 R (window reading 1.2 M) | fast checker in the game behind a switch (off), 26-27 Oct, about 11.0 R, four tries 5, 2.5, 2.5, 1 (window reading 2.74 M) | 3.93 R; 2.28 M | JSON lines 355-372, 373-390; UC lines 12, 21. The cited-facts feature, 1.5 R (window 1.0 M), is the third in UC; the 7 Oct bundle of four small features is 1.54 M in one window (time-log 36-37) |
| A prop, review windows only (making time not separable) | crates, 3 Nov, 0.30 M (day 0.13 + night 0.17) | litter, 3 Nov, 0.78 M (three rounds, day and night) | 2.6 | time-log 374-377 (crates), 380-383 (kiosk, 0.12 + 0.18 = 0.30), 386-397 (litter: 0.13, 0.08, 0.17, 0.22, 0.08, 0.10). Sums of rounded window hours. The corner's making windows (350-353, 366-367, 372-373, 378-379, 384-385) do not name a prop |
| Gate (review-kind window, session time) | item 1.1's third review, ten reviewers, 8 Oct, 0.50 M | two fresh reviewers on jeans/boots and sitting, 4 Nov, 0.12 M (two pieces in one window) | 0.24 | time-log 52-53; 454-455. Between: office gate, eight reviewers 0.85 (74-75), glass gate, seven reviewers 0.50 (82-83), outfit gate launch 0.07 (312-313). Office rounds of 3 Nov: 0.13 + 0.13 + 0.05 + 0.07 = 0.38 (400-407; reviewer count not in the text) |
| Packaged pass (packaged build with its reviews or film) | a packaged build as 1.1's evidence, packaged walk-in and two reviews, 8 Oct, 0.92 M (also holds the frame-rate verdict traced) | sitting packaged film, 6 Nov, 0.27 M | 0.29 | time-log 78-79; 505-506. Between: Mickey's office photographed in the packaged game, three gate reviews, 27 Oct, 0.22 (188-189); n02-packaged-walks, 3 Nov, 0.55 (358-359) |

Notes on the table.
- The garment and dressing rows use the same windows (Tom's outfit holds the jacket, jeans, jumper, boots).
- The log names Tom (7 Oct, 26-30 Oct, 2 Nov) and Ron (7 Oct, 7-8 Nov); whether they are one person: unread (task text only).
- Ron's plain outfit, third try, 7 Oct is 1.99 M (time-log 32-33, shared with records and the CC0 route; earlier tries not itemised; set aside). Against it the six dress-the-cast windows are 5.81, ratio 2.92.
- The review-kind field has 31 starts in the whole log; table rows use only windows whose text names the piece.
- UC states the shop and garment figures are medium and low confidence (UC lines 9, 10).

## 2. Kinds named in the brief with no repeat, or nothing logged

| Kind | What the sources show |
|---|---|
| Roof piece | One piece, no repeat: the corner's roof, 5 Nov, step 9d 0.52 (484-485), roof try 2 0.13 (486-487), roof breaks 0.38 (488-489): 1.03 M. PD line 19 says "roofs already street-wide (1.1 h measured)"; its source was not found in the files read: unverified |
| Room | One room: Mickey's front office, 6-8 Oct, 1.1 windows 22-27 (7.54 + 3.01 + 13.21 = 23.76 M, each window also holds gate fixes and rounds), later office work in many mixed windows. No second room. Near shop rooms: PD line 14, 8 to 16 h guess (not E from a record) |
| Sign | Not logged. "lettering" appears inside one mixed window (24-25, 3.01 h). PD line 12: signage 6 to 10 h guess |
| Face | Not logged as hours. Darren's S6 face in the game 2 Oct (RM line 96, commit 74dbd477f, commit evidence only). Ron's face not boundable (RM step 2) |
| Voice | Not logged by window. RM: Ron's and Darren's voice hours "not recorded" |
| Hair | "n02-tom-hair-crown" 3 Nov, 364-365 (1.33) and 368-369 (0.77): 2.10 M in two windows of one piece; PD line 36: hair 6 h this week (order) |
| Person's routine | None measured (UC line 11; JSON person_routine) |
| Wear pass on a finished front | One: chandler front wear, D11, 30 Oct, 1.77 M (306-307) |
| Corner (a street's first corner) | One: about 12.6 h, a reviewer's rough sum, I (PD line 19, 116); not recomputed here |

## 3. Estimates for the next instance (E, no window yet)

| Kind | E figure | Source |
|---|---|---|
| Shop fronts, fishmonger and empty unit | 16 to 37 h for both | PD line 10 |
| Mickey's front dark at night | about 2 h | PD line 11 |
| Dressing: Darren | 6.3 h E, with Sheila's remainder 6.3 to 16.6 h E | PD line 37 |
| Dressing the props, under 30 m left | 3.5 to 7 h | PD line 31 |

## 4. The week's logged hours, 2 to 8 November, by the log's kind field

Windows whose start falls on 2 to 8 Nov (time-log lines 325 to 596, 272 lines). A window with no stop is counted to the next start (six such: starts at lines 341, 504, 513, 528, 553, 554).

| Kind | Windows | Hours |
|---|---|---|
| production | 117 | 53.53 |
| review | 21 | 3.49 |
| Total | 138 | 57.03 |

By day (production / review): 2 Nov 12.55 / 0; 3 Nov 13.57 / 2.20; 4 Nov 3.25 / 0.12; 5 Nov 5.62 / 0; 6 Nov 7.14 / 0.89; 7 Nov 6.69 / 0.28; 8 Nov 4.71 / 0. The log's kinds are only "production" and "review".

**Rows that could not be assigned.** No start row lacks a kind (0 of 139 starts in the week). One window of two rows could not be counted: lines 569-570, "n02-9-pass-is-players-launch", start 8 Nov 08:50:00, stop 08:34:00, a negative window of -0.27 h, left out of both totals. Of the week's 272 lines, 139 are starts and 133 are stops; 138 windows are counted.

**Not assigned to a piece kind.** The log's kind field has no piece kinds. Of the 138 counted windows, the table rows above use the windows listed in their source column; the rest were not assigned to any row of section 1.

## Unread or unreached

- RECIPE.md Cost lines (behind every R figure) were taken from UC/JSON, not re-read.
- Hours before 5 Oct and in the log's gaps (8 Oct 16:10 to 23 Oct 15:15; 26 Oct 11:03 to 27 Oct 02:58; 28 Oct 14:26 to 29 Oct 11:28): not logged.
- Token dollars: not part of this table.
