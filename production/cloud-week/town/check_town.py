#!/usr/bin/env python3
"""check_town.py: the checks on people.json (unit 11, cloud week 42). Standard library only, light.

    python3 production/cloud-week/town/check_town.py

Writes checks/check_v1.json and prints "N of M rows pass". Exit 0 when every row passes, else 1.

It is written apart from build_people.py: it re-reads every home (the casting sheets, the story documents,
StreetFacts.cs, hook-cast.json) and does not trust what the builder said about them.

What each row says, in plain words:
  cast       every person in canon's cast and the regulars list has an entry, and nobody else does
  facts      every sourced fact is word for word in the lines it cites; derived facts are re-derived from
             hook-cast.json and equal; every new fact has a group that DECISIONS.md names, marked for Jafar
  schedule   derived from hook-cast.json and equal to it; proposals use known places, cover the day and keep
             to the shop hours of the place they stand in
  talks_to   the ties are hook-cast.json's, the hours a week are recomputed from the routines
  rumours    exactly five; each rests on the person's own facts; told only to people they actually meet;
             the RULINGS limits hold (witness sureness, the fire's truth, Mickey, the heart)
  questions  exactly ten (Tom's are the player's own words: none); answers under 30 words, drawn only from
             the person's own facts, no secret told to a stranger, no invented specific (a name, a number)
  content    tools/content-gate.py and tools/canon-gate.py over the text, and word lists for children, real
             names and places, the era, the old names, Tom's name, Mickey and the fire's truth
Words are checked by lists: a screen, not a reader. NOTES.md lists the canon checks made by hand.
"""
import importlib.util
import json
import re
import subprocess
import sys
sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PEOPLE = HERE / "people.json"
OUT = HERE / "checks" / "check_v1.json"

rows = []


def row(rid, what, ok, detail=""):
    rows.append({"id": rid, "what": what, "pass": bool(ok), "detail": detail if not ok else (detail or "")})


def fold(s):
    return " ".join(s.split())


_lines_cache = {}


def lines_of(path):
    if path not in _lines_cache:
        p = REPO / path
        _lines_cache[path] = p.read_text(encoding="utf-8").split("\n") if p.exists() else None
    return _lines_cache[path]


def quote_at(path, a, b, quote):
    L = lines_of(path)
    if L is None or not (1 <= a <= b <= len(L)):
        return False
    return fold(quote) in fold(" ".join(L[a - 1:b]))


def words(s):
    return re.findall(r"[a-z0-9']+", s.lower())


# ------------------------------------------------------------------ the homes, read afresh

HK = json.loads((REPO / "production/specs/hook-cast.json").read_text(encoding="utf-8"))
HKP = {p["id"]: p for p in HK["people"]}
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
RANGE = HK["talk_range_m"]


def hk_segments(pid, day):
    p = HKP[pid]
    r = sorted((float(h), pl) for h, pl in (p.get("days", {}).get(day) or p["routine"]))
    out = []
    for i, (h, pl) in enumerate(r):
        out.append([h, r[i + 1][0] if i + 1 < len(r) else 24.0, pl])
    if out and out[0][0] > 0:
        out.insert(0, [0.0, out[0][0], r[-1][1]])
    m = []
    for s in out:
        if m and m[-1][2] == s[2]:
            m[-1][1] = s[1]
        else:
            m.append(s)
    return m


def hhmm(h):
    h = float(h)
    return "%02d:%02d" % (int(h), round((h - int(h)) * 60))


def to_h(x):
    a, b = x.split(":")
    return int(a) + int(b) / 60.0


def place_xy(pl):
    p = HK["places"].get(pl)
    return (p["x_m"], p["z_m"]) if p else None


def together(sa, sb):
    """sa, sb: day -> [(from, to, place)]; hours a week within the talking range."""
    t = 0
    for d in DAYS:
        for h in range(24):
            pa = next((s[2] for s in sa[d] if s[0] <= h < s[1]), "off")
            pb = next((s[2] for s in sb[d] if s[0] <= h < s[1]), "off")
            xa, xb = place_xy(pa), place_xy(pb)
            if xa and xb and ((xa[0] - xb[0]) ** 2 + (xa[1] - xb[1]) ** 2) ** 0.5 <= RANGE:
                t += 1
    return t


def stored_days(sched):
    out = {}
    for d in DAYS:
        lst = sched["saturday"] if d == "sat" else sched["sunday"] if d == "sun" else sched.get("weekday_differs", {}).get(d) or sched["weekday"]
        out[d] = [(to_h(s["from"]), to_h(s["to"]), s["place"]) for s in lst]
    return out


def hk_days(pid):
    return {d: hk_segments(pid, d) for d in DAYS}


def render_hours(area):
    a = HK["areas"][area]
    hrs = a.get("hours", {})
    groups = []
    for d in DAYS:
        if d in hrs:
            span = tuple(hrs[d])
            if groups and groups[-1][1] == span and DAYS.index(groups[-1][0][-1]) == DAYS.index(d) - 1:
                groups[-1][0].append(d)
            else:
                groups.append(([d], span))
    parts = []
    for ds, span in groups:
        lab = ds[0] if len(ds) == 1 else ds[0] + " to " + ds[-1]
        parts.append("%s %s-%s" % (lab, hhmm(span[0]), hhmm(span[1] if span[1] <= 24 else span[1] - 24)))
    if a.get("hours_note"):
        parts.append(a["hours_note"])
    return "%s: %s" % (a["names"][0], "; ".join(parts))


def render_day(pid):
    def fmt(segs):
        bits = ["%s to %s %s" % (hhmm(a), hhmm(b) if b < 24 else "24:00", "away" if pl == "off" else HK["places"][pl]["said"]) for a, b, pl in segs if pl != "off"]
        return ", then ".join(bits) if bits else "not on the street"
    return "Monday: %s. Saturday: %s. Sunday: %s." % (fmt(hk_segments(pid, "mon")), fmt(hk_segments(pid, "sat")), fmt(hk_segments(pid, "sun")))


