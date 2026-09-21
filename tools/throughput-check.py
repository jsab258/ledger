#!/usr/bin/env python3
"""The throughput ledger's BATCH rows: the shape, the series, and the zeros.

    python3 tools/throughput-check.py             # the gate, on this repo
    python3 tools/throughput-check.py --series    # the printed series
    python3 tools/throughput-check.py --selftest  # accepting case FIRST

WHY THIS EXISTS. Queue 403, from Jafar 2026-09-21: "the throughput ledger
takes a batch as its unit and counts rejected attempts, since the industry
research found nobody measures rework and ours would be the instrument that
does." Until this landed, `production/throughput.md` had one unit, the piece,
and NO FIELD ANYWHERE for an attempt that was thrown away: a facade rejected
at review left no mark on the ledger it failed against. A ledger that counts
only what survived prices the wrong thing, because the cost of a unit of
content includes the attempts nobody kept.

WHAT A ZERO MEANS HERE, and the whole instrument turns on it. There are three
states for a rejection count and they must never collapse into one:

    attemptsRejected=0/of=4-attempts      four attempts, none rejected
    attemptsRejected=0/of=0-attempts-so-far   nothing has been attempted yet
    attemptsRejected=nothing-measured     NOBODY COUNTED, and the batch ran

The third is what every batch before 2026-09-21 reads, because the field did
not exist while the work happened. A retrospective zero there would be an
invented measurement. So this checker REFUSES a bare zero anywhere in a batch
block: a zero ships its denominator or it is not a reading (CLAUDE.md 3b).
`nothing-measured` is the no-space token form of the words "nothing measured",
which is what this tool prints in prose when it walked no batches at all.

WHAT IT ASSERTS, each printing what it examined:

  A1 SHAPE. Every batch block carries its seven labelled lines (batch,
     unit, attempts, before, after, machine, wear) and the required keys on each.
  A2 NO BARE ZERO, and no bare word where a key=value belongs. A value of
     exactly `0` fails; so does a stray token with no `=`, which is what a
     value containing a space looks like after any reader splits on space.
  A3 THE COUNTS ARE CONSISTENT: rejected <= attempts, a resolved batch has a
     close instant, an OPEN batch has `closed=not-yet` rather than a fake one.
  A4 THE DEFINITIONS ARE STILL IN THE FILE: the piece-unit sentence, the
     batch-unit sentence and the rejected-attempt sentence. A row shape whose
     definition has been edited away is a column of numbers with no unit.
  A5 NO BATCH BLOCK IS A PIPE TABLE. Measured, not feared:
     `tools/dashboard/build-dashboard.py:425` takes EVERY pipe row with four
     or more cells, and `read_throughput` at :1216 sums cell 3 of every row
     whose cell 1 matches the current ISO week. A batch written as a table row
     would therefore be added to the dashboard's verified-piece count in
     silence. That is why the batch rows are blocks and not a table.

WHAT IT DOES NOT CLAIM. It does not judge whether a batch SHOULD have been
rejected, and it sets NO BOUND on rejections, sessions or minutes per batch. A
bound needs a printed series over real runs and this is the printer; `--series`
prints the points, and the count of points is printed beside them so a reader
can see how thin the series still is.

PRICED, and it is queue 369's four conditions rather than this tool's opinion:
end to end (the batch resolved), the rejected work counted in (not
`nothing-measured`), BOTH meters read BEFORE and AFTER, and nothing else
running in that window (`cleanWindow=yes`, which only Jafar can say). A batch
missing any one is counted as UNPRICED and named. It is not a failure: an
unpriced batch is a true state of the world. It is a failure to let one read
as priced.

EXIT CODES, distinct per outcome. 0 clean. 1 at least one batch block or
definition failed, each named. 2 the ledger is missing or carries no batch
section, so this run measured nothing and says so rather than reporting a
clean sweep it did not perform. 3 the selftest failed.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(REPO, "production", "throughput.md")

NOTHING = "nothing measured"
NM = "nothing-measured"

#: The block head. `### BATCH <id>` opens one; anything else closes it.
HEAD_RE = re.compile(r"^###\s+BATCH\s+(\S+)\s*$")
#: A labelled reading line inside a block: `label: key=value key=value ...`
LINE_RE = re.compile(r"^(batch|unit|attempts|before|after|machine|wear):\s+(.*)$")
#: The section this tool reads. Everything below it, to the next `## `.
SECTION_RE = re.compile(r"^##\s+.*BATCH", re.I)

#: label -> keys that must be present. Values are checked below by name.
REQUIRED = {
    "batch": ("batchId", "line", "status", "opened", "closed"),
    "unit": ("deliverables", "deliverableUnit"),
    "attempts": ("attemptsMade", "attemptsRejected", "rejectedAtStation"),
    # TWO INSTANTS, NAMED SEPARATELY. The meter is a row Jafar reported and
    # the session count is read off the log now; one `takenAt` standing for
    # both would print two moments as one.
    "before": ("meterTakenAt", "meterTotalPct", "meterFablePct", "meterSource",
               "sessionsTakenAt", "sessionsCumulative", "sha"),
    "after": ("meterTakenAt", "meterTotalPct", "meterFablePct", "meterSource",
              "sessionsTakenAt", "sessionsCumulative", "sha", "cleanWindow"),
    # THE MACHINE HALF, which queue 403's spec names: "a runner-time
    # denominator where measured". A SUM over the steps the verdict times,
    # never the job, which is the distinction the cost section above draws.
    "machine": ("runnerMinutes", "runnerSteps"),
    "wear": ("wearCoverageN", "wearCoverageMin"),
}
STATUSES = ("OPEN", "VERIFIED", "REJECTED")
CLEAN = ("yes", "no", "not-stated")

#: The sentences that give the numbers their unit. Phrases, never values: a
#: constant read off the live tree is the fault queue 416 files.
DEFINITIONS = (
    ("piece-unit", "A piece counts when it passes station 3"),
    ("batch-unit", "A batch counts when"),
    ("rejected-unit", "An attempt counts as REJECTED when"),
)

#: A count with its denominator: `0/of=4-attempts`, `2/of=2-attempts-so-far`.
COUNT_RE = re.compile(r"^(\d+)/of=(\d+)(-[a-z-]+)?$")
INT_RE = re.compile(r"^\d+$")


def cap(items, n=6, sep=","):
    """Every cap announces itself, and an empty list reads as none."""
    items = list(items)
    if not items:
        return "none"
    if len(items) <= n:
        return sep.join(items)
    return sep.join(items[:n]) + sep + "(+%d-more-not-shown)" % (len(items) - n)


def tokens(rest):
    """(pairs, strays). A stray is a token with no `=`, which is what a value
    containing a space becomes the moment anything splits on whitespace."""
    pairs, strays = [], []
    for tok in rest.split():
        if "=" in tok and not tok.startswith("="):
            k, v = tok.split("=", 1)
            pairs.append((k, v))
        else:
            strays.append(tok)
    return pairs, strays


def parse(text):
    """(blocks, tableRowsInSection, sawSection). A block is a dict of label ->
    (dict of key -> value, strays), plus its id and its line number."""
    blocks, table_rows = [], []
    in_section = False
    cur = None
    label = None
    for i, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        if SECTION_RE.match(line):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            in_section = False
            cur = None
            continue
        if not in_section:
            continue
        if line.lstrip().startswith("|"):
            table_rows.append(i)
            continue
        m = HEAD_RE.match(line)
        if m:
            cur = {"id": m.group(1), "line": i, "labels": {}}
            label = None
            blocks.append(cur)
            continue
        if line.startswith("### "):
            # A heading that is not a batch head closes the block, so its
            # lines are never attributed to the batch above it.
            cur, label = None, None
            continue
        m = LINE_RE.match(line)
        if m and cur is not None:
            label = m.group(1)
            cur["labels"][label] = ({}, [], [], i)
            _absorb(cur["labels"][label], m.group(2))
            continue
        # A CONTINUATION LINE, so a reading may wrap and stay readable: it is
        # indented and its first token is a key=value. Prose sits at column 0
        # and is not parsed, which is how a block carries its own sentences.
        if (cur is not None and label is not None and raw[:1].isspace()
                and line.strip() and "=" in line.split()[0]):
            _absorb(cur["labels"][label], line.strip())
    return blocks, table_rows, in_section


def _absorb(slot, rest):
    kv, strays, dupes, _ln = slot
    pairs, more = tokens(rest)
    strays.extend(more)
    for k, v in pairs:
        if k in kv:
            dupes.append(k)
        kv[k] = v


def count_pair(value):
    """(numerator, denominator, ok). `nothing-measured` is (None, None, True):
    it is a legal reading, and the one thing a zero must not be mistaken for."""
    if value == NM:
        return None, None, True
    m = COUNT_RE.match(value)
    if not m:
        return None, None, False
    return int(m.group(1)), int(m.group(2)), True


def audit_block(b):
    """Every violation this block carries, as (code, detail) with no spaces in
    the detail's values, so the failure line survives a whitespace split."""
    bad = []
    labels = b["labels"]
    for label, keys in REQUIRED.items():
        if label not in labels:
            bad.append(("missing-line", "%s:%s" % (b["id"], label)))
            continue
        kv, strays, dupes, ln = labels[label]
        for s in strays:
            bad.append(("stray-token-or-value-with-a-space",
                        "%s:%s:%s" % (b["id"], label, s)))
        for d in dupes:
            bad.append(("key-written-twice", "%s:%s:%s" % (b["id"], label, d)))
        for k in keys:
            if k not in kv:
                bad.append(("missing-key", "%s:%s:%s" % (b["id"], label, k)))
        for k, v in kv.items():
            if v == "":
                bad.append(("empty-value", "%s:%s:%s" % (b["id"], label, k)))
            elif v == "0":
                # A ZERO SHIPS ITS DENOMINATOR OR IT IS NOT A READING.
                bad.append(("bare-zero-no-denominator",
                            "%s:%s:%s" % (b["id"], label, k)))
            elif " " in v:
                bad.append(("value-with-a-space",
                            "%s:%s:%s" % (b["id"], label, k)))

    head = labels.get("batch", ({}, [], [], 0))[0]
    status = head.get("status")
    if status is not None and status not in STATUSES:
        bad.append(("status-not-one-of-%s" % "/".join(STATUSES),
                    "%s:%s" % (b["id"], status)))
    closed = head.get("closed")
    if status in ("VERIFIED", "REJECTED") and closed in ("not-yet", NM):
        bad.append(("resolved-batch-with-no-close-instant",
                    "%s:status=%s/closed=%s" % (b["id"], status, closed)))
    if status == "OPEN" and closed not in (None, "not-yet"):
        bad.append(("open-batch-carrying-a-close-instant",
                    "%s:closed=%s" % (b["id"], closed)))
    if head.get("batchId") not in (None, b["id"]):
        bad.append(("batchId-does-not-match-its-heading",
                    "%s:%s" % (b["id"], head.get("batchId"))))

    att = labels.get("attempts", ({}, [], [], 0))[0]
    rej = att.get("attemptsRejected")
    if rej is not None:
        n, d, ok = count_pair(rej)
        if not ok:
            bad.append(("attemptsRejected-not-a-count-with-a-denominator",
                        "%s:%s" % (b["id"], rej)))
        elif n is not None and n > d:
            bad.append(("more-rejected-than-attempted",
                        "%s:%s" % (b["id"], rej)))
    made = att.get("attemptsMade")
    if made is not None and made != NM:
        m = re.match(r"^(\d+)-cumulative$", made)
        if not m:
            bad.append(("attemptsMade-must-be-N-cumulative-or-%s" % NM,
                        "%s:%s" % (b["id"], made)))
        elif rej is not None:
            n, d, ok = count_pair(rej)
            if ok and d is not None and d != int(m.group(1)):
                bad.append(("rejected-denominator-is-not-attemptsMade",
                            "%s:%s/vs=%s" % (b["id"], rej, made)))

    after = labels.get("after", ({}, [], [], 0))[0]
    cw = after.get("cleanWindow")
    if cw is not None and cw not in CLEAN:
        bad.append(("cleanWindow-not-one-of-%s" % "/".join(CLEAN),
                    "%s:%s" % (b["id"], cw)))
    # THE SESSION DENOMINATOR CARRIES ITS SOURCE INLINE. A count of sessions
    # with no file behind it is a number somebody remembered.
    for lab in ("before", "after"):
        v = labels.get(lab, ({}, [], [], 0))[0].get("sessionsCumulative")
        if v not in (None, NM) and not re.match(r"^\d+/src=\S+$", v):
            bad.append(("sessionsCumulative-names-no-source",
                        "%s:%s:%s" % (b["id"], lab, v)))

    # THE DENOMINATOR IS FIXED BEFORE THE WORK, OR IT WAS CHOSEN AFTER IT.
    # Three legal forms, and a resolved batch may not still be unfixed.
    unit = labels.get("unit", ({}, [], [], 0))[0]
    dl = unit.get("deliverables")
    if dl is not None and dl != NM:
        fixed = re.match(r"^(\d+)/(fixed-at-open|fixed-after-the-fact)/list=\S+$", dl)
        if not fixed and dl != "not-yet-fixed/at=station-1-SPEC":
            bad.append(("deliverables-not-one-of-the-three-legal-forms",
                        "%s:%s" % (b["id"], dl)))
        if not fixed and status in ("VERIFIED", "REJECTED"):
            bad.append(("resolved-batch-with-no-fixed-deliverable-list",
                        "%s:%s" % (b["id"], dl)))

    mach = labels.get("machine", ({}, [], [], 0))[0]
    rm, rs = mach.get("runnerMinutes"), mach.get("runnerSteps")
    if rm not in (None, NM) and not re.match(
            r"^\d+\.\d+/sum-of-timed-steps/over=\S+$", rm or ""):
        bad.append(("runnerMinutes-not-a-sum-with-its-coverage",
                    "%s:%s" % (b["id"], rm)))
    if (rm == NM) != (rs == NM):
        bad.append(("machine-pair-half-measured",
                    "%s:minutes=%s/steps=%s" % (b["id"], rm, rs)))

    wear = labels.get("wear", ({}, [], [], 0))[0]
    wn, wmin = wear.get("wearCoverageN"), wear.get("wearCoverageMin")
    if wn is not None and wn != NM:
        n, d, ok = count_pair(wn)
        if not ok:
            bad.append(("wearCoverageN-not-a-count-with-a-denominator",
                        "%s:%s" % (b["id"], wn)))
    # D53 point 2: the surface at the minimum is NAMED, because a median
    # cannot see the one clean wall. And a baked-in wear prints the words,
    # never a zero, so the pair moves together or not at all.
    if (wn == NM) != (wmin == NM):
        bad.append(("wear-pair-half-measured",
                    "%s:N=%s/min=%s" % (b["id"], wn, wmin)))
    if wmin not in (None, NM) and "/" not in (wmin or ""):
        bad.append(("wearCoverageMin-does-not-name-its-surface",
                    "%s:%s" % (b["id"], wmin)))
    return bad


