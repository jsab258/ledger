# Topic 11: social network structure in small towns

STATUS: SPEC (research delivery). Branch `research/small-town-networks`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written, no constant changed.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged: no
external page was read in full. Repository claims name their file and line and
were produced by commands run this session.

The brief's reason for this topic is "so schedule intersections are not uniform".
Section 2 answers that. Section 3 is a decayed claim I found on the way and have
to report, because it is about the rung the whole design turns on.

## 1. What the structure actually is

### 1.1 The layers, and the ratio between them

CITED (search summaries of "Calling Dunbar's numbers" on ScienceDirect and its
arXiv preprint, the PMC paper "Reflecting on Dunbar's numbers", UpHabit's
summary and the US Army's write-up of the study): the theory gives "cognitively
efficient social groups of sizes 5, 15, 50, 150 and 500, with layers that differ
in terms of strength of relationships"; people dedicate "nearly 40% of their
socially-oriented efforts to these five most important people" and "a further 20%
of emotional energy [...] to the next ten closest", so 60 percent goes to fifteen
people; the 50 layer is an "affinity group" whose relationships are "less about
emotional support and closeness and more about providing useful connections and
information"; and 150 is "the full active network [...] with whom you may connect
once a year". The whole thing is "a fractal series [...] created by
sub-structuring the 150 into smaller subgroups".

DERIVED: the ratio between layers is about three, and the distribution of
attention is steeply unequal. **A uniform tie-weight distribution is not a
simplification of this structure, it is a different structure.**

### 1.2 Two mechanisms make the shape, and they compound

CITED (search summaries of "Cumulative effects of triadic closure and homophily
in social networks" in Science Advances, the arXiv paper on disentangling them,
and Kleinberg's networks chapter): clustering, or triadic closure, "measures the
probability that if a randomly selected node is connected to two other nodes,
then these two nodes are also connected"; homophily is "the tendency to form ties
with similar others", called "one of the most robust sociological principles";
and their "dynamic interplay [...] amplifies homophily and creates
core-peripheries in social networks", such that "even small individual bias may
prompt network-level changes such as segregation or core group dominance".

And the sentence that matters most for us: homophily "can produce a division of a
social network into densely-connected, homogeneous parts that are weakly
connected to each other."

## 2. What this says about Meridian, which is the brief's question

### 2.1 The districts ARE the network's community structure

`canon.md` gives seven districts, each with a character: the Hook (old port), Copper
Row (market), the Exchange (offices, lawyers), the Parade (nightlife), Fairview
(residential hills), Ironside (industrial), Gullwing (faded resort). And three
rival organisations.

That is, in the literature's own words, a network divided into
"densely-connected, homogeneous parts that are weakly connected to each other".
Homophily by trade, by street and by allegiance produces exactly the districts
canon already names.

DERIVED, and it is the answer to "so schedule intersections are not uniform":
**the non-uniformity is already authored and nothing reads it.** The tile "the
town layout" (exists) holds "seven districts with home and work shares"; the tile
"daily routines" (exists) puts people somewhere for a reason. What the gossip
model does not do is treat a cross-district tie as structurally different from a
within-district one. The research says it is the DIFFERENT KIND, not merely a
weaker one.

### 2.2 And it compounds with topic 9's finding, in the bad direction

Topic 9 found that `Core/Gossip.cs:371` passes a rumour at
`Confidence * tie * HopDecay`, so a strong tie carries better and a weak tie
carries worse, which is backwards from Granovetter for reach.

Put that together with 1.2. If districts are dense clusters weakly tied to each
other, then the few cross-district ties are BOTH the only route between
communities AND, in our model, the worst carriers. DERIVED: talk would pool in
the district where it started and arrive at the Exchange, if at all, as a whisper.

That may be what the design wants. A crime in the Hook that the Exchange never
hears about is a legitimate and interesting town. But it is currently an
accident of two unexamined choices rather than a decision, and it is the single
most consequential structural consequence I have found in the gossip model.

### 2.3 The authored cast fits inside one person's Dunbar 50, and the crowd does not

The tile "the cast" (partial) says "the town needs 30 to 50 residents at phase 2".
The tile "the crowd you see" reads 65 walkers.

DERIVED, and it resolves an apparent tension rather than creating one: a cast of
30 to 50 fits ENTIRELY inside a single person's affinity layer, the one the
literature describes as being about "useful connections and information" rather
than closeness. **So among the authored cast, nobody should be a stranger to
anybody.** Everyone has at least heard of everyone. Meanwhile the crowd is the
strangers, and should be.

That is a clean division and it matches what `Core/Acquaintance.cs` already says
about why it matters: "A face in the crowd. Cannot name you at any distance, in
any light, however long they stare, which is correct, and is what makes a busy
street safer than an empty one where your neighbour lives."

The design consequence, offered as an observation: the player's safety is a
function of WHICH crowd, and the authored cast is never safe cover.

## 3. A decayed claim I have to report, because it concerns the top rung

`Core/Acquaintance.cs`'s header makes a strong present-tense claim:

> `Witnesses.Resolve` takes a `Func<NpcWalker,double>` for familiarity;
> `ViolenceHost.Commit` takes one and passes it through; and **no caller
> anywhere has ever supplied one**, so it defaults to null, every witness scores
> 0.0, and every person in the city is a stranger to a man they have known for
> three acts [...] Rule 6, in its purest form: built, tested in Core, and never
> called.

**That is no longer true in this checkout, measured this session.**
`Game/GameController.cs:78` defines `FamiliarityWithPlayer`, assembling the value
from `Acquaintance.Of(sharesYourHome, walksWithYou, inTheSocialGraph,
hasHeardOfYou)`, and its own comment says it was written precisely to close this
gap. `Game/SimDirector.cs:6522` passes `_game.FamiliarityWithPlayer` into one
call site and `:7196` into another.

So the fix exists and is wired. The claim in `Acquaintance.cs` describes the world
before it, in the present perfect, and a reader arriving at that file today is
told the top rung is unreachable when it is not. That is rule 1's decay case, and
the reason I am reporting it here rather than filing it is that my boundaries
forbid me touching code.

**WHAT I DID NOT ESTABLISH, and it matters.** The inventory, typed 2026-09-09,
still records "every recognition beat measured sat below the rung at which
anybody comments, 1944 of 1944". I cannot tell from this checkout whether that
measurement predates the fix or survives it. So the correct statement is
narrower than "the problem is solved": **the 1944 of 1944 can no longer be
attributed to a missing familiarity function, and what it should now be attributed
to is unknown.** A run would settle it and I cannot make one.

ONE MORE THING FOUND IN THE SAME GREP, and it is small but it is a magic number:
`Game/NpcWalker.cs:919` calls `Perception.IdRung(metres, light, familiarity: 0.5,
...)` with the value written as a literal rather than taken from the function.
0.5 is `Acquaintance.Known` and sits above `RecognitionFamiliarity` of 0.35, so
every crowd walker on that path is treated as somebody who can name the player.
I have not traced what that path feeds and am recording it rather than
interpreting it.

## 4. What follows, as findings

1. **Tie weights should be layered, not uniform**, at roughly 5 / 15 / 50 with a
   ratio near three and a steeply unequal attention distribution (1.1).
2. **Districts are the community structure**, and a cross-district tie is a
   different kind of tie rather than a weaker one (2.1).
3. **Our weak ties are our worst carriers and they are the only bridges**, which
   compounds topic 9's finding and decides whether talk ever leaves the Hook
   (2.2).
4. **The authored cast should have no strangers in it; the crowd should be
   nothing but** (2.3).
5. **`Acquaintance.cs`'s header is stale about the thing it exists to explain**
   (3), and the 1944 of 1944 needs a fresh attribution.

## 5. What could not be established

1. **Every paper.** Same limit as topics 9 and 10. Science Advances, the arXiv
   preprints and ScienceDirect were not fetched, and Dunbar's numbers are
   themselves contested in a literature I have only in outline (the PMC paper's
   title, "Individual differences in energy allocation to personal
   relationships", suggests the variance around those numbers is the current
   subject, and I could not read it).
2. **Whether the 1944 of 1944 survives the familiarity fix** (section 3). This is
   the most important open question in the file and it needs a run.
3. **What `NpcWalker.cs:919`'s hardcoded 0.5 feeds.** Recorded, not traced.
4. **Any figure for how rumours actually cross community boundaries in a real
   small town.** The literature gives structure and mechanism; I found no
   measured transmission rate across a weak bridge, which is the number 2.2 would
   want.
5. **Historical British small-town network research.** Everything above is
   general network science. Whether a 1990 port town's structure differs from the
   general case, and in what way, is a sociology question I did not reach.
6. **Not covered:** how a network CHANGES over the span of a game, which is
   canon's "remediation is behavioral, rebuild relationships" clause and is the
   dynamic version of this whole topic.

## 6. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- ScienceDirect, "Calling Dunbar's numbers", https://www.sciencedirect.com/science/article/pii/S0378873316301095
- arXiv 1604.02400, "Calling Dunbar's Numbers", https://arxiv.org/pdf/1604.02400 (EGRESS BLOCKED)
- PMC, "Reflecting on Dunbar's numbers: Individual differences in energy allocation to personal relationships", https://pmc.ncbi.nlm.nih.gov/articles/PMC11896044/
- UpHabit, "Social Networks: The Dunbar 5-15-50-150", https://uphabit.com/2023/01/08/social-networks-the-dunbar-5-15-50-150/
- US Army, "Study suggests optimal social networks of no more than 150 people", https://www.army.mil/article/237792/study_suggests_optimal_social_networks_of_no_more_than_150_people
- Research Outreach, "Size matters: The link between social groups and human evolution", https://researchoutreach.org/articles/size-matters-social-groups-human-evolution/
- Science Advances, "Cumulative effects of triadic closure and homophily in social networks", https://www.science.org/doi/10.1126/sciadv.aax7310
- arXiv 2101.02510, "Disentangling homophily, community structure and triadic closure in networks", https://arxiv.org/pdf/2101.02510 (EGRESS BLOCKED)
- Nature Scientific Reports, "Network inequality through preferential attachment, triadic closure, and homophily", https://www.nature.com/articles/s41598-026-42911-3
- JASSS, "Homophily as a Process Generating Social Networks: Insights from Social Distance Attachment Model", https://www.jasss.org/23/2/6.html
- Cornell (Easley and Kleinberg), "Networks in Their Surrounding Contexts", https://www.cs.cornell.edu/home/kleinber/networks-book/networks-book-ch04.pdf

Repository sources, read this session at commit `074f85b`:
`ledger/Assets/Scripts/Core/Acquaintance.cs`, `Core/Perception.cs`,
`Core/Gossip.cs`, `Game/GameController.cs` (lines 60 to 95),
`Game/NpcWalker.cs:919`, `Game/SimDirector.cs:6522` and `:7196`,
`Game/Witnesses.cs:215`, `canon.md`, `production/systems-inventory.json`.
