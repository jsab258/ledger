# Whether the simulation should run live at all

Research topic 27. Delivered to the studio. Nothing here is an instruction.

**Standing egress note.** One route out of this container reads a page in full:
`curl` reaches package registries and `raw.githubusercontent.com`, verified with
real content. `github.com` and `api.github.com` return 403; arxiv, Wikipedia,
Hansard, journals, news and vendor documentation all return 000. So source
repositories and licence files are readable primary sources and research
literature is not. Everything cited below from press or devblogs is a search
engine's summary and is labelled so.

The brief set a precondition before anything else: establish whether Shadows of
Doubt's precomputed day is a full simulation or a schedule resolution, because
that decides what the finding is worth. Part 1 settles it. Parts 2 and 3 are
what it is worth, and Part 3 contains a correction I owe to three earlier
deliveries.

Labels: CITED, DERIVED, ASSUMED, HOLE.

---

## Part 1. The precondition, settled: it is a schedule resolution

CITED, ColePowered's DevBlog 8, "Simulating a City", via search summary (the
devblog host is egress-blocked):

- "The game needs a brief period of calculation time before the start of each
  day (typically no more than 10-15 seconds depending on the population count).
  During this time their ACTIVITIES FOR THE DAY ARE CHOSEN AND MAPPED OUT FOR
  THEM."
- "Simulating 100s of citizens would be a hugely intensive task for a system to
  handle in real time, which is why the developers chose not to handle it in
  real-time."
- "Citizens can deviate from their scheduled routines if the situation calls for
  it, and their altered routine can be calculated by the game in real time as
  there will never be more than a handful of citizens requiring deviations."