def priced(b):
    """(metCount, unmet) against queue 369's four conditions. A number, not an
    opinion: last-wins on the block as written."""
    labels = b["labels"]
    head = labels.get("batch", ({}, [], [], 0))[0]
    att = labels.get("attempts", ({}, [], [], 0))[0]
    before = labels.get("before", ({}, [], [], 0))[0]
    after = labels.get("after", ({}, [], [], 0))[0]
    unmet = []
    if head.get("status") not in ("VERIFIED", "REJECTED"):
        unmet.append("not-end-to-end")
    if att.get("attemptsRejected", NM) == NM:
        unmet.append("rejections-not-counted")
    reads = [before.get("meterTotalPct"), before.get("meterFablePct"),
             after.get("meterTotalPct"), after.get("meterFablePct")]
    if any(r in (None, NM) for r in reads):
        unmet.append("both-meters-not-read-both-ends")
    if after.get("cleanWindow") != "yes":
        unmet.append("window-not-stated-clean")
    return 4 - len(unmet), unmet


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def check(path=None, series_only=False):
    path = path or LEDGER
    rel = os.path.relpath(path, REPO) if path.startswith(REPO) else path
    out = []
    text = read(path)
    if text is None:
        out.append("THROUGHPUT: %s does not exist, so this run measured "
                   "%s" % (rel, NOTHING))
        return 2, out
    blocks, table_rows, _ = parse(text)
    defs_missing = [name for name, phrase in DEFINITIONS if phrase not in text]

    if not blocks:
        out.append("THROUGHPUT: %s carries no batch block, so this run walked "
                   "0 batches and measured %s. It is not a clean ledger and "
                   "it is not zero rejections." % (rel, NOTHING))
        out.append("throughput done: batchesWalked=0 definitionsMissing=%d/of=%d "
                   "verdict=%s" % (len(defs_missing), len(DEFINITIONS),
                                   NM))
        return 2, out

    bad = []
    for name in defs_missing:
        bad.append(("definition-sentence-missing", "%s:%s" % (rel, name)))
    for ln in table_rows:
        # A5, and the reason is in the docstring: the dashboard sums cell 3
        # of every four-cell pipe row whose first cell is the current week.
        bad.append(("batch-section-carries-a-pipe-table-row",
                    "%s:line=%d" % (rel, ln)))

    priced_n = fixed_at_open = 0
    rej_total = att_total = counting = 0
    for b in blocks:
        blk_bad = audit_block(b)
        bad.extend(blk_bad)
        met, unmet = priced(b)
        if met == 4:
            priced_n += 1
        head = b["labels"].get("batch", ({}, [], [], 0))[0]
        if "/fixed-at-open/" in b["labels"].get(
                "unit", ({}, [], [], 0))[0].get("deliverables", ""):
            fixed_at_open += 1
        att = b["labels"].get("attempts", ({}, [], [], 0))[0]
        n, d, ok = count_pair(att.get("attemptsRejected", NM))
        if ok and n is not None:
            counting += 1
            rej_total += n
            att_total += d
        if not series_only:
            continue
        # PER-BATCH NUMBERS ON THE BATCH LINE. Whole-file numbers are on the
        # done line below and nowhere else.
        out.append("batch %s line=%s status=%s rejected=%s attempts=%s "
                   "pricedConditionsMet=%d/of=4 unmet=%s runnerMinutes=%s "
                   "wearCoverageN=%s wearCoverageMin=%s shapeViolations=%d"
                   % (b["id"], head.get("line", NM), head.get("status", NM),
                      att.get("attemptsRejected", NM),
                      att.get("attemptsMade", NM), met, cap(unmet),
                      b["labels"].get("machine", ({}, [], [], 0))[0]
                      .get("runnerMinutes", NM),
                      b["labels"].get("wear", ({}, [], [], 0))[0]
                      .get("wearCoverageN", NM),
                      b["labels"].get("wear", ({}, [], [], 0))[0]
                      .get("wearCoverageMin", NM), len(blk_bad)))

    if bad:
        out.append("THROUGHPUT: %d violation(s) over %d batch block(s) in %s"
                   % (len(bad), len(blocks), rel))
        for code, detail in bad[:20]:
            out.append("  %s %s" % (code, detail))
        if len(bad) > 20:
            out.append("  (+%d-more-not-shown)" % (len(bad) - 20))

    # THE DONE LINE, whole-file numbers only, each zero with its denominator.
    # rejectedCumulative is a SUM over the batches that counted at all; the
    # batches that counted nothing are the denominator beside it, never
    # folded in as zeros.
    out.append("throughput done: batchesWalked=%d batchesPriced=%d/of=%d "
               "rejectedCumulative=%s attemptsCumulative=%s "
               "batchesCountingRejections=%d/of=%d deliverableListsFixedAtOpen=%d/of=%d "
               "definitionsMissing=%d/of=%d violations=%d seriesPoints=%d"
               % (len(blocks), priced_n, len(blocks),
                  ("%d" % rej_total) if counting else NM,
                  ("%d" % att_total) if counting else NM,
                  counting, len(blocks), fixed_at_open, len(blocks),
                  len(defs_missing), len(DEFINITIONS),
                  len(bad), len(blocks)))
    if series_only:
        out.append("NO BOUND IS SET HERE and none may be read off this run: a "
                   "bound needs a printed series over real batches, and this "
                   "is the printer. seriesPoints=%d priced=%d."
                   % (len(blocks), priced_n))
    return (1 if bad else 0), out


