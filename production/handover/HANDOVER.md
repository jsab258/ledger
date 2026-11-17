# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 10:07 (the hourly run; the last session set its Stopped line at 09:52)

**Row due:** 2026-11-17 11:11 (last 10:11; page and advisor read 10:09)
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
- git show 47cfaec10:production/handover/HANDOVER.md (06:22 to 09:52), 4b16a336e, d74c1862d, 5606f2805.

## Done this run (10:07 to the stop)
- Advisor 193 (his pick about 10:00): Kiln about 70% of the week; acked, DECISIONS, order ledger. Review step 3 had already landed (Kiln aab3778). Step 4 cap 32 h (failed-capability report if not landed Thu 19 Nov); step 5's layered-job worst edge recorded as a known shortfall. Engine-count tuning in the jacket/trouser lanes STOPPED (lane-jackets parked until step 4 lands). n16-5 S2 and the rest of n16-3 WAIT.
- n16-7 knees: fresh review (production/research/n16-7-knees-review-2026-11-17.md): same fault as the stopped pelvis method; set aside, listed, NOTEBOOK entry; no further try.
- Recipe map: D3 and D5 rows updated for 17 Nov.
- Committed and pushed 3c3d8e671 (wip): M5 step 2 (tools/md/skin_transfer.py, jeans match Blender's weights, worst 0.033); Kiln disk bounded (retention rows; production/research/disk/KILN-DISK-2026-11-17.md: Kiln 15.5 GB, 2.4 on F:, so F:'s squeeze is the gate-picture clear-out); held-back patterns made (judge/heldback/patterns, HB-1 9 pieces, HB-2 12; start check passes; re-hashed; reference_drape PENDING).
- Kiln main c16be30: collar-plane lane merged on a passing gate (only false collar flags go). Fabric numbers: thin (two wools only), a sanity band; the re-tune leans on Tom's references.
- Helpers running at the stop (check their files): step 4 stiffness lane (report KILN-STEP4-STIFFNESS-2026-11-17.md); zips lane gate (verdict appended to KILN-ZIPS-2026-11-17.md; md-bridge writers on wip uncommitted: commit after a PASS); held-back first judge run on main (judge/heldback/RESULTS-2026-11-17-main.md; counts only, HB-1/HB-2); M5 step 3 code (tools/md, uncommitted); re-tune plan (production/research/tool-tests-2026-11/KILN-RETUNE-PLAN-2026-11-17.md).

## Next, in order
0. FIRST: verdicts after 2026-11-17T09:45:00Z; advisor after 2026-11-17T10:10:00+01:00 (last ack 10:33, pace). Row due 11:11.
1. Read each helper's verdict as it lands; merge only on a passing gate; commit md-bridge writers and M5 step 2 code with their evidence; NOTEBOOK lines per finished unit.
2. Kiln step 4: after the code lands, re-tune presets against Tom's references using the fabric numbers (12-20 h), then re-judge M2-M4; the speed lane's card port re-checked on the new engine before switching on. Held-back jobs run once patterns exist (judge only; no fixer sees them).
3. M5 step 3 for Ron's trousers after step 2 (a real Kiln drape, bend_back, skin, film held for his page).
4. n16-7: the look by eye and the packaged film with the hip-joint default (knees listed).
5. n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 (small slot). DAILY by 19:00 (production/research/token-audit/DAILY-2026-11-17.md).
6. n16-8 when an editor run is allowed: head and scalp into F:/LedgerTools/game-inputs/loomwright-darren/, round 5 at 60 roots/cm2.
7. Waiting by his pick: n16-5 S2 (notes in git show 47cfaec10:production/handover/HANDOVER.md, item 1, incl. the editor brick path fault) and n16-3's people ladder; S1 pictures go to his batched rough-street page with S2.

## Tonight's machine-free queue (start before 01:15)
1. Kiln step 4 preset re-tune prep and held-back judge runs (processor, outside Unreal's runs). 2. M5 step 3 code. 3. Reviews of the evening's work. If the current order waits on the machine: the next order's waiting list (advisor 192).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2; the rewrite is the genuinely different method under his pick A).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: in production/orders/2026-11-16.md section 3 (13 items) and git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left); retarget pelvis 2 of 2 (fixed); breadth start check 2 of 2 (set aside, listed); collar placement 1 of 2 (kept); slide-down at 10 mm 2 of 2 (in flight); Darren's arm line 0 of 2; packing step 2 1 of 2 (passed editor review); brick new method try 1 passed film (in the game); Kiln speed 2 of 2 (kept on lane, off); hair capture fault 4 (fixed); CMU route try 1 at step 3 of 5. 17 Nov 04:52 on: CMU measure reader 2 of 2 (the clips were wrong, not the reader); CMU source root scale 1 of 2 (fixed); CMU feet 2 of 2 (set aside, try 1 kept); Kiln collar ring 1 of 2 in flight; hair round 5 is a fixer round within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov). Model spend US$14.04 from 23:32 to 00:03.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture (both load the processor).
