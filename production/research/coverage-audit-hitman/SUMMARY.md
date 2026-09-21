> **ONE ASK NARROWED.** `production/research/coverage-audit-rdr2/DELIVERY.md`
> section 3 corrects this delivery's ASK about showing the player who can see
> them: half of it is already decided in `Core/Observation.cs`, where
> `NeitherKnows` deliberately gives the player nothing. Read that section
> alongside this file.

# What Hitman has that we do not

Coverage audit, game 2 of 5. Hitman is the closest thing to our shape that
exists: a small dense place full of people, where the whole game is whether you
are being looked at. I listed 32 things it contains and checked each against our
91 systems.

More of it transfers than did from Kingdom Come. Ten of the twenty gaps I marked
as worth taking, against nine of thirty-five last time. That is not me going
soft: it is that almost everything Hitman has IS perception and evidence, which
is the list we said to fund. Two of the ten are small additions to others and
one is just paperwork, so five real things are below.

## Five things to take

**1. The people who see through a disguise are the people who know you.**
Hitman hand-places "enforcers", guards who recognise a fake uniform, and marks
them for you. We get the same thing free, and better: our own rule already says
recognition needs familiarity, so a change of coat works on strangers and never
on your regulars. Nothing in our plan names that as a system, which means nobody
can design the disguise verb against it.
COST: small. The rule exists. What is missing is the decision to treat it as
one thing.

**2. Behaving like you belong there.**
Our game can tell whether you were seen. It cannot tell whether what you were
doing needed explaining. Those are different, and the second is what makes a
busy street playable instead of a place where you are simply always visible. A
man at a bus stop at eight in the morning is invisible; the same man in the same
spot at three is something people mention. We already know what a reason to be
somewhere looks like, because every NPC has one.
COST: moderate. Mostly it is deciding what counts as a reason, which is writing.

**3. Bodies get found, at a time, by a person.**
We record a killing with a day, an hour and a place, and we track who saw it.
Nothing models the body lying in the yard until the man whose job it is opens
the yard on Tuesday morning. The gap between doing it and it being found is
where the tension of a crime game lives, and right now we do not have that gap.
COST: moderate, and it brings hiding a body with it, otherwise it is a timer
rather than a decision.

**4. The camera and the tape.**
You already specified this without meaning to. Canon says CCTV is rare, the bank
and one other place, tape recycled weekly, plus one camcorder in town. That is a
witness who cannot be talked to, cannot be frightened, never forgets, and has a
one-week clock. It is the opposite of the gossip mill, which is exactly why it
is worth having, and getting to the tape before Thursday is a whole kind of
evening we currently cannot offer.
COST: small. An object with a timer and a place.

**5. Finding a person from a description.**
Hitman's roguelike mode makes you pick the real target out of a crowd from
things like what they are wearing or that they sneeze. That is our own
recognition ladder run backwards: our rungs are literally "a man, big, long
coat" and "the one with the limp". At the moment that ladder only ever points
from the town at the player. Pointing it the other way, so a rumour gives Tom a
description and he has to find who it fits, turns the information side of the
game into something he does rather than something done to him.
COST: small in model terms, since the descriptions already exist. The work is a
screen and a reason to care.

Two smaller ones are argued in the full file and left out here: a doorman who
pats you down, and ringing a phone box to move somebody off a doorway.

## Two questions only you can answer

**How much does the player see of being watched, while it is happening?**
Hitman shows you, live, who can see through you and how close you are to being
noticed, and that readout is most of why a Hitman level is playable rather than
just crowded. Your own ruling says we never show what NPCs know as fact, only
what Tom could reasonably believe, and that there is no free look inside
anyone's head. I do not think those are necessarily in conflict: Tom walking
into his own pub would genuinely know which people in it know him too well for a
new coat to help, and that is his knowledge, not theirs. But where the line
falls is a feel call and it is yours.

**After it is over, does anything tell the player who saw what?**
Hitman ends every mission with a plain readout of what the world observed.
Ours is a town that never ends, so there is no natural moment for that, and the
whole design says you learn what people know by asking, listening and paying.
The risk is that the moat works perfectly and the player never notices it, which
is one of the four things the Meridian Test asks for. Do we ever tell them
directly, or never?

## What I said no to

The structure, all of it, and for one reason: Hitman is a box that forgets.
Every mission resets, so the clockwork can be wound up and broken as often as
you like, and everything clever about its shape depends on that. So no replay
loop, no mastery unlocks, no one-shot targets, and no Mission Stories, which are
hand-written guided routes IO added because their own testing found players
lost. We will hit that same problem and we have to solve it out of the
simulation instead, or the moat ends up being something a guided tour walks
past. I also said no to the two things that cheat: their "lookouts", who spot
you regardless of what you wear or where you are, and instinct mode, which shows
you everyone through walls. Both hand the player or the NPC knowledge nobody
earned, which is the exact thing our game is built not to do.
