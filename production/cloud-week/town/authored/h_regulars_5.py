"""Regulars 25 to 30: Dawn Pybus, Dennis Iveson, Norman Dent, Grace Rinaldi, Peter Tang, Lily Tang."""
from .common import *  # noqa: F401,F403

PEOPLE = []
PLACES = {}
NEVER = ("ELLIS", "**Some never go at all**, whatever they see or suffer, because their trade keeps them from it: Rita, the customs officer (the machine's stamp, the roster says), Hal, the pawn's back-room hand, the scrap dealer, and the outfit's man.")
AWAY = ("FIRE", "He had slipped off home, and he swore in his report that he had done his rounds.")
WHY_NEW = "No routine for this person in hook-cast.json (REGULARS.md: 'Grace and the Tangs need theirs'); proposed from the contact sheet and the shop hours."

# ---------------------------------------------------------------- 25 Dawn Pybus (danica)
PEOPLE.append(regular(
    "danica", "Dawn", knew=False, line_as="believes", line_truth="unknown",
    line_basis=NOTE("A collector's remark; whose fault the rent is is not settled by canon."), manner=("hates the job",),
    knows=[D("day", "day")],
    believes=[],
    saw=[W("rounds", "REG", "runs for the rent collector", "every week, on her rounds")],
    rumours=[
        pool("heart", ["sam"], ["sam", "lena"], ["died_heart"], "heard it from Darren"),
        pool("arrive", ["lena"], ["sam", "franjo"], ["will"], "heard it from Sheila at the office on a Friday", limits=["L7"]),
        pool("fire", ["sam"], ["lena"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        pool("june", ["lena"], ["sam", "franjo"], ["june"], "heard it from Sheila"),
        pool("trade", ["self"], ["sam", "lena"], ["trade"], "sees who is behind on the rent", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Dawn Pybus. I run for the rent collector.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I run for the rent collector. I hate the job, to be honest.", ["job", "manner1"], "firsts: What do you do here?"),
        Q("Who do I pay the rent to?", "partly", "I only collect it. Shout at the landlord, not me.", ["line"], "invented: a stranger asks a collector"),
        Q("Who's Sheila?", "answers", "Sheila Dunn, Mickey's bookkeeper.", ["who_lena"], "invented: a stranger asks about a neighbour"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 26 Dennis Iveson (drago)
PEOPLE.append(regular(
    "drago", "Dennis", knew=False, manner=("buys anything",),
    knows=[
        K("fittings", "FIRE", "A scrap dealer bought fittings stripped from the burned building.", secret=True, via="the town's own fact about the scrap dealer; when he stripped them is left open by the fire design"),
        K("never_police", *NEVER, secret=True, via="his trade keeps him from the police (the Ellis design)"),
        D("day", "day"),
    ],
    believes=[
        B("owner_did", "SF", "the street says the owner had it done for the insurance", "false", TB_FIRE_STREET),
    ],
    saw=[
        WN("burned_end", "N-LIVES", "He works on the old warehouse row and has seen the burned end of it every day since November.",
           "His yard is on the row (contact sheet) and the fire was at its far end (street fact).", "every working day since the fire"),
    ],
    rumours=[
        pool("fire", ["self"], ["sam", "rocco"], ["fire", "owner_did", "burned_end"], "the paper's word and street talk; he sees the burned end himself", limits=["L2", "L1"]),
        pool("heart", ["rocco"], ["sam"], ["died_heart"], "heard it from Ron at the cafe"),
        pool("arrive", ["rocco"], ["sam"], ["will"], "heard it from Ron at the cafe", limits=["L7"]),
        pool("june", ["rocco"], ["sam"], ["june"], "heard it from Ron"),
        pool("trade", ["self"], ["sam", "rocco"], ["trade"], "sees how little scrap comes in", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Dennis Iveson. I'm a scrap dealer on the old warehouse row.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I deal in scrap on the old warehouse row. I buy anything.", ["job", "manner1"], "firsts: What do you do here?"),
        Q("What do you buy?", "answers", "Copper, lead, brass. I'll weigh it and I'll pay you. Fair's fair.", ["line"], "invented: a stranger asks a scrap dealer"),
        Q("What happened at the warehouse fire?", "answers", STD["fire"], ["fire"], "fresh: What happened at the warehouse fire?"),
        Q("Did you buy anything from the fire?", "deflect", "I buy anything, me. Copper, lead, brass, I'll weigh it and I'll pay you.", ["fittings", "manner1", "line"], "invented: a stranger asks a scrap dealer"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 27 Norman Dent (filip)
PEOPLE.append(regular(
    "filip", "Norman", knew=False, line_as="believes", line_truth="partly", line_basis=H(*AWAY, note="True on the nights he is there; the story has him away the night of the fire."),
    manner=("glad of company", "swears he misses nothing"),
    knows=[
        K("walks_row", "FIRE", "The watchman walks the whole row for the warehouses still standing."),
        K("slipped", "FIRE", "His secret is that he slipped off home on his break the night of the fire and lied in his report, and Darren knows it.", secret=True, via="the approved fire design"),
        D("day", "day"),
    ],
    believes=[],
    saw=[W("away", *AWAY, "the night of the fire, last November", secret=True)],
    rumours=[
        rumour("Nothing moves on the old warehouse row at night but the watchman and the rats.", "partly", H(*AWAY, note="True on the nights he is there; the story has him away the night of the fire."),
               "his own word, and he was away the night of the fire", ["self"], ["sam"], ["line", "walks_row"], ["L1", "L2"]),
        pool("fire", ["street"], ["sam"], ["fire"], "the paper's word; he says nothing of his own night", limits=["L2", "L1"]),
        pool("heart", ["sam"], ["sam"], ["died_heart"], "heard it from Darren"),
        pool("arrive", ["sam"], ["sam"], ["will"], "heard it from Darren", limits=["L7"]),
        pool("june", ["sam"], ["sam"], ["june"], "heard it from Darren"),
    ],
    questions=[
        Q("Who are you?", "answers", "Norman Dent. I'm the night watchman on the warehouse row.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I walk the whole row at night, for the warehouses still standing.", ["job", "walks_row"], "firsts: What do you do here?"),
        Q("What's it like at night?", "answers", "Nothing moves on that row at night but me and the rats.", ["line"], "held: What's the street like after dark?"),
        Q("Were you there the night of the fire?", "deflect", "I swear I miss nothing on that row.", ["manner2", "slipped"], "invented: a stranger asks the watchman"),
        Q("What happened at the warehouse fire?", "answers", STD["fire"], ["fire"], "fresh: What happened at the warehouse fire?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 28 Grace Rinaldi (cafe)
PEOPLE.append(regular(
    "cafe", "Grace", knew=True, manner=("fierce about her tea", "forgets nobody"),
    knows=[D("my_hours", "hours", "cafe")],
    believes=[
        BN("tea_sets_right", "N-LIVES", "A cup of tea sets most people right, and nobody leaves her caff hungry or cold.",
           "From her line 'Sit down before you fall down. Tea's on.' and 'warm, bossy'.", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[W("keeps_caff", "REG", "keeps the caff, her Italian father's before her", "every day, behind her counter")],
    rumours=[
        pool("heart", ["rocco"], ["rocco", "franjo"], ["died_heart"], "heard it from Ron, who has his tea at the cafe"),
        pool("arrive", ["rocco"], ["rocco", "franjo"], ["will"], "heard it from Ron at the cafe", limits=["L7"]),
        pool("fire", ["drago"], ["rocco", "luka"], ["fire"], "street talk at the counter", limits=["L2", "L1"]),
        pool("june", ["rocco"], ["franjo", "luka"], ["june"], "heard it from Ron at the cafe"),
        pool("trade", ["self"], ["rocco", "tomas"], ["trade"], "sees the custom at the counter", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Grace Rinaldi. I keep the caff, my Italian father's before me.", ["job"], "firsts: Who are you?"),
        Q("What have you got?", "answers", "Sit down before you fall down. Tea's on.", ["line"], "invented: a stranger walks into a caff"),
        Q("What time do you open?", "answers", "Half six till ten at night, Monday to Saturday. Eight till twelve on a Sunday.", ["my_hours"], "held: What time do we open in the morning?"),
        Q("Where can I get something to eat?", "answers", "Here, love. The cafe's over the road from Mickey's. Half six till ten at night, and eight till twelve on a Sunday.", ["cafe", "my_hours"], "firsts: Where can I get something to eat?"),
        Q("Is there anywhere to get breakfast?", "answers", "Here, love. Half six in the morning. Sit down and I'll bring you a tea.", ["my_hours", "line"], "fresh: Is there anywhere to get breakfast?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Is June still about?", "answers", STD["june"], ["june"], "fresh: Is June still about?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
    ],
    schedule=PS(
        weekday=[(0, 6, "off"), (6, 14, "cafe"), (14, 17, "off"), (17, 22.5, "cafe"), (22.5, 24, "off")],
        saturday=[(0, 6, "off"), (6, 14, "cafe"), (14, 17, "off"), (17, 22.5, "cafe"), (22.5, 24, "off")],
        sunday=[(0, 7.5, "off"), (7.5, 12.5, "cafe"), (12.5, 24, "off")],
        note=WHY_NEW + " She opens at six for the half past six opening, takes the afternoon off, and keeps the evening trade the area's hours show (some regulars eat there on weekday evenings)."),
))

# ---------------------------------------------------------------- 29 Peter Tang (takeaway_m)
PEOPLE.append(regular(
    "takeaway_m", "Peter", knew=False, manner=("careful with strangers", "proud of his cooking"),
    knows=[
        K("with_wife", "REG", "keeps the takeaway on the parade with his wife", via="the contact sheet's who-and-where column"),
    ],
    believes=[
        BN("good_food_waits", "N-LIVES", "Good food is worth the ten minutes it takes, and a customer who will not wait is not worth the trouble.",
           "From his line 'Good food takes ten minutes.'", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[W("came_1968", "REG", "came from the New Territories in 1968", "1968, when he came to Britain")],
    rumours=[
        pool("heart", ["street"], ["takeaway_f"], ["died_heart"], "customers at the counter"),
        pool("arrive", ["street"], ["takeaway_f"], ["will"], "customers at the counter", limits=["L7"]),
        pool("fire", ["street"], ["takeaway_f"], ["fire"], "customers at the counter", limits=["L2", "L1"]),
        pool("june", ["street"], ["takeaway_f"], ["june"], "customers at the counter"),
        pool("trade", ["self"], ["takeaway_f"], ["trade"], "sees what the street spends", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Peter Tang. My wife and I keep the takeaway on the parade.", ["job", "with_wife"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I cook, and I'm proud of it. We keep the takeaway on the parade, my wife and I.", ["job", "manner2"], "firsts: What do you do here?"),
        Q("How long will it be?", "answers", "Ten minutes, love. Good food takes ten minutes.", ["line"], "invented: a stranger orders at a takeaway"),
        Q("How long have you been here?", "answers", "I came over in 1968.", ["came_1968"], "held: How long have you been here?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", "Here, love. Ten minutes, and good food takes ten minutes.", ["line", "job"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
    schedule=PS(
        weekday=[(0, 10, "off"), (10, 14, "takeaway"), (14, 16.5, "off"), (16.5, 23, "takeaway"), (23, 24, "off")],
        saturday=[(0, 10, "off"), (10, 14, "takeaway"), (14, 16.5, "off"), (16.5, 23, "takeaway"), (23, 24, "off")],
        sunday=[(0, 12, "off"), (12, 14, "takeaway"), (14, 16.5, "off"), (16.5, 22.5, "takeaway"), (22.5, 24, "off")],
        note=WHY_NEW + " A takeaway sells meals, so the Shops Act lets it open on a Sunday and late (shop-hours note); his unit is not fixed (RULINGS.md has bay 3 empty and to let)."),
    extra={"ties_new": [{"who": "takeaway_f", "weight": None, "band": "his wife", "meets": "they keep the takeaway together", "hours_a_week": None,
                         "source": {"file": "production/casting/regulars/REGULARS.md", "line": 116, "end": 116}}]},
))

# ---------------------------------------------------------------- 30 Lily Tang (takeaway_f)
PEOPLE.append(regular(
    "takeaway_f", "Lily", knew=False, manner=("warm with regulars", "sharp with anyone who's rude"),
    knows=[
        K("with_husband", "REG", "keeps the takeaway on the parade with his wife", via="her husband's row: the two keep the takeaway together"),
    ],
    believes=[
        BN("customers_known", "N-LIVES", "Regulars are remembered, and a customer who thinks she forgets is mistaken.",
           "From her line 'Same as last week? I remember. Everybody thinks I don't.'", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[W("front_books", "REG", "the takeaway's front and its books", "every day, at the front of the takeaway")],
    rumours=[
        pool("heart", ["street"], ["takeaway_m"], ["died_heart"], "customers at the counter"),
        pool("arrive", ["street"], ["takeaway_m"], ["will"], "customers at the counter", limits=["L7"]),
        pool("fire", ["street"], ["takeaway_m"], ["fire"], "customers at the counter", limits=["L2", "L1"]),
        pool("june", ["street"], ["takeaway_m"], ["june"], "customers at the counter"),
        pool("trade", ["self"], ["takeaway_m"], ["trade"], "she keeps the books and sees the takings", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Lily Tang. I'm the front of the takeaway, and I keep its books.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I'm the takeaway's front and its books. Warm with regulars, sharp with anyone who's rude.", ["job", "manner1", "manner2"], "firsts: What do you do here?"),
        Q("Do you remember what I had?", "answers", "Same as last week? I remember. Everybody thinks I don't.", ["line"], "invented: a stranger at a takeaway counter"),
        Q("Who keeps the takeaway?", "answers", "My husband and I keep the takeaway on the parade.", ["with_husband"], "invented: a stranger at a takeaway counter"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", "Here, love. Same as last week, if you've been.", ["line", "job"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
    schedule=PS(
        weekday=[(0, 11, "off"), (11, 14, "takeaway"), (14, 16.5, "off"), (16.5, 23, "takeaway"), (23, 24, "off")],
        saturday=[(0, 11, "off"), (11, 14, "takeaway"), (14, 16.5, "off"), (16.5, 23, "takeaway"), (23, 24, "off")],
        sunday=[(0, 12, "off"), (12, 14, "takeaway"), (14, 16.5, "off"), (16.5, 22.5, "takeaway"), (22.5, 24, "off")],
        note=WHY_NEW + " The front of the takeaway at the same hours as her husband, the books done in the afternoon break; his unit is not fixed (RULINGS.md has bay 3 empty and to let)."),
    extra={"ties_new": [{"who": "takeaway_m", "weight": None, "band": "her husband", "meets": "they keep the takeaway together", "hours_a_week": None,
                         "source": {"file": "production/casting/regulars/REGULARS.md", "line": 116, "end": 116}}]},
))
