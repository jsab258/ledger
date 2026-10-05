# Expressing group standing without storing a score

Research topic 30, the last in this batch. Delivered to the studio. Nothing here
is an instruction.

**Standing egress note.** One route out of this container reads a page in full:
`curl` reaches package registries and `raw.githubusercontent.com`. `github.com`
and `api.github.com` return 403; arxiv, Wikipedia, journals, news and vendor
documentation return 000. Source repositories and licence files are readable
primary sources; research literature is not.

A note on this topic's framing before anything else, because it is the same
situation as two earlier topics.

**D34 does not exist in this checkout.** The decision register is
`ledger-v2/respec/decision-register/` and it holds D1 to D18 and nothing else. A
grep of every `.md` in the repository outside my own research lane for any token
`D20` to `D39` returns zero hits. This is the third time in thirty topics (D24
and D28 were the others), and as before I have taken the brief's own formulation
as the governing statement and worked against that rather than inventing a
record:

> a district's feeling is what its residents individually remember, never a
> number.

Labels: CITED, DERIVED, ASSUMED, HOLE.

---

## Part 1. The mechanism exists, and it is better than what I would have proposed

I went into this expecting to design an aggregation. It is built.

### 1.1 The pipeline, read out of the code

CITED, `Core/Gossip.cs:525`, `DayCircleHeat()`, in full behaviour:

    public double DayCircleHeat()
    {
        double max = 0;
        foreach (var a in _agents.Values)
        {
            if (a.Circle != "day") continue;
            var bestPerTopic = new Dictionary<string, double>();
            foreach (var r in a.Rumors)
                if (r.Sensitive && (!a.Leashed || r.Indelible)
                    && (!bestPerTopic.TryGetValue(r.TopicKey, out var b) || r.Confidence > b))
                    bestPerTopic[r.TopicKey] = r.Confidence;
            double doubt = 1.0;
            foreach (var c in bestPerTopic.Values) doubt *= 1.0 - c;
            double combined = 1.0 - doubt;
            if (combined > max) max = combined;
        }
        return max;
    }

CITED, its own docstring: "A 0..1 'heat' reading: how convinced the
most-convinced day-circle NPC is that the player leads a hidden life. DISTINCT
stories corroborate, the noisy-or of an agent's best rumor per topic, so three
half-believed sightings expose you where one never would, while retellings of
the SAME story never stack. This is what makes carelessness (new witnesses every
night) lethal and damage control (kill or discredit a story) meaningful."

CITED, `Game/GameController.cs:285`, how it reaches a player:

    public static string StreetWord(double heat) =>
        heat < 0.2 ? "quiet" : heat < 0.45 ? "murmuring"
        : heat < 0.7 ? "uneasy" : "hostile";

with `CurrentHeat => _gossip.Mill.DayCircleHeat()` at :288, and the docstring
"The street's mood about the player, in words, shared by the HUD and by
conversation context so everyone describes the same weather."

DERIVED, the pipeline in one line: **individual rumours, deduplicated per topic
per person, combined within a person by noisy-or, maximised across the group,
banded into one of four words.**

### 1.2 It satisfies the brief's constraint exactly

- **Nothing is stored.** `DayCircleHeat()` walks `_agents.Values` on every call.
  There is no district score field anywhere; a grep for `districtStanding`,
  `districtRep` and `reputation` across `Core` returns only false friends in
  `Rig.cs` and `Acoustics.cs` about people standing still.
- **The group is a filter, not an object.** `if (a.Circle != "day") continue;`
  is the entire definition of the group. Membership is read at call time.
- **No number reaches the player.** Four words do.

That is the brief's formulation implemented, and it was implemented before the
brief was written.

### 1.3 A second, different expression, and it is the better pattern

CITED, `Game/DialogueUI.cs:1043`, the day summary's liability line:

    talkCount == 0 -> "No open liabilities you know of."
    talkCount == 1 -> "Somebody is carrying something on you"
    talkCount <= 3 -> "A few people are carrying things on you"
    else           -> "Too many people are carrying things on you"

DERIVED: this is a COUNT of people rather than a maximum over them, banded into
language. "A few people" and "too many people" are statements about a
population. "Hostile" is a statement about a mood. The second is what the max in
1.1 cannot actually support, and the first is what it can.

Both mechanisms are in the same codebase, four hundred lines apart, and the
weaker one is the one that names the street.

---

## Part 2. The one more question the brief asked of it

The brief says this is "the same literature as the small-towns topic with one
more question asked of it". The question is how you compute the aggregate, and
the answer in the code is a MAX. That is worth examining rather than accepting.

### 2.1 A max is not a description of a group

CLAUDE.md rule 2 puts it better than I can: "A peak answers 'did it ever', a
median answers 'is this normal', and neither answers the other. Before a new
number enters a conclusion, say which of peak, median, last-wins or at-worst it
is."

`DayCircleHeat` is a peak. Its docstring says so honestly: "how convinced the
MOST-CONVINCED day-circle NPC is".

`StreetWord` then renders that peak as a description of a collective: "The
street is hostile."

DERIVED, with the arithmetic explicit. Suppose the day circle holds forty
people. Consider two towns:

| | one furious person | a town that has turned |
|---|---|---|
| person A | 0.75 | 0.75 |
| the other 39 | 0.05 each | 0.70 each |
| `DayCircleHeat()` | **0.75** | **0.75** |
| `StreetWord` | **"hostile"** | **"hostile"** |

Those two situations are as different as a social simulation can make them, and
the moat exists to tell them apart. The readout cannot.

