# What a crime scene actually yields in Britain in 1990

Research topic 29. Delivered to the studio. Nothing here is an instruction.

**Standing egress note.** One route out of this container reads a page in full:
`curl` reaches package registries and `raw.githubusercontent.com`. `github.com`
and `api.github.com` return 403; arxiv, Wikipedia, journals, news and vendor
documentation return 000. Source repositories and licence files are readable
primary sources; research literature is not. Everything cited below is a search
engine's summary and is labelled so.

The brief asked for a short period-specific list as the research behind what a
player leaves behind. The list is short, and the reason it is short turns out to
be the finding.

Labels: CITED, DERIVED, ASSUMED, HOLE.

---

## Part 1. The dates that bound the period

### 1.1 DNA exists, and is four years old

CITED: DNA typing debuted in a criminal investigation in October 1986 in the
Enderby case, where it first proved a prime suspect innocent. The first
conviction followed: Colin Pitchfork was arrested on 19 September 1987 and
sentenced at Leicester Crown Court on 23 January 1988. By 1987 DNA results had
been admitted in evidence in UK and US criminal courts, and by 1988 British
institutions and courts accepted DNA evidence "without much question".
[YourGenome, The dawn of DNA profiling](https://www.yourgenome.org/theme/the-dawn-of-dna-profiling-the-eureka-moment-that-revolutionised-crime-solving/),
[SimplyForensic, Colin Pitchfork: first DNA murder conviction](https://simplyforensic.com/colin-pitchfork-case-the-debut-of-dna-fingerprinting/),
[ScienceDirect, DNA fingerprinting on trial: the dramatic early history](https://www.sciencedirect.com/science/article/abs/pii/S0160932705000773)

DERIVED: Meridian's window opens in 1988, the year of the first conviction's
sentencing. DNA is not science fiction here and it is not routine. It is NEWS.

### 1.2 And there is nothing to search it against

CITED: the National DNA Database of England and Wales was established on
**10 April 1995**.
[Wikipedia, United Kingdom National DNA Database](https://en.wikipedia.org/wiki/United_Kingdom_National_DNA_Database),
[YourGenome, What is the UK National DNA Database](https://www.yourgenome.org/facts/what-is-the-uk-national-dna-database/)

CITED: the UK's national automated fingerprint system, NAFIS, was established in
**1999**.
[Wikipedia, National Automated Fingerprint Identification System](https://en.wikipedia.org/wiki/National_Automated_Fingerprint_Identification_System),
[Oxford Reference, NAFIS](https://www.oxfordreference.com/display/10.1093/oi/authority.20110803100223917)

DERIVED, and it is the finding of this topic: **in 1990 there is no national
database of either kind.** The DNA database arrives three years after Meridian's
window closes and the automated fingerprint system seven years after.

A sample from a scene can therefore be COMPARED to a person you have already
got. It cannot be SEARCHED to produce a person you have not. There are no cold
hits in 1990.

Fingerprints are the partial exception and the exception is local: a mark can be
compared against a force's own manual collection, so it identifies somebody who
already has form with that force and nobody else.

### 1.3 What the technique physically needed

CITED: RFLP analysis, the method of the period, "required a relatively large
amount of non-degraded DNA, about 100 nanograms", practically "a biological
sample about the size of a quarter", "roughly the size of a small bloodstain,
quantities rarely available from trace evidence, weapons, or touch surfaces".
"Any degradation of the DNA from heat, moisture, or time destroyed the large
fragments the method depended on." The original method "took several days to
process". PCR-based STR analysis, which needs about one hundred times less DNA
and works on degraded samples, replaced it in the late 1990s.
[EBSCO, Restriction fragment length polymorphism (RFLP)](https://www.ebsco.com/research-starters/science/restriction-fragment-length-polymorphism-rflp),
[National Institute of Justice, DNA evidence: basics of analyzing](https://nij.ojp.gov/topics/articles/dna-evidence-basics-analyzing),
[NCBI, DNA Typing: Technical Considerations](https://www.ncbi.nlm.nih.gov/books/NBK234539/)

DERIVED, and it is period AND place specific in a way this project should
enjoy: **moisture destroys it.** `canon.md` sets the visual target as
"photoreal, wet, overcast, grimy Britain" and says "weather and grime are the
strategy". The weather that defines Meridian's look is the weather that ruins
the only new forensic technique in it. A bloodstain left in the open on a wet
night in a port town is not a DNA sample by the time anyone lifts it.

### 1.4 The SOCO of 1990 is one person doing two jobs

CITED: a scenes of crime officer "identif[ies] and collect[s] forensic,
photographic and fingerprint evidence from crime scenes", recovering "footwear
marks, fingerprints and DNA (blood, cellular, body fluids)" and traces such as
"blood, hairs, fibres, paint, glass". And the period detail: **in 1990 the role
combined crime scene examiner and fingerprint expert functions; they have since
been divided into two separate roles.**
[Wikipedia, Scenes of crime officer](https://en.wikipedia.org/wiki/Scenes_of_crime_officer),
[TargetJobs, Scene of crime officer job description](https://targetjobs.co.uk/careers-advice/job-descriptions/scene-crime-officer-job-description),
[College of Policing, Forensics](https://www.college.police.uk/app/investigation/forensics)

DERIVED: in Meridian, the person who lifts the mark is the person who compares
it. That is one named character rather than a pipeline, which is a gift for a
game with ten named cast members and a detective already in canon.

---

## Part 2. The list, as short as it actually is

What a scene of crime officer in a British town could collect in 1990, and what
each was worth.

| yield | status in 1990 | what it can do | what it cannot |
|---|---|---|---|
| **Fingerprints** | mature, and the SOCO's own job | confirm a named suspect; identify somebody with local form | find a stranger |
| **Footwear marks** | routine | link scenes to each other; match a seized shoe | name anybody |
| **Blood, grouping** | mature, cheap, fast | exclude most of the population, include a large minority | identify |
| **Blood, DNA (RFLP)** | four years old, admissible, slow | confirm a suspect you have, if the sample is big and dry and fresh | search, or work from a trace |
| **Hairs and fibres** | routine, comparative | link a person or a place to a scene, once you have the person or the place | originate a lead |
| **Glass and paint** | routine, comparative | same | same |
| **Tool marks** | routine, comparative | match a seized tool | name a hand |
| **Photography** | routine, and the SOCO's | record what was there | interpret it |

DERIVED, reading down the third and fourth columns: **every single technique
available in 1990 is comparative.** Each one answers "is this the same as that",
and not one of them answers "who". The only thing on the list that can produce
a name unprompted is a fingerprint belonging to somebody the local force has
already printed.

That is the period fact a crime game has to build on, and it is not a
limitation to be worked around. It is a design given.

---

## Part 3. What this means for LEDGER, which is already built for it

### 3.1 The game models no forensics at all

CITED, checked 2026-09-14: a grep of `ledger/Assets/Scripts/` for `fingerprint`,
`forensic`, `dna`, `soco`, `scene of crime` and `swab` returns six hits and all
six are substring false friends (`ChildName` and `HeadName` contain the letters
d-n-a). **There is no forensic model in this project.**

### 3.2 What it models instead is exactly right for 1990

CITED, `Core/Traces.cs`:

- `class Stain` with a strength, `Age(s, minutes)` drying it toward
  `StainFloor = 0.45`, `Wash` requiring `WashMinutes = 25` with water and
  privacy, `CountsAsMark(s) => s.Strength > 0.3`, and
  `Noticeable(s, metres, lightLevel)`.
- `SocialCost(s, familiarity)`: what a stain costs you with a person, scaled by
  how well they know you.
- `Item` with `Origin` in {Bought, Stolen, Taken, Inherited, Ordinary}, a
  `History` list that is never cleared, `DisposalWitnessed`, and
  `UsedInAKilling => History.Any(h => h.StartsWith("killed:"))`.

DERIVED: this is a SOCIAL trace model. A stain in LEDGER is noticed by a PERSON,
at a distance, in a light level, and it costs you STANDING. It is never swabbed.
An item carries a history that follows it rather than a chemistry that betrays
it.

That is the correct model for 1990, arrived at by design rather than by
research, and this delivery's main practical value is to say so before somebody
builds a lab.

### 3.3 The alignment, stated plainly

Part 2 concludes that in 1990 forensics can only confirm a suspect somebody
already has. Something else has to produce the suspect.

In Meridian that something is the moat: perception, memory, gossip and
informing. `Core/Informing.cs` states its own version of the same truth, that
"truth is not an input. A true accusation nobody will corroborate is ignored. A
false one three people will swear to lands."

**The period and the design agree.** A game set in 1990 in which people are the
only route from a crime to a name is not a game making a concession to its era.
It is a game whose era happens to enforce its premise.

That is worth writing down because the temptation, when forensics does get
built, will be to make it satisfying, and satisfying forensics is
twenty-first-century forensics. A lab that names a stranger from a smear on a
door handle would quietly destroy the reason the moat exists.

### 3.4 What a 1990-accurate forensic layer would actually be

DERIVED from Part 2, offered as the shape rather than as a proposal:

- It produces **comparisons**, never names.
- It **confirms or refuses** a person the player or the law already suspects.
- It takes **days**, not minutes, for anything involving DNA.
- It is **destroyed by weather**, which this game has in abundance and already
  simulates: `Traces.Age` already dries a stain toward a floor over time, and
  wet weather is already a system.
- It is administered by **one person who is also the fingerprint expert**.
- Its most useful output against an unknown offender is a **local fingerprint
  hit**, which is to say: it works on people who already have form, which is to
  say, on people the town already knows something about.

That last line is the one worth keeping. Even the forensics of 1990 route back
through what is already known about somebody.

---

## Part 4. What could not be established

1. **Any primary source.** Every citation is a search summary; the journals and
   the College of Policing pages are unreachable.
2. **What a provincial force could actually access in 1990**, as against what
   existed. Whether a town like Meridian sends to a regional forensic science
   laboratory, how long the queue is, and what it costs are exactly the details
   a game would want and none were found.
3. **Blood grouping's discriminating power in practice.** Named in Part 2 as
   "exclude most, include a large minority" on general knowledge of ABO and
   secretor status; no source found gives period figures.
4. **Whether footwear mark collections were systematised** in the UK by 1990.
5. **PACE's rules on taking samples from a suspect**, which is the legal half of
   this and belongs with the earlier British-policing topic rather than here.

---

## Part 5. Findings and interpretation

### Findings

F1. DNA profiling debuted in a criminal investigation in October 1986 and
produced its first conviction with Pitchfork's sentencing on 23 January 1988.
Courts accepted it by 1988.

F2. The UK National DNA Database was established 10 April 1995, three years
after Meridian's window closes.

F3. The UK national automated fingerprint system was established in 1999, seven
years after it closes.

F4. RFLP required about 100 nanograms of non-degraded DNA, practically a stain
the size of a coin, was destroyed by heat, moisture or time, and took several
days.

F5. In 1990 the scenes of crime officer role combined crime scene examiner and
fingerprint expert; the two were separated later.

F6. Every forensic technique available in 1990 is comparative. None produces a
name from nothing except a fingerprint matching a local collection.

F7. LEDGER models no forensics at all: six grep hits, all substring false
friends.

F8. `Core/Traces.cs` models traces socially instead: a stain that dries to a
floor of 0.45, washes in 25 minutes with water and privacy, counts as a mark
above 0.3, is `Noticeable` at a distance in a light level, and carries a
`SocialCost` scaled by familiarity; and an item with an `Origin` and a `History`
that is never cleared.

### Interpretation

I1. The period does not constrain this game's premise, it enforces it. In 1990
nothing except people can turn a crime into a name, which is the sentence the
moat already implements.

I2. The main risk this research guards against is a future forensic layer built
at modern capability because modern capability is more satisfying. A lab that
identifies a stranger from a trace would remove the reason witnesses matter.

I3. The wet, overcast weather that is canon's stated visual strategy is also, on
the evidence in 1.3, a forensic eraser. A game that already simulates rain and
already ages stains has the mechanism for that in place without adding anything.

I4. The one detail I would give a designer from this whole topic is that the
SOCO and the fingerprint expert were the same person in 1990. It turns a
faceless process into somebody with a name who can be known, avoided, bribed or
lied to, which is the only form in which forensics could ever join this game's
moat rather than compete with it.
