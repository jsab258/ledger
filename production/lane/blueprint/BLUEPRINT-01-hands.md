# BLUEPRINT 01: What the player does with his hands

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. The verbs: moving, driving, fighting, being seen, chases, jobs, the crew.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 1.1 Moving on foot

Walking the town with the camera: the verb under every other verb.


### 1.1.1 Walk, run and turn

- How it works: Frank walks, runs and turns with weight, like a man in boots on wet cobbles: turning is quick, starting and stopping have a short ease, and running is plainly louder and more noticed than walking. Z held (or a light stick touch) walks slowly and halves the reach of his footsteps. Crouch is in (his ruling of 24 Nov, Q19): C, toggle or hold in settings, 1.2 m/s against 1.6 walking; what it does to what is caught is set in 1.1.5 and 1.4.3 (CS-12). Every action answers within 100 ms, a press up to 0.1 s early counts, keyboard movement is eased and mouse look never jumps. Tuning speeds are walk 1.6 m/s, slow walk 0.9, run 5.5, holdall run 5.3.
- Standard: ER-INPUT-01 (every action answers within 100 ms, eased keys, mouse look never jumps); crouch 1.2 m/s with hold or toggle (accessibility); feel numbers (start, stop, turn rate, run speed) to be measured from reference games. Test: feel numbers inside measured bands (input probe); H: 'did moving feel heavy or slippery?'; his eye in Unreal
- Source: DESIGN §17 ER-INPUT-01; advisor 256 (waits on a dated study); crouch from his ruling of 24 Nov (Q19) with its speed and input DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-02, CS-12)
- Status: pending. Coverage row: 1.1.1. Conflicts settled: C-270, C-355.
- Reference solid (Sleeping Dogs; STATUS.md on wip, 24 Nov 00:50, five-sample rule): sprint 5.5 m/s and jog 4.5 m/s (4.1 to 4.9). The design's run (5.5) equals the sprint; the built prototype runs at 4.2 m/s, about the jog; which Frank's run follows is open (C-267). One game only and it has no walk key, so walk, slow walk, start, stop and turn stay pending (second game about 2 h, DECIDES-CHECK 24 Nov).
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov); the combat pass's numbers (wind costs, weapon forces, edge table) are for the next data wave. Data sweep class C.
- Crouch in, answered 24 Nov (Q19): his ruling of 24 Nov (RULINGS on wip, his decisions page). Replaces 'there is no crouch'. The feel numbers still wait on the study, so the status stays pending.
- Reference solid (GTA V; STATUS.md on wip, 25 Nov 01:12, five uncut stretches at 0.1 s): Franklin's walk about 2.0 steps a second (1.9 to 2.0). A cadence only: no step length was read, so Frank's walk speed stays pending (C-508).

### 1.1.2 On-foot camera follow

- How it works: The street camera sits at the Between picture's height with an 86 degree lens, 3.1 m back, so his feet are always in frame and his head is level with the far end of the street. It blends in a second or less: closer in rooms and talk (Frank 1.5 m from the speaker), wider in a fight (both men's feet in at least 90% of frames, about 3.5 to 5.0 m back). It never ends inside a wall, body, car, lamp post, shelter or van; it comes in front of thin things. Shake obeys Reduce motion, and the field of view is a setting of 75 to 100 with 86 the default. A camera re-centre is in (his ruling of 24 Nov); its input and its time are not yet written.
- Standard: Between height, 86 degree lens, 3.1 m back, feet in frame; never inside a wall, body or car (ER-CAM-01, ER-CAM-02); follow lag and turn feel to be measured Test: B soak with clip detector; S frames counted for feet in frame; H screenshots in tight rooms
- Source: ruling 28 Oct (camera); DESIGN §17 (waits on a dated study). Designed in: DESCRIPTION-COPY-2 §6; DESIGN §17 ER-CAM-01/02; RULINGS 28 Oct (camera) and 21 Nov (setting); FEEL-TARGETS-MELEE C10; DEFINITIONS AX-03 and pass 3 header
- Status: pending. Coverage row: 1.1.2. Conflicts settled: C-001.
- Camera re-centre in, 24 Nov: his ruling of 24 Nov (RULINGS on wip, his decisions page).
- Prior research: PRIOR-RESEARCH-INDEX section 3 group 1: camera measured in his packaged build (production/specs/camera.json: feet fully in frame from 3.0 m); that file's talk (1.2 m, 63 degrees), run and room rows were copied from Mafia's files and are provisional.
- Checklist (23 Nov, top twenty no. 10; A05.09, A05.11): missing: a rule for the camera when it is close in rooms (fade or hide Frank, or hold back) and for a usable view going up and down stairs, with a tight-room and stairs check. Gap for the design proof; status unchanged.
- Checklist (23 Nov, top twenty no. 20; A05.13): missing: the camera must never override the player's mouse or stick input, with a test. Gap for the design proof; status unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 1.1.3 Doors, stairs and thresholds

- How it works: A door opens with the use key and Frank walks through without catching; stairs are walked, not snagged on; a locked door says it is locked. Nothing inside Mickey's holds him against a wall. Doors creak, hit and latch, and a forced door is the loudest thing in a quiet street. From any state he can move on within 5 s by walking, getting out or backing out, or a short in-world reset puts him on clear ground; there is no jump.
- Standard: Never stuck (ER-CORE-01: moves on within 5 s); in or out of a door in under 2 s; no jump (ruling 23 Sep) Test: B: 30 minutes of walking into every door and stair; S: door use timed
- Source: DESIGN §1 ER-CORE-01; ruling 23 Sep (his ruling or canon). Designed in: DESCRIPTION-COPY-2 §6; DESIGN §1 ER-CORE-01; RULINGS 23 Sep genre line (no jump) Reality check (CHECK A20): the 68 cm and 11 cm a side figures come from our own scene; the real figure would come from 1990 door and room dimensions (British Standards, period plans), the camera need kept as a stated exception.
- Status: ruled (his ruling or canon). Coverage row: 1.1.3.
- Prior research: research/interior-blockout and research/office-camera (research-3 and research-4 sheets): Frank is 68 cm wide, so a real front door leaves about 11 cm a side; walks were straight lines with a 30 cm capsule, no nav mesh and no doors, so every target through a wall failed; third-person rooms run 1.5 to 2 times real size.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G14.

### 1.1.4 Carrying

- How it works: A holdall in the hand slows him a little and can be seen; a thing under the coat cannot be seen but is found in a search. What he carries raises what a witness catches ('a man with a holdall on the quay at midnight is a man with a holdall'). Running with a holdall is 5.3 m/s against 5.5 empty, still just faster than a constable. Loads named by the row are the suitcase, holdall, envelope and a box.
- Standard: Found is worse than used (load as a tension source); running blocked while carrying in the prototype; how much a load slows to be measured Test: S: a carried load raises what a witness catches; H: 'could you tell what Frank was carrying?'
- Source: DESIGN §3 source 3; prototype round 6 (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §6; DESIGN §3, §15; DEFINITIONS pass 3 §G4; MEASUREMENTS-NEEDED A1
- Status: unmeasured. Coverage row: 1.1.4. Conflicts settled: C-002.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13.

### 1.1.5 Hiding and keeping out of sight

- How it works: Hiding is what a man in a street can really do, with the move keys and crouch (his ruling of 24 Nov, Q19). A still figure in a doorway counts at the doorway's light (0.12) and is caught at most as a shape, and only beyond 8 m; moving through the same doorway counts at the street's light (0.25 unlit). Crouch halves footstep reach and makes his shape half as easy to pick out beyond 4 m in the dark, at the cost of speed (1.2 against 1.6 m/s); it does nothing in light within 4 m, and crouching where nobody crouches is itself odd to anyone who sees it. With his back to a watcher his face cannot be caught, though the coat can. Among three or more people within 2 m a glance takes 0.7 s instead of 0.35 s; behind a van, stall or corner nothing is caught; nothing on screen says 'hidden'.
- Standard: Light scale (doorway 0.12, unlit street 0.25) and symmetry (ER-EYES-02); crouched in the dark beyond 4 m he is caught less than standing, and under a lamp within 4 m crouch changes nothing. Simulated: approach from 12 m behind an unaware man in a dark doorway, crouched, wet cobbles: 58% put out, 13% spotted; by day walking 15% out, 77% spotted (leads, judgement). Test: S: standing still in a doorway lowers what is caught versus walking past; H: 'where would you stand to not be seen?'; ER-HIDE-01 to 03
- Source: DESIGN §2 ER-EYES-02 (waits on a dated study); crouch ruling 24 Nov (Q19); the crouch effect DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-12), for him to overturn
- Status: pending. Coverage row: 1.1.5. Conflicts settled: C-270, C-355.

### 1.1.6 Tailing on foot

- How it works: A tail is the town's eyes in reverse: the target looks back about once every 20 to 40 s on foot and at every corner and stop. Being made uses the watcher ladder: a shape is nothing, a mark is a doubt (he speeds up or changes route, always shown first), a face he knows ends the tail and he turns and says so, or runs. There is no hidden distance fail, and losing sight is not failing: the target keeps his routine and Frank picks him up at the next place on it. It ends in a Ledger line within a game minute naming what was learned.
- Standard: none yet: distance bands and the 'made' rule to be measured Test: S: a scripted tail is made at the addendum's rule and never fails on a hidden distance; H: 'did losing him feel fair?'; addendum rules ER-TAIL-01 to 03
- Source: DESIGN §4 (tails family, no numbers) (no reference figure yet). Designed in: DESIGN-ADDENDUM A2 (ER-TAIL-01 to 03); DESIGN §4 Tails; DESCRIPTION-COPY-2 §13
- Status: unmeasured. Coverage row: 1.1.6.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12, G16.

### 1.1.7 Stopping and blending in

- How it works: Sit on a bench, wall or step, lean in a doorway, light a cigarette (key B). A stopped man who belongs (sitting, smoking, waiting at the bus stop) is caught as a shape like anyone and draws no second look; a man standing about at night without a reason draws one. A seated or smoking Frank is never caught more than a walking one at the same spot. Waiting stays under 10% of play (aim about 3%).
- Standard: A stopped Frank draws less notice than a loiterer; tobacco allowed (canon); waiting under 10% of play (ER-CORE-06) Test: S: a seated or smoking Frank is caught less than one standing about; H: minding feels like play; addendum rules ER-STOP-01
- Source: canon content rule; DESIGN §1 (no reference figure yet). Designed in: DESIGN-ADDENDUM A10 (ER-STOP-01); DESCRIPTION-COPY-2 §8 and §34; DESIGN §1 ER-CORE-06
- Status: unmeasured. Coverage row: 1.1.7.
- Being followed, stared at or crowded is noticed (catalogue 23 Nov, rank 4; seen in 3 games): A neighbour notices Frank loitering and says so. Partly: a stopped man who does not belong draws notice; short is the spoken warning, then a complaint or a report. Feature only; no timing; the part's status is unchanged.
- A rest idle on world objects (catalogue 23 Nov, next tier): Frank leans on the harbour rail, smokes, watches. Partly: sitting and smoking are covered; leaning on the rail is not. Feature only; no timing; the part's status is unchanged.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G01.

### 1.1.8 Vaulting low walls and fences

- How it works: At set places only (low walls, yard fences and bins under about 1.2 m, marked in the map data), running at one carries Frank over in about 0.8 s. Nowhere else: no jump key and no free climbing; set climbing places are in (his ruling of 24 Nov, Q19), their places, heights and times not yet written. A constable vaults the same places in 1.2 s, so a yard and back fence is a real way to gain ground. The road plan has six vault places: one on the yards' lane, three on the terraces' ginnel, one on each warehouse cut.
- Standard: His word of 20 Nov 07:54 (advisor 263, DECISIONS A26) confirmed it as recommended; never a jump (ruling 23 Sep); vault speed and heights to be measured Test: S: each vault point works in a chase; no vault anywhere else; addendum rules ER-VAULT-01
- Source: ruling 23 Sep; Q1, answered by his words of 20 Nov 07:39 (advisor 263; DESIGN-ADDENDUM A26) (his answer; speed and heights wait on a dated study). Designed in: DESIGN-ADDENDUM A26; DESCRIPTION-COPY-2 §6; DEFINITIONS pass 3 §G1, §G4
- Status: pending (in scope by his answer of 20 Nov; speed and heights wait on the measuring). Coverage row: 1.1.8. Conflicts settled: C-003, C-271.
- Set climbing places in, answered 24 Nov (Q19): his ruling of 24 Nov (RULINGS on wip, his decisions page). Replaces 'no climbing'.
- Measuring note (SLEEPING-DOGS-DRILL, 23 Nov): in Sleeping Dogs the run key also vaults; no number for LEDGER's vault times yet.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G14, G12.

### FIT-G4 Frank's, the constables' and the runner's speeds

- How it works: Frank walks at 1.6 m/s, walks slowly at 0.9, runs at 5.5, and with a holdall runs at 5.3, still just faster than a constable. A constable walks his beat at 1.1 m/s and runs at 5.2; he vaults the set places in 1.2 s (Frank 0.8). A runner fleeing Frank runs at Frank's run less about 5%. So Frank outruns a constable on a straight by 0.3 m/s and gains on the vaults; from 10 m behind a runner he closes in about 33 s, and a gap over about 25 m is closed only by a better line. Speeds never depend on the frame rate.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS design pass 3 §G4; FIT-CHECK F21
- Status: pending. Coverage row: FIT-G4.
- Reference solid (Sleeping Dogs; STATUS.md on wip, 24 Nov 00:50): sprint 5.5 m/s, equal to the design's run; jog 4.5 m/s, about the built prototype's run of 4.2 (C-267). The walk, the constable's speeds and the runner's 5% stay pending; one game only, a second wanted (DECIDES-CHECK, 24 Nov). GTA V walk cadence is now solid at about 2.0 steps a second (STATUS.md on wip, 25 Nov 01:12; five stretches by one method, leg crops every 0.1 s, in ON-FOOT-FOOTAGE-QUESTIONS-2026-11-24.md): a cadence only, no step length was found, so no walk speed follows from it; Frank's 1.6 m/s walk stays pending (C-508). Status unchanged.

## 1.2 Driving

The cab and other cars: at AAA quality as the end state, never a driving game.


### 1.2.1 Car handling

- How it works: Fun first, as non-sim open-world games do it; 1990 shows in sound, sway, look and relative speed; automatic gearbox. Game set: 0 to 30 mph in 3.0 to 4.5 s, 0 to 60 in 10 to 14 s; dry braking from 30, 50, 70 mph in 8 to 11, 22 to 30, 44 to 58 m; wet is 1.3 to 1.6 times dry; handbrake turn 120 to 180 degrees settling in 1.0 to 1.6 s. On keys steering eases to lock in 0.2 to 0.35 s and centres in 0.4 to 0.9 s, a lane change at 60 mph swings the tail under 15 degrees and settles within 1 s; the pad is analogue and a set course takes the same time within 10% on keys or pad. Rain lowers grip through the one wetness value.
- Standard: Game set M1 to M9 (e.g. 0 to 30 mph 3.0 to 4.5 s; dry braking 30 mph 8 to 11 m; steering yaw 63% in 0.15 to 0.25 s); ER-DRIVE-02 on keys Test: S: drives D1 to D8 by keys and pad inside the bands; his feel check
- Source: FEEL-TARGETS-DRIVING (c2); DESIGN §5; to be replaced by the measured sheet (DRIVING-MEASUREMENT-METHOD) (waits on a dated study). Designed in: FEEL-TARGETS-DRIVING (c2) M1 to M9; DESIGN §5 ER-DRIVE-02; DESCRIPTION-COPY-2 §10; DEFINITIONS pass 3 §G2
- Status: pending. Coverage row: 1.2.1. Conflicts settled: C-004, C-005.
- Prior research: his rulings of 17 and 18 Nov (fun first, automatic gearbox, real figures a floor, game-band targets, cars hurt and never kill) replace the old 'no drivable vehicle, ever' (game-design/agency-model.md, streets-and-cars-spec.md); PRIOR-RESEARCH-INDEX section 1 item 4.
- DECIDES-CHECK, 24 Nov: driving drops to a lead: the Hook's roads are fixed, so the car is tuned to the map; the open map question (R1) turns on chase speed and lap time from the car-chase clips, not on acceleration or braking. Sleeping Dogs drill plus a second game, about 3 h, as a lead.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 1.2.2 Car camera

