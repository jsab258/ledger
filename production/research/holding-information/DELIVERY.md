# Topic 13: how investigation games hold information a player cannot write down

STATUS: SPEC (research delivery). Branch `research/holding-information`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged.
Repository claims name their file and line.

This topic answers an ASK I put to Jafar in the coverage audit (game 5, Shadows
of Doubt): a notebook or a corkboard with string. Section 3 is a third option
that I think is better than either, and it comes from Outer Wilds.

## 1. Three games, three different problems solved

### 1.1 Obra Dinn: how to let a player COMMIT a deduction without letting them guess

CITED (search summaries of Wireframe's "Exploring Return of the Obra Dinn's rule
of three", Film Stories' version, and the Intermittent Mechanism blog's
"Confirmation in The Return of Obra Dinn"): "As soon as three deaths have been
accurately logged, the game pulls you out of the action and lets you know that
they were correct, stamping them permanently into the insurance ledger." The
reason is stated explicitly: "If it did [verify immediately], you could simply
try every combination of names, or if you knew one character's name but not the
other, you could click through the others until the game verified the correct
answer." And each entry must be complete: "All three details within the journal
entry must be correct before it counts."

DERIVED: this is the cleanest known solution to the brute-force problem in
deductive games, and the elegance is that it costs nothing to build. It is a
batching rule over a validation that already has to exist.

**Where it lands for us:** `Core/Informing.cs` is the verb where the player names
somebody, and its thesis is that "truth is not an input. A true accusation nobody
will corroborate is ignored." So LEDGER already refuses immediate verification,
by a different and arguably better route: our accusation is not checked against
truth at all, it is weighed by corroboration. A player cannot brute-force a name
because naming a name is a public act with a cost.

That is a real design advantage and it is worth noticing that we got it for free
from the moat. Obra Dinn needed a rule of three because it has a right answer to
protect. Ours has a town to convince.

### 1.2 Her Story: how to make a corpus the player can never exhaust

CITED (search summaries of the official Her Story about page, PocketGamer's
"Howdunnit: The making of Her Story", and Emily Short's review): the game is a
search interface over a police database; "you type search terms and get a row of
5 clips"; "the database is only able to display five results per keyword at a
time, so as you try and unlock more of the story, you have to become ever more
clever with your searches", against 271 clips; and "as you watch these clips,
more potential search terms are unearthed". "How you figure out the story, from
clip to clip, is entirely up to you."

DERIVED, and it is the mechanism worth naming: **the cap is the design.** Five
results per query is what forces the player to think of a better word, and the
better word comes from something they heard. The information the player holds in
their head IS the interface, because a search term is a thing you have to have
learned. Nothing is written down for you and nothing needs to be.

**Where it lands for us:** this is a remarkably good description of what
D12 already asks for. "Learning what people know is done through diegetic verbs
[...] asking around, buying gossip, pub talk, eavesdropping, stealing tapes.
There is no free omniscient read." Asking around IS a search query, and what you
can ask about is bounded by what you have heard. Her Story is the proof that this
shape carries a whole game.

### 1.3 Outer Wilds: how to track what the player knows without solving it

CITED (search summaries of the New Horizons Ship Log guide, the Outer Wilds
Fandom wiki's Computer entry, and the Medium piece on its UX): "Rumor Mode allows
you to view the entries in the way in which they relate to each other, and since
the connections between entries can be different depending on the order in which
you find them, the layout of Rumor Mode can be different for each player." It
"tracks everything you learn, notes everything important and shows you how things
link to each other", and it does this "without directly solving puzzles for you".

And the principle underneath, CITED (same sources): "In Outer Wilds, you and the
main character have the exact same knowledge."

## 2. The principle all three share, and we already have it as a ruling

**The player's knowledge and the character's knowledge are the same thing, and
the interface is a record of it rather than a source of it.**

D12 says this in its own words: "The player's own memory is fully surfaced in an
in-game journal called the Ledger. Per-person and per-event entries for
everything witnessed, heard or told", tagged `witnessed`, `heard` (with source
and time) or `deduced`. And, separately, "NPC minds are never shown as ground
truth."

DERIVED: those two clauses together are the Outer Wilds contract exactly. Which
means the design question for the Ledger is not WHAT it holds, which is settled,
but what it DOES with what it holds. That is section 3.

## 3. The answer to the ASK, and it is neither of the two options I gave

In the Shadows of Doubt delivery I put a question to Jafar: a notebook, which is
a list and holds any amount, or a corkboard with string, which shows the
connections the player drew because the player drew them.

**Rumor Mode is a third thing and it is better than both.** It is a notebook that
draws its own string.

- It is a LIST in the sense that it holds everything and cannot become
  unreadable.
- It shows CONNECTIONS, which is the corkboard's whole advantage.
- The player does not do the pinning, so it is not busywork.
- And the layout differs per player, because it reflects the order of discovery,
  so it is still personal. That is the thing I thought only the corkboard could
  give.

DERIVED, against our tags: D12's three tags are `witnessed`, `heard` (carrying
its source and the time) and `deduced`. **`heard` already carries an edge.** A
heard entry names who told you, which is a link from a fact to a person. So the
graph Rumor Mode draws is already implicit in the data D12 specifies; nothing new
has to be recorded to draw it.

I am not withdrawing the ASK, because which of the three Meridian gets is still a
feel judgement and still his. I am adding a third option and saying I think it
wins, and that our own decision record already specifies the data it needs.

