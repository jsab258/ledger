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
  python tools/progress_page.py --check    # fail when progress.json disagrees with the ledger or the pictures, lacks a key, or is stale
  python tools/progress_page.py --published  # record a publish (run right after the Artifact publish)
  python tools/progress_page.py --selftest
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
    files = order_ledger.files_at(None)  # each order joined to its archive (his ruling of 4 November)
    name = sorted(f for f in files if re.match(r"^\d{4}-\d\d-\d\d.*\.md$", f))[-1]
    return name, order_ledger.parse(files[name])[0]


def derived():
    name, items = newest_order()
    studies = []
    for i in range(1, 17):
        sid = "study-%d" % i
        status, rest = items.get(sid, ("missing", ""))
        week = "this week" if "this week" in rest else "next week" if "next week" in rest else ""
        studies.append({"n": i, "name": NAMES[sid], "status": status, "week": week})
    carried = []
    text_all = order_ledger.files_at(None)[name]
    # since 4 November this section is in the order's archive, and the carried items still open stand short in the order's
    # "## Carried still open", their full lines kept in the archive's history (read for FOLDED)
    section = "\n".join(text_all.split(head, 1)[1].split("\n## ", 1)[0] for head in (CARRIED_SECTION, "## Carried still open")
                        if head in text_all)
    for iid in re.findall(r"^- `([^`]+)`", section, re.M):
        status, rest = items.get(iid, ("missing", ""))
        full = re.search(r"^  - `%s` \*\*[a-z ]+\*\*(.*)$" % re.escape(iid), text_all, re.M)
        rest = full.group(1) if full else rest
        if status in ("done", "dropped") or any(f in rest for f in FOLDED):
            continue
        carried.append({"id": iid, "status": status, "text": PLAIN.get(iid, ""), "his": iid.startswith("his-")})
    days = sorted({m.group(1) for f in os.listdir(PREVIEWS) for m in [re.match(r"^morning-night-(\d{4}-\d\d-\d\d)\.jpg$", f)] if m
                   and all(os.path.exists(os.path.join(PREVIEWS, "morning-%s-%s.jpg" % (v, m.group(1)))) for v in VIEWS)})
    return name, studies, carried, days


LANE = os.path.join(ROOT, "production", "lane")
NEEDED = ("prototype", "joins", "week", "date_move")  # advisor 253: the new layout's keys; a missing one fails the check
STALE_H = 26  # advisor 253: progress.json, or its last publish, over 26 hours old fails the check
PUBLISHED = os.path.join(ROOT, "production", "progress-page", "published.json")


def prototype_now(proto, lane=LANE):
    """THE PROTOTYPE'S TRACK (advisor 254, his words 19 Nov: "1 shot the entire thing", then loops): the 33 rounds are
    replaced by the one-shot (moved to Friday 20 Nov night by advisor 257, after the parts tree) and loops after it. The round is read from the lane's files:
    REVIEWS-loop<n>.md gives 'Loop n', REVIEWS-oneshot.md 'The one-shot'; the panel per review file ('Thumbs up: N of M');
    hours from ROUND-HOURS.md when it is there. BUILD-ORDER's four stages stay as the map, without round numbers."""
    p = dict(proto or {})
    files = os.listdir(lane) if os.path.isdir(lane) else []
    loops = sorted(int(m.group(1)) for f in files for m in [re.match(r"^REVIEWS-loop(\d+)\.md$", f)] if m)
    shot = "REVIEWS-oneshot.md" in files
    p.pop("of", None)
    if loops:
        p["round"], p["round_note"] = "Loop %d" % loops[-1], "the one-shot, then loops; loop %d reviewed" % loops[-1]
    elif shot:
        p["round"], p["round_note"] = "The one-shot", "built in the cloud, reviewed; loops next"
    else:
        p["round"], p["round_note"] = "The one-shot", "Friday night, 20 November, in the cloud, after the parts tree (advisor 257); then loops"
    for s in p.get("stages", []):
        s.pop("rounds", None)
    panel = []
    for key, short, f in ([("one-shot", "1S", "REVIEWS-oneshot.md")] if shot else []) + [
            ("loop %d" % n, "L%d" % n, "REVIEWS-loop%d.md" % n) for n in loops]:
        m = re.search(r"Thumbs up:\s*(\d+)\s+of\s+(\d+)", open(os.path.join(lane, f), encoding="utf-8").read())
        if m:
            panel.append({"round": key, "short": short, "up": int(m.group(1)), "of": int(m.group(2))})
    p["panel"] = panel
    hours = os.path.join(lane, "ROUND-HOURS.md")
    if os.path.exists(hours):
        txt = open(hours, encoding="utf-8").read()
        got = [(k, m.group(1)) for k in ("one-shot",) + tuple("loop %d" % n for n in loops)
               for m in [re.search(r"(?im)^.*%s\D*?([\d.]+)\s*h" % re.escape(k), txt)] if m]
        p["hours"] = {"estimate": "the one-shot about 10 h overnight, then loops",
                      "actual": "; ".join("%s %s h" % kv for kv in got) or "not measured yet"}
    else:
        p["hours"] = {"estimate": "the one-shot about 10 h overnight, then loops", "actual": "not measured yet"}
    return p


