<!--RULING spawn=2026-09-13T02:39:43Z-->
# LOG: ruling on the 266/267 batch (the bot reads its ceiling, the selftest stops writing his log), and the order of 267's remainder, 268 and 269, 2026-09-13

> **STATUS: LOG, 2026-09-13. NOT CURRENT** once section 11 carries the
> printed numbers. Decision record, binding on the resident, on the builders
> briefed from sections 7 and 8, and on whoever next edits `tools/glance.py`
> or `production/budget.md`'s ceiling paragraphs.

Author: tier-1 director spawned 2026-09-13T02:39:43Z, row 562 of
`.claude/agent-log.tsv`, read this session; the row reads
`2026-09-13T02:39:43Z` TAB `studio-director` TAB `fable` TAB `default` TAB
`a10dfbe91eeeaaa93`. It is the only `studio-director` row dated 2026-09-13;
the two rows before it (560 and 561, 02:14:08Z and 02:33:08Z) are the
instrument-builder that wrote the batch, one spawn resumed once. A resident
never stamps a ruling; if the gate reports this stamp unmatched or stale, the
numbers go into section 11 and the stamp is not touched.

## 0. What was read, what was not run, and which version of the file

No shell in this seat: read, grep and glob only. I could not run `git diff`,
so the file reviewed is `tools/runner/telegram-bot.py` AS IT SITS IN THE
WORKING TREE, and every number below that I did not read out of the code is
the resident's print from this session, cited as such. Section 10 makes the
resident print them again from the file as staged.

**The version reviewed is the SETTLED one (02:40:25), not the one the brief
described.** The resident said mid-review that a final write was in flight
when I was briefed. The file I read is the later one, and the proof is in
what I read rather than in a timestamp: the denominator in
`ceiling_from_text` is `len(text.splitlines())` at line 573 with the 587
against 588 comment beside it; the rejecting case at 2229 to 2231 asserts
`line(s) 1/3 of 3 examined`; the provenance sentence sits in
`budget_reading` at 678 to 679. All three are the settled state. The batch
is 592 changed lines by the resident's count; nothing in this ruling rests
on the count.

Read whole: CLAUDE.md, `.claude/rules/instruments.md`, `.claude/rules/ci.md`,
`ledger-v2/studio-v2/organization.md`, queues 266, 267, 268, 269,
`production/budget.md`, `production/NOW.md` lines 1 to 260,
`production/wakes/2026-09-13T0400Z-86b37ffe.wake.txt`, the 2026-09-11
link-floor ruling. Read in the bot: lines 1 to 700 (the docstring, the
constants, `load_glance`, `ceiling_from_text`, `read_ceiling`,
`ceiling_refusal`, `budget_reading`), 700 to 1260 (`budget_log_path`,
`budget_log_lines`, `log_budget`, `Bot.__init__`), 1272 to 1362 (the
handler's budget path), 1633 to 1668 (the done line), 2060 to 2310 (the
arithmetic cases, the document cases), 2338 to 2355 (the fixture tree's
budget document), 2400 to 2510 (b4, b4c, b4b), 3457 to 3530 (the suite's last
case and `selftest`). Read in `tools/glance.py`: 1 to 1054 and the grep of
its top-level statements. Grepped repo-wide for every new name (rule 6) and
for the sentence `standing 80` (rule 1).

**Premise check.** A process ruling about the channel to Jafar and the
budget instrument. Nothing here touches Meridian, the era, the moat or the
visual bar; section 0 of CLAUDE.md is unchanged.

## 1. The batch as read, against what the two items asked

