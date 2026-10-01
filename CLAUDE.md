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

- NOW.md, no history: the GOAL line (what runs, until when), the builder's list in order as Jafar wrote it (- [ ] open, - [x] done), a line of state, and a Handovers heading where the town session leaves single lines for the builder. SHORT (Jafar, 30 September, after the audit found NOW and TOWN at about 20,000 words): current state and the list; a handover leaves when it is done; history is in git.
- EVERY HANDOVER NAMES THE EXACT VERSION of the asset it fits (Jafar, 30 September: Sheila's spectacles were fitted to a head that had been replaced): the take or file it was made against (MH_LenaS4, not "Sheila"), and the receiver checks it is still current before fitting.
- EVERY NUMBER IN THE OVERVIEW COMES FROM THE REAL PATH, or says plainly that it does not (Jafar, 30 September: the three-second speaking delay was measured with stand-in text).
- FOR-JAFAR.md: one dated summary a day, written by 07:00 each morning and covering everything since the last, under 200 words, that day's approval page linked first; anything that needs him urgently before then goes in the overview at once: what changed, evidence, what failed or is unproven, free space on C: before and after, one line per piece of research done, and anything that needs him. Unresolved decisions carry forward; git keeps earlier summaries (Jafar, 28 September). An item he has answered comes off the overview's "Needs you" in the same commit that acts on his answer, so the file never asks him something already settled (Jafar, 28 September: the cleanup note stayed up hours after it was done).
- THE OVERVIEW (Jafar, 29 September, to keep his view across three sessions): the first section of FOR-JAFAR.md, above every session's summary, and edited by the builder alone, so the sessions never edit the same lines. Updated by 07:30 each morning, after the town and clothing sessions have written their own summaries by 07:00, and again whenever something in it changes. Two parts and nothing else. (1) Needs you: everything waiting on him from all three sessions, one list, at most five items, each with its page link and the recommendation; an item leaves the moment he has answered it. (2) Road to worth playing: one line each for what stands between today and a game he would want to play, at least faces approved, people dressed, the delay before a character speaks, the replies that time out, the first week wired into the game, and the AI tester walking it; each line gives who owns it, where it stands in one phrase, and what changed since yesterday. Each session's own summary stays below it.
- READ HIS PAGES' PICKS before every summary and every overview update (the page's store, verdicts/<key>): on 29 September his picks on Wednesday's page lay unread for seven hours. NOTHING GOES INTO NEEDS YOU UNTIL ITS PAGE'S STORED ANSWERS ARE CHECKED, the town's and clothing's pages too (Jafar, 30 September: two taps he had answered at 16:24 were listed as waiting at 18:00, copied from a summary's text); if he has answered, it is not waiting on him.
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
- RESEARCH THE METHOD BEFORE THE SYMPTOM (Jafar, 30 September; the clothing session researched sleeves dragging instead of how game studios make clothing, and it cost us the clothes): before a new kind of work, first research how professionals do it from start to finish, the whole pipeline, with dated sources; only then research specific problems. When something fails, ask first whether the method is wrong, before fixing the symptom. Researching a symptom is not researching the method.
- THE TWO-TRIES RULE HAS TEETH (Jafar, 29 September): after two failed attempts at the same thing, research it; after one more failure, set it aside and move to the next item on the list. Every daily summary names anything that went past that. The jacket's fourteen overnight rounds must not happen again.
- A SET-ASIDE NEVER SIMPLY STOPS (Jafar, 1 October, after clothing stopped silently that day), on every session: when the two-tries rule sets aside something the game cannot do without (clothes, faces, voices, the talk), it goes into the overview's Needs you at once as a blocked capability, with what was tried and why it failed, and the session proposes research in a different direction.
- The research goes to a separate helper given the problem, not your theory about it, capped at about thirty minutes, with dated sources. Its note is saved in production/research/ under a topic folder, and the day's summary gives it one line.
- Anything the research suggests that touches money, licences, canon or scope goes to Jafar as a decision.

## Three sessions, one repository (Jafar, 28 and 29 September)

- The builder works in C:\Users\Jafar\ledger-local on main: the Unreal project, art, faces, voices and anything that uses the graphics card. The graphics card is the builder's first.
- The town session works in the git worktree C:\Users\Jafar\ledger-town on the branch town: the town's simulation, the check on invented facts, casting sheets and the story. It never touches the Unreal project, art, voices or anything that uses the graphics card. It leaves work for the builder as single lines under the Handovers heading in NOW.md; the builder wires them into the game.
- The clothing session (Jafar, 29 September) works only in Blender, in C:\Users\Jafar\ledger-clothes: the jacket and all clothing, sewn and draped on the MetaHuman bodies the builder exports into F:\LedgerTools\bodies (Ron, Darren and Sheila, and a slim, an average and a heavy male build), handed back into F:\LedgerTools\garments. The builder leaves it single lines under the "Handovers to clothing" heading in NOW.md; it leaves the builder single lines under Handovers. The builder fits each garment in Unreal by script (MetaHuman's resizing graph with Strip Sim Mesh false, and Chaos cloth) and puts the dressed characters on Jafar's page: clothes on people are his to approve. It keeps its use of the graphics card light.
- Each session fetches and rebases before every push, and pushes its work to main.

## How to work

- THE PLAYABLE ROUTE COMES FIRST (Jafar, 30 September, after the outside audit, production/audits/2026-09-30-adversarial-audit.md; the reasoning is his): for the next days, one continuous route through ordinary play before visual work. STOP ALL OTHER VISUAL ITERATION while that route (the list's first item) is broken.
- FACES ARE FROZEN (Jafar, 30 September): Ron's and Sheila's approved heads are final, and Darren's once he approves him. No more portrait adjustments.
- LIGHTING IS JUDGED THROUGH THE GAME'S OWN CAMERA AND EXPOSURE, never portrait frames alone (Jafar, 30 September).
- Nothing is multiplied until one complete sample has been approved by Jafar in the assembled game.
- An approval lives beside what it approves and names what it was approved against; when that changes (a canon rule, a spec, a voice), it lapses by itself, and the build flags anything in the game without a current one (tools/approvals.py).
- Approvals reach him as one page a day, pictures and sound, judged in minutes, linked first in the day's summary. The page keeps the 25 September casting page's format: each item's pictures and sound, one pick and a note, stored on the page (tools/candidate_page.py).
- PICTURES JUDGED ON THE PAGE ITSELF (Jafar, 30 September and 1 October; Wednesday's were too small to judge), on every session's pages: tap a picture and it opens full-screen at its full resolution, pinch to zoom, swipe to the next, close to return; films play there with their sound; no separate links (tools/page_pictures.py, applied by every page tool). A picture shown for judging is never smaller than the page is wide, and is taken at full size in the first place (the game's frames at 2560 by 1440), never enlarged.
- EVERY PAGE FITS ONE PHONE SCREEN (Jafar, 30 September; the town's page was a wall of text), on every session's pages: at most three decisions, each one line with its options and the recommendation, answered with a tap; any detail sits folded underneath, closed unless he opens it. Whatever can be decided without him under his rulings never goes on a page: decide it and write it in DECISIONS.md.
- WHAT REACHES HIS PAGE (Jafar, 29 September): only what is expensive to get wrong or is his taste or ruling: people (faces, voices, clothes); the overall look of the street and its light, as whole frames; the story, dialogue and anything touching canon; anything involving money, licences or scope. Props, street clutter, materials, sounds and other small assets are approved by the gate alone (your check against real reference photographs, then a reviewer who has not seen the work): if they pass, they go into the game, and he sees them in context in the street frames on his page and says if something jars.
- THE GATE JUDGES AGAINST THE BAR (Jafar, 1 October, after a no to all four of Wednesday's looks, which the page had recommended): every visual is compared with the approved Hook sheet (production/reference/hook-sheet.png) and the KCD2 frames (production/reference/kcd2-town-arcades.jpg, kcd2-town-fountain.jpg), never with "looks like a street", by me and by the reviewer, and the page says plainly where it falls short of them. Recommending yes is only for what would pass in a 2026 game; anything short of that goes on the page with its shortfalls named first and no recommendation of yes.
- THE GATE (Jafar, 25 September; a lumpy cap and American-accented voices reached him). Nothing goes on his page until it passes two checks. First, yours: compared against real references (photographs of the actual thing, the approved face, the casting sheet; for a voice, the accent the sheet names); if it fails, fix it or leave it off. VOICES ARE JUDGED BY EAR (Jafar, 30 September: the accent checker rejects half of genuine Scottish clips): the checker is a screen only, never a gate; what it flags is said beside the take, and his ear decides. Second, a reviewer that has not seen it being made compares it against the same references and tries to find what is wrong. Only what passes both reaches him. A rough proof that a method works is a finding in the summary, never an item on his page. The gate stops obvious failures, not imperfection: once the obvious faults are fixed and a fresh reviewer fails a candidate only on narrow points, stop refining and put the best one on his page with the reviewer's remaining notes beside it; his eye decides the rest (Jafar, 28 September).
- The AI tester walks the packaged release build, with the real cast, dialogue, light and sound.
- Every audit is saved in production/audits/, and each finding ends as a ruling in DECISIONS.md, one of these rules, or an item on the list, never only a prompt; the next audit checks the last one's stuck.
- Iterate locally: build and render in Unreal on this PC, look, fix, repeat; push only accepted work. Two Unreal builds must not overlap.
- Commits say in plain words what changed and why. Pushes run the Core tests and the Unreal build; a red run is fixed first.
- BEFORE EVERY PUSH, KNOW WHAT IT SETS OFF (which workflows, and whether any costs money or holds the build machine), and never push on a failing check (Jafar, 29 September).
- NOTHING COUNTS AS DONE ON PAPER (Jafar, 29 September): done means in the build and walked by the AI tester. A BIG ITEM IS MARKED DONE ONLY AFTER AN INDEPENDENT REVIEW HAS CHECKED IT (Jafar, 30 September, after the route marked done had eight High faults): when an item is ready, tell Jafar, and he runs that review in the cloud; until it passes, the overview says "ready for review", never "done".
- A GOLDEN ROW IS WRITTEN FROM WHAT THE GAME SHOULD DO, not copied from what the code does (Jafar, 30 September: an independent review found four faults written into the golden tables, so the tests passed because of them). Where a golden row encodes a fault, first write a test from the design that fails, then fix the code and the row together.
- Simulation work (perception, memory, gossip, and their port) keeps its tests: CoreTests, Soak, SaveChaos, PerceptionGolden and StrangerTest before the commit, plus a regression test. The C++ port must match the C# golden table, regenerated from the C# Core for the comparison. It also gets one independent check: a subagent that has not seen your reasoning gets the change, its test, canon and the intended behaviour in plain words, and is told to break it.
- Visual work: references live in production/reference/ only. The concept sheet governs mood, palette and composition; the photographs (links only) govern what things looked like and win where they disagree. An asset gets two attempts against its reference, then is finished from dimensions or set aside.
- NO API CALLS IN DEVELOPMENT (Jafar, 29 September: he pays for Max, not for API calls on top). Model work (playing the game as the AI tester, judging, the few talk checks that need a real reply) runs through Claude Code on his subscription: ourselves, our helpers, or its non-interactive mode called from a script; talk tests run against the stand-in. The one exception is the characters talking live while he plays, on LEDGER's own key with a hard monthly cap, which no automated tool or workflow may ever use.
- Subagents for bounded, mechanical tasks and the independent check; never as a director.
- Of two fine ways, take the cheaper.
