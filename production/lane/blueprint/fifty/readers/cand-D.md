# Candidate D: hidden details and gaps (reader's pass on the blueprint data, 24 Nov 2026)

Read: data/SUMMARY.md, DATA-BUILD-STATUS.md, the player-facing data files (sampled), what-if SUMMARY/LONG-HEAT/PROPOSED-PARTS, reality-check SUMMARY, BLUEPRINT-11 structure and gaps. Nothing changed. Paths below are inside production/lane/blueprint/.

Key. "Designed" = the figure or wording is exact in the data and not marked provisional, pending or owed. "Partly" = the data holds the detail but a number is chosen (working value), pending footage, owed, or a word is "TO WRITE" or marked story_check.

## Part 1. Candidate hidden details (46)

### The Ledger and what Frank is called

1. Frank never sees a rung number, but the street calls him "the new owner", then "Nowak", then "Frank", then "Frankie" as it warms to him. File: data/cast.json name_ladder; data/ledger-texts.json people_call_ladder; data/line-situations.json (greeting.owner, greeting.nowak, greeting.frank). Designed.
2. Frank's Ledger writes "Nobody saw." two game minutes after an act goes unseen, then strikes it through the moment someone turns up: "{Name} knows." File: data/ledger-texts.json day_book (db_unseen, db_unseen_late); clock_figures. Designed (2 game minutes; the 4 real seconds is derived from the 120 s hour).
3. The Ledger grades a witness in plain words: "saw a shape: a man, about his size", "saw a mark: the coat, the cab, a limp", "saw his face, and does not know his name", "knows it was him". File: data/ledger-texts.json people_recognition_lines. Designed.
4. Every act is written in seven slots (what led up to it, what he took out, the act, victim, actor, flight, aftermath), so a witness who only "may have seen what he took out" is recorded differently from one who saw it done. 116 act kinds. File: data/ledger-texts.json kinds, slot_names, belief_lines. Designed (wording of many slots marked chosen).
5. Frank writes only what he saw, in his own clipped past tense ("Came off the ferry with one suitcase"), never another person's mind, never a meter or colour. File: data/ledger-texts.json voice, kinds[arrive]. Designed.
6. The end of the story is read from signs, not a bar: "The inspector read a line twice." then "The inspector has stopped being courteous." File: data/ledger-texts.json signs (insp_nod, insp_twice, insp_cold); reading. Designed (wording; story_check on the pen-laid-on-the-book line).
7. The Ledger's open list says "Tonight, before the last ferry" and "Said yes / Said no / The time passed" for the same Monday bag job, so a job lapses visibly. File: data/ledger-texts.json open_items (open_ask1, open_job1). Designed.

### Print, post and the town's paper

