# The Long Pause re-measured on the packaged build, the cast's own voices (1 November 2026)

His order of 2 November, 3.1: "The page's 4.14 s is from 25 October, before the Pocket voices ... Re-measure on the packaged build with the cast's own voices."

## The run

`latency.py --live --pending --voice game --prewarm --lines 20 --helper <the packaged copy's LedgerTalk.exe> --settle 60`, the packaged game (the nightly build of 31 October, 70da7ac) open in the street beside it:
- the talk program the packaged copy carries, its fast checker beside it, started as the game starts it (`--early --pending`), 60 s to load before the first line;
- the game's own voice program (F:/LedgerTools/voice-portable, Pocket on the processor for all three: production/specs/voice-engines.json);
- 20 real replies on LEDGER's key, newcomers' lines (latency.py LINES); 56 calls, US$0.15 at the game's own price table.

Raw: F:/LedgerTools/latency/pocket-packaged-2026-11-01-2035.json.

**Found first, and mended (DECISIONS 1 November 20:36):** the game's voice program had been coming up without Pocket since 29 October (its weights cleared by the night cleanup), so the first try of this run could not start its voice; the game itself had fallen back to the card's older voices.

## Result

| From the line sent, seconds | Median | Fastest | 90th of 20 | Slowest |
|---|---|---|---|---|
| **First sound heard** | **1.17** | 0.87 | 2.32 | 6.62 |
| The reply whole | 2.30 | 1.75 | | 6.41 |

- **Under 2.0 s: 11 of 20** (12 at 2.00 or under). Against 4.14 s median on 25 October (CAST-VOICE-2026-10-25.md): the fast checker (on by default since 28 October) and Pocket on the processor (0.1 to 0.2 s to first sound, against the card voice's 2.8 s) did it.
- **Two kinds of turn, by the talk program's own steps:**
  - 10 of 20: the first sentence written at about 0.7 to 0.8 s and cleared by the fast checker about 0.15 s later; heard at 0.87 to 1.18 s.
  - 8 of 20: no first sentence sent early; the reply drafted whole at about 0.7 s, then the full check (Haiku) passed at 1.7 to 2.0 s; heard at 2.00 to 2.32 s. These replies come as one sentence, so the early path (which acts on a first sentence before the rest) is not taken and the fast checker is not asked.
  - 2 of 20, the tail: one first sentence that needed Haiku's second look (heard 3.34 s), and one flagged twice and redrafted (6.62 s).

## What this points at

- The median is under the 2.0 s bar on this run; the eight one-sentence replies at 2.0 to 2.3 s are the largest group above it, and they have one cause: the fast checker's reach stops at first sentences. Asking it about a whole one-sentence reply, as about a first sentence, is the first lever to try (his list: "the fast checker's reach").
- The tail (a second look, a redraft) is the check's own work on doubtful sentences; study A's local checker is the lever for that, measured before trusted.
- One run of 20; a second run is needed before the number goes to his page as settled. Spend logged in production/api-spend.jsonl.

## Lever 1, tried and failed (1 November, 21:00 to 21:30): one-sentence replies spoken early

- **The change:** the turn's own model's reply of one sentence, at its stream's end, taken as the first sentence (ConversationEngine), so it gets the early check (the fast checker, then Haiku's first look) as first sentences do. Core tests 5214 of 5214, the talk program's 136 of 136.
- **Measured:** the old talk program (the packaged copy's) against the new (the repository's), alternating, 20 lines a run, 80 lines, the packaged game open beside them (F:/LedgerTools/latency/ab-oneline-2026-11-01; US$0.67).

| First sound heard | Old | New |
|---|---|---|
| Median | 1.16 s | 1.21 s |
| Under 2.0 s | 27 of 40 (68%) | 26 of 40 (65%) |
| 75th / 90th of 40 | 2.04 / 4.92 s | 2.13 / 5.48 s |

- **Why no gain:** the ten one-sentence replies the change moved onto the early path are the ones the fast checker does not clear (it cleared 22 of 40 in both arms, the same replies' kind): they state something checkable, so they wait for Haiku's first look (median 1.25 s after the sentence) where they had waited for the full check (1.10 s after the draft). Heard at about 2.0 s either way.
- **Set back:** the change reverted, so the shipped path is the one measured. The first of two tries on speech, failed.
- **What it shows:** under 2.0 s now turns on two things: what share of first sentences the fast checker clears (about 55%), and how long Haiku takes on the rest (about 1.1 to 1.25 s). His ruling of 28 October set the fast checker's cut-off ("on, at the open cut-off"), so its reach is not moved without him; the check's own time is the next lever, and study A's local checker the one after.
- **Pooled, the old path:** 60 lines tonight (this run's 40 and the first 20): median about 1.17 s, about two thirds under 2.0 s.
