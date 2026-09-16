#!/usr/bin/env python3
"""A PRODUCER MESSAGE, AGAINST THE RULED REGISTER, BEFORE IT REACHES JAFAR.

    python3 tools/producer-check.py MESSAGE.md          # unprompted, 120 words
    python3 tools/producer-check.py --kind brief FILE    # morning brief, 150
    python3 tools/producer-check.py --kind answer FILE   # he asked; length follows
    python3 tools/producer-check.py -                    # read stdin
    python3 tools/producer-check.py --selftest           # accepting case FIRST

WHY IT EXISTS. Jafar ruled on 2026-09-03 that the Producer is the only voice
that addresses him, and ruled its register. A register that lives only in an
agent file is a preference: the next session writes a 400 word message with
four file paths in it, nothing objects, and the rule quietly stops existing.
This is the half that objects.

WHAT IT CAN AND CANNOT SEE, said out loud rather than skipped, because a check
whose silence reads as a clean bill is the fault this project keeps paying
for. It is MECHANICAL. It counts words, matches tokens, and decides whether a
sentence has the SHAPE of a claim. It cannot tell whether a claim is TRUE,
whether the link behind it actually shows what the sentence says, or whether
the recommendation is any good. Those need the director. The report says so at
the bottom rather than implying the absence of a finding is approval.

THE LINK BAND, ruled by Jafar 2026-09-06 after a message with ten repository
links passed this check: ONE link at least (constitution law 12), TWO at most,
and the only destinations are the published pages named in SITE_PAGES. A
picture goes to him as a Telegram image, never as a link. Rules ruled after a
message was written do not apply to it, and the mechanism is a FROZEN LIST OF
NAMES (see LEGACY_LINK_RULES), never the date in a filename: the date at the
front of a name is typed by the writer, so a date switch lets the specimen
choose its own rulebook. The three already-sent messages are named; today's is
not.

THE FLOOR IS CONDITIONAL FROM 2026-09-11, and it is not deleted (see
SERVED_MARKER_REL). Ruled 2026-09-10, queue 256 and queue 259: while NO page
is served from the new repository, zero links is legal and `linkfloor` does
not fire, because all five permitted destinations sit under the ARCHIVE's
pages and a link sent today would show Jafar the world as it was before the
move. Once a page is served the floor is one to two again. The condition is a
committed marker naming the served commit, never a date and never a constant,
and every run PRINTS the branch it took: `linkFloorActive=<true|false>
reason=<...>` on the done line, with the effective floor beside the ruled band
in the body. A missing or malformed marker leaves the floor LIVE.

THE ONE RULED WHOLE-URL EXCEPTION, 2026-09-09 (see RULED_LINKS). Jafar asked
for one message carrying a link to research that no published page holds, which
his own band of 2026-09-06 forbids. A later, specific instruction from the
rule's own author governs its instance and repeals nothing, so exactly one URL
is admitted BY WHOLE STRING, the entry names the record that admits it, and the
rung that publishes the research DELETES the entry. Whole-string equality and
not a prefix is the whole difference between an exception and a hole: a prefix
match on a tree URL would admit every file under it, which is the repository.

THE READING ASK, RULED 2026-09-15 AND ENFORCED IN THE BRIEF REGISTER ONLY
(see READING_PARTS). A budget reading older than TEN HOURS means the day is
UNMEASURED, and the half that makes that cost Jafar nothing is that the brief
ASKS HIM FOR THE READING AS ITS FIRST LINE, every morning, with the studio at
inbox only until he answers. So a brief's first non-blank line must ask: a
question mark, the meter or the usage figure named, and NO option,
recommendation, default or deadline on it, because it is a LINE and not a
NEEDS YOU item and there is no default. A day he does not answer is a day the
studio does not spend. The 17 briefs written before the ruling are named on
PRE_READING_BRIEFS and waive exactly that rule, by name and never by the date
in the name.

THE REGISTERS. UNPROMPTED and BRIEF get the shape, the cap, the ban list and
the link floor. ANSWER gets the ban list and the link rules only, because
Jafar's question sets the length and a question asking for a number is
answered with the number. Every register PRINTS the rules it did not enforce,
by name: a skipped check that prints nothing is indistinguishable from a
passing one.

WHAT THE BRIEF REGISTER STOPPED REQUIRING ON 2026-09-09, and where the number
went. The BUDGET section and the studio-versus-game split are RETIRED FROM THE
BRIEF, because Jafar's director test of that morning forbids in the daily
message the unit and the vocabulary his own 2026-09-05 order requires of the
split, so no brief could pass both. The split is OWED BY THE SUNDAY SUMMARY,
which has no register in this file yet; the rule, its five-part detector and its
four rejecting fixtures are kept whole and tested, and every register prints
`split` under NOT ENFORCED. The reasoning, which ruling supersedes which, and
the four moves that re-attach the rule are at SECTIONS_RETIRED_IN_BRIEF.

EXIT CODES, distinct per outcome. 0 the message may be sent. 1 it may not, and
every finding is named. 2 there was no message to read (missing file, empty
stdin), which is not a pass. 3 the selftest failed. 4 tools/capsay.py could not
be imported: this program refuses to report a truncated finding list without
the one implementation of the truncation notice.
"""
import argparse
import datetime
import importlib.util
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent


def _load(path, name):
    try:
        spec = importlib.util.spec_from_file_location(name, str(path))
        if spec is None or spec.loader is None:
            return None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:                                            # noqa: BLE001
        return None


# ONE IMPLEMENTATION PER IDEA. The truncation notice already exists in this
# repo and is imported, never re-typed.
_capsay = _load(REPO / "tools" / "capsay.py", "capsay")
if _capsay is None:
    sys.stderr.write("producer-check: tools/capsay.py could not be imported; "
                     "refusing to print a finding list with no truncation "
                     "notice behind it\n")
    sys.exit(4)
cap, NOTHING = _capsay.cap, _capsay.NOTHING_MEASURED

FINDINGS_SHOWN = 3      # per rule. cap() announces when it bites.

# ---------------------------------------------------------------- the register

CAP_UNPROMPTED = 120
CAP_BRIEF = 150
MIN_DEADLINE_HOURS = 24
MIN_OPTIONS, MAX_OPTIONS = 2, 4

# EVERY SECTION LABEL THIS PARSER KNOWS, in the ruled order. Membership here is
# the parser's VOCABULARY and the order rule, not the required list: which of
# them a register DEMANDS is SECTIONS_REQUIRED below, because BUDGET is required
# in an unprompted message and retired from the brief.
SECTIONS = ["HEADLINE", "WHAT CHANGED", "NEEDS YOU", "NEXT VISIBLE THING",
            "BUDGET"]

# ------------- THE BUDGET SECTION AND THE STUDIO-VERSUS-GAME SPLIT, RETIRED
# ------------- FROM THE BRIEF REGISTER 2026-09-09. THE NUMBER MOVED; IT WAS
# ------------- NOT DROPPED, AND WHERE IT IS OWED IS NAMED BELOW.
#
# TWO OF JAFAR'S OWN RULINGS COLLIDED, and this block is the resolution.
#
#   2026-09-05, game-design/decision-2026-09-05-ruling-standing-order-refill-
#   and-the-wake-half.md, section 6: EVERY BRIEF reports the studio-versus-game
#   split, in words, COUNTED IN SESSIONS, and not points until the rate is
#   measured.
#
#   2026-09-09, game-design/decision-2026-09-09-the-regime-change-lands-three-
#   doors-the-sky-and-the-caption.md and production/NOW.md ruling 2: the Producer
#   applies THE DIRECTOR TEST to the daily message itself, in his words, "no
#   numbers with units, no coordinates, no file names, no studio vocabulary",
#   and the register "stays as a FORMAT CHECK AFTER the Producer writes, not as a
#   gate that shapes what is written".
#
# "Sessions" IS a number with a unit and "the studio versus the game" IS studio
# vocabulary, so NO BRIEF COULD SATISFY BOTH RULINGS AT ONCE. On 2026-09-09 this
# program refused the first message written under the new regime with exactly
# two findings, `shape: missing section(s): BUDGET` and `split`, on a message
# that obeyed the newer ruling as written.
#
# WHICH SUPERSEDES WHICH, AND WHY: the newer one, for the DAILY MESSAGE only.
# Same author, same channel, later instruction, and it is specifically about
# what that reader may be shown. What it replaces is the split's PLACE, not the
# number: the 2026-09-05 order is not withdrawn and has never been withdrawn.
#
# WHERE THE NUMBER IS OWED NOW: THE SUNDAY SUMMARY, which the same 2026-09-09
# ruling names as the place the studio reports to itself ("reports the notable
# ones in the Sunday summary"), where studio vocabulary and a count in sessions
# are appropriate because the audience is a studio report and not a man with a
# phone and twenty seconds.
#
# THERE IS NO SUNDAY OR WEEKLY REGISTER IN THIS FILE TODAY. REGISTERS below
# holds three kinds and KIND_SUFFIX three suffixes; the selftest asserts both
# counts so this sentence cannot rot into a false claim. WHOEVER BUILDS THAT
# REGISTER PICKS THE SPLIT UP, in four moves and no rebuilding: add the kind to
# REGISTERS with "split" in its enforced list, give it a SECTIONS_REQUIRED row
# that includes BUDGET, add its filename suffix to KIND_SUFFIX, and point the
# four BAD_BRIEF fixtures at it. The five-part detector is kept whole and is
# driven directly by the selftest on every run (see split_parts and SPLIT_PARTS),
# so it cannot rot while it waits.
SECTIONS_RETIRED_IN_BRIEF = ("BUDGET",)
# Printed wherever the retirement is mentioned. No spaces: it crosses key=value
# channels, and every reader of those splits on whitespace.
SPLIT_OWED_BY = "the-Sunday-summary/which-has-no-register-in-this-file-yet"
SPLIT_RETIRED_ON = datetime.date(2026, 9, 9)

# The rules, by name, so a register can say which of them it enforces and the
# report can print the ones it did not.
RULES = ["wordcap", "shape", "options", "deadline", "nextvisible",
         "banned", "linkfloor", "linkcap", "linkdest", "split", "reading",
         "filedline"]
# `split` IS ENFORCED IN NO REGISTER TODAY: retired from the brief by the ruling
# block above, and never applied to an unprompted message or an answer, which
# Jafar's 2026-09-05 order says nothing about. IT STAYS IN RULES ON PURPOSE, so
# every register NAMES it under NOT ENFORCED and the done line carries
# rulesEnforced=9/10 beside rulesNotEnforced=split. A retired rule deleted from
# this list would read exactly like a rule that passed, and the ruling would be
# lost rather than moved.
# `filedline` IS ENFORCED IN NO REGISTER EITHER, and it is here for the same
# reason rather than as a placeholder. Jafar ruled it 2026-09-16 after a
# two-part answer spent four paragraphs explaining items he had raised and the
# studio had already filed: "A filed item needs one line saying it is filed,
# not four paragraphs on its reasoning." NOTHING CHECKS THAT TODAY. Detecting
# "this sentence reports a filed item" is a phrase-list problem, and a phrase
# list is the weak link in every checker here that has one, so a bound was not
# invented to make the rule look enforced. It is NAMED at every run instead, so
# the next drift is visible in the done line rather than discovered by him.
RULES_NO_REGISTER = ("split", "filedline")
# ENFORCED IN THE BRIEF AND NOWHERE ELSE, ruled by Jafar 2026-09-15 (see
# READING_PARTS). The daily message is the one place he is asked for the meter;
# an unprompted message and an answer are not that place and would turn the
# one daily ask into a nag. Named in one constant so the register, the report
# and the selftest cannot come to disagree about which kinds it binds.
RULES_BRIEF_ONLY = ("reading",)
REGISTERS = {
    "unprompted": (CAP_UNPROMPTED,
                   [r for r in RULES if r not in RULES_NO_REGISTER
                    and r not in RULES_BRIEF_ONLY]),
    "brief": (CAP_BRIEF, [r for r in RULES if r not in RULES_NO_REGISTER]),
    # ANSWER: his question sets the length, so the cap and the shape are not
    # enforced and are NAMED as not enforced. The ban list and the link floor
    # still bind, minus counts: a question asking how many is answered with
    # how many.
    # THE TWO LINK RULES BIND IN EVERY REGISTER. Jafar ruled them of "a
    # message", not of a kind: "at most two links per message, and never to a
    # repo markdown file". A cap that an answer could escape is a cap the next
    # long answer escapes.
    "answer": (None, ["banned", "linkfloor", "linkcap", "linkdest"]),
}

# WHICH SECTIONS THE `shape` RULE DEMANDS, PER REGISTER. BUDGET is retired from
# the BRIEF and from nothing else: it is still a known label in every register,
# so a brief that carries a money line is parsed and order-checked exactly as
# before and the section is PERMITTED, just no longer required. The unprompted
# register is untouched and still requires all five.
SECTIONS_REQUIRED = {
    "unprompted": list(SECTIONS),
    "brief": [s for s in SECTIONS if s not in SECTIONS_RETIRED_IN_BRIEF],
    # The answer register does not enforce `shape` at all and names it under NOT
    # ENFORCED. The row exists so required_sections() never has to guess a kind.
    "answer": list(SECTIONS),
}


def required_sections(kind):
    """The sections `shape` demands in this register, in the ruled order."""
    return SECTIONS_REQUIRED.get(kind, list(SECTIONS))


# THE THREE MESSAGES WRITTEN BEFORE THE LINK BAND WAS RULED, BY NAME.
#
# Jafar ruled the band on 2026-09-06. Three messages were already written and
# sent under the register as it stood, whose destination rule was a host
# allowlist. Grading them against a rule that did not exist would turn them red
# in ledger/verify.py, delete the footer and block every commit until somebody
# edited a message that was correct when it was sent, which is queue item 077's
# failure one rule further on.
#
# WHY A NAME AND NOT A DATE, ruled 2026-09-06 after the first version of this
# used the ISO date at the front of the filename as the switch. THE GATE WOULD
# HAVE READ ITS RULEBOOK OFF THE SPECIMEN: that date is typed by the writer, so
# a file named 2026-09-05-x.unprompted.md written next week would be graded with
# no link cap and the retired host list. The defence offered for it ("changing a
# filename takes a reviewed diff") does not hold, because outbox messages commit
# on the resident's read under the narrowing of 2026-09-06. The same argument is
# already written down at PRE_REGISTER below, for the same reason.
#
# THIS TUPLE MAY NEVER GAIN A MEMBER WHOSE FILENAME DATE IS ON OR AFTER
# 2026-09-06, and it widens only in a reviewed diff. The selftest asserts the
# first half on every run.
#
# ONE LEADING `HISTORICAL,` LINE MAY SIT INSIDE THESE MESSAGES AND IS NOT
# CHARGED TO THE WORD CAP. This REVERSES what stood here until 2026-09-06 ("no
# marker line goes inside these messages"), and the ruling that reversed it is
# Jafar's, 2026-09-06: "Make older queued updates clearly historical so the
# initial backlog does not tell me that resolved problems are still current."
# Nothing has ever been sent from this outbox, so the first burst delivers
# every queued message at once and two of them describe problems that are now
# fixed. TWO is the live reading, not a typed constant: the gate prints it as
# historicalLinesUncounted=N/M on every run, and the outbox gained a message
# while this very change was being written, which is why no count of the
# OUTBOX appears in this comment. A reader who finds a marker line here must
# NOT delete it as a register violation: it is there under that ruling.
#
# WHY THE EXCLUSION IS DEFENSIBLE, AND WHY IT IS PINNED TO THIS LIST. The cap
# governs what the PRODUCER WROTE. A historical marker is an annotation the
# studio added afterwards, on top of a body that is the record of what was
# written and may not be trimmed: both bodies were written TO the cap, 118 and
# 119 words of 120 measured 2026-09-06, so any honest marker breaks it. That
# distinction is real and it is also exactly the kind of distinction that
# becomes a loophole the moment it is not pinned, so it is pinned to this
# frozen list and scoped three ways in historical_split(): the line must be
# FIRST in the file, must begin with the exact token, and only ONE is excused.
# It is excluded from the word count and from NOTHING ELSE: the ban list, the
# link rules and the shape rules all still read it. And it is never silent, on
# the file's own line and in the footer key historicalLinesUncounted=N/M, so
# nobody can read "118 of 120" without the line that is not in it.
LEGACY_LINK_RULES = (
    "production/outbox/2026-09-03-batch-landed-and-the-wait.unprompted.md",
    "production/outbox/2026-09-05-the-console-run.unprompted.md",
    "production/briefs/2026-09-05.md",
)

# DOCUMENTATION, AND IT SELECTS NO RULE. The band was ruled on this date; the
# only code that reads it is the selftest assertion that no name above is dated
# on or after it. Nothing in check() or gate() branches on a date.
LINK_BAND_RULED_ON = datetime.date(2026, 9, 6)

# ENFORCED IN EVERY REGISTER WHEN A NEEDS YOU SECTION IS PRESENT, ruled
# 2026-09-03. An answer has no cap and no required shape, but the moment it
# carries a decision it carries Jafar's floor with it: two to four options, a
# recommendation, a default, and a deadline no shorter than 24 hours. Without
# this a decision buried in a long answer escapes the default and the floor,
# which is the failure the decision queue exists to end.
RULES_IF_NEEDS_YOU = ["options", "deadline"]
# THE TWO RULES THE LINK BAND ADDED on 2026-09-06, named once so the legacy
# switch and the report cannot come to disagree about which rules it covers.
LINK_BAND_RULES = ("linkcap", "linkdest")

# ---------------------------------------------------------------------------
# THE MESSAGES THAT WERE ALREADY SENT WHEN THE SITE MOVED, 2026-09-15.
#
# WHAT HAPPENED, AND IT WAS MEASURED BEFORE IT WAS HANDLED rather than
# discovered by a red gate. Queue 256 moves `SITE_ORIGIN` off the archive and
# writes a served commit into `production/site-served.txt` in one commit. Both
# halves change what an ALREADY COMMITTED message is graded against, and this
# walk re-grades every message in the tree on every commit, so the two halves
# together turned a clean live walk into 40 failures out of 42 files checked.
#
# THE LADDER THAT SAID WHICH HALF DID WHAT. One live tree, one vantage, four
# rungs, all in one run on 2026-09-15, toggling one contributor at a time:
#
#   rung A  origin=archive  floor off (that morning)    0 of 42 failing
#   rung B  origin=ledger   floor off                  19 of 42 failing
#   rung C  origin=archive  floor ON                   20 of 42 failing
#   rung D  origin=ledger   floor ON  (what ships)     39 of 42 failing
#
# and 40 rather than 39 once `RULED_LINKS` moved to the `ledger` tree URL too,
# which took the atlas-02 digest with it. The rungs are differences within one
# run; a rung read from a different run would be a different photograph.
#
# WHY A WAIVER AND NOT A FIX. Neither class of failure is a fault in the
# message. The 20 `linkdest` failures are messages whose link pointed at the
# archive's pages, which is where the pages WERE when they were written. The 40
# `linkfloor` failures include every message written during the window in which
# zero links was LEGAL by ruling (`servedCommit=none`, 2026-09-10 to today).
# Both were correct under the rulebook in force when they went. Grading them
# under today's is letting today's rulebook grade yesterday's specimen, which
# is the fault already written down at LEGACY_LINK_RULES, and the fix nobody
# may make is editing the archived copy of a message Jafar has already read.
#
# THE SHAPE IS LEGACY_LINK_RULES' AND RESEARCH_VERBATIM'S, DELIBERATELY, and
# it is the third instance of ONE idea rather than a new one: a frozen tuple of
# repo-relative NAMES, waiving a NAMED subset of the rules, counted with its
# denominators, with a rot check for entries no file answers. MEMBERSHIP IS BY
# NAME AND NEVER BY THE DATE IN THE NAME: a date switch would let a specimen
# choose its own rulebook by choosing its own filename, which is the reasoning
# at LEGACY_LINK_RULES and it is unchanged here.
#
# IT CANNOT GROW BY ITSELF AND IT DOES NOT COVER TOMORROW. Every name below was
# in the tree before this commit (measured 2026-09-15: all 40 tracked at HEAD,
# newest last-commit 2026-09-15T03:33Z, before the move landed), and 37 of the
# 40 have a send receipt in `production/outbound/`. The three without one are
# `production/briefs/2026-09-06.md`, `2026-09-07.md` and `2026-09-12.md`; they
# are named here on the same ground as the rest, which is WHEN they were
# written and not whether a receipt was found for them. A message written from
# here on is not on this list and faces the full band and the full floor, which
# is the whole point: the next linkless brief is refused.
#
# THE NEXT RUNG DELETES ENTRIES RATHER THAN ADDING THEM. When an archived
# message is superseded or cleared out of `production/outbox/`, its name comes
# off this tuple in the same diff, and the walk's rot count says how many names
# no file answers so that never happens in silence.
# GATE-ONLY, EXACTLY AS LEGACY_LINK_RULES IS, AND ON PURPOSE (ruled
# 2026-09-15 05:43Z). main() below, the single-file path that
# tools/runner/outbox.py:run_check and the brief sender shell out to,
# passes research_verbatim by name and does not pass pre_move, so at
# the DOOR a name on this list faces the floor in force at the moment
# of sending. That is the right direction: this list grades messages
# that were already sent, and a message sent after the move carries
# a link or does not go. Three names here have no receipt (briefs
# 2026-09-06, -07 and -12); if one of them is ever sent it is refused
# on linkfloor at the door and the Producer rewrites it with a link
# or drops it. Do not "fix" the door by passing pre_move to it.
PRE_MOVE_MESSAGES = (
    "production/briefs/2026-09-06.md",
    "production/briefs/2026-09-07.md",
    "production/briefs/2026-09-09.md",
    "production/briefs/2026-09-10.md",
    "production/briefs/2026-09-12.md",
    "production/briefs/2026-09-14.md",
    "production/briefs/2026-09-15.md",
    "production/outbox/2026-09-06-pc-processes-one-window.answer.md",
    "production/outbox/2026-09-06-the-map-and-its-link.unprompted.md",
    "production/outbox/2026-09-06-where-the-project-stands.unprompted.md",
    "production/outbox/2026-09-07-the-map-changed-4917df34e120.unprompted.md",
    "production/outbox/2026-09-07-the-map-changed-78a360dcdf18.unprompted.md",
    "production/outbox/2026-09-07-the-walk.answer.md",
    "production/outbox/2026-09-08-closing-status.brief.md",
    "production/outbox/2026-09-08-the-first-crime.brief.md",
    "production/outbox/2026-09-08-the-four-confirmations.brief.md",
    "production/outbox/2026-09-08-the-return-half-works.unprompted.md",
    "production/outbox/2026-09-08-the-street-and-the-correction.brief.md",
    "production/outbox/2026-09-08-you-were-right-about-11-30.unprompted.md",
    "production/outbox/2026-09-09-atlas-02-research-digest.unprompted.md",
    "production/outbox/2026-09-09-morning-brief.brief.md",
    "production/outbox/2026-09-09-the-grate-readable.unprompted.md",
    "production/outbox/2026-09-09-the-map-changed-388cdbcead10.unprompted.md",
    "production/outbox/2026-09-11-yes-it-works.answer.md",
    "production/outbox/2026-09-14-research-1of5-kcd2-part1.answer.md",
    "production/outbox/2026-09-14-research-1of5-kcd2-part2.answer.md",
    "production/outbox/2026-09-14-research-2of5-hitman-part1.answer.md",
    "production/outbox/2026-09-14-research-2of5-hitman-part2.answer.md",
    "production/outbox/2026-09-14-research-3of5-rdr2-part1.answer.md",
    "production/outbox/2026-09-14-research-3of5-rdr2-part2.answer.md",
    "production/outbox/2026-09-14-research-4of5-disco-elysium-part1.answer.md",
    "production/outbox/2026-09-14-research-4of5-disco-elysium-part2.answer.md",
    "production/outbox/2026-09-14-research-5of5-shadows-of-doubt-part1.answer.md",
    "production/outbox/2026-09-14-research-5of5-shadows-of-doubt-part2.answer.md",
    "production/outbox/2026-09-14-the-street-before.answer.md",
    "production/outbox/2026-09-14-the-street-then-after-the-brief.brief.md",
    "production/outbox/2026-09-14-the-street-then-one-call-for-you.brief.md",
    "production/outbox/2026-09-14-the-street-then-the-frame-itself.brief.md",
    "production/outbox/2026-09-14-the-street-then-your-sky-on-it.brief.md",
    "production/outbox/2026-09-14-the-street-then-your-sky-strike-one-sentence"
    ".answer.md",
)
# EXACTLY THE TWO RULES THE MOVE BROKE, and nothing else. `linkcap` is NOT
# here: nothing about the move changed how many links a message carries, so a
# pre-move message over the cap is still refused. Named in one constant so the
# waiver, the report and the selftest cannot come to disagree about its width.
PRE_MOVE_WAIVED_RULES = ("linkfloor", "linkdest")

# ---------------------------------------------------------------------------
# THE BRIEFS THAT WERE WRITTEN BEFORE THE READING ASK WAS RULED, 2026-09-15.
#
# THE SHAPE IS LEGACY_LINK_RULES', RESEARCH_VERBATIM'S AND PRE_MOVE_MESSAGES',
# DELIBERATELY, and it is the fourth instance of ONE idea rather than a new
# one: a frozen tuple of repo-relative NAMES, waiving a NAMED subset of the
# rules, counted with its denominators, with a rot check for entries no file
# answers. MEMBERSHIP IS BY NAME AND NEVER BY THE DATE IN THE NAME, which is
# the reasoning written out at LEGACY_LINK_RULES and unchanged here: the date
# at the front of a filename is typed by the writer, so a date switch lets the
# specimen choose its own rulebook.
#
# IT IS NOT FOLDED INTO PRE_MOVE_MESSAGES even though the two lists overlap.
# That list's own comment says "EXACTLY THE TWO RULES THE MOVE BROKE, and
# nothing else"; a reading ask has nothing to do with the site move, and two
# waivers under one name is how a narrow exemption becomes a wide one nobody
# noticed.
#
# MEASURED BEFORE IT WAS WRITTEN, on the live tree at 2026-09-15T19:51Z:
# `--gate` graded 17 of 43 checked files as briefs and every one of them was
# written before this evening's ruling, so requiring the ask without this list
# would turn a clean walk (0 failing of 43) into 17 failures on messages that
# were correct when they went, and the fix nobody may make is editing a brief
# Jafar has already read.
#
# GATE-ONLY, EXACTLY AS LEGACY_LINK_RULES AND PRE_MOVE_MESSAGES ARE, AND ON
# PURPOSE. main() below, the single-file path the sender shells out to, does
# not pass pre_reading, so AT THE DOOR a name on this list still faces the
# rule: measured 2026-09-15, `--kind brief production/briefs/2026-09-15.md`
# reports the ask at 1 of 3 parts and refuses. That is the right direction.
# This list grades briefs that were already sent; a brief sent from here on
# carries the ask or does not go. Do not "fix" the door by passing pre_reading
# to it.
#
# IT CANNOT GROW BY ITSELF AND IT DOES NOT COVER TOMORROW. A brief written from
# here on is not on this list and is refused without the ask, which is the
# whole point. The next rung DELETES entries rather than adding them, and the
# walk's rot count says how many names no file answers so that never happens in
# silence.
PRE_READING_BRIEFS = (
    "production/briefs/2026-09-05.md",
    "production/briefs/2026-09-06.md",
    "production/briefs/2026-09-07.md",
    "production/briefs/2026-09-09.md",
    "production/briefs/2026-09-10.md",
    "production/briefs/2026-09-12.md",
    "production/briefs/2026-09-14.md",
    "production/briefs/2026-09-15.md",
    "production/outbox/2026-09-08-closing-status.brief.md",
    "production/outbox/2026-09-08-the-first-crime.brief.md",
    "production/outbox/2026-09-08-the-four-confirmations.brief.md",
    "production/outbox/2026-09-08-the-street-and-the-correction.brief.md",
    "production/outbox/2026-09-09-morning-brief.brief.md",
    "production/outbox/2026-09-14-the-street-then-after-the-brief.brief.md",
    "production/outbox/2026-09-14-the-street-then-one-call-for-you.brief.md",
    "production/outbox/2026-09-14-the-street-then-the-frame-itself.brief.md",
    "production/outbox/2026-09-14-the-street-then-your-sky-on-it.brief.md",
)
# EXACTLY THE ONE RULE THE RULING ADDED, and nothing else. Every other rule
# still binds on every name above.
PRE_READING_WAIVED_RULES = ("reading",)

# ---------------------------------------------------------------------------
# RESEARCH DELIVERIES THAT GO TO HIM VERBATIM. Ruled by Jafar 2026-09-14: when
# a research delivery lands, its SUMMARY.md goes to him "through the bot as its
# own message, in full, before you act on anything in it".
#
# WHY THE REGISTER HAD TO MOVE AND NOT THE DOCUMENTS. Five coverage audits were
# staged on 2026-09-14 and four were refused, every one of them on `banned:run
# internals` alone, for these words used as ORDINARY ENGLISH: "job" (the man
# whose job it is opens the yard), "commit"/"committed" (committing a crime),
# and "gate" (a gate in a city). The ban list is a word filter and cannot tell a
# CI job from a man's job. It must not try: a context-sensitive word filter is a
# worse instrument than a narrow exemption that is counted. Obeying the register
# here would mean editing documents Jafar asked for IN FULL, and the channel
# regime of 2026-09-09 says the register "stays as a FORMAT CHECK AFTER the
# Producer writes, never as a gate that shapes what is written". His instruction
# is the authority; the register is not.
#
# THE SHAPE IS LEGACY_LINK_RULES', DELIBERATELY, and not a second mechanism: a
# frozen tuple of repo-relative NAMES, waiving a NAMED subset of the rules, that
# widens only in a reviewed diff. BY NAME AND NEVER BY PATTERN, for the reason
# written at LEGACY_LINK_RULES: a rule that matched "research" in a filename
# would let any future session name a file into the exemption and out of the ban
# list, which is the specimen choosing its own rulebook.
#
# IT IS NOT A HOLE. Only `banned` is waived. linkcap, linkdest and linkfloor
# still bind in full on these files, `banned` is still named under NOT ENFORCED
# on every one of them, and the gate prints how many of these entries the waiver
# actually CHANGED anything for, which is what stops a dead exemption sitting
# here for ever pretending to do work.
#
# WHY EVERY PART IS LISTED AND NOT ONLY THE ONES THAT FAIL. The category is
# "a third-party document he ruled goes to him unedited", not "the files that
# happened to trip the filter". A list assembled from failures cannot be read
# by the next person: 1of5-kcd2-part1's absence would say nothing about
# whether it is a research delivery. All ten parts are listed, and the LADDER
# below measures whether the waiver did anything for each one, so "part 1 of
# kcd2 passes the ban list on its own merits" is a reading printed on every
# run rather than an arrangement nobody can see. MEASURED on these ten files,
# 2026-09-14, and printed on every gate run as researchVerbatimWaiverBit: the
# waiver changes the verdict on 5 of the 10, and the other 5 pass with it and
# without it.
#
# WHY THE TEN SPLIT PARTS AND NOT THE FIVE UNSPLIT FILES, ruled 2026-09-14.
# Jafar ruled the same day that each summary goes to him in TWO messages with
# the cut announced in both halves. The five unsplit files run 5300 to 6221
# characters, every one of them over the wire's cap, so no sweep can ever send
# one and they are held in BLOCKED_DIR. Listing one here would be an exemption
# for a file that must never go out, which is why the selftest asserts both
# halves of that: no BLOCKED_DIR original is on the sendable list, and every
# name on that list measures under the wire cap while every original measures
# over it, with the cap READ FROM tools/runner/executor.py rather than typed
# here.
#
# AND THE SPLIT IS ASSERTED LOSSLESS RATHER THAN TRUSTED. "In full" is his
# word for what a research delivery owes him, and a split that silently
# dropped a paragraph would be the worst failure available here: it would pass
# every rule in this file while delivering less than he asked for. So
# research_rejoin() below rebuilds each original from its two parts and the
# selftest compares it to the file in BLOCKED_DIR byte for byte.
#
# WHY THE ORIGINAL IS NAMED IN THE ROW AND NOT DERIVED FROM THE PART'S NAME.
# It was derived, for about an hour on 2026-09-14, and then the ten parts were
# renamed to carry Jafar's send order (research-1of5-kcd2-part1 and so on)
# while the five originals kept the name they were written under. Name
# arithmetic would have gone on returning a path that no longer exists, and
# the lossless check would have reported nothing measured over five pairs it
# could not read, which is the silent instrument this file exists to prevent.
# So each delivery is ONE ROW carrying all three names, the sendable register
# is DERIVED from the rows rather than typed a second time, and a rename shows
# up as a red or as a counted absence instead of as a quiet skip.
RESEARCH_DELIVERIES = (
    ("production/outbox/"
     "2026-09-14-research-1of5-kcd2-part1.answer.md",
     "production/outbox/"
     "2026-09-14-research-1of5-kcd2-part2.answer.md",
     "production/outbox-blocked/"
     "2026-09-14-research-coverage-audit-kcd2.answer.md"),
    ("production/outbox/"
     "2026-09-14-research-2of5-hitman-part1.answer.md",
     "production/outbox/"
     "2026-09-14-research-2of5-hitman-part2.answer.md",
     "production/outbox-blocked/"
     "2026-09-14-research-coverage-audit-hitman.answer.md"),
    ("production/outbox/"
     "2026-09-14-research-3of5-rdr2-part1.answer.md",
     "production/outbox/"
     "2026-09-14-research-3of5-rdr2-part2.answer.md",
     "production/outbox-blocked/"
     "2026-09-14-research-coverage-audit-rdr2.answer.md"),
    ("production/outbox/"
     "2026-09-14-research-4of5-disco-elysium-part1.answer.md",
     "production/outbox/"
     "2026-09-14-research-4of5-disco-elysium-part2.answer.md",
     "production/outbox-blocked/"
     "2026-09-14-research-coverage-audit-disco-elysium.answer.md"),
    ("production/outbox/"
     "2026-09-14-research-5of5-shadows-of-doubt-part1.answer.md",
     "production/outbox/"
     "2026-09-14-research-5of5-shadows-of-doubt-part2.answer.md",
     "production/outbox-blocked/"
     "2026-09-14-research-coverage-audit-shadows-of-doubt.answer.md"),
)
# THE SENDABLE REGISTER, DERIVED: the two PARTS of every row and never the
# third name, which is the unsplit original and must never be sendable. One
# line, so a reader can see that the register cannot contain anything the rows
# above do not, and the selftest asserts the exclusion rather than trusting
# this expression.
RESEARCH_VERBATIM = tuple(rel for row in RESEARCH_DELIVERIES
                          for rel in row[:2])
