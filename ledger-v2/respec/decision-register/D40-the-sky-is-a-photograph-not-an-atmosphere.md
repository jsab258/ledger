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
