# LEDGER: cast changes for the people data

Written 24 November 2026 by the story lane, for the people-data builders; revised the same day after the fresh reviews. It sets CAST.md (paper/CAST.md) against the earlier frame (working/STORY-FRAME-v2-before-paper.md) and the people data (blueprint/data/people/, 119 files, with ties.json and cast.json). Each line is one fact or one job, with its source in brackets: a scene number, a card id (S for the spine, D for the side stories), a frame section, or a data file. Where an approved casting sheet and a scene disagree on age, look or name, the sheet wins and the scene owes the fix.

The story uses 55 files: 54 named people (6 core, 29 supporting, 19 named residents) and old_firm_man, who is never named. Mickey is a 56th person and has no file yet. 64 of the 119 files are not used.

## Where each change is made

The files in people/, cast.json and ties.json are generated. A hand edit is lost at the next build. All paths below are under blueprint/data/.

- Facts about a person: tools/wave2/cast_src.py (the add(...) line: n name, a age, r role, die, fb fallback, card text) and tools/wave2/people_fix.py (FIELDS, applied after cast_src; it carries a, fb, k, r, card and card_replace).
- Who can die: tools/wave2/build_people.py, where the cover rule sets die false for women, anyone of 60 or over and Father Walsh. people_fix.py holds the rule's text (COVER_RULE).
- Ties: tools/wave2/build_ties.py (the FRAME list of pairs and strengths), people_fix.py (EXTRA_TIES for new pairs, BY_MESSAGE for pairs that never meet in a routine). build_ties.py drops any tie of 0.5 or under that neither meets in a routine nor has a BY_MESSAGE text, so every new tie below gives both.
- Notes and counts in cast.json: tools/wave2/build_cast.py. cast.json holds its own copy of each name, age and kind, so it must be rebuilt, not edited.
- Then run build_people.py, build_cast.py, build_ties.py and check_wave2.py, and read DATA-BUILD-STATUS.md's table again.

## Renamed

- R1. The lead is Frank Nowak, not Tom. frank_nowak.json already says so (never_called Tom, Tommy). Its internal cast_id "tom" and home id "toms_flat" may stay; the brief allows it. Tidy-up only. [PAPER-BRIEF section 1; frame section 1]
- R2. The name ladder is the new owner, Nowak, Frank, Frankie. cast.json name_ladder already holds it: no change. [frame section 1]
- R3. Lines files use greeting.frank and greeting.frankie, not tom and tommy. lines/README.md says this is done: check, no change expected. [lines/README.md]
- R4. Frank Stathers, not Vic. Undo the rename: in cast_src.py change n="Vic Stathers" (line 442) to "Frank Stathers", and rewrite its src text (line 449). Delete the note in build_cast.py (line 46) and the open point in cast.json. Rebuild, then grep Vic under blueprint/data: lines/own-stathers.json (line 11), routines.json (the stathers src, line 3197) and DATA-BUILD-STATUS.md (line 26) must lose it. The id "stathers" stays. His line is "There's one Frank on this gate." [scene 8; frame section 9]
- R5. His role word is "the Widow's man at the gate", not "lieutenant". Change r= in cast_src.py (stathers) and the card's rivals line. [frame section 4]
- R6. The Man in Black has no name in the story. cyril_pashby.json keeps the invented name in the file only; no line may say it. No change. [frame section 4]
- R7. Hal Metcalfe: the approved sheet names him Henry "Hal" Metcalfe, and the file already says Henry Metcalfe, called Hal. Keep the sheet's name. No change. [REGULARS #9]
- R8. The lead's name is still Tom in CASTING.md (the row "Tom Nowak"), the sheet folder tom-nowak and REGULARS.md ("clean shave (Tom)"). A name-only fix is owed by the casting files; whether it lapses the approval is the builder's call. [tools/approvals.py]

## Added

