# Guards to set, 23 Nov 2026: the ready texts

For the advisor to set in one pass. Each text is the exact sentence to add or replace, with the task id or the row it goes in, and the ways it closes (GUARDS.md). Urgent first: A1 before the watchdog's next run, since a Fable story row (2026-11-23-1315-story) can be read as the builder's model.

## Advisor: scheduled-task prompts and rows

**A1. Watchdog trig_01E5EPcJSPkax9vSa98h7iHT (ways 48, 49, 68). Today, before 14:07.**
In step 4 replace "For signs of life and the model check, use only rows whose text does not start with \"Lane row\" (the main session's rows)." with:
"For signs of life and the model check, use only the builder's rows: those whose doc_id ends exactly \"-main\". Rows ending -story, -design, -blueprint, -studies, -checkers, -premortem, -look, -gtavi, -lane or anything else are cloud sessions: never a sign of the builder's life, and never a model fault, except that a Fable model line counts toward step 4c."
Add step 4c: "4c. Fable at once (his ruling 20 Nov: Fable one builder, none parallel). Count the distinct doc_id suffixes whose rows in the last 70 minutes name a Fable model. If more than one, write one advisor row, doc_id \"<YYYY-MM-DD-HHMM>-fable\" (only if none of yours in the last 3 hours), naming them. Do not message him."
In step 6 replace the sentence beginning "If \"active\" is true and \"monday\" is 2026-11-16" up to "Otherwise the normal line:" with:
"If \"active\" is true and \"monday\" is this week's Monday and the file gives its own line fields, use them; in every other case, including an active file whose \"monday\" is an earlier week, use the normal line:"
Then delete step 6b (the double week's reset alert) and in step 8 the double-week clause. Test once with two planted rows on a test collection: a \"-story\" row with \"Model: claude-fable-5-2\" must raise nothing; a \"-main\" row an hour old with \"Model: Sonnet\" must raise the model row.

**A2. Night pace check trig_016zpc3R1cyEfmqAmUHxFxoB (ways 48, 49). Today.**
Replace "for silence, use only the main session's rows (not starting with \"Lane row\")" with "for silence and pace, use only rows whose doc_id ends exactly \"-main\" (the builder's); every other row is a cloud session". Replace its week-shape paragraph's double-week branch with the same sentence as A1's step 6.

**A3. Giant prompt reminder trig_01U4kN3hbYjT7ZGTxsZfLzfb, due Thu 3 Dec 18:00 (ways 6, 7, 8, 9, 44). Today.**
Replace its prompt with:
"Giant prompt v2. First read production/lane/design-proof/DESIGN-COMPLETE.md on lane-2026-11. If it does not say the gate is met (all four conditions, red team 4 done, his scope answers in), write nothing: tell him in three lines what stands before the gate and its date, with one multiple-choice question and a recommendation if one is his. If it is met: write the giant prompt from production/lane/blueprint/BLUEPRINT.md alone (the story chapter as he approved it, or as his 21 Nov ruling on a small gap allows), as rules, breadth first, checks hidden and run by the checkers (production/lane/checkers/CHECKERS-PROVEN.md), the staging check, the go or no-go after two days. Size: the prompt itself at most 60 KB, detail in named files it points to; before it counts as written, a fresh Opus session given only the prompt and its files answers 20 rules picked at random from the blueprint, and needs 18. Capacity: from production/lane/blueprint/INVENTORY.md, the one-shot's hours needed against the Fable hours the week of 7 Dec holds at the order's line (one Fable builder at max is about 2 weekly points an hour; check the newest meter readings, never this number alone); if needed exceeds held, cut to breadth first and say what waits for the loops. Write the no-go line from that: the checks the first two days must pass at the needed rate. A fresh reviewer checks the prompt against the blueprint and the gate. The launch is the 7 Dec check's job, not this one. Tell him in three lines."

**A4. One-shot launch reminder trig_0141AXQEx2gbwe374VVAZgzB, due Mon 7 Dec 13:05 (ways 7, 8, 44).**
Replace "the seven preparation items done (checkers proven, tech plan, numbers run, inventory, his 30 minutes on the prototype, sound plan, live talk settled)" with "the six preparation items done (checkers proven, tech plan, numbers run, inventory, sound plan, live talk settled; his ruling of 21 Nov 21:43: he plays only after the one-shot, so nothing asks him to play or test before it)". Add after "the giant prompt v2 written and reviewed": "with its 18 of 20 recall check passed and its capacity line showing the run fits the week".

**A5. Cloud hourly update trig_01TXqvh6qLiVx7RSzb3MJvGf (ways 45, 62). Today.**
Add to step 5: "Every run, also list the LEDGER scheduled tasks (list_triggers, following next_cursor; reading only). Any enabled LEDGER task whose due time (next_run_at or run_once_at) passed more than 30 minutes ago with no last_run at or after it has failed to fire (the one-off reminders run in a session tied to his desktop): say so in the entry as a failure, naming the task and what it was to do, and write one advisor row, doc_id \"<YYYY-MM-DD-HHMM>-missed\", so the advisor does it by hand. The reminder named \"Hourly LEDGER update for Jafar (fired every hour by the…)\" is fired on purpose and has a far date: skip it."
Add to step 4's progress line: "until the 7 Dec re-forecast, any release date or phase forecast is shown as \"old plan, not current\"."

**A6. Job runner trig_01VkJFKewkVG9txfZCbj3L4j, standing rules (ways 44, 47, 60). Today.**
Replace "Budget: the weekly reading from the newest row with an \"Allowance:\" reading; stop at the limit the brief names, else 88% before the Monday 07:00 line." with "Budget: the weekly reading from the newest row with an \"Allowance:\" reading, and say its age in your start row (a reading older than 90 minutes, or from before the last Monday 13:00 reset, is not a reading: say so and keep spend small until a newer one lands); stop at the current order's stop (production/orders/, newest adopted), never at a number copied into a brief, else 88% before the Monday 07:00 line." When relaunching the checkers, the story v3, the blueprint prep or any older task whose stored prompt says \"stop at 95%\", append: "The 95% in your stored prompt is last week's; this week stops at 88% before Mon 30 Nov 07:00." When a task is fired for a later run than its stored prompt describes (design proof run 5 from run 2's task), always append the run's full brief.

