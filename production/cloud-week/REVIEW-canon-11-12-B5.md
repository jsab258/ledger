FAIL

# Canon review: town content (unit 11), ambient lines (unit 12), the first thirty minutes draft (B5)

Fresh reviewer, 13 October 2026, branch cloud/week-42, read only. Nothing else was changed.

**Verdict by piece.** Town content: FAIL (faults 1, 6, 7, 8). Ambient lines: FAIL (faults 2, 4, 5). First thirty minutes draft: FAIL (faults 3, 4). There are **8 faults** and **31 narrow points**. All three pieces would pass once the faults' exact fixes below are applied: every fault is a text change, and none needs a new design. By Jafar's ruling of 9 October, a piece that then fails only on narrow points is a PASS with those points listed.

## What was read and sampled

- **Read in full first:** canon.md; CLAUDE.md; CHARTER.md; RULINGS.md, every line; TOWN.md; PLAN.md; NOW.md; production/specs/hook-cast.json (places, areas, hours, the 41 routines); production/research/shop-hours-1990/NOTE-2026-09-29.md; production/casting/regulars/REGULARS.md and CASTING.md; the approved designs the content leans on (story outline, first hour, day-one, day-three, first-ask, landing, waiting, Ellis, sheila-trust, what-they-call-him, warehouse fire, town-news sample); StreetFacts.cs; FirstMoments.cs; the three cards; both helpers' NOTES.md and HOMES.md; the DECISIONS.md entries ending "Marked for Jafar" (lines 464 to 478 and 526 to 529); DECISIONS 3 October on the trades; the shop-windows target's bay table; the atlas's names.
- **Town:** all 44 entries. For all 14 principals and all 30 regulars I read every non-street fact, every rumour and every answer. The 18 StreetFacts.cs facts were checked once against the code and then by script: every copy in every person is word for word. For all 430 answers a script checked that every cited fact id exists in that person's own facts, that no answer outside a deflection cites a secret, and that every answer that is not a don't-know cites at least one fact. All three hold. I read 60 randomly drawn answers beside the full text of the facts they cite, and read the other answers with their id lists. A script compared every derived "day" fact with the person's schedule, and every rumour's "sure" against the routines for the cases below.
- **Lines:** all 1,643 lines were read, not a sample: the 9 shared kinds, the 4 own kinds (all of Ron, Darren, Father Walsh and June) and all 176 directions. By script I checked line lengths (the longest is 11 words), exact and near duplicates, a hidden-case word list (pint, bet, dogs, pools, flutter, lad, kiddie, school and about 150 more), every capitalised name, the police flags against rules.json's never-police list, and the kinds' members.
- **Draft:** read in full. Section 3.3 and every row of section 4 were recomputed from the two route tables. Each named person's routine place was checked at each beat's clock and at its marked times. Every quoted line was checked against its home (the landing, waiting, first-ask and day-three designs, the town answers and the ambient lines). The hint times were checked against FirstMoments.cs.
- **Gates, run here:** `python3 tools/canon-gate.py` on the seven files (people.json, HOMES.md and NOTES.md from town; lines.json, rules.json and NOTES.md from lines; DRAFT.md) is clean: 0 findings in 35,493 lines. `tools/content-gate.py`'s own `scan()` over every string of people.json, lines.json, rules.json and DRAFT.md gives 0 hits. Its 6 hits are all in NOTES and HOMES prose that names the rule ("gambling debts", "no children anywhere"). The gate run with no arguments walks its declared corpus, which does not include production/cloud-week, so it says nothing about these folders until they are adopted into content/. The helpers' own checks pass as stated: 578 of 578, 2,489 of 2,489 and 64 of 64.
- **Real names:** no real firm, person, club, programme or paper appears, and no real place that canon makes fictional. There is no Hull, Grimsby, Humberside or Hessle Road anywhere in these texts. The one real place is the New Territories in Peter Tang's row, which is his approved sheet's own words and is not Meridian.

