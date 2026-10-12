#!/usr/bin/env python3
"""Assembles people.json from authored/*.py and the homes (unit 11, cloud week 42).

    python3 build_people.py            # writes people.json next to this file

What it does, in plain words:
  * every fact copied from a home is found in the home's file (a quote that is not
    there stops the build), so each citation is a real line and the fact is word for word;
  * schedules and ties are derived from production/specs/hook-cast.json for everyone
    who has a routine there, never retyped; the nine who have none carry proposals;
  * everything with no home is marked new, with a group that DECISIONS.md names.
Light: standard library only, a few seconds.
"""
import importlib
import json
import pkgutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import town_lib as T  # noqa: E402

GROUPS = {
    "N-LIVES": {"title": "Small beliefs, sightings and trade knowledge of the street's people, and how they feel about those they talk to",
                "decisions_key": "small beliefs, sightings and trade knowledge"},
    "N-RIVALS": {"title": "What the three heads, the detective and the Fixer know and believe at the baseline, where canon and the story are silent",
                 "decisions_key": "the three heads, the detective and the Fixer"},
    "N-SCHEDULES": {"title": "Schedules, places and ties for the nine people with no routine in hook-cast.json",
                    "decisions_key": "the nine people with no routine"},
    "N-RUMOURS": {"title": "The rumours: five a person, each a rewording of facts the person holds, with who tells whom",
                  "decisions_key": "five rumours a person"},
    "N-ANSWERS": {"title": "A newcomer's ten likeliest questions and the answers, in each person's voice",
                  "decisions_key": "ten likeliest questions"},
    "N-MICKEY": {"title": "Which regulars knew Mickey, and so may say the two approved lines about him",
                 "decisions_key": "which regulars knew Mickey"},
}

OUT = Path(__file__).resolve().parent / "people.json"


def load_authored():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import authored
    people, places = [], {}
    for m in pkgutil.iter_modules(authored.__path__):
        mod = importlib.import_module("authored." + m.name)
        people.extend(getattr(mod, "PEOPLE", []))
        places.update(getattr(mod, "PLACES", {}))
    return people, places


def src_dict(path, quote, near=None):
    a, b = T.locate(path, quote, near)
    return {"file": path, "line": a, "end": b}


def hk_area_line(area):
    lines = T._lines(T.ALIASES["HK"])
    in_areas = False
    for i, l in enumerate(lines, 1):
        if l.startswith(' "areas": {'):
            in_areas = True
        if in_areas and l.startswith('  "%s": {' % area):
            return i
    raise SystemExit("no area " + area)


def resolve_basis(b):
    if b is None:
        return None
    if "basis_src" in b:
        alias, quote = b["basis_src"]
        out = {"src": src_dict(T.path_of(alias), quote)}
        if b.get("note"):
            out["note"] = b["note"]
        return out
    return {"note": b["basis_note"]}