**266, all four done-lines met by the code as read.** (1) The ceiling is read
out of `production/budget.md` at the instant of each verdict, through
`glance.CEILING` and `glance.BUDGET` imported by path (`load_glance` 501 to
542, `read_ceiling` 595 to 629), and `CEILING_PCT` is gone: the repo-wide grep
finds the token only in the bot's own comment naming its death, in the two
queue items, in NOW.md and in the wake record. (2) Both outcomes, accepting
first: `accept/ceiling-is-read-from-the-live-document` reads the live file
(the resident's print: `ceilingPct=85
ceilingFrom=production/budget.md:49..the-standing-line`, which agrees with
my read of budget.md, where line 49 is the only line the pattern can match;
line 55 quotes the regex source and cannot match itself); the rejecting
fixtures are synthetic and refuse OUT LOUD with `nothing-measured` and a
reason that carries its denominator. There is no number to fall back to:
`budget_reading` takes `ceiling` with no default (647), and the handler
refuses and records nothing when `read_ceiling` returns None (1326 to
1335). (3) The four arithmetic cases pass `ceiling=ARITH_CEILING` (2100 to
2113) and the rung `accept/the-ceiling-argument-is-what-moves-the-verdict`
(2123 to 2126) proves the argument is wired: the same meters give
`headroomPct=18` at 80 and `headroomPct=8` at 70. (4)
`accept/ceiling-is-the-standing-85` (2161 to 2165) holds the document
against the pin.

**The builder caught its own instrument, and that is the part of this
batch to keep in mind when the next refusal is written.** The refusal's
denominator was `text.count("\n") + 1`, which says 588 for a 587-line file
and "of 4 examined" for a three-line fixture: a denominator one larger than
the set examined, rule 3b's false claim with a number on it, sitting inside
the fix for a silent instrument. It is `len(text.splitlines())` now (573),
the reason is written beside it, and two rejecting cases pin the printed
count to the fixture's real length (`2 line(s) were examined` at 2221,
`of 3 examined` at 2231). That is the standard: a refusal whose own number
is wrong by one is not a refusal that can be trusted.

**267, done-lines 1 and 2 met; 3 and 4 NOT done, and the batch must not
claim them.** (1) `log_budget(line, repo=None)` (771 to 799) takes its tree
from the caller, the handler passes `self.repo` (1339), and the grep finds no
other call site. (2) Both outcomes: `accept/a-reading-appends-exactly-one-line-to-the-log`
(2447 to 2450) proves a genuine reading through the real handler appends one
line, in the fixture tree; `reject/the-suite-writes-no-line-to-the-live-budget-log`
(3486 to 3491) holds the live count across the whole suite, and it is the
LAST case so its denominator is every case before it, with
`accept/the-suite-still-wrote-its-rows-somewhere` beside it so a guard that
stopped all writing cannot pass as a redirect. The resident's print, twice
on the settled file: `151 passed, 0 failed`, `liveBudgetLogLines=90..90`.
(3) Marking the ninety existing rows: nothing in the tree does it;
`source=selftest` appears nowhere under `tools/`. (4) The log printing its
own denominator on read-back: nothing reads the log back except
`budget_log_lines`, which counts rows and cannot tell a reading from a
fixture. Both go to section 7.

**The handler judged a fixture reading against the fixture document's 71**
(`FIXTURE_CEILING` at 2341, written into the throwaway tree's
`production/budget.md` at 2343 to 2347, asserted at 2467 to 2474 with
`ceilingFrom=production/budget.md:2..the-standing-line`). 71 is in no copy
of anything else, which is what makes that case evidence that the number
travelled from a document rather than from the file.

**The one red verify at 02:37 is accepted as a moving tree, not a defect**:
`inspect.getsource` read a file mid-write, which is the ruler's fault (rule
3), and the builder's second row at 02:33:08Z is the write that was in
progress. Two clean runs followed on the settled file. Section 10 requires
one more, because section 6 changes the file again.

## 2. The four questions

**Q1, `STANDING_CEILING_PCT = 85`: SOUND, LANDS. Not the fault in a quieter
form, and here is the test that separates them.** The fault was a number the
VERDICT computed with, whose staleness failed SILENTLY in the direction that
stops the studio. The pin is a number NOTHING computes with, whose staleness
fails LOUDLY (a red case in a suite verify runs) while the phone stays right,
because the phone reads the document. Those are opposite failure directions,
and the pin is what queue 266's done-line 4 asked for: a case that asserts
the standing number has to hold it somewhere. What keeps a future reader from
turning it into a fallback is not the comment (comments decay) but three
rejecting cases that go red the moment any code path computes with it:
`reject/no-ceiling-no-verdict-and-nothing-recorded` (a handler with no
document must record nothing and say "I cannot read the ceiling"),
`reject/ceiling-no-document-at-all` and
`reject/ceiling-prose-alone-is-not-machine-readable`. A fallback cannot pass
those. The residual is the NAME, which reads like a setting, and the next
rung is named in section 9 and folded into 268 rather than taken here.

**Q2, importing `tools/glance.py` into the bot: WORTH IT TODAY, and the
pattern moves in 268, not in this batch.** The coupling buys one
implementation of "where the ceiling lives", which is the whole lesson of
1aedef87. What I checked, because a page generator imported into the channel
on his PC is the thing to be afraid of: glance.py executes only definitions
at import (its single top-level call sits under `if __name__ ==
"__main__":` at line 2184; no `load_*` is called at module level, unlike
`tools/map.py:235` and `tools/gallery.py:111`, which do); it imports only
the standard library at module level and Pillow lazily inside
`encode_image`; the import is from the bot's own repository and never from a
caller's `repo` (525), which is glance's own rule in reverse; and a failed
import is a refusal, not a crash (533 to 537). The failure that remains is a
bad edit to glance.py turning every reading on his phone into a refusal, and
that is caught on the container before the PC pulls it: the bot's suite
calls `read_ceiling()` on the live tree, so a glance that cannot import goes
red in verify. The remaining cost is that a 2,200-line page generator is now
imported by four things for one regex, and that is the point at which a
shared module pays for itself; for the PC it also shrinks the channel's
coupling surface from 2,200 lines to a few dozen. Ruled for 268 in section
7: 268 is the THIRD reader, and it lifts the pattern rather than importing
glance a third time. The glance side of the coupling is unrecorded today (0
mentions of the bot in glance.py); section 6 dictates the note.

**Q3, the two readers differ on purpose: CORRECT, and recorded on one side
only, with the document CONTRADICTING it in the present tense.** The bot
reads the standing line and ignores a row's per-session sentence. That is
right under the 2026-09-10 ruling, which budget.md states at 109 to 115:
"IT IS NOT PER SESSION. Earlier ceilings were given with a reading and
expired with it." A number Jafar is typing now is ruled by no old row, and
the bot cannot know whether the newest row's session is the current one;
the standing line has no such ambiguity. Glance prefers the row because its
bar is drawn OVER that row, and six rows dated before the 10th still carry
the wording. So the difference is a difference in what is being judged, not
a disagreement about the ceiling, and both readers give 85 on today's file.
It is recorded well on the bot's side: the `read_ceiling` docstring (600 to
609) and two cases, `reject/ceiling-a-per-session-row-is-not-standing` and
`accept/ceiling-a-row-ruling-does-not-override-the-standing-line`, so a
reader who "fixes" the bot to prefer the row goes red. It is NOT recorded on
glance's side, whose comment at 654 to 660 tells the opposite story ("a bar
drawn against a ceiling he retired is a false reading") and will send the
next reader straight at the bot. And `production/budget.md` lines 125 to 140
still instruct the retired regime in the present tense: "his number wins
over the standing 80 above" (127) and "the page draws his bar against the
standing 80" (132 to 133). Those two are also live copies of the repealed
number that the 03:00Z sentence-sweep missed (rule 1: the sentence, not the
site). Section 6 dictates both fixes. If he ever sets a session ceiling
again, that is a decision to take then (the bot's verdict says which number
it used, and the resident applies the row); the document now says so rather
than instructing a regime that no longer exists.

**Q4, what the diff does that the items did not ask.** Kept, one with a
condition, and the three the builder flagged are ruled in section 2b. (a)
`ceilingFrom=` on the log line and `budgetCeilingUnreadable=N/M-pairs` on
the done line: instruments.md, every zero with its denominator, every number
with its provenance; the log's ninety rows are the proof of why. Kept. (b)
The top docstring rewrite. Kept. (c) `accept/the-prose-and-the-machine-line-agree`
(2174 to 2189), a THIRD regex over budget.md, matching `the (standing)
ceiling is N on the higher meter` and holding its set against the machine
line. It is exactly queue 268's done-line 2, pre-empted inside the bot's
selftest. Kept for now because it is loud, cheap and correct on today's
file (my read: lines 44 and 109 match and both say 85; line 117 does not
match because of its ellipsis), with the condition that 268 OWNS this idea:
when 268's guard lands, this case is retired from the bot's suite in the
same change, so one idea has one implementation. Nothing else in the diff
falls outside the two items.

## 2b. The three calls the builder flagged, ruled

**(1) The provenance line on his phone: KEPT.** "That ceiling was read from
production/budget.md just now and is not a number I carry." Three reasons,
against the one cost. First, the read-back is the sentence that decides
whether the studio stops, and on 2026-09-11 a verdict with no source was
believed for a session; a verdict that names its source can be checked by
the person reading it in the time it takes to read it, which is the only
check that runs on his phone. Second, the register question does not arise:
the bot's own chrome is deliberately outside `tools/producer-check.py` (the
docstring at 85 to 88, ruled 2026-09-05), and this is chrome on a
measurement read-back, not Producer content; the Producer owns judgement
messages, not the bot's receipt of a number. Third, the line prints only
when a source exists (`if ceiling_from`, 679), so the arithmetic fixtures
carry no false provenance. The cost is real and acknowledged: three lines
became four on a phone. The wording is plain and it stays. If Jafar finds
it noise, it is one line to remove and that is his call, not a builder's.

**(2) Two agreeing `Ceiling for LEDGER` lines are ANSWERED, not refused:
UPHELD as a deliberate departure from queue 268's point 1, and recorded as
one.** The bot's job is the verdict on a number he just typed; refusing him
that verdict over a duplicate that agrees with itself is a refusal in the
wrong direction, and it would put a document-tidiness fault on his phone as
"I cannot read the ceiling". Disagreement is refused, with both line
numbers, because there the answer is genuinely unknown. Two agreeing lines
are still VISIBLE: `ceilingFrom` carries every hit (`49/120..the-standing-line`),
so the log and the console show the duplicate without denying the verdict.
"Exactly one" is the DOCUMENT's rule and belongs to the document's guard,
which is what 268 becomes in section 7; the guard failing turns verify red
without taking a verdict away from him. 268's builder must not "align" the
bot to the guard's strictness, and the record says so twice on purpose.

**(3) Queue 268's premise is partly false and the builder proved it:
REWRITE, DO NOT CLOSE.** True as stated: `accept/ceiling-is-read-from-the-live-document`
reads the live `production/budget.md`, the suite runs inside
`ledger/verify.py`, so deleting the machine-readable line now fails the
commit gate rather than the console alone, and the prose cross-check does
the same for a header that disagrees with the line. Most of 268's four
done-lines are met by this batch. It is not closed outright, for one reason
that is not bookkeeping: a guard that lives in another tool's selftest is a
guard nobody knows to distrust, and "268 was closed because the bot's tests
happen to cover it" is the sentence the next reader will find when the bot
is retired or its suite is skipped. So 268 keeps its number and is rewritten
to what remains, all of which is real and small: the pattern's shared home
(section 2 Q2), the document-level exactly-one check that the bot rightly
does not make (2b 2), the prose cross-check moving out of the bot's suite
into the guard so it has one implementation (Q4 c), and the pin's move out
of the module namespace (Q1). Section 7 has the text.

## 3. Findings the brief did not have

**F1, blocking, one dictated sentence.** `ceiling_refusal` ends "Fix the
line in production/budget.md and send the two numbers again." But the
handler clears `pending` at 1318 BEFORE it reads the ceiling, and a bare
number reaches `parse_reading` only while `pending` is set (1289). So the
two numbers he sends again are filed as prose with the tail "Commands:
/budget, /ping, /help." and never read. The instruction on his phone is
wrong on the one path this batch exists for. Fix: the sentence names
`/budget`. Not the alternative of re-opening `pending`, which would be a
state change with no case asserting it. Section 6 (a).

**F2, document, not the builder's.** budget.md 127 and 133, above.

**F3, document, not this batch.** `tools/runner/README.md` line 77 to 78
still says the bot asks "with numeric quick-replies"; the grid was retired
2026-09-05 (queue 104). One-line fix on the resident's read, not a condition
of this landing.

**F4, scope.** 267 closes on none of this; see section 7.

## 4. Verdict

**THE BATCH LANDS WITH NAMED CHANGES**, all three hand-applied by the
resident from the dictated text in section 6, none of them a builder round:
(a) one sentence and its comment in `ceiling_refusal`; (b) one comment
block in `tools/glance.py` beside `CEILING`; (c) one paragraph and two
phrases in `production/budget.md`. No threshold moved, no instrument
weakened, no fallback number anywhere in the bot. The selftest count may
stay at 151 (no case is added); what changes is the refusal string, and the
b4c assertions do not read that sentence, so a red after the edit is a
finding and not an expectation.

## 5. What is landed and what is closed, which are different facts

**266: LANDED, NOT CLOSED.** Rule 6. The bot on his PC started at
01:14:15Z from a checkout that carries `CEILING_PCT = 80`, and nothing in
this repository reaches that process; `ledger-restart-telegram-bot.yml` is
the mechanism and it dispatches to `ledger-pc`, which is off. 266 closes on
the first row in `production/logs/telegram-budget.log` ON HIS PC that
carries `ceilingFrom=production/budget.md`, which can only be written by a
bot running this commit or later. Until then his phone's verdict is against
80, in the direction that stops work, and the 2026-09-13 brief carries that
as the wake record already orders. The resident writes the LANDED line and
the closing condition into 266 rather than changing its status to done.

**267: LANDED ON POINTS 1 AND 2, OPEN ON 3 AND 4.** Section 7 carries the
remainder to a builder.

## 6. Dictated text, resident to apply before the commit

**(a) `tools/runner/telegram-bot.py`, `ceiling_refusal`, the last two
string lines (642 to 643 as read).** Replace

    "Nothing was recorded. Fix the line in production/budget.md and "
    "send the two numbers again."

with

    "Nothing was recorded. Fix the line in production/budget.md, then "
    "send /budget and the two numbers again."

and add, directly above the `return (` of that function, this comment:

    # `/budget` IS NAMED BECAUSE `pending` IS ALREADY CLEARED by the time this
    # is sent (the handler closes the question before it reads the ceiling),
    # so a bare number typed after this refusal is filed as prose, not read.

**(b) `tools/glance.py`, directly above `CEILING = re.compile(...)` at
line 653 as read, one comment block:**

    # THIS PATTERN HAS A SECOND READER, AND IT DIFFERS FROM THIS FILE ON
    # PURPOSE. tools/runner/telegram-bot.py imports CEILING and BUDGET by
    # path (queue 266) to judge a reading Jafar has just typed, and it reads
    # the STANDING line only: the per-session sentence in a row's note, which
    # this file prefers below for the bar it draws over THAT row, expired
    # with the reading it came with (production/budget.md, the 2026-09-10
    # ruling), and no old row rules a number typed now. Do not make either
    # reader match the other; the bot's selftest holds the difference
    # (reject/ceiling-a-per-session-row-is-not-standing). Renaming or moving
    # CEILING or BUDGET turns every reading on his phone into a refusal.
    # Ruled 2026-09-13, decision-2026-09-13-ruling-the-ceiling-is-read-not-carried-batch.md.

**(c) `production/budget.md`.** Insert, as its own paragraph directly above
"HOW TO WRITE A PER-SESSION CEILING SO A MACHINE READS IT" (line 125 as
read):

    THE PARAGRAPH BELOW DESCRIBES THE PER-SESSION REGIME THAT THE 2026-09-10
    RULING RETIRED. It is kept because six rows above still carry that wording
    and `tools/glance.py` still honours it for the bar it draws over those
    rows. Two readers now take a ceiling from this file and they differ on
    purpose, ruled 2026-09-13: glance prefers the selected row's own sentence,
    because its bar is drawn over that row; the Telegram bot
    (`tools/runner/telegram-bot.py`, `read_ceiling`) reads the `Ceiling for
    LEDGER:` line above and nothing else, because a number Jafar is typing now
    is ruled by no old row. If he ever sets a ceiling for one session again,
    the bot's verdict on his phone is still against the standing line and its
    text says so; the session number is applied by the resident from the row,
    and whether the bot should read it is a decision to take then, not a fix
    to make quietly.

Then, in the paragraph that follows, change "his number wins over the
standing 80 above" to "his number wins over the standing line above", and
"the page draws his bar against the standing 80" to "the page draws his bar
against the standing line". Line 136's "the page printed 80 against his 75"
is history and stays.

## 7. Queue amendments, resident to apply

**266.** Under STATUS, one line: `LANDED <sha> 2026-09-13; CLOSES on the
first row in production/logs/telegram-budget.log on the PC carrying
ceilingFrom=production/budget.md, which needs the bot restarted on this
commit or later (ledger-restart-telegram-bot.yml, waiting on ledger-pc).`

**267.** Under STATUS: `POINTS 1 AND 2 LANDED <sha> 2026-09-13; 3 AND 4
OPEN, ride with 268's builder.` And one clarification to point 3, because
the container holds the same ninety rows the PC does (thirty verify runs
wrote them here): the marking tool's accepting case is THIS container's
copy, run once and its before/after counts printed; the PC copy is marked
by the same tool when the runner returns, and that run is the second
accepting case, not the first.

**268, REWRITTEN, not closed (section 2b 3).** Its opening states what
this batch already covers and where: deleting the machine line or letting
the header disagree with it now fails `ledger/verify.py` through the bot's
suite (`accept/ceiling-is-read-from-the-live-document`,
`accept/the-prose-and-the-machine-line-agree`), which is a guard that lives
in another tool's tests and is therefore the thing to move, not the thing
to rely on. What 268 now delivers, in one builder pass: (i) THE PATTERN'S
HOME. One small standard-library-only module under `tools/`, name the
builder's, carrying `BUDGET`, `CEILING`, `ROW_CEILING` and the
standing-line reader (the bot's `ceiling_from_text`, moved, with its
`(pct, from, why)` contract and its refusal on disagreement intact).
Glance, the bot and the guard import it; `load_glance` in the bot becomes
the import of that module by the same by-path mechanism, so the channel on
his PC depends on a few dozen lines rather than on a page generator;
glance's `read_budget` keeps its row preference and calls the shared reader
for the standing half. (ii) THE DOCUMENT GUARD, where the other document
checks run: exactly one machine line (zero and two both fail, each named),
the prose agreeing with it, tested both ways with the live file as the
accepting case and three synthetic fixtures (deleted, duplicated,
disagreeing) as the rejecting ones, failure naming the remedy. The bot's
`accept/the-prose-and-the-machine-line-agree` is retired in the same
change, so the cross-check has one implementation. (iii) THE PIN MOVES:
`STANDING_CEILING_PCT` leaves the module namespace and becomes the literal
inside the selftest case that reads it, case name and message unchanged,
so the top comment's "no number in this file" is true at module level.
(iv) ONE THING THE BUILDER MUST NOT ALIGN: the bot ANSWERS when two
matching lines agree and refuses only on disagreement; the guard fails on
any duplicate. The bot's leniency is right for the channel and the guard's
strictness is right for the document, ruled in section 2b 2, and a case in
the bot's suite keeps proving the lenient half.

**269, one narrowing under CLAUDE.md rule 9.** Done-line 1 says all six
trigger on `main`. Not blanket: `publish-glance.yml` re-points to `main`
with its path filter, because it is cheap and Jafar-facing. For each of the
other five (`citypack-fetch`, `citypack-inventory`, `ledger-build-mac`,
`props-fetch`, `voice-candidates`) the builder reads what the job costs and
decides, per workflow and in writing in the YAML comment, between
re-pointing the push trigger to `main` and DELETING the dead push trigger
to leave `workflow_dispatch` only; an expensive job does not become
push-triggered on `main` by a find-and-replace. `voice-candidates.yml`'s
checkout `ref` and the fetch and rebase at 69, 84 and 85 move with whatever
is decided, as the item already says. Done-line 2's proof by a run applies
to every workflow that keeps or gains a push trigger; a workflow that
becomes dispatch-only is proven by done-line 4's check and by one dispatch
only if it is cheap. Done-line 3 stands: the page is opened and the bar
reads 85.

## 8. The order of what is left, and how it is dispatched

One dispatch cycle, two builders, ONE director review, because the budget
is the binding constraint (his last reading, 78 total and 82 Fable against
85, and directors run on Fable) and a batch is all builder work landing in
one reviewed commit:

1. **269 first**, to a builder who works in YAML and proves by runs. Rule
   12: his console is a blocked feedback channel, and a guard against a
   repaired fault (268) does not outrank a channel that has not rebuilt
   since the move.
2. **268 plus 267's remainder**, to one instrument-builder in the same
   cycle: the shared module and the guard (section 7), the marking tool for
   the ninety rows, and the read-back that prints
   `rows=N readings=A fixtures=B unmarked=C`, all with selftests both ways,
   accepting case first.
3. Both land in one reviewed commit under the next director spawn; a red
   fix never waits for the batch.

The running PC bot is not on this list because nothing here can reach it;
it is the brief's job to tell him and the runner's job to restart it.

## 9. Quality ladder at close

Best available for the channel's verdict: the number is read at the instant
it is used, from the document of record, through the one pattern that owns
it, with its provenance on his phone and in the log, a refusal that keeps
his numbers visible, and a refusal whose own denominator is right. Rungs
above it, named and all in 268: the shared module, the document guard with
one implementation of the prose cross-check, the pin out of the namespace;
and in 267: the log that can say how many of its rows are real. The blank
rung is what the bot should do if a per-session ceiling ever returns
(section 2 Q3), which is a decision for the day it happens and is recorded
in the document as such rather than designed for now.

## 10. Conditions the resident prints before the commit, and after the push

1. The three edits of section 6 applied; `git diff --stat` unstaged EMPTY
   for `tools/runner/telegram-bot.py`, `tools/glance.py` and
   `production/budget.md`, so the tested files and the staged files are one.
2. `python3 tools/runner/telegram-bot.py --selftest` on the staged file,
   pasted whole: cases passed and failed, `liveBudgetLogLines=90..90
   beforeSuite..afterSuite state=present..present`, the `ceiling:` line
   reading `ceilingPct=85 ceilingFrom=production/budget.md:49..the-standing-line`,
   the two rung lines (`headroomPct=18` at 80 and `headroomPct=8` at 70),
   the fixture log row carrying `ceilingPct=71` and
   `ceilingFrom=production/budget.md:2..the-standing-line`, the two
   `refuses:` lines carrying `2 line(s) were examined` and `of 3 examined`,
   and the printed `refuses:` line for b4c showing the NEW sentence with
   `/budget` in it.
3. `python3 tools/glance.py --selftest` green after the comment, and one
   live run's ceiling line, `ceilingPct=85 ceilingFrom=the-standing-line..`.
4. `grep -rn "standing 80" production/ tools/` pasted with its count; every
   remaining hit is a dated history line and is named as such, or it is
   fixed.
5. `python3 ledger/verify.py` green, footer pasted FROM
   `ledger/.verify-footer`, and the cadence pairing sentence naming ONE
   ruling record paired to a director row newer than the reference, which
   is this stamp; the line reads REVIEWED and no longer `DIRECTOR RAN BUT
   DID NOT RULE`.
6. `python3 tools/docs-check.py`: this record LOG, dated, em-dash count 0.
7. Queue 266, 267, 268, 269 amended as section 7; NOW.md block from
   section 12 pasted at the top.
8. After the push: nothing is expected from the PC (the runner is off);
   the resident records that the PC has not restarted the bot and that 266
   stays open on the section 5 condition.
9. Rule 13: 269's builder and 268's builder briefed from sections 7 and 8
   and dispatched before this session ends, or the resume armed for them.

## 11. Landing

Filled by the resident 2026-09-13 03:0xZ, one line per condition.

1. THREE EDITS APPLIED. `git diff --stat` over the three files:
   `production/budget.md` 37 changed, `tools/glance.py` 11, and
   `tools/runner/telegram-bot.py` 595 at that moment (616 after condition 2's
   fix below). Nothing left unstaged at commit: the tested files and the
   committed files are one tree.
2. BOT SELFTEST `151 passed, 0 failed (151 case(s) run)`, exit 0, and every
   line the condition names:
       liveBudgetLogLines=90..90 beforeSuite..afterSuite state=present..present
       ceiling: ceilingPct=85 ceilingFrom=production/budget.md:49..the-standing-line
       rung ceiling=80: ... ceilingPct=80 ... headroomPct=18
       rung ceiling=70: ... ceilingPct=70 ... headroomPct=8
       fixture log row: ... ceilingPct=71 ceilingFrom=production/budget.md:2..the-standing-line headroomPct=9
       refuses: ... and 2 line(s) were examined looking for it.
       refuses: ... on line(s) 1/3 of 3 examined ...
   THE b4c LINE NEEDED A FOURTH EDIT TO SATISFY THIS CONDITION, and it is
   recorded rather than done quietly. The print at 2501 was `[:200]` with no
   announcement, and the sentence it exists to show ends in `/budget` at
   character 362, so the one word the condition asks for was the word the cap
   ate, silently, against instruments.md. The bound is 700 now and it
   announces itself if it ever bites. The line prints whole and ends:
   "Nothing was recorded. Fix the line in production/budget.md, then send
   /budget and the two numbers again."
3. GLANCE `glance selftest: 80 check(s) run, 0 failed` after the comment, and
   one live run: `ceilingPct=85 ceilingFrom=the-standing-line..2026-09-11
   ceilingStandingPct=85`.
4. `grep -rn "standing 80" production/ tools/` COUNT 7, and all 7 examined
   and named: `budget.md` 36, 38, 39 are dated 2026-09-08 and 2026-09-09
   table rows recording a per-session ceiling set at the time;
   `brief-input/2026-09-09.md:132` and `findings.txt:2287` are the same dated
   passage about that morning's `read_budget` work; `glance.py:670` quotes a
   historical row inside a comment; `glance.py:1623` is `FIXTURE_CEILING_RULED`,
   a verbatim quote of Jafar's 2026-09-08 row used as the pattern's ACCEPTING
   fixture, which would break the test if edited. ZERO live claims remain; the
   two the sweep of 2026-09-11 missed, at 127 and 133, are fixed by 6(c).
5. VERIFY GREEN, `checks=81ran/0skipped/81total`, and the cadence line reads
   what this record exists to produce: `director cadence ok (616 changed
   line(s) ... over threshold, REVIEWED; 1 director row(s) newer than the
   reference ...; rulingRecords=1/82 ... 1 ruling record(s) paired to a
   director row newer than the reference`. It no longer reads DIRECTOR RAN
   BUT DID NOT RULE. Footer pasted into the commit FROM `ledger/.verify-footer`.
6. DOCS-CHECK `179/179 clean under game-design/`, this record among them,
   banner LOG and dated, em-dash count 0, italic count 0.
7. QUEUE 266, 267, 268, 269 AMENDED per section 7, and the NOW.md block from
   section 12 pasted at the top. 268 was also RENAMED to
   `268-the-duplicate-ceiling-line-is-the-half-nothing-owns.md`, because its
   old title asserted something this batch made false; every reference to it
   is by number, so nothing broke.
8. AFTER THE PUSH, nothing is expected from the PC. `pc-results` has not moved
   since 2026-09-11 08:18 and `production/pc-ops/supervisor-status.txt` still
   names `70e9ac5`. The bot started at 2026-09-13T01:14:15Z and asked for a
   budget reading, so until it is restarted on this commit his phone judges
   against 80. 266 stays open on the section 5 condition.
9. Rule 13: recorded below and in `production/wakes/2026-09-13T0400Z-86b37ffe.wake.txt`.

## 12. Dictated block for `production/NOW.md`, resident to paste at the top

    ## 2026-09-13 HH:MMZ: THE BOT READS ITS CEILING, 266 IS LANDED NOT CLOSED, AND THE ORDER IS 269 THEN 268

    The 266/267 batch lands under
    game-design/decision-2026-09-13-ruling-the-ceiling-is-read-not-carried-batch.md.
    The bot reads `Ceiling for LEDGER:` out of production/budget.md at each
    verdict through glance.py's own pattern, refuses out loud with his two
    numbers still in the chat when it cannot, names /budget in that refusal
    because the question is already closed by then, and the selftest writes
    nothing to the live log (90..90). 266 is LANDED and NOT CLOSED: it closes
    on the first row in production/logs/telegram-budget.log on his PC carrying
    ceilingFrom=production/budget.md, which needs the bot restarted on this
    commit or later; until then the bot on his phone judges against 80, and
    the daily brief says so. 267 landed points 1 and 2; 3 and 4 (mark the
    ninety rows, print the denominator on read-back) ride with 268's builder.
    268 is rewritten, not closed: the bot's suite now fails verify if the
    machine line goes, and what remains is the pattern's shared home, the
    document's exactly-one guard, and the pin out of the namespace. Two
    readers of budget.md differ on purpose and both files now say so: glance
    prefers a row's own sentence for the bar over that row, the bot reads the
    standing line for a number typed now. Next dispatch cycle, one review:
    269 (publish-glance re-pointed at main and proven by a run; the other
    five decided per workflow under rule 9) and 268 plus 267's remainder.