- A1. Mickey Suddaby needs a file: id mickey_suddaby, name Michael Suddaby, called Mickey, age 66, kind principal, layer 2, can_die false, no street lines, a framed photograph (flat cap, moustache). Born 1924, died 1990, a trawlerman then the cab office. Give him the same routine marker as the lead (rt "lead") so build_ties.py skips his routine. [CASTING.md; cast_src.py add; build_ties.py SL line]
- A2. Roles with no file go in a new "roles" block in cast.json (written by build_cast.py): one row per unnamed role in CAST.md's table, with the scene or card, any spoken line and a likely holder (a file id, or none). PAPER-BRIEF section 1 item 5 says to name no residents beyond those written, so no new people files. [PAPER-BRIEF.md]
- A3. Roles that speak, for the roles block: the three packers (youngest, middle, eldest; scene 8); the man on the gate ("I'm stood here while you say different, Mr Nowak"; scene 21); the remand officer ("Time."; scene 18); the test-centre woman (scene 18); the man at the landing who says "Cammack's?" (scene 23); the custody sergeant (scene 14); the one who shows the wooden grip (scene 10).
- A4. Roles that do not speak: the duty solicitor (offered in scene 13), Stathers's two gate men, the Harbour Board men, Ozols's boat-hand, Danny's lodger, the lorry driver, the milk-float driver, the deck hand, Frank's own men (first man, most loyal man, successor, crewmen), and the stranger with the suitcase (S61 only).
- A5. The Widow's men on the stage are a role. steve_brannigan is the likely holder; Billany is the named one. [scene 10; X3]
- A6. Peter Tang is named in full in scene 15 and is on file. Grace needs a tie to him (T below). [scene 15]
- A7. The old firm's man is buried on Monday 26 November, game week 7, the day of Grace's tea. Add the field "dies": {"on": "1990-11-26", "how": "natural, off screen, scripted"} to old_firm_man (add "dies" to the keys build_people.py copies from FIELDS). After it, the man at the landing in scene 23 is another man: a role (A3), not this file. [scenes 17, 23; S46]
- A8. Layer field. Add "layer" (1, 2 or 3) to every file, in cast_src.py's add and build_people.py: 1 for the six, 2 for the 29 and Mickey, 3 for everybody else. [CAST.md]
- A9. Items owed to be written: Philip Danby and PC Trevor Garton have no line in any source. Each needs one line from the story lane before the lines build. [CAST.md]

## Cut or not used by the story

