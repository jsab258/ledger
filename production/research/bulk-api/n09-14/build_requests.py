"""Builds production/research/bulk-api/n09-14/REQUESTS.jsonl from the sources, quoted, not retyped (n09-14)."""
import json, os, re

ROOT = r"C:\Users\Jafar\ledger-local"
FACTS = r"F:\LedgerTools\checkers\claim-labels-2026-11-03\requests.jsonl"
OUT = os.path.join(ROOT, "production", "research", "bulk-api", "n09-14", "REQUESTS.jsonl")
MODEL = "claude-sonnet-5-5"


def rd(*p):
    return open(os.path.join(ROOT, *p), encoding="utf-8").read()


def section(text, head, stop_prefix="## "):
    i = text.index(head)
    j = text.find("\n" + stop_prefix, i + len(head))
    return text[i: j if j > 0 else len(text)].strip()


canon = rd("canon.md")
outline = rd("game-design", "story-outline-2026-09-28.md")
rulings = rd("RULINGS.md")
side = rd("game-design", "side-stories-2026-11-08.md")
regulars = rd("production", "casting", "regulars", "REGULARS.md")

CANON = "\n\n".join(section(canon, h) for h in
                    ("## Game", "## Era", "## Tone", "## Premise and cast", "## The content rule", "## What LEDGER is not"))
# the content rule's enforcement paragraph is about tooling, not the world: cut it
CANON = re.sub(r"\nEnforced at six sites:.*?claim to\.\n?", "\n", CANON, flags=re.S)
OUTLINE = "\n\n".join(section(outline, h) for h in
                      ("## The spine", "## Arrival", "## Act I", "## Act II", "## Act III", "## Rules the writing keeps"))
STORY_RULINGS = section(rulings, "## The story and the first week")

COMMON = """You write design text for LEDGER, a single-player third-person crime game on PC, set in Meridian, a fictional British port town, in 1990 (the working window is 1988 to 1992). The game is set in 1990: judge every date, price, object and turn of phrase as of 1990, never as of today. What follows is the project's canon, which outranks everything, then the approved story outline and the producer's story rulings. Write only within them.

=== CANON (canon.md, approved; outranks everything) ===
""" + CANON + """

=== THE APPROVED STORY OUTLINE (28 September; abridged to its story sections) ===
""" + OUTLINE + """

=== THE PRODUCER'S STORY RULINGS (RULINGS.md) ===
""" + STORY_RULINGS + """
- 29 Sep (DECISIONS, within canon): the outfit Mickey worked for is somebody else's, not one of the three rivals, and stays unnamed; its man waits at the ferry landing. Ron carries its ask to Tom on the first night and every other night after; refusing ends Mickey's arrangement for good, and nothing ends the game.

=== RULES FOR EVERYTHING YOU WRITE ===
- Canon outranks everything. Any fact that does not follow from the sources given here is an invention: mark it, at the end of the sentence that states it, with [invented]. Never present an invention as settled; the producer checks every [invented] mark. Prefer few, small, ordinary inventions to many or dramatic ones.
- The content rule, absolutely: no alcohol and no gambling of any kind, never shown, served, drunk or spoken of (no pubs as places to drink, no bets, raffles, pools, bingo or horses); tobacco is allowed. NO CHILDREN ANYWHERE: no child, baby, schoolchild or childhood scene appears or is spoken of; every person in the text is an adult; no one is shown with young children. No sexual content (seaside-postcard innuendo at most). Drugs only as an off-screen economy others run. No slurs of any kind; racism may be a fact about a character, never voiced. Religion never mocked. Police corruptible only as individuals.
- No real people, brands, firms, newspapers, bands, clubs, products, vehicle models or real towns and streets. Use Meridian's own names (its districts: the Hook, Copper Row, the Exchange, the Parade, Fairview, Ironside, Gullwing; Quay Street, Weighhouse Lane, Tannery Row; the Tivoli; Meridian Harbour Board; Meridian Ferry). A place outside Meridian is described, never named ("a shipyard town up the coast"), and marked [invented].
- Period: late-analog Britain. Landlines, phone boxes, pagers for a few, cash and paper; no mobiles in ordinary pockets, no internet. The dock labour scheme ended in July 1989 and more than half the registered dockers' jobs went; say that it happened, never explain why the docks went.
- Leave open what canon leaves open: the truth of the warehouse fire, what Mickey's real book holds, who the outfit is, who the stranger in the yard was, how the story ends. Tom Nowak's life before the Hook is never told: nobody in Meridian knows it, and you must not invent it.
- Mickey's is a minicab office (never a pub, never a former pub). Mickey (Michael Suddaby) died of his heart at the office early one morning three weeks before Tom came; Ron found him; nobody thinks otherwise.
- Names: nobody on the street addresses or names Tom by name in a quoted line (never "Mr Nowak"); what each person calls him is decided by the game, by how well they know him. In quoted speech, write around his name.
- British English, 1990 usage, plain and concrete; grounded noir with dry British wit, never American satire. Third person throughout."""

