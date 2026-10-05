# Coverage audit: what showed up five times

STATUS: SPEC (research delivery). Branch `research/coverage-audit`, from commit
`074f85b`. Written 2026-09-14 by the research lane, after the five game
deliveries.

NOTHING IN THIS FILE IS AN INSTRUCTION. It proposes no tile, files no queue
item, and edits no inventory. The deliveries are recommendations and the
decisions are Jafar's.

## 0. What this file is for

The brief's reason, quoted: "what was absent in every game's mapping, since a
gap that shows up five times is a category we are blind to rather than a feature
we skipped, and any research topics the audit revealed that are not already in
my queue."

Two sections do that (2 and 5). Three more exist because the audit produced
results the per-game files could not hold: the totals (1), the twenty distinct
recommendations after duplicates are merged (3), and the seven questions that
now sit with Jafar (4). Section 6 is what the whole audit could not establish.

The five deliveries are:

| Game | Branch |
|---|---|
| Kingdom Come Deliverance 2 | `research/coverage-audit-kcd2` |
| Hitman (World of Assassination) | `research/coverage-audit-hitman` |
| Red Dead Redemption 2 | `research/coverage-audit-rdr2` |
| Disco Elysium | `research/coverage-audit-disco-elysium` |
| Shadows of Doubt | `research/coverage-audit-shadows-of-doubt` |

## 1. The totals

**188 systems** enumerated across five games and mapped against the 91 tiles in
`production/systems-inventory.json`.

| Column | Count | Share |
|---|---|---|
| COVERED | 41 | 22% |
| PARTIAL | 26 | 14% |
| ABSENT | 106 | 56% |
| RULED OUT by a decision record | 15 | 8% |
| **Total** | **188** | |

Of the 106 absent: **33 IN, 55 OUT, 12 ASK, 6 BENCHMARK.**

WHAT THE 188 IS A COUNT OF, because a number without that is not a measurement:
distinct player-facing or world-facing systems I could establish each game
contains, from the search channel, in one session per game. It is not a census
of those games. Each delivery's "what could not be established" names what it
knows it left out, and the biggest omissions are combat in all five, animation
in RDR2, and the entire Hitman Absolution design.

THREE FURTHER IN RECOMMENDATIONS SIT IN THE PARTIAL COLUMN and are not in the
33: RDR2's A3, D2 and D7, where a tile covers part of a thing and the uncovered
part is worth building. Four PARTIAL entries in KCD2 carry one shared IN. So 39
entries carry an IN, and section 3 collapses them to twenty.

**The OUT rate is 52 percent of everything absent, and that is the number the
brief asked to see.** The two games with the lowest OUT rate are Hitman (40
percent) and Shadows of Doubt (31 percent), and both deliveries defend the
figure rather than present it: those two are games about being observed in a
small dense place, which is pillar 1 and pillar 6 restated.

## 2. The gap that showed up five times

**Every one of the five games tells the player where they stand with the world.
LEDGER has no such surface at all.**

This is the only category absent in all five mappings, and I have checked it
against the honest denominator rather than asserting it:

| Game | Its surface | CITED in |
|---|---|---|
| KCD2 | Reputation shown per settlement and per social group | delivery D1 to D3 |
| Hitman | The white dot over an enforcer; the filling suspicion meter | delivery A3, A7 |
| RDR2 | The WITNESS banner; a white or red eye icon per witness; the wanted level; a per-county bounty | delivery A1, A2, A9 |
| Disco Elysium | Every modifier itemised with its source before you commit | delivery A2 |
| Shadows of Doubt | The pinboard; the case form you write a name into | delivery C1, C3 |

On our side: the tile "the what-they-know HUD for wanted states" is typed
absent, and D12 deliberately scoped it down to "law enforcement's institutional
knowledge during wanted states, and nothing else". The tile "HUD" (exists) is
"Clock, money and slot on one line plus the toast channel", and the inventory
says so explicitly: "The what-they-know HUD the roadmap names for wanted states
is a separate thing and is not here."

