#!/usr/bin/env python3
"""check_lines.py: the checks on lines.json and rules.json (unit 12, cloud week 42). Standard library only, light.

    python3 production/cloud-week/lines/check_lines.py

Writes checks/check_v1.json and checks/walk_v1.json, and prints "N of M rows pass". Exit 0 when every row passes, else 1.

Written apart from build_lines.py: it re-reads every home (people.json, hook-cast.json, the atlas, Population.cs, RealWorld.cs,
StreetFacts.cs, StreetVoice.cs, the content and canon gates) and does not trust what the builder said about them.

What each row says, in plain words:
  line.<id>    one row for every line: under twelve words; fields and ids right; every condition valid for its situation; no
               alcohol, gambling, child, slur, real brand, place, person, team or programme, nothing after 1992, no quotation or
               known lyric; standing words exactly canon's (the new owner, Nowak, Tom, Tommy, and only the rung's own); only the
               regulars who knew Mickey mention him, and only in the two approved lines; dialect, police and gender flags true;
               a crime line never claims more than its sureness; no line states a standing the simulation might not hold (what the street has said,
               heard, expected or felt about him; what he has done or been called before; an opening nobody set; a window the speaker may not
               have); a direction agrees with the map
  claims.*     the two lines that say 'heard you ...' and stay claim only what a StreetFacts.cs fact says, held by every named member of the kind
  cell.*       counts per kind and situation: eight or more where the kind has the situation, none where it has not
  pool.*       after every condition (each weather and hour it can happen, each standing, each accent, never-police) at least six
               lines are left in every group, so a bag is never one or two lines
  group.*      each standing's greeting reads out its rung; no two lines in a group say the same thing
  kinds.*      every person in the cast and the routines has a kind or a reason for none; every trade the old crowd generator
               names has a kind; own kinds are the four RULINGS names
  places.*     every place is where its home says, and has its directions
  rules.*      each number in rules.json agrees with the code and rulings it comes from; the priorities, silence and numbers exist
  rule.*       each rule played alone in a small scenario (a crime fades neighbours, a witness says no hello, the 45 s gap ...)
  walk.*       thirty minutes of a walk through the rules: repeats, gaps, the busiest minute; the same walk in thirty other
               seeds, a busy one of eighty passers-by, an afternoon and a night
  content.*    tools/content-gate.py over every text, tools/canon-gate.py over the files
  fault.*      the check damages a copy of the files thirty-odd ways and requires each to fail a row
Words are checked by lists: a screen, not a reader. NOTES.md says what a reader still has to judge.
"""
import copy
import importlib.util
import json
import re
import subprocess
import sys
sys.dont_write_bytecode = True
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import walk_sim  # noqa: E402

LINES = HERE / "lines.json"
RULES = HERE / "rules.json"
OUT = HERE / "checks" / "check_v1.json"
WALK_OUT = HERE / "checks" / "walk_v1.json"

# ------------------------------------------------------------------ the vocabulary the check holds the file to
RUNGS = ["stranger", "owner", "nowak", "tom", "tommy"]
KNOWN = ["owner", "nowak", "tom", "tommy"]
WEATHERS = ["dry", "drizzle", "rain"]
TIMES = ["morning", "afternoon", "evening", "night"]
SURE = {"noise": 0, "shape": 1, "face": 3}
SITUATIONS = ["greeting.stranger", "greeting.owner", "greeting.nowak", "greeting.tom", "greeting.tommy", "bumped", "rain_starts", "in_rain",
              "crime_noise", "crime_shape", "crime_face", "after_deed", "asked_way", "farewell"]
CONTEXT = {"greeting": "greeting", "bumped": "bump", "rain_starts": "rain", "in_rain": "rain", "crime": "crime", "after_deed": "deed",
           "asked_way": "way", "farewell": "farewell"}
OWN_KINDS = {"ron": "rocco", "darren": "sam", "father_walsh": "emil", "june": "june"}   # RULINGS Talk and AI: street lines own for Ron, Darren, Father Walsh and June
KEEP_SHARED = {"lena": "Sheila", "noor": "Alison", "ada": "Ada"}                       # ... Sheila, Alison and Ada keep the shared ones
ALLOWED_COND = {"standing", "weather", "time", "sure", "destination", "since_deed_s", "rain_began_within_s"}
DELIVERY = {"normal", "hushed", "raised"}
MAX_WORDS = 11            # "each under 12 words"
MIN_LINES = 8
MIN_ELIGIBLE = 6
NEVER_POLICE = {"rocco", "lena", "rita", "hal", "victor", "tibor", "drago"}   # town NOTES 14: RULINGS 1 Oct and the Ellis design
GENDER = {}   # filled from REGULARS.md and the principals
FEMALE_EXTRA = {"lena", "ada", "june", "noor", "iva", "selma", "ines", "marta", "jelena"}
MALE_EXTRA = {"rocco", "sam", "emil", "elias", "goran"}

CHILD = re.compile(r"\b(child|children|kid|kids|baby|babies|boy|boys|girl|girls|lad|lads|lass|lasses|infant|toddler|pupil|pupils|schoolboy|"
                   r"schoolgirl|nursery|little ones?|young ones?|teenager|teenagers|youngster|youngsters|school|schools|pram|pushchair|"
                   r"playground|nappy|nappies|toys?|bairn|bairns)\b", re.I)
OLD_NAMES = re.compile(r"\b(Lena|Rocco|Aldous|Vane|Sera|Kest|Noor|Elias|Novak|Toma|Father Emil|Mara|Sam|Danny Ro|Halvard|Zlata|Ferko|Marla|Dusan|"
                       r"Joey|Victor|Tibor|Vesna|Magda|Zora|Iva|Selma|Tanja|Stipe|Fabjan|Goran|Tomas|Luka|Bruno|Petra|Dario|Sanja|Hana|Franjo|"
                       r"Danica|Drago|Filip|Katarina|Ines|Marta|Jelena)\b")
EXTRA_PLACES = ["hull", "grimsby", "humberside", "hessle", "humber", "cleethorpes", "scunthorpe", "yorkshire", "lincolnshire", "east riding", "downtown",
                "north sea", "baltic", "iceland", "norway", "poland", "polish", "ireland", "irish", "cork", "scotland", "scottish", "england", "english", "britain", "british"]
MODERN = re.compile(r"\b(okay|guys|awesome|amazing|no worries|my bad|get a life|chill|innit|basically|literally|totally|seriously|"
                    r"wheelie bin|recycl\w+|cctv|postcode|smart|app|online|download|text me|phone me back|ring me back|hashtag|cool)\b|\bwhatever(?=[.!?]$)", re.I)
LYRICS = ["hey jude", "let it be", "yellow submarine", "we will rock you", "bohemian rhapsody", "another brick in the wall", "i will survive",
          "dancing queen", "ghost town", "come on eileen", "tainted love", "love me do", "she loves you", "money money money", "waterloo sunset",
          "always look on the bright side", "walking on sunshine", "karma chameleon", "back in the ussr", "stairway to heaven", "lovely jubbly",
          "plonker", "cushty", "don't panic", "i don't believe it", "are you being served", "nudge nudge", "what's all this then", "evening all",
          "ooh matron", "you're fired", "i'm free", "suits you sir", "stupid boy", "mind my bike"]
BAD_ADDRESS = re.compile(r"\b(Sir|Guv|Guvnor|Governor|Squire|Chief|Skipper|Captain|Master|Madam|Mrs|Miss|sir|guv|squire|guvnor)\b")
KIND_ADDRESS_RX = re.compile(r"\b(boss|son|young man)\b", re.I)
ADDRESS_OK = {"boss": {"ron"}, "son": {"father_walsh"}, "young man": {"pensioner"}}
POLICE = re.compile(r"\b(police|guards|station|ring|telephone|radio it in)\b", re.I)
# canon review, fault 2: what the street thinks of him is the game's mechanic, so a canned line may not claim it (the simulation may not hold it)
OPINION = re.compile(r"\b(?:they|people|folk|folks|everyone|everybody) (?:say|says|tell me|think|reckon) (?:you|he)\b[^.?!]*\b(?:fair|all right|alright|good|decent|honest|kind|straight|trouble|mad|bad|hard|soft)\b"
                     r"|\byour name'?s all over\b|\byou'?re famous\b|\bis it true what they say\b|\b(?:talking|talked) about you\b", re.I)
# canon review, fault 5: Ada's tea is asked once and never to a stranger, and Ada speaks the shared pensioner lines
TEA_INVITE = re.compile(r"\b(kettle|cuppa|come (?:in )?(?:for|to) tea|your tea|tea'?s (?:on|ready|poured)|pot'?s on|cup of tea)\b", re.I)
# canon review, follow-up of 13 October: a canned line may not state a standing the simulation might not hold. Seven kinds of claim (the last, the window, below), each its own pattern
# (and its own planted fault): what the street has said, heard, waited for or felt about him; what is reported of him; what he has done; what was said
# of his name before; an opening nobody set. 'heard you ...' passes only on the two lines whose claim a StreetFacts.cs fact holds (KEPT_CLAIMS).
STANDING_CLAIMS = [
    ("street talk", re.compile(r"\b(?:everyone|everybody)(?:'s| has| have)? (?:been )?(?:talking|hearing)\b"
                               r"|\b(?:we|they|everyone|everybody)(?:'ve| have|'d| had)? (?:all )?(?:been )?(?:hearing|heard|dying|expecting|waiting|talking|told)\b[^.?!]*\b(?:you|new owner)\b", re.I),
     "says the street has talked of him, heard of him, waited or been curious: the simulation holds none of that for the speaker"),
    ("hearsay", re.compile(r"\bheard (?:so much|all about|a lot about|plenty about|about you|of you)\b"
                           r"|\b(?:they|people|folk|everyone|everybody) (?:say|says|tell me|told me|reckon|think|know|hear) (?:you|he|that you)\b", re.I),
     "reports what is said or known of him: the simulation may not hold it"),
    ("heard you", re.compile(r"\bheard (?:that )?you\b", re.I),
     "'heard you ...' reports something about him: only a line whose claim a StreetFacts.cs fact holds for every member of the kind may (claims.kept_lines_held_by_street_facts)"),
    ("his doings", re.compile(r"\bdoing the rounds\b|\byou'?ve (?:met|seen|been round|been to|done) (?:half|all|most|everyone|everybody|the whole)\b", re.I),
     "says what he has done in the town: the simulation may not hold it"),
    ("his name", re.compile(r"\byour name right\b|\b(?:was|were|been|just|only) (?:just |only )?(?:saying|said|using|learning|practising) your name\b|\bgot your name\b", re.I),
     "says what was said of his name before: the simulation may not hold it"),
    ("an opening", re.compile(r"\bto fill\b|\bis it true\b|\bit'?s true (?:that )?you\b|\btrue (?:that )?you\b", re.I),
     "asserts, or asks as if it were so, an opening or a fact nobody set"),
]
# a speaker may not be put at a window, a door or a step in a crime line unless the kind has a shop window (the shopkeeper's: a counter, a doorway)
WINDOW_CLAIM = re.compile(r"\b(?:past|by|across|through|at|behind) (?:my|the) (?:window|door|step)\b|\bmy (?:window|door|step)\b", re.I)
# The two 'heard you ...' lines that stay (canon review follow-up, 13 October): each claims only what a StreetFacts.cs fact states, and every named member of the
# kind holds that fact in people.json: 'will' (Mickey left the office to the new owner, who came with one suitcase and a letter) and 'office' (Mickey's, with the rank outside).
KEPT_CLAIMS = {
    "dock_worker.greet-owner.05": {"phrase": "one suitcase", "facts": {"will": ["came with one suitcase"]}},
    "casual_worker.greet-owner.02": {"phrase": "a rank to run", "facts": {"office": ["with the rank outside"], "will": ["left the office", "the new owner"]}},
}