BACK = COMMON + """

=== YOUR TASK: ONE PERSON'S BACKSTORY ===
Write the backstory of the one person named in the message, for the writers and the live-talk briefing: 600 to 900 words of prose, third person, past tense for the past and present tense for 1990. Start the life at about eighteen (no childhood, no school days). Cover: where they came from, in described (unnamed) places; their work and how they came to Mickey's; Mickey as they knew him; the people of Quay Street they are close to; what 1989 and the end of the dock labour scheme did to them, if it touched them; their habits, their day and their week as the game runs them; what they want and fear now, three weeks after Mickey's death, with a stranger owning the office. Everything must agree with the person's card, casting sheet, the game's fact list and routine given in the message, and with the side-story facts listed there; it must not reveal or pre-empt a side story's turn or a main-story beat.
Mark every invention [invented]. Where two sources disagree, follow the one the message says to follow and do not hide the disagreement.
After the prose, two short lists:
INVENTIONS: one line each, every [invented] fact, in a few words.
GAPS: one line each, anything the sources leave open or contradict that a writer will trip on, with what you did about it.
Nothing else: no title, no preamble."""

regular_rows = [l for l in regulars.splitlines() if re.match(r"^\| \d+ \|", l)]
ROSTER = "\n".join("- " + " | ".join(c.strip() for c in l.strip("|").split("|")[2:5]) + " | " +
                   l.strip("|").split("|")[7].strip() for l in regular_rows)
RULES_EVERY = section(side, "## The rules every story keeps")
TEMPLATE = section(rd("production", "research", "aaa-reference", "studies", "16-jobs-story.md"),
                   "**The job template (for the builder).**", "**Targets")

OUTL = COMMON + """

=== THE STREET'S THIRTY REGULARS (approved casting sheets: name | age | who and where | manner) ===
""" + ROSTER + """

Principals beside them (canon): Ron Kirby (58, Mickey's door and rank), Sheila Dunn (53, Mickey's bookkeeper), Darren Milner (25, the street hustler, owes the office), Ada (the widow at her window on Quay Street), June Suddaby (Mickey's estranged daughter, still in town after the funeral), DS Carol Ellis, Father Brendan Walsh (Father Walsh to the street), Alison Sedman (journalist), Philip Danby (teacher), Keith Garbutt (the Fixer), and the three rivals' heads (Geoffrey Agar, Maureen Jensen called the Widow, Danny Cammack) with their people.

=== SIDE STORIES: THE RULES EVERY STORY KEEPS (the approved draft of 8 November) ===
""" + RULES_EVERY + """
- Nothing in a side story carries a main-story beat or names Act III, the inspection, the warehouse fire, Mickey's real book, the sit-down or the endings; no side story uses Ellis's Act III trade ("give her a rival, at the price that the street learns who talks"). Boats are scenery: never bought, sold, owned or lost as an item. Tom never drives.

=== THE JOB TEMPLATE THE BUILDER WILL USE (study 16, Kingdom Come II's method) ===
""" + TEMPLATE + """

=== YOUR TASK: ONE SIDE STORY'S OUTLINE ===
The message gives one side story as approved in the draft, with when it is offered and how long its giver waits. Expand it into a builder's outline of 150 to 250 words that keeps every person, place, ending and town-keeps line it already has, and changes none of them. Use exactly these headings, each a short line or two:
FOUND: how Tom stumbles on it, the giver's own words naming the place by a landmark.
OFFERED / WAITS: as given.
STEPS: 3 to 5 numbered steps; each names the place by a landmark, who is there, and what Tom can do.
ENDINGS: each ending, what Tom does, and what the town keeps (who knows, says or remembers what).
IF IT GOES WRONG: the failure that continues into a world state the town can talk about.
LEDGER LINES: two sample lines of about 22 words for Tom's notebook, naming person and place by a landmark.
INVENTIONS: every detail not in the given entry, one line each, marked [invented]; "none" if none.
Nothing else: no title, no preamble."""


