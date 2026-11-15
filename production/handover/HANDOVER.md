# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-15 07:51 (hourly run; the gate said GO: last stopped 06:52, no turn written for 59 minutes)
**Next due:** 2026-11-15 18:30 (DAILY-2026-11-15 file by 19:00 and the Monday evaluation drafted, step 5; no Kiln or hair round: 89% at 04:52, the last point kept for the evaluation, DECISIONS 15 Nov 04:52; the gate starts only a page check each 55 minutes, advisor 160; set it at every stop)
**Stopped:** 2026-11-15 07:57 (page check from 07:51: no new verdicts, advisor 165 acted on (community read saved, committed locally); ci red on page-answers-fresh, push held, step 1a; no row, row 2026-11-15-0452 states 18:30)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted 8 Nov 17:17; runs to 13:00 Monday 16 November). **Until Monday 16 Nov 07:00 Kiln has priority over the order's game work, clothing first (advisor 144, his pick 14:36)**; game items run only where Kiln waits (Unreal or the card idle). The weekly line still governs total usage.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). Write it with ArtifactData and see its version. "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing** (tools run fast: never estimate elapsed time).
- Pace rules: RULINGS 7, 10 Nov and 13 Nov (idle fine while on track; the 16 Nov reset week runs a doubled line from his adoption tap, six helpers, no busywork; rows in that week name any hour with no session, advisor 140/143).
- Never end a turn while work remains (advisors 64, 68); the Stopped line is the last thing written (advisor 104).
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open" (the field is "state", not "status"). Never list collections whole.
- Advisor 113: of two tools, prefer the one driven without clicks. Advisor 117: every garment's work its own time-log window. Advisor 111: check the paid-tools sweep before any second try.
- **Kiln (RULINGS 13 Nov 14:19, advisor 142):** serves LEDGER, never itself; every module and fix names the game item it unblocks and hours saved; 15% of a week's usage (suspended until Mon 07:00 by advisor 144); park rule: M3 by about 22 Nov or keep-or-drop. Time log "tool loop: <tool> round n". Caps: clothing about 20 h, hair about 8 h.
- **Weekend pacing (advisor 158, his pick 14 Nov 11:41, replaces 155's spacing; to Mon 07:00):** the meter is LEDGER's alone (his Fable project is off); Kiln rounds about every 4 hours, nights included outside 01:15 to 04:30, the spacing set from each round's measured cost (about 1 point) to land near 90% at Monday 07:00; never a round for the meter's sake; one fixer at a time, a fresh reviewer only where a milestone is judged, no extra helpers. A quiet check (nothing due, nothing new on his page or from the advisor) writes no row while the last row states the next time (advisor 160); it sets Stopped and stops.
- **M7 (his decision 14 Nov 12:33, advisor 159):** the Hook's whole garment list through Kiln is the clothing module's finish line; its count in every round report (0 so far, total not counted); no M7 work this weekend beyond M4.
- **Kiln stays general (his decision 14 Nov 08:32, advisor 157):** no special cases (each report: 'special cases: none' or what was refused); from M4 on two held-back jobs the fixer never sees; the Marvelous renewal rests on M4 plus their result (design note, 'Breadth by design').
- **He no longer develops any of his tools (advisor 146, 14:45):** the copies under F:/LedgerTools/tool-dev are their only line of development; no more rebasing on his folders.

## Run on 13 Nov (15:36 to 20:30, 21:06 to 22:05, 22:36 to its stop)
- Bodies (148): heavy Ron, slim Darren, average Tom; KILN_ENGINE=drapestudio; report KILN-ROUND1-2026-11-13.md.
- His 'Authored breadth' ruling (advisor 156) is RULINGS's first line; its note 6 (verified pieces per week by kind beside hours) goes into Monday's audit.
- **Kiln round 9, M4 MET** (report's 'Round 9'; kiln 72670c3, tag m4-2026-11-14; judge run runs/kiln-r4-judge/r9b): seen through 0, layered 144 s of 153, through over 3 mm 124 of 133 and worst edge 2.88 of 3 (thin), M1 to M3 byte for byte, reviewer pass with shortfalls. The added-pieces start check is opt-in (KILN_START_CHECK_FRESH=1; 12 s): making it cheaper is a listed shortfall.
- **14 Nov evening (advisors 162, 163):** guards after a run on the wrong model: fresh_gate.py reads each run's model from its log (wrong: due work only, MODEL WRONG in its line); `token_measures.py --spend` ends with the row's model words; `--by-model DAY` gives DAILY its table and JUMP line. C:'s root: `python tools/c_root_guard.py check` before and after every round (C-ROOT NEW fails it); every tool-loop output path goes through F:/LedgerTools/tool-dev/outpath.py.
- **Advisor 164 done by the advisor on his ask (advisor 165, 15 Nov 07:40):** saved unchanged as production/research/discord-scan/COMMUNITY-2026-11-14.md, committed locally 07:57; nothing else taken from it until he answers ideas 1, 2 and 5 for the 16 Nov order.

## In flight
- Nothing running. No helper is out. F: 20.0 GB by retention.py (a fixer reading GiB sees 18.6: briefs say 'by tools/retention.py'). Own leftovers of round 9: runs/fixer-r9/nofresh and rep, runs/kiln-r4-judge/r9 (the check-on run), runs/c-root-moved-2026-11-14 (34.8 MB); keep fixer-r9/review, closeups, METHOD-NOTE and r9b. F: was, at its floor: space check before every round; on STOP delete own unreferenced scratch first (next: runs/fixer-r6, fixer-r7/t, kiln-r4-judge/r5, r6; fixer-r8's a1, b2, c0, c1 if left; keep fixer-r8/final and kiln-r4-judge/r7, r8).
- No round started after about 23:50 (advisor 154).
- Pace: 89% at 04:52 Sunday (+13.5 on the line); no more rounds before Monday's order unless the meter shows room after the evaluation is drafted. Row 2026-11-15-0452 states the 18:30 time.
- His page: nothing open (the model and C: folder items closed 22:05 and 22:19).
- DAILY file: due 19:00 every day (as DAILY-2026-11-14.md, with runs by kind).

## Next, in order
1. FIRST: fresh_gate's line must not say MODEL WRONG; verdicts after 2026-11-14T21:12Z; advisor after 2026-11-15T07:40+01:00 (165, acted on; no ack needed beyond its commit).
1a. **ci red, push held:** page-answers-fresh fails (read-back last 12 Nov) because the scheduled task ledger-page-answers-nightly is disabled (last ran 12 Nov 04:46; no record of why: search NOTEBOOK and git log before asking). A scheduled run cannot edit a schedule; if it was not retired on purpose, re-enabling is his hands on his page; if retired, the check goes with it (a DECISIONS line). 165's commit is unpushed.
2. Kiln after M4: M5 (outfits refitted and rigged to the cast) waits for the 16 Nov order and its held-back jobs; until then only cheap shortfall work if the meter allows (the added-pieces start check made cheaper; the thin margins). Fixer briefs: free space by tools/retention.py, every output path through outpath.py, c_root_guard before and after.
3. Epic's baseline (149): the small C++ helper for outfit resizing, Tom's jumper onto Ron and Darren, same judge; only when the card and Unreal are free and no Kiln timing runs beside it; held while far ahead (155).
4. Loomwright hair loop, alternating with Kiln (first cluster: cards outside the scalp, with a camera coverage check); one round at a time (155).
5. By Monday 07:00 (advisor 144): his evaluation: milestones passed (M1, M2, M3), numbers against Marvelous, hours spent (timelog 'tool loop'), cost of the next milestones; adoption is his (LOOP.md's releases/vN; none made yet, tag m3-2026-11-14).
6. Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true, the doubled line.
7. Space check by 23:30.
8. Leftovers of mine (keep while rounds continue): C:/LedgerTools/mocap-solve (about 1 GB); F:/LedgerTools/tool-tests-2026-11/* (keep motionsmith-r2's rise430s_Body.fbx), F:/LedgerTools/drapestudio-test-2026-11-13 and -final, C:/LedgerTools/cargo-target.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Rounds 7 to 9: measure each check's cost on the real job; measure a named cause before fixing it; prove a new check on a fail and a pass control first.
- Rounds 4 and 5: guessed fixes failed (speed kept from sewing in frame 1): close-ups frame by frame, one-change tests first. Measure milestone jobs before briefing; judge counts beside pictures, every layer present.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: the breadth set (six jobs from HOOK-GARMENT-LIST-2026-11-03.md, patterns in Marvelous before 26 Nov, game items) and the held-back jobs' setup (about 1 h), advisor 157; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are'), plus the talk quality loop beside the provider bake-off (advisor 147, a small item), about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key.
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left).; HumanMotionCraft's retarget pelvis 2 of 2 (fixed: source retarget pose raised, root-motion step off). Ours: F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body (identical measurements); use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run heavy jobs beside the Drape Studio round before DONE; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; write into his folders under C:/Game Dev Tools.
