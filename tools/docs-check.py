#!/usr/bin/env python3
"""Every design doc must say what it is, at the top, before anybody reads it.

WHY THIS EXISTS. Jafar asked for the project's high-level state. I answered
from `roadmap.md`'s "STILL OPEN — the honest list", told him the Mixamo
character drop was the single biggest blocker in the project, and recommended
he go and do it. It had shipped the day before — 41 clips and two bodies, in
the repo, with a whole roadmap section describing them. The list I quoted was
dated three days earlier and said so at the top of a 1400-line file, hundreds
of lines above the part I read.

That is not a mistake you fix by being more careful. A file is read from
wherever the grep landed, and a date at the top of a long document is invisible
from the middle of it. So every doc now declares its own status in its first
few lines, where any excerpt of it starts:

  LIVE: kept current, and wrong is a bug
  SPEC: the intent; build state lives in the roadmap
  LOG:  true on one dated day, explicitly NOT the present

    python tools/docs-check.py
    python tools/docs-check.py --selftest    # accepting case FIRST

THE BANNER PUNCTUATION, RULED BY JAFAR 2026-09-03. This checker used to demand
`**STATUS` followed by an EM-DASH, while constitution law 11 bans em-dashes
anywhere: every document in `game-design/` therefore carried a deliberate law
violation because the checker required it, and two separate roles lost time to
it in one day, each writing the lawful colon form and being rejected for it.
The colon form is now the only accepted form and THE OLD ONE IS REFUSED, so
the migration in `tools/migrate-status-banner.py` cannot half-happen and
quietly leave two conventions running.

WHAT "AT BANNER POSITION" MEANS, and why the refusal is anchored. A dated
report may legitimately QUOTE the retired form inside backticks while
carrying a lawful banner of its own; five documents here do. So the refusal
fires on the old form at the START of a line only, and that definition is
IMPORTED from the migration script rather than retyped, because one idea with
two implementations is one implementation nobody fixes.

IT ALSO CHECKS THAT A RULING'S ORDERS TO THE QUEUE LANDED. Jafar, 2026-09-14:
"a ruling that orders work to the queue names the item by number, and something
checks the item exists. Three instructions today landed in a commit and became
nothing, and no gate caught any of them." A ruling that orders queue work
writes `QUEUE: <number> <name>` at column 0 and this resolves the number
against ALL THREE PLACES AN ITEM CAN SIT: `production/queue/`, its `blocked/`
holding area and its `done/` archive. An item moved to any of them is still a
filed item, and an index walking only some of them turns a ruling RED on the
day its work is done. The coverage limit is printed on every run: markers are
read, prose is not, and the item files carrying no number (which no marker can
name) are counted out loud rather than skipped in silence.

EXIT CODES, distinct per outcome. 0 clean. 1 at least one document failed, and
each is named. 3 the selftest failed. 4 the migration script could not be
imported, so the retired form has no definition to refuse against; this
program will not report a clean sweep it could not perform. 5 the queue counter
could not be imported, so the work queue has no definition to resolve markers
against, and the same refusal applies.
"""
import argparse
import collections
import importlib.util
import pathlib
import re
import sys

DOCS = pathlib.Path(__file__).resolve().parent.parent / "game-design"
KINDS = ("LIVE", "SPEC", "LOG")
# A banner has to be near the top or it does not do its job.
WITHIN_LINES = 8

# ONE IMPLEMENTATION PER IDEA: the retired form at banner position is defined
# by the migration that removed it, and imported here.
_MIG = pathlib.Path(__file__).resolve().parent / "migrate-status-banner.py"


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


_mig = _load(_MIG, "migrate_status_banner")
if _mig is None:
    sys.stderr.write("docs-check: tools/migrate-status-banner.py could not be "
                     "imported; refusing to report a banner sweep with no "
                     "definition of the retired form behind it\n")
    sys.exit(4)
RETIRED_RE = _mig.OLD_RE

# ONE IMPLEMENTATION PER IDEA, again: WHERE the work queue lives and WHICH
# files in it are items belong to `tools/queue-check.py`, which calls itself the
# one counter of the queue, and are imported rather than retyped here. What is
# new is the index BY NUMBER, which nothing in this repository built before.
_QC = pathlib.Path(__file__).resolve().parent / "queue-check.py"
_qc = _load(_QC, "queue_check")
if _qc is None:
    sys.stderr.write("docs-check: tools/queue-check.py could not be imported; "
                     "refusing to report a clean queue-marker sweep with no "
                     "definition of the work queue behind it\n")
    sys.exit(5)

# THE RULED FORM. The bold marks are optional: `**STATUS: LIVE**` and a plain
# `STATUS: LIVE` are the same declaration, and the second is what both roles
# wrote unprompted on the day this was ruled.
BANNER_RE = re.compile(r"(?:\*\*)?STATUS:[ \t]*(LIVE|SPEC|LOG)")
LOG_DATE_RE = re.compile(r"(?:\*\*)?STATUS:[ \t]*LOG,[ \t]*(\d{4}-\d{2}(-\d{2})?)")


def banner(head):
    """(kind, fault) for a document's first lines. EXACTLY ONE of the two is
    None. `head` is the joined first WITHIN_LINES lines.

    The order is deliberate: a document carrying the retired form at banner
    position is REFUSED even if it also carries a lawful one, because that is
    a half-migrated file and the two conventions must not both run."""
    if RETIRED_RE.search(head):
        return None, "the retired em-dash STATUS banner (ruled out 2026-09-03)"
    m = BANNER_RE.search(head)
    if m:
        return m.group(1), None
    return None, "no STATUS banner"


