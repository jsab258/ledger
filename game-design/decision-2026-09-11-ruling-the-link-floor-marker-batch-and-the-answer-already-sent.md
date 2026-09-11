<!--RULING spawn=2026-09-11T13:39:39Z-->
# LOG: ruling on the link-floor marker batch, and on the answer Jafar already received, 2026-09-11

> **STATUS: LOG, 2026-09-11. NOT CURRENT** once section 10 carries the printed
> numbers and queue 261 has landed. Decision record, binding on the resident,
> on the builder who applies section 3, on the Producer who applies section 6,
> and on the builders briefed from section 5.

Author: tier-1 director spawned 2026-09-11T13:39:39Z, row 555 of
`.claude/agent-log.tsv`, read this session; the row reads
`2026-09-11T13:39:39Z` TAB `studio-director` TAB `fable` TAB `default` TAB
`a1a0c7e09c77f158a`, and it is the only `studio-director` row newer than the
reference commit `1aedef87@2026-09-11T07:02:42Z` (rows 546 and 549 are 06:09Z
and 06:43Z, older). A resident never stamps a ruling; if the gate reports this
stamp unmatched or stale, the numbers go into section 10 and the stamp is not
touched.

## 0. What was read, what was not run

No shell in this seat: read, grep and glob only. Nothing below came from
running `git`, `verify.py`, any selftest or `wc`; the resident prints every
number in section 9 before the commit, and a number in this record that the
resident's print contradicts is wrong here, not there. I could not run
`git diff --cached`, so the file reviewed is `tools/producer-check.py` AS IT
SITS IN THE WORKING TREE; section 9 condition 2 makes the resident prove the
working tree and the index are one file.

Read whole: CLAUDE.md, the 2026-09-10 ruling record, queues 256, 259, 260 and
261, `production/site-served.txt`, `production/outbox/README.md`,
`production/outbox-blocked/README.md`, the answer
`production/outbox/2026-09-11-yes-it-works.answer.md`,
`production/pc-ops/supervisor-status.txt`, `.claude/agents/producer.md`, and
`tools/producer-check.py` lines 1 to 1700, 2530 to 2790, 2905 to 2965 and
3225 to 3336. Read in part: `tools/runner/executor.py` (1 to 110, 170 to 200,
340 to 440, 1000 to 1095, 1128 to 1182, 1360 to 1420, 1480 to 1600, 1780 to
1800), `tools/runner/outbox.py` (grep of `run_check` and the receipt shapes),
`tools/supervise.py` 300 to 333, `ledger/verify.py` 1686 to 1730, 3225 to
3260, 4098 to 4210, `.github/workflows/ledger-install-supervisor-task.yml` 870
to 975, `production/NOW.md` 1 to 239, and today's windowless ruling 125 to 185.

**Premise check.** A process ruling about the channel to Jafar. Nothing here
touches Meridian, the era, the moat or the visual bar; section 0 of CLAUDE.md
is unchanged.

## 1. The batch as reviewed, and the one number that does not match

The batch does what the brief says. `link_floor_state()` (lines 400 to 445)
reads one file, returns four outcomes, three of them strict, and every branch
carries a space-free reason token. `check()` is still pure: the reading is
taken at the call site (`main()` line 3324, `gate()` line 2925) and a caller
that passes nothing gets `FLOOR_NOT_CONSULTED`, which is the strict default.
The rule leaves `enforced` rather than being skipped, so it lands under NOT
ENFORCED and on `rulesNotEnforced=` (lines 961 to 962). The report prints the
ruled band and the effective band as a pair on one line (1358 to 1369) and
the floor's branch with its reason on another (1386 to 1396). The gate reads
the marker ONCE for the walk (2925) and prints `filesLinkFloorOff=N/checked`
beside `linkFloorActive=` (3242 to 3255). The ladder (2534 to 2738) is one
message, three rungs, one run, and it also re-drives every rejecting fixture
with the floor suspended and requires all but `linkfloor` to still refuse
(2678 to 2694), which is the half that proves the suspension is narrow.
`LINK_MIN` is still 1, `SITE_PAGES` is unchanged, `linkcap` and `linkdest`
are re-proven on the suspended rung (2650 to 2672). No threshold moved.

