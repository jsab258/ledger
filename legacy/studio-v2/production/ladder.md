# The plan's rungs: the visual ladder, under the stages

STATUS: LIVE. verified 2026-09-14. THIS FILE IS THE RUNGS OF THE PLAN. The arc
above it is `production/stages.md`, the six stages Jafar ruled on 2026-09-14
(D22); this file plus `production/queue/` is what he ruled the plan on
2026-09-10, in the same cleanup batch that gave the project one decision
register, and the stages now sit above it as the thing the rungs serve. Before
the 2026-09-10 ruling there were four plan documents and a reader had to guess
which one governed. The folds are recorded at the bottom of this file.

The ladder itself was ruled by Jafar 2026-09-09, item 5 of that
morning's message, and his own words are the whole specification: "The next
ladder is visual-first... The crime and gossip work continues underneath; the
ladder measures what I can see."

THIS FILE IS READ BY A MACHINE. `tools/map.py` renders the table below as the
project overview's first screen, so the columns are a contract: `rung`, `name`,
`status`, `done looks like`. Status is exactly one of `done`, `current`, `next`,
`later`. Exactly one row may be `current`. Change a rung's name here and the
map changes; there is no second copy.

WHAT THE LADDER MEASURES, AND WHAT THE STAGES MEASURE. The rung table below is
ONE AXIS, the one Jafar can see without being told what to look at, and it ends
at the Meridian Test's first condition: a person who loves GTA or KCD2 plays
thirty minutes and does not bounce off the visuals. The stages in
`production/stages.md` are the other axis: what gets built, in what order, and
what has to be true before a stage is done, with the phases' instrumented gates
folded under them. They are not two plans. The rung is what Jafar looks at this
week; the stage is what the work is for. `production/queue/` is where both turn
into items somebody can pick up. The current stage is read off the rung marked
`current` below and is typed nowhere else.

WHY IT IS VISUAL-FIRST NOW. The art line shipped its research and its plans and
skipped its visual half, and the channel was reporting counts rather than
outcomes, so two weeks of work were legible to the studio and invisible to him.
A ladder whose rungs are all pictures cannot have that failure.

## The rungs

| rung | name | status | done looks like |
|---|---|---|---|
| 1 | The street matched to the Hook sheet | current | The built Quay Street rendered from the SAME viewpoint as the lower panel of OUR OWN Hook sheet, approved by Jafar 2026-09-10 and made the reference panel in place of the outside one, with rain, a wet road, worn materials and sky, and you judging the two side by side. Your judgement is the gate; no number passes this rung. |
| 2 | Props read as their materials | next | Every placed prop reads as the material it is meant to be, and the first-batch clutter is placed per `production/art/atlas-01/PRODUCTION-CATALOGUE.md` on `origin/art/atlas-01`, which is where the atlas lives and not in this checkout, in a frame he can see it in. |
| 3 | Mickey's frontage on the street | next | The frontage stands on Quay Street at the bay count you rule. IT IS A MINICAB OFFICE, NOT A PUB, by your ruling 6 of 2026-09-10, so the design is `production/art/mickeys-cars/`, not `production/art/atlas-01/MICKEYS.md` on `origin/art/atlas-01`, which D17 supersedes for the trade while its siting, two bays and fascia stand. |
| 4 | People on the street | next | People on the street with varied bodies, not one body repeated, in a frame. |
| 5 | A face that moves and a voice | later | One face that moves and one voice, per decision record D2. |
| 6 | Mickey's enterable | later | He can walk in through the door he saw from the street, into the cab office drawn in `production/art/mickeys-cars/`: the waiting room, the counter and the speaking gap, with the drivers' room beyond it that the public never enters. |
| 7 | Your thirty-minute dry run | later | You play for thirty minutes. The four conditions of the Meridian Test are read off that session and nothing else. |

## The rule about the rungs

A RUNG IS CLEARED BY YOUR EYE, NOT BY A GATE. Every rung above describes a
picture or a session, and the studio's numbers exist to tell us whether the
picture is worth sending, never to declare the rung passed. CLAUDE.md rule 4 is
the reason: a green number may not stand in for the frame it claims to describe.

