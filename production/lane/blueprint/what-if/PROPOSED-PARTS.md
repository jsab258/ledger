# Proposed answers for the top gaps (what-if sweep, 24 Nov 2026)

Each part answers one or more of the worst gaps in QUESTIONS.csv (ids in brackets), in the blueprint's form, for the keeper to fold in. Decided by this session within canon and his rulings and recorded in SUMMARY.md's decisions list; he overturns any. The long heat, RT2-02, the women officers and Ellis rule and the weapon gaps are in LONG-HEAT.md. Working values are marked; all are to be measured in the loops.

## P01 Frank strikes his own people (Q088, Q092, Q096, reviewer R01)

- How it works: Nothing refuses the input (RT-09). Ron, struck, does not hit back the first time: he steps back, says one hard line, and his loyalty falls a band; struck a second time he hits back once (he is old muscle) and leaves the office for three game days, then returns to the door if Frank calls at his house; a third time he leaves the firm for good and his asks come by the outfit's man (RT2-05); the story's loss (Ron going inside unless Frank pays, canon's frame) still fires, from outside the firm: Ron is taken all the same and still asks Frank's help through Sheila or the solicitor. Sheila, struck once, leaves at once and comes back only as RT2-06 already says (Frank calls at her house after a quiet week) and only once; struck again, she is gone for good, with the books' fallback in P02. Pauline, struck, leaves as RT2-06's unpaid-wages rule (fares by the office phone only until she is paid and asked back). A driver struck quits that night unless his nerve is low, when he stays and his loyalty falls two bands; robbing a driver of his half is the same as not paying him (2.15.1). Mickey's people never go to the police about it (ruling of 1 Oct), but the street hears from them within a day, and the regulars' regard for Frank falls a band.
- Standard: Every first blow on his own people has a felt, stated cost and a way back; the third is final; Mickey's people never report it. Test: S: one, two and three strikes on Ron, Sheila, Pauline and a driver; who leaves, who returns, what the street says.
- Source: RT-09; RT2-05; RT2-06; ruling of 1 Oct. Status: proposed.

## P02 Fallbacks for everyone the dropped line once shielded (Q003, Q069, Q089, Q120, Q123, Q124, Q178, Q195, reviewer R03, R11)

- How it works: The line is gone (his ruling of 24 Nov), so each person it shielded gets a fallback by role, as RT2-05 already does for the rest. Sheila: the count and the wash pass to Pauline at half the wash and with one week in four put off by mistake; Sheila's place in the ending's friends is empty, read as Frank's doing if he did it. Pauline: the board and radio pass to Kevin's sister-in-law, hired from the counter at the same wage, slower to pass fares (a fare in four missed). Ada: her tea-and-talk witness role (on Frank's side) is simply lost; the parade's watching passes to the next neighbour by routine. June: the envelope and Mickey's family thread pass to Father Walsh, who holds Mickey's letter. Alison: the paper's side of the fire thread passes to a staff reporter at the Pilot with no friendship, and the fire thread runs on through Ellis (RT2-05's Iveson rule). Ellis: Detective Inspector Hebden (LH-13). The Widow: her lieutenant takes her ladder at the same rung, as for the other heads. Father Walsh: a supply priest from Fairview holds the parish and the remand visits; Mickey's letter, if June is gone too, goes to the solicitor's office. The retired doctor: stitching only at the hospital, where a knife wound in casualty is noticed and a nurse is a witness (2.18). Anyone of sixty or over: as the person's role. A second death in a chain (a deputy's deputy, a lieutenant's successor) falls to the role's generic holder (a hired hand, a new man from out of town) named from cast.json, and nothing the story needs ever waits on a named person (RT2-05's last sentence, now rechecked for these). The data still shields some of them and must be corrected: can_die false on Sheila, Pauline, Ada, June, Alison, Ellis, Agar, the Widow, Father Walsh, the retired doctor and several shopkeepers in data/people/; "never Sheila, Pauline, Ada, June, Alison, Ellis, the Widow, Father Walsh or anyone 60 or over" in the send jobs; "tom_never_lays_hands_on" in police.json; Ellis's "cannot be bought".
- Standard: Act II's beats, the sit-down, Act III and the endings never wait on one killable person, two deep. Test: B: each named person killed in turn at Act I's end and again at Act II's start, with the first fallback killed too; the story bot reaches an ending every time.
- Source: his ruling of 24 Nov (Q3, line dropped); RT2-05; C-285; batch answerers' data findings (24 Nov). Status: proposed; the generic holders are named by the keeper from cast.json.

## P03 What is taken at an arrest, and the solicitor (Q045, Q046, reviewer R16)

- How it works: At an arrest the custody sergeant books his property: paper money and coins are listed and handed back on release, except a sum held as evidence (below), returned in a week unless it joins a charge; a weapon, stolen goods and anything that is evidence are kept; the envelope is kept if it holds what a search would call evidence (the night's fare copy, cash in a sum he cannot account for: kept until he shows it is the firm's, a game week, then returned unless it joins a charge) and its loss is a debt to the landing men only if it is never returned. The duty solicitor is free (2.6.4) and, under legal aid, represents him at any committal; the economy's brief out of cash (the conflict found by the reviewer) is a paid solicitor of his own at forty pounds a visit (a working value, to check against 1990 rates), who cuts the hours of any holding by a quarter and asks for the witnesses' attendance with more weight (one weak witness in a committal, his choice, counts at half).
- Standard: An arrest takes no money except a sum held as evidence, returned in a week unless it joins a charge; the envelope's fate follows what it holds; the free and paid solicitors differ in one stated way. Test: S: arrests carrying cash, a weapon, the envelope with the copy, the envelope with only fare money; property logged on release.
- Source: 2.6.4; reviewer R16 (the duty solicitor free against the economy's charged brief). Status: proposed; ten pounds and a quarter are working values; 1990 custody property practice to be confirmed (PACE Code C on property).

## P04 The firm while Frank is held (Q047, Q093)

- How it works: Under 24 game hours held, the firm runs by its floor without him (2.15, RT2-06): Pauline dispatches, the drivers drive, rent and wages fall due as normal, and a job or story appointment inside the hold is missed and settles by the clock as any missed appointment (windows, not minutes). A driver arrested or frightened while carrying something for Frank: goods or the envelope are kept as P03; the driver's nerve decides whether he names Frank (a statement only if he saw the deed; otherwise a lead to Ellis, a talk entry); a body in his boot is a killing found, and the driver is a knower with his nerve; Frank learns it from Pauline's radio within the game hour.
- Standard: Every hold has a stated effect on the firm and the jobs; a crewman's arrest traces to Frank only through what the crewman perceived. Test: S: a 22-hour hold across a night job and an appointment; a driver stopped with goods, the envelope and a body.
- Source: 2.15; RT2-06; RT2-17; FF-05. Status: proposed.

## P05 Mugging and shoplifting (Q101, Q118)

- How it works: Beating a man and searching him for his money (1.6.2, a man down can be searched) is a robbery at any rung: 12 hours if arrested, Ellis up one stage, the man a witness at face distance. A threat with a weapon to make a man hand over (a hold-up of a person) keeps 1.6.15's gate: before it opens, the man refuses or runs, as the shopkeeper does in P12, and it is reported as an assault with a weapon; Frank gets nothing. Shops in 1990 Quay Street keep most stock behind the counter (newsagent, tobacconist, chandler) or under the keeper's eye (grocer, ironmonger); taking from a shelf is a lift (1.6.13) with the keeper as the person who may feel it, by the same fixed limits; felt, he says so to Frank's face, will not serve him for a game week and tells his own people; unfelt, the loss is found at closing and suspected of whoever he noticed. Stock taken is hot goods (1.6.3).
- Standard: A beating and search for money is a robbery at any rung; a weapon hold-up of a person keeps 1.6.15's gate; a shelf lift follows the lift rule with the keeper watching. Test: S: a mugging in Act I logged as robbery; a shelf lift in good light with the keeper attentive is felt.
- Source: 1.6.13; 1.6.15; 1.6.3. Status: proposed.

## P06 Turning a rival's man, paying one to inform, playing rivals off (Q076, Q077, Q080, reviewer R13; his story ruling of 24 Nov names "rivals fought or played off, rivals' men recruited")

- How it works: Each rival's three men and lieutenant are named people with temper (data/people). Paying one to inform: from rung 2, a man whose greed is high and loyalty to his head below the middle takes thirty pounds a week to tell Frank one true thing a week from what his head's people hold (a read like Garbutt's, narrower); his head learns of it when any of his other men sees the two together (a sighting like any other), and then the man is beaten and gone from the Hook, and his head climbs a rung. Recruiting: from rung 3, a man whose loyalty to his head is below a third, or whose head lost a sit-down, or who was beaten by his own side, can be asked in talk; if his temper takes it, he comes to Frank's crew with his nerve and one hook on his old head (what he knew); his old head climbs a rung and points his next pressure at him. Playing off: a lie carried to one head about another (a deed blamed, a threat invented) is believed only if it fits what his own people hold and the liar's regard is high enough; believed, it is a deed against the other head in his eyes (his ladder rises against them, not Frank); found false later (a man of the other side tells him), Frank's regard with him falls two bands and the lie becomes a hook against Frank. All of it is decided by the Core from held facts; the talk model only classifies what Frank said.
- Standard: Every turn, tip and lie traces to held facts and named tempers; each has a stated discovery and its cost. Test: B: seeded attempts with men of known tempers; who turns, who is found out, how each ladder moves.
- Source: his story ruling of 24 Nov; RT-07; 2.10; C-342. Status: proposed; thirty pounds and the thresholds are working values; the story lane's terms for Danny's own offer (Q085, reviewer R12) stay with the story lane.

## P07 A witness after she has signed (Q105, Q106, Q107, Q108)

- How it works: A signed statement stays on file. She can take it back by going to the station and saying she was mistaken, which she does if she is talked round or paid and her temper allows it (the same pull as LH-04, reversed); the police then hold it at no weight, but she remembers and still tells her sister. Frightened into staying away, her statement can still be read (LH-09), and the threat adds to the case. Paid once, she may come back: a witness whose greed is high asks again a game week later (half the first sum); refusing makes her pull toward the police rise. Killing a witness is a second killing (LH-04); her statement, if already signed, is read anyway, as a dead witness's statement could be.
- Standard: Every way to undo a statement has a stated weight and a lasting memory (MEM-09). Test: S: a signed witness talked round, paid, frightened and killed in four runs; the statement's weight logged.
- Source: 2.6.3; MEM-09; CJA 1988 s.23 (LONG-HEAT sources). Status: proposed.

## P08 Talking to a constable: threats, lies, a second bribe (Q019, Q020, Q033)

- How it works: A threat to a constable is a deed he witnessed (threatening behaviour): an honest constable arrests on the spot (2 hours and a caution, a charge the second time, like a refused stop); a bought one ends the arrangement. A lie at a challenge is checked only against what that constable holds (his own sightings, a description that is hot, a noted plate): caught, his next challenge is on cause and Ellis hears it as talk; not caught, nothing. A bribe offered to an honest constable is a crime he saw (2.6.2); a second note to Garton after his one look-away is refused, and a third reported.
- Standard: A constable judges talk only against what he holds. Test: S: threats, lies and bribes to an honest and a bought constable; outcomes logged.
- Source: 2.6.2; 2.6.8; FF-05. Status: proposed.

## P09 Walls, doors and a sleeping house (Q143, Q144, Q198)

- How it works: A shut door or a wall halves the reach of any sound (2.2.4), a closed window halves it again from inside; a fight or a shot indoors is heard in the next rooms and next door, and on the street only within half reach. Sleepers wake to a sound at their room over a fixed loudness (a forced door, a drawer slammed, a shot in the house; never a careful step), get up, and act as an owner who finds a stranger (1.6.1's warning, warning again, then shout or ring). A household asleep is known from dark windows after 23:00; a dog in a yard is a sound that wakes.
- Standard: Sound through walls and sleepers' waking follow fixed loudness rules, never a roll. Test: S: indoor fight heard map; a break-in with careful and loud acts in a sleeping house.
- Source: checklist A28.06 (listed gap); 2.2.4; 1.6.1. Status: proposed; the half and the waking loudness are working values.

## P10 Hiding indoors during a chase (Q055)

- How it works: A foot pursuer follows Frank through any open door he saw him use; a door Frank shuts and the pursuer did not see shut is not searched (new rule: the lost-chase search of DP5-C03 walks streets for 30 to 120 s and does not try doors); a shop he runs into is a place full of witnesses, and the keeper tells the constable. Hiding in a yard or a lane's dark corner works by breaking sight (1.1.5), and the search's lamp finds him only if it lights him.
- Standard: Indoors is searched only where the pursuer saw him go or the search's reach passes. Test: S: chases ending through a seen door, an unseen door, and into a shop.
- Source: 1.1.5; DP5-C03. Status: proposed.

## P11 The hospital (Q190, Q191)

- How it works: The hospital is a soft-edge place: a visit is a short talk scene during visiting hours (afternoons and evenings), with the patient Frank chooses among those he knows to be there; a man Frank put there can be visited (to apologise, to frighten, to pay), and the ward sister and other patients are witnesses at face distance. Violence in a hospital is a deed like any other, seen by many, with the police called at once; nothing in the hospital is walked.
- Standard: The hospital is reachable as a scene, never a dead end. Test: S: visit a patient Frank hurt; a threat there is witnessed.
- Source: 2.18. Status: proposed.

## P12 Trying a crime before it is allowed, and the bank (Q097, reviewer R15, R17)

- How it works: When a player draws a weapon at a counter before the hold-up gate opens (Act I, under rung 2), it is a threat with a weapon, not a hold-up (LH-14b): the keeper's temper decides: most step back from the till and shout, one with nerve reaches for the phone under the counter; the till is never handed over, Frank gets nothing, and it is reported as an assault with a weapon (8 hours if arrested). The reason is the town's, never a refusal on screen: shopkeepers do not yet know or fear him. The bank sits in the Exchange (soft edge, not walked), its camera the town's only CCTV; it cannot be robbed in the release (out of scope, recorded; a bank job would need the map to grow).
- Standard: No input is refused on screen; an early attempt has a real outcome. Test: S: weapon drawn at the grocer's counter in hour one; outcome logged.
- Source: 1.6.15; canon (CCTV at the bank); RT-09. Status: proposed; the bank out of scope is a scope decision he may overturn.

## P13 The truce against deeds (reviewer R24)

- How it works: Garbutt's truce holds the rival's own moves at his rung for two game weeks; a deed by Frank against that rival during the truce breaks it: the rival climbs a rung as normal, the truce ends at once, and Garbutt keeps the money and remembers it (the truce is offered once a game, 2.10.4, so it is simply spent, and his reads cost half again for a game week). A deed against another rival does not break it.
- Standard: A truce holds only while Frank keeps it. Test: S: a deed against the truce rival on day 3; the truce ends and the rung rises.
- Source: 2.10.4; RT2-07. Status: proposed.

## P14 A dismissed man's grudge (Q091, reviewer R25)

- How it works: A crewman or driver sent away keeps what he knows (his memory is permanent): if his loyalty was low when he went, he may sell it to the rival whose eyes are nearest (one hook against Frank), or, with his nerve broken, tell Ellis what he saw first-hand (a statement only for deeds he witnessed). A man sent away fairly (paid up, with a word) holds unless he is leaned on. Ron and Sheila cannot be dismissed in Act I (new rule: the arrangement needs them, 2.9); after it, sending either away is P01's third-strike state without the blow.
- Standard: Every dismissed man keeps what he knows; what he does with it follows his temper and how he was let go. Test: B: dismissals at high and low loyalty; hooks and statements logged.
- Source: 2.11.3; RT-07; MEM-09. Status: proposed.

## P15 Beaten again and again (Q184)

- How it works: Each beating costs as 1.3.9 says. A third beating within a game week brings someone in: Ron comes to fetch him from the pavement or the hospital and says plainly what the streets are saying, and the men who beat him (named) are known in the Ledger; the robbers rob only what he carries (RT2-13), so a run of beatings cannot strip the office or the tin. No loop is closed: running, backing off and staying in are always open.
- Standard: Repeated defeat never strips the floor and always names who did it. Test: B: a bot beaten seven nights running keeps the office, car two and the tin.
- Source: 1.3.9; RT2-13; RT2-06. Status: proposed.

## P16 Love interests (reviewer R30)

- Note for the story lane, not a part: canon names Alison Sedman and Philip Danby as love interests; the blueprint designs only a friendship that holds. The story lane's cards owe the love-interest thread within canon's content rule (no sexual content; seaside-postcard innuendo allowed), and what a lesser crime learned does to it.