# THE ONE RULE THE VERBATIM EXEMPTION WAIVES, named once so the switch, the
# report and the gate cannot come to disagree about what it covers. Adding a
# name here widens the exemption for every file on the list above at once,
# which is why it is a constant a reviewer can see and not a literal inside a
# branch.
RESEARCH_WAIVED_RULES = ("banned",)
# Counts are legitimate in an answer and only there. Named as its own set
# rather than hidden inside the register tuple, so the exemption is greppable.
COUNTS_ALLOWED_IN = {"answer"}

# ---------------------------------------------------------------------------
# THE SPLIT, AND PROVING IT LOST NOTHING. Ruled by Jafar 2026-09-14: each
# research summary is split in two, "with the cut announced in the message",
# and all five go out in order before anything acts on them. The register above
# lists the parts. What follows is the arithmetic that puts them back together,
# and it lives HERE, in the layer the selftest runs, rather than in the script
# that did the splitting: a split asserted once in a throwaway script is a
# split nobody can re-check on the day somebody edits one of these files.

#: Where the Producer writes, and the first of GATE_TREES below, which is
#: built from this name rather than repeating it: `tools/runner/outbox.py`
#: asserts its own OUTBOX_DIR equals GATE_TREES[0], so a third copy of the
#: string is a third place for the sender and the gate to disagree about which
#: directory is the outbox.
OUTBOX_DIR = "production/outbox"

#: Where a message OVER THE WIRE CAP is held so no sweep can ever pick it up.
#: Deliberately NOT one of GATE_TREES: nothing in here is sendable, and walking
#: it would grade files whose whole problem is that they must not go out.
BLOCKED_DIR = "production/outbox-blocked"

#: How a split part names itself, and what the unsplit original it came from is
#: called. Name arithmetic only; nothing here reads a file.
RESEARCH_PART_SUFFIXES = ("-part1.answer.md", "-part2.answer.md")
RESEARCH_WHOLE_SUFFIX = ".answer.md"

#: THE TWO LINES THE SPLIT ADDED and the ONLY text research_rejoin() removes.
#: Matched at the START of a line because that is where the splitter put them.
#: If a marker ever stops matching, the marker text stays in the rejoin and the
#: byte comparison goes RED, which is the safe direction for a guard to fail.
CUT_MARKERS = (b"[CUT HERE:", b"[PART 2 of 2")


def research_pairs(rows=RESEARCH_DELIVERIES):
    """(part1, part2, unsplit-original) per delivery, and every row that does
    not hold that shape. PURE: name arithmetic, reads no file, so it answers
    the same on a machine with no outbox at all.

    Returns (pairs, faults). A row is a FAULT rather than a pair when its two
    parts are not the two announced part suffixes under the outbox, or when
    its third name is not under BLOCKED_DIR. That last one is the dangerous
    typo: an original listed where a part belongs would put an unsendable file
    on the sendable register. A fault is RETURNED AND NAMED, never dropped, so
    a row nobody could parse cannot read as a row that passed.
    """
    pairs, faults = [], []
    for row in rows:
        if len(row) != 3:
            faults.append("%d-name(s)-in-a-row-that-needs-3/%s"
                          % (len(row), "+".join(row) or "empty"))
            continue
        p1, p2, whole = row
        bad = [rel for rel, suffix in zip((p1, p2), RESEARCH_PART_SUFFIXES)
               if not (rel.endswith(suffix)
                       and rel.startswith(OUTBOX_DIR + "/"))]
        if not whole.startswith(BLOCKED_DIR + "/") \
                or not whole.endswith(RESEARCH_WHOLE_SUFFIX):
            bad.append(whole)
        if bad:
            faults.append("/".join(bad))
            continue
        pairs.append((p1, p2, whole))
    return pairs, faults


def research_rejoin(part1, part2, markers=CUT_MARKERS):
    """The two halves of a split delivery put back together. PURE: bytes in,
    a reading out, reads no file.

    THE ONLY TEXT IT REMOVES is a line starting with one of the announced cut
    markers, and the ONLY thing it normalises is the run of blank lines at the
    seam, which is what the split itself inserted. Every other byte of either
    half survives into the rejoin, which is the whole point: this exists to
    catch a split that dropped a paragraph, so it must not be able to tidy one
    away.
    """
    dropped = []

    def strip(blob):
        kept = []
        for line in blob.split(b"\n"):
            if any(line.startswith(m) for m in markers):
                dropped.append(line)
            else:
                kept.append(line)
        return b"\n".join(kept)

    a, b = strip(part1), strip(part2)
    return {"joined": a.rstrip(b"\n") + b"\n\n" + b.lstrip(b"\n"),
            # CUMULATIVE over both halves: how many announced marker lines this
            # rejoin took out. Two is the shape the splitter of 2026-09-14
            # produced; zero would mean the markers stopped matching.
            "markers_dropped": len(dropped),
            "bytes_part1": len(part1), "bytes_part2": len(part2)}


def research_rejoin_reading(original, part1, part2):
    """research_rejoin() against the file it claims to reproduce. PURE.

    THE PAIRED READING: `equal` never travels without `first_diff`, the BYTE
    OFFSET of the first difference (-1 when identical), and `bytes_delta`, the
    rejoin's length minus the original's. Equality alone says a split is sound;
    the offset says where to look when it is not, in the same entry, so no
    reader has to join two numbers from two lines.
    """
    r = research_rejoin(part1, part2)
    joined = r["joined"]
    r["bytes_joined"] = len(joined)
    r["bytes_original"] = len(original)
    r["bytes_delta"] = len(joined) - len(original)
    r["equal"] = joined == original
    first = -1
    if not r["equal"]:
        for i in range(min(len(joined), len(original))):
            if joined[i] != original[i]:
                first = i
                break
        else:
            first = min(len(joined), len(original))
    r["first_diff"] = first
    return r

# WHERE A LINK MAY POINT, RULED BY JAFAR 2026-09-06, verbatim: "images are
# sent as Telegram images, never as links; at most two links per message, and
# never to a repo markdown file, only to the glance, map or gallery".
#
# SO THE ALLOWLIST IS PUBLISHED PAGES, NOT A HOST, and how many there are is
# read off SITE_PAGES rather than typed into prose. It used to be a host list,
# and that is the hole: production/outbox/2026-09-05-the-console-run.
# unprompted.md carried fifteen URLs, thirteen of them to github.com and eight
# of those to repository markdown files, and this program printed SEND. That
# pass is the measurement this rule was written from, taken 2026-09-06 before
# the change: urls=15 goodLinks=13 findings=0.
#
# AN IMAGE IS NOT A LINK EITHER. A blob link to a .png is still a link to the
# repository, so it fails `linkdest` like any other; the picture goes to him as
# a Telegram image, which is the sender's job and not this program's.
# MOVED 2026-09-15 (queue 256 deliverable 2, queue 259). It held the value of
# `ARCHIVE_ORIGIN` below, character for character, from the move of 2026-09-10
# until today (named that way rather than repeated, so this file carries the
# archive string ONCE, at the constant that rejects it), because nobody here
# could measure whether either site served: the
# container's egress proxy refuses github.io at CONNECT. publish-glance run 26
# (id 34928226785) measured it on a runner instead and its check step passed on
# all four published pages at commit ada1535b, which is the sha now in
# `production/site-served.txt`. THE TWO FACTS ARE STILL SEPARATE: that run
# proves the PAGE serves, this constant is what the CHECKER believes, and
# moving one without the other is the half-move `marker_origin_consistent()`
# below exists to refuse.
SITE_ORIGIN = "https://jsab258.github.io/ledger/"
# THE ORIGIN A LINK MUST NEVER POINT AT after the move of 2026-09-10, and it is
# KEPT after queue 256 flips SITE_ORIGIN off it, BECAUSE A REJECTING FIXTURE
# MUST NAME WHAT IT REJECTS: a guard whose refused value was deleted from the
# file is a guard nobody can prove still bites. SINCE 2026-09-15 THE TWO
# CONSTANTS DIFFER, which is the first day this rejecting fixture can actually
# fire: while they were equal, "an archive link is refused" was untestable, and
# the selftest now drives it (search REJECTING, THE ARCHIVE ORIGIN ITSELF).
ARCHIVE_ORIGIN = "https://jsab258.github.io/wc26-picks/"
# (path under the origin, what to call it in a finding). The empty path is the
# glance itself. Adding a page here is the ONE place the allowlist grows.
SITE_PAGES = (("", "the-glance"),
              ("map.html", "the-map"),
              ("gallery.html", "the-gallery"),
              # THE FOURTH PAGE, added 2026-09-09, and it is not adjacent work.
              # Jafar's item 2 of that morning (production/NOW.md): "The town
              # atlas from art/atlas-01 goes in the gallery as a world page,
              # not on the map." tools/publish-glance.py's PAGES already
              # publishes world.html, as the gallery row's extraPages entry
              # ("--world-out", "world.html"), so the publisher's list and this
              # one were two copies of one idea left out of step by the same
              # batch: a page he can open that the register would refuse to
              # link. Ruled A5 of section 2.5 of game-design/decision-2026-09-
              # 09-the-hook-comparison-the-ruled-link-and-the-stale-pages.md.
              # Reversible in one line if he says the band stays at three.
              ("world.html", "the-world"),
    # A2 OF THE BATCH RULING, 2026-09-09. tools/publish-glance.py PAGES (120)
    # publishes index.html and glance.html from the ONE generator, so the glance
    # under its own filename is the glance. The per-card link Jafar taps is
    # index.html#card-<id>, and without this row site_page refuses it; it survives
    # today only because send_cards never calls the check.
    ("index.html", "the-glance"))
# THE BAND, not a floor: one link at least (constitution law 12, evidence) and
# two at most (Jafar, 2026-09-06). Both ends are his, neither is measured, and
# both are cited rather than chosen.
LINK_MIN, LINK_MAX = 1, 2

# ---------- THE ONE CONDITION UNDER WHICH THE FLOOR DOES NOT FIRE, 2026-09-11
#
# THE FLOOR IS NOT DELETED AND THE BAND IS NOT WIDENED. `LINK_MIN` above is
# still 1 and `SITE_PAGES` still names every destination a link may point at.
# What changed is WHEN the floor applies, and the change is narrow, temporary
# and ruled.
#
# THE RULING. `game-design/decision-2026-09-10-ruling-the-move-batch-and-the-
# fleet-left-behind.md`, section 5 finding 6, verbatim: "Until this item lands,
# briefs carry no site link; the register allows zero." Filed as
# `production/queue/256` (which decides when a page IS served) and
# `production/queue/259` (the code catching up with the ruling, where the cost
# is written down: this program refused a finished answer to Jafar on
# `linkfloor` alone, and `tools/runner/outbox.py:run_check` reads exit 1 as DO
# NOT SEND, so the message sat in the outbox and he got silence).
#
# WHY THE FLOOR IS WRONG TODAY AND NOT IN GENERAL. LEDGER moved off
# `jsab258/wc26-picks` on 2026-09-10, and all five destinations in SITE_PAGES
# sit under the ARCHIVE's published pages. After the move a link shows him the
# world as it was BEFORE it. A message with no link is honest; a message with
# one of those links is not. The floor's own reasoning, that a message without
# evidence behind it teaches vagueness, is untouched by the move, which is why
# the rule is made CONDITIONAL rather than removed or loosened.
#
# THE CONDITION IS A FACT ON DISK, NOT A GUESS AND NOT A DATE. One committed
# marker, one machine-readable line, read by link_floor_state() below and by
# nothing else. A date switch would let the specimen choose its own rulebook,
# which is the fault already written down at LEGACY_LINK_RULES; a constant in
# this file would be a session's opinion about a page it never loaded.
#
# THE FAILURE DIRECTION IS LOUD, ON PURPOSE. A missing marker, an unreadable
# one, or a marker carrying anything other than exactly one `servedCommit=`
# line all leave the floor LIVE, with the fault named in the printed reason. A
# broken instrument then refuses a linkless message and somebody looks; the
# other direction sends a message with no evidence because nobody could read
# the fact, which is the silent-instrument failure `.claude/rules/
# instruments.md` exists for.
SERVED_MARKER_REL = "production/site-served.txt"
SERVED_KEY = "servedCommit"
#: The value that means NO page is served. Anything else is a served commit.
SERVED_NONE = "none"
#: Built from SERVED_KEY so the key has ONE spelling in this file.
SERVED_LINE_RE = re.compile(r"(?m)^\s*%s=(\S+)" % SERVED_KEY)
#: How much of the marker's value the printed reason carries. A whole sha is
#: 40, so this never bites on a correct marker; cap() announces it when it does.
SERVED_VALUE_WIDTH = 40
#: The reason a caller that took no reading at all gets. Named rather than
#: typed at the default, so `not-consulted` is greppable and can never be
#: confused with `no-page-served-yet`: one is an instrument that did not look,
#: the other is a fact it looked at.
FLOOR_NOT_CONSULTED = ("not-consulted..caller-took-no-reading"
                       "..floor-stays-live")


def floor_reading(active, reason, served=None, lines=0):
    """ONE CONSTRUCTOR for the link floor's reading, so the strict default and
    the file reader cannot drift apart about which keys exist."""
    return {"active": active, "reason": reason, "marker": SERVED_MARKER_REL,
            "served": served, "marker_lines": lines}


def link_floor_state(root):
    """IS THE EVIDENCE FLOOR LIVE RIGHT NOW, and why, read off disk.

    Returns floor_reading(). `active` is the branch; `reason` is a token with
    NO SPACES in it (every reader of a key=value channel splits on whitespace),
    structured with `/` and `..`, and both are printed by report() and
    gate_report() on every run, pass or fail. A branch nobody can see taken is
    a branch nobody audits.

    FOUR OUTCOMES, THREE OF THEM STRICT:
      - exactly one `servedCommit=none` line  -> floor OFF, zero links legal;
      - exactly one `servedCommit=<sha>` line -> floor ON at LINK_MIN..LINK_MAX;
      - no marker, or an unreadable one       -> floor ON, the absence named;
      - zero or several `servedCommit=` lines -> floor ON, the count named.
    """
    marker = pathlib.Path(root) / SERVED_MARKER_REL
    try:
        text = marker.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return floor_reading(True, "marker-absent..%s..floor-stays-live"
                             % SERVED_MARKER_REL)
    except OSError:
        return floor_reading(True, "marker-unreadable..%s..floor-stays-live"
                             % SERVED_MARKER_REL)
    hits = SERVED_LINE_RE.findall(text)
    if len(hits) != 1:
        return floor_reading(
            True,
            "marker-carries-%d-%s-lines-of-the-1-required..%s"
            "..floor-stays-live" % (len(hits), SERVED_KEY, SERVED_MARKER_REL),
            lines=len(hits))
    value = hits[0]
    # THE VALUE IS CAPPED AND THE CAP ANNOUNCES ITSELF, through the one
    # implementation of the truncation notice this repo has. 40 characters is a
    # whole sha, so it never bites on a correct marker; it exists so a marker
    # carrying a paragraph cannot push the rest of a done line off a reader's
    # screen and read as a finding. The value goes LAST in the token, so the
    # `...` lands at the end and cannot be misread as a separator.
    shown = cap([value], keep=1, width=SERVED_VALUE_WIDTH)
    if value.lower() == SERVED_NONE:
        return floor_reading(False, "no-page-served-yet..%s..%s/%s"
                             % (SERVED_MARKER_REL, SERVED_KEY, shown),
                             served=value, lines=1)
    return floor_reading(True, "page-served..%s..%s/%s"
                         % (SERVED_MARKER_REL, SERVED_KEY, shown),
                         served=value, lines=1)


def marker_origin_consistent(reading, site_origin):
    """(ok, reason) for the ONE transition A1 forbids: a served commit typed
    into the marker while site_origin is still the archive, which turns the
    floor back ON and makes the STALE link MANDATORY, not merely legal. PURE.
    ok is True while the floor is off or nothing is served (an absent or
    malformed marker is A1's business only in that it passes); reason carries
    no spaces and is empty on a pass."""
    if not reading["active"] or reading["served"] is None:
        return True, ""
    if norm_url(site_origin) != norm_url(ARCHIVE_ORIGIN):
        return True, ""
    return False, ("marker-names-served-commit-but-SITE_ORIGIN-is-the-archive"
                   "..%s" % reading["marker"])


# THE ONE RULED WHOLE-URL EXCEPTION TO THE DESTINATION BAND, and it is an
# EXCEPTION AND NOT A HOLE. (url, label, rulingRecordPath), frozen, one member.
#
# WHY IT EXISTS. Jafar, 2026-09-09, item 4(c) of production/NOW.md, verbatim:
# "One message, plain English, digesting the atlas-02 research: what was found,
# what is missing, with the link." The research is five markdown files in the
# repository and no published page carries it, so the only honest link is one
# his own band of 2026-09-06 forbids ("never to a repo markdown file, only to
# the glance, map or gallery"). His later instruction governs its instance and
# repeals the band for nothing else, which is why the mechanism is one URL
# matched by whole string rather than a widened rule.
#
# THE NEXT RUNG DELETES THE ENTRY. Ruled in section 2 (2.4 and 2.5) of
# game-design/decision-2026-09-09-the-hook-comparison-the-ruled-link-and-the-
# stale-pages.md and filed as production/queue/184: when the research is
# published as a page, that page goes in SITE_PAGES and RULED_LINKS loses this
# entry in the SAME commit, so the exception cannot outlive its reason.
#
# HOW IT IS KEPT HONEST. ruled_link() matches the WHOLE normalised string, so
# the parent directory, a child file, blob instead of tree, another branch and
# one extra character are all refused: the selftest runs those five. The
# selftest also asserts the tuple holds exactly one member and that every
# entry's ruling record exists in the tree and still carries the URL, which is
# the guard against an entry outliving its ruling.
#
# THE URL IS ONE UNWRAPPED LITERAL ON PURPOSE, so a grep for the whole URL
# finds the place that admits it.
RULED_LINKS = (
    ("https://github.com/jsab258/ledger/tree/main/production/art/atlas-02/research",
     "atlas-02-research",
     "game-design/decision-2026-09-09-the-hook-comparison-the-ruled-link-and-the-stale-pages.md"),
)

# THE RETIRED DESTINATION LIST, kept because the link FLOOR is older than the
# band and the three named messages satisfied the floor with the destinations
# that existed when they were written. It governs ONLY the files named in
# LEGACY_LINK_RULES and it can never widen. Without it, changing what "an
# allowed link" MEANS would fail those three through the oldest rule in the
# file rather than through the new one.
LEGACY_LINK_HOSTS = ("github.com", "raw.githubusercontent.com")
LINK_RE = re.compile(r"https?://[^\s<>()\[\]]+")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")

# ------------------------------------------------------------------- banned
# Each pattern runs over the SCRUBBED text (links removed), because the links
# are the evidence floor and a path check that fires on a required URL would
# make the two rules contradict each other.

KNOWN_DIRS = ("production", "tools", "ledger", "ledger-v2", "game-design",
              ".claude", "research", "legacy", "docs", "assets")
EXT_RE = re.compile(r"\.(md|py|cs|json|txt|html?|ya?ml|jpe?g|png|bat|sh|tsv|"
                    r"csv|uasset|umap)\b", re.I)
SLASHED_RE = re.compile(r"(?<![\w/])(?:[\w.@#-]+/)+[\w.@#-]+")


def find_paths(text):
    """File paths and directory names. A slashed token counts as a path when it
    carries a file extension, or has two or more slashes, or begins with a
    directory this repo actually has. `and/or` and `24/7` are neither, and a
    check that flagged them would be overruled by its second user."""
    out = []
    for m in SLASHED_RE.finditer(text):
        tok = m.group(0)
        if (EXT_RE.search(tok) or tok.count("/") >= 2
                or tok.split("/")[0].lower() in KNOWN_DIRS):
            out.append(tok)
    for m in re.finditer(r"(?<![\w/])[\w.-]*" + EXT_RE.pattern, text, re.I):
        tok = m.group(0)
        if tok not in out:
            out.append(tok)
    return out


BANNED = [
    ("verdict key",
     lambda t: [m.group(0) for m in
                re.finditer(r"(?<![\w=])[A-Za-z][\w-]*=[^\s]+", t)]),
    ("run internals",
     lambda t: [m.group(0) for m in re.finditer(
         r"\b(workflow|workflows|runner|runners|dispatch\w*|sha|shas|commit\w*|"
         r"branch\w*|CI\b|job|jobs|verdict\w*|gate|gates|exit code|selftest\w*|"
         r"stack trace|pull request|PR\b|repo|repository|grep\w*|log file|"
         r"artifact ID)\b", t, re.I)]),
    ("tool narration",
     lambda t: [m.group(0) for m in re.finditer(
         r"\b(I (?:ran|checked|opened|grepped|read|looked at|verified|re-ran|"
         r"rebuilt|kicked off)|let me\b|I'?ll now\b|I have (?:run|checked)|"
         r"I am (?:running|checking))", t, re.I)]),
    ("heartbeat",
     lambda t: [m.group(0) for m in re.finditer(
         r"\b(still working|still going|quick update|status update|"
         r"checking in|just a moment|no news|nothing to report|as promised|"
         r"as an update|touching base)\b", t, re.I)]),
    ("self-correction",
     lambda t: [m.group(0) for m in re.finditer(
         r"\b(I was wrong|my mistake|apolog\w+|sorry\b|earlier I said|"
         r"correction:|to correct|it turns out I|I had assumed|I misread|"
         r"I should have)\b", t, re.I)]),
    ("file path", find_paths),
]

# ------------------------------------------------------- counts, and the forms
# that are NOT counts. Order matters: each scrub removes a legitimate numeral
# form before the next one looks, so what survives to the end is a count.
PRODUCT_NUMERALS = (r"\bGTA\s?6\b", r"\bGTA\s?5\b", r"\bKCD\s?2\b")
NUMERAL_OK = [
    ("ISO date", r"\b\d{4}-\d{2}-\d{2}\b"),
    ("clock time", r"\b\d{1,2}[:.]\d{2}\s?(?:am|pm)?\b"),
    ("named-month date", r"\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|"
                        r"March|April|May|June|July|August|September|October|"
                        r"November|December)\b"),
    ("month-named date", r"\b(?:January|February|March|April|May|June|July|"
                         r"August|September|October|November|December)\s+"
                         r"\d{1,2}(?:st|nd|rd|th)?\b"),
    ("money", r"[£$€]\s?\d[\d,]*(?:\.\d+)?k?\b|\b\d+\s?(?:pounds?|quid)\b"),
    ("duration", r"\b\d+(?:\.\d+)?\s?(?:minute|hour|day|week|month|year)s?\b"),
    ("list label", r"(?m)^\s*\d{1,2}[.)]\s"),
    ("product name", "|".join(PRODUCT_NUMERALS)),
]
NUMERAL_RE = re.compile(r"(?<![\w-])\d[\d,]*(?:\.\d+)?%?(?![\w])")


def find_counts(text):
    """Bare quantities. Dates, clock times, money, durations, numbered list
    labels and product names carry digits and are not counts; what is left
    after those are scrubbed is '563 of 593' and '72 gates', which are the
    shape Jafar ruled out of his messages."""
    t = text
    # A PATH IS ONE VIOLATION, NOT TWO. `production/queue/062-uv.md` was being
    # reported as a path AND as the count 062, which trains a reader to skim
    # the finding list. The path rule owns it.
    for tok in find_paths(t):
        t = t.replace(tok, " " * len(tok))
    for _, pat in NUMERAL_OK:
        t = re.sub(pat, lambda m: " " * len(m.group(0)), t, flags=re.I)
    return [m.group(0) for m in NUMERAL_RE.finditer(t)]


# ------------------------------------------------------------- claim detection
ASSERTION_RE = re.compile(
    r"\b(is|are|was|were|isn'?t|aren'?t|has|have|had|does|did|"
    r"landed|shipped|works|working|failed|passed|broke|broken|fixed|added|"
    r"removed|started|stopped|finished|stalled|runs|ran|renders|rendered|"
    r"built|wired|measured|chose|ruled|holds|stands|sits)\b", re.I)
# Lines that propose, label or structure rather than assert. A recommendation
# is an argument for a choice, not a claim about the world, and a check that
# demanded a link on `DEFAULT B if unruled` would teach link-stuffing.
NON_CLAIM_PREFIX = re.compile(
    r"^\s*(?:[-*>]\s*)?(?:%s|RECOMMENDATION|RECOMMEND|DEFAULT|DEADLINE|"
    r"OPTION|[A-D][.)]\s|\d{1,2}[.)]\s|#)" % "|".join(SECTIONS), re.I)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")


def sentences(text):
    """(line-relative sentence, its section) for every sentence in the body."""
    out, section = [], "(before any section)"
    for line in text.splitlines():
        head = section_label(line)
        if head:
            section = head
            # THE PREFIX CONTEXT IS THE LINE MINUS ITS LABEL. Passing the whole
            # line made every section-opening sentence non-claim-shaped,
            # because the label itself matched the non-claim prefix: HEADLINE
            # carries the headline, which is the most claim-shaped sentence in
            # the message, and the first selftest run caught 1 claim in 18
            # sentences because of it.
            body = line.split(":", 1)[1] if ":" in line else ""
        else:
            body = line
        for s in SENTENCE_SPLIT.split(body):
            s = s.strip()
            if s:
                out.append((s, section, body))
    return out


def section_label(line):
    """The section this line OPENS, or None. A label is the line's start, in
    capitals, optionally after a markdown heading or bullet mark."""
    t = re.sub(r"^[\s#*>-]+", "", line).strip()
    for name in SECTIONS:
        if t.upper().startswith(name):
            return name
    return None


def claim_shaped(sentence, whole_line):
    """Does this sentence ASSERT something about the world?

    Mechanical, and the definition is printed in the report so nobody has to
    read this function to audit a finding. A sentence is claim-shaped when all
    three hold: it is not a question, its line does not begin with a section
    label or an option / recommendation / default / deadline marker, and it
    contains a finite assertion verb from the list above. Everything else is a
    proposal, a label or a fragment, and none of those is a claim.
    """
    if sentence.rstrip().endswith("?"):
        return False
    if NON_CLAIM_PREFIX.match(whole_line):
        return False
    return bool(ASSERTION_RE.search(sentence))


# ------------------------------------------------------------------- the check

class Finding:
    def __init__(self, rule, what, where=""):
        self.rule, self.what, self.where = rule, what, where

    def __str__(self):
        return "%s: %s%s" % (self.rule, self.what,
                             (" [%s]" % self.where) if self.where else "")


def scrub_links(text):
    """Text with every URL and markdown link target replaced by a spacer of
    the same length, so offsets stay honest and no ban pattern fires on the
    evidence the link floor REQUIRES."""
    t = MD_LINK_RE.sub(lambda m: "[%s](%s)" % (m.group(1),
                                               " " * len(m.group(2))), text)
    return LINK_RE.sub(lambda m: " " * len(m.group(0)), t)


def links_in(text):
    return LINK_RE.findall(text)


def site_destination_words(sep="/"):
    """The published pages a link may point to, named from SITE_PAGES itself.

    ONE IMPLEMENTATION. This list used to be typed into the findings and the
    report as the words "the glance, the map or the gallery", which is a copy
    that goes stale the moment the list grows, and it grew on 2026-09-09."""
    return sep.join(lbl for _, lbl in SITE_PAGES)


def norm_url(url):
    """THE ONE NORMALISATION both destination tests use: drop the fragment,
    strip the trailing slash. Two copies of this is how the site list and the
    ruled exception come to disagree about whether a URL with an anchor on it
    is the same URL, and a disagreement there is an admitted link in one test
    and a refused one in the other."""
    return url.split("#", 1)[0].rstrip("/")


def site_page(url):
    """Which of the published pages in SITE_PAGES this URL IS, or None.

    Whole-URL matching, not host matching. `https://github.com/...blob/....md`
    and `https://jsab258.github.io/ledger/map.html` differ only in the part
    a host check throws away, and throwing it away is what let ten repository
    links through on 2026-09-05."""
    u = norm_url(url)
    base = SITE_ORIGIN.rstrip("/")
    if u != base and not u.startswith(base + "/"):
        return None
    rest = u[len(base):].lstrip("/")
    for name, label in SITE_PAGES:
        if rest == name.rstrip("/"):
            return label
    return None


def ruled_link(url):
    """Which frozen RULED_LINKS entry this URL IS, by its label, or None.

    WHOLE-STRING EQUALITY after norm_url(), the same normalisation site_page()
    uses. NO prefix match, NO host match, NO startswith: the admitted URL is a
    directory tree, so a prefix match would admit every file under it and the
    exception Jafar's instruction bought would be a hole in his own band. The
    five near misses the selftest refuses are the parent directory, a child
    file, blob instead of tree, another branch, and one extra character."""
    u = norm_url(url)
    for ruled, label, _record in RULED_LINKS:
        if u == norm_url(ruled):
            return label
    return None


def link_ok(url, legacy_links=False):
    """May this URL appear? `legacy_links` is MEMBERSHIP OF A NAMED LIST, never
    a date: see LEGACY_LINK_RULES for why the specimen may not choose.

    ONE FUNCTION, TWO GENERATIONS. The retired generation is a SUPERSET: the
    ruling of 2026-09-06 REMOVED repository links, it did not remove the site,
    so anything allowed today was allowed before and the tightening is
    monotone. False is the default, which is what every caller with no entry on
    the list must get."""
    if site_page(url) is not None:
        return True
    # THE RULED WHOLE-URL EXCEPTION, consulted after the site and before the
    # retired host list, because it is narrower than either: one string.
    if ruled_link(url) is not None:
        return True
    if legacy_links:
        host = re.sub(r"^https?://", "", url).split("/")[0].lower()
        return host in LEGACY_LINK_HOSTS
    return False


def link_rule_generation(legacy_links, ruled_used=()):
    """Which destination list applied, in words, for the report.

    `/plus-ruled-url` is appended ONLY when a ruled entry was actually MATCHED
    in this message, never merely because the tuple exists. A report that said
    it on every message would say nothing about the one message that used the
    exception, and the exception being visible where it was used is the
    condition it was granted under."""
    site = site_destination_words("-or-")
    if legacy_links:
        gen = "legacy-by-name/%s-or-%s" % (site,
                                           "-or-".join(LEGACY_LINK_HOSTS))
    else:
        gen = "ruled-2026-09-06/%s-only" % site
    if ruled_used:
        gen += "/plus-ruled-url"
    return gen


def count_words(text):
    """Words = whitespace-separated tokens of the body, with URLs removed
    first. The cap must not charge the writer for the link the floor demands,
    or the two rules trade against each other and evidence loses."""
    stripped = MD_LINK_RE.sub(lambda m: m.group(1), text)
    stripped = LINK_RE.sub(" ", stripped)
    stripped = re.sub(r"^[\s#*>-]+", " ", stripped, flags=re.M)
    return [w for w in stripped.split() if re.search(r"\w", w)]


# THE HISTORICAL ANNOTATION, ruled by Jafar 2026-09-06. The token, the split
# and the three scopes live here; LEGACY_LINK_RULES carries the ruling and the
# reasoning for why an exclusion from a cap is pinned to a frozen list.
HISTORICAL_PREFIX = "HISTORICAL,"


def historical_split(text, legacy_links=False):
    """(the one leading annotation line, the body the word cap governs).

    (None, text) for everything else, which is every file in this project bar
    the ones named on LEGACY_LINK_RULES.

    THREE SCOPES, ALL DELIBERATE, because an unscoped exclusion from a cap is
    simply a way round the cap:
      - `legacy_links` is MEMBERSHIP OF THE FROZEN LIST, decided by the caller
        BY NAME, never by anything inside the text and never by the date in a
        filename (LEGACY_LINK_RULES says why the specimen may not choose);
      - the line must be the FIRST line of the file and must begin with the
        exact token, so a marker cannot be dropped in mid-message;
      - exactly ONE line comes back, so a SECOND `HISTORICAL,` line stays in
        the body and is counted like any other line.
    """
    if not legacy_links:
        return None, text
    head, _, rest = text.partition("\n")
    if not head.startswith(HISTORICAL_PREFIX):
        return None, text
    return head, rest


# NO INSTANT TO MEASURE FROM. Passed as `now` by the gate for a file whose
# name carries no date. It is a sentinel and not a datetime on purpose: a
# missing instant must reach the deadline rule as "unreadable" and come out as
# a finding, never as a quietly substituted wall clock.
UNPINNED = object()


def deadline_hours(line, now):
    """Hours from `now` to the deadline this line states, or None when no
    deadline form parses. None is reported as unparseable, never as fine."""
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", line)
    if m:
        try:
            d = datetime.date.fromisoformat(m.group(1))
        except ValueError:
            return None
        return (datetime.datetime.combine(d, datetime.time(9, 0))
                - now).total_seconds() / 3600.0
    m = re.search(r"\b(\d+(?:\.\d+)?)\s?(hour|day|week)s?\b", line, re.I)
    if m:
        mult = {"hour": 1, "day": 24, "week": 168}[m.group(2).lower()]
        return float(m.group(1)) * mult
    if re.search(r"\btomorrow\b", line, re.I):
        return 24.0
    return None


TIME_FORMS = re.compile(
    r"\b(unknown|tonight|tomorrow|\d{4}-\d{2}-\d{2}|"
    r"\d+\s?(?:minute|hour|day|week)s?|monday|tuesday|wednesday|thursday|"
    r"friday|saturday|sunday|this evening|this week|next week)\b", re.I)


# ------------------------------------------------------- the split sentence
# RULED BY JAFAR 2026-09-05 ("every brief reports the STUDIO VERSUS GAME split")
# and given its unit by the director ruling of the same day, section 6: the
# split is COUNTED IN SESSIONS and says so, because production/budget.md line 87
# rules the turns-to-points conversion UNMEASURED and queue 076 is the rate that
# would fix it. A split in a unit nobody has measured is one number twice.
#
# NO LONGER REQUIRED IN THE BRIEF, 2026-09-09. The daily message is graded
# against Jafar's director test, which forbids the unit and the vocabulary this
# sentence is made of, so the number MOVED to the Sunday summary rather than
# being dropped. The two rulings, which supersedes which, and the four moves that
# re-attach this rule are written out at SECTIONS_RETIRED_IN_BRIEF above. This
# detector is kept whole and tested on every selftest run, and the rule name
# stays in RULES so every register prints it under NOT ENFORCED.
#
# WHY IT IS FIVE PARTS AND NOT ONE REGEX OVER A SENTENCE: a brief that names
# the studio and the game but calls the count points is exactly the failure the
# ruling refuses, and a single pattern that missed it would report the rule as
# passing. Each part is named in the finding, so a writer is told which half is
# missing rather than that "the split sentence" is wrong.
#
# `splitBasis=` IS A VERDICT KEY AND STAYS OUT OF THE MESSAGE. The ban list
# already refuses it; this rule requires the words, and tools/morning-brief.py
# prints the key on its own done line. Both halves ruled together, 2026-09-05.
SPLIT_PARTS = (
    ("the studio", re.compile(r"\bstudio\b", re.I)),
    ("the game", re.compile(r"\bgames?\b", re.I)),
    ("the unit, sessions", re.compile(r"\bsessions?\b", re.I)),
    ("the words 'not points'", re.compile(r"\bnot\s+points\b", re.I)),
    ("what makes it points later, 'measured'",
     re.compile(r"\bmeasured\b", re.I)),
)


