# BLUEPRINT 04: The place

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. Meridian's Hook and its docks: one port, dense, known by heart.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 4.1 The Hook's layout

The map as data with testable layout rules.


### 4.1.1 Quay Street

- How it works: Quay Street is the built street, in the Hook, Mickey's on it: 48 m from the quay, climbing about 3 m, then bending east behind the parade, 10.25 m front to front with both pavements (terrace-fronts.md, atlas-01; C-226). The east side is the six-bay parade; the west block across from the north half of the parade carries shops; the west block across from Mickey's, at the quay end, is plain terraces. Trades by bay: 1 fishmonger, 3 the empty unit to let (bare glass dressed with card, cardboard and a fallen blind, never painted over: R5), 4 launderette, 5 grocer; west north: a newsagent and tobacconist, an ironmonger, a tea room. Two concrete lamp columns stand about 34 m apart (his ruling of 24 Nov, advisor 371: Quay Street's lamps follow the period code like the other side streets, darker gaps between; the photo count confirms or corrects the spacing). Their places are to be set in the map data, which still draws four (x 8 east, 18 west, 28 east, 38 west). The 593 pieces keep their east_parade_ identifiers, which carry no claim about location. Window frames are white and some surrounds are painted (R6). Every visual is judged against the Hook sheet and KCD2 frames; photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov).
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work; canon's three sides Test: the gate; his eye on whole street frames
- Source: canon; RULINGS The look (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon ('The built street', 'Quay Street's three sides'); RULINGS 'The look and the street' (3 Oct trades, 5 Oct atlas); DEFINITIONS G1; TARGET-STREET-FURNITURE-2026-11-17 S1; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7); bay 3 (R5) and windows (R6): his ruling of 24 Nov (RULINGS on wip, his decisions page) Lamps: his ruling of 24 Nov (advisor 371); BS 5489-3:1977 group B5/6, 34 m plus or minus 10% for residential roads of 5 to 6 m columns (Fotios and Robbins 2020, a modern paper describing the code; the code text unreached; RESEARCH L1). Street width: 10.25 m front to front is just under the 1877 model byelaws' 11 m for new streets, possible for an older dockside street (RESEARCH W1). Length 48 m here against 57.1 m in the map file is open (C-396).
- Status: outside. Coverage row: 4.1.1. Conflicts settled: C-092, C-093, C-291, C-290.
- Prior research: production/specs/terrace-fronts.md and atlas-01 ADOPTED-2026-10-06: carriageway 6.0 m, footways 2.0 m, front to front 10.25 m, granite kerb upstand 115 mm (the scene file's 125 is wrong), bays 6 m, 1 in 12 climb at the north end.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 4.1.2 The rest of the Hook

- How it works: The rest of the Hook is the G1 road plan: a quay road of 540 m, a north road of 338 m to the soft edge, Chapel Lane 240 m, the cold-store road 380 m, the dock road 350 m, Basin Road 353 m, the warehouse row 350 m, and foot-only lanes (the yards' lane 63 m, the terraces' ginnel 345 m, two 50 m warehouse cuts) with six vault places. About 620 by 400 m, all reachable. Density goes up and back, not out: back rooms, yards, alleys, upstairs flats. The look follows the Hook sheet and KCD2 frames, with a thinner dressing away from Quay Street where the player does not walk.
- The map is made (24 Nov, R1: the Hook plus its docks kept): production/lane/blueprint/data/map.json, one file in metres from the ferry landing (x east, y north), footprint x -80 to 540 and y 0 to 400, with drawings map-topdown.svg and paper-map.svg. Its drawn lengths differ a little from G1's: quay road 540, North Road 333.5 (G1 338), Basin Road 352.3 (G1 353), the yards' lane 65.8 (G1 63), the ginnel 342.9 (G1 345), the two warehouse cuts 72.9 and 55.7 (G1 50 each, approximate); Quay Street 57.1 with Back Parade 41.1. Which figures win where they differ is a gap.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work; density up and back, not out (Study 17) Test: the gate; B navigation soak
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate; DESIGN §6 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: atlas-01 (DISTRICTS, TOWN-FORM-BIBLE); DEFINITIONS G1; DESIGN s.6; Study 4 target 3; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7); R1 and the map file: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: outside. Coverage row: 4.1.2. Conflicts settled: C-094, C-095, C-291.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G21, G14.

### 4.1.3 Landmarks and signs

- How it works: Every door that matters has a number and every street a name plate at its ends (Marcellus SC, his ruling of 30 Sep). A job, a fare and a letter give an address and a landmark; people asked the way give it by landmark if they know it ('past the chapel, second left') and say 'no idea, try the caff' if not; shopkeepers and the constable always know. After 90 real seconds without progress Frank's own line notes the landmark again, once; after three minutes the next person within 5 m offers the way. A paper map opens on Comma. A newcomer reaches any named place unaided within 3 real minutes.
- Answered 24 Nov (Q20): Frank appears on the paper map only at a sign or landmark, never as a moving marker. Printed things read close (map, fare book, letters, paper, signs, boards) get a final 2026 look as 2D before Unreal, the paper map first (his ruling of 24 Nov). map.json carries 16 landmarks with the words people use for them.
- Standard: Every go-to step named by a landmark reachable unaided in 3 minutes (ER-JOB-01) Test: H: newcomer reaches named places
- Source: DESIGN §4 (DECIDED by the design proof, for him to overturn). Designed in: COPY-2 s.13 'Finding the way'; DESIGN s.4 (ER-JOB-01); DESIGN-ADDENDUM A9; STYLE-SHEET-1990-DRAFT 1.5; RULINGS (paper map, street signs); Q20 and printed things: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: decided. Coverage row: 4.1.3.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-07 every Act I step reachable by landmark with the map shut; 6 of 8 open it less in evening two; decided. None measured.
- Period-correct signs and shop names (catalogue 23 Nov, next tier): Signs and shop names are checked by date. Already the canon gate's job; the part holds landmarks and signs. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 4.1.4 The soft edge

- How it works: A fare that leaves the Hook is driven to the west road or the north road and comes back as time passed and money paid; nothing fails for leaving and nothing loads. A chase, by car or on foot, that reaches the edge ends there as lost within 2 s: the pursuer turns back, Frank goes out and returns after 30 game minutes, and the patrol waits on that road for the rest of the night, so he must come back past it. A plate read within 18 m in light 0.7 or more is noted, and a deed the officer saw brings a constable to the office the next morning at ten. Driving to the edge with no fare offers the six districts by landmark.
- Standard: Nothing fails for leaving (DESIGN §5) Test: S: leaving the map edge in the cab
- Source: DESIGN §5; Study 2 (DECIDED by the design proof, for him to overturn). Designed in: ONE-SHOT-PROMPT s.11; COPY-2 s.10; DESIGN s.5; DEFINITIONS G3, G1
- Status: decided. Coverage row: 4.1.4. Conflicts settled: C-096.
- Studies: aaa-studies/MISSIONS-AND-SIDE-QUESTS.md: MS-01 a job judges the result, never the route; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/places.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G21.

### 4.1.5 Street build rules

- How it works: Study 4's street rules, still rules and not yet a spec: front-to-front width between 9 and 15 m (Quay Street passes); prop density per 10 m of street from a fixed list (bins, signs, boxes, pots, seating, lamps, bikes, litter, post boxes, kiosks) is owed from counts on dated 1988 to 1992 photographs, no bar until counted (the old 5 per 10 m was Mafia's and our own scene's, about 9 per 10 m, neither evidence); dress where the player walks; kit reuse counted per street (the terraces share one family, the shops and Mickey's are one-offs); interiors only where the story goes; every fixed camera's view along the street ends on a building or a turn; one switchable layer per street state (day, night, market, blocked) once the town grows past one street.
- Standard: Study 4's street rules with front to front 9 to 15 m; no prop-density number stands until counted from dated photographs Test: automatic layout check against the rules
- Source: aaa-reference study 04; TRACE s04 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: aaa-reference study 04 'Targets for LEDGER's phase 2'; TRACE s04; RULINGS 17 Nov Reality check (CHECK C25, C26, C27; RESEARCH P2, W1): Mafia is never a reference by his ruling, so the 4.9 and 5 per 10 m have no standing; the only period-adjacent count found is modern central London (6.5 to 15 items per 100 m), an upper bound for a different place. Widths: 1877 model byelaws give new streets at least 11 m, carriageway at least 7.3 m, footways about 1.8 m each; older streets can be narrower; 9 to 15 m is KCD2's median (9.9 m) and a design choice.
- Status: outside. Coverage row: 4.1.5. Conflicts settled: C-097.
- Prior research: game-design/street-spec.md and research/procedural-density: terrace street 6.5 to 7.5 m with 2 m pavements, high street 9 to 10 m with 3 m, block depth 16 to 19 m; research/hitman-density: density is connections, more than one way out and a different way back.

### GD-01 Travel time across the playable map

- How it works: Provisional bands until measured: the Hook is crossed end to end (ferry landing to the north road) on foot in 3 to 5 real minutes and by car in 60 to 100 s. On the G1 plan the car crossing is 548 m with three corners, about 66 s for the ordinary-driving bot at 20 mph (about 44 s at 28 mph); the walking crossing is 475 m, about 4.9 minutes at Frank's 1.6 m/s, taken as 5 real minutes for notice. Every go-to step is reachable unaided in 3 minutes and nothing to do is more than 30 real seconds away by day. To be replaced by the reference games' crossings (KCD2's Kuttenberg, RDR2's Saint Denis, a GTA V district, GTA VI's streets).
- Map file (24 Nov): map.json gives the crossings as 548 m by road and 475 m on foot, the G1 figures, not yet recomputed from the drawn graph; the part stays pending on the reference games' crossings.
- Standard: Provisional bands until measured: on foot 3 to 5 real minutes, by car 60 to 100 s; to be replaced by the reference games' town crossings (KCD2's Kuttenberg, RDR2's Saint Denis, a GTA V district, GTA VI's Vice City streets as a fourth). Test: B: timed crossings by the walk and drive bots on the prototype map.
- Source: ER-JOB-01; the description, section 40; MEASUREMENTS-NEEDED A (travel time). (waits on a dated study). Designed in: DEFINITIONS GD-01, G1, G4; FIT-CHECK F01; MEASUREMENTS-NEEDED A8; COPY-2 s.37
- Status: pending. Coverage row: GD-01. Conflicts settled: C-098.
- Prior research: research/street-scale-test: the Hook 0.107 square km, about 500 m of road, about ten street-lengths; walking every slot about 1.4 km, 422 m for the three nearest copies (a layout, not a crossing time).
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-10 things met per minute and crossing times set from footage; pending. None measured.
- Studies: aaa-studies/MISSIONS-AND-SIDE-QUESTS.md: MS-03 no dead leg over 2 minutes; a job 5 to 30 minutes, planned ones to 45; decided. None measured.
- Prior research: aaa-studies/DENSE-DISTRICT-REVIEWS.md: one writer crossed Like a Dragon's Ijincho in under three minutes avoiding fights; studies/17 gives about 8 minutes for Kamurocho (inferred); crossing times owed from footage (DENSE-10).

### FIT-G1 The Hook's road plan in metres, the chase loop

- How it works: The Hook and its docks on one plan in metres, origin at the ferry landing, x east, y north. Quay Street is the built 48 m street, climbing about 3 m, bending east behind the parade. Roads: quay road 540 m (9 m wide), the bend 42 m, north road 338 m to the soft edge, Chapel Lane 240 m, cold-store road 380 m, dock road 350 m, Basin Road 353 m, basin's north road 260 m, warehouse row 350 m; foot-only lanes: yards' lane 63 m, the terraces' ginnel 345 m, two warehouse cuts of 50 m, six vault places. Footprint about 620 by 400 m (0.25 km2), all reachable. Crossings 548 m by road, 475 m on foot. The chase loop is 1,528 m (76 to 96 s a lap), with a basin ring of about 1,000 m and a third loop of about 910 m sharing six junctions. Chases run 1 to 3 minutes, rich in lanes and yards (R1, his ruling of 24 Nov); how many laps or routes that takes against 76 to 96 s a lap is a gap. The docks are kept (R1), so the old fallback of the 910 m parade loop if the docks are cut is not planned; that loop stays on the map as the parade loop.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 G1, D-Q2; design pass 4 C-01; FIT-CHECK F01, F02, F22; RULINGS 28 Oct and 19 Nov; R1 and the map file: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: ruled. Coverage row: FIT-G1. Conflicts settled: C-099, C-100, C-101, C-102, C-299.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-02 no stretch over 40 m without a door to a place with a person in it; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

## 4.2 The docks

The Hook's working waterfront (canon, 19 Nov).


### 4.2.1 Ferry landing and quay

- How it works: Frank arrives by the Meridian Ferry at about twenty to four on Monday 15 October under a grey sky: a 20 s skippable shot, then control on the gangway, the quay people look at him, and a hint names the way to Quay Street if he stands 4 s. The ferry landing is the plan's origin (0,0); the landing and its rank run 0 to 30 m along the 540 m, 9 m quay road with the quay edge on its south side. The landing's window is 22:00 to 01:00 (the outfit's envelope goes here, and a man says 'Mickey's?'). Dock water: quay edges and ladders (see 4.2.4).
- Answered 24 Nov (Q12): his first hour is restaged as designed (DESIGN section 15), this arrival included. Frank may fish off the quay (Q13; three fishing places in map.json); swimming is out (Q19).
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COPY-2 s.1, s.4; DESIGN s.15; DEFINITIONS G1, G10; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7); Q12, Q13, Q19: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: outside. Coverage row: 4.2.1. Conflicts settled: C-291.
- Prior research: research/south-quay: granite cope 0.60 across, 0.30 deep, 50 mm proud (chosen, no source), setts 100 to 200 mm, wall batter 1 in 20 (chosen), water 3.20 m below the cope at half tide.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G20.

### 4.2.2 Old Basin, fish dock, cold stores

- How it works: The Old Basin's mouth runs 250 to 480 m along the quay road, crossed on the fixed basin bridge; the fish dock is at 480 to 540 m (Brenda Laverack goes there at dawn; 10 to 18 people between 05:30 and 07:00; gulls in flocks of 5 to 20). The Old Basin Cold Stores stand on the cold-store road, north side, x 300 to 470, a 170 m block with a loading yard mouth at x 340; the packing shift leaves them at half past five and is a fare. From rung 3 the cold-store contract makes the packing shift the firm's daily legitimate loop. Basin Road, the basin's north road (the burned warehouse at x 300 to 360) and the warehouse row (Norman Dent's warehouses) complete the working places. The docks stay (R1, his ruling of 24 Nov: the Hook plus its docks kept); 'the docks are cut first' no longer holds. A working crane is ruled in (24 Nov).
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN s.5, s.13, s.14; atlas-01 TOWN-FORM-BIBLE D04; DEFINITIONS G1, G9; COPY-2 s.12, s.31; RULINGS 28 Oct; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7); R1 and the crane: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: outside. Coverage row: 4.2.2. Conflicts settled: C-103, C-291, C-299.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G20, G13, G14.