**A7. Sunday order build trig_01R2mQHWm6T2HV6e9wRwgahX, from 29 Nov (ways 1, 10, 11, 41, 44, 46, 65, 75).**
Add to step 3: "Budget from the meter's real weekly rise over the last two weeks, everything on the account included, not from LEDGER's own estimates; section 3 gives each cloud session's expected points beside the builder's, and the total against the line. Stagger the Monday launches by dependency: no session starts before the files it reads first have landed. Name the data the 1 Feb look check needs and who makes it (a waiting item if not this week). From the order of 7 Dec: the date Kiln restarts and the date of the friends' play of the browser evening, from the re-forecast. Count the messages and phone alerts sent to him last week in one line."
Add a step 3b: "Prompt audit: read every enabled LEDGER task's stored prompt; list in the row any fact that disagrees with RULINGS.md, canon.md or the new order (dates, stops, counts, models, withdrawn items), with the exact replacement sentence, for the advisor to set."

**A8. Weekly pre-mortem trig_01NxQGLqkGUjVrpJ8s63oCCP (all ways).**
Add to step 1: "Read production/lane/premortem/GUARDS.md and GUARDS-TO-SET-*.md; for every guard marked set, partial or none with a date that has passed, check it now exists and fired, and mark it guarded, still open (with the owner told again) or wrong."

**A9. Progress page (way 62). Today.** In plan.json, beside any release date or phase forecast: "Old plan, not current; re-forecast on 7 Dec."

**A10. Red team 3's brief, at its launch on Sun 29 Nov (ways 5, 36).**
Add: "Of the ten planted parts, five are taken from production/research/lane/REFERENCE-MECHANICS-2026-11-20.md items that were never written into any LEDGER file (check with git grep on both branches before planting); report their catch rate apart from the five removed from the text. Before the round, a fresh Opus reviewer samples 20 theme-test pairs from themes.json and judges whether each test measures its theme; under 2 of 20 failing passes, otherwise the failing pairs are redefined first."

**A11. A fallback page, by job runner (way 73). By Fri 4 Dec.**
Job text: "Write production/lane/FALLBACK.md, under 400 words: if Fable is unavailable or the subscription changes, what of the plan runs on Opus 5.5 alone (one-shot, loops, story, checkers), at what pace in weekly points, and what slips by how long. Sources: the logs of the first one-shot and the story runs, the meter readings in the rows. One fresh reviewer."

**A12. The story to him on Sat 28 Nov (way 28).** Present STORY-V3-SUMMARY.md as one phone screen: the premise in two lines, its numbers beside RDR2 and the best per aspect, at most three one-line decisions each with a recommendation, the summary linked.

