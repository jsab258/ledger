# The combat simulator

combat_sim.py runs COMBAT-SYSTEM.md's rules on fights, threats and takedowns. Seeded and repeatable: `python3 combat_sim.py --seed 1990 --n 2000` reproduces results.json byte for byte (checked twice, and by the fresh reviewer). It takes about 15 s.

- results.json: every scenario's numbers (win, lost, escaped, stopped, durations, deaths per 1,000, knock-outs, yields, flights, surface use, the opponents' worst injuries, the consequences: charges at each level, the street's reading band, revenge, reports, hospital days), the stealth approach grid (light by crouch by surface), the takedowns, the held-choke curve and the threat table.
- results-print.txt: the short print.
- TUNE at the top holds every number, named as in COMBAT-SYSTEM.md.

Limits, named so nobody over-reads it: the player is a bot with a style (patient, masher, street, menace, runner), not a person; positions and spacing are not simulated (no geometry; the surface and the kerb are chances by place); bystanders, police arrival and consequences are rates, not people; rare events (deaths in fist fights, falls) rest on few cases at 2,000 fights and are leads. The come-round, sends, growth and police procedure are not in it.

Fixes after the fresh review (tests-work/REVIEW-1.md): a knock-down no longer ends a fight; a beaten Frank counts as a loss; finishing with a weapon now lands; a shove into a surface is under the fists cap; cosh, fist and knife takedowns run through the body rule, and the choke's break chance now rises with the man's size and as Frank's wind goes; a critical fall puts Frank out, never dying; the fall needs three heavy blows as RT2-12; crouch hides a shape only in the dark; townspeople may use surfaces and counter by the same chance as Frank; mashing now empties a man and loses; Frank's menace weighs only on his opponents; a knock-out is at least ABH; the threat weight is general by weapon menace.
