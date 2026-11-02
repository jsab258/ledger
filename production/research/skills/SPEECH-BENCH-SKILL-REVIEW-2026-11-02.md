# Review of the speech-bench skill, 2 November 2026

One fresh reviewer checked .claude/skills/speech-bench/SKILL.md against its source files. The reviewer was general-purpose and read only: no game, Unreal, talk program or paid call; no clicks, computer use or UI Automation; the key never opened. The sources were:
- the voice-latency notes (IN-GAME-2026-11-02 in full, REMEASURE, SPEECH-LEVERS, POCKET-SWITCH);
- the invented-claims notes (SOURCE-TEST, LOCAL-CHECKERS);
- the cost notes (SUMMARY, COST-PER-HOUR);
- api-spend.jsonl's fields, the order of 2 November, PLAN.md, and RULINGS.md and DECISIONS.md on speech;
- the code: TalkHelper Program.cs, ConversationEngine, TalkMoment, LlmClient, BudgetedClient, CostTracker, ClaimCheck, ClaimBench, CrimeProbe.cpp;
- the tools: latency.py, slow_turns.py, early_looks_ab.py, talk_cost_sample.py, tools/checkers, play.py, publish-talk-helper.ps1, ci-checks.sh;
- the voice-engines, fast-checker and retention specs;
- the named memory notes;
- the run folders of 2 November on F:.

**Verdict: PASS WITH FIXES.** About 90 claims were checked: 9 were wrong or unbacked, 7 imprecise and 8 points missing. There were no setting or key leaks. Before applying anything, the builder re-checked these against the files:
- BudgetedClient's settlement;
- run D's transcript: 20 replies on Haiku 4.5 and 3 with no model; 7 walkedOff rows;
- the walk-off lines in the logs of runs B and D;
- run D's full command line and the sizes run's command line (-AskScript=12, no -AskReal);
- ClaimBench's `--cap` default;
- talk_cost_sample.py's LIVE_DAILY_USD;
- LOCAL-CHECKERS' 17M table and its timings with the voice running;
- fast-checker.json's answerWithinMs;
- api_batch.py's BILLING_DAY.

## Wrong or unbacked (all applied)

1. Step 8 said budgetSpent reads higher because each call reserves its whole output allowance. BudgetedClient settles every reserve to the tokens actually used, stopped streams included. Only failed calls keep their reserve, and calls stopped before any answer are charged an estimated prompt. COST-PER-HOUR carries the same error. Run D's gap (0.327 against 0.241) is unexplained, so which figure the bill follows is now "check first", and both figures are logged.
2. Step 8 divided by replies. COST-PER-HOUR divides by lines asked ($0.2415 / 30 = $0.0080; $0.12 an hour). Divided by run D's 23 replies, the hour would be about $0.16. The skill now says which divisor and asks for it to be named.
3. Step 8 put three levers on the waiting list. n02-9-talk-cost-levers holds two (caching, Haiku 5.5). Fewer calls per reply is ranked in COST-PER-HOUR but is not on the list.
4. Step 7 gave the fast checker the bar "no more invented through than Haiku alone, within 0.15 s". At his open cut-off it misses both bars, and he chose that trade-off knowingly from a table:
   - 36.0 against 34.1 per 300 (2 more per 617);
   - 3 to 4% of answers over 0.15 s with the voice running.

   The skill now describes his trade-off table and the 400 ms answer limit (answerWithinMs).
5. "Always" said -unattended runs get the stand-in. With -unattended and no -TalkHelper=, no talk program starts at all (LiveHelperStart). LiveTalkPlayed tests -AskScript, -AskReal and the cap before it tests -unattended, so such a run naming -TalkHelper= uses the key. The skill now forbids those switches on unattended runs.
6. Step 4's check cited run A for budgetRefused. Run A kept no end line, and budgetRefused was 0 in runs B to D. The source is now the code (BudgetedClient.Refused).
7. Step 4's command line was incomplete. Run D's log also has -TalkHelper= and ends -ForceRes -nosplash. The skill now gives it whole.
8. Step 5 cited Program.cs for which model is which. The source is now TalkMoment.ModelFor with LlmClient.cs Models.Core and Models.Ambient.
9. "Always" cited RULINGS for "no voice moved without his yes". "Moved" comes from voice-engines.json's "about" line, which is now cited apart.

