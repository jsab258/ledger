# D50. The voice watermark is kept, and the first question is whether it can be reapplied after the game decodes the audio

CANON: none

Ruled by Jafar, 2026-09-21, first message, under "On the conversation pillar",
kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"The voice watermark is kept. The allowlist says keep it, the August stub was
right and said the shipped game would have to decide, and that decision was
never made, so the game speaks unmarked audio today. Ask the engineering
question first, which nobody has asked: whether the watermark can be reapplied
after the game decodes the audio. With the EU AI Act fully applicable since 2
August 2026, unmarked generated speech is not a risk worth carrying."**

## The three facts in his sentence, checked 2026-09-21

- "The allowlist says keep it": `ledger-v2/research/license-allowlist.md`
  line 4, "Chatterbox (MIT, keep watermark)". The allowlist is law and this
  record changes nothing in it.
- "The August stub was right and said the shipped game would have to decide":
  `game-design/production-plan-audio-art.md` section 1e records the
  `resemble-perth` watermarker failing on load and being "stubbed with a no-op,
  with a note that the stub must not survive into a shipping build: the
  watermarker exists so generated speech stays identifiable as generated".
  The stub and its note are `tools/tts-benchmark/ledger_tts_bench.py` lines
  374 to 389 (`fix_watermarker`, "NOTE FOR SHIPPING").
- "The game speaks unmarked audio today": the live voice tools carry the same
  stub. `tools/voice-live/speak.py` lines 265 to 293 ("THE WATERMARKER MUST NOT
  BE ABLE TO STOP THIS") and 413 to 434 ("THE WATERMARKER STUB, ON THE CASE IT
  MUST LET THROUGH"); `tools/voice-live/precompute-voices.py:177-179` prints
  "watermarker: ... (stubbed, it is not used here at all)". Every voice path
  found on main runs with the watermarker stubbed. No path that applies it was
  found. HOLDS.

The EU AI Act date is his statement and is not verified here.

## The engineering question, and the one piece of evidence the code already gives

The question, his: can the watermark be reapplied AFTER the game decodes the
audio, rather than inside the Python generation step that the shipped game
does not run (production-plan section 1g-bis: the ship path is ONNX Runtime
with no Python anywhere)?

Evidence bearing on it, read rather than argued: `tools/voice-live/speak.py:430`
calls `maker().apply_watermark(same, sample_rate=24000)`, a waveform in and a
waveform out. That is the shape of a post-process on decoded audio, which is
what the question needs. Whether that post-process can run where the game
decodes, in C# or through an exported model, and whether a detector then reads
it back, is answered by running it, not by reading it.

## What answers it

A dispatched job on the PC, in two halves, both printed with denominators:
(1) apply the watermark to a decoded clip and detect it back, clips examined
and clips detected; (2) the same through the path the shipped game would use.
A clean result ships its count. The deliverable is the two printed detect
results; a "yes" from reading the library is not a result.

QUEUE ITEM: NOT YET FILED as of the afternoon of 2026-09-21. Items 399 to 405
were filed that afternoon and none of them is this job (399 and 400 are D58's
checkpoint work, 401 and 402 are D56's placeholders, 403 the throughput
ledger, 404 the commit gate's selftest, 405 the soak's finding). The resident
files it citing D50 and the afternoon ruling of 2026-09-21, and replaces this
paragraph's first sentence with the number, a hand-apply of dictated text.
(When first written this record said a number minted here would collide with
388 to 398, which was true that morning; the gap is named in the afternoon
ruling, section 5, and closes at filing.)

## Its queue item, which did not exist when this record was written

QUEUE 407, `production/queue/407-the-voice-watermark-decision-has-a-record-and-no-job.md`,
filed 2026-09-21 by the resident on the ruling's instruction. This record was
written when no item existed to name, which is a D32 gap; the gap is now
closed by fact and not by omission.

## What this does not decide

The shipped build's watermark implementation. Any other engine. Whether the
bark bank generated offline is re-marked (it is generated through the same
tools, so the answer to the question above covers it).
