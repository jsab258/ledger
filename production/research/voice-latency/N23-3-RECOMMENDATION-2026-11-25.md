# n23-3 live talk: the recommendation (draft 25 Nov 2026, revised 09:40; open to Fri 4 Dec)

Order item n23-3 (production/orders/2026-11-23.md): model, speed and cost from the bake-off, and the voice delay with Pocket against the 2 s bar. Every figure below is from N23-3-QUESTIONS-2026-11-23.md (same folder), which holds the raw paths; one run per row unless said, so differences under about 0.3 s are noise. Reference: studies/03-dialogue-barks.md. Method researched: speech-bench skill, the bench then the packaged game.

## The recommendation (revised 25 Nov 09:40 after advisor 380: live talk stays open to 4 Dec)

Built on the October and November records (IN-GAME-2026-11-02.md, REMEASURE-2026-11-01.md): real questions on Sonnet 5 read 2.40 s in the game on 2 Nov (run A, every line on Sonnet 5), the voice 0.02 to 0.17 s of it; 4 Nov's 2.02 s (run F) came after the 2 Nov change that classed a newcomer's real questions as small talk. **New against them:** the 2 s bar has not been met on the reply model chosen for real questions in any in-game run (Sonnet 5 2.40 s on 2 Nov; Sonnet 5.5 2.63 s at its lowest thinking today), and the voice is still not the delay.

