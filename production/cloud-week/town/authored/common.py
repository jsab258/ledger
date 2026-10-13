"""Shared pieces for the authored files: the street's fact lists, truth bases and the pool of stories
the street passes round. Every quote is found in its home by the builder; none is retyped from memory."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from town_lib import *  # noqa: F401,F403,E402

# --- what the street holds (StreetFacts.cs ids) ---------------------------------
# Everyone who lives or works on the street holds these (StreetFacts.For gives them to every
# talking character). The two Mickey lines are held only by the regulars who knew him (RULINGS 101).
STREET_ALL = ["died_when", "died_heart", "fire", "will", "funeral", "june", "flat", "door", "drivers", "hours", "trade", "cafe", "office",
              "sheila_books", "ron_rank", "darren_rounds"]
MICKEY2 = ["mickey_counsel", "mickey_kept_ron"]
STREET_MIN = ["died_when", "died_heart", "fire", "funeral", "trade", "office"]

# --- truth bases ------------------------------------------------------------------
TB_HEART = H("RUL", "Mickey died of his heart at the office early one morning; Ron found him; nobody thinks otherwise.")
TB_FIRE_STREET = H("FIRE", "The street says the owner had it done for the insurance, his trade being dead since the docks went (the street's talk, not a fact).",
                   note="The paper's 'arson' and 'nobody charged' stand; the owner's guilt is the street's talk, false against the story: the home's lines 48 to 56 say what is true and it is never said here (RULINGS: the truth is never the street's).")
TB_FIRE_PAPER = H("FIRE", "the evening paper called it arson, since it started in two places, and nobody was charged.",
                  note="The paper's word and the silence of the courts are plain street facts and true; nothing of the street's talk about the owner is repeated here.")
TB_WILL = H("SF", "Mickey left the office, Mickey's, the cab office on Quay Street, to his nephew, the new owner, by his will")
TB_FUNERAL = H("SF", "Mickey's funeral was at Father Walsh's chapel, before the new owner came; he missed it.")
TB_JUNE = H("SF", "June, Mickey's daughter, came back to the Hook for the funeral and is still in town; she wants nothing from the office.")
TB_TRADE = H("SF", "Mickey's has not made much money since the docks went; trade has been thin.")
TB_DOOR = H("SF", "it has been locked since he died, and Sheila keeps the key.")
TB_ARRIVE = H("DAY1", "six see him come (Ron, Sheila, the dispatcher, a day driver, Ada, and the sign painter doing the street's boards)")
TB_LANDING = H("ASK", "to the street, a man who hangs about the ferry landing at night")
TB_NEWS = H("NEWS", "**Hal and Rita had words in the pawn, and nobody knows what about.**",
            note="Told as the town sample tells it: only what was seen; nobody can say why.")

# --- limits a rumour keeps (RULINGS and the story), coded ------------------------
LIMITS = {
    "L1": "A witness's story is only as sure as the witness was: a noise or a shape is suspicion, never 'he did it' (RULINGS.md 113).",
    "L2": "The warehouse fire's truth is never the street's: only the paper's arson, nobody charged and the street's insurance talk (RULINGS.md 110).",
    "L3": "Nobody but regulars who knew Mickey describe him, and only in the approved lines (RULINGS.md 101; StreetFacts.cs mickey_counsel, mickey_kept_ron).",
    "L4": "Mickey died of his heart at the office early one morning and Ron found him; nobody thinks otherwise (RULINGS.md 108).",
    "L5": "No reason is given for why the docks went (the outline keeps it underneath, never explained: story-outline 20 to 22).",
    "L6": "Nobody can say what the row at Rita's was about, so nobody invents it (town-news-sample 19 to 21).",
    "L7": "Tom's name follows the ladder: 'the new owner' or Mickey's nephew unless they know it; Sheila, Ron and Darren know it from the start (canon.md 88 to 91; what-they-call-him).",
}

# --- the pool of stories the street passes on --------------------------------------
# Each is a rewording of a fact a person already holds; a person picks the ones that reach them.
POOL = {
    "heart": dict(gist="Mickey died of his heart at the office early one morning; Ron found him when he came on at the rank, and the doctor said it was his heart.",
                  truth="true", basis=TB_HEART, limits=["L4"]),
    "nephew": dict(gist="Mickey's nephew has come to take the office, with one suitcase and a letter that says Mickey left it to him.",
                   truth="true", basis=TB_WILL, limits=["L7"]),
    "funeral": dict(gist="Mickey's nephew missed the funeral, which was at Father Walsh's chapel before he came.",
                    truth="true", basis=TB_FUNERAL, limits=["L7"]),
    "june": dict(gist="June, Mickey's daughter, came back for the funeral, is still in town, and wants nothing from the office.",
                 truth="true", basis=TB_JUNE, limits=[]),
    "fire": dict(gist="The importer's warehouse at the far end of the old warehouse row burned down last November; the paper called it arson, nobody was charged, and the street says the owner had it done for the insurance.",
                 truth="partly", basis=TB_FIRE_STREET, limits=["L2", "L1"]),
    "trade": dict(gist="Mickey's has not made much since the docks went; trade has been thin.",
                  truth="true", basis=TB_TRADE, limits=["L5"]),
    "door": dict(gist="The door at the back of Mickey's is Mickey's own room; it has been locked since he died and Sheila keeps the key.",
                 truth="true", basis=TB_DOOR, limits=[]),
    "landing": dict(gist="There is a man who hangs about the ferry landing at night.",
                    truth="true", basis=TB_LANDING, limits=["L1"]),
    "halrita": dict(gist="Hal and Rita had words in the pawn, and nobody knows what about.",
                    truth="unknown", basis=TB_NEWS, limits=["L6", "L1"]),
    "radio": dict(gist="Whatever goes out on Mickey's radio is heard by every car and half the street.",
                  truth="true", basis=H("CANON", "a radio nobody can help overhearing"), limits=[]),
    "arrive": dict(gist="Saw Mickey's nephew come to Mickey's with his case, the new owner.",
                   truth="true", basis=TB_ARRIVE, limits=["L7"]),
}


def pool(name, frm, to, on, sure, gist=None, limits=None):
    """A story from the pool, as this person would pass it: who it came from, who it would go to,
    the person's own facts it rests on, and how sure the one who first told it was."""
    p = POOL[name]
    return R(gist or p["gist"], p["truth"], p["basis"], sure, frm, to, on, limits if limits is not None else p["limits"])


