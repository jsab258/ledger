# Review 03: research and the studies (full audit, 19 November 2026)

Area: production/research (1,155 files in 167 folders, among them aaa-reference with its 17 studies, PLAYERS.md, CENSUS.md and TALKS.md; study-recs; the coverage-audit folders; pre-production; the lane's research), ledger-v2/research (the allowlist only as research method) and the research under legacy. Read only. One limit up front: the git history in this checkout is shallow (184 commits: 3 to 5 October, then 17 to 19 November), so dates before 17 November come from the files themselves, the orders, DECISIONS.md and the time log, not from commits.

## Summary

The research is large, mostly careful in its own terms (questions first, sources dated, unreached sources listed, fresh reviews) and widely used: about a hundred files cite the studies, and the phase 2 plan, street checks, camera and asset budgets are built on them. But its centre, the sixteen AAA studies of 25 to 28 October and their 145 lines, rests on reading Mafia's and Kingdom Come II's own files, which Jafar's ruling of 17 November turned into leads. Nothing has been re-marked: specs, canon's new pillar targets and target sheets still use them as evidence, two standing rules still send the sessions to the games' files with Mafia as an equal reference, and the order of 23 November holds a step that reads Mafia's files again. The 145 lines' states are untrue and untracked since 6 November. Research-first broke where it mattered most: the study method's legality was read at the statutes 23 days after the files were opened. The studio's own research named the fun risk (3 October) and Mafia's weakness (12 October) weeks before Jafar raised both on 18 November. Missing: the outside-only sources the studies skipped, the rise to power, and whether cab fares can carry the day.

## Findings, ranked

### 1. The study numbers are still used as evidence after the outside-only ruling (high)

Why it matters: canon's newest targets, the camera, the garment budgets and several target sheets rest on numbers that are leads only since 17 November, and Mafia, never the yardstick, sets most of them.

Evidence:
- The method was the games' files: "Three ways in, used in this order: the game's files first, its code only where the files are silent" (production/research/aaa-reference/STUDY-PLAN.md line 30 onward); REFERENCE.md lines 7 to 12 (Mafia's 29 containers opened with a published key; KCD2's 31,150 files unpacked). Mafia leads 9 of the 16 studies (STUDY-PLAN.md table at line 73).
- Canon lines 160 to 162: "Targets (Study 2 and the player study): about ten distinct activities per thirty minutes; nothing new for at most about five minutes". Study 2 says its order of beats comes from the files and "The minutes between them are estimated" (studies/02-first-30-minutes.md line 5).
- production/specs/camera.json line 3 ("Mafia: The Old Country, read from its files"), lines 22, 37, 44 (every room, talk and run row is a ratio of Mafia's); last changed 30 October.
- production/specs/asset-budgets.json lines 4, 5, 33, 34 (garment triangle thresholds and LOD steps from Mafia's jackets, "study6"); these thresholds drive tools/ue/asset_checks.py.
- Target sheets written on 17 November before the 22:33 ruling and not revisited: TARGET-MICKEYS-NIGHT-2026-11-17.md line 9 ("290 in Kuttenberg's region, 104 in Trosecko"), TARGET-LIGHT-WEATHER, TARGET-STREET-FURNITURE, PLAN-PARKED-CARS, all with no lead marking.
- Only the lane's melee sheet does it right: "Every Study 14 number is pre-ruling: it may guide a first tuning, but it is not evidence" (production/research/lane/FEEL-TARGETS-MELEE-2026-11-18.md line 9).

Proposed ends:
- Rule: every file that cites studies 1 to 16, Study A or Study B carries a one-line "lead, pre-17 Nov" mark beside each such number; a check fails a spec or target that cites a study number without it.
- List item: re-derive from outside sources (measured footage, developers' talks, published figures) the three most used sets first: the camera rows, the garment budgets, the activity and empty-minute counts.
- Ruling for him: Canon's pillar numbers (ten activities, five empty minutes) came from Study 2's file reading and estimates. A) keep them, marked provisional until footage of KCD2 and one GTA confirms them (recommended); B) keep them as they are; C) drop the numbers and keep the words.

### 2. Two standing rules still order file reading and Mafia as an equal reference (high)

Why it matters: while these stand, every new item is pushed toward the method he banned and the game he demoted on 18 November.

Evidence:
- CLAUDE.md line 51: "look up how Mafia or Kingdom Come II does it (the studies, then their files on demand)"; line 52: "Mafia's missing numbers fetched only when an item needs one".
- tools/order_ledger.py lines 23 to 26 and 108: a new item fails the push unless it names "Mafia's or Kingdom Come II's number or method, or 'none found'" or a studies/ path; line 44 accepts any "studies/" citation, so citing a file-read study satisfies reference-first.
- DECISIONS.md line 341 (17 Nov 22:38) already saw it: "CLAUDE.md's reference-first and game-extract lines still name the games' files: his to change". Nothing changed in the two days since. DECISIONS-TRACE.md lines 48 to 50 and 63 to 65 found the same; this review confirms it and adds the order_ledger.py half.
- The consequence is already in his next order: waiting item 15, "its files read once at S0" (production/orders/2026-11-16.md line 50), from production/research/traffic/TRAFFIC-COST-2026-11-17.md line 41 ("S0, 1.5 h: one capped look at Mafia's traffic and spawner files (one extractor...)").

Proposed end: rule. The session changes order_ledger.py now (code, not his document): "Reference:" names an outside source (footage measured in the browser, a talk, published analysis, a study number marked lead) or "none found", with KCD2 named as the bar and Mafia as period reference only; S0 is struck from item 15. The two CLAUDE.md lines go to him as a replacement text on his page, since CLAUDE.md is his.

### 3. Two costings of the same traffic, the same day, 29 hours against 85 (high)

Why it matters: his order of 23 November will spend from one of them, and they differ by about three times. Neither knows the other exists.

Evidence:
- production/research/traffic/TRAFFIC-COST-2026-11-17.md (main session, commit 3be39f3, 17 Nov 21:33): "about 29 h (24 to 36)", steps S0 to S8 at lines 41 to 49, carried into the order (orders/2026-11-16.md line 50).
- production/research/lane/TRAFFIC-COST-2026-11-17.md (cloud lane, same date): stage 1 "est. 38 hours machine-free (range 33 to 43) and 47 on the PC (range 40 to 55)" (lines 9 and 123).
- Neither names the other. Both passed a fresh review.

Proposed end: list item. Before item 15 enters the order of 23 November, one reconciliation of the two, a fresh reviewer on the result, and the number that reaches him says which costing it is and why the other was wrong.

### 4. The state of the 145 study lines is untrue and untracked (high)

Why it matters: every study recommendation is meant to be a ledger line with a true status. No line has ever been marked done there, advice not to do something is listed as work to do, and no record says which lines the game now carries.

Evidence:
- Done in production/research/study-recs/RECS-BY-PHASE-2026-11-06.md (s02-02 hints, s10-03 prompts by facing, s14-14 his fists ruling), yet "carried over" in all four orders: production/orders/2026-10-25.md, and archive/2026-11-02, 2026-11-09 and 2026-11-16 (checked line by line).
- The 18 "ignore" lines (study says do not adopt) were "set aside" until 2 November and became "carried over" on 9 November (s01-02, s14-13, s15-10 and the rest), under his keep-or-drop tap K1 "kept for their phase".
- 53 phase 1 and 2 lines were "dropped, folded into n09-1 (or n09-4)" on 9 November (archive/2026-11-09.md); n09-4 is "done" as the phase 2 plan, but only 13 of the 53 appear in production/research/phase2-plan by their ids; the crowd recipe (s06-04, s06-05), the texture pool (s12-04), naming and tuning rows (s13-02, s13-03) and most of sound appear by none.
- The state table stopped on 6 November. A third tracker, the lane's production/lane/synthesis/TRACE.md (18 Nov), maps the lines into the new design.
- What is actually built: of the 8 lines done after review on 6 November, about five are game behaviour (s02-02, s07-01, s09-02, s09-05 with s10-03); since then s04-01, s04-04 and s04-06 went into tools/street_checks.py (production/research/street-checks/N16-4-TARGET-2026-11-16.md lines 62 to 80).
- A repeat of an August lesson: rows "drifted for weeks; audits, not the plan, found" them (ledger-v2/research/waste-lessons.md, lesson 6).

Proposed end: rule. One home for study-line state (the lane's TRACE.md or study-recs, not both), updated in the same commit as the work; the order ledger points at it instead of copying 92 lines; "ignore" lines return to set aside; tools/order_ledger.py fails when a line it lists as carried over is marked done at its home.

### 5. Research came after the work where it mattered most (high)

Why it matters: research-first is his rule (13 October, CLAUDE.md). Twice the method itself was researched only after it had been used, and each time the late research showed the work was done the wrong way.

Evidence:
- Legality of the study method. The games' files were opened on 25 October. The only legal note before that, production/research/frontier-ai-uses/3-LEGAL.md (12 Oct), says "Unreached: every legislation and court site" (line 5) and its own rule of thumb is "Do not decompile, disassemble, unpack or rip another game" (line 24). The statutes were first read at source on 17 November (production/research/lane/GAME-TERMS-AND-STUDY-LAW-2026-11-17.md section 4), the day he ruled outside-only. Jafar accepted the risk on 11 October, but the research method says an unreached source is never evidence, and the research was not done.
- KCD2's tools: KIT.md (12 Oct) planned "KCD2 through Warhorse's own modding tools"; their licence, which bars companies, was found only on 25 October (KCD2-OFFICIAL-TOOLS.md, top).
- Kiln's strain limit: merged into Kiln main at 00:51 on 18 November with "each fabric's limit applied last" (commit 1d64d1c); its primary source was read twelve minutes later and says the opposite, collisions last (commit d1ddd84; production/research/lane/STRAIN-LIMIT-ORDER-2026-11-18.md, "Short answer"). A reorder lane followed.

Proposed end: rule. A tool test or merge names its "Method researched:" note, and a check fails when that note's date and time are later than the first commit of the work. For any new way of studying other people's work, the terms and law are read at source before the first use.

### 6. The studio's own research named the fun risk and Mafia's weakness; Jafar had to raise both (high)

Why it matters: this is the audit's question 7 in its plainest form. On 18 November Jafar said "we don't want a gossip simulator", and that Mafia was only a period Unreal study, never the bar. The research had said both in October.

Evidence:
- Risk R6, "There are not thirty minutes worth playing" (production/research/pre-production/6-RISKS.md line 28, 3 October). Its proof P4 was ranked first, one day, cost at most 1 (3-PROOFS.md line 13). P4 was first run on 18 November, part (a) only (pre-production/P4-LONG-SESSION-MODE-2026-11-18.md).
- PLAYERS.md (12 Oct) item 1: "LEDGER's first half hour needs one scene a friend would retell (R6, P4) before it needs more street" (line 642). It reached no order until his "against drift" item of 18 November (orders/2026-11-16.md line 57). Its question 10 on price and length (line 651) never reached his page; it sits only in the lane's pack (production/lane/synthesis/pack/05-players-basics.md line 157).
- PLAYERS.md line 11: positive English reviews KCD2 92.9%, Mafia 72.4%; Mafia punished for "Linear, an empty map, an interactive movie" (line 414). Thirteen days later the study plan still made Mafia the main source of 9 of 16 studies.
- Jafar wrote Study 17 himself on 31 October (how one small district carries a long game, public sources only), a question none of the sixteen asked. It feeds the design yet "has had no fresh review against its sources yet" (studies/17-yakuza-shenmue.md line 55).
- The checks that should have caught it: PLAN.md line 59, "Monday's review updates R1 to R10", and the research method's fresh reviewer for anything that becomes a design.

Proposed end: list item. P4's activity and empty-minute count, on the real game's packaged build, every Monday beside the street pictures; Study 17 gets its fresh review; PLAYERS.md question 10 goes to his page as written, with its recommendation.

### 7. The risk register is dead while the plan says it is updated weekly (medium)

Why it matters: the risks he sees are now five production worries; none is about fun, driving, combat or scope, the things he raised himself.

Evidence: 6-RISKS.md last changed 5 October (commit 6679e4a); PLAN.md line 59 still names it. The live list is production/progress-page/progress.json, weeks/0 "risks" (street scale test, Kiln, drive F, live talk's 2 s). A third home is drafted: production/lane/RISK-REGISTER-WHOLE-GAME-DRAFT-2026-11-18.md.

Proposed end: rule. One risk home, named in PLAN.md; 6-RISKS.md marked archived at its head; the Monday review must carry a line on whether thirty minutes are worth playing.

### 8. Research repeated without reading what was already there (medium)

Why it matters: time and tokens paid twice, and conclusions that contradict the project's own code.

Evidence:
- None of studies 1 to 16 cites the September coverage audit, and Study 1 (NPC life) and Study 3 (barks) cite TALKS.md zero times, though TALKS read Warhorse's NPC interviews and Hangar 13's 123-page "Designing System Driven Dialogue in Mafia III" in full (TALKS.md lines 45 to 53).
- s01-06 and s06-07, "dirt, blood ... give Tom away", are listed open for phase 6, while the C# Core already has it: class Stain and Noticeable(Stain, metres, lightLevel) (ledger/Assets/Scripts/Core/Traces.cs lines 17 and 44); coverage-audit-kcd2/SUMMARY.md line 9 said so on 14 September: "already built".
- UE4SS read in five notes from 8 to 17 November (games-numbers/, aaa-reference/UE4SS-METHOD-LICENCE, two lane notes), which disagree on its latest release (v4.0.0 against v3.0.1), for a method that loads code into the game and is now banned.
- The two legal notes (12 Oct and 17 Nov) do not cite each other; the newer assumes "four Steam games he owns", a premise it did not check against the older note's record of 25 October (ownership is his and is not reopened here).

Proposed ends: rule (reuse first applies to research: a new note lists the existing notes on its topic, found through the catalogue and a search, or says none). Deletion: the UE4SS notes and N16-11's methods C and D, kept only as one archived line saying the route is closed by his 17 November ruling; safe because nothing may use them now.

### 9. Missing research for an exciting, immersive game with KCD2 as the bar (medium)

Why it matters: the outside-only route is now the only route, and the parts of it that matter most for excitement were left as leads.

Evidence:
- TALKS.md (12 Oct) holds 40 leads, the best Warhorse talks among them, "in the Leads list for the PC to watch" (line 9); no later file reports one watched. Footage measuring exists only as plans (production/lane/FOOTAGE-TO-GAME-SET-2026-11-18.md, BLIND-LINEUP-PLAN-2026-11-18.md).
- Canon's pillar promises "a rise to power" (canon.md line 169); no research file contains the phrase, and the empire is touched only in Studies 15 and 17. How crime games make a rise feel earned and keep it from repeating (TALKS' own pointer is Mafia III, line 8) is unstudied.
- The lane's whole-game design makes "the cab the day's main verb" (production/lane/synthesis/DESIGN.md line 158) with no research on how fare work stays fresh over 15 to 20 hours, beside canon's "NOT a driving game".
- Why people play for hours (GTA, his words of 18 November) is staged for later (GTA VI from outside: order item 24, a reception study about 19 December); no study of an earlier GTA's loop exists.

Proposed end: list item. An outside-only study list for the order of 23 November, each with questions first: KCD2's first hour measured from footage (activity mix, empty minutes, how the town shows it noticed); the Warhorse talks on NPC sight and daycycles; one study of a rise-to-power loop; one of fare and delivery jobs in open-world games. And a ruling for him on the cab: Should cab fares be the day's main verb? A) prototype it, kept inside canon's spend rule until P4 shows fares stay fresh over a week of play (recommended); B) adopt it now; C) keep fares a side activity.

### 10. What the research cost is mostly not recorded (low)

Why it matters: he asked for real numbers. The study plan promised "about 45 to 50 hours"; nobody can say what it took.

Evidence: production/time-log.jsonl holds 6.9 session hours across 20 study tasks; helpers' time is largely absent. The token audit for 26 October to 2 November gives research about $445 of $2,222.29 at API prices (20%), with 44% of all spend "not in the time log" (production/research/token-audit/AUDIT-2026-10-26_to_2026-11-02.md lines 5 to 30); 25 October, when six studies ran, is in no audit. Study 2's raw exports, about 26 GB, filled drive F (orders/2026-10-25.md, study-2 line). His attention: the legal acceptance of 11 October, the ownership exchange of 25 October, the keep-or-drop tap of 8 November over 145 lines.

Proposed end: rule. Helpers' time and the study's token cost are logged against the study item (CLAUDE.md already asks it); a study closes with its hours and dollars in its own header.

### 11. The research has no current index, and two records misstate their own state (low)

Why it matters: 167 folders with no map of which conclusions stand is how repeats (finding 8) happen.

Evidence: production/research/README.md last changed 22 September and routes only look; CATALOGUE.md lines 75 to 86 list folder names with no conclusion or status. study-recs' header still says "Not yet checked by a fresh reviewer" (line 3) though REVIEW-2026-11-06.json checked it that day. The allowlist's older entries 1 to 6 (Kokoro, Chatterbox, TRELLIS, Audio2Face, MusicGen, OSM) carry no source link or date read, unlike entries 9 to 13, against the 13 October method (ledger-v2/research/license-allowlist.md lines 4 to 9); its header says "recheck at ship".

Proposed end: rule. Each research folder gets one catalogue line: the question, the answer in one sentence, the date, and live, superseded or lead; catalogue.py already fails on unlisted folders and can fail on a missing status. The allowlist's undated entries are re-read at source and dated when next touched.

## Answers to the brief's seven questions, in short

1. Same game: half pointed at Mafia's (findings 1, 2, 6). 2. Still true: no (3, 4, 7, 11). 3. Used: yes, as evidence it no longer is (1). 4. Cost: mostly not recorded (10). 5. Missing: finding 9. 6. Contradictions: findings 2, 3, 4, 8. 7. Raised by Jafar himself: outside-only study (17 Nov), KCD2 not Mafia as the bar and not a gossip simulator (18 Nov), Study 17 (31 Oct); findings 5 and 6 name the checks that should have caught them.
