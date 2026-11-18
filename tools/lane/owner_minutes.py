#!/usr/bin/env python3
"""HIS MINUTES A WEEK: WHAT THE SESSIONS ASKED OF JAFAR'S TIME, FOR MONDAY'S AUDIT.

Blind-spots recommendation 8, adopted by Jafar 18 Nov 08:05 (advisor 218); the design and its sources are in
production/lane/OWNER-MINUTES-MEASURE-2026-11-18.md (reviewed). This is that design's counting function,
written by the cloud lane for the main session to merge into Monday's audit (beside the process share).

Counted from the repository: page items (words read at 200 a minute), his taps (stored answers, 10 s each),
pictures (20 s each), hands at the PC (ACTION or his_hands: 5 minutes plus 30 s a step). Passed in when the
caller has them (read from the page's database): report rows' words, advisor rows (2 minutes each, "chosen",
shown beside the target, never judged against it). Everything per event except the reading speed is an
estimate, as the design says; anything not passed in is "n.m." (not measured) in the line.

    python tools/lane/owner_minutes.py 2026-11-09 [--finished 23] [--target 30] [--advisor-dir DIR]
    (DIR: the page database's "advisor" collection exported one JSON file a row, as ArtifactData out_dir writes it)
"""
import datetime as dt
import glob
import io
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE = os.path.join(ROOT, "production", "approvals", "needs-you")
ANSWERS = os.path.join(ROOT, "production", "approvals", "answers", "1VZHkCBAHdw8HBdNHrByL8")
WORD = re.compile(r"[A-Za-z0-9À-ɏ'’]+")
TEXT_FIELDS = ("title", "text", "why", "steps", "options", "recommendation", "detail")


def words(x):
    """Words in any nested mix of strings, lists and dicts (option keys like 'yes' count, as he sees the labels)."""
    if x is None:
        return 0
    if isinstance(x, str):
        return len(WORD.findall(x))
    if isinstance(x, dict):
        return sum(words(v) for v in x.values())
    if isinstance(x, (list, tuple)):
        return sum(words(v) for v in x)
    return 0


def count_of(x):
    """How many steps or pictures: a list counts its entries; a string its non-empty lines; anything else 0."""
    if isinstance(x, (list, tuple)):
        return len(x)
    if isinstance(x, str):
        return len([ln for ln in x.splitlines() if ln.strip()])
    return 0


def item_words(item):
    return sum(words(item.get(f)) for f in TEXT_FIELDS)


def _swiss_from_utc(s):
    """An ISO UTC time ('...Z') as Swiss local time (CET; CEST from the last Sunday of March to the last of October)."""
    t = dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")

    def last_sunday(y, m):
        d = dt.datetime(y, m + 1, 1) - dt.timedelta(days=1)
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    start, end = last_sunday(t.year, 3).replace(hour=1), last_sunday(t.year, 10).replace(hour=1)
    return t + dt.timedelta(hours=2 if start <= t < end else 1)


def parse_added(s):
    """An item's 'added' (Swiss local, 'YYYY-MM-DD HH:MM'), or None."""
    try:
        return dt.datetime.strptime((s or "")[:16], "%Y-%m-%d %H:%M")
    except ValueError:
        return None


def parse_answer_at(s):
    """A stored answer's 'at' as Swiss local time: '...Z' or an explicit offset is converted; no zone means Swiss."""
    if not isinstance(s, str) or not s:
        return None
    try:
        if s.endswith("Z"):
            return _swiss_from_utc(s)
        t = dt.datetime.fromisoformat(s)
        if t.tzinfo is not None:
            u = t.astimezone(dt.timezone.utc).replace(tzinfo=None)
            return _swiss_from_utc(u.strftime("%Y-%m-%dT%H:%M:%S"))
        return t.replace(microsecond=0)
    except ValueError:
        return None


def count_advisor_rows(folder, week_start):
    """Numbered advisor rows in a week, from the page database's 'advisor' collection exported as one JSON file a row
    (file name = row id, numbered rows end in -<number>). Returns (rows carrying his_answer, all numbered rows).
    Pass the first as advisor_rows: his_answer is the one field that proves his time was spent (a lower bound)."""
    ws = dt.datetime.combine(week_start, dt.time()) if isinstance(week_start, dt.date) and not isinstance(week_start, dt.datetime) else week_start
    days = set((ws + dt.timedelta(days=k)).date().isoformat() for k in range(7))
    with_answer = total = 0
    for p in sorted(glob.glob(os.path.join(folder, "*.json"))):
        rid = os.path.splitext(os.path.basename(p))[0]
        if rid[:10] not in days or not re.search(r"-\d+$", rid):
            continue
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except ValueError:
            continue
        d = d.get("data", d) if isinstance(d, dict) else {}
        total += 1
        if str(d.get("his_answer") or "").strip():
            with_answer += 1
    return with_answer, total


