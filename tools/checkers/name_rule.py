#!/usr/bin/env python3
"""The hard rule on names, measured: no first sentence that names a person, place or event missing from the speaker's
facts may pass (his order of 27 October 2026, evening, 3).

    python tools/checkers/name_rule.py tune [--wider]          # the rule on the tuning sentences (TRAIN3, VAL3): design
    python tools/checkers/name_rule.py test OUT.json [--wider] # once, on the 617 held, with Haiku's verdicts and harm sort
    python tools/checkers/name_rule.py --selftest

THE RULE (the reference for ClaimCheck.NamesMissing, which the game runs). A name is a run of capitalised words, a
possessive taken off ("Mickey's" is Mickey), titles set aside (Father, Mr, Mrs, Old ...). A sentence's first word starts
a name only when the next word is capitalised too ("Frank Doyle", "Father Walsh"): alone it is the capital every sentence
opens with, so a lone invented name opening a sentence ("Frank was in") is not caught. Days, months and holidays are
times, numbers are numbers, nationalities and oaths are not people, "I" is the speaker: none is a name here. A name is
in the facts when any of its words, other than a title or a common word ("The Crown" is judged on Crown), is a word of
the facts (any case). One name missing refuses the sentence, whatever the checker or Haiku said.

DESIGNED ON THE TUNING HALF ONLY (the 2,151 near-miss sentences of the third try, Gemini's labels); the 617 held
sentences are read once, by `test`.
"""
import ast
import json
import re
import sys

TITLES = {"father", "mr", "mrs", "miss", "ms", "dr", "doctor", "saint", "st", "old", "young", "uncle", "aunt", "auntie",
          "sister", "brother", "mother", "nurse", "officer", "constable", "pc", "ds", "sergeant", "inspector", "detective"}
TIMES = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "january", "february", "march",
         "april", "may", "june_month", "july", "august", "september", "october", "november", "december", "christmas",
         "easter", "whitsun", "boxing", "new", "year", "eve", "bank", "holiday"}
NATIONS = {"english", "british", "irish", "scottish", "scots", "welsh", "geordie", "geordies", "northern", "southern",
           "yorkshire", "lancashire"}
STARTERS = set("""a about after again ah all also always an and any anyone anything are as ask at aye away back be because
been before being best better between bit both but by can can't come could couldn't course did didn't do does doesn't
done don't down each either else enough even ever every everyone everything exactly fair far few fine first for from get
give go goes going gone good got had has hasn't have haven't he he'd he'll he's her here here's hers him his honest how
however i if in is isn't it it'll it's its just keep kind know last least leave less let let's like listen little look
lot love mate maybe me mind mine more most much must my myself near need never next no nobody none nor not nothing now
of off oh ok okay on once one only or other our ours out over pal perhaps plenty pretty quite rather really right round
same say see seems she she'd she'll she's should since so some somebody someone something sometimes sorry still such
sure take tell than thank thanks that that'll that's the their them then there there's these they they'd they'll they're
they've thing things think this those though three through till to today told tomorrow tonight too two under until up
upstairs downstairs us very wait want was wasn't way we we'd we'll we're we've well were weren't what what's whatever
when where where's whether which while who who's whoever whole why will with without won't would wouldn't yeah yes yet
you you'd you'll you're you've your yours four five six seven eight nine ten twenty half quarter word nah son love lad
lass pet hen chief boss sir madam funny strange odd straight head truth work depends aside apart morning afternoon
evening night cheers ta blimey honestly frankly hardly mostly usually second third find turn walk follow try try""".split())
# oaths and exclamations: not a person, place or event (tuning half, 27 October: "God knows trade has been thin")
OATHS = {"god", "christ", "lord", "heaven", "heavens", "jesus", "hell"}

WORD = re.compile(r"[A-Za-z][A-Za-z'\u2019\-]*")


def norm(w):
    w = w.replace("\u2019", "'")
    for s in ("'s", "s'", "'"):
        if w.lower().endswith(s) and len(w) > len(s) + 1:
            return w[: -len(s)]
    return w


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]


NUMBERS = re.compile(r"^(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|"
                     r"seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand)"
                     r"(-[a-z]+)?$")


def capitalised(w):
    low = w.lower()
    return (w[:1].isupper() and w != "I" and not low.startswith("i'") and low not in NATIONS and low not in OATHS
            and low.rstrip("s") not in TIMES and low not in TIMES and not NUMBERS.match(low))


