# Candidate hidden details, reader C (BLUEPRINT 03, 04, 05)

Read: BLUEPRINT-03-story.md, BLUEPRINT-04-place.md, BLUEPRINT-05-looks-sound.md, in full.

How I judged the fields.
- Status: "designed" means rules and exact numbers or a named data file are given. "partly" means words only, numbers or data missing, or marked pending, unmeasured or gap. "missing" means a wish is mentioned and no design is given. Many parts in 4 and 5 carry "Status: outside" (Unreal work judged by the gate); I judged those on their text, and say so.
- First ten hours: week one is 3.8 to 5.6 hours of clock (3.1.1) and a game week is about 5.6 real hours (3.7, RT-19), so ten hours reaches the end of week one and about the middle of week two. Act II beats set for weeks 3 to 6 are "no".
- Build or content: "build" means a system, rule or data structure the code must have; "content" means only more written, drawn or recorded material.
- Where a part says "Data: ... .json", I name the file as the data file.

---

## A. Weather, light and the look of the street

### 1
- Detail: Rain sends the street's crowd home: every crowd band halves, voices halve, and cars grip less on the wet road.
- Parts: 4.8 (data: light-weather.json); 3.2.4 (crowd bands, data: crowd.json); 5.5.4.
- Status as written: designed. 4.8 gives "each crowd band halved" and "halves the voices"; Status: ruled (his ruling or canon).
- First ten hours: yes.
- Build or content: n/a (designed).

### 2
- Detail: The same street, played dry, in drizzle and in rain, looks and sounds like three different places, and a wet road takes hours to dry while puddles last days.
- Parts: 4.8; 5.3.3 (data: light-weather.json).
- Status as written: designed. "A wet road takes about 3 to 14 hours to dry and puddles days"; test "S: same seed in three weathers".
- First ten hours: yes.
- Build or content: n/a (designed).

### 3
- Detail: The wet street is dark and glistening, mirroring the sky and the terraces, and the puddles are real water.
- Parts: 5.3.3 (data: light-weather.json); 5.11.4 "Wet ground" row.
- Status as written: partly. 5.3.3 is "Status: outside"; the bar is a ruling ("dark, glistening, mirroring"), the values are "ruling for the bar, judgement for the values" (roughness 0.06 asphalt, 0.16 reads dry).
- First ten hours: yes.
- Build or content: content and tuning (one wetness value is already specified); no new system.

### 4
- Detail: At dusk the street lamps come on and take ten minutes to warm from pink to full sodium yellow.
- Parts: 4.7 (data: light-weather.json); 4.4 (low-pressure sodium, 35 W lanterns).
- Status as written: designed. "dusk comes with the lamps switching on (about 70 lux, the sodium taking 8 to 15 minutes to turn full yellow)"; Status: ruled.
- First ten hours: yes.
- Build or content: n/a (designed).

### 5
- Detail: Night on Quay Street is pools of lamp light with real darkness between, not one orange wash, and Frank's feet always stay readable.
- Parts: 4.7; 4.4; 5.4.2 (data: light-weather.json).
- Status as written: designed. "pool under a lamp is about ten times the night fill", "3.5 to 6 lux average"; Status: ruled.
- First ten hours: yes.
- Build or content: n/a (designed).

### 6
- Detail: The corners of the screen darken at night by exactly the light value that decides whether a watcher can see Frank.
- Parts: 4.7; 5.4.2.
- Status as written: designed. "the frame's corners darken with the same light value the watchers use".
- First ten hours: yes.
- Build or content: n/a (designed; the link between picture and the watcher rule is a code rule already named).

### 7
- Detail: The empty unit on the parade has bare glass dressed with card, cardboard and a fallen blind, and is never painted over.
- Parts: 4.1.1 (R5; data: map.json).
- Status as written: designed. His ruling R5; the dressing items are listed. Status: outside.
- First ten hours: yes.
- Build or content: content.

### 8
- Detail: Quay Street's four lamp posts are plain concrete columns with boat-shaped lanterns, each throwing a straight-down cone and a faint glow, placed on alternate sides.
- Parts: 4.1.1; 4.4 (data: map.json).
- Status as written: designed. "x 8 east, 18 west, 28 east, 38 west", "lantern top at 5.0 m", cone 22 to 46 degrees, 167 lm; "staining still to finish".
- First ten hours: yes.
- Build or content: content (staining only).

### 9
- Detail: Window frames are white, some surrounds painted, with sash bars and real sky in the glass; shop glass shows the street.
- Parts: 5.3.4 (R6); 4.1.1; 5.3.1.
- Status as written: partly. 5.3.4 "Status: outside"; the look is a ruling, the glass method is research (Thin Translucent, room dimmed to a tenth), with no per-shop list.
- First ten hours: yes.
- Build or content: content and shader tuning.

