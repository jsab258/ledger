# REVISION-1: what changed in the combat and stealth pass, and why

25 Nov 2026, the same day as the pass. His answers 10:52 to 11:31 ("combat revision A, start it now"): chance pick A (advisor 382), D1, D2 and D3 yes, and his question at 10:52 ("what happens if I stab or shoot someone in the arm vs face or chest?"). Opus 5.5 for design; Sonnet readers for the law and the wound research; a fresh Opus question writer, tester and reviewer.

## His decisions applied

| Change | Where | Why |
|---|---|---|
| The chance rule written once, near the top: readable rules decide; chance only at the violent end; every chance fixed to the save | COMBAT-SYSTEM.md, new section | his pick A |
| Blocks follow what the struck man is doing (guard up and facing, mid-swing, emptied); his guard comes up by his reaction time against the blow's wind-up, not a roll at landing | CS-05, chance rule; SIM react() and land() | A: no hidden roll on a correct play; the fresh review found the first fix still flipped a coin for the guard |
| Blows land on the attacker's line (high, low, the weapon arm; a low kick or low thrust on the legs; a guarded blow on the forearms); the zone dice table removed | CS-02, CS-05; SIM aim_line() | A: unaimed blows by line, not a table |
| Knock-down and knock-out by thresholds on force and visible state (head harm, wind), steadiness measured before the blow's own harm | CS-05; SIM land(), knockdown() | A; the review found the first version counted the blow against itself |
| Stealth: he turns only for his routine glance (a rhythm the player can watch), a footstep inside his hearing, or other eyes; "turned at the last moment" removed | CS-12; SIM approach() rewritten, three ways to play | A |
| Choke: no break chance, except a big, fresh man against a winded or hurt Frank; time by build (6.5, 7.5, 10 s) | CS-13; SIM | A |
| Cosh from behind: out every time, no death from one blow; fist from behind floors, never puts out | CS-13 | A: the low end safe and certain |
| Disarm by grip and moment (winded, hurt, arm hurt, just swung), else a struggle for the arm; guns by the same rule | CS-08; SIM try_grab() | A |
| Fixed-to-the-save draws for the knife's depth, the fall at the kerb (and where he falls), whether a dying man is helped, how a critical wound ends, gun wounds, the held choke | SIM fixed(), Fight.chance() | A; the review found the helped draw and the fall position still on the session's stream |
| Reload check: the same act from the same save under two different random streams gives the same result; a different save differs | SIM reload_check() | A; the review found the first check too weak |
| One finishing blow raises harm one level at most; the cue (he stops covering, goes still; "He's not moving. Again?"); a bot that heeds the cue | CS-05, CS-13, CS-14; SIM finish() | D2 yes, readable as it gets worse |
| D1 yes: the held choke kills, the body showing it; the curve moved later (no risk for 40 s past the knock-out) | CS-13; SIM choke_death(), now drawn from the save | D1; the review found the first curve began before its only source |
| D3 yes: a gunshot can kill at any stage | CS-23, RT-10 replaced in part | D3 |

## His gaps closed