[ColePowered, DevBlog 8: Simulating a City](https://colepowered.com/shadows-of-doubt-devblog-8-simulating-a-city/),
[ModDB mirror of DevBlog 8](https://www.moddb.com/games/shadows-of-doubt/news/shadows-of-doubt-devblog-8-simulating-a-city)

DERIVED, and this is the answer the brief asked for: **it is a schedule
resolution, not a simulation.** The 10 to 15 seconds buys an ITINERARY per
citizen, chosen and mapped out in advance. It does not fast-forward a world and
record what happened in it. Nothing is simulated during those seconds except
the act of planning.

What that rules out, stated plainly so the finding is not oversold: a
precomputed day cannot tell you who saw what, who was hurt, what was stolen or
who fell out with whom, because none of those things happen during the
precompute. They happen when the day is played and citizens deviate.

What it rules IN is narrower and still valuable: after the precompute, the
position of every citizen at every hour is a KNOWN QUANTITY rather than a thing
you must run a body to discover.

HOLE: the devblog's own text beyond these lines could not be read. How
deviations are reconciled with the plan, whether the plan is regenerated
mid-day, and what happens to a citizen whose plan is invalidated are all
unestablished.

---

## Part 2. Why that distinction matters so much here

LEDGER's moat is not schedules. It is perception, memory and gossip, and all
three are EVENT-DRIVEN. A precomputed itinerary answers "where is everyone",
which is a different question from "who knows what".

But the two are joined at one specific point, and it is the point this project
already depends on.

CITED, `Game/GossipDirector.cs:660`, the whole of the predicate that decides
whether a rumour can move:

    bool Together(string a, string b)
    {
        var pa = PositionOf(a);
        var pb = PositionOf(b);
        if (pa == null || pb == null) return false;
        return Vector3.Distance(pa.Value, pb.Value) <= TalkRange;
    }

with `const float TalkRange = 6f` at :34, and `Mill.Tick(now, Together)` called
from :225.

DERIVED: gossip in this project propagates only between two people who are
within six metres of each other AND both have a position. So the question "can
this rumour move" reduces entirely to "where is everyone", which is exactly the
question a precomputed day answers.

That is the real relationship between the two architectures, and it is tighter
than it first looks: Shadows of Doubt's precompute is not an alternative to our
gossip mill, it is a way of supplying the one input our gossip mill cannot do
without.

---

## Part 3. The correction: LEDGER already has this, under a name I did not grep for

### 3.1 What I said, and why it was wrong

Topics 17, 21 and 25 each stated that this project has no simulation radius and
simulates everybody at full rate everywhere. Topic 21 put it most explicitly:
"there is no simulation radius in this project. A grep for `SimRadius`,
`simulationRadius`, `offscreen`, `AbstractSim` and `Distant` across Core and
Game returns only visual-detail comments."

That grep was run and its output was reported accurately. The conclusion drawn
from it was wrong, because the project does not use any of those five words. It
calls the thing `Lod` and `Band`.

This is CLAUDE.md rule 1's exact failure: I asserted an absence from a search
that did not cover the project's own vocabulary, and then quoted that absence in
two further deliveries.

### 3.2 What is actually there

CITED, `Core/Population.cs`:

    public enum Lod { Near, Mid, Far }
    public double NearMetres = 70;
    public double MidMetres  = 130;
    public double BandSlack  = 12;     // hysteresis, so a walker on the
                                       // boundary does not strobe
    public int NearCap = 28;
    public int MidCap  = 120;

CITED, `Game/PopulationHost.cs:962`, `ApplyBand`, what each band costs:

- **Near**: `EnsureInMill(r, mill, ambientReach)` AND `EnsureWalker(r)`. In the
  gossip network and drawn.
- **Mid**: `EnsureInMill(...)` AND `DespawnWalker(r)`. In the gossip network,
  NOT drawn.
- **Far**: `CrowdPositionOf` returns null at :958 (`if (r == null || r.Band ==
  Lod.Far) return null;`).

CITED, `PopulationHost.cs:934`, how a Mid-band person's position is obtained
with no body:

    Vector3 WhereIs(Resident r)
    {
        if (Population.OutdoorPosition(r, Now.Day, Now.Hour, out var ox, out var oz))
        { ... snap to StreetMap.NearestOnStreet ... }
        bool working = Now.Hour >= r.WorkFromHour && Now.Hour < r.WorkToHour;
        return working ? new Vector3(r.WorkX, 0, r.WorkZ)
                       : new Vector3(r.HomeX, 0, r.HomeZ);
    }

DERIVED, and it is the finding of the topic: **the Mid band IS the Shadows of
Doubt architecture, already built.** A position derived from a schedule and a
clock rather than from a body, snapped to the street network, feeding the same
co-location predicate the drawn crowd uses. The hook that carries it,
`GossipDirector.ExtraPosition`, is assigned at `GameController.cs:924` and its
comment states the reason exactly: "without it the crowd could carry talk but
never pass it on, because a person with no body has no position and Together
would always say no."

The difference from ColePowered is one of timing, not of kind. They resolve the
whole day in one 10-to-15-second pass at dawn. We resolve one person's position
on demand, per query, from the same kind of data. Both replace a body with a
schedule lookup.

### 3.3 Where the moat actually stops

CITED, the band populations from the last landed run in
`game-design/sim-shots/verdict.txt`: **near=22, mid=159, far=382**.

DERIVED: 563 residents were banded at that moment. 181 of them, 32%, could
participate in gossip. **382 of them, 68%, could not**, because
`CrowdPositionOf` returns null for the Far band, so `Together` returns false for
every pair involving them.

That is not a defect. It is a deliberate, documented, hysteresis-protected
performance boundary with caps on both bands, and it is exactly the decision
GSC had to make under launch pressure in topic 21 and made badly. This project
made the same decision early, calmly, with the numbers printed.

What it does mean is that the sentence "the town remembers" has a measured
radius, and the radius is 130 metres. A crime witnessed by somebody who then
walks past 130 metres from the player stops being able to tell anyone until
they come back. Whether that matters depends on whether rumours are carried by
PEOPLE moving or by the PLAYER moving, and nothing in this checkout measures
which.

### 3.4 A second correction, to topic 17's framing

While establishing the above I found the landed per-system frame cost ladder,
which topic 17 reported as not existing in a usable form. It is in the same
verdict file:

    frameCost=[all:26.3/noPost:24.3/noShadow:19.6/noShafts:25.4/
               noBodies:26.2/noPixLights:20.6/shadow45:24.8]

DERIVED, by subtraction from `all:26.3`:

| system | cost | share of frame |
|---|---|---|
| shadows | 6.7 ms | 25.5% |
| pixel lights | 5.7 ms | 21.7% |
| post | 2.0 ms | 7.6% |
| light shafts | 0.9 ms | 3.4% |
| **all drawn bodies** | **0.1 ms** | **0.4%** |

Topic 17 framed the frame budget as a crowd problem and did the arithmetic in
rendered bodies per millisecond. This measurement, which was landed and
committed before that delivery was written, says the entire drawn crowd costs a
tenth of a millisecond and lighting costs twelve and a half.

Both numbers in topic 17 were correctly read: `npcsMs=4.85` is the CPU cost of
walker ticks and is genuinely 76% of attributed game time. The error was
framing: I measured the SIM cost of people and then wrote the topic as though
the RENDER cost of people were the binding constraint. It is not. On the landed
evidence the binding constraint is lighting.

That is precisely the fault topic 25 closed the queue by naming, a number that
exists for one half of a question and gets quoted for both, and I committed it
myself in the same batch.

---

## Part 4. So should the simulation run live

DERIVED, and the answer is narrower than the question:

It already does not, for 68% of the population. The architectural choice in the
brief has been made here and was made before I looked. What remains open is not
whether to precompute but THREE smaller things the evidence actually bears on.

1. **Whether the Mid band's position should be resolved once per day rather than
   once per query.** ColePowered's reason for batching is that planning is
   intensive; `WhereIs` is cheap (an outdoor-position lookup, a street snap, or
   two field reads) so the batching argument does not obviously transfer. This
   is a measurement nobody has taken.
2. **Whether the Far band should be able to gossip at all.** Today it cannot,
   by construction. A schedule-only propagation for Far-band pairs would cost no
   bodies and no render, and would make the 382 count for something. Whether the
   moat needs it depends on 3.3's unanswered question.
3. **Whether the radius should be the same for SEEING and for TELLING.** Right
   now one number, the band, governs both, and `TalkRange = 6` governs the
   second within it. Perception and transmission are different physical
   processes with different ranges and this project already knows that
   elsewhere: `Perception.cs` has five distinct rung distances.

---

## Part 5. What could not be established

1. **The devblog itself.** Host blocked; Part 1 rests on summaries of it.
2. **How ColePowered handles a deviated plan**, which is the interesting half of
   their design and the half nobody summarised.
3. **What `WhereIs` costs.** Never measured, and it decides item 1 above.
4. **Whether rumours travel by people moving or by the player moving.** Decides
   whether the Far band's exclusion matters.
5. **The Unreal side of any of this.** Everything in Part 3 is Unity, the
   engine D16 archived. Whether the band system was ported is not established
   here.

---

## Part 6. Findings and interpretation

### Findings

F1. Shadows of Doubt's precomputed day is a SCHEDULE RESOLUTION: "their
activities for the day are chosen and mapped out for them", 10 to 15 seconds,
explicitly because real-time simulation of hundreds of citizens was too
intensive. Deviations are computed live for "a handful".

F2. LEDGER's gossip can move only between two people within `TalkRange = 6f`
who both return a position.

F3. LEDGER has a three-band LOD: `Lod.Near/Mid/Far`, `NearMetres = 70`,
`MidMetres = 130`, `BandSlack = 12`, `NearCap = 28`, `MidCap = 120`.

F4. The Mid band is in the gossip mill with no body, its position computed by
`WhereIs` from schedule and clock and snapped to the street network. That is the
same architecture as the precomputed day, resolved per query instead of per day.

F5. The Far band returns no position, so it cannot gossip. The last landed run
banded near=22, mid=159, far=382: 68% of residents outside the moat.

F6. Topics 17, 21 and 25 each stated this project has no simulation radius.
That was wrong; the grep did not cover the project's own vocabulary.

F7. The landed verdict carries a per-system frame ladder:
`all:26.3/noShadow:19.6/noPixLights:20.6/noBodies:26.2`. Drawn bodies cost
0.1 ms of 26.3; shadows and pixel lights cost 12.4 ms between them.

F8. Topic 17 framed the frame budget as a crowd problem. On this evidence it is
a lighting problem.

### Interpretation

I1. The brief's architectural question is already answered in this codebase and
was answered before I started auditing it. The useful output of this topic is
not a recommendation to adopt the approach but a correction to three deliveries
that said it was absent.

I2. The one number worth putting in front of Jafar is 382. Two thirds of the
simulated population is outside the range at which anybody can tell anybody
anything, and that is a deliberate, well-documented performance decision whose
consequence for the moat has never been measured.

I3. My own errors in this batch have one shape and it is the shape I named at
the end of the last batch. I grepped for the wrong vocabulary and reported an
absence; I measured a CPU cost and framed a render conclusion. Both are the same
fault as the ones I was finding, which is worth saying plainly rather than
burying in a findings list.

I4. The strongest evidence in this delivery came from a file I had already read
twice. `verdict.txt` carried `frameCost=[...]` and `near=/mid=/far=` throughout
the previous batch, and I extracted the keys I went looking for and did not read
the ones I had no question for. That is a research failure mode worth recording:
a verdict file is only as good as the questions brought to it.