# ------------------------------------------- orders to the queue (Jafar, 2026-09-14)
#
# THE RULE, VERBATIM: "a ruling that orders work to the queue names the item by
# number, and something checks the item exists. Three instructions today landed
# in a commit and became nothing, and no gate caught any of them."
#
# THE THREE THAT PAID FOR IT. (1) The 2026-09-10 exposure ruling, line 132,
# ordered a research rung "to the queue with a name: settled night exposure
# reference" and dictated its three steps. A grep of 268 queue files four days
# later found ZERO hits: it sat dark and no gate said a word. It is now
# production/queue/276. (2) The same ruling ordered the camera-by-condition
# determinism matrix printed with its count, a rule 3b finding from a sample of
# one, and that is still filed nowhere. (3) 182 items were closed under an
# archiving commit with no ruling naming what went with them (queue 275).
#
# WHY A MARKER, DECIDED AGAINST THE ALTERNATIVE RATHER THAN BY DEFAULT.
# "This sentence orders work to the queue" is a fuzzy match over free prose, and
# the corpus refuses it out loud: the phrase `to the queue` appears on 22 lines
# of 17 decision records here, meaning at least five different things. An order
# ("goes to the queue with a name"), an order DEFERRED ("goes to the queue and
# waits for Monday"), a recollection of one already filed ("was filed to the
# queue, then ruled IN"), an explicit NON-item ("not an item, goes to the queue
# to revisit only if a landed still says"), and a quotation of somebody else's
# standing rule. A heuristic over that population buys a handful of catches and
# pays in reds against records that did nothing wrong, and a checker that cries
# on correct documents is uninstalled within a week.
#
# So the channel is EXPLICIT, and THE LIMIT IS PRINTED ON EVERY RUN rather than
# left to be discovered: this reads markers, not prose, and it says in as many
# words that it cannot see an order written without one. The size of that blind
# spot is printed too, as an unjudged count, so "0 missing" can never be read as
# full coverage of the rule.
#
# THE FORM, one line, column 0:
#
#     QUEUE: 276 settled-night-exposure-reference
#
# Number first because that is what Jafar's rule names; a space-free name after
# it because a failure has to say WHAT went missing, not just which integer.
# Fenced code blocks are blanked before scanning and the marker must start at
# column 0, so a document can show the form (fenced, or indented) without being
# read as using it. Both escapes exist because the record explaining this rule
# will quote it.
QUEUE_MARKER = "QUEUE:"
QUEUE_STRICT_RE = re.compile(r"^QUEUE:[ \t]+(\d{1,4})[ \t]+(\S+)[ \t]*$")
# Blanked, not deleted: the replacement keeps the newline count so the line
# numbers in a failure still match the file a reader opens.
FENCE_RE = re.compile(r"(?ms)^```.*?^```")
# THE NUMERIC PREFIX, AND WHAT IT CANNOT NAME. The marker's channel is the
# number, so an item file whose name does not begin `NNN-` cannot be named by
# any marker at all. This index skips those files, and until 2026-09-14 it
# skipped them IN SILENCE: `production/queue/art-atlas-01-integration.md` is
# one, it was reopened that day, and the index was already short of a real item
# without a word about it. The skip is now a printed count with its
# denominator beside it, and a zero prints as a reading rather than as nothing
# (rule 3b). Found by the director ruling of 2026-09-14, section 5.
QUEUE_NUM_RE = re.compile(r"^(\d+)-")

# EVERY PLACE AN ITEM CAN SIT, in the order `tools/queue-check.py` walks them.
# `queue` is the top of production/queue/ itself; the other two are its
# subdirectories.
#
# WHERE THE QUEUE LIVES IS IMPORTED, NOT RETYPED: `_qc.QUEUE_REL`,
# `_qc._md_files` and `_qc.EXEMPT_NAMES` all come from queue-check.py, which
# calls itself the one counter of the work queue and is right. THE TWO
# SUBDIRECTORY NAMES ARE STRING LITERALS THERE (count_queue, lines 151 and 157)
# with no constant to import, so they are written out here ONCE and then PINNED
# BY A FIXTURE rather than trusted: `planted_queue_tree()` below puts one item
# in each of the three places and asserts that queue-check's own count_queue()
# and this index see the same tree. The day that file grows a fourth place or
# renames one, the fixture disagrees out loud instead of this index missing a
# directory quietly.
#
# THE HOLE THIS CLOSES, ruled 2026-09-14 section 5. This index walked `queue`
# and `done` only. No `blocked/` exists in the tree today, so nothing was red;
# the day one item is moved there, every ruling naming it goes red for the work
# having been done correctly. That is rule 5b's ratchet, and it is the same
# shape the done/ walk already corrected once.
QUEUE_TOP = "queue"
QUEUE_SUBDIRS = ("blocked", "done")
QUEUE_PLACES = (QUEUE_TOP,) + QUEUE_SUBDIRS
# The prose the blind-spot counter looks for. It NEVER fails a run and never
# names a document as wrong; it exists only to put a size on what markers
# cannot see. Printed beside the count so a reader knows exactly what matched.
QUEUE_PROSE = ("to the queue",)
# A ruling record is `game-design/decision-*.md`, the definition `ledger/verify.py`
# already uses for its cadence stamp (DIRECTOR_DECISION_GLOB). Not imported:
# verify.py runs THIS program as a subprocess, so importing it back would be a
# cycle. Kept as one line beside the citation so the two cannot drift silently.
RULING_GLOB = "decision-*.md"


def _blank_fences(text):
    """Fenced blocks replaced by their own newlines. PURE."""
    return FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)


def queue_markers(text):
    """(markers, malformed) for one document's full text. PURE: no file read.

    markers   [(line, number, name)]
    malformed [(line, the line as written, truncated)]

    A `QUEUE:` line at column 0 that the strict form cannot read is MALFORMED
    AND REPORTED, never skipped. A marker nothing can parse looks exactly like
    compliance from a distance and enforces nothing, which is the silent
    instrument failure this file exists to prevent."""
    markers, malformed = [], []
    for i, line in enumerate(_blank_fences(text).split("\n"), 1):
        if not line.startswith(QUEUE_MARKER):
            continue
        m = QUEUE_STRICT_RE.match(line.rstrip("\r"))
        if m:
            markers.append((i, int(m.group(1)), m.group(2)))
        else:
            malformed.append((i, line.strip()[:56]))
    return markers, malformed


#: ONE WALK, ONE INSTANT, and every number below is CUMULATIVE OVER THAT WALK.
#:
#: index            number -> [(place, filename)], places in QUEUE_PLACES order
#: by_place         place -> {"walked", "numbered", "unnumbered", "exempt"}
#: exists           place -> was the directory there to be walked at all, so
#:                  that a zero from an absent directory can never be read as a
#:                  zero from an empty one
#: walked           item files opened across all three places, exempt names
#:                  excluded. THE DENOMINATOR for `unnumbered`.
#: exempt           files skipped by name (queue-check.py's EXEMPT_NAMES:
#:                  README.md is documentation, not an item), counted apart so
#:                  it is not silently inside or outside `walked`
#: unnumbered       item files no marker can name, with their names
#: dups             numbers found in more than one file, across all places
QueueIndex = collections.namedtuple(
    "QueueIndex",
    "index by_place exists walked exempt unnumbered unnumbered_names dups")


def place_rel(where):
    """The repository-relative directory a place sits at. ONE DEFINITION, used
    by the walk and by every line that names the place, so a printed path can
    never disagree with the directory actually opened."""
    if where == QUEUE_TOP:
        return _qc.QUEUE_REL
    return "%s/%s" % (_qc.QUEUE_REL, where)


