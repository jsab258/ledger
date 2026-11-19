# Feel measurement method for fists, on foot, being seen and chases (20 November 2026)

Part (b) for the four verbs of his pick "1" (20:16, 19 Nov), the same way as DRIVING-MEASUREMENT-METHOD-2026-11-19.md. The games are in FEEL-REFERENCE-GAMES-2026-11-20.md. This file says how professionals measure each verb from video, the numbers per verb, how they are sampled, which behaviours are written down as experience rules, and the sheet the builder fills in on his PC beside the driving sheet from Monday 23 Nov. Written by the cloud lane (task 4f).

Permission: his ruling of 17 Nov lets the builder measure how other games behave "from gameplay footage in the browser", outside only, videos never downloaded. Same browser, same frame stepping and same screenshot rule as the driving method (its section 3): screenshots read to measure stay outside the repository and are deleted once the numbers are written.

Tags as in the games file: [READ] fetched 20 Nov 2026; [SS] search title only; [I] our own reasoning, not from a source.

## 1. How professionals measure these from video

What was found, honestly: very little is published on measuring these verbs from footage. Most of the method below is the driving method's, carried over, plus a few dated sources.

- Fighting-game frame data (the nearest professional practice for blows). Players who build frame data capture at 60 fps and step one frame at a time: start-up is counted from the first frame that leaves the idle pose to the frame before contact; hit-stun counts must take out the hit-stop (their example: 39 frames minus 13 of hit-stop is 26); named pitfalls are games that do not hold a steady 60, repeated frames that hide when a blow is active, and hit-stop distorting the counts. Dustloop forum, "Counting move frames", July to August 2012 https://www.forums.dustloop.com/topic/5153-counting-move-frames/ [READ]. Community practice, not a standard, but the pitfalls match the driving method's clip check.
- Hit-stop as designed. Masahiro Sakurai: a brief freeze of both fighters to sell the impact, scaled with damage, capped, tuned per attack; the flinch pose takes four frames. Famitsu column vol. 490 to 491, translated by Source Gaming, 11 Nov 2015 https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/ [READ]. Intent, no totals. The melee sheet's other hit-stop sources (Capcom's seminar, Celia Wagar, 2017) are in FEEL-TARGETS-MELEE-2026-11-18.md.
- Input delay. Digital Foundry measured button-to-screen delay with a camera filming the pad and the screen together (Kotaku, 7 Sep 2009, pointing to Eurogamer's method page, which was not reached) https://kotaku.com/measuring-the-time-it-takes-between-a-button-press-and-5353769 [READ]. Gameplay footage shows no pad, so true press-to-hit cannot be measured from it (section 2 says what is measured instead).
- The third-person camera. Epic lists the parts a camera is tuned by: arm length (distance), position lag and rotation lag, field of view, offset and pitch. Epic, "Six ingredients for a dynamic third person camera", undated https://www.unrealengine.com/tech-blog/six-ingredients-for-a-dynamic-third-person-camera [READ]. That is the list of numbers to estimate. John Nesky's GDC 2014 talk names the failures to log (lost orientation, blocked sight lines, poor depth judgement, sickness) https://gdcvault.com/play/1020460/50-Camera [READ, abstract only].
- Perception. IO Interactive's design gives each person senses (sight, hearing) feeding shared knowledge that updates only now and then, so a reaction can lag what was seen (Tommy Thompson, The AI of Hitman 2016, Game Developer, 7 Aug 2019) https://gamedeveloper.com/design/the-ai-of-hitman-2016- [READ]. No ranges or times are published for any game read. Splinter Cell: Blacklist's perception talk (GDC 2014) is members only.
- Chases: no source on measuring a chase was found.
- Not reached, to try from his PC: Eurogamer's "The Lag Factor" (2009), Steve Swink's Game Feel, Nesky's full talk, Naughty Dog's and Ubisoft's motion matching talks, any community detection-range test for Hitman or Splinter Cell.

So the method is ours, built on the driving method, and every number it gives is our own measurement. No number is copied from anyone into a target (his rule of 17 Nov; the driving method section 4).

## 2. The numbers, per verb

Each number: what it is, where in the footage, how it is read. Units are seconds, metres and degrees. Scale in metres comes from objects of known size in the frame [I]: a door about 2.0 m high, a man about 1.75 m, a car about 4.3 m long, a paving slab 0.6 m (Britain) or a kerb; the object used is written down beside each sample.

### Fists (F1 to F9; key names as the melee sheet C1 to C15 where they match)

- F1 Start-up (melee sheet C2): first frame the player's blow leaves its ready pose to the frame of contact. Jab, hook or heavy, each counted separately. Press-to-hit (C1) is not visible in footage; it is measured only in our own build, or from a clip that shows an input overlay if one is found (noted).
- F2 Recovery: frame after contact to the first frame the player can visibly act again (a new blow starting, a block or a step).
- F3 Hit-stop (C3): frames where both bodies are frozen at contact, per kind of blow. Zero is a valid result (the melee sheet notes KCD2 may have none).
- F4 Reaction of the man struck (C4): contact to his first frame back in a ready pose; light and heavy separately; and whether he staggers, steps back, falls.
- F5 The incoming blow, readable (C5): first frame of the enemy's wind-up to contact; and what shows it (a shoulder drop, a sound shown by a visible flinch, a flash, a camera move).
- F6 Block and dodge answer: the player's guard or dodge starting to be fully up, when it can be seen in the frame; and the gap between the enemy's tell and the player's answer in successful defences (a lower bound on what players manage).
- F7 Camera in a fight: distance change on entering a fight (character height on screen before and after, section 3), the time the change takes, any shake on a hit (frames), any slow motion (frames and how slow).
- F8 Blows to put a man down (C15): count per fight, with the kind of blow.
- F9 Rhythm: blows a minute by the player and by enemies over a whole fight; the longest gap with no blow.

### On foot (W1 to W10)

- W1 Start: first frame of input-driven movement (the body leans or the first foot lifts) to full walking speed, and to full running speed.
- W2 Stop: release (the last frame of full speed) to standing still; walking and running separately.
- W3 Turn: a 180-degree turn while running: first frame of turning to running the other way at full speed; and a 90-degree corner.
- W4 Speeds: walk, jog, run, sprint, in metres a second, timed over a known distance (paving slabs, a car length, a doorway gap) or by stride count times an estimated stride.
- W5 Camera distance: the character's height on screen as a share of the frame height, standing; converted to metres with the field of view (section 3).
- W6 Camera height and offset: where the character's head sits on screen (fraction across and down); shoulder offset left or right.
- W7 Camera lag: on a start, frames until the camera begins to follow; the most the character drifts from his resting screen place; frames to settle back. Same on a stop and on a hard turn.
- W8 Field of view: horizontal, at walking and at sprinting (section 3).
- W9 Tight spaces: in a corridor, a doorway, an alley and against a wall: does the camera pull in, swing, fade the wall, clip through, lose the character; the frames it takes to settle; the closest distance reached.
- W10 Small moves: a step over a kerb, a doorway, a stair: does the walk slow, and by how much.

### Being seen (S1 to S8)

- S1 Glance: the first frame a person's head or eyes turn to the player after he comes into their view (or makes a sound), measured from the frame the player comes into a clear line of sight; with the distance at that moment.
- S2 How a glance is shown: what the player sees (a head turn, a stare held, a stop in walking, a line spoken, a mark or meter on screen), and how long it lasts.
- S3 Suspicion to alarm: from the first glance to a full reaction (a shout, running off, calling a guard, a fight); with what the player was doing.
- S4 Recognition: a person who has seen the player before, or knows his face from a report, reacting to him: time from line of sight to the reaction, distance, and what shows it (KCD2's backing away from a branded man, a guard's challenge).
- S5 Sight range: the furthest distance a glance (S1) happens, in daylight and at night or in rain where the footage has it.
- S6 Sound range: the furthest distance a person visibly turns to a sound the player makes (a fight, a breaking window, running), only where the reaction is seen.
- S7 Telling: from a witness's alarm to the report reaching others (police arrive, a shopkeeper changes, a line about it); in game minutes where a clock shows, else real minutes, and whether it happens off screen.
- S8 Losing it: how a suspicion ends when the player leaves sight; the time to calm.

### Chases on foot (C1 to C8; distinct from the melee sheet's C numbers by the word "chase")

- Chase C1 Start: what starts it (a witness, a runaway, the police), and the time from the trigger to the first running step on each side.
- Chase C2 Length: from both running to caught or lost, per chase.
- Chase C3 The gap: distance between chaser and runaway every 5 seconds (known objects for scale); does it close steadily, or jump (the rubber band L.A. Noire is criticised for).
- Chase C4 Speeds: runaway and chaser in metres a second (W4's method), and whether either speeds up or slows when near.
- Chase C5 Obstacles: things in the way per minute (stalls, people, cars, fences), and what each does (a slowdown, a vault, a fall, a tackle chance).
- Chase C6 Endings: how it ends (a tackle, a corner, the runaway escapes by sight, by distance, by a hiding place, a timer), and the time from the decisive moment to control back.
- Chase C7 Bystanders: what passers-by do (step back, block, point, join in).
- Chase C8 Camera in a chase: distance change, any cut, whether the runaway stays in view, and whether a marker shows him when out of sight.

## 3. Reading scale, field of view and distance from a frame [I]

No source on doing this from game footage was reached; these are standard geometry, our own and unverified, to be checked once on a game whose field of view is known (a PC game with the setting shown on screen) before the numbers are trusted.
- Field of view by panning: when the camera turns at a steady rate, time how long a fixed landmark takes to cross from the left edge to the right edge (t), and the time for a full 360-degree turn at the same rate (T). Horizontal field of view is about 360 times t divided by T. Five pans, middle value.
- Distance from size: with the vertical field of view V (from the horizontal and the frame's shape), a man of height h who fills a fraction f of the frame height stands at about h divided by (2 times f times tan(V/2)) from the camera.
- Speed: distance from known objects passed (paving slabs, car lengths) divided by the frames taken.

## 4. Sampling, two measurers, what is kept

As the driving method section 3 and 4, unchanged:
- Clip check first: frame rate from Stats for nerds, repeated frames (step 60 frames; under 55 new pictures means the game ran slower than the upload, noted, counts in game frames), normal camera, no mods, no edit cuts inside a sample, minute marks of each scene needed.
- At least five samples per number, from at least two clips or two separate moments where possible.
- Two measurers working apart: the builder first; a later builder run that has not seen the first sheet second, picking at least two of each five samples itself. Pixel measures (camera distance, field of view) may also be read blind by a fresh helper from the same screenshots as a third check.
- Report the middle value and the lowest and highest. If the two measurers' middle values differ by more than 10% (or 3 degrees, or 2 frames for anything under 0.2 s), both measure again; if they still differ, report both and mark it uncertain.
- Only our own numbers are kept. Numbers from other people (forums, wikis, frame-data sites) may say where to look, never what the target is.

## 5. Behaviours written down as experience rules

One line each, with the minute mark; each becomes a candidate rule (an ER line with its check, the format of DESIGN's experience rules) once seen in at least two games or twice in one, and is marked "not for LEDGER" where it breaks canon or a ruling.
- Fists: what a struck bystander or friend does; whether a fight draws a crowd and what it does; how a fight ends (down, surrender, run off) and how long until free play; what the camera does when a second attacker joins; whether a blow from behind is warned of, and how (the sound-only part is a research item, as in the teardown brief).
- On foot: bumping into people (who stumbles, who speaks); running in a crowd; the camera at a door and on stairs; how the character shows tiredness or a limp.
- Being seen: how a stare is held and broken; what a witness does next (runs, phones, tells a friend, follows); how a recognised man is treated (backing away, refusing to trade, a guard's challenge); whether the player is ever told he was seen when he could not have known (LEDGER says no: ER-CORE-02).
- Chases: how a chase is offered or forced; what happens on a fall; how a caught runaway behaves; what the town does afterwards.

## 6. The measuring sheet, extended (the builder fills it in on his PC)

The same file per game per measurer in production/research/lane/measurements/ as the driving sheet, with these blocks added after the driving block for the verbs that game serves (FEEL-REFERENCE-GAMES section 6).

```
Clip check: as the driving sheet (reuse it if the same video was checked for driving or the teardown)
  Extra minute marks: fist fight __ __ __   on foot in street __ interior __ alley __
                      noticed or witnessed __ __ __   foot chase __ __ __
Fists (five samples each; scale object named)
  F1 start-up s  jab _ _ _ _ _  hook _ _ _ _ _  heavy _ _ _ _ _
  F2 recovery s  _ _ _ _ _      F3 hit-stop frames  jab _ hook _ heavy _ (x5)
  F4 reaction s  light _ _ _ _ _  heavy _ _ _ _ _   kind: stagger / step / fall
  F5 enemy tell to contact s  _ _ _ _ _   what shows it:
  F6 guard up s _ _ _ _ _   tell-to-answer s _ _ _ _ _
  F7 camera: height share before/after _/_  change s _  shake frames _  slow motion _
  F8 blows to down _ _ _ _ _   F9 blows a minute player/enemy _/_  longest gap s _
On foot
  W1 start to walk s _ _ _ _ _  to run s _ _ _ _ _   W2 stop walk s _ _ _ _ _  run s _ _ _ _ _
  W3 180 turn s _ _ _ _ _  90 corner s _ _ _ _ _
  W4 m/s walk _ jog _ run _ sprint _ (x5 each; object)
  W5 height share _ _ _ _ _ -> distance m _   W6 head across/down _/_  shoulder L/R
  W7 lag: frames to follow _  drift share _  settle frames _ (start, stop, turn)
  W8 field of view deg walk _ sprint _ (pans x5)
  W9 tight spaces (corridor, door, alley, wall): what it does, settle frames, closest m
  W10 kerb, door, stair: slow-down share
Being seen
  S1 glance s _ _ _ _ _ at m _ _ _ _ _     S2 how shown, how long
  S3 glance to alarm s _ _ _ _ _ (what Tom did)   S4 recognition s / m / how shown
  S5 sight range m day _ night _   S6 sound range m _ (which sound)
  S7 telling: minutes _ on or off screen   S8 calm after leaving sight s _
Chases on foot
  C1 trigger, s to first step _   C2 length s _ _ _ _ _   C3 gap every 5 s: _ _ _ _ _ _
  C4 m/s runaway/chaser _/_  speeds up near? yes/no   C5 obstacles a minute _ (kinds)
  C6 ending kind, s to control _   C7 bystanders   C8 camera, marker when unseen?
Behaviours (one line each, minute mark)
Notes: numbers marked uncertain and why
```

### Hours on his PC, priced per verb

PC hours of the builder's session; none of them his hands. Times per game are our judgement from the driving sheet's figures (its numbers block about 95 minutes for ten numbers), replaced by real ones after the first game.

| Verb | Games | First measurer | Second measurer | Together |
|---|---|---|---|---|
| Fists (9 numbers, behaviours) | Sleeping Dogs, KCD2, GTA IV full (about 75 min each); Mafia DE light (about 30 min) | about 4.25 h | about 3 h | about 7.25 h |
| On foot (10 numbers) | GTA IV, Mafia DE, GTA V, RDR2 (about 70 min each) | about 4.75 h | about 3.5 h | about 8.25 h |
| Being seen (8 numbers; finding the scenes takes longest) | KCD2, RDR2, Hitman, GTA V (about 60 min each) | about 4 h | about 3 h | about 7 h |
| Chases (8 numbers) | L.A. Noire, Sleeping Dogs, GTA V (about 50 min each) | about 2.5 h | about 2 h | about 4.5 h |
| New clip checks | Hitman, L.A. Noire (25 min each) | about 0.75 h | reused | about 0.75 h |
| Field-of-view method check, once (section 3) | one PC game with its setting shown | about 0.5 h | none | about 0.5 h |
| All four verbs | | about 16.75 h | about 11.5 h | about 28 h |

Counted once: every clip check for GTA V, GTA IV, Sleeping Dogs, Mafia DE, KCD2 and RDR2 is already priced in the driving sheet or the teardown brief and is not counted here. Where the teardown's early, middle and late pieces contain a fight, a chase or a witness, the builder takes those samples from the same stepping (noted on both sheets) and the time saved comes off this table.

Lean order if the week is tight: fists and on foot first (the melee and movement bands are what the one-shot's loops tune), both measurers; then being seen and chases with one measurer, the second later. Fists and on foot with both measurers: about 16 hours.

## 7. What comes out

A filled table per verb, game by game: each number with its middle value, spread, sample count and the two measurers' middle values, beside the targets it informs (FEEL-TARGETS-MELEE's bands for fists; the parts tree's standards for moving, being seen and chases). Where measured games disagree with a provisional band, the band is changed with the evidence and the change recorded. The behaviours become experience rules for the prototype's loops and the Unreal port. The parts tree's research items RN-01, RN-03, RN-05, RN-07 and RN-08 point here.
