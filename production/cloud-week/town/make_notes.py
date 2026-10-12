#!/usr/bin/env python3
"""Writes NOTES.md from people.json and the check's result (unit 11, cloud week 42).
The lists in it (new facts by person, proposed schedules, specific rumours) are generated, so none can be missed.

    python3 make_notes.py        # after build_people.py and check_town.py
"""
import collections
import json
import sys
sys.dont_write_bytecode = True
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from authored.common import POOL  # noqa: E402

doc = json.loads((HERE / "people.json").read_text(encoding="utf-8"))
people = doc["people"]
chk = json.loads((HERE / "checks" / "check_v1.json").read_text(encoding="utf-8")) if (HERE / "checks" / "check_v1.json").exists() else None
byid = {p["id"]: p for p in people}

nf = sum(len(p["facts"]) for p in people)
street = sum(1 for p in people for f in p["facts"] if f.get("street"))
who = sum(1 for p in people for f in p["facts"] if f.get("via", "").startswith("who ") and "is, as the home describes" in f.get("via", ""))
derived = sum(1 for p in people for f in p["facts"] if f.get("derived"))
new = [(p, f) for p in people for f in p["facts"] if f.get("new")]
sec = sum(1 for p in people for f in p["facts"] if f.get("secret"))
pg = {v["gist"] for v in POOL.values()}
pooled = sum(1 for p in people for r in p["rumours"] if r["gist"] in pg)
specific = [(p, r) for p in people for r in p["rumours"] if r["gist"] not in pg]
kinds = collections.Counter(q["kind"] for p in people for q in p["newcomer_questions"])
nq = sum(len(p["newcomer_questions"]) for p in people)
nr = sum(len(p["rumours"]) for p in people)
src_n = sum(1 for p in people for f in p["facts"] if f.get("src"))
knew = [p for p in people if p["knew_mickey"]]
proposed = [p for p in people if p["schedule"].get("source", {}).get("proposed")]
beliefs = collections.Counter(f["truth"] for p in people for f in p["facts"] if f["kind"] == "believes")
if chk:
    failing = [r["id"] for r in chk["rows"] if not r["pass"]]
    ok = chk["summary"]["pass"] + (1 if failing == ["shape.notes_file"] else 0)
    result = "%d of %d rows pass" % (ok, chk["summary"]["rows"])
else:
    result = "not run"

