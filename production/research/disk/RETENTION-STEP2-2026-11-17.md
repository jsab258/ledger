# Retention step 2: the storage map's expiry rules, 17 November 2026 (advisor 196)

Method researched: production/storage-map.json (its expiry rules and 132 folder lines), production/retention.json, RULINGS.md "Disk, git and backup" (17 Nov, 29 Oct), INVENTORY-2026-11-17.md and INVENTORY-F-2026-11-17.md; read 17 Nov 15:50 to 16:20.

Nothing was removed. The self-test ran on temporary folders only; `plan` was run once, read-only, at 16:20 (local).

## What changed in tools/retention.py
- `map_plan` reads each mapped folder's shelf and applies the map's rules: working, newest file over 3 days old; tools, no file written for 14 days. A folder goes only if no tool in the repository names its path, the map's own line names no existing reader file, and the map's line proposes removal ("remove...", without "keep" or "shrink"). A tools folder that is unused and not known to be refetchable (source unknown, needs a sign-in, unverified) becomes a "his page" candidate and is never removed.
- Never removed by the map: the lasting, side-session, build-cache and installed-program shelves; an owner other than LEDGER or Claude; a line naming a side session; a line marked backed up; a folder holding another mapped folder; a mapped link; anything delete() refuses (outside retention.json's places, protected, in the Dropbox backup list, tracked by git, held, named by a report). Folders not on the map are never touched by these rules.
- `plan` prints the limits' rows, then the map's rows, the refused, the his-page candidates, the expired folders the map keeps (with the reason), and each drive against its floor (the map's floors, F: 20, C: 40; `space` now takes its default needs from them).
- Switch: `run`, `nightly` and `space` remove the map's rows only once production/retention.json sets `"mapRulesLive": true`. It is absent today, so the map's rules are listed only. Reason: the LEDGER retention task runs tools/retention.py from this working copy every night, so an uncommitted, unreviewed change would otherwise act tonight. When the switch is on, `run` removes only the map's `remove` list, each through the same delete() and its log.

## Self-test
`python tools/retention.py --selftest`: passed. 23 earlier checks plus 24 new map checks (several run in loops over the fixtures): each shelf's rule, an in-date working and tools folder kept, a map line saying keep or shrink, a reader named in the repository or in the map's line, a side session's work, backed up, his owner, protected, held, outside the places, a folder holding a mapped folder, an unmapped old folder on no list, his-page items never removed, nothing removed while the switch is off, the dry plan equal to the remove list, the live run removing exactly that list (three log lines), a junction inside a working folder removed as one link with its target intact, and the floors (the map's beating retention.json's, below-floor before and after). A mutation run (working days set to 30, refetch words emptied) made the map checks fail, so they bite.

## The plan's output (17 Nov 16:20, read-only)
Total: 0.78 GB in 18 places: retention.json limits 0.51 GB (4 rows), map rules 0.26 GB (14 rows, not live). His page: 2.25 GB in 1. Floors: C: 50.6 GB free (floor 40), F: 46.1 GB free (floor 20), both above.

Map rules, would remove (not live):

| Path | GB | Rule |
|---|--:|---|
| F:/LedgerTools/drapestudio-test-2026-11-11 | 0.13 | working 3 days; superseded by -final |
| F:/LedgerTools/dotnet10-download | 0.08 | tools 14 days unused, refetchable (public Microsoft download) |
| F:/LedgerTools/retired | 0.04 | working 3 days; superseded imagegen set |
| F:/LedgerTools/review-faces-2026-09-26 | 0.01 | working 3 days |
| F:/LedgerTools/cleanup-2026-09-26, game-voice, game-voice2, latency, playtest, pso-record, review-voice-2026-09-25, review-voice-2026-09-26, selfcheck-voice-2026-09-26, south-quay-work | 0.00 each | working 3 days; empty or tiny, no reader |

Refused (outside retention.json's places, so delete() will not act): F:/LedgerToolsscratchtalk-fast, F:/town-bench, F:/town-bisect (0.01 GB together). Kept by the reader check: F:/f (the text "/f" matches too widely; safe, but the stray stays) and F:/LedgerTools/ai-video.

His page (never removed): F:/LedgerTools/voice-env-export, 2.25 GB, unused 22 days, source unknown (already protected in retention.json).

Limits, would remove: C:/LedgerTools/cargo-target/drapestudio 0.51 GB (Rust caches, 3 days), one empty crash folder, two tiny cargo files. 1,343 limit rows are refused as protected, almost all inside cargo-target/kiln/release (named in a report, namedKeep); that is existing behaviour and only noise in the output.

## Points for the session and reviewer
- The 17 old scratch folders proposed for removal: 12 are on the remove list above, 3 are refused because they sit outside retention.json's places, and 2 are kept by the reader check (F:/f, too short a name; F:/LedgerTools/ai-video: the match is a test text in tools/needs_you_page.py about C:/LedgerTools/ai-video as his files, since the drive is left out of the match; keeping it is the safe side). Adding the 3 to places is a policy change left to the session. The two own leftovers (drapestudio-test-2026-11-11, dotnet10-download) are on the list.
- F:/LedgerTools/pylib (1.05 GB) is kept because the map's line names tools/checkers/measure_checkers.py. That checker adds F:\LedgerTools\checkers\pkgs to its path (line 43), not pylib, and no file in tools/ names pylib, so the summary's "the local checker reads it" looks unfounded (unverified: a path set outside the repository was not checked beyond PYTHONPATH, which is empty). Correcting the map's line would make pylib a remove row (public, PyPI).
- The map has no owner field on any of its 132 lines; the rule relies on the map's header ("nothing of his is ever on the map"). An explicit owner on each line would make the guard checkable.
- mh-dress's Saved, Intermediate and DerivedDataCache (0.30 GB, the inventory's own leftovers) are inside a lasting folder, so the map never removes them; they need their own working lines in the map.
- Not judged by code: "once its numbers are recorded" and "a superseded review picture keeps its preview only". An expired folder the map keeps is listed so the map can be corrected.
- Readers are found by path text only (as in the inventory); a path built from pieces is missed. Tools are read, not written, so file dates alone cannot show a tool is unused; the reader check stands in for use.
- production/storage-map.json had uncommitted changes from elsewhere during this work; the plan used the file as it stood at 16:20.
