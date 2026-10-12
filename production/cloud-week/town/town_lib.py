#!/usr/bin/env python3
"""Helpers for build_people.py (unit 11, cloud week 42). Standard library only.

The authored files in authored/ describe each person with the small constructors
below. This module turns them into people.json's shape: it finds every cited
quote in its home file (so a citation is a real line and a fact copied from its
home is word for word), and it derives schedules and ties from the home
(production/specs/hook-cast.json) rather than retyping them.

Light on purpose: nothing here renders, trains or calls a model.
"""
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOWN = Path(__file__).resolve().parent

# --- where the homes are (short names used in the authored files) -------------

GD = "game-design/"
ALIASES = {
    "CANON": "canon.md",
    "RUL": "RULINGS.md",
    "CASTING": "production/casting/CASTING.md",
    "REG": "production/casting/regulars/REGULARS.md",
    "SF": "ledger/Assets/Scripts/Core/StreetFacts.cs",
    "OUT": GD + "story-outline-2026-09-28.md",
    "HOUR": GD + "first-hour-2026-09-29.md",
    "FIRE": GD + "warehouse-fire-2026-09-29.md",
    "ASK": GD + "first-ask-2026-09-29.md",
    "LAND": GD + "landing-2026-09-29.md",
    "DAY1": GD + "day-one-2026-09-29.md",
    "DAY3": GD + "day-three-2026-09-29.md",
    "ELLIS": GD + "ellis-2026-09-29.md",
    "POLICE": GD + "police-asking-2026-09-29.md",
    "TRUST": GD + "sheila-trust-2026-09-29.md",
    "WEEK": GD + "week-end-2026-09-29.md",
    "NAMES": GD + "what-they-call-him-2026-09-29.md",
    "NEWS": GD + "town-news-sample-2026-09-29.md",
    "EMP": GD + "empire-roster.md",
    "LENA": "production/cast/cards/lena.md",
    "RON": "production/cast/cards/rocco.md",
    "SAM": "production/cast/cards/sam.md",
    "STL": "production/casting/ron-kirby/STREET-LINES.md",
    "NEWSJSON": "production/specs/town-news.json",
    "HK": "production/specs/hook-cast.json",
}
SHEET_DIRS = {
    "rocco": "ron-kirby", "lena": "sheila-dunn", "sam": "darren-milner", "tom": "tom-nowak",
    "ellis": "carol-ellis", "aldous": "geoffrey-agar", "sera": "maureen-jensen", "danny": "danny-cammack",
    "ada": "ada", "june": "june", "emil": "father-emil", "noor": "alison-sedman", "elias": "philip-danby",
    "fixer": "the-fixer",
}


def path_of(alias):
    if alias.startswith("S:"):
        return "production/casting/%s/SHEET.md" % SHEET_DIRS.get(alias[2:], alias[2:])
    return ALIASES.get(alias, alias)


# --- finding a quote in its home ----------------------------------------------

_cache = {}


def _lines(path):
    if path not in _cache:
        _cache[path] = (REPO / path).read_text(encoding="utf-8").split("\n")
    return _cache[path]


def _norm(s):
    return " ".join(s.split())


def locate(path, quote, near=None):
    """(first line, last line), 1-based, of the quote in the file, whitespace
    folded so a sentence wrapped over two lines still matches. Fails loudly."""
    lines = _lines(path)
    text, owner = [], []
    for i, l in enumerate(lines, 1):
        seg = _norm(l)
        if not seg:
            continue
        if text:
            text.append(" ")
            owner.append(i)
        text.extend(seg)
        owner.extend([i] * len(seg))
    flat = "".join(text)
    q = _norm(quote)
    hits, at = [], 0
    while True:
        j = flat.find(q, at)
        if j < 0:
            break
        hits.append(j)
        at = j + 1
    if not hits:
        raise SystemExit("QUOTE NOT FOUND in %s: %r" % (path, quote))
    if near is not None:
        hits.sort(key=lambda j: abs(owner[j] - near))
    j = hits[0]
    return owner[j], owner[j + len(q) - 1]


# --- the street's plain facts (StreetFacts.cs), parsed ------------------------

