# The workflows, sorted 2026-09-22 when the studio was paused

STATUS: LOG. What was switched off, what was kept, and why each. Nothing was
deleted: every disabled workflow is in `legacy/studio-v2/workflows/` with its
history intact, and moving a file back into `.github/workflows/` is the whole
of re-enabling it.

HOW THEY WERE DISABLED, and why this way. A workflow is live because it sits in
`.github/workflows/`. Editing the trigger out of a file leaves something that
looks live and is not, which is the decayed-claim shape this project keeps
finding; moving the file says the same thing unambiguously and survives someone
reading only the directory listing.

NONE OF THESE RAN ON A TIMER. The order said to disable anything on a timer or
a sentinel file; checked rather than assumed, with comment lines stripped so a
commented-out trigger could not read as live: no workflow in this repository
carries a `schedule:` trigger, and none ever did on this branch. Eight ran on
SENTINEL FILES, which is the dispatch machinery, and those are the eight below.

---

## Disabled: the fleet, the pages and the dispatch machinery

    ledger-install-supervisor-task.yml
        THE FLEET. Registered and started the scheduled task on Jafar's PC that
        ran the supervisor, the bot and the send step. Fired on a push touching
        its own runner scripts or production/outbox/**. With the studio paused
        there is no fleet to install.

    publish-glance.yml
        THE PAGES. Rebuilt and deployed the glance, the map and the gallery to
        GitHub Pages on a push touching any of twenty-one paths, among them
        production/decision-queue.md and production/queue/**. Every one of
        those sources is now archived, so it would have deployed a page about
        a studio that is not running.

    ledger-art-blender-preview.yml
        THE ART DISPATCH. Rendered a named Blender recipe on Jafar's PC and
        committed the frames and a keyed verdict to art/atlas-01. Sentinel
        production/pc-ops/art-preview.request, plus workflow_dispatch. This is
        the lane the lamp column's four attempts went through. The recipes
        themselves are NOT archived: tools/art-recipes/ stays, because the
        local session runs Blender directly and does not need a round trip.

    ledger-mesh-import.yml
        DISPATCH. Sentinel production/pc-ops/mesh-import.request.

    ledger-restart-telegram-bot.yml
        THE FLEET AND THE CHANNEL. Sentinel
        production/pc-ops/telegram-bot-restart.request.

    ledger-imagegen.yml
        DISPATCH. Sentinel production/d1-probe/RUN-IMAGEGEN.

    ledger-setup-msvc.yml
        MACHINE SETUP BY SENTINEL. production/d1-probe/SETUP-MSVC and
        SETUP-BLENDER. Setting up a toolchain is a thing to do at the machine,
        not to ask for by committing a file.

    ledger-vignette-fetch.yml
        DISPATCH. Sentinel production/d1-probe/FETCH-VIGNETTE.

---

## Kept, and running on push: the safeguards Jafar named

    ledger-core-tests.yml
        THE CORE TESTS AND THE LICENCE CHECK, which are two of the three
        safeguards. Runs tools/ci-checks.sh on a push touching ledger/**,
        tools/*.py, tools/*.sh, THIRD-PARTY.md or voice-candidates/**.

        ONE PATH WAS DROPPED: game-design/**. It was there with the comment
        "docs-check runs here, so docs must trigger it", and docs-check is
        archived, so the path was triggering a full Core run for a reason that
        no longer existed. The comment would have become a false claim about
        why the line was there.

        THREE CHECKS LEFT ci-checks.sh with their subjects, sixteen entries to
        eleven, and the file itself says so above its table: docs-check (read
        game-design/ and production/queue/), canon-register (read the archived
        decision register) and goal-block (compared CLAUDE.md's goal block
        against the archived vision pillars; the new CLAUDE.md has no goal
        block). CANON IS STILL GATED: canon-gate --corpus and its selftest
        stay, and they are the check that matters for the game's content.

    ledger-probe-unreal.yml
        THE UNREAL BUILD, the third safeguard, and it CHANGED. It fired on a
        sentinel, production/d1-probe/DISPATCH, which was the dispatch
        machinery asking the runner for a build. It now runs on push touching
        ue-probe/**, tools/ue/** or its own file, which is what "kept as a
        safeguard, running on push" means. Still on the self-hosted runner,
        because that is where Unreal is.

## Kept, untouched: neither fleet, pages, dispatch, timer nor sentinel

    ledger-ai-playtest.yml      push on Core and SimHarness paths. A test OF
                                THE GAME, not of the method.
    citypack-fetch.yml          push on tools/citypack/choices.json
    citypack-inventory.yml      push on the citypack fetchers
    citypack-shortlist.yml      push on tools/citypack/shortlist-candidates.json
                                The three above are the texture-sourcing
                                pipeline. They fire only when someone edits
                                those files on purpose.
    ledger-build-windows.yml    workflow_dispatch only
    ledger-build-mac.yml        workflow_dispatch only
    props-fetch.yml             workflow_dispatch only
    tier2-generate.yml          workflow_dispatch only
    voice-candidates.yml        workflow_dispatch only
                                The five above cannot start themselves.

---

## What a reader should check before re-enabling any of the eight

The disabled workflows read paths that moved. publish-glance reads
production/decision-queue.md and production/queue/**; the supervisor installer
reads production/outbox/** and tools/runner/. Both are now under
legacy/studio-v2/. Restoring the workflow file alone gives a green run that
measures nothing, which is the exact failure `.claude/rules/ci.md` was written
about. `legacy/studio-v2/REACTIVATE.md` puts the file moves before the workflow
moves for that reason.
