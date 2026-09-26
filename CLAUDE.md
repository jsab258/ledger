# LEDGER

One session, on Jafar's PC, building a game. The old studio is archived under legacy/studio-v2/.

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

- NOW.md: under 150 words, no history: the SITTING line (start and limit), the sitting's list in order (- [ ] open, - [x] done), a line of state.
- FOR-JAFAR.md: one dated summary at the end of each sitting, under 200 words: what changed, evidence, what failed or is unproven, what next, decisions he must make. Unresolved decisions carry forward; git keeps earlier summaries.
- DECISIONS.md: one entry per material choice: date, decision, reason, who decided, link. Routine implementation choices go in commit messages.
- FINDINGS.md: unresolved faults only, at most twenty.
- Records go in with the work they describe or in the closing summary. No commit that only updates notes during a sitting.
- The old records and the 979-item feature checklist are in production/archive/. The checklist is a reference, not a gate: check it for missing basics at each milestone; nothing waits on it.
- Why: the two audits in production/audits/.

## Disk: what may ever be deleted (Jafar, 25 September)

- Deletion happens only inside this fixed list, and only after he approves a cleanup page that names each folder, its size and why: the two old copies, C:\Users\Jafar\wc26-picks and C:\Users\Jafar\ledger-migrate; the project's own build, render and scratch folders (its gitignored build output, such as ue-probe\Intermediate, Saved, Packaged and DerivedDataCache and the .NET bin and obj folders, and its gitignored render and scratch output); C:\LedgerTools; the build machine's working copy, C:\actions-runner-ledger\_work; Unreal's cache, %LOCALAPPDATA%\UnrealEngine\Common; and, in F:\LedgerTools, only the files and folders production/large-files.json names as my own rejected or superseded ones, never the folder itself (the voice libraries and his played game live there; Jafar, 26 September). Nothing outside it is ever deleted, moved or changed, least of all his Documents, Desktop, Downloads, Dropbox or anything else of his.
- Never deleted, even inside the list: what he has approved, anything the game or a build uses, anything the backup covers (tools/backup-to-dropbox.py's list). The old copies go only once everything in them is shown to be on GitHub or moved out (the voice tools and the played copy of the game, as agreed on 24 September).
- tools/cleanup.py refuses any path outside the list, and any protected one.
- THE LARGE-FILE RECORD, so it cannot creep back: every file or folder of 100 MB or more that I create goes into production/large-files.json (tools/large_files.py) with what made it and why. At the end of every sitting I delete only my own entries from that record that are rejected or superseded, only inside the list above; never anything I did not create, and never by guessing that something is unused. New scratch and caches go to drive F, not C.
- Every sitting's summary gives free space on C: at the start and at the end. Below 60 GB, the cleanup page comes before anything else in the next sitting.

## How a sitting runs

- Each sitting has a list in order and a time limit (four hours if unnamed). When an item is done, take the next without asking. Stop only when time is up or the list is done, everything committed; the closing summary ends with something he can act on: how to play what exists, a recommended decision, or both. At the end of every sitting the backup runs (tools/backup-to-dropbox.py; the summary's commit sets it off through tools/hooks/post-commit) and the summary gives its line, and the large-file record is swept.
- The stop hook has one job: while time remains and the list has an item left, keep going. It reads NOW.md, for the builder's own session only (its id is in the untracked .claude/builder-checkout).
- If an item turns out much bigger than it looked, tell him rather than push on.

## How to work

- Nothing is multiplied until one complete sample has been approved by Jafar in the assembled game.
- An approval lives beside what it approves and names what it was approved against; when that changes (a canon rule, a spec, a voice), it lapses by itself, and the build flags anything in the game without a current one (tools/approvals.py).
- Approvals reach him as one page per sitting, pictures and sound, judged in minutes, linked first in the closing summary. The page keeps the 25 September casting page's format: each item's pictures and sound, one pick and a note, stored on the page (tools/candidate_page.py).
- THE GATE (Jafar, 25 September; a lumpy cap and American-accented voices reached him). Nothing goes on his page until it passes two checks. First, yours: compared against real references (photographs of the actual thing, the approved face, the casting sheet; for a voice, the accent the sheet names); if it fails, fix it or leave it off. A voice drifting American or away from the named accent is rejected before he hears it. Second, a reviewer that has not seen it being made compares it against the same references and tries to find what is wrong. Only what passes both reaches him. A rough proof that a method works is a finding in the summary, never an item on his page.
- The AI tester walks the packaged release build, with the real cast, dialogue, light and sound.
- Every audit is saved in production/audits/, and each finding ends as a ruling in DECISIONS.md, one of these rules, or an item on the list, never only a prompt; the next audit checks the last one's stuck.
- Iterate locally: build and render in Unreal on this PC, look, fix, repeat; push only accepted work. Two Unreal builds must not overlap.
- Commits say in plain words what changed and why. Pushes run the Core tests and the Unreal build; a red run is fixed first.
- Simulation work (perception, memory, gossip, and their port) keeps its tests: CoreTests, Soak, SaveChaos, PerceptionGolden and StrangerTest before the commit, plus a regression test. The C++ port must match the C# golden table, regenerated from the C# Core for the comparison. It also gets one independent check: a subagent that has not seen your reasoning gets the change, its test, canon and the intended behaviour in plain words, and is told to break it.
- Visual work: references live in production/reference/ only. The concept sheet governs mood, palette and composition; the photographs (links only) govern what things looked like and win where they disagree. An asset gets two attempts against its reference, then is finished from dimensions or set aside.
- Subagents for bounded, mechanical tasks and the independent check; never as a director.
- Of two fine ways, take the cheaper.