def rumour(gist, truth, basis, sure, frm, to, on, limits=()):
    return R(gist, truth, basis, sure, frm, to, on, limits)


# --- places the proposals need that hook-cast.json does not have (new, marked) -------------------
T = sys.modules["town_lib"]
T.PROPOSED_PLACES.update({
    "exchange_office": {"said": "his office in the Exchange, the district of offices and lawyers", "district": "the Exchange", "new": "N-SCHEDULES"},
    "exchange_lunch": {"said": "his table at luncheon in the Exchange", "district": "the Exchange", "new": "N-SCHEDULES"},
    "fairview_house": {"said": "his house in Fairview, on the hills", "district": "Fairview", "new": "N-SCHEDULES"},
    "dock_room": {"said": "the back room of a dockside office in the Hook", "district": "the Hook", "new": "N-SCHEDULES"},
    "jensen_house": {"said": "her house by the docks", "district": "the Hook", "new": "N-SCHEDULES"},
    "parade_district": {"said": "the Parade, the nightlife district", "district": "the Parade", "new": "N-SCHEDULES"},
    "danny_flat": {"said": "his flat above a shop in the Parade district", "district": "the Parade", "new": "N-SCHEDULES"},
    "station": {"said": "the police station, in the CID office", "district": "not named in canon", "new": "N-SCHEDULES"},
    "garbutt_room": {"said": "the room he keeps for meetings, over a shop in Copper Row", "district": "Copper Row", "new": "N-SCHEDULES"},
    "takeaway": {"said": "the Tangs' takeaway on the parade (its unit not yet fixed: RULINGS.md has bay 3 empty and to let)", "district": "the Hook", "new": "N-SCHEDULES"},
})


def PS(*a, **k):
    return T.PS(*a, **k)


# --- the thirty regulars: their rows are parsed from REGULARS.md so every name, age and cell is the home's own ---------
REGTAB = {}
for _l in T._lines(T.ALIASES["REG"]):
    if _l.startswith("| ") and _l.count("|") >= 10 and _l.split("|")[1].strip().isdigit():
        _c = [x.strip() for x in _l.strip().strip("|").split("|")]
        REGTAB[_c[1]] = dict(n=_c[0], id=_c[1], name=_c[2], age=int(_c[3]), who=_c[4], look=_c[5], voice=_c[6], manner=_c[7], line=_c[8].strip('"'))
assert len(REGTAB) == 30, len(REGTAB)

