# The voices: where they came from, and the one thing we stopped doing

Research topic 20. Topic 1 asked how the speech pipeline should be built and
topic 2 asked what it weighs. This one asks what we are allowed to ship, and
under whose rules. Nothing here is legal advice, and where it names law it is
reporting somebody else's reporting.

## First, the part that is right, because it is the part that cannot be fixed later

Your consent rule is stricter than the law requires:

> only corpora whose contributors donated their voices to build speech
> technology, and no identifiable public figures, ever.

Every voice in the game comes from VCTK, 110 people recorded in a treated room
at Edinburgh who volunteered specifically so that speech technology could be
built. That is the right sourcing, it was chosen deliberately, and it is the
reason nothing below is an emergency. A project that had scraped voices off
YouTube would be reading this page very differently.

Everything that follows is paperwork and plumbing.

## Three things, smallest first

### 1. We owe an attribution and we have not given it

VCTK is Creative Commons Attribution. It asks for exactly one thing in return:
say where it came from.

There are six attribution files in the project. All six are for props, decals
and city assets. **Not one of them mentions VCTK, Edinburgh or CSTR.** The only
place the corpus is named outside the fetch tool is a shopping list.

This is an afternoon's work and the easiest thing in the project to keep
forgetting, precisely because the six files that do exist make the area look
covered.

### 2. A rule we made mechanical only covers half the ground

We ban two text-to-speech models by name, because their weights are
non-commercial. That ban is real code, word-matched, with a proper test.

It lives in the tool that generates 3D props. **Nothing in any of the three
voice tools uses it.** A voice job naming a banned speech model would be
stopped by nothing but a person reading the allowlist.

Nobody is about to do that by accident. It matters as a shape rather than a
risk: we made a legal rule mechanical and wired it into one of our two
pipelines, and the one we missed is the one the rule was written about.

### 3. The watermark, which is the one with a clock on it

Chatterbox, our voice model, stamps every clip it makes with an inaudible
watermark that says "this audio was generated". Our own allowlist says to keep
it.

In August the export tool put a do-nothing stub in its place. That was a
correct decision and it was declared in writing at the time: the watermark is
applied after the pieces we were exporting, it was breaking the export on your
machine, and the note says plainly that the shipped game would have to make its
own decision.

**That decision was never made.** There is no watermarker anywhere in the game
code. The audio the game speaks today carries nothing.

Meanwhile the reason to keep it got stronger. The EU AI Act became fully
applicable on **2 August 2026**, six weeks ago, and the reporting on it says
providers must mark AI-generated audio in a machine-readable way. Our own
allowlist already bans one 3D tool on exactly this reasoning, "given
Switzerland plus likely EU reach".

I am not a lawyer and these are news sources rather than the law itself. What I
can say is: we told ourselves to keep it, we stopped keeping it for a good
reason, the good reason expired, and nobody went back. The engineering question
nobody has asked is whether the watermark can simply be reapplied after the
game decodes the audio. That is worth asking before it becomes a ship blocker.

## The one that is bigger than voices

Steam changed its AI rules on 16 January 2026. There are now two categories.
One is for AI content made during development and shipped in the box. The other
is for content the game **makes while you play**: dynamic NPC dialogue,
procedurally voiced characters.

We are in the second category twice over: our characters both write and speak
their lines live.

For that category Valve requires you to build guardrails that stop illegal or
offensive material reaching the player. That is a condition of being on the
store, not a design preference.

What we have: the validator that checks every reply says in its own header that
it does "two jobs only", length and not breaking character. Our content rule
exists, and it is called from three places, all three of which are the code that
builds bodies for the crowd. **Nothing screens what a character says, or what
the voice speaks.**

Worth knowing, in the allowlist's favour: it predicted the disclosure half of
this rule exactly, including the exemption for coding tools that Valve added in
January.

## What I would do next, cheapest first

1. **Write the voice attribution file.** One obligation, one afternoon, closed.
2. **Ask whether the watermark can be reapplied after the game decodes audio.**
   An engineering question, never asked, with a date attached to it.
3. **Point the banned-models check at the voice tools too.** The code exists.
4. **Decide what screens a live spoken line.** This is the big one, it is not
   really a voice question, and it is a Steam condition rather than a
   preference.

## What I could not check

The Edinburgh page that holds VCTK's licence and its speaker consent terms is
blocked from where I work, so I identified the licence through search summaries
and could not read what the speakers actually agreed to. Your inference that
they consented to this kind of use is reasonable and I could not verify it.
That page opens fine on your machine.
