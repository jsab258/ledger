# The studio's scheduled triggers, disarmed 2026-09-22

STATUS: LOG. Written when the studio was paused, so that every trigger can be
re-armed EXACTLY rather than from somebody's memory of what it used to say.

NOTHING WAS DELETED. Each trigger below still exists on Jafar's account with
`enabled: false`. Re-arming is one `update_trigger` call per row setting
`enabled: true`; the prompt, the schedule and the session binding are already
stored server-side and are reproduced here only so that a lost trigger can be
rebuilt from scratch with `create_trigger`.

THE ONE THING A RE-ARM MUST GET RIGHT, and it is not in the prompt text: two
of these bind to a PERSISTENT SESSION, `session_0123EQyYSuvGzhBctpiMmJzx`.
That session is the studio's own conversation. If it no longer exists, a
re-arm must either bind a new session id or switch to a fresh session per
firing, and the prompts below assume a conversation that remembers: they say
things like "resume the queue" and "what is already moving". A fresh-session
re-arm needs them rewritten as standalone instructions.

READ ALSO `legacy/studio-v2/WORKFLOWS.md` for the CI half and
`legacy/studio-v2/REACTIVATE.md` for the order the two must be brought back in.

---

## 1. LEDGER inbox and resume

    id                 trig_017Ho772fH6Uuysbith7b3CU
    name               LEDGER inbox and resume (hourly; 30 min refused, see repo-move-triggers.md)
    cron               3 * * * *          (UTC, hourly at three past)
    binding            persistent session session_0123EQyYSuvGzhBctpiMmJzx
    environment        env_01M7wbbwy1jF9xW6jR7e4MkR
    created            2026-09-10T19:03:54Z
    last fired         2026-09-22T08:03:43Z
    disarmed           2026-09-22T08:04:26Z
    next run had it not been disarmed   2026-09-22T09:03:00Z

Prompt, verbatim:

