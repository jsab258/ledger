# Parts added from the red team (Fable and Opus) and the reference-mechanics check, 19-20 Nov.
from tree_a import P
AD = "DESIGN-ADDENDUM-2026-11-20 "
RT = "found by the red team"
# group 1
P("1.1.7", "Stopping and blending in", "Sit on a bench or wall, lean in a doorway, light a cigarette, wait at a bus stop: standing still without looking suspicious.",
  std="A stopped Tom draws less notice than a loiterer; tobacco allowed (canon); waiting under 10% of play (ER-CORE-06)", ss="canon content rule; DESIGN §1", des=AD + "§A10", tr="both", f=1, o="lane", n=["1.1.1"],
  h="1|30|guess", rk="low|" + RT, t="S: a seated or smoking Tom is caught less than one standing about; H: minding feels like play")
P("1.1.8", "Vaulting low walls and fences", "A context vault over low walls, yard fences and bins at set places; no jump key.",
  std="Recommended answer to QUESTIONS-FOR-JAFAR-2026-11-20 Q1, built to it meanwhile; never a jump (ruling 23 Sep); vault speed and heights to be measured", ss="ruling 23 Sep; Q1 (open)", des=AD + "§A26 (to the recommended answer)", tr="both", f=1, o="lane", n=["1.1.1"],
  h="1|40|guess", rk="medium|his ruling's edge; " + RT + " and the mechanics check", rn=["RN-08"], t="S: each vault point works in a chase; no vault anywhere else")
P("1.2.8", "Riding as a passenger", "Kevin, Terry or a crewman drives Tom; the ride can be skipped as passed time.",
  std="A crewman told to drive is an AI driver and always brakes for people (DESIGN §12); a skipped ride costs its real time on the clock", ss="DESIGN §12; canon", des=AD + "§A24", tr="both", f=1, o="lane", n=["1.7.1", "4.5.1"],
  h="1|24|guess", rk="low|" + RT, t="S: a ride arrives; skip advances the clock by the drive's time")
P("1.2.9", "Repairs, plates and paint", "The firm fetches and mends a wrecked cab; Shaun Hewson's paint makes a cab not look like a cab; plates are what witnesses note.",
  std="A dead car is off the road a day (DESIGN §5); no fuel or wear (DESIGN §18)", ss="DESIGN §5, §12, §18", des=AD + "§A24", tr="both", f=1, o="lane", n=["1.2.4"],
  h="0.5|16|guess", rk="low|" + RT, t="S: a repainted car is not named as the firm's by a witness who saw the old paint")
P("1.2.10", "Taking a parked car", "Getting into a car that is not his by force (a window, a tool), loud, no minigame; the owner reports it.",
  std="Recommended answer to Q2, built to it meanwhile; no lockpicking game (DESIGN §18); never a moving car", ss="Q2 (open)", des=AD + "§A27 (to the recommended answer)", tr="both", f=1, o="lane", n=["1.6.1", "4.5.2"],
  h="1|30|guess", rk="medium|scope is his; " + RT + " and the mechanics check", t="S: a taken car is reported and named; force heard at its reach")
P("1.3.11", "Marks that last", "Bruises, a cut lip and a limp stay on a beaten Tom for days; others see them; a doctor who asks no questions.",
  std="Condition shows in the body, never a bar (DESIGN §7); a mark is a give-away (DESIGN §2)", ss="DESIGN §2, §7", des=AD + "§A21", tr="both", f=1, o="lane", n=["1.3.7"],
  h="0.5|24|guess", rk="low|" + RT, t="S: a marked Tom is caught more; marks fade on the clock")
P("1.4.7", "Street manners", "A nod, a greeting, a hard look, a shove on one key: the smallest acts, answered by the person.",
  std="Answered in body or voice within 1 s; each is an act with the seven slots (canon moat)", ss="canon; DESIGN §7 lower rungs", des=AD + "§A10", tr="both", f=1, o="lane", n=["1.3.4", "2.12.4"],
  h="1|30|guess", rk="low|" + RT, t="S: each gesture answered within 1 s and remembered")
P("1.4.8", "Drawing a watcher away", "A noise or a thrown thing turns a watcher's head or moves him off a door.",
  std="Uses the sound reach rule (DESIGN §2); a watcher drawn away remembers the noise", ss="DESIGN §2", des=AD + "§A23", tr="both", f=1, o="lane", n=["2.2.4"],
  h="0.5|16|guess", rk="low|found by the mechanics check", t="S: a noise inside reach turns a head; outside reach does nothing")
