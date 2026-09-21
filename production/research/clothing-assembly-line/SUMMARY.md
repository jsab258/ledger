# Can we make clothes the way we make kerbs

One page. The long version is DELIVERY.md in this folder.

## The answer

Yes. Nothing about clothing is fundamentally harder than what we already do.

But the thing actually stopping us is not clothing at all. It is that we
cannot generate ANY new 3D object on your PC. The tool that turns a picture
into a 3D shape needs an NVIDIA card with 16 GB; yours is an AMD card with
10 GB, and there are three more reasons besides. So that station is shut for
coats and for kerbs equally. Every 3D object in the game today was made by
somebody else and downloaded; our pipeline cleans and measures them, it does
not create them.

Once you get past that station, clothing does not break anything that is not
small and ours to fix.

## Three things I found that change the picture

**Our people already wear separate clothes.** I opened all 18 character
files. Fourteen of them carry their clothing as its own piece, with names
like Hoodie, Pants, Suit, Shirt, Boots, Shorts. The Boss is wearing a
jacket that is a separate item. Joe is wearing a suit jacket. So we have
fourteen worked examples of exactly the thing we want to produce, sitting in
the repository, free. Last week's research said the clothes were fused into
the body. That was wrong and I had marked it as unverified at the time. I
have now looked.

**All 18 bodies use the same skeleton.** This is the one I expected to be
bad news. Every body we have carries the same 65 bones; four of them add a
handful of extras for hair and a cape and so on, on top of the same 65.
Mixamo labels each export slightly differently, which made my first
measurement say they shared nothing at all, but that was my measuring, not
the files.
So the hardest-sounding problem on the list, moving clothing between
different skeletons, does not exist for us. Moving a jacket from Joe to Kate
is moving it between two people built on the same frame.

**Blender already has the one command we need, and Blender is on your PC.**
One instruction transfers the clothing weights from a body onto a garment,
and it has a setting that means exactly "copy the bones that actually bend".
I could check this properly this time rather than guessing from a search
result: there is a package that lists Blender's entire set of commands for
exactly the version on your PC, and that package is downloadable from here.
It proves the command exists and what you can tell it to do. It does not
prove the command works on our files, which is what the afternoon is for.

## Two things of ours are broken, and both are small

Our mesh cleaning script destroys clothing, silently, in four lines. Those
four lines are all correct for a kerb: it scales it, sits it on the ground
and flattens it. Do that to a coat and the coat stops following the body.

Worse, our checker cannot tell. It counts corners and measures size, so a
coat that works and a coat that has been ruined look identical to it, and
both get a green tick. It would also mark a correctly made coat as a
failure, because it is written to expect a rigid object.

## What I would do

**Build the checker first, then spend one afternoon.** Not more research.
Everything left is a question that only a run on your PC can answer, and
there are four of them.

The checker is an evening's work and it has to come first. Without it, an
afternoon of trying this produces a file, a green tick, and no way to know
whether any of it worked. That is the failure this project has paid for
before.

Then the afternoon: take the jacket off The Boss, put it on Leonard and on
Kate, and see what happens. It costs nothing and answers everything left.

**I would not buy a clothing pack yet.** Not because buying is wrong, but
because a bought pack lands in the same broken cleaning script and the same
blind checker. Fix the two small things we own, prove them on a jacket we
already have, and then the question of buying is about how good the clothes
look rather than about whether the machinery works.

## One decision that is yours

Where do 3D objects come from at all. Pay for one of the generator services,
model things by hand in Blender, or keep reusing what we already hold. That
is the shut station, and it has nothing to do with clothes. I have not
proposed anything; it is a decision, not a task.

## Process note

The blocked-host problem has eased slightly. Vendor pages, Blender's website
and Epic's documentation are all still unreachable. But one software
repository is readable, which is where the Blender command list came from, and
most of this topic was answered by reading our own code and measuring our own
files rather than by reading anything external at all. So this delivery rests on measurements you can
re-run, not on search summaries. Everything I could not settle is listed
plainly at the end of the long version: four questions that one Blender
session on your PC would answer, and two others, of which one is worth
knowing about. Our licence rules name Mixamo ANIMATIONS as safe to ship and
do not mention Mixamo BODIES in words, and we have eighteen of the bodies.
That probably just needs writing down properly. It does not block trying any
of this.