def card(idn):
    t = rd("production", "cast", "cards", idn + ".md")
    return t.split("## Their Own Words")[0].strip()


def sheet(slug):
    t = rd("production", "casting", slug, "SHEET.md")
    rows = [l for l in t.splitlines() if l.startswith("| **")]
    lines = section(t, "## Three lines").split("Spoken by")[0].strip()
    return "\n".join(rows) + "\n\n" + lines


facts = {}
for l in open(FACTS, encoding="utf-8"):
    m = json.loads(l)["messages"][0]["content"].split("THE DETAIL:")[0]
    name = re.search(r"Their own name is ([A-Z][a-z]+ [A-Z][a-z]+)", m).group(1)
    if name not in facts:
        keep = [x for x in m.splitlines() if re.match(r"^(C|H|P)\d+:", x)
                and "Here with you now" not in x and "The street's places" not in x]
        facts[name] = "\n".join(keep).replace(" \ufffd ", ", ").replace("Somebody or somewhere on the street they know: ", "Knows: ")

cast = json.load(open(os.path.join(ROOT, "production", "specs", "hook-cast.json"), encoding="utf-8"))
routine = {p["id"]: {"routine": p["routine"], "days": p.get("days", {})} for p in cast["people"]}

PEOPLE = [
    ("ron", "Ron Kirby", "rocco", "ron-kirby", [
        "Story 4: Mickey and Ron shared a Friday order at the Tangs' takeaway, two of number nine, every Friday; asked, Ron goes quiet, then says \"Fridays, aye.\"",
        "Story 25: Mickey's watch went into Rita's pawn the week he died; it was Ron who pawned it, to pay for the funeral flowers. Nobody has been told. The backstory may hold this as a private fact but must not resolve how Tom learns it.",
        "Story 27: Ron is the man the boarding house would expect to send to have a word with a lodger behind on his rent.",
        "Story 12: Ron may stand at the takeaway's counter at closing on Tom's word.",
    ], "Sources disagree on Ron's years at the docks: his card and the game's fact list say thirty years (follow these); his casting sheet's first sample line says \"Forty years on the docks\". Say thirty and name the disagreement under GAPS. Sheila saw Ron argue with a stranger in the yard behind the office two nights before Mickey died (her fact, not his): do not explain it, name the stranger or give its cause; Ron's backstory may not mention it at all."),
    ("sheila", "Sheila Dunn", "lena", "sheila-dunn", [
        "Story 1: Sheila keeps the day book and the fare book; she will see if Tom quietly pays a driver's shortfall.",
        "Story 9: Sheila marks in the book any money the office pays out.",
        "Story 24: Edith Stockill, at the newsagent's pension counter, trusts Sheila's judgement of people.",
        "Story 29: Mickey quietly paid the difference when Ada's landlord raised her rent, without Ada knowing; Sheila knew and admits it if asked.",
    ], "Sheila came to Mickey's at 22 (1959), thirty-one years ago, but the word \"minicab\" and minicab firms date from about 1961: if Mickey's was something else in 1959 (a car-hire or private-hire firm, never a pub), say so, mark it [invented] and name it under GAPS. She saw Ron argue with a stranger in the yard two nights before Mickey died: she knows only what she saw; do not explain it. She withholds Tom's name until she trusts him, as she promised Mickey. Where the real book is stays unsaid."),
    ("darren", "Darren Milner", "sam", "darren-milner", [
        "Story 3: Darren has sometimes slept across the back seat of Mickey's spare car in the yard (his casting sheet says he lives at his mother's: reconcile, and name it under GAPS).",
        "Story 13: Darren turns up with a crate of transistor radios of a made-up maker; he owes Mickey's money already (the outline: \"friendly and owing\").",
        "Story 3: he talks about whoever treats him well or hard; the parade hears it from him.",
    ], "His casting sheet's sample line names a real town (\"a lift to Grimsby\"): never name a real town. He was on a youth training scheme after leaving school (dates from 1983 fit a man born 1965); start his life at about eighteen. His voice is a young northern Englishman's; do not name the town he came from."),
]