P("1.6.10", "Tom's wardrobe", "Buying and changing clothes: the three outfits of the rise, the dark coat, a second coat after a deed, a barber.",
  std="Three outfits across the game each changing how strangers speak and which doors open (DESIGN §14); his to approve in the game's camera", ss="DESIGN §14; rulings 29 Sep, 3 Oct", des="DESIGN §14; " + AD + "§A21", tr="both", f=1, o="lane", n=["1.4.4", "5.1.4"],
  h="1|24|guess", rk="medium|clothes are Kiln's slowest pipeline", t="S: a change of coat lowers a witness's mark rung; H: strangers greet differently")
P("1.6.11", "Casing a place", "Watching a place by day to learn its hours, who keeps the key, which way is left open.",
  std="What is learned goes in the Ledger as a sourced line (ER-LEDG-01); windows, not minutes (DESIGN §4)", ss="DESIGN §4, §10", des=AD + "§A23", tr="both", f=1, o="lane", n=["1.1.6", "6.2.3"],
  h="1|20|guess", rk="medium|" + RT, t="S: a cased place's hours appear in the Ledger and match the routines")
P("1.7.4", "Men at his side", "Crew who follow, ride along and stand in a fight with him, without blocking doors.",
  std="A follower keeps up or waits and never fails the job (ER-CREW-02); two against one is deadly both ways (DESIGN §7)", ss="DESIGN §7, §12", des=AD + "§A16", tr="both", f=1, o="lane", n=["1.7.1", "1.3.8"],
  h="2|60|guess", rk="medium|companion AI cost; " + RT, t="B: followers never block; S: a fight with Ron at his side goes as the odds say")
# group 2
P("2.1.6", "The town's calendar", "Market day, Saturday's match, Sunday, and two dated days in the window (Bonfire Night with adults only, Remembrance Sunday).",
  std="No real people or events spoken of (canon: no real people); no children (canon)", ss="canon", des=AD + "§A20", tr="both", f=1, o="town", n=["2.1.1"],
  h="1|40|guess", rk="medium|Bonfire Night against no children; " + RT, t="S: routines change on the calendar days; content gate")
P("2.2.6", "Ground rules and trespass", "Whose ground it is (public, shop hours, private, forbidden) and the warnings given.",
  std="Rooms labelled by privacy with a night rule; a challenge warns, warns again, then acts within half a minute (DESIGN §4)", ss="DESIGN §4", des="DESIGN §4; " + AD + "§A10", tr="both", f=1, o="town", n=["2.2.1"],
  h="1|16|guess", rk="low|" + RT, t="S: every place has a label and the warnings fire in order")
P("2.4.5", "The paper and the news", "Alison Sedman's stories in the local paper: what she knows, printed; read in the caff and talked about.",
  std="The press works only through a person, Alison (D56); a story prints only what she knows (canon moat)", ss="D56; DESIGN §11", des=AD + "§A19", tr="both", f=1, o="town", n=["3.2.1"],
  h="1|24|guess", rk="medium|the paper's name is owed by the brand bible; " + RT, t="S: every printed line traces to what Alison was told or saw")
P("2.6.7", "Traffic police and stops", "A patrol car; reckless driving in its sight starts a stop; the plate is noted.",
  std="Reckless driving in a police car's sight starts a stop; refusing it is a chase (DESIGN §5); no fines as a system (DESIGN §18)", ss="DESIGN §5, §18", des="DESIGN §5; " + AD + "§A12", tr="both", f=1, o="town", n=["4.5.1", "1.5.3"],
  h="1|24|guess", rk="medium|" + RT, t="S: a stop starts only on reckless driving in sight; ends within 2 minutes")
P("2.6.8", "Bought men and squaring the law", "A named officer who can be paid or leaned on; never the force as a whole.",
  std="Police corruptible as individuals, never as a thesis (canon)", ss="canon", des=AD + "§A13", tr="both", f=1, o="town", n=["2.6.5", "2.7.2"],
  h="1|24|guess", rk="medium|menace; " + RT + " and the mechanics check", t="S: one bought officer, his limits; the rest of the station unchanged")
P("2.6.9", "Charges, bail and the office searched", "A charge joins Ellis's case and the endings; bail; at the investigating stage, one search of the office.",
  std="An arrest is hours, a caution, or a charge and bail; no prison terms (DESIGN §8, §18)", ss="DESIGN §8, §18", des=AD + "§A13", tr="both", f=1, o="town", n=["2.6.4", "1.6.9"],
  h="1|24|guess", rk="medium|" + RT, t="S: a charge reaches the endings; a search finds what is stored at the office")
