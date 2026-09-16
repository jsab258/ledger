line: simulation (Core: Suspicion, Gossip, Claims, Acquaintance; canon's
  remediation clause)
spec: RAISED BY JAFAR 2026-09-16 FROM AN EXTERNAL RED TEAM, and he ruled its
  class before filing it: A DESIGN GAP, NOT A BUG. Nothing here is behaving
  wrongly; the thing that would let a player back has never been built.

  THE ARGUMENT. Memory is permanent by design, confidence has a floor, and
  rumours are indelible. So every escalation runs ONE WAY: the town can close
  against a player and there is no route back. Canon says remediation is
  BEHAVIOURAL. Nothing implements it.

  WHY THIS CHANGES THE PLAN RATHER THAN THE CODE. Pillar 1 is the moat and the
  permanence IS the moat; a forgetting mechanic would buy a route back by
  spending the thing the game is for. So the fix cannot be forgetting. Jafar's
  own framing, which is the brief for whoever takes this: "not forgetting, but
  acting on what people believe."
acceptance: a player who has been closed against has at least one route that
  changes what the town BELIEVES without anything being forgotten, reachable
  inside one sitting, and the route is legible enough that a player can tell it
  worked; permanence is untouched and provably so, with the memory store's own
  tests still green
max_sessions: 3
status: READY 2026-09-16, filed and NOT started, per his standing rule. Before
  the slice it is a card; after it, work.

  THE SMALLEST THING, PROPOSED AND NOT DECIDED, because he asked for a proposal
  and the ruling is his. THE VOUCH. One resident who has direct positive
  experience of the player, and who has standing of their own, can say so, and
  that statement enters the gossip mill AS A CLAIM WITH A SOURCE exactly like
  any other. Nobody forgets anything. What changes is which belief dominates
  when two accounts of the player compete and one has a better source.

  WHY THAT SHAPE AND NOT ANOTHER, from what already exists rather than from
  taste:
  - THE MACHINERY IS BUILT. `Claims.cs` already raises suspicion 0.15 on a
    contradiction and lowers it 0.03 when a story checks out, so belief already
    moves on evidence in both directions. The mill already carries source and
    credibility. A vouch is a claim with a good source, not a new subsystem.
  - IT IS BEHAVIOURAL, WHICH IS WHAT CANON ASKS FOR. The player earns the
    voucher by dealing with them, so the route back is play rather than a menu.
  - IT CANNOT LAUNDER EVERYTHING, which is the design's protection. A voucher
    with weak standing moves little; a voucher who is themselves distrusted
    moves less; and a witness to the original act still holds a first-hand
    memory that a second-hand vouch does not overwrite. The asymmetry that
    makes the town feel real survives.

  WHAT WOULD MAKE THIS WRONG, named so it is watched: if a vouch overwrites
  first-hand memory it is forgetting wearing a costume, and pillar 1 is spent.
  The 2026-09-16 fix to `PlayerClaims` is the precedent to follow, where a
  caught lie is REFUSED rather than allowed to replace a witnessed fact.

  AND ONE THING TO MEASURE BEFORE BUILDING ANYTHING: whether the town actually
  closes in play, and how fast. The claim is structurally sound and nobody has
  run it. A soak that escalates a player and reports the rung distribution over
  time would say whether this is a thirty-minute problem or a fifty-hour one,
  and the answer changes how small the smallest thing needs to be.
