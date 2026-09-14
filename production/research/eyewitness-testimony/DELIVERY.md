# Topic 10: eyewitness testimony, as validation for the five-rung ladder

STATUS: SPEC (research delivery). Branch `research/eyewitness-testimony`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written, no constant changed.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged: no
external page was read in full, which matters here because this is a large
experimental literature and I have abstracts and summaries of it. Repository
claims name their file and line.

The brief asks for this as validation. Section 1 is what validated, section 2 is
one number worth checking, section 3 is two missing couplings, and section 4 is a
question I am handing to topic 24 rather than answering.

## 1. What the ladder gets right, with the numbers behind it

### 1.1 The distance structure

CITED (search summaries of Nyman, "The Distance Threshold of Reliable Eyewitness
Identification", the Psychonomic Bulletin and Review paper "Effects of distance
on face recognition: implications for eyewitness identification", and the Abo
Akademi summary):

- Accuracy for young adults "dropped from 96% at 5 meters to 42% at 20 meters".
- "In optimal viewing conditions (daylight, no distractions, 20 second duration),
  eyewitness accuracy was only approximately 50% at 5 to 10 meters."
- "At 40 meters the accuracy was approximately 30%, and after 100 meters,
  line-ups had no added value", with "an upper distance threshold at 100 m".
- "In low light the upper distance threshold is considerably shorter; after 20
  meters identification accuracy is at chance level."
- "Increased distance had a more pronounced negative impact than lighting."

Against `ledger/Assets/Scripts/Core/Perception.cs`, read this session:
`DetectRangeMetres = 40.0`, `Rung1SilhouetteMetres = 35.0`,
`Rung2MarkMetres = 18.0`, `Rung3FaceMetres = 8.0`, `Rung4RecogniseMetres = 25.0`,
every one scaled by `LightFactor`.

DERIVED: the shape is right and the scale is conservative in the correct
direction. Our detection range of 40 m is where the literature puts 30 percent
identification accuracy, and our model calls that DETECTION rather than
identification, which is the correct distinction. Our rung 3, a face at 8 m, sits
exactly in the band where the literature measures about 50 percent accuracy in
optimal conditions, and rung 3's own text is "I'd know him again" rather than a
name, which is again the correct distinction. Nothing in our ladder claims
something the literature says is impossible.

### 1.2 The light model's shape

`LightFactor(0) = 0.12`, `LightFactor(0.25)` is about 0.34, `LightFactor(0.5)`
about 0.55, `LightFactor(1) = 1.0`, and it multiplies every rung's range.

DERIVED: at a sodium-lit street of, say, light level 0.25, our rung 3 becomes
8 x 0.34 = 2.7 m and rung 4 becomes 25 x 0.34 = 8.5 m. The literature puts
low-light identification at chance beyond 20 m. Our night thresholds sit well
inside that, so the model is conservative rather than generous. For a game whose
pillar is a wet, sodium-lit, overcast town, having the night model err toward
"they could not have seen you" is the right way to be wrong.

### 1.3 The thing I expected to find missing and did not

**`Core/Observation.cs` already implements the confidence-accuracy dissociation,
and its own comment claims the science.** Read this session, at
`Observation.Retell`:

> MEMORY HARDENS AS IT DECAYS: accuracy falls, confidence rises. A hesitant "a
> big man in a long coat" becomes, after a week of telling it, a certain "it was
> Tom Novak", with no new observation, purely from retelling. It is true of real
> witnesses [...] a witness left alone gets MORE dangerous.

`RetellingsPerRung = 4`; each retelling adds 0.10 to certainty up to a 0.94
ceiling; every fourth retelling climbs the rung; and climbing to rung 4 with no
name attached takes the name from what the witness already expected, which the
comment calls "the mechanism, not a side effect".

**CITED, and the claim is correct.** (search summaries of Nolo's "The Psychology
of Eyewitness Identification" and the Kentucky Department of Public Advocacy's
misidentification page): "those who express great confidence in their
identifications are no more accurate than those who admit to uncertainty", and
"delayed interviews allow memories to fade and become contaminated".

AND THE NUANCE MAKES OUR MODEL LOOK BETTER, NOT WORSE. One source I found is
titled "Black-and-white? When eyewitness confidence counts and when it doesn't",
which implies the modern position is conditional rather than the flat claim
above. HOLE: I could not read it, and the current consensus in this field is
something I have only in outline, that confidence is diagnostic at the FIRST
identification under clean conditions and stops being diagnostic afterwards.
If that outline is right, then our model is not merely defensible, it is exactly
right: `Observation.Certainty` at the moment of the sighting is meaningful, and
`Retell` is what makes later certainty meaningless. Somebody should read Wixted
and Wells before this paragraph is relied on.

