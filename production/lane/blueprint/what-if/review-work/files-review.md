# Fresh review of the finished files (24 Nov 2026)

Reviewer: fresh Opus 5.5, about 30 minutes. Read: LONG-HEAT.md, PROPOSED-PARTS.md, BREAKER-PLAYTESTER.md, SUMMARY.md; canon.md and RULINGS.md (scratchpad copies); BLUEPRINT-01 (1.1.5, 1.3.4, 1.3.6, 1.6.2, 1.6.7, 1.6.10, 1.6.15, RT-09, DP5-C03) and BLUEPRINT-02 (2.5, 2.6, 2.10, 2.11.3, 2.14 to 2.18, RT-07, RT2-05, RT2-06); data/police.json; QUESTIONS.csv counts (216: 150 weak, 42 well, 24 unanswered, matching the summary). Style check: no em-dashes, no italics, no American spellings, no GTA VI story, no Mafia reference found in the four files. 25 items: 10 must-fix, 15 should-fix, most serious first.

## Must-fix

1. SUMMARY.md, Detail, "Data still contradicting": says this job changed RT2-02's text in BLUEPRINT-02 and the police.json row "(see the commit)". Neither has changed: RT2-02 still says a struck officer "knows it was him" and ends "(gap)", and police.json still has tom_never_lays_hands_on; LH-12 meanwhile says the keeper does it. Fix: make both edits before the commit, or reword the line to "listed for the keeper".

2. LONG-HEAT.md, LH-12: replaces RT2-02 but leaves the same rule in 2.6.3 ("An officer struck by Frank is a witness who knows it was him, so no statement is needed"), and the new personal radio contradicts 2.6.1 and 2.6.6 ("carry only a truncheon"). Fix: name 2.6.3's sentence and both "only a truncheon" lines as replaced too.

3. LONG-HEAT.md, LH-07 and LH-09: court scenes and a remand prison contradict 2.6.9 ("there is no court scene and no prison"), and the remand road replaces 2.6.4's and RT2-02's "22 hours and a charge, which removes the best turn of every ending", without saying so. Fix: list those sentences as superseded, and say what a dismissed or acquitted killing does to the endings (does the charge still remove the best turn?).

4. LONG-HEAT.md, LH-06 and LH-14d: a weapon's prints link to Frank "only" if his prints are on file from an earlier Meridian arrest. Wrong for 1990: once he is arrested on suspicion (LH-06's own arrest), PACE s.61 lets the police take his prints and compare them with the weapon directly. Fix: prints link after any arrest in this case; the earlier-file rule only decides whether a print points to him before he is a suspect.

5. LONG-HEAT.md, LH-06 (gloves) and LH-14d (search reaches): gloves free with the dark coat cancel every print, and a weapon dropped more than 100 m from the spot (or 50 m into the dock) is never found, so an unseen killing is trivially clean. Fix: widen the reaches to the routes from the spot (to Mickey's, the landing, the yards' lane) for a police killing, and make gloves a mark at night (a man in gloves is noted) or able to carry blood.

6. LONG-HEAT.md, LH-07, with PROPOSED-PARTS P01 and P02: the dead-end standard (an act that can change the count every remand day) can fail when Ron and Sheila are gone and every helper is hostile, since visits are the only channel. Fix: in 1990 legal visits were separate from the daily social visit; give a solicitor's visit on top of the daily one, always available, always offering one act (challenge an identification, test an alibi, find a witness to take back).

7. LONG-HEAT.md, LH-02 to LH-09 (the calendar): squad week, eight remand days, a trial week and an appeal week take about 3.5 of the roughly 7 game weeks his clock ruling sets. Nothing says how this sits in the seven-week arc or whether a late killing can run the game out. Fix: one paragraph saying story beats fire on states (BLUEPRINT-07), remand days are skipped hours, and the week-7 end cannot fall during the long heat (or what happens if it does).

8. PROPOSED-PARTS.md, P05, against 1.6.15 and P12: robbery of a person "at any rung, whatever the hold-up gate says" contradicts 1.6.15 ("Never in Act I", which covers people with a purse), and P12 has a shopkeeper never hand over before rung 2 while P05's man in the street does. Fix: either P05 states it replaces 1.6.15's people clause, or Act I street threats follow P12 (the man refuses or runs, and it is reported as an assault with a weapon).

9. LONG-HEAT.md, LH-04: killing a knower "makes Frank the squad's man at once" even when unseen and unlinked. That breaks FF-05 (police know only what someone perceived or a search found). Fix: only if her lead or statement already named him, or a slot ties him to her death.

10. PROPOSED-PARTS.md P03 and SUMMARY.md gap 5: "an arrest never takes his money" and "cash is never taken", while P03 keeps cash in the envelope that he cannot account for, for a game week. Fix: "cash is listed and returned, except a sum held as evidence, returned in a week unless it joins a charge", in both files.

## Should-fix

