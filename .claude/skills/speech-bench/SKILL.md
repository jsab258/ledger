---
name: speech-bench
description: The one way LEDGER measures and improves live talk. The Long Pause (the time from the player's line to the first meaningful speech heard: a median of 2.0 s or less, no prepared openings), invented claims and the claim check, fall-backs and brush-offs, live talk's cost per hour, and the voices' share of the wait. Free screens first (the talk program's self-test, request sizes, the stand-in), then capped paid runs inside the packaged game (-AskScript with -AskReal), old against new, every dollar inside the day's credit and logged. Use it whenever speech, talk, replies, the fact check, the fast checker, Haiku or Sonnet, a model switch, prompt caching, the API credit or spend, a voice's delay, "that's all I know" replies or the cost of talk come up; whenever a talk change is to be timed or a bench is to stand in for the game's check; and whenever someone asks "how long does a reply take?", "is speech under two seconds?", "why did it fall back?" or "what does talk cost an hour?", even if nobody says "bench".
---

# The speech bench

Why: phase 1's exit asks for a median first meaningful speech of two seconds or less, with no prepared openings (PLAN.md; RULINGS 7 Oct). Numbers taken beside the game have misled before. 1 November's 1.17 s was the small-talk model's, while the packaged game sent every line to the larger model and took 2.40 s (production/research/voice-latency/IN-GAME-2026-11-02.md). This skill is shaped like the garment skill (.claude/skills/game-garment/SKILL.md). A change it keeps ends in the packaged-walk skill, and anything for Jafar goes through the his-page skill. Each step names its source: a tool's usage text or code, a research note, RULINGS.md or DECISIONS.md by date, or a memory note by file name (C:\Users\Jafar\.claude\projects\C--Users-Jafar-ledger-local\memory\). "Check first" marks what the sources do not settle.

**Always** (his rulings; none of these bends):
- The bar is judged on a newcomer's real questions inside the packaged game, with small talk reported beside, never instead (RULINGS 28 Oct; CLAUDE.md: a piece passes only packaged; SPEECH-LEVERS-2026-11-01.md). Runs beside the game (latency.py) are screens.
- Every paid call comes out of his plan's monthly API credit. The day's ceiling is what remains of the month's credit divided by the days left in its billing month. Each run is capped in code and logged. No bought credits and no automatic reload (RULINGS 1 Nov; CLAUDE.md).
- The key. The game reads its live-talk key file (under %LOCALAPPDATA%\LEDGER) into the talk program's environment as ANTHROPIC_API_KEY. It does so only for a run somebody plays, or for an -AskScript run with -AskReal under a dollar cap (CrimeProbe.cpp LiveTalkPlayed, TalkKeyForThisRun). latency.py --live and ClaimBench --key read the same file themselves. Never open, print, copy, search or pass the key by hand (CLAUDE.md; appdata-writes-are-private-to-claude). A run with -unattended (the build machine, the nightly walk) and no -TalkHelper= starts no talk program at all (CrimeProbe.cpp LiveHelperStart). LiveTalkPlayed tests -AskScript with -AskReal and a cap before it tests -unattended, so such a run that names -TalkHelper= uses the key even when unattended: never pass those switches to an unattended run.
- The model follows the kind of moment, never who is talking (D48, RULINGS 1 Oct). The claim check stays on Haiku (RULINGS 23 Oct). The fast checker's cut-off and prepared openers are his calls: neither is moved or built without his word (RULINGS 7 and 28 Oct; SPEECH-LEVERS-2026-11-01.md). No paid voice and no cloud voice. No voice is cast without his yes, and voices are judged by ear (RULINGS 24, 29 and 30 Sep, 7 Oct). Nobody is moved to another voice engine without his yes on a blind page (production/specs/voice-engines.json, its "about" line).
- Two tries per fault, counted in DECISIONS.md. A new method on the same fault is still a try, and a new fault blocks (two-tries-means-two; IN-GAME-2026-11-02.md, try 2). Speech's two tries are spent: lever 1 (DECISIONS 1 Nov 21:31) and try 2 (2 Nov 07:41); the escalation was the new fault's first try (2 Nov 07:51). Another try at the bar needs his yes first, asked once with its reason.
- If the bar is not reached, the exit's stop rule applies (PLAN.md, phase 1 exit: "else the stop rule"). Report the failed capability plainly, never as another plan (CLAUDE.md).
- A result or target goes to his page only after one fresh reviewer has checked it against its sources (CLAUDE.md, the research method).
- A lever found while measuring is new work. It goes on the order's waiting list, not into the running week (CLAUDE.md; COST-PER-HOUR-2026-11-02.md).

