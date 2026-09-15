# 256. The site links move with publish-glance, after one run prints a served commit

STATUS: STEP 2 LANDED 2026-09-15, section at the bottom. STEP 1 SATISFIED
2026-09-13T04:08Z, quoted below. The trigger moved
under the morning ruling, so publish-glance fires on this push for the first
time on this repository; step 1 is satisfied by what that run prints
(servedCommit, or the Pages refusal, whichever it is), and the resident quotes
it here once read. THE LINKS HAVE NOT MOVED and are this item. Step 2 next., 2026-09-10. Ruled by
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

Ruled 2026-09-15 05:43Z: the count is THREE and the three are named
(producer-check.py:671, ARCHIVE_ORIGIN; map-notify.py:40 and :44, a dated
transcript of a measurement taken against the archive on 2026-09-06 and the
sentence saying so). The carve-out gains the clause: a dated transcript of a
measurement stays, provided the same lines say it is a transcript and name the
date. A fourth hit is a finding, not a fourth clause.

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

   SUPERSEDED 2026-09-15 (ruling of 05:43Z, section 5): the workflow commits
   nothing, so there is no CI commit to name; the check is ancestry and
   origin, as "The provenance amendment described a workflow that does not
   exist" under Step 2 records. The intent, a printed fact beating a typed
   one, is unchanged.
2. The done line's `grep -rn 'github.io/wc26-picks' tools/` at 0 becomes "at 0
   OUTSIDE `ARCHIVE_ORIGIN` and the rejecting fixtures that name it". Amendment
   A1 keeps that string on purpose, because a rejecting fixture must name what
   it rejects.

Ruling: game-design/decision-2026-09-11-ruling-the-link-floor-marker-batch-and-the-answer-already-sent.md

## Step 1, satisfied 2026-09-13T04:08Z

What the run actually printed, rather than a summary of it:

    servedCommit  dc04da736cbdbd3fffc119d1ff47801ec7706204
    servedUrl     https://jsab258.github.io/ledger/
    glance        pageHttp=200 pageStampCommit=dc04da73.. expectCommit=dc04da73..
    printedBy     publish-glance run 34737101663, job 103670366299, step
                  "REQUEST THE PUBLISHED PAGES AND READ WHAT CAME BACK"
    servedAt      2026-09-13T04:08:07Z

`production/site-served.txt` IS NOT UPDATED BY THIS AND THAT IS DELIBERATE.
That file's own rule is that the served line moves in the SAME commit that
moves `SITE_ORIGIN` off the archive, and `tools/producer-check.py:310` still
reads `https://jsab258.github.io/wc26-picks/`. There is a named guard for
exactly the half-move, `marker-names-served-commit-but-SITE_ORIGIN-is-the-archive`,
so writing the marker alone would turn the floor back on and make the STALE
link mandatory. Both move together in queue 259 or neither moves.

MEASURED CONSEQUENCE, 2026-09-13T04:18Z: the resident told the Producer mid-turn
that it could carry the link, then read `site_page()` and found it matches whole
URLs against `SITE_ORIGIN`, so a link to the live site returns None and the
message would have bounced on a `linkdest` refusal. Retracted before it shipped.
THE PAGE BEING LIVE AND THE CHECKER KNOWING WHERE THE SITE LIVES ARE TWO
DIFFERENT FACTS, and only the first changed this morning. Step 2 is the links.

## Step 2, landed 2026-09-15: the links moved

### The line numbers in "What is wrong" were stale, and one was never right

Found BY NAME, not by number. `SITE_ORIGIN` is `tools/producer-check.py:548`
as Jafar said, not 299 as this item said; 299 is inside an unrelated comment.
The others: `cards.py:222` (this item was right), `executor.py:198` (not 190),
`telegram-bot.py:2887` (not 2353), `glance.py:32` (right), `map-notify.py` nine
fixture sites. The two tree links are `producer-check.py:734` (RULED_LINKS) and
`:1996` (the RULED_DIGEST fixture body), not 356 and 1486. A line number in a
document is a claim that decays; every site here was located by grepping the
string and the constant name.

### What moved, and the one thing that did not

Seven sites plus the two tree links moved to `https://jsab258.github.io/ledger/`
and `https://github.com/jsab258/ledger/tree/main/production/art/atlas-02/research`.
The path under the new tree URL was MEASURED before it was typed: `git ls-tree
-r --name-only HEAD -- production/art/atlas-02/research` returns five files.

THE DONE LINE, `grep -rn 'github.io/wc26-picks' tools/`, IS 3 AND NOT 0, and
every one is named rather than counted away:

    tools/producer-check.py:671  ARCHIVE_ORIGIN, carved out by amendment A2
    tools/map-notify.py:40       a TRANSCRIPT of a curl run on 2026-09-06
    tools/map-notify.py:44       the comment explaining why line 40 stays

Line 40 is the recorded output of a request made against the origin that was
live that day (`curl: (56) CONNECT tunnel failed, response 403 http=000`).
Rewriting it would claim a measurement nobody took. It is the same case as a
rejecting fixture naming what it rejects, and the done line should say so.