### 10
- Detail: A broken window shows scattered glass in a glittering band about 2 m deep, and the frame stays empty until the owner mends it.
- Parts: 5.3.4; 5.3.2; 5.5.2.
- Status as written: designed. "radial cracks, ragged dark hole low, glass thrown back up to 3 m, a glittering band of shards about 2 m deep"; "stays until mended".
- First ten hours: likely.
- Build or content: n/a (designed).

### 11
- Detail: Frank leaves a mark that stays: blood on the pavement lasts until rain or a bucket washes it, and a forced door shows for a day, and all of it survives a save and load.
- Parts: 5.3.2; 5.9; 3.5.3.
- Status as written: partly. 5.3.2 "Status: outside"; rules in words ("until rain or a bucket", "a forced door shows for a day"), no wear-layer data or durations except the door.
- First ten hours: likely.
- Build or content: build (persistent marks that save, and that rain clears).

### 12
- Detail: Worn paths across the verge, scuffed shop steps, pigeon marks under ledges and soot over coal-fire chimneys show where people actually walk.
- Parts: 5.3.2 (catalogue "Wear placed by use").
- Status as written: partly. "the wear layer is seeded; placing it by use is not yet stated."
- First ten hours: yes.
- Build or content: build (wear driven by the routes people use) and content.

### 13
- Detail: Homes show their class in how they are heated: gas fire, storage heater, coal fire, paraffin heater, and nearly a fifth have no central heating.
- Parts: 4.9 (catalogue "Class shown in heating"); 4.3.4 (18.5%).
- Status as written: partly. "the part gives the share of homes without central heating; the dressing by class is not named."
- First ten hours: likely.
- Build or content: content.

## B. The street, shops and 1990 texture

### 14
- Detail: The shops keep real hours: shut on Sunday, the newsagent from six, the caff to three but late on Friday and Saturday, the pawn shop's back room open by knock until ten with its window lit.
- Parts: 4.3.3 (data: places.json).
- Status as written: designed. Hours given for newsagent 06:00 to 18:00, caff 06:00 to 15:00 (22:00 Fri and Sat), launderette 08:00 to 23:00, pawn 10:00 to 17:00, chip shop 23:30.
- First ten hours: yes.
- Build or content: n/a (designed).

### 15
- Detail: Everything costs 1990 money: tea 30p, a caff meal £2.50, a crowbar £6, a torch £4, a key cut for £1.50.
- Parts: 4.3.3 (data: places.json).
- Status as written: designed. Prices listed in 4.3.3.
- First ten hours: yes.
- Build or content: n/a (designed).

### 16
- Detail: The pubs on the street are boarded up or serve food, nobody can bet on anything, and the snooker hall and the boxing club have no money in them.
- Parts: 4.10; 4.3.3 (Pastimes, Q13; data: map.json).
- Status as written: designed. "Pubs may stand as buildings on the street, boarded or serving food"; map.json places the snooker hall, boxing club, fishing spots and pigeon loft.
- First ten hours: yes.
- Build or content: n/a (designed).

### 17
- Detail: Frank can fish off the quay, play snooker upstairs by the landing, and visit an allotment pigeon loft on Chapel Lane.
- Parts: 4.2.1 (Q13); 4.3.3 (data: map.json).
- Status as written: partly. Places and coordinates are given (three fishing places, snooker x 13 to 33); what the activities are and what they give back is not designed.
- First ten hours: likely.
- Build or content: build for fishing (a verb and its rules); content for the rest.

### 18
- Detail: Every door that matters has a number, every street has a Marcellus name plate at each end, and typed letters are in Courier Prime.
- Parts: 4.1.3; 4.9 (data: letters-and-print.json).
- Status as written: designed. Fonts and rule named; Status: decided / ruled.
- First ten hours: yes.
- Build or content: n/a (designed).

### 19
- Detail: The poll-tax posters on the walls belong to an invented local campaign, never a real party or person.
- Parts: 4.9 (data: letters-and-print.json).
- Status as written: partly. "Poll-tax posters are an invented local campaign"; no poster text or placement.
- First ten hours: yes.
- Build or content: content.

### 20
- Detail: In all of Meridian there is one CCTV camera, at the bank, and one camcorder that can turn up as a rare witness.
- Parts: 4.9 (Q10).
- Status as written: partly. Rule stated; no place, trigger or number for the camcorder.
- First ten hours: likely.
- Build or content: build (a witness kind with its own rule) and content.