def split_parts(budget_body):
    """(howManyFound, whichAreMissing) of the five ruled parts in a BUDGET body.

    THE MEASUREMENT LIVES HERE, IN THE TESTED LAYER, and not inside check(),
    because no register enforces this rule today: driven only through check() it
    would ship UNRUN, and an unrun detector that a future Sunday register trusts
    is the silent-instrument failure. The selftest drives this function directly
    over the four synthetic briefs on every run.

    FIVE NAMED PARTS AND NOT ONE REGEX OVER A SENTENCE: a brief that names the
    studio and the game but calls the count POINTS is exactly the failure the
    2026-09-05 ruling refuses, and one pattern over the whole sentence would
    report that brief as passing. Each part is named in the finding, so a writer
    is told WHICH half is missing rather than that "the split sentence" is wrong.
    """
    missing = [name for name, rx in SPLIT_PARTS if not rx.search(budget_body)]
    return len(SPLIT_PARTS) - len(missing), missing


def split_sections(text):
    """{label: body-lines} plus the order the labels appeared in."""
    bodies, order, current = {}, [], None
    for line in text.splitlines():
        head = section_label(line)
        if head:
            current = head
            order.append(head)
            rest = line.split(":", 1)[1] if ":" in line else ""
            bodies.setdefault(head, [])
            if rest.strip():
                bodies[head].append(rest.strip())
            continue
        if current:
            bodies[current].append(line)
    return bodies, order


# ------------------------------------------------- the reading line, 2026-09-15
# RULED BY JAFAR 2026-09-15, recorded in production/budget.md stop condition 2,
# production/repo-move-triggers.md, production/watchdog-prompt.md and
# .claude/agents/producer.md. His reasoning, verbatim: "The ceiling does not
# brake anything, because you cannot read the meter and work from whatever
# number I last typed. A night can spend thirty points while every check says
# the morning's figure." A reading older than TEN HOURS means the day is
# UNMEASURED, and the half that makes that cost him nothing is this one: "THE
# BRIEF ASKS FOR THE READING AS ITS FIRST LINE, EVERY MORNING, AND THE STUDIO
# HOLDS AT INBOX ONLY UNTIL HE ANSWERS", because "that way I am asked once a
# day rather than having to remember, and forgetting costs nothing".
#
# IT IS A LINE AND NOT A NEEDS YOU ITEM, and the distinction is the ruling's.
# A NEEDS YOU item carries two to four options, a recommendation, a DEFAULT and
# a deadline no shorter than 24 hours (RULES_IF_NEEDS_YOU above). The reading
# has none of those and CANNOT have them: there is no default, because a day he
# does not answer is a day the studio does not spend, and that is the rule
# working rather than failing. Putting it through the options-and-deadline
# machinery would manufacture a default for the one question that must not have
# one, so the third part below REFUSES a line carrying those markers.
#
# WHY POSITION IS A PART. "As its first line" is the ruling's own wording, and
# it is the cheapest property in this file to satisfy and the hardest to
# satisfy by accident: a brief cannot drift the ask into the middle where he
# stops reading, and a line that is first cannot also be inside NEEDS YOU, so
# the two halves of the ruling are enforced by one reading.
#
# THE PARTS ARE NAMED, for SPLIT_PARTS' reason one rule up: a single regex over
# a whole sentence that missed the ask would report this rule as passing, and a
# writer told only that "the reading line is wrong" has to guess which half.
READING_PARTS = (
    ("an ask and not a statement, a question mark on the line",
     lambda line: "?" in line),
    ("what he is asked to read, the meter or the usage figure",
     lambda line: bool(re.search(r"\b(meters?|usage)\b", line, re.I))),
    # REFUSING, not requiring: this part is FOUND when the markers are ABSENT.
    ("no option, recommendation, default or deadline on it: it is a line and "
     "not a decision",
     lambda line: not re.search(r"\b(RECOMMENDATION|RECOMMEND|DEFAULT|"
                               r"DEADLINE|OPTION)\b", line, re.I)),
)
# Printed wherever the rule is mentioned. No spaces: it crosses key=value
# channels, and every reader of those splits on whitespace.
READING_RULED_ON = datetime.date(2026, 9, 15)
READING_OWED_BY = "the-brief/its-first-line/ruled-2026-09-15"


def reading_line(text):
    """(the first non-blank line, its 1-based number). ("", 0) for a blank
    message, which is nothing measured and not a line that failed."""
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip():
            return line.strip(), n
    return "", 0


def reading_parts(text):
    """(howManyFound, whichAreMissing, theLineItRead) for the reading ask.

    THE MEASUREMENT LIVES HERE, IN THE TESTED LAYER, for split_parts()' reason:
    driven only through check() a detector ships half-run, and the selftest
    drives this function directly over its fixtures on every run as well as
    through the register.

    POSITION IS MEASURED BY THE CALLER'S CHOICE OF LINE, not by a fourth part:
    this function is handed the first non-blank line, so "it is first" is true
    of whatever it grades. A brief whose ask sits lower down fails because the
    FIRST line is graded and does not ask, and the finding prints both.
    """
    line, _n = reading_line(text)
    missing = [name for name, fn in READING_PARTS if not fn(line)]
    return len(READING_PARTS) - len(missing), missing, line


def check(text, kind="unprompted", now=None, legacy_links=False,
          link_floor=None, research_verbatim=False, pre_move=False,
          pre_reading=False):
    """Every reading this program takes, as data. PURE: takes text, returns a
    dict, touches no file. The selftest drives it with synthetic fixtures and
    the report function only formats what comes out of here.

    `link_floor` is a reading taken by link_floor_state() AT THE CALL SITE,
    because this function reads no file. Passing nothing gets the STRICT
    default: the floor LIVE, with the reason `not-consulted`, so a caller that
    forgot to look can only ever be stricter than the ruling and never looser.
    """
    # `now` may be a datetime, None (meaning the wall clock, which is what the
    # SINGLE-FILE check wants) or UNPINNED (no instant at all, which is what
    # the GATE passes for a file whose name carries no date). Written as an
    # identity test rather than `now or ...` so the sentinel cannot be
    # swallowed by a truthiness change later.
    if now is None:
        now = datetime.datetime.now()
    # THE STRICT DEFAULT. See SERVED_MARKER_REL for why the direction of a
    # missing reading is "refuse loudly" and never "send it anyway".
    if link_floor is None:
        link_floor = floor_reading(True, FLOOR_NOT_CONSULTED)
    word_cap, enforced = REGISTERS[kind]
    # A DECISION CARRIES ITS FLOOR INTO ANY REGISTER. The answer register has
    # no cap and no required shape, but the moment a message carries a NEEDS
    # YOU section it carries Jafar's options-and-deadline floor with it, or a
    # decision buried in a long answer escapes the 24-hour default he ruled.
    # Read off the same section parser the rest of this function uses, so the
    # trigger cannot drift from what the reader sees.
    _bodies_probe, _ = split_sections(text)
    needs_you_present = bool(_bodies_probe.get("NEEDS YOU"))
    if needs_you_present:
        enforced = list(enforced) + [r for r in RULES_IF_NEEDS_YOU
                                     if r not in enforced]
    # THE LINK BAND DOES NOT APPLY TO THE THREE MESSAGES WRITTEN BEFORE IT WAS
    # RULED, and membership of that list is decided BY NAME by the caller (the
    # gate) rather than by anything inside the text. `now` selects no rule at
    # all: it measures deadlines and nothing else.
    if legacy_links:
        enforced = [r for r in enforced if r not in LINK_BAND_RULES]
    # THE VERBATIM RESEARCH EXEMPTION, decided BY NAME by the caller exactly as
    # the line above is, and never by anything inside the text: a document that
    # could talk its way out of the ban list is not an exemption, it is a hole.
    # `waived` is what was ACTUALLY removed, read off this file's own register
    # rather than off the constant, so a rule the register never enforced here
    # cannot be reported as waived. See RESEARCH_VERBATIM for the ruling.
    waived = ([r for r in enforced if r in RESEARCH_WAIVED_RULES]
              if research_verbatim else [])
    if waived:
        enforced = [r for r in enforced if r not in waived]
    # THE FLOOR IS CONDITIONAL SINCE 2026-09-11 AND IT IS NOT DELETED. It drops
    # out of `enforced` while no page is served, which means the existing NOT
    # ENFORCED line names it and the done line's rulesNotEnforced= carries it:
    # a rule that stopped biting in silence reads exactly like a rule that
    # passed. The condition is a fact on disk, read by the caller; the reason is
    # printed beside the branch on every run. See SERVED_MARKER_REL.
    #
    # IT APPLIES TO EVERY REGISTER, including the legacy rung, because the
    # condition is about THE WORLD (no page is served from the new repository)
    # and not about when a message was written. The legacy messages all carry
    # links anyway, so nothing on that rung moves today.
    if "linkfloor" in enforced and not link_floor["active"]:
        enforced = [r for r in enforced if r != "linkfloor"]
    # THE MESSAGES THAT WERE ALREADY SENT WHEN THE SITE MOVED, 2026-09-15,
    # decided BY NAME by the caller exactly as the two exemptions above are.
    # `pre_move_waived` is what was ACTUALLY removed, read off this file's own
    # register rather than off the constant, so a rule this register never
    # enforced cannot be reported as waived and a message on the list that was
    # passing anyway reports a waiver of nothing. See PRE_MOVE_MESSAGES.
    pre_move_waived = ([r for r in enforced if r in PRE_MOVE_WAIVED_RULES]
                       if pre_move else [])
    if pre_move_waived:
        enforced = [r for r in enforced if r not in pre_move_waived]
    # THE BRIEFS WRITTEN BEFORE THE READING ASK WAS RULED, 2026-09-15, decided
    # BY NAME by the caller exactly as the three exemptions above are.
    # `pre_reading_waived` is what was ACTUALLY removed, read off this file's
    # own register rather than off the constant, so a rule this register never
    # enforced (every non-brief kind) cannot be reported as waived. See
    # PRE_READING_BRIEFS.
    pre_reading_waived = ([r for r in enforced if r in PRE_READING_WAIVED_RULES]
                          if pre_reading else [])
    if pre_reading_waived:
        enforced = [r for r in enforced if r not in pre_reading_waived]
    # THE CAP GOVERNS THE BODY THE PRODUCER WROTE. On the frozen legacy list
    # only, one leading HISTORICAL, line is an annotation the studio added
    # afterwards and is not charged to the writer: see historical_split() and
    # the ruling at LEGACY_LINK_RULES. EXCLUDED FROM THE WORD COUNT AND FROM
    # NOTHING ELSE. Every other rule in this function reads `text`, so the
    # annotation still faces the ban list, the link rules and the shape rules.
    historical, capped_body = historical_split(text, legacy_links)
    words = count_words(capped_body)
    scrubbed = scrub_links(text)
    found, notes = [], []
    urls = links_in(text)
    # EVERY DESTINATION TEST IN THIS FUNCTION READS THE SAME INSTANT. A second
    # call site using today's list while the first used the dated one would
    # report a message as both compliant and not.
    good_links = [u for u in urls if link_ok(u, legacy_links)]
    # THE RULED WHOLE-URL EXCEPTION, PER MESSAGE. `ruled_matched` is the URLs in
    # THIS message that matched an entry on the frozen tuple (per message, never
    # cumulative: the gate's own line carries the walk), read off the same
    # ruled_link() every destination test above uses.
    ruled_matched = [u for u in urls if ruled_link(u) is not None]
    ruled_labels = sorted({ruled_link(u) for u in ruled_matched})

    # 1. THE WORD CAP.
    if "wordcap" in enforced and len(words) > word_cap:
        found.append(Finding("wordcap", "%d words over the %d cap (%d words)"
                             % (len(words) - word_cap, word_cap, len(words))))

    # 2. THE BANNED TOKENS.
    banned_checked = 0
    if "banned" in enforced:
        rules = list(BANNED)
        if kind not in COUNTS_ALLOWED_IN:
            rules.append(("count", find_counts))
        else:
            notes.append("counts are permitted in the %s register (his "
                         "question sets what is answered), so that pattern "
                         "did not run" % kind)
        banned_checked = len(rules)
        for label, fn in rules:
            hits = fn(scrubbed)
            if hits:
                found.append(Finding("banned:" + label,
                                     cap(hits, keep=FINDINGS_SHOWN, width=40,
                                         sep=", ")))

    # 3. THE LINK FLOOR.
    sents = sentences(text)
    claims = [(s, sec, ln) for s, sec, ln in sents if claim_shaped(s, ln)]
    if "linkfloor" in enforced:
        # UNCONDITIONAL for the unprompted and brief registers, ruled
        # 2026-09-03. It used to fire only `if claims and not good_links`, so
        # the one rule carrying constitution law 12 was the PERMISSIVE one
        # while the stylistic bans were aggressive: a message whose claims the
        # verb list failed to recognise sailed through with no link at all.
        # Claim detection under-flags by construction (a closed verb list
        # cannot see "the street looks right"), so hanging the evidence floor
        # off it inherited that blindness. The floor now asks only whether a
        # message that says anything carries a link.
        if len(good_links) < LINK_MIN:
            where = "; ".join(u for u in urls[:2]) or "no URL at all"
            found.append(Finding(
                "linkfloor",
                "no link to any of the %d published page(s) (%s) and none to "
                "the %d ruled whole-URL entry/entries either. What it carries "
                "instead: %s. %d sentence(s) read "
                "as claim-shaped, and the floor does NOT depend on that count: "
                "law 12 requires the evidence behind any message that speaks. "
                "First claim, if any: %s" % (
                    len(SITE_PAGES), site_destination_words(", "),
                    len(RULED_LINKS), where, len(claims),
                    cap([claims[0][0]], keep=1, width=60) if claims
                    else "none recognised, which is not the same as none")))
    # ADVISORY, never a rejection: the ruled floor is one link in the message.
    # Per-section linkage is the stronger reading of "every claim links", and
    # it is printed with its denominator so a bound can be read off real
    # messages later rather than guessed at now.
    linked_sections = {sec for sec, in [(s,) for s in []]}
    by_section = {}
    for s, sec, ln in sents:
        by_section.setdefault(sec, []).append(s)
    linked_sections = {sec for sec, ss in by_section.items()
                       if any(link_ok(u, legacy_links) for t in ss
                              for u in links_in(t))}
    # links live on the LINE, not the sentence, so re-derive from lines
    linked_sections = set()
    cur = "(before any section)"
    for line in text.splitlines():
        head = section_label(line)
        if head:
            cur = head
        if any(link_ok(u, legacy_links) for u in links_in(line)):
            linked_sections.add(cur)
    unlinked_claims = [c for c in claims if c[1] not in linked_sections]

    # 3b. THE LINK BAND AND THE DESTINATION, ruled 2026-09-06. The floor above
    # counts SITE links; these two count every URL in the message, because "at
    # most two links" is about what he has to read past, not about which of
    # them are good ones.
    if "linkcap" in enforced and len(urls) > LINK_MAX:
        found.append(Finding(
            "linkcap",
            "%d link(s), %d over the ruled cap of %d per message. Ruled "
            "2026-09-06: at most two links, everything else said in plain "
            "words. Over the cap: %s"
            % (len(urls), len(urls) - LINK_MAX, LINK_MAX,
               cap(urls[LINK_MAX:], keep=FINDINGS_SHOWN, width=60, sep=" | "))))
    if "linkdest" in enforced:
        offsite = [u for u in urls if not link_ok(u, legacy_links)]
        if offsite:
            found.append(Finding(
                "linkdest",
                "%d of %d link(s) point somewhere other than the %d published "
                "page(s) (%s) or the %d ruled whole-URL entry/entries. Ruled "
                "2026-09-06: never to a repository "
                "markdown file, and a picture goes to him as a Telegram image "
                "rather than as a link. A URL admitted by a ruling is matched "
                "by whole string and never by prefix, so the parent directory "
                "of a ruled URL and any file under it are both refused. "
                "Offending: %s"
                % (len(offsite), len(urls), len(SITE_PAGES),
                   site_destination_words(", "), len(RULED_LINKS),
                   cap(offsite, keep=FINDINGS_SHOWN, width=60, sep=" | "))))

    # 4. THE SHAPE. REQUIRED sections are per register (SECTIONS_REQUIRED);
    # the ORDER is checked against every known label, so a section that is
    # permitted but not required still has to sit where it was ruled to sit.
    bodies, order = split_sections(text)
    wanted_sections = required_sections(kind)
    if "shape" in enforced:
        missing = [s for s in wanted_sections if s not in bodies]
        if missing:
            found.append(Finding("shape", "missing section(s): %s"
                                 % cap(missing, keep=5, sep=", ")))
        seen = [s for s in order if s in SECTIONS]
        first_seen = []
        for s in seen:
            if s not in first_seen:
                first_seen.append(s)
        wanted = [s for s in SECTIONS if s in first_seen]
        if first_seen != wanted:
            found.append(Finding("shape", "sections out of order: got %s, "
                                          "ruled order is %s"
                                 % ("/".join(first_seen), "/".join(wanted))))

    # 5. THE NEEDS YOU ITEMS.
    items = needs_you_items(bodies.get("NEEDS YOU", []))
    if "options" in enforced:
        for i, item in enumerate(items, 1):
            n = len(item["options"])
            if not (MIN_OPTIONS <= n <= MAX_OPTIONS):
                found.append(Finding("options", "item %d has %d option(s), "
                                     "ruled range is %d..%d"
                                     % (i, n, MIN_OPTIONS, MAX_OPTIONS)))
            for need in ("recommendation", "default"):
                if not item[need]:
                    found.append(Finding("options", "item %d states no %s"
                                         % (i, need)))
    if "deadline" in enforced:
        for i, item in enumerate(items, 1):
            if not item["deadline"]:
                found.append(Finding("deadline", "item %d states no deadline"
                                     % i))
                continue
            if now is UNPINNED:
                # A DEADLINE NOBODY CAN MEASURE IS NOT A DEADLINE THAT PASSED.
                # The gate pins its clock to the date in the filename; a name
                # with no date leaves it nothing to measure from, and the
                # honest outcome is a finding naming the fix rather than a
                # silent skip. This is what stops "drop the date from the
                # filename" becoming the way round the floor.
                found.append(Finding("deadline", "item %d states a deadline "
                                     "and this file's name carries no date to "
                                     "measure it from, so the %d-hour floor "
                                     "could not be read at all. Name the file "
                                     "<YYYY-MM-DD>-<slug>.<kind>.md"
                                     % (i, MIN_DEADLINE_HOURS)))
                continue
            hrs = deadline_hours(item["deadline"], now)
            if hrs is None:
                found.append(Finding("deadline", "item %d states a deadline "
                                     "this check cannot parse: %s"
                                     % (i, cap([item["deadline"]], keep=1,
                                               width=50))))
            elif hrs < MIN_DEADLINE_HOURS:
                found.append(Finding("deadline", "item %d gives %.1f hour(s), "
                                     "under the ruled %d"
                                     % (i, hrs, MIN_DEADLINE_HOURS)))

    # 6. NEXT VISIBLE THING: a measured time, or the word unknown. Never a
    # padded guess, and never a blank, which reads as unknown without saying so.
    if "nextvisible" in enforced:
        body = " ".join(bodies.get("NEXT VISIBLE THING", [])).strip()
        if "NEXT VISIBLE THING" in bodies and not TIME_FORMS.search(body):
            found.append(Finding("nextvisible",
                                 "neither a time nor the word unknown: %s"
                                 % (cap([body], keep=1, width=60) if body
                                    else "the section is empty")))

    # 7. THE STUDIO VERSUS GAME SPLIT, in the BUDGET section, in words.
    # ENFORCED IN NO REGISTER SINCE 2026-09-09: retired from the brief by the
    # ruling block at SECTIONS_RETIRED_IN_BRIEF, never applied to the other two.
    # `split_found` is None when nothing measured it, NOT 0: a zero here would
    # read as five parts looked for and none found, which is a different fact
    # from a rule that did not run. report() prints the words accordingly.
    split_found, split_missing = None, [name for name, _ in SPLIT_PARTS]
    if "split" in enforced:
        budget_body = " ".join(bodies.get("BUDGET", [])).strip()
        split_found, split_missing = split_parts(budget_body)
        if split_missing:
            found.append(Finding(
                "split",
                "the BUDGET section carries %d of %d required part(s) of the "
                "studio-versus-game split: missing %s. Jafar's standing order "
                "of 2026-09-05 requires the split in every brief, in words, "
                "counted in sessions, saying it is sessions and not points "
                "until the rate is measured"
                % (split_found, len(SPLIT_PARTS),
                   cap(split_missing, keep=5, sep=", ")),
                "BUDGET" if budget_body else "the section is empty"))

    # 8. THE READING LINE, ruled by Jafar 2026-09-15. See READING_PARTS for the
    # ruling and for why position is one of the readings. ENFORCED IN THE BRIEF
    # REGISTER ONLY (RULES_BRIEF_ONLY), so every other register names it under
    # NOT ENFORCED rather than skipping it in silence.
    # `reading_found` is None when nothing measured it, NOT 0, for the reason
    # written at `split_found` one rule up: a zero would read as three parts
    # looked for and none found, which is a different fact from a rule that
    # did not run.
    reading_found, reading_missing = None, [n for n, _ in READING_PARTS]
    read_line, read_line_no = reading_line(text)
    if "reading" in enforced:
        reading_found, reading_missing, read_line = reading_parts(text)
        if reading_missing:
            found.append(Finding(
                "reading",
                "the first line of this brief does not ask Jafar for his "
                "budget reading: it carries %d of %d required part(s) and is "
                "missing %s. Ruled 2026-09-15: the brief asks for the reading "
                "as its FIRST line, every morning, and the studio holds at "
                "inbox only until he answers. It is a LINE and not a NEEDS YOU "
                "item: no options, no recommendation, no default and no "
                "deadline, because a day he does not answer is a day the "
                "studio does not spend. The line this rule graded, which is "
                "line %d: %s"
                % (reading_found, len(READING_PARTS),
                   cap(reading_missing, keep=5, sep="; "), read_line_no,
                   cap([read_line], keep=1, width=60) if read_line
                   else "the message is blank, which is nothing measured"),
                "line %d" % read_line_no if read_line_no
                else "the message is blank"))

    return {
        # WHICH CLOCK PRODUCED THE DEADLINE READING, carried out of the pure
        # function so the report never has to guess which of the two callers
        # it is serving.
        "now": "unpinned/no-date-in-filename" if now is UNPINNED
               else now.isoformat(timespec="minutes"),
        "kind": kind, "cap": word_cap, "words": len(words),
        "sentences": len(sents), "claims": len(claims),
        "unlinked_claims": len(unlinked_claims),
        "unlinked_examples": [c[0] for c in unlinked_claims],
        # THREE SECTION READINGS, NAMED, because one count cannot carry them:
        # what the message has (of every known label), what THIS register
        # demands, and which labels it retired and therefore did not demand.
        "sections_found": [s for s in SECTIONS if s in bodies],
        "sections_required": list(wanted_sections),
        "sections_required_found": [s for s in wanted_sections if s in bodies],
        "sections_retired": [s for s in SECTIONS if s not in wanted_sections],
        "sections_retired_present": [s for s in SECTIONS
                                     if s not in wanted_sections
                                     and s in bodies],
        "items": len(items), "urls": urls, "good_links": good_links,
        "link_min": LINK_MIN, "link_max": LINK_MAX,
        # THE BRANCH THE FLOOR TOOK, AND WHY, carried out of the pure function
        # so the report never has to re-read the marker and can never disagree
        # with the rule that ran. `link_min_effective` is the RULED floor when
        # the floor is live and 0 while it is suspended: the pair of it and
        # `link_min` is the before/after a reader needs, never one number whose
        # meaning moved underneath them.
        "link_floor_active": link_floor["active"],
        "link_floor_reason": link_floor["reason"],
        "link_floor_marker": link_floor["marker"],
        "link_floor_served": link_floor["served"],
        # A1, PRINTED ON THIS PATH AND DECISIVE ONLY AT THE GATE: the sender on
        # his PC must not be where a stale-link-forcing marker is discovered.
        "marker_origin_ok": marker_origin_consistent(link_floor,
                                                     SITE_ORIGIN)[0],
        # READ OFF THE REGISTER THIS MESSAGE WAS ACTUALLY GRADED BY, never off
        # the marker alone: since 2026-09-15 the floor can also drop out
        # PER FILE (PRE_MOVE_MESSAGES), and a number derived from the marker
        # would keep saying 1 for a file graded at 0.
        "link_min_effective": LINK_MIN if "linkfloor" in enforced else 0,
        "offsite_links": [u for u in urls if not link_ok(u, legacy_links)],
        "link_generation": link_rule_generation(legacy_links, ruled_labels),
        # WHICH of the published pages this message actually links, named. A
        # link accepted under the OLDER generation is not one of them, so it
        # contributes no label and is counted in `good_links` only.
        "site_labels": sorted({site_page(u) for u in good_links
                               if site_page(u) is not None}),
        # THE THREE WAYS A URL CAN BE ADMITTED, COUNTED SEPARATELY, so the
        # report's arithmetic closes: site + ruled + retired-host + offsite is
        # every URL in the message. `good_links` is the first three together and
        # on its own cannot tell a link to the gallery from a link admitted by
        # the ruled exception.
        "site_links": [u for u in urls if site_page(u) is not None],
        "retired_host_links": [u for u in good_links
                               if site_page(u) is None
                               and ruled_link(u) is None],
        # PER MESSAGE, not cumulative: how many of this message's URLs matched a
        # frozen RULED_LINKS entry, which of them, and how many entries there
        # were to match. The zero ships that denominator: 0 of 1 says the
        # exception existed and this message did not use it.
        "ruled_used": len(ruled_matched),
        "ruled_labels": ruled_labels,
        "ruled_of": len(RULED_LINKS),
        # THE LINK BAND'S TWO RULES DID NOT APPLY TO THIS FILE, because it is
        # named in LEGACY_LINK_RULES. Printed, never silent: a rule skipped in
        # silence is indistinguishable from a rule that passed.
        "legacy_links": legacy_links,
        # PER MESSAGE, not cumulative: whether this file was graded under the
        # verbatim research exemption, and WHICH rule(s) it actually removed
        # from this file's register. The pair is one reading: membership alone
        # would not say the exemption did anything, and the walk's own count is
        # on the gate's done line.
        "research_verbatim": bool(research_verbatim),
        "research_waived": list(waived),
        # PER MESSAGE, not cumulative, and the SAME PAIR the research exemption
        # prints: whether this file was named on PRE_MOVE_MESSAGES, and WHICH
        # rule(s) that actually removed from its register. Membership alone
        # would not say the waiver did anything; the walk's counts are on the
        # gate's report lines. See PRE_MOVE_MESSAGES for the ladder this list
        # was read off.
        "pre_move": bool(pre_move),
        "pre_move_waived": list(pre_move_waived),
        # PER MESSAGE, not cumulative, and the SAME PAIR the other three
        # waivers print: whether this file was named on PRE_READING_BRIEFS,
        # and WHICH rule(s) that actually removed from its register.
        "pre_reading": bool(pre_reading),
        "pre_reading_waived": list(pre_reading_waived),
        # THE ANNOTATION THE CAP DID NOT CHARGE FOR: per message, 0 or 1, with
        # the words it would have cost. Printed by report() and counted by the
        # gate, never silent, so "118 of 120" cannot be read without the line
        # that is not in it. `historical_eligible` is the denominator of the
        # per-message zero: this file COULD have carried one.
        "historical_uncounted": 1 if historical else 0,
        "historical_words": len(count_words(historical)) if historical else 0,
        "historical_eligible": bool(legacy_links),
        "split_found": split_found, "split_of": len(SPLIT_PARTS),
        "split_missing": split_missing,
        # THE READING ASK: how many of its parts were found, out of how many,
        # which are missing, and THE LINE THE RULE ACTUALLY GRADED with its
        # number. The line and its number travel together because "it asks"
        # and "it asks FIRST" are two readings and a reader given only the
        # first cannot tell a brief that buried the ask from one that has none.
        "reading_found": reading_found, "reading_of": len(READING_PARTS),
        "reading_missing": reading_missing,
        "reading_line": read_line, "reading_line_no": read_line_no,
        # WHAT THE ASK COSTS THE CAP, measured off the line the rule graded and
        # never a typed constant. MEASURED ON THE LIVE CORPUS 2026-09-15: the
        # ask is 9 words, the 17 brief-kind files in the tree run 106 to 150
        # words with a median of 146, and 14 of the 17 would cross the 150 cap
        # with it. So "157 of 150" must never be readable without the part of
        # it that is mandatory; the pair is printed on one line below.
        "reading_line_words": len(count_words(read_line)) if read_line else 0,
        "banned_checked": banned_checked,
        "enforced": list(enforced),
        "not_enforced": [r for r in RULES if r not in enforced],
        "findings": found, "notes": notes,
    }


OPTION_RE = re.compile(r"^\s*(?:[-*]\s*)?([A-D])[.)]\s+\S")
REC_RE = re.compile(r"^\s*(?:[-*]\s*)?RECOMMEND", re.I)
DEF_RE = re.compile(r"^\s*(?:[-*]\s*)?DEFAULT", re.I)
DEAD_RE = re.compile(r"^\s*(?:[-*]\s*)?DEADLINE", re.I)


def needs_you_items(lines):
    """The NEEDS YOU section as items. An item ENDS at its DEADLINE line, which
    is the ruled last part of one; a trailing chunk with no deadline is still
    an item and is reported as missing one rather than dropped. A section whose
    body carries no option, no recommendation and no deadline is an EMPTY
    needs-you (the honest 'nothing needs you today') and yields no items."""
    items, cur = [], None

    def fresh():
        return {"options": [], "recommendation": None, "default": None,
                "deadline": None, "lines": []}

    for line in lines:
        if not line.strip():
            continue
        if cur is None:
            cur = fresh()
        cur["lines"].append(line)
        m = OPTION_RE.match(line)
        if m:
            cur["options"].append(m.group(1))
        if REC_RE.match(line):
            cur["recommendation"] = line.strip()
        if DEF_RE.match(line):
            cur["default"] = line.strip()
        if DEAD_RE.match(line):
            cur["deadline"] = line.strip()
            items.append(cur)
            cur = None
    if cur and (cur["options"] or cur["recommendation"] or cur["default"]):
        items.append(cur)
    return items


# ------------------------------------------------------------------- reporting

def research_bit_key(r):
    """The `researchVerbatimWaiverBit=` value for a gate done line. PURE.

    THE DENOMINATOR IS THE FILES THE WAIVER COULD HAVE BITTEN ON, which is the
    listed files this walk actually graded, and when that is zero the value is
    the WORDS. `0/0` would be a zero nobody can read: a walk where no listed
    delivery was present and a walk where five were present and the exemption
    changed nothing are different facts with the same digits.
    """
    if not r["research_graded"]:
        return "%s/no-listed-delivery-in-this-walk" % NOTHING
    return "%d/%d" % (r["research_waiver_bit"], r["research_graded"])


def research_key(r):
    """The `researchVerbatimWaived=` value for a done line. PURE, one word.

    ONE ENTRY CARRYING BOTH MOMENTS: what the exemption actually waived on this
    file, and whether this file is on the list at all, so no reader has to join
    two keys to learn that "none" meant "not exempt" rather than "exempt and it
    changed nothing". Structure is `..` and `/` because every reader of a
    key=value channel here splits on whitespace.
    """
    listed = ("listed-1-of-%d" % len(RESEARCH_VERBATIM)
              if r["research_verbatim"]
              else "not-on-the-%d-name-list" % len(RESEARCH_VERBATIM))
    return "%s..%s" % ("/".join(r["research_waived"]) or "none", listed)