FIVE OF FIVE IS THE ONLY CATEGORY THAT REACHED FIVE. The honest denominators for
the near misses, because a four is not a five:

- **Appearance and clothing as an identity the world holds: 4 of 5.** Present in
  KCD2, Hitman, RDR2 and Disco Elysium (in the one form we cannot use, as a stat
  bonus). Shadows of Doubt identifies people by face and fingerprint and does not
  use it.
- **The gap between the act and the world finding out: 4 of 5.** Hitman's body
  discovery, RDR2's witness who must travel, Shadows of Doubt's evidence that
  decays in hours and citizens questioned later, KCD2's stolen tag that cools
  over one to two weeks. Disco Elysium has no simulation and so cannot have it.
- **Physical evidence at a PLACE rather than on a person: 3 of 5.** Hitman,
  RDR2, Shadows of Doubt.
- **Standing held by a group or a district rather than by an individual: 2 of 5
  strongly** (KCD2 per settlement and social group, RDR2 per county), with
  Hitman's trespass zones and Disco Elysium's political alignments as weak
  fourths.

### 2.1 Why the five-of-five is not simply "build a HUD"

D12 is not wrong and this finding does not overturn it. Its argument is exact:
"if knowing is free, then asking around, buying gossip and eavesdropping are
decorations rather than verbs, and the information layer has no cost, no risk
and no play in it."

But D12 governs WHAT NPCs KNOW. Four of the five surfaces above are not that.
Disco Elysium's is a breakdown of the game's own arithmetic. RDR2's eye icon is
the player character noticing a person looking at him. Hitman's white dot is who
would see through a disguise, which in our model is who knows you well, and
that is Tom's own knowledge. Only the KCD2 reputation screen is a genuine read
of other minds.

`Core/Observation.cs` has already decided the hardest case in the right
direction, and the RDR2 delivery treats it as a correction to the Hitman one:
`Awareness.NeitherKnows` is documented as "THE QUIET HORROR CASE, and the design
deliberately gives the player nothing here, no ghost, no warning."

So the question this finding raises is not whether to show NPC minds. It is
whether the player is ever shown THEIR OWN position: what Tom can see, what Tom
can work out, and why the game decided what it decided. Currently the answer is
no, in every case, and five games disagree. That is section 4's questions 4 and
5, and it is the single most consequential result of this audit.

## 3. The twenty distinct recommendations

39 IN-bearing entries collapse to twenty things, because the games agree far
more than they differ. Sorted by how many independent games arrived at them.

**Confirmed by three or more games**

1. **Appearance as a perception input**: what you are wearing, and whether it is
   dirty, bloodied or torn. KCD2, Hitman, RDR2, and Disco Elysium in a form D11
   forbids. Half built already (`Core/Traces.cs` blood, `Disguise v0`). The
   period research is half done too: `production/art/atlas-02/research/adult-clothing-by-occupation.md`
   exists.
2. **The gap between the act and the discovery.** Hitman (a body is found at a
   time by a person), RDR2 (a witness must reach somebody), Shadows of Doubt
   (evidence and questioning both happen later). Our own
   `HomicideBook.Pressure` has no travel term.

**Confirmed by two games**

3. **The camera and the tape** as a witness that cannot be talked to. Hitman,
   Shadows of Doubt. `canon.md` has already specified it.
4. **Sleep and crossing a day.** KCD2, Disco Elysium. A tile exists, typed
   absent.
5. **Objects that can be traced back to what you did.** KCD2 (the stolen tag),
   Shadows of Doubt (documents that name people). `Core/Traces.Origin` is built.

**From one game each**

6. Enforcers named as a system: who can see through a disguise is who knows you
   (Hitman).
7. Blend-in: behaviour that fits what you appear to be (Hitman).
8. Frisking at a threshold, which would finally exercise `Arsenal.Concealment`'s
   four rungs (Hitman).