def series(path=None):
    return check(path, series_only=True)


# ----------------------------------------------------------------- selftest

FIX_OK = """# Throughput ledger

A piece counts when it passes station 3 (VERIFY) and lands at station 4
(INTEGRATE). Partial work counts zero.

| week | line | pieces verified | notes |
|---|---|---|---|
| 2026-W36 | dialogue bank | 1 (pub-regular-v1) | a piece row, untouched |

## The BATCH unit

A batch counts when every deliverable on its list crosses station 4.
An attempt counts as REJECTED when a station or a named judge refuses it.

### BATCH b901-synthetic-open

batch: batchId=b901-synthetic-open line=art/synthetic status=OPEN
  opened=2026-09-21T19:00:00Z closed=not-yet
unit: deliverables=1/fixed-at-open/list=production/art/none.md
  deliverableUnit=glb-mesh-asset
attempts: attemptsMade=0-cumulative attemptsRejected=0/of=0-attempts-so-far
  rejectedAtStation=none/of=0-attempts-so-far
before: meterTakenAt=2026-09-21T16:2xZ meterTotalPct=13 meterFablePct=17
  meterSource=production/budget.md#row-2026-09-21b
  sessionsTakenAt=2026-09-21T19:00:00Z
  sessionsCumulative=745/src=.claude/agent-log.tsv sha=0f1b8fa4
after: meterTakenAt=nothing-measured meterTotalPct=nothing-measured
  meterFablePct=nothing-measured meterSource=nothing-measured
  sessionsTakenAt=nothing-measured sessionsCumulative=nothing-measured
  sha=nothing-measured
  cleanWindow=not-stated
machine: runnerMinutes=nothing-measured runnerSteps=nothing-measured
wear: wearCoverageN=nothing-measured wearCoverageMin=nothing-measured

Prose about the batch goes here and is not parsed.
"""