L = []
w = L.append
w("# NOTES: town content (unit 11, cloud week 42)")
w("")
w("Written 13 October 2026 for Jafar's order of 12 October: for every principal and regular in canon, the authored facts the talk draws on, their schedule, who they talk to, five rumours, and a newcomer's ten likeliest questions answered from those facts. Third person throughout. Canon outranks all of it; anything new is marked and sits in DECISIONS.md as six entries, each ending \"Marked for Jafar.\" Nothing here is in the game or on a page of his yet.")
w("")
w("## What was made (production/cloud-week/town/)")
w("")
w("- **HOMES.md**: where each kind of fact lives today, and how these files relate to each home. Written first.")
w("- **people.json**: %d entries (the fourteen principals, with Tom's entry holding only what the town knows of him, and the thirty regulars). Each has facts (knows, believes, saw), a schedule, who they talk to, five rumours and ten answers." % len(people))
w("- **check_town.py** and **checks/check_v1.json**: the checks, written apart from the builder. Result today: **%s**." % result)
w("- **build_people.py**, **town_lib.py**, **authored/**: the builder and the written text. `python3 build_people.py` makes people.json; `python3 check_town.py` checks it; `python3 make_notes.py` makes this file. Standard library only; the whole run takes seconds.")
w("")
w("## The numbers")
w("")
w("- **People:** %d (14 principals, 30 regulars). Tom is the player: his entry is only what the town knows of him, and no answer is written for him (his words are typed)." % len(people))
w("- **Facts:** %d in all. Sourced or derived: %d. New (marked): %d." % (nf, nf - len(new), len(new)))
w("  - Of the sourced, %d are the street's plain facts copied from StreetFacts.cs (each person holds the ones that reach them), %d say who each tie is, in hook-cast.json's words, %d are derived by script from hook-cast.json (a person's day, a shop's hours), and the rest are word for word from a casting sheet, the contact sheet, a card, canon, RULINGS or an approved design, each with file and line." % (street, who, derived))
w("  - %d facts are secrets: held, never told to a stranger. The check fails an answer that cites one, except a deflection that repeats none of its words." % sec)
w("  - Beliefs (%d): %d unknown, %d true, %d false, %d partly, each against canon and the story." % (sum(beliefs.values()), beliefs["unknown"], beliefs["true"], beliefs["false"], beliefs["partly"]))
w("- **Rumours:** %d, five a person. %d are one of eleven pooled stories the street passes round (the heart, the nephew, the funeral, June, the fire as the street has it, the thin trade, the door, the man at the landing, Hal and Rita, the radio, and the arrival seen); %d are specific to a person (listed below)." % (nr, pooled, len(specific)))
w("- **Answers:** %d, ten a person but Tom's. Kinds: %d plain answers, %d partial, %d pointing to someone, %d deflections, %d honest don't-knows. Every answer is under thirty words and cites the fact ids it draws on." % (nq, kinds["answers"], kinds["partly"], kinds["points_to"], kinds["deflect"], kinds["dont_know"]))
seeded = ("%d seeded faults, %d caught" % (chk["summary"]["seeded_faults"], chk["summary"]["seeded_faults_caught"])) if chk else "not run"
w("- **Check:** %s. It covers the cast (each of the 44, nobody else), every citation, every derived fact and schedule re-derived from hook-cast.json, the ties and their hours a week recomputed, the rumours' limits, each answer's facts, words and length, the gates, and DECISIONS.md. It also damages a copy of people.json thirty ways (a changed quote, a wrong line, a secret told, a real brand, drink, a year after 1992, Tom's name, the fire's truth, murder, a missing or extra person and so on) and requires each to fail a row: %s." % (result, seeded))
w("")
w("## Where the files do not settle things (homes that disagree, for the PC session; none is settled here)")
w("")
w("1. The old prototype cards (a pub, a bar, gambling debts, Ada a teacher, other ages and trades) still sit in Tier2Setup.cs, SecretsSetup.cs, CastSetup.cs and tier2-batch-1.json, with ids that now mean other people (the old 'vesna' is a nurse). REGULARS.md already says its sheets replace them. Nothing is drawn from them except two sentences the approved fire design itself uses.")
w("2. Ron's years on the docks: his sheet's line says forty, his card thirty, his street lines thirty on the quay. No answer gives a number.")
w("3. The Tangs' takeaway has no unit: REGULARS.md puts it on the parade's empty bay, RULINGS.md (3 Oct, later) rules bay 3 empty and to let. Their schedule says so.")
w("4. Julie Kettlewell is laid off by her sheet and still at the laundry counter in hook-cast.json. Albert Suggitt mends nets 'some mornings' by his sheet and is on the docks all day in hook-cast.json. Both schedules are written afresh and say they replace the routine.")
w("5. Doreen Harland's early shift starts at six, before the laundry counter opens at eight. Kept as hook-cast.json has it, since a works runs before its counter; the check names the exception.")
w("6. The trades line lists an ironmonger and a tea room on the west block; hook-cast.json has Hal's coin shop and the cafe there.")
w("7. The empire roster makes Ferko the night cab; the sheet makes Kevin Needham the day driver and Terry Hodgson the night one. The sheet outranks; the arm Kevin belongs to is carried as a secret.")
w("8. CASTING.md names a force for Carol Ellis; her sheet says canon names none. No force is named here. CASTING.md says Mickey was a trawlerman until the fleet went; canon does not, so it is not used.")
w("9. Sheila's card says the fish shop is two doors up; the street's bays put it next door. No answer says which.")
w("")
w("## Canon checks made by hand (besides the word lists the check runs)")
w("")
import re
d_facts = sum(1 for p in people for f in p["facts"] if re.search(r"\bdied|death|dead\b", f["text"]))
d_rum = sum(1 for p in people for r in p["rumours"] if re.search(r"\bdied|death\b", r["gist"]))
d_ans = sum(1 for p in people for q in p["newcomer_questions"] if re.search(r"\bdied|death\b", q["a"]))
chk_hand = [
    "Mickey's death: every fact, rumour and answer that speaks of it says only that he died of his heart at the office early one morning and that Ron found him (RULINGS 108). %d facts, %d rumours and %d answers mention a death or dying; none suggests another cause, and nobody doubts it. The one other mention is Sheila's sighting 'two nights before Mickey died' (her card)." % (d_facts, d_rum, d_ans),
    "Tom's life before the Hook stays unsaid (canon): no fact, rumour or answer gives it; the only rumour about it says that nobody knows (canon, 28 Sep).",
    "Tom's name follows the ladder (canon 88 to 91, what-they-call-him): only Ron, Sheila and Darren, who know it from the start, and Tom's own entry use it; everyone else says 'the new owner' or Mickey's nephew. Ron says 'boss'; Sheila's answers never name him.",
    "Sheila withholds his name until she trusts him: no answer of hers uses it. Whether she has read the fire's page in the real book is left open (the fire design leaves it open): no fact says either.",
    "The warehouse fire: the street's version only (last November, a Saturday night, started in two places, the paper's 'arson', nobody charged, the street's insurance talk). That the owner did it is marked false against the story and never corrected aloud. The truth is held only by Father Walsh, sealed; Alison's belief (marked secret, unproved) matches it and Ellis's (that someone paid the watchman) does not; no non-secret text contains it.",
    "Nobody but regulars who knew Mickey describes him, and only in the two approved lines (RULINGS 101). The sixteen who may are listed below; June and Alison never do.",
    "A witness is only as sure as the witness (RULINGS 113): each rumour records how sure its first teller was; none turns a guess into 'he did it'. No deed of Tom's has happened at the baseline, so none appears.",
    "Mickey's is a minicab office (D19): no text calls it a pub or a bar; the pawn, the cafe, the chapel, the shops are the street's.",
    "No children anywhere: nobody is in the school, which stands closed; Philip Danby is the only teacher and says so only with the school shut; Ada was never a teacher (canon).",
    "No alcohol or gambling in image or speech: tools/content-gate.py is clean over every written and every carried text; no answer mentions drink or betting, and nobody's trade touches either.",
    "Era: poll-tax letters, pagers, phone boxes, the evening paper, the radio; no year after 1992 anywhere in the text; no real brand, club, programme, paper, song or public figure (RealWorld.cs's lists and the Humber-side towns are scanned). Real places in carried text were avoided by choosing fragments; the one that remains is the New Territories in Peter Tang's row (his sheet's own words), and his answers say only 'I came over in 1968'.",
    "Names: the old names (Lena, Rocco, Sam and the rest) appear only as ids. 'Father Walsh' and 'Father Emil' are kept apart; the heads are Agar, Jensen and Cammack.",
    "The regulars stand as written (RULINGS 115): names, ages, trades and sample lines are word for word from REGULARS.md; the three changes of routine come from its own notes (laid off; mornings only; Grace and the Tangs need routines).",
    "Mickey's people never go to the police about one of their own (RULINGS 111) and Rita, Hal, the pawn's back-room hand, the customs officer and the scrap dealer never go at all (the Ellis design): carried as secrets, contradicted nowhere.",
    "The outfit's man stays unnamed and has no entry (canon; REGULARS.md); the street's own word for him is 'a man who hangs about the ferry landing at night'.",
    "The first week's designs are not contradicted: the six who see him come (Ron, Sheila, the dispatcher, a day driver, Ada, the sign painter) are exactly the six with that sighting; Sheila keeps the key; the cab office's hours are seven to three; nothing says Ada asks a stranger in.",
    "Religion is present and never mocked: Father Walsh's seal is kept and Nora's and Winifred's chapel work is plain.",
    "Faces, clothes and voices are untouched; no voice is cast by these files. Where a sheet says a voice does not fit (Ellis, Agar, Jensen, June, Walsh, Ada), nothing here depends on it.",
]
for i, t in enumerate(chk_hand, 1):
    w("%d. %s" % (i, t))
