# Authoring source for groups 0 to 3 of the parts tree. P(id, name, what, **fields)
# fields: std, ss (standard's source), des (designed in), tr (track), h ("proto|unreal|basis"),
# rk ("level|why"), t (test), o (owner), f (felt 1/0), n (needs), rn (research item ids)
PARTS = []
def P(i, name, what, **k):
    k.update(id=i, name=name, what=what); PARTS.append(k)

G = "marked guess"
LR = "comparable: a prototype round 0.7 to 2.8 cloud hours (LANE-LOG, ROUND-HOURS)"

P("0", "LEDGER", "The whole game: a 1990 British port-town crime RPG in Unreal 5.8, proved first in a browser prototype.",
  std="The vision is met when most of a panel of eight kinds of player recommend it after a whole evening and a whole week", ss="VISION.md The bar; BUILD-ORDER M1", des="VISION.md; DESIGN.md", tr="both", o="builder", f=0,
  rk="high|scope against a late-2027 release; phase 1 ran 4.9 weeks against 1 to 2 (measured-hours)", t="panel of eight: 6 of 8 thumbs before Unreal multiplies anything (BUILD-ORDER M1)")

# ---------------- GROUP 1 ----------------
P("1", "What the player does with his hands", "The verbs: moving, driving, fighting, being seen, chases, jobs, the crew.", tr="both", o="lane", f=1,
  std="Each child part has its own standard; KCD2 for immersion, GTA for always something to do with the hands", ss="canon pillar 18 Nov; VISION The bar", des="DESIGN §1, §3 to §7, §12")
P("1.1", "Moving on foot", "Walking the town with the camera: the verb under every other verb.", tr="both", o="lane", f=1,
  std="See children", ss="his pick 19 Nov 20:16 (advisor 256): on-foot feel measured like driving", des="DESIGN §17 camera, ER-INPUT-01")
P("1.1.1", "Walk, run and turn", "How Tom starts, stops, turns and runs on keys and pad; weight without lag.",
  std="ER-INPUT-01 (every action answers within 100 ms, eased keys, mouse look never jumps); feel numbers (start, stop, turn rate, run speed) to be measured from reference games", ss="DESIGN §17 ER-INPUT-01; advisor 256", des="DESIGN §17 (input only); feel not designed", tr="both", f=1, o="lane",
  h="2|24|guess; Unreal walk already passed his eye 26 Oct (status-unreal); motion matching tries 1 to 3.5 h each (RECIPE)", rk="high|feel numbers rest on nothing measured yet; the walk slides in Unreal (FINDINGS)", rn=["RN-01"],
  t="feel numbers inside measured bands (input probe); H: 'did moving feel heavy or slippery?'; his eye in Unreal")
P("1.1.2", "On-foot camera follow", "The street camera following Tom as he walks, runs and turns, never inside a wall.",
  std="Between height, 86 degree lens, 3.1 m back, feet in frame; never inside a wall, body or car (ER-CAM-01, ER-CAM-02); follow lag and turn feel to be measured", ss="ruling 28 Oct (camera); DESIGN §17", des="DESIGN §17", tr="both", f=1, o="lane", n=["5.8.1"],
  h="2|17|measured: camera rows 17.2 h in Unreal (time log)", rk="medium|camera gives way to big props only, not vans, lamp posts or people (NOT_DONE round 6)", rn=["RN-01"],
  t="B soak with clip detector; S frames counted for feet in frame; H screenshots in tight rooms")
P("1.1.3", "Doors, stairs and thresholds", "Going through doors, up stairs and into rooms without stalls; no jump.",
  std="Never stuck (ER-CORE-01: moves on within 5 s); in or out of a door in under 2 s; no jump (ruling 23 Sep)", ss="DESIGN §1 ER-CORE-01; ruling 23 Sep", des="DESIGN §1, §6 rooms", tr="both", f=1, o="lane", n=["4.3"],
  h="1|12|guess", rk="medium|doors and stairs are where engines stick characters", t="B: 30 minutes of walking into every door and stair; S: door use timed")
P("1.1.4", "Carrying", "Holding a load (suitcase, holdall, envelope, a box) so it shows on him and changes how he moves and is seen.",
  std="Found is worse than used (load as a tension source); running blocked while carrying in the prototype; how much a load slows to be measured", ss="DESIGN §3 source 3; prototype round 6", des="DESIGN §3, §15 (the carry)", tr="both", f=1, o="lane", n=["1.1.1", "2.2.5"],
  h="1|16|guess", rk="medium|carrying animation and props in hand are a known Unreal cost", rn=["RN-02"],
  t="S: a carried load raises what a witness catches; H: 'could you tell what Tom was carrying?'")
P("1.1.5", "Hiding and keeping out of sight", "Using doorways, shadow, standing still and turning away so fewer people see him; no crouch-walk stealth game.",
  std="Light scale (doorway 0.12, unlit street 0.25) and symmetry (ER-EYES-02); the felt rules to be measured in reference games", ss="DESIGN §2 'In the moment'; ER-EYES-02", des="DESIGN-ADDENDUM-2026-11-20 §A1 (new)", tr="both", f=1, o="lane", n=["2.2.3", "1.4.2"],
  h="2|20|guess", rk="medium|no explicit verb existed before the addendum; risk of a stealth minigame creeping in", rn=["RN-03"],
  t="S: standing still in a doorway lowers what is caught versus walking past; H: 'where would you stand to not be seen?'")
P("1.1.6", "Tailing on foot", "Following a person without being made, to learn a routine.",
  std="none yet: distance bands and the 'made' rule to be measured", ss="DESIGN §4 (tails family, no numbers)", des="DESIGN §4 Tails; DESIGN-ADDENDUM §A2", tr="both", f=1, o="lane", n=["2.1.1", "2.2.3"],
  h="2|24|guess", rk="medium|tail missions are a punished theme when they are slow and fail on distance (PLAYERS punish 5, 9)", rn=["RN-04"],
  t="S: a scripted tail is made at the addendum's rule and never fails on a hidden distance; H: 'did losing him feel fair?'")

P("1.2", "Driving", "The cab and other cars: at AAA quality as the end state, never a driving game.", tr="both", o="lane", f=1,
  std="Driving feel game set M1 to M12 (provisional) until the measured sheet of next week", ss="FEEL-TARGETS-DRIVING-2026-11-17 (c2); rulings 17, 18 Nov", des="DESIGN §5")
P("1.2.1", "Car handling", "Acceleration, braking, steering, grip and sway: the feel of a 1990 car, fun first.",
  std="Game set M1 to M9 (e.g. 0 to 30 mph 3.0 to 4.5 s; dry braking 30 mph 8 to 11 m; steering yaw 63% in 0.15 to 0.25 s); ER-DRIVE-02 on keys", ss="FEEL-TARGETS-DRIVING (c2); DESIGN §5; to be replaced by the measured sheet (DRIVING-MEASUREMENT-METHOD)", des="DESIGN §5; driving study rounds 1 to 3", tr="both", f=1, o="lane", n=["9.9"],
  h="3|60|from comparable: driving study rounds took 5 to 6 Fable hours (advisor 230 relay); Unreal guess", rk="high|AAA bar; current prototype cab tops out at 32 mph with no tail (NOT_DONE)",
  t="S: drives D1 to D8 by keys and pad inside the bands; his feel check")
P("1.2.2", "Car camera", "The chase camera behind the car, widening with speed, never inside anything.",
  std="M10: 5 to 6.5 m back, 1.6 to 2.0 m high, lag 0.1 to 0.25 s, field of view 60 to 65 deg at rest widening to 76 to 86 at 90 mph; ER-DRIVE-06", ss="FEEL-TARGETS-DRIVING (c2) M10; DESIGN §5, §17", des="DESIGN §17", tr="both", f=1, o="lane",
  h="1|10|guess", rk="medium|camera does not widen with speed yet (status-prototype)", t="S: D8 camera run; B: 40-minute soak with no clipped frame")
P("1.2.3", "Getting in and out", "Doors, seats, a blocked door, passengers getting in and out.",
  std="In or out in under 2 s; a blocked door never traps him (ER-DRIVE-07)", ss="DESIGN §5", des="DESIGN §5", tr="both", f=1, o="lane", n=["5.2.3"],
  h="0.5|16|guess; car in-and-out animation is an Unreal cost", rk="low|built and checked in the prototype", t="S: enter and exit timed from both sides, door blocked")
