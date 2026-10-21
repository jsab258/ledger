#!/usr/bin/env python3
"""Assembles lines.json and rules.json from authored/*.py (unit 12, cloud week 42).

    python3 build_lines.py            # writes lines.json and rules.json next to this file

lines.json is a dialogue bank in the shape of content/dialogue/crime-witness-v1.json (bank, license, era,
register, rungs, speakers, lines with id, context, rung, speaker, text), extended with what ambient talk needs
(situation, kind, conditions, weight, group, delivery, dialect). The authored files hold the words only;
everything else is derived here, never retyped, and check_lines.py re-reads it all and does not trust this file.
Standard library only; takes a second.
"""
import importlib
import json
import re
import sys
sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lines_lib as L  # noqa: E402
from rules_source import RULES  # noqa: E402

OUT = HERE / "lines.json"
OUT_RULES = HERE / "rules.json"
MADE = "13 Oct 2026, cloud week 42, unit 12"


POLICE = re.compile(r"\b(police|guards|station|ring|telephone|radio it in)\b", re.I)


def dialect_of(text):
    low = " " + L.norm_text(text) + " "
    for m in L.DIALECT_MARKERS:
        if " " + m + " " in low:
            return "local"
    return "plain"


def build_line(kind, sit, dest, idx, raw):
    text, tag = L.parse_line(raw)
    s = L.SITUATIONS[sit]
    cond = {}
    if sit.startswith("greeting."):
        cond["standing"] = [s["rung"]]
    if sit.startswith("crime_"):
        cond["sure"] = sit.split("_", 1)[1]
    if sit == "after_deed":
        cond["since_deed_s"] = [0, 3600]
    if sit == "rain_starts":
        cond["weather"] = ["drizzle", "rain"]
        cond["rain_began_within_s"] = 40
    if sit == "in_rain":
        cond["weather"] = ["drizzle", "rain"]
    if sit == "asked_way" and dest:
        cond["destination"] = dest
    for k, v in tag.items():
        if k in ("weight", "delivery"):
            continue
        if k == "weather" and "weather" in cond:
            cond["weather"] = [w for w in cond["weather"] if w in v]
        else:
            cond[k] = v
    bank = s["bank"] + ("/to/" + dest if dest else "")
    short = s["short"] + ("-" + dest.replace("_", "-") if dest else "")
    delivery = tag.get("delivery") or ("hushed" if sit == "after_deed" else "normal")
    line = {
        "id": "%s.%s.%02d" % (kind, short, idx),
        "bank": bank,
        "context": s["context"],
        "situation": sit,
        "kind": kind,
        "speaker": kind,
        "rung": s["rung"],
    }
    if sit.startswith("crime_"):
        line["idRung"] = L.SURE[cond["sure"]]
    line.update({
        "text": text,
        "conditions": cond,
        "weight": tag.get("weight", 2),
        "group": "%s@%s" % (bank, kind),
        "delivery": delivery,
        "dialect": dialect_of(text),
    })
    if POLICE.search(text):
        line["calls_police"] = True
    return line


def load_authored():
    import authored
    out = {}
    for k in L.KIND_ORDER + [L.ANYONE]:
        mod = importlib.import_module("authored." + k)
        out[k] = mod
    return out