| Change | Where | Why |
|---|---|---|
| What each zone does for blunt, blade and gun: arm (drops it, out until treated), leg (cannot run, crawls), torso (drops him, serious to dying), head and face (knock-out, broken face, dying; a mark the town names him by), neck (most dangerous) | new CS-31; SIM limb(), face marks, edge table with face and neck split | his question of 10:52 |
| Y1.5 restored: an aimed shot to the arm disarms, one to the leg stops a runner | CS-23, CS-31 | his brief |
| Gun table by zone and range for the revolver and the sawn-off, worse than a knife, with hit by aim and sway | CS-23, CS-31; SIM gun_table() | his brief; research partial (below) |
| Where weapons come from in 1990 (homes, the ironmonger, the chandler, Rita's back room with Wayne, off a man, off a body, a rival's lock-up, RT2-14 for guns) and the carrying and selling law of the time | new CS-32; rev1-work/RESEARCH-LAW.md | his brief |
| Searching anyone down as a combat action, with the constable's kit and its consequences | new CS-33 | his ruling, advisor 376 |
| Can-yous beyond the big three, each checked for fun, fit and animation | new CS-34 | his principle, advisor 377 |
| Thirteen lines the outside questions asked for (thrown things' force, falls from height, a car door, a collar grab, losing, wronged people meeting, followers, suspicion adding up, a remembered noise, windows, searching a crowd, a bribed witness beaten, the sawn-off at the legs) | new CS-35 | RESULTS-30.md |
| Hand-over to Monday's people pass: inventories by role, owners' memory of their things, back-room and shop stock | COMBAT-SYSTEM.md, last section | his brief |

## Fixes from the fresh review (rev1-work/REVIEW-REV1.md, 15 findings, fixed once)

All fifteen taken: the knife-arm claim corrected and counted per side (a bat-against-knife fight added); the guard coin removed; the cosh second blow; the knock-down threshold; the reload check and the two stream draws; every stale number in CS-09, 10, 11, 14, 15, 18 re-quoted; legs now reached by low kicks and low thrusts; law marked unverified where the research says so (the 1953 Act's "in itself" weapons, the 1988 start date from Hansard, the revolver's certificate from a summary, the constable's kit) and the confirmed stop-and-search power no longer marked; the knife standard's shortfall said; the lamp distance; CS-02's "by chance"; the gun sway shown in Frank's arms, not on screen; the shove no longer multiplied by a held weapon and a breaking thing's last blow scored as the thing; the choke curve; the boot force; the knuckleduster knock-out from behind; guns disarmed by the grab; the gun death rate per man; this file.

## What moved in the simulator (seed 1990, 2,000 a scenario; first pass, then now)

| Number | First pass | Revision 1 |
|---|---|---|
| Careful 1 v 1 fists, won | 79% | 73% (94% of decided) |
| Masher 1 v 1, won | 19% | 11% |
| Careful 2 v 1, won | 29% | 29% |
| With Ron, won | 78% | 73% (95% of decided) |
| Fist fight deaths | 1 in 2,000 | 0 in 2,000 (open and kerb) |
| Knife used by Frank, deaths per 1,000 fights | 94 | 57.5 |
| Unarmed Frank against a knife man, won | 50% | 48%; with a bat aimed at the knife arm 77% |
| Finishing with boots, deaths per 1,000 | 15.5 | 31 kicking on regardless; 0 stopping at the cue |
| Finishing with a cosh to the head, deaths per 1,000 | 42 | 56.5 regardless; 1 stopping at the cue |
| Knock-outs per careful fist fight | 0.15 | 0.34 |
| Men yielding per careful fist fight | 0.39 | 0.26 |
| Dark doorway, takedown works | 58% crouched (23% broke free, 7% turned for no cause) | 99.6% careful, 24% crouching in blind |
| Unlit street, takedown works | 41% crouched | 86% careful (14% held back), 20% crouching in blind, 0% walking |
| Under a lamp | 18% crouched | 19% careful, 54% held back (the player sees it cannot be done) |
| By day | 15% walking | 7% careful, 12% walking |
| Choke, once reached unseen | broke free 17% of attempts | never, except a big fresh man against a winded Frank |
| Cosh from behind, once reached | out 6 in 10, death 1 in 200 | out every time, no death |
| Held choke, death at 60 s past | 40% | 20% |
| Revolver, body at 8 m | not simulated | hits 79%, kills 21% |
| Sawn-off, body at 3 / 10 / 20 m, kills | not simulated | 50% / 18% / 1% |

## The outside questions

20 clean questions (C01 to C20) re-judged and 10 new ones on zones, weapons and searching (N01 to N10, a fresh Opus writer who saw nothing), judged by a fresh Opus tester against the revised design (rev1-work/RESULTS-30.md): C set 8 answered, 11 weak, 1 unanswered (the first pass: 8, 12, 0); N set 7 answered, 3 weak, 0 unanswered. CS-35 and the CS-02 aim then answered every weak and unanswered point the tester listed; that is the designer's count, not re-judged.

## Research (dated 25 Nov 2026)

- Law (rev1-work/RESEARCH-LAW.md, a Sonnet reader, legislation.gov.uk enacted and point-in-time texts, Hansard): s.139 blades (fine only in 1990, folding under 3 inches exempt, good reason); s.141 and its Order (18 Jan 1989: knuckledusters, butterfly knives, swordsticks and the rest, no selling, private possession lawful); the 1959 Act (flick knives); the 1953 Act; no under-16 knife rule until 1 Jan 1997; firearms (revolver s.1, a shotgun under 24 inches outside the shotgun certificate, s.4 shortening, ss.16 to 18 life); 1990 police kit partly unverified. Not reached: the s.139 commencement order, the 1990 Schedule 6 terms, the 1953 Act's definition text.
- Wounds (rev1-work/RESEARCH-WOUNDS.md, a Sonnet reader, partial: about half the medical fetches were blocked from the cloud): two Swedish gunshot series (30-day mortality 13% and 17% of those reaching hospital; head and chest carry most early deaths; limbs few). Not reached: per-region percentages, shotgun range classes and pattern widths, limb function, facial scarring, blunt head and kick series. The zone and gun numbers are judgement in the research's direction, to read from the PC.

## Still open

- The gun, arm and leg figures and the sawn-off spread want the medical and ballistic sources the cloud could not reach.
- Melee and gun feel timings wait for the footage measuring (unchanged).
- The masher now wins 11% one-on-one (was 19%); his 12 Oct design wants skill to win most fights, which holds; tune by fighter kind if he wants a masher nearer one in five.
- The swap test, sends, growth and police procedure in the simulator (owed from the first pass).
- CS-35's thirteen lines are not re-judged by a fresh tester.