## Faults, worst first

### 1. Four regulars hold a design paragraph that tells them other people's secrets (town)

- **File and ids:** production/cloud-week/town/people.json: `hal.k21`, `victor.k19`, `tibor.k20`, `drago.k21`. Each holds the same text, copied with its markdown from game-design/ellis-2026-09-29.md line 18: "**Some never go at all**, ... Rita, the customs officer (the machine's stamp, the roster says), Hal, the pawn's back-room hand, the scrap dealer, and the outfit's man."
- **What is wrong:** Hal, Wayne, Susan and Dennis each "know" that the customs officer is Geoffrey Agar's man and that the outfit's man never goes to the police. Those are other factions' secrets from the empire roster; nothing puts them in reach of a coin dealer, a pawn's porter or a scrap dealer. The texts are marked secret, but they are still these people's knowledge, which trust or Act II can later bring out.
- **Breaks:** RULINGS.md, Talk and AI, 25 Sep: "A character says only what the simulation knows".
- **Whose:** the town helper (unit 11).
- **Exact fix:** replace each text with the holder's own fact:
  - `hal.k21`: "Hal never goes to the police, whatever he sees or suffers; his trade keeps him from it."
  - `victor.k19`: "Wayne never goes to the police, whatever he sees or suffers; his trade keeps him from it."
  - `tibor.k20`: "Susan never goes to the police, whatever she sees or suffers; her trade keeps her from it."
  - `drago.k21`: "Dennis never goes to the police, whatever he sees or suffers; his trade keeps him from it."

### 2. Canned greetings tell Tom what the street thinks of him, whatever the simulation holds (lines)

- **File and ids:** production/cloud-week/lines/lines.json:
  - `darren.greet-nowak.06` "Your name's all over. Nice things. Mostly."
  - `darren.greet-tom.09` "You're famous, you know."
  - `dock_worker.greet-nowak.07` "They tell me you're all right."
  - `casual_worker.greet-owner.07` "They say you're fair."
  - `laundry_worker.greet-nowak.06` "Is it true what they say?"
  - `laundry_worker.greet-tom.04` "We were just talking about you."
- **What is wrong:** these are conditioned only on the name rung, never on what the town holds. After Tom has put Rita's window in, "They say you're fair" is a lie by the game's own state. What people know about Tom is the game's mechanic (canon, D24), and the AI tester reports broken illusions (RULINGS 3 Oct).
- **Breaks:** RULINGS.md, Talk and AI, 25 Sep: "A character says only what the simulation knows".
- **Whose:** the lines helper (unit 12).
- **Exact fix:** replace the texts. Conditions and weights stay as they are.
  - `darren.greet-nowak.06` → "Afternoon, Nowak. Anything you're after, I'm your man."
  - `darren.greet-tom.09` → "Tom! There he is. Got a minute for me?"
  - `dock_worker.greet-nowak.07` → "Mr Nowak. Mind the bollards, they're low."
  - `casual_worker.greet-owner.07` → "The new owner. I'm good with a broom, me."
  - `laundry_worker.greet-nowak.06` → "Nowak. You'll be wanting a collar starched."
  - `laundry_worker.greet-tom.04` → "Tom. Don't look like that, it's only steam."

### 3. The draft has the newcomer learn the fire's truth at minute 17 (draft)

