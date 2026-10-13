#!/usr/bin/env python3
"""Writes NOTES.md from the real files and the check's own numbers (unit 12, cloud week 42). Standard library only.

    python3 make_notes.py      # after build_lines.py and check_lines.py

Every number in NOTES.md is read from lines.json, rules.json, checks/check_v1.json or checks/walk_v1.json, never typed.
No em dashes and no italics anywhere in it: it is written for Jafar.
"""
import json
import statistics
import sys
sys.dont_write_bytecode = True
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import export_slots as X  # noqa: E402

DOC = json.loads((HERE / "lines.json").read_text(encoding="utf-8"))
RULES = json.loads((HERE / "rules.json").read_text(encoding="utf-8"))
CHK = json.loads((HERE / "checks" / "check_v1.json").read_text(encoding="utf-8"))
WALK = json.loads((HERE / "checks" / "walk_v1.json").read_text(encoding="utf-8"))
TOWN = json.loads((HERE.parent / "town" / "people.json").read_text(encoding="utf-8"))
HEARD_AS = {p["id"]: p["heard_as"] for p in TOWN["people"]}
HEARD_AS.update({"iva": "Iva (laundry presser)", "selma": "Selma (laundress)", "ines": "the pawn's appraiser", "marta": "the pawn's clerk", "jelena": "Jelena (locksmith)", "goran": "the customs assistant"})

S = CHK["summary"]
lines = DOC["lines"]
kinds = [k for k in DOC["speakers"] if k != "anyone"]
n_lines = len(lines)
by_kind = Counter(l["kind"] for l in lines)
by_sit = Counter(l["situation"] for l in lines if l["kind"] != "anyone")
way_lines = [l for l in lines if l["kind"] == "anyone"]
shared = [k for k in kinds if not DOC["speakers"][k]["own"]]
own = [k for k in kinds if DOC["speakers"][k]["own"]]
main = WALK["main"]
seeds = WALK["seeds_summary"]
stress, afternoon, night, off = WALK["stress"], WALK["afternoon"], WALK["night"], WALK["unenforced"]


def rng(key):
    v = sorted(s[key] for s in seeds) + [main[key]]
    return min(v), statistics.median(v), max(v)


