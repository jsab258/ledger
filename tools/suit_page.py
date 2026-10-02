#!/usr/bin/env python3
"""Jafar's page for the ready-made suit: one phone screen, two one-line decisions, detail folded.

    python tools/suit_page.py      # writes production/approvals/2026-10-02-suit/index.html

WHY, 2 October, night. His order: screen ready-made rigged suits against the fixed rubric
(production/art/clothing/RUBRIC.md), NoAI-tagged ones rejected, and bring him the best one free or under $40 on one
page, or a plain report that none qualifies (production/art/clothing/SCREENING-2026-10-02.md). None qualifies outright;
one candidate's NoAI field is hidden from a signed-out browser, and only he can check it. Buying is his. The page
keeps the look and the stored answers of tools/clothes_page.py (verdicts/<key>). No seller's pictures are copied onto
the page: he opens the listing itself to check it.
"""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clothes_page  # noqa: E402
import page_pictures  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "production", "approvals", "2026-10-02-suit")
NICE = "https://www.fab.com/listings/a49a955d-d038-434f-99b3-d4b3621f77fc"
HUSKY = "https://www.fab.com/listings/ef35cb3e-ebd9-4167-b1f4-596056daed21"

ASKS = [
    ("suit-nice", "Nice Pictures' Business Jacket, $39.99: open it signed in; if it allows use with AI, buy it? "
                  "(recommended: yes if it does)",
     [("bought", "It allows AI: bought", True), ("noai", "It is NoAI", False), ("no", "Don't buy", False)],
     ['<a href="%s" target="_blank" rel="noopener">Its Fab page</a>: rigged to the MetaHuman skeleton, a MetaHuman '
      'Outfit Asset. Fab hides its details from a signed-out browser ("mature content"), so I could not read its NoAI '
      'field. On Fab, signed in, look under Details for "Allows usage with AI": Yes means it qualifies. Its one picture I '
      'could see: a grey two-button jacket, notch lapels rolling to the top button near the waist, flap pockets, natural '
      'shoulders, perhaps a little short. If you buy it, I import it unchanged onto Ron and Darren and the builder films '
      'it against the rubric.' % NICE]),
    ("suit-noai", "If it is NoAI too, none qualifies: every other MetaHuman suit under $40 is NoAI. Ask a seller? "
                  "(recommended: ask Husky)",
     [("ask-husky", "Ask Husky (you write)", True), ("stop", "Stop: no suit yet", False)],
     ['Of 387 suit listings on Fab at $40 or under, 247 are NoAI, including every one rigged to the MetaHuman skeleton '
      'that I could read. The closest in cut is <a href="%s" target="_blank" rel="noopener">Husky\'s Business Suit 55</a> '
      '($29.99): two buttons, medium notch lapels, natural shoulders, resizes on every MetaHuman body; rejected only as '
      'NoAI. Husky offers support and changes by email (on the page). The question for them: may an AI assistant import '
      'and fit the files in our own game, never training any AI on them? The free suits are patterns or unrigged '
      'meshes; none is ready to wear. The full screening: production/art/clothing/SCREENING-2026-10-02.md.' % HUSKY]),
]


def build():
    os.makedirs(OUT, exist_ok=True)
    e = html.escape
    css = clothes_page.CSS.replace("<title>Tailored clothes</title>", "<title>The ready-made suit</title>")
    parts = [css, '<main class="wrap">',
             '<header><p class="eyebrow">LEDGER · clothes · 2026-10-02</p><h1>The ready-made suit</h1></header>',
             '<section class="ask"><p>Against the rubric for 1990 suits, none qualifies outright. One may: only you can '
             'check it.</p></section>']
    for key, q, opts, more in ASKS:
        btns = "\n".join('<button type="button"%s id="%s-%s" data-pick="%s" aria-pressed="false">%s</button>'
                         % (' class="rec"' if rec else "", key, v, v, e(label)) for v, label, rec in opts)
        parts.append('<section class="ask" data-key="%s"><p>%s</p><div class="row" role="group" aria-label="%s">\n%s\n</div>'
                     '<p class="status" id="%s-status"></p><details><summary>More</summary>%s'
                     '<label for="%s-note">A word, if any</label><textarea id="%s-note"></textarea></details></section>'
                     % (key, e(q), e(q), btns, key, "".join("<p>%s</p>" % m for m in more), key, key))
    parts.append("</main>")
    parts.append(clothes_page.SCRIPT)
    page = page_pictures.apply("\n".join(parts))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
    print("PAGE", os.path.join(OUT, "index.html"))


if __name__ == "__main__":
    build()
