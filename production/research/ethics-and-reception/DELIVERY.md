# Ethics and reception risks

Research topic 24. Delivered to the studio. Nothing here is an instruction, and
the one decision this topic exists to frame is deliberately not made here.

Topic 10 ended by handing this topic a concrete case rather than an abstract
worry, and said so: a mechanic that is "scientifically correct, thematically
apt, and capable of reading extremely badly in a review". Section 3 takes it
up. Sections 1 and 2 establish what this project already has and what the
measured reception landscape actually says, because the case cannot be argued
sensibly without both.

Labels follow `production/art/atlas-02/research/`: CITED, DERIVED, ASSUMED,
HOLE.

A correction owed first, from topic 22, made here rather than left standing:
that delivery said "how corrupt Meridian's police are is a real decision that
nobody has recorded". It IS recorded. D18 carries it, in canon: "Police are
corruptible as individuals, never as a thesis." I had not read the content rule
when I wrote that sentence.

---

## Part 1. What this project already has, which is more than most

### 1.1 The content rule is unusually specific

CITED, `canon.md`, the D18 section, approved 2026-09-10: eighteen clauses
governing "what may exist in this work at all, in image and in speech".
Alcohol and gambling out entirely (pubs may exist as places, and "what the pub
is for without drink is a design task, not a subtraction"); tobacco stays;
violence including blood and light gore stays, with no torture and no cruelty
as spectacle; killing "possible, rare, permanent, and the town remembers it
forever"; full period swearing allowed and NO SLURS OF ANY KIND; drugs only as
an off-screen economy, never a player verb; no prostitution or sexual content;
NO CHILDREN ANYWHERE, with the school standing closed; "Racism and sectarianism
may exist as FACTS ABOUT CHARACTERS, never voiced as slurs, never rewarded";
religion present, never mocked, never a mechanic; police corruptible as
individuals, never as a thesis.

### 1.2 The gate counts what it cannot enforce, which is the rarest thing here

CITED, run on 2026-09-14: `python3 tools/content-gate.py --enforceable` prints

    WHAT THIS GATE ENFORCES MECHANICALLY: 7 of 18 clauses. The rest are named
    below and are NOT claimed.
    ...
    enforceable: mechanical=7 notMechanical=11 total=18

The seven mechanical ones are alcohol, gambling, children, slurs, drug-use,
prostitution and sexual-content. The eleven it declines to claim include
cruelty-as-spectacle ("Framing and duration, not vocabulary"),
never-rewarded ("An outcome-table property"), police-never-a-thesis ("A thesis
is a reading of the whole work"), and racism-as-fact-never-voiced, annotated
"HALF ONLY. The slur list enforces `never voiced`. Nothing here can tell a card
that says a man is a bigot from a card that endorses him."

Three of the permitted clauses (tobacco, violence, swearing) are marked
`mechanical=false` with the note "PERMITTED by D18. The gate proves it permits
it: a tobacco line is an accepting fixture in the selftest." That is CLAUDE.md
rule 5b, a guard tested on the case it should PASS, applied to a content rule.

And the last row is the one I would keep: `what-a-picture-actually-shows`,
marked "NOT MECHANICAL, AND MEASURED", recording that a sheet drawn from a
prompt asking for "three nonidentifiable people" came back with two children in
school uniform at a school gate, and that "No word gate can see that. Somebody
opens the file."

DERIVED: a project that publishes the ratio of what its own rule enforces to
what it merely asserts is in a different class from one that says "we have a
content policy". This is worth stating before Part 2, because Part 2 is
uncomfortable and the honest response to it depends on this being true.

### 1.3 There are 197 known violations waiting

CITED, running the gate today: `hitsNew=0 hitsBaselined=197 staleBaseline=0
over stringsScanned=10058 filesOpened=33`, with the tool's own words: "Every
one of these breaks D18 and is waiting on a content pass. THIS LIST IS TO BE
EMPTIED, NEVER GROWN", stamped 2026-09-10.

DERIVED: zero new hits and a shrinking-by-policy baseline of 197 is a healthy
state four days after a rule landed that "voids decisions already taken". It is
recorded here because a reader of Part 2 should know the number exists and is
counted rather than discovering it later.

### 1.4 The corpora the gate reads are all files, and none of them is live

CITED: the gate's source table lists dialogue banks, barks, bark names, the
barks manifest, the tier-2 cards in two locations, image prompt specs, mesh
specs, concept sheet and pair specs, the brand bible, dialogue specs and art
delivery records. Every entry is a glob over files on disk.

DERIVED, and it is the same finding topic 20 reached from the voice side:
`tools/content-gate.py` is a build-time Python tool over authored content. The
live conversation path cannot pass through it, because the live path is C#
running on a player's machine and this is a tool that runs in CI. Canon says
D18 is "enforced at five sites", and one of those five is this gate "over
dialogue and spoken lines". For AUTHORED dialogue that is true. For the live
LLM, which is pillar 2, there is no runtime equivalent: `ResponseValidator` has
"two jobs only", length and the fourth wall, and never calls `ContentRule`.

---

## Part 2. The reception landscape, with a number

### 2.1 The penalty is measured, and it is large

CITED: an analysis of 508,192 English-language Steam reviews, with a
qualitative pass over 600 purposively sampled keyword-filtered reviews coded by
three raters at inter-rater reliability alpha = 0.920.
[arXiv, Player Perceptions of Generative AI in Games: A Steam Review Analysis](https://arxiv.org/abs/2608.11539) (EGRESS BLOCKED; figures below from search summaries)

CITED, the headline: "Disclosed generative AI use comes with a persistent
reception penalty: a 17.9 percentage point lower recommendation rate (86.3%
versus 68.4%) and more negative text sentiment", with negative comments
explicitly citing "AI", "soulless" or "lazy development".
[TechBuzz, AI in game development: why the 2026 backlash is real](https://www.techbuzz.ai/articles/ai-in-game-development-why-the-2026-backlash-is-real),
[a90skid, The AI stigma: why players are rejecting AI-made games](https://www.a90skid.com/the-ai-stigma-why-players-are-rejecting-ai-made-games/)

CITED, the industry's own view: in the 2026 State of the Game Industry survey,
52% of professionals said generative AI is having a negative impact on the
field, up from 30% a year earlier.
[TechBuzz, as above]

CITED, that the label itself is contested: developers complain "that the
disclosure label alone triggers negative reviews regardless of content
quality", and Valve narrowed the requirement in January 2026 to content that
ships with the game, exempting development tools.
[SoonLab, Can AI games survive on Steam](https://www.soonlab.ai/blog/steam-ai-games/),
[PC Gamer, Steam week in review: a touch of AI is all it takes to trigger backlash](https://www.pcgamer.com/gaming-industry/steam-week-in-review-a-touch-of-ai-is-all-it-takes-to-trigger-backlash-as-a-promising-new-indie-falls-afoul-of-slop-skeptics/)

### 2.2 And the distinction the same study draws, which matters enormously here

CITED, and this is the finding that changes the shape of the problem: "When AI
was the game's premise (such as LLM-driven dialogue or procedurally generated
narratives) players evaluated it on its interactive merits rather than as a
cost-cutting measure." The rejection attaches to AI "perceived as a cost-cutting
measure replacing authentic creative work", and "AI used in backend pipelines
largely [goes] unnoticed while AI in front-and-centre story sequences does
not".
[arXiv 2608.11539 via search summary, as above],
[TechBuzz, as above]

DERIVED, and LEDGER sits on both sides of that line at once:

- **The live conversation is AI-as-premise.** Nobody can hand-author
  memory-conditioned dialogue for thirty to fifty residents who remember what
  the player did last Tuesday. It is not a substitute for writing; it is a
  thing writing cannot do. On the study's own distinction this is the category
  players judge on its merits.
- **The art pipeline is asset substitution.** Generated props, generated
  textures, generated concept sheets and synthesised voices are, in the
  taxonomy above, exactly the "content that ships with the game" that carries
  the penalty. That they are generated because there is no art department is
  true and is not a distinction the study found players making.

I am not going to soften that. The dialogue is defensible on the published
evidence. The art is in the penalised bucket, and the honest version of the
defence is not "it is not AI", it is that the quality bar this project holds
itself to, `production/quality-ladder.md` and the D7 judges and the "no AI
slop" standard, is the thing that distinguishes it, and that is a claim
reviewers will test rather than accept.

### 2.3 What that means for the Meridian Test

Condition 1 is that a person who loves GTA or KCD2 plays thirty minutes and
does not bounce off the visuals. That is a visuals test.

DERIVED: the reception literature says there is a second bounce available, one
the Meridian Test does not currently measure, and it happens before the visuals
do. A player who learns the game is largely AI-built may not reach minute one.
The 17.9 point figure is about recommendation, not about installation, so it
does not directly price this, and no source found measures the pre-play effect.
HOLE, and a significant one.

---

## Part 3. The own-race bias case, laid out and not decided

### 3.1 The finding topic 10 handed over

CITED, from topic 10's delivery: "Eyewitnesses are less accurate when asked to
identify someone of a different race [...] Approximately 42% of wrongful
convictions based on misidentification involved cross-racial errors." Topic 10
recorded it as "real, large, well-replicated, and period-appropriate for a
British port town in 1990" and recommended nothing.

### 3.2 Where it would live, mechanically

`Core/Perception.cs` implements a five-rung identification ladder with distance
bounds (silhouette 35 m, mark 18 m, face 8 m, recognise 25 m), a light factor,
and `Observation.Misattribute` with p = 0.45 at rung 1 and 0.25 at rungs 2 and
3. Own-race bias, implemented faithfully, would be an additional multiplier on
misattribution keyed to whether observer and observed share a racial category.

DERIVED: that requires the game to hold a racial category per character as a
simulation variable, and to branch on it. It is not a flavour text change. The
data structure is the mechanic.

### 3.3 The arguments, both directions, stated as fairly as I can

FOR, and they are not weak:

- It is true, it is one of the most replicated findings in the eyewitness
  literature, and it has sent real people to prison. A game whose entire moat
  is that memory is fallible and confident memory is worse (`Observation.Retell`:
  "MEMORY HARDENS AS IT DECAYS: accuracy falls, confidence rises") is already
  making exactly this argument about human testimony.
- It is a mechanic that indicts the SYSTEM, not the people. The finding is
  about perception, not about character, and the wrongful-conviction statistic
  is the point of it.
- D18 does not forbid it. A cross-race identification penalty is not a slur and
  is not a reward.

AGAINST:

- A player who notices it does not read a research finding. They read a game
  rule that says people of one race cannot tell people of another apart. The
  mechanism is invisible; the output is a sentence somebody will write in a
  review.
- It cannot be contextualised in play. The literature's framing, that this is a
  well-documented failure of cross-race face processing with serious
  consequences for justice, requires prose the game has no place to put.
- It requires racial categories as live simulation data, which is a thing the
  project does not currently have and would have to build deliberately.
- D18's own instinct runs the other way. Its racism clause permits a FACT ABOUT
  A CHARACTER and forbids the depiction and the reward. Own-race bias is not a
  fact about a character; it is a rule about a population.
- HOLE: I searched for any game that has implemented a race-linked perception
  mechanic, in any framing, and found none. There is no precedent in either
  direction, so there is no evidence about how it lands.

One further caution, found in the literature and worth carrying regardless of
the decision: the "historical accuracy" argument has an asymmetric track record
in games criticism. One source notes that "white heroes in games can be
anything without scrutiny, [while] non-white heroes must pass the test of
'historical accuracy'".
[Historians.org, Racing games: choice and history in video games](https://www.historians.org/research-and-publications/perspectives-on-history/december-2022/racing-games-choice-and-history-in-video-games)
That does not make accuracy a bad argument. It means it is an argument that has
been used selectively, and a defence resting on it alone will be read in that
light.

### 3.4 What I am doing with it

Recording it, arguing both sides, and stopping. The brief for this lane says my
work ends at a recommendation and a decision Jafar makes, and this is the one
item in twenty-four topics where I do not think a recommendation from me is
worth more than the arguments themselves.

The narrower question that a decision could be made on, if a whole answer is
too big: does LEDGER hold a racial category per character as simulation data at
all? Everything above follows from that, and it is a smaller question with a
clearer answer.

---

## Part 4. The risk that is nobody's judgement call

Separated deliberately from Part 3, because Part 3 is a values question and
this is not.

The live conversation path has no content screen. `ResponseValidator` checks
length and the fourth wall. `ContentRule` has three call sites, all crowd and
body generation. `tools/content-gate.py` is a build-time tool over files.

Valve's January 2026 clarification creates a live-generated tier and, because
that content is unpredictable, "requires developers to build safety guardrails
preventing illegal or offensive material from appearing".
[StraySpark, Steam's 2026 AI disclosure rules](https://www.strayspark.studio/blog/steam-ai-disclosure-rules-2026-indie-developer-guide)

DERIVED: D18's most absolute clauses are the ones a language model is most
likely to breach unprompted. NO SLURS OF ANY KIND and NO CHILDREN ANYWHERE are
both clauses a model writing 1990 British dialogue could violate in a single
line, and the slur list that enforces the first exists as
`content/rules/slurs-v1.json` and is read by a Python tool that the running
game never calls.

This is not an ethics dilemma. It is a gap between a rule the project takes
seriously and the one surface where nothing checks it, and it is the same gap
whichever way Part 3 is decided.

---

## Part 5. What could not be established

1. **The Steam review paper itself.** arXiv is egress-blocked, for the third
   topic in this queue. All figures in 2.1 and 2.2 are search summaries.
2. **Whether the reception penalty applies before purchase.** The 17.9 point
   figure is a recommendation rate among people who played.
3. **Any precedent for a race-linked perception mechanic.** Four searches, no
   case in either direction.
4. **How the penalty splits between AI art, AI voice and AI dialogue.** The
   study's distinction is premise-versus-substitute, not medium.
5. **Anything about voice actors' organised position** on synthesised voices in
   games, which is adjacent to topic 20 and was not researched here.

---

## Part 6. Findings and interpretation

### Findings

F1. D18 has eighteen clauses. `tools/content-gate.py --enforceable` reports
seven enforced mechanically and eleven named and explicitly not claimed.

F2. Three permitted clauses are proven permitted by accepting fixtures in the
gate's own selftest.

F3. The gate reports 197 baselined D18 violations over 121 distinct texts,
stamped 2026-09-10, zero new, with the instruction that the list is to be
emptied and never grown.

F4. Every corpus the gate reads is a file glob. The live conversation path
passes through none of them, and `ResponseValidator` never calls `ContentRule`.

F5. Disclosed generative AI carries a measured 17.9 percentage point lower
recommendation rate on Steam (86.3% against 68.4%), over 508,192 reviews.

F6. The same study finds that when AI is the game's PREMISE, including
LLM-driven dialogue, players judge it on interactive merits rather than as
cost-cutting.

F7. 52% of game industry professionals in the 2026 State of the Game Industry
survey said generative AI is having a negative impact, up from 30%.

F8. No game was found that implements a race-linked perception mechanic, in
any framing.

F9. Topic 22's claim that Meridian's police corruption is an unrecorded
decision was wrong. D18 records it.

### Interpretation

I1. LEDGER sits on both sides of the reception line the evidence draws. The
live dialogue is the defensible category by the study's own distinction; the
generated art and voices are the penalised one. Any public framing of this
project should probably lead with the first and be straightforward about the
second, because the study says players punish the perception of substitution
and not the technology.

I2. The strongest asset this project has against the reception risk is the one
in Part 1: a content rule that counts what it cannot enforce, and a throughput
ledger that records finished-looking work as zero. Those are legible to a
sceptical reader in a way that a quality claim is not.

I3. Part 4 is the item that should not wait on Part 3. A runtime screen on the
live path is required by a storefront, is implied by a rule canon calls
permanent, and is orthogonal to every values question in this delivery.

I4. On the own-race bias: the narrow question, whether the game holds racial
categories as simulation data, is the one worth putting to Jafar. It is
answerable, everything else follows from it, and it does not require him to
adjudicate a research finding to decide it.
