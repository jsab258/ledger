<!--RULING spawn=2026-09-13T03:37:28Z-->
# LOG: ruling on the 269 and 268-plus-267-remainder batch (six triggers come home, the ceiling gets one home, the ninety rows say what they are), 2026-09-13

> **STATUS: LOG, 2026-09-13. NOT CURRENT** once section 10 carries the
> printed numbers. Decision record, binding on the resident, and on whoever
> next edits `.github/workflows/`, `tools/budget-ceiling.py`,
> `tools/budget-log-mark.py` or `ledger/verify.py`'s `tools_tracked`.

Author: tier-1 director spawned 2026-09-13T03:37:28Z, row 567 of
`.claude/agent-log.tsv`, read this session; the row reads
`2026-09-13T03:37:28Z` TAB `studio-director` TAB `fable` TAB `default` TAB
`ac7052c815800f3f7`. It is the second `studio-director` row dated 2026-09-13;
the first (562, 02:39:43Z) wrote the morning ruling this one continues. Rows
563 to 566 are the two builders this record reviews, an engine-specialist
(269) and an instrument-builder (268 plus 267's remainder), each spawned once
and resumed once. A resident never stamps a ruling; if the gate reports this
stamp unmatched or stale, the numbers go into section 10 and the stamp is not
touched.

## 0. What was read, what was not run, and what rests on the resident's prints

No shell in this seat: read, grep and glob only. I could not run a selftest,
`git diff`, `git status` or `git ls-remote`, so everything below that is a
number I did not read out of a file is the resident's or a builder's print,
cited as such, and section 9 makes the resident print it again from the tree
as staged. What I COULD verify by reading, I did, and I say which.

Read whole: CLAUDE.md, `.claude/rules/instruments.md`, `.claude/rules/ci.md`,
`ledger-v2/studio-v2/organization.md`, the morning ruling
(`decision-2026-09-13-ruling-the-ceiling-is-read-not-carried-batch.md`),
queues 254, 256, 267, 268, 269, the six workflows in the item, the four new
tools (`tools/workflow-branch-refs.py`, `tools/budget-ceiling.py`,
`tools/budget-ceiling-check.py`, `tools/budget-log-mark.py`),
`production/budget.md` lines 1 to 220, `production/logs/telegram-budget.log`
(all 90 rows, as marked), `production/NOW.md` 1 to 70 and 176 to 196, the
04:00Z wake record, the 2026-09-10 move-batch ruling section 5, D16 lines 8
to 39. Read in `ledger/verify.py`: `tools_tracked` (392 to 458),
`TOOL_SELFTESTS` and its helpers (1315 to 1493), `budget_ceiling_line` (1632
to 1699), `workflow_branch_refs` (2173 to 2268), the check registration (7476
to 7494), `SKIP_MARKS` (115). Read in the bot: 140 to 164, 498 to 622, 2095
to 2229. Read in glance: 62 to 93, 676 to 790. Grepped repo-wide for the dead
branch name (rule 1), for every retired name (`load_glance`,
`STANDING_CEILING_PCT`, `the-prose-and-the-machine-line-agree`,
`glance.py:653`), for `branches:`, `ref:` and `git push origin` across all 18
workflows, and for `higher` in the bot.

**Premise check.** A process batch about CI triggers and the budget
instrument. Nothing touches Meridian, the era, the moat or the visual bar;
section 0 of CLAUDE.md is unchanged. No tool enters from outside, so the
licence allowlist is not engaged. New text read carries no em-dash and no
italic.

## 1. The two halves as read, against what the items asked

### 269, the six workflows

**Done-line 1, met, and the per-workflow decisions are sound.** Read against
the files, not the report. `publish-glance`, `citypack-inventory` and
`citypack-fetch` carry `branches: [main]` with their path filters unchanged
(47, 47, 58). `ledger-build-mac`, `props-fetch` and `voice-candidates` carry
`on: workflow_dispatch:` alone (58 to 59, 46 to 47, 62 to 63). Each of the
five carries a decision comment naming what was read; the mac build's cites
the 2026-09-10 ruling and D16, and I checked the citation: the move-batch
record's section 5 finding 1 does say `ledger-build-mac.yml` stays dead by
ruling, and D16 line 11 does make Unity the legacy reference build.

**Across all 18 workflows, by grep and not by trust:** `branches:` appears in
exactly the three re-pointed files and reads `[main]` each time; `ref:`
appears only in `ledger-art-blender-preview.yml`, three times, all
expressions (`${{ github.sha }}`, `art/${{ ... }}`), which the check counts
into its `expr` bucket rather than testing; `git push origin` appears in five
files and every one pushes `HEAD:${GITHUB_REF_NAME}`. The dead branch name
appears in the workflows directory on ten lines and every one of them begins
with `#`. That is queue 254's done-line (the grep at zero outside prose, 18
files scanned) met on the tree as it sits.

**The resurrect hazard was not new, and the self-trigger was.** The builder's
report says nobody had noticed either. Half right: queue 254, filed
2026-09-10 by the move-batch ruling, names the four `ref:` sites and the two
pushes and says in its own words that a partial fix "creates the old branch in
the new repository". What 254 did NOT see, and the builder did, is that
`voice-candidates`' inventory job commits `tools/voice-fetch/vctk-speakers.json`
inside its own old `tools/voice-fetch/**` filter, so a dispatched inventory
run would have fired a second run of `page` and `diagnose` on its own commit.
That finding is real and it is the reason deleting that trigger is right
rather than merely allowed (section 2, Q3).

