# Rumour reach: why a realistic witness under-fills the circle, and whether the town visibly knows within thirty minutes

Decision 2, ruled by Jafar on 23 September. No constant was changed. One read-only measurement mode was added to the Soak tool, and one throwaway program was written in the scratchpad.

---

## Plain English

**Thirty minutes of play is 60 game hours**, about two and a half game days. The game clock runs at 2 game minutes for every real second. Only the pause menu stops it.

### 1. Why a realistic witness doesn't fill the circle

- **A story can be retold only once.** Each retelling multiplies the story's certainty by the friendship's strength and by 0.8, and anything under 0.2 is dropped. A witness who is half sure (0.5) can pass it only to friends of 0.6 or stronger. A friend of exactly 0.5 gets it only in the first hour. For a second retelling, the two friendships multiplied together would need to reach about 0.52 to 0.63. With friendships no stronger than 0.8, fewer than 3 in 100 two-step chains manage it. So the "circle", meaning friends and friends-of-friends (about 20 people), can't be reached. The most a realistic witness can reach is the stronger half of their own friends.
- **The story also fades.** Every rumour loses half its certainty every 96 game hours, which is two hours of play. That gives the witness a limited window with each friend: about a day for a 0.6 friend and two to three days for a 0.8 friend.
- **The soak's 5 to 10 comes from a well-connected witness, told 125 times.** The soak's witness, Rocco, has 5 to 8 friends. A typical person in that town has 3. The soak also has him see something new on a quarter of all days for 500 days. Picked at random, a realistic witness in the same town reaches **1 to 2.5 people on average** and 5 at best.
- **In the real street it is fewer still, because friends rarely meet.** In the actual game, two friends can only talk when they stand within 6 metres of each other. Going by the characters' daily routines, **55 of the 80 friendships between people who exist in the game never meet at all** (29 of 80 if walking between places is counted). The 700 crowd residents are not connected to the named characters at all, and their own friendships meet in 0.14% of hours. The result for a realistic witness in the real street: **Rocco reaches 3 to 4 people. The average witness among the 40 named characters reaches 0.5 to 1.5, and most reach nobody.**
- **What gives out first:** the certainty arithmetic sets the ceiling everywhere, so no second retelling ever happens. In the real street, the routines then cut even that ceiling by about two thirds. Time is not the limit. Whatever is going to happen has happened within about one game day, which is about 12 real minutes.

### 2. Is that too few for the town to visibly know within thirty minutes?

- **The number of people who know is not what's missing. How faintly they know is.** Someone who hears it from a half-sure witness holds it at 0.20 to 0.38 certainty. A character's reaction to the player depends on their suspicion and their certainty. With no suspicion, they only give you a lingering look at 0.58, and only say something to you at 0.93. The most a hearer of a realistic witness can do is glance at you from within 6 metres while standing still. Ordinary passers-by who see you already glance at you the same way. Nobody makes a remark, refuses you, or greets you differently, and their suspicion barely moves (by 0.02 to 0.05).
- **Who you would meet:** in the Unity build, Rocco's listeners (Lena, Sam, Joey, sometimes Noor) spend their days around the bar. A player who stays near the bar would meet most of them in thirty minutes, and would see almost nothing from them. The two things that could show it, overhearing the actual retelling or asking one of them about it, depend on luck or on the player already knowing whom to ask. Each retelling happens in a single 6-minute round, which is 3 real seconds.
- **What a player can see within thirty minutes comes from "heat", not from reach.** Heat needs just one daytime person holding the story. It changes the on-screen word for the street to "murmuring" or "uneasy". Every character is told the street is murmuring when you talk to them. It cuts the next morning's takings by about a quarter to two fifths. It also gives roughly 1 in 10 newly-appeared passers-by a vague rumour, which again only earns a glance.
- **So: yes, it is too few to see, but raising the count would not fix that.** Twenty people knowing at 0.2 to 0.38 would still show nothing more than twenty glances.
- **The single thing that would change the answer most** is how certainty turns into behaviour: the reaction ladder, which counts the rumour at only 0.45 weight. If having heard something about you showed at the certainty hearers actually hold, the 3 to 10 people who know would each be a visible reaction, and a player near the bar would meet most of them within thirty minutes. The next two, in order: how often friends' routines actually bring them together, and friendship strength (the steepest dial for reach, but it does not create anything visible).

