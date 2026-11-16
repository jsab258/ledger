# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-16 10:07 (the hourly run; the last session stopped at 09:16)
**Next due:** 2026-11-16 09:53 (the hourly row; then work paced to near 99% by 12:55, never 100%; about 12:50 the week's numbers; set it at every stop)
**Stopped:** 2026-11-16 09:16 (history past its point after the camera switch; all pushed to wip)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted by his tap 15 Nov 21:08; runs to 13:00 Monday 23 November). Until Monday 13:00 the advisor 168 pacing applies: near 99% by 12:55, never 100%; start nothing that cannot finish by 12:55.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). Write it with ArtifactData and see its version. "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing.**
- Pace rules: RULINGS 7, 10 Nov and 13 Nov; the 16 Nov reset week runs a doubled line from 13:00 Monday, six helpers, no busywork; rows name any hour with no session (advisor 140/143).
- Never end a turn while work remains (advisors 64, 68; the stop hook enforces it); the Stopped line is the last thing written (advisor 104).
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Advisors 111, 113, 117: paid-tools sweep before any second try; the tool driven without clicks; each garment its own time-log window.
- **Kiln (RULINGS 13 Nov; by design 14 Nov, now in RULINGS):** serves LEDGER; every module and fix names the game item it unblocks; no special cases ('special cases: none' in each report); held-back jobs at every milestone from M5; M7 the finish line, its count in every round report (0 so far). Time log "tool loop: <tool> round n". Caps: clothing about 20 h (12.6 spent), hair about 8 h. Its share this week is set by his answer to the advisor's 07:40 evaluation (held at 23% in the order).
- **He no longer develops any of his tools (advisor 146):** the copies under F:/LedgerTools/tool-dev are their only line of development.
- **Held-back jobs never reach a fixer:** never name the two held-back garments in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked in judge/HASHES.txt, 22 files, verified 07:10).

## Done this run (08:52 to 09:16)
- His own turn of 07:52 (gate hook on, FoldCraft and ast-grep on the licence list) left no Stopped line; this run took over. Advisor 170 (his answer A to the Kiln evaluation: Kiln front-loaded, about 35% Mon to Wed, about 20% after, 46 h; breadth patterns and held-back jobs first, then M5 without a hardening round, then M6; held-back result and renewal recommendation by about Thursday; Marvelous renews 26 Nov) acked (2026-11-16-0853-170). Row 2026-11-16-0853 written (meter 95%, pace +5.0). No verdicts after 2026-11-16T07:50Z, no advisor after 07:55+01:00 at 09:07.
- n16-6: OpenAiCompatibleClient built in ledger/DevTools (bench only), ten acceptance cases plus the review's fixes tested, CoreTests 5,254 pass, ci 101/101; review production/research/talk-providers/CLIENT-REVIEW-2026-11-16.md (pass with fixes, all taken). Commit 74db26f60, pushed. Not done: Models.Cost entries for candidates (set from each pricing page at the bake-off); keys (the router key is on the waiting list).
- n16-3 step 1: perf-hook.py's scale-test columns (in 74db26f60). The camera switch: -PerfHookCam=<id> in CrimeProbe.cpp, reading "cameras" then a new "measure_cameras" list in vignette-scene.json (kept apart so -PageShots, which takes every camera, does not grow a picture); cam_hill drafted (x 44, z 0, eye 1.7, yaw 16, pitch -3, fov 46), held back: see In flight.

## Earlier this morning (06:37 to 07:17; commits 856ecc080 rebased and the second part, both pushed, checks failed=none)
- Order section 1 into RULINGS (4,898 of 4,900 words). NOW.md on the 16 Nov order; HOURLY-TASK.md points at "the current order" generically.
- n16-3: method note (production/research/street-scale-test/METHOD-NOTE-2026-11-16.md), fourteen review fixes taken (section 7 binds). About 26 h plus 4 h card; at 2 to 4 times it overruns 40 h: a risk named in rows, cut to hook, walk and night views if long.
- n16-1: FoldCraft read (MIT; Kiln processor-only, the vendored card path the bigger lever). Round 10's speed brief, the code-search plan, the parity list in production/research/tool-tests-2026-11/ (KILN-*-2026-11-16.md, CODE-SEARCH-TEST-PLAN). Breadth set: Ron's donkey jacket and Titan wool trousers (MH_RoccoP2), Sheila's pleated skirt (MH_LenaS4; draft from meas_S4.json, not measurements.json), Darren's nylon jacket (MH_SamS6); two held back. Pattern plan production/art/clothing/BREADTH-PATTERNS-2026-11-16.md (FreeSewing blocks; only Tom has a Marvelous avatar: Ron, Sam, Lena need one import each). Ron's trousers are not a recoloured jeans variant (DECISIONS 07:09).
- n16-6: method note (production/research/talk-providers/METHOD-NOTE-2026-11-16.md), passed review with fixes; its last section binds (built this run).

