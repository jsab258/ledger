# Rumour reach in Quay Street, with the slice's routines written so friends meet

23 September. Jafar's decision 7 (a): make faint knowledge show, and fix the routines so friends actually meet, since 55 of the Unity prototype's 80 friendships never did; then measure reach again, touching no constant. This is the routines half and the measurement. Showing faint knowledge is the next piece.

## Plain English

- **Every friendship in the slice's cast now meets.** Ten people who work on or pass through Quay Street, with the prototype's own friendships between them (20 ties), are placed hour by hour so friends share a doorway, a counter or the pavement outside. All 20 are within talking range at least an hour a day, 3.3 hours on average. In the prototype's hand-placed city, 55 of 80 never were.
- **The story now reaches people.** A witness who is only half sure has told 1.7 of the other nine, on average, within thirty minutes of play (two and a half game days); one who is sure has told 4.7. Only 2 of 10 half-sure witnesses reach nobody, against 29 of 40 in the prototype's city. At 0.6 sure, nobody reaches nobody.
- **The two who reach nobody at half-sure are Zlata and Marla.** Their friendships (0.4 to 0.5) are too weak to carry a half-sure story at all: 0.5 x 0.5 x 0.8 is the 0.2 floor. That is the certainty arithmetic, which this does not touch.
- **No constant changed.** The retelling decay (0.8), the floor (0.2), the half-life and the six-metre talking range are the Core's own.

## What was done

- The cast, places and routines are in production/specs/quay-cast.json: Mickey's minicab office (Rocco, Lena, the dispatcher Zlata), Rita's pawn (Rita, Victor), the fish market (Marla), the quay (Joey), and Sam, Ada and Noor passing between them. Places are the scene file's own coordinates.
- Measured with the shipped Core's GossipMill and the game's meeting rule (within 6 m, a round every 6 game minutes, the hourly fade), the same method as game-design/rumour-reach-2026-09-23.md section F, over the 24 hours a sighting could happen. The measuring program is a throwaway in the scratchpad, as that study's was.
- One routine was moved after the first measurement: Victor stays on Rita's step until six, where Lena's evening errand finds him (their 0.4 tie had been the only one never together).
- The Unreal game does not read this file yet: the slice's walkers are still to come.

## Beside the prototype's city (section F of the earlier study, standing at routine targets)

| | prototype's city (40 people, 80 live ties) | Quay Street slice (10 people, 20 ties) |
|---|---|---|
| friendships never within 6 m | 55 / 80 | 0 / 20 |
| mean hours together a day | 2.1 | 3.3 |
| half-sure witness (0.5): mean others told at 60 h | 0.52 | 1.72 |
| half-sure witnesses reaching nobody | 29 / 40 | 2 / 10 |
| 0.6 sure: mean told / reaching nobody | 0.84 / 26 of 40 | 2.80 / 0 of 10 |
| sure (1.0): mean told / reaching nobody | 1.58 / 24 of 40 | 4.73 / 0 of 10 |