def queue_index(root):
    """A QueueIndex over the work queue: all three places, one walk.

    ALL THREE PLACES ARE INDEXED ON PURPOSE. A finished item moves to
    `production/queue/done/` and a stalled one to `production/queue/blocked/`,
    so a checker resolving against the live directory alone would turn a ruling
    RED the day its work landed or the day it was parked: rule 5b's ratchet,
    and precisely the shape the instrument rules name as making the work break
    the tool. Every place resolves, and the split is printed per place.

    WHAT IT DECLINES TO INDEX IS COUNTED, NOT DROPPED. Files exempt by name and
    files with no numeric prefix are each counted, per place and in total, and
    printed: a file this index declined to open is part of the denominator."""
    root = pathlib.Path(root)
    index, dups = {}, 0
    exists = {}
    by_place = {w: {"walked": 0, "numbered": 0, "unnumbered": 0, "exempt": 0}
                for w in QUEUE_PLACES}
    walked = exempt = unnumbered = 0
    unnumbered_names = []
    for where in QUEUE_PLACES:
        d = root / place_rel(where)
        exists[where] = d.is_dir()
        if not exists[where]:
            continue
        for p in _qc._md_files(d):
            if p.name in _qc.EXEMPT_NAMES:
                exempt += 1
                by_place[where]["exempt"] += 1
                continue
            walked += 1
            by_place[where]["walked"] += 1
            m = QUEUE_NUM_RE.match(p.name)
            if not m:
                unnumbered += 1
                by_place[where]["unnumbered"] += 1
                # `place/name`, no spaces: this goes into a printed line that
                # every reader splits on whitespace.
                unnumbered_names.append("%s/%s" % (where, p.name))
                continue
            n = int(m.group(1))
            if n in index:
                dups += 1
            index.setdefault(n, []).append((where, p.name))
            by_place[where]["numbered"] += 1
    return QueueIndex(index, by_place, exists, walked, exempt, unnumbered,
                      unnumbered_names, dups)


def resolve_markers(index, numbers):
    """Marker numbers against a QueueIndex's index. PURE: no file is read.

    Returns a dict carrying `resolved`, `missing` and one count per place in
    QUEUE_PLACES. ONE IMPLEMENTATION: the run's own line, the planted-tree
    fixture and the selftest all resolve through this, so a fixture can never
    agree with a copy of the logic rather than with the logic.

    A number found in more than one place is counted ONCE, at the FIRST place
    in QUEUE_PLACES order. An item sitting in queue/ and done/ at the same
    moment is live work with a stale archive copy, not two items, and
    `resolved` has to stay the exact sum of the per-place counts or the run
    line prints a total that does not add up."""
    counts = {w: 0 for w in QUEUE_PLACES}
    counts["resolved"] = 0
    counts["missing"] = 0
    for n in numbers:
        hit = index.get(n)
        if not hit:
            counts["missing"] += 1
            continue
        counts["resolved"] += 1
        places = {w for w, _f in hit}
        for w in QUEUE_PLACES:
            if w in places:
                counts[w] += 1
                break
    return counts


def queue_section(docs, marks, qi, rulings, prose_lines, prose_docs,
                  prose_unmarked):
    """The whole-run numbers for the queue-order rule, on the run's own lines.

    Per-document faults went through `check()` at the call site, which is where
    the per-sample moment belongs; everything here is a count OF THE RUN."""
    found = sum(len(m) for _, m, _ in marks)
    bad = sum(len(b) for _, _, b in marks)
    if not docs:
        print("\nqueue orders: nothing measured, no document was walked")
        return
    r = resolve_markers(qi.index,
                        [n for _, ms, _ in marks for _, n, _nm in ms])
    if not qi.index:
        print(f"\nqueue orders: nothing measured, no numbered item under "
              f"{_qc.QUEUE_REL}/ to resolve against")
    else:
        print(f"\nqueue orders (Jafar 2026-09-14: a ruling that orders work to "
              f"the queue names the item by number)")
        # THE RUN LINE. Every value on it is CUMULATIVE OVER THE ONE WALK and
        # belongs to this run, never to a document: per-document faults are on
        # their own lines above, through check().
        #
        # The two halves are generated from QUEUE_PLACES rather than typed, so
        # a place can never appear in one half and be forgotten in the other.
        # The keys they emit, spelled out here so a grep for a key name lands
        # in this file: `inQueue= inBlocked= inDone=` are MARKERS RESOLVED to
        # an item in that place, and `indexQueue= indexBlocked= indexDone=` are
        # NUMBERED FILES WALKED there. The pair moves independently: a place
        # can hold items nobody has named yet, which is the normal state.
        marker_kv = " ".join("in%s=%d" % (w.capitalize(), r[w])
                             for w in QUEUE_PLACES)
        index_kv = " ".join("index%s=%d" % (w.capitalize(),
                                            qi.by_place[w]["numbered"])
                            for w in QUEUE_PLACES)
        # `unnumberedSkipped=N/M` is the paired reading rule 3b asks for:
        # numerator and its denominator in one value, one instant, no spaces.
        # M is `indexWalked`, item files opened across all three places with
        # the names exempt by name excluded and counted apart as indexExempt.
        print("  queueMarkers=%d docsWalked=%d rulingRecords=%d resolved=%d "
              "%s missing=%d malformed=%d indexed=%d %s indexWalked=%d "
              "indexExempt=%d unnumberedSkipped=%d/%d dupNumbers=%d"
              % (found, len(docs), rulings, r["resolved"], marker_kv,
                 r["missing"], bad, len(qi.index), index_kv, qi.walked,
                 qi.exempt, qi.unnumbered, qi.walked, qi.dups))
        # PER PLACE, AND AN ABSENT DIRECTORY SAYS SO. Without this line an
        # `inBlocked=0` reads as "no ruling names a parked item" when it may
        # mean "no blocked/ directory was opened", and those are different
        # facts about the tree.
        for w in QUEUE_PLACES:
            if not qi.exists[w]:
                print("  place=%s dir=%s/ ABSENT=nothing-measured-there"
                      "/an-absent-directory-is-not-an-empty-one"
                      % (w, place_rel(w)))
                continue
            b = qi.by_place[w]
            print("  place=%s dir=%s/ walked=%d numbered=%d unnumbered=%d "
                  "exemptByName=%d" % (w, place_rel(w), b["walked"],
                                       b["numbered"], b["unnumbered"],
                                       b["exempt"]))
        # THE UNNUMBERED, NEVER A SILENT ZERO. A file this index declined to
        # open is part of the denominator, and an item with no number cannot be
        # named by a marker however carefully a ruling is written.
        if qi.unnumbered:
            print("  UNNUMBERED AND THEREFORE UNNAMEABLE: %d of %d item "
                  "file(s) walked carry no NNN- prefix, so no marker can name "
                  "them and this index skips them: %s"
                  % (qi.unnumbered, qi.walked,
                     _qc.cap_list(qi.unnumbered_names)))
        else:
            print("  unnumberedSkipped=0 of %d item file(s) walked across "
                  "%s/: every item file carries a numeric prefix, so every "
                  "item CAN be named by a marker. A reading, not a silence."
                  % (qi.walked, "/".join(QUEUE_PLACES)))
        if not found:
            print(f"  0 marker(s) across {len(docs)} document(s) and "
                  f"{rulings} ruling record(s): NOT a clean sweep of the rule, "
                  f"an empty one. Nothing ordered work with a marker.")
    # THE FORM, PRINTED ON EVERY RUN. An author who never fails never sees a
    # failure message, so the only place the convention could be learned would
    # be this file's source. A gate for a form nobody is told is rule 6 with a
    # green light on it.
    print("  THE FORM, one line at column 0 in the ruling that orders the "
          "work: `QUEUE: <number> <name>`,")
    print("  the name space-free. Fenced or indented text is not scanned, so a "
          "record can show the form.")
    # THE COVERAGE LIMIT, PRINTED, because a check that implies it read the
    # prose is worse than no check: it retires the worry without doing the work.
    print("  COVERAGE LIMIT: this reads MARKERS, not prose. Every marker above "
          "was resolved against")
    print("  %s. An order to the queue written WITHOUT a marker is"
          % ", ".join("%s/" % place_rel(w) for w in QUEUE_PLACES))
    print("  invisible here and always will be, so the rule is a convention "
          "this only partly enforces.")
    # THE BLIND SPOT, SIZED AND NOT JUDGED. Rule 3b turned on the checker
    # itself: without this number, "0 missing" reads as coverage of the rule,
    # and the rule's whole population is unmarked prose today.
    print(f"  BLIND SPOT SIZED, NOT JUDGED: {prose_lines} line(s) in "
          f"{prose_docs} of {rulings} ruling record(s) contain "
          f"{QUEUE_PROSE[0]!r};")
    print(f"  {prose_unmarked} of those {prose_docs} carry no marker at all. "
          "This is NOT a finding and never fails.")
    print("  This program cannot tell an order from a mention, a deferral or a "
          "recollection; the count")
    print("  is here so that a zero above is read as markers checked, never as "
          "the rule covered.")