11. LONG-HEAT.md, LH-08: a "lost" statement in a HOLMES-indexed inquiry (the file's own source) would be noticed and the witness simply seen again; and officers on a colleague's murder are the least likely to sell. With Garton, Wardell and Ellis also bought, it starts to read as a thesis. Fix: a lost statement holds only until the squad's next visit to her unless she is also turned; on a constable's killing the bribe costs double or is not offered.

12. LONG-HEAT.md, LH-05 and LH-13: Ellis signing a statement about payments she took, and keeping a record of them in her desk, are implausible (she would be incriminating herself), and proof of bribery is not proof of murder. Fix: make either one a lead or a separate corruption charge, worth at most 1 point toward the murder count.

13. LONG-HEAT.md, LH-03: "Mickey's people back him unasked (ruling of 1 Oct)". The ruling says they never go to the police about one of their own, not that they give a false alibi in a murder inquiry. Fix: they never inform; whether they lie for him follows their temper and what they actually saw.

14. LONG-HEAT.md, LH-03: "what he says is written down and later checked" cannot be built or tested as free talk. Fix: the account is a few structured claims (where, when, with whom), classified from talk by the model and checked by the Core against knowers' slots and the fare book.

15. LONG-HEAT.md, LH-05 and LH-08: a rival's and Garbutt's "hook" on Frank cites RT-07, but RT-07 only defines hooks Frank holds. Fix: write the reverse hook as a part (what it is, when it is spent, how Frank takes it back), with a test.

16. LONG-HEAT.md, LH-05: his ruling says "the rival heads gain a hold on him" without condition; LH-05 gives a hold only to heads whose people saw or heard something. That is defensible under 2.10.2 but differs from his words. Fix: say so plainly in LH-05, and add the squad's cost to their business (LH-02) as something that counts, so a clean killing still gets him leaned on.

17. LONG-HEAT.md, LH-03 and LH-10: Crimestoppers and the Police Memorial Trust are real organisations. Canon's brands rule (all fictional) bars their names on in-game posters or a plaque. Fix: the posters show a generic anonymous line and the plaque has no maker's name; keep the real names in the sources only.

18. LONG-HEAT.md, LH-02: a police killing in 1990 brought dozens of officers, often more, under a Detective Chief Superintendent; "six detective constables" is far too few, and £5,000 is low for a police-murder reward. Fix: say the pairs on the street stand for a larger inquiry, consider Det Ch Supt, and mark the reward for checking against period cases.

19. LONG-HEAT.md, LH-07: in 1990, prison visits took place under officers' supervision, yet an order passed through a visitor to frighten a witness carries no risk of being heard. Fix: an order to frighten or pay a witness given in a visit can be overheard (a fixed chance by visit type, or always when the visitor has low nerve), adding the interference point.

20. LONG-HEAT.md, LH-13 and LH-14c: "his crew's loyalty dips if they hear it was needless" has no definition anyone could test. The town reading a blow on a woman or anyone over sixty as heavier touches the line he has just dropped and falls in his violence area. Calling the kick "cruelty" invites a clash with canon's "no cruelty as spectacle". Fix: define "needless" (for example, the target was down, pleading or not resisting), show him the heavier-reading rule as an overturnable line, and say "vicious" rather than "cruelty".

21. SUMMARY.md, the top: about 430 words is not short or one phone screen. Questions are numbered 1 to 5, while LONG-HEAT and BREAKER call them Q-H1 to Q-H5. Gap 6 says "daily visits" (it is daily except Sunday). The bank ruled out at release is a scope choice, and scope is his to decide. Fix: cut to about 200 words (five gaps, the decisions in three short lines), label the questions Q-H1 to Q-H5, and mark the bank as "scope: yours to overturn" in the top.

22. Citations: P10's "the last-seen search's 80 m" is not in DP5-C03, which is time-based (30 to 120 s). P14's "Ron and Sheila cannot be dismissed in Act I (as today)" is not in 2.11.3. LONG-HEAT says to fold into 2.6 and 2.16 but also changes 2.5.5 ("a sunk body is never found"). P13's "next price half again" applies to a truce that 2.10.4 offers once a game. Fix each citation, or mark the new rule as new.

23. PROPOSED-PARTS.md, P01: Ron gone for good after a third blow collides with canon's story frame ("the big loss is Ron going inside unless Frank pays"). Fix: give the fallback (the loss falls on the next crewman, or Ron's remand beat still fires from outside the firm).

24. Plausibility, small: LH-14d's "washing takes blood off, not prints" (washing can spoil prints too); P03's paid solicitor at £10 a visit is far below 1990 rates, and legal aid covered representation at committal for any indictable charge, not only a killing. Fix: soften the washing rule to "blood off, prints only sometimes" (deterministically by surface), raise the fee, and drop "only for a killing".

25. Clarity: LH-10's "challenges Frank's known men on cause, never on suspicion only" reads both ways. BREAKER-PLAYTESTER says "never edit saves" yet sets up "from a save made for it" and blames "save tools". Fix: "treats Frank's known men as having cause"; say the setup saves are made by the loop's save tool before the breaker starts, not by the breaker.
