# LEDGER

Two sessions on Jafar's PC, building a game (see "Two sessions, one repository"). The old studio is archived under legacy/studio-v2/.

## Project facts: every session and every prompt gets these right

- Third-person, never first-person. (An audit prompt on 24 September called it first-person; that was wrong and must never recur.)
- PC only, Windows.
- Britain, 1990 (canon's window is 1988 to 1992).
- Content: no alcohol and no gambling, shown or spoken of; tobacco allowed; no children anywhere. The rest is canon.md's content rule.

## What governs

canon.md (the world and content rules; it outranks everything), ROADMAP.md (milestones), DECISIONS.md (what is decided; its archive still binds), production/research/README.md (what governs each thing's look). The licence allowlist is law.

## Talking to Jafar

- He is not a programmer: plain words, short; no paths, hashes, flags or tool output unless asked.
- Finished work: three lines: what changed; the picture; what next.
- Ask him only about canon, scope or money: one multiple-choice question, your recommendation marked, and carry on with it meanwhile. The rest is yours.
- No voice is cast without his yes.
- Free content for Unreal (Fab, Epic or elsewhere) whose licence is on the allowlist: download it, note it in the summary, never ask (Jafar, 24 September).
- If you got something wrong, one sentence, then move on.

## Records, and nothing more

- NOW.md, no history: the GOAL line (what runs, until when), the builder's list in order as Jafar wrote it (- [ ] open, - [x] done), a line of state, and a Handovers heading where the town session leaves single lines for the builder.
- FOR-JAFAR.md: one dated summary a day, written by 07:00 each morning and covering everything since the last, under 200 words, that day's approval page linked first; anything that needs him urgently before then goes at the top of the file at once: what changed, evidence, what failed or is unproven, free space on C: before and after, one line per piece of research done, and anything that needs him. Unresolved decisions carry forward; git keeps earlier summaries (Jafar, 28 September). An item he has answered comes off "Needs you now" in the same commit that acts on his answer, so the file never asks him something already settled (Jafar, 28 September: the cleanup note stayed up hours after it was done).
- DECISIONS.md: one entry per material choice: date, decision, reason, who decided, link. Routine implementation choices go in commit messages.
- FINDINGS.md: unresolved faults only, at most twenty.
- Records go in with the work they describe or in the day's summary. No commit that only updates notes, except the day's summary.
- The old records and the 979-item feature checklist are in production/archive/. The checklist is a reference, not a gate: check it for missing basics at each milestone; nothing waits on it.
- Why: the two audits in production/audits/.

## Disk: what may ever be deleted (Jafar, 25 September)

- Deletion happens only inside this fixed list, and only after he approves a cleanup page that names each folder, its size and why: the two old copies, C:\Users\Jafar\wc26-picks and C:\Users\Jafar\ledger-migrate; the project's own build, render and scratch folders (its gitignored build output, such as ue-probe\Intermediate, Saved, Packaged and DerivedDataCache and the .NET bin and obj folders, and its gitignored render and scratch output); C:\LedgerTools; the build machine's working copy, C:\actions-runner-ledger\_work; Unreal's cache, %LOCALAPPDATA%\UnrealEngine\Common; and, in F:\LedgerTools, only the files and folders production/large-files.json names as my own rejected or superseded ones, never the folder itself (the voice libraries and his played game live there; Jafar, 26 September). Nothing outside it is ever deleted, moved or changed, least of all his Documents, Desktop, Downloads, Dropbox or anything else of his.
- Never deleted, even inside the list: what he has approved, anything the game or a build uses, anything the backup covers (tools/backup-to-dropbox.py's list). The old copies go only once everything in them is shown to be on GitHub or moved out (the voice tools and the played copy of the game, as agreed on 24 September).
- tools/cleanup.py refuses any path outside the list, and any protected one.
- THE LARGE-FILE RECORD, so it cannot creep back: every file or folder of 100 MB or more that I create goes into production/large-files.json (tools/large_files.py) with what made it and why. At the end of every day I delete only my own entries from that record that are rejected or superseded, only inside the list above; never anything I did not create, and never by guessing that something is unused. New scratch and caches go to drive F, not C.
- Every day's summary gives free space on C: before and after. Below 60 GB, the cleanup page comes before anything else next.

## How the week runs (Jafar, 28 September)

- One goal runs until Sunday evening, set by Jafar with /goal; there are no sittings and no stop hook of our own. The builder's list in NOW.md is worked in order; when an item is done, take the next without asking. Nothing waits on his hands: he writes from his phone.
- Each day's summary (by 07:00) ends with something he can act on (how to play what exists, a recommended decision, or both); then the backup runs (tools/backup-to-dropbox.py; the summary's commit sets it off through tools/hooks/post-commit) and the summary gives its line, and the large-file record is swept.
- If an item turns out much bigger than it looked, tell him rather than push on.

## Research first (Jafar, 28 September)

- Before solving something from memory, check production/research/, which already holds nearly fifty topics.
- Research when: before a kind of work not yet done in this project; after two failed attempts at the same thing; before relying on memory about a tool, version, API or licence that could have changed; and always before declaring anything impossible, blocked or possible only by hand.
- The research goes to a separate helper given the problem, not your theory about it, capped at about thirty minutes, with dated sources. Its note is saved in production/research/ under a topic folder, and the day's summary gives it one line.
- Anything the research suggests that touches money, licences, canon or scope goes to Jafar as a decision.

## Two sessions, one repository (Jafar, 28 September)

- The builder works in C:\Users\Jafar\ledger-local on main: the Unreal project, art, faces, clothes, voices and anything that uses the graphics card.
- The town session works in the git worktree C:\Users\Jafar\ledger-town on the branch town: the town's simulation, the check on invented facts, casting sheets and the story. It never touches the Unreal project, art, voices or anything that uses the graphics card. It leaves work for the builder as single lines under the Handovers heading in NOW.md; the builder wires them into the game.
- Each session fetches and rebases before every push, and pushes its work to main.

## How to work

- Nothing is multiplied until one complete sample has been approved by Jafar in the assembled game.
- An approval lives beside what it approves and names what it was approved against; when that changes (a canon rule, a spec, a voice), it lapses by itself, and the build flags anything in the game without a current one (tools/approvals.py).
- Approvals reach him as one page a day, pictures and sound, judged in minutes, linked first in the day's summary. The page keeps the 25 September casting page's format: each item's pictures and sound, one pick and a note, stored on the page (tools/candidate_page.py).
- THE GATE (Jafar, 25 September; a lumpy cap and American-accented voices reached him). Nothing goes on his page until it passes two checks. First, yours: compared against real references (photographs of the actual thing, the approved face, the casting sheet; for a voice, the accent the sheet names); if it fails, fix it or leave it off. A voice drifting American or away from the named accent is rejected before he hears it. Second, a reviewer that has not seen it being made compares it against the same references and tries to find what is wrong. Only what passes both reaches him. A rough proof that a method works is a finding in the summary, never an item on his page.
- The AI tester walks the packaged release build, with the real cast, dialogue, light and sound.
- Every audit is saved in production/audits/, and each finding ends as a ruling in DECISIONS.md, one of these rules, or an item on the list, never only a prompt; the next audit checks the last one's stuck.
- Iterate locally: build and render in Unreal on this PC, look, fix, repeat; push only accepted work. Two Unreal builds must not overlap.
- Commits say in plain words what changed and why. Pushes run the Core tests and the Unreal build; a red run is fixed first.
- Simulation work (perception, memory, gossip, and their port) keeps its tests: CoreTests, Soak, SaveChaos, PerceptionGolden and StrangerTest before the commit, plus a regression test. The C++ port must match the C# golden table, regenerated from the C# Core for the comparison. It also gets one independent check: a subagent that has not seen your reasoning gets the change, its test, canon and the intended behaviour in plain words, and is told to break it.
- Visual work: references live in production/reference/ only. The concept sheet governs mood, palette and composition; the photographs (links only) govern what things looked like and win where they disagree. An asset gets two attempts against its reference, then is finished from dimensions or set aside.
- Subagents for bounded, mechanical tasks and the independent check; never as a director.
- Of two fine ways, take the cheaper.
