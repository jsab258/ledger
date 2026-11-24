Verdict: pass after must-fixes.

Review of paper/CAST.md, 24 November 2026, by a fresh reviewer, against the brief (PAPER-BRIEF.md sections 1 to 5 and 7, and the lead's two later decisions), the revised frame, the 23 scenes, SPINE-CARDS.md, SIDE-CARDS.md, CASTING.md, REGULARS.md and the people data files.

What was checked and holds: layer sizes (core six; supporting 29 living plus Mickey, inside 20 to 30; 19 named residents, 13 of them givers, as the table says). Every age against CASTING.md and REGULARS.md, including the 17 regulars who sit in the residents' table. Every quoted line (about 90) was searched for word for word in the scenes, cards, frame and REGULARS: all are there, and each speaker matches. No em-dash, no italics, no Tom or Tommy as a name in use, no Mafia, no GTA VI, no drink, betting or children, no quotation of the owner.

## Must fix

1. Geoffrey Agar, Age line: "Scene 17 says seventy: the scene owes the fix" is no longer true. Scene 17 now says "Agar, sixty-two" (CAST-CHANGES F1 marks it fixed on 24 November). Delete the second sentence, and the same stale claim in CAST-CHANGES C18.
2. DS Carol Ellis, Path notes: "about £800 from the tin" goes against the lead's later decision and scene 14, which need exactly £800 in cash in Frank's hand that night ("Only if he has eight hundred pounds in cash on him; without it she is a detective in a car"). Write "£800 in cash, in his hand that night, then £100 every Friday". CAST-CHANGES C2 needs the same change.

## Should fix

1. Maureen Jensen, Path notes: "She cannot die (Frank's line covers every woman)" gives a reason no source holds. Neither canon, the frame, the brief nor the scenes have a rule about women dying, and a data writer could take it as a rule for every woman. Keep "She cannot die" (maureen_jensen.json has can_die false) and drop the bracket, or point to the real source.
2. Ron Kirby and Sheila Dunn, Path notes: the owner's decision 4 counts Ron and Sheila as friends at the ending, next to Alison and Danby. Alison's and Danby's entries say so; Ron's and Sheila's do not. Add one line to each.
3. Named residents table, Sylvia Rennison: "scenes 2, 3, 21, 23". She is not in scene 21. Make it "scenes 2, 3, 23".
4. The Man in Black, Role: "Speaks in scene 17 and in each close." He speaks in scenes 17, 21 and 22, and not in scene 23 (Burn Both). Name the three scenes, or give him a line in scene 23.
5. Frank Stathers, Age: "he has had the gate twenty years, scene 11". The twenty years are in scene 8. Change the scene number.
6. June Suddaby, Ties: "Sylvia Rennison (lodges at Regent House, data)" reads as if Sylvia is the lodger. Write "Sylvia Rennison (June lodges at her boarding house, Regent House; data)".
7. Julie Kettlewell, Ties: "the Widow (lets her in, scene 16)" reads the wrong way round. Write "the Widow (on the night desk, Julie may be the one who lets her in, scene 16)".
8. Darren Milner, Role: "sleeps in the spare car" sounds like where he lives. His approved sheet and darren_milner.json have him living at his mother's. Write "lives at his mother's; in The night lodger (D03) he sleeps in the spare car".
9. Unnamed roles, the custody sergeant: "sgt_bellwood (Roy Bellwood, 52)". REGULARS.md does not allow a first name one letter from a principal's, and gives Roy and Ron as its own example. CAST-CHANGES K1 already flags this. Give the person a new first name here, or mark it "name owed a change (K1)".
10. Philip Danby, Role: the line about his sheet making him a teacher at the comprehensive is correct, but REGULARS.md's content rule bars teaching from any line because it cannot be spoken of without children. Add "never said in any line or routine", so a data writer does not put it into his routine.
11. DC Graham Wardell, Ties: "Sheila (the property book)". The cards make the property book Wardell's own (S36: "DC Wardell's property book"). Write "Sheila (he works through the drawers with his property book while she sits with her handbag)", or drop the tie.
12. Alison Sedman, Role: "reporter on the Pilot". A reader who is not a programmer will not know the name. Write "the Meridian Pilot, the local paper", as alison_sedman.json and CASTING.md have it.
13. Geoffrey Agar, Carries: "S40" is the only card in the list with no title (S40 The week-six aim). Add the title, and say what Agar does in it, since Garbutt is the person who says that aim.
14. Philip Danby and PC Trevor Garton, Voice: both say "A line is owed", but nothing says who writes it or where it is tracked. Add both to CAST-CHANGES as owed items, so they are not lost.
15. Pauline Kitching, Role: the ladder she says aloud stops at week five ("nothing at all"). The frame's table also gives week six ("his name, said carefully") and week seven ("what the week has earned"). Add those two, so her line on the air is set for every week.
