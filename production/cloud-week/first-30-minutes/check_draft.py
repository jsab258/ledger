#!/usr/bin/env python3
"""The check for DRAFT.md, LEDGER's first thirty minutes (cloud week 42, backlog item B5).

    python3 check_draft.py                     # every row, then "N of M rows pass" (exit 1 on any failure)
    python3 check_draft.py --measures          # print the blocks that section 3.3 and section 4 must carry
    python3 check_draft.py --negative-controls # damage copies of the draft on purpose; each must fail by name

Written apart from the draft and reading it as a stranger would. What it holds the draft to:

  shape      the first line; six sections; section 1 at most six lines; no placeholder left
  routes     each of the two tables covers minutes 0 to 30 with no gap and no overlap, a beat of one or two
             minutes; the Clock column is what the stated clock gives (two game hours a real minute from
             Monday 09:00, plus the waits); the Tags give one group a minute and the empty flag is derived
             from them (a minute with none of I, C, S, W is empty); at most five empty minutes a route
  people     every id in Who is in production/cloud-week/town/people.json (or one of three roles with a
             source); every id in Where is in production/specs/hook-cast.json (or an alias with a source);
             each person is where their routine puts them at that game time (a star marks an authored
             visit); no capitalised name in the prose that canon, the town data or the allow list lacks
  story      each route has a choice, a consequence within three minutes of a choice, a restart and, after
             it, saved state that names a piece of TownSave; live exchanges within the cap
  measures   section 4's cells equal what the tables give; section 3.3 equals the computed differences
  content    tools/content-gate.py and tools/canon-gate.py are clean over the file; no em dash, no
             italics; third person outside quotation marks
  sections   section 5 cites real sections of the praise-and-punish file; section 6 has at most five
             questions with a recommendation each and a page of at most three decisions after its shortfalls;
             every proposal is defined and used

Standard library only. The repository's two gates are loaded from tools/.
"""
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
DRAFT = HERE / "DRAFT.md"

FIRST_LINE = ("DRAFT UNTIL THE AAA STUDY (13 October 2026): written from canon, PLAN.md and public research only; "
              "the study's measured benchmark (study 2 of the AAA Reference Study) replaces any number marked 'guess'.")
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DAYKEY = {"Mon": "mon", "Tue": "tue", "Wed": "wed", "Thu": "thu", "Fri": "fri", "Sat": "sat", "Sun": "sun"}
GAME_MIN_PER_REAL_MIN = 120          # guess, stated in section 2.3: two game hours a real minute
START_MIN = 9 * 60                   # Monday 09:00
TOTAL = 30
LIVE_CAP = 20                        # section 2.2: $0.50 a run at a guess of $0.025 a live exchange
COST_PER_LIVE = 0.025
EMPTY_CAP = 5
ROLES = {                            # no entry in people.json; each has a source the draft names
    "outfit_man": "canon and REGULARS.md leave the outfit's man unnamed; the first-ask and landing designs",
    "constable": "the waiting and police designs (a constable calls at ten)",
    "neighbour": "the town-news sample's two neighbours, unnamed",
}
WHERE_ALIASES = {                    # places canon or the street's plain facts name that hook-cast.json does not
    "quay_street": "canon: the street itself, anywhere on it",
    "mickeys_flat": "StreetFacts 'flat': Mickey's flat over the office",
    "mickeys_yard": "canon: a yard with two escapes",
}
TOWNSAVE_PIECES = {"hints", "asks", "tea", "police", "heard", "news", "damage", "arrests", "hours", "week", "shown", "memory"}
MARK_TIMED = {"control", "move", "talk", "choice", "conflict", "consequence", "restart"}
STATUSES = ("BUILT", "DESIGNED", "NOT YET")
COLS = ["No", "Min", "Clock", "Where", "Who", "Mode", "Tags", "Tension", "Marks", "Beat", "Learns", "Status"]
# capitalised words that are not people or places of canon; everything else mid-sentence must come from
# canon.md, the town data or the cast files. Kept short and plain so a stranger name cannot hide in it.
GENERIC_CAPS = set("""
Monday Tuesday Wednesday Thursday Friday Saturday Sunday October September
PLAN CHARTER RULINGS DECISIONS CATALOGUE NOW TOWN LEDGER Ledger Core Unreal Tab Esc
AAA Study Reference Route Routes Neighbour Shaun Kevin Terry Pauline Brenda Wayne Edith Doreen Tracey Julie Grace Hal
Sheila Ron Darren Ada June Alison Ellis Walsh Father Mickey Mickeys Rita Ritas Tom Nowak Mr
DS CID BUILT DESIGNED NOT YET P Q D G A B C
Quay Street Hook Parade Epic Game Animation Sample FirstMoments AiNotice Coat Waiting Arrangement PoliceFile Custody TownSave
Debts Perception Gossip StreetFacts REGULARS
Skippable Clock Where Who Mode Tags Marks Beat Learns Status Min No Words Continue Quit Resume New Tuesdays
""".split())


# ------------------------------------------------------------------ the repository's own homes

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CG = load_module(REPO / "tools" / "content-gate.py", "_cg")
PEOPLE = json.loads((REPO / "production/cloud-week/town/people.json").read_text(encoding="utf-8"))["people"]
PBYID = {p["id"]: p for p in PEOPLE}
HOOK = json.loads((REPO / "production/specs/hook-cast.json").read_text(encoding="utf-8"))
PLACES = HOOK["places"]
AREAS = HOOK["areas"]
PLACE_AREA = {}
for _a, _v in AREAS.items():
    for _p in _v.get("places", []):
        PLACE_AREA[_p] = _a