---

## Evidence

### A. The rules, from the code

- The share rule. `Gossip.cs:141-142` `HopDecay = 0.8`, `MinConfidenceToShare = 0.2`. `Gossip.cs:402` refuses a speaker holding under 0.2 unless indelible. `Gossip.cs:410-411` computes `passed = r.Confidence * tie * HopDecay`, refused below 0.2 (a body is exempt).
- One hop per round. `Gossip.cs:387` snapshot.
- Retelling. `Gossip.cs:389-465`: every holder tells every tied friend they are `together` with, EVERY round, with no once-only limit. The only guard is `Gossip.cs:420-422`: skip a listener who already holds that version at least as strongly. Copies are compared by max and never added, so hearing it twice does not reinforce it.
- Repeated sightings. `Gossip.cs:291-321`: the same fact seen again only raises certainty to the max. The game's facts carry the day in the predicate (`night_job_d{day}`, `racket_*_d{day}`, `street_trouble_d{day}`), so a new day's sighting is a new story with its own spread. Distinct stories corroborate only in heat (`Gossip.cs:564-594`, a noisy-or per holder). The stance reads only the single strongest rumour (`GossipDirector.cs:309-315`).
- Fading. `Gossip.cs:926-947`: `Age` halves every non-indelible rumour every `RumorHalfLifeHours = 96` game hours and drops it under 0.03. The game calls it once per game hour (`GameController.cs:1071-1074`). Memory events are never deleted: the memory stays even after the rumour is gone.
- Asking outright. `CompareNotes` (`Gossip.cs:478`, `GossipDirector.cs:623-644`) runs only for NPCs at Suspicious or above (suspicion 0.5 or more, `Suspicion.cs:193-197`). A realistic rumour cannot get anyone there.

### B. The clock

- `GameController.cs:12` `MinutesPerRealSecond = 2f` ("1 game day = 12 real minutes"). `GameController.cs:990-995` advances it per frame.
- Only the pause menu stops it (`DialogueUI.cs:93`, `Time.timeScale = 0`); dialogue does not. The Fall skips 3 days (`GameController.cs:1856`). Sim mode runs at 20 (`SimDirector.cs:65`) and is not play.
- **30 real minutes = 3600 game minutes = 60 game hours = 2.5 game days.**

### C. The real game's meeting rule

- `GossipDirector.cs:29` has a gossip round every 6 GAME minutes (10 a game hour, 3 real seconds each). `GossipDirector.cs:34` sets `TalkRange = 6f`. `GossipDirector.cs:660-666` defines `Together` as both positions within 6 m.
- A crowd member's position is either their body or `WhereIs` (`PopulationHost.cs:934-948`, `954-960`).
- The soak instead tosses a 10% coin per tied pair per hour, with one round an hour (`Soak/Program.cs:841`).
- The ties are wired in two places:
  - The cast graph is `GossipDirector.cs:125-167`: authored ties plus the tier-2 batch json.
  - Crowd residents are linked only to other crowd residents, at index +137/+274/+411, with weights 0.4/0.5/0.6 (`PopulationHost.cs:1029-1042`), and only when those residents are already in the mill.
  - **Nothing links a crowd resident to a named character**: `.Link(` appears only in those two files.

### D. Hop arithmetic (from `--reach-clock`, section 1; town seed 1, and seeds 2-3 agree)