def age_hours(stamp, now=None):
    """Hours since a stamp written as 'Thursday 19 November 2026, 18:15 (...)' or ISO; None when unreadable."""
    now = now or datetime.datetime.now()
    m = re.search(r"(\d{1,2}) (\w+) (\d{4}), (\d{1,2}):(\d\d)", stamp or "")
    try:
        t = (datetime.datetime.strptime("%s %s %s %s:%s" % m.groups(), "%d %B %Y %H:%M") if m
             else datetime.datetime.fromisoformat(stamp))
    except (TypeError, ValueError):
        return None
    return (now - t).total_seconds() / 3600.0


def fresh_faults(d, published, now=None):
    """Advisor 253: the page stayed at 17 Nov for two nights because the write ran and no session published. Faults when
    a needed key or a boss's 'blocks' is missing, progress.json's 'updated' is over 26 h old, or its last publish is."""
    out = ["progress.json lacks %s (the new layout's key)" % k for k in NEEDED if k not in d]
    out += ["boss %s has no 'blocks'" % b.get("name") for b in d.get("bosses", []) if not b.get("blocks")]
    a = age_hours(d.get("updated"), now)
    if a is None or a > STALE_H:
        out.append("progress.json was last updated %s, over %d hours ago: run tools/progress_page.py" % (d.get("updated"), STALE_H))
    pa = age_hours((published or {}).get("at"), now)
    if pa is None or pa > STALE_H:
        out.append("the page was last published %s, over %d hours ago: publish production/progress-page with the Artifact "
                   "tool, then run tools/progress_page.py --published" % ((published or {}).get("at"), STALE_H))
    return out


