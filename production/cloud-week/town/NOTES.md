# NOTES: town content (unit 11, cloud week 42)

Written 13 October 2026 for Jafar's order of 12 October: for every principal and regular in canon, the authored facts the talk draws on, their schedule, who they talk to, five rumours, and a newcomer's ten likeliest questions answered from those facts. Third person throughout. Canon outranks all of it; anything new is marked and sits in DECISIONS.md as seven entries (the first six when the files were made, a seventh for the facts reworded after the canon review of 13 October), each ending "Marked for Jafar." Nothing here is in the game or on a page of his yet.

## What was made (production/cloud-week/town/)

- **HOMES.md**: where each kind of fact lives today, and how these files relate to each home. Written first.
- **people.json**: 44 entries (the fourteen principals, with Tom's entry holding only what the town knows of him, and the thirty regulars). Each has facts (knows, believes, saw), a schedule, who they talk to, five rumours and ten answers.
- **check_town.py** and **checks/check_v1.json**: the checks, written apart from the builder. Result today: **617 of 619 rows pass**.
- **build_people.py**, **town_lib.py**, **authored/**: the builder and the written text. `python3 build_people.py` makes people.json; `python3 check_town.py` checks it; `python3 make_notes.py` makes this file. Standard library only; the whole run takes seconds.

## The numbers

- **People:** 44 (14 principals, 30 regulars). Tom is the player: his entry is only what the town knows of him, and no answer is written for him (his words are typed).
- **Facts:** 1162 in all. Sourced or derived: 1111. New (marked): 51.
  - Of the sourced, 662 are the street's plain facts copied from StreetFacts.cs (each person holds the ones that reach them), 149 say who each tie is, in hook-cast.json's words, 44 are derived by script from hook-cast.json (a person's day, a shop's hours), and the rest are word for word from a casting sheet, the contact sheet, a card, canon, RULINGS or an approved design, each with file and line.
  - 27 facts are secrets: held, never told to a stranger. The check fails an answer that cites one, except a deflection that repeats none of its words.
  - Beliefs (48): 40 unknown, 5 true, 3 false, 0 partly, each against canon and the story.
- **Rumours:** 220, five a person. 190 are one of eleven pooled stories the street passes round (the heart, the nephew, the funeral, June, the fire as the street has it, the thin trade, the door, the man at the landing, Hal and Rita, the radio, and the arrival seen); 30 are specific to a person (listed below).
- **Answers:** 430, ten a person but Tom's. Kinds: 315 plain answers, 26 partial, 23 pointing to someone, 28 deflections, 38 honest don't-knows. Every answer is under thirty words and cites the fact ids it draws on.
- **Check:** 617 of 619 rows pass. It covers the cast (each of the 44, nobody else), every citation, every derived fact and schedule re-derived from hook-cast.json, the ties and their hours a week recomputed, the rumours' limits, each answer's facts, words and length, the gates, and DECISIONS.md. It also damages a copy of people.json 34 ways (a changed quote, a wrong line, a secret told, a real brand, drink, a year after 1992, Tom's name, the fire's truth, murder, a missing or extra person a day fact that disagrees with its schedule, and so on) and requires each to fail a row: 34 seeded faults, 34 caught.

## Where the files do not settle things (homes that disagree, for the PC session; none is settled here)

1. The old prototype cards (a pub, a bar, gambling debts, Ada a teacher, other ages and trades) still sit in Tier2Setup.cs, SecretsSetup.cs, CastSetup.cs and tier2-batch-1.json, with ids that now mean other people (the old 'vesna' is a nurse). REGULARS.md already says its sheets replace them. Nothing is drawn from them except two sentences the approved fire design itself uses.
2. Ron's years on the docks: his sheet's line says forty, his card thirty, his street lines thirty on the quay. No answer gives a number.
3. The Tangs' takeaway has no unit: REGULARS.md puts it on the parade's empty bay, RULINGS.md (3 Oct, later) rules bay 3 empty and to let. Their schedule says so.
4. Julie Kettlewell is laid off by her sheet and still at the laundry counter in hook-cast.json. Albert Suggitt mends nets 'some mornings' by his sheet and is on the docks all day in hook-cast.json. Both schedules are written afresh and say they replace the routine. Their 'where to find' facts (Julie's and Albert's k20) are derived from those proposed schedules, not from the routine they replace, and the check compares every such fact with its schedule (review fault 6).
5. Doreen Harland's early shift starts at six, before the laundry counter opens at eight. Kept as hook-cast.json has it, since a works runs before its counter; the check names the exception.
6. The trades line lists an ironmonger and a tea room on the west block; hook-cast.json has Hal's coin shop and the cafe there. For Jafar's page: the built west row is a tea room (x 24 to 30), an ironmonger (30 to 36) and the newsagent and tobacconist (36 to 42); Hal's coin shop (hook-cast.json x 39) and Grace's caff have no unit of their own on it, and the newsagent holds the pension counter (hook-cast.json x 32). Hal's trade and his facts stay as the casting sheet has them; no direction to his shop is written until Jafar places it (review fault 4, T13).
7. The empire roster makes Ferko the night cab; the sheet makes Kevin Needham the day driver and Terry Hodgson the night one. The sheet outranks; the arm Kevin belongs to is carried as a secret.
8. CASTING.md names a force for Carol Ellis; her sheet says canon names none. No force is named here. CASTING.md says Mickey was a trawlerman until the fleet went; canon does not, so it is not used.
9. Sheila's card says the fish shop is two doors up; the street's bays put it next door. No answer says which.

## Canon checks made by hand (besides the word lists the check runs)

1. Mickey's death: every fact, rumour and answer that speaks of it says only that he died of his heart at the office early one morning and that Ron found him (RULINGS 108). 125 facts, 50 rumours and 9 answers mention a death or dying; none suggests another cause, and nobody doubts it. The one other mention is Sheila's sighting 'two nights before Mickey died' (her card).
2. Tom's life before the Hook stays unsaid (canon): no fact, rumour or answer gives it; the only rumour about it says that nobody knows (canon, 28 Sep).
3. Tom's name follows the ladder (canon 88 to 91, what-they-call-him): only Ron, Sheila and Darren, who know it from the start, and Tom's own entry use it; everyone else says 'the new owner' or Mickey's nephew. Ron says 'boss'; Sheila's answers never name him.
4. Sheila withholds his name until she trusts him: no answer of hers uses it. Whether she has read the fire's page in the real book is left open (the fire design leaves it open): no fact says either.
5. The warehouse fire: the street's version only (last November, a Saturday night, started in two places, the paper's 'arson', nobody charged, the street's insurance talk). That the owner did it is marked false against the story and never corrected aloud. The truth is held only by Father Walsh, sealed; Alison's belief (marked secret, unproved) matches it and Ellis's (that someone paid the watchman) does not; no non-secret text contains it.
6. Nobody but regulars who knew Mickey describes him, and only in the two approved lines (RULINGS 101). The sixteen who may are listed below; June and Alison never do.
7. A witness is only as sure as the witness (RULINGS 113): each rumour records how sure its first teller was; none turns a guess into 'he did it'. No deed of Tom's has happened at the baseline, so none appears.
8. Mickey's is a minicab office (D19): no text calls it a pub or a bar; the pawn, the cafe, the chapel, the shops are the street's.
9. No children anywhere: nobody is in the school, which stands closed; Philip Danby is the only teacher and says so only with the school shut; Ada was never a teacher (canon).
10. No alcohol or gambling in image or speech: tools/content-gate.py is clean over every written and every carried text; no answer mentions drink or betting, and nobody's trade touches either.
11. Era: poll-tax letters, pagers, phone boxes, the evening paper, the radio; no year after 1992 anywhere in the text; no real brand, club, programme, paper, song or public figure (RealWorld.cs's lists and the Humber-side towns are scanned). Real places in carried text were avoided by choosing fragments; the one that remains is the New Territories in Peter Tang's row (his sheet's own words), and his answers say only 'I came over in 1968'.
12. Names: the old names (Lena, Rocco, Sam and the rest) appear only as ids. 'Father Walsh' and 'Father Emil' are kept apart; the heads are Agar, Jensen and Cammack.
13. The regulars stand as written (RULINGS 115): names, ages, trades and sample lines are word for word from REGULARS.md; the three changes of routine come from its own notes (laid off; mornings only; Grace and the Tangs need routines).
14. Mickey's people never go to the police about one of their own (RULINGS 111) and Rita, Hal, the pawn's back-room hand, the customs officer and the scrap dealer never go at all (the Ellis design): carried as secrets, contradicted nowhere. Each holds only the sentence about themselves: the Ellis design's paragraph naming the others is no one's fact but the designer's (review fault 1).
15. The outfit's man stays unnamed and has no entry (canon; REGULARS.md); the street's own word for him is 'a man who hangs about the ferry landing at night'.
16. The first week's designs are not contradicted: the six who see him come (Ron, Sheila, the dispatcher, a day driver, Ada, the sign painter) are exactly the six with that sighting; Sheila keeps the key; the cab office's hours are seven to three; nothing says Ada asks a stranger in.
17. Religion is present and never mocked: Father Walsh's seal is kept and Nora's and Winifred's chapel work is plain.
18. Faces, clothes and voices are untouched; no voice is cast by these files. Where a sheet says a voice does not fit (Ellis, Agar, Jensen, June, Walsh, Ada), nothing here depends on it.

## Who knew Mickey (group N-MICKEY: new, for Jafar)

Only these 16 hold the two approved lines about him ("Mickey kept his business to himself...", "Mickey kept Ron on..."): Ron Kirby (rocco); Sheila Dunn (lena); Darren Milner (sam); Ada (ada); Father Brendan Walsh (emil); Pauline Kitching (zlata); Kevin Needham (ferko); Terry Hodgson (dusan); Brenda Laverack (marla); Rita Welburn (rita); Henry "Hal" Metcalfe (hal); Nora Cronin (vesna); Winifred Duggleby (magda); Doreen Harland (zora); Edith Stockill (hana); Grace Rinaldi (cafe).
The rule used: those who worked for him (the dispatcher and the two drivers), Ron, Sheila, Darren, Ada, Father Walsh, and those over forty who keep a shop, the cafe, the laundry's floor, the pension counter or the priest's house, or work at Father Walsh's chapel, on or beside Quay Street (the chapel was added after the canon review, which found Winifred Duggleby among the sixteen with no clause that covered her; review T12). Nobody else describes him; asked what he was like, they say they never really knew him.

## Every new fact, by person, one line each (for Jafar's check)

Groups: N-LIVES is a small belief, sighting or trade fact where canon and the sheets are silent; N-RIVALS is the same for the three heads, the detective and the Fixer; N-REWORDED is a fact that was word for word from a home until the canon review of 13 October and is now worded for its person alone (no design note, no old name, no other person's secret in it). Each follows the line named after it.


**Ron Kirby** (rocco)
- rocco.k19, knows, N-REWORDED: A docker until 1989. Mickey kept him on the door and the rank. Follows: Reworded from his sheet's line 9: it names the dock labour scheme's end, which explains why the docks went, and the outline keeps that underneath, never explained (story-outline lines 20 to 22; limit L5). Review T3.
- rocco.b02, believes, N-LIVES [truth: unknown]: A stranger who stands about his rank should stand where he can be seen; Ron will wait to see what the new owner does before he thinks anything of him. Follows: From his sheet's line 'You want to stand there, son, you stand where I can see you', and the outline's 'calls him boss and watches him'.

**Sheila Dunn** (lena)
- lena.k29, knows, N-REWORDED: I have known the new owner's name from the start; I will not use it until I trust him. Follows: Reworded from the what-they-call-him design (game-design/what-they-call-him-2026-09-29.md): the line is a note about three people, in the design's voice, not what Sheila knows. Review T1.
- lena.b02, believes, N-LIVES [truth: unknown]: The new owner will show what he is by what he does, not by what he says. Follows: Follows her promise to Mickey to size up whoever inherited (talk card) and the outline's 'she promised Mickey to size him up'.

**Darren Milner** (sam)
- sam.k26, knows, N-REWORDED: The night watchman slipped off home on his break the night of the fire and lied in his report; Darren knows it. Follows: Reworded from the fire design (game-design/warehouse-fire-2026-09-29.md): the design's line is a note ('His secret is that...') written about Darren, not in his knowledge. Review T1.
- sam.k28, knows, N-REWORDED: I have known the new owner's name from the start, as Mickey's own people do. Follows: Reworded from the what-they-call-him design (game-design/what-they-call-him-2026-09-29.md): the line is a note about three people, in the design's voice, not what Darren knows. Review T1.
- sam.b02, believes, N-LIVES [truth: unknown]: The new owner will be worth being useful to, and it pays to be first. Follows: Follows 'friendly and owing' (outline) and 'trades in being useful' (talk card).

**Tom Nowak** (tom)
- tom.k05, knows, N-REWORDED: He has never been to the Hook: a stranger to everyone there, known only as Mickey's nephew by name. Follows: Reworded from canon's premise: the citation (Jafar, 2026-09-23) is a design note and must not be part of what the town knows. Review T1.
- tom.k06, knows, N-REWORDED: Nobody knows his life before the Hook; nobody asks and he never tells. Follows: Reworded from canon's premise: the citation (Jafar, 2026-09-28) and 'in the game' are design notes and must not be part of what the town knows. Review T1.
- tom.b01, believes, N-LIVES [truth: false]: Some on the street suppose the new owner has come into money. Follows: A street guess, a small hope or envy; canon's own picture is a half-dead outfit and a book of uncollectable debts, so the guess is false. Reworded after the review (T2): the earlier text said he had come into more than a cab office, which canon's premise (an outfit and a book of debts as well) makes true.
- tom.b02, believes, N-LIVES [truth: unknown]: Some on the street suppose the new owner will sell up and go. Follows: A street guess; nothing in canon or the story settles what he will do (the week's end is the player's answer).

**Ada** (ada)
- ada.b01, believes, N-LIVES [truth: unknown]: Whoever stands about the street long enough is seen, and what is seen is remembered. Follows: Follows her sheet's 'I don't gossip. I remember.'
- ada.b02, believes, N-LIVES [truth: unknown]: A man is no more than a name until he is seen to do something. Follows: Follows 'she does not ask a stranger in' (day-three design) and her window's patience.

**Father Brendan Walsh** (emil)
- emil.k23, knows, N-REWORDED: Father Walsh heard Mickey's confession for twenty years, the last year's with it. Follows: Reworded from the fire design (game-design/warehouse-fire-2026-09-29.md): the design's line is a note about his card ('Father Walsh's card changes to...'), not in his knowledge. Sealed: never said, never passed on. Review T1.
- emil.s01, saw, N-LIVES: Father Walsh took Mickey's funeral service at his chapel. Follows: The street fact puts the funeral at his chapel; a priest takes the service there.

**Alison Sedman** (noor)
- noor.s01, saw, N-LIVES: She covered the warehouse fire for the paper and walked the burned row afterwards. Follows: She 'will not drop' the story (outline); a reporter on the paper would have covered it.

**Geoffrey Agar** (aldous)
- aldous.b01, believes, N-RIVALS [truth: unknown]: The Hook's affairs are beneath a visit and reach him, if at all, as paper. Follows: Follows 'I make sure people have read the paperwork' and the outline's Act II, where his arm comes by paper (a letter, a licence, an inspection).
- aldous.s01, saw, N-RIVALS: He read of the warehouse fire in the evening paper, as the town did. Follows: The paper called it arson (fire design); an alderman reads the evening paper.

**Maureen Jensen** (sera)
- sera.k14, knows, N-REWORDED: Lee Drewery on the quay and Kevin Needham on Mickey's rank are the Widow's people on the street. Follows: Reworded from the empire roster's faction table (game-design/empire-roster.md), which names the Widow's two people by their old studio names (Joey, Ferko): canon keeps old names as ids, never what the player sees or hears. The roster's 'night cab' against the sheet's day driver stays item 7 of NOTES.md for Jafar. Review fault 7.
- sera.b01, believes, N-RIVALS [truth: unknown]: Whoever has inherited Mickey's has yet to show her what he will do; she is interested in that, not in what he is. Follows: From her sheet line 'I'm interested in what you'll do.'

**Danny Cammack** (danny)
- danny.k07, knows, N-REWORDED: Heads the new crew: flashy, reckless, loud money. Follows: Reworded from his sheet's line ('flashy and reckless (canon); loud money (CASTING.md)'): the citations inside the fact were design notes, and the talk could have read them aloud. Review T1.
- danny.k11, knows, N-REWORDED: Rita Welburn fences for the new crew from her back room. Follows: Reworded from the empire roster's faction table (game-design/empire-roster.md), whose entry reads 'Rita (the back-room fence)': the fact now holds her full name in a plain sentence, as the Widow's people do. Review fault 7, for consistency.

**Keith Garbutt** (fixer)
- fixer.k08, knows, N-REWORDED: Brokers between the old-money machine, the dockside syndicate and the new crew. Follows: Reworded from his sheet's line, which ends '(canon)', a design note the talk could have read aloud. Review T1.

**Philip Danby** (elias)
- elias.b01, believes, N-LIVES [truth: unknown]: The street is quiet enough now that anything out of the ordinary is noticed. Follows: Follows 'You notice things when you're not in a hurry' (sheet) and the street's thin trade.

**Pauline Kitching** (zlata)
- zlata.b01, believes, N-LIVES [truth: true]: Whatever goes out on the radio is heard by every car and half the street; nothing said on it is private. Follows: Canon: 'a radio nobody can help overhearing'.

**Kevin Needham** (ferko)
- ferko.k23, knows, N-REWORDED: Lee Drewery on the quay and Kevin Needham on Mickey's rank are the Widow's people on the street. Follows: Reworded from the empire roster's faction table (game-design/empire-roster.md), which names the Widow's two people by their old studio names (Joey, Ferko): canon keeps old names as ids, never what the player sees or hears. The roster's 'night cab' against the sheet's day driver stays item 7 of NOTES.md for Jafar. Review fault 7.
- ferko.b01, believes, N-LIVES [truth: unknown]: The bridge is jammed more often than not, and the way round by the market is quicker. Follows: From his line 'Traffic on the bridge again. I went round by the market.'

**Terry Hodgson** (dusan)
- dusan.b01, believes, N-LIVES [truth: unknown]: Nights on the rank are thin, and the fares that come are few. Follows: Follows the street fact that trade has been thin since the docks went.
- dusan.s01, saw, N-LIVES: He sees who comes and goes on the street after dark, from the rank, and says little of it. Follows: His routine puts him on the rank all night (hook-cast.json) and his manner is few words.

**Lee Drewery** (joey)
- joey.k19, knows, N-REWORDED: Lee Drewery on the quay and Kevin Needham on Mickey's rank are the Widow's people on the street. Follows: Reworded from the empire roster's faction table (game-design/empire-roster.md), which names the Widow's two people by their old studio names (Joey, Ferko): canon keeps old names as ids, never what the player sees or hears. The roster's 'night cab' against the sheet's day driver stays item 7 of NOTES.md for Jafar. Review fault 7.

**Rita Welburn** (rita)
- rita.k22, knows, N-REWORDED: Rita Welburn fences for the new crew from her back room. Follows: Reworded from the empire roster's faction table (game-design/empire-roster.md), whose entry reads 'Rita (the back-room fence)': the fact now holds her full name in a plain sentence, as the Widow's people do. Review fault 7, for consistency.
- rita.k23, knows, N-REWORDED: Rita fences for the new crew, so she never asks the police into her shop, not even for her own window. Follows: Reworded from the Ellis design (game-design/ellis-2026-09-29.md line 18), which carries a design note about the empire roster inside the fact. Review T1.
- rita.b01, believes, N-LIVES [truth: unknown]: What people bring over her counter is their business, and what she is told stays on her side of it. Follows: From 'looking costs you nothing' and 'never says what a thing is worth until she has to'.

**Wayne Harrison** (victor)
- victor.k19, knows, N-REWORDED: Wayne never goes to the police, whatever he sees or suffers; his trade keeps him from it. Follows: Reworded from the Ellis design (game-design/ellis-2026-09-29.md line 18), keeping only the sentence about this person: the design's paragraph names other people's arms, which this person could not know. Review fault 1.

**Henry "Hal" Metcalfe** (hal)
- hal.k21, knows, N-REWORDED: Hal never goes to the police, whatever he sees or suffers; his trade keeps him from it. Follows: Reworded from the Ellis design (game-design/ellis-2026-09-29.md line 18), keeping only the sentence about this person: the design's paragraph names other people's arms, which this person could not know. Review fault 1.

**Susan Coverdale** (tibor)
- tibor.k19, knows, N-REWORDED: Susan Coverdale is the old-money machine's stamp at customs. Follows: Reworded from the empire roster's faction table (game-design/empire-roster.md), which names her by her old studio name: canon keeps old names as ids, never what the player sees or hears. Review fault 7.
- tibor.k20, knows, N-REWORDED: Susan never goes to the police, whatever she sees or suffers; her trade keeps her from it. Follows: Reworded from the Ellis design (game-design/ellis-2026-09-29.md line 18), keeping only the sentence about this person: the design's paragraph names other people's arms, which this person could not know. Review fault 1.

**Nora Cronin** (vesna)
- vesna.b01, believes, N-LIVES [truth: unknown]: Father Walsh is not to be troubled by every caller. Follows: From the contact sheet's 'devout, dry, a quick laugh, protective of the priest'.

**Tracey Scarth** (katarina)
- katarina.b01, believes, N-LIVES [truth: unknown]: The market stall could grow into a shop of her own one day. Follows: From the contact sheet's 'chatty, ambitious'.

**Albert Suggitt** (fabjan)
- fabjan.b01, believes, N-LIVES [truth: unknown]: The old fleet was a better trade than anything the dock has now. Follows: From 'full of the old fleet' and his line; no reason is given for why the docks went.

**Gary Mawer** (tomas)
- tomas.b01, believes, N-LIVES [truth: unknown]: Boats still need mending whatever the docks are doing, so the yard stays busy. Follows: Follows his trade, 'a boat repairer at the yard'.

**Ian Megginson** (luka)
- luka.b01, believes, N-LIVES [truth: unknown]: Most of the street's locks would not stop anyone patient. Follows: From his line 'Old lock, that. Anybody with a hairpin and an hour.'

**Sylvia Rennison** (sanja)
- sanja.b01, believes, N-LIVES [truth: unknown]: A landlady who keeps her eyes open learns what her lodgers and the street are up to. Follows: From the contact sheet's 'house-proud, nosy'.

**Edith Stockill** (hana)
- hana.b01, believes, N-LIVES [truth: unknown]: Whatever goes in the post on a weekday should go by the last collection, and she will not have it missed. Follows: From her line 'It'll catch the last post.'

**Dennis Iveson** (drago)
- drago.k21, knows, N-REWORDED: Dennis never goes to the police, whatever he sees or suffers; his trade keeps him from it. Follows: Reworded from the Ellis design (game-design/ellis-2026-09-29.md line 18), keeping only the sentence about this person: the design's paragraph names other people's arms, which this person could not know. Review fault 1.
- drago.s01, saw, N-LIVES: He works on the old warehouse row and has seen the burned end of it every day since November. Follows: His yard is on the row (contact sheet) and the fire was at its far end (street fact).

**Norman Dent** (filip)
- filip.k21, knows, N-REWORDED: I slipped off home on my break the night of the fire and swore in my report I had done my rounds. Follows: Reworded from the fire design (game-design/warehouse-fire-2026-09-29.md): the design's line is a note about him ('His secret is that...') and carries the design's words, not his own. Review T1.

**Grace Rinaldi** (cafe)
- cafe.b01, believes, N-LIVES [truth: unknown]: A cup of tea sets most people right, and nobody leaves her caff hungry or cold. Follows: From her line 'Sit down before you fall down. Tea's on.' and 'warm, bossy'.

**Peter Tang** (takeaway_m)
- takeaway_m.b01, believes, N-LIVES [truth: unknown]: Good food is worth the ten minutes it takes. Follows: From his line 'Good food takes ten minutes.'

**Lily Tang** (takeaway_f)
- takeaway_f.k21, knows, N-REWORDED: keeps the takeaway on the parade with her husband Follows: Reworded from her husband's row on the contact sheet (REGULARS.md row 29: 'keeps the takeaway on the parade with his wife'): the row's pronoun is his, so it was wrong for her. Review T10.
- takeaway_f.b01, believes, N-LIVES [truth: unknown]: Regulars are remembered, and a customer who thinks she forgets is mistaken. Follows: From her line 'Same as last week? I remember. Everybody thinks I don't.'

## Schedules proposed (group N-SCHEDULES), one line each

- **Carol Ellis** (ellis), a weekday: 08:30 to 17:00 the police station, in the CID office; 17:00 to 18:00 the old warehouse row.
- **Geoffrey Agar** (aldous), a weekday: 00:00 to 09:30 his house in Fairview, on the hills; 09:30 to 13:00 his office in the Exchange, the district of offices and lawyers; 13:00 to 14:30 his table at luncheon in the Exchange; 14:30 to 17:30 his office in the Exchange, the district of offices and lawyers; 17:30 to 24:00 his house in Fairview, on the hills.
- **Maureen Jensen** (sera), a weekday: 00:00 to 06:30 her house by the docks; 06:30 to 07:30 the wholesale fish market on the fish dock; 07:30 to 09:30 her house by the docks; 09:30 to 17:30 the back room of a dockside office in the Hook; 17:30 to 24:00 her house by the docks.
- **Danny Cammack** (danny), a weekday: 00:00 to 02:00 the Parade, the nightlife district; 02:00 to 13:00 his flat above a shop in the Parade district; 13:00 to 24:00 the Parade, the nightlife district.
- **Keith Garbutt** (fixer), a weekday: 09:00 to 11:00 the room he keeps for meetings, over a shop in Copper Row; 11:00 to 12:30 his table at luncheon in the Exchange; 12:30 to 14:00 the room he keeps for meetings, over a shop in Copper Row; 14:00 to 16:00 the back room of a dockside office in the Hook; 16:00 to 17:30 the room he keeps for meetings, over a shop in Copper Row; 17:30 to 19:30 the Parade, the nightlife district.
- **Philip Danby** (elias), a weekday: 08:30 to 09:30 inside the cafe across the street from Mickey's; 09:30 to 12:00 the quay at the bottom of Quay Street; 12:00 to 13:00 by the kiosk on Quay Street; 13:00 to 16:00 the allotments by the railway; 16:00 to 18:00 the quay at the bottom of Quay Street.
- **Julie Kettlewell** (tanja) (replaces hook-cast.json's routine), a weekday: 09:00 to 10:00 by the kiosk on Quay Street; 10:00 to 11:00 the pavement outside the steam laundry; 11:00 to 12:00 the newsagent's counter, where the pensions are paid.
- **Albert Suggitt** (fabjan) (replaces hook-cast.json's routine), a weekday: 06:00 to 12:00 the dock gate; 17:00 to 18:00 the quay at the bottom of Quay Street.
- **Grace Rinaldi** (cafe), a weekday: 06:00 to 14:00 inside the cafe across the street from Mickey's; 17:00 to 22:30 inside the cafe across the street from Mickey's.
- **Peter Tang** (takeaway_m), a weekday: 10:00 to 14:00 the Tangs' takeaway on the parade (its unit not yet fixed: RULINGS.md has bay 3 empty and to let); 16:30 to 23:00 the Tangs' takeaway on the parade (its unit not yet fixed: RULINGS.md has bay 3 empty and to let).
- **Lily Tang** (takeaway_f), a weekday: 11:00 to 14:00 the Tangs' takeaway on the parade (its unit not yet fixed: RULINGS.md has bay 3 empty and to let); 16:30 to 23:00 the Tangs' takeaway on the parade (its unit not yet fixed: RULINGS.md has bay 3 empty and to let).

Places added that hook-cast.json lacks (all off Quay Street or unplaced): exchange_office: his office in the Exchange, the district of offices and lawyers; exchange_lunch: his table at luncheon in the Exchange; fairview_house: his house in Fairview, on the hills; dock_room: the back room of a dockside office in the Hook; jensen_house: her house by the docks; parade_district: the Parade, the nightlife district; danny_flat: his flat above a shop in the Parade district; station: the police station, in the CID office; garbutt_room: the room he keeps for meetings, over a shop in Copper Row; takeaway: the Tangs' takeaway on the parade (its unit not yet fixed: RULINGS.md has bay 3 empty and to let).

## Rumours specific to a person (group N-RUMOURS)

The eleven pooled stories, each a rewording of facts every holder has, with its truth against canon and the story: the heart (true); the nephew has come (true); he missed the funeral (true); June is still in town (true); the fire as the street has it (partly: the paper's arson and 'nobody charged' stand, the owner's guilt is false against the story); trade is thin (true); the door and the key (true); a man at the landing (true); Hal and Rita had words (unknown, nobody can say why); the radio is overheard (true, canon); the arrival seen (true). The 30 specific ones:

- Ron Kirby (rocco.r2), true: Mickey's nephew came to Mickey's with his case; the new owner, with a letter.
- Ron Kirby (rocco.r4), true: The street has been dead since the docks went, and nobody has the money for a cab.
- Sheila Dunn (lena.r2), true: Mickey's nephew has come, with one suitcase and a letter; Sheila showed the new management round.
- Sheila Dunn (lena.r3), true: Mickey's has not made much since the docks went; the takings are thin and the phone rings more than it used to, and it is rarely good news.
- Tom Nowak (tom.r3), true: Mickey's nephew has come and nobody knows where from: he has said nothing of his life before the Hook, and nobody has asked.
- Tom Nowak (tom.r4), false: Some say the new owner has come into money. The takings say otherwise.
- Tom Nowak (tom.r5), unknown: Some say the new owner will sell up and go.
- Ada (ada.r3), true: The importer's warehouse at the far end of the old warehouse row burned down last November; the paper called it arson and nobody was charged.
- June Suddaby (june.r5), true: June, Mickey's daughter, is still in town and wants nothing from the office.
- Carol Ellis (ellis.r1), true: The importer's warehouse at the far end of the old warehouse row burned down last November; it started in two places and nobody was charged.
- Carol Ellis (ellis.r2), true: The fire's file was marked undetected, and the sergeant on it keeps asking.
- Carol Ellis (ellis.r3), true: The watchman's times on the night of the fire do not fit the brigade's.
- Geoffrey Agar (aldous.r2), true: The importer's warehouse at the far end of the old warehouse row burned down last November; the paper called it arson and nobody was charged.
- Geoffrey Agar (aldous.r4), true: Mickey died three weeks before his nephew came to Quay Street.
- Geoffrey Agar (aldous.r5), true: Mickey's, the minicab office, is on Quay Street in the Hook.
- Maureen Jensen (sera.r4), true: Mickey died three weeks before his nephew came to Quay Street.
- Maureen Jensen (sera.r5), true: Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside.
- Danny Cammack (danny.r4), true: Mickey died three weeks before his nephew came to Quay Street.
- Danny Cammack (danny.r5), true: Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside.
- Keith Garbutt (fixer.r5), true: Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside.
- Kevin Needham (ferko.r4), unknown: Traffic on the bridge is bad again; it is quicker round by the market.
- Brenda Laverack (marla.r5), unknown: Haddock is dear this week and it is not even good haddock.
- Lee Drewery (joey.r5), true: Casual work on the quay is scarce: Lee takes a day when there is any, and mostly there isn't.
- Susan Coverdale (tibor.r4), true: The quay has never been so quiet, not in all Susan's time.
- Doreen Harland (zora.r5), true: A laundress at the steam laundry, laid off from the presses in the summer, is looking for anything.
- Julie Kettlewell (tanja.r1), true: A laundress laid off from the steam laundry's presses in the summer is looking for anything.
- Colin Mastin (stipe.r4), true: Half the berths on the docks are empty.
- Ian Megginson (luka.r5), unknown: Most of the street's locks would not stop a patient man.
- Gordon Leckenby (dario.r5), unknown: The wind is getting up and she will be lively on the crossing.
- Norman Dent (filip.r1), partly: Nothing moves on the old warehouse row at night but the watchman and the rats.

## What canon and the story left open, and was not filled

- Mickey's past (a pub and a trawler both appear in older text; canon says neither) and what Mickey was like beyond the two approved lines.
- Who Mickey's solicitor was, who drew the will, and who the doctor was; who attended the funeral beyond June and Father Walsh.
- Where Tom grew up and what he did; why his family left; whether June knows him as a cousin.
- What is in the outfit's envelope, who the outfit's man is, and what the outfit is beyond 'Mickey's arrangement'.
- What Hal and Rita's row was about (nobody can say, by design); why Hal's shop sells no coins.
- Whether Sheila has read the real book's page about the fire; who the stranger was that Ron argued with in the yard two nights before Mickey died (her sighting; Ron's own account is not written).
- When the scrap dealer stripped the fittings (the fire design's reviewer asked for 'after the police let it go'); who lost a shed to the fire; the importer's name.
- Why the docks went (the outline keeps it underneath, never explained): Colin's and Albert's lines are kept as their own feeling, not a reason.
- Which police force Ellis belongs to; the local paper's name; the Tangs' unit; Ron's years on the docks.
- How the three heads, the Fixer and Ellis stand to each other at the baseline beyond canon's one line (each is Act II's).
- Feelings between people beyond the tie's weight: no home has any, so only the band is given.
- Whether the street holds more of the cast's secrets (the roster's arms are carried as secrets for the five it names).

## How the PC session would adopt these files (each kind to its home)

- **Who they are, schedules, ties:** stay in the casting sheets, REGULARS.md and hook-cast.json. To adopt: append the ten proposed routines (and the places they use) to hook-cast.json and replace Julie's and Albert's two; people.json's derived fields then match it, and check_town.py fails the build if they drift.
- **The street's plain facts:** stay in StreetFacts.cs. To adopt: add each person's list of the ids they hold (the `street` lists in authored/) as the table StreetFacts.For reads, replacing 'everyone holds everything'; the two Mickey lines then go only to the sixteen.
- **What each person knows, believes and saw:** a proposal with no home. To adopt: one authored facts file per person beside the casting sheets (id, text, source or 'new', secret), read by the same code that reads the cards' Hard Facts; the secret ones never reach the plain-fallback path (TalkLadder already refuses a card's own secrets).
- **Rumours:** town-news.json and Core/TownNews.cs hold one sample story; RULINGS 29 Sep says ten more wait until he meets it in the game. Jafar's order of 12 October asks for five a person, so these are written, not wired: adopt a few at a time, after he has heard the sample, each with its limits.
- **Newcomer answers:** the ten a person are written answers for the fresh-question bench: each lists its facts, so the PC session can score the live talk against them (answer, partial, don't-know) and use the don't-knows as the honest 'that's all I know' cases. They are not new lines for the game.
- **DECISIONS and approvals:** the seven entries are for Jafar's page; nothing here has an approval file, and CATALOGUE.md needs a line for production/cloud-week/town when the session takes it.

## Limits of the check

- The word lists are a screen, not a reader: they find the words in the lists and the capitalised names and numbers an answer adds, not an invented detail in lower case, a wrong idiom or a flat voice. The answers were read by hand once for added claims; the places they add anything are in the fact ids each lists.
- Tone (canon's judge is D7) and British 1990 speech were written to the street-lines note and read, not tested; no accent or voice was tried.
- No live model was called and no API money spent; nothing was run in the game.

