#!/usr/bin/env python3
"""HIS ONE PAGE OF WHAT IS OPEN FOR HIM: "LEDGER: Needs you", at one link that never changes.

    python tools/needs_you_page.py            # writes production/approvals/needs-you/page.json and index.html
    python tools/needs_you_page.py --check    # fails when an item lacks a field, or a link is not a full https link
    python tools/needs_you_page.py --close ID "how"   # he answered or did it: the item is done and leaves the page
    python tools/needs_you_page.py --archive  # each Monday: items done over two days ago move to archive.json, unpublished
    python tools/needs_you_page.py --action-week 2026-11-16   # Monday: every ACTION item since that day, with its reason
    python tools/needs_you_page.py --waiting  # fails when the order's waiting list or the handover's next steps ask him with no open item
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
# A TAG BEFORE EVERY ITEM (his message of 17 Nov 14:38, advisor 199): ACTION (his hands at the PC, a sign-in, a click),
# DECISION (pick an option), REVIEW (look at pictures or frames and judge); stored as "tag", shown first on the page.
TAGS = ("ACTION", "DECISION", "REVIEW")
# HIS HANDS ONLY WHEN NOTHING ELSE CAN (his messages of 17 Nov 16:34 and 16:36, advisors 203 and 204): an open ACTION
# item names in "only_you" exactly one of these reasons and in "tried" one line saying which other routes were tried
# and why each fails; the check refuses it otherwise, and the page shows both under the title.
ONLY_YOU = ("sign-in", "purchase", "licence", "taste", "his-setting")
# A DECISION ONLY WHEN IT IS HIS (his message of 18 Nov 12:13, advisor 221): an open DECISION item names in "kind" one of
# CLAUDE.md's categories he alone decides. His own tools are not licences; deleting something nothing uses, guarded
# by a check, is not his decision either.
DECISION_KINDS = ("money", "sign-in", "hands", "licence-off-list", "canon", "story", "scope", "frame-look", "person-look",
                  "taste", "identity")
PICTURES_REL = "production/approvals/needs-you/pictures"   # an open item's pictures, ignored by git (pictures stay out of it)
# OWN LEFTOVERS NEVER REACH HIS PAGE (his decision, 16 Nov 12:23, advisor 174; RULINGS 29 Oct): an open item asking him
# whether to delete the session's own outputs (test or run outputs, leftovers, temporary files) is refused. An item
# about something genuinely his (his folders, page-approved, bought or unmakeable things) says so with "his_files": true.
DELETE_WORDS = re.compile(r"\b(delete|deleting|deleted|clear|clearing|remove|removing|free up)\b", re.I)
OWN_WORDS = re.compile(r"(working outputs?|leftovers?|tool[- ]tests?|test outputs?|run outputs?|temporary|scratch|"
                       r"Claude made|made itself|Claude's own|its own outputs?|Kiln'?s? (runs?|outputs?))", re.I)
# NO ROUTINE HANDS ON HIS PAGE (advisor 177, his weekly audit of 16 Nov): an open item asking him to install something,
# change a setting or click what the session can do itself is refused. What the app's safety check truly needs from his
# hands says so with "his_hands": true, and open items come in at most two batches a day (RULINGS 8 Nov; a batch is
# the items sharing one 'added' time).
HANDS_WORDS = re.compile(r"\b(install|installing|reinstall|uninstall|change (a|the|its|this) settings?|settings? change|"
                         r"turn (on|off)|switch (on|off)|click|tick|untick|enable|disable)\b", re.I)


PLACEHOLDER = re.compile(r"\b(placeholder|lorem ipsum|TODO|TBD)\b", re.I)


def picture_size(path):
    """(width, height) of a page picture, or None when it cannot be read (films' sprite sheets are not pictures)."""
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


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
        if it.get("state") == "open" and it.get("tag") in TAGS:
            if not it.get("title") or len(it.get("why", [])) > 2 or (it["tag"] == "ACTION" and not it.get("steps")):
                out.append("%s: an open item needs a one-line title, at most two why bullets and, for ACTION, numbered steps (his message 17 Nov 15:48)" % it.get("id"))
        if it.get("state") == "open" and it.get("tag") == "ACTION":
            tried = str(it.get("tried") or "").strip()
            if it.get("only_you") not in ONLY_YOU or not tried or "\n" in tried:
                out.append("%s: an ACTION item needs only_you (one of %s) and tried (one line: the other routes and why "
                           "each fails); his hands only when nothing else can (advisors 203, 204)" % (it.get("id"), ", ".join(ONLY_YOU)))
        if it.get("state") == "open" and it.get("tag") == "DECISION" and it.get("kind") not in DECISION_KINDS:
            out.append("%s: a DECISION item needs kind (one of %s); anything else is decided by the session "
                       "(his message 18 Nov 12:13, advisor 221)" % (it.get("id"), ", ".join(DECISION_KINDS)))
        if it.get("state") == "open" and it.get("tag") not in TAGS:
            out.append("%s lacks its tag (one of %s; his message 17 Nov 14:38)" % (it.get("id"), ", ".join(TAGS)))
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
        if (it.get("state") == "open" and not it.get("his_files") and DELETE_WORDS.search(str(it.get("text", "")))
                and OWN_WORDS.search(str(it.get("text", "")))):
            out.append("%s asks him about deleting the session's own outputs: delete them under RULINGS 29 Oct, one "
                       "DECISIONS line each, no page item (his decision 16 Nov); if they are his, mark his_files" % it.get("id"))
        if it.get("state") == "open" and not it.get("his_hands") and HANDS_WORDS.search(str(it.get("text", ""))):
            out.append("%s asks his hands for an install, a setting or a click: do it yourself; only what the app's "
                       "safety check needs from him goes on the page, marked his_hands (advisor 177)" % it.get("id"))
        for p in it.get("pictures", []) if it.get("state") == "open" else []:
            # the page publishes only files inside the checkout: an open item's pictures live in pictures/ beside it
            src = str(p.get("src", "")).replace("\\", "/")
            if not src.startswith(PICTURES_REL + "/") or not p.get("alt"):
                out.append("%s: picture %r is not under %s/ with its words" % (it.get("id"), src, PICTURES_REL))
            elif check_files and not os.path.isfile(os.path.join(REPO, src)):
                out.append("%s: picture %s is missing" % (it.get("id"), src))
            elif check_files and picture_size(os.path.join(REPO, src)) not in (None, (2560, 1440)):
                # RULINGS 30 Sep: his page's pictures are taken at 2560x1440, never enlarged (advisor 205's backfill)
                out.append("%s: picture %s is %sx%s, not 2560x1440 (RULINGS 30 Sep)" % ((it.get("id"), src) + picture_size(os.path.join(REPO, src))))
        if it.get("state") == "open" and PLACEHOLDER.search(json.dumps(it, ensure_ascii=False)):
            # RULINGS 3 Oct: placeholders meanwhile, never on his page (advisor 205's backfill)
            out.append("%s: a placeholder on his page (RULINGS 3 Oct: never on his page)" % it.get("id"))
    days = {}
    for it in data.get("items", []):
        if it.get("state") == "open":
            added = str(it.get("added", ""))
            days.setdefault(added[:10], set()).add(added)
    for day, times in sorted(days.items()):
        if len(times) > 2:
            out.append("%s: open items came in %d batches (at most two a day, RULINGS 8 Nov; advisor 177)" % (day, len(times)))
    return out


ASKS_HIM = re.compile(r"(one pick for him|his pick (among|between|on|before)|his (one-line )?yes (before|for|on)|needs his yes|"
                      r"for his (yes|pick|answer|tap)|ask(s)? him (for|whether|to)|waits? on his (yes|pick|answer|tap))", re.I)
PHASE_KEPT = re.compile(r"\bK[1-7]\b")


def current_order(repo=None):
    """The newest order in production/orders/ (not its archive)."""
    d = os.path.join(repo or REPO, "production", "orders")
    names = sorted(n for n in os.listdir(d) if re.match(r"\d{4}-\d{2}-\d{2}\.md$", n))
    return os.path.join(d, names[-1]) if names else None


def section_lines(path, starts):
    """The lines under the first heading that starts with any of `starts`, up to the next heading of that level."""
    if not path or not os.path.exists(path):
        return []
    out, inside, level = [], False, 0
    for line in open(path, encoding="utf-8").read().splitlines():
        m = re.match(r"(#+) (.*)", line)
        if m:
            if inside and len(m.group(1)) <= level:
                break
            if any(m.group(2).startswith(s) for s in starts):
                inside, level = True, len(m.group(1))
            continue
        if inside and line.strip():
            out.append(line.strip())
    return out


def waiting_without_item(data, order=None, handover=None):
    open_ids = [x["id"] for x in data["items"] if x.get("state") == "open"]
    order = order or current_order()
    handover = handover or os.path.join(REPO, "production", "handover", "HANDOVER.md")
    found = []
    for where, path, starts in (("order", order, ("3.",)), ("handover", handover, ("Next",))):
        for line in section_lines(path, starts):
            if ASKS_HIM.search(line) and not PHASE_KEPT.search(line) and not any(i in line for i in open_ids):
                found.append((where, line))
    return found


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
        "sections": [{"kind": "need", "key": it["id"], "name": "%s: %s" % (it.get("tag", "?"), it.get("title") or it["text"]),
                      # his message of 17 Nov 15:48 (advisor 200): a one-line title, why in short bullets, steps numbered
                      "why": it.get("why", []), "steps": it.get("steps", []), "links": it["links"],
                      "only_you": it.get("only_you", "") if it.get("tag") == "ACTION" else "",
                      "tried": it.get("tried", "") if it.get("tag") == "ACTION" else "",
                      "recommendation": it["recommendation"], "added": it["added"],
                      "pictures": it.get("pictures", []),
                      # a written piece he rules on, folded shut on the page (8 Nov, the side stories)
                      "detail": it.get("detail", []),
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
                       "recommendation": "Yes.", "state": "open", "tag": "DECISION", "kind": "story", "title": "Pick a.", "why": ["Because."]},
                      {"id": "b", "added": "2026-11-01 07:00", "text": "Did b.", "links": [], "recommendation": "No.", "state": "done",
                       "closed": "2026-11-02 08:00, answered no"}]}
    check("a clean list has no faults", faults(good) == [])
    check("only open items are drawn", [s["key"] for s in spec(good)["sections"]] == ["a"])
    check("the tag comes first on the page", spec(good)["sections"][0]["name"] == "DECISION: Pick a.")
    check("a DECISION without its kind is refused (advisor 221)",
          faults({"items": [dict(good["items"][0], kind=None)]}) != []
          and faults({"items": [dict(good["items"][0], kind="cleanup")]}) != [])
    act = dict(good["items"][0], tag="ACTION", only_you="sign-in", tried="The runner and the gate cannot sign in to Fab for him.")
    check("an ACTION without numbered steps is refused", faults({"items": [dict(act, steps=[])]}) != [])
    check("an ACTION with steps passes and they reach the page",
          faults({"items": [dict(act, steps=["Do it."])]}) == []
          and spec({"items": [dict(act, steps=["Do it."])]})["sections"][0]["steps"] == ["Do it."])
    check("an ACTION without only_you or tried is refused (advisor 204)",
          faults({"items": [dict(act, steps=["Do it."], only_you=None)]}) != []
          and faults({"items": [dict(act, steps=["Do it."], tried="")]}) != [])
    check("an ACTION with another reason is refused", faults({"items": [dict(act, steps=["Do it."], only_you="convenience")]}) != [])
    check("an ACTION's tried must be one line", faults({"items": [dict(act, steps=["Do it."], tried="a\nb")]}) != [])
    check("only_you and tried reach the page under the title",
          spec({"items": [dict(act, steps=["Do it."])]})["sections"][0]["only_you"] == "sign-in"
          and spec({"items": [dict(act, steps=["Do it."])]})["sections"][0]["tried"].startswith("The runner"))
    check("an open item without a tag is refused",
          faults({"items": [dict(good["items"][0], tag=None)]}) != [] and faults({"items": [dict(good["items"][0], tag="ASK")]}) != [])
    check("a link must be a full https link", faults({"items": [dict(good["items"][0], links=[{"label": "A", "url": "fab.com/x"}])]}) != [])
    check("a done item must say when and how it closed", faults({"items": [dict(good["items"][1], closed="")]}) != [])
    check("the tab is his page's name", spec(good)["tab"] == "LEDGER: Needs you")
    pic = dict(good["items"][0], pictures=[{"src": PICTURES_REL + "/hook-day.jpg", "alt": "the hook by day"}])
    check("an open item's pictures reach its section", spec({"items": [pic]})["sections"][0]["pictures"][0]["alt"] == "the hook by day")
    check("a picture outside the page's folder is a fault", faults({"items": [dict(pic, pictures=[{"src": "F:/x.png", "alt": "x"}])]}, check_files=False) != [])
    check("a picture in the page's folder passes", faults({"items": [pic]}, check_files=False) == [])
    check("a placeholder on an open item is refused", faults({"items": [dict(good["items"][0], text="Pick the placeholder name.")]}) != [])
    import tempfile
    from PIL import Image
    tdir = tempfile.mkdtemp()
    small, full = os.path.join(tdir, "s.jpg"), os.path.join(tdir, "f.jpg")
    Image.new("RGB", (1600, 900)).save(small)
    Image.new("RGB", (2560, 1440)).save(full)
    check("picture sizes are read", picture_size(small) == (1600, 900) and picture_size(full) == (2560, 1440))
    d = json.loads(json.dumps(good))
    it = close(d, "a", "answered done", datetime.datetime(2026, 11, 2, 9, 5))
    check("a closed item is done with when and how", it and it["state"] == "done" and it["closed"] == "2026-11-02 09:05, answered done")
    check("a closed item leaves the page", spec(d)["sections"] == [] and faults(d) == [])
    check("closing an unknown or done item changes nothing", close(d, "b", "x") is None and close(d, "zz", "x") is None)
    own = dict(good["items"][0], text="One tap: may Claude delete the working outputs of four finished tool tests (2.5 GB)?")
    check("an item asking to delete own test outputs is refused", faults({"items": [own]}) != [])
    check("the same words on a done item are history, not a fault", faults({"items": [dict(own, state="done", closed="2026-11-16 12:38, x")]}) == [])
    his = dict(good["items"][0], text="May Claude delete C:/LedgerTools/ai-video (26 GB, your dropped video route)?", his_files=True)
    check("an item about his own files, marked his_files, passes", faults({"items": [his]}) == [])
    check("an ordinary ask about a test passes", faults({"items": [dict(good["items"][0], text="Your hands: start the tool test window once.")]}) == [])
    inst = dict(good["items"][0], text="Your hands: install the new driver and change the setting to 60 Hz.")
    check("an item asking him to install or change a setting is refused", faults({"items": [inst]}) != [])
    check("a click the app's safety check needs, marked his_hands, passes", faults({"items": [dict(inst, his_hands=True)]}) == [])
    batch = [dict(good["items"][0], id="t%d" % n, added="2026-11-16 %02d:00" % (8 + n)) for n in range(3)]
    check("three batches of open items in one day are refused", faults({"items": batch}) != [])
    check("two batches in one day pass", faults({"items": batch[:2]}) == [])
    # --waiting (advisor 231): a waiting line asking him needs an open item's id; K1-K7 and past answers pass
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        o, h = os.path.join(td, "order.md"), os.path.join(td, "HANDOVER.md")
        open(o, "w", encoding="utf-8").write("## 2. Week\n- his pick among A and B (not the waiting list)\n"
                                             "## 3. Waiting\n1. A licence: one pick for him with the next order.\n"
                                             "2. A font: one pick for him (font-pick-2026-11-19).\n3. K3: his pick for its phase.\n"
                                             "4. Combat: decided by his pick of 16:02.\n## 4. Decided\n- his yes before X\n")
        open(h, "w", encoding="utf-8").write("## Tried\n- none asks him to\n## Next, in order\n1. ask him for the key\n")
        d = {"items": [{"id": "font-pick-2026-11-19", "state": "open"}]}
        got = waiting_without_item(d, order=o, handover=h)
        check("waiting: only the unmatched order line and the handover's ask", [w for w, _ in got] == ["order", "handover"]
              and got[0][1].startswith("1. A licence") and got[1][1].startswith("1. ask him"))
    print("needs_you_page selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--archive" in a:
        # Each Monday (the advisor's housekeeping of 4 November): items done more than two days ago move to
        # archive.json beside this list, not published; the last two days' stay so his answers stay visible.
        cut = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M")
        data = load()
        old = [x for x in data["items"] if x.get("state") == "done" and x.get("closed", "9")[:16] < cut]
        data["items"] = [x for x in data["items"] if x not in old]
        path = os.path.join(DIR, "archive.json")
        kept = load(path) if os.path.exists(path) else {"about": "Items done more than two days ago, moved from items.json each Monday; not published.", "items": []}
        kept["items"] += old
        for p, d in ((path, kept), (ITEMS, data)):
            with open(p, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(d, fh, indent=1, ensure_ascii=False)
                fh.write("\n")
        print("needs-you: %d archived, %d kept" % (len(old), len(data["items"])))
        sys.exit(build())
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
    if "--action-week" in a:
        # MONDAY'S NUMBERS (advisor 204, point 4): every ACTION item added since the given day, from items.json and
        # archive.json, with its reason and what was tried, for the audit's "only his taps" test.
        since = a[a.index("--action-week") + 1]
        arch = os.path.join(DIR, "archive.json")
        allit = load()["items"] + (load(arch)["items"] if os.path.exists(arch) else [])
        rows = [x for x in allit if x.get("tag") == "ACTION" and str(x.get("added", "")) >= since]
        for x in sorted(rows, key=lambda r: r["added"]):
            print("%s | %s | only_you=%s | tried=%s | %s" % (x["added"], x["id"], x.get("only_you", "none (before 17 Nov 16:50)"),
                                                          x.get("tried", "-"), x.get("closed", "open")))
        print("action items since %s: %d" % (since, len(rows)))
        sys.exit(0)
    if "--waiting" in a:
        # NOTHING WAITS ON HIM OFF HIS PAGE (advisor 231, his question of 18 Nov 21:10, "why didn't this come to my needs
        # you page"): every line of the current order's waiting list or the handover's next steps that still asks for
        # his yes, pick or answer must name an open page item by its id; his phase-kept items (K1 to K7) are exempt.
        hits = waiting_without_item(load())
        for where, line in hits:
            print("needs-you WAITING %s: %s" % (where, line[:160]))
        print("needs-you waiting: %d line(s) asking him with no open page item" % len(hits))
        sys.exit(1 if hits else 0)
    if "--check" in a:
        f = faults(load())
        for x in f:
            print("needs-you FAIL " + x)
        print("needs-you: %d fault(s)" % len(f))
        sys.exit(1 if f else 0)
    sys.exit(build())