**A13. Lane prompt, before the lane restarts after the one-shot (ways 33, 34, 43, 56).** Rewrite production/lane/lane-prompt.txt and LANE-HANDOVER.md to the current plan; add: "Once per loop, time the changed feel on his PC in real time (the builder), never only in the headless browser; run the panel on every build he plays and record it in PANEL-VS-JAFAR.json."

**A14. Story gap threshold (way 24). By Fri 27 Nov, recorded as DECIDED for him to overturn.** "A small gap under his 21 Nov ruling: the chosen story's pooled mean within 1.0 of RDR2's by the checked readers and no aspect more than 2.0 below its best game; anything wider is large and his call."

**A15. Model switches (way 51).** Add to RULINGS' models line, on the next switch: "after a model switch, the calibration sets (story reader, panel, cheap reader) rerun before their judge counts."

## Builder: advisor row texts

**B1 (ways 48, 55, 61). Today.** "Advisor: three checks on the adoption tap of 23 Nov. (1) production/week-shape.json: active false now; confirm in your row. (2) The handover's goal line names the order of 23 November; tools/order_current_check.py passes. (3) From your next row, the headline is the current order's item in hand (for example 'n23-1: GTA V feel rows'), never 'v1'; your rows keep doc_ids ending '-main', which the watchdog now reads. Acknowledge as usual."

**B2 (ways 52, 53). By Fri 27 Nov.** "Advisor: three CLAUDE.md copies differ (main still the three-session version, which every cloud session reads; wip; lane). Make wip's the one copy: bring it to main (text only, through the usual review) and to lane-2026-11, and add to tools/doc-caps.py a check that fails when CLAUDE.md differs between main, wip and lane-2026-11 (via git show of each branch). Acknowledge as usual."

**B3 (way 54). By Wed 25 Nov.** "Advisor: add to the shared pre-commit hook a check that fails on any line starting <<<<<<<, ======= alone, or >>>>>>> in .md, .json and .py files; it runs on every branch. Acknowledge as usual."

**B4 (way 58). By Fri 27 Nov.** "Advisor: order 1.5's Mafia word check: show it firing in your row on a planted line, then list the fifteen lane files that name Mafia (production/research/lane/ methods and references, LANE-HANDOVER.md) and mend each: Mafia removed as a reference to measure or compare; Mafia: The Old Country kept only as an Unreal-use study (advisor 310). Acknowledge as usual."

**B5 (way 72). By Fri 27 Nov, before the story's delivery.** "Advisor: widen tools/canon-gate.py's scope to production/lane/story/ (skipping only gtavi-story-working/, which no one reads for him) and run it once; any hit on alcohol, gambling or children goes to the story v3 session as a finding. Acknowledge as usual."

**B6 (way 20). By Fri 27 Nov.** "Advisor: every sound-level row in production/research/lane/measurements/ is read by code from the recording's audio (integrated loudness and peaks, the tool named), or marked 'his, by ear' and kept out of the gate. Acknowledge as usual."

**B7 (ways 12, 14, 16). By Fri 27 Nov.** "Advisor: three columns in STATUS.md for every number: the method of each of its two readings (code, cheap reader, Opus, by hand); its error from n23-2's ruler check; and 'provisional' for any GTA VI number, to be read again after its reception study of 19 Dec. A higher bar wins only where it is higher by more than its error. Acknowledge as usual."

**B8 (way 10). Today, in the 20:00 reprice.** "Advisor: give the reprice in weekly points as well as hours, set against what this week's line leaves the builder after the cloud sessions (about half), with the finish date that follows. Acknowledge as usual."

**B9 (way 57). By Mon 30 Nov.** "Advisor: the overview's Monday risk lines come from the newest production/lane/premortem/PREMORTEM-*.md and GUARDS.md (the five worst open ways and their owners); mark production/research/pre-production/6-RISKS.md superseded in its first line. Acknowledge as usual."

**B10 (way 64). By Mon 30 Nov.** "Advisor: tools/needs_you_page.py refuses an item whose subject is a licence (licences are never his question); show it refusing a planted one. Acknowledge as usual."

**B11 (way 33).** "Advisor: when the loops start, each loop's changed feel is timed in real time on this PC once, and the row says so." (Send with the order of 7 Dec.)

**B12 (way 23). By Fri 4 Dec.** "Advisor: hand-read 100 more Steam story reviews for each of the top four story games (RDR2, GTA V, GTA IV, KCD2) by the same coding, and report whether the ranking holds. Acknowledge as usual." (Waiting item if the week is full.)

