from tree_a import P
HS = "Every visual judged against the Hook sheet and KCD2 frames, dated photographs win; yes only for 2026-grade work"
HSS = "RULINGS 21 Sep, 1 Oct (the look); CLAUDE.md gate"
# ---------------- GROUP 4 ----------------
P("4", "The place", "Meridian's Hook and its docks: one port, dense, known by heart.", tr="both", o="builder", f=1, std=HS, ss=HSS, des="canon; atlas-01; DESIGN §6")
P("4.1", "The Hook's layout", "The map as data with testable layout rules.", tr="both", o="builder", f=1, std="D13: map drawn from canon as data with testable layout rules; atlas-01 updated to the built street", ss="D13; ruling 5 Oct", des="atlas-01")
P("4.1.1", "Quay Street", "The built street: the six-bay parade, the shop block, the terraces, Mickey's.", std=HS+"; canon's three sides", ss="canon; RULINGS The look", des="canon; atlas-01", tr="both", f=1, o="builder", n=["5.3.1", "5.4.1"],
  h="2|400|comparable: shop front median 4.25 h each (measured-hours); whole street frames all failed review so far", rk="high|risk R3: every whole street frame failed review", t="the gate; his eye on whole street frames")
P("4.1.2", "The rest of the Hook", "Streets, alleys, yards and back ways round Quay Street.", std=HS+"; density up and back, not out (Study 17)", ss=HSS+"; DESIGN §6", des="atlas-01 (rest of the Hook as data)", tr="both", f=1, o="builder", n=["4.1.5"],
  h="3|800|guess", rk="high|only one street is built; release map is the Hook plus the docks", t="the gate; B navigation soak")
P("4.1.3", "Landmarks and signs", "Street signs and the landmarks people give directions by.", std="Every go-to step named by a landmark reachable unaided in 3 minutes (ER-JOB-01)", ss="DESIGN §4", des="DESIGN §4; street_signs tool", tr="both", f=1, o="builder", n=["4.1.1"],
  h="1|40|guess", rk="medium|", t="H: newcomer reaches named places")
P("4.1.4", "The soft edge", "A fare out of the Hook is driven to the west or north road and comes back as time passed.", std="Nothing fails for leaving (DESIGN §5)", ss="DESIGN §5; Study 2", des="DESIGN §5", tr="both", f=1, o="lane",
  h="0.5|16|guess", rk="low|", t="S: leaving the map edge in the cab")
P("4.1.5", "Street build rules", "Width, props per 10 m, kit reuse, view ends, sightlines, one layer per street state.", std="Study 4's measured street rules", ss="aaa-reference study 04; TRACE s04", des="study 04 (rules, not yet a spec)", tr="unreal", f=1, o="builder", n=[],
  h="0|16|guess", rk="medium|found by the studies gap check", t="automatic layout check against the rules")
P("4.2", "The docks", "The Hook's working waterfront (canon, 19 Nov).", tr="both", o="builder", f=1, std=HS, ss=HSS+"; canon 19 Nov", des="canon; atlas proposal")
P("4.2.1", "Ferry landing and quay", "Where Tom arrives; where the envelope goes.", std=HS, ss=HSS, des="DESIGN §15", tr="both", f=1, o="builder", n=["4.1.2"],
  h="1|120|guess", rk="medium|first thing the player sees", t="the gate")
P("4.2.2", "Old Basin, fish dock, cold stores", "The working places and the packing shift.", std=HS, ss=HSS, des="DESIGN §5, §14; atlas proposal", tr="both", f=1, o="builder",
  h="1|200|guess", rk="medium|docks are cut first if time runs short (ruling 28 Oct)", t="the gate")
P("4.2.3", "Dock gate, customs, Harbour Board", "The gate all three rivals want.", std=HS, ss=HSS, des="DESIGN §13", tr="both", f=1, o="builder",
  h="1|120|guess", rk="medium|", t="the gate")
P("4.3", "Interiors", "Rooms where jobs and stories go; every interior designed and photoreal (D14).", tr="both", o="builder", f=1, std=HS+"; D14: assembled by script from designed kits", ss=HSS+"; D14", des="DESIGN §6 Rooms")
for i, nm, w in [("4.3.1", "Mickey's office and yard", "The front room, radio, counter, the yard with two escapes."),
                 ("4.3.2", "The flat above", "Tom's home, Mickey's until it stops being."),
                 ("4.3.3", "Shops and workplaces", "The caff, Rita's back room, Hal's shop, the pawn, the launderette, the chandler."),
                 ("4.3.4", "Homes", "Ada's front room and other homes jobs and stories enter."),
                 ("4.3.5", "Iveson's yard and hut", "The scrapyard."),
                 ("4.3.6", "The chapel and hall", "Father Walsh's place; religion never a mechanic."),
                 ("4.3.7", "The police station", "Where custody happens."),
                 ("4.3.8", "Where a beaten Tom wakes", "The hospital ward and Grace Rinaldi's kitchen.")]:
    P(i, nm, w, std=HS + ("; ruling 4 Oct (Mickey's office: real glass, 1990 cab office wear)" if i == "4.3.1" else ""), ss=HSS, des="DESIGN §6, §7, §8", tr="both", f=1, o="builder",
      h="1|" + ("24" if i == "4.3.1" else "30") + "|comparable: Mickey's front office 23.8 h logged in phase 1 (measured-hours)", rk="medium|" + ("built shallow; glass and wear owed" if i == "4.3.1" else "interior kits not yet proven at scale"), t="the gate")
