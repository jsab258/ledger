# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-14 07:36 (hourly run; the gate said GO: last stopped 06:52, no turn written for 43 minutes)
**Stopped:** 2026-11-14 08:39 (run from 07:36: Kiln round 6, M3 met; advisor 157 acted on and acked; 81% against 64.2%, 16.8 ahead; next round, M4, not before about 16:30; nothing running)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted 8 Nov 17:17; runs to 13:00 Monday 16 November). **Until Monday 16 Nov 07:00 Kiln has priority over the order's game work, clothing first (advisor 144, his pick 14:36)**; game items run only where Kiln waits (Unreal or the card idle). The weekly line still governs total usage.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). Write it with ArtifactData and see its version. "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing**.
- Pace rules: RULINGS 7, 10 Nov and 13 Nov (idle fine while on track; the 16 Nov reset week runs a doubled line from his adoption tap, six helpers, no busywork; rows in that week name any hour with no session, advisor 140/143).
- Never end a turn while work remains (advisors 64, 68); the Stopped line is the last thing written (advisor 104).
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open" (the field is "state", not "status"). Never list collections whole.
- Advisor 113: of two tools, prefer the one driven without clicks. Advisor 117: every garment's work its own time-log window. Advisor 111: check the paid-tools sweep before any second try. Launcher ruling (RULINGS 11 Nov) as written.
- **Kiln (RULINGS 13 Nov 14:19, advisor 142):** serves LEDGER, never itself; every module and fix names the game item it unblocks and hours saved; 15% of a week's usage (suspended until Mon 07:00 by advisor 144); park rule: M3 by about 22 Nov or keep-or-drop. Time log "tool loop: <tool> round n". Caps: clothing about 20 h, hair about 8 h.
- **Weekend pacing (advisor 155, 13 Nov 21:40, to Mon 07:00):** part of the meter is his own project; pace Kiln to the line, not ahead: one fixer round at a time, a fresh reviewer only where a milestone is judged, no extra helpers; while more than 6 points ahead, a hold of at least 30 minutes between rounds even with the priority mark; aim about 90% at Monday 07:00 including his use.
- **Kiln stays general (his decision 14 Nov 08:32, advisor 157):** no special cases (each report: 'special cases: none' or what was refused); from M4 on two held-back jobs the fixer never sees; the Marvelous renewal rests on M4 plus their result (design note, 'Breadth by design').
- **He no longer develops any of his tools (advisor 146, 14:45):** the copies under F:/LedgerTools/tool-dev are their only line of development; no more rebasing on his folders.