P("1.2.4", "Crashes, damage and unsticking", "Damage in stages by closing speed, a car that will not drive on, never stuck, the firm fetches it.",
  std="M11: fragile like The Getaway (under 5 mph nothing; over 30 to 35 mph may not drive on); ER-DRIVE-01 (moves or can be left within 5 s); ER-DRIVE-08", ss="FEEL-TARGETS-DRIVING M11; DESIGN §5", des="DESIGN §5", tr="both", f=1, o="lane", n=["1.2.1"],
  h="2|30|guess", rk="medium|the prototype cab never stops driving (NOT_DONE round 6)", t="S: pole and wall hits at 10, 20, 35, 50 mph; B: 30 minutes of crashing")
P("1.2.5", "Cars and people", "A car can knock a person down and hurt them badly, never kills; then stop and help or drive off.",
  std="Canon (his pick 18 Nov 22:07): hurts, never kills; only the player's car strikes; the choice put within 2 s (ER-DRIVE-03, ER-DRIVE-04, ER-DRIVE-05, ER-DRIVE-10)", ss="canon content rule; DESIGN §5", des="DESIGN §5", tr="both", f=1, o="lane", n=["2.6.5", "2.15", "1.5.3"],
  h="2|30|guess", rk="high|violence and menace area; the stop-or-drive-off choice is missing in the prototype (NOT_DONE)", t="S: 1,000 seeded crossings with no contact; hits at 5, 15, 30, 50 mph, nobody dies; both choices seeded")
P("1.2.6", "Tailing and being tailed by car", "Following a car without being made; a car in the mirror.",
  std="none yet: following distance and the 'made' rule to be measured", ss="DESIGN §5 wrinkle 'the tail' (no numbers)", des="DESIGN §5 wrinkles; DESIGN-ADDENDUM §A2", tr="both", f=1, o="lane", n=["1.2.1", "4.5"],
  h="2|20|guess", rk="medium|car tails are a commonly punished mission type when fail states are hidden", rn=["RN-04"], t="S: scripted car tail; H: 'did you know how close was too close?'")
P("1.2.7", "Driving with passengers", "Fares and crew in the car; talk while driving; a sit-down in the back seat.",
  std="No fare longer than 2 real minutes without a decision, a person or a sighting (ER-CORE-08); typing never moves Tom (ER-TALK-05)", ss="DESIGN §1, §11", des="DESIGN §5, §11 staging", tr="both", f=1, o="lane", n=["3.6.1"],
  h="1.5|20|guess", rk="medium|talking while driving splits attention; no talk while driving yet (status-prototype)", t="H: fare log; S: a staged back-seat talk with the car moving")

P("1.3", "Fighting", "Fists first, things to hand, carried weapons, guns rare and last; the whole street watches.", tr="both", o="lane", f=1,
  std="Melee sheet C1 to C15 (provisional) until re-measured from footage", ss="FEEL-TARGETS-MELEE-2026-11-18; his combat design 12 Oct; ruling 30 Oct", des="DESIGN §7; game-design/combat-design.md")
P("1.3.1", "Blows and contact", "Strike timing and how contact is sold: freeze, camera close-in, shake, four sound layers.",
  std="ER-FIGHT-01 (timings inside the melee sheet bands C1 to C15): C1 blow starts within 0.1 s; C2 jab 0.25 to 0.40 s to contact, heavy 0.63 to 0.85 s; C3 hit-stop 0.025 to 0.13 s by blow; camera close-in held about 0.8 s", ss="FEEL-TARGETS-MELEE (c); DESIGN §7", des="DESIGN §7 Feel", tr="both", f=1, o="lane", n=["5.5.6"],
  h="2|80|guess; combat 'not yet thrown in Unreal' (risk register)", rk="high|AAA bar; most bands rest on judgement, not measurement (melee sheet 'In short')", rn=["RN-05"],
  t="S: melee drills at 1/60 s inside C1 to C15 (tools/lane/melee_drills.py); his feel check")
P("1.3.2", "Reading and answering blows", "Block and dodge on sight of a readable wind-up.",
  std="Every incoming blow readable 0.45 to 0.80 s before it lands; at most two men swing at once, 0.4 s apart (ER-FIGHT-02)", ss="DESIGN §7; melee sheet", des="DESIGN §7", tr="both", f=1, o="lane", n=["1.3.1"],
  h="1.5|40|guess", rk="high|KCD2 combat was punished as clunky and unexplained (PLAYERS punish 3)", rn=["RN-05"], t="S: drills; H: 'did you see the blow coming?'")
P("1.3.3", "Targeting without lock-on", "Tom hits the man the stick points at, sliding to range in the wind-up.",
  std="ER-FIGHT-06: the man pointed at is the man hit, nobody hit through a wall; slide to about 1 m (lead)", ss="DESIGN §7", des="DESIGN §7", tr="both", f=1, o="lane",
  h="1|24|guess", rk="medium|no lock-on is harder to make feel fair", t="S: targeting script with three men round Tom")
P("1.3.4", "The lower rungs", "Stare, square up, threaten, shove or grab as acts with the seven slots; most confrontations end here.",
  std="Most confrontations end on rungs 1 to 4; each rung an act the town treats like any deed", ss="his combat design 12 Oct; DESIGN §7", des="DESIGN §7", tr="both", f=1, o="lane", n=["2.2.1", "1.3.8"],
  h="1.5|30|guess", rk="medium|needs body language animation that reads at street distance", t="S: each rung exposes seven slots; H: rung reached and why")
P("1.3.5", "The street as a weapon", "Walls, doorways, railings, car bonnets, steps, kerbs and the quay edge as paired moves.",
  std="Seven places first, fitted by height (DESIGN); Sleeping Dogs' environment moves as the reference (melee sheet (a))", ss="DESIGN §7; FEEL-TARGETS-MELEE (a)", des="DESIGN §7", tr="both", f=1, o="lane", n=["1.3.1", "5.2.2"],
  h="2|50|guess", rk="high|paired animations by height cost the most in Unreal; no cruelty as spectacle (canon)", t="S: each of seven places triggers its move; content check: no finisher shown at length")
P("1.3.6", "Things to hand and carried weapons", "Chair, brick, dustbin lid, pipe; cosh, knuckleduster, knife, bat: seen, found, got rid of.",
  std="Breaks after chair 2, brick 3, lid 4 blows, wheel brace never; C2 swing 0.80 to 1.05 s; a weapon drawn cannot be undrawn unseen", ss="DESIGN §7; melee sheet C2", des="DESIGN §7", tr="both", f=1, o="lane", n=["1.3.1", "1.6.6"],
  h="1.5|30|guess", rk="medium|no glass or bottles (content rule)", t="S: breakage counts; a weapon out on a held input only (ER-FIGHT-08); a cosh from behind on an unaware man knocks out and is seen as a strike")
P("1.3.7", "Condition without bars", "Posture, breath, a dropped guard, blood and a limp show a man's state; knock-outs; the fall rule.",
  std="No health bar; fists never kill; only a fall against kerb, wall or step within 3 s of a blow can, rarely (ER-FIGHT-05); knock-out 10 to 30 s", ss="ruling 30 Oct; DESIGN §7; melee sheet", des="DESIGN §7", tr="both", f=1, o="lane", n=["5.2.2", "5.9"],
  h="1|40|guess", rk="high|readability without bars is unproven; blood within canon's light gore", t="S: 10,000 simulated fights, deaths only by the fall rule; H: 'who was winning?'")
P("1.3.8", "Odds, crowds and nerve in a fight", "Two against one is deadly; men stand or give way by nerve; watchers keep their distance.",
  std="Fair one-on-one roughly even; skill beats mashing (patient bot wins most, masher under 3 in 10, ER-FIGHT-07); watchers about 3 m (lead)", ss="DESIGN §7", des="DESIGN §7", tr="both", f=1, o="lane", n=["2.14", "2.5.3"],
  h="1.5|30|guess", rk="medium|nerve needs per-person temper (QUESTIONS 3, open)", t="S: scripted patient and mashing fighters; seeded nerve cases")
P("1.3.9", "How a fight ends", "Back off, run, down, police, people step in; Tom beaten comes round with the cost said.",
  std="A way out at every moment (ER-FIGHT-03); Tom never dies, in control within 60 real s (ER-FIGHT-04); Tom cannot die (his ruling)", ss="DESIGN §7; his rulings", des="DESIGN §7 Death", tr="both", f=1, o="lane", n=["7.9", "4.3.8"],
  h="1|24|guess", rk="medium|Tom beaten must read as a story, not a game over", t="S: each of five endings scripted; beaten route timed")
P("1.3.10", "Firearms", "Rare, late guns: drawing, firing, what a shot does and who hears it.",
  std="Guns rare and late (ruling 18 Nov end state A); AAA when used; shot heard 177 m by day; feel numbers to be measured", ss="RULINGS 28 Oct combat line; DESIGN §7 dial", des="DESIGN §7 Weapons, dial", tr="both", f=1, o="lane", n=["2.13", "1.3.1"],
  h="2|60|guess", rk="medium|late in the game; easy to over-build", rn=["RN-06"], t="S: dial rules; feel numbers inside measured bands once researched")

