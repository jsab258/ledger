# How a game teaches a social system in thirty minutes

Research topic 28. Delivered to the studio. Nothing here is an instruction.

**Standing egress note.** One route out of this container reads a page in full:
`curl` reaches package registries and `raw.githubusercontent.com`. `github.com`
and `api.github.com` return 403; arxiv, Wikipedia, journals, news and vendor
documentation return 000. Source repositories and licence files are readable
primary sources; research literature is not. Everything cited below from press
or design writing is a search engine's summary and is labelled so.

The brief is right that no queued topic covers this, and right about why it
matters: KCD2 explains almost nothing and has a hundred hours to recover. This
part of the work turned out to be mostly arithmetic, and the arithmetic settles
a question topic 25 left open.

Labels: CITED, DERIVED, ASSUMED, HOLE.

---

## Part 1. What thirty minutes actually is, and a hole closed

Topic 25 reported that no play-mode clock rate exists in this checkout and left
it as a hole. That was wrong: I searched for `MinutesPerSecond`, `clockRate`,
`ClockScale`, `DayMinutes` and `compression` and the constant is called
`MinutesPerRealSecond`.

CITED, `Game/GameController.cs:12`:

    public float MinutesPerRealSecond = 2f; // 1 game day = 12 real minutes
                                            // (sim mode overrides)

CITED, `GameController.cs:990`, the accumulator that spends it, and
`SimDirector.cs:65`, `const float SimMinutesPerRealSecond = 20f; // 1 game day
= 72 real seconds`, applied at `:352`. So the sim runs ten times faster than
play, which is why topic 17 found the 20 and mistook it for the only figure.

CITED, `GameController.cs:14`: the game begins at
`new GameTime(1, 9, 0)`, nine in the morning on day one.

DERIVED, and this is the frame everything else in this delivery sits in:

| quantity | value |
|---|---|
| play clock | 2 game-minutes per real second |
| one game day | 12 real minutes |
| **the Meridian Test's 30 real minutes** | **2.5 game days** |
| phase 1's gossip gate, one in-game week | 84 real minutes |
| that gate against the whole first session | **2.8x longer** |

That last row is the resolution of topic 25's open question, now a number rather
than a hole. Phase 1's gate permits a witnessed crime to reach a second and
third NPC on a schedule nearly three times slower than the Meridian Test's
condition 2 requires. A build can pass the gate and fail the test, and nothing
currently connects them.

---

## Part 2. What the game teaches today, and when

There IS an onboarding, and the systems inventory types it honestly.

CITED, `production/systems-inventory.json`, tile "first hour and tutorial",
status PARTIAL, phase 3: "First-morning onboarding is four diegetic toast lines
fired on conditions, and Act I has its pressure points. No authored first hour
judged as one thing is in this checkout, and no record committed here says
anybody has played one."

CITED, `GameController.cs:1226`, `CheckOnboarding`, the four lines verbatim with
their triggers:

    09:02  "Your feet know the way: WASD walks, Shift runs. The street watches
            whoever is moving."                                     toast 8s
    09:10  "The pub is yours now. Walk up to anyone and press {Talk} to talk
            - they remember."                                       toast 9s
    10:00  "Press {Ledger} for your ledger: what you believe the street knows
            about you - and what you hold over it."                 toast 9s
    12:00  "Tonight the outfit will want its first drop made. {Coat} toggles
            the runner's coat - harder to name in the dark, harder to explain
            in daylight."                                          toast 10s

CITED, the design reasoning above it, which is sound and worth keeping: "Movement
first - the playtest plan's research found the game taught talking before it
ever taught WALKING, and a first-time player on a borrowed laptop starts by
standing still. Every key is printed from the live binding, not the default
letter: the prompt is read at the exact moment a player trusts it most."

DERIVED, converting those game-clock triggers at 2 game-minutes per real second
from a 09:00 start:

| line | game time | real time | note |
|---|---|---|---|
| walking | 09:02 | **1.0 s** | 8-second toast |
| talking | 09:10 | **5.0 s** | **fires while line 1 still has 4 s to run** |
| the ledger | 10:00 | **30 s** | |
| the coat | 12:00 | **90 s** | |

