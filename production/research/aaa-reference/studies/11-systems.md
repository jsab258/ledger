# Study 11: Systems (28 October 2026)

How Kingdom Come: Deliverance II and Mafia: The Old Country run heat and police, money, saves, missions, and time and weather; read from their data and Warhorse's public modding wiki, not their code. Our own words and numbers; raw notes on F:/LedgerTools/aaa-study/kcd2/study-11-15/s11/ and F:/LedgerTools/aaa-study/mafia/study-11-15/, read 28 October 2026. Study 1's crime memory is not repeated. Kingdom Come II stores money in tenths of a groschen; figures here are in groschen (gr). Tags: **M** measured, **R** read, **I** inferred, **N** a name only.

**The short answer.** Kingdom Come II has no wanted meter: heat is each witness's information (Study 1), anger that a faction feels 12 hours late and sheds in about a day and a half (I), and nervousness that passes in about three hours (I). Money runs out at the counter; shops restock weekly. It saves at quest steps and after sleep; quests are state machines, half of which can fail; a day lasts about 96 minutes. Mafia is the staged opposite: no heat or fines, a shop of unlocks, checkpoint saves, a time of day set per checkpoint. LEDGER is built the Kingdom Come way already; the lessons are its delays, save points, quest states and weather draw.

## The numbers

| | Kingdom Come II | Mafia |
|---|---|---|
| Heat | no meter; anger 0 to 1 per person and faction (seen theft +0.1 to 0.2, killing +0.8); a faction's change acts 12 h late, clears in about 34.7 h (R, I) | none (M) |
| Police posture | all arm at anger 0.67; extra guards at 0.8 (R) | 11 carabinieri class names (M, N) |
| Merchant's cash | 35 to 1,500 gr (R) | not in the data read |
| Restock | 7 days, all 168 shops (M) | none: items unlock by progress (R) |
| Prices | food median 6.5 gr; clothing and armour 120 (p90 1,662); helmets 2,059 (M) | 199 unlocks; priced medians: outfits 500, weapons 1,000, vehicles 1,500, horses 200; top 8,000 (M) |
| Autosaves | 686 save points in 126 of 135 quests, median 4 a quest; after 1 h of sleep (M, R) | at checkpoints; 15 main checkpoint tables (M, N) |
| A bought save | an item that saves on use, 25 to 55 gr (R); whether it is the only field save, unverified (I) | none found |
| Quests | 135; median 11 objectives (2 to 52); 52% can fail; 1,061 timers, world-time median 4 h, longest 336 h (M) | failure restarts the checkpoint after a 3 s screen (R) |
| Clock | 15 × real time: a day in 96 min (R, I); night 21:18 to 04:42, 2.6 h fade (R) | a preset per checkpoint; 4 phases (R) |
| Weather | 31 profiles a level, 15 weighted; rain-capable in about 35% of weighted draws, about 25% weighted by rain chance (M, I) | a block inside each preset (R) |

## Heat and police