def names(sentence):
    """Runs of capitalised words, as (words) tuples, titles kept inside the run. A sentence's first word starts a
    run only when the word after it is capitalised too ("Frank Doyle ...", "Father Walsh ..."): alone it is just the
    capital every sentence opens with (tuning half: "Head down Quay Street", "Proper old sort", "Aren't you")."""
    out = []
    for sent in sentences(sentence):
        toks = [norm(t) for t in WORD.findall(sent)]
        run = []
        for i, w in enumerate(toks):
            is_name = capitalised(w)
            if is_name and i == 0 and not (len(toks) > 1 and capitalised(toks[1])):
                is_name = False
            if is_name:
                run.append(w)
            else:
                if run:
                    out.append(tuple(run))
                run = []
        if run:
            out.append(tuple(run))
    return out


FACT_ID = re.compile(r"^\s*[A-Z]{1,2}\d+\*?:\s*")


def bare(facts):
    """The facts' own words, their IDs ("C1: ", "P22: ") taken off, as the game hands the rule its items' text
    (the fresh review of 27 October night: with the IDs read as numbers, 1 to 22 always counted as stated)."""
    return [FACT_ID.sub("", f) for f in facts]


def fact_words(facts):
    return {norm(w).lower() for w in WORD.findall(" ".join(bare(facts)))}


def missing(sentence, facts):
    words = fact_words(facts)
    miss = []
    for run in names(sentence):
        # a title or a common word ("The Crown") never makes a name present by itself
        core = [w for w in run if w.lower() not in TITLES and w.lower() not in STARTERS]
        if not core:
            continue
        if not any(w.lower() in words for w in core):
            miss.append(" ".join(run))
    return miss


# THE WIDER VERSION, beyond his rule and measured apart (27 October): every number the sentence states (a clock time, a
# count, a year) is a number the facts state; and a place or a role named by a plain noun from the list below is a
# word of the facts. Designed on the tuning half; the harm sort found most harmful leaks were times and described
# people and places ("half past seven", "since nineteen sixty-three", "the harbourmaster", "the pier head").
UNITS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
         "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
         "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
PLACE_NOUNS = {"pier", "chemist", "chemists", "pub", "inn", "church", "school", "station", "harbour", "hospital", "library",
               "post", "bank", "garage", "mill", "factory", "warehouse", "club", "hotel", "cinema", "park", "shop", "shops",
               "bakery", "butcher", "butchers", "awning", "allotments", "flats", "estate", "beach", "promenade", "lighthouse",
               "bus", "ferry", "landing", "market", "cafe", "laundry", "launderette", "chapel", "yard", "docks", "quay"}
# kin are relations the facts often imply ("your cousin June", tuning half), and "coppers" is an idiom: not listed
ROLE_NOUNS = {"harbourmaster", "landlord", "landlady", "vicar", "priest", "doctor", "police", "constable",
              "dispatcher", "foreman", "manager", "cleaner", "barman", "postman", "milkman", "councillor", "solicitor"}


def numbers(text):
    """The numbers a text states, as ints: digits, number words (compounds and years read as their parts too)."""
    out = set()
    low = text.lower().replace("’", "'")
    for d in re.findall(r"\d+", low):
        n = int(d)
        out.add(n)
        if n >= 1900:
            out.add(n % 100)
    words = re.findall(r"[a-z]+", low)
    for i, w in enumerate(words):
        if w in TENS:
            v = TENS[w] + (UNITS[words[i + 1]] if i + 1 < len(words) and words[i + 1] in UNITS and UNITS[words[i + 1]] < 10 else 0)
            out.add(v)
        elif w in UNITS and not (i > 0 and words[i - 1] in TENS):
            out.add(UNITS[w])
    return out


def missing_wider(sentence, facts):
    miss = missing(sentence, facts)
    fact_nums = numbers(" ".join(bare(facts)))
    sent_low = sentence.lower()
    # "one" as a pronoun ("one of them", "the one") is no number
    nums = numbers(re.sub(r"(the|that|this|any|no|every|which) one|one of|one another|one day", " ", sent_low))
    for n in sorted(nums - fact_nums):
        miss.append("#%d" % n)
    words = fact_words(facts)
    for w in re.findall(r"[a-z]+", sent_low.replace("'s", "")):
        if (w in PLACE_NOUNS or w in ROLE_NOUNS) and w not in words and w.rstrip("s") not in words:
            miss.append(w)
    return miss