## Run on 13 Nov (15:36 to 20:30, 21:06 to 22:05, 22:36 to its stop)
- Earlier runs: bodies (advisor 148): heavy = Ron (RoccoP2), slim = Darren (SamS6), average = Tom, twins refused; 149: Epic's Panel Cloth and outfit resizing a baseline (RESIZING-SCRIPT-CALLS-2026-11-11.md: about 4 h on a small C++ helper, no clicks); Kiln rounds 1 to 4: M2 met on the Drape Studio engine path (KILN_ENGINE=drapestudio). Report KILN-ROUND1-2026-11-13.md, a section per round.
- **His 'Authored breadth' ruling (advisor 156, 23:02) is RULINGS's first line**; notes in game-design/authored-breadth-2026-11-13.md; the hair pass list moved to production/art/hair-2026-09-29/PASS-LIST.md to keep the cap (4,898 of 4,900). Its note 6 (verified pieces per week by kind beside hours) goes into Monday's audit. Acknowledged.
- **Run 14 Nov 07:36: Kiln round 6, M3 MET** (report's 'Round 6'; preview kiln-round6-2026-11-14; Kiln commit 63753e3, tag m3-2026-11-14; fixer 41 min, round 55 min; one fresh final reviewer: pass by eye, runs/kiln-r4-judge/r6/REVIEW-M3.md).  Jacket worst edge 2.08x, through 0, 109 s; jeans pass (top edge 19 and 20 of 25: watch); jumper front 41 of 63; M1 matches; the judge's run byte-identical. Rows 07:39 and 08:33.

## In flight
- Nothing running. No helper is out. Scratch on F: (runs/fixer-r1, r3 to r6, runs/kiln-r4-judge with r6; F: 20.0 GB, at its floor: space check before every round; on STOP delete own unreferenced scratch first).
- Advisor 154: Kiln carries on through the night; no round 01:15 to 04:30 and none started after about 23:50.
- Pace to Monday 07:00 (advisor 155): 81% at 08:33 against 64.2%; 9 points left to 90%, part of them his; a round with its session cost about 1 to 3 points. So at most about two more rounds and Monday's evaluation: one about every eight hours (the next not before about 16:30 on 14 Nov), and a session that finds no round due reads his page, writes Stopped and stops at once.

## Next, in order
1. FIRST: pace (advisor 155: to the line, not ahead; the spacing above); verdicts after 2026-11-13T19:30Z (none since); advisor after the latest ack (2026-11-14-0835-157).
2. Kiln M4, jacket over jumper, one cloth system (about 16:30, 14 Nov). The session first: write M4's bars in the judge (judge/bars.json has only a title for M4; then re-make HASHES.txt), choose or build the job (Marvelous's layered jacket-over-jumper job if one exists under F:/LedgerTools/drapestudio-test-2026-11-13-final/jobs or the Marvelous exports; search first; else the two M2/M3 jobs combined), and run it through Kiln AS IT STANDS before any fixer is briefed (round 4's lesson). Then one fresh Opus fixer (the diagnoser agent, its brief saying "diagnose AND fix"; the brief's rules are in LOOP.md and the report's Round 6: close-ups frame by frame and one-change tests before any fix, general fixes only, folder runs/fixer-r7 from fixer-r6/run.sh, CARGO_TARGET_DIR=C:/LedgerTools/cargo-target/kiln, never read job files whole, never edit judge/ or jobs, no clicks, byte-identical repeats, M1 to M3 kept, two tries per fault). Judge: `bash F:/LedgerTools/tool-dev/runs/kiln-r4-judge/judge_r5.sh rN m1` keeps M1 to M3; add the M4 job to a copy of it. One fresh final reviewer only when the counts pass. Round 7's brief adds the no-special-cases rule and has KILN_DEBUG_SEAMS log every seam or go. Carried shortfalls (fix only where a general cause shows): lumpy sleeve surface, sawtooth zip line, collar ripple, armhole puckers, the right cuff's 1 cm tuck, hem gathers, ribs that do not grip, the jumper's shoulder ridge.
3. Epic's baseline (149): the small C++ helper for outfit resizing, Tom's jumper onto Ron and Darren, same judge; only when the card and Unreal are free and no Kiln timing runs beside it; held while far ahead (155).
4. Loomwright hair loop, alternating with Kiln (first cluster: cards outside the scalp, with a camera coverage check); one round at a time (155).
5. By Monday 07:00 (advisor 144): his evaluation: milestones passed (M1, M2, M3), numbers against Marvelous, hours spent (timelog 'tool loop'), cost of the next milestones; adoption is his (LOOP.md's releases/vN; none made yet, tag m3-2026-11-14).
6. Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true, the doubled line.
7. Nothing touching Unreal 01:15 to 04:30. Space check by 23:30.
8. Leftovers of mine (keep while rounds continue): C:/LedgerTools/mocap-solve (about 1 GB); F:/LedgerTools/tool-tests-2026-11/* (keep motionsmith-r2's rise430s_Body.fbx), F:/LedgerTools/drapestudio-test-2026-11-13 and -final, C:/LedgerTools/cargo-target.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Rounds 4 and 5 on the cuffs: a wrap hold on open bands, seams closing gradually and a cap on seam pull per pass all failed; the cause (round 6) was speed kept from sewing in frame 1: close-ups frame by frame and one-change tests before a fix.
- A start check added in one round refused the next round's garments outright (round 4): measure every milestone's jobs as they stand before briefing a fixer.
- A set-aside input crept back into a test suite (the build bodies): refuse twins in the judge and the tool, never rely on a readme.
- A count passed a bad shape (Seamshift's sitting hem) and a lost layer passed every picture (Loomwright's jacket): judge every count beside a picture and check every layer is present.
- Vellum on Tom's jumper 3 of 3, Cascadeur test 4, 2 of 2: set aside.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the breadth set (six jobs from HOOK-GARMENT-LIST-2026-11-03.md, patterns in Marvelous before 26 Nov, game items) and the held-back jobs' setup (about 1 h), advisor 157; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are'), plus the talk quality loop beside the provider bake-off (advisor 147, a small item), about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key.
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left).; HumanMotionCraft's retarget pelvis 2 of 2 (fixed: source retarget pose raised, root-motion step off). Ours: F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body (identical measurements); use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run heavy jobs beside the Drape Studio round before DONE; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; write into his folders under C:/Game Dev Tools.