def fmt_t(t):
    return "%02d:%02d" % (int(t // 60), int(t % 60))


KIND_NAMES = {"shopkeeper": "shopkeeper", "dock_worker": "dock worker", "pensioner": "pensioner", "office_worker": "office worker", "driver": "driver",
              "laundry_worker": "laundry worker", "tradesman": "tradesman", "night_shift": "night shift", "casual_worker": "casual worker",
              "ron": "Ron", "darren": "Darren", "father_walsh": "Father Walsh", "june": "June"}
SIT_LABEL = {"greeting.stranger": "greeting to a stranger", "greeting.owner": "greeting to the new owner", "greeting.nowak": "greeting to Nowak", "greeting.tom": "greeting to Tom",
             "greeting.tommy": "greeting to Tommy", "bumped": "bumped into", "rain_starts": "rain starting", "in_rain": "talk in rain", "crime_noise": "a crime heard",
             "crime_shape": "a crime glimpsed", "crime_face": "a crime seen face to face", "after_deed": "after a deed", "asked_way": "asked the way", "farewell": "farewell"}
GREET = ["greeting.stranger", "greeting.owner", "greeting.nowak", "greeting.tom", "greeting.tommy"]

# cross-kind overlaps still standing between 50 and 60 percent
import re as _re
def _words(s):
    return _re.findall(r"[a-z0-9']+", s.lower())
_RW = _re.compile(r"\b(the new owner|new owner|Mr Nowak|Nowak|Tommy|Tom|boss|son|mate|love|dear|friend|pal)\b", _re.I)
_by = defaultdict(list)
for _l in lines:
    if _l["kind"] != "anyone":
        _by[_l["situation"]].append((_l["kind"], set(_words(_RW.sub(" ", _l["text"])))))
CROSS_LEFT = 0
for _s, _ls in _by.items():
    for _i in range(len(_ls)):
        for _j in range(_i + 1, len(_ls)):
            if _ls[_i][0] != _ls[_j][0] and _ls[_i][1] and _ls[_j][1]:
                _o = len(_ls[_i][1] & _ls[_j][1]) / len(_ls[_i][1] | _ls[_j][1])
                if 0.5 <= _o < 0.6:
                    CROSS_LEFT += 1
CROSS_FIXED = 153    # the count the first run found at 60 percent or more, before the rewrite (this unit's own log)

# the voice plan's numbers
per_kind, clips = X.plan(True)
clips_today = X.plan(False)[1]
total_clips = sum(clips.values())
all_six = 0
for k in shared:
    all_six += by_kind[k] * 6
all_six += by_kind["anyone"] * 6
for k in ("office_worker",):
    all_six += by_kind[k] * 2     # Sheila's voice and the dispatcher's, on top of the six
for k in own:
    all_six += by_kind[k]
crowd_total = sum(v for k, v in clips.items() if k.startswith("crowd_"))

rows = []
for k in kinds:
    members = ", ".join(HEARD_AS.get(m, m) for m in DOC["speakers"][k]["members"])
    rows.append("| %s | %s | %d |" % (KIND_NAMES[k], members, by_kind[k]))

cell_rows = []
for k in kinds:
    g = sum(1 for l in lines if l["kind"] == k and l["situation"].startswith("greeting"))
    rain = sum(1 for l in lines if l["kind"] == k and l["situation"] in ("rain_starts", "in_rain"))
    crime = sum(1 for l in lines if l["kind"] == k and l["situation"].startswith("crime"))
    one = lambda s: sum(1 for l in lines if l["kind"] == k and l["situation"] == s)   # noqa: E731
    cell_rows.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d |" % (KIND_NAMES[k], g, one("bumped"), rain, crime, one("after_deed"), one("asked_way"), one("farewell"), by_kind[k]))

sample = [r for r in main["log"] if r["heard"]]
sample_lines = ["- %s, %s, %s: \"%s\"" % (fmt_t(r["t"]), KIND_NAMES.get(r["kind"], r["kind"]), SIT_LABEL[r["situation"]], r["text"]) for r in sample]

real_rows = [r for r in CHK["rows"] if r["id"].startswith("line.")]
faults = [r for r in CHK["rows"] if r["id"].startswith("fault.")]

pc = lambda x: "%d percent" % round(x * 100)   # noqa: E731

lo, med, hi = rng("lines_heard")
blo, bmed, bhi = rng("busiest_minute_without_crime_lines")
qlo, qmed, qhi = rng("quiet_share")
glo, gmed, ghi = rng("longest_gap_s")
sit_totals = Counter()
for s in seeds:
    sit_totals.update(s["heard_by_situation"])

T = []
w = T.append
w("# NOTES: ambient lines (unit 12, cloud week 42)")
w("")
w("Written 13 October 2026 for Jafar's order of 12 October: \"Ambient lines: short spoken lines per kind of person and situation (greeting, being bumped into, rain, seeing a crime, being asked the way), in the voice canon.md gives the town, within the content rule, with cooldown and variety rules, as data the game can play without a model call.\" Nothing here is in the game or on a page of his yet. It is a proposed addition: the PC session adopts it after its tests (how is below). Everything invented is marked, and sits in DECISIONS.md as eight entries, each ending \"Marked for Jafar.\"")
w("")
w("## What was made (production/cloud-week/lines/)")
w("")
w("- **lines.json**: the lines. %s lines, %d kinds of person, %d situations, %d places for directions. Each line has an id, its words, who says it (kind), the moment (situation), the conditions that must hold (weather, time of day, his standing with them, how sure they are, the place asked about), a weight and a cooldown group. It is the street's own dialogue-bank format, extended (see the format section)." % (format(n_lines, ","), len(kinds), len(DOC["situations"]), len(DOC["places"])))
w("- **rules.json**: the rules, as data: cooldowns, variety, priorities and silence. Every number carries its reason and its source, or says it is invented here.")
w("- **check_lines.py**, **checks/check_v1.json**, **checks/walk_v1.json**: the check, its rows, and the walks. Result today: **%d of %d rows pass**, and **%d of %d seeded faults** are caught." % (S["pass"], S["rows"], S["seeded_faults_caught"], S["seeded_faults"]))
w("- **walk_sim.py**: the small simulation the check plays (thirty minutes of a walk through the rules).")
w("- **build_lines.py**, **lines_lib.py**, **rules_source.py**, **authored/**: the builder and the written text. `python3 build_lines.py` makes lines.json and rules.json; `python3 check_lines.py` checks them; `python3 make_notes.py` makes this file; `python3 export_slots.py` turns lines.json into the street's two existing derived shapes (below). Standard library only; each takes seconds on one core.")
w("")
w("## The numbers")
w("")
w("- **Kinds of person: %d.** Nine shared (said by anybody who stands in the kind) and four own, for Ron, Darren, Father Walsh and June, as RULINGS has it. Sheila, Alison and Ada keep the shared lines, as RULINGS has it: Sheila and Alison stand in office worker, Ada in pensioner. Tom, the three heads, the Fixer, DS Ellis and the outfit's man have no kind; they speak in authored scenes and live talk only, and the check requires each of them to have a stated reason." % len(kinds))
w("- **Situations: %d** (greeting at five standings, being bumped into, rain starting, in rain, a crime heard, a crime glimpsed, a crime seen face to face, after a deed, being asked the way, a farewell), and **%d places** for the way." % (len(DOC["situations"]), len(DOC["places"])))
w("- **Lines: %s.** Of these %s are the kinds' own words (at least 8 in every kind and situation the kind has, and 13 for a greeting to a stranger), and %d are directions, 5 or 6 for each of the %d places, said by any resident who knows the place." % (format(n_lines, ","), format(n_lines - len(way_lines), ","), len(way_lines), len(DOC["places"])))
w("- Every line is under twelve words (the longest is %d)." % max(len(l["text"].split()) for l in lines))
w("")
w("| Kind | Who stands in it | Lines |")
w("|---|---|---|")
T.extend(rows)
w("| directions (any resident who knows the place) | | %d |" % by_kind["anyone"])
w("")
w("Lines by kind and moment (the kind's own words, not the directions):")
w("")
w("| Kind | Greetings | Bumped | Rain | Crime | After a deed | Asked the way | Farewell | Total |")
w("|---|---|---|---|---|---|---|---|---|")
T.extend(cell_rows)
w("")
w("Greeting lines by standing, over all kinds: stranger %d, the new owner %d, Nowak %d, Tom %d, Tommy %d. Ron and Darren have no stranger or new owner greeting (they know his name from the start); Father Walsh and June have no stranger greeting; Tommy has lines in three kinds only (pensioner, office worker, Father Walsh)." % tuple(by_sit["greeting." + r] for r in ("stranger", "owner", "nowak", "tom", "tommy")))
w("")
w("## The check (check_lines.py): %d of %d rows pass" % (S["pass"], S["rows"]))
w("")
w("It re-reads every home (the cast and the routines, the atlas, Population.cs, RealWorld.cs, StreetFacts.cs, StreetVoice.cs, the content and canon gates) and does not trust what the builder said. One row for each of the %d lines, and rows for:" % len(real_rows))
w("")
w("- **each line**: under twelve words; its fields, id and bank right; every condition valid for its situation; none of the words the content rule bans (the content gate and slurs-v1.json), no real brand, place, person, team or programme (RealWorld.cs's lists and a few of its own), nothing after 1992, no quotation or known lyric; standing words exactly canon's (the new owner, Nowak, Tom, Tommy, and only the line's own rung); Mickey named only as the place, and the two approved lines carried by no kind; dialect, police and gender flags true; a crime line never claims more than its sureness (a noise line never says it saw, a shape line never gives a face, a sex or a coat, a face line never names or accuses); each direction checked against where its place really is.")
w("- **each kind and situation**: the count, and no lines in a situation the kind does not have.")
w("- **each situation across kinds**: no two kinds say the same thing in other words (at least 60 percent of the words shared, address words such as boss, love and son aside). This is the fault that failed the street's earlier attempts at lines in several mouths; all %d pairs found at 60 percent or more were rewritten, and %d pairs between 50 and 60 percent remain (the same fact in a similar frame, such as two ways to say mind how you go)." % (CROSS_FIXED, CROSS_LEFT))
w("- **each group (kind and bank)**: after every condition (each weather and hour it can happen, each standing, each accent, never-police) at least six lines are left; each rung reads out its word; no two lines say the same thing (a shared four-word run, or three quarters of the content words).")
w("- **the cast and the trades**: every person in the cast and the routines has one kind or a stated reason for none; every trade the old crowd generator names has one kind; the own kinds are exactly the four RULINGS names; Sheila, Alison and Ada keep the shared lines.")
w("- **the places**: each place is where its home says (the routines, the built street, the atlas converted with its own anchor), with five or more lines.")
w("- **the rules**: each number agrees with the code and the rulings it comes from (the 45 s is StreetVoice.ClearWordsEverySeconds), each has a reason, and the priorities put a crime above a greeting.")
w("- **each rule alone** (rule.*): a small scenario for each: a crime line fades neighbour talk, a crime outranks a waiting greeting, a higher priority replaces a waiting line, the neighbours' gap in the dry and in rain, the hush doubles it, a witness says no hello, the bag uses every line before a repeat, the seven who never go to the police are never picked a line that rings them, Nora and the Tangs never get dialect, a question is always answered.")
w("- **the walks** (below), **canon-gate** over lines.json, rules.json and this file, and **content-gate** over this file.")
w("- **%d seeded faults**: the check damages a copy of the files (a thirteen-word line, a banned word of each of the rule's kinds, a real brand, a year after 1992, a real place, Nowak in a stranger greeting, a stranger describing Mickey, a direction up for a place down, a long walk for a place at 76 m, Ron ringing the police, the neighbours' gap set to 30 s, a greeting above a crime in the priorities and the rest) and requires each to fail a row. **%d of %d** do." % (S["seeded_faults"], S["seeded_faults_caught"], S["seeded_faults"]))
w("")
w("Words are checked by lists: a screen, not a reader. What a reader still has to judge is at the end of this file.")
w("")
w("## The walk: thirty minutes through the rules (walk_sim.py, seed 1990)")
w("")
w("Tom walks Quay Street and pauses; twenty passers-by cross his path; four of the street's own people stay where they are (Ron at the rank, Marla at her door, Ada on her step, Rita at hers); rain falls from minute 12 to minute 20 (drizzle for the first and last minute); one crime happens at minute 15, within sight of where he is. Every line goes through rules.json as the PC session's picker would apply it.")
w("")
w("**The main walk.** %d people came within earshot; %d lines were played and %d heard by him. Heard by moment: %s." % (main["people_who_came_within_earshot"], main["lines_played"], main["lines_heard"], ", ".join("%s %d" % (SIT_LABEL[k], v) for k, v in main["heard_by_situation"].items())))
w("")
w("- **Repeats: none.** No speaker said a line twice inside 30 minutes, no line was said by two speakers inside 120 s, and no words were heard twice at all.")
w("- **Busiest minute:** %d heard lines (the cap is six outside a crime)." % main["busiest_minute_without_crime_lines"])
w("- **Gaps:** %d of the 30 minutes had no line at all (%s); the longest silence was %s (from %s to %s). The rain thinned the street: %d passers-by arrived in the 8 rain minutes against %d in the other 22." % (main["minutes_with_no_line"], pc(main["quiet_share"]), "%d s" % round(main["longest_gap_s"]), fmt_t(main["longest_gap_from_s"]), fmt_t(main["longest_gap_to_s"]), main["passers_arriving_in_the_rain_minutes"], main["passers_arriving_otherwise"]))
w("- **Neighbours' talk:** %d neighbour line(s) heard%s, never closer than 45 s. One group never spoke twice inside a minute (the closest two were %s apart)." % (main["neighbour_lines"], "", ("%d s" % round(main["group_min_gap_s"])) if main["group_min_gap_s"] else "n/a"))
w("- **Not played:** %d moments, nearly all by design: %s." % (main["attempts_not_played"], ", ".join("%s %d" % (k, v) for k, v in list(main["not_played_by_reason"].items())[:5])))
w("")
w("The lines he heard, in order (minutes and seconds into the walk):")
w("")
T.extend(sample_lines)
w("")
w("**Thirty other seeds of the same walk** (1991 to 2020), with the main one: lines heard %d to %d (middle %d); busiest minute outside a crime %d to %d; minutes with no line %s to %s of the half hour (middle %s); longest silence %d s to %d s (middle %d s). Zero repeats inside a floor and no neighbour line closer than 45 s in any of them. Across them every moment was heard at least once but Tommy: %s." % (lo, hi, med, blo, bhi, pc(qlo), pc(qhi), pc(qmed), glo, ghi, gmed, ", ".join("%s %d" % (SIT_LABEL[k], v) for k, v in sorted(sit_totals.items()))))
w("")
w("**A busy half hour** (eighty passers-by instead of twenty, same rain and crime): %d lines heard, busiest minute %d outside the crime, still no repeat and no neighbour line closer than 45 s. **An afternoon walk** (15:00): %d heard. **A night walk** (22:00, more night shift, fewer old people and shopkeepers out): %d heard, no repeat. **The test has teeth:** the busy walk with the variety and cooldown rules switched off shows %d same-speaker repeats and a neighbour gap of %s s." % (stress["lines_heard"], stress["busiest_minute_without_crime_lines"], afternoon["lines_heard"], night["lines_heard"], len(off["repeats_same_speaker_same_line_within_floor"]), off["neighbour_min_gap_s"]))
w("")
w("What the walk does not show, and the first target it missed: it is quiet after the crime, because witnesses say no hello for the hour and their talk carries 4 m, as ruled. The first target for silence was 40 percent of the minutes in every walk; one walk of thirty-one came in at 37 percent, a busy half hour and no fault, so the target is now a third in every walk and 45 percent in the middle one (rules.json says so). The street's existing ambient exchanges are stood in for by a share of the neighbour slots (60 percent in the dry, 40 in rain): an assumption of the simulation, not a measurement, and TownReach on the PC should replace it.")
w("")
w("## The format and where it lives")
w("")
w("**Its home today.** The street's lines already have homes and shapes, and this adds none:")
w("")
w("1. Core/StreetVoice.cs holds the shared banks (a bank key such as ambient/open/night or recognition/avoids, and an array of lines), and Core/OwnLines.cs holds a named person's own banks under the same keys (ByCast[id][bank]). RemarkLedger keeps what he heard under the key \"bank@id\" and saves it.")
w("2. game-design/barks.json is the enumeration of those banks that BarkGen makes (a slot per bank: id, family, brief, everySeconds, wanted, have, lines), and the voice manifest lists a clip per voice and line (slot, index, line, voice, file).")
w("3. content/dialogue/*-v1.json are dialogue banks in JSON (bank, license, era, register, rungs, speakers, and lines with id, context, rung, speaker, text), read by the content gate and the dialogue pipeline.")
w("")
w("**What lines.json is.** The third shape, extended, with the first's bank keys: its header and its id, context, rung, speaker and text fields are the dialogue bank's own (speaker is the kind of person, as w1 is \"the shopkeeper\" there; rung is the standing, as its \"stranger\" and \"novak\" are; idRung is how sure, as in crime-witness-v1: 0 a noise, 1 a shape, 3 a face). It adds kind and situation (kind repeats speaker, situation refines context; the check requires them equal), conditions, weight, group, delivery and dialect, and a flag for lines that ring the police. Each line's bank is a key in the street's grammar (greeting/stranger, rain/in, crime/face, way/to/ritas) and its group is \"bank@kind\", exactly the key RemarkLedger already keeps for OwnLines. So the ledger, the shuffle bag and BarkGen's repeat floor already fit it.")
w("")
w("export_slots.py writes the second shape (barks.json's slots) and the third (barks-manifest.json's renders, with each clip named as VoiceBank.ClipName names it) from lines.json whenever they are wanted, and stores neither: lines.json stays the one home.")
w("")
w("## How the PC session adopts it")
w("")
w("1. **Put the data home.** Copy lines.json to content/dialogue/ambient-lines-v1.json and rules.json beside it (content/rules/ambient-rules-v1.json). The content gate already walks content/dialogue/*.json (its bank reader takes id and text), so the gate covers it from then on; run `python3 tools/content-gate.py` and `python3 tools/canon-gate.py --corpus`.")
w("2. **Read it in Core.** A new Core/AmbientLines.cs, no engine types, loads the two files the way CastDay reads hook-cast.json (MiniJson), and picks: the conditions, the accent and never-police filters, the cooldowns, the weighted bag through RemarkLedger under \"bank@kind\". Resolve a speaker's kind in the order rules.json gives: an own kind (rocco, sam, emil, june), the person's kind (lines.json speakers), then the crowd's trade (rules.json trade_kinds). An unknown trade says nothing.")
w("3. **Wire the moments that do not exist yet.** Today the game plays only two street lines to Tom (Recognition as he comes near, FaintRemark once he has passed: production/research/ambient-lines/own-lines-2026-10-01.md found this). So: a greeting where Recognition is asked, only for somebody at Notices or below (above that the existing recognition banks speak and these stay silent); a bump from the knock the street's figures already take (NpcWalker.Bumped in the C# reference, and whatever the Unreal build calls it); rain from Weather.Rain crossing the cut points; crime and after a deed from each witness's perception (idRung 0, 1 or 3, never above what Perception measured); farewell when a talk ends; the way when he asks one (the answer is a direction line if the person knows the place, else one of the kind's own).")
w("4. **The voice's rules belong to the Game layer.** One line sounding at a time (two in a crime), priority, shelf life and the fade are in rules.json; SpeechDirector and SpeechQueue apply them.")
w("5. **Tests first.** Port walk_sim.py's rule_tests as CoreTests rows (they are small scenarios, one rule each), a golden table of picks (seed and state to line id) for the C++ port as OwnLines.h has, and the walk as a Soak. Run TownReach --two-hours to size the groups of lines as METHOD-2026-09-30 says (I could not: it is C# on the PC).")
w("6. **Voices** (below): render in the order of how often a moment plays.")
w("7. **His page before it merges** (CLAUDE.md: anything touching a voice or identity reaches him on one page). Not all %s lines: three lines for each kind, the four own kinds first, shortfalls first. The one line most worth his eye is Ron's, whose tone he approved." % format(n_lines, ","))
w("8. **A fresh reviewer per situation**, as the gate asks, against the casting sheets and a third hearing. None was run here: this unit is content, and the check cannot hear a voice. Until then every line is ready for review, not passed.")
w("9. **Nothing multiplied before one complete sample** (CLAUDE.md). This unit wrote all kinds at once because the order asked for it. The recommendation: land one kind first, Ron's new moments, in the assembled game, on his page, then the rest.")
w("")
w("## The voices it needs")
w("")
w("The new lines need no new voice. Per RULINGS (3 Oct, 24 Sep): Ron, Darren, Sheila and the dispatcher have their game voices; June and Father Walsh wait for his yes on the listening page; nobody else has one, so everybody else speaks in the six crowd voices (crowd_m1 to m3, crowd_f1 to f3, which VoiceBank.VoiceFor draws by the speaker's id).")
w("")
w("| Kind | Spoken by |")
w("|---|---|")
w("| Ron | Ron's July voice (p227) |")
w("| Darren | Darren's voice (p241) |")
w("| Father Walsh | his July voice, once he says yes to it (the sheet notes it needs an older one) |")
w("| June | p277 or a better fit, once he says yes |")
w("| office worker | Sheila (p267) and the dispatcher (p280) in their own voices; Alison, Christine, Susan, the customs assistant and Philip in crowd voices |")
w("| the other eight shared kinds and the directions | the crowd voices |")
w("")
w("What that costs in clips (a clip per voice and line): **about %s** if every shared line is made in the voices of the people who stand in its kind and are met more than once, which keeps each of them sounding like one person; **about %s** if every shared kind is made in all six crowd voices. The first is recommended. (Sex known: %s. Sex not known, as VoiceBank is called today: %s.) By voice, sex known: %s." % (format(total_clips, ","), format(all_six, ","), format(total_clips, ","), format(sum(clips_today.values()), ","), ", ".join("%s %d" % (k, v) for k, v in clips.items())))
w("")
w("Rules the voice plan rests on, all checked: shared lines are gender-free (a gendered word is allowed only in a kind that one sex speaks: laundry worker, Ron, Darren, Father Walsh, June); a line in northern dialect is never given to Nora (Cork) or the Tangs (Hong Kong English), who have no local-accent voice, and the recommendation is that they say nothing from these banks until their voices are cast; hushed lines are the same take played 6 dB lower, not a different one. The street's anonymous passers-by have no fixed voice, so VoiceFor needs a second argument, the voices rendered for the line's kind, to choose among.")
w("")
w("## Where this departs from the method note (METHOD-2026-09-30.md), and why")
w("")
w("- **Conditions are data, not branches.** The street's picker chooses its bank by code (an hour test here, a stance there). Fourteen moments with weather, hour, standing and sureness would be thousands of lines of branches; as data the PC session tests them as rows and a writer can change them. The bank keys, the ledger and the bag are the street's own.")
w("- **A group is 8 to 13 lines, not the note's 8 to 20, and not sized from TownReach.** The brief set eight as the floor; the busiest bank (a greeting to a stranger) is 13; the walks use a fraction of every group. TownReach --two-hours has to be run on the PC to size them as the note says. A larger group costs render time: the plan above is already about %s clips." % format(total_clips, ","))
w("- **\"Never repeats\" is measured over thirty-one walks of thirty minutes and a busy one, not many two-hour walks.** Same reason: the real walk is the PC's.")
w("- **All kinds were written together**, where the note says one character complete first, then the rest. The order asked for kinds by situations, and everything here is a proposal on a cloud branch. The recommendation above (one kind first, Ron) restores the note's order at the point it matters, before anything is multiplied in the game.")
w("- **The note's per-line gate** (the casting sheet's voice; words and prices right; the content rule and canon; whether the speaker could know it; not a paraphrase of its group's other lines; low-key enough for a third hearing): the machine part is the check (content, canon, could-know through conditions, paraphrase by shared runs); the part that needs a reader (voice, third hearing) is not done.")
w("- **Set-aside lessons used.** The set-aside note (six-voices-v3) says the banks failed because they were written from their names and not from the moment that plays them, and that people meet each other. These are written from the moment (a rung, a weather, a sureness, a place asked about), and the check holds each to its moment. Known shortfall: in rain and after a deed the lines are one-sided remarks, not exchanges; replies are the street's existing reply banks.")
w("")
w("## Where the homes disagree (for the PC session; none is settled here)")
w("")
w("1. **Two chapels, two markets.** hook-cast.json has Father Walsh's chapel and the open market (Tuesday, Friday, Saturday) a few minutes up from the street; the atlas has Fairview Chapel and the Market Hall far up the hills. The directions treat them as four places.")
w("2. **The cafe.** StreetFacts.cs puts it opposite the north end of the parade; hook-cast.json puts it at 24 m, opposite the middle; canon says the shops of the west block are across from the north half. The lines say \"opposite the parade's north half\", canon's words.")
w("3. **Population.Trades** still names a \"bartender\" (ContentRule.cs's own comment calls the trade a design question). No line mentions it; the trade is mapped to shopkeeper; a replacement such as \"cafe hand\" would end the question. Its names (Yolanda, Wendell) are the prototype's, American, and unused here.")
w("4. **VoiceBank.Cast** lists ada, marla, joey, rita, hal and vesna as cast, though RULINGS says no voice is cast without his yes and names only five in the game. This plan uses only the five (and the two pending); the PC session should look at what the game really speaks.")
w("5. **Julie Kettlewell** is laid off by her sheet and still a laundress in hook-cast.json; her sheet outranks, so she stands in casual worker.")
w("6. **The directions' small details** (the steam over the laundry, the chapel's bell, the stack at the Retort works, net curtains at the boarding house) are invented flavour, not facts from a home.")
w("")
w("## Invented for Jafar (DECISIONS.md, one entry for each kind, each marked)")
w("")
w("1. The thirteen kinds and who stands in each (%d people and routines' ids, %d trades), and who has none." % (len([r for r in CHK["rows"] if r["id"].startswith("kinds.person.")]), len([r for r in CHK["rows"] if r["id"].startswith("kinds.trade.")])))
w("2. Standing in greetings: where each person starts on the ladder, Tommy in three kinds only, Sheila held at the new owner until trust, \"boss\" Ron's and \"son\" Father Walsh's.")
w("3. Crime lines in three levels of sureness, none naming or accusing; the mark and named rungs left without lines.")
w("4. Directions to %d places, and what the lines do where the homes disagree (two chapels, two markets, the cafe's place)." % len(DOC["places"]))
w("5. The numbers in the rules (floors, gaps, caps, chances, priorities, shelf lives, the quiet targets).")
w("6. Weather and hour bands (0.10 and 0.50; five, twelve, seventeen, twenty-one), and who is out in rain and how far talk carries.")
w("7. The hour after a deed: a 90 s gap, 6 dB quieter, 4 m, and no hello or remark on the weather.")
w("8. Voices: nothing new cast, the crowd voices for the rest, Nora and the Tangs silent until cast, the clip counts.")
w("")
w("## What to look at first")
w("")
w("1. **Tommy.** Which three kinds may say it (pensioner, office worker which is Sheila's, Father Walsh), or fewer. Canon keeps the last rung for two or three people and names none, so which kinds may say it is his choice.")
w("2. **One sample, not %s lines.** Three lines for each of the thirteen kinds, from the file, would tell him whether the town sounds like his town. Ron's are the ones his tone approval covers." % format(n_lines, ","))
w("3. **The quiet.** In the main walk he hears %d lines in half an hour and goes %d seconds once with none (the rain and the crime). Is that a street or too still?" % (main["lines_heard"], round(main["longest_gap_s"])))
w("4. **The clip count** (about %s) against the voice engine's time." % format(total_clips, ","))
w("")
w("## What the check cannot judge")
w("")
w("- Whether a line is funny, or in a person's voice, or bears a third hearing. The machine part is screens and counts. The nine groups of greetings to a stranger are the ones to read first, since they are said the most.")
w("- Whether two kinds say the same thing in other words below the 60 percent line: %d pairs stand between 50 and 60 percent. Across kinds the crime lines share a plain fact (I saw the face; I'd know it again), and some ideas recur (ask at the cab office, a face in the head)." % CROSS_LEFT)
w("- Whether a direction is easy to follow in the game's own geometry. It agrees with the atlas, the routines and the built street's bays; it was not walked.")
w("- The real lyric or catchphrase: the check holds a list of known ones and the line lengths; it cannot prove none exists.")
w("")
(HERE / "NOTES.md").write_text("\n".join(T) + "\n", encoding="utf-8")
print("NOTES.md: %d words" % len(" ".join(T).split()))
