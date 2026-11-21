# Red team 2: score (21 November 2026)

The copy: redteam2/GAME-DESCRIPTION-COPY-2.md, made by scripts/rt2_build.py: the "LEDGER, as the player plays it" half of ONE-SHOT-PROMPT.md with tags stripped, run 2's definitions (DEFINITIONS-2026-11-21.md, both parts) and the six GTA VI gap rows folded in as six new sections, internal ids and file names removed, ten parts cut, and every section renumbered after the cut (41 sections, about 22,000 words). The ten cut parts are in planted-2.json, kept outside the helpers' folder and never shown to them. None repeats round 1's ten.

Round 2a used round 1's two briefs unchanged (redteam/BRIEFS.md); fresh Opus helpers, each told to read only the copy.

## Catch rate (planted gaps found)

| # | Planted gap | 2a A | 2a B | 2b A | 2b B |
|---|---|---|---|---|---|
| 1 | Break-ins | A13 | B11 | A11 | B6 |
| 2 | Hold-ups | A14 | B10 | A12 | B5 |
| 3 | Taking a parked car | A30 | B27 | A14 | B38 |
| 4 | Debts and collections | A15 | B40 | A58 | B25 |
| 5 | The sit-down | A17 | B4 | A53 | B16 |
| 6 | Light, noise and time | A40 | B31, B61 | A63 | B54 |
| 7 | Who tells whom (how talk spreads) | A21 | B13 | missed | B1 |
| 8 | Missed rent | A5 | B7 | A43 | B14 |
| 9 | Subtitle options | A74 | missed | A92 | B70 |
| 10 | Live-talk abuse and off-limits typed input | A10 | missed | A27 | B8 |
| | Catch rate | 10 of 10 | 8 of 10 | 9 of 10 | 10 of 10 |

My scoring by keyword and reading; both triage helpers scored the same independently (triage-v2.json, triage-v3.json).

Round 2a's B fell under 9, so the brief was improved once (one generic sentence added to both briefs: check every input path including typed text and what the game does with input it must not accept, and every Settings and accessibility option; redteam/BRIEFS.md) and two new fresh Opus helpers ran (round 2b): 9 of 10 and 10 of 10. Condition 4 is met for round 2b.

## Real gaps not in the map

Round 2a: 181 lines; triage: 24 planted, 38 defined, 5 ruled out, 13 not material, 97 partly (30 material), 4 gaps. Round 2b: 232 lines; triage: 29 planted, 44 defined, 2 ruled out, 40 not material, 113 partly, 4 gaps (all repeats of 2a's). The material ones merge into 22 topics (redteam2/real-gaps-v2.md), now rows RT2-01 to RT2-22, UNDEFINED until written. So red team 2 found material gaps: the gate's count of clean rounds stays at 0.

Pattern: the gaps are no longer whole systems (round 1 found 19, mostly missing systems); they are edges of systems that exist: what happens when the player attacks the police or kills someone the story needs, what moves a rival, how the ending is chosen, and loops that contradict (the cold-store contract and rung 3). Both rounds also flag that many numbers are handed to the tuning table and story content to the story measure; those are counted as owed, not as gaps.

Also noted by all four helpers: section cross-references inside the description point to the old numbers once sections move; the next giant prompt should refer to sections by name.