rows = []


def row(rid, what, ok, detail=""):
    rows.append({"id": rid, "what": what, "pass": bool(ok), "detail": detail if not ok else (detail or "")})


def words(s):
    return re.findall(r"[a-z0-9']+", s.lower().replace("’", "'"))


def norm(t):
    return re.sub(r"[^a-z0-9 ]+", "", t.lower().replace("’", "'").replace("'", "")).strip()


# ------------------------------------------------------------------ the homes, read afresh

def load_content_gate():
    spec = importlib.util.spec_from_file_location("_cg", REPO / "tools" / "content-gate.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CG = load_content_gate()


def cs_array(path, name):
    src = (REPO / path).read_text(encoding="utf-8")
    a = src.index("static readonly string[] %s" % name)
    b = src.index("};", a)
    return re.findall(r'"([^"]+)"', re.sub(r"//[^\n]*", "", src[a:b]))


ANYCASE = cs_array("ledger/Assets/Scripts/Core/RealWorld.cs", "AnyCase")
ASNAME = cs_array("ledger/Assets/Scripts/Core/RealWorld.cs", "AsName")
ANY_RX = re.compile(r"(?<![\w'])(" + "|".join(re.escape(x) for x in ANYCASE) + r")(?![\w-])", re.I)
NAME_RX = re.compile(r"(?<![\w'])(" + "|".join(re.escape(x) for x in ASNAME) + r")(?![\w'-])")
PLACE_RX = re.compile(r"(?<![\w'])(" + "|".join(re.escape(x) for x in EXTRA_PLACES) + r")(?![\w-])", re.I)
TRADES = cs_array("ledger/Assets/Scripts/Core/Population.cs", "Trades")
HK = json.loads((REPO / "production/specs/hook-cast.json").read_text(encoding="utf-8"))
HK_IDS = [p["id"] for p in HK["people"]]
TOWN = json.loads((REPO / "production/cloud-week/town/people.json").read_text(encoding="utf-8"))
TOWN_IDS = [p["id"] for p in TOWN["people"]]
KNEW_MICKEY = {p["id"] for p in TOWN["people"] if p["knew_mickey"]}
ATLAS = json.loads((REPO / "production/art/atlas-01/data/atlas.json").read_text(encoding="utf-8"))


def _proposal_names(node, out):
    if isinstance(node, dict):
        n = node.get("name")
        if isinstance(n, str) and "(proposal)" in n:
            out.add(re.sub(r"\s*\(proposal\)", "", n))
        for v in node.values():
            _proposal_names(v, out)
    elif isinstance(node, list):
        for v in node:
            _proposal_names(v, out)
    return out


PROPOSAL_NAMES = {n for n in _proposal_names(ATLAS, set()) if not re.search(r"[→/]|alignment", n)}   # the atlas's street and footway names only
BARKS = json.loads((REPO / "game-design/barks.json").read_text(encoding="utf-8"))
SV = (REPO / "ledger/Assets/Scripts/Core/StreetVoice.cs").read_text(encoding="utf-8")
SF = (REPO / "ledger/Assets/Scripts/Core/StreetFacts.cs").read_text(encoding="utf-8")
TOWN_BY_ID = {p["id"]: p for p in TOWN["people"]}


def street_fact_text(fid):
    """The street's words for a StreetFacts.cs fact (the third string of its tuple), or None."""
    m = re.search(r'\("%s",\s*"[^"]*",\s*"((?:[^"\\]|\\.)*)"' % re.escape(fid), SF)
    return m.group(1) if m else None


def string_literals(path):
    src = (REPO / path).read_text(encoding="utf-8")
    return [m.group(1).encode().decode("unicode_escape", errors="ignore") if "\\" in m.group(1) else m.group(1)
            for m in re.finditer(r'"((?:[^"\\\n]|\\.)*)"', src)]


def existing_texts():
    """Every spoken text the street already has: a line here that repeats one is a second home for the same fact."""
    ts = set()
    for p in ("ledger/Assets/Scripts/Core/StreetVoice.cs", "ledger/Assets/Scripts/Core/OwnLines.cs"):
        for s in string_literals(p):
            if " " in s and len(s) > 8:
                ts.add(norm(s))
    for slot in BARKS["slots"]:
        for l in slot["lines"]:
            ts.add(norm(l))
    for f in ("content/dialogue/crime-witness-v1.json", "content/dialogue/pub-regular-v1.json"):
        d = json.loads((REPO / f).read_text(encoding="utf-8"))
        for l in d.get("lines", []):
            if l.get("text"):
                ts.add(norm(l["text"]))
    return ts


EXISTING = existing_texts()


def approved_mickey_lines():
    out = set()
    for key in ("mickey_counsel", "mickey_kept_ron"):
        a = SF.index('("%s"' % key)
        b = SF.index('("', a + 5)
        for s in re.findall(r'"((?:[^"\\]|\\.)*)"', SF[a:b]):
            if " " in s:
                out.add(norm(s))
    return out


APPROVED_MICKEY = approved_mickey_lines()


def gender_map():
    g = {}
    t = (REPO / "production/casting/regulars/REGULARS.md").read_text(encoding="utf-8")
    for line in t.splitlines():
        m = re.match(r"\|\s*\d+\s*\|\s*(\w+)\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*(woman|man)\b", line)
        if m:
            g[m.group(1)] = "f" if m.group(2) == "woman" else "m"
    for i in FEMALE_EXTRA:
        g[i] = "f"
    for i in MALE_EXTRA:
        g[i] = "m"
    return g


GENDER = gender_map()


# ------------------------------------------------------------------ memo for the word screens (the seeded faults re-run them)

_screen_cache = {}


def screen(text):
    """The content gate and the word lists over one text. Returns a list of what was found."""
    if text in _screen_cache:
        return _screen_cache[text]
    found = ["gate:" + h[0] + ":" + h[2] for h in CG.scan(text)]
    found += ["slur:" + w for w in (CG.SLURS or []) if re.search(r"\b" + re.escape(w) + r"\b", text, re.I)]
    for m in CHILD.finditer(text):
        found.append("child:" + m.group(0))
    for rx, tag in ((ANY_RX, "real"), (NAME_RX, "real"), (PLACE_RX, "place")):
        for m in rx.finditer(text):
            found.append("%s:%s" % (tag, m.group(0)))
    for m in OLD_NAMES.finditer(text):
        found.append("oldname:" + m.group(0))
    for m in re.finditer(r"\b(19[0-9]{2}|20[0-9]{2})\b", text):
        if int(m.group(0)) > 1992:
            found.append("era:" + m.group(0))
    for m in MODERN.finditer(text):
        found.append("modern:" + m.group(0))
    low = text.lower()
    for ly in LYRICS:
        if ly in low:
            found.append("lyric:" + ly)
    if re.search(r"[\"“”♪♫]|\.\.\.|…", text):
        found.append("quotation or lyric mark")
    _screen_cache[text] = found
    return found


# ------------------------------------------------------------------ places: where each is, from the homes

def home_places():
    """id -> (x, z) from the homes: hook-cast.json places, the built street, the atlas converted with its own anchor."""
    P = HK["places"]
    out = {
        "quay": (P["quay"]["x_m"], P["quay"]["z_m"]), "mickeys": (P["mickeys_office"]["x_m"], P["mickeys_office"]["z_m"]),
        "fish_shop": (P["fish_counter"]["x_m"], P["fish_counter"]["z_m"]), "ritas": (P["ritas_counter"]["x_m"], P["ritas_counter"]["z_m"]),
        "phone_box": (P["kiosk"]["x_m"], P["kiosk"]["z_m"]), "laundry": (P["laundry_counter"]["x_m"], P["laundry_counter"]["z_m"]),
        "cafe": (P["cafe"]["x_m"], P["cafe"]["z_m"]), "newsagent": (P["pension_counter"]["x_m"], P["pension_counter"]["z_m"]),
        "bus_stop": (P["bus_stop"]["x_m"], P["bus_stop"]["z_m"]),
        "docks": (P["docks"]["x_m"], P["docks"]["z_m"]), "fish_dock": (P["fish_dock"]["x_m"], P["fish_dock"]["z_m"]),
        "boatyard": (P["repair_yard"]["x_m"], P["repair_yard"]["z_m"]), "harbour_office": (P["harbour_office"]["x_m"], P["harbour_office"]["z_m"]),
        "customs_shed": (P["customs_shed"]["x_m"], P["customs_shed"]["z_m"]), "ferry": (P["ferry_stop"]["x_m"], P["ferry_stop"]["z_m"]),
        "warehouse_row": (P["warehouse_row"]["x_m"], P["warehouse_row"]["z_m"]), "walsh_chapel": (P["chapel"]["x_m"], P["chapel"]["z_m"]),
        "open_market": (P["market"]["x_m"], P["market"]["z_m"]), "boarding_house": (P["boarding_house"]["x_m"], P["boarding_house"]["z_m"]),
        "flats": (P["flats"]["x_m"], P["flats"]["z_m"]), "allotments": (P["allotments"]["x_m"], P["allotments"]["z_m"]),
    }
    scene = json.loads((REPO / "production/specs/vignette-scene.json").read_text(encoding="utf-8"))
    kiosk = [f for f in scene["furniture"] if f.get("bom") == "E3_telephone_kiosk"][0]
    assert abs(kiosk["x_m"] - out["phone_box"][0]) < 0.01
    east = [b for b in scene["blocks"] if b["id"] == "east_parade"][0]
    bay = lambda i: (east["start_x_m"] + east["bay_width_m"] * (i + 0.5), 7.5)       # noqa: E731
    out["grocer"] = bay(5)       # RULINGS trades: bay 5 grocer
    out["chandler"] = (43.0, 7.5)   # east_chandler_bay0, x 40 to 46 (vignette-scene.json street.length_note)
    anchor = ATLAS["street_anchor"]["origin_atlas"]
    names = {"H2": "old_basin", "H3": "harbour_board", "C1": "market_hall", "P1": "tivoli", "F1": "fairview_chapel", "E1": "records_court", "E2": "police_station",
             "I1": "canteen", "I2": "retort_works", "G1": "winter_rooms", "G2": "short_pier"}
    for lm in ATLAS["landmarks"]:
        if lm["id"] in names:
            out[names[lm["id"]]] = (lm["point"][1] - 350.0, lm["point"][0] - 400.0)   # x = north - 350, z = east - 400 (atlas street_anchor.source_to_atlas)
    return out


HOME_PLACES = home_places()
STREET_SIDE = {"mickeys": "east", "fish_shop": "east", "ritas": "east", "phone_box": "east", "laundry": "east", "grocer": "east", "chandler": "east",
               "cafe": "west", "newsagent": "west", "bus_stop": "west"}
STREET_IDS = ["quay", "mickeys", "fish_shop", "ritas", "phone_box", "laundry", "grocer", "chandler", "cafe", "newsagent", "bus_stop"]
# Hal's coin shop (hook-cast.json x 39) has no unit on the built street: the west row is a tea room, an ironmonger and the newsagent (RULINGS 3 Oct).
# Its directions are held until Jafar places it, so it is in no list of places here (canon review of 13 October, fault 4).
HELD_PLACES = ["hals"]
PLACE_CLASS_FAR_M = 200.0
MIDDLE = 24.0


def place_class(pid):
    x, z = HOME_PLACES[pid]
    if pid in STREET_IDS:
        return "street"
    return "down" if x < 0 else "up"


def place_far(pid):
    x, z = HOME_PLACES[pid]
    return ((x - MIDDLE) ** 2 + z ** 2) ** 0.5 > PLACE_CLASS_FAR_M


def strip_the(s):
    return re.sub(r"^the\s+", "", s.strip(), flags=re.I)


def name_forms(names):
    out = set()
    for n in names:
        out.add(strip_the(n).lower())
        out.add(n.lower())
    return out


def mentions(text, forms):
    low = text.lower().replace("’", "'")
    return any(re.search(r"(?<![\w])" + re.escape(f) + r"(?![\w])", low) for f in forms)


ANCHOR_NAMES = {"quay": ["the quay"], "mickeys": ["mickey's", "the cab office"], "fish_shop": ["the fish shop"], "ritas": ["rita's", "the pawn"],
                "phone_box": ["the phone box"], "laundry": ["the laundry"], "grocer": ["the grocer's"], "chandler": ["the chandler's"], "cafe": ["the caff"],
                "newsagent": ["the paper shop", "the newsagent's"], "bus_stop": ["the bus stop"], "docks": ["the dock gate", "the docks"],
                "walsh_chapel": ["the chapel"], "open_market": ["the market"], "harbour_office": ["the harbour office"], "customs_shed": ["the customs shed"]}
REL = [
    (r"\b(?:up past|up from)\s+(?:the\s+)?", "up"),
    (r"\b(?:down past|down from)\s+(?:the\s+)?", "down"),
    (r"\b(?:next door to|next to|beside|by|near)\s+(?:the\s+)?", "near"),
    (r"\b(?:opposite|across from|across the road from|over the road from|over from)\s+(?:the\s+)?", "opp"),
]


def way_failures(text, pid, names):
    """Where the words say a place is, against where its home says it is."""
    if pid not in HOME_PLACES:
        return ["directions to %s, which is not a place on the built street (held places have none)" % pid]
    fails = []
    low = text.lower().replace("\u2019", "'")
    x, z = HOME_PLACES[pid]
    cls = place_class(pid)
    far = place_far(pid)
    forms = name_forms(names)
    if pid == "police_station":
        forms.add("station")
    if pid == "cafe":
        forms.add("grace's")
    if pid == "mickeys":
        forms.update({"cab office", "the rank"})
    consumed = low
    both_street = lambda o: pid in STREET_IDS and o in STREET_IDS   # noqa: E731
    for oid, nms in ANCHOR_NAMES.items():
        if oid == pid:
            continue
        ox, oz = HOME_PLACES[oid]
        for nm in sorted(nms, key=lambda n: -len(n)):
            bare = strip_the(nm)
            for rx, kind in REL:
                for m in re.finditer(rx + re.escape(bare) + r"(?![\w])", consumed):
                    if kind == "up" and not x > ox:
                        fails.append("says up from %s but it is not" % nm)
                    if kind == "down" and not x < ox:
                        fails.append("says down from %s but it is not" % nm)
                    if kind == "near":
                        d = abs(x - ox) if both_street(oid) else ((x - ox) ** 2 + (z - oz) ** 2) ** 0.5
                        if d > (7.0 if both_street(oid) else 60.0):
                            fails.append("says next to %s but it is %.0f m off" % (nm, d))
                    if kind == "opp" and not (both_street(oid) and STREET_SIDE.get(pid) != STREET_SIDE.get(oid) and abs(x - ox) <= 10.0):
                        fails.append("says opposite %s but it is not" % nm)
                consumed = re.sub(rx + re.escape(bare) + r"(?![\w])", " ", consumed)
    if re.search(r"(?<!up )(?<!down )\b(past|before|after|beyond)\b", consumed.replace("past the top", " ")):
        fails.append("a bare 'past', 'before', 'after' or 'beyond': it depends which way he walks; say up past or down past")
    top = re.search(r"\b(the top|near the top|top of|very top|up the top)\b", consumed)
    hill = re.search(r"\b(up the hill|uphill|climb|climbing|up and up)\b", consumed)
    bottom = re.search(r"\b(bottom|quay end|nearest the quay)\b", consumed)
    up_word = re.search(r"\bup\b", consumed)
    down_word = re.search(r"\bdown\b", consumed)
    if cls == "up":
        if bottom or down_word:
            fails.append("says down for a place up the hill")
    elif cls == "down":
        if top or hill or up_word:
            fails.append("says up for a place down by the water")
    else:
        if top and x < 33.0:
            fails.append("says the top for a place at %.0f m" % x)
        if bottom and x > 12.0:
            fails.append("says the bottom for a place at %.0f m" % x)
        if up_word and x < 9.0:
            fails.append("says up for a place at the bottom")
        if down_word and x > 12.0:
            fails.append("says down for a place at %.0f m" % x)
        if hill:
            fails.append("says the hill for a place on the street")
    if re.search(r"\b(long walk|long way|good walk|very long|a long|far(?! (end|side)))\b", low) and not far:
        fails.append("says far for a place under 200 m off")
    if re.search(r"\b(short walk|round the corner|not far|a step)\b", low) and far:
        fails.append("says near for a place over 200 m off")
    for compass, ok in (("east", z > 100.0), ("west", z < -100.0), ("north(?! (half|end))", False), ("south", False)):
        if re.search(r"\b" + compass + r"\b", low) and not ok:
            fails.append("says %s for a place that is not" % compass)
    if re.search(r"\b(left|right)\b", low):
        fails.append("says left or right (it depends which way he faces)")
    return fails


# ------------------------------------------------------------------ a line

CAP_NAMES = re.compile(r"\b(Tom|Tommy|Nowak|Mickey|Mickey's)\b")


def standing_words(text):
    return {"new owner": bool(re.search(r"\bnew owner\b", text, re.I)), "Nowak": bool(re.search(r"\bNowak\b", text)),
            "Tom": bool(re.search(r"\bTom\b", text)), "Tommy": bool(re.search(r"\bTommy\b", text))}


def mickey_failures(text, kind, cond):
    fails = []
    n = norm(text)
    if n in APPROVED_MICKEY:
        if kind not in OWN_KINDS or OWN_KINDS[kind] not in KNEW_MICKEY:
            fails.append("an approved Mickey line in a kind whose speakers did not all know him")
        return fails
    for m in re.finditer(r"\bMickey\b", text):
        rest = text[m.end():]
        if re.match(r"'s(?! (nephew|daughter|funeral|death|heart|friend|widow|boy|man|family|name|sister|brother|will|money|business|people|crowd|lot|arrangement|run|day|old))", rest):
            continue          # the place: Mickey's, the cab office
        if re.match(r"'s old (place|office)\b", rest):
            continue
        fails.append("describes or names Mickey outside the two approved lines")
        break
    return fails


def line_failures(l, ctx):
    """Everything wrong with one line. ctx has the doc's vocabulary and the home-derived data."""
    f = []
    need = ["id", "bank", "context", "situation", "kind", "speaker", "rung", "text", "conditions", "weight", "group", "delivery", "dialect"]
    for k in need:
        if k not in l:
            f.append("missing field " + k)
    if f:
        return f
    t = l["text"]
    kind, sit = l["kind"], l["situation"]
    if not isinstance(t, str) or not t.strip():
        return ["empty text"]
    if t != t.strip() or "  " in t or "{" in t or "}" in t:
        f.append("spacing or a placeholder")
    if not re.search(r"[.?!]$", t):
        f.append("no closing full stop, question or exclamation mark")
    nw = len(t.split())
    if nw > MAX_WORDS:
        f.append("%d words (the limit is %d)" % (nw, MAX_WORDS))
    # fields
    if sit not in SITUATIONS:
        f.append("unknown situation")
        return f
    fam = "greeting" if sit.startswith("greeting") else "crime" if sit.startswith("crime") else sit
    if l["context"] != CONTEXT[fam]:
        f.append("context %s is not %s" % (l["context"], CONTEXT[fam]))
    if l["speaker"] != kind:
        f.append("speaker is not kind")
    if kind not in ctx["kinds"] and kind != "anyone":
        f.append("unknown kind")
        return f
    exp_rung = sit.split(".")[1] if sit.startswith("greeting") else "any"
    if l["rung"] != exp_rung:
        f.append("rung %s is not %s" % (l["rung"], exp_rung))
    if sit.startswith("crime"):
        s = sit.split("_")[1]
        if l.get("idRung") != SURE[s]:
            f.append("idRung is not %d" % SURE[s])
    elif "idRung" in l:
        f.append("idRung on a line that is not a crime line")
    dest = l["conditions"].get("destination")
    bank_expect = ctx["banks"][sit] + ("/to/" + dest if dest else "")
    if l["bank"] != bank_expect or l["group"] != "%s@%s" % (l["bank"], kind):
        f.append("bank or group is not the derived one")
    if not (isinstance(l["weight"], int) and 1 <= l["weight"] <= 3):
        f.append("weight not 1 to 3")
    if l["delivery"] not in DELIVERY:
        f.append("delivery not valid")
    if sit == "after_deed" and l["delivery"] != "hushed":
        f.append("after a deed the delivery is hushed")
    if sit.startswith("greeting") and l["delivery"] != "normal":
        f.append("a greeting is not hushed or raised")
    if l["delivery"] == "raised" and not sit.startswith("crime"):
        f.append("raised outside a crime")
    # conditions
    c = l["conditions"]
    if not isinstance(c, dict) or set(c) - ALLOWED_COND:
        f.append("unknown condition key %s" % sorted(set(c) - ALLOWED_COND))
    else:
        if "standing" in c and (not c["standing"] or set(c["standing"]) - set(RUNGS)):
            f.append("invalid standing")
        if "weather" in c and (not c["weather"] or set(c["weather"]) - set(WEATHERS)):
            f.append("invalid weather")
        if "time" in c and (not c["time"] or set(c["time"]) - set(TIMES)):
            f.append("invalid time")
        if "sure" in c and c["sure"] not in SURE:
            f.append("invalid sure")
        if "since_deed_s" in c and not (isinstance(c["since_deed_s"], list) and len(c["since_deed_s"]) == 2 and 0 <= c["since_deed_s"][0] < c["since_deed_s"][1] <= 3600):
            f.append("invalid since_deed_s")
        if "rain_began_within_s" in c and not (isinstance(c["rain_began_within_s"], (int, float)) and 0 < c["rain_began_within_s"] <= 120):
            f.append("invalid rain_began_within_s")
        if "destination" in c and c["destination"] not in ctx["place_ids"]:
            f.append("unknown destination")
        if sit.startswith("greeting") and c.get("standing") != [exp_rung]:
            f.append("a greeting's standing condition is its rung")
        if sit.startswith("crime") and c.get("sure") != sit.split("_")[1]:
            f.append("a crime line's sure is its situation's")
        if not sit.startswith("crime") and "sure" in c:
            f.append("sure outside a crime line")
        if sit == "after_deed" and "since_deed_s" not in c:
            f.append("after a deed needs since_deed_s")
        if sit != "after_deed" and "since_deed_s" in c:
            f.append("since_deed_s outside after a deed")
        if sit in ("rain_starts", "in_rain"):
            if not c.get("weather") or set(c["weather"]) - {"drizzle", "rain"}:
                f.append("a rain line holds only in drizzle or rain")
        if sit == "rain_starts" and "rain_began_within_s" not in c:
            f.append("rain_starts needs rain_began_within_s")
        if "destination" in c and sit != "asked_way":
            f.append("destination outside asked_way")
        if "standing" in c and not sit.startswith("greeting"):
            if sit != "bumped":
                f.append("standing condition on a line that is not a greeting or a bump")
        if "standing" in c and kind in ctx["kinds"] and not set(c["standing"]) & set(ctx["kinds"][kind]["greeting_rungs"]):
            f.append("no speaker of this kind can stand at that rung with him, so the line could never be said")
    # content: the gate and the word lists
    for fnd in screen(t):
        f.append("content " + fnd)
    # standing words: exactly canon's, and only the rung's own
    sw = standing_words(t)
    allowed = set()
    if sit.startswith("greeting"):
        allowed = {"owner": {"new owner"}, "nowak": {"Nowak"}, "tom": {"Tom"}, "tommy": {"Tommy"}, "stranger": set()}[exp_rung]
    for w, present in sw.items():
        if present and w not in allowed:
            f.append("standing word %s outside its rung" % w)
    for a in BAD_ADDRESS.findall(t):
        f.append("address word '%s' is not canon's" % a)
    for a in KIND_ADDRESS_RX.findall(t):
        if kind not in ADDRESS_OK.get(a.lower(), set()):
            f.append("address word '%s' belongs to another kind" % a.lower())
    if OPINION.search(t):
        f.append("says what the street thinks of him: the simulation may not hold it (canon review, fault 2)")
    if kind == "pensioner" and TEA_INVITE.search(t):
        f.append("an invitation to tea in a kind Ada speaks: her tea is asked once and never to a stranger (day-three design)")
    for code, rx, why in STANDING_CLAIMS:
        if rx.search(t) and not (code == "heard you" and l["id"] in KEPT_CLAIMS):
            f.append("standing claim (%s): %s" % (code, why))
    if sit.startswith("crime") and kind != "shopkeeper" and WINDOW_CLAIM.search(t):
        f.append("standing claim (a window): puts the speaker at a window, door or step, which a speaker of this kind may not have; only the shopkeeper's kind has a shop window")
    # Mickey
    f += mickey_failures(t, kind, c)
    # gendered words only where the kind is single-gender
    if kind in ctx["kinds"] and ctx["kinds"][kind]["voice"] == "any" or kind == "anyone":
        for g in ctx["gender_words"]:
            if re.search(r"\b" + g + r"\b", t, re.I):
                f.append("gendered word '%s' in a kind spoken by either voice" % g)
    # dialect and police flags are true
    low = " " + norm(t) + " "
    local = any(" " + m + " " in low for m in ctx["dialect_markers"])
    if (l["dialect"] == "local") != local:
        f.append("dialect flag is %s but the words say %s" % (l["dialect"], "local" if local else "plain"))
    if bool(l.get("calls_police")) != bool(POLICE.search(t)):
        f.append("calls_police flag is wrong")
    if kind == "ron" and l.get("calls_police"):
        f.append("Ron never goes to the police about one of Mickey's own (RULINGS 1 Oct)")
    # a crime line never claims more than its sureness
    if sit == "crime_noise":
        tt = re.sub(r"(never saw|didn't see|did not see|haven't seen|engine running)", " ", t, flags=re.I)
        if re.search(r"\b(saw|seen|face|figure|shape|ran|running|legged|looked|watching|spotted|glimpse\w*)\b", tt, re.I):
            f.append("a noise line claims to have seen something")
    if sit == "crime_shape":
        if re.search(r"\b(face|name|he|she|him|his|her|man|woman|bloke|coat|jacket|hat|tall|short|fat|thin)\b", t, re.I) or re.search(r"\bI (knew|know)\b", t):
            f.append("a shape line gives a face, a name, a sex or a mark")
    if sit == "crime_face":
        if re.search(r"\b(did it|done it|guilty|i know who|it was (him|her|them)|whose)\b", t, re.I) or re.search(r"(?<!'d )(?<!would )\bI know (that|the|this) face\b", t):
            f.append("a face line names, accuses or claims to have placed the face")
    if sit == "after_deed" and CAP_NAMES.search(t):
        f.append("a line after a deed names somebody")
    # directions against the map
    if sit == "asked_way":
        if dest:
            if kind != "anyone":
                f.append("a destination line must be kind anyone")
            else:
                f += way_failures(t, dest, ctx["place_names"].get(dest, []))
        else:
            if kind == "anyone":
                f.append("anyone says only destination lines")
            if re.search(r"\b(up|down|top|bottom|east|west)\b", t, re.I) and False:
                f.append("a place-free answer gives a direction")
    elif dest:
        f.append("destination outside asked_way")
    return f


# ------------------------------------------------------------------ groups and cells

def kinds_required(kind, ctx):
    """The situations a kind must have lines for."""
    req = []
    for r in ctx["kinds"][kind]["greeting_rungs"]:
        req.append("greeting." + r)
    req += ["bumped", "rain_starts", "in_rain", "crime_noise", "crime_shape", "crime_face", "after_deed", "asked_way", "farewell"]
    return req


def cond_ok(l, w, tm, standing=None, since_deed=None):
    c = l["conditions"]
    if "weather" in c and w not in c["weather"]:
        return False
    if "time" in c and tm not in c["time"]:
        return False
    if standing is not None and "standing" in c and standing not in c["standing"]:
        return False
    return True


def group_rows_for(doc, ctx, emit):
    by_group = defaultdict(list)
    for l in doc["lines"]:
        by_group[l["group"]].append(l)
    kinds = ctx["kinds"]
    counts = Counter((l["kind"], l["situation"]) for l in doc["lines"] if l["kind"] != "anyone")
    # cells
    for k in kinds:
        if k == "anyone":
            continue
        req = kinds_required(k, ctx)
        for sit in req:
            n = counts.get((k, sit), 0)
            min_n = 12 if sit == "greeting.stranger" else MIN_LINES
            emit("cell.%s.%s" % (k, sit), "%s has at least %d lines for %s" % (k, min_n, sit), n >= min_n, "%d" % n)
        extra = [s for (kk, s), n in counts.items() if kk == k and s not in req]
        emit("cell.%s.extra" % k, "%s has no lines for a situation it does not have (%s)" % (k, ", ".join(sorted(set(SITUATIONS) - set(req)))), not extra, str(extra))
    # pools: every condition applied, six left (a destination group holds five and is judged by places.*)
    for g, ls in sorted(by_group.items()):
        kind = ls[0]["kind"]
        sit = ls[0]["situation"]
        if kind == "anyone" or kind not in kinds:
            continue
        persons = [m for m in kinds[kind]["members"]] or [None]
        combos = {(who in ctx["not_local"], who in ctx["never_police"], frozenset(ctx["excluded"].get(who, ()))) for who in persons}
        standings = kinds[kind]["greeting_rungs"] if sit == "bumped" else [sit.split(".")[1]] if sit.startswith("greeting") else [None]
        worst, worst_at = 999, ""
        for w in WEATHERS:
            if sit in ("rain_starts", "in_rain") and w == "dry":
                continue
            for tm in TIMES:
                for st in standings:
                    base = [l for l in ls if cond_ok(l, w, tm, st)]
                    for nl, npol, nex in combos:
                        el = base
                        if nl:
                            el = [l for l in el if l["dialect"] != "local"]
                        if npol:
                            el = [l for l in el if not l.get("calls_police")]
                        if nex:
                            el = [l for l in el if l["id"] not in nex]
                        if len(el) < worst:
                            worst, worst_at = len(el), "%s %s %s accent-limited=%s never-police=%s" % (w, tm, st, nl, npol)
        emit("pool." + g, "%s keeps at least %d lines in every weather and hour, standing, accent and never-police case" % (g, MIN_ELIGIBLE), worst >= MIN_ELIGIBLE, "worst %d at %s" % (worst, worst_at))
    # each rung reads out its word
    for g, ls in sorted(by_group.items()):
        sit = ls[0]["situation"]
        if not sit.startswith("greeting.") or sit == "greeting.stranger":
            continue
        rung = sit.split(".")[1]
        kind = ls[0]["kind"]
        if kind not in kinds:
            continue
        pats = {"owner": [r"\bnew owner\b"], "nowak": [r"\bNowak\b"], "tom": [r"\bTom\b"], "tommy": [r"\bTommy\b"]}[rung]
        if kind == "ron":
            pats = pats + [r"\bboss\b"]
        have = sum(1 for l in ls if any(re.search(p, l["text"], re.I) for p in pats))
        emit("group.reads_rung." + g, "%s reads out its rung (at least half the lines carry the word)" % g, have * 2 >= len(ls), "%d of %d" % (have, len(ls)))
    # no two KINDS say the same thing in other words: the same retort in two mouths is what failed the earlier attempts (set-aside-2026-09-30, own-lines-2026-10-01)
    RUNGW = re.compile(r"\b(the new owner|new owner|Mr Nowak|Nowak|Tommy|Tom|boss|son|mate|love|dear|friend|pal)\b", re.I)
    by_sit = defaultdict(list)
    for l in doc["lines"]:
        if l["kind"] != "anyone":
            by_sit[l["situation"]].append((l["id"], l["kind"], set(words(RUNGW.sub(" ", l["text"])))))
    for sit, ls in sorted(by_sit.items()):
        bad = []
        for i in range(len(ls)):
            for j in range(i + 1, len(ls)):
                if ls[i][1] == ls[j][1] or not ls[i][2] or not ls[j][2]:
                    continue
                if len(ls[i][2] & ls[j][2]) / len(ls[i][2] | ls[j][2]) >= 0.6:
                    bad.append("%s ~ %s" % (ls[i][0], ls[j][0]))
        emit("cross." + sit, "no two kinds say the same thing in other words in %s (at least 60 percent of the words shared, address words aside)" % sit, not bad, "; ".join(bad[:3]))
    # no two lines in a group say the same thing
    STOP = set("the a an i you it to of and in on is was my me we that this at for with be are not no do don't i'd i'll it's that's you'll you're i've they them there here so as but if or by from have has had will would can could just then than too very really".split())
    RUNGWORD = re.compile(r"\b(the new owner|new owner|Mr Nowak|Nowak|Tommy|Tom|boss)\b", re.I)
    for g, ls in sorted(by_group.items()):
        if "/to/" in g:
            continue      # several wordings of one fact are the point of a place's directions; exact repeats are caught by doc.texts_unique
        bad = []
        for i in range(len(ls)):
            wi = words(RUNGWORD.sub(" ", ls[i]["text"]))
            ci = {w for w in wi if w not in STOP}
            grams_i = {tuple(wi[k:k + 4]) for k in range(len(wi) - 3)}
            for j in range(i + 1, len(ls)):
                wj = words(RUNGWORD.sub(" ", ls[j]["text"]))
                cj = {w for w in wj if w not in STOP}
                grams_j = {tuple(wj[k:k + 4]) for k in range(len(wj) - 3)}
                share = grams_i & grams_j
                ov = len(ci & cj) / max(1, min(len(ci), len(cj)))
                if share or (ov >= 0.75 and min(len(ci), len(cj)) >= 3):
                    bad.append("%s ~ %s" % (ls[i]["id"].split(".")[-1], ls[j]["id"].split(".")[-1]))
        emit("group.distinct." + g, "no two lines in %s say the same thing (a shared 4-word run, or three-quarters of the content words)" % g, not bad, "; ".join(bad[:4]))


# ------------------------------------------------------------------ the doc as a whole

def doc_rows(doc, rules, emit, light=False):
    lines = doc["lines"]
    kinds = doc["speakers"]
    ctx = {
        "kinds": kinds, "banks": {s: None for s in SITUATIONS},
        "place_ids": {p["id"] for p in doc["places"]}, "place_names": {p["id"]: p["names"] for p in doc["places"]},
        "gender_words": ["husband", "wife", "missus", "wifey", "mam", "mum", "mummy", "dad", "widow", "widower", "gentleman", "lady", "madam", "ladies"],
        "dialect_markers": ["nowt", "owt", "summat", "aye", "nithered", "mither", "mardy", "nesh", "ey up", "eh up", "now then", "ginnel", "gansey", "mucky", "daft", "tha", "reet", "chuffed", "scran"],
        "not_local": set(rules["speaker_overrides"]["not_local_voice"]["speakers"]),
        "never_police": set(rules["speaker_overrides"]["never_police"]["speakers"]),
        "excluded": {who: set(rules["speaker_overrides"].get("excluded_lines", {}).get("lines", [])) for who in rules["speaker_overrides"].get("excluded_lines", {}).get("speakers", [])},
    }
    ctx["banks"] = {"greeting.stranger": "greeting/stranger", "greeting.owner": "greeting/owner", "greeting.nowak": "greeting/nowak", "greeting.tom": "greeting/tom",
                    "greeting.tommy": "greeting/tommy", "bumped": "bumped", "rain_starts": "rain/starts", "in_rain": "rain/in", "crime_noise": "crime/noise",
                    "crime_shape": "crime/shape", "crime_face": "crime/face", "after_deed": "deed/after", "asked_way": "way/ask", "farewell": "farewell"}
    # ---- the header
    emit("doc.header", "lines.json has the dialogue bank's own header (bank, license, era, register) and the new fields' legend",
         all(k in doc for k in ("bank", "license", "era", "register", "rungs", "speakers", "lines", "fields", "places", "weather", "time", "contexts", "situations")) and doc["era"] == "1988-1992"
         and doc["license"].startswith("original-work"), "")
    emit("doc.vocabulary", "rungs, situations, weather and time bands are the ones the check holds it to",
         doc["rungs"] == RUNGS and doc["situations"] == SITUATIONS and list(doc["weather"]) == WEATHERS and list(doc["time"]) == TIMES and doc["idRungs"] == [0, 1, 3], "")
    # ---- unique ids and texts, and no second home for a line the street already has
    ids = Counter(l.get("id") for l in lines)
    emit("doc.ids_unique", "every id is unique", all(v == 1 for v in ids.values()), str([k for k, v in ids.items() if v > 1][:4]))
    texts = defaultdict(list)
    for l in lines:
        texts[norm(l.get("text", ""))].append(l.get("id"))
    dup = {k: v for k, v in texts.items() if len(v) > 1}
    emit("doc.texts_unique", "no two lines in the whole bank have the same words (case and punctuation aside)", not dup, str(list(dup.values())[:4]))
    ex = [ids_[0] for t, ids_ in texts.items() if t in EXISTING]
    emit("doc.no_second_home", "no line repeats one the street already has (StreetVoice.cs, OwnLines.cs, barks.json, the dialogue banks)", not ex, str(ex[:6]))
    # ---- no street name the adopted atlas still marks '(proposal)': canon mints three streets (Quay Street, Weighhouse Lane, Tannery Row)
    proposal_names = sorted(PROPOSAL_NAMES)
    bad_names = [l["id"] for l in lines if any(n.lower() in l.get("text", "").lower() for n in proposal_names)]
    emit("doc.no_proposal_street_names", "no line speaks a street name the adopted atlas still marks '(proposal)' (canon mints three: Quay Street, Weighhouse Lane, Tannery Row)",
         not bad_names and len(proposal_names) >= 5, "%s %s" % (bad_names[:4], len(proposal_names)))
    # ---- one row for every line
    for l in lines:
        fails = line_failures(l, ctx)
        emit("line." + str(l.get("id")), "line %s passes every line check" % l.get("id"), not fails, "; ".join(fails[:5]))
    kept_claims_row(doc, emit)
    group_rows_for(doc, ctx, emit)
    kinds_rows(doc, ctx, emit)
    places_rows(doc, ctx, emit)
    return ctx


def kept_claims_row(doc, emit):
    """The lines that say 'heard you ...' and stay: the words still carry the claim, a StreetFacts.cs fact states it, and every named member of the kind holds that fact."""
    by_id = {l["id"]: l for l in doc["lines"]}
    bad = []
    for lid, c in KEPT_CLAIMS.items():
        l = by_id.get(lid)
        if l is None:
            bad.append("%s is missing" % lid)
            continue
        if c["phrase"] not in l["text"]:
            bad.append("%s no longer says '%s'" % (lid, c["phrase"]))
            continue
        members = doc["speakers"][l["kind"]]["members"]
        for fid, needs in c["facts"].items():
            ft = street_fact_text(fid)
            if ft is None or not all(n in ft for n in needs):
                bad.append("%s: StreetFacts.cs fact %s does not say %s" % (lid, fid, needs))
            for m in members:
                person = TOWN_BY_ID.get(m)
                if person is None or fid not in {f.get("street") for f in person["facts"]}:
                    bad.append("%s: %s does not hold fact %s" % (lid, m, fid))
    emit("claims.kept_lines_held_by_street_facts",
         "the %d lines that say 'heard you ...' claim only what a StreetFacts.cs fact states, held by every named member of their kind (people.json)" % len(KEPT_CLAIMS),
         not bad and len(KEPT_CLAIMS) == 2, "; ".join(bad[:4]))


def kinds_rows(doc, ctx, emit):
    kinds = doc["speakers"]
    members = defaultdict(list)
    for k, v in kinds.items():
        for m in v["members"]:
            members[m].append(k)
    no_kind = doc["no_kind"]
    cast = sorted(set(TOWN_IDS) | set(HK_IDS))
    for pid in cast:
        ks = members.get(pid, [])
        ok = (len(ks) == 1 and pid not in no_kind) or (len(ks) == 0 and pid in no_kind and no_kind[pid])
        emit("kinds.person." + pid, "%s (people.json or hook-cast.json) has exactly one kind, or a stated reason for none" % pid, ok, str(ks))
    extra = [m for m in members if m not in cast]
    emit("kinds.nobody_else", "no kind holds anybody who is not in the cast or the routines", not extra, str(extra))
    emit("kinds.tom_has_none", "Tom is the player and has no kind", "tom" in no_kind and "tom" not in members, "")
    trade_kind = defaultdict(list)
    for k, v in kinds.items():
        for t in v["trades"]:
            trade_kind[t].append(k)
    for t in TRADES:
        emit("kinds.trade." + t.replace(" ", "_"), "Population's trade '%s' maps to exactly one kind" % t, len(trade_kind.get(t, [])) == 1, str(trade_kind.get(t)))
    stray = [t for t in trade_kind if t not in TRADES]
    emit("kinds.trades_are_the_sims", "no kind names a trade the old crowd generator does not", not stray, str(stray))
    own = {k for k, v in kinds.items() if v["own"]}
    emit("kinds.own_are_rulings", "the own kinds are exactly Ron, Darren, Father Walsh and June (RULINGS: street lines own for those four)", own == set(OWN_KINDS)
         and all(kinds[k]["members"] == [OWN_KINDS[k]] for k in OWN_KINDS), str(sorted(own)))
    for pid, nm in KEEP_SHARED.items():
        k = members.get(pid, [None])[0]
        emit("kinds.%s_keeps_shared" % pid, "%s keeps the shared lines (RULINGS): a shared kind, not an own one" % nm, k is not None and not kinds[k]["own"], str(k))
    for k, v in kinds.items():
        if v["voice"] in ("f", "m"):
            bad = [m for m in v["members"] if GENDER.get(m) != v["voice"]]
            emit("kinds.voice." + k, "%s is spoken by %s voices only, and every member is" % (k, "women's" if v["voice"] == "f" else "men's"), not bad, str(bad))
    emit("kinds.no_children", "no kind's description or name speaks of children", not any(CHILD.search(v["what"]) or CHILD.search(k) for k, v in kinds.items()), "")
    emit("kinds.sheila_first_rung", "Sheila is held at the first rung until she trusts him (canon): rules.json says so", RULES_DOC["speaker_overrides"]["lena"]["standing_cap"] == "owner", "")
    # tommy: three kinds only
    tommy_kinds = sorted({l["kind"] for l in doc["lines"] if l["situation"] == "greeting.tommy"})
    # a rung a kind has lines for must be one some member can stand at (canon review L10: thirteen stranger lines of the drivers could never be said)
    RANK = {r: i for i, r in enumerate(RUNGS)}
    so = RULES_DOC["speaker_overrides"]
    floor = {k: so[k]["standing_floor"] for k in ("lena", "rocco", "sam")}
    floor.update({who: so["staff"]["standing_floor"] for who in so["staff"]["speakers"]})
    for k, v in kinds.items():
        if k == "anyone":
            continue
        unreachable = [r for r in v["greeting_rungs"] if not any(RANK[floor.get(m, "stranger")] <= RANK[r] for m in v["members"])]
        emit("kinds.rung_reachable." + k, "every greeting rung %s has lines for is one a member can stand at (floors from rules.json)" % k, not unreachable, str(unreachable))
    emit("kinds.tommy_few", "Tommy is the last rung and canon keeps it for two or three people: lines for it exist in three kinds only", len(tommy_kinds) <= 3 and tommy_kinds == ["father_walsh", "office_worker", "pensioner"], str(tommy_kinds))
    # the approved Mickey lines: carried by no kind in the file (they stay answers to 'What was Mickey like?')
    carried = [l["id"] for l in doc["lines"] if norm(l["text"]) in APPROVED_MICKEY]
    emit("kinds.mickey_lines_not_barks", "the two approved Mickey lines are not ambient lines: they stay answers (RULINGS: the rule for 'What was Mickey like?')", not carried, str(carried))
    emit("kinds.mickey_knowers", "sixteen regulars knew Mickey (unit 11): the list read from people.json", len(KNEW_MICKEY) == 16, str(len(KNEW_MICKEY)))


def places_rows(doc, ctx, emit):
    by_id = {p["id"]: p for p in doc["places"]}
    emit("places.same_set", "lines.json's places are the thirty-four the homes name and the built street has", set(by_id) == set(HOME_PLACES) and len(by_id) == 34, "%d vs %d" % (len(by_id), len(HOME_PLACES)))
    held = [l["id"] for l in doc["lines"] if l["conditions"].get("destination") in HELD_PLACES]
    emit("places.held_have_no_directions", "a place held until Jafar places it (Hal's coin shop) has no directions and is in no line's words",
         not held and not any(re.search(r"\bhal's\b|\bcoin shop\b", l["text"], re.I) for l in doc["lines"]), str(held[:3]))
    per = Counter(l["conditions"].get("destination") for l in doc["lines"] if l["situation"] == "asked_way" and l["kind"] == "anyone")
    named = Counter()
    for l in doc["lines"]:
        d = l["conditions"].get("destination")
        if d and l["kind"] == "anyone":
            forms = name_forms(by_id[d]["names"]) if d in by_id else set()
            if d == "police_station":
                forms.add("station")
            if d == "cafe":
                forms.add("grace's")
            if d == "mickeys":
                forms.update({"cab office", "the rank"})
            if mentions(l["text"], forms):
                named[d] += 1
    for pid, (x, z) in sorted(HOME_PLACES.items()):
        p = by_id.get(pid)
        ok = p is not None and abs(p["x_m"] - x) < 0.01 and abs(p["z_m"] - z) < 0.01 and p["class"] == place_class(pid) and p["far"] == place_far(pid)
        emit("places.where." + pid, "%s is where its home says (x %.1f, z %.1f), its class and distance are right" % (pid, x, z), ok, str(p))
        emit("places.directions." + pid, "%s has at least five lines of directions, and at least two of them name it" % pid, per.get(pid, 0) >= 5 and named.get(pid, 0) >= 2, "%d lines, %d name it" % (per.get(pid, 0), named.get(pid, 0)))
    emit("places.down_up_both", "the places include some down by the water, some up the hill, some on the street, some beyond 200 m",
         {place_class(p) for p in HOME_PLACES} == {"street", "down", "up"} and any(place_far(p) for p in HOME_PLACES), "")


# ------------------------------------------------------------------ rules

def rules_rows(rules, doc, emit):
    cd = rules["cooldowns"]
    clear = float(re.search(r"ClearWordsEverySeconds\s*=\s*([0-9.]+)", SV).group(1))
    emit("rules.neighbours_45", "the neighbours' gap is the ruled 45 s and StreetVoice.ClearWordsEverySeconds", cd["neighbours_talk_min_gap_s"]["value"] == 45 == clear, "%s vs %s" % (cd["neighbours_talk_min_gap_s"]["value"], clear))
    emit("rules.floor_not_below_barkgen", "the same-speaker floor is no shorter than BarkGen's repeat floor in barks.json", cd["per_line"]["same_speaker_same_line_s"]["value"] >= BARKS["repeatFloorSeconds"], str(BARKS["repeatFloorSeconds"]))
    emit("rules.any_speaker_floor", "no two speakers say the same line inside twice Valve's 60 s", cd["per_line"]["any_speaker_same_line_s"]["value"] >= 120, "")
    pr = rules["priority"]["order"]
    emit("rules.priority_all", "every situation has a priority", set(pr) == set(SITUATIONS), str(set(SITUATIONS) ^ set(pr)))
    emit("rules.crime_outranks_greeting", "a crime line outranks a greeting, and the order runs crime, bump, answer, greeting, farewell, rain, after a deed, talk in rain",
         pr["crime_face"] > pr["crime_shape"] > pr["crime_noise"] > pr["bumped"] > pr["asked_way"] > max(pr[s] for s in SITUATIONS if s.startswith("greeting")) > pr["farewell"] > pr["rain_starts"] > pr["after_deed"] > pr["in_rain"], "")
    fam = cd["per_family"]
    emit("rules.families", "every family of moment has a class, a gap and a per-speaker cooldown", set(fam) == {"greet", "bump", "rain_starts", "in_rain", "crime", "after_deed", "way", "farewell"}
         and all({"class", "gap_s", "speaker_s"} <= set(v) for v in fam.values()), "")
    emit("rules.neighbour_class", "only talk among neighbours (in rain, after a deed) is on the 45 s clock", {k for k, v in fam.items() if v["class"] == "neighbour"} == {"in_rain", "after_deed"}, "")
    emit("rules.every_number_has_a_reason", "every number carries a reason and a source", _numbers_have_reasons(rules), "")
    ch = rules["chance"]
    probs = []
    for k in ("stranger", "owner", "nowak", "tom", "tommy"):
        probs.append(ch["greet"][k]["value"])
    probs += [ch["bump"]["value"], ch["farewell"]["value"], ch["rain_starts"]["value"], ch["in_rain"]["value"], ch["after_deed"]["value"], ch["way"]["value"]] + [v["value"] for v in ch["crime"].values()]
    emit("rules.chances_are_chances", "every chance is between 0 and 1, and greeting chances rise with the rung", all(0 <= p <= 1 for p in probs) and probs[0] < probs[1] < probs[2] < probs[3] <= probs[4], str(probs))
    rain = rules["rain"]
    emit("rules.rain_presence_all_kinds", "rain says who is out for every kind in lines.json", set(rain["presence"]["values"]) == {k for k in doc["speakers"] if k != "anyone"}, str(set(doc["speakers"]) ^ set(rain["presence"]["values"])))
    emit("rules.rain_thins", "rain thins the street: nobody is more present in rain than in the dry except the drivers", all(v[2] <= v[0] for k, v in rain["presence"]["values"].items() if k != "driver"), "")
    emit("rules.hear_radius_falls", "the hearing radius is 7 m dry (GossipDirector) and falls in rain", rain["hear_radius_m"]["dry"]["value"] == 7 > rain["hear_radius_m"]["drizzle"]["value"] > rain["hear_radius_m"]["rain"]["value"], "")
    ad = rules["after_deed"]
    emit("rules.after_deed_hour", "witnesses are quieter for an hour (RULINGS 23 Sep): 3600 s, the gap doubled, quieter in level, a shorter carry", ad["hour_s"]["value"] == 3600 and ad["gap_multiplier"]["value"] >= 2 and ad["gain_db"]["value"] < 0 and ad["hear_radius_m"]["value"] < 7, "")
    emit("rules.silence", "the silence rules list when nobody says anything, and never to fill a gap", len(rules["silence"]["nobody_says_anything_when"]) >= 8 and rules["silence"]["never_to_fill_a_gap"] is True, "")
    so = rules["speaker_overrides"]
    emit("rules.never_police_list", "the never-police list is the seven (Ron, Sheila, Rita, Hal, the pawn's back-room hand, the customs officer, the scrap dealer)", set(so["never_police"]["speakers"]) == NEVER_POLICE, str(so["never_police"]["speakers"]))
    emit("rules.not_local_voices", "the three whose voices are not local are Nora and the Tangs (REGULARS.md rows 11, 29, 30)", set(so["not_local_voice"]["speakers"]) == {"vesna", "takeaway_m", "takeaway_f"}, "")
    emit("rules.staff_know_him", "the dispatcher and the two drivers, who work at Mickey's, start at the new owner; Sheila is held there", so["staff"]["standing_floor"] == "owner" and set(so["staff"]["speakers"]) == {"zlata", "ferko", "dusan"} and so["lena"]["standing_floor"] == "owner", "")
    ex = so.get("excluded_lines", {})
    ids_ok = all(any(l["id"] == i and l["kind"] == "office_worker" and l["situation"].startswith("greeting.") for l in doc["lines"]) for i in ex.get("lines", []))
    emit("rules.excluded_lines", "Sheila and the dispatcher are kept from the two office-worker greetings about their own desks ('Do you have a card?', 'Is the radio still crackling?')",
         set(ex.get("speakers", [])) == {"lena", "zlata"} and set(ex.get("lines", [])) == {"office_worker.greet-owner.04", "office_worker.greet-nowak.05"} and ids_ok and bool(ex.get("why")), str(ex))
    emit("rules.ron_darren_start_at_nowak", "Ron and Darren begin at Nowak: they know his name from the start", so["rocco"]["standing_floor"] == "nowak" and so["sam"]["standing_floor"] == "nowak", "")
    emit("rules.minute_cap", "no more than six heard lines in any minute outside a crime, as a rule the picker enforces", cd["lines_per_minute_cap"]["lines"]["value"] == 6 and cd["lines_per_minute_cap"]["window_s"]["value"] == 60, "")
    emit("rules.min_eligible", "six lines must stay after conditions", rules["variety"]["min_eligible"]["value"] == MIN_ELIGIBLE, "")
    emit("rules.trade_kinds", "rules.json maps every trade of the old crowd generator to a kind", set(rules["trade_kinds"]) == set(TRADES), str(set(TRADES) ^ set(rules["trade_kinds"])))
    emit("rules.shelf_lives", "every family has a shelf life (a line not said in time is dropped)", all(k in rules["priority"]["shelf_life_s"] for k in ("crime", "bumped", "greet", "farewell", "rain_starts", "asked_way", "in_rain", "after_deed")), "")


def _numbers_have_reasons(node, path=""):
    ok = True
    if isinstance(node, dict):
        if "value" in node and ("why" not in node or "source" not in node):
            return False
        for k, v in node.items():
            if isinstance(v, (dict, list)):
                ok = ok and _numbers_have_reasons(v, path + "/" + k)
    elif isinstance(node, list):
        for v in node:
            ok = ok and _numbers_have_reasons(v, path)
    return ok


# ------------------------------------------------------------------ the walk rows

def walk_rows(doc, rules, emit, results):
    main = results["main"]
    emit("walk.main.shape", "the main walk is thirty minutes, twenty passers-by, rain from minute 12 to 20, one crime at minute 15, a fixed seed",
         main["minutes"] == 30 and main["passers"] == 20 and main["rain_minutes"] == [12, 20] and main["crime_minute"] == 15.0 and main["seed"] == 1990, "")
    emit("walk.main.no_same_speaker_repeat", "no speaker says the same line twice within 30 minutes", not main["repeats_same_speaker_same_line_within_floor"], str(main["repeats_same_speaker_same_line_within_floor"][:3]))
    emit("walk.main.no_same_line_two_speakers", "no line is said by two speakers within 120 s", not main["repeats_same_line_two_speakers_within_floor"], str(main["repeats_same_line_two_speakers_within_floor"][:3]))
    emit("walk.main.no_same_words_twice", "no words are heard twice in the walk", not main["same_words_heard_twice"], str(main["same_words_heard_twice"][:3]))
    emit("walk.main.neighbours_gap", "neighbour lines are never closer than 45 s", main["neighbour_min_gap_s"] is None or main["neighbour_min_gap_s"] >= 45, str(main["neighbour_min_gap_s"]))
    emit("walk.main.group_gap", "one group never speaks twice inside a minute (crime and answers excepted)", main["group_min_gap_s"] is None or main["group_min_gap_s"] >= 60, str(main["group_min_gap_s"]))
    emit("walk.main.busiest_minute", "no minute holds more than six heard lines outside the crime", main["busiest_minute_without_crime_lines"] <= 6, str(main["busiest_minute_without_crime_lines"]))
    q = rules["silence"]["target_quiet_share"]["value"]
    emit("walk.main.quiet", "at least a third of the minutes pass with no line heard", main["quiet_share"] >= q, str(main["quiet_share"]))
    emit("walk.main.everybody_met", "the walk met people: lines were heard", main["lines_heard"] >= 10, str(main["lines_heard"]))
    emit("walk.main.rain_thins", "the rain thinned the street: fewer passers-by per minute arrive in the rain than outside it",
         main["passers_arriving_in_the_rain_minutes"] / main["rain_minutes_length"] <= main["passers_arriving_otherwise"] / main["other_minutes_length"],
         "%d in %d rain minutes, %d in %d others" % (main["passers_arriving_in_the_rain_minutes"], main["rain_minutes_length"], main["passers_arriving_otherwise"], main["other_minutes_length"]))
    seeds = results["seeds"]
    emit("walk.seeds.no_repeats", "in thirty other seeds of the same walk, no repeat inside a floor and no neighbour line closer than 45 s",
         all(not s["repeats_same_speaker_same_line_within_floor"] and not s["repeats_same_line_two_speakers_within_floor"] and (s["neighbour_min_gap_s"] is None or s["neighbour_min_gap_s"] >= 45) for s in seeds), "")
    emit("walk.seeds.group_gap", "in the thirty seeds, one group never speaks twice inside a minute", all(s["group_min_gap_s"] is None or s["group_min_gap_s"] >= 60 for s in seeds), "")
    heard = Counter()
    for s in seeds:
        heard.update(s["heard_by_situation"])
    missing = [x for x in SITUATIONS if heard.get(x, 0) == 0 and x not in ("greeting.tommy",)]
    emit("walk.seeds.every_situation_heard", "across the thirty seeds every situation is heard at least once (but Tommy, who stands for nobody in the first week)", not missing, str(missing))
    over = [s["seed"] for s in seeds if s["busiest_minute_without_crime_lines"] > 6]
    emit("walk.seeds.busiest_minute", "in the thirty seeds no minute outside a crime holds more than six lines", not over, str(over))
    quiet = [s["seed"] for s in seeds if s["quiet_share"] < q]
    emit("walk.seeds.quiet", "in the thirty seeds at least a third of every walk's minutes are quiet", not quiet, str(quiet))
    shares = sorted(s["quiet_share"] for s in seeds + [main])
    emit("walk.seeds.quiet_median", "in the thirty-one walks the middle one has at least 45 percent of its minutes quiet", shares[len(shares) // 2] >= rules["silence"]["target_quiet_median"]["value"], str(shares[len(shares) // 2]))
    stress = results["stress"]
    emit("walk.stress.no_repeats", "with eighty passers-by in the half hour, still no repeat inside a floor", not stress["repeats_same_speaker_same_line_within_floor"] and not stress["repeats_same_line_two_speakers_within_floor"], "")
    emit("walk.stress.busiest_minute", "with eighty passers-by, no minute holds more than six heard lines outside the crime", stress["busiest_minute_without_crime_lines"] <= 6, str(stress["busiest_minute_without_crime_lines"]))
    emit("walk.stress.neighbours_gap", "with eighty passers-by, neighbour lines are never closer than 45 s", stress["neighbour_min_gap_s"] is None or stress["neighbour_min_gap_s"] >= 45, str(stress["neighbour_min_gap_s"]))
    for lab in ("afternoon", "night"):
        r = results[lab]
        emit("walk.%s.holds" % lab, "the %s walk: lines are heard, no repeat inside a floor, no minute over six outside the crime" % lab,
             r["lines_heard"] >= 5 and not r["repeats_same_speaker_same_line_within_floor"] and not r["repeats_same_line_two_speakers_within_floor"] and r["busiest_minute_without_crime_lines"] <= 6, "heard %d" % r["lines_heard"])
    off = results["unenforced"]
    emit("walk.teeth", "the test has teeth: the same busy walk with the variety and cooldown rules switched off shows repeats and over-close neighbour talk",
         len(off["repeats_same_speaker_same_line_within_floor"]) > 0 and (off["neighbour_min_gap_s"] is not None and off["neighbour_min_gap_s"] < 45 or off["busiest_minute_without_crime_lines"] > 6), "%d same-speaker repeats, neighbour gap %s, busiest %s" % (len(off["repeats_same_speaker_same_line_within_floor"]), off["neighbour_min_gap_s"], off["busiest_minute_without_crime_lines"]))
    for rid, what, ok, detail in results["rule_tests"]:
        emit(rid, what, ok, detail)


def run_walks(doc, rules):
    res = {}
    res["main"] = walk_sim.simulate(doc, rules, seed=1990, label="main")
    res["seeds"] = [walk_sim.simulate(doc, rules, seed=s, label="seed") for s in range(1991, 2021)]
    res["stress"] = walk_sim.simulate(doc, rules, seed=1990, passers=80, label="stress")
    res["afternoon"] = walk_sim.simulate(doc, rules, seed=1990, start_hour=15.0, label="afternoon")
    res["night"] = walk_sim.simulate(doc, rules, seed=1990, start_hour=22.0, label="night")
    res["unenforced"] = walk_sim.simulate(doc, rules, seed=1990, passers=80, label="unenforced", enforce=False)
    res["rule_tests"] = walk_sim.rule_tests(doc, rules)
    return res


# ------------------------------------------------------------------ content rows over the files

def gate_rows(emit):
    files = [str(p.relative_to(REPO)) for p in (HERE / "lines.json", HERE / "rules.json", HERE / "NOTES.md") if p.exists()]
    try:
        r = subprocess.run([sys.executable, str(REPO / "tools" / "canon-gate.py")] + files, cwd=REPO, capture_output=True, text=True, timeout=300)
        tail = ((r.stdout.strip().split("\n") or [""])[-1] + " " + (r.stderr.strip().split("\n") or [""])[-1]).strip()
        emit("content.canon_gate", "tools/canon-gate.py is clean over %s" % ", ".join(files), r.returncode == 0, tail)
    except Exception as e:  # noqa: BLE001
        emit("content.canon_gate", "tools/canon-gate.py is clean over the files", False, str(e))
    notes = HERE / "NOTES.md"
    if notes.exists():
        t = notes.read_text(encoding="utf-8")
        emit("content.notes_no_em_dash_or_italics", "NOTES.md has no em dash and no italics (his rule for what is written for Jafar)",
             "\u2014" not in t and "\u2013" not in t and not re.search(r"(?<![\w*])\*[^*\s][^*\n]*[^*\s]\*(?![\w*])", t) and not re.search(r"(?<![\w_])_[^_\s][^_\n]*[^_\s]_(?![\w_])", t), "")
        hits = CG.scan(t)
        emit("content.notes_gate", "tools/content-gate.py finds nothing in NOTES.md", not hits, str([h[2] for h in hits[:5]]))
    d = (REPO / "DECISIONS.md").read_text(encoding="utf-8").split("\n")
    mine = [l for l in d if "(cloud week 42, unit 12)" in l]
    emit("content.decisions_marked", "every DECISIONS.md entry of this unit ends 'Marked for Jafar.' and has no em dash or italics",
         bool(mine) and all(l.rstrip().endswith("Marked for Jafar.") and "\u2014" not in l and "\u2013" not in l and not re.search(r"(?<![\w*])\*[^*\s][^*\n]*[^*\s]\*(?![\w*])", l) for l in mine), "%d entries" % len(mine))


# ------------------------------------------------------------------ seeded faults

def seeded_faults(doc, rules):
    """Damage a copy thirty-odd ways. Each must make some row fail. Returns [(name, expected row prefix, caught, which)]."""
    out = []

    def lines_of(d, kind, sit):
        return [l for l in d["lines"] if l["kind"] == kind and l["situation"] == sit]

    def trial(name, prefix, mutate, rules_mut=None, walk=False, needle=None):
        d = copy.deepcopy(doc)
        r = copy.deepcopy(rules)
        mutate(d, r)
        got = []
        detail_of = {}

        def emit(rid, what, ok, detail=""):
            if not ok:
                got.append(rid)
                detail_of[rid] = detail
        global RULES_DOC
        saved = RULES_DOC
        RULES_DOC = r
        try:
            doc_rows(d, r, emit)
            rules_rows(r, d, emit)
            if walk:
                res = {"unenforced": None}
                for rid, what, ok, detail in walk_sim.rule_tests(d, r):
                    if not ok:
                        got.append(rid)
                big = walk_sim.simulate(d, r, seed=1990, passers=80, label="stress")
                if big["repeats_same_speaker_same_line_within_floor"] or big["repeats_same_line_two_speakers_within_floor"]:
                    got.append("walk.stress.no_repeats")
                if big["neighbour_min_gap_s"] is not None and big["neighbour_min_gap_s"] < 45:
                    got.append("walk.stress.neighbours_gap")
                if big["busiest_minute_without_crime_lines"] > 6:
                    got.append("walk.stress.busiest_minute")
        finally:
            RULES_DOC = saved
        hit = [g for g in got if g.startswith(prefix)] if prefix else got
        if needle:
            hit = [g for g in hit if needle in detail_of.get(g, "")]      # caught by the check this fault is aimed at, not by another
        out.append((name, prefix, bool(hit), (hit or got)[:2]))

    def put(d, kind, sit, i, text):
        lines_of(d, kind, sit)[i]["text"] = text

    slur = (CG.SLURS or ["x"])[0]
    trial("a line of thirteen words", "line.", lambda d, r: put(d, "shopkeeper", "farewell", 0, "Mind how you go and do come back again when you have more time, dear."))
    trial("alcohol in a line", "line.", lambda d, r: put(d, "dock_worker", "farewell", 0, "Fancy a pint after the shift?"))
    trial("gambling in a line", "line.", lambda d, r: put(d, "casual_worker", "greeting.stranger", 0, "Fancy a gamble on the horses?"))
    trial("a child in a line", "line.", lambda d, r: put(d, "pensioner", "farewell", 0, "Give my love to the kids."))
    trial("a real brand", "line.", lambda d, r: put(d, "shopkeeper", "greeting.stranger", 0, "Cheaper than Woolworths, love."))
    trial("a year after 1992", "line.", lambda d, r: put(d, "driver", "farewell", 0, "See you again in 1995."))
    trial("a real place", "line.", lambda d, r: put(d, "driver", "asked_way", 0, "It's near the station in London."))
    trial("a slur", "line.", lambda d, r: put(d, "driver", "bumped", 0, "Watch it, you %s." % slur))
    trial("a modern word", "line.", lambda d, r: put(d, "tradesman", "farewell", 0, "Text me when it's done."))
    trial("Nowak in a stranger greeting", "line.", lambda d, r: put(d, "shopkeeper", "greeting.stranger", 1, "Morning, Nowak."))
    trial("the new owner in a Tom greeting", "line.", lambda d, r: put(d, "driver", "greeting.tom", 0, "Tom. The new owner needs a cab."))
    trial("Tom in a farewell", "line.", lambda d, r: put(d, "driver", "farewell", 1, "See you on the rank, Tom."))
    trial("an old name (Novak)", "line.", lambda d, r: put(d, "driver", "greeting.nowak", 0, "Novak. All right?"))
    trial("the same retort in two mouths", "cross.", lambda d, r: put(d, "driver", "farewell", 4, "Mind the step on your way out, love."))
    trial("a bump line for strangers in June's mouth (she is never a stranger)", "line.", lambda d, r: lines_of(d, "june", "bumped")[0].update({"conditions": {"standing": ["stranger"]}}))
    trial("a stranger describes Mickey", "line.", lambda d, r: put(d, "dock_worker", "greeting.stranger", 0, "Mickey was a hard man, mate."))
    trial("an approved Mickey line in a dock worker's mouth", "line.", lambda d, r: put(d, "dock_worker", "greeting.stranger", 1, "Mickey kept Ron on when the docks let him go."))
    trial("an address word that is not canon's", "line.", lambda d, r: put(d, "driver", "greeting.tom", 1, "Evening, guv. Where to?"))
    trial("two lines with the same words", "doc.texts_unique", lambda d, r: put(d, "driver", "farewell", 3, lines_of(d, "driver", "farewell")[2]["text"]))
    trial("a line the street already has", "doc.no_second_home", lambda d, r: put(d, "driver", "bumped", 0, "Quiet day. Mostly."))
    trial("an invalid weather value", "line.", lambda d, r: lines_of(d, "driver", "farewell")[0]["conditions"].update({"weather": ["snow"]}))
    trial("an unknown kind", "line.", lambda d, r: lines_of(d, "driver", "farewell")[0].update({"kind": "banker", "speaker": "banker"}))
    trial("a noise line that claims to have seen", "line.", lambda d, r: put(d, "driver", "crime_noise", 0, "I saw it happen, down the road."))
    trial("a shape line that gives a sex", "line.", lambda d, r: put(d, "driver", "crime_shape", 0, "I saw a man running past."))
    trial("a face line that names the culprit", "line.", lambda d, r: put(d, "driver", "crime_face", 0, "I know who it was, I saw."))
    trial("a direction 'down' for a place up the hill", "line.", lambda d, r: [l for l in d["lines"] if l["conditions"].get("destination") == "market_hall"][0].update({"text": "The Market Hall? Down by the water."}))
    trial("'a long walk' for a place at 76 m", "line.", lambda d, r: [l for l in d["lines"] if l["conditions"].get("destination") == "walsh_chapel"][0].update({"text": "The chapel? A long walk up the hill."}))
    trial("a wrong relation (the laundry down past Rita's)", "line.", lambda d, r: [l for l in d["lines"] if l["conditions"].get("destination") == "laundry"][0].update({"text": "The laundry? Down past Rita's."}))
    trial("'east' for a place on the street", "line.", lambda d, r: [l for l in d["lines"] if l["conditions"].get("destination") == "ritas"][0].update({"text": "Rita's? East of the fish shop."}))
    trial("a dialect word flagged plain", "line.", lambda d, r: lines_of(d, "driver", "farewell")[0].update({"text": "Nowt to worry about, mate.", "dialect": "plain"}))
    trial("a gendered word in a shared kind", "line.", lambda d, r: put(d, "driver", "farewell", 2, "My husband drives too."))
    trial("a Ron line that rings the police", "line.", lambda d, r: put(d, "ron", "crime_noise", 0, "Somebody ring the police, boss."))
    trial("after a deed, not hushed", "line.", lambda d, r: lines_of(d, "driver", "after_deed")[0].update({"delivery": "normal"}))
    trial("a cell left with seven lines", "cell.", lambda d, r: d.update({"lines": [l for l in d["lines"] if l["id"] != "driver.farewell.01"]}))
    trial("a group starved by conditions", "pool.", lambda d, r: [l["conditions"].update({"weather": ["rain"]}) for l in lines_of(d, "shopkeeper", "greeting.stranger")[:8]])
    trial("a line for a situation the kind does not have", "cell.", lambda d, r: d["lines"].append(dict(lines_of(d, "ron", "farewell")[0], id="ron.greet-stranger.99", situation="greeting.stranger", bank="greeting/stranger", group="greeting/stranger@ron", rung="stranger", context="greeting", text="Hello there, stranger.", conditions={"standing": ["stranger"]})))
    trial("a stranger greeting for a kind none of whose members can be a stranger to him", "kinds.rung_reachable", lambda d, r: d["speakers"]["driver"]["greeting_rungs"].insert(0, "stranger"))
    trial("what the street thinks of him, in a greeting", "line.", lambda d, r: put(d, "dock_worker", "greeting.nowak", 0, "They tell me you're all right."))
    trial("an invitation to tea in a pensioner's mouth", "line.", lambda d, r: put(d, "pensioner", "greeting.owner", 0, "The new owner. Come to tea one day."))
    trial("a standing claim: the street has been hearing about him", "line.", lambda d, r: put(d, "dock_worker", "greeting.owner", 0, "The new owner. We've all been hearing about you."), needle="standing claim (street talk)")
    trial("a standing claim: they say he has the keys to the lot", "line.", lambda d, r: put(d, "tradesman", "greeting.owner", 0, "The new owner. They say you've the keys to the lot."), needle="standing claim (hearsay)")
    trial("a standing claim: 'heard you' on a line no street fact holds", "line.", lambda d, r: put(d, "night_shift", "greeting.owner", 0, "The new owner. Heard you've a bad back."), needle="standing claim (heard you)")
    trial("a standing claim: what he has done in the town", "line.", lambda d, r: put(d, "tradesman", "greeting.nowak", 0, "Mr Nowak. You've met half the street already."), needle="standing claim (his doings)")
    trial("a standing claim: what was said of his name before", "line.", lambda d, r: put(d, "shopkeeper", "greeting.tom", 0, "Tom. I was just saying your name."), needle="standing claim (his name)")
    trial("a standing claim: an opening nobody set", "line.", lambda d, r: put(d, "driver", "greeting.tom", 0, "Tom. Got a vacancy to fill?"), needle="standing claim (an opening)")
    trial("a standing claim: a window the speaker may not have", "line.", lambda d, r: put(d, "pensioner", "crime_shape", 0, "Somebody ran, past my window. Gone in a flash."), needle="standing claim (a window)")
    trial("a kept 'heard you' line that no longer matches its street fact", "claims.", lambda d, r: put(d, "dock_worker", "greeting.owner", 4, "The new owner. Heard you came with two suitcases."))
    trial("a street name the atlas marks proposal", "doc.no_proposal_street_names", lambda d, r: put(d, "driver", "farewell", 0, "Take Sea Road, love."))
    trial("directions to a place with no unit on the built street (Hal's)", "places.", lambda d, r: d["lines"].append(dict(lines_of(d, "driver", "farewell")[0], id="anyone.way-hals.01", kind="anyone", speaker="anyone", situation="asked_way", bank="way/ask/to/hals", group="way/ask/to/hals@anyone", rung="any", context="way", text="Hal's? Up the top, on the quiet side.", conditions={"destination": "hals"})))
    trial("Sheila given back the line about her own desk", "rules.", lambda d, r: r["speaker_overrides"]["excluded_lines"].update({"speakers": []}))
    trial("Sheila given back the line about her own desk, in the picker", "rule.excluded", lambda d, r: r["speaker_overrides"]["excluded_lines"].update({"speakers": []}), walk=True)
    trial("a place moved", "places.", lambda d, r: [p for p in d["places"] if p["id"] == "ritas"][0].update({"x_m": 30.0}))
    trial("a person left out of every kind", "kinds.", lambda d, r: d["speakers"]["driver"]["members"].remove("ferko"))
    trial("a trade left out", "kinds.", lambda d, r: d["speakers"]["driver"]["trades"].remove("bus driver"))
    trial("Sheila given her own kind", "kinds.", lambda d, r: d["speakers"]["office_worker"]["members"].remove("lena") or d["speakers"]["ron"]["members"].append("lena"))
    trial("the neighbours' gap set to 30 s", "rules.", lambda d, r: r["cooldowns"]["neighbours_talk_min_gap_s"].update({"value": 30}))
    trial("a greeting above a crime in the priorities", "rules.", lambda d, r: r["priority"]["order"].update({"greeting.owner": 99}))
    trial("the never-police list emptied", "rules.", lambda d, r: r["speaker_overrides"]["never_police"].update({"speakers": ["rocco"]}))
    trial("the never-police rule broken in the picker", "rule.", lambda d, r: r["speaker_overrides"]["never_police"].update({"speakers": []}), walk=True)
    trial("the crime-fades-neighbours rule broken (no priority above 90)", "rule.", lambda d, r: r["priority"]["order"].update({"crime_noise": 60, "crime_shape": 60, "crime_face": 60}), walk=True)
    trial("the hush gap multiplier set to 1", "rule.", lambda d, r: r["after_deed"]["gap_multiplier"].update({"value": 1.0}), walk=True)
    trial("the floors set to nothing", "rule.", lambda d, r: (r["cooldowns"]["per_line"]["same_speaker_same_line_s"].update({"value": 0}), r["cooldowns"]["per_line"]["any_speaker_same_line_s"].update({"value": 0}), r["cooldowns"]["neighbours_talk_min_gap_s"].update({"value": 0})), walk=True)
    return out


# ------------------------------------------------------------------ main

RULES_DOC = None


def main():
    global RULES_DOC
    doc = json.loads(LINES.read_text(encoding="utf-8"))
    rules = json.loads(RULES.read_text(encoding="utf-8"))
    RULES_DOC = rules
    doc_rows(doc, rules, row)
    rules_rows(rules, doc, row)
    results = run_walks(doc, rules)
    walk_rows(doc, rules, row, results)
    gate_rows(row)
    WALK_OUT.parent.mkdir(exist_ok=True)
    slim = {k: v for k, v in results.items() if k not in ("seeds", "rule_tests")}
    slim["seeds_summary"] = [{k: s[k] for k in ("seed", "lines_heard", "busiest_minute_without_crime_lines", "busiest_minute_heard", "quiet_share", "longest_gap_s", "neighbour_min_gap_s", "heard_by_situation")} for s in results["seeds"]]
    WALK_OUT.write_text(json.dumps(slim, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    faults = seeded_faults(doc, rules)
    for name, prefix, caught, which in faults:
        row("fault." + re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_"), "seeded fault caught: " + name, caught, "not caught" if not caught else "by " + ", ".join(which))
    kinds = [k for k in doc["speakers"]]
    counts = defaultdict(dict)
    for l in doc["lines"]:
        counts[l["kind"]][l["situation"] if not l["conditions"].get("destination") else "asked_way(directions)"] = counts[l["kind"]].get(l["situation"] if not l["conditions"].get("destination") else "asked_way(directions)", 0) + 1
    n_pass = sum(1 for r in rows if r["pass"])
    caught = sum(1 for f in faults if f[2])
    summary = {"rows": len(rows), "pass": n_pass, "fail": len(rows) - n_pass, "seeded_faults": len(faults), "seeded_faults_caught": caught,
               "kinds": len([k for k in kinds if k != "anyone"]), "situations": len(SITUATIONS), "lines": len(doc["lines"]), "places": len(doc["places"])}
    out = {"made": "13 Oct 2026, cloud week 42, unit 12", "file_checked": "production/cloud-week/lines/lines.json and rules.json", "summary": summary,
           "counts_per_kind_and_situation": {k: dict(sorted(v.items())) for k, v in sorted(counts.items())},
           "walk_main": {k: v for k, v in results["main"].items() if k != "log"}, "rows": rows}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("%d of %d rows pass" % (n_pass, len(rows)))
    print("seeded faults: %d of %d caught" % (caught, len(faults)))
    m = results["main"]
    print("walk (seed %d, %d min, %d passers-by, rain %d to %d, crime at %d): %d lines heard, repeats %d, busiest minute %d, longest gap %d s, %d percent of minutes quiet"
          % (m["seed"], m["minutes"], m["passers"], m["rain_minutes"][0], m["rain_minutes"][1], m["crime_minute"], m["lines_heard"],
             len(m["repeats_same_speaker_same_line_within_floor"]) + len(m["repeats_same_line_two_speakers_within_floor"]) + len(m["same_words_heard_twice"]),
             m["busiest_minute_without_crime_lines"], m["longest_gap_s"], round(100 * m["quiet_share"])))
    sits = SITUATIONS
    print("lines per kind and situation (rows: kinds; columns: " + ", ".join(sits) + ")")
    for k in kinds:
        if k == "anyone":
            continue
        print("  %-14s" % k + " ".join("%3s" % (counts[k].get(s, "-")) for s in sits))
    print("  directions: %d lines for %d places" % (sum(counts["anyone"].values()), len(doc["places"])))
    for r in rows:
        if not r["pass"]:
            print("FAIL", r["id"], "|", r["detail"][:200])
    return 0 if n_pass == len(rows) and caught == len(faults) else 1


if __name__ == "__main__":
    sys.exit(main())
