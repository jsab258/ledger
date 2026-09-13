#!/usr/bin/env python3
"""THE BUDGET LOG JAFAR READS BACK, WITH ITS OWN DENOMINATOR, AND THE NINETY
FIXTURE ROWS MARKED RATHER THAN DELETED.

    python3 tools/budget-log-mark.py              # read it back, census only
    python3 tools/budget-log-mark.py --mark       # mark the fixture rows
    python3 tools/budget-log-mark.py --log PATH   # another copy (the PC's)
    python3 tools/budget-log-mark.py --selftest   # both outcomes, accepting first

WHAT WENT WRONG, MEASURED (queue 267). `production/logs/telegram-budget.log`
is the file `log_budget` describes as "written where Jafar can read it back
without the bot running". On 2026-09-13 it held 90 rows, 0 of them readings he
had typed: three selftest fixtures drove the real handler, thirty verify runs
wrote the same three rows, and nothing in any row said fixture. The values are
worse than plausible: a flat 40 on the total meter, a Fable meter stepping 62
to 77, and sixty rows closing on `headroomPct=3`, which reads as a studio
sitting three points off its ceiling. The writing is fixed at 0e522c1f
(`log_budget` takes its repository from the caller); THESE ROWS ARE EVIDENCE
OF THE FAULT AND OF THIRTY VERIFY RUNS, so they are marked and never deleted.

WHY A TOOL AND NOT A COMMIT. The log is gitignored (`.gitignore:96`), so the
rows cannot travel in a diff: the method ships instead. The accepting case is
THIS CONTAINER'S COPY, ruled 2026-09-13, because the same thirty verify runs
wrote the same ninety rows here; the PC's copy is marked by this same tool
when the runner returns, and that run is the second accepting case.

WHAT THE ROWS KEEP. The timestamp and every measured value (`budgetTotalPct`,
`budgetFablePct`, `governing`, `governingPct`, `ceilingPct`, `headroomPct`) are
byte-identical after marking, and this tool CHECKS that rather than promising
it: a fixture row that quietly acquired today's ceiling would be a second
falsification on top of the first. What changes is `source=typed`, which was
never true of a row nobody typed, and one appended `markedBy=` naming this
tool and the queue item.

NO HEADER LINE IS WRITTEN, though queue 267 allowed one. `budget_log_lines` in
tools/runner/telegram-bot.py counts LINES and calls them rows, and the bot's
own case compares that count before and after its suite; a header would make
90 rows read as 91 in an instrument that is right today. The mark goes in every
row instead, which is also the stronger fix: the fault was that nothing IN the
line said fixture.

HOW A FIXTURE ROW IS RECOGNISED, AND THE BOUND CAME FROM THE PRINTED SERIES.
Not "every row without `ceilingFrom=`": a row Jafar typed on his PC before
0e522c1f carries no such key either, and marking one of his readings as a
fixture would be this fault committed a second time in the opposite direction.
A fixture GROUP is three consecutive unmarked rows whose meter pairs are
exactly 40/62, 40/77, 40/77 in that order, none of them carrying
`ceilingFrom=`, and spanning no more than BURST_SPAN_MAX_S seconds. Measured
over this container's 90 rows before any bound was chosen: 30 groups, every
one of them that exact shape, intra-group span peak 2s and median 1s, and the
smallest gap BETWEEN groups 22s (median 726s, peak 49902s). The bound sits at
5s, above the peak of what it must catch and well below the minimum of what it
must not. Anything this rule cannot place stays UNMARKED and is counted as
unmarked, never guessed at.

EXIT CODES, distinct per outcome. 0 the log was read or marked. 2 NOTHING
MEASURED: the log is not there, which is a fresh checkout or a bot nobody has
answered yet and is not an empty log. 3 the selftest failed. 4 marking would
have moved a measured value, so nothing was written and the backup stands.
"""
import argparse
import datetime
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG_REL = "production/logs/telegram-budget.log"

