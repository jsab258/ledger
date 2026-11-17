# Retention step 2, second version: fresh hostile review, 17 November 2026

Method researched: tools/retention.py at commit 1aae40794 (map_plan, reader_text, enforce, newest_any, map_files_committed, the self-test), the two fix commits (`git log -3 -p -- tools/retention.py`), DECISIONS.md 17 Nov 17:54, the first review (RETENTION-STEP2-REVIEW-2026-11-17.md), production/storage-map.json, production/retention.json, RULINGS.md "Disk, git and backup" (29 Oct, 17 Nov), F:/LedgerTools/drapestudio-test-2026-11-13-final/run_all.ps1, the LEDGER retention task's command line (Task Scheduler); read 17 Nov evening.

Checks run: `python tools/retention.py --selftest` (passed, 3 s); `python tools/retention.py plan` (dry, 16 s; map section: 134 kept, 0 removed, 0 his page, because no map line has an owner); a read-only simulation that loads the real map, writes `owner: LEDGER` on every working and tools line in memory only, and runs map_plan with the real reader text (timed); read-only probes of map_plan on throwaway folders and junctions in the reviewer's own scratch folder. Nothing in the project was deleted, moved or switched; mapRulesLive was not touched. The probe folders (about 5,100 tiny files and two junctions pointing inside the scratch folder) remain in the reviewer's session scratch folder on C:.

## Verdict: FAIL (do not set mapRulesLive)

Switching on today would remove nothing, because no map line carries an owner. But the handover names "write the map's owners" as the next step after this review, and that data edit would arm two faults left from the first review's blocking findings. B2's "source unknown" guard does not match the way the real map writes its source ("unknown"), so 11 of the 14 remove rows pass it once owned. B1's reader scan still never reads the job files of working-shelf folders: that includes the protected -final round the first review cited, and every newer round. That is the scalp pattern itself. With today's data both are hidden only by accident: the reviews, the inventories and a copy of storage-map.json in the lane worktree name every row, so even with owners the simulation removes nothing. That accident also makes the rules inert, and the reason the plan prints is wrong.

The parts that hold: the dry run is truly dry, the switch is exact, the twin, '..' and short-name logic works as written, creation-time ages work, a malformed map no longer crashes run or nightly, uncommitted map files stop the night's map rows.

## The first review's findings now

