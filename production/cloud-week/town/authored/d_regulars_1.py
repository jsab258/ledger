"""Regulars 1 to 6: Pauline Kitching, Kevin Needham, Terry Hodgson, Brenda Laverack, Lee Drewery, Rita Welburn."""
from .common import *  # noqa: F401,F403

PEOPLE = []
PLACES = {}
ARRIVE = ("DAY1", "six see him come (Ron, Sheila, the dispatcher, a day driver, Ada, and the sign painter doing the street's boards)")
ROW = ("NEWS", "Everybody in the pawn then saw it: Rita and Hal themselves, Darren Milner, the pawn's back-room hand, its appraiser, its clerk, and the locksmith who works its counter in the mornings.")

# ---------------------------------------------------------------- 1 Pauline Kitching (zlata)
PEOPLE.append(regular(
    "zlata", "Pauline", knew=True, manner=("quick and dry on the radio, kind off it",),
    knows=[
        K("book_radio", "CANON", "a book of every fare, a radio nobody can help overhearing, a yard with two escapes, a rank outside."),
        D("my_hours", "hours", "mickeys"), D("day", "day"),
    ],
    believes=[
        BN("on_air", "N-LIVES", "Whatever goes out on the radio is heard by every car and half the street; nothing said on it is private.",
           "Canon: 'a radio nobody can help overhearing'.", "true", H("CANON", "a radio nobody can help overhearing")),
    ],
    saw=[W("arrive", *ARRIVE, "day 1, about nine, as the dispatcher, when the new owner came to Mickey's")],
    rumours=[
        pool("heart", ["ferko"], ["joey", "sam"], ["died_heart"], "heard it from the day driver"),
        pool("arrive", ["self"], ["ferko", "joey", "sam"], ["arrive", "will"], "saw it herself from the office"),
        pool("trade", ["self"], ["ferko", "joey"], ["trade"], "knows it from the office's own takings", limits=["L5"]),
        pool("halrita", ["sam"], ["ferko", "joey"], ["fire"], "heard it from Darren on his rounds", limits=["L6", "L1"]),
        pool("fire", ["sam"], ["ferko"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Pauline Kitching. I'm Mickey's dispatcher, on the radio and the phone.", ["job"], "firsts: Who are you?"),
        Q("How do I get a cab?", "partly", "Ring the office or wait on the rank. Car to the station, two minutes. No, love, two real minutes.", ["line", "drivers"], "held: Are we still taking bookings?"),
        Q("How many drivers are there?", "answers", STD["drivers"], ["drivers"], "firsts: How many drivers are there?"),
        Q("What time does the night driver finish?", "answers", "Three. The office runs on till the night driver goes home at three.", ["hours"], "fresh: What time does the night driver finish?"),
        Q("What time do we open in the morning?", "answers", "Seven in the morning, nine on a Sunday.", ["hours"], "held: What time do we open in the morning?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("What's behind that door?", "answers", STD["door"], ["door"], "firsts: What's behind that door?"),
    ],
))

# ---------------------------------------------------------------- 2 Kevin Needham (ferko)
PEOPLE.append(regular(
    "ferko", "Kevin", knew=True, manner=("knows every short cut", "moans about his car"),
    knows=[
        K("syndicate", "EMP", "Joey (dock hand), Ferko (night cab)", secret=True, via="the dockside syndicate's people on the street (empire roster); the sheet makes Kevin the day driver"),
        D("day", "day"),
    ],
    believes=[
        BN("bridge_bad", "N-LIVES", "The bridge is jammed more often than not, and the way round by the market is quicker.",
           "From his line 'Traffic on the bridge again. I went round by the market.'", "unknown", NOTE("A driver's opinion; the story does not settle it.")),
    ],
    saw=[
        W("arrive", *ARRIVE, "day 1, about nine, as a day driver on the rank, when the new owner came to Mickey's"),
        W("bridge_jam", "REG", "Traffic on the bridge again.", "most days, driving"),
    ],
    rumours=[
        pool("heart", ["zlata"], ["joey", "sam"], ["died_heart"], "heard it from the dispatcher"),
        pool("arrive", ["self"], ["zlata", "joey", "sam"], ["arrive", "will"], "saw it himself from the rank"),
        pool("fire", ["sam"], ["zlata", "joey"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        pool("trade", ["self"], ["zlata", "joey"], ["trade"], "knows it from the rank", limits=["L5"]),
        pool("june", ["zlata"], ["joey", "sam"], ["june"], "heard it from the dispatcher"),
    ],
    questions=[
        Q("Who are you?", "answers", "Kevin Needham. I'm the day driver on Mickey's rank.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I drive the day shift on the rank. I know every short cut, and I moan about my car.", ["job", "manner1", "manner2"], "firsts: What do you do here?"),
        Q("How many drivers are there?", "answers", STD["drivers"], ["drivers"], "firsts: How many drivers are there?"),
        Q("Which cars are still on the road?", "answers", "Two on the rank: mine by day and the night driver's.", ["drivers", "job"], "held: Which cars are still on the road?"),
        Q("What's the traffic like?", "answers", "Traffic on the bridge again. I went round by the market.", ["line"], "invented: a driver's likely small talk"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
    ],
))

# ---------------------------------------------------------------- 3 Terry Hodgson (dusan)
PEOPLE.append(regular(
    "dusan", "Terry", knew=True, manner=("few words, all nights, keeps himself to himself",),
    knows=[D("day", "day")],
    believes=[
        BN("nights_thin", "N-LIVES", "Nights on the rank are thin, and the fares that come are few.",
           "Follows the street fact that trade has been thin since the docks went.", "unknown", H("SF", "Mickey's has not made much money since the docks went; trade has been thin.")),
    ],
    saw=[
        WN("night_street", "N-LIVES", "He sees who comes and goes on the street after dark, from the rank, and says little of it.",
           "His routine puts him on the rank all night (hook-cast.json) and his manner is few words.", "every night, before the game"),
    ],
    rumours=[
        pool("heart", ["rocco"], ["sam", "rocco"], ["died_heart"], "heard it from Ron, who found him"),
        pool("fire", ["street"], ["sam"], ["fire"], "street talk", limits=["L2", "L1"]),
        pool("trade", ["self"], ["rocco", "sam"], ["trade"], "knows it from the night rank", limits=["L5"]),
        pool("june", ["rocco"], ["sam"], ["june"], "heard it from Ron"),
        pool("arrive", ["rocco"], ["sam", "rocco"], ["will"], "heard it from Ron, who saw it", limits=["L7"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Terry Hodgson. The night driver.", ["job"], "firsts: Who are you?"),
        Q("Where to?", "answers", "Now then. Where to?", ["line"], "invented: a fare's first words"),
        Q("What time do you finish?", "answers", "Three. The office runs on till the night driver goes home at three.", ["hours"], "fresh: What time does the night driver finish?"),
        Q("How busy does the rank get at night?", "answers", "Not very. Trade has been thin since the docks went.", ["trade"], "fresh: How busy does the rank get at night?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("What's the street like after dark?", "dont_know", "Quiet. That's all I know.", [], "held: What's the street like after dark?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What's behind that door?", "answers", STD["door"], ["door"], "firsts: What's behind that door?"),
        Q("Is June still about?", "answers", STD["june"], ["june"], "fresh: Is June still about?"),
    ],
))

# ---------------------------------------------------------------- 4 Brenda Laverack (marla)
PEOPLE.append(regular(
    "marla", "Brenda", knew=True, line_as="believes", line_truth="unknown",
    line_basis=NOTE("A shopkeeper's opinion of this week's fish; nothing in canon or the story settles it."),
    manner=("knows the price of everything",),
    knows=[D("my_hours", "hours", "fish_market"), D("day", "day")],
    believes=[],
    saw=[W("dawn_dock", "REG", "buys on the fish dock at dawn", "every dawn, on the fish dock")],
    rumours=[
        pool("heart", ["ada"], ["ada", "vesna"], ["died_heart"], "heard it from Ada, who watches the street"),
        pool("arrive", ["ada"], ["ada", "noor"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("fire", ["vesna"], ["ada", "noor"], ["fire"], "street talk, by way of Father Walsh's housekeeper", limits=["L2", "L1"]),
        pool("june", ["noor"], ["ada", "vesna"], ["june"], "heard it from the reporter"),
        pool("trade", ["self"], ["ada", "sam"], ["trade"], "knows it from the shop's own counter", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Brenda Laverack. I've the fish shop, and I buy on the fish dock at dawn.", ["job"], "firsts: Who are you?"),
        Q("What's the fish like today?", "answers", "Haddock's dear this week and it's not even good haddock.", ["line"], "invented: a stranger at a fish counter"),
        Q("What time do you open?", "answers", "Half seven, till two. Wednesdays I shut at one.", ["my_hours"], "held: What time do we open in the morning?"),
        Q("Where do you buy your fish?", "answers", "On the fish dock, at dawn.", ["job"], "invented: a stranger at a fish counter"),
        Q("What's the price of that?", "answers", "I know the price of everything, love. Ask me and I'll tell you.", ["manner1"], "invented: a stranger at a fish counter"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("What is this place?", "answers", "That's Mickey's, next door. The minicab office, on Quay Street in the Hook, with the rank outside.", ["office"], "firsts: What is this place?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
    ],
))

# ---------------------------------------------------------------- 5 Lee Drewery (joey)
PEOPLE.append(regular(
    "joey", "Lee", knew=False, line_as="believes", line_truth="true", line_basis=TB_TRADE, manner=("careful with Ron",),
    knows=[
        K("syndicate", "EMP", "Joey (dock hand), Ferko (night cab)", secret=True, via="the dockside syndicate's people on the street (empire roster)"),
        D("day", "day"),
    ],
    believes=[],
    saw=[W("casual_quay", "REG", "takes casual days on the quay when there are any", "most weeks, on the quay")],
    rumours=[
        pool("heart", ["rocco"], ["ferko", "zlata", "rocco"], ["died_heart"], "heard it from Ron, who found him"),
        pool("arrive", ["rocco"], ["ferko", "zlata", "sam"], ["will"], "heard it from Ron, who saw it", limits=["L7"]),
        pool("fire", ["sam"], ["ferko", "rocco"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        pool("trade", ["self"], ["rocco", "ferko", "zlata"], ["trade"], "knows it from the quay", limits=["L5"]),
        pool("june", ["rocco"], ["zlata", "sam"], ["june"], "heard it from Ron"),
    ],
    questions=[
        Q("Who are you?", "answers", "Lee Drewery. Casual days on the quay, when there are any.", ["job"], "firsts: Who are you?"),
        Q("Is there any work going?", "answers", "Casual again. If they want me. They mostly don't.", ["line"], "invented: a stranger asks a man on the quay"),
        Q("What do you do here?", "answers", "I take casual days on the quay when there are any.", ["job"], "firsts: What do you do here?"),
        Q("Who's the big man on the rank?", "answers", "Ron Kirby. He keeps Mickey's door and the rank. I'm careful with Ron.", ["who_rocco", "manner1"], "held: Who's the lad hanging about by the rank?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "Never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 6 Rita Welburn (rita)
PEOPLE.append(regular(
    "rita", "Rita", knew=True, manner=("never says what a thing is worth until she has to",),
    knows=[
        K("fence", "EMP", "Rita (the back-room fence)", secret=True, via="the new crew's person on the street (empire roster, faction table)"),
        K("never_police", "ELLIS", "Not Rita: the empire roster makes her the new crew's fence, and a fence does not ask the police into her shop, so her own window goes unreported.", secret=True),
        K("row", "NEWS", "Hal and Rita had words in the pawn, and nobody knows what about.", via="day 1, Monday at eleven, in her own pawn: the town's sample story"),
        D("my_hours", "hours", "ritas"), D("day", "day"),
    ],
    believes=[
        BN("across_counter", "N-LIVES", "What people bring over her counter is their business, and what she is told stays on her side of it.",
           "From 'looking costs you nothing' and 'never says what a thing is worth until she has to'.", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[W("row_seen", *ROW, "day 1, Monday at eleven, in her own pawn")],
    rumours=[
        pool("halrita", ["self"], ["victor"], ["row", "row_seen"], "saw it herself; she and Hal keep it to themselves", limits=["L6", "L1"]),
        pool("heart", ["joey"], ["victor", "joey"], ["died_heart"], "heard it from the dock hand on her step"),
        pool("arrive", ["joey"], ["victor", "tibor"], ["will"], "heard it on her step in the evening", limits=["L7"]),
        pool("fire", ["street"], ["victor", "joey"], ["fire"], "street talk", limits=["L2", "L1"]),
        pool("trade", ["self"], ["victor", "tibor"], ["trade"], "she sees what comes over the counter", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Rita Welburn. I keep the pawn.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I'll look at it. Looking costs you nothing.", ["line"], "firsts: What do you do here?"),
        Q("What time do you open?", "answers", "Nine till half past five, except Wednesdays, when it's nine till one.", ["my_hours"], "held: What time do we open in the morning?"),
        Q("What's it worth?", "deflect", "I never say what a thing is worth until I have to. Let me look at it.", ["manner1", "line"], "invented: a stranger at a pawn counter"),
        Q("What happened between you and Hal?", "deflect", "That's between Hal and me.", ["row"], "invented: the town's own news"),
        Q("Who's Hal?", "answers", "Hal keeps the coin shop that sells no coins.", ["who_hal"], "invented: a stranger asks about a neighbour"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Is there any money in the business?", "answers", STD["trade"], ["trade"], "firsts: Is there any money in the business?"),
        Q("What's behind that door?", "answers", STD["door"], ["door"], "firsts: What's behind that door?"),
    ],
))