def build_person(p, sf, proposed_places):
    pid = p["id"]
    facts = []
    keymap = {}
    counters = {"knows": 0, "believes": 0, "saw": 0}

    def add(f):
        counters[f["kind"]] += 1
        letter = {"knows": "k", "believes": "b", "saw": "s"}[f["kind"]]
        f["id"] = "%s.%s%02d" % (pid, letter, counters[f["kind"]])
        if f["key"] in keymap:
            raise SystemExit("duplicate key %s for %s" % (f["key"], pid))
        keymap[f["key"]] = f["id"]
        facts.append(f)

    # 1. the street's plain facts this person holds (StreetFacts.cs)
    ids = list(p["street"])
    for sid in ids:
        s = sf[sid]
        text = s["own"] if (s["about"] == pid and s["own"]) else s["fact"]
        add({"key": sid, "kind": "knows", "text": text, "src": src_dict(T.ALIASES["SF"], text), "street": sid, "secret": False})
    # 1b. who they are, in the home's own words (the role cell or line)
    ralias, rquote = p["role"]
    add({"key": "job", "kind": "knows", "text": rquote, "src": src_dict(T.path_of(ralias), rquote), "secret": False, "via": "who and what they are, as their home gives it"})
    # 2. the rest, in the order written (knows, then who they talk to, then believes and saw)
    ties_early = T.derive_ties(pid) if T.hk_person(pid) else []

    def who_facts():
        out = []
        for t in ties_early:
            other = T.hk_person(t["who"])
            called = other["called"]
            line = None
            ol = T.hk_person_line(t["who"])
            for i in range(ol, ol + 8):
                if T._lines(T.ALIASES["HK"])[i - 1].strip().startswith('"called": '):
                    line = i
                    break
            out.append(T.Spec(key="who_" + t["who"], kind="knows", src=("HK", called, line), secret=False,
                              via="who %s is, as the home describes them (hook-cast.json, the tie of %s)" % (t["who"], t["weight"])))
        return out

    for f in p["knows"] + who_facts() + p["believes"] + p["saw"]:
        out = {"key": f["key"], "kind": f["kind"], "secret": bool(f.get("secret"))}
        if "src" in f:
            alias, quote, near = f["src"]
            path = T.path_of(alias)
            out["text"] = quote
            out["src"] = src_dict(path, quote, near)
            if f.get("via"):
                out["via"] = f["via"]
        elif "new" in f:
            if f["new"] not in GROUPS:
                raise SystemExit("unknown group " + f["new"])
            out["text"] = f["text"]
            out["new"] = f["new"]
            out["why"] = f["why"]
        elif "derived" in f:
            how = f["derived"]
            if how == "day":
                out["text"] = T.render_day_fact(pid)
                out["derived"] = {"file": T.ALIASES["HK"], "line": T.hk_person_line(pid), "how": "day"}
            elif how == "hours":
                out["text"] = T.render_hours(f["arg"])
                out["derived"] = {"file": T.ALIASES["HK"], "line": hk_area_line(f["arg"]), "how": "hours", "area": f["arg"]}
            else:
                raise SystemExit("bad derived")
        if f["kind"] == "believes":
            out["truth"] = f["truth"]
            out["truth_basis"] = resolve_basis(f["basis"])
        if f["kind"] == "saw":
            out["when"] = f["when"]
        add(out)

    # the person's identity and role, copied from their home
    ialias, iquote = p["identity"]
    ident = src_dict(T.path_of(ialias), iquote)
    ralias, rquote = p["role"]
    role = {"text": rquote, "src": src_dict(T.path_of(ralias), rquote)}

    # schedule: derived from the home when there is a routine, else the proposal
    sched = T.derive_schedule(pid)
    overridden = False
    if p["schedule"] is not None:
        if sched is not None:
            # a sheet outranks hook-cast: the proposal replaces the home's routine, and says so
            overridden = True
            home = sched
            sched = dict(p["schedule"])
            sched["overrides"] = {"file": T.ALIASES["HK"], "line": home["source"]["line"], "why": p["extra"].get("override_why", "")}
        else:
            sched = dict(p["schedule"])
    if sched is None:
        raise SystemExit("no schedule for " + pid)
    # ties
    ties = T.derive_ties(pid) if T.hk_person(pid) else []
    if overridden:
        for t in ties:
            o = T.hk_person(t["who"])
            if o:
                t["hours_a_week"] = T.hours_together_sched(sched, T.derive_schedule(t["who"]))
                t["hours_note"] = "computed from the proposed schedule, which replaces the routine in hook-cast.json"
    if not T.hk_person(pid) and not p["tom_exception"]:
        ties = T.propose_ties(pid, sched)
        for t in ties:
            t["other_role"] = T.hk_person(t["who"])["role"]
            t["crowd"] = None
    colours = p["talks"]
    for t in ties:
        if t["who"] in colours:
            t["colour"] = colours[t["who"]]
        t["crowd"] = None
        other = T.hk_person(t["who"])
        t["other_role"] = other["role"] if other else None
    for t in p["extra"].get("ties_new", []):
        sq = t["source"]
        if isinstance(sq, dict) and "_q" in sq:
            alias, quote = sq["_q"]
            t["source"] = src_dict(T.path_of(alias), quote)
        dup = next((x for x in ties if x["who"] == t["who"]), None)
        if dup is not None:
            # the story's own tie and the computed one are the same pair: keep the computed hours, add the story's reason
            dup["story_tie"] = {"band": t.get("band"), "meets": t.get("meets"), "source": t.get("source")}
            continue
        ties.append(t)
    for t in ties:
        t["feeling"] = t.get("band")

    rumours = []
    for i, r in enumerate(p["rumours"], 1):
        on = []
        for k in r["on"]:
            if k not in keymap:
                raise SystemExit("rumour of %s rests on unknown fact %s" % (pid, k))
            on.append(keymap[k])
        rumours.append({"id": "%s.r%d" % (pid, i), "gist": r["gist"], "truth": r["truth"], "truth_basis": resolve_basis(r["basis"]), "sure": r["sure"],
                        "heard_from": r["frm"], "would_pass_to": r["to"], "based_on": on, "limits": r["limits"], "new": "N-RUMOURS"})
    questions = []
    for i, q in enumerate(p["questions"], 1):
        uses = []
        for k in q["uses"]:
            if k not in keymap:
                raise SystemExit("answer of %s uses unknown fact %s (%s)" % (pid, k, q["q"]))
            uses.append(keymap[k])
        questions.append({"id": "%s.q%d" % (pid, i), "q": q["q"], "kind": q["kind"], "a": q["a"], "uses": uses,
                          **({"bench": q["bench"]} if q.get("bench") else {}), "new": "N-ANSWERS"})
    entry = {"id": pid, "name": p["name"], "heard_as": p["heard_as"], "tier": p["tier"], "age": p["age"], "role": role,
             "identity_src": ident, "knew_mickey": p["knew_mickey"], "facts": facts, "schedule": sched, "talks_to": ties,
             "rumours": rumours, "newcomer_questions": questions}
    if p["tom_exception"]:
        entry["tom_exception"] = "The player's words are typed, never authored (casting/tom-nowak/SHEET.md); no questions are written for Tom."
    if p["internal_id_note"]:
        entry["id_note"] = p["internal_id_note"]
    if p["extra"].get("note"):
        entry["note"] = p["extra"]["note"]
    return entry