P("1.4", "Being seen", "The felt side of the town's eyes: the player's three questions answered from picture and sound.", tr="both", o="lane", f=1,
  std="ER-EYES-01: the three questions answered 8 times in 10 from picture and sound alone", ss="DESIGN §2", des="DESIGN §2")
P("1.4.1", "Reading watchers", "Head turns, longer looks, a pause in a walk, a figure at a lit window: a cue before knowing.",
  std="Cue at the start of the 1.2 s to know him, at least 0.8 s before identification (ER-EYES-03); posture first (D29); a window is a watcher only when a figure shows at it (ER-NIGHT-02); reference behaviour to be measured", ss="DESIGN §2; D29", des="DESIGN §2", tr="both", f=1, o="lane", n=["2.2.2", "5.2.6"],
  h="2|40|guess", rk="high|the whole tension engine depends on readable bodies; the felt numbers are LEDGER's own first values", rn=["RN-07"], t="H: the three questions at ten random moments, 8 of 10 right, sound off and light cue off")
P("1.4.2", "Light and dark as cover", "Tom can read how lit he is; dark doorways hide him; the dark is readable, not blind.",
  std="Picture corners follow the rule's light value; Tom and 5 m round him always visible above a brightness floor (ER-NIGHT-01)", ss="DESIGN §2, §6", des="DESIGN §2, §6", tr="both", f=1, o="lane", n=["5.4.2", "6.1.4"],
  h="1|16|guess", rk="medium|exposure one stop darker (ruling 29 Oct) fights readability", rn=["RN-07"], t="H: screenshots at the darkest spots; S: light value matches the cue")
P("1.4.3", "Hearing his own noise", "His own noise mixed by the same number as its reach; a street that has noticed goes quiet.",
  std="ER-SND-01: every noise the rule hears the player hears at the same strength; with picture off a walk is told from a run", ss="DESIGN §17", des="DESIGN §2, §17", tr="both", f=1, o="lane", n=["2.2.4", "5.5.7"],
  h="1|20|guess", rk="medium|sound as information is rare in games and untested", t="H: sound-only test")
P("1.4.4", "Give-aways and the coat", "Coat, blood, dirt, weapon in hand, running, the car: what makes him easier to know, and how he changes it.",
  std="ER-EYES-10: each give-away raises what a witness catches; a deed from the car always names the car", ss="DESIGN §2", des="DESIGN §2 'What gives him away'", tr="both", f=1, o="lane", n=["2.2.5", "1.6.6", "5.1.4"],
  h="1|20|guess", rk="low|rule-driven, golden rows possible", t="S: golden rows, one per give-away")
P("1.4.5", "Reaching the witness", "Catching a witness on the walk to the phone box: talk round, pay, threaten, help, or let go.",
  std="The walk lasts at least 30 real s when it starts in Tom's sight (ER-EYES-04); a threat stops a report, never the talk (ruling 3 Oct)", ss="DESIGN §2; ruling 3 Oct", des="DESIGN §2 'The walk'", tr="both", f=1, o="lane", n=["2.5.1", "2.5.2", "3.6.1"],
  h="2|30|guess", rk="high|the design's 'best minute in the game' is missing in the prototype (status-prototype)", t="S: walk timed; H: 'did you get to her first?'")
P("1.4.6", "Seeing assist", "An optional outline of people Tom can see who are facing him; off by default.",
  std="Never a figure he could not see, never what they know (ER-SCREEN-01)", ss="DESIGN §2, §17", des="DESIGN §2", tr="both", f=1, o="lane", n=["6.1.4"],
  h="0.5|8|guess", rk="low|small and optional", t="S: screen inventory with the assist on")

P("1.5", "Chases", "On foot and by car; every chase ends, caught or lost.", tr="both", o="lane", f=1,
  std="ER-POL-04: a chase ends within 90 real s and can always be lost by breaking sight", ss="DESIGN §8", des="DESIGN §7, §8")
P("1.5.1", "Fleeing on foot", "Running from a constable or men through alleys and yards; lost once unseen 7 s or 70 m.",
  std="Lost once unseen for 7 s or 70 m (DESIGN §8); ends within 90 real s (ER-POL-04); feel to be measured in reference games", ss="DESIGN §8; advisor 256", des="DESIGN §8 The beat", tr="both", f=1, o="lane", n=["1.1.1", "1.5.4", "4.1.2"],
  h="1.5|30|guess", rk="medium|chase feel standards missing until he asked (advisor 257)", rn=["RN-08"], t="S: 50 seeded chases end in 90 s; H: 'how did you lose him?'")
P("1.5.2", "Pursuing on foot", "Chasing a runner fare, a man who ran from a fight, a witness heading for the phone.",
  std="none yet: catch-up speeds and give-up rules to be measured", ss="DESIGN §5 runner wrinkle, §7 'someone runs'", des="DESIGN-ADDENDUM §A3", tr="both", f=1, o="lane", n=["1.1.1", "2.5.1"],
  h="1.5|24|guess", rk="medium|not designed before the addendum", rn=["RN-08"], t="S: a runner can be caught by a direct line and lost by a slow one; ends within 90 s")
P("1.5.3", "Car chases", "A refused stop, a hit-and-run, a rival's car: chased or chasing in the cab.",
  std="Refusing a stop is a chase that ends caught or lost (DESIGN §5); ER-POL-04 and ER-DRIVE-10", ss="DESIGN §5, §8", des="DESIGN §5", tr="both", f=1, o="lane", n=["1.2.1", "4.5", "1.5.4"],
  h="2|40|guess", rk="medium|no car chase in the prototype (status-prototype)", rn=["RN-08"], t="S: seeded car chases end within 90 s; lost by breaking sight")
P("1.5.4", "Pursuers", "How constables, rivals' men and police cars chase, shout, cut corners and give up.",
  std="Police announce themselves 3 s before a challenge (ER-POL-02); give up when sight is broken per 1.5.1", ss="DESIGN §8", des="DESIGN §8", tr="both", f=1, o="town", n=[],
  h="1.5|30|guess", rk="medium|pursuer AI in narrow alleys is a known navigation cost", t="S: pursuer gives up at the rule; never cheats through walls")

P("1.6", "Jobs with the hands", "The work itself: getting in, searching, taking, fronting up, minding, getting ready, getting rid.", tr="both", o="lane", f=1,
  std="Three keys to every lock (ER-JOB-03); failure continues (ER-JOB-05)", ss="DESIGN §4", des="DESIGN §4")
P("1.6.1", "Getting in", "A key lent or copied, a back way a routine leaves open, or force that is loud and shows; no lockpicking game.",
  std="Several keys to every lock; force is loud, shows for a day and is a crime; a challenge warns twice then acts within half a minute (lead)", ss="DESIGN §4 Break-ins", des="DESIGN §4", tr="both", f=1, o="lane", n=["2.1.1", "4.3"],
  h="2|30|guess", rk="medium|break-ins not built in the prototype (status-prototype)", t="S: a room entered three ways; force heard at its reach")
P("1.6.2", "Searching and taking", "Drawers, cupboards, safes, desks: what is found and taken, and the time it takes in a room.",
  std="none yet: search time per container and the noise of searching to be set", ss="DESIGN §4 (no numbers)", des="DESIGN-ADDENDUM §A4", tr="both", f=1, o="lane", n=["1.6.8", "4.4"],
  h="1.5|24|guess", rk="medium|not designed before the addendum; KCD2 pickpocket/lockpick praised when it works (PLAYERS praise 14)", rn=["RN-09"], t="S: every container searchable, each search timed and heard at its reach")
P("1.6.3", "Lifts and the hot mark", "Taking goods; a hot mark that fades with value and distance; the owner never forgets.",
  std="Hot mark fades with value and distance; owner never forgets; fence about 0.4 of honest price (lead)", ss="DESIGN §4 Lifts", des="DESIGN §4", tr="both", f=1, o="lane", n=["2.7.6", "2.3.1"],
  h="1.5|20|guess", rk="low|rule-driven", t="S: golden rows for the mark; the owner recognises the goods")
P("1.6.4", "Fronting up", "Collections and pressure in person: standing over a man, between talk and fists.",
  std="Every pressure has three answers (ER-RIV-03); a debtor pays what the purse holds; squeezing or letting go is told on the street", ss="DESIGN §4 Collections", des="DESIGN §4, §7 lower rungs", tr="both", f=1, o="lane", n=["1.3.4", "2.8.2", "3.6.5"],
  h="1|20|guess", rk="medium|the same debt ladder five times was a round 5 complaint (status-prototype)", t="S: each debtor's outcomes scripted; H: 'did the five debts feel different?'")
