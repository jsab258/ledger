# The scheduled triggers, recorded so a fresh session on `ledger` can re-arm them

STATUS: LIVE, verified 2026-09-10. Written for the move to the new repository,
ruled by Jafar 2026-09-10. It supersedes `production/watchdog-prompt.md` on the
question of WHICH TRIGGER IS LIVE: that file is dated 2026-09-01 and describes
the hourly watchdog, which has been disabled since 2026-09-04.

WHY THIS FILE EXISTS. A trigger's prompt lives in the scheduling system, not in
the repository, so nothing inside the tree can prove what the studio is actually
told to do each morning. When this session's triggers are disabled and a new
session starts on `ledger`, the prompt is gone unless it was written down first.

## The state at the move, read from the scheduler on 2026-09-10

    trig_013itgDeay6t41BHEmaYFbAj  ENABLED   0 4 * * *    the daily wake
    trig_01EA7ybQTcsiFyrTryptqVUi  disabled  20 * * * *   the hourly watchdog
    trig_01JGZTaSpb7zpiASUkc48FoF  disabled  47 * * * *   the continuous build loop

All three bind to the session persisted as `session_01GmRn6ayehpVYDAoQE5DKQo`
in environment `env_01M7wbbwy1jF9xW6jR7e4MkR`. A fourth trigger on the account
belongs to another project entirely and is not ours; leave it alone.

ONE IS ENABLED. The other two are kept here as history because their prompts
carry rulings that are still binding, not because they should be revived. The
continuous build loop in particular was stopped by Jafar on 5 August and its
prompt names an agent identity that no longer applies; do not re-arm it.

## WHAT MUST CHANGE BEFORE RE-ARMING ON `ledger`

Four things, and all four are wrong by construction if the prompt is copied
across unedited:

1. THE BRANCH. The prompt says "push only to
   `claude/game-dev-ai-automation-2h67ix`". On the new repository that branch
   becomes `main`. A prompt that names the old branch will either push nowhere
   or, worse, push to a branch that still exists in the archive.
2. THE SESSION. `persistent_session_id` names this session. A new trigger must
   bind to the new session, or fire into a session that is no longer working.
3. THE ARCHIVE SENTENCE, AND IT IS NOT THE ONE THIS FILE FIRST GAVE. The
   first version of this line said every commit identifier written before
   2026-09-10 would resolve only in the archive, because moving the large files
   through history rewrote them. THAT IS NO LONGER TRUE AND WAS NEVER RUN:
   Jafar ruled a few hours later that there is no Large File Storage and no
   rewrite, so history is copied unchanged and EVERY IDENTIFIER IS IDENTICAL.
   Decision records keep resolving against the new repository. The sentence a
   new prompt needs is the smaller one: the old repository is the archive, and
   it holds the branches that were not carried.
4. THE FOUR BRANCHES. `art/atlas-01`, `pc-inbox` and `pc-results` are carried
   across by the migration and are load-bearing: the sheet compositor reads the
   atlas branch directly at `tools/imagegen/sheet-furniture.py:49`, and the
   message channel to the PC runs on the other two. Anything that names them
   keeps working only if they arrived.

## How to re-arm, once the new session exists

One trigger, the daily wake. Fire into the new persistent session, cron
`0 4 * * *`, which is 06:00 in Zurich so the single message is on his phone
before 07:00. Do not re-arm the other two.

## THE LIVE PROMPT, VERBATIM

Everything between the markers is the prompt as the scheduler holds it on
2026-09-10, copied without edit. The four corrections above are NOT applied
here on purpose: this is the record of what was, and a record that quietly
improves itself is not a record.

<<<BEGIN DAILY WAKE PROMPT>>>

DAILY WAKE, 04:00 UTC, 06:00 CEST, so the one message is on his phone before 07:00.

THE CHANNEL REGIME, RULED BY JAFAR 2026-09-09, AND IT REPLACED MACHINERY WITH JUDGMENT. His words: "The channel fails because nobody with judgment sits in it. Replace the machinery with one judgment step."

