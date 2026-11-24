# Reality check: summary (24 Nov 2026)

## For Jafar, short

1,164 numbers and rules checked: is each decided by the right kind of thing? 482 fine; 441 stated as fact with no source (the soft count: the blind check judged several fine); 75 decided by the wrong kind of thing; 73 carried over from another setting unchecked; 93 tests that judge the game by its own rules.

Five worst:

1. Lamps. Every lamp was placed by choice. The 1977 lighting code, which side streets lit before 1989 followed, spaced residential lamps about 34 m apart. The other side streets (30 to 32 m) fit it; Quay Street's four alternate sides 10 m apart, copied from our own scene. Our plan had it backwards: it let the being-seen tests decide where lamps go.
2. Being seen. How far watchers see and know Frank are prototype numbers labelled real, never measured in a game. One study: even familiar faces are recognised reliably only within about 15 m, in light brighter than a lit side street.
3. Street clutter and doors: "5 props per 10 m" came from one stretch measured in Mafia and our own scene; "a door every 40 m" from a game study. A rough estimate gives 40 to 50 front doors per 100 m of real terrace. Four camera distances also came from Mafia.
4. Fares: 80p plus 1.10 pounds a mile is above London's 1990 rate and the average outside London (about 80p a mile, late 1991). A Hook ride would have cost about 1.00 to 1.40 pounds.
5. The constable's sight rule was widened from 6 to 10 m so its own test would pass; other tests run on our own bots.

Fixed: the Mafia camera distances are now placeholders until measured; the real lamp code is written beside the lamp data (no lamp moved); the phone boxes and ambulance time got their sources. The data's own checks still pass.

Questions:

1. Lamps. A (recommended): space Quay Street's lamps at the 1977 code's 34 m like the other side streets: four columns become two, darker gaps between. B: keep its four as a deliberate brighter street. C: leave as is.
2. Fares. A (recommended): keep your 2.50 to 3.50, with rides running beyond the Hook at the late-1991 average (about 60p plus 80p a mile). B: keep the current tariff as a game choice. C: real short-ride prices, more fares a night.

## For the PC session: what changes in the measuring order

- Lamp spacing comes first, from the 1977 code and from counting lamp columns in dated 1988 to 1992 photographs of northern port terraces (the cloud cannot see images): about 1 hour, before any being-seen footage.
- Being seen is still measured first among the game rows, but only for watcher numbers (how fast and how far, under known light in KCD2 and RDR2), then applied to the real lamp layout; it no longer sets lamps.
- New short item beside the lamp count: doors and street furniture per 10 m in the same photographs; this replaces the Mafia figure.
- The planned Sleeping Dogs camera drill also covers talk, run and room distances.
- Townspeople's walking speed comes from real figures (about 1.3 to 1.5 m/s, modern UK counts; no pre-1992 figure found). The constable's beat pace has no source (about 1.1 to 1.3 m/s with stops is a guess; the game's 1.1 fits). Only Frank's walk is measured in games.
- Crowd counts: game counts stay a feel lead; the ceiling still comes from 1990 photographs.

## Detail

- Counts by fault kind (CHECK.csv): ok 482; unsourced 441 (191 real-world numbers, 154 feel numbers never measured in a game, 90 of our own design numbers and 6 canon points not marked as judgement); wrong-source 75; carried 73; self-judging 93. Harm 4 and 5 rows: 284, of which 222 are faults.
- Files: CHECK.csv (every row, verdict, fix, harm 1 to 5); REVIEW.csv (the blind reviewer's 40 rows, settled); RESEARCH.md (dated sources; four helpers' notes in research/).
- Readers: eight Sonnet 5.5 readers (chapters 1 to 11, the inventory and sound plan, tune.json, the map and other data, people, economy and temper). Research: four Sonnet 5.5 helpers plus a separate fetch of the key lamp paper.
- Blind check: one fresh Opus 5.5 reviewer re-judged 40 rows drawn at random without seeing the readers' verdicts. Agreement 25 of 40 (62.5%). Of 15 disagreements the reviewer was upheld on 11, the readers on 4; all settled in CHECK.csv (review_verdict, settled). Pattern: readers called honestly marked design or ruled numbers unsourced or carried (6 cases) and missed some unsourced real procedures (police steps, liveries, tie strengths) and one clock carry-over. The counts are a rough guide (a judgement: perhaps 15% either way), not exact.
- Fixed in data: tune.json (cam.talk.back_m, cam.talk_close.back_m, cam.run.back_m, cam.room.back_m to owed; car.ambulance_game_min sourced: London 8 min for 50% from 1990, urban charter 1992 to 1993 14 min for 95%); light-weather.json (lamp.real_spacing_check, lamp.period_lighting_classes: BS 5489-3:1989 classes 3/1 to 3/3, so 5.4.2's 3.5 to 6 lux is a period figure); tools/build_map.py and map.json (lamp and phone-box sources only; the three phone boxes sit inside a rough estimate of 3 to 6 for the district, low confidence; no position changed). check_map 187 passed with the two old open-point warnings; validate_data 338 passed.
- Not fixed, by rule: lamp positions and the fare tariff (questions; both change play); being-seen numbers (owed from footage); street clutter and door spacing (owed from PC photo counts); self-judging tests (each needs an outside reference named; listed in CHECK.csv with harm).
- Other clashes, for the keeper: chase loop 1,528 m with lap times giving 16 to 20 m/s against FIT-G2's 27 m/s; Quay Street 48 against 57.1 m; passers-by 25 to 35 (INVENTORY) against at most 25 (GD-02); happenings 60 against 80; evening ending 23:00 or 24:00; crouch out (SND-06) against in (6.6); boot slots 7 against 3 plus 1; milk float hours; lorry driver pay 245 against 255 pounds; tune.json's "basis: real" on 427 keys, most of them prototype values.
- Allowance: 75% at the start (21:37 reading); no newer reading posted during the run. Model: Opus 5.5.