## 2. One number that now has a series to be checked against

`Observation.Misattribute` sets the chance a witness names the wrong man:
`p = o.Rung == 1 ? 0.45 : 0.25`, applied at rungs 1 to 3, with rung 4 treated as
certain.

CITED, from 1.1: in optimal viewing conditions accuracy is about 50 percent at 5
to 10 metres, which is the band our rung 3 occupies.

DERIVED: **the literature's error rate at rung 3's distance is roughly 50
percent. Ours is 25 percent.** Our witnesses are about twice as reliable as real
ones at the same distance in the same light.

I am not proposing a change, for two honest reasons. First, the two numbers are
not measuring quite the same thing: the studies measure a formal identification
from a line-up of a stranger seen once, and our rung 3 is a witness's own
recollection in a town where they may see the person again. Second, rule 2 says
set a bound from a printed series, and one summarised figure is not a series.

What I am recording is that `p = 0.25` was set without one, and that there is now
a literature with numbers in it to set it from. That is the useful output: the
number is checkable, and it was not before.

## 3. Two couplings the literature says should exist and our model does not have

### 3.1 Weapon focus: the slots should compete, and they are independent

**This is the finding of the topic.**

`Core/Observation.cs`'s header states the architecture: "A violent act is a short
sequence [...] and a witness catches WHICHEVER PARTS their senses reached. Seven
slots, filled independently."

Filled independently is the design and it is what the literature contradicts.