`RULED_DIGEST` no longer carries its own copy of the URL: it is built from
`RULED_LINKS[0][0]`, so the two can never drift again.

### The push filter was already on main

`publish-glance.yml` reads `push: branches: [main]` and has since queue 269 on
2026-09-13. Nothing to do; this part of deliverable 2 was already done.

### `pagesEnableHttp: 403` IS NOT A FAILURE

The workflow's optional PUT to set the Pages build source is refused for lack
of permission on the job token. Pages is already configured and serving, which
is what the check step measures. The step records the refusal rather than
swallowing it; a recorded refusal is the ruled ending. Do not chase it.

### The served commit, and why it is not the one this item was handed

Run 26 (id 34928226785, ada1535b) is the reading the director watched. It was
SUPERSEDED while this item was being built: publish-glance rides every push and
a commit landed at 05:18:30Z. Re-queried rather than assumed:

    run 27, id 34932214186, head_sha 5a8ef789dc1f5044052abd496667352c752b1b9c,
    branch main, conclusion success, completed 2026-09-15T05:21:01Z,
    job `publish` id 104262618410, step 13 "REQUEST THE PUBLISHED PAGES AND
    READ WHAT CAME BACK" success, 05:20:55Z to 05:20:56Z.

NOBODY IN THE CONTAINER HAS LOADED THE PAGE and this item does not claim
anyone has. The egress proxy refuses github.io, and the raw job log redirects
to a blob host it also refuses, so the step's CONCLUSION from the Actions API
is the strongest reading available here. That conclusion is the assertion: the
step runs under `set -eu` and calls `publish-glance.py --check` on all four
published pages, and `check()` exits non-zero on STALE or a secret leak.

### The provenance amendment described a workflow that does not exist

Amendment 1 of 2026-09-11 says `printedBy=` names the short sha of "the CI
commit carrying the publish-glance verdict file", and that `ledger/verify.py`
check that commit exists and that a file in it carries `servedCommit=<the same
sha>`. `.github/workflows/publish-glance.yml` was read on 2026-09-15: it runs
with `permissions: contents: read`, has no `git add`, `git commit` or `git
push` in any step, and writes its verdict to `$GITHUB_STEP_SUMMARY` and
nowhere else. THERE IS NO CI COMMIT TO NAME. Implemented literally the guard
could never pass, which is the validator-nothing-survives failure this project
has already paid for.

What `ledger/verify.py:served_marker_provenance()` checks instead, all offline:
the sha is a whole 40 hex; that object exists here and is a commit; it is an
ANCESTOR of HEAD (never equality, because the served commit is routinely behind
by the time anything reads the marker); `servedUrl` is the string
`producer-check.py` actually sets `SITE_ORIGIN` to; `printedBy` names a
publish-glance run with an id. RED, not a warning, as the amendment ruled.

STRONGER THAN THE AMENDMENT IN ONE WAY: `printedBy` points at the run, the job
and the step that PRINTED, rather than at a commit that might carry a file.
WEAKER IN ANOTHER: nothing here re-reads the run, so git refutes an invented or
foreign sha but not a plausible one. The run id is what a human re-queries.

### The consequence nobody had measured: 40 of 42 sent messages went red

Moving the constant and turning the floor on in one commit re-grades every
message already in the tree. A ladder on the live tree, one vantage, one run,
one contributor toggled per rung:

    rung A  origin=archive  floor off (that morning)    0 of 42 failing
    rung B  origin=ledger   floor off                  19 of 42 failing
    rung C  origin=archive  floor ON                   20 of 42 failing
    rung D  origin=ledger   floor ON                   39 of 42 failing

and 40 once RULED_LINKS moved too, taking the atlas-02 digest with it. Twenty
messages linked the archive's pages, which is where the pages were when they
were written; forty carried no link, which was LEGAL by ruling for the whole
`servedCommit=none` window. `ledger/verify.py` walks this register, so shipping
the move alone would have held every commit in the project red.

`PRE_MOVE_MESSAGES` in `tools/producer-check.py` is the answer, and it is the
third instance of the shape `LEGACY_LINK_RULES` and `RESEARCH_VERBATIM` already
use, not a new idea: a frozen tuple of repo-relative NAMES waiving a NAMED
subset (`linkfloor`, `linkdest`, and NOT `linkcap`), counted with its
denominators on its own report line, with a rot check. Membership is by name
and never by the date in the name. A message written from here on is not on it
and faces the full floor, which is the point.

RULED 2026-09-15 05:43Z (decision-2026-09-15-ruling-the-forty-are-waived-by-
name-and-the-walk-back-stands-as-his-number.md): step 2 lands as built;
PRE_MOVE_MESSAGES is the right shape and the right forty, gate-only as
LEGACY_LINK_RULES is, and a fourth frozen list needs a ruling that first
answers queue 307; the provenance guard's rejecting fixtures are queue 306.
