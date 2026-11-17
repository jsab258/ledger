# Retention step 2: fresh hostile review, 17 November 2026

Method researched: tools/retention.py (map_plan, enforce, main, the self-test), production/storage-map.json, production/retention.json, RULINGS.md "Disk, git and backup", RETENTION-STEP2-2026-11-17.md, the 17 Nov scalp note; read 17 Nov evening. Checks run: `python tools/retention.py --selftest` (passed), a read-only `map_plan` on the real map (removes nothing), read-only probes of `map_plan` on throwaway folders in the reviewer's scratch folder, and text searches of the repository and F:/LedgerTools for the names on the remove list. Nothing in the project was deleted, moved or switched; mapRulesLive was not touched.

## Verdict: FAIL (do not set mapRulesLive)

The switch, the dry run and the delete path are sound: `plan` is truly dry, `run`/`nightly`/`space` remove no map row while the switch is off, a junction inside a removed folder goes as a link, protected, held, backed-up and outside-the-places paths are refused, and an unmapped folder is never touched. The fault is in what the rules decide is safe to remove. Of today's 14 remove rows, 4 are named by the project's own records or job files as kept or as evidence, and the checks that would catch that (a reader outside tools/, an owner, a known maker) are missing or empty. Two blocking findings, then the rest.

## Blocking

### B1. The reader check cannot see the project's records or the job files on F:, so it repeats the 17 Nov scalp loss
- Where: tools/retention.py:992-995 (READER_DIRS: tools, ue-probe/Source and Config, production/specs, .github only), 1119-1127 (the reader check), 979-982 and RETENTION-STEP2 line 9 (the claim that delete() refuses anything "named by a report"; named_keep, 119-143, protects only direct children of the namedKeep folders, never a map row such as F:/LedgerTools/retired).
- Today's real plan would remove, with no tool flagging them:
  - F:/LedgerTools/selfcheck-voice-2026-09-26 (14 files): production/approvals/2026-09-26-weekend/gate.json line 69 names it as the evidence for that gate's set-aside voices, and production/casting/voice-key-2026-09-26.json line 86 says the clips were "moved to ... selfcheck-voice-2026-09-26/clips as evidence".
  - F:/LedgerTools/playtest (walk-2026-10-26-pm): production/research/cab-office-interior-1990/WEAR-2026-10-25.md line 100 cites it as the AI tester's walk verdict for a packaged build (evidence that cannot be made again).
  - F:/LedgerTools/retired (41 files): the tracked note ledger/Assets/StreamingAssets/Decals/generated/RETIRED.md says the retired pictures "are kept, unchanged, in F:\LedgerTools\retired\imagegen-2026-09-03" (ledger/ is not scanned).
  - F:/LedgerTools/drapestudio-test-2026-11-11: F:/LedgerTools/drapestudio-test-2026-11-13-final/run_all.ps1 lines 5 and 19-20 (inside the protected -final folder) read their job sources from it. After the delete, a rerun of run_all.ps1 finds no source and, with ErrorActionPreference Continue, writes empty job files over the -final copies. This is the scalp pattern exactly: an "old round" read by a newer, protected round, named only in a job file on F:.
- The same blindness applies to any working line nested inside an unprotected lasting folder (24 lasting folders on F:, such as casting-candidates, ron-voice, trellis, mh-dress outside Content, are not in retention.json's protected list): a future line "F:/LedgerTools/casting-candidates/old-round, working, remove: superseded" is judged only by the repository text.
- Smallest fix: before a map row may go, search, besides READER_DIRS, the root records and production/ (all .md and .json, the approvals, casting, audits, handover), ledger/, and the text files (.py .ps1 .json .md .txt, under 2 MB) in the other F:/LedgerTools and C:/LedgerTools folders, excluding the candidate itself, the map, retention.json, the inventories and F:/LedgerTools/retention; any hit keeps the folder and lists it. Correct the docstring and RETENTION-STEP2's "named by a report" claim. Add a fixture: a protected sibling whose script names the candidate.

### B2. "When in doubt, it is his" is inverted: a line with no owner and an unknown source is treated as LEDGER's
- Where: tools/retention.py:1088 and 1092 (`if owner and owner not in LEDGER_OWNERS`), and the working branch at 1145-1149, which never looks at the source.
- The map has no `owner` field on any of its 134 lines (its fields: path, shelf, gb, serves, expiry, last_write, proposal, backup, source), although the 17 Nov ruling says each gigabyte has an owner in the map. So the owner guard never fires. 11 of the 14 remove rows have `source: unknown` (cleanup-2026-09-26, game-voice, game-voice2, latency, playtest, pso-record, retired, review-faces-2026-09-26, both review-voice folders, selfcheck-voice, south-quay-work). The 29 Oct ruling lets Claude delete without asking only what it made itself that nothing uses, and never what cannot be made again; an unknown maker is the doubt the ruling hands to him.
- Smallest fix: one line, keep any row whose owner is not explicitly LEDGER or Claude (`if owner not in LEDGER_OWNERS`), and for the working shelf also keep a row whose source contains a DOUBT word ("unknown" first), listing both as "his page" candidates. Then add `owner` to the map's lines (the inventory knows most of them). Until the map carries owners the map's rules remove nothing, which is the safe state. Fixture: a line with no owner and source unknown is kept.

## Should fix (before or with going live)

### S1. The lasting guarantee depends on spelling: a duplicate or aliased line removes a lasting folder
- Where: tools/retention.py:1110 (the inner check skips any line whose normalised path equals this one) and 1089 (the shelf is read from this line only).
- Probe (throwaway folders): the same folder listed twice, once lasting and once working with a trailing slash, was put on the remove list; so was a working line spelled "other/../lastingx" pointing at a lasting line. An 8.3 short name or a path through a junction parent (is_link checks only the path itself, line 1104) would do the same, and inside() and may_delete compare text, not the real folder, so a working line under a junction in a place could reach a folder outside the places.
- Fix: compare `os.path.normcase(os.path.realpath(...))`; refuse a row when any other line (any shelf other than working or tools, or another owner) resolves to the same folder or to a parent of it, when the path contains "..", or when its real path differs from its written one. Fixtures for the twin and the alias.

### S2. Files moved or copied in keep their old dates, so they can go the same night
- Where: tools/retention.py:1115 (age from newest_mtime, file modification times only, 253-272).
- Scenario: a session moves a superseded but still-wanted set into F:/LedgerTools/retired (its name invites it; its line says remove). A move keeps the files' dates, so at 03:30 the folder reads as 56 days unwritten and goes. A zip extracted or a robocopy into a remove-line folder behaves the same. Probe confirmed: a folder made today holding a 30-day-old file is on the remove list.
- Fix: for map rows, take the age from the newest of the files' modification and creation times (st_birthtime on Python 3.12, which the nightly's miniconda runs) and the folders' own dates; whole-folder removal can afford the stricter reading.