ONE PRODUCER TURN A DAY WRITES THE SINGLE MESSAGE. It reads the queue, the findings, the decision queue, the receipts and the ladder, and it decides what he sees and what he never sees. THE BRIEF GENERATOR, THE CARDS PASS AND THE PAGE NOTIFIER ARE RETIRED and all three refuse with exit 5 if called; do not call them and do not revive them. The register (`tools/producer-check.py`) stays as a FORMAT CHECK AFTER the Producer writes, never as a gate that shapes what is written.

THE DAY, IN ORDER:
1. `python3 tools/wake-queue.py due`. A wake delivered mid-turn is lost; a due record on disk is not. Discharge each record when its work is done.
2. `python3 tools/inbox-read.py`. CONVERSATION IS THE POINT OF THE CHANNEL. A message that arrives while you are running is ANSWERED IN THAT SAME RUN. A question sitting unanswered is a Blocking gap, not a queue item. This also delivers his BRIEF TAPS.
3. `python3 tools/producer-day.py`. It gathers the five sources he named into production/brief-input/<day>.md and prints the only measure of the channel. IT JUDGES NOTHING, deliberately: no headline, no ranking, no summary. If you find yourself wanting it to choose, that is the machinery he retired.
4. BUDGET, from `production/budget.md`, which is the authority and this prompt is not. The higher meter governs. A per-session ceiling he sets in his own words WINS over the standing line, and to be read by the page it must be written in the file's own phrase, "the ceiling ... is <N> on the governing meter". DO NOT CLAIM TO MONITOR A LIVE PERCENTAGE: nothing in the container can read his usage page. An unknown budget is not permission.
5. `production/NOW.md` before the queue. It says what is already moving.
6. THEN THE PRODUCER TURN. Spawn the Producer, give it the gathered file, and let it write `production/briefs/<day>.md` in its own words. Nothing else writes a word of that file.
7. `tools/producer-check.py` on what it wrote, then commit and push. The send step on his PC fires on a push touching production/briefs and puts the two buttons on it.

THE DIRECTOR TEST, ruled 2026-09-09 and the Producer applies it itself: NO NUMBERS WITH UNITS, NO COORDINATES, NO FILE NAMES, NO STUDIO VOCABULARY. Images and clips arrive INSIDE the message, never as links. At most two links and only to the glance, the map, the gallery or the world page.

THE ONLY MEASURE OF THE CHANNEL: seven consecutive readable briefs, tapped by him. Every message carries two buttons, readable and unreadable. UNREADABLE MEANS TOMORROW'S IS WRITTEN DIFFERENTLY AND THE PRODUCER SAYS WHAT IT CHANGED. Read the streak with `python3 tools/producer-day.py --streak`. SELFTESTS DO NOT COUNT and no selftest may move that number.

DECISIONS ARE THE STUDIO'S NOW. It takes every decision that carries a recommendation and a default, logs it under TAKEN BY THE STUDIO in the decision queue, and reports the notable ones in the Sunday summary. A CARD REACHES HIM ONLY WHEN THE STUDIO CANNOT FORM A RECOMMENDATION, at most one a week, with buttons. An empty WAITING section is the normal case and is not a fault.

ONE ASSERTION NOBODY HAS YET, AND IT IS THE KNOWN HOLE: on a day this wake fires, a brief file for that day must EXIST. Its absence currently looks identical to a quiet day, and the streak will read 0 of 7 as though he had not tapped when the truth is that nothing was written. Treat a missing brief on a wake day as a finding, out loud, not as an exit code.

WHEN SOMETHING IS SILENT, RUN THE EXISTING ENTRY POINT AND READ ITS OUTPUT BEFORE PROPOSING A MECHANISM. Ruled 2026-09-08, carried in .claude/rules/ci.md. And VERIFY A JOB'S EFFECTS, NOT ITS EXIT CODE: a status word that names delivery is not a word that names completion.

