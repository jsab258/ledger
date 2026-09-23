"""The per-stage checklist's count, and the one check that keeps a stage honest.

    python tools/stage-check.py                  # counts, and refuses a finished stage with open items
    python tools/stage-check.py --write-count    # also writes the count block at the top of FOR-JAFAR.md
    python tools/stage-check.py --selftest

WHY IT EXISTS, 23 September. Jafar sorted the master feature checklist and
made it the plan, in ROADMAP.md, with four rules. The fourth, his words: "A
stage cannot be declared finished while any item in it is open. Enforce this
mechanically, with one check that counts open items per stage and refuses to
mark a stage done until the count is zero." This is that check. It reads
ROADMAP.md and nothing else, keeps no history, and runs with the cheap checks
on every push.

WHAT IT READS. Under "## The checklist, per stage", one "### Stage N" (or
"### Ship-prep", "### Not staged") heading per stage, a line "Stage state:
OPEN" or "Stage state: FINISHED", and a table:

    | id | feature | kind | status | evidence or reason |

status is open, done, moved or out. Rule 3: done needs evidence, a link or a
file in the last column, and a done row without one COUNTS AS OPEN. Rule 2: a
moved or out row needs its reason; a moved row names the stage it went to
("to stage 4: ...") and that stage must carry the same id.

WHAT IT REFUSES, exit 1: a stage marked FINISHED with any open item; a row
whose status is not one of the four; an out or moved row with no reason; a
moved row whose target stage does not carry it; an id twice in one stage.

THE COUNT, one line per stage, as he asked for it: "stage 1: 38 of 47 done,
4 moved, 5 out, 5 open".
"""
import os
import re
import sys

ROADMAP_REL = "ROADMAP.md"
FOR_JAFAR_REL = "FOR-JAFAR.md"
SECTION = "## The checklist, per stage"
COUNT_START = "<!-- stage-count: written by tools/stage-check.py --write-count, never typed -->"
COUNT_END = "<!-- /stage-count -->"
STATUSES = ("open", "done", "moved", "out")


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def has_evidence(cell):
    return bool(re.search(r"\]\([^)]+\)|[\w./-]+\.(png|gif|jpg|webp|mp4|wav|txt|md|cs|cpp|h|py|json|tsv)\b", cell))


