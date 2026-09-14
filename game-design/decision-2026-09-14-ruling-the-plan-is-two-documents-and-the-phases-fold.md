# Ruling, 2026-09-14: the plan is two documents, the phases FOLD into the stages, and roadmap-v2.md is retired as a plan document

STATUS: LOG, 2026-09-14. NOT CURRENT after this date: the live plan is
`production/stages.md` over `production/ladder.md`, and the visual path is D31.
Written by the studio-director spawned for D22. No builder work is in this
batch, every file below was written by the director, so `director_cadence` has
nothing to cover and this record carries no spawn stamp. The resident commits.

## What was asked

D22, Jafar, 2026-09-14: record the plan as two documents, the stages above the
ladder and the visual path as a decision record, and "fold roadmap-v2's phases
into this or retire them, and say which. Two plans in one repository is how the
ladder came to disagree with the roadmap before."

## The decision: FOLD the phases; RETIRE the file as a plan document

The phases R and 0 to 6 of `ledger-v2/respec/roadmap-v2.md` are FOLDED into
`production/stages.md`: each row and its instrumented exit gate hangs under the
stage it serves, in that file's section "The phases, folded in", and a gate is
changed there and nowhere else. `roadmap-v2.md` is RETIRED as a plan document
and says so in its own first lines, pointing at the stages. Its phase table
stays byte for byte as parser input for one program, named below, until that
program is repointed. The phases section of `production/ladder.md`, which had
carried the rows since the fold of 2026-09-10, becomes a pointer to the stages,
so the rows have exactly one prose home.

## Why fold and not retire the phases

1. THE GATES ARE THE ONLY INSTRUMENTED HALF OF THE PLAN. The six stages are
   judged by Jafar's eye (D23) and the ladder's rungs are cleared by his eye;
   the phase gates are measurements: the gossip instrument green, arrest
   callers counted and printed, Core tests passing, a resolved blow from a
   call site outside Core, the repetition blind test. Retiring the phases
   retires the gates, and stage 3, the milestone to protect, would have no
   instrument under it. M17.10's lesson, carried with the rows since the
   respec: instrumented phases, bounded milestones.
2. THE LABELS ARE KEYS. `production/systems-inventory.json` line 50 says every
   system's `phase` "names a row in ledger-v2/respec/roadmap-v2.md", over the
   91 entries the validator counted on 2026-09-10. `tools/dashboard/build-dashboard.py`
   parses the phase table (`SOURCES["roadmap"]` at line 417, `parse_roadmap` at
   311, `read_phases` at 577, measured 2026-09-14) to derive its current-phase
   reading. Retiring the labels is code and data work across two tools and the
   whole inventory for no gain in clarity. Rule 5: look before you destroy.
