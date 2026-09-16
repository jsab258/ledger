line: studio (.claude/agents/*.md)
spec: An agent that hits its turn limit mid-investigation delivers NOTHING, and
  the resident cannot tell that outcome apart from an agent still thinking.
  Five of fifteen agent definitions tell their agent to hand back what it has
  before the limit. THE FIVE ARE ALL BUILDERS. Every pure verifier except
  guard-tester lacks it, and so does the studio-director, which is the most
  expensive role in the studio and therefore the worst one to lose silently.
acceptance: every definition whose output is a REPORT carries the instruction,
  in its own words rather than pasted, and it names what a partial report must
  contain: what was measured, what was only looked at, and what was never
  reached
max_sessions: 1
status: READY 2026-09-16, filed from an incident an hour old.

  MEASURED, one line per definition, 16 files of which README is not an agent:

      HAS   engine-specialist  guard-tester  instrument-builder
            systems-builder    world-designer
      LACKS artifact-reader    claim-auditor  measurement-auditor
            reach-auditor      studio-director  producer  planner
            integrator         content-wrangler  dialogue-writer

  So 5 of 15. The split is not random: the BUILDERS were taught this and the
  REPORTERS were not, which is backwards. A builder that dies mid-task leaves a
  diff on disk that the next session can read. A verifier that dies mid-task
  leaves nothing at all, because its entire deliverable is the report it never
  wrote.

  THE INCIDENT. An artifact-reader spawned at 06:47Z to judge run 48's day
  frames against the Hook sheet ran 59 tool calls and 146,812 tokens and
  stopped at its 40-turn limit with no report delivered. Resuming it recovered
  the work, so the cost is a round trip rather than the whole spend, but the
  recovery was the resident noticing, not anything in the system.

  AND THE BRIEF WAS HALF THE FAULT, which this item should not let the
  definition take alone. It asked for four findings plus a comparison image and
  named no order of importance, so the agent had no way to know which one to
  secure first. A brief that wants four things says which two it would keep.

  THE LIVE RISK WAS HANDLED BY HAND, which is the evidence this belongs in the
  definitions rather than in the resident's memory: a studio-director was
  running on the night-lighting batch while this was being written and had to
  be sent the instruction as a message, one agent at a time, because its
  definition does not carry it.

REWRITTEN 2026-09-16 AROUND THE ACTUAL DIAGNOSIS, which the day disproved.
This item said the verifiers were never told. They were told, and it did not
matter.

  THE COUNT BY THE END OF THE DAY: SEVEN agents hit their turn limit without
  delivering, across roughly 1.2M subagent tokens. Several had FINISHED THE
  WORK and simply never reported it, which is the worst version: the diff was
  on disk and the resident could not tell it from an agent that had died doing
  nothing.

  THE INSTRUCTION WAS PRESENT AND DID NOT FIRE. Two of the seven had
  deliver-before-your-limit in their agent definition AND in the brief. The
  studio-director had it only because it was sent by hand mid-run. So the fix
  this item originally proposed, put the sentence in the definitions that lack
  it, IS NOT THE FIX. It is necessary and it is not sufficient, and shipping
  only that would have closed this item while the failure continued, which is
  the queue 111 fault.

  WHY IT DOES NOT FIRE, stated as the best available reading and not as a
  measurement: "when you are two thirds through your budget" asks an agent to
  estimate a quantity it cannot observe. It has no reliable view of its own
  remaining turns, so the instruction is an instruction to guess, and an agent
  mid-task guesses that it has room.

  WHAT WORKED, AND THE ONE THAT DID NOT. A MECHANICAL condition tied to an
  OBSERVABLE fires: "hand back the first time this gate passes" was obeyed by
  the builder that met it. But the seventh death was an agent given exactly
  that condition, because A CONDITION TIED TO SUCCESS CANNOT FIRE WHEN THE
  WORK DOES NOT SUCCEED. It had no way to stop having not reached green, so it
  worked until the limit took it.

  SO THE CONDITION MUST BE TWO-SIDED, and the second side must also be
  observable: hand back when the gate passes OR when a named count of attempts
  is spent, whichever comes first. A stop condition with one exit is a stop
  condition for the happy path only.

  ACCEPTANCE, REPLACING THE ONE ABOVE: every definition whose output is a
  report carries a two-sided stop condition naming both exits in observable
  terms, and the brief template names the deliverable that is due at the
  UNSUCCESSFUL exit, because "hand back what you have" is a judgement and
  "name every file you touched and say whether it compiles" is not.

