"""Carol Ellis, Geoffrey Agar, Maureen Jensen, Danny Cammack, Keith Garbutt, Philip Danby:
the six principals hook-cast.json has no routine for (their schedules are proposals)."""
from .common import *  # noqa: F401,F403

PEOPLE = []
PLACES = {}

WHY_NEW_ROUTINE = "No routine for this person in hook-cast.json; proposed from the sheet, the shop hours and the districts of canon.md."

# =============================================================== DS CAROL ELLIS (ellis)
PEOPLE.append(person(
    "ellis", "Carol Ellis", "DS Ellis", "principal", 40,
    role=("S:ellis", "Detective Sergeant, CID, in plain clothes."),
    identity=("CASTING", "**DS Carol Ellis** | 40"),
    street=["died_when", "died_heart", "fire", "office", "trade"], knew_mickey=False,
    knows=[
        K("local", "S:ellis", "A local woman who came up through the town's force."),
        K("same_twice", "S:ellis", "I'm not asking you to remember everything. I'm asking you to remember it the same way twice."),
        K("write_down", "S:ellis", "Write it down. Paper doesn't get tired and it doesn't change its mind."),
        K("here_or_station", "S:ellis", "You can talk to me here, or you can talk to me at the station. I'd rather here. So would you."),
        K("on_the_fire", "FIRE", "she was the detective sergeant on it. The file was marked undetected, and she keeps asking"),
        K("times", "FIRE", "the watchman's times do not fit the brigade's"),
        K("moves", "S:ellis", "Brisk and economical. Writes in her notebook while she listens and lets silences run."),
    ],
    believes=[
        B("paid_away", "FIRE", "the watchman's times do not fit the brigade's, and she thinks someone paid him to be away.", "false",
          H("FIRE", "Nobody did, but it is why she will not let it go", note="False against the story; it is why she will not let the fire go.")),
    ],
    saw=[
        W("sergeant", "FIRE", "she was the detective sergeant on it.", "last November, the fire and the days after"),
    ],
    rumours=[
        pool("fire", ["self"], ["noor"], ["fire", "on_the_fire"], "first hand: the file's own words", limits=["L2", "L1"],
             gist="The importer's warehouse at the far end of the old warehouse row burned down last November; it started in two places and nobody was charged."),
        rumour("The fire's file was marked undetected, and the sergeant on it keeps asking.", "true", H("FIRE", "she was the detective sergeant on it. The file was marked undetected, and she keeps asking"), "first hand: her own file",
               ["self"], ["noor", "filip"], ["on_the_fire"], ["L2"]),
        rumour("The watchman's times on the night of the fire do not fit the brigade's.", "true", H("FIRE", "the watchman's times do not fit the brigade's"), "first hand: she has compared them",
               ["self"], ["filip"], ["times"], ["L2", "L1"]),
        pool("heart", ["street"], ["noor"], ["died_heart"], "heard it on the street; the doctor's word"),
        pool("trade", ["street"], ["noor"], ["trade"], "heard it on the street"),
    ],
    questions=[
        Q("Who are you?", "answers", "DS Carol Ellis, CID. I'm in plain clothes.", ["job"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "I ask questions, and I write the answers down. Paper doesn't get tired.", ["write_down"], "firsts: What do you do here?"),
        Q("What happened at the warehouse fire?", "partly", "The importer's warehouse on the old row, last November. Started in two places. Nobody was charged. I was the sergeant on it, and I keep asking.", ["fire", "on_the_fire"], "fresh: What happened at the warehouse fire?"),
        Q("How did Mickey die?", "answers", "His heart, the doctor said. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("Did Mickey have any enemies?", "deflect", "I'm not asking you to remember everything. I'm asking you to remember it the same way twice.", ["same_twice"], "fresh: Did Mickey have any enemies?"),
        Q("What do people say about me?", "dont_know", "Nothing to me yet. That's all I know.", [], "fresh: What do people say about me?"),
        Q("Who can I trust?", "deflect", "Write it down. Paper doesn't get tired and it doesn't change its mind.", ["write_down"], "firsts: Who can I trust?"),
        Q("What is this place?", "answers", "Mickey's, the minicab office, on Quay Street in the Hook. The rank's outside.", ["office"], "firsts: What is this place?"),
        Q("Can we talk?", "answers", "You can talk to me here, or at the station. I'd rather here. So would you.", ["here_or_station"], "invented: a stranger meeting a detective"),
        Q("Who was Mickey's solicitor?", "dont_know", "I couldn't tell you. That's all I know.", [], "held: Who was Mickey's solicitor?"),
    ],
    schedule=PS(
        weekday=[(0, 8.5, "off"), (8.5, 17, "station"), (17, 18, "warehouse_row"), (18, 24, "off")],
        differs={"tue": [(0, 8.5, "off"), (8.5, 18, "station"), (18, 24, "off")], "thu": [(0, 8.5, "off"), (8.5, 18, "station"), (18, 24, "off")]},
        saturday=[(0, 9, "off"), (9, 13, "station"), (13, 24, "off")], sunday=[(0, 24, "off")],
        note=WHY_NEW_ROUTINE + " She is off Quay Street until the story brings her (police-asking: days 4 and 5, each reason once); Monday, Wednesday and Friday at the row when the watchman comes on."),
    extra={"ties_new": [
        {"who": "noor", "weight": None, "band": "both are on the fire", "meets": "the fire: the reporter who will not drop it, the sergeant who will not close it", "hours_a_week": None,
         "source": SQ("FIRE", "**Alison:** Mickey's outfit was the story she never landed.")},
        {"who": "filip", "weight": None, "band": "she goes back to him", "meets": "the watchman whose times do not fit", "hours_a_week": None,
         "source": SQ("FIRE", "the watchman's times do not fit the brigade's")},
    ]},
))

# =============================================================== GEOFFREY AGAR (aldous)
PEOPLE.append(person(
    "aldous", "Geoffrey Agar", "Mr Agar", "principal", 62,
    role=("CASTING", "solicitor and alderman, head of the old-money machine"),
    identity=("CASTING", "**Geoffrey Agar** | 62"),
    street=["died_when", "died_heart", "fire", "office", "trade"], knew_mickey=False,
    internal_id_note="'aldous' is the internal id (the old name Aldous Vane survives only as an id).",
    knows=[
        K("solicitor", "S:aldous", "Solicitor; a former long-serving councillor, now honorary alderman"),
        K("machine", "CANON", "the old-money machine (corruption and lawyers, head Geoffrey Agar)"),
        K("sit_down", "S:aldous", "Sit down. I find most things go better sitting down."),
        K("paperwork", "S:aldous", "I don't make threats. I make sure people have read the paperwork."),
        K("properly", "S:aldous", "I prefer things done properly. It saves everybody so much trouble later."),
        K("moves", "S:aldous", "Slowly, and never seen to hurry. Waits for doors to be opened."),
    ],
    believes=[
        BN("hook_paper", "N-RIVALS", "The Hook's affairs are beneath a visit and reach him, if at all, as paper.",
           "Follows 'I make sure people have read the paperwork' and the outline's Act II, where his arm comes by paper (a letter, a licence, an inspection).", "unknown",
           NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        WN("read_fire", "N-RIVALS", "He read of the warehouse fire in the evening paper, as the town did.",
           "The paper called it arson (fire design); an alderman reads the evening paper.", "last November"),
    ],
    rumours=[
        pool("heart", ["fixer"], ["fixer"], ["died_heart"], "heard it from the Fixer"),
        pool("fire", ["street"], ["fixer"], ["fire", "read_fire"], "the paper's own word; he repeats nothing else", limits=["L2", "L1"],
             gist="The importer's warehouse at the far end of the old warehouse row burned down last November; the paper called it arson and nobody was charged."),
        pool("trade", ["fixer"], ["fixer"], ["trade"], "heard it from the Fixer"),
        rumour("Mickey died three weeks before his nephew came to Quay Street.", "true", H("SF", "Mickey died three weeks before the new owner, his nephew, came to Quay Street."), "a plain fact, held by the whole street",
               ["street"], ["fixer"], ["died_when"], ["L7"]),
        rumour("Mickey's, the minicab office, is on Quay Street in the Hook.", "true", H("SF", "Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside."), "a plain fact",
               ["street"], ["fixer"], ["office"], []),
    ],
    questions=[
        Q("Who are you?", "answers", "Geoffrey Agar. I'm a solicitor, and an honorary alderman.", ["solicitor"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "I make sure people have read the paperwork.", ["paperwork"], "firsts: What do you do here?"),
        Q("What is this place?", "answers", "Mickey's, I understand. The minicab office, on Quay Street in the Hook.", ["office"], "firsts: What is this place?"),
        Q("How did Mickey die?", "answers", "His heart, I understand. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("What happened at the warehouse fire?", "partly", "The paper called it arson, I understand. It started in two places. Nobody was charged.", ["fire", "read_fire"], "fresh: What happened at the warehouse fire?"),
        Q("Who can I trust?", "deflect", "Sit down. I find most things go better sitting down.", ["sit_down"], "firsts: Who can I trust?"),
        Q("Did Mickey have any enemies?", "deflect", "I don't make threats. I make sure people have read the paperwork.", ["paperwork"], "fresh: Did Mickey have any enemies?"),
        Q("Is there any money in the business?", "partly", "I'm told it has not made much since the docks went. Trade has been thin.", ["trade"], "firsts: Is there any money in the business?"),
        Q("What do people say about me?", "dont_know", "Nothing that reaches me. That's all I know.", [], "fresh: What do people say about me?"),
        Q("Who was Mickey's solicitor?", "dont_know", "I couldn't say. That's all I know.", [], "held: Who was Mickey's solicitor?"),
    ],
    schedule=PS(
        weekday=[(0, 9.5, "fairview_house"), (9.5, 13, "exchange_office"), (13, 14.5, "exchange_lunch"), (14.5, 17.5, "exchange_office"), (17.5, 24, "fairview_house")],
        saturday=[(0, 10, "fairview_house"), (10, 12.5, "exchange_office"), (12.5, 24, "fairview_house")], sunday=[(0, 24, "fairview_house")],
        note=WHY_NEW_ROUTINE + " Never on Quay Street at the baseline: the Exchange is canon's district of offices and lawyers, Fairview its residential hills."),
    extra={"ties_new": [
        {"who": "fixer", "weight": None, "band": "the broker he uses", "meets": "the Fixer brokers between all three rivals (canon)", "hours_a_week": None,
         "source": SQ("CANON", "the Fixer, Keith Garbutt (broker between all three rivals)")},
    ]},
))

# =============================================================== MAUREEN JENSEN, "THE WIDOW" (sera)
PEOPLE.append(person(
    "sera", "Maureen Jensen", "the Widow", "principal", 57,
    role=("CASTING", "head of the dockside syndicate"),
    identity=("CASTING", "**Maureen Jensen, \"the Widow\"** | 57"),
    street=["died_when", "died_heart", "fire", "office", "trade"], knew_mickey=False,
    internal_id_note="'sera' is the internal id (the voice file says kest); the old name Sera Kest survives only as an id.",
    knows=[
        K("called_widow", "CANON", "the dockside syndicate (muscle and smuggling, head Maureen Jensen, called the Widow)"),
        K("hook_family", "S:sera", "A fishing family of the Hook"),
        K("trawler_widow", "S:sera", "a trawler-owner's widow."),
        K("counts", "S:sera", "I've learned to count. You'd be surprised how few round here have."),
        K("no_surprises", "S:sera", "I don't like surprises, love. I've had enough of them for one life."),
        K("what_you_do", "S:sera", "I'm not interested in what you are. I'm interested in what you'll do."),
        K("receives", "S:sera", "She hardly does: people come to her. Sits facing the door."),
        K("her_people", "EMP", "Joey (dock hand), Ferko (night cab)", secret=True, via="the dockside syndicate's people on the street (empire roster, faction table); the sheet makes Ferko the day driver"),
    ],
    believes=[
        BN("show_me", "N-RIVALS", "Whoever has inherited Mickey's has yet to show her what he will do; she is interested in that, not in what he is.",
           "From her sheet line 'I'm interested in what you'll do.'", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        W("door_watch", "S:sera", "She hardly does: people come to her. Sits facing the door.", "every day, in her dockside room"),
    ],
    rumours=[
        pool("heart", ["fixer"], ["fixer"], ["died_heart"], "heard it from the Fixer"),
        pool("fire", ["street"], ["fixer"], ["fire"], "the paper's word and street talk; she says nothing of it herself", limits=["L2", "L1"]),
        pool("trade", ["joey"], ["fixer"], ["trade"], "heard it from her people on the street", limits=["L5"]),
        rumour("Mickey died three weeks before his nephew came to Quay Street.", "true", H("SF", "Mickey died three weeks before the new owner, his nephew, came to Quay Street."), "a plain fact",
               ["street"], ["fixer"], ["died_when"], ["L7"]),
        rumour("Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside.", "true", H("SF", "Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside."), "a plain fact",
               ["street"], ["fixer"], ["office"], []),
    ],
    questions=[
        Q("Who are you?", "answers", "Maureen Jensen. They call me the Widow.", ["called_widow"], "firsts: Who are you?"),
        Q("What do you do?", "deflect", "I count, love. You'd be surprised how few round here have.", ["counts"], "firsts: What do you do here?"),
        Q("Who runs things round here?", "deflect", "People come to me, love. I don't go to them.", ["receives"], "firsts: Who runs things round here?"),
        Q("What happened at the warehouse fire?", "partly", "The paper called it arson. Nobody was charged. I don't like surprises, love.", ["fire", "no_surprises"], "fresh: What happened at the warehouse fire?"),
        Q("How did Mickey die?", "answers", "His heart, I hear. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("What was Mickey like?", "deflect", "I'm not interested in what he was. I'm interested in what you'll do.", ["what_you_do"], "firsts: What was Mickey like?"),
        Q("Is there any money in the business?", "partly", "Not much, I hear, since the docks went. Trade has been thin.", ["trade"], "firsts: Is there any money in the business?"),
        Q("Did Mickey leave me anything?", "dont_know", "No idea. That's all I know.", [], "firsts: Did Mickey leave me anything?"),
        Q("What do people say about me?", "dont_know", "Nothing to me yet. That's all I know.", [], "fresh: What do people say about me?"),
        Q("Who can I trust?", "deflect", "I've learned to count, love. You'd be surprised how few round here have.", ["counts"], "firsts: Who can I trust?"),
    ],
    schedule=PS(
        weekday=[(0, 6.5, "jensen_house"), (6.5, 7.5, "fish_dock"), (7.5, 9.5, "jensen_house"), (9.5, 17.5, "dock_room"), (17.5, 24, "jensen_house")],
        saturday=[(0, 6.5, "jensen_house"), (6.5, 7.5, "fish_dock"), (7.5, 9.5, "jensen_house"), (9.5, 13, "dock_room"), (13, 24, "jensen_house")], sunday=[(0, 24, "jensen_house")],
        note=WHY_NEW_ROUTINE + " The fish dock at the morning's selling (shop-hours note: auction about 7 to 7.30), then people come to her."),
    extra={"ties_new": [
        {"who": "joey", "weight": None, "band": "one of her people on the street", "meets": "empire roster, faction table", "hours_a_week": None,
         "source": SQ("EMP", "| Dockside syndicate | Sera Kest | Joey (dock hand), Ferko (night cab) |")},
        {"who": "ferko", "weight": None, "band": "one of her people on the street", "meets": "empire roster, faction table (it calls him the night cab)", "hours_a_week": None,
         "source": SQ("EMP", "| Dockside syndicate | Sera Kest | Joey (dock hand), Ferko (night cab) |")},
        {"who": "fixer", "weight": None, "band": "the broker she uses", "meets": "the Fixer brokers between all three rivals (canon)", "hours_a_week": None,
         "source": SQ("CANON", "the Fixer, Keith Garbutt (broker between all three rivals)")},
    ]},
))

# =============================================================== DANNY CAMMACK (danny)
PEOPLE.append(person(
    "danny", "Danny Cammack", "Danny Cammack", "principal", 27,
    role=("CASTING", "head of the new crew"),
    identity=("CASTING", "**Danny Cammack** | 27"),
    street=["died_when", "died_heart", "fire", "office", "trade"], knew_mickey=False,
    internal_id_note="'danny' is the internal id (the old name Danny Ro survives only as an id).",
    knows=[
        K("flashy", "S:danny", "Heads the new crew: flashy and reckless (canon); loud money (CASTING.md)."),
        K("hurry", "S:danny", "Always in a hurry, me. Somebody's got to be."),
        K("stood_next", "S:danny", "You want to watch who you stand next to round here. You're stood next to me."),
        K("moves", "S:danny", "Fast. Takes up room, talks with his hands, never quite still; sits on tables rather than chairs."),
        K("fence", "EMP", "Rita (the back-room fence)", secret=True, via="the new crew's person on the street (empire roster, faction table)"),
    ],
    believes=[
        B("old_men", "S:danny", "Old men and their arrangements. It's 1990, mate. Nobody asks permission any more.", "unknown",
          NOTE("His view of the old organisations; the story's Act II tests it and nothing at the baseline settles it.")),
    ],
    saw=[
        W("room", "S:danny", "Fast. Takes up room, talks with his hands, never quite still; sits on tables rather than chairs.", "every day, in the Parade's pavements and rooms"),
    ],
    rumours=[
        pool("heart", ["fixer"], ["fixer"], ["died_heart"], "heard it from the Fixer"),
        pool("fire", ["street"], ["fixer"], ["fire"], "the paper's word and street talk", limits=["L2", "L1"]),
        pool("trade", ["rita"], ["fixer"], ["trade"], "heard it from Rita, his fence", limits=["L5"]),
        rumour("Mickey died three weeks before his nephew came to Quay Street.", "true", H("SF", "Mickey died three weeks before the new owner, his nephew, came to Quay Street."), "a plain fact",
               ["street"], ["fixer"], ["died_when"], ["L7"]),
        rumour("Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside.", "true", H("SF", "Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside."), "a plain fact",
               ["street"], ["fixer"], ["office"], []),
    ],
    questions=[
        Q("Who are you?", "answers", "Danny Cammack, mate. Always in a hurry. Somebody's got to be.", ["hurry"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "I head the new crew, mate. Flashy and reckless, they say. Loud money.", ["flashy"], "firsts: What do you do here?"),
        Q("What is this place?", "answers", "Mickey's, mate. The cab office on Quay Street. Old men and their arrangements.", ["office", "old_men"], "firsts: What is this place?"),
        Q("How did Mickey die?", "answers", "His heart, I heard. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("What happened at the warehouse fire?", "partly", "Importer's warehouse, last November. Paper said arson. Nobody was charged.", ["fire"], "fresh: What happened at the warehouse fire?"),
        Q("Who runs things round here?", "deflect", "Nobody asks permission any more, mate. It's 1990.", ["old_men"], "firsts: Who runs things round here?"),
        Q("Who can I trust?", "deflect", "You want to watch who you stand next to round here. You're stood next to me.", ["stood_next"], "firsts: Who can I trust?"),
        Q("Is there any money in the business?", "partly", "Not much, mate, since the docks went. Trade's been thin.", ["trade"], "firsts: Is there any money in the business?"),
        Q("What do people say about me?", "dont_know", "Nothing to me yet, mate. That's all I know.", [], "fresh: What do people say about me?"),
        Q("Did Mickey leave me anything?", "dont_know", "No idea, mate. That's all I know.", [], "firsts: Did Mickey leave me anything?"),
    ],
    schedule=PS(
        weekday=[(0, 2, "parade_district"), (2, 13, "danny_flat"), (13, 24, "parade_district")],
        saturday=[(0, 3, "parade_district"), (3, 13, "danny_flat"), (13, 24, "parade_district")], sunday=[(0, 2, "parade_district"), (2, 14, "danny_flat"), (14, 24, "parade_district")],
        note=WHY_NEW_ROUTINE + " Never on Quay Street at the baseline: canon makes the Parade the nightlife district. Act II's noise on Quay Street is the story's, not his daily round."),
    extra={"ties_new": [
        {"who": "rita", "weight": None, "band": "his fence on the street", "meets": "empire roster, faction table", "hours_a_week": None,
         "source": SQ("EMP", "| The New crew | Danny Ro | Rita (the back-room fence) |")},
        {"who": "fixer", "weight": None, "band": "the broker he uses", "meets": "the Fixer brokers between all three rivals (canon)", "hours_a_week": None,
         "source": SQ("CANON", "the Fixer, Keith Garbutt (broker between all three rivals)")},
    ]},
))

# =============================================================== KEITH GARBUTT, THE FIXER (fixer)
PEOPLE.append(person(
    "fixer", "Keith Garbutt", "the Fixer", "principal", 48,
    role=("CASTING", "brokers between all three rivals"),
    identity=("CASTING", "**Keith Garbutt, the Fixer** | 48"),
    street=["died_when", "died_heart", "fire", "will", "office", "trade"], knew_mickey=False,
    internal_id_note="No internal id found; 'fixer' is proposed (the sheet folder is the-fixer).",
    knows=[
        K("brokers", "S:fixer", "Brokers between the old-money machine, the dockside syndicate and the new crew (canon)."),
        K("of_the_town", "S:fixer", "Of the town; nobody can say which side he started on, which is the point of him."),
        K("percentage", "S:fixer", "I don't take sides. I take a percentage. It's a more honest arrangement."),
        K("first", "S:fixer", "Everybody wants the same thing. They just want it first."),
        K("what_you_need", "S:fixer", "Say what you need. Whether I can help is another conversation."),
        K("moves", "S:fixer", "Calm; sits with his back to a wall; never raises his voice; lights other people's cigarettes before his own."),
    ],
    believes=[
        B("want_first", "S:fixer", "Everybody wants the same thing. They just want it first.", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        W("wall", "S:fixer", "Calm; sits with his back to a wall; never raises his voice; lights other people's cigarettes before his own.", "every meeting he makes"),
    ],
    rumours=[
        pool("heart", ["street"], ["aldous", "sera", "danny"], ["died_heart"], "street talk; the doctor's word"),
        pool("nephew", ["street"], ["aldous", "sera", "danny"], ["will"], "street talk and the will", limits=["L7"]),
        pool("fire", ["street"], ["aldous", "sera", "danny"], ["fire"], "the paper's word and street talk", limits=["L2", "L1"]),
        pool("trade", ["street"], ["aldous", "sera", "danny"], ["trade"], "street talk", limits=["L5"]),
        rumour("Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside.", "true", H("SF", "Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside."), "a plain fact",
               ["street"], ["aldous", "sera", "danny"], ["office"], []),
    ],
    questions=[
        Q("Who are you?", "answers", "Keith Garbutt. Most call me the Fixer.", ["job"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "I don't take sides. I take a percentage. It's a more honest arrangement.", ["percentage"], "firsts: What do you do here?"),
        Q("What is this place?", "answers", "Mickey's, the minicab office, on Quay Street in the Hook.", ["office"], "firsts: What is this place?"),
        Q("How did Mickey die?", "answers", "His heart, the doctor said. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("What happened at the warehouse fire?", "partly", "Importer's warehouse, last November. The paper called it arson. Nobody was charged.", ["fire"], "fresh: What happened at the warehouse fire?"),
        Q("Who can I trust?", "deflect", "Everybody wants the same thing. They just want it first.", ["first"], "firsts: Who can I trust?"),
        Q("Who runs things round here?", "deflect", "Say what you need. Whether I can help is another conversation.", ["what_you_need"], "firsts: Who runs things round here?"),
        Q("Is there any money in the business?", "partly", "Not much, I hear, since the docks went. Trade has been thin.", ["trade"], "firsts: Is there any money in the business?"),
        Q("Did Mickey leave me anything?", "answers", "The office, I hear. He left it to his nephew by his will.", ["will"], "firsts: Did Mickey leave me anything?"),
        Q("What do people say about me?", "dont_know", "Nothing to me yet. That's all I know.", [], "fresh: What do people say about me?"),
    ],
    schedule=PS(
        weekday=[(0, 9, "off"), (9, 11, "garbutt_room"), (11, 12.5, "exchange_lunch"), (12.5, 14, "garbutt_room"), (14, 16, "dock_room"), (16, 17.5, "garbutt_room"), (17.5, 19.5, "parade_district"), (19.5, 24, "off")],
        saturday=[(0, 10, "off"), (10, 12, "garbutt_room"), (12, 24, "off")], sunday=[(0, 24, "off")],
        note=WHY_NEW_ROUTINE + " He calls on each of the three in turn: the Exchange, the docks and the Parade."),
    extra={"ties_new": [
        {"who": "aldous", "weight": None, "band": "one of the three he brokers between", "meets": "canon", "hours_a_week": None, "source": SQ("CANON", "the Fixer, Keith Garbutt (broker between all three rivals)")},
        {"who": "sera", "weight": None, "band": "one of the three he brokers between", "meets": "canon", "hours_a_week": None, "source": SQ("CANON", "the Fixer, Keith Garbutt (broker between all three rivals)")},
        {"who": "danny", "weight": None, "band": "one of the three he brokers between", "meets": "canon", "hours_a_week": None, "source": SQ("CANON", "the Fixer, Keith Garbutt (broker between all three rivals)")},
    ]},
))

# =============================================================== PHILIP DANBY (elias)
PEOPLE.append(person(
    "elias", "Philip Danby", "Philip", "principal", 33,
    role=("CASTING", "a teacher at the comprehensive, which stands closed for the game's window"),
    identity=("CASTING", "**Philip Danby** | 33"),
    street=["died_when", "died_heart", "fire", "will", "funeral", "june", "trade", "office", "cafe"], knew_mickey=False,
    internal_id_note="No internal id found in the code; 'elias' is proposed (the sheet says he was Elias until 24 September).",
    knows=[
        K("local", "S:elias", "Local; went away to train and came back."),
        K("own_days", "S:elias", "so his days are his own."),
        K("time", "S:elias", "I've more time than I know what to do with just now."),
        K("walk", "S:elias", "I walk. It's that or sit indoors watching the rain."),
        K("notice", "S:elias", "You notice things when you're not in a hurry. I'm never in a hurry now."),
        K("moves", "S:elias", "Walks a great deal; carries a paperback or the paper; stands a little too close when he is interested and steps back when he notices."),
    ],
    believes=[
        BN("quiet_street", "N-LIVES", "The street is quiet enough now that anything out of the ordinary is noticed.",
           "Follows 'You notice things when you're not in a hurry' (sheet) and the street's thin trade.", "unknown", NOTE("A stance, not a fact about the world.")),
    ],
    saw=[
        W("walks_seen", "S:elias", "Walks a great deal; carries a paperback or the paper; stands a little too close when he is interested and steps back when he notices.", "most days, with the school shut"),
    ],
    rumours=[
        pool("heart", ["street"], ["noor", "sam"], ["died_heart"], "street talk; the doctor's word"),
        pool("nephew", ["ada"], ["noor", "sam"], ["will"], "heard it from Ada", limits=["L7"]),
        pool("fire", ["street"], ["noor", "sam"], ["fire"], "the paper's word and street talk", limits=["L2", "L1"]),
        pool("june", ["street"], ["noor"], ["june"], "street talk"),
        pool("trade", ["street"], ["sam", "noor"], ["trade"], "street talk", limits=["L5"]),
    ],
    questions=[
        Q("Who are you?", "answers", "Philip Danby. I'm a teacher at the comprehensive, but it's shut, so my days are my own.", ["job", "own_days"], "firsts: Who are you?"),
        Q("What do you do?", "answers", "I walk. It's that or sit indoors watching the rain.", ["walk"], "firsts: What do you do here?"),
        Q("What is this place?", "answers", "Mickey's, the minicab office, on Quay Street in the Hook. The rank's outside.", ["office"], "firsts: What is this place?"),
        Q("How did Mickey die?", "answers", "His heart, I heard. Ron found him at the office early one morning, when he came on at the rank.", ["died_heart"], "firsts: How did Mickey die?"),
        Q("What happened at the warehouse fire?", "partly", "Last November, a Saturday night. The paper called it arson, since it started in two places. Nobody was charged.", ["fire"], "fresh: What happened at the warehouse fire?"),
        Q("Where can I get something to eat?", "answers", "The cafe's over the road, in the shops across from the north end of the parade. Half past six till ten, and eight till twelve on a Sunday.", ["cafe"], "firsts: Where can I get something to eat?"),
        Q("Is June still about?", "answers", "She's still in town. She came back for the funeral and wants nothing from the office.", ["june"], "fresh: Is June still about?"),
        Q("Who's the priest round here?", "partly", "Father Walsh, I think. Mickey's funeral was at his chapel.", ["funeral"], "fresh: Who's the priest round here?"),
        Q("What's the street like after dark?", "dont_know", "I couldn't tell you. That's all I know.", [], "held: What's the street like after dark?"),
        Q("Who was Mickey closest to?", "dont_know", "No idea. That's all I know.", [], "fresh: Who was Mickey closest to?"),
    ],
    schedule=PS(
        weekday=[(0, 8.5, "off"), (8.5, 9.5, "cafe"), (9.5, 12, "quay"), (12, 13, "kiosk"), (13, 16, "allotments"), (16, 18, "quay"), (18, 24, "off")],
        saturday=[(0, 9, "off"), (9, 11, "cafe"), (11, 13, "market"), (13, 24, "off")], sunday=[(0, 10, "off"), (10, 13, "allotments"), (13, 24, "off")],
        note=WHY_NEW_ROUTINE + " He walks: the cafe, the quay, the kiosk for the paper, the allotments by the railway; the school stands closed (canon)."),
))
