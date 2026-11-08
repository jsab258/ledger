# Talk cost per person (8 November 2026)

Step 5 of RON-END-TO-END-PLAN-2026-11-08.md. No paid run, no API call; existing logs only, read 8 Nov 2026.

**Does the closing cost line split by speaker? No.** It splits by model only: CostTracker keeps one bucket per model name (ledger/Assets/Scripts/Core/CostTracker.cs:9-24, Report at :46-55, EstimateUsd at :31-44), and the closing line (ledger/TalkHelper/Program.cs:1682-1696) writes cost (that per-model report), usd, calls, cacheRead, cacheWrite, budgetSpent, budgetRefused; the call recorded at Program.cs:1010 passes model and tokens only. production/api-spend.jsonl (19 lines, line 1 is its description) carries day, at, what, usd, calls, source, item per run, never a speaker.

The speaker is named only on each reply line of a run's talk-transcript.jsonl (field `to`: sam = Darren, lena = Sheila, rocco = Ron; names per production/research/voice-latency/IN-GAME-2026-11-02.md:9) beside the reply's model. Those lines carry no per-reply calls, tokens or dollars (their `calls` field is what the person calls the player).

## Table

| Speaker | Calls | Tokens | US$ | Source | Tag |
|---|---|---|---|---|---|
| Ron (Ron Kirby, rocco): calls, tokens, dollars by speaker | not recorded | not recorded | not recorded | Program.cs:1682-1696; CostTracker.cs:9-24; production/api-spend.jsonl (no speaker field) | not recorded |
| Darren (sam): calls, tokens, dollars by speaker | not recorded | not recorded | not recorded | same | not recorded |
| Sheila (lena): calls, tokens, dollars by speaker | not recorded | not recorded | not recorded | same | not recorded |
| Ron: replies, runs H, I, J, K (7 Nov, build e998e06, 30 lines each) | not recorded | not recorded | not recorded | 40 of 120 replies; F:/LedgerTools/latency/askreal-2026-11-07{h,i,j,k}/talk-transcript.jsonl, field `to` = rocco | measured (replies only) |
| Darren: replies, runs H to K | not recorded | not recorded | not recorded | 40 of 120 replies; same files, `to` = sam | measured (replies only) |
| Sheila: replies, runs H to K | not recorded | not recorded | not recorded | 40 of 120 replies; same files, `to` = lena | measured (replies only) |
| Ron: share of cost, runs H to K | 135+122+114+139 = 510 calls in all four runs; Ron's share about 170 | not recorded | 0.2952+0.2587+0.3638+0.2479 = 1.1656 in all four runs; Ron's third about 0.389 | closing lines in the same transcripts and api-spend.jsonl lines 16-19; times 40/120 | inferred (equal share of replies; assumes each reply costs the same, which is not recorded) |
| Darren: share of cost, runs H to K | about 170 of 510 | not recorded | about 0.389 | same | inferred |
| Ron: per hour of play | not recorded | not recorded | about 0.04 an hour (0.12 at 15 replies x 40/120) | COST-PER-HOUR-2026-11-02.md:20 (run D, $0.12 at 15 replies, divided by lines asked, not replies; 0.16 by replies per SPEECH-BENCH-SKILL-REVIEW-2026-11-02.md:28) x Ron's replies share in runs H to K | inferred |
| Darren: per hour of play | not recorded | not recorded | about 0.04 an hour (same arithmetic); his real-question replies ran on Sonnet 5, so an equal share understates him | same | inferred |
| Darren, Sonnet 5 replies, run E (3 Nov) | not recorded | not recorded | not recorded | 10 replies, all `to` = sam, model claude-sonnet-5; the run's 91 calls and US$0.3367 are the whole run (api-spend.jsonl:9) | measured (replies and model); cost not recorded |

## Reply counts by speaker in every readable run (scripted -AskScript/-AskSet runs)

Replies = transcript lines with a `reply` field. Closing line = calls, usd (the talk program's own price estimate).

| Run | Replies | Ron | Darren | Sheila | Closing line |
|---|---|---|---|---|---|
| 2026-11-02b | 15 | 6 | 2 | 7 | 53, 0.3293 |
| 2026-11-02c | 23 | 10 | 3 | 10 | 74, 0.2183 |
| 2026-11-02d | 23 | 3 | 10 | 10 | 86, 0.2415 |
| 2026-11-03e | 25 | 9 | 10 | 6 | 91, 0.3367 |
| 2026-11-04f | 30 | 10 | 10 | 10 | 130, 0.3664 |
| 2026-11-07h | 30 | 10 | 10 | 10 | 139, 0.2952 |
| 2026-11-07i | 30 | 10 | 10 | 10 | 122, 0.2587 |
| 2026-11-07j | 30 | 10 | 10 | 10 | 114, 0.3638 |
| 2026-11-07k | 30 | 10 | 10 | 10 | 135, 0.2479 |
| All readable (236 replies; the 3 Nov to 7 Nov six runs: 175 replies, Ron 59, Darren 60, Sheila 56) | 236 | 78 | 75 | 83 | not summed |

Unread: F:/LedgerTools/latency/askreal-2026-11-02 (no talk-transcript.jsonl) and askreal-2026-11-02e (no replies, closing line 0 calls). Runs before 2 Nov and the bench runs (production/playtest/talk-runs.jsonl, 97 lines: date, what, turns, calls, tokens by model, usd; no speaker field) name no speaker. 24 of the 236 replies in the readable runs have no model recorded (timed out or fell back).

Method: replies counted from each talk-transcript.jsonl with a short script reading the `to` field; no key, .env or call involved.