P("4.4", "Props and street furniture", "Lamps, the phone box, bins, railings, bollards, signs.", std=HS+"; 3 Oct sources (free first, else our own from photographs)", ss=HSS+"; ruling 3 Oct", des="TARGET-STREET-FURNITURE-2026-11-17; FURNITURE-SPECS", tr="unreal", f=1, o="builder", n=["9.1"],
  h="0|80|comparable: a prop 1 to 2 h (RECIPE)", rk="low|", t="small-piece review (RULINGS 3 Nov)")
P("4.5", "Traffic and parked cars", "AI drivers that always brake for people; parked cars from the kit.", std="AI drivers always brake for people (canon); 1,000 seeded crossings with no contact (ER-DRIVE-03)", ss="canon; DESIGN §5; ruling 17 Nov", des="TRAFFIC-STAGE1-REFERENCE-MODEL; PLAN-PARKED-CARS", tr="both", f=1, o="builder", n=["4.6"],
  h="2|120|guess", rk="medium|", t="S: crossings; his look at parked cars")
P("4.6", "Vehicles", "The firm's cabs, period cars, police cars and vans, all fictional.", std="Fictional makes only (canon brands); 1990 by look and sound (ruling 18 Nov)", ss="canon Brands and law; RULINGS cars", des="car kit tools (car_kit, car_loft)", tr="unreal", f=1, o="builder", n=["9.1"],
  h="0|120|guess", rk="medium|vehicles module waits for Kiln's three proofs (ruling 18 Nov)", t="the gate")
P("4.7", "Day and night", "The clock's light: day and night now, four or five states later, no moving sun.", std="Ruling 7 Oct; night as pools of lamp light with dark between (1 Oct)", ss="RULINGS weather and night", des="DESIGN §6", tr="both", f=1, o="builder", n=["5.4.2"],
  h="0.5|24|guess", rk="low|", t="the gate at night")
P("4.8", "Weather", "Dry overcast, drizzle, rain; one wetness value drives look, sight, sound and who is out.", std="Grey range only, never sunshine in the friends' build (5 Oct); one wetness value (DESIGN §6)", ss="RULINGS 5 Oct; DESIGN §6", des="DESIGN §6; LIGHT-WEATHER-VALUES-2026-11-17", tr="both", f=1, o="builder", n=[],
  h="0.5|40|guess", rk="low|", t="S: same seed in three weathers")
P("4.9", "1990 detail", "Signage, poll-tax posters, the brand bible's owed brands, CCTV at the bank, phone boxes.", std="canon era; late-analog; brand bible owes the football club, paper, pirate radio, TV channel, phone operator, postal cypher", ss="canon Era, Brands and law", des="STYLE-SHEET-1990-DRAFT", tr="both", f=1, o="builder", n=["9.2"],
  h="0.5|40|guess", rk="medium|content-rule breaches found before (back-bar decal; W7)", t="canon-gate and content-gate; his eye")
P("4.10", "Pubs without drink and the closed school", "Places that exist with no drink and no children.", std="canon content rule: pubs as places, boarded or serving food; the school stands closed", ss="canon D18", des="canon", tr="both", f=1, o="builder",
  h="0.5|16|guess", rk="medium|content rule", t="content gate over clips and props")
P("4.11", "Animals and birds", "Gulls and pigeons on a port street; dogs on a lead.", std="none yet: ambient life densities to be set from period photographs", ss="MASTER-CHECKLIST A25.14, A25.15", des="not designed", tr="unreal", f=1, o="builder",
  h="0|24|guess", rk="low|found by the checklist mapping", rn=["RN-15"], t="his eye on the street frame")

# ---------------- GROUP 5 ----------------
P("5", "How it looks and sounds", "Presentation: people, motion, places, light, sound, voices, music, camera, effects.", tr="unreal", o="builder", f=1, std=HS, ss=HSS, des="RULINGS The look; Faces; Clothes")
P("5.1", "Characters", "People on screen.", tr="unreal", o="builder", f=1, std=HS+"; principals at talking distance on the 2026 bar against KCD2 frames", ss="RULINGS 19 Nov", des="casting sheets")
P("5.1.1", "Faces", "MetaHuman faces cast from the casting sheets.", std="Faces frozen: Ron P2, Sheila S4, Darren S6, Tom L1; the other eleven cast from their sheets", ss="RULINGS 30 Sep, 8 Oct", des="casting sheets", tr="unreal", f=1, o="builder", n=["9.2"],
  h="0|80|guess", rk="medium|risk R4: underlit faces", t="his eye at talking distance")