## Imprecise (all applied)

1. Step 5: the transcript's "model" is null for any reply the model did not write. It stays the moment's model when a second draft is escalated, and escalations show only in "re-" steps and in the end line.
2. Step 4: each person always gets the same two lines, so per-person figures are per-question figures.
3. Step 2: talk_cost_sample.py --sizes sends its own sample with no evidence record. The game's sizes came from -AskScript=12 without -AskReal and with LEDGER_TALK_SIZES set.
4. Step 3: ClaimBench `--cap` defaults to 1.00 a run, and a task's money left counts every earlier run in talk-runs.jsonl. The task must be named in the code or be today's measure-date. The stale $1, in KeyRuns.cs and in talk_cost_sample.py's LIVE_DAILY_USD, is settled by RULINGS 1 Nov. So it is now a fault to list in FINDINGS.md, not a "check first".
5. Step 7: checktime needs `--task` and `--from` with folders from earlier `firsts --early` runs. slow_turns.py reads those bench folders, not game transcripts.
6. Step 6: alternating 40 lines or more an arm is the method beside the game. Inside the game one run holds one talk program, and try 2 was not alternated. How to alternate inside the game is now "check first".
7. Step 8: Haiku 4.5's price line carries no read date of its own.

## Missing (all added)

1. Step 5's "check first" on real questions is partly settled by the sources. By the game's own rule (TalkMoment.Of, TalkRules.ConceptOf), the six -AskScript lines are small talk: in run D all 20 replies the model wrote were Haiku 4.5's. So -AskScript as built does not measure the bar RULINGS sets (a newcomer's real questions), and IN-GAME-2026-11-02's "bar met with D" is small talk only. The newcomer question set is in ClaimBench `firsts`.
2. Walk-offs. In every run of 2 November one person was asked from 7 to 29 m away, and the log shows "walked away" after their lines. In run D, 7 of one person's lines left only walkedOff rows. Step 4 now counts them and leaves them out.
3. The stop rule: PLAN's exit ends "else the stop rule", and CLAUDE.md says to report a failed capability plainly.
4. Speech's two tries are spent (DECISIONS 1 Nov 21:31 and 2 Nov 07:41). Another try needs his yes first.
5. A fresh reviewer is needed before any result or target reaches his page (CLAUDE.md, the research method). IN-GAME-2026-11-02 had none.
6. tools/api_batch.py --dry prints today's ceiling from api-spend.jsonl with no key. It assumes the billing month starts on the 12th, so the skill marks it "check first". (This tool was found outside the listed sources.)
7. The switches for an arm: `--first-model` or LEDGER_TALK_FIRST_MODEL, LEDGER_CHECKER_MODEL (latency.py `--checker`), and LEDGER_TALK_FAKE. latency.py --live has no CI refusal of its own.
8. The fast checker loads in the background, and lines sent before it is ready go to Haiku alone; this is why runs beside the game wait 60 s. The game's log does not show when it was on.

## Not changed

- The reviewer noted a naming risk: an unrelated bench at ledger/SpeechBench. The skill keeps the name the order gives it ("the speech bench"); it lives under .claude/skills/, where nothing collides.

## Backed

- the CheckAsync order, the 552 of 617 lesson, KnownOnlyLines and the 8 s timeout;
- the end line's fields, BudgetedClient's worst case and its rate for unknown models;
- the switches -AskReal, -PreparedAck, --fake, LEDGER_TALK_SIZES and LEDGER_FAST_CHECKER=0;
- the publish command, run figures A to D, POCKET-SWITCH's timings and the 1 November mend;
- the retention.json gap for F:/LedgerTools/latency;
- api-spend.jsonl's fields, the self-test counts and the ci-checks lines;
- RULINGS D48, 7, 23 and 28 Oct and 1 Nov.