CITED (search summaries of Fiveable's social psychology entry on the weapon focus
effect and Nolo's overview): "Eyewitnesses confronted by a weapon are apt to
focus on the weapon rather than the person holding it", and more precisely, "the
weapon focus effect is the tendency for attention to lock onto a weapon during a
crime, which reduces memory for other details; eyewitnesses may remember the
weapon clearly but forget the attacker's face, clothing, or actions."

DERIVED, and it maps onto our slots exactly: the literature says catching
`Slot.Draw` should REDUCE the chance of `Slot.Actor`, and of the clothing a rung-1
identification is made of, and of `Slot.Act`. Three of our seven slots are the
ones the effect names, and the effect is one of the better-replicated results in
the field.

**Our seven-slot decomposition is not just validated by this, it is the right
shape to express it.** A game that asked "did he see it" could not model weapon
focus at all. Ours can model it as one coupling between two slots it already has.
And the design consequence is rich rather than fiddly: pulling a weapon buys you
a witness who is certain about the weapon and vague about you, which is a real
trade a player could learn.

### 3.2 Memory conformity: witnesses who talk should change, not just agree

CITED (search summary of Nolo and the Psychology Town overview): "discussing
events with other witnesses corrupts individual memory", and "leading questions
may suggest a particular answer and lead to misinformation".

Our mill passes BELIEF between people. `Core/Gossip.cs` moves a `Rumor` with a
`Confidence`; the underlying `Observation` of a witness who hears a different
version is untouched.

DERIVED, and it is the same gap topic 9 found from the other side: two witnesses
who talk to each other should converge, and the literature says the convergence
can pull a correct memory toward a wrong one. In our model they simply each hold
their own. Topic 9 found no term for independent corroboration RAISING belief;
this is the same absence seen from the memory end, and it is arguably the more
damaging one, because it means the gossip mill cannot corrupt the evidence it
carries.

### 3.3 And one shape question, smaller

`LightFactor` multiplies range, so halving the light and halving the distance are
interchangeable. CITED, from 1.1: "Increased distance had a more pronounced
negative impact than lighting." A multiplicative model makes them symmetric.
Flagged as a shape mismatch, not costed, and much less important than 3.1.

## 4. One finding I am handing to topic 24 rather than acting on

CITED (search summaries of the Race and Social Justice Review piece and the APA
record for "A synthetic perspective on the own-race bias in eyewitness
identification"): "Eyewitnesses are less accurate when asked to identify someone
of a different race [...] Approximately 42% of wrongful convictions based on
misidentification involved cross-racial errors."

This is real, large, well-replicated, and period-appropriate for a British port
town in 1990. It is also a parameter that would make a perception system less
accurate as a function of a character's race, and the question of whether that
belongs in this game is not a research question.

`canon.md`'s D18 is the relevant rule: "Racism and sectarianism may exist as
FACTS ABOUT CHARACTERS, never voiced as slurs, never rewarded." A cross-race
identification penalty is neither a slur nor a reward, so D18 does not obviously
forbid it, and D18 also does not obviously invite it.

**I am recording it and recommending nothing.** It belongs to queue topic 24, the
ethics and reception risks of a crime game with a real social memory, and it is
the sharpest example that topic is going to get: a mechanic that is scientifically
correct, thematically apt, and capable of reading extremely badly in a review.
Flagged now so that topic 24 starts from a concrete case rather than an abstract
worry.

## 5. What could not be established

1. **Every paper.** Same limit as topic 9: this is an experimental literature and
   I read abstracts and summaries of it. Several of the key sources
   (psycnet.apa.org, tandfonline, springer) were not fetched.
2. **The modern confidence-accuracy consensus** (1.3), which I have only in
   outline and which decides whether our `Retell` model is defensible or exactly
   right. Wixted and Wells is the reading.
3. **A usable error-rate series** to set `Misattribute`'s p from (section 2). One
   summarised figure is not a series, and the studies measure a different task
   from ours.
4. **Any effect size for weapon focus** (3.1). I establish that the effect is
   well attested and names our exact slots; I have no number for how much
   catching the weapon should cost the face.
5. **Any effect size for memory conformity** (3.2).
6. **Whether familiar-person recognition at distance has been measured**, which
   is the single most load-bearing number in our ladder. `Rung4RecogniseMetres`
   is 25 m, gated on `RecognitionFamiliarity = 0.35`, and the file calls it "the
   most characteristic number in the project". Every study I found measures
   STRANGER identification. Recognising someone you know is a different task,
   almost certainly much better, and I could not find it measured. **That is the
   research gap I would most want closed on this topic.**
7. **Not covered:** line-up procedure and its effect on accuracy (sequential
   versus simultaneous, blind administration), which is a large applied
   literature and bears on topic 6's identification parade rather than on the
   ladder; earwitness identification, which our model has as a hearing channel;
   and the effect of stress, which is contested.

## 6. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Nyman, "The Distance Threshold of Reliable Eyewitness Identification", https://psycnet.apa.org/fulltext/2019-38765-001.pdf and https://www.researchgate.net/publication/334409261_The_distance_threshold_of_reliable_eyewitness_identification
- Springer, "Effects of distance on face recognition: implications for eyewitness identification", https://link.springer.com/article/10.3758/s13423-014-0641-2 and https://pubmed.ncbi.nlm.nih.gov/24820456/
- Taylor and Francis, "The masked villain: the effects of facial masking, distance, lighting, and eyewitness age on eyewitness identification accuracy", https://www.tandfonline.com/doi/full/10.1080/1068316X.2023.2242999 and https://centaur.reading.ac.uk/118712/1/
- Abo Akademi, "Could you correctly identify someone wearing sunglasses from a distance of 20 meters?", https://www.abo.fi/en/news/could-you-correctly-identify-someone-wearing-sunglasses-from-a-distance-of-20-meters/
- PsyPost, "New research sheds light on challenges eyewitnesses face in identifying criminals", https://www.psypost.org/new-research-sheds-light-on-challenges-eyewitnesses-face-in-identifying-criminals/
- Nolo, "The Psychology of Eyewitness Identification", https://www.nolo.com/legal-encyclopedia/the-psychology-eyewitness-identification.html
- Psychonomic Society, "Black-and-white? When eyewitness confidence counts and when it doesn't", https://featuredcontent.psychonomic.org/black-and-white-when-eyewitness-confidence-counts-and-when-it-doesnt/
- Kentucky Department of Public Advocacy, "Eyewitness Misidentification", https://dpa.ky.gov/kentucky-department-of-public-advocacy/about-dpa/kip/causes/misid/
- Fiveable, "Weapon Focus Effect", https://fiveable.me/social-psychology/key-terms/weapon-focus-effect
- APA PsycNet, "A synthetic perspective on the own-race bias in eyewitness identification", https://psycnet.apa.org/record/2016-53658-008
- Race and Social Justice Review, "White Eyes, Huge Lies: The Pitfalls of Cross-Race Eyewitness Identification", https://race-and-social-justice-review.law.miami.edu/white-eyes-huge-lies-the-pitfalls-of-cross-race-eyewitness-identification/
- National Academies Press, "Identifying the Culprit: Assessing Eyewitness Identification", chapter 5, https://nap.nationalacademies.org/read/18891/chapter/7
- Psychology Town, "Assessing Eyewitness Testimonies: Techniques and Challenges", https://psychology.town/forensic/assessing-eyewitness-testimony-techniques-challenges/

Repository sources, read this session at commit `074f85b`:
`ledger/Assets/Scripts/Core/Perception.cs` (the constants, `LightFactor`,
`InSight`, `IdRung`), `Core/Observation.cs` (the `Slot` enum and its header,
`Misattribute`, `Retell`, `RetellingsPerRung`), `Core/Gossip.cs`, `canon.md`,
`production/systems-inventory.json`.
