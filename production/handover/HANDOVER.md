# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 06:22 (the hourly run; the last session set its Stopped line at 06:19)

**Row due:** 2026-11-17 10:27 (last 09:27; page and advisor read 09:30)
**Stopped:** 2026-11-17 09:52 (history near its hard stop at an item's end; all helpers reported; two days-old fixer-r5 wait loops (bash 14768, 20724) are not this session's and were left)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted by his tap 15 Nov 21:08; runs to 13:00 Monday 23 November). The doubled line runs from 0 at Monday 13:00 to 95% by Wednesday 15:00, six helpers, full pace. week-shape.json's reset_at stays null until HE presses the spare reset.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing**.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page or the progress page: read the live page and each published file first (out_dir to the scratchpad), diff, then publish.
- Advisors 111, 113, 117: paid-tools sweep before any second try; each garment its own time-log window.
- **Kiln (RULINGS 13 and 14 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone from M5; M7 count in every round report (0 so far). Time log "tool loop: <tool> round n".
- **Advisor 182 (his 14:12), trial from 16 Nov for two to three days:** Kiln rounds and their judging run in helpers that hand back a short verdict only (counts, reviewer's line, files); judged by history share and rework in the DAILY files against last week's 24%.
- **Advisor 181 (his 14:06):** helpers on the cheapest model that matches: reading, extraction, imports, log summaries, first screens, routine edits go to the project's Sonnet agents (extractor, importer, research-reader, small-reviewer), never general-purpose; Opus (diagnoser, research-synthesis, final-reviewer) for diagnosis, design, judged fixes, final reviews.
- **His pick A, 16 Nov 12:24 (advisor 174):** breadth patterns from FreeSewing and GarmentCode into Kiln's job format; Marvelous only for comparison drapes while its bridge is up; the bridge's start recovers by itself (closing the Welcome window, restarting by script) and is never raised on his page again. Own leftovers deleted under RULINGS 29 Oct, never a page item (the page tool refuses one).
- **Held-back jobs never reach a fixer:** never name the two held-back garments in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked).

- **Advisor 189 (his 08:02, 17 Nov):** every hourly row names F:'s free room and the next 12 h's need (clear it that hour if short) and the gap to the line; `python tools/retention.py space` before every Kiln round, film, build, capture and in every helper brief; each round deletes its own bulky outputs once its numbers are reported (1 GB a job); no delete outside retention.py without its protected list and readers checked; before 01:15 each night queue machine-free work for the allowed helpers. **Advisors 190-192 (his 08:20, 09:07, 09:25):** no new drives ever; superseded gate pictures and the Game Animation Sample copy (if unread) may go, list first (production/research/disk/CLEAROUT-LIST-2026-11-17.md); target a steady 1.4 points an hour day and night, each row giving the 6-hour rate and when 93% comes (he presses the spare reset near 93%; asleep near 93%: stay under 95%); when the current order waits on the machine, free helper places take the next order's machine-free work, recorded in the order ledger.

- **Before writing Stopped: end every background job of your own** (fresh_gate.py since 17 Nov holds starts up to 120 min while any session's background command still runs).

## Done the runs before
- git show 4b16a336e:production/handover/HANDOVER.md (04:52 to 06:19), d74c1862d, 5606f2805, 9f155e60f, 983ad87da.

## Done this run (06:22 to the stop), all committed and pushed to wip
- Tester fix (Sheila "missing" was the tester); start-check fix (fresh_gate.py: running background commands hold, claude -p not counted); scale ladder read (100 MB a street-length, +0.2 ms).
- n16-7: hip-joint method 7 of 36 failing (try 1 9) after the measure floor fix; stopped, kept default; knees note production/research/n16-7-knees-method-2026-11-17.md.
- n16-1: Kiln main aab3778 (skirt, trousers lanes in; gate exit fix); M5 method reviewed (41-69 h: this week Ron's trousers only, rest on the waiting list); M5 step 1 code (tools/md/bend_back.py, Ron's turns record PASS).
- n16-5: fronts launderette to chandler checked (no own change; 0.65 h); S1 street-level wear to x 48 with gable feet (tools/street_wear.py, production/specs/street-wear.json; pictures F:/LedgerTools/gate/new/s1-street-level-n16-5-2026-11-17/, previews production/previews/n16-5-*): a whole-frame change, held for his batched look before main.
- Held: n16-8 Darren's head (editor launch refused to a helper); the F: clear-out (production/research/disk/CLEAROUT-LIST-2026-11-17.md: retention protects gate, the direct delete refused by the permission system; told him 09:35).

## Next, in order
0. FIRST: verdicts after 2026-11-17T08:40:00Z; advisor after 2026-11-17T09:30:00+01:00 (last ack 09:16). Row due 10:27 (give the 6-hour rate and the 93% time).
1. n16-5 S2 (the grey row to the photographed brick): inputs ready (tile production/assets/scanned/photo_flemish_n16_5_grey on F: game inputs, before pictures F:/LedgerTools/gate/new/s2-grey-brick-n16-5-2026-11-17/before); left: the C++ houses filter (patches in the 06:22 session's scratchpad: patch_vs.py, patch_corner.py, may be gone: rewrite from the note), after pictures, match check, brick_ids accepting the entry. FOUND: editor runs read scan pictures from the checkout and the n16-4 brick files are only on F:, so every editor picture since 16 Nov shows the drawn brick (packaged unaffected): fix the editor's path or copy before judging any brick picture. The kerb-top marks read 0% in corner and S1: look. Then S1+S2 pictures to his batched rough-street page.
2. n16-1: jackets lane 9b3f4c6 try 1 of 2 failed (14 lines out; donkey made); try 2 with the collar-plane fix 1b88925; re-take the baseline. M5 next: a real Kiln drape of Ron's trousers on the standard body, then bend_back. Zips patch parked (F:/LedgerTools/tool-dev/runs/kiln-gate-jobs-2026-11-17/dressing-rule-and-jobs.patch; the cherry-pick refused to a helper): gate lane-zips like any lane.
3. n16-7: fresh review of the knees note; decide under RULINGS 7 Nov whether it is a new try (separate cause from the stopped pelvis method) or listed. Then the look by eye and the packaged film.
4. n16-3: people 0 to 40 at N=10 packaged (nothing beside it).
5. n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5. DAILY by 19:00 (production/research/token-audit/DAILY-2026-11-17.md).
6. n16-8 when an editor run is allowed: head and scalp into F:/LedgerTools/game-inputs/loomwright-darren/, round 5 at 60 roots/cm2.
7. Recipe map (https://claude.ai/artifact/PDhLE6yEQKYuHWbzy7Y3pH): add today's four notebook entries.

## Tonight's machine-free queue (start before 01:15)
1. n16-5 roof runs R1-R4 checks as script inputs (slate-roofs skill). 2. n16-3 people ladder script at N=10. 3. M5 step 2 code (skin from Ron's full body) per the method note. 4. Reviews of the evening's work. If the current order waits on the machine: the next order's waiting list (advisor 192).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: in production/orders/2026-11-16.md section 3 (13 items) and git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick new method try 1 passed film (in the game); Kiln speed 2 of 2 (kept on lane, off); hair capture fault 4 (fixed); CMU route try 1 at step 3 of 5. 17 Nov 04:52 on: CMU measure reader 2 of 2 (the clips were wrong, not the reader); CMU source root scale 1 of 2 (fixed); CMU feet 2 of 2 (set aside, try 1 kept); Kiln collar ring 1 of 2 in flight; hair round 5 is a fixer round within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$14.04 from 23:32 to 00:03.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