def _write(d, text, name="throughput.md"):
    p = os.path.join(d, name)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    return p


def selftest():
    ok = fail = 0

    def c(name, cond, detail=""):
        nonlocal ok, fail
        if cond:
            ok += 1
            print("  ok   %s" % name)
        else:
            fail += 1
            print("  FAIL %s %s" % (name, detail))

    print("throughput-check selftest - accepting case first, and it is the "
          "live ledger")
    # ACCEPTING CASE FIRST, AND IT IS THE LIVE TREE. No constant here was
    # read off production/throughput.md: the assertions are about SHAPE, so
    # the day a batch lands or a count moves, this case still passes. That is
    # queue 416's fault class and it is not repeated here.
    code, out = check()
    text = "\n".join(out)
    c("ACCEPTING: the live ledger passes the batch-row shape (exit 0)",
      code == 0, "exit %d:\n%s" % (code, text))
    c("ACCEPTING: the done line ships every zero's denominator",
      all(k in text for k in ("batchesWalked=", "batchesPriced=",
                              "batchesCountingRejections=",
                              "definitionsMissing=", "seriesPoints=")),
      text.splitlines()[-1] if out else "(no output)")
    code, out = series()
    stext = "\n".join(out)
    c("ACCEPTING: --series prints a line per batch and sets no bound",
      code == 0 and "batch " in stext and "NO BOUND IS SET HERE" in stext,
      "exit %d:\n%s" % (code, stext))

    import tempfile
    with tempfile.TemporaryDirectory() as d:
        # ACCEPTING, synthetic: the minimal well-formed shape.
        p = _write(d, FIX_OK)
        code, out = check(p)
        c("ACCEPTING: a minimal well-formed synthetic ledger passes",
          code == 0, "exit %d:\n%s" % (code, "\n".join(out)))

        # REJECTING FIXTURES, every one SYNTHETIC: b9xx exists in no ledger,
        # so doing the work this tool prompts can never break the tool.
        cases = [
            ("a bare zero with no denominator is refused",
             "attemptsRejected=0/of=0-attempts-so-far",
             "attemptsRejected=0", "bare-zero-no-denominator"),
            ("a rejection count nobody can read is refused",
             "attemptsRejected=0/of=0-attempts-so-far",
             "attemptsRejected=some",
             "attemptsRejected-not-a-count-with-a-denominator"),
            ("more rejected than attempted is refused",
             "attemptsMade=0-cumulative attemptsRejected=0/of=0-attempts-so-far",
             "attemptsMade=2-cumulative attemptsRejected=3/of=2-attempts",
             "more-rejected-than-attempted"),
            ("a resolved batch with no close instant is refused",
             "status=OPEN", "status=VERIFIED",
             "resolved-batch-with-no-close-instant"),
            ("a value with a space is refused as a stray token",
             "meterSource=production/budget.md#row-2026-09-21b",
             "meterSource=production/budget.md row 2026-09-21b",
             "stray-token-or-value-with-a-space"),
            ("half a wear pair is refused, because a baked surface prints "
             "the words for BOTH",
             "wearCoverageN=nothing-measured wearCoverageMin=nothing-measured",
             "wearCoverageN=1/of=1-surfaces wearCoverageMin=nothing-measured",
             "wear-pair-half-measured"),
            ("a wear minimum that names no surface is refused",
             "wearCoverageN=nothing-measured wearCoverageMin=nothing-measured",
             "wearCoverageN=1/of=1-surfaces wearCoverageMin=0.41",
             "wearCoverageMin-does-not-name-its-surface"),
            ("a missing reading line is refused",
             "wear: wearCoverageN=nothing-measured "
             "wearCoverageMin=nothing-measured", "", "missing-line"),
            ("a runner-minute figure with no coverage is refused",
             "runnerMinutes=nothing-measured runnerSteps=nothing-measured",
             "runnerMinutes=4.92 runnerSteps=meshEditorBuild+propImport",
             "runnerMinutes-not-a-sum-with-its-coverage"),
            ("half a machine pair is refused",
             "runnerMinutes=nothing-measured runnerSteps=nothing-measured",
             "runnerMinutes=4.92/sum-of-timed-steps/over=3-verdicts-of-4-runs "
             "runnerSteps=nothing-measured",
             "machine-pair-half-measured"),
            ("a deliverable list in no legal form is refused",
             "deliverables=1/fixed-at-open/list=production/art/none.md",
             "deliverables=about-one", 
             "deliverables-not-one-of-the-three-legal-forms"),
            ("the batch-unit definition edited away is refused",
             "A batch counts when", "A batch used to count when",
             "definition-sentence-missing"),
        ]
        for name, old, new, code_word in cases:
            p = _write(d, FIX_OK.replace(old, new))
            rc, rout = check(p)
            t = "\n".join(rout)
            c("rejecting: " + name,
              rc == 1 and code_word in t, "exit %d:\n%s" % (rc, t))

        # A RESOLVED BATCH WHOSE DENOMINATOR WAS NEVER FIXED: two edits, so
        # the fixture differs from the accepting one in exactly the pair that
        # matters, the status and the list.
        p = _write(d, FIX_OK
                   .replace("status=OPEN\n  opened", "status=VERIFIED\n  opened")
                   .replace("closed=not-yet", "closed=2026-09-22T09:00:00Z")
                   .replace("deliverables=1/fixed-at-open/list=production/art/none.md",
                            "deliverables=not-yet-fixed/at=station-1-SPEC"))
        rc, rout = check(p)
        c("rejecting: a resolved batch whose deliverable list was never fixed",
          rc == 1 and "resolved-batch-with-no-fixed-deliverable-list"
          in "\n".join(rout), "exit %d:\n%s" % (rc, "\n".join(rout)))

        # THE DASHBOARD HAZARD, and it is measured rather than feared: a batch
        # written as a pipe row is summed as verified pieces by
        # tools/dashboard/build-dashboard.py:1216.
        p = _write(d, FIX_OK.replace(
            "### BATCH b901-synthetic-open",
            "| 2026-W38 | art | 9 | a batch smuggled in as a piece row |\n\n"
            "### BATCH b901-synthetic-open"))
        rc, rout = check(p)
        c("rejecting: a pipe-table row inside the batch section is refused",
          rc == 1 and "batch-section-carries-a-pipe-table-row"
          in "\n".join(rout), "exit %d" % rc)

        # AND THE SAME LEDGER PASSES WHEN THE FAULT IS REMOVED: a guard that
        # cannot tell a regression from an improvement is a ratchet.
        p = _write(d, FIX_OK.replace("attemptsRejected=0/of=0-attempts-so-far",
                                     "attemptsRejected=2/of=5-attempts")
                   .replace("attemptsMade=0-cumulative",
                            "attemptsMade=5-cumulative")
                   .replace("rejectedAtStation=none/of=0-attempts-so-far",
                            "rejectedAtStation=3-VERIFY/of=5-attempts"))
        rc, rout = check(p)
        c("ACCEPTING: a real rejection count on the same ledger passes",
          rc == 0, "exit %d:\n%s" % (rc, "\n".join(rout)))

        # NOTHING MEASURED IS NOT CLEAN, both halves, and both are exit 2.
        p = _write(d, FIX_OK.split("## The BATCH unit")[0])
        rc, rout = check(p)
        t = "\n".join(rout)
        c("rejecting: a ledger with no batch block is exit 2 and prints the "
          "words", rc == 2 and NOTHING in t, "exit %d:\n%s" % (rc, t))
        rc, rout = check(os.path.join(d, "gone.md"))
        c("rejecting: a missing ledger is exit 2, never a pass",
          rc == 2 and NOTHING in "\n".join(rout), "exit %d" % rc)

        # THE CAP ANNOUNCES WHEN IT BITES.
        c("the cap says how much it hid",
          cap([str(i) for i in range(20)], n=3) == "0,1,2,(+17-more-not-shown)",
          cap([str(i) for i in range(20)], n=3))
        c("and an empty list reads as none, not as a silent blank",
          cap([]) == "none")

    print("throughput-check selftest: %d passed, %d failed" % (ok, fail))
    return 3 if fail else 0


if __name__ == "__main__":
    # FAIL READABLE: `--series | head` is how anybody reads this, and a
    # correct run ending in a BrokenPipeError costs twenty minutes before
    # somebody notices it worked.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--series" in sys.argv:
        rc, lines = series()
    else:
        rc, lines = check()
    for line in lines:
        print(line)
    sys.exit(rc)
