# How Hitman gets density out of a small place

Research topic 3. Hitman is our shape more than an open world is, so the
question was how it makes a small footprint feel full, and how a level stays
readable when it is crowded.

One warning before the findings: this is the worst-sourced topic I have done.
The two authoritative sources are IO Interactive's own conference talks, and
five different sites carrying them or writing them up are blocked from where I
work. Everything below is second-hand. If any of it turns out to matter, it is
worth re-running properly from the build machine.

## The main finding: density is connections, not size

Their lead level designer describes building a level as a spiral, a "snail
house" you can walk through without ever hitting a wall. Their lead game
designer puts it plainer: there are no dead ends, and you never need to
backtrack, though you can. They call the result Swiss cheese, meaning a volume
that is mostly holes, and they say straight out that their levels "feel larger
than they maybe are in terms of square meters because players can keep moving
ahead all the time."

So Sapienza, the level everyone calls their best, gets its size from how many
ways there are through it, not from how big it is.

For comparison, our own street file says Quay Street is 42 metres long with one
gap in the terrace, at the yard entrance. That is exactly right for what it is,
a single picture to prove the look. It is a corridor, not a snail house. The
moment that street has to carry a chase, a tail or a getaway, the difference
matters. **The rule worth holding the next street to: more than one way out, and
a different way back.**

## The thing I actually want us to take

IO grade every space in their game on two axes: how strong the rules are, and
whether anyone enforces them. Six kinds: public with no enforcement, public with
enforcement, public with strong rules, private with vague rules, private
professional, and private personal. They got the framework from two sociologists
you would not expect to find in a game studio, Bourdieu on social spaces, and
Goffman on the difference between how people behave front of house and how they
behave out the back.

That last one is the pub, in one sentence. The bar is front stage, the cellar
and the yard are back stage, and a crime game lives on the seam between them.

This matters to us more than it does to them, and here is why. In the coverage
audit I recommended taking their "blend in" idea, the thing where behaving like
you belong makes you invisible. That recommendation had a hole in it that I
could not fill at the time: I could say what the system does and not what it
reads. This is the missing half. Whether an action needs explaining is not about
the action. It is about what kind of space you are standing in and whether
anybody there is paid to care.

It costs a column in a spec. It buys the blend-in idea a definition, and it
gives every interior we author a shared vocabulary for what that room is for
socially, which each one would otherwise invent for itself.

## The uncomfortable part, and I have now hit it twice

When Hitman 2016 was nearly finished, their own player testing said people were
enjoying it but the learning curve was too steep and the scale of the first
level was, in their words, incomprehensible. Their fix was not to shrink
anything. It was to add guided routes through the sandbox, which is the thing I
recommended we say no to in the coverage audit, because hand-written guided
routes are the opposite of a world that generates its own stories.

So we refused their answer, which means we have inherited their problem. The
best studio in the world at this shipped a level their own testers could not
comprehend, and we are building something denser in information and thinner in
guidance.

This is the second time in two weeks of work that the same conclusion has come
up from a different direction. **I would move the topic on making emergent
stories legible up my queue.** It is currently seventh.

## Two smaller things

**A crowd is cheaper than you think.** Hitman Absolution ran 1200 reactive crowd
characters at 30 frames per second on 2012 console hardware. Our sim currently
has 65 walkers and no committed picture of anyone walking the Unreal street. The
gap is not a hardware gap. But I am deliberately not turning 1200 into a target,
because their crowd is characters with a behaviour and ours is people with a
schedule and a memory, which costs incomparably more. The useful takeaway is
narrower: a crowded street is not expensive because it is crowded. The
remembering is the expensive part.

**Verticality is already half-solved for us.** They built Sapienza on the Amalfi
coast's topography specifically to get layers connected by slopes and stairs.
Meridian has Fairview, residential hills, and we already did the research on
hillside housing for the atlas. And on the flat, a British terrace has its own
version: our street file puts first-floor windows at 3.4 metres across a
six-metre road, which means upper windows look into each other. That is exactly
the geometry the "man in the lit window is a witness" idea from the audit needs.

## What I did not get

The specific techniques from their guidance talk, which is the most useful part
of it. I know the problem they had and the philosophy they used. I do not know
their methods, and I have not pretended to.
