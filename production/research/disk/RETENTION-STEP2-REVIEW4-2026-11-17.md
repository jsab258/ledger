# Retention step 2, fourth review (commit 93a05b206), 17 Nov 2026

Reviewer: a fresh helper. Scope: commit 93a05b206 only (tools/retention.py, production/storage-map.json), against items N-R2, M2, M4 and N-R9 of RETENTION-STEP2-REVIEW3-2026-11-17.md.
What was run: `python tools/retention.py --selftest` (passed, 149 checks, 6.6 s); one dry `plan` (docstring line 5: "nothing is deleted"; 19.4 s; map: 134 rows kept, 0 pending, 0 to remove); a read-only script calling link_targets and reached_by_link on the real map; a read-only walk of the repository for junctions. Nothing was deleted, applied or edited apart from this file.

## Verdict: PASS WITH FIXES

All four items are closed. Each self-test would fail without its fix. None of the changes adds a way to delete anything: N-R2, M2 and N-R9 only add reasons to keep or skip, and M4 lengthens an expiry. The fixes listed below are small and none of them blocks. The last one matters before the switch is turned on: the link rule has never run inside a real plan.

## The items

**N-R2: closed.**
- The fix is at tools/retention.py:1559-1612 (LINK_ROOTS, link_targets, reached_by_link) and 1762-1775 (map_plan: links found under every mapped row that is not never-opened, every protected path and LINK_ROOTS; any candidate the link reaches, equal, inside or holding, is kept). The keys folder is in `avoid`, so it is not walked for links.
- Real disk, read-only: 48 links found, including `F:/LedgerTools/played-game\Windows\Voice -> f:\ledgertools\voice-portable`. reached_by_link keeps two tools rows: voice-portable (the review's case) and F:/LedgerTools/parler-tts, which C:/LedgerTools/parler-tts links to. The repository holds 38 links, all inside ue-probe/Content, so LINK_ROOTS covers every link in the repository.
- Test (selftest, the N-R2 block near the end of map_rule_cases): it makes two junctions, one in a lasting folder and one in an unmapped game folder. Both targets are kept, and with LINK_ROOTS emptied the one target becomes removable. Without the fix both targets would be removed, so the test exercises the fix.
- The N4 test was loosened to accept "kept by N-R2" (around 1092-1098). N4's own guard is still checked directly through may_delete, so nothing is lost.

**M2: closed.**
- DOUBT_WORDS adds "not public" and "private" (1389-1390). The words are used at 1705 (working rows) and 1743 (tools: doubt overrides the refetch words, so "not public" cannot count as "public").
- Test: a tools row with the source "private build, not public" goes to his page. A working row with the source "a private copy" is kept "in doubt". Without the fix, the first row would read as refetchable ("public") and be removed, and the second row would also be removed. The test exercises the fix.

**M4: closed.**
- MAP_WORKING_DAYS changes from 3 to 14 (1383). The storage map diff touches only expiry text: 49 rows and the shelf line, 3 days to 14 days, and no other field. RULINGS.md:123 says "run outputs expire in 14 days".
- Test: the selftest reads RULINGS with the regex `run outputs expire in (\d+) days` and checks it equals MAP_WORKING_DAYS. It also checks that every working row's expiry starts with "14 days" and that the retention.json "run outputs" limit (production/retention.json:176) has 14 days. Every one of these checks would fail on the old code. The fixture ages are now MAP_WORKING_DAYS+6, so the rule tests still exercise an expired row.

**N-R9: closed.**
- busy_from (392-404) returns {"unknown"} on a non-zero return code, when the "image name" header is missing, and on OSError or SubprocessError. "unrealeditor" without ".exe" also matches UnrealEditor-Cmd.exe, and seamshift is added under drape. "unknown", "unreal" and "drape" are all in MAP_BUSY (409).
- Test: stubs for a failing tasklist, an empty one, a timeout, UnrealEditor-Cmd, seamshift and a quiet machine. On the old code the failing and empty stubs would read as idle, so the test exercises the fix.

## New faults, ranked (none blocking)

1. **The link walk fails open on an unreadable folder (minor).** link_targets skips any folder it cannot list without a word (`except OSError: continue`, around 1585-1588). If played-game or a game content folder is unreadable for a moment (antivirus, a lock), the junction inside it is never recorded and its target can become removable. This is the same pattern as N-R6. Fix: count the folders that could not be listed, and if any exist, keep every pending row as "links not fully read".
2. **The link rule has never run inside a real plan (minor, the same point as N-R5).** map_plan returns before the link walk when nothing is pending (1762-1763). Today's real plan has nothing pending, so the walk is exercised only by the selftest and by this review's direct call. Have the fresh review of the first real plan with pending rows confirm the N-R2 lines.
3. **The commit's timing claim is wrong (note).** The commit message says "39 links ... in 0.1 s". Measured here: 48 links in 18.8 s, because the walk covers every mapped and protected folder and not only LINK_ROOTS. This is harmless for the nightly run, but the RECIPE and DECISIONS text should give the real figure.
4. **Junction detection depends on Python 3.12 (note).** link_targets finds junctions through DirEntry.is_junction, which exists only from Python 3.12. On an older interpreter, junctions would be walked into as plain folders and not recorded, and the selftest's "the N-R2 junctions were made / link_targets records both" checks would fail, so the gap would show. Falling back to is_link(e.path) would remove the dependency. This session runs Python 3.12.8. The interpreter the nightly task uses was not confirmed (schtasks gave no readable line).
5. **Links from places outside the map and LINK_ROOTS stay invisible (residual, already accepted).** Examples are C:/Games, other repositories, and a folder in the user's profile. This review found no such link reaching a mapped row, but it did not search those places.
6. **Processes not on the busy list (residual).** A python.exe voice server reading voice-portable is not on the list. That folder is now kept by N-R2 anyway.

No new path was found by which anything of Jafar's, anything a build or the game uses, anything the backup holds, or the keys folder could be deleted.
