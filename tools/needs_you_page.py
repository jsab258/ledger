#!/usr/bin/env python3
"""HIS ONE PAGE OF WHAT IS OPEN FOR HIM: "LEDGER: Needs you", at one link that never changes.

    python tools/needs_you_page.py            # writes production/approvals/needs-you/page.json and index.html
    python tools/needs_you_page.py --check    # fails when an item lacks a field, or a link is not a full https link
    python tools/needs_you_page.py --close ID "how"   # he answered or did it: the item is done and leaves the page
    python tools/needs_you_page.py --selftest

WHY, 2 November 2026. Jafar: "make one permanent page, 'LEDGER: Needs you', in the same format as your decision
pages, at one link that never changes. It replaces the daily decision pages for good. It lists only what is open for
me, each item with: what to do in one line, every link it needs, your recommendation, and the date and time it was
added. An item leaves the page when I have answered it or done it. Keep the items also as a plain list in the page's
data (id, added, text, links, recommendation, open or done) so the advisor's hourly checker can read it."

THE HOME of the items is production/approvals/needs-you/items.json (one per thing he is asked; state "open" or
"done"; done items stay in the list with when and how they closed, and leave the page). The page is drawn by
tools/day_page.py (kind "need") from the open ones; items.json is published beside it, and copied into the page's
database (collection "items"), so a checker can read either. His picks are stored as the decision pages' are
(verdicts/<id>); they are read before anything about the page is asked again.
"""
import datetime
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(REPO, "production", "approvals", "needs-you")
ITEMS = os.path.join(DIR, "items.json")
URL = "https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8"   # his one permanent link (published 2 November 2026)
FIELDS = ("id", "added", "text", "links", "recommendation", "state")
PICTURES_REL = "production/approvals/needs-you/pictures"   # an open item's pictures, ignored by git (pictures stay out of it)


def load(path=ITEMS):
    return json.load(open(path, encoding="utf-8"))


def faults(data, check_files=True):
    out = []
    seen = set()
    for it in data.get("items", []):
        for f in FIELDS:
            if f not in it:
                out.append("%s lacks %s" % (it.get("id", "?"), f))
        if it.get("id") in seen:
            out.append("%s appears twice" % it.get("id"))
        seen.add(it.get("id"))
        if it.get("state") not in ("open", "done"):
            out.append("%s has state %r (open or done)" % (it.get("id"), it.get("state")))
        if not re.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d$", str(it.get("added", ""))):
            out.append("%s: added is not 'YYYY-MM-DD HH:MM'" % it.get("id"))
        for l in it.get("links", []):
            if not str(l.get("url", "")).startswith("https://"):
                out.append("%s: link %r is not a full https link" % (it.get("id"), l.get("url")))
        if it.get("state") == "done" and not it.get("closed"):
            out.append("%s is done with no 'closed' (when, and how)" % it.get("id"))
        for p in it.get("pictures", []) if it.get("state") == "open" else []:
            # the page publishes only files inside the checkout: an open item's pictures live in pictures/ beside it
            src = str(p.get("src", "")).replace("\\", "/")
            if not src.startswith(PICTURES_REL + "/") or not p.get("alt"):
                out.append("%s: picture %r is not under %s/ with its words" % (it.get("id"), src, PICTURES_REL))
            elif check_files and not os.path.isfile(os.path.join(REPO, src)):
                out.append("%s: picture %s is missing" % (it.get("id"), src))
    return out


def close(data, item_id, how, now=None):
    """Marks one open item done, with when and how; returns the item, or None if no open item has that id."""
    now = now or datetime.datetime.now()
    for it in data["items"]:
        if it["id"] == item_id and it["state"] == "open":
            it["state"] = "done"
            it["closed"] = "%s, %s" % (now.strftime("%Y-%m-%d %H:%M"), how)
            return it
    return None