def parse(text):
    """{stage label: {"state": str, "rows": [(id, status, last cell)]}} in file order."""
    stages = {}
    order = []
    at = text.find(SECTION)
    if at < 0:
        return stages, order
    body = text[at + len(SECTION):]
    nxt = re.search(r"^## ", body, re.M)
    if nxt:
        body = body[:nxt.start()]
    cur = None
    for line in body.splitlines():
        h = re.match(r"^### (.+?)\s*$", line)
        if h:
            cur = stage_label(h.group(1))
            stages[cur] = {"state": "", "rows": []}
            order.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^Stage state:\s*(\w+)", line)
        if m:
            stages[cur]["state"] = m.group(1).upper()
            continue
        if not line.startswith("|") or re.match(r"^\|\s*-", line) or re.match(r"^\|\s*id\s*\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        stages[cur]["rows"].append((cells[0], cells[3].lower(), cells[4]))
    return stages, order


def stage_label(heading):
    m = re.match(r"(?i)stage\s+(\d+)", heading)
    if m:
        return "stage " + m.group(1)
    if heading.lower().startswith("ship"):
        return "ship-prep"
    if heading.lower().startswith("not staged"):
        return "not staged"
    return heading.lower()


def count(stages, order):
    out = []
    problems = []
    for st in order:
        rows = stages[st]["rows"]
        n = {"open": 0, "done": 0, "moved": 0, "out": 0}
        seen = set()
        for rid, status, last in rows:
            if rid in seen:
                problems.append("%s: %s appears twice" % (st, rid))
            seen.add(rid)
            if status not in STATUSES:
                problems.append("%s: %s has status '%s', not one of %s" % (st, rid, status, "/".join(STATUSES)))
                n["open"] += 1
                continue
            if status == "done" and not has_evidence(last):
                n["open"] += 1
                problems.append("%s: %s is marked done with no evidence linked; counted open" % (st, rid))
                continue
            if status in ("out", "moved") and not last.strip():
                problems.append("%s: %s is %s with no reason" % (st, rid, status))
            if status == "moved":
                t = re.match(r"(?i)to (stage \d+|ship-prep)", last.strip())
                target = t.group(1).lower() if t else None
                if target is None or target not in stages or rid not in [r[0] for r in stages[target]["rows"]]:
                    problems.append("%s: %s is moved but %s does not carry it" % (st, rid, target or "no stage named"))
            n[status] += 1
        out.append((st, len(rows), n, stages[st]["state"]))
    return out, problems


def count_line(st, total, n):
    return "%s: %d of %d done, %d moved, %d out, %d open" % (st, n["done"], total, n["moved"], n["out"], n["open"])


def refusals(counts):
    return ["%s is marked FINISHED with %d item(s) open" % (st, n["open"])
            for st, total, n, state in counts if state == "FINISHED" and n["open"] > 0]


def write_count(root, counts):
    path = os.path.join(root, FOR_JAFAR_REL)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    block = COUNT_START + "\n" + "\n".join("- " + count_line(st, total, n) for st, total, n, _ in counts) + "\n" + COUNT_END
    if COUNT_START in text and COUNT_END in text:
        a = text.index(COUNT_START)
        b = text.index(COUNT_END) + len(COUNT_END)
        text = text[:a] + block + text[b:]
    else:
        at = text.find("## Decisions waiting on me")
        head = "## The plan at a glance\n\n" + block + "\n\n"
        text = text[:at] + head + text[at:] if at >= 0 else head + text
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def run(root, write):
    with open(os.path.join(root, ROADMAP_REL), encoding="utf-8") as fh:
        stages, order = parse(fh.read())
    if not order:
        print("stage-check: NOTHING-MEASURED - ROADMAP.md has no '%s' section" % SECTION)
        return 1
    counts, problems = count(stages, order)
    for st, total, n, state in counts:
        print("  " + count_line(st, total, n) + ("  [FINISHED]" if state == "FINISHED" else ""))
    for p in problems[:40]:
        print("  note: " + p)
    if len(problems) > 40:
        print("  note: ... and %d more" % (len(problems) - 40))
    refused = refusals(counts)
    hard = [p for p in problems if "counted open" not in p]
    for r in refused:
        print("  REFUSED: " + r)
    if write:
        write_count(root, counts)
        print("  wrote the count block at the top of FOR-JAFAR.md")
    items = sum(t for _, t, _, _ in counts)
    ok = not refused and not hard
    print("stage-check: %s - %d stage(s), %d item(s), %d refused, %d malformed"
          % ("clean" if ok else "RED", len(counts), items, len(refused), len(hard)))
    return 0 if ok else 1


FIXTURE = """# R
## The checklist, per stage
### Stage 1
Stage state: %s
| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| A | a | floor | done | [frame](x.png) |
| B | b | floor | %s | %s |
| C | c | genre G3 | out | G3: not a shooter |
| D | d | floor | moved | to stage 2: needs people |
### Stage 2
Stage state: OPEN
| id | feature | kind | status | evidence or reason |
|---|---|---|---|---|
| D | d | floor | open | from stage 1 |
## Next
"""


def selftest():
    passed = failed = 0

    def ok(name, cond, detail=""):
        nonlocal passed, failed
        if cond:
            passed += 1
        else:
            failed += 1
            print("stage-check selftest FAIL %s %s" % (name, detail))

    def counts_of(state, b_status, b_last):
        s, o = parse(FIXTURE % (state, b_status, b_last))
        return count(s, o)

    c, p = counts_of("OPEN", "open", "")
    ok("the count reads each status", count_line(*c[0][:3]) == "stage 1: 1 of 4 done, 1 moved, 1 out, 1 open", count_line(*c[0][:3]))
    ok("an open stage with open items is not refused", not refusals(c))
    c, p = counts_of("FINISHED", "open", "")
    ok("a finished stage with an open item is REFUSED", len(refusals(c)) == 1)
    c, p = counts_of("FINISHED", "done", "[test](t.txt)")
    ok("a finished stage with nothing open passes", not refusals(c) and not p, str(p))
    c, p = counts_of("FINISHED", "done", "looked fine to me")
    ok("done without evidence counts as open and the stage is refused",
       c[0][2]["open"] == 1 and len(refusals(c)) == 1)
    c, p = counts_of("OPEN", "out", "")
    ok("out with no reason is malformed", any("no reason" in x for x in p))
    c, p = counts_of("OPEN", "gone", "")
    ok("an unknown status is malformed and counted open", any("not one of" in x for x in p) and c[0][2]["open"] == 1)
    s, o = parse((FIXTURE % ("OPEN", "open", "")).replace("| D | d | floor | open | from stage 1 |\n", ""))
    c, p = count(s, o)
    ok("a moved item its target does not carry is malformed", any("does not carry" in x for x in p))
    print("stage-check selftest: passed=%d/%d failed=%d" % (passed, passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run(repo_root(), "--write-count" in sys.argv))