### 4.2.3 Dock gate, customs, Harbour Board

- How it works: The dock road runs 350 m: the dock gate and its yard mouth at y 210, customs and the Harbour Board at y 20 to 80. All three rivals want the gate, the Hook's way in (the ferry, the Old Basin, customs, the Harbour Board). From rung 3 in Act II: tax collected on his drivers, a man posted, smuggled loads seen; the Harbour Board's counter has an account and a clerk who sells times of shipments; customs has an officer who never reports, by trade, and a bonded store (tobacco and boxed goods, never drink) as a place of risk. A tea stall stands at the gate 22:00 to 06:00. Men of Frank's stand at the gate by the end.
- Ruled in 24 Nov: dock barriers (the gate's striped pole is already a map landmark) and a working crane.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN s.13; COPY-2 s.1, s.31; DEFINITIONS RT-03, G1, G10; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7); dock barriers: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: outside. Coverage row: 4.2.3. Conflicts settled: C-291.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Economy conflict C-333 (run 5): The part says tax is collected on his drivers "from rung 3 in Act II". The design says £5 a car a week once Frank has five cars, until answered; consistent in effect (five cars come at rung 3), the design's figure fills it. RT2-09 says a lost dock gate post brings the tax back; the design leaves the post's £40 a week out of the run. Won: his ruling where one speaks, else the newer economy design.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13, G04, G11, G12.

### 4.2.4 The water's edge

- How it works: Frank never walks or runs into the water: the quay edge stops him like a kerb that cannot be stepped off, and cars cannot leave the quay (bollards and the edge stop them, and a car backs out). In a fight the quay edge is one of the street's places: a man put in climbs out at the nearest ladder within 60 real seconds, soaked and humiliated, and the town talks. An unconscious man face down in the water drowns in about two minutes, a killing to town and police (his decision 6, 25 Nov; combat pass CS-07; C-543). Frank, put in by others, climbs out the same way. Things can be thrown in (a weapon, goods, a bag); what goes in is gone and whoever saw it keeps it. Tested by 30 minutes along every quay edge on foot and by car with no fall in.
- Answered 24 Nov (Q19): swimming is out (the quay edge stops him as written); set climbing places are in.
- Standard: Never stuck (ER-CORE-01); Frank cannot die (his ruling of 12 Oct, archived DECISIONS 13 Oct 02:45); a conscious man never drowns, an unconscious man face down does after about two minutes Test: B: 30 minutes along the quay edge, no fall in; S: a man knocked in climbs out; addendum rules ER-WATER-01 to 02
- Source: DESIGN §1; his rulings (his ruling or canon); drowning of an unconscious man: his decision 6 of 25 Nov. Designed in: ONE-SHOT-PROMPT s.6; COPY-2 s.6; DESIGN-ADDENDUM A11 (ER-WATER-01, 02); DESIGN s.1; Q19: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: ruled (his ruling or canon). Coverage row: 4.2.4.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

## 4.3 Interiors

Rooms where jobs and stories go; every interior designed and photoreal (D14).


### 4.3.1 Mickey's office and yard

- How it works: The office is the front room Frank walks into, built from the room kit: real glass reflecting the street, a 1990 cab office's wear and clutter (radio set, ashtrays, kettle, telephone, scuffed counter), no glitches. From it a door and stair lead to the flat and the yard door at the back; a locked door leads to Mickey's inner office. Its information room is the business: the fare book, the radio nobody can help overhearing, the tin for night money, and a rank outside. The yard has two escapes; the yards' lane (63 m, foot only) leaves it, with one vault place at the back fence taking Frank 0.8 s and a pursuer 1.2 s. The beat constable tries the door on his rounds.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work; ruling 4 Oct (Mickey's office: real glass, 1990 cab office wear) Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon ('Mickey's is a minicab office'); RULINGS 4 Oct; COPY-2 s.1, s.6, s.4; DEFINITIONS G1, G4, G5; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7) Reality check (CHECK C46): the 6 by 8 m shell and the 0.8 s vault are our own; the office size would come from a dated photograph of a cab office or small shop, the vault from reference-game measurement.
- Status: outside. Coverage row: 4.3.1. Conflicts settled: C-291.
- Prior research: game-design/mickeys-office and research/interior-blockout (shell 6 by 8 m); research/cab-office-interior-1990: no openable photograph of a real British minicab office interior dated 1985 to 1995; the one real interior is Brixton 1980, black and white.
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 4.3.2 The flat above

- How it works: The flat is up the stair from the office: Sheila shows it at about minute 4:30 of the first hour, with the fare book, the locked inner door and the debt book. Frank sleeps there; sleeping skips the night, is never a need, and the game saves. Rent of £18 falls on Friday. Named only; not designed beyond: what makes it Frank's rather than Mickey's, and what is in each room.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COPY-2 s.4, s.6; DESIGN s.6, s.9; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7)
- Status: outside. Coverage row: 4.3.2. Conflicts settled: C-291.
- Home as play (catalogue 23 Nov, rank 20; seen in 1 game): The flat: kettle, wireless, letters on the mat, a tin under the floorboards, photographs and letters, never children. Not yet: the flat is named only; things to use there are for the design proof to place. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13.

