# Topic 3: Hitman, and how density is reached in a small footprint

STATUS: SPEC (research delivery). Branch `research/hitman-density`, from commit
`074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written. It ends at findings and a recommendation.

## 0. How to read this file, and how it differs from game 2 of the audit

`production/research/coverage-audit-hitman/` mapped what Hitman CONTAINS against
our inventory. This file asks a different question, the brief's: how does it
reach density in a small footprint, and how does a level stay legible while full
of people. It is about SPACE, not systems, and it does not repeat the audit's
recommendations.

Claim labels are CITED, DERIVED, ASSUMED and HOLE.

SOURCING LIMIT, and it is worse here than on any previous topic. The two
authoritative sources are IO Interactive's own GDC talks, and I could not read
either. Measured this session: `media.gdcvault.com` answered `EGRESS_BLOCKED`,
`haywiremag.com` answered `EGRESS_BLOCKED`, `80.lv` answered `EGRESS_BLOCKED`,
and the GDC Europe 2016 slide PDF on
`ubm-twvideo01.s3.amazonaws.com` answered HTTP 403. `gamedeveloper.com` was
already known blocked from the audit. So **every claim about IO's own design
vocabulary below is the search channel's summary of a page describing a talk,
two removes from the talk itself.** Where a specific phrase is quoted it is
quoted from that summary and labelled as such. This is the topic in my queue
most damaged by the egress policy and I would re-run it through CI if the
project wants it firmed up.

## 1. The findings, in order of usefulness to us

### 1.1 Density comes from connections, not from square metres

CITED (search summaries of 80.lv, "The Making of Hitman's Best Level" and "The
Snail Structure of Hitman's Levels", Game Developer, "Hitman dev says the secret
to expansive level design is spirals", and Kotaku's write-up): lead level
designer Torbjorn Christensen describes designing levels as a big spiral, a
"snail house" a player can walk through without hitting a wall; lead game
designer Jesper Hylling is quoted as "There are no dead ends and you never need
to backtrack, although you can"; and the levels are described as "Swiss cheese
design", which "utilises the impression of a volume of content that is
constructed meticulously and filled with connections". The stated effect: "The
levels feel larger than they maybe are in terms of square meters because players
can keep moving ahead all the time."

**This is the single most transferable thing in the topic, and it is a rule we
can hold a street to.** Sapienza is a whole coastal town with a mansion, a town
square and a church, and its designers explain its felt size as a property of
its CONNECTEDNESS rather than its area.

For scale, measured from this repository: `production/specs/vignette-scene.json`
puts Quay Street at **42.0 metres long**, with a 6.0 m carriageway, two 2.0 m
footways, and terrace blocks occupying x = 3.0 to 39.0. That is the whole built
footprint today. It has one yard entrance, at x = 22.5, where the dropped kerb
and the gap in the terrace are deliberately the same event.

DERIVED: a 42-metre street with one gap is a corridor, not a snail house. That
is entirely appropriate for a vignette whose stated scope is "The D1b street
vignette and nothing else", and it becomes the wrong shape the moment the street
has to carry play. The Hitman rule, applied to us, is a question with a testable
answer: **can a player leave Quay Street by more than one route, and can they
come back by a different one?** Today, no.

### 1.2 The social space taxonomy, which is the vocabulary our design is missing

CITED (search summary of the GDC 2019 talk listing and PC Gamer's "How the
creators of Hitman use social science to design perfect murder playgrounds"):
IO's level-design terminology classifies six kinds of social space, graded by
how strong the rules are and whether anybody enforces them:

| Space | Rules | Enforcement |
|---|---|---|
| public | few | none |
| public purpose | few | yes |
| public rule | strong | yes |
| private | vague | (unstated in the summary) |
| private professional | strong | yes |
| private personal | strong | and "rewarding for players" |

CITED (same sources): the framework draws on Pierre Bourdieu's theory of social
spaces, "and a social marketplace where different behaviours serve as capital
being exchanged", and on Erving Goffman's "front stage versus back stage", "the
idea that humans have a forward-facing personality in public, and a backstage
personality in more private circumstances". The talk is by Mette Podenphant
Andersen and covers how level design changed between Hitman 2016 and Hitman 2.

**WHY THIS MATTERS TO US MORE THAN IT MATTERS TO HITMAN.** The coverage audit
recommended blend-in, behaviour that fits what you appear to be, as one of the
five things to take from Hitman (audit A8). That recommendation had a hole in it
which I could not fill at the time: it said what the system does and not what it
reads. This taxonomy is the missing half. What makes an act need explaining is
not the act, it is the KIND OF SPACE it happens in and whether anybody in that
space is charged with caring.

Our tile "doors and who gets in" (exists) already implements the hardest case,
the threshold: "A door asks for an introduction, standing, a payment or the
right clothes". What the six categories add is that the interesting spaces are
not the ones with doors. A public street with no enforcement and a public street
with a beat constable on it are different spaces that look identical, and
Meridian has both.

DERIVED, and offered as an illustration rather than a proposal, because a
taxonomy for Meridian is a design job and not research: Mickey's bar is public
purpose (few rules, and Tom enforces them); its cellar and yard are private
personal; the Exchange's offices are private professional; Quay Street at noon
is public and at three in the morning is a different space with the same
geometry. Goffman's front stage and back stage is the pub in one sentence, and a
crime sim lives on the seam between them.

### 1.3 Legibility was a crisis, and the fix was not to shrink anything

CITED (search summaries of the GDC Europe 2016 talk listing and Game Developer's
video write-up): "During the final development stages of HITMAN, user research
showed that players had fun, but that the learning curve was way too steep and
the scale of the first level (Paris) was incomprehensible." The response was to
"improve the player guidance and teach players how to think and act like 47
without changing the sandbox core of the game."

Three things follow, and the third is the one for us.

1. **A dense space is not automatically legible**, and the studio that is best in
   the world at this shipped a level their own testing called incomprehensible.
2. **Their fix was guidance, not simplification.** The sandbox stayed.
3. **Their guidance was Mission Stories, which the coverage audit recommended
   OUT.** That is not a contradiction and it is worth being explicit about,
   because it is the tension at the centre of this topic: we refused their
   answer, so we inherit their problem. The audit already flagged this and
   pointed at queue topic 7 (how emergent-story games make stories legible). This
   topic is the second half of the same finding, and together they are the
   strongest argument in my queue for moving topic 7 up.

HOLE, and it is the one I most want closed: the specific guidance techniques.
The 2016 talk is where they are, and neither the slides nor a full write-up was
reachable. I know the problem they solved and the shape of their answer. I do
not know their techniques, and this file should not pretend otherwise.

### 1.4 What the crowd costs, and it is not what I expected

CITED (from the coverage audit's sourcing, search summary of PlayStationTrophies'
coverage of IO's GDC 2012 crowds talk): Hitman Absolution achieved "1200
character crowds while running at 30fps on current-gen consoles", with over 1000
crowd NPCs "active in a given level" and still reactive to the player.

DERIVED, and it reframes our density anxiety: 1200 reactive crowd characters at
30fps was achievable on 2012 console hardware. Our tile "the crowd you see"
(partial) reads 65 walkers in the headless sim and records that no committed
frame shows anybody walking the Unreal street. The gap between 65 and 1200 is
not a hardware gap, it is a not-built-yet gap.

I am deliberately NOT turning that into a target. Absolution's crowd is a crowd:
characters with a behaviour, not people with a schedule and a memory, and the
whole point of LEDGER is that its people are the latter. A thousand of ours
would cost incomparably more, and topic 17 is where that gets measured. **What
the number is good for is killing the assumption that a dense street is
expensive because it is dense.** The density is cheap. The memory is the cost.

### 1.5 Verticality, and the one place it is free for us

CITED (search summaries of 80.lv and PC Gamer on Sapienza): the designers "especially
wanted to explore the verticality in coastal towns, and how streets and
corridors connect everything", building layers "interconnected with slopes and
stairways", based on the Amalfi coast's topography.

DERIVED, for Meridian: canon gives us "Fairview (residential hills)" and a port,
which is the same topography for the same reason. And
`production/art/atlas-02/research/hillside-housing-dated-series.md` exists in
this repository already, which means the research for the one district where
Hitman's verticality transfers directly has been done.

The flat half is also useful. Quay Street's spec has a first floor at 3.4 m and
eaves at 6.30 m. DERIVED: two storeys over a 6.0 m carriageway is a street whose
upper windows look into each other across it, which is exactly the geometry the
coverage audit's lit-window finding needs (game 5, A6). Verticality in a British
terrace is not a hillside, it is a first-floor window, and we have one.

## 2. What this says about our shape

The brief's framing is right and I want to sharpen it rather than agree with it.

**Hitman is our shape in geometry and not in structure.** Its levels are small,
dense, layered, re-walked, and full of people whose attention is the mechanic.
So is Meridian. But a Hitman level is a closed box that resets, and its
legibility solutions are allowed to be extra-diegetic (a white dot, a mission
story, an instinct mode) because the box does not have to hold together as a
place people live in. The audit ruled all three of those OUT.

DERIVED, and it is the honest summary of this topic: **we can take Hitman's
spatial rules wholesale and can take almost none of its legibility rules.** The
spatial rules are about how a space is built, and they are free. The legibility
rules are about what the game tells you, and ours has to come from the
simulation.

Which puts the load on the one thing this topic can hand over: the social space
taxonomy is BOTH. It is a way of building a space and a way of making it
readable, and it is readable diegetically, because a player learns what kind of
space they are in by looking at it and at who is in it. That is why it is the
recommendation.

## 3. Recommendation

**One thing to take, one rule to hold the street to, one topic to move up.**

**TAKE: the social space taxonomy, as design vocabulary rather than as code.**
Six grades of rule-and-enforcement, applied to every space in Meridian as it is
authored. It costs a column in a spec. What it buys is that the blend-in
recommendation from the coverage audit becomes buildable, because the question
"does this behaviour need explaining" has a table to read. And it buys D14's
authored interiors a shared vocabulary for what an interior is FOR, socially,
which is a thing every interior spec will otherwise invent separately.

**HOLD THE STREET TO: no dead ends, and more than one way out.** Quay Street at
42 metres with one yard entrance is a corridor. That is correct for a vignette
and wrong for play, and the moment the street has to carry a chase, a tail or an
escape, the snail-house rule is the difference between a place and a set. This
is a constraint on the NEXT street rather than a criticism of this one.

**MOVE UP: queue topic 7.** Twice now, from two directions, the audit and this
topic have landed on the same thing: we refused Hitman's legibility answer and
have not got one of our own. IO's own user research found their densest level
incomprehensible to players who were enjoying it. We are building something
denser in information and thinner in guidance.

**DO NOT TAKE: a crowd target.** 1200 at 30fps is a real number about a
different kind of crowd and would be a bad thing to aim at. Topic 17 sets ours,
against people with schedules and memories rather than characters with
behaviours.

## 4. What could not be established

1. **Both GDC talks, in full.** The 2016 guidance talk and the 2019 social
   spaces talk are the two primary sources for this entire topic, and four hosts
   carrying them or their write-ups are blocked or forbidden from here
   (`media.gdcvault.com`, `haywiremag.com`, `80.lv`,
   `ubm-twvideo01.s3.amazonaws.com` with a 403, plus `gamedeveloper.com` from
   earlier). Everything above is two removes from the source.
2. **The definition of the "private" category**, which the summary gives as
   "vague rules" with no enforcement value. Five of the six are clear and one is
   not.
3. **The guidance techniques from the 2016 talk.** I have the problem and the
   philosophy and not the methods, which is the most useful part.
4. **Any square-metre figure for a Hitman level.** "Feels larger than they maybe
   are in terms of square meters" is the closest any source comes, and no source
   gives the actual number, so the comparison with our 42 metres is a comparison
   of shapes and not of sizes.
5. **Whether Sapienza's crowd is anywhere near Absolution's 1200.** The 1200 is
   an Absolution figure from 2012 and Sapienza is a different engine and a
   different game; sources describe Sapienza's population only as "dense".
6. **How many simultaneous NPCs the current Unreal probe can carry.** Not
   measured here, and it is topic 17's.
7. **Not covered here, deliberately**: everything the coverage audit already
   covered about Hitman's systems. This file is about space.

## 5. Sources

Search channel summaries, retrieved 2026-09-14; none read in full, and see the
sourcing limit in section 0.

- GDC Vault listing, "Level Design in 'HITMAN': Guiding Players in a Non-Linear Sandbox", https://www.gdcvault.com/play/1023872/Level-Design-in-HITMAN-Guiding
- GDC Vault listing, "Level Design Workshop: 'Hitman' Levels as Social Spaces: The Social Anthropology of Level Design", https://gdcvault.com/play/1026531/Level-Design-Workshop-Hitman-Levels
- GDC 2019 schedule entry for the same talk, https://schedule2019.gdconf.com/session/level-design-workshop-hitman-levels-as-social-spaces-the-social-anthropology-of-level-design/865179
- GDC slide PDF, "HITMAN levels as Social Spaces" (Mette Podenphant Andersen), https://media.gdcvault.com/gdc2019/presentations/MettePodenphantAndersen_HitmanSocial.pdf (EGRESS BLOCKED)
- GDC Europe 2016 slide PDF, "Level Design in HITMAN: Guiding players in a non-linear sandbox", https://ubm-twvideo01.s3.amazonaws.com/o1/vault/gdceurope2016/presentations/Mette_Poedenphant_GuidingThePlayer.pdf (HTTP 403)
- Class Central listing of the 2016 talk, https://www.classcentral.com/course/youtube-level-design-in-hitman-guiding-players-in-a-non-linear-sandbox-158086
- Class Central listing of the 2019 talk, https://www.classcentral.com/course/youtube-hitman-levels-as-social-spaces-the-social-anthropology-of-level-design-165739
- PC Gamer, "How the creators of Hitman use social science to design perfect murder playgrounds", https://www.pcgamer.com/how-the-creators-of-hitman-use-social-science-to-design-perfect-murder-playgrounds/
- PC Gamer, "The making of Sapienza, Hitman's best level", https://www.pcgamer.com/the-making-of-sapienza-hitmans-best-level/
- Game Developer, "Hitman dev says the secret to expansive level design is spirals", https://www.gamedeveloper.com/design/-i-hitman-i-dev-says-the-secret-to-expansive-level-design-is-spirals (EGRESS BLOCKED)
- Game Developer, "From 'Coastal Town' to Sapienza: Designing a Hitman level", https://www.gamedeveloper.com/design/from-coastal-town-to-sapienza-designing-a-i-hitman-i-level (EGRESS BLOCKED)
- Game Developer, "Mapping out the subtle social cues throughout Hitman's level design", https://www.gamedeveloper.com/design/mapping-out-the-subtle-social-cues-throughout-i-hitman-i-s-level-design (EGRESS BLOCKED)
- 80.lv, "The Making of Hitman's Best Level", https://80.lv/articles/hitman-sapienza-level-analysis (EGRESS BLOCKED)
- 80.lv, "The Snail Structure of Hitman's Levels", https://80.lv/articles/the-snail-structure-of-hitmans-levels (EGRESS BLOCKED)
- Kotaku, "IKEA Stores And Hitman Levels Are Both Snail Houses With Swiss Cheese", https://kotaku.com/ikea-stores-and-hitman-levels-are-both-snail-houses-wit-1832842270
- Haywire Magazine, "The Language of Level Design in Hitman", https://haywiremag.com/features/the-language-of-level-design-in-hitman/ (EGRESS BLOCKED)
- Unsupervised Nerds, "Level Design in Hitman", https://www.unsupervisednerds.com/reads-full/2020/8/19/level-design-in-hitman
- Adam Ludwiczak, "Hitman: Level Design", https://www.adamludwiczak.com/portfolio/hitman-level-design
- PlayStationTrophies, "GDC 2012: IO Interactive Focusing on Quality Rather Than Quantity When it Comes to Crowds", https://www.playstationtrophies.org/news/news-6081-gdc-2012-io-interactive-focusing-on-quality-rather-than-quantity-when-it-comes-to-crowds-in-hitman-absolution.html
- The Level Design Book, "Verticality", https://book.leveldesignbook.com/process/layout/flow/verticality

Repository sources, read this session at commit `074f85b`:
`production/specs/vignette-scene.json`, `production/systems-inventory.json`,
`canon.md`, `ledger-v2/respec/vision-pillars-v2.md`,
`production/research/coverage-audit-hitman/DELIVERY.md` (this lane's own,
on its branch), `production/art/atlas-02/research/` (file listing).
