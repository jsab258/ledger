"""Regulars 7 to 12: Wayne Harrison, Hal Metcalfe, Susan Coverdale, Nora Cronin, Winifred Duggleby, Doreen Harland."""
from .common import *  # noqa: F401,F403

PEOPLE = []
PLACES = {}
ROW = ("NEWS", "Everybody in the pawn then saw it: Rita and Hal themselves, Darren Milner, the pawn's back-room hand, its appraiser, its clerk, and the locksmith who works its counter in the mornings.")
NEVER = ("ELLIS", "**Some never go at all**, whatever they see or suffer, because their trade keeps them from it: Rita, the customs officer (the machine's stamp, the roster says), Hal, the pawn's back-room hand, the scrap dealer, and the outfit's man.")

# ---------------------------------------------------------------- 7 Wayne Harrison (victor)
PEOPLE.append(regular(
    "victor", "Wayne", knew=False, line_as="believes", line_truth="unknown",
    line_basis=NOTE("His own account of his job; the story says only that he is the pawn's back-room hand."),
    manner=("always carrying something",),
    knows=[
        K("never_police", *NEVER, secret=True, via="his trade keeps him from the police (the Ellis design)"),
        K("row", "NEWS", "Hal and Rita had words in the pawn, and nobody knows what about.", via="day 1, Monday at eleven: the town's sample story; he was there"),
        D("my_hours", "hours", "ritas"), D("day", "day"),
    ],
    believes=[],
    saw=[W("row_seen", *ROW, "day 1, Monday at eleven, in the pawn, from the back room")],
    rumours=[
        pool("halrita", ["self"], ["lena", "sam"], ["row", "row_seen"], "saw it himself, from the back room", limits=["L6", "L1"]),
        pool("heart", ["lena"], ["sam", "rita"], ["died_heart"], "heard it from Sheila on Rita's step"),
        pool("arrive", ["lena"], ["sam", "rita"], ["will"], "heard it from Sheila on Rita's step", limits=["L7"]),
        pool("fire", ["sam"], ["rita", "lena"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        pool("trade", ["self"], ["rita", "sam"], ["trade"], "sees what comes over the counter", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Wayne Harrison. I work the pawn's back room.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "deflect", "Don't ask me, I just shift the boxes.", ["line"], "firsts: What do you do here?"),
        Q("What's in the boxes?", "deflect", "Don't ask me, I just shift the boxes.", ["line"], "invented: a stranger at a pawn's back door"),
        Q("What time does the shop open?", "answers", "Nine till half past five, except Wednesdays, when it's nine till one.", ["my_hours"], "held: What time do we open in the morning?"),
        Q("Who's Rita?", "answers", "Rita keeps the pawn shop.", ["who_rita"], "invented: a stranger asks about the keeper"),
        Q("What happened between Hal and Rita?", "partly", "They had words in the pawn, and nobody knows what about.", ["row", "row_seen"], "invented: the town's own news"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("What was Mickey like?", "dont_know", "Never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 8 Hal Metcalfe (hal)
PEOPLE.append(regular(
    "hal", "Hal", knew=True, line_as="believes", line_truth="unknown",
    line_basis=NOTE("His own account of why he keeps the shop; canon says only that it sells no coins and why is not settled."),
    manner=("remembers everyone's business",),
    knows=[
        K("never_police", *NEVER, secret=True, via="his trade keeps him from the police (the Ellis design)"),
        K("row", "NEWS", "Hal and Rita had words in the pawn, and nobody knows what about.", via="day 1, Monday at eleven, in the pawn: the town's sample story; he was a party to it"),
        D("my_hours", "hours", "hals"), D("day", "day"),
    ],
    believes=[],
    saw=[
        W("row_seen", *ROW, "day 1, Monday at eleven, in Rita's pawn"),
        W("mondays", "REG", "calls on Rita's on Mondays", "every Monday at eleven, at Rita's"),
    ],
    rumours=[
        pool("halrita", ["self"], ["sam", "rita"], ["row", "row_seen"], "saw it himself; he and Rita keep it to themselves", limits=["L6", "L1"]),
        pool("heart", ["sam"], ["sam", "rita"], ["died_heart"], "heard it from Darren"),
        pool("arrive", ["sam"], ["rita"], ["will"], "heard it from Darren", limits=["L7"]),
        pool("fire", ["sam"], ["rita"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        pool("june", ["sam"], ["rita"], ["june"], "heard it from Darren"),
    ],
    questions=[
        Q("Who are you?", "answers", "Hal Metcalfe. I keep the coin shop that sells no coins.", ["job"], "firsts: Who are you?"),
        Q("What do you sell?", "answers", "Coins? Now and then. It's the company I keep the shop for.", ["line"], "invented: a stranger at a coin shop"),
        Q("What time do you open?", "answers", "Ten till six, Wednesdays ten till one.", ["my_hours"], "held: What time do we open in the morning?"),
        Q("Why do you call on Rita's?", "answers", "I call on Rita's on Mondays.", ["job"], "invented: a stranger asks about a neighbour"),
        Q("What happened between you and Rita?", "deflect", "Not for me to say, I'm afraid.", ["row"], "invented: the town's own news"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Who was Mickey closest to?", "dont_know", "I wouldn't like to say. That's all I know.", [], "fresh: Who was Mickey closest to?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is there any money in the business?", "answers", STD["trade"], ["trade"], "firsts: Is there any money in the business?"),
    ],
))

# ---------------------------------------------------------------- 9 Susan Coverdale (tibor)
PEOPLE.append(regular(
    "tibor", "Susan", knew=False, line_as="believes", line_truth="true", line_basis=TB_TRADE, manner=("off duty never quite off duty",),
    knows=[
        K("stamp", "EMP", "Tibor (the customs stamp)", secret=True, via="the old-money machine's person on the street (empire roster, faction table)"),
        K("never_police", *NEVER, secret=True, via="her trade keeps her from the police (the Ellis design)"),
        D("day", "day"),
    ],
    believes=[],
    saw=[W("quiet_quay", "REG", "I've never known the quay this quiet.", "every working day, on the quay")],
    rumours=[
        pool("heart", ["joey"], ["rita", "joey"], ["died_heart"], "heard it from the dock hand on Rita's step"),
        pool("arrive", ["joey"], ["rita"], ["will"], "heard it on Rita's step in the evening", limits=["L7"]),
        pool("fire", ["street"], ["rita", "joey"], ["fire"], "street talk", limits=["L2", "L1"]),
        pool("trade", ["self"], ["joey", "rita"], ["trade", "line"], "sees the quay herself", limits=["L5"]),
        pool("june", ["rita"], ["joey"], ["june"], "heard it from Rita"),
    ],
    questions=[
        Q("Who are you?", "answers", "Susan Coverdale. I'm a customs officer, and I live past Rita's.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I'm a customs officer, on the quay.", ["job"], "firsts: What do you do here?"),
        Q("What's the quay like?", "answers", "I've never known the quay this quiet. Not in all my time.", ["line"], "invented: a stranger asks a customs officer"),
        Q("Is it always this quiet?", "answers", "Not in all my time. Trade has been thin since the docks went.", ["line", "trade"], "held: Is it always this quiet?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I didn't know him. That's all I know.", [], "firsts: What was Mickey like?"),
        Q("What happened at the warehouse fire?", "answers", STD["fire"], ["fire"], "fresh: What happened at the warehouse fire?"),
    ],
))

# ---------------------------------------------------------------- 10 Nora Cronin (vesna)
PEOPLE.append(regular(
    "vesna", "Nora", knew=True, manner=("protective of the priest",),
    knows=[D("day", "day")],
    believes=[
        BN("not_troubled", "N-LIVES", "Father Walsh is not to be troubled by every caller.",
           "From the contact sheet's 'devout, dry, a quick laugh, protective of the priest'.", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[W("buys", "REG", "buys for his table", "most days, at the fish counter and the market")],
    rumours=[
        pool("heart", ["emil"], ["emil", "ada"], ["died_heart"], "heard it from Father Walsh"),
        pool("funeral", ["emil"], ["ada", "marla"], ["funeral"], "heard it from Father Walsh, who took the service"),
        pool("june", ["emil"], ["ada", "marla"], ["june"], "heard it from Father Walsh, who sees her at the chapel"),
        pool("arrive", ["ada"], ["emil", "marla"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("fire", ["marla"], ["ada"], ["fire"], "street talk, by way of the fish shop", limits=["L2", "L1"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Nora Cronin. I keep Father Walsh's house and buy for his table.", ["job"], "firsts: Who are you?"),
        Q("How long have you been here?", "answers", "I came over in fifty-one for a year. That was a long year.", ["line"], "held: How long have you been here?"),
        Q("Who's the priest round here?", "answers", "Father Walsh, who says mass and calls on the old.", ["who_emil"], "fresh: Who's the priest round here?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("Sorry I missed the funeral.", "answers", STD["funeral"], ["funeral"], "firsts: Sorry I missed the funeral."),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Is June still about?", "answers", STD["june"], ["june"], "fresh: Is June still about?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("What's behind that door?", "answers", STD["door"], ["door"], "firsts: What's behind that door?"),
        Q("Did Mickey have any enemies?", "dont_know", "I couldn't say. That's all I know.", [], "fresh: Did Mickey have any enemies?"),
    ],
))

# ---------------------------------------------------------------- 11 Winifred Duggleby (magda)
PEOPLE.append(regular(
    "magda", "Winifred", knew=True, line_as="believes", line_truth="unknown",
    line_basis=NOTE("An old woman's remark about what is brought to the chapel; nothing in canon settles it."),
    manner=("talks to the flowers",),
    knows=[D("day", "day")],
    believes=[],
    saw=[W("chapel_flowers", "REG", "cleans the chapel and does its flowers", "most mornings, at the chapel")],
    rumours=[
        pool("heart", ["ada"], ["ada"], ["died_heart"], "heard it from Ada, who watches the street"),
        pool("funeral", ["ada"], ["ada"], ["funeral"], "heard it at the chapel, and from Ada"),
        pool("june", ["ada"], ["ada"], ["june"], "heard it from Ada"),
        pool("arrive", ["ada"], ["ada"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("door", ["ada"], ["ada"], ["door"], "heard it from Ada, who had it from Sheila", limits=[]),
    ],
    questions=[
        Q("Who are you?", "answers", "Winifred Duggleby. I clean the chapel and do its flowers.", ["job"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "I clean the chapel and do the flowers. I talk to them, I'm told.", ["job", "manner1"], "firsts: What do you do here?"),
        Q("What are the flowers?", "answers", "Chrysanthemums again. Nobody gives lilies any more.", ["line"], "invented: a stranger at the chapel"),
        Q("Who's the priest round here?", "partly", "Father Walsh. Mickey's funeral was at his chapel.", ["funeral"], "fresh: Who's the priest round here?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("Sorry I missed the funeral.", "answers", STD["funeral"], ["funeral"], "firsts: Sorry I missed the funeral."),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Is June still about?", "answers", STD["june"], ["june"], "fresh: Is June still about?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
    ],
))

# ---------------------------------------------------------------- 12 Doreen Harland (zora)
PEOPLE.append(regular(
    "zora", "Doreen", knew=True, line_text="They'll carry me out of that laundry.", manner=("blunt",),
    knows=[
        K("layoff_known", "REG", "laid off from the steam laundry's presses in the summer, looking for anything", via="a colleague's row on the contact sheet"),
        D("my_hours", "hours", "laundry"), D("day", "day"),
    ],
    believes=[],
    saw=[W("early_shift", "REG", "still on the early shift", "every working day, from six")],
    rumours=[
        pool("heart", ["ada"], ["ada", "noor"], ["died_heart"], "heard it from Ada"),
        pool("arrive", ["ada"], ["ada", "noor"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("fire", ["noor"], ["ada", "lena"], ["fire"], "the paper's word, by way of the reporter", limits=["L2", "L1"]),
        pool("june", ["ada"], ["noor", "lena"], ["june"], "heard it from Ada"),
        rumour("A laundress at the steam laundry, laid off from the presses in the summer, is looking for anything.", "true", H("REG", "laid off from the steam laundry's presses in the summer, looking for anything"),
               "knows it first hand: she works there", ["self"], ["ada", "noor"], ["layoff_known"], []),
    ],
    questions=[
        Q("Who are you?", "answers", "Doreen Harland. I'm a washerwoman at the steam laundry, on the early shift.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I wash at the steam laundry, and I won't retire. Still on the early shift.", ["job"], "firsts: What do you do here?"),
        Q("What time does the laundry open?", "answers", "Eight till half past five, Monday to Saturday.", ["my_hours"], "held: What time do we open in the morning?"),
        Q("Why don't you retire?", "answers", "They'll carry me out of that laundry.", ["line"], "invented: a stranger asks an old hand"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("What's behind that door?", "answers", STD["door"], ["door"], "firsts: What's behind that door?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
    ],
))
