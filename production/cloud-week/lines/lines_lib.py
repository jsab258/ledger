#!/usr/bin/env python3
"""Shared vocabulary for build_lines.py and check_lines.py (unit 12, cloud week 42). Standard library only.

What lives here, in plain words: the kinds of person and who stands in each, the situations, the
standing rungs and the words that read them out, the places a person can be asked the way to (with
where they are, taken from the atlas and the street's own places), the weather and time bands, and the
small shorthand the authored files use after a line ("Morning. @m" means: only in the morning).

Nothing here renders, trains or calls a model.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

# --------------------------------------------------------------------------- conditions

TIME_BANDS = {
    "morning": [5, 12],
    "afternoon": [12, 17],
    "evening": [17, 21],
    "night": [21, 5],
}
# The game's own cut: StreetVoice.Ambient reads night as hour >= 21 or < 5 ("ambient/open/night") and calls the
# rest "ordinary", which its comment says "runs from five till nine at night". Morning and afternoon are the
# split of that ordinary band at noon, so that "Morning." is never said at two o'clock.

WEATHER_BANDS = {
    "dry": "Weather.Rain below 0.10 (dry overcast; the street may still be wet)",
    "drizzle": "Weather.Rain from 0.10 up to 0.50",
    "rain": "Weather.Rain 0.50 and over",
}
# The three states are RULINGS 5 October ("a grey range (dry overcast, drizzle, rain)"); the two cut points are
# invented here, from Weather.cs's own sample days (a day of 0.35 is called Day 1 'rains outright' there; 0.90 is
# the downpour), and marked for Jafar in DECISIONS.md.

TIMES = list(TIME_BANDS)
WEATHERS = list(WEATHER_BANDS)

# --------------------------------------------------------------------------- standing

RUNGS = ["stranger", "owner", "nowak", "tom", "tommy"]
KNOWN = ["owner", "nowak", "tom", "tommy"]
# canon.md: "What the town calls you reads out your standing: the new owner, then Nowak, then Tom, then Tommy."
# 'stranger' is the one below the ladder: somebody who does not know who he is.
RUNG_WORDS = {
    "stranger": [],
    "owner": ["new owner"],
    "nowak": ["Nowak"],
    "tom": ["Tom"],
    "tommy": ["Tommy"],
}
# The only address words a line may use besides the rung's own. Ron's "boss" is his (what-they-call-him: "Ron's
# 'boss' stays his"); "son" is Father Walsh's (OwnLines.cs, his approved lines).
GENERIC_ADDRESS = ["mate", "love", "pal", "friend", "dear"]
KIND_ADDRESS = {"ron": ["boss"], "father_walsh": ["son"], "pensioner": ["young man"]}

# --------------------------------------------------------------------------- how sure (crime)

SURE = {"noise": 0, "shape": 1, "face": 3}
# The identification ladder of content/dialogue/crime-witness-v1.json and production/specs/dialogue-crime-witness-v1.md:
# idRung 1 a shape, 2 a distinguishing mark, 3 a face she would know again, 4 the person named. A noise is below the
# ladder (heard, not seen): idRung 0, new here. Rung 2 is left without lines on purpose: a mark (a coat, a walk) is
# content the simulation has to supply, so a line for it would have to be composed at run time, and composed lines
# cannot be recorded (StreetVoice.cs, SpokenLine.Composed). Rung 4 (named) is the dialogue bank's own business.

# --------------------------------------------------------------------------- situations

SITUATIONS = {
    "greeting.stranger": {"context": "greeting", "bank": "greeting/stranger", "short": "greet-stranger", "rung": "stranger", "family": "greet"},
    "greeting.owner":    {"context": "greeting", "bank": "greeting/owner",    "short": "greet-owner",    "rung": "owner",    "family": "greet"},
    "greeting.nowak":    {"context": "greeting", "bank": "greeting/nowak",    "short": "greet-nowak",    "rung": "nowak",    "family": "greet"},
    "greeting.tom":      {"context": "greeting", "bank": "greeting/tom",      "short": "greet-tom",      "rung": "tom",      "family": "greet"},
    "greeting.tommy":    {"context": "greeting", "bank": "greeting/tommy",    "short": "greet-tommy",    "rung": "tommy",    "family": "greet"},
    "bumped":            {"context": "bump",     "bank": "bumped",            "short": "bumped",         "rung": "any",      "family": "bump"},
    "rain_starts":       {"context": "rain",     "bank": "rain/starts",       "short": "rain-starts",    "rung": "any",      "family": "rain_starts"},
    "in_rain":           {"context": "rain",     "bank": "rain/in",           "short": "in-rain",        "rung": "any",      "family": "in_rain"},
    "crime_noise":       {"context": "crime",    "bank": "crime/noise",       "short": "crime-noise",    "rung": "any",      "family": "crime"},
    "crime_shape":       {"context": "crime",    "bank": "crime/shape",       "short": "crime-shape",    "rung": "any",      "family": "crime"},
    "crime_face":        {"context": "crime",    "bank": "crime/face",        "short": "crime-face",     "rung": "any",      "family": "crime"},
    "after_deed":        {"context": "deed",     "bank": "deed/after",        "short": "after-deed",     "rung": "any",      "family": "after_deed"},
    "asked_way":         {"context": "way",      "bank": "way/ask",           "short": "way",            "rung": "any",      "family": "way"},
    "farewell":          {"context": "farewell", "bank": "farewell",          "short": "farewell",       "rung": "any",      "family": "farewell"},
}
FAMILIES = ["greet", "bump", "rain_starts", "in_rain", "crime", "after_deed", "way", "farewell"]

# --------------------------------------------------------------------------- kinds of person

# members: ids from production/cloud-week/town/people.json and production/specs/hook-cast.json
# trades: entries of Population.Trades (ledger/Assets/Scripts/Core/Population.cs), the sim's own names for the
#         crowd's jobs; every one maps to exactly one kind.
# rungs: which greeting rungs exist for the kind.
# voice: 'any' (lines are gender-free), or 'f' / 'm' (the kind is spoken only by that voice, so a gendered word is allowed).
KINDS = {
    "shopkeeper": {
        "desc": "somebody behind a counter or in a doorway: the fish shop, the pawn, the coin shop, the caff, the takeaway, the boarding house",
        "members": ["marla", "rita", "victor", "hal", "cafe", "takeaway_m", "takeaway_f", "sanja", "ines", "marta"],
        "trades": ["baker", "barber", "hairdresser", "cook", "line cook", "waitress", "cashier", "usher", "bartender"],
        "rungs": ["stranger", "owner", "nowak", "tom"], "voice": "any", "own": False,
    },
    "dock_worker": {
        "desc": "dockside and quayside hands: the crane, the yard, the fish dock, the scrap, the ferry",
        "members": ["stipe", "drago", "dario", "petra"],
        "trades": ["dock hand", "stevedore", "ferry hand", "forklift driver", "scrap hauler"],
        "rungs": ["stranger", "owner", "nowak", "tom"], "voice": "any", "own": False,
    },
    "pensioner": {
        "desc": "the old of the street: retired, on the pension, the chapel's women, the net-mender",
        "members": ["ada", "hana", "fabjan", "magda", "vesna"],
        "trades": [],
        "rungs": ["stranger", "owner", "nowak", "tom", "tommy"], "voice": "any", "own": False,
    },
    "office_worker": {
        "desc": "desks and counters of paper: the books, the radio and phone, the harbour office, customs, the paper",
        "members": ["lena", "noor", "zlata", "bruno", "tibor", "elias", "goran"],
        "trades": ["clerk", "bookkeeper", "secretary"],
        "rungs": ["stranger", "owner", "nowak", "tom", "tommy"], "voice": "any", "own": False,
    },
    "driver": {
        "desc": "wheels for hire or for the firm: the cab on Mickey's rank, the bus, the lorry",
        "members": ["ferko", "dusan"],
        "trades": ["bus driver", "cab driver", "trucker"],
        "rungs": ["stranger", "owner", "nowak", "tom"], "voice": "any", "own": False,
    },
    "laundry_worker": {
        "desc": "the steam laundry's floor and the seamstress's bench: presses, folding, pins and thread",
        "members": ["zora", "katarina", "iva", "selma"],
        "trades": [],
        "rungs": ["stranger", "owner", "nowak", "tom"], "voice": "f", "own": False,
    },
    "tradesman": {
        "desc": "somebody who mends, makes or paints for a living: locks, engines, signs, wiring, welding, print",
        "members": ["luka", "franjo", "jelena", "tomas"],
        "trades": ["mechanic", "welder", "printer", "roofer", "electrician", "machinist", "sign painter"],
        "rungs": ["stranger", "owner", "nowak", "tom"], "voice": "any", "own": False,
    },
    "night_shift": {
        "desc": "those who work while the street sleeps: the watchman, the janitor, the guard, the nurse coming off a shift",
        "members": ["filip"],
        "trades": ["night janitor", "security guard", "nurse"],
        "rungs": ["stranger", "owner", "nowak", "tom"], "voice": "any", "own": False,
    },
    "casual_worker": {
        "desc": "no steady work in 1990: casual days on the quay, laid off, looking for anything, running for the rent collector",
        "members": ["joey", "tanja", "danica"],
        "trades": [],
        "rungs": ["stranger", "owner", "nowak", "tom"], "voice": "any", "own": False,
    },
    "ron": {
        "desc": "Ron Kirby's own lines: the door and the rank, 58, low and worn, 'boss' and 'friend'",
        "members": ["rocco"], "trades": [],
        "rungs": ["nowak", "tom"], "voice": "m", "own": True,
    },
    "darren": {
        "desc": "Darren Milner's own lines: 25, the street hustler, quick, useful, always talking",
        "members": ["sam"], "trades": [],
        "rungs": ["nowak", "tom"], "voice": "m", "own": True,
    },
    "father_walsh": {
        "desc": "Father Walsh's own lines: about 61, the Irish-born parish priest, soft and slow, 'the guards'",
        "members": ["emil"], "trades": [],
        "rungs": ["owner", "nowak", "tom", "tommy"], "voice": "m", "own": True,
    },
    "june": {
        "desc": "June Suddaby's own lines: 38, Mickey's daughter, back for the funeral and leaving soon, clipped and on guard",
        "members": ["june"], "trades": [],
        "rungs": ["owner", "nowak", "tom"], "voice": "f", "own": True,
    },
}
# The shared directions (a place's facts are the place's, not a kind's) are said by any resident who knows the place.
ANYONE = "anyone"
KIND_ORDER = list(KINDS)

# people in people.json or hook-cast.json who have no kind, and why
NO_KIND = {
    "tom": "the player: his words are typed",
    "ellis": "DS Ellis speaks in authored scenes and live talk (game-design/ellis-2026-09-29.md), not from street banks",
    "aldous": "a head of a rival organisation: authored and live talk only, never a passer-by's greeting",
    "sera": "a head of a rival organisation: authored and live talk only",
    "danny": "a head of a rival organisation: authored and live talk only",
    "fixer": "the Fixer brokers between the three: authored and live talk only",
    "outfit_man": "the outfit's man is never named and never speaks to a stranger (canon; town list 6z)",
}

# What each person says when they are not their kind's only voice: (accent slot from REGULARS.md's contact sheet)
# a person whose voice is not the local one may not be given a line written in the local dialect.
NOT_LOCAL_VOICE = {
    "vesna": "Irish (Cork): REGULARS.md row 11",
    "takeaway_m": "Hong Kong English with twenty years of Hull in it: REGULARS.md row 29",
    "takeaway_f": "Hong Kong English: REGULARS.md row 30",
}
# Words that make a line local dialect. A line carrying one is marked dialect "local" and is not given to
# anybody in NOT_LOCAL_VOICE.
DIALECT_MARKERS = ["nowt", "owt", "summat", "aye", "nithered", "mither", "mardy", "nesh", "ey up", "eh up", "now then",
                   "ginnel", "gansey", "mucky", "daft", "tha", "reet", "chuffed", "scran"]

# gendered words: only allowed in a kind whose voice is single-gender
GENDER_WORDS = ["husband", "wife", "missus", "wifey", "mam", "mum", "mummy", "dad", "widow", "widower", "gentleman", "lady", "madam", "ladies"]

# --------------------------------------------------------------------------- people and trades to kinds

PERSON_KIND = {}
for _k, _v in KINDS.items():
    for _m in _v["members"]:
        PERSON_KIND[_m] = _k

# --------------------------------------------------------------------------- places and how to get there

# Street frame: x along the street in metres from the quay end (the Hook's atlas north), z across, east positive
# (production/specs/vignette-scene.json frame; hook-cast.json places). Atlas places are converted with the atlas's own
# street_anchor: x = north - 350, z = east - 400.
# cls: 'street' (on Quay Street), 'down' (x below the quay end: towards the water), 'up' (x above the street's top).
# far: more than 200 m from the street's middle: a walk, not a step.
def _d(pid, names, x, z, src, side=None, kind="street"):
    return {"id": pid, "names": names, "x": x, "z": z, "src": src, "side": side, "kind": kind}

DESTS = [
    # ---- on Quay Street (hook-cast.json places; RULINGS 3 Oct trades; vignette-scene.json)
    _d("quay", ["the quay"], -5.0, 0.0, "hook-cast.json places.quay", None),
    _d("mickeys", ["Mickey's", "the cab office", "the rank"], 6.0, 7.5, "hook-cast.json places.mickeys_office; vignette-scene.json bay 0 (x 3 to 9)", "east"),
    _d("fish_shop", ["the fish shop", "the fishmonger's"], 12.0, 7.5, "hook-cast.json places.fish_counter; RULINGS trades: bay 1 fishmonger", "east"),
    _d("ritas", ["Rita's", "the pawn", "the pawnbroker's"], 18.0, 7.5, "hook-cast.json places.ritas_counter", "east"),
    _d("phone_box", ["the phone box", "the kiosk"], 16.5, 4.3, "vignette-scene.json furniture E3 (x 16.5, east); hook-cast.json places.kiosk", "east"),
    _d("laundry", ["the laundry", "the steam laundry"], 30.0, 7.5, "hook-cast.json places.laundry_counter; RULINGS trades: bay 4", "east"),
    _d("grocer", ["the grocer's"], 36.0, 7.5, "RULINGS trades: bay 5 grocer (x 33 to 39)", "east"),
    _d("chandler", ["the chandler's", "the ship's chandler"], 43.0, 7.5, "vignette-scene.json east_chandler (x 40 to 46)", "east"),
    _d("cafe", ["the caff", "the cafe"], 24.0, -7.5, "hook-cast.json places.cafe (west block, across from the parade's north half)", "west"),
    _d("newsagent", ["the newsagent's", "the paper shop"], 32.0, -7.5, "hook-cast.json places.pension_counter", "west"),
    _d("hals", ["Hal's"], 39.0, -7.5, "hook-cast.json places.hals_shop", "west"),
    _d("bus_stop", ["the bus stop"], 46.0, -4.3, "hook-cast.json places.bus_stop (the street's north end)", "west"),
    # ---- the town the street's people go to (hook-cast.json places, same frame)
    _d("docks", ["the dock gate", "the docks"], -60.0, 0.0, "hook-cast.json places.docks", None, "town"),
    _d("fish_dock", ["the fish dock"], -60.0, 40.0, "hook-cast.json places.fish_dock", None, "town"),
    _d("boatyard", ["the boatyard", "the repair yard"], -60.0, -40.0, "hook-cast.json places.repair_yard", None, "town"),
    _d("harbour_office", ["the harbour office", "the harbourmaster's"], -100.0, 0.0, "hook-cast.json places.harbour_office", None, "town"),
    _d("customs_shed", ["the customs shed"], -100.0, 40.0, "hook-cast.json places.customs_shed", None, "town"),
    _d("ferry", ["the ferry landing", "the ferry"], -100.0, -40.0, "hook-cast.json places.ferry_stop", None, "town"),
    _d("warehouse_row", ["the warehouse row", "the old warehouses"], -140.0, 0.0, "hook-cast.json places.warehouse_row", None, "town"),
    _d("walsh_chapel", ["Father Walsh's chapel", "the chapel"], 100.0, 0.0, "hook-cast.json places.chapel", None, "town"),
    _d("open_market", ["the open market", "the market"], 100.0, -40.0, "hook-cast.json places.market (Tue, Fri, Sat)", None, "town"),
    _d("boarding_house", ["the boarding house"], 140.0, 0.0, "hook-cast.json places.boarding_house", None, "town"),
    _d("flats", ["the flats", "the council flats"], 140.0, 40.0, "hook-cast.json places.flats", None, "town"),
    _d("allotments", ["the allotments"], 140.0, -40.0, "hook-cast.json places.allotments", None, "town"),
    # ---- the atlas's own landmarks (production/art/atlas-01/data/atlas.json), converted: x = north - 350, z = east - 400
    _d("old_basin", ["the Old Basin"], -105.0, -30.0, "atlas.json landmarks H2 [370, 245]", None, "atlas"),
    _d("harbour_board", ["the Harbour Board"], -30.0, 110.0, "atlas.json landmarks H3 [510, 320]", None, "atlas"),
    _d("market_hall", ["the Market Hall"], 300.0, 50.0, "atlas.json landmarks C1 [450, 650]", None, "atlas"),
    _d("tivoli", ["the Tivoli"], 215.0, 373.0, "atlas.json landmarks P1 [773, 565]", None, "atlas"),
    _d("fairview_chapel", ["Fairview Chapel"], 485.0, -70.0, "atlas.json landmarks F1 [330, 835]", None, "atlas"),
    _d("records_court", ["the Records Court cafe"], 510.0, 400.0, "atlas.json landmarks E1 [800, 860]", None, "atlas"),
    _d("police_station", ["the police station"], 565.0, 470.0, "atlas.json landmarks E2 [870, 915]", None, "atlas"),
    _d("canteen", ["the clocking-in canteen", "the canteen"], 225.0, -150.0, "atlas.json landmarks I1 [250, 575]", None, "atlas"),
    _d("retort_works", ["the Retort works"], 30.0, -275.0, "atlas.json landmarks I2 [125, 380]", None, "atlas"),
    _d("winter_rooms", ["the Winter Rooms"], 100.0, 510.0, "atlas.json landmarks G1 [910, 450]", None, "atlas"),
    _d("short_pier", ["the Short pier"], 100.0, 660.0, "atlas.json landmarks G2 [1060, 450]", None, "atlas"),
]
DEST = {d["id"]: d for d in DESTS}
STREET_TOP = 46.0
STREET_MIDDLE = 24.0


def dest_class(d):
    """'street', 'down' (below the quay end), 'up' (past the top of the street)."""
    if d["kind"] == "street":
        return "street"
    return "down" if d["x"] < 0 else "up"


def dest_far(d):
    return ((d["x"] - STREET_MIDDLE) ** 2 + d["z"] ** 2) ** 0.5 > 200.0


# --------------------------------------------------------------------------- the shorthand after a line

TAGS = {
    "m": ("time", "morning"), "a": ("time", "afternoon"), "e": ("time", "evening"), "n": ("time", "night"),
    "wet": ("weather", ["drizzle", "rain"]), "dz": ("weather", ["drizzle"]), "rn": ("weather", ["rain"]), "dry": ("weather", ["dry"]),
    "st": ("standing", ["stranger"]), "kn": ("standing", list(KNOWN)),
    "w1": ("weight", 1), "w3": ("weight", 3),
    "h": ("delivery", "hushed"), "r": ("delivery", "raised"),
}


def parse_line(raw):
    """'Morning. @m,w1' -> ('Morning.', {'time': ['morning'], 'weight': 1})."""
    text, _, tagpart = raw.partition(" @")
    cond = {}
    for t in [x.strip() for x in tagpart.split(",") if x.strip()]:
        if t not in TAGS:
            raise ValueError("unknown tag %r in %r" % (t, raw))
        key, val = TAGS[t]
        if key == "time":
            cond.setdefault("time", []).append(val)
        elif key in ("weather", "standing"):
            cond[key] = list(val)
        else:
            cond[key] = val
    return text.strip(), cond


def words_in(text):
    return len(text.split())


def norm_text(text):
    return re.sub(r"[^a-z0-9 ]+", "", text.lower().replace("’", "'").replace("'", "")).strip()
