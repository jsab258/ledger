# Why the AI NPC demos felt hollow, and where we stand

Research topic 5. Every other topic asks what somebody did well. This one asks
what everybody did badly, in exactly the thing our second pillar promises.

## Five ways they failed

**They talk without saying anything.** A reviewer on Seed: "AI-powered NPCs can
talk and talk and talk, that's for damn sure. But they're not saying anything
worth listening to." Others called NVIDIA's demo characters stiff and robotic,
"more like an automated voice mailbox than an actual human", reading "from a
parody book of genre cliches". The problem is not bad writing. It is that
nothing they say is news.

**They will not push back.** NVIDIA's NPCs are reactive to questions, never
proactive, and completely deferential, and their own public pitch is that the
characters will not behave antagonistically. This is the sharpest of the five
because it is a choice, not a limit. A company selling this to studios cannot
demo a character who refuses you, lies to you, or takes against you, because a
demo that goes wrong does not sell. So the flagship product has a hole in it
exactly where a person would be.

**One wrong syllable kills it.** Seed's tutorial bot occasionally stresses the
wrong syllable, and reviewers said that single detail is instantly
immersion-breaking. This is asymmetric in a nasty way: a thousand correct lines
buy nothing, one wrong one costs everything.

**Personality with no consequence reads as none.** An inZOI player survey found
that "relationships grow through spammed identical dialogues with personality
having no impact". If what a character says does not change what the game does,
the talking is decoration and players find the shortest path to the meter
underneath.

**Players break it immediately.** In one MMO full of chatbot NPCs, players
promptly convinced them of absurd things and screenshotted the results. The
failure is not that players tried. It is that the world accepted it.

## The numbers, which are worse than I expected

Gamer sentiment toward generative AI in games is running at **77 to 83 percent
negative**, and the researchers note that a skew that strong is rare in years of
surveying players. Among developers, 52 percent now think it is harming the
industry, up from 30 the year before and 18 the year before that, and actual use
among developers has fallen to 29 percent.

There is no goodwill available. The only thing that reconciles our second pillar
with that number is the work being genuinely good, and I think that is worth
saying plainly rather than working around.

## What we already get right, and it is most of it

This is not reassurance, it is four specific structural defences.

**Against the empty talk and the jailbreaking:** our architecture does not let a
character say whatever it likes. Conversation outputs are classifications and
closed-set choices that the deterministic code executes, and the model never
decides an outcome. A character who can only say things the simulation licenses
cannot produce plausible nothing, and cannot be argued into believing something
absurd, because its beliefs are rows in a memory store rather than a chat
history. **I do not think this has ever been written down as the argument it is.**
If anyone ever asks in public why this is not the thing players hate, that is
the answer.

**Against the deference:** our own code already says the opposite. One file
notes that a killing "cannot be bought or scared quiet". Another documents a
state where they know you saw them and you do not, and calls it "the worst one,
and the game must allow it". A design that writes that down is not going to ship
a servile NPC.

**Against personality without consequence:** that is the entire moat, and your
no-global-number ruling is precisely what forces it.

## Two places we are not defended

**We already show two of the symptoms, and we have measured them.** Our own
inventory says "in 90 of 90 caught lies not one spoken line differed" and
"honesty pays nothing", and separately that recognition landed below the level
where anyone comments 1944 times out of 1944, so nobody says a word to you. That
first one is inZOI's failure in our own numbers. The architecture that prevents
it is right; the current build does it anyway. Measuring it is better than not
knowing, and it is not different in kind.

**The live conversation has no content safeguard, and Steam now asks for one.**
This is the finding I would most want you to see. Our content rule, the one that
forbids slurs, children, sexual content, alcohol and gambling, is enforced at
five places. I checked all of them against the path a live generated line takes
to the player, and none is on it. The validator that sees every reply does two
things: it shortens replies and it stops the character breaking the fourth wall.
The one content rule that is actual code guards the crowd generator, so it cannot
produce a child, and its three call sites are all crowd or body code. The
word-list gate runs over files in the repository at build time, not over
generated speech.

Meanwhile Steam rewrote its rules in January 2026. Games with content generated
live during play must now declare it AND **describe their safeguards against
inappropriate output, with removal from Steam for failing to**. We are a
live-generation case by definition. Our allowlist already anticipates the
declaration; it does not anticipate that the declaration requires a safeguard to
exist first.

I want to be honest about the limits of that check: I grepped the two files that
build the prompt and read the validator and the content rule. A prompt
instruction could live somewhere I did not look. But a prompt instruction would
be a soft guard anyway, and our own content-rule file makes that argument better
than I can: a generator "has to be UNABLE to produce the thing", because nobody
reviews three thousand residents.

## What I would do

1. Write down the structural argument in section "what we get right". It is the
   best answer we have to the 77 percent problem and it exists only implicitly.
2. Treat the content gap as a gap with a deadline rather than a design note. Not
   urgent this month; it is the one thing in my whole queue that an outside party
   will eventually check.
3. Put a quality floor on the voice work next to the speed floor. One wrong
   stress costs more than a hundred right lines buy, and nothing currently sizes
   correctness.