_fails = []


def check(ok, what, got=""):
    print(("  ok   " if ok else "  FAIL ") + what + ("" if ok else f": {got}"))
    if not ok:
        _fails.append(what)


def main():
    # ONE LEVEL WAS NEVER THE SCOPE, it was the shape of the directory the
    # day this was written. `game-design/agent-reports/` arrived on 24 Aug and
    # nothing examined it: adding a report left the count at 61/61 clean, so
    # the check could not tell "examined and fine" from "never looked" —
    # rule 3b, in the checker rather than in a metric. Its own convention
    # decayed inside one day: the first report carried the banner, the four
    # written the next night did not, because nothing enforced it.
    docs = sorted(DOCS.rglob("*.md"))
    print(f"docs-check — {len(docs)} documents under game-design/ (recursive)")
    seen = {k: 0 for k in KINDS}

    # THE QUEUE-ORDER SWEEP RIDES THIS WALK, and is collected BEFORE the
    # banner branch below, which `continue`s on a fault. A document missing its
    # banner can still carry a marker, and a gate that stops watching the
    # moment something unrelated goes wrong is the quietest kind there is.
    marks = []                 # [(path, markers, malformed)], documents with any
    ruling_docs = []           # the population Jafar's rule is about
    prose_lines = prose_docs = prose_unmarked = 0

    retired = 0            # COUNT of documents refused for the old banner
    for p in docs:
        text = p.read_text(encoding="utf-8")
        ms, bad_marks = queue_markers(text)
        if ms or bad_marks:
            marks.append((p, ms, bad_marks))
        if p.parent == DOCS and p.match(RULING_GLOB):
            ruling_docs.append(p)
            hits = sum(1 for line in text.split("\n")
                       if any(ph in line for ph in QUEUE_PROSE))
            if hits:
                prose_lines += hits
                prose_docs += 1
                if not ms:
                    prose_unmarked += 1
        head = "\n".join(text.split("\n")[:WITHIN_LINES])
        kind, fault = banner(head)
        if kind is None:
            retired += 1 if "retired" in fault else 0
            check(False, f"{p.name} declares a status in its first {WITHIN_LINES} lines",
                  fault)
            continue
        seen[kind] += 1

        if kind == "LOG":
            # A log without its date is the exact trap this file exists for.
            dated = LOG_DATE_RE.search(head)
            check(bool(dated), f"{p.name}: LOG entry carries its date", "undated LOG")
            check("NOT CURRENT" in head,
                  f"{p.name}: LOG entry says it is not current")
        if kind == "LIVE":
            # A live doc that has not been verified is just a log nobody
            # relabelled, which is how this went wrong the first time.
            check(bool(re.search(r"verified \d{4}-\d{2}-\d{2}", head)),
                  f"{p.name}: LIVE doc carries a verified date")

    print(f"\n  {seen['LIVE']} live, {seen['SPEC']} spec, {seen['LOG']} log")

    # A LIVE DOC THAT HAS GROWN A CHRONOLOGY IS NOT LIVE ANY MORE.
    #
    # The roadmap reached 1,525 lines of which ~85% was dated: thirteen
    # "BUILD STATE — <date>" sections interleaved with milestone definitions,
    # a 219-line "STILL OPEN" list four days stale, a 337-line re-sequencing.
    # The first pass of this checker gave it a LIVE banner and called it clean,
    # because a banner says what a document CLAIMS to be and nothing about
    # whether it still is. Jafar read it and said so.
    #
    # Two cheap shapes catch it: length, and dated headings. A live doc that
    # wants to be read has to stay short, and history belongs in a LOG.
    for p2 in docs:
        head = "\n".join(p2.read_text(encoding="utf-8").split("\n")[:WITHIN_LINES])
        if banner(head)[0] != "LIVE":
            continue
        # splitlines, NOT split("\n"): every text file here ends in a newline,
        # so split leaves a phantom empty final element and the count printed
        # in the failure message is one more than wc -l says. That made the
        # 400-line cap really a 399-line cap and sent me hunting for a line
        # that was not there — the instrument disagreeing with every other
        # line-counting tool in the project (rule 3).
        body = p2.read_text(encoding="utf-8").splitlines()
        # NARROWED, DELIBERATELY, after the first version flagged three docs
        # of which only one was really guilty. "§7.1 Streets and the car (M12,
        # built 2026-07-26)" is a design section carrying its provenance and is
        # good practice; "BUILD STATE — 2026-07-29" and "What changed on
        # 2026-07-29" are a diary. A date in a heading does not distinguish
        # them, so the check now looks for the diary markers rather than for
        # dates, and asserts only what it can actually tell.
        diary = [l for l in body
                 if re.match(r"^#{2,3} .*(BUILD STATE|[Ww]hat changed on|"
                             r"[Tt]he night of|[Oo]vernight|— round \d)", l)]
        check(not diary, f"{p2.name} — a live doc is not a diary",
              "; ".join(x.strip()[:44] for x in diary[:2]))
        # LENGTH IS FOR PLANS AND QUEUES, NOT FOR SPECIFICATIONS. A founding
        # design document is long by nature; a roadmap that is long has failed.
        # The doc says which it is rather than this file keeping a list.
        reference = "reference" in head
        if not reference:
            check(len(body) <= 400,
                  f"{p2.name} — a live plan stays scannable (<=400 lines)",
                  f"{len(body)} lines — mark it `reference` if it is a specification")
    # The roadmap is the tiebreak and has to say so, because two docs
    # disagreeing is the normal state of a project this size.
    road = (DOCS / "roadmap.md").read_text(encoding="utf-8")[:600]
    check("this wins" in road or "wins" in road,
          "roadmap.md claims precedence over other docs")

    # ORDERS TO THE QUEUE, per document. The whole-run counts are on the run's
    # own lines in queue_section() below, never mixed in with these, so a grep
    # across lines cannot read a per-document number as a run total.
    qi = queue_index(DOCS.parent)
    index = qi.index
    if not index:
        check(False, "the work queue is readable at all",
              "nothing measured: no numbered item under %s/, so no marker "
              "could be resolved" % _qc.QUEUE_REL)
    MARK_CAP = 8               # announced below when it bites
    shown = overflow = 0
    for p3, ms, bad_marks in marks:
        for ln, num, name in ms:
            if index.get(num):
                continue
            if shown >= MARK_CAP:
                overflow += 1
                continue
            shown += 1
            check(False,
                  "%s:%d orders %s as queue item %03d, and the item exists"
                  % (p3.name, ln, name, num),
                  "no production/queue/%03d-*.md and none under done/: the "
                  "ruling ordered work that was never filed" % num)
        for ln, raw in bad_marks:
            if shown >= MARK_CAP:
                overflow += 1
                continue
            shown += 1
            check(False, "%s:%d carries a QUEUE: line this can read"
                         % (p3.name, ln),
                  "malformed marker %r, wanted `QUEUE: <number> <name>` with "
                  "no spaces in the name" % raw)
    if overflow:
        print("  (+%d more queue-marker fault(s) not shown, cap %d)"
              % (overflow, MARK_CAP))
    queue_section(docs, marks, qi, len(ruling_docs),
                  prose_lines, prose_docs, prose_unmarked)
    qf_pass, qf_fail, qf_lines = queue_fixtures(qi)
    for line in qf_lines:
        print(line)
    if qf_fail:
        check(False, "the queue-marker fixtures agree with this checker",
              "%d of %d fixture(s) disagreed" % (qf_fail, qf_pass + qf_fail))
    print("  markerFixtures=%d/%d agreed (the live corpus above is the other "
          "accepting fixture)" % (qf_pass, qf_pass + qf_fail))

    # THE UNWALKED SET, NAMED. "117/117 clean" reads as full coverage of the
    # project's documents and is nothing of the kind: this checker's root is
    # game-design/ alone, and since the v2 respec landed there are two more
    # markdown trees it has never opened. Saying so out loud costs three lines
    # and stops a clean result being read as a claim about documents nobody
    # examined. Widening the scope is a DECISION, not a tidy-up: the v2
    # package carries its own conventions and would go red on this one.
    root = DOCS.parent
    unwalked = []
    for other in ("production", "ledger-v2", "legacy"):
        d = root / other
        if d.is_dir():
            unwalked.append((other, sum(1 for _ in d.rglob("*.md"))))
    if unwalked:
        print("\nNOT WALKED (this checker's root is game-design/ only): " +
              ", ".join(f"{n}/ {c} doc(s)" for n, c in unwalked) +
              " — those trees carry the v2 conventions and are not checked here.")
        print("  QUEUE: markers are not read there either. The rule is scoped "
              "to rulings, and a ruling")
        print("  record is game-design/decision-*.md, the definition "
              "ledger/verify.py already uses.")

    # THE BANNER FIXTURES RUN ON EVERY RUN, not behind a flag. A selftest
    # nobody runs is rule 6 wearing a lab coat, and what these two fixtures
    # guard is SILENT: the day the accepting pattern stops matching, every
    # document goes red at once and reads as 135 broken documents; the day the
    # refusal stops firing, the retired form comes back one file at a time and
    # nothing says a word. They are pure string work and cost no file read.
    fx_pass, fx_fail, fx_lines = banner_fixtures()
    for line in fx_lines:
        print(line)
    if fx_fail:
        check(False, "the banner fixtures agree with this checker",
              f"{fx_fail} of {fx_pass + fx_fail} fixture(s) disagreed")

    print(f"\n  banner form: {seen['LIVE'] + seen['SPEC'] + seen['LOG']} of "
          f"{len(docs)} document(s) carry the ruled colon banner, {retired} "
          f"carry the retired em-dash form (ruled out 2026-09-03), "
          f"{fx_pass}/{fx_pass + fx_fail} synthetic fixture(s) agreed")

    print(f"\n{len(docs) - len(_fails)}/{len(docs)} clean under game-design/"
          if not _fails else f"\n{len(_fails)} problem(s)")
    return 1 if _fails else 0