def hk_ties():
    lines = lines_of("production/specs/hook-cast.json")
    start = next(i for i, l in enumerate(lines) if l.startswith(' "ties": ['))
    out, i = [], start + 1
    while i < len(lines):
        if lines[i] == "  [":
            vals = [json.loads(lines[i + k].strip().rstrip(",")) for k in (1, 2, 3, 4)]
            out.append((i + 1, vals))
            i += 6
        else:
            i += 1
    return out


# ------------------------------------------------------------------ the gates

def load_content_gate():
    spec = importlib.util.spec_from_file_location("_cg", REPO / "tools" / "content-gate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def real_world_lists():
    src = (REPO / "ledger/Assets/Scripts/Core/RealWorld.cs").read_text(encoding="utf-8")
    def arr(name):
        a = src.index("static readonly string[] %s" % name)
        b = src.index("};", a)
        block = re.sub(r"//[^\n]*", "", src[a:b])
        return re.findall(r'"([^"]+)"', block)
    return arr("AnyCase"), arr("AsName")


# real places the live-talk list does not name, found in the casting and research text of this project
EXTRA_PLACES = ["hull", "grimsby", "humberside", "hessle", "humber", "cleethorpes", "scunthorpe", "yorkshire", "lincolnshire", "east riding",
                "copper row at", "downtown"]
CHILD_WORDS = r"\b(child|children|kid|kids|baby|babies|boy|boys|girl|girls|lad|lads|lass|lasses|infant|toddler|pupil|pupils|schoolboy|schoolgirl|nursery|little ones?|young ones?|teenager|teenagers|youngster|youngsters)\b|(?<!grammar )\bschools?\b(?! stands closed)"
OLD_NAMES = r"\b(Lena|Rocco|Aldous|Vane|Sera|Kest|Noor|Elias|Novak|Toma|Father Emil|Mara|Sam|Danny Ro|Halvard|Zlata|Ferko|Marla|Dusan|Joey|Victor|Tibor|Vesna|Magda|Zora|Iva|Selma|Tanja|Stipe|Fabjan|Goran|Tomas|Luka|Bruno|Petra|Dario|Sanja|Hana|Franjo|Danica|Drago|Filip|Katarina|Ines|Marta|Jelena)\b"
FIRE_TRUTH = r"outfit|burned him out|burnt him out|as a lesson|found them the men|page in|tying it|seal of confession|confess"
FOUL = r"murder|killed|poison|foul play|stabbed|shot|pushed him|suspicious death|not natural"
MICKEY_DESC = r"\bMickey(?:'s)? (?:was|used to|liked|loved|hated|would|always|never|kept|ran|owed|thought|wanted|said|told|had a)\b"
DK = re.compile(r"that's all i know|no idea|couldn't (?:tell|say)|wouldn't (?:like to )?(?:say|know)|didn't know|don't know|can't say|never really knew|not that i've found|not to me", re.I)
NUMW = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
        "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100, "thousand": 1000}
DAYWORD = {"monday": "mon", "tuesday": "tue", "wednesday": "wed", "thursday": "thu", "friday": "fri", "saturday": "sat", "sunday": "sun"}
SHOP_EXCEPT = {("zora", "laundry_counter"): "REGULARS.md row 13: still on the early shift; the steam laundry is a works, which runs before its counter opens"}
OK_CAPS = {"I", "Mickey", "Mr", "Mrs", "Miss", "Mickey's"}


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]


def specifics_ok(answer, allowed_text):
    """Every capitalised word (not opening a sentence) and every number in an answer is in what it draws on."""
    allowed = fold(allowed_text).lower()
    allowed_tokens = set(words(allowed_text))
    ints = {int(x) for x in re.findall(r"\d+", allowed_text)}
    bad = []
    for sent in sentences(answer):
        toks = re.findall(r"[A-Za-z][A-Za-z']*|\d+", sent)
        for i, w in enumerate(toks):
            base = re.sub(r"'s$", "", w)
            if w.isdigit():
                n = int(w)
                if n not in ints and n + 12 not in ints:
                    bad.append(w)
                continue
            lw = base.lower()
            if base == "I" or base.startswith("I'"):
                continue
            if lw.endswith("s") and lw[:-1] in DAYWORD:
                lw = lw[:-1]
            if lw in NUMW:
                n = NUMW[lw]
                if lw not in allowed_tokens and n not in ints and n + 12 not in ints:
                    bad.append(w)
                continue
            if i > 0 and base[0].isupper() and base not in OK_CAPS:
                if lw in DAYWORD:
                    if DAYWORD[lw] in allowed_tokens or lw in allowed_tokens or (lw + "s") in allowed_tokens:
                        continue
                    bad.append(w)
                    continue
                stem = lw.rstrip("s") if lw.endswith("s") and lw[:-1] in allowed_tokens else lw
                if stem not in allowed_tokens and lw not in allowed_tokens and lw not in allowed:
                    bad.append(w)
    return bad


# ------------------------------------------------------------------ main