The authored tie bag is 0.3 0.4 0.4 0.5 0.5 0.5 0.6 0.6 0.6 0.7 0.8 (mean 0.54). Everyone above the seven authored residents draws from it.

| first sight | hop 1 needs tie ≥ | arrives at (tie .8/.7/.6/.5) | hop 2 needs tie product ≥ | 2-step paths that clear it (seed 1/2/3) |
|---|---|---|---|---|
| 0.50 | 0.500 (0.5 only before the first hourly fade) | .32/.28/.24/.20 | 0.625 (only 0.8×0.8) | 6/968, 7/979, 15/985 |
| 0.55 | 0.455 | .35/.31/.26/.22 | 0.568 (only 0.8×0.8) | same |
| 0.60 | 0.417 | .38/.34/.29/.24 | 0.521 (0.8×0.7 or better) | 25/968, 30/979, 27/985 |
| 1.00 | 0.250 | .64/.56/.48/.40 | 0.313 | 277/968, 354/979, 309/985 |

How long the witness's own copy can still pass to a friend of each tie strength (Age included), seed 1 Rocco:

- at 0.5: tie 0.8 for 65 h, 0.7 for 47 h, 0.6 for 25 h, 0.5 for 0 h, 0.4 refused
- at 0.6: 90 / 72 / 51 / 25 h (0.4 refused)

### E. The time curve in the soak's town (`--reach-clock`, 200 residents, 200 trials a row, seeds 1/2/3)

People other than the witness who have heard, after N game hours. **60 h is thirty minutes of play.**

Witness Rocco (5, 8 and 5 friends in the three towns; 19/35/19 within two ties):

| first sight, meetings | 6 h | 12 h | 24 h | **60 h** | 168 h | ceiling (always together) |
|---|---|---|---|---|---|---|
| 0.50, soak coin | 2.4/1.9/2.4 | 3.5/2.9/3.5 | 4.6/3.7/4.5 | **4.8/3.9/4.9** | same | 5/7/5 |
| 0.50, 6-min rounds, pair meets 10% of rounds | 5.0/5.9/5.0 | 5.0/5.9/5.0 | 5.0/5.9/5.0 | **5.0/5.9/5.0** | same | |
| 0.50, 6-min rounds, pair shares 1 h a day | 1.5/1.3/1.5 | 2.9/2.3/2.7 | 5.0/4.1/5.0 | **5.0/4.1/5.0** | same | |
| 0.60, soak coin | 2.3/3.5/2.4 | 3.5/5.5/3.8 | 4.6/6.9/4.9 | **5.0/7.3/5.3** | same | 5/9/6 |
| 1.00, soak coin | 3.8/5.0/3.6 | 6.8/9.9/6.5 | 9.5/15.1/9.9 | **10.1/17.6/11.4** | same | 14/23/15 |

A random resident as witness (mean; p10-p90 at 60 h):

| first sight | soak coin at 60 h | always together (ceiling) |
|---|---|---|
| 0.50 | 1.2 / 1.5 / 1.3 (0-3) | 2.3 / 2.4 / 2.5 (0-5) |
| 0.55 | 1.9 / 2.3 / 2.1 (0-4) | 2.2 / 2.4 / 2.4 |
| 0.60 | 2.2 / 2.3 / 2.3 (0-5) | 2.4 / 2.6 / 2.5 |
| 1.00 | 4.9 / 5.6 / 5.0 (1-10) | 6.1 / 6.9 / 6.3 |

What the tables show:

- **Every row's 60 h figure equals its 168 h figure.** Thirty minutes is enough time for everything that will ever happen.
- The deepest retelling at 0.5-0.6 is 1, and occasionally 2 at 0.6 through a 0.8×0.7 path.
- **Confirmed against the soak's own series** (seed 1, `reach-series-seed1.txt`):
  - first-sight 0.50 gives `remembered=6/200 maxHop=1 hops=811,0,0,0,0`
  - first-sight 0.60 gives `6/200 maxHop=1`
  - that 6 is Rocco plus the 5 friends of tie 0.6 or more that the arithmetic above predicts. The clock's ceilings (5/7/5 at 0.5, 5/9/6 at 0.6, plus Rocco) are the "5 to 10".

