# LEDGER

One session, on Jafar's PC, building a game. The old studio is archived under legacy/studio-v2/.

## What governs

canon.md (the world and content rules; it outranks everything), ROADMAP.md (milestones), DECISIONS.md (what is decided; its archive still binds), production/research/README.md (what governs each thing's look). The licence allowlist is law.

## Talking to Jafar

- He is not a programmer. Plain words, short. No paths, hashes, flags or tool output unless he asks.
- A finished piece of work: three lines. What changed; what it looks like, with the picture; what next.
- Ask him only about canon, scope or money: one multiple-choice question, your recommendation marked, and carry on with it meanwhile. The rest is yours.
- No voice is cast without his yes.
- If you got something wrong, one sentence, then move on.

## Records, and nothing more

- NOW.md: five lines of current state, under 150 words, no history. It carries the SITTING line (start time and limit) and the GOAL line (the sitting's goal, marked open or done).
- FOR-JAFAR.md: one dated summary at the end of each sitting, under 200 words: what changed, evidence, what failed or is unproven, what next, decisions he must make. Unresolved decisions carry forward; git keeps earlier summaries.
- DECISIONS.md: one entry per material choice: date, decision, reason, who decided, link. Routine implementation choices go in commit messages.
- FINDINGS.md: unresolved faults only, at most twenty.
- Records go in with the work they describe or in the closing summary. No commit that only updates notes during a sitting.
- The old records and the 979-item feature checklist are in production/archive/. The checklist is a reference, not a gate: check it for missing basics at each milestone; nothing waits on it.
- Why: the two audits in production/audits/.

## How a sitting runs

- Each sitting has a goal and a time limit (four hours if unnamed). Stop when the goal is done or time is up, with everything committed and the closing summary written.
- The stop hook has one job: while the goal is open and time remains, keep going; when either ends, stop. It reads NOW.md's SITTING and GOAL lines, for the builder's own session only (its id is in the untracked .claude/builder-checkout).
- If a goal turns out much bigger than it looked, tell him rather than push on.

## How to work

- Iterate locally: build and render in Unreal on this PC, look, fix, repeat; push only accepted work. Two Unreal builds must not overlap.
- Commits say in plain words what changed and why. Pushes run the Core tests and the Unreal build; a red run is fixed first.
- Simulation work (perception, memory, gossip, and their port) keeps its tests: CoreTests, Soak, SaveChaos, PerceptionGolden and StrangerTest before the commit, plus a regression test. The C++ port must match the C# golden table, regenerated from the C# Core for the comparison. It also gets one independent check: a subagent that has not seen your reasoning gets the change, its test, canon and the intended behaviour in plain words, and is told to break it.
- Visual work: references live in production/reference/ only. The concept sheet governs mood, palette and composition; the photographs (links only) govern what things looked like and win where they disagree. An asset gets two attempts against its reference, then is finished from dimensions or set aside.
- Subagents for bounded, parallel, mechanical tasks and for the independent check; never as a director.
- When two ways are both fine, take the cheaper one.