def run(doc, full=True):
    """All the rows over one people.json document. `full` also runs the git and canon-gate checks (not for seeded faults)."""
    rows.clear()
    people = doc["people"]
    byid = {p["id"]: p for p in people}
    groups = doc["groups"]

    # ---- the cast, read from the homes
    casting = lines_of("production/casting/CASTING.md")
    exp_principals = []
    in_table = False
    for l in casting:
        if l.startswith("## "):
            in_table = l.startswith("## The fourteen principals")
        m = re.match(r"\| \*\*(.+?)\*\* \| (about )?(\d+) \|", l)
        if in_table and m:
            exp_principals.append(m.group(1))
    reg_lines = lines_of("production/casting/regulars/REGULARS.md")
    exp_regs = {}
    for l in reg_lines:
        if l.startswith("| ") and l.count("|") >= 10 and l.split("|")[1].strip().isdigit():
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            exp_regs[c[1]] = (c[2], int(c[3]))
    row("cast.principals_listed", "CASTING.md lists fourteen principals", len(exp_principals) == 14, str(len(exp_principals)))
    row("cast.regulars_listed", "REGULARS.md lists thirty regulars", len(exp_regs) == 30, str(len(exp_regs)))

    def surname(n):
        n = re.sub(r'^DS ', "", n)
        n = n.split(",")[0].replace('"', "").strip()
        return n.split()[-1] if " " in n else n
    entry_by_surname = {}
    for p in people:
        entry_by_surname.setdefault(surname(p["name"]), []).append(p["id"])
    for n in exp_principals:
        s = surname(n)
        row("cast.principal." + s, "principal %s has an entry" % n, s in entry_by_surname and any(byid[i]["tier"] == "principal" for i in entry_by_surname[s]))
    for rid, (name, age) in exp_regs.items():
        e = byid.get(rid)
        row("cast.regular." + rid, "regular %s (%s) has an entry with that name and age" % (rid, name),
            bool(e) and e["tier"] == "regular" and name.split(" (")[0].split()[0] in e["name"] and e["age"] == age,
            "" if e else "missing")
    extra = [p["id"] for p in people if (p["tier"] == "regular" and p["id"] not in exp_regs) or (p["tier"] == "principal" and surname(p["name"]) not in {surname(n) for n in exp_principals})]
    row("cast.no_extra", "nobody else has an entry", not extra and len(people) == 44, "extra %s; entries %d" % (extra, len(people)))

    # ---- DECISIONS.md: appended only, one entry per group, marked for Jafar
    dec = (REPO / "DECISIONS.md").read_text(encoding="utf-8")
    mine = [l for l in dec.split("\n") if "(cloud week 42, unit 11)" in l]
    used_groups = sorted({f["new"] for p in people for f in p["facts"] if f.get("new")} | ({"N-RUMOURS"} if any(p["rumours"] for p in people) else set())
                         | ({"N-ANSWERS"} if any(p["newcomer_questions"] for p in people) else set())
                         | ({"N-SCHEDULES"} if any(p["schedule"].get("source", {}).get("new") for p in people) else set())
                         | ({"N-MICKEY"} if any(p["knew_mickey"] for p in people) else set()))
    for g in used_groups:
        if g not in groups:
            row("decisions." + g, "the group %s is defined in people.json" % g, False, "undefined group")
            continue
        key = groups[g]["decisions_key"]
        hit = [l for l in mine if key in l]
        row("decisions." + g, "DECISIONS.md has one entry for %s, ending 'Marked for Jafar.'" % g,
            len(hit) == 1 and hit[0].rstrip().endswith("Marked for Jafar.") and re.match(r"- 13 Oct \d\d:\d\d \(cloud week 42, unit 11\): ", hit[0]) and "Reason:" in hit[0] and "Link:" in hit[0],
            "%d entries" % len(hit))
    row("decisions.only_mine_new", "every unit 11 line in DECISIONS.md belongs to a group", len(mine) == len(used_groups), "%d lines, %d groups" % (len(mine), len(used_groups)))
    if full:
        try:
            first = subprocess.run(["git", "log", "-S(cloud week 42, unit 11)", "--format=%H", "--", "DECISIONS.md"], cwd=REPO, capture_output=True, text=True, timeout=60).stdout.split()
            base = (first[-1] + "^") if first else "HEAD"
            ns = subprocess.run(["git", "diff", "--numstat", base, "--", "DECISIONS.md"], cwd=REPO, capture_output=True, text=True, timeout=60).stdout.split()
            removed = int(ns[1]) if len(ns) >= 2 else 0
            row("decisions.append_only", "DECISIONS.md has no removed or changed line since before unit 11's entries (against %s)" % base[:9], removed == 0, "removed lines: %d" % removed)
        except Exception as e:  # noqa: BLE001
            row("decisions.append_only", "DECISIONS.md has no removed or changed line against HEAD", False, str(e))

    # ---- per person
    cg = get_gate()
    any_case, as_name = get_real()
    any_rx = re.compile(r"(?<![\w'])(" + "|".join(sorted((re.escape(x) for x in any_case), key=len, reverse=True)) + r")(?![\w-])", re.I)
    name_rx = re.compile(r"(?<![\w'])(" + "|".join(re.escape(x) for x in as_name) + r")(?![\w-])")
    place_rx = re.compile(r"(?<![\w'])(" + "|".join(re.escape(x) for x in EXTRA_PLACES) + r")(?![\w-])", re.I)
    approved_mickey = set()
    for sid in ("mickey_counsel", "mickey_kept_ron"):
        s = doc["street_facts"][sid]["text"]
        approved_mickey.add(fold(s).lower())
    sf_src = lines_of("ledger/Assets/Scripts/Core/StreetFacts.cs")
    for l in sf_src:
        for m in re.finditer(r'"([^"]*Mickey kept[^"]*)"', l):
            for s in sentences(m.group(1)):
                approved_mickey.add(fold(s).lower())

    written_texts = []   # (person, where, text) of written (not carried) text for the content rows
    carried_texts = []
    all_ids_ok = True

    def check_person(p):
        pid = p["id"]
        facts = p["facts"]
        fids = {f["id"] for f in facts}
        secret = {f["id"] for f in facts if f.get("secret")}
        ftext = {f["id"]: f["text"] for f in facts}

        # identity
        isrc = p["identity_src"]
        itext = fold(" ".join((lines_of(isrc["file"]) or [""])[isrc["line"] - 1:isrc["end"]]))
        age_ok = str(p["age"]) in itext
        ok_id = all(tok in itext for tok in [p["name"].split()[0] if not p["name"].startswith("Father") else "Brendan", surname(p["name"])]) and age_ok
        row("%s.identity" % pid, "%s: name and age are on the cited casting line" % pid, ok_id, itext[:120])

        # ids
        ids_unique = len(fids) == len(facts)
        row("%s.ids" % pid, "%s: fact ids are unique" % pid, ids_unique)

        # sourced facts verbatim, derived re-derived, new marked
        bad = []
        n_src = n_der = n_new = 0
        for f in facts:
            if f.get("street") and not f.get("src"):
                n_src += 1
                if f["text"] != doc["street_facts"].get(f["street"], {}).get("text"):
                    bad.append("%s street fact differs from the table" % f["id"])
                carried_texts.append((pid, f["id"], f["text"]))
            elif f.get("src"):
                n_src += 1
                s = f["src"]
                if not quote_at(s["file"], s["line"], s["end"], f["text"]):
                    bad.append("%s: not at %s:%s" % (f["id"], s["file"], s["line"]))
                carried_texts.append((pid, f["id"], f["text"]))
            elif f.get("derived"):
                n_der += 1
                d = f["derived"]
                if d["how"] == "day":
                    ok = f["text"] == render_day(pid) and lines_of(d["file"])[d["line"] - 1].strip() == '"id": "%s",' % pid
                elif d["how"] == "hours":
                    ok = f["text"] == render_hours(d["area"]) and lines_of(d["file"])[d["line"] - 1].startswith('  "%s": {' % d["area"])
                else:
                    ok = False
                if not ok:
                    bad.append("%s derived text differs from hook-cast.json" % f["id"])
            elif f.get("new"):
                n_new += 1
                if f["new"] not in groups or not f.get("why"):
                    bad.append("%s new without group or reason" % f["id"])
                written_texts.append((pid, f["id"], f["text"]))
            else:
                bad.append("%s has no source, no derivation and is not marked new" % f["id"])
            if f["kind"] == "believes":
                if f.get("truth") not in ("true", "false", "unknown", "partly") or not f.get("truth_basis"):
                    bad.append("%s belief without truth or basis" % f["id"])
                tb = f.get("truth_basis") or {}
                if tb.get("src") and not (lines_of(tb["src"]["file"]) and 1 <= tb["src"]["line"] <= len(lines_of(tb["src"]["file"]))):
                    bad.append("%s truth basis line missing" % f["id"])
            if f["kind"] == "saw" and not f.get("when"):
                bad.append("%s saw without when" % f["id"])
        row("%s.facts" % pid, "%s: %d facts: %d cite a line that holds their words, %d derived and equal to the home, %d new and marked" % (pid, len(facts), n_src, n_der, n_new), not bad, "; ".join(bad[:4]))

        # who_ facts equal hook-cast 'called'
        wb = []
        for f in facts:
            m = re.match(r"who (\S+) is, as the home describes them", f.get("via", ""))
            if m:
                other = m.group(1)
                if other not in HKP or HKP[other]["called"] != f["text"]:
                    wb.append(f["id"])
        row("%s.who" % pid, "%s: what they know of who each tie is equals hook-cast.json's description" % pid, not wb, str(wb))

        # schedule
        sc = p["schedule"]
        if p.get("tom_exception"):
            row("%s.schedule" % pid, "%s: the player's own schedule is not authored" % pid, sc.get("player_controlled") is True)
        else:
            sd = stored_days(sc)
            contiguous = True
            for d in DAYS:
                segs = sd[d]
                if not segs or abs(segs[0][0]) > 1e-6 or abs(segs[-1][1] - 24) > 1e-6 or any(abs(segs[i][1] - segs[i + 1][0]) > 1e-6 for i in range(len(segs) - 1)):
                    contiguous = False
            places_ok = all(s[2] == "off" or s[2] in HK["places"] or s[2] in doc["proposed_places"] for d in DAYS for s in sd[d])
            if pid in HKP and not sc.get("overrides"):
                same = all([tuple(x) for x in hk_segments(pid, d)] == [tuple(x) for x in sd[d]] for d in DAYS)
                row("%s.schedule" % pid, "%s: schedule equals the routine in hook-cast.json for every weekday" % pid, same and contiguous and places_ok)
            elif pid in HKP:
                row("%s.schedule" % pid, "%s: a proposal that replaces hook-cast.json's routine says why" % pid, contiguous and places_ok and bool(sc["overrides"].get("why")))
            else:
                row("%s.schedule" % pid, "%s: a proposed schedule (no routine in hook-cast.json) covers each day and uses known places" % pid,
                    contiguous and places_ok and sc.get("source", {}).get("new") == "N-SCHEDULES")
            # shop hours: inside a place whose area has hours, only within them (an hour either side for opening up and clearing)
            viol = []
            for d in DAYS:
                for a, b, pl in sd[d]:
                    if pl not in HK["places"] or not HK["places"][pl].get("inside"):
                        continue
                    if (pid, pl) in SHOP_EXCEPT:
                        continue
                    for area in HK["areas"].values():
                        if pl in area.get("places", []) and area.get("hours"):
                            hrs = area["hours"].get(d)
                            lo, hi = (hrs[0] - 1, hrs[1] + 1) if hrs else (None, None)
                            rest = area.get("hours_breaks", {}).get(d, [])
                            if hrs is None or a < lo - 1e-6 or b > hi + 1e-6:
                                # night routines past 24 are the next morning's
                                if hrs is not None and hrs[1] > 24 and a >= 0 and b <= hrs[1] - 24 + 1:
                                    continue
                                if hrs is not None and hrs[1] > 24 and a >= lo and b <= 24:
                                    continue
                                if hrs is not None and hrs[1] > 24:
                                    prev = area["hours"].get(DAYS[(DAYS.index(d) - 1) % 7])
                                    if prev and prev[1] > 24 and a >= 0 and b <= prev[1] - 24 + 1:
                                        continue
                                viol.append("%s %s %s-%s in %s (open %s)" % (pid, d, hhmm(a), hhmm(b), pl, hrs))
            row("%s.shop_hours" % pid, "%s: inside a shop or the cafe only in its opening hours" % pid, not viol, "; ".join(viol[:3]))

        # talks_to
        ties = p["talks_to"]
        tids = {t["who"] for t in ties}
        if pid in HKP:
            exp = {}
            for line, (a, b, w, txt) in hk_ties():
                if pid in (a, b):
                    exp.setdefault(b if a == pid else a, (w, line))
            got = {t["who"]: (t["weight"], t["source"]["line"]) for t in ties if t.get("weight") is not None}
            okset = set(exp) == set(got) and all(exp[k][0] == got[k][0] and exp[k][1] == got[k][1] for k in exp)
            row("%s.ties" % pid, "%s: who they talk to equals hook-cast.json's ties (weight and line)" % pid, okset, "expected %s got %s" % (sorted(exp), sorted(got)))
            hb = []
            mine_days = stored_days(sc)
            for t in ties:
                if t["who"] in HKP and t.get("weight") is not None:
                    h = together(mine_days, hk_days(t["who"]))
                    if t.get("hours_a_week") != h:
                        hb.append("%s %s vs %s" % (t["who"], t.get("hours_a_week"), h))
            row("%s.ties_hours" % pid, "%s: hours a week with each tie are recomputed from the schedules" % pid, not hb, "; ".join(hb[:3]))
        elif not p.get("tom_exception"):
            sd = stored_days(sc)
            hb = []
            for t in ties:
                if t.get("computed") or t["source"].get("computed"):
                    h = together(sd, hk_days(t["who"]))
                    if t.get("hours_a_week") != h:
                        hb.append("%s %s vs %s" % (t["who"], t.get("hours_a_week"), h))
            tie_src_bad = []
            for t in ties:
                s = t["source"]
                if s.get("computed"):
                    continue
                if not (lines_of(s["file"]) and 1 <= s["line"] <= s.get("end", s["line"]) <= len(lines_of(s["file"]))):
                    tie_src_bad.append(t["who"])
                    continue
                txt = fold(" ".join(lines_of(s["file"])[s["line"] - 1:s.get("end", s["line"])])).lower()
                other = byid.get(t["who"])
                toks = {surname(other["name"]).lower(), other["heard_as"].lower().split()[-1], other["name"].split()[0].lower()}
                role = (other["role"]["text"] if other else "").lower()
                toks |= {w for w in re.findall(r"[a-z]{6,}", role)}
                toks |= {surname(p["name"]).lower(), p["heard_as"].lower().split()[-1], other["id"].lower(), pid.lower()}
                if not any(k in txt for k in toks):
                    tie_src_bad.append(t["who"])
            row("%s.ties" % pid, "%s: proposed ties cite a line that names the other person, or are computed from the schedules" % pid, not hb and not tie_src_bad, "%s %s" % (hb[:3], tie_src_bad[:3]))
        else:
            tb = [t["who"] for t in ties if not (lines_of(t["source"]["file"]) and t["source"]["line"] <= len(lines_of(t["source"]["file"])))]
            row("%s.ties" % pid, "%s: the people who first knew him cite a line" % pid, not tb)

        # rumours
        names_all = " ".join([p["name"], p["heard_as"]] + [byid[t["who"]]["name"] + " " + byid[t["who"]]["heard_as"] for t in ties if t["who"] in byid])
        rbad = []
        if len(p["rumours"]) != 5:
            rbad.append("%d rumours" % len(p["rumours"]))
        for r in p["rumours"]:
            written_texts.append((pid, r["id"], r["gist"]))
            if r["truth"] not in ("true", "false", "unknown", "partly") or not r.get("truth_basis") or not r.get("sure"):
                rbad.append("%s truth/basis/sure" % r["id"])
            for k in ("heard_from", "would_pass_to"):
                for who in r[k]:
                    if who in ("self", "street"):
                        continue
                    if who not in tids:
                        rbad.append("%s %s %s is not someone they talk to" % (r["id"], k, who))
                    else:
                        t = next(t for t in ties if t["who"] == who)
                        if t.get("hours_a_week") is not None and t["hours_a_week"] <= 0:
                            rbad.append("%s %s %s never shares a place" % (r["id"], k, who))
            if not r["would_pass_to"]:
                rbad.append("%s passes to nobody" % r["id"])
            if not r["based_on"] or any(x not in fids for x in r["based_on"]):
                rbad.append("%s rests on facts that are not theirs" % r["id"])
            else:
                badw = specifics_ok(r["gist"], " ".join(ftext[x] for x in r["based_on"]) + " " + names_all)
                if badw:
                    rbad.append("%s says %s, which is in none of the facts it rests on" % (r["id"], badw))
            if any(x in secret for x in r["based_on"]) and not r["id"].endswith("zzz"):
                rbad.append("%s rests on a secret fact" % r["id"])
            for lim in r["limits"]:
                if lim not in doc["limits"]:
                    rbad.append("%s unknown limit %s" % (r["id"], lim))
            g = r["gist"]
            if re.search(r"fire|warehouse", g, re.I) and "L2" not in r["limits"]:
                rbad.append("%s speaks of the fire without limit L2" % r["id"])
            if re.search(r"had it done", g) and r["truth"] == "true":
                rbad.append("%s calls the street's insurance talk true" % r["id"])
            if re.search(r"his heart", g) and "L4" not in r["limits"]:
                rbad.append("%s speaks of the death without limit L4" % r["id"])
            if re.search(r"new owner|nephew", g) and "L7" not in r["limits"]:
                rbad.append("%s speaks of the new owner without limit L7" % r["id"])
            if re.search(r"Hal and Rita", g) and "L6" not in r["limits"]:
                rbad.append("%s speaks of the row without limit L6" % r["id"])
            if re.search(r"a guess|suspicion|shape|noise|nobody saw", r["sure"], re.I) and re.search(r"he did it|it was Tom|Tom did|did it himself", g, re.I):
                rbad.append("%s turns a guess into 'he did it'" % r["id"])
        row("%s.rumours" % pid, "%s: exactly five rumours, each on their own facts, told only to people they meet, within RULINGS' limits" % pid, not rbad, "; ".join(rbad[:4]))

        # newcomer questions
        qs = p["newcomer_questions"]
        qbad = []
        if p.get("tom_exception"):
            row("%s.questions" % pid, "%s: the player's words are typed; no questions are written for him" % pid, len(qs) == 0 and bool(p["tom_exception"]))
        else:
            if len(qs) != 10:
                qbad.append("%d questions" % len(qs))
            names_ok = " ".join([p["name"], p["heard_as"]] + [byid[t["who"]]["name"] + " " + byid[t["who"]]["heard_as"] for t in ties if t["who"] in byid])
            seen_q = set()
            for q in qs:
                written_texts.append((pid, q["id"], q["a"]))
                if q["q"] in seen_q:
                    qbad.append("%s repeats a question" % q["id"])
                seen_q.add(q["q"])
                a = q["a"]
                if len(a.split()) >= 30:
                    qbad.append("%s is %d words" % (q["id"], len(a.split())))
                if q["kind"] not in ("answers", "partly", "dont_know", "points_to", "deflect"):
                    qbad.append("%s kind" % q["id"])
                if any(u not in fids for u in q["uses"]):
                    qbad.append("%s uses a fact that is not theirs" % q["id"])
                if q["kind"] in ("answers", "partly", "points_to") and not q["uses"]:
                    qbad.append("%s says something but cites nothing" % q["id"])
                if q["kind"] == "dont_know" and (q["uses"] or not DK.search(a)):
                    qbad.append("%s is not a plain don't-know" % q["id"])
                if q["kind"] != "deflect" and any(u in secret for u in q["uses"]):
                    qbad.append("%s tells a stranger a secret" % q["id"])
                if q["kind"] == "deflect":
                    aw = words(a)
                    tri = {tuple(aw[i:i + 3]) for i in range(len(aw) - 2)}
                    for u in q["uses"]:
                        if u in secret:
                            sw = words(ftext.get(u, ""))
                            st = {tuple(sw[i:i + 3]) for i in range(len(sw) - 2)}
                            if tri & st:
                                qbad.append("%s repeats words of the secret it withholds" % q["id"])
                if q["kind"] != "dont_know":
                    allowed = q["q"] + " " + " ".join(ftext.get(u, "") for u in q["uses"]) + " " + names_ok
                    badw = specifics_ok(a, allowed)
                    if badw:
                        qbad.append("%s says %s, which is not in what it draws on" % (q["id"], badw))
                else:
                    badw = specifics_ok(a, q["q"])
                    if badw:
                        qbad.append("%s don't-know names %s" % (q["id"], badw))
                # Mickey: only regulars who knew him, only in the approved lines
                for s in sentences(a):
                    if re.search(MICKEY_DESC, s):
                        if not p["knew_mickey"] or fold(s).lower() not in approved_mickey:
                            qbad.append("%s describes Mickey outside the approved lines" % q["id"])
            row("%s.questions" % pid, "%s: ten answers under 30 words, from their own facts only, no secret told, no invented specific" % pid, not qbad, "; ".join(qbad[:4]))

        # Mickey in rumours and new facts
        mb = []
        for src, label in ([(r["gist"], r["id"]) for r in p["rumours"]] + [(f["text"], f["id"]) for f in facts if f.get("new")]):
            for s in sentences(src):
                if re.search(MICKEY_DESC, s) and (not p["knew_mickey"] or fold(s).lower() not in approved_mickey):
                    mb.append(label)
        row("%s.mickey" % pid, "%s: Mickey is described only by regulars who knew him, in the approved lines" % pid, not mb, str(mb[:3]))

    for p in people:
        try:
            check_person(p)
        except Exception as e:  # noqa: BLE001
            row("%s.crash" % p.get("id", "?"), "the check could not read this entry", False, repr(e))

    # ---- content rows over the written text and the carried text
    def scan_all(items, label, rid):
        hits = []
        for pid, where, t in items:
            for h in cg.scan(t):
                hits.append("%s %s: %s" % (pid, where, h[2]))
        row(rid, "tools/content-gate.py finds nothing in %s (%d texts)" % (label, len(items)), not hits, "; ".join(hits[:6]))
        return hits
    scan_all(written_texts, "the written text: new facts, rumours, answers", "content.gate_written")
    scan_all(carried_texts, "the text carried word for word from the homes", "content.gate_carried")
    qtexts = [(p["id"], q["id"], q["q"]) for p in people for q in p["newcomer_questions"]]
    scan_all(qtexts, "the questions", "content.gate_questions")

    def rx_rows(rid, what, rx, items, extra_ok=lambda pid, t, m: False):
        hits = []
        for pid, where, t in items:
            for m in rx.finditer(t):
                if not extra_ok(pid, t, m):
                    hits.append("%s %s: %s" % (pid, where, m.group(0)))
        row(rid, what + " (%d texts)" % len(items), not hits, "; ".join(hits[:6]))
    allw = written_texts + qtexts
    rx_rows("content.children", "no children, schools or children's words in written text", re.compile(CHILD_WORDS, re.I), allw)
    rx_rows("content.children_carried", "no children's words in carried text", re.compile(CHILD_WORDS, re.I), carried_texts)
    real_hits = []
    for pid, where, t in allw:
        for rx in (any_rx, name_rx, place_rx):
            for m in rx.finditer(t):
                real_hits.append("%s %s: %s" % (pid, where, m.group(0)))
    row("content.real_names", "no real brand, place, public figure or later-than-1992 word in written text (RealWorld.cs's lists plus Humber-side towns) (%d texts)" % len(allw), not real_hits, "; ".join(real_hits[:6]))
    carried_real = []
    for pid, where, t in carried_texts:
        for rx in (any_rx, name_rx, place_rx):
            for m in rx.finditer(t):
                carried_real.append("%s %s: %s" % (pid, where, m.group(0)))
    row("content.real_names_carried", "carried text names no real brand or place from the lists (%d texts)" % len(carried_texts), not carried_real, "; ".join(carried_real[:6]))
    yr = re.compile(r"\b(19[0-9]{2}|20[0-9]{2})\b(?!-\d\d)")
    year_bad = ["%s %s: %s" % (pid, where, m.group(0)) for pid, where, t in allw + carried_texts for m in yr.finditer(t) if int(m.group(0)) > 1992]
    row("content.era", "no year after 1992 in any text", not year_bad, "; ".join(year_bad[:6]))
    rx_rows("content.old_names", "no old name (Lena, Rocco, Sam and the rest) in written text: they survive only as ids", re.compile(OLD_NAMES), allw)
    tomrx = re.compile(r"\b(Tom|Tommy|Nowak)\b")
    rx_rows("content.tom_name", "Tom's name appears only in Ron's, Sheila's, Darren's and Tom's own written text (the ladder)", tomrx, allw,
            extra_ok=lambda pid, t, m: pid in ("rocco", "lena", "sam", "tom"))
    rx_rows("content.foul_play", "nothing suggests Mickey died other than of his heart", re.compile(FOUL, re.I), allw)
    fire_hits = []
    for p in people:
        for f in p["facts"]:
            if f.get("secret") or f["kind"] == "believes" and f.get("secret"):
                continue
            if re.search(FIRE_TRUTH, f["text"], re.I) and re.search(r"fire|warehouse|Mickey", f["text"], re.I):
                fire_hits.append("%s %s" % (p["id"], f["id"]))
        for r in p["rumours"]:
            if re.search(FIRE_TRUTH, r["gist"], re.I):
                fire_hits.append("%s %s" % (p["id"], r["id"]))
        for q in p["newcomer_questions"]:
            if re.search(FIRE_TRUTH, q["a"], re.I):
                fire_hits.append("%s %s" % (p["id"], q["id"]))
    row("content.fire_truth", "the warehouse fire's truth is in no fact, rumour or answer that is not a marked secret", not fire_hits, "; ".join(fire_hits[:6]))
    pub = re.compile(r"Mickey's (pub|bar)|the (pub|bar) at Mickey", re.I)
    rx_rows("content.mickeys_is_a_cab_office", "Mickey's is never a pub or a bar (canon D19)", pub, allw + carried_texts)
    teach = [("%s %s" % (pid, where)) for pid, where, t in allw if re.search(r"teach|taught|schoolmaster|schoolmistress|lessons?\b", t, re.I) and pid != "elias"]
    row("content.nobody_teaches", "nobody but Philip Danby is a teacher (Ada never was)", not teach, "; ".join(teach[:4]))
    tom_q = [p["id"] for p in people if p.get("tom_exception") and p["newcomer_questions"]]
    row("content.tom_unwritten", "no word is written for Tom", not tom_q)

    # ---- canon-gate over the files
    files = [str((HERE / n).relative_to(REPO)) for n in ("people.json", "HOMES.md", "NOTES.md") if (HERE / n).exists()]
    if full:
        try:
            r = subprocess.run([sys.executable, str(REPO / "tools" / "canon-gate.py")] + files, cwd=REPO, capture_output=True, text=True, timeout=300)
            tail = (r.stdout.strip().split("\n") or [""])[-1] + " " + (r.stderr.strip().split("\n") or [""])[-1]
            row("content.canon_gate", "tools/canon-gate.py is clean over %s" % ", ".join(files), r.returncode == 0, tail.strip())
        except Exception as e:  # noqa: BLE001
            row("content.canon_gate", "tools/canon-gate.py is clean over the files", False, str(e))

    # ---- global shape rows
    row("shape.homes_file", "HOMES.md exists and names each kind of fact's home", (HERE / "HOMES.md").exists())
    row("shape.notes_file", "NOTES.md exists", (HERE / "NOTES.md").exists())
    sf_ids_bad = [sid for sid, s in doc["street_facts"].items() if not quote_at(s["src"]["file"], s["src"]["line"], s["src"]["end"], s["text"])]
    row("shape.street_facts", "the street's facts in people.json are word for word in StreetFacts.cs", not sf_ids_bad, str(sf_ids_bad))
    new_n = sum(1 for p in people for f in p["facts"] if f.get("new"))
    row("shape.counts", "44 entries, 5 rumours each, 10 answers each but Tom's", len(people) == 44 and all(len(p["rumours"]) == 5 for p in people) and sum(len(p["newcomer_questions"]) for p in people) == 430,
        "new facts: %d" % new_n)

    return list(rows)