The marker file's header lines that show `servedCommit=` as examples (lines
40 and 41) begin with `#`, and `SERVED_LINE_RE` anchors on `^\s*servedCommit=`,
so they cannot be counted; the selftest asserts the live file reads exactly
one line (2543 to 2549). Good.

THE NUMBER THAT DOES NOT MATCH. The resident's pasted selftest line says
`5 marker fixture(s)`. The done line prints `len(floor_cases) + 3` (line
2784), and `floor_cases` in the file I read has FOUR members (2555 to 2567:
none, a served commit, no line, two lines), so the file I read prints 7.
Either the tested file is older than the staged one, or the transcription is
wrong. `ledger/verify.py` runs `--gate` only (1711 to 1712), never
`--selftest`, so the commit would not catch it. Section 9 condition 2.

## 2. The seven calls

**(a) A committed marker, not an edited constant: UPHELD.** Three reasons,
each of which the constant fails. First, a constant is a session's opinion
about a page it never loaded; the marker is a fact with a named writer, and
the run that proves the page is the run that flips it. Second, the branch
prints on every run, pass or fail, in both entry points, so a rule that
stopped biting cannot read like a rule that passed; an edited constant prints
nothing and the suspension becomes invisible the day it is made. Third, the
flip back is one data line in the same commit as the origin move, and the
selftest pins the marker's shape and not its value, so doing the work the
marker prompts cannot break the tool. The alternative rests on "remembering
to put it back", and every casebook in this project is a list of things
nobody remembered. One cost, named: the marker is a second copy of a fact CI
will print. Section 3 and queue 256 tie the copy to its source.

**(b) The fail-safe direction: UPHELD.** An absent, unreadable or malformed
marker leaves the floor LIVE. That refuses a linkless message, which in
today's world is the wrong verdict, and it is still the right direction:
the refusal is loud on a channel we read (the sender writes a refusal record
to `pc-inbox` carrying the DO NOT SEND line, which now carries
`linkFloorActive=true reason=marker-absent..`), while the other direction
sends a message with no evidence because nobody could read the fact, which
is the silent-instrument failure by name. Consistent with
`outbox.py:run_check`, where a check that could not run is DO NOT SEND. The
accepting case is rung one of the ladder; the planted condition is rung two.
Rule 5b is met on both halves.

**(c) A typed sha: A HOLE, and it is closed by A1 in this batch.** Nothing
mechanical stops a session typing a sha into the marker. The prevention today
is a sentence in two files, and the effect of ignoring it is worse than it
looks: a sha turns the floor back to 1..2 while `SITE_ORIGIN` still names
the archive, so a linkless message is refused and a message carrying the
ARCHIVE link is accepted. A typed sha therefore FORCES the stale link, which
is the 2026-09-09 fault. The guard is small and decisive: while the marker
names a served commit, `SITE_ORIGIN` may not be the archive origin, checked
in the GATE (the entry point verify runs) and not only in the selftest.
Section 3 specifies it. The second half, that `printedBy=` names a CI
commit that carries the same sha, needs git and the verdict file's name,
and goes to queue 256 (section 5).

**(d) The batch may commit, under section 9, with A1 and the revised answer
in it, and with this morning's ordering narrowed in writing (section 4).**

**(e) The executor's archive link: ITS OWN ITEM, queue 262, ordered before
256.** Not this batch: the batch is the register, the executor is a daemon
with a selftest that asserts the opposite (`executor.py` line 1844,
`a.count(SITE_LINK) == 1`), and a fault in one must not hold the other. Not
256: 256 moves the DESTINATION after a page is served; the hole is that the
executor ADDS a link during the window in which the register allows zero,
and it is wider than the fallbacks: `compose_answer` (371 to 394) appends
`The board: <archive>` to EVERY session answer that carries no site link.
The floor suspension governs what the register refuses, not what the
executor writes, so the link the ruling exists to keep off his phone will
ride every executor reply until 262 lands. Dictated in section 5.

