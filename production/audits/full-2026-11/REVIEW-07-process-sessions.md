# Review 07: process and sessions (full audit, November 2026)

One fresh reviewer, read only, 19 Nov 2026. Read: INVENTORY.md, DECISIONS-TRACE.md (tested, not trusted), canon.md, RULINGS.md, CLAUDE.md, NOW.md, TOWN.md, CLOTHES.md, FOR-JAFAR.md, FINDINGS.md, RECIPE.md, NOTEBOOK.md (size and history only), production/handover/, production/handovers/, production/lane/, .claude/, .githooks/, tools/hooks/, the process tools, the token-audit files, the scheduled-task summary, the 273 advisor rows, 261 acks and 87 page picks, and git history.

## Summary

The studio has built a large machine for running itself, and the machine now disagrees with itself. Fifteen places say how the work is done. The file every session and helper loads first, CLAUDE.md, has not changed since 4 Nov and contradicts at least nine of his later rulings, so helpers act on old rules and the session corrects them by hand. The process costs a lot and is not measured: the 15% line counts only edits to record files, the time log has no kind for process work, and yet about 37 of his 87 page taps and about 60% of 273 advisor messages were about the studio's own setup, not the game. The hourly hand-over between sessions cost about 62 idle hours from 12 to 16 Nov, and he or the advisor raised stopped work at least six times. The rulings check reports all 85 standing rules "enforced", but 33 of them rest on a Monday audit that has not yet run in its new form, and the rest mostly pass if a phrase appears in a file. Nothing in the process looks at the game as a whole, which is why he had to say on 18 Nov "we had all those discussions months ago. Seems like we drifted" and "again, we dont want a gossip simulator". Main has not moved since 5 Oct. The proposed ends are mostly fewer, truer rules in one home, with checks that run.

## Findings, ranked

### 1. The rule book disagrees with itself, and the stale rules reach the helpers (high)

Impact: high. Helpers and fresh sessions follow rules he replaced weeks ago; the session spends effort correcting them, and an outsider cannot tell which rule holds.

Evidence:
- CLAUDE.md last changed 4 Nov (git log: 8db3212b4, 9a3516365). Since then it contradicts RULINGS on: tries, "a third try needs his yes" (CLAUDE.md:53) against RULINGS.md:27 "None asks him"; his share, "20% kept for him" (CLAUDE.md:16, also CHARTER.md Constraints) against RULINGS.md:37 "the last 10% shared with him"; orders "about 1,200 words" (CLAUDE.md:17) against orders of 28,226, 8,026, 6,353 and 3,599 words (production/orders/2026-10-25 to 2026-11-16); FOR-JAFAR.md and the overview (CLAUDE.md:32-33) against RULINGS.md:36 "No FOR-JAFAR.md"; RECIPE.md as the notebook and "no recipe tests" (CLAUDE.md:36) against RULINGS.md:36 (NOTEBOOK.md; monthly cold re-run); "Mafia or Kingdom Come II ... their files on demand" and "Mafia's missing numbers fetched" (CLAUDE.md:51-52) against RULINGS.md:53 (outside only; KCD2 the bar, Mafia never the yardstick); "a full disk: stop and wait" (CLAUDE.md:67) against advisor 189 (DECISIONS.md, 17 Nov: no idle); "never unattended lanes" (CLAUDE.md:15) against the cloud lane running hourly with automatic approval (scheduled-tasks summary, entry 2).
- The old tries rule also sits in RECIPE.md:10 ("then research and the owner's yes"), which is "read before any first try", and in five skills: asset-import:17, game-garment:12, gate:14, packaged-walk:16, shopfront:15. The Mafia-first rule sits in RECIPE.md:7, tools/order_ledger.py:23 and :108, game-garment:10, shopfront:10 and LANE-HANDOVER.md:27 (whose own header says the opposite).
- The session knows: HANDOVER.md:29 "Helpers quote CLAUDE.md's 'third try needs his yes': correct them"; DECISIONS.md:420 (18 Nov 13:13) "the helper's 'needs his yes' is CLAUDE.md's older rule".
- Why it persists: CLAUDE.md sits at 1,622 of its 1,625-word cap (doc-caps), his words are not trimmed (DECISIONS archive, 21 Oct 12:55), so new rulings are written into RULINGS "over CLAUDE.md" (RULINGS.md:36) and the old line stays.
- The fifteen homes: CLAUDE.md, RULINGS.md, HOURLY-TASK.md (929 words), HANDOVER.md's standing list, LANE-HANDOVER.md, lane-prompt.txt, SCHEDULED-TASK-PROMPT.md, LANE-RULES.md on F:, seven agents, nine skills (about 29,000 words), RECIPE.md chapter 0, each order's week rules, CHARTER.md, the advisor's running-list doc, rulings-enforcers.json.