9. Finding a person from a description, the identification ladder run backwards
   (Hitman).
10. The phone box as the period distraction verb (Hitman, small, conditional).
11. The town's behaviour changing after a crime: people stay in, carry
    something, ask for more patrols (KCD2).
12. Persuasion, coercion and intimidation as a resolved system, re-based off
    memory rather than stats (KCD2).
13. A codex entry unlocked on first contact with a system (KCD2, small, a rider
    on the first-hour tile).
14. Nod or needle: an interaction verb available on every person (RDR2).
15. Weather as an event that moves people indoors (RDR2).
16. Habits belonging to a person, which make them predictable (RDR2).
17. Show the working: itemised reasons for a social judgement (Disco Elysium).
18. Failure producing content rather than a refusal (Disco Elysium).
19. The lit window as a witness, not only as a light (Shadows of Doubt).
20. What you leave at a scene: prints, a heel mark, a dropped object (Shadows of
    Doubt).

Five of these twenty are half built already (1, 2, 5, 8, 19), in the sense that
the model exists and the call site, the surface or the other direction does not.
That is a different shape of work from the other fifteen and the studio should
not price them the same.

## 4. The seven questions now sitting with Jafar

Collected from the five summaries so they can be answered in one sitting rather
than five. Each is stated where it was raised.

1. **Does the town have an opinion, or only people?** Per-district or per-group
   standing against D11's ban on a global number. Raised in KCD2, repeated by
   RDR2. Two games.
2. **What stops a player reloading to un-see a witness?** Raised in KCD2 (save
   scarcity), sharpened by Disco Elysium (a game that says up front which
   choices are permanent) and by Hitman (Elusive Targets). Three games.
3. **Does Meridian have a map, or do you learn it by walking and asking?**
   Raised in KCD2's hardcore mode, where asking a person for directions replaces
   the marker.
4. **How much does the player see of being watched, while it is happening?**
   Raised in Hitman, corrected in RDR2: the unaware case is already decided
   against in `Core/Observation.cs`, so this is only about the aware cases and
   about knowledge Tom would legitimately hold.
5. **After the fact, does anything tell the player who saw what?** Raised in
   Hitman. With 4, this is the five-of-five finding in section 2.
6. **A notebook, or a corkboard with string?** D12's journal against Shadows of
   Doubt's pinboard. Raised in Shadows of Doubt, and it links to queue topic 13.
7. **Do the five built-but-untiled systems get tiles?** Bookkeeping rather than
   design, and the reason is section 5.1.

Questions 4 and 5 are the same question at two moments and should be answered
together. So should 2 and 5, since a readout of who saw what is also the thing
that would make reloading pointless.

## 5. What the audit revealed about our own instruments

### 5.1 The inventory cannot see five systems it already owns

Found in games 1 and 2, measured by reading the code and counting tokens in
`production/systems-inventory.json`:

| System | Where it lives | Reached from the Game layer |
|---|---|---|
| Blood on the player, noticed against distance and light, aged, washed | `Core/Traces.cs` (`Stain`, `Noticeable`, `Age`, `Wash`, `CountsAsMark`, `SocialCost`) | `Game/ViolenceHost.cs:294`, `Game/NpcWalker.cs:904`, `Game/SimDirector.cs:1670` and `:7302` |
| Object provenance across five origins, with a history never cleared | `Core/Traces.cs` (`Item`, `Origin`, `Traceability`, `ResidualRisk`, `Dispose`) | `Game/EvidenceHost.cs`, `Game/SimDirector.cs:6849` to `:6874` |
| Disguise | `Core/Gossip.cs:259` | `Game/GameController.cs:189`, `Game/GossipDirector.cs:678`, `Game/SimDirector.cs:13797` and `:15311` |
| A four-rung concealment model | `Core/Arsenal.cs` (`Concealment`, `Fits`) | `Core/Coat.cs` |
| The lit window as an information carrier | `Core/Occupancy.cs` | `WorldBuilder.SetWindowsLit` |

