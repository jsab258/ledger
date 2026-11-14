# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-14 12:21 (hourly run; the gate said GO: last stopped 11:37, no turn written for 44 minutes)
**Stopped:** 2026-11-14 14:09 (run from 12:21: Kiln round 7, M4 not met, the layered job now runs in 134 s; round 8 about 16:30; nothing running, no helper out; 83% against 67.3%, 15.7 ahead)
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
- **Weekend pacing (advisor 158, his pick 14 Nov 11:41, replaces 155's spacing; to Mon 07:00):** the meter is LEDGER's alone (his Fable project is off); Kiln rounds about every 4 hours, nights included outside 01:15 to 04:30, the spacing set from each round's measured cost (about 1 point) to land near 90% at Monday 07:00; never a round for the meter's sake; one fixer at a time, a fresh reviewer only where a milestone is judged, no extra helpers. A session that finds no round due still leaves one short row (advisor's 12:08 watchdog).
- **M7 (his decision 14 Nov 12:33, advisor 159):** the Hook's whole garment list through Kiln is the clothing module's finish line; its count in every round report (0 so far, total not counted); no M7 work this weekend beyond M4.
- **Kiln stays general (his decision 14 Nov 08:32, advisor 157):** no special cases (each report: 'special cases: none' or what was refused); from M4 on two held-back jobs the fixer never sees; the Marvelous renewal rests on M4 plus their result (design note, 'Breadth by design').
- **He no longer develops any of his tools (advisor 146, 14:45):** the copies under F:/LedgerTools/tool-dev are their only line of development; no more rebasing on his folders.

## Run on 13 Nov (15:36 to 20:30, 21:06 to 22:05, 22:36 to its stop)
- Earlier runs: bodies (advisor 148): heavy = Ron (RoccoP2), slim = Darren (SamS6), average = Tom, twins refused; 149: Epic's outfit resizing a baseline (RESIZING-SCRIPT-CALLS-2026-11-11.md: about 4 h, a small C++ helper); Kiln's engine path is KILN_ENGINE=drapestudio. Report KILN-ROUND1-2026-11-13.md, a section per round.
- His 'Authored breadth' ruling (advisor 156) is RULINGS's first line (cap 4,898 of 4,900); its note 6 (verified pieces per week by kind beside hours) goes into Monday's audit.
- Run 14 Nov 07:36: Kiln round 6, M3 MET (63753e3, tag m3-2026-11-14; report's 'Round 6').
- **Run 14 Nov 12:21: Kiln round 7, M4 NOT met, large progress** (report's 'Round 7'; preview kiln-round7-2026-11-14; Kiln f1bc759; judge f48ca07 with M4's and M7's bars and drape/layer/layer_check.py; fixer 47 min). The layered job went from not finishing in 2,400 s to 134 s (bar 153), byte-identical, 22 pieces present, M1 to M3 kept. Fails on the judge's run (runs/kiln-r4-judge/r7): jumper seen through 15 (bar 0), right sleeve 5.98x at the cuff (bar 3x), the opened jumper's rib pieces come back coarser. Rows 12:24, 13:05, 14:06; advisors 158, 159 and the 12:08 watchdog acknowledged.

## In flight
- Nothing running. No helper is out. F: 20.5 GB, at its floor: space check before every round; on STOP delete own unreferenced scratch first (next: runs/fixer-r6, kiln-r4-judge/r5, fixer-r7/t; keep fixer-r7/final and kiln-r4-judge/r6, r7).
- No round 01:15 to 04:30 and none started after about 23:50 (advisor 154).
- Pace to Monday 07:00 (advisor 158): 83% at 14:05 against 67.3%; 7 points to 90%, a round with its session about 1 point. Round 7 started 12:21; **round 8 about 16:30**, then about every 4 hours. A session that finds no round due reads his page, writes one short row, sets Stopped and stops.

## Next, in order
1. FIRST: pace and the spacing above; verdicts after 2026-11-14T13:00Z (none since 13 Nov); advisor after the latest ack (2026-11-14-1236-159).
2. Kiln round 8, M4 (about 16:30, 14 Nov): one fresh Opus fixer (the diagnoser agent, brief "diagnose AND fix"; rules in LOOP.md's last lines and the report's Round 7; folder runs/fixer-r8 from fixer-r7/run.sh, which has the layered job (G=layer, JUMPER=, LAYER_CAP=); CARGO_TARGET_DIR=C:/LedgerTools/cargo-target/kiln; never read job or OBJ files whole, never edit judge/ or jobs, no clicks, byte-identical repeats, M1 to M3 kept, two tries per fault, general fixes only, 'special cases: none'; it must return its report as its answer, it cannot write REPORT.md). Its order: (a) an opened project keeps each piece's point spacing (the jumper's ribs come back coarser: welts 1,339 to 494 points); (b) jacket points against the frozen garment's triangles with thickness (jumper seen through 15: armholes at the back, right cuff; 0 tries used); (c) the right sleeve's 5.98x at the cuff, the grip closing over the jumper's cuff, close-ups frame by frame first (0 tries used); (d) judge the two older name rules (arrangement points 'Neck_'/'Body_', fabric preset by name words). Judge: `LAYER_CAP=600 bash F:/LedgerTools/tool-dev/runs/kiln-r4-judge/judge_r7.sh r8 m1` (check HASHES.txt first; if judge/ changes, re-make it with two spaces, not sha256sum's ' *'). One fresh final reviewer only when the counts pass. Carried shortfalls: the report's Round 6 list.
3. Epic's baseline (149): the small C++ helper for outfit resizing, Tom's jumper onto Ron and Darren, same judge; only when the card and Unreal are free and no Kiln timing runs beside it; held while far ahead (155).
4. Loomwright hair loop, alternating with Kiln (first cluster: cards outside the scalp, with a camera coverage check); one round at a time (155).
5. By Monday 07:00 (advisor 144): his evaluation: milestones passed (M1, M2, M3), numbers against Marvelous, hours spent (timelog 'tool loop'), cost of the next milestones; adoption is his (LOOP.md's releases/vN; none made yet, tag m3-2026-11-14).
6. Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true, the doubled line.
7. Nothing touching Unreal 01:15 to 04:30. Space check by 23:30.
8. Leftovers of mine (keep while rounds continue): C:/LedgerTools/mocap-solve (about 1 GB); F:/LedgerTools/tool-tests-2026-11/* (keep motionsmith-r2's rise430s_Body.fbx), F:/LedgerTools/drapestudio-test-2026-11-13 and -final, C:/LedgerTools/cargo-target.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Round 7: layer friction that grips while seams close left seams 5 to 14 mm open (dropped; friction without grip while sewing kept). A layer check aimed at the nearest body point miscounted at the armpit: prove a new check on a fail and a pass control first.
- Rounds 4 and 5 on the cuffs: three guessed fixes failed; the cause was speed kept from sewing in frame 1: close-ups frame by frame and one-change tests before a fix.
- Measure every milestone's jobs as they stand before briefing a fixer (round 4).
- Judge every count beside a picture and check every layer is present (Seamshift's hem, Loomwright's jacket).
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the breadth set (six jobs from HOOK-GARMENT-LIST-2026-11-03.md, patterns in Marvelous before 26 Nov, game items) and the held-back jobs' setup (about 1 h), advisor 157; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are'), plus the talk quality loop beside the provider bake-off (advisor 147, a small item), about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key.
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left).; HumanMotionCraft's retarget pelvis 2 of 2 (fixed: source retarget pose raised, root-motion step off). Ours: F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body (identical measurements); use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run heavy jobs beside the Drape Studio round before DONE; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; write into his folders under C:/Game Dev Tools.
