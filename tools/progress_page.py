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
     "Characters and wardrobe", "Animation", "Sound", "Camera, controls and feel", "Interface", "Systems",
     "Tech and budgets", "Production pipeline", "Combat and violence", "The crime toolkit", "Jobs and story"]) if i}
# THE CARRIED LIST IN HIS WORDS (Jafar, 26 October: "plain words only: no item codes, no file names, no
# technical detail; one short line per item"): one line for each item carried from earlier orders, kept
# here beside the ledger's own wording; --check fails when a carried item has no line, so a new one is
# never shown in the ledger's working words.
PLAIN = {
    "shop-empty-unit": "The empty shop to let: its review's fixes not made yet",
    "shop-mickeys-front": "Mickey's shop front: its review's fixes not made yet",
    "shop-fish-market": "The fish market: failed its review; the second go not started",
    "q-first-30": "The first 30 minutes: three choices waiting to go on your page",
    "q-town-inventions": "29 new facts about the town, waiting for your check",
    "q-sound-listening": "Street sounds only an ear can judge, waiting for you",
    "q-street-dressing": "Street props: nine kinds planned, none built yet",
    "his-archive-retention": "The old archive: keep its build files for 3 days",
    "his-archive-actions": "The old archive: switch its automatic runs off",
    "f-hill-haze": "The haze on the hill doesn't thicken toward the top",
    "f-street-details": "Small street faults: the broken window, glass reflections, a lamp post, shop details",
    "f-suspicion-port": "The game doesn't yet use the town's suspicion",
    "f-invented-claims": "Characters still invent details in about 7 replies in 100",
    "f-old-launchers": "Old launchers still name things that are gone",
    "f-face-light": "Faces too dark outside conversations; Sheila's and Darren's faces off their sheets",
    "f-voice-accents": "Some recorded crowd lines sound American",
    "f-thats-all": "Newcomers hear \"that's all I know\" too often",
    "f-claim-about-listener": "The fact check misses what someone says about you",
    "f-placeholder-people": "Three stand-in figures still in the street",
    "f-police-file": "Three timing faults in the police file",
    "f-free-play": "Free play's faults: the dark quay, pavements that trap you, a test key, the save",
    "f-mickey-past": "Mickey's past contradicts itself",
    "f-nightly-bench": "The nightly question test measured nothing three nights running",
    "f-licences-three": "Three pieces of code whose licences are not read yet",
    "f-sash-windows": "The sash windows beyond Mickey's row",
    "o25-2a-walk-slide": "The walk's last slide: the stop's re-step and the run's start, set aside after two tries",
    "o25-2b-sit": "Tom's first sitting route, set aside after two tries",
    "o26-sit-third": "The sit's third try, set aside; the face-up sitting replaced it",
    "o27-invented-source": "Where invented details come from in replies: measured, waiting",
    "o27-cited-replies": "Replies that cite their facts: in the game, waiting for review",
    "o26-pocket-flat-delivery": "The cast voices' flat delivery: a choice for your ear, waiting",
    "o25-4b-voice-frame": "The voice's frame spike, set aside after two tries; worked again as the Stutter",
    "f-office-shadows-high": "The office's small shadows at High, set aside after two tries",
    "o25-fallback-sim-port": "The town's rules ported into the game: the fallback work",
    "o25-progress-page": "This page, kept current every night",
    "o25-daily": "The daily summary and overview",
    "o28d-camera-modes": "The camera by situation: the room row waits for you to see it; fights next",
    "o28c-d13-asset-checks": "Automatic asset checks before reviewers: rounds per piece still to measure",
}
CARRIED_SECTION = "## Carried from earlier orders"
FOLDED = ("now item", "now part of", "worked again as", "worked again in", "worked this week as", "on the waiting list as")   # carried into this week's own items or its waiting list, shown there


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
    text_all = open(os.path.join(ROOT, order_ledger.ORDERS, name), encoding="utf-8").read()
    section = text_all.split(CARRIED_SECTION, 1)[1].split("\n## ", 1)[0] if CARRIED_SECTION in text_all else ""
    for iid in re.findall(r"^- `([^`]+)`", section, re.M):
        status, rest = items.get(iid, ("missing", ""))
        if status in ("done", "dropped") or any(f in rest for f in FOLDED):
            continue
        carried.append({"id": iid, "status": status, "text": PLAIN.get(iid, ""), "his": iid.startswith("his-")})
    days = sorted({m.group(1) for f in os.listdir(PREVIEWS) for m in [re.match(r"^morning-night-(\d{4}-\d\d-\d\d)\.jpg$", f)] if m
                   and all(os.path.exists(os.path.join(PREVIEWS, "morning-%s-%s.jpg" % (v, m.group(1)))) for v in VIEWS)})
    return name, studies, carried, days


def line_2027(stations, today=None):
    """THE 2027 LINE (his order of 2 November, n02-7-2): each phase's weeks against the top of the plan's own estimate
    (PLAN.md), a positive total being weeks behind. The open phase's weeks are counted from its "began" date to today;
    a phase passed keeps the weeks written on it. Returns (stations with the open phase's weeks set, weeks behind)."""
    today = today or datetime.date.today()
    out = []
    for st in stations:
        st = dict(st)
        if st.get("state") == "here" and st.get("began"):
            st["actual_w"] = round((today - datetime.date.fromisoformat(st["began"])).days / 7.0, 1)
        out.append(st)
    behind = sum(st["actual_w"] - st["planned_w"][1] for st in out if "actual_w" in st and st.get("planned_w"))
    return out, round(behind, 1)


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
        for x in carried:
            if not x["text"]:
                print("progress-page FAIL carried item %s has no plain line in tools/progress_page.py PLAIN" % x["id"])
                bad.append("plain")
        if missing:
            print("progress-page FAIL morning pictures not on the page: %s" % ", ".join(missing))
        # the 2027 line agrees with the stations' own weeks as written (not with today's date, which moves)
        behind = round(sum(st["actual_w"] - st["planned_w"][1] for st in d["stations"] if "actual_w" in st and st.get("planned_w")), 1)
        if d.get("line2027", {}).get("behind_w") != behind:
            print("progress-page FAIL the 2027 line says %s weeks behind, the stations %s: run tools/progress_page.py" % (d.get("line2027", {}).get("behind_w"), behind))
            bad.append("line2027")
        print("progress-page: %d studies, %d carried items, %d days; %s" % (len(studies), len(carried), len(days),
              "FAIL" if bad or missing else "PASS"))
        return 1 if bad or missing else 0
    d.update(want)
    d["stations"], behind = line_2027(d["stations"])
    d["line2027"]["behind_w"] = behind
    d["line2027"]["as_of"] = datetime.date.today().strftime("%A %d %B").replace(" 0", " ")
    d["street"]["days"] = sorted(set(d["street"]["days"]) | set(days))
    d["updated"] = datetime.datetime.now().strftime("%A %d %B %Y, %H:%M").replace(" 0", " ")
    json.dump(d, open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("progress.json: %d of 16 studies done, %d carried items, %d days, %.1f weeks behind the plan, updated %s" % (want["studies"]["done"], len(carried), len(d["street"]["days"]), behind, d["updated"]))
    for day in days:
        for v in VIEWS:
            print("  street/morning-%s-%s.jpg <- production/previews/morning-%s-%s.jpg" % (v, day, v, day))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
