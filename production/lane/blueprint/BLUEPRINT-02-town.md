# BLUEPRINT 02: The town under the hood

Part of the LEDGER blueprint; the index, the rules of reading and the conflicts are in BLUEPRINT.md. The engine: routines, perception, memory, gossip, witnesses, police, money, debts, the outfit, rivals, crew, position.

Each entry: how it works; its standard and test; the source of the standard; its status; its coverage row. Conflicts are numbered C-nnn and listed in BLUEPRINT-11-conflicts-and-gaps.md.


## 2.1 Routines and the living town

Everyone keeps a day, with Tom or without him.


### 2.1.1 Schedules of named people

- How it works: Everyone named keeps a routine, hour by hour: where they are, what they do, which door they use. Each place in a routine has a cap and an owner, so no doorway jams. People sleep at night and their windows go dark; a lit window means somebody is home. Under the 60 s clock a person's places lie within about 200 m of walking (about 125 real seconds, 2 game hours); longer moves are a few blocks of several game hours. The town code uses no chance, so the same week plays the same way twice.
- Standard: Places with a cap and an owner (Studies 1, 17); every walk arrives (prototype walk checks) Test: S: walk checks wherever Tom stands; no jammed doorway in a seeded week
- Source: DESIGN §2; aaa-s01-04 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2; DESCRIPTION-COPY-2 §5 (The town lives without him); DEFINITIONS CLK-03 (F09)
- Status: decided. Coverage row: 2.1.1. Conflicts settled: C-036.

### 2.1.2 The crowd's clock windows

- How it works: The unnamed crowd keeps clock windows: the dock shift at dawn, shoppers through the day, the street emptying at night; adults only. On Quay Street's parade front (100 m, both pavements) the bands (design pass 4, rescaled) are 05:30 to 07:00 5 to 8 people; 08:00 to 09:30, 12:00 to 14:00 and 16:30 to 18:00 12 to 20; other daytime 6 to 12; 18:00 to 22:00 5 to 10; 22:00 to 01:00 2 to 5; 01:00 to 05:30 0 to 2 besides the constable. On the quay road by the fish dock 05:30 to 07:00 it is 10 to 18. One camera frame holds 4 to 10 at a busy band (GD-02). Rain halves each band; Thursday's market takes a third off the shops' daytime bands; Saturday's match doubles the street at 15:00 and 17:00 for half an hour (up to 30). These bands are the design's until the 1990 hours are found.
- Standard: Hours from 1990 research (owed) Test: S: crowd counts by hour match the researched table
- Source: DESIGN §2; aaa-s01-05 (no reference figure yet). Designed in: DESIGN §2; DESCRIPTION-COPY-2 §5; DEFINITIONS G9 (FIT-G9); CLOUD-FIGURES B4
- Status: unmeasured. Coverage row: 2.1.2.

### 2.1.3 Off-screen life

- How it works: Unseen people keep the same rules as seen ones: they go on seeing, remembering and talking. A week plays out the same, deed for deed, whether Tom watches or not. Job steps sleep while he is away and settle by the clock when he returns.
- Standard: Unseen people keep the same rules as seen ones (DESIGN §2) Test: S: a seeded week gives the same result watched or unwatched
- Source: DESIGN §2 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2; DESCRIPTION-COPY-2 §5; DESIGN §4 (ER-JOB-07)
- Status: decided. Coverage row: 2.1.3.

### 2.1.4 Weather and hour change who is out

- How it works: Weather comes as weighted profiles (dry overcast, drizzle, rain), never sunshine, and one wetness value drives the look, what is seen and heard, and who is out. Rain cuts sight and sound, empties the street, halves the voices (and halves each crowd band) and makes the road slippery. The same seed dry, in drizzle and in rain gives three different streets, the same way every time. Day turns to night with dusk and lamps; no moving sun, four or five states later.
- Standard: ER-NIGHT-03: rain changes who is out, heard and seen, the same way every time Test: S: the same seed dry, drizzle, rain
- Source: DESIGN §6 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §6 (ER-NIGHT-03); RULINGS 5 Oct and 7 Oct; DEFINITIONS G9
- Status: decided. Coverage row: 2.1.4.

### 2.1.5 Crowd movement and avoidance

- How it works: Named only; not designed beyond: the crowd walks round people and things without clipping or jamming, looks before stepping into the road and uses the crossings; nobody steps into the road within 23 m of a car at 30 mph or less (G2). The test is 30 minutes walking through crowds with no clipping or jams, plus screenshots. Avoidance distances and step-aside timing are still to be timed from reference footage (PC, 26 to 28 Nov).
- Standard: none yet: avoidance distances and step-aside timing to be measured; the checklist's civilian behaviour items as acceptance checks Test: B: 30 minutes walking through crowds, no clipping or jams; H screenshots
- Source: MASTER-CHECKLIST A12, A13 (no numbers) (no reference figure yet). Designed in: DESCRIPTION-COPY-2 §5; DEFINITIONS G2; MEASUREMENTS-NEEDED A4; PARTS-TREE 2.1.5
- Status: unmeasured. Coverage row: 2.1.5.

### 2.1.6 The town's calendar

- How it works: The game runs from Monday 15 October 1990. Thursday is market day in Copper Row and empties the Hook's shops; Saturday's match fills the street at three and five; on Sunday the shops shut and the chapel is busy. Two dated days: Bonfire Night (a display on the quay, adults only), taken as Monday 5 November, and Remembrance Sunday at the chapel on 11 November, both in week 4 of the 7-week calendar. Nobody speaks of real people or news; the invented local poll-tax campaign may be talked about. After the ending the town repeats its ordinary weeks with no special days beyond Christmas Day.
- Standard: No real people or events spoken of (canon: no real people); no children (canon) Test: S: routines change on the calendar days; content gate; addendum rules ER-CAL-01 to 02
- Source: canon (his ruling or canon). Designed in: DESIGN-ADDENDUM A20; DESCRIPTION-COPY-2 §5; DEFINITIONS CLK-06, RT2-21; canon (Brands, content rule)
- Status: measured. Coverage row: 2.1.6. Conflicts settled: C-037.

### FIT-G9 Crowd counts by hour and place