8. Mickey's will letter ends "Sheila knows the book. Ron knows the door." and sits in the Ledger from the first read in the flat. File: data/letters-and-print.json letters (letter_mickey_will). Partly (wording chosen; the story frame may replace it).
9. The Meridian Pilot is 25p, comes out Tuesday and Friday, 14 issues from Tue 16 Oct to Fri 30 Nov, and the headlines follow the weeks (berths closing, the poll tax meeting, the march, "THE HOOK GATE TO BE CHAINED TOMORROW"). File: data/letters-and-print.json paper.issues. Designed (some items story_check).
10. The paper words a story about Frank by how sure the reporter is: "states it plainly" when Alison saw it, "is understood to" from one other, "several people say", "it is said" for rumour, "police say" / "the court heard" for the law. File: data/letters-and-print.json paper.strength_wording. Designed.
11. Alison only prints what she knows: every item carries a source_fact and an alison_knows, so a thing she was never told never appears in the paper. File: data/letters-and-print.json paper.rules. Designed.
12. Rent falls apart on a fixed ladder: a card on the counter ("Nobody to take the rent. £18 due"), then £36 arrears, a 14-day notice to quit, then "The flat over 1 Quay Street has been let", and a receipt that withdraws the notice if he pays. File: data/letters-and-print.json letters (letter_rent_card to letter_rent_cleared). Designed.
13. The council letters about the licence all hang off one hearing date (default Thursday 15 November, 10.30, the Town Hall), at minus 14, 10 and 7 days, and the paper prints the same date. File: data/letters-and-print.json licence_schedule. Partly (the date is set by the story state; story_check).
14. A tax inspector calls on Monday 26 November at nine and each morning asks for one more book: the fare book, the car logs, the wages book, one account, week one, with a verdict at five on the last day. File: data/letters-and-print.json letters (letter_vat, letter_vat_m1 to m5, letter_vat_result_*). Designed (story_check).
15. Frank's mail: Ellis's card ("Ring me. C.E."), Alison's ("Rang twice. I would like five minutes about the fire"), Cammack's ("Nice cars. Pity about the rank. D.C.") and the Widow's slip to a driver ("Dock gate. Car 3. £5 received. Weekly, Friday. M.J."). File: data/letters-and-print.json letters (note_*). Designed.
16. Mickey's fare card on the counter reads 80p to start, £1.10 a mile, a quarter more nights and Sundays, waiting 20p a minute after five. File: data/letters-and-print.json print.cab_office. Partly (the reality check says this is above 1990 rates; the tariff waits on his answer).
17. The chalk board in the office shows "CAR 1 KEVIN DAYS ... CAR 3 (on terms) CAR 4 (open)" and fills up as cars are bought; car two's keys are always on it. File: data/letters-and-print.json print.cab_office (print_cab_board); data/vehicles.json firm_fleet. Designed (chosen).
18. Shop signs carry opening hours built from the town's real opening times, so a plate can never disagree with the shop; and the launderette's board "LAST WASH 10.30 PM" changes to 16:30 from Friday 16 November (a machine is out of order). File: data/letters-and-print.json print.hours_plate_rule, price_boards; data/timetables.json events (washeteria_last_wash). Designed.
19. Prices are real and small: tea 30p, breakfast £1.80, the Pilot 25p, 20 Ashcombe £1.70, keys cut £1.50, "FISH & CHIPS £1.60". File: data/letters-and-print.json print.price_boards. Designed (chip shop items chosen).
20. The graffiti tags TANNER, SNIDE and GULL are district wall names, not the three rival firms, and "NO POLL TAX" is chalked on the Hook. File: data/letters-and-print.json print.graffiti. Designed.
21. The phone box reads "LOCAL CALLS 10p ... EMERGENCY: DIAL 999, NO COIN NEEDED ... FAULTS: DIAL 151" under a made-up operator, Tidewire. File: data/letters-and-print.json print.phone_box. Designed.

### The town's calendar

22. The game opens on Monday 15 October in drizzle with a wet street, and the weather is the same on every run of the same seed; it is never sunshine. File: data/light-weather.json weather.spells (opening_weather, same_seed_same_weather), weather.never_sunshine. Designed (from the prototype).
23. The clocks go back at 02:00 on Sunday 28 October and Frank plays 01:00 to 02:00 twice; night people just stay where they are. File: data/light-weather.json clock_change. Designed (chosen).
24. Street lamps do not switch on together: each strikes up to six minutes apart, glows red first and takes about 12 game minutes (24 real seconds) to reach full sodium yellow. File: data/light-weather.json lamp_rule (individual_strike_jitter, warm_up_curve). Partly (the 8 to 15 minute range is sourced; the curve and the 70/35 lux switch points are chosen).
25. Sunrise and sunset for every day of the story come from the NOAA equations, rechecked by a reviewer to within two minutes. File: data/light-weather.json days (49 rows), sun_anchors. Designed (the latitude is a stand-in; canon names none).
26. Quay Street is closed to traffic on Sunday 4 November from 8 to 6 for the gas main, and householders move their cars off on the Saturday night. File: data/timetables.json calendar (gas_main_cars_off, quay_street_closed_gas_main). Designed.
27. Bonfire Night (Monday 5 November) puts adults on the waste ground behind Basin Top and the display on the quay from 19:30 to 20:00; nobody under 18 anywhere. File: data/timetables.json events (bonfire_night_*); data/crowd.json events (ev_bonfire_*). Designed (dates); partly (crowd counts provisional).
28. On Remembrance Sunday the street goes silent at 11:00 for two game minutes, about four real seconds. File: data/timetables.json events (remembrance_sunday); data/crowd.json events (ev_remembrance). Designed (silence); partly (crowd counts).
29. The poll-tax march on Saturday 10 November draws the Hook's adults out to the Exchange from ten, so the shops and street run quiet; the Thursday market cuts shop trade to two thirds. File: data/timetables.json events (poll_tax_march), calendar (shops_daytime_multiplier 0.67). Designed.
30. Saturday matches name their visitors (Thornwick Town, Fenby Albion, Saltmarsh Athletic, Northwold Rangers) and double Quay Street at kick-off and full-time. File: data/timetables.json calendar match; data/crowd.json events (ev_match_1500, ev_match_1700). Designed (fixtures); partly (counts).