### S3. The proposal parser reads "removed ... kept" and "check with him" as remove orders
- Where: tools/retention.py:1128.
- F:/LedgerTools/parler-tts's line, "removed 17 Nov 14:41 by his yes (env and model); designed voices kept", parses as says_remove (it starts with "remove"; "kept" is not "keep"); only the reader check and the protected designed/ folder stop it. Probe: "remove candidate: check with him before any delete" also parses as remove.
- Fix: require the proposal to start with "remove:" or "remove candidate" (not "removed"), and keep when it contains "kept", "his yes", "check with him", "needs his" or "ask".

### S4. A malformed map crashes `run` and `plan` before the limits run, and the night after the limits
- Where: tools/retention.py:1185-1190 (catches only OSError and ValueError) and 415-419 (the same in enforce).
- Probe: `folders` holding a string gives AttributeError, `folders: null` gives TypeError, a numeric path gives AttributeError. `run` then deletes nothing at all, limits included. With the switch on, `nightly` dies after the limits' deletions and before the second census, the night's summary and line.txt, so the morning line goes stale with only errors.log to show it.
- Fix: validate the map (a list of objects, each path a non-empty string) and treat any exception from map_plan as "the map's rules list nothing", printed and written to errors.log.

### S5. The night acts on whatever the working copy holds, reviewed or not
- Where: the LEDGER retention task runs `pythonw tools/retention.py nightly` from C:/Users/Jafar/ledger-local (Task Scheduler, read 17 Nov); enforce 413-414.
- Once live, any uncommitted edit to storage-map.json (RETENTION-STEP2 notes the file had uncommitted changes from elsewhere today) or a proposal changed to "remove: ..." on wip acts that night, unreviewed. The same holds for the switch itself.
- Fix: in nightly and space, act on map rows only when `git status --porcelain production/storage-map.json production/retention.json` is empty; otherwise list them and log why.

## Minor

- M1. tools/retention.py:414-426: map rows skip the busy() check the limits use (Unreal, the runner); a working line under ue-probe or the runner's folders could go while they run. Apply the same skip().
- M2. tools/retention.py:1132: "public" is matched as a substring, so a source such as "not public" counts as refetchable. Add "not public" and "private" to DOUBT_WORDS.
- M3. F:/LedgerTools/latency is both a retention.json limit folder (line 126) and a map remove row ("empty"); removing the root of a limit folder that reports name as the raw-evidence home is untidy. Prefer a "keep: limit covers it" line, as page-frames has.
- M4. Working expiry: the map says 3 days, RULINGS (29 Oct, 16 Nov) says run outputs expire in 14 days. The 17 Nov ruling makes the map the home, but a one-line note in RULINGS or the map saying which wins would stop the next reader stumbling.
- M5. F:/LedgerTools/ai-video and F:/f are kept only by accidental text matches (a test text in tools/needs_you_page.py calling C:/LedgerTools/ai-video his files; "/f" matching widely). Harmless now (both empty), but the reason printed is wrong; fixing B1 and B2 makes it moot.

## What held up under attack
- Dry run: `plan` passes dry=True to delete(), which returns before removing and writes no log; map_plan only reads (git ls-files, the reader text, named_keep's files).
- Switch: map_rules_live needs the JSON value true exactly; absent, false, "true" or 1 all keep the map listing only. retention.json has no mapRulesLive today.
- Junctions: is_link catches both links and junctions; cleanup.remove_tree removes a link without entering it; the self-test's junction case passed.
- Paths: case and forward or back slashes are normalised by norm(); a trailing slash on a line that holds other lines is kept; "F:/" or a path outside the places is refused; the map has no relative or duplicate paths today; the only mapped junction (C:/LedgerTools/parler-tts) is kept as a link.
- Overlap, outer side: a working folder holding any other mapped folder, a protected path, a named run or a backed-up path is kept or refused.
- Time: ages compare file times with time.time(), both UTC, so time zones and summer time do not matter; holds use the local date, as before.
- Floors: the map's 20 and 40 win over retention.json's, and `space` takes them as its defaults.