- How it works: The chase camera sits about 5.8 m back (band 5 to 6.5 m) and 1.6 to 2.0 m high, with lag of 0.1 to 0.25 s. The field of view is 60 to 65 degrees at rest, 64 to 70 at 30 mph, 70 to 78 at 60, which is how a slow car reads as quick. B held turns it to the rear window for the car in the mirror. It never enters a wall, a car or a post.
- Standard: M10: 5 to 6.5 m back, 1.6 to 2.0 m high, lag 0.1 to 0.25 s, field of view 60 to 65 deg at rest widening to 70 to 78 at 60 mph (the Hook's top speed, G2); ER-DRIVE-06 Test: S: D8 camera run; B: 40-minute soak with no clipped frame
- Source: FEEL-TARGETS-DRIVING (c2) M10; DESIGN §5, §17 (waits on a dated study). Designed in: FEEL-TARGETS-DRIVING (c2) M10; DESIGN §5, §17 ER-DRIVE-06; DESCRIPTION-COPY-2 §10
- Status: pending. Coverage row: 1.2.2.
- DECIDES-CHECK, 24 Nov: the GTA VI car camera (M10) is a one-game lead; second game a Sleeping Dogs drill, about 0.3 h.

### 1.2.3 Getting in and out

- How it works: A car Frank may open (the firm's cars, his own, an unlocked one) takes 1.5 to 2.5 s from door to seated, from either side, and he is moving within 1 s after; getting out takes under 2 s. A blocked door never traps him. Forcing a locked parked car takes about 6 s; a car with somebody in it can be taken by pulling the driver out (1.2.10; his ruling of 25 Nov, advisor 378): loud, reported, heavy consequences. Crew and fares ride in the cab and a man at his side rides along; getting out after a wreck is immediate and Frank walks.
- Standard: a car Frank may open: door to seated 1.5 to 2.5 s, moving within 1 s after; out under 2 s; forced entry of a locked car about 6 s; a blocked door never traps (ER-DRIVE-07) Test: S: enter and exit timed from both sides, door blocked
- Source: STATUS.md and gtavi-driving-builder-2026-11-21 (SOLID); description section 23 (reference game). Designed in: DEFINITIONS design pass 4 'Getting in and out (1.2.3)'; GTAVI-MAP Run 5 additions; DESCRIPTION-COPY-2 s.10, s.23; DESIGN s.5 ER-DRIVE-07; PARTS-TREE notes on 1.2.3
- Status: measured (the times: solid in STATUS.md, five uncut, dated samples; the carjack sentence is ruled, 25 Nov). Coverage row: 1.2.3. Conflicts settled: C-006, C-007, C-501.

### 1.2.4 Crashes, damage and unsticking

- How it works: Damage comes in stages by closing speed: under 10 mph is forgiven, then dented, then crumpled, and from about 35 mph in one hit the car will not drive on. It says so at once, Frank gets out and walks, the firm fetches it and it is off the road a day; a dent stays until the firm mends it at the yard overnight. A car wedged on a pole or wall always backs out, and after any crash it moves or can be left within 5 s. Raised by Y1.1: front damage over the threshold pulls the car to one side until repaired, a broken lamp darkens the road ahead at night, and a dent is a mark witnesses remember. A car can ram another; both take damage and nobody inside dies.
- Standard: M11: fragile like The Getaway (under 5 mph nothing; over 30 to 35 mph may not drive on); ER-DRIVE-01 (moves or can be left within 5 s); ER-DRIVE-08. Raised by Y1.1: front damage over the crash threshold pulls the car to one side until repaired, and a broken lamp darkens the road ahead at night; a dent is a mark witnesses remember. Test: S: pole and wall hits at 10, 20, 35, 50 mph; B: 30 minutes of crashing
- Source: FEEL-TARGETS-DRIVING M11; DESIGN §5 (waits on a dated study). Designed in: DESIGN §5 ER-DRIVE-01, -08; DESCRIPTION-COPY-2 §10; FEEL-TARGETS-DRIVING M11; GTAVI-MAP Y1.1; DEFINITIONS pass 3 §F05
- Status: pending. Coverage row: 1.2.4. Conflicts settled: C-008, C-009.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G19.

### 1.2.5 Cars and people

- How it works: People look before they step out, so nobody steps out within the stopping distance of a car at 30 mph (23 m); at town speeds a hit is the player's doing, and only his car can strike anybody. A hit knocks a person down and hurts them badly but never kills, whatever they land on. Fall by speed: under 10 mph a stagger, 10 to 25 mph knocked down and sitting up within 5 s, over 25 mph thrown down and still up to 20 s, then moving. The choice (stop and help, or drive off) comes within 2 s; an ambulance takes about ten game minutes; drive off and it is a hit-and-run chase and 'a Mickey's cab knocked her down and never stopped' goes round.
- Standard: Canon (his pick 18 Nov 22:07): hurts, never kills; only the player's car strikes; the choice put within 2 s (ER-DRIVE-03, ER-DRIVE-04, ER-DRIVE-05, ER-DRIVE-10) Test: S: 1,000 seeded crossings with no contact; hits at 5, 15, 30, 50 mph, nobody dies; both choices seeded
- Source: canon content rule; DESIGN §5 (his ruling or canon). Designed in: Canon content rule (his pick 18 Nov 22:07); DESIGN §5 ER-DRIVE-03 to -05, -10; DESCRIPTION-COPY-2 §11; DEFINITIONS pass 3 §P04, §G2
- Status: ruled (his ruling or canon). Coverage row: 1.2.5.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G19.

### 1.2.6 Tailing and being tailed by car

- How it works: Following a car works like a foot tail with the car as the mark: a cab behind him twice is a doubt, and the roof sign makes it worse; the doubt always shows first. Being tailed is a fare's wrinkle, a car in the mirror, and B held shows the rear window. The patrol car is no faster than Frank's car on a straight.
- Standard: none yet: following distance and the 'made' rule to be measured Test: S: scripted car tail; H: 'did you know how close was too close?'; addendum rules ER-TAIL-01 to 03
- Source: DESIGN §5 wrinkle 'the tail' (no numbers) (no reference figure yet). Designed in: DESIGN-ADDENDUM A2; DESIGN §5 wrinkles; DEFINITIONS pass 3 §G2
- Status: unmeasured. Coverage row: 1.2.6.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12.

### 1.2.7 Driving with passengers

- How it works: Passengers talk while the car moves; a fare says 'left here' a junction before Pauline does; a sit-down can happen in the back of his own cab. No fare runs longer than 2 real minutes without a decision, a person or a sighting, and driving stays under about a quarter of play. Talk staged while driving runs the clock and the car keeps moving; typing never moves Frank. In a chase, a passenger who knows the town gives at least one landmark line per 20 s.
- Standard: No fare longer than 2 real minutes without a decision, a person or a sighting (ER-CORE-08); typing never moves Frank (ER-TALK-05) Test: H: fare log; S: a staged back-seat talk with the car moving
- Source: DESIGN §1, §11 (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §10, §34; DESIGN §1 ER-CORE-08, §11 ER-TALK-05; DEFINITIONS RT2-20; GTAVI-MAP GV-03
- Status: unmeasured. Coverage row: 1.2.7.
- Studies: aaa-studies/MISSIONS-AND-SIDE-QUESTS.md: MS-03 no dead leg over 2 minutes; a job 5 to 30 minutes, planned ones to 45; decided. None measured.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G20.

### 1.2.8 Riding as a passenger

- How it works: Kevin, Terry or a crewman can drive Frank: he says where, by landmark, and can skip the ride, which passes exactly its drive time on the clock. He can talk with the driver on the way. A crewman told to drive is an AI driver and always brakes for people. Free fast travel is out (his ruling of 24 Nov); this skip by his own driver is the one allowed.
- Standard: A crewman told to drive is an AI driver and always brakes for people (DESIGN §12); a skipped ride costs its real time on the clock Test: S: a ride arrives; skip advances the clock by the drive's time; addendum rules ER-RIDE-01
- Source: DESIGN §12; canon; his ruling of 24 Nov (RULINGS on wip, his decisions page) for free fast travel out (his ruling or canon). Designed in: DESIGN-ADDENDUM A24 (ER-RIDE-01); DESCRIPTION-COPY-2 §10; DESIGN §12
- Status: ruled (his ruling or canon). Coverage row: 1.2.8. Conflicts settled: C-010.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G04.

### 1.2.9 Repairs, plates and paint

- How it works: A wrecked cab is off the road a day and a dent is mended at the yard overnight. A witness notes the plate as a mark. Shaun Hewson's paint takes the roof sign off and gives a new colour, after which earlier sightings no longer name that car; new plates or a respray also clear a noted plate, but only for witnesses who have not yet told anyone. There is no fuel or wear.
- Standard: A dead car is off the road a day (DESIGN §5); no fuel or wear (DESIGN §18). Raised by GTA VI's respray rule: new plates or a respray clear the police's noted plate for that car (see GV-02). Test: S: a repainted car is not named as the firm's by a witness who saw the old paint; addendum rules ER-PAINT-01
- Source: DESIGN §5, §12, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A24; DESIGN §5, §12, §18; GTAVI-MAP GV-02
- Status: decided. Coverage row: 1.2.9. Conflicts settled: C-011.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-01 no hunger, tiredness or hygiene value drains on a clock; decided; IM-06 cars and men show harm; no repeated care action required; decided. None measured.
- People react to appearance (catalogue 23 Nov, rank 5; seen in 3 games): Passers-by remark on a clean or a battered cab. Not yet: a remark on the cab's state, for the design proof to place. Feature only; no timing; the part's status is unchanged.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G11, G13.

### 1.2.10 Taking a parked car

- How it works: A parked car is taken only by force, with no minigame. A car with a driver in it can also be taken by pulling him out (his ruling of 25 Nov, advisor 378): loud, reported, with heavy consequences from the witness, memory and police systems and no cap. It is loud (heard at the force reach), the owner reports it when he finds it gone, the car is then known to the police, and a taken car has no roof sign so witnesses do not name it as the firm's. Taking one by force takes about 6 s (the description, section 23, kept by design pass 4). GTA VI's two ways in (a brick through the quarter-light or a tool at the door) are a lead to check in the footage pass, without their times; a car with a steering lock cannot be taken.
- Standard: His word of 20 Nov 07:54 (advisor 263, DECISIONS A27) confirmed it as recommended; no lockpicking game (DESIGN §18). Pulling a driver out: heard at the force reach, always reported, the car known to the police; the time it takes and whether a moving car can be stopped for it are not set (none yet). Forced entry about 6 s (design pass 4, 1.2.3); a car with a steering lock cannot be taken. Test: S: a taken car is reported and named; force heard at its reach; addendum rules ER-TAKE-01
- Source: Q2, answered by his words of 20 Nov 07:39 (advisor 263; DESIGN-ADDENDUM A27) (his answer); advisor 378, 25 Nov (RULINGS on wip). Designed in: DESIGN-ADDENDUM A27; ONE-SHOT-PROMPT 'Taking a parked car'; GTAVI-MAP Y1.2
- Status: ruled (parked car: his answer of 20 Nov 07:39, advisor 263; pulling a driver out: his ruling of 25 Nov, advisor 378, which replaces 'never one with somebody in it'). Coverage row: 1.2.10. Conflicts settled: C-012, C-501.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13, G15, G20.

### 1.2.11 The horn

- How it works: One key (H) sounds the horn while held. It is a noise at about 60 m by day, further at night and less in rain, and turns watchers' heads like any noise. A short toot outside a door brings out a fare or a man Frank is waiting for within 10 s if he is within 15 m; a long blast in a quiet street at night draws a look from lit windows; pedestrians in the road step aside; it never alarms police alone.
- Standard: rule: A horn sounded at night is heard by every listener inside its reach and by nobody outside it, and a waiting fare inside 15 m comes out within 10 s (golden rows). Test: A horn sounded at night is heard by every listener inside its reach and by nobody outside it, and a waiting fare inside 15 m comes out within 10 s (golden rows).
- Source: DESIGN-ADDENDUM-2026-11-20 A32 (from REFERENCE-MECHANICS-2026-11-20 M1.75) (reference game). Designed in: DESIGN-ADDENDUM A32; DESCRIPTION-COPY-2 §10
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 1.2.11.

### GV-01 The boot, seen

- How it works: The cab's boot holds what is not on him: the envelope, a spare coat, a box. Opening it is an act with the seven slots, seen like any act. A constable who stops the cab with cause may look in it, and what is in the boot survives save and load. A body goes into the boot in 4 s.
- Standard: Opening the boot is perceived like any act; a stop with cause searches it; what is in it survives save and load. Test: B: boot opened in sight of a watcher x 20 (memory written); a stop with cause finds the boot's contents.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP §GV-01; DEFINITIONS RT2-11
- Status: decided. Coverage row: GV-01.
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13, G17.

### GV-03 The passenger who knows the way

- How it works: Whoever rides with Frank (Ron, a crewman, a fare who knows the town) says the way by landmark in a chase and when asked on a fare: 'left after the chapel, he cannot follow you through the yard'. No marker. At least one landmark line per 20 s of chase, each naming a real landmark on the way.
- Standard: In a car chase with a passenger, at least one landmark line per 20 s of chase; every line names a real landmark on the way. Test: B: car chases with each passenger; lines logged and checked against the map.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP §GV-03; DESCRIPTION-COPY-2 §10
- Status: decided. Coverage row: GV-03.
- Data (run 5): exact values in production/lane/blueprint/data/lines/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Story needs (frame and paper, 24 Nov): Ron's naming of buildings as a driving state that stops for good after the night between (paper second run via the story on paper). Partly covered: the passenger says the way by landmark; the state that ends after the night is missing.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G20.

### FIT-G2 Car speeds and the stop band

- How it works: The Hook is a 30 mph town (the built-up limit of 1990). Traffic drives at 20 to 28 mph; every car in the Hook reaches 60 mph on the 420 m straights and no more there; a patrol car is no faster than Frank's car on a straight. The patrol stops a driver it sees at 50 mph or more, or doing a reckless act (a hit, the pavement, a red light at speed); 31 to 49 mph draws a look and a noted plate, never a stop. Nobody steps out within the 23 m stopping distance of a car at 30 mph.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 §G2; FIT-CHECK F33
- Status: decided. Coverage row: FIT-G2. Conflicts settled: C-013.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G19.

### FIT-F05 How often the one-hit wreck happens in ordinary driving

- How it works: Named only; not designed beyond: a measurement. Bot chases and an hour of ordinary fast driving on the prototype count hits of 35 mph or more; the pass is that ordinary driving under 30 mph wrecks the car less than once an hour (cloud, 1 h, with the next prototype build). It tests whether the one-hit wreck at about 35 mph (DESIGN §5) ends chases too often.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS design pass 3 §F05; FIT-CHECK F05
- Status: pending. Coverage row: FIT-F05.

### FIT-P04 The struck person's fall

- How it works: A person hit by Frank's car falls by speed: under 10 mph a stagger and a hand on the bonnet; 10 to 25 mph knocked down, rolls once and sits up within 5 s holding the hurt; over 25 mph thrown down, lies still up to 20 s, then moves and calls out. Never a body flung through the air, never limp as dead, nothing shown at length; the choice comes within 2 s. A person always moves within 20 s.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 §P04; DESCRIPTION-COPY-2 §11
- Status: decided. Coverage row: FIT-P04.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G19.

## 1.3 Fighting

Fists first, things to hand, carried weapons, guns rare and last; the whole street watches.


### 1.3.1 Blows and contact

- How it works: A blow starts within 0.1 s of the button. A jab lands in 0.25 to 0.40 s; the committed heavy blow in 0.63 to 0.85 s and cannot be cancelled, which is what makes it readable. Contact is sold by a hit-stop of 0.025 to 0.13 s by blow (jab 0.025 to 0.05, heavy 0.06 to 0.12, swing 0.07 to 0.13), a camera close-in held about 0.8 s inside the wider fight view, a small shake and four layers of sound. A struck man reels to the side he was hit. No combos, no feints, no five-zone rose (his ruling of 24 Nov); the cross and hook are the heavy blow's animations by angle, and in a grab the heavy comes out as a knee, elbow or headbutt. Aim is high or low by stick or mouse. Holding guard while striking pulls the blow to a third of its force for sparring. Every action costs wind (jab 0.12, heavy 0.20, kick 0.10, grab 0.08 of a full breath).
- Standard: ER-FIGHT-01 (timings inside the melee sheet bands, C1 to C13 and C15; C14, combination, is struck since combos are out): C1 blow starts within 0.1 s; C2 jab 0.25 to 0.40 s to contact, heavy 0.63 to 0.85 s; C3 hit-stop 0.025 to 0.13 s by blow; close-in about 0.8 s. Test: S: melee drills at 1/60 s (tools/lane/melee_drills.py), drill M2 struck; his feel check
- Source: FEEL-TARGETS-MELEE (c); DESIGN §7 (waits on a dated study); verb set and wind costs DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-02, CS-03), for him to overturn
- Status: pending. Coverage row: 1.3.1.
- Prior research: research/aaa-reference study 14 (read from files, a lead): KCD2 swing to contact about 0.75 s, hit reaction median 1.27 s. DECIDES-CHECK 24 Nov: fist timings are a lead (Sleeping Dogs and KCD2 drills, about 2 h).
- DECIDES-CHECK, 24 Nov: fist timings drop from deciding to a lead: they are band numbers the loops retune in minutes. Sleeping Dogs and KCD2 drills, about 2 h, as a lead. Status unchanged.
- Revision 1 (25 Nov, his pick A; CS-02): blows land on the attacker's line (high the head, low the body, a guarded blow on the forearms, a low kick or low thrust on the legs); the zone dice table removed. Rule: G19.

### 1.3.2 Reading and answering blows

- How it works: Every incoming blow can be read 0.45 to 0.80 s before it lands, in the other man's shoulders, feet and breath, never an icon; at most two men swing at once, 0.4 s apart, and the rest circle, block the way out, pick something up or try to grab him from behind. Guard (a held key) makes a blocked fist do little and a blocked heavy blow stagger Frank a little, though wind still drains. A guard plus a direction tap slips a blow (about 0.3 s). A blow thrown within 0.45 s of a block or slip is a counter: 0.6 of the wind-up and half again the force. A guard raised in the last 0.15 s costs no wind. Mashing empties Frank in a handful of blows (wind under 0.18, hands drop, he gasps); wind comes back at 0.12 a second, twice that with hands up. Getting it back takes 4 to 8 s by the earlier figure; the simulator's median is about 10 s, a tuning item for the loops. The slower-fights assist makes wind-ups 25% longer.
- Standard: Every incoming blow readable 0.45 to 0.80 s before it lands; at most two men swing at once, 0.4 s apart (ER-FIGHT-02); 'who was winning?' answered right 4 times in 5 from the body alone. Test: S: drills; H: 'did you see the blow coming?'; ER-DEFEND-01 to 02
- Source: DESIGN §7; melee sheet (waits on a dated study); wind and counter rules DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-02 to CS-04), for him to overturn
- Status: pending. Coverage row: 1.3.2.
- Checklist (23 Nov, top twenty no. 13; A18.05): missing: recovery times after a jab, heavy blow and swing, set and tested as readable. Gap for the design proof. DECIDES-CHECK 24 Nov: a lead, read with 1.3.1.
- DECIDES-CHECK, 24 Nov: a lead, read with 1.3.1 (fist timings are band numbers).

### 1.3.3 Targeting without lock-on

- How it works: No lock-on: the man the stick or mouse points at is the man hit, and Frank slides to about 1 m in the wind-up. With three men round him he hits the one he points at, and nobody is hit through a wall. Closing in takes 0.40 to 0.55 s from at most 2.0 m. A man needs about a metre of front to swing, so in a doorway or passage only one can reach Frank at a time, and walls shorten a long swing. The man the next blow goes to shows it only in Frank's shoulders and head turning, no marker.
- Standard: ER-FIGHT-06: the man pointed at is the man hit, nobody hit through a wall; slide to about 1 m (lead). Test: S: targeting script with three men round Frank; in a doorway only one man reaches him
- Source: DESIGN §7 (DECIDED by the design proof, for him to overturn); passage and doorway rule DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-03, CS-29)
- Status: decided. Coverage row: 1.3.3.