## 4. The one place our problem is harder than theirs

All three games have a FIXED, FINITE, AUTHORED body of truth. Obra Dinn has sixty
fates. Her Story has 271 clips. Outer Wilds has a solar system that does not
change.

LEDGER does not. Our information is generated by a simulation that keeps running,
about people who keep doing things, and it never stops arriving.

DERIVED, and it is the thing none of these three can teach us: **a finite mystery
can be laid out completely, and an infinite one has to be filtered.** Her Story's
five-result cap is a filter over a fixed corpus and works because the corpus is
fixed. Outer Wilds' Rumor Mode can show every connection because there are a
knowable number of them.

The nearest thing to guidance is `Core/Gossip.cs:970`, the `Lead` type, which is
already the right shape for a filter: "who is carrying talk about them, how sure
they are, where it came from, and whether it touches the hidden life". That is a
ranked, sourced, current view rather than a complete one, and a complete one is
not available to us.

HOLE: I did not find any investigation game with an open-ended, ongoing
information supply that solves this. Shadows of Doubt is the nearest and its
reviews say the cases become interchangeable (coverage audit game 5). **This may
be genuinely unsolved, and if so it is the most interesting unsolved problem in
LEDGER's design.**

## 5. Findings

1. **We already have Obra Dinn's protection and did not have to build it** (1.1).
   A name is not checked against truth here, it is weighed by corroboration, so
   brute force costs something.
2. **Her Story is proof that "what you can ask about is what you have heard"
   carries a whole game** (1.2), and D12 already specifies that shape.
3. **Rumor Mode is a third answer to my own ASK and I think it beats both my
   options** (3), and D12's `heard` tag already carries the edge it needs.
4. **All three games solve a FINITE mystery and ours is not finite** (4). That is
   the part nobody can hand us, and it points at ranked leads rather than
   complete maps.

## 6. What could not be established

1. **Any measurement of how well these interfaces work.** Everything here is
   design description and critical praise. I have no data on completion,
   confusion or abandonment for any of the three.
2. **How Rumor Mode's layout algorithm works.** "The layout can be different for
   each player" is stated, and how it is computed is not, which matters if
   anybody tries to build one.
3. **Whether Her Story's five-cap number is load-bearing** or an arbitrary
   choice that happened to work.
4. **Any game with an ongoing, generated information supply that solves the
   legibility problem** (4). This is the important one. I looked and did not
   find, and I am recording that as a genuine gap in the field rather than a gap
   in my search, while acknowledging I cannot distinguish those two from here.
5. **Not covered:** the detective-fiction tradition of the fair-play mystery,
   which is where Obra Dinn's rules come from and which topic 22 may touch; and
   the Ace Attorney and Danganronpa family, which solve this with explicit
   evidence-presentation mechanics and which I did not survey.

## 7. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Wireframe Magazine, "Exploring Return of the Obra Dinn's rule of three", https://wireframe.raspberrypi.com/articles/obra-dinn-the-rule-of-three
- Film Stories, "Exploring Return of the Obra Dinn's rule of three", https://filmstories.co.uk/features/exploring-return-of-the-obra-dinns-rule-of-three/
- Intermittent Mechanism, "Confirmation in The Return of Obra Dinn", https://intermittentmechanism.blog/2024/05/21/confirmation-in-the-return-of-obra-dinn/
- Game Developer, "For Lucas Pope, Return of the Obra Dinn was a bunch of appealing design problems", https://www.gamedeveloper.com/design/for-lucas-pope-i-return-of-the-obra-dinn-i-was-a-bunch-of-appealing-design-problems (EGRESS BLOCKED)
- Emily Short's Interactive Storytelling, "Return of the Obra Dinn (Lucas Pope)", https://emshort.blog/2019/06/06/return-of-the-obra-dinn-lucas-pope/
- AIAS Game Maker's Notebook, "Lucas Pope's Return of the Obra Dinn", https://interactive.libsyn.com/lucas-popes-return-of-the-obra-dinn
- Her Story official site, "About", http://www.herstorygame.com/about/
- PocketGamer.biz, "Howdunnit: The making of Her Story", https://www.pocketgamer.biz/feature/62104/making-of-her-story/
- Emily Short's Interactive Storytelling, "Her Story (Sam Barlow)", https://emshort.blog/2015/06/24/her-story-sam-barlow/
- Vice, "Watching as Detectives: The Truth Behind Her Story", https://www.vice.com/en/article/watching-as-detectives-the-truth-behind-her-story-400/
- New Horizons, "Ship Log" guide, https://nh.outerwildsmods.com/guides/ship-log/
- Outer Wilds Fandom wiki, "Computer", https://outerwilds.fandom.com/wiki/Computer
- Medium (Claudia Mohedano), "How Outer Wilds transcends UX to become Human Experience", https://medium.com/@claudmohe/how-outer-wilds-transcends-ux-to-become-human-experience-3ff41def8f8c
- Outer Wilds Ventures, interactive ship log, https://outerwilds.ventures/

Repository sources, read this session at commit `074f85b`:
`ledger-v2/respec/decision-register/D12-information-surfaces.md`,
`ledger/Assets/Scripts/Core/Informing.cs`, `Core/Gossip.cs:970`,
`production/systems-inventory.json`, and this lane's own
`production/research/coverage-audit-shadows-of-doubt/` on its branch.