P("1.6.5", "Minding and waiting", "Standing at a door, sitting in the car, being seen at someone's shoulder.",
  std="Waiting under 10% of play (ER-CORE-06); watching and waiting 3% of the hour budget (DESIGN, judgement)", ss="DESIGN §1, §4", des="DESIGN §4 Minding", tr="both", f=1, o="lane", n=["7.11", "2.2.1"],
  h="1|12|guess", rk="medium|waiting was 41% in round 5", rn=["RN-10"], t="H: waiting share; S: minding recorded as 'stood with'")
P("1.6.6", "Getting ready", "Coat on, two things in the pockets, which car, who comes: the minute before a job.",
  std="Two things under the coat; one key for the coat; a minute at most", ss="DESIGN §6, §7 Weapons", des="DESIGN §1 evening, §6, §7", tr="both", f=1, o="lane", n=["1.6.9", "1.7.1"],
  h="1|16|guess", rk="low|small", t="S: loadout limits; H: time spent getting ready")
P("1.6.7", "Getting rid of things", "Weapons dumped, blood washed with water and privacy, goods sold or ditched, a body moved.",
  std="Blood until washed with water and privacy; the launderette washes a coat and remembers it; a body is never wiped", ss="DESIGN §2, §7", des="DESIGN §2, §7; body moving as a crew verb (§12)", tr="both", f=1, o="lane", n=["1.4.4", "2.16"],
  h="1.5|24|guess", rk="medium|body handling is violence and menace territory", t="S: washing clears the give-away and plants a witness at the launderette")
P("1.6.8", "Using the world", "Object interaction: the phone box, the office radio and phone, doors, switches, the tin, the board.",
  std="A prompt names what is ahead and in view, held 0.2 s; everything usable has a prompt (ER-INPUT-02)", ss="DESIGN §17", des="DESIGN §17 Screen", tr="both", f=1, o="lane", n=["6.1.1", "5.2.3"],
  h="1|30|guess", rk="low|built in the prototype", t="H: walk-up sweep with no prompt faults")
P("1.6.9", "Coat, pockets and office storage", "What Tom carries and where things are kept: two pockets under the coat, a holdall, storage at the office.",
  std="Two things under the coat; the rest at the office; found in a search (ruling 23 Sep: coat, pockets, cab-office storage)", ss="ruling 23 Sep genre line; DESIGN §7", des="DESIGN §7 Weapons; DESIGN-ADDENDUM §A5", tr="both", f=1, o="lane", n=[],
  h="1|16|guess", rk="low|small, but found by the checklist mapping as a missing part (16 items)", t="S: a search finds what is carried; office storage keeps across saves")

P("1.7", "Running the crew", "Tom's power is people: orders in the field, sending in Act II, the board.", tr="both", o="lane", f=1,
  std="ER-CREW-01 to 04", ss="DESIGN §12", des="DESIGN §12")
P("1.7.1", "Orders in the field", "With me, wait here, watch that, fetch him, take this there, drive, lean on him.",
  std="Two inputs at most, answered in voice or body within 1 s; a man who cannot says why (ER-CREW-01); crew never block a door (ER-CREW-02)", ss="DESIGN §12", des="DESIGN §12 Orders", tr="both", f=1, o="lane", n=["2.11.2", "6.6"],
  h="2|40|guess", rk="medium|companion AI is a punished theme when it blocks or lags (checklist A16)", t="S: each order; B: crew never block a lane")
P("1.7.2", "Sending (the eight verbs)", "D56's owed verbs through named men: hurt, plan, frame, lean on a witness, move a body, discipline, hit property, vouch.",
  std="Each through a named person; an order given and a line written; a beating never shown at length (DESIGN §12; canon no cruelty as spectacle)", ss="D56; DESIGN §12", des="DESIGN §12", tr="both", f=1, o="lane", n=["1.7.1", "2.11.2", "3.5.6"],
  h="3|40|guess", rk="high|violence and menace beyond fists, through others; Act II depends on it", t="S: each verb leaves a chain the town can trace; accomplice knows")
P("1.7.3", "The board", "A chalkboard in the office: cars, drivers, ranks, shifts; a minute a day at most.",
  std="A minute a day at most; Pauline runs it if he never touches it (DESIGN §12)", ss="DESIGN §12 The board", des="DESIGN §12", tr="both", f=1, o="lane", n=["2.15", "6.2"],
  h="1|16|guess", rk="low|management screen creep is the risk (his lesson 8: management on the street)", t="S: placements change sightings; H: minutes spent at the board")

# ---------------- GROUP 2 ----------------
P("2", "The town under the hood", "The engine: routines, perception, memory, gossip, witnesses, police, money, debts, the outfit, rivals, crew, position.", tr="both", o="town", f=0,
  std="Deterministic Core decides every outcome the player feels (canon moat); one simulation shared by prototype and Unreal", ss="canon moat; ruling 18 Nov one simulation", des="DESIGN §2, §8 to §14")
P("2.1", "Routines and the living town", "Everyone keeps a day, with Tom or without him.", tr="both", o="town", f=1,
  std="KCD2: the town runs without him and nothing breaks the spell", ss="VISION The bar; canon", des="DESIGN §2 'The town lives without him'")
P("2.1.1", "Schedules of named people", "Routines with places, each place with a cap and an owner so no doorway jams.",
  std="Places with a cap and an owner (Studies 1, 17); every walk arrives (prototype walk checks)", ss="DESIGN §2; aaa-s01-04", des="DESIGN §2; prototype rules.js schedules", tr="both", f=1, o="town", n=["9.3"],
  h="2|40|guess; a person's routine not measured (measured-hours)", rk="medium|walks near Tom are slow and can outlast their row (NOT_DONE 1)", t="S: walk checks wherever Tom stands; no jammed doorway in a seeded week")
P("2.1.2", "The crowd's clock windows", "Unnamed people by hour, their hours from 1990 research.",
  std="Hours from 1990 research (owed)", ss="DESIGN §2; aaa-s01-05", des="DESIGN §2 (hours owed)", tr="both", f=1, o="town", n=[],
  h="1|40|guess", rk="high|the crowd beyond named people is unpriced (risk R5, draft 7)", rn=["RN-11"], t="S: crowd counts by hour match the researched table")
P("2.1.3", "Off-screen life", "Unseen people go on perceiving, remembering and talking.",
  std="Unseen people keep the same rules as seen ones (DESIGN §2)", ss="DESIGN §2", des="DESIGN §2", tr="both", f=0, o="town", n=["9.3"],
  h="1|24|guess", rk="medium|cost at full town size; Soak runs 7 residents against 41 (status-unreal)", t="S: a seeded week gives the same result watched or unwatched")
P("2.1.4", "Weather and hour change who is out", "Rain empties the street; night thins it; the same way every time.",
  std="ER-NIGHT-03: rain changes who is out, heard and seen, the same way every time", ss="DESIGN §6", des="DESIGN §6", tr="both", f=1, o="town", n=["4.8", "4.7"],
  h="1|16|guess", rk="low|rule-driven", t="S: the same seed dry, drizzle, rain")
P("2.1.5", "Crowd movement and avoidance", "People walk round each other and round Tom, queue, step aside, never clip through.",
  std="none yet: avoidance distances and step-aside timing to be measured; the checklist's civilian behaviour items as acceptance checks", ss="MASTER-CHECKLIST A12, A13 (no numbers)", des="not designed", tr="both", f=1, o="builder", n=["2.1.1", "5.2.5"],
  h="0.5|40|guess", rk="medium|found by the checklist mapping (8 items had no part)", rn=["RN-12"], t="B: 30 minutes walking through crowds, no clipping or jams; H screenshots")

P("2.2", "Perception", "The moat: every act exposes seven slots; identification climbs five rungs.", tr="both", o="town", f=0,
  std="canon moat (unchangeable)", ss="canon The moat", des="DESIGN §2")
P("2.2.1", "Seven slots per act", "Precursor, draw, act, victim, actor, flight, aftermath, each caught or missed.",
  std="Every act exposes seven perceivable slots (canon)", ss="canon The moat", des="DESIGN §2; C# Core", tr="both", f=0, o="town", n=["9.3"],
  h="0|0|exists in the C# Core and port (status-unreal)", rk="low|built and golden-tested", t="S: PerceptionGolden rows")
P("2.2.2", "Identification ladder", "Someone, a shape, a mark, a face, recognition; the top rung needs someone who knows him.",
  std="Five rungs; recognition gated by relationship, never by distance and light alone (canon)", ss="canon The moat", des="DESIGN §2; C# Core", tr="both", f=0, o="town", n=["9.3"],
  h="0|0|exists in Core", rk="low|built and golden-tested", t="S: golden rows")