### 21
- Detail: The details are period-exact: no tactile paving, a KX100 phone box, a 390 mm pillar box, skip plates and to-let boards that follow the 1989 rules.
- Parts: 4.4 (prior research); 4.9; 4.3.4 (satellite dishes about 1 in 20 to 30).
- Status as written: partly. Figures are in "Prior research" only and "search-summary figures stay leads until re-read"; Status: outside.
- First ten hours: yes.
- Build or content: content.

### 22
- Detail: A parked cab or car has a G or H plate by date: G until 31 July 1990, then H, so a new car in October 1990 wears an H, and every car is a fictional make.
- Parts: 4.5.2 (prior research); 4.6.1.
- Status as written: partly. The plate switch is in "Prior research" only; the fictional-makes rule is "Status: outside".
- First ten hours: yes.
- Build or content: content (plate by car age is a small data field).

### 23
- Detail: Frank's cab is recognisable on the street: the roof sign and plate make it the firm's, and anyone who sees it names the car.
- Parts: 4.6.1; 3.5.1.
- Status as written: partly. The sign and plate are in 4.6.1 "Status: outside"; the "anyone who sees it names the car" rule is in 3.5.1 and 5.2.6.
- First ten hours: yes.
- Build or content: n/a for the rule (designed in 3.5.1); content for the model.

### 24
- Detail: Traffic on Quay Street slows from 60 m out, stops 2 m behind a person in the lane, hoots at 3 s and 10 s, and halts dead if you step out in front.
- Parts: 4.5.1 (data: tune.json).
- Status as written: designed. Numbers given; Status: ruled.
- First ten hours: yes.
- Build or content: n/a (designed).

### 25
- Detail: Cars indicate and pull aside for a siren.
- Parts: 4.5.1 (catalogue "Traffic that indicates and yields to sirens").
- Status as written: partly. "indicating and yielding are not named."
- First ten hours: likely.
- Build or content: build (a siren reaction rule for traffic).

### 26
- Detail: The same week always plays the same traffic: cars arrive from a seeded stream, a gap of 450 s at night, 50 s in the rush.
- Parts: 4.5.1 (data: tune.json).
- Status as written: designed. Gaps by hour listed.
- First ten hours: yes.
- Build or content: n/a (designed).

### 27
- Detail: Dockers wear nylon anoraks, not the donkey jacket, because that is what the 1989 photographs show, in navy, charcoal, brown, bottle green and oatmeal.
- Parts: 5.1.4 (prior research); 5.11.4 "Crowd dressing".
- Status as written: partly. Palette and anorak note are "Prior research"; no wardrobe list per job or person.
- First ten hours: yes.
- Build or content: content.

### 28
- Detail: Frank's coat changes how the street treats him: a £15 second-hand coat as he arrives, a £45 decent jacket, a £90 good overcoat, and a dark coat for nights.
- Parts: 5.1.4; 3.6.4 (greetings by regard).
- Status as written: partly. Outfits and prices are designed; "each changing how strangers speak to him and which doors open" has no rule or table. Status: outside.
- First ten hours: likely.
- Build or content: build (outfit as an input to greeting and door rules) and content.

### 29
- Detail: No one in the crowd is frozen: idles start at random moments, run at 0.9 to 1.1 speed, and neighbours never match.
- Parts: 5.2.5.
- Status as written: partly. Numbers given, but "work, smoke and talk idles are not built."
- First ten hours: yes.
- Build or content: content (animations), tuning only.

### 30
- Detail: The crowd keeps the clock: dockers at dawn, shoppers by day, the street emptying at night, with half the people sitting or standing in twos and threes facing inward.
- Parts: 3.2.4 (data: crowd.json); 4.2.2.
- Status as written: designed in numbers (4 to 10 people per frame at busy bands, 0 to 2 on quiet nights), but "Status: pending (a reference-game lead...)".
- First ten hours: yes.
- Build or content: n/a for the rule; the counts are still open.

## C. Sound and music

### 31
- Detail: Footsteps carry about 3.6 m at three in the morning and nothing at noon, because sound travels twice as far in the small hours.
- Parts: 5.5.1; 4.7 (data: sounds.json).
- Status as written: designed. Numbers named. Status: unmeasured.
- First ten hours: yes.
- Build or content: n/a (designed).

### 32
- Detail: Each surface has its own footstep: setts, flagstone, tarmac, wet ground, wood and stairs, iron plates, boards and lino, for each kind of shoe.
- Parts: 5.5.1 (SND-05 to 07; data: sounds.json).
- Status as written: designed in the plan (at least 7 surfaces, three shoe kinds); "the prototype has no surface, shoe or left and right."
- First ten hours: yes.
- Build or content: build (surface and shoe lookup for steps) plus content.

