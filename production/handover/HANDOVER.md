# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-13 21:06 (hourly run; the gate said GO: last stopped 20:30, no turn written for 35 minutes)
**Stopped:** 2026-11-13 20:30 (hourly run from 15:36: Drape Studio's final round judged; the false heavy body replaced by Ron's and twin bodies refused (148); Kiln rounds 1 to 3, M2 met; advisors 147 to 154 and the 19:40 efficiency note acknowledged; DAILY-2026-11-13 written; last push ff679fb67; history near its hard stop, so handed over at an item's end with no helper out).
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted 8 Nov 17:17; runs to 13:00 Monday 16 November). **Until Monday 16 Nov 07:00 Kiln has priority over the order's game work, clothing first (advisor 144, his pick 14:36)**; game items run only where Kiln waits (Unreal or the card idle). The weekly line still governs total usage.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). Write it with ArtifactData and see its version. "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing** (this run guessed 14:40 for records written at 14:26 and had to correct them).
- Pace rules: RULINGS 7, 10 Nov and 13 Nov (idle fine while on track; the 16 Nov reset week runs a doubled line from his adoption tap, six helpers, no busywork; rows in that week name any hour with no session, advisor 140/143).
- Never end a turn while work remains (advisors 64, 68); the Stopped line is the last thing written (advisor 104).
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open" (the field is "state", not "status"). Never list collections whole.
- Advisor 113: of two tools, prefer the one driven without clicks. Advisor 117: every garment's work its own time-log window. Advisor 111: check the paid-tools sweep before any second try. Launcher ruling (RULINGS 11 Nov) as written.
- **Kiln (RULINGS 13 Nov 14:19, advisor 142):** serves LEDGER, never itself; every module and fix names the game item it unblocks and hours saved; 15% of a week's usage (suspended until Mon 07:00 by advisor 144); park rule: M3 by about 22 Nov or keep-or-drop. Time log "tool loop: <tool> round n". Caps: clothing about 20 h, hair about 8 h.
- **Weekend pacing (advisor 155, 13 Nov 21:40, to Mon 07:00):** part of the meter is his own project; pace Kiln to the line, not ahead: one fixer round at a time, a fresh reviewer only where a milestone is judged, no extra helpers; while more than 6 points ahead, a hold of at least 30 minutes between rounds even with the priority mark; aim about 90% at Monday 07:00 including his use.
- **He no longer develops any of his tools (advisor 146, 14:45):** the copies under F:/LedgerTools/tool-dev are their only line of development; no more rebasing on his folders.

