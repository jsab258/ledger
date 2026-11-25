# n23-3 live talk settled: the recommendation (draft 25 Nov 2026, due Fri 4 Dec)

Order item n23-3 (production/orders/2026-11-23.md): model, speed and cost from the bake-off, and the voice delay with Pocket against the 2 s bar. Every figure below is from N23-3-QUESTIONS-2026-11-23.md (same folder), which holds the raw paths; one run per row unless said, so differences under about 0.3 s are noise. Reference: studies/03-dialogue-barks.md. Method researched: speech-bench skill, the bench then the packaged game.

## The recommendation

1. **Newcomer questions and small talk: keep Haiku 4.5 as shipped.** Inside the game it has the most lines under 2 s (19 and 17 of 30 over two runs, medians 1.59 and 1.73 s) and the fewest lost (3 of 30), at about 0.4 US cents a line (bench cost). Fast-first (1.71 s) and Haiku 5.5 (1.85 s) are also under 2 s on the median but lose more lines; one run each.
   The tension to name: RULINGS (Speech) sets the 2 s bar on a newcomer's real questions, and 1 Oct gives real conversation the better model, small talk the lighter. The game's moment rule classes these questions as small talk, and only the light path meets the bar. Whether a newcomer's questions are small talk by the 1 Oct ruling is his call if the rulings don't settle it; it goes with this recommendation on 4 Dec, with the invented-detail rates (firsts-label) for both models beside it.
2. **Haiku 5.5 is the first candidate for the 7 Dec monthly talk-model check** (RULINGS 12 Nov: three candidates, a win his one tap). Inside the game it came close (1.85 s, 17 of 30 under 2 s) with the shortest tail of any arm (90th 4.6 s against 5.7 s) at a tenth of Haiku 4.5's token price, but lost 5 of 30 lines. One run, through the forced conversation path, not the small-talk prompt Haiku 4.5 ran: not like for like, so no switch now; the 7 Dec check (on the talk bench, as the ruling says) runs it as small talk, then one in-game run if it wins there.
3. **Real-conversation moments: keep Sonnet 5 for now.** Sonnet 5.5, the bench's leader, misses the bar inside the game even with thinking at its lowest (2.63 s, 8 of 30). Shipped Sonnet 5 has never been measured inside the game at all (drafted there with thinking on, see below); the keep rests on the bench only.
4. **Reply thinking off in the game: worth a measured trial in the talk loop**, not yet a change: on Sonnet 5.5 forced through the conversation path it cut the first sentence written from about 3.2 s (only 11 of 30 turns reached that step, so likely low) to 1.24 s, but lines lost stayed at 5 (time-outs 5 to 0, written lines 0 to 4). It was not measured on real-conversation moments or on Sonnet 5.
5. **Fast-first (Haiku's first sentence, Sonnet 5.5 the rest): not now.** As fast as Haiku alone (1.71 s) but loses 8 of 30 lines; only worth a loop if a redraft goes wholly to the better model.
6. **The voice stays Pocket**: under the game's load it adds 0.015 to 0.145 s median (worst 0.52 s); the delay is the text model.

The open question this leaves for the loops: by the 24 Nov ruling a reply later than 2 s becomes a written line, so on Haiku 4.5 about 11 to 13 of every 30 newcomer questions would be heard as written lines, not live ones. The game does not yet cut at 2 s (its time-outs are longer: 2-3 of 30 brush-offs). The tail, not the median, is the real gap.

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
- Lines recorded for his ear later (the order): -AskScript keeps no audio. Plan: the voice-alone tool (latency.py) saves Pocket's output for the 12 cast lines; done with the n23-4 trial's lines against ZONOS3-Mini, before 4 Dec.
- In-game cost: the runs' spend is logged as their caps (upper bounds); per-line cost here is the bench's.
- The invented-detail rates (firsts-label) for Haiku 4.5 and the better model beside the tension in point 1.
