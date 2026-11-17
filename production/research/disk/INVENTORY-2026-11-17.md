# LEDGER storage inventory, 17 November 2026 (advisor 196)

Method researched: INVENTORY-F-2026-11-17.md and INVENTORY-C-2026-11-17.md (two read-only helpers, 13:00 to 13:15, sizes measured on disk, readers found by searching the repository for each path), F-USAGE-2026-11-16.md before them. The map they feed: production/storage-map.json (81 folders).

## The drives
- F: 119.5 GB, 84.4 used, 35.0 free (floor 20). LEDGER's rows: lasting 43.2, tools 22.7, working 20.1. Nothing on F: is not LEDGER's but vuze (0 MB read, never opened), the recycle bin and system folders.
- C: 52.5 GB free (floor 40, so 12.5 GB of room). LEDGER's folders on C: about 185 GB: build caches 51.3, installed programs 53.8 (Unreal 5.8 alone 43.1), working 37.5, tools 31.5, lasting 11.0. The Dropbox backup (20 GB) sits on C: inside the Dropbox folder.

## Why F: kept running short
Folders that arrived as protected were never reviewed: the old Parler voice (5.5 GB on F: and 3.3 GB of its model on C:), the OpenSLR 83 recordings (3.8), a voice environment export with no reader (2.3), the study extracts (1.8). Cleaning reached only the runs' own leftovers. Since 16 Nov the clear-out freed 12.6 GB (gate/new 13.2 to 5.4; the animation sample copy gone).

## Shelves proposed (F:, adding up to the drive)
lasting 44.5 (today 43.2), tools 25 (22.7), working 20 (20.1), spare 10, floor 20. The lasting shelf is larger than advisor 196's starting 35 GB because mh-dress (21.2 GB, the approved cast's MetaHumans: advisor 197's correction) is lasting.

## The one remove list (his page, one yes; carried out by retention.py)
| What | GB | Why it can go | Back from |
|---|--:|---|---|
| The old Parler voice program and its model (F: parler-tts, C: Hugging Face copy) | 8.8 | Sheila's voice is Pocket p267 since 27 Oct; only an old take-maker reads it | public: Hugging Face and pip, no sign-in |
| OpenSLR 83 accent recordings (F: slr83) | 3.8 | no tool reads it | public download, no sign-in |
| Study extracts of KCD2 and Mafia (F: aaa-study extracts) | 1.8 | their numbers are recorded (CLAUDE.md: extracts deleted once recorded) | re-extracted from his installed games, no sign-in |
Total 14.4 GB. Kept although no reader was found: the voice environment export (2.3 GB; it may not be rebuildable), F: lab (1.0 GB; may hold unique work), the side sessions' checkouts on C: (ledger-talk, ledger-lab, ledger-exec, 6.9 GB; never this session's to touch). Kept because something reads them: pylib (the local checker), sw-scratch (a shop front's wear spec), garmentcode's environment (the breadth patterns).

## Own leftovers (RULINGS 29 Oct, no page item)
drapestudio-test folders 0.16 and dotnet10-download 0.08 GB on F:, mh-dress's Saved, Intermediate and DerivedDataCache 0.30 GB: through retention.py once its map rules land (18 Nov).

## Not measured, open
- Readers were found by path text only; a script building a path from pieces would be missed.
- The F: rows add to 86.0 GB against 84.4 used (links counted twice, most likely; unverified).
- Unknown sources: slr83's exact link, voice-env-export's requirements, chatterbox weights, imagegen models.