### 4.3.3 Shops and workplaces

- How it works: Quay Street's shops open 09:00 to 17:30 Monday to Saturday and shut on Sunday; the newsagent 06:00 to 18:00; the caff 06:00 to 15:00 (to 22:00 on Friday and Saturday), tea 30p, a meal £2.50; the launderette (bay 4) 08:00 to 23:00; the pawn (Wayne Harrison) 10:00 to 17:00 with its back room by knock to 22:00 and its window lit at night; the chip shop on the parade to 23:30. Rita Welburn's back room fences at about a third of retail (0.33, CLOUD-FIGURES B3) from rung 2 (her front is the shops' sample); Hal has a shop; the ironmonger sells a crowbar £6, torch £4, key cut £1.50; the ship's chandler stands on the quay road with the boxing club's old hall behind. Nothing serves drink and nobody plays for money.
- Pastimes (24 Nov, Q13): the boxing club, a snooker hall with no money in it, quay fishing, and an allotment pigeon loft with no betting. map.json places them: the snooker hall upstairs on the quay by the landing (x 13 to 33, y 6.6 to 24.6), the boxing club behind the chandler's store (x 210 to 230), three fishing spots along the quay and basin, and the allotments with the pigeon loft on Chapel Lane (x -78 to -24, y 194 to 254). A shop mirror is ruled in (24 Nov).
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN s.6, s.15; COPY-2 s.14, s.29; DEFINITIONS G8, G10; RULINGS 22 Oct, 3 Oct, 8 Nov; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7); Q13 and the shop mirror: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: outside. Coverage row: 4.3.3. Conflicts settled: C-291.
- Prior research: research/shopfronts: stallriser 0.40 to 0.70 m (spec 0.60), fascia at most 0.60 m and a fifth of the front (spec 0.55), mullions 40 to 70 mm proud (spec 48); research/shop-hours-1990; research/shop-window-interiors (one authored room per shop, near 0.6 to 1 m real geometry).
- Data (run 5): exact values in production/lane/blueprint/data/places.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 4.3.4 Homes

