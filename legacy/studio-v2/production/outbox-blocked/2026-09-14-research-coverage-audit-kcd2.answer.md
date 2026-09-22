# What Kingdom Come 2 has that we do not

Coverage audit, game 1 of 5. I listed 71 things KCD2 actually contains and
checked each against our own list of 91 systems. I recommend taking five of
them. Almost all the rest should stay where it is.

## One thing to know first

Three of the ten gaps we spotted by hand are **already built**. The code makes
blood land on your coat, fade to a mark over half a day, get noticed by someone
near you under a light and not across a dark street, cost more when the person
noticing knows you well, and take 25 minutes and a private sink to wash off. It
gives every weapon a history: who sold it, what you did with it, where you
dumped it, whether anyone saw. And a disguise works: it buys doubt about your
face and none about your car.

None of that appears on our list of 91 systems. We have been calling things gaps
that are half done, because the list has no square for them.

## Five things to take

**1. What you look like, as something people can see.**
Blood we have. Dirty, torn, a different coat, somebody else's watch on your
wrist, we do not. Our own recognition ladder already says the bottom rung of
"who was that" is "a man, big, long coat", so clothing is what a witness is
meant to report and nothing supplies it. It is also the escape route you asked
for: change your appearance rather than reset anything. Right now they cannot.
COST: small in code, moderate in art. Making a coat read as bloodied and torn in
a photoreal frame is the expensive half, not the rule.

**2. Things on you that can be traced back to what you did.**
KCD2 marks stolen goods so everyone can tell, and the mark fades over a week or
two. We already track where every object came from. Missing is the other end:
somebody looking at you connects the object to the act. Same rule as the blood,
used twice.
COST: small. The model exists. What is missing is a screen telling the player
the watch is dangerous, and that screen is already specified.

**3. Sleeping, and ending a day.**
Nothing currently ends a day. That matters because rumours take time to travel,
and if the player cannot deliberately cross a night, that time happens to them
instead of being something they play against. The best move in the game should
be: do it, then get off the street before the town wakes up. It does not exist.
COST: moderate. Advancing a clock is easy. Making the town move while you sleep
is the work.

**4. Leaning on people, as a real system rather than two buttons.**
We have a bribe button and a threaten button. KCD2 has six ways to push someone
and each reads something different. We cannot copy theirs, because theirs reads
character stats and you ruled the player has none. Ours would read better
things: what this person remembers about you, what you look like right now, and
who else is close enough to hear. The same lie then costs different amounts to
different people, which is the thing you wanted.
COST: moderate, and the expensive half is writing. When a push fails, the person
has to say why, and the why has to be something that actually happened.

**5. The town changing how it behaves after a crime.**
In KCD2, if there has been violence nearby, people stay in instead of going out,
carry something, ask for more patrols. No dialogue needed. That is cheap and it
hits two Meridian Test conditions at once, which matters because our own
measurements say nobody currently comments on recognising you: 1944 times out of
1944 the moment landed below the level where anyone speaks. A town that goes
quiet does not need words.
COST: moderate. We have the schedules and the heat already. The hard part is
making a bent routine still look deliberate rather than broken.

## Four questions only you can answer

**Does the town have an opinion, or only people?** KCD2 tracks your standing
separately in every town and separately per group within it. You ruled out a
global reputation number, for good reasons. But Meridian has seven districts and
three outfits, and nothing says the Hook thinks differently of you from the
Exchange. There is a version that is not the number you banned: not a stored
score, but a readout added up from what individuals already remember. Do you want
that, or is the answer still individuals only?

**What stops a player reloading to un-see a witness?** This is the one that
worries me. The moat assumes being seen is permanent; a save file makes it
optional. KCD2 makes saving cost a consumable, which works and is also the most
complained-about thing in both their games. Three options: accept that people
reload; make saving cost something; or save automatically at the moment you are
seen, so reloading costs the whole approach rather than the sighting. I lean to
the third, but it is a feel call.

**Does Meridian have a map?** Their hardest mode deletes the map marker and the
compass, and instead lets you ask a person for directions, who points at where
you are. In a one-town game people learn the streets by walking anyway, and
asking somebody is the same kind of verb as asking around for gossip, with the
bonus that they remember you asked. Map, no map, or both?

**Do the four already-built systems get put on the list?** Bookkeeping rather
than design, but the list is what everyone works from, and it cannot currently
see work we have already paid for.

## What I said no to

Almost everything else: their character stats, all 275 perks, skills that rise
with use, alchemy, blacksmithing, sharpening, archery contests, hunger, food
going off, illness, potions, carry weight, horses, fast travel, the dog, dice
and drink (already ruled out), reading as a skill, and their habit of explaining
nothing. Three reasons cover nearly all of it. Most is a private loop between
the player and a menu that nobody in Meridian can see. Some would actively hurt
us: serving a sentence in KCD2 wipes your criminal record, which is exactly the
reset you said never happens here, and selling stolen goods in the next town
along only works because they have next towns and we deliberately do not. And
one is admired for the wrong reason: KCD2 gets away with a punishing,
unexplained opening because it has a hundred hours to win you back. We have
thirty minutes.