**Done-line 4, met, and the check is the best part of this half.**
`tools/workflow-branch-refs.py` reads `git ls-remote --heads origin` first,
falls back to local tracking refs under a key that says `MAY-BE-STALE`, and
skips out loud with the words nothing measured when neither answers (107 to
131). It reads trigger filters, checkout refs AND git commands (169 to 205),
which is the three-shape fault 254 described. Its selftest is accepting case
first on the live tree with a non-zero denominator required (445), three
synthetic rejecting shapes, the ratchet case that plants EXISTING names in the
same slots (466 to 469), a comment quoting the dead name that must pass (472
to 475), expressions and globs counted into `skipped=` (478 to 481), and an
empty tree that must say nothing measured (484 to 487): eight checks. Wired at
`verify.py:2173`, registered at 7484; the live verdict is read before the
selftest, for a reason printed from a failure rather than chosen (2194 to
2201). `SKIP_MARKS` is `("SKIPPED", "NOT CHECKED")` and the clean output's
`skipped=` is lower case, so a clean run cannot read as a skip; I checked
because that is the instrument fault to suspect first.

**Done-lines 2 and 3 are AFTER THE PUSH and section 9 carries them.** The
landing push fires `publish-glance` (four of its paths are in this batch:
`production/budget.md`, `tools/glance.py`, `production/queue/**`, and its own
file) and fires `citypack-inventory` (its own file is in its filter). Those two
runs are the proof for the two cheap workflows; `citypack-fetch` is ruled in
section 2, Q2.

### 268, the pattern's home and the document guard

**All four deliverables of section 7 are in the tree as specified.** (i)
`tools/budget-ceiling.py`: standard library only, `BUDGET`, `CEILING`,
`ROW_CEILING`, `PROSE_CEILING`, `line_hits`, `ceiling_from_text` with its
`(pct, from, why)` contract and its refusal on disagreement (117 to 179).
Glance imports it by path at module level and refuses to start without it
(62 to 83), the bot imports it by path from its own repository and turns a
failed import into a refusal (503 to 554), the guard imports it and exits 4
without it (58 to 79). `load_glance` is gone from the bot: the grep finds the
name nowhere in the tree. `read_budget` in glance keeps its row preference
and calls the shared reader for the standing half (762 to 773). (ii)
`tools/budget-ceiling-check.py`: exactly one machine line, zero and two both
named (`machine-line/deleted`, `machine-line/duplicated`), the prose held
against it (`prose/missing`, `prose/disagrees`), the third check printing
"cannot run" rather than passing when the first two failed (187 to 191), exit
codes distinct per outcome, the live document walked first and six synthetic
fixtures on every plain invocation, each printing THIS guard's verdict beside
the bot reader's on the same bytes (260 to 289). Wired at `verify.py:1632`,
which reads the LAST line with the prefix, for a reason the guard's own
comment at 316 to 321 records from a failure. (iii) The pin: `STANDING_CEILING_PCT`
is a local inside `accept/ceiling-is-the-standing-85` (bot 2134), the top
comment says so (148 to 155), and the name appears in the module namespace
nowhere. (iv) The asymmetry: `accept/ceiling-two-lines-that-agree-are-answered`
(bot 2161 to 2168) proves the lenient half with a planted duplicate at 71 and
prints `guardOnTheSameBytes=fails-by-design`; the guard's
`reject/two-lines-at-the-same-number` proves the strict half. Nobody aligned
them.

**The retired case is retired and the cross-check has one implementation.**
`accept/the-prose-and-the-machine-line-agree` survives only as a comment
naming its own retirement (bot 2140 to 2148). The word `higher` occurs in the
bot at 603, 646 and 702, all three sentences to Jafar, none a pattern. The
prose regex lives in `budget-ceiling.py` alone (`PROSE_CEILING`, 95 to 97) and
is read by the guard alone. The suite's count stays at 151 because one case
was retired and one planted-71 case, `accept/ceiling-is-whatever-the-document-says`
(2174 to 2176), sits where it was; that case asserts a number travelled from a
document and is not a second copy of anything. Verified by reading, not by
the count.

### 267, points 3 and 4

