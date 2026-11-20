# The one-shot's checklist

Every gameplay part the one-shot (Friday 20 Nov, 22:10) builds into the browser prototype, in BUILD-ORDER's stages, each with its test and where its design is. The one-shot reports against this list, part by part: done (its test passes), shallow (built, test not yet passing), or not reached, with the reason. Generated from PARTS-TREE.json by tools/lane/parts-tree/render_views.py.

Rules for the one-shot: never change tools/lane/one-sim/; the town simulation stays the real one where the switch has landed; no polish (art, animation detail, voices, clothes and faces are never the browser's work); the content rule; a play build reaches him only through the publish gate. 'Now' is the prototype's status before the one-shot, from evidence (round 5 published, round 6 built and not published).

Parts: 191. Already passing their standard: 1 (keep them passing).

## Stage A: one evening that holds (121 parts)

- [ ] 1.1.1 Walk, run and turn. Now: built. Design: DESIGN §17 (input only); feel not designed. Test: feel numbers inside measured bands (input probe); H: 'did moving feel heavy or slippery?'; his eye in Unreal.
- [ ] 1.1.2 On-foot camera follow. Now: built. Design: DESIGN §17. Test: B soak with clip detector; S frames counted for feet in frame; H screenshots in tight rooms.
- [ ] 1.1.3 Doors, stairs and thresholds. Now: built shallow. Design: DESIGN §1, §6 rooms. Test: B: 30 minutes of walking into every door and stair; S: door use timed.
- [ ] 1.1.4 Carrying. Now: built. Design: DESIGN §3, §15 (the carry). Test: S: a carried load raises what a witness catches; H: 'could you tell what Tom was carrying?'.
- [ ] 1.1.5 Hiding and keeping out of sight. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A1 (new). Test: S: standing still in a doorway lowers what is caught versus walking past; H: 'where would you stand to not be seen?'; addendum rules ER-HIDE-01 to 03.
- [ ] 1.1.7 Stopping and blending in. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A10. Test: S: a seated or smoking Tom is caught less than one standing about; H: minding feels like play; addendum rules ER-STOP-01.
- [ ] 1.2.1 Car handling. Now: built. Design: DESIGN §5; driving study rounds 1 to 3. Test: S: drives D1 to D8 by keys and pad inside the bands; his feel check.
- [ ] 1.2.2 Car camera. Now: built shallow. Design: DESIGN §17. Test: S: D8 camera run; B: 40-minute soak with no clipped frame.
- [ ] 1.2.3 Getting in and out. Now: built. Design: DESIGN §5. Test: S: enter and exit timed from both sides, door blocked.
- [ ] 1.2.4 Crashes, damage and unsticking. Now: built. Design: DESIGN §5. Test: S: pole and wall hits at 10, 20, 35, 50 mph; B: 30 minutes of crashing.
- [ ] 1.2.5 Cars and people. Now: built shallow. Design: DESIGN §5. Test: S: 1,000 seeded crossings with no contact; hits at 5, 15, 30, 50 mph, nobody dies; both choices seeded.
- [ ] 1.2.7 Driving with passengers. Now: built shallow. Design: DESIGN §5, §11 staging. Test: H: fare log; S: a staged back-seat talk with the car moving.
- [ ] 1.3.1 Blows and contact. Now: built. Design: DESIGN §7 Feel. Test: S: melee drills at 1/60 s inside C1 to C15 (tools/lane/melee_drills.py); his feel check.
- [ ] 1.3.2 Reading and answering blows. Now: built. Design: DESIGN §7; DESIGN-ADDENDUM-2026-11-20 §A29 (guard, slip, counter, breath, grab). Test: S: drills; H: 'did you see the blow coming?'; addendum rules ER-DEFEND-01 to 02.
- [ ] 1.3.3 Targeting without lock-on. Now: built. Design: DESIGN §7. Test: S: targeting script with three men round Tom.
- [ ] 1.3.4 The lower rungs. Now: built. Design: DESIGN §7. Test: S: each rung exposes seven slots; H: rung reached and why.
- [ ] 1.3.5 The street as a weapon. Now: built shallow. Design: DESIGN §7. Test: S: each of seven places triggers its move; content check: no finisher shown at length.
- [ ] 1.3.6 Things to hand and carried weapons. Now: built. Design: DESIGN §7. Test: S: breakage counts; a weapon out on a held input only (ER-FIGHT-08); a cosh from behind on an unaware man knocks out and is seen as a strike.
- [ ] 1.3.7 Condition without bars. Now: built. Design: DESIGN §7. Test: S: 10,000 simulated fights, deaths only by the fall rule; H: 'who was winning?'.
- [ ] 1.3.8 Odds, crowds and nerve in a fight. Now: built. Design: DESIGN §7. Test: S: scripted patient and mashing fighters; seeded nerve cases.
- [ ] 1.3.9 How a fight ends. Now: built. Design: DESIGN §7 Death. Test: S: each of five endings scripted; beaten route timed.
- [ ] 1.3.12 Fighter types. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A29. Test: S: the job data; addendum rules ER-TYPES-01.
- [ ] 1.4.1 Reading watchers. Now: built. Design: DESIGN §2. Test: H: the three questions at ten random moments, 8 of 10 right, sound off and light cue off.
- [ ] 1.4.2 Light and dark as cover. Now: built. Design: DESIGN §2, §6. Test: H: screenshots at the darkest spots; S: light value matches the cue.
- [ ] 1.4.3 Hearing his own noise. Now: built shallow. Design: DESIGN §2, §17. Test: H: sound-only test.
- [ ] 1.4.4 Give-aways and the coat. Now: built shallow. Design: DESIGN §2 'What gives him away'. Test: S: golden rows, one per give-away.
- [ ] 1.4.5 Reaching the witness. Now: designed. Design: DESIGN §2 'The walk'. Test: S: walk timed; H: 'did you get to her first?'.
- [ ] 1.4.6 Seeing assist. Now: built shallow. Design: DESIGN §2. Test: S: screen inventory with the assist on.
- [ ] 1.4.7 Street manners. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A10. Test: S: each gesture answered within 1 s and remembered; addendum rules ER-MANNER-01.
- [ ] 1.5.1 Fleeing on foot. Now: built. Design: DESIGN §8 The beat. Test: S: 50 seeded chases end in 90 s; H: 'how did you lose him?'.
- [ ] 1.5.3 Car chases. Now: designed. Design: DESIGN §5. Test: S: seeded car chases end within 90 s; lost by breaking sight.
- [ ] 1.5.4 Pursuers. Now: built shallow. Design: DESIGN §8. Test: S: pursuer gives up at the rule; never cheats through walls.
- [ ] 1.6.4 Fronting up. Now: built. Design: DESIGN §4, §7 lower rungs. Test: S: each debtor's outcomes scripted; H: 'did the five debts feel different?'.
- [ ] 1.6.5 Minding and waiting. Now: designed. Design: DESIGN §4 Minding. Test: H: waiting share; S: minding recorded as 'stood with'.
- [ ] 1.6.6 Getting ready. Now: built shallow. Design: DESIGN §1 evening, §6, §7. Test: S: loadout limits; H: time spent getting ready.
- [ ] 1.6.7 Getting rid of things. Now: designed. Design: DESIGN §2, §7; body moving as a crew verb (§12). Test: S: washing clears the give-away and plants a witness at the launderette.
- [ ] 1.6.8 Using the world. Now: built shallow. Design: DESIGN §17 Screen. Test: H: walk-up sweep with no prompt faults.
- [ ] 1.6.9 Coat, pockets and office storage. Now: built shallow. Design: DESIGN §7 Weapons; DESIGN-ADDENDUM §A5. Test: S: a search finds what is carried; office storage keeps across saves; addendum rules ER-POCKET-01 to 02.
- [ ] 2.1.1 Schedules of named people. Now: built. Design: DESIGN §2; prototype rules.js schedules. Test: S: walk checks wherever Tom stands; no jammed doorway in a seeded week.
- [ ] 2.1.2 The crowd's clock windows. Now: built shallow. Design: DESIGN §2 (hours owed). Test: S: crowd counts by hour match the researched table.
- [ ] 2.1.3 Off-screen life. Now: built. Design: DESIGN §2. Test: S: a seeded week gives the same result watched or unwatched.
- [ ] 2.1.4 Weather and hour change who is out. Now: built shallow. Design: DESIGN §6. Test: S: the same seed dry, drizzle, rain.
- [ ] 2.1.5 Crowd movement and avoidance. Now: built shallow. Design: not designed. Test: B: 30 minutes walking through crowds, no clipping or jams; H screenshots.
- [ ] 2.2.1 Seven slots per act. Now: built shallow. Design: DESIGN §2; C# Core. Test: S: PerceptionGolden rows.
- [ ] 2.2.2 Identification ladder. Now: built shallow. Design: DESIGN §2; C# Core. Test: S: golden rows.
- [ ] 2.2.3 Sight by distance and light. Now: built. Design: DESIGN §2. Test: S: figures at 8, 18, 35 m.
- [ ] 2.2.4 Sound reach. Now: built. Design: DESIGN §2. Test: S: reach rows by act, hour and rain.
- [ ] 2.2.5 Give-away rules. Now: built shallow. Design: DESIGN §2. Test: S: golden rows per give-away.
- [ ] 2.2.6 Ground rules and trespass. Now: designed. Design: DESIGN §4; DESIGN-ADDENDUM-2026-11-20 §A10. Test: S: every place has a label and the warnings fire in order; addendum rules ER-GROUND-01.
- [ ] 2.3.1 Per-person memory store. Now: built. Design: DESIGN §2; C# Core. Test: S: SaveChaos; reload at random moments and compare.
- [ ] 2.3.2 Witness certainty. Now: built. Design: DESIGN §2. Test: S: golden rows.
- [ ] 2.4.1 Transmission. Now: built. Design: DESIGN §2; C# Core. Test: S: golden rows; Soak.
- [ ] 2.4.2 Cooling by kind. Now: built shallow. Design: DESIGN §2 (a town task with new golden rows). Test: S: new golden rows.
- [ ] 2.4.3 Showing what people know. Now: built. Design: DESIGN §2. Test: H: 'who in the street knew about last night?'.
- [ ] 2.4.4 It comes back. Now: built. Design: DESIGN §2. Test: S: 16 seeded weeks; timeliness at the playing clock.
- [ ] 2.5.1 The walk to tell. Now: built shallow. Design: DESIGN §2. Test: S: walk timed and visible.
- [ ] 2.5.2 Stopping a witness. Now: built shallow. Design: DESIGN §2, §8. Test: S: each answer's effect on the report and the talk.
- [ ] 2.5.3 Crowd reaction to a deed. Now: built. Design: DESIGN §2. Test: S: after a seen deed, look, gather, quieter talk.
- [ ] 2.6.1 The beat constable. Now: built shallow. Design: DESIGN §8 (new system needing its place in PLAN.md). Test: S and H: the challenge announced.
- [ ] 2.6.2 Challenge and search. Now: built. Design: DESIGN §8. Test: S: a search finds what is carried.
- [ ] 2.6.3 Statements and the arrest rule. Now: built. Design: DESIGN §8; C# Core. Test: S: golden rows.
- [ ] 2.6.4 Custody as hours. Now: built shallow. Design: DESIGN §8. Test: S: arrest timed.
- [ ] 2.7.1 Clean money and the fare book. Now: built. Design: DESIGN §9. Test: S: sum of flows.
- [ ] 2.7.2 Night money and the tin. Now: built. Design: DESIGN §9. Test: S: sum of flows.
- [ ] 2.7.3 The wash. Now: built. Design: DESIGN §9. Test: S: warning before the books go off.
- [ ] 2.7.4 Rent and running costs. Now: built shallow. Design: DESIGN §9. Test: S: both weeks scripted.
- [ ] 2.7.7 Flows ledger. Now: built shallow. Design: DESIGN §9. Test: S: no money from nowhere.
- [ ] 2.8.1 The five debtors. Now: built. Design: DESIGN §4; first-week designs. Test: H: the five debts named as different.
- [ ] 2.8.2 Partial payment and the book. Now: built shallow. Design: DESIGN §4. Test: S: golden rows.
- [ ] 2.9.1 The asks. Now: built. Design: DESIGN §6, §15, §16. Test: S: ask schedule in a seeded week.
- [ ] 2.12.1 The name ladder. Now: built. Design: DESIGN §14. Test: S: each step heard within a day.
- [ ] 2.12.4 Greetings by regard. Now: built shallow. Design: DESIGN §11. Test: H: same street walked at rung 1 and rung 3 (ER-RISE-03).
- [ ] 2.18 Ambulance and the hospital. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A22. Test: S: an ambulance arrives after a call within its set time; addendum rules ER-AMB-01.
- [ ] 3.2.1 Principals. Now: built shallow. Design: canon; casting sheets; DESIGN §16. Test: his eye on each whole person; H: talk transcripts.
- [ ] 3.2.2 The firm's people. Now: built. Design: DESIGN §5, §12. Test: S: the firm runs; H: Pauline's directions.
- [ ] 3.2.3 The thirty regulars. Now: built shallow. Design: regular cards; DESIGN §11. Test: H: transcripts; S: line counts.
- [ ] 3.2.4 The crowd. Now: built shallow. Design: DESIGN §2. Test: S: crowd generation content check; counts by hour.
- [ ] 3.4.1 Fare people. Now: built shallow. Design: DESIGN §5. Test: H: fare freshness over a week; ER-CORE-08.
- [ ] 3.4.2 Wrinkles. Now: designed. Design: DESIGN §5. Test: H: the log; S: no repeat twice running.
- [ ] 3.4.3 Pauline and the radio. Now: built shallow. Design: DESIGN §5. Test: S: a scripted driver follows each fare's words alone.
- [ ] 3.5.1 Carries. Now: built. Design: DESIGN §4, §15. Test: S: three routes each finish; H retellable.
- [ ] 3.5.2 Collections. Now: built. Design: DESIGN §4. Test: S: every outcome scripted.
- [ ] 3.5.6 Job template and step states. Now: built shallow. Design: DESIGN §4. Test: S: job data checks; every outcome reached by script.
- [ ] 3.5.7 How jobs reach him. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A17. Test: S: every job has a giver and a channel; H: 'how did you hear of it?'; addendum rules ER-REACH-01.
- [ ] 3.6.1 Live talk. Now: built. Design: DESIGN §11; talk system in C#. Test: S: slow stand-in; packaged speech measure.
- [ ] 3.6.2 Claim check. Now: built shallow. Design: DESIGN §11. Test: S: planted bad replies.
- [ ] 3.6.3 Written street lines. Now: built. Design: DESIGN §11. Test: H: transcripts.
- [ ] 3.6.4 Crowd lines by situation. Now: built shallow. Design: DESIGN §11. Test: S: line counts; content gate.
- [ ] 3.6.5 Decision lines. Now: built. Design: DESIGN §11. Test: S: 170 lines that are not a plain yes.
- [ ] 3.6.6 Suggested lines. Now: built. Design: DESIGN §11. Test: S: shown on both devices.
- [ ] 3.6.7 AI notice and line report. Now: built shallow. Design: DESIGN §11. Test: S: report filed from talk and from pause.
- [ ] 3.6.8 How the player speaks. Now: built. Design: DESIGN-ADDENDUM-2026-11-20 §A25. Test: S: a whole talk by pad alone; addendum rules ER-SPEAK-01.
- [ ] 4.1.4 The soft edge. Now: designed. Design: DESIGN §5. Test: S: leaving the map edge in the cab.
- [ ] 4.2.4 The water's edge. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A11. Test: B: 30 minutes along the quay edge, no fall in; S: a man knocked in climbs out; addendum rules ER-WATER-01 to 02.
- [ ] 4.5.1 Traffic drivers. Now: built shallow. Design: TRAFFIC-STAGE1-REFERENCE-MODEL. Test: S: 1,000 seeded crossings; 40 minutes lawful driving with no hits.
- [ ] 6.1.1 The prompt. Now: built. Design: DESIGN §17. Test: H: walk-up sweep.
- [ ] 6.1.2 Subtitles. Now: built shallow. Design: DESIGN §17. Test: S: layout test at four sizes.
- [ ] 6.1.3 The belief line. Now: built. Design: DESIGN §10. Test: S: trigger each perceivable change.
- [ ] 6.1.4 Light and sound cues. Now: designed. Design: DESIGN §2. Test: H: ER-EYES-01 with the cue off and on.
- [ ] 6.1.5 Knowing the time. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A31. Test: S: the watch glance; H: 'what time is it?'; addendum rules ER-TIME-01.
- [ ] 6.2.1 People. Now: built. Design: DESIGN §10. Test: S: no entry without a source event.
- [ ] 6.2.2 Day book. Now: built. Design: DESIGN §10. Test: S: struck through, never removed.
- [ ] 6.2.3 Open. Now: built. Design: DESIGN §10. Test: H: 'what next, and where' from the Ledger alone.
- [ ] 6.2.4 Money in words. Now: built. Design: DESIGN §10. Test: H: asked what he has.
- [ ] 6.3 The paper map. Now: built shallow. Design: DESIGN §10. Test: S: no unknown place marked; H: finds a told place.
- [ ] 6.4 Menus. Now: built. Design: DESIGN §17. Test: S and B: pause, continue, quit on every device.
- [ ] 6.5 Teaching the player. Now: built shallow. Design: DESIGN §15 Teaching. Test: S: idle test.
- [ ] 6.6 Controls. Now: built shallow. Design: DESIGN §17. Test: S: the same scripted evening by each device.
- [ ] 6.7 Talk screen. Now: built. Design: DESIGN §11. Test: S: typing never moves Tom; Leave always offered.
- [ ] 6.9 Finding the way. Now: built shallow. Design: DESIGN §4 Guidance; DESIGN-ADDENDUM-2026-11-20 §A9. Test: H: ten named places reached unaided; S: every place has an address and a landmark; addendum rules ER-WAY-01 to 03.
- [ ] 7.1 The first hour. Now: built shallow. Design: DESIGN §15 (restaging, QUESTIONS 4 open). Test: H: first-hour run timed; S: control timing.
- [ ] 7.2 An evening. Now: built shallow. Design: DESIGN §1, §3. Test: H: the evening run and the panel.
- [ ] 7.6 Tension and retellable moments. Now: built shallow. Design: DESIGN §3. Test: H: tense log; panel 'most exciting moment'.
- [ ] 7.8 Saving. Now: built shallow. Design: DESIGN §17. Test: S: reload at random moments; SaveChaos.
- [ ] 7.9 Failure without reload. Now: built. Design: DESIGN §1, §4, §7, §8. Test: S: every failure route timed.
- [ ] 7.11 Waiting and time skips. Now: built. Design: DESIGN §6; waiting design 29 Sep. Test: S: the week of waits.
- [ ] 7.12 Always something to do. Now: built shallow. Design: DESIGN §1. Test: S: idle probe at 20 daytime moments; H empty minutes.
- [ ] 7.13 The game clock. Now: passes. Design: DESIGN §15. Test: S: one value in the tuning table, read by both.
- [ ] 7.14 Variety. Now: missing. Design: DESIGN §4. Test: H: the log.
- [ ] 8.4.1 Visual stand-ins for sound cues. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A6. Test: H: ER-EYES-01 with sound off and the option on; addendum rules ER-ASSIST-01.
- [ ] 9.6 The tuning table. Now: built. Design: prototype rules.js. Test: S: no magic number outside the table.

## Stage B: a week that holds (38 parts)

- [ ] 1.1.6 Tailing on foot. Now: designed. Design: DESIGN §4 Tails; DESIGN-ADDENDUM §A2. Test: S: a scripted tail is made at the addendum's rule and never fails on a hidden distance; H: 'did losing him feel fair?'; addendum rules ER-TAIL-01 to 03.
- [ ] 1.1.8 Vaulting low walls and fences. Now: missing. Design: DESIGN-ADDENDUM-2026-11-20 §A26 (to the recommended answer). Test: S: each vault point works in a chase; no vault anywhere else; addendum rules ER-VAULT-01.
- [ ] 1.2.6 Tailing and being tailed by car. Now: designed. Design: DESIGN §5 wrinkles; DESIGN-ADDENDUM §A2. Test: S: scripted car tail; H: 'did you know how close was too close?'; addendum rules ER-TAIL-01 to 03.
- [ ] 1.2.8 Riding as a passenger. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A24. Test: S: a ride arrives; skip advances the clock by the drive's time; addendum rules ER-RIDE-01.
- [ ] 1.2.9 Repairs, plates and paint. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A24. Test: S: a repainted car is not named as the firm's by a witness who saw the old paint; addendum rules ER-PAINT-01.
- [ ] 1.2.10 Taking a parked car. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A27 (to the recommended answer). Test: S: a taken car is reported and named; force heard at its reach; addendum rules ER-TAKE-01.
- [ ] 1.3.11 Marks that last. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A21. Test: S: a marked Tom is caught more; marks fade on the clock; addendum rules ER-MARK-01.
- [ ] 1.4.8 Drawing a watcher away. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A23. Test: S: a noise inside reach turns a head; outside reach does nothing.
- [ ] 1.5.2 Pursuing on foot. Now: designed. Design: DESIGN-ADDENDUM §A3. Test: S: a runner can be caught by a direct line and lost by a slow one; ends within 90 s; addendum rules ER-PURSUE-01 to 02.
- [ ] 1.6.1 Getting in. Now: designed. Design: DESIGN §4. Test: S: a room entered three ways; force heard at its reach.
- [ ] 1.6.2 Searching and taking. Now: designed. Design: DESIGN-ADDENDUM §A4. Test: S: every container searchable, each search timed and heard at its reach; addendum rules ER-SEARCH-01 to 02.
- [ ] 1.6.3 Lifts and the hot mark. Now: designed. Design: DESIGN §4. Test: S: golden rows for the mark; the owner recognises the goods.
- [ ] 1.6.10 Tom's wardrobe. Now: designed. Design: DESIGN §14; DESIGN-ADDENDUM-2026-11-20 §A21. Test: S: a change of coat lowers a witness's mark rung; H: strangers greet differently; addendum rules ER-COAT-01.
- [ ] 1.6.11 Casing a place. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A23. Test: S: a cased place's hours appear in the Ledger and match the routines; addendum rules ER-CASE-01.
- [ ] 2.1.6 The town's calendar. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A20. Test: S: routines change on the calendar days; content gate; addendum rules ER-CAL-01 to 02.
- [ ] 2.4.5 The paper and the news. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A19. Test: S: every printed line traces to what Alison was told or saw; addendum rules ER-PAPER-01.
- [ ] 2.6.5 DS Ellis and the four stages. Now: built shallow. Design: DESIGN §8. Test: S: every route to a manhunt passes its signs.
- [ ] 2.6.7 Traffic police and stops. Now: designed. Design: DESIGN §5; DESIGN-ADDENDUM-2026-11-20 §A12. Test: S: a stop starts only on reckless driving in sight; ends within 2 minutes; addendum rules ER-TRAFFIC-01 to 02.
- [ ] 2.7.5 Purses, tills and shops. Now: built shallow. Design: DESIGN §9; DESIGN-ADDENDUM-2026-11-20 §A30 (haggling). Test: S: a shop refuses and remembers; addendum rules ER-HAGGLE-01.
- [ ] 2.7.6 Fencing. Now: designed. Design: DESIGN §4, §9. Test: S: golden rows.
- [ ] 2.7.8 Spending. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A21. Test: S: each shop sells its list; H: 'what did you spend on?'; addendum rules ER-SPEND-01.
- [ ] 2.9.2 Keeping or ending the arrangement. Now: built shallow. Design: DESIGN §16. Test: S: both branches reach Act II.
- [ ] 2.10.2 Rival eyes. Now: designed. Design: DESIGN §13. Test: S: every rival move traces; ER-EYES-05 no all-knowing town: every reaction by a neighbour, the police or a rival prints its chain of sightings.
- [ ] 2.14 Each person's temper. Now: built. Design: QUESTIONS 3 (recommended). Test: S: the same deed goes differently with different people there.
- [ ] 2.16 Death, bodies and the missing. Now: built shallow. Design: DESIGN §7 Death. Test: S: a missing routine is noticed; a body never cools.
- [ ] 2.19 Lasting marks on the town. Now: designed. Design: DESIGN §4. Test: S: marks persist across save and load for their set time.
- [ ] 3.1.1 Act I, The Inheritance. Now: built. Design: DESIGN §16; game-design first-week designs. Test: H: the week run; panel M1.
- [ ] 3.1.6 Mickey's past. Now: built shallow. Design: DESIGN §16; story outline. Test: S: the street version stays a street fact.
- [ ] 3.2.5 Someone worth being honest for. Now: designed. Design: DESIGN §16 (Danby still to write). Test: S: the friendship reaches its ending state.
- [ ] 3.3 Side stories. Now: designed. Design: DESIGN §4; drafts of 8 Nov. Test: H: found unaided; S: each ends in a town fact.
- [ ] 3.5.3 Break-in sites. Now: designed. Design: DESIGN §4. Test: S: each site entered three ways.
- [ ] 3.5.4 Tails, minding and lifts content. Now: designed. Design: DESIGN §4. Test: S: each instance's outcomes.
- [ ] 3.7 Street happenings. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A18. Test: S: placement by state; H: empty minutes fall; addendum rules ER-HAPPEN-01 to 02.
- [ ] 4.11.1 Yard dogs. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A23. Test: S: a bark draws the owner within the rule; addendum rules ER-DOG-01.
- [ ] 6.10 Letters and papers in hand. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A19. Test: S: each letter opens and goes in the Ledger.
- [ ] 7.3 A week. Now: built. Design: DESIGN §16. Test: H: the week run and the panel.
- [ ] 7.10 Difficulty as assists. Now: built shallow. Design: DESIGN-ADDENDUM §A6. Test: S: each assist changes only its own thing; H: an impatient player finishes the first hour with assists on; addendum rules ER-ASSIST-01 to 02.
- [ ] 7.16 Pastimes. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A28 (to the recommended answer). Test: H: chosen in free time; S: no stakes anywhere; addendum rules ER-PASTIME-01.

## Stage C: the rise (27 parts)

- [ ] 1.3.10 Firearms. Now: designed. Design: DESIGN §7 Weapons, dial. Test: S: dial rules; feel numbers inside measured bands once researched.
- [ ] 1.7.1 Orders in the field. Now: designed. Design: DESIGN §12 Orders. Test: S: each order; B: crew never block a lane.
- [ ] 1.7.2 Sending (the eight verbs). Now: designed. Design: DESIGN §12. Test: S: each verb leaves a chain the town can trace; accomplice knows.
- [ ] 1.7.3 The board. Now: designed. Design: DESIGN §12. Test: S: placements change sightings; H: minutes spent at the board.
- [ ] 1.7.4 Men at his side. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A16. Test: B: followers never block; S: a fight with Ron at his side goes as the odds say; addendum rules ER-SIDE-01.
- [ ] 2.6.6 Armed response and the dial's police. Now: designed. Design: DESIGN §7. Test: S: three seeded weeks at War.
- [ ] 2.6.8 Bought men and squaring the law. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A13. Test: S: one bought officer, his limits; the rest of the station unchanged; addendum rules ER-BOUGHT-01.
- [ ] 2.6.9 Charges, bail and the office searched. Now: built shallow. Design: DESIGN-ADDENDUM-2026-11-20 §A13. Test: S: a charge reaches the endings; a search finds what is stored at the office; addendum rules ER-SEARCHED-01.
- [ ] 2.10.1 Rival ladders. Now: built shallow. Design: DESIGN §13. Test: S: no rung skipped, each said or shown.
- [ ] 2.10.3 Pressures and answers. Now: designed. Design: DESIGN §13. Test: S: each pressure's three answers.
- [ ] 2.10.4 The Fixer. Now: designed. Design: DESIGN §13. Test: S: reads are true to the simulation.
- [ ] 2.11.1 Recruiting. Now: designed. Design: DESIGN §12. Test: S: both roads seeded.
- [ ] 2.11.2 Nerve, loyalty and breaking. Now: designed. Design: DESIGN §12. Test: S: sign before event in every seeded case.
- [ ] 2.11.3 Crew fates. Now: designed. Design: DESIGN §12. Test: S: each fate reached by script.
- [ ] 2.12.2 Rung table. Now: designed. Design: DESIGN §14. Test: S: each rung's holdings and openings.
- [ ] 2.12.3 Access and soft keys. Now: designed. Design: DESIGN §14. Test: S: each door's keys.
- [ ] 2.12.5 Property that reacts. Now: designed. Design: DESIGN §14. Test: H: office at rung 1 and rung 3 compared.
- [ ] 2.13 The escalation dial. Now: designed. Design: DESIGN §7. Test: S: dial never moves on an unseen deed; War weeks counted.
- [ ] 2.15.1 Fleet and drivers. Now: designed. Design: DESIGN §12, §14; DESIGN-ADDENDUM-2026-11-20 §A14. Test: S: a bought car joins the board and the ranks; addendum rules ER-FIRM-01 to 02.
- [ ] 2.15.2 Ranks and accounts. Now: built shallow. Design: DESIGN §14; DESIGN-ADDENDUM-2026-11-20 §A14. Test: S: an account adds fares to the book; addendum rules ER-FIRM-01.
- [ ] 2.15.3 Other firms on the ranks. Now: designed. Design: DESIGN-ADDENDUM-2026-11-20 §A14. Test: S: fares move to the other firm after a drive-off and come back.
- [ ] 2.17 Fronts and rackets held. Now: designed. Design: DESIGN §14; DESIGN-ADDENDUM-2026-11-20 §A15. Test: S: a front pays through its man; trouble at it reaches Tom through people; addendum rules ER-FRONT-01 to 02.
- [ ] 3.1.2 Act II, The Rise and the Squeeze. Now: designed. Design: DESIGN §16 (proposal for the writing). Test: H: a played stretch of Act II; S: every beat reachable.
- [ ] 3.5.5 Sit-downs. Now: designed. Design: DESIGN §11, §16. Test: S: three answers each.
- [ ] 7.4 Acts II and III pacing. Now: designed. Design: DESIGN §16. Test: H: sampled stretches; S: no dead weeks.
- [ ] 7.5 The hour budget. Now: built shallow. Design: DESIGN §1. Test: H: play time booked by activity against the measured shares.
- [ ] 7.7 Rising in position, felt. Now: built shallow. Design: DESIGN §14. Test: H: same street at rung 1 and 3.

## Stage D: the end (5 parts)

- [ ] 3.1.3 Act III, The Ledger Comes Due. Now: designed. Design: DESIGN §16. Test: S: each morning's step graded; H: 'how does this end, and why'.
- [ ] 3.1.4 The endings. Now: built shallow. Design: DESIGN §16 (three shown, five kept underneath). Test: S: every ending by a scripted route, including hunted (ER-END-01).
- [ ] 3.1.5 Ending signs and Tom's reading. Now: designed. Design: DESIGN §16. Test: S: balance sweep; H predicts the ending.
- [ ] 6.2.5 Tom's reading. Now: designed. Design: DESIGN §10. Test: H predicts the ending from it.
- [ ] 7.15 After the ending. Now: built shallow. Design: DESIGN-ADDENDUM §A7. Test: S: the close plays, credits roll, the player returns to a stated place; addendum rules ER-AFTER-01.

## Not for the one-shot

Every part whose track is Unreal only (art, faces, clothes, Kiln, performance, shipping) and the machinery outside the prototype. See PLAN-VIEW.md for their order.
