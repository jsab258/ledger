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
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import town_page  # noqa: E402  (the same style, script and markdown renderer)

REPO = town_page.REPO

DAYS = {
    "2026-09-29": {
        "title": "The first hour, and twelve decisions",
        "lede": "The plan for a player's first hour, the first story of the town's own, and twelve things only you can decide. One tap each, and a note if you want. Done as you picked: the first hour, the neighbours' talk and Sheila's name, and everything on the 28 September page (Father Emil is now Father Brendan Walsh). New today: the last two calls, what the town cannot say because nobody has written it, the hints, each the first time it matters, and the outfit's first ask, with whose outfit it is.",
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
            ("q-bench", "The check that stops characters inventing things flags three honest replies in ten and has them written again, which costs time; and in small talk it was far worse: asked \"what biscuits have you got in?\" or \"what do you drive?\", 28 of 36 answers came out as \"That's as far as I can take you\"; a narrow fix tonight brought that to 13, inventions caught as before, and the full retune would go further. Tuning it properly means writing the test conversations again with today's cards, about $20 to $40 of calls",
             [("yes", "Yes, spend it: every third reply is slower than it needs to be (recommended)"),
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
        ],
    },
}


def build(date):
    day = DAYS[date]
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
    for key, title, path, yes, no in day["docs"]:
        parts.append(f'<section><h2>{esc(title)}</h2><article class="card outline" data-key="{key}">')
        parts.append(town_page.outline_html(path))
        parts.append(f'<div class="row"><label class="pick"><input type="radio" name="{key}" id="{key}-approve" value="approve"><span>{esc(yes)}</span></label>'
                     f'<label class="pick"><input type="radio" name="{key}" id="{key}-redo" value="redo"><span>{esc(no)}</span></label></div>'
                     f'<textarea id="{key}-note" placeholder="What to change"></textarea><p class="status" id="{key}-status"></p></article></section>')
    parts.append('<p class="status" id="store-status"></p></main>')
    parts.append(town_page.SCRIPT)
    return "\n".join(parts)


def selftest():
    page = build("2026-09-29")
    assert page.startswith("<title>") and 'data-key="first-hour"' in page and 'data-key="q-chatter"' in page and 'q-relay' not in page
    assert "<script" not in town_page.outline_html(DAYS["2026-09-29"]["docs"][0][2])
    for key, _, options in DAYS["2026-09-29"]["questions"]:
        assert "recommended" in options[0][1], key
    print("town_day_page selftest: ok")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    date = argv[1]
    out_dir = os.path.join(REPO, "production", "approvals", date + "-town")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "index.html")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build(date))
    print("wrote", os.path.relpath(path, REPO))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