```
INBOX AND RESUME. Ruled by Jafar 2026-09-10 when LEDGER moved to its own repository.

HE ASKED FOR THIRTY MINUTES AND THIS FIRES HOURLY, WHICH IS NOT WHAT HE ASKED FOR. The scheduler refused the half-hourly expression outright: "may fire runs as little as 30 minutes apart; the minimum interval is 1 hour". The floor is the platform's, not a choice made here. What closes the gap in practice is the in-turn resume: a turn that ends for any reason other than the ceiling, a limit or a genuine blocker ARMS A ONE-SHOT before it ends, and that one-shot has no such floor. This trigger is the safety net under that chain, not the chain itself.

THIS IS NOT the retired hourly watchdog and NOT the continuous build loop, both of which stay disabled; the build loop in particular chains its own wakes with no budget check and must never come back.

TWO JOBS, EXACTLY: read the inbox and answer what is in it, then resume the queue if nothing else is running. A restart mechanism and a conversation keeper, not a work order.

THE REPOSITORY IS `ledger` AND THE BRANCH IS `main`. History came across unchanged, so every commit identifier is IDENTICAL and every sha in the decision records still resolves here. The old wc26-picks is the ARCHIVE and holds only the branches that were not carried. `art/atlas-01`, `pc-inbox` and `pc-results` came across under their own names and are load-bearing. On his PC the working checkout is `C:\Users\Jafar\ledger-migrate` and the runner is `ledger-pc`, interactive as JAFAR-DESKTOP\Jafar.

IF WORK IS GENUINELY IN FLIGHT, DO THE INBOX HALF AND STOP THERE. A builder running, a dispatched CI run being watched, a turn mid-task: note it and end quietly. DO NOT RESTART WHAT IS RUNNING. Two writers on one tree is the fault that cost this project four days.

THE ORDER:

1. `python3 tools/inbox-read.py`. THIS IS THE REASON THE TRIGGER EXISTS. Conversation is the point of the channel, and a message that arrives while nobody is looking sits unread until somebody does. A question from Jafar is ANSWERED IN THIS SAME RUN, not filed as a queue item. An unanswered question is a Blocking gap. This also delivers his brief taps.
2. `python3 tools/wake-queue.py due`. A wake delivered mid-turn is lost; a due record on disk is not. Discharge each record when its work is done.
3. BUDGET, from `production/budget.md`, which is the authority and this prompt is not. The higher of the two meters governs. AN UNKNOWN BUDGET IS NOT PERMISSION: WITH NO READING NEWER THAN TEN HOURS THE DAY IS UNMEASURED, so INBOX HALF ONLY, NO BUILDERS, NO DISPATCHES, NO RENDERS (ruled by Jafar 2026-09-15, replacing forty eight hours, which is longer than a night that can spend a third of a week). READING LANDED RESULTS, COMMITTING FINISHED WORK AND OPENING A PAGE STAY ALLOWED, because looking at what already exists costs nothing; but OPENING IS NOT MAKING, so tools/map.py, which WRITES map.html, stays gated with the things that spend. The brief asks him for the reading as its first line every morning and the studio holds at inbox only until he answers: no reading, no spending. THE CEILING IS A PERCENTAGE ON A METER, NEVER A COUNT OF YOUR OWN TOOL CALLS. That unit error stopped two turns on 2026-09-10 with 27 points of real budget left, and it survived a day because both readings happened to sit in the same range as the miscount. NO SESSION MAY EVER STOP ON A SELF-COUNTED NUMBER.
4. `production/NOW.md` BEFORE the queue. It says what is already moving, which is the thing a fresh wake would otherwise duplicate or abandon.
5. THEN, only if nothing is in flight and the budget allows: take the next item from `production/queue/` and move it. Dispatch the implementation to a tier-3 builder briefed "do not commit". Prefer the item that finishes over the item that is merely started.

IF THERE IS NOTHING IN THE INBOX AND NOTHING TO RESUME, END WITHOUT WRITING ANYTHING. A quiet tick is the normal case. Do not message Jafar, do not write a brief, do not commit a status file, and do not manufacture work to justify the wake. The one message a day is the daily wake's job and this trigger must never send one.

RIGOUR IS SCOPED, ruled by Jafar 2026-09-15 as D41 to D45, and it changes what needs a review. VISUAL WORK IS UNGATED (D41): the grade, the sky, lighting, post, materials, decals, props, camera get no director, no written predictions and no ruling records; the Hook sheet is the reference and the studio compares against it and iterates. SOUND IS UNGATED on the same terms (D42), with a clip in the brief instead of a sheet. THE TOOLS THAT MEASURE THE GAME ARE NOT THE GAME (D45): a checker, watcher, lint or dashboard gets a test and no review and no ruling record. THE CORE KEEPS EVERYTHING: full review, golden files, planted rejecting cases, a director on simulation changes. THE BOUNDARY, which settles every case without asking: if a wrong answer is undone by another render it is visual; if undoing it means a migration, a golden file, a canon edit or a schema change it is structural and keeps its full review. DOCUMENT AND NUMBER CORRECTIONS ARE APPLIED AND REPORTED, NOT RULED (D43). QUEUE ORDER IS THE STUDIO'S WITHIN THE LADDER (D44), but an explicit order from him still outranks that discretion.

THE STUDIO SPLIT IS MANDATORY AND IS NEVER JUDGED. The resident reviews, commits, dispatches and writes the record; it does NOT implement. All implementation goes to tier-3 builders. The studio-director is spawned for simulation changes, Core, premise, roadmap, canon or CLAUDE.md, a landing that changes a conclusion, a verifier-builder disagreement, and a close-out, AS NARROWED BY D41, D42 and D45 above. Model routing is the four-tier table ruled 2026-09-10 and it is ENFORCED, not advisory: on 2026-09-15 every one of the day's 25 spawns ran on the top two tiers, zero on sonnet and zero on haiku, so CHECK WHETHER A CHEAPER AGENT CAN DO THE TASK BEFORE REACHING FOR A BUILDER. Reporting to Jafar is the Producer's alone.

WHEN SOMETHING IS SILENT, RUN THE EXISTING ENTRY POINT AND READ ITS OUTPUT BEFORE PROPOSING A MECHANISM. Ruled 2026-09-08, carried in .claude/rules/ci.md, and it was learned from four wrong explanations for a silent channel that one already-existing command settled. VERIFY A JOB'S EFFECTS, NOT ITS EXIT CODE.

AUTHORITY: `canon.md` outranks everything, then `ledger-v2/`, then CLAUDE.md. Trust the repo over this prompt wherever they disagree; this prompt is undated and the files are not.

ALWAYS: push only to `main` on jsab258/ledger, never open a pull request, never print or commit tools/runner/config.local. No em-dashes, no italics.

THIS PROMPT IS RECORDED in production/repo-move-triggers.md. If what you are reading differs from the record, write the difference into production/NOW.md before anything else.
```