# ------------------------------------------------------------------- fixtures

# ACCEPTING FIRST, and the accepting fixture that matters most is the LIVE
# CORPUS: `main()` walks 135 real documents and a checker nothing survives
# would show up there before it showed up here. These synthetic pairs cover
# the two things the corpus cannot: the form that no longer exists anywhere
# (so nothing real can exercise the refusal) and the forms nobody has written
# yet.
BANNER_ACCEPT = [
    ("bold colon banner", "> **STATUS: LIVE, verified 2026-09-03.**", "LIVE"),
    ("plain colon banner, what two roles wrote unprompted",
     "STATUS: LOG, 2026-09-03. NOT CURRENT.", "LOG"),
    ("spec banner", "**STATUS: SPEC, 2026-08-25.**", "SPEC"),
    ("a lawful banner beside an inline QUOTATION of the retired form",
     "> **STATUS: LOG, 2026-09-02. NOT CURRENT.**\nIt matched "
     "`\\*\\*STATUS ... LOG` once.", "LOG"),
]
# The rejecting fixtures are synthetic and none of them is a real document:
# a rejecting fixture pinned to a real file breaks the day somebody fixes the
# file, which is the trap of making the work break the tool.
BANNER_REJECT = [
    ("the retired em-dash form", "> **STATUS \u2014 LIVE, verified 2026-09-03.**",
     "retired"),
    ("the retired form with no bold marks", "STATUS \u2014 SPEC, 2026-08-25.",
     "retired"),
    ("a half-migrated file carrying BOTH forms",
     "> **STATUS: LIVE, verified 2026-09-03.**\n> **STATUS \u2014 LIVE.**",
     "retired"),
    ("no banner at all", "# A document with a title and nothing else",
     "no STATUS banner"),
]