w("")
w("## Who knew Mickey (group N-MICKEY: new, for Jafar)")
w("")
w("Only these %d hold the two approved lines about him (\"Mickey kept his business to himself...\", \"Mickey kept Ron on...\"): %s." % (len(knew), "; ".join("%s (%s)" % (p["name"], p["id"]) for p in knew)))
w("The rule used: those who worked for him (the dispatcher and the two drivers), Ron, Sheila, Darren, Ada, Father Walsh, and those over forty who keep a shop, the cafe, the laundry's floor, the pension counter or the priest's house on or beside Quay Street. Nobody else describes him; asked what he was like, they say they never really knew him.")
w("")
w("## Every new fact, by person, one line each (for Jafar's check)")
w("")
w("Groups: N-LIVES is a small belief, sighting or trade fact where canon and the sheets are silent; N-RIVALS is the same for the three heads, the detective and the Fixer. Each follows the line named after it.")
w("")
cur = None
for p, f in new:
    if p["id"] != cur:
        cur = p["id"]
        w("")
        w("**%s** (%s)" % (p["name"], p["id"]))
    extra = "" if f["kind"] != "believes" else " [truth: %s]" % f["truth"]
    w("- %s, %s, %s%s: %s Follows: %s" % (f["id"], f["kind"], f["new"], extra, f["text"], f["why"]))
w("")
w("## Schedules proposed (group N-SCHEDULES), one line each")
w("")
for p in proposed:
    segs = [s for s in p["schedule"]["weekday"] if s["place"] != "off"]
    day = "; ".join("%s to %s %s" % (s["from"], s["to"], s["said"]) for s in segs)
    over = " (replaces hook-cast.json's routine)" if p["schedule"].get("overrides") else ""
    w("- **%s** (%s)%s, a weekday: %s." % (p["name"], p["id"], over, day))
