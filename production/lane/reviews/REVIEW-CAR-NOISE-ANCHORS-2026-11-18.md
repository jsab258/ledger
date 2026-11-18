# Review: CAR-NOISE-ANCHORS-2026-11-18 (fresh reviewer, 18 November 2026)

Verdict: PASS WITH FIXES

All three links fetched 18 Nov 2026; Perception.cs read only.

What holds: every cited figure, date and directive matches its source, and the Core's constants match (1.5 m, divisor 8, cap 250 m, street 45, 3am 15, rain +12, shout 65). All worked numbers recompute: 84 units; 44.0 m by day; 250 m cap at 3am; floor 62.1 at 10 m, shout 1.93 m (8.49 m quiet); floor 54.1 at 20 m, shout 3.86 m.

Findings

1. Wrong about the Core. The "Open" line says the Core has a rule for rain (the louder of the two, or a sum) that can be reused. It has none. Rain is a flat +12 added to the floor. The worked masking cases already assume the louder of the two (the floor becomes 62, not 45 plus something). Fix: "The Core has no rule for combining two floors; rain is a flat +12. The worked cases assume the louder of the two. The town task must choose and record a rule."

2. Wet roads overstated. Berge never mentions wet roads. Fix: keep "tyre noise matters even at 40 to 60 km/h (Berge, section 3)". Move the wet-road point to its own line, marked as the costing's assumption, not Berge.

3. "Mostly engine and driveline" is the lane's inference from the grade, not the paper's words. Fix: add "(inference, not stated)".

4. The street figure is not a background level. LA10 is the level beaten 10% of the time, so it is mostly passing traffic. The game's 45 is a background floor. Also, the paper does not say where the BRE readings were taken. Comparing a car against LA10 likely makes the car look too quiet against a true background. Fix: state this under the 84, and say the value is more likely low than high.

5. Small point. Converting the distance in game units (8 x log2 5 = 18.6) gives 83.4, not 84. Fix: write "about 83 to 84".

6. Dunne's second author: the file name says I C Yarnold, but the scan is unclear. Fix: "J. M. Dunne and I. C. Yarnold (initials unclear in scan)".
