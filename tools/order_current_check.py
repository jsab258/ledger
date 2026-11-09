"""Is the order the session works from still running? (9 November 2026, advisor 62.)

From 13:00 to 15:31 on Monday 9 November no session worked: the hourly task's
instructions named the order of 2 November and its end, so every start stopped.
This check reads the order the handover's "**The goal:**" line names (and any
order named in production/handover/HOURLY-TASK.md, the exact copy of the hourly
task's instructions), reads its end from its own "Runs ... to <weekday> <day>
<Month> [year], HH:MM" line, and fails when that end has passed and no newer
order file exists in production/orders/ (then: "adopt the next order" goes first
on his page). It also fails when HOURLY-TASK.md is missing.

    python tools/order_current_check.py            # PASS or FAIL with the reason
    python tools/order_current_check.py --selftest
"""
import datetime
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MONTHS = {m: i for i, m in enumerate(["January", "February", "March", "April", "May", "June", "July",
                                      "August", "September", "October", "November", "December"], 1)}
END = re.compile(r"[Rr]uns\b[^.]*?\bto (?:\w+day )?(\d{1,2}) (" + "|".join(MONTHS) + r")(?: (\d{4}))?,? (\d{1,2}):(\d{2})")
NAMED = re.compile(r"production/orders/(\d{4}-\d{2}-\d{2})\.md")


def order_end(text, year):
    m = END.search(text)
    if not m:
        return None
    d, mon, y, hh, mm = m.groups()
    return datetime.datetime(int(y or year), MONTHS[mon], int(d), int(hh), int(mm))


def verdict(named, files, texts, now):
    """named: order dates named by the handover/task; files: dates present; texts: date -> text."""
    if not named:
        return "FAIL: the handover names no order (production/orders/<date>.md)"
    for n in sorted(set(named)):
        if n not in files:
            return "FAIL: order %s is named but has no file" % n
        end = order_end(texts[n], int(n[:4]))
        if end is None:
            return "FAIL: order %s has no 'Runs ... to <day> <Month>, HH:MM' line" % n
        newer = [f for f in files if f > n]
        if now > end and not newer:
            return "FAIL: order %s ended %s and no newer order exists: put 'adopt the next order' first on his page" % (n, end.strftime("%d %b %H:%M"))
    return "PASS"


def main():
    if "--selftest" in sys.argv:
        t = {"2026-11-02": "Runs to Monday 9 November 2026, 13:00 Swiss time.",
             "2026-11-09": "adopted by his tap on his page. Runs from that tap to Monday 16 November, 13:00 Swiss time."}
        at = datetime.datetime(2026, 11, 9, 15, 0)
        assert verdict(["2026-11-02"], ["2026-11-02"], t, at).startswith("FAIL: order 2026-11-02 ended")
        assert verdict(["2026-11-02"], ["2026-11-02", "2026-11-09"], t, at) == "PASS"
        assert verdict(["2026-11-09"], ["2026-11-02", "2026-11-09"], t, at) == "PASS"
        assert verdict(["2026-11-09"], ["2026-11-09"], t, datetime.datetime(2026, 11, 16, 13, 1)).startswith("FAIL")
        assert verdict([], [], {}, at).startswith("FAIL")
        assert order_end(t["2026-11-09"], 2026) == datetime.datetime(2026, 11, 16, 13, 0)
        print("order_current_check selftest: PASS")
        return 0
    od = os.path.join(REPO, "production", "orders")
    files = sorted(f[:-3] for f in os.listdir(od) if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.md", f))
    texts = {f: open(os.path.join(od, f + ".md"), encoding="utf-8").read() for f in files}
    ho = open(os.path.join(REPO, "production", "handover", "HANDOVER.md"), encoding="utf-8").read()
    goal = next((l for l in ho.splitlines() if l.startswith("**The goal:**")), "")
    named = NAMED.findall(goal)[:1]
    task = os.path.join(REPO, "production", "handover", "HOURLY-TASK.md")
    if not os.path.exists(task):
        print("FAIL: production/handover/HOURLY-TASK.md missing (the exact copy of the hourly task's instructions)")
        return 1
    named += NAMED.findall(open(task, encoding="utf-8").read())
    v = verdict(named, files, texts, datetime.datetime.now())
    print("order-current:", v)
    return 0 if v == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