### 33
- Detail: A forced door or breaking glass is the loudest thing in a quiet street, and each room has its own tone and echo as you step through the doorway.
- Parts: 5.5.2 (SND-17, SND-18); 5.5.4 (SND-16; data: sounds.json).
- Status as written: designed. "crossfaded over about 1 m of walking and at least 0.5 s"; tone "at least 10 dB under speech".
- First ten hours: yes.
- Build or content: n/a (designed).

### 34
- Detail: Walls and shut doors muffle a shout, and a shout through an open door carries.
- Parts: 5.5.4 (checklist item 2).
- Status as written: missing. "missing: walls and shut doors must dull sound, and open doors and windows must let it through."
- First ten hours: likely.
- Build or content: build (sound occlusion by openings).

### 35
- Detail: A car passing pans across your ears from its own side, and sounds change when Frank turns.
- Parts: 5.5.3 (checklist item 1).
- Status as written: missing. "today only reach in metres is set."
- First ten hours: yes.
- Build or content: build (spatial audio rule).

### 36
- Detail: Frank's cab sounds like 1990: a small four-cylinder idling near 28 Hz, an automatic gearbox that only dips softly, and tyres that squeal as you near the grip limit.
- Parts: 5.5.5 (SND-08 to 11; data: sounds.json).
- Status as written: partly. Frequencies, reach (44 m, horn 60 m) and squeal point given; "length not yet set" for the gear dip. Status: unmeasured.
- First ten hours: yes.
- Build or content: content and one number; no new system. A damaged cab sounding hurt is "Not yet" (build).

### 37
- Detail: A gunshot is heard 177 m away with an echo off the warehouses and quay walls, then the whole street goes quiet and the gulls lift.
- Parts: 5.5.6 (SND-13, SND-19).
- Status as written: designed. The 177 m and the behaviours are given in Prep. Status: unmeasured.
- First ten hours: likely.
- Build or content: n/a (designed).

### 38
- Detail: The only music in LEDGER comes from the world: a radio in the caff, a record through a window, the chapel organ, and it sounds like it is through a small speaker.
- Parts: 5.7.1 (SND-21 to 23); FIT-P09 (data: sounds.json).
- Status as written: designed as a rule ("no music unless a world source ... is within its distance"; small-speaker filter); tunes themselves are not made, and a short score is held ("nothing built until he says").
- First ten hours: yes.
- Build or content: build for the distance rule and filter (already specified); content for the tunes. A score exception is a gap.

### 39
- Detail: There is never combat music: nothing starts or changes because a fight or chase begins.
- Parts: 5.5.6; 5.7.1.
- Status as written: designed. "There is never combat music."
- First ten hours: yes.
- Build or content: n/a (designed).

### 40
- Detail: The chapel bell, a milk float, the paper round and a light coming on at a curtain when a night noise wakes someone mark the hours.
- Parts: 5.5.3 (catalogue "The day's clock heard and seen"); 5.2.6.
- Status as written: partly. "the chapel bell and lit windows are covered; milk float, paper round and the curtain answer are not."
- First ten hours: yes.
- Build or content: content mostly; the curtain answer is a small build (noise leading to a lit window and a face).

### 41
- Detail: Every shared street line is heard once in a real hour at most, and no person repeats a line inside a day.
- Parts: 3.6.3 (data: lines/); FIT-L01; FIT-F19.
- Status as written: designed. "No shared street line is heard twice in one real hour anywhere", "a person's own line comes once a day at most". FIT-F19 itself is "Status: pending".
- First ten hours: yes.
- Build or content: n/a for the rule (designed); content for the line count.

### 42
- Detail: In the rain people grumble about it, and the crowd's greeting lines change by how they feel about Frank (afraid, angry, knows and likes him).
- Parts: 3.6.4 (data: lines/).
- Status as written: designed. "At least 6 lines per situation per kind of speaker"; situations list names rain and regard greetings. Status: unmeasured.
- First ten hours: yes.
- Build or content: content (cloud-week already holds 1,225 lines).

## D. People who know and react

### 43
- Detail: A watcher turns his head at least 0.8 s before he recognises Frank, and two heads together, a pause in a walk, a step back at night and a face at a lit window all say "they know".
- Parts: 5.2.6; 5.3.4.
- Status as written: designed. "a glance is 0.35 s", "at least 0.8 s before identification"; Status: ruled.
- First ten hours: yes.
- Build or content: n/a for the rule; content (clips) for the poses.

### 44
- Detail: Ada sits in her dark front room as a watcher who is a window, and her back gate opens on the terraces' ginnel.
- Parts: 4.3.4; 5.3.4 (data: rooms.json).
- Status as written: designed. A window is a watcher "only when a figure shows at it, head and shoulders at the glass".
- First ten hours: yes.
- Build or content: n/a (designed).

