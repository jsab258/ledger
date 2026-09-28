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
        "title": "The first hour, and two decisions",
        "lede": "The plan for a player's first hour, and two things only you can decide. One tap each, and a note if you want.",
        "questions": [
            ("q-relay", "Where the talk server runs, so no key ships with a friend's copy",
             [("hetzner", "A small rented server in Germany, about €6 a month, stopping all calls at $50 a month while friends play (recommended: cheapest, simple, and Europe is where they are)"),
              ("fly", "Fly.io, about $3 a month, the same stop"),
              ("later", "Not yet: no copies go to friends until you say")]),
            ("q-reading", "Tom's reading of what the ending will cost (D58, D33)",
             [("seen", "Built from what he has seen and heard, so it can be wrong, as a man's reading of his own position is (recommended: it is what D33 says)"),
              ("truth", "The true state, put into words: simpler and always right, but a meter by another name")]),
            ("q-sheila-name", "Sheila's card keeps Tom at \"new management\" until he earns a name; canon says names follow knowing, not liking",
             [("exception", "Sheila is the exception by choice: she withholds his name until she trusts him, as she promised Mickey she would size him up; everyone else follows canon (recommended: it is her character, and the rule stays the town's)"),
              ("canon", "Canon wins: once she has met him she calls him Nowak like everyone else")]),
        ],
        "docs": [
            ("first-hour", "The first hour, on paper", os.path.join(REPO, "game-design", "first-hour-2026-09-29.md"),
             "Approve the hour", "Change it (say what in the note)"),
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
    assert page.startswith("<title>") and 'data-key="first-hour"' in page and 'data-key="q-relay"' in page and 'data-key="q-reading"' in page
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