def spec(data, now=None):
    now = now or datetime.datetime.now()
    open_items = [it for it in data["items"] if it["state"] == "open"]
    when = now.strftime("%A %d %B, %H:%M").replace(" 0", " ")
    return {
        "tab": "LEDGER: Needs you",
        "kicker": "LEDGER · Needs you · %d open · updated %s" % (len(open_items), when),
        "title": "Needs you",
        "how": ["Only what is open for you, oldest first. Each item says what to do, links everything it needs, and gives my recommendation. It leaves this page once you have answered it here or done it.",
                "Nothing open: the page says so." if not open_items else "Pick an answer under each item; a note is optional."],
        "foot": "One page, one link, kept current (his order of 2 November). The same list is kept as plain data beside it (items.json) for the advisor's checker.",
        # an item may carry pictures, judged on the page itself at full size (a whole street frame or a person at its
        # gate, 3 November: the corner's midweek page is the first); their files sit in pictures/ beside the page, out of git
        "sections": [{"kind": "need", "key": it["id"], "name": it["text"], "links": it["links"],
                      "recommendation": it["recommendation"], "added": it["added"],
                      "pictures": it.get("pictures", []),
                      "options": it.get("options", [["done", "Done"]])} for it in sorted(open_items, key=lambda x: x["added"])],
    }


def build():
    data = load()
    bad = faults(data)
    if bad:
        for b in bad:
            print("needs-you FAIL " + b)
        return 1
    with open(os.path.join(DIR, "page.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(spec(data), fh, indent=1, ensure_ascii=False)
    sys.path.insert(0, os.path.join(REPO, "tools"))
    import day_page
    rc = day_page.build(os.path.join(DIR, "page.json"))
    print("needs-you: %d open, %d done" % (sum(1 for i in data["items"] if i["state"] == "open"), sum(1 for i in data["items"] if i["state"] == "done")))
    return rc


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("needs_you_page selftest FAIL " + name)
    good = {"items": [{"id": "a", "added": "2026-11-02 07:00", "text": "Do a.", "links": [{"label": "A", "url": "https://x.y/a"}],
                       "recommendation": "Yes.", "state": "open"},
                      {"id": "b", "added": "2026-11-01 07:00", "text": "Did b.", "links": [], "recommendation": "No.", "state": "done",
                       "closed": "2026-11-02 08:00, answered no"}]}
    check("a clean list has no faults", faults(good) == [])
    check("only open items are drawn", [s["key"] for s in spec(good)["sections"]] == ["a"])
    check("a link must be a full https link", faults({"items": [dict(good["items"][0], links=[{"label": "A", "url": "fab.com/x"}])]}) != [])
    check("a done item must say when and how it closed", faults({"items": [dict(good["items"][1], closed="")]}) != [])
    check("the tab is his page's name", spec(good)["tab"] == "LEDGER: Needs you")
    pic = dict(good["items"][0], pictures=[{"src": PICTURES_REL + "/hook-day.jpg", "alt": "the hook by day"}])
    check("an open item's pictures reach its section", spec({"items": [pic]})["sections"][0]["pictures"][0]["alt"] == "the hook by day")
    check("a picture outside the page's folder is a fault", faults({"items": [dict(pic, pictures=[{"src": "F:/x.png", "alt": "x"}])]}, check_files=False) != [])
    check("a picture in the page's folder passes", faults({"items": [pic]}, check_files=False) == [])
    d = json.loads(json.dumps(good))
    it = close(d, "a", "answered done", datetime.datetime(2026, 11, 2, 9, 5))
    check("a closed item is done with when and how", it and it["state"] == "done" and it["closed"] == "2026-11-02 09:05, answered done")
    check("a closed item leaves the page", spec(d)["sections"] == [] and faults(d) == [])
    check("closing an unknown or done item changes nothing", close(d, "b", "x") is None and close(d, "zz", "x") is None)
    print("needs_you_page selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--close" in a:
        i = a.index("--close")
        data = load()
        if not close(data, a[i + 1], a[i + 2]):
            print("needs-you: no open item %s" % a[i + 1])
            sys.exit(1)
        with open(ITEMS, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(data, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
        sys.exit(build())
    if "--check" in a:
        f = faults(load())
        for x in f:
            print("needs-you FAIL " + x)
        print("needs-you: %d fault(s)" % len(f))
        sys.exit(1 if f else 0)
    sys.exit(build())
