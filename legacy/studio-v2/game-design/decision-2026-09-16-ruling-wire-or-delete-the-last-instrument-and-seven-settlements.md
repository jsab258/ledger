<!--RULING spawn=2026-09-16T11:36:51Z paths=ledger/verify.py,tools/ci-checks.sh,tools/canon-gate.py,tools/goal-block-check.py,tools/enforcement-claims-check.py,tools/canon-register-check.py,CLAUDE.md,canon.md,ledger-v2/studio-v2/constitution.md,ledger-v2/studio-v2/operations.md,ledger-v2/studio-v2/organization.md,.claude/rules/ci.md,legacy/claude-md-superseded-2026-09-01.md,.claude/agents/dialogue-writer.md,production/queue/354-thirteen-enforcement-claims-in-claude-md-and-how-many-are-true.md,production/queue/352-the-commit-gate-read-156-gated-lines-that-no-path-accounts-for.md,production/queue/353-the-turns-log-is-288-rows-nobody-reads-and-the-ceiling-does-not-match-it.md,production/queue/333-the-sodium-lantern-has-no-lit-element-only-a-point-light.md,game-design/decision-2026-09-16-ruling-wire-or-delete-the-last-instrument-and-seven-settlements.md-->
# Ruling, 2026-09-16: wire or delete, the last instrument of the month, and seven settlements

STATUS: LOG, 2026-09-16. NOT CURRENT once the wiring lands and the
enforcement-claims check ships; from then `ledger/verify.py`,
`tools/ci-checks.sh`, CLAUDE.md, canon.md and the constitution are the
reading copies and this file is their history.

Director ruling, spawn row `2026-09-16T11:36:51Z studio-director fable`
in `.claude/agent-log.tsv` line 688. Executes Jafar's policy of 2026-09-16 on
enforcement claims; does not revisit it. Evidence read this session is cited
by file and line beside every call. Where a number was not printed this
session the record says "nothing measured" rather than guessing.

Jafar's policy, verbatim, which this record executes: "Wire or delete, no
third option, and no claim survives unwired. The canon gate is wired, because
canon's own line says a violation is a gate failure and that sentence is
currently false. goal-block-check is wired. Anything else found unwired is
either wired in the same batch or deleted with its claim, and a sentence that
survives in a narrower scope than it states gets rewritten to the scope that
is true." And: "a document may not claim something is enforced unless a gate
runs it. A check that proves that, over CLAUDE.md, canon and the
constitution, is the last instrument this month and something retires for it
under D45."

---

## PART ONE. Executing the policy

### 1.1 The wiring order

Both tools go into BOTH runners, as two rows each, in this shape:

`ledger/verify.py`: two new check functions in the check tuple, `canon_gate`
and `goal_block`, built the way `canon-register` is already wrapped at
verify.py:2030-2033: run the tool, parse its done line, and turn a
denominator of zero into red. A run of canon-gate that examined 0 files is
NOTHING MEASURED and must not read as clean (rule 3b).

`tools/ci-checks.sh`: four rows in `real_table()` at ci-checks.sh:78-90, in
the existing tab-separated shape: `canon-gate`, `canon-gate-selftest`,
`goal-block`, `goal-block-selftest`. Names carry no spaces.

THE CORPUS IS DECLARED IN THE TOOL, NOT IN THE RUNNERS. `canon-gate.py`
takes a file list (canon-gate.py:4 and :264-267) and has no walk of its own.
The builder adds one mode, `--corpus`, that walks the roots below, prints the
roots and the file and line counts, and exits through the same `gate()`.
verify.py and ci-checks.sh both call `--corpus`, so there is one definition of
what canon governs mechanically and two runners cannot drift apart (one idea,
one implementation).

The roots, ruled here: `content/`, `ledger/Assets/Scripts/`, and
`production/specs/` (its `judge-` fixtures stay exempt by the existing prefix
at canon-gate.py:74). That is where world content lives. NOT in the corpus:
CLAUDE.md, `.claude/rules/`, `game-design/`, `production/queue/`, `tools/`.
Those are the law and its discussion, which is the tool's own stated
principle at canon-gate.py:55-57, and the code says why this is not a
preference: the era-term list at canon-gate.py:39-53 contains the word for the
network that does not exist in 1988, CLAUDE.md section 0 uses that word in
its own ban, and `tools/imagegen/prompts.json` IS the brand list. A corpus
containing the law arrives red on the law. That reading is from the code, not
from a run; the run comes first below.

### 1.2 Does canon-gate arrive green? Nothing measured yet, and it lands green or not at all

The gate has never run over this corpus. Nobody has printed the series, so
this record does not predict a colour. The order is fixed instead:

1. The builder runs `python3 tools/canon-gate.py --corpus` BEFORE wiring it
   and pastes the printed done line and every `CANON:` line into the
   hand-back. That is the series (rule 2).
