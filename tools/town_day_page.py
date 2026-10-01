#!/usr/bin/env python3
"""The town session's approval page for a day after the first: the documents
to approve and the decisions waiting on Jafar, each one tap and a note, stored
on the page (the artifact's db, at verdicts/<key>), as the 28 September page.

    python tools/town_day_page.py 2026-09-29     # writes production/approvals/2026-09-29-town/index.html
    python tools/town_day_page.py --selftest

Each day's content is a DAYS entry: a title, a line of lede, the questions
(recommendation first and marked) and the documents, read from the repo so the
page shows what was committed.
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import town_page  # noqa: E402  (the same style, script and markdown renderer)

REPO = town_page.REPO
# WHAT JAFAR HAS ANSWERED (Jafar, 30 September: "An item I have answered never
# appears on a page again"): each page's stored verdicts, read before the next
# page is built and kept here, key by key; build() leaves every one out.
ANSWERED_PATH = os.path.join(REPO, "production", "approvals", "town-answered.json")


def answered():
    try:
        with open(ANSWERED_PATH, encoding="utf-8") as fh:
            return set(json.load(fh))
    except (OSError, ValueError):
        return set()

DAYS = {
    "2026-09-29": {
        "title": "The first hour, and fifteen decisions",
        "lede": "The plan for a player's first hour, the first story of the town's own, and fifteen things only you can decide. One tap each, and a note if you want. Done as you picked: the first hour, the neighbours' talk and Sheila's name, and everything on the 28 September page (Father Emil is now Father Brendan Walsh). New today: the last two calls, what the town cannot say because nobody has written it, the hints, each the first time it matters, the outfit's first ask, with whose outfit it is, when DS Ellis turns up, and day 3: Ada's tea, and the warehouse fire Alison asks about.",
        "questions": [
            ("q-sheila-name", "Sheila's card keeps Tom at \"new management\" until he earns a name; canon says names follow knowing, not liking",
             [("exception", "Sheila is the exception by choice: she withholds his name until she trusts him, as she promised Mickey she would size him up; everyone else follows canon (recommended: it is her character, and the rule stays the town's)"),
              ("canon", "Canon wins: once she has met him she calls him Nowak like everyone else")]),
            ("q-chatter", "How often Tom can make out what neighbours say to each other (their own small talk, not about him); each kind has fourteen lines",
             [("cap", "No oftener than every 45 seconds, the street's murmur staying as it is: a line then comes round after 22 minutes on a walk, and never inside ten even in a crowd; nothing new to write or voice (recommended: the cheaper; in the Core now)"),
              ("cap-more", "The same, and thirty lines to each everyday kind instead of fourteen, so a line never comes round inside 22 minutes even in a crowd: sixteen more openers and sixteen more replies for day and for night, which I write and the builder voices"),
              ("pace", "The old pace, an exchange every 6 to 78 seconds: livelier, but a line comes round every one and a half minutes, and it needs about sixty lines a kind before ten minutes hold")]),
            ("q-clock", "How fast the game's day runs. A plainly seen job on night one reaches Tom's face by minute thirty only at two game minutes a real second or faster, and at two, seven times in thirteen only at minute thirty itself",
             [("two-wait", "Two game minutes a second, a day in twelve real minutes, as the first hour was planned, and a way to wait until evening, so a slow player is not caught at the thirty-minute edge; a way to wait is a basic the game needs anyway (recommended)"),
              ("three", "Three a second, a day in eight minutes: the night's story reaches Tom by minute twenty every time, nothing new to build, but a night lasts under three real minutes"),
              ("slower", "Slower, a day in twenty-four minutes or more: calmer, but the town cannot know him inside the first half hour unless he waits through a day")]),
            ("q-reading", "Tom's reading of what the ending will cost failed its review a second time. It is built only from what he sees, as you ruled, but the game's visible signs do not change where the hidden lines are: a friend calls him Tom well below the line where the ending counts them a friend, so the reading can say all is well while a door shuts",
             [("signs", "Give every line a sign: each thing that decides the ending gets one thing Tom can see that changes exactly when it crosses its line (a friend who would stand by him says so; the inspector's manner turns on the morning the books stop standing; the police at the door when it is a manhunt), and the reading is built on those; several evenings of work, some of it the builder's (recommended: it is what your D58 asks, a cost he can watch arrive)"),
              ("rough", "Let his reading be roughly right: it follows the signs there are and can be caught out; cheaper, but a cost can land unseen, which D58 calls a trap"),
              ("later", "Leave it until the town's signs are built in the game, and come back to it then")]),
            ("q-name-before", "Canon says Tom arrives \"known only as Mickey's nephew by name\", and Mickey spoke of him to his own people. Before he comes, do Sheila, Ron and Darren know his name?",
             [("mickeys-own", "Mickey's own people know his name, Tom Nowak, from Mickey, though they have never seen him; the rest of the street does not (recommended: it is what \"Mickey spoke of him\" means, and the street's ladder still starts at \"the new owner\")"),
              ("nobody", "Nobody knows his name until he gives it, Mickey's own people included")]),
            ("q-privacy", "Before your friends play through our server, players should be able to read a short privacy notice, linked from the notice they already see: who is responsible for their words, how long a reported line is kept, and their rights",
             [("draft", "I draft it for your approval, naming you as responsible and keeping reported lines for a year (recommended: the law asks for it at that point, and it is text I can write)"),
              ("later", "Later, before the store: friends see the notice as it stands, which says where their words go and what is kept")]),
            ("q-bench", "The check that stops characters inventing things flags three honest replies in ten and has them written again, which costs time; and in small talk it was far worse: asked \"what biscuits have you got in?\" or \"what do you drive?\", 28 of 36 answers came out as \"That's as far as I can take you\"; a narrow fix tonight brought that to 13, inventions caught as before, and the full retune would go further. Tuning it properly means writing the test conversations again with today's cards. Since your ruling of 29 September that runs through Claude Code on your subscription, not the API: no money, but a good share of a week's allowance",
             [("yes", "Yes, on the subscription, in small runs over the week: every third reply is slower than it needs to be (recommended)"),
              ("later", "Not now")]),
            ("q-keep-quiet", "When Tom asks someone to keep what he did to themselves, who does? The game decides, never the AI; this is my reading of the approved cards and canon, built that way meanwhile",
             [("cards", "Nobody keeps a killing quiet; Ron and Sheila, Mickey's inherited loyalists, keep it quiet for the owner they work for; Darren, loyal to whoever helped him last, says yes to anybody and breaks it the moment someone else pays or threatens him; everyone else only for someone on first-name terms (recommended: it follows the cards)"),
              ("friends", "Stricter: only people on first-name terms with him keep anything quiet, Ron and Sheila included, so the loyalists must come to like him first"),
              ("nobody", "Nobody keeps anything quiet for the asking; only money or a threat works")]),
            ("q-allowance", "Each friend's copy may spend $0.50 of live talk a day and $5 a month (the relay's allowance). Measured tonight, a line costs about 1.2 cents, most of it the check against invented facts, so about forty lines a day: a talkative friend could run out inside the half hour, and then everyone answers in a few words",
             [("raise", "$1.50 a day and $10 a month a copy, about 125 lines a day; three friends playing every day would be at most $4.50 a day, and the relay's own stop at $320 of its $400 month still holds (recommended: the thirty minutes should never run dry)"),
              ("keep", "Keep $0.50 a day and $5 a month; a friend who talks a lot sees the plain note and the short answers"),
              ("more", "$3 a day and $20 a month a copy, for long sessions")]),
            ("q-mickey-death", "How Mickey died. Neither canon nor the outline says, so asked \"How did Mickey die?\", Sheila and Ron made up a heart attack and the check stopped them; now they say they don't know. Sheila's card has her see Ron argue with a stranger in the yard two nights before he died",
             [("heart", "His heart, at the office early one morning; Ron found him when he came on at the rank; the doctor said his heart, and nobody on the street thinks otherwise (recommended: the story is what Tom inherited, and a mystery in the death would be a thread the outline has no room for; the argument in the yard stays something Sheila saw)"),
              ("doubt", "His heart, as the doctor said, but some on the street wonder, and the argument in the yard keeps the doubt alive; never solved, never a quest"),
              ("yours", "Something else, in your note")]),
            ("q-street-facts", "What the street knows that nobody has written. Asked a newcomer's twenty first questions, Sheila, Ron and Darren answered about 38 of 60 with \"that's all I know\" (46 before tonight's fix to the check), nearly all for want of plain facts: the door Sheila does not open, the funeral, what Mickey left, where Tom sleeps, the drivers, the money, where to eat, what Mickey was like",
             [("draft", "I write them from canon and the outline as one short page for your yes: the door is Mickey's own office, locked since he died, and Sheila keeps the key; the funeral was at Father Walsh's chapel, June came back for it; Mickey left Tom the office by his will, as the letter says; Tom sleeps in the flat over the office, Mickey's; one driver by day, one by night, and the dispatcher; the takings thin since the docks went; the cafe across the street. Then everybody can say them (recommended)"),
              ("cards", "Only what each person would know, written into their own cards, for your yes card by card: slower, and every card changes"),
              ("leave", "Leave them unwritten for now: the town says it does not know until the story reaches them")]),
            ("q-outfit", "Whose outfit. Canon says Tom inherits \"a half-dead criminal outfit\"; the first ask (below) needs to know whether it is his to command or somebody else's that Mickey worked for",
             [("mickeys-place", "Somebody else's: Tom inherits Mickey's place in it, so they ask and he can say no, and it is not one of the three rivals (recommended: it is how the July drafts and the outline you approved tell it, \"Mickey's arrangements outlive him\", \"refusing breaks his deal\")"),
              ("his", "His own: Mickey's crew, now Tom's to run; the asks come from whoever Mickey's crew answered to"),
              ("other", "Something else, in your note")]),
            ("q-loud", "When the street's talk brings DS Ellis. On night one only four of the cast are out to see him, and how far the talk goes depends on which: plainly seen by Ron, who meets half the street, five to eight people pass it round by days 3 to 5; by Dusan, two; by the other two, one or none",
             [("three", "When three of his day world are passing it round, from day 4: she comes in the first hour if Ron saw him plainly, or if he was seen two nights (recommended: \"if the street has got loud about him\", and talk rarely brought a detective in 1990)"),
              ("two", "When two are: Dusan's sighting brings her too, so she comes more often"),
              ("never", "Never for talk alone: only for a reported crime a detective takes, or a body")]),
            ("q-fire", "The warehouse fire. Alison asks him about it on day 3, and it is Act I's thread, but the new game has no fire yet: not when it burned, whose warehouse it was, whether anybody was hurt, or what the street says",
             [("draft", "I draft it from the outline for your yes: when and where it burned, whose it was, who was hurt if anybody, and what the street believes, with the truth (the outfit's hand, in Mickey's real book) kept apart from the talk (recommended)"),
              ("yours", "You write it, in your note"),
              ("later", "Leave Alison's question until Act I's thread is written")]),
            ("q-traits", "Each person's nerve, loyalty and greed. Today all forty-one have the same middle values, so no witness goes to the police unless the story cools them on him. Giving each their own (drafted from the cards, canon and their trades: a third of the town would then report a wounding they saw, as in 1990) also moves bribes, debts, who walks with Tom from the start and how people answer frightening talk, and it showed an old rule the wrong way round (the bravest answer as if frightened), in both the simulation and the game's copy",
             [("all", "Give everybody their own, checking each thing it moves, and put the old rule right in both: about a day, with a share for the builder (recommended: a town of forty with one temper cannot surprise him)"),
              ("police", "Only for who goes to the police, as a setting of its own, leaving the rest alike: an hour or two"),
              ("later", "Leave everybody alike for now")]),
        ],
        "docs": [
            ("first-hour", "The first hour, on paper", os.path.join(REPO, "game-design", "first-hour-2026-09-29.md"),
             "Approve the hour", "Change it (say what in the note)"),
            ("town-news", "The town's own news: one sample", os.path.join(REPO, "game-design", "town-news-sample-2026-09-29.md"),
             "Approve it, and write about ten more like it", "Change it (say what in the note)"),
            ("first-moments", "The hints, each the first time it matters", os.path.join(REPO, "game-design", "first-moments-2026-09-29.md"),
             "Approve the moments and their words", "Change them (say what in the note)"),
            ("first-ask", "The outfit's first ask", os.path.join(REPO, "game-design", "first-ask-2026-09-29.md"),
             "Approve the ask and its lines", "Change it (say what in the note)"),
            ("ellis", "When DS Ellis turns up, and what she has", os.path.join(REPO, "game-design", "ellis-2026-09-29.md"),
             "Approve how she comes and what she has", "Change it (say what in the note)"),
            ("day-three", "Day 3: Ada's tea", os.path.join(REPO, "game-design", "day-three-2026-09-29.md"),
             "Approve Ada's tea", "Change it (say what in the note)"),
            ("first-hour-on-paper", "The first hour, on paper: what the town does for each choice", os.path.join(REPO, "game-design", "first-hour-on-paper-2026-09-29.md"),
             "Seen: it reads as the first hour should", "Something here is wrong for the hour (say what in the note)"),
        ],
    },
}



def carried(day, answered, title, lede, new_questions, new_docs):
    """A day's page carrying yesterday's open items: every question and
    document not answered, then the new ones."""
    base = DAYS[day]
    return {
        "title": title,
        "lede": lede,
        "questions": [q for q in base["questions"] if q[0] not in answered] + new_questions,
        "docs": [d for d in base["docs"] if d[0] not in answered] + new_docs,
    }


# Jafar, 29 September: only what shapes the game's identity or is hard to
# undo reaches him, at most three a day; the rest the town decided, one line
# each in DECISIONS.md.
DAYS["2026-09-30"] = {
    "title": "Three calls: how Mickey died, winding it down, threats",
    "lede": "Only three, as you asked. Everything else on yesterday's and today's pages I have settled with my recommendations, one line each in the decisions record; tell me any you would overturn. Your relay answer (no key yet) is done. One tap each, and a note if you want.",
    "questions": [
        ('q-mickey-death', 'How Mickey died. Neither canon nor the outline says, so asked "How did Mickey die?", Sheila and Ron made up a heart attack and the check stopped them; now they say they don\'t know. Sheila\'s card has her see Ron argue with a stranger in the yard two nights before he died', [('heart', 'His heart, at the office early one morning; Ron found him when he came on at the rank; the doctor said his heart, and nobody on the street thinks otherwise (recommended: the story is what Tom inherited, and a mystery in the death would be a thread the outline has no room for; the argument in the yard stays something Sheila saw)'), ('doubt', 'His heart, as the doctor said, but some on the street wonder, and the argument in the yard keeps the doubt alive; never solved, never a quest'), ('yours', 'Something else, in your note')]),
        ('q-wind-down', 'Day 7 is also a night the outfit asks. Told "wind it down", Sheila closes the book on Mickey\'s arrangements, yet Ron would still bring the envelope that evening', [('ends', 'Winding it down ends the arrangement that night: Ron takes the word down, as he does a no; taking it over never undoes a no (recommended; built this way meanwhile)'), ('words', 'Her words change instead, and only his no to Ron ends it')]),
        ('q-threat', 'Threats to a witness ("Say a word and you\'ll regret it"). Built for now: a threat never buys silence, it becomes the street\'s story and makes them warier of him, read from word shapes. Every one of the forty has the same middling nerve, so the old threat code would have silenced everybody; and no word list catches every way of threatening someone, so a threat it misses the town never hears of', [('story-model', 'A threat never buys silence this week, and the checking model reads each line about a deed for a threat ("is this a threat to keep quiet?"), on your capped key while you play, about a twentieth of a penny a line (recommended)'), ('story-words', 'It never buys silence, read from word shapes only, as built: free, with gaps'), ('nerve', 'It silences those of low nerve, once each of the forty has their own nerve')]),
    ],
    "docs": [],
}

# 1 October: yesterday's three, carried while unanswered, and one new call of
# backstory (Jafar, 29 September: only identity or what is hard to undo, at most
# three new a day).
DAYS["2026-10-01"] = {
    "title": "The warehouse fire, the talk's biggest fault, and Steam's wording",
    "lede": "Three new calls: the warehouse fire (backstory); whether to reopen the check behind the talk's biggest fault; and the wording of Steam's AI disclosure, which locks once Valve approves the game. "
            "Paused by your ruling of 29 September (no new systems until the slice is worth playing), yours to reopen any time: Tom's reading of what the ending will cost, everyone's own nerve, the day in court, and what he is told going into his Ledger. "
            "Yesterday's three stay until you answer them. One tap each, and a note if you want.",
    "questions": list(DAYS["2026-09-30"]["questions"]) + [
        ("q-fire-draft", "The warehouse fire: nothing says when it burned, whose it was or whether anybody was hurt, so Alison's question on day 3 finds a town with nothing to say (Father Walsh's old July card would put it around 1970; everything else says last year)",
         [("recommended", "Last November, eleven months before Tom comes: an importer's warehouse on the old row, nobody hurt (the night watchman had slipped off home and lied about his rounds); the outfit had it burned as a lesson for the rent it was owed, Mickey found them the men, and his page in the real book says so; the street believes the owner did it for the insurance (recommended)"),
          ("long-ago", "Long ago, about 1970, as Father Walsh's old card has it: Ellis's and Alison's thread becomes an old story"),
          ("hurt", "Last November, but the watchman got out with his hands burned (his secret, that he was not there, goes)"),
          ("death", "Last November, and the watchman died: a murder inquiry and an inquest, the whole town still talking of it")]),
        ("q-fallback", "The talk's biggest fault: half of a newcomer's first questions end in \"that's all I know\", because the check against invented facts also stops honest paraphrase. Three attempts failed, so it is set aside under your rule; the route left is retuning the check itself (its standard and worked examples), in small runs on your subscription",
         [("retune", "Reopen it: retune the check on the bench in small runs over the week, measured on a newcomer's questions and on the inventions it must still catch (recommended: it is what most stops the slice being worth playing)"),
          ("leave", "Leave it set aside for now")]),
    ],
    "docs": [("steam-ai", "Steam's AI disclosure, drafted", os.path.join(REPO, "production", "store", "steam-ai-disclosure.md"),
              "Approve it as the wording for the store page", "Change it (say what in the note)")],
}


# 30 September, the second page: the street's lines and its regulars, each the
# sample before more are made (CLAUDE.md: nothing is multiplied before he
# approves one), with the blind reviewer's remaining notes beside it.
DAYS["2026-09-30-2"] = {
    "title": "Ron's street lines, the thirty regulars, and the ending's signs",
    "lede": "One call, and two things to read, each a sample before more are made. Ron's own street lines: 159, in his voice, so the street stops talking with one voice; the rest of the named cast follow his pattern once you say yes. And the street's thirty regulars as one contact sheet of text; their faces, clothes and voices come after, from the builder, only with your yes. One tap each, and a note if you want.",
    "questions": [
        ("q-ending-signs", "Item i, every cost that decides how the week ends readable before it decides, turned out much bigger than it looked: the game in Unreal has no endings yet, and each of the seven things that decide them needs a sign that moves exactly at its line, most of them the builder's to put in the street. The design is written (one state for each thing, read by both the ending and its sign, as the research found studios do; and a killing with a sure witness passes through a day of police investigating before a manhunt, so no ending shuts unseen)",
         [("wait", "Keep the design on file; the code waits until the week's end is in the game, and the day of investigating goes in with it (recommended: no new systems until the slice is worth playing)"),
          ("core", "Build the Core half now: the states, the signs' words, Tom's reading and its tests, several evenings, for the builder to wire when the endings come")]),
    ],
    "docs": [
        ("ron-street-lines", "Ron's own street lines", os.path.join(REPO, "production", "casting", "ron-kirby", "STREET-LINES.md"),
         "Yes: this is Ron; write the rest of the named cast this way", "Change them (say what in the note)",
         ["He is more clipped than rambling: most lines are two to five words, where his card has him run on.",
          "His money-minded side shows in only a line or two.",
          "Thirty years on the docks, as his card and the talk have it; his sheet's line says forty, which I read as his own rounding.",
          "A few everyday lines still assume the street, such as the smell of the fish market, and he also stands at the caff, the quay and the allotments."]),
        ("regulars", "The thirty regulars: a contact sheet", os.path.join(REPO, "production", "casting", "regulars", "REGULARS.md"),
         "Yes: these are the street's regulars", "Change them (say what in the note)",
         ["Hal and Doreen work every day though the sheet counts Hal as retired and Doreen as one who won't retire.",
          "The two older voice slots carry five people each, ages fifty to sixty-six on one voice.",
          "An Irish priest's Irish housekeeper may still bring Father Ted's Mrs Doyle to mind for some, whatever her name.",
          "The parade's empty unit, the takeaway's bay, is labelled a repair shop in the street's spec and has no sign yet.",
          "New routines must keep Tanja's friendship with Ada and Albert's with Ron meeting as they do now."]),
    ],
}


# 30 September, the third page: after Jafar's answers to the second (the
# ending's signs wait; Ron's lines and the regulars decided by the town), five
# of Ron's street lines, once, for his tone.
DAYS["2026-09-30-3"] = {
    "title": "Ron's tone",
    "one_screen": True,
    "heading": "Five of Ron's street lines",
    "show": [],
    "decisions": [
        ("ron-tone", "Is this Ron's tone?", [("yes", "Yes"), ("hard", "Too hard"), ("soft", "Too soft")], "yes",
         "Ron has 159 street lines, all short: remarks in passing, a word with a neighbour, a line after a noise. "
         "They are on in the game. In conversation his card has him talk on at more length. "
         "\"Thirty years on the quay\" matches his card and the threat line you approved on 29 September. "
         "If his tone is off, I rewrite all 159 to match and write nobody else's lines until then.",
         [
        ("passing Tom on the rank", "Boss. Kettle's on in the office."),
        ("meeting him the first time", "You'll be the new owner, then. Ron. The rank's mine, the door too."),
        ("while talk about Tom goes round", "Your name's going round, boss. Just so you know."),
        ("after Tom threatens him", "Thirty years on the quay, boss. I've been told worse by better."),
        ("once Tom winds Mickey's business down", "Can't say I'm sorry, boss. Mickey's other business never did him any good."),
    ]),
        ("ron-plain", "Refused twice, Ron says it plainly. Right?", [("yes", "Yes"), ("stiff", "Too stiff")], "yes",
         "When the check refuses a reply twice, Ron can say the facts that bear on the question plainly, after a short opener of his own, "
         "instead of \"that's all I know\". Every detail in it is a written fact, so nothing is invented; his secrets are never said this "
         "way. Measured, it is off for now: the facts it picks by shared words miss the question two times in three, so it waits until "
         "the rule table picks them by the kind of question. This is how it sounds when the fact is right. Two blind reviews; what the "
         "second left: \"Now then\" can read as hello mid-talk; the cards say Mickey died \"three weeks ago\" where this says \"three "
         "weeks before you came\" (I will align the cards).",
         [("Sorry I missed the funeral.", "All I know is this, boss. Mickey's funeral was at Father Walsh's chapel, before you came."),
          ("Where do I sleep?", "Here's what I can tell you, boss. You're in Mickey's flat, over the office."),
          ("Is there any money in it?", "Now then. Mickey's hasn't made much since the docks went. Trade's been thin.")]),
        ("mickey-like", "What was Mickey like? Say only these two for now?", [("yes", "Yes"), ("write", "I'll write it"), ("leave", "Leave it")], "yes",
         "\"What was Mickey like?\" is among a newcomer's first questions, and nobody has written it. I drafted three versions of what the "
         "street says of him; three blind reviews each found lines that give away the story (the fire, the envelope on night one, which "
         "way the drivers' money runs). These two survived. Yes: every regular who knew him can say them; the rest stays unsaid. I'll "
         "write it: you give me what the street says of him. Leave it: the question keeps today's path, where he is often left blank.",
         [("anyone on the street", "Mickey kept his business to himself. You'd not hear it from him on the street."),
          ("anyone on the street", "Mickey kept Ron on when the docks let him go.")]),
        ("talk-next", "Next for talk: write down what the street would know?", [("write", "Yes, write it"), ("leave", "Leave talk")], "write",
         "\"That's all I know\" is down from 36 to about 22 of a newcomer's 60 questions. Two ways of prompting the writer failed today "
         "(planning first: no better; a narrower second try: worse, 27). What still falls back is a question nobody wrote the answer to: "
         "who took Mickey's funeral, how he ran things, last week's takings. The writer fills the gap and the check stops it. "
         "Studios write that knowledge ahead (Valve's talk). I would write it from the questions that fall back, within canon, "
         "backstory to you first, and measure it the same way."),
    ],
}

DAYS["2026-10-01-2"] = {
    "title": "The police, and Sheila's speed",
    "one_screen": True,
    "heading": "Two decisions",
    "show": [],
    "decisions": [
        ("police-witness", "Seeing Tom break a window: enough to report him?",
         [("yes", "Yes"), ("no", "No")], "yes",
         "The review found nobody ever reports him: the rule says a witness goes to the police only when not on his side, "
         "and everybody starts in the middle, where nobody is. Only standing Ada up moves anyone. "
         "Yes: seeing him do it is enough, unless he has won them over (tea, a friend) or talks them round "
         "(keep it quiet, a threat), which gives those their point. No: only those he has already let down report, as now."),
        ("sheila-model", "Sheila on the faster, cheaper model?",
         [("try", "Try it"), ("keep", "Keep")], "try",
         "Measured on your key tonight ($0.18): her first sentence comes 1.43 s after she is asked on today's model, "
         "0.81 s on the faster one Ron and Darren use; caching her card gave nothing. With a fast voice (about 0.8 s) "
         "she can then be heard within 2 s; on today's model not. Try: I write twenty of her replies on both, a reviewer "
         "who does not know which is which compares them against her casting sheet, and I switch only if she still sounds like herself; "
         "about half the cost a line. Keep: she stays about 0.6 s slower than the others."),
        ("street-lines", "The other characters' street lines: one more try, a new way?",
         [("try", "Try once more"), ("leave", "Leave them")], "try",
         "Your list's item 2: Darren, Sheila, Alison, Ada, Father Walsh and June in their own voices on the street. Three versions "
         "failed three fresh reviews (lines refusing what Tom never asked, openers nobody could answer, the same idea in four mouths), "
         "so by your two-tries rule they are set aside and the street's shared lines stay for them. The reviews showed the method "
         "was wrong, not the wording: they were written for every situation the street has, not for where each person really is. "
         "Try once more: only the lines each is heard saying where their day puts them, written as exchanges between the people who "
         "meet (Ada and Walsh at her step, the four at the fish market), checked by machine for repeats first; one review, and if it "
         "fails they stay on the shared lines for good. Leave them: the shared lines, as now."),
    ],
}

# 1 October, the third page: the street lines' fourth try, after one blind review.
DAYS["2026-10-01-3"] = {
    "title": "Three characters' street lines",
    "one_screen": True,
    "heading": "Street lines: three passed",
    "show": [],
    "decisions": [
        ("own-lines-three", "Darren's, Father Walsh's and June's own street lines: put them in?",
         [("yes", "Put them in"), ("no", "Shared lines")], "yes",
         "Your one more try: written only for what the game says to Tom as he passes, each person only for what their day "
         "lets them know; a machine check, then one fresh blind review. Darren, Father Walsh and June passed. Sheila, Alison "
         "and Ada failed (the same retort in two or three mouths; Sheila talking about the books on the pavement) and keep "
         "the shared lines for good, as you said. The reviewer's flagged lines are taken out, not rewritten. Put them in: the "
         "builder adds these 58. Shared lines: everybody but Ron keeps the shared lines, for good.",
         [("Darren, hearing the police took Tom in", "Hear you had a ride with the police. Free taxi, that. Nice for a cab man."),
          ("Darren, hearing Tom refused the errand", "Turned them down, did you? Takes nerve, that. Or you don't know who they are."),
          ("Father Walsh, hearing the police ask", "The guards are asking after you, I'm told. The police, I mean. Old habit."),
          ("Father Walsh, after Tom threatens him", "Threats don't work on an old priest, son. I've nothing left anyone can take."),
          ("June, hearing Tom was taken in", "You get yourself arrested, and I'm the one getting looks in the street. Thanks.")],
         [('Darren (33)', [('a story about him going round', "So listen. Your name's doing the rounds. I'm not saying where. Yet."), ('a story about him going round', "Everybody's got a version of you going. Mine's the one worth having."), ('a story about him going round', "There he is. You want to know what's being said, you know where I'll be."), ('half aloud, once he has passed', "Him? I had something on him. Can't have been worth much, I've forgot it."), ('half aloud, once he has passed', "Don't look. That's him. Whisper going round a while back. Old news."), ('after the detective asked them about him', "Ellis had me in a doorway over you. I said I'd seen nothing. I'm good at that."), ('after the detective asked them about him', "Your detective friend's been on at me. Didn't tell her much. Didn't know much, did I."), ('having seen the police take him', "Saw them stick you in the back of the panda. You're out quick. Who'd you know?"), ('having seen the police take him', 'Out already? Watched them drive you off. Thought that was the last of you.'), ('hearing the police took him in', 'Hear you had a ride with the police. Free taxi, that. Nice for a cab man.'), ('hearing the police took him in', "They're saying the law lifted you. You're walking about, so it can't have been much."), ("hearing he ran Mickey's errand by the ferry", "So you did Mickey's errand by the ferry. I'll not ask. I'd only have to forget it."), ("hearing he ran Mickey's errand by the ferry", "Picked up the late run, they're saying. Nobody's heard it from me."), ('hearing he said no to it', "Turned them down, did you? Takes nerve, that. Or you don't know who they are."), ('hearing he said no to it', "Word is you turned the ferry lot down. I'd walk the long way home for a bit."), ("hearing Mickey's arrangement is finished", "Mickey's old arrangement's off, they say. There's people by the ferry not happy about that."), ("hearing Mickey's arrangement is finished", "Finished with the sideline, I hear. Clean hands. Doesn't pay, but there you go."), ('hearing he never turned up for it', "You left them stood by the ferry half the night. They've been asking where you were."), ('hearing he never turned up for it', "Never turned up, they're saying. I'd have a story ready if I were you."), ('after he threatens them', "Message received, mate. I've gone deaf and blind, me."), ('after he threatens them', "No need to say it twice. I've forgot everything already."), ('hearing he threatened somebody', 'Leaning on folk now, are you? Not on me, I hope. I scare easy, me.'), ('hearing he threatened somebody', "Somebody's been told to keep shut, I hear. I keep shut for nothing, me."), ("hearing he is taking all of Mickey's on", "Mickey's whole lot, then? Big shoes, mate. Anything wants fetching, I'm your man."), ("hearing he is taking all of Mickey's on", "Taking the lot on, they're saying. You'll be needing friends. I'm cheap."), ("hearing he is winding Mickey's other business down", 'Only the cabs from now on, I hear. Shame. I had ideas.'), ("hearing he is winding Mickey's other business down", 'Winding the other business up, they reckon. Safer. Duller, mind.'), ('hearing he would not tell Sheila', "Not even telling Sheila, they say. You can tell me. I'll only tell people who pay."), ('hearing he would not tell Sheila', "Keeping it under your hat. That's worth something, that, to the right buyer."), ('done with him', "I'm not dealing with you, mate. Bad for business."), ('done with him', "Your money's no good with me now. Nothing personal."), ('coming at him over it', "Here. Word with you. What you did's got people asking me, and I don't like being asked."), ('coming at him over it', "No, stop a minute. I've had nothing but grief over you.")]), ('Father Walsh (17)', [('a story about him going round', "I hear things, God help me. I don't hold any of them against a man."), ('a story about him going round', "You look like a man carrying something. My door's open, any hour."), ('a story about him going round', "There's a lot said about you. None of it's my business unless you make it so."), ('half aloud, once he has passed', "God keep him. There's been talk, I know. I'd not trouble with it."), ('half aloud, once he has passed', "That's the young fella with the cabs. Whatever it was, I let it go by."), ('after the detective asked them about him', 'The detective was round asking about you. I said I see you about the street, which is the truth of it.'), ('after the detective asked them about him', "That Ellis woman came to me about you. I've no stories to give her, and I said so."), ('hearing the police are asking about him', "The guards are asking after you, I'm told. The police, I mean. Old habit."), ('hearing the police are asking about him', 'If the police come to you, and you want somebody to stand beside you, say.'), ('hearing the police took him in', "I heard they took you in. I said a prayer, for what it's worth. It's not nothing."), ('hearing the police took him in', "You're out, thank God. I hope they treated you decent."), ('after he threatens them', "Threats don't work on an old priest, son. I've nothing left anyone can take."), ('after he threatens them', "I'll forget you said that. I'd rather you did too."), ('hearing he threatened somebody', "Frightening people, they're saying. That's not the man I took you for."), ('hearing he threatened somebody', "Fear buys you nothing in the end. I've watched men try."), ('avoiding him', "The chapel's waiting on me. Another time."), ('avoiding him', "Forgive me, I'm late for a call.")]), ('June (8)', [('a story about him going round', "Whatever you've got yourself into, I don't want to hear it. Well. Go on, then."), ('a story about him going round', "You've got this street talking already. Took me years to get away from it."), ('hearing the police are asking about him', 'Police, now. I came back for a funeral, not this.'), ('hearing the police are asking about him', 'Sort out whatever the police want before I go home, would you.'), ('hearing the police took him in', "I'm not asking what the police wanted you for. I'm just saying I know."), ('hearing the police took him in', "You get yourself arrested, and I'm the one getting looks in the street. Thanks."), ('avoiding him', "Not now. I've a train to see about."), ('avoiding him', "I'm not stopping.")])]),
    ],
}

# EVERY PAGE FITS ONE PHONE SCREEN (Jafar, 30 September: "Your page is a wall
# of text"): at most three decisions, each one line with its options and the
# recommendation, answered with a tap; any detail folded underneath, closed.
MAX_DECISIONS = 3
MAX_QUESTION = 90      # characters: one line on a phone, the recommendation added
MAX_OPTION = 16        # a tap button's label
MAX_SHOWN = 5          # lines shown above the decisions, each short
MAX_SHOWN_CHARS = 120   # the moment and the line together, about two phone lines

ONE_SCREEN_STYLE = """
:root{--bg:#eef0ee;--card:#fbfcfb;--ink:#1d2326;--soft:#56646a;--line:#cdd4d2;--amber:#a7650f;--amber-bg:#f6e8d3;--ok:#2f6b45}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141819;--card:#1c2123;--ink:#e3e7e5;--soft:#9aa8ad;--line:#33403f;--amber:#e3a454;--amber-bg:#2f2517;--ok:#7cc497;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#141819;--card:#1c2123;--ink:#e3e7e5;--soft:#9aa8ad;--line:#33403f;--amber:#e3a454;--amber-bg:#2f2517;--ok:#7cc497;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font:15px/1.45 "Public Sans",system-ui,sans-serif;margin:0}
.wrap{max-width:30rem;margin:0 auto;padding-inline:16px;padding-block:18px 28px;display:grid;gap:14px}
.eyebrow{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--soft);margin:0}
h1{font:600 1.35rem/1.2 "Newsreader",Georgia,serif;margin:2px 0 0;text-wrap:balance}
ol{list-style:none;margin:0;padding:0;display:grid;gap:9px}
li{display:grid;gap:1px}
li small{color:var(--soft);font-size:.74rem;letter-spacing:.02em}
li q{font:italic 500 1.08rem/1.3 "Newsreader",Georgia,serif}
.ask{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px;display:grid;gap:10px}
.ask p{margin:0;font-weight:600}
.row{display:flex;gap:8px;flex-wrap:wrap}
.row button{flex:1 1 6rem;font:inherit;padding:10px 8px;border:1px solid var(--line);border-radius:5px;background:var(--bg);color:var(--ink);cursor:pointer}
.row button.rec{border-color:var(--amber)}
.row button[aria-pressed="true"]{background:var(--amber-bg);border-color:var(--amber);font-weight:600}
.row button:focus-visible,summary:focus-visible,textarea:focus-visible{outline:2px solid var(--amber);outline-offset:2px}
.status{font-size:.8rem;color:var(--soft);margin:0;min-height:1.1em}
.status.saved{color:var(--ok)}
details{font-size:.86rem;color:var(--soft)}
summary{cursor:pointer}
details p{margin:6px 0 0}
textarea{width:100%;box-sizing:border-box;min-height:2.6rem;margin-top:6px;font:inherit;padding:6px 8px;border:1px solid var(--line);border-radius:4px;background:var(--bg);color:var(--ink)}
"""

ONE_SCREEN_SCRIPT = """<script>
let db = null, canWrite = true;
const picks = {};
function status(key, t, ok) { const s = document.getElementById(key + "-status"); s.textContent = t; s.className = "status" + (ok ? " saved" : ""); }
function show(key, p) { document.querySelectorAll('[data-key="' + key + '"] [data-pick]').forEach(b => b.setAttribute("aria-pressed", String(b.dataset.pick === p))); }
function save(key) {
  const note = document.getElementById(key + "-note").value;
  if (!db) { status(key, "Not saved: this view cannot store your answer."); return; }
  if (!canWrite) { status(key, "Not saved: you can read this page but not answer on it."); return; }
  status(key, "Saving...");
  db.doc("verdicts/" + key).set({ pick: picks[key] || null, note, at: new Date().toISOString() })
    .then(() => status(key, "Saved", true))
    .catch(e => { if (e && (e.code === "not_granted" || e.code === "permission_denied")) canWrite = false; status(key, "Not saved: " + (e && e.message ? e.message : "the store refused it") + "."); });
}
document.querySelectorAll("[data-key]").forEach(card => {
  const key = card.dataset.key;
  card.querySelectorAll("[data-pick]").forEach(b => b.addEventListener("click", () => { picks[key] = b.dataset.pick; show(key, picks[key]); save(key); }));
  document.getElementById(key + "-note").addEventListener("change", () => save(key));
});
(async () => {
  try { db = await window.claude?.use?.("db"); } catch (e) { db = null; }
  if (!db) return;
  for (const card of document.querySelectorAll("[data-key]")) {
    const key = card.dataset.key;
    try {
      const snap = await db.doc("verdicts/" + key).get();
      const v = snap && (snap.data ? snap.data() : snap);
      if (v && v.pick) { picks[key] = v.pick; show(key, v.pick); status(key, "Saved", true); }
      if (v && v.note) document.getElementById(key + "-note").value = v.note;
    } catch (e) {}
  }
})();
</script>"""


def one_screen(day, date, done):
    """A page that fits one phone screen, or ValueError saying what does not."""
    esc = html.escape
    decisions = [d for d in day["decisions"] if d[0] not in done]
    shown = day.get("show", [])
    if len(decisions) > MAX_DECISIONS:
        raise ValueError("more than %d decisions" % MAX_DECISIONS)
    if len(shown) > MAX_SHOWN or any(len(w) + len(t) > MAX_SHOWN_CHARS for w, t in shown):
        raise ValueError("too much shown above the decisions")
    shown_total = len(shown) + sum(len(d[5]) for d in decisions if len(d) > 5)
    if shown_total > 8 or any(len(w) + len(t) > MAX_SHOWN_CHARS for d in decisions if len(d) > 5 for w, t in d[5]):
        raise ValueError("too much shown on one screen")
    for key, question, options, rec, *_ in decisions:
        if len(question) > MAX_QUESTION:
            raise ValueError(key + ": the question is longer than one line")
        if any(len(label) > MAX_OPTION for _, label in options):
            raise ValueError(key + ": an option is longer than a tap button")
        if rec not in [v for v, _ in options]:
            raise ValueError(key + ": the recommendation is not one of its options")
    parts = ["<title>" + esc(day["title"]) + "</title>",
             '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,500;1,6..72,500&family=Public+Sans:wght@400;600&display=swap">',
             "<style>" + ONE_SCREEN_STYLE + "</style>", '<main class="wrap">',
             '<header><p class="eyebrow">LEDGER · the town · ' + esc(date) + "</p><h1>" + esc(day.get("heading", day["title"])) + "</h1></header>"]
    if shown:
        parts.append("<ol>" + "".join("<li><small>%s</small><q>%s</q></li>" % (esc(w), esc(t)) for w, t in shown) + "</ol>")
    for key, question, options, rec, detail, *lines in decisions:
        if lines and lines[0]:
            parts.append("<ol>" + "".join("<li><small>%s</small><q>%s</q></li>" % (esc(w), esc(t)) for w, t in lines[0]) + "</ol>")
        rec_label = dict(options)[rec].lower()
        parts.append('<section class="ask" data-key="%s"><p>%s (recommended: %s)</p><div class="row" role="group" aria-label="%s">'
                     % (key, esc(question), esc(rec_label), esc(question)))
        for v, label in options:
            parts.append('<button type="button"%s id="%s-%s" data-pick="%s" aria-pressed="false">%s</button>'
                         % (' class="rec"' if v == rec else "", key, v, v, esc(label)))
        parts.append('</div><p class="status" id="%s-status"></p><details><summary>More</summary>' % key)
        if detail:
            parts.append("<p>" + esc(detail) + "</p>")
        # EVERYTHING ELSE TO READ, folded with the detail (1 October: the three
        # characters' 58 street lines, so he judges all of them, closed unless opened).
        if len(lines) > 1 and lines[1]:
            for who, said in lines[1]:
                parts.append("<p><b>" + esc(who) + "</b></p><ul>" + "".join("<li>%s: <q>%s</q></li>" % (esc(m), esc(t)) for m, t in said) + "</ul>")
        parts.append('<textarea id="%s-note" placeholder="A note, if you want one"></textarea></details></section>' % key)
    if not decisions:
        parts.append("<p>Nothing is waiting on you from the town: every question on this page is answered.</p>")
    parts.append("</main>")
    parts.append(ONE_SCREEN_SCRIPT)
    return "\n".join(parts)


def build(key):
    done = answered()
    day = dict(DAYS[key])
    date = key[:10]
    if day.get("one_screen"):
        return one_screen(day, date, done)
    day["questions"] = [q for q in day["questions"] if q[0] not in done]
    day["docs"] = [d for d in day["docs"] if d[0] not in done]
    esc = html.escape
    parts = ["<title>" + esc(day["title"]) + "</title>",
             '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;600&display=swap">',
             "<style>" + town_page.STYLE + "</style>", '<main class="wrap">',
             '<header><p class="eyebrow">LEDGER · the town session · ' + esc(date) + "</p>",
             "<h1>" + esc(day["title"]) + "</h1>",
             '<p class="lede">' + esc(day["lede"]) + "</p></header>"]
    if day["questions"]:
        parts.append('<section><h2>Your calls</h2><p class="intro">The first choice in each is my recommendation.</p>')
        for key, title, options in day["questions"]:
            parts.append(f'<div class="card" data-key="{key}"><h3>{esc(title)}</h3><div class="row">')
            for v, label in options:
                parts.append(f'<label class="pick"><input type="radio" name="{key}" id="{key}-{v}" value="{v}"><span>{esc(label)}</span></label>')
            parts.append(f'</div><textarea id="{key}-note" placeholder="A note, if you want one"></textarea><p class="status" id="{key}-status"></p></div>')
        parts.append("</section>")
    for doc in day["docs"]:
        key, title, path, yes, no = doc[:5]
        notes = doc[5] if len(doc) > 5 else None
        parts.append(f'<section><h2>{esc(title)}</h2><article class="card outline" data-key="{key}">')
        # THE REVIEWER'S REMAINING NOTES, beside what they are about (CLAUDE.md,
        # the gate: narrow points go to his page with the candidate, his eye decides).
        if notes:
            parts.append("<details class=\"notes\"><summary>The blind reviewer's remaining notes</summary><ul>"
                         + "".join("<li>" + esc(n) + "</li>" for n in notes) + "</ul></details>")
        parts.append(town_page.outline_html(path))
        parts.append(f'<div class="row"><label class="pick"><input type="radio" name="{key}" id="{key}-approve" value="approve"><span>{esc(yes)}</span></label>'
                     f'<label class="pick"><input type="radio" name="{key}" id="{key}-redo" value="redo"><span>{esc(no)}</span></label></div>'
                     f'<textarea id="{key}-note" placeholder="What to change"></textarea><p class="status" id="{key}-status"></p></article></section>')
    parts.append('<p class="status" id="store-status"></p></main>')
    parts.append(town_page.SCRIPT)
    return "\n".join(parts)


def selftest():
    # Jafar's rules for pages (30 September): an answered item never appears
    # again; a page is dated the day it is made; pictures open at full size.
    done = answered()
    assert {"q-mickey-death", "q-wind-down", "q-threat", "q-fire-draft", "q-fallback", "steam-ai"} <= done
    for date in DAYS:
        page = build(date)
        assert page.startswith("<title>")
        for key in done:
            assert 'data-key="%s"' % key not in page, (date, key)
    assert main(["town_day_page.py", "2099-01-01"]) == 1
    assert "zoom-in" in town_page.STYLE and 'className = "full"' in town_page.SCRIPT
    # One phone screen (Jafar, 30 September): too many decisions, a long line,
    # an unmarked recommendation or detail left open are refused.
    ok = {"title": "t", "one_screen": True, "decisions": [("k1", "Is it right?", [("yes", "Yes"), ("no", "No")], "yes", "why")]}
    assert "<details>" in one_screen(ok, "2026-09-30", set()) and "<details open" not in one_screen(ok, "2026-09-30", set())
    assert "(recommended: yes)" in one_screen(ok, "2026-09-30", set())
    for bad in (dict(ok, decisions=ok["decisions"] * 4),
                dict(ok, decisions=[("k1", "x" * 200, [("yes", "Yes")], "yes", "")]),
                dict(ok, decisions=[("k1", "Is it right?", [("yes", "Yes, and a great deal more besides")], "yes", "")]),
                dict(ok, decisions=[("k1", "Is it right?", [("yes", "Yes")], "maybe", "")]),
                dict(ok, show=[("when", "a line " * 40)])):
        try:
            one_screen(bad, "2026-09-30", set())
        except ValueError:
            continue
        raise AssertionError("a page that does not fit one screen was built")
    for day in DAYS.values():
        for key, _, options in day.get("questions", []):
            assert "recommended" in options[0][1], key
    print("town_day_page selftest: ok")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    import datetime
    date = argv[1]
    # A page is dated the day it is made (Jafar, 30 September).
    if date != datetime.date.today().isoformat():
        print("refused: a page is dated the day it is made; today is " + datetime.date.today().isoformat())
        return 1
    # A second page on one day (--part 2) is its own page, never the answered one rewritten.
    part = argv[argv.index("--part") + 1] if "--part" in argv else None
    key = date + ("-" + part if part else "")
    if key not in DAYS:
        print("no page written for " + key)
        return 1
    # EVERY PAGE FITS ONE PHONE SCREEN (Jafar, 30 September): only one-screen
    # pages are written from now on.
    if not DAYS[key].get("one_screen"):
        print("refused: a page must fit one phone screen (Jafar, 30 September); give it one_screen")
        return 1
    out_dir = os.path.join(REPO, "production", "approvals", date + "-town" + ("-" + part if part else ""))
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build(key))
    print("wrote", os.path.relpath(path, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
