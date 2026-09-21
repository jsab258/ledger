line: voice
spec: two research topics independently arrived at evaluating Resemble's
  smaller model of the same engine, and the voice is currently the largest
  thing on the card. Evaluate it on BOTH axes, speed and size, against the
  model in force, on the machine that runs the game. The speed axis has a
  measured bar already: playback consumes 25 tok/s, and the path in force
  landed at 17.2ms flat steps, 58 tok/s sustained, a 2.3x margin (lever A,
  12 Aug, game-design/live-speech-latency.md). A smaller model is only worth
  taking if it holds above 25 with margin AND the voice survives the swap,
  so the deliverable is both numbers and a listened comparison.
  AMENDED 2026-09-21 BY D51 (Jafar's ruling of that day): the candidates are
  Chatterbox-Nano (110M, his figure) FIRST and turbo SECOND, because "the
  turbo model drops the exaggeration control the 28 July decision was made
  on; its own code defaults it to zero and ignores it", and "neither earlier
  topic knew of" Nano. A THIRD AXIS comes before the two above: DIRECTION,
  the BORED against GRAVE A/B of 2026-07-28 (production-plan-audio-art.md
  section 1d, exaggeration 0.25 against 0.8), because that is the criterion
  the engine was chosen on. A candidate with no exaggeration control may still
  pass direction through section 1f's route (the reference clip is the
  direction); that is TESTED on the candidate, not assumed.
acceptance: a printed series for both models on the same line, same session,
  reading steps in ms and sustained tok/s against the 25 needed, plus
  on-disk size for each; and clips of the same line from both, opened and
  listened to, not inferred from a metric. NO CONSTANT MOVES from that run:
  which model ships is a ruling with Jafar's ear on it, since the reason to
  care is size and the cost of being wrong is the voice.
  ADDED 2026-09-21 BY D51: for each candidate, the direction A/B (the same
  line as BORED and as GRAVE) opened and listened to, and the run says by name
  whether direction came from the exaggeration parameter or from the reference
  clip; a candidate that cannot be directed by either route fails the axis
  whatever its speed and size say. Nano before turbo; the run names which of
  the two it measured and prints "nothing measured" for the other if it did
  not reach it.
max_sessions: 1
status: READY 2026-09-14, ordered by Jafar. The stale summary table that sent
  a research topic looking at this is FIXED in the same batch: the bottom of
  game-design/live-speech-latency.md still read "23.8, underruns" from the
  42ms/step reading at the top of the page, while lever A had landed 58 tok/s
  further up the SAME document on 12 August. The prose was corrected then and
  the summary table was not, so every later reader who skipped to the bottom
  read a solved problem as an open one. The row is now retracted in place
  with what it retracts named. Voice sourcing consent rule still binds: only
  corpora whose contributors donated their voices to build speech technology,
  and no identifiable public figures, ever.
  AMENDED 2026-09-21 by the director under D51; record:
  ledger-v2/respec/decision-register/D51-the-speech-engines-upgrade-path-is-not-the-upgrade-path.md
