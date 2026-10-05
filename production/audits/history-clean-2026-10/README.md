# The history cleaning of 5 October 2026

Phase 0, item 0.7. His orders of 4 and 5 October: clean the history while the sessions are stopped, after he hears the plan and all it touches; then, the new repository ready (the old one renamed to jsab258/ledger-archive-2026-10 and made private, a new empty public jsab258/ledger), upload the cleaned history with main, wip and the September map's branch, and keep the map of old to new commit fingerprints as a small text file. Plan, rehearsal and measurements: production/research/git-history-clean-2026-10-04.md.

## What was removed, from every commit of every branch

- Every picture and film under production/d1-probe (the build machine's test frames, committed on every run from 3 September to 3 October; 21,704 versions, 29.9 GB stored).
- The eight frames of other games: five GTA V screenshots (game-design/reference/gta5_*), two KCD2 frames (production/reference/kcd2-*) and one composite (production/art/atlas-01/street/terrace-front-street-hook.png).

Everything else is unchanged: each branch's latest files were compared with the original's and are identical apart from those (main 8,284 to 8,176 files, wip 8,551 to 8,443, art/atlas-01 4,674 to 4,658). The history went from 30.8 GB to 3.2 GB. Tool: git-filter-repo 2.47.0 (MIT).

## The map

commit-map.txt: one line per commit of the old history, its old fingerprint then its new one (4,556 commits). A commit cited by its old fingerprint anywhere in the records (DECISIONS.md and the rest keep them as written) is found here, and in the private archive. tools/push_guard.py reads it before every push and refuses any commit of the old history.

## Where the old history is

- The private archive on GitHub, jsab258/ledger-archive-2026-10, with every old branch and its 12 pull requests (which still hold 29.6 GB of the old pictures and the eight frames; whether to ask GitHub to remove them is his to decide later).
- A safety copy on this PC, C:\LedgerTools\history-safety-2026-10-05.git (protected in production/retention.json), kept until he confirms everything works.

## Not carried over

The 68 other branches stay in the archive only; what they held that existed nowhere else was saved first (production/archive/branches-2026-10-05). The two Unity secrets are not re-entered: their workflows are retired (production/archive/workflows-retired-2026-10-05).