2. If it is clean, wire it. If it is red, every finding is one of three
   classes, and the class decides the fix, never the gate's bound:
   (a) A REAL VIOLATION IN CONTENT: an era artefact or a real brand in a line
   the player could meet. Canon outranks the content; the content changes in
   the same batch. This is the case the gate exists for and the 06:35Z ruling
   is honoured by fixing it, not by shipping red.
   (b) LEGITIMATE DISCUSSION OF THE BAN INSIDE THE CORPUS (a spec that says
   what may not appear; an attribution or licence file whose job is to name a
   real licensor). Reword the prose where it is prose (the 26 Aug precedent at
   canon-gate.py:21-24: reword, never loosen). Where the file's job is to name
   real entities, exempt it BY NAME in `EXEMPT`, and the exemption prints
   whenever it bites, as the existing ones do at canon-gate.py:163-164.
   (c) A FALSE POSITIVE OF THE WORD LIST (a term inside an identifier, a
   path, a URL). The boundary is tightened only with a planted rejecting case
   beside it (rule 5b), and no term leaves the list.
3. The gate lands in the same commit as the fixes for (a), (b) and (c), green.
   A GATE NEVER LANDS RED. If the printed list exceeds what one builder can
   triage inside its budget, the builder hands back the printed list as a
   named partial and the director rules per class from the list. A red gate
   left in the tree to "burn down later" is the failure the 06:35Z ruling
   named, and it is refused here in advance.