P("2.2.3", "Sight by distance and light", "Shape at 35 m, mark at 18 m, face at 8 m; light scales it; glance 0.35 s, knowing 1.2 s.",
  std="DESIGN first values (35, 18, 8, 25 m; light 1, 0.7, 0.25, 0.12); ER-EYES-02 symmetry", ss="DESIGN §2 (LEDGER's own first values)", des="DESIGN §2", tr="both", f=1, o="town", n=["9.6"],
  h="0.5|8|guess", rk="medium|first values, not measured against how far people really recognise faces", rn=["RN-07"], t="S: figures at 8, 18, 35 m")
P("2.2.4", "Sound reach", "How far a noise carries by act, hour and rain.",
  std="Footstep at 3 am about 3.6 m; car 44 m by day; shot 177 m by day (DESIGN)", ss="DESIGN §2, §5, §7", des="DESIGN §2", tr="both", f=1, o="town", n=["9.6"],
  h="0.5|8|guess", rk="low|", t="S: reach rows by act, hour and rain")
P("2.2.5", "Give-away rules", "What makes a witness catch more: running, the same coat, blood, dirt, a weapon, wrong clothes, the car, a camera.",
  std="ER-EYES-10", ss="DESIGN §2", des="DESIGN §2", tr="both", f=0, o="town", n=["2.2.1"],
  h="0.5|8|guess", rk="low|", t="S: golden rows per give-away")
P("2.3", "Memory", "Permanent per-person memory.", tr="both", o="town", f=0, std="Nothing is ever wiped (canon)", ss="canon The moat", des="DESIGN §2")
P("2.3.1", "Per-person memory store", "What each person saw, heard and was told, kept for good across saves and skipped time.",
  std="ER-EYES-07: every memory survives save, load and skipped time", ss="canon; DESIGN §2", des="DESIGN §2; C# Core", tr="both", f=0, o="town", n=["9.3", "7.8"],
  h="0|0|exists", rk="low|", t="S: SaveChaos; reload at random moments and compare")
P("2.3.2", "Witness certainty", "A noise or a shape is suspicion, never 'he did it'.",
  std="ER-EYES-06; ruling 30 Sep", ss="ruling 30 Sep; DESIGN §2", des="DESIGN §2", tr="both", f=0, o="town",
  h="0.5|4|guess", rk="low|", t="S: golden rows")
P("2.4", "Gossip", "Talk passing between people who meet; the engine, never the show.", tr="both", o="town", f=1,
  std="Gossip spreads through schedule intersections (canon); not a gossip simulator (his words 18 Nov)", ss="canon", des="DESIGN §2")
P("2.4.1", "Transmission", "Only between people who know each other and meet, within 6 m, weaker with each telling.",
  std="Within 6 m, weaker each telling (the Core's rule); about 0.8 per hop against a 0.2 floor (PLAYERS standards list)", ss="canon; C# Core; map-players", des="DESIGN §2; C# Core", tr="both", f=0, o="town", n=["2.1.1"],
  h="0|0|exists", rk="medium|the packaged gossip regression fails on 23 of 57 nightly runs (status-unreal)", t="S: golden rows; Soak")
P("2.4.2", "Cooling by kind", "A deed stays hot in talk 1 to 7 game days by kind; a body never cools; memory never cools.",
  std="1 to 7 game days by kind (lead), replacing the Core's single 96-hour half-life", ss="DESIGN §2", des="DESIGN §2 (a town task with new golden rows)", tr="both", f=0, o="town", n=["9.3"],
  h="1|8|guess", rk="medium|changes the Core: new golden rows written from DESIGN", t="S: new golden rows")
P("2.4.3", "Showing what people know", "Notice, watch, comment, avoid, refuse, confront: knowledge shown, not displayed.",
  std="The Core's ladder shown in bodies and lines; the rumour study: what was missing was how faintly they showed it", ss="DESIGN §2", des="DESIGN §2", tr="both", f=1, o="lane", n=["5.2.6", "3.6.4"],
  h="1.5|30|guess", rk="high|the 23 Sep rumour study found knowledge shown too faintly", t="H: 'who in the street knew about last night?'")
P("2.4.4", "It comes back", "Every plainly seen deed is said to Tom's face by somebody he has met.",
  std="ER-EYES-08: in week one within one game day; and within the first 30 real minutes at the playing clock (gossip timeliness, map-players S4)", ss="DESIGN §2; PLAYERS second study", des="DESIGN §2", tr="both", f=1, o="lane", n=["2.4.1", "3.6.3"],
  h="1|8|guess", rk="medium|the Unreal clock is 30 real s a game hour, DESIGN and the prototype 45 (C11 open on his page)", t="S: 16 seeded weeks; timeliness at the playing clock")

P("2.5", "Witnesses after a deed", "What people do once they have seen something.", tr="both", o="town", f=1,
  std="ER-EYES-04, ER-EYES-09", ss="DESIGN §2", des="DESIGN §2")
P("2.5.1", "The walk to tell", "A witness who means to tell sets off to a friend, a phone box or the station, and is seen going.",
  std="No mobiles in 1990: the walk is the timer; at least 30 real s in Tom's sight (ER-EYES-04)", ss="canon era; DESIGN §2", des="DESIGN §2", tr="both", f=1, o="town", n=["2.1.1", "4.4"],
  h="1.5|24|guess", rk="high|missing in the prototype; central to tension", t="S: walk timed and visible")
P("2.5.2", "Stopping a witness", "Talked round, paid, threatened, helped or let go; a threat stops a report, never the talk.",
  std="Ruling 3 Oct; ruling 1 Oct (neighbour reports unless on his side or talked round)", ss="rulings 1 and 3 Oct", des="DESIGN §2, §8", tr="both", f=1, o="town", n=["3.6.5"],
  h="1|16|guess", rk="medium|menace through talk; checking model reads lines for a threat (ruling 3 Oct)", t="S: each answer's effect on the report and the talk")
P("2.5.3", "Crowd reaction to a deed", "Near people look, some gather and drift back; witnesses talk quieter for a game hour.",
  std="ER-EYES-09; ruling 23 Sep", ss="ruling 23 Sep", des="DESIGN §2", tr="both", f=1, o="builder", n=["5.2.5"],
  h="1|24|guess", rk="medium|crowd behaviour animation", t="S: after a seen deed, look, gather, quieter talk")

P("2.6", "Police and law", "A pressure Tom can read and answer, never the end of the game.", tr="both", o="town", f=1,
  std="Corruptible as individuals, never as a thesis (canon); ER-POL-01 to 05", ss="canon; DESIGN §8", des="DESIGN §8")
P("2.6.1", "The beat constable", "A constable walks Quay Street and the quay at night and challenges on suspicion.",
  std="Heard or seen 3 s before a challenge; calls out first (ER-POL-02)", ss="DESIGN §8", des="DESIGN §8 (new system needing its place in PLAN.md)", tr="both", f=1, o="town", n=["2.1.1", "1.5.4"],
  h="1.5|30|guess", rk="medium|", t="S and H: the challenge announced")
P("2.6.2", "Challenge and search", "Stand and be searched (what he finds he keeps), or run.",
  std="DESIGN §8: stand and be searched, run and it is a chase", ss="DESIGN §8", des="DESIGN §8", tr="both", f=1, o="lane", n=["1.6.9", "1.5.1"],
  h="1|16|guess", rk="low|", t="S: a search finds what is carried")
P("2.6.3", "Statements and the arrest rule", "Talk brings questions, never an arrest; an arrest needs a named statement or an officer who saw.",
  std="ER-POL-01", ss="DESIGN §8", des="DESIGN §8; C# Core", tr="both", f=0, o="town", n=["2.3.2"],
  h="0.5|8|guess", rk="low|", t="S: golden rows")
P("2.6.4", "Custody as hours", "Hours by deed, the duty solicitor, the coat kept, the street sees him go.",
  std="About 6 h a window, 8 a wounding, 12 a robbery, 22 a killing then bail; under 2 real minutes; never twice for one deed (ER-POL-03)", ss="DESIGN §8 (bail after a killing to be checked)", des="DESIGN §8", tr="both", f=1, o="town", n=["4.3.7"],
  h="1|16|guess", rk="medium|1990 custody figures not yet checked against period research", rn=["RN-13"], t="S: arrest timed")
P("2.6.5", "DS Ellis and the four stages", "Nothing, asking round, investigating, manhunt, each with its sign.",
  std="No stage skipped unseen; a manhunt's sign shows at least one game hour before an arrest (ER-POL-05, provisional on C5)", ss="DESIGN §8; ending signs 30 Sep", des="DESIGN §8", tr="both", f=1, o="town", n=["3.2.1"],
  h="2|24|guess", rk="medium|C5 open on his page", t="S: every route to a manhunt passes its signs")