def banner_fixtures():
    """(passed, failed, lines). PURE: no file is read, so this is cheap enough
    to run on every invocation."""
    passed, failed, lines = 0, 0, []
    for name, text, want in BANNER_ACCEPT:
        kind, fault = banner(text)
        if kind == want:
            passed += 1
        else:
            failed += 1
            lines.append(f"  FAIL fixture (accepting) {name}: got "
                         f"{kind!r}/{fault!r}, wanted {want}")
    for name, text, want in BANNER_REJECT:
        kind, fault = banner(text)
        if kind is None and fault and want in fault:
            passed += 1
        else:
            failed += 1
            lines.append(f"  FAIL fixture (rejecting) {name}: got "
                         f"{kind!r}/{fault!r}, wanted a fault naming {want!r}")
    return passed, failed, lines



# ------------------------------------------------- queue-marker fixtures
#
# ACCEPTING FIRST, and the first accepting fixture is THE LIVE CORPUS: a plain
# run reads every real marker under game-design/ and resolves it against the
# real queue. The pairs below cover what the corpus cannot. The accepting ones
# are forms nobody has written yet; the rejecting ones are SYNTHETIC, because a
# rejecting fixture pinned to a real item goes green the day somebody files it
# and red the day somebody archives it, which is the trap of making the work
# break the tool.
QUEUE_ACCEPT = [
    ("the form the 2026-09-10 exposure ruling now carries",
     "QUEUE: 276 settled-night-exposure-reference",
     (276, "settled-night-exposure-reference")),
    ("a marker below prose, which is where a ruling puts it",
     "...goes to the queue with a name:\nQUEUE: 12 a-second-item",
     (12, "a-second-item")),
    ("tabs rather than spaces", "QUEUE:\t7\tseven-by-tab", (7, "seven-by-tab")),
    ("a name carrying structure without spaces, per the key=value rule",
     "QUEUE: 42 exposure/night-pin..four-rungs",
     (42, "exposure/night-pin..four-rungs")),
]
# MALFORMED IS A FAULT, NOT A SKIP. The first two are the real failure shapes:
# an item named with no number is exactly what the 2026-09-10 ruling did.
QUEUE_MALFORMED = [
    ("a number and no name, so a failure could not say what went missing",
     "QUEUE: 276"),
    ("a name and no number, the 2026-09-10 shape Jafar ruled against",
     "QUEUE: settled-night-exposure-reference"),
    ("a name with spaces in it, which every reader would truncate",
     "QUEUE: 276 settled night exposure reference"),
    ("nothing after the colon", "QUEUE:"),
]
# Neither a marker nor a fault: a record must be able to SHOW the form.
QUEUE_IGNORED = [
    ("the form inside a fenced block, so this document can quote it",
     "```\nQUEUE: 276 settled-night-exposure-reference\n```"),
    ("the form indented as a code sample", "    QUEUE: 999 a-sample"),
    ("the word in a sentence", "It goes to the QUEUE: by name, they said."),
]
# A NUMBER THAT EXISTS NOWHERE AND CANNOT BE MADE TO EXIST BY DOING THE WORK:
# the queue is three digits by convention and 900 is its highest item, so no
# amount of filing turns this green. That is the point of a synthetic key.
QUEUE_ABSENT = 9999
QUEUE_ABSENT_NAME = "a-name-no-record-has-ever-written"

# ------------------------------------------ the planted tree (ruled 2026-09-14)
#
# `production/queue/blocked/` DOES NOT EXIST in this repository today, so the
# live corpus cannot exercise the blocked branch and will not until the day it
# suddenly matters, which is the day a ruling would go red for work being done
# correctly. A PLANTED TREE is the only fixture that can exercise it, and the
# ruling of 2026-09-14 section 5 asks for exactly this one: one item in each of
# the three places plus one unnumbered file, so all four readings that
# condition added (inQueue, inBlocked, inDone, unnumberedSkipped) are exercised
# in ONE walk at ONE instant.
#
# IT IS PLANTED, NOT PINNED. The unnumbered file carries a synthetic name that
# exists nowhere. The live one that prompted the condition
# (`production/queue/art-atlas-01-integration.md`) is deliberately NOT used,
# because the right fix for that file is to give it a number, and a fixture the
# fix would break is the trap this file's comments already name twice.
PLANTED_UNNUMBERED = "an-unnumbered-item-no-marker-can-name.md"


def planted_queue_tree():
    """A throwaway repository root: one item in each place of QUEUE_PLACES,
    numbered 1..N in that order, plus one unnumbered item and one file exempt
    by name.

    BUILT BY QUEUE-CHECK'S OWN `_tree`, which REGISTERS its cleanup with
    atexit: this runs inside ledger/verify.py at every commit, and a fixture
    that leaks a directory into /tmp on every run is its own small fault. The
    items are laid out FROM QUEUE_PLACES rather than typed out, so the day a
    fourth place is added the fixture covers it without being remembered."""
    files = {
        "%s/README.md" % _qc.QUEUE_REL:
            "# documentation, exempt BY NAME, not an item\n",
        "%s/%s" % (_qc.QUEUE_REL, PLANTED_UNNUMBERED):
            _qc._item("READY 2026-09-14"),
    }
    for i, w in enumerate(QUEUE_PLACES, 1):
        files["%s/%03d-planted-in-%s.md" % (place_rel(w), i, w)] = _qc._item(
            "READY 2026-09-14" if w == QUEUE_TOP else "LANDED 2026-09-14")
    return _qc._tree(files)


#: What one run of the planted tree yields. `accepting` and `rejecting` are
#: counted rather than written down, so the selftest's split cannot drift from
#: the checks actually run.
PlantedRun = collections.namedtuple(
    "PlantedRun", "passed failed lines summary accepting rejecting")


