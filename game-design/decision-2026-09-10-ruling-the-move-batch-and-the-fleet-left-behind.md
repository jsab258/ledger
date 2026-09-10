<!--RULING spawn=2026-09-10T19:44:21Z-->
# LOG: ruling on the move batch and the fleet left behind, 2026-09-10

> **STATUS: LOG, 2026-09-10. NOT CURRENT** once section 9 carries the printed
> numbers and queue 257 has landed. Decision record, binding on the resident
> and on the builder who applies section 4. The first ruling on the `ledger`
> repository: LEDGER moved off `jsab258/wc26-picks` today, history unchanged,
> the working branch renamed `main`, the PC checkout now
> `C:\Users\Jafar\ledger-migrate`, the runner `ledger-pc` re-registered and
> proven by a full Unreal probe landing on main at 8caa61d6.

Author: tier-1 director spawned 2026-09-10T19:19:06Z and resumed
2026-09-10T19:44:21Z, row 540 of `.claude/agent-log.tsv`, read this session;
the row reads `2026-09-10T19:44:21Z` TAB `studio-director` TAB `fable` TAB
`default` TAB `a8fc6dcacbdd1a392` and is the newest `studio-director` row in
the file, carrying the same agent id as row 537, the original spawn. A
resident never stamps a ruling; if the gate reports this stamp unmatched or
stale, the numbers go into section 9 and the stamp is not touched.

Stamp re-pointed, same session: this record first carried
`<!--RULING spawn=2026-09-10T19:19:06Z-->`, naming row 537. After it was
written the resident merged `origin/main`, and that merge commit, 31aa9541 at
2026-09-10T19:38:39Z, became the reference `director_cadence` measures from,
so every director row was older than it and the gate read "0 director row(s)
newer than the reference of 538 log row(s) examined". The batch did not
change; the pairing did. The stamp now names row 540, the resume of the same
director, and the batch reviewed below is the same batch.

## 0. What was read, what was not run

No shell in this seat: read, grep and search only. Nothing below came from
running `git`, `verify.py` or any selftest; every count is a grep over the
working tree this session or the brief's, and section 9 makes the resident
print each one before the commit. Read whole: `MIGRATE TO LEDGER.bat`,
`START EVERYTHING.bat`, `START THE STUDIO MACHINE.bat`, `UPDATE FROM
CLAUDE.bat`, `tools/runner/launch-supervisor.py`, `tools/resync.py`,
`production/repo-move-plan.md`, `production/repo-move-triggers.md`,
`production/pc-ops/scheduled-task-verify.txt`, the rulings log, CLAUDE.md and
`.claude/agents/integrator.md`. Read in part: `tools/runner/install-scheduled-task.ps1`
1 to 527, `tools/supervise.py` 337 to 484 and 698 to 723, `tools/pc-watcher.py`
49 to 57 and 696 to 740, `tools/runner/inbox.py` 20 to 64, the six dead
workflows' trigger blocks, `voice-candidates.yml` 1 to 95, and the
`ledger-install-supervisor-task.yml` trigger, concurrency and send steps. Not
opened, per the brief: `ledger/verify.py` and `.claude/hooks/verify-gate.sh`.

**Premise check.** A process ruling. Nothing here touches Meridian, the era,
the moat or the visual bar; section 0 of CLAUDE.md is unchanged and the goal
block is byte-identical to what was read.

## 1. Job one: the CLAUDE.md line, and the integrator brief

Line 159 named a branch that does not exist in this repository, and every
session obeyed it at startup. Replaced, by me, with:

> Branch: `main` of `jsab258/ledger`; `wc26-picks` is the archive, never
> pushed. No pull request unless asked. Purchases and accounts are Jafar's
> alone.

Why this wording and not a bare swap: the archive also has a `main`, and it
is an unrelated football-picks site, so "Branch: main" without the repository
is the sentence that would have sent a wrongly-remoted checkout to the wrong
world. The paragraph names the repository and the archive at the same cost.
Arithmetic, `len(text.split())` semantics, hand-counted twice: the paragraph
was 21 words (`Branch:` .. `Jafar's.`) and is 21 words. Under a `\w+`
counter it falls from 27 to 24. Under any counter the file does not grow, so
the footer should print the same number the routing ruling brought it to,
`CLAUDE.md 1998/2000 words`; section 9 condition 1 prints it. The two
sentences that were shortened lost no rule: "no pull request unless asked"
and "purchases and accounts are Jafar's alone" are the same prohibitions.
Section 0's "Nothing is purchased" already carries the longer form.

`.claude/agents/integrator.md` line 16 to 17 said "Never touch main" beside
the dead branch; the sentence protected the archive's main and now forbids
the integrator's own job. Replaced: the primary branch is `main` of
jsab258/ledger, night branches unchanged, jsab258/wc26-picks is the archive
and is never pushed to, and the old branch name is never resurrected here.