The other 64 files are not named in the frame, cards or scenes. Every one may stay as a resident. Some hold role lines but have no name in the story (the sergeant's three goes at Nowak; "I'll need the bag, madam"). By group:

- X1. Two regulars with no part (2): Edith Stockill, Susan Coverdale. Their old threads ("sign there dear", the quiet quay) are kept on file in the frame.
- X2. Six people the regulars sheet folds into the crowd tier (6): Pat Stainton, Irene Lowther, Stanley Hirst, Mandy Calvert, Leslie Cotterill, Kieran Rourke.
- X3. Eighteen who could fill an unnamed role (18): Roy Bellwood (the custody sergeant); Malcolm Ruddock (Tharratt's deputy); Leonard Askew (the landlord's man); Jason Pinder, Shane Boddy, Wes Akers (Danny's young men); Eddie Birtwhistle and Dougie Saltmarsh (the fish-dock porter and the Widow's man); Victor Tasker (the laundry's owner); Phil Rawling (the glazier); Barry Coult, Kenny Varley, Ray Spink (Agar's men from away); Steve Brannigan (the Widow's man at the van, likely holder of the men on the stage); Stuart Ackrill, Brian Haigh, Martin Ibbotson (beat constables); Anthony Raine (the brief at the station on the night between, if one is named; see C13).
- X4. Ten people whose threads the revision dropped (10): Jimmy Raw, Ken Swales, Alf Garside, Douglas Fenwick, Rodney Usher, Stan Pickles, Sid Bulmer, Margaret Lofthouse, Clive Ackroyd, Bernard Gill.
- X5. Twenty-eight town and fare people the data added for the town itself (28): Ahmed Rashid, Aidan Keogh, Arthur Brigham, Beryl Wood, Bill Huxtable, Walter Dobson, Dorothy Kirkup, Edna Coulson, Eileen Crabtree, Ernest Shillito, George Cammidge, Gerald Thwaite, Harold Stead, Harry Holt, Janet Lumb, Joe Cairns, Joyce Ellerby, Kathleen Moran, Maggie Firth, Neville Kaye, Herbert Peart, Sandra Newbould, Tadeusz Wrona, Ted Tindall, Terence Bould, Tony Marsden, Vince Lazenby, Wilf Hardcastle.
- X6. The totals: 2 + 6 + 18 + 10 + 28 = 64.
- X7. The frame's cast list (section 4) shrank from 19 items to 8. No longer listed there: Lee Drewery, Julie Kettlewell, Dennis Iveson, Brenda Laverack, Rita Welburn, Grace Rinaldi, Norman Dent, Ozols (all stay layer 2, now in their cards), and Wayne Harrison, Ian Megginson, Shaun Hewson (all move to layer 3, see C25). Darren and Ada are still in item 6. [frame section 4]

## Changed

### Facts the generator must now say

- C1. Ron lives on every path, so can_die goes from true to false. In build_people.py add ron_kirby to the covered set (line 22, beside Father Walsh), reword his fb into fb_note, and add Ron to COVER_RULE's text in people_fix.py. A rival's harm to him stops at the hospital. [frame sections 1, 5, 9]
- C2. Ellis can be bought once, for exactly £800 in cash in Frank's hand that night (not from the tin), then £100 every Friday. A missed week ends it and she is never bought twice. In cast_src.py (carol_ellis, line 109) change r= to "Detective Sergeant, CID; can be bought once, for £800 in cash, then £100 every Friday; a missed week ends it". Set venal to 0.2 (recommended; dutiful then follows as 0.84). police.json already holds the price (price_pounds 800, weekly_pounds 100, paid_only_from_cash true): no change there. [frame section 2; scene 14]
- C3. Ron's charge in the cells is conspiracy to evade duty on the landing's loads; he is remanded. Put it in his card's "life" line in cast_src.py. [owner's ruling, 24 November; scenes 14, 18]
- C4. Danny once drove car two for Mickey, for nine years, and kept the key. The file says "his key to car two": add "a brass key on a black leather fob" to the card's secret in cast_src.py. The key he hands Frank is a Yale to the empty unit's side door. [frame section 9; scene 6]
- C5. Craig Fewson is met in week one on the wall beside Danny, where he sets Danny's driving seat to fit himself. He speaks in scenes 6 ("So whose are we?") and 19 ("I want to see what you do"); in scenes 5, 17 and 23 he is present with no line. Add this to his card in cast_src.py. [frame section 4; scenes 5, 6, 19]
- C6. If Danny is given the top line and never turns, or is gone, Fewson has the brass key and is the man on the quay. The file's fallback_role already says he takes Danny's ladder, key and grudge: no change. [SPINE-CARDS.md]
- C7. Ron cannot drive. Every morning since Mickey died he starts car two and sits in it with the handbrake on. Add one sentence to his card's "life" in cast_src.py. [frame section 3; scene 1]
- C8. Ron stood the pen thirty-six years, not thirty. The card says "a docker for thirty years"; change it in cast_src.py. [scenes 7, 11, 16]
- C9. Ron carries brass tally 39 from week three. It is a prop and a tie to Stathers (T below). [scenes 8, 11, 14, 16, 18, 22]
- C10. Sheila's red book has a third column "Brought in by", with "R. Kirby" down it. Add it to her card's secret in cast_src.py (it is a tie to Ron). [scene 9]
- C11. Mark Billany is at the Landing on the stage, with a stitched eyebrow if struck, and goes to the van to lean on the horn. The earlier frame had him driving the van. Change his card in cast_src.py. [scene 10]
- C12. Garbutt says the week's aim in weeks four, five and six. His role is unchanged: no change. [S22, S27, S40]
- C13. Agar's brief on the night between: Simon Ombler opens the Exchange door and makes the offer; the man who goes to the station is unnamed. Anthony Raine is the likely holder, or none. Reword Raine's role in cast_src.py to match. [scene 14]
- C14. Ellis's force: CASTING.md says Humberside CID; the data scrubbed real forces to "CID" (build_cast.py, line 48). The game's text says CID. No data change. [CASTING.md; cast.json]
- C15. Neil Screeton is in the yard only if Frank took the £80 debt off Iveson. Add it to his card in cast_src.py. [frame section 4; scene 15]
- C16. The Widow's ally clause no longer says "his landlord at the gate". Her men stand his posts and stay hers. Check her card in cast_src.py for the landlord clause and drop it. [frame section 3]

### Ages, where scene and file disagree

- C17. Agar: 62 on the approved sheet, in the file and now in scene 17. No change.
- C18. Craig Fewson: scene 5 says thirty; the file says 25; no sheet. The scene wins for now: cast_src.py a=25 becomes 30. The lead may overturn it.
- C19. Derek Hebblewhite: scene 20 says fifty; the file says 49; no sheet. The scene wins: cast_src.py a=49 becomes 50.
- C20. The old firm's man: scene 3 says "past sixty"; cast_src.py says 60 and people_fix.py FIELDS says 59; no sheet. The scene wins: people_fix.py a becomes 61.
- C21. At 61 the data's own cover rule (age 60 or over) sets his can_die to false. His fb stays (build_people.py already keeps it for him). His burial (A7) is scripted, not a kill.
- C22. Ron is 58 as on the sheet. The thirty-six years are at the pen (C8), not his age.
- C23. Every other age agrees: Danny 27, the Widow 57, Terry 52, Ellis 40, Frank 32.

### Layer moves

- C24. Down to layer 3 from the earlier frame's supporting items: Simon Ombler and Alan Sowerby (item 1), Wayne Harrison (item 13), Ian Megginson, Karen Grummitt and Shaun Hewson (item 14). [working/STORY-FRAME-v2-before-paper.md section 4]
- C25. Not in the earlier frame's list at all, and layer 3 in the cast: Hal Metcalfe (named among "the other regulars"), Doreen Harland, Peter Tang, Sylvia Rennison, Dawn Pybus, Colin Mastin, Albert Suggitt, Christine Pickering, Tracey Scarth, Gordon Leckenby, Gary Mawer, Winifred Duggleby, Nora Cronin. They come from the side cards' givers.
- C26. Thirteen of these residents give a side story each (D03, D05, D06, D12 to D18, D20, D21, D24). A side story is not a spine beat, so the rule holds.
- C27. Data kinds do not match the layers: eight "principal" files are layer 2 (Ada, Alison, Walsh, Darren, June, Garbutt, Agar, Danby), three "firm" files are layer 2 (Pauline, Kevin, Terry). The new layer field (A8) replaces the guess.

### New ties the story needs

ties.json has 147 rows and 29 dropped never-meet rows. Each row below is added to people_fix.py EXTRA_TIES with the strength shown and, where the meeting is not a routine, a BY_MESSAGE text. A row meeting by routine says where and when.

Decision on Frank and Mickey: both get rows. Frank is the player and has no routine; every row of his is by message ("the story brings the person to him": a card or scene is the meeting). Mickey is dead; every row of his is by message ("his name on the board, his book, his letter").

| Pair | Strength | How they meet | Source |
|---|---|---|---|
| Ron, Lily Tang (restore) | 0.5 | by message: Friday at the takeaway counter, two of number nine, then one | D04, S39 |
| Ron, Stathers (restore) | 0.5 | by message: the six o'clock call at the pen, from week three | scenes 8, 11 |
| The Widow, Ron (restore) | 0.4 | by message: her men at the gate; once in Mickey's office | scene 16 |
| Danny, Sheila (restore) | 0.4 | by message: Danny's visits to the counter | scenes 5, 6 |
| Danny, Pauline (restore) | 0.4 | by message: car two on the radio | scenes 6, 19 |
| Ron, Ellis | 0.5 | by message: the station, his statement | scenes 14, 18 |
| Sheila, Ellis | 0.4 | by message: the search at the office, Friday 16 November, seven | scene 13 |
| Ron, Rita | 0.4 | by message: Rita's window and the ticket for Mickey's watch | D19 |
| Ron, Hal Metcalfe | 0.3 | by message: Monday at Rita's | D19 |
| Ron, Mark Billany | 0.4 | by message: the ferry rank, seventeen hundred | scene 7 |
| Hebblewhite, Sheila | 0.6 | by routine: mickeys 09:15 Thursday, 09:00 Friday | scene 20 |
| Garbutt, Hal Metcalfe | 0.4 | by message: Monday, pager and phone box | S22, S40 |
| Garbutt, Grace | 0.5 | by message: her back room, Monday 26 November | S27, S46 |
| The Widow, Agar | 0.3 | by message: Grace's table, once; letters about the cold-store road | scene 17 |
| Danny, Sylvia Rennison | 0.3 | by message: the boarding-house step on Friday | D20 |
| Danny, Wardell | 0.3 | by message: the station's back step on the hour | S38, S53 |
| Ellis, Norman Dent | 0.3 | by message: the row at night, his description in her notebook | D22, S36 |
| Ombler, Christine Pickering | 0.3 | by message: the harbour office counter, his request for the lease | D16 |
| June, Gordon Leckenby | 0.4 | by routine: ferry_landing 11:00 Saturday | D15 |
| June, Tracey Scarth | 0.3 | by message: her market stall, Mickey's coat | D05 |
| Winifred Duggleby, Iveson | 0.3 | by message: the chapel, the lead | D18 |
| Grace, Peter Tang | 0.4 | by message: she sends for him on the night of the yard | scene 15 |
| Fewson, Ron | 0.4 | by routine: rank_ferry 17:00 daily; and the quay on the last day | scene 19 |
| Ellis, Father Walsh | 0.3 | by message: the station cells | D17 |
| Julie, Pauline | 0.7 | by message: the night desk and the day desk hand over | D02, D09 |
| The Man in Black, Grace | 0.3 | by routine: chapel 10:00 Sunday; and her caff on funeral days | scenes 17, 21 |
| The Man in Black, old firm's man | 0.3 | by message: his funeral, Monday 26 November | scene 17 |
| Karen Grummitt, Gordon Leckenby | 0.5 | by routine: ferry_landing 06:30 Monday to Saturday | scenes 1, 23 |
| Ian Megginson, Norman Dent | 0.3 | by message: the warehouse row and the yard lights | D03, D22 |
| Tracey Scarth, Grace | 0.3 | by message: the caff window; she saw a man run | D10 |
| Frank, Ron | 0.9 | by message: the story brings him (scene 2 on) | frame section 3 |
| Frank, Sheila | 0.8 | by message: the book each morning | scene 4 |
| Frank, Danny | 0.8 | by message: scenes 5, 6, 19 | frame section 3 |
| Frank, Pauline | 0.7 | by message: the radio | scene 1 |
| Frank, the Widow | 0.6 | by message: S16, scene 16, scene 17 | frame section 3 |
| Frank, Ellis | 0.6 | by message: scenes 13, 14, 20 | frame section 3 |
| Frank, Garbutt | 0.5 | by message: scenes 10, 17 | frame section 4 |
| Frank, June | 0.5 | by message: D05, D15 | SIDE-CARDS.md |
| Frank, Darren; Frank, Grace; Frank, Rita; Frank, Father Walsh | 0.5 | by message: scenes 2, 15, 14, 18 | cards and scenes |
| Frank, Agar; Frank, Ada; Frank, Lily Tang; Frank, Stathers; Frank, Fewson; Frank, Kevin; Frank, Terry; Frank, Julie; Frank, Hebblewhite; Frank, Alison; Frank, Wardell; Frank, Lee Drewery; Frank, Tharratt | 0.4 | by message: the card or scene that names each | frame section 4 |
| Frank, Danby; Frank, Gordon; Frank, Shaun; Frank, Iveson; Frank, Brenda; Frank, Ozols; Frank, Garton; Frank, Screeton; Frank, Billany | 0.3 | by message: the card or scene that names each | frame section 4 |
| Mickey, Ron; Mickey, Sheila | 0.9 | by message: his arrangement, his book | frame section 2 |
| Mickey, June | 0.8 | by message: his letters, the parcel | D15 |
| Mickey, Frank; Mickey, the old firm's man | 0.7 | by message: his letter and the envelope | scene 6; scene 3 |
| Mickey, Pauline; Mickey, Danny | 0.6 | by message: his radio; car two | scene 6 |
| Mickey, the Widow; Mickey, Walsh; Mickey, Ada | 0.5 | by message: told her no thirty years; his confession; his Thursdays | scenes 16; S26; S07 |
| Mickey, Agar | 0.4 | by message: his licence renewed unasked | frame section 2 |

Ties that stay dropped: Danny and Grace (the story reaches her through his man at her sink, not through him); Danny and Kevin; Danny and Terry (no scene for them). Brenda and the porter: the story says only "the porter", so no tie to Eddie Birtwhistle unless he is cast. [D10, D08]

## Clashes

The rule: no first name one letter from a principal's (REGULARS.md).

- K1. Roy Bellwood, the custody sergeant, is one letter from Ron Kirby. The scenes never name him; only the file does. Change the first name in cast_src.py (sgt_bellwood), for example to Alec.
- K2. Brenda Laverack and Father Brendan Walsh are one letter apart. Brenda is on the approved regulars sheet, so she stays. They never share a scene, and Walsh is called Father Walsh in every line. [D08; D17]
- K3. Julie Kettlewell and June Suddaby sound alike. Julie is in scenes 15, 16 and 22; June is in scene 1 only; they share no scene. Both stay on their sheets.
- K4. Kevin Needham and Keith Garbutt share a first letter and a sound, and sit together on S22 and S27. Both stay; Garbutt is "Mr Garbutt" or "Garbutt" in speech.
- K5. Frank Nowak and Frank Stathers. Kept on purpose: "There's one Frank on this gate, and he was here first." Everyone else says Stathers. [scene 8; frame section 9]
- K6. Carol Ellis and Karen Grummitt sound alike. They share no scene. Stays.
- K7. Philip Danby and Phil Rawling (the glazier, unused). Rename the glazier if he is ever called up.
- K8. Unused pairs that sound alike: Shaun Hewson and Shane Boddy; Terry Hodgson and Terence Bould; Dougie Saltmarsh and Douglas Fenwick; Stan Pickles and Stanley Hirst; Ken Swales and Kenny Varley. Rename the unused one if he is ever called up.
- K9. The Peter in scene 15 is Peter Tang, now named in full. No other Peter exists. No change.
- K10. Nowak is misspelt on purpose: "Nowack" by Stathers, the Widow's receipt and the sergeant; "Nowek" by Agar's letters; "Novak" and "Knowak" by the sergeant. The lines build must not correct them. [S16, S17; scenes 8, 11, 14, 16]
- K11. The Widow is the Widow, Mrs Jensen, Maureen Jensen and M. Jensen (gate entries). One person, id maureen_jensen.
- K12. Lily Tang keeps her own surname Wong on her sheet ("Lily Tang (Wong Mei-ling)"). The story and the file use Tang. No change.
- K13. The rent collector in scene 1 is "D.P.", which matches Dawn Pybus. The file also holds a Leonard Askew as the landlord's agent. The story uses D.P. as Dawn Pybus and leaves Askew an unnamed landlord's man.
- K14. The id mickey_suddaby must never stand in for "Mickey's", the firm.

## Fixes owed by the scenes and cards

- F1. Scene 23 shows no stranger with a suitcase. Card S61 has him. Recommendation: S61 drops him.
- F2. Cards S35 and S52 say "a constable". The frame names PC Garton as the bought one, who looks away from a car once for £50; neither card uses that act. Question for the lead. Recommendation: add the act to one card (S52, on his beat), or drop Garton to an unnamed role.
- F3. Which scene claims the first time Nowak is spelt right? The sergeant writes it right after Ron spells it (week five, scene 14). Agar says it right on Monday 26 November (week 7, scene 17). The Customs letter is addressed right in week 6 (S47). Ellis says it right from the start, Pauline from week two and Ombler types it right from Tuesday of week 7. Question for the lead. Recommendation: none is "the first"; each is the first of its kind.
- F4. Card S43 lists Colin Mastin as a first carrier, and S29 and S52 use Ian Megginson and Ombler. Residents carry no spine beat, so a layer-2 carrier goes first. S24's first carrier is already Ron; S46's fallback is Ombler for Agar.
- F5. A sheet is owed for the Man in Black (no casting sheet exists). He is tall and in black in scene 17. [casting, not a scene]
