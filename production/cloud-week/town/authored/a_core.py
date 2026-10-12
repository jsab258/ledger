"""Ron Kirby, Sheila Dunn, Darren Milner and Tom Nowak: the three who talk today and the player."""
from .common import *  # noqa: F401,F403

PEOPLE = []
PLACES = {}

# =============================================================== RON KIRBY (rocco)
PEOPLE.append(person(
    "rocco", "Ron Kirby", "Ron", "principal", 58,
    role=("S:rocco", "A docker until the dock labour scheme ended in 1989. Mickey kept him on the door and the rank."),
    identity=("CASTING", "**Ron Kirby** | 58"),
    street=STREET_ALL + MICKEY2, knew_mickey=True,
    knows=[
        K("nephew_unmet", "RON", "Before he came to the Hook I had never met Mickey's nephew, the new owner. Mickey spoke of him now and then, and that is all I knew of him before he came."),
        K("night_eye", "RON", "I notice who comes and goes on this street at night."),
        K("watches", "OUT", "Ron Kirby, kept on since the docks let him go, calls him boss and watches him."),
        K("arrangement", "ASK", "Mickey took this down the ferry landing, regular. After ten, to the man who asks for Mickey's. They'll be expecting it. Say no and that's Mickey's arrangement finished, mind; your call.", secret=True, via="what Ron says to the owner on night one"),
        K("keeps_quiet", "ASK", "Ron, who keeps things quiet for the owner, tells nobody.", secret=True),
        K("dead_street", "STL", "Street's dead since the docks went."),
        K("lamp", "STL", "They've still not fixed that lamp by the gate."),
        K("poll_tax", "STL", "You get your letter about the poll tax?"),
        D("day", "day"),
    ],
    believes=[
        B("comes_back", "STL", "I've seen it come and go. It comes back.", "unknown",
          NOTE("Canon and the outline leave why the docks went underneath, never explained (story-outline 20 to 22), so whether trade returns is not settled.")),
        BN("size_up", "N-LIVES", "A stranger who stands about his rank should stand where he can be seen; Ron will wait to see what the new owner does before he thinks anything of him.",
           "From his sheet's line 'You want to stand there, son, you stand where I can see you', and the outline's 'calls him boss and watches him'.", "unknown",
           NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        W("found", "SF", "I found Mickey at the office early one morning, when I came on at the rank; the doctor said it was his heart.", "the morning Mickey died"),
        W("arrive", "DAY1", "six see him come (Ron, Sheila, the dispatcher, a day driver, Ada, and the sign painter doing the street's boards)", "day 1, about nine, when the new owner came to Mickey's"),
    ],
    rumours=[
        pool("heart", ["self"], ["lena", "sam"], ["died_heart", "found"], "saw it himself"),
        pool("arrive", ["self"], ["lena", "sam", "joey"], ["arrive", "will"], "saw it himself",
             gist="Mickey's nephew came to Mickey's with his case; the new owner, with a letter."),
        pool("fire", ["sam"], ["lena", "joey"], ["fire"], "street talk, nobody in particular"),
        rumour("Three fares a day on the rank and the street dead since the docks went; nobody has the money for a cab.", "true", TB_TRADE, "saw it himself from the rank",
               ["self"], ["sam", "joey", "dusan"], ["dead_street", "trade"], ["L5"]),
        pool("june", ["lena"], ["sam", "noor"], ["june"], "heard it from Sheila, who sees her at the office"),
    ],
    questions=[
        Q("Who are you?", "answers", "Ron Kirby. I keep the rank outside Mickey's and watch the yard gate.", ["ron_rank"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "Mind the rank and the gate, boss. Mickey kept me on when the docks let me go.", ["ron_rank", "mickey_kept_ron"], "firsts: What do you do here?"),
        Q("How did Mickey die?", "answers", "His heart, the doctor said. I came on at the rank early one morning and found him at the office.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("Who found Mickey?", "answers", "I did. Early one morning, when I came on at the rank.", ["died_heart", "found"], "fresh: Who found Mickey?"),
        Q("What was Mickey like?", "answers", "Mickey kept his business to himself. You'd not hear it from him on the street.", ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Where can I get something to eat?", "answers", "The cafe's over the road, in the shops across from the north end of the parade. Half six till ten, and eight till twelve on a Sunday.", ["cafe"], "firsts: Where can I get something to eat?"),
        Q("What's behind that door?", "answers", "Mickey's own room, at the back. Locked since he died. Sheila keeps the key.", ["door"], "firsts: What's behind that door?"),
        Q("Did Mickey leave me anything?", "answers", "The office, boss. He left it to you by his will, and your letter says so.", ["will"], "firsts: Did Mickey leave me anything?"),
        Q("Where do I sleep?", "answers", "You're in Mickey's flat, over the office.", ["flat"], "firsts: Where do I sleep?"),
        Q("Who was Mickey's solicitor?", "dont_know", "No idea, boss. That's all I know.", [], "held: Who was Mickey's solicitor?"),
    ],
))

# =============================================================== SHEILA DUNN (lena)
PEOPLE.append(person(
    "lena", "Sheila Dunn", "Sheila", "principal", 53,
    role=("S:lena", "Mickey's bookkeeper for thirty-one years, since she was 22. A widow in a council flat."),
    identity=("CASTING", "**Sheila Dunn** | 53"),
    street=STREET_ALL + MICKEY2, knew_mickey=True,
    knows=[
        K("nephew_unmet", "LENA", "Before he came to the Hook I had never met Mickey's nephew, the new owner. Mickey spoke of him now and then, and that is all I knew of him before he came."),
        K("promised", "LENA", "I promised Mickey I would size up whoever inherited the office.", secret=True),
        K("real_book", "LENA", "The office's second book — the real one — exists, and I know where it is. I will not reveal where until I fully trust the new owner.", secret=True),
        K("phone_rings", "LENA", "The phone rings more than it used to and it is rarely good news."),
        K("world", "LENA", "the quay at the bottom of the street, the fish market two doors up, Rita's pawn beyond it, the market to the north, the docks, the bridges across to Copper Row."),
        K("fare_book", "DAY1", "Every fare goes in the book."),
        K("flat_things", "DAY1", "Your flat's upstairs, over the office. His things are still in it. I didn't have the heart."),
        K("books_know", "S:lena", "I know what every fare cost and who never paid it."),
        K("arrangements", "WEEK", "Take it over, then? Mickey's arrangements and everything that comes with them, yours.", secret=True, via="her words on day 7, over the book"),
        K("knows_name", "NAMES", "Mickey's own people, Sheila, Ron and Darren, know it from the start"),
        K("row", "NEWS", "Hal and Rita had words in the pawn, and nobody knows what about.", via="day 1, heard at Rita's step in the evening from the pawn's back-room hand"),
        D("day", "day"),
    ],
    believes=[
        B("worry", "LENA", "Underneath the dryness, she is tired and quietly worried about what happens to the office and to her.", "unknown",
          NOTE("A worry about the future; the story has not told it yet.")),
        BN("judge_by_deeds", "N-LIVES", "The new owner will show what he is by what he does, not by what he says.",
           "Follows her promise to Mickey to size up whoever inherited (talk card) and the outline's 'she promised Mickey to size him up'.", "unknown",
           NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        W("saw_argue", "LENA", "I saw Ron argue with a stranger in the yard behind the office two nights before Mickey died.", "two nights before Mickey died", secret=True),
        W("arrive", "DAY1", "six see him come (Ron, Sheila, the dispatcher, a day driver, Ada, and the sign painter doing the street's boards)", "day 1, about nine, when the new owner came to Mickey's"),
    ],
    rumours=[
        pool("heart", ["rocco"], ["rocco", "ada"], ["died_heart"], "heard it from Ron, who found him"),
        pool("arrive", ["self"], ["rocco", "ada"], ["arrive", "will"], "saw it herself",
             gist="Mickey's nephew has come, with one suitcase and a letter; Sheila showed the new management round."),
        rumour("Mickey's has not made much since the docks went; the takings are thin and the phone rings more than it used to, and it is rarely good news.", "true", TB_TRADE,
               "knows it from the books", ["self"], ["rocco", "june"], ["trade", "phone_rings"], ["L5"]),
        pool("june", ["self"], ["noor", "ada"], ["june"], "sees her at the office herself"),
        pool("halrita", ["victor"], ["rocco", "ada"], ["row"], "heard it from the pawn's back-room hand at Rita's step", limits=["L6", "L1"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Sheila Dunn. I keep the books at Mickey's, and have for thirty-one years.", ["sheila_books"], "firsts: Who are you?"),
        Q("What is this place?", "answers", "Mickey's is the minicab office, on Quay Street in the Hook. The rank's outside.", ["office"], "firsts: What is this place?"),
        Q("How many drivers are there?", "answers", "Two on the rank, one by day and one by night. The dispatcher's on the radio and the phone.", ["drivers"], "firsts: How many drivers are there?"),
        Q("What time do we open in the morning?", "answers", "Seven, nine on a Sunday. We run until the night driver goes home at three.", ["hours"], "held: What time do we open in the morning?"),
        Q("What's behind that door?", "answers", "Mickey's own room, at the back. It's been locked since he died, and I keep the key.", ["door"], "firsts: What's behind that door?"),
        Q("Sorry I missed the funeral.", "answers", "It was at Father Walsh's chapel, before you came. June came back for it.", ["funeral", "june"], "firsts: Sorry I missed the funeral."),
        Q("What was Mickey like?", "answers", "Mickey kept his business to himself. You'd not hear it from him on the street.", ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Can I have a look at the books?", "deflect", "Every fare goes in the book, and that's on the counter. The rest, you'll earn.", ["fare_book", "real_book"], "held: Can I have a look at the books?"),
        Q("Who can I trust?", "deflect", "Trust is earned, love. I don't hand it out on the doorstep.", ["promised"], "firsts: Who can I trust?"),
        Q("Where do I sleep?", "answers", "Your flat's upstairs, over the office. His things are still in it. I didn't have the heart.", ["flat_things", "flat"], "firsts: Where do I sleep?"),
    ],
))

# =============================================================== DARREN MILNER (sam)
PEOPLE.append(person(
    "sam", "Darren Milner", "Darren", "principal", 25,
    role=("S:sam", "The street hustler. Out of work since a youth training scheme; lives at his mother's; a pager, and the phone boxes."),
    identity=("CASTING", "**Darren Milner** | 25"),
    street=STREET_ALL + MICKEY2, knew_mickey=True,
    knows=[
        K("nephew_unmet", "SAM", "Before he came to the Hook I had never met Mickey's nephew, the new owner. Mickey spoke of him now and then, and that is all I knew of him before he came."),
        K("both_crowds", "SAM", "I move between the day crowd and the night crowd; both talk to me."),
        K("self_first", "SAM", "I look after myself first; everybody knows it."),
        K("owing", "OUT", "Darren Milner is already on the pavement, friendly and owing."),
        K("landing_man", "ASK", "to the street, a man who hangs about the ferry landing at night", via="the street's own word for him"),
        K("breakfast_man", "ASK", "He has his breakfast at the cafe on weekdays, where Darren starts his day, and the two know each other a little.", secret=True, via="the outfit's man at the landing, never named"),
        K("watchman", "FIRE", "His secret is that he slipped off home on his break the night of the fire and lied in his report, and Darren knows it.", secret=True),
        K("row", "NEWS", "Hal and Rita had words in the pawn, and nobody knows what about.", via="day 1, Monday at eleven, at Rita's: the town's sample story; he was there"),
        K("knows_name", "NAMES", "Mickey's own people, Sheila, Ron and Darren, know it from the start"),
        D("day", "day"),
    ],
    believes=[
        B("keeps_clear", "SAM", "I'm not scared of him. I'm just not going to be where he is.", "unknown",
          NOTE("The card never says who 'him' is, and nothing in canon names anyone.")),
        BN("tom_useful", "N-LIVES", "The new owner will be worth being useful to, and it pays to be first.",
           "Follows 'friendly and owing' (outline) and 'trades in being useful' (talk card).", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        W("man_at_breakfast", "ASK", "He has his breakfast at the cafe on weekdays, where Darren starts his day, and the two know each other a little.", "weekday mornings at the cafe, before the game", secret=True),
        W("row_seen", "NEWS", "Everybody in the pawn then saw it: Rita and Hal themselves, Darren Milner,", "day 1, Monday at eleven, at Rita's pawn"),
    ],
    rumours=[
        pool("halrita", ["self"], ["rocco", "lena", "ada"], ["row", "row_seen"], "saw it himself", limits=["L6", "L1"]),
        pool("fire", ["street"], ["rocco", "noor", "ada"], ["fire"], "street talk, nobody in particular"),
        pool("landing", ["self"], ["rocco", "noor"], ["landing_man"], "saw him himself", limits=["L1"]),
        pool("heart", ["rocco"], ["lena", "noor", "joey"], ["died_heart"], "heard it from Ron, who found him"),
        pool("june", ["street"], ["noor", "ada", "marla"], ["june"], "street talk"),
    ],
    questions=[
        Q("Who are you?", "answers", "Darren. I'm up and down Quay Street at all hours, talking to everyone. If it's being said round here, I've heard it.", ["darren_rounds"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "Out of work since the training scheme, mate. I've a pager and the phone boxes, and I walk the street.", ["job"], "firsts: What do you do here?"),
        Q("What is this place?", "answers", "Mickey's, mate. The cab office on Quay Street, with the rank outside.", ["office"], "firsts: What is this place?"),
        Q("How did Mickey die?", "answers", "His heart, the doctor said. Ron came on at the rank early one morning and found him at the office.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("Where can I get something to eat?", "answers", "The cafe's over the road, in the shops across from the north end of the parade. Half six till ten, mate, and eight till twelve on a Sunday.", ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Who runs things round here?", "points_to", "Round the office, Sheila keeps the books and Ron keeps the rank, mate. Past that I couldn't say.", ["sheila_books", "ron_rank"], "firsts: Who runs things round here?"),
        Q("What do people say about me?", "partly", "Only that Mickey's nephew's come and he's the new owner, mate. Nobody knows you yet.", ["will", "nephew_unmet"], "fresh: What do people say about me?"),
        Q("Did Mickey ever mention me?", "answers", "Now and then, mate. That's all I knew of you before you came.", ["nephew_unmet"], "held: Did Mickey ever mention me?"),
        Q("What happened at the warehouse fire?", "answers", "Importer's warehouse, far end of the old row, last November. Paper called it arson. Nobody was charged. Street says the owner had it done for the insurance.", ["fire"], "fresh: What happened at the warehouse fire?"),
        Q("Who's the man at the ferry landing at night?", "deflect", "Not going there, mate. Round here people remember who was asking.", ["breakfast_man"], "none: Who was the man in the grey car?"),
    ],
))

# =============================================================== TOM NOWAK (tom): what the town knows of him
PEOPLE.append(person(
    "tom", "Tom Nowak", "the new owner", "principal", 32,
    role=("CANON", "Tom has never been to the Hook: he is a stranger to everyone there, known only as Mickey's nephew by name (Jafar, 2026-09-23)."),
    identity=("CASTING", "**Tom Nowak** | 32"),
    street=["died_when", "will", "flat", "funeral"], knew_mickey=False, tom_exception=True,
    internal_id_note="No internal id found for the player; 'tom' is proposed (the sheet says only that Novak became Nowak on 24 September).",
    knows=[
        K("life_unsaid", "CANON", "His life before the Hook is left unsaid: nobody in the game asks and he never tells (Jafar, 2026-09-28)."),
        K("ladder", "CANON", "What the town calls you reads out your standing: the new owner, then Nowak, then Tom, then Tommy. The gate is knowing, not liking."),
        K("same_things", "S:tom", "One suitcase: he is seen in the same few things again and again, which the town will notice."),
        K("nephew_by_name", "CANON", "known only as Mickey's nephew by name (Jafar, 2026-09-23)."),
    ],
    believes=[
        BN("heir_rich", "N-LIVES", "Some on the street suppose the new owner has come into more than a cab office that has made little since the docks went.",
           "A street guess, a small hope or envy; canon's own picture is a half-dead outfit and uncollectable debts.", "false", TB_TRADE),
        BN("will_sell", "N-LIVES", "Some on the street suppose the new owner will sell up and go.",
           "A street guess; nothing in canon or the story settles what he will do (the week's end is the player's answer).", "unknown",
           H("WEEK", "Wind it down, take it over, or refuse to say".replace("Wind it down, take it over, or refuse to say", "wind it down, take it over, or refuse to say"))),
    ],
    saw=[
        W("arrive", "DAY1", "six see him come (Ron, Sheila, the dispatcher, a day driver, Ada, and the sign painter doing the street's boards)", "day 1, about nine, when he came to Mickey's"),
    ],
    rumours=[
        pool("nephew", ["rocco"], ["lena", "sam"], ["will", "nephew_by_name"], "saw him come, as the six did"),
        pool("funeral", ["lena"], ["rocco", "ada"], ["funeral"], "street fact, held by all"),
        pool("arrive", ["rocco"], ["sam", "ferko"], ["arrive"], "saw him come"),
        rumour("Some say the new owner has come into money. The takings say otherwise.", "false", TB_TRADE, "a guess, nobody saw anything",
               ["street"], ["rocco", "sam"], ["heir_rich"], ["L1", "L7"]),
        rumour("Some say the new owner will sell up and go.", "unknown", H("WEEK", "wind it down, take it over, or refuse to say"), "a guess, nobody knows",
               ["street"], ["sam", "ada"], ["will_sell"], ["L1", "L7"]),
    ],
    questions=[],
    schedule={"player_controlled": True, "note": "Tom is wherever the player takes him; his first day begins at nine at Mickey's (first-hour 51 to 52).",
              "source": {"file": "game-design/first-hour-2026-09-29.md", "line": 51, "end": 52},
              "weekday": [], "saturday": [], "sunday": [], "weekday_differs": {}},
    extra={"ties_new": [
        {"who": "rocco", "weight": None, "band": "first hand", "meets": "saw him come on day 1", "hours_a_week": None, "source": {"file": "game-design/day-one-2026-09-29.md", "line": 32, "end": 34}},
        {"who": "lena", "weight": None, "band": "first hand", "meets": "showed him round on day 1", "hours_a_week": None, "source": {"file": "game-design/day-one-2026-09-29.md", "line": 32, "end": 34}},
        {"who": "sam", "weight": None, "band": "Mickey's own people", "meets": "on the pavement on day 1", "hours_a_week": None, "source": {"file": "game-design/first-hour-2026-09-29.md", "line": 56, "end": 57}},
        {"who": "ada", "weight": None, "band": "first hand", "meets": "at her window on day 1", "hours_a_week": None, "source": {"file": "game-design/day-one-2026-09-29.md", "line": 32, "end": 34}},
        {"who": "zlata", "weight": None, "band": "first hand", "meets": "the dispatcher, saw him come", "hours_a_week": None, "source": {"file": "game-design/day-one-2026-09-29.md", "line": 32, "end": 34}},
        {"who": "ferko", "weight": None, "band": "first hand", "meets": "a day driver, saw him come", "hours_a_week": None, "source": {"file": "game-design/day-one-2026-09-29.md", "line": 32, "end": 34}},
        {"who": "franjo", "weight": None, "band": "first hand", "meets": "the sign painter, saw him come", "hours_a_week": None, "source": {"file": "game-design/day-one-2026-09-29.md", "line": 32, "end": 34}},
    ], "note": "Tom is the player: this entry is only what the town knows of him. His words are typed by the player and none is written."},
))
