line: research (CLOSED as a negative on its engine half; OPEN as a measurement
  on its simulation half)
spec: TWO HALVES THAT LOOK LIKE ONE QUESTION AND ARE NOT. World streaming at
  Phase B's scale is SETTLED AND NEEDS NOBODY: Unreal's World Partition already
  does tiled distance-based streaming with a memory budget, and ten to fifteen
  square kilometres is an order of magnitude under what would need a bespoke
  system. NOBODY IS TO COMMISSION IT. The half that IS ours and is unmeasured:
  at town scale, residents OUTSIDE the streamed slice must keep perceiving,
  remembering and gossiping, or the moat dies the moment the player walks away.
acceptance: the soak is run at 50 residents and then at 200, and reports what
  holds and what falls over, BEFORE Phase B is planned rather than when it is
  built
max_sessions: 2
status: READY 2026-09-16, ruled by Jafar in his own words. The negative half is
  CLOSED on arrival and is recorded so that a later session cannot open it.

  THE NEGATIVE, RECORDED SO IT STAYS SHUT. "World streaming is not a research
  question." The engine already ships the mechanism, the scale is an order of
  magnitude under the threshold where a bespoke system earns its keep, and a
  session that later proposes one is repeating work Jafar has already
  dismissed on the evidence. THE ENGINE CLAIM IS HIS AND IS NOT RE-DERIVED
  HERE: this repository cannot measure World Partition's behaviour, and the
  tree's only mentions are D1-engine-probe.md:4 and the feasibility research
  at :5 and :28, which name it as a capability rather than benchmarking it.
  Recording whose claim it is, rather than dressing it as a measurement, is
  the point of writing it down at all.

  WHY THE OTHER HALF DOES NOT FOLLOW FROM IT, in his words: "GTA can unload
  people because nothing is lost; we cannot." The feasibility research confirms
  the mechanism it would be borrowed from, at line 128: GTA's ambient life runs
  on "pedestrian and traffic spawners tied to the streaming region". A spawner
  region is exactly the thing that makes unloading free, because a pedestrian
  who is despawned had no state to lose. Every pillar of this project says our
  residents do.

  THE SHAPE OF THE ANSWER IS ALREADY NAMED and is not what wants measuring:
  resolve schedules rather than simulate bodies. The research at :130 and :134
  puts it as tiered intelligence with daily schedules as data-driven state
  machines fed by authored data, and at :132 as the precomputed-versus-runtime
  lever. So this item is NOT asking what to build.

  WHAT NOBODY HAS IS A NUMBER, and that is the whole item. The only scale
  evidence in the tree is a SEVEN AGENT soak, and ledger/Soak/Program.cs says
  so itself at line 57: "Seven agents is not a town (queue 116), so the
  projection names its denominators and the HEADROOM is printed as a multiple
  of the measured rate". Against that, D25:26 sets the target as "a town of
  three to five hundred residents who all remember". SEVEN TO FIVE HUNDRED IS
  NOT AN EXTRAPOLATION, IT IS A DIFFERENT QUESTION, which is queue 116's own
  sentence about the same gap.

  SO IT IS QUEUED AS A MEASUREMENT AND NOT AS RESEARCH. The soak at 50, then at
  200. Report what holds and what falls over at each. His reason for the order,
  verbatim: "If it does not run at three hundred, that changes the design and I
  would rather know at fifty." A number that arrives while Phase B is being
  planned can still move the design; the same number arriving while it is being
  built cannot.

  WHAT THE RUN MUST PRINT, from this project's own instrument rules rather than
  invented here: every zero ships its denominator; a rate is named as the
  statistic it is (per resident per day, or whatever it turns out to be) rather
  than left as a bare number; and the thing that falls over first is named,
  because "it did not finish" and "memory grew without bound" and "the gossip
  round stopped terminating" are three different findings and only one of them
  changes the design.

  QUEUE 116 IS REOPENED AND RIDES WITH THIS ITEM. Ruled by Jafar 2026-09-16:
  "it is the scale evidence for pillar 1. Reopen it as part of 351 rather than
  leaving the decision to whoever picks that up." The first version of this
  item deferred that call to an unnamed later reader, which is the same shape
  as the archiving commit that closed 116 in the first place.

  THEY ARE NOT THE SAME WORK AND NEITHER SUBSUMES THE OTHER. 116 asks that no
  document cite the seven-agent soak as evidence for hundreds; THIS asks for
  the measurement that would make such a citation honest. The citation fix is
  DOWNSTREAM of the number: at 200 the citations need correcting to say 200,
  and at a failure by 50 they need removing entirely. So 351 runs first and
  116 closes on its result, and 116's own acceptance (the count of citations
  found and changed, printed) is part of this item's close-out.

  116 was CLOSED 2026-09-10 by cd55a79c, an archiving commit naming no ruling,
  and is the FOURTH item found closed that way, with 111, 138 and the 182 of
  queue 275.

  UNDER D45 this is the game and not a tool that measures it: the soak is the
  instrument, but what it would establish is a property of the simulation, so
  a landing that changes the design gets a director.

  ANSWERED 2026-09-21, RUN IN THE CONTAINER END TO END AT 7, 50, 200, AND
  BEYOND THE ASK AT 300 AND 500. One binary, one process, one clock, because a
  rung compared across runs is a different photograph. The 7-rung reproduces
  the previous reading bit for bit (1261 events, bytesPerEventAtWorst=229,
  rate 0.361), which is the accepting case for the knob itself.

  WHAT A SYNTHETIC RESIDENT IS, stated because the number is worthless without
  it and the run prints it on every line carrying a population: the seven are
  authored and untouched, and EVERY RESIDENT ABOVE SEVEN IS A COPY OF ONE OF
  THE SEVEN WITH A VARIED SEED. Varied: the id, three traits jittered up to
  0.15, and who they are tied to at what weight. NOT varied: behaviour,
  circle, vocabulary, schedule, economy. The graph takes the authored eleven
  ties plus random pairs up to the AUTHORED MEAN DEGREE of 3.14, measured off
  the authored street rather than chosen. So this BOUNDS THE MACHINERY AND
  SAYS NOTHING ABOUT CONTENT.

  COST IS NOT THE PROBLEM, and that is the half everybody expected to be the
  answer. secPerDayPerRun across five rungs: 0.0003, 0.0008, 0.0013, 0.0026,
  0.0030, which fits about 0.4 ms per in-game day plus about 5.5 microseconds
  per resident per in-game day. NOTHING IS SUPERLINEAR. At 500 residents and
  500 in-game days, run twice: 1.5 s and about 1.2 MB of world state.
  Determinism held at every rung (identical per-day digests), no invariant
  broke on any of 499 closed days at any population, and no resident's
  remembered count ever fell.

  REACH IS THE THING THAT FALLS OVER, AND IT IS THE ONLY THING. Residents who
  ever remembered anything: 7/7, then 17/50, 15/200, 20/300, 15/500. THE COUNT
  IS FLAT AT 15 TO 22 ACROSS EVERY POPULATION AND EVERY SEED; the FRACTION
  collapses 1.000, 0.340, 0.075, 0.067, 0.030. At 200, 185 memory stores were
  EMPTY after 499 days; at 500, 485 were.

  THE MECHANISM IS PRINTED AND IS NOT EMERGENT: `deepestHopEver=2` in 2187
  hops at 200 residents, and 2 at every rung (3 once, on seed 2). The
  rememberers are the witness's two-hop neighbourhood, which at mean degree
  3.14 is 7, 22, 21, 29 and 20 people at the five populations. TALK REACHES A
  NEIGHBOURHOOD, AND A NEIGHBOURHOOD IS A CONSTANT OF THE MEAN DEGREE, NOT OF
  THE TOWN.

  THE CAUTION THE RUN PRINTS ITSELF, and it is instruments.md's rule about two
  numbers from one variable: THE WALL CLOCK AND THE REACH ARE ONE FINDING
  TWICE. The tick is cheap at 200 because 185 of them carry nothing, so the
  per-hour cost is a walk over everybody and real work over almost nobody. THE
  1.33 SECONDS IS NOT HEADROOM FOR A BUSY TOWN and must never be quoted as it.
  The mean rate falls 15.7x from 7 to 200 residents (0.361 to 0.023) while the
  rate among residents who hear anything at all barely moves (0.361, 0.344,
  0.311, 0.345, 0.401), and those two are not independent readings: the first
  is the second times remembered/agents. Both now print on one line with their
  denominators for exactly that reason.

  WHAT IT SUPPORTS: the Core's gossip and memory machinery runs 500 residents
  for 500 in-game days twice without breaking determinism, an invariant or
  permanence. Population is not a performance or a memory problem at this
  scale on this hardware.

  WHAT IT DOES NOT SUPPORT, two reasons that must not be merged: (1) above
  seven every resident is a copy with a varied seed, so this bounds machinery,
  not content or social variety; (2) "who all remember" is NOT APPROACHED and
  this instrument cannot approach it, because the synthetic residents have no
  lives of their own and the only thing anyone can remember is one player
  sighting entering through one witness. 15 of 200 remembering is a
  measurement of ONE SOURCE'S REACH, not of whether 200 residents can each
  hold their own memory stream.

  NAMED GAP, NOT BUILT: to measure "500 residents who all remember" the soak
  needs per-resident stimulus, and that is the run in which the snapshot cost
  per tick stops being free. Until it exists the cost numbers hold only for a
  town where about twenty people carry talk.

  CORRECTS A READING OF THE QUEUE 115 PROJECTION: `xMeasuredMean` inflates as
  coverage collapses (15.5x at 7 residents, 239.6x at 200), so that multiple
  is NOT COMPARABLE ACROSS POPULATIONS and must be read with the coverage now
  printed beside it.

  NO CORE BUG FOUND and the Core was not changed (`git status
  ledger/Assets/Scripts/Core/` empty). Two faults in the SOAK were found by
  running the never-ran case and fixed: an empty-series index that crashed
  `--days 1`, and a zero-days guard that printed `eventsPerNpcPerDay=Infinity`
  and `NaNMB`. Both now print NOTHING MEASURED with all three denominators.

  THE DONE LINE NOW CARRIES WHAT IT SUPPORTS, which is queue 116's other half
  and is what makes the instrument honest without a document beside it. THE
  REMAINING HALF OF 116 IS NOT DONE: the grep for citations elsewhere, with
  the count found and the count changed printed. That is a documents job and
  the brief scoped this spawn to the measurement.
