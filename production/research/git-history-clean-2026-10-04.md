# Cleaning the git history: the plan (4 October 2026, for his go-ahead; nothing done yet)

His order, 4 October: "clean it, by the safest method you can find, while the sessions are stopped. Tell me the plan and everything it touches, the working folders, the build machine and the cloud branches, before doing it."

## What is in the history (measured today on this PC)

- 30.8 GB stored. 29.9 GB of it is the build machine's test pictures under production/d1-probe, each picture committed about 276 times (3 September to 3 October; stopped since).
- The other games' frames: five GTA V screenshots (game-design/reference/gta5_*) and two KCD2 frames (production/reference/kcd2-*), plus one composite (production/art/atlas-01/street/terrace-front-street-hook.png). Out of the working tree since P14; still in the history.
- Everything else together is about 3 GB (the Unity-era assets, the street, people, previews), which stays.

## Why not simply rewrite the history on GitHub

GitHub's own guide (docs.github.com, "Removing sensitive data from a repository", read today): rewrite with git-filter-repo 2.47 or later, force-push every branch, then ask GitHub Support to remove the old commits that pull requests still hold, because pull-request references are read-only to us. GitHub says Support helps only with secrets ("will only assist in the removal of sensitive data"), not with size.

Our repository has 12 pull requests (15 references), and every one of them still reaches about 299 of the picture commits (checked today). So a rewrite in place would leave the 30 GB, and the other games' frames, reachable on GitHub through those pull requests. It would not fix what it is for.

## The plan (recommended): a new repository with the cleaned history

1. **Before:** he stops the town and clothing sessions; every session's work committed and pushed (nothing half-pushed); the build machine idle; not between 02:20 and 03:30 (the nightly walk). git-filter-repo installed (from PyPI) after its licence is read and recorded in the allowlist; the three local stashes saved as patch files.
2. **Copy, never the original:** a mirror copy of the repository made beside it on C: (hard links, so it takes almost no room), all 70 GitHub branches fetched into it first. The original stays untouched throughout.
3. **Clean the copy:** remove every picture (png, gif, jpg, webp, mp4) under production/d1-probe and the eight other-games frames, from every commit of every branch; the text files there stay.
4. **Check:** every branch's latest files identical to today's except the removed pictures; the checks (ci-checks) pass on the cleaned main; the size about 3 GB.
5. **His part, about ten minutes on github.com (only he may sign in):** rename the old repository to ledger-archive-2026-10 and make it private (the full old history kept there, nothing lost, nothing public); create a new empty public repository named ledger; then, on the new one, re-enter the two Unity secrets and add the build machine as a runner (GitHub shows one command with a one-time token; he runs it, since I may not handle tokens).
6. **Push:** all 70 branches (main, town, clothes, pc-inbox, pc-results, 13 claude/* cloud branches, the research/* and art branches) to the new repository; about 3 GB of upload.
7. **Re-point every copy:** the one shared repository behind the four working folders (C:\Users\Jafar\ledger-local for the builder, C:\Users\Jafar\ledger-town, C:\Users\Jafar\ledger-clothes, F:\LedgerTools\town-scratch\ci-tree) points at the new repository, each folder moved onto its cleaned branch; local-only branches (shops-wip-2026-10-03, town-wall, town-review-1oct, town-wip-backup, wip/grounding-word-list) cleaned the same way and kept local.
8. **The build machine** (C:\actions-runner-ledger): registered to the new repository (step 5); its checkout (9.1 GB) made fresh from the new repository on its first run; one push then proves the Core tests and the Unreal build.
9. **Cloud sessions:** new ones clone the new repository; the claude/* branches arrive with it. Any cloud session still running on the old history is ended first (none should be).
10. **After his yes that all works (a day or so):** the old objects pruned from this PC, freeing about 28 GB on C:. The private archive stays until he says to delete it.

## What it touches, in one list

- Working folders: ledger-local, ledger-town, ledger-clothes, town-scratch\ci-tree (one shared repository).
- The build machine: its registration and its checkout.
- GitHub: the old repository renamed and made private; a new public one with all 70 branches; the 12 pull requests and 3 open issues stay on the archive (the issues can be moved across).
- Not touched: the Dropbox backup (it copies files, not git history), F:\LedgerTools, his own files.
- Every commit's number changes; DECISIONS.md and other notes that cite old numbers keep them as text (they then point into the archive).

## Time and risk

About an hour of work plus the upload, at a quiet moment. Nothing is deleted: the old history stays whole in the private archive and on this PC until he says otherwise. The one-way step is making the new repository public, which shows only the cleaned history.

## The other way (not recommended)

Rewrite in place and ask GitHub Support: same work on our side, no new repository or runner registration, but by GitHub's stated policy Support is unlikely to act, so the 30 GB and the other games' frames would likely stay reachable through the pull requests.

## Update, 5 October (phase 0, item 0.7): what changed since

- **Measured again:** 30.8 GB stored; 15 pull-request references still reach the old pictures; four workflows still read the two Unity secrets, so step 5 stands.
- **One session now.** The town's and clothing's folders (ledger-town, ledger-clothes) are retired rather than re-pointed: their branches' work is in main (the sweep, production/audits/sweep-2026-10-05/SWEEP.md), and their worktrees are clean. Two of their app sessions are still open (Ledger Town, waiting; Ledger Clothes, idle): closed before the cleaning.
- **Fewer branches.** If he answers yes on Monday's Sweep page, the 68 old branches become archive tags first; the tags are cleaned with everything else and pushed with the branches.
- **Quiet hours** now also avoid the nightly jobs: 02:20 to 03:30 (the walk), 04:30 to 05:45 (retention, the page answers' read-back, the morning pictures).
- **The tool:** git-filter-repo 2.47.0 (4 December 2024), MIT for the tool itself (its test harness GPL-2, never run here), by Elijah Newren (pypi.org and the project's COPYING, read today); a development tool, never shipped; recorded in DECISIONS.md.
- **Rehearsed first on a copy:** steps 2 to 4 run on a throwaway mirror copy before his go, touching nothing of his, the working folders, the build machine or GitHub; the result (size, branches, checks) goes to him with the question.
- **The rehearsal, 5 October 12:21 to 12:23,** on a throwaway mirror copy (scratch on C:, hard links): git-filter-repo removed every picture under production/d1-probe and the eight other-games frames from all 84 references in 2 seconds, and the repack took 46 seconds. The copy went from 30.77 GB to 3.19 GB. Every branch's latest files matched the original's apart from the removed pictures; the one difference on main and wip was a file committed after the copy was taken. Found: a local-only branch (wip/grounding-word-list) clashes with the GitHub branch wip, so local-only branches go under local-only/ for the cleaning; and main's own files still hold 108 stale probe pictures (130 MB, from before the build machine stopped committing them on 3 October), which the cleaning removes from the current files too. No check reads them; two old analysis tools (frame-shadow-probe.py, road-brightness.py) name them as defaults and take any picture as an argument.