**The entire onboarding is delivered in the first ninety seconds, and two of the
four lines overlap.** A player who has not yet worked out that WASD moves them
is told about the ledger twenty-five seconds later and about a night job a
minute after that.

That is not a criticism of the writing, which is good and diegetic. It is an
arithmetic consequence of firing a teaching sequence on a game clock that runs
at 120 times real time. The triggers were almost certainly chosen as story beats
("mid-morning", "noon") and the clock turns them into a burst.

CITED, and in the code's favour, the two follow-ups that are event-driven
rather than timed, at `GameController.cs:1252`: "the two things it structurally
cannot teach are the two-money economy and the day cycle, because a hint about
money not yet held or a close not yet lived teaches nothing. These fire at the
first occurrence instead."

DERIVED: the file already contains the correct principle and applies it to two
of six hints. The four that matter most are on the clock.

---

## Part 3. What the research says, and the one negative example worth having

CITED: teaching through action rather than instruction is the standard position,
with "the very best tutorials occur organically with the level design itself",
and the blunt form, "if you have to explain it, it's broken". Portal 2's opening
is cited as a playable non-level introduction followed by six levels of
graduating complexity, with the full toolset only in hand at the end of a 20 to
30 minute sequence.
[Medium, Portal 2 taught me everything I know about onboarding](https://medium.com/@mhkt/portal-2-taught-me-everything-i-know-about-onboarding-4e5abf0310c1),
[Game Developer, How onboarding should be applied to tutorials](https://www.gamedeveloper.com/design/how-onboarding-should-be-applied-to-tutorials)

CITED, the ordering rule, which transfers directly: "Movement usually comes
first because nothing else can be taught without it, then a resource, then a
threat, then a reason the two are connected." A first session has to "teach a
control scheme, introduce at least one system worth caring about, hand over a
first success, and hint at something bigger without spoiling it."
[COGconnected, The first 30 minutes: how games decide what to give a new player](https://cogconnected.com/2026/08/the-first-30-minutes-how-games-decide-what-to-give-a-new-player/)

CITED, the negative example, and it is the closest analogue to LEDGER's
problem: Dishonored's Chaos system runs invisibly during a mission and reports
afterwards, tallying kills and detections at the end. The reported player
experience is that it "made it feel like the game was penalizing players for
killing" rather than that they understood a system.
[PC Gamer, Bethesda reveals raw details on Dishonored chaos and stealth detection mechanics](https://www.pcgamer.com/dishonored-chaos-guide-stealth-no-detection-explanation/)

DERIVED: a hidden system with a delayed aggregated readout teaches
PUNISHMENT, not MECHANISM. That is the exact shape a day-close summary of what
the town now knows would take, and it is the obvious thing to reach for.

---

## Part 4. The specific thing our first session has to do

DERIVED, applying the ordering rule to this game rather than to a shooter. The
research's ladder is movement, resource, threat, connection. LEDGER's is:

1. **You move.** Already first, correctly, and already the first line.
2. **You are seen.** Somebody's attention lands on you and you can tell.
3. **It was written down.** The seeing became a fact that outlived the moment.
4. **It came back.** Somebody who was not there uses it.

Steps 2 and 4 are conditions 2 of the Meridian Test in two halves, and step 3
is the moat. Today the game ASSERTS all three in toast text within ninety
seconds ("the street watches whoever is moving", "they remember", "what you
believe the street knows") and demonstrates none of them.

Topic 25 found the one property shared by both cases where a memory system
landed loudly rather than quietly: the memory INTERRUPTED the player rather than
colouring a greeting. An orc came back with the scar and mentioned it. Step 4 is
that, and it is the only one of the four a toast cannot fake.

DERIVED, the arithmetic of whether step 4 can happen at all in thirty minutes.
A first session is 2.5 game days. Phase 1's gate asks that a witnessed crime
reach a second and third NPC within one in-game week, which is 2.8 first
sessions. So on the gate's own tolerance, **the rumour of something a player
does in their first half hour need not reach anybody until long after they have
stopped playing.**

That does not mean the mill is too slow. It means nothing has ever asked it to
be fast, and the two gates that describe the same capability were written
against different clocks by different documents.

HOLE, and it is the one I would most want measured: how long a rumour ACTUALLY
takes to make its first hop in play. Every input exists (`HopDecay = 0.8`,
`MinConfidenceToShare = 0.2`, `TalkRange = 6f`, the band system from topic 27,
and now the clock) and no run reports it. It is a single number, it decides
whether condition 2 is reachable, and nothing in the verdict carries it.

### 4.1 One thing that is cheap and is not a toast

`canon.md` already states the standing ladder: "What the town calls you reads
out your standing: the new owner, then Novak, then Tom, then Toma. The gate is
knowing, not liking."

DERIVED: that is step 4 in its cheapest possible form and it needs no crime, no
witnesses, no hops and no time. A stranger calling you "the new owner" and, half
an hour later, somebody calling you "Novak" is the world demonstrating that it
has kept track, in the register of the game rather than in a hint box. Topic 25
reached the same conclusion from the player-behaviour side and this topic
reaches it from the clock side, which is the strongest kind of agreement two
pieces of research can produce.

---

## Part 5. What could not be established

1. **Whether anybody has played a first hour.** The inventory tile says nobody
   has, and no record contradicts it.
2. **How long a rumour's first hop takes in play.** Part 4's hole.
3. **Whether the toast channel queues or replaces.** Two overlapping toasts is
   an arithmetic finding, not an observed one; whether the UI stacks them,
   replaces them or drops one is not established here.
4. **Primary sources for Part 3.** All summaries.
5. **Whether the Unreal build has any of this.** Everything in Part 2 is Unity.

---

## Part 6. Findings and interpretation

### Findings

F1. The play clock is `MinutesPerRealSecond = 2f`: one game day is 12 real
minutes. The sim overrides it to 20. Topic 25's claim that no play rate exists
was wrong.

F2. A 30-real-minute first session is 2.5 game days.

F3. Phase 1's gossip gate of one in-game week is 84 real minutes, 2.8 times the
whole first session.

F4. The game starts at 09:00 on day 1 and fires four onboarding toasts at 09:02,
09:10, 10:00 and 12:00.

F5. In real time those are 1 s, 5 s, 30 s and 90 s. The whole sequence lands
inside ninety seconds and lines 1 and 2 overlap by four seconds.

F6. The code already knows the right principle and applies it to the two hints
it cannot time: money and the day close fire on first occurrence.

F7. The inventory types "first hour and tutorial" as PARTIAL at phase 3, noting
no authored first hour exists and nobody has played one.

F8. Dishonored's Chaos system, the nearest analogue, reports invisibly and
after the fact, and is reported as reading to players as punishment rather than
as mechanism.

F9. The four toasts assert that the street watches, that people remember, and
that a ledger holds what they know. None of the three is demonstrated.

### Interpretation

I1. The finding here is not that the onboarding is badly written. It is well
written and diegetic. It is that a teaching sequence fired on a clock running at
120 times real time becomes a ninety-second burst, and nobody would have seen
that without doing the division.

I2. Phase 2's gate is "Jafar feel check passed" and the first hour is typed
phase 3. The feel check therefore happens before the thing that would make a
first session legible exists. That ordering is worth a look on its own.

I3. The two gates that describe the same capability, phase 1's in-game week and
the Meridian Test's thirty real minutes, are now known to differ by 2.8x. That is
no longer a mismatch of units, it is a quantified gap, and it is the cheapest
thing in this delivery to act on because both numbers already exist.

I4. Everything in this delivery came from three constants and a division. The
research in Part 3 is real and it is the least valuable part of the topic. What
decided the question was reading `MinutesPerRealSecond` and multiplying, which
is the second time in this batch that the strongest finding was sitting in a
file I had already opened.