- How it works: People in view over Quay Street's parade front (100 m, both pavements), by hour, rescaled to GD-02: 05:30 to 07:00, 5 to 8; busy bands 08:00 to 09:30, 12:00 to 14:00 and 16:30 to 18:00, 12 to 20; other daytime hours 6 to 12; 18:00 to 22:00, 5 to 10; 22:00 to 01:00, 2 to 5; 01:00 to 05:30, 0 to 2 besides the constable; the quay road by the fish dock 05:30 to 07:00, 10 to 18. Rain halves each band; Thursday's market takes a third off the shops' daytime bands; Saturday's match doubles the street at 15:00 and 17:00 for half an hour (up to 30, the archive's event-night top). Counts sampled each game hour fall inside the band in dry weather and inside half the band in rain. These are stretch counts, more than one camera frame holds (a frame is 4 to 10, see GD-02).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS design pass 3 G9; design pass 4 'The crowd against the counted views' and Run 5 second pass (stretch counts stay as rescaled)
- Status: pending. Coverage row: FIT-G9. Conflicts settled: C-038.

### FIT-G10 Opening hours, day and night

- How it works: Shops on Quay Street 09:00 to 17:30 Monday to Saturday, shut on Sunday (Shops Act 1950); the newsagent 06:00 to 18:00 and Sunday 07:00 to 12:00; the caff 06:00 to 15:00 Monday to Saturday, to 22:00 on Friday and Saturday; the chip shop on the parade 11:30 to 14:00 and 17:00 to 23:30 (to 00:30 Friday and Saturday); the launderette 08:00 to 23:00; the pawn 10:00 to 17:00 with its back room by knock to 22:00; the boxing club 18:00 to 21:30 Monday, Wednesday, Friday and 10:00 to 13:00 Saturday; the chapel hall's Tuesday evening 19:00 to 21:30; a tea stall at the dock gate 22:00 to 06:00; the ferry landing's window 22:00 to 01:00. Nothing serves drink and nobody plays for money. At 23:00 at least three places are open with people in them.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §G10; FIT-CHECK F11, P28; canon (content rule)
- Status: decided. Coverage row: FIT-G10.

## 2.2 Perception

The moat: every act exposes seven slots; identification climbs five rungs.


### 2.2.1 Seven slots per act

- How it works: Every act exposes seven slots a watcher may catch or miss: the precursor (a torch beam, a man hanging about), the draw (a weapon coming out), the act, the victim, the actor, the flight and the aftermath (broken glass, a body). A person who caught only the aftermath knows only that something happened. Offers, threats, promises and lies are acts with the seven slots too.
- Standard: Every act exposes seven perceivable slots (canon) Test: S: PerceptionGolden rows
- Source: canon The moat (his ruling or canon). Designed in: canon (The moat); DESIGN §2; DESCRIPTION-COPY-2 §5 (What a person catches); DEFINITIONS RT-14
- Status: measured. Coverage row: 2.2.1.

### 2.2.2 Identification ladder

- How it works: What a witness knew of who did it climbs five rungs: someone, a shape, a mark (the coat, the car, a limp, a bruise), a face, recognition. Recognition is gated by knowing him, never by distance and light alone: a stranger who saw his face clearly at 5 m can describe it but never name Tom. A person knows Tom for good only by four triggers (spoken to face to face, rode as his fare, somebody they know named him in his sight, or saw his face at 8 m or less in light 0.7 or more at the office on two different days). A face seen once can be matched later ('that's the man') and pointed out to the police, but not named until told.
- Standard: Five rungs; recognition gated by relationship, never by distance and light alone (canon) Test: S: golden rows
- Source: canon The moat (his ruling or canon). Designed in: canon (The moat); DESIGN §2; DEFINITIONS RT2-03; DESCRIPTION-COPY-2 §5
- Status: measured. Coverage row: 2.2.2.

### 2.2.3 Sight by distance and light

- How it works: A watcher sees a shape at 35 m, a mark at 18 m and a face at 8 m, and recognises Tom at 25 m only if they know him. Light scales it: daylight 1, a lamp 0.7, an unlit street 0.25, a doorway 0.12. A glance takes 0.35 s and knowing who it was 1.2 s; running doubles how fast he is noticed; the head turns at the start of the 1.2 s, so there is at least 0.8 s of warning. If Tom can tell a person faces him and he is in light, that person can see him. A still figure in a doorway counts at 0.12; among three or more people within 2 m a glance takes 0.7 s.
- Standard: DESIGN first values (35, 18, 8, 25 m; light 1, 0.7, 0.25, 0.12); ER-EYES-02 symmetry Test: S: figures at 8, 18, 35 m
- Source: DESIGN §2 (LEDGER's own first values) (waits on a dated study). Designed in: DESIGN §2 (ER-EYES-02, -03); DESCRIPTION-COPY-2 §7; DEFINITIONS RT2-03, RT2-16
- Status: pending. Coverage row: 2.2.3.

### 2.2.4 Sound reach

- How it works: Sound reach is set by the act, the hour and the rain. A footstep at 3 am carries about 3.6 m and at noon nothing; the car is heard within about 44 m by day and much further at night; the horn about 60 m by day; a shot about 177 m by day; a forced door or broken glass at the force reach, the loudest thing in a quiet street. Sound carries twice as far in the small hours, and rain cuts all of it. A searched drawer is heard at about 2 m, a forced cupboard about 10 m at night.
- Standard: Footstep at 3 am about 3.6 m; car 44 m by day; shot 177 m by day (DESIGN) Test: S: reach rows by act, hour and rain
- Source: DESIGN §2, §5, §7 (no reference figure yet). Designed in: DESIGN §2, §5, §6, §7; ONE-SHOT-PROMPT 8 (Light, noise and time); DESIGN-ADDENDUM
- Status: unmeasured. Coverage row: 2.2.4.

### 2.2.5 Give-away rules

- How it works: Each give-away makes a witness catch more than the same act without it: running; the same coat as last night; blood until washed with water in private (the launderette washes a coat too and remembers it); dirt; a weapon in the hand (watchers scatter once one is out); clothes wrong for the door he knocks at; bruises, a cut lip or a limp; a holdall; the car. A deed done from the car always names the car; the coat buys doubt about the face and none about the car. CCTV is rare (the bank's; a second site is his, Q10), its tape recycled weekly.
- Standard: ER-EYES-10 Test: S: golden rows per give-away
- Source: DESIGN §2 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §2 (ER-EYES-10); DESCRIPTION-COPY-2 §7; canon (Era)
- Status: decided. Coverage row: 2.2.5.

### 2.2.6 Ground rules and trespass

- How it works: Every place carries a label: public, open by hours, private or forbidden. Public is free; open by hours is free in its hours and private out of them. In a private place the owner or a neighbour warns, warns again, then calls someone or acts, within half a minute at worst; the warnings reset but the sighting is kept for good. Forbidden places (the customs shed, the Harbour Board's back office) skip the first warning. Force on a door is loud and shows for a day.
- Standard: Rooms labelled by privacy with a night rule; a challenge warns, warns again, then acts within half a minute (DESIGN §4) Test: S: every place has a label and the warnings fire in order; addendum rules ER-GROUND-01
- Source: DESIGN §4 (no reference figure yet). Designed in: DESIGN §4; DESIGN-ADDENDUM A10; DESCRIPTION-COPY-2 §8
- Status: unmeasured. Coverage row: 2.2.6.

### RT2-03 What makes a person know Tom

- How it works: A person knows Tom for good once any one of four things happens: he speaks to them face to face in talk; they ride as his fare; somebody they know names him while he is in their sight; or they see his face (8 m or less, light 0.7 or more) at the office counter or Mickey's door on two different days. Everyone staged in the first hour as meeting him knows him from that meeting. Knowing gates recognition at 25 m and the name ladder. A person who saw his face once but does not know him can say 'that's the man' on seeing it again within 8 m and point him out to the police, but cannot name him until told.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-03 Test: B (bot), as written under RT2-03
- Source: design pass 3, RT2-03 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-03; canon (The moat); DESCRIPTION-COPY-2 §5, §26
- Status: decided. Coverage row: RT2-03.

## 2.3 Memory

Permanent per-person memory.


### 2.3.1 Per-person memory store

- How it works: Every person's memory (what they saw, heard and were told) is permanent and per person: nothing is wiped by time, a save and load, or skipped hours. Remediation is behavioural: a man can be talked round, paid, frightened or befriended but still remembers. A crowd extra who catches a slot becomes a kept person with a fixed face, coat, home and routine, saved with the town. The station keeps what was signed, every plate noted and every description.
- Standard: ER-EYES-07: every memory survives save, load and skipped time Test: S: SaveChaos; reload at random moments and compare
- Source: canon; DESIGN §2 (his ruling or canon). Designed in: canon (The moat); DESIGN §2 (ER-EYES-07); DEFINITIONS RT2-10, RT2-16
- Status: measured. Coverage row: 2.3.1.

### 2.3.2 Witness certainty

- How it works: A witness is only as sure as what they caught: a noise or a shape is suspicion, never 'he did it'. A shopkeeper who saw a man in a dark coat says 'a man in a dark coat, could have been anyone', even if Tom was the only man in the street. A told version is weaker than the seen one ('Ada saw him' is sure, 'Ada told me' less, a third telling a guess), and Tom's Ledger shows the same: said to his face is sure, saw them looking is 'thinks so', two heads together is 'guesses'.
- Standard: ER-EYES-06; ruling 30 Sep Test: S: golden rows
- Source: ruling 30 Sep; DESIGN §2 (his ruling or canon). Designed in: RULINGS 30 Sep; DESIGN §2 (ER-EYES-06); DESCRIPTION-COPY-2 §5, §20; ONE-SHOT-PROMPT Who tells whom
- Status: measured. Coverage row: 2.3.2.

## 2.4 Gossip

Talk passing between people who meet; the engine, never the show.


### 2.4.1 Transmission

- How it works: Talk passes only between people who know each other and meet, within 6 m, weaker with each telling (about 0.8 per hop against a 0.2 floor, so a story fades by about seven hops). In the town code talk passes every 6 game minutes, only between people the cast ties together and puts in the same place that hour; a deed seen by one of the principals reaches about five of the nine on its first day and then stops. The paper carries news beyond the routines' meetings at the strength Alison wrote. How a deed was done (restraint or cruelty) travels with the telling.
- Standard: Within 6 m, weaker each telling (the Core's rule); about 0.8 per hop against a 0.2 floor (PLAYERS standards list) Test: S: golden rows; Soak
- Source: canon; C# Core; map-players (reference game). Designed in: DESIGN §2; ONE-SHOT-PROMPT Who tells whom; GTAVI-MAP GV-06; PARTS-TREE map-players S6
- Status: measured. Coverage row: 2.4.1.

### 2.4.2 Cooling by kind

- How it works: Talk cools by kind, about 1 to 7 game days: a scuffle or lift a day or two, a break-in about three, a wounding or robbery about a week; a hit-and-run 3 game days, an officer struck 7; a body or a killing never cools, and the person who saw keeps it for good. A told version cools like the seen one. This replaces the Core's single 96-hour half-life and needs new golden rows. KCD2's wanted status fades in a few in-game days; RDR2's bounty stays until paid. Under the 60 s clock talk cools in 24 real minutes to 2.8 real hours.
- Standard: 1 to 7 game days by kind (a lift or a scuffle a day or two, a break-in about three, a wounding or robbery about a week), replacing the Core's single 96-hour half-life; a told version cools like the seen one; slots shed by GV-02. Test: S: new golden rows
- Source: CLOUD-FIGURES-2026-11-21.md C1: KCD2 wanted fades within a few in-game days (GamerBlurb, PC Gamer, Gfinity 2025); RDR2 bounty held until paid (rdr2.org 2023); GTA VI clues shed by change (Vice, GamesRadar 2026) (reference game). Designed in: DESIGN §2; CLOUD-FIGURES C1; DEFINITIONS RT2-16, CLK-07; ONE-SHOT-PROMPT Who tells whom
- Status: measured. Coverage row: 2.4.2. Conflicts settled: C-039.

### 2.4.3 Showing what people know

- How it works: Everyone who knows something of Tom shows it on one ladder: notice, watch, comment, avoid, refuse, confront. It is posture first: half-recognition, lying and having heard of Tom show in how a person stands before a word is said. A woman at the bus stop looks a beat too long; the grocer serves him without a word; a docker crosses the road; a man says 'you want to watch yourself, son'. The step shown matches what the person holds (a told version never above a seen one), and someone who knows nothing shows nothing.
- Standard: Every person who knows something of Tom shows it on that ladder before any line; nobody who knows nothing shows it; the step shown matches what they hold (a told version never above a seen one). Test: B: seeded deed, then a walk past 30 people: each one's shown step is checked against their memory store.
- Source: The description, section 5 (What a person catches; Who tells whom). (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.4.3; ONE-SHOT-PROMPT Who tells whom; DESIGN §2
- Status: decided. Coverage row: 2.4.3.

### 2.4.4 It comes back

- How it works: In week one every answer to the outfit and every plainly seen deed is said to Tom's face by somebody he has met, within one game day (on paper at the old clock: the outfit's answer at minute 13 by Darren; a seen night 16 times in 16). Something must come back to him within his first 30 real minutes. Every reaction traces to a chain of sightings and tellings the test hook can print; there is no all-knowing town. At 60 s a game hour a game day is 24 real minutes.
- Standard: ER-EYES-08: in week one within one game day; and within the first 30 real minutes at the playing clock (gossip timeliness, map-players S4) Test: S: 16 seeded weeks; timeliness at the playing clock
- Source: DESIGN §2; PLAYERS second study (reference game). Designed in: DESIGN §2 (ER-EYES-08); ONE-SHOT-PROMPT Who tells whom, S06; PARTS-TREE map-players S4; DEFINITIONS clock
- Status: measured. Coverage row: 2.4.4.

### 2.4.5 The paper and the news

- How it works: The local paper (its name owed by the brand bible) comes out twice a week. Its local page carries only what Alison Sedman knows and chose to write, so a story about Tom is only as sure as what she was told. It lies on the caff's counter and in people's hands; readers know it at the strength she wrote it. Letters open on screen as a page and go into the Ledger (the solicitor's letter from Agar's side, the VAT letter in Act III, notes left at the office). No real people, events or brands in print.
- Standard: The press works only through a person, Alison (D56); a story prints only what she knows (canon moat) Test: S: every printed line traces to what Alison was told or saw; addendum rules ER-PAPER-01
- Source: D56; DESIGN §11 (his ruling or canon). Designed in: DESIGN-ADDENDUM A19; DESCRIPTION-COPY-2 §5; DESIGN §11 (D56)
- Status: measured. Coverage row: 2.4.5.

## 2.5 Witnesses after a deed

What people do once they have seen something.


### 2.5.1 The walk to tell

- How it works: A witness who means to tell sets off to a friend, a phone box or the station, and is seen going. No mobiles in 1990, so the walk is the timer: when it starts in Tom's sight it lasts at least 30 real seconds (50% longer with the assist). 'Oi!' stops a walker for about 2 s. A call from the phone box brings the constable to the spot that night; the signed statement is made at the station at nine next morning, and until she has signed Tom can still reach her.
- Standard: No mobiles in 1990: the walk is the timer; at least 30 real s in Tom's sight (ER-EYES-04) Test: S: walk timed and visible
- Source: canon era; DESIGN §2 (his ruling or canon). Designed in: DESIGN §2 (ER-EYES-04); DESCRIPTION-COPY-2 §16; DESIGN-ADDENDUM A10; DEFINITIONS RT2-19
- Status: measured. Coverage row: 2.5.1.

### 2.5.2 Stopping a witness

- How it works: Tom can reach a witness first and talk her round, pay, threaten, help or let her go. A threat can stop a report to the police, never the street's talk (she may not sign, but she will tell her sister). Paid, she remembers being paid; her temper decides how hard she is to pay or frighten. A neighbour who sees him put a window in reports him unless on his side (Ada's tea, a friend) or talked round. Mickey's people never go to the police about one of their own; Rita, Wayne, Hal, the scrap dealer, the customs officer and the outfit's man never go because of their trade.
- Standard: Ruling 3 Oct; ruling 1 Oct (neighbour reports unless on his side or talked round) Test: S: each answer's effect on the report and the talk
- Source: rulings 1 and 3 Oct (his ruling or canon). Designed in: RULINGS 1 Oct and 3 Oct; DESIGN §2, §8; DESCRIPTION-COPY-2 §16
- Status: measured. Coverage row: 2.5.2.

### 2.5.3 Crowd reaction to a deed

- How it works: After a seen deed, people within a few metres look, at least one gathers and drifts back, witnesses talk quieter for a game hour, and bystanders who saw a weapon flee. A person with the nerve (their temper) may step in, unarmed, at a hold-up or a beating in the street; Tom's line against women, the over-sixties and the priest holds if that person is one it covers.
- Standard: ER-EYES-09; ruling 23 Sep. Raised by Y2.6: a person with the nerve for it (their temper) may step in, unarmed, at a hold-up or a beating in the street; Tom's line holds if that person is one it covers. Test: S: after a seen deed, look, gather, quieter talk
- Source: ruling 23 Sep (his ruling or canon). Designed in: RULINGS 23 Sep; DESIGN §2 (ER-EYES-09); GTAVI-MAP Y2.6; DESCRIPTION-COPY-2 §16
- Status: measured. Coverage row: 2.5.3.

### 2.5.4 A street on edge

- How it works: Three seen deeds on one street within two game days set it on edge: doors locked earlier, windows watched longer, witnesses setting off to tell sooner, shops shut early, and the constable walking it more often (a second constable walks the same beat half a cycle behind, halving each gap to 2 minutes at Mickey's door and 4 at the yards' lane and landing). It eases as talk cools; the memories stay. One deed alone does not do it. It shows in people and doors, never a meter.
- Standard: rule: A burst of three seen deeds on one street raises its watchers' readiness to tell and the constable's visits, and both fall back as talk cools; one deed alone does not. Check S. Test: A burst of three seen deeds on one street raises its watchers' readiness to tell and the constable's visits, and both fall back as talk cools; one deed alone does not. Check S.
- Source: DESIGN-ADDENDUM-2026-11-20 A37 (from REFERENCE-MECHANICS-2026-11-20 M2.16) (reference game). Designed in: DESIGN-ADDENDUM A37; DESCRIPTION-COPY-2 §16; DEFINITIONS G5
- Status: measured. Coverage row: 2.5.4.

### 2.5.5 Finding an unseen deed

- How it works: Every unseen deed leaves traces (a forced door, glass, a missing thing, a body), and whoever's routine next brings them past finds it: the owner on his return, the cleaner at six, the first dock worker. The finder holds only the aftermath slot and reports or tells as a witness would. Nothing is found by a chance roll. A body hidden or sunk (put in the dock from the quay edge in 3 s) is never found, and the missing man becomes the town's question: his landlady asks, his mates at the dock gate ask, Ellis asks.
- Standard: rule: Every unseen deed with a trace where a routine passes is found by the first person whose routine passes it, and that person holds only the aftermath; a hidden or sunk body is never found. Check S: golden rows. Test: Every unseen deed with a trace where a routine passes is found by the first person whose routine passes it, and that person holds only the aftermath; a hidden or sunk body is never found. Check S: golden rows.
- Source: DESIGN-ADDENDUM-2026-11-20 A38 (from REFERENCE-MECHANICS-2026-11-20 M2.61) (reference game). Designed in: DESIGN-ADDENDUM A38; DESCRIPTION-COPY-2 §15; ONE-SHOT-PROMPT 14 (Death, bodies and the missing); DEFINITIONS RT2-11
- Status: measured. Coverage row: 2.5.5.

### GV-02 Shedding what a witness holds, slot by slot

- How it works: Each slot a witness can hold is shed its own way, and only against witnesses who have not yet told anyone: the coat (change it at the office), the car (the second car, the roof sign off, new plates or a respray), the face (a cap and scarf at night, a barber for a week), the companion (walk apart from Ron), the weapon (get rid of it). Gossip already carried is never undone, so a witness who told first still names it. Tom's guess of what each person holds of him shows in words on the Ledger's People page, never as icons. A cap or scarf is itself a mark by day.
- Standard: A changed slot no longer matches for witnesses who had not told; gossip already carried is never undone; the Ledger shows Tom's guess per slot in words. Test: B: deed, change one slot, meet the same witness: only that slot fails to match; a witness who told first still names it.
- Source: production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md (DECIDED by the design proof, for him to overturn). Designed in: GTAVI-MAP §GV-02; DESIGN-ADDENDUM A21; DESCRIPTION-COPY-2 §26
- Status: decided. Coverage row: GV-02. Conflicts settled: C-040.

### RT2-10 Crowd extras as witnesses

- How it works: A crowd extra who catches any slot of a deed becomes kept: given a fixed face, a coat and a home (a terrace in the Hook, or a district at the soft edge) and a routine from the crowd's hour windows, saved with the town. A kept extra remembers for good, can walk to the phone like any witness, can be found later at his routine's places and can be reached, paid or talked round. After seven game days with no open matter he lives at the soft edge and comes into the Hook only on his routine's days, but the police can still find and ask him.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-10 Test: B (bot), as written under RT2-10
- Source: design pass 3, RT2-10 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-10; DESCRIPTION-COPY-2 §5, §16
- Status: decided. Coverage row: RT2-10.

## 2.6 Police and law

A pressure Tom can read and answer, never the end of the game.


### 2.6.1 The beat constable

- How it works: At night (22:00 to 06:00) the beat constable walks a fixed two-part beat at 1.1 m/s: a short round of about 200 m (up Quay Street past Mickey's, round the bend to the yards' lane, down to the quay road and back; about 3 real minutes, Mickey's door tried) then a 240 m landing leg (about 3.6 minutes, the landing looked over for 15 s); the whole cycle about 7 real minutes. The beat never changes by chance, so the player can learn it. He is always heard or seen at least 3 s before he can challenge, and he calls out first. He challenges on suspicion: carrying at night, running, bloodied, or where he should not be. By day he walks Quay Street and the north road to the cold-store road. A rattled bin moves him off the beat and he rejoins it where he left.
- Standard: Heard or seen 3 s before a challenge; calls out first (ER-POL-02) Test: S and H: the challenge announced
- Source: DESIGN §8 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8 (ER-POL-02); DEFINITIONS G5; DESCRIPTION-COPY-2 §18; ONE-SHOT-PROMPT 21
- Status: decided. Coverage row: 2.6.1. Conflicts settled: C-041.

### 2.6.2 Challenge and search

- How it works: Stand, and he searches: he finds exactly what is under the coat and in the hand, and what he finds he keeps. Run, and it is a chase. Or a word: talked round if he has no cause; a note offered works on one of the two bought men; offered to an honest one, it is a crime he saw. A foot chase that ends with his hand on Tom's collar is searched as if Tom had stood: nothing found and no cause beyond running gives a name taken and a word; a weapon, stolen goods, the envelope, a signed statement or a deed the officer saw gives an arrest. The next challenge by that officer is on cause.
- Standard: DESIGN §8: stand and be searched, run and it is a chase Test: S: a search finds what is carried
- Source: DESIGN §8 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8; DESIGN-ADDENDUM A13; DEFINITIONS RT2-22; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: 2.6.2. Conflicts settled: C-042.

### 2.6.3 Statements and the arrest rule

- How it works: Talk alone brings questions, never an arrest. An arrest needs a signed statement from someone who knew it was him, or an officer who saw it. A signed statement is made at the station at nine the morning after the call. An officer struck by Tom is a witness who knows it was him, so no statement is needed. A person who saw his face but does not know him can point him out to the police but cannot name him.
- Standard: ER-POL-01 Test: S: golden rows
- Source: DESIGN §8 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8 (ER-POL-01); DESCRIPTION-COPY-2 §17; DEFINITIONS RT2-02, RT2-03
- Status: decided. Coverage row: 2.6.3.

### 2.6.4 Custody as hours

- How it works: An arrest costs hours, never the game, and under 2 real minutes of play: a constable walks up (go with him, or run), the station, the duty solicitor (free), the hours pass. About 6 hours for a window (2 and a caution if he owns up), 8 for a wounding, 12 for a robbery, 22 for a killing, then released without charge or on police bail pending inquiries, or charged and remanded (PACE 1984 as it stood in 1990). Also 8 for a hit-and-run or an officer struck, 12 for a gun found at a War stop, 22 for an officer killed; a refused stop with no deed behind it is 2 hours and a caution (a charge the second time). The coat is kept if he wore it; never taken twice for one deed; the street sees him go. This sits inside PACE (24 hours, 36 for serious).
- Standard: About 6 h a window, 8 a wounding, 12 a robbery, 22 a killing, then released without charge or on police bail pending inquiries, or charged and remanded (the 1990 terms; "released under investigation" is later wording); under 2 real minutes; never twice for one deed (ER-POL-03). Inside PACE limits (24 h, 36 serious); 73% of 1984-87 detainees held under 6 h; 542 held over 24 h in 1990. Test: S: arrest timed
- Source: CLOUD-FIGURES-2026-11-21.md B2: Hansard 8 Jul 1987; Home Office bulletin 1991 via Statewatch; Bottomley 1991 via Kemp and others (real-world figure or published standard). Designed in: DESIGN §8; CLOUD-FIGURES B2; DEFINITIONS RT2-02, RT2-16, RT2-17; DESCRIPTION-COPY-2 §17
- Status: measured. Coverage row: 2.6.4. Conflicts settled: C-043.

### 2.6.5 DS Ellis and the four stages

- How it works: Ellis is already on the warehouse fire. She comes to Quay Street for a body, for a detective's crime once reported, and from the second day for talk once three people of Tom's day world pass on talk of his nights. Four stages, each with its sign: nothing; asking round (her name in the street's talk); investigating (an officer at his door, the office search with notice); a manhunt (a car on the street and his description said aloud). No stage is skipped unseen, and a manhunt's sign shows at least one game hour (60 real seconds) before an arrest. She falls one stage after two quiet game weeks with no new reported deed or charge (never below asking round once she has reached investigating); a manhunt falls to investigating after three days without a sighting.
- Standard: No stage skipped unseen; a manhunt's sign shows at least one game hour before an arrest (ER-POL-05, provisional on C5) Test: S: every route to a manhunt passes its signs
- Source: DESIGN §8; ending signs 30 Sep (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8 (ER-POL-05); DEFINITIONS RT-13, RT2-02; ONE-SHOT-PROMPT 21; RULINGS 30 Sep
- Status: decided. Coverage row: 2.6.5. Conflicts settled: C-044.

### 2.6.6 Armed response and the dial's police

- How it works: No armed officer before the dial reaches Fired. At Fired every reported gun call brings armed officers from the station, later than an ordinary call. At War at least one armed car works the Hook's streets, and stop and search happens on the street at two fixed points (the dock gate and the north road's junction at Quay Street's top) between 18:00 and 02:00; a gun found at a stop means arrest on the spot, 12 hours, a charge, the gun kept and Ellis up a stage. Beat constables carry only a truncheon. Nothing of this shows on any map.
- Standard: No armed officer before Fired; at Fired every reported gun call brings armed officers later than an ordinary call; at War at least one armed car is on the Hook's streets and searches happen on the street; none of it shown on any map. Test: B: the dial forced through each state with seeded gun calls; police responses logged.
- Source: The description, sections 21, 33; RT-12. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.6.6, RT2-02, RT2-17; DESIGN §7; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: 2.6.6.

### 2.6.7 Traffic police and stops

- How it works: One patrol car works the Hook by day and night on a route; more only at War. The Hook is a 30 mph town; traffic drives at 20 to 28 mph and the patrol is no faster than Tom's car on a straight. The patrol stops a driver doing 50 mph or more or any reckless act (a hit, the pavement, a red light at speed) in its sight; 31 to 49 mph draws a look and a noted plate, never a stop. A stop: the car flashes and sounds, the constable looks at the car and driver (a search if he has cause), notes the plate and gives a caution, under 2 real minutes; refuse and it is a chase. No fines as a system.
- Standard: Reckless driving in a police car's sight starts a stop; refusing it is a chase (DESIGN §5); no fines as a system (DESIGN §18) Test: S: a stop starts only on reckless driving in sight; ends within 2 minutes; addendum rules ER-TRAFFIC-01 to 02
- Source: DESIGN §5, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §5, §18; DESIGN-ADDENDUM A12; DEFINITIONS G2; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: 2.6.7. Conflicts settled: C-045.

### 2.6.8 Bought men and squaring the law

- How it works: Two named officers in the Hook can be paid or leaned on, each with a price and a limit: one looks away from a car once (£50), the other loses a statement once (£200). A constable's challenge can be answered with a note if he is one of them; offered to an honest one it is a crime he saw. Buying one is an act a colleague may see, and that colleague keeps it. A bought officer Tom strikes stops being bought for good. The station as a whole never changes.
- Standard: Police corruptible as individuals, never as a thesis (canon) Test: S: one bought officer, his limits; the rest of the station unchanged; addendum rules ER-BOUGHT-01
- Source: canon (his ruling or canon). Designed in: canon (content rule); DESIGN-ADDENDUM A13; DEFINITIONS G8, RT2-02; DESCRIPTION-COPY-2 §18
- Status: measured. Coverage row: 2.6.8. Conflicts settled: C-046.

### 2.6.9 Charges, bail and the office searched

- How it works: An arrest ends in a caution, or a charge and bail. A charge joins Ellis's case and is read at the ending; there is no court scene and no prison. Charges accumulate one per arrest that ends in a charge, and an office-search find adds one; Ellis's trade (giving her a rival) removes one. Once Ellis reaches investigating she may search the office once, always with notice the evening before (a constable's word at the door, Sheila's warning), and what is stored there counts for the case.
- Standard: An arrest is hours, a caution, or a charge and bail; no prison terms (DESIGN §8, §18) Test: S: a charge reaches the endings; a search finds what is stored at the office; addendum rules ER-SEARCHED-01
- Source: DESIGN §8, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §8, §18; DESIGN-ADDENDUM A13; DEFINITIONS RT-13, RT2-04; DESCRIPTION-COPY-2 §17
- Status: decided. Coverage row: 2.6.9. Conflicts settled: C-047.

### 2.6.10 Police after a deed

- How it works: A reported deed always brings an officer to its spot; a body brings tape, a torch at night and Ellis next morning. The spot is watched ground for the rest of the night, and the place stays warm for days: next morning a constable knocks along that street and asks at windows, and for two nights the spot is walked more often. After a lost chase the patrol searches the last-seen streets for 30 to 120 real s, slowly, lamp on the turnings, then waits on that road for the rest of the night; seen inside the search, the same chase resumes (design pass 4, DP5-C03). An anonymous 999 call brings a constable that night but never makes an arrest alone. Nothing on screen marks where he searches.
- Standard: rule: A reported deed always brings an officer to its spot, a body brings tape and Ellis next morning, and the spot is watched until morning. Check S. Raised by Y2.3: the place stays warm for days, not minutes: next morning a constable knocks along that street and asks at windows, and for two nights the spot is walked more often; no circle on screen. Test: A reported deed always brings an officer to its spot, a body brings tape and Ellis next morning, and the spot is watched until morning. Check S.
- Source: DESIGN-ADDENDUM-2026-11-20 A36 (from REFERENCE-MECHANICS-2026-11-20 M2.8, M2.30) (reference game). Designed in: DESIGN-ADDENDUM A36; GTAVI-MAP Y2.3 (bars raised); DESCRIPTION-COPY-2 §18; DEFINITIONS RT2-19
- Status: measured. Coverage row: 2.6.10. Conflicts settled: C-048.

### RT-13 Ellis's case model

- How it works: The case is a list of charges and talk. Charges accumulate one per arrest that ends in a charge; an office-search find adds one (possession or handling). Ellis's interest falls one stage after two quiet game weeks with no new reported deed or charge, never below asking round once she has reached investigating. A manhunt ends with an arrest, or after three game days with no sighting falls to investigating. Tom's day world is Ada, Alison Sedman, Philip Danby, Father Walsh, June Suddaby, Darren, and any regular he has called on or carried as a fare twice. The charges list read at the ending equals the arrests and finds.
- Standard: Stages move only on these rules, each with its sign; the charges list read at the ending equals the arrests and finds. Test: B: seeded deeds and quiet stretches; the stage log against the rules.
- Source: The description, sections 20, 21. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-13; DESIGN §8; DESCRIPTION-COPY-2 §17, §18
- Status: decided. Coverage row: RT-13.

### RT2-02 Attacking the police

- How it works: An officer Tom strikes is a deed with the seven slots and a witness who knows it was him, so an arrest needs no statement. Striking: arrested when next met (go with him, or run), 8 hours and always a charge, never a caution; Ellis's interest rises one stage, its sign first. Knocking one out and getting away: the same, and the manhunt's sign (his description said aloud) shows within the game hour. Killing one: the manhunt at once (its sign still shows at least a game hour before an arrest), 22 hours and a charge, which removes the best turn of every ending. Beat officers carry only a truncheon. A bought officer struck stops being bought for good. Tom never lays hands on a woman officer or on Ellis.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-02 Test: B (bot), as written under RT2-02
- Source: design pass 3, RT2-02 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-02, RT-09, 2.6.4
- Status: decided. Coverage row: RT2-02.

### RT2-16 Police memory and arrest hours for road deeds

- How it works: Each officer remembers like anyone else, for good; the station keeps what was signed, every plate noted and every description. A patrol acts on a description only while the deed is hot in talk (a hit-and-run 3 game days, an officer struck 7, a killing never cools). An officer who knows Tom recognises him at 25 m; one with only a description stops a man who matches two marks (the coat and the car, the coat and a limp) within 18 m in light 0.7 or more while the deed is hot. A noted plate is known for good, and while its deed is hot the car is stopped on sight. Arrest hours: hit-and-run 8 hours and a charge; striking an officer 8 hours and a charge; a refused stop with no deed 2 hours and a caution (a charge the second time).
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-16 Test: B (bot), as written under RT2-16
- Source: design pass 3, RT2-16 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-16, 2.4.2; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: RT2-16.

### RT2-17 A gun found in a stop at War

- How it works: At War the police stop cars at two fixed points (the dock gate and the north road's junction at Quay Street's top) between 18:00 and 02:00, so the player can learn them. A gun found on Tom or in the cab at any stop: arrest on the spot, 12 hours, always a charge, the gun kept, Ellis's interest up one stage. A crewman driving a firm car with a gun in it is arrested instead and may break past his nerve.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-17 Test: B (bot), as written under RT2-17
- Source: design pass 3, RT2-17 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-17, 2.6.6; DESCRIPTION-COPY-2 §18, §27
- Status: decided. Coverage row: RT2-17.

### FIT-G5 The beat constable's round

- How it works: At night the beat constable walks a fixed two-part beat at 1.1 m/s: a short round of about 200 m (up Quay Street past Mickey's, round the bend to the yards' lane, down to the quay road and back to the street's foot, about 3 real minutes, Mickey's door tried) and a landing leg of 240 m (about 3.6 minutes, 15 s looking over the landing), the whole cycle about 7 real minutes under either clock. Mickey's door is in his sight at least every 4 real minutes, the yards' lane and the landing every 7.5; with the street on edge a second constable walks half a cycle behind and the gaps become 2 and 4. The beat never changes by chance and two runs from the same save are identical; a rattled bin moves him off and he rejoins where he left. By day he walks Quay Street and the north road to the cold-store road.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §G5; FIT-CHECK F06, P53; DESCRIPTION-COPY-2 §18
- Status: decided. Coverage row: FIT-G5. Conflicts settled: C-049.

## 2.7 Money

Two pots: clean money in the fare book, night money in the tin.


### 2.7.1 Clean money and the fare book

- How it works: Clean money is in the fare book and can be spent anywhere. Every fare driven, by Tom or the firm's drivers, enters the book; rent (£18 every Friday) and drivers' wages (£90 a week each) leave it on their days. Tom starts with £23.50. In Act I each driver's own fares bring the book about £85 to £95 a week, so the two drivers about cover their wages and the book alone does not pay Friday's rent; a week of Tom's own fares does. The book's balance always equals its flows, and it never goes below zero.
- Standard: Every fare driven, by Tom or the firm's drivers, enters the book; rent and wages leave it on their days; the book's balance always equals its flows (ER-MONEY-01). Test: B: a week of fares and wages; the book audited against the flows.
- Source: The description, section 24; RT-17. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.7.1, G8, RT-17, RT2-06; DESIGN §9; DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: 2.7.1.

### 2.7.2 Night money and the tin

- How it works: Night money is in the tin at the office and cannot be explained. Every night job's take goes to the tin or the pocket, never the book except through the count, and nothing turns the book back into tin. The tin can be lost only by being stolen in an office break-in or found in the office search, and that is said in words. Night money spent where it can be seen to be explained (a car, a front's share) is a lie someone may one day have to hold up. A man's night cut is agreed in talk and paid from the tin.
- Standard: Every night job's take goes to the tin or the pocket, never the book except through the count; the tin can be lost only by being stolen or searched, said in words. Test: B: night jobs then the count; a break-in on the tin.
- Source: The description, sections 24, 26; RT-17. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.7.2, RT-17; DESIGN §9; DESCRIPTION-COPY-2 §20, §22
- Status: decided. Coverage row: 2.7.2.

### 2.7.3 The wash

- How it works: At the count with Sheila, once a day and in twenty seconds, the fare book can hide £10 plus 80% of the fares really driven since the last wash, by Tom and by the firm's drivers. Over that, Sheila says so first ('That's more than the book will stand, love. You sure?'), thinks less of him, and each week over is recorded for the Act III inspection. A front's till raises the limit by a set amount a week. While the licence is suspended the count washes only the £10.
- Standard: The count never washes over the limit without Sheila's warning first; each week over is recorded for Act III; a front raises the limit by its set amount. The 80% and the front's amount are balance figures checked against GD-07's money curve. Test: B: counts at, under and over the limit; the record read by RT-01's grading.
- Source: The description, sections 26, 31; GD-07. (waits on a dated study). Designed in: DEFINITIONS §2.7.3, RT2-18; DESIGN §9 (ER-MONEY-04); DESCRIPTION-COPY-2 §21
- Status: pending. Coverage row: 2.7.3.

### 2.7.4 Rent and running costs

- How it works: Rent is £18 every Friday, owed to the landlord's agent, a named man who calls at the counter; drivers' wages (£90 a week) come out of the book weekly. Doing nothing misses Friday's rent; a week of Tom's own fares alone pays it. A missed Friday becomes arrears said in the Ledger and by the agent on Monday; two missed: a letter and notice to quit the flat above in a fortnight; three: the flat is let and Tom sleeps in the office. The office itself is never lost, and paying arrears ends the ladder. A car hit at about 35 mph is off the road for a day.
- Standard: Doing nothing misses Friday's rent; a week of fares alone pays it (ER-MONEY-03). The £18 rent sits in the 1990 band: council £23.36 a week (Apr 1990), private £65 (1991); cab running costs from 1990 fares (about £1.04 a mile London cab) and diesel about 45p a litre. Test: S: both weeks scripted
- Source: CLOUD-FIGURES-2026-11-21.md B1: Hansard 27 Jun 1990, 15 Apr 1993, 30 Jan 1992, 18 May 1990 (real-world figure or published standard). Designed in: DESIGN §9 (ER-MONEY-03); CLOUD-FIGURES B1; DEFINITIONS RT-16, G8; DESIGN §5
- Status: measured. Coverage row: 2.7.4. Conflicts settled: C-050.

### 2.7.5 Purses, tills and shops

- How it works: Everybody's money is somebody's circumstance: a debtor, a shopkeeper or a fence pays only what is in the purse or the drawer. Shops keep hours, restock weekly, and Thursday's market empties them. A shop buys, haggles or refuses, and remembers a robber, a man who walked out of a haggle, a man who robbed the shop next door. A haggle is three offers at most: the buyer names a price, Tom asks more, takes it, or walks; the buyer's answers come from his purse, how hot the goods are and how he regards Tom; no number shows except prices spoken. Walking away is remembered. No price tables, stock or supply chains.
- Standard: Purses and a weekly restock stay; no price tables or supply chains (DESIGN §18) Test: S: a shop refuses and remembers; addendum rules ER-HAGGLE-01
- Source: DESIGN §9, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §9, §18; DESIGN-ADDENDUM A30; DESCRIPTION-COPY-2 §14; DEFINITIONS G10
- Status: decided. Coverage row: 2.7.5.

### 2.7.6 Fencing

- How it works: Rita's back room (open from rung 2) buys hot goods at about a third of retail (0.33): about 0.2 for jewellery up to 0.4 for a video recorder, less for each further piece the same week. Buyers differ: the second-hand shop takes radios and video recorders, the scrap yard car parts, a man at the back of the caff jewellery, and Wayne's pawn takes goods too; each is also a listener. Rita refuses or lowballs goods whose deed is still hot in talk. A haggle is three offers at most, and no price table shows.
- Standard: About a third of retail (0.33), from 0.2 for jewellery to 0.4 for a video recorder; less for each further piece the same week; buyers differ in what they take (second-hand shop radios and video recorders, scrap yard car parts, a man at the back of the caff jewellery); each is also a listener. No price table on screen. Test: S: golden rows
- Source: CLOUD-FIGURES-2026-11-21.md B3: Sutton 2014; AIC 2002; BOCSAR 1998 (real-world figure or published standard). Designed in: CLOUD-FIGURES B3; DESIGN §4, §9; GTAVI-MAP Y2.7; DESIGN-ADDENDUM A30; DESCRIPTION-COPY-2 §14
- Status: measured. Coverage row: 2.7.6. Conflicts settled: C-051.

### 2.7.7 Flows ledger

- How it works: No money from nowhere: every pound in or out is a flow from a person, a purse, a fare, a till, a wage or a bribe, and every pound balances. The firm's takings are said when they come in. Tom always knows in words what he has and what is owed by Friday, for example '£31 in your pocket. The tin has about £40 in it. Rent, £18, Friday. Darren still owes £12.'
- Standard: ER-MONEY-01 Test: S: no money from nowhere
- Source: DESIGN §9 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §9 (ER-MONEY-01, -02); DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: 2.7.7.

### 2.7.8 Spending

- How it works: Money buys position, spoken by the seller and never shown as a table. The newsagent and tobacconist (20 cigarettes £1.70, the paper 25p), the caff (tea 30p, a meal £2.50), the ironmonger (crowbar £6, torch £4, key cut £1.50), coats (second-hand £15, the decent jacket £45, the good overcoat £90), the barber £4, a used car £600 to £1,200, the retired doctor's stitches £20, a solicitor's brief £50 a week, a bought officer £50 or £200, a man's night cut £10 to £40. Each shop sells only its list, by its hours, from its purse.
- Standard: What money buys is position (DESIGN §9); purses and weekly restock, no price tables (DESIGN §18) Test: S: each shop sells its list; H: 'what did you spend on?'; addendum rules ER-SPEND-01
- Source: DESIGN §9, §18 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN-ADDENDUM A21; DEFINITIONS G8; DESCRIPTION-COPY-2 §14; DESIGN §9, §18
- Status: decided. Coverage row: 2.7.8.

### GD-07 Economy over weeks: what money buys and how it rises across 15 to 20 hours

- How it works: Money buys position, never numbers. Act I: £23.50, rent £18 a week, a week of fares pays it, the debts £156. Act II: what money buys rises with the rung (a third car, a driver's wage, men's cuts, a front's share, a bribe to a bought man, the decent jacket, the good overcoat, the doctor). Act III: money cannot buy the books clean. Sinks never run dry before Act III: at each act's end, for a greedy and a lazy bot, one named thing on the rung ladder is still out of reach. A car on a good rank brings £110 to £140 a week from rung 2.
- Standard: The players study punishes money with nothing to buy (GTA V and RDR2 late game). Pass: at each act's end, in both a greedy and a lazy bot playthrough, at least one named thing on the rung ladder he does not yet hold is still out of reach of his money; the curve's shape is set from the reference games' money over a playthrough. Test: B: an economy bot playing greedy and lazy; the curve plotted against the rung ladder.
- Source: The description, sections 24, 28, 31, 32; MEASUREMENTS-NEEDED A (money over a playthrough); PLAYERS-KCD2-GTAV-RDR2 complaints. (waits on a dated study). Designed in: DEFINITIONS §GD-07, G8; DESCRIPTION-COPY-2 Economy over weeks; FIT-CHECK F24
- Status: pending. Coverage row: GD-07.

### RT-16 Missed rent

- How it works: Rent is owed to the landlord's agent, a named man who calls at the counter. A missed Friday becomes arrears said in the Ledger and by the agent on Monday; two missed: a letter and notice to quit the flat above in a fortnight; three: the flat is let to someone else and Tom sleeps in the office. The office itself is never lost, arrears can be paid at any time, which ends the ladder. No game over, no dead end.
- Standard: Each step on its Friday; paying clears it; the office itself is never lost at any point in the game (only the flat above). Test: B: the do-nothing run through three Fridays; a pay-late run.
- Source: The description, sections 24 (rent), 3 (no game over); the doing-nothing run of S23. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-16; DESIGN §9; DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: RT-16.

### RT-17 Money pots in practice

- How it works: Money is in three places: the pocket, the tin (night money at the office, which cannot be explained) and the book (clean money, spent anywhere). Rent and wages come out of the book weekly; a car, a front's share, shops and the doctor can be paid from the book or from cash; bribes and men's night cuts come from cash. The count turns tin money into book money within the wash limit; nothing turns the book back into tin. The tin can be stolen in an office break-in and is then gone, said in words. A constable's search finds what is under the coat and in the hand, cash included, and keeps what it finds.
- Standard: Every payment draws from a place the rules allow; the flows ledger balances (ER-MONEY-01); a search keeps exactly what was found. Test: B: every kind of payment from each place; a break-in; a night search with cash on Tom.
- Source: The description, sections 21 (what he finds he keeps), 24 (two pots; clean money spent anywhere), 26 (the count), 27 (cut from the tin). (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-17, §2.7.2; DESCRIPTION-COPY-2 §20 to §22
- Status: decided. Coverage row: RT-17.

### FIT-G8 Prices of what money buys

- How it works: Every item on the spending list has a price, spoken by the seller and never shown as a table (1990 prices, to be checked): 20 cigarettes £1.70; the paper 25p; tea at the caff 30p; a caff meal £2.50; a crowbar £6; a torch £4; a key cut £1.50; a second-hand coat £15; the decent jacket £45; the good overcoat £90; the barber £4; a used car £600 to £1,200; the doctor's stitches £20; a brief on call £50 a week; a bought officer £50 to look away once, £200 to lose a statement once. A driver's wage is £90 a week; a man's cut £10 to £40. In Act I each driver's fares bring the book about £85 to £95 a week; from rung 2 each car on a good rank brings £110 to £140.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS §G8; FIT-CHECK F24, P15; DESCRIPTION-COPY-2 §14
- Status: pending. Coverage row: FIT-G8. Conflicts settled: C-052.

### FIT-F24 Money over nine weeks (in against out; seven under the ruled clock)

- How it works: In week one Tom's own fares (about 18 at around £1.30) come to about £23, which covers the £18 rent, and the debts alone could bring £156; after week one there is nothing to compare, and the worry is money that stops mattering. The fix is G8's amounts for the spending list, then a money run over the whole calendar on the sim once the figures exist (cloud, by Sat 28 Nov). The related wash row (F25) needs night income, which has no amount; the count can hide at least £70 a week plus 80% of the firm's fares.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4) Test: B (bot) as written
- Source: design pass 3; FIT-CHECK-2026-11-21.md (waits on a dated study). Designed in: DEFINITIONS §G8, GD-07; FIT-CHECK F24, F25
- Status: pending. Coverage row: FIT-F24. Conflicts settled: C-053.

## 2.8 Debts

Mickey's debt book.


### 2.8.1 The five debtors

- How it works: Mickey's debt book holds five debts and five lessons, £156 in all: Darren Milner £22 (pays in what he hears); Wayne Harrison £30 (pays in goods from the pawn's back room, haggled); Lee Drewery £15 (stands, with the docks behind him, and it comes to blows); Julie Kettlewell £9 (cannot pay: mercy or shame); Dennis Iveson £80 (has the money, a yard and a yard hand in his twenties; three keys: front up the yard hand, the hut at night, or lean on what he bought out of the burned warehouse). In the first hour Tom can front Darren up, take what he hears, or strike the debt out.
- Standard: Each debt teaches a different answer (DESIGN §4) Test: H: the five debts named as different
- Source: DESIGN §4 (no reference figure yet). Designed in: DESIGN §4; ONE-SHOT-PROMPT 25, 4 (5:30); DEFINITIONS RT2-05
- Status: unmeasured. Coverage row: 2.8.1.

### 2.8.2 Partial payment and the book

- How it works: A debtor pays what his purse holds and the rest stays on the book, said in the Ledger's Money page ('Darren still owes £12'). Fronting up is a collection in person on the lower rungs: a stare, a word, a shove. Squeezing a debtor and letting a debt go are both told on the street, as a told version within a game day. A round, later, is the same collection repeated by a man of his crew.
- Standard: A payment never exceeds the debtor's purse; the remainder stays and is said in the Ledger's Money page; a squeeze or a let-off produces a told version within a game day. Test: B: each of the five debtors fronted up with different purses.
- Source: The description, section 25. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.8.2; ONE-SHOT-PROMPT 25; DESIGN §4; DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: 2.8.2.

## 2.9 The outfit and the arrangement

The run to the ferry landing that Mickey kept.


### 2.9.1 The asks

- How it works: In Act I the outfit asks on nights one, three, five and seven, at most one a night. Ron brings it in person after dark: a dark coat and an envelope for the ferry landing after ten. Tom can go, say no (asked twice), or stay away; staying away means Ron leaves the envelope with Sheila's word and the ask ends unanswered, written in the Ledger. No ask comes twice before it is taken. At the landing a man says 'Mickey's?', the hand-over plays and Tom's cut comes back into the tin. If a constable stops him and searches, the envelope is kept and the ask fails as a state the outfit hears of.
- Standard: At most one ask a night, every other night in Act I (DESIGN §6) Test: S: ask schedule in a seeded week
- Source: DESIGN §6, §16 (no reference figure yet). Designed in: DESIGN §6, §16; ONE-SHOT-PROMPT 4 (7:00 to 11:30), S04, S05
- Status: unmeasured. Coverage row: 2.9.1.

### 2.9.2 Keeping or ending the arrangement

- How it works: Kept (he went to the landing and took the firm on): the landing men hand him their end of the Hook in Act II and fade, the asks become his own runs, and he becomes what Mickey was: night money, cover and asks that grow. Ended (wound down or refused): the ground is open, every rival's ladder starts one rung up and each rival's first visit comes earlier on the game clock; freedom without cover. Winding down ends only Mickey's arrangement, never the cab trade. Both roads reach Act II at rung 2.
- Standard: Kept gives the hand-over beat; ended starts every rival one rung up; both reach rung 2 (RT-04). Test: B: week-one runs kept and ended; the Act II state compared.
- Source: The description, sections 36, 37; RT-04. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.9.2, RT-04, RT2-01; DESIGN §16; DESCRIPTION-COPY-2 §30, §31; ONE-SHOT-PROMPT S31
- Status: decided. Coverage row: 2.9.2.

### RT2-01 The cold-store contract and rung 3 are circular

- How it works: The contract comes before rung 3, never from it. The cold stores' shift manager (a named minor man) offers it once the firm has met the packing shift on time on five mornings in one game week and holds at least four cars; winning it opens the dock gate. Rung 3 is reached with five cars, a night desk, a first front, a first round and the contract. It is open on every road out of Act I, wound down included. It is lost after three missed mornings in one game week (its fares stop and the dock gate's daily pass goes, but no rung or name goes back), paused while the licence is suspended, and can be won again once, the same way.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-01 Test: B (bot), as written under RT2-01
- Source: design pass 3, RT2-01 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-01; DESIGN §14; DESCRIPTION-COPY-2 §25
- Status: decided. Coverage row: RT2-01. Conflicts settled: C-054.

## 2.10 Rivals

Three heads, each going after a different ledger.


### 2.10.1 Rival ladders

- How it works: Each rival climbs the same ladder: noticed, a visit, pressure, a threat, a sit-down. No rung is skipped and each is said to his face or shown on his street within a game day. Every climb is lifted from the rung below by a state: noticed by the first thing its people see or hear of Tom; a visit by two more sightings or tellings, or Tom reaching rung 2; pressure by refusing the visit, rung 3 or a deed against its men; a threat by defying or countering a pressure or a second deed; the sit-down by defying the threat, rung 4 or one of its men killed. Paying holds a rival two game weeks unless Tom does a deed against him.
- Standard: ER-RIV-02 Test: S: no rung skipped, each said or shown
- Source: DESIGN §13 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §13 (ER-RIV-02); DEFINITIONS RT2-07, RT-04; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: 2.10.1. Conflicts settled: C-055.

### 2.10.2 Rival eyes

- How it works: Each rival knows only what its own people saw or heard. Each has eyes among the regulars: Lee Drewery and Kevin Needham for the docks, Susan Coverdale for Agar, Rita Welburn for Cammack, so the first thing the Widow learns of Tom may come from his own day driver over a radio nobody can help overhearing. Every rival move traces to something one of its people saw or heard. Each rival has a base, a named lieutenant and three named men with routines.
- Standard: ER-RIV-01 Test: S: every rival move traces; ER-EYES-05 no all-knowing town: every reaction by a neighbour, the police or a rival prints its chain of sightings
- Source: DESIGN §13; Core rule (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §13 (ER-RIV-01); DESCRIPTION-COPY-2 §24; DEFINITIONS RT2-08
- Status: decided. Coverage row: 2.10.2.

### 2.10.3 Pressures and answers

- How it works: The Widow taxes his drivers at the dock gate and poaches his least loyal man; Agar sends paper (the licence letter, a solicitor's letter, an inspection of the cars); Cammack brings heat (trouble on Quay Street outside Mickey's). Every pressure has three answers: pay, defy, or counter with what he knows (which needs a hook Tom holds); none ends the game. At the threat rung each shows one harm in its style (the office window put in, a licence hearing date, car two's tyres slashed), all repairable for money and a day. Paying holds a rival on its rung two game weeks.
- Standard: ER-RIV-03: three answers, none ends the game Test: S: each pressure's three answers
- Source: DESIGN §13 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §13 (ER-RIV-03); DEFINITIONS RT-06, RT2-07, RT2-18; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: 2.10.3.

### 2.10.4 The Fixer

- How it works: Keith Garbutt, the Fixer, brokers between all three rivals and sells three things: true reads of a rival (true to what the town really holds at that moment), a meeting that then happens, and one truce that holds a rival at its rung for exactly two game weeks, offered once a game. He carries a pager: paged from a box, he rings that box back within half a game hour. His prices follow the economy curve.
- Standard: Every read he sells is true to the town's memory at that moment; a meeting he brokers happens; the truce holds exactly two game weeks and is offered once. His prices follow GD-07's curve. Test: B: reads compared with the rival's true state; truce timing.
- Source: The description, sections 29, 30; RT-06. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.10.4, RT-06, RT2-19; DESIGN §13; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: 2.10.4.

### RT-05 The two rivals not met at Act II's end

- How it works: After Act II's sit-down with one head, the two rivals whose ladders did not reach it keep their rung into Act III and their weekly pressure continues; neither is absorbed or defeated by the story alone. Act III's close names each: what they hold and what they call him.
- Standard: After the sit-down, both other rivals' rungs are unchanged by it, their weekly pressure continues, and the close names both. Test: B: an Act III run checking the other two ladders' state and pressure each day.
- Source: The description, sections 29, 37, 39. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-05; DESCRIPTION-COPY-2 §38
- Status: decided. Coverage row: RT-05.

### RT-06 Rival threat rung and counters

- How it works: At the threat rung each rival shows one harm in its own style, said to his face or shown on his property, never yet done to a person: the Widow's men put the office window in or tell a driver he will not drive again; Agar's solicitor names a date for the licence hearing; Cammack's lads slash car two's tyres on the rank. Property harm is repaired by people for money and a day (the glazier, the tyre man) and the street sees it. A counter spends a hook Tom holds. The Fixer's truce holds a rival two game weeks, once a game.
- Standard: Each rival's threat rung shows one harm in its own style; every harm repairable; a counter needs a hook Tom holds; a truce holds exactly two game weeks. Test: B: ladder runs to the threat rung for each rival; counter with and without a hook.
- Source: The description, sections 29, 30. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-06, RT2-18; DESCRIPTION-COPY-2 §24, §38
- Status: decided. Coverage row: RT-06.

### RT2-07 What moves a rival up his ladder

- How it works: Each rival rung is lifted by a state, from the rung below, never two, never by time alone: noticed on the first thing its people see or hear of Tom; a visit on two more sightings or tellings of his firm on that rival's ground, or Tom reaching rung 2; pressure on refusing the visit, rung 3 or any deed against its men or property; a threat on defying or countering a pressure or a second deed; the sit-down on defying the threat, rung 4 or one of its men killed. A deed against a rival lifts him one rung at once. Paying at a rung holds that rival there two game weeks unless Tom does a deed against him. Each climb is said to Tom's face or shown on his street within a game day. The only climb on time is the fail-safe.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-07 Test: B (bot), as written under RT2-07
- Source: design pass 3, RT2-07 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-07, RT-04, RT-06; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: RT2-07. Conflicts settled: C-056.

### RT2-08 Rivals as actors

- How it works: Each rival has a base inside the map, a named lieutenant and three named men with routines: the Widow a dock office over the fish dock's net store; Agar an estate agent's office on the cold-store road holding his papers; Cammack the lock-ups on the north road (east side, y 290 to 320). Sending men at a rival's property hits one thing: the base's windows and door, a vehicle (the Widow's van, Cammack's car) or a front or round of theirs. Each hit is a deed against that rival (he climbs a rung), leaves a mark until mended and points his next pressure at the crewman who did it. A night raid is a break-in with two or three of the base's men inside; what is found (the rival's book, a letter) can be used as a counter at the sit-down.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-08 Test: B (bot), as written under RT2-08
- Source: design pass 3, RT2-08 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-08, RT-07, RT-08; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: RT2-08.

## 2.11 Crew under the hood

Men who know: needs, nerve, loyalty, fates.


### 2.11.1 Recruiting

- How it works: Recruits come from the thirty regulars by two roads: meet a need (slow, holds; Julie Kettlewell, laid off, wants work and can drive) or spend a hook (quick, brittle). A need recruit's loyalty ceiling is higher and a hook recruit breaks sooner under the same pressure. Each brings a use the firm lacks: Ian Megginson's locks, Lee Drewery's fists, Norman Dent's nights on the warehouse row, Karen Grummitt's view of the ferry, Shaun Hewson's paint. Men who train at the boxing club can be recruited there.
- Standard: A need recruit's loyalty ceiling is higher than a hook recruit's; each named recruit brings the use the description gives (locks, fists, nights on the warehouse row, the ferry, paint); boxing club men can be recruited there. Test: B: both roads on two men; the same pressure applied; who breaks first.
- Source: The description, section 27; RT-07. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.11.1, RT-07; DESIGN §12; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: 2.11.1.

### 2.11.2 Nerve, loyalty and breaking

- How it works: Crew are named residents with a routine, a need, a nerve and a loyalty with a ceiling. Each man sent is a second person who knows: past his nerve he talks, to a rival or to the police, and the sign always comes first: he looks away, he asks for his cut early, he is not at his post. Paid short or late his loyalty falls; a hook recruit breaks sooner than a need recruit. A man at Tom's side never blocks a door or lane and never lags more than 10 s.
- Standard: ER-CREW-03 Test: S: sign before event in every seeded case
- Source: DESIGN §12 (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §12 (ER-CREW-03); DESIGN-ADDENDUM A40; DEFINITIONS RT-07; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: 2.11.2.

### 2.11.3 Crew fates

- How it works: Crew can be poached (the Widow takes his least loyal man), frightened off, arrested, docked or expelled by Tom, or killed for good. Each fate is reachable in play, becomes a told version and a Ledger line, and is a town fact. Drivers also leave if unpaid or frightened. Where the man held a post (the dock gate, the cold store, the landing), losing him loses the post.
- Standard: Each fate reachable in play; each produces a told version and a Ledger line; a poach always takes the least loyal man. Test: B: seeded runs for each fate.
- Source: The description, section 27. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.11.3, RT2-09; DESIGN §12; DESCRIPTION-COPY-2 §22
- Status: decided. Coverage row: 2.11.3.

### 2.11.4 Crew pay and the cut

- How it works: A driver gets a weekly wage (£90) from the fare book; drivers leave if unpaid or frightened. A man on a night job gets a cut (£10 to £40) agreed in a line of talk before it, paid from the tin. Going alone keeps the whole take but brings no second man. Paid short or late, a man's loyalty falls and he asks for his cut first, the sign before breaking; paid fairly he holds longer. Every pound paid out balances in the flows ledger.
- Standard: rule: S: a seeded night job paid short lowers that man's loyalty and he asks for his cut before any break; every pound paid out balances in the flows ledger. Test: S: a seeded night job paid short lowers that man's loyalty and he asks for his cut before any break; every pound paid out balances in the flows ledger.
- Source: DESIGN-ADDENDUM-2026-11-20 A40 (from REFERENCE-MECHANICS-2026-11-20 M7.8) (reference game). Designed in: DESIGN-ADDENDUM A40; DEFINITIONS G8, RT-17; DESCRIPTION-COPY-2 §22
- Status: measured. Coverage row: 2.11.4.

## 2.12 Position in the town

The rise under the hood: never a number.


### 2.12.1 The name ladder

- How it works: Each person uses the name they have reached: the new owner, then Nowak, then Tom, then Tommy (Tom to most and Tommy to two or three at rung 4). The gate is knowing, not liking: a man who fears him may still call him Tom. A step never goes back, and each step up is heard within a game day of being reached. Sheila withholds his name until she trusts him, which comes with a clean week in which he never asked her to put the books off (built so meanwhile; Q7 for him: a visible state rather than a day count).
- Standard: canon; ER-RISE-02 (heard within a game day, never goes back) Test: S: each step heard within a day
- Source: canon premise; ruling 29 Sep (his ruling or canon). Designed in: canon (Premise and cast); DESIGN §14 (ER-RISE-02); DESCRIPTION-COPY-2 §26; RULINGS 29 Sep
- Status: measured. Coverage row: 2.12.1.

### 2.12.2 Rung table

- How it works: Four rungs, each on exactly its holdings. Rung 1, the nephew: two cars, two drivers, Ron, Sheila, £23.50, the debt book; opens the street, the rank, the landing. Rung 2, Nowak: his answer to Sheila, a third car, a first recruit; opens Mickey's locked office and the real book (on trust) and Rita's back room. Rung 3, Tom: five cars, a night desk, a first front, a first round and the cold-store contract; opens the Harbour Board's counter and a solicitor. Rung 4, the port's man: fronts and rounds across the Hook (at least two of each), men at the dock gate, cold store and landing, a brief on call; opens the sit-down and people stepping aside.
- Standard: As RT-04: each rung on exactly its holdings; what opens at each rung opens then and not before. Test: B: rung climbs with holdings added one at a time.
- Source: The description, section 32; RT-04. (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §14; DEFINITIONS §2.12.2, RT-04, RT2-01, RT2-09; DESCRIPTION-COPY-2 §26
- Status: decided. Coverage row: 2.12.2. Conflicts settled: C-057, C-058.

### 2.12.3 Access and soft keys

- How it works: Access is by soft keys: standing, dress, an introduction, an appointment the Fixer brokers. The Harbour Board's counter refuses him in the arrival clothes and lets him in with the decent jacket (£45); any door that opens to him clean refuses him bloodied or filthy. Three outfits across the game (as he arrived, the decent jacket, the good overcoat £90) plus a dark coat for nights; the licensing hearing needs the decent jacket or better.
- Standard: Each soft key opens exactly its doors: the Harbour Board's counter refuses him in the arrival clothes and lets him in with the decent jacket; any door that opens to him clean refuses him bloodied or filthy. Test: B: the same doors tried in each outfit and state.
- Source: The description, section 32. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.12.3, RT2-18, G8; DESIGN §14; DESCRIPTION-COPY-2 §26
- Status: decided. Coverage row: 2.12.3.

### 2.12.4 Greetings by regard

- How it works: How the rise is heard in the street: greetings by regard (afraid, angry, knows and likes him, his appearance, neutral), at least 6 lines per situation per kind of speaker. A nod, a door held, a path cleared, 'morning, Mr Nowak', or a street that goes quiet. A person's own line is said once a day and a shared line once a week per street; everyday street talk comes at most every 45 s. Walked at rung 1 and at rung 3 the same street gives at least three differences a newcomer can point to.
- Standard: At least 6 lines per situation per kind of speaker (DESIGN §11) Test: H: same street walked at rung 1 and rung 3 (ER-RISE-03)
- Source: DESIGN §11, §14 (no reference figure yet). Designed in: DESIGN §11, §14 (ER-RISE-03); DESCRIPTION-COPY-2 §26; ONE-SHOT-PROMPT 32
- Status: unmeasured. Coverage row: 2.12.4.

### 2.12.5 Property that reacts

- How it works: Each rung changes at least three things a newcomer can point to. The office fills (a night desk, more phones, the board crowded) and the flat above stops being Mickey's; his cars pass him in the street. The rung 1 street and the rung 3 street, walked, differ in at least three listed ways.
- Standard: Each rung changes three things a newcomer can point to (ER-RISE-03) Test: H: office at rung 1 and rung 3 compared
- Source: DESIGN §14 (no reference figure yet). Designed in: DESIGN §14 (ER-RISE-03); DESCRIPTION-COPY-2 §26
- Status: unmeasured. Coverage row: 2.12.5.

### RT-07 Hooks and knowledge as leverage

- How it works: A hook is a fact Tom holds (a Ledger People line he is sure of) about a person which that person would not want told to a named other. He gets one by being told (Darren sells what he hears), seeing it himself, or from Mickey's real book. Spending it is one line of talk and buys a recruit (quick, brittle), an answer to a pressure, or a counter at a sit-down. A hook is spent once: the person now knows Tom knows and remembers. A 'guesses' line is no hook; using it is a bluff that works only if believed.
- Standard: Hooks exist only from a perceived source; spent once; a hook recruit breaks sooner than a need recruit under the same pressure. Test: B: recruit two men by each road and apply the same pressure; hook use logged.
- Source: The description, sections 24 (Ledger certainty), 27, 29, 30. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-07; DESIGN §12; DESCRIPTION-COPY-2 §38
- Status: decided. Coverage row: RT-07.

## 2.13 The escalation dial

Fists, shown, fired, war: a fact in the town's memory, not a meter.


### 2.13 The escalation dial

- How it works: The dial is a fact in the town's memory, not a meter, in four states: 0 Fists (nobody carries a gun); 1 Shown (a gun has been seen, news across town, the rivals' top men start carrying); 2 Fired (a shot heard to about 177 m by day, kept for good; armed officers come slowly; Ellis up a step); 3 War (a few named men on each side carry and everyone knows who; armed cars and stop and search; watchers run sooner, night fares fall; a shot can kill, each death named and permanent). Fired moves to War on a second shooting by a different side, a named man wounded by another firm's shot, or more than two of Tom's men seen carrying. It never moves on a deed nobody saw or heard, and falls one step after about two quiet game weeks, never back to 0.
- Standard: ER-FIGHT-08, ER-FIGHT-09 (guns and killing stay rare at every state); falls one step after about two quiet game weeks, never back to 0 Test: S: dial never moves on an unseen deed; War weeks counted
- Source: ruling 18 Nov; DESIGN §7 (his ruling or canon). Designed in: DESIGN §7 (ER-FIGHT-08, -09); DEFINITIONS RT-12; RULINGS 18 Nov; DESCRIPTION-COPY-2 §27
- Status: measured. Coverage row: 2.13.

### RT-12 Escalation dial War trigger

- How it works: Fired moves to War when the town learns of either a second shooting by a different side from the first or a named man of one firm wounded by a shot from another. Tom's men seen carrying (more than two, each seen by someone) also move it. Nothing that nobody saw or heard moves it. It falls one step after about two quiet game weeks, never back to 0.
- Standard: War only on these learned events; never on an unseen one; the fall rule as the description. Test: B: seeded sequences of shootings seen and unseen; the dial's state checked.
- Source: The description, section 33. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT-12; DESIGN §7; DESCRIPTION-COPY-2 §27
- Status: decided. Coverage row: RT-12.

## 2.14 Each person's temper

Nerve, loyalty and readiness to talk for each named person.


### 2.14 Each person's temper

- How it works: Every named person has their own nerve, loyalty and readiness to talk, so the same deed goes differently with different people there: one neighbour walks straight to the phone box, another pulls her curtain and tells only her sister, a debtor with nerve stands while another pays at once, a witness loyal to Mickey's people keeps quiet. The real simulation currently gives everyone the same middling nerve and loyalty; the design builds to the recommended answer, measured before it lands.
- Standard: Recommended answer to QUESTIONS 3: every named person their own, measured before it lands Test: S: the same deed goes differently with different people there
- Source: QUESTIONS 3 (open since 29 Sep) (DECIDED by the design proof, for him to overturn). Designed in: QUESTIONS 3; DESCRIPTION-COPY-2 §5 (Each person their own temper); DESIGN §2
- Status: decided. Coverage row: 2.14.

## 2.15 The firm runs without him

Kevin drives days, Terry nights; the book fills slowly; the firm's name rises and falls.


### 2.15.1 Fleet and drivers

- How it works: Two cars and two drivers at rung 1 (Kevin Needham days, Terry Hodgson nights), a third car at rung 2, at least four for the cold-store contract, five at rung 3. A car is bought from a man selling one or from the used-car lot by the north road (£600 to £1,200); a driver is hired from the regulars or a stranger who asks at the counter; drivers leave if unpaid or frightened. The board is a chalkboard in the office with a line per car and driver; it takes a minute a day at most and Pauline runs it if he never touches it. Car two is Mickey's own and cannot be sold, seized or wrecked for more than a day.
- Standard: Two cars and two drivers at rung 1, five cars at rung 3 (DESIGN §14) Test: S: a bought car joins the board and the ranks; addendum rules ER-FIRM-01 to 02
- Source: DESIGN §14 (no reference figure yet). Designed in: DESIGN §12, §14; DESIGN-ADDENDUM A14; DEFINITIONS RT2-01, RT2-06, G8; DESCRIPTION-COPY-2 §23
- Status: unmeasured. Coverage row: 2.15.1.

### 2.15.2 Ranks and accounts

- How it works: The rank outside Mickey's is his. The ferry rank and a second rank are won by being there with a car on the board five days in a fortnight, or by a word with whoever holds them. Accounts open in order: the cold-store contract, the Harbour Board's late men, a solicitor's office. The cold-store manager offers the contract once the packing shift has been met on time five mornings in one game week and the firm holds at least four cars; it is lost after three missed mornings in a week and can be won again once. From rung 2 each car on a good rank brings £110 to £140 a week.
- Standard: A rank is won by either road and never otherwise; accounts open in that order, each at its rung (the cold store at rung 3); "enough days" is five days in a fortnight (a balance figure checked with GD-07). Test: B: rank presence runs; account order.
- Source: The description, sections 28, 31. (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §2.15.2, RT2-01, G8; DESIGN-ADDENDUM A14; DESCRIPTION-COPY-2 §23
- Status: decided. Coverage row: 2.15.2. Conflicts settled: C-059.

### 2.15.3 Other firms on the ranks

- How it works: One other minicab firm works the Hook, a small outfit with two cars whose owner is a new minor person. It takes the fares people stop giving Mickey's after a hit-and-run and gives them back as the talk fades. It is a business, never a fourth rival and never a crime faction.
- Standard: 'People ring another firm for a while' (DESIGN §5); the three rivals stay three (canon) Test: S: fares move to the other firm after a drive-off and come back
- Source: DESIGN §5; canon (his ruling or canon). Designed in: DESIGN-ADDENDUM A14; DESIGN §5; canon (three rivals)
- Status: measured. Coverage row: 2.15.3.

### RT2-06 The firm failing for good

- How it works: The firm has a floor: the office, Pauline's radio and car two are never lost; car two cannot be sold, seized or wrecked for more than a day. The fare book never goes below zero; unpaid wages make drivers leave; Pauline leaves after two unpaid weeks and comes back when paid (until then fares come only by the office phone when Tom is there). Sheila leaves if asked to put the books off three counts running; without her there is no count and no wash, every week without her reads as put off, and she comes back if Tom calls at her house after a game week in which he asked nobody to put the books off. From any failed state but a revoked licence the way back is the same: drive car two, pay Pauline, hire a driver, buy a car at the lot.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-06 Test: B (bot), as written under RT2-06
- Source: design pass 3, RT2-06 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-06, RT-16, RT2-18; DESCRIPTION-COPY-2 §20
- Status: decided. Coverage row: RT2-06.

## 2.16 Death, bodies and the missing

A killing is permanent and remembered forever; a man who stops keeping his routine becomes the town's question.


### 2.16 Death, bodies and the missing

- How it works: A killing is rare, permanent and remembered forever; a body never cools in talk and is never wiped. Tom cannot die: beaten, he comes round on the pavement, in Grace Rinaldi's kitchen or in hospital, in control within 60 real seconds. Fists never kill on open ground; a fall onto a kerb's edge, a step or a wall's foot within 3 s of a heavy blow, when the man was already spent, can kill (1 in 50 to 1 in 20 such knockdowns). Finishing a downed man is a separate decision, asked twice. A body left where a routine passes is found; a hidden or sunk one never is, and the missing man becomes the town's question.
- Standard: Killing possible, rare, permanent, remembered forever (canon) Test: S: a missing routine is noticed; a body never cools
- Source: canon content rule (his ruling or canon). Designed in: canon (content rule); DESIGN §7; DEFINITIONS RT2-11, RT2-12; ONE-SHOT-PROMPT 14
- Status: measured. Coverage row: 2.16.

### RT2-05 Killing principals and needed people

- How it works: Tom's line keeps Sheila, Pauline, Ada, June, Alison, Ellis, the Widow, Father Walsh and anyone of sixty or over from his hands and sends; anyone else can be killed or hospitalised and the story falls back by role: Ron's asks come by the outfit's man at the office door; Darren's tips come through Pauline's radio talk and the caff, his debt closed; Kevin or Terry, a car short until a driver is hired; a rival head, his lieutenant takes the ladder at the same rung and counts as having seen the deed; Garbutt gone means no reads or truce; Danby gone ends that friendship; a hurt person is absent for the days their hurt sets; the beat constable's place goes to the second constable from the next night; the cold-store manager's deputy holds the contract; the car-lot man, cars come from a man selling one; Iveson, the fire thread runs on through Alison and Ellis, his debt closed; the dock gun seller, guns come the other three ways; the landlord's agent, letters by post. Act II's beats, the sit-down and Act III never depend on one killable person.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-05 Test: B (bot), as written under RT2-05
- Source: design pass 3, RT2-05 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-05; DESCRIPTION-COPY-2 §38
- Status: decided. Coverage row: RT2-05.

## 2.17 Fronts and rackets held

Taking a share of a business, putting a man in, money and trouble coming back; run through people, never sliders.


### 2.17 Fronts and rackets held

- How it works: A front is a share of a real business on the street (the launderette, the caff, the empty unit once let), got by money, a favour or pressure. It washes night money through its till, hides men and things, and is a place his men are. A round is a set of payments collected on a day by a man of his crew; trouble on it comes back to Tom through that man. Each has a named man with nerve and loyalty and is a target for rival pressure. Rung 3 needs a first front and round, rung 4 at least two of each. No stock, prices, sliders or screen; money arrives as the man brings it, short if the man is.
- Standard: A first front and a first round at rung 3 (DESIGN §14); empire as management on the street (his lesson 8); not an economy game (canon) Test: S: a front pays through its man; trouble at it reaches Tom through people; addendum rules ER-FRONT-01 to 02
- Source: DESIGN §14; canon (DECIDED by the design proof, for him to overturn). Designed in: DESIGN §14; DESIGN-ADDENDUM A15; DESCRIPTION-COPY-2 §25; DEFINITIONS RT-04
- Status: decided. Coverage row: 2.17.

### RT2-09 Turf: posts held and lost

- How it works: The three posts (the dock gate, the cold store, the landing) are held by one crewman each, standing there by his routine: the dock gate and cold store 06:00 to 22:00, the landing 22:00 to 02:00. Contested: a rival's men stand there too and it is a stare each time Tom or his man arrives. Lost: the post's man poached, frightened off, arrested or killed, the post empty three game days, or a sit-down defied and lost on it. Retaken by putting a man there and winning the stare or the fight. Holding all three is part of rung 4; losing one never drops the rung but costs: the landing loses the night runs, the cold store puts the contract at risk, the dock gate brings the Widow's tax back.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-09 Test: B (bot), as written under RT2-09
- Source: design pass 3, RT2-09 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-09; DESIGN §14; DESCRIPTION-COPY-2 §26
- Status: decided. Coverage row: RT2-09.

### RT2-18 The licence hearing

- How it works: Agar's licence letter is his pressure; his threat is a hearing at the council's licensing committee (in the Exchange, reached at the soft edge, a talk scene under 2 real minutes). The firm keeps its licence if at least two of four hold: every car passed Agar's inspection (no unmended damage), the fare book's last four weeks have no week put off, Tom attends in the decent jacket or better, and no road deed charge is outstanding; not attending counts as one failed. Otherwise the licence is suspended two game weeks: no bookings, Pauline cannot dispatch, the contract is paused and the count washes only £10. A firm car seen carrying a booked fare while suspended is stopped, and a second such stop revokes the licence for good, so the business does not survive.
- Standard: see DEFINITIONS-2026-11-21.md, design pass 3 (run 4), RT2-18 Test: B (bot), as written under RT2-18
- Source: design pass 3, RT2-18 (DECIDED by the design proof, for him to overturn). Designed in: DEFINITIONS §RT2-18, RT2-01, RT2-04; DESCRIPTION-COPY-2 §24
- Status: decided. Coverage row: RT2-18.

## 2.18 Ambulance and the hospital

Someone hurt is taken to hospital after a call from the phone box; stopping to help means making that call.


### 2.18 Ambulance and the hospital

- How it works: Stopping to help after a hit costs minutes and puts Tom's face beside the cab. Help is a call from the nearest phone box (10p) or the office, or a neighbour rings; the ambulance comes in about ten game minutes and takes the hurt person to hospital for the days their hurt sets. A car never kills, and only the player's car can strike anyone.
- Standard: Stop and help costs minutes and puts his face beside the cab (DESIGN §5) Test: S: an ambulance arrives after a call within its set time; addendum rules ER-AMB-01
- Source: DESIGN §5 (no reference figure yet). Designed in: DESIGN §5; DESIGN-ADDENDUM A22; DEFINITIONS RT2-19; canon (content rule)
- Status: unmeasured. Coverage row: 2.18.

## 2.19 Lasting marks on the town

A forced door shows for a day; glass stays broken until mended; his cars on the ranks; things stay where they were left.


### 2.19 Lasting marks on the town

- How it works: Damage stays until mended: a forced door shows for a day, broken glass stays broken until the owner mends it, blood stays until rain or a bucket washes it; a rival's base keeps a mark until mended and property harm is repaired by people for money and a day. A beaten Tom carries bruises and a cut lip for three game days and a limp for one. Marks keep across save and load, and nothing is ever wiped.
- Standard: Force shows on the door for a day (DESIGN §4); nothing is ever wiped (canon) Test: S: marks persist across save and load for their set time
- Source: DESIGN §4; canon (his ruling or canon). Designed in: DESIGN §4; ONE-SHOT-PROMPT 15; DEFINITIONS RT-06, RT2-08; canon (The moat)
- Status: measured. Coverage row: 2.19.
