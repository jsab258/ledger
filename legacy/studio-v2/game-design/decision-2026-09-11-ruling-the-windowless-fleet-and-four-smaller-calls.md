<!--RULING spawn=2026-09-11T06:09:35Z-->
# LOG: ruling on the windowless fleet and four smaller calls, 2026-09-11

> **STATUS: LOG, 2026-09-11. NOT CURRENT** once the re-enable condition in
> section 1 has been printed and the batch is committed. Decision record,
> binding on the resident for this commit.

Author: tier-1 director, stamp above naming row 546 of
`.claude/agent-log.tsv`, read this session (`2026-09-11T06:09:35Z` TAB
`studio-director`, the newest director row in the log at the time of writing).

Scope: 187 changed lines over the supervisor fleet (`tools/supervise.py`,
`tools/pc-watcher.py`, `tools/runner/executor.py`,
`tools/runner/launch-supervisor.py`,
`.github/workflows/ledger-install-supervisor-task.yml`),
`tools/container-setup.sh`, `production/budget.md`, and the outbox. No
simulation, Core, canon or premise change is in the batch; section 0 of
CLAUDE.md is untouched and nothing here is checked against it further.

Facts I rule on, as reported to me and not re-measured here: the install at
424cc7eb succeeded (`resyncAction=updated`,
`checkoutBroughtCurrentThisRun=True`, `installAction=update`); A1 is proven
on both outcomes by real runs; the task registers `pythonw.exe` with
`windowless=True`; 11 subprocess call sites carry `CREATE_NO_WINDOW` at 0 of
11; `taskLastTaskResult=267009` is 0x00041301, "currently running". The
windows were the fleet's first windowless parent surfacing a latent fault at
all 11 sites, not a crash loop. Anyone who finds a number above wrong grep for
the sentence, per rule 1, and this record is corrected, not the number.

## 1. The re-enable condition (Jafar's click, after the batch lands)

The scheduled task is registered and enabled again only when ONE proof run
on Jafar's PC has printed ALL of the following to the committed evidence
channel, and a later session checks each line by reading it, not by judging
it:

1. `fixCommit=<sha>` where the sha CONTAINS (ancestry, never branch name)
   the commit that adds `CREATE_NO_WINDOW` to every subprocess call site
   the fleet reaches, and the ast check on that same checkout prints
   `noWindowSites=20/20 unflagged=0`. The count rose from 11 to 20 because
   the builder derived the fleet by import rather than listing it by spawn,
   and the nine import-reachable sites it found (`tools/runner/single_instance.py`,
   `tools/runner/inbox.py`, `tools/runner/outbox.py`) were the ones actually
   producing windows in normal running; a reader who finds an 11 elsewhere
   in this record or the batch is reading the earlier, smaller scope, and 20
   is current.
2. `taskRegistered=False taskEnabled=False` printed at proof START. The
   fleet is started by hand for the proof; the task is not the launcher.
3. Per process, for every process in the roster the proof fixes after
   warmup and prints as `processesWatched=n/n`: `survivedSec=300/300`. The
   roster is the supervisor plus its children, not the two the installer
   happened to name at 424cc7eb; two is a floor, not the expected count,
   and the run in hand reads `processesWatched=5/5`. A later session checks
   that n is printed, that the two sides are equal, and that n is at least
   two. Any process below 300 reads as `verdict=DIED` whatever else the
   line says. A dead process has no window, so a fleet that died inside
   the window is the trivially windowless one; a green verdict word with a
   survival denominator short of 300 is a fail, not a pass.
4. `windowlessSamples=n/n` with n printed and equal on both sides,
   `handlesNonZero=0`, and `conhostChildren=0` where the conhost count is
   CUMULATIVE over the window, not last-wins: a git child lives a fraction
   of a second and a sampler that only reads the current instant cannot
   see it. If the printer cannot be made cumulative, it prints its cadence
   and says so, and item 5 carries the weight.
5. THE INSTRUMENT HAS BEEN SEEN TO FAIL FIRST (rule 5b, rule 3). Before the
   passing run counts, the same proof step is run against the pre-fix
   checkout (the commit Jafar watched fill his screen), and it prints
   `verdict=WINDOWS-SEEN` with `conhostChildren>0` or `handlesNonZero>0`.
   This run may be cut at the first sighting; it needs no fixed length.
   Without this line, `verdict=WINDOWLESS` means "the sampler cannot see
   windows" and re-enable is refused.
6. `verdict=WINDOWLESS` on the fixed checkout, and Jafar's word in the
   Telegram inbox, answered in the same run, that the screen stayed clear
   for the five minutes. The instrument measures handles and conhosts; the
   complaint was the screen, and he is the only reader of it.

`taskLastTaskResult=267009` is not read by this condition and is never
cited as a failure again. Re-enabling is Jafar's one click; the resident
does not register or enable the task on his behalf.

## 2. A fifth refusal in the installer: yes, static; no, runtime

Ruled: A5 is added, as a QUEUE ITEM, not this batch. The installer refuses
to register or enable when the ast check on the checkout it is installing
reports any unflagged subprocess site (`noWindowSites=<k>/<n> unflagged>0`).
It is same-run, one python invocation, and it measures the exact fault class
of this morning on the exact checkout being installed. Its rejecting fixture
is the pre-fix commit; its accepting fixture is the fixed one; both are
printed before A5 lands.

