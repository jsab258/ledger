# Measuring the emergent side of the story

24 November 2026. How to tell, before any player sits down, whether the town makes stories on its own: memorable moments counted per evening in simulated playthroughs by the checkers, against a target taken from the players' stories study. Built on that study's standards STORY-01 to STORY-08 (production/research/lane/aaa-studies/PLAYERS-STORIES.md, section 3; blueprint row 7.6), which this file keeps and extends to the story frame (STORY-FRAME-2026-11-26.md).

## 1. What counts as a moment

A full moment passes the study's four tests, each with evidence in the log:

1. The player chose: two or more options were open; the one taken is logged. The Core logs every choice point with the options it allowed (a decision line, a job's ways in, the verbs the slots allowed on a person, pay, defy or counter), so code can prove this test.
2. It could have gone another way: the deterministic Core snapshots at every logged choice point. From that snapshot the checker runs two scripted replays to the same horizon, one taking the option the tester took (the control) and one taking another option, with the tester's later inputs replaced by the same fixed idle script in both. The test passes when the two differ in at least one of: a fact held by a named person about Tom, a beat played, a ladder, dial or Ellis stage, a person's attitude to Tom. The control must reproduce the original comeback; if it does not, the moment is a near miss.
3. A named person was there: by id, a person with a name the player can learn (principals, regulars, crew, rivals' men, fare people). A crowd extra who caught a slot and became kept (RT2-10) counts only once his name has reached Tom (said to him, or in the Ledger).
4. It came back later: a later reaction is linked to the moment by the gossip chain print (2.4.4), within the evening or a later one, and the reaction reached Tom: said to him, done to him or in his sight or hearing, or shown by its sign (a refusal, a cooler door, Ellis's stage sign, a Ledger line). A telling he never meets does not count.

A moment missing one test is logged as a near miss. Near misses are counted too: many near misses with few full moments means the town notices but does not return.

## 2. The kinds counted

Each full moment carries every kind that applies (a moment can be K4 and K7), plus a mark field (STORY-01) that is filled when a witness connected Tom through a thing. Shares in section 3 are counted over moments, not tags:

| Kind | What it is | Frame source |
|---|---|---|
| K1 Said to his face | a named person says Tom's own deed back to him, accurately or in a told version | section 7, "said to his face" |
| K2 Witness | a person who saw or heard a deed acts on it later in a way that reaches Tom: refuses his fare, says it to him, or tells Ellis and her stage sign shows it | section 7, worked example 2 |
| K3 Recognition by a mark | a person connects Tom to a deed through a thing: a coat, a car, a bruise, an earlier talk | STORY-04 |
| K4 Returning enemy | someone Tom hurt, shamed, spared, paid off or poached meets him again and it shows | section 7, worked example 3; systems 24 |
| K5 Simulation-born alliance or betrayal | a pact, a turned man, a poached crewman, a betrayal whose cause was play, not a scripted beat | sections 2, 3 |
| K6 Crew under nerve | one of Tom's own men breaks, holds, or comes for him, from his own nerve and loyalty | the yard; posts |
| K7 Funny | any of the above that the panel tags funny (STORY-06) | section 5's jokes |

A moment that is part of an authored beat counts only if the beat's outcome came from play (the carrier was cast from the returning pool, or the outcome turned on a choice); the beat firing on its own does not count. The story director's main beats are measured separately (section 5).

## 3. Targets

There is no reference rate. The players' stories study says so plainly: posts never count how often such moments happen in an ordinary evening. The nearest figure is a design focus, not a rate: Michael de Plater, on Shadow of War, spoke of "five or six or seven" orcs a player remembers (MEMORY-SYSTEMS.md, M1). So the targets below are the study's design choices, kept until the owed reference band exists (section 6), and then re-set to the higher of the two.

"Real hours" here means play time at the ruled clock (60 real seconds a game hour), counted only while the tester is playing; skipped or stepped time is left out, so a stepped run cannot inflate the rate. Over five seeded first evenings (three real hours from New game, different first choices):

- T1 (STORY-02): in each of the five evenings, at least one full moment in the first 30 minutes and at least two in every later hour; so at least 5 in a three-hour evening.
- T2 (STORY-03): of all full moments across the five evenings together, at least half come from witnesses, recognition or a returning person (K2, K3, K4, or K6 where it is a man of Tom's coming back), and none counts whose only systems are physics or driving unless a person saw it and it came back. Basis: of 21 stories that came back, Nemesis 10, witnesses 7; physics 0 of 8, driving 0 of 5.
- T3 (STORY-04): of all full moments across the five evenings together, at least a third have the mark field filled. Basis: 4 of KCD2's 7 comebacks.
- T4 (STORY-05): once a rival has noticed Tom, at least one of that rival's men meets him twice; every man Tom beat or shamed who is still on the street meets him again within three game days and refers to it.
- T5 (STORY-06): of all full moments across the five evenings, at least one in five is funny, tagged by panel players (the checker's tags count only where a panel spot-check agrees). PENDING the panel; until then reported as the checker's tag count, marked unconfirmed.
- T6 (STORY-07): every pair of the five first evenings shares fewer than half its full moments, by kind and person.

Added here for the frame (design choices, same standing):

- T7 Said to his face: every deed of weight with a named witness produces a K1 within one game day (the frame's rule); measured as a share, target 100% where the witness is alive and free, with the misses listed.
- T8 Born of the simulation: across one whole seeded playthrough (all seven weeks), at least one K5 that no authored beat caused (a man turned, a crewman poached, a pact formed or broken by play). Basis: Nemesis's best bosses are "totally unique to your game" (de Plater, PC Gamer, 19 Sep 2014), a direction, not a number.
- T9 Later evenings too: at least two full moments an hour on three seeded evenings starting at the hand-over from Act I to Act IIa (the danger point the players' quit study names: the move from the guided week to the open rise; RDR2 loses 31.2 points of owners across chapter 2), and on two more from after the Landing.
- T10 The panel retells it (STORY-08): after a played evening, at least 6 of 8 panel players answer "What happened tonight?" with a sentence that names a person and a later consequence. PENDING the panel; this is the only test players make, and it outranks T1 to T9 when it disagrees with them.

## 4. How the checkers count it

1. Runs. The AI tester plays seeded evenings through the test door (seeded launch, stepped clock, saves as hand-overs; blueprint 09). Three play styles, each a fixed persona brief: rough (fists first, takes what he can), careful (pays, talks, keeps witnesses down), and talker (calls on people, makes pacts). Five first evenings per release candidate (T1 to T6); three hand-over evenings and two after the Landing (T9); one whole playthrough per style (T7, T8). The careful style matters most: it is the run where the readers feared the spine would not wake.
2. The log (STORY-01). The Core writes every deed with its seven slots, every witness, every telling with its chain print, every kept person's attitude change, and every beat the director plays with its carrier and cause. Nothing is judged by a model at this step.
3. Candidates by rule. A script walks the log and proposes candidates: a deed followed, at any later time, by a linked reaction from a named person. It marks which tests the log already proves (choice, named person, comeback) and queues the replay for test 2.
4. The other way. For each candidate the checker replays from the save before the choice with the other option, to a fixed horizon (one game day or the comeback's time, whichever is later), and records whether the outcome differs. This is code, not judgement.
5. Screen and confirm. A Sonnet screen reads each candidate's log extract and tags its kind and a mark if any; a fresh Opus checker confirms the four tests against the evidence and rejects any where the log does not show them. Funny tags (T5) come only from panel players or a panel spot-check agreeing with the checker's tags.
6. Report. Per evening: full moments by hour and kind, near misses, the list with one plain line each ("Lee Drewery, beaten on the rank at 21:10, refused Tom's fare at the ferry rank next noon and told him why"), and the targets passed or failed. Per release: the five-evening table and the sameness check.

A moment is counted once, at its comeback; a comeback that links to two deeds counts once, under the earlier.

## 5. The spine's health, measured beside it

The emergent count says whether the town makes stories; these say whether the spine lands on top of it, on every path. From the same runs:

- S1 The 30-minute rule (WQ-01): longest gap after Act I with nothing reaching Tom; target under 30 real minutes in every run.
- S2 No stacking: no two heavy beats within two real hours (the frame's PROPOSED minimum).
- S3 No repeat: neighbouring beats differ on at least three of seven shape fields; no beat twice.
- S4 The turn's window: in every run, including careful, the turn wakes after the Landing and lesson five and by the end of game week five.
- S5 The bond's hours: Ron at Tom's shoulder for at least a third of play before the turn (the frame's PROPOSED rule).
- S6 The next want: at every sampled minute the Ledger holds one named next thing in a person's words.
- S7 Every ending reachable: the five built states and the hunted state by scripted routes (blueprint ER-END-01), plus each final choice on each opponent path.

## 6. The reference band still owed

The players' stories study names one measurement it could not make from posts: in one ordinary three-hour evening of each of KCD2, GTA V and RDR2, played without a guide, count the moments meeting the four tests and the near misses, with STORY-01's fields (without replays, "could have gone another way" is met when two options were open and the game visibly allowed each). That gives the band for T1, T2 and T9. Until it exists, every target above is LEDGER's own choice and is reported as such, never as "measured against AAA".

## 7. What would make this measure lie

- The tester plays to the test. Fix: persona briefs written before the targets are shown to the tester's author; the tester never sees the log's tags.
- Comebacks that only the log sees. A reaction no player could notice (a line said out of earshot) would pass on paper. Fix: test 4 counts a comeback only when it reached Tom (section 1).
- Authored beats counted as emergence. Fix: section 2's rule; K5 counts only with no authored cause in the log.
- Model judges flattering. Fix: tests 1, 2 and 4 are proved by code from the log and the replays; models only tag kind and mark, and a fresh checker confirms.
- The tester's own play after a choice muddying the replay. Fix: both replays from a choice point run the same fixed idle script, with a control on the original option (section 1, test 2).
- Five evenings too few. They are the study's floor; if any target passes by one moment or fewer, run five more before calling it.