# the street's plain answers, in the street's own plain words (StreetFacts.cs "said"), for the people who say them
STD = {
    "died_heart": "His heart, the doctor said. Ron came on at the rank early one morning and found him at the office.",
    "cafe": "The cafe's over the road, in the shops across from the north end of the parade. Half six till ten at night, and eight till twelve on a Sunday.",
    "door": "Mickey's own room, at the back. It's been locked since he died, and Sheila keeps the key.",
    "office": "Mickey's, the minicab office, on Quay Street in the Hook, with the rank outside.",
    "june": "She came back for the funeral and she's still in town. She wants nothing from the office.",
    "funeral": "It was at Father Walsh's chapel, before you came.",
    "flat": "You're in Mickey's flat, over the office.",
    "will": "The office, by his will. The letter you came with says so.",
    "drivers": "Two on the rank, one by day and one by night, and a dispatcher on the radio and the phone.",
    "hours": "Seven in the morning, nine on a Sunday, and on till the night driver goes home at three.",
    "trade": "Not much since the docks went. Trade has been thin.",
    "fire": "The importer's warehouse at the far end of the old warehouse row burned down last November, on a Saturday night. The paper called it arson. Nobody was charged.",
    "mickey": "Mickey kept his business to himself. You'd not hear it from him on the street.",
    "who_runs": "Round the office, Sheila keeps the books and Ron keeps the rank.",
}


def regular(rid, heard_as, *, street=None, knew=False, line_as="knows", line_truth=None, line_basis=None, line_text=None,
            manner=(), knows=(), believes=(), saw=(), rumours, questions, schedule=None, extra=None, note=None):
    r = REGTAB[rid]
    shown = r["name"].split(" (")[0]
    aka = r["name"][r["name"].index("(") + 1:-1] if " (" in r["name"] else None
    line = line_text or r["line"]
    kn, be = [], []
    if line_as == "knows":
        kn.append(K("line", "REG", line, via="the sample line on the contact sheet"))
    else:
        be.append(B("line", "REG", line, line_truth, line_basis))
    for i, frag in enumerate(manner, 1):
        kn.append(K("manner%d" % i, "REG", frag, via="the contact sheet's manner column"))
    ex = dict(extra or {})
    if note:
        ex["note"] = note
    if aka:
        ex["aka"] = aka
    return person(
        rid, shown, heard_as, "regular", r["age"], role=("REG", r["who"]),
        identity=("REG", "%s | %s | %d" % (rid, r["name"], r["age"])),
        street=(STREET_ALL + (MICKEY2 if knew else [])) if street is None else street, knew_mickey=knew,
        knows=kn + list(knows), believes=be + list(believes), saw=list(saw), rumours=rumours, questions=questions,
        schedule=schedule, extra=ex,
        internal_id_note="The id is the routine's own, kept from the old studio (REGULARS.md).")


def QS(q, kind, a, uses, bench=None):
    return Q(q, kind, a, uses, bench)


