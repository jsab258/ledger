# Making being watched readable

Research topic 12. This one answers a question I have now put to you twice and
could not resolve either time.

## The question, and the one sentence that settles it

In the Hitman audit I asked how much the player should see of being watched while
it is happening, and flagged that your own information ruling says we never show
what NPCs know. In the Red Dead audit I narrowed it, because our own code had
already settled the hardest case: when nobody has noticed you noticing, the
design gives the player nothing, deliberately, and the first you hear is a rumour
three days later.

Thief settles the rest, and the answer is in the reason the light gem exists at
all: it "serves as a helper to give players information that they cannot
experience themselves, because they cannot see their own body in a first-person
view."

So the rule is: **a readout is fair when it gives back something the character
knows and the camera took away. It is cheating when it adds something the
character does not know.**

Garrett knows perfectly well whether he is standing in a pool of light. The
player, looking out through his eyes, does not. The gem returns what the camera
removed. And notably it does NOT tell you what the guard is thinking, which
during development was the other half of the confusion and which they left
deliberately unsolved.

That is clean, it needs no change to your ruling, and it is the principle I could
not put my finger on in either earlier write-up.

## Which means we should not copy the light gem

We are third person. The player can already see whether Tom is under a lamp,
whether his coat is dark, whether he is crouched. Giving him a light gem would be
returning something the camera never took, and by the rule above that is the
cheating kind.

So the useful question is what our camera DOES hide. Three things, and all three
are already on my recommendation list from other topics:

- **Being watched from behind.** Tom would feel a stare. The camera shows him a
  back.
- **Who in this room knows him well enough that changing his coat will not
  help.** That is his own knowledge, not theirs, and your ruling surfaces the
  player's own memory in full.
- **What is on his own coat.** Blood on the back of a coat is precisely the case
  the light gem was invented for: a fact about your own body you cannot see. So
  the appearance recommendation I have now made four times arrives with its
  interface question already answered.

And the thing the camera does not hide, and so should not be given: whether any
particular person is currently suspicious of you. That is a mind.

## The rules everyone else follows

Every stealth game that works has three guard states, and only three: unaware,
investigating, hunting. The middle one exists specifically so the player gets a
chance to react. And two rules come up everywhere: a state change has to be
readable the instant it happens, and, in the bluntest phrasing I found,
**"subtle doesn't work."**

They are also read from behaviour rather than from a bar. Alertness shows in
posture, in a head turning, in a walk becoming a run. Which is the cheap half, and
it lands on something I have recommended twice already from other games: a person
who stops, turns and looks at you for two seconds is an alert state, rendered
diegetically, with no interface at all.

Our own model has four states, but they are a different and more interesting
axis: they describe who knows that who saw whom. That is not a substitute for an
alert ladder, and whether we need one is a design call.

## One warning, and it is the third time this has come up

A Splinter Cell designer says that "one of the difficulties with modern stealth
games" is realistic lighting, because environments have become so much "harder to
read".

We have this problem in the worst possible form. Our visual bar is photoreal wet
overcast Britain. Our perception code scales every recognition distance by the
light level, so light is not atmosphere, it is the mechanic: at a sodium-lit
street our face-recognition range shrinks from eight metres to under three. That
is an enormous mechanical difference that the player has to read off a photoreal
frame. And our night lighting is not built yet.

This is the third time in this batch that the same conclusion has arrived from a
different direction. Photorealism made emergent stories harder to follow in topic
7, and it makes shadows harder to judge here. **Every system that asks the player
to read the frame pays for the visual bar.** That is not an argument against the
bar, which is decided. It is a bill that comes with it, and it is now itemised
three times.

## One thing worth knowing before someone suggests it

Splinter Cell justifies its visibility meter inside the fiction: it is a gadget in
Sam Fisher's suit, wired to light sensors. Tom Novak has no such gadget and 1990
has no such technology, so that route is closed to us. Anything we show has to be
justified as something Tom notices, not something he measures.