_STR = r'"((?:[^"\\]|\\.)*)"'
_ENTRY = re.compile(r'\(\s*"([a-z_]+)"\s*,\s*"([a-z]*)"\s*,\s*' + _STR + r'\s*,\s*(null|' + _STR + r')\s*,\s*' + _STR + r'\s*,\s*(null|' + _STR + r')\s*\)', re.S)


def street_facts():
    src = (REPO / ALIASES["SF"]).read_text(encoding="utf-8")
    block = src[src.index("All =") : src.index("};", src.index("All ="))]
    block = re.sub(r"//[^\n]*", "", block)
    out = {}
    for m in _ENTRY.finditer(block):
        g = m.groups()
        # groups: 0 id, 1 about, 2 fact, 3 own-or-null, 4 own-inner, 5 said, 6 ownsaid-or-null, 7 ownsaid-inner
        out[g[0]] = {"id": g[0], "about": g[1], "fact": g[2], "own": g[4], "said": g[5], "own_said": g[7]}
    return out


# --- hook-cast.json: schedules and ties ---------------------------------------

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
_HK = None


def hk():
    global _HK
    if _HK is None:
        _HK = json.loads((REPO / ALIASES["HK"]).read_text(encoding="utf-8"))
    return _HK


def hk_person(pid):
    for p in hk()["people"]:
        if p["id"] == pid:
            return p
    return None


def hk_person_line(pid):
    for i, l in enumerate(_lines(ALIASES["HK"]), 1):
        if l.strip() == '"id": "%s",' % pid and i > 300:
            return i
    raise SystemExit("no hook-cast line for " + pid)


def hk_ties_lines():
    """[(first line, [a, b, w, text])] for every tie, by reading the file."""
    lines = _lines(ALIASES["HK"])
    start = next(i for i, l in enumerate(lines) if l.startswith(' "ties": ['))
    out, i = [], start + 1
    while i < len(lines):
        if lines[i] == "  [":
            a = json.loads(lines[i + 1].strip().rstrip(","))
            b = json.loads(lines[i + 2].strip().rstrip(","))
            w = json.loads(lines[i + 3].strip().rstrip(","))
            t = json.loads(lines[i + 4].strip().rstrip(","))
            out.append((i + 1, [a, b, w, t]))
            i += 6
        else:
            i += 1
    return out


def day_segments(pid, day):
    """[(from, to, place)] covering 0 to 24 on a weekday ('mon'..'sun')."""
    p = hk_person(pid)
    routine = p.get("days", {}).get(day) or p["routine"]
    routine = sorted([(float(h), pl) for h, pl in routine])
    segs = []
    for i, (h, pl) in enumerate(routine):
        end = routine[i + 1][0] if i + 1 < len(routine) else 24.0
        segs.append([h, end, pl])
    if segs and segs[0][0] > 0:
        segs.insert(0, [0.0, segs[0][0], routine[-1][1]])
    merged = []
    for s in segs:
        if merged and merged[-1][2] == s[2]:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return merged


def place_said(place):
    if place == "off":
        return "away from the street (at home, or elsewhere)"
    return hk()["places"][place]["said"]


def hour_text(h):
    h = float(h)
    whole = int(h)
    return "%02d:%02d" % (whole, round((h - whole) * 60))


def seg_dicts(segs):
    return [{"from": hour_text(a), "to": hour_text(b) if b < 24 else "24:00", "place": pl, "said": place_said(pl)} for a, b, pl in segs]


def derive_schedule(pid):
    p = hk_person(pid)
    if p is None:
        return None
    mon = day_segments(pid, "mon")
    out = {"weekday": seg_dicts(mon), "weekday_note": "Monday, the first day of the game's week; the days below differ from it",
           "weekday_differs": {}, "saturday": seg_dicts(day_segments(pid, "sat")), "sunday": seg_dicts(day_segments(pid, "sun")),
           "source": {"file": ALIASES["HK"], "line": hk_person_line(pid), "derived": True}}
    for d in ["tue", "wed", "thu", "fri"]:
        s = day_segments(pid, d)
        if s != mon:
            out["weekday_differs"][d] = seg_dicts(s)
    return out


def pos(place):
    pl = hk()["places"].get(place)
    if not pl:
        return None
    return (pl["x_m"], pl["z_m"])


