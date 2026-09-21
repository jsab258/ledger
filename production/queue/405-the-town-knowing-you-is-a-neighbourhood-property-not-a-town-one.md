line: simulation (the moat itself; Core, so it keeps its full review)
spec: MEASURED 2026-09-21 BY THE SCALE SOAK (queue 351), AND IT IS THE FINDING
  THAT RUN DID NOT SET OUT TO MAKE. The soak was asked whether the simulation
  runs at three hundred residents rather than seven. It does, comfortably. What
  it found instead is that IT DOES NOT MATTER HOW BIG THE TOWN IS.

  THE READING. Residents who ever remembered anything, over 500 in-game days:
  7 of 7, 17 of 50, 15 of 200, 20 of 300, 15 of 500. THE COUNT IS FLAT AT 15 TO
  22 ACROSS EVERY POPULATION AND EVERY SEED. The fraction collapses 1.000,
  0.340, 0.075, 0.067, 0.030. At 200 residents, 185 memory stores were EMPTY
  after 499 days. At 500, 485 were.

  THE MECHANISM IS ARITHMETIC AND NOT EMERGENT, read out of the Core by the
  resident rather than inferred. `Gossip.cs:141` HopDecay = 0.8 and `:142`
  MinConfidenceToShare = 0.2. The hop test at `:410` is
  `passed = r.Confidence * tie * HopDecay`, refused at `:411` when
  `passed < MinConfidenceToShare`. So with a tie weight near 0.5 a rumour at
  full confidence passes one hop at 0.4 and is refused at the second, 0.16.

  CORRECTED BY THE DIRECTOR THE SAME DAY UNDER D43, AND THE CORRECTION
  MATTERS: THE CAP IS TIES TIMES DECAY, NOT DECAY ALONE. The sentence above is
  true at that tie weight and it invites the reader to blame the two
  constants. AT TIE 1.0 THE SAME TWO CONSTANTS CARRY A RUMOUR SEVEN TRANSFERS
  (0.8, 0.64, 0.512, 0.41, 0.328, 0.262, 0.21, then 0.168 refused). So
  `deepestHopEver=2` is a reading of WHERE THE SOAK'S TIE WEIGHTS SIT, and
  those are resampled from the eleven authored ties (`Soak/Program.cs:729-730,
  794`), not a property of HopDecay and MinConfidenceToShare.

  THREE THINGS MUST PRINT BEFORE ANY CONSTANT IS TOUCHED OR ANY CARD GOES TO
  HIM: the eleven authored tie weights, the seed confidence of a sighting, and
  the hop convention. A bare "one act reaches about twenty people" invites a
  constant to be tuned, and tuning a constant so that the instrument which
  would report the improvement reads better is the ratchet this item warns
  against at its foot.
  The soak measured `deepestHopEver=2` in 2187 hops at 200 residents, and 2 at
  every rung (3 once, on seed 2). The rememberers are the witness's two-hop
  neighbourhood, which at the authored mean degree of 3.14 is 7, 22, 21, 29 and
  20 people at the five populations.

  SO: TALK REACHES A NEIGHBOURHOOD, AND A NEIGHBOURHOOD IS A CONSTANT OF THE
  MEAN DEGREE, NOT OF THE TOWN. "The world knows what you did" is, under the
  current constants, a neighbourhood property.

  WHY THIS IS A MOAT ITEM AND NOT A TUNING TICKET. The Meridian Test's second
  condition is that within thirty minutes the world visibly knows the player at
  least once: recognized, gossiped about, or confronted with something they did
  earlier. Pillar 1 claims social memory at 93 against a best-in-class of 60. If
  one act reaches about twenty people whatever the town's size, the claim needs
  either a different set of constants or a different sentence.

  THE NUANCE THAT MUST NOT BE LOST, read in the same pass: `Indelible` rumours
  bypass the decay entirely. `:402` and `:514` skip the confidence floor when
  `r.Indelible`, and `:410` passes an indelible rumour at FULL confidence rather
  than multiplying it down. The design already says talk fades and a corpse does
  not. So the two-hop ceiling is the behaviour of ORDINARY TALK, and the most
  consequential events are already exempt.

  ESTABLISHED BY THE DIRECTOR 2026-09-21, SO THIS IS NO LONGER OPEN: THE
  SOAK'S RUMOURS ARE ORDINARY TALK. The word `Indelible` never occurs in
  `Soak/Program.cs`; it seeds sightings through `mill.Witness` at :469 and
  :525, and the Core marks a rumour indelible only when asked
  (`Gossip.cs:301-307`). SO THE BODY PATH IS UNMEASURED, NOT ABSENT, and the
  reading above describes the fading path only. A second scope fact from the
  same read: meetings are a 10 percent coin per tied pair
  (`Program.cs:736-737`) and not schedules, so the two-hop cap did NOT come
  from residents failing to meet.

  THE THREE LEVERS, NAMED AND NOT PULLED: HopDecay (0.8), MinConfidenceToShare
  (0.2), and the multi-day half-life in `Age` (`RumorHalfLifeHours`, applied as
  `Math.Pow(0.5, hrs / RumorHalfLifeHours)`). The authored mean degree of 3.14
  is a fourth and is a WORLD fact rather than a constant, so it is Jafar's.
acceptance: first, whether the soak's rumours were indelible, answered by
  reading the soak's own construction, so that the measurement's scope is known
  before any constant is touched; then a printed series of reach against each
  lever, one lever at a time, at a fixed population, so the relationship between
  a constant and the number of people who end up knowing is READ rather than
  guessed; and only then a decision on what reach the moat actually requires,
  which is Jafar's and not the studio's
max_sessions: 2
status: BLOCKED 2026-09-21, and blocked on a DECISION rather than on work.

  NOT THIS WEEK, and not the studio's to take. Jafar's order of 2026-09-21 puts
  the visual slice first, the five measurements beside it, the art lane behind
  both, and says to cut from the bottom and never from the slice. This is a
  SIMULATION change to the Core, which keeps its full review, a director on the
  change and golden files. Queue 250 is the only Core work he named for this
  week and only if budget remains.

  WHAT IS OWED HIM IS THE FINDING, NOT THE FIX. It goes in the brief as a
  reading, and the question of what reach the moat requires is his to answer.
  A studio that retunes the gossip decay because a measurement surprised it is
  the studio deciding by doing, which CLAUDE.md rule 11 exists to stop.

  DO NOT TOUCH THE CONSTANTS TO MAKE A NUMBER LOOK BETTER. The soak is now the
  instrument that would report the improvement, and moving a constant and then
  citing the soak is the shape of a ratchet.

  RULED BY: `game-design/decision-2026-09-21-ruling-five-landings-the-sixth-site-the-settled-night-frame-and-the-neighbourhood-that-is-not-the-town.md`, which upheld this item's PLACEMENT (constants untouched, Core untouched, blocked on his answer, the finding to the brief as a reading) and SPLIT its measurement half out as its own ready item. The mechanism paragraph above carries the director's correction under D43.