def report(r):
    """The report. Every zero here ships the denominator that produced it."""
    print("producer-check: register=%s" % r["kind"])
    if r["cap"] is None:
        print("  words: %d (no cap in this register; his question sets the "
              "length)" % r["words"])
    else:
        print("  words: %d of %d (URLs excluded from the count: the link floor "
              "requires them)" % (r["words"], r["cap"]))
    # THE EXCLUSION IS NEVER SILENT. A message that passed with a line
    # uncounted must read differently from one that passed with every line
    # counted, and the zero ships its denominator: eligible-and-none.
    if r["historical_eligible"]:
        if r["historical_uncounted"]:
            print("  historical annotation: 1 leading %s line of %d word(s) "
                  "NOT charged to the cap above, ruled 2026-09-06. The cap "
                  "governs what the Producer wrote; the marker was added "
                  "afterwards by the studio. Excluded from the count and from "
                  "nothing else: the ban list, the link rules and the shape "
                  "rules all read it"
                  % (HISTORICAL_PREFIX, r["historical_words"]))
        else:
            print("  historical annotation: 0 line(s) excluded of the 1 this "
                  "file is eligible for; its first line does not begin %s, so "
                  "every word above is counted" % HISTORICAL_PREFIX)
    # THE DENOMINATOR IS THIS REGISTER'S REQUIRED LIST, not every label this
    # parser knows: since 2026-09-09 those differ for the brief, and "4 of 5"
    # against the vocabulary would report a complete brief as short one section.
    print("  examined: %d sentence(s), %d claim-shaped, %d NEEDS YOU item(s), "
          "%d of the %d section(s) this register requires, %d label(s) present "
          "in all (%s)"
          % (r["sentences"], r["claims"], r["items"],
             len(r["sections_required_found"]), len(r["sections_required"]),
             len(r["sections_found"]),
             "/".join(r["sections_found"]) or NOTHING))
    # THE RETIREMENT ANNOUNCES ITSELF ON EVERY RUN, with the section's own state
    # beside it, because a requirement that vanished in silence reads exactly
    # like a requirement that was met.
    if r["sections_retired"]:
        print("  retired from this register on %s and therefore NOT required, "
              "still permitted and still order-checked: %s. The "
              "studio-versus-game split that lived in BUDGET is owed by %s"
              % (SPLIT_RETIRED_ON.isoformat(),
                 "/".join("%s=%s" % (s, "present"
                                     if s in r["sections_retired_present"]
                                     else "absent")
                          for s in r["sections_retired"]),
                 SPLIT_OWED_BY))
    # THE FOUR COUNTS ADD TO THE TOTAL, deliberately. This line used to print
    # len(good_links) as "to the site", which was true while the site list was
    # the only way in and became a false claim with a number on it the day a
    # whole URL was admitted by ruling.
    # THE PAIRED READING: the RULED band and the band that actually applied on
    # this run, on one line. "0 URL(s) of the ruled 1..2" read alone is a
    # violation; the pair is what the reader needs, and the link floor line
    # below carries the reason the two differ.
    print("  links: %d URL(s) of the ruled %d..%d (effective this run %d..%d, "
          "see the link floor line below): %d to the site (%s), %d by "
          "the ruled whole-URL exception, %d admitted by the retired host "
          "list, %d elsewhere. The only %d destination(s) allowed are %s under "
          "%s; a picture is sent as a Telegram image and never as a link"
          % (len(r["urls"]), r["link_min"], r["link_max"],
             r["link_min_effective"], r["link_max"],
             len(r["site_links"]),
             "/".join(l for l in r["site_labels"] if l) or NOTHING,
             r["ruled_used"], len(r["retired_host_links"]),
             len(r["offsite_links"]), len(SITE_PAGES),
             site_destination_words("/"), SITE_ORIGIN))
    # THE EXCEPTION IS NEVER SILENT, and its zero ships the denominator that
    # makes it readable: 0 of 1 is a message that did not use an exception that
    # exists, which is not the same reading as no exception existing at all.
    # PER MESSAGE; the gate's linksRuledUsed line is the walk.
    print("  ruled whole-URL exception: %d of this message's %d URL(s) matched "
          "one of the %d frozen RULED_LINKS entry/entries (%s), by whole-string "
          "equality and never by prefix. Each entry names the record that "
          "admits it and the rung that deletes it"
          % (r["ruled_used"], len(r["urls"]), r["ruled_of"],
             "/".join(r["ruled_labels"]) or NOTHING))
    print("  destination list applied: %s (the list is dated because the "
          "floor is older than today's ruling)" % r["link_generation"])
    # THE FLOOR'S BRANCH AND ITS REASON, ON EVERY RUN, pass or fail, so nobody
    # has to read tools/producer-check.py to know whether the floor was live.
    # THE PAIRED READING: whether it applied and the effective floor it applied
    # at, on ONE line, never two keys whose relationship the reader carries.
    print("  link floor: linkFloorActive=%s reason=%s. Effective floor on this "
          "run: %d link(s) at least, %d at most, against the ruled %d..%d. "
          "Ruled 2026-09-10 (queue 256, queue 259): zero links is legal WHILE "
          "no page is served from the new repository, because all %d permitted "
          "destinations sit under the ARCHIVE's pages and a link would show "
          "him the world as it was before the move. The floor is NOT deleted "
          "and returns to %d..%d the run after %s names a served commit"
          % ("true" if r["link_floor_active"] else "false",
             r["link_floor_reason"], r["link_min_effective"], r["link_max"],
             r["link_min"], r["link_max"], len(SITE_PAGES),
             r["link_min"], r["link_max"], r["link_floor_marker"]))
    print("  claim-shaped means: not a question, the line does not begin with "
          "a section label or an option / recommendation / default / deadline "
          "marker, and the sentence carries a finite assertion verb")
    if r["banned_checked"]:
        print("  ban list: %d pattern(s) run over the message with URLs "
              "removed" % r["banned_checked"])
    if "split" in r["enforced"]:
        print("  studio-versus-game split: %d of %d required part(s) found in "
              "BUDGET (%s). Ruled 2026-09-05: in words, counted in sessions, "
              "and not points until the rate is measured"
              % (r["split_found"], r["split_of"],
                 ", ".join(n for n, _ in SPLIT_PARTS)))
    else:
        # NOT "0 of 5". Nothing measured it, and the words say so, or a reader
        # would take a retired rule for a rule this message failed clean.
        print("  studio-versus-game split: %s, the rule is enforced in no "
              "register since %s (retired from the brief by Jafar's director "
              "test of that day, never applied to the other two). His order of "
              "2026-09-05 stands and the number is owed by %s; the %d-part "
              "detector is kept and is driven by the selftest on every run"
              % (NOTHING.replace("-", " "), SPLIT_RETIRED_ON.isoformat(),
                 SPLIT_OWED_BY, r["split_of"]))
    if "reading" in r["enforced"] and r["cap"] is not None:
        print("  of the %d word(s) above, %d are the mandatory reading ask on "
              "line %d, leaving %d of the %d cap for what the Producer chose "
              "to write. Both halves on one line because a count over the cap "
              "cannot be read without the part of it nobody may cut"
              % (r["words"], r["reading_line_words"], r["reading_line_no"],
                 r["cap"] - r["reading_line_words"], r["cap"]))
    if "reading" in r["enforced"]:
        print("  the reading ask: %d of %d required part(s) found on line %d, "
              "which is the first non-blank line and the only one this rule "
              "grades (%s). Ruled 2026-09-15: the brief asks for the meter "
              "reading as its first line and the studio holds at inbox only "
              "until he answers. No default and no deadline belong on it"
              % (r["reading_found"], r["reading_of"], r["reading_line_no"],
                 "; ".join(n for n, _ in READING_PARTS)))
    else:
        # NOT "0 of 3". Nothing measured it in this register, and the words say
        # so, or a reader takes a rule that did not run for a rule this message
        # passed. The brief register is named, so the reader knows where it does
        # bite rather than only that it did not bite here.
        print("  the reading ask: %s, the rule is enforced in the brief "
              "register only (ruled %s) and this is the %s register. Where it "
              "binds it is owed by %s; the %d-part detector is kept and is "
              "driven by the selftest on every run"
              % (NOTHING.replace("-", " "), READING_RULED_ON.isoformat(),
                 r["kind"], READING_OWED_BY, r["reading_of"]))
    if "deadline" in r["enforced"]:
        # TWO CALLERS, TWO CLOCKS, so neither may leave its instant implicit.
        # This path is the SINGLE-FILE check and its clock is the wall clock:
        # the question before sending is "is this deadline far enough away to
        # send", which is a question about now. The gate's clock is the date in
        # the file's own name, and it says so on its own line.
        print("  deadlines measured from %s, the wall clock unless --now was "
              "given: before sending, the question is about now" % r["now"])
    for n in r["notes"]:
        print("  note: %s" % n)
    if r["not_enforced"]:
        print("  NOT ENFORCED in this register, named rather than skipped in "
              "silence: %s%s"
              % (", ".join(r["not_enforced"]),
                 (" (%s: legacy link rules by name, this file is one of the "
                  "%d on the frozen LEGACY_LINK_RULES list in "
                  "tools/producer-check.py, written before the band was "
                  "ruled)" % (" and ".join(LINK_BAND_RULES),
                              len(LEGACY_LINK_RULES)))
                 if r["legacy_links"] else ""))

    # THE VERBATIM EXEMPTION IS NEVER SILENT, and the zero ships its
    # denominator: a file on the list that waived nothing reads differently
    # from a file that waived the ban list. Denominator is the frozen list,
    # because that is the only set this exemption can ever be claimed from.
    if r["research_verbatim"]:
        print("  verbatim research delivery: %s waived for this file, 1 of "
              "the %d name(s) on the frozen RESEARCH_VERBATIM list in "
              "tools/producer-check.py. Ruled 2026-09-14: a research "
              "SUMMARY goes to him IN FULL, and the ban list cannot tell a "
              "CI job from the man whose job it is. Waived here: %s. Every "
              "other rule in this register still binds"
              % ("/".join(RESEARCH_WAIVED_RULES), len(RESEARCH_VERBATIM),
                 "/".join(r["research_waived"]) or NOTHING))

    if r["claims"]:
        print("  advisory, not a rejection: %d of %d claim-shaped sentence(s) "
              "sit in a section carrying no link (%s). The ruled floor is one "
              "link in the message; this is the series a stricter bound would "
              "be read off later"
              % (r["unlinked_claims"], r["claims"],
                 cap(r["unlinked_examples"], keep=2, width=40, sep=" | ")))
    else:
        print("  advisory: %s for per-section linkage, because no sentence in "
              "this message is claim-shaped" % NOTHING)

    print("")
    if not r["findings"]:
        print("  0 finding(s) over %d rule(s) enforced (%s) and %d word(s) "
              "examined" % (len(r["enforced"]), ",".join(r["enforced"]),
                            r["words"]))
        print("  MECHANICAL ONLY: nothing here read whether a claim is TRUE, "
              "whether the link shows what the sentence says, or whether the "
              "recommendation is any good. That is the director's read.")
        # THE PAIR ON ONE LINE: how many rules ran, out of how many exist, AND
        # which ones did not. rulesEnforced=9/10 on its own sends the reader
        # looking for the tenth; the names have no spaces so every reader that
        # splits on whitespace keeps them whole.
        # linkFloorActive and its reason sit LAST and ADJACENT: the pair is one
        # reading, and the reason is the only token here that can grow, so a
        # reader truncating the line loses the explanation rather than a count.
        print("\nproducer-check: SEND register=%s rulesEnforced=%d/%d "
              "rulesNotEnforced=%s researchVerbatimWaived=%s "
              "markerOriginConsistent=%s "
              "linkFloorActive=%s reason=%s"
              % (r["kind"], len(r["enforced"]), len(RULES),
                 "/".join(r["not_enforced"]) or "none", research_key(r),
                 "true" if r["marker_origin_ok"] else "false",
                 "true" if r["link_floor_active"] else "false",
                 r["link_floor_reason"]))
        return 0
    shown = {}
    for f in r["findings"]:
        shown.setdefault(f.rule, []).append(str(f.what))
    print("  %d finding(s) over %d rule(s) enforced:" % (len(r["findings"]),
                                                         len(r["enforced"])))
    for rule in sorted(shown):
        print("    %-18s %s" % (rule, cap(shown[rule], keep=FINDINGS_SHOWN,
                                          width=110, sep=" | ")))
    print("\nproducer-check: DO NOT SEND register=%s rulesEnforced=%d/%d "
          "rulesNotEnforced=%s researchVerbatimWaived=%s "
          "markerOriginConsistent=%s "
          "linkFloorActive=%s reason=%s"
          % (r["kind"], len(r["enforced"]), len(RULES),
             "/".join(r["not_enforced"]) or "none", research_key(r),
             "true" if r["marker_origin_ok"] else "false",
             "true" if r["link_floor_active"] else "false",
             r["link_floor_reason"]))
    return 1


# ------------------------------------------------------------------- selftest

# THE ACCEPTING FIXTURE: a real compliant message about this project's real
# state on 2026-09-03, written in the ruled register. It is first, and it is
# the case that matters: the expensive failure here is a register check nothing
# survives, which would push every future message back to being written with no
# check at all.
GOOD = """HEADLINE: the town has textures again, and the street is worth a look.

WHAT CHANGED: the grey street now paints properly, and the first picture of it
is up. Everything else waited on that.
[the gallery](https://jsab258.github.io/ledger/gallery.html)

NEEDS YOU: how close should strangers stand on a pavement?
A. Almost touching, a crowded market.
B. Normal British pavement distance.
C. Reserved, a town that keeps its distance.
RECOMMENDATION B, a working port town rather than a festival.
DEFAULT B if you say nothing.
DEADLINE 2026-09-07.
[where things stand](https://jsab258.github.io/ledger/)

NEXT VISIBLE THING: a walk through that street, tomorrow evening.

BUDGET: £0 spent, well inside the month.
"""

# THE REJECTING FIXTURES ARE SYNTHETIC, every one of them, and none quotes a
# real message. A rejecting case pinned to a real asset breaks the day somebody
# fixes the asset.
BAD = {
    "banned:file path":
        GOOD.replace("the grey street now paints properly",
                     "production/queue/062-uv-chain.md is the blocker"),
    "banned:verdict key":
        GOOD.replace("Everything else waited on that.", "probeTest=PASS now."),
    "banned:count":
        GOOD.replace("Everything else waited on that.",
                     "563 of 593 objects carry textures."),
    "banned:run internals":
        GOOD.replace("Everything else waited on that.",
                     "The workflow went green on the runner."),
    "banned:tool narration":
        GOOD.replace("Everything else waited on that.",
                     "I checked the street myself."),
    "banned:heartbeat":
        GOOD.replace("Everything else waited on that.",
                     "Still working, quick update for you."),
    "banned:self-correction":
        GOOD.replace("Everything else waited on that.",
                     "My mistake, earlier I said it was done."),
    "wordcap":
        GOOD.replace("Everything else waited on that.",
                     "Everything else waited on that. " + ("and " * 130)),
    "linkfloor": re.sub(r"\[[^\]]*\]\([^)]*\)\n?", "", GOOD),
    # ONE MORE LINK THAN THE CAP, and it is a legal destination: the cap is
    # about how much he has to read past, not about where the links go, and a
    # fixture that broke both rules would prove neither.
    "linkcap": GOOD.replace(
        "NEXT VISIBLE THING: a walk through that street, tomorrow evening.",
        "NEXT VISIBLE THING: a walk through that street, tomorrow evening.\n"
        "[the map](https://jsab258.github.io/ledger/map.html)"),
    # A REPOSITORY MARKDOWN LINK, which is exactly what Jafar rejected. The
    # other site link stays, so the floor is satisfied and only the
    # destination rule can fire.
    "linkdest": GOOD.replace(
        "[the gallery](https://jsab258.github.io/ledger/gallery.html)",
        "[the card](https://github.com/jsab258/wc26-picks/blob/main/q.md)"),
    "shape": GOOD.replace("BUDGET:", "MONEY:"),
    "options": GOOD.replace("B. Normal British pavement distance.\n", "")
                   .replace("C. Reserved, a town that keeps its distance.\n", ""),
    "deadline": GOOD.replace("DEADLINE 2026-09-07.", "DEADLINE 2026-09-03."),
    "nextvisible": GOOD.replace("a walk through that street, tomorrow evening.",
                                "something good, soon, you will like it."),
}

# THE BRIEF FIXTURES. A brief is the same shape with a BUDGET section that
# carries the studio-versus-game split IN WORDS: no digits, because the ban
# list refuses bare counts in anything Jafar reads, and no `splitBasis=`,
# because that is a verdict key and lives on the tool's done line.
BRIEF_SPLIT = ("BUDGET: your newest reading was seven percent on the meter "
               "that governs, taken today. Nine sessions went to the studio "
               "and two to the game since the previous brief, counted in "
               "sessions and not points until the rate is measured.")
# THE READING ASK, ruled 2026-09-15 and required in the BRIEF register only.
# Its three parts are the ask (a question mark), what he is asked to read (the
# meter or the usage figure) and the ABSENCE of the NEEDS YOU markers, because
# the ruling makes it a LINE and not a decision: no options, no recommendation,
# no default, no deadline. It sits FIRST because the ruling says first.
# FIFTEEN WORDS IN ITS FIRST FORM PUT GOOD_BRIEF AT 151 OF 150, MEASURED, so
# it is nine and says the same thing: the accepting fixture may not sit over
# the cap it is meant to demonstrate, and padding the cap to fit a fixture
# would be moving the bound to fit the reading.
BRIEF_READING = "READING: what do your two usage meters say now?"
GOOD_BRIEF = BRIEF_READING + "\n\n" + GOOD.replace(
    "BUDGET: £0 spent, well inside the month.", BRIEF_SPLIT)

BAD_BRIEF = {
    "a brief with no split sentence at all":
        GOOD_BRIEF.replace(BRIEF_SPLIT, "BUDGET: comfortably inside the "
                                        "month, with nothing bought."),
    "a split that names no unit":
        GOOD_BRIEF.replace("Nine sessions went to the studio and two to the "
                           "game since the previous brief, counted in "
                           "sessions and not points until the rate is "
                           "measured.",
                           "Most of the work went to the studio and a little "
                           "to the game."),
    "a split counted in points rather than sessions":
        GOOD_BRIEF.replace("counted in sessions and not points until the rate "
                           "is measured", "counted in points"),
    "a split sitting outside the BUDGET section":
        GOOD_BRIEF.replace(BRIEF_SPLIT, "BUDGET: comfortably inside the "
                                        "month, with nothing bought.")
                  .replace("NEXT VISIBLE THING: a walk through that street, "
                           "tomorrow evening.",
                           "NEXT VISIBLE THING: a walk through that street, "
                           "tomorrow evening. Nine sessions went to the "
                           "studio and two to the game, counted in sessions "
                           "and not points until the rate is measured."),
}

# THE READING ASK, REJECTING, FOUR WAYS. Each differs from GOOD_BRIEF in ONE
# thing and every one is SYNTHETIC: pinning a rejecting fixture to a real brief
# would break the day somebody writes one, which is the reasoning already
# written at BAD_BRIEF_SURVIVING. (label, the exact rule name it must trip,
# the text). The four cover the three parts and the position separately,
# because a single fixture failing all of them at once would let three of the
# four stop biting in silence.
BAD_BRIEF_READING = (
    # NO ASK AT ALL. The brief opens on the headline, which is every brief in
    # the tree before this evening and is the case the rule exists for.
    ("a brief that never asks for the reading", "reading",
     GOOD_BRIEF.replace(BRIEF_READING + "\n\n", "")),
    # THE ASK EXISTS AND IS NOT FIRST. Ruled "as its FIRST line", and this is
    # the fixture that proves position is measured rather than described: the
    # text contains every word of the ask and is still refused.
    ("an ask buried below the headline", "reading",
     GOOD_BRIEF.replace(BRIEF_READING + "\n\n", "")
               .replace("WHAT CHANGED:", BRIEF_READING + "\n\nWHAT CHANGED:")),
    # A STATEMENT, NOT AN ASK. He is told a number instead of asked for one,
    # which is precisely the "work from whatever number I last typed" his
    # ruling refuses.
    ("a first line that tells him the meter instead of asking", "reading",
     GOOD_BRIEF.replace(BRIEF_READING,
                        "READING: your usage meters stood where you left "
                        "them.")),
    # THE ASK PUT THROUGH THE NEEDS YOU MACHINERY. The ruling is explicit that
    # this is the OPPOSITE of what it asked for: a default on this question
    # manufactures permission to spend on a day he never answered.
    ("an ask carrying a default and a deadline", "reading",
     GOOD_BRIEF.replace(BRIEF_READING,
                        BRIEF_READING + " DEFAULT: yesterday's number. "
                        "DEADLINE: noon.")),
)

# WHAT THE BRIEF REGISTER MUST STILL REFUSE AFTER THE RETIREMENT OF 2026-09-09.
# Two things left the brief's list; these are the proof that the rest did not
# leave with them, which is the whole difference between a retirement and a hole.
# (label, the exact rule name it must trip, and nothing else), each differing
# from GOOD_BRIEF in ONE thing. SYNTHETIC, like every rejecting fixture here.
BAD_BRIEF_SURVIVING = (
    # The four sections that were NEVER retired are still demanded, so the shape
    # rule cannot have been switched off along with BUDGET.
    ("a brief with no HEADLINE section", "shape",
     GOOD_BRIEF.replace("HEADLINE: the town has textures",
                        "The town has textures")),
    # The brief's own cap, which is 150 and not the unprompted 120.
    ("a brief past the brief register's own cap", "wordcap",
     GOOD_BRIEF.replace("Everything else waited on that.",
                        "Everything else waited on that. "
                        + ("and " * (CAP_BRIEF + 10
                                     - len(count_words(GOOD_BRIEF)))))),
    # The ban list, which binds in every register.
    ("a brief carrying a file path", "banned:file path",
     GOOD_BRIEF.replace("the grey street now paints properly",
                        "production/queue/062-uv-chain.md is the blocker")),
)

# THE HISTORICAL ANNOTATION FIXTURES, ruled 2026-09-06. SYNTHETIC to the last
# word: pinning a rejecting fixture to one of the two real annotated messages
# would break the day somebody edits a message, which is the whole reason the
# rejecting fixtures in this file are made up.
#
# AT_CAP is GOOD padded to EXACTLY the cap, COMPUTED rather than typed, so the
# fixture cannot drift out of position the day GOOD changes. The suite asserts
# the padding landed before it reads anything off these four readings: with the
# body at exactly the cap, the only thing that can move a verdict between them
# is the annotation line and its scoping.
AT_CAP = GOOD.replace(
    "Everything else waited on that.",
    "Everything else waited on that. "
    + "and " * (CAP_UNPROMPTED - len(count_words(GOOD))))
HISTORICAL_LINE = ("HISTORICAL, written on 3 September and sent later: the "
                   "street it asks about has since shown its textures.")
HISTORICAL_SECOND = ("HISTORICAL, and a second marker line is message content, "
                     "not an annotation.")
HIST_ONE = HISTORICAL_LINE + "\n" + AT_CAP
# NOT FIRST: the same annotation, one line down. It is message content there
# and is counted, or "put it under the headline" is the way round the cap.
HIST_NOT_FIRST = AT_CAP.partition("\n")[0] + "\n" + HISTORICAL_LINE + "\n" \
    + AT_CAP.partition("\n")[2]
# TWO: the first is the annotation, the second is a line of the message.
HIST_TWO = HISTORICAL_LINE + "\n" + HISTORICAL_SECOND + "\n" + AT_CAP

# THE ACCEPTING FIXTURE FOR THE RULED WHOLE-URL EXCEPTION: the message Jafar's
# item 4(c) of 2026-09-09 asked for, which is the real message this mechanism
# was built to send and therefore the right fixture for it. 117 words of 120,
# one URL, and that URL is the one entry on RULED_LINKS.
#
# A COPY, TAKEN 2026-09-09 from production/scratch/held/2026-09-09-atlas-02-
# research-digest.unprompted.md.held and verified equal to it byte for byte
# when it was taken. A COPY AND NOT A READ, on purpose: the file moves to the
# outbox when this lands and the Producer may still edit its NEEDS YOU line
# before it is sent, and an accepting fixture that reads a file somebody is
# about to edit goes red for something that is not a fault. The LIVE file is
# covered by the gate's live walk instead, which checks whatever is in the
# outbox on every run and prints linksRuledUsed=N/M for it.
#
# Derived, never typed twice: the fixtures below are built from the entry, and
# THAT NOW INCLUDES THE DIGEST'S OWN LINK. It was a second literal copy of the
# URL until 2026-09-15, when the tree link moved with the site and the two
# copies had to be found by grep rather than by the program; a copy the program
# cannot see is the one nobody updates.
RULED_URL = RULED_LINKS[0][0]
RULED_LABEL = RULED_LINKS[0][1]

RULED_DIGEST = """HEADLINE: Period research is in; the street needs a beer hatch.

WHAT CHANGED: Pubs were rooms, not one space; a surviving snug means poor or stubborn. No under-fourteens in the bar, by law; all-day opening only since eighty-eight. Houses get newer up the hill; one in five lacks central heating. Dockers lost their guaranteed work in eighty-nine: same coat, new standing. Evening buses thinned; the last bus matters. Still missing, pending a machine that can reach the sources: a real pub's measurements, what a trawlerman or barmaid wore, prices, a last-bus time. Nothing built yet.
[the research you asked for](%s)

NEEDS YOU: nothing new.

NEXT VISIBLE THING: Mickey's laid out; when, unknown.

BUDGET: nothing bought for this.
""" % RULED_URL

# The date the fixtures are checked against. Fixed, because a deadline fixture
# that reads the wall clock passes in September and fails in October, and a
# test whose result depends on the day it runs is not a test.
FIXTURE_NOW = datetime.datetime(2026, 9, 3, 12, 0)


def _gate_tree(files):
    """A throwaway repository root holding exactly `files`.

    SYNTHETIC ON PURPOSE. A rejecting fixture pinned to a real brief goes red
    the day somebody rewrites the brief, and a guard that reddens when the
    project improves is a guard somebody switches off. The cleanup is
    REGISTERED rather than left to the reader: these run on every verify.
    """
    import atexit
    import shutil
    import tempfile
    d = pathlib.Path(tempfile.mkdtemp(prefix="producer-gate-"))
    atexit.register(shutil.rmtree, str(d), True)
    for rel, text in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return d