- How it works: Ada's front room is where tea is taken at nine ('Ada's pot on at nine'); her window looks on the street Frank must cross, and she sits in a dark front room as the one watcher who is a window; her back gate opens on the terraces' ginnel. The retired doctor's terrace stitches wounds for money (£20) and asks nothing. Other homes are the rooms jobs and stories enter (upstairs flats, back rooms), at least 14 rooms across the eight named places. The collision beat puts a man at Ada's door for Frank.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COPY-2 s.4, s.9, s.31; DESIGN s.6, s.15; DEFINITIONS P34, G1, G8; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7)
- Status: outside. Coverage row: 4.3.4. Conflicts settled: C-104, C-291.
- Prior research: production/art/atlas-02 (search summaries, leads): 18.5% of homes without central heating, satellite dishes about 1 in 20 to 30 homes, Squarials dead after November 1990; research/phase5-procedural brick and window figures from a dated photograph.
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 4.3.5 Iveson's yard and hut

- How it works: Dennis Iveson's yard and hut stand on Basin Road, y 260 to 320. He owes Mickey's book £80, has the money, and keeps a yard hand in his twenties; he was bought out of the burned warehouse. Three ways in to the debt: front up the yard hand, come back for the hut at night, or lean on what he bought out of the fire. Darren's tip puts the hut as a break-in. It is one of the eight named enterable places.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: ONE-SHOT-PROMPT s.15, s.25; COPY-2 s.4, s.5, s.30; DEFINITIONS G1, P34; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7)
- Status: outside. Coverage row: 4.3.5. Conflicts settled: C-291.
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### 4.3.6 The chapel and hall