**Requests this covers**, for example: "re-measure the Long Pause on tonight's build"; "time this talk change against the old one"; "why did that reply take eight seconds?"; "why do people keep saying 'that's all I know'?"; "does the check let more through with this switch?"; "what does an hour of talk cost now?"; "can we afford a run today?"; "is the voice the delay?".

## 1. Questions, then the method

- Write the run's questions first, then measure (CLAUDE.md, the research method). COST-PER-HOUR-2026-11-02.md shows the shape: questions, what was measured, the levers ranked, what was not reached. Reference: none found for live talk; study A (inZOI) is its outside reference (production/orders/2026-11-02.md, n02-3-1-speech).
- When a number surprises you, first ask whether the measure is wrong, before fixing a symptom (research-the-method-first). The 1 November figure came from a lighter request than the game sends.
- Read each lever's standing before choosing one: done, tried and failed, his call, or after the exit (SPEECH-LEVERS-2026-11-01.md).
- **Check:** the questions are written and dated; the lever's earlier tries are counted from DECISIONS.md.

## 2. Free screens before any paid call

- The talk program's self-test, with no network: `dotnet run --project ledger/TalkHelper -c Release -- --selftest`. Also the talk tests, `dotnet run --project ledger/TalkTests -c Release`, and CoreTests (all three are in tools/ci-checks.sh). Each talk change adds its own self-test line (IN-GAME-2026-11-02.md: 137, then 138).
- What each request sends, and to which model, with no key: the stand-in (`--fake`, or LEDGER_TALK_FAKE=1) with LEDGER_TALK_SIZES naming a file logs every request (Program.cs). For what the game sends, set LEDGER_TALK_SIZES in the packaged game's environment and run -AskScript=N without -AskReal, as on 2 November (the sizes run's log: -AskScript=12). That run showed the requests were the same size beside and inside the game; the model was what differed (F:/LedgerTools/latency/sizes-2026-11-02). `python tools/talk_cost_sample.py --early --sizes <file.jsonl>` sends its own sample with no evidence record, so it cannot show what the game sends.
- The game and voice path alone: -AskScript=N without -AskReal runs the stand-in (a median of 0.20 s on 1 Nov, REMEASURE-2026-11-01.md). latency.py without --live does the same beside the game.
- **Check:** the self-test and the talk tests pass in full; the sizes file shows which model each kind of line reaches.

## 3. Room in the credit

- Today's spend is the sum of today's lines in production/api-spend.jsonl. Its fields are day, at, what, usd, calls, source and item; its first line, "about", states the rule. The credit left is the console's figure, and that is his to read (the same line). RULINGS 1 Nov gives this month's daily figures. `python tools/api_batch.py --dry REQUESTS.jsonl` prints today's ceiling from api-spend.jsonl with no key and no call, but it assumes the billing month starts on the 12th (BILLING_DAY, until the bill shows): check first.
- Cap every paid run below the day's room, in code. In the game and the talk program the cap is LEDGER_TALK_BUDGET_USD (or `--budget-usd`). BudgetedClient reserves each call's worst case: the input at four characters a token plus a tenth, and the call's whole output allowance. A call that could pass the cap is refused, never sent. The 2 November runs used caps of 0.50 to 0.60.
- latency.py --live sets no cap of its own. Its talk program inherits latency.py's environment, so set LEDGER_TALK_BUDGET_USD before starting it.
- ClaimBench `--key` holds a run to the lower of its task's money left and `--cap` (1.00 when not given). A task's money left counts every earlier run in production/playtest/talk-runs.jsonl, where each run logs itself. The task must be named in KeyRuns.cs KeyTaskCaps or be today's "measure-YYYY-MM-DD", which holds 3 October's $1 a day. talk_cost_sample.py's LIVE_DAILY_USD is the same $1. RULINGS 1 Nov replaced that dollar, so both disagree with their home: list them in FINDINGS.md as a fault, not as a reason to spend past the cap. Without `--key`, ClaimBench runs on his subscription through Claude Code (ClaudeCodeClient), and its "usd" is not billed.
- **Check:** the cap is set and is below the day's room. No paid run starts from CI or the build machine. talk_cost_sample.py and ClaimBench --key refuse there; latency.py --live has no such refusal of its own.

