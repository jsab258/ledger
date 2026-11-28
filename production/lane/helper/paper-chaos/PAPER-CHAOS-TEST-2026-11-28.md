# Paper chaos test of the LEDGER blueprint

28 November 2026, job 4: 105 schemes by seven temperaments, 527 steps, each traced to the blueprint. Detail in PART-1 to PART-7; re-check in RECHECK.md.

## What was found

66 of 105 schemes pass (63%): greedy 9, killer 7, schemer 11, talker 11, griefer 7, hoarder 11, patient 10 (each of 15).

Of 527 steps, 82% are handled by a part, 6% rest on a general rule alone, 6% are seams and 5% missing. No step needed a special case: every gap is a missing rule for a kind of thing.

The talk guards held completely, and fights, witnesses and police answered most killings end to end. The re-check kept 17 of 20 failing steps, corrected 3, and found decision 21 pointing to the wrong part (2.9.1).

## The ten worst seams

1. Nothing is destroyed and nothing public is mended: a broken lamp darkens a street for good (R03, R02, R11).
2. A weighted body deletes anyone, repeatably; disappearances never add up (K02).
3. After the ending rivals and Ellis freeze: the greedy round dominates, the town goes static (G04, P14).
4. Three hollow calls buy the best ending: 3.2.5 says honesty, RT2-04 counts calls (P05).
5. A true secret bites like a hook even when Frank could not know it; second runs become perfect bluffs (P13).
6. The water's edge contradicts itself: 4.2.4 against CS-16, 1.6.7 against 2.5.5 (R01, K01).
7. Act III has single points of failure: the fare book and the inspector (R05, R06).
8. Loyalty is a flag: Mickey's people would shield Ron's killer (K07).
9. Talk-only places: violence allowed in hospital with nowhere to act (K11); statements only at the station hold off a hurt witness (K12).
10. Decision 21's fare war is undesigned and the tobacco allowance never tightens (G02, G03).

## Easy wins

G03 tobacco within the gate; G04 the round after the ending; K02 the weighted body; K12 hospitalised witnesses; R03 the dark street; H01 unlimited storage; P05 the hollow friendship; P13 second-run bluffs.

## Rule-level fixes, ranked

1. One life for every object (law 2): room per place, stashing anywhere, a destroyed step with a replacer, public mending, body disposal as acts with traces, one water-edge rule, books as objects and records. Mends 14; changes the build.
2. How people weigh (laws 1 and 3): asks carry a weight, loyalty is a reading, a go-between carries the backer's menace, only fighting people answer a rumour by force, deceit is a deed, one disclosure rule in both brain modes, claims weighed by how the speaker could know, talk with several. Mends 8.
3. Property and trade (law 4): buildings and shares change hands, businesses set prices and sell goods, insurers are people, tenants are debtors. Mends 5; changes the build.
4. Frank's verbs equal everyone's (law 8): order any verb, plant a man, write a letter, act on a seated person, soft-edge scenes list their hand acts, anyone blocked answers by temper. Mends 6.
5. The town never stops learning (laws 4 and 5, G27): every repeat income has a learner, disappearances accumulate, adaptation runs after the ending. Mends 4, three of them easy wins; changes the post-ending build.
6. Police reach (laws 1 and 3): statements where the witness is; tips weighed, warrants next day. Mends 2.
7. Story reads the whole cast (law 7): a fallback for every role; the friendship reads what she holds. Mends 2.

Values only: tobacco hands, account takings, Garbutt's prices, gun stock, the kit response.

## Regression table

Every scheme is a regression test: when a fix lands, replay its steps and expect every mark to read H. Marks: H handled, H(rule) a general rule only, S seam, M missing. Step citations show the first parts named for each step; the part files give the full reasoning.

