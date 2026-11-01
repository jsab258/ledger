---
name: gate
description: The one way LEDGER judges a visual piece before it counts as done (a shop front, a wall, the wet ground, a lamp, a room, a garment, a person, a whole street frame). Pictures of each view it changes, automatic checks first, one fresh reviewer per view beside that view's last good picture, then the bar (the Hook sheet, the Kingdom Come II frames, the clothing floor), then the AI tester's walk in that night's packaged build, then his page when a whole frame or a whole person is at stake. Use it whenever a visual change is ready to be judged, a fix needs re-checking, a reviewer brief is to be written, someone asks "did it pass", or a page for Jafar would show pictures, even if nobody says "gate".
---

# The gate

How a visual piece passes in LEDGER: CLAUDE.md ("How the work is done", the gate) and RULINGS.md (1, 7 and 25 October; 1 November, the week's rules). Shaped like the garment skill (.claude/skills/game-garment/SKILL.md), which uses this gate at its step 9. The records behind it: production/audits/reviewer-test (7 October: one picture at a time, beside the last good one, finds 20 of 20 planted faults; a bundle let a black block through).

**Always** (his rulings; none of these bends):
- A piece passes only in that night's packaged build, walked by the AI tester; editor pictures and offline checks are screens, necessary and never enough.
- One view per fresh reviewer, never a bundle; each beside its last good picture.
- A new fault blocks; a known shortfall against the bar is listed and fails nothing alone; narrow, known points pass.
- Two tries per fault, then research; a third try needs Jafar's yes first, asked once with its reason.
- Reviewers and helpers never click, never use computer use or UI Automation; they read pictures and files.
- Whole-frame and whole-person looks go to Jafar at their gate; a single piece does not.

**Requests this covers**, for example: "gate the chandler's new wear"; "the wet ground changed, re-check it"; "brief the reviewers for Tom's outfit"; "did Mickey's office pass?"; "put the corner on his page"; "which views does a lamp change touch?".

## 1. The views a change can touch

- List the views this change can alter: the hook camera by day and at night, the reverse view, the shop views (chandler@x, shopnight), the office's three, the dress views for clothes, a close view by numbers (-PageAt). Re-check only those; one full pass of every view at the gate's end (25 October).
- **Check:** each listed view has a last good picture in F:/LedgerTools/gate/last-good/<view>/; one without says so in the record ("no last good: the first").

## 2. Pictures, at the played level

- Editor: UnrealEditor.exe ue-probe/LedgerProbe.uproject -game with the street's switches (-LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle), -PageShots=day|night|dress|shop|shopnight|at, -RenderOffScreen -ResX=2560 -ResY=1440 -LedgerRepo=<checkout>, and -ExecCmds="scalability 2" (the game ships at High). The pictures land in ue-probe/Saved/PageShots; copy them to F:/LedgerTools/gate/new/<piece>/<date>/.
- Packaged: the night build's copy (F:/LedgerTools/played-game), the same views; the morning pictures (tools/morning_pictures.py) are the street's three.
- No local Unreal during the night jobs (01:15 to 04:30), never two Unreal builds at once, and a full disk stops the job (tools/retention.py space first).
- **Check:** each picture is at full size, the view's own camera, nothing debug in frame (no visible stand-in, no gizmo, no placeholder text).

## 3. Automatic checks first

- The asset checks (tools/ue/asset_checks.py) for any new mesh or texture; the canon, content and names gates (tools/canon-gate.py, content-gate.py, names-gate.py) for any words or brands in view; the piece's own measures (tools/surface_values.py, wet_ground_check.py, measure_night_pools.py, pool_clip.py, stain_check.py, chart_read.py, as the piece needs).
- **Check:** every automatic check named in the piece's plan has run, its line read; reviewers judge the look, not what a script can count.

## 4. My own look

- Before any reviewer: compare against the references the piece answers to (dated photographs, the approved face, the casting sheet, the accent by ear) and its last good picture, zoomed where a fault would hide.
- **Check:** anything I see that is wrong is fixed or named before a reviewer is spent on it.

## 5. One fresh reviewer per view

- Brief each one with: the new picture; its last good picture (or the earlier ones); what changed and why; the view's known shortfalls, by name; the references (production/previews/hook-sheet-2026-10-05.jpg, read mirrored where its view is the mirror; F:/LedgerTools/reference-other-games/production/reference/kcd2-town-arcades.jpg and kcd2-town-fountain.jpg; production/art/clothing/RUBRIC.md for clothes); the ban on clicks, computer use and UI Automation; one verdict file (changes, newFaults, knownSeen, verdict PASS or FAIL) beside the pictures.
- Ask first "what changed, and is any change a fault?", then "anything new that is wrong?", and the known shortfalls apart.
- **Check:** one reviewer a view; each verdict file written; a FAIL names each new fault and where it is in the picture.

## 6. The verdict

- A new fault blocks: fix it (two tries), then re-check only that view. Known shortfalls go in the record and on the page, failing nothing alone.
- A view that passes: its picture becomes the view's last good (copy into F:/LedgerTools/gate/last-good/<view>/).
- **Check:** no view passes with an unread verdict; the last good folder holds the passed picture.

## 7. The bar

- Then each passed view against the bar: the Hook sheet and the Kingdom Come II frames for the street and rooms; for clothes, the floor (RUBRIC.md); a Mafia town street only as a public press frame viewed on the web, never stored (other games' screenshots never enter the repository).
- "Yes" on his page only for what would pass in a 2026 game; everything short of that is named first.
- **Check:** the shortfalls against the bar are a list, each one line, in the record.

## 8. The packaged walk

- The piece goes into that night's packaged build (pushed before the build, the game target built locally first for any C++ change); the AI tester walks it (the night walk, or tools/ai-tester/play.py on the packaged copy); its report is read in the morning.
- **Check:** the walk's report names no new fault in the piece; the piece is "done" only now, "ready for review" if it is big and waits for his word.

## 9. His page, for a whole frame or a whole person

- One phone screen, at most three one-line decisions, shortfalls first, pictures full size, each frame checked by a fresh reviewer first, nothing his rulings settle (production/approvals/; tools/day_page.py). His answers are read (ArtifactData) before asking anything about the page.
- Anything asked of him goes in its own message first, starting "NEEDS YOU:" with the page's full link.
- **Check:** the page shows no fault, debug object or placeholder; dated the day made.

## Records, every gate

- DECISIONS.md one entry: the views, the rounds, the verdict, the shortfalls, the evidence folder. A gate record at most about 500 words: a table of views and rounds, then the faults (25 October).
- The measures the order asks for (D13): gate rounds and reviews a piece, against the median 9 and 26 before the automatic checks.
- RECIPE.md gains what the gate taught (setting-free); the time log carries the reviewers' time against the piece.