P("5.1.2", "Bodies", "Body types for the cast and crowd.", std="Bodies in F:\\LedgerTools\\bodies; clothes fit them", ss="CLAUDE.md sessions", des="Kiln plan", tr="unreal", f=1, o="clothing", n=["9.2"],
  h="0|24|guess", rk="low|", t="the gate")
P("5.1.3", "Hair", "Strands; no hair skill until one character passes the full gate.", std="Hair PASS-LIST (his words); strands stay (9 Nov)", ss="RULINGS 3, 9 Nov", des="hair pass list", tr="unreal", f=1, o="builder",
  h="0|60|comparable: hair round 4 about 2.4 h", rk="high|no hair has passed; Houdini's free licence cannot export hair (draft risk 8)", t="the full gate and his look")
P("5.1.4", "Clothes", "Kiln garments; three outfits across the rise and a dark coat for nights.", std="Clothes' floor: plain, period-plausible, no modern giveaways, no clipping; principals at talking distance on the 2026 bar", ss="RULINGS Clothes (3 Oct, 19 Nov)", des="DESIGN §14; Kiln design note", tr="unreal", f=1, o="clothing", n=["9.1"],
  h="0|300|comparable: garments 1.6 to 9.8 h each, none finished (measured-hours)", rk="high|no garment finished; Marvelous lapses 26 Nov", t="the gate; his eye in the game's camera")
P("5.1.5", "Crowd variety", "Many people without noticed repeats.", std="none yet: repeat distance and variety rules to be set", ss="risk R5", des="not designed", tr="unreal", f=1, o="builder", n=["5.1.1", "5.1.4", "3.2.4"],
  h="0|120|guess", rk="high|unpriced; memory over budget (R5)", rn=["RN-11"], t="S: no identical pair in one frame; his eye")
P("5.2", "Animation", "Movement.", tr="unreal", o="builder", f=1, std="People in motion won by research and trial; no money for motion capture (5, 6 Nov)", ss="RULINGS 5, 6 Nov", des="RULINGS People's moves")
P("5.2.1", "Locomotion", "Motion matching walk and run on Epic's Game Animation Sample.", std="Third try the default (his eye 26 Oct); feet do not slide", ss="RULINGS People's moves", des="RULINGS", tr="unreal", f=1, o="builder", n=["1.1.1"],
  h="0|24|comparable: a motion try 1 to 3.5 h", rk="medium|treads on the spot, slides (FINDINGS)", t="his eye; foot-slide measure")
P("5.2.2", "Fight animation", "Blows, reactions, falls; the source gets a lab test first.", std="Melee sheet C2 to C4; ruling 12 Oct: animation source lab test before building", ss="RULINGS combat; melee sheet", des="combat design", tr="unreal", f=1, o="builder", n=["5.2.7", "1.3.1"],
  h="0|120|guess", rk="high|combat not yet thrown in Unreal (risk register)", t="melee drills in Unreal match the browser")
P("5.2.3", "Interaction animation", "Doors, carrying, sitting, phones, car in and out, searching.", std="No glitches (CLAUDE.md gate)", ss="CLAUDE.md", des="not designed as a list", tr="unreal", f=1, o="builder", n=["5.2.7"],
  h="0|80|comparable: character sit 6 h", rk="medium|", t="the gate")
P("5.2.4", "Faces and mouths", "Lip movement, expression, glances; audio-driven mouths for prepared lines.", std="Live lines' mouths follow loudness; prepared lines use Epic's audio-driven mouths (1 Oct); Sheila's face whole when she talks", ss="RULINGS 1 Oct, 4 Oct", des="RULINGS", tr="unreal", f=1, o="builder", n=["5.6.2"],
  h="0|40|guess", rk="medium|risk R4: mouths", t="his eye at talking distance")
P("5.2.5", "Crowd and idle animation", "Working, waiting, smoking, talking; idle breaks.", std="No stiff idle; nobody frozen stiff (clothes floor)", ss="RULINGS; risk R4", des="corner plan (n02-4)", tr="unreal", f=1, o="builder", n=["5.2.7"],
  h="0|60|comparable: the corner about 21 h", rk="medium|", t="the gate")
P("5.2.6", "Body language of knowing", "Half-recognition, lying and having heard of Tom show in posture first.", std="D29: posture first", ss="D29", des="D29; DESIGN §2", tr="both", f=1, o="builder", n=[],
  h="1|60|guess", rk="high|the engine is only felt if this reads", t="H: ER-EYES-01")
P("5.2.7", "Clip sourcing and cleanup", "Library clips (Epic, MetaHuman, Mixamo, CMU), retargeting, foot-slide fixes.", std="Sources allowed: Epic samples, MetaHuman, Mixamo on his account, CMU inside the game; Pexels/Pixabay as references", ss="RULINGS People's moves; 9, 12 Nov", des="RULINGS", tr="unreal", f=0, o="builder", n=["9.2"],
  h="0|40|guess", rk="medium|found by the departments check (no capture budget)", t="each clip's source and licence recorded")