STREET_AREAS = {a for a, v in AREAS.items() if v.get("street")}
CANON = (REPO / "canon.md").read_text(encoding="utf-8")
PRAISE_FILE = REPO / "production/research/aaa-reference" / ("PLAY" + "ERS.md")   # the canon gate refuses that word whole


def known_name_words():
    words = set()
    for p in PEOPLE:
        for field in (p["name"], p["heard_as"]):
            for w in re.findall(r"[A-Z][A-Za-z']+", field):
                words.add(w.replace("'s", ""))
    for w in re.findall(r"\b[A-Z][A-Za-z']+", CANON):
        words.add(w.replace("'s", ""))
    for v in PLACES.values():
        for w in re.findall(r"\b[A-Z][A-Za-z']+", v.get("said", "")):
            words.add(w)
    for v in AREAS.values():
        for n in v.get("names", []):
            for w in re.findall(r"\b[A-Z][A-Za-z']+", n):
                words.add(w.replace("'s", ""))
    return words | GENERIC_CAPS


KNOWN = known_name_words()


# ------------------------------------------------------------------ reading the draft

def split_sections(text):
    """{'1': text, ...} by '## n.' headings."""
    out = {}
    cur = None
    for line in text.split("\n"):
        m = re.match(r"^## (\d)\.", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def sub_section(text, heading_re):
    lines = text.split("\n")
    out, on = [], False
    for line in lines:
        if re.match(r"^###? ", line):
            if on:
                break
            if re.match(heading_re, line):
                on = True
                continue
        elif on:
            out.append(line)
    return "\n".join(out)


def parse_table(block):
    """Rows of a pipe table as lists of cell strings (header and rule lines dropped)."""
    rows = []
    for line in block.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and set(cells[0]) <= set("-:"):
            continue
        rows.append(cells)
    return rows


def ids_in(cell):
    return re.findall(r"`([^`]+)`", cell)


def parse_route(text, letter):
    sec = split_sections(text).get("3", "")
    head = {"A": r"^### 3\.1", "B": r"^### 3\.2"}[letter]
    block = sub_section(sec, head)
    rows = parse_table(block)
    out, errs = [], []
    for cells in rows:
        if cells[0] == "No":
            if cells != COLS:
                errs.append("header is %s" % cells)
            continue
        if len(cells) != len(COLS):
            errs.append("row %s has %d cells" % (cells[0], len(cells)))
            continue
        r = dict(zip(COLS, cells))
        m = re.match(r"^(\d+)-(\d+)$", r["Min"])
        r["start"], r["end"] = (int(m.group(1)), int(m.group(2))) if m else (None, None)
        r["len"] = (r["end"] - r["start"]) if m else None
        r["where"] = ids_in(r["Where"])
        r["who"] = ids_in(r["Who"])
        mm = re.match(r"^(play|cut:(\d+))(?: skip:(\d+))?$", r["Mode"])
        r["cut"] = int(mm.group(2) or 0) if mm else None
        r["skip"] = int(mm.group(3) or 0) if mm and mm.group(3) else 0
        r["mode_ok"] = bool(mm)
        r["groups"] = [g.strip() for g in r["Tags"].split("/")]
        r["tension"] = [g.strip() for g in r["Tension"].split("/")]
        r["marks"] = r["Marks"].split() if r["Marks"] != "-" else []
        out.append(r)
    return out, errs


def clock_string(start_min, skip_before_hours):
    t = START_MIN + GAME_MIN_PER_REAL_MIN * start_min + 60 * skip_before_hours
    d, rem = divmod(t, 1440)
    return "%s %02d:%02d" % (DAYS[d % 7], rem // 60, rem % 60), t


def mark_times(row):
    """[(name, seconds from route start)] for the timed marks, and the other marks."""
    timed, other = [], []
    for tok in row["marks"]:
        m = re.match(r"^([a-z]+)@(\d+):(\d\d)$", tok)
        if m and m.group(1) in MARK_TIMED:
            timed.append((m.group(1), int(m.group(2)) * 60 + int(m.group(3)), None))
            continue
        m = re.match(r"^(ui:[a-z-]+)@(\d+):(\d\d)$", tok)
        if m:
            timed.append((m.group(1), int(m.group(2)) * 60 + int(m.group(3)), None))
            continue
        m = re.match(r"^persists:([a-z]+)@(\d+):(\d\d)$", tok)
        if m:
            timed.append(("persists", int(m.group(2)) * 60 + int(m.group(3)), m.group(1)))
            continue
        other.append(tok)
    return timed, other


def fmt(sec):
    return "%d:%02d" % (sec // 60, sec % 60)


# ------------------------------------------------------------------ schedules

def segments(pid, day):
    p = PBYID[pid]
    s = p["schedule"]
    if day in ("sat", "sun"):
        return s.get(day) or s["weekday"]
    diff = s.get("weekday_differs") or {}
    return diff.get(day, s["weekday"])


def hm(t):
    return int(t[:2]) * 60 + int(t[3:])


def area_at(pid, abs_min):
    d, rem = divmod(abs_min, 1440)
    day = DAYKEY[DAYS[d % 7]]
    for seg in segments(pid, day):
        a, b = hm(seg["from"]), hm(seg["to"])
        if a <= rem < b or (b == 1440 and rem >= a):
            return PLACE_AREA.get(seg["place"])
    return None


def where_areas(ids):
    areas = set()
    for i in ids:
        if i == "quay_street":
            areas |= STREET_AREAS
        elif i in ("mickeys_flat", "mickeys_yard"):
            areas.add("mickeys")
        elif i in PLACE_AREA:
            areas.add(PLACE_AREA[i])
    return areas


def present(pid, abs_start, length_real_min, areas):
    end = abs_start + length_real_min * GAME_MIN_PER_REAL_MIN
    t = abs_start
    while t < end:
        if area_at(pid, t) in areas:
            return True
        t += 30
    return False


# ------------------------------------------------------------------ the rows

class Result:
    def __init__(self):
        self.rows = []

    def row(self, rid, text, ok, detail=""):
        self.rows.append((rid, text, bool(ok), detail if not ok else ""))

    def tally(self):
        ok = sum(1 for r in self.rows if r[2])
        return ok, len(self.rows)


def strip_for_prose(line):
    line = re.sub(r"`[^`]*`", " ", line)
    line = re.sub(r"\"[^\"]*\"", " ", line)
    return line


ITALIC_STAR = re.compile(r"(?<![\w*])\*[^*\s][^*\n]*[^*\s]\*(?![\w*])")
ITALIC_UND = re.compile(r"(?<![\w_])_[^_\s][^_\n]*[^_\s]_(?![\w_])")
FIRST_PERSON = re.compile(r"\b(I|I'm|I've|I'll|I'd|we|we're|we've|my|our|ours|us|me|you|your|yours|you're|you've)\b")


def prose_names(text):
    """Capitalised words in the prose that sit mid-sentence and that nothing known explains."""
    bad = []
    for n, line in enumerate(text.split("\n"), 1):
        s = re.sub(r"`[^`]*`", " ", line)
        s = re.sub(r'"([^"]*)"', lambda m: " QUOTE" + ("." if m.group(1).rstrip()[-1:] in ".?!" else "") + " ", s)
        if s.startswith("#"):
            s = re.sub(r"^#+\s*[\d.]*\s*", "", s)
        s = re.sub(r"\([a-z0-9_.\-]+\)", " ", s)             # (ron.greet-nowak.06)
        for m in re.finditer(r"\b[A-Z][a-z][A-Za-z']*", s):
            w = m.group(0)
            before = s[:m.start()].rstrip()
            if before == "" or before[-1] in ".?!:|(-;)" or before.endswith("#"):
                continue                                      # sentence, cell or list start
            base = w[:-2] if w.endswith("'s") else w
            if base in KNOWN or w in KNOWN:
                continue
            bad.append("line %d: %s" % (n, w))
    return bad


def all_checks(text, full=True):
    R = Result()
    sec = split_sections(text)

    # ---- shape
    R.row("shape.first_line", "the first line is the draft marking, word for word", text.split("\n")[0] == FIRST_LINE)
    R.row("shape.sections", "sections 1 to 6 are all there, in order", list(sec.keys()) == ["1", "2", "3", "4", "5", "6"], str(list(sec.keys())))
    s1 = [l for l in sec.get("1", "").split("\n") if l.strip()]
    R.row("shape.section1_lines", "section 1 is at most six lines", 1 <= len(s1) <= 6, "%d lines" % len(s1))
    R.row("shape.no_placeholder", "no placeholder is left in the draft", not re.search(r"SHARE_BUILT|DIFFERENCES_BLOCK|MEASURE_BLOCK|TODO|XXX", text))

    routes = {}
    for letter, nbeats in (("A", None), ("B", None)):
        rows, errs = parse_route(text, letter)
        routes[letter] = rows
        R.row("%s.table" % letter, "route %s: the table has the right header and %d well-formed rows" % (letter, len(rows)), rows and not errs, "; ".join(errs[:3]))
        names_ok = all(r["No"] == "%s%d" % (letter, i + 1) for i, r in enumerate(rows))
        R.row("%s.numbering" % letter, "route %s: beats are numbered %s1, %s2 and so on in order" % (letter, letter, letter), names_ok)
        R.row("%s.mode" % letter, "route %s: every Mode is play or cut:N, with an optional skip:N" % letter, all(r["mode_ok"] for r in rows))

        # coverage: no gap, no overlap, minutes 0 to 30
        gaps = []
        t = 0
        for r in rows:
            if r["start"] is None or r["len"] not in (1, 2):
                gaps.append("%s: bad Min %r" % (r["No"], r["Min"]))
                continue
            if r["start"] != t:
                gaps.append("%s starts at %d, expected %d" % (r["No"], r["start"], t))
            t = r["end"]
        if t != TOTAL:
            gaps.append("ends at %d, not %d" % (t, TOTAL))
        R.row("%s.coverage" % letter, "route %s covers minutes 0 to %d with no gap and no overlap, every beat one or two minutes" % (letter, TOTAL), not gaps, "; ".join(gaps[:4]))

        # clock
        bad, skipped = [], 0
        for r in rows:
            if r["start"] is None:
                continue
            want, _ = clock_string(r["start"], skipped)
            if r["Clock"] != want:
                bad.append("%s says %s, the clock gives %s" % (r["No"], r["Clock"], want))
            skipped += r["skip"]
        R.row("%s.clock" % letter, "route %s: every Clock is two game hours a real minute from Monday 09:00 plus the stated waits" % letter, not bad, "; ".join(bad[:3]))

        # tags and empties
        tagbad, empties, empty_runs, run = [], 0, [], 0
        for r in rows:
            if r["len"] not in (1, 2):
                continue
            if len(r["groups"]) != r["len"]:
                tagbad.append("%s has %d tag groups for %d minutes" % (r["No"], len(r["groups"]), r["len"]))
                continue
            for g in r["groups"]:
                if g == "-":
                    empties += 1
                    run += 1
                elif re.fullmatch(r"[ICSW]{1,4}", g) and len(set(g)) == len(g):
                    empty_runs.append(run)
                    run = 0
                else:
                    tagbad.append("%s has the tag group %r" % (r["No"], g))
        empty_runs.append(run)
        R.row("%s.tags" % letter, "route %s: one tag group a minute, each a dash or letters from I, C, S, W" % letter, not tagbad, "; ".join(tagbad[:3]))
        R.row("%s.empty_cap" % letter, "route %s has at most %d empty minutes by its own tags (it has %d)" % (letter, EMPTY_CAP, empties), empties <= EMPTY_CAP)
        tenbad = [r["No"] for r in rows if r["len"] in (1, 2) and (len(r["tension"]) != r["len"] or any(g not in ("rising", "falling", "quiet") for g in r["tension"]))]
        ten = [g for r in rows for g in r["tension"]]
        R.row("%s.tension" % letter, "route %s: one tension word a minute (rising, falling or quiet), and the route rises at least once" % letter, not tenbad and "rising" in ten, ", ".join(tenbad))
        statusbad = [r["No"] for r in rows if not r["Status"].startswith(STATUSES)]
        R.row("%s.status" % letter, "route %s: every Status begins BUILT, DESIGNED or NOT YET" % letter, not statusbad, ", ".join(statusbad))
        # a row flagged empty must say nothing new in Learns
        learnbad = [r["No"] for r in rows if r["groups"] == ["-"] and r["Learns"].strip().lower().rstrip(".") != "nothing new"]
        R.row("%s.empty_says_nothing" % letter, "route %s: a beat that is empty says 'Nothing new' in Learns" % letter, not learnbad, ", ".join(learnbad))

        # marks
        mbad, live = [], 0
        timed_all = []
        for r in rows:
            if r["start"] is None:
                continue
            timed, other = mark_times(r)
            for name, sec_, piece in timed:
                if not (r["start"] * 60 <= sec_ < r["end"] * 60):
                    mbad.append("%s: %s at %s is outside minutes %s" % (r["No"], name, fmt(sec_), r["Min"]))
                if name == "persists" and piece not in TOWNSAVE_PIECES:
                    mbad.append("%s: persists:%s names no piece of TownSave" % (r["No"], piece))
                timed_all.append((name, sec_, piece, r["No"]))
            for tok in other:
                m = re.match(r"^live:(\d+)$", tok)
                if m:
                    live += int(m.group(1))
                elif not re.match(r"^act:[a-z-]+$", tok):
                    mbad.append("%s: unknown mark %r" % (r["No"], tok))
        R.row("%s.marks" % letter, "route %s: every mark is a known kind and its time falls inside its beat" % letter, not mbad, "; ".join(mbad[:3]))
        R.row("%s.live_cap" % letter, "route %s: %d live exchanges, at most %d (about $%.2f at the guess of $%.3f)" % (letter, live, LIVE_CAP, live * COST_PER_LIVE, COST_PER_LIVE), live <= LIVE_CAP)

        # choice, consequence, restart, persists
        choices = sorted(s for n, s, p, b in timed_all if n == "choice")
        conseq = sorted(s for n, s, p, b in timed_all if n == "consequence")
        restarts = sorted(s for n, s, p, b in timed_all if n == "restart")
        persist = sorted((s, p) for n, s, p, b in timed_all if n == "persists")
        R.row("%s.choice" % letter, "route %s has at least one crime or choice (a choice mark)" % letter, bool(choices))
        near = [c for c in choices if any(0 <= k - c <= 180 for k in conseq)]
        R.row("%s.consequence" % letter, "route %s: a consequence is seen within three minutes of a choice" % letter, bool(near))
        R.row("%s.restart" % letter, "route %s has a restart, and every persisting mark comes after it" % letter,
              bool(restarts) and bool(persist) and all(s >= restarts[0] for s, p in persist), "restarts %s, persists %s" % (restarts, persist))
        R.row("%s.persists" % letter, "route %s: the consequence persists after the restart, naming at least two pieces of saved state" % letter,
              len({p for s, p in persist}) >= 2, str(sorted({p for s, p in persist})))

        # the restart beat says how many hints were shown, and the number is the tables' own
        words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}
        nh = len({tok.split("@")[0] for r in rows for tok in r["marks"] if re.match(r"^ui:[a-z-]+-hint@", tok)})
        last = rows[-1]["Beat"] if rows else ""
        R.row("%s.hint_claim" % letter, "route %s: the closing beat names the number of hints the table shows (%s)" % (letter, words.get(nh, nh)),
              re.search(r"the %s hints" % words.get(nh, "?"), last) is not None, last[-120:])

        # people and places
        pbad, wbad, sbad = [], [], []
        skipped = 0
        for r in rows:
            if r["start"] is None:
                continue
            for pid in r["who"]:
                base = pid.rstrip("*")
                if base not in PBYID and base not in ROLES and base != "-":
                    pbad.append("%s: %s" % (r["No"], pid))
            for w in r["where"]:
                if w not in PLACES and w not in WHERE_ALIASES:
                    wbad.append("%s: %s" % (r["No"], w))
            _, abs_start = clock_string(r["start"], skipped)
            areas = where_areas(r["where"])
            for pid in r["who"]:
                if pid.endswith("*") or pid not in PBYID:
                    continue
                if not present(pid, abs_start, r["len"], areas):
                    sbad.append("%s: %s is not in %s then" % (r["No"], pid, "/".join(r["where"])))
            skipped += r["skip"]
        R.row("%s.who_ids" % letter, "route %s: every person id exists in the town data (or is one of three sourced roles)" % letter, not pbad, "; ".join(pbad[:4]))
        R.row("%s.where_ids" % letter, "route %s: every place id exists in hook-cast.json (or is a sourced alias)" % letter, not wbad, "; ".join(wbad[:4]))
        R.row("%s.schedules" % letter, "route %s: each person is where their routine puts them at that game time" % letter, not sbad, "; ".join(sbad[:4]))

        # proposals used in the rows
    # ---- the two routes differ
    ids = {l: {p.rstrip("*") for r in routes[l] for p in r["who"]} for l in "AB"}
    R.row("routes.differ", "the two routes differ: each has people and beats the other lacks, and they open and choose differently",
          bool(ids["A"] - ids["B"]) and bool(ids["B"] - ids["A"]) and
          {r["No"] for r in routes["A"] if "crime" in " ".join(r["marks"])} != {r["No"] for r in routes["B"] if "crime" in " ".join(r["marks"])})

    # ---- measures against section 4 and section 3.3
    meas = measures(routes)
    s4 = sec.get("4", "")
    t4 = parse_table(s4)
    want_rows = measure_rows(meas)
    got = {c[0]: c for c in t4 if len(c) == 4}
    bad4 = []
    for label, a, b, _note in want_rows:
        c = got.get(label)
        if not c:
            bad4.append("missing row %r" % label)
            continue
        if c[1] != a or c[2] != b:
            bad4.append("%s: table says %r and %r, the tables give %r and %r" % (label, c[1], c[2], a, b))
    R.row("measures.table", "section 4: every cell equals what the two route tables give, each marked draft", not bad4 and len(got) >= len(want_rows), "; ".join(bad4[:3]))
    R.row("measures.marked", "section 4: every number cell is marked draft", all("(draft)" in c[1] and "(draft)" in c[2] for c in t4 if len(c) == 4 and c[0] != "Measure" and c[0] != "First reward"))
    diff_block = differences_block(routes, meas)
    R.row("measures.differences", "section 3.3 equals the computed differences", diff_block.strip() in sub_section(sec.get("3", ""), r"^### 3\.3"))
    built = meas["status"]
    n_all = sum(built["A"].values()) + sum(built["B"].values())
    share = "%d of its %d beats" % (built["A"]["BUILT"] + built["B"]["BUILT"], n_all)
    R.row("measures.share_built", "section 1 and the page of section 6 say how many beats are BUILT, by the tables' own count (%s)" % share,
          sec.get("1", "").count(share) >= 1 and sec.get("6", "").count(share) >= 1, share)

    tc = "rises in tension for only %d of its %d minutes (route A: %d)" % (meas["tension"]["B"]["rising"], TOTAL, meas["tension"]["A"]["rising"])
    R.row("measures.tension_claim", "the page of section 6 states the tension count the tables give (%s)" % tc, tc in sec.get("6", ""), tc)

    # ---- content
    hits = [h[2] for h in CG.scan(text)]
    R.row("content.gate", "tools/content-gate.py finds nothing in the draft", not hits, str(hits[:5]))
    if full:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, dir=str(HERE), encoding="utf-8") as tf:
            tf.write(text)
            tmp = tf.name
        try:
            r = subprocess.run([sys.executable, str(REPO / "tools" / "canon-gate.py"), tmp], cwd=REPO, capture_output=True, text=True, timeout=300)
            tail = ((r.stdout.strip().split("\n") or [""])[-1]).strip()
            R.row("content.canon_gate", "tools/canon-gate.py is clean over the draft", r.returncode == 0, tail)
        finally:
            Path(tmp).unlink()
    R.row("content.no_dash", "no em dash and no en dash", "—" not in text and "–" not in text)
    R.row("content.no_italics", "no italics", not ITALIC_STAR.search(text) and not ITALIC_UND.search(text))
    fp = []
    for n, line in enumerate(text.split("\n"), 1):
        for m in FIRST_PERSON.finditer(strip_for_prose(line)):
            fp.append("line %d: %s" % (n, m.group(0)))
    R.row("content.third_person", "third person outside quotation marks (no I, we, you, my, our)", not fp, "; ".join(fp[:5]))
    nb = prose_names(text)
    R.row("content.names", "no capitalised name in the prose that canon, the town data or the allow list lacks", not nb, "; ".join(nb[:12]))
    ptag = [p for p in ("play" + "ers",) if re.search(r"\b" + p + r"\b", text, re.I)]
    R.row("content.no_barred_word", "the word the canon gate refuses whole does not appear", not ptag)

    # ---- section 2.5 beat references exist
    refs = set(re.findall(r"\b([AB]\d+)\b", sec.get("2", "")))
    have = {r["No"] for l in "AB" for r in routes[l]}
    R.row("frame.refs", "section 2 cites only beats that exist", refs <= have, str(sorted(refs - have)))
    R.row("frame.guess_marked", "the clock and the cost per live exchange are marked guess", "Guess: two game hours" in sec.get("2", "") and "Guess: $0.025" in sec.get("2", ""))

    # ---- section 5
    s5 = sec.get("5", "")
    cites = re.findall(r"\b(PRAISE|PUNISH) (\d+)\b", s5)
    src = PRAISE_FILE.read_text(encoding="utf-8")
    missing = [c for c in cites if not re.search(r"^### %s %s\." % (c[0], c[1]), src, re.M)]
    items = [l for l in s5.split("\n") if l.startswith("- ")]
    noc = [l[:50] for l in items if not re.search(r"\((?:PRAISE|PUNISH|What this changes)", l)]
    R.row("research.cites", "section 5: every line cites a section of the praise-and-punish file and each cited section exists", items and not noc and not missing, "; ".join(noc[:2] + [str(missing)]))
    wi = re.findall(r"What this changes, item (\d+)", s5)
    wi_ok = all(re.search(r"^%s\. " % i, src.split("## What this changes for LEDGER")[1], re.M) for i in wi)
    R.row("research.items", "section 5: every 'What this changes' item cited exists", wi_ok)

    # ---- section 6
    s6 = sec.get("6", "")
    qs = re.findall(r"^- (Q\d+)\. ", s6, re.M)
    qlines = [l for l in s6.split("\n") if re.match(r"^- Q\d+\. ", l)]
    R.row("ask.questions", "section 6: at most five questions, each with a recommended answer", 1 <= len(qs) <= 5 and all("Recommended:" in l for l in qlines), str(qs))
    page = sub_section(s6, r"^### 6\.2")
    pl = [l for l in page.split("\n") if l.startswith("- ")]
    ds = [i for i, l in enumerate(pl) if re.match(r"^- D\d+\. ", l)]
    sh = [i for i, l in enumerate(pl) if l.startswith("- Shortfall")]
    R.row("ask.page", "the page: shortfalls first, then at most three one-line decisions, each recommended",
          1 <= len(ds) <= 3 and sh and max(sh) < min(ds) and all("Recommended" in pl[i] for i in ds))
    defined = set(re.findall(r"^- (P\d+)\. ", sub_section(s6, r"^### 6\.3"), re.M))
    used = set(re.findall(r"\b(P\d+)\b", sec.get("3", "")))
    R.row("ask.proposals", "every proposal for Jafar is defined in 6.3 and used in a beat, and every beat that cites one says 'proposal for Jafar'",
          defined and defined == used and all("proposal for Jafar" in r["Beat"] + r["Status"] for l in "AB" for r in routes[l] if re.search("P[0-9]", r["Beat"])),
          "defined %s, used %s" % (sorted(defined), sorted(used)))
    return R, routes, meas


# ------------------------------------------------------------------ measures

def measures(routes):
    out = {"first": {}, "ui": {}, "acts": {}, "empty": {}, "run": {}, "cut": {}, "live": {}, "hints": {}, "status": {}, "status_min": {},
           "ids": {}, "places": {}}
    for L, rows in routes.items():
        first = {}
        ui = {}
        acts = set()
        empties = 0
        runs, run = [], 0
        cut = 0
        live = 0
        ten = {"rising": 0, "falling": 0, "quiet": 0}
        st = {"BUILT": 0, "DESIGNED": 0, "NOT YET": 0}
        stm = {"BUILT": 0, "DESIGNED": 0, "NOT YET": 0}
        for r in rows:
            timed, other = mark_times(r)
            for name, sec_, piece in timed:
                if name in MARK_TIMED:
                    first.setdefault(name, sec_)
                    first[name] = min(first[name], sec_)
                elif name.startswith("ui:"):
                    ui.setdefault(name[3:], sec_)
                    ui[name[3:]] = min(ui[name[3:]], sec_)
            for tok in other:
                if tok.startswith("act:"):
                    acts.add(tok[4:])
                m = re.match(r"^live:(\d+)$", tok)
                if m:
                    live += int(m.group(1))
            for g in r["groups"]:
                if g == "-":
                    empties += 1
                    run += 1
                else:
                    runs.append(run)
                    run = 0
            for g in r["tension"]:
                if g in ten:
                    ten[g] += 1
            cut += r["cut"] or 0
            word = next((s for s in STATUSES if r["Status"].startswith(s)), "NOT YET")
            st[word] += 1
            stm[word] += r["len"] or 0
        runs.append(run)
        out["first"][L] = first
        out["ui"][L] = ui
        out["acts"][L] = acts
        out["empty"][L] = empties
        out["run"][L] = max(runs)
        out["cut"][L] = cut
        out["live"][L] = live
        out["hints"][L] = sorted((s, n) for n, s in ui.items() if n.endswith("-hint"))
        out["tension"] = out.get("tension", {})
        out["tension"][L] = ten
        out["status"][L] = st
        out["status_min"][L] = stm
        out["ids"][L] = {p.rstrip("*") for r in rows for p in r["who"]}
        out["places"][L] = {w for r in rows for w in r["where"]}
    return out


def measure_rows(m):
    def first(L, k):
        v = m["first"][L].get(k)
        return "none (draft)" if v is None else "%s (draft)" % fmt(v)

    def uis(L):
        return ", ".join("%s %s" % (n, fmt(s)) for n, s in sorted(m["ui"][L].items(), key=lambda kv: kv[1])) + " (draft)"

    rows = [
        ("Time to first control", first("A", "control"), first("B", "control"), "Tom can move; route B skips the shot"),
        ("First free movement", first("A", "move"), first("B", "move"), "he walks away from where he stood"),
        ("First conversation", first("A", "talk"), first("B", "talk"), "he types and is answered"),
        ("First choice", first("A", "choice"), first("B", "choice"), "a decision the town will remember"),
        ("First conflict", first("A", "conflict"), first("B", "conflict"), "a deed against someone or open opposition"),
        ("First consequence", first("A", "consequence"), first("B", "consequence"), "somebody reacts to what he did"),
        ("First reward", "none (draft)", "none (draft)", "no reward system exists"),
        ("Cutscene against play", "%s of %d:00 (draft)" % (fmt(m["cut"]["A"]), TOTAL), "%s of %d:00 (draft)" % (fmt(m["cut"]["B"]), TOTAL), "the skippable arrival shot only"),
        ("Distinct activities", "%d (draft)" % len(m["acts"]["A"]), "%d (draft)" % len(m["acts"]["B"]), "distinct act marks"),
        ("Empty minutes", "%d (draft)" % m["empty"]["A"], "%d (draft)" % m["empty"]["B"], "by the tags"),
        ("Longest stretch with nothing new", "%d min (draft)" % m["run"]["A"], "%d min (draft)" % m["run"]["B"], "consecutive empty minutes"),
        ("Hints shown", "%d, the last at %s (draft)" % (len(m["hints"]["A"]), fmt(m["hints"]["A"][-1][0])), "%d, the last at %s (draft)" % (len(m["hints"]["B"]), fmt(m["hints"]["B"][-1][0])), "each hint shows once"),
        ("First save", first_ui(m, "A", "save"), first_ui(m, "B", "save"), "the morning autosave"),
        ("Live exchanges and cost", "%d, $%.2f (draft)" % (m["live"]["A"], m["live"]["A"] * COST_PER_LIVE), "%d, $%.2f (draft)" % (m["live"]["B"], m["live"]["B"] * COST_PER_LIVE), "at the guess of $0.025 each"),
        ("Interface pieces, first appearance", uis("A"), uis("B"), "by time"),
        ("Minutes rising, falling, quiet", "%d, %d, %d (draft)" % (m["tension"]["A"]["rising"], m["tension"]["A"]["falling"], m["tension"]["A"]["quiet"]),
         "%d, %d, %d (draft)" % (m["tension"]["B"]["rising"], m["tension"]["B"]["falling"], m["tension"]["B"]["quiet"]), "by the tension column"),
        ("Beats BUILT, DESIGNED, NOT YET", "%d, %d, %d (draft)" % (m["status"]["A"]["BUILT"], m["status"]["A"]["DESIGNED"], m["status"]["A"]["NOT YET"]),
         "%d, %d, %d (draft)" % (m["status"]["B"]["BUILT"], m["status"]["B"]["DESIGNED"], m["status"]["B"]["NOT YET"]), "by the weakest link"),
    ]
    return rows


def first_ui(m, L, name):
    v = m["ui"][L].get(name)
    return "none (draft)" if v is None else "%s (draft)" % fmt(v)


def measure_block(meas):
    lines = ["| Measure | Route A | Route B | Note |", "|---|---|---|---|"]
    for label, a, b, note in measure_rows(meas):
        lines.append("| %s | %s | %s | %s |" % (label, a, b, note))
    return "\n".join(lines)


def differences_block(routes, meas):
    ia, ib = meas["ids"]["A"], meas["ids"]["B"]
    named = lambda s: ", ".join("%s (%s)" % (PBYID[x]["heard_as"], x) for x in sorted(s) if x in PBYID)
    pa, pb = meas["places"]["A"], meas["places"]["B"]
    lines = [
        "- People in both routes: %d. Only in A: %s. Only in B: %s." % (len(ia & ib & set(PBYID)), named(ia - ib), named(ib - ia)),
        "- Places only in A: %s. Only in B: %s." % (", ".join(sorted(pa - pb)), ", ".join(sorted(pb - pa))),
        "- A breaks a window and carries two envelopes; B carries none, says one plain no, and is in no crime. A meets the constable and DS Ellis; B meets neither.",
        "- A opens with the 20-second shot and a walk to Sheila's door; B skips it and talks first to Darren. The AI notice comes at A %s and B %s, because it waits for the first chance to talk." % (
            fmt(meas["ui"]["A"]["ai-notice"]), fmt(meas["ui"]["B"]["ai-notice"])),
        "- A's weather turns wet at dusk on Monday and Wednesday; B's stays dry.",
        "- A ends on Thursday night with the police file, a cold step and an arrangement that stands; B ends on Thursday night with an ended arrangement, a kept tea and a name from Sheila.",
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------ negative controls

def negative_controls(text):
    """Damage the draft in memory; each damaged copy must fail the named row. Returns [(name, row prefix, caught, which)]."""
    out = []
    banned = "be" + "er"               # built at run time so no file of ours carries the word
    modern = "smart" + "phone"
    sub = lambda a, b, n=1: text.replace(a, b, n)

    def edit_rows(prefix, fn, src=None):
        """Apply fn(line) to every table line that starts with the prefix ('| B' for route B)."""
        return "\n".join(fn(l) if l.startswith(prefix) else l for l in (src or text).split("\n"))

    def set_cell(src, rid, col, value):
        out = []
        for l in src.split("\n"):
            if l.startswith("| %s |" % rid):
                cells = [c.strip() for c in l.strip().strip("|").split("|")]
                cells[col] = value
                l = "| " + " | ".join(cells) + " |"
            out.append(l)
        return "\n".join(out)

    def run(name, damaged, expect, full=False):
        if damaged == text:
            out.append((name, expect, False, "the damage changed nothing"))
            return
        R, _, _ = all_checks(damaged, full=full)
        failed = [r[0] for r in R.rows if not r[2]]
        hit = [f for f in failed if f.startswith(expect)]
        out.append((name, expect, bool(hit), ", ".join(failed[:4])))

    # a gap in route A (beat A2 starts a minute late)
    run("a gap: beat A2 starts at minute 2 instead of 1", sub("| A2 | 1-2 |", "| A2 | 2-2 |"), "A.coverage")
    run("a gap: route B has its last beat cut away", "\n".join(l for l in text.split("\n") if not l.startswith("| B25 |")), "B.coverage")
    run("an overlap: B3 starts at minute 1", sub("| B3 | 2-3 |", "| B3 | 1-3 |"), "B.coverage")
    run("a wrong clock: A4 says Mon 14:00", sub("| A4 | 3-4 | Mon 15:00 |", "| A4 | 3-4 | Mon 14:00 |"), "A.clock")
    # an unknown person
    run("an unknown person id in a beat's Who", sub("`rocco`, `ferko`, `franjo`, `ada`, `zlata`, `lena`", "`rocco`, `bernard`, `franjo`, `ada`, `zlata`, `lena`"), "A.who_ids")
    run("an unknown person named in the prose", sub("Ron passes close and says low", "Ron passes close and Bernard Cooke says low"), "content.names")
    run("an unknown place id", set_cell(text, "A2", 3, "`the_old_lighthouse`"), "A.where_ids")
    run("a person who is elsewhere at that hour (June in the office on Monday evening)", set_cell(text, "A6", 4, "`rocco`, `zlata`, `dusan`, `june`"), "A.schedules")
    # a forbidden word, in the repository's own two gates
    run("a forbidden word of the content rule in a beat", sub("a plain dark coat", "a plain dark coat and a glass of " + banned), "content.gate")
    run("a modern thing in the era in a beat (canon gate)", sub("a plain dark coat", "a plain dark coat and a " + modern), "content.canon_gate", full=True)
    # em dash and italics
    run("an em dash", sub("Nothing new.", "Nothing new — at all."), "content.no_dash")
    run("italics", sub("Nothing new.", "*Nothing* new."), "content.no_italics")
    run("first person in the prose", sub("The newcomer is", "I think the newcomer is") if "The newcomer is" in text else sub("A person who has never seen LEDGER", "I am a person who has never seen LEDGER"), "content.third_person")
    # empties
    dash = text
    for rid in ("B1", "B2", "B3", "B4", "B5", "B8", "B9"):
        dash = set_cell(dash, rid, 6, "-")
    run("too many empty minutes in route B (tags blanked on seven beats)", dash, "B.empty_cap")
    run("an empty flag that disagrees: a beat of one minute given two tag groups", set_cell(text, "B1", 6, "ISW / IS"), "B.tags")
    # story
    run("no choice in route B", edit_rows("| B", lambda l: l.replace("choice@", "talk@")), "B.choice")
    run("no consequence in route B", edit_rows("| B", lambda l: l.replace("consequence@", "talk@")), "B.consequence")
    run("nothing persists after the restart in route A", re.sub(r" persists:[a-z]+@\d+:\d\d", "", text.split("| A25 |")[0]) + "| A25 |" + re.sub(r" persists:[a-z]+@\d+:\d\d", "", text.split("| A25 |", 1)[1].split("### 3.2")[0]) + "### 3.2" + text.split("### 3.2", 1)[1], "A.restart")
    run("a persisting mark that names no saved piece", sub("persists:damage@29:15", "persists:wishes@29:15"), "A.marks")
    run("too many live exchanges in route B", sub("live:3 act:talk", "live:9 act:talk"), "B.live_cap")
    # measures
    run("a number in section 4 that the tables do not give", sub("| Time to first control | 0:20 (draft)", "| Time to first control | 0:21 (draft)"), "measures.table")
    run("a missing first line", text.split("\n", 1)[1], "shape.first_line")
    run("a placeholder left in", sub("# LEDGER: the first thirty minutes, a first draft", "# LEDGER: the first thirty minutes, a first draft\n\nTODO"), "shape.no_placeholder")
    run("section 5 cites a section that does not exist", sub("(PUNISH 5)", "(PUNISH 77)"), "research.cites")
    run("a proposal used but not defined", sub("(P3, proposal for Jafar: the room behind her window)", "(P9, proposal for Jafar: the room behind her window)"), "ask.proposals")
    return out


def main():
    text = DRAFT.read_text(encoding="utf-8")
    if "--measures" in sys.argv:
        R, routes, meas = all_checks(text, full=False)
        print("SECTION 3.3\n" + differences_block(routes, meas))
        print("\nSECTION 4\n" + measure_block(meas))
        b = meas["status"]
        print("\nstatus A %s B %s" % (b["A"], b["B"]))
        print("people with no card or body in B: %s" % sorted(p for p in meas["ids"]["B"] if p in PBYID and p not in ("lena", "rocco", "sam")))
        return 0
    if "--negative-controls" in sys.argv:
        res = negative_controls(text)
        ok = 0
        for name, expect, caught, failed in res:
            print("%s  %s -> row %s (failed rows: %s)" % ("CAUGHT" if caught else "MISSED", name, expect, failed))
            ok += caught
        print("negative controls: %d of %d caught" % (ok, len(res)))
        return 0 if ok == len(res) else 1
    R, routes, meas = all_checks(text, full=True)
    for rid, label, ok, detail in R.rows:
        print("%s  %s  %s%s" % ("pass" if ok else "FAIL", rid, label, "" if ok else "  [" + detail + "]"))
    n_ok, n = R.tally()
    print("%d of %d rows pass" % (n_ok, n))
    return 0 if n_ok == n else 1


if __name__ == "__main__":
    sys.exit(main())