P("2.6.6", "Armed response and the dial's police", "Armed officers come slowly for gun calls; armed cars and stop and search at War.",
  std="DESIGN §7 dial states", ss="DESIGN §7", des="DESIGN §7", tr="both", f=1, o="town", n=["2.13"],
  h="1|24|guess", rk="low|late game", t="S: three seeded weeks at War")

P("2.7", "Money", "Two pots: clean money in the fare book, night money in the tin.", tr="both", o="town", f=1,
  std="Not an economy game (canon); ER-MONEY-01 to 04", ss="canon; DESIGN §9", des="DESIGN §9")
P("2.7.1", "Clean money and the fare book", "The firm's clean record, spent anywhere.", std="DESIGN §9", ss="DESIGN §9", des="DESIGN §9", tr="both", f=0, o="town", n=["3.4.1"],
  h="0.5|8|guess", rk="low|", t="S: sum of flows")
P("2.7.2", "Night money and the tin", "Money that cannot be explained.", std="DESIGN §9", ss="DESIGN §9", des="DESIGN §9", tr="both", f=0, o="town",
  h="0.5|8|guess", rk="low|", t="S: sum of flows")
P("2.7.3", "The wash", "At the count with Sheila: the fare book can hide £10 plus 80% of fares really driven since the last wash.",
  std="£10 plus 80% of real fares; Sheila warns first (ER-MONEY-04); a twenty-second decision once a day", ss="DESIGN §9 (prototype's rule)", des="DESIGN §9", tr="both", f=1, o="town", n=["2.7.1", "2.7.2"],
  h="1|12|guess", rk="low|", t="S: warning before the books go off")
P("2.7.4", "Rent and running costs", "Friday rent, wages, cars off the road.",
  std="Doing nothing misses Friday's rent; a week of fares alone pays it (ER-MONEY-03); 1990 rent figure owed", ss="DESIGN §9", des="DESIGN §9", tr="both", f=1, o="town",
  h="0.5|8|guess", rk="low|", rn=["RN-13"], t="S: both weeks scripted")
P("2.7.5", "Purses, tills and shops", "People pay only what they hold; shops keep hours, restock weekly, haggle, refuse, remember.",
  std="Purses and a weekly restock stay; no price tables or supply chains (DESIGN §18)", ss="DESIGN §9, §18", des="DESIGN §9", tr="both", f=1, o="town", n=["2.1.1"],
  h="1|16|guess", rk="low|", t="S: a shop refuses and remembers")
P("2.7.6", "Fencing", "Rita's back room buys hot goods at about 0.4 of an honest price.",
  std="About 0.4 (lead; the 1990 rate owed)", ss="DESIGN §4", des="DESIGN §4, §9", tr="both", f=1, o="town", n=[],
  h="0.5|8|guess", rk="low|", rn=["RN-13"], t="S: golden rows")
P("2.7.7", "Flows ledger", "Every pound traced through a sum of flows.", std="ER-MONEY-01", ss="DESIGN §9", des="DESIGN §9", tr="both", f=0, o="town",
  h="0.5|4|guess", rk="low|", t="S: no money from nowhere")
P("2.8", "Debts", "Mickey's debt book.", tr="both", o="town", f=1, std="DESIGN §4", ss="DESIGN §4", des="DESIGN §4")
P("2.8.1", "The five debtors", "Darren £22, Wayne £30, Lee £15, Julie £9, Dennis £80: five debts, five lessons.",
  std="Each debt teaches a different answer (DESIGN §4)", ss="DESIGN §4", des="DESIGN §4; first-week designs", tr="both", f=1, o="town", n=[],
  h="1|8|guess", rk="medium|played as one ladder five times in round 5", t="H: the five debts named as different")
P("2.8.2", "Partial payment and the book", "A debtor pays what his purse holds; squeezing or letting go is told on the street.",
  std="DESIGN §4", ss="DESIGN §4", des="DESIGN §4", tr="both", f=0, o="town", n=["2.7.5", "2.4.1"],
  h="0.5|8|guess", rk="low|", t="S: golden rows")
P("2.9", "The outfit and the arrangement", "The run to the ferry landing that Mickey kept.", tr="both", o="town", f=1, std="DESIGN §16 Act I", ss="DESIGN §16", des="DESIGN §15, §16")
P("2.9.1", "The asks", "Asks on nights one, three, five and seven; the envelope; the cut.",
  std="At most one ask a night, every other night in Act I (DESIGN §6)", ss="DESIGN §6, §16", des="DESIGN §6, §15, §16", tr="both", f=1, o="town", n=["3.5.1"],
  h="1|8|guess", rk="low|", t="S: ask schedule in a seeded week")
P("2.9.2", "Keeping or ending the arrangement", "Keeping brings night money, cover and growing asks; ending brings freedom without cover.",
  std="DESIGN §16 (Act II proposal, judged when built)", ss="DESIGN §16", des="DESIGN §16", tr="both", f=1, o="town", n=["3.1.2"],
  h="1|8|guess", rk="medium|Act II proposal not yet judged", t="S: both branches reach Act II")
P("2.10", "Rivals", "Three heads, each going after a different ledger.", tr="both", o="town", f=1, std="ER-RIV-01 to 03", ss="DESIGN §13", des="DESIGN §13")
P("2.10.1", "Rival ladders", "Noticed, a visit, pressure, a threat, a sit-down; no rung skipped.", std="ER-RIV-02", ss="DESIGN §13", des="DESIGN §13", tr="both", f=1, o="town", n=["3.2.1"],
  h="2|24|guess", rk="medium|Empire and ActTwo not ported (status-unreal)", t="S: no rung skipped, each said or shown")
P("2.10.2", "Rival eyes", "Each knows only what its own people saw or heard.", std="ER-RIV-01", ss="DESIGN §13; Core rule", des="DESIGN §13", tr="both", f=0, o="town", n=["2.4.1"],
  h="1|8|guess", rk="low|", t="S: every rival move traces; ER-EYES-05 no all-knowing town: every reaction by a neighbour, the police or a rival prints its chain of sightings")
P("2.10.3", "Pressures and answers", "The Widow taxes drivers and poaches, Agar sends paper, Cammack brings heat; pay, defy or counter.",
  std="ER-RIV-03: three answers, none ends the game", ss="DESIGN §13", des="DESIGN §13", tr="both", f=1, o="town", n=["3.5.5"],
  h="2|24|guess", rk="medium|", t="S: each pressure's three answers")
P("2.10.4", "The Fixer", "Keith Garbutt sells true reads, a meeting and one truce.", std="DESIGN §13", ss="DESIGN §13", des="DESIGN §13", tr="both", f=1, o="town",
  h="0.5|8|guess", rk="low|", t="S: reads are true to the simulation")
P("2.11", "Crew under the hood", "Men who know: needs, nerve, loyalty, fates.", tr="both", o="town", f=0, std="ER-CREW-03, 04", ss="DESIGN §12", des="DESIGN §12")
P("2.11.1", "Recruiting", "Meet a need (slow, holds) or spend a hook (quick, brittle).", std="DESIGN §12 two roads", ss="DESIGN §12; open-city spec", des="DESIGN §12", tr="both", f=1, o="town", n=["3.2.3"],
  h="1.5|16|guess", rk="medium|", t="S: both roads seeded")
P("2.11.2", "Nerve, loyalty and breaking", "Past his nerve a man talks; the sign comes first.", std="ER-CREW-03", ss="DESIGN §12", des="DESIGN §12", tr="both", f=1, o="town", n=["2.14"],
  h="1|16|guess", rk="medium|needs QUESTIONS 3", t="S: sign before event in every seeded case")
P("2.11.3", "Crew fates", "Poached, frightened, arrested, killed for good.", std="DESIGN §12", ss="DESIGN §12", des="DESIGN §12", tr="both", f=1, o="town", n=["2.10.3", "2.6.3"],
  h="1|16|guess", rk="low|", t="S: each fate reached by script")
P("2.12", "Position in the town", "The rise under the hood: never a number.", tr="both", o="town", f=1, std="ER-RISE-01 to 03", ss="ruling 30 Oct; DESIGN §14", des="DESIGN §14")
P("2.12.1", "The name ladder", "The new owner, Nowak, Tom, Tommy; knowing, not liking; Sheila's exception.",
  std="canon; ER-RISE-02 (heard within a game day, never goes back)", ss="canon premise; ruling 29 Sep", des="DESIGN §14", tr="both", f=1, o="town", n=["3.6.3"],
  h="0.5|8|guess", rk="low|", t="S: each step heard within a day")
