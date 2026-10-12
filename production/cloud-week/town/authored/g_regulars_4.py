"""Regulars 19 to 24: Christine Pickering, Karen Grummitt, Gordon Leckenby, Sylvia Rennison, Edith Stockill, Shaun Hewson."""
from .common import *  # noqa: F401,F403

PEOPLE = []
PLACES = {}
ARRIVE = ("DAY1", "six see him come (Ron, Sheila, the dispatcher, a day driver, Ada, and the sign painter doing the street's boards)")
LANDING = ("ASK", "to the street, a man who hangs about the ferry landing at night")

# ---------------------------------------------------------------- 19 Christine Pickering (bruno)
PEOPLE.append(regular(
    "bruno", "Christine", knew=False, line_as="believes", line_truth="unknown",
    line_basis=NOTE("A clerk's remark; nothing in canon settles what is on the forms."), manner=("fond of forms",),
    knows=[D("day", "day")],
    believes=[],
    saw=[W("harbour_desk", "REG", "a clerk at the harbour office", "every working day, at the harbour office")],
    rumours=[
        pool("heart", ["petra"], ["petra"], ["died_heart"], "heard it from the ticket clerk at the landing"),
        pool("arrive", ["petra"], ["petra"], ["will"], "heard it from the ticket clerk", limits=["L7"]),
        pool("fire", ["petra"], ["petra"], ["fire"], "street talk, by way of the ticket clerk", limits=["L2", "L1"]),
        pool("june", ["petra"], ["petra"], ["june"], "heard it from the ticket clerk"),
        pool("trade", ["self"], ["petra"], ["trade"], "she sees the harbour's paper go thin", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Christine Pickering. I'm a clerk at the harbour office.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I'm a clerk at the harbour office. It's all on the forms, if anybody ever read the forms.", ["job", "line"], "firsts: What do you do here?"),
        Q("Where's the harbour office?", "answers", "The harbourmaster's office. That's where you'll find me.", ["day"], "invented: a stranger asks a clerk"),
        Q("Does the business owe anyone money?", "deflect", "It's all on the forms, if anybody ever read the forms.", ["line"], "held: Does the business owe anyone money?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 20 Karen Grummitt (petra)
PEOPLE.append(regular(
    "petra", "Karen", knew=False, line_as="believes", line_truth="unknown",
    line_basis=NOTE("Her own plan; the story does not say whether she goes."), manner=("wants out of the Hook",),
    knows=[K("landing_man", *LANDING, via="the street's own word for him; she keeps the landing's ticket desk by day"), D("day", "day")],
    believes=[],
    saw=[W("ferry_desk", "REG", "the ferry's ticket clerk", "every day, at the ferry landing")],
    rumours=[
        pool("heart", ["rocco"], ["noor", "bruno"], ["died_heart"], "heard it from Ron on Friday evening"),
        pool("arrive", ["rocco"], ["noor"], ["will"], "heard it from Ron", limits=["L7"]),
        pool("fire", ["noor"], ["bruno", "rocco"], ["fire"], "the paper's word, by way of the reporter", limits=["L2", "L1"]),
        pool("landing", ["self"], ["noor", "bruno"], ["landing_man"], "knows him by sight from the landing", limits=["L1"]),
        pool("trade", ["self"], ["bruno", "noor"], ["trade"], "sees how few take the ferry", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Karen Grummitt. I'm the ferry's ticket clerk, and I lodge at the boarding house.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I'm the ferry's ticket clerk.", ["job"], "firsts: What do you do here?"),
        Q("Why do you want to leave?", "answers", "I'll be on that boat myself one day. One way. I want out of the Hook.", ["line", "manner1"], "invented: a stranger asks a ticket clerk"),
        Q("Who's the man at the ferry landing at night?", "partly", "The street just says a man who hangs about the ferry landing at night. That's all I know.", ["landing_man"], "none: Who was the man in the grey car?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 21 Gordon Leckenby (dario)
PEOPLE.append(regular(
    "dario", "Gordon", knew=False, line_as="believes", line_truth="unknown",
    line_basis=NOTE("A ferryman's forecast; nothing in canon settles the weather."), manner=("weather-wise",),
    knows=[K("landing_man", *LANDING, via="the street's own word for him; he works the ferry by day"), D("day", "day")],
    believes=[],
    saw=[W("crossing", "REG", "a ferryman", "every working day, on the crossing")],
    rumours=[
        pool("heart", ["sam"], ["sam", "noor"], ["died_heart"], "heard it from Darren"),
        pool("arrive", ["sam"], ["noor"], ["will"], "heard it from Darren", limits=["L7"]),
        pool("fire", ["sam"], ["noor"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        pool("landing", ["self"], ["sam", "noor"], ["landing_man"], "knows him by sight from the landing", limits=["L1"]),
        pool("trade", ["self"], ["sam"], ["trade"], "sees how few cross", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Gordon Leckenby. I'm a ferryman.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I'm a ferryman. I'm weather-wise, they say.", ["job", "manner1"], "firsts: What do you do here?"),
        Q("What's the weather doing?", "answers", "Wind's getting up. She'll be lively on the crossing.", ["line"], "invented: a stranger asks a ferryman"),
        Q("Who's the man at the ferry landing at night?", "partly", "The street just says a man who hangs about the ferry landing at night. That's all I know.", ["landing_man"], "none: Who was the man in the grey car?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 22 Sylvia Rennison (sanja)
PEOPLE.append(regular(
    "sanja", "Sylvia", knew=False, manner=("strict about the rent",),
    knows=[D("day", "day")],
    believes=[
        BN("eyes_open", "N-LIVES", "A landlady who keeps her eyes open learns what her lodgers and the street are up to.",
           "From the contact sheet's 'house-proud, nosy'.", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[W("fish_buy", "REG", "buys fish for her lodgers", "most days, at the fish counter")],
    rumours=[
        pool("heart", ["rocco"], ["noor", "ada"], ["died_heart"], "heard it from Ron at the fish counter"),
        pool("arrive", ["ada"], ["noor"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("fire", ["noor"], ["ada", "rocco"], ["fire"], "the paper's word, by way of the reporter", limits=["L2", "L1"]),
        pool("june", ["noor"], ["ada"], ["june"], "heard it from the reporter"),
        pool("trade", ["self"], ["noor", "ada"], ["trade"], "sees what her lodgers can afford", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Sylvia Rennison. I'm a widow, and I keep the boarding house.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I keep the boarding house and buy fish for my lodgers.", ["job"], "firsts: What do you do here?"),
        Q("Have you a room?", "partly", "Rent's Friday, and Friday means Friday.", ["line"], "invented: a stranger asks a landlady"),
        Q("What's the rent?", "partly", "Rent's Friday, and Friday means Friday.", ["line", "manner1"], "invented: a stranger asks a landlady"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 23 Edith Stockill (hana)
PEOPLE.append(regular(
    "hana", "Edith", knew=True, manner=("keeps confidences",),
    knows=[D("my_hours", "hours", "newsagent"), D("day", "day")],
    believes=[
        BN("last_post", "N-LIVES", "Whatever goes in the post on a weekday should go by the last collection, and she will not have it missed.",
           "From her line 'It'll catch the last post.'", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[W("counter", "REG", "writes letters and fills in forms at the newsagent's pension counter", "most mornings, at the pension counter")],
    rumours=[
        pool("heart", ["ada"], ["ada", "noor"], ["died_heart"], "heard it from Ada on her step"),
        pool("funeral", ["ada"], ["ada", "noor"], ["funeral"], "heard it from Ada on her step"),
        pool("arrive", ["ada"], ["noor"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("june", ["ada"], ["noor"], ["june"], "heard it from Ada"),
        pool("trade", ["self"], ["sam", "ada"], ["trade"], "sees the pensions counter's custom thin", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Edith Stockill. I'm a retired shipping clerk, and I write letters and fill in forms at the newsagent's pension counter.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I write letters and fill in forms, dear, at the newsagent's pension counter.", ["job"], "firsts: What do you do here?"),
        Q("Can you help me with this form?", "answers", "Sign there, dear. And there. It'll catch the last post.", ["line"], "invented: a stranger with a form"),
        Q("What time is the counter open?", "answers", "The pensions counter's nine till half past five on weekdays, dear.", ["my_hours"], "held: What time do we open in the morning?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "answers", STD["mickey"], ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Is June still about?", "answers", STD["june"], ["june"], "fresh: Is June still about?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Sorry I missed the funeral.", "answers", STD["funeral"], ["funeral"], "firsts: Sorry I missed the funeral."),
    ],
))

# ---------------------------------------------------------------- 24 Shaun Hewson (franjo)
PEOPLE.append(regular(
    "franjo", "Shaun", knew=False, line_as="believes", line_truth="unknown",
    line_basis=NOTE("A sign painter's opinion; nothing in canon settles it."), manner=("proud of his lettering",),
    knows=[D("day", "day")],
    believes=[],
    saw=[
        W("arrive", *ARRIVE, "day 1, about nine, as the sign painter on the street's boards, when the new owner came to Mickey's"),
        W("boards", "REG", "the sign painter doing the street's boards this month", "this month, on the street's boards"),
    ],
    rumours=[
        pool("arrive", ["self"], ["lena", "rocco"], ["arrive", "will"], "saw it himself from the street's boards"),
        pool("heart", ["rocco"], ["lena", "danica"], ["died_heart"], "heard it from Ron at the cafe"),
        pool("fire", ["rocco"], ["lena"], ["fire"], "street talk at the cafe", limits=["L2", "L1"]),
        pool("june", ["lena"], ["rocco", "danica"], ["june"], "heard it from Sheila"),
        pool("trade", ["self"], ["lena", "rocco"], ["trade"], "sees how few shops want new boards", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Shaun Hewson. I'm the sign painter doing the street's boards this month.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I paint the street's boards this month, and I'm proud of my lettering.", ["job", "manner1"], "firsts: What do you do here?"),
        Q("Do you do lettering?", "answers", "Nobody looks at a sign till the spelling's wrong.", ["line"], "invented: a stranger asks a sign painter"),
        Q("Who's the big man on the rank?", "answers", "Ron Kirby. He keeps Mickey's door and the rank.", ["who_rocco"], "held: Who's the lad hanging about by the rank?"),
        Q("How did Mickey die?", "answers", STD["died_heart"], ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", STD["office"], ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", STD["cafe"], ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", STD["trade"], ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", STD["who_runs"], ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", "I never really knew him. That's all I know.", [], "firsts: What was Mickey like?"),
    ],
))