# THE THREE FIXTURES, IN THE ORDER THE SUITE DRIVES THEM (telegram-bot.py's
# b4, b4b and b8 cases). The shape is the signature; a single 40/62 row on its
# own is not one and is left alone.
FIXTURE_GROUP = (("40", "62"), ("40", "77"), ("40", "77"))
# SECONDS. The series this came from is in the docstring above: intra-group
# peak 2, inter-group minimum 22. A bound between them, named, never guessed.
BURST_SPAN_MAX_S = 5
MARK_SOURCE = "source=selftest-fixture"
MARK_BY = "markedBy=queue267/tools/budget-log-mark.py"
MEASURED_KEYS = ("budgetTotalPct", "budgetFablePct", "governing",
                 "governingPct", "ceilingPct", "headroomPct")
# Rows listed in a failure before the cap bites, and it announces itself.
ROWS_SHOWN = 3


def parse_row(line):
    """(when, keys, text) for one log line, or None if it is not a row.

    A LINE THAT DOES NOT PARSE IS NOT SILENTLY A ROW AND NOT SILENTLY GONE:
    the caller counts it under `unparsed`, with its own denominator, because a
    file half of which this tool cannot read is a different fact from a clean
    one."""
    text = line.rstrip("\n")
    if not text.strip():
        return None
    head, _sep, rest = text.partition(" ")
    try:
        when = datetime.datetime.fromisoformat(head)
    except ValueError:
        return None
    keys = dict(p.split("=", 1) for p in rest.split() if "=" in p)
    if not keys:
        return None
    return when, keys, text


def classify(rows):
    """[(index, class)] over parsed rows, and the three classes PARTITION the
    rows by construction so `rows == readings + fixtures + unmarked` is an
    identity rather than a hope.

      fixture   marked by this tool, or a member of a matched fixture group
      reading   carries `ceilingFrom=`, which only a bot running 0e522c1f or
                later writes, and the fixtures cannot write it any more
      unmarked  everything else: provenance unknown, and saying so is the
                whole point of this file

    LAST-WINS IS NOT A STATISTIC HERE: every class is a CUMULATIVE count over
    one pass of the file.
    """
    out = ["unmarked"] * len(rows)
    for i, (_when, keys, _text) in enumerate(rows):
        if keys.get("source") == "selftest-fixture" or "markedBy" in keys:
            out[i] = "fixture"
        elif "ceilingFrom" in keys:
            out[i] = "reading"
    n = len(FIXTURE_GROUP)
    for i in range(0, len(rows) - n + 1):
        window = rows[i:i + n]
        if any(out[i + j] != "unmarked" for j in range(n)):
            continue
        if any("ceilingFrom" in k for _w, k, _t in window):
            continue
        shape = tuple((k.get("budgetTotalPct"), k.get("budgetFablePct"))
                      for _w, k, _t in window)
        if shape != FIXTURE_GROUP:
            continue
        span = (window[-1][0] - window[0][0]).total_seconds()
        if span < 0 or span > BURST_SPAN_MAX_S:
            continue
        for j in range(n):
            out[i + j] = "fixture"
    return out


def group_spans(rows, classes):
    """[(span, index)] of the fixture groups, so the PEAK intra-group span can
    be printed beside the bound it was measured against rather than asserted.
    The span is a statistic OF the groups this pass found: peak, not median.

    THE WALK CONSUMES A GROUP IT MATCHES AND DOES NOT SLIDE THROUGH IT. The
    first version slid one row at a time, so six consecutive fixture rows from
    two verify runs reported FOUR groups and a peak span of 86579 seconds,
    which is the gap between two runs read as the length of one. The census
    was right and the group counter was wrong, which is the instrument fault
    to suspect first: 6 fixture rows and 4 groups of 3 cannot both be true.
    """
    spans, n, i = [], len(FIXTURE_GROUP), 0
    while i <= len(rows) - n:
        if all(classes[i + j] == "fixture" for j in range(n)):
            spans.append(((rows[i + n - 1][0] - rows[i][0]).total_seconds(), i))
            i += n
        else:
            i += 1
    return spans