- How it works: The chapel and the closed school stand on Chapel Lane, x -20 to 60. Father Brendan Walsh is met by the chapel and in the street, with his own street lines and memory; the first fare goes to the priest's house by the chapel. The hall holds an evening of tea and talk on Tuesday 19:00 to 21:30 and is one of the eight enterable places; Sunday the chapel is busy and Remembrance Sunday is kept there. Religion is part of life, never mocked and never a mechanic. The school stands closed and nobody is in it.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon content rule; COPY-2 s.4, s.5, s.29; DEFINITIONS G1, G10, RT-09; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7)
- Status: outside. Coverage row: 4.3.6. Conflicts settled: C-291.
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G08.

### 4.3.7 The police station

- How it works: The station is where custody happens: a constable walks up (go with him, or run), then the station, the duty solicitor (free) and the hours pass, under 2 real minutes of play. About 6 hours for a window (2 and a caution if he owns up), 8 for a wounding, 12 for a robbery, 22 for a killing, then charged and remanded, or released without charge or on police bail pending inquiries. The coat is kept if he wore it; he is never taken twice for one deed. Two named officers can be bought (£50 to look away from a car once, £200 to lose a statement once); Ellis can be bought too, once: about 800 pounds, then 100 a week, and a missed week ends it (his ruling of 24 Nov, Q5). At dial state Fired armed officers come from the station slowly.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: ONE-SHOT-PROMPT s.20, s.21; COPY-2 s.17, s.18, s.27; DEFINITIONS G8; CLOUD-FIGURES-2026-11-21 B2; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7); Q5: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: outside. Coverage row: 4.3.7. Conflicts settled: C-105, C-291, C-294.
- Economy conflict C-328 (run 5): Settled: the part now carries his ruling of 24 Nov (Ellis can be bought, about £800 then £100 a week). Still open: nothing.

### 4.3.8 Where a beaten Frank wakes

- How it works: Beaten, Frank comes round on the pavement, in Grace Rinaldi's kitchen or in the hospital, sometimes robbed, with a street that knows he lost, in control within 60 real seconds with the cost said. Hospital costs days, never money, and plants a witness; the retired doctor costs money (stitches £20). Bruises and a cut lip last three game days, a limp one. The ambulance for a hit person comes in about ten game minutes and takes them to hospital.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COPY-2 s.5, s.9, s.11, s.41; DESIGN s.7; DEFINITIONS G8, P04; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7)
- Status: outside. Coverage row: 4.3.8. Conflicts settled: C-291.

### GV-04 Places stay open

- How it works: Every building used in a job stays enterable afterwards, as a place in someone's life, unless the story closes it and says so. Checked by walking back into every interior a job used. Private rooms stay private (the owner warns as before).
- Standard: Every interior used once can be entered again after its job, or its closing is said in the world. Test: B: after each job, a walk back into every interior it used.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP-2026-11-21 GV-04; production/research/lane/gtavi/YARDSTICK.md Y4.2; COPY-2 s.40; DEFINITIONS P34
- Status: decided. Coverage row: GV-04.

### FIT-P34 At least 24 rooms open

- How it works: At least 24 rooms can be entered: the 8 named places with their back rooms and upstairs (at least 14 rooms between them) and at least 10 break-in rooms that jobs name. Every other door says it is locked. Every enterable room has at least one usable object. Checked by counting the map data and a walker bot that opens every door.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 P34; FIT-CHECK P34; ONE-SHOT-PROMPT s.15
- Status: decided. Coverage row: FIT-P34.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-02 no stretch over 40 m without a door to a place with a person in it; decided. None measured.
- Prep: INVENTORY section 2: needed 27 or more enterable rooms (24 plus the three rival bases, raided as break-ins with men inside, RT2-08); the prototype has 17; built from room kits in map.js, about 5 hours if made in the one-shot.
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

