line: docs (the third of the week's three conventions)
spec: Jafar, 2026-09-21 ("Three conventions... "): "anything that names a
  file links to it: we carry 2,135 backticked paths against 16 markdown
  links across 861 files, so nothing here can be traversed, by a tool or
  by a person."

  MY OWN READING, taken 2026-09-21 for this item rather than his figures
  quoted ahead of it (CLAUDE.md rule 1, checked in the same turn it is
  stated), all three via this session's Grep tool (a ripgrep wrapper):

      pattern \]\([^)]+\) glob *.md, count mode
      -> 206 occurrences across 45 files. Every one sampled (15 read in
      full with -o) points at an external https:// URL, GitHub blob views
      and GitHub Pages links inside briefs and outbox messages. A second
      pass restricted to \]\(https?:// also returns 206 across the same
      45 files, so by this pattern ZERO markdown links in this corpus
      point at a local repository file.

      pattern `[^`(whitespace)]+/[^`(whitespace)]+` (a backtick, a token
      containing a slash, a closing backtick) glob *.md, count mode
      -> 5,560 occurrences across 433 files.

      Glob **/*.md over the whole tree -> 869 files total.

  These numbers do not match his, 2,135 backticked paths, 16 markdown
  links, 861 files, and are not expected to: the corpus has moved since
  his count and his exact matching pattern was not given. Both readings
  agree on the SHAPE of the finding, backticked paths heavily outnumber
  markdown links, by roughly two orders of magnitude either way, even
  though the exact counts differ. State both his figures and this item's
  fresh re-measurement, with the exact command for each, rather than
  silently reconciling them into one number.

  THE CONVENTION ITSELF, "anything that names a file links to it," is not
  yet written anywhere as a rule; this item's job is the measured sweep
  Jafar asks for, "re-measure those three numbers yourself," not to
  rewrite 2,135 or more backticked paths into links by hand, which is far
  outside one session. Confirm at pickup time whether
  ledger-v2/studio-v2/operations.md, named in production/NOW.md as where
  the convention itself is recorded, already states the rule; if it does
  not yet, that is silent in this item, per CLAUDE.md rule 11, and is
  named as a gap rather than filled in here.
acceptance: the three counts, markdown links, backticked file-shaped
  paths, and total files, are freshly re-measured with the exact command
  printed for each, distinct from and compared against his 2,135, 16 and
  861; the sample check of what the markdown-link matches actually point
  to, local file versus external URL, is stated with a count, how many of
  the sample were external; and the item states plainly whether it
  rewrote any files, expected answer no, this is a measurement and not the
  rewrite, so a reader cannot mistake a count for a completed convention
max_sessions: 1
status: READY 2026-09-21, filed as studio-third work, taken at a
  checkpoint. Not gated on the visual slice or the measurements. This is
  this week's work.