def census(lines):
    """The whole read-back, as numbers. PURE: lines in, dict out, so the
    arithmetic and the strings below are exercised by planted fixtures and not
    only by one live file that is right today."""
    parsed, unparsed = [], 0
    for line in lines:
        row = parse_row(line)
        if row is None:
            unparsed += 1 if line.strip() else 0
        else:
            parsed.append(row)
    classes = classify(parsed)
    spans = [s for s, _i in group_spans(parsed, classes)]
    newest = {"reading": None, "fixture": None}
    for (when, _k, _t), cls in zip(parsed, classes):
        if cls in newest and (newest[cls] is None or when > newest[cls]):
            newest[cls] = when
    return {
        "lines": len(lines),
        "rows": len(parsed),
        "blank": sum(1 for l in lines if not l.strip()),
        "unparsed": unparsed,
        "readings": classes.count("reading"),
        "fixtures": classes.count("fixture"),
        "unmarked": classes.count("unmarked"),
        "groups": len(spans),
        "spanPeak": max(spans) if spans else None,
        "newestReading": newest["reading"],
        "newestFixture": newest["fixture"],
        "classes": classes,
        "parsed": parsed,
    }


def read_line(c, rel, state):
    """The read-back's one machine line, whole-file numbers only.

    EVERY ZERO SHIPS ITS DENOMINATOR, which is this item's point 4: "0
    readings" beside 90 rows is a measurement, "0 readings" on its own is the
    same string a fresh checkout would print. A file that is not there says
    NOTHING MEASURED and never zero."""
    if state == "absent":
        return ("budget-log: NOTHING MEASURED log=%s state=absent "
                "rows=nothing-measured readings=nothing-measured "
                "fixtures=nothing-measured unmarked=nothing-measured "
                "why=the-file-does-not-exist,-which-is-a-fresh-checkout-or-a-"
                "bot-nobody-has-answered" % rel)
    rows = c["rows"]
    return ("budget-log: READ log=%s state=present lines=%d rows=%d "
            "readings=%d/%d-rows fixtures=%d/%d-rows unmarked=%d/%d-rows "
            "unparsed=%d/%d-lines blank=%d/%d-lines "
            "newestReading=%s newestFixture=%s"
            % (rel, c["lines"], rows, c["readings"], rows, c["fixtures"], rows,
               c["unmarked"], rows, c["unparsed"], c["lines"], c["blank"],
               c["lines"],
               c["newestReading"].isoformat() if c["newestReading"]
               else "nothing-measured",
               c["newestFixture"].isoformat() if c["newestFixture"]
               else "nothing-measured"))


def mark_row(text, when):
    """One row's marked form. `source=typed` was never true of a row nobody
    typed, so it is the key that changes; everything measured is left where it
    was. `when` is the marking date, not the row's: the row's own timestamp is
    the first field and is untouched."""
    if "source=typed" in text:
        out = text.replace("source=typed", MARK_SOURCE)
    elif MARK_SOURCE not in text:
        out = text + " " + MARK_SOURCE
    else:
        out = text
    return "%s %s markedOn=%s" % (out, MARK_BY, when)


def measured_values(row):
    """The tuple that must not move: the timestamp and every measured key.
    Missing keys are carried as None rather than dropped, so a key that
    DISAPPEARED is a difference and not an invisible one."""
    when, keys, _text = row
    return (when.isoformat(),) + tuple(keys.get(k) for k in MEASURED_KEYS)


def mark_lines(lines):
    """(out_lines, before, after, moved). PURE, and it checks its own effect:
    `moved` is every row whose measured values differ before and after, which
    is what stops this tool from becoming the second falsification."""
    before = census(lines)
    out, k = [], 0
    for line in lines:
        row = parse_row(line)
        if row is None:
            out.append(line)
            continue
        cls = before["classes"][k]
        k += 1
        if cls == "fixture" and MARK_BY not in line:
            out.append(mark_row(row[2],
                                datetime.date.today().isoformat()) + "\n")
        else:
            out.append(line)
    after = census(out)
    moved = []
    for i, (b, a) in enumerate(zip(before["parsed"], after["parsed"])):
        if measured_values(b) != measured_values(a):
            moved.append((i, measured_values(b), measured_values(a)))
    return out, before, after, moved