def main():
    mods = load_authored()
    lines = []
    for kind in L.KIND_ORDER:
        mod = mods[kind]
        for sit in L.SITUATIONS:
            for i, raw in enumerate(getattr(mod, "LINES", {}).get(sit, []), 1):
                lines.append(build_line(kind, sit, None, i, raw))
    way = getattr(mods[L.ANYONE], "WAY", {})
    for d in L.DESTS:
        for i, raw in enumerate(way.get(d["id"], []), 1):
            lines.append(build_line(L.ANYONE, "asked_way", d["id"], i, raw))
    speakers = {}
    for k in L.KIND_ORDER:
        v = L.KINDS[k]
        speakers[k] = {"what": v["desc"], "members": v["members"], "trades": v["trades"], "voice": v["voice"],
                       "own": v["own"], "greeting_rungs": v["rungs"]}
    speakers[L.ANYONE] = {"what": "any resident who knows the place: the shared directions, one set of words per place (a place's facts are the place's, not a kind's)",
                          "members": [], "trades": [], "voice": "any", "own": False, "greeting_rungs": []}
    doc = {
        "bank": "ambient-lines-v1",
        "license": "original-work: authored for LEDGER in this repository, no external source",
        "era": "1988-1992",
        "register": "D3: dry British wit, seaside-postcard smut sparingly, noir holds (canon, Tone); spoken lines, British 1990",
        "status": "PROPOSED, not in the game: a proposed addition for the PC session to adopt after its tests (NOTES.md says how). Unreviewed by a fresh reader; dialogue, so on Jafar's page before it merges.",
        "made": MADE,
        "fields": {
            "id": "kind.situation.nn, unique",
            "bank": "the existing street-lines bank key (StreetVoice.cs 'ambient/open/night', 'recognition/avoids'): the ledger keeps 'bank@kind' exactly as it keeps 'bank@id' for OwnLines",
            "context": "the family of moment (greeting, bump, rain, crime, deed, way, farewell), as the dialogue bank's own context",
            "situation": "the moment itself; kind is who says it; speaker repeats kind because the dialogue bank's own field is called speaker (check_lines.py requires them equal)",
            "rung": "the standing rung a greeting reads out (stranger, owner, nowak, tom, tommy), else any: the dialogue bank's own field",
            "idRung": "crime lines only: how sure the speaker is, on the dialogue bank's identification ladder: 0 a noise heard, 1 a shape, 3 a face (2 and 4 have no ambient lines: see NOTES.md)",
            "conditions": "every key present must hold: standing (rungs), weather (dry, drizzle, rain), time (morning, afternoon, evening, night), sure (noise, shape, face), destination (a place id), since_deed_s ([from, to]), rain_began_within_s",
            "weight": "1 to 3: the chance of being drawn next among the lines not yet used in the group's bag; every line is still used once per bag",
            "group": "the cooldown group and the shuffle bag: one per kind and bank, the ledger's own key",
            "delivery": "normal, hushed (witnesses quieter for an hour: RULINGS 23 Sep) or raised",
            "dialect": "local if the line uses a northern dialect word: never given to a speaker whose voice is not the local one",
            "calls_police": "present and true if the line rings, tells or fetches the police: never given to the people who never go to them (rules.json speaker_overrides.never_police)",
        },
        "rungs": L.RUNGS,
        "contexts": ["greeting", "bump", "rain", "crime", "deed", "way", "farewell"],
        "situations": list(L.SITUATIONS),
        "idRungs": [0, 1, 3],
        "weather": L.WEATHER_BANDS,
        "time": L.TIME_BANDS,
        "speakers": speakers,
        "no_kind": L.NO_KIND,
        "places": [{"id": d["id"], "names": d["names"], "x_m": d["x"], "z_m": d["z"], "class": L.dest_class(d), "far": L.dest_far(d), "src": d["src"]} for d in L.DESTS],
        "location": "Quay Street, the Hook, and the town's places",
        "lines": lines,
    }
    # one line to a row, like the dialogue banks: readable in a diff, small in git
    head = {k: v for k, v in doc.items() if k != "lines"}
    text = json.dumps(head, indent=1, ensure_ascii=False)
    text = text[:-2] + ',\n "lines": [\n' + ",\n".join("  " + json.dumps(l, ensure_ascii=False) for l in lines) + "\n ]\n}\n"
    OUT.write_text(text, encoding="utf-8")
    rules = dict(RULES)
    rules["trade_kinds"] = {t: k for k, v in L.KINDS.items() for t in v["trades"]}
    rules["person_kinds"] = dict(L.PERSON_KIND)
    OUT_RULES.write_text(json.dumps(rules, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s: %d lines, %d kinds" % (OUT.name, len(lines), len({l['kind'] for l in lines})))


if __name__ == "__main__":
    main()
