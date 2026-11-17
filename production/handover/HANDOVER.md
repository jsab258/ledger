# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-17 12:52 (the hourly run; the last session set its Stopped line at 12:39)

**Row due:** 2026-11-17 14:54 (last 13:54; page and advisor read 13:44; last ack 13:38, advisor 198)
**Stopped:** 2026-11-17 14:03 (history near its limit at an item's end; no helper or background job running)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted by his tap 15 Nov 21:08; runs to 13:00 Monday 23 November). The doubled line runs from 0 at Monday 13:00 to 95% by Wednesday 15:00, six helpers, full pace (34% at 13:26, about 12.5 behind). week-shape.json's reset_at stays null until HE presses the spare reset.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate (advisor 195), F:'s free room and the next 12 h's need (advisor 189), what fills each helper place (advisor 198).
- **Every time stamp from Get-Date at the moment of writing**.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page or the progress page: read the live page and each published file first (out_dir to the scratchpad), diff, then publish.
- **Kiln (RULINGS 13 and 14 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone from M5; M7 count in every round report (0 so far). Time log "tool loop: <tool> round n". Advisor 182 trial: Kiln rounds and judging run in helpers that hand back a short verdict only.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked).
- **Advisor 189-192:** `python tools/retention.py space` before every Kiln round, film, build, capture and in every helper brief; each round deletes its own bulky outputs once its numbers are reported; no new drives; target 1.4 points an hour; when the current order waits on the machine, free helper places take the next order's machine-free work, recorded in the order ledger.
- **Advisor 194:** any ask needing his hands, allowance or sign-in goes on the page the same hour.
- **Advisors 196-198 (storage and backup, his picks 12:43 and 12:58):** RULINGS 17 Nov line replaced 2 Oct's: every folder has a shelf in production/storage-map.json; writes and deletes only through retention.py and the map; nothing of his on it; mh-dress is lasting. Backup: the lasting shelf to Dropbox nightly about 05:00, never deletes or overwrites, never keys, Kiln to Dropbox only (bundle), 26 h staleness item, weekly restore check, FLOOR 40 GB on C:.
- **Before writing Stopped: end every background job of your own** (fresh_gate.py holds starts up to 120 min while any session's background command still runs).

## Done this run (12:52 to the stop)
- Advisor 196 storage: two read-only helpers inventoried F: and C: (production/research/disk/INVENTORY-2026-11-17.md, -F-, -C-); production/storage-map.json made (81 folders; shelves F: lasting 51, tools 20, working 25, spare 4, floor 20, so the lasting cast fits); retention.py gained `unmapped` and `shelves` (read only; selftest passes); the 53 small folders the inventory missed classified and added (134 folders, `unmapped` now 0; 17 tiny old scratch folders proposed remove, for step 2). Remove list on his page (storage-remove-list-2026-11-17: Parler 8.8 GB, OpenSLR 83 3.8, study extracts 1.8). Side sessions' checkouts on C: (ledger-talk, -lab, -exec) mapped "side-session", never touched.
- Advisor 197 backup: backup-to-dropbox.py now takes Kiln (source minus target/out/.git, plus a nightly git bundle on F:/LedgerTools/backup-staging), game-inputs, the judge folder, Tom L1 (source and built); refuses the keys folder and .env; FLOOR_GB 40; `--stale`, `--restore-check`, `--log`. First run 13:09: 4.3 GB copied, all whole; restore check 20 of 20. production/RESTORE.md written. Registering the 05:00 Windows task was REFUSED by the app's safety check: tools/register_backup_task.ps1 written, item backup-schedule-at-pc-2026-11-17 on his page (he types "Register the backup schedule now" in the session and clicks Allow; then run the script).
- Advisor 198: (2) a SHA-256 manifest (F:/LedgerTools/backup-staging/manifest.json) so runs compare with it instead of reading the backup's copies (seeded: 10,145 files; committed after the hostile review: production/audits/backup-review-2026-11-17.md, 13 findings, the 8 high and medium fixed with self-tests (32 of 32), the real backup VERIFIED whole; 5 low ones listed in the audit's Outcome for the next backup item; the restore check's floor fixed since, uncommitted until this stop's commit). Dropbox online-only research: production/research/disk/DROPBOX-ONLINE-ONLY-2026-11-17.md: only the Explorer right-click is documented; reading hydrates; whether stat hydrates and whether `attrib +U` works on Dropbox are unverified, so a measured test on a small test folder comes next before anything goes on his page.
- n16-8: Darren's head and scalp remade from MH_SamS6's face (F:/LedgerTools/game-inputs/loomwright-darren/, darren_scalp.py kept; scalp 652 cm2, ears out); round 5b at 60/cm2 (45,616 strands); drawn warm in Unreal: crown covered, soft hairline and sideburns, front still thin; previews loomwright-hair-r5b-darren-side/-front-2026-11-17.jpg. About 4.5 h of the 8 h cap used.
- Next order's machine-free work (advisor 192): targets for the fishmonger and the empty unit (production/research/phase2-plan/TARGET-*-2026-11-17.md; empty unit 1,367 words), noted in the order's waiting list item 2.

## At the stop (no helper running; none named a held-back job)
- Kiln zips round 2 STOPPED at a safe point for this handover (nothing committed): main 9ca019e built (C:/LedgerTools/kiln-runs/zips-r2-2026-11-17/exe/drape-studio-main-9ca019e.exe); base and n+1 runs done (jeans base drop 100.4, as the controls); n-1 NOT run (about 27 min); main's regression_jobs.json has the six source-line edit, uncommitted. Next commands in KILN-ZIPS-2026-11-17.md's 'Round 2' section: n-1, then baseline --commit 9ca019e, then the lane steps (discard the lane's identical jobs edit, rebase, flag true, tests, gate, merge on PASS). Provisional jeans bands much wider than the old (worst 0.386 vs 0.266).
- Kiln convergence try 1 of 2 DONE (lane-convergence ce7d7f7, not merged): 5 substeps at every quality under KILN_XPBD (Macklin 2019): 10 of 13 presets inside 10% Normal vs Fitting (1 before); outside: Stiff Interlining 15.6%, sheila_skirt_band 11.8%, darren_nylon 20.5% (Fitting itself unconverged); Normal hang runs 5x slower; 43 of 43 tests. Try 2 needs the session's pick (report section 'Convergence try 1'): (a) Normal takes Fitting's 8 passes under the switch, (b) judge the rule at Fitting only, (c) a faster solver. Not yet run: 10 mm, cantilever, Cusick, the gate, garment run times.

## Next, in order
0. FIRST: verdicts after 2026-11-17T12:44:00Z; advisor after the last ack (13:38, advisor 198). Row due 13:55.
1. Finish zips round 2 from its report's commands (a helper, diagnoser). Then the backup review's five low findings (audit's Outcome).
2. Dropbox online-only: a measured test on a 3-file test folder inside "LEDGER backup" (attrib +U; does os.stat or the manifest run hydrate; is the file still listed and restorable); safe: make the backup online-only that way; else his page with the numbers (advisor 197/198).
3. retention.py step 2 (tomorrow, advisor 196): expiry rules from the map (working 3 days or once numbers are recorded; tools 14 days unused if refetchable), fixture tests, a hostile fresh reviewer; then carry out the remove list on his yes.
4. Kiln re-tune per the benches' order: convergence (try 2: pick a/b/c from the report by its method review, then gate the lane), bending-link scaling, cantilever redesign, then denim on jeans. Cap 32 h; failed-capability report if switch-on is not inside the bands by Thu 19 Nov.
5. n16-8: Tom's crown (export his head, cut his scalp the same way, grow, draw warm); the verdict rides with the people looks.
6. n16-7 look and packaged film (knees listed); n16-6 packaged run with LEDGER_TALK_CORE_MODEL=claude-sonnet-5-5 (never during a Kiln gate run: the gate refuses while LedgerProbe or UnrealEditor runs). DAILY by 19:00 (production/research/token-audit/DAILY-2026-11-17.md).
7. M5 chain for Ron's trousers: the helper was refused twice by the app's permission check; not again without a new way.
8. Waiting by his pick: n16-5 S2 and n16-3's people ladder (git show 47cfaec10:production/handover/HANDOVER.md, item 1).

## Tonight's machine-free queue (start before 01:15)
1. Kiln re-tune code and held-back judge runs (processor, outside Unreal's runs). 2. retention.py step 2 code and tests. 3. Reviews of the evening's work. If the current order waits on the machine: the next order's waiting list (advisor 192).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 17 Nov: registering a Windows scheduled task refused by the app's safety check (once; not retried, on his page).
- Set aside: Vellum on Tom's jumper (3 of 3), Cascadeur test 4; the bridge start by UI Automation (2 of 2).

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (13 items) and git show 55179b917:production/handover/HANDOVER.md ('Kept as they are').
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus those listed in git show 8e4584953:production/handover/HANDOVER.md; 17 Nov afternoon: Kiln convergence 1 of 2 in flight; hair round 5b a round within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus the bake-off's US$2.62 (16 Nov); none today.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; run Kiln drapes during an Unreal perf capture.