P("2.7.8", "Spending", "What money buys and where: tobacco, food at the caff, tools at the ironmonger, clothes, a solicitor, a bribe, a car.",
  std="What money buys is position (DESIGN §9); purses and weekly restock, no price tables (DESIGN §18)", ss="DESIGN §9, §18", des=AD + "§A21", tr="both", f=1, o="town", n=["2.7.5"],
  h="1|24|guess", rk="medium|£23.50 only bites if money has uses; " + RT, t="S: each shop sells its list; H: 'what did you spend on?'")
P("2.12.5", "Property that reacts", "The office fills, the flat stops being Mickey's, a lock-up, a second phone line.",
  std="Each rung changes three things a newcomer can point to (ER-RISE-03)", ss="DESIGN §14", des="DESIGN §14", tr="both", f=1, o="lane", n=["2.12.2"],
  h="1|40|guess", rk="low|found by the mechanics check", t="H: office at rung 1 and rung 3 compared")
P("2.15.1", "Fleet and drivers", "Buying a car, hiring and losing drivers, shifts on the board.",
  std="Two cars and two drivers at rung 1, five cars at rung 3 (DESIGN §14)", ss="DESIGN §14", des="DESIGN §12, §14; " + AD + "§A14", tr="both", f=1, o="town", n=["1.7.3", "2.7.8"],
  h="1|24|guess", rk="medium|management creep; " + RT, t="S: a bought car joins the board and the ranks")
P("2.15.2", "Ranks and accounts", "Winning a rank, the cold-store shift contract, regular customers.",
  std="The cold-store contract is the daily loop that earns and explains money (DESIGN §14)", ss="DESIGN §14", des="DESIGN §14; " + AD + "§A14", tr="both", f=1, o="town", n=["2.15.1"],
  h="1|24|guess", rk="medium|" + RT, t="S: an account adds fares to the book")
P("2.15.3", "Other firms on the ranks", "The other minicab firm people ring after a hit-and-run; a presence, not a fourth rival.",
  std="'People ring another firm for a while' (DESIGN §5); the three rivals stay three (canon)", ss="DESIGN §5; canon", des=AD + "§A14", tr="both", f=1, o="town", n=["2.15"],
  h="0.5|16|guess", rk="low|" + RT, t="S: fares move to the other firm after a drive-off and come back")
P("2.17", "Fronts and rackets held", "Taking a share of a business, putting a man in, money and trouble coming back; run through people, never sliders.",
  std="A first front and a first round at rung 3 (DESIGN §14); empire as management on the street (his lesson 8); not an economy game (canon)", ss="DESIGN §14; canon", des="DESIGN §14; " + AD + "§A15", tr="both", f=1, o="town", n=["2.12.2", "2.11.1"],
  h="2|60|guess", rk="high|Act II rests on it; " + RT + " (both)", t="S: a front pays through its man; trouble at it reaches Tom through people")
P("2.18", "Ambulance and the hospital", "Someone hurt is taken to hospital after a call from the phone box; stopping to help means making that call.",
  std="Stop and help costs minutes and puts his face beside the cab (DESIGN §5)", ss="DESIGN §5", des=AD + "§A22", tr="both", f=1, o="town", n=["2.5.1", "4.3.8"],
  h="1|24|guess", rk="low|" + RT, t="S: an ambulance arrives after a call within its set time")
P("2.19", "Lasting marks on the town", "A forced door shows for a day; glass stays broken until mended; his cars on the ranks; things stay where they were left.",
  std="Force shows on the door for a day (DESIGN §4); nothing is ever wiped (canon)", ss="DESIGN §4; canon", des="DESIGN §4", tr="both", f=1, o="builder", n=["2.3.1"],
  h="1|30|guess", rk="medium|" + RT, t="S: marks persist across save and load for their set time")
# group 3
P("3.5.7", "How jobs reach him", "Callers at the office, the phone, a message left with Sheila or Pauline, a man waiting by the car.",
  std="A job is offered by a person, on a state, never by a marker or the clock alone (DESIGN §4 law 1)", ss="DESIGN §4", des=AD + "§A17", tr="both", f=1, o="town", n=["3.5.6"],
  h="1|16|guess", rk="medium|" + RT, t="S: every job has a giver and a channel; H: 'how did you hear of it?'")
P("3.6.8", "How the player speaks", "Typing on a keyboard, suggested lines on a pad, whether Tom is heard aloud.",
  std="Suggested lines on Tab, shown at once on a controller (ruling 1 Oct); Tom's written lines approved; no voice for Tom without his yes (24 Sep)", ss="RULINGS 1 Oct, 24 Sep", des=AD + "§A25", tr="both", f=1, o="lane", n=["6.7"],
  h="0.5|16|guess", rk="medium|a pad cannot type (NOT_DONE); " + RT, t="S: a whole talk by pad alone")
