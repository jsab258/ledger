line: voice (constitution law 6 territory; the allowlist says keep it)
spec: FILED BY THE RESIDENT ON THE DIRECTOR'S RULING, 2026-09-21, because D50
  was written with NO QUEUE ITEM TO NAME and D32 says a ruling names its item.
  The director checked 399 to 405 and none of them is this.

  THE RULING IS `ledger-v2/respec/decision-register/D50-the-voice-watermark-is-kept.md`.
  Jafar 2026-09-21: "The voice watermark is kept. The allowlist says keep it,
  the August stub was right and said the shipped game would have to decide, and
  that decision was never made, so the game speaks unmarked audio today."

  THE ENGINEERING QUESTION HE ASKED FIRST, AND NOBODY HAS ASKED IT: "whether
  the watermark can be reapplied after the game decodes the audio." That
  question comes BEFORE any implementation, because the answer decides whether
  this is a pipeline change or a runtime one.

  THE ONE CODE CLUE THE DIRECTOR FOUND: the stub is live at
  `tools/voice-live/speak.py:265-293` and `:413-434`, and
  `precompute-voices.py:177-179`, and `speak.py:430` calls
  `apply_watermark(wav, sample_rate)`, which is a POST-PROCESS SHAPE. A
  post-process on a decoded waveform is exactly the shape that could be applied
  again after the game decodes, which is why the question is worth asking
  rather than assuming.

  HIS REASON FOR URGENCY, recorded as his and not re-derived here: "With the EU
  AI Act fully applicable since 2 August 2026, unmarked generated speech is not
  a risk worth carrying." That date is his claim and is not verified in this
  tree.
acceptance: the engineering question is answered by a RUN rather than by
  reading, with the answer printed (a watermark applied, the audio decoded the
  way the game decodes it, and the watermark detected or not detected, with the
  detector named); and only then a route chosen, with the count of clips that
  would need reprocessing printed beside it
max_sessions: 2
status: READY 2026-09-21. NOT this week unless budget remains: Jafar's order of
  2026-09-21 puts the visual slice, the five measurements and the art lane
  first. Voice consent is constitution law 6 and is not loosened by anything
  here.

  RULED BY: D50, which now names this item.
