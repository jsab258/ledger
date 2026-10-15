"""Regulars 13 to 18: Julie Kettlewell, Tracey Scarth, Colin Mastin, Albert Suggitt, Gary Mawer, Ian Megginson."""
from .common import *  # noqa: F401,F403

PEOPLE = []
PLACES = {}
DOCKS_LOSS = H("OUT", "the dock labour scheme ended in July 1989 and more than half the registered dockers' jobs went")

# ---------------------------------------------------------------- 13 Julie Kettlewell (tanja)
sty, tag = "brisk", "love"
PEOPLE.append(regular(
    "tanja", "Julie", knew=False, manner=("sharp about the laundry",),
    knows=[D("day", "day")],
    believes=[B("generous", "REG", "Generous, they called it.", "unknown", NOTE("Her own bitter remark on the notice she was given; nothing settles whether it was generous."))],
    saw=[W("notice", "REG", "Twelve years on them presses and twelve weeks' notice.", "the summer, when she was laid off from the presses")],
    rumours=[
        rumour("A laundress laid off from the steam laundry's presses in the summer is looking for anything.", "true", H("REG", "laid off from the steam laundry's presses in the summer, looking for anything"),
               "first hand: it is her own", ["self"], ["ada"], ["job"], []),
        pool("heart", ["ada"], ["ada"], ["died_heart"], "heard it from Ada"),
        pool("nephew", ["ada"], ["ada"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("june", ["ada"], ["ada"], ["june"], "heard it from Ada"),
        pool("trade", ["self"], ["ada"], ["trade"], "she has felt the street's trade go herself", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Julie Kettlewell. I was laid off from the steam laundry's presses in the summer, and I'm looking for anything.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "Looking for anything, me. Laid off from the presses in the summer.", ["job"], "firsts: What do you do here?"),
        Q("Why were you laid off?", "answers", "Twelve years on them presses and twelve weeks' notice. Generous, they called it.", ["line", "generous"], "invented: a stranger asks a woman on the pavement"),
        Q("Is there any work going?", "dont_know", "Not that I've found. That's all I know.", [], "invented: a stranger asks a woman looking for work"),
        Q("How did Mickey die?", "answers", std("died_heart", sty, tag), ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", std("office", sty, tag), ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", std("cafe", sty, tag), ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", std("trade", sty, tag), ["trade"], "held: Is it always this quiet?"),
        Q("What was Mickey like?", "dont_know", std("dk_mickey", sty, tag), [], "firsts: What was Mickey like?"),
        Q("Who runs things round here?", "points_to", std("who_runs", sty, tag), ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
    ],
    schedule=PS(
        weekday=[(0, 9, "off"), (9, 10, "kiosk"), (10, 11, "laundry_front"), (11, 12, "pension_counter"), (12, 24, "off")],
        saturday=[(0, 11, "off"), (11, 13, "market"), (13, 24, "off")], sunday=[(0, 24, "off")],
        note="Replaces hook-cast.json's laundry routine: the contact sheet (row 8) says she was laid off in the summer, so the laundry's day loses her. She looks for work: the kiosk's cards, the laundry's pavement, the newsagent's counter."),
    extra={"override_why": "REGULARS.md row 8 and its notes: Tanja is laid off now, so the laundry's day loses her; hook-cast.json (28 Sep, earlier) still puts her at the laundry counter seven to six."},
))

# ---------------------------------------------------------------- 14 Tracey Scarth (katarina)
sty, tag = "warm", "love"
PEOPLE.append(regular(
    "katarina", "Tracey", knew=False, manner=("sews while she talks",),
    knows=[D("my_hours", "hours", "laundry"), D("market_hours", "hours", "market"), D("day", "day")],
    believes=[
        BN("stall_grows", "N-LIVES", "The market stall could grow into a shop of her own one day.",
           "From the contact sheet's 'chatty, ambitious'.", "unknown", NOTE("An ambition, not a fact about the world.")),
    ],
    saw=[W("two_jobs", "REG", "alterations at the laundry and a stall on the market", "every week, at the laundry and on the market")],
    rumours=[
        pool("heart", ["sam"], ["sam", "ada"], ["died_heart"], "heard it from Darren at the market"),
        pool("nephew", ["sam"], ["ada"], ["will"], "heard it from Darren", limits=["L7"]),
        pool("fire", ["sam"], ["ada"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        pool("june", ["ada"], ["sam"], ["june"], "heard it from Ada at the laundry"),
        pool("trade", ["self"], ["ada", "sam"], ["trade"], "sees what the street can afford", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Tracey Scarth. I'm a seamstress: alterations at the laundry and a stall on the market.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I do alterations at the laundry and I've a stall on the market. I sew while I talk.", ["job", "manner1"], "firsts: What do you do here?"),
        Q("Can you alter this?", "answers", "Take it in two inches and nobody'll know it wasn't made for you.", ["line"], "invented: a stranger with a coat over his arm"),
        Q("When are you on the market?", "answers", "Tuesdays, Fridays and Saturdays, from eight till four.", ["market_hours"], "invented: a stranger looks for a stall"),
        Q("What time does the laundry open?", "answers", "Eight till half past five, Monday to Saturday.", ["my_hours"], "held: What time do we open in the morning?"),
        Q("How did Mickey die?", "answers", std("died_heart", sty, tag), ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", std("office", sty, tag), ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", std("cafe", sty, tag), ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Who runs things round here?", "points_to", std("who_runs", sty, tag), ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", std("dk_mickey", sty, tag), [], "firsts: What was Mickey like?"),
    ],
))

# ---------------------------------------------------------------- 15 Colin Mastin (stipe)
sty, tag = "terse", "mate"
PEOPLE.append(regular(
    "stipe", "Colin", knew=False, line_as="believes", line_truth="true", line_basis=DOCKS_LOSS, manner=("worried about the work going",),
    knows=[D("day", "day")],
    believes=[],
    saw=[W("berths", "REG", "Half the berths empty.", "every working day, from the crane")],
    rumours=[
        pool("heart", ["rocco"], ["sam", "rocco"], ["died_heart"], "heard it from Ron on the quay"),
        pool("nephew", ["rocco"], ["sam"], ["will"], "heard it from Ron on the quay", limits=["L7"]),
        pool("fire", ["sam"], ["rocco"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        rumour("Half the berths on the docks are empty.", "true", DOCKS_LOSS, "sees the berths himself, from the crane",
               ["self"], ["sam", "rocco"], ["line", "berths"], ["L5"]),
        pool("june", ["rocco"], ["sam"], ["june"], "heard it from Ron"),
    ],
    questions=[
        Q("Who are you?", "answers", "Colin Mastin. I drive a crane on the docks, and I'm home by the quay.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I drive a crane on the docks.", ["job"], "firsts: What do you do here?"),
        Q("How's work?", "answers", "Half the berths empty. You stop asking after a while.", ["line"], "invented: a stranger asks a docker"),
        Q("Why are the berths empty?", "deflect", "You stop asking after a while.", ["line"], "invented: a stranger asks a docker"),
        Q("How did Mickey die?", "answers", std("died_heart", sty, tag), ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", std("office", sty, tag), ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", std("cafe", sty, tag), ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", std("trade", sty, tag), ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", std("who_runs", sty, tag), ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("Where's the nearest phone box?", "dont_know", "I couldn't tell you. That's all I know.", [], "held: Where's the nearest phone box?"),
    ],
))

# ---------------------------------------------------------------- 16 Albert Suggitt (fabjan)
sty, tag = "terse", "son"
PEOPLE.append(regular(
    "fabjan", "Albert", knew=False, manner=("full of the old fleet",),
    knows=[D("day", "day")],
    believes=[
        BN("old_fleet", "N-LIVES", "The old fleet was a better trade than anything the dock has now.",
           "From 'full of the old fleet' and his line; no reason is given for why the docks went.", "unknown", NOTE("An old man's opinion; the story keeps why the docks went underneath, never explained.")),
    ],
    saw=[W("nets", "REG", "mends nets on the docks some mornings", "some mornings, on the docks")],
    rumours=[
        pool("heart", ["rocco"], ["sam", "rocco"], ["died_heart"], "heard it from Ron on the quay"),
        pool("nephew", ["rocco"], ["sam"], ["will"], "heard it from Ron on the quay", limits=["L7"]),
        pool("fire", ["sam"], ["rocco", "goran"], ["fire"], "street talk, by way of Darren", limits=["L2", "L1"]),
        pool("trade", ["self"], ["sam", "goran"], ["trade"], "sees the dock himself", limits=["L5"]),
        pool("june", ["rocco"], ["sam"], ["june"], "heard it from Ron"),
    ],
    questions=[
        Q("Who are you?", "answers", "Albert Suggitt. A retired trawlerman, and I mend nets on the docks some mornings.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I mend nets on the docks some mornings. I'm retired.", ["job"], "firsts: What do you do here?"),
        Q("How long were you at sea?", "answers", "Forty year at sea and they give me a needle and a stool.", ["line"], "invented: a stranger asks an old trawlerman"),
        Q("What's the dock like now?", "dont_know", "Quiet, son. That's all I know.", [], "invented: a stranger asks an old trawlerman"),
        Q("How did Mickey die?", "answers", std("died_heart", sty, tag), ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", std("office", sty, tag), ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", std("cafe", sty, tag), ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", std("trade", sty, tag), ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", std("who_runs", sty, tag), ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", std("dk_mickey", sty, tag), [], "firsts: What was Mickey like?"),
    ],
    schedule=PS(
        weekday=[(0, 6, "off"), (6, 12, "docks"), (12, 17, "off"), (17, 18, "quay"), (18, 24, "off")],
        differs={"tue": [(0, 17, "off"), (17, 18, "quay"), (18, 24, "off")], "thu": [(0, 17, "off"), (17, 18, "quay"), (18, 24, "off")]},
        saturday=[(0, 24, "off")], sunday=[(0, 24, "off")],
        note="Replaces hook-cast.json's docks-all-day routine: the contact sheet says he mends nets 'some mornings' and REGULARS.md's notes say 'Albert mends nets mornings only'. Monday, Wednesday and Friday mornings on the docks; the quay at five as before."),
    extra={"override_why": "REGULARS.md: 'Albert mends nets mornings only' (the routines are the town's to write); hook-cast.json (28 Sep, earlier) has him on the docks six to five on weekdays."},
))

# ---------------------------------------------------------------- 17 Gary Mawer (tomas)
sty, tag = "warm", "mate"
PEOPLE.append(regular(
    "tomas", "Gary", knew=False, manner=("always hungry",),
    knows=[D("day", "day")],
    believes=[
        BN("boats_mend", "N-LIVES", "Boats still need mending whatever the docks are doing, so the yard stays busy.",
           "Follows his trade, 'a boat repairer at the yard'.", "unknown", NOTE("A tradesman's view; the story does not settle it.")),
    ],
    saw=[W("breakfast", "REG", "breakfast at the caff, the docks twice a week", "most mornings at the cafe; the docks on Tuesday and Thursday")],
    rumours=[
        pool("heart", ["rocco"], ["sam", "rocco"], ["died_heart"], "heard it from Ron at the cafe"),
        pool("nephew", ["rocco"], ["sam"], ["will"], "heard it from Ron at the cafe", limits=["L7"]),
        pool("fire", ["sam"], ["rocco"], ["fire"], "street talk, by way of Darren on the docks", limits=["L2", "L1"]),
        pool("trade", ["self"], ["sam", "rocco"], ["trade"], "sees it at the yard", limits=["L5"]),
        pool("june", ["rocco"], ["sam"], ["june"], "heard it from Ron"),
    ],
    questions=[
        Q("Who are you?", "answers", "Gary Mawer. I'm a boat repairer at the yard.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I repair boats at the yard. Breakfast at the caff first, mind.", ["job"], "firsts: What do you do here?"),
        Q("Where can I get breakfast?", "answers", "Bacon sandwich and a tea, then I'm anybody's. The cafe's over the road, in the shops across from the north end of the parade.", ["line", "cafe"], "fresh: Is there anywhere to get breakfast?"),
        Q("Where can I get something to eat?", "answers", std("cafe", sty, tag), ["cafe"], "firsts: Where can I get something to eat?"),
        Q("How did Mickey die?", "answers", std("died_heart", sty, tag), ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", std("office", sty, tag), ["office"], "firsts: What is this place?"),
        Q("Is it always this quiet?", "answers", std("trade", sty, tag), ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", std("who_runs", sty, tag), ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", std("dk_mickey", sty, tag), [], "firsts: What was Mickey like?"),
        Q("Is June still about?", "answers", std("june", sty, tag), ["june"], "fresh: Is June still about?"),
    ],
))

# ---------------------------------------------------------------- 18 Ian Megginson (luka)
sty, tag = "terse", ""
PEOPLE.append(regular(
    "luka", "Ian", knew=False, manner=("knows every lock on the street",),
    knows=[D("day", "day")],
    believes=[
        BN("locks_weak", "N-LIVES", "Most of the street's locks would not stop anyone patient.",
           "From his line 'Old lock, that. Anybody with a hairpin and an hour.'", "unknown", NOTE("A locksmith's opinion, not a fact about the world.")),
    ],
    saw=[W("locks_seen", "REG", "knows every lock on the street", "every working day, mending and repairing")],
    rumours=[
        pool("heart", ["rocco"], ["rocco"], ["died_heart"], "heard it from Ron at the cafe"),
        pool("nephew", ["rocco"], ["rocco"], ["will"], "heard it from Ron at the cafe", limits=["L7"]),
        pool("fire", ["street"], ["rocco"], ["fire"], "street talk at the cafe", limits=["L2", "L1"]),
        pool("door", ["rocco"], ["rocco"], ["door"], "heard it from Ron, who knows who has the key"),
        rumour("Most of the street's locks would not stop a patient man.", "unknown", NOTE("A locksmith's opinion, not a fact about the world."), "he has mended the street's locks himself",
               ["self"], ["rocco"], ["locks_weak", "locks_seen"], []),
    ],
    questions=[
        Q("Who are you?", "answers", "Ian Megginson. I'm a locksmith and repairman at the yard.", ["job"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I'm a locksmith and repairman. I know every lock on the street.", ["job", "manner1"], "firsts: What do you do here?"),
        Q("What's that lock like?", "answers", "Old lock, that. Anybody with a hairpin and an hour.", ["line"], "invented: a stranger asks a locksmith"),
        Q("Who's got the keys to this place?", "answers", "Mickey's own room has been locked since he died, and Sheila keeps the key.", ["door"], "held: Who's got the keys to this place?"),
        Q("How did Mickey die?", "answers", std("died_heart", sty, tag), ["died_heart"], "firsts: How did Mickey die?"),
        Q("What is this place?", "answers", std("office", sty, tag), ["office"], "firsts: What is this place?"),
        Q("Where can I get something to eat?", "answers", std("cafe", sty, tag), ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is it always this quiet?", "answers", std("trade", sty, tag), ["trade"], "held: Is it always this quiet?"),
        Q("Who runs things round here?", "points_to", std("who_runs", sty, tag), ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What was Mickey like?", "dont_know", std("dk_mickey", sty, tag), [], "firsts: What was Mickey like?"),
    ],
))
