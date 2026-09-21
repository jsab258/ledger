# D51. The speech engine's upgrade path is not the upgrade path: Chatterbox-Nano is evaluated ahead of turbo, and the 28 July record carries the note

CANON: none

Ruled by Jafar, 2026-09-21, first message, under "On speech and hardware",
kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"The speech engine's upgrade path is not the upgrade path. The turbo model
drops the exaggeration control the 28 July decision was made on; its own code
defaults it to zero and ignores it. Chatterbox-Nano at 110 million parameters
exists, clones from the same reference-clip interface, and neither earlier
topic knew of it. It goes on the evaluation list ahead of turbo, and the 28
July record gets a note that its premise no longer holds for the successor."**

## The 28 July record, found

`game-design/production-plan-audio-art.md`, a SPEC of 2026-07-28:

- section 1d: "chatterbox added, specifically because it exposes an
  `exaggeration` control. The bench now maps every case's stage direction to a
  scalar, with BORED at 0.25 and GRAVE at 0.8";
- section 1h, the result table: chatterbox, "takes direction: yes,
  exaggeration control";
- section 1i, "DECIDED, chatterbox, on the strength of the direction test",
  Jafar's verdicts of 2026-07-28: "The engine question is closed. Direction was
  the criterion".

Its copy: `game-design/decisions-answered.md`, "THE VOICE, engine decided,
casting is yours (2026-07-28)", and its lines 697 to 699: "chatterbox's
exaggeration control does moods, which you heard yourself. So the reference
clip decides IDENTITY and the parameter decides DIRECTION."

## The note, written into the record in this batch

Added to `production-plan-audio-art.md` at the head of section 1i, in these
words:

    D51, 2026-09-21: THE PREMISE OF THIS DECISION DOES NOT TRANSFER TO THE
    SUCCESSOR. This section chose chatterbox on the direction test, which the
    exaggeration control passed. Jafar's ruling of 2026-09-21: the turbo model
    drops that control ("its own code defaults it to zero and ignores it"), so
    the 28 July reasoning does not carry to it; Chatterbox-Nano (110M) is
    evaluated ahead of turbo, on the direction axis first (queue 296, amended).
    The decision itself, chatterbox for the bank, stands. Record:
    ledger-v2/respec/decision-register/D51-the-speech-engines-upgrade-path-is-not-the-upgrade-path.md

`decisions-answered.md` is a 923-line LOG that this batch does not re-emit;
the resident hand-applies this dictated line directly under its heading
"### Engine: CHATTERBOX. Decided by me, on measured evidence.":

    D51, 2026-09-21: the premise below (the exaggeration control) does not
    transfer to the turbo successor; see production-plan-audio-art.md section
    1i and the D51 record.

## Code that depends on the control, so a swap that drops it is a silent regression

Read by grep on 2026-09-21: `tools/voice-gen/ledger_voice_gen.py:22`
("direction comes from chatterbox's exaggeration parameter, bored 0.25"),
`:192`, `:418`, `:554`; `tools/voice-live/probe.py:287`,
`tools/voice-live/export_probe.py:628` and `:648`,
`tools/voice-live/precompute-voices.py:32`, `tools/voice-live/fixture.py`
lines 350 to 395 (the fixture's own axis is `exaggeration`);
`tools/tts-benchmark/ledger_tts_bench.py:24`. A successor that ignores the
parameter would run every one of these unchanged and produce undirected
speech that looks directed on the done line.

## The evaluation list, amended in this batch

`production/queue/296-evaluate-the-smaller-voice-model-for-speed-and-size.md`
(READY 2026-09-14, ordered by Jafar) names "Resemble's smaller model of the
same engine" and two axes, speed and size, with a listened comparison. Amended
to: Chatterbox-Nano first, turbo second; the DIRECTION axis added ahead of the
two it had, as the BORED against GRAVE A/B of 28 July, because that is the
criterion the engine was chosen on; a model with no exaggeration control may
still pass direction through section 1f's route (the reference clip is the
direction), which the evaluation must test on that model rather than assume.
Its line "NO CONSTANT MOVES from that run: which model ships is a ruling with
Jafar's ear on it" stands.

## What is his and not verified here

That turbo's code defaults the control to zero and ignores it; that
Chatterbox-Nano exists at 110 million parameters with the same reference-clip
interface. Both come from the research; the model hosts are blocked from this
environment (`.claude/rules/ci.md`), so the evaluation on the PC is where they
are checked.

## What this does not decide

Which model ships (his ear, through 296). The watermark (D50). The live
dialogue engine, which production-plan section 1g-bis left open.