NOBODY TYPES CONTINUE AGAIN. A turn ends for THE CEILING, A LIMIT, OR A GENUINE BLOCKER. Every other ending arms the resume. On a limit, parse the reset from the notice and arm for it. Reviews are gates, not pauses.

THE STUDIO SPLIT IS MANDATORY. The resident reviews, commits, dispatches and writes the record; it does not implement. All implementation goes to tier-3 builders briefed "do not commit". The studio-director is spawned for simulation changes, Core, premise, roadmap, canon or CLAUDE.md, a landing that changes a conclusion, a verifier-builder disagreement, and a close-out.

AUTHORITY: `canon.md` outranks everything, then `ledger-v2/`, then CLAUDE.md. Trust the repo over this prompt wherever they disagree; this prompt is undated and the files are not.

ALWAYS: push only to claude/game-dev-ai-automation-2h67ix, never open a pull request, never print or commit tools/runner/config.local. No em-dashes, no italics.

THIS PROMPT IS RECORDED in production/watchdog-prompt.md. If what you are reading differs, write the difference into production/NOW.md before anything else.

<<<END DAILY WAKE PROMPT>>>

## The two disabled prompts

Both are recorded in full in `production/watchdog-prompt.md`, which stays for
that purpose. The hourly watchdog, `trig_01EA7ybQTcsiFyrTryptqVUi`, was
disabled 2026-09-04 when the daily wake replaced it. The continuous build loop,
`trig_01JGZTaSpb7zpiASUkc48FoF`, was disabled by Jafar on 5 August when he
stopped auto mode, and its prompt tells a session to chain its own wake-ups
without a budget check, which is why it must not come back.

## The last line of this session

The daily trigger is disabled on this session's final turn, by Jafar's
instruction, so that nothing fires into a session working on an archived
repository. Disabling is not deleting: the trigger keeps its identifier and its
run history, and the prompt above is the copy a new session works from.


## RE-ARMED 2026-09-10 ON THE NEW REPOSITORY, and what changed in the doing

Two triggers are live on `ledger`, both bound to the session persisted as
`session_0123EQyYSuvGzhBctpiMmJzx` in environment `env_01M7wbbwy1jF9xW6jR7e4MkR`.
The three old triggers stay DISABLED and keep their identifiers and run
histories, which is why disabling was never deleting.

    trig_01QrCWMiEuuxjXAB4EHARS6J  ENABLED  0 4 * * *   the daily wake
    trig_017Ho772fH6Uuysbith7b3CU  ENABLED  3 * * * *   inbox and resume

### The daily wake: the four edits, applied, plus one correction

Recorded as the exact replacement text rather than as a description, so the
live prompt is reconstructible from this file: take the verbatim prompt above
and apply these. Nothing else in it changed.

1. THE BRANCH. The closing ALWAYS line now reads "push only to `main` on
   jsab258/ledger" in place of the old branch name.
2. THE SESSION. Bound to `session_0123EQyYSuvGzhBctpiMmJzx`, not to the
   session that worked the archive.
3 and 4. THE ARCHIVE SENTENCE AND THE FOUR BRANCHES, which arrive together as
   one new second paragraph, immediately after the opening line:

       THE REPOSITORY IS `ledger` AND THE BRANCH IS `main`. LEDGER moved off
       wc26-picks on 2026-09-10. History was copied UNCHANGED, so every commit
       identifier is IDENTICAL and every sha cited in all 170 decision records
       still resolves here; nothing needs re-pointing. The old repository is
       the ARCHIVE and it holds only the branches that were not carried. Four
       branches came across: `main` (which is the old
       `claude/game-dev-ai-automation-2h67ix`, renamed), plus `art/atlas-01`,
       `pc-inbox` and `pc-results`, which KEPT THEIR NAMES and are
       load-bearing. The sheet compositor reads the atlas out of
       `art/atlas-01` as a git blob (tools/imagegen/sheet-furniture.py), and
       the message channel to his PC runs on the other two. On his PC the
       working checkout is `C:\Users\Jafar\ledger-migrate`, and the
       self-hosted runner is `ledger-pc`, interactive as JAFAR-DESKTOP\Jafar.

