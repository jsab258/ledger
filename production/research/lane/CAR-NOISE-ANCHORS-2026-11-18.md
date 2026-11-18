# A passing car as a sound in the town's hearing model: real anchors and a proposed value (18 November 2026)

Reviewed 18 Nov 2026: PASS WITH FIXES, applied (production/lane/reviews/REVIEW-CAR-NOISE-ANCHORS-2026-11-18.md).

Lane, for the bounded town task of traffic stage 1 (TRAFFIC-COST-2026-11-17.md section 6: a passing car raises the street's loudness for a few seconds, so a scuffle may go unheard). A proposal with its arithmetic; the town task decides the value inside the C# Core with its goldens. The lane does not touch the Core.

## Real anchors (read 18 Nov 2026)

- Ordinary cars in real traffic, 1990, at 40 to 50 km/h: about 70.5 dB(A) as they pass (70.6 at 35 to 60 km/h; 72.7 in 1982). Berge 1993, Table 1, citing de Veer and Ullrich; a road on an 18% grade (the lane's reading: mostly engine and driveline noise); the distance is not stated in the table (the standard test distance is 7.5 m).
- The type-approval limit for new cars fell from 80 to 77 dB(A) in October 1989 (Berge 1993). That is a full-throttle acceleration test, louder than a car cruising, so it is a ceiling, not a passing level.
- Tyre noise matters even at 40 to 60 km/h (Berge 1993, section 3). (Wet roads are not in the source; the costing's wet tyre layer is a separate choice.)
- A 1990 UK survey (BRE) gave a mean street level of 55.6 dB as LA10 over 18 hours, the level exceeded 10% of the time (Hinton and Shield 1995). The paper gives no quiet side-street background levels; not found elsewhere in this run.
- Sound from a single passing car falls about 6 dB per doubling of distance (a point source; textbook, not re-read today).

## The game's hearing scale (ledger/Assets/Scripts/Core/Perception.cs, read only)

Loudness in dB-like units; audible radius r = 1.5 m x 2^((L - floor) / 8), capped at 250 m; the floor is the ambient at the listener (daytime street 45, 3am 15, rain adds 12). So 8 game units per doubling of distance stand for the real 6 dB: one real dB is about 1.33 units. The scale is not real decibels and is not calibrated to them.

## Proposed value: a passing car at about 83 to 84 units, at its usual 1.5 m reference

Matched on how far a car stands above a daytime street, the one comparison both scales share:
- Real: 70.5 dB(A) at about 7.5 m is about 15 dB above the 1990 street's 55.6; at the game's 1.5 m reference it is about 14 dB more (6 dB per doubling, 7.5 to 1.5 m), so about 29 dB above the street.
- Game: 29 x 1.33 = about 39 units above the daytime floor of 45, so about 83 to 84 (84 used below). The street's 55.6 is an LA10, mostly made by passing traffic, so a true background would be lower and the car's margin larger: 84 is more likely too low than too high.

Worked, so the town task can check it (computed here with the Core's formula):
- Daytime street: a car is heard within about 44 m. At 3am: to the 250 m cap.
- Masking, assuming the floor becomes the louder of the ambient and the car's level at the listener (a new rule: the Core has none; rain only adds a flat 12): while a car passes 10 m from a listener, the floor there rises to about 62 (84 minus 8 x log2(10 / 1.5)); a shout (65) is then heard only within about 1.9 m, instead of about 8.5 m on a quiet daytime street. At 20 m from the road the floor is about 54 and the shout carries about 3.9 m. That is the costing's "a scuffle may go unheard", out of the existing model with no special case.
- How long: the car's own loudness at the listener moves with it, so the masking lasts only while it is near: about 3 to 4 seconds in view at 20 to 30 mph (TRAFFIC-COST section 2), longer when it waits for a person. The reference model's spawn and despawn log (tools/lane/traffic/, G6) gives the times for golden rows.

## Open for the town task

- How a passing car sets the floor is a new rule for the town task: the louder of the two (as assumed above) or a sum. The Core has no such rule today; rain adds a flat 12.
- A horn: real horns are much louder than a passing car; no source read today, so no value proposed.
- Headlamps and cover (a car briefly blocking sight lines): no values here; the reference model gives each car's position every 0.1 s for them.
- The 84 rests on one comparison (car above street level); a second anchor (for example a real shout's level against the game's 65) would test the scale. Unverified until then.

## Sources

1. T. Berge, "Noise emission levels from passenger cars: past, present and future", Proceedings of the Institute of Acoustics, 1993. https://www.ioa.org.uk/system/files/publications/T%20BERGE%20NOISE%20EMISSION%20LEVELS%20FROM%20PASSENGER%20CARS%20-%20PAST%20PRESENT%20AND%20FUTURE.pdf
2. J. M. Dunne and a second author (initials unclear in the scan), "Vehicle Noise Legislation: An Overview", Proceedings of the Institute of Acoustics vol. 15 part 1, 1993 (the directives' dates: 84/424/EEC of 3 Sep 1984; 92/97/EEC for new types from 1 Oct 1995, all new vehicles from 1 Oct 1996; its limit tables were not legible). https://www.ioa.org.uk/system/files/publications/JM%20DUNNE%20IC%20YARNOLD%20VEHICLE%20NOISE%20LEGISLATION%20AN%20OVERVIEW.pdf
3. J. Hinton and B. Shield, "Noise trends in an urban environment", Proceedings of the Institute of Acoustics vol. 17 part 4, 1995 (Birmingham; the BRE 1990 survey's mean LA10 18 h of 55.6 dB). https://www.ioa.org.uk/system/files/proceedings/j_hinton_b_shield_noise_trends_in_an_urban_environment.pdf
4. Project: ledger/Assets/Scripts/Core/Perception.cs (hearing constants and formula), TRAFFIC-COST-2026-11-17.md, TRAFFIC-STAGE1-REFERENCE-MODEL-2026-11-18.md.
