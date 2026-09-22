# 261: the executor tells Jafar it failed, and nothing anywhere says why

STATUS: READY
OPENED: 2026-09-11

## The fault, measured

At 2026-09-11T13:16:56Z Jafar sent "Is this working?" from his phone. At
13:18:43Z, 107 seconds later, the studio answered him, and the receipt landed
on `pc-inbox` as
`production/outbound/2026-09-11T1316Z-79313220.answer.receipt.txt`. The round
trip works.

What it sent him was a failure notice:

    The machine cannot start the work you asked for: the tool it needs is not
    available on this machine right now. Nothing you asked for was lost, and
    nothing was started. It will work once somebody has looked at the machine.

The receipt records `chars: 271`. That number identifies the branch exactly:
`fallback_no_cli()` called with NO state words, which is
`tools/runner/executor.py:1533` and nowhere else. The three variants measure
271, 262 and 267 characters, so 3 of 3 were distinguished and the match is
unique, not merely consistent.

Line 1533 sits under `if not res["started"]`, which means `worktree_ready` and
`prepare_worktree` BOTH SUCCEEDED and the Claude CLI itself would not start.

## Why that is where the diagnosis stops

The branch that fired records the reason: `self.record("no-cli", msg=stemname,
why=oneword(res["why"]))`, and `run_session` distinguishes at least "would not
start" from "not on PATH" (both have selftest fixtures, at
`executor.py:2394` and `executor.py:2450`).

THE CHANNEL EXISTS, IT WORKS, AND IT DOES NOT CARRY THIS ONE KEY. That is the
finding, and it is a much smaller fix than the first version of this item
claimed. I wrote here that the reason reached no channel at all, then opened
`production/pc-ops/` and found that false: CI copies the supervisor's status
off the PC every run, into `production/pc-ops/supervisor-status.txt`, line 1
naming the commit it was read on, exactly the channel `.claude/rules/ci.md`
prescribes. On the 07:02Z run it read `statusFound=yes statusAgeSec=11
statusFresh=yes`, and it already carries an executor summary:
`executorState=idle executorHandled=1 executorPending=0
executorLimitResumeIn=none`.

WHAT IT DOES NOT CARRY IS THE ONE FIELD THAT WOULD HAVE ANSWERED THIS.
Measured, not inferred:

    grep -rn "cli=|no-cli|notOnPath|wouldNotStart" production/pc-ops/   0 hits
    pc-jobs paths named by tools                                        8
    of those, published by CI                                           1
      (supervisor-status.txt; request.json and result.txt are job input
       and output, tracked in the repo rather than status read off the PC)
    of those, carrying the executor's `cli` key or its no-cli reason     0

`self.status["cli"]` is set to "found" or "missing" at `executor.py:1789` and
1530, and the no-cli reason is recorded in the journal. Both live in
`game-design/pc-jobs/executor-status.txt` and the journal, neither of which is
published. So the aggregate says the executor is idle and has handled one
instruction, and nothing says it could not start the tool or why.

This is CLAUDE.md rule 12 in the live system: the feedback channel is blocked,
and that outranks the fault it is hiding.

## Done looks like

1. The executor's status file reaches a branch a session can read, by the
   channel `.claude/rules/ci.md` already prescribes: a file committed by the
   PC, staged BY NAME, carrying a `key=value` verdict whose line 1 names the
   commit it was written from.
2. A run that measured nothing says `NO RUN` rather than carrying the previous
   run's file forward under its own name.
3. The `no-cli` reason is on that file under its own key, with the two cases
   `run_session` already separates kept separate, so "not on PATH" and "would
   not start" never read alike.
4. The accepting case is run, not assumed: one instruction that SUCCEEDS
   publishes a status file too, so the channel is proven on the outcome it
   will spend most of its life reporting.

## What this does not cover

Why the CLI did not start on 11 September. That is unanswerable from here by
construction, and answering it is what this item buys.

## Deliverables, restated by the director 2026-09-11, section 5

DELIVERABLE 1 IS THE CHEAPEST DECISIVE MEASUREMENT AND IT IS A WORKFLOW EDIT,
not a daemon change. The `no-cli` branch at `executor.py:1533` returns WITHOUT
`push_record`, so the `why=` lives only in the journal on his PC. The "Publish
the supervisor's own status" step in `ledger-install-supervisor-task.yml`
(lines 870 to 908) gains two more sources, copied the same way, each with its
own `statusFound=`, `statusAgeSec=` and `statusFresh=` head and the NOTHING
MEASURED wording when absent:

    C:\Users\Jafar\ledger-migrate\game-design\pc-jobs\executor-status.txt
      -> production/pc-ops/executor-status.txt
    LAST 40 lines of C:\Users\Jafar\ledger-exec-state\journal.log
      -> production/pc-ops/executor-journal-tail.txt
      with the cap announced as journalLines=<shown>/<total>

Both staged BY NAME with `-A` beside line 968, per `.claude/rules/ci.md`. The
push that lands this FIRES the run, and that run prints the 13:18Z
`no-cli ... why=` record.

DELIVERABLE 2 IS THE DAEMON HALF, `executor.py` and `supervise.py` with their
selftests. The executor's status file gains:

    cliLastStart=started|not-started|nothing-measured
        LAST-WINS over sessions this process attempted; the words until the
        first attempt
    cliWhy=<oneword of res["why"]>|none|nothing-measured
        the reason of the last not-started session in run_session's own words,
        so not-on-PATH, would-not-start/<ExceptionName> and
        log-could-not-be-opened/<ExceptionName> stay DISTINCT; none when the
        last session started
    sessionsStarted=<n>/<attempted>
        CUMULATIVE since process start; nothing-measured when attempted is 0,
        never 0/0

`supervise.py: executor_keys` publishes them as `executorCli=`,
`executorCliLastStart=`, `executorCliWhy=`, `executorSessionsStarted=`. When
the executor's file predates the keys (an old process still running after the
code lands, WHICH WILL BE THE STATE ON THE FIRST RUN) it prints
`nothing-measured/key-absent`, never `unreadable`. `cli=found` stays and is
documented as "which() resolved the name", which A6 in that file shows is NOT
proof it starts.

NO BOUND IS SET ON ANY OF THESE NUMBERS. They are printers. Rule 2: a bound
needs a printed series first, and there is no series yet.

THE ACCEPTING CASE FOR DELIVERABLE 2 IS DEFERRED AND SAID SO. An instruction
that SUCCEEDS publishing the keys is a condition of this item's CLOSE, not of
its commit, because it cannot happen until the CLI starts. The commit condition
is the two selftests driven BOTH ways.

Ruling: game-design/decision-2026-09-11-ruling-the-link-floor-marker-batch-and-the-answer-already-sent.md