## 2. The two judgement calls, reviewed

**Call 1, `origin` keeps meaning the ledger repository: UPHELD, with the
hole named.** The alternative, renaming about forty `origin` sites, would
also rewrite every selftest fixture that builds a bare `origin.git`, for no
gain in safety. The hazard is real and I checked it: `MIGRATE TO LEDGER.bat`
line 76 clones from `SRC`, the archive, and line 96 adds ledger as a SECOND
remote, so in `ledger-migrate` the name `origin` is the archive and `git
fetch origin main` there resolves to the football-picks site. The pinning is
complete for the two attended doors, `install-scheduled-task.ps1` line 257
(`git fetch $LedgerRemote $DaemonsBranch`) and `START THE STUDIO MACHINE.bat`
line 125, and the three launchers repair the remote before anything below
them can reset (`START EVERYTHING.bat` 124, `START THE STUDIO MACHINE.bat`
111, `UPDATE FROM CLAUDE.bat` 72). The daemons themselves still say `origin`
and hard-reset to it: `tools/supervise.py` 467 to 479 and `tools/pc-watcher.py`
716 to 736. That is fine on every door that repairs first. THE ONE DOOR THAT
REPAIRS NOTHING IS THE SCHEDULED TASK: it runs `launch-supervisor.py`
directly (installer line 388), which acquires a lock and spawns
`supervise.py`, which fetches `origin`. Section 3 is what follows from that.

**Call 2, `$DaemonsBranch` stays a literal with a rewritten reason: UPHELD,
and the substituted reason is stronger than the comment says.** The workflow's
push trigger (`ledger-install-supervisor-task.yml` 81 to 98) has NO
`branches:` filter, only paths, and `workflow_dispatch` lets a caller pick
any branch, so `$env:GITHUB_REF_NAME` can read `pc-inbox` or `pc-results` on
a real run, and a hard reset onto the message channel's tip would replace
the checkout with an inbox. A literal is the only correct answer. The old
reason (a dispatch from `main` moving the checkout off the work branch) is
dead because `main` is the work branch; the comment says so and no longer
argues it. Nothing to change.

## 3. The finding that gates the commit: the installer would move the task onto a checkout it could not bring current

Measured off committed evidence, `production/pc-ops/scheduled-task-verify.txt`
at 4d75256 (epoch 1789047386, today 13:36Z): the registered task "LEDGER
supervisor" runs out of `C:\Users\Jafar\wc26-picks`, six supervisor processes
alive (two `launch-supervisor.py`, two `supervise.py`, two `pc-watcher.py`),
restart count 999 at one minute, `resyncAction=skipped-supervisor-running`.

After this batch, `Find-Repo` (installer 289 to 333) returns
`C:\Users\Jafar\ledger-migrate`, which exists (the probe wrote its packaged
build there tonight). The registration block (423 to 446) does not read the
resync's outcome: with the old fleet alive the resync AND the `origin` repair
are both skipped (they share the `else` at 192 to 287), and the task is then
rewritten with `-Force` to point at `ledger-migrate` because `Test-TaskMatches`
sees a different working directory. The push of this batch fires that run:
line 84 of the workflow names `tools/runner/install-scheduled-task.ps1` in its
path filter, and the morning brief push fires it again every day.