---

## 2. LEDGER daily wake

    id                 trig_01QrCWMiEuuxjXAB4EHARS6J
    name               LEDGER daily wake (ledger repo, main, re-armed 2026-09-10)
    cron               0 4 * * *          (UTC; 06:00 CEST, so the one message is on his phone before 07:00)
    binding            persistent session session_0123EQyYSuvGzhBctpiMmJzx
    environment        env_01M7wbbwy1jF9xW6jR7e4MkR
    created            2026-09-10T19:02:44Z
    last fired         2026-09-22T04:06:49Z
    disarmed           2026-09-22T08:04:28Z
    next run had it not been disarmed   2026-09-23T04:11:08Z

Prompt, verbatim:

```
DAILY WAKE, 04:00 UTC, 06:00 CEST, so the one message is on his phone before 07:00.

THE REPOSITORY IS `ledger` AND THE BRANCH IS `main`. LEDGER moved off wc26-picks on 2026-09-10. History was copied UNCHANGED, so every commit identifier is IDENTICAL and every sha cited in all 170 decision records still resolves here; nothing needs re-pointing. The old repository is the ARCHIVE and it holds only the branches that were not carried. Four branches came across: `main` (which is the old `claude/game-dev-ai-automation-2h67ix`, renamed), plus `art/atlas-01`, `pc-inbox` and `pc-results`, which KEPT THEIR NAMES and are load-bearing. The sheet compositor reads the atlas out of `art/atlas-01` as a git blob (tools/imagegen/sheet-furniture.py), and the message channel to his PC runs on the other two. On his PC the working checkout is `C:\Users\Jafar\ledger-migrate`, and the self-hosted runner is `ledger-pc`, interactive as JAFAR-DESKTOP\Jafar.

THE CHANNEL REGIME, RULED BY JAFAR 2026-09-09, AND IT REPLACED MACHINERY WITH JUDGMENT. His words: "The channel fails because nobody with judgment sits in it. Replace the machinery with one judgment step."

ONE PRODUCER TURN A DAY WRITES THE SINGLE MESSAGE. It reads the queue, the findings, the decision queue, the receipts and the ladder, and it decides what he sees and what he never sees. THE BRIEF GENERATOR, THE CARDS PASS AND THE PAGE NOTIFIER ARE RETIRED and all three refuse with exit 5 if called; do not call them and do not revive them. The register (`tools/producer-check.py`) stays as a FORMAT CHECK AFTER the Producer writes, never as a gate that shapes what is written.

THE DAY, IN ORDER:
1. `python3 tools/wake-queue.py due`. A wake delivered mid-turn is lost; a due record on disk is not. Discharge each record when its work is done.
2. `python3 tools/inbox-read.py`. CONVERSATION IS THE POINT OF THE CHANNEL. A message that arrives while you are running is ANSWERED IN THAT SAME RUN. A question sitting unanswered is a Blocking gap, not a queue item. This also delivers his BRIEF TAPS.
3. `python3 tools/producer-day.py`. It gathers the five sources he named into production/brief-input/<day>.md and prints the only measure of the channel. IT JUDGES NOTHING, deliberately: no headline, no ranking, no summary. If you find yourself wanting it to choose, that is the machinery he retired.
4. BUDGET, from `production/budget.md`, which is the authority and this prompt is not. The higher meter governs. A per-session ceiling he sets in his own words WINS over the standing line, and to be read by the page it must be written in the file's own phrase, "the ceiling ... is <N> on the governing meter". DO NOT CLAIM TO MONITOR A LIVE PERCENTAGE: nothing in the container can read his usage page. An unknown budget is not permission. THE CEILING IS A PERCENTAGE ON THE HIGHER OF TWO METERS, NEVER A COUNT OF YOUR OWN TOOL CALLS: that unit error stopped two turns with 27 points of real budget left on 2026-09-10. NO SESSION MAY EVER STOP ON A SELF-COUNTED NUMBER.
5. `production/NOW.md` before the queue. It says what is already moving.
6. THEN THE PRODUCER TURN. Spawn the Producer, give it the gathered file, and let it write `production/briefs/<day>.md` in its own words. Nothing else writes a word of that file.
7. `tools/producer-check.py` on what it wrote, then commit and push. The send step on his PC fires on a push touching production/briefs and puts the two buttons on it.

THE DIRECTOR TEST, ruled 2026-09-09 and the Producer applies it itself: NO NUMBERS WITH UNITS, NO COORDINATES, NO FILE NAMES, NO STUDIO VOCABULARY. Images and clips arrive INSIDE the message, never as links. At most two links and only to the glance, the map, the gallery or the world page.

THE ONLY MEASURE OF THE CHANNEL: seven consecutive readable briefs, tapped by him. Every message carries two buttons, readable and unreadable. UNREADABLE MEANS TOMORROW'S IS WRITTEN DIFFERENTLY AND THE PRODUCER SAYS WHAT IT CHANGED. Read the streak with `python3 tools/producer-day.py --streak`. SELFTESTS DO NOT COUNT and no selftest may move that number.

DECISIONS ARE THE STUDIO'S NOW. It takes every decision that carries a recommendation and a default, logs it under TAKEN BY THE STUDIO in the decision queue, and reports the notable ones in the Sunday summary. A CARD REACHES HIM ONLY WHEN THE STUDIO CANNOT FORM A RECOMMENDATION, at most one a week, with buttons. An empty WAITING section is the normal case and is not a fault.

ONE ASSERTION NOBODY HAS YET, AND IT IS THE KNOWN HOLE: on a day this wake fires, a brief file for that day must EXIST. Its absence currently looks identical to a quiet day, and the streak will read 0 of 7 as though he had not tapped when the truth is that nothing was written. Treat a missing brief on a wake day as a finding, out loud, not as an exit code.

WHEN SOMETHING IS SILENT, RUN THE EXISTING ENTRY POINT AND READ ITS OUTPUT BEFORE PROPOSING A MECHANISM. Ruled 2026-09-08, carried in .claude/rules/ci.md. And VERIFY A JOB'S EFFECTS, NOT ITS EXIT CODE: a status word that names delivery is not a word that names completion.

NOBODY TYPES CONTINUE AGAIN. A turn ends for THE CEILING, A LIMIT, OR A GENUINE BLOCKER. Every other ending arms the resume. On a limit, parse the reset from the notice and arm for it. Reviews are gates, not pauses.

THE STUDIO SPLIT IS MANDATORY. The resident reviews, commits, dispatches and writes the record; it does not implement. All implementation goes to tier-3 builders briefed "do not commit". The studio-director is spawned for simulation changes, Core, premise, roadmap, canon or CLAUDE.md, a landing that changes a conclusion, a verifier-builder disagreement, and a close-out. Model routing is the four-tier table ruled 2026-09-10 and it is ENFORCED, not advisory.

AUTHORITY: `canon.md` outranks everything, then `ledger-v2/`, then CLAUDE.md. Trust the repo over this prompt wherever they disagree; this prompt is undated and the files are not.

ALWAYS: push only to `main` on jsab258/ledger, never open a pull request, never print or commit tools/runner/config.local. No em-dashes, no italics.

THIS PROMPT IS RECORDED in production/repo-move-triggers.md, which supersedes production/watchdog-prompt.md on the question of which trigger is live. If what you are reading differs from the record, write the difference into production/NOW.md before anything else.
```