def selftest():
    """Both outcomes, ACCEPTING CASE FIRST, and each rejecting fixture must be
    refused BY ITS OWN RULE. A suite that only asserted 'rejected' would pass a
    check that rejects everything, which is the validator nothing survives."""
    passed, failed = 0, []

    def ok(name, cond, got=""):
        nonlocal passed
        if cond:
            passed += 1
            print("  ok   %s" % name)
        else:
            failed.append(name)
            print("  FAIL %s\n         got: %s" % (name, got))

    print("producer-check --selftest: ACCEPTING CASE FIRST\n")
    r = check(GOOD, "unprompted", FIXTURE_NOW)
    ok("a real compliant message passes with no finding at all",
       not r["findings"], [str(f) for f in r["findings"]])
    ok("and it carries %d link(s), inside the ruled band of %d..%d, both to "
       "the site (%s)" % (len(r["urls"]), LINK_MIN, LINK_MAX,
                          "/".join(r["site_labels"]) or NOTHING),
       LINK_MIN <= len(r["urls"]) <= LINK_MAX
       and len(r["good_links"]) == len(r["urls"]),
       (r["urls"], r["good_links"]))
    # THE LADDER: ONE MESSAGE, TWO RULEBOOKS, ONE RUN. The rung is membership
    # of LEGACY_LINK_RULES and nothing else, and the ruled property is that
    # this rung differs from the one above in nothing: the band only REMOVED
    # destinations, so a message legal today was legal before it.
    r_legacy = check(GOOD, "unprompted", FIXTURE_NOW, legacy_links=True)
    ok("the same message passes under the retired destination list too (%s), "
       "because the ruling of 2026-09-06 only REMOVED destinations"
       % r_legacy["link_generation"],
       not r_legacy["findings"], [str(f) for f in r_legacy["findings"]])
    ok("and on that rung the band's two rules are named as NOT ENFORCED "
       "rather than skipped in silence (%s)"
       % ",".join(sorted(set(r_legacy["not_enforced"]) & set(LINK_BAND_RULES))),
       set(LINK_BAND_RULES) <= set(r_legacy["not_enforced"])
       and not (set(LINK_BAND_RULES) & set(r["not_enforced"])),
       (r_legacy["not_enforced"], r["not_enforced"]))
    # THE LIST ITSELF, ON EVERY RUN. A grandfathering list that could gain a
    # member written after the rule would be the date switch again, wearing a
    # tuple: the specimen would choose its rulebook by being added to it.
    late = [rel for rel in LEGACY_LINK_RULES
            if (FILENAME_DATE_RE.match(rel.rsplit("/", 1)[-1]) or [None])
            and FILENAME_DATE_RE.match(rel.rsplit("/", 1)[-1])
            and datetime.date.fromisoformat(
                FILENAME_DATE_RE.match(rel.rsplit("/", 1)[-1]).group(1))
            >= LINK_BAND_RULED_ON]
    ok("every one of the %d frozen LEGACY_LINK_RULES name(s) is dated before "
       "the band was ruled on %s" % (len(LEGACY_LINK_RULES),
                                     LINK_BAND_RULED_ON.isoformat()),
       not late and len(LEGACY_LINK_RULES) == 3, late)

    # ---- THE VERBATIM RESEARCH EXEMPTION, ruled 2026-09-14 (queue: five
    # coverage audits staged, four refused on ordinary English). A LADDER:
    # ONE BODY, TWO RULEBOOKS, ONE RUN, and the only number it yields is the
    # difference between the rungs. ACCEPTING CASE FIRST.
    RESEARCH = ("The man whose job it is opens the yard gate on Tuesday, and "
                "the crime he committed that morning is on the record.\n"
                "[the gallery](https://jsab258.github.io/ledger/"
                "gallery.html)\n")
    r_ver = check(RESEARCH, "answer", FIXTURE_NOW, research_verbatim=True)
    ok("a verbatim research delivery passes with ordinary-English job, gate "
       "and committed in it",
       not r_ver["findings"], [str(f) for f in r_ver["findings"]])
    ok("and the waived rule is NAMED as not enforced rather than skipped in "
       "silence (%s)" % "/".join(r_ver["research_waived"]),
       r_ver["research_waived"] == list(RESEARCH_WAIVED_RULES)
       and set(RESEARCH_WAIVED_RULES) <= set(r_ver["not_enforced"]),
       (r_ver["research_waived"], r_ver["not_enforced"]))
    ok("and its done-line key carries both moments in one value (%s)"
       % research_key(r_ver),
       research_key(r_ver).startswith("banned..listed-1-of-")
       and " " not in research_key(r_ver), research_key(r_ver))
    # THE SECOND RUNG. Same body, same instant, exemption OFF: the ban list
    # still bites, which is what proves the rule was not disabled.
    r_plainv = check(RESEARCH, "answer", FIXTURE_NOW)
    ok("the SAME body off the list is still refused by the ban list, so the "
       "rule was narrowed and not disabled (%s)"
       % ",".join(sorted({f.rule for f in r_plainv["findings"]})),
       [f.rule for f in r_plainv["findings"]] == ["banned:run internals"],
       [str(f) for f in r_plainv["findings"]])
    ok("and its key says not-on-the-list rather than an empty waiver (%s)"
       % research_key(r_plainv),
       research_key(r_plainv).startswith("none..not-on-the-"),
       research_key(r_plainv))
    # NARROWNESS, BOTH WAYS. The exemption is one rule wide, and the other
    # rules still refuse a listed file.
    ok("the exemption waives exactly one rule (%s) and can only widen in a "
       "reviewed diff" % "/".join(RESEARCH_WAIVED_RULES),
       RESEARCH_WAIVED_RULES == ("banned",), RESEARCH_WAIVED_RULES)
    THREE = RESEARCH + ("[a](https://jsab258.github.io/ledger/)\n"
                        "[b](https://jsab258.github.io/ledger/map.html)\n")
    r_cap = check(THREE, "answer", FIXTURE_NOW, research_verbatim=True)
    ok("a listed file that breaks the link cap is STILL refused",
       any(f.rule == "linkcap" for f in r_cap["findings"]),
       [str(f) for f in r_cap["findings"]])
    BADDEST = ("The man whose job it is.\n"
               "[x](https://github.com/jsab258/ledger/blob/main/CLAUDE.md)\n")
    r_dest = check(BADDEST, "answer", FIXTURE_NOW, research_verbatim=True)
    ok("and a listed file that links to a repo markdown file is STILL refused",
       any(f.rule == "linkdest" for f in r_dest["findings"]),
       [str(f) for f in r_dest["findings"]])
    # MEMBERSHIP IS BY NAME AND BY LOCATION, and the sender's absolute path
    # must resolve to the same name the gate's walk produces or the two would
    # grade one file by two rulebooks. SYNTHETIC ROOT: a rejecting case pinned
    # to a real delivery breaks the day that delivery is sent and cleared.
    import tempfile as _tf
    _root = pathlib.Path(_tf.mkdtemp())
    (_root / "production" / "outbox").mkdir(parents=True)
    _abs = _root / "production" / "outbox" / "x.answer.md"
    _abs.write_text("")
    ok("an absolute path resolves to the repo-relative name the gate walks",
       rel_under(str(_abs), str(_root)) == "production/outbox/x.answer.md",
       rel_under(str(_abs), str(_root)))
    _outside = str(_root.parent / "not-in-the-repo.md")
    ok("a path outside the root claims no membership at all, and nor does "
       "stdin", rel_under(_outside, str(_root)) is None
       and rel_under("-", str(_root)) is None,
       (rel_under(_outside, str(_root)), rel_under("-", str(_root))))
    ok("a name on the frozen list that exists nowhere is still only a name: "
       "membership never reads the text",
       "production/outbox/never-existed.answer.md" not in RESEARCH_VERBATIM,
       RESEARCH_VERBATIM)

    # ---- THE SPLIT LOST NOTHING, ruled 2026-09-14 ("in full"). SYNTHETIC
    # ACCEPTING CASE FIRST, so the arithmetic is exercised on every machine
    # including one with no outbox at all; the live files follow as the series.
    WHOLE = (b"# A title\n\nFirst paragraph, which is the one a bad split "
             b"eats.\n\n## The header it was cut at\n\nSecond paragraph.\n")
    HALF1 = (b"# A title\n\nFirst paragraph, which is the one a bad split "
             b"eats.\n\n[CUT HERE: part 1 of 2. The rest follows as its own "
             b"message.]\n")
    HALF2 = (b"[PART 2 of 2, continuing: A title. Part 1 was the previous "
             b"message.]\n\n## The header it was cut at\n\nSecond "
             b"paragraph.\n")
    rj = research_rejoin_reading(WHOLE, HALF1, HALF2)
    ok("two announced halves rejoin to the whole byte for byte (%d+%d bytes "
       "in, %d of %d out, delta %+d, %d marker line(s) dropped, firstDiff=%d)"
       % (rj["bytes_part1"], rj["bytes_part2"], rj["bytes_joined"],
          rj["bytes_original"], rj["bytes_delta"], rj["markers_dropped"],
          rj["first_diff"]),
       rj["equal"] and rj["markers_dropped"] == 2 and rj["first_diff"] == -1,
       rj["joined"])
    # REJECTING, TWICE, because a check that only ever sees a good split is the
    # validator nothing survives. Fixture one drops a paragraph, which is the
    # failure this exists for. Fixture two swaps bytes for the SAME NUMBER of
    # bytes, which is what proves the comparison reads bytes and not lengths.
    LOST = HALF2.replace(b"\n\nSecond paragraph.\n", b"\n")
    rj_lost = research_rejoin_reading(WHOLE, HALF1, LOST)
    ok("a part 2 with one paragraph missing does NOT rejoin, and the reading "
       "says where (firstDiff=%d, delta %+d bytes)"
       % (rj_lost["first_diff"], rj_lost["bytes_delta"]),
       not rj_lost["equal"] and rj_lost["first_diff"] >= 0
       and rj_lost["bytes_delta"] < 0, rj_lost["bytes_delta"])
    EDITED = HALF2.replace(b"Second paragraph.", b"Secund paragraph.")
    rj_edit = research_rejoin_reading(WHOLE, HALF1, EDITED)
    ok("and a part 2 edited without changing its LENGTH is caught too, so the "
       "comparison is bytes and not sizes (firstDiff=%d, delta %+d bytes)"
       % (rj_edit["first_diff"], rj_edit["bytes_delta"]),
       not rj_edit["equal"] and rj_edit["bytes_delta"] == 0,
       rj_edit["bytes_delta"])
    # AND THE MARKERS ARE NOT A WILDCARD: ordinary text that merely mentions a
    # cut is not removed, or the rejoin could tidy away the very line a bad
    # split ate.
    rj_body = research_rejoin(b"a\nthe [CUT HERE: ...] is mid-line\n",
                              b"b\n")
    ok("a cut marker that is not at the start of a line is left in the body "
       "(%d dropped)" % rj_body["markers_dropped"],
       rj_body["markers_dropped"] == 0 and b"mid-line" in rj_body["joined"],
       rj_body["joined"])
    # AND A HALF THAT LOST ITS ANNOUNCEMENT IS VISIBLE AS A COUNT, not as a
    # pass. Jafar's ruling has TWO clauses, "split each into two parts" and
    # "with the cut announced in the message", and losslessness alone cannot
    # see the second: a part 1 with no CUT HERE line rejoins to exactly the
    # same bytes, because a line that was never added is a line the rejoin
    # never has to remove.
    rj_silent = research_rejoin_reading(WHOLE, HALF1.replace(
        b"\n[CUT HERE: part 1 of 2. The rest follows as its own message.]\n",
        b"\n"), HALF2)
    ok("a part 1 that lost its cut announcement still rejoins (equal=%s), so "
       "the announcement is counted SEPARATELY: %d marker(s) dropped where 2 "
       "is the ruled shape"
       % ("true" if rj_silent["equal"] else "false",
          rj_silent["markers_dropped"]),
       rj_silent["equal"] and rj_silent["markers_dropped"] == 1,
       rj_silent["markers_dropped"])

    # ---- THE ROWS THE REGISTER IS BUILT FROM. PURE and NEVER VACUOUS: these
    # hold whether or not a single delivery is still on disk.
    pairs, faults = research_pairs()
    ok("the %d delivery row(s) all hold the ruled shape (two parts in %s/, "
       "one unsplit original in %s/) and produce the %d listed name(s)"
       % (len(RESEARCH_DELIVERIES), OUTBOX_DIR, BLOCKED_DIR,
          len(RESEARCH_VERBATIM)),
       not faults and len(pairs) == len(RESEARCH_DELIVERIES)
       and len(pairs) * len(RESEARCH_PART_SUFFIXES) == len(RESEARCH_VERBATIM),
       faults or len(pairs))
    on_list = [b for _p1, _p2, b in pairs if b in RESEARCH_VERBATIM]
    ok("and not one of the %d unsplit original(s) is itself on the sendable "
       "register: those are over the wire cap and must never be sent"
       % len(pairs), not on_list, on_list)
    # REJECTING, SYNTHETIC, and pinned to no real asset: the dangerous typo is
    # a row that puts an unsplit original where a part belongs, which would
    # make an unsendable file sendable. It is reported as a fault, never
    # dropped, and the derived register does not gain the name.
    BAD_ROW = (("production/outbox/never-existed-part1.answer.md",
                "production/outbox-blocked/never-existed.answer.md",
                "production/outbox-blocked/never-existed.answer.md"),)
    bad_pairs, bad_faults = research_pairs(BAD_ROW)
    ok("a synthetic row naming a blocked original where part 2 belongs is a "
       "counted fault and yields no pair (%d fault(s), %d pair(s))"
       % (len(bad_faults), len(bad_pairs)),
       len(bad_faults) == 1 and not bad_pairs
       and "never-existed.answer.md" in bad_faults[0], (bad_faults, bad_pairs))
    ok("and a synthetic row of the wrong length is counted too rather than "
       "unpacked into an exception",
       research_pairs((("a-part1.answer.md",),))[1]
       and not research_pairs((("a-part1.answer.md",),))[0],
       research_pairs((("a-part1.answer.md",),)))

    # ---- THE LIVE SERIES. The repo IS the accepting fixture here. Every zero
    # ships its denominator: a pair whose files are not on disk is COUNTED as
    # unverifiable and NAMED, never passed in silence, because "sent and
    # cleared" and "silently truncated" must not read the same. The rejoin is
    # red only for a pair that could be read and did not match.
    rejoin_checked, rejoin_equal, rejoin_missing, rejoin_bad = 0, 0, [], []
    # THE SECOND CLAUSE OF THE RULING, counted over the same denominator and
    # in the same pass: part 1 carries its CUT HERE line and part 2 carries
    # its PART 2 line. Read off the two halves separately, never off the
    # rejoin's total, or one half carrying both markers would read as two
    # announced halves.
    rejoin_announced, rejoin_silent = 0, []
    for p1_rel, p2_rel, orig_rel in pairs:
        blobs, gone = [], []
        for rel in (orig_rel, p1_rel, p2_rel):
            f = REPO / rel
            try:
                blobs.append(f.read_bytes())
            except OSError:
                gone.append(rel)
        if gone:
            rejoin_missing.extend(gone)
            continue
        rejoin_checked += 1
        rr = research_rejoin_reading(*blobs)
        announced = all(
            any(line.startswith(marker) for line in half.split(b"\n"))
            for half, marker in zip(blobs[1:], CUT_MARKERS))
        if announced:
            rejoin_announced += 1
        else:
            rejoin_silent.append(orig_rel.rsplit("/", 1)[-1])
        if rr["equal"]:
            rejoin_equal += 1
        else:
            rejoin_bad.append("%s firstDiff=%d delta=%+d"
                              % (orig_rel.rsplit("/", 1)[-1],
                                 rr["first_diff"], rr["bytes_delta"]))
        print("       rejoin %-22s parts=%d+%d rejoined=%d/%d delta=%+d "
              "markersDropped=%d cutAnnounced=%s equal=%s"
              % (orig_rel.rsplit("/", 1)[-1].replace("2026-09-14-research-"
                                                     "coverage-audit-", "")
                 .replace(".answer.md", ""),
                 rr["bytes_part1"], rr["bytes_part2"], rr["bytes_joined"],
                 rr["bytes_original"], rr["bytes_delta"],
                 rr["markers_dropped"], "true" if announced else "FALSE",
                 "true" if rr["equal"] else "FALSE"))
    ok("every pair on disk rebuilds its unsplit original in %s/ byte for "
       "byte (rejoinPairsVerified=%s)%s"
       % (BLOCKED_DIR,
          "%d/%d" % (rejoin_equal, rejoin_checked) if rejoin_checked
          else "%s/no-pair-on-disk-in-this-run" % NOTHING,
          "" if not rejoin_missing
          else (". %d file(s) absent, so %d pair(s) could not be read: %s"
                % (len(rejoin_missing), len(pairs) - rejoin_checked,
                   cap([m.rsplit("/", 1)[-1] for m in rejoin_missing],
                       keep=3, width=60, sep=", ")))),
       not rejoin_bad, rejoin_bad)
    ok("and every pair on disk announces its cut in BOTH halves, which is the "
       "other half of the ruling (cutAnnounced=%s)"
       % ("%d/%d" % (rejoin_announced, rejoin_checked) if rejoin_checked
          else "%s/no-pair-on-disk-in-this-run" % NOTHING),
       not rejoin_silent, rejoin_silent)

    # ---- THE WIRE CAP, READ FROM THE ONE PLACE IT IS WRITTEN DOWN. The number
    # is not typed here: a second copy of 4096 in this file is a second place
    # for it to be wrong. The series is printed before the bound is read off
    # it, and the peak carries its own position (value@file).
    #
    # A FILE THAT IS NOT THERE IS COUNTED, NOT RED, exactly as the gate's rot
    # note treats a frozen entry whose file is gone: the day these deliveries
    # are cleared off the outbox, the denominator falls to the words NOTHING
    # MEASURED in this line and researchVerbatimGraded=0/10 on the gate's done
    # line, which is loud in both places. What IS red is a file that exists and
    # contradicts the bound.
    try:
        ex_src = (REPO / "tools" / "runner"
                  / "executor.py").read_text(encoding="utf-8")
    except OSError:
        ex_src = ""
    ex_cap = re.search(r"^TELEGRAM_TEXT_MAX = (\d+)$", ex_src, re.M)
    wire = int(ex_cap.group(1)) if ex_cap else None
    ok("the wire cap is read from tools/runner/executor.py rather than typed "
       "here (%s)" % (wire if wire else "%s: the file could not be read"
                      % NOTHING),
       wire is not None, ex_cap)
    # OVER THE LIST ITSELF, not over the pairs derived from it, so a name that
    # is not part-shaped is still measured: the invariant that matters is that
    # NOTHING ON THIS LIST IS UNSENDABLE, and an entry the pair arithmetic
    # could not parse is exactly where an unsplit file would hide.
    part_chars, orig_chars = [], []
    for rel, bucket in ([(x, part_chars) for x in RESEARCH_VERBATIM]
                        + [(o, orig_chars) for _1, _2, o in pairs]):
        try:
            bucket.append((len((REPO / rel).read_text(encoding="utf-8")),
                           rel.rsplit("/", 1)[-1]))
        except OSError:
            pass
    over = [n for n in part_chars if wire and n[0] > wire]
    under = [n for n in orig_chars if wire and n[0] <= wire]
    # PEAK for the parts and MINIMUM for the originals, because each is the
    # AT-WORST case for the claim beside it: the longest part is the one
    # closest to breaking "every part fits", the shortest original the one
    # closest to breaking "no original fits". Each carries its own position.
    worst_part = max(part_chars) if part_chars else None
    ok("every name on the list that was measured is under the wire cap: %s "
       "file(s) read, "
       "peak %s (the cap's own unit is characters, and these files are ASCII)"
       % (len(part_chars) or NOTHING,
          "%d@%s" % (worst_part[0], worst_part[1]) if worst_part else NOTHING),
       wire is not None and not over, over)
    slimmest = min(orig_chars) if orig_chars else None
    ok("and every unsplit original measured is OVER it, which is why none of "
       "them is on the list: %s original(s) read, shortest %s against a cap "
       "of %s"
       % (len(orig_chars) or NOTHING,
          "%d@%s" % (slimmest[0], slimmest[1]) if slimmest else NOTHING,
          wire if wire else NOTHING),
       wire is not None and not under, under)
    ok("and it is under the ruled cap (%d of %d words)"
       % (r["words"], CAP_UNPROMPTED), r["words"] <= CAP_UNPROMPTED, r["words"])
    ok("its five sections are all found, in order",
       r["sections_found"] == SECTIONS, r["sections_found"])
    ok("its one NEEDS YOU item parses as one item with three options",
       r["items"] == 1, r["items"])
    ok("its claims are seen as claims (%d of %d sentences)"
       % (r["claims"], r["sentences"]), r["claims"] >= 2,
       (r["claims"], r["sentences"]))

    # THE HISTORICAL ANNOTATION, ACCEPTING CASE FIRST, ruled by Jafar
    # 2026-09-06. Four readings of ONE body that sits at exactly the cap, so
    # the only variable across them is the annotation and its three scopes.
    ok("the padded fixture sits at exactly the cap before any annotation "
       "(%d of %d word(s))" % (len(count_words(AT_CAP)), CAP_UNPROMPTED),
       len(count_words(AT_CAP)) == CAP_UNPROMPTED, len(count_words(AT_CAP)))
    hist_words = len(count_words(HISTORICAL_LINE))
    r_hist = check(HIST_ONE, "unprompted", FIXTURE_NOW, legacy_links=True)
    ok("a LISTED file whose only over-cap content is one leading %s line "
       "PASSES, and the count printed is the body's (%d of %d word(s), with "
       "%d annotation word(s) uncounted and said so)"
       % (HISTORICAL_PREFIX, r_hist["words"], CAP_UNPROMPTED,
          r_hist["historical_words"]),
       not r_hist["findings"] and r_hist["words"] == CAP_UNPROMPTED
       and r_hist["historical_uncounted"] == 1
       and r_hist["historical_words"] == hist_words,
       [str(f) for f in r_hist["findings"]] or r_hist["words"])
    # REJECTING, and each of the three differs from the accepting reading in
    # ONE thing: the list, the position, the number of lines.
    r_unlisted = check(HIST_ONE, "unprompted", FIXTURE_NOW)
    ok("the SAME text UNLISTED is refused by wordcap and by nothing else "
       "(%d of %d word(s), %d line(s) uncounted)"
       % (r_unlisted["words"], CAP_UNPROMPTED,
          r_unlisted["historical_uncounted"]),
       {f.rule for f in r_unlisted["findings"]} == {"wordcap"}
       and r_unlisted["words"] == CAP_UNPROMPTED + hist_words
       and r_unlisted["historical_uncounted"] == 0,
       [str(f) for f in r_unlisted["findings"]])
    r_notfirst = check(HIST_NOT_FIRST, "unprompted", FIXTURE_NOW,
                       legacy_links=True)
    ok("a LISTED file whose %s line is NOT first counts it normally and is "
       "refused (%d of %d word(s), %d line(s) uncounted)"
       % (HISTORICAL_PREFIX, r_notfirst["words"], CAP_UNPROMPTED,
          r_notfirst["historical_uncounted"]),
       {f.rule for f in r_notfirst["findings"]} == {"wordcap"}
       and r_notfirst["words"] == CAP_UNPROMPTED + hist_words
       and r_notfirst["historical_uncounted"] == 0,
       [str(f) for f in r_notfirst["findings"]])
    second_words = len(count_words(HISTORICAL_SECOND))
    r_two = check(HIST_TWO, "unprompted", FIXTURE_NOW, legacy_links=True)
    ok("a LISTED file with TWO %s lines excuses the first and COUNTS the "
       "second (%d of %d word(s), which is the body plus the %d word(s) of "
       "the second line)"
       % (HISTORICAL_PREFIX, r_two["words"], CAP_UNPROMPTED, second_words),
       {f.rule for f in r_two["findings"]} == {"wordcap"}
       and r_two["words"] == CAP_UNPROMPTED + second_words
       and r_two["historical_uncounted"] == 1,
       [str(f) for f in r_two["findings"]])
    # AND THE FILE WITH NO ANNOTATION IS UNTOUCHED: same body, listed, no
    # marker, counted in full and inside the cap.
    r_plain = check(AT_CAP, "unprompted", FIXTURE_NOW, legacy_links=True)
    ok("a LISTED file with no annotation at all is unaffected (%d of %d "
       "word(s), %d line(s) uncounted)"
       % (r_plain["words"], CAP_UNPROMPTED, r_plain["historical_uncounted"]),
       not r_plain["findings"] and r_plain["words"] == CAP_UNPROMPTED
       and r_plain["historical_uncounted"] == 0
       and r_plain["historical_eligible"],
       [str(f) for f in r_plain["findings"]])

    # ACCEPTING, second register: a long answer carrying a number passes,
    # because his question sets the length and asks for the number.
    answer = ("You asked how many objects carry textures. Nearly all of them: "
              "563 of 593. The rest are the wet ground. "
              "https://jsab258.github.io/ledger/gallery.html " +
              "The remaining ones are small and none of them is in shot. " * 12)
    ra = check(answer, "answer", FIXTURE_NOW)
    ok("a long ANSWER carrying a count passes (%d words, no cap)" % ra["words"],
       not ra["findings"], [str(f) for f in ra["findings"]])
    ok("and the answer register NAMES the rules it did not enforce",
       set(ra["not_enforced"]) == {"wordcap", "shape", "options", "deadline",
                                   "nextvisible", "split", "reading",
                                   "filedline"},
       ra["not_enforced"])

    # ACCEPTING, third: a message with nothing needing him is not forced to
    # invent an item.
    empty = GOOD.replace(GOOD[GOOD.index("NEEDS YOU"):GOOD.index("NEXT VISIBLE")],
                         "NEEDS YOU: nothing today.\n\n")
    re_ = check(empty, "unprompted", FIXTURE_NOW)
    ok("an empty NEEDS YOU is accepted rather than forcing an invented item",
       not re_["findings"], [str(f) for f in re_["findings"]])

    # ACCEPTING, fourth: THE BRIEF REGISTER AND THE RETIREMENT OF 2026-09-09.
    # A brief that still carries a BUDGET section with the split sentence in it
    # passes: the retirement removed a REQUIREMENT and forbade nothing, so every
    # brief written under the old rule stays green. The accepting case that
    # matters is the live tree's own briefs, today's real message among them, and
    # it is asserted off the live gate walk further down.
    rb = check(GOOD_BRIEF, "brief", FIXTURE_NOW)
    ok("a brief STILL carrying the BUDGET section and the split sentence passes "
       "(%d word(s) of %d, %d of the %d section(s) the brief register requires)"
       % (rb["words"], rb["cap"], len(rb["sections_required_found"]),
          len(rb["sections_required"])),
       not rb["findings"], [str(f) for f in rb["findings"]])

    # THE READING ASK, ACCEPTING CASE FIRST, ruled by Jafar 2026-09-15. The
    # expensive failure for a new register rule is a rule nothing survives, so
    # the brief that CARRIES the ask is read before any brief that does not,
    # and it is read twice in the same run: through the DETECTOR directly (the
    # tested layer, so it cannot ship half-run) and through the REGISTER.
    rd_found, rd_missing, rd_line = reading_parts(GOOD_BRIEF)
    _rd_text, rd_no = reading_line(GOOD_BRIEF)
    ok("ACCEPTING: a brief whose FIRST line asks for the meter reading passes "
       "the brief register, and the detector finds %d of %d part(s) on line %d "
       "(missing %s)"
       % (rd_found, len(READING_PARTS), rd_no,
          cap(rd_missing, keep=5, sep=", ") or "none"),
       not rb["findings"] and rd_found == len(READING_PARTS)
       and not rd_missing and rd_no == 1
       and "reading" in rb["enforced"],
       "found=%d missing=%s line=%d enforced=%s"
       % (rd_found, rd_missing, rd_no, "reading" in rb["enforced"]))
    # THE RULE IS THE BRIEF'S AND NOBODY ELSE'S, both directions in one run.
    # An unprompted message and an answer NAME it under NOT ENFORCED rather
    # than skipping it in silence, and a message with no ask in those two
    # registers is not refused for the lack of one.
    ru_noask = check(GOOD, "unprompted", FIXTURE_NOW)
    ra_noask = check("You asked how many. Nearly all of them.\n"
                     "https://jsab258.github.io/ledger/gallery.html",
                     "answer", FIXTURE_NOW)
    ok("and the ask is required in the BRIEF register ONLY: an unprompted "
       "message and an answer with no ask on them carry `reading` under NOT "
       "ENFORCED and are not refused for it (%s / %s)"
       % ("/".join(ru_noask["not_enforced"]),
          "/".join(ra_noask["not_enforced"])),
       "reading" in ru_noask["not_enforced"]
       and "reading" in ra_noask["not_enforced"]
       and "reading" not in {f.rule for f in ru_noask["findings"]}
       and "reading" not in {f.rule for f in ra_noask["findings"]}
       and tuple(RULES_BRIEF_ONLY) == ("reading",),
       (ru_noask["not_enforced"], ra_noask["not_enforced"]))
    # AND `reading_found` IS None, NOT 0, WHERE THE RULE DID NOT RUN. A zero
    # would read as three parts looked for and none found, which is a different
    # fact from a rule that never looked; the report prints the words for it.
    ok("a register that does not enforce the ask reports it as nothing "
       "measured and never as zero of %d (unprompted=%s, answer=%s)"
       % (len(READING_PARTS), ru_noask["reading_found"],
          ra_noask["reading_found"]),
       ru_noask["reading_found"] is None
       and ra_noask["reading_found"] is None
       and rb["reading_found"] == len(READING_PARTS),
       (ru_noask["reading_found"], ra_noask["reading_found"],
        rb["reading_found"]))

    # THE LADDER FOR THE RETIREMENT: ONE TEXT, TWO REGISTERS, ONE RUN, and the
    # only thing that changes between the rungs is which register grades it. The
    # difference between the rungs IS the scope of the retirement, which is the
    # whole claim being made: the brief no longer requires BUDGET, and nothing
    # else was weakened. A rung taken in another run would be another photograph.
    no_budget = GOOD_BRIEF.replace(BRIEF_SPLIT + "\n", "")
    rb_nb = check(no_budget, "brief", FIXTURE_NOW)
    ru_nb = check(no_budget, "unprompted", FIXTURE_NOW)
    ok("a brief with NO BUDGET section at all passes the brief register, which "
       "is the message Jafar's director test produces (%d of %d required "
       "section(s): %s; retired here: %s)"
       % (len(rb_nb["sections_required_found"]),
          len(rb_nb["sections_required"]),
          "/".join(rb_nb["sections_required_found"]) or NOTHING,
          "/".join(rb_nb["sections_retired"]) or "none"),
       not rb_nb["findings"] and rb_nb["sections_retired"] == ["BUDGET"]
       and not rb_nb["sections_retired_present"],
       [str(f) for f in rb_nb["findings"]])
    ok("and the SAME text is still refused by `shape` in the UNPROMPTED "
       "register, which still requires all %d section(s): nothing but the brief "
       "was weakened" % len(SECTIONS),
       {f.rule for f in ru_nb["findings"]} == {"shape"}
       and ru_nb["sections_required"] == list(SECTIONS),
       [str(f) for f in ru_nb["findings"]])
    # THE RETIREMENT ITSELF, PINNED, and pinned in the direction that a future
    # session would have to read the ruling block to reverse. It is NOT pinned
    # the other way: nothing here asserts that no register may ever enforce
    # `split` again, because the Sunday summary is where the number is owed and
    # a test that reddened when that work was done would be a test against the
    # ruling.
    ok("BUDGET is retired from the brief register and from nothing else "
       "(required in %s; not required in %s) and is still a label the parser "
       "knows, so an old brief's money line is parsed and order-checked as "
       "before (section_label reads %s)"
       % ("/".join(k for k in sorted(SECTIONS_REQUIRED)
                   if "BUDGET" in SECTIONS_REQUIRED[k]),
          "/".join(k for k in sorted(SECTIONS_REQUIRED)
                   if "BUDGET" not in SECTIONS_REQUIRED[k]),
          section_label("BUDGET: nothing bought.")),
       "BUDGET" not in SECTIONS_REQUIRED["brief"]
       and "BUDGET" in SECTIONS_REQUIRED["unprompted"]
       and section_label("BUDGET: nothing bought.") == "BUDGET",
       (SECTIONS_REQUIRED, section_label("BUDGET: nothing bought.")))
    enforcing = sorted(k for k in REGISTERS if "split" in REGISTERS[k][1])
    ok("`split` is enforced by %d of the %d register(s) (%s) and is named under "
       "NOT ENFORCED by every one of them, so a retired rule cannot read as a "
       "rule that passed. The number is owed by %s"
       % (len(enforcing), len(REGISTERS), "/".join(enforcing) or "none",
          SPLIT_OWED_BY),
       "split" not in REGISTERS["brief"][1]
       and all("split" in check(GOOD_BRIEF, k, FIXTURE_NOW)["not_enforced"]
               for k in REGISTERS if "split" not in REGISTERS[k][1]),
       (enforcing, sorted(REGISTERS)))
    # THE INVARIANT THAT SURVIVES THE MOVE, and it is an invariant rather than a
    # snapshot on purpose: a register that enforces `split` must also REQUIRE the
    # BUDGET section, because the rule reads that section's body and nothing
    # else. Vacuously true today with nothing enforcing it, which is why the
    # denominator is printed and the words say so rather than printing a clean 0.
    mismatched = [k for k in enforcing
                  if "BUDGET" not in SECTIONS_REQUIRED.get(k, SECTIONS)]
    ok("every register that enforces `split` also requires the BUDGET section "
       "it reads (%s)"
       % ("%d of %d checked" % (len(enforcing) - len(mismatched), len(enforcing))
          if enforcing else NOTHING.replace("-", " ")
          + ": no register enforces it today"),
       not mismatched, mismatched)
    # THE DETECTOR, WHICH IS THE HALF THAT MUST NOT ROT WHILE IT WAITS. Driven
    # DIRECTLY, because no register calls it today: through check() alone these
    # four fixtures would prove nothing, and an unrun detector that the Sunday
    # register later trusts is the silent-instrument failure. Each fixture
    # differs from GOOD_BRIEF in ONE part of the sentence.
    found_good, missing_good = split_parts(
        " ".join(split_sections(GOOD_BRIEF)[0].get("BUDGET", [])))
    ok("the kept split detector still finds all %d part(s) in the good brief's "
       "BUDGET body (%d found, %s missing)"
       % (len(SPLIT_PARTS), found_good, "/".join(missing_good) or "none"),
       found_good == len(SPLIT_PARTS) and not missing_good,
       (found_good, missing_good))

    # ACCEPTING, fifth: THE ONE RULED WHOLE-URL EXCEPTION, and the accepting
    # case is the real message it was ruled for. The whole risk of this
    # mechanism is building a hole instead of an exception, so the accepting
    # reading comes first and the five near misses come straight after it in
    # the same run: the difference between the rungs is one URL.
    print("\n  THE RULED WHOLE-URL EXCEPTION, ACCEPTING CASE FIRST:\n")
    r_ruled = check(RULED_DIGEST, "unprompted", FIXTURE_NOW)
    ok("the digest Jafar asked for passes WITH the ruled URL (%d of %d "
       "word(s), %d URL(s), %d to the site, ruledUsed=%d/%d, list applied %s)"
       % (r_ruled["words"], CAP_UNPROMPTED, len(r_ruled["urls"]),
          len(r_ruled["site_links"]), r_ruled["ruled_used"],
          r_ruled["ruled_of"], r_ruled["link_generation"]),
       not r_ruled["findings"] and r_ruled["ruled_used"] == 1
       and r_ruled["ruled_labels"] == [RULED_LABEL]
       and r_ruled["good_links"] == r_ruled["urls"]
       and r_ruled["link_generation"].endswith("/plus-ruled-url"),
       [str(f) for f in r_ruled["findings"]] or r_ruled["link_generation"])
    # THE SAME NORMALISATION site_page USES, and it is the same function: an
    # anchor or a trailing slash is the same URL, and nothing else is.
    ok("the ruled URL is matched through norm_url, so a trailing slash and a "
       "fragment are the same URL (%s/%s)"
       % (ruled_link(RULED_URL + "/"), ruled_link(RULED_URL + "#readme")),
       ruled_link(RULED_URL + "/") == RULED_LABEL
       and ruled_link(RULED_URL + "#readme") == RULED_LABEL,
       (ruled_link(RULED_URL + "/"), ruled_link(RULED_URL + "#readme")))
    # AND A MESSAGE THAT USED NO EXCEPTION MUST NOT READ AS ONE THAT DID. The
    # generation string is where a reader sees the exception was used, so it is
    # silent when nothing matched: 0 of 1, said with its denominator.
    ok("a message that matched no ruled entry does not say it used one "
       "(ruledUsed=%d/%d, list applied %s)"
       % (r["ruled_used"], r["ruled_of"], r["link_generation"]),
       r["ruled_used"] == 0 and not r["ruled_labels"]
       and "plus-ruled-url" not in r["link_generation"],
       r["link_generation"])
    # A5, THE FOURTH PUBLISHED PAGE, ruled the same morning (item 2). The
    # register's list and the publisher's list are two copies of one idea, so
    # this reads the PUBLISHER'S OWN SOURCE rather than trusting this file: a
    # page the register allows and the publisher never writes is a 404 on his
    # phone, and a page the publisher writes and the register refuses is a link
    # the Producer cannot send. A missing publisher is red, not clean.
    pub = REPO / "tools" / "publish-glance.py"
    pub_src = pub.read_text(encoding="utf-8", errors="replace") \
        if pub.is_file() else ""
    ok("the world page is on the register's allowlist (%d destination(s): %s) "
       "and tools/publish-glance.py publishes that exact name (%d "
       "character(s) read)"
       % (len(SITE_PAGES), site_destination_words("/"), len(pub_src)),
       site_page(SITE_ORIGIN + "world.html") == "the-world"
       and link_ok(SITE_ORIGIN + "world.html")
       and '"world.html"' in pub_src,
       "siteLabel=%s publisherNamesIt=%s"
       % (site_page(SITE_ORIGIN + "world.html"), '"world.html"' in pub_src))

    print("\n  AND THE FIVE NEAR MISSES, EACH REFUSED BY linkdest:\n")
    # EACH DIFFERS FROM THE ADMITTED URL IN ONE THING: the directory, the file,
    # tree versus blob, the branch, one character. Every one is DERIVED from
    # the entry rather than typed, so they cannot drift away from it. Each
    # fixture keeps a legal site link so the FLOOR is satisfied and only
    # linkdest can fire, which is how BAD["linkdest"] is built too: a fixture
    # that broke two rules at once would prove neither.
    near_misses = {
        "the parent directory": RULED_URL.rsplit("/", 1)[0],
        "a child blob under it": RULED_URL.replace("/tree/", "/blob/")
                                 + "/transport-timetables.md",
        "blob instead of tree": RULED_URL.replace("/tree/", "/blob/"),
        # RE-DERIVED 2026-09-15, AND THE REASON IS THE WHOLE POINT OF THE
        # `differs` GUARD BELOW. This member read "the same path on main",
        # built by swapping the archive's working branch out of the ruled URL,
        # and it was a correct near miss for as long as the ruled entry pointed
        # at that branch. Queue 256 moved the entry ONTO main, which silently
        # turned `.replace(...)` into a no-op: the fixture then quoted the
        # RULED URL ITSELF and asserted it must be refused, so it failed with
        # ruledUsed=1/1. A near-miss set is relative to whatever the ruled URL
        # currently is. The one edit is now the branch, and art/atlas-01 is a
        # branch that EXISTS on jsab258/ledger (main, art/atlas-01, pc-inbox,
        # pc-results, read from `git ls-remote --heads origin` 2026-09-13), so
        # this stays the hardest version of the case: a real branch, a real
        # path, and still not the one admitted.
        "the same path on another branch":
            RULED_URL.replace("/tree/main/", "/tree/art/atlas-01/"),
        "one character appended": RULED_URL + "x",
    }
    # EVERY MEMBER MUST ACTUALLY DIFFER FROM THE RULED URL, asserted on the
    # member's own line rather than as a sixth case. A derivation that becomes
    # a no-op when the entry moves is how this group broke on 2026-09-15, and
    # a fixture that quietly equals the thing it rejects tests nothing.
    for name, url in near_misses.items():
        near = RULED_DIGEST.replace(RULED_URL, url) \
            + "\n[where things stand](%s)\n" % SITE_ORIGIN
        rn = check(near, "unprompted", FIXTURE_NOW)
        rules = {f.rule for f in rn["findings"]}
        ok("%-31s is refused by linkdest and admitted by nothing "
           "(differsFromRuledUrl=%s, ruledUsed=%d/%d, %d of %d link(s) "
           "offsite)"
           % (name, "true" if url != RULED_URL else "FALSE-it-IS-the-ruled-url",
              rn["ruled_used"], rn["ruled_of"],
              len(rn["offsite_links"]), len(rn["urls"])),
           url != RULED_URL
           and rules == {"linkdest"} and rn["ruled_used"] == 0
           and ruled_link(url) is None and not link_ok(url)
           and len(rn["offsite_links"]) == 1,
           "found %s for %s" % (sorted(rules) or "nothing", url))
    # THE REJECTING FIXTURE THAT EXISTS NOWHERE, which is the shape this
    # project's instrument rules ask for: a synthetic key pinned to no real
    # asset, so doing the work the tool prompts can never break the tool.
    ok("a synthetic URL on the same host and branch is not admitted",
       ruled_link(RULED_URL.replace("atlas-02", "atlas-99")) is None
       and not link_ok(RULED_URL.replace("atlas-02", "atlas-99")),
       RULED_URL.replace("atlas-02", "atlas-99"))
    # AND THE OLD FIXTURE Jafar's band was written from STAYS REFUSED. The BAD
    # loop below checks the message; this checks the URL itself, because the
    # exception is a URL test and that is where a hole would be.
    ok("the repository markdown URL the band was written from stays refused",
       not link_ok("https://github.com/jsab258/wc26-picks/blob/main/q.md")
       and ruled_link(
           "https://github.com/jsab258/wc26-picks/blob/main/q.md") is None,
       "blob/main/q.md")
    # THE TUPLE ITSELF, ON EVERY RUN. One member, because an exception that can
    # grow is a band being rewritten by whoever adds the next line; and the
    # record that admits each member must EXIST and still carry the URL, which
    # is the guard against an entry outliving its ruling.
    ok("the frozen RULED_LINKS tuple holds exactly 1 entry (%d, labelled %s)"
       % (len(RULED_LINKS), "/".join(lbl for _, lbl, _ in RULED_LINKS)
          or NOTHING),
       len(RULED_LINKS) == 1, [lbl for _, lbl, _ in RULED_LINKS])
    for url, label, record in RULED_LINKS:
        rec = REPO / record
        body = rec.read_text(encoding="utf-8", errors="replace") \
            if rec.is_file() else ""
        ok("the ruling that admits %s exists in the tree and carries the whole "
           "URL (%d character(s) read from %s)"
           % (label, len(body), record.rsplit("/", 1)[-1]),
           rec.is_file() and url in body,
           "exists=%s urlInRecord=%s" % (rec.is_file(), url in body))

    print("\n  REJECTING FIXTURES, one per rule, all synthetic:\n")
    # THE SPLIT, REJECTING, FOUR WAYS, AND THE PAIRED READING THE RETIREMENT
    # NEEDS. Each fixture differs from GOOD_BRIEF in ONE part of the sentence,
    # and each is read twice in the same run: the DETECTOR still refuses it (so
    # the guard the Sunday summary inherits is alive, and still tells a brief
    # that calls the count POINTS from one that says sessions, which is the exact
    # failure the 2026-09-05 ruling refuses) and the BRIEF REGISTER no longer
    # does (so the retirement is real and not a comment). One of these two going
    # quiet is the whole risk of this move.
    for want, text in BAD_BRIEF.items():
        budget_body = " ".join(split_sections(text)[0].get("BUDGET", []))
        found_n, missing = split_parts(budget_body)
        rr = check(text, "brief", FIXTURE_NOW)
        rules = {f.rule for f in rr["findings"]}
        ok("%-46s is refused by the kept detector (%d of %d part(s), missing "
           "%s) and is NOT refused by the brief register any more (%s)"
           % (want, found_n, len(SPLIT_PARTS),
              cap(missing, keep=5, sep=", "),
              "/".join(sorted(rules)) or "no finding"),
           bool(missing) and found_n < len(SPLIT_PARTS) and not rules
           and rr["split_found"] is None,
           "detectorMissing=%s registerFindings=%s splitFound=%s"
           % (missing, sorted(rules) or "nothing", rr["split_found"]))

    # AND THE BRIEF REGISTER MUST STILL REFUSE. The retirement took two things
    # off the brief's list, and the way that becomes a HOLE instead is if the
    # other rules quietly stopped biting in this register too, so three of them
    # are fixtured here against the brief's own cap and its own required list.
    # `shape` is the one that matters most: it still demands the four sections
    # that were never retired.
    for label, want, text in BAD_BRIEF_SURVIVING:
        rr = check(text, "brief", FIXTURE_NOW)
        rules = {f.rule for f in rr["findings"]}
        ok("%-42s is still refused in the BRIEF register by `%s` and nothing "
           "else (%d of %d word(s), %d of %d required section(s))"
           % (label, want, rr["words"], rr["cap"],
              len(rr["sections_required_found"]),
              len(rr["sections_required"])),
           rules == {want},
           "found %s" % (sorted(rules) or "nothing"))

    # THE READING ASK, REJECTING, FOUR WAYS, each refused by `reading` AND BY
    # NOTHING ELSE, so a fixture that fails for some unrelated reason cannot
    # certify this rule. The line the rule graded and the parts it missed are
    # printed on every row, because "the brief has no ask" and "the ask is
    # three lines down" are different faults and a reader given only the rule
    # name cannot tell them apart.
    for label, want, text in BAD_BRIEF_READING:
        rr = check(text, "brief", FIXTURE_NOW)
        rules = {f.rule for f in rr["findings"]}
        ok("%-52s is refused by `%s` and nothing else (%d of %d part(s) on "
           "line %d, missing %s)"
           % (label, want, rr["reading_found"], rr["reading_of"],
              rr["reading_line_no"],
              cap(rr["reading_missing"], keep=3, width=46, sep="; ")),
           rules == {want} and rr["reading_found"] < rr["reading_of"],
           "found=%s rules=%s line=%r"
           % (rr["reading_found"], sorted(rules) or "nothing",
              rr["reading_line"][:60]))

    for want, text in BAD.items():
        rr = check(text, "unprompted", FIXTURE_NOW)
        rules = {f.rule for f in rr["findings"]}
        ok("%-22s is refused, and by its own rule" % want,
           want in rules,
           "found %s" % (sorted(rules) or "nothing"))

    # THE FIXTURES MUST DIFFER FROM THE ACCEPTING ONE IN ONE THING ONLY. A
    # fixture that trips three rules proves the check is loud, not that it is
    # right, and the day one rule stops working the fixture still goes red.
    noisy = []
    for want, text in BAD.items():
        rules = {f.rule for f in
                 check(text, "unprompted", FIXTURE_NOW)["findings"]}
        if len(rules) > 1:
            noisy.append("%s->%s" % (want, "/".join(sorted(rules))))
    ok("each rejecting fixture trips exactly one rule (%d of %d clean)"
       % (len(BAD) - len(noisy), len(BAD)), not noisy,
       cap(noisy, keep=4, sep=", "))

    ok("the word cap does not charge for a required link",
       count_words("hello https://github.com/a/b there") == ["hello", "there"],
       count_words("hello https://github.com/a/b there"))
    ok("a URL is never read as a file path",
       not find_paths(scrub_links("see https://github.com/a/b/c.md")),
       find_paths(scrub_links("see https://github.com/a/b/c.md")))
    ok("and/or and 24/7 are not file paths",
       not find_paths("and/or 24/7"), find_paths("and/or 24/7"))
    ok("a date, a duration and a price are not counts",
       not find_counts("by 2026-09-07, within 24 hours, £250 left"),
       find_counts("by 2026-09-07, within 24 hours, £250 left"))
    ok("a bare quantity IS a count", find_counts("72 gates pass") == ["72"],
       find_counts("72 gates pass"))
    ok("a question is not claim-shaped",
       not claim_shaped("Is the street done?", "Is the street done?"))
    ok("a recommendation line is not claim-shaped",
       not claim_shaped("RECOMMENDATION B, it is a port town.",
                        "RECOMMENDATION B, it is a port town."))
    ok("a plain assertion IS claim-shaped",
       claim_shaped("The street has textures.", "The street has textures."))

    # ---------------------------------------------------------- THE GATE
    # ACCEPTING FIRST, and twice: the LIVE REPOSITORY is the accepting fixture
    # for a tool that checks this project (doing the work the gate prompts can
    # never break the gate), and a synthetic tree covers the shapes the live
    # repo does not currently hold. The rejecting fixtures are synthetic to
    # the last file: a rejecting case pinned to a real brief breaks the day
    # somebody rewrites the brief.
    print("\n  THE GATE, ACCEPTING CASES FIRST:\n")
    # EVERY GATE RUN THIS SUITE MAKES, COUNTED. The summary line used to add a
    # hand-maintained +3 to the fixture count, which is a denominator that
    # drifts the first time somebody adds a case.
    gate_runs = []

    def gate_run(*a, **kw):
        g = gate(*a, **kw)
        gate_runs.append(g)
        return g

    good_tree = _gate_tree({
        "production/outbox/README.md": "# documentation, not a message\n",
        "production/outbox/2026-09-03-street.unprompted.md": GOOD,
        "production/briefs/2026-09-02.md":
            "PRODUCER-REGISTER-EXEMPT: a director brief, written before the "
            "register was ruled.\n\n" + ("word " * 400),
    })
    g = gate_run(good_tree, FIXTURE_NOW,
                 pre_register=("production/briefs/2026-09-02.md",))
    ok("a compliant outbox message passes the gate", not g["failed"],
       g["failed"])
    # THE VERBATIM RESEARCH EXEMPTION AT THE GATE, ACCEPTING CASE FIRST, and
    # both rungs of the ladder in ONE walk. SYNTHETIC to the last byte: the
    # frozen list is injected, so this case cannot break the day a real
    # delivery is sent and cleared off the outbox.
    RTXT = ("The man whose job it is opens the yard gate.\n"
            "[the gallery](https://jsab258.github.io/ledger/gallery.html)"
            "\n")
    rel_in = "production/outbox/2026-09-14-research-in.answer.md"
    rel_out = "production/outbox/2026-09-14-research-out.answer.md"
    v_tree = _gate_tree({rel_in: RTXT, rel_out: RTXT,
                         "production/briefs/README.md": "# not a message\n"})
    gv = gate_run(v_tree, FIXTURE_NOW, research_verbatim=(rel_in,))
    ok("a listed research delivery passes the gate with ordinary English in it",
       not any(rel == rel_in for rel, _w in gv["failed"]), gv["failed"])
    ok("and the SAME text off the list still fails the gate on the ban list, "
       "so the exemption is a name and not a hole",
       any(rel == rel_out and "banned" in w for rel, w in gv["failed"]),
       gv["failed"])
    ok("the walk counts what it waived over both denominators (%d/%d graded, "
       "bit %s)" % (gv["research_graded"], gv["research_listed"],
                    research_bit_key(gv)),
       (gv["research_graded"], gv["research_listed"],
        gv["research_waiver_bit"], gv["research_findings_waived"])
       == (1, 1, 1, 1),
       (gv["research_graded"], gv["research_listed"],
        gv["research_waiver_bit"], gv["research_findings_waived"]))
    ok("and the file's own line names the waiver where the file is named",
       any(rel == rel_in and "research-verbatim:banned-waived" in w
           for rel, _s, w in gv["results"]), gv["results"])
    # REJECTING FIXTURE FOR THE ROT CHECK: a frozen entry with no file behind
    # it is a note with a count, never a silent zero.
    gv2 = gate_run(v_tree, FIXTURE_NOW,
                   research_verbatim=("production/outbox/never-existed"
                                      ".answer.md",))
    ok("a frozen RESEARCH_VERBATIM entry that no longer exists is counted, "
       "not silent (%d of %d)" % (len(gv2["research_absent"]),
                                  gv2["research_listed"]),
       len(gv2["research_absent"]) == 1 and gv2["research_graded"] == 0
       and gv2["research_waiver_bit"] == 0, gv2["research_absent"])
    ok("and a walk with no listed delivery in it prints the WORDS rather than "
       "a zero over a zero (%s)" % research_bit_key(gv2),
       research_bit_key(gv2).startswith(NOTHING)
       and " " not in research_bit_key(gv2), research_bit_key(gv2))
    ok("and the README is exempt BY NAME, counted, not skipped in silence",
       g["exempt"] == 2 and g["walked"] == 3 and g["checked"] == 1,
       (g["exempt"], g["walked"], g["checked"]))
    ok("a marked file on the frozen list is exempt however badly it reads",
       any(s == "exempt" and "pre-register" in w
           for _, s, w in g["results"]), g["results"])
    # THE LIVE REPOSITORY, WITH THE GRANDFATHERING READING NAMED. "0 failed"
    # alone cannot tell a clean tree from one where every file was let through
    # the link band by the legacy list, so the numerator and its denominator
    # are asserted together on this line.
    g_live = gate_run(REPO, FIXTURE_NOW)
    # THE DENOMINATORS ARE TIED TO THE FROZEN LIST, NOT TYPED. This assertion
    # read `checked == 4` until 2026-09-06 and by then the outbox held six
    # message files, so it was red on a tree nobody had broken: a hand-typed
    # count of a directory other sessions write to is a landmine, and this one
    # went off inside ledger/verify.py. What it was standing in for is the
    # property below: every name on the frozen list was either graded under the
    # retired rules or is gone (and printed as gone), never silently graded
    # under today's, and the walk examined at least those files.
    ok("the live repository passes the gate it was written against "
       "(filesChecked=%d filesLegacyLinks=%d/%d legacyAbsent=%d of the %d "
       "frozen name(s))"
       % (g_live["checked"], g_live["legacy_links"], g_live["checked"],
          len(g_live["legacy_absent"]), len(LEGACY_LINK_RULES)),
       not g_live["failed"]
       and g_live["legacy_links"] + len(g_live["legacy_absent"])
       == len(LEGACY_LINK_RULES)
       and g_live["checked"] >= g_live["legacy_links"],
       cap([f[0] for f in g_live["failed"]], keep=3))
    # THE ACCEPTING CASE FOR THE RETIREMENT, AND IT IS THE LIVE TREE: today's
    # real brief is in this walk, and it is the message that exposed the conflict
    # between the 2026-09-05 split order and the 2026-09-09 director test. A
    # synthetic brief could only show that the rule is off; only the live briefs
    # show that the messages the Producer actually writes now pass. Read off the
    # walk above rather than a second one, and the zero ships its denominator:
    # a tree with no brief in it fails this rather than reading as clean.
    live_briefs = [(rel, st) for rel, st, why in g_live["results"]
                   if why.startswith("brief,")]
    ok("every brief in the LIVE tree passes the brief register as it stands "
       "after the retirement, today's real message among them "
       "(briefsChecked=%d filesChecked=%d splitEnforcedOn=%d/%d)"
       % (len(live_briefs), g_live["checked"], g_live["split_enforced"],
          g_live["checked"]),
       # splitEnforcedOn is PRINTED and deliberately NOT BOUNDED here. It reads
       # 0 today; the day the Sunday summary picks the rule up it rises, and a
       # bound of zero would be a test that reddens when the ruling is honoured.
       bool(live_briefs) and len(live_briefs) == g_live["brief_files"]
       and all(st.startswith("pass") for _, st in live_briefs),
       cap(["%s %s" % (rel, st) for rel, st in live_briefs
            if not st.startswith("pass")], keep=3, width=80)
       or "briefs=%d" % len(live_briefs))
    # THE LIVE SERIES FOR THE ANNOTATION, AND THE ROT CHECK Jafar's ruling
    # needs: the two annotated messages pass WITH a line uncounted, the third
    # frozen name carries no annotation and is counted in full, and all three
    # pass. A number that could only be read off one file would not show that.
    live_hist = {rel: (state, why) for rel, state, why in g_live["results"]
                 if rel in LEGACY_LINK_RULES}
    ok("all %d frozen name(s) pass on the live tree, %d of them with one "
       "annotation line uncounted and the rest counted in full "
       "(historicalLinesUncounted=%d/%d)"
       % (len(live_hist), g_live["historical_uncounted"],
          g_live["historical_uncounted"], g_live["historical_listed"]),
       len(live_hist) + len(g_live["legacy_absent"]) == len(LEGACY_LINK_RULES)
       and all(st.startswith("pass") for st, _ in live_hist.values())
       and g_live["historical_listed"] == len(LEGACY_LINK_RULES)
       and sum(1 for _, why in live_hist.values()
               if "historicalUncounted=" in why)
       == g_live["historical_uncounted"],
       cap(["%s %s" % (rel, st) for rel, (st, _) in sorted(live_hist.items())],
           keep=3, width=80))

    # THE RULED WHOLE-URL EXCEPTION THROUGH THE GATE, ACCEPTING: the digest
    # under the exact name it will be sent as. The tree is synthetic only
    # because the message is HELD out of the outbox while this lands, so a
    # refusal cannot redden ledger/verify.py mid-build; the live reading is the
    # next case and it is the one that moves when the resident moves the file.
    ruled_name = ("production/outbox/"
                  "2026-09-09-atlas-02-research-digest.unprompted.md")
    # BOTH RULED TREES EXIST IN THIS FIXTURE, unlike the trees above, because
    # these two runs are read through gate_report() and gate_report returns on
    # a MISSING TREE before it prints any done line at all. A fixture with one
    # tree missing would have tested the missing-tree branch while claiming to
    # test the key. The suite found that, which is the reason the formatter is
    # driven here rather than trusted.
    ruled_tree = _gate_tree({"production/outbox/README.md": "# docs\n",
                             "production/briefs/README.md": "# docs\n",
                             ruled_name: RULED_DIGEST})
    g_ruled = gate_run(ruled_tree, FIXTURE_NOW)
    ok("the digest passes the gate under its own unprompted name and the "
       "FILE'S OWN line names the exception it used (linksRuledUsed=%d/%d, in "
       "%d of %d checked file(s))"
       % (g_ruled["links_ruled_used"], g_ruled["links_ruled_of"],
          len(g_ruled["links_ruled_files"]), g_ruled["checked"]),
       not g_ruled["failed"] and g_ruled["checked"] == 1
       and g_ruled["links_ruled_used"] == 1
       and g_ruled["links_ruled_files"] == [ruled_name]
       and any(("ruled-link:" + RULED_LABEL) in why
               for _, st, why in g_ruled["results"] if st.startswith("pass")),
       cap([why for _, _, why in g_ruled["results"]], keep=2, width=90))
    # THE LIVE SERIES, PRINTED AND DELIBERATELY NOT BOUNDED. While the message
    # is held the honest live reading is 0 of 1, which is exactly why the zero
    # ships its denominator; when it lands in the outbox this becomes 1 of 1 and
    # names the file. No bound is set on how many messages may carry the
    # exception: this is the printer, and that bound would be a number nobody
    # has measured. What IS asserted is that the denominator is the tuple and
    # that every file listed contributed at least one match.
    ok("the live walk prints its ruled-URL reading with its denominator "
       "(linksRuledUsed=%d/%d across %d checked file(s), in %s)"
       % (g_live["links_ruled_used"], g_live["links_ruled_of"],
          g_live["checked"],
          "/".join(g_live["links_ruled_files"]) or NOTHING),
       g_live["links_ruled_of"] == len(RULED_LINKS)
       and g_live["links_ruled_used"] >= len(g_live["links_ruled_files"]),
       (g_live["links_ruled_used"], g_live["links_ruled_files"]))
    # THE KEY ON BOTH DONE LINES, READ OFF THE PRINTER RATHER THAN TRUSTED.
    # gate_report() is where the key is formatted, so the suite drives it and
    # greps the line: an unrun formatter printing a plausible string is the
    # silent-instrument failure this project has already paid for.
    import contextlib
    import io

    def gate_done_line(g):
        """(exit code, the done line) from the real printer."""
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = gate_report(g)
        done = [ln.strip() for ln in buf.getvalue().splitlines()
                if ln.startswith("producer-check --gate:")]
        return code, (done[-1] if done else NOTHING)

    code_pass, line_pass = gate_done_line(g_ruled)
    ok("the PASS done line carries linksRuledUsed beside filesLegacyLinks, "
       "exit %d: %s" % (code_pass, line_pass),
       code_pass == GATE_EXIT_OK and "linksRuledUsed=1/1" in line_pass
       and "filesLegacyLinks=" in line_pass, line_pass)
    near_tree = _gate_tree({
        "production/outbox/README.md": "# docs\n",
        "production/briefs/README.md": "# docs\n",
        "production/outbox/2026-09-09-near-miss.unprompted.md":
            RULED_DIGEST.replace(RULED_URL, RULED_URL + "x")})
    g_near = gate_run(near_tree, FIXTURE_NOW)
    code_fail, line_fail = gate_done_line(g_near)
    ok("the same digest with ONE CHARACTER appended to the URL is refused by "
       "the gate, and the FAIL done line carries the reading as 0 of 1 rather "
       "than as a bare zero, exit %d: %s" % (code_fail, line_fail),
       code_fail == GATE_EXIT_FAIL and "linksRuledUsed=0/1" in line_fail
       and len(g_near["failed"]) == 1
       and "linkdest" in " ".join(w for _, w in g_near["failed"]), line_fail)

    # THE CASE QUEUE ITEM 077 WAS FILED FOR, and it is an ACCEPTING one. The
    # live message dated 2026-09-03 carries DEADLINE 2026-09-06; at a simulated
    # now of 2026-09-08 that deadline has been served. A served deadline is a
    # historical fact, not a quality fault. Before the fix this case failed,
    # and because ledger/verify.py runs this gate it would have deleted the
    # verification footer and blocked every commit from 2026-09-05T09:01 with
    # nobody having touched the tree.
    served = datetime.datetime(2026, 9, 8, 12, 0)
    g_served = gate_run(REPO, served)
    ok("the live repo passes with its own deadline SERVED (simulated now %s, "
       "%d file(s) actually checked, %d of them date-pinned)"
       % (served.date().isoformat(), g_served["checked"],
          g_served["date_pinned"]),
       not g_served["failed"] and g_served["checked"] >= 1,
       cap(["%s: %s" % f for f in g_served["failed"]], keep=2, width=90)
       if g_served["failed"] else "checked=%d" % g_served["checked"])

    # THE LADDER: one tree, one vantage, three instants, all in this run.
    # Differences between rungs are the only reading a ladder yields, and the
    # ruled property here is that there are none. A rung taken in a later run
    # would be a different photograph, so all three are taken together.
    rungs = [datetime.datetime(2026, 9, 3, 12, 0),
             datetime.datetime(2026, 9, 8, 12, 0),
             datetime.datetime(2027, 1, 1, 12, 0)]
    verdicts = [tuple(sorted(f[0] for f in gate_run(REPO, t)["failed"]))
                for t in rungs]
    ok("the gate's verdict does not move with the run's clock (%d rung(s): %s)"
       % (len(rungs), "/".join(t.date().isoformat() for t in rungs)),
       len(set(verdicts)) == 1,
       "/".join(str(len(v)) + "-failed" for v in verdicts))

    ok("a file's clock is midnight of the ISO date in its own name",
       gate_clock("production/outbox/2026-09-03-x.unprompted.md")[0]
       == datetime.datetime(2026, 9, 3, 0, 0),
       gate_clock("production/outbox/2026-09-03-x.unprompted.md")[0])

    # THE WALL-CLOCK REGRESSION DETECTOR, and the reason its dates are built
    # from today rather than written down: the DIFFERENCE is the fixture, not
    # the date. Named two days ago, deadline today, so the pinned reading is
    # always 57.0 hours (a pass) and the wall-clock reading is always 9.0 hours
    # or less (a refusal). It is armed on every day it ever runs.
    wall = datetime.datetime.now()
    named_day = (wall.date() - datetime.timedelta(days=2)).isoformat()
    pinned_tree = _gate_tree({
        "production/outbox/README.md": "# docs\n",
        "production/outbox/%s-served.unprompted.md" % named_day:
            GOOD.replace("DEADLINE 2026-09-07.",
                         "DEADLINE %s." % wall.date().isoformat()),
    })
    gp = gate_run(pinned_tree, wall)
    ok("a deadline 57h after its file's own date passes at the REAL wall "
       "clock, where the same deadline is under 9h (%d of %d checked file(s) "
       "date-pinned)" % (gp["date_pinned"], gp["checked"]),
       not gp["failed"] and gp["date_pinned"] == 1 and gp["checked"] == 1,
       "%s checked=%d" % (cap(["%s: %s" % f for f in gp["failed"]], keep=1,
                              width=90), gp["checked"]))

    # THE LADDER: ONE MESSAGE TEXT, ONE FILENAME, ONE DATE, TWO RULEBOOKS, ONE
    # RUN. Only membership of the frozen name list changes between the rungs,
    # and BOTH rungs carry the same 2026-09-05 date in the name. That is the
    # whole reading: the date cannot decide, so a message written next week
    # under a 2026-09-05 name cannot buy itself the retired rules. The text is
    # the shape Jafar rejected, ten repository links.
    ten_links = GOOD
    for i in range(10):
        ten_links = ten_links.replace(
            "Everything else waited on that.",
            "Everything else waited on that. [q%d](https://github.com/jsab258/"
            "wc26-picks/blob/main/production/q%d.md)" % (i, i), 1)
    rung_name = "production/outbox/2026-09-05-links.unprompted.md"
    rung_tree = _gate_tree({"production/outbox/README.md": "# docs\n",
                            rung_name: ten_links})
    listed = gate_run(rung_tree, FIXTURE_NOW, legacy_links=(rung_name,))
    unlisted = gate_run(rung_tree, FIXTURE_NOW,
                        legacy_links=LEGACY_LINK_RULES)
    unlisted_why = " ".join(w for _, w in unlisted["failed"])
    ok("the SAME text under the SAME name dated 2026-09-05 passes when the "
       "name is LISTED (failed=%d, filesLegacyLinks=%d/%d) and is refused when "
       "it is not (failed=%d), by linkcap and linkdest"
       % (len(listed["failed"]), listed["legacy_links"], listed["checked"],
          len(unlisted["failed"])),
       not listed["failed"] and listed["legacy_links"] == 1
       and len(unlisted["failed"]) == 1 and unlisted["legacy_links"] == 0
       and "linkcap" in unlisted_why and "linkdest" in unlisted_why,
       cap([unlisted_why], keep=1, width=140))

    # THE SECOND LADDER, THE SAME SHAPE ONE RULE ALONG: ONE TEXT, ONE NAME,
    # ONE DATE, TWO RULEBOOKS, ONE RUN, and the rung is the annotation. The
    # name carries the same 2026-09-05 date on both rungs, so the date cannot
    # decide; only membership of the frozen list can. This is the difference
    # between an exclusion pinned to three files and an exclusion any message
    # can buy by typing a word at the top.
    hist_name = "production/outbox/2026-09-05-historical.unprompted.md"
    hist_tree = _gate_tree({"production/outbox/README.md": "# docs\n",
                            hist_name: HIST_ONE})
    h_listed = gate_run(hist_tree, FIXTURE_NOW, legacy_links=(hist_name,))
    h_unlisted = gate_run(hist_tree, FIXTURE_NOW, legacy_links=())
    h_why = " ".join(w for _, w in h_unlisted["failed"])
    ok("the SAME text under the SAME name dated 2026-09-05 passes when the "
       "name is LISTED (failed=%d historicalLinesUncounted=%d/%d) and is "
       "refused by wordcap when it is not (failed=%d "
       "historicalLinesUncounted=%d/%d)"
       % (len(h_listed["failed"]), h_listed["historical_uncounted"],
          h_listed["historical_listed"], len(h_unlisted["failed"]),
          h_unlisted["historical_uncounted"], h_unlisted["historical_listed"]),
       not h_listed["failed"] and h_listed["historical_uncounted"] == 1
       and h_listed["historical_listed"] == 1
       and len(h_unlisted["failed"]) == 1 and "wordcap" in h_why
       and h_unlisted["historical_uncounted"] == 0,
       cap([h_why], keep=1, width=120))
    # AND THE UNCOUNTED LINE IS ON THE FILE'S OWN LINE, not only in the footer.
    ok("the passing file's own line names the uncounted annotation",
       any("historicalUncounted=1line/" in why
           for _, st, why in h_listed["results"] if st.startswith("pass")),
       cap([why for _, _, why in h_listed["results"]], keep=2, width=90))

    print("\n  THE GATE, REJECTING FIXTURES, all synthetic:\n")
    gate_bad = {
        "a message that breaks its register":
            ({"production/outbox/README.md": "# docs\n",
              "production/outbox/2026-09-03-x.unprompted.md":
                  BAD["banned:file path"]}, ()),
        "a filename carrying no register":
            ({"production/outbox/README.md": "# docs\n",
              "production/outbox/2026-09-03-x.md": GOOD}, ()),
        "the exempt marker on a file the frozen list does not name":
            ({"production/outbox/README.md": "# docs\n",
              "production/briefs/2026-09-04.md":
                  "PRODUCER-REGISTER-EXEMPT: let me through\n" +
                  ("word " * 400)}, ()),
        "a file on the frozen list that carries no marker":
            ({"production/outbox/README.md": "# docs\n",
              "production/briefs/2026-09-02.md": ("word " * 400)},
             ("production/briefs/2026-09-02.md",)),
        "an empty message file":
            ({"production/outbox/README.md": "# docs\n",
              "production/outbox/2026-09-03-x.answer.md": "   \n"}, ()),
        # THE FAILURE MODE THE FIX MUST NOT HAVE. Pinning the clock to the
        # filename date could have disabled the deadline rule instead of
        # repairing it, and a suite where both the served deadline and the
        # short one pass would not be able to tell the difference. This file's
        # deadline falls on the same day as its name, which is 9.0 hours from
        # the midnight pin, and it is refused at any run clock.
        "a same-day deadline, which the filename pin must NOT excuse":
            ({"production/outbox/README.md": "# docs\n",
              "production/outbox/2026-09-03-x.unprompted.md":
                  GOOD.replace("DEADLINE 2026-09-07.",
                               "DEADLINE 2026-09-03.")}, ()),
        # AND THE OTHER WAY ROUND THE FLOOR: no date in the name, so no instant
        # to measure from. It is a finding rather than a skip, or dropping the
        # date prefix would be the new escape hatch.
        "a deadline in a file whose name carries no date to pin to":
            ({"production/outbox/README.md": "# docs\n",
              "production/outbox/street.unprompted.md": GOOD}, ()),
        # THE SHAPE JAFAR REJECTED: a link to a repository markdown file, in
        # a file the frozen legacy list does not name.
        "a repository markdown link in a message no legacy list names":
            ({"production/outbox/README.md": "# docs\n",
              "production/outbox/2026-09-06-x.unprompted.md":
                  BAD["linkdest"]}, ()),
        "three links in a message no legacy list names":
            ({"production/outbox/README.md": "# docs\n",
              "production/outbox/2026-09-06-y.unprompted.md":
                  BAD["linkcap"]}, ()),
    }
    # WHICH RULE REFUSED IT, for the fixtures where the reason is the point. A
    # clock fixture refused for a shape fault would pass this loop while
    # proving nothing about the clock, which is the shape of a validator that
    # rejects everything.
    gate_bad_reason = {
        "a same-day deadline, which the filename pin must NOT excuse":
            "deadline: item 1 gives 9.0 hour(s)",
        "a deadline in a file whose name carries no date to pin to":
            "carries no date to measure it from",
        "a repository markdown link in a message no legacy list names":
            "linkdest: 1 of 2 link(s) point somewhere other than",
        "three links in a message no legacy list names":
            "linkcap: 3 link(s), 1 over the ruled cap of 2",
    }
    for name, (files, frozen) in gate_bad.items():
        gr = gate_run(_gate_tree(files), FIXTURE_NOW, pre_register=frozen)
        want = gate_bad_reason.get(name)
        why = " ".join(w for _, w in gr["failed"])
        ok("%-52s is refused%s" % (name, (", by its own rule" if want else "")),
           bool(gr["failed"]) and (want is None or want in why),
           "walked %d, failed %d: %s" % (gr["walked"], len(gr["failed"]),
                                         cap([why], keep=1, width=90)))
    # THE TREE THAT DOES NOT EXIST. Jafar's warning made flesh: this project
    # retired a file this morning that three readers were still pointed at.
    empty_root = _gate_tree({"production/notes.md": "hello\n"})
    ge = gate_run(empty_root, FIXTURE_NOW, pre_register=())
    ok("a MISSING outbox tree is red, never an empty walk reading as clean",
       len(ge["missing_trees"]) == 2, ge["missing_trees"])
    # THE FROZEN LIST CANNOT ROT IN SILENCE.
    gm = gate_run(good_tree, FIXTURE_NOW,
                  pre_register=("production/briefs/2026-09-02.md",
                                "production/briefs/gone.md"))
    ok("a frozen entry that no longer exists prints as a note, not a red",
       gm["listed_absent"] == ["production/briefs/gone.md"] and not gm["failed"],
       (gm["listed_absent"], gm["failed"]))
    # THE SAME ROT CHECK ON THE OTHER FROZEN LIST. Every name on the live
    # LEGACY_LINK_RULES exists today, so without this the branch would never
    # run and could be broken for months without a red.
    gz = gate_run(good_tree, FIXTURE_NOW,
                  pre_register=("production/briefs/2026-09-02.md",),
                  legacy_links=("production/outbox/never-existed.md",))
    ok("a LEGACY_LINK_RULES entry that no longer exists prints as a note, not "
       "a red (legacyAbsent=%d of %d listed)"
       % (len(gz["legacy_absent"]), 1),
       gz["legacy_absent"] == ["production/outbox/never-existed.md"]
       and not gz["failed"] and gz["legacy_links"] == 0,
       (gz["legacy_absent"], gz["failed"]))

    # ----------------------------- THE LINK FLOOR'S ONE CONDITION, 2026-09-11
    # ACCEPTING CASE FIRST, and the accepting case is the one that mattered on
    # the day this landed: a finished answer to a question Jafar asked from his
    # phone, sound on every other rule, refused on `linkfloor` alone, and
    # therefore never sent while he sat in silence.
    #
    # THE LADDER. ONE message, three rungs, ONE run, and the difference between
    # the rungs is ONE LINE IN ONE FILE: the marker says `none`, then names a
    # served commit, then is not there at all. Nothing else moves between them.
    # A rung compared across runs is a different photograph.
    print("\n  THE LINK FLOOR'S ONE CONDITION, ACCEPTING CASE FIRST:\n")
    # THE LIVE REPOSITORY IS THE ACCEPTING FIXTURE for the half of this tool
    # that reads the project (instruments.md), so DOING THE WORK THE MARKER
    # PROMPTS can never break the tool: printing a served commit into it moves
    # the reading, and this assertion pins the marker's SHAPE, never its value.
    live_floor = link_floor_state(REPO)
    ok("the live marker %s is readable and carries exactly 1 %s= line "
       "(linkFloorActive=%s reason=%s)"
       % (SERVED_MARKER_REL, SERVED_KEY,
          "true" if live_floor["active"] else "false", live_floor["reason"]),
       live_floor["marker_lines"] == 1,
       (live_floor["marker_lines"], live_floor["reason"]))
    # THE READER, DRIVEN DIRECTLY over five synthetic markers, because the two
    # strict branches (absent, malformed) cannot be reached from the live tree
    # and an unrun branch that a future session trusts is the silent-instrument
    # failure. SYNTHETIC to the last byte: a rejecting fixture pinned to the
    # real marker breaks the day queue 256 writes a served commit into it.
    floor_cases = (
        ("a marker saying none", "servedCommit=none servedRepo=none\n",
         False, "no-page-served-yet"),
        ("a marker naming a served commit",
         "servedCommit=0bc1def2 servedRepo=jsab258/ledger\n",
         True, "page-served"),
        ("a marker with no servedCommit line at all",
         "# a comment and nothing machine-readable\n", True,
         "marker-carries-0-"),
        ("a marker carrying two servedCommit lines",
         "servedCommit=none\nservedCommit=0bc1def2\n", True,
         "marker-carries-2-"),
    )
    for label, body, want_active, want_reason in floor_cases:
        st = link_floor_state(_gate_tree({SERVED_MARKER_REL: body}))
        ok("%-46s reads linkFloorActive=%s reason=%s"
           % (label, "true" if want_active else "false", st["reason"]),
           st["active"] is want_active and st["reason"].startswith(want_reason),
           (st["active"], st["reason"]))
    # THE CAP ON THE PRINTED VALUE, DRIVEN ON BOTH SIDES, because a cap that
    # never runs is a branch nobody has seen and a cap that bites in silence
    # reads as a finding. A whole sha is 40 characters and must NOT be cut.
    sha40 = "a" * SERVED_VALUE_WIDTH
    st_sha = link_floor_state(_gate_tree({SERVED_MARKER_REL:
                                          "servedCommit=%s\n" % sha40}))
    ok("a %d-character value (a whole sha) is printed WHOLE, uncut"
       % SERVED_VALUE_WIDTH,
       sha40 in st_sha["reason"] and not st_sha["reason"].endswith("..."),
       st_sha["reason"])
    st_long = link_floor_state(_gate_tree({SERVED_MARKER_REL:
                                           "servedCommit=%s\n" % ("b" * 200)}))
    ok("a 200-character value is cut to %d and the cut ANNOUNCES itself "
       "(reason ends %s)" % (SERVED_VALUE_WIDTH, st_long["reason"][-8:]),
       st_long["reason"].endswith("...")
       and ("b" * (SERVED_VALUE_WIDTH + 1)) not in st_long["reason"]
       and st_long["served"] == "b" * 200
       and " " not in st_long["reason"], st_long["reason"])
    st_absent = link_floor_state(_gate_tree({"production/other.txt": "x\n"}))
    ok("NO marker at all leaves the floor LIVE rather than open (reason=%s): "
       "the failure direction of an unreadable fact is refuse-loudly, never "
       "send-anyway" % st_absent["reason"],
       st_absent["active"] and st_absent["reason"].startswith("marker-absent")
       and st_absent["marker_lines"] == 0, st_absent)
    # THE TWO RUNGS THE REGISTER IS GRADED ON, read through the same reader the
    # live run uses, so the fixture and the tool cannot drift about what a
    # marker means.
    floor_off = link_floor_state(_gate_tree({SERVED_MARKER_REL:
                                             "servedCommit=none\n"}))
    floor_on = link_floor_state(_gate_tree({SERVED_MARKER_REL:
                                            "servedCommit=0bc1def2\n"}))
    # SYNTHETIC, and deliberately NOT the real answer sitting in the outbox: a
    # rejecting fixture pinned to a real message breaks the day the Producer
    # edits it, which is the rule every other fixture in this file follows.
    LINKLESS = ("HEADLINE: Yes. Your message reached the studio, and this "
                "reply is the proof travelling back the other way.\n\n"
                "Everything on your machine now works from the new folder "
                "rather than the old one, which is also why there is no link "
                "in this message: every page still shows the town as it was "
                "before the move.\n")
    r_off = check(LINKLESS, "answer", FIXTURE_NOW, link_floor=floor_off)
    ok("a linkless answer PASSES while no page is served (%d URL(s), "
       "effective floor %d of the ruled %d, 0 finding(s) over %d rule(s) "
       "enforced)"
       % (len(r_off["urls"]), r_off["link_min_effective"], LINK_MIN,
          len(r_off["enforced"])),
       not r_off["findings"] and r_off["link_min_effective"] == 0,
       [str(f) for f in r_off["findings"]])
    ok("and the suspended rule is NAMED rather than skipped in silence "
       "(rulesNotEnforced=%s)" % "/".join(r_off["not_enforced"]),
       "linkfloor" in r_off["not_enforced"]
       and "linkfloor" not in r_off["enforced"], r_off["not_enforced"])
    # REJECTING, RUNG TWO, AND THE MARKER IS PLANTED RATHER THAN REASONED
    # ABOUT. The same text, the same register, the same instant: the ONLY thing
    # that moved is the one line in the marker.
    r_on = check(LINKLESS, "answer", FIXTURE_NOW, link_floor=floor_on)
    ok("the SAME answer is refused again once a page IS served, by `linkfloor` "
       "and nothing else (effective floor %d of the ruled %d, found %s)"
       % (r_on["link_min_effective"], LINK_MIN,
          "/".join(sorted({f.rule for f in r_on["findings"]})) or "nothing"),
       {f.rule for f in r_on["findings"]} == {"linkfloor"}
       and r_on["link_min_effective"] == LINK_MIN,
       [str(f) for f in r_on["findings"]])
    # REJECTING, RUNG THREE: a caller that took NO reading gets the floor live.
    r_blind = check(LINKLESS, "answer", FIXTURE_NOW)
    ok("a caller that consulted no marker gets the floor LIVE and the reason "
       "says so (reason=%s), so a forgotten reading can only ever be stricter "
       "than the ruling" % r_blind["link_floor_reason"],
       {f.rule for f in r_blind["findings"]} == {"linkfloor"}
       and r_blind["link_floor_reason"] == FLOOR_NOT_CONSULTED,
       (r_blind["link_floor_reason"],
        [str(f) for f in r_blind["findings"]]))
    # THE DESTINATION LIST IS NOT LOOSENED, AND THIS IS THE HALF THAT PROVES
    # IT. "Zero links is legal" must not read as "any link is legal": a message
    # whose ONLY link points somewhere the band never permitted is still
    # refused with the floor suspended, by `linkdest` and nothing else.
    off_site_only = LINKLESS + ("[the card](https://github.com/jsab258/"
                                "ledger/blob/main/q.md)\n")
    r_bad_dest = check(off_site_only, "answer", FIXTURE_NOW,
                       link_floor=floor_off)
    ok("with the floor suspended, a message whose only link is NOT one of the "
       "%d permitted destinations is still refused by `linkdest` and nothing "
       "else (found %s)"
       % (len(SITE_PAGES),
          "/".join(sorted({f.rule for f in r_bad_dest["findings"]}))
          or "nothing"),
       {f.rule for f in r_bad_dest["findings"]} == {"linkdest"},
       [str(f) for f in r_bad_dest["findings"]])
    # AND THE CEILING IS NOT LOOSENED EITHER. The floor moved; the cap Jafar
    # ruled on 2026-09-06 did not.
    r_cap_off = check(BAD["linkcap"], "unprompted", FIXTURE_NOW,
                      link_floor=floor_off)
    ok("with the floor suspended, %d links is still over the ruled cap of %d "
       "and is refused by `linkcap` and nothing else (found %s)"
       % (len(r_cap_off["urls"]), LINK_MAX,
          "/".join(sorted({f.rule for f in r_cap_off["findings"]}))
          or "nothing"),
       {f.rule for f in r_cap_off["findings"]} == {"linkcap"},
       [str(f) for f in r_cap_off["findings"]])
    # A FLOOR THAT QUIETLY BECAME OPTIONAL EVERYWHERE IS NOT WHAT WAS RULED, so
    # EVERY rejecting fixture in this file is re-driven WITH THE FLOOR
    # SUSPENDED. All but one must still be refused by their own rule; the one
    # that now passes is `linkfloor` itself, which is the rule under
    # suspension, and it is NAMED rather than quietly dropped from the count.
    survived, suspended, lost = [], [], []
    for want, text in BAD.items():
        rules = {f.rule for f in check(text, "unprompted", FIXTURE_NOW,
                                       link_floor=floor_off)["findings"]}
        if want == "linkfloor":
            (suspended if not rules else lost).append(
                "%s->%s" % (want, "/".join(sorted(rules)) or "passes"))
        elif want in rules:
            survived.append(want)
        else:
            lost.append("%s->%s" % (want, "/".join(sorted(rules)) or "nothing"))
    ok("with the floor suspended, %d of the %d other rejecting fixture(s) are "
       "STILL refused by their own rule, and the %d that now passes is "
       "`linkfloor` itself"
       % (len(survived), len(BAD) - 1, len(suspended)),
       len(survived) == len(BAD) - 1 and len(suspended) == 1 and not lost,
       cap(lost, keep=4, sep=", "))
    # THE BRIEF REGISTER'S OTHER RULES, THE BAN LIST AND THE WORD CAP, re-driven
    # on the suspended rung for the same reason.
    rb_off = check(GOOD_BRIEF, "brief", FIXTURE_NOW, link_floor=floor_off)
    ok("the good brief still passes on the suspended rung (%d of %d word(s), "
       "%d of %d required section(s))"
       % (rb_off["words"], rb_off["cap"],
          len(rb_off["sections_required_found"]),
          len(rb_off["sections_required"])),
       not rb_off["findings"], [str(f) for f in rb_off["findings"]])
    for label, want, text in BAD_BRIEF_SURVIVING:
        rules = {f.rule for f in check(text, "brief", FIXTURE_NOW,
                                       link_floor=floor_off)["findings"]}
        ok("on the suspended rung, %-42s is STILL refused in the BRIEF "
           "register by `%s` and nothing else" % (label, want),
           rules == {want}, "found %s" % (sorted(rules) or "nothing"))
    # THE SAME LADDER AT THE GATE, because the gate is what holds the commit:
    # three trees identical but for the marker, walked in this run.
    floor_files = {"production/outbox/README.md": "# docs\n",
                   "production/outbox/2026-09-11-x.answer.md": LINKLESS}
    floor_rungs = []
    for label, extra, want_fail, want_reason in (
            ("no page served yet",
             {SERVED_MARKER_REL: "servedCommit=none\n"}, False,
             "no-page-served-yet"),
            ("a page IS served",
             {SERVED_MARKER_REL: "servedCommit=0bc1def2\n"}, True,
             "page-served"),
            ("no marker to read at all", {}, True, "marker-absent")):
        files = dict(floor_files)
        files.update(extra)
        gfl = gate_run(_gate_tree(files), FIXTURE_NOW, pre_register=())
        floor_rungs.append(gfl)
        ok("at the gate, a linkless answer with %-20s %s "
           "(linkFloorActive=%s reason=%s filesLinkFloorOff=%d/%d)"
           % (label, "FAILS" if want_fail else "passes",
              "true" if gfl["link_floor_active"] else "false",
              gfl["link_floor_reason"], gfl["link_floor_off"], gfl["checked"]),
           bool(gfl["failed"]) is want_fail
           and gfl["link_floor_reason"].startswith(want_reason)
           and gfl["link_floor_off"] == (0 if want_fail else gfl["checked"])
           and gfl["checked"] == 1
           and (not want_fail
                or "linkfloor" in " ".join(w for _, w in gfl["failed"])),
           (gfl["failed"], gfl["link_floor_reason"], gfl["link_floor_off"]))

    # ---------------------------- THE PRE-MOVE WAIVER, ACCEPTING CASE FIRST
    # ONE SYNTHETIC TREE, TOGGLED ONE CONTRIBUTOR AT A TIME, ALL IN THIS RUN.
    # Synthetic to the last byte, and the two message names are dated but do
    # not exist anywhere: clearing a real message out of the outbox can never
    # break this case, and the live tree can never make it pass by accident.
    # The marker in the tree names a served commit, so the floor is LIVE on
    # every rung and the waiver is the only thing that can move the verdict.
    print("\n  THE PRE-MOVE WAIVER AT THE GATE, ACCEPTING CASE FIRST:\n")
    # THE DATE IN EACH NAME IS THE INSTANT THAT BODY IS GRADED AT, because
    # gate_clock pins every file to its own name. GOOD carries DEADLINE
    # 2026-09-07, so the archive body is dated 2026-09-03 exactly as the other
    # GOOD-derived gate fixtures are; naming it 2026-09-08 made it fail on
    # `deadline` at -15.0 hours and proved nothing about the waiver.
    pm_linkless = "production/outbox/2026-09-11-pm-linkless.answer.md"
    pm_archive = "production/outbox/2026-09-03-pm-archive.unprompted.md"
    # DERIVED, NEVER TYPED: the archive body is the good body with the origin
    # swapped, so the day either constant moves this fixture moves with it.
    pm_tree_files = {"production/outbox/README.md": "# docs\n",
                     "production/briefs/README.md": "# docs\n",
                     pm_linkless: LINKLESS,
                     pm_archive: GOOD.replace(SITE_ORIGIN, ARCHIVE_ORIGIN),
                     SERVED_MARKER_REL: "servedCommit=0bc1def2\n"}
    pm_listed = (pm_linkless, pm_archive)
    g_pm = gate_run(_gate_tree(pm_tree_files), FIXTURE_NOW, pre_register=(),
                    pre_move=pm_listed)
    ok("ACCEPTING: %d listed message(s) of %d pass the gate with a page "
       "SERVED (linkFloorActive=%s, floorOff=%d/%d, waiverChangedVerdictOn="
       "%d/%d, %d finding(s) removed, rule(s) %s)"
       % (g_pm["pre_move_graded"], g_pm["pre_move_listed"],
          "true" if g_pm["link_floor_active"] else "false",
          g_pm["link_floor_off"], g_pm["checked"],
          g_pm["pre_move_waiver_bit"], g_pm["pre_move_graded"],
          g_pm["pre_move_findings_waived"],
          "/".join(g_pm["pre_move_rules"]) or NOTHING),
       not g_pm["failed"] and g_pm["link_floor_active"]
       and g_pm["pre_move_graded"] == 2 and g_pm["pre_move_waiver_bit"] == 2
       and g_pm["link_floor_off"] == 2 and g_pm["checked"] == 2
       and set(g_pm["pre_move_rules"]) == set(PRE_MOVE_WAIVED_RULES),
       (g_pm["failed"], g_pm["pre_move_rules"]))
    # THE SECOND RUNG: THE SAME TREE, THE SAME INSTANT, THE SAME MARKER, THE
    # LIST EMPTY. The difference between the rungs is the only number a ladder
    # yields, and a waiver that cannot be switched off is not a waiver.
    g_pm_off = gate_run(_gate_tree(pm_tree_files), FIXTURE_NOW,
                        pre_register=(), pre_move=())
    off_rules = set()
    for _rel, _w in g_pm_off["failed"]:
        off_rules.update(w.split(":")[0] for w in _w.split() if ":" in w)
    ok("REJECTING: the SAME two message(s) OFF the list FAIL the same walk "
       "(%d of %d checked, by %s), so the waiver is a name and not a hole"
       % (len(g_pm_off["failed"]), g_pm_off["checked"],
          "/".join(sorted(off_rules & set(PRE_MOVE_WAIVED_RULES))) or NOTHING),
       len(g_pm_off["failed"]) == 2 and g_pm_off["pre_move_graded"] == 0
       and g_pm_off["pre_move_waiver_bit"] == 0
       and set(PRE_MOVE_WAIVED_RULES) <= off_rules,
       (g_pm_off["failed"], sorted(off_rules)))
    # NARROWNESS, AND IT IS THE HALF THAT KEEPS A WAIVER FROM BECOMING A HOLE.
    # The waiver is exactly two rules wide. A listed file that breaks a THIRD
    # rule is still refused by it, and `linkcap` is the right third rule
    # because the move changed nothing about how many links a message carries.
    pm_capped = GOOD.replace(
        "[the gallery](%sgallery.html)" % SITE_ORIGIN,
        "[the gallery](%sgallery.html)\n[a](%smap.html)\n[b](%sworld.html)"
        % (ARCHIVE_ORIGIN, ARCHIVE_ORIGIN, ARCHIVE_ORIGIN))
    r_pm_cap = check(pm_capped, "unprompted", FIXTURE_NOW,
                     link_floor=floor_reading(True, "fixture..page-served",
                                              served="0bc1def2", lines=1),
                     pre_move=True)
    ok("REJECTING: a listed message over the ruled cap of %d is STILL refused "
       "by `linkcap` and by nothing else, so the waiver is %d rule(s) wide "
       "and not three (waived here: %s)"
       % (LINK_MAX, len(PRE_MOVE_WAIVED_RULES),
          "/".join(r_pm_cap["pre_move_waived"]) or NOTHING),
       {f.rule for f in r_pm_cap["findings"]} == {"linkcap"}
       and set(r_pm_cap["pre_move_waived"]) == set(PRE_MOVE_WAIVED_RULES),
       [str(f) for f in r_pm_cap["findings"]])
    # THE ROT CHECK, REJECTING: a frozen name no file answers is COUNTED, never
    # a silent zero. This is the list most likely to rot, because every name on
    # it is an archived message and archived messages get cleared out.
    g_pm_rot = gate_run(_gate_tree(pm_tree_files), FIXTURE_NOW,
                        pre_register=(),
                        pre_move=("production/outbox/never-existed.answer.md",))
    ok("REJECTING: a frozen PRE_MOVE_MESSAGES entry that no longer exists is "
       "counted, not silent (%d of %d listed, %d graded)"
       % (len(g_pm_rot["pre_move_absent"]), g_pm_rot["pre_move_listed"],
          g_pm_rot["pre_move_graded"]),
       g_pm_rot["pre_move_absent"] == ["production/outbox/never-existed"
                                       ".answer.md"]
       and g_pm_rot["pre_move_graded"] == 0
       and g_pm_rot["pre_move_waiver_bit"] == 0, g_pm_rot["pre_move_absent"])
    # ------------------------ THE PRE-READING WAIVER, ACCEPTING CASE FIRST
    # ONE SYNTHETIC TREE, TOGGLED ONE CONTRIBUTOR AT A TIME, ALL IN THIS RUN,
    # the shape of the pre-move ladder above. Synthetic to the last byte: the
    # brief name is dated but exists nowhere, so deleting or writing a real
    # brief can never break this case and the live tree can never make it pass
    # by accident.
    print("\n  THE PRE-READING WAIVER AT THE GATE, ACCEPTING CASE FIRST:\n")
    pr_old = "production/briefs/2026-09-04.md"
    pr_tree_files = {
        "production/outbox/README.md": "# docs\n",
        # THE OLD BRIEF IS GOOD_BRIEF WITH THE ASK TAKEN OFF, DERIVED AND NEVER
        # TYPED, so the day the ask's wording moves this fixture moves with it.
        pr_old: GOOD_BRIEF.replace(BRIEF_READING + "\n\n", ""),
        SERVED_MARKER_REL: "servedCommit=0bc1def2\n"}
    g_pr = gate_run(_gate_tree(pr_tree_files), FIXTURE_NOW, pre_register=(),
                    pre_move=(pr_old,), pre_reading=(pr_old,))
    ok("ACCEPTING: %d listed brief(s) of %d pass the gate with the reading "
       "rule LIVE (readingEnforcedOn=%d/%d, waiverChangedVerdictOn=%d/%d, "
       "%d finding(s) removed, rule(s) %s)"
       % (g_pr["pre_reading_graded"], g_pr["pre_reading_listed"],
          g_pr["reading_enforced"], g_pr["checked"],
          g_pr["pre_reading_waiver_bit"], g_pr["pre_reading_graded"],
          g_pr["pre_reading_findings_waived"],
          "/".join(g_pr["pre_reading_rules"]) or NOTHING),
       not g_pr["failed"] and g_pr["pre_reading_graded"] == 1
       and g_pr["pre_reading_waiver_bit"] == 1
       and g_pr["reading_enforced"] == 0 and g_pr["checked"] == 1
       and set(g_pr["pre_reading_rules"]) == set(PRE_READING_WAIVED_RULES),
       (g_pr["failed"], g_pr["pre_reading_rules"]))
    # THE SECOND RUNG: THE SAME TREE, THE SAME INSTANT, THE LIST EMPTY. The
    # difference between the rungs is the only number a ladder yields, and a
    # waiver that cannot be switched off is not a waiver.
    g_pr_off = gate_run(_gate_tree(pr_tree_files), FIXTURE_NOW,
                        pre_register=(), pre_move=(pr_old,), pre_reading=())
    off_reading = " ".join(w for _rel, w in g_pr_off["failed"])
    ok("REJECTING: the SAME brief OFF the list FAILS the same walk (%d of %d "
       "checked, readingEnforcedOn=%d/%d), so the waiver is a name and not a "
       "hole"
       % (len(g_pr_off["failed"]), g_pr_off["checked"],
          g_pr_off["reading_enforced"], g_pr_off["checked"]),
       len(g_pr_off["failed"]) == 1 and "reading" in off_reading
       and g_pr_off["pre_reading_graded"] == 0
       and g_pr_off["pre_reading_waiver_bit"] == 0
       and g_pr_off["reading_enforced"] == 1,
       (g_pr_off["failed"], g_pr_off["reading_enforced"]))
    # A BRIEF WRITTEN UNDER THE RULE NEEDS NO WAIVER AT ALL, which is the whole
    # point of the list being frozen: the same walk, the same empty list, the
    # ask restored. If this rung failed, the rule would be unsatisfiable and
    # the list would be load-bearing for ever.
    # THE DATE IN THE NAME IS THE INSTANT THIS BODY IS GRADED AT and selects no
    # rule: gate_clock pins every file to its own name, GOOD_BRIEF carries
    # DEADLINE 2026-09-07, and naming this 2026-09-16 made it fail on
    # `deadline` at -216 hours and proved nothing about the ask. Membership of
    # the waiver is by NAME and the list is EMPTY on this rung, so an early
    # date buys this fixture nothing.
    pr_new = "production/briefs/2026-09-03.md"
    g_pr_new = gate_run(_gate_tree({"production/outbox/README.md": "# docs\n",
                                    pr_new: GOOD_BRIEF,
                                    SERVED_MARKER_REL:
                                        "servedCommit=0bc1def2\n"}),
                        FIXTURE_NOW, pre_register=(), pre_move=(pr_new,),
                        pre_reading=())
    ok("ACCEPTING: a brief CARRYING the ask passes with the list empty "
       "(readingEnforcedOn=%d/%d, preReadingGraded=%d/%d), so the rule is "
       "satisfiable without the waiver"
       % (g_pr_new["reading_enforced"], g_pr_new["checked"],
          g_pr_new["pre_reading_graded"], g_pr_new["pre_reading_listed"]),
       not g_pr_new["failed"] and g_pr_new["reading_enforced"] == 1
       and g_pr_new["checked"] == 1 and g_pr_new["pre_reading_graded"] == 0,
       (g_pr_new["failed"], g_pr_new["reading_enforced"]))
    # NARROWNESS: the waiver is exactly one rule wide. A listed brief that
    # breaks a SECOND rule is still refused by it, and `shape` is the right
    # second rule because the ruling changed nothing about the sections.
    r_pr_shape = check(GOOD_BRIEF.replace(BRIEF_READING + "\n\n", "")
                                 .replace("HEADLINE: the town has textures",
                                          "The town has textures"),
                       "brief", FIXTURE_NOW,
                       link_floor=floor_reading(True, "fixture..page-served",
                                                served="0bc1def2", lines=1),
                       pre_reading=True)
    ok("REJECTING: a listed brief that also breaks `shape` is STILL refused by "
       "it, so the waiver is %d rule(s) wide and not two (waived here: %s)"
       % (len(PRE_READING_WAIVED_RULES),
          "/".join(r_pr_shape["pre_reading_waived"]) or NOTHING),
       {f.rule for f in r_pr_shape["findings"]} == {"shape"}
       and set(r_pr_shape["pre_reading_waived"])
       == set(PRE_READING_WAIVED_RULES),
       [str(f) for f in r_pr_shape["findings"]])
    # THE ROT CHECK, REJECTING: a frozen name no file answers is COUNTED, never
    # a silent zero.
    g_pr_rot = gate_run(_gate_tree(pr_tree_files), FIXTURE_NOW,
                        pre_register=(), pre_move=(pr_old,),
                        pre_reading=("production/briefs/never-existed.md",))
    ok("REJECTING: a frozen PRE_READING_BRIEFS entry that no longer exists is "
       "counted, not silent (%d of %d listed, %d graded)"
       % (len(g_pr_rot["pre_reading_absent"]), g_pr_rot["pre_reading_listed"],
          g_pr_rot["pre_reading_graded"]),
       g_pr_rot["pre_reading_absent"] == ["production/briefs/never-existed.md"]
       and g_pr_rot["pre_reading_graded"] == 0
       and g_pr_rot["pre_reading_waiver_bit"] == 0,
       g_pr_rot["pre_reading_absent"])
    # AND THE LIVE TREE, WHICH IS THE ACCEPTING FIXTURE THE LIST WAS SIZED
    # AGAINST. Every name on PRE_READING_BRIEFS must be a file this walk
    # actually graded, or the list is describing a tree that no longer exists.
    g_live_pr = gate_run(REPO, FIXTURE_NOW)
    ok("ACCEPTING, THE LIVE TREE: %d of the %d frozen PRE_READING_BRIEFS "
       "name(s) were graded in this walk and the waiver changed the verdict on "
       "%d of them; readingEnforcedOn=%d/%d of %d brief(s), %d file(s) failed"
       % (g_live_pr["pre_reading_graded"], g_live_pr["pre_reading_listed"],
          g_live_pr["pre_reading_waiver_bit"], g_live_pr["reading_enforced"],
          g_live_pr["checked"], g_live_pr["brief_files"],
          len(g_live_pr["failed"])),
       not g_live_pr["failed"] and not g_live_pr["pre_reading_absent"]
       and g_live_pr["pre_reading_graded"] == len(PRE_READING_BRIEFS)
       and g_live_pr["pre_reading_waiver_bit"]
       == g_live_pr["pre_reading_graded"],
       (g_live_pr["failed"][:2], g_live_pr["pre_reading_absent"]))

    # ---------------------- REJECTING, THE ARCHIVE ORIGIN ITSELF, 2026-09-15
    # THE FIRST DAY THIS CASE CAN FIRE. SITE_ORIGIN and ARCHIVE_ORIGIN were the
    # same string from 2026-09-10 until queue 256 landed, so "an archive link
    # is refused" was untestable and the constant kept for a rejecting fixture
    # had nothing to reject. THE PAIRED READING, one entry, both moments: the
    # same page path under each origin, graded in the same run.
    for label, origin, want_ok in (("the LIVE site", SITE_ORIGIN, True),
                                   ("the ARCHIVE", ARCHIVE_ORIGIN, False)):
        u = origin + "map.html"
        ok("%s: map.html under %s is %s by the destination band "
           "(sitePage=%s, linkOk=%s)"
           % ("ACCEPTING" if want_ok else "REJECTING", label,
              "ADMITTED" if want_ok else "REFUSED",
              site_page(u) or NOTHING, "true" if link_ok(u) else "false"),
           link_ok(u) is want_ok
           and (site_page(u) is not None) is want_ok
           and norm_url(SITE_ORIGIN) != norm_url(ARCHIVE_ORIGIN), u)

    # A1: rung 1 is the LIVE tree, rungs 2 and 3 are ONE SYNTHETIC tree graded
    # against two origins, so writing the sha queue 256 owes cannot break this.
    print("\n  A1, THE MARKER AGAINST SITE_ORIGIN, ACCEPTING CASE FIRST:\n")
    a1_tree = _gate_tree({"production/outbox/2026-09-03-street.unprompted.md":
                          GOOD, "production/briefs/README.md": "# docs\n",
                          SERVED_MARKER_REL: "servedCommit=0bc1def2\n"})
    for n, (want, label, g) in enumerate((
            # THE LABEL IS READ OFF THE CONSTANTS, NOT TYPED. It said
            # "SITE_ORIGIN the archive" until 2026-09-15 and would have gone on
            # saying it after queue 256 moved the constant, which is a label
            # describing a world the run is no longer in.
            (True, "the LIVE tree (%s=%s, SITE_ORIGIN=%s, archive=%s)"
             % (SERVED_KEY, cap([str(live_floor["served"])], keep=1, width=12),
                SITE_ORIGIN,
                "same" if norm_url(SITE_ORIGIN) == norm_url(ARCHIVE_ORIGIN)
                else "a-different-origin"), g_live),
            (False, "SYNTHETIC servedCommit=0bc1def2 against ARCHIVE_ORIGIN",
             gate_run(a1_tree, FIXTURE_NOW, pre_register=(),
                      site_origin=ARCHIVE_ORIGIN)),
            (True, "the SAME tree against the origin queue 256 produced",
             gate_run(a1_tree, FIXTURE_NOW, pre_register=(),
                      site_origin=SITE_ORIGIN))), 1):
        code, line = gate_done_line(g)
        ok("A1 rung %d, %s, %s: markerOriginConsistent=%s exit=%d, %d file "
           "finding(s) over %d checked, %d missing tree(s), reason=%s"
           % (n, "ACCEPTING" if want else "REJECTING", label,
              "true" if g["marker_origin_ok"] else "false", code,
              len(g["failed"]), g["checked"], len(g["missing_trees"]),
              g["marker_origin_reason"] or "none"),
           g["marker_origin_ok"] is want and not g["failed"]
           and not g["missing_trees"] and " " not in g["marker_origin_reason"]
           and code == (GATE_EXIT_OK if want else GATE_EXIT_FAIL)
           and ("markerOriginConsistent=%s" % ("true" if want else "false")
                in line), line)

    # ------------------------------------------- THE OTHER CLOCK, REJECTING
    # The gate is pinned; the SINGLE-FILE check is not, and must not be. Its
    # question is "is this deadline far enough away to SEND", which is a
    # question about now, and these two cases are what prove the fix repaired
    # the rule rather than disabling it.
    print("\n  THE SINGLE-FILE CHECK KEEPS THE WALL CLOCK, REJECTING:\n")
    wall_now = datetime.datetime.now()
    four_hours = GOOD.replace("DEADLINE 2026-09-07.", "DEADLINE in 4 hours.")
    r4 = check(four_hours, "unprompted", None)      # None means the wall clock
    ok("a four-hour deadline is refused by the single-file check at the real "
       "wall clock (%s), and the finding names the rule" % r4["now"],
       any(f.rule == "deadline" for f in r4["findings"]),
       cap([str(f) for f in r4["findings"]], keep=2, width=90))
    today_iso = wall_now.date().isoformat()
    dated_today = GOOD.replace("DEADLINE 2026-09-07.", "DEADLINE %s."
                               % today_iso)
    rt = check(dated_today, "unprompted", None)
    ok("a message dated today with a deadline of today (%s) is refused too: "
       "09:00 today is at most 9.0 hours from any instant inside it" % today_iso,
       any(f.rule == "deadline" for f in rt["findings"]),
       cap([str(f) for f in rt["findings"]], keep=2, width=90))
    # AND THE SAME MESSAGE, UNPINNED, is refused for a different reason: the
    # deadline could not be read at all. Distinct from "too soon", so the two
    # outcomes cannot be confused in a finding list.
    ru = check(GOOD, "unprompted", UNPINNED)
    ok("an UNPINNED check refuses a deadline it cannot measure, rather than "
       "passing it",
       any(f.rule == "deadline" and "no date" in str(f.what)
           for f in ru["findings"]),
       cap([str(f) for f in ru["findings"]], keep=2, width=90))

    print("\nproducer-check --selftest: %s. %d passed, %d failed, %d rejecting "
          "fixture(s) over %d rule(s) of which %d are enforced by no register "
          "(%s), %d detector fixture(s) for the retired split rule, %d "
          "rejecting fixture(s) for the reading ask, %d "
          "rejecting gate fixture(s) in %d measured gate run(s), %d marker "
          "fixture(s) and %d link-floor ladder rung(s) at the gate"
          % ("PASS" if not failed else "FAILED", passed, len(failed), len(BAD),
             len(RULES),
             len([x for x in RULES
                  if not any(x in v[1] for v in REGISTERS.values())]),
             "/".join(x for x in RULES
                      if not any(x in v[1] for v in REGISTERS.values()))
             or "none",
             len(BAD_BRIEF), len(BAD_BRIEF_READING),
             len(gate_bad), len(gate_runs),
             len(floor_cases) + 3, len(floor_rungs)))
    for f in failed:
        print("  " + f)
    return 0 if not failed else 3