def planted_tree_fixture():
    """A PlantedRun. ACCEPTING CASES FIRST.

    One walk of the planted tree, checking the four readings this condition
    added and the agreement with the one counter of the queue. The summary
    line's keys are all prefixed `fixture`, so a grep across lines can never
    read a planted number as a live one: two moments, two vocabularies."""
    passed, failed, lines = 0, 0, []
    accepting = rejecting = 0

    def verdict(good, kind, name, got):
        nonlocal passed, failed, accepting, rejecting
        if kind.startswith("accepting"):
            accepting += 1
        else:
            rejecting += 1
        if good:
            passed += 1
        else:
            failed += 1
            lines.append("  FAIL fixture (%s) %s: %s" % (kind, name, got))

    t = planted_queue_tree()
    qi = queue_index(t)
    numbers = list(range(1, len(QUEUE_PLACES) + 1))
    r = resolve_markers(qi.index, numbers + [QUEUE_ABSENT])
    want_places = dict(zip(numbers, QUEUE_PLACES))
    got_places = {n: qi.index[n][0][0] for n in numbers if n in qi.index}

    verdict(all(qi.exists[w] for w in QUEUE_PLACES), "accepting",
            "every place in QUEUE_PLACES exists on the planted tree and was "
            "walked", "exists=%r" % (qi.exists,))
    verdict(got_places == want_places and len(qi.index) == len(QUEUE_PLACES),
            "accepting", "one item indexed at each place, in place order",
            "got %r of %d indexed, wanted %r" % (got_places, len(qi.index),
                                                 want_places))
    verdict(all(r[w] == 1 for w in QUEUE_PLACES)
            and r["resolved"] == len(QUEUE_PLACES), "accepting",
            "a marker naming the item in each place resolves there",
            "got %r" % {k: r[k] for k in list(QUEUE_PLACES) + ["resolved"]})
    verdict(qi.unnumbered == 1 and qi.walked == len(QUEUE_PLACES) + 1
            and qi.unnumbered_names == ["%s/%s" % (QUEUE_TOP,
                                                   PLANTED_UNNUMBERED)],
            "accepting", "the unnumbered item is COUNTED against the walk, not "
            "dropped", "unnumberedSkipped=%d/%d names=%r"
            % (qi.unnumbered, qi.walked, qi.unnumbered_names))
    verdict(qi.exempt == 1 and qi.by_place[QUEUE_TOP]["exempt"] == 1,
            "accepting", "README.md is exempt BY NAME and counted apart from "
            "the walk", "exempt=%d walked=%d" % (qi.exempt, qi.walked))
    # THE ONE COUNTER AND THIS INDEX, ON THE SAME TREE AT THE SAME INSTANT.
    # queue-check.py names blocked/ and done/ as string literals that this file
    # has to repeat; this is the pin. Its `walked` is the top level only and
    # its `blocked` here is exactly the moved item, because no planted item
    # carries a blocked status word in place.
    qc = _qc.count_queue(t)
    qc_total = qc["walked"] + qc["blocked"] + qc["done"]
    agrees = (qc["blocked_dir"] and qc["done_dir"] and qc_total == qi.walked)
    verdict(agrees, "accepting",
            "queue-check.py walks the same three places to the same total",
            "queue-check top=%d blocked=%d done=%d total=%d, this index "
            "walked=%d, blocked_dir=%s done_dir=%s"
            % (qc["walked"], qc["blocked"], qc["done"], qc_total, qi.walked,
               qc["blocked_dir"], qc["done_dir"]))
    verdict(r["missing"] == 1, "rejecting/missing",
            "item %d resolves nowhere on the planted tree either" % QUEUE_ABSENT,
            "missing=%d, wanted 1" % r["missing"])

    kv = " ".join("fixtureIn%s=%d" % (w.capitalize(), r[w])
                  for w in QUEUE_PLACES)
    summary = ("  PLANTED TREE (no blocked/ exists live, so only a planted "
               "tree can exercise it): %s fixtureIndexed=%d "
               "fixtureUnnumberedSkipped=%d/%d fixtureExemptByName=%d "
               "fixtureMissing=%d fixtureQueueCheckAgrees=%s"
               % (kv, len(qi.index), qi.unnumbered, qi.walked, qi.exempt,
                  r["missing"], "yes" if agrees else "NO"))
    return PlantedRun(passed, failed, lines, summary, accepting, rejecting)


def queue_fixtures(qi):
    """(passed, failed, lines). ACCEPTING CASES FIRST.

    Runs on EVERY invocation, like the banner fixtures and for the same reason:
    what it guards is silent. The day the marker form stops matching, every
    marker in the corpus passes WITHOUT BEING READ and the run still prints a
    clean line. Parsing is pure and the resolution fixtures reuse the index
    main() already built; the planted tree is the one part that touches disk,
    five small files under the system temp directory with its cleanup
    registered, and it is the only way to exercise a place the live tree does
    not have."""
    index = qi.index
    passed, failed, lines = 0, 0, []

    def verdict(good, kind, name, got):
        nonlocal passed, failed
        if good:
            passed += 1
        else:
            failed += 1
            lines.append("  FAIL fixture (%s) %s: %s" % (kind, name, got))

    for name, text, want in QUEUE_ACCEPT:
        ms, bad = queue_markers(text)
        verdict(len(ms) == 1 and not bad and ms[0][1:] == want,
                "accepting", name, "got %r/%r, wanted one marker %r"
                % (ms, bad, want))
    # The corpus's own lowest-numbered item, so this accepting case cannot be
    # broken by anybody filing, finishing or archiving anything.
    if index:
        low = min(index)
        ms, _bad = queue_markers("QUEUE: %d the-lowest-item-on-disk" % low)
        verdict(bool(ms) and bool(index.get(ms[0][1])), "accepting",
                "the lowest-numbered real item (%03d) resolves" % low,
                "did not resolve against %d indexed item(s)" % len(index))
    else:
        lines.append("  FAIL fixture (accepting) a real item resolves: "
                     "nothing measured, the queue index is empty")
        failed += 1
    # THE PLANTED TREE, still accepting cases: the place the live tree does not
    # have, and the skip the live tree does not print a name for.
    planted = planted_tree_fixture()
    passed += planted.passed
    failed += planted.failed
    lines += planted.lines
    lines.append(planted.summary)
    for name, text in QUEUE_MALFORMED:
        ms, bad = queue_markers(text)
        verdict(len(bad) == 1 and not ms, "rejecting/malformed", name,
                "got %r/%r, wanted one malformed line and no marker" % (ms, bad))
    for name, text in QUEUE_IGNORED:
        ms, bad = queue_markers(text)
        verdict(not ms and not bad, "rejecting/ignored", name,
                "got %r/%r, wanted neither a marker nor a fault" % (ms, bad))
    ms, bad = queue_markers("QUEUE: %d %s" % (QUEUE_ABSENT, QUEUE_ABSENT_NAME))
    verdict(len(ms) == 1 and not index.get(QUEUE_ABSENT), "rejecting/missing",
            "a marker naming item %d, which exists nowhere" % QUEUE_ABSENT,
            "either it did not parse (%r) or the index claims it exists" % ms)
    return passed, failed, lines