What that arms, at Jafar's next sign-in, with nothing else done: the task
starts `launch-supervisor.py` in a `ledger-migrate` that is frozen at
migration time with `origin` unrepaired. The lock file is per checkout
(`launch-supervisor.py` line 61, `game-design/pc-jobs/supervisor.lock`
inside the repository), so nothing refuses. That checkout's `supervise.py`
still carries the OLD branch constant, which the archive still has, so its
`resync_once` succeeds against the archive's frozen tip and the fleet comes
up pinned to the archive for ever, pushing receipts there and unable to send
a brief (the send steps gate on `checkout-contains`, which refuses a checkout
that lacks the run's commit). The worse branch of the same tree: current code
with `main` in the constant reaching that checkout by any route that does not
repair the remote (Jafar typing `git pull`, whose upstream is `ledger/main`)
puts `fetch origin main` against the archive, and the hard reset replaces the
project with the football-picks site. The gate that cost four days to earn
would have held and the fleet would still have moved to the wrong world.

**Amendment A1, IN THIS BATCH, blocking, a builder edit to
`tools/runner/install-scheduled-task.ps1`:** the installer registers or moves
the task ONLY onto a checkout it brought current in this run
(`resyncAction=updated`) or that the existing task already names
(`WorkingDirectory` equal to `$Repo`). In every other case it prints
`installAction=refused-checkout-not-current taskRepo=<existing or none>
wantedRepo=<$Repo> resyncAction=<what it printed>` and exits 0: a refusal
with its reason is a measurement, not a failure. The three-way process gate
is not touched, not narrowed and not given a flag; this adds a fourth
refusal in the direction that can only refuse. Rule 5b: the first
push-triggered run after landing is the REJECTING case on live data (task at
`wc26-picks`, wanted `ledger-migrate`, fleet running) and the evidence file
must show the refusal; the accepting case is the transition run of queue
257, watched. `Test-TaskMatches` already reads the existing action, so the
existing working directory is one more field off the same object.

**A2, in the same edit, print only:** one line per supervisor process,
`supervisorPath=<the checkout root parsed from its CommandLine, or
unattributable>`. Fail closed: an unattributable process counts as this
checkout. This is the series queue 257 needs before any per-checkout
reasoning is allowed; it decides nothing today.

Two more one-liners the resident hand-applies, in this batch:

- `tools/imagegen/imagegen.py` line 1489, `EXPECTED_BRANCH = "main"`. The
  publisher's preflight (1576 to 1584) refuses to send from any clone not on
  that branch, so the art lane's next run would bank nothing; the selftest
  fixtures (4359 to 4380) use the symbol, so the value moves alone.
- nothing else. `tools/runner/run-night.ps1` line 41 also names the dead
  branch but that path is retired and manual; it goes to queue 255.

## 4. The transition, and the smallest correct action from Jafar

The deadlock is real and it is not weakened here: the runner is interactive
as JAFAR-DESKTOP\Jafar, so it runs only while he is signed in; while he is
signed in the old task's fleet is up; while a supervisor is up the installer
refuses to touch `ledger-migrate`; and signing out and in restarts the old
fleet because the task still names `wc26-picks`. Nothing on his disk today
runs this batch's code: `wc26-picks` is frozen at the archive's tip and
`ledger-migrate` at migration time, so every launcher he can double-click
still points at the old folder. The batch does not depend on anything he has
done; with A1 it also cannot half-move anything before he acts.

**Smallest correct action from Jafar, two clicks and no process hunting:** on
the PC, Task Scheduler, "LEDGER supervisor", Disable; then sign out and back
in (or restart). A disabled task does not fire at logon, the old fleet dies
with the session, and the next installer run finds nothing running, resyncs
`ledger-migrate` from the pinned URL, repairs `origin`, re-registers the
task there (enabled) and starts it. The studio dispatches that run when he
reports the restart; the 04:00Z brief push would also do it. The evidence
that it happened is one file: `production/pc-ops/scheduled-task-verify.txt`
reading `resyncAction=updated`, `originAction=repointed` or
`already-ledger`, `installAction=update`, `repo=C:\Users\Jafar\ledger-migrate`,
`startedNow=attempted`, `supervisorProcessesAfter` above 0, and then
`pcInboxHeadShort` moving past 2a7a234c on the run after.

**The studio's default if he has not acted, queue 257:** a dispatched job on
the runner that disables the task, stops the old tree leaves-first the way
`restart-telegram-bot.ps1` already does, verifies zero remain by the same
three-way query, and only then runs the installer's normal gated path. The
precedent is the 2026-09-07 remote restart job. The old fleet has no value to
the studio today (it pushes to the archive and cannot send a brief), so
stopping it loses nothing the studio can read. Until either route lands,
THE CHANNEL TO JAFAR IS DEAD FROM THIS REPOSITORY: the brief-send and outbox
sweeps refuse from a checkout that lacks the run's commit, and both checkouts
lack every commit made here. The Producer says so rather than counting a
missing brief as a quiet day.

## 5. The seven findings, ruled

1. **Six push-dead workflows: QUEUE 254.** Latent, not live: on a dispatch
   today every `voice-candidates.yml` job checks out `ref:
   claude/game-dev-ai-automation-2h67ix` (lines 69, 121, 148, 207), the ref
   does not exist here, checkout fails, and neither push (86, 401) is reached.
   The resurrect hazard becomes LIVE the moment a partial fix lands, so the
   seven sites in that file move in one edit and the proof is a grep count of
   zero. `ledger-build-mac.yml` stays dead by ruling: D16 retired the Unity
   build and `macos-latest` minutes are the expensive class. `publish-glance.yml`
   flips together with the site links, finding 6.
2. **`1 SET UP THE BUILD RUNNER.bat` line 102: QUEUE 255, first row.** The
   runner is registered; the next person to follow the file would register it
   to the archive and blind the studio silently.
3. **About thirty-one launchers: QUEUE 255.** Not in this batch, and not a
   blind replace: `tools/voice-live/8 START THE WATCHER.bat` fetches `origin`
   and hard-resets, `tools/mixamo-pick/SETUP.bat` clones the archive, the
   meshgen and imagegen launchers pull the dead branch. Each gets the same
   pin-or-repair discipline the six launchers in this batch got, from a
   per-file table of what it does when clicked. None of them runs on his disk
   until queue 257 has landed anyway.
4. **`tools/d1-cycles.py` line 269: QUEUE 255.** Grep finds no call site
   outside its own selftest, so it is a dormant instrument reading the wrong
   world; it moves in the sweep and prints the repository it reads on its
   first line, so the next reader can see which world the numbers are of.
5. **`imagegen.py` `EXPECTED_BRANCH`: IN THIS BATCH** (section 3).
   `run-night.ps1` line 41: QUEUE 255, retired path.
6. **Pages links: QUEUE 256, left as they are in this batch.** Neither a
   stale-but-live link nor an unverified one goes into a brief: the first is
   the 2026-09-09 fault (a page that does not show what today's message
   describes) and the second is a 404 on his phone. The register's
   `SITE_ORIGIN` and the other five sites change in the same commit that
   flips `publish-glance.yml` to `main`, after ONE dispatched run of that
   workflow on `ledger` prints the served commit through its own `--check`
   step, the entry point that already exists. If that run says Pages is not
   enabled on `ledger`, that is the one card for Jafar. Until then briefs
   carry no site link; the register allows zero.
7. **Data in the archive: QUEUE 258.** The return half (receipts, inbound
   messages) keeps landing on the archive's `pc-inbox` until the old fleet
   stops, and possibly on its `pc-results`. Recovery is a queue item ordered
   AFTER queue 257 and it must not assume: that the studio may write to the
   archive (never); that the archive branch is a fast-forward of ours (test
   by ancestry, `merge-base --is-ancestor`, and merge if not); that the new
   fleet has not pushed to our `pc-inbox` by then (never force over it); or
   that the archive has stopped moving before the fleet is stopped.

## 6. Dictated block for `production/NOW.md`, resident to paste at the top

    ## 2026-09-10 20:00Z: THE REPOSITORY MOVED AND THE FLEET DID NOT

    LEDGER is jsab258/ledger, branch main, identifiers unchanged. The PC's
    fleet still runs out of C:\Users\Jafar\wc26-picks, pushing to the
    archive, and the channel to Jafar is dead from this repository until it
    moves: both his checkouts lack every commit made here, and the senders
    refuse from such a checkout. The installer now refuses to move the task
    onto a checkout it has not brought current. Jafar's two clicks, or the
    studio's queue 257, complete the move. Ruling:
    game-design/decision-2026-09-10-ruling-the-move-batch-and-the-fleet-left-behind.md.

## 7. The gate hole, recorded on the resident's word

The resident reports the verify repair and the commit-gate repair finished in
this tree, and that the gate hook's hole dates to its first commit, cd30c19a
on 24 August, open seventeen days. I did not open either file, per the brief,
and I did not run the gate; this paragraph records the claim and section 9
condition 4 makes the gate print its own numbers on this batch, which is the
only evidence the claim needs.

## 8. Quality ladder at close

First working result for the move; the rungs above it, named: queue 257 (the
fleet moves), 258 (the return half recovered), 255 (nothing on his disk names
the old folder), 254 and 256 (every workflow and link on `main`), and the
per-checkout process attribution that A2 prints and nobody may act on until
its series exists. The blank rung is the lock: `launch-supervisor.py` locks
per checkout, and a machine with two checkouts can run two fleets on one
Telegram token; whether the lock should be per machine is a research task,
filed inside 257 as a question, not built.

## 9. Conditions the resident prints before the commit

1. `python3 ledger/verify.py` footer: `CLAUDE.md` word count, expected 1998
   of 2000, and `tools/goal-block-check.py` green.
2. `python3 tools/docs-check.py`: this record LOG, under 400 lines, em-dash
   count 0; the five queue files declare a status.
3. Cadence numbers: rulingStamps, rulingFresh, rulingStale, rulingUnmatched;
   this stamp lands FRESH.
4. The commit gate's own numbers on this batch, from the repaired hook.
5. `grep -c 'refused-checkout-not-current' tools/runner/install-scheduled-task.ps1`
   is at least 1, and `grep -n 'supervisorPath=' ` the same file finds the A2
   print; `grep -n 'EXPECTED_BRANCH = ' tools/imagegen/imagegen.py` reads
   `"main"`; `python3 tools/imagegen/imagegen.py --selftest` green after it.
6. Denominators for the sweep items, printed as counts over files scanned:
   `wc26-picks` in `tools/`, `.github/`, root launchers; the dead branch name
   in the same set; `ledger-migrate` sites (this batch, 11 files plus the
   installer's comments).
7. After the push: `production/pc-ops/scheduled-task-verify.txt` from the
   run this push fires reads `installAction=refused-checkout-not-current`
   with the two paths, or the batch is reverted and this section reopened.

## 10. Landing

Filled by the resident with printed numbers, one line per condition. Empty
until then.