def main():
    sf = T.street_facts()
    people, places = load_authored()
    out_people = [build_person(p, sf, places) for p in people]
    street_index = {sid: {"text": s["fact"], "about": s["about"], "src": src_dict(T.ALIASES["SF"], s["fact"])} for sid, s in sf.items()}
    doc = {
        "version": "v1",
        "made": "13 Oct 2026, cloud week 42, unit 11 (town content)",
        "status": "A PROPOSAL for the PC session. Homes are in HOMES.md. Nothing here is in the game. Every fact is either copied word for word from its home with file and line, derived by script from a home, or marked new with a group Jafar sees in DECISIONS.md.",
        "groups": GROUPS,
        "limits": __import__("authored.common", fromlist=["LIMITS"]).LIMITS,
        "proposed_places": T.PROPOSED_PLACES,
        "street_facts": street_index,
        "people": out_people,
    }
    OUT.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    nf = sum(len(p["facts"]) for p in out_people)
    nn = sum(1 for p in out_people for f in p["facts"] if f.get("new"))
    nr = sum(len(p["rumours"]) for p in out_people)
    nq = sum(len(p["newcomer_questions"]) for p in out_people)
    print("people.json: %d people, %d facts (%d new, %d sourced or derived), %d rumours, %d answers" % (len(out_people), nf, nn, nf - nn, nr, nq))


if __name__ == "__main__":
    main()