P("5.3", "Environment art", "Buildings and ground.", tr="unreal", o="builder", f=1, std=HS, ss=HSS, des="Hook sheet")
P("5.3.1", "Building kits", "Windows, doors, shopfronts, brick, Flemish bond.", std=HS+"; kit pieces from period books checked by a fresh helper (8 Oct)", ss=HSS+"; ruling 8 Oct", des="kit specs", tr="unreal", f=1, o="builder", n=["9.2"],
  h="0|200|comparable: shop front 4.25 h", rk="high|risk R3", t="the gate")
P("5.3.2", "Materials and grime", "A seeded wear layer; grime is the strategy (D53).", std="D53; calibrated to real reflectances", ss="D53; RULINGS 21 Sep", des="RULINGS", tr="unreal", f=1, o="builder",
  h="0|40|comparable: surface 1.5 to 4 h", rk="medium|", t="the gate")
P("5.3.3", "Wet street", "Dark, glistening, mirroring sky and buildings; puddles are water.", std="Ruling 3 Oct bars for the wet street", ss="RULINGS 3 Oct", des="RULINGS", tr="unreal", f=1, o="builder", n=["4.8"],
  h="0|16|comparable: wet ground about 4 h", rk="medium|", t="the gate")
P("5.3.4", "Shop glass and windows", "White frames, sash bars, sky in the glass; shop glass reflecting the street.", std="Ruling 3 Oct (windows); ruling 4 Oct (real glass)", ss="RULINGS 3, 4 Oct", des="RULINGS", tr="unreal", f=1, o="builder", n=["5.3.1"],
  h="0|24|guess", rk="medium|found by the studies gap check", t="the gate")
P("5.4", "Lighting and picture", "Light and grade.", tr="unreal", o="builder", f=1, std="Lighting judged through the game's camera and exposure (30 Sep)", ss="RULINGS 30 Sep", des="RULINGS")
P("5.4.1", "Day exposure and sky", "One stop darker, kept; the sky is a photograph.", std="Ruling 29 Oct; D40", ss="RULINGS 29 Oct, 15 Sep", des="RULINGS", tr="unreal", f=1, o="builder",
  h="0|16|guess", rk="medium|", t="checked against real values")
P("5.4.2", "Night lighting", "Pools of lamp light with darkness between, lit windows, not one orange wash.", std="Ruling 1 Oct; ER-NIGHT-01 brightness floor", ss="RULINGS 1 Oct; DESIGN §6", des="RULINGS", tr="both", f=1, o="builder", n=[],
  h="0.5|40|guess", rk="medium|readability against darkness", t="H: darkest-spot screenshots; the gate at night")
P("5.4.3", "Grade, grain and depth of field", "Presentation owed since D28.", std="D28 presentation built early", ss="RULINGS 15 Sep", des="not designed in detail", tr="unreal", f=1, o="builder",
  h="0|16|guess", rk="low|", t="the gate")
P("5.5", "Sound", "The street heard; sound carries the town's eyes. CC0 only (D26).", tr="both", o="builder", f=1, std="ER-SND-01; D26", ss="DESIGN §17; D26", des="DESIGN §17 Sound")
for i, nm, w, s in [("5.5.1", "Footsteps and foley", "Footsteps by surface and gait, cloth, handling.", "Footsteps by surface and gait (DESIGN §17)"),
                    ("5.5.2", "Doors and impacts", "Doors that creak, hit and latch; a forced door the loudest thing in a quiet street.", "DESIGN §17"),
                    ("5.5.3", "Street beds and states", "Beds, capped one-shots and placed sources; four states of the hour.", "DESIGN §17; STREET-SOUND-SOURCES plan"),
                    ("5.5.4", "Rain and rooms", "One rain value fades layers and halves voices; rooms change echo at the doorway.", "DESIGN §17"),
                    ("5.5.5", "Car sound", "1990 by sound: engine note, automatic changes, squeal from 80% grip.", "Driving sheet M12; ruling 18 Nov"),
                    ("5.5.6", "Fight sound", "Four layers landing within a frame of the blow.", "Melee sheet; DESIGN §7"),
                    ("5.5.7", "The mix", "The quietest lead voice sets the mix; talk lowers the beds; silence the commonest music.", "DESIGN §17")]:
    P(i, nm, w, std=s, ss="DESIGN §17", des="DESIGN §17", tr="both", f=1, o="builder", h="0.5|24|guess", rk="medium|sound is a lane with CC0 only", t="H: sound-only test; his ear")
P("5.6", "Voices", "Spoken lines.", tr="unreal", o="builder", f=1, std="Voices judged by ear; accent checker a screen only (30 Sep)", ss="RULINGS 30 Sep", des="RULINGS voices")
P("5.6.1", "Cast voices", "Chosen voices per character, cast only on his yes.", std="Sheila p267, Ron p227, Darren p286, Agar p226, dispatcher p280; others on his yes", ss="RULINGS voices (3 Oct to 19 Nov)", des="RULINGS", tr="unreal", f=1, o="builder",
  h="0|40|guess", rk="medium|accents (draft risk 4)", t="his ear")