### 1.3.4 The lower rungs and the one fight model

- How it works: The ladder has eight rungs: stare, square up, threaten, shove or grab, strike, weapon out, weapon used, kill. It is the street's reading of how far a confrontation has gone, not a separate system: there is no combat mode, and every person in the Hook (Frank, his crew, a docker, a constable, two strangers quarrelling) uses the same actions, body, wind and temper rule (CS-01, 1.3.7, 1.3.8), so a fight Frank only watches runs the same way. Each rung is an act with the seven slots. Most confrontations end on rungs 1 to 4. Talk is the main weapon: before or during a fight Frank can threaten, demand, offer, bluff, name himself, call his men or yield, a 1 to 2 s act he can be hit during. A threat folds a man when his nerve plus pride is under the threat (a word 0.5, a weapon shown 0.8) times 0.8 plus 0.4 of Frank's menace. A bluff counts as a word, and a man who learns it was one lowers Frank's menace. A threat stops a report to the police, never the street's talk (his ruling of 3 Oct). A standoff is two sides each with a weapon shown; the first to move commits the street to rung 7.
- Standard: One rule set: swapping Frank for a townsperson with the same choices gives the same outcome spread (swap test owed). Most confrontations end on rungs 1 to 4; a threat is not a sure win. Simulated at menace 0.3: a bare word folds 12% of lone men, a cosh shown 28%, a knife shown 47%; two men together 0%, 2%, 5%. Test: B: the simulator's threat table; S: every man who folds to a shown weapon is a witness to rung 6
- Source: his combat design 12 Oct and ruling 3 Oct (ruled); the one fight model and talk rules DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-01, CS-10), for him to overturn
- Status: decided. Coverage row: 1.3.4.
- The chance rule (his pick A, 25 Nov, advisor 382; combat pass revision 1): readable rules decide outcomes; no hidden roll overrules a correct play; blows land, are blocked or slipped by what the struck man is doing, his guard by his reaction time against the wind-up; blows land on the attacker's line, not a zone table; knock-downs and knock-outs by thresholds on force and visible state; the low end of injury safe and certain; a small chance only at the violent end (a knife's depth, a fall at a kerb, a critical wound, a shotgun's spread, a choke held on, boots on a head), every such chance fixed to the save, so a reload replays the same act the same way. Simulator (seed 1990, 2,000 a scenario): careful one against one with fists won 73% (94% of decided), a masher 11%, careful two against one 29%; no deaths in 2,000 fist fights. Standard: the reload check (the same 200 stabs from one save under two random streams give the same outcomes). Status of this line: ruled.

### CS-08 Grabs, holds and the ground

- How it works: A grab (collar or arm) works unless the man slips it. From a grab: shove, shove into a surface, throw down, pin to a wall (about 2 s a press, and opens live talk), or take the weapon arm (a disarm: 40 in 100 it comes free and drops where anyone may take it). A man can grab Frank from behind while another hits him; Frank breaks free by pressing grab, a fresh Frank in about 1 s, an emptied one in 3. A choke in a fight works only from behind on a man busy with someone else, and takes half as long again; from the front it is a grab. A downed man can be kicked, struck, helped up or left, and gets up in 2 to 5 s unless beaten or out; a man on the ground can grab an ankle. No wrestling minigame.
- Standard: Every hold has a way out; a disarmed weapon is a real object on the ground. Test: S: a dropped knife can be picked up by the other man; B: the simulator counts disarms both ways
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-08), for him to overturn; his design (shove, grab, pin); KCD2 clinch and Sleeping Dogs grapples (census M021 to M030)
- Status: decided. Coverage row: none yet.
- Revision 1 (25 Nov; CS-08): a disarm follows grip and moment (winded, hurt, arm hurt, just swung), else a struggle for the arm; guns by the same rule. Unarmed Frank against a knife man won 48%, with a bat aimed at the knife arm 77% (simulator leads).

### CS-13 Takedowns from behind

- How it works: An unaware man reached within 1 m from behind can be taken by any action; nothing is instant or certain. Choke: a carotid hold puts him out in about 7.5 s (4 to 11; sources say 5 to 10); each second he may break free (about 1 in 30 at the start); the struggle is heard about 6 m. Released at once he is out 10 to 60 s. Held on deliberately he is in danger: none for 20 s more, then a rising chance (10% at 30 s, 40% at a minute, 70% at 90 s, near certain at two minutes), the man going still as the cue; this is his question D1 (open, recommended yes), a judgement curve. Cosh from behind: out about 6 in 10, knocked down 3 in 10, death about 1 in 200. Fist: out about 1 in 8. Knife: by where it lands, a thrust kills about 1 in 8. Failure: he hears the last step and turns, startled. An officer struck unseen does not know it was Frank (24 Nov).
- Standard: No instant kill, no guaranteed knock-out; failure believable and readable. Simulated (unlit street, crouched, wet cobbles): choke out 40%, broke free 17%, spotted 38%; cosh out 35%. Test: B: the simulator; S: a held choke follows the curve once D1 is answered
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-13), for him to overturn, D1 his; combat/RESEARCH.md (carotid timings; no firm threshold); his rulings 24 Nov
- Status: decided. Coverage row: none yet.
- Revision 1 (25 Nov; D1 yes): the choke has no break chance except a big, fresh man against a winded or hurt Frank, time by build 6.5, 7.5 or 10 s; a cosh from behind puts a man out every time and one blow never kills; a fist from behind floors, never puts out; a choke held on after he passes out can kill, the body showing it, no risk for 40 s past the knock-out, 20% at 60 s past (simulator; C-548).

### 1.3.5 The street as a weapon

- How it works: Seven places first: walls, doorways, railings, car bonnets, steps, kerbs and the quay edge, each a paired move fitted by height. Surfaces are force, not finishers: a shove or throw into a hard surface hits at force 2.0 and the man is out of the fight about 4 s; glass adds a cut by the edge rule; phone box and quay bollard count too. Car doors can be slammed on a man (force 2.0 to an arm or head). Doors can be slammed, held shut or kicked open (a locked one takes several kicks and is heard). A heavy blow or run on wet cobbles slips 1 time in 20. Light can be changed (a bulb broken, a switch flicked). A man put in the water climbs out at the nearest ladder within a minute if conscious; unconscious and face down he is dying and dead in about two minutes unless pulled out. Frank never swims and can pull a man out from the steps. Every move is fully animated, no cut-away (his ruling of 24 Nov, Q4); blood and light gore only (canon).
- Standard: Seven places first, fitted by height (Sleeping Dogs' environment moves as the reference). Shove into a surface never takes a man past serious (his fists line). Quay: conscious man out within 60 s; unconscious face down dead by about 130 s. Test: S: each of seven places triggers its paired move; content check: no cut-away, gore light
- Source: DESIGN §7; FEEL-TARGETS-MELEE (a); his rulings 30 Oct and 24 Nov; surfaces, water and doors DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-07; cold-water figure from combat/RESEARCH.md, Tipton), for him to overturn
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 1.3.5. Conflicts settled: C-273, C-356.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov). Data sweep class B.
- Revision 1 (25 Nov; CS-07) and his decision 6: an unconscious man face down in the dock drowns in about two minutes, a killing; a conscious man climbs out (4.2.4 reworded, C-543).

### 1.3.6 Things to hand and carried weapons

- How it works: A weapon is a row of data, never a special case: kind (blunt, edge, firearm), force, wind-up, reach, wind cost, blows before it breaks, whether it hides under the coat, the menace it carries when shown, its noise and the evidence it leaves. Carried: knuckleduster, cosh, bat, utility knife, flick knife (his 12 Oct tiers; makes fictional). Things to hand break: a chair after 2 blows, a brick 3, a dustbin lid 4, a wheel brace never; anything graspable within 1.5 m that the props list marks can be swung or thrown. Never a bottle, a glass or anything to do with drink (canon). A knife is usable from the first second of a fight (advisor 374). Two things under the coat at most. A weapon comes out on a held input (semicolon) and cannot be undrawn unseen. A thrown thing hits by its force at half the wind-up and is left where it falls; a carried knife thrown is gone. A knife against one unarmed man nearly always wins, as in life; its price is the body count and what follows.
- Standard: Every weapon a data row with its answer (a grab on the weapon arm, a chair, numbers, running); breaks after chair 2, brick 3, lid 4, wheel brace never; C2 swing 0.80 to 1.05 s; a weapon drawn cannot be undrawn unseen. Simulated: a knife wins 99% of decided fights against one unarmed man and about 3 in 4 against two. Test: B: weapon table; S: props list carries the graspable flag, no drink item flagged; a cosh from behind on an unaware man is seen as a strike
- Source: his ruling 25 Nov (advisor 374: a knife from a fight's start); his design 12 Oct (four tiers); weapon table DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-06), for him to overturn; no reference figure for swing time yet
- Status: decided. Coverage row: 1.3.6.

### 1.3.7 Condition without bars: the body rule

- How it works: There is no health bar: posture, breath, a dropped guard, blood and a limp show a man's state. One rule decides every injury for every person from what struck, how hard, where and the state of the man struck. Zones are head, torso, arms, legs. Blunt harm adds up by zone (the head a quarter more): bruise, hurt from 3, serious from 9.5, critical from 15 on the head or 22.5 on the body. Edges and points do not add up: each cut or stab draws its wound by zone (a body thrust: minor 40%, serious 44%, critical 16%; neck or face 25%, 40%, 35%; arm 70%, 27%, 3%; leg 62%, 32%, 6%), so where a stab lands decides and a body stab can kill (advisor 374). Critical means dying: about 55 in 100 die unaided, about 20 helped. His fists line stands: fists and a shove into a surface never take a man past serious; a fall can (1.3.5, RT2-12). Knocked-out men breathe and twitch, never look dead. States: fresh, hurt, beaten, down, out, dying, dead; Frank alone never reaches dead. No armour, no healing items (24 Nov).
- Standard: Deaths from fist fights alone at most 1 in 1,000 (by the fall rule only); a knife fight kills roughly 1 in 10 (UK hospital data 7.2% of stabbed patients died; one Icelandic series 17% before hospital); a beating to submission leaves most men hurt, about a fifth seriously; knock-out 10 to 60 s from fists, 30 s to 5 minutes from a weapon. Test: B: seed 1990, 2,000 fights a scenario: fist fights 1 death in 2,000, a knife used by Frank 94 deaths per 1,000; H: 'who was winning?' right 4 in 5
- Source: his rulings 30 Oct (fists never kill alone) and 25 Nov (advisor 374); rule and edge table DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-04, CS-05; combat/RESEARCH.md), for him to overturn; the edge table is judgement inside the research bands
- Status: ruled (his ruling or canon). Coverage row: 1.3.7. Conflicts settled: C-350, C-353.
- Story conflict C-338: answered by CS-18 (a broken arm in plaster for weeks: no heavy blow with that arm, driving clumsy); see 1.3.11.
- Story conflict C-338 (run 5): The part gives Frank three states (fresh, hurt, beaten) with marks lasting one to five days, while the story needs a lasting arm in plaster that changes driving and the quay's fists. Until designed, the part stands; the need is a gap for the design proof.
- Revision 1 (25 Nov; CS-05): knock-down and knock-out by thresholds on force and visible state, steadiness measured before the blow's own harm; one finishing blow raises harm one level at most, with the cue (he stops covering, goes still; "He's not moving. Again?"); D2 yes: kicking a man on the ground can kill, rarely (31 deaths per 1,000 fights kicking on regardless, 0 stopping at the cue, simulator leads); his decision 7: cold kills after a stated time under the body rule.

### 1.3.8 Odds, crowds and nerve in a fight

- How it works: Every half second each man not acting chooses: press, hold, back off, look for something to hand, call for help, yield, beg or run. The choice comes from his will to fight: nerve plus friends standing, minus the menace of what he faces (knuckleduster 0.35, cosh 0.45, bat 0.55, knife 0.75, gun 1.0), minus hurt, minus being outnumbered, minus Frank's menace; grudge adds. Watched by his own people he stands longer. Low will: he runs if he can, else yields; beaten and cornered, he begs. A skilled player wins most fair one-on-ones (simulator: careful 79%, masher 19%) and tuning by fighter kind keeps a boxer or big man near even. At most two swing at once; the rest circle, cut off the way out or grab from behind; crowds are bodies and a wild blow can hit a bystander; friends join by ties. Two against one is deadly and three a beating; Ron at Frank's shoulder turns two against one into a fight he usually wins. A man seen running from every fight loses menace.
- Standard: Skill beats mashing: a patient fighter wins most fair one-on-ones, a masher under 3 in 10 (ER-FIGHT-07); fair two against one: skilled about 1 in 4 (simulated 29%), masher under 1 in 10 (0.1%); three against one 1%; with Ron (2 v 2) 78%. About 2 in 5 men yield and 1 in 7 run against a careful Frank. Test: B: scripted patient and mashing fighters; seeded nerve cases
- Source: DESIGN §7 ER-FIGHT-07; his design 12 Oct; DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-09, CS-11; simulator seed 1990, rare-event rates are leads), for him to overturn
- Status: decided. Coverage row: 1.3.8. Conflicts settled: C-359.
- Studies: FF-07 bot bands; DECIDES-CHECK 24 Nov: against several is a lead, at most two swing 0.4 s apart is decided (ER-FIGHT-02).
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov); the combat pass's numbers (wind costs, weapon forces, edge table) are for the next data wave. Data sweep class C.
- DECIDES-CHECK, 24 Nov: against several is a lead, not deciding: at most two swing, 0.4 s apart, is already decided (ER-FIGHT-02) and the method is built whatever the number.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G07, G08.

### 1.3.9 How a fight ends and Frank losing

- How it works: A fight ends when someone backs off, runs, yields, begs, goes down or is knocked out, a bystander steps in (odds rise about a tenth for each watcher), the police arrive or friends pull a man away. Backing off and running are inputs at every moment. A yielded or downed man can be left, helped up, robbed, held one night (no tying shown) or spoken to live. Frank's own yield (hands up) is answered by the other side's purpose: a man defending himself leaves, a robber robs. Frank cannot die: when the body rule would make him dying he is out instead. He comes round on the pavement, in a neighbour's kitchen (Grace Rinaldi's, with regard) or in hospital, where he wakes to days and the bill his 12 Oct design names (its size open, R14: recommended small, from the price list) and a witness is planted; what it costs follows who beat him: robbed by men who rob (RT2-13), taken to a rival's boss, cautioned by a constable, or left. He is in control within 60 real seconds with the cost said, and the town knows he lost. The men who did it can be fronted, paid or let go.
- Standard: A way out at every moment (ER-FIGHT-03); Frank never dies, in control within 60 real s (ER-FIGHT-04); no dead end. Simulated Frank beaten or out, never dead: 5% of careful one-on-ones, 43% of two against one. Test: S: every lost-fight route reaches a come-round within 60 real s (not simulated); each of five endings scripted
- Source: his ruling of 12 Oct (Frank cannot die; canon OPEN 3) and 24 Nov; hospital bill from his 12 Oct design as the combat pass reads it (the 12 Oct text not re-read by the keeper); manner of endings DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-14, CS-15)
- Status: ruled (his ruling or canon). Coverage row: 1.3.9. Conflicts settled: C-014, C-352.
- Studies: FF-01 failure costs game hours and standing, never replayed minutes; FF-07. None measured.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G07.

### CS-16 Bodies and evidence, 1990

- How it works: An unconscious man or body can be dragged (0.9 m/s), carried over the shoulder, put in a boot (4 s), rolled into the dock (3 s) or left. Bodies are found by people on their routines (2.5.5) and by smell after days. Evidence is what 1990 had: fingerprints on smooth surfaces compared by hand on the 16-point standard (days), blood on clothes until washed, blood group but no DNA database (1995), a weapon with a history, fibres, tyre and shoe marks, and witnesses above all. Getting rid of a weapon is itself a deed someone may see. A car pushed off the quay with a body is a big loud deed: divers come, the registration is traced and the boot searched. A bloodied coat can be burnt or washed. Carrying or dumping a body is read as a killing seen, at the grave band.
- Standard: The police know only what someone perceived or a search found (FF-05). Test: S: golden rows: a print on a knife handle names Frank only if his prints are on file (after an arrest)
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-16), for him to overturn; combat/RESEARCH.md (16-point standard 1953 to 2001; NAFIS 2001; DNA database 1995)
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13, G15.

### CS-17 How the street reads a fight

- How it works: Every confrontation is a deed with the seven slots plus how it was done: weapon, from behind, on a man down, on a man who yielded, the victim's sex and age, numbers. Reading is severity times manner: from behind 1.3, on a man down 1.5, on a man who yielded 1.6, with a weapon 1.4, on a woman or anyone over sixty 1.5 (the town's reading; Frank's own line is dropped, RT-09), dirty fighting 1.2, a fight in a church, hospital or tea room 1.3, a threat against a man's family 1.3. Provocation (the other struck first) lowers it to 0.7 if Frank stopped when it stopped. Gossip carries the manner and blurs it with distance and retelling. The reading moves menace, fear, regard and the local paper. Service is a temper decision: a shopkeeper refuses or serves frightened; a landlady Frank hurt puts him out. The street's mood follows the violence it has seen and is never wiped (canon).
- Standard: The same injury reads differently by manner; a player can hear the manner come back in talk. Test: B: consequence counts by band; S: gossip golden rows carry the manner slot
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-17), for him to overturn; canon (moat, gossip); 30 Sep witness ruling; his ruling of 24 Nov (RT-09 dropped)
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G08, G19.

### CS-19 Police, charges and the heat after a fight