### 45
- Detail: A man who only heard about last night says "I heard something about you" and never says what happened.
- Parts: 3.6.2.
- Status as written: designed. "a man who only heard of last night says 'I heard something about you', never what happened"; tested with planted bad replies; Status: ruled.
- First ten hours: yes.
- Build or content: n/a (designed).

### 46
- Detail: People talk at the counter and the bus stop about what Frank did, in their own words.
- Parts: 3.6.4 (catalogue "Bystander talk reflects what Frank just did"); 3.6.2 (MEM-01).
- Status as written: partly. "the situation list has a body or a man down but not recent deeds heard at second hand."
- First ten hours: yes.
- Build or content: build (a told-deed source for street lines) and content.

### 47
- Detail: How you beat a man gets told: three blows and walk away is a different story from kicking him on the floor, and the worse telling is never undone.
- Parts: 5.8 GV-06; 3.5.5 ("what was said is what the town then believes within a game day").
- Status as written: partly. GV-06 "Status: decided" with a paired-fight test but no numbers or line data for the two versions.
- First ten hours: yes.
- Build or content: build (told version derived from beliefs, not a meter).

### 48
- Detail: Every witness can be met again with a face and an own line, and a crowd extra who catches any slot of a deed becomes a kept person with a fixed face, a coat and a home.
- Parts: 5.1.5; 3.2.3 (MEM-07); 3.2.4.
- Status as written: partly. 5.1.5 "Named only; not designed beyond"; "No repeat distance or variety rule exists."
- First ten hours: likely.
- Build or content: build (promotion of crowd extras to kept people).

### 49
- Detail: Walk away mid-conversation and the person remembers it.
- Parts: 3.6.1 (checklist item 5).
- Status as written: missing. "missing: a rule for Frank walking off mid-talk (talk ends, the person remembers)".
- First ten hours: yes.
- Build or content: build.

### 50
- Detail: Call on a friend twice inside the gap and the door is cooler: "you again".
- Parts: 3.2.7.
- Status as written: partly. "Status: pending (a reference-game lead...)"; "the set gap" has no number.
- First ten hours: yes.
- Build or content: build (a per-friend gap and a cooler-door state, which also feeds the ending rule).

### 51
- Detail: What the town calls Frank climbs as he does: "the new owner", "Nowak", "Frank", "Frankie", and Sheila alone holds back his name until she trusts him.
- Parts: 3.2.1; 3.6.4 (greetings by regard).
- Status as written: partly. Names are listed; no thresholds. "Sheila's trust is a state the town sees, not a day count (Q7)".
- First ten hours: yes.
- Build or content: build (a trust state and a name ladder keyed to it).

### 52
- Detail: Characters glance at Frank before they answer, with no thinking noise or loading sign, and if the answer is slow a written line plays.
- Parts: 3.6.1; 5.6.3; 5.2.4.
- Status as written: designed. "reply within 2 s or the written line plays"; Status: ruled. One gap: whether the late live reply or a prepared line is shown.
- First ten hours: yes.
- Build or content: n/a (designed).

## E. Frank's work: carries, fares, debts, jobs

### 53
- Detail: Frank steps off the ferry on Monday 15 October 1990, about twenty to four, under a grey sky, with £23.50 in his pocket and a hint that names the way to Quay Street if he stands four seconds.
- Parts: 4.2.1 (Q12); 3.1.1; 5.8.2.
- Status as written: designed. "20 s skippable shot", "stands 4 s", date, money, rent (£18, Friday). Status: outside.
- First ten hours: yes.
- Build or content: n/a (designed).

### 54
- Detail: The first night's envelope can go three ways: the lit quay (quick, seen), the dark yards' lane (slow, footsteps carry half as far), or the cab (quickest, and anyone who sees it names the car).
- Parts: 3.5.1 (data: jobs/).
- Status as written: designed. Beat constable "1.1 m/s", "night cycle is about 7 real minutes", "Mickey's door is in his sight at least every 4 minutes"; Status: unmeasured.
- First ten hours: yes.
- Build or content: n/a (designed).

### 55
- Detail: Mickey's debt book is five debts and each pays a different way: Darren pays in what he hears, Wayne in goods from the pawn's back room (haggled), Julie cannot pay (mercy or shame), Drewery stands with the docks behind him.
- Parts: 3.5.2 (data: jobs/); 3.1.1.
- Status as written: designed. Sums (£22, £30, £15, £9, £80) and three keys for Iveson given; Status: unmeasured.
- First ten hours: yes.
- Build or content: n/a (designed).

### 56
- Detail: Squeeze a debtor or let him off, and the whole street knows within a game day.
- Parts: 3.5.2; 3.5.5 ("what was said is what the town then believes").
- Status as written: designed. "squeezing and letting a debt go are both told on the street within a game day".
- First ten hours: yes.
- Build or content: n/a (designed).