DAYNAMES = {"mon": "Monday", "tue": "Tuesday", "wed": "Wednesday", "thu": "Thursday", "fri": "Friday", "sat": "Saturday", "sun": "Sunday"}


def plain_routine(r):
    def one(lst):
        return ", ".join("%02d:00 %s" % (h, w.replace("_", " ")) for h, w in lst)
    s = "Weekdays unless named: " + one(r["routine"])
    for d, lst in r["days"].items():
        s += "\n" + DAYNAMES[d] + ": " + one(lst)
    return s


reqs = []
for key, name, idn, slug, side_facts, conflicts in PEOPLE:
    msg = ("THE PERSON: " + name + "\n\n=== THEIR CARD (the live-talk card) ===\n" + card(idn) +
           "\n\n=== THEIR CASTING SHEET (approved as text) ===\n" + sheet(slug) +
           "\n\n=== WHAT THE GAME'S TALK TELLS THEM (their fact list as the game builds it) ===\n" + facts[name] +
           "\n\n=== THEIR ROUTINE IN THE SIMULATION (hour, place) ===\n" + plain_routine(routine[idn]) +
           "\n\n=== SIDE-STORY FACTS THAT TOUCH THEM (the approved draft of 8 November) ===\n- " + "\n- ".join(side_facts) +
           "\n\n=== SOURCE DISAGREEMENTS AND OPEN POINTS FOR THIS PERSON ===\n" + conflicts +
           "\n\nWrite " + name + "'s backstory now, 600 to 900 words, then INVENTIONS and GAPS.")
    reqs.append({"id": "backstory-" + key, "model": MODEL, "system": BACK,
                 "messages": [{"role": "user", "content": msg}], "max_tokens": 4000,
                 "thinking": {"type": "between_tools"}})

# try 2 (8 Nov): her casting sheet's own line, so the notice is not read as her years at the laundry
JULIE = ("\n\nFROM JULIE'S CASTING SHEET: she worked twelve years on the steam laundry's presses and was given twelve weeks' "
         "notice; her line: \"Twelve years on them presses and twelve weeks' notice. Generous, they called it.\"")
# try 2 (8 Nov): Sonnet 5.5 thinks by default and its hidden thinking spent try 1's max_tokens (32 of 35 cut off);
# "between_tools" is its documented way to turn thinking off (the claude-api skill, read 8 Nov 2026)
stories = re.findall(r"^\*\*(\d+)\. (.+?)\*\* (.+)$", side, flags=re.M)
table = {m.group(1): (m.group(2).strip(), m.group(3).strip())
         for m in re.finditer(r"^\| (\d+) \| (.+?) \| (.+?) \|$", side, flags=re.M)}
assert len(stories) == 32 and len(table) == 32, (len(stories), len(table))
for num, title, body in stories:
    when, waits = table[num]
    msg = ("THE SIDE STORY, as approved in the draft of 8 November:\n\n" + num + ". " + title + " " + body +
           "\n\nOFFERED WHEN: " + when + "\nWAITS: " + waits +
           (JULIE if num == "9" else "") + "\n\nWrite this story's outline now, 150 to 250 words, under the headings given.")
    reqs.append({"id": "side-%02d" % int(num), "model": MODEL, "system": OUTL,
                 "messages": [{"role": "user", "content": msg}], "max_tokens": 3000,
                 "thinking": {"type": "between_tools"}})

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    for r in reqs:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print(len(reqs), "requests;", "system chars: backstory %d, outline %d" % (len(BACK), len(OUTL)))
print("user chars:", [len(r["messages"][0]["content"]) for r in reqs[:3]], max(len(r["messages"][0]["content"]) for r in reqs[3:]))