## 4.4 Props and street furniture

Lamps, the phone box, bins, railings, bollards, signs.
- Prior research: production/cloud-week/targets and research/street-clutter-1990: pillar box 390 mm across, 1,500 high (the earlier 489 is wrong); KX100 kiosk 890 mm square, about 2,190 tall; concrete lamp columns, low-pressure sodium (Quay Street: two about 34 m apart by the period code, his ruling of 24 Nov, advisor 371; earlier writing said four); no tactile paving in 1990; skip plates (1984 regulations); to-let boards (SI 1989/670).

### 4.4 Props and street furniture

- How it works: Quay Street's furniture: two concrete lamp columns about 34 m apart (his ruling of 24 Nov, advisor 371; lamp_post_C, 220 mm square at the foot tapering to 125 mm, lantern top at 5.0 m, unpainted concrete), staining still to finish; boat-shaped aluminium lanterns with 35 W low-pressure sodium lamps, each a straight-down pool (cone 22 to 46 degrees, 167 lm) plus a 40 lm bulb glow reaching 1 m, 4.83 m up, giving pools with darkness between. The KX100 phone box stays; no skip or pallets until real. Street name plates in Marcellus SC. Sources in order: free CC0 or unmarked CC-BY first, else the studio's own from photographs. Prop density per 10 m: no bar until counted on dated 1988 to 1992 photographs (the old bar of 5 was Mafia's and our own scene's).
- Standard: Every visual judged against the Hook sheet and KCD2 frames, photographs win on shape and material, measured values and the Hook sheet on colour (R7, his ruling of 24 Nov); yes only for 2026-grade work; prop density per 10 m owed from dated photographs; Quay Street lamps about 34 m apart (advisor 371); 3 Oct sources (free first, else the studio's own from photographs) Test: small-piece review (RULINGS 3 Nov)
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate; ruling 3 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: TARGET-STREET-FURNITURE-2026-11-17 S1 to S4; FURNITURE-SPECS-2026-11-17; RULINGS 22 Oct, 2 Oct, 3 Oct, 1 Oct; Study 4; colour rule: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R7) Lamps: his ruling of 24 Nov (advisor 371), BS 5489-3:1977 B5/6 spacing (RESEARCH L1); 35 W low-pressure sodium is a real period rating (35, 55, 90 W; lamptech.co.uk), but the 5.0 m column and one model everywhere are our choice (CHECK G19, C7). Phone boxes: BT had about 100,000 in 1992 (Hansard 12 Feb 1992; Ofcom gives 92,000), roughly 3 to 6 for a district this size (inferred, low confidence); the map's three sit inside it (RESEARCH P1).
- Status: outside. Coverage row: 4.4. Conflicts settled: C-106, C-291.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### FIT-P52 What an ordinary drawer holds

- How it works: Outside jobs, an ordinary drawer or cupboard in an enterable room holds one of a small written set: letters, a bill, a photograph, a few coins up to £2, cigarettes, a spare key to that room; never a job's thing. Searching it is the same act with the same noise and memory as in a job. Nothing found there is worth more than £2.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 P52; FIT-CHECK P52; ONE-SHOT-PROMPT s.15
- Status: decided. Coverage row: FIT-P52.

## 4.5 Traffic and parked cars

AI drivers that always brake for people; parked cars from the kit.


### 4.5.1 Traffic drivers

- How it works: Traffic stage 1 is the background cars at the street's end. Each lane draws arrivals from a seeded stream, so the same week plays the same: average gaps 50 s in the rush hours, 75 s by day, 150 s in the evening, 450 s at night, never under 4 s in one lane, at most three cars in the pool. Cars drive 20 to 28 mph (never over 30), follow the Intelligent Driver Model, slow to 20 mph from 60 m before Quay Street's mouth, and stop about 2 m behind a person in the lane, hooting at 3 s and 10 s. A person who steps out inside stopping distance (23 m at 30 mph) is never struck: the car halts dead. Only the player's car can strike anybody; AI drivers always brake, a crewman told to drive too.
- Standard: AI drivers always brake for people (canon); ER-DRIVE-04 Test: S: 1,000 seeded crossings; 40 minutes lawful driving with no hits
- Source: canon; DESIGN §5 (his ruling or canon). Designed in: TRAFFIC-STAGE1-REFERENCE-MODEL-2026-11-18; COPY-2 s.10, s.11; DESIGN s.5 (ER-DRIVE-04); DEFINITIONS G2; canon (cars)
- Status: ruled (his ruling or canon). Coverage row: 4.5.1. Conflicts settled: C-107.
- Prior research: research/traffic (TRAFFIC-COST-2026-11-17): at most two moving cars in view, one every 40 to 90 s by day, 15 to 20 mph, density by hour 1.0 at 07 to 10 and 17 to 20, 0.8 by day, 0.2 in the small hours; the 0.5 ms budget for up to six cars is unmeasured.
- Traffic that indicates and yields to sirens (catalogue 23 Nov, next tier): Cars indicate and pull aside for a siren. Partly: traffic stops for people and slows at the street mouth; indicating and yielding are not named. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G14, G04.

### 4.5.2 Parked cars