- **File and line:** production/cloud-week/first-30-minutes/DRAFT.md, beat A16, column Learns: "The fire is the story the street will not drop; Mickey's outfit is in it."
- **What is wrong:** Alison gives only the street's version in the beat itself ("The paper called it arson. Nobody was charged."). That the outfit burned the warehouse is the truth the fire design keeps out of the talk. Alison's belief is marked secret in the town data, and nothing in the beat tells a stranger.
- **Breaks:** RULINGS.md, The story and the first week, 30 Sep: "the street's version is a street fact; the truth is never the street's."
- **Whose:** the draft's helper (B5).
- **Exact fix:** in A16, column Learns, replace the text with "The fire is the story the street will not drop." (B16's words).

### 4. Hal's coin shop and the newsagent are placed where the built street, as ruled, has other shops (lines and draft)

- **Files and lines:**
  - production/cloud-week/lines/lines.json: `anyone.way-hals.01` to `.05` ("Hal's? Up the top, on the quiet side."; "The coin shop? Up past the newsagent's."; "Hal's. Opposite the grocer's, near the top."); `anyone.way-newsagent.04` "The paper shop's opposite the laundry."; `anyone.way-newsagent.05` "Over the road from the laundry"; `anyone.way-bus-stop.05` "Up past Hal's."
  - production/cloud-week/first-30-minutes/DRAFT.md: section 2.4 ("the newsagent with the pension counter (x 32), Hal's shop at the far end of the row (x 39)"); beat B12, where Tom walks into Hal's shop at the row's far end; beat A16 ("Rita's and Hal's shut at one").
- **What is wrong:** the built west row is a tea room (x 24 to 30), an ironmonger (x 30 to 36) and the newsagent and tobacconist (x 36 to 42), per DECISIONS of 3 October and the shop-windows target, which already lists Hal's x 39 as "INSIDE this bay". Hal's coin shop has no unit on the street as built, and the newsagent is opposite the grocer's, not the launderette. The town helper flagged this (its NOTES item 6). The lines helper and the draft did not flag it, and both use hook-cast.json's older positions as if built.
- **Breaks:** RULINGS.md, The look and the street, 3 Oct: "west_north a newsagent and tobacconist, an ironmonger, a tea room".
- **Whose:** the lines helper (unit 12) and the draft's helper (B5).
- **Exact fix, lines:**
  - Delete `anyone.way-hals.01` to `.05` until Jafar places Hal's coin shop.
  - `anyone.way-newsagent.04` → "The paper shop's opposite the grocer's."
  - `anyone.way-newsagent.05` → "The newsagent's. Over the road from the grocer's, mind the traffic."
  - `anyone.way-bus-stop.05` → "Up past the newsagent's. The bus stop's the last thing."
  - Add to lines/NOTES.md, "Where the homes disagree", item 7: "Hal's coin shop (hook-cast.json x 39) has no unit on the built street: RULINGS 3 Oct makes the west row a tea room, an ironmonger and the newsagent (x 36 to 42). Directions to Hal's are held until Jafar places it."
- **Exact fix, draft:**
  - Section 2.4: replace "the newsagent with the pension counter (x 32), Hal's shop at the far end of the row (x 39)" with "the ironmonger (x 30 to 36) and the newsagent and tobacconist with the pension counter (x 36 to 42), as ruled on 3 October; Hal's coin shop (hook-cast.json x 39) has no unit on the built street (town NOTES item 6)". Replace "the cafe opposite the parade's north half (x 24)" with "the cafe, in the tea room's unit opposite the parade's north half (x 24 to 30)".
  - B12, Status: "NOT YET: Hal's shop has no unit on the built street (RULINGS 3 October puts the newsagent there); shop insides and the bodies and cards for Hal and Grace".
  - A16, Beat: "Rita's and Hal's shut at one" → "Rita's shuts at one".

### 5. Ada's shared lines invite Tom to tea, which the approved tea design forbids (lines)

- **File and ids:** production/cloud-week/lines/lines.json:
  - `pensioner.greet-owner.08` "The new owner. You'll come to tea one day."
  - `pensioner.greet-nowak.09` "Mr Nowak. I've the kettle on, if you're passing."
  - `pensioner.greet-tommy.08` "Tommy, dear. Your tea's gone cold waiting."
- **What is wrong:** Ada speaks the shared pensioner lines (RULINGS, Street lines). Her tea is asked once, never to a stranger, and once she is stood up it is "I'll not ask again". A passing kettle invitation from her undoes the consequence route A ends on (A24).
- **Breaks:** game-design/day-three-2026-09-29.md, Ada's tea: "she does not ask a stranger in" and "I don't ask twice, mind."; RULINGS.md, 29 Sep: "The first week's nine designs in game-design/ stand as written".
- **Whose:** the lines helper (unit 12).
- **Exact fix:**
  - `pensioner.greet-owner.08` → "The new owner. I've seen you go by."
  - `pensioner.greet-nowak.09` → "Mr Nowak. You've found your feet, then."
  - `pensioner.greet-tommy.08` → "Tommy, dear. Sit a minute, if you've a minute."

### 6. Julie's and Albert's own facts contradict their approved sheets and their new schedules (town)

- **File and ids:** production/cloud-week/town/people.json:
  - `tanja.k20` "Monday: 07:00 to 18:00 the steam laundry's counter. Saturday: 07:00 to 18:00 the steam laundry's counter."
  - `fabjan.k20` "Monday: 06:00 to 17:00 the dock gate, ..."
- **What is wrong:** both facts are derived from the old hook-cast.json routines that the helper itself overrode. Julie is laid off and Albert mends nets mornings only. The talk draws on facts, so asked where she works, Julie can still say the laundry counter all day. A script comparing every "day" fact with its schedule found only these two.
- **Breaks:** RULINGS.md, 30 Sep: "The thirty regulars stand as written."; REGULARS.md row 8: "laid off from the steam laundry's presses in the summer"; its notes: "Albert mends nets mornings only."
- **Whose:** the town helper (unit 11).
- **Exact fix:**
  - `tanja.k20` → "Monday: 09:00 to 10:00 by the kiosk on Quay Street, then 10:00 to 11:00 the pavement outside the steam laundry, then 11:00 to 12:00 the newsagent's counter, where the pensions are paid. Saturday: 11:00 to 13:00 the open market. Sunday: not on the street."
  - `fabjan.k20` → "Monday: 06:00 to 12:00 the dock gate, then 17:00 to 18:00 the quay at the bottom of Quay Street. Saturday: not on the street. Sunday: not on the street."
  - In build_people.py, derive "day" facts from the final schedule (after overrides), and add a check_town.py row comparing each "day" fact with its schedule.

### 7. Old names stand in fact texts the talk draws on (town)

- **File and ids:** production/cloud-week/town/people.json:
  - `joey.k19`, `ferko.k23` and `sera.k14`: "Joey (dock hand), Ferko (night cab)"
  - `tibor.k19`: "Tibor (the customs stamp)"
- **What is wrong:** Joey, Ferko and Tibor are the old studio's names, kept only as ids. In these texts they are what Lee, Kevin, Susan and Maureen Jensen "know", so a model voicing them can say them. "Ferko (night cab)" also contradicts Kevin's own role as the day driver.
- **Breaks:** canon.md, Premise and cast: "identifiers, never what the player sees or hears."
- **Whose:** the town helper (unit 11).
- **Exact fix:**
  - `joey.k19`, `ferko.k23` and `sera.k14` → "Lee Drewery on the quay and Kevin Needham on Mickey's rank are the Widow's people on the street." The roster's "night cab" against the sheet's day driver stays NOTES item 7, for Jafar.
  - `tibor.k19` → "Susan Coverdale is the old-money machine's stamp at customs."
  - For consistency, `rita.k22` and `danny.k11` ("Rita (the back-room fence)") → "Rita Welburn fences for the new crew from her back room."

### 8. Hal and Rita pass on the row that the sample says they keep to themselves (town)

- **File and ids:** production/cloud-week/town/people.json:
  - `hal.r1`: would_pass_to ["sam", "rita"]
  - `rita.r1`: would_pass_to ["victor"]
- **What is wrong:** both carry the town-news sample's story. Their own "sure" fields say "he and Rita keep it to themselves", yet each lists people to pass it to.
- **Breaks:** game-design/town-news-sample-2026-09-29.md, The story: "Hal and Rita keep it to themselves."; RULINGS.md, 29 Sep: "The town's news: one sample stands".
- **Whose:** the town helper (unit 11).
- **Exact fix:** replace the two rumours with pooled stories each already holds.
  - `hal.r1`:
    - gist: "Mickey's has not made much since the docks went; trade has been thin."
    - truth: "true", truth_basis StreetFacts.cs line 63
    - sure: "sees it from his shop"; heard_from ["self"]; would_pass_to ["rita", "sam"]
    - based_on ["hal.k11"]; limits ["L5"]
  - `rita.r1`:
    - gist: "June, Mickey's daughter, came back for the funeral, is still in town, and wants nothing from the office."
    - truth: "true", truth_basis StreetFacts.cs line 49
    - sure: "heard it on her step in the evening"; heard_from ["joey"]; would_pass_to ["victor", "tibor"]
    - based_on ["rita.k06"]; limits []

## Narrow points, each with its exact fix

### Town (people.json unless named)

- **T1. Design notes and citations sit inside fact texts.** Replace:
  - `danny.k07` → "Heads the new crew: flashy, reckless, loud money."
  - `fixer.k08` → "Brokers between the old-money machine, the dockside syndicate and the new crew."
  - `tom.k05` → "He has never been to the Hook: a stranger to everyone there, known only as Mickey's nephew by name." (This removes "(Jafar, 2026-09-23)" from the town's knowledge.)
  - `tom.k06` → "Nobody knows his life before the Hook; nobody asks and he never tells."
  - `rita.k23` → "Rita fences for the new crew, so she never asks the police into her shop, not even for her own window."
  - `emil.k23` → "Father Walsh heard Mickey's confession for twenty years, the last year's with it."
  - `sam.k26` → "The night watchman slipped off home on his break the night of the fire and lied in his report; Darren knows it."
  - `filip.k21` → "I slipped off home on my break the night of the fire and swore in my report I had done my rounds."
  - `lena.k29` → "I have known the new owner's name from the start; I will not use it until I trust him."
  - `sam.k28` → "I have known the new owner's name from the start, as Mickey's own people do."
  - `fixer.r2`: sure "street talk and the will" → "street talk".
- **T2. One belief is marked false though canon says it is true.** `tom.b01` says the street supposes he came into "more than a cab office" and marks it false, but canon's premise gives him a half-dead outfit and a book of debts as well. Replace with "Some on the street suppose the new owner has come into money." and keep truth "false".
- **T3. Ron's fact explains why the docks went.** `rocco.k19` and Ron's `role` text → "A docker until 1989. Mickey kept him on the door and the rank." The outline keeps the dock labour scheme "underneath, never explained", and so does the helper's own limit L5.
- **T4. Ada passes on gossip she says she does not pass on.** Her answer says "The rest is street talk, and I don't gossip." Change `ada.r3`:
  - gist: "The importer's warehouse at the far end of the old warehouse row burned down last November; the paper called it arson and nobody was charged."
  - truth: "true"
  - sure: "the paper's word; she does not repeat the rest"
- **T5. Two truth labels are wrong.** Set `ellis.r1` and `aldous.r2` to truth "true". Neither carries the owner's guilt, which is the only false part.
- **T6. Alison's fact carries her schooling.** `noor.k17` → "a reporter on the local paper". This drops "grammar school", schooling REGULARS keeps out of speech for the same reason it has no teachers.
- **T7. Answers that read the casting sheet aloud.** Replace:
  - danny, "What do you do?" → deflect, uses ["danny.k08"]: "Bit of this, bit of that, mate. Always in a hurry." As written he tells a stranger he heads the new crew, against the helper's own DECISIONS line 465: plain facts, deflections and don't-knows.
  - takeaway_f, "What do you do here?" → "Front of the shop and the books. Same as last week, is it?" uses ["takeaway_f.k17", "takeaway_f.k18"].
  - ferko, "What do you do here?" → "Day shift on the rank. I know every short cut there is." uses ["ferko.k19", "ferko.k21"].
  - ellis, "Who are you?" → "DS Carol Ellis, CID."
  - emil, "Who are you?" → "Father Walsh, son. I've the parish here."
  - joey, "Who's the big man on the rank?" → "Ron Kirby. He keeps Mickey's door and the rank. I keep on his right side."
  - dario, "What do you do here?" → "I'm a ferryman. I watch the weather; it's the job."
- **T8. Father Walsh's deflection points at the confessional.** emil, "Did Mickey have any enemies?" → "I don't ask where people have been, son. I ask whether they're all right." uses ["emil.b01"]. The fire design makes the book "the only way to the truth", and the current answer ("What's said to me at my chapel stays there") points at the seal instead.
- **T9. Two sightings their routines cannot give.** `petra.r4` and `dario.r4` say each "knows him by sight from the landing", but their days at the landing end at 19:00 and 17:00 and the outfit's man is there from 22:00 (hook-cast.json). Set sure "street talk", with heard_from ["noor"] for petra and ["sam"] for dario.
- **T10. Wrong pronoun.** `takeaway_f.k21` → "keeps the takeaway on the parade with her husband".
- **T11. A garbled answer.** noor, "What do people say about me?" → "Only that Mickey's nephew has come, and Mickey left you the office. I like to hear a thing twice."
- **T12. Winifred is among the sixteen who knew Mickey, though the stated rule does not cover her.** Either add "or work at Father Walsh's chapel" to the rule in NOTES.md and DECISIONS.md line 469, or set magda knew_mickey false with the answer "I never really knew him, dear. That's all I know."
- **T13. The coin shop's and the caff's places are not settled.** Hal's coin shop and Grace's caff sit where the built row has the newsagent and the "Tea Rooms" fascia (fault 4). Keep NOTES item 6 and add "the built west row: tea room x 24 to 30, ironmonger 30 to 36, newsagent 36 to 42; Hal's has no unit" as one line for Jafar's page.

### Lines (lines.json unless named)

- **L1. Spoken street names the adopted atlas still marks "(proposal)".** Canon mints three streets. Replace:
  - `anyone.way-police-station.02` → "The station's in the Exchange, way up the hill."
  - `.05` → "Ask for the Exchange. The police station's up there."
  - `anyone.way-fairview-chapel.01` → "Fairview Chapel? A long way up the hill."
  - `anyone.way-tivoli.05` → "The Tivoli, in the Parade. Up the hill, a long way east."
  - `anyone.way-winter-rooms.01` → "The Winter Rooms? East, along the front. Gullwing."
  - `.05` → "East to the sea front. Ask for Gullwing."
  - `anyone.way-short-pier.04` → "The pier? East along the front till the land runs out."
- **L2. Later or American idiom.**
  - `driver.bumped.05` → "Steady. I've run over better. Not really."
  - `darren.crime-face.05` → "We looked right at each other. Neither of us liked it."
- **L3. Lines that assert things nobody set.**
  - `tradesman.greet-tom.02` → "Morning, Tom. Any locks giving you bother?"
  - `father_walsh.greet-tommy.08` → "Tommy, mind the damp, now."
  - `office_worker.greet-owner.07` → "The new owner. I've seen you about." At this rung they do not know his name, and canon says "The gate is knowing".
  - `pensioner.greet-stranger.05` → "I've known this street a long time, you know." Nora, Edith, Albert and Winifred do not live on it.
  - `pensioner.crime-face.08` → "Faces stay with me. Always have."
- **L4. People in a kind that does not fit them.**
  - Move `petra` (the ferry's ticket clerk) from dock_worker to office_worker; she would otherwise say "I was on the crane" and "Oilskins on".
  - Move `danica` (in work) from casual_worker to office_worker.
  - In rules.json speaker_overrides, exclude `lena` and `zlata` from `office_worker.greet-owner.04` ("Do you have a card?") and `office_worker.greet-nowak.05` ("Is the radio still crackling?").
- **L5. Ron's Tom-rung line does not read out the rung.** `ron.greet-tom.07` → "Afternoon, Tom. Tea's on, if you want it."
- **L6. Repetition.**
  - June's train comes up in 7 of her 102 lines. Replace three: `june.bumped.02` → "Watch it. I've enough on today."; `june.crime-noise.04` → "Not my business. Not any more."; `june.after-deed.07` → "I'm saying nothing. I'm not stopping."
  - The crime-face banks across all 13 kinds say nearly one thing ("I'd know that face"). This is a known shortfall; list it on the sample page.
- **L7. Darren's perm.** `darren.rain-starts.03` → "Rain. Great. My hair will never recover." His frozen face has Epic's short cut (RULINGS, 30 Sep).
- **L8. Lines that sound written, not said.**
  - `father_walsh.in-rain.05` → "Ah, the damp. It gets into the old hymn books."
  - `darren.in-rain.08` → "Rain like this, everybody's got a sudden errand indoors."
- **L9. The Tommy rule is credited to canon.** lines/NOTES.md and DECISIONS.md line 472: replace "canon keeps that rung for two or three people and names none" with "the what-they-call-him design keeps that rung for two or three people, ever, and for nobody in the first week; canon names none".
- **L10. Thirteen lines can never play.** The driver kind's 13 stranger greetings never play, because Kevin and Terry are its only members and both are floored at the owner rung. Drop them, or take them out of the clip count (about 4,687 clips stated).

### Draft (DRAFT.md)

- **D1. D2 and Q2 ask for ten more town stories now.** His ruling of 29 September says ten more wait until he meets the sample in the game, and the draft itself says town news is "never loaded".
  - Q2 (a) → "Ten more town stories of the Hal-and-Rita shape, once he has met that one in the game (his ruling of 29 September)."
  - D2 → "What fills a route with no crime, once the Hal-and-Rita story is in the game: ten more like it. Recommended: yes, then."
- **D2. Darren speaks before his day starts.** In A9 and B8 he speaks at 08:40 and 08:50 game time, but his Tuesday starts at the cafe at 09:00.
  - A9 marks → "consequence@9:30 ui:overheard-hint@9:32 ui:ledger@9:40 ui:ledger-hint@9:40 act:read"
  - B8 marks → "consequence@8:30 ui:overheard-hint@8:32 ui:ledger@8:40 ui:ledger-hint@8:40 act:read"
- **D3. Hint times disagree with FirstMoments.cs.** The Ledger's hint shows at once when the Ledger opens (AtOnce). Route B stands still five seconds (control 0:03, move 0:08) against StillFor 4 s. The ask's hint is Ron's line at the ask, which comes at eight o'clock (5:30). Fix:
  - B1: add "ui:move-hint@0:07".
  - B6: "ui:coat-hint@5:32".
  - B25: "the five hints".
  - Section 4, Hints shown: "6, the last at 9:40" and "5, the last at 8:40".
  - Section 4, the interface row: A ledger-hint 9:40; B move-hint 0:07, coat-hint 5:32, ledger-hint 8:40.
- **D4. Interface times disagree with the beats' prose.**
  - A7 shows a wait stop with no mark: add "ui:wait-stop@6:05", so A's first wait-stop is 6:05, not 23:05.
  - B19 likewise: add "ui:wait-stop@21:05".
  - The saves at 8:50 and 7:50 fall at 02:40 and 00:40 game time, neither "as the day turns" nor the "autosave each morning" of 2.7. Fix: change "the game saves as the day turns" to "the game saves in the morning" in A8 and B7; move "ui:save" to A9 "@9:00" and B8 "@8:00"; set First save to 9:00 and 8:00.
- **D5. Brenda is placed outside.** A11: "Outside the fish shop Brenda" → "At the fish counter Brenda". Her routine has her behind the counter until two.
- **D6. June greets twice in one beat, and one quote is wrong.** In A2 she says two greeting lines in one beat, against rules.json's one greeting a person in ten minutes, and the second is misquoted: june.greet-owner.02 is "So you're the new owner. I'm not stopping." Replace the second with her sheet's "I'm not stopping long. I've a life to get back to."
- **D7. Sheila did not see the window.** A17: "She saw the window" → "She heard the glass go and has heard who was about". A4 puts her in the office; the sheila-trust design counts "heard of him" too.
- **D8. Ellis's arrival rests on an unmeasured count.** A21 rests on three people passing talk of his nights by Thursday. The Ellis design's own measure needs Ron's sighting for that; here Ron tells nobody, and only Terry sees him, in the coat. Status → "NOT YET: Ellis has no body; whether three are passing it by Thursday is unmeasured (TownReach --loud on route A's sightings)".

## What is right

### Canon, held across all three pieces

- **How Mickey died** is told only as RULINGS 30 Sep has it: his heart, at the office, early one morning, found by Ron. Nobody doubts it.
- **The fire** is the street's version only. Its truth is held by Father Walsh under the seal and as Alison's secret belief; Ellis's belief is correctly false.
- **Tom's name:** no answer, rumour or fact outside his own entry uses it. Sheila never names him. The ladder is canon's.
- **The cast:** exactly 14 principals and 30 regulars, with ages, trades and districts matching canon and the sheets. The six who see him arrive are exactly the day-one design's six. The 29 new facts are small, each marked, and match DECISIONS (26 plus 3).
- **The content rule holds everywhere:** no drink or gambling, including hidden cases (the word list, the police flags, "brew", "lucky", "stay lucky" all checked); no children; tobacco only ("Got a light, mate?", "Cadge a fag?"). The laundry is "the Steam Laundry as a launderette", as DECISIONS 3 Oct has it.

### Town

- **The sixteen who knew Mickey** follow a stated, marked rule, and only they hold the two approved lines.
- **The 430 answers** all cite real fact ids, and their don't-knows are honest.
- **The 220 rumours** are honestly reconciled with the 29 September ruling under his later order of 12 October: written, not wired.

### Lines

- **The rules:** every line is under twelve words; the 45 s rule is kept; Ron, Darren, Father Walsh and June have their own lines; Sheila, Alison and Ada stay on the shared ones.
- **The filters:** the never-police filter covers Ron, Sheila, Rita, Hal, Wayne, Susan and Dennis; Nora and the Tangs get no dialect.
- **Witness lines** never accuse or claim more than the witness saw, and Mickey appears only as a place.
- **The voice:** British 1990 throughout ("nowt", "nithered", "ta-ra", "stair-rods", "dinner" at midday).

### The draft

- **Combat and danger:** no fight, death, health bar, waypoint or gun, and "Tom cannot die" is stated, as the 12 October rulings require.
- **The three proposals** are honestly marked in their beats, in section 6 and in DECISIONS. None silently changes canon: P1 adds a debt to a book canon already has, P2 is a short skippable cutscene, and P3 is the room the day-three design's "asks him in" implies. Darren's "owing" in A12 is grounded in the Core's debts (GameController.cs).
- **The numbers:** every cell of section 4 and section 3.3 equals what the tables give, recomputed here.
- **Quotes and schedules:** every quote but June's matches its home, and every person stands where their routine puts them, except D2 and D5.

## What I could not check

- **Voices, accents and tone:** I heard no voice. No accent was judged; Nora's Cork and the Tangs' Hong Kong English were not tried. Tone is the D7 judge's, and nothing here was played in the game.
- **TownReach (C#, the PC):** I could not run it, so neither the Ellis threshold in A21 nor the ambient groups' sizes are measured.
- **The AAA study's numbers:** they do not exist yet, and the draft says so.
- **1990 idiom:** read, not tested against a corpus. No list proves that a line is not a lyric or a catchphrase.
- **Positions off the built street:** whether a direction is easy to follow in the game's geometry was not walked. The atlas positions of off-street places were checked by name and district only.
- **Unit 12's walk simulation:** not re-derived beyond running its check.