## In flight
- The camera switch (-PerfHookCam, reading "cameras" then "measure_cameras" of vignette-scene.json): both targets built (build-local.ps1 "both targets built"), committed with this handover and pushed. cam_hill is NOT in the scene file: editing it makes ci's glass-bake-fresh fail (whole-file hash; a bake needs Unreal). Its entry waits at F:/LedgerTools/scratch/n16-3/cam_hill.json: add it at the next glass bake, or give measuring cameras their own file (C++ read plus stage_game_data.py line, memory packaged-copy-needs-ledgerrepo). The switch passes only in the night's packaged build and the tester's walk. Step 1's acceptance still needs: an unknown camera ends the game (a -PerfHookCam=cam_nope run, editor screen) and the cam_hill editor screen.
- No helper out. Meter 95% at 08:53 (pace +5.0). His reset press still pending: **when the meter drops, set reset_at in production/week-shape.json and say so in the next row.**
- His page: no open items (the gate-hook item closed by his turn of 07:52).
- DAILY file due 19:00 (as DAILY-2026-11-14.md). Monday: the week's numbers on the progress page, read the weekly figure about 12:50 before the reset, and republish the progress page then (its data already carries today's morning pictures).

## Next, in order
1. FIRST: fresh_gate's line must not say MODEL WRONG; verdicts after 2026-11-16T07:50:00Z; advisor after 2026-11-16T07:55+01:00 (170 acked). Hourly row due about 09:53.
2. Until 12:55, near 99%, only what finishes by then: (a) n16-6's bake-off, Sonnet 5.5 leg: write its questions first (speech-bench skill steps 1 to 3: newcomer real questions via ClaimBench `firsts`, small talk beside; cap in code; api-spend.jsonl; check api_batch.py's billing day of the 12th first); (b) Kiln round 10's bench step (his answer A puts Kiln at about 35% Mon to Wed, but its order is breadth patterns and held-back jobs first, from 13:00).
3. About 12:50: the week's numbers on the progress page and its republish; read the meter; when it drops, reset_at.
4. From 13:00 (doubled line, six helpers, Unreal and the card never idle): n16-3 step 1's rest (the office's fixed camera in "measure_cameras": its definition was not found in production/specs or tools, check the office gate's pictures in production/audits/office-2026-10-08 first; then an editor screen of cam_hill), then step 2 the scale switches; n16-1 the breadth patterns in Marvelous (bridge first; computer use only in Marvelous after 10 idle minutes; avatars for Ron, Sam, Lena), Kiln round 10, the code-search rounds; n16-6 the bake-off after the client; then the order's sequence.
5. Read-back of page verdicts at least every two days (last 16 Nov 07:00, verdicts to 15 Nov 20:08Z), then `python tools/page_answers.py --index`.
6. Kiln's disk cap on F: (n16-1): a retention rule with milestone evidence protected, not urgent.
7. Space check by 23:30 each night. Leftovers of mine (keep while rounds continue): C:/LedgerTools/mocap-solve, cargo-target; F:/LedgerTools/tool-tests-2026-11/* (keep rise430s_Body.fbx), drapestudio-test-2026-11-13 and -final.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 16 Nov: an unattended run may not edit the licence list or the project's settings: both refused by the safety check; they go to a turn he starts.
- 16 Nov, seen in passing (DECISIONS 09:03): AnthropicClient's stream registers the stop before opening its reader, so a token cancelled before the headers gives an ArgumentException, not a stop. Its paths were not touched; a candidate for the waiting list.
- Rounds 7 to 9: measure each check's cost on the real job; measure a named cause before fixing it; prove a new check on a fail and a pass control first. Rounds 4 and 5: guessed fixes failed: close-ups frame by frame, one-change tests first.
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4. 16 Nov: an edit of vignette-scene.json stales the glass bake (ci glass-bake-fresh).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept (autostash used for rebases, applied back each time).
- Waiting list for the next order: the talk quality loop beside the bake-off (advisor 147), about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key; as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed). F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body; use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since. Model spend US$7.77 from 07:52 to 08:53 (token_measures --spend).
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
