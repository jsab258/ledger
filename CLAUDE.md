# LEDGER

How the production session on Jafar's PC works.

## Project facts (every session and prompt)

Third-person, never first-person. PC only, Windows. Britain, 1990 (canon's window 1988 to 1992). No alcohol or gambling, shown or spoken of; tobacco allowed; no children anywhere; the rest is canon.md's content rule.

## Read first

canon.md (outranks everything), CHARTER.md, RULINGS.md, PLAN.md, NOW.md, CATALOGUE.md. The licence allowlist (ledger-v2/research/license-allowlist.md) is law. DECISIONS.md: append, don't read to start.

## One session, a weekly budget

- One production session, on main and wip. Town work (simulation, claim check, casting, story) and clothing work (Blender, in F:\LedgerTools) are bounded tasks handed out with versioned inputs and acceptance cases, checked on return, never unattended lanes; TOWN.md and CLOTHES.md hold their briefs.
- Each week: 70% production, 10% independent review, 20% kept for him; he reads the meter and stops the session when it is spent. Each task's time is recorded (tools/timelog.py).
- His orders come on Mondays; between them only a broken game or PC, or a deliberate change of scope stating what it displaces and its cost.

## Talking to Jafar

- Not a programmer: plain words, short; no paths, hashes, flags or tool output unless asked.
- Finished work in three lines: what changed; the picture; what next.
- Ask only about canon, scope or money: one multiple-choice question, recommendation marked; carry on meanwhile.
- Wrong: one sentence; move on.

## Records

- RULINGS.md: his ruling replaces its line the same day; if code must change a ruling, ask him first.
- DECISIONS.md: one entry per material choice (date, decision, reason, link); decide within canon and his rulings, record, carry on.
- NOW.md: the current phase's items from PLAN.md, one line each naming its file, a line of state, open handovers. tools/doc-caps.py sets and fails the word caps (this file 1,000).
- FOR-JAFAR.md: the day's summary by 07:00, under 200 words, what failed named, ending in something to act on. Above it the overview (by 07:30 and on change): retention's line, current and next item, the tester's paragraph, Mondays risks in five lines, Needs you (at most five, recommended, gone once answered), Road to worth playing; every number real or marked not.
- Morning pictures: by 07:30 daily, the same three views (hook camera by day, reverse view, street at night) as previews, in the overview beside yesterday's and the Hook sheet; no decision.
- The approval pages' answers are read into the repository nightly, and read before any summary.
- FINDINGS.md: open faults only, at most twenty. No notes-only commits except the day's summary, whose commit runs the backup.
- Audits in production/audits/; each finding ends as a ruling, a rule or a list item.

## One home per fact; reuse first

- Each kind of fact has one home (CATALOGUE.md's homes table); all else derives from it and is checked against it.
- Before making anything new, search CATALOGUE.md, canon, the research library and every branch; use what exists, or say in DECISIONS.md why it is replaced.
- Anything touching taste or identity (a map, a face, a voice, the look) reaches him on one page before merging.
- Rules alone have not held, so each gets a check failing the build where possible: a branch over a week old neither merged nor archived; a derived thing disagreeing with its home; new art or research without a catalogue line.

## How the work is done

- The NOW.md list in order, one item at a time, each finished with its evidence, then the next unasked. A fresh reviewer checks each phase's exit. An item much bigger than it looked: tell him.
- A sample that cannot pass within its capped budget: report the failed capability plainly; never disguise it as another plan.
- Research first (production/research/): the professional method end to end, dated, before any symptom, before trusting memory or calling anything impossible; on failure, question the method. An unreached source is never evidence.
- Two tries, then research; a third failure is set aside, named in the summary and, if the game needs it, in Needs you, with research in another direction.
- Done means in the packaged release build, walked by the AI tester; a big item is "ready for review" until he passes it. Nothing is multiplied before he approves one complete sample in the assembled game.
- The gate: your check against real references (photographs, the approved face, the casting sheet, the accent by ear), then a fresh reviewer's: visuals against the Hook sheet and KCD2 frames, clothes their floor; no visible fault or placeholder; a visible change since he last looked. A step passes when its reviewer fails it only on narrow points later steps deal with.
- His page (people, street frames, story, menace, canon, money, licences, scope, taste, identity): one a day, one phone screen, at most three one-line decisions with recommendations, picks stored; pictures full size; shortfalls first; yes only for 2026-grade work; nothing his rulings settle.
- Approvals live beside what they approve and lapse with their basis (tools/approvals.py).
- Simulation: CoreTests, Soak, SaveChaos, PerceptionGolden, StrangerTest and a regression test before committing; the port matches the C# goldens.
- Subagents for bounded tasks and independent checks, never as director; of two fine ways, the cheaper.

## Builds, git and disk

- Unfinished work goes to branch wip daily and after each finished piece, with previews; main gets only what passed review (fetch and rebase first), never on a failing check. Two Unreal builds never overlap. Commits say plainly what changed and why.
- Git holds text and small files, plus previews (JPEG, ~1600 px, under 500 KB) in production/previews/; tools/git-size-guard.py runs on every commit; never --no-verify.
- Write only where production/retention.json names; lasting inputs in F:\LedgerTools; nothing large on C:. Before any build or render: `python tools/retention.py space --job "what" --drives CF`; a full disk: stop and wait.
- Delete only what retention limits cover; else his yes on a page; nothing of his is touched.
