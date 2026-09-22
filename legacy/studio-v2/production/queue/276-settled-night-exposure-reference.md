line: instruments
spec: A night pin cannot be chosen until the night condition is known to settle,
  and no arithmetic connects a day pin to a night one. This item is the research
  rung the 2026-09-10 ruling ordered by name and that was never filed.
acceptance: a printed per-frame output-luma series for one held night condition
  at one camera, the settling frame count and the settled level named as
  last-wins, and only then a four-rung night set at the same spacing
max_sessions: 2
status: READY 2026-09-14. FILED FOUR DAYS LATE, and that is the first finding.

  THE RULING ORDERED IT AND NOBODY FILED IT.
  game-design/decision-2026-09-10-ruling-the-exposure-ladder-and-the-sheet.md
  line 132 says the night pin "is therefore a RESEARCH RUNG and goes to the
  queue with a name: settled night exposure reference", and dictates its three
  steps so the next brief would not have to invent them. A director grepped 268
  files under production/queue/ on 2026-09-14 and found ZERO hits. The
  instruction landed in a commit and never became work anyone could see, which
  is the same class of fault as the 182 items closed under an archiving commit
  (queue 275).

  THE SHAPE, COPIED FROM THE RULING RATHER THAN REINVENTED:

  1. Hold the night condition and render the same camera repeatedly, printing
     the output luma series PER FRAME, until the series stops moving. PRINT THE
     SERIES. Do not set anything.
  2. From that series state HOW MANY frames settling takes and what the settled
     level is, NAMING THE STATISTIC: last-wins, not peak, not mean. If it does
     not settle, THAT IS THE FINDING AND IT OUTRANKS THE PIN.
  3. Only then run a night rung set, four rungs at the same spacing, and only
     then choose a night pin.

  WHAT IS FORBIDDEN BY NAME, and the ruling forbade it precisely so a later
  session could not reinvent it as an optimisation: deriving a night pin by
  scaling a day pin by the ratio of two night lumas. No arithmetic connects a
  tonemapped 8-bit output luma to a scene-luminance input setting. The ruling
  records that it issued and withdrew that same instruction within an hour.

  UNTIL STEP 3 LANDS, night conditions carry exposure_pin=0.000 and are
  explicitly NOT determinism-gated. A gate covering a condition whose reference
  does not exist is a gate reading a number nobody measured. The 2026-09-14 pin
  ruling holds to this: position B pins every SUN-ON condition and leaves the
  two night conditions at 0.000 for exactly this reason.

  THE SECOND HALF THE RULING ALSO ORDERED, and it is still open. The
  determinism failure was reported as rigMeanLumaFirst=0.6102 against
  rigMeanLumaRepeat=0.9562 on ONE camera and ONE condition. Rule 3b: that
  finding has no denominator. How many camera-by-condition pairs were compared?
  If one, then "every cross-frame number in that run is void" is an inference
  from a sample of one and may be generous or may understate the damage. The
  full matrix must be printed with its count, because the shape of the spread
  across pairs decides whether this is adaptation carry-over between conditions
  or something worse.

  WHY IT MATTERS NOW RATHER THAN LATER. D28 step 2 is the sky and the sodium
  lamps at dusk. Dusk and night are where the sodium lamps are judged, and the
  studio currently has no settled reference for what night is exposed at, so a
  lamp that looks right could be a lamp photographed under an exposure nobody
  measured.