Proposed end: rule. How the work is done has one home, RULINGS.md. CLAUDE.md keeps only the project facts and where things live; skills and RECIPE.md point at RULINGS lines instead of restating them. A ruling that changes a rule changes every copy in the same commit, and a check fails on any text that says "over CLAUDE.md" or quotes a superseded rule (start with the third-try and Mafia-files wording).

### 2. What he had to raise himself, and the missing check behind each (high)

Impact: high. This is the heart of his 19 Nov complaint; each point cost his attention, often more than once.

Evidence (date he raised it; the check that should have caught it first):
- 9 Nov 08:35, never film or perform, "said many times" (advisor 51). Check: none refused plans that needed his body; needs_you_page.py's ACTION guard came 17 Nov.
- 9 Nov 07:32 and 17:25, 11 Nov 07:10 and 17:45, sessions idle or stopped at night, "can't have that again", "Silence again ... the watchdog woke him at 17:22" (advisors 44, 63, 92, 104). Check: no idle alarm (finding 4).
- 9 Nov 13:50, "should not have required my pushback; research was sloppy" (advisor 59). Check: CLAUDE.md:50's fresh reviewer never tests a negative finding; the promised rule was then lost (finding 7).
- 14 Nov 21:11, the session on Fable all day, "Major fuckup, can't happen again" (advisor 162). Check: no start check read the model until that night.
- 16 Nov 12:16 and 12:24, page items about deleting the session's own leftovers, already settled by RULINGS 29 Oct; the Marvelous bridge, "Clicked that many times in the past" (advisors 173, 174). Check: RULINGS line existed, no guard on the page tool.
- 17 Nov 12:36, "how the fuck are we running out of space all the time?" after F: hit its floor five times in four days (advisors 173, 196). Check: retention.py measured each hit; nothing treated a repeat as a fault.
- 17 Nov 16:38, "I had to tell you now to find a way to enforce this" (advisor 205). Check: CLAUDE.md:43 has asked since October for each rule to get a check.
- 18 Nov 15:19 and 16:02, "we had all those discussions months ago. Seems like we drifted" and "But again, we dont want a gossip simulator" (advisors 224, 226). Check: none. Phase exits and the gate judge pieces against pictures; no process step asks whether the work points at canon's pillars and his direction. CHARTER.md's goal is still "Thirty minutes of Quay Street".
- 18 Nov 16:43, Mafia is not the measuring stick (advisor 229). Check: CLAUDE.md, order_ledger.py and skills still name Mafia first (finding 1).
- 18 Nov 21:37, "We got distracted by other equally important but less urgent things" (advisor 232). Check: the waiting-list rule (finding 6).

Proposed end: rule. The Monday audit opens with one question: what did he raise this week that a check should have caught? Each answer names the check added that week. Each phase exit and each order carries one paragraph, by a fresh reviewer, on whether the week's work moves the game toward his 18 Nov direction (verbs first; exciting, immersive, novel), not only whether pieces passed.

### 3. The process costs a lot and the studio does not measure it (high)

Impact: high. His first philosophy since 11 Nov is efficiency, with records and process under about 15% (RULINGS.md:23); he cannot see that number.