3. THE FAULT D22 NAMES IS COPIES, NOT LABELS. Before this ruling the phase rows
   had two prose homes (the roadmap's table and the ladder's bullets), and a
   third document was arriving. After it: one prose home (the stages), one
   machine table (the roadmap's, frozen and marked as parser input), one rung
   table (the ladder's). What comes next is answered by one rule in all three
   places: the current stage is the one whose ladder rung is `current`.

## The options that were weighed

- A, FOLD, as above. Cost: two new files, four files edited, ten pointer edits
  owed to other lanes. Outcome: one answer to "what comes next" from any door.
- B, RETIRE THE PHASES OUTRIGHT. Six stages only; gates re-homed as stage
  instruments; every phase label removed. Cost: the inventory retyped, a
  dashboard reader rewritten, queue specs that name a phase gate (070, 098,
  100, 102, 107, 900) re-read. Outcome: the same one answer, at the price of a
  code change in a batch that is document work, and a week where the map's
  current-phase card reads nothing measured.
- C, ADD THE STAGES AND TOUCH NOTHING ELSE. Cost: nothing. Outcome: three
  documents carrying the phase rows, and the exact drift D22 forbids.

A was taken. B is the right end state once the dashboard is repointed and is a
queue item, not a ruling.

## What was written and edited, by path

- `production/stages.md` NEW. Document one: the six stages in his words, each
  with its bar, the rungs of `production/ladder.md` and the rows of
  `production/quality-ladder.md` placed under it, the phases folded in with
  their gates verbatim, the lanes (D26, D29, D30), the 2026-09-10 closure
  finding, and the one-source rule for what comes next. 398 lines when read
  back after writing, under the 400-line cap a live plan carries by two lines:
  the first draft read back at 416 and was trimmed twice. No tool enforces the
  cap under `production/` (`tools/docs-check.py` walks `game-design/` only), so
  the margin is a convention and the next edit that grows the file moves a
  section out rather than crossing it.
- `ledger-v2/respec/decision-register/D31-the-visual-path.md` NEW. Document two:
  the five-point order with his reasons, D28's ten steps placed inside it as one
  list with the queue items that carry each, the one inverted adjacency named,
  the estimate as PLAN-TO-TEST with the one measured piece it stands against
  named, the exclusions, the target frame, the pace rule.
- `ledger-v2/respec/roadmap-v2.md` EDITED: the banner now says retired as a plan
  document on 2026-09-14, names the stages, names the one parser and the four
  pointers that hold the file at its path. The table and everything below the
  banner are unchanged; the table was read back after writing and matches.
- `production/ladder.md` EDITED: the phases section is a pointer to the stages;
  the fold record gains a 2026-09-14 entry; the title no longer says the phases
  are underneath. THE RUNG TABLE IS BYTE FOR BYTE UNCHANGED, read back after
  writing, because `tools/map.py` reads every table row in the file and treats
  the first table's header as the rung contract. This edit fires
  `publish-glance` on push, which is cheap and expected.
- `game-design/roadmap.md` EDITED: the tiebreak stub delegates to the stages.
- `ledger-v2/respec/decision-register/rulings-log.md` EDITED: D31 added to the
  spine; this ruling added to the date-ordered log; the resident's line for the
  twelve-rulings record, which a concurrent lane had inserted between two
  2026-09-10 entries, moved into date order.
- `ledger-v2/respec/decision-register/D22-...md` EDITED: a discharge section at
  the bottom naming where the two documents landed.

## Edits owed to other lanes, dictated exactly, none made here

1. `CLAUDE.md` line 133 to 134 (rule 10). Replace "The plan is
   `ledger-v2/respec/roadmap-v2.md`; the live queue is `production/queue/`,
   with `production/NOW.md` for what is already moving." with "The plan is
   `production/stages.md` (the six stages, D22) over `production/ladder.md` (the
   rungs Jafar judges by eye); the live queue is `production/queue/`, with
   `production/NOW.md` for what is already moving." Director-gated; this ruling
   is the ruling.
2. `ledger-v2/respec/vision-pillars-v2.md` line 12, Jafar's own document: "This
   gate sits at the end of roadmap-v2.md." becomes "This gate sits at the end of
   production/stages.md, beyond its sixth stage." Then re-copy the goal block
   into `CLAUDE.md` (its line 17 is the copy) IN THE SAME COMMIT and run
   `python3 tools/goal-block-check.py`, which refuses any difference between the
   two. The sentence is a pointer and not a premise, so the recommendation is
   to make the edit on his one word rather than leave the goal block naming a
   retired file.
3. `.claude/agents/planner.md` line 3: "Decomposes roadmap-v2 milestones into
   production/queue task files" becomes "Decomposes the stages of
   production/stages.md, and D31's steps, into production/queue task files".
4. `ledger-v2/studio-v2/operations.md` line 26: "as instrumented in
   roadmap-v2.md" becomes "as folded into production/stages.md"; lines 59 to
   60: "the v2 plan is ledger-v2/respec/roadmap-v2.md" becomes "the plan is
   production/stages.md over production/ladder.md".
5. `ledger-v2/handoff/HANDOFF.md` line 8: append "(roadmap-v2 retired
   2026-09-14; the plan is production/stages.md)".
6. `production/systems-inventory.json` line 50, the `howToRead` sentence: "phase
   names a row in ledger-v2/respec/roadmap-v2.md" becomes "phase names a row R
   or 0 to 6 of the phases folded into production/stages.md". Data, so a
   builder's edit under the validator.
7. `tools/dashboard/build-dashboard.py` `SOURCES["roadmap"]`: a queue item, not
   a doc edit. Repoint at `production/stages.md` and let `parse_roadmap` accept
   a header whose first cell is `stage` as well as `phase`; the stages table
   there has the same first three columns. Until then the roadmap's table stays.
8. `production/quality-ladder.md` lines 56 to 61, "What is deliberately NOT on
   the ladder yet: everything visual ... the engine is undecided": stale since
   D16 (Unreal) and since the visual ladder of 2026-09-09. Replace the
   paragraph with: "Visual rows now hang under the stages of
   production/stages.md, section 'Where the quality ladder's rows hang'; the
   engine is Unreal by D16."
9. `game-design/decision-2026-09-07-jafars-five-rulings-and-the-order-of-the-game.md`
   section 6, "The game, in order" (walkable street, one crime, one overheard
   consequence): all three landed on 2026-09-08 per `production/next-three.json`,
   and the order of the game since is the visual ladder of 2026-09-09 and the
   stages of 2026-09-14. Add one line under the heading saying so; the file
   reads LIVE and a session that opens it reads an order two rulings old.
10. `production/next-three.json` line 71 still says "The pub's frontage" and
    "whether it is a free house". D17 and D19 retired both. The map renders this
    file to his phone. One-line data fix by whoever next edits the file under
    its own rules.

## Raised to Jafar, three lines, each with a default

1. STAGE 3 HAS NO RUNG. The ladder's seven rows are the street, its people,
   Mickey's and the session; the crime loop in the finished street has no row,
   so the protected milestone cannot be seen to slip on the instrument he
   reads. Proposed: a rung after rung 5, "The street knows me: one crime, one
   witness, one overheard consequence, in the frame that looks right". Default:
   the gap is recorded in the stages and nobody but him edits the rung table.
2. WETNESS AND SURFACES ARE ADJACENT IN BOTH HIS LISTS AND IN OPPOSITE ORDER.
   D22 says surfaces then wetness; D28 and his 2026-09-09 sequence say wetness
   then worn materials. D31 follows D22 as D22 itself instructs, and wires
   wetness when queue 186 lands while judging it after the material library.
   Default: as D31 has it.
3. THE ART QUARTER AND THE VISUAL-SLICE WEEK. `production/ladder.md` still says
   the art line takes at most a quarter of the week's points (ruled 2026-09-08);
   the 2026-09-14 ruling says the week is the visual slice and two thirds of
   spend goes to the ladder, the slice and the moat. The reading that reconciles
   them is that the quarter governs the in-house art line's commissions and not
   the slice on the runner. Default: that reading, and the sentence in the
   ladder stands until he says otherwise.

## Contradictions found with what Jafar was told, or with what a session reads

- `CLAUDE.md` line 133 has called `roadmap-v2.md` "the plan" since 2026-09-01
  while `roadmap-v2.md` has said since 2026-09-10 that it is not. Edit 1 above.
- The goal block he approved on 2026-08-31 says the Meridian Test "sits at the
  end of roadmap-v2.md". Edit 2 above.
- 182 of the 265 files at the top of `production/queue/` were closed on
  2026-09-10 with the line "not on the ladder", among them the crime loop
  milestone (138), the weekly process audit (900), the row-law checker (107)
  and every item the quality ladder's next rungs cite for stages 2 and 3. No
  record under `game-design/`, `ledger-v2/` or `production/NOW.md` contains that
  phrase (measured 2026-09-14). The stages put those items back on the route,
  and the rule from here is written in `production/stages.md`.
- `production/quality-ladder.md` says the engine is undecided and nothing
  visual is on the ladder. Both false since 2026-09-09. Edit 8.
- `production/next-three.json`, rendered to his phone, calls Mickey's a pub with
  a free-house question. Edit 10.
- `production/week-plan-2026-09-08.md` reads LIVE for a week that ended on
  2026-09-13 and carries a different order (the crime item first). Not edited;
  the 2026-09-14 ruling supersedes it and a week plan for W38 is the planner's.
- The Sunday page D30 names as the second home of the narrative debt does not
  exist: none of the thirteen top-level documents in `production/` is one and
  `tools/producer-check.py` line 173 records that the Sunday summary has no
  register yet. The stages carry the debt under stage 3 until it does.

## What this record does not do

It does not edit `CLAUDE.md`, the goal block's source, the planner's brief, the
inventory or any tool: those are named above with their exact text and belong to
their lanes. It does not move `roadmap-v2.md` under `legacy/`, because one
program still parses it. It does not touch the rung table.
