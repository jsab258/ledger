# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-23 17:21 (the hourly run)

**Row due:** at the next start (last row 16:28; page read 16:37: no verdicts, no advisor; filter verdicts after 2026-11-23T15:37 UTC, advisor after 2026-11-23T16:15:00+01:00; last ack 332 at 16:30).
**Uncommitted:** nothing beyond what the Stopped line names.
**Stopped:** 2026-11-23 16:43 (the 16:22 run: advisors 331-332 acked; his games ruling recorded; recorder asked on his page; installed-game reprice; catalogue notes read by two helpers; stopped at a clean point near the history limit, 222k of 250k)

(At each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 23 November (production/orders/2026-11-23.md, adopted by his tap 23 Nov 08:12 Swiss; runs to Mon 30 Nov 13:00). The measuring block (n23-1) leads; the normal line 0 to 90% by Mon 30 Nov 07:00 (week-shape.json inactive); `python tools/pace_line.py`.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, leading 'v1: N of 6', ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' and the model (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). "at" is +01:00. Each row: helper count and rate, F:'s free room and the next 12 h's need, what fills each helper place.
- Never end a turn while work remains (the stop hook enforces it); the Stopped line is the last thing written.
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open". Never list collections whole.
- Publishing to his page: read the live page first, diff, then publish index.html with items.json.
- **His hands only when nothing else can (advisors 203, 204, 221):** an ACTION item needs only_you and a one-line tried; since 18 Nov 12:20 an open DECISION item needs "kind", one of CLAUDE.md's categories (money, sign-in, hands, licence-off-list, canon, story, scope, frame-look, person-look, taste, identity); needs_you_page.py refuses both otherwise. His own tools are not licences; deleting what nothing uses, guarded by a check, is not his decision.
- **Every standing ruling names its enforcer (advisor 205)** in production/rulings-enforcers.json the same day.
- **Kiln (RULINGS 13, 14, 18 Nov):** serves LEDGER; every module names the game item it unblocks; 'special cases: none' in each report; held-back jobs at every milestone; M7 count in every round report (0). Share: `python tools/token_measures.py --kiln-share`.
- **Fable (advisors 248, 250):** reset pressed 19 Nov; Fable at max for Kiln's hardest pieces, prototype, simulation, any Kiln fault failing two Opus tries (given problem, tries, numbers, no conclusion); his last reset untouched, never called for. final-reviewer and research-synthesis at effort high until 23 Nov 13:00, then medium.
- **Held-back jobs never reach a fixer:** never name them in any brief, report, row or file a fixer reads.
- **The heavy lock** F:/LedgerTools/tool-dev/runs/kiln-heavy.lockdir (mkdir as the lock, owner file inside, released at once) for every cargo/gate/drape run. A Kiln gate whose seconds matter runs alone.
- **Before writing Stopped: end every background job of your own, and check for runs your stopped helpers leave behind:** stopping a helper does NOT stop its bash scripts; at 12:20 four trees (legtorso sweeps, donkey, blouse) were still running and holding the lock. List processes matching kiln-lanes|sweep.py|regression_gate|heavy*.sh and taskkill /T each top bash; then clear the lock.
- **Lane rules:** F:/LedgerTools/tool-dev/LANE-RULES.md; every Kiln brief points to it.
- **Tries (RULINGS 7 Nov) over CLAUDE.md:** after two failed tries one genuinely different researched method; up to four while each closes the gap by a third with no new fault; none asks him. Helpers quote CLAUDE.md's 'third try needs his yes': correct them.
- **Page read-back, daily (19 Nov):** query verdicts with "at" after the last read-back, out_dir production/approvals/answers/1VZHkCBAHdw8HBdNHrByL8, then `python tools/page_answers.py --index` (ci fails after 2 days).
- **Storage and backup (advisors 196-198, 203):** writes and deletes only through retention.py and the storage map; nothing of his.
- **Measuring block in every row (advisors 292, 295):** read from measurements/STATUS.md (per aspect and game: planned, logged, state, open question); weekly points per measured hour, expected finish (estimate marked). Mafia is never a reference.
- **Progress page (advisor 275):** each refresh reads the live page and publishes only progress.json and changed files; never an old index.html, never plan.json. Helpers only as project types: settings_check flags catch-all helpers (target under 2%).

## Done today
- 13:07-14:40: his tap (08:12) adopted it; its item ledger written, last week's items carried into orders/archive/2026-11-23.md; week-shape.json inactive; progress page with last week's numbers; the budget table (production/research/games-numbers/BUDGET-TABLE-2026-11-23.md, reviewed, fixes applied); his page: the three games can go (item uninstall-three-games-2026-11-23); nightly package and walk weekly, the night after Sunday (production/playtest/nightly/schedule.json, walk_tonight() in tools/nightly_walk.py); api_batch prices pictures by tokens; advisors 320-323 acked; the C: folder list in the 14:00 row.
- 15:22-2026-11-23 15:44: advisors 328-330 acked with the drive reading (C: 205 GB free, RDR2 fits leaving about 85 GB); the uninstall item closed; tools/star_slots.py (n23-2 try 3, fixed slots and a template, from HUD-ICON-READING-NOTES): 47 of 49 on 6wy7gx, about 30 of 36 on 49g1xb, red stars as lit; G5's flag cleared (A, B, C, G are two-star spells; STATUS.md); INSTALLED-METHOD.md written, reviewed (INSTALLED-METHOD-REVIEW), revised; GTA V, GTA IV, KCD2 copies load replaced unsigned files: not run (DECISIONS 15:26); his page asks store copies and scripted keys in Sleeping Dogs. Pushed 4aa0f93e5.
- 16:22-16:43: advisors 331-332 acked; his games ruling in RULINGS and INSTALLED-METHOD.md; game items closed; ffmpeg on the allowlist (item 18), its run refused, asked on his page; installed-game reprice in STATUS.md; catalogue started. Pushed 697d7ae91.

## In flight
- Nothing runs; no helpers. Catalogue notes done: NOTES-A (GTA VI 41 usable rows, RDR2 43, KCD2 24), NOTES-B (GTA V 41, GTA IV 20, Sleeping Dogs 12, Yakuza 12), NOTES-HIS-VIDEO (10); unreached: Reddit, ResetEra, GameFAQs, all YouTube view counts (helpers' WebFetch gets digests only).
- Page tools (lost on reload; rewrite): seekTo(v,t); starscan and starscanT crop x 0.854W-W, y 0-0.083H; fsheetT full frames; canvas at most 6 x 130 px; poll window._r (45 s).

## Next, in order
00. Pace first: `python tools/pace_line.py <week> --fable <fable>` (needs the number). Ceiling now line plus 25 (advisor 330, replaces 325). At 15:23 the week read 20% against 1.3%: under the ceiling, keep measuring.
0. His page: recorder-for-drills-2026-11-23 (his chat yes lets ffmpeg be fetched and run into F:/LedgerTools/tools/ffmpeg; the 9-byte ffmpeg-lgpl.zip there is a failed fetch of the session's own, delete it). With the recorder: KCD2 first (it has saves) per INSTALLED-METHOD.md, then the openings of Sleeping Dogs, GTA V, GTA IV by fixed key scripts (two tries each). Captions: YouTube's transcript panel in the browser pane works (expand the description, Show transcript, read the segments); a script fetch of the caption track was refused, do not retry it.
1. Advisor 324 catalogue (due Thu 26 Nov 18:00): the session reads the top videos' transcripts per game in the browser pane (search YouTube there for 'hidden details' per game; titles, views, dates from the page) to fill Sleeping Dogs, Yakuza and KCD2; then one research-synthesis helper ranks the twenty best for LEDGER into details-catalogue/CATALOGUE.md from the four notes, one fresh reviewer against the sources.
2. n23-2: the ruler check (film our own packaged build with play.py; true walk 160, run 420 cm/s, SliceCharacter.h; measure by the footage method; error per kind of number into STATUS.md). star_slots.py's known misses: grey over bright or white backgrounds, faint grey; empty slots untrusted.
3. n23-1: the reprice (advisor 328's split: drills in installed clean copies vs footage), then the feel rows; every row names its blueprint decision.
4. Advisor 320 (the backup's 28 GB on C:): two tries used; research before a third (Dropbox's client and the unpinned flag; whether this session's sandbox blocks the attribute write).
5. n23-3, n23-4, n23-5, n23-7 (the 19:00 DAILY file). Advisor 310 into RULINGS within its cap.
0g. GTA VI footage queue (depth first, advisor 302): the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover"; read it before the next footage piece.
0a. Advisor 277: Kiln, hair and the crowd paused.
0b. Night walk fixes: the 23 Nov walk ran 14 of 15 stages (per the audit's reviewer; read its report); the next walk is Mon 30 Nov 01:30.
1. Paused with Kiln: Ron's seated hem cover try 2 of 2 (Fable legs lane; the 20 Nov FAIL film its acceptance view); fins try 3 brief READY (tool-dev/reports/BRIEF-KILN-LANE-FINS3-FABLE.md).
4. Marvelous export done 21 Nov (results F:/LedgerTools/md-jobs/export-2026-11-21.json; LOG.md Exports). Marvelous stays open (his word). No Unreal work until the browser prototype is done, then Kiln (advisor 288).
5. History rewrite: HELD for his word at the PC. Progress page daily from the live page (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 23 Nov 16:2x: running a just-fetched ffmpeg, and a page script fetching YouTube captions, were refused by the permission check; not worked round. Stamps ran ahead twice more: Get-Date first.
- 21-22 Nov: 'uncut' descriptions can be false; seeks hang in some runs (test one); run ci-checks alone (./tools/ci-checks.sh after unset MSYS_NO_PATHCONV; env -u bash is refused); stamps ran about 10 minutes ahead of the clock five times: Get-Date in its own call before every stamp.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