def selftest():
    import tempfile
    ok = []
    with tempfile.TemporaryDirectory() as tmp:
        p = prototype_now({"round": 6, "of": 33, "stages": [{"key": "A", "rounds": [6, 11]}]}, tmp)
        ok.append(p["round"] == "The one-shot" and "of" not in p and "rounds" not in p["stages"][0])
        open(os.path.join(tmp, "REVIEWS-oneshot.md"), "w").write("- Thumbs up: 3 of 8 (x)\n")
        open(os.path.join(tmp, "REVIEWS-loop2.md"), "w").write("- Thumbs up: 5 of 8\n")
        open(os.path.join(tmp, "ROUND-HOURS.md"), "w").write("| one-shot | 9.5 h |\n| loop 2 | 3 h |\n")
        p = prototype_now({}, tmp)
        ok.append(p["round"] == "Loop 2" and [x["up"] for x in p["panel"]] == [3, 5] and "9.5 h" in p["hours"]["actual"])
    now = datetime.datetime(2026, 11, 19, 21, 0)
    good = {k: 1 for k in NEEDED}
    good.update(bosses=[{"name": "T", "blocks": "x"}], updated="Thursday 19 November 2026, 18:15 (note)")
    ok.append(fresh_faults(good, {"at": "2026-11-19T20:00:00"}, now) == [])
    ok.append(any("publish" in f for f in fresh_faults(good, {"at": "2026-11-17T05:13:00"}, now)))
    ok.append(any("updated" in f for f in fresh_faults(dict(good, updated="Tuesday 17 November 2026, 5:13"), {"at": "2026-11-19T20:00:00"}, now)))
    ok.append(any("date_move" in f for f in fresh_faults({k: v for k, v in good.items() if k != "date_move"}, {"at": "2026-11-19T20:00:00"}, now)))
    ok.append(any("blocks" in f for f in fresh_faults(dict(good, bosses=[{"name": "T"}]), {"at": "2026-11-19T20:00:00"}, now)))
    print("progress_page selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


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
    if "--selftest" in argv:
        return selftest()
    path = os.path.join(PAGE, "progress.json")
    d = json.load(open(path, encoding="utf-8"))
    published = json.load(open(PUBLISHED, encoding="utf-8")) if os.path.exists(PUBLISHED) else {}
    if "--published" in argv:
        # the session ran this right after publishing production/progress-page to the page's one link
        import hashlib
        rec = {"at": datetime.datetime.now().isoformat(timespec="minutes"),
               "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()}
        json.dump(rec, open(PUBLISHED, "w", encoding="utf-8"), indent=2)
        print("progress page: publish recorded at %s" % rec["at"])
        return 0
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
        # the forecast (8 Nov, n09-4): stations 1 to 10 carry weeks, 6 to 10 their label, and the forecast block its dates
        fc = d.get("forecast", {})
        for st in d["stations"]:
            if 1 <= st["n"] <= 10 and not st.get("fc_w"):
                print("progress-page FAIL phase %d has no forecast weeks (fc_w)" % st["n"])
                bad.append("forecast")
            if 6 <= st["n"] <= 10 and not st.get("est_label"):
                print("progress-page FAIL phase %d's estimate has no label (est_label)" % st["n"])
                bad.append("forecast")
        if not (fc.get("made") and fc.get("checks") and fc.get("release_target") and "unit_costs" in fc):
            print("progress-page FAIL the forecast block lacks made, checks, release_target or unit_costs")
            bad.append("forecast")
        if missing:
            print("progress-page FAIL morning pictures not on the page: %s" % ", ".join(missing))
        for f in fresh_faults(d, published):
            print("progress-page FAIL " + f)
            bad.append("fresh")
        if d.get("prototype") and d["prototype"] != prototype_now(d["prototype"]):
            print("progress-page FAIL the prototype block disagrees with production/lane's files: run tools/progress_page.py")
            bad.append("prototype")
        # the 2027 line agrees with the stations' own weeks as written (not with today's date, which moves)
        behind = round(sum(st["actual_w"] - st["planned_w"][1] for st in d["stations"] if "actual_w" in st and st.get("planned_w")), 1)
        if d.get("line2027", {}).get("behind_w") != behind:
            print("progress-page FAIL the 2027 line says %s weeks behind, the stations %s: run tools/progress_page.py" % (d.get("line2027", {}).get("behind_w"), behind))
            bad.append("line2027")
        print("progress-page: %d studies, %d carried items, %d days; %s" % (len(studies), len(carried), len(days),
              "FAIL" if bad or missing else "PASS"))
        return 1 if bad or missing else 0
    d.update(want)
    d["prototype"] = prototype_now(d.get("prototype"))
    d.setdefault("date_move", None)
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
    print("NOT YET ON THE PAGE: publish production/progress-page (index.html, progress.json, the pictures above) to "
          "https://claude.ai/artifact/EEcWMTp5E9VqKrQsC8KBdk with the Artifact tool, then run tools/progress_page.py --published")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
