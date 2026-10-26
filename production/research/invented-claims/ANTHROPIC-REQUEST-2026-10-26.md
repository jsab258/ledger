# A request to Anthropic: training a small checker on Claude's labels (draft, 26 October 2026)

His pick on his page of 26 October: ask Anthropic first; Claude drafts, he sends. Why it is asked: Anthropic's terms read three ways on this (production/research/invented-claims/LOCAL-CHECKERS-2026-10-26.md, section 4): the Commercial Terms bar using outputs to build a competing model; a help-centre article lists classifiers as an allowed use but says training needs written permission; the Usage Policy taking effect on 12 November 2026 bars training any model on outputs without prior authorisation. Nothing is trained until the answer comes.

**Where to send it (unverified):** Anthropic's support, from the help centre's contact form while signed in to the Console account that holds the game's API key, so the request is tied to that account. If the form offers a choice of topic, the one for commercial or policy questions.

---

**Subject:** Permission to train a small in-game fact checker on Claude Haiku's labels

Hello,

I make a single-player game, LEDGER, on my own. Its characters answer the player in speech; Claude (Sonnet) writes each reply, and Claude Haiku checks every sentence against what that character knows before it is spoken, so characters never invent facts. The check costs about a second a sentence.

I would like to add a small local classifier (an open model of about 17 to 68 million parameters, MIT-licensed) that runs on the player's PC and clears only sentences it is certain are supported; everything else would still go to Haiku. To train it, I would have Haiku label a few thousand short sentences from my own game as supported or unsupported by a given list of facts, and fine-tune the small model on those labels. It would do only this one narrow task inside my game; it would not be offered, sold or released separately, and it would not generate text.

Is this permitted under my account's terms, and does it need your written authorisation? If it does, may I have it?

My account: the Console organisation that owns the game's API key (the email this is sent from).

Thank you,
Jafar Sabadia
