# Motion capture on no budget: is it worth doing?

Research topic 8. You asked me to say plainly whether it is worth doing at all.

**No. Not now.** There is one small exception at the end, and it is not a mocap
pipeline.

## The reason is licensing, and it is worse than "free mocap libraries" sounds

The free academic mocap world has one enormous archive, AMASS, which pulled about
two dozen separate research datasets into a single usable format. It is the thing
that made free mocap practical.

**AMASS cannot ship.** Its own licence grants use "for the sole purpose of
performing non-commercial scientific research, non-commercial education, or
non-commercial artistic projects", and specifically prohibits "incorporation in a
commercial product".

What is left is the raw source that AMASS tidied up. Carnegie Mellon's database,
2,500-odd sequences, free, from the early 2000s, and widely used commercially.
Usable, and twenty years old.

## And the restriction follows the AI models downstream

This is the part I did not expect.

The standard training set for text-to-motion AI, the "describe a movement and get
an animation" tools, is called HumanML3D. It is 14,616 sequences taken directly
from AMASS, and it cannot even be distributed as a file: you have to download
AMASS and rebuild it.

Which means every open text-to-motion model, the ones you would reach for to
produce "the handful of movements nothing else has", was trained on data that
explicitly forbids commercial use.

I want to be careful here, because whether a model's OUTPUT is restricted by its
training data is a genuinely contested legal question and I am not qualified to
answer it. What I can say is that the chain is documented by the projects
themselves, and that this is exactly the case our allowlist already has a rule
for: it says verify the weights licence, not the code licence, and it already
lists two voice models on the never-ship list for precisely this reason. These
belong in the same category until somebody qualified has looked.

## What it would actually cost

For twenty bespoke movements, assuming three to five seconds each:

- If we had studio-quality capture: about 3 to 5 hours of cleanup, at the
  industry figure of two to four hours per minute of animation.
- From phone video and pose estimation, if the takes are good: about 3 hours.
- From phone video, if the takes are bad: **20 to 60 hours.**

Plus capturing it, retargeting it, importing it, and doing it again when it is
wrong.

So somewhere between twenty and eighty hours of skilled animation work. We do not
have an animator. That is not a budget line, it is a hiring decision.

## Four other reasons, all of them already in our own files

- Animation parity with mocap studios is already on your "worse at, and at peace
  with it" list, which exists so nobody quietly reopens it.
- The visual ladder puts "one face that moves" at rung five. We are on rung one.
- **The animation system we already have is not connected to anything.** Our own
  notes say the motion-matching file has no caller in the game layer. Adding
  twenty bespoke clips to a system nothing calls is building a second floor with
  no stairs.
- The route we are on works. Mixamo is free, on the allowlist by name, 2,500
  clips deep, and our own notes say the clips are advancing and the feet are
  solved.

## The one thing I would do

Not a mocap pipeline. **A foot-sliding cleanup tool.**

Foot sliding is the single biggest tell of amateur animation, and everyone agrees
on this: even a small amount destroys the illusion of weight, and audiences spot
it instantly without knowing what they are looking at. The two-to-four-hours
figure is for fixing it BY HAND.

But it is not a taste problem. It is geometry, with a published algorithm going
back decades and a modern machine-learning version: find the frames where a foot
should be planted, pin it, blend in and out, adjust the hips to compensate. Four
mechanical steps.

That is exactly the shape of work this studio is good at, and unlike a mocap
pipeline it improves the sixty-four clips we already have, immediately, and comes
with a number we can watch.

## What I could not establish

**D28 does not exist.** You cited it as parking animation polish until
presentation is right. There is no D28 in the register, which runs D1 to D18, and
no mention of it anywhere in the repository. This is the second record cited in
my brief that is not here; the other was D24. I have used the policy as you
stated it, because two things that ARE in the files agree with it.

I also could not read the actual Carnegie Mellon licence text, only descriptions
of it. Before anyone ships a clip derived from it, somebody should read the terms,
because "widely used commercially without issue" is a statement about practice
and not about permission.

And on AI-generated video as a motion source, which you asked about specifically:
my searches returned marketing pages rather than any real evaluation. Your own
framing, that generated footage has soft physics which the pose estimators then
inherit, is the most substantive thing I have, and I could not improve on it.