P("3.7", "Street happenings", "Small authored incidents placed on the clock and the town's state: a row on the pavement, a breakdown, a shoplifter, a lost tourist.",
  std="Authored, each with a spec and a check, never rolled at random (ruling 13 Nov; DESIGN §18 cuts random encounters); no set piece twice in 30 minutes (ER-JOB-06)", ss="ruling 13 Nov; DESIGN §4, §18", des=AD + "§A18", tr="both", f=1, o="town", n=["3.5.6"],
  h="3|80|guess", rk="medium|must stay authored, not random; " + RT + " (both)", t="S: placement by state; H: empty minutes fall")
# group 4, 5
P("4.2.4", "The water's edge", "Quay edges, ladders, the dock water: Tom never walks in; a man knocked in climbs out at a ladder.",
  std="Never stuck (ER-CORE-01); Tom cannot die (his ruling); water never kills", ss="DESIGN §1; his rulings", des=AD + "§A11", tr="both", f=1, o="lane", n=["4.2.1"],
  h="0.5|24|guess", rk="medium|a port makes it certain on night one; " + RT + " (both)", t="B: 30 minutes along the quay edge, no fall in; S: a man knocked in climbs out")
P("4.5.1", "Traffic drivers", "AI drivers at junctions, giving way, reacting to crashes and people; always braking for people.", std="AI drivers always brake for people (canon); ER-DRIVE-04", ss="canon; DESIGN §5", des="TRAFFIC-STAGE1-REFERENCE-MODEL", tr="both", f=1, o="builder", n=["4.6"],
  h="2|80|guess", rk="medium|" + RT, t="S: 1,000 seeded crossings; 40 minutes lawful driving with no hits")
P("4.5.2", "Parked cars", "Parked cars dressed along the kerbs from the car kit.", std="His look at one parked car before twenty (ruling 17 Nov)", ss="RULINGS cars 17 Nov", des="PLAN-PARKED-CARS-2026-11-17", tr="unreal", f=1, o="builder", n=["4.6.1"],
  h="0|40|guess", rk="low|", t="the gate")
P("4.6.1", "Car designs", "Fictional 1990 makes that read as period without any real make.", std="Fictional makes only; no real car models (canon)", ss="canon Brands and law", des="car kit tools", tr="unreal", f=1, o="builder",
  h="0|80|guess", rk="medium|trademark risk at shipping; " + RT, t="the gate; a look-alike check against real makes")
P("4.6.2", "Working vehicles", "Vans, lorries, dock trucks, a bus as scenery, police cars, an ambulance.", std="Boats and buses scenery (ruling 23 Sep)", ss="RULINGS 23 Sep", des="not designed", tr="unreal", f=1, o="builder",
  h="0|60|guess", rk="low|" + RT, t="the gate")
P("4.11.1", "Yard dogs", "A dog in a yard barks at a stranger: a witness by sound only, never hurt.", std="A bark is a noise at its reach (DESIGN §2); no harm to animals shown", ss="DESIGN §2", des=AD + "§A23", tr="both", f=1, o="lane", n=["2.2.4"],
  h="0.5|16|guess", rk="low|found by the mechanics check", t="S: a bark draws the owner within the rule")
P("5.2.8", "Physical reactions and falls", "Stagger, fall, being knocked down by a car, getting up: authored moves blended with physics.", std="A struck man reels by the side he was hit (DESIGN §7); nothing through walls", ss="DESIGN §7", des="DESIGN §7", tr="unreal", f=1, o="builder", n=["8.10"],
  h="0|60|guess", rk="high|GTA IV's bodies are the comparison players make; " + RT, rn=["RN-18"], t="his eye; drills")
P("5.2.9", "Live-talk faces", "Mouths, gestures and glances for lines that are made live, not prepared.", std="Live lines' mouths follow the voice's loudness (ruling 1 Oct)", ss="RULINGS 1 Oct", des="RULINGS", tr="unreal", f=1, o="builder", n=["5.2.4"],
  h="0|40|guess", rk="medium|" + RT, t="his eye at talking distance")
P("5.8.3", "Staged scenes in play", "Scripted moments inside play: blocking, performance and timing of a story beat without taking control away.", std="No talk scene runs 60 s without a choice or control (ER-TALK-06)", ss="DESIGN §11", des="DESIGN §11, §15", tr="both", f=1, o="builder", n=["5.8.1"],
  h="1|60|guess", rk="medium|" + RT, t="H: control returns; S: timing")
