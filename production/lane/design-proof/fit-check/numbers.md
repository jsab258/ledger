# Numbers that bear on the game's scale and timing (extraction, 21 Nov 2026)

Extraction only, no judgement. Every row: number | unit | what it is | file:line | short quote. Line numbers are as read on branch lane-2026-11 (canon.md and RULINGS.md from origin/wip). Rows marked "(arith)" are plain arithmetic by the extractor from the quoted numbers, not a source figure.

## Legend (short key = full path)

- OSP = production/lane/ONE-SHOT-PROMPT.md
- DEF = production/lane/design-proof/DEFINITIONS-2026-11-21.md
- MAP6 = production/lane/design-proof/GTAVI-MAP-2026-11-21.md
- CLD = production/lane/design-proof/CLOUD-FIGURES-2026-11-21.md
- MEAS = production/lane/design-proof/MEASUREMENTS-NEEDED.md
- MECH = production/research/lane/gtavi/MECHANICS.md
- YARD = production/research/lane/gtavi/YARDSTICK.md
- PLY = production/research/lane/PLAYERS-KCD2-GTAV-RDR2-2026-11-20.md
- STORY = production/research/lane/STORY-PATTERNS-STEAM-2026-11-20.md
- ACT = production/research/lane/ACTIVITY-SHARES-2026-11-20.md
- PATCH = production/lane/MONEY-AND-CONTENT-PATCH-2026-11-18.md
- CAN = canon.md on origin/wip
- RUL = RULINGS.md on origin/wip
- PASS6 = production/lane/story/measure/NOTES-V2-PASSENGER-v5k6.md (found by grep, not on the named list)

## Files with nothing or almost nothing for this purpose

