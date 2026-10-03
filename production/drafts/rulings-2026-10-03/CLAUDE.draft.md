# LEDGER

How the three sessions on Jafar's PC work; what is decided is in RULINGS.md.

## Project facts (every session and prompt gets these right)

Third-person, never first-person. PC only, Windows. Britain, 1990 (canon's window 1988 to 1992). No alcohol or gambling, shown or spoken of; tobacco allowed; no children anywhere; the rest is canon.md's content rule.

## Read first

canon.md (outranks everything), RULINGS.md, NOW.md, your own status file, ROADMAP.md. The licence allowlist (ledger-v2/research/license-allowlist.md) is law. DECISIONS.md is the history: append to it; do not read it to start work.

## Sessions

- Builder, on main: the Unreal project, art, faces, voices; the graphics card is the builder's first.
- Town, branch town: the simulation, the claim check, casting sheets, the story; never Unreal, art, voices or the graphics card.
- Clothing: Blender only, light on the graphics card, on the bodies in F:\LedgerTools\bodies; garments to F:\LedgerTools\garments.
- Handovers: single lines in NOW.md naming the exact asset version they fit (MH_LenaS4, not "Sheila"), checked current by the receiver.

## Talking to Jafar

- Not a programmer: plain words, short; no paths, hashes, flags or tool output unless asked.
- Finished work in three lines: what changed; the picture; what next.
- Ask only about canon, scope or money: one multiple-choice question, recommendation marked; carry on meanwhile. Nothing waits on his hands.
- Got something wrong: one sentence; move on.

## Records

- RULINGS.md (at most 2,500 words): his ruling replaces its line the same day and becomes a list item with its specifics; if code must change a ruling, ask him first.
- DECISIONS.md: one entry per material choice (date, decision, reason, who, link). Sessions decide within canon, the pillars and his rulings, record it and carry on; he overturns what he disagrees with.
- NOW.md (at most 200 words): his goal, the builder's list one line an item, a line of state, the handovers. TOWN.md and CLOTHES.md at most 300 each; this file 1,000. tools/doc-caps.py fails the build over a cap.
- FOR-JAFAR.md: each session's summary by 07:00, under 200 words, the day's page first, what failed named, ending in something to act on. Above them the builder's overview (by 07:30 and on change): the retention's line, the current and next item, the AI tester's nightly paragraph, Needs you (at most five, linked, recommended, gone once answered), Road to worth playing; every number from the real path or marked not.
- Read every page's stored answers before any summary or overview.
- FINDINGS.md: open faults only, at most twenty. No notes-only commits except the day's summary, whose commit runs the backup.
- Audits in production/audits/; each finding ends as a ruling, a rule or a list item. The feature checklist (production/archive/) is a reference, not a gate.

## How the work is done

- The NOW.md list in order, one item at a time, each finished with its evidence; then the next, without asking; no stop hook of our own. After each proof-view item, one picture into the overview, no decision. An item much bigger than it looked: tell him.
- Research first (production/research/ first): the professional method end to end, dated, before any symptom; before trusting memory on tools, versions, APIs or licences, or calling anything impossible; on failure, question the method. A helper gets the problem, not your theory: thirty minutes, saved by topic, one summary line. An unreached source is never evidence; what the cloud cannot reach is researched from this PC.
- Two tries, then research; one more failure, set aside and named in the summary. A set-aside the game needs goes into Needs you at once as blocked, with research in another direction.
- Done means in the packaged release build, walked by the AI tester. A big item is "ready for review" until his independent review passes it.
- Nothing is multiplied before one complete sample is approved by him in the assembled game.
- The gate: your check against real references (photographs, the approved face, the casting sheet, the accent by ear; the accent checker only screens); a fresh reviewer against the same, visuals against the Hook sheet and KCD2 frames, clothes against their floor; no visible fault or placeholder, and a visible change since he last looked. Narrow points only: the best goes up with the notes. A rough proof is a finding, not a page item.
- His page: people, whole street frames, backstory, endings, violence and menace, canon, money, licences, scope (small assets pass the gate alone); one a day, one phone screen, at most three one-line decisions with recommendations, his pick stored; pictures full size (RULINGS.md); shortfalls first; yes only for 2026-grade work (clothes: their floor); nothing his rulings settle.
- Approvals live beside what they approve and lapse when their basis changes (tools/approvals.py).
- Simulation work: CoreTests, Soak, SaveChaos, PerceptionGolden, StrangerTest and a regression test before committing; the port matches the C# goldens; a fresh subagent tries to break it; golden rows come from the design.
- Subagents for bounded tasks and the independent check, never as director; of two fine ways, the cheaper.

## Builds, git and disk

- Iterate locally; fetch and rebase, then push to main only accepted work, knowing what it sets off (the Core tests, the Unreal build); never on a failing check; fix a red run first. Two Unreal builds never overlap. Commits say plainly what changed and why.
- Git holds text and small files only; tools/git-size-guard.py runs on every commit (shared pre-commit hook); never --no-verify.
- Write only into the folders production/retention.json names (scratch in F:\LedgerTools\tmp\<session>\<job>, renders in F:\LedgerTools\renders\<job>, models in F:\LedgerTools\hf); lasting inputs in named F:\LedgerTools folders; nothing large on C:; a hold there for what must outlive its limit.
- Before any build, render or large job: `python tools/retention.py space --job "what" --drives CF`. A full disk: stop and wait.
- Delete only what the retention limits cover; anything else needs his yes on a page; nothing of his is ever touched.