### 57
- Detail: Every lock has at least three keys: a key lent or copied (Ian Megginson knows every lock), a key lifted from a pocket, a back way a routine leaves open, or force.
- Parts: 3.5.3 (data: rooms.json); 3.5.6.
- Status as written: designed. Search times (drawer 2 s, desk 4 s, wardrobe 5 s, doubled without a torch); drawer heard at 2 m, a forced cupboard at 10 m. Status: unmeasured.
- First ten hours: yes.
- Build or content: n/a (designed).

### 58
- Detail: An ordinary drawer holds a letter, a bill, a photograph, a few coins, cigarettes or a spare key, and never more than £2.
- Parts: FIT-P52 (4.4).
- Status as written: designed. "a small written set ... never worth more than £2". Status: decided.
- First ten hours: yes.
- Build or content: n/a (designed).

### 59
- Detail: Fares are named people on their own routine: Brenda Laverack to the fish dock at dawn, the packing shift from the cold stores at half past five, a lodger for the last ferry, and a later ride changed by what Frank did.
- Parts: 3.4.1 (data: fares.json); FIT-G7; 4.2.2.
- Status as written: designed. "£2.50 to £3.50", "at least 7 in the first week", "at least 40 fare people". Status: unmeasured. Open gap: how 40 people and 40 to 80 fares square with fares being few (R11).
- First ten hours: yes.
- Build or content: n/a for the rule; content for the people.

### 60
- Detail: Every fare after the first carries a small twist: the talker, the parcel, the tail, the runner, the wait, the hurry, or somebody who matters getting in, and never the same twice running.
- Parts: 3.4.2; FIT-F20 (data: fares.json).
- Status as written: designed. Seven wrinkles named; "no wrinkle twice running". Status: unmeasured.
- First ten hours: yes.
- Build or content: n/a (designed).

### 61
- Detail: Pauline gives the way by landmark, "past the chapel, second left, the house with the slippers on the step", and a driver who follows only her words always arrives.
- Parts: 3.4.3; 4.1.3.
- Status as written: designed. "ER-DRIVE-09: always right, repeated on a key"; Status: ruled.
- First ten hours: yes.
- Build or content: n/a (designed).

### 62
- Detail: Nothing said on the radio is private: the whole office and every cab hear it, so Frank's day driver can be the Widow's first source on him.
- Parts: 3.4.3; 3.2.2.
- Status as written: designed. "Nothing said on the radio is private"; Kevin is "one of the Widow's eyes". Status: ruled.
- First ten hours: likely.
- Build or content: n/a for the rule; content for Kevin's leaks.

### 63
- Detail: A fare can wave Frank's cab down in the street.
- Parts: 3.4.1 (catalogue "People flag the player's vehicle").
- Status as written: missing. "Not yet: fares come by Pauline's radio; street hails are for the design proof to weigh".
- First ten hours: yes.
- Build or content: build (a hail trigger beside the radio).

### 64
- Detail: Jobs reach Frank by a note Sheila or Pauline took ("a man came for you, said he'd be at the caff at six"), a phone-box call, a man waiting by the car at night, or a tip from Darren, never a marker.
- Parts: 3.5.7; 3.5.6 (Ledger line of about 22 words).
- Status as written: designed. Channels listed; Status: decided.
- First ten hours: yes.
- Build or content: n/a (designed).

### 65
- Detail: Fence a lifted thing and Rita pays a third of retail; buy it back within seven game days for the price plus a quarter, and it is never at Rita's because fences hold nothing.
- Parts: 3.5.4; 4.3.3.
- Status as written: partly. Numbers given (0.33, 7 days, plus a quarter); "No part for the buyback itself yet". Rita fences "from rung 2".
- First ten hours: likely.
- Build or content: build (buyback rule) plus content.

### 66
- Detail: A pickpocket lift is a held press of about 2 seconds, felt by an attentive man in good light or with fewer than three people near.
- Parts: 3.5.4.
- Status as written: designed. Status: unmeasured.
- First ten hours: likely.
- Build or content: n/a (designed).

### 67
- Detail: A tailed man looks back every 20 to 40 seconds and at every corner; "a shape is nothing, a mark is a doubt, a face he knows ends the tail".
- Parts: 3.5.4.
- Status as written: designed. Intervals given; Status: unmeasured.
- First ten hours: likely.
- Build or content: n/a (designed).

### 68
- Detail: Any chase that reaches the edge of the Hook ends as lost within 2 seconds: the pursuer turns back and the patrol waits on that road all night.
- Parts: 4.1.4 (data: places.json).
- Status as written: designed. "plate read within 18 m in light 0.7 or more is noted", "a constable to the office the next morning at ten". Status: decided.
- First ten hours: likely.
- Build or content: n/a (designed).

