# Photoreal on a budget: what actually carries a frame

Research topic 4. What small teams buy, what they fake, and what does the real
work. I have aimed it at where we actually are rather than at photorealism in
general: rung 1 is the built street matched to our own Hook sheet, with rain, a
wet road, worn materials and sky, judged by your eye.

## The first thing, and it changes an ordering we already have

**In an overcast scene the sky is not the background. It is the light.**

Under full cloud the sun contributes almost nothing and the whole grey hemisphere
does the lighting. Every guide agrees that image-based lighting from a sky is
the fastest way to light an exterior realistically, because it lights, shadows,
reflects and provides the backdrop all at once.

Our notes currently say the sky has to come before the wetness, and treat the
missing sky as blocking the wet pass. That is right and it undersells it. A
street with no sky is not a street missing its background. It is a street with no
light source. Which also explains the symptom we recorded: "the road reads near
white from its own albedo". With nothing for the exposure to sit on, the raw
material colour shows through.

So the sky is the highest-value item on rung 1, ahead of materials, props and
rain, for a stronger reason than the one written down. It is already queue 186.

## The second thing: overcast is forgiving for materials and brutal for shape

Our own pillar calls wet overcast Britain "the most forgiving photorealism there
is". For materials that is true, and diffuse light hides a lot.

For shape it is the opposite. Taking away directional light takes away the thing
that tells an eye where a surface turns. That is why overcast photographs look
flat and overcast renders look like grey plastic.

The named fix is worth having written down before you judge rung 1: put small
soft fill lights back in where shape matters, without letting them read as sun.
If your reaction to the first correct overcast street is "it looks flat", the
answer is fills, not more contrast in the grade.

## The third thing: of the five "cinematic" effects, only one is doing the job

Tonemapping is the one that decides whether an image reads as PHOTOGRAPHED at
all, because it maps brightness the way a camera does. Film grain, chromatic
aberration, vignette and bloom do something different and smaller: they make an
already-photographic image look like it was shot on a particular kind of camera.

Both matter to us, but they are different jobs. The first belongs to rung 1. The
second is really a period question, what 1990 looked like on film, which is
another topic in my queue. Worth not confusing them, and worth checking that the
Unreal side is tonemapping properly before anything is layered on top, because
grain on an untonemapped image just looks like a bad photograph.

## The fourth thing, and it pays twice

The standard way small teams get dense-looking environments without drowning in
work is trim sheets and tiling materials: a handful of reusable surfaces, blended
and masked in the engine, rather than a unique texture for every wall. Wear goes
into vertex colours, which have four channels, so edge wear, dirt and rust can
ride in the same mesh without any new textures at all.

One developer reports going from about 100 to over 130 frames per second and
"much less texture memory usage" after switching. Treat that as a direction, not
a number.

**Here is why it pays twice.** The hardware topic found the floor is a memory
wall, and that texture memory is the biggest controllable piece of what the
street costs. So the technique that makes a small team's street look dense is
the same technique that makes it fit on the card. That is now the second time in
this queue that two topics have independently recommended the same thing, and it
was right the first time.

And we are unusually well placed to do it. Our street is generated from one file
with nothing hand-placed. A generator can emit trim-sheet coordinates and wear
colours as easily as it emits positions. A hand-built street cannot be
retrofitted cheaply. Ours can, right now, because it is a file. That window
closes when things start being placed by hand.

## The fifth thing: real surfaces from a phone, free and clean

Epic's RealityScan is free on iPhone and Android including for commercial use,
with no export limit. A surface you photograph yourself is your own work: no
weights licence, no attribution chain, nothing to re-verify at ship. Given that
our licence allowlist is law and every other art route carries conditions, that
is unusually clean.

What to capture is not British architecture. It is British surfaces. The atlas
research has already covered period form, clothing, housing, household contents,
the pub plan. What no amount of reading supplies is what forty years of rain does
to a brick, a kerb, a painted shopfront or a rusted downpipe, and that is what
"wet, overcast, grimy" is actually made of.

The catch: you are in Switzerland. Brick bond, kerb profile and shopfront
proportion are British and cannot be captured there. Weathered render, moss,
rust, wet asphalt, peeling paint and concrete staining largely can. Which of them
travel is a question for whoever leads the art, not for me.

## One correction to a piece of advice you will be given

"Just use Megascans, it is free with Unreal" was true for five years and stopped
being true at the end of 2024. Epic began charging in 2025 and it is a
marketplace now. Our allowlist already has this right, it says Fab purchases
under the Fab Standard License plus the CC0 libraries, so nothing needs changing.
I am flagging it only because somebody will offer that advice.

## What I would do

1. The sky, treated as lighting rather than background.
2. Check what the Unreal side's tonemapping is doing before grading on top of it.
3. Expect flat, and know the fix is fill lights, not contrast.
4. Put wear into vertex channels and surfaces into a trim atlas while the street
   is still a generator.
5. Try exactly one phone capture, end to end, and see what it costs in hours.
   One wet kerb through the whole pipeline would teach more than any reading.

## What I could not find

I could not find a single solo-developer postmortem with real numbers on what
buying assets actually saved them. Plenty of forum posts, no measurements. That
belongs to two later topics in my queue and I have not pretended to answer it
here. I also have not read the Unreal probe's rendering setup, so point 2 above
is aimed at a chain I have not seen.