Evidence:
- The "records" share counts only edits to record files (tools/token_audit.py:57 and :153). Gates, pace readings, hourly rows, advisor reads and acks, handovers and the DAILY files are counted as building or, for production/research/token-audit, as research (token_audit.py:58). It reported records 4% on 18 Nov (DAILY-2026-11-18.md:15).
- tools/timelog.py:33 allows only "production" and "review". Since 12 Nov the log holds 134 production entries, 7 review and 43 automatic "session startup" starts filed as production on item n16-1.
- What can be counted: 273 advisor messages and 261 acks in 15 days; a keyword count puts about 164 of the messages mainly about the process. Of his 87 page picks, about 37 were about sessions, starts, gates, models, pace, disk and settings, and 9 more asked him for third tries, against about 10 whole looks or game-direction items. About 14,200 lines in 45 process tools (28% of the 51,127 lines of tools/*.py); 3,194 lines only to hand sessions over; 213 rewrites of HANDOVER.md since 4 Nov; 827 of 1,069 commits since 20 Oct touch process files. This audit itself is about 8 to 15% of a week (advisor 237).
- Total process share of spend: not recorded.

Proposed end: rule. The time log and token_audit.py get a "process" kind (gates, rows, pace, advisor, handovers, audits, his page, records), reported each Monday against the 15% line, with his taps split into game and setup.

### 4. The hourly hand-over machine cost tens of idle hours (high)

Impact: high for the game: idle hours in a paid week, and repeated alarms for him.

Evidence:
- Idle by the gate's own measure (tools/idle_gaps.py, the DAILY files, line 7 or 39): 12 Nov 553 day and 138 night minutes; 13 Nov 561 and 130; 14 Nov 470 and 197; 15 Nov 747 and 257; 16 Nov 463 and 235. About 62 hours in five days, about 49 of them "handover wait" (the weekend partly planned). After fixes: 115 minutes on 17 Nov, 190 on 18 Nov.
- Causes found only after the fact: the gate read the row's "Next due" time as a quiet spell, 196 of 240 day minutes on 16 Nov (IDLE-GAPS-2026-11-16.md:27); the night pause came back because fresh_gate.py coded a lapsed end date (advisor 92, 11 Nov); sessions ended without a Stopped line (advisors 92, 104).
- fresh_gate.py changed in 20 commits this month; the design is RULINGS.md:41 (one session at a time, switched by history size).

Proposed end: rule. An idle gap over 20 minutes while the order has open items is a fault the gate itself raises within the hour (a row and a fix), not a figure in the next day's DAILY file; a gate change ships with a test row for every hour of the week.

### 5. "Enforced" mostly means written down (high)

Impact: high. His rule on rules (17 Nov) asked for code, not memory; the check gives false comfort.

Evidence:
- python tools/rulings_check.py prints "rulingsCheck lines=85 enforced=85 faults=0". 33 of the 85 entries in production/rulings-enforcers.json name only "monday-audit". The new-form audit first runs 23 Nov (scheduled-tasks summary, entry 3); the last MONDAY-AUDIT file is 2026-11-09, none for 16 Nov.
- A file enforcer passes when the phrase appears anywhere in the file, comments included (tools/rulings_check.py, enforcer_fault).
- Example: the 8 Nov models line says "never a general-purpose helper" and is listed as enforced by settings_check.py; on 18 Nov catch-all and general-purpose helpers took about 62% of US$503 (DAILY-2026-11-18.md:21-25), two days after "From now no general-purpose" (DAILY-2026-11-16.md:31). No tool checks for it.
- The 9 Nov "DECISIONS.md one line, about 40 words" has no check (median 83 words in the trace's sample; doc-caps.py:45 "had no cap").
- The daily backstop task checks for "Enforced by" in RULINGS.md (scheduled-tasks summary, entry 1); RULINGS.md has none, by design (DECISIONS 17 Nov).
- A check that cries wolf: settings_check reports "wrong=1" for final-reviewer at high effort (DAILY-2026-11-18.md:38) while HANDOVER.md's standing list sanctions high until 23 Nov.

Proposed end: rule. An enforcer counts only if it runs and its self-test fails on a planted breach; the judgement-only lines are listed in each Monday audit with a yes or no per line; the backstop's text and settings_check's expected values follow the rulings in force.

### 6. In-week change is the norm, and the order is no longer a plan (medium)

Impact: medium. The Kiln and Marvelous deadline slipped behind additions, in his own words.

Evidence: CLAUDE.md:17 "Between them nothing new unless something is broken"; CHARTER.md Authority (a scope change states what it displaces and its cost). This week: Kiln's share 23% in the order (orders/2026-11-16.md:22), about 50% (DECISIONS.md:228, 16 Nov 22:00), 70% (RULINGS.md:39); a second session from 17 Nov; Fable from 20% to 40%; the prototype synthesis (18 Nov 20:47); this audit (19 Nov 00:18); three changes to the pace rule in about 26 hours (advisors 231, 236, 237; commit 345772ac4). 84 advisor messages 16 to 18 Nov. The order builder task still says "about 1,200 words at most" (scheduled-tasks summary, entry 4).

Proposed end: rule. Any in-week addition, his included, starts only with one line in the order's ledger, "displaces N hours of item X", and order_ledger.py fails the push without it.

### 7. Promises are acknowledged and then lost (medium)

Impact: medium. He believes a thing is in hand that is not.

Evidence: the negative-finding rule, ack of 9 Nov 15:33: "goes into the next batch on his page as one tap"; no page item, verdict or text in RULINGS, CLAUDE.md, agents or skills (searched). The verdict-only Kiln helper trial, "judged 18 Nov" (DAILY-2026-11-16.md:36); no verdict in DAILY-2026-11-18 or DECISIONS. The Cascadeur decision of about 25 Nov is tracked nowhere (trace, D-E-051). His own rule of 14 Sep, "A ruling that orders work to the queue names the item by number, and something checks the item exists", is itself lost (trace, D-G-078).

Proposed end: rule. Every ack that promises later work names an order or waiting-list item id; the backstop fails on a promise without one, and on an item past its date.

### 8. Main has not moved since 5 October (medium)

Impact: medium. "Passed review" has no home; reviewed and unreviewed work sit on one line.

Evidence: origin/main is 5437820f0 of 5 Oct ("UE machine probe from 17bf9da1"), confirmed against the remote on 19 Nov; 1,840 commits on wip are not on main. CLAUDE.md:64 "main gets only what passed review"; .claude/settings.json allows a push to main; tools/branch_check.py:29 exempts main and wip, so nothing fails.

Proposed end: rule. Of two fine ways, the cheaper: CLAUDE.md names wip as the one line and drops main's promise, with passed items marked in the order's ledger; or main receives each phase exit. Either way a check fails when the text and the branches disagree.

### 9. Files that describe October (medium)

Impact: medium. NOW.md points sessions at them; they mislead and add reading.

Evidence: TOWN.md last changed 5 Oct ("not started before phase 1 passes"; phase 1 closed 9 Nov; the town simulation is frozen, RULINGS.md:38). CLOTHES.md last changed 7 Oct ("Blender only", "Tailoring waits", "State, 7 October: failed") while the week is Kiln and Marvelous drapes; NOW.md:9 still says "n16-2 Ron as one complete person (CLOTHES.md)" and its Handovers line names both. production/handovers/ holds 13 port cards from the three-session era, last changed 7 Oct except talk.md. FOR-JAFAR.md (3,511 words) is kept with "Stopped 9 Nov". NOW.md:12 lists n16-9 and n16-11 as open, though both moved to the waiting list on 16 Nov 21:16 (orders/2026-11-16.md:89, :91). HOURLY-TASK.md:3 still says "Hourly from 05:15 to 00:15" (last changed 9 Nov) against his 15-minute, round-the-clock starts (verdicts fifteen-minute-start and schedule-fifteen-minutes, 11 Nov).

Proposed end: deletion. Move TOWN.md, CLOTHES.md, FOR-JAFAR.md and production/handovers/ into production/archive/ with one line each; safe because no rule or gate reads them as instructions (two tools name the handovers folder, tools/route_week_check.py and tools/art-recipes/terrace-front.py, and need their path updated in the same commit). NOW.md points at the order and the Kiln checklist, and its two moved items leave.

### 10. The live instructions are not in the repository (medium)

Impact: medium. Nobody, this audit included, can check what text actually drives the sessions.

Evidence: the production task's live text is its SKILL.md under the app's scheduled-tasks folder on his PC (advisor 95, 11 Nov); HOURLY-TASK.md is a copy, stale on its cadence (finding 9). The production task does not appear among the five LEDGER scheduled tasks read on 19 Nov (scheduled-tasks summary). Kiln's lane rules and LOOP.md live on F: (HANDOVER.md standing list); the running list doc and the advisor's standing prompts live in claude.ai.

Proposed end: rule. Every text that drives a session has its home in the repository; fresh_gate.py compares the live scheduled-task text with it at each start and refuses to go on a difference.

### 11. The cloud lane makes nearly as much intake work as it saves (medium)

Impact: medium, and a money question for him: a second session draws on the same allowance.

Evidence: its own count, 29 items with about 67 actions for the main session and about 15 picks for his page in one evening (LANE-SHARE-PROPOSAL-2026-11-18.md:9, :54), against one phone screen of three decisions; intake estimated at 10 to 15 main-session hours, "as much as the lane's whole share" (:39). Its handover still shows "Done: (nothing yet)" after 16 runs (LANE-HANDOVER.md:36-37), and its rules line keeps the Mafia rule (:27). RULINGS.md:37 ends the lane on 23 Nov.

Proposed end: ruling for him. Keep the cloud lane after 23 Nov? A: four more weeks, only items whose result lands without main-session work (cloud-tested code, files the order names), judged by intake under 25% of its hours (recommended); B: stop on 23 Nov; C: open-ended.

### 12. Word caps now force cramming, not pruning (low)

Impact: low on its own, but it is why stale lines survive (finding 1).

Evidence: tools/doc-caps.py on 19 Nov: CLAUDE.md 1,622 of 1,625, RULINGS.md 4,899 of 4,900, FINDINGS.md 2,000 of 2,000 and 20 of 20 entries, PLAN.md 1,200 of 1,200, CATALOGUE.md 1,499 of 1,500. CLAUDE.md:31 says its own cap is 1,000. FINDINGS.md's second entry runs to 1,989 characters and bundles about fifteen faults from 3 Oct to 4 Nov, so "at most twenty" counts bundles; the hill-haze fault has been open since 3 Oct.

Proposed end: rule. A file at its cap is pruned of done and superseded lines, never compressed; FINDINGS.md holds one fault per entry, and a fault older than 30 days is either on the order or closed as a listed known shortfall.

## The brief's questions, mapped

Same game: finding 2. Still true: findings 1, 8, 9. Used or dead weight: finding 9. Cost: findings 3, 4. Missing: findings 2 to 5. Contradictions: findings 1, 5, 9. Raised by him: finding 2.

Not reached: the live scheduled-task texts on his PC, LANE-RULES.md and LOOP.md on F:, and the advisor's running-list doc.
