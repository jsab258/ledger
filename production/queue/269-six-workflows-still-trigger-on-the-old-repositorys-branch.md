# 269: six workflows still trigger on the old repository's branch

STATUS: LANDED 2026-09-13 under
decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md;
CLOSES on done-line 3 (the served page opened, bar reads 85, servedCommit
recorded). publish-glance and citypack-inventory are proven by the landing
push's runs; citypack-fetch is proven at mechanism level ONLY, its job unrun
since the move and dormant under D16, proven at its own level when
tools/citypack/choices.json next changes. DUPLICATES 254, which closes with
this.
OPENED: 2026-09-13

## The fault, measured

Every workflow in `.github/workflows/` was examined, 18 of 18. Six carry a
live push trigger naming the branch of the repository we left:

    push:
      branches: [claude/game-dev-ai-automation-2h67ix]

    citypack-fetch.yml          line 26
    citypack-inventory.yml      line 23
    ledger-build-mac.yml        line 28
    props-fetch.yml             line 31
    publish-glance.yml          line 27
    voice-candidates.yml        line 23, and four more refs at 69, 84, 85

That branch DOES NOT EXIST on `jsab258/ledger`. The repository has four
branches and they are `main`, `art/atlas-01`, `pc-inbox` and `pc-results`. So
those six have not fired on a push since the move on 2026-09-10, and nothing
said so, because a workflow that never triggers produces no run, no log and no
red tick.

The effect, not the inference. `publish-glance.yml` on this repository:

    total_count 0, workflow_runs []

Zero runs, ever, out of every run of that workflow in this repository. The
run list agrees, with its denominator stated: of the repository's 40 runs the
30 most recent were sampled, and TEN distinct workflows appear in them, all
ten from the twelve that do NOT carry the stale filter: core tests, install
supervisor, restart telegram bot, mesh import, imagegen, Unreal probe, Blender
preview, AI playtest, MSVC setup, vignette fetch. None of the six appears.

WHAT THAT SAMPLE CANNOT SAY, and a first draft of this item said it anyway.
Ten is not twelve. `ledger-build-windows.yml` and `tier2-generate.yml` carry no
stale filter and did not appear either, and with 10 of 40 runs unsampled the
honest statement is that the sample does not cover them, not that they never
ran. `publish-glance` is the one claim that does not depend on the sample,
because its own run count was asked for directly and came back zero.

All six still carry `workflow_dispatch`, so they can be run by hand. That is
why this reads as quiet rather than broken.

## Why publish-glance is the one that matters

The glance is a JAFAR-FACING surface, named as one in
`ledger-v2/studio-v2/constitution.md` item 12 alongside the Producer messages
and the brief, and queue 097 was ruled "publish as designed" so it opens on his
phone. Its own workflow comment states the stake in its own words: "Without
these lines the map would publish once and then never rebuild, which is worse
than never publishing." The path filter it is defending is thirteen lines long
and carefully derived. It has been guarding a branch name that no longer
exists.

So his console has not rebuilt since the move, and the page behind that link is
whatever the old repository last published.

## What this sits next to

Queue 268, and the two are the same shape twice. There the console went blind
because a header rewrite deleted the line its reader matched; here it cannot
republish at all because the trigger names a dead branch. In both cases the
instrument was not lying, it simply was not reached, and in both cases the only
thing that would have surfaced it is somebody opening the artifact. CLAUDE.md
rule 4.

## Done looks like

1. NOT A BLANKET RE-POINT, narrowed by the 2026-09-13 ruling under CLAUDE.md
   rule 9. `publish-glance.yml` re-points to `main` keeping its path filter,
   because it is cheap and Jafar-facing. For each of the other five
   (`citypack-fetch`, `citypack-inventory`, `ledger-build-mac`, `props-fetch`,
   `voice-candidates`) the builder reads what the job COSTS and decides, per
   workflow and in writing in that workflow's YAML comment, between
   re-pointing the push trigger to `main` and DELETING the dead push trigger
   to leave `workflow_dispatch` only. An expensive job does not become
   push-triggered on `main` by a find-and-replace. `voice-candidates.yml`'s
   checkout `ref` at 69 and the fetch and rebase at 84 and 85 move with
   whatever is decided for it: a fix that changes the trigger and leaves a
   checkout pinned to a dead branch is worse than none, because the run fires
   and then works on nothing.
