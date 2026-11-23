# BLUEPRINT 01: What the player does with his hands

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. The verbs: moving, driving, fighting, being seen, chases, jobs, the crew.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 1.1 Moving on foot

Walking the town with the camera: the verb under every other verb.


### 1.1.1 Walk, run and turn

- How it works: Tom walks, runs and turns with weight, like a man in boots on wet cobbles: turning is quick, starting and stopping have a short ease, and running is plainly louder and more noticed than walking. Z held (or a light stick touch) walks slowly and halves the reach of his footsteps; there is no crouch. Every action answers within 100 ms, a press 100 ms early still counts, keyboard movement is eased and mouse look never jumps. Tuning speeds are walk 1.6 m/s, slow walk 0.9, run 5.5, holdall run 5.3.
- Standard: ER-INPUT-01 (every action answers within 100 ms, eased keys, mouse look never jumps); feel numbers (start, stop, turn rate, run speed) to be measured from reference games Test: feel numbers inside measured bands (input probe); H: 'did moving feel heavy or slippery?'; his eye in Unreal
- Source: DESIGN §17 ER-INPUT-01; advisor 256 (waits on a dated study). Designed in: DESCRIPTION-COPY-2 §6 and §3 (Controls); DESIGN §17 ER-INPUT-01; DEFINITIONS pass 3 §G4
- Status: pending. Coverage row: 1.1.1.

### 1.1.2 On-foot camera follow

- How it works: The street camera sits at the Between picture's height with an 86 degree lens, 3.1 m back, so his feet are always in frame and his head is level with the far end of the street. It blends in a second or less: closer in rooms and talk (Tom 1.5 m from the speaker), wider in a fight (both men's feet in at least 90% of frames, about 3.5 to 5.0 m back). It never ends inside a wall, body, car, lamp post, shelter or van; it comes in front of thin things. Shake obeys Reduce motion, and the field of view is a setting of 75 to 100 with 86 the default.
- Standard: Between height, 86 degree lens, 3.1 m back, feet in frame; never inside a wall, body or car (ER-CAM-01, ER-CAM-02); follow lag and turn feel to be measured Test: B soak with clip detector; S frames counted for feet in frame; H screenshots in tight rooms
- Source: ruling 28 Oct (camera); DESIGN §17 (waits on a dated study). Designed in: DESCRIPTION-COPY-2 §6; DESIGN §17 ER-CAM-01/02; RULINGS 28 Oct (camera) and 21 Nov (setting); FEEL-TARGETS-MELEE C10; DEFINITIONS AX-03 and pass 3 header
- Status: pending. Coverage row: 1.1.2. Conflicts settled: C-001.

### 1.1.3 Doors, stairs and thresholds

- How it works: A door opens with the use key and Tom walks through without catching; stairs are walked, not snagged on; a locked door says it is locked. Nothing inside Mickey's holds him against a wall. Doors creak, hit and latch, and a forced door is the loudest thing in a quiet street. From any state he can move on within 5 s by walking, getting out or backing out, or a short in-world reset puts him on clear ground; there is no jump.
- Standard: Never stuck (ER-CORE-01: moves on within 5 s); in or out of a door in under 2 s; no jump (ruling 23 Sep) Test: B: 30 minutes of walking into every door and stair; S: door use timed
- Source: DESIGN §1 ER-CORE-01; ruling 23 Sep (his ruling or canon). Designed in: DESCRIPTION-COPY-2 §6; DESIGN §1 ER-CORE-01; RULINGS 23 Sep genre line (no jump)
- Status: measured. Coverage row: 1.1.3.

### 1.1.4 Carrying