- How it works: The police act on what is reported and seen. The charge follows the injury and manner in 1990 terms: common assault (up to 6 months); actual bodily harm (s.47, 5 years); wounding or grievous bodily harm (s.20, 5 years); with a weapon, on a man down or yielded, or critical, GBH with intent (s.18, up to life); a death, manslaughter or murder; assaulting a constable, Police Act 1964 s.51. A report needs a witness who tells or a victim with high law; a threat can stop that, never the talk. A beat constable is a person on the same rules with a truncheon and a radio: he shouts to stop, holds the man he takes to be at fault, and strikes and radios if resisted; help comes in minutes. Holding or robbing a constable is grave. Killing a constable brings the long heat (24 Nov: always recoverable, bribery possible, an officer struck unseen does not know who). Bent officers can be bought (DS Ellis about £800 then £100 a week).
- Standard: No charge without what a witness or search gives; every route recoverable. Test: B: every injury maps to its charge (seed 1990); S (build): whether a charge is laid needs a witness
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-19), for him to overturn; combat/RESEARCH.md (OAPA 1861, CJA 1988 s.39, Police Act 1964 s.51); his rulings 3 Oct and 24 Nov
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G17.

### CS-20 Revenge and the man who comes back

- How it works: A beaten man's grudge times how badly he was hurt and shamed decides: he lets it go; tells (by his law dial); comes back alone (high nerve) or with friends (low nerve), usually within three game days; or sends word to whoever protects him, and a rival outfit takes it up as an insult. A man whose friend was beaten may come instead. Revenge can be met by fighting, talking (an apology, a payment) or sending men first. Settling a grudge ends the feud, never the memory. A beaten man can be recruited if his regard turns (a fair fight, a spared yield, money).
- Standard: Every man Frank beat crosses his path again within three game days (STORY-05; a meeting, not always a fight). Simulated: about 3 in 10 beaten men take revenge, about 1 in 12 report it. Test: S (build): the routine-crossing rule
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-20), for him to overturn; the temper model (grudge); PLAYERS-STORIES STORY-05
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G08, G02.

### CS-21 Sending men to do violence

- How it works: Frank orders a man hurt, frightened or taught a lesson through a crewman (D56's first crime verb). The crewman carries it out by the same fight rules and his temper decides whether as asked, less or more (a high-grudge man goes too far). He is a second person who knows: the accomplice is the risk. Striking or threatening one of his own men costs regard with him and every crewman who hears; low regard and high nerve refuses or quits; high grudge may sell Frank to a rival. Rivals may go for Frank's men. A send to kill is possible within canon, rare, refused by a crewman with high law or low regard, and he knows forever. A crewman with a gun follows the same dial as Frank.
- Standard: The result of a send is decided by the fight rules, not a dice roll on success. Test: B (owed): sends through the simulator with the crewman as the fighter; not run
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-21), for him to overturn; his design 12 Oct; D56
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G07, G10.

### 1.3.10 Firearms

- How it works: Guns are rare and late, after melee, and AAA when used. None in the Hook at the start; they come only through people. A held semicolon draws from under the coat, the camera goes to an aim row, there is no crosshair and no ammunition count; the aim is from one fixed shoulder (24 Nov); an empty revolver clicks; no gyro aiming, scope, explosion or ammunition types. A gun is a weapon row with the highest menace (1.0): men without guns run or take cover behind anything solid, which blocks a shot; a shut door or walls cut a shot's sound to about a quarter. A shot is heard to about 177 m by day and whoever hears it keeps it for good. The dial runs Fists, Shown, Fired, War and moves only on a gun seen or heard. Carrying a gun is a charge in itself. Before War a hit wounds and never kills, at War it can kill: the combat pass recommends the body rule for guns at any time (his question D3, open), with the dial governing who carries guns and how the police answer.
- Standard: Guns rare and late (ruling 18 Nov end state A); AAA when used; shot heard 177 m by day; feel numbers to be measured. D3 answered yes (25 Nov): a gunshot can kill at any stage, by the body rule and CS-31's zones. Test: S: dial rules; wall stops a shot; feel numbers inside measured bands once researched
- Source: RULINGS 28 Oct combat line (18 Nov end state A); DESIGN §7 dial; D3 answered yes 25 Nov (combat pass revision 1: COMBAT-SYSTEM.md CS-23, CS-31; combat/REVISION-1.md)
- Status: unmeasured. Coverage row: 1.3.10.
- Prior research: game-design/weapons-spec.md (approved 29 Jul): a .38 heard about 177 m, capped at 250 m; its bottle line is struck by canon. Checklist 23 Nov (A19.04, A19.09, A19.11): recoil, rate of fire and empty-gun cue still to measure; empty click answered 24 Nov.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov); the combat pass's numbers (wind costs, weapon forces, edge table) are for the next data wave. Data sweep class C.
- Checklist (23 Nov, top twenty no. 12; A19.04, A19.09, A19.11): missing: each gun needs visible recoil with aim return, a rate of fire, and an empty-gun cue (click and hand action) since there is no ammunition count; all measured against the firearms footage. Gap for the design proof; status unchanged. Answered 24 Nov for the empty gun: the empty revolver's click is in (his ruling of 24 Nov).

### 1.3.11 Marks that last

- How it works: Every injury is a record on the person with its days: a bruise a day or two; hurt (a cut lip, a black eye) three days, shown; serious (broken nose, ribs, a stab stitched) a hospital stay of 3 to 14 days and marks for weeks; a broken arm in plaster for weeks, changing what he can do (one-armed: no heavy blow with that arm, driving clumsy). Split knuckles from punching show and slow the grip a day. A man fighting on while hurt worsens and collapses sooner. Townspeople and crew heal on the same clock and are off their routines meanwhile. Others see Frank's marks (a give-away) and say so. A bat leaves a limp; a knife wound bleeds, blood on the coat, until stitched. A retired doctor in a terrace by the quay stitches for money (£20 in the price list) and remembers. No healing items.
- Standard: Condition shows in the body, never a bar; a mark is a give-away; injuries last their days on the same clock for everyone. Test: S: a marked Frank is caught more; marks fade on the clock; records last their days; ER-MARK-01
- Source: DESIGN §2, §7; his ruling of 24 Nov (no healing items); levels and days DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-18), for him to overturn
- Status: decided. Coverage row: 1.3.11.
- Studies: MEM-04 a man Frank beat shows a mark for a game day and mentions it first; STORY-04; STORY-05 every man he beat meets him within three game days; FF-04; IM-04. All decided, none measured.
- Story needs (frame, 24 Nov, S26): the lasting arm in plaster is now designed here (answers C-338).
- The body shows the day (catalogue 23 Nov, rank 6; seen in 3 games): Bruises, blood and dirt show and are noticed. Partly: short are wet coat and hair in rain and breath on a cold night (a soaked man talked of is in 4.2.4; wetness drives the look in 2.1.4). Feature only; no timing; the part's status is unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Story needs (frame, 24 Nov): a lasting injury, the left arm in plaster, that changes driving and the quay's fists, with days and rescuers read from the record (SYSTEMS-THE-STORY-NEEDS S26; Frank's deeds carried F6, F7, S57). Partly covered: marks last days; a lasting arm injury and a one-armed Frank are missing (see CONFLICT 1.3.7).
- Rules (question passes, 25 Nov; BLUEPRINT-12): G19.

### CS-22 Fire

- How it works: Fire can be set at any time and can kill (his ruling of 25 Nov). It spreads by material and wind, is seen and smelt, draws a crowd and the fire brigade, and a man trapped inside follows the body rule (smoke critical in minutes). Arson is its own deed, read grave if anyone was inside, to town and police like any other killing. It is not a hand weapon; hot fat, scalds and burns as weapons are out (cruelty, canon). The spread model (terraces, cars, warehouses) is a gap for the place parts.
- Standard: His ruling; the street reads it as grave. Test: S: golden rows for an empty and an occupied building
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-22), for him to overturn; his ruling of 25 Nov
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G18.

### 1.3.12 Fighter types

- How it works: Every fight's men are written as one of a few kinds, each a row of the same fight model, not special code: a boxer who guards, a brawler who rushes, a big man slow to drop, a man with a knife who keeps his distance, and a wiry one who slips and runs. Capacity differs: a big man 21, a boxer 15, a brawler 14, a wiry or knife man 12, Frank 12 (simulator values). No two fights in a row use the same mix, so Lee on the quay, Iveson's yard hand and the two dockers by the car each feel different. Each outfit has a way: the dockside syndicate's men come in numbers and grab; Cammack's crew draw a knife quickly and run quickly; Agar's men avoid fists and send for help.
- Standard: At least five kinds, no two fights in a row with the same mix (ER-TYPES-01); players punish the same loop. Test: S: the job data; addendum rules ER-TYPES-01
- Source: PLAYERS.md; DESIGN §18; DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-04, CS-11), for him to overturn
- Status: decided. Coverage row: 1.3.12. Conflicts settled: C-015.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov). Data sweep class B.

### CS-24 Frank's growth in the hands

- How it works: Frank rises mainly in position (crew, name, weapons, the menace the town has seen); skills are taught by those who trust him and kept if lost (Ron teaches the slip and counter window, the pin and the choke; the boxing club teaches guard and wind); hand skills improve quietly with practice, at most a quarter better (a wider counter window, less wind per blow, a firmer grab). No numbers shown, no skill tree. Sparring at the club or with Ron is practice without hospital (blows at a third of force, no knock-out past a count). This marks his 12 Oct line 'never gets better at fighting' as replaced by the later ruling.
- Standard: At most a quarter better; no skill tree. Test: B (owed): simulator with Frank's defence and wind at 1.25 times shows the gain stays inside a quarter
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-24), for him to overturn; RULINGS 23 Nov (growth); his design 30 Oct
- Status: decided. Coverage row: none yet.

### CS-25 Fight difficulty, assists and accessibility

- How it works: No difficulty levels (D27, D30), only assists that change their own thing: longer wind-ups (25%), auto-resolve a fight (the same rules at a different tempo), the seeing assist, sound shown as words, hold or toggle for guard, crouch and run, full rebinding, subtitles with speaker names, danger cues readable without colour, reduce motion, a gore setting, a simplified scheme (one button strikes, guard automatic against the man in front, timing still counts) and the minimal HUD switch his design names (a small figure for Frank's state, off by default, never anyone else's). Early on Frank is alone and fights are risky; crew, name and weapons tip the odds later while rivals send more men; nothing scales enemies to him.
- Standard: Each assist changes only its own thing. Test: S: screen inventory with each assist; B: auto-resolve uses the simulator's rules
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-25), for him to overturn; his design (accessible); D27, D30
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G24.

### CS-26 Fight sound and animation

- How it works: Blows differ by surface and body part; breath and grunts carry state; footsteps by surface; a shot by place (street, warehouse, over water). Animation is lab-tested before building (his ruling): motion matching for footwork, motion warping to line bodies up, physics reactions blended over authored ones with a cap on how far a body flops, paired moves per surface fitted by height; faces show pain, fear and anger; clothes pull when grabbed. No clip shows drink, gambling, children, torture or cruelty as spectacle.
- Standard: The animation source passes the lab test (one wind-up, strike, hit reaction, shove into a wall) before any build; content gate on clip names. Test: the lab test
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-26), for him to overturn; his design 12 Oct (the animation question); RULINGS 30 Oct and 25 Nov (advisor 379)
- Status: pending. Coverage row: none yet.

### CS-27 The inquiry into a death that is not a constable's

- How it works: A body found, a man dead in hospital after a fight or a man missing long enough to be reported starts an inquiry by the local CID (DS Ellis's office): the scene, the body, statements from whoever the record says saw anything, the dead man's ties. It needs what any charge needs: a witness who tells, evidence that names (CS-16) or a confession; without them it stays open. A bought Ellis slows it, steers it to another suspect if one fits, and stops short of covering a killing the town saw. Frank may be leaned on if talk points at him. A constable killed by anyone is the long heat. What the story does when a principal dies is the story pass's, a gap.
- Standard: No charge without a witness, evidence or confession; always recoverable. Test: S: golden rows for a body found with no witness, with one witness, and with a print on file
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-27), for him to overturn; his ruling of 24 Nov (long heat; Ellis bribable); the 1990 police research
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G16.

### CS-28 Edges a player will try

- How it works: Saves keep everything: a chase, manhunt or long heat carries across a load; reloading is never stopped, and the game says when something is permanent (D27, D30). No fighting on anything moving; Frank cannot climb on a moving car. No animal is ever harmed. A car can knock a person down and hurt them badly, never kill; a man knocked into the water by a car climbs out; a claim of accident is a cover story against what witnesses saw. Hiding in a car boot is a hiding place like a doorway, and a car search finds him. Pulling a driver out to take the car is in (his ruling of 25 Nov, advisor 378): loud, reported, heavy consequences; the pass's recommendation to leave it out is overruled.
- Standard: No dead end, no harmed animal, no killing car. Test: S: each edge as a golden row
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-28), for him to overturn; canon (cars, content rule); RULINGS 24 and 25 Nov (advisor 378 for the driver)
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G14.

### CS-29 Smaller fight rules the census asked for

- How it works: One line each: cross and hook are the heavy blow by angle, no third button; cover is moving behind something solid, no snap key, a wall stops a shot; carried weapons are bought (a utility knife and a cosh-length of pipe at the ironmonger), taken or found; a cover story to a constable is a claim, running from an arrest is a new offence; taunts are written ahead in period speech, slurs never; dirt on a man is a give-away; any coat is a give-away changed, never a key; a downed constable's tunic and helmet can be worn with the limits of CS-33 (his ruling, advisor 388; C-542); a yard or closed shop after hours is a wrong place; lifting from a pocket and planting are one verb with readable limits (1.6.13; his decision 12, 25 Nov; C-541); the bank's camera is the only one, tape recycled weekly; gossip cools by severity; breaking Garbutt's truce is read grave and the wronged outfit takes revenge; a man who runs from every fight loses menace; the ambulance takes 10 to 15 minutes and attacking medics reads at 1.6; ragdolls are capped and settle in seconds. Out: a stranger spawning to rob the loser, bailing from a moving car, stacking bodies as furniture.
- Standard: Each line a golden row or part of another test. Test: S: golden rows
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-29), for him to overturn; census rows; RULINGS 24 Sep, 30 Sep, 24 Nov
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G11, G13, G02, G03, G04.

### CS-30 Rules the second blind check asked for

- How it works: One line each: one action is held, never a queue, and a press 0.1 s early counts; a groin kick is a low kick, grit in the eyes blinds 2 s, both read dirty; a thrown thing is aimed like a blow with no reticle; broken glass and stalls are deeds against their owner, who asks for money or tells; a weapon under a coat shows as a bulge or a hand near a pocket, no icon; backing down is always there and the town remembers who did; a held man lies, stalls or bargains by his temper and says only what he knows; speech mid-fight is written lines, live talk opens with a man pinned or yielded; a shop bell rings at its reach and wired alarms are rare (the bank, the chandler's); orders are a held key and a word, no wheel; casualty passes a stab or gunshot to the police; blood stays until rain or a hose; a dead man's ties grieve with a funeral within the week; an alibi is a claim by another person; waiting at a man's home is a deed his household sees and nobody can be farmed by repeat beating.
- Standard: Each line a golden row. Test: S: golden rows
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-30), for him to overturn; the second blind check (census rows M411 to M463)
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G08, G07, G12.

### CS-31 What each part of the body does