| Scheme | Temperament | Steps | Step verdicts (step, mark, where) | Q1 to Q3 | Verdict |
|---|---|---|---|---|---|
| G01 The fare grinder | Greedy | 6 | 1 H EC-01 3.4.1 3.4.3; 2 H 7.11; 3 H 2.7.1 RT-17; 4 H EC-03 2.15.1; 5 H 2.15.2; 6 H(rule) G20 decision 21 | Q1 no, Q2 yes, Q3 yes | pass. |
| G02 The fare war | Greedy | 5 | 1 M EC-01 RT-14; 2 S G20 decision 21 2.9.1; 3 M 2.15.3; 4 H 2.15.2; 5 S EC-12 2.7.7 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F07. |
| G03 Tobacco at the gate, for ever | Greedy | 6 | 1 S EC-07 1.1.4; 2 H 1.6.9 G13; 3 H EC-07 2.2.1; 4 H EC-07; 5 H EC-04 5.2; 6 S EC-07 G27 | Q1 no, Q2 no, Q3 no | fail Q3. Fixes: F02, F12. |
| G04 After the ending, the round pays for ever | Greedy | 6 | 1 H 3.1.4 RT2-04; 2 H RT2-21; 3 H RT2-21; 4 S EC-06 5.1 RT2-21; 5 H 2.17 EC-06; 6 S RT2-21 | Q1 no, Q2 yes, Q3 no | fail Q3. Fixes: F01. |
| G05 The landlord | Greedy | 6 | 1 M decision 16 G20; 2 M FIT-G8 2.7.8; 3 H(rule) decision 16; 4 S 2.8.2 RT-16; 5 S 2.7.1 2.7.2; 6 H(rule) G04 G26 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F04, F09. |
| G06 A lift a day | Greedy | 6 | 1 H 1.6.3 WI-P05; 2 H 2.2.1 1.4; 3 H 2.7.6; 4 H(rule) G27; 5 H(rule) G27 2.5.4; 6 H 2.7.5 | Q1 no, Q2 yes, Q3 yes | pass (the town's answer rests on G27 having no working values yet). |
| G07 The burnt caff | Greedy | 5 | 1 S 2.17 G05; 2 H CS-22 G18; 3 H(rule) G18; 4 M G18; 6 H 2.17 EC-04 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F03. |
| G08 The loan book | Greedy | 6 | 1 H EC-08 RT-14; 2 H EC-08 2.7.7; 3 H 2.8.2; 4 H EC-08; 5 H 5.3 2.5; 6 H 5.3 | Q1 no, Q2 yes, Q3 yes | pass. |
| G09 Cars for scrap | Greedy | 6 | 1 H 1.2.10; 2 H 2.2.3 1.2.6; 3 S 2.7.6; 4 H 1.2.10; 5 H 1.2.9 GV-02; 6 H 2.7.6 | Q1 no, Q2 no, Q3 yes | fail Q2. Fixes: F05. |
| G10 A hook a fortnight | Greedy | 5 | 1 H 2.8.1 RT-07; 2 H RT-07; 3 H EC-09; 4 H EC-09; 5 H 5.4 LH-15 | Q1 no, Q2 yes, Q3 yes | pass. |
| G11 Selling to the rivals | Greedy | 5 | 1 H 2.10.4 RT2-08; 2 S G04 G10; 3 H G03 WI-P06; 4 H(rule) G10 G08; 5 H 2.10.2 WI-P06 | Q1 no, Q2 yes, Q3 yes | pass. Fixes: F06 (price for information). |
| G12 The wash at its limit | Greedy | 4 | 1 H 2.7.3; 2 H 2.7.3; 3 H 2.7.3; 4 H 2.7.3 RT-01 | Q1 no, Q2 yes, Q3 yes | pass. |
| G13 Every account in town | Greedy | 5 | 1 H RT2-01 2.15.2; 2 H 2.15.2 EC-02; 3 S 2.15.2; 4 H 2.15.2; 5 H(rule) G20 | Q1 no, Q2 yes, Q3 yes | pass. Fixes: F12 (values only). |
| G14 Robbing the lock-ups | Greedy | 5 | 1 H 1.6.11 RT2-08; 2 H 1.6.1 G14; 3 H(rule) G14 RT2-08; 4 H 2.5.5 RT2-07; 5 H(rule) G27 | Q1 no, Q2 yes, Q3 yes | pass. |
| G15 Ellis on the payroll | Greedy | 6 | 1 H EC-11 2.6.8; 2 H EC-11; 3 H 2.6.8; 4 H 1.6.15 2.6.3; 5 H 5.7; 6 H EC-11 | Q1 no, Q2 yes, Q3 yes | pass. |
| K01 The witness on her walk | Killer | 7 | 1 H 2.5.1 1.4.5; 2 H 1.5.2; 3 H 1.3.7 2.2.1 2.5.3; 4 H CS-16 1.6.7; 5 H 1.3.5 decision 6; 6 S 1.6.7 2.5.5 C-354; 7 H CS-27 2.6.10 2.4.2 | Q1 no, Q2 no, Q3 yes | fail Q2. Fixes: F13. |
| K02 The weighted body | Killer | 7 | 1 H 1.3.6 RT2-11 2.2.3; 2 M; 3 H CS-16; 4 M 2.5.5; 5 H 2.5.5; 6 H CS-27; 7 S G27 CS-27 | Q1 no, Q2 no, Q3 no | fail Q2 and Q3. Fixes: F13, F14. |
| K03 The fire at the terrace | Killer | 7 | 1 H 1.6.6 1.4.4; 2 H CS-22; 3 H CS-22 G18; 4 H CS-22 1.3.7; 5 H CS-22 G18; 6 H GV-02; 7 H CS-27 | Q1 no, Q2 yes, Q3 yes | pass. |
| K04 Clear the caff | Killer | 8 | 1 H WI-P12 1.3.6; 2 H 2.5.3; 3 H 2.5.3; 4 H FIT-P18; 5 H 1.5.2 2.5.1; 6 H 1.4.3 2.2.1; 7 H RT2-10; 8 H CS-27 CS-17 G26 | Q1 no, Q2 yes, Q3 yes | pass. |
| K05 Kill Ellis | Killer | 5 | 1 H 2.1.1 G16; 2 H 1.6.11 2.2.3; 3 H LH-13 G19; 4 H LH-01 LH-02 LH-06; 5 H WI-P02 RT2-16 | Q1 no, Q2 yes, Q3 yes | pass. |
| K06 The fare who saw the envelope | Killer | 6 | 1 H 3.4.3 G13; 2 H GV-01 2.2.1; 3 H(rule) G20; 4 M 1.2.10; 5 H 1.3.7 1.3.5; 6 H(rule) G13 LH-04 | Q1 no, Q2 no, Q3 yes | fail Q2. Fixes: F20. |
| K07 Kill Ron | Killer | 5 | 1 H 3.6.1 2.1.1; 2 H RT2-11 1.3.6; 3 H RT2-05 G22 decision 8; 4 H 2.3.1 2.4; 5 S 2.5.2 LH-04 | Q1 yes, Q2 no, Q3 no | fail Q1. Fixes: F19. |
| K08 The ordered killing | Killer | 5 | 1 S 1.7.2 RT-14; 2 H(rule) G10; 3 H 1.7.2; 4 H RT2-11 G19; 5 H 2.5.5 CS-27 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F15. |
| K09 The allotment grave | Killer | 6 | 1 H 3.6.1 G01; 2 H 1.3.6 RT2-11; 3 H CS-16 1.1.4; 4 M 2.5.5; 5 H 2.5.5 2.10.2 G10; 6 H 2.5.5 4.11.1 | Q1 no, Q2 no, Q3 yes | fail Q2. Fixes: F13. |
| K10 Three heads in a row | Killer | 5 | 1 H RT2-08 RT2-11; 2 H RT2-05; 3 H G19; 4 H WI-P02; 5 H RT-12 2.4.2 G26 | Q1 no, Q2 yes, Q3 yes | pass. |
| K11 The witness in hospital | Killer | 4 | 1 H WI-P11 2.3; 2 H WI-P11; 3 S WI-P11 RT-15; 4 H WI-P11 | Q1 yes, Q2 no, Q3 no | fail Q1. Fixes: F17. |
| K12 The car, then the bed | Killer | 5 | 1 H 1.2.5 FIT-P04; 2 H RT2-16 2.4.2; 3 H 1.3.11; 4 S 2.6.3 LH-04; 5 H 2.6.3 WI-P07 | Q1 no, Q2 no, Q3 no | fail Q2 and Q3. Fixes: F18. |
| K13 The held man | Killer | 5 | 1 H G17 decision 1; 2 H G17 1.6.1; 3 H G17 2.5.5; 4 H G19; 5 H CS-16 2.5.5 2.6.9 | Q1 no, Q2 yes, Q3 yes | pass. |
| K14 Kill and frame | Killer | 6 | 1 H CS-32 LH-06; 2 H G13 decision 12 1.7.2; 3 H LH-06 G13; 4 H CS-27; 5 H decision 24; 6 H CS-32 LH-04 | Q1 no, Q2 yes, Q3 yes | pass. |
| K15 The constable in the dock | Killer | 6 | 1 H LH-01; 2 H CS-16; 3 H LH-01; 4 H LH-02 LH-06; 5 H LH-07 LH-09; 6 H LH-10 | Q1 no, Q2 yes, Q3 yes | pass. |
| S01 The canary | Schemer | 6 | 1 H G01 3.6.1; 2 H G01 2.3.1; 3 H WI-P06 2.4.1; 4 H 2.10.2 G10; 5 H 1.7.3 1.6.11; 6 H WI-P06 2.11 G10 | Q1 no, Q2 yes, Q3 yes | pass. |
| S02 The paid talker | Schemer | 7 | 1 H G01 G04; 2 H 2.4.1 2.3.1; 3 H G03; 4 H 2.6.5 G16; 5 H G03 3.6.2; 6 H 3.1.6 law 7; 7 H 2.3.1 LH-15 | Q1 no, Q2 yes, Q3 yes | pass. |
| S03 The false grass | Schemer | 5 | 1 H G01 3.6.1; 2 H 2.4.1; 3 S decision 4 G27 decision 37; 4 H G01 2.3.1; 5 H 3.5.2 G08 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F22. |
| S04 The decoy row | Schemer | 6 | 1 H G04; 2 H 2.5.3 1.3.4; 3 H 2.5.3 2.6.10; 4 H 1.6.1 1.4.8; 5 H 2.6.4 G03 G10; 6 H 2.5.5 | Q1 no, Q2 yes, Q3 yes | pass. |
| S05 The coat double | Schemer | 6 | 1 H G04 1.6.10; 2 H 1.7.3; 3 H 2.2.2 2.3.2; 4 H 2.2.2; 5 H G03; 6 H LH-04 G03 | Q1 no, Q2 yes, Q3 yes | pass. |
| S06 The anonymous tip | Schemer | 5 | 1 H RT2-19; 2 S RT2-19 2.6.10; 3 M; 4 H G13; 5 H 2.6.9 2.10.2 | Q1 no, Q2 no, Q3 yes | fail Q2. Fixes: F21. |
| S07 The letter | Schemer | 4 | 1 M 2.4.5 G21; 3 H(rule) G03 G01; 4 H 2.4.1 2.10.2; 5 H 2.10.3 | Q1 no, Q2 no, Q3 yes | fail Q2. Fixes: F23. |
| S08 The go-between round | Schemer | 6 | 1 H 2.11.1; 2 H decision 33 2.17; 3 S 2.17 EC-06; 4 H(rule) G10; 5 H 2.17; 6 H LH-04 2.6.5 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F24. |
| S09 The turned lieutenant | Schemer | 6 | 1 H WI-P06; 2 H 3.6.1 RT-14; 3 H WI-P06; 4 H WI-P06 RT-07; 5 H WI-P06 RT2-07; 6 H(rule) G22 RT2-05 | Q1 no, Q2 yes, Q3 yes | pass. |
| S10 Playing the Widow against Cammack | Schemer | 5 | 1 H WI-P06 G01; 2 H WI-P06 G03; 3 H WI-P06 G08; 4 H(rule) G10 G08; 5 H WI-P06 | Q1 no, Q2 yes, Q3 yes | pass. |
| S11 The constable who listens | Schemer | 4 | 1 H 2.6.8; 2 H(rule) G16 G04; 3 H 3.6.2 G16; 4 H G16 LH-08 | Q1 no, Q2 yes, Q3 yes | pass. |
| S12 The patsy | Schemer | 6 | 1 H 1.6.9 1.1.4; 2 H G13 decision 12 1.7.2; 3 H G13; 4 H 2.6.9 G13; 5 H decision 24; 6 H 2.5.2 | Q1 no, Q2 yes, Q3 yes | pass. |
| S13 The man who takes the charge | Schemer | 6 | 1 H G04; 2 H 4.3.7 2.6.4; 3 H G03; 4 H 2.6.9 decision 15; 5 H LH-15; 6 H G04 | Q1 no, Q2 yes, Q3 yes | pass. |
| S14 The planted story | Schemer | 5 | 1 H 3.2.7; 2 H G01 G03; 3 H 2.4.5; 4 H 2.4.5 2.4.1; 5 H G01 3.2.5 | Q1 no, Q2 yes, Q3 yes | pass. |
| S15 Through the Fixer | Schemer | 5 | 1 H RT2-19 2.10.4; 2 H 2.10.4; 3 H(rule) G04 2.10.4; 4 H(rule) G03; 5 H 2.10.4 | Q1 no, Q2 yes, Q3 yes | pass. Fixes: F12 (Garbutt's prices). |
| T01 The steering line | Talker | 4 | 1 H RT-14; 2 H RT-15; 3 H 3.6.2; 4 H RT-14 2.3.1 | Q1 no, Q2 yes, Q3 yes | pass. |
| T02 The claimed act | Talker | 4 | 1 H RT-14; 2 H RT-15; 3 H RT-15 2.14; 4 H law 8 1.6.3 WI-P12 | Q1 no, Q2 yes, Q3 yes | pass. |
| T03 The future and the real world | Talker | 3 | 1 H RT-15; 2 H 3.6.2; 3 H 3.6.2 | Q1 no, Q2 yes, Q3 yes | pass. |
| T04 Charm at the till | Talker | 5 | 1 H RT-14 G04; 2 H 2.14.1; 3 H 2.14 G26; 4 H G04; 5 H RT-15 | Q1 no, Q2 yes, Q3 yes | pass. |
| T05 Talking a witness round without menace | Talker | 5 | 1 H 2.6.3 1.4.5; 2 H 2.5.2; 3 H 2.14.1; 4 H 2.5.2; 5 H WI-P07 | Q1 no, Q2 yes, Q3 yes | pass. |
| T06 The impostor detective | Talker | 6 | 1 H decision 13 CS-33 G11; 2 H G03; 3 H(rule) G04 G03; 4 M G19 CS-19 2.6.9; 5 H G03; 6 M | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F27. |
| T07 The talked robbery | Talker | 5 | 1 H RT-14; 2 H G03 RT-07; 3 H 2.5.2 WI-P12; 4 H 2.14.1; 5 H(rule) G19 WI-P05 2.5.3 | Q1 no, Q2 yes, Q3 yes | pass. |
| T08 The hired arsonist | Talker | 5 | 1 H RT-14; 2 S G04; 3 H CS-22 G18; 4 H LH-04 LH-15; 5 H 2.5.2 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F25. |
| T09 Talking to three at once | Talker | 4 | 1 H 3.6.1; 2 M 3.5.5; 3 H WI-P06; 4 H WI-P06 2.10.2 | Q1 yes, Q2 no, Q3 unclear | fail Q1. Fixes: F26. |
| T10 Talking out of an arrest | Talker | 5 | 1 H 2.6.4; 2 H WI-P08; 3 H 2.6.3; 4 H G03 LH-06; 5 H 2.14.1 | Q1 no, Q2 yes, Q3 yes | pass. |
| T11 Talking Ellis round | Talker | 4 | 1 H G16; 2 H G03 3.6.2; 3 H 2.6.5; 4 H G03 WI-P08 | Q1 no, Q2 yes, Q3 yes | pass. |
| T12 The endless asker | Talker | 5 | 1 H RT-14 2.7.3; 2 H 2.14.1; 3 H G04; 4 H RT-15; 5 H 3.6.1 8.6 | Q1 no, Q2 yes, Q3 yes | pass. |
| T13 Courting past the limits | Talker | 4 | 1 H G06; 2 H decision 20 RT-15; 3 H RT-15; 4 H 3.2.5 3.2.7 | Q1 no, Q2 yes, Q3 yes | pass. |
| T14 The bluffed hook at a sit-down | Talker | 5 | 1 H 3.5.5; 2 H RT-07; 3 H G03 G05; 4 H 2.14.1; 5 H G03 | Q1 no, Q2 yes, Q3 yes | pass. |
| T15 Pumping for a confidence | Talker | 4 | 1 H RT-14; 2 S G26 TALK-09 2.14; 3 H(rule) G26; 4 H 3.6.2 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F28. |
| R01 The cab off the quay | Griefer | 4 | 1 H 4.2.4; 2 H CS-16 GV-01; 3 S CS-16 4.2.4; 4 H CS-16 G13 | Q1 yes, Q2 no, Q3 no | fail Q1. Fixes: F30. |
| R02 Burn the fleet | Griefer | 5 | 1 H CS-22 G18; 2 H for car two RT2-06, M for the others 1.2.9; 3 H 2.15 RT2-04; 4 H EC-03; 5 H CS-22 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F31. |
| R03 Dark street | Griefer | 5 | 1 H 1.3.5 G19; 2 H 2.2.3; 3 M; 4 H(rule) G27; 5 H 2.2.1 | Q1 no, Q2 no, Q3 no | fail Q2 and Q3. Fixes: F31. |
| R04 No phones | Griefer | 4 | 1 H G19 RT2-19; 2 H 2.5.1; 3 M; 4 H 2.5.5 2.6.3 | Q1 no, Q2 no, Q3 yes | fail Q2. Fixes: F31. |
| R05 Burn the book | Griefer | 3 | 1 H 1.6.8 G13; 2 M RT-01 RT2-04; 3 S RT-01 | Q1 yes, Q2 no, Q3 no | fail Q1. Fixes: F32. |
| R06 Kill the inspector | Griefer | 4 | 1 H 3.1.3 2.1.1; 2 H G19; 3 H CS-27; 4 S G22 RT2-05 WI-P02 | Q1 yes, Q2 no, Q3 no | fail Q1. Fixes: F33. |
| R07 Striking his own | Griefer | 4 | 1 H WI-P01; 2 H WI-P01 2.11; 3 H 2.4.1 GV-06 G26; 4 H G10 | Q1 no, Q2 yes, Q3 yes | pass. |
| R08 Arrested thirty times | Griefer | 4 | 1 H 2.6.3; 2 H 2.6.4 7.9; 3 H 2.6.9 2.6.5; 4 H 2.5.4 | Q1 no, Q2 yes, Q3 yes | pass. |
| R09 Doing nothing | Griefer | 6 | 1 H 7.11; 2 H RT-16; 3 H 2.15; 4 H 7.4 3.1.3; 5 H 7.12; 6 H 3.1.4 | Q1 no, Q2 yes, Q3 yes | pass. |
| R10 The blocked door | Griefer | 3 | 1 H 1.7.4 2.1.1; 2 S 8.10; 3 H 2.7.3 | Q1 yes, Q2 no, Q3 no | fail Q1. Fixes: F29. |
| R11 The tin in the dock | Griefer | 3 | 1 H 1.1.4; 2 S 4.2.4 2.7.2; 3 H 2.7.7 | Q1 yes, Q2 no, Q3 yes | fail Q1. Fixes: F31. |
| R12 Giving it all away | Griefer | 4 | 1 H G04 2.7.7; 2 H G26 2.4.1; 3 H RT-16; 4 H decision 17 EC-01 | Q1 no, Q2 yes, Q3 yes | pass. |
| R13 The yard dog | Griefer | 3 | 1 H 4.11.1; 2 H 4.11.1; 3 H 4.11.1 | Q1 no, Q2 yes, Q3 yes | pass. |
| R14 The noon spree | Griefer | 6 | 1 H 1.3.6 2.5.3; 2 H 2.5.3; 3 H 2.6.3 RT2-03; 4 H LH-07 LH-09; 5 H 7.9; 6 H 3.1.4 decision 29 | Q1 no, Q2 yes, Q3 yes | pass. |
| R15 Reloading for luck | Griefer | 4 | 1 H 7.8; 2 H FIT-P18; 3 H 1.3; 4 H 1.3.5 1.7.4 | Q1 no, Q2 yes, Q3 yes | pass. |
| H01 The radio hoard | Hoarder | 7 | 1 H 1.6.3 WI-P05; 2 H 1.6.9 1.1.4; 3 M 1.6.9; 4 H 2.4.2 2.7.6; 5 H 2.7.6 2.7.5; 6 H 1.6.3; 7 H 2.6.9 | Q1 no, Q2 no, Q3 no | fail Q2. Fixes: F36. |
| H02 The stash under the boards | Hoarder | 4 | 1 H 1.6.1 G14; 2 M G13; 3 M; 4 H 2.2.1 2.5.5 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F36. |
| H03 The painted cars | Hoarder | 5 | 1 H 1.2.10; 2 H 1.2.9; 3 M; 4 S G13 1.2.9; 5 H G13 RT2-16 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F37, F36. |
| H04 The gun cupboard | Hoarder | 6 | 1 H RT2-14; 2 H RT2-14; 3 H 1.6.9; 4 H 1.3.10 RT2-14; 5 H 2.6.9; 6 H RT2-14 | Q1 no, Q2 yes, Q3 yes | pass. Fixes: F12 (the seller's stock). |
| H05 Trophies | Hoarder | 6 | 1 H CS-33; 2 H WI-P05; 3 H 1.6.9; 4 H G13; 5 H 2.6.9 G13; 6 H GV-06 G26 | Q1 no, Q2 yes, Q3 yes | pass. |
| H06 The letter collector | Hoarder | 5 | 1 H 1.6.13 decision 12; 2 H 2.4.5; 3 H(rule) G05 FIT-P52; 4 H G13 1.6.13; 5 H RT-07 EC-09 | Q1 no, Q2 yes, Q3 yes | pass. |
| H07 The corner on cigarettes | Hoarder | 5 | 1 H 2.7.5 FIT-G8; 2 M; 3 M EC-07; 4 H 2.7.5 EC-04; 5 H EC-04 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F07, F36. |
| H08 The ironmonger's knives | Hoarder | 4 | 1 H CS-29 CS-32; 2 H CS-32 LH-04; 3 H 2.7.5; 4 H 1.6.9 | Q1 no, Q2 yes, Q3 yes | pass. |
| H09 Taking back what he sold | Hoarder | 5 | 1 H 2.7.6 EC-10; 2 H 1.6.1; 3 H G14; 4 H G13 2.7.6; 5 H 2.5.2 | Q1 no, Q2 yes, Q3 yes | pass. |
| H10 The constable's kit | Hoarder | 5 | 1 H LH-13 RT2-02; 2 H CS-33; 3 H 1.6.9; 4 H 2.6.10; 5 H RT2-16 | Q1 no, Q2 yes, Q3 yes | pass. Fixes: F12 (the size of the rise). |
| H11 A key to every door | Hoarder | 5 | 1 H 1.6.1; 2 H G04; 3 H 1.6.1 G14; 4 H(rule) G27; 5 H G13 LH-04 | Q1 no, Q2 yes, Q3 yes | pass. |
| H12 The tin as a bank | Hoarder | 6 | 1 H 2.7.2; 2 H RT-17; 3 H 2.7.2; 4 H 2.7.2 G10; 5 H 2.6.9; 6 H RT-01 | Q1 no, Q2 yes, Q3 yes | pass. |
| H13 A fleet with no drivers | Hoarder | 4 | 1 H EC-03; 2 H 2.15.1 EC-02; 3 H EC-03 2.7.4; 4 H 2.15.2 | Q1 no, Q2 yes, Q3 yes | pass. |
| H14 The rival's stock in his shed | Hoarder | 6 | 1 H RT2-08 1.6.1; 2 H 1.1.4 GV-01; 3 H 1.6.9; 4 H G13; 5 H 2.10.2 RT2-07; 6 H(rule) G10 | Q1 no, Q2 yes, Q3 yes | pass. |
| H15 Lost property | Hoarder | 4 | 1 H(rule) G13; 2 H RT-17; 3 H(rule) G13 3.4.3; 4 H G01 G26 | Q1 no, Q2 yes, Q3 yes | pass. |
| P01 Seven weeks of clean books | Patient | 5 | 1 H 2.7.3; 2 H 2.7.3; 3 H 2.7.2; 4 H RT-01; 5 H RT2-04 | Q1 no, Q2 yes, Q3 yes | pass. |
| P02 Regard before the round | Patient | 5 | 1 H G07; 2 H G26 2.14; 3 H 2.17 EC-06; 4 H 2.17 G04; 5 H 2.17 | Q1 no, Q2 yes, Q3 yes | pass. |
| P03 A man inside the Widow's crew | Patient | 5 | 1 H 2.11.1; 2 M G10 WI-P06; 3 H(rule) G10 WI-P06; 4 M; 5 H WI-P06 | Q1 no, Q2 no, Q3 yes | fail Q2. Fixes: F38. |
| P04 Waiting out Ellis | Patient | 6 | 1 H 7.11 2.15; 2 H RT-13 2.6.5; 3 H 2.4.2; 4 H RT-12; 5 H RT-05 2.10.3; 6 H RT2-08 2.5.5 | Q1 no, Q2 yes, Q3 yes | pass. |
| P05 The hollow friendship | Patient | 5 | 1 H 3.2.7; 2 H G01 G03; 3 H 2.4.1 2.3.2; 4 S 3.2.5 RT2-04; 5 H RT2-04 | Q1 no, Q2 no, Q3 no | fail Q2 and Q3. Fixes: F39. |
| P06 Courting Ellis | Patient | 5 | 1 H G06 decision 31; 2 H G06; 3 H G06; 4 H 2.6.5 RT-13; 5 H G06 | Q1 no, Q2 yes, Q3 yes | pass. |
| P07 Saving for the contract | Patient | 4 | 1 H 2.7.1 RT-17; 2 H EC-03; 3 H RT2-01 2.15.2; 4 H RT2-01 | Q1 no, Q2 yes, Q3 yes | pass. |
| P08 Owning debts | Patient | 4 | 1 H(rule) G04; 2 H(rule) G04 2.8.2; 3 H G04; 4 H 2.8.2 | Q1 no, Q2 yes, Q3 yes | pass. |
| P09 The innocent man, timed | Patient | 5 | 1 H decision 24 2.6.9; 2 H decision 24 G26; 3 H 2.4.2; 4 H WI-P07; 5 H(rule) WI-P07 2.6.9 | Q1 no, Q2 yes, Q3 yes | pass. |
| P10 The truce kept for the end | Patient | 4 | 1 H 2.10.4; 2 H RT-05; 3 H 2.10.4; 4 H 3.1.3 | Q1 no, Q2 yes, Q3 yes | pass. |
| P11 His own routine as cover | Patient | 4 | 1 H G23; 2 H 1.4 2.2.3; 3 H G03; 4 H(rule) G23 G03 | Q1 no, Q2 yes, Q3 yes | pass. |
| P12 The building bought early | Patient | 3 | 1 M; 3 S 2.17; 4 H 2.17 2.7.3 | Q1 no, Q2 no, Q3 unclear | fail Q2. Fixes: F04. |
| P13 The second run | Patient | 4 | 1 H G30; 2 H G01 RT-07; 3 S RT-07 G03; 4 H G05 | Q1 yes, Q2 no, Q3 no | fail Q1. Fixes: F40. |
| P14 The months after | Patient | 5 | 1 H RT2-21; 2 H RT2-21; 3 H RT2-21; 4 H 7.12; 5 S RT2-21 G27 G28 | Q1 no, Q2 yes, Q3 no | fail Q3. Fixes: F01. |
| P15 Weeks of playing them off | Patient | 5 | 1 H WI-P06 G01; 2 H WI-P06 G08; 3 H RT2-07 2.10.1; 4 H 3.5.5; 5 H WI-P06 G03 | Q1 no, Q2 yes, Q3 yes | pass. |

## Fix numbers behind the ranking

1: F05, F13, F30, F31, F32, F36, F37. 2: F19, F22, F24, F25, F26, F27, F28, F40. 3: F03, F04, F06, F07, F09. 4: F15, F17, F20, F23, F29, F38. 5: F01, F02, F14. 6: F18, F21. 7: F33, F39. Values: F12. Each is written out in the fix register at the end of its part file, with its law.