**Met on this container, which the morning ruling made the accepting case.**
`tools/budget-log-mark.py` marks rather than deletes, writes no header (the
reason at 35 to 40 is right: `budget_log_lines` counts lines and calls them
rows, and the bot's own case pins 90..90), and checks its own effect by
comparing the timestamp and six measured keys before and after, refusing the
write with exit 4 if any moved (242 to 273, 353 to 364). The read-back prints
`rows=N readings=A/N-rows fixtures=B/N-rows unmarked=C/N-rows` with the file's
state, and an absent file prints NOTHING MEASURED and never zero (201 to 225).
The live log, read by me: 90 rows, every one carrying
`source=selftest-fixture markedBy=queue267/tools/budget-log-mark.py markedOn=2026-09-13`,
every measured value where it was (`ceilingPct=80` on all ninety, which is
267's own rule: a fixture row that quietly acquired 85 would be a second
falsification). The backup `telegram-budget.premark-20260913T032423.log` sits
beside it. Its selftest is thirteen cases, accepting first and the first one
the live log read and never written, with the last case measuring the suite
itself (502 to 508).

## 2. The eight questions, ruled

**Q1, `citypack-inventory` committing to `main` on a push: ACCEPTABLE AS IT
STANDS, and EXPECTED ON THIS VERY PUSH.** Four reasons and one cost. First,
it is a restoration and not a new behaviour: this job committed its three
JSON files to the working branch of the old repository on every fetcher
edit, and `main` is that branch's successor; the CI-commits-its-evidence
pattern is the one `.claude/rules/ci.md` names as the channel that works.
Second, it is the cheap class rule 9 protects: one minute of metadata on
`ubuntu-latest`, its own concurrency group, and it cannot start anything
else. I checked the last claim against the other ten `paths:` blocks rather
than taking it: the catalogue commit touches `tools/citypack/*.json`, and
`ledger-core-tests` watches `tools/*.py` one level deep and `ledger/**`, so a
JSON two levels down matches no workflow's filter. Third, it cannot
re-trigger itself: its filter is its own file plus the two fetchers, and it
commits three files that are in neither list. Fourth, the landing push fires
it because its own file is in its filter, so this push IS its proof run for
done-line 2, at no cost. The cost is real and it is the resident's to carry:
if ambientCG's catalogue has drifted since the last commit of
`tools/citypack/catalogue.json`, one CI commit lands on `main` a minute or two
after the push, and this job's push loop retries six times WITHOUT a rebase
(99 to 103), so a resident push inside that window turns the run red with the
catalogue saved only as an artifact. Nothing is lost either way. The rule is
`git pull --rebase origin main` before the next push, written into section 9.
Not dispatch-only, which would forfeit the free proof run and buy nothing;
not commit-only-on-dispatch, which is a conditional added for a benefit
nobody has asked for, in the one file whose own header records what a
conditional cost here.

**Q2, proving `citypack-fetch`'s push filter: NO DISPATCH. Rule 9 wins on
the run and rule 6 is not sacrificed, because the mechanism is exercised and
the words on the item say "unrun", not "proven".** A dispatch is up to thirty
minutes of downloads with no skip-if-present path, committing twelve textures
into `ledger/Assets/StreamingAssets/CityPack`, which is inside the tree D16
archived on 2026-09-10 (D16 line 11: Unity is the legacy reference build,
archived and never deleted). That is an expensive job with no consumer, and
a dispatch would not prove the filter anyway, which the builder said plainly.
What proves the filter is the mechanism: `push` on `main` with a `paths:`
filter, in this repository, is exercised by `citypack-inventory`'s landing
run, and `citypack-fetch` differs from it only in the list, which is one
literal path. The branch name is proven by the check. So 269's record reads:
`citypack-fetch` trigger proven at mechanism level, job unrun since the move,
dormant under D16, proven at its own level on the day `tools/citypack/choices.json`
next changes, which is a decision about the archived project. Rule 6 forbids
claiming "done" on a read; it does not require running a job nobody wants
run, and the sentence above is a true sentence with no green in it. One
sentence naming D16 goes into that workflow's decision comment, dictated in
section 6 (c), because the builder read the cost and the self-trigger for
this file and not the premise, and the next reader who edits `choices.json`
thinking it serves the game deserves to be told in the file.

**Q3, three workflows dispatch-only: RESTORATION, not loss, on all three, and
the one thing a push used to buy is named so it can be restored on purpose.**
`ledger-build-mac`: ruled push-dead on 2026-09-10 (section 5 finding 1), and
its own header has said since 15 August that macOS minutes are ten times the
Linux rate and the seat is one. `props-fetch`: its own first paragraph says
"Dispatch-only: it costs a few tens of MB of downloads and there is no reason
for it to ride every push", and the only reason it was push-triggered was a
dispatch-404 premise the builder measured dead (18 of 18 registered,
`state=active`, default branch `main`). `voice-candidates`: the same dead
premise, plus the self-trigger. What a push actually bought there was the
`page` job (a phone-size load of the listening page, rule 4's instrument for
that deliverable) and `diagnose`, up to twenty runner-minutes per edit under
`tools/voice-fetch/**`. Nobody is producing that deliverable today; the queue
behind this batch is 254 to 265 and none of it is voice work. When voice work
resumes, a push trigger scoped to the page tools and EXCLUDING the committed
JSON is the deliberate way back, and the file's "THE PATHS IT USED TO WATCH"
paragraph is there for that day. Not a loss anyone will notice this month;
named so that nobody has to rediscover it.

**Q4, the prose pattern matching a quotation: COUNTING IT IS RIGHT, the
denominator on the day the morning ruling was written was three and not two,
and the pattern is not loosened.** I read the three sites. Line 44, "THE
STANDING CEILING IS 85 ON THE HIGHER METER." Lines 46 to 47, inside the
resident's own paragraph: `under "THE CEILING IS 85 ON THE` and then, after
a line break, `HIGHER METER, STANDING"`. Line 117, "THE CEILING IS 85 ON THE
HIGHER METER, STANDING, ruled by Jafar 2026-09-10." `PROSE_CEILING` uses
`\s+` between words, so the quotation matches across the break and
`line_hits` reports it at the line where the match starts, 46. Line 125's
"The ceiling ... is 85 on the governing meter" does not match, because it
says governing. So `proseAt=44/46/117`, and the morning ruling's "44 and
109" (109 is 117 after the eight lines the builder added above it) missed
the spanning match. Why counting it is right: the guard exists so that no
sentence of that shape in the file says a different number from the machine
line, and a quotation of the heading is a sentence a reader reads; if the
ceiling moves to 90 and line 46 still quotes 85, line 46 then names a heading
that no longer exists, and a guard that named it would be doing its job. Why
spanning lines is right: the alternative, a single-line pattern, would let a
paragraph reflow silently drop a statement from the census, which is the
worse direction. The false-positive risk is real and is named rather than
designed around: a HISTORICAL sentence written in the exact phrase with an
old number ("the header said THE CEILING IS 80 ON THE HIGHER METER") would go
red. Today there is none (the census is three hits, all 85; the file already
writes its history in other words, as line 167's "80 until Jafar raised it"
does). When one is written, the remedy is to reword the history line the
guard names, and never to loosen the pattern: rule 2, and `production/budget.md`
line 160 says the same of `ROW_CEILING` in its own words.

**Q5, the separator for the ninety rows: THE BUILDER'S BAR IS THE RIGHT
ONE, THE BRIEF WAS WRONG AND NOT MERELY NARROW, and the record says so.**
"Every row lacking `ceilingFrom=` is a fixture" is necessary and not
sufficient: the key was born at 0e522c1f, and a reading Jafar typed on his PC
before that commit lacks it too. His bot started at 01:14:15Z on 2026-09-13
from a checkout carrying `CEILING_PCT = 80` and asked him for a reading; if
he answered before the PC pulls this commit, the PC's log holds a real
reading with no `ceilingFrom=`, and the brief's rule would have marked it a
fixture. That is the 267 fault committed a second time in the other
direction, which is exactly what the builder said. The rule it built instead
is a bound set from a printed series (rule 2), and I verified the series
against the log rather than the docstring: thirty groups of three, every one
40/62 then 40/77 then 40/77; the widest intra-group span is 2 seconds (for
instance rows 10 to 12, 19:40:55 to 19:40:57); the narrowest gap between
groups is 22 seconds (rows 54 to 55, 13:34:49 to 13:35:11). The bound of 5
seconds sits above the one and well under the other. Anything the rule
cannot place stays unmarked and is COUNTED as unmarked, which is the safe
direction: a real reading is never marked, and a PC group that a slow
machine stretched past 5 seconds is reported as `unmarked=3`, not guessed.
So the PC run, which is 267's second accepting case, is read like this: if
its print shows `unmarked=0` the log is clean; if it shows `unmarked>0` the
resident opens those rows and reads them before anyone touches the bound,
and a change to the bound needs the PC's own printed series, not this one.

**Q6, the one changed clause in the moved string: UPHELD, and the edit to
`production/budget.md` is REQUIRED, not uninstructed.** The morning ruling's
"intact" bound the `(pct, from, why)` contract and the refusal on
disagreement, both of which are intact. The sentence itself now prints from
three vantages, and "Nothing in this bot" printed by a commit gate is a
false clause in the one place a reader checks a refusal; "No reader of that
line" is true from all three. The change is named beside the string with its
reason (`budget-ceiling.py` 158 to 164), the bot's two assertions on that
refusal are on other substrings (`2 line(s) were examined` at 2200,
`line(s) 1/3 of 3 examined` at 2210) and both are untouched, and the bot's own
OSError refusal still says "Nothing in this bot carries one of its own"
(590), which is correct where it sits because there it IS the bot. The
document edit: a document of record named `tools/glance.py:653` as the
contract, the move made that false, and rule 1's corollary is that a false
sentence is fixed wherever it sits. The builder fixed it and removed the
line number while there, which is right (a line number in a document is a
claim that decays). I read the result: the machine line at 49 is unchanged,
the quoted regex at 55 cannot match itself, and the new paragraph at 57 to
63 says one home and three importers, which is true. Two dated entries
elsewhere still say `glance.py:653` in the present tense (`NOW.md` 142 and
159, the wake's second addendum); they are log entries dated 03:00Z, when
the sentence was true, and the NOW.md block in section 11 states the move
above them. They stand.

**Q7, tools no workflow names: THE CLASS IS REAL, IT IS NAMED, IT IS FILED,
AND IT IS NOT TAKEN IN THIS BATCH.** `tools_tracked` walks the eighteen
workflow files for `tools/...py|sh` strings and follows them transitively
(432 to 445). Of the four new tools, two are reached only because comment
lines in `tools/glance.py` (90 and 683) happen to name
`tools/budget-ceiling.py` and `tools/budget-ceiling-check.py`, and two,
`tools/workflow-branch-refs.py` and `tools/budget-log-mark.py`, are named by
`ledger/verify.py` and by themselves and by nothing else (grep: three files).
So the resident's point holds for both, and the reach that does exist rests
on a comment, which is the accidental coverage that decays. The failure
shape, though, is not the silent one `tools_tracked` was built for: after Q8
lands, a fresh checkout missing any of the four goes RED in verify (2210 "no
tool on disk"; 1662 to 1680 red on a missing guard; 1373 "SELFTEST DID NOT
REPORT" on a missing marker), which is loud. The fix is `tools_tracked` taking
`ledger/verify.py` as a second root, with a second pattern for the
`"tools" / "<name>.py"` join form and the `TOOL_SELFTESTS` rels, printing the
reach per root. That is builder work in a file two builders just left, and a
third hand in it before this lands is the hazard the resident named in Q8.
Filed as queue 270 in section 7 with today's measured denominator. Today's
condition is mechanical: `git status --short` listing all four as `A`, staged
BY NAME, and `git ls-files` returning all four (section 9, condition 2).

**Q8, the marking tool's selftest not in `TOOL_SELFTESTS`: LANDS NOW,
dictated.** A selftest nobody runs is the fault that table's own comment
describes, and its absence would also leave the fresh-checkout case in Q7
silent for this one file. The tool prints `N passed, M failed` in the shape
`TOOL_COUNT_RE` reads and exits 0 or 3, so it is one row, one four-line
function and one name in the registration tuple, all dictated in section 6
(a), and the check count goes 83 to 84. The builder left it out because it
was told to touch one row and nothing else while another builder held the
file; that was the right reading of its brief, and the file is settled now.

## 3. Findings the brief did not have

**F1, queue hygiene, and it is the resident's.** Queue 254 (READY since
2026-09-10, "six push filters name a dead branch, and one would resurrect
it") and queue 269 (opened 2026-09-13) are one fault filed twice: the same
six workflows, the same sites, the same remedy. `NOW.md` line 193 says
"Filed as 269" and nothing there says 254 was read. The morning ruling
narrowed 269 per workflow; that narrowing is the operative text and 254
closes with 269 on the same evidence. One thing 254 asked for that 269 did
not: a dispatched `voice-candidates` inventory run landing its table on
`main` with `git ls-remote` showing no new branch. NOT TAKEN: the hazard it
tests is closed by construction (no literal branch name remains outside
prose, grep at zero over 18 files) and kept closed by the check, and a
metadata stream with a 45-minute timeout that commits `vctk-speakers.json`
to `main` in the middle of a batch is rule 9 in reverse. The loop is proven
by its first real dispatch when the voice work resumes, and 254's close-out
line says so.

**F2, queue 256's ordering clause, superseded on the trigger and intact on
the links.** 256 says the `publish-glance` push filter "moves to `main`
(queue 254 leaves it alone for this reason)" only after one dispatched run
prints a served commit, and names the risk: flipping the LINKS early puts a
404 on his phone. The morning ruling moved the trigger now and is the newer
text; there is no contradiction on the substance, because moving the trigger
sends nobody anywhere (the seven link sites still point at the frozen old
site until 256 lands) and the landing push's run is the very run 256's step
1 asks for, with the same `--check` step printing the served commit or the
Pages refusal that is the ONE card for Jafar. So 256's step 1 is satisfied by
this landing, its step 2 (the links, `producer-check.py`'s constant, the two
tree links) is NOT in this batch (rule 11: adjacent, named, queued), and its
amendment about `production/site-served.txt` provenance stands for the day
the links move.

**F3, one false clause in a case name, dictated.** `budget-log-mark.py`
plants three matching rows at 10:00:00, 10:01:00 and 10:02:00 (433 to 434), a
span of two minutes, and names the case
`reject/three-matching-rows-ten-minutes-apart-are-not-a-group`, with "ten
minutes" at 427 and 449 too. The assertion is right (120 seconds is over the
5-second bound by any reading); the words are not. Section 6 (b).

**F4, D16 unread for `citypack-fetch`.** Section 2 Q2; section 6 (c).

**F5, the dead branch name outside the workflows, out of scope and counted.**
My grep for the token with the legacy directory excluded hit its cap at 60
lines; the hits are `.bat` launchers under `tools/voice-live/`,
`tools/mixamo-pick/`, `tools/runner/`, `tools/imagegen/`, `tools/meshgen/`,
`run-night.ps1`, `MIGRATE TO LEDGER.bat`, `runner.md`, and archive links in
dated records. That is queue 255 (the 2026-09-10 ruling's findings 2 to 4),
not this item, and none of it runs on his disk until 257 lands. Named so the
next reader does not re-find it from the same grep.

**F6, a known limit of the new check, filed.** `claims()` examines a `run:`
line for git targets only when that line contains `git ` (203), so a
multi-line git command's continuation lines are not examined:
`publish-glance.yml` 197 to 198 carries `refs/heads/art/atlas-01` on a
continuation line. Today that name exists, so nothing is missed, and the same
command's `rev-parse origin/art/atlas-01` two lines down IS tested. Queue
271, small, in section 7.

## 4. Verdict

**BOTH HALVES LAND, WITH NAMED CHANGES**, none of them a builder round, all
hand-applied by the resident from section 6: (a) one row, one function and
one name in `ledger/verify.py`; (b) one word at three sites in
`tools/budget-log-mark.py`; (c) one comment block in
`.github/workflows/citypack-fetch.yml`. No threshold moved, no instrument
weakened, no fallback number anywhere, no gate loosened to clear a red. The
one red the resident can clear is the untracked-tools line, by staging the
four files by name; the other red is this stamp.

## 5. What is landed and what is closed, which are different facts

**269: LANDED; CLOSES on done-line 3.** The served page opened after the
landing push's `publish-glance` run and the budget bar reading 85, recorded
with the run's `servedCommit`. Done-line 2 is met for `publish-glance` and
`citypack-inventory` by the landing push's runs, and for `citypack-fetch` at
mechanism level only, worded as section 2 Q2 says. Done-lines 1 and 4 are met
on the tree as read.

**254: CLOSES WITH 269**, same evidence, its third done-line superseded as
F1 records.

**256: STEP 1 SATISFIED by the landing run; the item stays open on step 2**,
the links, which are not this batch.

**268: CLOSED AT LANDING.** All four deliverables are in the tree, called by
`ledger/verify.py` at every commit, and the footer's `budget ceiling:` line is
the call-site proof rule 6 asks for. Nothing about it waits on the PC.

**267: POINTS 3 AND 4 LANDED; CLOSES on the PC run**, which is the second
accepting case: `python3 tools/budget-log-mark.py --mark --log <the PC's copy>`
when the runner returns, its before and after counts printed, read as section
2 Q5 says.

**266: UNCHANGED**, open on the first PC row carrying `ceilingFrom=`.

## 6. Dictated text, resident to apply before the commit

**(a) `ledger/verify.py`, three edits.**

In `TOOL_SELFTESTS`, directly after the line
`    ("producer day", "tools/producer-day.py"),` and before the closing `)`:

    # THE LOG JAFAR READS BACK, added 2026-09-13 (queue 267, points 3 and 4).
    # Its suite reads this container's live log twice and writes it never,
    # plants the four row shapes the PC's copy can hold at once (two verify
    # runs, one reading typed since the fix, one pre-fix row that is not a
    # fixture, three matching rows too far apart to be one), and proves the
    # marking tool REFUSES to move a measured value. Without this row it is
    # the sixth selftest nobody runs, which is the fault this table's own
    # comment describes, and a fresh checkout missing the tool would say
    # nothing until the PC runner tried to mark its log.
    ("budget log", "tools/budget-log-mark.py"),

Directly after the `producer_day_selftest` function (its body ends
`return _tool_selftest_run(9)`), one function:

    def budget_log_mark_selftest():
        """The budget log's read-back and marking (queue 267, points 3 and 4):
        the denominator on read-back, a fixture group recognised by shape and
        span rather than by a missing key, a typed reading left byte for byte,
        and a moved value refusing the write."""
        return _tool_selftest_run(10)

In the registration tuple (the `for fn in (` block near line 7477), change
`producer_day_selftest, systems_inventory,` to
`producer_day_selftest, budget_log_mark_selftest, systems_inventory,`.

**(b) `tools/budget-log-mark.py`, one word at three sites.** Line 427,
`# fixture, and three matching rows spread over ten minutes.` becomes
`# fixture, and three matching rows spread over two minutes.` Line 449,
`"over ten minutes" % c0["unmarked"])` becomes
`"over two minutes" % c0["unmarked"])`. Line 450, the case name
`reject/three-matching-rows-ten-minutes-apart-are-not-a-group` becomes
`reject/three-matching-rows-two-minutes-apart-are-not-a-group`. The case
name is referenced nowhere else (grep: this file only).

**(c) `.github/workflows/citypack-fetch.yml`, directly after the comment
line ending `so it cannot re-trigger itself.` (line 49 as read) and before
`on:`:**

    #   WHAT IT COMMITS INTO IS THE LEGACY REFERENCE BUILD. D16 (2026-09-10)
    #     made Unreal the engine and archived the Unity tree, never deleted,
    #     and ledger/Assets/StreamingAssets/CityPack is inside that tree. So
    #     committing choices.json is a decision about the archived project and
    #     not about the game. This trigger has not fired since the move: its
    #     filter is proven at mechanism level by citypack-inventory's landing
    #     run of 2026-09-13 (push on main with a paths filter, same repository,
    #     a different list), and the job itself is UNRUN here and dormant by
    #     premise, proven at its own level on the day that file next changes.
    #     Ruled 2026-09-13,
    #     decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md.

## 7. Queue amendments, resident to apply

**269.** Under STATUS: `LANDED <sha> 2026-09-13 under
decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md;
CLOSES on done-line 3 (the served page opened, bar reads 85, servedCommit
recorded). publish-glance and citypack-inventory proven by the landing
push's runs; citypack-fetch proven at mechanism level only, job unrun since
the move and dormant under D16, proven at its own level when
tools/citypack/choices.json next changes. Duplicates 254, which closes with
this.` And under "What this does not cover", one line: the check does not
examine continuation lines of a multi-line git command (queue 271).

**254.** Under STATUS: `CLOSES WITH 269, same evidence, 2026-09-13. The
dispatched voice-candidates inventory run this item asked for is NOT taken:
no literal branch name remains outside prose (grep 0 over 18 files) and
tools/workflow-branch-refs.py keeps it so; the loop is proven by its first
real dispatch when voice work resumes.`

**256.** Under STATUS: `STEP 1 SATISFIED 2026-09-13 by the landing push's
publish-glance run (servedCommit or the Pages refusal, whichever it printed,
quoted here: ...). The trigger moved under the 2026-09-13 morning ruling; the
LINKS have not and are this item. Step 2 next.`

**268.** Under STATUS: `CLOSED <sha> 2026-09-13 under
decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md: one
home (tools/budget-ceiling.py), three importers, the document guard in
ledger/verify.py at every commit (budget ceiling: line in the footer), the
pin a local in the case that reads it, the asymmetry proven on both sides.
proseAt=44/46/117 on the day of closing, three statements including the
quotation at 46 to 47, ruled counted.`

**267.** Under STATUS: `POINTS 3 AND 4 LANDED <sha> 2026-09-13; CLOSES on
the PC run: python3 tools/budget-log-mark.py --mark --log <PC copy>, counts
printed before and after; unmarked>0 on the PC means read those rows before
touching the 5-second bound, and a new bound needs the PC's printed series.`
And in point 3's text, strike "every row written from now on carries
ceilingFrom= and none of the ninety has that key, so pre-fix rows are
separable by content" and replace with: `a missing ceilingFrom= is necessary
and not sufficient, because a reading typed on the PC before 0e522c1f lacks
it too; the tool recognises a fixture GROUP by shape and span (40/62, 40/77,
40/77, within 5 seconds, bound set from the printed series) and counts
everything else as unmarked.`

**270, NEW: `tools_tracked` cannot see a tool only verify.py runs.** The
fault, measured 2026-09-13: four new tools in one batch; two
(`tools/budget-ceiling.py`, `tools/budget-ceiling-check.py`) reached only
through comment lines 90 and 683 of `tools/glance.py`; two
(`tools/workflow-branch-refs.py`, `tools/budget-log-mark.py`) reached by
nothing, named only by `ledger/verify.py` and by themselves. Done looks like:
`tools_tracked` walks `ledger/verify.py` as a second root, matching both the
`tools/<name>.py` string form and the `"tools" / "<name>.py"` join form and
the `TOOL_SELFTESTS` rels; prints reach per root (`viaWorkflows=N
viaVerify=M`, with the count reached only through a comment named if it can
be told); accepting case the live tree, rejecting case a synthetic verify
text naming a tool that exists nowhere. Risk: none; it is a wider denominator
on an existing check.

**271, NEW: `workflow-branch-refs` skips continuation lines of a multi-line
git command.** `claims()` examines a line for git targets only when it
contains `git `; `publish-glance.yml` 197 to 198 carries
`refs/heads/art/atlas-01` on a continuation. Done looks like: a `run:` block
is joined on backslash-newline before the git pass, with a fixture planting
a dead name on a continuation line, and the live tree still passing.

## 8. Quality ladder at close

Best available for the trigger class: a check that reads the repository's
own branch list over the network, names its source and falls back out loud,
tests three shapes of the fault, plants existing names so it cannot become a
ratchet, counts what it cannot test, and treats a comment as prose so the
repair's own explanation cannot fail it. Next rung, named: continuation lines
(271). For the ceiling: one pattern, one home, three importers, a guard whose
fixtures print both verdicts on the same bytes, the pin a local in the only
case that reads it. The blank rung is unchanged from this morning: what the
bot does if a per-session ceiling ever returns, a decision for that day. For
the log: every row says what it is and the read-back carries its
denominator. Next rung, the PC run (267's close); the rung after it, the
Producer quoting `readings=A/N-rows` whenever a brief cites that log, is
adjacent and not taken here.

## 9. Conditions the resident prints before the commit, and after the push

1. Section 6 applied; `git diff --stat` naming `ledger/verify.py`,
   `tools/budget-log-mark.py` and `.github/workflows/citypack-fetch.yml`
   among the changed files; unstaged EMPTY after staging, so the tested tree
   and the staged tree are one.
2. `git status --short tools/ .github/workflows/` pasted, showing
   `tools/budget-ceiling.py`, `tools/budget-ceiling-check.py`,
   `tools/budget-log-mark.py` and `tools/workflow-branch-refs.py` as `A`,
   each staged BY NAME and never by `git add tools/`; then
   `git ls-files tools/budget-ceiling.py tools/budget-ceiling-check.py tools/budget-log-mark.py tools/workflow-branch-refs.py`
   printing all four.
3. `python3 tools/budget-log-mark.py --selftest` on the staged file: `13
   passed, 0 failed`, the renamed case line
   `reject/three-matching-rows-two-minutes-apart-are-not-a-group  pass`, and
   the live line reading `rows=90 readings=0/90-rows fixtures=90/90-rows
   unmarked=0/90-rows`. Then `python3 tools/budget-log-mark.py` (read-back,
   no `--mark`) pasted whole.
4. `python3 tools/budget-ceiling-check.py`, its done line pasted whole,
   reading `machineLines=1/1-wanted machineAt=49 machinePct=85
   proseStatements=3 proseAt=44/46/117 proseValues=85 checksRun=3/3-checks
   faults=0/3-checks-that-ran fixturesAgreed=6/6-fixtures`. A different
   `proseAt` is a finding, not a typo to fix in this record.
5. `python3 tools/runner/telegram-bot.py --selftest` on the staged file:
   cases passed and failed, `liveBudgetLogLines=90..90`, the `ceiling:` line
   reading `ceilingPct=85 ceilingFrom=production/budget.md:49..the-standing-line`,
   the `duplicate that agrees:` line reading
   `ceilingFrom=production/budget.md:1/3..the-standing-line`, and the two
   `refuses:` lines. And the namespace print the resident already made, made
   again on the staged file and pasted: the module loaded by path has no
   `STANDING_CEILING_PCT`, no `load_glance`, no `ceiling_from_text`, and
   `read_ceiling()` returns `(85, 'production/budget.md:49..the-standing-line', '')`.
6. `python3 tools/glance.py --selftest` green (the resident's print: 80/0),
   and one live run's ceiling line, `ceilingPct=85 ceilingFrom=the-standing-line..`.
7. `python3 tools/workflow-branch-refs.py` pasted whole: `0 dead of N
   branch name(s) tested in 18 workflow(s)`, `branchSource=git-ls-remote/origin`,
   `comparedAgainst=art/atlas-01,main,pc-inbox,pc-results`, and the
   `skipped=` buckets; then `--selftest`: `8 passed, 0 failed, 8 checks run`.
   If either prints SKIPPED, the network changed since the builder measured
   `ls-remote` at 0.8 seconds; that is a finding, the commit message says
   the check was skipped, and this record's section 10 says so.
8. `grep -c 'claude/game-dev-ai-automation-2h67ix' .github/workflows/*.yml`
   per file, and `grep -n` over the same showing every hit begins with `#`:
   254's done-line, denominator 18 files.
9. The registry read behind "18 of 18, state=active": the builder's verbatim
   print quoted into 269, or a fresh
   `gh api repos/jsab258/ledger/actions/workflows --jq '.total_count, [.workflows[].state]'`
   pasted. A sentence I could not verify from this seat is not a fact until
   its print is beside it.
10. `python3 ledger/verify.py` green, footer pasted FROM
    `ledger/.verify-footer`, `checks=84ran/0skipped/84total`, the cadence line
    reading REVIEWED and naming ONE ruling record paired to a director row
    newer than the reference, which is this stamp; the `budget ceiling:` and
    `workflow branch refs` lines quoted; the `budget log selftest ok (13
    checks, 0 failed)` line present.
11. `python3 tools/docs-check.py`: this record LOG, dated, em-dash count 0,
    italic count 0.
12. Queues 254, 256, 267, 268, 269 amended and 270, 271 filed per section 7;
    NOW.md block from section 11 pasted at the top.
13. After the push, rule 9 first: this push triggers `publish-glance` (four
    of its paths are in the batch) and `citypack-inventory` (its own file),
    besides the cheap checks that always run. The sha captured BEFORE the
    push; both runs watched BY ANCESTRY, never by branch movement. For
    `publish-glance`: the `--check` keys (`servedCommit`, or the Pages
    refusal that is 256's one card for Jafar), then the page OPENED and the
    bar read (rule 4), 85, recorded in 269 as its closing line. For
    `citypack-inventory`: the run appeared; if it committed, the CI commit's
    sha noted in 269 and `git pull --rebase origin main` BEFORE the next
    push, because its push loop does not rebase.
14. Rule 8 and rule 13: the watcher for condition 13 is armed in the same
    turn as the push, and a one-shot three minutes out resumes the next queue
    item while budget remains. His last reading is 78 total and 82 Fable
    against 85, Fable is the binding meter, this spawn is on it, and the
    queue behind this batch (255 to 265, then 256's step 2 and 270, 271) is
    builder work on the other meter.
15. The PC: nothing is expected (`pc-results` unmoved since 2026-09-11,
    runner off). 266 and 267 stay open on their PC conditions and the
    2026-09-13 brief carries the restart line the wake record already orders.

## 10. Landing

Filled by the resident 2026-09-13T04:25Z, one line per condition.

1. SECTION 6 APPLIED, three files: `ledger/verify.py`, `tools/budget-log-mark.py`
   and `.github/workflows/citypack-fetch.yml`. Unstaged empty at commit, so the
   tested tree and the staged tree were one.
2. THE FOUR NEW TOOLS STAGED BY NAME, never by `git add tools/`, each reading
   `A` and each returned by `git ls-files`: budget-ceiling.py,
   budget-ceiling-check.py, budget-log-mark.py, workflow-branch-refs.py. Two of
   the four are invisible to `tools_tracked`, which is queue 270.
3. `budget-log-mark --selftest`: 13 passed, 0 failed, the renamed case
   `reject/three-matching-rows-two-minutes-apart-are-not-a-group pass`, live
   line `rows=90 readings=0/90-rows fixtures=90/90-rows unmarked=0/90-rows`.
   Read-back: "90 row(s): 0 reading(s) Jafar typed, 90 fixture row(s) from the
   selftest, 0 whose provenance this tool will not guess at".
4. THE GUARD'S DONE LINE, whole: `budget-ceiling-check: PASS
   doc=production/budget.md linesExamined=609 machineLines=1/1-wanted
   machineAt=49 machinePct=85 proseStatements=3 proseAt=44/46/117
   proseValues=85 checksRun=3/3-checks faults=0/3-checks-that-ran
   fixturesAgreed=6/6-fixtures`. proseAt is 44/46/117 as this record rules, not
   the morning ruling's 44 and 109.
5. BOT SELFTEST 151 passed, 0 failed. `liveBudgetLogLines=90..90`. `ceiling:
   ceilingPct=85 ceilingFrom=production/budget.md:49..the-standing-line`.
   `duplicate that agrees: ceilingPct=71
   ceilingFrom=production/budget.md:1/3..the-standing-line
   guardOnTheSameBytes=fails-by-design`, which is the ruled asymmetry measured
   on one line rather than argued. Namespace on the staged file:
   STANDING_CEILING_PCT False, load_glance False, ceiling_from_text False, and
   `read_ceiling()` returns `(85, 'production/budget.md:49..the-standing-line',
   '')`.
6. GLANCE `80 check(s) run, 0 failed`, live run `ceilingPct=85
   ceilingFrom=the-standing-line..2026-09-11 ceilingStandingPct=85`.
7. `workflow-branch-refs`: `0 dead of 8 branch name(s) tested in 18
   workflow(s)`, `walked=18workflow(s) examined=38ref(s) tested=8
   skipped=30expr/0glob/0sha/0empty`,
   `branchSource=git-ls-remote/origin repoBranches=4
   comparedAgainst=art/atlas-01,main,pc-inbox,pc-results`. `--selftest`: 8
   passed, 0 failed. Neither printed SKIPPED, so the network held.
8. THE DEAD NAME: 9 hits across 6 files of 18 walked, and all 9 begin with `#`.
   `liveDeadBranchRefs=0 commentLines=9 of 9 hit(s)`. THE BUILDER REPORTED TEN
   AND I MEASURE NINE; mine is the tree as committed and the difference is
   recorded rather than reconciled away.
9. THE REGISTRY READ, fresh rather than quoted: `total_count 18`, and every one
   of the 18 carries `state: active`. This is the sentence the ruling refused to
   let stand without its print, and it now has one.
10. VERIFY GREEN, `checks=84ran/0skipped/84total`, cadence `over threshold,
    REVIEWED`, `rulingRecords=1/83`, `1 ruling record(s) paired to a director
    row newer than the reference`. `budget ceiling: faults=0/3-checks-that-ran
    machineLines=1/1-wanted prose=3 of 609 line(s) examined [fixtures
    6/6-fixtures]`. `0 workflow branch ref(s) absent of 8 tested`. `budget log
    selftest ok (13 checks, 0 failed)`. Footer pasted FROM the file.
11. DOCS-CHECK `180/180 clean under game-design/`, this record LOG and dated,
    em-dash 0, italic 0.
12. QUEUES 254, 256, 267, 268, 269 amended and 270, 271 filed; the NOW.md block
    pasted. 268 was also RENAMED because its old title asserted something this
    batch made false.
13. AFTER THE PUSH, both runs matched BY ANCESTRY on
    `dc04da736cbdbd3fffc119d1ff47801ec7706204`. `publish-glance` run
    34737101663 served all four pages at 200 with the commit's own stamp, and
    one of 158 pictures whole at its expected bytes; the detail is 269's
    closing line and 256's step 1. THE ONE THING NOT VERIFIED BY THE RESIDENT
    is done-line 3's bar: this container's proxy refuses `jsab258.github.io`
    with `CONNECT tunnel failed, response 403`, tried twice, so CI opened the
    artifact and the resident did not. Named, not glossed.
    `citypack-inventory` run 34737101660 COMMITTED, `c022c872`, 4003 insertions
    and 3964 deletions in the ambientCG catalogue; the next push was rejected
    non-fast-forward exactly as ruled, and `git pull --rebase origin main`
    preceded it.
14. RULE 8 AND RULE 13: the watcher was armed in the same turn as the push and
    fired at 04:13Z, which is how these numbers were read. THE RESUME AFTER IT
    IS A STOP, not a queue item: at 04:16Z the Producer died on `HTTP 429,
    "You've reached your Fable limit"`, so budget.md rule 1 fires. Queue 272
    carries the deadlock it exposed, that rule 1's required action needs the
    Producer and the Producer is the spent meter.
15. THE PC: nothing expected and nothing arrived. `pc-results` unmoved since
    2026-09-11 08:18, supervisor status still naming `70e9ac5`. 266 and 267
    stay open on their PC conditions. The 2026-09-13 brief was NOT written, for
    the reason in condition 14, and that is recorded as a finding in
    production/NOW.md rather than left to look like a quiet day.


Filled by the resident, one line per condition, with the numbers.

## 11. Dictated block for `production/NOW.md`, resident to paste at the top

    ## 2026-09-13 HH:MMZ: SIX TRIGGERS COME HOME, THE CEILING HAS ONE HOME, THE NINETY ROWS SAY WHAT THEY ARE

    The second half of the day's batch lands under
    game-design/decision-2026-09-13-ruling-the-triggers-and-the-ceilings-home-batch.md.
    269: publish-glance, citypack-inventory and citypack-fetch push on main
    with their filters; ledger-build-mac, props-fetch and voice-candidates
    are dispatch-only, each with its reason in its own YAML (voice-candidates
    could trigger itself, and its ten dead-branch sites moved in one edit so
    no push can create the old branch here). tools/workflow-branch-refs.py
    reads the repository's own branch list and fails verify on a name it
    does not have. 269 duplicated 254; both close on the served page reading
    85 after this push's publish-glance run, which is also 256's step 1;
    256's links are still 256. THIS PUSH ALSO FIRES citypack-inventory, and
    a drifted catalogue lands as one CI commit on main: pull with rebase
    before the next push. citypack-fetch is proven at mechanism level only
    and its target tree is legacy under D16. 268 is CLOSED: the ceiling
    pattern lives in tools/budget-ceiling.py, three importers, and
    tools/budget-ceiling-check.py fails verify on zero lines, two lines, or
    prose that disagrees (proseAt=44/46/117 today, the quotation at 46
    counted on purpose). 267 points 3 and 4 landed: the ninety container
    rows carry source=selftest-fixture, recognised by shape and span and
    never by a missing key, because a reading he typed before 0e522c1f
    lacks ceilingFrom= too; the PC copy is marked by the same tool when the
    runner returns and closes 267. The marker's selftest runs in verify
    (checks 83 to 84). New: 270 (tools_tracked cannot see a tool only
    verify.py runs) and 271 (the branch check skips git continuation lines).
    266 unchanged: open on the first PC row carrying ceilingFrom=.