- How it works: Where a blow, stab or shot lands decides what it does, by readable effects shown in the body, for everyone (his question of 25 Nov 10:52). Arm: drops what that hand holds, no heavy blow or carrying with it until treated, a broken arm in plaster for weeks. Leg: cannot run, crawls. Torso: drops him, serious to dying. Head and face: knock-out, a broken face, dying; a facial mark the town names him by. Neck: the most dangerous. Arms and legs take blunt harm on their own count: 6 on one limb breaks it (a bat's full heavy blow on a forearm, a boot to a knee); fists alone never get there. An aimed shot to the arm disarms and one to the leg stops a runner (Y1.5, restored). Guns are worse than a knife, with the hit by aim and the sway shown in Frank's arms.
- Standard: each zone's effect for blunt, blade and gun a golden row; fists never break a limb; the simulator's gun table (revolver body hit at 8 m: hits 79%, kills 21%; sawn-off at 3, 10, 20 m: kills 50%, 18%, 1%) a lead to retune. Test: S: golden rows; combat/SIM revision 1
- Source: DECIDED by the combat pass revision 1, 25 Nov (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-31, REVISION-1.md), for him to overturn; wounds research partial and dated 25 Nov (rev1-work/RESEARCH-WOUNDS.md: two Swedish gunshot series, 30-day mortality 13% and 17% of those reaching hospital; per-region figures not reached from the cloud)
- Status: decided. Coverage row: none yet.

### CS-32 Where weapons come from, and the law of 1990

- How it works: Every weapon in the Hook has a place it came from, a person who saw it change hands, and a law it meets; every make fictional. From homes (a kitchen knife, a hammer, a poker; free, missed by the owner, who may say so); the ironmonger and the ship's chandler (knives, hammers, a wheel brace, pipe, a crowbar, rope; rigging knives, a marlinspike, cargo hooks; sold openly, the seller remembers a buyer by the witness rules, his ruling of advisor 378); Rita's back room with Wayne (knuckledusters and flick knives, which nobody could lawfully sell in 1990: under the counter, only to a man Rita trusts, rung 2 and up, dearer, and Rita or Wayne knows; Frank can sell there too); off a man, off a body, a rival's lock-up; guns only through people (RT2-14, kept). The law of 1990: a blade in public (s.139, a fine only; a folding blade under 3 inches exempt; good reason); the s.141 Order in force 18 Jan 1989 (knuckledusters, butterfly knives, swordsticks: no selling, private possession lawful); flick knives (the 1959 Act); no under-16 knife rule until 1 Jan 1997; a revolver under a section 1 certificate, a shotgun shortened under 24 inches outside the shotgun certificate.
- Standard: every weapon in the data has a source, a seller or owner who remembers, and the law it meets (golden rows). Test: S: golden rows
- Source: DECIDED by the combat pass revision 1, 25 Nov (COMBAT-SYSTEM.md CS-32), for him to overturn; law research dated 25 Nov (rev1-work/RESEARCH-LAW.md, legislation.gov.uk enacted and point-in-time texts, Hansard; the s.139 commencement order, the 1990 Schedule 6 terms and the 1953 Act's definition text not reached, marked unverified); prior research: game-design/weapons-spec.md (approved 29 Jul; its bottle line struck by canon)
- Status: decided. Coverage row: none yet. Hand-over to Monday's people pass: inventories by role, shop stock and prices, Rita's trust rung.

### CS-33 Searching anyone who is down, and the constable's kit

- How it works: Anyone down, out or dead, can be searched and carries what fits his role (his ruling, advisor 376). Kneel and go through his coat and pockets, about 4 s (a constable's belt kit about 6 s), hands full and back to the street, little noise; each thing taken or left. A beat constable in 1990 carries a wooden truncheon, handcuffs, a whistle, his personal radio, his pocketbook and his warrant card (the 1990 kit partly unverified, to check from the PC). The truncheon is a cosh's weapon row; the radio lets Frank hear police traffic while he holds it, until the station notices it has gone quiet; the pocketbook holds the day's names, descriptions and times. Taking anything from a man down is theft, or robbery if Frank put him down; from a constable it is read grave and raises the police response; police kit found on Frank later is evidence; a dead man's things on Frank are recognised by anyone who knew him. His tunic and helmet can be worn (his ruling, advisor 388, his A): a minute to take, done openly and remembered; distant strangers defer and may report to him; anyone close or who knows Frank sees through it; the police soon notice an unknown constable; caught, it is a grave crime; it traces to its owner.
- Standard: searching takes about 4 s (6 s for the belt kit) and finds only what the role's inventory holds; stolen police kit raises the police response; the worn tunic fools only distant strangers who do not know Frank (golden rows). Test: S: golden rows
- Source: his rulings of 25 Nov (advisors 376, 388; RULINGS on wip); COMBAT-SYSTEM.md CS-33 (revision 1) for the timings, DECIDED, for him to overturn
- Status: ruled. Coverage row: none yet. Conflicts settled: C-542. Rule: G16.

### CS-34 Can-yous beyond the big three

- How it works: The combat pass's list of things a player can do here that KCD2, RDR2 and GTA V do not allow, each checked for fun, for fit with Britain 1990 and for the animation it needs (a shared set reused across many people and acts where possible); for example, breaking a knife man's arm with a bat so he drops it, fights one-handed and walks the street in plaster for weeks. "Beyond" is on paper, from the census and general knowledge of the three games, not measured.
- Standard: each line passes fun, fit and an animation budget; the shared clip set reused wherever it serves (CS-34's table). Test: H: the panel's can-you questions
- Source: his principle of 25 Nov (advisor 377: "can you" far wider than KCD2, RDR2 or GTA, by general rules); COMBAT-SYSTEM.md CS-34 (revision 1), DECIDED, for him to overturn
- Status: decided. Coverage row: none yet.

### CS-35 Lines the outside questions asked for

- How it works: Thirteen lines, decided within canon: thrown things hit by weight (light 0.5, middling 1.2, heavy 1.8, aimed like a blow, the face a quarter more); falls from height (pushed down stairs, force 2.5 on landing, serious about 1 in 5, critical 1 in 30, fixed to the save; off the sea wall onto stone serious every time, critical about 1 in 4; Frank alone is out, never dying); a car door opened into a passer-by (1.5 from the seat, 2.0 standing; an assault when meant); a collar grab in a calm talk (a rung 4 deed, the talk goes on with him held); and lines on losing, wronged people meeting, followers, suspicion adding up, a remembered noise, windows, searching a crowd, a bribed witness beaten, and the sawn-off at the legs.
- Standard: each line a golden row. Test: S: golden rows
- Source: COMBAT-SYSTEM.md CS-35 (revision 1; rev1-work/RESULTS-30.md), DECIDED, for him to overturn; not yet re-judged by a fresh tester
- Status: decided. Coverage row: none yet.

### RT-09 Frank's line against women, over-sixties and the priest

- How it works: Dropped (Q3, answered 24 Nov): the line is gone, not kept as character. Frank has no rule against striking, shoving or grabbing a woman, anyone of sixty or over or the priest, and does not refuse a send for it; the strike input is never refused by who the man or woman is. Everything else about fights, the ladder and the dial stands, and canon's content rule (no children anywhere) still holds.
- Standard: None: the line no longer exists. Test: none; the content-rule check for children stays.
- Source: his ruling of 24 Nov (RULINGS on wip, his decisions page), replacing the description section 10 and DESIGN-ADDENDUM A41's line. Designed in: DEFINITIONS §RT-09 (superseded); DESCRIPTION-COPY-2 §9; DESIGN-ADDENDUM A41
- Status: out. Coverage row: RT-09. Conflicts settled: C-016, C-275.
- Story needs (frame, 24 Nov): Frank's line covering the Widow and others (SYSTEMS-THE-STORY-NEEDS S45). Covered.

### RT-10 Firearms as a verb

- How it works: Guns are late and rare through the dial. A held semicolon draws from under the coat, the camera goes to the aim row from one fixed shoulder (24 Nov), and the mouse or stick aims with no crosshair (an optional dot, off by default). A hit depends on aim, distance and whether Frank moved. A hit follows the body rule and CS-31's zones at any stage (D3, answered yes 25 Nov): a body or head shot can kill, a named and permanent event; in the simulator a revolver body shot at 8 m hits 79% and kills 21%, the sawn-off kills 50%, 18% and 1% at 3, 10 and 20 m (leads, combat/SIM revision 1). An aimed shot to the arm disarms and one to the leg stops a runner (Y1.5). A revolver holds six and reloads in a shown action; empty, it clicks. No gyro, scope, explosion or ammunition types (all out, 24 Nov). Men with guns shoot from where they stand and run when outmatched; men without take cover behind anything solid; nobody shoots from a moving car. A shot Frank goes down, comes round in hospital and never dies.
- Standard: The rules above pass or fail; draw, aim and hit timings within the band of the firearms footage measuring. Test: B: a gun range scene with timings; S: no on-screen count; a wall stops a shot
- Source: The description §3, §33; ruling 18 Nov (guns rare and late); MEASUREMENTS-NEEDED A; Y1.5; D3 answered yes 25 Nov (COMBAT-SYSTEM.md CS-23, CS-31, revision 1; C-540)
- Status: pending. Coverage row: RT-10.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov); the combat pass's numbers (wind costs, weapon forces, edge table) are for the next data wave. Data sweep class C.

### RT-11 Hidden damage and injury states

- How it works: Each man has a wind (0 to 1) and a condition: hurt taken against his capacity by fighter kind (1.3.12). A jab costs 0.12 wind, a heavy 0.20; below 0.18 a man is emptied, hands drop and he gasps; blows land weaker as wind falls. Force is the action's (jab 1.0, heavy 2.6, kick 1.7, boot on a downed man 1.6, shove into a surface 2.0) times the weapon (knuckleduster 1.35, chair 1.7, cosh 1.9, brick 2.0, bat 2.3), half again unseen or on a counter. A weapon blow does more than a heavy fist blow (bat more than cosh). States are shown only in the body: fresh, hurt (from 40% of capacity: guard slower, breath short, a stagger), beaten (can barely fight, yields or runs), down 2 to 5 s, out, dying, dead; Frank alone never reaches dead. Down is out, never dead from fists. Injury levels and their days are in 1.3.7 and 1.3.11.
- Standard: 'Who was winning?' answered right by 4 of 5 testers from the body alone; blows to put a man down per kind within the band of the damage footage measuring (KCD2, Sleeping Dogs, RDR2). Test: B: fixed-seed fights counting blows to down per kind; P: the five-friend question
- Source: The description §10; MEASUREMENTS-NEEDED A; wind, force and states DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-04, CS-05), for him to overturn; KCD2 stamina as the core resource (census M016, M017)
- Status: decided. Coverage row: RT-11.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov); the combat pass's numbers (wind costs, weapon forces, edge table) are for the next data wave. Data sweep class C.

### RT2-11 Finishing a downed man, kicks and bodies

- How it works: Finishing is a decision in the quiet afterwards, never a move in the flow of the fight: with nobody else standing Frank stands over the man and holds strike or kick for 2 s, and the game asks twice. The blow on a downed man, and beating a man who pleads, stay, fully animated with no cut-away (his ruling of 24 Nov, Q4; PEGI 18 within canon's limits); gore light. A kick standing is a low kick; on a downed man it is the boot (force 1.6). What it does is the body rule: fists stay at serious; boots can reach critical, rarely (his question D2, open; recommended yes), the second ask then naming it ('He's not moving. Again?'); a weapon can kill. Watchers read it worse (1.6 on a man who yielded). A body is dragged at 0.9 m/s, carried over the shoulder, put in a boot in 4 s, or rolled into the dock from the quay edge in 3 s. A knife wounds or kills by where it lands (1.3.7), not only by finishing. Bodies and evidence are in CS-16.
- Standard: Camera never turns away, blows fully animated (PEGI 18), gore light; with fists yes is a serious beating, never a death. Simulated, if D2 is yes: finishing a downed man with three boots kills about 1 in 50 of the fights Frank wins (15.5 per 1,000 fights), with a cosh to the head about 1 in 22. Test: B (bot); content check: no cut-away, no cruelty as spectacle
- Source: his ruling of 24 Nov (Q4) and 25 Nov (advisor 374); boots and bodies DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-14, CS-16), for him to overturn; D2 is his
- Status: ruled. Coverage row: RT2-11. Conflicts settled: C-017, C-274, C-341, C-353.
- Story needs (frame, 24 Nov): finishing a downed man, worked example 3 reworded to the finishing decision unless a kick is added (SYSTEMS-THE-STORY-NEEDS S46). Covered by the part; the frame's example needs rewording (see CONFLICT).
- Story conflict C-341 (run 5): The part has no kick input and finishing with fists means hospital, while the frame's worked example 3 has Frank "put the boot in" to a downed taxman. Until designed, the part stands; the need is a gap for the design proof.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G24.

### RT2-12 The rare fatal fall

- How it works: A fall can kill when a heavy or weapon blow knocks the man down near an edge (a kerb, a step or a wall's foot, head within 0.4 m) and he was already spent (three heavy blows or one weapon blow taken). Beforehand he shows it, unsteady with guard down. His head strikes: serious about 1 in 10, critical 1 in 50 of such knock-downs; a critical man dies about half the time, so deaths run below the earlier band of 1 in 50 to 1 in 20. It applies to everyone's fights, not only Frank's. Never in the boxing club, never by a car, never to Frank (he is out instead), and away from any edge never. The quay edge works through drowning (1.3.5), not this rule.
- Standard: Fist fights alone: 1 death in 2,000 (open street and kerb alike, too few events to call a rate); deterministic for a given seed; never away from an edge. Test: B (bot): kerbside scenario, seed 1990
- Source: his 30 Oct ruling (a fall can kill, rarely, a killing to the town); band reading DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-07; RULINGS-TO-REVISIT R17, R18), for him to overturn
- Status: decided. Coverage row: RT2-12. Conflicts settled: C-357.

### RT2-13 Robbed when beaten

- How it works: Frank is robbed when beaten by men who rob for a living (a rival's men, the dockers by car two, a robber), never by a constable, at the boxing club, or by a debtor standing his ground. They take the paper money in his pocket (coins are left) and anything in his hand or under the coat they want (the envelope, a weapon, goods), never the Ledger, his coat or the office keys. The takers are named men with routines, whom Frank can front up, send men at, or let go; a taken envelope becomes a debt to the landing men of what it held, said by Ron the next day.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-13 Test: B (bot), as written under RT2-13
- Source: design pass 3, RT2-13 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 RT2-13; DESCRIPTION-COPY-2 §9
- Status: decided. Coverage row: RT2-13. Conflicts settled: C-018.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-02 a failure takes only the money the design names; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/people/ (data build wave 2, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### WI-P15 Beaten again and again

- How it works: Each beating costs as the fight parts say. A third beating within a game week brings someone in: Ron comes to fetch him from the pavement or the hospital and says plainly what the streets are saying, and the men who beat him (named) are known in the Ledger; the robbers rob only what he carries (RT2-13), so a run of beatings cannot strip the office or the tin. No loop is closed: running, backing off and staying in are always open.
- Standard: Repeated defeat never strips the floor and always names who did it. Test: B: a bot beaten seven nights running keeps the office, car two and the tin.
- Source: 1.3.9 (replaced by CS-14 and CS-15 in the combat pass); RT2-13; RT2-06. DECIDED by the what-if sweep 24 Nov (production/lane/blueprint/what-if/PROPOSED-PARTS.md P15, D6) for him to overturn; CS-15 covers a run of losses in general, this part adds Ron's fetch and the floor.
- Status: decided. Coverage row: none yet.

### RT2-14 How guns reach Frank

- How it works: Two kinds of gun, both of fictional make: a service revolver (six rounds) and a sawn-off shotgun (two). None in the Hook at the start. Mickey's revolver lies in his inner office desk under the real book, found once when the locked office opens on Sheila's trust (rung 2; see the gap on guns rare and late). One seller, a deckhand off a coaster in on Tuesdays and Fridays, sells at the fish dock after midnight to a man introduced by Rita (rung 3) or Darren's tip: revolver £150, shotgun £90, rounds £10 a box (one kind of round only: ammunition types are out, his ruling of 24 Nov). A gun can also be taken from a man who drew one or from a body, or stolen from a rival's lock-up on a raid. A gun moves the dial only when seen or heard.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-14 Test: B (bot), as written under RT2-14
- Source: design pass 3, RT2-14 (waits on a dated study). Designed in: DEFINITIONS design pass 3 RT2-14; DESCRIPTION-COPY-2 §27
- Status: pending. Coverage row: RT2-14.
- Data (run 5): exact values in production/lane/blueprint/data/places.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.

### FIT-P17 At least five kinds of fighter

- How it works: At least five kinds of fighter, as data rows of one fight model: the boxer who guards, the brawler who rushes, the big man slow to drop, the man with a knife who keeps his distance, and the wiry one who slips and runs. No two fights in a row use the same mix. See 1.3.12 for capacities and outfit habits.
- Standard: At least five kinds in the data; no two fights in a row with the same mix. Test: B (bot) as written; S: the job data
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-04, CS-11), for him to overturn; design pass 3; FIT-CHECK-2026-11-21.md
- Status: decided. Coverage row: FIT-P17. Conflicts settled: C-019.

### FIT-P18 Two against one stays deadly

- How it works: Two against one stays deadly: a skilled player, patient and using the street, wins a fair two against one about one time in four; a masher under one in ten. Running and backing off are always there, and the street's places count double (a man put into railings is out of it for 4 s). Simulated (44,000 fights, seed 1990): careful Frank 29% (43% lost, 28% stopped by a bystander or the police), masher 0.1%; three against one 1% (84% lost); with Ron at his side (2 v 2) 78%.
- Standard: Skilled bot wins 15 to 35% of fair two against one, masher under 10% (the earlier text's one in twenty is inside it). Test: B (bot), 200 fights as written
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-11), for him to overturn; design pass 3; FIT-CHECK-2026-11-21.md
- Status: decided. Coverage row: FIT-P18.

## 1.4 Being seen

The felt side of the town's eyes: the player's three questions answered from picture and sound.


### 1.4.1 Reading watchers

- How it works: The world shows who has noticed him in bodies: a head turns, a longer look, a pause in a walk, two heads together, a step back at night, a figure at the glass of a lit window. The head turns at the start of the 1.2 s a watcher needs to know him, so there is at least 0.8 s of warning. A window is a watcher only when a figure shows at it (Ada in her dark front room is the one exception, learned once). A player can answer 'is he seen, how far did that carry, who noticed' from picture and sound eight times in ten, also with sound off and with the light cue off.
- Standard: Cue at the start of the 1.2 s to know him, at least 0.8 s before identification (ER-EYES-03); posture first (D29); a window is a watcher only when a figure shows at it (ER-NIGHT-02); reference behaviour to be measured Test: H: the three questions at ten random moments, 8 of 10 right, sound off and light cue off
- Source: DESIGN §2; D29 (waits on a dated study). Designed in: DESIGN §2 ER-EYES-01, -03; DESIGN §6 ER-NIGHT-02; DESCRIPTION-COPY-2 §7 Reality check (CHECK A84, A86; RESEARCH C2): the 1.2 s and the distances are prototype values, never measured in a game; one study found familiar faces recognised reliably only within about 15 m and above about 15 lux (abstract only), brighter than a lit side street, a flag for the measurement, not a change.
- Status: pending. Coverage row: 1.4.1.
- Prior research: research/detection-legibility: three states readable at once by posture and head turns, never bars; a readout is fair when it gives back what the character knows and the camera took away, cheating when it adds what he does not know.
- Deciding row (DECIDES-CHECK, 24 Nov, corrected by the reality check, 24 Nov): being seen in KCD2 and RDR2 sets only the watcher numbers (how fast and how far, under known light), hence cover places and the constable's ladder; it does not set lamp spacing, which comes from BS 5489-3:1977 (about 34 m plus or minus 10%) and dated photo counts (4.1.1, 4.4). The measurement is still first among the game rows, then applied to the real lamp layout; none sampled; two games planned, about 5 h.
- Deciding row (DECIDES-CHECK, 24 Nov): being seen in KCD2 and RDR2 sets sight distances and light scaling, hence lamp spacing, cover places and the constable's ladder; none sampled; two games planned, about 5 h.
- Reference solid (RDR2 and GTA VI; STATUS.md on wip, ladder-review-2026-11-25.md, eight uncut samples, four players): from a witness's flag to wanted, about 2 to 106 s, median about 33.5 s. A floor for the constable's ladder timing, folded as a reference; the part's own standard is unchanged (run 7).
- KCD2 being seen (STATUS.md on wip, 25 Nov 17:42): first uncut sample read from the alarm icon itself (a farm hand sees Henry at a lock: red about 1 s, a challenge within about 1 s, clear about 16 s after the alarm, no guard); one of five, a lead; RDR2 stays the only solid being-seen figure.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12.

### 1.4.2 Light and dark as cover

- How it works: The light value the watchers use is the one the player sees: the corners of the picture darken and lift with it (daylight 1, lamp 0.7, unlit street 0.25, doorway 0.12). Dark is readable, never blind: Frank and the ground 5 m round him are always visible above a brightness floor. Light can be changed in play: a broken bulb or a flicked switch changes it at once, and a lamp going out is noticed by anyone who sees it or knows the street. A torch shows its carrier, a lit cigarette is a light point visible far in the dark, and drizzle or rain, as his 5 Oct weathers, cut sight by the rain rule (no fog: R21). A dark coat at night makes his shape a fifth harder to pick out.
- Standard: Picture corners follow the rule's light value; Frank and 5 m round him always visible above a brightness floor (ER-NIGHT-01). Test: H: screenshots at the darkest spots; S: light value matches the cue; breaking a lamp changes the value within a frame
- Source: DESIGN §2, §6 (waits on a dated study); light changes and clothes DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-07, CS-12), for him to overturn; the numbers are judgement until the KCD2 and RDR2 seeing study
- Status: pending. Coverage row: 1.4.2.
- Deciding row (DECIDES-CHECK, 24 Nov): read with 1.4.1 (KCD2 and RDR2, about 5 h).
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12, G19.

