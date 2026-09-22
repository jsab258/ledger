line: tools (ledger/verify.py, the footer stamp)
spec: `ledger/.verify-footer` exists so a commit message cannot carry a footer
  from the scrollback. CLAUDE.md: "Green writes ledger/.verify-footer, red
  deletes it, so paste the footer FROM THE FILE, never from the scrollback."
  IT CLOSES STALENESS IN TIME AND NOT IN TREE. The file carries no identity
  for the working tree it walked, so a footer written by a green run is still
  sitting there, readable and plausible, after the tree underneath it changes.

  MEASURED ON THIS SESSION, 2026-09-16 03:35Z, not hypothesised. Verify ran
  green at a bookkeeping commit while `ue-probe/` was clean and wrote a footer
  reading `pathsWalked=3`. A builder then landed 769 lines across three
  `ue-probe/` files. The footer was STILL PRESENT and still said
  `pathsWalked=3`, describing a tree that no longer existed. Running verify
  then returned exit 1 and deleted it, which is the mechanism working, but
  NOTHING RAN IT: a session that had gone straight to `cat ledger/.verify-footer`
  into a commit message would have pasted a green footer over a batch the gate
  refuses, and the commit would have looked exactly like a verified one.

  WHAT THE FOOTER DOES CARRY: `reference = code commit 00bf7189@...`, which is
  the CADENCE REFERENCE and not the working tree. `pathsWalked=3` is the
  closest thing to a tree fingerprint and it is a count, so two different
  three-path trees read identically.

  NOT A HYPOTHETICAL FAILURE MODE FOR THIS PROJECT. The footer exists because
  an unmeasured footer reached a commit message three times, twice after the
  mechanism was introduced. Each of those was staleness in TIME. This is the
  same fault one axis over, and the file being the handle is what makes it
  quiet: a file on disk reads as authoritative in a way a scrollback line does
  not.
acceptance: the footer names the tree it measured, by a fingerprint that
  changes when the tree does (the hash of the pending path list plus each
  path's content hash is one way; `git stash create` or `git write-tree` on a
  temporary index is another, and whichever is chosen must cost nothing on a
  clean tree). A reader or a script can then tell a footer that describes THIS
  tree from one that does not. Both outcomes watched, ACCEPTING FIRST: a
  footer written and immediately read against an unchanged tree matches; a
  footer written, then one byte changed in any pending file, does not. The
  check prints both the stored and the current fingerprint when they differ,
  never a bare mismatch. Under D45 this is a tool that measures the studio: a
  test, no review, no ruling record.
max_sessions: 1
status: READY 2026-09-16, found by catching it rather than by falling into it.
  The stale footer was noticed because the builder's landing was fresh in mind
  and verify was re-run; that is a session remembering, which is precisely
  what the file-as-handle mechanism was built to stop needing. Not urgent, and
  behind 325, 326, 319 and 324, but it sits under every commit this project
  makes.