### The police

31. The night constable walks the same route every night, starting from Quay Street's foot at 22:00, so two runs from one save are identical; one circuit takes about 7 real minutes, so a learner can time it. File: data/police.json beat_constable (night, cycle_nodes). Partly (route exact; walking speed 1.1 m/s pending footage, sight rule chosen).
32. After a deed, an officer stays at the spot for an hour, the ground within 24 m is watched until 07:00, a body gets blue-and-white tape until noon, and Ellis calls at nine next morning; the beat then detours past the spot twice a cycle for two nights. File: data/police.json after_a_deed. Partly (taken from the prototype; response times chosen).
33. The police remember by what was perceived: a hit-and-run stays hot three days, a struck officer seven, a killing never cools; a noted plate is known for good, and fresh plates only help against witnesses who have not told yet. File: data/police.json memory_and_description; data/vehicles.json witness_slot_for_the_car. Designed.
34. A constable can be bought, once: PC Trevor Garton looks away from a car for £50, a detective constable loses one statement for £200; a colleague who sees the money keeps it for good; it must be paid from cash. File: data/police.json bought_officers. Designed (the prices are the economy's; uses once).
35. Ellis arrives in stages, first only as a name: "There was a woman in asking about your lot. Ellis, her name was." Later Sheila warns him the office will be searched, with 12 game hours' notice. File: data/police.json ellis.stages. Designed.
36. The police panda is white with a broad blue band, POLICE on doors and bonnet, no Battenburg, no force name, plate G227 PMK, and a made-up make (Harwick Thorne) that no other car in the Hook shares. File: data/vehicles.json special_vehicles (patrol_panda). Designed.
37. Plates follow the 1990 letter scheme: an H plate is under three months old, a G car under a year, tired traffic carries the old suffix style. File: data/vehicles.json plates. Designed.
38. The boot is a seen act: opening it takes 1.5 s, writes the same seven Ledger slots as any act, a body goes in in 4 s, and a stop with cause searches it. File: data/vehicles.json boot. Partly (slot counts chosen).

### The people

39. Every named person walks a week of rows between real doors, and the ties file says where two of them are in the same place at the same time (Ron and Sheila at Laverack's at noon, Monday to Saturday). 118 routines, 147 ties. File: data/routines.json; data/ties.json. Designed (some times chosen).
40. A crime is first found by whoever's routine passes it: Eddie Birtwhistle on the fish dock at 04:45, Bill Huxtable at 05:05, the cleaner Edna Coulson at six for Mickey's door. File: data/routines.json finders. Designed.
41. Small people with small facts: Tadeusz Wrona at the ironmonger's is the only man on the Hook who says "Nowak" right first time, and corrects the others; Maggie Firth sees the landing all night and says it is none of hers; Harold Stead tells the cab driver the tide. File: data/people/tadeusz_wrona.json, maggie_firth.json, harold_stead.json (card). Designed.
42. Keith Garbutt the Fixer is paged from a box and rings that box back within half a game hour; he sells true reads, a meeting that then happens, and one truce a game. File: data/people/keith_garbutt.json (card). Designed.
43. Fares come with a person and a wrinkle (talker, parcel, tail, runner, wait, hurry, face), never the same wrinkle twice running: Arvids Ozols wants "To nowhere, please. One hour." and pays in tinned fish; Wayne Harrison says "See Metcalfe's van? Stay behind it. Not close."; Susan Coverdale says "Mr Agar asks after the firm". File: data/fares.json fare_people, rules. Designed (lines written for a few; most are TO WRITE).
44. Father Walsh's first fare says "Your uncle drove me this road a hundred times. He never once let me pay." File: data/fares.json (brendan_walsh.1). Designed.
45. Darren's tip about Iveson's £80 debt: the money is in a tin box in the hut, the lad chains the gap at five, "Not that I'm telling you anything." File: data/jobs/debt_iveson.json; data/letters-and-print.json note_darren. Designed (the debt amount; lines partly TO WRITE).
46. Ron's driving lessons run one to five; in lesson one Frank has the handbrake and one word, "Stop"; a man with four lessons can bring the car round at the Landing. File: data/jobs/ron_lessons.json. Designed (structure); partly (words TO WRITE; the save-state rule is a gap, see Part 2).

## Part 2. Digest of gaps a player would notice (56 lines, worst first)

BUILD = closing it changes the system, a rule or a data structure. CONTENT = only adds writing or assets. VALUES = a number is owed and the build stays the same once it is measured. Ids are BLUEPRINT-11 part ids, or the file named.

1. The long heat (killing a constable, any killing charge, remand, committal) is designed in what-if/LONG-HEAT.md (LH-01 to LH-14) but not folded into BLUEPRINT-02 2.6 and 2.16; the data has no squad, remand or committal rows. BUILD (new system).
2. No story director: nothing chooses which eligible beat plays when (30-minute rule, one heavy beat a game week, rest beats). BLUEPRINT-11 keeper run 5, 7.4 (S15). BUILD (system).
3. No faction system between the three rivals: wants, relations, pacts, betrayal. BLUEPRINT-11 2.10.1, 2.10.3 (S6 to S8). BUILD (system).
4. No returning-people pool (everyone Frank hurt, spared, paid or let down comes back as a carrier). BLUEPRINT-11 2.4.4 (S24). BUILD (system).
5. Act II plays 18.6 to 28 hours against a 20-hour aim for the whole game, and the rule that skips empty hours is not written. BLUEPRINT-11 3.1.2, 7.4, FIT-F16, CLK-06, WQ-02/06. BUILD (rule).
6. Week one does not pay: a 1990 London fare cannot meet the £18 rent at the offered fare count; the tariff is a question for him. NUMBERS-RUN.md; BLUEPRINT-11 gaps run 2; reality-check Q2; data/fares.json rules. BUILD (economy rule) plus VALUES.
7. The rise stalls on car prices (rung 3 out of reach for most) and escalation runs away for a hard player or stalls for a payer; proposals (hire purchase, one rival rung per five game days) are not adopted. NUMBERS-RUN.md; BLUEPRINT-11 gaps run 2. BUILD (rules).
8. The data still contradicts his rulings: can_die false on Sheila, Pauline, Ada, June, Alison, Ellis, the Widow, Father Walsh and others; send jobs say "never Sheila..."; police.json has tom_never_lays_hands_on; Ellis "cannot be bought"; ids still say "tom". what-if/SUMMARY.md "Data still contradicting"; PROPOSED-PARTS P02. BUILD (data correction, no new content).
9. No fallback by role if a once-shielded person dies (so Act II beats might wait on one killable person). what-if P02; BLUEPRINT-11 RT2-05. BUILD (rule plus data).
10. Hitting Ron, Sheila, Pauline or a driver had no reaction until P01; P01 is only a proposal. what-if P01. BUILD (rule).
11. What is taken at arrest, and the free against paid solicitor. what-if P03; BLUEPRINT-11 2.6.4. BUILD (rule).
12. The firm while Frank is held: missed appointments, drivers carrying goods when arrested. what-if P04. BUILD (rule).
13. His five open questions: knife in a fight (Q-H1), trial witnesses (Q-H2), holding a witness overnight (Q-H3), fire (Q-H4), leaving Meridian or selling Mickey's (Q-H5). what-if/SUMMARY.md. BUILD (rules and scope).
14. A bought Ellis: what it does to her four stages, the case model and a manhunt, and what £100 a week buys. BLUEPRINT-11 2.6.5, 2.6.8. BUILD (rule).
15. Mickey's revolver can be found at rung 2 (about the start of Act II) against his rulings (guns rare and late). BLUEPRINT-11 RT2-14, 2.12.2. BUILD (gate rule).
16. Hold-ups have no parts-tree part and no coverage row; whether Ada, the priest and the over-sixties are barred is unsaid. BLUEPRINT-11 1.6.15. BUILD (rule).
17. How the player can tell someone is over sixty is not stated (RT-09). BLUEPRINT-11 RT-09. BUILD (rule or UI).
18. Buyback (7 game days, price plus a quarter, fences hold nothing) has no part: what is bought back, from whom. BLUEPRINT-11 2.7.6, 3.5.4, 1.6.3. BUILD (system).
19. Frank as lender (a pound in five a week, a quarter goes bad weekly), smuggled tobacco, the firm's costs ledger and a weekly flows audit have no part. BLUEPRINT-11 2.8.2, 4.2.3 (EC-07, EC-08), 2.7.4. BUILD (economy systems).
20. Wage bands, shop weeks and early closing (Friday and Saturday wages) have no part; no early-closing day exists in data. BLUEPRINT-11 2.7.5; data/DATA-BUILD-STATUS places/timetables. BUILD (data structure).
21. How a driver's half of his fares passes through the book, and what "unpaid" means under half-takings. BLUEPRINT-11 2.15.2, 2.11.3, 2.15.1, RT2-06. BUILD (rule).
22. The cold-store contract being open on every road out of Act I sits against an honest firm stopping at rung 2. BLUEPRINT-11 RT2-01. BUILD (rule).
23. Sheila's trust is a state the town should show, but nothing says what; her return is still counted in days. BLUEPRINT-11 2.12.1, RT2-06. BUILD (rule).
24. Ruled in on 24 Nov with no part: crouch, set climbing places (map has six vault places only), shop mirror, working crane and dock barriers, camera re-centre, the empty revolver's click. BLUEPRINT-11 keeper run 5 (1.1.1, 1.1.8, 1.5.3, 5.5.6 and others). BUILD (verbs and map items).
25. Pastimes (snooker with no money, quay fishing, pigeon loft) exist as places with hours in data/places.json but no play is designed. BLUEPRINT-11 FIT-G10, 7.16. BUILD (small systems).
26. Story-driven systems with no part: the world ending shown weekly (S32), the last-afternoon quay (S28), Ron's lessons as a save state (S48), Ron refusing to ride with the revolver (S49), the yard as a pay queue, the funeral tea's three heads, the clock slowed on authored rides, a licensing file, a dated remand hearing. BLUEPRINT-11 keeper run 5 (3.7, 3.1.3, 1.2.7, 1.7.4, 3.5.2, 3.2.4, 7.13, RT2-18, 2.6.4). BUILD (systems).
27. Sound has only reach in metres: no direction or pan, no dulling by walls or shut doors, nothing for above and below. BLUEPRINT-11 checklist top twenty nos. 1, 2, 11 (5.5.3, 5.5.4). BUILD (system).
28. Bystanders who see a weapon must run away from danger and toward doors; no rule. BLUEPRINT-11 2.5.3 (A13.18). BUILD (AI rule).
29. Walking off mid-talk, or a fight breaking into a talk, and a line stopping when its speaker falls, are not specified. BLUEPRINT-11 3.6.1, 3.6.4. BUILD (rule).
30. Pursuers do not replan around a shut door or blocked lane; armed men may fire without a clear line. BLUEPRINT-11 1.5.4 (A14.10, A14.14). BUILD (AI rule).
31. Chases have no timer, the 1 to 3 minute band is a judgement, reference chases of 4 to 8 minutes do not fit the map, and rivals' men have no pursuit rules. BLUEPRINT-11 1.5.1 to 1.5.4, DP5-C01, DP5-C02, FIT-G1. BUILD (rule) plus VALUES.
32. Saving: no plain-words message, no saving sign, no confirm before overwrite, and New game must never overwrite. BLUEPRINT-11 7.8, AX-07 (A39.01 to A39.09). BUILD (rule and UI).
33. Taking something says nothing, and holds (pocket lift, gun draw, searches) show no progress and no cancel rule. BLUEPRINT-11 1.6.2, 6.1.1 (A36.02, A11.10). BUILD (UI rule).
34. Menus and pauses let stray input through (a menu click, held input through loading or the ferry shot); a stray key can skip a scene. BLUEPRINT-11 6.6, 5.8.2 (A03.15, A32.08). BUILD (rule).
35. Camera in tight rooms and stairs, and a promise that it never overrides his own input. BLUEPRINT-11 1.1.2 (A05.09, A05.13). BUILD (rule).
36. Gamepad: no dead-zone defaults, no unplug or reconnect rule, no rule for two pads, no rule for clashing inputs. BLUEPRINT-11 6.6, AX-05 (A03.12, A03.19 to A03.24). BUILD (rule).
37. Small loose props must not block him and crates need weight; one gravity for drops and throws; objects settle and sleep. BLUEPRINT-11 8.10 (A12.05 to A12.08). BUILD (system).
38. Dropped and spilled things (a bag spilled in a bump, gathered, the bumper remembered). BLUEPRINT-11 details catalogue rank 8, nearest 3.6.4. BUILD (small system).
39. A shared line may repeat inside an hour: the line record has no no-repeat field, and the 30 regulars repeat their own lines from night 31. BLUEPRINT-11 gaps run 2 (tech plan, INVENTORY). BUILD (data structure) plus CONTENT.
40. Shared street lines are sized flat (6 per situation) when need depends on how often a situation comes up (about 500 in all). BLUEPRINT-11 gaps run 2; data/line-situations.json (60 situations). CONTENT with a sizing rule.
41. 1,800 own lines and the story banks are TO WRITE (2,015 line records exist, most own lines empty). data/DATA-BUILD-STATUS.md row 10. CONTENT.
42. Most fare, job, happening and side-story words are TO WRITE (63 happenings, 80 rides, 54 jobs, 32 side stories to be cut to 22 to 28). data/DATA-BUILD-STATUS.md rows 10 and 11. CONTENT.
43. Frank fully written: 5 of 23 key scenes done; 18 scenes still wait on the story pick. BLUEPRINT-11 keeper run 6, 3.6.6; data/DATA-BUILD-STATUS.md. CONTENT.
44. The cast: CAST-CHANGES.md not applied; his 200 to 300 residents does not fit the one-shot week; nine uncast voices unnamed; 35 to 48 against 24 to 36 named people. data/DATA-BUILD-STATUS.md row 3; BLUEPRINT-11 FIT-F16, 3.2.1, run 3 (R13). Scope plus CONTENT.
45. Happenings are 63 against 60 to 80 wanted, the count is unset, and they have no jobs-per-hour figure. BLUEPRINT-11 FIT-G6, GD-08. VALUES.
46. Crowd counts are all provisional until the 1990 pavement study lands; the match frame sits under GD-02's 15 to 25. data/crowd.json status; data/DATA-BUILD-STATUS.md row 8; BLUEPRINT-11 GD-02, FIT-G9, 2.1.2. VALUES.
47. Being seen: how far watchers see and know Frank are prototype numbers (data uses 25 m for a known face; one study says about 15 m); the constable's sight rule was widened from 6 to 10 m so its test would pass. reality-check/SUMMARY.md; BLUEPRINT-11 2.2.3, 1.4.1; data/police.json open_points. VALUES (could change a rule).
48. Lamps: Quay Street's four lamp columns are 10 m apart against the 1977 code's 34 m; his answer decides. reality-check/SUMMARY.md Q1; data/light-weather.json lamp. VALUES (map data).
49. Street clutter, door spacing and camera distances came from Mafia and our own scene; real terrace counts owed from photographs. reality-check/SUMMARY.md. VALUES.
50. Feel numbers are first values: walk, run, turn, vault, carry, car handling, blows, firearm draw and aim, hit-stop, damage capacity, knock-out lengths. BLUEPRINT-11 1.1.1 to 1.1.8, 1.2.x, 1.3.x, RT-10, RT-11; data/tune.json (23 numbers owed from footage). VALUES.
51. 441 numbers stated as fact with no source, 75 decided by the wrong kind of thing, 73 carried over from another setting, 93 self-judging tests; tune.json labels 427 prototype keys "basis: real". reality-check/SUMMARY.md CHECK.csv. VALUES (and tests).
52. The clock rewrite is not finished: the staged hour, the landing's window, the 1.5 game hour lead and the first-hour minute marks were fitted to older clocks. BLUEPRINT-11 7.1, CLK-01 to CLK-04, 2.4.4. VALUES (re-run).
53. Map facts disagree: warehouse cuts 73 and 56 m against 50; north edge y 400 against 440; Quay Street 48 against 57.1 m (and no slope rule); passers-by 25 to 35 against at most 25; evening ending 23:00 against 24:00; boot slots 7 against 3 plus 1; lorry driver pay 245 against 255; the Tangs' takeaway and six rooms have no place record. BLUEPRINT-11 4.1.2, 4.7, A06.13; reality-check "Other clashes"; data/DATA-BUILD-STATUS.md rows 1, 2, 4. BUILD (data structure, small) plus VALUES.
54. Unchecked names and wording: Fenmarsh Television and the tune titles were checked from memory only; the content gate catches two design words ("a round", "red light"); "Released under investigation" is later wording than PACE 1984. data/DATA-BUILD-STATUS.md rows 13, 14, 17; BLUEPRINT-11 CLOUD-FIGURES B2. CONTENT (a check and a gate change).
55. The live voices in the browser: transport, install, prewarm (about 14 s), watermark, mouths and latency are not written. BLUEPRINT-11 gaps run 2, 8.12. BUILD (technical system).
56. Feasibility and scope: the one-shot can make about 11 free hours against about 62 hours of content, 31 checklist items are undecided in or out, and "2026-grade frames" spend is unbounded. BLUEPRINT-11 gaps run 3 (INVENTORY section 4), checklist decide-in-or-out, 10.8. Scope (BUILD in effect: decides what exists).