P("5.6.2", "Voice generation and watermark", "Local voice program, prepared lines with acted references, the watermark kept.", std="D50 watermark; Pocket kept (19 Nov)", ss="RULINGS D50, 19 Nov", des="RULINGS", tr="unreal", f=0, o="builder", n=["8.7"],
  h="0|24|guess", rk="medium|", t="packaged speech measure")
P("5.6.3", "Thinking sound and timing", "A short thinking sound with a glance before an answer, cut when it starts.", std="Ruling 28 Sep; no loading sign", ss="RULINGS 28 Sep", des="RULINGS; DESIGN §11", tr="both", f=1, o="builder",
  h="0.5|8|guess", rk="low|", t="S: timing")
P("5.7", "Music", "Silence is the commonest music; never combat music.", std="DESIGN §17; never combat music", ss="DESIGN §17", des="DESIGN §17 (one line); DESIGN-ADDENDUM §A8", tr="unreal", f=1, o="builder",
  h="0|40|guess", rk="medium|music barely designed; PLAYERS praise 9 (music and sound) is a loved theme", rn=["RN-16"], t="his ear")
P("5.7.1", "Radio programmes and period songs", "What plays on radios in cabs, shops and the office; the pirate radio station the brand bible owes.", std="No real bands, lyrics or brands (canon); content from the allowlist or our own, only on licences that never expire", ss="canon Brands and law", des="not designed", tr="unreal", f=1, o="builder", n=["4.9"],
  h="0|40|guess", rk="medium|found by the departments check", t="canon gate; his ear")
P("5.8", "Cameras and cut scenes", "The camera system and the few short scenes.", tr="both", o="builder", f=1, std="ER-CAM-01, 02", ss="DESIGN §17", des="DESIGN §17")
P("5.8.1", "Camera rig by state", "One arm read from rows: street, run, room, talk, fight, car; blends of a second or less.", std="Ruling 28 Oct (street, talk closer, fights wider); blends 1 s or less; shake obeys Reduce motion", ss="RULINGS 28 Oct; DESIGN §17", des="DESIGN §17", tr="both", f=1, o="builder",
  h="1|17|measured: camera rows 17.2 h", rk="medium|", t="S: frames counted; B clip detector")
P("5.8.2", "Cut scenes", "Few, short, skippable; the ferry shot 20 s.", std="Every scene skippable and at most 60 s (ER-FIRST-02); few short skippable cutscenes (23 Sep)", ss="RULINGS 23 Sep; DESIGN §15", des="DESIGN §15", tr="unreal", f=1, o="builder",
  h="0|40|guess", rk="low|", t="S: skip works; length measured")
P("5.9", "Effects", "Blood (light gore at most), rain, breath, smoke, broken glass.", std="Blood and light gore, no cruelty as spectacle (canon); photosensitivity line once guns flash", ss="canon; DESIGN §17", des="not designed as a list", tr="unreal", f=1, o="builder",
  h="0|40|guess", rk="low|", t="the gate; content check")
P("5.10", "Art direction and look reference", "The Hook sheet, grade targets, the floors and the KCD2 frames everything is judged against.", std="The Hook sheet (pass 4) governs mood, palette and composition", ss="RULINGS 21 Sep, 1 Oct", des="the Hook sheet", tr="unreal", f=0, o="builder",
  h="0|8|guess", rk="low|exists; found by the departments check as having no part", t="the gate uses it")

# ---------------- GROUP 8 ----------------
P("8", "Technical", "Runs well on his PC and on players' PCs.", tr="unreal", o="builder", f=1, std="ER-PERF-01", ss="ruling 23 Sep", des="DESIGN §17")
P("8.1", "Performance", "Smooth play.", std="60 fps at 3440x1440 on the RX 6700 with the voice running, never under 30 (ruling 23 Sep); median frame 16.7 ms, p99 25 ms", ss="RULINGS 23 Sep; PLAYERS standards", des="DESIGN §17 ER-PERF-01", tr="unreal", f=1, o="builder",
  h="0|60|comparable: a frame-headroom round 4 to 12.5 h", rk="high|PLAYERS punish 7: stutter and crashes", t="S: packaged frame-time run")
P("8.1.1", "Frame, memory and crowd budget", "Per-system budgets: update, texture pool, crowd, voice on the 6 GB card.", std="6 GB card line is the game alone (24 Oct); spare card time 1.7 ms", ss="RULINGS 24 Oct; study 12", des="study 12 (budgets owed)", tr="unreal", f=0, o="builder", n=["9.9"],
  h="0|24|guess", rk="high|memory 6,005 MB against about 4.7 GB binding (risk R5)", t="S: budget table per build")
P("8.1.2", "Streaming and loading", "Loading the Hook and docks without stutter or long waits.", std="none yet: load and hitch limits to be set", ss="study 04, 12", des="not designed", tr="unreal", f=1, o="builder",
  h="0|24|guess", rk="medium|", rn=["RN-17"], t="S: hitch count on a scripted drive")