### 1.4.3 Hearing his own noise

- How it works: Every noise the rule hears, the player hears at the same strength. Reach is set by act, surface, hour and weather: a walking footstep at night about 3.6 m on dry flags, a quarter more on wet cobbles, 1.7 times on gravel, about twice on a metal deck, more on broken glass; rain halves it and the day's traffic drowns it; crouched or slow walking halves it. Indoors a bare stair creaks at twice dry flags and carpet halves it; walls and shut doors cut a sound to a quarter, an open door to a half; sleepers hear at a third. A blow lands as a noise of about 8 m, broken glass 15 m, a shout 40 m, a shot about 177 m by day; the cab is heard within about 44 m by day. A street that has noticed him goes quiet. A 'sound shown' assist offers short words for deaf players.
- Standard: ER-SND-01: every noise the rule hears the player hears at the same strength; with picture off a walk is told from a run. Simulated: surface cuts a choke's success by a seventh to a quarter (crouched, unlit: wet cobbles 41%, gravel 35%, metal deck 31%). Test: H: sound-only test; S: reach by surface matches the table
- Source: DESIGN §17 (DECIDED by the design proof); surfaces and indoors DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-12), for him to overturn; judgement, no published detection numbers found (combat/RESEARCH.md)
- Status: decided. Coverage row: 1.4.3.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov); the combat pass's numbers (wind costs, weapon forces, edge table) are for the next data wave. Data sweep class C.

### CS-12 Senses and stealth, the settled details

- How it works: Stealth is the perception ladder canon holds, with these settled beyond 1.1.5, 1.4.2, 1.4.3 and 1.4.8: a watcher sees only where he faces, and how sure he is grows with light, nearness, movement and time in view. A man found unconscious is acted on by temper: helped, fetched help for, robbed or walked past, and a found man is a story that travels. Frank's men on a quiet job are noise and light like anyone: a crewman with low nerve or high mouth chatters unless ordered quiet. A mask or scarf hides the face slot but is itself a give-away; disguise fools strangers, never those who know him. No meters; the optional seeing assist outlines only people facing Frank. Everyone sees everything their senses allow, so a takedown seen is a deed seen.
- Standard: Stealth works and fails believably: crouched in the dark it mostly works, under a lamp or by day it mostly does not, a loud surface is felt. Simulated: unlit street walking 34% out, crouched 41%; under a lamp crouched 18% out, 73% spotted. Test: B: the simulator; S: no meter on screen
- Source: DECIDED by the combat pass 25 Nov, ready for review (production/lane/blueprint/combat/COMBAT-SYSTEM.md CS-12), for him to overturn; canon (perception ladder); census (KCD2 noise and visibility, Hitman, RDR2); combat/RESEARCH.md (no published detection timings found: judgement)
- Status: decided. Coverage row: none yet.
- Revision 1 (25 Nov, his pick A): a man turns only for his routine glance (a rhythm the player can watch), a footstep inside his hearing, or other eyes; "turned at the last moment" removed. Simulator: a careful takedown from a dark doorway works 99.6%, on an unlit street 86%, under a lamp 19% (54% held back), by day 7% (leads).
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12, G11, G14, G19.

### 1.4.4 Give-aways and the coat

- How it works: What makes him easier to know: running, the same coat as last night, blood (until washed with water in private), dirt, a weapon in the hand, wrong clothes for the door, bruises, a holdall, the car, a mask. A mask goes through the same witness rules (his ruling of 25 Nov, advisor 378): whoever sold it remembers, and worn in the street it is noticed. The coat buys doubt about the face and none about the car: a deed from the car always names the car. He can shed a slot against witnesses who have not told yet: change the coat, use the second car or respray, a cap and scarf at night or a barber for a week, walk apart from Ron, get rid of the weapon; what gossip has carried is never undone.
- Standard: ER-EYES-10: each give-away raises what a witness catches; a deed from the car always names the car Test: S: golden rows, one per give-away
- Source: DESIGN §2 (DECIDED by the design proof, for him to overturn); the mask: his ruling of 25 Nov (advisor 378). Designed in: DESIGN §2 'What gives him away', ER-EYES-10; DESIGN-ADDENDUM A21; GTAVI-MAP GV-02; DESCRIPTION-COPY-2 §7
- Status: decided. Coverage row: 1.4.4. Conflicts settled: C-020.
- Prior research: coverage audits of Hitman, KCD2 and RDR2 (research-2 sheet): disguise fools strangers, never people who know him; a new coat does not beat someone who knows him; coat, not face, is what RDR2 recognises.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-02 a witness who caught a mark but not Frank links him only while he wears it; decided, thin. None measured.
- Studies: aaa-studies/PLAYERS-STORIES.md: STORY-04 a third of moments turn on a mark a witness connected; decided. None measured.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-04 blood and dirt come from deeds, never walking or rain alone, and are noticed; decided; IM-05 a coat seen at a deed stays recognised until he changes coat; washing clears blood only; decided. None measured.
- Data (run 5): exact values in production/lane/blueprint/data/tune.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G11, G03.

### 1.4.5 Reaching the witness

- How it works: A witness who means to tell sets off, to a friend, a phone box or the station, and is seen going; when the walk starts in Frank's sight it lasts at least 30 real seconds (50% longer with the assist). 'Oi!' stops her for about 2 s and turns her round; then he can talk her round, pay, threaten, help or let her go. A threat can stop a report to the police, never the street's talk; a paid witness remembers being paid. A phone-box call brings a constable that night and the statement is signed at the station at nine next morning, until which Frank can still reach her.
- Standard: The walk lasts at least 30 real s when it starts in Frank's sight (ER-EYES-04); a threat stops a report, never the talk (ruling 3 Oct) Test: S: walk timed; H: 'did you get to her first?'
- Source: DESIGN §2; ruling 3 Oct (his ruling or canon). Designed in: DESIGN §2 'The walk', ER-EYES-04; DESCRIPTION-COPY-2 §16, §8; RULINGS 3 Oct; DEFINITIONS RT2-19
- Status: ruled (his ruling or canon). Coverage row: 1.4.5.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-05 police know only what a person perceived or a search found; decided. None measured.

### 1.4.6 Seeing assist

- How it works: An optional outline of the people Frank can see who are facing him. It is off by default, an assist that changes only its own thing, and never shows a figure he could not see or what anyone knows. It is not a meter.
- Standard: Never a figure he could not see, never what they know (ER-SCREEN-01) Test: S: screen inventory with the assist on
- Source: DESIGN §2, §17 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2, §17 ER-SCREEN-01; DESCRIPTION-COPY-2 §3 (What the screen does show)
- Status: decided. Coverage row: 1.4.6.

### 1.4.7 Street manners

- How it works: Street manners sit on one key (M), picked by the stick: a nod, a greeting, a hard look, a shove, and a call ('Oi!') that stops a walker for about 2 s and turns him round. Each is an act with the seven slots, answered in body or voice within 1 s and remembered like any act. A greeting raises nothing; a hard look and a shove are rungs 1 and 4.
- Standard: Answered in body or voice within 1 s; each is an act with the seven slots (canon moat) Test: S: each gesture answered within 1 s and remembered; addendum rules ER-MANNER-01
- Source: canon; DESIGN §7 lower rungs (his ruling or canon). Designed in: DESIGN-ADDENDUM A10 (ER-MANNER-01); DESCRIPTION-COPY-2 §8
- Status: ruled (his ruling or canon). Coverage row: 1.4.7.
- Studies: aaa-studies/TALK-AS-PLAY.md: TALK-06 every person answers a street manner within 1 s (ruled, though the study says measured). None measured.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G01.

### 1.4.8 Drawing a watcher away

- How it works: A thrown stone or a rattled bin makes a noise at its reach; a watcher inside it turns his head or walks to look, and remembers there was a noise. Watchers have four states: calm (glances round now and then), uneasy (heard something: turns, looks, walks to look), alert (knows someone is there: searches the likely places, calls out) and engaged; he settles back to calm after about a minute. A rattled bin moves the beat constable off his round and he rejoins it where he left. A yard dog barks at a stranger and a scrap of food quiets it; no verb harms any animal (dogs, pigeons, gulls). No meters: alertness reads in heads, posture and voice.
- Standard: Uses the sound reach rule (1.4.3); a watcher drawn away remembers the noise; back to calm about 60 s after. Test: S: a noise inside reach turns a head; outside reach does nothing; no verb harms an animal
- Source: DESIGN §2 (DECIDED by the design proof); alertness states and animals DECIDED by the combat pass 25 Nov, ready for review (COMBAT-SYSTEM.md CS-12, CS-28), for him to overturn
- Status: decided. Coverage row: 1.4.8.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12.

## 1.5 Chases

On foot and by car; every chase ends, caught or lost.


### 1.5.1 Fleeing on foot

- How it works: Run from a constable and it is a chase through the Hook's back ways: ginnels, yards, bollarded lanes a car cannot follow, six vault places. There is no timer. It is lost once the constable has not seen Frank for 7 s, or the gap is over 70 m while he is out of sight (70 m applies on foot; a car chase uses 200 m), and otherwise ends caught, wrecked or at the soft edge. A good bot's foot chase has a median of 30 to 90 s (the ginnel and a street). Frank runs 5.5 m/s, a constable 5.2 and vaults in 1.2 s against Frank's 0.8. After losing him the constable searches the last-seen streets for 30 to 120 real s; seen inside it, the same chase resumes. By his ruling of 24 Nov (R1) a chase runs 1 to 3 minutes, rich in lanes and yards.
- Standard: Lost once unseen for 7 s or 70 m (DESIGN §8); No chase ends while the pursuer can see Frank, except caught, wrecked or at the soft edge; lost car chase median 60 to 120 s, 90th percentile under 240 s; foot chase median 30 to 90 s; none past 240 s (design pass 4, DP5-C01 to C03); feel to be measured in reference games; By his ruling of 24 Nov (R1) chases run 1 to 3 minutes, rich in lanes and yards; the bot bands above are the checks and are to be set against it. Test: S: 50 seeded chases, chase and search lengths logged (DP5-C01 to C03); H: 'how did you lose him?'
- Source: DESIGN §8; advisor 256; chase length: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R1) (waits on a dated study). Designed in: DEFINITIONS design pass 4 C-01 to C-03 and Run 5 second pass; design pass 3 F03, G1, G4; DESIGN s.8
- Status: pending. Coverage row: 1.5.1. Conflicts settled: C-021, C-022, C-276.
- Lead, not solid (STATUS.md on wip, 25 Nov; SLEEPING-DOGS-FOOT-CHASE-2026-11-25.md, two of five samples): Sleeping Dogs' foot chases ran 96 s (a scripted opening run, ends in capture) and 67 s (the Night Market, the runner held 12 to 16 m ahead); its loss rule is a gap held, not sight alone: a 20 s countdown starts once the gap passes about 43 to 45 m (read from our own drill, one run), and whether closing the gap stops it is unread. LEDGER's 7 s unseen or 70 m rule stands; this is a lead for the keeper to weigh (C-504). Status stays pending.
- Deciding row (DECIDES-CHECK, 24 Nov): chases on foot (C1 to C8) decide where the ginnels, yards and six vault places go, by whether chases are won by breaking sight or by outrunning; none sampled yet; three games planned, about 4 h.
- Measuring update (STATUS.md on wip, 25 Nov evening): L.A. Noire 5 of 5 (about 52, 58, 21, 54, 60 s, median about 54 s; one channel, Nov 2017 uploads, every chase a scripted catch), its review found it not solid and STATUS now calls the length "solid with notes" with no escape rule; Sleeping Dogs 5 of 5 (about 96, 67, 14, 66, 72 s, median about 67 s), not solid (edges for four samples and the loss rule still open). The keeper keeps the part pending until STATUS marks a figure solid outright (standing rule a). Both medians sit inside the 30 to 90 s bot band; L.A. Noire's is under his 1 to 3 minutes, Sleeping Dogs' just over a minute (R22). His decision 22 (25 Nov): no set roof routes in chases.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G11.

### 1.5.2 Pursuing on foot

- How it works: Somebody runs from Frank: a runner fare, a man from a fight, a witness heading for the phone. He runs at Frank's run speed less about 5% (5.2 against 5.5 m/s) by the routes of his own routine. From 10 m behind a runner on a straight Frank closes in about 33 s; a gap over about 25 m is closed only by a better line. A hand on the collar from within 1 m behind, then let go, talk or the lower rungs; breaking sight for 7 s or 70 m loses him and he goes home or to a friend. As with every chase there is no timer; a foot chase is a median of 30 to 90 s.
- Standard: none yet: catch-up speeds and give-up rules to be measured Test: S: a runner can be caught by a direct line and lost by a slow one; no timer, foot chase median 30 to 90 s (DP5-C02); addendum rules ER-PURSUE-01 to 02
- Source: DESIGN §5 runner wrinkle, §7 'someone runs' (waits on a dated study). Designed in: DESIGN-ADDENDUM A3 (ER-PURSUE-01, -02); DEFINITIONS design pass 4 C-01, C-02; design pass 3 G4
- Status: pending. Coverage row: 1.5.2. Conflicts settled: C-023.
- Deciding row (DECIDES-CHECK, 24 Nov): read with 1.5.1 (chases on foot, three games planned, about 4 h); the runner's speed rests on Frank's run; Sleeping Dogs' sprint (5.5 m/s) is solid in one game, Frank's run is a design figure (C-267).

### 1.5.3 Car chases

- How it works: A hit-and-run seen by an officer, a refused stop or a car that saw the deed starts a chase with the patrol car's bell and lights. There is no timer: it ends lost, caught, wrecked or at the soft edge. A car chase is lost by 7 s unseen or a gap over 200 m while unseen, never by distance driven alone. A good-driver bot's lost car chase has a median of 60 to 120 s and a 90th percentile under 240 s; none passes 4 real minutes. The drivable loop is 1,528 m, a lap in 76 to 96 s. Caught is a stop or an arrest, never a game over, and nobody shoots from a moving car. By his ruling of 24 Nov (R1) a chase runs 1 to 3 minutes, rich in lanes and yards.
- Standard: Refusing a stop is a chase that ends caught or lost (DESIGN §5); ER-DRIVE-10; No chase ends while the pursuer can see Frank, except caught, wrecked or at the soft edge; lost car chase median 60 to 120 s, 90th percentile under 240 s; foot chase median 30 to 90 s; none past 240 s (design pass 4, DP5-C01 to C03); By his ruling of 24 Nov (R1) chases run 1 to 3 minutes, rich in lanes and yards; the bot bands above are the checks and are to be set against it. Test: S: 50 seeded chases, chase and search lengths logged (DP5-C01 to C03); lost by breaking sight
- Source: DESIGN §5, §8; chase length: his ruling of 24 Nov (RULINGS on wip, his decisions page) (R1) (waits on a dated study). Designed in: DEFINITIONS design pass 4 C-01, C-02, Run 5 second pass 'Can the Hook and the docks hold the measured chases?'; design pass 3 F03, G1, G3; DESIGN s.5 Reality check (CHECK A98, A94, E06): 1,528 m with a 76 to 96 s lap gives 16 to 20 m/s against FIT-G2's 27 m/s (C-395); the loop length is our own, and the loss rule (7 s, 200 m) and search length are carried from the prototype, owed from reference footage.
- Status: pending. Coverage row: 1.5.3. Conflicts settled: C-024, C-025, C-026, C-276.

### 1.5.4 Pursuers

- How it works: A constable announces himself (footsteps, a torch, a cough) at least 3 s before he can challenge, and calls out first. He walks his beat at 1.1 m/s, runs 5.2 m/s, never sees through a wall, never knows where Frank went without seeing, and never catches by a speed Frank cannot match on a straight. The patrol car is no faster than Frank's car. He gives up only when sight is broken (7 s unseen, or the gap over 200 m by car or 70 m on foot): no chase ends while he can see Frank. After that he searches the last-seen streets for 30 to 120 real s, lamp on the turnings, then waits on that road for the night; seeing Frank inside the search resumes the same chase, after it starts a new one.
- Standard: Police announce themselves 3 s before a challenge (ER-POL-02); give up when sight is broken per 1.5.1 Test: S: pursuer gives up at the rule; never cheats through walls
- Source: DESIGN §8 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN s.8 ER-POL-02; DESCRIPTION-COPY-2 s.18, s.19; DESIGN-ADDENDUM A3, A36; DEFINITIONS design pass 4 C-01, C-03; design pass 3 G2, G4, G5
- Status: decided. Coverage row: 1.5.4. Conflicts settled: C-027.
- Checklist (23 Nov, top twenty no. 19; A14.10, A14.14): missing: pursuers and people must replan when a door shuts or a car blocks a lane, and armed men must not fire without a clear line, with a wall-between test. Gap for the design proof; status unchanged.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G14.

### RT2-22 A foot chase caught by a constable