# ----------------------------------------------------------------- the gate
# WIRED INTO `ledger/verify.py`, ruled by Jafar 2026-09-03: "any file under
# production/briefs/ or the Producer's outbox must pass the check for its kind
# before it can be committed. The sender still runs it before sending; the gate
# makes skipping it impossible."
#
# The tool existed, passed its own selftest, and NOTHING CALLED IT, which is
# rule 6 pointed at an instrument: built, tested, plausible, never once running
# where it mattered. `docs_shape` in verify.py carries the same story about
# tools/docs-check.py, one tool and three weeks earlier.

GATE_TREES = (OUTBOX_DIR, "production/briefs")

# The outbox names its kind in the filename because the three registers
# enforce different rules, and a gate that GUESSES the kind checks a message
# against rules its writer never agreed to. Longest suffix first: `.brief.md`
# and `.md` must not race.
KIND_SUFFIX = ((".unprompted.md", "unprompted"),
               (".answer.md", "answer"),
               (".brief.md", "brief"))

# Everything in production/briefs/ is a brief. The directory IS the kind
# there, which is why the outbox needs a suffix and this tree does not.
TREE_DEFAULT_KIND = {"production/briefs": "brief"}

# Documentation, not a message. Named rather than pattern-matched, and the
# count is printed, so an exemption cannot grow quietly into a hole.
GATE_EXEMPT_NAMES = ("README.md",)

