# LEDGER

How the production session on Jafar's PC works.

## Project facts (every session and prompt)

Third-person, never first-person. PC only, Windows. Britain, 1990 (canon's window 1988 to 1992). No alcohol or gambling, shown or spoken of; tobacco allowed; no children anywhere; the rest is canon.md's content rule.

## Read first

At the start: RULINGS.md, the handover, NOW.md, the week's order, his page's open items, the advisor channel (RULINGS 4 Nov); the rest when an item needs it, canon.md (outranks everything) included. The licence allowlist (ledger-v2/research/license-allowlist.md) is law. DECISIONS.md, RECIPE.md: append, never read whole.

## One session, a weekly budget

- One production session, on main and wip. Town work (simulation, claim check, casting, story) and clothing work (Blender, in F:\LedgerTools) are bounded tasks handed out with versioned inputs and acceptance cases, checked on return, never unattended lanes; TOWN.md and CLOTHES.md hold their briefs.
- Each week: 70% production, 10% independent review, 20% kept for him; he reads the meter and stops the session when it is spent. Each task's time is recorded (tools/timelog.py), helpers' time against their item.
- His orders come on Mondays, small (about 1,200 words, each item costed, the total within the week). Between them nothing new unless something is broken: anything else that comes up, from him, the advisor or me, goes on the order's waiting list for the next order, never into the running week (RULINGS 1 Nov, the week's rules).

## Talking to Jafar

- Not a programmer: plain words, short; no paths, hashes, flags or tool output unless asked.
- Updates in the chat, copied to the page's reports: plain, at most ten lines, no files, no promised times; never idle while the goal runs.
- Ask him only for money, his sign-in or hands, licences outside the list, canon, story or scope, and whole-frame or whole-person looks at their gate; decide the rest (RULINGS 30 Oct). One multiple-choice question, recommendation marked; carry on meanwhile.
- Anything needed from him: its own message, sent before any report, starting "NEEDS YOU:" with exactly what to do and every link, nothing else (RULINGS 1 Nov). Reports carry no asks; results reach his page as they land.
- Wrong: one sentence; move on.

## Records

- RULINGS.md: his ruling replaces its line the same day; if code must change a ruling, ask him first.
- DECISIONS.md: one entry per material choice (date, decision, reason, link); decide within canon and his rulings, record, carry on.
- NOW.md: the current phase's items from PLAN.md, one line each naming its file, a line of state, open handovers. tools/doc-caps.py sets and fails the word caps (this file 1,000).
- FOR-JAFAR.md: the day's summary by 07:00, under 200 words, what failed named, ending in something to act on. Above it the overview (by 07:30 and on change; Mondays opening with the week's visible change, before and after): retention's line, current and next item, the tester's paragraph, Mondays risks in five lines, Needs you (at most five, recommended, gone once answered), Road to worth playing; every number real or marked not.
- Morning pictures: by 07:30 daily, the same three views (hook camera by day, reverse view, street at night) as previews, in the overview beside yesterday's and the Hook sheet; no decision.
- FINDINGS.md: open faults only, at most twenty. No notes-only commits except the day's summary, whose commit runs the backup.
- Audits in production/audits/; each finding ends as a ruling, a rule or a list item.
- RECIPE.md (repository root) is a notebook, not a project: no lesson we learn is lost, so that one day the process can make a whole AAA game. Every unit that finishes or is set aside adds a few lines to it in the same commit: what was made; the method in setting-free words; the tools; the target and the check; the cost in hours; what failed and why; the evidence file. Anything specific to 1990 or Meridian stays in data, never in the method. No separate recipe work, no recipe tests.

## One home per fact; reuse first