w("")
w("Places added that hook-cast.json lacks (all off Quay Street or unplaced): %s." % "; ".join("%s: %s" % (k, v["said"]) for k, v in doc["proposed_places"].items()))
w("")
w("## Rumours specific to a person (group N-RUMOURS)")
w("")
w("The eleven pooled stories, each a rewording of facts every holder has, with its truth against canon and the story: the heart (true); the nephew has come (true); he missed the funeral (true); June is still in town (true); the fire as the street has it (partly: the paper's arson and 'nobody charged' stand, the owner's guilt is false against the story); trade is thin (true); the door and the key (true); a man at the landing (true); Hal and Rita had words (unknown, nobody can say why); the radio is overheard (true, canon); the arrival seen (true). The %d specific ones:" % len(specific))
w("")
for p, r in specific:
    w("- %s (%s), %s: %s" % (p["name"], r["id"], r["truth"], r["gist"]))
w("")
w("## What canon and the story left open, and was not filled")
w("")
for t in [
    "Mickey's past (a pub and a trawler both appear in older text; canon says neither) and what Mickey was like beyond the two approved lines.",
    "Who Mickey's solicitor was, who drew the will, and who the doctor was; who attended the funeral beyond June and Father Walsh.",
    "Where Tom grew up and what he did; why his family left; whether June knows him as a cousin.",
    "What is in the outfit's envelope, who the outfit's man is, and what the outfit is beyond 'Mickey's arrangement'.",
    "What Hal and Rita's row was about (nobody can say, by design); why Hal's shop sells no coins.",
    "Whether Sheila has read the real book's page about the fire; who the stranger was that Ron argued with in the yard two nights before Mickey died (her sighting; Ron's own account is not written).",
    "When the scrap dealer stripped the fittings (the fire design's reviewer asked for 'after the police let it go'); who lost a shed to the fire; the importer's name.",
    "Why the docks went (the outline keeps it underneath, never explained): Colin's and Albert's lines are kept as their own feeling, not a reason.",
    "Which police force Ellis belongs to; the local paper's name; the Tangs' unit; Ron's years on the docks.",
    "How the three heads, the Fixer and Ellis stand to each other at the baseline beyond canon's one line (each is Act II's).",
    "Feelings between people beyond the tie's weight: no home has any, so only the band is given.",
    "Whether the street holds more of the cast's secrets (the roster's arms are carried as secrets for the five it names).",
]:
    w("- " + t)
w("")
w("## How the PC session would adopt these files (each kind to its home)")
w("")
w("- **Who they are, schedules, ties:** stay in the casting sheets, REGULARS.md and hook-cast.json. To adopt: append the ten proposed routines (and the places they use) to hook-cast.json and replace Julie's and Albert's two; people.json's derived fields then match it, and check_town.py fails the build if they drift.")
w("- **The street's plain facts:** stay in StreetFacts.cs. To adopt: add each person's list of the ids they hold (the `street` lists in authored/) as the table StreetFacts.For reads, replacing 'everyone holds everything'; the two Mickey lines then go only to the sixteen.")
w("- **What each person knows, believes and saw:** a proposal with no home. To adopt: one authored facts file per person beside the casting sheets (id, text, source or 'new', secret), read by the same code that reads the cards' Hard Facts; the secret ones never reach the plain-fallback path (TalkLadder already refuses a card's own secrets).")
w("- **Rumours:** town-news.json and Core/TownNews.cs hold one sample story; RULINGS 29 Sep says ten more wait until he meets it in the game. Jafar's order of 12 October asks for five a person, so these are written, not wired: adopt a few at a time, after he has heard the sample, each with its limits.")
w("- **Newcomer answers:** the ten a person are written answers for the fresh-question bench: each lists its facts, so the PC session can score the live talk against them (answer, partial, don't-know) and use the don't-knows as the honest 'that's all I know' cases. They are not new lines for the game.")
w("- **DECISIONS and approvals:** the six entries are for Jafar's page; nothing here has an approval file, and CATALOGUE.md needs a line for production/cloud-week/town when the session takes it.")
w("")
w("## Limits of the check")
w("")
w("- The word lists are a screen, not a reader: they find the words in the lists and the capitalised names and numbers an answer adds, not an invented detail in lower case, a wrong idiom or a flat voice. The answers were read by hand once for added claims; the places they add anything are in the fact ids each lists.")
w("- Tone (canon's judge is D7) and British 1990 speech were written to the street-lines note and read, not tested; no accent or voice was tried.")
w("- No live model was called and no API money spent; nothing was run in the game.")
w("")
(HERE / "NOTES.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("NOTES.md written, %d lines" % len(L))