**(f) The Producer's reply: REVISED, then sent. Not as written, not dropped.**
He asked "Is this working?" and 107 seconds later his phone read "The machine
cannot start the work you asked for: the tool it needs is not available on
this machine right now", plus the archive link. A person reads that as "no".
The Producer's draft opens "Yes" and never mentions the note he already has,
so as written he receives two answers that contradict each other. Dropping
it leaves the wrong answer standing, and the outcome DID change for him (the
channel works both ways, which is what he asked), so the register's own rule
applies: one line, because the outcome changed. Section 6 says what the
revision must carry and what it may not.

**(g) The executor's `cli` keys: QUEUE 261, the NEXT builder dispatch in this
session, not this batch.** Rule 12 orders the channel fix before anything
else, and it is satisfied by ORDER: 261 is briefed and dispatched the moment
this batch is pushed, ahead of 262, 260 and 256. It does not go in this batch
because the message to Jafar waits on this batch and a daemon change carries
its own way of blocking it; because the daemon half takes effect only when
the executor process on his PC restarts, so thirty minutes costs nothing
measurable; and because the cheapest decisive measurement of TODAY's fault is
not a daemon change at all but two more sources in a CI copy step that
already exists (section 5, 261 deliverable 1), and a workflow edit fires a PC
run that should not be coupled to a register commit. What ships, with keys,
denominators and the never-ran wording, is in section 5 so the brief is the
ruling's words and not a paraphrase.

## 3. Amendment A1, IN THIS BATCH, blocking, a builder edit to `tools/producer-check.py`

One named constant, one pure function, one gate finding, two fixtures.

- `ARCHIVE_ORIGIN = "https://jsab258.github.io/wc26-picks/"`, beside
  `SITE_ORIGIN`, with the comment that it is the origin a link must NEVER
  point at after the move, and that it is kept after 256 flips `SITE_ORIGIN`
  BECAUSE a rejecting fixture must name what it rejects.
- `marker_origin_consistent(reading, site_origin)` returning
  `(ok, reason)`: `ok` is True whenever `reading["active"]` is False or the
  reading's `served` is None (floor live for an absent or malformed marker
  is A1's business only in that it passes); it is False exactly when the
  marker names a served commit AND `norm_url(site_origin) ==
  norm_url(ARCHIVE_ORIGIN)`. The reason token has no spaces:
  `marker-names-served-commit-but-SITE_ORIGIN-is-the-archive..<marker>`.
- `gate()` calls it once with the reading it already takes at line 2925 and
  `SITE_ORIGIN`; a False result is a whole-run failure that
  `gate_report()` prints as its own line and as `markerOriginConsistent=false`
  on the done line, with `GATE_EXIT_FAIL`. On a pass the done line carries
  `markerOriginConsistent=true`. The single-file path prints the same key on
  its done line and does NOT fail on it, because the sender on the PC must
  not be the place this is discovered; the gate is.
- Selftest, accepting case FIRST: the live tree reads
  `markerOriginConsistent=true` (marker `none`, origin the archive). Then the
  rejecting rung, SYNTHETIC: a `_gate_tree` carrying `servedCommit=0bc1def2`
  graded with `site_origin=ARCHIVE_ORIGIN` fails by this finding and nothing
  else; and the same tree with `site_origin="https://jsab258.github.io/ledger/"`
  passes, so the guard is seen to accept the state 256 will produce. The
  origin is a PARAMETER of `gate()` defaulting to `SITE_ORIGIN`, so the
  fixture does not need the module constant to be the archive on the day it
  runs.

Bound on size: if A1 exceeds about sixty changed lines, or the builder round
is not back when the Producer's revision (section 6) is, the resident lands
the batch WITHOUT A1, records that in section 10, and A1 becomes the first
deliverable of queue 256, which may not write a sha until it exists.
(Superseded by the History entry at the foot of this record: measured 83,
KEPT.)

## 4. This morning's ordering against queue 260, narrowed

Today's windowless ruling, section 5: "queue 259's link-floor fix must NOT
land before 260's length gate, or land with it. The held 4739-character
message would otherwise be released straight into the same 400." The hazard
named is the RELEASE of a held message into the live outbox. This batch
releases nothing from `production/outbox-blocked/`: both held messages stay
there, and 259's done item 4 (move the held message back, empty the
directory) is the part that now WAITS on 260 and on the Producer rewriting
both held messages under the cap or dropping them, exactly as ruled. The
code half of 259 lands now because the only message it releases is
today's answer, whose length the resident prints (section 9 condition 6)
and which must read under 4096. The ordering ruling is not overturned; it
is attached to the item it was written for.

