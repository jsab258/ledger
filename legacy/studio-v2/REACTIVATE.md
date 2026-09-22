# Bringing the studio back

STATUS: LOG. Written 2026-09-22, the day it was paused, by the session that
paused it, while the reasons were still in front of it.

WHAT THIS IS FOR. Jafar paused the studio for a two-week test after an outside
audit found that operationally it had become the product. Nothing was deleted.
This file is the order the pieces have to come back in, and the order matters
in one place: THE FILES MOVE BEFORE THE WORKFLOWS AND THE WORKFLOWS BEFORE THE
TRIGGERS. A trigger that fires into a repository whose queue is still archived
does not fail loudly, it runs and finds nothing to do, and a green run that
measured nothing is the failure this project has spent the most time on.

DECIDE FIRST WHETHER YOU WANT ALL OF IT. The audit's finding was not that the
machinery was broken; most of it worked. The finding was that it competed with
making the game. Bringing back the queue, the register, the briefs and the
gates as one block restores the competition along with the capability. The
pieces below are separable and are listed so they can be taken one at a time.

---

## 0. Before anything

    git log --oneline --follow -- legacy/studio-v2/CLAUDE.md

will show the studio's own history; every file below kept its history through
`git mv`. Read `legacy/studio-v2/CLAUDE.md` first. It is the thing that made
the rest cohere, and reading the parts without it produces a studio that has
the machinery and not the reasons.

## 1. The session's own rules and execution paths

    git mv legacy/studio-v2/CLAUDE.md CLAUDE.md
    git mv legacy/studio-v2/claude/hooks .claude/hooks
    git mv legacy/studio-v2/claude/agents .claude/agents
    git mv legacy/studio-v2/claude/rules .claude/rules
    git mv legacy/studio-v2/claude/settings.json .claude/settings.json
    git mv legacy/studio-v2/claude/agent-log.tsv .claude/agent-log.tsv
    git mv legacy/studio-v2/claude/agent-turns.tsv .claude/agent-turns.tsv
    git mv legacy/studio-v2/claude/template-sync.txt .claude/template-sync.txt

THE OLD settings.json CARRIES THE HOOKS, and they are the studio's reflexes:
the session-start banner, the verify gate that refuses a commit when the tree
changed after the last green footer, and the wake drain at the turn boundary.
Restoring that file restores all three at once. The minimal settings.json the
local session uses will be overwritten, so keep a copy if it has grown
permissions worth keeping.

## 2. The documents

    git mv legacy/studio-v2/studio-v2 ledger-v2/studio-v2
    git mv legacy/studio-v2/respec ledger-v2/respec
    git mv legacy/studio-v2/handoff ledger-v2/handoff
    git mv legacy/studio-v2/open-questions.md ledger-v2/open-questions.md
    git mv legacy/studio-v2/README.md ledger-v2/README.md
    git mv legacy/studio-v2/game-design/* game-design/
    git mv legacy/studio-v2/production/* production/

`ledger-v2/research/` never moved: the licence allowlist lives there and is law
whether the studio runs or not.

## 3. The tools

    git mv legacy/studio-v2/tools/* tools/
    git mv legacy/studio-v2/verify.py ledger/verify.py

Then put the three archived checks back in `tools/ci-checks.sh`. The file says
in its own comment which three left and why; the entries are:

    docs-check            "$REPO"   "python3 tools/docs-check.py"
    canon-register        "$REPO"   "python3 tools/canon-register-check.py"
    canon-register-selftest "$REPO" "python3 tools/canon-register-check.py --selftest"
    goal-block            "$REPO"   "python3 tools/goal-block-check.py"
    goal-block-selftest   "$REPO"   "python3 tools/goal-block-check.py --selftest"

GOAL-BLOCK WILL FAIL UNTIL CLAUDE.md CARRIES THE GOAL BLOCK AGAIN. Step 1 puts
the old CLAUDE.md back, which carries it, so do step 1 before this.

## 4. The workflows

    git mv legacy/studio-v2/workflows/* .github/workflows/

and put `ledger-probe-unreal.yml` back on its sentinel if you want the dispatch
shape rather than push-on-Unreal-paths; `legacy/studio-v2/WORKFLOWS.md` records
exactly what that trigger was. Restore `game-design/**` to the Core tests'
paths at the same time, since docs-check reads it again.

DO NOT DO THIS BEFORE STEP 2. publish-glance reads production/decision-queue.md
and production/queue/**; the supervisor installer reads production/outbox/**.
Restored early, they run and publish a page about nothing.

## 5. The scheduled triggers

LAST, and only when steps 1 to 4 are pushed. `legacy/studio-v2/TRIGGERS.md` has
all three with their schedules, their session bindings and their prompts
verbatim. They still exist on Jafar's account with `enabled: false`, so each is
one call:

    update_trigger  trig_017Ho772fH6Uuysbith7b3CU  enabled=true   hourly inbox and resume
    update_trigger  trig_01QrCWMiEuuxjXAB4EHARS6J  enabled=true   daily wake, writes the brief
    update_trigger  trig_017Wzurh3D3fV2JiMQj7NS34  enabled=true   Sunday page

THE ONE THING THAT CAN HAVE ROTTED: two of them bind to persistent session
`session_0123EQyYSuvGzhBctpiMmJzx`, and their prompts assume a conversation
that remembers. If that session is gone, rebind or rewrite them as standalone
instructions before enabling, or they will wake into an empty room and improvise.

## 6. The fleet on his PC

The scheduled task on Jafar's machine is installed by
`ledger-install-supervisor-task.yml`, which step 4 restores. It is a
`workflow_dispatch` run against his self-hosted runner. Nothing in this
repository can install it for him and nothing here can confirm it started; the
only readings are the files his PC commits under `production/pc-ops/`.

---

## What was NOT archived, and must not be archived by a later tidy-up

The game's own half stayed where it was and the studio's return does not touch
it: `canon.md`, `content/`, `production/research/`, `production/specs/`,
`production/art/`, `production/assets/`, `production/playtest/`,
`production/stranger-test/`, `research/`, `ledger-v2/research/` with the licence
allowlist, `THIRD-PARTY.md`, `voice-candidates/`, the C# Core and its tests, the
C++ port, the Unreal project under `ue-probe/`, the Blender recipes under
`tools/art-recipes/`, the material and mesh pipelines, the citypack fetchers,
and the fifty-eight design documents left in `game-design/`.
