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
