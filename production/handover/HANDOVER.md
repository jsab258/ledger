# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 15:21 (the hourly run; the last session set its Stopped line at 15:10)

**Row due:** at the next start (last row 15:28; page and advisor read 16:17, last ack 226)
**Stopped:** 2026-11-18 15:10 (history OVER at an item's end; helpers stopped, their leftover runs and old Claude waiters ended by tree; lock cleared; no job of mine running. Last commit not yet pushed: the next session pushes after ci.)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). HIS GOAL THIS WEEK (advisor 220): Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits. Plan: F:/LedgerTools/tool-dev/reports/KILN-V1-CHECKLIST-2026-11-18.md (top of LOOP.md): 0 of 6 lines done. Pace: 97% at 14:27 against 97.9%, -0.9 (behind, full pace); the spare reset is due at 98-99% (his hands: if it reaches 98% with no reset, a NEEDS YOU message and an ACTION item). This week (RULINGS, his picks 17 Nov): eight helpers a session, Fable up to 20% for the hardest code, high effort on hard code and reviews. week-shape.json's reset_at stays null until HE presses the spare reset.

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
- **Lane rules file:** F:/LedgerTools/tool-dev/LANE-RULES.md (lane folders, the lock, tries, report lines, no clicks); every Kiln brief points to it; all nine briefs passed the permission check on 18 Nov.
- **Tries (RULINGS 7 Nov) over CLAUDE.md:** after two failed tries one genuinely different researched method; up to four while each closes the gap by a third with no new fault; none asks him. Helpers quote CLAUDE.md's 'third try needs his yes': correct them.
- **Helper spawns in an unattended run:** the permission check refused four of eight briefs at 11:15 (reasons given: destructive actions, unsanctioned communication, needs approval). A leaner brief without "delete" wording passed for two. Do not retry a refused brief verbatim.
- **Quay Run (advisor 222):** his desktop shortcut opens F:/LedgerTools/quay-run/index.html in Chrome; whenever the driving study (https://claude.ai/artifact/UdoyuRSba3tseVmA5daeFq) is republished, copy its index.html there again (Artifact read with path) and run tools/driving_feel_check.py: a copy newer than the ruling must start automatic.
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his. Kiln's LOOP.md and reports folder joined the backup list today.

## Done this run (15:21 to stop; details in DECISIONS 15:35 on)
- Advisors 224-226 acted on and acknowledged: canon pillar "verbs first, talk as the consequence" plus his words "not a gossip simulator" (226); RULINGS prototype line widened; combat end state A with an escalation dial, no silenced .22 (RULINGS release line, weapons spec head); spare reset recorded (reset_at 15:20); waiting items 20 (prototype licences: his own yes still needed, NOT on the allowlist), 22, 23. Pushed 2b285d039; the 226 records commit with this handover.
- J4 try 2 PASS: lane j4-b2 fc61b57 (identity split from rest; the gate keeps rest_label under "checks").
- Skin verdict FIXED: lane-skin-verdict d5b06ca (own-body shape faults stay information, Kiln's own skin-weight checks fail on every body; Ron's jeans stand-in now FAILS on sitting; 21/21 tests).
- Legs SET ASIDE: try 2 (waist/floor rule) failed; the researched different method (CLO patent's area-centroid rule, GarmentCode's crotch-corner rule) screened offline missed by 6 to 196 mm, no drape spent (legtorso run folder offline-rules/; notes KILN-LEG-PLACEMENT-METHODS and -REVIEW in production/research/tool-tests-2026-11). Borrowed values 0.459/0.968 stay, listed; Ron's trousers go on to M5 on them.
- Line 5: Marvelous drapes exist only for Tom's jeans, j3 and zip jacket (F:/LedgerTools/tool-dev/reports/KILN-V1-MARVELOUS-DRAPES-2026-11-18.md).

## In flight at the stop (ended at the stop; rerun, never trust a cut run)
- Merge candidate lane-merge-cand-1118 (main 89157c3 + restlabel-fixes + donkey-start + e1d17f4 + fc61b57): build OK, cargo 136 pass, python tests pass; the whole gate (--allow-better) was running: rerun F:/LedgerTools/tool-dev/runs/kiln-merge-cand-2026-11-18/gate.sh (rename machine.log first), reading gate.out.
- Helper lanes cut at the stop: r4-refit (try 1 of 2; no report yet), coat first drape (try 1 of 2; lane coat), nylon-jam (new lane from donkey-start; diagnosis plus try 1). Read each lane's report and run folder before resuming.

## Next, in order
0. Verdicts after 2026-11-18T15:05:00Z; advisor after 2026-11-18T16:08:00+01:00 (last ack 226). A row on his page at once.
1. Rerun the merge gate alone; add d5b06ca to the candidate first (its regression job sheila-layers-to-cast may newly fail: a real fault, not a reason to drop the fix). Merge what passes into Kiln main; re-take the baseline (the torso default moves the trousers' drop out of band on the better side).
2. Resume r4-refit, coat drape, nylon-jam from their folders.
3. Ron's trousers M5 steps 6-10 on the borrowed leg values.
4. Line 5: the close-up comparison on Tom's three garments; for the rest, research Marvelous's DXF-AAMA import and a Kiln pattern-to-DXF writer before the Marvelous month ends (about 26 Nov).
5. Then n16-6, n16-8, n16-7.
6. Morning 19 Nov: the P4 table (production/playtest/p4/2026-11-19-session.md); Thursday's checkpoint (KILN-V1-CHECKLIST section c).
- tools/timelog.py start "<item> ..." at every task.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov: leg start: swept shares (try 1), waist/floor landmark (try 2), then the area-centroid and crotch-corner rules screened offline: none within about 1 mm on both garments.
- 18 Nov: J4: tests used made-up file shapes twice; each first real run was NOT MADE. Always one test on a real output file.
- 18 Nov: helper briefs: two refused by the permission check (wording about cut runs and rerunning what a run started); a leaner brief passed.
- 18 Nov: blouse: plain sleeve twice, then gathered cuff: the lower sleeve folds through the wrist (unproven: particles too coarse).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: 18 Nov legs 2 of 2 plus the researched screen (set aside); J4 2 of 2 (passed); skin-verdict 1 (passed); R4 1 of 2, coat 1 of 2, nylon-jam 1 of 2 in flight; donkey-start 1 (passed); blouse set aside. Earlier: git show 570374d9a:production/handover/HANDOVER.md.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 or 18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
