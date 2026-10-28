#!/usr/bin/env python3
"""NOTHING HE ORDERED IS FORGOTTEN: EVERY ITEM HAS A STATUS, AND NONE VANISHES.

Jafar, 25 October 2026: "An order ledger: this order is saved as production/orders/2026-10-25.md,
every item and every study with a status: done (with its evidence), set aside (with its reason),
carried over, or dropped by me. Each later order gets its own file; anything not done or dropped
carries into the next one automatically." And: "A check that fails the push when any ledger item or
study has no status, or when an item disappears from one order's file without being done or dropped."

An item is one line in an order file's list sections:

    - `id` **status** what it is ... Evidence: ... / Reason: ...

The statuses: open (the newest order's own work in progress), done (needs "Evidence:"), set aside
(needs "Reason:"), carried over, dropped (needs "Jafar"). This fails when:
  - a list line in an item section has no id and status, or an unknown status;
  - done has no Evidence, set aside no Reason, dropped does not name Jafar;
  - an older order (not the newest) still has an open item;
  - an id in an older order that is not done or dropped is missing from the next order;
  - an id leaves an order's file (against the version being replaced) without having been done or dropped;
  - the newest order lacks any of the sixteen studies (study-1 to study-16);
  - an item new against the version being replaced, still to be worked (open or carried over), names
    no reference: neither "Reference:" (a number or method from Mafia or Kingdom Come II, or "Reference:
    none found") nor the study it comes from (a path under studies/). Jafar, 28 October 2026, A1: "Before
    starting any new item, look up how Mafia or Kingdom Come II does it ... Add a check that fails the push
    when a new item's plan names neither a reference nor 'none found'."

  python tools/order_ledger.py              # the files on disk against the last commit (HEAD)
  python tools/order_ledger.py --push       # a pre-push hook: stdin "<lref> <lsha> <rref> <rsha>" lines
  python tools/order_ledger.py --selftest
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDERS = "production/orders"
STATUSES = ("open", "done", "set aside", "carried over", "dropped")
ITEM = re.compile(r"^- `([A-Za-z0-9._-]+)` \*\*([a-z ]+)\*\*(.*)$")
SECTION = re.compile(r"^## (Items|Studies|Carried)")
STUDIES = {"study-%d" % i for i in range(1, 17)}
REFERENCED = re.compile(r"Reference:|studies/")
ZERO = "0" * 40


def parse(text):
    """{id: (status, rest)} and a list of faults, from one order file's text."""
    items, faults, in_items = {}, [], False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            in_items = bool(SECTION.match(line))
            continue
        if not in_items or not line.startswith("- "):
            continue
        m = ITEM.match(line)
        if not m:
            faults.append("line %d is an item with no id and status: %s" % (n, line[:80]))
            continue
        iid, status, rest = m.group(1), m.group(2), m.group(3)
        if status not in STATUSES:
            faults.append("line %d: %s has an unknown status '%s'" % (n, iid, status))
            continue
        if iid in items:
            faults.append("line %d: %s appears twice" % (n, iid))
        if status == "done" and "Evidence:" not in rest:
            faults.append("%s is done with no 'Evidence:'" % iid)
        if status == "set aside" and "Reason:" not in rest:
            faults.append("%s is set aside with no 'Reason:'" % iid)
        if status == "dropped" and "Jafar" not in rest:
            faults.append("%s is dropped without naming Jafar" % iid)
        items[iid] = (status, rest)
    return items, faults


def check(files, previous=None):
    """files and previous: {filename: text}. Returns the list of faults (empty: clean)."""
    faults, parsed = [], {}
    names = sorted(f for f in files if re.match(r"^\d{4}-\d\d-\d\d.*\.md$", f))
    if not names:
        return ["no order file in %s: nothing measured" % ORDERS]
    for f in names:
        items, fs = parse(files[f])
        parsed[f] = items
        faults += ["%s: %s" % (f, x) for x in fs]
        if not items:
            faults.append("%s: no items" % f)
    newest = names[-1]
    for i, f in enumerate(names[:-1]):
        nxt = parsed[names[i + 1]]
        for iid, (status, _) in parsed[f].items():
            if status == "open":
                faults.append("%s: %s is still open in an older order" % (f, iid))
            if status not in ("done", "dropped") and iid not in nxt:
                faults.append("%s: %s (%s) is not carried into %s" % (f, iid, status, names[i + 1]))
    missing = STUDIES - set(parsed[newest])
    if missing:
        faults.append("%s: studies missing: %s" % (newest, ", ".join(sorted(missing, key=lambda s: int(s[6:])))))
    if previous is not None:
        # REFERENCE FIRST (his A1, 28 October): what is new here and still to be worked names its reference.
        before = set()
        for text in previous.values():
            before |= set(parse(text)[0])
        for f in names:
            for iid, (status, rest) in parsed[f].items():
                if iid not in before and status in ("open", "carried over") and not REFERENCED.search(rest):
                    faults.append("%s: %s is new and names no reference: add 'Reference:' (Mafia's or Kingdom Come II's "
                                  "number or method, or 'none found') or its study (studies/...)" % (f, iid))
    for f, text in (previous or {}).items():
        if f not in files:
            faults.append("%s: the order file was removed" % f)
            continue
        old, _ = parse(text)
        for iid, (status, _) in old.items():
            if iid not in parsed.get(f, {}) and status not in ("done", "dropped"):
                faults.append("%s: %s left the file without being done or dropped (it was %s)" % (f, iid, status))
    return faults


def git(*args, check=True):
    r = subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        raise RuntimeError(r.stderr.strip())
    return r.stdout