## F. The places, the water, the animals

### 69
- Detail: Frank can never walk into the harbour: the quay edge stops him like a kerb, a man knocked in climbs out at the nearest ladder within 60 seconds, soaked, and the town talks.
- Parts: 4.2.4 (Q19; data: map.json).
- Status as written: designed. "30 minutes along every quay edge ... no fall in"; "what goes in is gone and whoever saw it keeps it".
- First ten hours: yes.
- Build or content: n/a (designed).

### 70
- Detail: The fish dock fills at dawn: 10 to 18 people between 05:30 and 07:00, gulls in flocks of 5 to 20 that rise when someone runs at them.
- Parts: 4.2.2; FIT-P45 (data: map.json).
- Status as written: designed. "Gulls are present on the fish dock every daylight hour in dry weather".
- First ten hours: yes.
- Build or content: n/a (designed).

### 71
- Detail: A tea stall stands at the dock gate from ten at night to six in the morning, and a striped barrier pole and a working crane stand behind it.
- Parts: 4.2.3 (data: map.json).
- Status as written: designed. Hours given; the crane and barrier are "ruled in (24 Nov)" with no spec.
- First ten hours: likely.
- Build or content: content (crane animation).

### 72
- Detail: A yard dog barks at a stranger and draws the owner, so the dog is a witness by sound; throw it a scrap and it hushes; no verb can ever harm an animal.
- Parts: 4.11.1.
- Status as written: designed. "A bark is a noise at its reach"; ER-DOG-01 "checked by trying every verb". Status: decided.
- First ten hours: yes.
- Build or content: n/a (designed).

### 73
- Detail: Frank can pat a dog, and a fox works the bins by night, a dog waits outside the butcher's.
- Parts: FIT-P45 (catalogue "Animals with their own lives").
- Status as written: missing. "short are a fox at the bins, a dog outside the butcher's and a dog Frank can pat".
- First ten hours: yes.
- Build or content: build for the pat (a harmless verb); content for the animals.

### 74
- Detail: The flat above the office is Frank's: kettle, wireless, letters on the mat, a tin under the floorboards and photographs, and he sleeps to skip the night.
- Parts: 4.3.2 (catalogue "Home as play"; data: rooms.json).
- Status as written: missing. "Named only; not designed beyond: what makes it Frank's rather than Mickey's, and what is in each room."
- First ten hours: yes.
- Build or content: content, with a build need for a tin under the floor (a hide and use).

### 75
- Detail: Mickey's office is a 1990 cab office: radio set, ashtrays, kettle, telephone, scuffed counter and real glass that reflects the street.
- Parts: 4.3.1 (data: rooms.json).
- Status as written: partly. "Status: outside"; items listed, "no openable photograph of a real British minicab office interior dated 1985 to 1995".
- First ten hours: yes.
- Build or content: content.

### 76
- Detail: The beat constable tries Mickey's door on his rounds, and the yard has a vault place at the back fence that takes Frank 0.8 s and a pursuer 1.2 s.
- Parts: 4.3.1; 3.5.1 (data: rooms.json).
- Status as written: designed.
- First ten hours: yes.
- Build or content: n/a (designed).