## 4. The Long Pause inside the packaged game

- First, the packaged-walk skill's step 2: room on the drives, no build machine job, no game left open, and outside the night jobs.
- The run. No tool launches it yet; 2 November's runs were started by hand, so check first how. The played copy is F:\LedgerTools\played-game\Windows\LedgerProbe.exe, started with `-LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -NoTitle -AskScript=30 -AskReal [-TalkHelper=...] -windowed -ResX=1920 -ResY=1080 -ForceRes -nosplash` (the command line in run D's LedgerProbe.log). Its environment carries LEDGER_TALK_BUDGET_USD, without which -AskReal stays the stand-in, and LEDGER_TALK_TRANSCRIPT naming a file for the talk program's steps (IN-GAME-2026-11-02.md). Never add -PreparedAck when measuring the bar: it plays a prepared opener (CrimeProbe.cpp).
- A change not yet shipped: publish it with `powershell -File tools/publish-talk-helper.ps1 -Out F:\LedgerTools\scratch\<try>`, then add `-TalkHelper=F:/LedgerTools/scratch/<try>/LedgerTalk.exe` (as runs C and D did).
- The script asks three cast members six fixed lines in turn, each once the last answer has been heard out. It writes ask-script.json to the game's log folder, with one row per line (who, firstWords, firstHeard, opener, wholeAnswer, each in seconds from the line sent), then closes the game (CrimeProbe.cpp AskScriptTick). Each person always gets the same two of the six lines (People[I%3], Lines[I%6]), so per-person figures are per-question figures.
- Read the log before trusting the run. It must say "LedgerTalk: live, on LEDGER's own key" (otherwise the talk was the stand-in or offline), and the voice's ready line must name every cast voice. On 1 November the voice program had been starting without its Pocket voices since 29 October and had fallen back without a word (DECISIONS 1 Nov 20:36).
- Count the walk-offs in the log ("LedgerTalk: walked away from ... at N m"). In every 2 November run one person was asked from 7 to 29 m away and their replies were cut short; in run D, 7 of one person's lines left only walkedOff rows in the transcript. Name them and leave them out of the reply counts.
- The fast checker loads in the background, and lines sent before it is ready go to Haiku alone (Program.cs). Beside the game, runs wait 60 s first (`--settle 60`). The game's log does not say when it was on: check first.
- Copy ask-script.json, LedgerProbe.log and the transcript into one run folder. 2 November's went to F:/LedgerTools/latency/askreal-<date><run>/, a folder production/retention.json does not name: check first where raw runs belong (CLAUDE.md: write only where retention.json names).
- The tester's real-talk run (`play.py start --real-talk`, capped at $0.50, transcript under F:/LedgerTools/tmp/builder/real-talk) is the session's free play, not this measure (packaged-walk skill, step 7).
- **Check:** there is one row per line asked. Lines asked after the cap ran out are counted and left out. They show as the game's "Live talk cannot be reached just now" and answers at about 0.2 s (IN-GAME-2026-11-02.md, run A), and as budgetRefused above 0 in the end line (BudgetedClient.Refused; run A kept no end line).

## 5. Read the run