def files_at(rev):
    if rev is None:
        d = os.path.join(ROOT, ORDERS)
        return {f: open(os.path.join(d, f), encoding="utf-8").read() for f in os.listdir(d)} if os.path.isdir(d) else {}
    out = {}
    for name in git("ls-tree", "--name-only", rev, ORDERS + "/", check=False).split():
        out[os.path.basename(name)] = git("show", "%s:%s" % (rev, name))
    return out


def report(faults, what):
    for x in faults:
        print("order-ledger FAIL " + x)
    print("order-ledger: %s, %d fault(s)%s" % (what, len(faults), "" if not faults else " (production/orders; RULINGS.md, 25 Oct)"))
    return 1 if faults else 0


def selftest():
    good = ("# o\n\n## Items\n\n- `a` **done** x. Evidence: y\n- `b` **set aside** x. Reason: y\n"
            "- `c` **carried over** x\n- `d` **dropped** by Jafar\n\n## Studies\n\n" +
            "".join("- `study-%d` **carried over** s\n" % i for i in range(1, 17)) + "\n## His words\n\n- free text\n")
    nxt = good.replace("- `a` **done** x. Evidence: y\n", "").replace("- `d` **dropped** by Jafar\n", "")
    cases = [
        ("ACCEPT one clean order", {"2026-10-25.md": good}, None, 0),
        ("ACCEPT a carried item in the next order; done and dropped need not carry",
         {"2026-10-25.md": good, "2026-11-02.md": nxt}, None, 0),
        ("REFUSE an item with no status", {"2026-10-25.md": good.replace("- `c` **carried over** x", "- c, no status")}, None, 1),
        ("REFUSE an unknown status", {"2026-10-25.md": good.replace("**carried over** x\n- `d`", "**maybe** x\n- `d`")}, None, 1),
        ("REFUSE done without evidence", {"2026-10-25.md": good.replace(" Evidence: y", "")}, None, 1),
        ("REFUSE set aside without a reason", {"2026-10-25.md": good.replace(" Reason: y", "")}, None, 1),
        ("REFUSE a drop not by Jafar", {"2026-10-25.md": good.replace("by Jafar", "by me")}, None, 1),
        ("REFUSE a carried item missing from the next order",
         {"2026-10-25.md": good, "2026-11-02.md": nxt.replace("- `c` **carried over** x\n", "")}, None, 1),
        ("REFUSE an open item left in an older order",
         {"2026-10-25.md": good.replace("`c` **carried over**", "`c` **open**"), "2026-11-02.md": nxt}, None, 1),
        ("REFUSE a study missing", {"2026-10-25.md": good.replace("- `study-9` **carried over** s\n", "")}, None, 1),
        ("REFUSE an item that leaves the file without being done or dropped",
         {"2026-10-25.md": good.replace("- `b` **set aside** x. Reason: y\n", "")}, {"2026-10-25.md": good}, 1),
        ("ACCEPT a done item leaving the file", {"2026-10-25.md": good.replace("- `a` **done** x. Evidence: y\n", "")},
         {"2026-10-25.md": good}, 0),
        ("REFUSE an empty ledger: nothing measured", {}, None, 1),
        ("REFUSE a new open item naming no reference",
         {"2026-10-25.md": good.replace("- `c` **carried over** x\n", "- `c` **carried over** x\n- `e` **open** new\n")},
         {"2026-10-25.md": good}, 1),
        ("ACCEPT a new item naming its reference",
         {"2026-10-25.md": good.replace("- `c` **carried over** x\n", "- `c` **carried over** x\n- `e` **open** new. Reference: Mafia's 1.65 m\n")},
         {"2026-10-25.md": good}, 0),
        ("ACCEPT a new item saying none found",
         {"2026-10-25.md": good.replace("- `c` **carried over** x\n", "- `c` **carried over** x\n- `e` **open** new. Reference: none found\n")},
         {"2026-10-25.md": good}, 0),
        ("ACCEPT a new item citing its study",
         {"2026-10-25.md": good.replace("- `c` **carried over** x\n", "- `c` **carried over** x\n- `e` **carried over** new (studies/09-camera-controls.md)\n")},
         {"2026-10-25.md": good}, 0),
        ("ACCEPT an old item without a reference (the rule is for new items)",
         {"2026-10-25.md": good}, {"2026-10-25.md": good}, 0),
        ("ACCEPT a new item already done, its evidence its own record",
         {"2026-10-25.md": good.replace("- `c` **carried over** x\n", "- `c` **carried over** x\n- `e` **done** new. Evidence: z\n")},
         {"2026-10-25.md": good}, 0),
    ]
    fails = 0
    print("order-ledger selftest")
    for name, files, prev, want_bad in cases:
        got = check(files, prev)
        ok = bool(got) == bool(want_bad)
        fails += 0 if ok else 1
        print("  %s %s: %d fault(s)" % ("ok  " if ok else "FAIL", name, len(got)))
    print("order-ledger selftest: %s" % ("passed" if not fails else "FAILED (%d)" % fails))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--push" in argv:
        faults, n = [], 0
        for line in sys.stdin.read().splitlines():
            p = line.split()
            if len(p) != 4 or p[1] == ZERO:
                continue
            prev = files_at(p[3]) if p[3] != ZERO and git("cat-file", "-t", p[3], check=False).strip() == "commit" else None
            now = files_at(p[1])
            if not now and not prev:
                # the side sessions' branches (lab, talk, cloud) carry no ledger: nothing of his to lose there
                print("order-ledger: %s carries no order ledger, skipped" % p[0])
                continue
            n += 1
            faults += check(now, prev)
        if not n:
            print("order-ledger: no pushed ref carries the order ledger")
            return 0
        return report(faults, "%d pushed ref(s)" % n)
    return report(check(files_at(None), files_at("HEAD")), "the working tree against HEAD")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
