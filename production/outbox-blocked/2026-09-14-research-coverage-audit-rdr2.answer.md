# What Red Dead 2 has that we do not

Coverage audit, game 3 of 5. I listed 36 things it contains and checked each
against our 91 systems. Most of Red Dead's excellence is in size, animation and
hand-made detail, which are the three things we have already decided not to
compete on, so the no pile is large again. Five things are worth taking.

## One result worth knowing on its own

You asked what NPCs do when you are not looking. In the most celebrated living
world ever made, the answer is: they stop existing. Red Dead's people despawn
when you walk away, and a person you kill is replaced by a different person.
Kingdom Come's carry on. So do ours: our headless run did seventeen days with
nobody watching and logged 346 sightings and 508 sounds. This is one axis where
we are already ahead of a hundred-million-dollar world, and I do not think we
have ever said so.

## Five things to take

**1. The town remembers the coat, not the face.**
In Red Dead, if people have seen you commit a crime in that clothing, they may
recognise you through a mask afterwards. This is the third game out of three
where what you are wearing is an identity, and it is the sharpest version:
changing your coat works until the new coat is the one they remember, and then
you need another. That is the "change your appearance rather than reset
anything" idea you already wanted, with a natural failure mode built in.
COST: small on top of what games 1 and 2 already recommend. This is the same
work, now confirmed three times.

**2. The minute between being seen and being reported.**
In Red Dead, a witness has to physically get to a lawman before anything
happens, and you can see them going, and chase, pay or stop them. In ours the
police effectively know the instant somebody believes it: our pressure
calculation counts any living witness who holds the rumour, with no travel and
no arrival. So the most valuable minute in a crime game currently does not
exist for us. It is also the minute where three verbs we already built (bribe,
intimidate, and the arithmetic for what killing a witness costs) would finally
have somewhere to happen.
COST: moderate. The change to the model is one term in one function. The work is
making that minute visible and playable.

**3. Nod or needle: something to do with everybody.**
Red Dead lets you greet or antagonise any person in the world. Our own notes say
the town will have thirty to fifty residents and that most of them are "a body
with a schedule". A body with a schedule you can nod at or needle is a person.
Two buttons, no conversation tree, and every use is something that person then
remembers, which is our whole game working on the smallest possible input.
COST: small. It is the cheapest thing in this audit.

**4. Weather as an event, not a condition.**
We already model rain changing what people can see and hear, and it wets nearly
fourteen thousand surfaces. What we do not model is rain changing what people
DO. A downpour that empties the street changes who could have seen you, which
turns weather from scenery into something you wait for. Given that wet, overcast
Britain is the look we committed to, it seems wrong that the weather currently
affects the picture and not the town.
COST: small. Both halves exist and neither talks to the other.

**5. Habits that belong to a person, not to the street.**
Red Dead's NPCs have schedules, and then small habits on top: a stable hand who
smokes and plays a harmonica. That sounds like decoration and it is not. A habit
makes a person predictable, and predictable people are both what makes a town
feel alive and what a player plans around. The man who steps out for a smoke at
the same time every evening is a witness you can avoid or a witness you can
count on.
COST: small. One more field on a routine that already exists.

## One question only you can answer

**Does the town have an opinion, or only people?** This is the same question
from game 1 and I am only flagging that it has now come up three times.
Kingdom Come tracks standing per town and per social group; Red Dead tracks
bounties per county; we track per person and you ruled against any global
number. Three games arriving at the same structure is at least evidence that
the structure is doing work. The question and the options are in the Kingdom
Come summary.

## What I said no to

Nearly everything else. The whole survival layer again (eating, warmth, health
meters), hunting, two hundred species of animal, horses, fishing, trains and
fast travel, random encounters, and the honour system, which is exactly the
single global number you ruled out and which turns out to be farmable by
greeting strangers repeatedly.

Two refusals are worth naming because they are the game getting it wrong rather
than making a different choice. Red Dead's lawmen recognise you through any
disguise, which is the psychic guard you already banned, shipped at enormous
expense, and the article explaining it is a guide for working around it. And
Red Dead puts a WITNESS banner on screen the moment you are seen. We already
decided against that one in our own code, deliberately, and the note explaining
why is better than anything I could add: you have a witness and no idea, no
warning, and the first you hear of it is a rumour three days later.