# --- the same plain fact, said four ways, so that thirty people do not answer in one voice -------------------
# styles: terse (few words), brisk (quick and clipped), warm (talkative), formal (careful and exact).
# {t} is the person's own tag of address (", love", ", mate" or nothing). Every number and name is the fact's own.
VOICES = {
    "died_heart": {
        "terse": "His heart. The doctor said so. Ron found him at the office early one morning, when he came on at the rank.",
        "brisk": "His heart, the doctor said. Ron found him at the office early one morning, when he came on at the rank.",
        "warm": "His heart{t}, the doctor said. Ron came on at the rank early one morning and found him at the office.",
        "formal": "It was his heart, the doctor said. Ron found him at the office early one morning, when he came on at the rank.",
    },
    "cafe": {
        "terse": "The cafe. Over the road, in the shops across from the north end of the parade. Half six till ten; Sundays, eight till twelve.",
        "brisk": "The cafe's over the road, in the shops across from the north end of the parade. Half six till ten at night; Sundays, eight till twelve.",
        "warm": "The cafe's over the road{t}, in the shops across from the north end of the parade. Half six till ten at night; Sundays, eight till twelve.",
        "formal": "There is the cafe, over the road in the shops across from the north end of the parade. Half six till ten at night; Sundays, eight till twelve.",
    },
    "office": {
        "terse": "Mickey's. The minicab office, on Quay Street in the Hook, with the rank outside.",
        "brisk": "Mickey's, the minicab office, on Quay Street in the Hook. The rank's outside.",
        "warm": "That's Mickey's{t}, the minicab office, on Quay Street in the Hook, with the rank outside.",
        "formal": "That is Mickey's, the minicab office, on Quay Street in the Hook, with the rank outside.",
    },
    "door": {
        "terse": "Mickey's own room, at the back. Locked since he died. Sheila keeps the key.",
        "brisk": "Mickey's own room, at the back. It's been locked since he died, and Sheila keeps the key.",
        "warm": "That's Mickey's own room, at the back{t}. It's been locked since he died, and Sheila keeps the key.",
        "formal": "It is Mickey's own room, at the back. It has been locked since he died, and Sheila keeps the key.",
    },
    "june": {
        "terse": "She came back for the funeral. Still in town. Wants nothing from the office.",
        "brisk": "She came back for the funeral and she's still in town. She wants nothing from the office.",
        "warm": "She is{t}. She came back for the funeral and she's still in town, and she wants nothing from the office.",
        "formal": "She is. She came back for the funeral and is still in town. She wants nothing from the office.",
    },
    "funeral": {
        "terse": "At Father Walsh's chapel. Before you came.",
        "brisk": "It was at Father Walsh's chapel, before you came.",
        "warm": "It was at Father Walsh's chapel{t}, before you came.",
        "formal": "The funeral was at Father Walsh's chapel, before you came.",
    },
    "trade": {
        "terse": "Thin. Mickey's has not made much since the docks went.",
        "brisk": "Mickey's hasn't made much since the docks went. Trade's been thin.",
        "warm": "Mickey's hasn't made much since the docks went{t}. Trade's been thin.",
        "formal": "Mickey's has not made much since the docks went. Trade has been thin.",
    },
    "who_runs": {
        "terse": "Sheila keeps the books. Ron keeps the rank.",
        "brisk": "Round the office, Sheila keeps the books and Ron keeps the rank.",
        "warm": "Round the office{t}, Sheila keeps the books and Ron keeps the rank.",
        "formal": "Round the office, Sheila keeps the books and Ron keeps the rank. Past that I could not say.",
    },
    "fire": {
        "terse": "The importer's warehouse, far end of the old warehouse row. Burned down last November, a Saturday night. The paper called it arson. Nobody was charged.",
        "brisk": "The importer's warehouse at the far end of the old warehouse row burned down last November, a Saturday night. The paper called it arson. Nobody was charged.",
        "warm": "The importer's warehouse at the far end of the old warehouse row burned down last November{t}, a Saturday night. The paper called it arson. Nobody was charged.",
        "formal": "The importer's warehouse at the far end of the old warehouse row burned down last November, on a Saturday night. The paper called it arson, and nobody was charged.",
    },
    "drivers": {
        "terse": "Two on the rank, one by day, one by night. A dispatcher on the radio and the phone.",
        "brisk": "Two drivers on the rank, one by day and one by night, and a dispatcher on the radio and the phone.",
        "warm": "Two on the rank{t}, one by day and one by night, and a dispatcher on the radio and the phone.",
        "formal": "There are two drivers on the rank, one by day and one by night, and a dispatcher on the radio and the phone.",
    },
    "hours": {
        "terse": "Seven in the morning, nine on a Sunday. On till the night driver goes home at three.",
        "brisk": "Seven in the morning, nine on a Sunday, and on till the night driver goes home at three.",
        "warm": "It opens at seven{t}, nine on a Sunday, and runs till the night driver goes home at three.",
        "formal": "The office opens at seven in the morning, nine on Sundays, and runs until the night driver goes home at three.",
    },
    "flat": {
        "terse": "You're in Mickey's flat, over the office.",
        "brisk": "You're in Mickey's flat, over the office.",
        "warm": "You're in Mickey's flat{t}, over the office.",
        "formal": "You are in Mickey's flat, over the office.",
    },
    "will": {
        "terse": "The office. By his will. Your letter says so.",
        "brisk": "The office, by his will. The letter you came with says so.",
        "warm": "The office{t}, by his will. The letter you came with says so.",
        "formal": "He left you the office, by his will. The letter you came with says so.",
    },
    "mickey": {s: "Mickey kept his business to himself. You'd not hear it from him on the street." for s in ("terse", "brisk", "warm", "formal")},
    "dk_mickey": {
        "terse": "Didn't know him. That's all I know.",
        "brisk": "I never really knew him. That's all I know.",
        "warm": "I never really knew him{t}. That's all I know.",
        "formal": "I did not know him well. That's all I know.",
    },
}


def std(key, style, tag=""):
    t = (", " + tag) if tag else ""
    return VOICES[key][style].replace("{t}", t)