## Run on 13 Nov, from 15:36 (this session)
- Advisor 147 in RULINGS (Kiln's sequence; cap held at 4,899 by trimming tap times); acks 147 to 151 written.
- Drape Studio's final round judged: DRAPESTUDIO-TEST-2026-11-13-FINAL.md, preview drapestudio-final-2026-11-13. Jumper 125 s (Marvelous 124), jacket 147 s, jeans 173 s; cuffs and waistband fixed; jacket sleeves 5.47x and its gripped cuff crumples (its own check now fails it); layering holds the jumper under by eye but took 6,795 s. Work folder F:/LedgerTools/drapestudio-test-2026-11-13-final (checks/ has the scripts).
- Advisor 148, bodies: the three build bodies are one body (known since 29 Sep, later used as batch targets). Heavy = Ron (RoccoP2), slim = Darren (SamS6), average = Tom. Judge and Kiln refuse twin bodies (tested both ways). Seamshift rerun on Ron: Sheila's cardigan fails its fold check (130 folded edges), sitting 18; judge re-based (baseline from runs/bodies-fix-2026-11-13, bar 18); note in SEAMSHIFT-ROUND1 'The heavy body was not heavy'.
- Advisor 151: ClothCraft briefs saved (kiln/KILN-CLOTHCRAFT-BRIEFS.md and beside the design note). 150: HumanMotionCraft uninstalled; its ideas in LOOP.md. 149: Epic's Panel Cloth and outfit resizing are a baseline in LOOP.md; our 11 Nov note RESIZING-SCRIPT-CALLS found no script-only route: about 4 h on a small C++ helper (clicks not allowed).
- Pushed 7b54bbcae to wip (failed=none). Judge commits 13f217b, 2a7b8e4; Kiln cc12933 plus the briefs.
- Kiln rounds 1 to 3 (KILN-ROUND1-2026-11-13.md, all pushed): round 1 ClothCraft engine met every M2 count but failed by eye (boxy, open seams); round 2 (advisor 153) settling was not the cause, Drape Studio's engine copied into Kiln as a second engine (KILN_ENGINE=drapestudio), both failed by eye, Drape Studio's nearer; round 3 on that engine: **M2 MET** (PASS WITH SHORTFALLS, 143 s, every count at or better than Marvelous, byte-identical repeat). Kiln commits through 015997a. Fixers 2 h 58 min, three reviewers.
- DAILY-2026-11-13.md written late (advisor 19:41) and pushed; acks current to the 19:40 efficiency note.

## In flight
- Nothing running. No helper is out. The Drape Studio test's and the fixers' scratch folders are on F: (runs/fixer-r1..r3 about 120 MB; F: at its floor).
- Advisor 154: Kiln carries on through the night as his priority; only Unreal and processor-heavy drape runs pause 01:15 to 04:30 (job_j3/jacket/jeans judge runs are processor-heavy: hold them in that window); a short night summary in the 07:00 handover.

## Next, in order
1. FIRST: pace; verdicts after 2026-11-13T19:30Z; advisor after the latest ack (current to the 19:40 'eff' note).
2. Kiln round 4 = M3 (LOOP.md 'Round 3 result'): one fresh Opus fixer on the Drape Studio engine path: the jacket with its cuff grip and the jeans (jobs in F:/LedgerTools/drapestudio-test-2026-11-13-final/jobs, copy and change only the output folder), at or better than Marvelous v19 and n7 on the judge and by eye; carry the ribs that do not grip and the shoulder ridge; keep job_j3 passing (M2) and M1 matching. Expect the jacket's sleeve stretch (5.47x) first. Brief pattern: the round 3 brief (in this session's history; rebuild it from LOOP.md and the report). Judge: drape_check_any.py on each job's plan (checks/plans.py in the Drape Studio final folder extracts them), bounds.py hang heights, pictures beside Marvelous's (production/previews/drapestudio-jacket-2026-11-11.jpg and -jeans-), one fresh final reviewer; a 'Round 4' section in the report; a row. Check bars.json M3's exact rule first.
3. Epic's baseline (149): the small C++ helper for outfit resizing (RESIZING-SCRIPT-CALLS-2026-11-11.md's closest route), Tom's jumper onto Ron and Darren, measured by the same judge; only when the card and Unreal are free and no Kiln timing runs beside it.
4. Loomwright hair loop, alternating with Kiln (first cluster: cards outside the scalp, with a camera coverage check).
5. By Monday 07:00 (advisor 144): his evaluation: milestones passed, numbers against Marvelous, hours spent, cost of the next milestones.
6. Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true, the doubled line.
7. Nothing touching Unreal 01:15 to 04:30. Tonight's walk: no game piece changed today.
8. Leftovers of mine (keep while rounds continue): C:/LedgerTools/mocap-solve (about 1 GB); F:/LedgerTools/tool-tests-2026-11/* (motionsmith-r2 keep rise430s_Body.fbx, r3, loomwright-r2, loomwright-cloth-r2, seamshift-r3, seamshift-r4, kiln-twin-check), F:/LedgerTools/drapestudio-test-2026-11-13 and -final, C:/LedgerTools/cargo-target (kiln, drapestudio). F: is at its 20 GB floor.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- A box passed every count (Kiln round 1) and closing seams after a simulation left ridges (round 2): judge every drape by eye beside the reference; close seams inside the steps.
- A set-aside input crept back into a test suite (the build bodies): refuse twins in the judge and the tool, never rely on a readme.
- A count passed a bad shape (Seamshift's sitting hem) and a lost layer passed every picture (Loomwright's jacket): judge every count beside a picture and check every layer is present.
- A folder-date check that skipped subfolders missed his Loomwright update for three hours: date the source files.
- Vellum on Tom's jumper 3 of 3, set aside. Cascadeur test 4, 2 of 2, set aside.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are'), plus the talk quality loop beside the provider bake-off (advisor 147, a small item), about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key.
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left).; HumanMotionCraft's retarget pelvis 2 of 2 (fixed: source retarget pose raised, root-motion step off). Ours: F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body (identical measurements); use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run heavy jobs beside the Drape Studio round before DONE; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; write into his folders under C:/Game Dev Tools.