P("8.2", "Stability and saves that never break", "No crashes, no corrupt saves, long sessions safe.", std="SaveChaos; Soak; no bug that stops progress (PLAYERS punish 6)", ss="CLAUDE.md simulation tests; PLAYERS", des="simulation tests", tr="both", f=1, o="builder",
  h="1|40|guess", rk="medium|the main cloud check red for 544 runs (status-unreal)", t="SaveChaos, Soak, nightly walk")
P("8.3", "Settings", "Graphics, audio and controls settings, presets.", std="ER-START-01 presets; checklist sections 41, 42 as acceptance checks", ss="DESIGN §17", des="DESIGN §17", tr="both", f=1, o="builder", n=[],
  h="0.5|24|guess", rk="low|", t="S: each setting applies and persists")
P("8.4", "Accessibility", "Text, hearing, motor and cognition options.", std="Subtitles and prompts large; switches for prompts, hints, chatter subtitles; Reduce motion; checklist 43 to 46", ss="DESIGN §17; MASTER-CHECKLIST 43 to 46", des="DESIGN §17 Screen", tr="both", f=1, o="builder",
  h="0.5|40|guess", rk="medium|", t="S: each option; layout test")
P("8.5", "Install and launch", "Starts from its shortcut, shows progress, opens at a sensible size.", std="ER-START-01 (basics 1 to 5)", ss="DESIGN §17", des="DESIGN §17", tr="unreal", f=1, o="builder",
  h="0|16|guess", rk="medium|risk R7", t="S on the packaged build")
P("8.6", "Live talk service", "The server relay, the key never shipped, each copy's allowance, a spending stop, offline fallback.", std="Ruling 24 Sep (sold once, key never shipped, allowance above a playthrough's cost); offline: the written street carries on", ss="RULINGS 28 Oct, 24 Sep, 23 Sep", des="RULINGS", tr="unreal", f=0, o="builder", n=[],
  h="0|60|guess", rk="high|cost per hour likely low by a quarter to a third (draft risk 3)", t="S: offline and slow stand-ins; cost per playthrough measured")
P("8.7", "Local models on the card", "Voice and fallback talk on the player's card, re-tested every three months.", std="RULINGS 28 Oct", ss="RULINGS 28 Oct", des="RULINGS", tr="unreal", f=0, o="builder", n=["8.1.1"],
  h="0|24|guess", rk="medium|", t="talk bench")
P("8.8", "Runtime content guards", "The content rule on live speech and crowd generation.", std="canon content rule's six enforcement sites; live talk names no real brand or anything after 1992", ss="canon D18; RULINGS 29 Sep", des="canon", tr="both", f=0, o="town",
  h="0.5|16|guess", rk="medium|", t="content gate; planted bad replies")
P("8.9", "Text and language", "English only; text out of code.", std="Ruling 23 Sep", ss="RULINGS 23 Sep", des="RULINGS", tr="both", f=0, o="builder",
  h="0.5|8|guess", rk="low|", t="S: no player-facing string in code")
P("8.10", "Collision and physics", "Bodies, props, cars and doors colliding believably; ragdoll blended with authored falls.", std="none yet: checklist A12 as acceptance checks; nothing passes through walls (ER-FIGHT-06)", ss="MASTER-CHECKLIST 12", des="not designed", tr="both", f=1, o="builder", n=["5.2.2"],
  h="0.5|40|guess", rk="medium|found by the checklist and departments checks", rn=["RN-18"], t="B soak; S physics drills")

# ---------------- GROUP 9 ----------------
P("9", "The machinery", "How the game is made: Kiln, the art pipeline, one simulation, the port, tests, records.", tr="both", o="builder", f=0, std="Authored breadth: every piece has a spec and a check (13 Nov)", ss="RULINGS 13 Nov", des="RULINGS")
P("9.1", "Kiln", "His clothing pipeline, then props, vehicles, buildings and people modules.", std="Three proofs before any other module (18 Nov): held-back garments pass; Ron walks the packaged game in a Kiln outfit; a garment costs a fraction of the old route", ss="RULINGS 13, 14, 18 Nov", des="Kiln design note; KILN-TO-GAME-PLAN", tr="unreal", f=0, o="clothing",
  h="0|400|guess", rk="high|v1 0 of 6 (NOW); wrist tangle set aside (draft risk 6)", t="Kiln v1 checklist; held-back jobs")
for i, nm in [("9.1.1", "Drape"), ("9.1.2", "Kiln-to-game adapter"), ("9.1.3", "Garment mesh chain (weld, retopology, layout, bake)"), ("9.1.4", "Skinning and pose tests"),
              ("9.1.5", "Import to Unreal"), ("9.1.6", "Packaged wear film and gate"), ("9.1.7", "Bend-back for posed bodies"), ("9.1.8", "Cloth hand-off in game (Chaos, for skirts)")]:
    P(i, nm, "A stage of the Kiln-to-game chain (KILN-TO-GAME-PLAN-2026-11-17).", std="The plan's stage check", ss="KILN-TO-GAME-PLAN-2026-11-17", des="KILN-TO-GAME-PLAN", tr="unreal", f=0, o="clothing", h="0|30|guess", rk="medium|", t="the plan's stage check")
