# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-18 08:36 (the hourly run; the last session set its Stopped line at 08:23)

**Row due:** 2026-11-18 10:31 (last 09:31; page and advisor read 09:20, nothing new; last ack the 08:10 watchdog, 08:38)
**Stopped:** 2026-11-18 09:30 (history at 234k of 250k at an item's end, too close to start the next machine item. Kiln main 3869f3e, all 58 values replaced; no helper or job running.)
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 16 November (production/orders/2026-11-16.md, adopted 15 Nov 21:08; runs to 13:00 Monday 23 November). The doubled line, full pace: 65% at 04:25 against 78%, 13 behind. His 17 Nov 22:12 direction (advisor 213): Kiln's share aims at 60% of spend from this morning (25.5% at 04:25). This week (RULINGS, his picks 17 Nov): eight helpers a session, a machine-free lane session, Fable up to 20% for the hardest code (3.3% today), high effort on hard code and reviews. week-shape.json's reset_at stays null until HE presses the spare reset.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate (advisor 195), F:'s free room and the next 12 h's need (advisor 189), what fills each helper place (advisor 198).
- **Every time stamp from Get-Date at the moment of writing**.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page: read the live page and items.json first (out_dir to the scratchpad), diff, then publish.
- **His hands only when nothing else can (advisors 203, 204, RULINGS 17 Nov):** an ACTION item needs only_you (sign-in, purchase, licence, taste, his-setting) and a one-line tried; needs_you_page.py refuses it otherwise. Look for a route through what already runs first.
- **Every standing ruling names its enforcer (advisor 205):** a new or changed RULINGS line gets its entry in production/rulings-enforcers.json the same day (file::message, an advisor check, or monday-audit); the pre-commit hook runs tools/rulings_check.py when RULINGS or the list changes; the start gate prints its line.
- **Kiln (RULINGS 13 and 14 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone from M5; M7 count in every round report (0 so far). Kiln's share now measurable: `python tools/token_measures.py --kiln-share`.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads; they live only in F:/LedgerTools/tool-dev/judge/heldback (hash-locked).
- **A Kiln gate runs alone (memory kiln-gate-needs-quiet-machine):** no builds, drapes or bench runs beside it, and do not edit tools/retention.py while one runs (its space check calls the script: an edit mid-gate stopped gate-r3).
- **Advisor 189-192:** `python tools/retention.py space` before every Kiln round, film, build, capture and in every helper brief; each round deletes its own bulky outputs once its numbers are reported; target 1.4 points an hour; free helper places take the next order's machine-free work, recorded in the order ledger.
- **Storage and backup (advisors 196-198, 203):** every folder has a shelf in production/storage-map.json; writes and deletes only through retention.py and the map; nothing of his. The backup now starts from tools/fresh_gate.py when the last good one is over 20 h old (outside 01:15-04:30, never beside Unreal or a Kiln gate, 3 h lock file production/handover/backup-start.lock); the post-commit hook is the second chance; `backup-to-dropbox.py --stale` the 26 h alert. No Windows task, no Dropbox online-only (C: 50 GB, floor 40; if tight, free our own C: space first through the map).
- **His page items (advisors 199, 200):** tagged ACTION, DECISION or REVIEW; title, at most two why bullets, numbered steps; places named as he sees them; after Done, check it happened and say so in the row.
- **Before writing Stopped: end every background job of your own.**

## Done this run (08:36 on; details in DECISIONS 08:44 on)
- Advisor 218 done: RULINGS (Kiln's share as the week's order sets, 70% this week; three proofs before props/vehicles/buildings modules; monthly cold skill re-run; six line-up frames), condensed to 4,900; fight lab test in PLAN.md phase 3; enforcers updated. Kiln's share counted per step by order item (token_audit.is_kiln, KILN_ITEMS n16-1 and n09-6; untimed steps by what they touch): 64.2% since Monday (old 22.8%); week-shape.json kiln_share 70. Pushed 470b96b74 (ci 105/105).
- Lane branch lane-2026-11 merged into wip (its own folders only). timelog.py start now writes "item" and production/current-item.json (gitignored). Wiring item_tags' SessionStart and Agent hooks into .claude/settings.json was REFUSED by the unattended safety check: not worked round; needs Jafar at the PC (an ACTION item only if nothing else can: he can paste the two hooks from production/lane/ITEM-TAGS-MERGE-NOTE-2026-11-18.md step 2).
- Row 28 second reading: PASS WITH FIXES (tests only). Fixes written, NOT BUILT: Kiln branch lane-position-tests de5bc5e (worktree C:/LedgerTools/kiln-lanes/position-tests); swap_body.py/shrink_body.py comment edits on wip.
- Rest label checked on the baseline's real lines: says nothing yet (all "moving"; leftover share unit doubtful; donkey jacket no window): KILN-REST-LABEL-REAL-LINES-2026-11-18.md, three fixes listed.
- C: freed 4.3 GB (merged lanes rewrite, window, public, position and two build folders): C: 44.9 GB.

## Running
- Nothing. Kiln main 3869f3e: row 27 (Z step stays 2 mm, Kiln's own sweep) and row 28's test fixes merged 09:30; engine tests 121; Python 136 with one failure already on 424695a (test_regression_gate, link_cap_solves): look at it. All 58 decompiled values replaced. His licence item updated 09:29 (facts; "not yet, briefly").

## Next, in order
00. NOT PUSHED: the last commit is local only. ci fails attribution: the lane's prototype bundle (tools/lane/prototype/src/bundle/part-01.js, part-02.js) is a copy of three.js (third-party, MIT: check the allowlist and SHIPPED-LIBRARIES-LICENCES-2026-11-18.md), with no attribution entry; .js is deliberately not classed not-asset. Add its THIRD-PARTY.md/attribution entry (or class .js with a rule naming the bundle), run ci to failed=none, push wip.
0. Verdicts after 2026-11-18T08:20:00Z; advisor after 2026-11-18T08:20:00+01:00.
1. Licence item's remaining two (outside the 58): the start values read from the installed program's data files (time step, air damping, substeps, ground, self-collision stiffness, thread presets) and the leg/torso arrangement fits made against Marvelous's drapes: re-source to physics, Kiln's own measurement or LEDGER's references, one lane each, gate alone; then the item back to him with "yes" recommended. Also check Kiln no longer serves the ~22 names absent from the public docs.
2. Step 4: public names lane, gate alone, merge, writer edits. Step 5: KILN_STRAIN_LAST=1 gate. Step 6: R4, J4, B2. Cantilever convergence check.
3. After Kiln (advisor 218): P4, a thirty-minute played session: route_walk/nightly_walk have no thirty-minute mode yet; write it as a bounded task (stand-in talk, minute-by-minute log as 3-PROOFS.md P4) and run it in a night walk before the corner is copied. Hair fallback only if this week's verdict fails.
4. Gap 2 (nylon wrist) stays set aside. On his licence answer: trousers path as before (handover 08:23 step 8), then n16-6, n16-8, n16-7.
- Use tools/timelog.py start "<item> ..." at every task; the time log had no line from 17 Nov 14:30 to 08:58 today.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 18 Nov: Kiln gap 2 (nylon right wrist): two tries and the S6 fit route failed; the cuff is too short for the forearm it lands on (details in TRIED-ARCHIVE.md, 18 Nov).

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3 (items 2, 3 and 4 have targets now).
- Tries used: 18 Nov Kiln row 27: 1 of 2 (passed, 2 mm kept). As in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus git show 8e4584953:production/handover/HANDOVER.md; 18 Nov: Kiln gap 2 (nylon sleeve) 2 of 2 used, both failed; the third route (S6 fit) running; 17 Nov: Kiln convergence 2 of 2 (passed); bending 1 of 2 (try 2 not yet run); cantilever bench 1 (passed as a bench); double precision 2 of 2 (try 2 passed, merged); retention step 2: 3 tries (the third under RULINGS 7 Nov, closing the gap; a fourth only if it closes a third of what is left with no new fault); hair round 5b within the 8 h cap.
- API spend: US$1.15 (8 Nov) plus US$2.62 (16 Nov); none 17 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help (or with no arguments when its docstring shows required ones); let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools.
