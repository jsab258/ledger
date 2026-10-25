#!/usr/bin/env python3
"""HIS PROGRESS PAGE, KEPT CURRENT FROM ITS HOMES.

Jafar, 25 October 2026: "My progress page stays current every night:
https://claude.ai/artifact/EEcWMTp5E9VqKrQsC8KBdk. Read it first, update its progress.json (stations,
bosses and their numbers, studies, carried items, the date), add each morning's three pictures under
street/ with the same names as in production/previews, and republish to the same link." And: "On my
progress page, a studies bar (studies done out of 16) and the list of carried-over items."

The page's source lives in production/progress-page/ (index.html, progress.json). The stations and
bosses are written by hand from the measurements and his rulings; the studies and the carried items
are derived here from the order ledger (production/orders, their home) and never typed twice; the
street's days are the morning pictures found in production/previews.

  python tools/progress_page.py            # refresh progress.json; print the files a publish must carry
  python tools/progress_page.py --check    # fail when progress.json disagrees with the ledger or the pictures
"""
import datetime
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import order_ledger  # noqa: E402

PAGE = os.path.join(ROOT, "production", "progress-page")
PREVIEWS = os.path.join(ROOT, "production", "previews")
VIEWS = ("hook-day", "reverse-day", "night")
NAMES = {"study-%d" % i: n for i, n in enumerate(
    ["", "NPC life and AI", "The first 30 minutes", "Dialogue and barks", "Street and world building", "Visuals",
     "Characters and wardrobe", "Animation", "Sound", "Study 9", "Study 10", "Systems", "Tech and budgets",
     "Study 13", "Combat and violence", "The crime toolkit", "Jobs and story"]) if i}


def newest_order():
    d = os.path.join(ROOT, order_ledger.ORDERS)
    name = sorted(f for f in os.listdir(d) if re.match(r"^\d{4}-\d\d-\d\d.*\.md$", f))[-1]
    return name, order_ledger.parse(open(os.path.join(d, name), encoding="utf-8").read())[0]


def derived():
    name, items = newest_order()
    studies = []
    for i in range(1, 17):
        sid = "study-%d" % i
        status, rest = items.get(sid, ("missing", ""))
        week = "this week" if "this week" in rest else "next week" if "next week" in rest else ""
        studies.append({"n": i, "name": NAMES[sid], "status": status, "week": week})
    carried = []
    for iid, (status, rest) in items.items():
        if iid.startswith(("o25-", "study-")) or status in ("done", "dropped"):
            continue
        text = rest.strip()
        text = re.split(r" Reason: | \(production/| \(cloud week", text)[0].rstrip(" .")
        carried.append({"id": iid, "status": status, "text": text, "his": iid.startswith("his-")})
    days = sorted({m.group(1) for f in os.listdir(PREVIEWS) for m in [re.match(r"^morning-night-(\d{4}-\d\d-\d\d)\.jpg$", f)] if m
                   and all(os.path.exists(os.path.join(PREVIEWS, "morning-%s-%s.jpg" % (v, m.group(1)))) for v in VIEWS)})
    return name, studies, carried, days


def main(argv):
    path = os.path.join(PAGE, "progress.json")
    d = json.load(open(path, encoding="utf-8"))
    order, studies, carried, days = derived()
    want = {"studies": {"done": sum(1 for s in studies if s["status"] == "done"), "total": 16, "order": order, "list": studies},
            "carried": carried}
    if "--check" in argv:
        bad = [k for k in want if d.get(k) != want[k]]
        missing = [x for x in days if x not in d["street"]["days"]]
        for k in bad:
            print("progress-page FAIL %s disagrees with the order ledger (%s): run tools/progress_page.py" % (k, order))
        if missing:
            print("progress-page FAIL morning pictures not on the page: %s" % ", ".join(missing))
        print("progress-page: %d studies, %d carried items, %d days; %s" % (len(studies), len(carried), len(days),
              "FAIL" if bad or missing else "PASS"))
        return 1 if bad or missing else 0
    d.update(want)
    d["street"]["days"] = sorted(set(d["street"]["days"]) | set(days))
    d["updated"] = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M").replace(" 0", " ")
    json.dump(d, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("progress.json: %d of 16 studies done, %d carried items, %d days, updated %s" % (want["studies"]["done"], len(carried), len(d["street"]["days"]), d["updated"]))
    for day in days:
        for v in VIEWS:
            print("  street/morning-%s-%s.jpg <- production/previews/morning-%s-%s.jpg" % (v, day, v, day))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