P("9.2", "Art pipeline", "MetaHuman casting, Blender kits, the asset plan, the catalogue.", std="Every asset family follows the asset plan (3 Oct); reuse first", ss="RULINGS 3 Oct; CLAUDE.md", des="asset plan; CATALOGUE", tr="unreal", f=0, o="builder",
  h="0|80|guess", rk="medium|", t="catalogue line per asset")
P("9.3", "One simulation", "The C# Core as source of truth, its C++ port in Unreal, its browser build in the prototype; one set of goldens.", std="The port matches the C# goldens; 102,949 browser rows matched (19 Nov); town simulation frozen until C#'s replaces the prototype's", ss="canon OPEN 1; RULINGS 18-19 Nov; advisor 249", des="ONE-SIM-METHOD-2026-11-19", tr="both", f=0, o="town",
  h="2|80|measured: browser build about 2.2 cloud hours (measured-hours)", rk="high|11 of 30 planted breaks in the port fail no test; combat, debts, economy, empire, acts II and III not ported", t="CoreTests, Soak, SaveChaos, PerceptionGolden, StrangerTest; goldens identical")
P("9.4", "Prototype to Unreal port", "Each system proved in the prototype ported under the same tests (money, debts, jobs, fights, talk).", std="Unreal ports its money, debts, jobs, fights and talk under the same tests (ruling 18-19 Nov; ONE-SHOT-PORTING.md)", ss="RULINGS prototype line; advisor 254", des="ONE-SHOT-PORTING.md (to be written)", tr="both", f=0, o="builder", n=["9.3", "9.5"],
  h="2|200|guess", rk="high|a second implementation can drift", t="same tests pass in both")
P("9.5", "Testing and gates", "The clumsy-player bot, scripted tests, the AI hands-on session, the panel of eight, the nightly packaged walk, the publish gate.", std="DESIGN §19; a play build reaches him only with a publish-gate pass and a known-issues note", ss="DESIGN §19; RULINGS 18 Nov", des="DESIGN §19; tools/lane/gate", tr="both", f=0, o="lane",
  h="3|60|measured: round 6 gate about 2.8 h", rk="medium|his eye is the only final judge (W6)", t="gate.py passes; nightly walk report")
P("9.6", "The tuning table", "One home for every number the browser, the Core and Unreal are tuned from.", std="Every rule's number in one table (DESIGN §19; Study 13)", ss="DESIGN §19", des="prototype rules.js", tr="both", f=0, o="lane",
  h="1|16|guess", rk="medium|1,053 small numbers not examined (NOT_DONE 3)", t="S: no magic number outside the table")
P("9.7", "Records and guards", "Doc caps, approvals, retention, git size guard, content and canon gates.", std="CLAUDE.md Records and Builds", ss="CLAUDE.md", des="tools/", tr="both", f=0, o="builder",
  h="0|16|guess", rk="low|", t="guards run on every commit")
P("9.7.1", "Licence and terms record", "The allowlist and THIRD-PARTY.md: every source's licence recorded; decided by the sessions (19 Nov).", std="The allowlist is law; licences never go to him (19 Nov)", ss="CLAUDE.md; advisor 252", des="license-allowlist.md", tr="both", f=0, o="builder",
  h="0|8|guess", rk="medium|terms unread for some tools (R8)", t="every shipped file on the allowlist")
P("9.7.2", "Recipe and handover", "RECIPE.md and the handovers, so the method survives without the history.", std="RECIPE rewritten each phase; monthly cold re-run (18 Nov)", ss="RULINGS 9, 18 Nov", des="RECIPE.md", tr="both", f=0, o="builder",
  h="0|8|guess", rk="medium|never run cold (draft risk 5)", t="monthly cold re-run judged by the gate")
P("9.8", "Talk bench", "Choosing talk and voice models by the kind of moment, re-checked monthly.", std="D48; monthly from 7 Dec, three candidates at most", ss="RULINGS 1 Oct, 12 Nov", des="RULINGS", tr="unreal", f=0, o="town",
  h="0|16|guess", rk="medium|models change under us (W3)", t="bench scores")
P("9.9", "Feel measurement", "Measuring sheets for driving and the other felt verbs and activity shares, from footage, outside only.", std="DRIVING-MEASUREMENT-METHOD: five samples a number, two independent measurers, clips played never downloaded", ss="DRIVING-MEASUREMENT-METHOD-2026-11-19; advisors 255 to 257", des="DRIVING-MEASUREMENT-METHOD; FEEL-MEASUREMENT-METHOD-2026-11-20 (pending)", tr="both", f=0, o="builder",
  h="0|24|measured estimate: driving about 23.5 h on his PC (advisor 249)", rk="medium|", t="two measurers agree within the sheet's tolerance")