### F. The real cast street (throwaway `castreach`, scratchpad)

Routines transcribed from `GameController.cs:733-874`, ties from `GossipDirector.cs:125-167` plus `StreamingAssets/tier2-batch-1.json` (live ids per `Tier2Batch.cs:18-25`). Places come from Core `HookMap`, and positions are each walker's routine target (`NpcWalker.cs:727-735`). Together means within 6 m, in 6-min rounds, with the hourly `Age`.

The graph:

- 40 people are in the mill. 98 ties are written, and 80 of those are between people who exist.
- Mean live tie is 0.44. Only 12 ties are 0.6 or stronger, and only 4 are 0.7 or stronger (Rocco–Sam 0.8; Rocco–Lena, Noor–Ada, Emil–Vesna 0.7).

Meetings:

- **55/80 live ties are never within 6 m** at their routine targets. The mean is 2.1 h/day and the median 0 h/day.
- With straight-line walking between targets (NpcWalker's 1.4 m/s real, which is 0.7 m per game minute), 29/80 never meet. With a 10 m radius instead of 6 m, 46/80 never meet.

Rocco's friends and time together each day:

| Sam 0.8 | Lena 0.7 | Joey 0.6 | Noor 0.5 | Dusan 0.5 | Franjo 0.4 | 7 others (0.3-0.4) |
|---|---|---|---|---|---|---|
| 10 h | 7 h | 5 h | 3.5 h | 0 h | 2 h | 0 h |

Results. The figures are means over the 24 possible hours of the sighting; each cell reads standing / walking.

| first sight | Rocco at 60 h (ceiling) | all 40 as witness, mean at 60 h | median | witnesses reaching nobody |
|---|---|---|---|---|
| 0.50 | 3.2 / 3.2 (5) | 0.52 / 0.76 | 0 / 0 | 29/40 / 27/40 |
| 0.55 | 3.7 / 3.8 (5) | 0.73 / 1.24 | 0 / 0.6 | 27/40 / 16/40 |
| 0.60 | 4.0 / 4.0 (5) | 0.84 / 1.48 | 0 / 1 | 26/40 / 16/40 |
| 1.00 | 7.0 / 13.8 (28) | 1.58 / 3.33 | 0 / 2 | 24/40 / 11/40 |

- Rocco's curve at 0.6 (standing): 1.2 people at 1 h, 2.0 at 6 h, 3.0 at 12 h, 4.0 at 24 h, and flat after that.
- **Crowd:** of the 2,100 crowd ties (700 residents, seed 20260726, the `WhereIs` model, 7 days), 63 are ever within 6 m. That is 0.14% of pair-hours.
- **Caveats:** detours, confab walks and exact street paths are not modelled. Suppliers and Ellis have no ties.

### G. What a player can see (all reads; nothing changed)

**Stance.** `StreetVoice.cs:89-110` works out a pressure score:

- pressure = 0.55 × suspicion + 0.45 × strongest rumour confidence
- minus 0.7 × (loyalty − 0.5) for loyal NPCs
- minus 0.12 with the coat on

The rungs, and the rumour confidence each needs when suspicion is zero:

| rung | pressure | confidence needed |
|---|---|---|
| Notices | 0.12 | 0.267 |
| Watches | 0.26 | 0.578 |
| Comments (a bark, `GossipDirector.cs:321-337`) | 0.42 | 0.933 |
| Avoids | 0.58 | |
| Refuses | 0.72 | |
| Confronts | 0.86 | |

- The only thing Notices does is a head turn when the player is within 6 m and the NPC is standing still (`StreetVoice.cs:115-121`, `NpcWalker.cs:2079-2087`). The code OR-s that with the ordinary perception look (`NpcWalker.cs:2089-2098`), so it is the same look any stranger who sees you gives.
- A hearer of a 0.5-0.6 witness holds 0.20-0.384. Those under 0.267 are Indifferent; the rest reach Notices at most.
- Rocco himself at 0.6 has pressure 0.27, minus 0.07 for his loyalty of 0.6, which gives 0.20: Notices.

**Suspicion from hearing.**

- A daytime listener hearing a night-life rumour gains 0.12 × passed, which is +0.02 to +0.05 (`Gossip.cs:449-453`).
- A rumour that contradicts something the player told that same listener adds 0.35 × passed, which is +0.07 to +0.13 (`Gossip.cs:439-446`).
- Both stay under Uneasy (0.25), so the prompt's descriptor stays "trusting" (`Suspicion.cs:220-233`). The cast's passing greeting needs Uneasy (`GameController.cs:1989-1992`), so it does not change either.

**Recognition.** `GossipDirector.cs:68-76` and `Acquaintance.cs:46`: having heard of the player gives familiarity 0.20, which is below the 0.35 needed to name him.

**Dialogue.** The hearer's memory "I heard from X that …" is saved with importance 0.2-0.31 (`Gossip.cs:431-433`). It reaches the model only if it makes the top 8 on recency, importance and word overlap with what the player says (`MemoryRetrieval.cs:41-69`, `ConversationEngine.cs:57-63`).

**Overhearing.** The spoken exchange, the lead and the on-screen line fire only in the single round of the transfer, and only with the player within 6 m of both people (`GossipDirector.cs:567-616`). The staged conversation needs both people to be cast walkers (`GossipDirector.cs:410-468`).

**Heat.** `Gossip.cs:564-594`: heat is the best single daytime holder. It drives four things:

- the on-screen status word: quiet under 0.2, murmuring under 0.45, uneasy under 0.7 (`GameController.cs:285-286`, `DialogueUI.cs:1374-1379`)
- every cast prompt's line "Talk about the new owner around the street is …" (`GameController.cs:908`)
- takings of 220 × (1 − 0.85 × heat) at the daily close (`Campaign.cs:333`)
- how busy the ambient chatter is (`StreetVoice.cs:677-688`)

**Ambient reach for the crowd.** Newly-appeared crowd residents get a 0.3 rumour at 0.8 × heat × (1 − 0.72^days) (`Population.cs:609-627`, `PopulationHost.cs:196-201`, `1012-1026`). For a daytime witness at 0.5, that is about 9% on day 1 and about 14% on day 2. Their pressure is 0.135, which is Notices.

### H. Commands run

```
dotnet run -c Release --project ledger/Soak -- --reach-series --residents 200 --days 500 --seed 1   # 1m51s -> reach-series-seed1.txt
dotnet ledger/Soak/bin/Release/net8.0/Soak.dll --reach-clock --residents 200 --seed {1,2,3} --trials 200   # ~6 min each -> reach-clock-seed{1,2,3}.txt
dotnet run -c Release   (scratchpad/castreach)            -> castreach-output.txt
dotnet run -c Release -- --walk --no-crowd / --radius 10 --no-crowd   -> castreach-sensitivity.txt
dotnet ledger/Soak/bin/Release/net8.0/Soak.dll --days 5   # default mode still: "soak ok - all 9 checks passed"
```

### I. Files

- **Changed in the repository:** `ledger/Soak/Program.cs`, +204 lines. This adds the `--reach-clock` mode: one sighting, a clock, the meeting models as a dimension, read-only. The default mode is untouched. Not committed.
- **Scratchpad:** this file, `reach-series-seed1.txt`, `reach-clock-seed{1,2,3}.txt`, `castreach/` (throwaway program), `castreach-output.txt`, `castreach-sensitivity.txt`.