**B13 (way 59). By Mon 30 Nov.** "Advisor: every page read and row converts commit times to Swiss time before comparing. Acknowledge as usual."

**B14 (way 67).** Waiting item: "When the town simulation thaws, its browser build is made on this PC, not in the cloud."

**B15 (way 60). Today.** "Advisor: every hourly row carries the meter reading and its time, so the cloud sessions read a fresh one; your first row after the reset gives one at once. Acknowledge as usual."

## Cloud sessions: what to add to their briefs

**C1. Blueprint keeper trig_01Ur6ZQZj4S3KsyAq86ZMtyG, from its run of Tue 24 Nov (ways 2, 14, 16, 17, 40, 71, 78).** Add standing rules:
"(h) Unreal reachability: a chapter listing every OUTSIDE row of coverage.json (looks, engine, performance, shipping), each with its standard where known, its owner and a date; frame and memory budgets for the crowds as rows; the shipping list (store page, rating, AI disclosure, privacy, legal) dated. (i) A higher bar from another game wins only where it is higher by more than its stated error, and only after a check against canon's not-list (not a driving game, one port, the content rule); a clash goes under Rulings to revisit. (j) Standards that rest on GTA VI are marked provisional until its reception study of 19 Dec. (k) The memory-and-gossip pillar against the older canon line: quote both lines and put one multiple-choice question with a recommendation under Questions for him."

**C2. Design proof run 5, on its next relaunch (ways 3, 35, 36, 37, 69).** Append: "Make the coverage scripts fail any row marked MEASURED whose real_basis is empty or not one of the three kinds G-A allows, on every run. Add gate rows for live talk: delay to first audible word (bar 2 s) and cost per played hour, from n23-3. Mark the typed-talk set 'AI-checked, a human sample due at the friends' play'. Hold 1.6.5 (waiting under 10%) as a gate row read on our filmed build (n23-2). Before red team 3, the 20 theme-test pairs sample of A10."

**C3. Story v3 trig_01HoWEpFLCpnBq55KansF1mU, on its next relaunch (ways 22, 26, 27).** Append: "Phase 2: calibrate the checked reader also on four less-known games with Steam story scores, disguised, and report whether its fit holds. Phase 3: play the cab confession sketch both ways, typed lines and suggested lines, and record which the AI players and the checked reader prefer. Before delivery: a fresh Opus helper checks the chosen bible against RULINGS.md, canon.md and itself (who can drive, how many endings, the content rule) and every contradiction is mended or listed."

**C4. Checkers trig_01TLMCmhy6GorXtJoCgNtoLW, on its next relaunch (ways 29, 31, 32, 34).** Append: "Add screen-based checks for the experience rules (camera out of walls, a face on screen when talked to, nothing black for more than a second) read from screenshots, not game values. The harness spec freezes baselines; a baseline changes only with a reviewer's line in the log. Write the panel's bar once, in one file, and make every other mention point to it."

**C5. Blueprint prep trig_01PhpaXNa1YdaS1pk98wuB4X, on its next relaunch (way 39).** Append to TECH-PLAN: "For each module, its Unreal counterpart and the port test that proves it, so nothing browser-only is built; the cab named as the first port when Unreal work resumes."

**C6. Job runner job, by Wed 25 Nov (way 54).** "On lane-2026-11 only: replace RULINGS.md with wip's current copy (it has no merge markers and is within its 4,900-word cap; the lane copy has two marker lines and 5,014 words); confirm tools/doc-caps.py passes on the lane; commit 'Lane RULINGS replaced by wip's: merge markers removed'. Nothing else."

## His list (account, canon, scope), for the advisor to put to him

1. Way 74, the repository is public: anyone can read the unreleased game and story. (a) Make it private once the advisor has moved the watchdog and night check to authenticated reads (recommended; about an hour of the advisor's work, then one switch in GitHub's settings); (b) keep it public; (c) make it private now (the two clock tasks would go blind until changed).
2. Way 39, the browser game must port: (a) when Unreal work resumes, the first job is porting the cab under the same checks, before Kiln (recommended); (b) Kiln first as ruled; (c) a one-day cab port now, against the paused-Unreal ruling.
3. Way 71, a canon question: once the keeper quotes the two lines (C1 k), one multiple-choice question with its recommendation. Not before.
Account matter, already his: the backup's Dropbox folder set to online-only (advisor 320).
