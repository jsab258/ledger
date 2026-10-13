#!/usr/bin/env python3
"""Turns lines.json into the street's existing bark shapes (unit 12, cloud week 42). Standard library only.

    python3 export_slots.py                      # prints the voice plan's numbers
    python3 export_slots.py --slots out.json     # writes the slots in game-design/barks.json's shape
    python3 export_slots.py --renders out.json   # writes the renders in barks-manifest.json's shape (a clip per voice and line)

The street already has two derived views of its lines: game-design/barks.json (one slot per bank: id, family, brief,
everySeconds, wanted, have, lines; made by BarkGen) and the voice manifest (slot, index, line, voice, file; the file is
VoiceBank.ClipName: voice/FNV-1a of voice, a unit separator and the line). This writes the same two shapes from lines.json, so the
bank is not a second format. Nothing is stored: lines.json stays the one home, and these are made when the PC session wants them.

The voice plan (which voice speaks which kind) is the one in NOTES.md: Ron, Darren, Sheila and the dispatcher have their game
voices; June and Father Walsh wait for his yes on the listening page; everybody else is one of the six crowd voices, which
VoiceBank.VoiceFor draws by the speaker's id (and, once the speaker's sex is threaded through, by sex).
"""
import json
import sys
sys.dont_write_bytecode = True
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DOC = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))
RULES = json.loads((HERE / "rules.json").read_text(encoding="utf-8"))

SEP = "\u001f"
POOL_M = ["crowd_m1", "crowd_m2", "crowd_m3"]
POOL_F = ["crowd_f1", "crowd_f2", "crowd_f3"]
# RULINGS 3 Oct: the voices in the game; 3 Oct: June, Father Walsh get a listening page, cast only on his yes
GAME_VOICES = {"lena": "sheila_p267", "rocco": "ron_p227", "sam": "darren_p241", "zlata": "dispatcher_p280"}
PENDING = {"june": "june_p277_pending", "emil": "walsh_july_voice_pending"}
# REGULARS.md rows 11, 29, 30: no local-accent crowd voice fits; they need real speakers' references
NO_VOICE_YET = {"vesna", "takeaway_m", "takeaway_f"}
FEMALE = {"lena", "ada", "june", "noor", "iva", "selma", "ines", "marta", "jelena", "marla", "rita", "tibor", "vesna", "magda", "zora", "tanja", "katarina", "bruno", "petra",
          "sanja", "hana", "danica", "cafe", "takeaway_f", "zlata"}


def fnv(s):
    h = 2166136261
    for ch in s:
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def clip_name(voice, text):
    t = " ".join(text.split())
    return "%s/%08x" % (voice, fnv(voice + SEP + t))


def crowd_voice(pid, sexed=True):
    h = fnv(pid)
    if not sexed:
        return (POOL_M if h % 2 == 0 else POOL_F)[(h // 2) % 3]
    return (POOL_F if pid in FEMALE else POOL_M)[h % 3]


def voices_of_kind(kind, sexed=True):
    """The voices that speak this kind: [(person id, voice)]."""
    members = DOC["speakers"][kind]["members"]
    out = []
    for m in members:
        if m in GAME_VOICES:
            out.append((m, GAME_VOICES[m]))
        elif m in PENDING:
            out.append((m, PENDING[m]))
        elif m in NO_VOICE_YET:
            continue
        else:
            out.append((m, crowd_voice(m, sexed)))
    return out


def plan(sexed=True):
    """Per voice: how many clips it needs. A line is rendered in each distinct voice its kind has."""
    lines_by_kind = defaultdict(list)
    for l in DOC["lines"]:
        lines_by_kind[l["kind"]].append(l)
    clips = defaultdict(set)
    per_kind = {}
    for kind, ls in lines_by_kind.items():
        if kind == "anyone":
            # directions: said by any resident who knows the place; rendered in the crowd voices only
            vs = set(POOL_M + POOL_F) if not sexed else set(POOL_M + POOL_F)
        else:
            vs = {v for _, v in voices_of_kind(kind, sexed)}
        per_kind[kind] = sorted(vs)
        for l in ls:
            for v in vs:
                if v.endswith("_pending") and False:
                    continue
                if l["dialect"] == "local" and False:
                    continue
                clips[v].add(clip_name(v, l["text"]))
    return per_kind, {v: len(c) for v, c in sorted(clips.items())}


def slots():
    out = []
    by = defaultdict(list)
    for l in DOC["lines"]:
        by[l["group"]].append(l)
    fam = RULES["cooldowns"]["per_family"]
    famkey = {"greeting": "greet", "bump": "bump", "rain": None, "crime": "crime", "deed": "after_deed", "way": "way", "farewell": "farewell"}
    for g, ls in sorted(by.items()):
        l0 = ls[0]
        sid = g.replace("/", ".").replace("@", ".")
        f = {"greeting": "greet", "bumped": "bump", "rain_starts": "rain_starts", "in_rain": "in_rain", "crime_noise": "crime", "crime_shape": "crime", "crime_face": "crime",
             "after_deed": "after_deed", "asked_way": "way", "farewell": "farewell"}["greeting" if l0["situation"].startswith("greeting") else l0["situation"]]
        out.append({
            "id": sid,
            "family": "AMBIENT, %s: %s" % (l0["context"].upper(), l0["situation"]),
            "brief": "Said by a %s (%s). Conditions are in lines.json; these are the words." % (l0["kind"], DOC["speakers"][l0["kind"]]["what"]),
            "everySeconds": fam[f]["gap_s"]["value"] or 4,
            "wanted": 13 if l0["situation"] == "greeting.stranger" else 8,
            "have": len(ls),
            "lines": [l["text"] for l in ls],
        })
    return {"generatedBy": "export_slots.py, from production/cloud-week/lines/lines.json (not authored here)", "repeatFloorSeconds": RULES["cooldowns"]["per_line"]["same_speaker_same_line_s"]["value"], "slots": out}


def renders(sexed=True):
    rows = []
    for l in DOC["lines"]:
        kind = l["kind"]
        vs = sorted({v for _, v in voices_of_kind(kind, sexed)}) if kind != "anyone" else POOL_M + POOL_F
        for v in vs:
            rows.append({"slot": l["group"].replace("/", ".").replace("@", "."), "index": int(l["id"].split(".")[-1]) - 1, "line": l["text"], "voice": v, "file": clip_name(v, l["text"])})
    return {"renders": rows}


if __name__ == "__main__":
    if "--slots" in sys.argv:
        Path(sys.argv[sys.argv.index("--slots") + 1]).write_text(json.dumps(slots(), indent=1, ensure_ascii=False), encoding="utf-8")
    if "--renders" in sys.argv:
        Path(sys.argv[sys.argv.index("--renders") + 1]).write_text(json.dumps(renders(), ensure_ascii=False), encoding="utf-8")
    per_kind, counts = plan(True)
    print("voices per kind (sex known):")
    for k, v in per_kind.items():
        print("  %s: %s" % (k, ", ".join(v)))
    print("clips per voice:", counts, "total", sum(counts.values()))
    per_kind0, counts0 = plan(False)
    print("clips per voice, sex not known (today):", counts0, "total", sum(counts0.values()))
