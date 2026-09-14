# Live speech: the problem we were about to solve is already solved

Research topic 1. The question was whether the voice experiment we wrote in
August is still the right next step, or whether the architecture needs changing
first. The answer turned out to be neither, and the reason is worth two minutes.

## The number in the brief is out of date

The plan says our voice model generates speech slightly slower than it plays
back, so streaming would stutter. That sentence is still sitting in the
document. But further up the SAME document, someone recorded on 12 August that
they fixed it: keeping the model's memory on the graphics card instead of
shuttling it back and forth made each step 17 milliseconds instead of 42, with
no slowdown as a sentence gets longer, and the output bit-for-bit identical.

So we generate speech more than twice as fast as it plays. The line computes
faster than it speaks even without streaming. The document contradicts itself
because nobody went back to update the summary table at the bottom after the
work at the top succeeded.

Four of the six experiments in that plan have already run. Two have not.

## But the margin is much thinner than it looks

The "twice as fast" number only counts one half of the work. Because of a crash
we hit in August, the speech steps and the audio rendering have to take turns on
one thread, never at the same time. So the real budget is: for every second of
speech, do 25 steps AND one render pass.

Doing that arithmetic on our own numbers: about 0.93 seconds of work for every
1.00 second of speech. It fits, by seven percent. Seven percent is not a margin,
it is a rounding error, and that is measured on a machine that is not yet also
running the game, the conversation model, and a rendered street.

## The thing worth doing

Resemble AI, who make the voice engine we chose in July, released a faster
version of it after our measurements were taken. Its headline change is exactly
the half of our budget that is too big: they distilled the audio rendering step
from ten passes down to one. We use four passes.

If that holds up, our budget goes from 0.93 seconds per second to about 0.55,
and time-to-first-word goes from roughly one second to roughly 0.64 seconds.
That second number matters more than it looks, because the only outside
benchmark anyone offers is that voice systems feel natural up to about 800
milliseconds and degrade reliably past one second. We are currently sitting
exactly on the bad line and this would put us comfortably on the good side.

It is also low risk on paper: same company, same family, same MIT licence
already on our approved list, and they publish it in the same file format our
whole pipeline already uses.

## Two things I could not check, and one of them decides it

**Does the new version keep the "exaggeration" control?** We chose this engine
in July specifically because of it, and you heard the difference yourself in the
direction test. A faster model that cannot do moods is not an upgrade, it is a
different decision. I could not establish this.

**Does it run on AMD?** Our machine is an AMD card and the game has to ship for
both. The new version's documentation mentions NVIDIA, AMD's Linux stack, and
plain CPU, and never mentions the Windows path we actually use. This is the one
that decides whether any of the above is usable.

Both need HuggingFace, which is blocked from where I am working, so both have to
go through the build machine.

## What I recommend

Do not build the streaming worker yet. Its whole design is shaped by how long
the audio rendering pause is, and that is the number about to change by a factor
of four. Building around it now means designing for a constraint that may not
exist.

Three measurements first, in this order:

1. **Measure the rendering pause.** It is the biggest term in the budget and the
   only one in my whole analysis that is an estimate rather than a real number.
2. **Answer the two questions above about the new model.**
3. **Time the conversation model's reply.** It has never been measured once. Our
   own document calls it "the leg nobody has measured". If the text takes two
   seconds to arrive, saving four tenths of a second on the voice is irrelevant,
   and nobody knows which world we are in.

## On paying a service to do the voices instead

No. Priced out, a line of dialogue costs between a tenth of a penny and about
two pence depending on the provider. A thirty-hour playthrough would cost
between roughly nine and a hundred and eighty dollars, per player, every time
somebody plays, on a game they bought once. It also means the game does not work
without an internet connection, and it sends our nineteen cast voices to a third
party, which reopens a licensing question that is currently closed. Worth
keeping only as a convenience for hearing a line without a graphics card.

## One small thing that pleased me

NVIDIA now ships a text-to-speech plugin for Unreal Engine aimed at exactly this
use case, with a 350-million-parameter model. It is the same engine we picked in
July. A hardware company productised our choice, which is a reasonable sign we
picked right.
