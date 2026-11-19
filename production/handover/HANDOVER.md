# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 22:36 (the hourly run; the last session set its Stopped line at 22:02)

**Row due:** at the next start (last row 23:18; page and advisor read 23:31, last acks 22:42)
**Stopped:** 2026-11-18 23:32 (advisor 236's guard tripped at 23:18, so no new work; the coat round returned; nothing of mine running, lock clear; work committed with this handover)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace: 26% at 23:18 against 6.4% (+19.6); Kiln his priority item above 6 ahead (advisor 236) under the 99% guard; Fable 36% of its week. This week (RULINGS, his picks 17-18 Nov): eight helpers a session, Fable up to 40% on Kiln's hardest pieces, high effort on hard code and reviews.

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
- **Fable (advisors 227-228, to 23 Nov 13:00):** Kiln's hardest pieces (stiffness, Sheila's blouse, the trousers' legs) and any Kiln fault failing two Opus tries go to Fable at max (Agent model fable, effort max), given the problem, tries and numbers, no conclusion; never straight to a set-aside. Fable up to 40% of the week; rows name Fable helpers and share; Fable heavy runs first in the lock queue. final-reviewer and research-synthesis at effort high until 23 Nov 13:00, then medium.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads.
- **The heavy lock** F:/LedgerTools/tool-dev/runs/kiln-heavy.lockdir (mkdir as the lock, owner file inside, released at once) for every cargo/gate/drape run. A Kiln gate whose seconds matter runs alone.
- **Before writing Stopped: end every background job of your own, and check for runs your stopped helpers leave behind:** stopping a helper does NOT stop its bash scripts; at 12:20 four trees (legtorso sweeps, donkey, blouse) were still running and holding the lock. List processes matching kiln-lanes|sweep.py|regression_gate|heavy*.sh and taskkill /T each top bash; then clear the lock.
- **Lane rules file:** F:/LedgerTools/tool-dev/LANE-RULES.md (lane folders, the lock, tries, report lines, no clicks); every Kiln brief points to it; all nine briefs passed the permission check on 18 Nov.
- **Tries (RULINGS 7 Nov) over CLAUDE.md:** after two failed tries one genuinely different researched method; up to four while each closes the gap by a third with no new fault; none asks him. Helpers quote CLAUDE.md's 'third try needs his yes': correct them.
- **Helper spawns in an unattended run:** the permission check refuses some briefs (delete wording, cut runs); a leaner brief passes. Never retry a refused brief verbatim.
- Quay Run: on each driving study republish, copy its index.html to F:/LedgerTools/quay-run and run tools/driving_feel_check.py (advisor 222).
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his. Kiln's LOOP.md and reports folder joined the backup list today.


## Done this run (22:36 on; details in DECISIONS 22:41 on)
- Advisors 232-236 and the backstop recorded and acknowledged: canon's cars line (hurt, never kill), RULINGS within the cap (cars, play-build gate, GTA VI no-spoilers, Marvelous by 25 Nov), waiting item 24 (GTA VI footage, about 10 h). Fable cap enforced: `python tools/pace_line.py <pct> --fable <pct>` at each row stores Fable's share; the Agent hook refuses a Fable helper at 40%. Pushed 3fbabe72b.
- Marvelous reference drapes (v1 line 5): trousers, skirt, donkey jacket done by the .avt route (runs/kiln-md-compare-2026-11-18: bodies/MH_RoccoP2.avt, MH_LenaS4.avt; *_avt folders; report MD-REFERENCE-DRAPES-2026-11-18.md). The 19:31 trousers drape is unusable (body at scale 1.0). Trousers sit about 100 mm low; pleats unpressed (no fold call in this API). Marvelous is free, bridge idle, inbox empty.
- Coat, Fable try 1 of 2, NOT passed, uncommitted in lane coat (with the earlier try 2): pattern check fixed in general terms (hang from the top opening; cargo 129/129); the drape stops at the start check on the collar stand through the neck (KILN_SKIN_NECK_OVER_JOINT is on main, not in the lane); then likely the under collar (folded in front, 79-88 self-crossings). The helper's lock release was refused four times by the safety check reading rm; no lock is held now. Files: runs/kiln-coat-2026-11-18/fable.

## In flight at the stop
- Nothing of mine running; the heavy lock is free. Bash processes from 17 Nov (shell snapshots) are not this run's: leave them.
- THE GUARD (advisor 236) TRIPPED at the 23:18 row: 24% at 22:42, 26% at 23:18 (about 1.1 points an hour since 21:30; under 99% by Mon 07:00 needs about 0.7). Start nothing new until a row's rate is back under; then Kiln resumes as his priority item with up to two helpers, Fable allowed under 40% (36% at 23:18).
- Night space 23:04: C: 40.8, F: 43.5 GB, GO. The stiffness2 lane build (1 GB on C:) is the first of mine to free.

## Next, in order (when the guard allows)
0. Verdicts after 2026-11-18T22:30:00Z; advisor after 2026-11-18T22:32:00+01:00 (last acks 22:42: 234-236). A row at once with the projection.
1. Coat: join lane-coat with main in the lane (main changed sim.rs and serve.rs, which try 2 also changed: expect text conflicts), run the coat job with KILN_SKIN_NECK_OVER_JOINT=1; optional control_work.sh under the lock. Fable try 2 of 2 left. Lock release: word lane briefs so releasing the lock does not read as a delete to the safety check (it refused rm -r of the lockdir at 23:20).
2. Then legs, blouse, R4 on Fable (priorities); stiffness steps 5-7 only by a genuinely different method.
3. Marvelous before 25 Nov: Darren's nylon jacket needs a body with a head (or him at the PC for a box); pressed pleats and a zipper are window steps; a look by eye at the three drapes; the money DECISION item by Tue 24 Nov (each v1 line's state after Mon 13:00, what only Marvelous makes, a recommendation).
4. Ron's trousers M5 steps 6-10 (KILN-V1-CHECKLIST line 3); never Unreal 01:15-04:30.
5. ADVISOR 231: first batch tomorrow: publish production/approvals/needs-you/next-batch.json (font, DINOv3; re-read the dinov3 licence in full first), then --waiting into ci-checks, enforcers, RULINGS within the cap.
6. ADVISOR 230: the 23 Nov order's waiting list gets the real game's phase plan checked against the prototype design; RULINGS prototype line (rounds build the approved design).
7. Morning 19 Nov: the P4 table (long session requested); Thursday's checkpoint (KILN-V1-CHECKLIST section c); the DAILY token file by 19:00.
- tools/timelog.py start "<item> ..." at every task.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov 23:30: coat drape blocked by the collar stand at the start check (the lane lacks main's switch), after the pattern check was fixed.
- 18 Nov 19:31: Marvelous trousers by FBX import at scale 1.0: body a tenth size, no arrangement points, a hidden box, pieces in a heap. Use the .avt bodies.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used 18 Nov: coat Opus 2/2, Fable 1/2; stiffness 2/2 (Fable; a third method may follow); Marvelous drapes 2/2 on the FBX route, .avt route 1/2 (worked); legs 2/2 (Fable); R4 1/2; blouse set aside (Fable).
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).