- **Kingdom Come II, three stand-ins for a wanted level.** The witness's information, kept 1 to 7 days by crime (Study 1). Anger: 119 event rows (51 animal reactions, 31 hostile-faction copies, 37 others, two of which lower it) set a person's anger (M): a lock heard picked 0.15 (0.4 among bandits), a gunshot nearby 0.9 (R); that they feed the faction's anger is I. A faction's change acts 12 h late, then falls evenly to nothing in 34.7 h if the rate is per world second (R, I). Nervousness, one person's alarm, gone in 2.8 h on the same reading (R, I).
- **Guards follow anger:** low under 0.3, middle to 0.6, high to 0.9, alerted above; extra guards come at most every 300 s (R).
- **Reputation, beyond Study 1:** 203 change rows, 166 losses and 30 gains (M); a charge talked away still costs 0.18 (0.25 if the talk fails) (R, Study 15's notes). No fading parameter among the values read (code defaults not checked) (M). Repair by quests, reconciliation (+1.2) or a paid indulgence of 1 to 1,000 gr (R; groschen I).
- **Mafia** has no heat, wanted level or fine, in names or data (M; Study 1). Its one apprehend role serves trespass (Study 15).

## Money

- **Kingdom Come II, in:** quest rewards: 191 reward points in quest data, about 16,665 gr, 171 of them (16,100 gr) in the 74 quests that carry one (M), from 11 fixed sums of 5 to 1,000 gr (R; unit I); selling; loot (14 presets, 2 to 500 gr) (R); pickpocketing (Study 15).
- **Out:** goods; repairs at 0.45 of value (0.6 in hardcore); a bed at 5 gr a night or 50 gr to keep one (R); fines, median 75 gr (M); lessons, the save item, indulgences.
- **At the counter:** 168 shops, chiefly innkeepers 21, smiths 15, merchants 10, armourers 8; 58 in Kutná Hora (M). A merchant cannot pay more than he holds, at most about 212 gr in the median shop (R; M, I). Buy and sell multipliers have medians 0.8 and 0.5 over 2,840 rows; which is the player's side is not stated (M, I). Worn goods sell for less, by condition (R).
- **Hours come from people and doors,** not the shop: townsfolk work 08 to 20, villagers 07 to 19, village services 08:00 to 22:30, town services 09:00 to 01:00 (R); 1,053 of 1,249 placed doors stay unlocked 05:00 to 21:00 (M).
- **Mafia:** one currency (N); 199 shop items in five kinds, 98 free (M). 105 unlock at a story chapter, 41 in free ride, 17 by challenges; 27 edition items have no unlock point (M). Money comes from loot and opened safes (R, N). No fines, rent or upkeep (M).

## Saves and restarts

- **Kingdom Come II saves when an objective changes:** 686 save points, 33 marked important, 607 tied to an objective, only 7 on entering an area (M); also after an hour's sleep (R). 31 points block saving: 23 in scripted scenes, 6 in combat, 2 in minigames (M).
- UI text exists for manual slots, a quick save, save-and-quit and an exit save (R); which ones normal play offers is not in data. The bought item (four grades, 25 to 55 gr) saves on use (R).
- Of the quest graph, only state nodes are saved; effects are rebuilt from them (R, wiki KM-A-30). The rest of the save was not read (N).
- 62 kinds of game over (11 general, 51 belonging to quests), with one action, accept (M, R); what follows is not in data.
- **Mafia saves to nine slots in five files (R):** the current checkpoint and each plotline's step; the player (health, weapons, coins, outfit, last car and horse); safes opened, notes, tutorials, purchases; free ride, collectibles, settings. A failure shows a 3 s screen and returns to the checkpoint; leaving a mission's bounds fails it after 15 s (R).

## Missions as states

- **Kingdom Come II builds each quest as a graph** of definitions, states and effects (R). Quest states: none, active, done, failed. Objective states: none, started, updated, completed, cancelled (R).
- 135 quests with objectives: 45 micro, 43 side, 32 main or untyped, 15 activities; objectives median 11 (micro 4, side 16, main 17.5) (M). 70 (52%) can fail; 119 can cancel an objective (M); whether a failed quest's world carries on is I.
- 1,061 timers, 338 on world time: median 4 h, longest 336 h (14 days). Only one was found failing a quest directly, a lower bound (M).
- **Mafia nests plotline, missions, checkpoints and objectives (R):** ten objective kinds; levels main, sub, optional; a stealth rule of none, mandatory, or a "blood gate" (I: shedding blood fails it). 12 folders carry 65 custom mission scripts (M).

## Time of day and weather

- **Kingdom Come II's clock** runs at 15 times real time (R): a day in 96 minutes, by a developer's comment beside the setting (I).
- **Weather:** 15 of 31 profiles a level carry weights (sum 5.1) and rain chances of 0.3 to 1.0 (M). If the weights are draw weights, rain-capable profiles take about 35% of draws, and about 25% weighted by rain chance (M, I). Routines split by it (Study 1: 1,399 sun-only, 890 rain-only links).
- **The player gets dirty** (100% after 35 km at full speed or about 7.9 h of work; people smell it from 0.8) (R); rain washing or wetting him was not found in data. Sleep needs at least 1 h and 30% health; 86 kinds of time skip (R, M).
- **Mafia** has no running weather (M). Each checkpoint names a time-of-day preset and a transition (R); a preset sets clock, light, exposure, sky and a weather block (lightning, cloud, wind) together (R); 103 presets by name (M, N).

## For LEDGER

1. **Propose: a delay before the police act, read from the talk.** LEDGER's heat is the street's talk (fading on a 96 h half-life, 144 h while Ellis is in town: Gossip, EllisSetup), and Ellis comes for talk from day 4 once three people pass it round (PoliceFile Loudness). Kingdom Come II's 12 h delay and two posture steps suggest a constable's beat on Quay Street at a lower loudness, before Ellis. A new system: under the 29 September ruling it waits for a place in PLAN.md. **Ignore** faction anger as a number: the town has no opinion, only people (D34).
2. **Adopt: money that runs out at the counter and restocks weekly.** Already built (Purses; Economy's weekly suppliers); Kingdom Come II confirms the shape. **Adapt** hours from people and doors, Meridian's from LEDGER's own 1990 research (owed). Serves D24 (trade must not look broken) and the 23 September ruling (buying, selling).
3. **Adopt: a save at every job step, held during a fight.** LEDGER saves after each committed decision (GameController) and keeps state only (SaveCodec), as Kingdom Come II does for quests. For the Unreal port: save on every change of a job's state; in a fight or scripted moment the save waits, never refused. Serves phase 3's exit (kept after restart). **Ignore** the bought save and the checkpoint restart: reloading is never stopped and the game says what is permanent (D35, D58); an arrest costs hours, not the game (Custody).
4. **Adopt for jobs: four job states and five step states,** limits on the town's clock (median 4 h), cancelled steps. To Study 16's job template (jobs, no waypoints: 23 September).
5. **Adopt: weather as weighted profiles feeding routines,** for phase 3's weather proof: one saved wetness value, drizzle and rain profiles changing who is out; no sunshine in the friends' build. **Ignore** Mafia's weather set per checkpoint.
6. **Adapt Mafia's presets for light:** clock, light, exposure and sky in one preset. LEDGER's day and night (7 October: four or five states later, no moving sun) can be two presets, then four.
7. **Measure the clock against the thirty minutes.** The C# game runs a day in 12 real minutes (GameController), Kingdom Come II in 96: phase 3's thirty minutes are two and a half days in LEDGER, under eight hours there. Playing them answers it; noted, not decided.

## Coverage map

To tick in REFERENCE.md: economy and shops (both games); time and needs (time, sleep and weather; food not studied); saving (both games); NPC mood and anger (Kingdom Come II's rates); reputation (Mafia: none); missions (states and counts, for Study 16). Open: the engines' code.

## Open blind spots

- **Kingdom Come II's code:** the barter formula, cash refills, saving rules in play, the decay rates' time unit, weather choice and rain length. **Its data:** which multiplier is the player's; lesson, horse, barber and bath prices.
- **Mafia:** loot sums, checkpoint counts and presets, names only: not exported, as the F: drive filled on 28 October.
- **Shown only in play:** what follows a game over; Mafia's shop in use. No recordings (25 October).

## Sources (read 28 October 2026)

- **Kingdom Come II's files:** Libs tables (money_change, reputation_change, angriness, shop, item, game_over, game_mode, skiptime, ScriptParams), quest files, level weather profiles and doors; Warhorse's wiki (warhorse.youtrack.cloud) through its public interface, in full: KM-A-12, 20, 21, 27, 30, 32 to 34, 84, 89, 90.
- **Mafia's files:** the published mappings file's type names; the exported Economy folder; DefaultGame.ini; the package index.
- **LEDGER:** Core (Gossip, PoliceFile, Custody, Purses, Economy, SaveCodec); Game/GameController; RULINGS.md.

## Review

A fresh reviewer (28 October) checked about 60 numbers, 26 re-measured: pass with fixes, all applied (the quest breakdown, the reward base, anger as a person's value, decay times inferred, the rain share, what a save is known to keep, the bought save, Mafia's time per checkpoint, unlock sources, cash as an upper bound, tags; item 1 rebased on Loudness and made a proposal). Cost, from the clock: with Study 15, 10:35 to 11:37 (reading and two helpers to 11:17, synthesis, two reviews, fixes).
