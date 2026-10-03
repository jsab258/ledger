# LEDGER

Three sessions on Jafar's PC build a game. This file is how they work; what is decided is in RULINGS.md.

## Project facts: every session and every prompt gets these right

Third-person, never first-person. PC only, Windows. Britain, 1990 (canon's window is 1988 to 1992). No alcohol or gambling, shown or spoken of; tobacco allowed; no children anywhere; the rest is canon.md's content rule.

## Read at the start of work

canon.md (outranks everything), RULINGS.md, NOW.md, your own status file, ROADMAP.md. The licence allowlist (ledger-v2/research/license-allowlist.md) is law. DECISIONS.md is the history: append to it; do not read it to start work.

## Three sessions, one repository

- Builder, on main (C:\Users\Jafar\ledger-local): the Unreal project, art, faces, voices, the graphics card.
- Town, on the branch town (C:\Users\Jafar\ledger-town): the simulation, the check on invented facts, casting sheets, the story; never Unreal, art, voices or the graphics card.
- Clothing (C:\Users\Jafar\ledger-clothes): Blender only, on the bodies in F:\LedgerTools\bodies; garments to F:\LedgerTools\garments.
- Handovers are single lines in NOW.md, each naming the exact asset version it fits (MH_LenaS4, not "Sheila"); the receiver checks it is current.
- Fetch and rebase before every push; push to main.

## Talking to Jafar

- Not a programmer: plain words, short; no paths, hashes, flags or tool output unless asked.
- Finished work in three lines: what changed; the picture; what next.
- Ask only about canon, scope or money: one multiple-choice question, recommendation marked; carry on meanwhile.
- Got something wrong: one sentence, then move on.

## Records

- RULINGS.md (at most 2,500 words): his ruling replaces its line the same day, and is appended to DECISIONS.md (date, decision, reason, who, link). The same day it becomes a list item with its specifics. If code must change a ruling, ask him first.
- NOW.md (at most 200 words): the goal (his /goal), the builder's list one line an item, one line of state, the handovers. TOWN.md and CLOTHES.md at most 300 each; this file at most 1,000. tools/doc-caps.py fails the build over a cap.
- FOR-JAFAR.md: each session's summary by 07:00, under 200 words (the day's page first; what changed; evidence; what failed; the retention's line; one line per research; something to act on). Above them the builder's overview, by 07:30 and on change: the current item and the next; Needs you (at most five, each with its page and recommendation, gone once answered); Road to worth playing; numbers only from the real path, or saying not.
- Read every page's stored answers before any summary or overview.
- FINDINGS.md: open faults only, at most twenty.
- No notes-only commits except the day's summary, whose commit runs the backup (post-commit hook).
- Audits in production/audits/; each finding ends as a ruling, a rule or a list item. The feature checklist (production/archive/) is a reference at each milestone, not a gate.

## How the work is done

- The NOW.md list in order, one item at a time, each finished with its evidence. After each proof-view item, one picture into the overview, no decision asked. An item much bigger than it looked: tell him.
- Research first:
  - check production/research/;
  - before new kinds of work, the professional method end to end with dated sources, before any symptom; on failure, question the method first;
  - by a separate helper given the problem, about thirty minutes, saved by topic, one summary line;
  - an unreached source is never evidence;
  - money, licences, canon or scope go to him.
- Two tries, then research; one more failure, set aside and named in the summary. A set-aside the game needs goes into Needs you at once as blocked, with research in another direction.
- Done means in the build and walked by the AI tester on the packaged release build. A big item waits for his independent review: "ready for review" until it passes.
- Nothing is multiplied before one complete sample is approved by him in the assembled game.
- The gate:
  1. your own check against production/reference/ and dated photographs (voices by ear; the accent checker only screens);
  2. a fresh reviewer against the Hook sheet and the KCD2 frames;
  3. no visible fault, placeholder or hole, and a visible change since he last looked.

  On narrow points only, the best goes up with the notes.
- His page:
  - only people, whole street frames, story and dialogue, canon, money, licences and scope; small assets pass the gate alone;
  - one a day, one phone screen, at most three one-line decisions with recommendations;
  - pictures full size (tools/page_pictures.py);
  - shortfalls first; yes only for 2026-grade work;
  - nothing his rulings settle.
- Approvals live beside what they approve and lapse when their basis changes (tools/approvals.py).
- Simulation work: CoreTests, Soak, SaveChaos, PerceptionGolden, StrangerTest and a regression test before the commit; the port matches the C# golden table; a fresh subagent tries to break it; golden rows come from the design, never the code.
- No API calls in development: model work runs through Claude Code on his subscription; LEDGER's key only as RULINGS.md says.
- Subagents for bounded tasks and the independent check, never as director; of two fine ways, the cheaper.

## Builds, git and disk

- Iterate locally; two Unreal builds never overlap; commits say plainly what changed and why.
- Before every push, know what it sets off; never push on a failing check.
- Git holds text and small files only; tools/git-size-guard.py runs on every commit through the shared pre-commit hook; never --no-verify.
- Write only into known folders: scratch in F:\LedgerTools\tmp\<session>\<job>, renders in F:\LedgerTools\renders\<job>, builds in ue-probe\Packaged; a hold in production/retention.json for what must outlive its limit.
- Before any build, render or large job: `python tools/retention.py space --job "what" --drives CF`. A full disk: stop and wait.
- Delete only what the retention limits cover; anything else needs his yes on a page; nothing of his is ever touched.