Token counts over the whole 70,491-byte inventory file: `Traces` 0, `Stain` 0,
`blood` 0, `stolen` 0, `disguise` 0, `appearance` 0, `clothing` 0, `conceal` 0,
`concealment` 0, `blend` 0, `cctv` 0, `tape` 0. `EvidenceHost.cs` appears once,
inside the evidence list of a tile about planning jobs and banking takings. The
single hits for `clothes`, `dirt` and `washing` are false friends and are named
in game 1.

WHAT THIS IS AND IS NOT. It is not a claim that the inventory is wrong: it is
typed by a director under a ruling, and every tile it has is a tile somebody
thought about. It is that the inventory is a good map of what the studio has
CONSIDERED and an incomplete map of what it HAS, and the difference is invisible
from inside it. Three of the brief's ten known-already gaps were reported as
gaps for this reason.

WHAT IS NOT CLAIMED, and it bounds all five rows above: I established the code
and the call sites. I did NOT establish that any of it has run in front of a
person or that any gate measures it. `StainsNoticed` and `WorstStainCost` are
counters on `ViolenceHost` and I found no verdict key emitting them. Built is
not running.

### 5.2 The project already owns the idiom D12 asks for

A grep for a public `Why(` method across `ledger/Assets/Scripts/Core/*.cs`
returns exactly two, `Core/Homicide.cs:351 PressureWhy` and
`Core/YardDepth.cs:330 ProbeWhy`, and both are instruments that print which term
of a number moved. D12 asks for precisely that, pointed at the player. Disco
Elysium is the evidence that it works at a far larger scale of information. Game
4, section 2.

### 5.3 Pillar 4 has an empirical case now, and it is not flattering