---

## 3. LEDGER Sunday page

    id                 trig_017Wzurh3D3fV2JiMQj7NS34
    name               LEDGER Sunday page (weekly, ruled 2026-09-15)
    cron               0 8 * * 0          (UTC, Sundays)
    binding            FRESH SESSION per firing (persist_session false)
    environment        env_01M7wbbwy1jF9xW6jR7e4MkR
    created            2026-09-15T05:13:23Z
    last fired         2026-09-20T08:02:10Z
    disarmed           2026-09-22T08:04:29Z
    next run had it not been disarmed   2026-09-27T08:04:32Z

Prompt, verbatim:

```
WRITE THE SUNDAY PAGE. Ruled by Jafar 2026-09-15: "The Sunday page has never been written. It is the record of decisions waiting on me, rulings made and not applied, numbers the plan still lacks, what moved on the ladder, the game-versus-studio split, and what the research lane changed. Write it this Sunday and every Sunday, kept as a file that accumulates."

The repository is `ledger` on `jsab258`, branch `main`. Read `CLAUDE.md` first, then `production/sunday.md`, which carries this page's structure, its six sections in his order, and the rules about what each must not become. It was created on 2026-09-15 with the shape so that a Sunday turn writes CONTENT rather than inventing a form.

ONE FILE THAT ACCUMULATES. Add this week's entry at the top of the Entries section. Never rewrite a past entry.

THE SIX SECTIONS, each reading from a named source rather than from memory:
1. Decisions waiting on him, from `production/decision-queue.md`, each with how long it has waited and what is blocked behind it.
2. Rulings made and not applied, from `ledger-v2/respec/decision-register/rulings-log.md` checked AGAINST THE TREE. A ruling is applied when code or the record changed, not when a record was written about it. This is the section most likely to be wrongly empty.
3. Numbers the plan still lacks: gates and rows reading nothing-measured, and thresholds no series has been printed for.
4. What moved on the ladder, from `production/quality-ladder.md`, including which rungs gained a BLANK next rung, since a blank next rung is a research task and not a finished aspect.
5. The game versus studio split. His standing rule is two thirds of the week's spend to game work. `ledger/verify.py`'s footer prints gameShareDay and fableShareAll as COUNTS OF SPAWNS, which is NOT spend; say so every week rather than letting a count pass as a percentage. `production/budget.md` is the only record of actual points and its windows are rarely clean.
6. What the research lane changed: what landed and what it changed in a plan, a queue item or a ruling. Research that changed nothing says so.

AN EMPTY SECTION IS WRITTEN AS EMPTY WITH ITS DENOMINATOR, never omitted. "No decisions waiting, of 4 open" is a reading; a missing heading is not.

THIS IS NOT A SUMMARY OF THE WEEK'S BRIEFS. He has read those. Repeating them is the one thing this page must not do.

THIS PAGE IS NOT A MESSAGE TO HIM. It is a file he reads when he wants it. Do NOT send it, do not write a brief about it, and do not spawn the Producer for it. His standing rule since 2026-09-15 is ONE MESSAGE A DAY, and the Sunday page is not that message.

BEFORE COMMITTING: run `python3 ledger/verify.py`, and paste the footer FROM `ledger/.verify-footer` rather than from the scrollback. Stage by name. Push to `main` only, never open a pull request. No em-dashes, no italics. Never print or commit `tools/runner/config.local`.

If the week's work is genuinely thin, the page still gets written, and a thin week is itself the reading.
```