def ctx(r):
    c = r["context"]
    return ast.literal_eval(c) if isinstance(c, str) else c


def tune(rule=None):
    rule = rule or missing
    rows = json.load(open("F:/LedgerTools/checkers/train3/TRAIN3.json")) + json.load(open("F:/LedgerTools/checkers/train3/VAL3.json"))
    tr = [r for r in rows if str(r["supported"]) == "True"]
    inv = [r for r in rows if str(r["supported"]) == "False"]
    t_hit = [(r, rule(r["answer"], ctx(r))) for r in tr]
    i_hit = [(r, rule(r["answer"], ctx(r))) for r in inv]
    print("tune: true refused by the rule %d of %d; invented refused %d of %d" % (
        sum(1 for _, m in t_hit if m), len(tr), sum(1 for _, m in i_hit if m), len(inv)))
    for r, m in t_hit:
        if m:
            print("  TRUE refused:", m, "|", r["answer"][:110])


def test(out, rule=None):
    rule = rule or missing
    rows = json.load(open("F:/LedgerTools/checkers/train3/TEST3.json"))
    h = {}
    for line in open("F:/LedgerTools/checkers/train3/haiku-verdicts.jsonl", encoding="utf-8"):
        if line.strip():
            r = json.loads(line)
            h[r["sentence"]] = r["passed"]
    harm = {k["sentence"]: k["verdict"] for k in json.load(open("F:/LedgerTools/checkers/try4/harm37-verdicts.json", encoding="utf-8"))}
    res = {"true": 0, "invented": 0, "trueRefusedByHaiku": 0, "trueRefusedByRuleToo": 0, "trueNewlyRefusedByRule": [],
           "inventedThroughHaiku": 0, "inventedStoppedByRule": [], "inventedThroughBoth": 0}
    for r in rows:
        m = rule(r["answer"], ctx(r))
        passed = h[r["answer"]]
        if str(r["supported"]) == "True":
            res["true"] += 1
            res["trueRefusedByHaiku"] += not passed
            if m and passed:
                res["trueNewlyRefusedByRule"].append({"sentence": r["answer"], "names": m})
        else:
            res["invented"] += 1
            if passed:
                res["inventedThroughHaiku"] += 1
                if m:
                    res["inventedStoppedByRule"].append({"sentence": r["answer"], "names": m, "harm": harm.get(r["answer"])})
                else:
                    res["inventedThroughBoth"] += 1
    json.dump(res, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("test: invented through Haiku %d, stopped by the rule %d, through both %d; true refused by Haiku %d of %d, newly by the rule %d" % (
        res["inventedThroughHaiku"], len(res["inventedStoppedByRule"]), res["inventedThroughBoth"], res["trueRefusedByHaiku"], res["true"],
        len(res["trueNewlyRefusedByRule"])))


def selftest():
    facts = ["C1: Ron Kirby keeps Mickey's door and the rank.", "P17: Hal keeps the coin shop on Quay Street."]
    ok = 0
    ok += missing("Hal runs it from the coin shop.", facts) == []
    ok += missing("Frank Doyle runs it now.", facts) == ["Frank Doyle"]
    ok += missing("I heard it from Father Walsh.", facts) == ["Father Walsh"]
    ok += missing("Mickey's door shuts on a Sunday in November.", facts) == []
    ok += missing("He came up from Leeds.", facts) == ["Leeds"]
    ok += missing("Mr Kirby keeps it.", facts) == []
    ok += missing("The Crown shuts at ten on Mondays.", facts) == ["The Crown"]
    ok += missing("Head down Quay Street, mate.", facts + ["H1: the rank is on Quay Street"]) == []
    ok += missing("Frank was in earlier.", facts) == []          # the known gap: a lone name opening a sentence
    print("name_rule selftest: passed=%d/9" % ok)
    return 0 if ok == 9 else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--selftest":
        sys.exit(selftest())
    if a and a[0] == "tune":
        tune(missing_wider if "--wider" in a else None)
    elif a and a[0] == "test":
        test(a[1], missing_wider if "--wider" in a else None)