def selftest():
    """The verbose form of the fixtures above, ACCEPTING CASE FIRST."""
    print("docs-check --selftest: ACCEPTING CASES FIRST\n")
    bad = qbad = 0
    for name, text, want in BANNER_ACCEPT:
        kind, fault = banner(text)
        good = kind == want
        bad += 0 if good else 1
        print(("  ok   " if good else "  FAIL ") +
              f"{name}: {kind or fault}")
    print("\n  THE RETIRED FORM, refused, and one fixture with no banner:\n")
    for name, text, want in BANNER_REJECT:
        kind, fault = banner(text)
        good = kind is None and fault and want in fault
        bad += 0 if good else 1
        print(("  ok   " if good else "  FAIL ") +
              f"{name}: {fault or ('accepted as ' + str(kind))}")
    n = len(BANNER_ACCEPT) + len(BANNER_REJECT)
    print(f"\n  banner fixtures: {n - bad} passed, {bad} failed, "
          f"{len(BANNER_ACCEPT)} accepting, {len(BANNER_REJECT)} rejecting.")

    # THE QUEUE-ORDER RULE, ACCEPTING CASES FIRST AND THE LIVE REPO AMONG THEM.
    print("\nQUEUE ORDERS (Jafar 2026-09-14). ACCEPTING CASES FIRST, and the "
          "first is the live repo:\n")
    qi = queue_index(DOCS.parent)
    index = qi.index
    print("  ok   %d item(s) indexed by number over %d item file(s) walked, "
          "%d exempt by name, %d duplicate number(s)"
          % (len(index), qi.walked, qi.exempt, qi.dups))
    for w in QUEUE_PLACES:
        if qi.exists[w]:
            b = qi.by_place[w]
            print("       place=%s dir=%s/ walked=%d numbered=%d "
                  "unnumbered=%d exemptByName=%d"
                  % (w, place_rel(w), b["walked"], b["numbered"],
                     b["unnumbered"], b["exempt"]))
        else:
            print("       place=%s dir=%s/ ABSENT=nothing-measured-there"
                  " (the planted tree below is the only fixture that can "
                  "exercise it)" % (w, place_rel(w)))
    if qi.unnumbered:
        print("       unnumberedSkipped=%d/%d item file(s) carry no NNN- "
              "prefix and NO MARKER CAN NAME THEM: %s"
              % (qi.unnumbered, qi.walked, _qc.cap_list(qi.unnumbered_names)))
    else:
        print("       unnumberedSkipped=0 of %d item file(s) walked: every "
              "item can be named by a marker. A reading, not a silence."
              % qi.walked)
    for name, text, want in QUEUE_ACCEPT:
        ms, bad_m = queue_markers(text)
        good = len(ms) == 1 and not bad_m and ms[0][1:] == want
        qbad += 0 if good else 1
        print(("  ok   " if good else "  FAIL ") + "%s: %s"
              % (name, ms[0][1:] if ms else (ms, bad_m)))
    if index:
        low = min(index)
        ms, _b = queue_markers("QUEUE: %d the-lowest-item-on-disk" % low)
        good = bool(ms) and bool(index.get(ms[0][1]))
        qbad += 0 if good else 1
        print(("  ok   " if good else "  FAIL ") +
              "a marker naming real item %03d resolves to %s"
              % (low, index.get(low)))
    else:
        qbad += 1
        print("  FAIL nothing measured: the queue index is empty")
    # The live corpus, which is the accepting fixture that matters most.
    docs = sorted(DOCS.rglob("*.md"))
    live_marks = 0
    live_missing = []
    for p in docs:
        ms, bad_m = queue_markers(p.read_text(encoding="utf-8"))
        live_marks += len(ms)
        live_missing += [(p.name, ln, num, nm) for ln, num, nm in ms
                         if not index.get(num)]
        live_missing += [(p.name, ln, "malformed", raw) for ln, raw in bad_m]
    good = live_marks > 0 and not live_missing
    qbad += 0 if good else 1
    print(("  ok   " if good else "  FAIL ") +
          "THE LIVE CORPUS: %d marker(s) across %d document(s), %d unresolved"
          % (live_marks, len(docs), len(live_missing)) +
          ("" if not live_missing else " " + repr(live_missing[:3])) +
          ("" if live_marks else " - nothing measured, no marker exists to check"))

    # THE PLANTED TREE, STILL ACCEPTING. Four readings from one walk, and the
    # only fixture that can exercise blocked/ while no blocked/ exists live.
    planted = planted_tree_fixture()
    qbad += planted.failed
    print("\n  THE PLANTED TREE (ruled 2026-09-14 section 5): one item in each "
          "of %d places, one unnumbered\n  file, one file exempt by name. "
          "%d check(s), %d accepting and %d rejecting:\n"
          % (len(QUEUE_PLACES), planted.passed + planted.failed,
             planted.accepting, planted.rejecting))
    print(("  ok   " if not planted.failed else "  FAIL ")
          + "%d of %d planted-tree check(s) agreed"
          % (planted.passed, planted.passed + planted.failed))
    for line in planted.lines:
        print(line)
    print(planted.summary)

    print("\n  REJECTING, ALL SYNTHETIC. Malformed markers, ignored forms, and "
          "a number that exists nowhere:\n")
    for name, text in QUEUE_MALFORMED:
        ms, bad_m = queue_markers(text)
        good = len(bad_m) == 1 and not ms
        qbad += 0 if good else 1
        print(("  ok   " if good else "  FAIL ") + "%s: %s"
              % (name, "malformed, refused" if good else (ms, bad_m)))
    for name, text in QUEUE_IGNORED:
        ms, bad_m = queue_markers(text)
        good = not ms and not bad_m
        qbad += 0 if good else 1
        print(("  ok   " if good else "  FAIL ") + "%s: %s"
              % (name, "not a marker, not a fault" if good else (ms, bad_m)))
    ms, _b = queue_markers("QUEUE: %d %s" % (QUEUE_ABSENT, QUEUE_ABSENT_NAME))
    good = len(ms) == 1 and not index.get(QUEUE_ABSENT)
    qbad += 0 if good else 1
    print(("  ok   " if good else "  FAIL ") +
          "item %d, which exists nowhere: %s"
          % (QUEUE_ABSENT, "parsed and reported missing" if good
             else ("parsed %r, index says %r" % (ms, index.get(QUEUE_ABSENT)))))

    p_total = planted.passed + planted.failed
    qn = (len(QUEUE_ACCEPT) + len(QUEUE_MALFORMED) + len(QUEUE_IGNORED) + 3
          + p_total)
    print(f"\n  queue fixtures: {qn - qbad} passed, {qbad} failed, "
          f"{len(QUEUE_ACCEPT) + 2 + planted.accepting} accepting (2 of them "
          f"the live repo, {planted.accepting} the planted tree), "
          f"{len(QUEUE_MALFORMED) + len(QUEUE_IGNORED) + 1 + planted.rejecting}"
          f" rejecting.")
    print("  COVERAGE LIMIT, the same words a plain run prints: this reads "
          "MARKERS, not prose.")
    print("  An order to the queue written without a marker is invisible here "
          "and always will be.")

    total, allbad = n + qn, bad + qbad
    print(f"\ndocs-check --selftest: {'PASS' if not allbad else 'FAILED'}. "
          f"{total - allbad} passed, {allbad} failed, of {total} fixture(s) "
          f"in two families. The live corpus is the accepting fixture that "
          f"matters most and is walked by a plain run.")
    return 0 if not allbad else 3


if __name__ == "__main__":
    # A correct run that ends in a BrokenPipeError traceback costs twenty
    # minutes before anybody notices it worked.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    _ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    _ap.add_argument("--selftest", action="store_true")
    sys.exit(selftest() if _ap.parse_args().selftest else main())