P("2.12.2", "Rung table", "What he holds and what opens at each of four rungs.", std="DESIGN §14 table", ss="DESIGN §14", des="DESIGN §14", tr="both", f=1, o="town", n=["2.12.3"],
  h="1|16|guess", rk="medium|Empire not ported", t="S: each rung's holdings and openings")
P("2.12.3", "Access and soft keys", "Standing, dress, an introduction, an appointment the Fixer brokers.", std="DESIGN §14", ss="DESIGN §14", des="DESIGN §14", tr="both", f=1, o="town",
  h="1|16|guess", rk="low|", t="S: each door's keys")
P("2.12.4", "Greetings by regard", "How the rise is heard in the street: afraid, angry, knows and likes him, his appearance, neutral.",
  std="At least 6 lines per situation per kind of speaker (DESIGN §11)", ss="DESIGN §11, §14", des="DESIGN §11", tr="both", f=1, o="town", n=["3.6.4"],
  h="1|16|guess", rk="low|", t="H: same street walked at rung 1 and rung 3 (ER-RISE-03)")
P("2.13", "The escalation dial", "Fists, shown, fired, war: a fact in the town's memory, not a meter.",
  std="ER-FIGHT-08, ER-FIGHT-09 (guns and killing stay rare at every state); falls one step after about two quiet game weeks, never back to 0", ss="ruling 18 Nov; DESIGN §7", des="DESIGN §7", tr="both", f=1, o="town", n=[],
  h="1|16|guess", rk="medium|late game", t="S: dial never moves on an unseen deed; War weeks counted")
P("2.14", "Each person's temper", "Nerve, loyalty and readiness to talk for each named person.",
  std="Recommended answer to QUESTIONS 3: every named person their own, measured before it lands", ss="QUESTIONS 3 (open since 29 Sep)", des="QUESTIONS 3 (recommended)", tr="both", f=0, o="town", n=["9.3"],
  h="1|16|guess", rk="medium|his answer pending", t="S: the same deed goes differently with different people there")
P("2.15", "The firm runs without him", "Kevin drives days, Terry nights; the book fills slowly; the firm's name rises and falls.",
  std="DESIGN §5 'The firm drives without him'; after a drive-off, fares fall for [first value] game days (ER-DRIVE-10)", ss="DESIGN §5", des="DESIGN §5", tr="both", f=1, o="town", n=["3.2.2"],
  h="1|16|guess", rk="low|", t="S: fares counted for a week after a drive-off")
P("2.16", "Death, bodies and the missing", "A killing is permanent and remembered forever; a man who stops keeping his routine becomes the town's question.",
  std="Killing possible, rare, permanent, remembered forever (canon)", ss="canon content rule", des="DESIGN §7 Death", tr="both", f=1, o="town", n=["2.3.1"],
  h="1|24|guess", rk="medium|most of Homicide not ported (status-unreal)", t="S: a missing routine is noticed; a body never cools")

# ---------------- GROUP 3 ----------------
P("3", "Story and people", "One main story with two or three endings, the cast, side stories, fares, jobs, dialogue.", tr="both", o="town", f=1,
  std="One main story, two or three endings (ruling 28 Oct, reaffirmed 19 Nov M8)", ss="RULINGS 28 Oct; advisor 241", des="DESIGN §16")
P("3.1", "The main story", "Three acts: The Inheritance, The Rise and the Squeeze, The Ledger Comes Due.", tr="both", o="town", f=1,
  std="Story praised when characters are worth caring about; punished when predictable or rushed (PLAYERS praise 1, punish 1)", ss="PLAYERS.md", des="DESIGN §16; story outline 28 Sep")
P("3.1.1", "Act I, The Inheritance", "Week one, five threads, Sunday's question: wind it down, take it over, or refuse to say.",
  std="The first week's nine designs stand as written (ruling 29 Sep); M1 5 of 8 for a week", ss="ruling 29 Sep; BUILD-ORDER", des="DESIGN §16; game-design first-week designs", tr="both", f=1, o="town", n=["2.9.1", "2.8.1"],
  h="6|80|guess", rk="medium|the most scripted act; has to hold the week run", t="H: the week run; panel M1")
P("3.1.2", "Act II, The Rise and the Squeeze", "About seven game weeks; beats fire on states; the guaranteed collision; a sit-down with one head.",
  std="Beats fire on states, never on days; 11 to 14 hours", ss="DESIGN §16", des="DESIGN §16 (proposal for the writing)", tr="both", f=1, o="town", n=["2.10.1", "2.12.2", "1.7.2"],
  h="10|200|guess", rk="high|longest act, least designed; ActTwo not ported", t="H: a played stretch of Act II; S: every beat reachable")
P("3.1.3", "Act III, The Ledger Comes Due", "A VAT inspection week: one item each morning, Ellis's trade, a successor's offer.",
  std="Each morning one deciding step graded by what the books hold (DESIGN §16)", ss="DESIGN §16", des="DESIGN §16", tr="both", f=1, o="town", n=["2.7.3", "2.6.5"],
  h="4|60|guess", rk="medium|", t="S: each morning's step graded; H: 'how does this end, and why'")
P("3.1.4", "The endings", "Two or three states (the Kingdom, the Straight Life, Burn Both), each with a better and a plainer way.",
  std="Two or three endings (ruling 28 Oct, his pick M8 19 Nov); ending states never picked from a list; no single beat fails the run", ss="RULINGS; advisor 241 point 8", des="DESIGN §16 (three shown, five kept underneath)", tr="both", f=1, o="town", n=["3.1.3", "3.1.5"],
  h="2|40|guess", rk="medium|ActThree.cs has five; amend to fit (his ruling, a list item in the 23 Nov order)", t="S: every ending by a scripted route, including hunted (ER-END-01)")
P("3.1.5", "Ending signs and Tom's reading", "Every cost that decides the ending shows its sign before it decides.",
  std="ER-END-02, ER-END-03; D58; ending signs 30 Sep", ss="DESIGN §16", des="DESIGN §16", tr="both", f=1, o="town", n=["6.2.5"],
  h="2|24|guess", rk="medium|", t="S: balance sweep; H predicts the ending")
P("3.1.6", "Mickey's past", "The real book, the warehouse fire and its street version; the truth is never the street's.",
  std="Ruling 30 Sep (Mickey's death and the fire)", ss="ruling 30 Sep", des="DESIGN §16; story outline", tr="both", f=1, o="town",
  h="2|24|guess", rk="low|", t="S: the street version stays a street fact")
P("3.2", "The cast", "Named people.", tr="both", o="town", f=1, std="canon cast; casting sheets", ss="canon; ruling 25 Sep", des="DESIGN §16 cast")
P("3.2.1", "Principals", "Sheila, Ron, Darren, Ada, June, Father Walsh, Alison, Danby, Ellis, Agar, Jensen, Cammack, Garbutt.",
  std="Casting sheets approved as text (25 Sep); faces frozen for Ron, Sheila, Darren, Tom", ss="RULINGS faces line; canon", des="canon; casting sheets; DESIGN §16", tr="both", f=1, o="town", n=["5.1.1", "5.6.1"],
  h="4|300|guess; a whole person not yet measured", rk="high|a complete person's cost unmeasured (risk register)", t="his eye on each whole person; H: talk transcripts")
P("3.2.2", "The firm's people", "Pauline on the radio, Kevin and Terry driving.", std="the thirty regulars as written", ss="ruling 30 Sep", des="DESIGN §5, §12", tr="both", f=1, o="town", n=["3.2.3"],
  h="1|60|guess", rk="low|", t="S: the firm runs; H: Pauline's directions")
P("3.2.3", "The thirty regulars", "The cards as written, each with a routine and own lines.", std="Thirty regulars stand as written (ruling 30 Sep); about 30 own street lines each", ss="ruling 30 Sep; DESIGN §11", des="regular cards; DESIGN §11", tr="both", f=1, o="town", n=["2.1.1", "3.6.3"],
  h="4|300|guess", rk="medium|", t="H: transcripts; S: line counts")
P("3.2.4", "The crowd", "Unnamed townspeople, adults only, by hour.", std="No children anywhere (canon); 6 of 13 street figures have a resident behind them (map-players)", ss="canon; PLAYERS second study", des="DESIGN §2", tr="both", f=1, o="town", n=["2.1.2"],
  h="1|80|guess", rk="high|unpriced (risk R5)", t="S: crowd generation content check; counts by hour")
P("3.2.5", "Someone worth being honest for", "Alison Sedman or Philip Danby: one friendship that can hold.",
  std="One of Act I's five threads; Danby is never seen at work (the school stands closed)", ss="DESIGN §16; canon", des="DESIGN §16 (Danby still to write)", tr="both", f=1, o="town", n=["3.1.1"],
  h="2|40|guess", rk="medium|Danby still to write in the outline", t="S: the friendship reaches its ending state")