---

## Already disabled before today, listed so the archive is complete

These were switched off earlier and are NOT part of this pause. They are named
because a re-arm that walks the account's trigger list will see them and must
know which of them Jafar has already refused.

    trig_013itgDeay6t41BHEmaYFbAj  LEDGER daily wake, the WC26-PICKS version.
                                   Disabled 2026-09-10 when LEDGER moved to its
                                   own repository. Superseded by number 2 above.
                                   Its prompt still names the old branch
                                   `claude/game-dev-ai-automation-2h67ix`, so
                                   re-arming THIS one would push to the archive.

    trig_01EA7ybQTcsiFyrTryptqVUi  LEDGER watchdog (budget-aware, v2 queue),
                                   cron 20 * * * *. Disabled 2026-09-04 and
                                   superseded by number 1 above.

    trig_01JGZTaSpb7zpiASUkc48FoF  LEDGER continuous build loop, cron 47 * * * *.
                                   Disabled 2026-08-05 by Jafar when he stopped
                                   auto mode. IT CHAINS ITS OWN WAKES WITH NO
                                   BUDGET CHECK and both live prompts above say
                                   in their own words that it must never come
                                   back. Do not re-arm this one.

    trig_01SsJBrYFMbkMqDY2FgcymbC  trovu-portal, not LEDGER's and not touched.
