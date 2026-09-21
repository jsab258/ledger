# Every photograph of 1990 is lying to us about one thing

Research topic 23. I went looking for what film stock made 1990 look like, and
the useful finding turned out to be about our reference material rather than
about our renderer.

## The problem, in one paragraph

Canon says the visual target is **wet, overcast, grimy Britain**. A wet overcast
British street is, physically, cool and grey and low contrast.

Now look at any surviving photograph of a British street in 1990. It is warm.
Yellowish. That warmth is not the weather. It is **Kodak Gold 200**, the film
almost every ordinary person used through the eighties and nineties, which
leans heavily yellow and magenta. Then it went through an automated high-street
minilab that applied its own correction, and then somebody scanned it decades
later with their own settings, and probably adjusted it again before posting it.

So between us and that street there are three or four layers of process, and
all of them touched the colour.

**Any art process that reads colour off period photographs will pull this game
warm, in exactly the weather canon says is the whole strategy.** And it will do
it consistently, because every reference agrees with every other one, which is
the sort of error that survives review.

## The good news: we already know how to fix this

There is a line in our own street spec that derives the colour of a sodium
street lamp from physics: the wavelength, through the standard colour matching
curves, into sRGB, with the working shown and a note saying the derivation was
run rather than recalled.

That is exactly right, and it is already ours. The rule it generalises to is
one sentence:

> **Photographs for geometry and material. Physics for colour.**

Photographs are excellent evidence of what was there, how big it was, what it
was made of, how worn it was, how people stood and dressed, what a shopfront's
layout was. Our atlas research already uses them that way and measures rather
than eyeballs. They are simply not evidence of what colour anything was.

## The film of 1990, if we do want to reproduce it

It has a name and a date. The **Eastman EXR family** was introduced on 17
January 1989: a slow daylight stock, a medium tungsten one, and a fast 500-speed
one. That fast stock is the one you would have used on a wet overcast British
day, and it was the grainiest of the three.

Which means something slightly awkward: **our target scene is the one where
period film looked worst.** Grain is not a tasteful garnish here. On the kind of
day this game is set in, it was the dominant texture.

People who do film emulation professionally name four ingredients:

1. **Colour response**: we have a tonemap, which is not the same thing
2. **Grain**: we have this, and ours is done well
3. **Halation**: we do not have it
4. **Gate weave**: we do not have it, and I would not add it (see below)

**Halation is the one worth having.** It is the reddish-orange glow around
bright lights, and it happens because light punches through the film and
bounces back into the red layer specifically. Our shader currently has BLOOM
where halation belongs, and bloom is the wrong colour. Halation is the effect
people read as "film" without being able to name it.

Gate weave is the tiny wobble of film in the camera. In a film you never notice
it. In a game it would be a permanent sub-pixel jitter on every frame anyone
ever plays, and I could not find anyone who has shipped it. I would leave it.

## The thing I keep finding

Our film grade (grain, vignette, bloom, tonemap, with a genuinely well-judged
grain curve) lives in `LedgerFilmGrade.shader`, which is Unity. **The Unreal
side has no grade at all.**

That is now the third time: the frame-rate readout, the graphics preset cost
model, and now the look. Three systems that represent real thinking, all built
and argued and tuned in the engine you retired on 10 September, none of them
ported, and nothing in the project currently counts them as outstanding.

Nothing is lost. But somebody should probably write down that they exist.

## One question nobody has asked

Making the **world** look like 1990 (what was there, what it was made of, what
the light did) and making the **image** look like 1990 (grain, halation, colour
response) are two independent decisions.

Canon leans towards the first: "weather and grime are the strategy, not
stylization". The art direction line our shader quotes asks for a little of the
second.

My own view, flagged as opinion: a heavy film look would fight the first
condition of the Meridian Test, since neither GTA nor Kingdom Come ships a
strong period grade, and a look that announces itself is a different thing from
one a player stops noticing after a minute. But that is your call and it has
never been recorded as a decision.

## What I could not find out

How much of that 1990 warmth is the film itself and how much is the high-street
printing machine. It is the single most useful thing to know here and no source
I could reach settles it.