- How it works: A holdall in the hand slows him a little and can be seen; a thing under the coat cannot be seen but is found in a search. What he carries raises what a witness catches ('a man with a holdall on the quay at midnight is a man with a holdall'). Running with a holdall is 5.3 m/s against 5.5 empty, still just faster than a constable. Loads named by the row are the suitcase, holdall, envelope and a box.
- Standard: Found is worse than used (load as a tension source); running blocked while carrying in the prototype; how much a load slows to be measured Test: S: a carried load raises what a witness catches; H: 'could you tell what Tom was carrying?'
- Source: DESIGN §3 source 3; prototype round 6 (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §6; DESIGN §3, §15; DEFINITIONS pass 3 §G4; MEASUREMENTS-NEEDED A1
- Status: unmeasured. Coverage row: 1.1.4. Conflicts settled: C-002.

### 1.1.5 Hiding and keeping out of sight

- How it works: Hiding is what a man in a street can really do, with only the move keys. A still figure in a doorway counts at the doorway's light (0.12) and is caught at most as a shape, and only beyond 8 m; moving through the same doorway counts at the street's light (0.25 unlit). With his back to a watcher his face cannot be caught, though the coat can. Among three or more people within 2 m a glance at him takes 0.7 s instead of 0.35 s; behind a van, stall or corner nothing is caught; nothing on screen says 'hidden'.
- Standard: Light scale (doorway 0.12, unlit street 0.25) and symmetry (ER-EYES-02); the felt rules to be measured in reference games Test: S: standing still in a doorway lowers what is caught versus walking past; H: 'where would you stand to not be seen?'; addendum rules ER-HIDE-01 to 03
- Source: DESIGN §2 'In the moment'; ER-EYES-02 (waits on a dated study). Designed in: DESIGN-ADDENDUM A1; DESCRIPTION-COPY-2 §7; DESIGN §2 ER-EYES-02
- Status: pending. Coverage row: 1.1.5.

### 1.1.6 Tailing on foot

- How it works: A tail is the town's eyes in reverse: the target looks back about once every 20 to 40 s on foot and at every corner and stop. Being made uses the watcher ladder: a shape is nothing, a mark is a doubt (he speeds up or changes route, always shown first), a face he knows ends the tail and he turns and says so, or runs. There is no hidden distance fail, and losing sight is not failing: the target keeps his routine and Tom picks him up at the next place on it. It ends in a Ledger line within a game minute naming what was learned.
- Standard: none yet: distance bands and the 'made' rule to be measured Test: S: a scripted tail is made at the addendum's rule and never fails on a hidden distance; H: 'did losing him feel fair?'; addendum rules ER-TAIL-01 to 03
- Source: DESIGN §4 (tails family, no numbers) (no reference figure yet). Designed in: DESIGN-ADDENDUM A2 (ER-TAIL-01 to 03); DESIGN §4 Tails; DESCRIPTION-COPY-2 §13
- Status: unmeasured. Coverage row: 1.1.6.

### 1.1.7 Stopping and blending in

- How it works: Sit on a bench, wall or step, lean in a doorway, light a cigarette (key B). A stopped man who belongs (sitting, smoking, waiting at the bus stop) is caught as a shape like anyone and draws no second look; a man standing about at night without a reason draws one. A seated or smoking Tom is never caught more than a walking one at the same spot. Waiting stays under 10% of play (aim about 3%).
- Standard: A stopped Tom draws less notice than a loiterer; tobacco allowed (canon); waiting under 10% of play (ER-CORE-06) Test: S: a seated or smoking Tom is caught less than one standing about; H: minding feels like play; addendum rules ER-STOP-01
- Source: canon content rule; DESIGN §1 (no reference figure yet). Designed in: DESIGN-ADDENDUM A10 (ER-STOP-01); DESCRIPTION-COPY-2 §8 and §34; DESIGN §1 ER-CORE-06
- Status: unmeasured. Coverage row: 1.1.7.

### 1.1.8 Vaulting low walls and fences

- How it works: At set places only (low walls, yard fences and bins under about 1.2 m, marked in the map data), running at one carries Tom over in about 0.8 s. Nowhere else: no jump key, no climbing. A constable vaults the same places in 1.2 s, so a yard and back fence is a real way to gain ground. The road plan has six vault places: one on the yards' lane, three on the terraces' ginnel, one on each warehouse cut.
- Standard: Recommended answer to QUESTIONS-FOR-JAFAR-2026-11-20 Q1, built to it meanwhile; never a jump (ruling 23 Sep); vault speed and heights to be measured Test: S: each vault point works in a chase; no vault anywhere else; addendum rules ER-VAULT-01
- Source: ruling 23 Sep; Q1 (open) (waits on a dated study). Designed in: DESIGN-ADDENDUM A26; DESCRIPTION-COPY-2 §6; DEFINITIONS pass 3 §G1, §G4
- Status: pending. Coverage row: 1.1.8. Conflicts settled: C-003.

### FIT-G4 Tom's, the constables' and the runner's speeds

- How it works: Tom walks at 1.6 m/s, walks slowly at 0.9, runs at 5.5, and with a holdall runs at 5.3, still just faster than a constable. A constable walks his beat at 1.1 m/s and runs at 5.2; he vaults the set places in 1.2 s (Tom 0.8). A runner fleeing Tom runs at Tom's run less about 5%. So Tom outruns a constable on a straight by 0.3 m/s and gains on the vaults; from 10 m behind a runner he closes in about 33 s, and a gap over about 25 m is closed only by a better line. Speeds never depend on the frame rate.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS design pass 3 §G4; FIT-CHECK F21
- Status: pending. Coverage row: FIT-G4.

## 1.2 Driving

The cab and other cars: at AAA quality as the end state, never a driving game.


### 1.2.1 Car handling

- How it works: Fun first, as non-sim open-world games do it; 1990 shows in sound, sway, look and relative speed; automatic gearbox. Game set: 0 to 30 mph in 3.0 to 4.5 s, 0 to 60 in 10 to 14 s; dry braking from 30, 50, 70 mph in 8 to 11, 22 to 30, 44 to 58 m; wet is 1.3 to 1.6 times dry; handbrake turn 120 to 180 degrees settling in 1.0 to 1.6 s. On keys steering eases to lock in 0.2 to 0.35 s and centres in 0.4 to 0.9 s, a lane change at 60 mph swings the tail under 15 degrees and settles within 1 s; the pad is analogue and a set course takes the same time within 10% on keys or pad. Rain lowers grip through the one wetness value.
- Standard: Game set M1 to M9 (e.g. 0 to 30 mph 3.0 to 4.5 s; dry braking 30 mph 8 to 11 m; steering yaw 63% in 0.15 to 0.25 s); ER-DRIVE-02 on keys Test: S: drives D1 to D8 by keys and pad inside the bands; his feel check
- Source: FEEL-TARGETS-DRIVING (c2); DESIGN §5; to be replaced by the measured sheet (DRIVING-MEASUREMENT-METHOD) (waits on a dated study). Designed in: FEEL-TARGETS-DRIVING (c2) M1 to M9; DESIGN §5 ER-DRIVE-02; DESCRIPTION-COPY-2 §10; DEFINITIONS pass 3 §G2
- Status: pending. Coverage row: 1.2.1. Conflicts settled: C-004, C-005.

### 1.2.2 Car camera

- How it works: The chase camera sits about 5.8 m back (band 5 to 6.5 m) and 1.6 to 2.0 m high, with lag of 0.1 to 0.25 s. The field of view is 60 to 65 degrees at rest, 64 to 70 at 30 mph, 70 to 78 at 60, which is how a slow car reads as quick. B held turns it to the rear window for the car in the mirror. It never enters a wall, a car or a post.
- Standard: M10: 5 to 6.5 m back, 1.6 to 2.0 m high, lag 0.1 to 0.25 s, field of view 60 to 65 deg at rest widening to 70 to 78 at 60 mph (the Hook's top speed, G2); ER-DRIVE-06 Test: S: D8 camera run; B: 40-minute soak with no clipped frame
- Source: FEEL-TARGETS-DRIVING (c2) M10; DESIGN §5, §17 (waits on a dated study). Designed in: FEEL-TARGETS-DRIVING (c2) M10; DESIGN §5, §17 ER-DRIVE-06; DESCRIPTION-COPY-2 §10
- Status: pending. Coverage row: 1.2.2.

### 1.2.3 Getting in and out

- How it works: A car Tom may open (the firm's cars, his own, an unlocked one) takes 1.5 to 2.5 s from door to seated, from either side, and he is moving within 1 s after; getting out takes under 2 s. A blocked door never traps him. Forcing a locked parked car takes about 6 s; there is no carjacking of a car with somebody in it. Crew and fares ride in the cab and a man at his side rides along; getting out after a wreck is immediate and Tom walks.
- Standard: a car Tom may open: door to seated 1.5 to 2.5 s, moving within 1 s after; out under 2 s; forced entry of a locked car about 6 s; a blocked door never traps (ER-DRIVE-07) Test: S: enter and exit timed from both sides, door blocked
- Source: STATUS.md and gtavi-driving-builder-2026-11-21 (SOLID); description section 23 (reference game). Designed in: DEFINITIONS design pass 4 'Getting in and out (1.2.3)'; GTAVI-MAP Run 5 additions; DESCRIPTION-COPY-2 s.10, s.23; DESIGN s.5 ER-DRIVE-07; PARTS-TREE notes on 1.2.3
- Status: measured. Coverage row: 1.2.3. Conflicts settled: C-006, C-007.

### 1.2.4 Crashes, damage and unsticking

- How it works: Damage comes in stages by closing speed: under 10 mph is forgiven, then dented, then crumpled, and from about 35 mph in one hit the car will not drive on. It says so at once, Tom gets out and walks, the firm fetches it and it is off the road a day; a dent stays until the firm mends it at the yard overnight. A car wedged on a pole or wall always backs out, and after any crash it moves or can be left within 5 s. Raised by Y1.1: front damage over the threshold pulls the car to one side until repaired, a broken lamp darkens the road ahead at night, and a dent is a mark witnesses remember. A car can ram another; both take damage and nobody inside dies.
- Standard: M11: fragile like The Getaway (under 5 mph nothing; over 30 to 35 mph may not drive on); ER-DRIVE-01 (moves or can be left within 5 s); ER-DRIVE-08. Raised by Y1.1: front damage over the crash threshold pulls the car to one side until repaired, and a broken lamp darkens the road ahead at night; a dent is a mark witnesses remember. Test: S: pole and wall hits at 10, 20, 35, 50 mph; B: 30 minutes of crashing
- Source: FEEL-TARGETS-DRIVING M11; DESIGN §5 (waits on a dated study). Designed in: DESIGN §5 ER-DRIVE-01, -08; DESCRIPTION-COPY-2 §10; FEEL-TARGETS-DRIVING M11; GTAVI-MAP Y1.1; DEFINITIONS pass 3 §F05
- Status: pending. Coverage row: 1.2.4. Conflicts settled: C-008, C-009.

### 1.2.5 Cars and people

- How it works: People look before they step out, so nobody steps out within the stopping distance of a car at 30 mph (23 m); at town speeds a hit is the player's doing, and only his car can strike anybody. A hit knocks a person down and hurts them badly but never kills, whatever they land on. Fall by speed: under 10 mph a stagger, 10 to 25 mph knocked down and sitting up within 5 s, over 25 mph thrown down and still up to 20 s, then moving. The choice (stop and help, or drive off) comes within 2 s; an ambulance takes about ten game minutes; drive off and it is a hit-and-run chase and 'a Mickey's cab knocked her down and never stopped' goes round.
- Standard: Canon (his pick 18 Nov 22:07): hurts, never kills; only the player's car strikes; the choice put within 2 s (ER-DRIVE-03, ER-DRIVE-04, ER-DRIVE-05, ER-DRIVE-10) Test: S: 1,000 seeded crossings with no contact; hits at 5, 15, 30, 50 mph, nobody dies; both choices seeded
- Source: canon content rule; DESIGN §5 (his ruling or canon). Designed in: Canon content rule (his pick 18 Nov 22:07); DESIGN §5 ER-DRIVE-03 to -05, -10; DESCRIPTION-COPY-2 §11; DEFINITIONS pass 3 §P04, §G2
- Status: measured. Coverage row: 1.2.5.

### 1.2.6 Tailing and being tailed by car

- How it works: Following a car works like a foot tail with the car as the mark: a cab behind him twice is a doubt, and the roof sign makes it worse; the doubt always shows first. Being tailed is a fare's wrinkle, a car in the mirror, and B held shows the rear window. The patrol car is no faster than Tom's car on a straight.
- Standard: none yet: following distance and the 'made' rule to be measured Test: S: scripted car tail; H: 'did you know how close was too close?'; addendum rules ER-TAIL-01 to 03
- Source: DESIGN §5 wrinkle 'the tail' (no numbers) (no reference figure yet). Designed in: DESIGN-ADDENDUM A2; DESIGN §5 wrinkles; DEFINITIONS pass 3 §G2
- Status: unmeasured. Coverage row: 1.2.6.

### 1.2.7 Driving with passengers

- How it works: Passengers talk while the car moves; a fare says 'left here' a junction before Pauline does; a sit-down can happen in the back of his own cab. No fare runs longer than 2 real minutes without a decision, a person or a sighting, and driving stays under about a quarter of play. Talk staged while driving runs the clock and the car keeps moving; typing never moves Tom. In a chase, a passenger who knows the town gives at least one landmark line per 20 s.
- Standard: No fare longer than 2 real minutes without a decision, a person or a sighting (ER-CORE-08); typing never moves Tom (ER-TALK-05) Test: H: fare log; S: a staged back-seat talk with the car moving
- Source: DESIGN §1, §11 (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §10, §34; DESIGN §1 ER-CORE-08, §11 ER-TALK-05; DEFINITIONS RT2-20; GTAVI-MAP GV-03
- Status: unmeasured. Coverage row: 1.2.7.

### 1.2.8 Riding as a passenger

- How it works: Kevin, Terry or a crewman can drive Tom: he says where, by landmark, and can skip the ride, which passes exactly its drive time on the clock. He can talk with the driver on the way. A crewman told to drive is an AI driver and always brakes for people.
- Standard: A crewman told to drive is an AI driver and always brakes for people (DESIGN §12); a skipped ride costs its real time on the clock Test: S: a ride arrives; skip advances the clock by the drive's time; addendum rules ER-RIDE-01
- Source: DESIGN §12; canon (his ruling or canon). Designed in: DESIGN-ADDENDUM A24 (ER-RIDE-01); DESCRIPTION-COPY-2 §10; DESIGN §12
- Status: measured. Coverage row: 1.2.8. Conflicts settled: C-010.

### 1.2.9 Repairs, plates and paint

- How it works: A wrecked cab is off the road a day and a dent is mended at the yard overnight. A witness notes the plate as a mark. Shaun Hewson's paint takes the roof sign off and gives a new colour, after which earlier sightings no longer name that car; new plates or a respray also clear a noted plate, but only for witnesses who have not yet told anyone. There is no fuel or wear.
- Standard: A dead car is off the road a day (DESIGN §5); no fuel or wear (DESIGN §18). Raised by GTA VI's respray rule: new plates or a respray clear the police's noted plate for that car (see GV-02). Test: S: a repainted car is not named as the firm's by a witness who saw the old paint; addendum rules ER-PAINT-01
- Source: DESIGN §5, §12, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A24; DESIGN §5, §12, §18; GTAVI-MAP GV-02
- Status: decided. Coverage row: 1.2.9. Conflicts settled: C-011.

### 1.2.10 Taking a parked car

- How it works: Only parked cars, never one with somebody in it, and only by force, with no minigame. It is loud (heard at the force reach), the owner reports it when he finds it gone, the car is then known to the police, and a taken car has no roof sign so witnesses do not name it as the firm's. Taking one by force takes about 6 s (the description, section 23, kept by design pass 4). GTA VI's two ways in (a brick through the quarter-light or a tool at the door) are a lead to check in the footage pass, without their times; a car with a steering lock cannot be taken.
- Standard: Recommended answer to Q2, built to it meanwhile; no lockpicking game (DESIGN §18); never a moving car. Forced entry about 6 s (design pass 4, 1.2.3); a car with a steering lock cannot be taken. Test: S: a taken car is reported and named; force heard at its reach; addendum rules ER-TAKE-01
- Source: Q2 (open) (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A27; ONE-SHOT-PROMPT 'Taking a parked car'; GTAVI-MAP Y1.2
- Status: decided. Coverage row: 1.2.10. Conflicts settled: C-012.

### 1.2.11 The horn

- How it works: One key (H) sounds the horn while held. It is a noise at about 60 m by day, further at night and less in rain, and turns watchers' heads like any noise. A short toot outside a door brings out a fare or a man Tom is waiting for within 10 s if he is within 15 m; a long blast in a quiet street at night draws a look from lit windows; pedestrians in the road step aside; it never alarms police alone.
- Standard: rule: A horn sounded at night is heard by every listener inside its reach and by nobody outside it, and a waiting fare inside 15 m comes out within 10 s (golden rows). Test: A horn sounded at night is heard by every listener inside its reach and by nobody outside it, and a waiting fare inside 15 m comes out within 10 s (golden rows).
- Source: DESIGN-ADDENDUM-2026-11-20 A32 (from REFERENCE-MECHANICS-2026-11-20 M1.75) (reference game). Designed in: DESIGN-ADDENDUM A32; DESCRIPTION-COPY-2 §10
- Status: measured. Coverage row: 1.2.11.

### GV-01 The boot, seen

- How it works: The cab's boot holds what is not on him: the envelope, a spare coat, a box. Opening it is an act with the seven slots, seen like any act. A constable who stops the cab with cause may look in it, and what is in the boot survives save and load. A body goes into the boot in 4 s.
- Standard: Opening the boot is perceived like any act; a stop with cause searches it; what is in it survives save and load. Test: B: boot opened in sight of a watcher x 20 (memory written); a stop with cause finds the boot's contents.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP §GV-01; DEFINITIONS RT2-11
- Status: decided. Coverage row: GV-01.

### GV-03 The passenger who knows the way

- How it works: Whoever rides with Tom (Ron, a crewman, a fare who knows the town) says the way by landmark in a chase and when asked on a fare: 'left after the chapel, he cannot follow you through the yard'. No marker. At least one landmark line per 20 s of chase, each naming a real landmark on the way.
- Standard: In a car chase with a passenger, at least one landmark line per 20 s of chase; every line names a real landmark on the way. Test: B: car chases with each passenger; lines logged and checked against the map.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP §GV-03; DESCRIPTION-COPY-2 §10
- Status: decided. Coverage row: GV-03.

### FIT-G2 Car speeds and the stop band

- How it works: The Hook is a 30 mph town (the built-up limit of 1990). Traffic drives at 20 to 28 mph; every car in the Hook reaches 60 mph on the 420 m straights and no more there; a patrol car is no faster than Tom's car on a straight. The patrol stops a driver it sees at 50 mph or more, or doing a reckless act (a hit, the pavement, a red light at speed); 31 to 49 mph draws a look and a noted plate, never a stop. Nobody steps out within the 23 m stopping distance of a car at 30 mph.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 §G2; FIT-CHECK F33
- Status: decided. Coverage row: FIT-G2. Conflicts settled: C-013.

### FIT-F05 How often the one-hit wreck happens in ordinary driving

- How it works: Named only; not designed beyond: a measurement. Bot chases and an hour of ordinary fast driving on the prototype count hits of 35 mph or more; the pass is that ordinary driving under 30 mph wrecks the car less than once an hour (cloud, 1 h, with the next prototype build). It tests whether the one-hit wreck at about 35 mph (DESIGN §5) ends chases too often.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS design pass 3 §F05; FIT-CHECK F05
- Status: pending. Coverage row: FIT-F05.

### FIT-P04 The struck person's fall

- How it works: A person hit by Tom's car falls by speed: under 10 mph a stagger and a hand on the bonnet; 10 to 25 mph knocked down, rolls once and sits up within 5 s holding the hurt; over 25 mph thrown down, lies still up to 20 s, then moves and calls out. Never a body flung through the air, never limp as dead, nothing shown at length; the choice comes within 2 s. A person always moves within 20 s.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 §P04; DESCRIPTION-COPY-2 §11
- Status: decided. Coverage row: FIT-P04.

## 1.3 Fighting

Fists first, things to hand, carried weapons, guns rare and last; the whole street watches.


### 1.3.1 Blows and contact

- How it works: A blow starts within 0.1 s of the button. A jab lands in 0.25 to 0.40 s; the committed heavy blow in 0.63 to 0.85 s and cannot be cancelled, which is what makes it readable. Contact is sold by a hit-stop of 0.025 to 0.13 s by blow (jab 0.025 to 0.05, heavy 0.06 to 0.12, swing 0.07 to 0.13), a brief camera close-in held about 0.8 s inside the wider fight view, a small shake and four layers of sound. A struck man reels to the side he was hit.
- Standard: ER-FIGHT-01 (timings inside the melee sheet bands C1 to C15): C1 blow starts within 0.1 s; C2 jab 0.25 to 0.40 s to contact, heavy 0.63 to 0.85 s; C3 hit-stop 0.025 to 0.13 s by blow; camera close-in held about 0.8 s Test: S: melee drills at 1/60 s inside C1 to C15 (tools/lane/melee_drills.py); his feel check
- Source: FEEL-TARGETS-MELEE (c); DESIGN §7 (waits on a dated study). Designed in: FEEL-TARGETS-MELEE C1 to C4, C10; DESIGN §7 Feel; DESCRIPTION-COPY-2 §9
- Status: pending. Coverage row: 1.3.1.

### 1.3.2 Reading and answering blows

- How it works: Every incoming blow can be read 0.45 to 0.80 s before it lands, in the other man's shoulders, feet and breath, never an icon; at most two men swing at once, 0.4 s apart. Guard (a held key) makes a blocked fist do little, a blocked heavy blow stagger Tom a little, and a swung weapon break through. A tap with a direction slips a blow (about 0.3 s); a blow thrown just after a slip or block counts as a counter, a heavy blow at a jab's speed. Mashing empties Tom in 6 to 10 jabs and he needs 4 to 8 s for his wind; the slower-fights assist makes wind-ups 25% longer with one swinger.
- Standard: Every incoming blow readable 0.45 to 0.80 s before it lands; at most two men swing at once, 0.4 s apart (ER-FIGHT-02) Test: S: drills; H: 'did you see the blow coming?'; addendum rules ER-DEFEND-01 to 02
- Source: DESIGN §7; melee sheet (waits on a dated study). Designed in: DESIGN §7 ER-FIGHT-02; DESIGN-ADDENDUM A29; DESCRIPTION-COPY-2 §9, §3; FEEL-TARGETS-MELEE C5, C6, C8, C11
- Status: pending. Coverage row: 1.3.2.

### 1.3.3 Targeting without lock-on

- How it works: No lock-on: the man the stick points at is the man hit, and Tom slides to about 1 m in the wind-up. With three men round him he hits the one he points at, and nobody is hit through a wall. Closing in takes 0.40 to 0.55 s from at most 2.0 m.
- Standard: ER-FIGHT-06: the man pointed at is the man hit, nobody hit through a wall; slide to about 1 m (lead) Test: S: targeting script with three men round Tom
- Source: DESIGN §7 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §7 ER-FIGHT-06; DESCRIPTION-COPY-2 §9; FEEL-TARGETS-MELEE C9
- Status: decided. Coverage row: 1.3.3.

### 1.3.4 The lower rungs

- How it works: The ladder has eight rungs: stare, square up, threaten, shove or grab, strike, weapon out, weapon used, kill. Most confrontations end on rungs 1 to 4: a stare held, a man squared up to, a threat said (in talk or shown), a shove into a wall, and somebody gives way. Each rung is an act with the seven slots, so the town treats it like any deed. On the M key a hard look is rung 1 and a shove rung 4; a grab holds a man about 2 s.
- Standard: Most confrontations end on rungs 1 to 4; each rung an act the town treats like any deed Test: S: each rung exposes seven slots; H: rung reached and why
- Source: his combat design 12 Oct; DESIGN §7 (his ruling or canon). Designed in: DESIGN §7; DESCRIPTION-COPY-2 §9, §8; RULINGS 12 Oct (combat design)
- Status: measured. Coverage row: 1.3.4.

### 1.3.5 The street as a weapon

- How it works: Seven places first: walls, doorways, railings, car bonnets, steps, kerbs and the quay edge, each a paired move fitted by height (a man shoved against railings, a head against a bonnet, a man put over the quay edge). Nothing is shown at length. A man put into railings is out of the fight for 4 s, and a man put in the water climbs out at the nearest ladder within a minute.
- Standard: Seven places first, fitted by height (DESIGN); Sleeping Dogs' environment moves as the reference (melee sheet (a)) Test: S: each of seven places triggers its move; content check: no finisher shown at length
- Source: DESIGN §7; FEEL-TARGETS-MELEE (a) (reference game). Designed in: DESIGN §7; DESCRIPTION-COPY-2 §9, §6; DEFINITIONS pass 3 §P18; FEEL-TARGETS-MELEE (a)
- Status: measured. Coverage row: 1.3.5.

### 1.3.6 Things to hand and carried weapons

- How it works: Things to hand break: a chair after about 2 blows, a brick 3, a dustbin lid 4, a wheel brace never, and they are left behind. Carried weapons (cosh, knuckleduster, knife, bat) can be seen on him, are found in a search and must be got rid of; a weapon comes out only on a held input (semicolon), chosen from the two things under the coat, and cannot be undrawn unseen. A swung improvised weapon takes 0.80 to 1.05 s to contact. What the town makes of a blow rises with the weapon, with no number shown.
- Standard: Breaks after chair 2, brick 3, lid 4 blows, wheel brace never; C2 swing 0.80 to 1.05 s; a weapon drawn cannot be undrawn unseen Test: S: breakage counts; a weapon out on a held input only (ER-FIGHT-08); a cosh from behind on an unaware man knocks out and is seen as a strike
- Source: DESIGN §7; melee sheet C2 (no reference figure yet). Designed in: DESIGN §7; DESCRIPTION-COPY-2 §9; FEEL-TARGETS-MELEE C2, C12; DESIGN §7 ER-FIGHT-08
- Status: unmeasured. Coverage row: 1.3.6.

### 1.3.7 Condition without bars

- How it works: There is no health bar: posture, breath, a dropped guard, blood and a limp show a man's state, and a player asked 'who was winning?' can say. Fists knock a man out (10 to 30 s) and never kill on their own. A fall against a kerb, wall or step within 3 s of a blow can kill, rarely, and the town treats it as a killing; the quiet blow from behind with a cosh or fist knocks out for 10 to 30 s. Tom has three states, fresh, hurt and beaten, shown only in his body.
- Standard: No health bar; fists never kill; only a fall against kerb, wall or step within 3 s of a blow can, rarely (ER-FIGHT-05); knock-out 10 to 30 s Test: S: 10,000 simulated fights, deaths only by the fall rule; H: 'who was winning?'
- Source: ruling 30 Oct; DESIGN §7; melee sheet (his ruling or canon). Designed in: DESCRIPTION-COPY-2 §9; DESIGN §7 ER-FIGHT-05; RULINGS 30 Oct; FEEL-TARGETS-MELEE C7; DEFINITIONS RT-11, RT2-12
- Status: measured. Coverage row: 1.3.7.

### 1.3.8 Odds, crowds and nerve in a fight

- How it works: A fair one-on-one is roughly even and skill tips it: a patient fighter wins most, a masher fewer than 3 in 10. Two against one is deadly and three is a beating; a skilled player wins a fair two against one about one time in four (15 to 35% in the bots), a masher under 10%. A man who is watched or cornered stands longer; alone he gives way sooner; blood on Tom lowers his nerve. Watchers keep about 3 m and scatter once a weapon is out; a man at Tom's side takes the second man.
- Standard: Fair one-on-one roughly even; skill beats mashing (patient bot wins most, masher under 3 in 10, ER-FIGHT-07); watchers about 3 m (lead) Test: S: scripted patient and mashing fighters; seeded nerve cases
- Source: DESIGN §7 (no reference figure yet). Designed in: DESIGN §7 ER-FIGHT-07; DESCRIPTION-COPY-2 §9; DEFINITIONS pass 3 §P18
- Status: unmeasured. Coverage row: 1.3.8.

### 1.3.9 How a fight ends

- How it works: A fight ends when someone backs off, runs, goes down, the police arrive or people step in; backing off and running are inputs at every moment. Tom cannot die: beaten, he comes round on the pavement, in Grace Rinaldi's kitchen or in hospital, sometimes robbed, with a street that knows he lost, and is in control within 60 real seconds with the cost said. Hospital costs days, never money, and plants a witness.
- Standard: A way out at every moment (ER-FIGHT-03); Tom never dies, in control within 60 real s (ER-FIGHT-04); Tom cannot die (the approved design) Test: S: each of five endings scripted; beaten route timed
- Source: DESIGN §7; the description §3; the approved design, canon OPEN 3 (his ruling or canon). Designed in: DESIGN §7 Death; DESCRIPTION-COPY-2 §9; DEFINITIONS RT2-13; canon OPEN 3 (the approved whole-game design)
- Status: measured. Coverage row: 1.3.9. Conflicts settled: C-014.

### 1.3.10 Firearms

- How it works: Guns are rare and late, after melee, and AAA when used. None in the Hook at the start; they come only through people (bought, stolen, taken, or found once at Mickey's). A held semicolon draws from under the coat, the camera goes to an aim row, there is no crosshair and no ammunition count; before War a hit wounds and never kills, at War it can kill. A shot is heard to about 177 m by day and whoever hears it keeps it for good. The dial runs Fists, Shown, Fired, War and never moves on a deed nobody saw or heard.
- Standard: Guns rare and late (ruling 18 Nov end state A); AAA when used; shot heard 177 m by day; feel numbers to be measured Test: S: dial rules; feel numbers inside measured bands once researched
- Source: RULINGS 28 Oct combat line; DESIGN §7 dial (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §27; DESIGN §7 dial; DEFINITIONS RT-10, RT2-14; RULINGS 28 Oct combat line (18 Nov end state A)
- Status: unmeasured. Coverage row: 1.3.10.

### 1.3.11 Marks that last

- How it works: A beaten Tom carries bruises and a cut lip for three game days and a limp for one. Others see them (a give-away) and say so, and marks fade on the clock. A bat leaves a limp for a day; a knife wound bleeds, with blood on the coat, until stitched. A retired doctor in a terrace by the quay stitches without asking, for money (£20 in the price list), and remembers.
- Standard: Condition shows in the body, never a bar (DESIGN §7); a mark is a give-away (DESIGN §2) Test: S: a marked Tom is caught more; marks fade on the clock; addendum rules ER-MARK-01
- Source: DESIGN §2, §7 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A21 (ER-MARK-01); DESCRIPTION-COPY-2 §9; DEFINITIONS RT-11, §G8
- Status: decided. Coverage row: 1.3.11.

### 1.3.12 Fighter types

- How it works: Every fight's men are written as one of a few kinds: a boxer who guards, a brawler who rushes, a big man slow to drop, a man with a knife who keeps his distance, and (from the fit check) a wiry one who slips and runs. A big man has the most hidden capacity and a knife man the least. No two fights in a row use the same mix, so Lee on the quay, Iveson's yard hand and the two dockers by car two each feel different.
- Standard: No two fights in a row use the same mix (ER-TYPES-01); players punish the same loop (PLAYERS punish 9) Test: S: the job data; addendum rules ER-TYPES-01
- Source: PLAYERS.md; DESIGN §18 (reference game). Designed in: DESCRIPTION-COPY-2 §9; DESIGN-ADDENDUM A29 (ER-TYPES-01); DEFINITIONS pass 3 §P17, RT-11
- Status: measured. Coverage row: 1.3.12. Conflicts settled: C-015.

### RT-09 Tom's line against women, over-sixties and the priest

- How it works: If someone Tom's line covers (a woman, anyone of sixty or over, the priest) attacks him, he guards, slips and backs off; the strike input does nothing and he says so. In a fight that includes them he strikes, shoves or grabs only the others, and does not grab a covered person even to take a weapon. He refuses a send that would hurt one, in his own words. A rival's men are not bound. The line holds at the boxing club and in hold-ups.
- Standard: Zero strikes, shoves or grabs by Tom on anyone covered, and zero sends that hurt one, in any fight, hold-up or send. Test: B: seeded fights and sends including covered people; any such strike fails.
- Source: The description, section 10 (Tom's own line) and its conflicts note on hold-ups. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-09; DESCRIPTION-COPY-2 §9; DESIGN-ADDENDUM A41
- Status: decided. Coverage row: RT-09. Conflicts settled: C-016.

### RT-10 Firearms as a verb

- How it works: Guns are late and rare through the dial. A held semicolon draws from under the coat, the camera goes to the aim row, and the mouse or stick aims with no crosshair (an optional dot, off by default). A hit depends on aim, distance and whether Tom moved; before War a hit wounds and never kills, at War a body hit can kill, a named and permanent event. An aimed shot to the arm disarms and one to the leg stops a runner (Y1.5). A revolver holds six and reloads in a shown action; men with guns shoot from where they stand, never use cover, and run when outmatched; nobody shoots from a moving car. A shot Tom goes down, comes round in hospital and never dies.
- Standard: The rules above pass or fail; draw, aim and hit timings within the band of the firearms footage measuring. Test: B: a gun range scene with timings; S: no on-screen count.
- Source: The description, sections 3, 33; ruling 18 Nov (guns rare and late); MEASUREMENTS-NEEDED A (firearms feel); Y1.5. (waits on a dated study). Designed in: DEFINITIONS §RT-10; DESCRIPTION-COPY-2 §27; RULINGS 18 Nov (guns rare and late); MEASUREMENTS-NEEDED A12; GTAVI-MAP Y1.5
- Status: pending. Coverage row: RT-10.

### RT-11 Hidden damage and injury states

- How it works: Each man has a hidden capacity by fighter type (big man most, knife man least): a jab takes little, a heavy blow about three jabs' worth, a weapon more (bat more than cosh); a blow from behind knocks out for 10 to 30 s. Down is out, never dead from fists. Tom has three states shown only in his body: fresh, hurt (guard slower to rise, breath shorter, a stagger) and beaten (down). A knife wound bleeds until stitched; a bat leaves a limp for a day; hurt does not stack past beaten.
- Standard: Blows to put a man down per type within the band of the damage footage measuring (KCD2, Sleeping Dogs, RDR2); "who was winning?" answered right by 4 of 5 testers from the body alone. Test: B: fixed-seed fights counting blows to down per type; P: the five-friend question.
- Source: The description, section 10; MEASUREMENTS-NEEDED A (damage model). (waits on a dated study). Designed in: DEFINITIONS §RT-11; DESCRIPTION-COPY-2 §9; MEASUREMENTS-NEEDED A6
- Status: pending. Coverage row: RT-11.

### RT2-11 Finishing a downed man, kicks and bodies

- How it works: There is no kick input and no finisher animation. Finishing a downed man is a decision in the quiet afterwards: with nobody else standing, Tom stands over him and holds strike for 2 s, and the game asks 'Finish him?' twice. With fists yes is a serious beating (hospital, days), never a death; with a weapon it is a killing. The camera turns away and the sound carries it. A body is dragged at 0.9 m/s, loaded into a boot in 4 s, or put in the dock from the quay edge in 3 s; a living man put in the water climbs out at the nearest ladder. A knife wounds (hospital 5 game days, blood on Tom, 8 hours if arrested) and kills only by the finishing decision or the fall rule.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-11 Test: B (bot), as written under RT2-11
- Source: design pass 3, RT2-11 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 RT2-11; DESCRIPTION-COPY-2 §9; canon content rule
- Status: decided. Coverage row: RT2-11. Conflicts settled: C-017.

### RT2-12 The rare fatal fall

- How it works: A fall kills only when all hold: a heavy or weapon blow knocks the man down, his head lands within 0.4 m of a kerb's edge, a step's edge or a wall's foot, and he was already spent (at least three heavy blows or one weapon blow taken before). Beforehand he shows it, unsteady with his guard down. Never in the boxing club, never by a car, never to Tom, never from fists alone on open ground. It is deterministic: the same fight replayed gives the same result; at the three edges a fall kills in 1 in 50 to 1 in 20 knockdowns, away from any edge never.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-12 Test: B (bot), as written under RT2-12
- Source: design pass 3, RT2-12 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 RT2-12; DESIGN §7 ER-FIGHT-05; RULINGS 30 Oct
- Status: decided. Coverage row: RT2-12.

### RT2-13 Robbed when beaten

- How it works: Tom is robbed when beaten by men who rob for a living (a rival's men, the dockers by car two, a robber), never by a constable, at the boxing club, or by a debtor standing his ground. They take the paper money in his pocket (coins are left) and anything in his hand or under the coat they want (the envelope, a weapon, goods), never the Ledger, his coat or the office keys. The takers are named men with routines, whom Tom can front up, send men at, or let go; a taken envelope becomes a debt to the landing men of what it held, said by Ron the next day.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-13 Test: B (bot), as written under RT2-13
- Source: design pass 3, RT2-13 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 RT2-13; DESCRIPTION-COPY-2 §9
- Status: decided. Coverage row: RT2-13. Conflicts settled: C-018.

### RT2-14 How guns reach Tom

- How it works: Two kinds of gun, both of fictional make: a service revolver (six rounds) and a sawn-off shotgun (two). None in the Hook at the start. Mickey's revolver lies in his inner office desk under the real book, found once when the locked office opens on Sheila's trust (rung 2; see the gap on guns rare and late). One seller, a deckhand off a coaster in on Tuesdays and Fridays, sells at the fish dock after midnight to a man introduced by Rita (rung 3) or Darren's tip: revolver £150, shotgun £90, rounds £10 a box. A gun can also be taken from a man who drew one or from a body, or stolen from a rival's lock-up on a raid. A gun moves the dial only when seen or heard.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-14 Test: B (bot), as written under RT2-14
- Source: design pass 3, RT2-14 (waits on a dated study). Designed in: DEFINITIONS design pass 3 RT2-14; DESCRIPTION-COPY-2 §27
- Status: pending. Coverage row: RT2-14.

### FIT-P17 At least five kinds of fighter

- How it works: At least five kinds of fighter: the boxer who guards, the brawler who rushes, the big man slow to drop, the man with a knife who keeps his distance, and the wiry one who slips and runs. No two fights in a row use the same mix.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 §P17; DESIGN-ADDENDUM A29
- Status: decided. Coverage row: FIT-P17. Conflicts settled: C-019.

### FIT-P18 Two against one stays deadly

- How it works: Two against one stays deadly: a skilled player, patient and using the street, wins a fair two against one about one time in four; a masher about one in twenty. Running and backing off are always there, and the street's places count double (a man put into railings is out of it for 4 s). In 200 bot fights the skilled bot wins 15 to 35% and the masher under 10%.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 §P18; DESCRIPTION-COPY-2 §9
- Status: decided. Coverage row: FIT-P18.

## 1.4 Being seen

The felt side of the town's eyes: the player's three questions answered from picture and sound.


### 1.4.1 Reading watchers

- How it works: The world shows who has noticed him in bodies: a head turns, a longer look, a pause in a walk, two heads together, a step back at night, a figure at the glass of a lit window. The head turns at the start of the 1.2 s a watcher needs to know him, so there is at least 0.8 s of warning. A window is a watcher only when a figure shows at it (Ada in her dark front room is the one exception, learned once). A player can answer 'is he seen, how far did that carry, who noticed' from picture and sound eight times in ten, also with sound off and with the light cue off.
- Standard: Cue at the start of the 1.2 s to know him, at least 0.8 s before identification (ER-EYES-03); posture first (D29); a window is a watcher only when a figure shows at it (ER-NIGHT-02); reference behaviour to be measured Test: H: the three questions at ten random moments, 8 of 10 right, sound off and light cue off
- Source: DESIGN §2; D29 (waits on a dated study). Designed in: DESIGN §2 ER-EYES-01, -03; DESIGN §6 ER-NIGHT-02; DESCRIPTION-COPY-2 §7
- Status: pending. Coverage row: 1.4.1.

### 1.4.2 Light and dark as cover

- How it works: The light value the watchers use is the one the player sees: the corners of the picture darken and lift with it (daylight 1, lamp 0.7, unlit street 0.25, doorway 0.12). Dark is readable, never blind: Tom and the ground 5 m round him are always visible above a brightness floor.
- Standard: Picture corners follow the rule's light value; Tom and 5 m round him always visible above a brightness floor (ER-NIGHT-01) Test: H: screenshots at the darkest spots; S: light value matches the cue
- Source: DESIGN §2, §6 (waits on a dated study). Designed in: DESIGN §2, §6 ER-NIGHT-01; DESCRIPTION-COPY-2 §7, §3
- Status: pending. Coverage row: 1.4.2.

### 1.4.3 Hearing his own noise

- How it works: Every noise the rule hears, the player hears at the same strength. Reach is set by the act, the hour and the rain: a footstep at three in the morning carries about 3.6 m and at noon nothing; walking slowly halves the reach; the cab is heard within about 44 m by day. A street that has noticed him goes quiet. With the picture off a tester can still tell a walk from a run; a 'sound shown' assist offers short words for deaf players.
- Standard: ER-SND-01: every noise the rule hears the player hears at the same strength; with picture off a walk is told from a run Test: H: sound-only test
- Source: DESIGN §17 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2, §17 ER-SND-01; DESCRIPTION-COPY-2 §6, §10, §3
- Status: decided. Coverage row: 1.4.3.

### 1.4.4 Give-aways and the coat

- How it works: What makes him easier to know: running, the same coat as last night, blood (until washed with water in private), dirt, a weapon in the hand, wrong clothes for the door, bruises, a holdall, the car. The coat buys doubt about the face and none about the car: a deed from the car always names the car. He can shed a slot against witnesses who have not told yet: change the coat, use the second car or respray, a cap and scarf at night or a barber for a week, walk apart from Ron, get rid of the weapon; what gossip has carried is never undone.
- Standard: ER-EYES-10: each give-away raises what a witness catches; a deed from the car always names the car Test: S: golden rows, one per give-away
- Source: DESIGN §2 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2 'What gives him away', ER-EYES-10; DESIGN-ADDENDUM A21; GTAVI-MAP GV-02; DESCRIPTION-COPY-2 §7
- Status: decided. Coverage row: 1.4.4. Conflicts settled: C-020.

### 1.4.5 Reaching the witness

- How it works: A witness who means to tell sets off, to a friend, a phone box or the station, and is seen going; when the walk starts in Tom's sight it lasts at least 30 real seconds (50% longer with the assist). 'Oi!' stops her for about 2 s and turns her round; then he can talk her round, pay, threaten, help or let her go. A threat can stop a report to the police, never the street's talk; a paid witness remembers being paid. A phone-box call brings a constable that night and the statement is signed at the station at nine next morning, until which Tom can still reach her.
- Standard: The walk lasts at least 30 real s when it starts in Tom's sight (ER-EYES-04); a threat stops a report, never the talk (ruling 3 Oct) Test: S: walk timed; H: 'did you get to her first?'
- Source: DESIGN §2; ruling 3 Oct (his ruling or canon). Designed in: DESIGN §2 'The walk', ER-EYES-04; DESCRIPTION-COPY-2 §16, §8; RULINGS 3 Oct; DEFINITIONS RT2-19
- Status: measured. Coverage row: 1.4.5.

### 1.4.6 Seeing assist

- How it works: An optional outline of the people Tom can see who are facing him. It is off by default, an assist that changes only its own thing, and never shows a figure he could not see or what anyone knows. It is not a meter.
- Standard: Never a figure he could not see, never what they know (ER-SCREEN-01) Test: S: screen inventory with the assist on
- Source: DESIGN §2, §17 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2, §17 ER-SCREEN-01; DESCRIPTION-COPY-2 §3 (What the screen does show)
- Status: decided. Coverage row: 1.4.6.

### 1.4.7 Street manners

- How it works: Street manners sit on one key (M), picked by the stick: a nod, a greeting, a hard look, a shove, and a call ('Oi!') that stops a walker for about 2 s and turns him round. Each is an act with the seven slots, answered in body or voice within 1 s and remembered like any act. A greeting raises nothing; a hard look and a shove are rungs 1 and 4.
- Standard: Answered in body or voice within 1 s; each is an act with the seven slots (canon moat) Test: S: each gesture answered within 1 s and remembered; addendum rules ER-MANNER-01
- Source: canon; DESIGN §7 lower rungs (his ruling or canon). Designed in: DESIGN-ADDENDUM A10 (ER-MANNER-01); DESCRIPTION-COPY-2 §8
- Status: measured. Coverage row: 1.4.7.

### 1.4.8 Drawing a watcher away

- How it works: A thrown stone (O) or a rattled bin makes a noise at its reach; a watcher inside it turns his head or walks to look, and remembers there was a noise. A rattled bin moves the beat constable off his round and he rejoins it where he left. A yard dog barks at a stranger and a scrap of food quiets it for a while; no verb harms a dog.
- Standard: Uses the sound reach rule (DESIGN §2); a watcher drawn away remembers the noise Test: S: a noise inside reach turns a head; outside reach does nothing
- Source: DESIGN §2 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A23; DESCRIPTION-COPY-2 §3 (Controls); DEFINITIONS pass 3 §G5
- Status: decided. Coverage row: 1.4.8.

## 1.5 Chases

On foot and by car; every chase ends, caught or lost.


### 1.5.1 Fleeing on foot

- How it works: Run from a constable and it is a chase through the Hook's back ways: ginnels, yards, bollarded lanes a car cannot follow, six vault places. There is no timer. It is lost once the constable has not seen Tom for 7 s, or the gap is over 70 m while he is out of sight (70 m applies on foot; a car chase uses 200 m), and otherwise ends caught, wrecked or at the soft edge. A good bot's foot chase has a median of 30 to 90 s (the ginnel and a street). Tom runs 5.5 m/s, a constable 5.2 and vaults in 1.2 s against Tom's 0.8. After losing him the constable searches the last-seen streets for 30 to 120 real s; seen inside it, the same chase resumes.
- Standard: Lost once unseen for 7 s or 70 m (DESIGN §8); No chase ends while the pursuer can see Tom, except caught, wrecked or at the soft edge; lost car chase median 60 to 120 s, 90th percentile under 240 s; foot chase median 30 to 90 s; none past 240 s (design pass 4, DP5-C01 to C03); feel to be measured in reference games Test: S: 50 seeded chases, chase and search lengths logged (DP5-C01 to C03); H: 'how did you lose him?'
- Source: DESIGN §8; advisor 256 (waits on a dated study). Designed in: DEFINITIONS design pass 4 C-01 to C-03 and Run 5 second pass; design pass 3 F03, G1, G4; DESIGN s.8
- Status: pending. Coverage row: 1.5.1. Conflicts settled: C-021, C-022.

### 1.5.2 Pursuing on foot

- How it works: Somebody runs from Tom: a runner fare, a man from a fight, a witness heading for the phone. He runs at Tom's run speed less about 5% (5.2 against 5.5 m/s) by the routes of his own routine. From 10 m behind a runner on a straight Tom closes in about 33 s; a gap over about 25 m is closed only by a better line. A hand on the collar from within 1 m behind, then let go, talk or the lower rungs; breaking sight for 7 s or 70 m loses him and he goes home or to a friend. As with every chase there is no timer; a foot chase is a median of 30 to 90 s.
- Standard: none yet: catch-up speeds and give-up rules to be measured Test: S: a runner can be caught by a direct line and lost by a slow one; no timer, foot chase median 30 to 90 s (DP5-C02); addendum rules ER-PURSUE-01 to 02
- Source: DESIGN §5 runner wrinkle, §7 'someone runs' (waits on a dated study). Designed in: DESIGN-ADDENDUM A3 (ER-PURSUE-01, -02); DEFINITIONS design pass 4 C-01, C-02; design pass 3 G4
- Status: pending. Coverage row: 1.5.2. Conflicts settled: C-023.

### 1.5.3 Car chases

- How it works: A hit-and-run seen by an officer, a refused stop or a car that saw the deed starts a chase with the patrol car's bell and lights. There is no timer: it ends lost, caught, wrecked or at the soft edge. A car chase is lost by 7 s unseen or a gap over 200 m while unseen, never by distance driven alone. A good-driver bot's lost car chase has a median of 60 to 120 s and a 90th percentile under 240 s; none passes 4 real minutes. The drivable loop is 1,528 m, a lap in 76 to 96 s. Caught is a stop or an arrest, never a game over, and nobody shoots from a moving car.
- Standard: Refusing a stop is a chase that ends caught or lost (DESIGN §5); ER-DRIVE-10; No chase ends while the pursuer can see Tom, except caught, wrecked or at the soft edge; lost car chase median 60 to 120 s, 90th percentile under 240 s; foot chase median 30 to 90 s; none past 240 s (design pass 4, DP5-C01 to C03) Test: S: 50 seeded chases, chase and search lengths logged (DP5-C01 to C03); lost by breaking sight
- Source: DESIGN §5, §8 (waits on a dated study). Designed in: DEFINITIONS design pass 4 C-01, C-02, Run 5 second pass 'Can the Hook and the docks hold the measured chases?'; design pass 3 F03, G1, G3; DESIGN s.5
- Status: pending. Coverage row: 1.5.3. Conflicts settled: C-024, C-025, C-026.

### 1.5.4 Pursuers

- How it works: A constable announces himself (footsteps, a torch, a cough) at least 3 s before he can challenge, and calls out first. He walks his beat at 1.1 m/s, runs 5.2 m/s, never sees through a wall, never knows where Tom went without seeing, and never catches by a speed Tom cannot match on a straight. The patrol car is no faster than Tom's car. He gives up only when sight is broken (7 s unseen, or the gap over 200 m by car or 70 m on foot): no chase ends while he can see Tom. After that he searches the last-seen streets for 30 to 120 real s, lamp on the turnings, then waits on that road for the night; seeing Tom inside the search resumes the same chase, after it starts a new one.
- Standard: Police announce themselves 3 s before a challenge (ER-POL-02); give up when sight is broken per 1.5.1 Test: S: pursuer gives up at the rule; never cheats through walls
- Source: DESIGN §8 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN s.8 ER-POL-02; DESCRIPTION-COPY-2 s.18, s.19; DESIGN-ADDENDUM A3, A36; DEFINITIONS design pass 4 C-01, C-03; design pass 3 G2, G4, G5
- Status: decided. Coverage row: 1.5.4. Conflicts settled: C-027.

### RT2-22 A foot chase caught by a constable

- How it works: A constable who catches Tom (his hand on the collar) searches as if Tom had stood. Found nothing and no cause beyond running: Tom's name is taken (the constable now knows him) and a word, no arrest. Found a weapon, stolen goods or the envelope, or Tom is wanted on a signed statement, or the constable saw the deed: arrest with that deed's hours. Running is not a crime, but the next challenge by that officer is on cause and he searches without being talked round; seen again the same night or while the deed is hot he calls out and a new chase starts.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-22 Test: B (bot), as written under RT2-22
- Source: design pass 3, RT2-22 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 RT2-22; DESCRIPTION-COPY-2 §18, §19
- Status: decided. Coverage row: RT2-22.

### FIT-G3 A chase at the soft edge

- How it works: One rule for any chase, by car or on foot, that reaches the soft edge: it ends there as lost, the pursuer turns back, and Tom or his car goes out of the Hook and comes back as time passed (30 game minutes out and back, which is 30 real seconds at 60 s a game hour, nothing on screen). The patrol waits on that road for the rest of the night, so Tom must come back past it. A plate read within 18 m in light 0.7 or more is noted, and a deed he saw brings a constable to the office next morning at ten. Driving to the edge with no chase offers the six districts by landmark and comes back as time passed. Design pass 4 makes the edge one of the four chase endings (lost, caught, wrecked, edge).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 G3; design pass 4 C-01; FIT-CHECK F34
- Status: decided. Coverage row: FIT-G3. Conflicts settled: C-028.

### FIT-F03 What the 70 m of a lost chase means

- How it works: A chase is lost when the pursuer has not seen Tom for 7 s, or the gap is over 70 m while Tom is out of sight. For car chases the distance is 200 m, because a car covers 70 m in about 4 s. On foot the gap rarely reaches 70 m in a typical chase, so foot chases are mostly lost by the 7 s. Distance driven alone never loses a chase. Design pass 4 changes only the wording: 'inside 90 s' becomes 'in a typical chase', since no chase has a timer.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 F03; design pass 4 C-01; FIT-CHECK F03
- Status: decided. Coverage row: FIT-F03. Conflicts settled: C-029, C-030.

### FIT-F04 Chase length against the reference games (GTA IV in Mafia DE's place)

- How it works: A measurement, still open: time police chases in GTA V, RDR2 (lawmen), GTA VI footage (no story) and GTA IV (in Mafia DE's place), from start to caught or lost, to check the chase band against what players expect. The 19-chase sheet already gives leads (most 2 to 8 minutes; shortest escapes about 1 minute; floors at 7 to 67 s steps; long chases over-represented). Design pass 4 has dropped the 90 s limit this measurement was meant to test, so it now tests C-02's band (median 60 to 120 s car, 30 to 90 s foot, 90th percentile under 240 s). Five-sample lengths are due in PC block 1 and the feel block (23 to 27 Nov); the row closes in PC block 4, 26 to 28 Nov, about 2 h.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS design pass 3 F04; design pass 4 'The chase against the chase sheet'; FIT-CHECK F04
- Status: pending. Coverage row: FIT-F04. Conflicts settled: C-031.

### DP5-C01 A chase has no timer (car and foot)

- How it works: A chase has no timer, on foot or by car. It ends lost (7 s unseen, or the gap over 200 m by car or 70 m on foot while unseen), caught, wrecked, or at the soft edge, and no chase ends while the pursuer can see Tom except caught, wrecked or at the edge. One patrol car stays, so pressure comes from where he waits and what he knows. The experience rule 'every chase ends within 90 s' becomes 'every chase ends caught, lost, wrecked or at the edge, and none passes 4 real minutes'. No bot's chase may pass 240 s. Decided; his to overturn.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 4 (run 5), the chase Test: B: seeded chase set, lengths logged
- Source: car-chases-sheet-2026-11-21 (leads); g5-heat-samples (SOLID, whole spell); FIT-CHECK F02 to F04, P13 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 4 C-01 and its Standard; car-chases-sheet; g5-heat-samples; FIT-CHECK F02 to F04, P13
- Status: decided. Coverage row: DP5-C01. Conflicts settled: C-032.

### DP5-C02 Chase length on the Hook's loops

- How it works: On the Hook's loops a good-driver bot's lost car chase has a median of 60 to 120 s and a 90th percentile under 240 s (about two and a half laps of the 1,528 m loop); a foot chase has a median of 30 to 90 s. This is below the sheet's 2 to 8 minutes on purpose: those are uploaders' picks at three stars and more on maps many times the Hook. At chase speed (16 to 20 m/s) 2 minutes cover 1.3 to 1.6 laps and 4 minutes 2.5 to 3.1 laps; past about 3 minutes every road has been driven twice. A bot that drives straight and never breaks sight is caught or reaches an edge, never chased past 4 minutes.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 4 (run 5), the chase Test: B: seeded chase set, lengths logged
- Source: car-chases-sheet-2026-11-21 (leads); g5-heat-samples (SOLID, whole spell); FIT-CHECK F02 to F04, P13 (waits on a dated study). Designed in: DEFINITIONS design pass 4 C-02 and Run 5 second pass; car-chases-sheet; g5-heat-samples
- Status: pending. Coverage row: DP5-C02. Conflicts settled: C-033.

### DP5-C03 The search after a chase is lost

- How it works: After a chase is lost the patrol searches the last-seen streets for 30 to 120 real seconds, slowly, lamp on the turnings, then waits on that road for the rest of the night. Seen again inside the search, the same chase resumes with what he already knows; seen after it, a new chase starts. The band is a judgement between the search leads (about 20 s, 50 s, 68 s, once at least 6 minutes) and GTA VI's solid whole wanted spell (about 27 to 122 s, median about 47 s, four of five samples from one player).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 4 (run 5), the chase Test: B: seeded chase set, lengths logged
- Source: car-chases-sheet-2026-11-21 (leads); g5-heat-samples (SOLID, whole spell); FIT-CHECK F02 to F04, P13 (waits on a dated study). Designed in: DEFINITIONS design pass 4 C-03; g5-heat-samples; being-seen sheets
- Status: pending. Coverage row: DP5-C03. Conflicts settled: C-034.

## 1.6 Jobs with the hands

The work itself: getting in, searching, taking, fronting up, minding, getting ready, getting rid.


### 1.6.1 Getting in

- How it works: A lock has several keys: a key lent or copied (Ian Megginson knows every lock on the street), a back way a routine leaves open, or force, which is loud, shows on the door for a day and is a crime. No lockpicking game. In a private place the owner or a neighbour warns, warns again, then calls someone or acts, within half a minute at worst; the warnings reset and the sighting is kept for good. Forbidden places skip the first warning.
- Standard: Several keys to every lock; force is loud, shows for a day and is a crime; a challenge warns twice then acts within half a minute (lead) Test: S: a room entered three ways; force heard at its reach
- Source: DESIGN §4 Break-ins (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §4 Break-ins; DESCRIPTION-COPY-2 §8, §13
- Status: decided. Coverage row: 1.6.1.

### 1.6.2 Searching and taking

- How it works: No search minigame. Search times are a drawer 2 s, a desk 4 s, a wardrobe 5 s; a safe needs its key or combination from a person. Searching makes noise (a drawer about 2 m, a forced cupboard about 10 m at night); in a dark room it takes twice as long without a torch. What is found is authored per job; taking is one press and what is taken can be found on him. A man down can be searched in a few seconds, seen like any act.
- Standard: none yet: search time per container and the noise of searching to be set Test: S: every container searchable, each search timed and heard at its reach; addendum rules ER-SEARCH-01 to 02
- Source: DESIGN §4 (no numbers) (no reference figure yet). Designed in: DESIGN-ADDENDUM A4 (ER-SEARCH-01, -02), A33; DESCRIPTION-COPY-2 §9
- Status: unmeasured. Coverage row: 1.6.2.

### 1.6.3 Lifts and the hot mark

- How it works: Goods carry a hot mark that fades with value and distance, and the owner never forgets them: he recognises his own goods in a shop window. Rita's back room fences from rung 2, refuses or lowballs hot goods, and Wayne's pawn takes goods too. A haggle is three offers at most; the buyer's answers come from his purse, how hot the goods are and how he regards Tom. Notes from a till are hot for a week. The fence's rate is about a third of retail (0.33; 0.2 for jewellery up to 0.4 for a video recorder), from the 1990 research (CLOUD-FIGURES B3).
- Standard: Hot mark fades with value and distance; owner never forgets; fence about 0.33 of retail (CLOUD-FIGURES B3) Test: S: golden rows for the mark; the owner recognises the goods
- Source: DESIGN §4 Lifts (no reference figure yet). Designed in: DESIGN §4 Lifts; DESCRIPTION-COPY-2 §14; DESIGN-ADDENDUM A41; CLOUD-FIGURES B3
- Status: unmeasured. Coverage row: 1.6.3. Conflicts settled: C-035.

### 1.6.4 Fronting up

- How it works: Mickey's debt book has five debts: Darren Milner £22 (pays in what he hears), Wayne Harrison £30 (in goods from the pawn's back room), Lee Drewery £15 (stands, with the docks behind him), Julie Kettlewell £9 (cannot pay) and Dennis Iveson £80 (has the money, a yard and a yard hand). A debtor pays what his purse holds and the rest stays on the book; squeezing or letting go is told on the street. Every pressure has three answers and none ends the game; threats sit at rung 3.
- Standard: Every pressure has three answers (ER-RIV-03); a debtor pays what the purse holds; squeezing or letting go is told on the street Test: S: each debtor's outcomes scripted; H: 'did the five debts feel different?'
- Source: DESIGN §4 Collections (no reference figure yet). Designed in: DESIGN §4 Collections; DESIGN §13 ER-RIV-03; DESCRIPTION-COPY-2 §9
- Status: unmeasured. Coverage row: 1.6.4.

### 1.6.5 Minding and waiting

- How it works: Stand at someone's door, sit in the car, be seen at someone's shoulder. The town records who stood with whom ('Tom and Ron were at the gate' is a sighting), and what minding pays is set in each job. Escorting someone out of danger is minding. Tom on the wall opposite with a cigarette is caught no more than walking. Watching and waiting is under 10% of play (aim 3%).
- Standard: Waiting under 10% of play (ER-CORE-06); watching and waiting 3% of the hour budget (DESIGN, judgement) Test: H: waiting share; S: minding recorded as 'stood with'
- Source: DESIGN §1, §4 (no reference figure yet). Designed in: DESIGN §4 Minding; DESCRIPTION-COPY-2 §13, §8, §34
- Status: unmeasured. Coverage row: 1.6.5.

### 1.6.6 Getting ready

- How it works: At dusk at the office: the dark coat goes on with one key; two things under the coat (a weapon, the envelope, a key, a tool, the torch), one thing in the hand or a holdall, which car, who comes. The rest stays at the office: a locked drawer, the yard shed and the tin. It takes a minute and never a screen. The boot of the cab can hold what is not on him.
- Standard: Two things under the coat; one key for the coat; a minute at most Test: S: loadout limits; H: time spent getting ready
- Source: DESIGN §6, §7 Weapons (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §22; DESIGN §6, §7 Weapons; DESIGN-ADDENDUM A5; GTAVI-MAP GV-01
- Status: unmeasured. Coverage row: 1.6.6.

### 1.6.7 Getting rid of things

- How it works: Weapons can be dropped down a drain; a bag thrown in the dock is gone and remembered by anyone who saw; blood comes off with water and privacy, or at the launderette, which washes the coat and plants a witness. A body can be moved by Tom (dragged at 0.9 m/s, into a boot in 4 s, off the quay edge in 3 s) or by a sent man; a body is never wiped, and one sunk is never found.
- Standard: Blood until washed with water and privacy; the launderette washes a coat and remembers it; a body is never wiped Test: S: washing clears the give-away and plants a witness at the launderette
- Source: DESIGN §2, §7 (DECIDED by the design proof, for him to overturn). Designed in: DESCRIPTION-COPY-2 §22, §9, §7; DESIGN §2, §7, §12; DEFINITIONS RT2-11
- Status: decided. Coverage row: 1.6.7.

### 1.6.8 Using the world

- How it works: Every object a job or story needs is used with the one use key and a prompt naming it (a drawer, the kettle, the radio, the fare book, the tin, a phone box, a bench). The prompt is held 0.2 s before it changes; when two things share a key one prompt asks which, and a person with something to say is offered before a door. A walk-up sweep finds no usable thing without a prompt, and pressing the key 500 times in crowded spots never fires the wrong action.
- Standard: A prompt names what is ahead and in view, held 0.2 s; everything usable has a prompt (ER-INPUT-02) Test: H: walk-up sweep with no prompt faults
- Source: DESIGN §17 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §17 ER-INPUT-02; DESCRIPTION-COPY-2 §6, §3; GTAVI-MAP Y1.8
- Status: decided. Coverage row: 1.6.8.

### 1.6.9 Coat, pockets and office storage

- How it works: Two things under the coat (a weapon, the envelope, a key, a tool, the torch) and one in the hand or a holdall; the rest lives at the office in a locked drawer, the yard shed and the tin. A constable's search finds what is under the coat and in the hand; an office search finds what is stored there; what is stored survives save, load and skipped time. The Ledger's Open list says in words what he carries. The cab's boot also holds the envelope, a spare coat or a box.
- Standard: Two things under the coat; the rest at the office; found in a search (ruling 23 Sep: coat, pockets, cab-office storage) Test: S: a search finds what is carried; office storage keeps across saves; addendum rules ER-POCKET-01 to 02
- Source: ruling 23 Sep genre line; DESIGN §7 (his ruling or canon). Designed in: DESIGN-ADDENDUM A5 (ER-POCKET-01, -02); RULINGS 23 Sep genre line; GTAVI-MAP GV-01
- Status: measured. Coverage row: 1.6.9.

### 1.6.10 Tom's wardrobe

- How it works: Three outfits across the game (as he arrived, a decent jacket, a good overcoat) plus a dark coat for nights, each changing how strangers speak to him and which doors open. A second coat bought after a deed breaks the mark rung for witnesses who saw the first and have not yet told anyone (GV-02); what gossip has carried is never undone; a barber changes the look for a week; a scarf up and a hat down at night break the face rung but are a mark by day. Prices: second-hand coat £15, decent jacket £45, good overcoat £90, barber £4 (to be checked against 1990 sources). Clothes are his to approve in the game's camera.
- Standard: Three outfits across the game each changing how strangers speak and which doors open (DESIGN §14); his to approve in the game's camera Test: S: a change of coat lowers a witness's mark rung; H: strangers greet differently; addendum rules ER-COAT-01
- Source: DESIGN §14; rulings 29 Sep, 3 Oct (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §14; DESIGN-ADDENDUM A21; DESCRIPTION-COPY-2 §26; DEFINITIONS pass 3 §G8; RULINGS 29 Sep, 3 Oct (clothes)
- Status: decided. Coverage row: 1.6.10.

### 1.6.11 Casing a place

- How it works: Casing is a tail on a place: standing a while across the street or sitting in a parked car learns its hours, who holds the key and which way is left open, each written in the Ledger as Tom sees it and matching the town's real routines. It is done close, which is its risk. Hours are windows, not minutes.
- Standard: What is learned goes in the Ledger as a sourced line (ER-LEDG-01); windows, not minutes (DESIGN §4) Test: S: a cased place's hours appear in the Ledger and match the routines; addendum rules ER-CASE-01
- Source: DESIGN §4, §10 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A23; DESCRIPTION-COPY-2 §13; DESIGN §4, §10 ER-LEDG-01
- Status: decided. Coverage row: 1.6.11.

### 1.6.12 A torch on a night job

- How it works: A torch (about £4 at the ironmonger) takes one of the two pockets and is worked with I. Switched on it lights a short cone: a search in a dark room takes its table time with it and twice as long without. A lit torch makes Tom count as lit at 0.7 to anyone with a line of sight to him or the beam, and a beam moving behind a window shows from the street as a precursor. Off, it is a thing in a pocket a constable may find.
- Standard: rule: In the same dark room, a search with the torch takes the table time and without it twice that; a watcher outside the window catches the beam as a precursor only when the torch is on (golden rows). Test: In the same dark room, a search with the torch takes the table time and without it twice that; a watcher outside the window catches the beam as a precursor only when the torch is on (golden rows).
- Source: DESIGN-ADDENDUM-2026-11-20 A33 (from REFERENCE-MECHANICS-2026-11-20 M1.101) (reference game). Designed in: DESIGN-ADDENDUM A33, A4; DESCRIPTION-COPY-2 §3 (Controls); DEFINITIONS pass 3 §G8
- Status: measured. Coverage row: 1.6.12.

### 1.6.13 Lifting from a pocket

- How it works: Beside or behind a person in a crowd, a queue or a packed caff, one held press of about 2 s takes the one thing worth taking (a key, a letter, a wallet). Whether he feels it follows fixed limits, never a roll: an attentive man, good light or fewer than three people near means he feels it; a distracted man in a crowd of three or more in poor light does not. His head turns before he feels it and Tom can stop. Felt, it is a deed with the seven slots and he turns on Tom; a lifted key is missed by morning and he suspects only people he noticed near him.
- Standard: rule: A lift on an attentive person, in good light or with fewer than three people near, is always felt; one on a distracted person in a crowd of three or more in poor light is never felt; his head turns before any felt lift; a lifted key is missed by the next morning and suspicion falls only on people he noticed (golden rows). Test: A lift on an attentive person, in good light or with fewer than three people near, is always felt; one on a distracted person in a crowd of three or more in poor light is never felt; his head turns before any felt lift; a lifted key is missed by the next morning and suspicion falls only on people he noticed (golden rows).
- Source: DESIGN-ADDENDUM-2026-11-20 A34 (from REFERENCE-MECHANICS-2026-11-20 M1.97) (reference game). Designed in: DESIGN-ADDENDUM A34; DESCRIPTION-COPY-2 §14
- Status: measured. Coverage row: 1.6.13.

### 1.6.14 Damage by hand

- How it works: A job or pressure can ask Tom to break a window, windscreen, van light or shop sign himself. It is a loud act heard at the force reach, the damage stays until mended, and the owner reads it as a message from whoever he suspects and knows by morning. It climbs a rival's ladder if aimed at his; sending men to do it is the sent verb.
- Standard: rule: Every damage act is heard at the force reach, leaves a mark that stays until mended, and is known to its owner by morning. Check S. Test: Every damage act is heard at the force reach, leaves a mark that stays until mended, and is known to its owner by morning. Check S.
- Source: DESIGN-ADDENDUM-2026-11-20 A35 (from REFERENCE-MECHANICS-2026-11-20 M3.13) (reference game). Designed in: DESIGN-ADDENDUM A35; DESCRIPTION-COPY-2 §22
- Status: measured. Coverage row: 1.6.14.


### 1.6.15 Hold-ups of shops and people
- How it works: Never in Act I: possible from rung 2 and only through the escalation dial, with a carried weapon (bat, knife) from dial state 0 and with a gun only once a gun has reached Tom through a person. Only places with a till and people with a purse: the six shops of Quay Street, the pawn, the chandlery, the Harbour Office pay window on a Friday, a named adult carrying takings to the bank; never Ada, the priest, anyone sixty or over, and no children anywhere. It starts on the held weapon key with the weapon out (rung 6 of the ladder); the keeper answers by his temper; Tom can wait (the till in about 8 s, to measure), threaten again, or go. The take is what the till holds that hour, hot for a week. Always witnessed at face distance, always reported or told (Rita, Wayne and Hal tell their own people), a robbery (12 hours if taken), DS Ellis up one stage; said to his face within a game day; that shop refuses him for good; at most one a week per street before the shops shut early, never the same place twice; never a game over.
- Standard: ER-HOLDUP-01 to 05: none before rung 2, none with a gun before one reached Tom through a person; every one witnessed at face distance, reported or told within a game hour, said to his face within a game day; the take never above the till and balanced in the flows ledger; Tom in control within 2 real minutes with a Ledger line; nobody under the content rule and no place twice. Test: S: seeded hold-ups, the chain printed; the target list.
- Source: his ruling of 20 Nov (hold-ups: shops and people, rare and late through the dial; loud, witnessed, remembered, heavily punished, never a game over); DESIGN-ADDENDUM A41 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A41; RULINGS 20 Nov.
- Status: decided. Coverage row: none yet (no parts-tree part or coverage.json row; asked of the design proof in BLUEPRINT-11).

### RT2-19 The phone as a verb

- How it works: Phones are the office's (the desk phone and Pauline's line), three phone boxes (by the landing, at the parade's north end, at the dock gate) and some homes' own. A box call costs 10p; 999 is free and an anonymous call brings a constable to the spot that night but never makes an arrest alone. Numbers are Ledger facts, got from a card, being told, the real book, or the directory in the box for businesses. A rival head can be rung only once Tom has the number. Calls are talk and stop the clock as talk does. The office answering machine takes messages and each goes into the Ledger; Garbutt carries a pager and rings a box back within half a game hour; Tom never carries a pager.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-19 Test: B (bot), as written under RT2-19
- Source: design pass 3, RT2-19 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS design pass 3 RT2-19; DESCRIPTION-COPY-2 §16
- Status: decided. Coverage row: RT2-19.

## 1.7 Running the crew

Tom's power is people: orders in the field, sending in Act II, the board.


### 1.7.1 Orders in the field

- How it works: Orders take two inputs at most (a digit, then a target): with me; wait here; watch that; fetch him; take this there; drive; lean on him. Each is answered in voice or body within 1 s, and a man who cannot do it says why. Crew never block a door or a lane and never do what cannot be undone unless told.
- Standard: Two inputs at most, answered in voice or body within 1 s; a man who cannot says why (ER-CREW-01); crew never block a door (ER-CREW-02) Test: S: each order; B: crew never block a lane
- Source: DESIGN §12 (no reference figure yet). Designed in: DESIGN §12 ER-CREW-01, -02, -04; DESCRIPTION-COPY-2 §22
- Status: unmeasured. Coverage row: 1.7.1.

### 1.7.2 Sending (the eight verbs)

- How it works: From Act II, eight verbs, each through a named man: hurt, plan, frame, lean on a witness, move or hide a body, dock or beat one of his own, hit a rival's property, vouch. A send is two inputs, the verb then a target from the Ledger; the man does it on the next night his routine allows, decided by his nerve against the target's, the watchers, light and noise. Every send resolves within two game nights, Tom learns the morning after from the man's own line, and the result runs the same perception and memory as his own deed. A beating is never shown at length, and each send leaves a chain the town can trace.
- Standard: Each through a named person; an order given and a line written; a beating never shown at length (DESIGN §12; canon no cruelty as spectacle) Test: S: each verb leaves a chain the town can trace; accomplice knows
- Source: D56; DESIGN §12 (his ruling or canon). Designed in: DESIGN §12 Orders; DESCRIPTION-COPY-2 §22; DEFINITIONS RT-08, RT-09
- Status: measured. Coverage row: 1.7.2.

### 1.7.3 The board

- How it works: A chalkboard in the office with a line for each car and driver placed by the last radio call, and the week's fares. It puts a car on a rank or a shift; a car on a rank is the firm's eyes there and can give Tom an alibi or a witness. It takes a minute a day at most, and Pauline runs it if he never touches it. The rank outside Mickey's is his; the ferry rank and a second are won by being there with a car on the board enough days.
- Standard: A minute a day at most; Pauline runs it if he never touches it (DESIGN §12) Test: S: placements change sightings; H: minutes spent at the board
- Source: DESIGN §12 The board (no reference figure yet). Designed in: DESIGN §12 The board; DESCRIPTION-COPY-2 §23
- Status: unmeasured. Coverage row: 1.7.3.

### 1.7.4 Men at his side

- How it works: A man at his side follows at about 2 m, waits at doors, rides in the car and stands in a fight, taking the second man, so two against two is fair. He never blocks a door or lane, never lags more than 10 s and never fails a job by being slow. He is a witness the town sees with Tom ('Tom and Ron were at the gate'); with Ron beside him, the two dockers by car two are a fair fight.
- Standard: A follower keeps up or waits and never fails the job (ER-CREW-02); two against one is deadly both ways (DESIGN §7) Test: B: followers never block; S: a fight with Ron at his side goes as the odds say; addendum rules ER-SIDE-01
- Source: DESIGN §7, §12 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A16 (ER-SIDE-01); DESIGN §12 ER-CREW-02; DESCRIPTION-COPY-2 §22, §9
- Status: decided. Coverage row: 1.7.4.

### RT-08 Sending verbs in play

- How it works: A send is given in talk with the man (or by the board's line for him): two inputs, the verb, then a target from the Ledger (a person or place Tom knows). The man does it on the next night his routine allows; the outcome is the man's nerve against the target's, with the watchers, light and noise. Tom learns it the morning after from the man's own line and later from the town's version. Every send resolves within two game nights and leaves a chain the town can trace; the man knows.
- Standard: Every send resolves within two game nights; its result runs the same perception and memory as a deed by Tom; nothing is shown at length. Test: B: each of the eight verbs sent twenty times with seeds; outcomes traced to watchers.
- Source: The description, section 27. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-08; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: RT-08.
