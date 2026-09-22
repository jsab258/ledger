# D40. The sky is a photograph, not an atmosphere

Ruled by Jafar, 2026-09-15, answering the brief of the 15th. It overturns a
reasoned position written in the code on 2026-09-11 and the overturning is the
point of this record.

## The ruling, in his words

"A, the photograph becomes the sky. The reasoned position at
VignetteShot.cpp:163-171 was written before anyone compared a rendered sky
against the reference, and my sheet is overcast while the atmosphere renders
clear-sky blue. Scattering constants will not turn a clear sky into a soft grey
one. Record that this overturns that position and why."

## What is overturned

`VignetteShot.cpp:163-173` gives three reasons for a SkyAtmosphere and a
capturing SkyLight instead of the HDRI the shared spec names:

1. A `USkyLightComponent` takes a CUBE texture and this engine builds none at
   runtime.
2. `belfast_open_field_2k.hdr` is a long-lat Radiance file needing resampling
   into six faces AND a staging step to reach a packaged binary, which is
   three unverifiable links instead of one.
3. An atmosphere with a SkyLight capturing it makes the thing that is SEEN and
   the thing that is REFLECTED the same object, which an HDRI ambient beside an
   atmosphere backdrop would not.

HIS RULING DEFEATS 3 AND ONLY 3. Reasons 1 and 2 are not arguments, they are
work, and they remain true after this record. They are queue 186's, and the
builder solves them there or reports precisely why it cannot. A record that
let them be forgotten would be the shape of failure this project keeps finding:
an aesthetic call quietly deleting an engineering constraint.

## What his stated reason says, and what the measurement says

HIS CONCLUSION STANDS AND HIS STATED REASON DOES NOT SURVIVE MEASUREMENT. Both
are recorded because a record that smooths this over is worth nothing.

Measured 2026-09-15 on the brightest 30 per cent of the top band of each image,
so roofs are excluded, over the landed frame of run 44 and the Hook sheet panel:

    render      meanRGB 200.4/203.2/210.7   B over R 1.051
    Hook sheet  meanRGB 205.7/212.6/224.5   B over R 1.091

THE RENDER IS LESS BLUE THAN HIS OWN REFERENCE, not more. A clear daytime sky
runs well above 1.1 and often past 1.3; both of these are near neutral, and his
sheet is the bluer of the two. "The atmosphere renders clear-sky blue" is not
what the pixels say.

What the pixels DO say, over the same band:

    render      lumSD 2.21   p05 to p95 spread  6.7
    Hook sheet  lumSD 4.18   p05 to p95 spread 12.5

His sky has about twice the structure and is six points brighter. A flat
gradient has a small spread; cloud has a large one. So the difference he is
reacting to is most likely CLOUD rather than HUE: an atmosphere model produces
a smooth scattered gradient and cannot produce an overcast dome's structure at
all, which is exactly his second sentence, "scattering constants will not turn a
clear sky into a soft grey one". That sentence is right about the mechanism even
though the word blue is wrong about this frame.

## Why the ruling stands anyway

D23 gives him the frame. The reason offered for a judgement is not the
judgement, and a director does not overturn his call because his reason was
imprecise. There is also a measured argument FOR it that nobody made: the sky
visible from cam_hook is a narrow wedge at the end of a street, so the two
skies are compared over very little sky. The dusk frame he has asked for next
will show far more of it, and a flat gradient has further to fall there.

## What this does not decide

Not the sky's brightness, which already matches: `band.skyCentre.p50` reads
0.8035 against the sheet's 0.808, and that match survived run 44 untouched
because nothing in the sky wears the albedo grade. Not wetness, which is queue
186 and is the term still owed. Not whether the HDRI on disk is the right
photograph; it is the one the shared spec names and the first to try.

## Where the work is

Queue 186 carries the staging half and the two engine obstacles. This record
carries the ruling. The correction to the comment at `VignetteShot.cpp:163-173`
names this record, keeps reasons 1 and 2 visible as work, and does NOT claim
the atmosphere renders blue, because it measurably does not.

## Amendment A1, 2026-09-16: the ruling is the PHOTOGRAPH, not the binding

Ruled by Jafar twice on 2026-09-16, and recorded here because the first time he
put it in a budget message and it never reached this file. His words, the
second time, which are the ones that matter:

"I approved the overcast photograph as the sky, not a particular binding. Fix
the mechanism under D41 without asking; the ruling was the photograph, not how
it is wired."

And the first time, inside a budget line: "On the sky: I approved the
photograph, not a particular binding. If it needs a different asset type or a
different setup to render as a sky, do that under D41 without asking."

WHAT THIS AMENDMENT ADDS TO THE RULING ABOVE. D40 as written settles WHICH SKY
and leaves the two engine obstacles standing as work. It does not say who owns
the MECHANISM. This amendment says: the mechanism is D41's, which means visual,
which means ungated, which means no spawn asks him before changing it. A future
session that finds the binding wrong changes it and renders again; it does not
write a card.

## What was already true when he ruled it the second time

HIS PREMISE THE SECOND TIME WAS THAT IT HAD NEVER RENDERED, AND THAT WAS NO
LONGER TRUE. It is recorded rather than smoothed over, because a record that
quietly agrees with a stale premise is how a fixed thing gets fixed twice.

The `.hdr` WAS the wrong asset type for a runtime SkyLight, exactly as he
described, and that was obstacle 1 and 2 of the three above. It was re-bound
under D41 without asking, on 2026-09-16, as a long-lat PNG on an unlit dome
that a SkyLight captures. Runs 50 and 51 are the proof, and the keys are
quoted rather than summarised, from the landed verdict at commit 73c902b5:

    skyDomeMatIsSky=yes/from=bIsSky
    skyHdriBytes=2224812
    ambientModel=skylight-captured-sky=THE-PHOTOGRAPH-ON-THE-DOME
    skyLightLowerHemisphereSolid=yes/from=bLowerHemisphereIsBlack
    skyLumDriveWrote=32/ofWalks=32/noInstance=0

`bIsSky` is the engine's OWN sky-material flag, so "a texture Unreal does not
read as a sky" describes the state before the re-bind and not after it. The
frame was opened as well as the keys read, per CLAUDE.md rule 4: overcast sky
down the street and above the rooftops, four lanterns lit, wet road.

Night brightness, the three-way bracket, read in the ruled order:

    run 49   e1b4de77   no dome              meanLuma  43.6   floor
    run 50   654dd381   dome at 1.0          meanLuma 142.9   ceiling
    run 51   73c902b5   dome per condition   meanLuma  47.4

The ten day rows at `sky_intensity=1.000` moved by +0.1 between runs 50 and 51,
which is the undesigned null control that makes 47.4 a reading rather than a
coincidence.

## What is still open about the sky, so this record does not read as finished

The photograph's HORIZON BAND, trees and a dry field from 0 to about 11 degrees
of elevation, is visible at the vanishing point of the street: fogged and
subtle, but present, and a British port town's skyline is not an open field.
The horizon-fade rung is therefore open rather than hypothetical. It is visual,
so it is D41's and needs no ruling; it needs a render.
