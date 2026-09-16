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