P("3.2.6", "One complete person", "The assembled unit: face, body, hair, clothes, voice, routine, lines, memory, measured as one cost.",
  std="Nothing multiplied before he approves one complete sample in the assembled game (CLAUDE.md)", ss="CLAUDE.md; Kiln plan; risk register", des="KILN-TO-GAME-PLAN (Ron as one complete person, n16-2)", tr="unreal", f=1, o="builder", n=["5.1.1", "5.1.4", "5.6.1", "2.1.1"],
  h="0|60|guess; never measured", rk="high|cost unmeasured; drives the whole cast's budget", t="his eye in the packaged game")
P("3.3", "Side stories", "25 to 40 found on foot, no markers, each 3 to 5 steps, ending in something the town knows.",
  std="25 to 40; whole stories, not errands (PLAYERS praise 5); the 32 drafts of 8 Nov", ss="DESIGN §4; Study 17", des="DESIGN §4; drafts of 8 Nov", tr="both", f=1, o="town", n=["3.5.6"],
  h="8|200|guess", rk="medium|authored breadth at scale", t="H: found unaided; S: each ends in a town fact")
P("3.4", "Fares", "Few and chosen, each a person with something going on, feeding the crime; never a taxi sim.", tr="both", o="town", f=1,
  std="His OK 19 Nov: few and chosen, a person each, feeding the crime, no taxi-sim parts; prototype question until fares stay fresh over a week", ss="advisor 241 point 10, 242 point 2; canon", des="DESIGN §5")
P("3.4.1", "Fare people", "Named passengers going where their routine takes them at that hour.",
  std="1 to 2 real minutes; 80p plus distance; drawn from routines (DESIGN §5)", ss="DESIGN §5", des="DESIGN §5", tr="both", f=1, o="town", n=["2.1.1", "1.2.7"],
  h="2|60|guess", rk="high|fares are random errands with generic passengers today (status-prototype); taxi-sim risk", t="H: fare freshness over a week; ER-CORE-08")
P("3.4.2", "Wrinkles", "The talker, the parcel, the tail, the runner, the wait, the hurry, the face.",
  std="About half of Act I's fares carry one; no wrinkle twice running (ER-JOB-06)", ss="DESIGN §5, §4", des="DESIGN §5", tr="both", f=1, o="town", n=["3.4.1"],
  h="2|40|guess", rk="high|without wrinkles fares are the grind he warned against", t="H: the log; S: no repeat twice running")
P("3.4.3", "Pauline and the radio", "Directions by landmark, repeated on a key; nothing said on it is private.",
  std="ER-DRIVE-09: always right, repeated on a key", ss="DESIGN §5; canon (radio)", des="DESIGN §5", tr="both", f=1, o="town", n=["4.1.3", "5.6.1"],
  h="1|24|guess", rk="low|", t="S: a scripted driver follows each fare's words alone")
P("3.5", "Job content", "The authored jobs.", tr="both", o="town", f=1, std="Authored, never rolled (ruling 13 Nov); ER-JOB-01 to 07", ss="ruling 13 Nov; DESIGN §4", des="DESIGN §4")
P("3.5.1", "Carries", "The envelope to the landing first, then later carries.", std="Three routes: lit quay quick and seen, dark yard slower, cab quickest and known", ss="DESIGN §15", des="DESIGN §4, §15", tr="both", f=1, o="town", n=["1.1.4", "3.5.6"],
  h="2|24|guess", rk="low|built shallow in the prototype", t="S: three routes each finish; H retellable")
P("3.5.2", "Collections", "The five debts and later ones.", std="DESIGN §4", ss="DESIGN §4", des="DESIGN §4", tr="both", f=1, o="town", n=["2.8.1", "1.6.4"],
  h="1|24|guess", rk="low|", t="S: every outcome scripted")
P("3.5.3", "Break-in sites", "Rooms labelled by privacy with a night rule, each with its keys.", std="DESIGN §4 Break-ins", ss="DESIGN §4", des="DESIGN §4", tr="both", f=1, o="town", n=["1.6.1", "4.3"],
  h="2|40|guess", rk="medium|", t="S: each site entered three ways")
P("3.5.4", "Tails, minding and lifts content", "Authored instances of the smaller families.", std="DESIGN §4", ss="DESIGN §4", des="DESIGN §4", tr="both", f=1, o="town", n=["1.1.6", "1.6.5", "1.6.3"],
  h="2|40|guess", rk="medium|", t="S: each instance's outcomes")
P("3.5.5", "Sit-downs", "The steps that decide an act, in talk; can be in the back of his own cab.", std="Accept, defy, counter (DESIGN §16)", ss="DESIGN §11, §13, §16", des="DESIGN §11, §16", tr="both", f=1, o="town", n=["3.6.1", "3.6.5"],
  h="2|40|guess", rk="medium|", t="S: three answers each")
P("3.5.6", "Job template and step states", "A job as a small graph of saved states: windows, landmarks, outcomes, a Ledger line per step, a tester's skip.",
  std="Four job states and five step states; every step's place by landmark, two sources of direction, a skip (DESIGN §4; ER-JOB-02, 05, 07)", ss="DESIGN §4; Studies 11, 16", des="DESIGN §4", tr="both", f=0, o="lane", n=["7.8"],
  h="2|30|guess", rk="medium|found by the studies gap check as having no part", t="S: job data checks; every outcome reached by script")
P("3.6", "Dialogue", "Talk content and its system; the moat, never the main thing.", tr="both", o="town", f=1, std="ER-TALK-01 to 07", ss="DESIGN §11", des="DESIGN §11")
P("3.6.1", "Live talk", "Any named person can be spoken to live; a short thinking sound; brush-off when slow.",
  std="Reply within 2 s or the written line plays; slower than 8 s dropped (ER-TALK-01); median first speech 2 s or less", ss="DESIGN §11; RULINGS speech line", des="DESIGN §11; talk system in C#", tr="both", f=1, o="town", n=["8.6", "3.6.2", "9.8"],
  h="2|40|comparable: talk feature 1.5 to 2.8 h (measured-hours)", rk="high|risk R1 and R2: talk empty or slow", t="S: slow stand-in; packaged speech measure")
P("3.6.2", "Claim check", "A character says only what the simulation knows; a sentence naming a fact the speaker lacks is refused.",
  std="ER-TALK-04; ruling 25 Sep; speech rulings 7 to 28 Oct", ss="RULINGS; DESIGN §11", des="DESIGN §11", tr="both", f=0, o="town", n=["2.3.1"],
  h="1|16|comparable: fast checker about 11 h over four tries", rk="medium|", t="S: planted bad replies")
P("3.6.3", "Written street lines", "Own lines for Ron, Darren, Walsh, June; shared for Sheila, Alison, Ada; at most every 45 s.",
  std="About 30 own lines a regular; a person's own line once a day, a shared line once a week per street (ER-TALK-02)", ss="RULINGS street lines; DESIGN §11", des="DESIGN §11", tr="both", f=1, o="town", n=[],
  h="2|60|guess", rk="low|", t="H: transcripts")
P("3.6.4", "Crowd lines by situation", "Greetings by regard, bumping, neighbours, talking to oneself at work, rain.",
  std="At least 6 lines per situation per kind of speaker (DESIGN §11)", ss="DESIGN §11", des="DESIGN §11", tr="both", f=1, o="town", n=["3.2.4"],
  h="1|40|guess", rk="low|", t="S: line counts; content gate")
P("3.6.5", "Decision lines", "The game's own yes, no and a line that keeps talking; only a plain yes; asked twice if permanent.",
  std="ER-TALK-03; ER-CORE-03", ss="DESIGN §11", des="DESIGN §11", tr="both", f=1, o="lane", n=["6.7"],
  h="1|16|guess", rk="low|", t="S: 170 lines that are not a plain yes")
P("3.6.6", "Suggested lines", "Tab on a keyboard, shown at once on a controller; Mixed sourcing.", std="Ruling 1 Oct", ss="RULINGS 1 Oct", des="DESIGN §11", tr="both", f=1, o="lane", n=["6.7"],
  h="0.5|8|guess", rk="low|", t="S: shown on both devices")
P("3.6.7", "AI notice and line report", "The AI notice once before the first talk; any live line reported from pause or a key.",
  std="ER-TALK-07; ruling 24 Sep", ss="RULINGS 24 Sep", des="DESIGN §11", tr="both", f=0, o="lane", n=["6.4", "10.2"],
  h="0.5|8|guess", rk="medium|required before outsiders play", t="S: report filed from talk and from pause")
