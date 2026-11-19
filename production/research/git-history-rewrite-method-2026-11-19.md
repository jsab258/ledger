# Git history rewrite: method reading (read 19 Nov 2026)

Reading only. No recommendation or decision. Pages were fetched through a summarising reader, not seen raw; wording marked "quoted" is the reader's quotation of the page. Coordinator's correction applied: the repository (jsab258/ledger) is PUBLIC, and one filter-repo rewrite (2.47.0) was already done on 5 Oct 2026.

## Questions
1. GitHub's recommended method for removing files from history.
2. git filter-repo: paths, remotes, refs, tags, stashes, fresh-clone check.
3. After a force-push, for a public repository: what GitHub keeps; Support purge; any private difference.
4. Other clones, the runner's work folder, open pull requests.
5. Size recompute and garbage collection after a rewrite.
6. Limits and gotchas with LFS and large files.

## Answers

**1. GitHub's method** (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository, read 19 Nov 2026)
- Tool: git-filter-repo 2.47 or later (provides `--sensitive-data-removal`). Step 0: rotate any credential first.
- Steps: fresh clone; `git-filter-repo --sensitive-data-removal --invert-paths --path PATH` (one `--path` per old/renamed path); verify; count affected PRs with `grep -c '^refs/pull/.*/head$' .git/filter-repo/changed-refs`; `git push --force --mirror origin`; save the tool's output ("First Changed Commit(s)", LFS orphan note).
- Warnings: irreversible after the push; pushes to `refs/pull/*` fail (read-only); branch protection must be lifted for the push; every commit from the first change gets a new hash; commit/tag signatures are removed; `git pull` then `git push` from an old clone re-introduces the data; open PR comments on old diffs may be lost (page advises merge or close open PRs first); clones holding old history make the removed data easy to find.

**2. git filter-repo** (https://raw.githubusercontent.com/newren/git-filter-repo/main/Documentation/git-filter-repo.txt and .../README.md, read 19 Nov 2026)
- `--path` (union of several) selects paths; `--invert-paths` keeps everything matching none of them, i.e. removes them. Renames are not followed (list old and new paths). `--paths-from-file FILE`: one directive per line; `literal:` (default), `glob:`, `regex:` prefixes; `==>` marks a rename; blank and `#` lines ignored.
- Fresh-clone check: aborts if the repo does not look like a fresh clone; `--force` overrides; the manual calls it a proxy check with false positives and negatives and the rewrite irreversible. Later runs skip it once `.git/filter-repo/already_ran` exists.
- Removes the `origin` remote on purpose, so rewritten history is not pushed back by accident; `git remote add origin URL` restores it.
- Rewrites refs and tags (tags already downloaded elsewhere are not updated by a normal `--tags` fetch). Stashes are rewritten. `--replace-refs` default `update-no-add`. Runs reflog expiry and gc/repack afterwards unless overridden.
- With `--sensitive-data-removal`: writes `original_lfs_objects` and `orphaned_lfs_objects` under `.git/filter-repo/`.

**3. After the force-push, public repository** (GitHub page in 1; forks page https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/what-happens-to-forks-when-a-repository-is-deleted-or-changes-visibility; both read 19 Nov 2026)
- The sensitive-data page never mentions public or private; it gives one procedure.
- Cached views: commit SHAs can still show content on GitHub; only Support removes them.
- `refs/pull/*`: stay until Support deletes or dereferences the PRs (dereferenced PRs keep text, lose affected diffs).
- Forks: public forks stay public and share Git data with the network; quoted: "Commits pushed to any repository in a network can be accessible from other repositories in that network"; deleting a fork does not remove its data from the network. The sensitive-data page: a commit in any fork stays accessible there; fork owners must be asked to remove it; GitHub gives no contact details.
- Support is asked with: owner/repo, number of affected PRs, First Changed Commit(s), LFS orphan note. It proceeds only if non-PR refs are clean and no fork references the data, and only for sensitive data not mitigated by rotation. It then runs server garbage collection and removes cached views, PR data and LFS objects.
- Dangling commits reachable by SHA: not discussed on the page (unverified); cached views, PR refs and forks are the routes it names.
- Private repository: no separate guidance; whether Support handling differs is unverified.
- Third parties may already hold clones of a public repository; the sources give no way to find them (unverified).
- Effect of the 5 Oct rewrite on cached views or PR refs: not examined.

**4. Other clones, runner, PRs** (git-filter-repo manual; GitHub page; read 19 Nov 2026)
- Manual: others should not re-run the same filter (different hashes, duplicate history). Instead: delete tags, `git fetch --prune --tags`, rebase local work onto the new history, `git reflog expire --expire=now --all`, `git gc --prune=now`. Check: `git cat-file -t <first changed commit>` giving a fatal error means gone. Expiring reflogs also drops stash entries.
- GitHub: collaborators must rebase, not merge. Open PRs: see 1 and 3.
- A self-hosted runner's work folder: neither source mentions it (unverified); it is an ordinary clone.

**5. Size and gc**
- The GitHub page says Support performs server garbage collection; no timing and no automatic recompute stated (unverified). Local gc: see 2.

**6. LFS and large files**
- https://docs.github.com/en/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage (read 19 Nov 2026): history removal or editing .gitattributes does not delete LFS objects; they keep counting toward LFS quota; the only stated way to remove them is delete and recreate the repository, otherwise contact Support (deleting also deletes issues, stars, forks).
- https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github (read 19 Nov 2026): warning above 50 MiB; blocked above 100 MiB; under 1 GB recommended, under 5 GB strongly advised; LFS maximum depends on plan.
- https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits (read 19 Nov 2026): 10 GB on-disk recommended; push size enforced at 2 GB; 5,000 branches recommended; 6 pushes per minute. Force pushes not mentioned.
- Whether a `--mirror` push of a large history meets the 2 GB limit: inference, unverified.

## Unverified
- Dangling-commit reachability by SHA after a force-push.
- Private-repository differences.
- Runner work-folder behaviour after a rewrite.
- Whether and when GitHub recomputes size; gc duration.
- Whether the 2 GB push limit applies to a rewrite push.
- Exact filter-repo wording (reader summaries, not raw text).

## Unreached
- The filter-repo user manual HTML (htmlpreview link) and INSTALL.md.
- GitHub Docs pages on pull-request refs and self-hosted runner behaviour (not requested).
- Git's own documentation (git-gc, git-reflog); not read.