Shadows of Doubt generated its city, cases and documents, and reviewers
describe identical text in every location and an investigation that collapses to
a rote procedure. Pillar 4 ("No procedural filler without an authoring pass and
verification") was arrived at on argument; this is what the other choice looks
like from outside. Our tile "the cast" already records that the population
generator "supplies names, not people". Game 5, section 3.

## 6. Research topics the audit revealed that are not in the queue

Three new, two extensions to topics already queued. Named as findings, not
filed.

**NEW 1. Holding a large branching script without losing editorial control.**
ZA/UM wrote Disco Elysium's roughly one-million-word script in Articy, the
industry-standard tool for exactly this, and it slowed and then froze under the
volume, with the studio describing text so voluminous that "control over the
material began to be lost". LEDGER intends more authored dialogue than it has
any tooling for: the tile "dialogue banks" is partial and the no-repetition
blind test is phase 3's gate. Nothing in the 25 covers authoring tooling.
Topic 20 covers voice licensing, topic 1 covers speech architecture, topic 15
covers authored stories surviving emergence. None of them asks what holds the
words.

**NEW 2. Whether the simulation should run live at all.**
Shadows of Doubt pre-computes each day in 10 to 15 seconds rather than
simulating it in real time, and then scales AI update rate by proximity so 95
percent of citizens cost almost nothing. That is an architectural choice, not a
budget one, and it was made by the only other team to try this. Topics 2 and 17
are both about what things cost per frame; neither asks whether the town should
be on the frame at all. This is adjacent to them and is not either of them.
CAVEAT ATTACHED: game 5 could not establish whether their pre-computed day is a
full simulation or a schedule resolution, and that distinction decides how much
the finding is worth, so this topic starts by reading the devblog.

**NEW 3. How a game teaches a SOCIAL system in thirty minutes.**
Meridian Test condition 1 gives us thirty minutes before a player who loves KCD2
or GTA decides. KCD2's admired answer is to explain almost nothing, which it can
afford because it has a hundred hours to recover; game 1 recommends OUT on that
basis. Queue topic 12 covers how stealth games teach detection without
tutorials, and topic 7 covers how emergent-story games make stories legible.
Neither covers teaching a player, fast, that they are being watched and
remembered, which is the specific thing our first thirty minutes has to do.

**EXTENSION to topic 6 (British policing 1988 to 1992).** Topic 6 as written
asks what a person experiences: arrest, custody, charge, the magistrates. Game 5
raises the other half, which is what a SCENE yields. Around 1990 fingerprints are
the one mature forensic tool, DNA profiling is brand new rather than routine,
CCTV is rare by canon, and there are no mobile records. The list of what a
scene-of-crime officer could actually collect in Meridian in 1990 is a short,
useful, period-specific list, and it is the research behind recommendation 20.

**EXTENSION to topic 11 (social network structure in small towns).** Question 1
in section 4 (does the town have an opinion) needs an answer that is not a
number. Topic 11 is about how schedule intersections should be non-uniform;
the adjacent question is how group-level standing can be EXPRESSED and COMPUTED
from individual records without ever storing a score, which is what D11 would
require. Same literature, one more question.

## 7. What this audit could not establish, in total

1. **D24 does not exist in this checkout.** The D-numbered spine runs D1 to D18;
   a grep for `D24` and for the three phrases the brief quotes returns zero hits
   across `ledger-v2/`, `production/`, `game-design/` and `canon.md`. All 188
   verdicts are argued against the brief's own formulation of it, cited as such.
   If the record exists elsewhere it should be pointed at; if it has never been
   written, a principle this audit leans on is unwritten.
2. **No page was read in full.** Outbound HTTPS to research hosts is refused by
   the egress proxy: `en.wikipedia.org`, `kingdomcomedeliverance-archive.fandom.com`,
   `www.gamepressure.com`, `www.gamedeveloper.com` and `colepowered.com` were
   each fetched this session and each answered `EGRESS_BLOCKED`. WebSearch
   works. So every external citation in all five deliveries is the search
   channel's SUMMARY of a named page. Every quantity relayed (KCD2's carry
   weight and perk count, Hitman's crowd figures, RDR2's species counts, Disco
   Elysium's word count and recording times, Shadows of Doubt's 10 to 15 seconds
   and 95 percent) is a direction, not a measurement.
3. **The two most load-bearing primary sources are blocked.** Game Developer's
   "The AI of Hitman (2016)" and ColePowered's devblog series. Games 2 and 5
   both say so at the point where they depend on them.
4. **Two GDC talks are paywalled**, which is where Hitman's level-design and
   crowd claims come from.
5. **One source discrepancy is unresolved**: Disco Elysium's narrator recorded
   350,000 WORDS (PC Gamer) or 350,000 LINES (PSU). More than an order of
   magnitude apart, neither page reachable.
6. **Search returned `Web search error: unavailable` twice** and answered from
   the model's own memory instead. Both answers were discarded and the searches
   re-run. Nothing in any delivery rests on them, and this is recorded because
   the failure mode is silent: an unavailable search that answers anyway is
   indistinguishable from a successful one unless the error line is read.
7. **The 188 is not a census.** It is what one session's search channel surfaced
   per game. Combat was not enumerated for any of the five, animation was not
   enumerated for RDR2, and each delivery's own section names what else it left.
8. **Built is not running**, for every claim in section 5.1.

## 8. One thing the audit did not find, stated because a null result needs saying

I looked, in all five mappings, for a system that would threaten a pillar or
contradict a decision record, and found none. The fifteen RULED OUT entries are
all struck by D11, D17 or D18, cleanly and without argument, and nothing in 188
systems suggested that any of those three records is wrong. The nearest thing to
a challenge is question 1 in section 4, where two games independently reached a
group-level standing that D11's reasoning addresses only partly.

DENOMINATOR: 188 systems examined, 0 found to contradict a pillar or a record,
15 struck by one. That is a clean result with its count attached, and it is
evidence that the framework is settled rather than evidence that I looked
hard enough.