_gate = []
_real = []


def get_gate():
    if not _gate:
        _gate.append(load_content_gate())
    return _gate[0]


def get_real():
    if not _real:
        _real.append(real_world_lists())
    return _real[0]


def seeded_faults():
    """(what, a row id part that must fail, a function that damages a copy of the document)."""
    import copy  # noqa: F401

    def person(d, pid):
        return next(p for p in d["people"] if p["id"] == pid)

    def q(d, pid, n=0):
        return person(d, pid)["newcomer_questions"][n]

    def first_sourced(d, pid):
        return next(f for f in person(d, pid)["facts"] if f.get("src") and not f.get("street"))

    def secret_of(d, pid):
        return next(f for f in person(d, pid)["facts"] if f.get("secret"))

    def m_text(d):
        first_sourced(d, "rocco")["text"] += " indeed"
    def m_line(d):
        f = first_sourced(d, "rocco"); f["src"]["line"] += 3; f["src"]["end"] += 3
    def m_group(d):
        f = next(x for x in person(d, "ada")["facts"] if x.get("new")); f["new"] = "N-NOWHERE"
    def m_unmarked(d):
        f = first_sourced(d, "ada"); del f["src"]
    def m_rumour_drop(d):
        person(d, "ada")["rumours"].pop()
    def m_rumour_to(d):
        person(d, "ada")["rumours"][0]["would_pass_to"] = ["aldous"]
    def m_fire_limit(d):
        r = next(r for r in person(d, "ada")["rumours"] if "warehouse" in r["gist"]); r["limits"] = []
    def m_foreign_fact(d):
        q(d, "rocco")["uses"] = ["lena.k05"]
    def m_secret_cited(d):
        q(d, "lena", 0)["uses"] = ["lena.k21", secret_of(d, "lena")["id"]]; q(d, "lena", 0)["kind"] = "answers"
    def m_long(d):
        q(d, "rocco")["a"] = " ".join(["word"] * 31)
    def m_name(d):
        q(d, "rocco", 2)["a"] += " Mrs Pemberton saw it."
    def m_number(d):
        q(d, "rocco", 2)["a"] += " Fourteen men saw it."
    def m_brand(d):
        q(d, "rocco")["a"] = "Ron Kirby. I keep the rank, and I smoke Marlboro."
    def m_pint(d):
        q(d, "rocco")["a"] = "Ron Kirby. I keep the rank and have a pint after."
    def m_child(d):
        person(d, "ada")["rumours"][0]["gist"] += " The children know it."
    def m_year(d):
        q(d, "rocco")["a"] = "Ron Kirby. I keep the rank, since 1995."
    def m_tom(d):
        q(d, "ada")["a"] = "That is Tom, love."
    def m_fire_truth(d):
        q(d, "ada", 7)["a"] = "The outfit burned him out, love."
    def m_mickey(d):
        q(d, "june", 7)["a"] = "Mickey was a generous man."
    def m_murder(d):
        q(d, "ada", 3)["a"] = "Somebody murdered Mickey, love."
    def m_day(d):
        f = next(f for f in person(d, "rocco")["facts"] if f.get("derived")); f["text"] += " "
    def m_sched(d):
        person(d, "rocco")["schedule"]["weekday"][1]["place"] = "quay"
    def m_missing(d):
        d["people"] = [p for p in d["people"] if p["id"] != "hal"]
    def m_extra(d):
        d["people"].append(dict(person(d, "hal"), id="hal2", name="Harold Hal", tier="regular"))
    def m_weight(d):
        person(d, "rocco")["talks_to"][0]["weight"] = 0.1
    def m_tom_q(d):
        person(d, "tom")["newcomer_questions"].append(dict(q(d, "ada"), id="tom.q1"))
    def m_teach(d):
        q(d, "ada")["a"] = "I teach on this street, love."
    def m_old_name(d):
        q(d, "ada")["a"] = "That is Lena's affair, love."
    def m_dk(d):
        q(d, "ada", 9)["uses"] = ["ada.k05"]
    def m_hours(d):
        person(d, "rita")["schedule"]["weekday"][0]["place"] = "ritas_counter"
    return [
        ("a sourced fact's words changed", "rocco.facts", m_text), ("a citation pointed at the wrong line", "rocco.facts", m_line),
        ("a new fact with no such group", "ada.facts", m_group), ("a fact with no source and no mark", "ada.facts", m_unmarked),
        ("a rumour dropped (four left)", "ada.rumours", m_rumour_drop), ("a rumour passed to someone never met", "ada.rumours", m_rumour_to),
        ("a fire rumour without its limit", "ada.rumours", m_fire_limit), ("an answer citing another person's fact", "rocco.questions", m_foreign_fact),
        ("a stranger told a secret", "lena.questions", m_secret_cited), ("an answer of 31 words", "rocco.questions", m_long),
        ("an invented name in an answer", "rocco.questions", m_name), ("an invented number in an answer", "rocco.questions", m_number),
        ("a real brand in an answer", "content.real_names", m_brand), ("drink in an answer", "content.gate_written", m_pint),
        ("children in a rumour", "content.children", m_child), ("a year after 1992", "content.era", m_year),
        ("Tom's name in Ada's answer", "content.tom_name", m_tom), ("the fire's truth in an answer", "content.fire_truth", m_fire_truth),
        ("Mickey described by one who did not know him", "june.", m_mickey), ("murder suggested", "content.foul_play", m_murder),
        ("a derived day fact altered", "rocco.facts", m_day), ("a schedule altered against hook-cast", "rocco.schedule", m_sched),
        ("a regular missing", "cast.regular.hal", m_missing), ("an extra entry", "cast.no_extra", m_extra),
        ("a tie's weight altered", "rocco.ties", m_weight), ("a question written for Tom", "content.tom_unwritten", m_tom_q),
        ("a teacher outside Philip", "content.nobody_teaches", m_teach), ("an old name in an answer", "content.old_names", m_old_name),
        ("a don't-know that cites a fact", "ada.questions", m_dk), ("a pawn counter open at three in the morning", "rita.shop_hours", m_hours),
    ]


