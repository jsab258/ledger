# A sweep for the town lane, eighth pass, 29 September 2026

What this is: the list is down to bn and bo; i, q, as, aq and bj wait on
Jafar. A helper read TOWN.md, ROADMAP.md, the seven earlier sweeps and the
archived checklist: 148 open rows in possibly non-visual sections are cited
nowhere, nearly all the builder's or past the first hour. What is left sits
after the police decide something. Evidence from the code at 984227b5.

## Candidates, most important first

1. **What an arrest does** (A15.17, consequences of arrest; A15.16, submitting
   or resisting; A15.18's other half; A25.12, a time skip with the ask
   standing; ROADMAP stage 3, "arrest reachable from live play"). About 6 h,
   research first.
   Why: stage 3's own measure. Today no arrest can happen at all: the build's
   only crime is Rita's window, Rita never goes to the police, and a witness
   reports only a detective's crime.
   Not done: only tests and SaveChaos call PoliceFile.CanArrest.
   Reaction.Confront, the arrest in the act, needs a constable watching, and
   the cast has none; the coat's search reaches only the retired Unity layer.
   Nothing decides when a constable calls, how long he is held, or what the
   street and the outfit make of it; a night in the cells on an ask night
   would pass as if Ron never found him.
   The work: research 1990 custody limits, police bail and the caution; a
   custody piece (taken on a named statement, held, bailed, never a game end;
   the coat searched; the street sees him taken, filed as a story; the ask
   night settled), in TownSave and SaveChaos, measured through TownReach
   --first-hour. Which deed in the friends' build may lead to an arrest goes
   to Jafar as one question.

2. **Word that the police are asking** (A15.06, a warning before punishment;
   the audible half of A15.09, which ar left). About 4 h.
   Why: days 4 and 5 are the first hour's climax, Ellis on Quay Street, yet
   the people she asks forget it at once. Nobody says "That detective was
   asking after you", and the claim check would refuse it as invented: the
   town's plainest reaction (Meridian condition 2) and the warning before any
   arrest are both missing.
   Not done: HearTheStreet only adds to her file; nothing in the gossip, the
   street's lines or talk mentions the police.
   The work: each person she asks remembers it (the helper already sends
   memories to talk); the visit filed as a story that is no night-life
   secret, so it cannot count towards Loudness and bring her back; a telling
   line and a to-his-face line; measured through TownReach --first-hour; the
   words to his page.

3. **The damage found in the morning** (the town's half of A12.16, remnants of
   what is broken; A25.07, what a deed leaves handled consistently). About
   4 h, after bo.
   Why: a friend who breaks the window unseen hears nothing next day, though
   the pane is gone. "Somebody put Rita's window in last night" is the town's
   first reaction to an unwitnessed crime.
   Not done: Observation has a slot for somebody who comes on it afterwards
   (ArrivedLater), in the Core and the port, but nothing decides who does; the
   game always sends false (CrimeProbe.h). The street's words after a deed
   last three minutes, in earshot only (an).
   The work: from the routines and bo's hours, who comes on the place before
   it is mended (Rita first, when she opens), each filed as an aftermath
   naming nobody; told with the story's own banks; measured on the forty,
   raising nobody's suspicion. The encounter's unwitnessed control then reads
   "nobody knows it was him", which the builder's regression check keeps.

## Considered and set aside

- The envelope kept after a night away (A33.08, A33.12): a question for the
  first-ask page, not a build. Sheila's question on day 7 (A33.05): past the
  first hour. The same routines in every new game (ROADMAP's "a session worth
  repeating"): design, and friends play once.
- Taking turns (A13.12), acknowledging speech (A31.02), timers across a
  reload (A39.15): already covered. Pause and save screens, ambient
  interruption (A25.13), crowd density (A25.03): the builder's. Other time
  skips wait on the clock ruling (x).
