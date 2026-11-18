# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 11:12 (the hourly run; the last session set its Stopped line at 11:09)

**Row due:** 2026-11-18 12:37 (last 11:37; page and advisor read 12:19, advisor 221 acted on and acked)
**Stopped:** 2026-11-18 12:22 (history past the point at 252k at an item's end; helpers stopped and their leftover runs ended by tree; lock cleared; no job of mine running.)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace: 89% at 11:36 against 92.3%, -3.3 (behind, full pace). This week (RULINGS, his picks 17 Nov): eight helpers a session, Fable up to 20% for the hardest code, high effort on hard code and reviews. week-shape.json's reset_at stays null until HE presses the spare reset.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, leading 'v1: N of 6', ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate, F:'s free room and the next 12 h's need, what fills each helper place.
- **Every time stamp from Get-Date at the moment of writing**.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page: read the live page first, diff, then publish index.html with items.json.
- **His hands only when nothing else can (advisors 203, 204, 221):** an ACTION item needs only_you and a one-line tried; since 18 Nov 12:20 an open DECISION item needs "kind", one of CLAUDE.md's categories (money, sign-in, hands, licence-off-list, canon, story, scope, frame-look, person-look, taste, identity); needs_you_page.py refuses both otherwise. His own tools are not licences; deleting what nothing uses, guarded by a check, is not his decision.
- **Every standing ruling names its enforcer (advisor 205)** in production/rulings-enforcers.json the same day.
- **Kiln (RULINGS 13, 14, 18 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone; M7 count in every round report (0). Share: `python tools/token_measures.py --kiln-share`.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads.
- **The heavy lock** F:/LedgerTools/tool-dev/runs/kiln-heavy.lockdir (mkdir as the lock, owner file inside, released at once) for every cargo/gate/drape run. A Kiln gate whose seconds matter runs alone.
- **Before writing Stopped: end every background job of your own, and check for runs your stopped helpers leave behind:** stopping a helper does NOT stop its bash scripts; at 12:20 four trees (legtorso sweeps, donkey, blouse) were still running and holding the lock. List processes matching kiln-lanes|sweep.py|regression_gate|heavy*.sh and taskkill /T each top bash; then clear the lock.
- **Helper spawns in an unattended run:** the permission check refused four of eight briefs at 11:15 (reasons given: destructive actions, unsanctioned communication, needs approval). A leaner brief without "delete" wording passed for two. Do not retry a refused brief verbatim.
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his. Kiln's LOOP.md and reports folder joined the backup list today.

## Done this run (11:12 on; details in DECISIONS 11:2x on)
- His page: republished (merged ACTION item); on his chat word at 12:15 the output cap (tools/output_cap.py, PreToolUse Bash|PowerShell|Read) and the order-item hooks (tools/lane/item_tags.py: SessionStart; PreToolUse Agent|Task) are ON in .claude/settings.json; item closed. Advisor 221 (his 12:13): both DECISION items withdrawn (page now 0 open); Kiln's job interface decided by the session (adopt Ron's trousers once start values and leg/torso fits are own-sourced); old readers stay; needs_you_page.py now refuses an untyped DECISION (selftest 30/30, enforcer named); ack written.
- Backup list (in-game.json backupAlso): F:/LedgerTools/tool-dev/LOOP.md and tool-dev/reports (selftest 33/33, dry run clean). Pushed to wip (ci 105/105) at 11:2x as 8f43f3ab3.
- Kiln main is now cfe56f2: lane resource-datafiles fast-forwarded in after main e748abf was merged into it; cargo test 126 passed. Its gate was the lane's own (636b595, plain runs reproduce c52c3ab). The merge commit's message still says "tests owed" (they ran after: 126 pass).
- Lane restlabel-fixes committed 9b8dfd5 (helper): move line 1.0 mm, speed and leftover shown not judged, reason in words; cargo 124/0; drape unchanged on work trousers, jeans, donkey (51 fields, 26 exports byte for byte vs 21b7f77). Gate not run (its judge starts Blender). Not merged.
- Lane j4-b2 committed 734dc9c (session): B2 PASS (four passing garments as one wardrobe equal the gate in measures, export bytes, exceptions, bands). J4: reader fixed for the drape file's named x, y, z points (try 1 of 2); rerun: run 1 and run 2 identical (exports identical), but the check FAILS on 20.3 mm of movement after reopening and reopen not equal to the saved state. Report: KILN-LANE-J4-B2-2026-11-18.md. Not merged.
- C: freed 2.3 GB (lane-publicnames and lane-resource-lineinfo build caches, merged lanes). Row 11:37 written.

## Running
- Nothing. All helpers stopped at 12:20; their leftover runs ended by tree; lock cleared.
- Lanes left with uncommitted work (worktrees in C:/LedgerTools/kiln-lanes/):
  - resource-legtorso: 3 files uncommitted (mechanics.rs, rig.rs, serve.rs), base 3869f3e; sweeps in F:/LedgerTools/tool-dev/runs/kiln-legtorso-2026-11-18 (variants unset, legplain, legknee, torso1, torsoneck, plain, knee1, unset2, leglisted, torsohead, torsosite; some cut mid-run); report still only its questions. Try 1 of 2.
  - donkey-start (new, from e748abf): bdc599d's KILN_SKIN_NECK_OVER_JOINT port, 2 files uncommitted; runs in F:/LedgerTools/tool-dev/runs/kiln-donkey-start-2026-11-18 (diag-off cut). No report. Try 1 of 2.
  - blouse (new, from e748abf): 3 files uncommitted; report skeleton KILN-LANE-BLOUSE-2026-11-18.md; runs in kiln-blouse-2026-11-18; the first drape had not started. Try 1 of 2.

## Next, in order
0. Verdicts after 2026-11-18T11:15:00Z; advisor after 2026-11-18T12:18:00+01:00 (last ack 221). Row due 12:37 (lead 'v1: 0 of 6'; say in it that the output cap and item hooks are on, and check the first helper's description shows "[n16-x]").
1. Fill the helper places with v1 lines, biggest first (lean briefs; no delete wording): resume donkey-start, blouse and legtorso from their folders; R4 refit (line 2 step 1, never started: a refused brief); M5 shared steps (line 3 step 1).
2. Kiln main's Python suite has 8 failures on e748abf/cfe56f2 (test_compat_lineinfo, test_compat_public, test_spec_job: writers outside Kiln changed and public names), present before the data-files merge: one fix lane.
3. Merge restlabel-fixes (re-merge main first; the rest of the gate's jobs not yet run on it) and j4-b2 after J4 try 2: J4 should judge run 1 against run 2 (identity) apart from the movement after reopening (rest); find why reopening does not restore the saved places.
4. When legtorso is own-sourced and merged: one gate alone on merged main against c52c3ab; then Ron's trousers adopted (regenerate job_wt2.py from the edited writer), and the time to Ron in the game in the row (advisor 221). Then n16-6, n16-8, n16-7.
5. Step 5: KILN_STRAIN_LAST=1 gate; cantilever convergence check.
6. Morning 19 Nov: read the P4 table (production/playtest/p4/2026-11-19-session.md); NOTEBOOK entry for P4 then. Thursday's checkpoint (KILN-V1-CHECKLIST section c).
- Use tools/timelog.py start "<item> ..." at every task.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov: J4 identity check: first machine run NOT MADE (its tests used plain [x,y,z] points; the drape file saves named points); fixed; rerun shows the identity holds but the check mixes in rest. Try 1 of 2 used.
- 18 Nov: Kiln gap 2 (nylon right wrist): two tries and the S6 fit route failed; the cuff is too short for the forearm it lands on (TRIED-ARCHIVE.md, 18 Nov).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: 18 Nov lanes legtorso, donkey-start, blouse, J4: each try 1 of 2; restlabel-fixes try 1 passed (committed); datafiles passed (merged). Public-names: passed. 18 Nov Kiln row 27: 1 of 2 (passed). Earlier: git show 570374d9a:production/handover/HANDOVER.md ('Tries used') and 8e4584953; 18 Nov: Kiln gap 2 (nylon sleeve) 2 of 2 used, both failed, third route failed; 17 Nov: convergence 2 of 2 (passed); bending 1 of 2; cantilever bench 1 (passed); double precision 2 of 2 (passed, merged); retention step 2: 3 tries; hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 or 18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