## The measurement, verbatim

    quayCast people=10 ties=20 meanTie=0.53 talkRangeM=6
    coPresence never=0/20 meanHoursPerDay=3.3 medianHoursPerDay=3.0 atLeastOneHour=20/20
      tie rocco-sam 0.8: 8.0 h/day
      tie rocco-lena 0.7: 8.0 h/day
      tie noor-ada 0.7: 2.0 h/day
      tie sam-lena 0.6: 3.0 h/day
      tie ada-lena 0.6: 3.0 h/day
      tie joey-rocco 0.6: 3.0 h/day
      tie noor-sam 0.6: 3.0 h/day
      tie rita-victor 0.6: 8.0 h/day
      tie ada-sam 0.5: 3.0 h/day
      tie marla-ada 0.5: 2.0 h/day
      tie noor-lena 0.5: 2.0 h/day
      tie noor-rocco 0.5: 2.0 h/day
      tie victor-sam 0.5: 2.0 h/day
      tie zlata-joey 0.5: 3.0 h/day
      tie marla-sam 0.4: 4.0 h/day
      tie noor-marla 0.4: 2.0 h/day
      tie victor-lena 0.4: 1.0 h/day
      tie rita-joey 0.4: 1.0 h/day
      tie zlata-sam 0.4: 3.0 h/day
      tie joey-sam 0.3: 3.0 h/day
    FIRST SIGHT 0.50: others who have heard, mean over the 24 hours the sighting could happen
      rocco  deg= 4 1h=1.1 3h=1.4 6h=1.8 12h=2.5 24h=3.1 60h=3.1
      lena   deg= 5 1h=0.9 3h=1.3 6h=1.6 12h=2.4 24h=3.1 60h=3.1
      zlata  deg= 2 1h=0.1 3h=0.1 6h=0.1 12h=0.1 24h=0.1 60h=0.1
      sam    deg= 8 1h=1.0 3h=1.4 6h=1.8 12h=2.5 24h=3.2 60h=3.2
      rita   deg= 2 1h=0.4 3h=0.5 6h=0.6 12h=0.8 24h=1.0 60h=1.0
      victor deg= 3 1h=0.5 3h=0.5 6h=0.7 12h=0.9 24h=1.1 60h=1.1
      marla  deg= 3 1h=0.1 3h=0.1 6h=0.1 12h=0.1 24h=0.1 60h=0.1
      joey   deg= 4 1h=0.3 3h=0.5 6h=0.6 12h=0.8 24h=1.1 60h=1.1
      ada    deg= 4 1h=0.5 3h=0.8 6h=1.0 12h=1.5 24h=2.2 60h=2.2
      noor   deg= 5 1h=0.5 3h=0.7 6h=1.0 12h=1.5 24h=2.2 60h=2.2
      ALL 10 as witness: at 60 h mean 1.72, max 3.2, reaching 0: 2/10
    FIRST SIGHT 0.60: others who have heard, mean over the 24 hours the sighting could happen
      rocco  deg= 4 1h=1.2 3h=1.6 6h=2.1 12h=3.1 24h=4.0 60h=4.0
      lena   deg= 5 1h=1.0 3h=1.5 6h=2.0 12h=3.0 24h=4.0 60h=4.0
      zlata  deg= 2 1h=0.2 3h=0.3 6h=0.5 12h=0.7 24h=1.0 60h=1.0
      sam    deg= 8 1h=1.3 3h=1.9 6h=2.5 12h=3.7 24h=5.0 60h=5.0
      rita   deg= 2 1h=0.4 3h=0.5 6h=0.6 12h=0.8 24h=1.0 60h=1.0
      victor deg= 3 1h=0.5 3h=0.7 6h=0.9 12h=1.4 24h=2.0 60h=2.0
      marla  deg= 3 1h=0.1 3h=0.2 6h=0.3 12h=0.6 24h=1.0 60h=1.0
      joey   deg= 4 1h=0.4 3h=0.7 6h=0.9 12h=1.4 24h=2.0 60h=2.0
      ada    deg= 4 1h=0.7 3h=1.2 6h=1.7 12h=2.7 24h=4.0 60h=4.0
      noor   deg= 5 1h=0.7 3h=1.1 6h=1.6 12h=2.6 24h=4.0 60h=4.0
      ALL 10 as witness: at 60 h mean 2.80, max 5.0, reaching 0: 0/10
    FIRST SIGHT 1.00: others who have heard, mean over the 24 hours the sighting could happen
      rocco  deg= 4 1h=1.8 3h=2.8 6h=3.5 12h=5.0 24h=6.6 60h=6.6
      lena   deg= 5 1h=1.3 3h=2.0 6h=2.8 12h=4.3 24h=6.0 60h=6.0
      zlata  deg= 2 1h=0.5 3h=1.0 6h=1.3 12h=1.8 24h=2.3 60h=2.3
      sam    deg= 8 1h=1.9 3h=2.8 6h=3.8 12h=5.8 24h=8.0 60h=8.0
      rita   deg= 2 1h=0.5 3h=0.6 6h=0.9 12h=1.4 24h=2.0 60h=2.0
      victor deg= 3 1h=0.6 3h=1.0 6h=1.5 12h=2.5 24h=4.0 60h=4.0
      marla  deg= 3 1h=0.6 3h=1.0 6h=1.4 12h=2.1 24h=3.3 60h=3.3
      joey   deg= 4 1h=0.8 3h=1.5 6h=2.1 12h=3.3 24h=5.0 60h=5.0
      ada    deg= 4 1h=0.8 3h=1.5 6h=2.1 12h=3.4 24h=5.0 60h=5.0
      noor   deg= 5 1h=0.8 3h=1.3 6h=2.0 12h=3.2 24h=5.0 60h=5.0
      ALL 10 as witness: at 60 h mean 4.73, max 8.0, reaching 0: 0/10