THE FIFTH EDIT, WHICH THE FOUR DID NOT NAME. The closing pointer said the
prompt was recorded in `production/watchdog-prompt.md`. It now names THIS
file, which that one already declares itself superseded by on the question of
which trigger is live. A pointer to the wrong record is the same fault as a
wrong record, and leaving it would have sent the next reader to the hourly
watchdog.

Two sentences were also carried in from rulings made after the prompt was
written, both of which the prompt would otherwise contradict: the budget
ceiling is a percentage on a meter and never a count of your own tool calls,
and model routing is the enforced four-tier table.

### The inbox and resume trigger: it does not fire every thirty minutes

Jafar asked for thirty minutes. The scheduler refused the expression outright:

    cron expression "0,30 * * * *" may fire runs as little as 30 minutes
    apart; the minimum interval is 1 hour (cron interval too short)

So it is armed hourly. TWO OFFSET HOURLY TRIGGERS WOULD PRODUCE A THIRTY
MINUTE CADENCE AND THAT WAS DELIBERATELY NOT DONE: each would pass the check
alone while together they are exactly what the floor forbids, and routing
around a stated platform limit is not a decision a session takes on its own.
It is recorded here as an option for Jafar rather than taken.

What closes the gap meanwhile is the in-turn resume CLAUDE.md rule 13 already
requires: a turn ending for anything other than the ceiling, a limit or a
genuine blocker ARMS A ONE-SHOT, and a one-shot has no hourly floor. The
hourly trigger is the safety net under that chain and was never the chain.

THE CRON MINUTE IS 3 AND NOT 0, WHICH NOBODY CHOSE EITHER. An hourly
expression at minute 0 is anchored server-side to the minute it was created,
so Routines spread across the hour instead of all firing at the top of it.
`0 * * * *` was sent and `3 * * * *` was stored. Read the stored value, never
the one that was submitted.

### ONE HOLE BOTH TRIGGERS HAVE, and it is a hole rather than a note

Neither stores any connector, and the tool that created them said so:

    warning: this trigger stores no MCP connectors, so the sessions it fires
    will run without connector (mcp__<server>__*) tools

Connectors pass through only from a session that itself holds them in a
passable form, and this one had none to pass. Both prompts are written in
terms of `python3 tools/...` and git, which need no connector, so the daily
message and the inbox read are unaffected. WHAT IS AFFECTED IS ANYTHING THAT
DISPATCHES A WORKFLOW OR READS A RUN, because that goes through the GitHub
tools: a fired session that needs to start a build may find it cannot, and
CI is the only feedback channel this project has. Untested either way as of
this writing, which is the honest state. The remedy the warning names is to
create the trigger from a session holding the connectors, or from the
Routines page on claude.ai.

### THE INBOX AND RESUME PROMPT, VERBATIM

This one exists nowhere else, so it is carried in full rather than as a diff.

<<<BEGIN INBOX AND RESUME PROMPT>>>

INBOX AND RESUME. Ruled by Jafar 2026-09-10 when LEDGER moved to its own repository.

HE ASKED FOR THIRTY MINUTES AND THIS FIRES HOURLY, WHICH IS NOT WHAT HE ASKED FOR. The scheduler refused the half-hourly expression outright: "may fire runs as little as 30 minutes apart; the minimum interval is 1 hour". The floor is the platform's, not a choice made here. What closes the gap in practice is the in-turn resume: a turn that ends for any reason other than the ceiling, a limit or a genuine blocker ARMS A ONE-SHOT before it ends, and that one-shot has no such floor. This trigger is the safety net under that chain, not the chain itself.

THIS IS NOT the retired hourly watchdog and NOT the continuous build loop, both of which stay disabled; the build loop in particular chains its own wakes with no budget check and must never come back.

TWO JOBS, EXACTLY: read the inbox and answer what is in it, then resume the queue if nothing else is running. A restart mechanism and a conversation keeper, not a work order.

