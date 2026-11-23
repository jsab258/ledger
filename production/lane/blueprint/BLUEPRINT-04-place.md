# BLUEPRINT 04: The place

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. Meridian's Hook and its docks: one port, dense, known by heart.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 4.1 The Hook's layout

The map as data with testable layout rules.


### 4.1.1 Quay Street

- How it works: Quay Street is the built street, in the Hook, Mickey's on it: 48 m from the quay, climbing about 3 m, then bending east behind the parade, 11 m wide with both pavements. The east side is the six-bay parade; the west block across from the north half of the parade carries shops; the west block across from Mickey's, at the quay end, is plain terraces. Trades by bay: 1 fishmonger, 3 the empty unit to let (whitewashed), 4 launderette, 5 grocer; west north: a newsagent and tobacconist, an ironmonger, a tea room. Four concrete lamp columns stand at x 8 east, 18 west, 28 east, 38 west. The 593 pieces keep their east_parade_ identifiers, which carry no claim about location. Every visual is judged against the Hook sheet and KCD2 frames; dated photographs win.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work; canon's three sides Test: the gate; his eye on whole street frames
- Source: canon; RULINGS The look (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon ('The built street', 'Quay Street's three sides'); RULINGS 'The look and the street' (3 Oct trades, 5 Oct atlas); DEFINITIONS G1; TARGET-STREET-FURNITURE-2026-11-17 S1
- Status: outside. Coverage row: 4.1.1. Conflicts settled: C-077, C-078.

### 4.1.2 The rest of the Hook

- How it works: The rest of the Hook is the G1 road plan: a quay road of 540 m, a north road of 338 m to the soft edge, Chapel Lane 240 m, the cold-store road 380 m, the dock road 350 m, Basin Road 353 m, the warehouse row 350 m, and foot-only lanes (the yards' lane 63 m, the terraces' ginnel 345 m, two 50 m warehouse cuts) with six vault places. About 620 by 400 m, all reachable. Density goes up and back, not out: back rooms, yards, alleys, upstairs flats. The look follows the Hook sheet and KCD2 frames, with a thinner dressing away from Quay Street where the player does not walk.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work; density up and back, not out (Study 17) Test: the gate; B navigation soak
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate; DESIGN §6 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: atlas-01 (DISTRICTS, TOWN-FORM-BIBLE); DEFINITIONS G1; DESIGN s.6; Study 4 target 3; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.1.2. Conflicts settled: C-079, C-080.

### 4.1.3 Landmarks and signs

- How it works: Every door that matters has a number and every street a name plate at its ends (Marcellus SC, his ruling of 30 Sep). A job, a fare and a letter give an address and a landmark; people asked the way give it by landmark if they know it ('past the chapel, second left') and say 'no idea, try the caff' if not; shopkeepers and the constable always know. After 90 real seconds without progress Tom's own line notes the landmark again, once; after three minutes the next person within 5 m offers the way. A paper map opens on Comma. A newcomer reaches any named place unaided within 3 real minutes.
- Standard: Every go-to step named by a landmark reachable unaided in 3 minutes (ER-JOB-01) Test: H: newcomer reaches named places
- Source: DESIGN §4 (DECIDED by the design proof, for him to overturn). Designed in: COPY-2 s.13 'Finding the way'; DESIGN s.4 (ER-JOB-01); DESIGN-ADDENDUM A9; STYLE-SHEET-1990-DRAFT 1.5; RULINGS (paper map, street signs)
- Status: decided. Coverage row: 4.1.3.

### 4.1.4 The soft edge

- How it works: A fare that leaves the Hook is driven to the west road or the north road and comes back as time passed and money paid; nothing fails for leaving and nothing loads. A chase, by car or on foot, that reaches the edge ends there as lost within 2 s: the pursuer turns back, Tom goes out and returns after 30 game minutes, and the patrol waits on that road for the rest of the night, so he must come back past it. A plate read within 18 m in light 0.7 or more is noted, and a deed the officer saw brings a constable to the office the next morning at ten. Driving to the edge with no fare offers the six districts by landmark.
- Standard: Nothing fails for leaving (DESIGN §5) Test: S: leaving the map edge in the cab
- Source: DESIGN §5; Study 2 (DECIDED by the design proof, for him to overturn). Designed in: ONE-SHOT-PROMPT s.11; COPY-2 s.10; DESIGN s.5; DEFINITIONS G3, G1
- Status: decided. Coverage row: 4.1.4. Conflicts settled: C-081.

### 4.1.5 Street build rules

- How it works: Study 4's street rules, still rules and not yet a spec: front-to-front width between 9 and 15 m (Quay Street passes); at least 5 props per 10 m of street from a fixed list (bins, signs, boxes, pots, seating, lamps, bikes, litter, post boxes, kiosks), the Quay Street scene file placing about 9 per 10 m; dress where the player walks; kit reuse counted per street (the terraces share one family, the shops and Mickey's are one-offs); interiors only where the story goes; every fixed camera's view along the street ends on a building or a turn; one switchable layer per street state (day, night, market, blocked) once the town grows past one street.
- Standard: Study 4's measured street rules Test: automatic layout check against the rules
- Source: aaa-reference study 04; TRACE s04 (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: aaa-reference study 04 'Targets for LEDGER's phase 2'; TRACE s04; RULINGS 17 Nov
- Status: outside. Coverage row: 4.1.5. Conflicts settled: C-082.

### GD-01 Travel time across the playable map

- How it works: Provisional bands until measured: the Hook is crossed end to end (ferry landing to the north road) on foot in 3 to 5 real minutes and by car in 60 to 100 s. On the G1 plan the car crossing is 548 m with three corners, about 66 s for the ordinary-driving bot at 20 mph (about 44 s at 28 mph); the walking crossing is 475 m, about 4.9 minutes at Tom's 1.6 m/s, taken as 5 real minutes for notice. Every go-to step is reachable unaided in 3 minutes and nothing to do is more than 30 real seconds away by day. To be replaced by the reference games' crossings (KCD2's Kuttenberg, RDR2's Saint Denis, a GTA V district, GTA VI's streets).
- Standard: Provisional bands until measured: on foot 3 to 5 real minutes, by car 60 to 100 s; to be replaced by the reference games' town crossings (KCD2's Kuttenberg, RDR2's Saint Denis, a GTA V district, GTA VI's Vice City streets as a fourth). Test: B: timed crossings by the walk and drive bots on the prototype map.
- Source: ER-JOB-01; the description, section 40; MEASUREMENTS-NEEDED A (travel time). (waits on a dated study). Designed in: DEFINITIONS GD-01, G1, G4; FIT-CHECK F01; MEASUREMENTS-NEEDED A8; COPY-2 s.37
- Status: pending. Coverage row: GD-01. Conflicts settled: C-083.

### FIT-G1 The Hook's road plan in metres, the chase loop

- How it works: The Hook and its docks on one plan in metres, origin at the ferry landing, x east, y north. Quay Street is the built 48 m street, climbing about 3 m, bending east behind the parade. Roads: quay road 540 m (9 m wide), the bend 42 m, north road 338 m to the soft edge, Chapel Lane 240 m, cold-store road 380 m, dock road 350 m, Basin Road 353 m, basin's north road 260 m, warehouse row 350 m; foot-only lanes: the yards' lane 63 m, the terraces' ginnel 345 m, two warehouse cuts of 50 m, with six vault places. The footprint is about 620 by 400 m (0.25 km2), all reachable. The chase loop is 1,528 m (76 to 96 s a lap at 35 to 45 mph), with a basin ring of about 1,000 m and a third loop of about 910 m sharing six junctions. If the docks are cut, the loop goes with them and chases shorten to 45 s.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 G1 and D-Q2; FIT-CHECK F01, F02, F22; RULINGS 5 Oct, map ruling
- Status: decided. Coverage row: FIT-G1. Conflicts settled: C-084, C-085.

## 4.2 The docks

The Hook's working waterfront (canon, 19 Nov).


### 4.2.1 Ferry landing and quay

- How it works: Tom arrives by the Meridian Ferry at about twenty to four on Monday 15 October under a grey sky: a 20 s skippable shot, then control on the gangway, the quay people look at him, and a hint names the way to Quay Street if he stands 4 s. The ferry landing is the plan's origin (0,0); the landing and its rank run 0 to 30 m along the 540 m, 9 m quay road with the quay edge on its south side. The landing's window is 22:00 to 01:00 (the outfit's envelope goes here, and a man says 'Mickey's?'). Dock water: quay edges and ladders (see 4.2.4).
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COPY-2 s.1, s.4; DESIGN s.15; DEFINITIONS G1, G10; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.2.1.

### 4.2.2 Old Basin, fish dock, cold stores

- How it works: The Old Basin's mouth runs 250 to 480 m along the quay road, crossed on the fixed basin bridge; the fish dock is at 480 to 540 m (Brenda Laverack goes there at dawn; 15 to 25 people between 05:30 and 07:00; gulls in flocks of 5 to 20). The Old Basin Cold Stores stand on the cold-store road, north side, x 300 to 470, a 170 m block with a loading yard mouth at x 340; the packing shift leaves them at half past five and is a fare. From rung 3 the cold-store contract makes the packing shift the firm's daily legitimate loop. Basin Road, the basin's north road (the burned warehouse at x 300 to 360) and the warehouse row (Norman Dent's warehouses) complete the working places. If time runs short the docks are cut first.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN s.5, s.13, s.14; atlas-01 TOWN-FORM-BIBLE D04; DEFINITIONS G1, G9; COPY-2 s.12, s.31; RULINGS 28 Oct; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.2.2. Conflicts settled: C-086.

### 4.2.3 Dock gate, customs, Harbour Board

- How it works: The dock road runs 350 m: the dock gate and its yard mouth at y 210, customs and the Harbour Board at y 20 to 80. All three rivals want the gate, the Hook's way in (the ferry, the Old Basin, customs, the Harbour Board). From rung 3 in Act II: tax collected on his drivers, a man posted, smuggled loads seen; the Harbour Board's counter has an account and a clerk who sells times of shipments; customs has an officer who never reports, by trade, and a bonded store (tobacco and boxed goods, never drink) as a place of risk. A tea stall stands at the gate 22:00 to 06:00. Men of Tom's stand at the gate by the end.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN s.13; COPY-2 s.1, s.31; DEFINITIONS RT-03, G1, G10; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.2.3.

### 4.2.4 The water's edge

- How it works: Tom never walks or runs into the water: the quay edge stops him like a kerb that cannot be stepped off, and cars cannot leave the quay (bollards and the edge stop them, and a car backs out). In a fight the quay edge is one of the street's places: a man put in climbs out at the nearest ladder within 60 real seconds, soaked and humiliated, and the town talks. Water never kills. Tom, put in by others, climbs out the same way. Things can be thrown in (a weapon, goods, a bag); what goes in is gone and whoever saw it keeps it. Tested by 30 minutes along every quay edge on foot and by car with no fall in.
- Standard: Never stuck (ER-CORE-01); Tom cannot die (his ruling); water never kills Test: B: 30 minutes along the quay edge, no fall in; S: a man knocked in climbs out; addendum rules ER-WATER-01 to 02
- Source: DESIGN §1; his rulings (his ruling or canon). Designed in: ONE-SHOT-PROMPT s.6; COPY-2 s.6; DESIGN-ADDENDUM A11 (ER-WATER-01, 02); DESIGN s.1
- Status: measured. Coverage row: 4.2.4.

## 4.3 Interiors

Rooms where jobs and stories go; every interior designed and photoreal (D14).


### 4.3.1 Mickey's office and yard

- How it works: The office is the front room Tom walks into, built from the room kit: real glass reflecting the street, a 1990 cab office's wear and clutter (radio set, ashtrays, kettle, telephone, scuffed counter), no glitches. From it a door and stair lead to the flat and the yard door at the back; a locked door leads to Mickey's inner office. Its information room is the business: the fare book, the radio nobody can help overhearing, the tin for night money, and a rank outside. The yard has two escapes; the yards' lane (63 m, foot only) leaves it, with one vault place at the back fence taking Tom 0.8 s and a pursuer 1.2 s. The beat constable tries the door on his rounds.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work; ruling 4 Oct (Mickey's office: real glass, 1990 cab office wear) Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon ('Mickey's is a minicab office'); RULINGS 4 Oct; COPY-2 s.1, s.6, s.4; DEFINITIONS G1, G4, G5; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.3.1.

### 4.3.2 The flat above

- How it works: The flat is up the stair from the office: Sheila shows it at about minute 4:30 of the first hour, with the fare book, the locked inner door and the debt book. Tom sleeps there; sleeping skips the night, is never a need, and the game saves. Rent of £18 falls on Friday. Named only; not designed beyond: what makes it Tom's rather than Mickey's, and what is in each room.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COPY-2 s.4, s.6; DESIGN s.6, s.9; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.3.2.

### 4.3.3 Shops and workplaces

- How it works: Quay Street's shops open 09:00 to 17:30 Monday to Saturday and shut on Sunday; the newsagent 06:00 to 18:00; the caff 06:00 to 15:00 (to 22:00 on Friday and Saturday), tea 30p, a meal £2.50; the launderette (bay 4) 08:00 to 23:00; the pawn (Wayne Harrison) 10:00 to 17:00 with its back room by knock to 22:00 and its window lit at night; the chip shop on the parade to 23:30. Rita Welburn's back room fences at about 0.4 of an honest price from rung 2 (her front is the shops' sample); Hal has a shop; the ironmonger sells a crowbar £6, torch £4, key cut £1.50; the ship's chandler stands on the quay road with the boxing club's old hall behind. Nothing serves drink and nobody plays for money.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: DESIGN s.6, s.15; COPY-2 s.14, s.29; DEFINITIONS G8, G10; RULINGS 22 Oct, 3 Oct, 8 Nov; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.3.3.

### 4.3.4 Homes

- How it works: Ada's front room is where tea is taken at nine ('Ada's pot on at nine'); her window looks on the street Tom must cross, and she sits in a dark front room as the one watcher who is a window; her back gate opens on the terraces' ginnel. The retired doctor's terrace stitches wounds for money (£20) and asks nothing. Other homes are the rooms jobs and stories enter (upstairs flats, back rooms), at least 14 rooms across the eight named places. The collision beat puts a man at Ada's door for Tom.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COPY-2 s.4, s.9, s.31; DESIGN s.6, s.15; DEFINITIONS P34, G1, G8; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.3.4. Conflicts settled: C-087.

### 4.3.5 Iveson's yard and hut

- How it works: Dennis Iveson's yard and hut stand on Basin Road, y 260 to 320. He owes Mickey's book £80, has the money, and keeps a yard hand in his twenties; he was bought out of the burned warehouse. Three ways in to the debt: front up the yard hand, come back for the hut at night, or lean on what he bought out of the fire. Darren's tip puts the hut as a break-in. It is one of the eight named enterable places.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: ONE-SHOT-PROMPT s.15, s.25; COPY-2 s.4, s.5, s.30; DEFINITIONS G1, P34; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.3.5.

### 4.3.6 The chapel and hall

- How it works: The chapel and the closed school stand on Chapel Lane, x -20 to 60. Father Brendan Walsh is met by the chapel and in the street, with his own street lines and memory; the first fare goes to the priest's house by the chapel. The hall holds an evening of tea and talk on Tuesday 19:00 to 21:30 and is one of the eight enterable places; Sunday the chapel is busy and Remembrance Sunday is kept there. Religion is part of life, never mocked and never a mechanic. The school stands closed and nobody is in it.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon content rule; COPY-2 s.4, s.5, s.29; DEFINITIONS G1, G10, RT-09; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.3.6.

### 4.3.7 The police station

- How it works: The station is where custody happens: a constable walks up (go with him, or run), then the station, the duty solicitor (free) and the hours pass, under 2 real minutes of play. About 6 hours for a window (2 and a caution if he owns up), 8 for a wounding, 12 for a robbery, 22 for a killing, then charged and remanded or released under investigation. The coat is kept if he wore it; he is never taken twice for one deed. Two named officers can be bought (£50 to look away from a car once, £200 to lose a statement once); Ellis is not among them. At dial state Fired armed officers come from the station slowly.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: ONE-SHOT-PROMPT s.20, s.21; COPY-2 s.17, s.18, s.27; DEFINITIONS G8; CLOUD-FIGURES-2026-11-21 B2; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.3.7. Conflicts settled: C-088.

### 4.3.8 Where a beaten Tom wakes

- How it works: Beaten, Tom comes round on the pavement, in Grace Rinaldi's kitchen or in the hospital, sometimes robbed, with a street that knows he lost, in control within 60 real seconds with the cost said. Hospital costs days, never money, and plants a witness; the retired doctor costs money (stitches £20). Bruises and a cut lip last three game days, a limp one. The ambulance for a hit person comes in about ten game minutes and takes them to hospital.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work Test: the gate
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: COPY-2 s.5, s.9, s.11, s.41; DESIGN s.7; DEFINITIONS G8, P04; RULINGS 'The look and the street' (21 Sep, 1 Oct, 3 Oct); CLAUDE.md gate
- Status: outside. Coverage row: 4.3.8.

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

## 4.4 Props and street furniture

Lamps, the phone box, bins, railings, bollards, signs.


### 4.4 Props and street furniture

- How it works: Quay Street's furniture: four concrete lamp columns (lamp_post_C, 220 mm square at the foot tapering to 125 mm, lantern top at 5.0 m, unpainted concrete), staining still to finish; boat-shaped aluminium lanterns with 35 W low-pressure sodium lamps, each a straight-down pool (cone 22 to 46 degrees, 167 lm) plus a 40 lm bulb glow reaching 1 m, 4.83 m up, giving pools with darkness between. The KX100 phone box stays; no skip or pallets until real. Street name plates in Marcellus SC. Sources in order: free CC0 or unmarked CC-BY first, else our own from photographs. At least 5 props per 10 m of street.
- Standard: Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work; 3 Oct sources (free first, else our own from photographs) Test: small-piece review (RULINGS 3 Nov)
- Source: RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate; ruling 3 Oct (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: TARGET-STREET-FURNITURE-2026-11-17 S1 to S4; FURNITURE-SPECS-2026-11-17; RULINGS 22 Oct, 2 Oct, 3 Oct, 1 Oct; Study 4
- Status: outside. Coverage row: 4.4. Conflicts settled: C-089.

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
- Status: measured. Coverage row: 4.5.1. Conflicts settled: C-090.

### 4.5.2 Parked cars

- How it works: Our own scripted Blender hatchback goes first as the one parked car; the other three follow only after he has seen it. Kerb places are held in production/specs/street-vehicles.json; budget 40,000 triangles, 4 LODs, 2,048 px, simple collision, at most six cars in view at 0.5 ms. P9 gate: a blind reviewer on the untextured body names no model with confidence and places it in Britain or Europe, 1985 to 1991. Traffic from their kit follows in the friends' build after one passes. Nothing is bought for street or cars.
- Standard: His look at one parked car before twenty (ruling 17 Nov) Test: the gate
- Source: RULINGS cars 17 Nov (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: PLAN-PARKED-CARS-2026-11-17; RULINGS 17 Nov, 6 Nov, 16 Sep; canon 'Brands and law'
- Status: outside. Coverage row: 4.5.2.

## 4.6 Vehicles

The firm's cabs, period cars, police cars and vans, all fictional.


### 4.6.1 Car designs

- How it works: Every vehicle is fictional: no real car models or makes. Method: invented makers with an ethos, blend a class, never copy a car; each design passes the P9 blind silhouette check. The firm's cars are two tired cabs at the start and five at rung 3, with the roof sign and plate making a cab the firm's; a used car at the lot costs £600 to £1,200. The traffic hatch has a second variant and 8 colours.
- Standard: Fictional makes only; no real car models (canon) Test: the gate; a look-alike check against real makes
- Source: canon Brands and law (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: canon 'Brands and law'; PLAN-PARKED-CARS s.2; TRAFFIC-STAGE1 rule 3; DEFINITIONS RT-04, G8
- Status: outside. Coverage row: 4.6.1.

### 4.6.2 Working vehicles

- How it works: Named only; not designed beyond: boats and buses are scenery (ruling 23 Sep). The sources mention vans and lorries only as things in events (goods off a van or lorry are a lift; a van broken down across the lane; a crate off a lorry at the dock gate; lorry-delivered fish), a police car no faster than Tom's car on a straight (stops a driver at 50 mph or more), and an ambulance that arrives about ten game minutes after help is called. No dock truck has a design.
- Standard: Boats and buses scenery (ruling 23 Sep) Test: the gate
- Source: RULINGS 23 Sep (Unreal-only; judged in Unreal against the Hook sheet and KCD2 frames). Designed in: RULINGS 23 Sep; COPY-2 s.3, s.11, s.14; DEFINITIONS G2, G6
- Status: outside. Coverage row: 4.6.2.

## 4.7 Day and night

The clock's light: day and night now, four or five states later, no moving sun.


### 4.7 Day and night

- How it works: Day and night now, four or five light states later, no moving sun (7 Oct). Night is pools of lamp light with darkness between and lit windows, never one orange wash (1 Oct); dusk comes with the lamps switching on (about 70 lux, the sodium taking 8 to 15 minutes to turn full yellow). Day exposure stays one stop darker (29 Oct). Sound carries about twice as far in the small hours. Tom and the ground 5 m round him stay readable at night; the frame's corners darken with the same light value the watchers use. Under the ruled clock a game day is 24 real minutes and the dark part about 14 of them.
- Standard: Ruling 7 Oct; night as pools of lamp light with dark between (1 Oct) Test: the gate at night
- Source: RULINGS weather and night (his ruling or canon). Designed in: DESIGN s.6 (ER-NIGHT-01, 02); LIGHT-WEATHER-VALUES-2026-11-17; RULINGS 1 Oct, 7 Oct, 29 Oct; DEFINITIONS CLK-05
- Status: measured. Coverage row: 4.7. Conflicts settled: C-091, C-092.

## 4.8 Weather

Dry overcast, drizzle, rain; one wetness value drives look, sight, sound and who is out.


### 4.8 Weather

- How it works: Weather comes as weighted profiles: dry overcast, drizzle, rain; never sunshine in the friends' build. One wetness value drives the look (wet street dark and glistening, mirroring sky and buildings, puddles that are water), what is seen and heard, and who is out: rain cuts sight and sound, halves the voices, empties the street (each crowd band halved), lowers car grip and makes the road slippery. The same seed played dry, in drizzle and in rain gives three different streets, the same each time. A wet road takes about 3 to 14 hours to dry and puddles days; rain on about 12 days a month is the working assumption.
- Standard: Grey range only, never sunshine in the friends' build (5 Oct); one wetness value (DESIGN §6) Test: S: same seed in three weathers
- Source: RULINGS 5 Oct; DESIGN §6 (his ruling or canon). Designed in: DESIGN s.6 (ER-NIGHT-03); LIGHT-WEATHER-VALUES-2026-11-17; COPY-2 s.5, s.10; DEFINITIONS G9; RULINGS 5 Oct
- Status: measured. Coverage row: 4.8.

## 4.9 1990 detail

Signage, poll-tax posters, the brand bible's owed brands, CCTV at the bank, phone boxes.


### 4.9 1990 detail

- How it works: Late-analog 1990: landlines, phone boxes, answering machines, pagers, cash and paper; no mobiles, no internet. CCTV only at the bank, one camcorder in town as a rare witness. Poll-tax posters are an invented local campaign, never real parties or people. Money is pounds and pence only, written plain; typed letters in Courier Prime, street plates in Marcellus SC. The brand bible still owes six names: the football club, the local paper, the pirate radio station, the regional TV channel, the telephone operator (kiosk mark) and the postal cypher. The interface style sheet is a draft, nothing ruled.
- Standard: canon era; late-analog; brand bible owes the football club, paper, pirate radio, TV channel, phone operator, postal cypher Test: canon-gate and content-gate; his eye
- Source: canon Era, Brands and law (his ruling or canon). Designed in: canon 'Era' and 'Brands and law'; STYLE-SHEET-1990-DRAFT-2026-11-18; RULINGS 3 Oct; COPY-2 s.2, s.5
- Status: measured. Coverage row: 4.9. Conflicts settled: C-093.

## 4.10 Pubs without drink and the closed school

Places that exist with no drink and no children.


### 4.10 Pubs without drink and the closed school

- How it works: Pubs may stand as buildings on the street, boarded or serving food, never entered for drink; Mickey's is a minicab office (D19, superseding D15's pub). Alcohol and gambling are out entirely, in image and speech, and nobody can bet on anything, including at the boxing club. The school stands closed for the game's window: the building is there and nobody is in it; no children are rendered, in the crowd or in dialogue. Enforced at six sites including the animation library by clip name. Tuesday's chapel hall evening (tea and talk) is the model for a place that exists without drink.
- Standard: canon content rule: pubs as places, boarded or serving food; the school stands closed Test: content gate over clips and props
- Source: canon D18 (his ruling or canon). Designed in: canon content rule (D18) and Mickey's (D19); COPY-2 s.3, s.29; DEFINITIONS G10
- Status: measured. Coverage row: 4.10. Conflicts settled: C-094.

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