P("9.10", "Plan, forecast and spend", "The dated plan, forecasts, hour coding, allowances and caps; a new system placed in PLAN.md first.", std="No new system before its place in PLAN.md (29 Sep); re-plan from measured pace (19 Nov H3 A)", ss="RULINGS; advisor 241 point 2", des="PLAN.md; order ledgers", tr="both", f=0, o="builder",
  h="0|16|guess", rk="high|scope outruns the date (risk register)", t="Monday audit")
P("9.11", "Reference studies and re-checks", "The 18 studies, unreached sources, re-checks (Study 17 review, GTA VI after a month).", std="Research method (13 Oct): primary sources, dated, unreached listed", ss="CLAUDE.md research method", des="aaa-reference studies", tr="both", f=0, o="lane",
  h="0|16|comparable: one study 0.6 to 1.3 helper h", rk="low|", t="a fresh reviewer per study")
P("9.12", "Design records", "canon, VISION, DESIGN and its addendum, BUILD-ORDER, this parts tree.", std="canon outranks; DESIGN approved 19 Nov; every part has a standard (RULINGS line proposed in advisor 257)", ss="canon OPEN 3; advisor 257", des="production/lane/synthesis/", tr="both", f=0, o="lane",
  h="1|0|guess", rk="low|", t="tools/lane/parts-tree/check.py")

# ---------------- GROUP 10 ----------------
P("10", "Shipping", "Getting the game out: one full release late in 2027.", tr="unreal", o="builder", f=0, std="One full release late in 2027, not early access (28 Oct)", ss="RULINGS 28 Oct", des="RULINGS")
P("10.1", "Release build", "The packaged release build and installer.", std="Done means in the packaged release build, walked by the AI tester (CLAUDE.md)", ss="CLAUDE.md", des="packaging scripts", tr="unreal", f=0, o="builder", n=["8.5"],
  h="0|40|guess", rk="medium|risk R7", t="nightly packaged walk")
P("10.2", "Store, rating and disclosure", "Store page, age rating, Steam's AI disclosure, price and length statement.", std="Steam's AI disclosure as drafted (24 Sep); length 15 to 20 hours (28 Oct)", ss="RULINGS 24 Sep, 28 Oct; G4-RATING-AND-STORE", des="G4-RATING-AND-STORE-2026-11-17", tr="unreal", f=0, o="builder",
  h="0|24|guess", rk="medium|disclosure untrue today (R8); price not set (map-players P7)", t="rating questionnaire; disclosure matches the build")
P("10.3", "Friends' builds", "A friends' build at the end of every phase from phase 4, on his PC.", std="Meridian Test (3 Oct): they do not bounce off, the town knows them, talk feels live, he would rather play it", ss="RULINGS 3 Oct, 28 Oct, 1 Nov", des="RULINGS; friends-build MAP", tr="unreal", f=0, o="builder", n=["7.1"],
  h="0|40|guess", rk="high|no thirty minutes ever played (R6)", t="the Meridian Test")
P("10.4", "Credits and notices", "Third-party notices, credits for CC-BY makers, allowlist notices kept.", std="Every CC-BY maker credited; notices kept (allowlist)", ss="RULINGS 3 Oct, 30 Oct; allowlist", des="THIRD-PARTY.md", tr="unreal", f=0, o="builder",
  h="0|8|guess", rk="low|", t="script: every shipped licensed file has its notice")
P("10.5", "Release testing", "Final passes over the whole game: every ending, every job outcome, long sessions.", std="ER-END-01, ER-JOB-05 across the whole game; the panel at 6 of 8", ss="DESIGN §16, §4; BUILD-ORDER", des="DESIGN §19", tr="unreal", f=0, o="builder", n=["9.5"],
  h="0|80|guess", rk="medium|", t="all scripted routes in the release build")
P("10.6", "After release", "Patches, new districts in updates, a stated position on mods.", std="More districts in updates after release (28 Oct)", ss="RULINGS 28 Oct", des="RULINGS", tr="unreal", f=0, o="builder",
  h="0|0|not costed", rk="low|", t="none until release")
P("10.7", "Platform account, cloud saves and achievements", "Steam integration: cloud saves, achievements if any, overlay, account handling.", std="none yet: checklist 39 and 49 as acceptance checks", ss="MASTER-CHECKLIST 39, 49", des="not designed", tr="unreal", f=0, o="builder",
  h="0|24|guess", rk="low|found by the checklist mapping", t="checklist 49 items pass")
P("10.8", "Trailer, key art and store capsule", "The pictures and film that sell it.", std=HS, ss=HSS, des="not designed", tr="unreal", f=0, o="builder",
  h="0|24|guess", rk="low|found by the departments check", t="his eye")
P("10.9", "Player support and community", "Where players report problems and get answers after release.", std="none", ss="map-departments", des="not designed", tr="unreal", f=0, o="builder",
  h="0|16|guess", rk="low|found by the departments check", t="a support route exists before release")
P("10.10", "Legal and company admin", "Name search, the company's admin, tax and contracts for selling the game.", std="none; money matters are his", ss="map-departments; RULINGS 16 Sep", des="not designed", tr="unreal", f=0, o="builder",
  h="0|8|guess", rk="medium|his area (money)", t="his yes")
