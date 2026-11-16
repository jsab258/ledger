# Review of BAKEOFF-SONNET55-2026-11-16.md (fresh reviewer, 16 Nov 2026)

Verdict: PASS WITH FIXES. Every table number recomputes; two statements in the findings are wrong or overstated and two caveats are missing. Read only; nothing run against a model.

## 1. Recomputed from F:/LedgerTools/town-scratch/bakeoff-2026-11-16/<arm>/firsts.jsonl and run.log
Median first sentence (held-back turn counts turnMs), under 2.0 s, 90th percentile (nearest rank), worst, held back, fell back, invented items (turns with any), cost:
- A 1.811 / 32 / 6.62 / 16.14 / 4 / 0 / 49 (36) / 0.2497
- B 4.511 / 1 / 5.69 / 10.40 / 33 / 1 / 15 (12) / 0.4121
- C 2.497 / 19 / 6.52 / 14.52 / 9 / 4 / 54 / 0.3491
- A2 1.536 / 35 / 4.69 / 10.84 / 5 / 2 / 54 / 0.1941
- B2 1.885 / 30 / 6.93 / 9.46 / 8 / 6 / 62 / 0.3593
- C2 2.329 / 26 / 5.87 / 10.38 / 4 / 4 / 79 / 0.3433
- C3 2.610 / 24 / 7.09 / 10.39 / 5 / 3 / 61 / 0.3555
- B3 2.090 / 29 / 5.96 / 13.98 / 7 / 6 / 54 / 0.3541
All match the table (rounded). Costs match each run.log "key run logged" line and the eight n16-6 lines in production/api-spend.jsonl; the sum is US$2.617 (note: 2.62; 1.91 before the second pair: 1.908). Fall-back totals 12 vs 7 of 120 match run.log. Label split 23 yes / 25 partly / 12 no matches firsts-answerable-held.jsonl merged with firsts-answerable-rulings-held.json (the jsonl alone leaves 20 pairs unlabelled; the note should say both files are used). Fall-backs on "yes" questions: B2 3 (Sheila greeting, Sheila opening time, Darren opening time), B3 0, C2 1, C3 2: as stated.

## 2. Findings that need fixing
a. Arm B "29 empty drafts / 29 of 60 replies were empty": firsts.jsonl B has 26 final replies equal to "..." (26 with empty text before and after; C has 1). The 29 cannot be recomputed from the raw files (draft counts are not logged in run.log). State 26 final replies, or give the source of 29.
b. "A cost in what the newcomer hears" for the extra fall-backs: B3's six fall-backs are 5 on questions labelled "no" (nobody can answer them) and 1 partly; falling back there is the right behaviour. Sonnet 5.5's real excess on answerable questions is B2's 3 against C2's 1 only, and over both pairs 3 against 3. So the extra fall-backs are not shown to be a cost; the note's own text says this but the bullet's closing sentence and "falls back more in both pairs" lead the other way. Reword; the reader judgement is still wanted.
c. The speed claim: B2 vs C2 and B3 vs C3 medians differ 0.44 and 0.52 s, but the 90th percentile and worst point both ways (p90 6.93 vs 5.87, then 5.96 vs 7.09; worst 9.46 vs 10.38, then 13.98 vs 10.39), 5.5 was held back more often (15 vs 9 over both pairs), the A to A2 p90 swing is 1.9 s and the worst swing 5.3 s, and each arm is 60 correlated turns (20 questions x 3 cast, one run each). "Holds it" is too strong for the median alone; say "a median edge of about half a second in two pairs, not seen in the tail", no significance claim.

## 3. The moment rule (TalkMoment.cs, arm A's model column)
Arm A's model column is claude-haiku-4-5 on all 60 rows, and TalkMoment.Of(probe) returns SmallTalk for them (no concept match), so in the bench all twenty go to Haiku 4.5 (Models.Ambient). But the game's own call (ledger/TalkHelper/Program.cs:1122) also passes deedOrEvidence, dealStanding and the game's "moment"; any of these makes the line Conversation, i.e. Sonnet 5 (Models.Core). The finding "the game sends all twenty to Haiku, so run F of 4 Nov was measured on Haiku too" is true only for lines with no deed, evidence or standing deal, and the run F claim was not checked here (unverified). Reword to "by the rule's text alone, with no deal or evidence standing".

## 4. The fix (ConversationEngine.cs 244-260, ClaimBench/Program.cs:108)
Matches: ReplyThinking returns null unless ReplyThinkingOff (set by --reply-thinking-off); "disabled" for claude-sonnet-5 and claude-haiku-*; "between_tools" for models starting claude-sonnet-5-5; null otherwise. Applied at the reply draft (line 2137) and the redraft (2286). Without the flag Sonnet 5.5 is sent nothing. Note that --reply-thinking-off also sends "disabled" to Sonnet 5 and Haiku, so C2/C3 (and the Haiku "thinking off" if the flag was on) differ from arm C and the game; the table labels C "as the game sends it" and C2/C3 "thinking off", which is right. Was --reply-thinking-off set on A2? Not in the note; run.log does not record the flags: add them.

## 5. Missing for a reader
- The exact commands/flags per arm (run.log has none), including whether A and A2 had the flag.
- Sample size and tail: 60 turns, one run per arm, no interval; invented counts per turn are check catches in drafts, not final replies, and the final-reply invented lists were not judged.
- Order and machine load: arm A shared the CPU with an Unreal build (noted); no note on whether the second pair ran clear.
- The speed result is the timing of a screen beside the game (bench client, parallel 1), not the packaged game; the note says this and should keep the line next to any figure that leaves the file.
- Sonnet 5.5 price/cache claim "cache hits half Sonnet 5's" rests on the 16 Nov pricing page; observed costs are equal within 0.01, consistent.
