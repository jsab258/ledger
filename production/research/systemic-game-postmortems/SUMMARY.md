# Four games that tried something like this and got hurt

Research topic 21. Topic 18 looked at small teams that finished. This is the
other half: ambitious simulation games that shipped badly or never shipped at
all. I picked cases whose ambition was the same shape as ours, not just famous
disasters.

## 1. Oblivion, 2006: the simulation ate the story

Bethesda built NPCs with real wants and let them act on them. In testing, the
world turned into a bloodbath. Characters murdered each other over drugs,
money and objects they wanted, and because quests need specific people alive,
the quests broke.

The two reasons are almost embarrassingly small:

- A drug dealer ran out of stock, so the addicts who wanted it **attacked
  him**. There was no other way for them to get what they wanted.
- An NPC who stole something and was spotted by a guard had **no way to pay a
  fine**, so the guard killed them.

Give a simulated person a want with no legal way to satisfy it, or a punishment
with no middle option, and violence is the only branch left. Radiant AI was
mostly cut before release.

**Where we are on this:** nothing in our code can kill anybody. There is no
death state at all, and nobody is marked as protected either. That is fine, and
it is because combat is a later phase. But it means our simulation and our ten
named characters have never met. Oblivion did not break while the simulation was
being built. It broke the moment the simulation met a cast the story needed
alive.

Their fix, marking people unkillable, is the one we should not copy, because
our whole moat is that the town does not lie to you.

## 2. STALKER 2, 2024: the invisible half lost

Their A-Life system simulates the whole zone living its life while you are
somewhere else. It is the closest thing in a shipped game to what we are
building.

It arrived broken, and the developer said exactly why: **"We were fighting with
optimization."** To hit a frame rate they shrank the radius within which A-Life
runs, and the system needs a much bigger radius to mean anything. The feature
was quietly removed from the Steam page.

This is a real studio, with a real team and real money, two years ago.

**Where we are on this:** topic 17 found our version of the same trap before I
found theirs. We currently simulate everyone at full speed everywhere, and our
frame budget and our resident count are still one number instead of two. The
difference is that GSC had to make this choice under launch pressure and we get
to make it deliberately, years early, with nobody waiting.

## 3. No Man's Sky, 2016: the description broke, not the game

The game that shipped was roughly the game people reviewed harshly. What was
actually broken was everything that had been said about it beforehand. Players
cut together video montages of promises that were not in the box.

It took two years and three big free updates to recover.

**Where we are on this:** we cannot make this mistake yet, because there is no
publisher, no Kickstarter, no store page and nobody has been told anything. Of
the four failure modes here, this is the one that has destroyed the most
goodwill in the industry, and it is the one you would have to actively choose.

The smaller version still applies: the Meridian Test's first condition is a
thirty-minute first impression, which is exactly what a reviewer measures.

## 4. Milo, 2010: the conversation demo that never shipped

Peter Molyneux demoed a game where you talk to a simulated child, on stage, at
E3 and at TED. It was never seen again.

Sixteen years ago somebody promised the world live conversation with a person
who is not real, and it did not ship. The technology to make the words is not
what stopped it. It was a beautiful ten-minute demo sold as a product.

His own lesson afterwards, about a different project, was that showing and
funding something "before having something defined and playable is a hugely
risky undertaking."

## The one I could not find, which is the interesting one

I searched four different ways for a post-mortem of a game whose **NPC memory
or relationship system** was cut before release. There isn't one.

Plenty has been written about how to build such systems. Nothing about one
failing. Our central moat, the thing that makes this game different, is the one
part of it with no cautionary tale to learn from.

That cuts both ways. Nobody has proved it is a trap. Nobody has proved it is
not. It means our own instruments matter more than anything I can read.

## What I would take from all four

Three of these four were made much worse by talking. We have said nothing to
anyone, and that is a real advantage rather than an accident of timing.

The two that genuinely threaten us arrive at moments we can see coming:

1. **When death becomes possible** and the simulation first meets the named
   cast. The Oblivion lesson is not "protect people". It is "never leave a
   character with only one branch."
2. **When the frame budget is first set at a resident count.** That is a
   decision we can make calmly this year, and the studio that made it under
   deadline lost the feature.

And a note in our own favour, since this page is otherwise a list of worries.
The defence against the Milo failure is already built here and it is not a
document: it is the rule that nothing counts as done until something calls it
and a gate proves the call, and the throughput ledger that recorded a finished
brand bible as **zero** because nothing read it. A studio with that habit
notices a beautiful demo that is not a game.