def mark_line(before, after, moved, marked_now, rel, backup):
    """The marking run's one machine line. Before and after ride together on
    it as a pair: two keys a reader has to remember the relationship between
    are two readings, and this is one."""
    return ("budget-log-mark: %s log=%s rowsBefore=%d rowsAfter=%d "
            "markedNow=%d/%d-rows fixtures=%d..%d-rows-before..after "
            "readings=%d..%d-rows-before..after "
            "unmarked=%d..%d-rows-before..after groupsMatched=%d "
            "groupShape=40/62..40/77..40/77 spanPeakS=%s/%d-bound "
            "valuesMoved=%d/%d-rows-compared backup=%s"
            % ("MARKED" if not moved else "REFUSED", rel, before["rows"],
               after["rows"], marked_now, before["rows"], before["fixtures"],
               after["fixtures"], before["readings"], after["readings"],
               before["unmarked"], after["unmarked"], after["groups"],
               ("%g" % before["spanPeak"]) if before["spanPeak"] is not None
               else "nothing-measured", BURST_SPAN_MAX_S, len(moved),
               before["rows"], backup))


def read_log(path):
    """(lines, state). A missing file is "absent" and never an empty list
    pretending to be an empty log."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.readlines(), "present"
    except OSError:
        return [], "absent"


def rel_to_repo(path):
    """A path as a value with no spaces in it, repository-relative when it is
    inside this repository."""
    try:
        return str(pathlib.Path(path).resolve().relative_to(ROOT)).replace(
            "\\", "/")
    except ValueError:
        return str(path).replace(" ", "-")


def do_read(path):
    lines, state = read_log(path)
    c = census(lines)
    rel = rel_to_repo(path)
    if state == "present":
        print("budget-log: %s, read back and classified by what each row "
              "carries" % rel)
        print("  %d row(s): %d reading(s) Jafar typed, %d fixture row(s) from "
              "the selftest, %d whose provenance this tool will not guess at"
              % (c["rows"], c["readings"], c["fixtures"], c["unmarked"]))
    print(read_line(c, rel, state))
    return 0 if state == "present" else 2


def do_mark(path, backup=True):
    lines, state = read_log(path)
    rel = rel_to_repo(path)
    if state == "absent":
        print(read_line(census(lines), rel, state))
        return 2
    out, before, after, moved = mark_lines(lines)
    marked_now = sum(1 for a, b in zip(out, lines) if a != b)
    # LOOK BEFORE YOU DESTROY (CLAUDE.md rule 5): the copy is taken before a
    # byte is written, it sits beside the log inside the gitignored directory,
    # and its name is printed on the done line so the reader does not have to
    # find it.
    #
    # THE SUFFIX STAYS `.log` AND THAT IS NOT COSMETIC. The first version
    # wrote `telegram-budget.log.premark-20260913T032423`, whose file KIND is
    # `.premark-20260913T032423`, and `ledger/verify.py`'s attribution check
    # went red with "1 unclassified of 5647 walked" naming it. An instrument
    # that turns the commit gate red by taking its own backup is a fault in
    # the instrument, found by running it (rule 3: suspect the instrument).
    bpath = "%s.premark-%s.log" % (
        path[:-4] if path.endswith(".log") else path,
        datetime.datetime.now().strftime("%Y%m%dT%H%M%S"))
    if backup:
        shutil.copy2(path, bpath)
    if moved:
        print("budget-log-mark: REFUSED to write. %d row(s) would have had a "
              "measured value moved, and a fixture row that quietly acquired "
              "today's ceiling would be a second falsification on top of the "
              "first." % len(moved))
        for i, b, a in moved[:ROWS_SHOWN]:
            print("  row %d: %s -> %s" % (i + 1, b, a))
        if len(moved) > ROWS_SHOWN:
            print("  (+%d more not shown)" % (len(moved) - ROWS_SHOWN))
        print(mark_line(before, after, moved, 0, rel,
                        rel_to_repo(bpath) if backup else "not-taken"))
        return 4
    print("budget-log: BEFORE")
    print("  " + read_line(before, rel, "present"))
    with open(path, "w", encoding="utf-8") as fh:
        fh.writelines(out)
    lines_after, _state = read_log(path)
    reread = census(lines_after)
    print("budget-log: AFTER, re-read off the disk rather than from memory")
    print("  " + read_line(reread, rel, "present"))
    print(mark_line(before, reread, moved, marked_now, rel,
                    rel_to_repo(bpath) if backup else "not-taken"))
    return 0


# ------------------------------------------------------------------ selftest
_FX_KEYS = ("governing=fable governingPct=%s ceilingPct=80 headroomPct=%s "
            "source=typed")


def _row(when, total, fable, extra=""):
    head = ("%s budgetTotalPct=%s budgetFablePct=%s "
            % (when, total, fable)) + (_FX_KEYS % (fable, 80 - int(fable)))
    return head + (" " + extra if extra else "") + "\n"


def _fixture_run(day, second):
    """One verify run's three rows, the shape measured off this container's
    ninety: 40/62 then 40/77 twice, one second apart."""
    return [_row("2026-09-%02dT19:%02d:0%d" % (day, second, i), "40",
                 "62" if i == 0 else "77") for i in range(3)]


def selftest():
    print("budget-log-mark --selftest: ACCEPTING CASE FIRST, and the first "
          "one is this container's live log, read and never written\n")
    import tempfile
    ok, bad = [], []

    def check(name, cond, detail=""):
        (ok if cond else bad).append(name)
        print("  %-52s %s%s" % (name, "pass" if cond else "FAIL",
                                (" : " + detail) if not cond else ""))

    live = ROOT / LOG_REL
    live_lines_before, live_state_before = read_log(live)
    c_live = census(live_lines_before)
    print("      live: " + read_line(c_live, LOG_REL, live_state_before))
    check("accept/the-live-log-reads-back-with-its-denominator",
          c_live["rows"] == (c_live["readings"] + c_live["fixtures"]
                             + c_live["unmarked"]),
          "rows=%d against readings=%d + fixtures=%d + unmarked=%d, which "
          "must partition" % (c_live["rows"], c_live["readings"],
                              c_live["fixtures"], c_live["unmarked"]))
    check("accept/an-absent-log-says-nothing-measured-and-never-zero",
          "NOTHING MEASURED" in read_line(census([]), LOG_REL, "absent")
          and "rows=nothing-measured" in read_line(census([]), LOG_REL,
                                                   "absent"),
          read_line(census([]), LOG_REL, "absent"))

    with tempfile.TemporaryDirectory() as tmp:
        # ONE PLANTED LOG CARRYING ALL FOUR SHAPES AT ONCE, because that is
        # the file this tool will actually meet on the PC: two verify runs,
        # one reading Jafar typed since the fix, one pre-fix row that is NOT a
        # fixture, and three matching rows spread over two minutes.
        p = pathlib.Path(tmp) / "telegram-budget.log"
        planted = (_fixture_run(10, 11) + _fixture_run(11, 14)
                   + [_row("2026-09-12T08:00:00", "78", "82",
                           "ceilingFrom=production/budget.md:49..the-standing-line")]
                   + [_row("2026-09-12T09:00:00", "40", "62")]
                   + [_row("2026-09-12T10:0%d:00" % i, "40",
                           "62" if i == 0 else "77") for i in range(3)])
        p.write_text("".join(planted), encoding="utf-8")
        c0 = census(p.read_text(encoding="utf-8").splitlines(True))
        print("      planted: " + read_line(c0, "fixture/planted.log",
                                            "present"))
        check("accept/a-fixture-group-is-recognised-before-anything-is-written",
              c0["fixtures"] == 6 and c0["groups"] == 2,
              "fixtures=%d groups=%d, wanted 6 rows in 2 group(s)"
              % (c0["fixtures"], c0["groups"]))
        check("accept/a-reading-with-ceilingFrom-is-a-reading",
              c0["readings"] == 1, "readings=%d/%d-rows"
              % (c0["readings"], c0["rows"]))
        check("reject/a-lone-pre-fix-row-is-not-guessed-at",
              c0["unmarked"] == 4,
              "unmarked=%d, wanted the lone 40/62 row plus the three spread "
              "over two minutes" % c0["unmarked"])
        check("reject/three-matching-rows-two-minutes-apart-are-not-a-group",
              c0["groups"] == 2 and c0["unmarked"] >= 3,
              "groups=%d unmarked=%d, and the bound is %ds"
              % (c0["groups"], c0["unmarked"], BURST_SPAN_MAX_S))
        rc = do_mark(str(p), backup=False)
        after = census(p.read_text(encoding="utf-8").splitlines(True))
        check("accept/marking-marks-every-fixture-row-and-only-those",
              rc == 0 and after["fixtures"] == 6 and after["readings"] == 1
              and after["unmarked"] == 4,
              "exit=%d fixtures=%d readings=%d unmarked=%d"
              % (rc, after["fixtures"], after["readings"], after["unmarked"]))
        check("accept/marking-moves-no-measured-value-and-no-row-count",
              after["rows"] == c0["rows"]
              and [measured_values(r) for r in after["parsed"]]
              == [measured_values(r) for r in c0["parsed"]],
              "rowsBefore=%d rowsAfter=%d" % (c0["rows"], after["rows"]))
        marked_text = p.read_text(encoding="utf-8").splitlines()[0]
        check("accept/the-mark-is-in-the-row-itself",
              MARK_SOURCE in marked_text and MARK_BY in marked_text
              and "source=typed" not in marked_text
              and "ceilingPct=80" in marked_text, marked_text)
        check("reject/the-reading-row-is-untouched-by-marking",
              [l for l in p.read_text(encoding="utf-8").splitlines()
               if "ceilingFrom=" in l][0] == planted[6].rstrip("\n"),
              "the row Jafar typed must come back byte for byte")
        rc2 = do_mark(str(p), backup=False)
        again = census(p.read_text(encoding="utf-8").splitlines(True))
        check("accept/marking-twice-marks-nothing-the-second-time",
              rc2 == 0 and again["fixtures"] == after["fixtures"]
              and p.read_text(encoding="utf-8").count(MARK_BY) == 6,
              "fixtures=%d markers=%d"
              % (again["fixtures"],
                 p.read_text(encoding="utf-8").count(MARK_BY)))
        # THE OTHER DIRECTION OF POINT 3: a value that moved must REFUSE the
        # write, or the check is decoration. The condition is planted rather
        # than waited for.
        broken = list(planted)
        broken[0] = broken[0].replace("ceilingPct=80", "ceilingPct=85")
        c_b = census(broken)
        moved_probe = [i for i, (b, a) in
                       enumerate(zip(census(planted)["parsed"],
                                     c_b["parsed"]))
                       if measured_values(b) != measured_values(a)]
        check("reject/a-moved-measured-value-is-seen-by-the-comparison",
              moved_probe == [0],
              "the comparison must see a ceiling rewritten from 80 to 85, "
              "got %s" % moved_probe)

    live_lines_after, live_state_after = read_log(live)
    # THE LAST CASE MEASURES THE SUITE, the same shape queue 267 put at the
    # bottom of the bot's: a tool that marks fixture rows must not be the next
    # thing writing this file.
    check("reject/this-suite-writes-no-line-to-the-live-log",
          len(live_lines_after) == len(live_lines_before)
          and live_state_after == live_state_before
          and live_lines_after == live_lines_before,
          "the live log went from %d line(s) (%s) to %d (%s) during this run"
          % (len(live_lines_before), live_state_before, len(live_lines_after),
             live_state_after))
    n = len(ok) + len(bad)
    print("\nbudget-log-mark selftest: %d passed, %d failed, %d case(s) run "
          "(%d accepting, %d rejecting; the live log was read %s and written "
          "0 times)"
          % (len(ok), len(bad), n,
             sum(1 for c in ok + bad if c.startswith("accept/")),
             sum(1 for c in ok + bad if c.startswith("reject/")),
             "0 times" if live_state_before == "absent" else "twice"))
    return 0 if not bad else 3


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--mark", action="store_true",
                    help="write the marks; without it this only reads")
    ap.add_argument("--log", default=str(ROOT / LOG_REL),
                    help="another copy of the log, for the PC's")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    sys.exit(do_mark(a.log) if a.mark else do_read(a.log))