goal-block-check follows the same order: run first, paste the line. Its
direction is fixed by its own docstring (goal-block-check.py:15-16, "the
source wins"), so a red arrival is fixed by re-copying the block from
`ledger-v2/respec/vision-pillars-v2.md` into CLAUDE.md, never the reverse. If
the tool has no `--selftest`, it ships one in this batch, accepting case first
on the live tree, rejecting case a temporary copy of CLAUDE.md with one word
changed (instruments.md, "Selftest ships with the tool").

### 1.3 The three narrowed sentences, dictated verbatim

The resident applies these as dictated text and nothing else. Each replaces
the whole sentence or paragraph named. CLAUDE.md line numbers are those of
the copy read this session.

SAME-DAY NOTE: applying (i) to (iv) as written below put CLAUDE.md at 2154
words against its 2000 bound. Addendum 1.3b at the end of this record rules
what moves out, and it SUPERSEDES the CLAUDE.md wording of (i), (ii), (iii)
and (iv) with shorter forms; the full texts of (i) and (ii) survive verbatim
as constitution laws 6 and 11. Read 1.3b before applying anything here.

(i) THE LICENCE ALLOWLIST, CLAUDE.md lines 40-42. Replace the sentence
beginning "THE LICENCE ALLOWLIST IS LAW" with:

"THE LICENCE ALLOWLIST IS LAW (`ledger-v2/research/license-allowlist.md`):
nothing ships that is not on it, and `tools/attribution-check.py` walks the
tree for that half, run by `ledger/verify.py` and `tools/ci-checks.sh`. The
other half, that a new tool enters only through a decision record naming its
weights licence, is a standing order that NO TOOL CHECKS: the director reads
for it at every landing that adds an external tool."

(ii) THE FORMATTING LAW, CLAUDE.md lines 43-45. Jafar named this the test
case and gave two options: scan the documents, or rewrite the sentence to say
game text. RULED: REWRITE. Three reasons, in order of weight. First, the
document scanner is not free: "written from 31 August on" is a per-line
authorship date, which means blame, which is a real instrument with a real
weak link, and Jafar has just capped this month at one more instrument and
that one is spoken for. Second, D45: an em-dash in a document is found the
next time somebody reads it and costs nothing hidden; a document scanner buys
rigour where no fault hides. Third, the constitution's law 11 ("anywhere")
stands as a law; what changes is only the sentence that implied a tool
applies it. Replace the paragraph with:

"THE FORMATTING LAW: no em-dashes and no italic text in anything written from
31 August on; older text is corrected opportunistically, never rewritten
wholesale. The only tool that applies it is `tools/slopcheck.py`, over game
text under `ledger/Assets/Scripts` and as a ratchet at its printed
SLOP_CEILING, not at zero. In documents it is a reading rule that no tool
checks: whoever reads a document applies it, and a violation found is fixed
where it is found."

The next rung is named and queued, not taken: if Jafar wants documents
scanned after this month, the cheapest shape is a blame-free scan of the
three governance files only, added inside the enforcement-claims check rather
than as a tool of its own. Queue it under a name; it is not in this batch.

(iii) RULE 9, CLAUDE.md, the paragraph beginning "**9. Do not block
yourself.**". The audit spot-verified 10 of 19 workflows carrying a named
group and did not check the opt-in half. The sentence is a rule of conduct
that reads as a description of a mechanism; the rewrite makes it a rule of
conduct in its own words:

"**9. Do not block yourself.** Know what your pushes trigger. Expensive jobs
are opt-in (`workflow_dispatch`), concurrency groups scope to them, cheap
checks never queue behind a stream. No tool checks this: every workflow change
is read against it by hand, and the reader says how many workflows carry a
group out of how many exist."

Two further sentences change because the two wired gates now have a scope,
and a sentence that survives in a narrower scope than it states is rewritten
(the policy's last clause):

(iv) CLAUDE.md lines 33-34, item 1 under "What outranks this file". Replace
with: "1. `canon.md`. World facts, approved by Jafar. It outranks every
document and every agent. Violating it in content is a gate failure, not a
style note: `tools/canon-gate.py --corpus` refuses era and brand violations
over `content/`, `ledger/Assets/Scripts` and `production/specs`, run by
`ledger/verify.py` and `tools/ci-checks.sh`. In a document a violation is
corrected on sight, by hand. Tone is not mechanical and is the judge's under
D7."

(v) canon.md line 5. Replace "This outranks every document and
agent; violating it is a gate failure." with: "This outranks every document
and agent; violating it in content is a gate failure (`tools/canon-gate.py
--corpus`, era and brands, over content/, ledger/Assets/Scripts and
production/specs, run by verify.py and ci-checks.sh). Tone is the judge's
under D7, not a gate."

### 1.4 The two false claims: the builder's brief

Role: instrument-builder (declared `maxTurns: 70`; observed median 78.5,
peak 194 per queue 353, so the brief is sized to hand back partial).
Model: the role file's own. Under D45 this is tool work: a test, no review;
the director at landing is this record. The builder never commits.

The brief, in order, with a countable two-armed exit: "Hand back at 55 tool
calls or when all six steps are done, whichever comes first, with the printed
lines from steps 1 and 2 pasted whether or not the rest landed."

1. Add `--corpus` to `tools/canon-gate.py` (roots as ruled in 1.1; print the
   roots, the file count and the line count on the done line). Run it. Paste
   the done line and every `CANON:` line. Do not fix anything yet.
2. Run `python3 tools/goal-block-check.py`. Paste its line.
3. Triage step 1's findings by the three classes in 1.2 and fix (a), (b), (c)
   as ruled. If more than thirty findings, stop, hand back the list.
4. Wire both tools: verify.py check tuple (`canon_gate`, `goal_block`, each
   red on a zero denominator) and ci-checks.sh rows (`canon-gate`,
   `canon-gate-selftest`, `goal-block`, `goal-block-selftest`). Ship a
   goal-block selftest if none exists, accepting case first.
5. Rule 6: grep for every reference to both tool names across `.py`, `.sh`,
   `.yml`, `.md` and paste the count, so "wired" has its call sites beside it.
6. Run `python3 ledger/verify.py` and `tools/ci-checks.sh --list`; paste the
   footer line and the table count. The table count must have risen by four.

### 1.5 Is an ASKED a claim? No, and the zero had the wrong denominator

`production/quality-ladder.md` calls itself "an INSTRUMENT OF that plan" that
"holds one question, asked at close" (quality-ladder.md:7-9). The audit found
zero readers in `.py`, `.sh` and `.yml` (queue 354:63-66). Two rulings:

First, an "asked" is not an enforcement claim. The policy governs sentences
that assert a MECHANISM. "Asked at close" asserts a practice by a named actor
at a named moment. It survives as written.

Second, the zero is a zero with the wrong denominator (rule 3b). The file's
readers are not scripts: quality-ladder.md:11-14 names two document readers
itself (CLAUDE.md line 205 and `.claude/agents/world-designer.md` line 90),
and the studio-director role definition carries the question verbatim as item
4 of what the director owns ("is this the best available result, or the first
working one? Name the next rung or take it"). A close-out is a director spawn
by CLAUDE.md's escalation list, so the question is wired to the actor who
performs the close, through the file every such spawn reads. The audit
grepped scripts for a reader that lives in a role file. Recorded so the same
zero is not re-filed next week.

---

## PART TWO. The standing rule, and what retires for it

### 2.1 Wording, and where it lives

THE RULE LIVES IN THE CONSTITUTION, because the constitution binds
(CLAUDE.md, "What outranks this file", item 2) and its law 1 is already the
parent of this rule. Dictated, appended as the next numbered law after the
last one present (12 at constitution.md:14 when read this session; the
resident applies the next free number and reports it):

"13. No enforcement claim without a runner (Jafar, 2026-09-16). A document may
not say that something is enforced, gated, checked, blocked, refused or proven
unless the sentence names the tool that does it and something runs that tool.
A sentence true in a narrower scope than it states is rewritten to the scope
that is true. `tools/enforcement-claims-check.py` proves this over CLAUDE.md,
canon.md and this file, prints which sentences it matched and which it could
not, and is THE LAST INSTRUMENT OF SEPTEMBER 2026: another checker lands this
month only when one retires under D45, and the retirement is named in the same
record."

CLAUDE.md gets ONE sentence, no more, because verify.py prints its word
count. The wording is edit K of addendum 1.3b, which supersedes the longer
form first dictated here, and it lands WITH the check, not before it, because
it names a tool that has no runner until the check lands.

canon.md carries no copy of the rule. Canon holds world facts; its only
enforcement sentence is line 5, rewritten in 1.3(v).

### 2.2 The shape of the check

`tools/enforcement-claims-check.py`, one file, selftest included, accepting
case first with the live tree as the accepting fixture and a synthetic
rejecting fixture (a sentence claiming `tools/no-such-tool.py` enforces
something; a sentence with an enforcement verb and no path).

Inputs: CLAUDE.md, canon.md, `ledger-v2/studio-v2/constitution.md`. Nothing
else this month.

What it does, per sentence:
1. Sentence split, then a PHRASE LIST of enforcement verbs. The list is set
   from a printed series, not chosen: the builder ships `--series` first,
   which prints every sentence in the three files containing any candidate
   verb (enforce, gate, check, block, refuse, prove, wired, runs, deletes,
   writes, withholds), reads it, then sets the list. The phrase list is the
   weak link, exactly as it is for canon-register-check, so it is printed at
   every run.
2. A matched sentence must name a runnable path in backticks (`tools/x.py`,
   `ledger/verify.py`, a hook or workflow path). The path must exist.
3. The path must have a RUNNER: it appears in verify.py's check tuple, in
   `tools/ci-checks.sh`'s `real_table()`, in a workflow under
   `.github/workflows/`, or in the hooks configuration under `.claude/`. The
   set of runners is printed on the head line so a fifth runner added later
   is visible as absent. THE SENTENCE NEVER RECITES ITS RUNNER: proving that
   something runs the named tool is this step's job, and a sentence that
   names the tool has said everything the policy asks of it.
4. NEGATIVE CLAIMS. A sentence that says NO tool checks something ("no tool
   checks this", "no tool applies it to documents") is printed as
   `runner=none-by-design` and is never red. The policy forbids false claims
   of enforcement, not honest statements of its absence; the audit's three
   narrowed sentences are exactly this shape and must pass.
5. UNMATCHED: every sentence containing a candidate verb that the phrase list
   did not classify as a claim, printed with file and line, counted, advisory.
   The same discipline as canon-register-check.py:40-49: a miss must not look
   like a pass.

Output: one line per matched claim, `file:line matched=<slug> tool=<path>
runner=<which|none|none-by-design>`; the UNMATCHED block, capped at 12 with
the cap announcing itself; a done line with denominators: sentences examined,
claims matched, claims wired, claims unwired, negative claims, unmatched.
Exit 0 all wired; 1 any matched claim names no tool or a tool with no runner;
2 nothing measured; 3 selftest broken. No spaces inside values.

Landing order: Part One's rewrites land first or in the same commit, so the
check arrives green on the tree it was built against. The builder pastes its
done line on the live tree and the count of matched claims, which must be
at least the six the audit found cleanly true plus the two wired here.

### 2.3 What retires: `template_sync` in verify.py, on code evidence

The candidate class Jafar named is a gate that has never fired. This record
distinguishes "never fired" from "never had cause to fire", and then reports
what it could and could not establish.

WHAT WAS NOT MEASURED. verify.py keeps no per-check firing history that this
session found, and no run of verify.py was made from this spawn (no shell).
So for the 85 live checks, firing history is NOTHING MEASURED, and this
record does not name any live check as "never fired". A session that wants a
live candidate ships the printer first: a per-check tally of red outcomes
over the last N runs, then reads it (rule 2, "a new bound needs a printed
series").

WHAT WAS ESTABLISHED, FROM THE CODE. `template_sync()` at verify.py:2036-2058
occupies one of the 86 slots and CANNOT fire: it has no branch that returns
False, examines nothing, and returns `True` with the string "template sync
RETIRED by D10" on every run (verify.py:2057-2058). Its docstring says it was
retired 2026-08-31 by D10. So for this slot both facts are settled at once:
it has not fired since 31 August because it has no cause and no means. It is
an instrument that measures nothing and prints a sentence nobody acts on,
which is the exact class D45 says to stop spending on.

RULED: `template_sync` leaves the check tuple, and its evidence row for
`.claude/template-sync.txt` at verify.py:3804 leaves with it. The
verify.py test fixture that names `.claude/template-sync.txt` (verify.py:7063)
is the call site rule 6 requires the builder to grep for and adjust.
`tools/template-sync.py` itself STAYS ON DISK, because D10 says in Jafar's
words that it stays as machinery a harvest may reuse, and this record does
not revisit a Jafar decision; it makes no enforcement claim, so it is outside
the new law. The count of checks after this batch is therefore 86 minus one
plus one: unchanged. That is the point.

Acknowledged plainly: this is the cheapest retirement, and it is real rather
than clever only because the slot has been printing a sentence into every
verify run for sixteen days. If Jafar wants a LIVE instrument to go, the
firing-history printer above is the measurement that picks it, and it is a
research task under the quality ladder, not a guess made here.

A second retirement is named as the next rung, not taken: the phrase-list
half of canon-register-check retires once every record in the register
carries a `CANON:` directive; the tool's own docstring says the directive
path "is what this tool exists to retire" (canon-register-check.py:36-39).
Queue a scribe task: add `CANON: none` or `CANON: edits <lines>` to every
pre-2026-09-16 record, the resident reading each. When UNMATCHED reads 0 of
0, the phrase list and its UNMATCHED block are deleted, and the register is
gated on the directive alone.

---

## PART THREE. Seven settlements

### 3.1 canon-register-check's A1 unit: CONFIRMED, with two conditions

The builder made A1's unit the ITEM rather than the citation, because section
9.2 of the 2026-09-16 record dictated item 1 under `## OPEN` as "Engine:
DECIDED, Unreal (D16 ...)", kept numbered so "OPEN 2" keeps its meaning
(record lines 385-390; canon-register-check.py:108-111). Per-citation A1
would have arrived red on the very line the same ruling dictated: a gate red
on its own spec's text is the 06:35Z failure, and both modes print and are
counted. Confirmed.

Conditions: (a) section 8 of that record is amended in this batch to say the
unit is the item, so the spec and the tool do not disagree (a sentence
surviving in a narrower scope than it states gets rewritten). (b) The
`DECLARED_CLOSED_RE` escape at canon-register-check.py:111 is a hole unless
tested: the selftest must plant an OPEN item that cites a DECIDED record and
does NOT say "it is not open", and assert red (rule 5b). If that planted case
is already there, the builder says so with its line number; if not, it lands
with the batch.

### 3.2 UNMATCHED does not redden

11 of 15 canon-mentioning records are unmatched today. A gate that reddens on
73 percent of its population on arrival is the gate everybody learns to
ignore. UNMATCHED stays advisory, printed and counted at every run, as the
tool's docstring rules at lines 45-49. The real gate is the directive path,
which already reddens for any record dated on or after 2026-09-16 without a
`CANON:` line. No ratchet on the UNMATCHED count is set: the tool's docstring
says 16 mention and 4 match, the brief says 15 and 11, and two counts that
do not agree are not a series a bound may be read off (rule 2). The number
goes to zero by the scribe task in 2.3, not by a threshold.

### 3.3 Queue 333, the lamp instrument's two headers: the split is confirmed

The constraint was "one tested header"; the principle behind it is
instruments.md, "measurement arithmetic and formatting live where the tests
run". `LedgerVignette::Camera` and `Piece` live in `VignetteSpec.h` and
`SurfaceBind.h` and cannot be reached from `FrameStats.h`, which carries no
spec type on purpose (queue 333:197-202). Two headers that verify.py already
runs tests over satisfy the principle; one header was the means. RULED:
projection in `SurfaceBind.h`, pixel maths and the formatter in
`FrameStats.h`, whose test already builds synthetic BGRA frames. `Probe.cpp`
supplies membership, order and live state only. Both halves get a planted
rejecting case in the tests verify.py runs.

### 3.4 Queue 333, condition 3 against P4: P4 wins, condition 3 is rewritten

Condition 3 says the segment prints per lantern per PROBED shot; P4 predicts
"no" at the day rows of the same cameras; a day row is never a probed shot
(`ShouldProbeShot` returns true only with lanterns or practicals on, queue
333:206-208). A refutable prediction that cannot be reached is not a
prediction, and P4 carries the item's acceptance sentence: yes at night, no at
day, in ONE run. RULED: the segment prints on every shot line that has a
decoded frame, per lantern, yes or no, with its denominator (lanterns
examined) on the line, and `(+N not shown)` if the per-line count is capped.
Condition 3 is rewritten in the item to say exactly that, in the same batch.

### 3.5 Queue 353, the maxTurns unit: run the thing, then set ceilings at peak

Four facts cannot all be about one quantity (queue 353:41-55): the docstring
says turns is what maxTurns bounds; 45 has been declared for engine-specialist
since 2026-08-25; 65 of its runs exceed 45 in the log's unit; one died at 45
this morning logging 47. RULED, in order:

1. The dispatch path is read before anything is argued: grep
   `tools/runner/executor.py` and `tools/runner/brief.py` for `maxTurns` and
   say whether the dispatcher passes a value, passes nothing, or the harness
   reads the frontmatter itself. HYPOTHESIS, labelled as one: the 65 runs and
   the one death came through different dispatch paths, and only one of them
   reads the definition. The grep decides; the record does not.
2. One planted run, the cheapest decisive measurement: a scratch agent
   definition with `maxTurns: 3` and a brief demanding eight tool calls.
   Observe where it dies and what `.claude/agent-turns.tsv` records for that
   agent id. Together with this morning's pair (declared 45, logged 47) that
   is n=2 on the calibration between the harness's unit and the log's.
3. Only then do ceilings move. A ceiling is a "did it ever" bound, so it is
   set at the role's observed PEAK in the established unit, not its median;
   the countable exit in every brief (waste lesson 9) sits at the median,
   which is where a healthy run hands back. Rule 2 applies to the unit as
   much as to the number: a ceiling raised in the wrong unit is a threshold
   set without a series.
4. Until step 2 has run, no ceiling moves. The four roles at n=0
   (guard-tester, integrator, measurement-auditor, reach-auditor) print
   "nothing measured" in their own files where the observed-spend line sits.
5. The acceptance line in 353 stands as written: "established by running
   something rather than by reading a comment".

### 3.6 dialogue-writer's mechanical checks: the sentence goes, Bash does not come

`.claude/agents/dialogue-writer.md:24` orders "You DO run the mechanical
checks the spec names before handing off" and line 4 grants Read, Glob, Grep,
Write and no shell. That is an enforcement claim with no runner, in a role
file. Adding Bash to a tier-3 writer widens a permission, and no agent
message, this record included, authorises a permission change. RULED: the
claim is deleted and the work is routed. Replace line 24 with:

"You have no shell, so you cannot run the mechanical checks the spec names.
Say so in your hand-back, and the resident runs them on the file you wrote
before the judge reads it."

If Jafar wants the writer self-checking, granting Bash is his to do and is
noted here as the alternative, not taken.

### 3.7 Queue 352, the 156 phantom: name it, then test it

Two verify runs minutes apart read 156 gated lines then 0 with no commit
between; the 156 sat under the `ledger` scope while no untracked path was
under `ledger/` (queue 352:15-42). The arithmetic in the item is sound: 859
untracked minus 703 for the intent-added tool is 156, which is the size of
the other untracked file, the wake record under `production/wakes/`. Two
hypotheses, labelled as such, and the two commands that decide them:

1. `_cadence_classify("production/wakes/<that record>")`. If it lands in the
   `ledger` catch-all, the phantom has a name: a path under no listed prefix
   falling into the bucket the table's comment says "keeps the game". `wc -l`
   on that record: if it prints 156 the attribution is proven, not inferred.
2. Whether that record still exists. A wake record is consumed by the wake
   mechanism; if it was consumed between the two runs, that is why 156 left
   the count with no commit, and both readings were "correct" over two
   different working trees, which is the item's second acceptance branch.

The fix, under D45 a test and no review, with this record as the director at
landing because it is the commit gate: whenever the gate is red it prints,
per untracked file, the path and the bucket it landed in (capped, the cap
announcing itself), so the next phantom carries its name; a rejecting test
plants an untracked file under `production/wakes/` and asserts it lands
ungated, and an accepting test plants a real file under `ledger/` and asserts
it still gates (rule 5b, both outcomes watched).

---

## What this record does not touch

Jafar's policy. The negative on world streaming. Queue 351 and the reopened
116. The claim fix, canon corrections and null floor, all landed. D10's
"stays on disk" for `tools/template-sync.py`.

## Ledger of numbers used here, and what each is a statistic of

86 checks in verify.py: the brief's count, not re-counted this session.
10 of 19 workflows with a named group: the audit's spot count. 11 of 15
unmatched: the brief's count; the tool's docstring says 16 and 4, and the
disagreement is recorded rather than resolved. 65 runs over 45, one death
logging 47: queue 353's counts from the turns log. 156, 859, 703, 766, 922:
queue 352's readings, verbatim. 1998 and 2154 words of CLAUDE.md: the
resident's printed counts before and after applying 1.3. Firing history of
live verify checks: nothing measured. Colour of canon-gate over its corpus:
nothing measured.

---

## ADDENDUM 1.3b, same day: what comes out of CLAUDE.md so the policy's words fit

Reported by the resident after applying 1.3 (i) to (iv): CLAUDE.md was 1998
words against its 2000 bound before the edit and 2154 after, and
`claude_md_size()` in `ledger/verify.py` is red with its own words:
"CLAUDE.MD HAS GROWN BACK: 2154 words against the 2000 bound. Move the
passage to a casebook." The remedy is the one the file prescribes for itself;
which passages move is ruled here.

### The bound does not move

Three reasons. Rule 2: a bound is never moved to make red go away, and this
bound is one of the six enforcement claims the audit found cleanly true, so
raising it inside the batch that exists to make enforcement claims true would
be the batch refuting itself. The bound was set at 2000 against a file of
1990 on 2026-09-01: ten words of room, on purpose, so that every addition
displaces its own length. A file at its bound for two weeks is that guard
working as designed, not a straw waiting to fall. And the pressure the policy
adds is real but containable at its source, which the next paragraph does.

### The structural fix, so the next session is not in the same place

Enforcement DETAIL (which tool, which scope, what nothing checks) lives beside
the law in the constitution, which binds and which the enforcement-claims
check reads. CLAUDE.md states the law and names the tool in the fewest words.
A sentence never recites its runner: proving that something runs the named
tool is the check's job (2.2, step 3), and "run by `ledger/verify.py` and
`tools/ci-checks.sh`" in every sentence was ritual, now struck from every
dictated text below. A sentence that says no tool checks something is an
honest negative, never red (2.2, step 4).

### The edits, dictated verbatim, in application order

The resident applies A to J and then pastes the count `ledger/verify.py`
prints. The word counts behind this ordering are hand counts of passages in
this session's copy of CLAUDE.md, so they are estimates and the printed count
decides. Estimated landing: about 1,920 words, which leaves room for edit K.
If the printed count is still over 2000 after J, the reserve at the end is
taken and the count pasted again.

EDIT A. Constitution laws 6 and 11 take the full texts of 1.3(i) and 1.3(ii);
CLAUDE.md keeps a compact form that states both laws and names both tools.

Constitution line 8 (law 6) becomes, one paragraph:
"6. The licence allowlist is law (`ledger-v2/research/license-allowlist.md`):
nothing ships that is not on it, and `tools/attribution-check.py` walks the
tree for that half. The other half, that a new tool enters only through a
decision record naming its weights licence, is a standing order that NO TOOL
CHECKS: the director reads for it at every landing that adds an external
tool. Voice corpora: only those whose contributors donated their voices to
build speech technology, and no identifiable public figures, ever."

Constitution line 13 (law 11) becomes, one paragraph:
"11. Formatting law: no em-dashes and no italic text in anything written from
31 August 2026 on; older text is corrected opportunistically, never rewritten
wholesale. The only tool that applies it is `tools/slopcheck.py`, over game
text under `ledger/Assets/Scripts` and as a ratchet at its printed
SLOP_CEILING, not at zero. In documents it is a reading rule that no tool
checks: whoever reads a document applies it, and a violation found is fixed
where it is found."

CLAUDE.md: the paragraph that now holds (i) and (ii), from "Two are absolute
and repeated here" to the end of the formatting-law text, becomes:
"Two are absolute and repeated here; constitution laws 6 and 11 carry what
checks each and what nothing checks. THE LICENCE ALLOWLIST IS LAW
(`ledger-v2/research/license-allowlist.md`): nothing ships that is not on it,
which `tools/attribution-check.py` walks the tree for, and a new tool enters
only through a decision record naming its weights licence, which no tool
checks. THE FORMATTING LAW: no em-dashes and no italic text in anything
written from 31 August on, older text corrected opportunistically, never
rewritten wholesale; `tools/slopcheck.py` applies it to game text only, and no
tool applies it to documents."

EDIT B. Rule 9, replacing the 1.3(iii) text as applied:
"**9. Do not block yourself.** Know what your pushes trigger. Expensive jobs
are opt-in (`workflow_dispatch`), concurrency groups scope to them, cheap
checks never queue behind a stream. No tool checks this; a workflow change is
read against it by hand."

EDIT C. Item 1 under "What outranks this file", replacing the 1.3(iv) text
as applied:
"1. `canon.md`. World facts, approved by Jafar. It outranks every document
and every agent. Violating it in content is a gate failure, not a style note:
`tools/canon-gate.py --corpus` refuses era and brand violations over
`content/`, `ledger/Assets/Scripts` and `production/specs`. In a document a
violation is corrected on sight, by hand. Tone is the judge's under D7, not a
gate."

EDIT D. The paragraph between the goal heading and "## The goal", which
begins "Copied VERBATIM", becomes:
"Copied VERBATIM from `ledger-v2/respec/vision-pillars-v2.md`, the source;
`tools/goal-block-check.py` proves the copy matches, and the source wins. Do
not edit this copy: edit the source and re-copy."
This is safe for the checker: goal-block-check.py:46-56 compares from "## The
goal" to the "---" rule, and this paragraph sits above that span.

EDIT E. The paragraph under "## The standard" beginning "Reporting to Jafar
is THE PRODUCER'S ALONE" moves intact to `ledger-v2/studio-v2/operations.md`,
beneath the heading at its line 169. That heading carries a 22 Aug em-dash,
corrected while there: it becomes
"### Reporting: RETIRED 22 Aug by Jafar ("drop the updates"), superseded
2026-09-03". Directly under it, first this lead line, then the paragraph
unchanged:
"Moved here intact from CLAUDE.md on 2026-09-16 under the ruling of that
date:"
In CLAUDE.md its place is taken by:
"Reporting to Jafar is the Producer's alone (ruled 2026-09-03):
`.claude/agents/producer.md` carries the register, the cap and the required
link; `ledger-v2/studio-v2/operations.md`, Reporting, carries the rest."

EDIT F. Under "## Before you commit", the sentence beginning "Voice sourcing
consent rule" and the two sentences beginning "HuggingFace and most external
hosts" leave. The voice sentence is carried by law 6 in edit A. The
HuggingFace pair moves intact to `.claude/rules/ci.md` as a new bullet
directly after the "Batch changes per dispatch" bullet:
"- **HuggingFace and most external hosts are blocked here, so corpus work
goes through CI.** Make each run maximally informative, not a blind attempt.
Moved intact from CLAUDE.md, 2026-09-16."
In CLAUDE.md their place is taken by:
"Voice consent is constitution law 6; blocked hosts and corpus runs are
`.claude/rules/ci.md`."

EDIT G. Under "## The studio split", the sentences from "The resident
hand-applies only dictated text" to "a resident never stamps the ruling."
move intact to `ledger-v2/studio-v2/organization.md`, at the end of the
section that carries the split (CLAUDE.md's own index says that file holds
it); if no such heading exists, at the end of the file under the heading
"Escalation mechanics, moved from CLAUDE.md 2026-09-16". Lead line, then the
sentences unchanged:
"Moved here intact from CLAUDE.md on 2026-09-16; the mechanism is
`director_cadence` in `ledger/verify.py`:"
In CLAUDE.md their place is taken by:
"The resident hand-applies only dictated text or a one-line fix.
`director_cadence` in `ledger/verify.py` blocks a commit of builder work no
ruling covers; the ruling's shape is in `ledger-v2/studio-v2/organization.md`."

EDIT H. The section "## Where the rest of this file went, 2026-09-01" moves
intact to the head of `legacy/claude-md-superseded-2026-09-01.md`, under the
heading "Index of the 2026-09-01 move, moved here from CLAUDE.md on
2026-09-16". In CLAUDE.md the section becomes:
"## Where the rest of this file went

Casebooks under `ledger-v2/studio-v2/`, by rule number: `casebook-claims.md`
1, 3, 4, 5, 5b, 6; `casebook-measurement.md` 2, 3b;
`casebook-build-and-evidence.md` 12; `operations.md` 7 to 11 and reporting;
`organization.md` the split; `runner.md` dispatch. The full index of the
2026-09-01 move heads `legacy/claude-md-superseded-2026-09-01.md`.
`ledger/verify.py` bounds this file at 2000 words."

EDIT I. One claim stated twice becomes one. Under "## 0.", the sentence pair
"The moat is social memory, consequence persistence and information,
unmistakably deeper than KCD2. Everything else is in service of it." becomes:
"The moat is social memory 93, consequence persistence 95, information 90,
against a best-in-class of 60, 85 and 65: unmistakably deeper than KCD2.
Everything else is in service of it."
and under "## The standard" the sentences from "The framing every plan is
judged against" to "Everything else serves it." are deleted, since section 0
now carries them with their numbers. Jafar's quote stays where it is.

EDIT J. The two paragraphs under "# CLAUDE.md: how to work on LEDGER", from
"Read this first, every session." to "so it goes to a casebook instead.",
become one:
"Read this first, every session. Every rule below was broken here, and its
incident is in the casebook listed at the bottom, by rule number. It was
16,291 words on 2026-09-01. A paragraph added here is read by every future
session, so it goes to a casebook instead, and every addition displaces its
own length: the ruling that adds names what moved."

EDIT K, which lands WITH the enforcement-claims check and not before it,
because it names a tool that has no runner until the check lands. This
supersedes the CLAUDE.md sentence first dictated in 2.1. Its own paragraph,
directly after the "Two are absolute" paragraph:
"NO ENFORCEMENT CLAIM WITHOUT A RUNNER (constitution law 13): a sentence here
that says something is checked names the tool, and
`tools/enforcement-claims-check.py` proves something runs it."

### Reserve, named so nobody has to judge next time

If the printed count after A to J is still over 2000, or when the next
addition comes: under "## The studio split", the tier description from "Tier
2 (read-only)" to "not to commit" moves intact to
`ledger-v2/studio-v2/organization.md` beside edit G's passage, and its place
in CLAUDE.md is taken by "Tiers and their limits:
`ledger-v2/studio-v2/organization.md`."

### What was measured and what was not

1998 and 2154 are the resident's printed counts. Every count behind the
ordering above is a hand count from this session's copy of CLAUDE.md,
labelled an estimate. The landing count is the resident's to print and paste
into the commit message beside the verify footer.