2. The change is PROVEN by a run, not by reading the YAML, for every workflow
   that KEEPS OR GAINS a push trigger. Push a commit touching one path in that
   workflow's filter and show the run appearing, or dispatch it once and show
   it green. Rule 6: built is not running. A workflow that becomes
   dispatch-only is proven by point 4's check instead, and by one dispatch only
   if it is cheap.
3. `publish-glance` is proven all the way to the artifact per CLAUDE.md rule 4:
   the page is opened after the first successful run and the budget bar on it
   reads 85, which is also the accepting case for queue 268's reader.
4. A check that no workflow names a branch absent from the repository, tested
   both ways per rule 5b: the live tree passes once fixed, and a synthetic
   workflow naming a nonexistent branch fails. Otherwise the next move repeats
   this exactly.

## What this does not cover

A multi-line git command's CONTINUATION lines. `tools/workflow-branch-refs.py`
examines a line for git targets only when the line itself contains `git `, and
`publish-glance.yml` 197 to 198 carries `refs/heads/art/atlas-01` on a
continuation. Filed as queue 271 rather than left implicit in a green result.

Why every workflow also runs on `pc-results` pushes, which the run list shows
plainly: 11 of the 30 runs sampled have `head_branch` `pc-results`, including
core tests three times and the Unreal probe once. That is a separate item and
may be deliberate. It is named here so the next reader does not have to
rediscover it from the same list.

## Closing line, 2026-09-13T04:25Z

THE PAGE SERVED. `publish-glance` run 34737101663, job 103670366299, the first
run of that workflow ever on this repository, fired by the landing push and
matched BY ANCESTRY on `head_sha=dc04da736cbdbd3fffc119d1ff47801ec7706204`.
Its own `--check` step requested all four pages back from the live site and
read what came back, on the first attempt with no retry:

    glance    pageHttp=200 pageBytes=8893    pageStampCommit=dc04da73.. expectCommit=dc04da73..
    map       pageHttp=200 pageBytes=227991  pageStampCommit=dc04da73..
    gallery   pageHttp=200 pageBytes=35092   pageStampCommit=dc04da73..
    world     pageHttp=200 pageBytes=17770   pageStampCommit=dc04da73..
    picture   pictureHttp=200 pictureBytes=317539/317539-expected
              filesInManifest=158 picturesAsked=1/158
    secretHits=0/7-patterns on every page
    servedUrl=https://jsab258.github.io/ledger/
    pagesEnableHttp=403   on the SET-THE-SOURCE call, not on serving

WHAT I DID NOT VERIFY MYSELF, AND IT IS DONE-LINE 3. CLAUDE.md rule 4 says to
open the artifact. CI opened it; I could not. This container's outbound proxy
refuses `jsab258.github.io` with `CONNECT tunnel failed, response 403`, tried
twice. So "the page serves, stamped with this commit" is MEASURED, by the
step the project built for exactly this, and "the budget bar on the published
bytes reads 85" is NOT independently measured by the resident. What IS
measured here is that the same generator against the same document draws that
bar from the standing line and says so on the page in its own words: "the
ceiling on both bars is from the standing line in production/budget" and "the
ceiling is the file's standing '85%' line". A reader who can open the page
should close done-line 3 by looking; nobody in this container can.

CITYPACK-INVENTORY RAN AND IT COMMITTED, which is the behaviour change the
ruling flagged rather than a surprise. Run 34737101660 on the same sha, and
its commit is `c022c872 City pack: what the catalogue actually holds`, 4003
insertions and 3964 deletions across `tools/citypack/catalogue.json` and
`candidates.json`: the ambientCG catalogue had drifted. The next push was
REJECTED as non-fast-forward, exactly as predicted, and `git pull --rebase
origin main` was run before pushing, which is now a standing cost of that
trigger and is written into 269 rather than remembered.
