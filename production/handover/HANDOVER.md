# Handover: where the production session stands

The one file a fresh session starts from. Rewritten at each stop; cap 1,800 words. Holds what is in flight, what failed, the next steps and the tries used.

**Started:** 2026-11-23 18:51 (the hourly run)

**Row due:** at the next start (last rows 17:22 hourly, 17:50 catalogue; page read 17:40: no verdicts, no advisor; filter verdicts after 2026-11-23T16:40 UTC, advisor after 2026-11-23T16:15:00+01:00; last ack 332 at 16:30).
**Uncommitted:** nothing beyond what the Stopped line names.
**Stopped:** 2026-11-23 18:08 (the 17:21 run: catalogue done and pushed; DAILY file; n23-5 research notes in; stopped before the recipe rewrite, which needs the whole recipe read and would not fit this run's history, 290k)

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
- 13:07-14:40: order adopted (his tap 08:12); ledger, archive, week-shape inactive, progress page, budget table, nightly schedule weekly; advisors 320-323 acked.
- 15:22-15:44: advisors 328-330 acked; tools/star_slots.py (47 of 49); G5 flag cleared; INSTALLED-METHOD.md written and reviewed. Pushed 4aa0f93e5.
- 16:22-16:43: advisors 331-332 acked; his games ruling in RULINGS; ffmpeg on the allowlist, its run refused, asked on his page; installed-game reprice. Pushed 697d7ae91.
- 17:21-18:08: hourly row 17:22; the hidden-details catalogue DONE (details-catalogue/CATALOGUE.md, NOTES-C; review PASS WITH FIXES, all 21 applied; row 17:50 on his page); NOW.md moved to this order; pushed f9ea54ea6. n23-5's questions written (production/research/recipe-rewrite/QUESTIONS-2026-11-23.md). DAILY-2026-11-23.md written by an extractor helper (US$48.17 by 17:50; API credit US$193.55 left to 12 Dec, ceiling about US$10 a day). final-reviewer and research-synthesis set to medium effort (due 13:00 today). Advisor 310 found already in RULINGS (DECISIONS 18:05).

## In flight
- Nothing runs. Browser pane page tools (lost on reload): capt/capt2 caption-strip finders, grab sheets.

## Next, in order
00. Pace first: `python tools/pace_line.py <week> --fable <fable>`. 17:22 read 24% against 2.4% (ceiling line plus 25, advisor 330): under it; lean, few helpers.
0. His page: recorder-for-drills-2026-11-23 still open. Without the recorder BOTH n23-1's drills AND n23-2's ruler check wait: the walk film (F:/LedgerTools/tmp/ai-tester/film/2026-11-23-0236, 94 frames) is play.py screen grabs at about 8 a second with no frame times, so it cannot time a walk (true walk 160, run 420 cm/s, SliceCharacter.h). With the recorder: KCD2 first per INSTALLED-METHOD.md, then Sleeping Dogs, GTA V, GTA IV openings by fixed key scripts; and film our packaged build for the ruler check.
1. n23-5 recipe rewrite: questions 3 answered (in QUESTIONS-2026-11-23.md: about 3,000 words of unfolded notebook entries since line 113 make room), 1/4/5/6 in OWN-FILES-NOTES-2026-11-23.md (1 and 6 partly). Gaps: DESIGN-COMPLETE.md and tools/lane/parts-tree/check.py live on origin/lane-2026-11 only (read with git show origin/lane-2026-11:production/lane/design-proof/DESIGN-COMPLETE.md); no build check tests the five-sample rule or the one-shot start gate. Question 2: WEB-NOTES-2026-11-23.md, thin (5 useful sources, fetches came back as digests, no first-hand Warhorse or Rockstar account; the Volition GDC 2015 abstract makes the slice the exit gate from pre-production). Next: the rewrite itself (fold the unfolded entries into their chapters; the order in chapter 0 and how a design counts as measured in chapter 1, linking tools/research_rules_check.py and needs_you_page.py; name that no build check tests the five-sample rule or the one-shot start gate), one fresh reviewer, commit.
2. n23-3 live talk measurements due Fri 27 Nov (Pocket delay against the 2 s bar); n23-4 voice scan; n23-7 (the credit row now in DAILY-2026-11-23.md; keep it daily).
3. n23-1: the reprice split and feel rows once drills run; every row names its blueprint decision.
4. Advisor 320 (the backup's 28 GB on C:): two tries used; research before a third.
0g. GTA VI footage queue: TRIED-ARCHIVE.md, "Moved from the handover".
0a. Advisor 277: Kiln, hair and the crowd paused. 0b. Next night walk Mon 30 Nov 01:30.
1p. Paused with Kiln: Ron's seated hem cover try 2 of 2; fins try 3 brief READY.
4p. Marvelous stays open (his word). No Unreal work until the browser prototype is done (advisor 288).
5p. History rewrite HELD for his word at the PC. Progress page daily (progress.json only); DAILY token file 19:00.

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- 23 Nov 17:3x: a caption-box detector run twice at once fought over the video's position and missed half the boxes; run one scan at a time. Silent detail videos have empty transcripts: read their caption strip by frames.
- 23 Nov 16:2x: running a just-fetched ffmpeg, and a page script fetching YouTube captions, were refused by the permission check; not worked round. Stamps ran ahead twice more: Get-Date first.
- 21-22 Nov: 'uncut' descriptions can be false; seeks hang in some runs (test one); run ci-checks alone (./tools/ci-checks.sh after unset MSYS_NO_PATHCONV; env -u bash is refused); stamps ran about 10 minutes ahead of the clock five times: Get-Date in its own call before every stamp.

## Kept as they are
- Waiting list for the next order: production/orders/2026-11-16.md section 3.
- Tries used: the full list moved 22 Nov 12:55 to TRIED-ARCHIVE.md, "Moved from the handover".
- API spend: US$3.77 this month (8 and 16 Nov); none 17-18 Nov.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run drapes or builds beside a timed Kiln gate; edit retention.py during a Kiln gate; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another main LEDGER session works; write a time without Get-Date; write judge/ from a fixer; name a held-back job to a fixer; write into his folders under C:/Game Dev Tools; delete a job file from md-jobs/inbox while the bridge runs (it crashed the bridge's tick at 19:17).