- First sound heard (firstHeard): the median, how many came under 2.0 s, the 90th percentile and the worst, per person.
- Split the real questions from small talk, and report the bar on the real questions with small talk beside (RULINGS 28 Oct). The transcript's "model" is the moment's model (TalkMoment.ModelFor; LlmClient.cs: Models.Core, Sonnet 5, for real conversation; Models.Ambient, Haiku 4.5, for small talk). It is null for any reply the model did not write (fall-backs, brush-offs, the ladder, plain lines; Program.cs). It stays the moment's model when a second draft was escalated (ConversationEngine.cs secondModel); escalations show only in "re-" steps and in the end line's per-model counts.
- By the game's own rule (TalkMoment.Of, TalkRules.ConceptOf) the six -AskScript lines are small talk. In run D all 20 replies the model wrote were Haiku 4.5's, so 2 November's "bar met" was measured on small talk. -AskScript as built does not measure the bar's real questions. The newcomer question set lives in ClaimBench `firsts`. How to ask those questions inside the game: check first.
- Where the time goes: each reply's "steps" in the transcript, in milliseconds (the first sentence written, its check cleared, the voice). If first words reach first sound within 0.02 to 0.17 s, the voice is not the delay (IN-GAME-2026-11-02.md).
- Fall-backs and brush-offs. A reply is marked fellBack when it is a "that's all I know" kind (ClaimCheck.KnownOnlyLines) or the ladder's refusal. Brush-offs are marked offline, or timedOut after eight seconds (Program.cs). A rise against the last run is a new fault, and it blocks: in try 2, 5 of 23 replies fell back where run B had none.
- When beside and inside disagree, compare the request sizes and models (step 2) before blaming the model's speed.
- **Check:** the note's table gains one row, as in IN-GAME-2026-11-02.md's "Where speech stands" (run, talk, median, under 2.0 s, fall-backs). A tail that stays is named as a known shortfall.

## 6. A change: old against new