P("6.9", "Finding the way", "Addresses, house numbers, street-name plates, passengers' 'left here', asking a stranger, a nudge when lost.",
  std="A newcomer reaches a named place unaided within 3 minutes (ER-JOB-01); no markers (ruling 23 Sep)", ss="DESIGN §4; rulings", des="DESIGN §4 Guidance; " + AD + "§A9", tr="both", f=1, o="lane", n=["4.1.3", "6.3"],
  h="2|30|guess", rk="high|fares cannot work without it; " + RT + " (both)", t="H: ten named places reached unaided; S: every place has an address and a landmark")
P("6.10", "Letters and papers in hand", "Things to read: the paper, Agar's solicitor's letters, the VAT letter, notes, posters.", std="Nothing Tom could not know on screen (ER-SCREEN-01)", ss="DESIGN §17", des=AD + "§A19", tr="both", f=1, o="lane", n=["2.4.5"],
  h="0.5|16|guess", rk="low|found by the mechanics check", t="S: each letter opens and goes in the Ledger")
P("7.16", "Pastimes", "Things to do with people that are not crime: the recommended answer is an amateur boxing club.",
  std="Recommended answer to Q3, built to it meanwhile; no stakes, no drink (canon)", ss="Q3 (open); canon", des=AD + "§A28 (to the recommended answer)", tr="both", f=1, o="lane", n=["1.3.1"],
  h="1|40|guess", rk="medium|scope is his; " + RT + " and the mechanics check", t="H: chosen in free time; S: no stakes anywhere")
# group 8, 10
P("8.1.3", "Player PCs and shader stutter", "A minimum machine, scaling steps, shader compilation and traversal hitches fixed by precaching.", std="Epic's PSO precaching for shader stutter; minimum spec to be set", ss="Epic tech blog on shader stutter (red team source)", des="not designed", tr="unreal", f=1, o="builder", n=["8.1"],
  h="0|40|guess", rk="high|UE5 releases are marked down for stutter; " + RT + " (both)", rn=["RN-17"], t="S: hitch count on first run of a clean install")
P("8.2.1", "Crash and bug reporting", "Unreal's crash reporter, an in-game bug report, consented play records.", std="none yet: what is collected and with what consent", ss=RT, des="not designed", tr="unreal", f=0, o="builder",
  h="0|16|guess", rk="medium|" + RT + " (both)", t="a crash produces a report")
P("8.3.1", "PC display options", "Upscalers and frame generation, ultrawide, field of view, uncapped frame rate, HDR.", std="ER-START-01 presets; 3440x1440 is his own screen (ruling 23 Sep)", ss="DESIGN §17; RULINGS 23 Sep", des="not designed", tr="unreal", f=1, o="builder", n=["8.3"],
  h="0|24|guess", rk="medium|" + RT, t="S: each option applies")
P("8.4.1", "Visual stand-ins for sound cues", "For deaf and hard-of-hearing players: what sound tells (noise reach, a street gone quiet) shown another way, as an option.", std="ER-SND-01's information reachable without sound, never as a meter of others' minds (D33)", ss="DESIGN §17; D33", des=AD + "§A6", tr="both", f=1, o="lane", n=["1.4.3"],
  h="1|16|guess", rk="medium|sound carries the town's eyes; " + RT, t="H: ER-EYES-01 with sound off and the option on")
P("8.6.1", "Talk service longevity and offline", "Cost per player hour, outages, the day the service ends, typing with a pad.", std="Offline: the written street carries on (ruling 23 Sep); allowance above a playthrough's measured cost (24 Sep)", ss="RULINGS 23, 24 Sep", des="RULINGS", tr="unreal", f=0, o="builder", n=["8.6"],
  h="0|24|guess", rk="high|" + RT + " (both)", t="the game played whole with the service off")
P("10.11", "Player data and privacy", "Consent and data protection for what players type that is sent to the talk service.", std="none yet: UK and EU data protection to be researched", ss=RT, des="not designed", tr="unreal", f=0, o="builder",
  h="0|16|guess", rk="medium|" + RT + " (both)", t="a privacy notice and consent before the first talk")
P("10.12", "Demo, price and wishlists", "A demo of the first hour, the price, the wishlist plan.", std="none; price is money, his", ss=RT, des="not designed", tr="unreal", f=0, o="builder",
  h="0|24|guess", rk="low|" + RT + " (both)", t="his yes on price")