def owner_minutes(week_start, items, answers, reports=None, advisor_rows=None, finished_units=None,
                  wpm=200, tap_s=10, pic_s=20, pc_walk_min=5, step_s=30, advisor_total=None):
    """items: page items (dicts as items.json); answers: [{"id", "at" (datetime, Swiss)}]; reports: [text] or None;
    advisor_rows: int or None, the numbered advisor rows carrying his_answer (count_advisor_rows' first value, not all
    rows); advisor_total: all numbered rows, shown beside it; finished_units: int or None. Returns the design's dict."""
    ws = dt.datetime.combine(week_start, dt.time()) if isinstance(week_start, dt.date) and not isinstance(week_start, dt.datetime) else week_start
    we = ws + dt.timedelta(days=7)
    inweek = lambda t: t is not None and ws <= t < we  # noqa: E731
    items = [i for i in items if isinstance(i, dict)]
    week_items = [i for i in items if inweek(parse_added(i.get("added")))]
    by_id = {i.get("id"): i for i in items}
    items_min = sum(item_words(i) for i in week_items) / float(wpm)
    pictures_min = sum(count_of(i.get("pictures")) for i in week_items) * pic_s / 60.0
    hands_min = 0.0
    for i in week_items:
        if i.get("tag") == "ACTION" or i.get("his_hands"):
            hands_min += pc_walk_min + count_of(i.get("steps")) * step_s / 60.0
    week_answers = [a for a in answers if inweek(a.get("at"))]
    taps_min = len(week_answers) * tap_s / 60.0
    estimated = []
    for a in week_answers:
        if a.get("id") not in by_id:
            estimated.append("answer with no matching item: %s" % a.get("id"))
    batches = defaultdict(set)
    for i in week_items:
        t = parse_added(i.get("added"))
        batches[t.date().isoformat()].add(t)
    reports_min = None if reports is None else sum(words(r) for r in reports) / float(wpm)
    advisor_min = None if advisor_rows is None else advisor_rows * 2.0
    asked = items_min + taps_min + pictures_min + hands_min + (reports_min or 0.0)
    if reports is None:
        estimated.append("reports not measured")
    if advisor_rows is None:
        estimated.append("advisor rows not measured")
    if not finished_units:
        per_piece = "none finished"
    else:
        per_piece = round(asked / finished_units, 1)
    return {"asked": round(asked, 1), "chosen": None if advisor_min is None else round(advisor_min, 1),
            "items_min": round(items_min, 1), "taps_min": round(taps_min, 1), "pictures_min": round(pictures_min, 1),
            "hands_min": round(hands_min, 1), "reports_min": None if reports_min is None else round(reports_min, 1),
            "advisor_min": None if advisor_min is None else round(advisor_min, 1), "per_piece": per_piece,
            "estimated_parts": estimated, "batches_by_day": {d: len(s) for d, s in sorted(batches.items())},
            "items": len(week_items), "answers": len(week_answers),
            "advisor_rows": advisor_rows, "advisor_total": advisor_total}


def audit_line(week_start, r, target=None):
    nm = lambda v: "n.m." if v is None else "%.0f" % v  # noqa: E731
    end = week_start + dt.timedelta(days=6)
    over = [d for d, n in r["batches_by_day"].items() if n > 2]
    adv = "advisor"
    if r.get("advisor_rows") is not None and r.get("advisor_total") is not None:
        adv = "%d advisor rows with his words of %d" % (r["advisor_rows"], r["advisor_total"])
    line = "Owner minutes %s to %s: asked %.0f (items %.0f, taps %.0f, pictures %.0f, hands %.0f, reports %s); chosen %s (%s); per finished piece %s" % (
        week_start.strftime("%d %b"), end.strftime("%d %b"), r["asked"], r["items_min"], r["taps_min"], r["pictures_min"],
        r["hands_min"], nm(r["reports_min"]), nm(r["chosen"]), adv,
        r["per_piece"] if isinstance(r["per_piece"], str) else "%.1f" % r["per_piece"])
    if target is not None:
        line += "; target %d%s" % (target, " OVER" if r["asked"] > target else "")
    if over:
        line += "; days over two batches: %d" % len(over)
    return line


def read_items(folder=PAGE):
    out = []
    for name in ("items.json", "archive.json"):
        p = os.path.join(folder, name)
        if os.path.exists(p):
            d = json.load(io.open(p, encoding="utf-8"))
            out.extend(d.get("items", []) if isinstance(d, dict) else d)
    seen, uniq = set(), []
    for i in out:
        if isinstance(i, dict) and i.get("id") not in seen:
            seen.add(i.get("id"))
            uniq.append(i)
    return uniq


def read_answers(folder=ANSWERS):
    """Stored answers (files with an 'at'; the items/ copies carry none). One tap per id, the earliest kept."""
    best = {}
    for p in sorted(glob.glob(os.path.join(folder, "*", "*.json"))):
        try:
            d = json.load(io.open(p, encoding="utf-8"))
        except ValueError:
            continue
        t = parse_answer_at(d.get("at")) if isinstance(d, dict) else None
        k = os.path.splitext(os.path.basename(p))[0]
        if t is not None and (k not in best or t < best[k]):
            best[k] = t
    return [{"id": k, "at": t} for k, t in sorted(best.items())]


def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 0
    ws = dt.datetime.strptime(argv[0], "%Y-%m-%d")
    ws -= dt.timedelta(days=ws.weekday())
    fin = int(argv[argv.index("--finished") + 1]) if "--finished" in argv else None
    tgt = int(argv[argv.index("--target") + 1]) if "--target" in argv else None
    adv_rows = adv_total = None
    if "--advisor-dir" in argv:
        adv_rows, adv_total = count_advisor_rows(argv[argv.index("--advisor-dir") + 1], ws)
    r = owner_minutes(ws, read_items(), read_answers(), finished_units=fin, advisor_rows=adv_rows, advisor_total=adv_total)
    print(audit_line(ws, r, tgt))
    print("batches by day: %s; items %d, answers %d; estimated: %s" % (r["batches_by_day"], r["items"], r["answers"], "; ".join(r["estimated_parts"]) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