- Change one lever at a time. Beside the game, alternate the old and the new talk programs, 40 lines or more an arm (SPEECH-LEVERS-2026-11-01.md; lever 1 used 80 alternating lines): `python tools/voice-live/latency.py --live --pending --voice game --prewarm --lines 20 --helper <LedgerTalk.exe> --settle 60 --out <file>`, with the packaged game open in the street (REMEASURE-2026-11-01.md). This is a screen. Its docstring's "no real calls" predates --live.
- Inside the game, one run holds one talk program (step 4, with -TalkHelper naming the new arm). Try 2 was one run of 30 lines, not alternated. How to alternate inside the game: check first.
- Switches for an arm, from the talk program: `--first-model` or LEDGER_TALK_FIRST_MODEL (a faster model writes the first sentence); LEDGER_CHECKER_MODEL (the check's model; latency.py `--checker`); LEDGER_FAST_CHECKER=0 (Program.cs).
- No gain: revert, so the shipped path stays the one measured (lever 1, 1 Nov).
- A gain ships only through the night's build and the tester's walk (packaged-walk skill). A second run on that build must confirm it before the number is called settled or goes to his page (REMEASURE-2026-11-01.md; IN-GAME-2026-11-02.md).
- **Check:** the arms alternated; the try is counted in DECISIONS.md; the note gives both arms' median, share under 2.0 s and fall-backs.

## 7. Invented claims and the claim check

- A bench standing in for the game's check must call its whole entry point, ClaimCheck.CheckAsync: the hard rule on names, the list, the code's word-for-word clearing, then the second look. Never call RequestItems and ParseItems alone. The list step alone read 552 of 617 sentences as refused, and a repair was wrongly set aside on that reading (bench-must-call-whole-check). Compare any stand-in's pass rate once with the component's own before concluding anything. A mismeasured try is measured again, not counted.
- The measures (SOURCE-TEST-2026-10-27.md): invented sentences let through per 300, harmful and harmless apart (sorted by a fresh reader blind to their source), and true sentences refused per 300. They are taken on held sentences, labelled by an independent model and read once. Anything tuned is tuned on tuning data only (tools/checkers/name_rule.py, tradeoff.py, sentence_test.py).
- The tools:
  - `dotnet run --project ledger/ClaimBench -c Release -- sentcheck --key --task <task> --from <TEST.json> [--out OUT.jsonl]`: the game's check on each sentence, timed.
  - `checktime --key --task <task> --from RUN_DIR[,RUN_DIR...]`: what the check spends its time on, on first sentences from earlier `firsts --early` runs.
  - `firsts`: a newcomer's first questions through the real engine.
  - tools/voice-live/slow_turns.py RUN_DIR: the waits sorted by cause, read from those bench folders' turns, not from game transcripts.
  - tools/checkers/source_test.py, tradeoff.py and name_rule.py.
- The check is not deterministic. Judge a change against how often two runs of the same check disagree (tools/voice-live/early_looks_ab.py). On 27 October the check alone moved by about 5 per 300 between runs (DECISIONS 27 Oct 14:57).
- The fast checker (production/specs/fast-checker.json) runs at the open cut-off, his pick from a trade-off table (LOCAL-CHECKERS-2026-10-26.md, "His pick"). The table set three cut-offs against his bars of no more invented through than Haiku alone and 0.15 s beside the game. At the open cut-off it lets 36.0 per 300 through against Haiku's 34.1 (2 more per 617) and clears about half of real first sentences, about 0.6 s sooner a question. With the voice running, 3 to 4% of its answers take over 0.15 s; its answers are dropped after 400 ms (answerWithinMs). He chose this knowingly. Any new cut-off or checker goes to him the same way, as a table.
- **Check:** each question reads the held set once; each number carries its run file and date.

## 8. Cost per hour of play

- The talk program writes an end line when its input closes: the calls, tokens in and out by model (CostTracker), usd at the game's price card (LlmClient.cs Models.Cost), cacheRead and cacheWrite (tokens; 0 and 0 mean the cache never worked), and budgetSpent and budgetRefused under a cap (Program.cs).
- The cost per line is usd divided by the lines asked (COST-PER-HOUR-2026-11-02.md: run D, $0.2415 over 30, $0.0080). An hour is 15 replies (n02-7-3), which gives $0.12. The target is $0.05 an hour (CostTracker; llm-inference-economics/SUMMARY.md). Say which divisor was used: over run D's 23 replies the hour would be about $0.16.
- budgetSpent read higher than usd in every 2 November run (run D: 0.327 against 0.241). COST-PER-HOUR says this is because each call reserves its whole output allowance. The code disagrees: BudgetedClient settles each reserve to the tokens used, stopped streams included. Only failed calls keep their reserve, and calls stopped before any answer are charged an estimated prompt. The gap is unexplained, so which figure the bill follows: check first. Log both, as api-spend.jsonl's "source" does.
- Every model in the end line must be on the price card. CostTracker counts a model it does not know as costing nothing, while BudgetedClient charges it the dearest rate (CostTracker.cs; BudgetedClient.cs). Most prices carry the date their page was read in Models.Cost's comments; Haiku 4.5's carries none. Read the pricing page again before a cost goes to his page.
- Two levers wait on the waiting list as n02-9-talk-cost-levers, each to be measured before it is kept: caching the briefing, and replies on Haiku 5.5 after their own check (production/orders/2026-11-02.md). COST-PER-HOUR ranks a third, fewer calls per reply, which is not on the list.
- **Check:** the per-model rows add up to the run's usd; the hour's figure names its run and date.

## 9. The voices' share

- production/specs/voice-engines.json says which engine speaks for whom. Since 26 October all three cast voices run on Pocket, on the processor, with the first sound about 0.1 to 0.2 s after the sentence (POCKET-SWITCH-2026-10-26.md). latency.py --voice game runs the game's own voice program (F:/LedgerTools/voice-portable).
- A cast voice missing from the ready line stops the run until it is mended. On 1 November the night cleanup's model rule had cleared Pocket's weights (DECISIONS 1 Nov 20:36).
- **Check:** in every reply, first words reach first sound in under about 0.2 s; any slower reply is named.

## Records

- production/api-spend.jsonl: one line per paid run (RULINGS 1 Nov). It holds day; at, in Swiss time from PowerShell's Get-Date (read-swiss-time-with-powershell); what; usd; calls; source, saying which figure usd is; and item. ClaimBench --key and talk_cost_sample.py --live also log to production/playtest/talk-runs.jsonl themselves.
- The dated note goes in production/research/voice-latency/ (or invented-claims/, or llm-inference-economics/): how the run was made, the raw folder, the table of runs, and what was not reached.
- DECISIONS.md gets one entry per try and per result, with the try's count. FINDINGS.md holds the open faults, such as the long tail. RECIPE.md gets a few setting-free lines when the unit finishes. The time goes against the item (tools/timelog.py). His calls (a cut-off, prepared openers, money) go through the his-page skill.