- How it works: A constable who catches Frank (his hand on the collar) searches as if Frank had stood. Found nothing and no cause beyond running: Frank's name is taken (the constable now knows him) and a word, no arrest. Found a weapon, stolen goods or the envelope, or Frank is wanted on a signed statement, or the constable saw the deed: arrest with that deed's hours. Running is not a crime, but the next challenge by that officer is on cause and he searches without being talked round; seen again the same night or while the deed is hot he calls out and a new chase starts.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-22 Test: B (bot), as written under RT2-22
- Source: design pass 3, RT2-22 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 RT2-22; DESCRIPTION-COPY-2 §18, §19
- Status: decided. Coverage row: RT2-22.

### FIT-G3 A chase at the soft edge

- How it works: One rule for any chase, by car or on foot, that reaches the soft edge: it ends there as lost, the pursuer turns back, and Frank or his car goes out of the Hook and comes back as time passed (30 game minutes out and back, which is 60 real seconds at 120 s a game hour, nothing on screen (recomputed for the 48-minute day, his ruling of 24 Nov)). The patrol waits on that road for the rest of the night, so Frank must come back past it. A plate read within 18 m in light 0.7 or more is noted, and a deed he saw brings a constable to the office next morning at ten. Driving to the edge with no chase offers the six districts by landmark and comes back as time passed. Design pass 4 makes the edge one of the four chase endings (lost, caught, wrecked, edge).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 G3; design pass 4 C-01; FIT-CHECK F34
- Status: decided. Coverage row: FIT-G3. Conflicts settled: C-028, C-272.

### FIT-F03 What the 70 m of a lost chase means

- How it works: A chase is lost when the pursuer has not seen Frank for 7 s, or the gap is over 70 m while Frank is out of sight. For car chases the distance is 200 m, because a car covers 70 m in about 4 s. On foot the gap rarely reaches 70 m in a typical chase, so foot chases are mostly lost by the 7 s. Distance driven alone never loses a chase. Design pass 4 changes only the wording: 'inside 90 s' becomes 'in a typical chase', since no chase has a timer.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 F03; design pass 4 C-01; FIT-CHECK F03
- Status: decided. Coverage row: FIT-F03. Conflicts settled: C-029, C-030, C-504.
- Lead, not solid (STATUS.md on wip, 25 Nov; two of five Sleeping Dogs samples): its foot chase is lost when the gap stays over about 45 m for about 20 s, against LEDGER's 70 m while unseen or 7 s unseen. One game, one drill run; the design's figure is not changed.

### FIT-F04 Chase length against the reference games (GTA IV in Mafia DE's place)

- How it works: A measurement, still open: time police chases in GTA V, RDR2 (lawmen), GTA VI footage (no story) and GTA IV (in Mafia DE's place), from start to caught or lost, to check the chase band against what players expect. The 19-chase sheet already gives leads (most 2 to 8 minutes; shortest escapes about 1 minute; floors at 7 to 67 s steps; long chases over-represented). Design pass 4 has dropped the 90 s limit this measurement was meant to test, so it now tests C-02's band (median 60 to 120 s car, 30 to 90 s foot, 90th percentile under 240 s). Five-sample lengths are due in PC block 1 and the feel block (23 to 27 Nov); the row closes in PC block 4, 26 to 28 Nov, about 2 h.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS design pass 3 F04; design pass 4 'The chase against the chase sheet'; FIT-CHECK F04
- Status: pending. Coverage row: FIT-F04. Conflicts settled: C-031.
- Solid so far (STATUS.md on wip): GTA VI heat at peak two stars, star lit to cleared by car, about 27 to 122 s, median about 47 s (22 Nov, five uncut samples, four from one player); RDR2 wanted lit to cleared by riding off with no lawman close, about 41.5 to 97 s, median about 70.5 s (24 Nov 20:25, five samples, four from one player). These are heat lengths, not chase lengths; foot chases have only the Sleeping Dogs leads (1.5.1).

### DP5-C01 A chase has no timer (car and foot)

- How it works: A chase has no timer, on foot or by car. It ends lost (7 s unseen, or the gap over 200 m by car or 70 m on foot while unseen), caught, wrecked, or at the soft edge, and no chase ends while the pursuer can see Frank except caught, wrecked or at the edge. One patrol car stays, so pressure comes from where he waits and what he knows. The experience rule 'every chase ends within 90 s' becomes 'every chase ends caught, lost, wrecked or at the edge, and none passes 4 real minutes'. No bot's chase may pass 240 s. Decided; his to overturn.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 4 (run 5), the chase Test: B: seeded chase set, lengths logged
- Source: car-chases-sheet-2026-11-21 (leads); g5-heat-samples (SOLID, whole spell); FIT-CHECK F02 to F04, P13 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 4 C-01 and its Standard; car-chases-sheet; g5-heat-samples; FIT-CHECK F02 to F04, P13
- Status: decided. Coverage row: DP5-C01. Conflicts settled: C-032, C-276.
- Ruling 24 Nov (R1): his ruling of 24 Nov (RULINGS on wip, his decisions page): chases run 1 to 3 minutes, rich in lanes and yards; the 4-minute ceiling above is the bots' outer check, to be set against it.
- Deciding row (DECIDES-CHECK, 24 Nov): chases on foot (read with 1.5.1); none sampled; three games planned, about 4 h.

### DP5-C02 Chase length on the Hook's loops

- How it works: On the Hook's loops a good-driver bot's lost car chase has a median of 60 to 120 s and a 90th percentile under 240 s (about two and a half laps of the 1,528 m loop); a foot chase has a median of 30 to 90 s. This is below the sheet's 2 to 8 minutes on purpose: those are uploaders' picks at three stars and more on maps many times the Hook. At chase speed (16 to 20 m/s) 2 minutes cover 1.3 to 1.6 laps and 4 minutes 2.5 to 3.1 laps; past about 3 minutes every road has been driven twice. A bot that drives straight and never breaks sight is caught or reaches an edge, never chased past 4 minutes.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 4 (run 5), the chase Test: B: seeded chase set, lengths logged
- Source: car-chases-sheet-2026-11-21 (leads); g5-heat-samples (SOLID, whole spell); FIT-CHECK F02 to F04, P13 (waits on a dated study). Designed in: DEFINITIONS design pass 4 C-02 and Run 5 second pass; car-chases-sheet; g5-heat-samples
- Status: pending. Coverage row: DP5-C02. Conflicts settled: C-033, C-276.
- Ruling 24 Nov (R1): his ruling of 24 Nov (RULINGS on wip, his decisions page): chases run 1 to 3 minutes, rich in lanes and yards; the median and 90th-percentile bands above are the bots' checks, to be set against it.

### DP5-C03 The search after a chase is lost

- How it works: After a chase is lost the patrol searches the last-seen streets for 30 to 120 real seconds, slowly, lamp on the turnings, then waits on that road for the rest of the night. Seen again inside the search, the same chase resumes with what he already knows; seen after it, a new chase starts. The band is a judgement between the search leads (about 20 s, 50 s, 68 s, once at least 6 minutes) and GTA VI's solid whole wanted spell (about 27 to 122 s, median about 47 s, four of five samples from one player).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 4 (run 5), the chase Test: B: seeded chase set, lengths logged
- Source: car-chases-sheet-2026-11-21 (leads); g5-heat-samples (SOLID, whole spell); FIT-CHECK F02 to F04, P13 (waits on a dated study). Designed in: DEFINITIONS design pass 4 C-03; g5-heat-samples; being-seen sheets
- Status: pending (the reference heat lengths are solid in STATUS.md on wip; the 30 to 120 s band stays a design judgement the bots check, C-505). Coverage row: DP5-C03. Conflicts settled: C-034, C-505.
- Measured 25 Nov (STATUS.md on wip): heat length at peak two stars in GTA VI, median about 47 s (about 27 to 122 s; solid 22 Nov); RDR2 riding off, no lawman close, median about 70.5 s (about 41.5 to 97 s, five samples, video seconds with some map time inside; solid 24 Nov 20:25); a return into sight resumes pursuit at the level held (GTA VI, five samples, solid), as the rule says. Both medians sit inside 30 to 120 s. RDR2's shootout case (about 109 and 513 s) and three stars (about 322 s) stay leads.
- DECIDES-CHECK, 24 Nov: a lead, a 30 to 120 s band the bots check; the GTA VI wanted spell at peak two stars (median about 47 s) stays SOLID in STATUS.md after its star level was re-read by code on 23 Nov 15:33, and still falls inside the band.

### WI-P10 Hiding indoors during a chase

- How it works: A foot pursuer follows Frank through any open door he saw him use; a door Frank shuts unseen is not searched (the lost-chase search of DP5-C03 walks streets for 30 to 120 s and does not try doors); a shop he runs into is a place full of witnesses and the keeper tells the constable. Hiding in a yard or a lane's dark corner works by breaking sight (1.1.5), and the search's lamp finds him only if it lights him.
- Standard: Indoors is searched only where the pursuer saw him go or the search's reach passes. Test: S: chases ending through a seen door, an unseen door, and into a shop.
- Source: 1.1.5; DP5-C03. DECIDED by the what-if sweep 24 Nov (production/lane/blueprint/what-if/PROPOSED-PARTS.md P10, D6) for him to overturn.
- Status: decided. Coverage row: none yet.

## 1.6 Jobs with the hands

The work itself: getting in, searching, taking, fronting up, minding, getting ready, getting rid.


### 1.6.1 Getting in

- How it works: A lock has several keys: a key lent or copied (Ian Megginson knows every lock on the street), a back way a routine leaves open, or force, which is loud, shows on the door for a day and is a crime. No lockpicking game. In a private place the owner or a neighbour warns, warns again, then calls someone or acts, within half a minute at worst; the warnings reset and the sighting is kept for good. Forbidden places skip the first warning.
- Standard: Several keys to every lock; force is loud, shows for a day and is a crime; a challenge warns twice then acts within half a minute (lead) Test: S: a room entered three ways; force heard at its reach
- Source: DESIGN §4 Break-ins (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §4 Break-ins; DESCRIPTION-COPY-2 §8, §13
- Status: decided. Coverage row: 1.6.1.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G14, G12.

### 1.6.2 Searching and taking

- How it works: No search minigame. Search times are a drawer 2 s, a desk 4 s, a wardrobe 5 s; a safe needs its key or combination from a person. Searching makes noise (a drawer about 2 m, a forced cupboard about 10 m at night); in a dark room it takes twice as long without a torch. What is found is authored per job; taking is one press and what is taken can be found on him. Anyone down, out or dead can be searched in a few seconds, seen like any act, and carries what fits their role (his ruling of 25 Nov, advisors 376, 377): a constable's truncheon, cuffs, whistle, radio (police traffic is heard while Frank holds it) and pocketbook (the day's names and descriptions). Stolen police kit raises the police response (2.6.10).
- Standard: none yet for times: search time per container and the noise of searching to be set. Pass: anyone down, out or dead can be searched and yields only what fits his role. Test: S: every container and every downed person searchable, each search timed and heard at its reach; addendum rules ER-SEARCH-01 to 02
- Source: DESIGN §4 (no numbers) (no reference figure yet); his ruling of 25 Nov (advisors 376, 377) for who can be searched and what they carry. Designed in: DESIGN-ADDENDUM A4 (ER-SEARCH-01, -02), A33; DESCRIPTION-COPY-2 §9
- Status: ruled (who can be searched and what they carry: his ruling of 25 Nov, advisors 376, 377); search times unmeasured. Coverage row: 1.6.2. Conflicts settled: C-502.
- Checklist (23 Nov, top twenty no. 8; A36.02): missing: taking something must say what was taken, on screen or in Frank's words; the design describes no feedback. Gap for the design proof; status unchanged.
- Data (run 5): exact values in production/lane/blueprint/data/rooms.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G03, G11, G14.

### 1.6.3 Lifts and the hot mark

- How it works: Goods carry a hot mark that fades with value and distance, and the owner never forgets them: he recognises his own goods in a shop window. Rita's back room fences from rung 2, refuses or lowballs hot goods, and Wayne's pawn takes goods too. A haggle is three offers at most; the buyer's answers come from his purse, how hot the goods are and how he regards Frank. Notes from a till are hot for a week. Buyback is in (his ruling of 24 Nov): goods sold or pawned can be bought back within 7 game days at the price plus a quarter; fences hold nothing. The fence's rate is about a third of retail (0.33; 0.2 for jewellery up to 0.4 for a video recorder), from the 1990 research (CLOUD-FIGURES B3).
- Standard: Hot mark fades with value and distance; owner never forgets; fence about 0.33 of retail (CLOUD-FIGURES B3) Test: S: golden rows for the mark; the owner recognises the goods
- Source: DESIGN §4 Lifts (no reference figure yet); buyback: his ruling of 24 Nov (RULINGS on wip, his decisions page). Designed in: DESIGN §4 Lifts; DESCRIPTION-COPY-2 §14; DESIGN-ADDENDUM A41; CLOUD-FIGURES B3
- Status: unmeasured. Coverage row: 1.6.3. Conflicts settled: C-035.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-05 every buyer has a weekly purse; a refusal or part-payment in the last two weeks; decided. None measured.
- Data (run 5): the data sweep (class B) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13.

### 1.6.4 Fronting up

- How it works: Mickey's debt book has five debts: Darren Milner £22 (pays in what he hears), Wayne Harrison £30 (in goods from the pawn's back room), Lee Drewery £15 (stands, with the docks behind him), Julie Kettlewell £9 (cannot pay) and Dennis Iveson £80 (has the money, a yard and a yard hand). A debtor pays what his purse holds and the rest stays on the book; squeezing or letting go is told on the street. Every pressure has three answers and none ends the game; threats sit at rung 3.
- Standard: Every pressure has three answers (ER-RIV-03); a debtor pays what the purse holds; squeezing or letting go is told on the street Test: S: each debtor's outcomes scripted; H: 'did the five debts feel different?'
- Source: DESIGN §4 Collections (no reference figure yet). Designed in: DESIGN §4 Collections; DESIGN §13 ER-RIV-03; DESCRIPTION-COPY-2 §9
- Status: unmeasured. Coverage row: 1.6.4.

### 1.6.5 Minding and waiting

- How it works: Stand at someone's door, sit in the car, be seen at someone's shoulder. The town records who stood with whom ('Frank and Ron were at the gate' is a sighting), and what minding pays is set in each job. Escorting someone out of danger is minding. Frank on the wall opposite with a cigarette is caught no more than walking. Watching and waiting is under 10% of play (aim 3%).
- Standard: Waiting under 10% of play (ER-CORE-06); watching and waiting 3% of the hour budget (DESIGN, judgement) Test: H: waiting share; S: minding recorded as 'stood with'
- Source: DESIGN §1, §4 (no reference figure yet). Designed in: DESIGN §4 Minding; DESCRIPTION-COPY-2 §13, §8, §34
- Status: unmeasured. Coverage row: 1.6.5.

### 1.6.6 Getting ready