THE REPOSITORY IS `ledger` AND THE BRANCH IS `main`. History came across unchanged, so every commit identifier is IDENTICAL and every sha in the decision records still resolves here. The old wc26-picks is the ARCHIVE and holds only the branches that were not carried. `art/atlas-01`, `pc-inbox` and `pc-results` came across under their own names and are load-bearing. On his PC the working checkout is `C:\Users\Jafar\ledger-migrate` and the runner is `ledger-pc`, interactive as JAFAR-DESKTOP\Jafar.

IF WORK IS GENUINELY IN FLIGHT, DO THE INBOX HALF AND STOP THERE. A builder running, a dispatched CI run being watched, a turn mid-task: note it and end quietly. DO NOT RESTART WHAT IS RUNNING. Two writers on one tree is the fault that cost this project four days.

THE ORDER:

1. `python3 tools/inbox-read.py`. THIS IS THE REASON THE TRIGGER EXISTS. Conversation is the point of the channel, and a message that arrives while nobody is looking sits unread until somebody does. A question from Jafar is ANSWERED IN THIS SAME RUN, not filed as a queue item. An unanswered question is a Blocking gap. This also delivers his brief taps.
2. `python3 tools/wake-queue.py due`. A wake delivered mid-turn is lost; a due record on disk is not. Discharge each record when its work is done.
3. BUDGET, from `production/budget.md`, which is the authority and this prompt is not. The higher of the two meters governs. AN UNKNOWN BUDGET IS NOT PERMISSION: with no reading newer than 48 hours, do only work that costs no model time, and the inbox half is that work. THE CEILING IS A PERCENTAGE ON A METER, NEVER A COUNT OF YOUR OWN TOOL CALLS. That unit error stopped two turns on 2026-09-10 with 27 points of real budget left, and it survived a day because both readings happened to sit in the same range as the miscount. NO SESSION MAY EVER STOP ON A SELF-COUNTED NUMBER.
4. `production/NOW.md` BEFORE the queue. It says what is already moving, which is the thing a fresh wake would otherwise duplicate or abandon.
5. THEN, only if nothing is in flight and the budget allows: take the next item from `production/queue/` and move it. Dispatch the implementation to a tier-3 builder briefed "do not commit". Prefer the item that finishes over the item that is merely started.

IF THERE IS NOTHING IN THE INBOX AND NOTHING TO RESUME, END WITHOUT WRITING ANYTHING. A quiet tick is the normal case. Do not message Jafar, do not write a brief, do not commit a status file, and do not manufacture work to justify the wake. The one message a day is the daily wake's job and this trigger must never send one.

THE STUDIO SPLIT IS MANDATORY AND IS NEVER JUDGED. The resident reviews, commits, dispatches and writes the record; it does NOT implement. All implementation goes to tier-3 builders. The studio-director is spawned for simulation changes, Core, premise, roadmap, canon or CLAUDE.md, a landing that changes a conclusion, a verifier-builder disagreement, and a close-out. Model routing is the four-tier table ruled 2026-09-10 and it is ENFORCED, not advisory. Reporting to Jafar is the Producer's alone.

WHEN SOMETHING IS SILENT, RUN THE EXISTING ENTRY POINT AND READ ITS OUTPUT BEFORE PROPOSING A MECHANISM. Ruled 2026-09-08, carried in .claude/rules/ci.md, and it was learned from four wrong explanations for a silent channel that one already-existing command settled. VERIFY A JOB'S EFFECTS, NOT ITS EXIT CODE.

AUTHORITY: `canon.md` outranks everything, then `ledger-v2/`, then CLAUDE.md. Trust the repo over this prompt wherever they disagree; this prompt is undated and the files are not.

ALWAYS: push only to `main` on jsab258/ledger, never open a pull request, never print or commit tools/runner/config.local. No em-dashes, no italics.

THIS PROMPT IS RECORDED in production/repo-move-triggers.md. If what you are reading differs from the record, write the difference into production/NOW.md before anything else.

<<<END INBOX AND RESUME PROMPT>>>