## 5. Queue amendments, resident to apply

**256, two additions.** (i) Provenance: when the marker gains a sha, its
`printedBy=` names the short sha of the CI commit that carries the
`publish-glance` verdict file, and `ledger/verify.py` (which has `_git`)
checks that commit exists and that a file in it carries
`servedCommit=<the same sha>`; a marker whose provenance cannot be found is
a red gate, not a warning. (ii) The done line's `grep -rn
'github.io/wc26-picks' tools/` at 0 becomes "at 0 outside `ARCHIVE_ORIGIN`
and the rejecting fixtures that name it", because A1 keeps that string on
purpose.

**259, one note.** Done item 4 waits on 260 (section 4). Items 1 to 3 land
with this batch; item 2 is satisfied by construction (`run_check` shells out
to the single-file path with no `--root`, so it reads the marker in its own
checkout) and is PROVEN only by the receipt in section 9 condition 8.

**261, deliverables restated from this ruling.** Deliverable 1, the cheapest
decisive measurement, a workflow edit: the "Publish the supervisor's own
status" step in `ledger-install-supervisor-task.yml` (870 to 908) gains two
more sources copied the same way, each with its own `statusFound=`,
`statusAgeSec=` and `statusFresh=` head and the NOTHING MEASURED wording when
absent: `C:\Users\Jafar\ledger-migrate\game-design\pc-jobs\executor-status.txt`
into `production/pc-ops/executor-status.txt`, and the LAST 40 lines of
`C:\Users\Jafar\ledger-exec-state\journal.log` into
`production/pc-ops/executor-journal-tail.txt` with the cap announced as
`journalLines=<shown>/<total>`. Both staged BY NAME with `-A` beside line 968.
The push that lands this fires the run, and that run prints the 13:18Z
`no-cli ... why=` record. Deliverable 2, the daemon half, `executor.py` and
`supervise.py` with their selftests: the executor's status file gains
`cliLastStart=started|not-started|nothing-measured` (LAST-WINS over sessions
this process attempted; the words until the first attempt),
`cliWhy=<oneword of res["why"]>|none|nothing-measured` (the reason of the
last not-started session in `run_session`'s own words, so `not-on-PATH`,
`would-not-start/<ExceptionName>` and `log-could-not-be-opened/<ExceptionName>`
stay distinct; `none` when the last session started), and
`sessionsStarted=<n>/<attempted>` (CUMULATIVE since process start;
`nothing-measured` when attempted is 0, never `0/0`). `supervise.py:
executor_keys` publishes them as `executorCli=`, `executorCliLastStart=`,
`executorCliWhy=`, `executorSessionsStarted=`, and when the executor's file
predates the keys (an old process still running after the code lands, which
WILL be the state on the first run) prints `nothing-measured/key-absent`,
never `unreadable`. `cli=found` stays and is documented as "which() resolved
the name", which A6 in that file shows is not proof it starts. The accepting
case for deliverable 2 (an instruction that SUCCEEDS publishes the keys) is
a condition of 261's CLOSE, deferred until the CLI starts, and said so in the
landing section; the commit condition is the two selftests driven both ways.
No bound is set on any of these numbers; they are printers.

**262, new, dictated text for `production/queue/262-the-executor-adds-the-archive-link-while-the-register-allows-zero.md`:**

    # 262: the executor adds the archive link while the register allows zero

    STATUS: READY
    OPENED: 2026-09-11. Ruled by game-design/decision-2026-09-11-ruling-the-
    link-floor-marker-batch-and-the-answer-already-sent.md, section 2 (e).

    ## What is wrong

    tools/runner/executor.py hardcodes SITE_LINK (line 198) to the archive
    and adds it in five places: compose_answer (371 to 394) appends "The
    board: <archive>" to every session answer carrying no site link, and the
    four fallback wordings (400 to 436) carry it unconditionally. Queue 259
    taught the register that zero links is legal while no page is served;
    it did not teach the executor to stop adding one, and linkdest still
    admits the archive, so every executor reply to Jafar carries the link
    the 2026-09-10 ruling exists to keep off his phone. Measured: his
    "Is this working?" of 2026-09-11 was answered at 13:18:43Z by
    fallback_no_cli() with that link.

    ## Done looks like

    1. The executor reads the same marker through producer-check's own
       link_floor_state (loaded by path the way outbox.py's selftest already
       does), never a copy of the logic. While the floor is suspended,
       compose_answer adds nothing and the fallbacks carry no link; while it
       is live, today's behaviour, unchanged.
    2. The selftest is a ladder: the same wordings run through the REAL
       register on both rungs with the marker planted each way, and the
       assertion at line 1844 becomes conditional on the rung.
    3. The link line is one function with one call site per wording, so a
       sixth wording cannot exist to forget it.

    ## Ordering

    After 261, before 256. 256 changes the destination; this stops the
    addition during the window.

**A question for the queue, not ruled here:** the executor is a second,
judgement-free voice in the channel Jafar said should carry one judgement
step (2026-09-09), and it answers questions as if they were instructions.
Options: (A) the executor replies only to instructions it actually started,
and no-cli and failed outcomes reach the studio's inbox reading instead of
his phone; (B) as today. Recommendation A, default B until ruled, because A
trades a wrong answer for silence when the machine is broken and that
trade is his to make.

## 6. The Producer's revision, and what the resident checks before it sends

The Producer rewrites `production/outbox/2026-09-11-yes-it-works.answer.md`
in place. It must carry, in its own words: the yes; ONE plain sentence saying
that the short note he received a couple of minutes after asking came from
the machine's own automatic reply and means the part of his PC that would
run the work could not start its tool, while the message channel he asked
about worked in both directions; and one honest sentence on that fault: the
reason is not readable from here until the next machine run reports it, it
is being fixed, and the next visible thing or the word unknown. It may not
use the banned self-correction tokens, and it needs no link. The sentence
about the start-at-logon entry is re-read against the newest
`production/pc-ops/scheduled-task-verify.txt` and NOW.md's 08:40Z entry
before it stands; I cannot measure the task's state from here and neither
can the Producer from memory. The resident then prints `--kind answer` on it
(section 9 condition 5) and `wc -c` (condition 6).

## 7. Dictated block for `production/NOW.md`, resident to paste at the top

    ## 2026-09-11 14:10Z: THE FLOOR IS CONDITIONAL, THE ORDER AGAINST 260 IS
    ## NARROWED, AND HE ALREADY HAD AN ANSWER

    Queue 259's code lands: the link floor reads production/site-served.txt
    and is off while it says none, and every run prints which branch it
    took. The two held messages stay in outbox-blocked until 260 lands;
    that is the part of the 08:40Z ordering that still binds. Jafar's "Is
    this working?" was answered at 13:18:43Z by the executor's no-cli
    fallback, with the archive link, so the Producer's reply is revised to
    say what that note meant before it sends. Next builder dispatches, in
    order: 261 (the executor's cli keys and its journal tail reach
    production/pc-ops/), 262 (the executor stops adding the archive link
    while the register allows zero), 260, 256. Ruling:
    game-design/decision-2026-09-11-ruling-the-link-floor-marker-batch-and-the-answer-already-sent.md.

## 8. Quality ladder at close

First working result for the register; best available once A1 is in. Rungs
above it, named: 256's provenance check (section 5); a blast-radius half for
the gate, `filesLinklessPassed=N/checked`, counting the checked files that
carry no site link and passed only because the floor was off, beside
`filesLinkFloorOff`, which today counts every file whether or not the
suspension changed its verdict; and 262. The blank rung is the executor's
standing as a voice at all (section 5's question), which is a decision for
Jafar and not a build.

## 9. Conditions the resident prints before the commit, and after the push

1. `python3 ledger/verify.py` green; the cadence line reads this stamp FRESH
   (`rulingFresh=1`), and the footer is pasted from `ledger/.verify-footer`.
2. `git diff --stat -- tools/producer-check.py` (unstaged) is EMPTY, so the
   tested file and the staged file are one file; then
   `python3 tools/producer-check.py --selftest` pasted whole from that run,
   and the done line's marker-fixture count equals `len(floor_cases) + 3` in
   the staged file (7 as read; if it prints 5, say which file was tested).
3. `python3 tools/producer-check.py --gate` pasted: PASS,
   `filesLinkFloorOff=N/N`, `linkFloorActive=false`,
   `reason=no-page-served-yet..production/site-served.txt..servedCommit/none`,
   and after A1 `markerOriginConsistent=true`.
4. A1's rejecting rung in the selftest output, named, and its accepting rung
   first.
5. `python3 tools/producer-check.py --kind answer production/outbox/2026-09-11-yes-it-works.answer.md`
   on the REVISED file: SEND, `rulesEnforced=3/10`, `linkFloorActive=false`.
6. `wc -c` on the revised answer, under 4096, and the count written here.
7. `python3 tools/runner/outbox.py --selftest` and
   `python3 tools/runner/executor.py --selftest` still green, their done
   lines pasted: both copy `producer-check.py` into fixture trees with no
   marker, so their fixtures now run with the floor LIVE for the reason
   `marker-absent`, which is the same verdict as before and must be seen,
   not assumed.
8. After the push: `pc-inbox` gains
   `production/outbound/2026-09-11-yes-it-works.answer.receipt.txt`. That
   receipt is the proof of 259's item 2. If a `refused-` record appears
   instead naming `linkfloor`, the PC's checkout or its copy of the tool is
   behind this commit, and the instrument is the first suspect.
9. `python3 tools/docs-check.py`: this record LOG, dated, em-dash count 0;
   queue 262 declares a status.
10. Queue 261 dispatched to a builder from section 5's words before this
    session ends, or the resume armed for it (rule 13).

## 10. Landing

Filled by the resident, 2026-09-11, one line per condition, every number
printed rather than remembered. Landed as `ce564254`.

1. VERIFY GREEN. `checks=81ran/0skipped/81total`, `director cadence ok (566
   changed line(s) ... over threshold, REVIEWED)`, `rulingRecords=1/81
   rulingFiles=77`, "1 ruling record(s) paired to a director row newer than the
   reference", reference `1aedef87@2026-09-11T07:02:42Z`. No `NOT GREEN` in the
   output (0 hits), and the footer was pasted FROM `ledger/.verify-footer`,
   which was deleted before the run so it could only come from this one.
   NOTE ON YOUR CONDITION 1: `rulingFresh=` is not a key this codebase emits, so
   nothing could print it. The pairing sentence above is the equivalent fact.
2. `git diff -- tools/producer-check.py` unstaged: 0 lines, so the tested file
   and the staged file are one file. Selftest done line from that same file:
   `PASS. 126 passed, 0 failed, 15 rejecting fixture(s) over 10 rule(s) ...,
   9 rejecting gate fixture(s) in 30 measured gate run(s), 7 marker fixture(s)
   and 3 link-floor ladder rung(s) at the gate`. SEVEN, as you read it, not the
   5 I pasted from a stale run.
3. `--gate: PASS filesChecked=23 ... markerOriginConsistent=true
   filesLinkFloorOff=23/23 linkFloorActive=false
   reason=no-page-served-yet..production/site-served.txt..servedCommit/none`
   exit 0.
4. A1's three rungs, ACCEPTING FIRST, pasted from the staged file:
   rung 1 ACCEPTING, the LIVE tree, `markerOriginConsistent=true exit=0, 0 file
   finding(s) over 23 checked, reason=none`; rung 2 REJECTING, SYNTHETIC
   `servedCommit=0bc1def2` against the archive, `markerOriginConsistent=false
   exit=1, 0 file finding(s) over 1 checked,
   reason=marker-names-served-commit-but-SITE_ORIGIN-is-the-archive..production/site-served.txt`;
   rung 3 ACCEPTING, the same tree against the origin 256 will produce,
   `markerOriginConsistent=true exit=0`.
5. The REVISED answer: `SEND register=answer rulesEnforced=3/10
   rulesNotEnforced=wordcap/shape/options/deadline/nextvisible/linkfloor/split
   markerOriginConsistent=true linkFloorActive=false` exit 0.
6. `wc -c` on the revised answer: 1661, against the 4096 cap. The receipt in
   condition 8 records 1660 sent, the difference being the trailing newline.
7. `outbox.py --selftest exit=0 casesRun=115 casesFailed=0`. `executor.py
   --selftest: 123 passed, 0 failed (of 123 case(s))`. Both fixtures run with
   the floor LIVE for `marker-absent`, seen rather than assumed.
8. THE RECEIPT LANDED, NOT A REFUSAL, 150 seconds after the push:
   `production/outbound/2026-09-11-yes-it-works.answer.receipt.txt` on
   `pc-inbox`, reading `receipt: sent  kind: answer  messageId: 77
   chars: 1660  fileCommit: ce5642541a598977a5435022f3b603fb6b9cf650
   sent: 2026-09-11T14:22:27+00:00  outboundLatencySec: 125`. The receipt NAMES
   THIS COMMIT, which is what makes it evidence of this batch rather than of
   some earlier one. That is 259's item 2 proven end to end: the sender read
   the marker in its own checkout and did not refuse on `linkfloor`.
   ONE SAMPLE of one message, not a rate.
9. `docs-check: 178/178 clean under game-design/`. This record: STATUS LOG,
   dated, em-dash count 0. Queue 262 declares `STATUS: READY`.
10. Queue 261 NOT dispatched in this session. The resume is armed instead
    (rule 13): the hourly inbox and resume trigger `trig_017Ho772fH6Uuysbith7b3CU`
    fires at `3 * * * *`, last run SUCCEEDED at 2026-09-11T13:18:06Z, and
    `production/NOW.md` names 261 as the next dispatch in order. The reason is
    Jafar's own instruction to report and then stop, and a budget of 78 total
    and 82 Fable against the standing 85.

A1 WAS KEPT AT 83 LINES AGAINST YOUR SIXTY-LINE ESTIMATE. Ruled KEEP on the
per-block measurement, which showed the overrun sitting in the specification
rather than in padding: the selftest rungs are 28 lines, the pure function 16,
the four done lines 10, the gate finding line 9, and no clause could be dropped
that reached sixty. Trimming every comment recovers about 9 and lands at 74.

## History

2026-09-11, same director spawn, before commit. Section 3's size bound
("about sixty changed lines") was a rule-7 estimate of what the guard should
cost, set with no series and paired with a lateness condition that did not
occur: the builder round and the Producer's revision came back together.
Measured by the resident against a copy taken before the first A1 edit: 83
added lines (4 blank), 5 modified or removed, em-dashes 0, and per block
the selftest rungs 28, the function 16, the finding line 9, the four done
lines 10, the constant 5, gate keys 4, check() key 4, gate call 3, header 2,
signature 1, pass condition 1, every block mapping to a clause of section 3
and no trim reaching sixty. All three rungs pass, accepting first: the live
tree `markerOriginConsistent=true` over 23 checked; the synthetic sha against
`ARCHIVE_ORIGIN` `markerOriginConsistent=false exit=1` with the named reason;
the same tree against the origin 256 will produce, true. Selftest 126 passed
0 failed with 7 marker fixtures; gate PASS `filesLinkFloorOff=23/23`;
outbox selftest 115 passed 0 failed. Ruled KEEP: the bound was not a gate
threshold, and dropping a proven guard to honour an estimate would leave the
(c) hole on prose alone. One deviation from section 3's literal text is kept
on purpose: the finding line is indented four spaces and carries `: `,
because `ledger/verify.py:producer_register()` (1719 to 1722) harvests a
finding into the footer by exactly that shape, and at two spaces the footer
would read `see producer-check` instead of naming the fault. The working
tree also carried 33 unstaged lines of the `SERVED_VALUE_WIDTH` cap work,
which is part of the file reviewed in section 1 (432 to 438, 2574 to 2591):
the whole file is staged, and section 9 condition 2 stands as written. The
5-marker-fixture count in section 1 was a stale paste, read before the
builder's last edit; the live line prints 7.
