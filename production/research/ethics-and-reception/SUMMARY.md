# Two risks, one number, and one decision I am not going to make for you

Research topic 24. Topic 10 ended by handing this one a specific problem rather
than a vague worry, and I take it up at the bottom of this page. First, the
thing with an actual measurement on it.

## The number

Someone analysed **508,192 Steam reviews**. Games that disclose using generative
AI get a **17.9 percentage point lower recommendation rate**: 68.4% against
86.3%. The negative reviews say "AI", "soulless", "lazy".

Separately, 52% of game industry professionals in this year's big survey said
generative AI is having a negative impact on the field, up from 30% last year.

That is the bad news and I am not going to dress it up.

## The part of the same study that matters more

The researchers found a clear split in **what** players are punishing:

> When AI was the game's premise (such as LLM-driven dialogue) players evaluated
> it on its interactive merits rather than as a cost-cutting measure.

The penalty attaches to AI used as a **substitute for creative work**. It does
not attach to AI used as **the thing the game is**.

**We are on both sides of that line at once.**

- **The conversations are the good side.** Nobody can hand-write
  memory-conditioned dialogue for fifty residents who remember what you did on
  Tuesday. It is not replacing a writer; it is a thing writing cannot do. On
  this study's own terms, players judge that on whether it is good.
- **The art and the voices are the bad side.** Generated props, textures,
  concept sheets and synthesised speech are exactly the "content that ships in
  the box" that carries the penalty. That we generate them because there is no
  art department is true, and the study did not find players making that
  distinction.

The honest defence of the second half is not "it isn't AI". It is the quality
bar you already hold, and that is a claim reviewers test rather than accept.

## What genuinely protects us, and it already exists

I want to be clear that this project is in unusually good shape on the ethics
side, and the reason is specific and unusual.

Run `tools/content-gate.py --enforceable` and it prints:

> WHAT THIS GATE ENFORCES MECHANICALLY: 7 of 18 clauses. The rest are named
> below and are NOT claimed.

It then names the eleven it cannot enforce and says why. "Nothing here can tell
a card that says a man is a bigot from a card that endorses him." "A thesis is a
reading of the whole work." "No word gate can see that. Somebody opens the file."

Almost nobody does this. A project that publishes the ratio between what its
rules enforce and what they merely assert is legible to a sceptical reader in a
way that no quality claim is. If the AI question ever gets asked in public, that
tool is a better answer than any sentence I could write.

(It currently reports 197 known violations waiting on a content pass, zero new,
flagged as a list to be emptied and never grown. That is a healthy state four
days after the rule landed.)

## The gap that is not a judgement call

Everything that gate checks is a **file**. Dialogue banks, cards, image prompts,
the brand bible.

**Nothing checks what a character says live.** The validator on the live path
does two things, by its own description: reply length and not breaking
character. Our content rule is never consulted.

The clauses most likely to be broken by a language model writing 1990 British
dialogue are the two most absolute ones we have: **no slurs of any kind** and
**no children anywhere**. The slur list exists. The running game never reads it.

Steam now requires guardrails on live-generated content as a condition of being
on the store. So this one is required, it is implied by a rule canon calls
permanent, and it is unrelated to anything below. It should not wait.

## The decision I am handing you

Topic 10 found that eyewitnesses are significantly less accurate identifying
someone of a different race, and that around 42% of wrongful convictions from
misidentification involved cross-racial errors. It is real, large, heavily
replicated, and true of a British port town in 1990.

Our perception system has exactly the shape to implement it: a five-rung
identification ladder with misidentification probabilities.

**For it:** it is true; it indicts the justice system rather than any person;
and our moat already argues that human testimony is unreliable and gets more
confident as it gets worse. D18 does not forbid it.

**Against it:** a player who notices it does not read a research finding, they
read a game rule saying people of one race cannot tell people of another apart.
There is no room in play to explain the context. It would require the game to
hold **racial categories as live simulation data**, which it currently does not.
And D18's own instinct runs the other way: it permits racism as a fact about a
person and forbids the depiction and the reward, whereas this is a rule about a
population.

I searched four ways for any game that has done this, in any framing, and found
none. There is no precedent either direction.

**I am not recommending either way, and that is deliberate.** Across
twenty-four topics this is the one where I think my opinion is worth less than
the arguments.

**But here is a smaller question you could answer instead:** does LEDGER hold a
racial category per character as simulation data at all? Everything above
follows from that, it has a clear answer, and it does not require you to
adjudicate a psychology finding.

## One correction

In topic 22 I said nobody had decided how corrupt Meridian's police are. That
was wrong. D18 says it: "Police are corruptible as individuals, never as a
thesis." I had not read the content rule when I wrote that.