- How it works: The studio's own scripted Blender hatchback goes first as the one parked car; the other three follow only after he has seen it. Kerb places are held in production/specs/street-vehicles.json; budget 40,000 triangles, 4 LODs, 2,048 px, simple collision, at most six cars in view at 0.5 ms. P9 gate: a blind reviewer on the untextured body names no model with confidence and places it in Britain or Europe, 1985 to 1991. Traffic from their kit follows in the friends' build after one passes. Nothing is bought for street or cars.
- Standard: His look at one parked car before twenty (ruling 17 Nov) Test: the gate
- Source: RULINGS cars 17 Nov (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: PLAN-PARKED-CARS-2026-11-17; RULINGS 17 Nov, 6 Nov, 16 Sep; canon 'Brands and law'
- Status: outside. Coverage row: 4.5.2.
- Prior research: research/period-vehicles-and-props: Ford, Vauxhall and Rover about 55% of the 1990 market; plates G until 31 Jul 1990, then H; police cars with a white stripe, no Battenburg; buses deregulated 26 Oct 1986; the car script's 15,000-triangle bevelled boxes were partly a Nanite stand-in fault.

## 4.6 Vehicles

The firm's cabs, period cars, police cars and vans, all fictional.


### 4.6.1 Car designs

- How it works: Every vehicle is fictional: no real car models or makes. Method: invented makers with an ethos, blend a class, never copy a car; each design passes the P9 blind silhouette check. The firm's cars are two tired cabs at the start and five at rung 3, with the roof sign and plate making a cab the firm's; a used car at the lot costs £600 to £1,200. The traffic hatch has a second variant and 8 colours.
- Standard: Fictional makes only; no real car models (canon) Test: the gate; a look-alike check against real makes
- Source: canon Brands and law (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon 'Brands and law'; PLAN-PARKED-CARS s.2; TRAFFIC-STAGE1 rule 3; DEFINITIONS RT-04, G8
- Status: outside. Coverage row: 4.6.1.
- Prior research: research/field-scans (public blog): background cars 5,000 to 25,000 triangles, hero 40,000 to 80,000, hatchback first; research/asset-plan: nothing free fits, own design in Blender.

### 4.6.2 Working vehicles

- How it works: Named only; not designed beyond: boats and buses are scenery (ruling 23 Sep). The sources mention vans and lorries only as things in events (goods off a van or lorry are a lift; a van broken down across the lane; a crate off a lorry at the dock gate; lorry-delivered fish), a police car no faster than Frank's car on a straight (stops a driver at 50 mph or more), and an ambulance that arrives about ten game minutes after help is called. No dock truck has a design.
- Standard: Boats and buses scenery (ruling 23 Sep) Test: the gate
- Source: RULINGS 23 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 23 Sep; COPY-2 s.3, s.11, s.14; DEFINITIONS G2, G6
- Status: outside. Coverage row: 4.6.2.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G14, G20.

## 4.7 Day and night

The clock's light: day and night now, four or five states later, no moving sun.
- Prior research: research/evening-light-1990: low-pressure sodium 589 nm, about sRGB 255,140,0, warm-up red-pink then yellow-orange; 35 W lantern about 4,550 lm (unverified); about 10 lux under the lamp, 0.5 midway at 30 m (inferred); real night photographs 3.0 to 5.2 stops pool to gap; autumn dark by about 20:00. The 4500 K Mafia lamp has lapsed.
- Studies: aaa-studies/DENSE-DISTRICT-REVIEWS.md: DENSE-08 the night is its own street; a third of jobs and side stories after dark; decided. None measured.

### 4.7 Day and night

- How it works: Day and night now, four or five light states later, no moving sun (7 Oct). Night is pools of lamp light with darkness between and lit windows, never one orange wash (1 Oct); dusk comes with the lamps switching on (about 70 lux, the sodium taking 8 to 15 minutes to turn full yellow). Day exposure stays one stop darker (29 Oct). Sound carries about twice as far in the small hours. Frank and the ground 5 m round him stay readable at night; the frame's corners darken with the same light value the watchers use. Under the 24 Nov clock a game day is 48 real minutes (120 real seconds a game hour) and the dark part about 28 of them (recomputed for the 48-minute day, his ruling of 24 Nov).
- Standard: Ruling 7 Oct; night as pools of lamp light with dark between (1 Oct) Test: the gate at night
- Source: RULINGS weather and night (his ruling or canon). Designed in: DESIGN s.6 (ER-NIGHT-01, 02); LIGHT-WEATHER-VALUES-2026-11-17; RULINGS 1 Oct, 7 Oct, 29 Oct; DEFINITIONS CLK-05; clock: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R2); map.json carries realSecondsPerGameHour 120
- Status: ruled (his ruling or canon). Coverage row: 4.7. Conflicts settled: C-108, C-109, C-292.
- Data (run 5): exact values in production/lane/blueprint/data/light-weather.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12.

## 4.8 Weather

Dry overcast, drizzle, rain; one wetness value drives look, sight, sound and who is out.
- Prior research: research/phase2-plan TARGET-LIGHT-WEATHER-2026-11-17: EV100 11 to 12.8 by day (two real rainy exposures 11.9 and 12.3); overcast noon 6,000 to 18,000 lux; British overcast about 2 to 1 over sun (1,403 sunshine hours a year at 54.5 N).

### 4.8 Weather

- How it works: Weather comes as weighted profiles: dry overcast, drizzle, rain; never sunshine in the friends' build. One wetness value drives the look (wet street dark and glistening, mirroring sky and buildings, puddles that are water), what is seen and heard, and who is out: rain cuts sight and sound, halves the voices, empties the street (each crowd band halved), lowers car grip and makes the road slippery. The same seed played dry, in drizzle and in rain gives three different streets, the same each time. A wet road takes about 3 to 14 hours to dry and puddles days; rain on about 12 days a month is the working assumption.
- Standard: Grey range only, never sunshine in the friends' build (5 Oct); one wetness value (DESIGN §6) Test: S: same seed in three weathers
- Source: RULINGS 5 Oct; DESIGN §6 (his ruling or canon). Designed in: DESIGN s.6 (ER-NIGHT-03); LIGHT-WEATHER-VALUES-2026-11-17; COPY-2 s.5, s.10; DEFINITIONS G9; RULINGS 5 Oct
- Status: ruled (his ruling or canon). Coverage row: 4.8.
- Data (run 5): exact values in production/lane/blueprint/data/light-weather.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12, G19.

## 4.9 1990 detail

Signage, poll-tax posters, the brand bible's owed brands, CCTV at the bank, phone boxes.
- Prior research: about thirty dated Geograph photographs of 1975 to 1995 (production/cloud-week), TSRGD road markings, poll-tax posters as an invented campaign, canon's CCTV and camcorder; search-summary figures stay leads until re-read.

### 4.9 1990 detail

- How it works: Late-analog 1990: landlines, phone boxes, answering machines, pagers, cash and paper; no mobiles, no internet. CCTV only at the bank (answered 24 Nov, Q10: the bank the only CCTV), one camcorder in town as a rare witness. Poll-tax posters are an invented local campaign, never real parties or people. Money is pounds and pence only, written plain; typed letters in Courier Prime, street plates in Marcellus SC. The brand bible still owes six names: the football club, the local paper, the pirate radio station, the regional TV channel, the telephone operator (kiosk mark) and the postal cypher. The interface style sheet is a draft, nothing ruled.
- Printed things read close (letters, paper, signs, boards, the fare book, the map) get a final 2026 look as 2D before Unreal, the paper map first (his ruling of 24 Nov).
- Standard: canon era; late-analog; brand bible owes the football club, paper, pirate radio, TV channel, phone operator, postal cypher Test: canon-gate and content-gate; his eye
- Source: canon Era, Brands and law (his ruling or canon). Designed in: canon 'Era' and 'Brands and law'; STYLE-SHEET-1990-DRAFT-2026-11-18; RULINGS 3 Oct; COPY-2 s.2, s.5; Q10 and printed things: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: ruled (his ruling or canon). Coverage row: 4.9. Conflicts settled: C-110.
- Class shown in heating (catalogue 23 Nov, next tier): Gas fire, storage heater, coal fire and paraffin heater as set dressing. Partly: the part gives the share of homes without central heating; the dressing by class is not named. Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/letters-and-print.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G20.

## 4.10 Pubs without drink and the closed school

Places that exist with no drink and no children.
- Prior research: production/specs/the-pub-without-drink.md; atlas-02's facts stand only for the building's front of boarded or food-serving pubs, never for drink; atlas-01's pub, cask line and betting offices, and the pub-regular line bank, are void under the content rule.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-02 every daily act pays in the town; decided. None measured.

### 4.10 Pubs without drink and the closed school

- How it works: Pubs may stand as buildings on the street, boarded or serving food, never entered for drink; Mickey's is a minicab office (D19, superseding D15's pub). Alcohol and gambling are out entirely, in image and speech, and nobody can bet on anything, including at the boxing club. The school stands closed for the game's window: the building is there and nobody is in it; no children are rendered, in the crowd or in dialogue. Enforced at six sites including the animation library by clip name. Tuesday's chapel hall evening (tea and talk) is the model for a place that exists without drink.
- Answered 24 Nov (Q13): the snooker hall has no money in it and the allotment pigeon loft no betting; the content rule above holds.
- Standard: canon content rule: pubs as places, boarded or serving food; the school stands closed Test: content gate over clips and props
- Source: canon D18 (his ruling or canon). Designed in: canon content rule (D18) and Mickey's (D19); COPY-2 s.3, s.29; DEFINITIONS G10; Q13: his ruling of 24 Nov (RULINGS on wip, his decisions page)
- Status: ruled (his ruling or canon). Coverage row: 4.10. Conflicts settled: C-111.

