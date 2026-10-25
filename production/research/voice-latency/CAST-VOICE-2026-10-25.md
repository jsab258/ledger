# Speech with the cast voice on the card, re-timed the game's way (25 October 2026)

His order of 25 October, item 4: "the last stretch to 2 seconds with the cast's own voice on the card. First re-time the whole path with the cast voice (the 2.41 s was with the stand-in voice). The model writing the first checked sentence (2.1 s) is now the slow part, so research the levers there; the check stays on Haiku."

## A fault in the measure, fixed first

- **The game** starts the talk helper with `--early --pending` (CrimeProbe.cpp). So the voice makes the first sentence from its draft while the check runs, holds it, and releases it the moment the check passes.
- **The timing tool** (`tools/voice-live/latency.py`) ran without `--pending` and spoke only after the check, so every earlier figure counted the voice's time the game hides.
- `--pending` is added (selftest 5 of 5). It times "heard" as the later of the check passing and the held sound being ready, plus one frame and the sound card's buffer.
- Found by the research helper (below). Its estimate: 22 October's 2.41 s with Pocket would have been about 2.14 s in the game.

## The run

`latency.py --live --pending --voice nano --prewarm --lines 20 --checker claude-haiku-5-5`:
- the packaged game open in the street (the played copy of 24 October, `-unattended`, so no helpers of its own);
- the cast voice on the card;
- 20 checked replies on LEDGER's key (about $0.15, within his $1 a day).

Raw: `F:/LedgerTools/latency/cast-pending-2026-10-25.json`.

| Stage, seconds after the line is sent | Median | Fastest | Slowest |
|---|---|---|---|
| The first sentence drafted (before its check) | 0.75 | 0.68 | 1.38 |
| The first sentence checked | 2.01 (1.90 where the draft was used) | 1.62 | 6.43 |
| The check alone (drafted to passed) | 1.12 | | |
| The cast voice: drafted to first sound made | 2.84 | | |
| **First sound heard, all 20** | **4.14** | 2.89 | 9.19 |
| First sound heard, the 14 whose draft passed unchanged | 3.69 | 2.89 | 4.89 |

**What it shows:**
- The model drafts its first sentence fast: 0.75 s. The check adds about 1.1 s.
- The cast voice on the card, beside the running game, takes about 2.8 s to make a first sentence of about 1.5 s of sound. That makes it the slow part again: Pocket on the processor took about 0.3 s on 22 October.
- The model and its check are ready at about 1.9 s. Even with the check gone, the cast voice would hold the first sound near 3.6 s.
- In 6 of 20 turns the draft did not pass unchanged and the sentence was voiced after its check, at 5 to 9 s.

## The levers researched (the model's side)

A research helper read the talk helper's code and Anthropic's own pages (read 25 October). Its findings:

**What the code does now:**
- The helper calls Anthropic's API directly. The ruling's "paid router" (24 September) is the intent classifier; no third-party router is in the path.
- Replies: Sonnet 5 for conversation, Haiku 4.5 for small talk, `max_tokens` 300, streamed, no thinking field. No prompt caching: the volatile parts come first in the prompt.
- The check: Haiku 5.5, not streamed. It already runs beside the stream.

**The levers, by likely saving at the median:**
1. **Skip the check for first sentences that state nothing checkable** (widening its plain-words rule): about 1 s on such turns. It changes the check's reach, so it is his call.
2. **Newer models within the moment rule:** Sonnet 5.5 must think (`between_tools`); Haiku 5.5 runs with thinking off. 0 to 0.3 s, unmeasured.
3. **A shorter check answer and fewer known items:** 0.1 to 0.3 s.
4. **A warm connection when the talk box opens:** 40 to 170 ms on the first line. No ruling touched.
5. **Start the check at the full stop**, not one token later: 15 to 50 ms. No ruling touched.
6. **Prompt caching:** at most about 0.15 s at this prompt size (measured 1 October within noise). It needs the prompt reordered and the bench re-run.

These levers cut at most about 1.3 s from the check side. The voice's 2.8 s is untouched by any of them.

## Where this leaves the 2 seconds

His ruling of 7 October stands: "No third attempt at the voice; no cloud voice." So the voice's side is not changed here.

Two seconds needs a choice that is his:
- **(a)** live lines in Pocket on the processor: about 0.3 s. This reopens his 3 October voice rulings, because Pocket drifted in accent in September.
- **(b)** keep the cast voice on the card and accept about 3.5 to 4 s.
- **(c)** allow a voice attempt aimed at the card voice's first piece.

On the model's side, levers 4 and 5 touch no ruling and are next; lever 1 is his call too.

## Next in item 4

The frame spike while the voice speaks (42 to 55 ms, set aside after two tries on 23 October; its next step was a trace of that moment).