def main():
    import copy
    doc = json.loads(PEOPLE.read_text(encoding="utf-8"))
    real_rows = run(doc, True)
    controls = []
    for i, (what, expect, mut) in enumerate(seeded_faults(), 1):
        d2 = copy.deepcopy(doc)
        try:
            mut(d2)
            r2 = run(d2, False)
            failed = [r["id"] for r in r2 if not r["pass"]]
            caught = any(expect in rid for rid in failed)
            detail = "failed rows: %s" % failed[:4]
        except Exception as e:  # noqa: BLE001
            caught, detail = False, "check crashed: %r" % (e,)
        controls.append({"id": "control.%02d" % i, "what": "seeded fault caught: %s" % what, "pass": caught, "detail": "" if caught else "expected a failing row with '%s'; %s" % (expect, detail)})
    all_rows = real_rows + controls
    passed = sum(1 for r in all_rows if r["pass"])
    summary = {"rows": len(all_rows), "pass": passed, "fail": len(all_rows) - passed, "seeded_faults": len(controls), "seeded_faults_caught": sum(1 for c in controls if c["pass"])}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"made": "13 Oct 2026, cloud week 42, unit 11", "file_checked": "production/cloud-week/town/people.json", "summary": summary, "rows": all_rows}, indent=1) + "\n", encoding="utf-8")
    for r in all_rows:
        if not r["pass"]:
            print("FAIL %s: %s | %s" % (r["id"], r["what"], r["detail"]))
    print("%d of %d rows pass (including %d of %d seeded faults caught)" % (passed, len(all_rows), summary["seeded_faults_caught"], len(controls)))
    return 0 if passed == len(all_rows) else 1


if __name__ == "__main__":
    sys.exit(main())