| Finding | State | Evidence |
|---|---|---|
| B1 readers sought too narrowly | **Partly fixed; the defining case is still open** | All tracked text files are now read (6,715 files, 4.4 s), plus the scripts in map folders whose shelf is not working or tools (retention.py:1254-1257). Working-shelf folders are never read, even protected ones: on the real map, F:/LedgerTools/drapestudio-test-2026-11-13-final, tool-dev and kiln-runs are working rows, so the scan never opens them ("-final in extra dirs: False"). Probe G: a protected working row's run_all.ps1 that names the candidate does not save it. The B1 fixture (946-950) calls reader_text with extra_dirs=[mp-final] directly, so it never tests map_plan's own choice of folders. The docstring (1065-1068) and RETENTION-STEP2 line 9 still claim that delete() refuses anything "named by a report". See N2. |
| B2 rows with no owner treated as ours | **Partly fixed** | The owner half is fixed: `if owner not in LEDGER_OWNERS` (1222). The source half fails on real data: it matches only "source unknown" or "unknown source" (1227), but the map writes `"source": "unknown"` (11 remove rows) and "unknown (an exported Python env ...)". Probe D: a working row with source "unknown" is removed. The fixture uses the one spelling that matches ("source unknown", 875). See N1. |
| S1 spelling, twins, aliases | **Mostly fixed** | Twins with a trailing slash, '..', a junction parent and 8.3 short names are all kept (probe A: realpath expands the short name, so the row is kept). Still open: a working row that holds the real folder of a lasting row reached through a junction elsewhere (probe B), and a protected path spelled through a junction (probe C). See N4. |
| S2 copied-in files keep old dates | **Fixed** | newest_any takes the newest of modification and creation times of the files and folders (275-295). Python 3.12.8 (miniconda, the nightly's interpreter) has st_birthtime. A move into the row bumps the row folder's own date, which newest_any counts. The map_plan fixtures swap in newest_mtime (905), so the real age function is tested only alone (minor, N11). |
| S3 "removed ... kept", "check with him" read as orders | **Partly fixed** | Both phrases are now refused. Still read as remove orders: "remove: the logs (2 GB); the models stay", "remove once Kiln confirms", "remove after his OK", "remove: keeping only the reports", "Remove candidate - not yet", "remove only if unused by 20 Nov" (probe E). See N3. |
| S4 a malformed map crashes run, plan and nightly | **Mostly fixed** | A non-list `folders` raises ValueError, and enforce and main catch any Exception (459, 1327). Still open: malformed rows are dropped silently, which removes the protection they gave (N6), and `space` still crashes on a malformed shelves_gb (N12). |
| S5 the night acts on uncommitted map edits | **Fixed as asked** | map_files_committed (305-313) refuses every map row when either file shows in `git status --porcelain`. It returns False, so refuses, when git is missing or fails. Remaining gaps are minor (N10). |
| M1 busy skip | **Partly fixed** | Map rows now get the runner and Unreal skip (472). It covers only ue-probe, UnrealEngine and the runner's paths. A failed tasklist ("unknown") skips nothing, and Kiln, drape-studio, Blender, Marvelous and the game are not considered (N9). |
| M2 "not public", "private" | Not fixed | DOUBT_WORDS (1076-1077) unchanged. |
| M3 latency is both a limit folder and a remove row | Not fixed (data) | The map line is unchanged. Harmless while no line has an owner. |
| M4 working 3 days against RULINGS' 14 days | Not fixed | RULINGS line 123 still says run outputs expire in 14 days. The map and code say 3. Nothing says which wins. |
| M5 ai-video and F:/f kept by accidental matches | Moot | Both are kept by the owner rule now. |

## New findings

### N1. Blocking. The "source unknown" guard misses the map's own spelling (B2 not closed)
- Where: tools/retention.py:1227-1229. Fixture at 874-875 and 924.
- Scenario: the next step writes `owner: LEDGER` on the working rows the inventory attributes to LEDGER runs, for example F:/town-bench, game-voice, game-voice2, playtest, retired, selfcheck-voice-2026-09-26 and south-quay-work, all `source: unknown`. `line` becomes "unknown remove: ...", which contains neither "source unknown" nor "unknown source", so the guard passes them. Today the reader text's accidental matches keep them (N5). Once those are cleaned, or for any new row whose source is "unknown" and which no inventory names, a row of unknown making goes after 3 days. That breaks RULINGS 29 Oct: "anything that cannot be made again ... When in doubt, it is his". Probe D confirmed it on throwaway folders.
- Smallest fix: for working and tools rows alike, keep any row whose `source` field contains a DOUBT_WORDS entry ("unknown" first) or is empty, and list it as a his-page candidate. Change the fixture's source to the real spelling "unknown", and add an empty-source case.

### N2. Blocking. The reader scan never opens working-shelf folders: the newer round that reads an old round (the scalp pattern) is not seen
- Where: tools/retention.py:1254-1257, where the extra folders are only lines whose shelf is not working or tools. Also reader_text 1135-1145, docstring 1104-1108 ("lasting and protected folders": protected folders are not read), and the fixture at 946-950.
- Scenario (the first review's own case): F:/LedgerTools/drapestudio-test-2026-11-13-final is protected in retention.json but sits on the map as `working`. Its run_all.ps1, lines 5 and 20, reads F:/LedgerTools/drapestudio-test-2026-11-11 (absolute paths). map_plan does not pass -final to reader_text, so the script is never read. -11-11 is kept today only because the first review, RETENTION-STEP2 and the inventories, all tracked, name it. A future pair is unprotected: drapestudio-test-2026-11-20 (working, "remove: superseded") read by drapestudio-test-2026-11-22's job files (working, inside its 3 days). No note names -11-20, so it goes on night four, and a rerun of -22 finds no source. That is exactly how Darren's scalp was lost. Probe G reproduced it. F:/LedgerTools/tool-dev (Drape Studio's source, the judge and the protected runs) and C:/LedgerTools/kiln-runs are also working rows, so their scripts are never read either.
- Smallest fix: build the extra folders from every mapped folder that exists, on every shelf, plus retention.json's protected paths. Skip the candidate itself, the repository copies listed in N5 and F:/LedgerTools/retention. Add a fixture that runs through map_plan, not reader_text: a protected working sibling whose script names the candidate keeps it. Correct the docstrings and RETENTION-STEP2's "named by a report".

### N3. Should-fix. Conditional and partial proposals still remove the whole folder
- Where: tools/retention.py:1265-1267.
- Scenario: Claude writes "remove: superseded review pictures; the preview stays", which follows the map's own working rule ("a superseded review picture keeps its preview only"). The whole folder goes, preview included. "remove once Kiln confirms" goes the same night, before Kiln confirms. "keeping" and "keeps" slip past the word-bounded `keep` (probe E).
- Smallest fix: remove only on an explicit field (`"expire": true`), or only when the proposal starts with "remove:" and contains none of: stay, keep\w*, kept, except, but, only, once, after, until, when, if, wait, not yet, unsure, "?". Add a fixture for each probe-E phrase.

### N4. Should-fix. A junction or other alias elsewhere hides a protected or lasting folder inside a working row
- Where: tools/retention.py:1210-1211 (the twin check looks only for equal or parent folders, never for children), 1245 (the inner check compares text), and may_delete 160-174 (inside() compares text, not real folders).
- Scenario: probe B. A lasting line names C:/side/assemble, a junction whose target is F:/work-b/inner. The working row F:/work-b is removed, and the lasting folder's real contents go with it. Probe C: retention.json protects a path spelled through a junction (as it does with C:/LedgerTools/parler-tts → F:/LedgerTools/parler-tts). The working row at the target is not refused. Today the only junction is parler-tts, and its F: row is held by the protected designed/ folder and its "removed ... kept" line, so this is latent.
- Smallest fix: in map_plan, compare real paths for the inner check too: keep a row when any other line's real path lies inside its real path. Before may_delete, add the real path of each protected entry to protected_extra.

### N5. Should-fix. The scan reads copies of the map, the inventories and side checkouts: it protects everything, by accident, and slowly
- Where: tools/retention.py:1254-1257 (side-session and build-cache shelves count as reader folders), 1112 (NOT_READERS skips only the repository's own two files), 1259 (the printed reason).
- Measured (simulation, owners added in memory): C:/Users/Jafar/ledger-lane, a sparse worktree holding a copy of storage-map.json, names 78 of 78 working and tools rows. ledger-local/production names 78 of 78, through INVENTORY*, CLEAROUT-LIST and the two reviews. The runner's checkout names 68, ledger-lab 40 and ledger-talk 38. Result: remove 0, his page 0. Every row prints "a tool in the repository names it", which is false: it is a copy of the map or an inventory. The rules are inert, and whether a row survives depends on what an unrelated sparse worktree happens to hold. Its last sync decides the outcome.
- Smallest fix: skip every file named storage-map.json or retention.json wherever it is, production/research/disk/, F:/LedgerTools/retention, the side-session and runner checkouts (git copies of this repository), and build caches. Print which file named the row.

### N6. Should-fix. Malformed rows are dropped silently, and their protection goes with them
- Where: tools/retention.py:1188.
- Scenario: a lasting row's path is written as null, a list or "" by an editing slip. It vanishes from `folders`, so the inner check (1245) and the twin check no longer see it. A working parent row that holds it now passes "holds another mapped folder" and is removed, lasting contents included. The first review's S4 asked for validation, not filtering.
- Smallest fix: raise ValueError when any entry is not an object with a non-empty string path. enforce and main already turn that into "the map's rules list nothing".

### N7. Should-fix. When git fails, the reader scan silently narrows to the old folders
- Where: tools/retention.py:1124-1134.
- Scenario: `git ls-files` returns an error, for example "dubious ownership" under another account, a damaged index, or the runner's checkout mid-clean. `names` is empty, so the scan falls back to READER_DIRS (tools, ue-probe Source and Config, specs, .github). Records, approvals and casting notes drop out without a word: B1's original blindness returns. A missing git raises FileNotFoundError, which enforce catches as "lists nothing" (safe). A git that runs and fails is not caught.
- Smallest fix: when `git ls-files` returns non-zero or nothing inside a checkout, raise, so the map lists nothing. Keep the fallback only behind a parameter the self-test passes.

### N8. Should-fix. The reader text costs about 2 minutes and several GB at the moment `space` is short of room
- Where: tools/retention.py:1110-1146; enforce 455-458, which `space` calls (685-689) when a drive is short; tools/ue/build-local.ps1:23, the workflow's line 196, morning_pictures.py and every Kiln round's check.
- Measured: tracked text alone 4.4 s and 481 MB as one Python string (a character above U+FFFF, U+1F990, forces 4 bytes per character). The extra folders add about 109 s and roughly 365 M characters, about 120 M of them from the runner and side checkouts. The final string is about 1.9 GB, and join, two replaces and lower keep two or three copies alive at once: roughly 4-6 GB peak. That figure is estimated from the measured sizes, not measured as a peak. Once owners exist, the scan runs on every `space` call that finds a drive short: before a build, a Kiln gate (whose timing bands already failed once on a busy machine) or a render, which is exactly when memory and disk are scarce. The nightly at 03:30 sits between the 01:30 walk and the 04:15 pictures.
- Smallest fix: drop the copies (N5). Instead of one joined string, search each file for the candidates' keys as it is read: compute the remaining candidate keys first, read files one at a time and stop when all are found, never holding the whole text. In `space`, list the map's rows without removing them unless the limits alone leave the drive short.

### N9. Minor. The busy skip ignores an unknown process list and the project's other long jobs
- Where: tools/retention.py:464 and 472, busy 358-366.
- Scenario: tasklist times out, so `running == {"unknown"}`, and nothing is skipped. Separately, a Kiln or drape-studio job, Blender, Marvelous or the game reads old inputs from a working row at 03:30. Reading does not change the files' dates, so the row is removed under the running job.
- Smallest fix: treat "unknown" as busy for every map row. Skip all map rows while "game", "marvelous", Blender or a drape-studio or Kiln process runs (add them to busy()).

### N10. Minor. "Committed" is not "reviewed", and the files checked are not always the files used
- Where: tools/retention.py:305-313, 463; POLICY and MAP environment overrides at 55 and 1002.
- Scenario: a session commits "remove: ..." on wip at 03:00, and it acts at 03:30. The build machine runs `space` in its own checkout (always clean), so any pushed commit with the switch on acts there. When LEDGER_RETENTION_POLICY or LEDGER_STORAGE_MAP points elsewhere, the check still looks at the repository's files.
- Smallest fix: act on map rows only when HEAD's storage-map.json and retention.json equal main's (`git diff --quiet main -- ...`), since main holds only what passed review. Refuse map rows when either environment override is set.

### N11. Minor. Smaller points
- tools/retention.py:1073: "session" counts as our owner. A side session's owner written as "session" would count as LEDGER's. Allow only "ledger" and "claude".
- tools/retention.py:905: the self-test sets MAP_AGE[0] = newest_mtime and never restores it. map_plan's real age function is not exercised end to end.
- tools/retention.py:1136-1145: the cap of 5,000 text files per folder silently drops the rest. Probe I: a script after 5,100 small JSON files was not read. Count only after N5's skips, and list a capped folder as "not fully read: its rows kept".
- Relative references (probe F: `Join-Path $PSScriptRoot '..\work-f'`) are not matched. This is known ("paths built from pieces"), but a folder's own name, on its own, appearing in a protected sibling's script is a cheap extra check.
- tools/retention.py:1155-1166 and 1415-1420: a malformed `shelves_gb` (for example `"F": 5`) raises AttributeError in floors(). `space` then exits with a traceback, which build-local.ps1 and the workflow read as STOP. That fails safe but stops builds.

## What held up under attack
- Dry run: `plan` passes dry=True. enforce sets committed=True without calling git, and delete() returns before removing and before logging. map_plan and reader_text only read (git ls-files, file reads, tasklist). The run wrote nothing.
- Switch: only the JSON value true turns the map's rules on. retention.json has no mapRulesLive.
- Twins and aliases: a lasting twin with a trailing slash, a '..' path, a path through a junction parent and an 8.3 short name are all kept (fixture and probe A). Case and slash differences normalise.
- Ages: creation times on Python 3.12.8. Directory dates count, so a move or copy into a row reads as new.
- Owners: a row with no owner, or another owner, is kept. Today that means the map removes nothing (plan: 134 kept).
- S5: uncommitted map or policy files refuse every map row at night, and git missing or failing refuses too.
- S4: a non-list `folders`, a None entry or a numeric path no longer crashes run, plan or nightly. The limits' rows stand.
