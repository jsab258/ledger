# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-13 22:36 (hourly run; the gate said GO: last stopped 22:05, no turn written for 31 minutes)
**Stopped:** 2026-11-13 23:55 (run from 22:36: Kiln round 5 judged, the jeans pass, the jacket's cuffs fail, M3 not met with progress; advisor 156's ruling written and acknowledged; stopped at the item's end, no helper out, no priority mark: the pace hold applies and no round fits before the night window)
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
- **He no longer develops any of his tools (advisor 146, 14:45):** the copies under F:/LedgerTools/tool-dev are their only line of development; no more rebasing on his folders.

## Run on 13 Nov (15:36 to 20:30, 21:06 to 22:05, 22:36 to its stop)
- Earlier runs: bodies (advisor 148): heavy = Ron (RoccoP2), slim = Darren (SamS6), average = Tom, twins refused; 149: Epic's Panel Cloth and outfit resizing a baseline (RESIZING-SCRIPT-CALLS-2026-11-11.md: about 4 h on a small C++ helper, no clicks); Kiln rounds 1 to 3, **M2 met** on the Drape Studio engine path (KILN_ENGINE=drapestudio); round 4: jacket and jeans drape (72b1e94dd). Report KILN-ROUND1-2026-11-13.md, a section per round.
- This run: **Kiln round 5 judged, M3 not met, progress** (report's 'Round 5'; preview kiln-round5-2026-11-13; Kiln commit bb84846; fixer 57 min, no reviewer): **the jeans pass every M3 count** (friction had been applied twice; hang 69 to 1,098, waistband 1,076 to 1,133, 64 s). The jacket fails: worst edge 6.38x (left sleeve above the cuff seam), cuffs crumpled wads; back hang 22 mm off (bar 25, was 14); body-through 48 (was 9, bar 103); hem band about 24 mm higher. Jumper passes M2 with its front piece at 61 edges of 63. M1 matches; the judge's run byte-identical to the fixer's.
- **His 'Authored breadth' ruling (advisor 156, 23:02) is RULINGS's first line**; notes in game-design/authored-breadth-2026-11-13.md; the hair pass list moved to production/art/hair-2026-09-29/PASS-LIST.md to keep the cap (4,898 of 4,900). Its note 6 (verified pieces per week by kind beside hours) goes into Monday's audit. Acknowledged.
- Allowance 77% at 23:34 against 59.2% (about 3 points a round with its session).

## In flight
- Nothing running. No helper is out. Scratch on F: (runs/fixer-r1..r5, runs/kiln-r4-judge; F: at its floor). Empty stray F:/f/LedgerTools: Sunday's leftovers.
- Advisor 154: Kiln carries on through the night; only Unreal and processor-heavy drape runs pause 01:15 to 04:30 (the judge's and a fixer's drape runs are processor-heavy: no round in that window, and none started after about 23:50, a round with its judging takes 80 minutes); a short night summary in the 07:00 handover.
- Pace to Monday 07:00 (advisor 155): 13 points left to 90%, part of them his; a round costs about 3. So at most about three more rounds and Monday's evaluation: space them (about one every eight hours), and a session that finds no round due reads his page, writes Stopped and stops at once.

## Next, in order
1. FIRST: pace (advisor 155: to the line, not ahead; the spacing above); verdicts after 2026-11-13T19:30Z (none since); advisor after the latest ack (2026-11-13-2304-156).
2. Kiln round 6, still M3, one fresh Opus fixer, at most about 70 min, not before 04:30 (brief pattern: this run's round 5 brief, rebuilt from LOOP.md's 'Round 5 result' and the report's Round 5 section; rules: no clicks, never read the job files whole (25,000-token PLAN lines), never edit judge/ or the jobs, build with CARGO_TARGET_DIR=C:/LedgerTools/cargo-target/kiln, own folder runs/fixer-r6 (copy fixer-r5/run.sh with the paths changed), general fixes only, runs repeat byte for byte, the jeans' and jumper's passes kept). Targets in order: what crumples the open cuff in frames 1 to 5 (it starts as a C-shaped ring with an 84 to 89 mm gap; test KILN_TUBE_CLEAR=0, the cuff-to-sleeve seam's pull, a band stiff along its length only; the tried diff is runs/fixer-r5/tried-wrap-hold-and-gradual-sew.diff); why body-through rose 9 to 48 and the hem band 24 mm; the jumper's front piece (61 of 63); then the grip stage, zip line, collar ripple, armhole puckers; carried: ribs that do not grip, the jumper's shoulder ridge. Judge: `bash F:/LedgerTools/tool-dev/runs/kiln-r4-judge/judge_r5.sh r6 m1` (about 6 min; cuff and wide views included), judge/HASHES.txt checked first, counts against bars.json M3, pictures beside production/previews/drapestudio-jacket-2026-11-11.jpg and -jeans-; one fresh final reviewer only when the counts pass; a 'Round 6' section; a row. M3 with two rounds and no measured progress is set aside (rounds 4 and 5 each had progress).
3. Epic's baseline (149): the small C++ helper for outfit resizing, Tom's jumper onto Ron and Darren, same judge; only when the card and Unreal are free and no Kiln timing runs beside it; held while far ahead (155).
4. Loomwright hair loop, alternating with Kiln (first cluster: cards outside the scalp, with a camera coverage check); one round at a time (155).
5. By Monday 07:00 (advisor 144): his evaluation: milestones passed, numbers against Marvelous, hours spent, cost of the next milestones.
6. Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true, the doubled line.
7. Nothing touching Unreal 01:15 to 04:30. Tonight's walk: no game piece changed today; space checked 22:38 (C: 71 GB, F: 20.0 GB, GO).
8. Leftovers of mine (keep while rounds continue): C:/LedgerTools/mocap-solve (about 1 GB); F:/LedgerTools/tool-tests-2026-11/* (keep motionsmith-r2's rise430s_Body.fbx), F:/LedgerTools/drapestudio-test-2026-11-13 and -final, C:/LedgerTools/cargo-target.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Round 5: a wrap hold on open bands and seams closing gradually both failed (cuffs still crumple; the jacket never settled); a cap on seam pull per pass (round 4) too. A fault blamed on the open phase's length was in frames 1 to 5: close-ups frame by frame before a fix.
- A start check added in one round refused the next round's garments outright (round 4): measure every milestone's jobs as they stand before briefing a fixer.
- A set-aside input crept back into a test suite (the build bodies): refuse twins in the judge and the tool, never rely on a readme.
- A count passed a bad shape (Seamshift's sitting hem) and a lost layer passed every picture (Loomwright's jacket): judge every count beside a picture and check every layer is present.
- Vellum on Tom's jumper 3 of 3, Cascadeur test 4, 2 of 2: set aside.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are'), plus the talk quality loop beside the provider bake-off (advisor 147, a small item), about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key.
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left).; HumanMotionCraft's retarget pelvis 2 of 2 (fixed: source retarget pose raised, root-motion step off). Ours: F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body (identical measurements); use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run heavy jobs beside the Drape Studio round before DONE; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; write into his folders under C:/Game Dev Tools.
