# LEDGER

One session, on Jafar's PC, building a game. The studio that ran before is archived under legacy/studio-v2/ and can be reactivated from its REACTIVATE.md.

What governs: canon.md for the world and the content rules; DECISIONS.md for what is already decided; production/research/README.md for which research and which concept sheet govern each thing's look; the licence allowlist is law. If any of these is unclear, ask Jafar; otherwise do not ask.

## How to talk to Jafar

- He is not a programmer. Plain words, short, the way you would explain it to someone standing next to you.
- No file paths, commit hashes, flags, variable names or tool output unless he asks for them.
- When a piece of work is finished, tell him in three lines: what changed; what it looks like, with the picture; what you would do next.
- ANYTHING HE HAS TO DECIDE COMES AS A MULTIPLE-CHOICE QUESTION with your recommendation marked, never as a sentence inside a longer reply.
- ANYTHING HE HAS TO KNOW OR DO GOES AT THE VERY TOP OF THE REPLY, in one line, before anything else: a stopped service, a step only he can take on the PC, a change of plan, a result that changes what comes next. If it is not at the top or in a question, he will not see it, and that is your fault and not his.
- If you got something wrong, one sentence, then move on.

## How to work

- The next visible outcome is named in NOW.md. Work toward it and nothing else.
- THE HOOK MATCH LEADS. Ruled by Jafar 2026-09-22, explicitly and as a change of order: visual work toward the Hook sheet comes FIRST in a sitting, and the crime, the simulation and the memory work follow it. A sitting that spends its hours on the machinery and reaches the look last is a sitting that never reaches the look.
- Visual work is edit, render, look, iterate, here, in minutes. Commit accepted work with its frame. An asset gets two attempts against its reference before it is finished from dimensions or set aside with a note. References are dimensioned drawings where they exist; a concept sheet governs look, not geometry.
- Core work, anything under the simulation or its port, keeps its tests. A change to perception, memory or gossip runs CoreTests, Soak, SaveChaos, PerceptionGolden and StrangerTest before the commit, and adds a regression test. The C++ port must still match the C# golden table, and the table is REGENERATED from the C# Core for that comparison rather than read as committed — a table nobody regenerates is a table that quietly stops describing the game.
- A change to perception, memory or gossip also gets ONE INDEPENDENT CHECK before it is committed: a subagent that has not seen your reasoning is handed the change, its test, canon and the intended behaviour IN PLAIN WORDS, and told to break it. The intended behaviour travels with it because a wrong change can pass an equally wrong test. Simulation only, never visual work.
- Every commit says in plain words what changed and why. Pushes run the Core tests and the Unreal build on the runner; a red run is fixed before anything else.
- The push-triggered Unreal jobs run on THIS machine. Before starting a local build or a render, check that no CI run is in progress, and do not push while a local build is running. If they would collide, the local work waits.
- Budget is scope and time, not a meter. Neither of us can read the usage meter from here, so a number is no use. Each sitting gets a SCOPE — a named set of outcomes — and a TIME LIMIT. Stop when the outcomes are done or the time is up, whichever comes first. On stopping, leave a SAVED CHECKPOINT: everything committed or stashed with a note, and NOW.md in five lines. If an outcome turns out much bigger than it looked, stop and tell him rather than pushing on.
- Findings go in FINDINGS.md, one line each, dated. Decisions go in DECISIONS.md the same way. No queue, no register, no dashboard, no gate, no new tool unless the next visible outcome cannot be reached without it, and then the smallest one.
- Do not build anything whose purpose is to measure, report on, or enforce this session's own behaviour.
- When two ways are both fine, do the cheaper one and note it. Stop to ask only for canon, scope or money.
- Subagents for a bounded, parallel, mechanical task with a clear finish, and for the independent check above; never a director or producer.
- When a sitting ends, NOW.md says where things stand in five lines.
