# Fresh hourly sessions: counts, Mon 9 Nov 13:00 to Wed 11 Nov 12:00 Swiss (advisor 96)

Counts only. Dollars are API-price measures (tools/token_audit.py PRICES, one count per message id), not a bill. Window ends at the last logged step, 11 Nov 12:00. One log = one session; a resumed log (06d657ae, 19:07 to 21:41 on 9 Nov, three Started lines) counts once. The 11:21 session on 11 Nov is the one still running.

## 1. By day: history share and dollars per step
History share as token_audit defines it: the part of each step above its own log's first step, at the cache-read price, over cost. "Total" includes helpers; "session" is the session's own steps only.

| Period | Session steps | Session $ | $ per session step | History share, session steps | Helpers $ | History share, total |
|---|---|---|---|---|---|---|
| 26 Oct to 1 Nov | 8,505 | 1,112.43 | 0.131 | 73% | 1,038.20 | 53% |
| 2 to 8 Nov | 8,457 | 869.38 | 0.103 | 49% | 500.83 | 40% |
| Mon 9 Nov (from 13:00) | 449 | 31.43 | 0.070 | 33% | 127.96 | 17% |
| Tue 10 Nov | 890 | 56.70 | 0.064 | 28% | 29.57 | 26% |
| Wed 11 Nov (to 12:00) | 896 | 64.12 | 0.072 | 38% | 18.81 | 35% |
| 9 to 11 Nov | 2,235 | 152.26 | 0.068 | 33% | 176.35 | 24% |

Mon 9 Nov helpers' $127.96 is mostly one session's batch (0e7a84ad: 632 helper steps, $144.53 over its whole run).

## 2. Production sessions (25 logs with real steps; 5 of them also ran helpers)
Stop reason, by the last turns and the Stopped line: history line = history_check run and Stopped written for history; pacing = Stopped written with history UNDER (handover: "small pieces only", "nothing new"); hard stop = context at or past 400k: none reached (highest peak 360,671).

| Reason | Sessions | Minutes (mean / median / sum) | $ each (mean) / sum, with helpers | Peak context mean | History share |
|---|---|---|---|---|---|
| History line | 8 | 72 / 55 / 578 | 14.10 / 112.81 | 315k | 36% |
| Pacing stop, history UNDER | 11 | 10 / 4 / 111 | 1.93 / 21.23 | 145k | 19% |
| End of turn without Stopped, or unknown | 4 | 147 / 141 / 589 | 42.38 / 169.52 | 220k | 16% |
| Stopped on his word | 1 | 184 / 184 / 184 | 1.45 | 116k | 4% |
| Running now | 1 | (39 so far) | 13.13 | 333k | 39% |

Unknown/no-Stopped: 8519fb4e (9 Nov 13:22 to 15:52), 0e7a84ad ($144.53 of its $154.29 was helpers), fef05981 (261 min, 220 idle between steps), 2b3659b7.

Session own $ per step by peak context: peak 100 to 200k, 13 sessions, 0.057; 200 to 300k, 6, 0.065; 300 to 360k, 6, 0.070.

Gate-only runs (fresh_gate then stop, 2 to 6 steps, no edits): 24 sessions, $7.09. Four other short logs (3 steps, no fresh_gate), $1.89, not read further.

## 3. Minutes with no production session running
Running = from a log's first to last step, overlapping logs merged. Window 2,820 minutes: 1,394 running, 1,439 in gaps (rounding of overlaps about 13).
- Gaps daytime 07:00 to 23:00: 798 minutes. Night: 641 minutes.
- Gaps over 20 minutes: 20. Two over 200 minutes, both night: 10 Nov 00:33 to 05:21 (288), 11 Nov 01:08 to 05:21 (253). Between 10 Nov 05:27 and 17:21 every gap is 54 to 64 minutes except 13:50 to 14:21 (32): the wait for the next hourly run after a short pacing stop. Others: 9 Nov 18:21 to 19:07 (45), 21:41 to 22:21 (40); 10 Nov 18:45 to 19:21 (36); 11 Nov 06:54 to 07:21 (27), 09:01 to 09:21 (20), 10:25 to 11:21 (56).
- Idle inside logs (steps over 20 minutes apart, counted as running above): 778 minutes (day 610, night 168), 11 gaps, largest 176, 120, 96, 80 minutes. Background jobs in them: not measured.

## 4. Start cost
Rule: dollars from the first step to the first step with Edit, Write, Agent, or a shell command not starting with a read-only word (cat, sed, grep, ls, head, tail, git log/status/diff/show, fresh_gate, history_check and the like). 25 production sessions: mean $0.35, median $0.32, range $0.21 to $1.09; mean 0.4 minute, longest 2 minutes. Together 6.1% of those sessions' own cost.

## 5. Records and reports share
9 Nov 13:00 to 11 Nov 12:00: $23.52 of $328.60 = 7.2% (15% line). By day: 9 Nov 3.2%, 10 Nov 10.3%, 11 Nov 11.6%; 2 to 8 Nov 13.3%; 26 Oct to 1 Nov 7.2%.

## Five lines
1. History share of total cost: 53% (26 Oct week), 40% (2 to 8 Nov), 24% (9 to 11 Nov); in session steps alone 73%, 49%, 33%. Dollars per session step: 0.131, 0.103, 0.068.
2. Sessions that stopped on history ran a mean 72 minutes (median 55), $14.10 each, peak 315k; none reached the 400k hard stop (max 360k).
3. 11 of 25 sessions were short pacing stops (mean 10 minutes, $1.93); 4 ran a mean 147 minutes with no Stopped line.
4. No production session ran 1,439 of 2,820 minutes (798 daytime, 641 night); most 10 Nov gaps 54 to 64 minutes (waits for the next hourly run); a further 778 minutes sat idle inside logs.
5. A fresh start costs $0.35 and under 1 minute to its first real work (6.1% of session cost); gate-only runs cost $7.09 for 24 runs; records share 7.2% against the 15% line.