1. **A routing fault, not a result.** Since the 2 Nov change (Program.cs evidenceBears: a newcomer's real question no longer makes the moment real conversation), the talk program sends a newcomer's real questions to the light model as small talk. Today's transcripts confirm it: all 27 generated replies to the held real questions named Haiku 4.5. RULINGS (Speech) sets the 2 s bar on a newcomer's real questions, small talk reported beside, never instead; 1 Oct gives real conversation the better model. So every in-game figure since 2 Nov that reads under 2 s on these questions (2.02 s on 4 Nov, 1.59 to 1.73 s today) measured small talk's model. Listed as a fault (FINDINGS); the bar is measured on the real-question model.
2. **No switch to Haiku for real questions on speed.** Haiku 5.5 existed in the earlier passes and was passed over; today's quality check (1 invented detail in 60 for each model) is far thinner than those passes. Any switch needs the same blind comparison as before (grounded replies, character voice, the claim check) and his ear. The speed figures below stand as measurements only.
3. **The talk layer stays swappable:** the reply model, the check model and the voice sit behind settings (and LEDGER_TALK_THINKING_OFF for thinking), so the monthly re-tests from 7 Dec can swap them without code. Newer models are expected over the game's making; the bar is re-read on each.
4. **The voice:** Pocket adds 0.015 to 0.145 s in the game; his ear judged the voices "okay, not really convincing" against acted AAA speech, so voice quality stays open beside speed. The two new local voices of the monthly scan (ZONOS3-Mini first) wait for his yes on the download.
5. **Measured but not recommended:** reply thinking off (Sonnet 5.5's first sentence written 3.20 to 1.24 s, lost lines unchanged at 5 of 30) and fast-first (1.71 s, 8 of 30 lost) are loop trials on the real-question model, not changes.

The open question for the loops: on the real-question model the median sits about 0.4 to 0.6 s over the bar and the tail is long; by the 24 Nov ruling a reply later than 2 s becomes a written line, so as things stand most real questions would be heard as written lines. That gap, not the routing, is what 4 Dec has to state.

## What was measured

### Voice (Pocket, cast voices lena, rocco, sam)
- Alone, no game: 0.15 s to first heard, worst 0.35 s (23 Nov, two runs of 12).
- Inside the packaged game: 0.015 to 0.055 s median, worst 0.25 s on real questions (25 Nov, three runs). The voice is not the delay; the text model is.

### Text model inside the packaged game, the 20 held newcomer questions, 30 lines a run

| Arm | First heard median s | Under 2.0 s | 90th s | Worst s | Fall-backs |
|---|---|---|---|---|---|
| Haiku 4.5, small talk as shipped (05:53) | 1.59 | 19/30 | 5.66 | 8.24 | 3/30 |
| Haiku 4.5, as shipped (04:43, no transcript) | 1.73 | 17/30 | 6.67 | 8.23 | not counted |
| Sonnet 5.5 forced, thinking as shipped (no field: it thinks) | 5.34 | 1/30 | 8.22 | 8.27 | 5/30 (all time-out brush-offs; 0 written) |
| Sonnet 5.5 + Haiku 4.5 first sentence, thinking as shipped | 1.71 | 17/30 | 6.54 | 8.23 | 8/30 (5 redraft first sentences flagged, 1 time-out, 2 the cap) |
| Sonnet 5.5 forced, thinking at its lowest (07:25) | 2.63 | 8/30 | 7.57 | 7.67 | 5/30 (4 written lines, 1 ladder fact); 0 time-outs |
| Haiku 5.5 forced, thinking off (07:34) | 1.85 | 17/30 | 4.57 | 7.56 | 5/30 written lines; 0 time-outs |

### Text model on the bench (outside the game, first sentence handed over, thinking off; 60 turns a run)
- Sonnet 5.5: 1.41 s median, 78/120 under 2 s over two days; Sonnet 5: 1.64 s, 68/120; Haiku 4.5 by the moment rule: 1.71 s, 35/60 (one day).

### Cost (bench api-rate dollars, ceilings: cache reads priced at full input)
- Per line with checks: Haiku 4.5 US$0.0039, Sonnet 5.5 US$0.0057, Sonnet 5 US$0.0060; an hour of 15 replies 6 to 9 US cents; the 20-hour story US$1.2 to 1.8 (a floor: long conversations carry more).
- Prices re-read 24 Nov (PRICES-2026-11-24.md): Sonnet 5 and 5.5 US$2/US$10, Haiku 4.5 US$1/US$5, Haiku 5.5 US$0.10/US$0.50 per million tokens.

## Found on the way
- The talk program never sends a thinking setting for reply drafts (ConversationEngine.ReplyThinkingOff is false in the game; only the bench sets it). Sonnet 5 and 5.5 think unless told, so the game's real-conversation moments (deeds, deals, recognised topics, on Sonnet 5) are drafted with thinking on. A default-off measuring switch, LEDGER_TALK_THINKING_OFF=1, was added 25 Nov to measure it; the shipped game is unchanged. Measured: Sonnet 5.5's first sentence written at a median 3.20 s with thinking (11 of 30 turns reached the step: likely low), 1.24 s at its lowest (talk transcripts' first-written step; Haiku 4.5 as shipped 0.67 s). Sonnet 5 in the shipped real-conversation moments likely pays the same; whether to send thinking off in the game is a talk-program change for the loops, not made here.
- The shipped folder's LedgerTalk.exe --selftest crashes (index out of range) beside its cards; from the repository it passes 143/143. Self-test is a repository check, not a shipped one.

## Open before Fri 4 Dec
- Reviewed 25 Nov 08:00 (N23-3-RECOMMENDATION-REVIEW-2026-11-25.md): pass with fixes, all applied; every figure recomputed from the raw files.
- Lines recorded for his ear later (the order): done 25 Nov 08:20. Twelve real in-game replies (Haiku 4.5 as shipped, the 05:53 run, four each for Sam, Lena, Rocco) spoken by the packaged game's own voice program, one file each, 1.4 to 13.2 s: F:/LedgerTools/game-inputs/voice-n23-3/lines-for-ear-2026-11-25/ (index.json holds each text). Nothing asked of him now; they go with the 4 Dec recommendation. Two of Sam's answers run 12-13 s (three long sentences): length, not speed, for the talk loop.
- In-game cost: the runs' spend is logged as their caps (upper bounds); per-line cost here is the bench's.
- Invented-detail rates: done 08:30 (point 1); bench runs, not in-game ones.