## 4.11 Animals and birds

Gulls and pigeons on a port street; dogs on a lead.


### 4.11.1 Yard dogs

- How it works: A dog in a yard barks at a stranger: a bark is a noise at its reach that draws the owner, so the dog is a witness by sound only. A scrap of food quiets it for a while. Dogs are never hurt: no verb harms a dog or any animal (ER-DOG-01, checked by trying every verb). One dog is loose on the quay as a street happening.
- Standard: A bark is a noise at its reach (DESIGN §2); no harm to animals shown Test: S: a bark draws the owner within the rule; addendum rules ER-DOG-01
- Source: DESIGN §2 (DECIDED by the design proof, for him to overturn). Designed in: ONE-SHOT-PROMPT s.8; DESIGN-ADDENDUM A23; DEFINITIONS P45
- Status: decided. Coverage row: 4.11.1.

### FIT-P45 Birds and animals

- How it works: Gulls on the fish dock and the quay (flocks of 5 to 20 in daylight, crying, rising when someone runs at them), pigeons on the parade, a few cats in the yards at night, the yard dogs, and the one dog loose on the quay as a happening. No animal is hurt by any verb; a gull rising is a small noise that draws a glance. Gulls are present on the fish dock every daylight hour in dry weather.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 P45; FIT-CHECK P45; DESIGN-ADDENDUM A23
- Status: decided. Coverage row: FIT-P45.
- Animals with their own lives (catalogue 23 Nov, rank 9; seen in 3 games): Gulls, pigeons, cats and yard dogs are carried. Partly: short are a fox at the bins, a dog outside the butcher's and a dog Frank can pat, with no verb harming it. Feature only; no timing; the part's status is unchanged.
