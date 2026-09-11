# 256. The site links move with publish-glance, after one run prints a served commit

STATUS: READY, 2026-09-10. Ruled by
`game-design/decision-2026-09-10-ruling-the-move-batch-and-the-fleet-left-behind.md`
section 5, finding 6.

## What is wrong

Seven code sites still build links to `https://jsab258.github.io/wc26-picks/`:
`tools/producer-check.py` line 299 (`SITE_ORIGIN`, the register's allowlist),
`tools/runner/cards.py` 222, `tools/runner/executor.py` 190 (`SITE_LINK`),
`tools/runner/telegram-bot.py` 2353, `tools/glance.py` 32, `tools/map-notify.py`
(retired, fixtures), and `tools/producer-check.py` 356 and 1486 (a GitHub
tree link into the archive at the dead branch). The move batch left them on
purpose: github.io is refused at the container's egress proxy, so nobody here
can measure whether either site serves.

## The ruling

Neither a stale-but-live link nor an unverified one goes into a brief. The
old site is frozen at the last publish before the move and would show a page
that does not describe today's message, which is the 2026-09-09 fault by
name. The new site is a 404 until Pages is enabled on `ledger`, which is a
repository setting and therefore Jafar's. Until this item lands, briefs carry
no site link; the register allows zero.

## The deliverable

1. One dispatched run of `publish-glance.yml` on `ledger`, its own `--check`
   step being the entry point that already exists: it prints the served
   commit, or it prints that Pages is not enabled. If not enabled, that is
   the ONE card for Jafar (enable Pages on jsab258/ledger, source GitHub
   Actions) and this item waits on it.
2. In one commit, once a served commit has been printed: the push filter in
   `publish-glance.yml` moves to `main` (queue 254 leaves it alone for this
   reason), and every site above becomes `https://jsab258.github.io/ledger/`
   with the same path; the two tree links become
   `https://github.com/jsab258/ledger/tree/main/production/art/atlas-02/research`.
   `producer-check.py --selftest` and the register fixtures move with the
   constant.

## Done looks like

`publish-glance` green on a push to `main`, its check step quoting a served
commit that is an ancestor of HEAD, and `grep -rn 'github.io/wc26-picks'
tools/` at 0 over the files scanned.

## Dependencies and risk

Jafar's setting, if the first run says so. Risk: flipping the links before
the served commit is printed, which puts a 404 on his phone.

## Amended 2026-09-11 by the director, section 5

TWO ADDITIONS, and both exist because a printed fact beats a typed one.

1. PROVENANCE. When `production/site-served.txt` gains a sha, its `printedBy=`
   names the SHORT SHA of the CI commit carrying the `publish-glance` verdict
   file. `ledger/verify.py` (which already has `_git`) checks that the commit
   exists AND that a file in it carries `servedCommit=<the same sha>`. A marker
   whose provenance cannot be found is A RED GATE, not a warning. This is what
   stops a sha typed by a session that never watched it printed.
2. The done line's `grep -rn 'github.io/wc26-picks' tools/` at 0 becomes "at 0
   OUTSIDE `ARCHIVE_ORIGIN` and the rejecting fixtures that name it". Amendment
   A1 keeps that string on purpose, because a rejecting fixture must name what
   it rejects.

Ruling: game-design/decision-2026-09-11-ruling-the-link-floor-marker-batch-and-the-answer-already-sent.md