- How it works: At dusk at the office: the dark coat goes on with one key; two things under the coat (a weapon, the envelope, a key, a tool, the torch), one thing in the hand or a holdall, which car, who comes. The rest stays at the office: a locked drawer, the yard shed and the tin. It takes a minute and never a screen. The boot of the cab can hold what is not on him.
- Standard: Two things under the coat; one key for the coat; a minute at most Test: S: loadout limits; H: time spent getting ready
- Source: DESIGN §6, §7 Weapons (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §22; DESIGN §6, §7 Weapons; DESIGN-ADDENDUM A5; GTAVI-MAP GV-01
- Status: unmeasured. Coverage row: 1.6.6.

### 1.6.7 Getting rid of things

- How it works: Weapons can be dropped down a drain; a bag thrown in the dock is gone and remembered by anyone who saw; blood comes off with water and privacy, or at the launderette, which washes the coat and plants a witness. A body can be moved by Frank (dragged at 0.9 m/s, into a boot in 4 s, off the quay edge in 3 s) or by a sent man; a body is never wiped, and one sunk is never found.
- Standard: Blood until washed with water and privacy; the launderette washes a coat and remembers it; a body is never wiped Test: S: washing clears the give-away and plants a witness at the launderette
- Source: DESIGN §2, §7 (DECIDED by the design proof, for him to overturn). Designed in: DESCRIPTION-COPY-2 §22, §9, §7; DESIGN §2, §7, §12; DEFINITIONS RT2-11
- Status: decided. Coverage row: 1.6.7.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-03 a daily act holds control at most 10 s the first time, 5 after; decided; IM-04 blood and dirt come from deeds, never walking or rain alone, and are noticed; decided. None measured.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-05 a coat seen at a deed stays recognised until he changes coat; washing clears blood only; decided. None measured.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13.

### 1.6.8 Using the world

- How it works: Every object a job or story needs is used with the one use key and a prompt naming it (a drawer, the kettle, the radio, the fare book, the tin, a phone box, a bench). The prompt is held 0.2 s before it changes; when two things share a key one prompt asks which, and a person with something to say is offered before a door. A walk-up sweep finds no usable thing without a prompt, and pressing the key 500 times in crowded spots never fires the wrong action.
- Standard: A prompt names what is ahead and in view, held 0.2 s; everything usable has a prompt (ER-INPUT-02) Test: H: walk-up sweep with no prompt faults
- Source: DESIGN §17 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §17 ER-INPUT-02; DESCRIPTION-COPY-2 §6, §3; GTAVI-MAP Y1.8
- Status: decided. Coverage row: 1.6.8.
- Data (run 5): exact values in production/lane/blueprint/data/ui-text.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.

### 1.6.9 Coat, pockets and office storage

- How it works: Two things under the coat (a weapon, the envelope, a key, a tool, the torch) and one in the hand or a holdall; the rest lives at the office in a locked drawer, the yard shed and the tin. A constable's search finds what is under the coat and in the hand; an office search finds what is stored there; what is stored survives save, load and skipped time. The Ledger's Open list says in words what he carries. The cab's boot also holds the envelope, a spare coat or a box.
- Standard: Two things under the coat; the rest at the office; found in a search (ruling 23 Sep: coat, pockets, cab-office storage) Test: S: a search finds what is carried; office storage keeps across saves; addendum rules ER-POCKET-01 to 02
- Source: ruling 23 Sep genre line; DESIGN §7 (his ruling or canon). Designed in: DESIGN-ADDENDUM A5 (ER-POCKET-01, -02); RULINGS 23 Sep genre line; GTAVI-MAP GV-01
- Status: ruled (his ruling or canon). Coverage row: 1.6.9.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13, G10.

### 1.6.10 Frank's wardrobe

- How it works: Three outfits across the game (as he arrived, a decent jacket, a good overcoat) plus a dark coat for nights, each changing how strangers speak to him and which doors open. A second coat bought after a deed breaks the mark rung for witnesses who saw the first and have not yet told anyone (GV-02); what gossip has carried is never undone; a barber changes the look for a week; a scarf up and a hat down at night break the face rung but are a mark by day. Prices: second-hand coat £15, decent jacket £45, good overcoat £90, barber £4 (to be checked against 1990 sources). Clothes are his to approve in the game's camera.
- Standard: Three outfits across the game each changing how strangers speak and which doors open (DESIGN §14); his to approve in the game's camera Test: S: a change of coat lowers a witness's mark rung; H: strangers greet differently; addendum rules ER-COAT-01
- Source: DESIGN §14; rulings 29 Sep, 3 Oct (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §14; DESIGN-ADDENDUM A21; DESCRIPTION-COPY-2 §26; DEFINITIONS pass 3 §G8; RULINGS 29 Sep, 3 Oct (clothes)
- Status: decided. Coverage row: 1.6.10.
- Studies: aaa-studies/MEMORY-SYSTEMS.md: MEM-02 a witness who caught a mark but not Frank links him only while he wears it; decided, thin. None measured.
- Studies: aaa-studies/FAILURE-AND-FRUSTRATION.md: FF-08 a forced-failure bot still finds jobs, rent and two brakes it can act on (talk it down, buy it quiet, a favour) the next week of Act II; decided. None measured.
- Studies: aaa-studies/IMMERSION-FEATURES.md: IM-02 every daily act pays in the town; decided; IM-05 a coat seen at a deed stays recognised until he changes coat; washing clears blood only; decided. None measured.
- Studies: aaa-studies/MONEY-AND-PROGRESSION.md: MP-07 no purchase raises a fighting, driving or speaking value; decided. None measured.
- Data (run 5): the data sweep (class C) sends its exact figures to the economy job: production/lane/blueprint/economy/ECONOMY-DESIGN-2026-11-26.md (see the Economy lines).
- Rules (question passes, 25 Nov; BLUEPRINT-12): G11.

### 1.6.11 Casing a place

- How it works: Casing is a tail on a place: standing a while across the street or sitting in a parked car learns its hours, who holds the key and which way is left open, each written in the Ledger as Frank sees it and matching the town's real routines. It is done close, which is its risk. Hours are windows, not minutes.
- Standard: What is learned goes in the Ledger as a sourced line (ER-LEDG-01); windows, not minutes (DESIGN §4) Test: S: a cased place's hours appear in the Ledger and match the routines; addendum rules ER-CASE-01
- Source: DESIGN §4, §10 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A23; DESCRIPTION-COPY-2 §13; DESIGN §4, §10 ER-LEDG-01
- Status: decided. Coverage row: 1.6.11.
- Studies: aaa-studies/MISSIONS-AND-SIDE-QUESTS.md: MS-02 a planned job's three keys leave at least two different traces; decided. None measured.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G12, G13, G23.

### 1.6.12 A torch on a night job

- How it works: A torch (about £4 at the ironmonger) takes one of the two pockets and is worked with I. Switched on it lights a short cone: a search in a dark room takes its table time with it and twice as long without. A lit torch makes Frank count as lit at 0.7 to anyone with a line of sight to him or the beam, and a beam moving behind a window shows from the street as a precursor. Off, it is a thing in a pocket a constable may find.
- Standard: rule: In the same dark room, a search with the torch takes the table time and without it twice that; a watcher outside the window catches the beam as a precursor only when the torch is on (golden rows). Test: In the same dark room, a search with the torch takes the table time and without it twice that; a watcher outside the window catches the beam as a precursor only when the torch is on (golden rows).
- Source: DESIGN-ADDENDUM-2026-11-20 A33 (from REFERENCE-MECHANICS-2026-11-20 M1.101) (reference game). Designed in: DESIGN-ADDENDUM A33, A4; DESCRIPTION-COPY-2 §3 (Controls); DEFINITIONS pass 3 §G8
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 1.6.12.
- Story needs (paper, 24 Nov): the old man's torch as an object carrying the claim to the landing (Frank's deeds carried S46, S61). Partly covered: the part is a torch on a night job; a torch that carries a claim is missing.

### 1.6.13 Lifting from a pocket

- How it works: Beside or behind a person in a crowd, a queue or a packed caff, one held press of about 2 s takes the one thing worth taking (a key, a letter, a wallet). Whether he feels it follows fixed limits, never a roll: an attentive man, good light or fewer than three people near means he feels it; a distracted man in a crowd of three or more in poor light does not. His head turns before he feels it and Frank can stop. Felt, it is a deed with the seven slots and he turns on Frank; a lifted key is missed by morning and he suspects only people he noticed near him.
- Standard: rule: A lift on an attentive person, in good light or with fewer than three people near, is always felt; one on a distracted person in a crowd of three or more in poor light is never felt; his head turns before any felt lift; a lifted key is missed by the next morning and suspicion falls only on people he noticed (golden rows). Test: A lift on an attentive person, in good light or with fewer than three people near, is always felt; one on a distracted person in a crowd of three or more in poor light is never felt; his head turns before any felt lift; a lifted key is missed by the next morning and suspicion falls only on people he noticed (golden rows).
- Source: DESIGN-ADDENDUM-2026-11-20 A34 (from REFERENCE-MECHANICS-2026-11-20 M1.97) (reference game). Designed in: DESIGN-ADDENDUM A34; DESCRIPTION-COPY-2 §14
- Status: pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 1.6.13.
- Planting (his decision 12, 25 Nov; rule G13): the same held press puts a small thing into a pocket, coat or bag under the same limits; what is planted keeps its owner and how it moved, and found later it traces by G13. CS-29's old line against it is struck (C-541).
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13.

### WI-P05 Mugging and shoplifting

- How it works: Beating a man and searching him for his money (1.6.2, a man down can be searched) is a robbery at any rung: 12 hours if arrested, Ellis up one stage, the man a witness at face distance. A threat with a weapon to make a man hand over is a robbery of a person and possible from the start (his ruling of 25 Nov, advisor 378): his temper decides whether he hands over, runs or fights; it is witnessed, reported, remembered, with consequences from the systems and never caps (C-431). Shops in 1990 Quay Street keep most stock behind the counter (newsagent, tobacconist, chandler) or under the keeper's eye (grocer, ironmonger); taking from a shelf is a lift (1.6.13) with the keeper as the person who may feel it, by the same fixed limits. Felt, he says so to Frank's face, will not serve him for a game week and tells his own people; unfelt, the loss is found at closing and suspected of whoever he noticed. Stock taken is hot goods (1.6.3).
- Standard: A beating and search for money is a robbery at any rung; a weapon hold-up of a person is open from the start with consequences by temper; a shelf lift follows the lift rule with the keeper watching. Test: S: a mugging in Act I logged as robbery; a shelf lift in good light with the keeper attentive is felt.
- Source: 1.6.13; 1.6.3; his ruling of 25 Nov (advisor 378: robbery a general action, anyone, anywhere, from the start). DECIDED by the what-if sweep 24 Nov (production/lane/blueprint/what-if/PROPOSED-PARTS.md P05, D6) for him to overturn; its keeping 1.6.15's gate is replaced by the ruling.
- Status: decided. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13.

### 1.6.14 Damage by hand

- How it works: A job or pressure can ask Frank to break a window, windscreen, van light or shop sign himself. It is a loud act heard at the force reach, the damage stays until mended, and the owner reads it as a message from whoever he suspects and knows by morning. It climbs a rival's ladder if aimed at his; sending men to do it is the sent verb. Frank may also set fire to a building at any time (his ruling of 25 Nov, advisors 374, 375): a fire can kill, and a death by fire is a killing to the town and the police like any other (2.16), within canon's content rule.
- Standard: rule: Every damage act is heard at the force reach, leaves a mark that stays until mended, and is known to its owner by morning. Check S. Test: Every damage act is heard at the force reach, leaves a mark that stays until mended, and is known to its owner by morning. Check S.
- Source: DESIGN-ADDENDUM-2026-11-20 A35 (from REFERENCE-MECHANICS-2026-11-20 M3.13) (reference game); fire: his ruling of 25 Nov (advisors 374, 375). Designed in: DESIGN-ADDENDUM A35; DESCRIPTION-COPY-2 §22
- Status: ruled (fire: his ruling of 25 Nov); the rest pending (a reference-game lead; measured only when STATUS.md marks it solid). Coverage row: 1.6.14. Conflicts settled: C-503.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G18, G19, G07, G13.

### 1.6.15 Hold-ups of shops and people

- How it works: Robbery is a general action: Frank can hold up anyone, anywhere, from the first hour, a till, a purse or a person in the street. No rung, dial state, Act or weekly quota stands in front of it, and no list of places or people limits it, except canon's content rule (no children anywhere). The bank is a soft-edge place with no walked interior; whether it can be robbed waits on Q21 (C-432). The take is what the till or purse holds that hour. A mask goes through the witness rules: whoever sold it remembers the sale, and worn in the street it is noticed (1.4.4). The consequences come from the systems and are never capped by this part: witnesses at face distance, the report or the telling, the police and the case (a robbery, 12 hours if taken), talk that cools in about a week, the shop's fear and takings. Never a game over.
- Standard: Pass: a hold-up can be tried on any adult in any place from the first hour, and the code holds no rung, dial, Act, per-street, per-week or per-place limit; every one is witnessed at face distance, reported or told within a game hour, and remembered through the witness rules; the take never above what the till or purse held and balanced in the flows ledger; nobody under the content rule; Frank in control within 2 real minutes with a Ledger line. Test: S: seeded hold-ups in the first hour and late, on a shop, a person and a home, the chain printed; a read of the code finds no gate.
- Source: His ruling of 25 Nov (advisor 378: robbery a general action, anyone, anywhere, from the start; masks through the witness rules; consequences from the systems, never caps; the people pass checks the economy), which replaces his ruling of 20 Nov (rare and late, only through the dial) and the gates of DESIGN-ADDENDUM A41; RULINGS on wip. Designed in: DESIGN-ADDENDUM A41 (the consequence chain only).
- Status: ruled (his ruling of 25 Nov, advisor 378). Conflicts settled: C-275, C-500. Coverage row: none yet (no parts-tree part or coverage.json row; asked of the design proof in BLUEPRINT-11).
- Economy (24 Nov, section 5.5): A hold-up pays what the till holds that hour (about £90, a small shop's day), loud, witnessed, 2 case points. The shop is afraid for weeks: takings fall a tenth and recover as the fear fades. Judgement.
- Data (run 5): exact values in production/lane/blueprint/data/places.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G08, G11, G20, G21.

### WI-P12 Trying a crime early, and the bank

- How it works: No input is refused on screen. A weapon drawn at a counter in hour one is a robbery attempt like any other (his ruling of 25 Nov, advisor 378: robbery from the start, anyone, anywhere); the keeper's temper decides: most step back from the till and shout, one with nerve reaches for the phone, a frightened one hands over. It is witnessed and reported as a robbery (12 hours if arrested), Ellis rises a stage, and the shop refuses him; consequences come from the systems, never from caps (C-431). The bank sits in the Exchange (soft edge, not walked), its camera the town's only CCTV (his ruling of 24 Nov); it cannot be robbed in the release (out of scope, D7: a bank job would need the map to grow).
- Standard: No input is refused; an early attempt has a real outcome by temper. Test: S: a weapon drawn at the grocer's counter in hour one; outcome logged and the town's reading checked against 1.6.15's witnessed-and-told rule.
- Source: 1.6.15; canon (CCTV at the bank); RT-09; his ruling of 25 Nov (advisor 378). DECIDED by the what-if sweep 24 Nov (production/lane/blueprint/what-if/PROPOSED-PARTS.md P12, D6 and D7) for him to overturn: the bank out of scope is a scope call (see revisit).
- Status: decided; the bank out of scope. Coverage row: none yet.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G21.

### RT2-19 The phone as a verb

- How it works: Phones are the office's (the desk phone and Pauline's line), three phone boxes (by the landing, at the parade's north end, at the dock gate) and some homes' own. A box call costs 10p; 999 is free and an anonymous call brings a constable to the spot that night but never makes an arrest alone. Numbers are Ledger facts, got from a card, being told, the real book, or the directory in the box for businesses. A rival head can be rung only once Frank has the number. Calls are talk and stop the clock as talk does. The office answering machine takes messages and each goes into the Ledger; Garbutt carries a pager and rings a box back within half a game hour; Frank never carries a pager.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-19 Test: B (bot), as written under RT2-19
- Source: design pass 3, RT2-19 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 RT2-19; DESCRIPTION-COPY-2 §16
- Status: decided. Coverage row: RT2-19.
- Prep: INVENTORY section 2: 3 phone boxes needed (the prototype has 1 in map.js), 0.2 hour if made in the one-shot.
- Data (run 5): exact values in production/lane/blueprint/data/map.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class B.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G03, G01, G19, G20, G04.

## 1.7 Running the crew

Frank's power is people: orders in the field, sending in Act II, the board.


### 1.7.1 Orders in the field

- How it works: Orders take two inputs at most (a digit, then a target): with me; wait here; watch that; fetch him; take this there; drive; lean on him. Each is answered in voice or body within 1 s, and a man who cannot do it says why. Crew never block a door or a lane and never do what cannot be undone unless told.
- Standard: Two inputs at most, answered in voice or body within 1 s; a man who cannot says why (ER-CREW-01); crew never block a door (ER-CREW-02) Test: S: each order; B: crew never block a lane
- Source: DESIGN §12 (no reference figure yet). Designed in: DESIGN §12 ER-CREW-01, -02, -04; DESCRIPTION-COPY-2 §22
- Status: unmeasured. Coverage row: 1.7.1.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G07.

### 1.7.2 Sending (the eight verbs)

- How it works: From Act II, eight verbs, each through a named man: hurt, plan, frame, lean on a witness, move or hide a body, dock or beat one of his own, hit a rival's property, vouch. A send is two inputs, the verb then a target from the Ledger; the man does it on the next night his routine allows, decided by his nerve against the target's, the watchers, light and noise. Every send resolves within two game nights, Frank learns the morning after from the man's own line, and the result runs the same perception and memory as his own deed. A beating is never shown at length, and each send leaves a chain the town can trace.
- Standard: Each through a named person; an order given and a line written; a beating never shown at length (DESIGN §12; canon no cruelty as spectacle) Test: S: each verb leaves a chain the town can trace; accomplice knows
- Source: D56; DESIGN §12 (his ruling or canon). Designed in: DESIGN §12 Orders; DESCRIPTION-COPY-2 §22; DEFINITIONS RT-08, RT-09
- Status: ruled (his ruling or canon). Coverage row: 1.7.2.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G13.

### 1.7.3 The board

- How it works: A chalkboard in the office with a line for each car and driver placed by the last radio call, and the week's fares. It puts a car on a rank or a shift; a car on a rank is the firm's eyes there and can give Frank an alibi or a witness. It takes a minute a day at most, and Pauline runs it if he never touches it. The rank outside Mickey's is his; the ferry rank and a second are won by being there with a car on the board enough days.
- Standard: A minute a day at most; Pauline runs it if he never touches it (DESIGN §12) Test: S: placements change sightings; H: minutes spent at the board
- Source: DESIGN §12 The board (no reference figure yet). Designed in: DESIGN §12 The board; DESCRIPTION-COPY-2 §23
- Status: unmeasured. Coverage row: 1.7.3.
- Data (run 5): exact values in production/lane/blueprint/data/places.json (data build wave 1, 24 Nov, checked by tools/validate_data.py and reviewed; open points in the file and DATA-BUILD-STATUS.md). Data sweep class C.
- Story needs (paper, 24 Nov): the board as a visible score (Danny's name and arrow, or CAMMACK on the unit's shutter) (the story on paper, in KEEPER-LOG). Not covered; the part is a chalkboard of cars and fares only.
- Rules (question passes, 25 Nov; BLUEPRINT-12): G10, G20.

### 1.7.4 Men at his side

- How it works: A man at his side follows at about 2 m, waits at doors, rides in the car and stands in a fight, taking the second man, so two against two is fair. He never blocks a door or lane, never lags more than 10 s and never fails a job by being slow. He is a witness the town sees with Frank ('Frank and Ron were at the gate'); with Ron beside him, the two dockers by car two are a fair fight.
- Standard: A follower keeps up or waits and never fails the job (ER-CREW-02); two against one is deadly both ways (DESIGN §7) Test: B: followers never block; S: a fight with Ron at his side goes as the odds say; addendum rules ER-SIDE-01
- Source: DESIGN §7, §12 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A16 (ER-SIDE-01); DESIGN §12 ER-CREW-02; DESCRIPTION-COPY-2 §22, §9
- Status: decided. Coverage row: 1.7.4.
- Story needs (frame, 24 Nov): Ron at Frank's shoulder on every main job until the turn, and the tester's S5 count of a third of play beside him (SYSTEMS-THE-STORY-NEEDS S47; EMERGENT-MEASURE S5). Partly covered: a man at his side follows and fights; the until-the-turn companion rule is missing.
- Story conflict C-345 (run 5): The part says a man at his side never fails a job and follows and rides, while the story needs Ron to refuse to ride with the gun. Until designed, the part stands; the need is a gap for the design proof.

### RT-08 Sending verbs in play

- How it works: A send is given in talk with the man (or by the board's line for him): two inputs, the verb, then a target from the Ledger (a person or place Frank knows). The man does it on the next night his routine allows; the outcome is the man's nerve against the target's, with the watchers, light and noise. Frank learns it the morning after from the man's own line and later from the town's version. Every send resolves within two game nights and leaves a chain the town can trace; the man knows.
- Standard: Every send resolves within two game nights; its result runs the same perception and memory as a deed by Frank; nothing is shown at length. Test: B: each of the eight verbs sent twenty times with seeds; outcomes traced to watchers.
- Source: The description, section 27. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-08; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: RT-08.