### 77
- Detail: Frank can see the real book behind the locked inner office only when Sheila trusts him, and Mickey's old revolver lies under it, found once.
- Parts: 3.1.6; 3.2.1.
- Status as written: partly. Words and "at least five new names"; scenes file "(data file 18), still to be made". Frame pending "his yes on the measured story is still open (Q18)".
- First ten hours: likely (week one's end or week two).
- Build or content: build (trust state) and content (the book).

### 78
- Detail: Ask about the warehouse fire and the street's version stays a street fact, however it is asked; the truth is never the street's.
- Parts: 3.1.6; 4.3.5; 3.6.2.
- Status as written: designed as a rule ("Test: S: the street version stays a street fact"); Status: ruled. Scene content pending.
- First ten hours: yes.
- Build or content: n/a for the rule; content for the lines.

### 79
- Detail: Sheila has Frank finish a half-written line in the fare book on the first morning, and five weeks later the police read it back.
- Parts: 3.1.1; 3.1.2 (week 5); 3.6.5 (S18).
- Status as written: partly. 3.6.5: "missing are the stored line, the classifier and the comparison."
- First ten hours: likely for the setup, no for the payoff.
- Build or content: build (word-for-word storage, classed lie, truth or blank, compared at returns).

### 80
- Detail: On the first Sunday Sheila asks "So which is it going to be?" and the street learns Frank's answer.
- Parts: 3.1.1.
- Status as written: partly. Scene text from the paper cards; "his yes on the measured story is still open (Q18)", scenes file not made.
- First ten hours: yes.
- Build or content: build (street learns an answer as state) and content.

### 81
- Detail: Danby the teacher is never seen at work, because the school stands closed and empty.
- Parts: 3.2.5; 4.10; 4.3.6.
- Status as written: designed. "Danby is never seen at work (the school stands closed)". Status: ruled.
- First ten hours: yes.
- Build or content: n/a (designed).

### 82
- Detail: The chapel hall holds tea and talk on Tuesday 19:00 to 21:30, the model for a place with no drink.
- Parts: 4.3.6; 4.10 (data: rooms.json).
- Status as written: designed. Day and hours given.
- First ten hours: yes.
- Build or content: n/a (designed).

### 83
- Detail: Beaten, Frank wakes on the pavement, in Grace Rinaldi's kitchen or in hospital, bruises last three game days, a limp one, and the retired doctor stitches for £20 and asks nothing.
- Parts: 4.3.8; 4.3.7.
- Status as written: designed. "in control within 60 real seconds"; "Hospital costs days, never money, and plants a witness".
- First ten hours: likely.
- Build or content: n/a (designed).

### 84
- Detail: Held at the station, hours pass fast: 6 for a window, 8 for a wounding, 12 for a robbery, 22 for a killing, in under two real minutes, and the coat is kept.
- Parts: 4.3.7.
- Status as written: designed. Durations given; Status: outside.
- First ten hours: likely.
- Build or content: n/a (designed).

### 85
- Detail: Hit by a cab at under 10 mph a person staggers and puts a hand on the bonnet; at 10 to 25 mph they roll once and sit up within five seconds.
- Parts: 5.2.8.
- Status as written: designed. Speeds and times given; Status: outside.
- First ten hours: likely.
- Build or content: n/a (designed).

## G. Light touches in the telling

### 86
- Detail: Each act holds at least one scene written to be funny.
- Parts: 3.3.
- Status as written: partly. A sentence in "How it works"; no list of the scenes. Status: pending.
- First ten hours: yes.
- Build or content: content.

### 87
- Detail: A side story starts with no marker when you walk past, with the first at about minute 23 of the first hour, and ends in something the whole town knows.
- Parts: 3.3 (data: side-stories/); 3.7.
- Status as written: partly. "Status: pending"; count "about 25 (at least 22, at most 28)"; one placed at minute 23.
- First ten hours: yes.
- Build or content: content (the stories); the "returns" need a build rule (each story names its return).

### 88
- Detail: Help a stranger on the street and days later he turns up with a small favour.
- Parts: 3.7 (data: happenings.json).
- Status as written: partly. One sentence: "A helped stranger can turn up days later with a small favour"; no rule or data.
- First ten hours: likely.
- Build or content: build (a happening return).

### 89
- Detail: A man fallen on the cobbles or a crate off a lorry at the dock gate can be helped, robbed or walked past, and the street sees which.
- Parts: 3.7; FIT-G6 (data: happenings.json).
- Status as written: designed. Kinds named, at least 60 across 8 kinds, never rolled, none twice in 3 real hours. Status: ruled.
- First ten hours: yes.
- Build or content: n/a for the rule; content for the scenes.

### 90
- Detail: Chase the grocer's shoplifter or let him go, and the street remembers which.
- Parts: 3.7 (catalogue "Owners and witnesses chase a thief").
- Status as written: partly. "Already covered: the shoplifter running from the grocer is a happening".
- First ten hours: yes.
- Build or content: content, with a small build (a thief running with owners chasing).

### 91
- Detail: The clock stops while Frank talks, and no talk scene runs 60 seconds without a choice or control.
- Parts: 5.8.3; 3.2.7.
- Status as written: designed. "the clock stops in talk"; ER-TALK-06. Status: unmeasured.
- First ten hours: yes.
- Build or content: n/a (designed).

### 92
- Detail: Danny Cammack, who once drove Mickey's car and kept the key, is never far away in week one.
- Parts: 3.1.1; 3.2.1.
- Status as written: partly. Words only; "his yes on the measured story is still open (Q18)".
- First ten hours: yes.
- Build or content: content.

### 93
- Detail: The main street is judged plain and period-right everywhere: shop paint, fascia, stallriser and mullions follow the Hull and Grimsby surveys, in red and buff brick with blue bands.
- Parts: 4.3.3 (prior research); 5.3.1.
- Status as written: partly. Dimensions are in "Prior research" (stallriser 0.60, fascia 0.55, mullions 48 mm; brick course 85 to 88 mm). Status: outside; brick saturation ceiling "to be rechecked".
- First ten hours: yes.
- Build or content: content.
