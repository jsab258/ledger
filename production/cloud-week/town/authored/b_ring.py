"""Ada, June Suddaby, Father Walsh, Alison Sedman, Philip Danby: the day-life ring."""
from .common import *  # noqa: F401,F403

PEOPLE = []
PLACES = {}

ARRIVE = ("DAY1", "six see him come (Ron, Sheila, the dispatcher, a day driver, Ada, and the sign painter doing the street's boards)")

# =============================================================== ADA (ada)
PEOPLE.append(person(
    "ada", "Ada", "Ada", "principal", 78,
    role=("CASTING", "the old woman of the street; a widow who keeps a window on Quay Street"),
    identity=("CASTING", "**Ada** | 78"),
    street=STREET_ALL + MICKEY2, knew_mickey=True,
    knows=[
        K("widow", "S:ada", "A widow of the Hook."),
        K("window", "S:ada", "I've sat at that window a long time, love. Long enough to know when to say nothing."),
        K("remember", "S:ada", "I don't gossip. I remember. It's not the same thing."),
        K("step_rule", "S:ada", "Don't stand on my step with that face on. Come in or go on."),
        K("watches_out", "OUT", "Ada watches from her window."),
        D("day", "day"),
    ],
    believes=[
        BN("seen_remembered", "N-LIVES", "Whoever stands about the street long enough is seen, and what is seen is remembered.",
           "Follows her sheet's 'I don't gossip. I remember.'", "unknown", NOTE("A stance, not a fact about the world.")),
        BN("name_earned", "N-LIVES", "A man is no more than a name until he is seen to do something.",
           "Follows 'she does not ask a stranger in' (day-three design) and her window's patience.", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        W("watching_step", "S:ada", "On her step or at her window, watching; she turns her whole body to look, not just her head.", "every day, from her step or window"),
        W("arrive", *ARRIVE, "day 1, about nine, from her window, when the new owner came to Mickey's"),
    ],
    rumours=[
        pool("heart", ["lena"], ["emil", "marla"], ["died_heart"], "heard it from Sheila"),
        pool("arrive", ["self"], ["noor", "emil", "lena"], ["arrive", "will"], "saw it herself from her window"),
        rumour("The importer's warehouse at the far end of the old warehouse row burned down last November; the paper called it arson and nobody was charged.", "true", TB_FIRE_PAPER,
               "the paper's word; she does not repeat the rest", ["street"], ["magda", "hana"], ["fire"], ["L2", "L1"]),
        pool("june", ["emil"], ["noor", "vesna"], ["june"], "heard it from Father Walsh, who sees her at the chapel"),
        pool("door", ["lena"], ["noor", "magda"], ["door"], "heard it from Sheila, who keeps the key"),
    ],
    questions=[
        Q("Who are you?", "answers", "Ada, love. A widow of the Hook, with a window on Quay Street. I've sat at it a long time.", ["job", "widow", "window"], "firsts: Who are you?"),
        Q("What do you do here?", "answers", "I keep a window on Quay Street and I watch. I don't gossip. I remember.", ["job", "remember"], "firsts: What do you do here?"),
        Q("What is this place?", "answers", "Mickey's, love. The minicab office, on Quay Street. My step's across the road from it.", ["office", "day"], "firsts: What is this place?"),
        Q("How did Mickey die?", "answers", "His heart, the doctor said. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("Sorry I missed the funeral.", "answers", "It was at Father Walsh's chapel, love, before you came. June came back for it.", ["funeral", "june"], "firsts: Sorry I missed the funeral."),
        Q("Is June still about?", "answers", "She's still in town, love. She came back for the funeral and she wants nothing from the office.", ["june"], "fresh: Is June still about?"),
        Q("What was Mickey like?", "answers", "Mickey kept his business to himself. You'd not hear it from him on the street.", ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("What happened at the warehouse fire?", "partly", "The paper called it arson, love, and nobody was charged. The rest is street talk, and I don't gossip.", ["fire", "remember"], "fresh: What happened at the warehouse fire?"),
        Q("Who's the priest round here?", "answers", "Father Walsh, love. He says mass and calls on the old.", ["who_emil"], "fresh: Who's the priest round here?"),
        Q("Did Mickey ever mention me?", "dont_know", "Not to me, love. That's all I know.", [], "held: Did Mickey ever mention me?"),
    ],
))

# =============================================================== JUNE (june)
PEOPLE.append(person(
    "june", "June Suddaby", "June", "principal", 38,
    role=("CASTING", "Mickey's estranged daughter, back for the funeral"),
    identity=("CASTING", "**June Suddaby** | 38"),
    street=["died_when", "died_heart", "fire", "will", "funeral", "june", "flat", "door", "drivers", "hours", "trade", "cafe", "office", "sheila_books", "ron_rank"],
    knew_mickey=False,
    knows=[
        K("born", "S:june", "Born in the Hook; left it young."),
        K("came_back", "S:june", "I didn't come back for the business. I came back because somebody had to."),
        K("not_stopping", "S:june", "I'm not stopping long. I've a life to get back to."),
        K("coat_on", "S:june", "Keeps her coat on indoors at Mickey's and does not sit down there, as if she might leave at any minute."),
        D("day", "day"),
    ],
    believes=[
        B("leaving", "S:june", "I'm not stopping long. I've a life to get back to.", "unknown",
          NOTE("Canon has her 'still in town' and says nothing of when she goes.")),
    ],
    saw=[
        W("funeral_there", "SF", "I came back to the Hook for my father's funeral and I am still in town; I want nothing from the office.", "the funeral, before the game"),
    ],
    rumours=[
        pool("heart", ["emil"], ["lena", "emil"], ["died_heart"], "heard it from Father Walsh"),
        pool("nephew", ["lena"], ["emil", "lena"], ["will"], "heard it from Sheila"),
        pool("funeral", ["emil"], ["lena"], ["funeral_there", "funeral"], "was there herself"),
        pool("door", ["lena"], ["emil"], ["door"], "heard it from Sheila, who keeps the key"),
        rumour("June, Mickey's daughter, is still in town and wants nothing from the office.", "true", TB_JUNE, "her own word, said plainly", ["self"], ["lena", "emil"], ["june"], []),
    ],
    questions=[
        Q("Who are you?", "answers", "June. I came back to the Hook for my father's funeral and I'm still here. I want nothing from the office.", ["june"], "firsts: Who are you?"),
        Q("Was Mickey your father?", "answers", "He was. I'm his daughter, back for the funeral.", ["job"], "fresh: Is June still about?"),
        Q("What do you do here?", "answers", "Nothing here. I came back because somebody had to, and I'm not stopping long.", ["came_back", "not_stopping"], "firsts: What do you do here?"),
        Q("Did Mickey leave me anything?", "answers", "The office. He left it to you in his will, and the letter you came with says so.", ["will"], "firsts: Did Mickey leave me anything?"),
        Q("How did Mickey die?", "answers", "His heart, the doctor said. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("Sorry I missed the funeral.", "answers", "It was at Father Walsh's chapel, before you came. I was there.", ["funeral", "funeral_there"], "firsts: Sorry I missed the funeral."),
        Q("What's behind that door?", "answers", "Mickey's own room, at the back. It's been locked since he died, and Sheila keeps the key.", ["door"], "firsts: What's behind that door?"),
        Q("What was Mickey like?", "points_to", "Ask Sheila. She kept his books thirty-one years. I'm not the one to tell you.", ["sheila_books", "who_lena"], "firsts: What was Mickey like?"),
        Q("Are you stopping long?", "answers", "No. I've a life to get back to.", ["leaving", "not_stopping"], "fresh: Is June still about?"),
        Q("Who was Mickey's solicitor?", "dont_know", "I couldn't tell you. That's all I know.", [], "held: Who was Mickey's solicitor?"),
    ],
))

# =============================================================== FATHER WALSH (emil)
PEOPLE.append(person(
    "emil", "Father Brendan Walsh", "Father Walsh", "principal", 61,
    role=("CASTING", "the Irish-born parish priest, Father Walsh to the street"),
    identity=("CASTING", "**Father Brendan Walsh** | about 61"),
    street=STREET_ALL + MICKEY2, knew_mickey=True,
    internal_id_note="'emil' is the internal id (the sheet folder keeps the old name: father-emil).",
    extra={"note": "Age: the casting row says 'about 61'."},
    knows=[
        K("called", "HK", "Father Walsh, who says mass and calls on the old"),
        K("in_case", "S:emil", "I'm not here to ask you anything. I'm here in case you want to say something."),
        K("sit", "S:emil", "Sit a minute. Nobody's going to mind you sitting a minute."),
        N("confessor", "N-REWORDED", "Father Walsh heard Mickey's confession for twenty years, the last year's with it.", "Reworded from the fire design (game-design/warehouse-fire-2026-09-29.md): the design's line is a note about his card ('Father Walsh's card changes to...'), not in his knowledge. Sealed: never said, never passed on. Review T1.", secret=True),
        K("sealed", "FIRE", "Father Walsh heard him confess it, and the seal of confession keeps him silent for good, so the book is the only way to the truth.", secret=True, via="sealed: the fire's truth is never the street's"),
        D("day", "day"),
    ],
    believes=[
        B("all_right", "S:emil", "I don't ask where people have been. I ask whether they're all right.", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        WN("funeral_led", "N-LIVES", "Father Walsh took Mickey's funeral service at his chapel.",
           "The street fact puts the funeral at his chapel; a priest takes the service there.", "the funeral, before the game"),
        W("round", "S:emil", "An unhurried walk round the parish with his hands behind his back; stops for everybody; calls on the old.", "every day, round the parish"),
    ],
    rumours=[
        pool("heart", ["vesna"], ["vesna", "ada"], ["died_heart"], "heard it from his housekeeper, who had it from the street"),
        pool("funeral", ["self"], ["vesna", "ada", "june"], ["funeral", "funeral_led"], "was there himself, at the service"),
        pool("june", ["self"], ["vesna", "ada"], ["june"], "sees her at the chapel"),
        pool("nephew", ["ada"], ["vesna", "ada"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("trade", ["ada"], ["vesna", "ada"], ["trade"], "heard it from the street"),
    ],
    questions=[
        Q("Who are you?", "answers", "Father Walsh, son. I've the parish here.", ["job"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "I say mass and I call on the old. I stop for everybody.", ["called", "round"], "firsts: What do you do here?"),
        Q("Who's the priest round here?", "answers", "I am, son. Father Walsh.", ["job"], "fresh: Who's the priest round here?"),
        Q("How did Mickey die?", "answers", "His heart, the doctor said. Ron found him at the office early one morning.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("Sorry I missed the funeral.", "answers", "It was at my chapel, before you came. Sit a minute. Nobody's going to mind you sitting.", ["funeral", "funeral_led", "sit"], "firsts: Sorry I missed the funeral."),
        Q("What was Mickey like?", "answers", "Mickey kept his business to himself. You'd not hear it from him on the street.", ["mickey_counsel"], "firsts: What was Mickey like?"),
        Q("Did Mickey have any enemies?", "deflect", "I don't ask where people have been, son. I ask whether they're all right.", ["all_right"], "fresh: Did Mickey have any enemies?"),
        Q("What happened at the warehouse fire?", "deflect", "The paper called it arson, and nobody was charged. Beyond that, son, I've nothing to say.", ["fire", "sealed"], "fresh: What happened at the warehouse fire?"),
        Q("Is June still about?", "answers", "She is. She came back for the funeral and she's still in town. She wants nothing from the office.", ["june"], "fresh: Is June still about?"),
        Q("Who can I trust?", "partly", "I'm not here to ask you anything, son. I'm here in case you want to say something.", ["in_case"], "firsts: Who can I trust?"),
    ],
))

# =============================================================== ALISON SEDMAN (noor)
PEOPLE.append(person(
    "noor", "Alison Sedman", "Alison", "principal", 30,
    role=("CASTING", "a reporter on the local paper"),
    identity=("CASTING", "**Alison Sedman** | 30"),
    street=STREET_ALL, knew_mickey=False,
    knows=[
        K("not_writing", "S:noor", "I'm not writing anything yet. I'm just listening. People forget there's a difference."),
        K("twice", "S:noor", "I like to hear a thing twice before I believe it once."),
        K("dont_ask", "S:noor", "You'd be surprised what people tell you when you don't ask."),
        K("never_landed", "FIRE", "Mickey's outfit was the story she never landed.", secret=True, via="her own working belief about the fire; not told to a stranger"),
        K("editor", "FIRE", "Her editor wants it dropped."),
        K("moves", "S:noor", "Fast, always half writing; leans on counters; asks the second question after the answer."),
        K("row", "NEWS", "Hal and Rita had words in the pawn, and nobody knows what about.", via="day 1, heard from the pawn's clerk at the kiosk"),
        D("day", "day"),
    ],
    believes=[
        B("thinks_outfit", "FIRE", "She has heard the owner stopped paying somebody, so she thinks the outfit burned him out, and that Mickey knew.", "true",
          H("FIRE", "The truth, kept out of the talk:", note="Her belief matches the story's truth; she cannot prove it and it is not the street's."), secret=True),
    ],
    saw=[
        WN("covered_fire", "N-LIVES", "She covered the warehouse fire for the paper and walked the burned row afterwards.",
           "She 'will not drop' the story (outline); a reporter on the paper would have covered it.", "last November, the days after the fire"),
    ],
    rumours=[
        pool("fire", ["street"], ["ada", "sam"], ["fire", "covered_fire"], "the paper's own word and street talk; she has not got more", limits=["L2", "L1"]),
        pool("heart", ["lena"], ["ada", "sam"], ["died_heart"], "heard it from Sheila"),
        pool("nephew", ["ada"], ["sam", "rocco"], ["will"], "heard it from Ada, who saw it from her window", limits=["L7"]),
        pool("halrita", ["marta"], ["ada", "sam"], ["row"], "heard it from the pawn's clerk at the kiosk", limits=["L6", "L1"]),
        pool("june", ["ada"], ["lena", "sam"], ["june"], "heard it from Ada"),
    ],
    questions=[
        Q("Who are you?", "answers", "Alison Sedman. I'm a reporter on the local paper.", ["job"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "I listen. I'm not writing anything yet. People forget there's a difference.", ["not_writing"], "firsts: What do you do here?"),
        Q("What happened at the warehouse fire?", "partly", "The importer's warehouse on the old row, last November. The paper called it arson. Nobody was charged. I'm not writing anything yet.", ["fire", "not_writing"], "fresh: What happened at the warehouse fire?"),
        Q("How did Mickey die?", "answers", "His heart, the doctor said. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("What do people say about me?", "partly", "Only that Mickey's nephew has come, and Mickey left you the office. I like to hear a thing twice.", ["will", "twice"], "fresh: What do people say about me?"),
        Q("Who was Mickey closest to?", "dont_know", "I couldn't tell you. That's all I know.", [], "fresh: Who was Mickey closest to?"),
        Q("What's the cafe like?", "answers", "It's over the road, in the shops across from the north end of the parade. Half past six till ten at night, and eight till twelve on a Sunday.", ["cafe"], "fresh: What's the cafe like?"),
        Q("Who's the priest round here?", "partly", "Father Walsh, I think. Mickey's funeral was at his chapel.", ["funeral"], "fresh: Who's the priest round here?"),
        Q("Is June still about?", "answers", "She's still in town. She came back for the funeral and wants nothing from the office.", ["june"], "fresh: Is June still about?"),
        Q("Who can I trust?", "deflect", "People tell you a lot when you don't ask. I'd listen first.", ["dont_ask"], "firsts: Who can I trust?"),
    ],
))
