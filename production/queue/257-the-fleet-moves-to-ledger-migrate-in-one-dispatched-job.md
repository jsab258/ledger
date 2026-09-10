# 257. The fleet moves to ledger-migrate, in one dispatched job

STATUS: READY, 2026-09-10, BLOCKING the channel. Ruled by
`game-design/decision-2026-09-10-ruling-the-move-batch-and-the-fleet-left-behind.md`
sections 3, 4 and 8. Opus per the routing table (a workflow under
`.github/workflows/` and a PowerShell instrument for the PC).

## What is wrong

The PC's fleet runs out of `C:\Users\Jafar\wc26-picks`, started by the
scheduled task "LEDGER supervisor" at every logon (evidence:
`production/pc-ops/scheduled-task-verify.txt` at 4d75256, six processes,
restart count 999). It pushes receipts to the archive and cannot send a
brief, because the send steps refuse from a checkout that lacks the run's
commit and both of his checkouts lack every commit made on `ledger`. The
installer cannot move it: while a supervisor is alive it refuses to resync
`ledger-migrate` (correctly), and after the move batch it also refuses to
re-register the task onto a checkout it has not brought current (amendment
A1). The runner is interactive as Jafar, so it runs only while the old fleet
is up. The channel to him is dead until this lands or he does the two clicks
in the ruling's section 4.

## The deliverable

One workflow, `workflow_dispatch` ONLY, never on push, concurrency group
`ledger-install-supervisor-task` so it queues behind the installer rather than
racing it. Its script, in order, each step printing its key=value evidence to
one committed file `production/pc-ops/fleet-move.txt` with the commit on
line 1:

0. Read the series first: `supervisorPath=` per process (the A2 print from the
   installer, reused by dot-sourcing `process-query.ps1`, never copied). Refuse
   with `moveAction=refused-fleet-not-in-old-checkout` unless every attributed
   process lives under `C:\Users\Jafar\wc26-picks` and none is unattributable.
1. `Disable-ScheduledTask "LEDGER supervisor"`, read back `taskEnabled=False`.
   Disabled first so the restart-on-failure setting cannot bring the tree back
   between steps 2 and 3.
2. Stop the old tree leaves-first, the pattern `restart-telegram-bot.ps1`
   already implements for the bot (matched set widened to
   `launch-supervisor\.py|supervise\.py|pc-watcher\.py|telegram-bot\.py|executor\.py`,
   roots last), then re-query until `supervisorProcessesFound=0` or a 60 s
   ceiling; on the ceiling, stop and print what survived. Never touch a
   process whose path is not under the old checkout.
3. Only then call `install-scheduled-task.ps1` unchanged. Its own gate now
   passes: `resyncAction=updated`, `originAction=repointed` or
   `already-ledger`, `installAction=update`, `repo=...\ledger-migrate`,
   `startedNow=attempted`, and re-enabling happens in its registration.
4. Verify the effect, not the exit code: `supervisorProcessesAfter` above 0
   with every `supervisorPath=` under `ledger-migrate`, and on the next
   installer run `pcInboxHeadShort` past 2a7a234c.

Step 0 of the whole item, before the workflow: `tools/runner/launch-supervisor.py`
repairs `origin` to `https://github.com/jsab258/ledger.git` after it holds
the lock and before it spawns `supervise.py`, read back and printed
`originAction=`. It owns the checkout at that moment, so this is not a second
writer; it closes the one door that repairs nothing today (the scheduled task)
and the hand-typed `git pull` path named in the ruling. Selftest in the
container, accepting case first: a temp clone whose `origin` is a bare
"archive" reads the ledger URL after one launch; the rejecting fixture is a
checkout with no `.git`, which prints `originAction=no-checkout` and does not
raise.

## Done looks like

`fleet-move.txt` committed with the keys above, the installer's evidence file
from the same run reading the accepting case of A1 (`installAction=update`
on a checkout it resynced), and one receipt landing on `ledger`'s `pc-inbox`
from the new fleet. Then the Producer tells Jafar it happened, which is the
first message that can reach him from this repository.

## Dependencies and risk

The move batch with A1 and A2 landed and its first push-triggered installer
run showing the refusal. Risk: the tree-stop leaves an orphan the query
cannot see; step 2's re-query and ceiling are the guard, and a stopped fleet
with no restart is the failure the evidence file names out loud. Open
question filed here, not built: the single-instance lock is per checkout
(`launch-supervisor.py` line 61) and a machine with two checkouts can run two
fleets on one Telegram token; whether it should be per machine is decided
after this lands, from the `supervisorPath=` series.