- No file in production/research/lane/ or production/lane/ has WALKTHROUGH in its name (find -iname). `grep -ril walkthrough` hits (ACTIVITY, DRIVING-REFERENCE-GAMES, FEEL-REFERENCE-GAMES, feel-2026-11-20/*-raw.md, refmech-2026-11-20/*, lane/story/measure/*, design-proof/DESIGN-COMPLETE.md, LOG.md, COVERAGE.md, GTAVI-MAP) are video titles and "walkthrough games" in the story study; they carry no scale or timing numbers beyond what is quoted below.
- MONEY-AND-CONTENT-PATCH-2026-11-18.md: no game-scale number. Only dollar-to-pound renames; the only figures are the fascia and poster counts (PATCH:20 "(~24 to ~21)", "(~16 to ~15)": shopfront and poster counts in an image batch, not map scale) and sim-harness test text "about $120; you have $300" (PATCH:49, test strings, not design).
- STORY-PATTERNS-STEAM-2026-11-20.md: no scale or timing number for LEDGER or the reference games (only review shares and sample sizes).
- PLAYERS-KCD2-GTAV-RDR2-2026-11-20.md: only reference-game hours played at review and LEDGER's length (F).

---

## A. Map

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| 48 | m | Length of the built Quay Street | RUL:119 | "updated to the built street (48 m, its climb, its bend east behind the parade at the far end" |
| none | | Hook and docks size in metres, km, blocks, road length | none in any listed source | OSP:671 gives only "Not a hundred square miles: one port, dense, known by heart." |
| 7 | districts | Meridian's districts (Hook, Copper Row, Exchange, Parade, Fairview, Ironside, Gullwing); only the Hook plus docks is playable | CAN:17-20; OSP:661 | "One map, seven districts" |
| 3 | streets named | Streets minted: Quay Street, Weighhouse Lane, Tannery Row (only Quay Street is built/playable) | CAN:23 | "Streets minted: Quay Street, Weighhouse Lane, Tannery Row." |
| 1 | street | The built street is Quay Street | CAN:27 | "THE BUILT STREET IS QUAY STREET, IN THE HOOK" |
| 3 | sides | Quay Street's sides: east six-bay parade; west shop block (opposite north half of the parade); west plain terraces (opposite Mickey's, quay end) | CAN:35-42; OSP:661 | "the east side is the six-bay parade" |
| 6 | bays | Six-bay parade | CAN:36; OSP:661 | "six-bay parade on its east side" |
| 6 | shops | "the six shops of Quay Street" (hold-up targets) | OSP:972 | "the six shops of Quay Street, the pawn, the chandlery" |
| 593 | pieces | Built street's art pieces (asset ids east_parade_*) | CAN:33 | "The 593 pieces keep their east_parade_* identifiers" |
| 7 | trades named | Bay 1 fishmonger, bay 3 empty unit, bay 4 launderette, bay 5 grocer; west_north newsagent/tobacconist, ironmonger, tea room; east_chandler | RUL:67 | "bay 1 fishmonger, bay 3 empty unit to let ... bay 5 grocer" |
| about 19 | named places | Places the play description names in the playable map: Quay Street/Mickey's, parade, shop block, terraces, yards and lanes, quay, ferry landing, Old Basin, fish dock, cold stores, dock gate, customs, Harbour Board (count by extractor from list) (arith) | OSP:661 | "the yards and lanes behind them, the quay, the ferry landing, the Old Basin, the fish dock, the cold stores, the dock gate, customs and the Harbour Board" |
| 8+ | enterable rooms named | Mickey's and flat above, caff, Rita's back room, Hal's shop, Ada's front room, Iveson's hut, chapel hall, plus "break-in sites jobs name"; also customs shed, Harbour Board back office, launderette, boxing club hall, doctor's terrace, pawn back room appear elsewhere | OSP:944 | "Rooms are enterable where jobs and stories go" |
| 3 | ways in | Each break-in site entered by at least three ways | OSP:944, 946 | "each entered by at least three ways" |
| 2 | escapes | Mickey's yard has two escapes | CAN:45 | "a yard with two escapes" |
| 5 | s | Never stuck: move on within 5 s from any state | OSP:806, 1255 | "from any state the player can move on within 5 seconds" |
| 3 to 5 | real min | Crossing the Hook end to end ON FOOT (ferry landing to north road), provisional band | DEF:151-152 | "on foot 3 to 5 real minutes, by car 60 to 100 s" (GD-01) |
| 60 to 100 | s | Crossing by car, provisional band | DEF:152 | as above |
| 3 | real min | Any named place reached unaided by a newcomer | OSP:940 | "A newcomer reaches any named place unaided within 3 real minutes." |
| 3 | real min | Walk from the paper map alone to the hut | OSP:266 | "walking to it from the map alone takes under 3 real minutes" |
| 3 | real min | Dead stretch: after 3 min lost, next person within 5 m offers the way | OSP:266, 940 | "After three minutes, the next person he passes within 5 m offers the way." |
| 90 | s | Lost: no progress for 90 real seconds, Tom's own line names landmark again once | OSP:266, 940 | "Lost (90 real seconds without progress ...)" |
| 30 | s | Something to do within 30 real seconds of wherever Tom stands by day | OSP:1249; DEF:151 | "a fare, a debt or a person with a word for him is within 30 real seconds" |
| 1.2 | m | Vault places only: low walls, fences, bins under about 1.2 m | OSP:810 | "(low walls, yard fences and bins under about 1.2 m" |
| 3.1 / 5.8 | m | Camera pull-back on street / in car (map-fit constraint for lanes and rooms) | OSP:804, 884 | "pulled back 3.1 m"; "about 5.8 m back" |
| 6 | m | Talk passes only between people within 6 m | OSP:788 | "within 6 m, weaker with each telling" |
| none | | Number of buildings, total streets in the Hook, blocks | none | not given anywhere in the listed files |
| about 2x / 3x | ratio | Reference: GTA VI map vs GTA V and RDR2 | MECH:100 | "Map about twice GTA V's and three times RDR2's" |
| about 15 | % | Reference: GTA VI roads narrower than GTA V's | MECH:11 | "Roads about 15% narrower than GTA V's" |
| more than 100 | people | Reference: distinct people seen at one GTA VI tram stop | MECH:81; YARD:25 | "more than 100 distinct people moving" |
| none | | Reference crossing times (KCD2 Kuttenberg, RDR2 Saint Denis, GTA V district, GTA VI) | MEAS:42 | A8: "timed crossings in footage", 1 PC hour, not yet measured |

## B. Cars

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| none | | Top speed, typical speed, town speed of the cab (mph or km/h) | none | OSP and DEF give no speed figure for the car; only thresholds below. RUL:11 "game-band targets" with no number |
| 30 | mph | Nobody steps out inside stopping distance of a car doing 30 mph or less | OSP:97, 904 | "nobody steps out inside the stopping distance of a car doing 30 mph or less" |
| 60 | mph | Lane change test speed: tail swings under 15 degrees, settles within 1 s | OSP:882, 1258 | "a lane change at 60 mph on keys swings the tail under 15 degrees" |
| 10 | mph | A touch under 10 mph is forgiven | OSP:387, 888, 1258 | "a touch under 10 mph is forgiven" |
| 10, 20, 35, 50 | mph | Pole crash test speeds | OSP:381 | "Drives into a pole at 10, 20, 35 and 50 mph" |
| 35 | mph | From about 35 mph in one hit the car will not drive on; off the road for a day | OSP:387, 888 | "from about 35 mph in one hit the car will not drive on" |
| 1 | day | Car off road after 35 mph hit; dent stays until the yard mends it overnight | OSP:387, 888 | "it is off the road for a day" |
| 5 | s | After any crash the car moves or can be left within 5 s | OSP:387, 888 | "within 5 real seconds" |
| 0.2 to 0.35 | s | Keys: steering eases to lock | OSP:96, 882 | "eases to lock in 0.2 to 0.35 s" |
| 0.4 to 0.9 | s | Keys: steering centres | OSP:96, 882 | "centres in 0.4 to 0.9 s" |
| 10 | % | Same course on keys or pad within 10% | OSP:882, 1258 | "within 10% on keys or pad" |
| 2 | s | In or out of the car, either side | OSP:96, 886 | "under 2 s from either side" |
| 5.8 | m | Car camera distance | OSP:96, 884 | "about 5.8 m back" |
| 44 | m | Car heard by day (much further at night) | OSP:890, 832 | "heard within about 44 m by day" |
| 60 | m | Horn reach by day | OSP:177, 890 | "about 60 m by day" |
| 15 | m | Short toot brings out a waiting fare within 10 s if within 15 m | OSP:177, 890 | "inside 15 m out of the door within 10 real seconds" |
| 6 | s | Taking a parked car (loud, force reach) | OSP:370, 1030 | "about 6 seconds of loud work" |
| 3 and 10 | s | GTA VI-raised ways in: brick through quarter-light about 3 s loud; tool at door and ignition about 10 s quieter (times to be checked) | MAP6:177 | "about 3 s, loud ... about 10 s, quieter" |
| 90 | s | Every chase (car or foot) ends, caught or lost, within 90 real seconds | OSP:143, 175, 242, 372, 1020, 1024, 1026, 1255 | "ends caught or lost within 90 real seconds" |
| 7 | s | Chase lost once out of sight 7 s | OSP:143, 175, 373, 1020, 1026 | "lost by breaking sight ... for 7 s or 70 m" |
| 70 | m | Chase lost at 70 m out of sight | same | same |
| about 1 | game hour | Constable searches last place seen after a lost chase | OSP:143, 1008 | "looks round there for about a game hour" |
| half | real min at most | Same search "on the spot" (note: 1 game hour is 45 real s) | OSP:1008 | "(half a real minute at most on the spot)" |
| 1 | patrol car | One patrol car works the Hook by day and night; more only at War | OSP:1012 | "One patrol car works the Hook by day and night on a route" |
| 2 | min | Pull-over stop (look at car and driver, plate, caution) under 2 real minutes | OSP:372, 1012 | "under 2 real minutes" |
| 2 | min | No drive may run longer than 2 real min without a decision, person or sighting; no fare either | OSP:178, 880 | "no drive runs longer than 2 real minutes without a decision, a person or a sighting" |
| 40 | real min | Test: "drives fast but lawfully for 40 real minutes"; lawful fast driving never stopped | OSP:366, 372 | "Drives fast but lawfully for 40 real minutes" |
| none | | The "game's band" for a speed "far over" that starts a police stop | OSP:1012 | "or a speed far over the game's band" (band not given) |
| 22 / 25 | % | Driving share of play: budget about 22% (a fifth), never over 25% | OSP:552, 633, 1240 | "Driving: fares, tails, getaways ... about a fifth, never over 25%" |
| 2 | s | Choice after a car hit put within 2 s | OSP:384, 906 | "the choice is put within 2 real seconds" |
| about 10 | game min | Ambulance arrives after the call. (arith) 10 game min = 7.5 real s at 45 s/hour | OSP:385, 906 | "the ambulance comes in about ten game minutes" |
| 1 to 2 | real min | One fare's length | OSP:99, 914 | "A fare lasts one to two real minutes" |
| 2 | cars | Start fleet: "two tired cars"; 3rd car by rung 2; 5 cars at rung 3 | OSP:655, 1128-1129 | "two tired cars"; "five cars, a night desk" |
| 2 | cars | The other minicab firm has two cars | OSP:908 | "a small outfit with two cars" |
| 0 | | Fuel, wear, tuning, garage, racing: none | OSP:683 | "no fuel" (no hunger, tiredness, fuel or wear) |
| none | | Reference-game car chase lengths | none in listed files | MAP6 maps GTA VI only; no chase duration found. RUL:11 and OSP:1026 give LEDGER's own 90 s. MEAS:11 GTA VI footage pass (chases) not yet done |
| about 30 | fps | Reference: GTA VI frame rate | MECH:131; YARD:61 | "30 frames a second on every console" |

## C. Clock

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| 45 | real s per game hour | The one clock | OSP:56, 100, 696 | "A game hour is 45 real seconds, so a game day is 18 real minutes" |
| 18 | real min per game day | (same) | OSP:696; CLD:58 | "18 at 45 s a game hour" |
| 0.75 | real s per game minute | (arith) 45 s / 60 | derived from OSP:696 | |
| 12 | real min per game day | The Unreal clock at 30 s an hour (CLD recommends not building this one) | CLD:58, 60 | "12 at 30 s (the Unreal clock) ... should not be the one built" |
| 48 | real min per game day | GTA V (2 s a game minute); RDR2 average 48 | CLD:54-55 | "48 (2 s a game minute)" |
| about 96 | real min per game day | KCD1 (15 to 1) | CLD:56 | "about 96 (15 to 1)" |
| about 144 | real min per game day | GTA VI, reported from footage, unconfirmed | CLD:57 | "about 144 reported from footage" |
| 2 | s | Watch face shows hour for 2 s | OSP:100, 838 | "the hour shows on his watch face for 2 s" |
| 3 | s | Hour known within 3 s anywhere | OSP:838 | "within 3 s anywhere" |
| 15:40 Mon 15 Oct 1990 | clock | Start: ferry arrives "about twenty to four in the afternoon" | OSP:655 | "Monday 15 October 1990, about twenty to four" |
| about 9 | game weeks | Calendar length from Monday 15 Oct 1990 | OSP:770 | "for about nine game weeks" |
| (arith) 63 days = about 18.9 real h | | 9 weeks x 7 x 18 min | derived | |
| 7 | days | Act I week, Monday to Sunday | OSP:1192, 1198 | "seven days from Monday to Sunday" |
| 7 (about) | game weeks | Act II length; ends at sit-down or after seven game weeks | OSP:551, 1202 | "Act II ends at the sit-down, or after seven game weeks" |
| 8 | game weeks | Fail-safe: after the eighth game week of Act II the leading rival climbs one rung a game day | DEF:229 | "by the end of the eighth game week of Act II" |
| 1 week | | Act III (VAT inspection) | OSP:1216 | "One week, 2 to 3 hours" |
| 5 | mornings | Inspector's mornings (grading) at nine | DEF:208; OSP:570 | "Each of the five mornings the inspector asks for one item" |
| nine | o'clock | Inspector each morning; statement next morning; Ada's tea; Ada's pot | OSP:570, 986, 675, 738 | "the signed statement is made at the station at nine next morning" |
| ten | o'clock | Landing open "from ten till one"; customs lamp out at eleven | OSP:144, 675 | "the landing open from ten till one, the customs lamp out at eleven" |
| after ten | o'clock | Ron's first ask: coat and envelope for the landing after ten | OSP:125, 655 | "for the ferry landing after ten" |
| ten (morning) | o'clock | Constable comes to the door at ten (Wednesday after a signed fight statement; morning after Ellis for a window) | OSP:244, 736, 1010 | "a constable at ten the morning after that" |
| eight | o'clock | Ron's second envelope at eight | OSP:739 | "Ron with the second envelope at eight" |
| half past five | o'clock | Packing shift from Old Basin cold stores (morning); also evening | OSP:914, 474 | "the packing shift from the Old Basin cold stores at half past five" |
| 6 | game min | Talk passes every 6 game minutes between tied people in same place | OSP:788 | "talk passes every 6 game minutes" |
| 1 to 7 | game days | How long a deed stays hot in talk: scuffle a day, window a few days, robbery or serious beating most of a week; body never | OSP:790 | "about 1 to 7 game days" |
| 1 | game day | Anything he did comes back to his face within one game day | OSP:794, 157 | "within one game day" |
| 3 | game days | Bruises and cut lip last 3 game days; limp 1 game day | OSP:874 | "bruises and a cut lip for three game days and a limp for one" |
| 1 | day | A forced door shows damage for a day | OSP:263, 946, 954 | "shows on the door for a day" |
| 1 | week | Hot notes from a till are hot for a week; shops restock weekly | OSP:962, 974 | "notes from a till are hot for a week" |
| 6, 2, 8, 12, 22 | game hours | Arrest cost: window about 6 (2 and a caution if he owns up), wounding 8, robbery 12, killing 22 then bail | OSP:242, 244, 976, 996 | "About six hours for a window ... eight for a wounding, twelve for a robbery, twenty-two for a killing" |
| (arith) 6 to 22 game h = 4.5 to 16.5 real min | | Against "the arrest passes in under 2 real minutes" (hours are skipped, not played) | OSP:242, 996 | |
| 24 / 36 | hours | 1990 legal custody limits (36 for serious, by a superintendent) | CLD:21 | "24 hours, 36 for serious offences" |
| 73 | % | Share held under 6 hours, 1984-87 | CLD:23 | "about three quarters (73%) held under six hours" |
| 2 | game weeks | Dial falls one step after about two quiet game weeks; Ellis falls one stage after two quiet weeks | OSP:1156; DEF:292 | "falls one step only after about two quiet game weeks" |
| 3 | game days | Manhunt with no sighting falls to investigating | DEF:292 | "after three game days with no sighting" |
| 2 | game weeks | Fixer's truce holds a rival at its rung two game weeks, once a game | DEF:243 | "holds exactly two game weeks" |
| 5 in 14 | days | Rank won by presence "five days in a fortnight" (balance figure) | DEF:432 | "'enough days' is five days in a fortnight" |
| 3 Fridays | | Missed-rent ladder: 1 miss = arrears and agent Monday; 2 = letter, notice to quit flat in a fortnight; 3 = flat let, Tom sleeps in office | DEF:313 | "Three: the flat is let to someone else" |
| 2 | game days | Three seen deeds in two game days put a street on edge | OSP:536, 990 | "within two game days" |
| 1 | game week | After a hold-up, that street's shops shut early; a happening never repeats on one street within a game week (DEF) / twice in a week (OSP) | OSP:938, 972; DEF:337 | "after one hold-up in a game week" |
| 1 | game hour | Witnesses talk quieter for a game hour after a deed; manhunt sign at least one game hour before an arrest | OSP:792, 541, 1010 | "at least one game hour before an arrest can land" |
| 1 | hour | Minding job: stand at a door for an hour | OSP:199 | "stands at a door for an hour" |
| 1 | hour | Wait for an appointment: "wait until"; windows of at least 2 game hours, no lateness fail inside | OSP:924 | "no lateness fail inside a window of at least 2 game hours" |
| 2 | game days | Ellis "from the second day for talk" once three day-world people pass on talk of his nights; arrives day 4 in S24 | OSP:1010, 435 | "from the second day for talk" |
| Thu, Sat, Sun | days | Thursday market day in Copper Row empties Hook shops; Saturday match fills street at three and five; Sunday shops shut, chapel busy; paper twice a week | OSP:770, 798, 425 | "Saturday's match fills the street at three and at five" |
| Friday | day | Rent day; Sunday: Sheila's question | OSP:655, 1034, 1192 | "Rent falls on Friday" |
| 4 and 12 | real s | First hint after standing still 4 s; no second hint within 12 s | OSP:78, 704 | "standing still for 4 real seconds brings one first hint" |
| none | | Shop opening and closing hours (numbers) | none | "Shops keep hours from their people and doors" (OSP:962); no hours given |
| none | | Pub/club/night hours | none | pubs stand as places only (CAN:46-48, OSP:684); the Parade "nightlife" district has no hours |
| none | | Routine schedules hour by hour, curfews | none | "Everyone named keeps a routine, hour by hour" (OSP:766) lives in the tuning table; no values in these files |
| none | | Separate day length and night length (hours of dark) | none | dusk and lamps shown at about 2:30 to 4:30 of play (OSP:99, 710) |
| none | | Evening span | none | A5 would time "dusk to midnight" in reference games (CLD:60); "An evening has a shape" (OSP:675) has no length |
| none | | Reference-game shop, pub, curfew hours | MECH:88 | GTA VI: "Kotaku says every shop is open all night; another review says shops open and close" (conflict, no hours) |

## D. Jobs, fares and happenings

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| 80p plus distance | £ | Fare pay | OSP:99, 914 | "pays 80p plus distance" |
| 2:30 (never later than 3 min) | min of play | First fare starts | OSP:99, 710, 750 | "The first fare starts at about 2:30 of play and never later than 3 real minutes" |
| 7 | wrinkles | Talker, parcel, tail, runner, wait, hurry, face | OSP:916 | "no wrinkle comes twice running" |
| about half | | Fares with a wrinkle (S07) | OSP:173 | "About half the fares carry one wrinkle" |
| every fare after the first | | Fares with a wrinkle (design text; "wins") | OSP:916, 1274 | "Every fare after the first carries one wrinkle" |
| at least 6 | fares | Fares in S07's day shift | OSP:166 | "Takes fares from Pauline for the rest of the day, at least six" |
| 2 | fares | First hour's day shift (not 3) | OSP:726, 1274 | "the first hour's day shift has two fares, not three" |
| 1 to 2 | min | Fare length; none over 2 min without a decision, person or sighting | OSP:178, 914 | |
| 41 | stories | Play stories S01 to S41 (finish line) | OSP:66-634 | "### S41 Never five minutes with nothing new" |
| 200 | ids | Checklist ids; 1 not placed in play (9.6); 2 half-proven | OSP:638-645 | "Of the 200, one is not proven by any story" |
| 5 | debts | Debt book | OSP:110, 1049 | "five names, £156" |
| 30 | regulars | Named regulars | OSP:760 | "The thirty regulars stand as written" |
| 25 to 40 | side stories | Found on foot, no markers, each 3 to 5 steps | OSP:936 | "Side stories: 25 to 40" |
| 3 to 5 | steps | Steps per side story | OSP:936 | "each 3 to 5 steps" |
| 6 | happening types listed | Row, van across lane, shoplifter, lost man, dog loose, woman locked out | OSP:938 | "a row on a doorstep ... a woman locked out" |
| 2 | min | Happening lasts under 2 real minutes | OSP:202, 938 | "takes under 2 real minutes" |
| 30 | min | No happening twice in 30 minutes (and no set piece twice in 30 min) | OSP:202, 924, 938 | "None comes twice in thirty minutes" |
| 1 | week | Or twice in a week on one street | OSP:938 | "or twice in a week on one street" |
| none | | Count of authored happenings in the library | DEF:336 | "enough happenings that none repeats on one street within a game week" (count pending, RT-19) |
| 22 | words | Ledger line per job step | OSP:924, 115 | "a Ledger line of about 22 words" |
| 2+ | outcomes | Per deciding step; at least 2 sources of direction | OSP:924 | |
| 5 | min | Never more than 5 real minutes anywhere with nothing new; first hour never more than 3 | OSP:633, 750 | "more than 5 real minutes anywhere with nothing new, or more than 3 in the first hour" |
| about 10 | activities | Distinct activities per 30-minute stretch | OSP:633, 1247; CAN:162-164 | "about ten distinct activities per thirty minutes" |
| about 13 | activities | Distinct activities by minute 30 of the first hour | OSP:750 | "about thirteen distinct activities by minute 30" |
| 3 | min | Something new at least every 3 minutes in the first hour | OSP:700, 1254 | "Something new happens at least every 3 minutes" |
| 12 | tense moments | At least 12 per 30 min, from at least 4 of 9 sources, none over half | OSP:208, 675, 1263 | "at least twelve tense moments, from at least four sources, none of them more than half" |
| 9 | sources | Eyes, ears, load, window, walk, law near, other man's nerve, odds, two lives | OSP:675 | "The nine:" |
| 1 / 2 | moments | Retellable: 1 in first 30 min, 2 every hour after | OSP:673, 432, 1263 | "at least one such moment, and every hour after holds two" |
| 5 of 8 | players | Panel names a retellable moment as most exciting | OSP:1266 | "at least five of eight name a retellable moment" |
| 30 | s | By day an idle moment has a fare, debt or person within 30 s (tested at 20 idle moments of 30 real s each) | OSP:199, 201, 1249 | "stands idle at 20 daytime moments for 30 real seconds each" |
| 4 | asks | Outfit's asks on nights 1, 3, 5, 7 | OSP:1192 | "the asks on nights one, three, five and seven" |
| 8 | verbs | Sending verbs (Act II) | OSP:453, 1074 | "the eight verbs" |
| 7 | orders | Crew digit orders | OSP:450, 1070 | "1 with me ... 7 lean on him" |
| 8 | beats | Act II beats (old firm's end, rival notice, real book, cold-store, first gun, one case, collision, sit-down) | OSP:1203-1210; DEF:215 | "Each of Act II's eight beats" |
| 1 each | per Act II game week | At least one rival rung, one firm change and one return | OSP:550, 1212 | "every game week of Act II brings at least one rival rung, one firm change and one return of a deed" |
| 5 | names | Mickey's real book yields at least five new names | DEF:215 | "at least five new names" |
| 5 | rungs | Rival ladder: noticed, visit, pressure, threat, sit-down | OSP:1105 | |
| 3 | rivals | Widow, Agar, Cammack | OSP:1096-1099 | |
| 4 | rungs | Rise rungs 1 to 4 | OSP:1124-1130 | |
| 8 | named differences | Replay with different Sunday answer and first rival meets at least 8 differences in first 5 hours | DEF:173 | "at least eight named differences" |
| 2 each | jobs | Each place (dock gate, Harbour Board counter, customs) has at least 2 jobs and one person with a word | DEF:223 | "at least two jobs and one person with a word" |
| 3 | answers | Per pressure: pay, defy, counter; three outcomes per sit-down | OSP:1107, 1113 | |
| none | | Jobs per real hour; kinds per act count | DEF:198, 201; MEAS:44 | GD-08 PENDING: "inside the band the teardown and the reference games' mission counts show" |
| none | | Counts of fares, jobs, happenings per hour or per week | none | not given as numbers beyond the above |
| 55 | missions | Reference: GTA V story missions | ACT:18 | "GTA V story about 30 hours, 55 missions" |
| 20 | chapters | Reference: Mafia DE | ACT:19 | "about 15 hours, 20 chapters" |
| 22 + 4 | stranger missions | Reference: RDR2 stranger missions | lane/story/measure/NOTES-V2-RDR2.md:5 | "22 numbered plus 4 unnumbered" |
| 8 | decisions | Reference: KCD2 epilogue decisions; RDR2 2 endings, 4 variants | CLD:68-69 | "8 decisions change the epilogue" |

## E. Crowd and people

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| at least 25 | distinct people | In the busiest view of the Hook at its busiest hour (judgement figure, to be replaced) | DEF:159 | "at least 25 distinct people in the busiest view" |
| none | | People per street, per hour; total residents; density by hour | OSP:206, 762, 766 | "The crowd's numbers by hour on the street follow the tuning table's hours"; no values given |
| 30 | regulars | Named regulars with about 30 street lines each | OSP:760 | "about thirty of their own street lines" |
| 13 | named principals | Ron, Sheila, Ellis, Darren, Ada, June, Father Walsh, Alison, Danby, Garbutt, Agar, Jensen, Cammack (count by extractor) (arith) | OSP:756; CAN:79-89 | "the principals are canon's cast" |
| 5 | firm's people | Pauline, Kevin, Terry, Ron, Sheila (plus Darren runs messages) | OSP:758 | |
| about 5 of 9 | principals | A deed seen by one principal reaches about five of nine on its first day | OSP:788 | "reaches about five of the nine on its first day" |
| 6 | lines | Each crowd kind at least six lines per situation | OSP:762 | "at least six lines per situation" |
| 7 | words | Street line length | OSP:1166 | "about 7 words a street line" |
| 7 | m | A remark is said within 7 m | OSP:1166 | "a remark said within 7 m" |
| 45 | s | Everyday street talk at most every 45 s; person's own line at most once a day; shared line once a week per street; at least three closing lines | OSP:208, 1166 | "at most every 45 s" |
| 1 hour | | No shared street line heard twice in one real hour (raised bar) | DEF:159 | "no shared street line heard twice in one real hour" |
| 1 | constable on night beat | One beat constable walks Quay Street and quay at night; a second constable is a minor named person | OSP:1004, 760 | "A constable walks Quay Street and the quay at night." |
| 2 | named bought officers | | OSP:1014 | "Two named officers in the Hook can be paid or leaned on" |
| 1 | patrol car | | OSP:1012 | |
| none | | Constables on shift by hour | none | |
| 3 | m | Onlookers keep about 3 m and scatter once a weapon is out | OSP:190, 866 | "people stop to watch at about 3 m" |
| 3+ within 2 m | people | Group cover: glance takes 0.7 s instead of 0.35 s | OSP:354, 826 | "Among a group of three or more people within 2 m" |
| fewer than 3 | people near | Pickpocket felt if fewer than three near; distracted man in crowd of 3 or more not | OSP:288, 960 | |
| 5 | s | Tom never held by the crowd 5 s; no doorway jam | OSP:206 | "Tom is never held by the crowd for 5 real seconds" |
| 60 | h | Reference: one GTA VI reviewer heard no repeated line in about 60 hours | YARD:25 | "one reviewer heard none in about 60 hours" |
| 600,000 / 300,000 / 55,000 | animations | Reference: GTA VI / RDR2 / GTA V | MECH:79 | "600,000 or more animations against about 55,000 in GTA V and 300,000 in RDR2" |
| none | | Total named people in the game | none | OSP:756-760 lists categories only |
| none | | Pedestrian counts by hour from 1990 time-use | CLD:38 | "Not found." (B4, status UNMEASURED) |

## F. Content hours

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| 15 to 20 | h | Release length | RUL:9; OSP:657; PLY:169 | "Length: 15 to 20 hours." |
| about 2 | h | Act I | OSP:1192 | "Week one, about two hours" |
| 11 to 14 | h | Act II (about seven game weeks) | OSP:1202 | "About seven game weeks, 11 to 14 hours" |
| 2 to 3 | h | Act III | OSP:1216 | "One week, 2 to 3 hours" |
| 2 + 9.5 + 2.5 = about 14 | h | Story bible's act lengths for the main line | PASS6:6 | "the act lengths (2 + 9.5 + 2.5 hours) give about fourteen hours for the main line" |
| (arith) 7 d x 18 min = 126 min | | One game week in real time; Act II at 7 weeks = about 14.7 h | derived | |
| 20 | s | Ferry shot; control within 20 s (never later than 1.5 min) | OSP:77, 702, 1254 | "Tom is under control within 20 real seconds" |
| 1:30 | min | Talk possible by 1:30 (within 3) | OSP:79, 706, 750 | |
| 1:45 | min | Sheila's walk-round (six lines) | OSP:708 | |
| 2:30 | min | First verb with the hands (within 3) | OSP:710, 750 | |
| 4:30 | min | Back at office; debt book | OSP:712 | |
| 5:30 | min | First choice and deed (never later than 20, aim 6) | OSP:111, 714, 750 | "a choice and a deed at 5:30 (within 20, aim 6)" |
| 7:00 | min | Ron's ask after dark | OSP:716 | |
| 9:00 / 11:30 | min | The carry / the landing | OSP:718, 720 | |
| 13:00 | min | Tuesday; Darren says it to Tom's face; Ledger opens | OSP:722, 750 | "the town visibly knows him at minute 13" |
| 14:00 / 15:00 / 19:00 / 20:30 / 23:00 / 25:00 | min | The count; day shift; Wayne's £30; Lee's £15; side story; night with no ask | OSP:724-734 | |
| 29:00 / 31:00 / 39:00 / 45:00 / 47:00 / 53:00 / 56:00 | min | Wednesday constable; Ada's tea and Alison; Ron's second envelope; Thursday "Nowak"; Iveson £80; Ellis on street; two dockers by car two, rent day tomorrow | OSP:736-748 | |
| 30 | min | Town visibly knows Tom by minute 30 (note: 13 in OSP:750) | OSP:1263 | "the town visibly knows Tom by minute 30" |
| 60 s; 5%; 3.5 min | | Every scene skippable and at most 60 s; under 5% of the hour watched; never over 3.5 min without control | OSP:700 | |
| 2 min | | Search, lost fight, arrest each under 2 min | OSP:750 | |
| 25/22/19/17/8/6/3 | % | DESIGN hour budget: foot 25, driving 22, talk 19, jobs 17, fights 8, Ledger 6, waiting 3 | OSP:552; ACT:73 | "on foot 25%, driving 22%, talk 19%, jobs 17%, fights 8%, Ledger 6%, waiting 3%" |
| under 30 / under 10 / under 25 | % | Caps: talk, waiting, driving | OSP:633, 1241, 1245, 1178 | "talk over 30% of play, waiting over 10%, driving over 25%" |
| 18 | h | Budget compared to Mafia DE | ACT:9 | "LEDGER's 18-hour budget" |
| 5 of 8 / 8 | players | Panel size and recommendation bar (the "4 of 8" bar to be set) | OSP:1266; MEAS:29 | |
| 8 | | Critics of 18 found GTA VI slow opening or a sag | YARD:57 | "8 of 18 critics found a slow opening" |
| 50 to 80 (VGC about 60) | h | Reference: GTA VI main story; 100 to 150 with most side content | MECH:123 | "Main story about 50 to 80 hours ... about 100 to 150 hours with most side content" |
| about 30 / 75 to 85 | h | Reference: GTA V story / 100% | ACT:18 | "story about 30 hours, 55 missions; 100% 75 to 85 hours" |
| about 15 | h | Reference: Mafia DE | ACT:19 | |
| 40 to 50 / 90 to 110 | h | Reference: KCD2 story / 100% | ACT:20 | |
| 60 (65 before cuts); about 12 of story scenes | h | Reference: RDR2 story; scenes (weak source) | ACT:17 | "about 12 hours of story scenes" |
| 108 / 155; 77 / 20; 127 / 42 | h | Median hours at review, positive / negative: GTA V; RDR2; KCD2 | PLY:38 | "GTA V positive 108, negative 155" |
| none | | "First evening" and "first week" lengths in real time as distinct targets | none | the S09 day = 18 min, week = 7 days (OSP:198, 1192); no separate target |

## G. On foot

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| none | m/s | Tom's walk, jog, run, sprint speeds; stamina | none in listed sources | OSP:802 "walks, runs and turns with weight"; no speeds. MECH:30 lists GTA VI "Walk, fast walk, jog, run"; MAP6:64 "PC measuring" |
| none | | Stamina numbers (no stamina bar; breath only) | OSP:38 (S38), 854 | "Breath, not a bar" |
| half | | Slow walk (Z) halves footstep reach | OSP:802, 358 | "halves the reach of his footsteps" |
| 0.8 | s | Vault at a set place | OSP:373, 810 | "carries Tom over it in about 0.8 s" |
| 1.2 | m | Vaultable height | OSP:810 | |
| about 5 | % | Runner flees at Tom's run speed less about 5% | OSP:1024 | "Tom's run speed less about 5%" |
| 1 | m | Catch: hand on collar within 1 m behind | OSP:175, 1024 | |
| 7 s / 70 m | | Pursuit lost | OSP:143, 175, 373, 1020 | |
| 90 | s | Foot chase ends | OSP:175, 1020 | |
| 20 to 40 | s | Tail target looks back on foot | OSP:304, 928 | "about once every 20 to 40 s on foot" |
| 5, 20, 40, 60 | m | Tail follow distances tested | OSP:299 | "follows a named man at 5, 20, 40 and 60 m" |
| 35 / 18 / 8 / 25 | m | Sight: shape / mark / face / recognise if known | OSP:353, 820, 1259 | "a shape at 35 m, a mark at 18 m and a face at 8 m, and recognises Tom at 25 m" |
| 1 / 0.7 / 0.25 / 0.12 | light | Daylight / lamp / unlit / doorway | OSP:353, 820 | |
| 0.35 / 1.2 / 0.8 | s | Glance / knowing / minimum warning | OSP:820 | |
| 2x | | Running noticed twice as fast | OSP:353, 820 | |
| 0.7 | s | Glance among 3+ people within 2 m | OSP:354, 826 | |
| 8 | m | Still in doorway: only a shape, beyond 8 m | OSP:354, 826 | |
| 3.6 | m | 3 a.m. footstep carries; at noon nothing; slow steps half | OSP:142, 832, 1260 | "about 3.6 m" |
| 3 | s | Constable heard or seen at least 3 s before he can challenge | OSP:139, 1004 | |
| 2 | m / 10 m | Drawer search heard about 2 m; forced cupboard about 10 m at night | OSP:263, 948 | |
| 60 / 177 | m | Horn / shot reach by day | OSP:890, 832, 1153 | "heard to about 177 m by day" |
| twice | | Sound carries twice as far in small hours | OSP:832 | |
| 30 | s | Witness's walk to tell lasts at least 30 real s in sight (50% longer with assist) | OSP:224, 984 | |
| 2 | s | "Oi!" call stops a walker about 2 s | OSP:225, 842 | |
| 2 / 10 | m / s | Crew: follows at about 2 m, never lags over 10 s | OSP:457, 1072 | |
| 1 | m | Fight: Tom slides to about 1 m in wind-up | OSP:856, 1257 | |
| 0.1 | s | Blow starts | OSP:190, 852 | |
| 0.25 to 0.40 / 0.63 to 0.85 | s | Jab / heavy blow lands | OSP:190, 852 | |
| 0.45 to 0.80 | s | Tell before an incoming blow | OSP:190, 854 | |
| 0.4 | s | Two men swing at most 0.4 s apart | OSP:190, 854 | |
| about 0.3 | s | Slip | OSP:190, 854 | |
| about 2 | s | Grab hold | OSP:858 | |
| 6 to 10 / 4 to 8 | jabs / s | Mashing empties Tom / wind back | OSP:191, 854 | |
| fewer than 3 in 10 | | Masher wins fair fights | OSP:854 | |
| 10 to 30 | s | Knock-out from behind | OSP:325, 862 | |
| 2 / 3 / 4 | blows | Chair / brick / bin lid break | OSP:324, 862 | |
| 3 | s | Fall within 3 s of a blow can kill, rarely | OSP:864 | |
| 60 | s | Tom in control after a beating; 60 s in S37 | OSP:336, 868, 613 | |
| 60 | s | Man in water climbs out within 60 s | OSP:327, 812 | |
| 25 | % | Slower-fights assist: wind-ups 25% longer | OSP:358, 690 | |
| 24 | units | Minimum on-screen element | OSP:84, 688 | |
| none | | Constables' own speeds | none | only "vaults it slower" (OSP:373, 810) and "no pursuer catches by a speed Tom cannot match" (OSP:1022) |
| 120 / 100 | ms | Ledger opens / input answers within | OSP:112, 692 | |
| 60 / 30 | fps | Target / floor | OSP:1264 | |

## H. Money

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| 23.50 | £ | Tom's starting money | OSP:110, 655, 1034 | "Tom has £23.50 in his pocket" |
| 18 | £ per week | Rent, due every Friday | OSP:110, 655, 1034 | "the rent, £18, is due on Friday" |
| 80p | £ | Fare base ("plus distance") | OSP:99, 914 | |
| (arith) at least 23 | fares | Fares at 80p needed for £18 (22.5), before distance and before drivers' wages | derived | |
| 156 | £ | Debt book total: Darren 22, Wayne Harrison 30, Lee Drewery 15, Julie Kettlewell 9, Dennis Iveson 80 | OSP:110, 1049-1054 | "£156 in all" (22+30+15+9+80 = 156) |
| 10 + 80% | £ and % | Count: book can hide £10 plus 80% of fares really driven since last wash | OSP:160, 1062; DEF:375 | "£10 plus 80% of the fares really driven" |
| none | £ | Front's till raises the washable amount "by a set amount a week" | OSP:1062, 1117; DEF:375 | amount not set (balance figure pending GD-07) |
| about 0.4 | ratio | Rita's fence rate of an honest price | OSP:290, 964 | "about 0.4 of an honest price" |
| about 0.33 | ratio | Recommended fence rate (a third of retail; 0.2 jewellery to 0.4 video recorder) | CLD:35 | "Set the fence's rate to about a third of retail (0.33)" |
| 3 | offers | Haggle length at most | OSP:290, 962 | |
| 8 | s | Hold-up: till given about 8 s | OSP:533, 974 | |
| 12 | game hours | Hold-up if Tom taken | OSP:976 | |
| n/a | sample text | Money page example wording | OSP:1044 | "£31 in your pocket. The tin has about £40 in it. Rent, £18, Friday. Darren still owes £12." |
| none | £ | Wages (drivers), job pay, cuts, prices of torch, coat, car, jacket, doctor, bribes | OSP:1078, 966 | "A driver gets a weekly wage"; "price tables" are out (OSP:683); no figures |
| none | £ | Money targets per week or act; firm income | DEF:190-193 | GD-07 PENDING: curve "Act I, £23.50 and rent at £18 a week, a week of fares pays it, the debts at £156"; Acts II and III have no amounts |
| 23.36 / 20.70 | £ per week | 1990 / 1989 English council rent (provisional) | CLD:10 | "£23.36 a week (April 1989 £20.70)" |
| 65 / 47 | £ per week | 1991 private rent / recent movers | CLD:11 | "£65 a week" |
| 27 (14 after HB) | £ per week | 1990 rent, households under £10,000 | CLD:12 | |
| 1.00; 20p per 340.5 yd (about 1.04 a mile) | £ | London cab fare from 8 June 1990 | CLD:13 | "£1.00 minimum for the first 0.58 mile, then 20p each 340.5 yd" |
| about 45p | per litre | Diesel early 1990s (recollection) | CLD:14 | |
| one third (range 1/4 to 1/2); 38 / 21 / 33 | % | Fence and burglar price estimates | CLD:31-33 | |
| none | | PATCH has no design amounts (sim-harness strings $120, $300, $80, $180, $200 are test text) | PATCH:49 | |

## I. Everything else two parts depend on

| Number | Unit | What it is | File:line | Short quote |
|---|---|---|---|---|
| 3 / 1 | game days | Marks: bruise and cut lip 3, limp 1 | OSP:874, 336 | |
| days | | Hospital costs days (no number) | OSP:868, 906 | "Hospital costs days, never money" |
| permanent | | Witness memory; body never cools | OSP:784, 790 | "Memory is permanent and per person." |
| 1 to 7 | game days | Talk cooling by kind | OSP:790; CLD:49 (KCD2 "a few in-game days") | |
| 4 | stages | Ellis: nothing, asking round, investigating, manhunt | OSP:1010 | |
| 3 | people | Ellis stage: talk passed by three people of Tom's day world | OSP:435, 1010; DEF:292 | |
| 4 | states | Escalation dial: Fists, Shown, Fired, War | OSP:1150-1154 | |
| 2 | game weeks | Dial falls one step; never to 0 | OSP:1156 | |
| 3 | rivals; 5 ladder rungs | | OSP:1096, 1105 | |
| more than 2 | men | Tom's men seen carrying moves Fired to War | DEF:285 | "(more than two of them, each seen by someone)" |
| 2 | named officers bought | one looks away, one loses a statement once | OSP:1014 | |
| 2 | cars of rival taxi firm | | OSP:908 | |
| 2 / 3 / 5 | cars | Firm: 2 at start, 3rd at rung 2, 5 at rung 3 | OSP:1127-1129 | |
| 2 | fronts and 2 rounds | Rung 4: at least two of each, plus men at dock gate, cold store, landing | DEF:229 | "(at least two of each)" |
| 2 | things | Under the coat; 1 in hand | OSP:128, 950, 1082 | "Two things fit under the coat" |
| 2 | s | Pickpocket hold about 2 s; drawer 2 s, desk 4 s, wardrobe 5 s (double in dark) | OSP:263, 948, 960 | |
| 6 | s | Forcing a door | OSP:263 | |
| 3 | people | Crew recruits: first Julie (need), second by hook | OSP:449 | |
| 1 | second man | Man at side takes second man; two against two | OSP:458, 866, 1072 | |
| 2 / 3 | | Odds: two against one deadly, three a beating | OSP:866 | |
| 7 | slots | Seven perceivable slots per act; 5 rungs of identification | OSP:778-780 | |
| 8 | manual slots | At least 8 manual saves, 3 rotating autosaves | DEF:81 | |
| 200 | % | Text scale maximum (contrast at least 4.5 to 1) | DEF:39 | "scales from 100% to 200%" |
| 10 / 24 to 85 | m / mm | Photo mode radius; lens | DEF:25 | |
| 86 (75 to 100 proposed) | degrees | Street lens | OSP:804; DEF:14 | |
| 7 | marks | GTA VI police knowledge marks (reference) | MECH:83 | |

## Sections thin or without numbers

- A Map: no size of the Hook or docks anywhere (metres, km, blocks, road length) except Quay Street 48 m (RUL:119). No count of streets or buildings; crossing times are only provisional bands (DEF:151-155).
- B Cars: no top, typical or town speed; no police-pursuit timers beyond the shared 90 s, 7 s and 70 m; no reference-game chase lengths.
- C Clock: shop, pub, club hours, curfews, routine schedules, evening span and separate day/night lengths have no numbers in these files.
- D Jobs: no job, fare or happening counts per hour, week or act (GD-08, RT-03, RT-19 all pending PC measuring).
- E Crowd: no per-street or per-hour counts, no total residents, no constables-on-shift by hour (only 25 busiest-view people and 30 regulars).
- G On foot: no Tom speeds, no stamina numbers, no constable speeds.
- H Money: no wages, prices, job pay, cut sizes, firm income or per-week or per-act targets (GD-07 pending).

## Arithmetic and mismatches seen while extracting (no judgement)

- Minute town knows him: minute 13 (OSP:750) against minute 30 (OSP:1263).
- Fares with a wrinkle: "about half" (OSP:173) against "every fare after the first" (OSP:916, 1274).
- Lost-chase search: "about a game hour" = 45 real s (OSP:143) against "half a real minute at most" (OSP:1008).
- Happening repeat rule: 30 minutes (OSP:202, 938), one street twice in a week (OSP:938), within a game week (DEF:337).
- Fence rate 0.4 (OSP:290, 964) against 0.33 recommended (CLD:35).
- First-hour clock check (arith): at 45 s a game hour, 15:40 Monday plus 7:00 of play is 01:00 and plus 11:30 of play is about 07:00 Tuesday, while OSP:716-720 place Ron's ask "after dark" at 7:00 and the landing (open 22:00 to 01:00) at 11:30; the clock stops in talk and during the Ledger is not stopped (DEF:327), so the true offset is not derivable from these files.
- Arrest cost 6 to 22 game hours (4.5 to 16.5 real min if played) against "under 2 real minutes" (OSP:242, 996).
- Act II: 7 weeks x 7 x 18 min = 14.7 real h against "11 to 14 hours" (OSP:1202).
- 80p base fares: 23 fares for £18 rent (arith), against fares of 1 to 2 real min each.
