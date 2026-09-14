# Topic 9: rumour propagation, against the literature rather than our assumptions

STATUS: SPEC (research delivery). Branch `research/rumour-propagation`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written, no tunable changed.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged: no
external page was read in full, which is a heavier limitation here than usual
because this is an academic topic and the papers are the sources. Repository
claims name their file and line.

Batch 2's brief says these topics change the moat's design. This one is written
as a comparison: what the literature says, what `Core/Gossip.cs` does, and where
they differ. Section 3 is five differences and one of them is an internal
contradiction in our own code.

## 1. The famous model is contested, and it is the one everybody would reach for

CITED (search summaries of "The rumour spectrum" in PLOS One, the ScienceDirect
article on Bartlett's serial reproduction, and the ResearchGate entry for "The
experimental study of the transmission of rumour"): Allport and Postman (1947)
used serial reproduction and proposed that rumours are "levelled" (loss of
detail), "sharpened" (emphasis of some details) and "assimilated" (distorted
toward the hearer's expectations), and found that "as the story progressed along
the chain it became shorter". Replicated by Higham (1951).

**AND THEN:** CITED (same PLOS One source): "studies of naturally occurring
rumours have not found levelling and sharpening consistent with Allport and
Postman's work and found that some rumours are actually extended (Rosnow and
Fine, 1976) or undergo minimal or no change (Prasad, 1935)."

There is also a paper titled "Cite Unseen: Distortions of the Allport and Postman
Rumor Study in the Eyewitness Testimony Literature", which is a paper about the
canonical study being systematically misrepresented by the people citing it.

DERIVED, and it is rule 3 applied to a literature rather than an instrument:
**the model a designer would reach for is a laboratory result from 1947 whose
central finding does not reliably reproduce in the wild, and which is
widely cited wrongly.** A game that implemented levelling and sharpening as the
mechanism of rumour distortion would be implementing a contested finding, and
would be doing so because it is the one everybody has heard of.

What survives, and is the useful part: rumours change in transmission, and the
direction of change is NOT reliably toward less. Some grow. That is a different
design from a decay.

## 2. What the literature does say, that we could use

**Transmission has motives, and there are three of them.** CITED (search summary
of DiFonzo and Bordia's work, including "Rumor Psychology: Social and
Organizational Approaches" and "Ferreting Facts or Fashioning Fallacies? Factors
in Rumor Accuracy"): "Rumor transmission is motivated by three broad
psychological motivations, fact-finding, relationship-enhancement, and
self-enhancement, all of which help individuals and groups make sense in the face
of uncertainty."

**Rumours have three states, and the third is the interesting one.** CITED
(search summary of "Theory of Rumour Spreading in Complex Social Networks" and
the arXiv work on rumour spreading in community-based networks): "The classic
rumor spreading process models each node as being in one of three states:
ignorant, spreader, or stifler." A stifler knows the rumour and has stopped
passing it on.

**Weak ties carry information far; strong ties carry the complicated kind.**
CITED (search summaries of the arXiv papers on complex contagion in small-world
networks and "Time varying networks and the weakness of strong ties"):
Granovetter's finding that "people often obtain job referrals through weak ties
rather than strong ties", and the qualification that "while weak ties are
effective in transmitting information quickly across long distances, they may not
be as effective in complex contagion".

**People choose who to tell, strategically.** CITED (search summary of
"Knowledge of information cascades through social networks facilitates strategic
gossip", Nature Human Behaviour, 2025): "people use knowledge of social network
structure, popularity and distance, to strategically spread gossip, drawing on
internal models that capture cascading dynamics of information flow across
network ties."

**And somebody has modelled exactly our case.** CITED (title and abstract via
search summary): "Gossipping Until You Get Tired of It: A Network Model of the
Adaptive Exchange of Rumors in a Small Scale Social Environment". HOLE: I could
not read it. Of everything in my queue, this is the paper whose title most
exactly describes what LEDGER is, and it is the one I most want read.

## 3. Five differences between the literature and `Core/Gossip.cs`

Read from the file this session. The model: an undirected weighted acquaintance
graph, rumours carrying a structured `Fact` and a `Confidence` in 0 to 1,
propagated in `Tick` when two people are together.

### 3.1 We decay confidence per hop. The literature does not say confidence decays.

`Core/Gossip.cs:141` sets `HopDecay = 0.8`, and line 371 applies it:
`passed = r.Confidence * tie * HopDecay`. The file's own header says why: "third-
hand rumor carries less weight than an eyewitness account."

That is intuitive and it is not what section 1 found. Distortion in transmission
is real; monotonic decay of BELIEF is not established, and natural rumours
sometimes strengthen. Our model conflates two things the literature separates:
how much the story has changed, and how much the hearer believes it.

NOTE ON THE NUMBER ITSELF, under rule 2: 0.8 appears under a comment that reads
"Tunables". I found no measured series behind it, and the literature offers no
value for it because it does not use this shape.

### 3.2 Our rumours die of weakness. Real ones die of boredom.

`MinConfidenceToShare = 0.2` (line 142), enforced at lines 363 and 372: below
that, nobody passes it on. So a rumour's death in our mill is the arithmetic
consequence of hops.

The classic model's third state, the stifler, is a person who still believes the
rumour perfectly well and has stopped repeating it, because it is no longer news.
DERIVED: those produce different worlds. Ours says a rumour reaching the far side
of town is a faint one. Theirs says the far side of town may hold it as firmly as
the first teller and simply not mention it again. The second is the one that
matches a small town, where "everyone knows and nobody says" is an ordinary
condition, and it is exactly the texture canon's late-analog Britain wants.

### 3.3 We have no independent corroboration, and that contradicts our own design

**This is the finding of the topic.**

`Core/Gossip.cs:308`: when a witness hears a fact they already hold,
`already.Confidence = Math.Max(already.Confidence, confidence)`. Line 313 only
overwrites if `confidence > already.Confidence`. Line 382 skips entirely when
`existing.Confidence >= passed`.

DERIVED, and it is arithmetic rather than interpretation: **hearing the same
thing from two different people is worth exactly as much as hearing it once from
the better-placed of them.** There is no term anywhere for independence of
source. Line 520 notes that "DISTINCT stories corroborate", which is a different
mechanism about the hidden life, not about one fact from two mouths.

And that is at odds with the project's own stated thesis, one file away.
`Core/Informing.cs`'s header: "**truth is not an input.** A true accusation
nobody will corroborate is ignored. A false one three people will swear to
lands." `HomicideBook`'s own comment, quoted there: "Every witness after the
first. Corroboration is what turns one person's word into a case."

So corroboration is the whole thesis of how the LAW weighs a claim, and the MILL
that produces the people who would corroborate does not model it. A person in
Meridian can be told by three separate neighbours that Tom did it and end up
exactly as certain as if one had told them.

I am not proposing the fix; that is design. I am recording that two files in this
repository disagree with each other about the most important mechanism either of
them has, and that the literature is on `Informing.cs`'s side.

### 3.4 Our ties are backwards for reach

Line 371 multiplies by `tie`, so a strong tie passes a rumour at higher
confidence and a weak tie at lower. Our model therefore says information travels
best between close friends.

Granovetter's finding is the opposite for REACH: weak ties are how information
crosses a network, precisely because strong ties are redundant (your close
friends mostly know each other and already know what you know). The qualification
matters and is in section 2: weak ties are worse for complex contagion, which
is the kind of transmission that needs several exposures.

DERIVED: a rumour about the player is simple contagion, one fact, easily
repeated. So the literature suggests our weakest ties should be our best
carriers, and our model makes them our worst. In a seven-district town with
three rival organisations, that is the difference between talk staying in the
Hook and talk reaching the Exchange.

### 3.5 Our transmission has opportunity but no motive

`Tick` passes a rumour when two people are together (the `together` predicate)
and the tie and confidence clear their floors. That is pillar 1's schedule
intersections, and it is the right spine.

What it has no term for is DiFonzo and Bordia's three motives. Nobody in our mill
tells a story because it makes them look good, because it draws them closer to
the hearer, or because they are trying to work out what is true. The tile "the
cast" already records the related problem: the generator "supplies names, not
people". A mill where everyone transmits identically is a mill where nobody has a
reason to talk, and the coverage audit found the same failure in inZOI from a
different direction.

## 4. What this adds up to

Five differences, and they are not equally important.

- **3.3 is a defect**, because two of our own files disagree and one of them is
  the moat's thesis.
- **3.2 and 3.4 are design choices made without knowing they were choices.**
  Both are defensible; neither is documented as a decision; both produce a
  materially different town.
- **3.1 is an unmeasured number in a shape the literature does not use**, which
  is rule 2's case exactly.
- **3.5 is a known gap** with a known consequence, already visible elsewhere in
  the project.

And the meta-finding, which is section 1: **the model everybody reaches for is
the wrong one.** If this project had gone looking for rumour research and stopped
at the famous answer, it would have implemented levelling and sharpening, which
is a 1947 lab result that natural rumours do not reliably show and that the
literature citing it routinely misstates.

## 5. What could not be established

1. **Every paper.** This is an academic topic and I read no paper. Every claim
   is the search channel's summary of an abstract or a citing page, and for a
   topic where the whole point is what the evidence actually says, that is a
   serious limitation. Four hosts that would carry these papers are blocked from
   here.
2. **"Gossipping Until You Get Tired of It"** (section 2), which models an
   adaptive rumour exchange in a small-scale social environment, is the closest
   thing in the literature to LEDGER and I could not read it.
3. **Any number for a hop decay**, because the literature does not use that
   shape. So 3.1 identifies a shape mismatch and offers no replacement value.
4. **Whether independent corroboration has a measured effect size.** I establish
   that the literature treats multiple sources as central and that our model has
   no term for it; I do not have a number for how much a second independent
   source should be worth.
5. **The illusory truth effect** specifically, which is the mechanism by which
   repetition raises belief without raising accuracy. I went looking for it in
   the rumour literature and the search returned DiFonzo and Bordia's general
   work instead. It is a large, well-replicated literature in its own right and
   it is the obvious next thing to read for 3.3.
6. **Not covered:** rumour CORRECTION (what makes a denial work), which is the
   half of this literature that bears on the player's ability to fight back, and
   which topic 10 partly touches from the eyewitness side.

## 6. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- PLOS One, "The rumour spectrum", https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0189080 and https://pmc.ncbi.nlm.nih.gov/articles/PMC5774683/
- ScienceDirect, "Bartlett revisited: Direct comparison of repeated reproduction and serial reproduction techniques", https://www.sciencedirect.com/science/article/abs/pii/S2211368114000485
- ResearchGate, "The experimental study of the transmission of rumour", https://www.researchgate.net/publication/229483566_The_experimental_study_of_the_transmission_of_rumour
- ResearchGate, "Cite Unseen: Distortions of the Allport and Postman Rumor Study in the Eyewitness Testimony Literature", https://www.researchgate.net/publication/240134366_Cite_unseen_Distortions_of_the_Allport_and_Postman_rumor_study_in_the_eyewitness_testimony_literature
- DiFonzo and Bordia, "Rumor Psychology: Social and Organizational Approaches", https://www.semanticscholar.org/paper/Rumor-Psychology:-Social-and-Organizational-DiFonzo-Bordia/640f90505de7b6f184288e00937b49971be948b3
- Wiley, DiFonzo (2010), "Ferreting Facts or Fashioning Fallacies? Factors in Rumor Accuracy", https://compass.onlinelibrary.wiley.com/doi/10.1111/j.1751-9004.2010.00321.x
- ScienceDirect, "Corporate rumor activity, belief and accuracy", https://www.sciencedirect.com/science/article/abs/pii/S0363811102001078
- Nature Human Behaviour, "Knowledge of information cascades through social networks facilitates strategic gossip", https://www.nature.com/articles/s41562-025-02241-2
- ResearchGate, "Theory of Rumour Spreading in Complex Social Networks", https://www.researchgate.net/publication/222819843_Theory_of_Rumour_Spreading_in_Complex_Social_Networks
- ResearchGate, "Gossipping Until You Get Tired of It: A Network Model of the Adaptive Exchange of Rumors in a Small Scale Social Environment", https://www.researchgate.net/publication/372776111_Gossipping_Until_You_Get_Tired_of_It_A_Network_Model_of_the_Adaptive_Exchange_of_Rumors_in_a_Small_Scale_Social_Environment
- arXiv 2607.08546, "Rumour Spreading In Community Based Networks", https://arxiv.org/pdf/2607.08546 (EGRESS BLOCKED)
- arXiv 1303.5966, "Time varying networks and the weakness of strong ties", https://arxiv.org/pdf/1303.5966 (EGRESS BLOCKED)
- arXiv 1503.00448, "The Routing of Complex Contagion in Kleinberg's Small-World Networks", https://arxiv.org/pdf/1503.00448 (EGRESS BLOCKED)
- arXiv 1410.8175, "Randomized Rumor Spreading in Poorly Connected Small-World Networks", https://arxiv.org/pdf/1410.8175 (EGRESS BLOCKED)
- Janet L. Falk, "Understanding and Managing Rumors", https://www.janetlfalk.com/pdf/Killing_Rumors.pdf

Repository sources, read this session at commit `074f85b`:
`ledger/Assets/Scripts/Core/Gossip.cs` (header, the `Rumor` and `GossipMill`
types, `Tick`, and the tunables at lines 139 to 142),
`ledger/Assets/Scripts/Core/Informing.cs`, `Core/Homicide.cs`,
`production/systems-inventory.json`, `canon.md`,
`ledger-v2/respec/vision-pillars-v2.md`.