- Each kind of fact has one home (CATALOGUE.md's homes table); all else derives from it and is checked against it.
- Reuse first starts at home: before making anything new, search the garment list, CATALOGUE.md, the game, canon, the research library and every branch; then Epic's MetaHuman clothing; then outside. Anything fetched is looked at before it is used; else say in DECISIONS.md why it is replaced.
- Anything touching taste or identity (a map, a face, a voice, the look) reaches him on one page before merging.
- Each rule gets a check failing the build where possible: a branch over a week old neither merged nor archived; a derived thing disagreeing with its home; new art or research without a catalogue line.

## How the work is done

- The NOW.md list in order, one item at a time, each finished with its evidence, then the next unasked. A fresh reviewer checks each phase's exit. An item much bigger than it looked: tell him.
- A sample that cannot pass within its capped budget: report the failed capability plainly; never disguise it as another plan.
- Research first (production/research/): the professional method end to end, dated, before any symptom, before trusting memory or calling anything impossible; on failure, question the method. An unreached source is never evidence.
- Research method, for every session. Research starts from a written list of questions. Primary sources are read in full, never from search snippets; every number or claim carries its link and the date it was read. Measure rather than trust where possible (photographs, data, code run on it). Anything not confirmed is marked unverified, and what could not be reached is listed. Independent parts run as parallel helpers. Anything that becomes a target, a design or a decision gets one fresh reviewer who checks it against its sources. The deep-research skill may be used for broad first scans of what exists; these rules still apply to its results. (Jafar, 13 October.)
- Reference first (his rule, 28 October): before any new item, look up how Mafia or Kingdom Come II does it (the studies, then their files on demand) and copy its method, taking its numbers only after checking they fit our kind of game; trial and error only where none exists, the item's plan saying "none found". tools/order_ledger.py fails the push when a new item names neither.
- Game extracts: capped in size, written only above the drive's floor, deleted once their numbers are recorded; Mafia's missing numbers fetched only when an item needs one.
- Two tries means two, then research; a third try needs his yes first, asked once with its reason; without it the fault is set aside and named in the summary.
- Every piece changed in a day is walked by the AI tester in that night's packaged build; a piece passes only there, offline checks are screens; a big item is "ready for review" until he passes it. Nothing is multiplied before he approves one complete sample in the assembled game.
- The gate: your check against references (photographs, approved face, casting sheet, accent by ear), then fresh reviewers sized to the piece (RULINGS 3 Nov), the last good picture beside: what changed; is it a fault? Then the Hook sheet, KCD2 frames, clothes' floor; a visible change since he looked. New faults block; known shortfalls are listed, failing nothing alone; narrow, known points pass.
- His page, "LEDGER: Needs you" (one permanent link, RULINGS 2 Nov; no daily pages): only what is open (people, street frames, story, menace, canon, money, licences, scope, taste, identity), each item its one line, links, recommendation and time added, gone once answered or done; one phone screen, at most three one-line decisions with recommendations, picks stored; pictures full size; shortfalls first; yes only for 2026-grade work; nothing his rulings settle.
- Approvals live beside what they approve and lapse with their basis (tools/approvals.py).
- Simulation: CoreTests, Soak, SaveChaos, PerceptionGolden, StrangerTest and a regression test before committing; the port matches the C# goldens.
- Subagents for bounded tasks and independent checks, never as director; of two fine ways, the cheaper. Helpers never send clicks or keys; computer use as RULINGS 29 and 30 Oct.
- API calls only within his plan's monthly credit: the day's ceiling is the credit left divided by the days left in its month; no bought credits, no automatic reload; each day's spend logged; the key never printed, copied or committed (RULINGS 1 Nov).

## Builds, git and disk

- Unfinished work goes to branch wip daily and after each finished piece, with previews; main gets only what passed review (fetch and rebase first), never on a failing check. Two Unreal builds never overlap. Commits say what changed and why.
- Git holds text, small files and previews (JPEG, ~1600 px, under 500 KB) in production/previews/; guards check every commit and push; never --no-verify.
- Unreal editor tools (Epic's MCP and its Claude Code plugin): commit before every editor session; save before and after any bulk change; never run with permissions bypassed while the plugin is loaded; wait for compiles to finish; read every tool's result and treat anything but an explicit success as a stop; no edits while Play-in-Editor runs.
- Write only where production/retention.json names; lasting inputs in F:\LedgerTools; nothing large on C:. Before any build or render: `python tools/retention.py space --job "what" --drives CF`; a full disk: stop and wait.
- Delete only what retention limits cover, or what Claude made itself and nothing uses (RULINGS.md, 29 October; each recorded in one line); else his yes on a page; nothing of his is touched.
