# Retention step 2, third version: fresh hostile review, 17 November 2026

Method researched: tools/retention.py at commit d970baa10 (the map, plan, reader-scan, owner, proposal, space and delete code and the self-test, read in full), tools/cleanup.py remove_tree, tools/backup-to-dropbox.py's source list, production/storage-map.json, production/retention.json, production/specs/in-game.json, RULINGS.md "Disk, git and backup" (29 Oct, 17 Nov), RETENTION-STEP2-2026-11-17.md, RETENTION-STEP2-REVIEW-2026-11-17.md, RETENTION-STEP2-REVIEW2-2026-11-17.md, the LEDGER scheduled tasks' command lines (Task Scheduler); read 17 Nov 18:30 to 19:45 (local).

Checks run: `python tools/retention.py --selftest` (passed, 6.4 s wall, in the reviewer's scratch folder); `python tools/retention.py plan` once, dry (see "The plan's measured time"). Besides those two, only read-only probes written in the reviewer's own scratch folder, none importing or running a project tool: a listing of junctions and links near the mapped folders; a text search of files the reader scan never opens (untracked files in the repository, the side-session folders, two unmapped ledger-* folders, the Claude config's scheduled tasks and skills); and a walk that counts, without opening, the files the reader scan would open. That walk read only file names and sizes in F:/LedgerTools/keys. Nothing in the project was deleted, moved, switched or committed. mapRulesLive was not touched.

## Verdict: PASS WITH FIXES (three must-fix before mapRulesLive is set)

Every blocking finding of the first two reviews is now closed in the code path, not only in the test names: rows with no owner or an unknown source are kept, a newer round's scripts in a working folder keep the old round, copies of the map are no readers, git failures and malformed rows stop the map, and the night acts only when the map files equal main's. Switching on today would remove nothing, for four separate reasons: no map line has an owner; storage-map.json is not on main yet, so map_files_committed refuses every row; Marvelous is open on most nights and counts as busy; and eight mapped folders exceed the reader cap (N-R5 below). That safety is real but partly accidental. Three gaps would let a wrong delete through once the owners are written, and each has a small fix.

## Earlier findings, checked by code path

| Finding | State | Evidence |
|---|---|---|
| First review B1 / second review N2: readers outside tools/, the scalp pattern | **Fixed** | find_readers (1409-1455) reads every tracked text file, then every mapped folder except side-session and build-cache shelves, working rows included, plus every protected path (1445-1446). A file inside the candidate never counts (1425). Fixture 1015-1022 goes through map_plan with a working sibling. The docstring now says reports keep a folder through find_readers, not delete() (1281-1282). RETENTION-STEP2 line 9 still says delete() refuses what is "named by a report" (docs only). |
| B2 / N1: no owner, or an unknown source | **Fixed** | `if owner not in LEDGER_OWNERS` (1542). A working row with an empty source, or one holding any DOUBT_WORDS entry, is kept (1548). This covers the map's plain "unknown" spelling (fixture 1028-1029). A tools row in doubt goes to his page, never to the remove list (1586-1594). |
| S1: twins, '..', aliases | **Fixed** | Real-path comparison, a '..' refusal and a link or short-name refusal (1521-1535). A twin or parent line on another shelf, or with another owner, keeps the row. |
| S2: copied-in files keep old dates | **Fixed** | newest_any (278-298) takes the newest modification or creation time of every file and folder. Python is 3.12.8 (st_birthtime). The fixture at 1159-1163 now runs map_plan's own age function. See N-R6 for silent walk errors. |
| S3 / N3: "removed ... kept", conditional and partial orders | **Fixed for the listed phrases** | says_remove (1315-1319) needs "remove:" or "remove candidate" at the start and no HEDGE word (1311-1312). All eleven probe-E phrases are fixtures (1031-1036). Negations are still read as orders (N-R4). |
| S4 / N6: malformed map | **Fixed** | Any non-object row, or a row with a non-string or empty path, raises (1504-1508). enforce (498-502) and main (1656-1661) turn that into "the map lists nothing". floors() tolerates malformed shelves_gb (1464-1481). Paths are not checked for being absolute (N-R7). |
| S5 / N10: uncommitted or unreviewed map edits | **Fixed for the two data files; the code is not covered** | map_files_committed (311-332) refuses when either file is dirty, differs from main (origin/main as a fallback), git fails, or an environment override is set. MAP_FILES (308) leaves out tools/retention.py and tools/cleanup.py, which decide what goes (N-R1). |
| M1 / N9: busy skip | **Mostly fixed** | Any of MAP_BUSY stops every map row (391, 507, 516-520). A tasklist that runs but fails still reads as "nothing running", and UnrealEditor-Cmd.exe and seamshift.exe are not matched (N-R9). |
| M2: "not public", "private" as refetchable | **Not fixed** | DOUBT_WORDS (1292-1293) is unchanged. A tools source such as "private build, not public" still counts as refetchable (1586). |
| M3: latency is both a limit folder and a remove row | Moot for now | The row's source is "unknown", so N1 keeps it. |
| M4: working 3 days against RULINGS' 14 days | **Not fixed** | RULINGS line 123 still says run outputs expire in 14 days. The map and code say 3. |
| N4: aliases elsewhere | **Fixed for mapped lines and protected paths** | The inner check also compares real paths (1570). with_reals (472-483) adds the real folder of each protected path. Links from unmapped places into a candidate are not seen (N-R2). |
| N5: copies of the map protect everything | **Fixed as asked** | COPY_NAMES, NOT_READER_DIRS and is_repo_copy (1304-1340, 1360, 1393, 1449). But Claude's scratch transcripts now play the same part (N-R5). |
| N7: git failure narrows the scan | **Fixed** | repo_files raises (1347-1353). The fixture is at 1082-1088. |
| N8: time and memory | **Memory fixed; time not exercised on real data** | Files are read one at a time and the scan stops once every candidate is named (1409-1455). space runs the map rows only when the limits leave a drive short (737-742). Measured below. |
| N11: smaller points | **Fixed** | "session" is no owner (1289). MAP_AGE and READ_CAP are restored (865-866). A capped folder keeps unnamed rows (1613-1617). Relative bare names in scripts under the parent count (1427-1428). floors() is robust. |

## Must fix

### N-R1. The night runs whatever tools/retention.py the working copy holds; only the two data files are checked against main
- Where: tools/retention.py:308 (MAP_FILES), 311-332. The task "LEDGER retention" runs `pythonw C:\Users\Jafar\ledger-local\tools\retention.py nightly` from the working copy (Task Scheduler, read 17 Nov).
- Scenario: a session on wip edits retention.py while working on step 3. It might widen REFETCH_WORDS, raise READ_CAP or add "site-packages" to SCAN_SKIP_DIRS so the rules finally act, or drop a guard while debugging, and leave it uncommitted or committed on wip only. With the switch on and both data files equal to main's, the 03:30 run applies the unreviewed decision code. S5 was blocking for exactly this risk in the data files, and the code that interprets them carries more risk.
- Fix: add "tools/retention.py" and "tools/cleanup.py" to MAP_FILES. That way the night's map rows need the decision code itself to be clean and equal to main's. Add a fixture: a dirty retention.py in the fixture repository refuses.

### N-R2. A link from elsewhere into a candidate is invisible: the played game reads voice-portable through a junction
- Where: tools/retention.py:1393 and 1449 (the scan skips links and never records where they point), 1569-1570 (the inner check knows map lines only). The scan also avoids the repository whole (1443), including ue-probe/Content and its junctions.
- Measured on disk (read-only listing): F:\LedgerTools\played-game\Windows\Voice is a junction to F:\LedgerTools\voice-portable. That folder is a tools row, not protected, with source "rebuilt by tools/voice-live/make_portabl..." ("rebuilt by" counts as refetchable, 1290). The game's content uses 37 junctions, from ue-probe\Content\Ledger\... to F:\LedgerTools\mh-dress\Content\... and C:\LedgerTools\mh-assemble\.... Those targets are protected today.
- Scenario: a later map edit gives voice-portable the owner LEDGER and "remove candidate: superseded by the pocket build". It is read every time the played game talks, but never written, so after 14 days it reads as unused. Today it is kept only because prose files (THIRD-PARTY.md, the workflow, playtest notes) mention its path. A future junction from ue-probe\Content into a new working folder on F: would have no such mention, and RULINGS 29 Oct says what the game uses is never deleted.
- Fix: while walking, read each skipped link's target (os.readlink) and keep any candidate equal to, inside or holding a target. Walk ue-probe\Content and F:\LedgerTools\played-game for links only, even though the repository is otherwise avoided. Add a fixture: a junction in a lasting folder pointing at a working candidate keeps it.

### N-R3. The reader scan opens F:/LedgerTools/keys
- Where: tools/retention.py:1445-1446 (every lasting row and every protected path is a scan root; F:/LedgerTools/keys is both) and 1397-1406 (its .txt and .json files are yielded and read by read_lower).
- Scenario: once any map row is pending, the first plan or night that finds a candidate still unnamed reads every key file into memory. The map's own line says "keys; contents never opened". The backup refuses that folder (backup-to-dropbox.py NEVER_DIRS), and the standing key rule says keys are never opened, printed or copied. Nothing is printed, but this is the opening the rule forbids.
- Fix: in scan_walk and the roots loop, skip any folder that backup-to-dropbox's NEVER_DIRS would refuse (ledgertools/keys, fmodel, .ssh) and any file named like a key (.env, *key*). A fixture: a keys folder whose file names the candidate is never opened (the row stays removable, or is kept by a rule other than that file).

## Should fix (with or soon after going live)

### N-R9. The busy check reads a failed tasklist as "nothing running", and misses Unreal commandlets and Kiln's seamshift
- Where: tools/retention.py:380 and 383-386.
- Scenario: tasklist returns non-zero with empty output (WMI fault, timeout inside tasklist). busy() returns set(), so map rows are removed while the game or Unreal may be running. "unrealeditor.exe" is no substring of "unrealeditor-cmd.exe", which every -run=pythonscript import uses, and seamshift.exe, a Kiln binary in cargo-target/kiln/release, is not listed.
- Fix: return {"unknown"} when returncode is non-zero or the output lacks "image name". Match "unrealeditor" without ".exe", and add "seamshift". A fixture with a stubbed failing tasklist.

### N-R4. Negations and his refusals read as remove orders
- Where: tools/retention.py:1311-1319.
- Scenario: a session records his answer in the line as "remove candidate rejected: his no, 18 Nov" or "remove: not safe, the regression jobs read it". Neither holds a HEDGE word ("rejected", "not", "his no", "never", "do not" are absent), so both parse as whole-folder orders.
- Fix: add not, never, rejected, refused, declined, "his no", "do not", "don't" and "jafar" to HEDGE. Better still, remove only on an explicit field such as `"expire": "remove"` and leave the prose for people.

### N-R5. The reader scan is inert on the real disk by accident, so the rules have never been exercised on real data
- Where: tools/retention.py:1299 (READ_CAP 5000), 1298 (SCAN_SKIP_DIRS), 1613-1617 (any capped folder keeps every unnamed pending row), and the working row C:/Users/Jafar/AppData/Local/Temp/claude (a scan root).
- Measured (read-only count, same skips as scan_walk): eight roots exceed 5,000 text files. They are C:/LedgerTools/chatterbox-nano (5,633), Temp/claude (10,192), voice-portable (6,554), uv (30,050), voice-env-export (15,921), pylib (13,392), pocket-tts (7,986) and garmentcode-lab (5,915), all Python environments except Temp/claude. So once owners exist, every row nothing names is kept as "not fully read". Temp/claude also holds Claude sessions' tool transcripts. They contain whole reads of the map and the inventories, so they name every row (the N5 accident again), and walking that folder alone took 77 s.
- Risk: none today, since this keeps. But the first change that makes the rules act (skip "site-packages", raise the cap, clean Temp/claude) switches on decision behaviour that no review has seen run.
- Fix: avoid Temp/claude as a reader root (it is a scratch, not a reader). Skip site-packages, Lib, venv*, env and the python folders inside tools rows as reader roots. Print the capped folders in `plan` so an inert plan says it is inert. Have a fresh review read the first real plan that lists remove rows before the switch.

### N-R6. Silent walk errors make a folder look older and leave readers unread
- Where: tools/retention.py:291 (newest_any's os.walk, no onerror), 1384 (scan_walk), 1370-1376 (read_lower skips files over 2 MB, or unreadable files, without a word).
- Scenario: a subfolder that cannot be listed (access denied, or in use by a sync or antivirus scan) is skipped. Its new files then never count toward the age, so the row reads as weeks old and goes, and remove_tree then fails inside it: a partial delete. A reader inside a 2.5 MB manifest or job list is never read.
- Fix: pass onerror to both walks and keep the row ("not fully read") on any error. Search files over 2 MB in chunks for the candidates' keys rather than skipping them.

### N-R7. A removal that dies midway leaves no line in deleted.log
- Where: tools/retention.py:238-245 (log only after _remove returns), tools/cleanup.py:172-177 (a failed rmdir raises after the children are gone).
- Scenario: the machine sleeps or reboots for an update at 03:30, or remove_tree raises something other than OSError. The folder is half removed and nothing is logged. The morning line shows nothing, and the next night the folder's changed dates make it look new.
- Fix: write an "about to remove" line (path, bytes, rule) before _remove, then the result. Better: rename the folder into a same-drive quarantine (F:/LedgerTools/retention/quarantine, C:/LedgerTools/.quarantine) and remove it after 7 days. On Windows a directory rename fails as a whole if a file inside is open, so a used folder is never half deleted, and a wrong delete can be undone within a week. Cap the first live weeks at a few rows a night.

### N-R8. Paths are not checked for being absolute; doubt words miss his approvals
- Where: tools/retention.py:1507 (validation), 68-69 (norm resolves a relative path against the current folder), 1292-1293 (DOUBT_WORDS).
- Scenario: a row written "ue-probe/Saved/old-captures" resolves against the night's Start In (ledger-local) and lands inside retention.json's places. Run from another folder, it resolves elsewhere, so plan and night disagree. Separately, a working row whose source reads "made by LEDGER runs; approved pictures also copied" (the real F:/LedgerTools/gate line, protected today) or "downloaded at his request" carries no doubt word. RULINGS 29 Oct needs his yes for both.
- Fix: refuse the map (ValueError) when any path lacks a drive letter and a root. Add approved, "his request", bought, evidence, licence, "not public" and private to DOUBT_WORDS.

## Minor

- RETENTION-STEP2-2026-11-17.md line 9 still says delete() refuses what is "named by a report". RULINGS line 123 (14 days) and the map (3 days) still disagree, and nothing says which wins.
- `plan` treats the map files as committed (504), so it lists rows the night would refuse. Today storage-map.json is not on main at all, and the plan does not say so. Print map_files_committed's answer in plan.
- remove_tree clears the read-only attribute before removing (cleanup.py:181), so a file someone marked read-only to keep it goes anyway. Treat a read-only file in a map row as "keep the row".
- Marvelous stays open between garments (his word) and counts as busy, so on most nights no map row can go. That is safe, but the night's summary should say why nothing went.

## What held up under attack
- Dry run: `plan` passes dry=True. delete() returns before removing and before logging, and map_plan only reads.
- The switch: only the JSON value true. retention.json has no mapRulesLive.
- Owners: no map line has an owner, so the plan keeps all 134 rows (measured).
- Twins, '..', short names, junction parents, protected paths written through a junction: kept or refused.
- Malformed map or rows, git failure, environment overrides, dirty or non-main map files: the map lists or acts on nothing, and the limits stand.
- The backup: backup_paths reads the same in-game.json list as backup-to-dropbox.py, Kiln's sources and bundle included, and the Dropbox folder is outside every place.
- Junctions inside a removed folder go as links (cleanup.remove_tree), so the target is untouched. LongPathsEnabled is 1, so deep paths are walked.

## The plan's measured time
- `python tools/retention.py plan`, 17 Nov 19:2x local: **19.0 s wall, peak working set 133 MB** (psutil, polled every 0.2 s), exit 0. The map section kept 134 rows and removed none. The reader scan never ran, because no row is pending without owners. So this figure is the limits and their protected-row output (1,343 lines), not the scan.
- The scan's cost once owners exist was not run, as the brief allows only these two commands. A read-only count of what it would open: walking the scan's roots took **110 s** (77 s of it Temp/claude), with about 59,000 text files after the cap and about 1.8 GB of text eligible to be read, plus the 6,715 tracked files (4.4 s in the second review). Memory should stay low, since files are read one at a time (each under 2 MB). Expect a few minutes per plan, night or short `space`. This is an estimate, not a measurement.

## Fixes, 17 November (helper; mapRulesLive still off, nothing deleted)
- N-R2: map_plan walks every mapped folder (not the never-opened keys), every protected path and LINK_ROOTS (ue-probe/Content, F:/LedgerTools/played-game) for links only (link_targets, names only, about 0.1 s for the 39 real links), and keeps any candidate a link outside it reaches: equal, inside or holding its target (reached_by_link). Read-only on disk it finds played-game/Windows/Voice to voice-portable. Tests: reached_by_link cases; link_targets records two junctions; a junction in a lasting folder and one in an unmapped game folder keep their working targets, and without the game folder only that one is removable. The N4 fixture now gets kept by the link rule first; N4's own guard is checked directly through may_delete.
- M2: DOUBT_WORDS adds "not public" and "private". No real map source has either. Tests: a tools row "private build, not public" goes to his page, never removed; a working row with a private source is his.
- M4: MAP_WORKING_DAYS 3 to 14, following RULINGS' "run outputs expire in 14 days"; the map's working expiry text was changed in 50 places (49 rows and the shelf's line). The "tool test and Kiln run outputs" limit was already 14. The "renders and films" limit (3 days, its own older rule) was left alone. Fixture ages now follow MAP_WORKING_DAYS. Tests: RULINGS' number equals MAP_WORKING_DAYS, every working row says 14 days, and the run-output limit keeps 14.
- N9 (N-R9): busy_from(run): a tasklist that fails, times out or answers without its "Image Name" header reads as "unknown" (busy). "unrealeditor" now matches UnrealEditor-Cmd.exe, and seamshift counts as drape. Tests: failing, empty, timeout, Cmd, seamshift and idle stubs. The header check assumes an English Windows, which this PC has.
- Self-test: passed, 149 checks (it now counts them). `plan`: exit 0, map not live, 134 kept, none removed.