def hours_together(a, b):
    """Hours a week the two are within the talking range, from the routines."""
    rng = hk()["talk_range_m"]
    total = 0.0
    for d in DAYS:
        sa = day_segments(a, d)
        sb = day_segments(b, d)
        for h in range(24):
            pa = next((s[2] for s in sa if s[0] <= h < s[1]), "off")
            pb = next((s[2] for s in sb if s[0] <= h < s[1]), "off")
            xa, xb = pos(pa), pos(pb)
            if xa is None or xb is None:
                continue
            if ((xa[0] - xb[0]) ** 2 + (xa[1] - xb[1]) ** 2) ** 0.5 <= rng:
                total += 1
    return total


def weight_band(w):
    if w >= 0.8:
        return "the strongest tie in the cast"
    if w >= 0.7:
        return "old and close"
    if w >= 0.6:
        return "good friends"
    if w >= 0.5:
        return "friendly"
    if w >= 0.4:
        return "on easy terms"
    return "a nod and a word"


def derive_ties(pid):
    out, seen = [], set()
    for line, (a, b, w, t) in hk_ties_lines():
        if pid not in (a, b):
            continue
        other = b if a == pid else a
        if other in seen:
            continue
        seen.add(other)
        entry = {"who": other, "weight": w, "band": weight_band(w), "meets": t,
                 "hours_a_week": hours_together(a, b) if hk_person(other) else None,
                 "source": {"file": ALIASES["HK"], "line": line, "derived": True}}
        out.append(entry)
    out.sort(key=lambda e: -e["weight"])
    return out


# --- shop hours, rendered the same way the check renders them -----------------


def render_hours(area):
    a = hk()["areas"][area]
    hrs = a.get("hours", {})
    if not hrs:
        return None
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
        label = ds[0] if len(ds) == 1 else ds[0] + " to " + ds[-1]
        parts.append("%s %s-%s" % (label, hour_text(span[0]), hour_text(span[1] if span[1] <= 24 else span[1] - 24)))
    if a.get("hours_note"):
        parts.append(a["hours_note"])
    return "%s: %s" % (a["names"][0], "; ".join(parts))


def render_day_fact(pid):
    """One sentence per weekday kind, from the routines (the derived 'where to find' fact)."""
    sched = derive_schedule(pid)

    def fmt(segs):
        bits = ["%s to %s %s" % (s["from"], s["to"], s["said"]) for s in segs if s["place"] != "off"]
        return ", then ".join(bits) if bits else "not on the street"

    return "Monday: %s. Saturday: %s. Sunday: %s." % (fmt(sched["weekday"]), fmt(sched["saturday"]), fmt(sched["sunday"]))


# --- the small authoring language ---------------------------------------------


class Spec(dict):
    pass


def K(key, src, quote, secret=False, near=None, via=None):
    """A fact copied word for word from its home (file and line found by reading)."""
    d = Spec(key=key, kind="knows", src=(src, quote, near), secret=secret)
    if via:
        d["via"] = via
    return d


def N(key, group, text, why, secret=False, kind="knows"):
    """A fact that has no home: new, marked for Jafar, with the reason it fits canon and the story."""
    return Spec(key=key, kind=kind, new=group, text=text, why=why, secret=secret)


def D(key, how, arg=None):
    """A fact derived by script from hook-cast.json: how is 'day' or 'hours' (arg = area)."""
    return Spec(key=key, kind="knows", derived=how, arg=arg)


def B(key, src, quote, truth, basis, secret=False, near=None):
    """Something believed, copied from a home; truth is true, false or unknown against canon and the story."""
    return Spec(key=key, kind="believes", src=(src, quote, near), truth=truth, basis=basis, secret=secret)


def BN(key, group, text, why, truth, basis, secret=False):
    return Spec(key=key, kind="believes", new=group, text=text, why=why, truth=truth, basis=basis, secret=secret)


def W(key, src, quote, when, secret=False, near=None):
    """Something seen, copied from a home; when says the baseline moment."""
    return Spec(key=key, kind="saw", src=(src, quote, near), when=when, secret=secret)


def WN(key, group, text, why, when, secret=False):
    return Spec(key=key, kind="saw", new=group, text=text, why=why, when=when, secret=secret)


