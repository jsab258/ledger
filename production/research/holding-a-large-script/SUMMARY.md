# The thing that broke Disco Elysium cannot break us, and a different thing can

Research topic 26. You asked what holds the words. The answer turned out to be
three gates, two of which run automatically and one of which does not.

## First, the good news, and it is structural rather than lucky

Disco Elysium had over a million words in Articy, a visual tool that draws
dialogue as a branching flowchart. Its lead writer says it "got quite janky, at
some point froze completely, because it definitely wasn't built for it."

**Our dialogue is not a branching flowchart.** A bank is a flat list. Each line
is four fields: an id, a rung (stranger, Novak, Tom), a context (greeting, deed
reaction, gossip pass), and the text. Three rungs by three contexts is nine
boxes holding forty-eight lines. There is no tree, no path, no node.

You cannot freeze a flat list. That specific disaster is not available to us,
and buying a graph tool to avoid it would be insuring a building we do not own.

For scale: we have **65,769 words** of authored speech and cards today. That is
6.6% of Disco Elysium's million. The corpus that broke the tool is fifteen times
ours.

## The half of their story that was not about software

This is the part I would not skip. Their writer:

> we were writing too much. Like, there wasn't enough time to edit it, to go
> over it, we would have to cut some parts.

And then they decided not to cut, because the writing was good.

A faster tool fixes nothing about that. It is a judgement made at the moment
volume has already outgrown the process, and it is exactly the judgement a
project with your standard is most likely to make.

## What holds our words today

Three gates, and they are all word lists:

1. **The content gate** (D18): 10,058 strings scanned, no new hits, 197 known
   violations baselined and counted down.
2. **The slop check**: nineteen signs-of-AI-writing patterns, a ratchet at 86 of
   88 that may only go down, with the bark bank and the cards held at zero.
3. **The canon gate**: era terms and real brands. Clean today.

The first one demonstrably catches what a human would not. Our pub bank's very
first line is:

> Evening. You'll be the one that got the pub, then. Mickey kept the mild on the
> left.

Period-perfect, in register, and it breaks D18's absolute alcohol rule. Nobody
reading five thousand lines catches that twice running. The gate did, named the
rule, and it is already in the 197.

## The thing I found by opening a file

I had written this page saying I had not read the canon gate. Your own rule 3
says open the file instead of reporting it missing, so I did, and it changed the
answer twice.

**It works.** Run over both banks and the bark file it reports "0 findings in 3
files, 97 lines examined, 13 era terms and 45 brand tokens screened". It is also
unusually honest: its docstring says tone is not mechanical and it refuses to
pretend to check it.

**And nothing runs it.** I grepped every script, workflow and config in the
repository. Nine references, and every single one is a DOCUMENT: decision
records and learning-log rows. `verify.py` runs the content gate and the slop
check before every commit. It has never run the canon gate.

One of those decision records says it in as many words: "tools/canon-gate.py was
NOT run here. I did what the gate does by hand."

So: two of the three gates are held by the build, and the third is held by
somebody remembering. It is green whenever anyone runs it, which is exactly why
it looks fine in every record that mentions it.

## The failure we actually have

Not freezing. **Contradiction.**

At five thousand lines, line 3,012 says the pub opens at eleven and line 418 says
half ten, and not one of our three gates can see it, because both lines are
clean, in period, in register, and not repeating each other.

Three things make that sharper for us than for an ordinary game:

- **Our corpus is what the language model reads, not just what the player
  reads.** The character cards are 13,564 of those 65,769 words, and a card
  block goes into EVERY SINGLE conversation turn. A wrong fact in a card is not
  one wrong line, it is a wrong premise in everything that character will ever
  say.
- **Consistency is the moat.** Topic 25 found players reliably notice NPCs
  forgetting, and no research measures them noticing memory that works. A
  self-contradicting corpus is the authored form of forgetting.
- **The volume is planned to grow and the tooling is not.** Two banks today,
  thirty to fifty residents at phase 2.

## What I would do, cheapest first

1. **Have `verify.py` run the canon gate.** It already exists, it already
   passes, it already prints its denominators. One line.
2. **Nothing else, yet.** No tool purchase, no format change. The JSON diffs
   cleanly in git, which matters more here than anywhere, because every gate you
   have reads files and every claim carries a footer.

If a tool ever becomes worth it, the two candidates are Ink and Yarn Spinner,
both of which I confirmed are MIT by reading their actual licence files rather
than a summary. Articy is commercial and, more to the point, stores its script
in a form git cannot diff, which would remove the review surface this whole
studio runs on.

---

EGRESS NOTE, now standing in every delivery: exactly one route out of this
container reads a page in full, and it reaches source repositories and package
registries only. That is how the two licences above were read properly. Research
literature, news, journals and vendor documentation are all unreachable, so
anything cited from those is a search engine's summary and is labelled as one.