EXEMPT_MARKER = "PRODUCER-REGISTER-EXEMPT"
EXEMPT_WITHIN_LINES = 8

# THE FROZEN LIST. Four files predate the register (2026-09-03): three
# director briefs and one step-1 report, none of them a Producer message, all
# of them failing the register badly. Jafar ruled they must not be SILENTLY
# exempt, so the exemption exists in two places that must agree: this list,
# and the marker line inside each file. A marker on a file this list does not
# name is a FAILURE, which is what stops the marker being an escape hatch any
# future session can type at the top of a 600-word message.
PRE_REGISTER = (
    "production/briefs/2026-08-31.md",
    "production/briefs/2026-09-02.md",
    "production/briefs/latest.md",
    "production/briefs/2026-09-03-directors-console-step-1.md",
)

GATE_FINDINGS_SHOWN = 2      # per file. cap() announces when it bites.


# THE GATE'S CLOCK IS NOT THE WALL CLOCK, ruled 2026-09-03 in
# production/queue/077-a-sent-message-goes-red-by-the-clock.md. The gate used
# to re-measure every deadline against the moving wall clock, so the live
# message dated 2026-09-03 carrying DEADLINE 2026-09-06 was 64 hours away when
# written and read -51 hours five days later. The gate runs inside
# ledger/verify.py, so a served deadline would have deleted the footer and
# blocked every commit until somebody edited a message that was correct when it
# was written, with nobody having touched the tree.
#
# TWO CALLERS, TWO CLOCKS, on purpose:
#   - the SINGLE-FILE check keeps the wall clock. "Is this deadline far enough
#     away to send" is a question about now, and that is where the floor bites.
#   - the GATE pins each file to the ISO date its own filename carries. "Was
#     this message correct when it was written" has one answer for ever, which
#     makes the gate idempotent over time by construction rather than by
#     anybody remembering to re-date a file.
#
# MIDNIGHT of that date, not 09:00 and not noon: it is the most permissive
# instant inside the day the file claims, so the gate can never retroactively
# refuse a message the send check accepted at some hour of that same day. The
# floor itself is untouched at MIN_DEADLINE_HOURS: a file dated D whose
# deadline is D 09:00 still reads 9.0 hours and is still refused.
#
# PRODUCTION/BRIEFS GETS THE SAME RULE, not a special case. Three of the four
# briefs already carry an ISO date at the front of the name, so they pin like
# any message; latest.md carries none and comes out UNPINNED. UNPINNED is not
# a pass and not the wall clock: a deadline that cannot be measured is a
# finding naming the fix (put the date in the name). That is what stops a
# dateless brief becoming the next landmine in either direction, and all four
# of these files are exempt from the register anyway, so today nothing rides
# on it.
FILENAME_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(?!\d)")


def gate_clock(rel):
    """(instant, why) the deadline rule measures this file from.

    The ISO date at the front of the filename, at midnight. UNPINNED when the
    name carries none, because the gate refuses to guess an instant: a
    wall-clock fallback here is exactly the landmine this function exists to
    remove."""
    name = rel.rsplit("/", 1)[-1]
    m = FILENAME_DATE_RE.match(name)
    if not m:
        return UNPINNED, "the name carries no date to pin a deadline to"
    try:
        d = datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return UNPINNED, "the date in the name is not a real date: %s" % m.group(1)
    return (datetime.datetime.combine(d, datetime.time(0, 0)),
            "pinned to the date in its own name")


def rel_under(path, root):
    """The repo-relative posix name for `path`, or None when it is not under
    `root`. PURE-ISH: resolves paths, opens nothing.

    THE TWO CALLERS MUST PRODUCE THE SAME NAME. The gate walks and gets
    "production/outbox/x.answer.md"; the sender
    (`tools/runner/outbox.py:run_check`) shells out with an ABSOLUTE path and
    no --root. Without this they would disagree about whether one file is on a
    frozen list, and the file that reached his phone would be the one graded by
    the looser of the two. None for stdin and for anything outside the root, so
    an exemption can never be claimed by a file this repository does not hold.
    """
    if not path or path == "-":
        return None
    try:
        return pathlib.Path(path).resolve().relative_to(
            pathlib.Path(root).resolve()).as_posix()
    except (ValueError, OSError):
        return None


def gate_kind(rel):
    """(kind, why) for a repo-relative path, or (None, why-not)."""
    name = rel.rsplit("/", 1)[-1]
    for suffix, kind in KIND_SUFFIX:
        if name.endswith(suffix):
            return kind, "filename suffix %s" % suffix
    for tree, kind in TREE_DEFAULT_KIND.items():
        if rel.startswith(tree + "/"):
            return kind, "everything under %s/ is a brief" % tree
    return None, ("the name carries no register: end it %s"
                  % "/".join(s for s, _ in KIND_SUFFIX))