def R(gist, truth, basis, sure, frm, to, on, limits=(), new_basis=None):
    """A rumour: its gist, its truth against canon and the story, how sure the first witness was,
    who it came from, who it would go to, and the facts of the person it rests on."""
    return Spec(gist=gist, truth=truth, basis=basis, sure=sure, frm=list(frm), to=list(to), on=list(on), limits=list(limits))


def Q(question, kind, answer, uses=(), bench=None):
    return Spec(q=question, kind=kind, a=answer, uses=list(uses), bench=bench)


def H(alias, quote, note=None):
    """A truth basis that points at a line in a home (the quote is found and cited)."""
    return Spec(basis_src=(alias, quote), note=note)


def NOTE(text):
    """A truth basis that is only a reason in words (canon and the story are silent)."""
    return Spec(basis_note=text)


def person(pid, name, heard_as, tier, age, role, identity, knows, believes, saw, rumours, questions, street=(), ties_note=None,
           schedule=None, talks=None, knew_mickey=False, tom_exception=False, internal_id_note=None, extra=None):
    return Spec(id=pid, name=name, heard_as=heard_as, tier=tier, age=age, role=role, identity=identity, knows=list(knows),
                believes=list(believes), saw=list(saw), rumours=list(rumours), questions=list(questions), street=list(street),
                schedule=schedule, talks=talks or {}, knew_mickey=knew_mickey, tom_exception=tom_exception,
                internal_id_note=internal_id_note, extra=extra or {})


# --- proposed schedules (for the people hook-cast.json has no routine for) ------

PROPOSED_PLACES = {}


def _hv(x):
    if isinstance(x, str):
        h, m = x.split(":")
        return int(h) + int(m) / 60.0
    return float(x)


def said_any(place):
    if place in PROPOSED_PLACES:
        return PROPOSED_PLACES[place]["said"]
    return place_said(place)


def PS(weekday, saturday, sunday, differs=None, note=""):
    """A proposed schedule: lists of (from, to, place) with hours as numbers; places are hook-cast's or PROPOSED_PLACES."""
    def seg(lst):
        out = []
        for a, b, pl in lst:
            out.append({"from": hour_text(a), "to": hour_text(b) if b < 24 else "24:00", "place": pl, "said": said_any(pl)})
        return out
    d = {"weekday": seg(weekday), "weekday_note": "Monday to Friday unless a day is listed below",
         "weekday_differs": {k: seg(v) for k, v in (differs or {}).items()},
         "saturday": seg(saturday), "sunday": seg(sunday),
         "source": {"new": "N-SCHEDULES", "proposed": True}, "note": note}
    return Spec(d)


def sched_day_segments(sched, day):
    """[(from, to, place)] on a weekday for a schedule dict (derived or proposed)."""
    if day == "sat":
        lst = sched["saturday"]
    elif day == "sun":
        lst = sched["sunday"]
    else:
        lst = sched.get("weekday_differs", {}).get(day) or sched["weekday"]
    return [(_hv(s["from"]), _hv(s["to"]), s["place"]) for s in lst]


def hours_together_sched(sa, sb):
    rng = hk()["talk_range_m"]
    total = 0.0
    for d in DAYS:
        a, b = sched_day_segments(sa, d), sched_day_segments(sb, d)
        for h in range(24):
            pa = next((s[2] for s in a if s[0] <= h < s[1]), "off")
            pb = next((s[2] for s in b if s[0] <= h < s[1]), "off")
            xa, xb = pos(pa), pos(pb)
            if xa is None or xb is None:
                continue
            if ((xa[0] - xb[0]) ** 2 + (xa[1] - xb[1]) ** 2) ** 0.5 <= rng:
                total += 1
    return total


def propose_ties(pid, sched, min_hours=3):
    """People whose hook-cast routines put them within the talking range of this proposed schedule: computed, not invented."""
    out = []
    for p in hk()["people"]:
        if p["id"] == pid or p["id"] == "outfit_man":
            continue
        other = derive_schedule(p["id"])
        h = hours_together_sched(sched, other)
        if h >= min_hours:
            out.append({"who": p["id"], "weight": None, "band": "shares the same place %d hours a week (computed from the two schedules)" % h,
                        "meets": "computed", "hours_a_week": h, "source": {"new": "N-SCHEDULES", "computed": True}})
    out.sort(key=lambda e: -e["hours_a_week"])
    return out