Rejected: a refusal that reads a runtime proof verdict from an EARLIER run.
That couples every install to a five-minute proof per commit, and it makes
the installer read a previous run's file under its own name, which is the
carry-forward hazard `.claude/rules/ci.md` names. The runtime proof is
section 1's gate for THIS re-enable and a manual step thereafter.

## 3. `tools/container-setup.sh`: resident-written, not rewritten

The split says the resident hand-applies dictated text or a one-line fix;
187 lines of shell is neither, so by the letter the resident was wrong and
a builder brief was the course. Rule 12 is the mitigation: verify was
crashing on its first check, the feedback channel was the bug, and fixing
it first is the standing order. The cost of the breach was one bug (a
`find_spec` call without `import importlib.util`) caught by the
accepting-case run, which is what the run is for.

Ruled: NOT rewritten. A builder rewrite spends a spawn to produce the same
187 lines. It ships IN THE BATCH on two conditions, both dictation-level
work the resident may do: (a) the accepting line `stepsOk=5/5` is pasted
into the commit message from the run, and (b) the pymods check is run once
with a planted absent module name (a name that exists nowhere) and prints
FAILED for it, pasted beside (a). The first draft failed a passing case;
until (b) prints, nobody knows whether the fix also passes a failing one.
A `--selftest` flag carrying both fixtures is a QUEUE ITEM for a builder.

## 4. The budget header: the rewrite is not enough

Two ceilings in one file turned a 78/82 reading against an 85-on-the-higher-
meter ceiling into a breach that had not happened, and work was narrowed for
it. The rewrite removes the disagreement today; nothing stops the next
session that edits the header from re-creating it. This is the goal-block
pattern: CLAUDE.md carries `tools/goal-block-check.py` for exactly this.

Ruled, QUEUE ITEM, builder, small: `production/budget.md` carries exactly
ONE machine-readable line declaring the ceiling (form for the builder:
`ceiling=85 meter=higher ruled=2026-09-10`), verify.py asserts the count
(`ceilingLines=1/1`), and every reader of the ceiling, the resident
included, reads that line and nothing else. Prose may recount old ceilings
as history. Rejected: a check that fails when "two ceiling numbers appear",
because a history line that says the ceiling rose from 80 to 85 is correct
and would trip it. Rejecting fixture: a synthetic second `ceiling=` line.

IN THE BATCH: the 78/82 reading was not a breach. Whatever the resident
narrowed on it is un-narrowed, named in `production/NOW.md` by the resident
in this commit. I do not know what was narrowed; the resident does.

## 5. Queue 260: the 5346-character message poisons the sweep

A message over Telegram's 4096 cap 400s on every sweep, will 400 for ever,
and holds `sweepExitCode=1`, so the one channel that works reads red for a
cause that cannot clear. Rule 12: highest-leverage bug on the board.

IN THE BATCH, one-line, resident: move the 5346-character message from the
live outbox to `production/outbox-blocked/` beside the 4739-character one.
The next sweep must print exit 0 with its counts; if it still reads 1 the
instrument is the next suspect (rule 3), not the message.

QUEUE 260, builder: (a) the outbox WRITER refuses at write time when the
length exceeds the cap, printing `chars=<n>/4096`, so an oversized message
never enters the outbox; (b) the sweep classes a 400 as permanent, moves the
message to `outbox-blocked/` with the response body beside it, and never
retries it; retries are for 5xx, 429 and network only; (c) the sweep prints
`sent=<n> held=<n> blocked=<n>` every run. The decisive measurement for (b)
is the real poisoned message: one sweep with the classifier must move it
and print `blocked=1`. No test messages are sent to Jafar's channel.

Rejected: splitting oversized messages into several sends. The cap is a
producer-register rule (`.claude/agents/producer.md`), there to stop status
dumps; splitting would defeat the rule at the transport layer. Oversized
messages are rewritten to the register by their author or dropped.

Ordering: queue 259's link-floor fix must NOT land before 260's length gate,
or land with it. The held 4739-character message would otherwise be released
straight into the same 400. Both held messages are rewritten under the cap
or dropped; neither is sent as it stands.

## What was rejected, in one place

Runtime-proof coupling in the installer (section 2). A builder rewrite of
`container-setup.sh` (3). A two-numbers heuristic on the budget file (4).
Splitting Telegram messages (5). Reading `taskLastTaskResult=267009` as a
failure (1). Reading `verdict=WINDOWLESS` without `survivedSec=300/300` per
process and without a prior `WINDOWS-SEEN` from the instrument (1).

## Quality ladder at close

The fleet's next rung after WINDOWLESS is not blank: a single launcher for
the daemons that carries the flag once, so a twelfth site cannot exist to
forget it. That is a research task for the queue, not this batch.

## History

2026-09-11, same director spawn, on the coordinator's correction, before
commit. Section 1 item 1: the ast-check string corrected from
`noWindowSites=11/11` to `noWindowSites=20/20`, because the 11 was the
coordinator's count over the four files the builder was scoped to, and the
builder's derived fleet found nine more import-reachable sites that were the
ones actually opening windows. Section 1 item 3: the process roster reworded
from a fixed count of two to the roster the proof fixes after warmup
(`processesWatched=n/n`, two a floor, 5/5 in the run in hand), because a
condition that names a wrong count fails a correct run. The facts paragraph
above still carries the 11 as the number reported to me at the time of the
ruling; item 1 says which is current. Nothing else changed. Stamp unchanged:
the row it names is still the newest director row, and this is a correction
inside the record, not a new ruling.
