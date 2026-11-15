# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-15 22:07 (hourly run; the gate said GO: last stopped 21:07)
**Next due:** 2026-11-16 07:00 (advisor 168: quiet tonight; from about 07:00 Monday preparation for the 16 Nov order paced to near 99% by 12:55, never 100%; set it at every stop)
**Stopped:** 2026-11-15 22:12 (his taps of 21:08 acted on: the 16 Nov order adopted; the gate hook refused unattended, waits for a turn he starts; advisor 168 acked: quiet until about 07:00 Monday; row 2026-11-15-2209 states it)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted by his tap 15 Nov 21:08; runs to 13:00 Monday 23 November). Until Monday 13:00 only the advisor 168 pacing applies: quiet tonight, preparation from about 07:00 Monday aiming near 99% by 12:55, never 100%.

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

## In flight
- Nothing running. No helper is out. F: 20.0 GB by retention.py (a fixer reading GiB sees 18.6: briefs say 'by tools/retention.py'). Own leftovers of round 9: runs/fixer-r9/nofresh and rep, runs/kiln-r4-judge/r9 (the check-on run), runs/c-root-moved-2026-11-14 (34.8 MB); keep fixer-r9/review, closeups, METHOD-NOTE and r9b. F: was, at its floor: space check before every round; on STOP delete own unreferenced scratch first (next: runs/fixer-r6, fixer-r7/t, kiln-r4-judge/r5, r6; fixer-r8's a1, b2, c0, c1 if left; keep fixer-r8/final and kiln-r4-judge/r7, r8).
- Pace: 91% at 18:36 Sunday (+7.9 on the line); no more rounds before Monday's order. Row 2026-11-15-1841 states the 23:15 time.
- His page: nothing open. **His taps of 21:08 (15 Nov):** order of 16 Nov adopted: week-shape.json active, goal line, order check PASS, items closed (DECISIONS 22:09). Still due from the adoption: when the meter drops after his reset press set reset_at; before Mon 13:00 a row confirming HOURLY-TASK.md and this file point at the current order; the order's section 1 records (Discord line, Kiln by design) into RULINGS within its cap.
- **Gate hook: his yes (21:09), NOT installed:** the unattended run's safety check refused the edit of .claude/settings.json (adding a UserPromptSubmit hook, command `python "$CLAUDE_PROJECT_DIR/tools/gate_prompt_hook.py"`, timeout 30). Do not work round it. It needs a turn he starts at the PC (he types, e.g., "install the gate hook"); then commit and measure from gate-blocked.jsonl as planned.
- DAILY file: due 19:00 every day (as DAILY-2026-11-14.md, with runs by kind).

## Next, in order
1. FIRST: fresh_gate's line must not say MODEL WRONG; verdicts after 2026-11-15T20:09Z (read 22:08 Swiss); advisor after 2026-11-15T22:09+01:00 (168 acked). Advisor 168 governs until Mon 13:00: no work before about 07:00 Monday; then, reading the meter at every step: the breadth set's patterns and held-back jobs set up, FoldCraft's solver read, the street scale test's method note (n16-3), the code-search test made ready; start nothing that cannot finish by 12:55; stop near 99%.
1a. **Read-back by the session (DECISIONS 15 Nov 09:10):** the nightly answers task was switched off by him on 12 Nov; read his page's verdicts back into production/approvals/answers by a filtered read at least every two days (last 15 Nov 09:10, verdicts to 2026-11-14T21:11Z), then `python tools/page_answers.py --index`, or page-answers-fresh holds the push.
2. Kiln after M4: M5 (outfits refitted and rigged to the cast) waits for the 16 Nov order and its held-back jobs; until then only cheap shortfall work if the meter allows (the added-pieces start check made cheaper; the thin margins). Fixer briefs: free space by tools/retention.py, every output path through outpath.py, c_root_guard before and after.
3. Epic's baseline (149, held while ahead) and the Loomwright hair loop (now n16-8) wait for the new order.
5. Monday's evaluation (advisor 144): DRAFTED 15 Nov 18:40, production/research/tool-tests-2026-11/KILN-EVALUATION-2026-11-16.md (M1 to M4 met, numbers against Marvelous, 12.6 h of 20, next milestones' cost); point the advisor's 07:40 evaluation to it; adoption is his (none made yet, tag m4-2026-11-14).
6. Monday's audit: 'Authored breadth' note 6 (verified pieces per week by kind beside hours; advisor 156). Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true, the doubled line.
7. Space check by 23:30.
8. Leftovers of mine (keep while rounds continue): C:/LedgerTools/mocap-solve, cargo-target; F:/LedgerTools/tool-tests-2026-11/* (keep rise430s_Body.fbx), drapestudio-test-2026-11-13 and -final.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Rounds 7 to 9: measure each check's cost on the real job; measure a named cause before fixing it; prove a new check on a fail and a pass control first.
- Rounds 4 and 5: guessed fixes failed: close-ups frame by frame, one-change tests first.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: **advisor 166 (his pick A, 15 Nov 07:59; about 3 h inside Kiln's share, nothing before the order): FoldCraft onto the allowlist as MIT (notice in Kiln's third-party file) and its GPU solver read for speed and layer separation before Kiln's speed work, reuse with notice; Kiln's parity list against Marvelous (layering, sewing, fabrics, poses and sitting, pressing and pleats, women's garments, export to Unreal) beside M7's count in every round report; a code-search tool for fixers (licence first, or one we have), two rounds with and two without, kept only if cheaper at the same quality**; the breadth set (six jobs from HOOK-GARMENT-LIST-2026-11-03.md, patterns in Marvelous before 26 Nov, game items) and the held-back jobs' setup (about 1 h), advisor 157; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are'), plus the talk quality loop beside the provider bake-off (advisor 147, a small item), about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key.
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left).; HumanMotionCraft's retarget pelvis 2 of 2 (fixed: source retarget pose raised, root-motion step off). Ours: F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body (identical measurements); use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run heavy jobs beside the Drape Studio round before DONE; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; write into his folders under C:/Game Dev Tools.