ONE RUNG AT A TIME, and the art line takes at most a quarter of the week's
points (ruled 2026-09-08, carried 2026-09-09). The crime, gossip and memory work
continues underneath on the rest.

A RUNG NEVER MOVES BACKWARDS QUIETLY. If a later landing breaks a cleared rung,
the row goes back to `current` and the reason is written into the row, because a
ladder that only climbs is a ladder that lies.


## The phases, and the exit gate each one gets out on

FOLDED AGAIN ON 2026-09-14, INTO THE STAGES. The phase rows and their exit gates
lived here from 2026-09-10 to 2026-09-14, copied in from
`ledger-v2/respec/roadmap-v2.md`. Jafar ruled the six stages on 2026-09-14 (D22)
and they are `production/stages.md`, ABOVE this file: the arc the rungs serve.
Every phase row and its gate now hangs under the stage it serves there, in the
section "The phases, folded in", together with the row law, the 2026-09-05 gate
repairs, the standing rule about time budgets at kickoff, and the validator
command for the systems census. Change a gate THERE and nowhere else. This
heading stays so the 2026-09-10 fold record below and `roadmap-v2.md`'s banner
still resolve. Which rung hangs under which stage is the table "Where the rungs
of production/ladder.md hang" in the stages file.

## The Meridian Test, which is the last gate of all

COPIED, NOT AUTHORED HERE. The source is
`ledger-v2/respec/vision-pillars-v2.md`, and `tools/goal-block-check.py`, run by hand
(nothing calls it yet; see the wiring item), checks that the copy in
`CLAUDE.md` matches that source. IT DOES NOT CHECK THIS COPY.
If this one and the source ever differ, the source wins and the difference is a
bug in this file.

The goal is met when all four hold:

1. A person who loves GTA or KCD2 plays 30 minutes and does not bounce off the
   visuals.
2. Within those 30 minutes the world visibly knows them at least once:
   recognized, gossiped about, or confronted with something they did earlier.
3. They describe the town as alive without being prompted.
4. Jafar, on a free evening, chooses playing LEDGER over replaying KCD2.

Rung 7 above is where those four get read, off one session and nothing else.

## The fold of 2026-09-10: what folded in, and what could not move

Jafar ruled one plan in the cleanup batch of 2026-09-10: this file plus
`production/queue/`. What folded in, and what did not:

- `ledger-v2/respec/roadmap-v2.md` FOLDED IN and STAYED AT ITS PATH. Its phase
  rows and their exit gates were above, and its stale systems column was replaced
  by the validator command. The file could not move under `legacy/`
  because `CLAUDE.md` line 133 names it as the plan and `.claude/agents/planner.md`
  line 3 tells the planner to decompose its milestones, and a separate lane owns
  both of those files. `tools/dashboard/build-dashboard.py` also parses its phase
  table (`SOURCES["roadmap"]`, and `parse_roadmap`). So the file keeps its path
  and now carries a banner saying the plan is here.
- `production/quality-ladder.md` STAYED IN PLACE, unfolded, and it is not a
  second plan. It is the close-question instrument of this one: before an item
  closes, is this the best available result or the first working one. `CLAUDE.md`
  line 205 names it as the place that question is asked, so it cannot move
  either.
- `game-design/queue.md` was already retired and is not touched.
  `tools/queue-check.py` prints `retiredNotRead=game-design/queue.md`.
- `production/week-plan.md` was already gone.

## The fold of 2026-09-14: the stages above, the phases out

Jafar ruled D22 on 2026-09-14: the plan is two documents, the stages above this
ladder and the visual path as a decision record. What moved:

- The phase rows and gates that sat in this file since 2026-09-10 moved whole
  to `production/stages.md`, each under the stage it serves. Nothing was
  deleted; the section above is now a pointer.
- `ledger-v2/respec/roadmap-v2.md` is retired as a plan document and says so in
  its first lines. Its table stays at its path as parser input for the dashboard
  until `SOURCES["roadmap"]` is repointed.
- The visual path is `ledger-v2/respec/decision-register/D31-the-visual-path.md`,
  the route inside stage 1, feeding rung 1, then 2 and 3.
- The rung table above did not change by one byte. Ruling:
  `game-design/decision-2026-09-14-ruling-the-plan-is-two-documents-and-the-phases-fold.md`.