def gate(root, now=None, pre_register=PRE_REGISTER, trees=GATE_TREES,
         legacy_links=LEGACY_LINK_RULES, site_origin=SITE_ORIGIN,
         research_verbatim=RESEARCH_VERBATIM, pre_move=PRE_MOVE_MESSAGES,
         pre_reading=PRE_READING_BRIEFS):
    """Every message file under the ruled trees, against its own register.

    PURE-ISH: reads files, touches nothing, returns data. The report function
    formats; the selftest drives this with throwaway trees.

    `now` IS THE RUN'S WALL CLOCK AND IT MEASURES NO DEADLINE. It is recorded
    and printed as provenance only; each file's deadlines are measured from
    gate_clock(rel), the date in that file's own name. That is the whole fix
    of queue item 077, and the property it buys is that this function returns
    the same verdict for the same tree on every day for ever.
    """
    root = pathlib.Path(root)
    wall_now = (now if now is not None and now is not UNPINNED
                else datetime.datetime.now())
    # ONE READING FOR THE WHOLE WALK, taken from the root being walked, because
    # the floor's condition is a fact about the REPOSITORY and not about a file.
    # Read once so two files in one walk can never be graded against two
    # different answers to the same question.
    floor = link_floor_state(root)
    # A1, ONE CALL FOR THE WALK on the reading just taken. WHOLE-RUN: one
    # marker, one origin, so it rides the done line and never a file's line.
    origin_ok, origin_reason = marker_origin_consistent(floor, site_origin)
    r = {"missing_trees": [], "walked": 0, "checked": 0, "exempt": 0,
         "failed": [], "notes": [], "listed_absent": [], "results": [],
         # OF THE FILES CHECKED, how many were graded under the retired
         # destination list because their NAME is on LEGACY_LINK_RULES.
         # Cumulative over the walk, printed beside its denominator.
         "legacy_links": 0, "legacy_absent": [],
         # OF THE URLS WALKED, how many matched a frozen RULED_LINKS entry, and
         # how many entries there were to match. CUMULATIVE over the walk, and
         # the denominator is the tuple's length because that is the number of
         # whole URLs the studio has a ruling for. Printed on the done line as
         # linksRuledUsed=N/M, pass or fail, so a report can never carry the
         # exception in silence.
         "links_ruled_used": 0, "links_ruled_of": len(RULED_LINKS),
         # WHICH files used one, so the per-file lines are not the only record.
         "links_ruled_files": [],
         # OF THE FILES NAMED ON THE FROZEN LEGACY LIST, how many were checked
         # with one leading HISTORICAL, line uncounted by the word cap.
         # Cumulative over the walk, printed beside its denominator, which is
         # the list itself because nothing else can carry the exclusion.
         "historical_uncounted": 0, "historical_listed": len(legacy_links),
         # THE VERBATIM RESEARCH EXEMPTION, AS A LADDER. `research_graded` is
         # CUMULATIVE over the walk: checked files whose NAME is on the frozen
         # RESEARCH_VERBATIM list, over that list's length, so an entry that
         # never gets walked is visible as a gap rather than as nothing.
         # `research_waiver_bit` is the second rung: of those, how many the
         # waiver actually CHANGED anything for, measured by running the same
         # file through the same check() twice in the same run with the one
         # contributor toggled. A membership count alone cannot tell an
         # exemption that is doing work from one that is dead weight, and a
         # dead entry is how a narrow exemption becomes a wide one nobody
         # noticed. `research_findings_waived` is CUMULATIVE findings removed.
         "research_graded": 0, "research_listed": len(research_verbatim),
         "research_waiver_bit": 0, "research_findings_waived": 0,
         "research_absent": [],
         # THE PRE-MOVE WAIVER, AS THE SAME LADDER, for the same reason: a
         # membership count cannot tell a waiver doing work from dead weight.
         # `pre_move_graded` is CUMULATIVE over the walk (checked files whose
         # NAME is on PRE_MOVE_MESSAGES) over that list's length, so an entry
         # nothing walks is visible as a gap rather than as nothing.
         # `pre_move_waiver_bit` is the second rung: of those, how many the
         # waiver actually CHANGED the verdict for, measured by running the
         # same file through the same check() twice in the same run with the
         # one contributor toggled. `pre_move_findings_waived` is CUMULATIVE
         # findings removed, and `pre_move_rules` is the set of rule names
         # those findings carried, so the report can say WHICH rules the
         # waiver is actually holding up rather than only how many.
         "pre_move_graded": 0, "pre_move_listed": len(pre_move),
         "pre_move_waiver_bit": 0, "pre_move_findings_waived": 0,
         "pre_move_rules": set(), "pre_move_absent": [],
         # THE PRE-READING WAIVER, AS THE SAME LADDER AND FOR THE SAME REASON.
         # `pre_reading_graded` is CUMULATIVE over the walk (checked files whose
         # NAME is on PRE_READING_BRIEFS) over that list's length;
         # `pre_reading_waiver_bit` is the second rung, measured by running the
         # same file through the same check() twice in the same run with the one
         # contributor toggled; `pre_reading_findings_waived` is CUMULATIVE
         # findings removed.
         "pre_reading_graded": 0, "pre_reading_listed": len(pre_reading),
         "pre_reading_waiver_bit": 0, "pre_reading_findings_waived": 0,
         "pre_reading_rules": set(), "pre_reading_absent": [],
         # OF THE FILES CHECKED, how many had an instant to measure from.
         # Cumulative over the walk, printed beside its denominator.
         "date_pinned": 0, "unpinned": 0,
         # OF THE FILES CHECKED, how many were graded by a register that still
         # enforces `split`, and how many were graded as briefs. Both cumulative
         # over the walk and printed beside their denominators. The first reads
         # 0 of N while the rule waits for the Sunday summary it is owed by, and
         # moves the day that register exists: a retirement that printed nothing
         # would be indistinguishable from a rule passing on every file.
         "split_enforced": 0, "brief_files": 0,
         # OF THE FILES CHECKED, how many were graded by a register that
         # actually enforced `reading` after every waiver. CUMULATIVE over the
         # walk, printed beside its denominator: on the day it landed it reads
         # 0 of N, because every brief in the tree predates the ruling and is
         # named on PRE_READING_BRIEFS, and it climbs by itself as briefs are
         # written under the rule.
         "reading_enforced": 0,
         # THE LINK FLOOR'S BRANCH FOR THIS WALK, and its blast radius. The
         # branch is a WHOLE-RUN fact (one marker, read once above) and goes on
         # the done line; `link_floor_off` is CUMULATIVE over the walk, counting
         # the checked files actually graded with the floor suspended, beside
         # the denominator of files checked. A suspension with no count beside
         # it cannot be told from a suspension that touched nothing.
         "link_floor_active": floor["active"],
         "link_floor_reason": floor["reason"],
         "link_floor_marker": floor["marker"],
         "link_floor_off": 0,
         # A1: WHOLE-RUN and not a count. False ONLY for the one transition
         # that would make the archive link mandatory again.
         "marker_origin_ok": origin_ok,
         "marker_origin_reason": origin_reason,
         "wall_now": wall_now.isoformat(timespec="minutes")}
    frozen = set(pre_register)
    seen = set()

    for tree in trees:
        d = root / tree
        if not d.is_dir():
            # A GATE POINTED AT A PATH NOBODY WRITES TO IS THE FAULT THIS
            # CONVENTION WAS CREATED TO AVOID, so a missing tree is red rather
            # than an empty walk that reads as clean.
            r["missing_trees"].append(tree)
            continue
        for p in sorted(d.rglob("*.md")):
            rel = p.relative_to(root).as_posix()
            seen.add(rel)
            r["walked"] += 1
            if p.name in GATE_EXEMPT_NAMES:
                r["exempt"] += 1
                r["results"].append((rel, "exempt", "exempt by name (%s)"
                                     % p.name))
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            head = "\n".join(text.splitlines()[:EXEMPT_WITHIN_LINES])
            marked = EXEMPT_MARKER in head
            listed = rel in frozen
            if marked and listed:
                r["exempt"] += 1
                r["results"].append((rel, "exempt",
                                     "pre-register, marked and on the frozen "
                                     "list"))
                continue
            if marked and not listed:
                r["failed"].append((rel, "the %s marker is on a file the "
                                    "frozen PRE_REGISTER list in "
                                    "tools/producer-check.py does not name. "
                                    "The marker is not an escape hatch: widen "
                                    "the list in a reviewed diff, or write the "
                                    "message to the register."
                                    % EXEMPT_MARKER))
                r["results"].append((rel, "fail", "marker without a listing"))
                continue
            if listed and not marked:
                r["failed"].append((rel, "the frozen PRE_REGISTER list names "
                                    "this file but its first %d lines do not "
                                    "carry the %s marker, so a reader of the "
                                    "file cannot see that it is exempt"
                                    % (EXEMPT_WITHIN_LINES, EXEMPT_MARKER)))
                r["results"].append((rel, "fail", "listed without a marker"))
                continue
            kind, why = gate_kind(rel)
            if kind is None:
                r["failed"].append((rel, why))
                r["results"].append((rel, "fail", "no register in the name"))
                continue
            if not text.strip():
                r["failed"].append((rel, "the file is empty, which is not a "
                                    "pass: nothing measured"))
                r["results"].append((rel, "fail", "empty"))
                continue
            # EACH FILE AT ITS OWN INSTANT, never at the run's. See the
            # gate_clock comment: the wall clock made a sent message go red by
            # sitting still.
            file_now, clock_why = gate_clock(rel)
            if file_now is UNPINNED:
                r["unpinned"] += 1
            else:
                r["date_pinned"] += 1
            as_of = ("asOf=" + file_now.isoformat(timespec="minutes")
                     if file_now is not UNPINNED else "asOf=unpinned")
            # BY NAME, NEVER BY THE DATE IN THE NAME. See LEGACY_LINK_RULES.
            legacy = rel in legacy_links
            if legacy:
                r["legacy_links"] += 1
            # BY NAME HERE TOO. See RESEARCH_VERBATIM for the ruling.
            research = rel in research_verbatim
            # AND HERE. See PRE_MOVE_MESSAGES for the ladder it was read off.
            premove = rel in pre_move
            # AND HERE. See PRE_READING_BRIEFS for the ruling and the
            # measurement that sized the list.
            prereading = rel in pre_reading
            res = check(text, kind, file_now, legacy_links=legacy,
                        link_floor=floor, research_verbatim=research,
                        pre_move=premove, pre_reading=prereading)
            r["checked"] += 1
            # THE SECOND RUNG, from the same vantage in the same run: the same
            # file, the same instant, the same floor, the exemption OFF. The
            # difference between the rungs is the only number this yields, and
            # it is the one that says whether the exemption is doing anything.
            waiver_removed = 0
            if research:
                r["research_graded"] += 1
                # ONE CONTRIBUTOR TOGGLED, AND `pre_move` IS CARRIED RATHER
                # THAN DROPPED. It was dropped when the pre-move waiver landed
                # on 2026-09-15, and the reading moved from 5 of 10 to 10 of
                # 10 in one run: with `pre_move=False` this rung also faced the
                # floor, so the linkfloor finding it gained was being credited
                # to the RESEARCH waiver. Two contributors toggled at once is
                # not a ladder, and the number it yields belongs to neither.
                # A banned finding's rule carries its label after a colon
                # (banned:run internals, at the Finding() that builds it), so
                # the match is on the name before the colon, the suite's own
                # idiom. Ruled 2026-09-15 05:43Z, corrected in section 15 of
                # the same record after the first form matched nothing.
                plain = check(text, kind, file_now, legacy_links=legacy,
                              link_floor=floor, research_verbatim=False,
                              pre_move=premove)
                waiver_removed = sum(
                    1 for f in plain["findings"]
                    if f.rule.split(":", 1)[0] in res["research_waived"])
                r["research_findings_waived"] += waiver_removed
                if waiver_removed:
                    r["research_waiver_bit"] += 1
            # THE PRE-MOVE WAIVER'S SECOND RUNG, taken exactly as the research
            # one above is: same file, same instant, same floor, ONE
            # contributor toggled, both readings inside this run.
            if premove:
                r["pre_move_graded"] += 1
                plain = check(text, kind, file_now, legacy_links=legacy,
                              link_floor=floor, research_verbatim=research,
                              pre_move=False)
                removed = [f.rule for f in plain["findings"]
                           if f.rule in res["pre_move_waived"]]
                r["pre_move_findings_waived"] += len(removed)
                r["pre_move_rules"].update(removed)
                if removed:
                    r["pre_move_waiver_bit"] += 1
            # THE PRE-READING WAIVER'S SECOND RUNG, taken exactly as the two
            # above are: same file, same instant, same floor, ONE contributor
            # toggled, both readings inside this run. `removed_reading` is its
            # own name and never `removed`: reusing the pre-move variable would
            # credit one waiver's findings to the other, which is the two-
            # contributors-at-once fault written out at the research rung.
            removed_reading = []
            if prereading:
                r["pre_reading_graded"] += 1
                plain_r = check(text, kind, file_now, legacy_links=legacy,
                                link_floor=floor, research_verbatim=research,
                                pre_move=premove, pre_reading=False)
                removed_reading = [f.rule for f in plain_r["findings"]
                                   if f.rule in res["pre_reading_waived"]]
                r["pre_reading_findings_waived"] += len(removed_reading)
                r["pre_reading_rules"].update(removed_reading)
                if removed_reading:
                    r["pre_reading_waiver_bit"] += 1
            # READ OFF THE REGISTER THIS FILE WAS ACTUALLY GRADED BY, never
            # off the walk's constant. That mattered on 2026-09-15, when the
            # floor DID become per-file: `link_floor_active` is the marker's
            # whole-run answer and stays true for a file PRE_MOVE_MESSAGES
            # exempts, so counting it would have reported a floor that bit 42
            # files while it bit 2.
            if "linkfloor" not in res["enforced"]:
                r["link_floor_off"] += 1
            # READ OFF THE REGISTER THIS FILE WAS ACTUALLY GRADED BY, never off
            # a constant, so the walk's reading moves by itself when a register
            # picks the rule up.
            if "split" in res["enforced"]:
                r["split_enforced"] += 1
            # READ OFF THE REGISTER THIS FILE WAS ACTUALLY GRADED BY, never off
            # a constant, for the reason one line up: since 2026-09-15 the
            # reading rule can drop out PER FILE (PRE_READING_BRIEFS), and a
            # number derived from the register alone would report the rule as
            # biting on every brief while it bit on none of them.
            if "reading" in res["enforced"]:
                r["reading_enforced"] += 1
            if kind == "brief":
                r["brief_files"] += 1
            # THE UNCOUNTED LINE RIDES ON THE FILE'S OWN LINE, pass or fail,
            # because a cap that let something through must say so where the
            # file is named and not only in the footer.
            r["historical_uncounted"] += res["historical_uncounted"]
            hist = (", historicalUncounted=1line/%dwords"
                    % res["historical_words"]) if res["historical_uncounted"] \
                else ""
            # THE RULED EXCEPTION RIDES ON THE FILE'S OWN LINE TOO, pass or
            # fail: a walk that admitted a whole URL by ruling must say which
            # file did it where the file is named, not only in the footer.
            r["links_ruled_used"] += res["ruled_used"]
            if res["ruled_labels"]:
                r["links_ruled_files"].append(rel)
            ruled = (", ruled-link:" + "+".join(res["ruled_labels"])
                     if res["ruled_labels"] else "")
            # THE EXEMPTION RIDES ON THE FILE'S OWN LINE, pass or fail, with
            # what it removed HERE: a waiver counted only in the footer cannot
            # be attached to the file it let through.
            verbatim = ((", research-verbatim:%s-waived/%d-finding(s)-removed"
                         % ("/".join(res["research_waived"]) or NOTHING,
                            waiver_removed)) if research else "")
            # AND THE PRE-MOVE WAIVER RIDES ON IT TOO, pass or fail, with what
            # it removed HERE. Same shape as the line above, for the same
            # reason: a waiver counted only in the footer cannot be attached to
            # the file it let through.
            premoved = ((", pre-move:%s-waived/%d-finding(s)-removed"
                         % ("/".join(res["pre_move_waived"]) or NOTHING,
                            len(removed) if premove else 0))
                        if premove else "")
            # AND THE PRE-READING WAIVER RIDES ON IT TOO, for the same reason.
            prereaded = ((", pre-reading:%s-waived/%d-finding(s)-removed"
                          % ("/".join(res["pre_reading_waived"]) or NOTHING,
                             len(removed_reading)))
                         if prereading else "")
            if res["findings"]:
                r["failed"].append(
                    (rel, "%s: %s" % (kind,
                                      cap([str(f) for f in res["findings"]],
                                          keep=GATE_FINDINGS_SHOWN, width=90,
                                          sep=" | "))))
                r["results"].append((rel, "fail", "%s, %d finding(s), %s%s%s"
                                     % (kind, len(res["findings"]), as_of,
                                        hist,
                                        ruled + verbatim + premoved
                                        + prereaded)))
            else:
                r["results"].append(
                    (rel, "pass-legacy-links" if legacy else "pass",
                     "%s, %d of %s word(s), %s%s%s%s"
                     % (kind, res["words"],
                        res["cap"] if res["cap"] else "no-cap", as_of, hist,
                        ruled + verbatim + premoved + prereaded,
                        ", the link band is not enforced on it: written "
                        "before it was ruled and named in LEGACY_LINK_RULES"
                        if legacy else "")))
    # A FROZEN ENTRY THAT NO LONGER EXISTS IS A NOTE, NOT A RED. Deleting an
    # old brief is legitimate; leaving the rot invisible is not, so it prints
    # with its own count on every run.
    r["listed_absent"] = sorted(rel for rel in frozen if rel not in seen)
    # THE SAME ROT CHECK FOR THE OTHER FROZEN LIST. A grandfathering entry
    # whose file is gone is legitimate history and an invisible one is not, so
    # it prints with its own count on every run.
    r["legacy_absent"] = sorted(rel for rel in legacy_links if rel not in seen)
    # AND THE SAME ROT CHECK FOR THE VERBATIM LIST. A named delivery that has
    # been sent and removed is legitimate; an entry nobody can see rotting is
    # not, so it prints with its own count on every run.
    r["research_absent"] = sorted(rel for rel in research_verbatim
                                  if rel not in seen)
    # AND THE SAME ROT CHECK FOR THE PRE-MOVE LIST, which is the one most
    # likely to rot: every name on it is an archived message, and archived
    # messages get cleared out. An entry nobody can see rotting is a waiver
    # that outlives the file it was written for.
    r["pre_move_absent"] = sorted(rel for rel in pre_move if rel not in seen)
    r["pre_move_rules"] = sorted(r["pre_move_rules"])
    r["pre_reading_absent"] = sorted(rel for rel in pre_reading
                                     if rel not in seen)
    r["pre_reading_rules"] = sorted(r["pre_reading_rules"])
    return r


GATE_EXIT_OK, GATE_EXIT_FAIL, GATE_EXIT_NOTHING = 0, 1, 2


def gate_report(r):
    """Every zero here ships the denominator that produced it."""
    print("producer-check --gate: trees=%s" % "/".join(GATE_TREES))
    for rel, state, why in r["results"]:
        print("  %-17s %-58s %s" % (state, rel, why))
    if r["missing_trees"]:
        print("  MISSING TREE(S), which is red rather than an empty walk: %s. "
              "A gate reading a path nobody writes to reports clean for ever."
              % ", ".join(r["missing_trees"]))
    if r["listed_absent"]:
        print("  note: %d frozen PRE_REGISTER entry/entries no longer exist: "
              "%s" % (len(r["listed_absent"]),
                      cap(r["listed_absent"], keep=3, width=60, sep=", ")))
    if r["legacy_absent"]:
        print("  note: %d frozen LEGACY_LINK_RULES entry/entries no longer "
              "exist: %s" % (len(r["legacy_absent"]),
                             cap(r["legacy_absent"], keep=3, width=60,
                                 sep=", ")))
    if r["research_absent"]:
        print("  note: %d of the %d frozen RESEARCH_VERBATIM entry/entries no "
              "longer exist (sent and cleared, or renamed): %s"
              % (len(r["research_absent"]), r["research_listed"],
                 cap(r["research_absent"], keep=3, width=60, sep=", ")))
    if r["pre_move_absent"]:
        print("  note: %d of the %d frozen PRE_MOVE_MESSAGES entry/entries no "
              "longer exist (cleared out of the outbox, or renamed), so the "
              "waiver they carry is holding nothing up and the name comes off "
              "the tuple: %s"
              % (len(r["pre_move_absent"]), r["pre_move_listed"],
                 cap(r["pre_move_absent"], keep=3, width=60, sep=", ")))
    if r["pre_reading_absent"]:
        print("  note: %d of the %d frozen PRE_READING_BRIEFS entry/entries no "
              "longer exist (superseded, cleared or renamed), so the waiver "
              "they carry is holding nothing up and the name comes off the "
              "tuple: %s"
              % (len(r["pre_reading_absent"]), r["pre_reading_listed"],
                 cap(r["pre_reading_absent"], keep=3, width=60, sep=", ")))
    # THE EXEMPTION'S LADDER, PRINTED WHETHER OR NOT IT BIT. Both rungs come
    # from the same walk and the same instant. The zero ships two denominators
    # because they answer different questions: how many listed files this walk
    # graded, and of those, how many the waiver changed anything for.
    print("  verbatim research deliveries: %d of the %d name(s) on the frozen "
          "RESEARCH_VERBATIM list were graded in this walk with %s waived; "
          "the waiver changed the verdict on %d of them, removing %d "
          "finding(s) in total. Ruled 2026-09-14: a research SUMMARY goes to "
          "him IN FULL. An entry the waiver never bites on is dead weight and "
          "comes off the list; every other rule still binds on all of them"
          % (r["research_graded"], r["research_listed"],
             "/".join(RESEARCH_WAIVED_RULES), r["research_waiver_bit"],
             r["research_findings_waived"]))
    # THE PRE-MOVE WAIVER'S LADDER, PRINTED WHETHER OR NOT IT BIT, and its
    # zeros ship three denominators because they answer three questions: how
    # many listed names this walk graded, of those how many the waiver changed
    # the verdict for, and WHICH rules those removed findings carried. A walk
    # where the second number is 0 over a non-zero first is a list that has
    # stopped doing anything and should be deleted; a walk where it equals the
    # first is the list holding the gate up on its own. NAMED AS A CUMULATIVE
    # COUNT OVER THE WALK, not a peak and not a per-file number.
    print("  messages already sent when the site moved: %d of the %d name(s) "
          "on the frozen PRE_MOVE_MESSAGES list were graded in this walk with "
          "%s waived; the waiver changed the verdict on %d of them, removing "
          "%d finding(s) in total, carrying the rule(s) %s. Queue 256 moved "
          "SITE_ORIGIN and turned the floor back on in one commit, and both "
          "halves re-grade messages that were already sent: these were correct "
          "under the rulebook in force when they went. Membership is by name, "
          "never by the date in the name, and a message written after the move "
          "is not on it"
          % (r["pre_move_graded"], r["pre_move_listed"],
             "/".join(PRE_MOVE_WAIVED_RULES), r["pre_move_waiver_bit"],
             r["pre_move_findings_waived"],
             "/".join(r["pre_move_rules"]) or NOTHING))
    # THE PRE-READING WAIVER'S LADDER, PRINTED WHETHER OR NOT IT BIT, with the
    # same three denominators as the one above and for the same reasons. THE
    # SECOND NUMBER IS THE ONE THAT MATTERS: briefs graded over briefs listed
    # says the walk found them, and verdicts changed over those says the list
    # is doing work rather than sitting there. CUMULATIVE OVER THE WALK.
    print("  briefs written before the reading ask was ruled: %d of the %d "
          "name(s) on the frozen PRE_READING_BRIEFS list were graded in this "
          "walk with %s waived; the waiver changed the verdict on %d of them, "
          "removing %d finding(s) in total, carrying the rule(s) %s. Ruled "
          "2026-09-15: from that ruling the brief asks Jafar for his meter "
          "reading as its FIRST line. Every name above was written before it "
          "and was correct under the rulebook in force when it went; a brief "
          "written after it is not on the list and is refused without the ask"
          % (r["pre_reading_graded"], r["pre_reading_listed"],
             "/".join(PRE_READING_WAIVED_RULES), r["pre_reading_waiver_bit"],
             r["pre_reading_findings_waived"],
             "/".join(r["pre_reading_rules"]) or NOTHING))
    # THE FLOOR'S BRANCH FOR THIS WALK, printed whether or not anything was
    # checked, because a walk that measured nothing still has an answer to
    # "was the floor live". The numerator is cumulative over the walk and its
    # denominator is the files checked: 0/0 reads as a floor that suspended
    # nothing, which is a different fact from a floor that let 23 files
    # through.
    print("  link floor: linkFloorActive=%s reason=%s. %d of %d checked "
          "file(s) were graded with the floor suspended (zero links legal); "
          "the rest faced the ruled %d..%d. Ruled 2026-09-10 (queue 256, queue "
          "259): no link goes out while every permitted destination sits under "
          "the ARCHIVE's pages. The floor is NOT deleted and returns the run "
          "after %s names a served commit"
          % ("true" if r["link_floor_active"] else "false",
             r["link_floor_reason"], r["link_floor_off"], r["checked"],
             LINK_MIN, LINK_MAX, r["link_floor_marker"]))
    if not r["marker_origin_ok"]:
        # FOUR SPACES AND A COLON, which is how ledger/verify.py harvests a
        # FINDING out of this report; at two it reaches the footer as
        # "see producer-check" and the reader has to run the tool again.
        print("    MARKER VERSUS ORIGIN, WHOLE-RUN and no file's: "
              "markerOriginConsistent=false reason=%s. SITE_ORIGIN is still "
              "%s, so the floor is back on and every link it would accept is "
              "stale: flip it in the commit that writes the sha (queue 256)"
              % (r["marker_origin_reason"], ARCHIVE_ORIGIN))
    if r["checked"]:
        print("  link band: %d of %d checked file(s) graded under the RETIRED "
              "destination list because their name is one of the %d on "
              "LEGACY_LINK_RULES; the other %d were graded under the band "
              "Jafar ruled 2026-09-06. Membership is by name, never by the "
              "date in the name."
              % (r["legacy_links"], r["checked"], len(LEGACY_LINK_RULES),
                 r["checked"] - r["legacy_links"]))
    if r["checked"]:
        # THE RULED WHOLE-URL EXCEPTION ACROSS THE WALK, with its denominator,
        # so a zero here reads as "the exception existed and no message used
        # it" rather than as nothing at all. Cumulative over the walk; the
        # denominator is the frozen tuple, which is how many whole URLs the
        # studio has a ruling for. NO BOUND IS SET ON THIS NUMBER YET: this is
        # the printer, and the series it prints is what a bound would be read
        # off if the exception ever spreads past the one message it was for.
        print("  ruled whole-URL exception: %d URL(s) across the walk matched "
              "one of the %d frozen RULED_LINKS entry/entries, in %d file(s) "
              "(%s). Whole-string equality, never a prefix, so admitting a URL "
              "admits nothing under it. Each entry names the record that "
              "admits it and the rung that deletes it."
              % (r["links_ruled_used"], r["links_ruled_of"],
                 len(r["links_ruled_files"]),
                 cap(r["links_ruled_files"], keep=3, width=60, sep=", ")
                 if r["links_ruled_files"] else NOTHING))
    if r["checked"]:
        # WHAT THE CAP DID NOT READ, with the only denominator under which the
        # exclusion can exist. Cumulative over the walk.
        print("  historical annotations: %d of the %d file(s) named on the "
              "frozen LEGACY_LINK_RULES list were checked with one leading %s "
              "line uncounted by the word cap. Ruled 2026-09-06: the cap "
              "governs what the Producer wrote and the marker is an annotation "
              "the studio added afterwards. Only the FIRST line is excused and "
              "only from the count; a second is counted like any other line."
              % (r["historical_uncounted"], r["historical_listed"],
                 HISTORICAL_PREFIX))
    if r["checked"]:
        # THE RETIRED RULE ACROSS THE WALK, with both denominators, so a reader
        # of this report can tell "the split passed everywhere" from "the split
        # was measured nowhere". Cumulative over the walk.
        print("  studio-versus-game split: enforced on %d of %d checked "
              "file(s), %d of them graded as brief(s). Retired from the brief "
              "register on %s by Jafar's director test and applied to no "
              "register since; his order of 2026-09-05 stands and the number is "
              "owed by %s"
              % (r["split_enforced"], r["checked"], r["brief_files"],
                 SPLIT_RETIRED_ON.isoformat(), SPLIT_OWED_BY))
    # WHICH CLOCK READ THE DEADLINES, with its denominator, because "0 failed"
    # from a gate measuring the wrong instant is the fault this line exists to
    # make visible. Cumulative over the walk.
    if r["checked"]:
        print("  deadline clock: %d of %d checked file(s) pinned to the ISO "
              "date in their own name, %d unpinned (no date in the name, and a "
              "deadline in one of those is a finding, not a pass). The run's "
              "wall clock was %s and measured NO deadline: this gate returns "
              "the same verdict on every day."
              % (r["date_pinned"], r["checked"], r["unpinned"], r["wall_now"]))
    else:
        print("  deadline clock: %s, no file reached a register (wall clock "
              "%s, which measures no deadline here)"
              % (NOTHING.replace("-", " "), r["wall_now"]))
    print("  %d file(s) walked: %d checked against a register, %d exempt "
          "(%d by name, %d pre-register), %d failed"
          % (r["walked"], r["checked"], r["exempt"],
             sum(1 for _, s, w in r["results"]
                 if s == "exempt" and "by name" in w),
             sum(1 for _, s, w in r["results"]
                 if s == "exempt" and "pre-register" in w),
             len(r["failed"])))
    if r["missing_trees"]:
        return GATE_EXIT_FAIL
    if not r["walked"]:
        print("  nothing measured: the trees exist and hold no markdown file "
              "at all")
        return GATE_EXIT_NOTHING
    if not r["failed"] and r["marker_origin_ok"]:
        # A CLEAN GATE THAT CHECKED NOTHING IS NOT A CLEAN GATE. Today every
        # file in both trees is exempt, so "0 findings" would be true and
        # useless: the words go in the human line AND in the key, because the
        # key is what reaches the verification footer and the footer is what
        # anybody actually reads.
        if not r["checked"]:
            print("  %s against a register: all %d walked file(s) were exempt "
                  "(%d by name, %d pre-register). The gate is running; no "
                  "message has been written to it yet."
                  % (NOTHING.replace("-", " "), r["walked"],
                     sum(1 for _, s, w in r["results"]
                         if s == "exempt" and "by name" in w),
                     sum(1 for _, s, w in r["results"]
                         if s == "exempt" and "pre-register" in w)))
        else:
            print("  0 finding(s) over %d file(s) checked against %d "
                  "register(s) (%s). MECHANICAL ONLY: nothing here read "
                  "whether a claim is TRUE." % (r["checked"], len(REGISTERS),
                                                ",".join(sorted(REGISTERS))))
        # linksRuledUsed: CUMULATIVE URL matches across the walk over the
        # number of frozen RULED_LINKS entries. On the done line because it is
        # a whole-run number; the per-file lines carry ruled-link:<label>.
        # splitEnforcedOn: CUMULATIVE count of checked files whose register still
        # enforces `split`, over the files checked. On the done line because it
        # is a whole-run number, and in the verification footer through it, so
        # the retirement of 2026-09-09 is visible at every commit rather than
        # only in this file's comments.
        # filesLinkFloorOff: CUMULATIVE count of checked files graded with the
        # evidence floor suspended, over the files checked. linkFloorActive and
        # its reason are WHOLE-RUN (one marker, read once) and sit last and
        # adjacent, because the reason is the only token here that can grow.
        print("\nproducer-check --gate: PASS filesChecked=%s "
              "filesLegacyLinks=%d/%d researchVerbatimWaiverBit=%s "
              "researchVerbatimGraded=%d/%d linksRuledUsed=%d/%d "
              "historicalLinesUncounted=%d/%d splitEnforcedOn=%d/%d "
              "readingEnforcedOn=%d/%d preReadingGraded=%d/%d "
              "preReadingWaiverBit=%d/%d "
              "filesBriefs=%d filesExempt=%d filesWalked=%d filesDatePinned=%d/%d "
              "markerOriginConsistent=%s "
              "filesLinkFloorOff=%d/%d linkFloorActive=%s reason=%s"
              % (r["checked"] if r["checked"] else "0/" + NOTHING,
                 r["legacy_links"], r["checked"],
                 research_bit_key(r),
                 r["research_graded"], r["research_listed"],
                 r["links_ruled_used"], r["links_ruled_of"],
                 r["historical_uncounted"], r["historical_listed"],
                 r["split_enforced"], r["checked"],
                 r["reading_enforced"], r["checked"],
                 r["pre_reading_graded"], r["pre_reading_listed"],
                 r["pre_reading_waiver_bit"], r["pre_reading_graded"],
                 r["brief_files"],
                 r["exempt"], r["walked"], r["date_pinned"], r["checked"],
                 "true" if r["marker_origin_ok"] else "false",
                 r["link_floor_off"], r["checked"],
                 "true" if r["link_floor_active"] else "false",
                 r["link_floor_reason"]))
        return GATE_EXIT_OK
    print("  %d file(s) failed, %d whole-run finding(s):"
          % (len(r["failed"]), 0 if r["marker_origin_ok"] else 1))
    for rel, why in r["failed"][:5]:
        print("    %s: %s" % (rel, why))
    if len(r["failed"]) > 5:
        print("    (+%d more not shown of %d)"
              % (len(r["failed"]) - 5, len(r["failed"])))
    print("\nproducer-check --gate: FAIL filesFailed=%d filesChecked=%d "
          "filesLegacyLinks=%d/%d researchVerbatimWaiverBit=%s "
          "researchVerbatimGraded=%d/%d linksRuledUsed=%d/%d "
          "historicalLinesUncounted=%d/%d splitEnforcedOn=%d/%d "
          "readingEnforcedOn=%d/%d preReadingGraded=%d/%d "
          "preReadingWaiverBit=%d/%d "
          "filesBriefs=%d filesExempt=%d filesWalked=%d filesDatePinned=%d/%d "
          "markerOriginConsistent=%s "
          "filesLinkFloorOff=%d/%d linkFloorActive=%s reason=%s"
          % (len(r["failed"]), r["checked"], r["legacy_links"], r["checked"],
             research_bit_key(r),
             r["research_graded"], r["research_listed"],
             r["links_ruled_used"], r["links_ruled_of"],
             r["historical_uncounted"], r["historical_listed"],
             r["split_enforced"], r["checked"],
             r["reading_enforced"], r["checked"],
             r["pre_reading_graded"], r["pre_reading_listed"],
             r["pre_reading_waiver_bit"], r["pre_reading_graded"],
             r["brief_files"],
             r["exempt"], r["walked"], r["date_pinned"], r["checked"],
             "true" if r["marker_origin_ok"] else "false",
             r["link_floor_off"], r["checked"],
             "true" if r["link_floor_active"] else "false",
             r["link_floor_reason"]))
    return GATE_EXIT_FAIL


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", nargs="?", help="message file, or - for stdin")
    ap.add_argument("--kind", default="unprompted", choices=sorted(REGISTERS))
    ap.add_argument("--now", help="ISO datetime the deadlines are measured "
                                  "against (default: now)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--gate", action="store_true",
                    help="walk production/outbox/ and production/briefs/ and "
                         "check every message against its own register")
    ap.add_argument("--root", default=str(REPO),
                    help="repository root the gate walks, and the root the "
                         "served-page marker (%s) is read from for the "
                         "single-file check too (default: this repo)"
                         % SERVED_MARKER_REL)
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.gate:
        now = (datetime.datetime.fromisoformat(args.now) if args.now
               else datetime.datetime.now())
        return gate_report(gate(args.root, now))
    if not args.file:
        ap.print_usage()
        print("producer-check: nothing measured, no message given")
        return 2
    if args.file == "-":
        text = sys.stdin.read()
    else:
        p = pathlib.Path(args.file)
        if not p.is_file():
            print("producer-check: nothing measured, no file at %s" % args.file)
            return 2
        text = p.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        print("producer-check: nothing measured, the message is empty")
        return 2
    now = (datetime.datetime.fromisoformat(args.now) if args.now
           else datetime.datetime.now())
    # THE FLOOR'S CONDITION IS READ HERE, at the call site, because check() is
    # pure. `tools/runner/outbox.py:run_check` shells out to exactly this path
    # with no --root, so the sender reads the marker in its own checkout and
    # the gate and the sender can never disagree about whether a page is
    # served.
    #
    # AND MEMBERSHIP OF THE FROZEN VERBATIM LIST IS DECIDED HERE TOO, for the
    # same reason: check() reads no path. Resolved through rel_under so this
    # call site and the gate's walk name the same file the same way.
    return report(check(text, args.kind, now,
                        link_floor=link_floor_state(args.root),
                        research_verbatim=rel_under(args.file, args.root)
                        in RESEARCH_VERBATIM))


if __name__ == "__main__":
    # A correct run that ends in a BrokenPipeError traceback costs twenty
    # minutes before anybody notices it worked.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    sys.exit(main())