It is worse in the other direction too. Thirty-nine people at 0.69 and nobody
above it reads as "uneasy", one band below a single person at 0.71. A town in
which almost everybody half-believes something is reported as calmer than a town
with one convinced witness.

### 2.2 What it is right for, and it is not nothing

ASSUMED, and stated as my reading rather than as a finding: the max is probably
the correct aggregator for the thing it was originally built to drive, which is
DANGER. One person convinced enough to act is a threat regardless of what the
other thirty-nine think, and the docstring's framing, "makes carelessness lethal
and damage control meaningful", is a threat model.

The error is not the aggregator. It is that one number is doing two jobs: a
danger reading and a mood description. That is the fault topic 25 closed the
last batch by naming and that I then committed myself in topic 17, appearing
here for the third time in a different system.

### 2.3 What a mood actually needs

DERIVED from 1.3, which already contains the answer in the same codebase: a
group's feeling is a DISTRIBUTION, and the honest renderings of a distribution
are a count above a threshold, a median, or a shape.

Three readings the same walk over `_agents` could produce at no extra cost,
since the loop already visits every agent:

- **how many** are above the sharing floor (`MinConfidenceToShare = 0.2`), which
  is the count that already drives the liability line
- **the median**, which answers "is this normal"
- **the max**, which answers "is anyone dangerous", and which exists

Rule 2's own instruction is to say which of peak, median or at-worst a number
is. Today the street's word does not say, and it is a peak.

### 2.4 And the district question specifically

The brief asks about a DISTRICT's feeling. `DayCircleHeat` filters on
`a.Circle == "day"`, which is a time-of-day social circle, not a place.

CITED: `Core/Population.cs:57` gives every `Resident` a `District` field, and
`:687` holds `DistrictPulse`, which is a pure function:

    Unease(ownedBusinessesHere, prosperity)
      => clamp(0.18 * owned + max(0, 0.45 - prosperity) * 1.2, 0, 1)
    Arrival(unease) => (suspicionFloor, loyaltyShave)

with the docstring "Deliberately gentle: this seeds STARTING posture, it does
not play the game for anybody."

DERIVED: `DistrictPulse` runs in the opposite direction to the brief's question.
It takes district FACTS and seeds an INDIVIDUAL's starting state. It does not
read a district's feeling out of its residents. So the write direction exists
and is correctly shaped, and **the read direction the brief asks about does not
exist for districts at all.** The only group readout in the game is the day
circle.

HOLE: nothing in this checkout computes any per-district aggregate over
residents. The ingredients are all present (a `District` on every resident, the
mill's per-agent rumours, the existing walk) and no function joins them.

---

## Part 3. What could not be established

1. **D34.** Does not exist in this checkout; the register is D1 to D18. Third
   occurrence in thirty topics.
2. **Whether the day circle is a proxy for a district.** `Circle` takes at least
   "day"; what its full value set is, and whether it correlates with `District`,
   was not established.
3. **The day circle's size in play.** The two-town arithmetic in 2.1 assumes
   forty; the real number is unknown and changes how badly the max misleads.
4. **Any external literature.** This topic is almost entirely a code read. The
   aggregation question is a statistics question rather than a games question,
   and CLAUDE.md rule 2 answers it better than anything I found searching.
5. **Whether `StreetWord`'s four bands were set from a printed series.** Rule 2
   would require that and no series is recorded.

---

## Part 4. Findings and interpretation

### Findings

F1. D34 does not exist. The decision register holds D1 to D18 and no `D20` to
`D39` token appears anywhere in the repository.

F2. `Gossip.DayCircleHeat()` computes group standing live from individual
records, storing nothing: filter to the circle, best rumour per topic per
person, noisy-or within a person, max across people.

F3. `GameController.StreetWord` bands that into four words at 0.2, 0.45 and 0.7.
No number reaches the player.

F4. The brief's constraint is therefore already met: computed on read, stored
nowhere, expressed in language.

F5. The aggregator is a MAX, and its own docstring says so: "how convinced the
most-convinced day-circle NPC is".

F6. A max cannot distinguish one furious person from a town that has turned.
Both produce "hostile". Thirty-nine people at 0.69 report as calmer than one
person at 0.71.

F7. A better pattern exists four hundred lines away: `DialogueUI.cs:1043` bands
a COUNT of people carrying something into "somebody", "a few people", "too many
people".

F8. `DistrictPulse` seeds an individual's starting posture from district facts.
It is the write direction. No read-direction district aggregate exists anywhere.

F9. `DayCircleHeat` filters on a social circle, not on a district, so the game
has no district-level group standing at all.

### Interpretation

I1. The brief's question has a good answer already in the codebase and my main
job here was to find it rather than to design one. Computed on read, group as a
filter, language as the output: that is the pattern, and it should probably be
written down as the pattern rather than existing as one function.

I2. The finding worth acting on is that the street's word is a peak rendered as
a description. It is rule 2's exact fault, in the expression layer of the moat,
and it is the third appearance of that shape in this research (topic 25 named
it, topic 17 committed it, this is it again). The aggregator is probably right
for danger and wrong for mood, and the cure is not to change it but to stop one
number doing two jobs.

I3. The cheapest improvement is already written: the liability line's
count-and-band. The same loop that computes the max could return a count above
the sharing floor and a median at no extra cost, because it already visits every
agent.

I4. For districts specifically there is nothing to critique, because there is
nothing there. Every ingredient exists and no function joins them, which is the
honest state and worth knowing before anybody designs a district reputation
feature that the brief's formulation would forbid.
