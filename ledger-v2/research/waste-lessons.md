# Waste lessons (extracted 2026-08-31 from agent-reports/process-faults-25aug.md, both CLAUDE.md files, roadmap-history.md)

Each lesson is now an operating rule in studio-v2/operations.md. Named failures, kept so nobody relearns them at full price.

1. maxTurns ceilings too tight: four parallel agents, about 398k tokens, zero delivered on first pass, several stopped one step short of done. Rule: generous ceilings, resumable state files, one deliverable per brief.
2. Standing constraints retyped into every brief. Rule: constraints live in agent definitions.
3. Multi-deliverable briefs caused partial delivery counted as none. Rule: one brief, one deliverable.
4. Shared scratchpad filename collisions corrupted outputs (including a commit message). Rule: per-agent namespaced scratch.
5. Single-writer commit gate fought multi-agent work. Rule: branch per agent, integrator merges.
6. Giant stale roadmap rows re-read at top-model prices; rows drifted for weeks; audits, not the plan, found 17.6 to 17.9. Rule: 80-word row cap, verified dates, doc-decay gate, history file on landing.
7. Top-model usage for mechanical work. Rule: routing law plus token ledger with recorded escalations.
8. Decisions living only in session memory (the era drift caught 2026-08-31). Rule: canon.md plus decision records; anything decided verbally gets written the same day.
9. Lessons 1 and 3 were relearned at full price on 2026-09-16, which is the thing this file exists to prevent. EIGHT agents hit their turn limit without delivering across roughly 1.3M tokens; several had FINISHED the work and never reported it, and one spent 49 calls and wrote nothing. Lesson 1 already said ceilings too tight, zero delivered, stopped one step short. Lesson 3 already said one brief one deliverable, and the brief that failed worst named four call sites across 13,734 lines. THE NEW HALF, measured that day: 0 of 16 agent definitions declare a turn budget, and the real limits differ by role (45 for engine-specialist, 70 for the builders), so every instruction of the form "hand back when you are N through your budget" asks an agent to measure itself against a number written nowhere it can read. Rule: a stop condition names a COUNTABLE exit the agent tallies itself (a tool-call count, or a number of failed attempts), it has TWO exits because one tied to success cannot fire on failure, and each definition states its own budget so the dispatcher sets the tally honestly. First dispatch under that form delivered at call 26 of 30.

## Checked negatives, kept so nobody commissions them

Things deliberately NOT to be worked on, with the reason and whose call it was. A negative is only useful if it is findable before somebody spends a week.

- **World streaming at Phase B scale. Jafar, 2026-09-16.** Unreal's World Partition already does tiled distance-based streaming with a memory budget, and Phase B's ten to fifteen square kilometres is an order of magnitude under what would need a bespoke system. NOT A RESEARCH QUESTION. The engine claim is his and is not re-derived in this repository, which cannot benchmark World Partition; the tree's only mentions (D1-engine-probe.md:4, the feasibility research at :5 and :28) name it as a capability rather than measuring it. WHAT IS NOT COVERED BY THIS NEGATIVE, and the distinction is the whole reason it is written down: residents OUTSIDE the streamed slice must keep perceiving, remembering and gossiping, because GTA can unload people only since nothing is lost when it does. That half is queue 351 and is a MEASUREMENT, not research.

